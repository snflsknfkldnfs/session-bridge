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
        "schema_version": "1.0.0",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "phase": "iterate",
        "roles": {
            "advisor": {
                "session_id": "local_advisor_test",
                "expertise_source": "smoke-test-fixture",
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

    if verbose:
        print("Passed:", results.passed)

    print(results.summary())
    return results.exit_code()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    sys.exit(main(verbose=args.verbose))
