#!/usr/bin/env python3
"""
session-bridge plugin Self-Smoke-Test.

Akzeptanz M7 (ADR_0029 §10.2): Plugin-internal Konsistenz vor Phase 5 Pilot.

Tests:
  1. State-Schema syntaktisch valid (M1')
  2. Handover-Schema syntaktisch valid (M2')
  3. Synthetisches state.json validate PASS
  4. Synthetisches handover-Frontmatter validate PASS
  5. Negative: invalid state FAIL
  6. allOf: type=execute ohne acceptance_criteria FAIL
  7. allOf: type=decision-lock ohne decided_by FAIL
  8. allOf: type=pre-patch ohne wallclock_estimate_min FAIL

Exit-Codes:
  0 = alle Tests PASS
  1 = ein oder mehr Tests FAIL
  2 = jsonschema nicht verfügbar (degraded mode, Tests übersprungen)

Usage:
  python3 smoke_self_test.py
  python3 smoke_self_test.py --verbose
"""

import json
import os
import sys
import uuid
import argparse
from datetime import datetime, timezone
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = PLUGIN_ROOT / "schemas"
STATE_SCHEMA_PATH = SCHEMAS_DIR / "bridge_state_v1.json"
HANDOVER_SCHEMA_PATH = SCHEMAS_DIR / "handover_frontmatter_v1.json"


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_pair_id() -> str:
    return str(uuid.uuid4())


def synth_valid_state() -> dict:
    """Minimal-but-valid state.json fixture."""
    return {
        "pair_id": make_pair_id(),
        "schema_version": "1.1.0",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "phase": "iterate",
        "roles": {
            "advisor": {
                "session_id": "local_advisor_test",
                "expertise_source": "smoke-test-fixture",
                "expertise_profile": None,
                "profile_version": None,
                "active_since": now_iso(),
            },
            "worker": {
                "session_id": "local_worker_test",
                "current_focus": "smoke-test",
                "phase": "test-phase",
                "active_since": now_iso(),
            },
        },
        "topic": "smoke-test-topic",
        "current_round": 1,
        "rounds": [
            {
                "round": 1,
                "type": "initial-advice",
                "initiator": "advisor",
                "artifact_path": "bridge/handover/1-advisor-worker-abc123de.md",
                "timestamp": now_iso(),
            }
        ],
        "open_blockers": [],
        "decision_log": [],
        "status_observations": [],
        "file_ownership": {},
        "shared_artifacts": [],
        "wallclock_estimates": [],
        "rollback_plan_path": None,
    }


def synth_valid_handover(round_type: str = "initial-advice") -> dict:
    """Minimal-but-valid handover frontmatter fixture for given round-type."""
    base = {
        "pair_id": make_pair_id(),
        "round": 1,
        "from": "advisor",
        "to": "worker",
        "type": round_type,
        "timestamp": now_iso(),
        "worker_phase": "smoke-test-phase",
        "worker_focus": "smoke-test-focus",
        "status_verified_at": now_iso(),
        "references": [
            {
                "type": "filesystem",
                "pointer": "/path/to/artifact",
                "verified": True,
            }
        ],
    }
    # allOf-conditional Pflichten
    if round_type in ("pre-patch", "execute", "verify"):
        base["acceptance_criteria"] = ["criterion-1"]
    if round_type == "execute":
        base["rollback_triggers"] = [{"condition": "fail", "action": "revert"}]
    if round_type in ("pre-patch", "execute"):
        base["wallclock_estimate_min"] = 30
    if round_type == "decision-lock":
        base["decided_by"] = "user"
        # NEU v0.1.4 PB-003: pre_decision_verification Pflicht (allOf type=decision-lock)
        base["pre_decision_verification"] = [
            {
                "question": "smoke-test: ist Decision-Boden ausreichend?",
                "answer": "ja",
                "timestamp": "2026-04-30T10:00:00Z"
            }
        ]
    return base


class TestResult:
    def __init__(self):
        self.passed = []
        self.failed = []

    def record(self, name: str, ok: bool, msg: str = "") -> None:
        if ok:
            self.passed.append(name)
        else:
            self.failed.append((name, msg))

    def summary(self) -> str:
        total = len(self.passed) + len(self.failed)
        lines = [
            f"\n{'='*60}",
            f"Smoke-Test Summary: {len(self.passed)}/{total} PASS",
            f"{'='*60}",
        ]
        if self.failed:
            lines.append("FAILED:")
            for name, msg in self.failed:
                lines.append(f"  - {name}: {msg}")
        else:
            lines.append("All tests PASSED.")
        return "\n".join(lines)

    def exit_code(self) -> int:
        return 0 if not self.failed else 1


