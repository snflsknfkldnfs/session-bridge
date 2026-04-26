#!/usr/bin/env python3
"""Setup-Skript: bereitet shared/bridge/state.json (post-attach Phase=scope-lock) für P2 Subagent-Pair-Pilot vor."""

import json
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED = SCRIPT_DIR / "shared"
BRIDGE = SHARED / "bridge"


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    if BRIDGE.exists():
        shutil.rmtree(BRIDGE)
    BRIDGE.mkdir(parents=True)
    (BRIDGE / "handover").mkdir()
    (BRIDGE / "artifacts").mkdir()
    (BRIDGE / "orphans").mkdir()

    pair_id = str(uuid.uuid4())
    state = {
        "pair_id": pair_id,
        "schema_version": "1.0.0",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "phase": "scope-lock",
        "roles": {
            "advisor": {
                "session_id": "subagent_advisor",
                "expertise_source": "p2-pilot-mock-expertise",
                "active_since": now_iso(),
            },
            "worker": {
                "session_id": "subagent_worker",
                "current_focus": "p2-pilot-mock-feature",
                "phase": "phase-test",
                "active_since": now_iso(),
            },
        },
        "topic": "p2-subagent-pair-pilot-topic",
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
    (BRIDGE / "state.json").write_text(json.dumps(state, indent=2))
    print(f"Initial state written: pair_id={pair_id}")
    print(f"State path: {BRIDGE / 'state.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
