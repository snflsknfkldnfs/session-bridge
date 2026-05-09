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
import re
import sys
import uuid
import argparse
from datetime import datetime, timezone
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = PLUGIN_ROOT / "schemas"

# v0.1.8: tools/ als Modul importierbar machen
sys.path.insert(0, str(PLUGIN_ROOT))
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

    # Test 39 (v0.1.4 Phase F): ADR_0031 Cross-Pair-Patterns existiert + Pflicht-Sektionen
    try:
        adr_path = PLUGIN_ROOT / "docs" / "adr" / "ADR_0031_Cross-Pair-Patterns.md"
        assert adr_path.exists(), "ADR_0031 fehlt"
        adr_text = adr_path.read_text()
        # Pflicht-Sektionen
        for section in ["§1 Scope", "§2 Empirie", "§3 Cross-Pair-Patterns",
                       "§4 Decisions", "§5 Foundation fuer PB-006",
                       "§6 Implications", "§7 Cross-Refs"]:
            assert section in adr_text, f"§-Section fehlt: {section}"
        # Empirie-Sample 4 Pairs
        for pilot in ["p3-real-user", "p4-eg-dev", "p5-eg-v06-spec", "p6-upp-eg-advice"]:
            assert pilot in adr_text, f"Pilot-Reference fehlt: {pilot}"
        # PB-002 Threshold-Decision
        assert "Domain-Hint-aware" in adr_text or "Domain-aware" in adr_text, "Domain-aware-Decision fehlt"
        # PB-007 Domain-Hint-Field Activation
        assert "PB-007" in adr_text, "PB-007 Activation-Decision fehlt"
        results.record("T39 v0.1.4 Phase F ADR_0031 Cross-Pair-Patterns", True)
    except Exception as e:
        results.record("T39 v0.1.4 Phase F ADR_0031 Cross-Pair-Patterns", False, str(e))

    # Test 40 (v0.1.5 PB-007): topic_metadata.domain_hint-Enum + backward-compat
    try:
        # State-Schema enum erweitert auf 1.2.0
        sv_enum = state_schema["properties"]["schema_version"].get("enum", [])
        assert "1.2.0" in sv_enum, f"schema_version 1.2.0 fehlt in Enum: {sv_enum}"

        # topic_metadata.domain_hint-Enum vorhanden
        tm = state_schema["properties"].get("topic_metadata", {})
        assert tm.get("type") == "object", "topic_metadata fehlt oder nicht object"
        dh = tm.get("properties", {}).get("domain_hint", {})
        # v0.1.10 update: subset-check (forward-compat fuer v0.1.10+ enum-Erweiterungen)
        v15_required_subset = {"plugin-self-dev", "use-case", "architecture-spec",
                              "investigation-trace", "methodology-improvement", "other"}
        actual_enum = set(dh.get("enum", []))
        missing = v15_required_subset - actual_enum
        assert not missing, f"v0.1.5 Pflicht-enum-Werte fehlen: {missing}"

        # Positive: state mit topic_metadata.domain_hint validate PASS
        state = synth_valid_state()
        state["schema_version"] = "1.2.0"
        state["topic_metadata"] = {"domain_hint": "plugin-self-dev"}
        jsonschema.validate(state, state_schema)

        # Backward-compat: state OHNE topic_metadata validate PASS (optional)
        state2 = synth_valid_state()
        # synth bleibt ohne topic_metadata
        assert "topic_metadata" not in state2 or state2["topic_metadata"] == {}
        jsonschema.validate(state2, state_schema)

        # Negative: invalid domain_hint enum value FAIL
        state3 = synth_valid_state()
        state3["schema_version"] = "1.2.0"
        state3["topic_metadata"] = {"domain_hint": "INVALID-VALUE"}
        try:
            jsonschema.validate(state3, state_schema)
            raise AssertionError("expected ValidationError fuer invalid domain_hint")
        except jsonschema.ValidationError:
            pass

        # bridge-init.md doku: --domain-hint dokumentiert
        init_text = (PLUGIN_ROOT / "commands" / "bridge-init.md").read_text()
        assert "--domain-hint" in init_text, "--domain-hint flag in bridge-init.md fehlt"

        results.record("T40 v0.1.5 PB-007 topic_metadata.domain_hint-Enum + backward-compat", True)
    except Exception as e:
        results.record("T40 v0.1.5 PB-007 topic_metadata.domain_hint-Enum + backward-compat", False, str(e))

    # Test 41 (v0.1.5 Phase I): ADR_0029 Annex B Filename-Konvention
    try:
        adr_path = PLUGIN_ROOT / "docs" / "adr" / "ADR_0029_Session_Bridge_Pattern.md"
        adr_text = adr_path.read_text()
        assert "Annex B" in adr_text, "ADR_0029 Annex B fehlt"
        assert "bridge/bilanz_<pair_id>.md" in adr_text, "Filename-Konvention fehlt"
        assert "schemas/bilanz_v1.json" in adr_text, "Schema-Pointer fehlt"
        assert "ADR_0031" in adr_text, "ADR_0031-Cross-Ref fehlt"
        results.record("T41 v0.1.5 Phase I ADR_0029 Annex B Filename-Konvention", True)
    except Exception as e:
        results.record("T41 v0.1.5 Phase I ADR_0029 Annex B Filename-Konvention", False, str(e))

    # Test 42 (v0.1.5 PB-012): tools/bridge_state.py existiert + importierbar
    try:
        sys.path.insert(0, str(PLUGIN_ROOT / "tools"))
        import bridge_state
        # API check: v0.1.5 Phase B-Foundation-Subset (forward-compat fuer Phase H+D Erweiterungen)
        phase_b_required = {"SENTINEL_PENDING_ATTACH", "read_state", "write_atomic_cas",
                           "validate_against_schema", "pending_attach_replace",
                           "append_round", "archive_shared_artifact",
                           "calibrate_wallclock_post_hoc"}
        actual_api = set(bridge_state.__all__)
        missing = phase_b_required - actual_api
        assert not missing, f"Phase B Foundation-API missing: {missing}"
        assert bridge_state.SENTINEL_PENDING_ATTACH == "pending-attach"
        results.record("T42 v0.1.5 PB-012 tools/bridge_state.py Library-API", True)
    except Exception as e:
        results.record("T42 v0.1.5 PB-012 tools/bridge_state.py Library-API", False, str(e))

    # Test 43 (v0.1.5 PB-012): Library validate_against_schema funktional
    try:
        import bridge_state
        valid_state = synth_valid_state()
        errors = bridge_state.validate_against_schema(valid_state)
        assert errors == [] or errors == ["jsonschema-not-available"], f"unexpected errors: {errors}"

        # Negative: invalid state produces errors
        invalid = synth_valid_state()
        del invalid["phase"]
        errors2 = bridge_state.validate_against_schema(invalid)
        assert errors2 != [] or errors2 == ["jsonschema-not-available"], "expected errors fuer missing phase"
        results.record("T43 v0.1.5 PB-012 Library validate_against_schema", True)
    except Exception as e:
        results.record("T43 v0.1.5 PB-012 Library validate_against_schema", False, str(e))

    # Test 44 (v0.1.5 PB-012): Library pending_attach_replace strict-mode
    try:
        import bridge_state
        state = synth_valid_state()
        # Setze worker auf Sentinel
        state["roles"]["worker"]["session_id"] = bridge_state.SENTINEL_PENDING_ATTACH
        # Initial-Set Test: phase entfernen damit setdefault greift
        state["roles"]["worker"].pop("phase", None)
        # Replace
        state2 = bridge_state.pending_attach_replace(state, "worker", "local_test_123", "test-focus")
        assert state2["roles"]["worker"]["session_id"] == "local_test_123"
        assert state2["roles"]["worker"]["current_focus"] == "test-focus"
        assert state2["roles"]["worker"]["phase"] == "kickoff"  # Initial-Set v0.1.4 Phase A.2

        # Plus: existing phase wird NICHT ueberschrieben (setdefault-Semantik)
        state_x = synth_valid_state()
        state_x["roles"]["worker"]["session_id"] = bridge_state.SENTINEL_PENDING_ATTACH
        state_x["roles"]["worker"]["phase"] = "existing-phase"
        state_y = bridge_state.pending_attach_replace(state_x, "worker", "local_xyz")
        assert state_y["roles"]["worker"]["phase"] == "existing-phase"  # nicht ueberschrieben

        # Negative: non-Sentinel direct-pin → ValueError per D-004 R23-Revidierung strict
        state3 = synth_valid_state()
        state3["roles"]["worker"]["session_id"] = "local_already_pinned"
        try:
            bridge_state.pending_attach_replace(state3, "worker", "local_other")
            raise AssertionError("expected ValueError for non-Sentinel session_id")
        except ValueError:
            pass
        results.record("T44 v0.1.5 PB-012 Library pending_attach_replace strict", True)
    except Exception as e:
        results.record("T44 v0.1.5 PB-012 Library pending_attach_replace strict", False, str(e))

    # Test 45 (v0.1.5 PB-012): Library append_round + worker.phase Auto-Propagation
    try:
        import bridge_state
        state = synth_valid_state()
        round_data = {
            "round": state["current_round"] + 1,
            "type": "status",
            "initiator": "worker",
            "artifact_path": "bridge/handover/test.md",
            "timestamp": "2026-04-30T12:00:00Z",
            "frontmatter": {"worker_phase": "iterate-substantive"}
        }
        state2 = bridge_state.append_round(state, round_data)
        assert state2["current_round"] == round_data["round"]
        assert len(state2["rounds"]) >= 1
        # Auto-Propagation worker.phase aus frontmatter (F-RP-26 v0.1.4)
        assert state2["roles"]["worker"]["phase"] == "iterate-substantive"
        results.record("T45 v0.1.5 PB-012 Library append_round + Auto-Propagation", True)
    except Exception as e:
        results.record("T45 v0.1.5 PB-012 Library append_round + Auto-Propagation", False, str(e))

    # Test 46 (v0.1.5 PB-012): Library calibrate_wallclock_post_hoc
    try:
        import bridge_state
        state = synth_valid_state()
        phases = [
            {"phase": "init", "rounds_range": "R0", "estimated_rounds": 1, "actual_rounds": 1},
            {"phase": "scope-lock", "rounds_range": "R1-R11", "estimated_rounds": 5, "actual_rounds": 12, "note": "Profile-Pin-Effekt"}
        ]
        state2 = bridge_state.calibrate_wallclock_post_hoc(state, phases)
        we = state2["wallclock_estimates"]
        assert len(we) == 2
        assert we[1]["drift_factor"] == 2.4  # 12/5 = 2.4 per ADR_0030 Annex A Empirie
        results.record("T46 v0.1.5 PB-012 Library calibrate_wallclock_post_hoc", True)
    except Exception as e:
        results.record("T46 v0.1.5 PB-012 Library calibrate_wallclock_post_hoc", False, str(e))

    # Test 47 (v0.1.5 PB-013): commands/bridge-update.md existiert + Pflicht-Sektionen
    try:
        bu_path = PLUGIN_ROOT / "commands" / "bridge-update.md"
        assert bu_path.exists()
        bu_text = bu_path.read_text()
        for sec in ["## Argumente", "## Pre-Flight", "## Ablauf", "## Output", "## Akzeptanz", "## Anti-Pattern"]:
            assert sec in bu_text, f"Sektion fehlt: {sec}"
        # Whitelist + Library-Cross-Ref
        assert "topic\\|expertise-source\\|worker-focus\\|domain-hint" in bu_text or "topic|expertise-source|worker-focus|domain-hint" in bu_text
        assert "tools/bridge_state.py" in bu_text
        results.record("T47 v0.1.5 PB-013 commands/bridge-update.md", True)
    except Exception as e:
        results.record("T47 v0.1.5 PB-013 commands/bridge-update.md", False, str(e))

    # Test 48 (v0.1.5 PB-013): bridge-update Pre-Flight 3 phase-block dokumentiert
    try:
        bu_text = (PLUGIN_ROOT / "commands" / "bridge-update.md").read_text()
        assert "phase \u2208 {init, scope-lock, iterate}" in bu_text or "phase ∈ {init, scope-lock, iterate}" in bu_text, "phase-Whitelist fehlt"
        assert "execute/verify/close" in bu_text or "Decision-Log brechen" in bu_text, "phase-block-Begruendung fehlt"
        # status_observations Update-Trail
        assert "status_observations" in bu_text
        results.record("T48 v0.1.5 PB-013 bridge-update Pre-Flight phase-block + Update-Trail", True)
    except Exception as e:
        results.record("T48 v0.1.5 PB-013 bridge-update Pre-Flight phase-block + Update-Trail", False, str(e))

    # Test 49 (v0.1.5 Phase H): bridge-close.md §bilanz-schema-enforcement + Library
    try:
        # Library validate_bilanz_against_schema vorhanden
        import bridge_state
        assert "validate_bilanz_against_schema" in bridge_state.__all__, "Library-API fehlt validate_bilanz_against_schema"

        # Synth valide Bilanz validate PASS
        synth_bilanz = {
            "pair_id": "8cbeaad0-e67a-4184-889b-76a70c21d617",
            "pair_topic": "test",
            "created_at": "2026-04-30T00:00:00Z",
            "closed_at": "2026-04-30T01:00:00Z",
            "total_rounds": 5,
            "phase_sequence": [{"phase": "init", "rounds_range": "R0", "rounds_count": 1}],
            "decision_log_summary": [{"decision": "x", "decided_by": "consensus"}],
            "wallclock_drift_calibrated": [{"phase": "init", "estimated_rounds": 1, "actual_rounds": 1, "drift_factor": 1.0}],
            "reflection": {"was_funktionierte": ["a"], "was_problematisch": [], "was_als_naechstes": ["b"]},
            "successful_patterns": [],
            "anti_patterns_detected": [],
            "cross_pair_transfer_hinweise": []
        }
        errors = bridge_state.validate_bilanz_against_schema(synth_bilanz)
        assert errors == [] or errors == ["jsonschema-not-available"], f"unexpected errors: {errors}"

        # bridge-close.md hat §bilanz-schema-enforcement
        bc_path = PLUGIN_ROOT / "commands" / "bridge-close.md"
        assert bc_path.exists()
        bc_text = bc_path.read_text()
        assert "§bilanz-schema-enforcement" in bc_text
        assert "schemas/bilanz_v1.json" in bc_text
        assert "validate_bilanz_against_schema" in bc_text
        results.record("T49 v0.1.5 Phase H bilanz-schema-enforcement", True)
    except Exception as e:
        results.record("T49 v0.1.5 Phase H bilanz-schema-enforcement", False, str(e))

    # Test 50 (v0.1.5 Phase D.1 PB-009): check_drift_plausibility Domain-aware
    try:
        import bridge_state
        # Plugin-Self-Dev domain: p3-drift 2.4 sollte OK sein (range 0.8-3.5)
        result = bridge_state.check_drift_plausibility("plugin-self-dev", 2.4)
        assert result["status"] == "OK", f"p3 drift 2.4 sollte OK sein: {result}"
        # Plugin-Self-Dev: drift 5.0 ausserhalb range → WARN
        result2 = bridge_state.check_drift_plausibility("plugin-self-dev", 5.0)
        assert result2["status"] == "WARN", f"drift 5.0 sollte WARN sein: {result2}"
        # Use-Case: drift 0.67 OK
        result3 = bridge_state.check_drift_plausibility("use-case", 0.67)
        assert result3["status"] == "OK"
        # Default fuer unknown domain
        result4 = bridge_state.check_drift_plausibility(None, 1.5)
        assert result4["status"] == "OK"
        results.record("T50 v0.1.5 Phase D.1 PB-009 check_drift_plausibility Domain-aware", True)
    except Exception as e:
        results.record("T50 v0.1.5 Phase D.1 PB-009 check_drift_plausibility Domain-aware", False, str(e))

    # Test 51 (v0.1.5 Phase D.2 PB-002): compute_reflection_action_ratio + check_ratio_threshold
    try:
        import bridge_state
        # Synth p3-style state: 18 re-sync, 1 initial-advice, 1 decision-lock
        state = synth_valid_state()
        state["rounds"] = (
            [{"round": i, "type": "re-sync", "initiator": "advisor", "artifact_path": "x", "timestamp": "2026-04-30T00:00:00Z"} for i in range(18)] +
            [{"round": 19, "type": "initial-advice", "initiator": "advisor", "artifact_path": "x", "timestamp": "2026-04-30T00:00:00Z"}] +
            [{"round": 20, "type": "decision-lock", "initiator": "worker", "artifact_path": "x", "timestamp": "2026-04-30T00:00:00Z"}]
        )
        ratio = bridge_state.compute_reflection_action_ratio(state)
        assert ratio == 9.0, f"expected 18/2=9.0, got {ratio}"  # 18 re-sync (refl) / 2 action (initial-advice + decision-lock)

        # Domain-aware Threshold-Check
        # Default domain (unknown) → threshold 4.0 → 9.0 > 4.0 = WARN
        state["topic_metadata"] = {"domain_hint": "use-case"}
        result = bridge_state.check_ratio_threshold(state)
        assert result["status"] == "WARN", f"use-case ratio 9 sollte WARN sein"
        assert result["threshold"] == 4.0

        # Plugin-Self-Dev: threshold 15.0 → 9.0 < 15.0 = OK
        state["topic_metadata"]["domain_hint"] = "plugin-self-dev"
        result2 = bridge_state.check_ratio_threshold(state)
        assert result2["status"] == "OK", f"plugin-self-dev ratio 9 sollte OK sein"
        assert result2["threshold"] == 15.0
        results.record("T51 v0.1.5 Phase D.2 PB-002 ratio Domain-aware Threshold", True)
    except Exception as e:
        results.record("T51 v0.1.5 Phase D.2 PB-002 ratio Domain-aware Threshold", False, str(e))

    # Test 52 (v0.1.5 Phase D): bridge-handover.md §lifecycle-health-checks-Sektion
    try:
        bh_text = (PLUGIN_ROOT / "commands" / "bridge-handover.md").read_text()
        assert "§lifecycle-health-checks" in bh_text
        assert "§drift-plausibility-check" in bh_text
        assert "§reflection-action-ratio-check" in bh_text
        # ADR_0031-Cross-Refs
        assert "ADR_0031" in bh_text
        # Empirie-Anker p3 12.5
        assert "12.5" in bh_text or "12.50" in bh_text
        results.record("T52 v0.1.5 Phase D bridge-handover §lifecycle-health-checks", True)
    except Exception as e:
        results.record("T52 v0.1.5 Phase D bridge-handover §lifecycle-health-checks", False, str(e))

    # Test 53 (v0.1.5 Phase D): RATIO_THRESHOLDS + DRIFT_RANGES Konstanten
    try:
        import bridge_state
        # RATIO_THRESHOLDS hat alle 6 ADR_0031-Domains
        rt = bridge_state.RATIO_THRESHOLDS
        for d in ["plugin-self-dev", "use-case", "default"]:
            assert d in rt, f"RATIO_THRESHOLDS fehlt {d}"
        assert rt["plugin-self-dev"] == 15.0
        assert rt["use-case"] == 4.0
        # DRIFT_RANGES
        dr = bridge_state.DRIFT_RANGES
        assert "plugin-self-dev" in dr
        assert dr["plugin-self-dev"]["min"] >= 0.5  # p3-Empirie sanity
        assert dr["plugin-self-dev"]["max"] <= 5.0
        results.record("T53 v0.1.5 Phase D Library-Konstanten RATIO_THRESHOLDS + DRIFT_RANGES", True)
    except Exception as e:
        results.record("T53 v0.1.5 Phase D Library-Konstanten RATIO_THRESHOLDS + DRIFT_RANGES", False, str(e))

    # T54: v0.1.6 ADR_0030 Annex B Profile-with-workflows.md-Pattern dokumentiert
    try:
        adr_path = Path(__file__).parent.parent / "docs/adr/ADR_0030_Expertise_Profile_Pattern.md"
        adr_content = adr_path.read_text()
        assert "## Annex B" in adr_content, "Annex B fehlt"
        assert "Profile-with-workflows.md-Pattern" in adr_content
        assert "workflows.md" in adr_content
        assert "Vorrang" in adr_content, "Vorrang-Regel nicht dokumentiert"
        assert "Backward-Compatibility" in adr_content or "backward-compat" in adr_content.lower()
        results.record("T54 v0.1.6 ADR_0030 Annex B workflows.md-Pattern dokumentiert", True)
    except Exception as e:
        results.record("T54 v0.1.6 ADR_0030 Annex B workflows.md-Pattern dokumentiert", False, str(e))

    # T55: v0.1.6 bridge-advisor SKILL.md workflows.md-Loading-Patch
    try:
        skill_path = Path(__file__).parent.parent / "skills/bridge-advisor/SKILL.md"
        skill_content = skill_path.read_text()
        # Schritt 0 Pseudocode erwähnt workflows.md
        assert "workflows.md" in skill_content, "workflows.md nicht in SKILL.md"
        # workflow_specs als Profile-Substruktur
        assert "workflow_specs" in skill_content, "workflow_specs Variable fehlt"
        # Vorrang-Regel
        assert "Vorrang" in skill_content, "Vorrang-Regel fehlt"
        # Anti-Pattern Workflow-Output-Format-Enforcement
        assert "workflows.md-Output-Formate ignorieren" in skill_content, "AP für Output-Format-Enforcement fehlt"
        # Verweigerungs-Logik
        assert "Verweigerungs-Logik" in skill_content or "verweigerungs_klausel" in skill_content
        # Cross-Ref auf Annex B
        assert "Annex B" in skill_content and "v0.1.6" in skill_content, "Cross-Ref auf v0.1.6 Annex B fehlt"
        results.record("T55 v0.1.6 bridge-advisor SKILL.md workflows.md-Loading-Patch", True)
    except Exception as e:
        results.record("T55 v0.1.6 bridge-advisor SKILL.md workflows.md-Loading-Patch", False, str(e))

    # T56: v0.1.6 klafki-didaktik Reference-Profile vollständig
    try:
        klafki_dir = Path("/Users/paulad/session-bridge/private-notes/expertise-profiles/klafki-didaktik")
        if not klafki_dir.exists():
            # Skip wenn private-notes nicht vorhanden (CI-Environment)
            results.record("T56 v0.1.6 klafki-didaktik Reference-Profile (skip-if-private)", True, "skipped: private-notes not present")
        else:
            for f in ["PROFILE.md", "diagnostic-frames.md", "anti-patterns.md", "question-bank.md", "workflows.md"]:
                assert (klafki_dir / f).exists(), f"klafki-didaktik missing {f}"
            # workflows.md hat 5 Workflows
            wf_text = (klafki_dir / "workflows.md").read_text()
            wf_ids = re.findall(r"## (W-\d+):", wf_text)
            assert len(wf_ids) == 5, f"klafki workflows count {len(wf_ids)} != 5"
            # PROFILE.md required_files enthält workflows.md
            profile_text = (klafki_dir / "PROFILE.md").read_text()
            assert "workflows.md" in profile_text, "workflows.md nicht in required_files"
            results.record("T56 v0.1.6 klafki-didaktik Reference-Profile vollständig", True)
    except Exception as e:
        results.record("T56 v0.1.6 klafki-didaktik Reference-Profile vollständig", False, str(e))

    # T57: v0.1.7 ADR_0030 Annex C Multi-Pass-Workflow-Pattern + File-Aliase
    try:
        adr_path = Path(__file__).parent.parent / "docs/adr/ADR_0030_Expertise_Profile_Pattern.md"
        adr_content = adr_path.read_text()
        assert "## Annex C" in adr_content, "Annex C fehlt"
        assert "Multi-Pass-Workflow-Pattern" in adr_content
        assert "File-Aliase" in adr_content or "File-Aliasen" in adr_content
        assert "passes" in adr_content
        assert "konstellations-anker.md" in adr_content, "Adorno-Alias nicht referenziert"
        assert "negative-diagnose-fragen.md" in adr_content
        assert "selbstkritik_klausel" in adr_content
        results.record("T57 v0.1.7 ADR_0030 Annex C Multi-Pass + File-Aliase dokumentiert", True)
    except Exception as e:
        results.record("T57 v0.1.7 ADR_0030 Annex C Multi-Pass + File-Aliase dokumentiert", False, str(e))

    # T58: v0.1.7 bridge-advisor SKILL.md Multi-Pass-Loading + File-Aliase + Selbstkritik-Enforcement
    try:
        skill_path = Path(__file__).parent.parent / "skills/bridge-advisor/SKILL.md"
        skill_content = skill_path.read_text()
        # File-Aliase
        assert "File-Aliase" in skill_content, "File-Aliase nicht in SKILL.md"
        assert "konstellations-anker.md" in skill_content
        assert "negative-diagnose-fragen.md" in skill_content
        # Multi-Pass-Workflow-Loading
        assert "Multi-Pass-Workflow-Loading" in skill_content, "Multi-Pass-Loading nicht in SKILL.md"
        assert "passes" in skill_content
        assert "lesart" in skill_content, "Pass-Lesart-Konvention nicht erwaehnt"
        # Anti-Pattern Pass-Skip-Verbot
        assert "Multi-Pass-Workflow-passes überspringen" in skill_content
        # Anti-Pattern Selbstkritik-Klausel
        assert "Selbstkritik-Klauseln" in skill_content
        results.record("T58 v0.1.7 SKILL.md Multi-Pass-Loading + File-Aliase + Selbstkritik-Enforcement", True)
    except Exception as e:
        results.record("T58 v0.1.7 SKILL.md Multi-Pass-Loading + File-Aliase + Selbstkritik-Enforcement", False, str(e))

    # T76: architecture-archaeology Reference-Profile (skip-if-private)
    try:
        arch_dir = Path("/Users/paulad/session-bridge/private-notes/expertise-profiles/architecture-archaeology")
        if not arch_dir.exists():
            results.record("T76 architecture-archaeology Reference-Profile (skip-if-private)", True, "skipped")
        else:
            for f in ["PROFILE.md", "diagnostic-frames.md", "anti-patterns.md",
                      "question-bank.md", "workflows.md", "token-efficiency-patterns.md"]:
                assert (arch_dir / f).exists(), f"arch missing {f}"
            wf_text = (arch_dir / "workflows.md").read_text()
            wf_ids = re.findall(r"## (W-A-[\w-]+):", wf_text)
            assert len(wf_ids) >= 6, f"arch workflows count {len(wf_ids)}"
            for wid in ["W-A-Triangulate", "W-A-Drift-Diagnose", "W-A-Token-Forensik",
                        "W-A-Inflation-Detektion", "W-A-Approximations-Test", "W-A-Reflex"]:
                assert wid in wf_ids, f"missing workflow: {wid}"
            # Multi-Pass Triangulate + Approximations + Reflex
            for wid in ["W-A-Triangulate", "W-A-Approximations-Test", "W-A-Reflex"]:
                bm = re.search(rf"## {re.escape(wid)}:.*?(?=## W-A-|## Workflow|---\Z)", wf_text, re.DOTALL)
                assert bm
                for p in [1, 2, 3, 4]:
                    assert f"### Pass {p}" in bm.group(0), f"{wid} pass {p} fehlt"
            # 10 APs mit Selbstanwendung
            ap_text = (arch_dir / "anti-patterns.md").read_text()
            ap_ids = re.findall(r"## (AP-T\d+):", ap_text)
            assert len(ap_ids) == 10
            assert ap_text.count("**SELBSTANWENDUNG:**") >= 10
            assert "Anti-Kosmetik" in ap_text
            # token-efficiency-patterns: 8 IP + 8 OP
            tep = (arch_dir / "token-efficiency-patterns.md").read_text()
            ip_ids = re.findall(r"### IP-(\d+)", tep)
            assert len(set(ip_ids)) == 8
            op_ids = re.findall(r"### OP-(\d+)", tep)
            assert len(set(op_ids)) == 8
            # Anti-Kosmetik in workflows
            assert "W-A-Anti-Kosmetik" in wf_text
            results.record("T76 architecture-archaeology Reference-Profile (6 Files + 8 IP/OP + Anti-Kosmetik)", True)
    except Exception as e:
        results.record("T76 architecture-archaeology Reference-Profile", False, str(e))

    # T71: v0.1.10 bridge-close.md §Memory-Symmetrie-Pflicht-Workflow
    try:
        bc_path = Path(__file__).parent.parent / "commands/bridge-close.md"
        c = bc_path.read_text()
        assert "§Memory-Symmetrie-Pflicht-Workflow" in c, "Memory-Symmetrie-Section fehlt"
        assert "Pattern-#103" in c, "Pattern-#103-Ref fehlt"
        assert "memory_symmetry_status" in c
        assert "advisor_items" in c or "Advisor-Memory" in c
        assert "worker_items" in c or "Worker-Memory" in c
        assert "Pre-Init-WARN" in c
        results.record("T71 v0.1.10 bridge-close §Memory-Symmetrie-Pflicht-Workflow", True)
    except Exception as e:
        results.record("T71 v0.1.10 bridge-close §Memory-Symmetrie-Pflicht-Workflow", False, str(e))

    # T72: v0.1.10 schemas/bridge_state_v1 domain_hint cross-project + memory_symmetry_status
    try:
        s_path = Path(__file__).parent.parent / "schemas/bridge_state_v1.json"
        schema = json.loads(s_path.read_text())
        domain_enum = schema["properties"]["topic_metadata"]["properties"]["domain_hint"]["enum"]
        for v in ["plugin-self-dev", "use-case", "use-case-with-profile",
                  "architecture-spec", "architecture-spec-patch",
                  "cross-project", "investigation-trace", "methodology-improvement", "other"]:
            assert v in domain_enum, f"missing domain_hint enum: {v}"
        # memory_symmetry_status field
        assert "memory_symmetry_status" in schema["properties"]
        mss = schema["properties"]["memory_symmetry_status"]
        for s in ["pending", "partial", "complete", "skipped"]:
            assert s in mss["enum"], f"missing status: {s}"
        results.record("T72 v0.1.10 bridge_state_v1 cross-project + memory_symmetry_status", True)
    except Exception as e:
        results.record("T72 v0.1.10 bridge_state_v1 cross-project + memory_symmetry_status", False, str(e))

    # T73: v0.1.10 handover_frontmatter_v1 source_of_truth_locked-Field
    try:
        h_path = Path(__file__).parent.parent / "schemas/handover_frontmatter_v1.json"
        hschema = json.loads(h_path.read_text())
        assert "source_of_truth_locked" in hschema["properties"]
        sot = hschema["properties"]["source_of_truth_locked"]
        assert sot["type"] == "array"
        assert "ref" in sot["items"]["required"]
        assert "at_round" in sot["items"]["required"]
        assert "drift_against" in sot["items"]["properties"]
        results.record("T73 v0.1.10 handover_frontmatter source_of_truth_locked", True)
    except Exception as e:
        results.record("T73 v0.1.10 handover_frontmatter source_of_truth_locked", False, str(e))

    # T74: v0.1.10 tools/bridge_state DRIFT_RANGES cross-project + TRACK_TYPE_DRIFT_EMPIRIE
    try:
        from tools import bridge_state as bs
        # cross-project in DRIFT_RANGES
        assert "cross-project" in bs.DRIFT_RANGES
        cp = bs.DRIFT_RANGES["cross-project"]
        assert cp["min"] == 0.20
        assert cp["max"] == 0.5
        # architecture-spec NEU
        assert "architecture-spec" in bs.DRIFT_RANGES
        # cross-project in RATIO_THRESHOLDS
        assert bs.RATIO_THRESHOLDS["cross-project"] == 6.0
        # TRACK_TYPE_DRIFT_EMPIRIE
        assert hasattr(bs, "TRACK_TYPE_DRIFT_EMPIRIE")
        for tt in ["schema", "doku", "validator", "spec-patch", "code"]:
            assert tt in bs.TRACK_TYPE_DRIFT_EMPIRIE
        # spec-patch ist VALIDE (n=4)
        assert bs.TRACK_TYPE_DRIFT_EMPIRIE["spec-patch"]["status"] == "VALIDE"
        # schema/doku/validator sind HYPOTHESE
        assert bs.TRACK_TYPE_DRIFT_EMPIRIE["schema"]["status"] == "HYPOTHESE"
        # __all__ exports
        assert "TRACK_TYPE_DRIFT_EMPIRIE" in bs.__all__
        results.record("T74 v0.1.10 DRIFT_RANGES cross-project + TRACK_TYPE_DRIFT_EMPIRIE", True)
    except Exception as e:
        results.record("T74 v0.1.10 DRIFT_RANGES cross-project + TRACK_TYPE_DRIFT_EMPIRIE", False, str(e))

    # T75: v0.1.10 ADR_0029 Annex D Cross-Pair-Empirie post-v0.1.9
    try:
        adr_path = Path(__file__).parent.parent / "docs/adr/ADR_0029_Session_Bridge_Pattern.md"
        c = adr_path.read_text()
        assert "## Annex D" in c
        assert "Cross-Pair-Empirie-Konsolidierung post-v0.1.9" in c
        assert "Pattern-#103" in c
        assert "Pattern-#109" in c
        assert "p10-phase1a-foundation-audit" in c
        assert "p11-eg-schsch-architektur-import" in c
        assert "Source-of-Truth-Lock" in c
        assert "Iteration-Cycle-4-Round-Pattern" in c
        results.record("T75 v0.1.10 ADR_0029 Annex D Cross-Pair-Empirie", True)
    except Exception as e:
        results.record("T75 v0.1.10 ADR_0029 Annex D Cross-Pair-Empirie", False, str(e))

    # T68: v0.1.9 bridge-advisor SKILL.md §Phase-Gate-Audit + §Cowork-Mode-Composition
    try:
        skill_path = Path(__file__).parent.parent / "skills/bridge-advisor/SKILL.md"
        c = skill_path.read_text()
        assert "§Phase-Gate-Audit-Pflicht" in c, "Phase-Gate-Audit fehlt"
        assert "Pattern-#88" in c, "Pattern-#88-Ref fehlt"
        assert "§Cowork-Mode-Composition-Pattern" in c, "Cowork-Mode-Composition fehlt"
        assert "Reading-Pattern-Skill" in c
        assert "Pattern-#76" in c
        # Phase-Gate-Audit-Output-Format
        assert "§Phase-Gate-Audit (v0.1.9-Pflicht)" in c
        assert "Audit-Verdikt" in c
        results.record("T68 v0.1.9 bridge-advisor Phase-Gate-Audit + Cowork-Composition", True)
    except Exception as e:
        results.record("T68 v0.1.9 bridge-advisor Phase-Gate-Audit + Cowork-Composition", False, str(e))

    # T69: v0.1.9 bridge-worker SKILL.md §Phase-Gate-Spiegel + §User-Veto + §Cowork-Mode-Composition
    try:
        skill_path = Path(__file__).parent.parent / "skills/bridge-worker/SKILL.md"
        c = skill_path.read_text()
        assert "§Cowork-Mode-Composition-Pattern" in c
        assert "Reading-Pattern-Skill" in c
        assert "§Phase-Gate-Pflicht-Spiegel-Klausel" in c, "Phase-Gate-Spiegel fehlt"
        assert "§User-Veto-Authority" in c, "User-Veto fehlt"
        assert "Pattern-#89" in c
        assert "Final-Authority" in c
        results.record("T69 v0.1.9 bridge-worker Phase-Gate-Spiegel + User-Veto + Cowork-Composition", True)
    except Exception as e:
        results.record("T69 v0.1.9 bridge-worker Phase-Gate-Spiegel + User-Veto + Cowork-Composition", False, str(e))

    # T70: v0.1.9 DRIFT_RANGES + ADR_0029 Annex C empirisch updated
    try:
        from tools import bridge_state as bs
        # use-case mit min=0.05 (post-empirisch)
        assert bs.DRIFT_RANGES["use-case"]["min"] == 0.05, f'use-case min: {bs.DRIFT_RANGES["use-case"]["min"]}'
        assert bs.DRIFT_RANGES["use-case"]["max"] == 2.0
        assert bs.DRIFT_RANGES["use-case"]["stddev"] == 0.4
        # use-case-with-profile NEU in DRIFT_RANGES
        assert "use-case-with-profile" in bs.DRIFT_RANGES, "use-case-with-profile fehlt in DRIFT_RANGES"
        # default min=0.05 (extreme-low aus p8 0.05)
        assert bs.DRIFT_RANGES["default"]["min"] == 0.05
        # ADR_0029 Annex C
        adr_path = Path(__file__).parent.parent / "docs/adr/ADR_0029_Session_Bridge_Pattern.md"
        adr = adr_path.read_text()
        assert "## Annex C" in adr
        assert "Cross-Pair-Empirie-Konsolidierung" in adr
        assert "Pattern-#88" in adr
        assert "L-p8-01" in adr
        assert "Klafki-Profile-Pin-Mechanik" in adr
        results.record("T70 v0.1.9 DRIFT_RANGES + ADR_0029 Annex C", True)
    except Exception as e:
        results.record("T70 v0.1.9 DRIFT_RANGES + ADR_0029 Annex C", False, str(e))

    # T62: v0.1.8 tools.bridge_state Pre-Flight-Helpers verfügbar
    try:
        from tools import bridge_state
        for fn in ["resolve_shared_path_default", "resolve_profile_path",
                   "_slugify_topic", "_next_pilot_id"]:
            assert hasattr(bridge_state, fn), f"missing function: {fn}"
        for const in ["PROFILE_SHORT_NAMES", "PROFILE_SEARCH_DIRS"]:
            assert hasattr(bridge_state, const), f"missing constant: {const}"
        # PROFILE_SHORT_NAMES enthält alle 5 Profile
        for short in ["klafki", "adorno", "foucault", "luhmann", "process-consulting"]:
            assert short in bridge_state.PROFILE_SHORT_NAMES, f"missing short-name: {short}"
        # __all__ erweitert
        assert "resolve_shared_path_default" in bridge_state.__all__
        assert "resolve_profile_path" in bridge_state.__all__
        assert "PROFILE_SHORT_NAMES" in bridge_state.__all__
        results.record("T62 v0.1.8 tools.bridge_state Pre-Flight-Helpers", True)
    except Exception as e:
        results.record("T62 v0.1.8 tools.bridge_state Pre-Flight-Helpers", False, str(e))

    # T63: v0.1.8 _slugify_topic + _next_pilot_id Logik
    try:
        from tools.bridge_state import _slugify_topic, _next_pilot_id, resolve_shared_path_default
        import tempfile

        # Slugify-Tests
        assert _slugify_topic("Klafki UE-Beratung") == "klafki-ue-beratung"
        assert _slugify_topic("A B!@# C") == "a-b-c"
        assert _slugify_topic("ÄÖÜ Test") == "test", f'umlaut-strip: got "{_slugify_topic("ÄÖÜ Test")}"'
        long_topic = "x" * 100
        assert len(_slugify_topic(long_topic)) <= 30

        # _next_pilot_id mit tmpdir
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            assert _next_pilot_id(base) == 1, "leerer dir -> 1"
            (base / "p1-test").mkdir()
            (base / "p3-test").mkdir()
            (base / "p7-test").mkdir()
            assert _next_pilot_id(base) == 8, "max+1 statt count"

        # resolve_shared_path_default
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            p = resolve_shared_path_default("Test Topic", base_dir=base)
            assert p.parent == base
            assert p.name == "p1-test-topic"

        results.record("T63 v0.1.8 slugify + next_pilot_id Logik", True)
    except Exception as e:
        results.record("T63 v0.1.8 slugify + next_pilot_id Logik", False, str(e))

    # T64: v0.1.8 resolve_profile_path mit Short-Names + Glob (skip-if-private)
    try:
        from tools.bridge_state import resolve_profile_path, PROFILE_SHORT_NAMES
        import tempfile
        # Setup Mock-Profile-Verzeichnis
        with tempfile.TemporaryDirectory() as td:
            search_dir = Path(td)
            (search_dir / "klafki-didaktik").mkdir()
            (search_dir / "adorno-halbbildung-kritik").mkdir()
            (search_dir / "foucault-genealogie").mkdir()
            (search_dir / "luhmann-erziehungssystem").mkdir()
            (search_dir / "process-consulting").mkdir()

            # Short-name resolution
            assert resolve_profile_path("klafki", search_dirs=[search_dir]).name == "klafki-didaktik"
            assert resolve_profile_path("adorno", search_dirs=[search_dir]).name == "adorno-halbbildung-kritik"
            assert resolve_profile_path("foucault", search_dirs=[search_dir]).name == "foucault-genealogie"
            assert resolve_profile_path("luhmann", search_dirs=[search_dir]).name == "luhmann-erziehungssystem"
            assert resolve_profile_path("process-consulting", search_dirs=[search_dir]).name == "process-consulting"

            # Absolute path
            abs_p = search_dir / "klafki-didaktik"
            assert resolve_profile_path(str(abs_p), search_dirs=[search_dir]) == abs_p

            # Not found
            try:
                resolve_profile_path("nonexistent", search_dirs=[search_dir])
                assert False, "sollte FileNotFoundError werfen"
            except FileNotFoundError:
                pass

        results.record("T64 v0.1.8 resolve_profile_path Short-Names + Glob", True)
    except Exception as e:
        results.record("T64 v0.1.8 resolve_profile_path Short-Names + Glob", False, str(e))

    # T65: v0.1.8 commands/bridge-init.md Pre-Flight Phase A dokumentiert
    try:
        bi_path = Path(__file__).parent.parent / "commands/bridge-init.md"
        bi_content = bi_path.read_text()
        assert "Pre-Flight Phase A" in bi_content
        assert "Auto-Resolution" in bi_content or "auto-resolution" in bi_content.lower()
        assert "request_cowork_directory" in bi_content
        assert "Phase A.1" in bi_content
        assert "Phase A.2" in bi_content
        assert "Phase A.3" in bi_content
        assert "PROFILE_SHORT_NAMES" in bi_content or "Kurz-Name" in bi_content
        results.record("T65 v0.1.8 bridge-init.md Pre-Flight Phase A", True)
    except Exception as e:
        results.record("T65 v0.1.8 bridge-init.md Pre-Flight Phase A", False, str(e))

    # T66: v0.1.8 commands/bridge-attach.md Pre-Flight Phase A dokumentiert
    try:
        ba_path = Path(__file__).parent.parent / "commands/bridge-attach.md"
        ba_content = ba_path.read_text()
        assert "Pre-Flight Phase A" in ba_content
        assert "request_cowork_directory" in ba_content
        results.record("T66 v0.1.8 bridge-attach.md Pre-Flight Phase A", True)
    except Exception as e:
        results.record("T66 v0.1.8 bridge-attach.md Pre-Flight Phase A", False, str(e))

    # T67: v0.1.8 ADR_0030 Annex D
    try:
        adr_path = Path(__file__).parent.parent / "docs/adr/ADR_0030_Expertise_Profile_Pattern.md"
        adr_content = adr_path.read_text()
        assert "## Annex D" in adr_content
        assert "Pre-Flight Auto-Resolution" in adr_content
        assert "PROFILE_SHORT_NAMES" in adr_content
        assert "request_cowork_directory" in adr_content
        results.record("T67 v0.1.8 ADR_0030 Annex D Pre-Flight Pattern", True)
    except Exception as e:
        results.record("T67 v0.1.8 ADR_0030 Annex D Pre-Flight Pattern", False, str(e))

    # T61: luhmann-erziehungssystem Reference-Profile vollständig (skip-if-private)
    try:
        luhmann_dir = Path("/Users/paulad/session-bridge/private-notes/expertise-profiles/luhmann-erziehungssystem")
        if not luhmann_dir.exists():
            results.record("T61 luhmann-erziehungssystem Reference-Profile (skip-if-private)", True, "skipped: private-notes not present")
        else:
            for f in ["PROFILE.md", "diagnostic-frames.md", "anti-patterns.md", "question-bank.md", "workflows.md"]:
                assert (luhmann_dir / f).exists(), f"luhmann missing {f}"
            wf_text = (luhmann_dir / "workflows.md").read_text()
            wf_ids = re.findall(r"## (W-L-\w+):", wf_text)
            assert len(wf_ids) == 6, f"luhmann workflows count {len(wf_ids)} != 6"
            for wid in ["W-L-Funkdiff", "W-L-Beob2", "W-L-Reflex"]:
                block_match = re.search(rf"## {re.escape(wid)}:.*?(?=## W-L-|## Workflow|---\Z)", wf_text, re.DOTALL)
                assert block_match
                for p in [1, 2, 3, 4]:
                    assert f"### Pass {p}" in block_match.group(0), f"{wid} pass {p} fehlt"
            frames_text = (luhmann_dir / "diagnostic-frames.md").read_text()
            frame_ids = re.findall(r"### Frame (F\d+\.\d+)", frames_text)
            assert len(frame_ids) == 10, f"luhmann frames count {len(frame_ids)} != 10"
            ap_text = (luhmann_dir / "anti-patterns.md").read_text()
            ap_ids = re.findall(r"## (AP-L\d+):", ap_text)
            assert len(ap_ids) == 10, f"luhmann APs count {len(ap_ids)} != 10"
            assert ap_text.count("**SELBSTANWENDUNG:**") >= 10
            all_text = (luhmann_dir / "PROFILE.md").read_text() + frames_text + ap_text + wf_text
            for marker in ["Funktionssystem", "Code", "Programm", "strukturelle Kopplung",
                          "Beobachtung 2. Ordnung", "operative Geschlossenheit",
                          "System/Umwelt", "Re-Entry", "Erziehungssystem", "Karriere-Code"]:
                assert marker in all_text, f"Methodik-Marker fehlt: {marker}"
            results.record("T61 luhmann-erziehungssystem Reference-Profile vollständig", True)
    except Exception as e:
        results.record("T61 luhmann-erziehungssystem Reference-Profile vollständig", False, str(e))

    # T60: foucault-genealogie Reference-Profile vollständig (skip-if-private)
    try:
        foucault_dir = Path("/Users/paulad/session-bridge/private-notes/expertise-profiles/foucault-genealogie")
        if not foucault_dir.exists():
            results.record("T60 foucault-genealogie Reference-Profile (skip-if-private)", True, "skipped: private-notes not present")
        else:
            for f in ["PROFILE.md", "diagnostic-frames.md", "anti-patterns.md", "question-bank.md", "workflows.md"]:
                assert (foucault_dir / f).exists(), f"foucault missing {f}"
            # workflows.md hat 6 Workflows
            wf_text = (foucault_dir / "workflows.md").read_text()
            wf_ids = re.findall(r"## (W-F-\w+):", wf_text)
            assert len(wf_ids) == 6, f"foucault workflows count {len(wf_ids)} != 6"
            # W-F-Genea + W-F-Reflex haben 4 Passes
            for wid in ["W-F-Genea", "W-F-Reflex"]:
                block_match = re.search(rf"## {re.escape(wid)}:.*?(?=## W-F-|## Workflow|---\Z)", wf_text, re.DOTALL)
                assert block_match, f"{wid} block not found"
                for p in [1, 2, 3, 4]:
                    assert f"### Pass {p}" in block_match.group(0), f"{wid} pass {p} fehlt"
            # 10 Frames
            frames_text = (foucault_dir / "diagnostic-frames.md").read_text()
            frame_ids = re.findall(r"### Frame (F\d+\.\d+)", frames_text)
            assert len(frame_ids) == 10, f"foucault frames count {len(frame_ids)} != 10"
            # 10 APs mit Selbstanwendungs-Pflicht
            ap_text = (foucault_dir / "anti-patterns.md").read_text()
            ap_ids = re.findall(r"## (AP-F\d+):", ap_text)
            assert len(ap_ids) == 10, f"foucault APs count {len(ap_ids)} != 10"
            assert ap_text.count("**SELBSTANWENDUNG:**") >= 10, "Selbstanwendungs-Pflicht nicht erfüllt"
            # Foucault-spezifische Methodik-Marker
            all_text = (foucault_dir / "PROFILE.md").read_text() + frames_text + ap_text + wf_text
            for marker in ["Genealogie", "Macht-Wissen", "Disziplinargesellschaft", "Dispositiv", "Subjektivierung"]:
                assert marker in all_text, f"Methodik-Marker fehlt: {marker}"
            results.record("T60 foucault-genealogie Reference-Profile vollständig", True)
    except Exception as e:
        results.record("T60 foucault-genealogie Reference-Profile vollständig", False, str(e))

    # T59: v0.1.7 adorno-halbbildung-kritik Reference-Profile vollständig
    try:
        adorno_dir = Path("/Users/paulad/session-bridge/private-notes/expertise-profiles/adorno-halbbildung-kritik")
        if not adorno_dir.exists():
            results.record("T59 v0.1.7 adorno-halbbildung-kritik Reference-Profile (skip-if-private)", True, "skipped: private-notes not present")
        else:
            # Adorno verwendet File-Aliase
            for f in ["PROFILE.md", "konstellations-anker.md", "anti-patterns.md", "negative-diagnose-fragen.md", "workflows.md"]:
                assert (adorno_dir / f).exists(), f"adorno missing {f}"
            # workflows.md hat W-A-Multi mit passes
            wf_text = (adorno_dir / "workflows.md").read_text()
            assert "W-A-Multi" in wf_text
            assert "Pass 1" in wf_text and "Pass 2" in wf_text and "Pass 3" in wf_text and "Pass 4" in wf_text
            assert "literal" in wf_text and "konzeptuell-immanent" in wf_text and "anti-identifikatorische-konstellation" in wf_text and "meta-kritisch" in wf_text
            # Selbstkritik-Klausel pro Workflow
            assert "Selbstkritik-Klausel" in wf_text
            # PROFILE.md required_files enthält Aliase
            profile_text = (adorno_dir / "PROFILE.md").read_text()
            assert "konstellations-anker.md" in profile_text
            assert "negative-diagnose-fragen.md" in profile_text
            # 10 Konstellations-Anker
            anker_text = (adorno_dir / "konstellations-anker.md").read_text()
            anker_ids = re.findall(r"## A(\d+)", anker_text)
            assert len(anker_ids) == 10, f"adorno anker count {len(anker_ids)} != 10"
            # 10 APs
            ap_text = (adorno_dir / "anti-patterns.md").read_text()
            ap_ids = re.findall(r"## (AP-A\d+):", ap_text)
            assert len(ap_ids) == 10, f"adorno AP count {len(ap_ids)} != 10"
            # Selbstanwendungs-Sektion in jedem AP
            assert ap_text.count("**SELBSTANWENDUNG:**") >= 10, f"AP-Selbstanwendung-Pflicht nicht erfüllt"
            results.record("T59 v0.1.7 adorno-halbbildung-kritik Reference-Profile vollständig", True)
    except Exception as e:
        results.record("T59 v0.1.7 adorno-halbbildung-kritik Reference-Profile vollständig", False, str(e))

    if verbose:
        print("Passed:", results.passed)

    print(results.summary())
    return results.exit_code()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    sys.exit(main(verbose=args.verbose))
