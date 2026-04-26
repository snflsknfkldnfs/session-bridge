#!/usr/bin/env python3
"""
Phase 5 P1: Skript-Mock für session-bridge Lifecycle.

Simuliert 12-Round-Pair-Lebenszyklus von init bis close, validiert nach jedem
Schritt state.json gegen bridge_state_v1 + handover gegen handover_frontmatter_v1.

Akzeptanz P1 (ADR_0029 Phase 5):
  - Alle Phase-Übergänge konsistent (init→scope-lock→iterate→execute→verify→close)
  - State.current_round == len(state.rounds)
  - Jeder handover-Frontmatter validiert PASS
  - Schema-allOf-Pflichten erfüllt (acceptance_criteria, rollback_triggers, ...)
  - drift_factor in close-Phase berechnet
  - Atomic-Write-Pattern simuliert (read-mutate-CAS-write)

Usage:
  python3 pilot_lifecycle_mock.py [--shared-path=<path>] [--verbose]
"""

import argparse
import json
import os
import sys
import uuid
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPT_DIR.parent.parent / "plugin"
SCHEMAS_DIR = PLUGIN_ROOT / "schemas"


def now_iso(offset_seconds: int = 0) -> str:
    return (datetime.now(tz=timezone.utc) + timedelta(seconds=offset_seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")


def short_uuid() -> str:
    return uuid.uuid4().hex[:8]


def atomic_write(path: Path, data: dict) -> None:
    """Atomic-Write via tmp-file + rename (ADR_0029 §13.2)."""
    tmp_path = path.with_suffix(path.suffix + f".tmp.{short_uuid()}")
    tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    tmp_path.rename(path)


def read_state(state_path: Path) -> dict:
    return json.loads(state_path.read_text())


def cas_write_state(state_path: Path, expected_updated_at: str, new_state: dict) -> bool:
    """CAS-Write: rename only if current updated_at matches expected."""
    if state_path.exists():
        current = read_state(state_path)
        if current["updated_at"] != expected_updated_at:
            return False
    new_state["updated_at"] = now_iso()
    atomic_write(state_path, new_state)
    return True


def write_handover(handover_dir: Path, frontmatter: dict, body: str) -> Path:
    short = short_uuid()
    name = f"{frontmatter['round']}-{frontmatter['from']}-{frontmatter['to']}-{short}.md"
    path = handover_dir / name
    yaml_lines = ["---"]
    for k, v in frontmatter.items():
        if isinstance(v, (dict, list)):
            yaml_lines.append(f"{k}: {json.dumps(v)}")
        elif isinstance(v, bool):
            yaml_lines.append(f"{k}: {'true' if v else 'false'}")
        else:
            yaml_lines.append(f"{k}: {v}")
    yaml_lines.append("---")
    content = "\n".join(yaml_lines) + "\n\n" + body + "\n"
    path.write_text(content)
    return path


class PilotResult:
    def __init__(self):
        self.steps = []
        self.failed_steps = []

    def step(self, name: str, ok: bool, details: str = "") -> None:
        self.steps.append((name, ok, details))
        if not ok:
            self.failed_steps.append((name, details))

    def summary(self) -> str:
        total = len(self.steps)
        passed = total - len(self.failed_steps)
        lines = [
            f"\n{'='*70}",
            f"Pilot P1 (Script-Mock) Summary: {passed}/{total} steps PASS",
            f"{'='*70}",
        ]
        for name, ok, details in self.steps:
            mark = "✓" if ok else "✗"
            lines.append(f"  {mark} {name}" + (f" — {details}" if details else ""))
        return "\n".join(lines)

    def exit_code(self) -> int:
        return 0 if not self.failed_steps else 1


def setup_run(shared_path: Path) -> tuple[Path, Path]:
    """Bereite shared_path/bridge/ vor, leere ggf. alte Run-Daten."""
    bridge = shared_path / "bridge"
    if bridge.exists():
        shutil.rmtree(bridge)
    bridge.mkdir(parents=True)
    (bridge / "handover").mkdir()
    (bridge / "artifacts").mkdir()
    (bridge / "orphans").mkdir()
    return bridge / "state.json", bridge / "handover"


def main(shared_path: Path, verbose: bool = False) -> int:
    print(f"Phase 5 P1 Script-Mock starting (shared-path: {shared_path})")

    try:
        import jsonschema
    except ImportError:
        print("[FATAL] jsonschema not available — cannot run Pilot.")
        return 2

    # Schemas laden
    state_schema = json.loads((SCHEMAS_DIR / "bridge_state_v1.json").read_text())
    handover_schema = json.loads((SCHEMAS_DIR / "handover_frontmatter_v1.json").read_text())

    # Setup
    state_path, handover_dir = setup_run(shared_path)

    pilot = PilotResult()
    pair_id = str(uuid.uuid4())

    # ============================================================
    # Step 1: /bridge-init (advisor side)
    # ============================================================
    state = {
        "pair_id": pair_id,
        "schema_version": "1.0.0",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "phase": "init",
        "roles": {
            "advisor": {
                "session_id": "local_advisor_mock",
                "expertise_source": "pilot-script-mock",
                "active_since": now_iso(),
            },
            "worker": {
                "session_id": "",
                "active_since": now_iso(),
            },
        },
        "topic": "pilot-script-mock-topic",
        "current_round": 0,
        "rounds": [],
        "open_blockers": [],
        "decision_log": [],
        "status_observations": [],
        "file_ownership": {},
        "shared_artifacts": [],
        "wallclock_estimates": [],
        "rollback_plan_path": None,
    }
    # NOTE: we'll fill worker post-attach. For schema validity at this point we need
    # to allow temporary-empty worker. The schema requires session_id+active_since
    # in worker — we satisfy with empty string + now timestamp; attach overwrites.
    try:
        jsonschema.validate(state, state_schema)
        atomic_write(state_path, state)
        pilot.step("Step 1 /bridge-init", True, "phase=init advisor-Rolle gesetzt")
    except jsonschema.ValidationError as e:
        pilot.step("Step 1 /bridge-init", False, str(e.message)[:200])
        print(pilot.summary())
        return pilot.exit_code()

    # ============================================================
    # Step 2: /bridge-attach (worker side) → phase init→scope-lock
    # ============================================================
    state = read_state(state_path)
    expected = state["updated_at"]
    state["roles"]["worker"] = {
        "session_id": "local_worker_mock",
        "current_focus": "plugin-pilot-test",
        "phase": "phase-1.6",
        "active_since": now_iso(1),
    }
    state["phase"] = "scope-lock"
    try:
        jsonschema.validate(state, state_schema)
        ok = cas_write_state(state_path, expected, state)
        pilot.step("Step 2 /bridge-attach", ok, "phase=scope-lock worker-Rolle gesetzt")
    except jsonschema.ValidationError as e:
        pilot.step("Step 2 /bridge-attach", False, str(e.message)[:200])
        print(pilot.summary())
        return pilot.exit_code()

    # Helper: schreibe handover + update state.rounds + auto-phase
    def add_round(round_type: str, initiator: str, extra_frontmatter: dict = None,
                  body: str = "Mock body", phase_override: str = None,
                  blocker: dict = None, decision: dict = None,
                  observation: dict = None) -> tuple[bool, str]:
        nonlocal state
        state = read_state(state_path)
        expected_local = state["updated_at"]
        new_round = state["current_round"] + 1

        from_role = initiator
        to_role = "worker" if initiator == "advisor" else "advisor"

        worker_phase = state["roles"]["worker"]["phase"]
        worker_focus = state["roles"]["worker"]["current_focus"]

        frontmatter = {
            "pair_id": pair_id,
            "round": new_round,
            "from": from_role,
            "to": to_role,
            "type": round_type,
            "timestamp": now_iso(new_round * 60),  # spaced 1 min apart
            "worker_phase": worker_phase,
            "worker_focus": worker_focus,
            "status_verified_at": now_iso(new_round * 60),
            "references": [
                {"type": "filesystem", "pointer": f"/mock/path/round-{new_round}", "verified": True}
            ],
        }
        if extra_frontmatter:
            frontmatter.update(extra_frontmatter)

        # Schema-Validate VOR Persistierung
        try:
            jsonschema.validate(frontmatter, handover_schema)
        except jsonschema.ValidationError as e:
            return (False, f"frontmatter schema FAIL: {e.message}")

        artifact_path = write_handover(handover_dir, frontmatter, body)
        rel_path = f"bridge/handover/{artifact_path.name}"

        state["rounds"].append({
            "round": new_round,
            "type": round_type,
            "initiator": initiator,
            "artifact_path": rel_path,
            "timestamp": frontmatter["timestamp"],
        })
        state["current_round"] = new_round

        if phase_override:
            state["phase"] = phase_override

        if blocker:
            state["open_blockers"].append(blocker)
        if decision:
            state["decision_log"].append(decision)
        if observation:
            state["status_observations"].append(observation)

        if "wallclock_estimate_min" in frontmatter:
            state["wallclock_estimates"].append({
                "round": new_round,
                "estimated_min": frontmatter["wallclock_estimate_min"],
                "actual_min": None,
                "drift_factor": None,
            })

        try:
            jsonschema.validate(state, state_schema)
        except jsonschema.ValidationError as e:
            return (False, f"state schema FAIL: {e.message}")

        ok = cas_write_state(state_path, expected_local, state)
        return (ok, f"round={new_round} type={round_type}")

    # ============================================================
    # Step 3: handover type=status (advisor)
    # ============================================================
    ok, det = add_round("status", "advisor",
                        observation={"round": 1, "observed_by": "advisor", "fact": "worker auf phase-1.6", "verified_against": "transcript"})
    pilot.step("Step 3 handover status (advisor)", ok, det)

    # ============================================================
    # Step 4: handover type=status (worker)
    # ============================================================
    ok, det = add_round("status", "worker",
                        observation={"round": 2, "observed_by": "worker", "fact": "Validatoren grün", "verified_against": "filesystem"})
    pilot.step("Step 4 handover status (worker)", ok, det)

    # ============================================================
    # Step 5: handover type=initial-advice (advisor) → phase scope-lock→iterate
    # ============================================================
    ok, det = add_round("initial-advice", "advisor", phase_override="iterate",
                        body="3 Optionen: A B C — Empfehlung A")
    pilot.step("Step 5 handover initial-advice → iterate", ok, det)

    # ============================================================
    # Step 6: handover type=counter (worker) — Falsifikation
    # ============================================================
    ok, det = add_round("counter", "worker",
                        body="Option A faktisch falsch wegen X",
                        blocker={"id": "B-1", "summary": "Annahme X falsch", "raised_by": "worker", "raised_in_round": 4, "severity": "high", "resolution_needed_before": "execute"})
    pilot.step("Step 6 handover counter", ok, det)

    # ============================================================
    # Step 7: handover type=re-sync (advisor)
    # ============================================================
    ok, det = add_round("re-sync", "advisor",
                        body="Akzeptiert Counter, revidiere zu Option A'")
    pilot.step("Step 7 handover re-sync", ok, det)

    # ============================================================
    # Step 8: handover type=decision-lock (advisor, decided_by=user)
    # ============================================================
    ok, det = add_round("decision-lock", "advisor",
                        extra_frontmatter={"decided_by": "user"},
                        body="User wählt Option A'",
                        decision={"round": 6, "decision": "Option A' gewählt", "rationale": "Counter validiert, A' ist sicherer", "decided_by": "user", "alternatives_considered": ["A", "B", "C"]})
    pilot.step("Step 8 handover decision-lock", ok, det)

    # ============================================================
    # Step 9: handover type=pre-patch (advisor)
    # ============================================================
    ok, det = add_round("pre-patch", "advisor",
                        extra_frontmatter={
                            "acceptance_criteria": ["Patch P1 angewandt", "Patch P2 angewandt"],
                            "wallclock_estimate_min": 15,
                        },
                        body="2 Patches identifiziert vor Execute")
    pilot.step("Step 9 handover pre-patch (allOf)", ok, det)

    # ============================================================
    # Step 10: handover type=pre-flight (worker) → phase iterate→execute
    # ============================================================
    ok, det = add_round("pre-flight", "worker", phase_override="execute",
                        body="Pre-Flight PASS: alle Tools verfügbar, Backup angelegt")
    pilot.step("Step 10 handover pre-flight → execute", ok, det)

    # ============================================================
    # Step 11: handover type=execute (worker) — allOf voll
    # ============================================================
    ok, det = add_round("execute", "worker",
                        extra_frontmatter={
                            "acceptance_criteria": ["Schritt 1 done", "Schritt 2 done", "Schritt 3 done"],
                            "rollback_triggers": [
                                {"condition": "Schritt 2 FAIL", "action": "git reset HEAD~"},
                                {"condition": "Smoke-Test FAIL", "action": "tar restore backup"},
                            ],
                            "wallclock_estimate_min": 30,
                            "related_blockers": ["B-1"],
                        },
                        body="Plan-Schritte ausgeführt")
    pilot.step("Step 11 handover execute (allOf voll)", ok, det)

    # ============================================================
    # Step 12: handover type=verify (worker) → phase execute→verify
    # ============================================================
    ok, det = add_round("verify", "worker", phase_override="verify",
                        extra_frontmatter={"acceptance_criteria": ["Smoke-Test 12/12 PASS"]},
                        body="Smoke-Test komplett PASS")
    pilot.step("Step 12 handover verify → verify-phase", ok, det)

    # ============================================================
    # Step 13: /bridge-close → phase verify→close
    # ============================================================
    state = read_state(state_path)
    expected = state["updated_at"]

    # Wall-Clock-Drift kalibrieren (mock actual = estimate * 0.85, drift=0.85)
    for we in state["wallclock_estimates"]:
        we["actual_min"] = int(we["estimated_min"] * 0.85)
        we["drift_factor"] = round(we["actual_min"] / we["estimated_min"], 2) if we["estimated_min"] > 0 else None

    # Active artifacts archivieren
    for a in state["shared_artifacts"]:
        if a["lifecycle_state"] == "active":
            a["lifecycle_state"] = "archived"

    state["phase"] = "close"

    try:
        jsonschema.validate(state, state_schema)
        ok = cas_write_state(state_path, expected, state)
        pilot.step("Step 13 /bridge-close → close", ok, f"drift kalibriert für {len(state['wallclock_estimates'])} estimates")
    except jsonschema.ValidationError as e:
        pilot.step("Step 13 /bridge-close → close", False, str(e.message)[:200])

    # ============================================================
    # Final Validations
    # ============================================================

    # V1: state.current_round == len(state.rounds)
    final_state = read_state(state_path)
    pilot.step("V1 current_round == len(rounds)",
               final_state["current_round"] == len(final_state["rounds"]),
               f"current={final_state['current_round']} len={len(final_state['rounds'])}")

    # V2: Phase-Sequence in rounds[]-rückblickend rekonstruierbar
    expected_sequence = [
        ("status", "advisor"),       # 1
        ("status", "worker"),         # 2
        ("initial-advice", "advisor"),# 3
        ("counter", "worker"),        # 4
        ("re-sync", "advisor"),       # 5
        ("decision-lock", "advisor"), # 6
        ("pre-patch", "advisor"),     # 7
        ("pre-flight", "worker"),     # 8
        ("execute", "worker"),        # 9
        ("verify", "worker"),         # 10
    ]
    actual_sequence = [(r["type"], r["initiator"]) for r in final_state["rounds"]]
    pilot.step("V2 Round-Sequence korrekt", actual_sequence == expected_sequence,
               f"expected={len(expected_sequence)} actual={len(actual_sequence)}")

    # V3: Final Phase == close
    pilot.step("V3 Final Phase=close", final_state["phase"] == "close",
               f"phase={final_state['phase']}")

    # V4: Decision-Log hat 1 Eintrag
    pilot.step("V4 Decision-Log == 1", len(final_state["decision_log"]) == 1,
               f"len={len(final_state['decision_log'])}")

    # V5: Drift-Factor kalibriert in alle wallclock_estimates
    drift_uncalibrated = [we for we in final_state["wallclock_estimates"] if we["drift_factor"] is None]
    pilot.step("V5 Wall-Clock-Drift kalibriert", len(drift_uncalibrated) == 0,
               f"uncalibrated={len(drift_uncalibrated)}")

    # V6: Alle handover-Files existieren
    handover_files = list(handover_dir.glob("*.md"))
    pilot.step("V6 10 Handover-Files existieren", len(handover_files) == 10,
               f"count={len(handover_files)}")

    # V7: State.json final-validate
    try:
        jsonschema.validate(final_state, state_schema)
        pilot.step("V7 Final state.json schema valid", True)
    except jsonschema.ValidationError as e:
        pilot.step("V7 Final state.json schema valid", False, str(e.message)[:200])

    if verbose:
        print(f"\nFinal state.json:\n{json.dumps(final_state, indent=2)[:2000]}")

    print(pilot.summary())
    return pilot.exit_code()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--shared-path", default=str(SCRIPT_DIR / "shared"))
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    sys.exit(main(Path(args.shared_path), verbose=args.verbose))