def load_schema(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def main(verbose: bool = False) -> int:
    print(f"session-bridge smoke-test starting (plugin-root: {PLUGIN_ROOT})")

    # Step 0: jsonschema available?
    try:
        import jsonschema
    except ImportError:
        print("[DEGRADED] jsonschema not available — tests skipped, exit 2.")
        return 2

    results = TestResult()

    # Test 1: State-Schema syntaktisch valid (M1')
    try:
        schema = load_schema(STATE_SCHEMA_PATH)
        jsonschema.Draft7Validator.check_schema(schema)
        results.record("M1' state-schema syntax", True)
    except Exception as e:
        results.record("M1' state-schema syntax", False, str(e))
        # Fatal — kann nicht weitermachen ohne valides Schema
        print(results.summary())
        return results.exit_code()

    state_schema = schema

    # Test 2: Handover-Schema syntaktisch valid (M2')
    try:
        schema = load_schema(HANDOVER_SCHEMA_PATH)
        jsonschema.Draft7Validator.check_schema(schema)
        results.record("M2' handover-schema syntax", True)
    except Exception as e:
        results.record("M2' handover-schema syntax", False, str(e))
        print(results.summary())
        return results.exit_code()

    handover_schema = schema

    # Test 3: Valid state validate PASS
    try:
        state = synth_valid_state()
        jsonschema.validate(state, state_schema)
        results.record("T3 valid-state validate", True)
    except Exception as e:
        results.record("T3 valid-state validate", False, str(e))

    # Test 4: Valid handover (initial-advice) validate PASS
    try:
        ho = synth_valid_handover("initial-advice")
        jsonschema.validate(ho, handover_schema)
        results.record("T4 valid-handover initial-advice", True)
    except Exception as e:
        results.record("T4 valid-handover initial-advice", False, str(e))

    # Test 4b: Valid handover (execute) validate PASS — alle allOf Pflichten erfüllt
    try:
        ho = synth_valid_handover("execute")
        jsonschema.validate(ho, handover_schema)
        results.record("T4b valid-handover execute (allOf)", True)
    except Exception as e:
        results.record("T4b valid-handover execute (allOf)", False, str(e))

    # Test 4c: Valid handover (decision-lock) validate PASS
    try:
        ho = synth_valid_handover("decision-lock")
        jsonschema.validate(ho, handover_schema)
        results.record("T4c valid-handover decision-lock", True)
    except Exception as e:
        results.record("T4c valid-handover decision-lock", False, str(e))

    # Test 5: Invalid state — missing required field 'phase'
    try:
        state = synth_valid_state()
        del state["phase"]
        jsonschema.validate(state, state_schema)
        results.record("T5 negative-state (missing phase)", False, "expected ValidationError, got PASS")
    except jsonschema.ValidationError:
        results.record("T5 negative-state (missing phase)", True)
    except Exception as e:
        results.record("T5 negative-state (missing phase)", False, f"unexpected: {e}")

    # Test 6: allOf — type=execute ohne acceptance_criteria FAIL
    try:
        ho = synth_valid_handover("execute")
        del ho["acceptance_criteria"]
        jsonschema.validate(ho, handover_schema)
        results.record("T6 allOf execute-ohne-acceptance", False, "expected ValidationError, got PASS")
    except jsonschema.ValidationError:
        results.record("T6 allOf execute-ohne-acceptance", True)
    except Exception as e:
        results.record("T6 allOf execute-ohne-acceptance", False, f"unexpected: {e}")

    # Test 7: allOf — type=decision-lock ohne decided_by FAIL
    try:
        ho = synth_valid_handover("decision-lock")
        del ho["decided_by"]
        jsonschema.validate(ho, handover_schema)
        results.record("T7 allOf decision-lock-ohne-decided_by", False, "expected ValidationError, got PASS")
    except jsonschema.ValidationError:
        results.record("T7 allOf decision-lock-ohne-decided_by", True)
    except Exception as e:
        results.record("T7 allOf decision-lock-ohne-decided_by", False, f"unexpected: {e}")

    # Test 8: allOf — type=pre-patch ohne wallclock_estimate_min FAIL
    try:
        ho = synth_valid_handover("pre-patch")
        del ho["wallclock_estimate_min"]
        jsonschema.validate(ho, handover_schema)
        results.record("T8 allOf pre-patch-ohne-wallclock", False, "expected ValidationError, got PASS")
    except jsonschema.ValidationError:
        results.record("T8 allOf pre-patch-ohne-wallclock", True)
    except Exception as e:
        results.record("T8 allOf pre-patch-ohne-wallclock", False, f"unexpected: {e}")

    # Test 9: Round-type enum — invalid type FAIL
    try:
        ho = synth_valid_handover("initial-advice")
        ho["type"] = "made-up-type"
        jsonschema.validate(ho, handover_schema)
        results.record("T9 negative round-type enum", False, "expected ValidationError, got PASS")
    except jsonschema.ValidationError:
        results.record("T9 negative round-type enum", True)
    except Exception as e:
        results.record("T9 negative round-type enum", False, f"unexpected: {e}")

    # Test 10: pair_id pattern — invalid uuid FAIL
    try:
        ho = synth_valid_handover("initial-advice")
        ho["pair_id"] = "not-a-uuid"
        jsonschema.validate(ho, handover_schema)
        results.record("T10 negative pair_id pattern", False, "expected ValidationError, got PASS")
    except jsonschema.ValidationError:
        results.record("T10 negative pair_id pattern", True)
    except Exception as e:
        results.record("T10 negative pair_id pattern", False, f"unexpected: {e}")

    # Test 11 (v1.1.0 ADR_0030): expertise_profile-Field als Pfad-String akzeptiert
    try:
        state = synth_valid_state()
        state["roles"]["advisor"]["expertise_profile"] = "expertise-profiles/process-consulting"
        state["roles"]["advisor"]["profile_version"] = "0.1.0"
        jsonschema.validate(state, state_schema)
        results.record("T11 v1.1.0 expertise_profile string-pfad valid", True)
    except Exception as e:
        results.record("T11 v1.1.0 expertise_profile string-pfad valid", False, str(e))

    # Test 12 (v1.1.0 ADR_0030): schema_version 1.1.0 akzeptiert (Migration aus 1.0.0)
    try:
        state = synth_valid_state()
        state["schema_version"] = "1.0.0"
        # v1.0.0 darf keine expertise_profile haben (nicht required, aber pattern-konform)
        state["roles"]["advisor"].pop("expertise_profile", None)
        state["roles"]["advisor"].pop("profile_version", None)
        jsonschema.validate(state, state_schema)
        results.record("T12 v1.0.0 backward-compatible (Migration-Pfad)", True)
    except Exception as e:
        results.record("T12 v1.0.0 backward-compatible (Migration-Pfad)", False, str(e))

    # Test 13 (v1.1.0 ADR_0030): schema_version invalid → FAIL
    try:
        state = synth_valid_state()
        state["schema_version"] = "2.0.0"  # nicht im enum
        jsonschema.validate(state, state_schema)
        results.record("T13 negative schema_version enum", False, "expected ValidationError, got PASS")
    except jsonschema.ValidationError:
        results.record("T13 negative schema_version enum", True)
    except Exception as e:
        results.record("T13 negative schema_version enum", False, f"unexpected: {e}")

    # ----------------------------------------------------------------
    # v0.1.3 Mapping-Decision-Tests T14-T22 (D-001..D-005 + F-RP-30..32)
    # ----------------------------------------------------------------

    # Test 14 (v1.1.1 NEU v0.1.3): schema_version 1.1.1 akzeptiert
    try:
        state = synth_valid_state()
        state["schema_version"] = "1.1.1"
        jsonschema.validate(state, state_schema)
        results.record("T14 v1.1.1 schema_version valid", True)
    except Exception as e:
        results.record("T14 v1.1.1 schema_version valid", False, str(e))

    # Test 15 (v1.1.1 NEU v0.1.3 / E.1): mapping_budget optional, top-level
    try:
        state = synth_valid_state()
        state["schema_version"] = "1.1.1"
        state["mapping_budget"] = {
            "min": 14,
            "max": 16,
            "started_round": 12,
            "soft_cap": True,
            "rounds_per_befund": 2,
            "klarstellungs_reserve": 2,
            "triggers": {"T1": "convergence", "T2": "exhaustion"}
        }
        jsonschema.validate(state, state_schema)
        results.record("T15 v1.1.1 mapping_budget optional", True)
    except Exception as e:
        results.record("T15 v1.1.1 mapping_budget optional", False, str(e))

    # Test 16 (D-002 F-RP-32): bridge-attach Pre-Flight 5 — required-Args hard-enforce
    # Negative-Spec-Check: attach-Skill requires --worker-focus when role=worker.
    # Implementation-Test-Stub: simulated via Spec-Doc-Read-Heuristic.
    try:
        attach_spec_path = PLUGIN_ROOT / "commands" / "bridge-attach.md"
        spec_text = attach_spec_path.read_text()
        # Pre-Flight 5 hard-enforce-Marker muss vorhanden sein
        assert "hard-enforce" in spec_text and "Pre-Flight" in spec_text
        assert "--worker-focus" in spec_text and "--expertise-source" in spec_text
        results.record("T16 D-002 bridge-attach Pre-Flight 5 hard-enforce spec", True)
    except Exception as e:
        results.record("T16 D-002 bridge-attach Pre-Flight 5 hard-enforce spec", False, str(e))

    # Test 17 (D-002 F-RP-32): bridge-handover Pre-Flight 5 type=execute Pflicht-Args dokumentiert
    try:
        ho_spec_path = PLUGIN_ROOT / "commands" / "bridge-handover.md"
        spec_text = ho_spec_path.read_text()
        assert "hard-enforce" in spec_text
        assert "type=execute" in spec_text and "--acceptance" in spec_text
        assert "type=decision-lock" in spec_text and "--decided-by" in spec_text
        results.record("T17 D-002 bridge-handover Pre-Flight 5 type-spezifisch hard-enforce", True)
    except Exception as e:
        results.record("T17 D-002 bridge-handover Pre-Flight 5 type-spezifisch hard-enforce", False, str(e))

    # Test 17b (D-005 Sub-B / F-RP-34): Pre-Flight 6 convergence-skip-marker dokumentiert
    try:
        ho_spec_path = PLUGIN_ROOT / "commands" / "bridge-handover.md"
        spec_text = ho_spec_path.read_text()
        assert "convergence_criterion_skip" in spec_text
        assert "konvergenz-skip-rationale" in spec_text
        results.record("T17b D-005-B Pre-Flight 6 convergence-skip-marker", True)
    except Exception as e:
        results.record("T17b D-005-B Pre-Flight 6 convergence-skip-marker", False, str(e))

    # Test 18 (F-RP-31): bridge-status output completeness — neue Felder dokumentiert
    try:
        status_spec_path = PLUGIN_ROOT / "commands" / "bridge-status.md"
        spec_text = status_spec_path.read_text()
        # Output muss Rolle, other-title, last activity, letzte 3 Rounds, nächste Aktion enthalten
        assert "Diese Session" in spec_text
        assert "Andere Session" in spec_text
        assert "Last activity" in spec_text or "last_activity" in spec_text.lower()
        assert "Letzte 3 Rounds" in spec_text
        assert "Nächste erwartete Aktion" in spec_text
        assert "Polling-Hint" in spec_text or "polling-hint" in spec_text.lower()
        results.record("T18 F-RP-31 bridge-status output completeness", True)
    except Exception as e:
        results.record("T18 F-RP-31 bridge-status output completeness", False, str(e))

    # Test 19 (D-004 F-RP-23): bridge-init writes Sentinel always
    try:
        init_spec_path = PLUGIN_ROOT / "commands" / "bridge-init.md"
        spec_text = init_spec_path.read_text()
        # Spec muss klarstellen dass --worker-session-id UX-Hint ist
        assert "UX-Hint" in spec_text or "UX-hint" in spec_text
        # Worker-obj-Code muss IMMER SENTINEL_PENDING setzen
        assert "REVIDIERT v0.1.3" in spec_text
        assert 'session_id": SENTINEL_PENDING' in spec_text
        # bridge-attach Pre-Flight 4 strict
        attach_spec_path = PLUGIN_ROOT / "commands" / "bridge-attach.md"
        attach_text = attach_spec_path.read_text()
        assert "REVIDIERT v0.1.3 strict" in attach_text or "strict" in attach_text
        results.record("T19 D-004 Sentinel-Invariante v0.1.3", True)
    except Exception as e:
        results.record("T19 D-004 Sentinel-Invariante v0.1.3", False, str(e))

    # Test 20 (F-RP-30): bridge-worker §Role-Boundary dokumentiert
    try:
        worker_skill_path = PLUGIN_ROOT / "skills" / "bridge-worker" / "SKILL.md"
        spec_text = worker_skill_path.read_text()
        assert "§Role-Boundary" in spec_text or "Role-Boundary" in spec_text
        assert "AP-Diagnosen" in spec_text or "AP-Diagnose" in spec_text
        assert "advisor-mode-Tags" in spec_text or "advisor-mode-tags" in spec_text
        assert "[bridge-worker mode]" in spec_text
        results.record("T20 F-RP-30 bridge-worker Role-Boundary + Mode-Marker", True)
    except Exception as e:
        results.record("T20 F-RP-30 bridge-worker Role-Boundary + Mode-Marker", False, str(e))

    # Test 21 (D-001 Worker-Pos): re-sync sub-type marker dokumentiert
    try:
        ho_spec_path = PLUGIN_ROOT / "commands" / "bridge-handover.md"
        spec_text = ho_spec_path.read_text()
        assert "resync_sub_type" in spec_text
        assert "plan-layer" in spec_text and "execution-layer" in spec_text and "hybrid" in spec_text
        results.record("T21 D-001-W re-sync sub-type marker", True)
    except Exception as e:
        results.record("T21 D-001-W re-sync sub-type marker", False, str(e))

    # Test 22 (D-005 Sub-A F-RP-15): bridge-init Pre-Flight 5b sandbox-mount + section
    try:
        init_spec_path = PLUGIN_ROOT / "commands" / "bridge-init.md"
        spec_text = init_spec_path.read_text()
        assert "sandbox-mount-prerequisite" in spec_text
        assert "5.b" in spec_text or "5.b " in spec_text
        assert "sandbox-mounted" in spec_text or "sandbox-erreichbar" in spec_text
        results.record("T22 D-005-A bridge-init Pre-Flight 5b sandbox-mount", True)
    except Exception as e:
        results.record("T22 D-005-A bridge-init Pre-Flight 5b sandbox-mount", False, str(e))

    # Test 23 (D-001 Advisor-Pos / F-RP-29): bridge-advisor Anti-Plan-Drift + bridge-handover Output-Marker
    try:
        advisor_skill_path = PLUGIN_ROOT / "skills" / "bridge-advisor" / "SKILL.md"
        adv_text = advisor_skill_path.read_text()
        assert "§Anti-Plan-Drift" in adv_text or "Anti-Plan-Drift" in adv_text
        assert "User-Translation-Konvention" in adv_text or "[plan-layer | no-bridge-write]" in adv_text
        assert "[bridge-advisor mode" in adv_text
        ho_spec_path = PLUGIN_ROOT / "commands" / "bridge-handover.md"
        ho_text = ho_spec_path.read_text()
        assert "BRIDGE-WRITE COMPLETED" in ho_text
        results.record("T23 D-001 Advisor-Pos Anti-Plan-Drift + Output-Marker", True)
    except Exception as e:
        results.record("T23 D-001 Advisor-Pos Anti-Plan-Drift + Output-Marker", False, str(e))

    # Test 24 (D-003 F-RP-33): forward-pointer-rationale dokumentiert + Schema-Felder
    try:
        ho_spec_path = PLUGIN_ROOT / "commands" / "bridge-handover.md"
        ho_text = ho_spec_path.read_text()
        assert "forward-pointer-rationale" in ho_text
        assert "pre-allocated" in ho_text
        # Schema muss neue shared_artifacts Felder enthalten (status, round_allocated, round_active)
        sa = state_schema["properties"]["shared_artifacts"]["items"]["properties"]
        assert "status" in sa and "round_allocated" in sa and "round_active" in sa
        results.record("T24 D-003 forward-pointer-rationale + Schema-Felder", True)
    except Exception as e:
        results.record("T24 D-003 forward-pointer-rationale + Schema-Felder", False, str(e))

    # Test 25 (F-RP-22): Pre-Flight 2 filesystem-read documented
    try:
        init_spec_path = PLUGIN_ROOT / "commands" / "bridge-init.md"
        spec_text = init_spec_path.read_text()
        # F.1 Patch hat Pflicht-Tool-Call dokumentiert
        assert "PFLICHT-Tool-Call" in spec_text or "Conversational-Memory" in spec_text
        results.record("T25 F-RP-22 Pre-Flight 2 filesystem-read", True)
    except Exception as e:
        results.record("T25 F-RP-22 Pre-Flight 2 filesystem-read", False, str(e))

    # Test 26 (v0.1.4 F-RP-24): bridge-init --worker-session-title primary flag in Argumente
    try:
        init_spec_path = PLUGIN_ROOT / "commands" / "bridge-init.md"
        spec_text = init_spec_path.read_text()
        # NEU v0.1.4: --worker-session-title primaer empfohlen
        assert "--worker-session-title" in spec_text, "--worker-session-title flag missing"
        assert "primaer empfohlen" in spec_text, "primary marker missing"
        assert "Fallback / Power-User" in spec_text, "fallback marker for --worker-session-id missing"
        results.record("T26 v0.1.4 F-RP-24 bridge-init Title-Flag primary", True)
    except Exception as e:
        results.record("T26 v0.1.4 F-RP-24 bridge-init Title-Flag primary", False, str(e))

    # Test 27 (v0.1.4 F-RP-24): bridge-init Argument-Resolution title-first multi-match + no-match
    try:
        init_spec_path = PLUGIN_ROOT / "commands" / "bridge-init.md"
        spec_text = init_spec_path.read_text()
        # multi-match resolution path
        assert "multi-match" in spec_text, "multi-match resolution path missing"
        # no-match resolution path
        assert "no-match" in spec_text, "no-match resolution path missing"
        # Sentinel-Invariante v0.1.3+ bestaetigt
        assert "IMMER auf `pending-attach`-Sentinel gesetzt" in spec_text, "Sentinel-Invariante v0.1.3+ marker missing"
        results.record("T27 v0.1.4 F-RP-24 Argument-Resolution title-first paths", True)
    except Exception as e:
        results.record("T27 v0.1.4 F-RP-24 Argument-Resolution title-first paths", False, str(e))

    # Test 28 (v0.1.4 F-RP-24): bridge-attach --this-session-title row
    try:
        attach_spec_path = PLUGIN_ROOT / "commands" / "bridge-attach.md"
        spec_text = attach_spec_path.read_text()
        assert "--this-session-title" in spec_text, "--this-session-title flag missing in bridge-attach"
        assert "F-RP-24" in spec_text, "F-RP-24 reference marker missing"
        results.record("T28 v0.1.4 F-RP-24 bridge-attach Title-Flag", True)
    except Exception as e:
        results.record("T28 v0.1.4 F-RP-24 bridge-attach Title-Flag", False, str(e))

    # Test 29 (v0.1.4 F-RP-26): bridge-handover §worker.phase-Auto-Propagation + bridge-attach Initial-Set
    try:
        handover_spec_path = PLUGIN_ROOT / "commands" / "bridge-handover.md"
        handover_text = handover_spec_path.read_text()
        # Auto-Propagation-Sektion
        assert "§worker.phase-Auto-Propagation" in handover_text, "§worker.phase-Auto-Propagation section missing"
        # Pseudocode-Marker fuer Auto-Propagation
        assert 'state.roles.worker.phase = frontmatter.get("worker_phase")' in handover_text, "auto-propagation pseudocode missing"

        attach_spec_path = PLUGIN_ROOT / "commands" / "bridge-attach.md"
        attach_text = attach_spec_path.read_text()
        # Initial-Set-Sektion in bridge-attach
        assert "§worker.phase-Initial-Set" in attach_text, "§worker.phase-Initial-Set section missing in bridge-attach"

        # Schema-Spec worker.phase Auto-propagation description
        sa_path = PLUGIN_ROOT / "schemas" / "bridge_state_v1.json"
        sa = json.load(open(sa_path))
        worker_phase_spec = sa["properties"]["roles"]["properties"]["worker"]["properties"]["phase"]
        assert "description" in worker_phase_spec, "worker.phase description missing"
        assert "Auto-propagation" in worker_phase_spec["description"], "Auto-propagation marker missing in description"

        results.record("T29 v0.1.4 F-RP-26 worker.phase Auto-Propagation + Initial-Set", True)
    except Exception as e:
        results.record("T29 v0.1.4 F-RP-26 worker.phase Auto-Propagation + Initial-Set", False, str(e))

    # Test 30 (v0.1.4 PB-001): bilanz_v1.json schema syntax + valid-bilanz validate
    try:
        bilanz_schema_path = SCHEMAS_DIR / "bilanz_v1.json"
        bilanz_schema = load_schema(bilanz_schema_path)
        jsonschema.Draft7Validator.check_schema(bilanz_schema)

        # Synth valid Bilanz
        synth = {
            "pair_id": "8cbeaad0-e67a-4184-889b-76a70c21d617",
            "pair_topic": "test",
            "created_at": "2026-04-28T06:49:01Z",
            "closed_at": "2026-04-29T11:09:53Z",
            "total_rounds": 28,
            "phase_sequence": [{"phase": "init", "rounds_range": "R0", "rounds_count": 1}],
            "decision_log_summary": [{"decision": "test", "decided_by": "consensus"}],
            "wallclock_drift_calibrated": [{"phase": "test", "estimated_rounds": 5,
                                           "actual_rounds": 12, "drift_factor": 2.4}],
            "reflection": {"was_funktionierte": ["x"], "was_problematisch": [],
                          "was_als_naechstes": ["y"]},
            "successful_patterns": [],
            "anti_patterns_detected": [],
            "cross_pair_transfer_hinweise": []
        }
        jsonschema.validate(synth, bilanz_schema)
        results.record("T30 v0.1.4 PB-001 bilanz_v1 schema + valid-bilanz", True)
    except Exception as e:
        results.record("T30 v0.1.4 PB-001 bilanz_v1 schema + valid-bilanz", False, str(e))

    # Test 31 (v0.1.4): mapping_decisions_v1 schema + DISSENS-allOf-Constraint
    try:
        md_schema_path = SCHEMAS_DIR / "mapping_decisions_v1.json"
        md_schema = load_schema(md_schema_path)
        jsonschema.Draft7Validator.check_schema(md_schema)

        # Synth valid mapping with both PATCH + DISSENS-DOCUMENTED-with-sub_type
        synth = {
            "pair_id": "8cbeaad0-e67a-4184-889b-76a70c21d617",
            "schema_version": "1.0.0",
            "mapping_phase_start": {"round": 12, "decision_locked_in_round": 11},
            "decisions": [
                {"id": "D-001", "round_decided": 12, "konvergenz_status": "locked",
                 "frame": "F1.2", "mapping_category": "DISSENS-DOCUMENTED",
                 "sub_type": "§3.4.2 Skopus"},
                {"id": "D-002", "round_decided": 16, "konvergenz_status": "locked",
                 "frame": "F1.1", "mapping_category": "PATCH"}
            ]
        }
        jsonschema.validate(synth, md_schema)

        # Negative: DISSENS-DOCUMENTED ohne sub_type → FAIL erwartet
        bad = {
            "pair_id": "8cbeaad0-e67a-4184-889b-76a70c21d617",
            "schema_version": "1.0.0",
            "mapping_phase_start": {"round": 12, "decision_locked_in_round": 11},
            "decisions": [{"id": "D-001", "round_decided": 12, "konvergenz_status": "locked",
                          "frame": "F1.2", "mapping_category": "DISSENS-DOCUMENTED"}]
        }
        try:
            jsonschema.validate(bad, md_schema)
            raise AssertionError("expected ValidationError for DISSENS without sub_type")
        except jsonschema.ValidationError:
            pass

        results.record("T31 v0.1.4 mapping_decisions_v1 schema + DISSENS-allOf", True)
    except Exception as e:
        results.record("T31 v0.1.4 mapping_decisions_v1 schema + DISSENS-allOf", False, str(e))

    # Test 32 (v0.1.4): bridge_state_v1 shared_artifacts.artifact_type-Enum
    try:
        sa_at = state_schema["properties"]["shared_artifacts"]["items"]["properties"].get("artifact_type", {})
        assert "enum" in sa_at, "artifact_type missing enum"
        expected = {"mapping-method-annex", "mapping-decisions-log", "bilanz", "custom"}
        assert set(sa_at["enum"]) == expected, f"expected {expected}, got {set(sa_at['enum'])}"
        results.record("T32 v0.1.4 bridge_state shared_artifacts.artifact_type-Enum", True)
    except Exception as e:
        results.record("T32 v0.1.4 bridge_state shared_artifacts.artifact_type-Enum", False, str(e))

    # Test 33 (v0.1.4 Cross-Validation): mapping_decisions accepts P3-style mapping_category_history audit-trail
    try:
        md_schema_path = SCHEMAS_DIR / "mapping_decisions_v1.json"
        md_schema = load_schema(md_schema_path)

        # P3 D-004 R23-Revision pattern: mapping_category_history mit 4 Eintraegen
        synth = {
            "pair_id": "8cbeaad0-e67a-4184-889b-76a70c21d617",
            "schema_version": "1.0.0",
            "mapping_phase_start": {"round": 12, "decision_locked_in_round": 11},
            "decisions": [{
                "id": "D-004",
                "round_decided": 21,
                "konvergenz_status": "locked",
                "frame": "F1.1 + F4.2",
                "mapping_category": "PATCH",
                "mapping_category_history": [
                    {"round": 21, "position": "AFFORDANCE", "by": "advisor"},
                    {"round": 22, "position": "PATCH", "by": "worker", "basis": "counter"},
                    {"round": 23, "position": "PATCH", "by": "advisor",
                     "basis": "Worker-Argument 3 Methoden-Logik-Treffer + F4.2"},
                    {"round": 24, "position": "PATCH", "by": "worker", "basis": "konvergenz-lock"}
                ]
            }]
        }
        jsonschema.validate(synth, md_schema)
        results.record("T33 v0.1.4 mapping_decisions akzeptiert P3-D-004-Revision-Pattern", True)
    except Exception as e:
        results.record("T33 v0.1.4 mapping_decisions akzeptiert P3-D-004-Revision-Pattern", False, str(e))

    # Test 34 (v0.1.4 PB-003): decision-lock-Handover mit pre_decision_verification 1 Eintrag PASS
    try:
        ho = synth_valid_handover("decision-lock")
        # synth schon mit 1 Eintrag — sollte validate PASS
        jsonschema.validate(ho, handover_schema)
        results.record("T34 v0.1.4 PB-003 decision-lock pre_decision_verification 1 Eintrag PASS", True)
    except Exception as e:
        results.record("T34 v0.1.4 PB-003 decision-lock pre_decision_verification 1 Eintrag PASS", False, str(e))

    # Test 35 (v0.1.4 PB-003): decision-lock OHNE pre_decision_verification FAIL via allOf
    try:
        ho = synth_valid_handover("decision-lock")
        del ho["pre_decision_verification"]
        jsonschema.validate(ho, handover_schema)
        results.record("T35 v0.1.4 PB-003 decision-lock ohne pre_decision_verification FAIL", False, "expected ValidationError")
    except jsonschema.ValidationError:
        results.record("T35 v0.1.4 PB-003 decision-lock ohne pre_decision_verification FAIL", True)
    except Exception as e:
        results.record("T35 v0.1.4 PB-003 decision-lock ohne pre_decision_verification FAIL", False, f"unexpected: {e}")

    # Test 36 (v0.1.4 PB-003): pre_decision_verification mit 3 Eintraegen FAIL via maxItems=2
    try:
        ho = synth_valid_handover("decision-lock")
        ho["pre_decision_verification"] = [
            {"question": "q1?", "answer": "ja", "timestamp": "2026-04-30T10:00:00Z"},
            {"question": "q2?", "answer": "nein", "timestamp": "2026-04-30T10:01:00Z"},
            {"question": "q3?", "answer": "vielleicht", "timestamp": "2026-04-30T10:02:00Z"}
        ]
        jsonschema.validate(ho, handover_schema)
        results.record("T36 v0.1.4 PB-003 pre_decision_verification maxItems=2 FAIL", False, "expected ValidationError fuer 3 Eintraege")
    except jsonschema.ValidationError:
        results.record("T36 v0.1.4 PB-003 pre_decision_verification maxItems=2 FAIL", True)
    except Exception as e:
        results.record("T36 v0.1.4 PB-003 pre_decision_verification maxItems=2 FAIL", False, f"unexpected: {e}")

    # Test 37 (v0.1.4 PB-011): tools/find_shared_path.sh existiert + executable
    try:
        import os as _os
        helper_path = PLUGIN_ROOT / "tools" / "find_shared_path.sh"
        assert helper_path.exists(), "find_shared_path.sh fehlt"
        assert _os.access(helper_path, _os.X_OK), "find_shared_path.sh nicht executable"
        # Plus: bridge-init.md verweist auf tools/find_shared_path.sh
        init_text = (PLUGIN_ROOT / "commands" / "bridge-init.md").read_text()
        assert "tools/find_shared_path.sh" in init_text, "bridge-init.md verweist nicht auf Helper"
        results.record("T37 v0.1.4 PB-011 find_shared_path.sh + bridge-init-Pointer", True)
    except Exception as e:
        results.record("T37 v0.1.4 PB-011 find_shared_path.sh + bridge-init-Pointer", False, str(e))

    # Test 38 (v0.1.4 PB-010): bridge-handover.md §body-number-konsistenz dokumentiert
    try:
        ho_text = (PLUGIN_ROOT / "commands" / "bridge-handover.md").read_text()
        assert "§body-number-konsistenz" in ho_text, "§body-number-konsistenz Sektion fehlt"
        # Plus: Pattern-Match-Doku-Marker
        assert "atomar" in ho_text or "Eintraege" in ho_text or "Items" in ho_text, "Pattern-Match-Doku fehlt"
        # Plus: Empirie-Anker UPP-Pair
        assert "UPP-Pair" in ho_text, "Empirie-Anker UPP-Pair fehlt"
        results.record("T38 v0.1.4 PB-010 bridge-handover §body-number-konsistenz", True)
    except Exception as e:
        results.record("T38 v0.1.4 PB-010 bridge-handover §body-number-konsistenz", False, str(e))

    if verbose:
        print("Passed:", results.passed)

    print(results.summary())
    return results.exit_code()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    sys.exit(main(verbose=args.verbose))
