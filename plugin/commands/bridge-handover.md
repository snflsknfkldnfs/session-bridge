---
description: Schreibt einen Handover-Eintrag (advisor↔worker oder worker↔advisor) im Pair. Validiert Frontmatter gegen Schema vor Persistierung. Atomic-CAS-Write auf state.json mit Round-Counter-Increment.
argument-hint: --type=<round-type> [--summary="<string>"] [--references=<json-array>] [--blockers=B-1,B-2] [--decisions=D-1] [--acceptance=<json-array>] [--rollback=<json-array>] [--wallclock-min=<int>] [--decided-by=<user|consensus>]
---

# /bridge-handover

Schreibt einen Handover-Eintrag in `bridge/handover/<round>-<from>-<to>-<short-uuid>.md`.

## Argumente

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--type=<round-type>` | ja | siehe ADR_0029 §4.2 (initial-advice, counter, re-sync, decision-lock, pre-patch, pre-flight, execute, verify, status, question) |
| `--summary="<string>"` | empfohlen | Zusammenfassung für Body-Section |
| `--references=<json-array>` | ja (≥1) | mind. 1 reference, format: `[{"type":"...","pointer":"...","verified":true}]` |
| `--blockers=B-1,B-2` | optional | related_blockers |
| `--decisions=D-1,D-2` | optional | related_decisions |
| `--acceptance=<json-array>` | wenn type ∈ {pre-patch, execute, verify} | acceptance_criteria |
| `--rollback=<json-array>` | wenn type=execute | format: `[{"condition":"...","action":"..."}]` |
| `--wallclock-min=<int>` | wenn type ∈ {pre-patch, execute} | Schätzung Wall-Clock-Minuten |
| `--decided-by=<user\|consensus>` | wenn type=decision-lock | Wer hat entschieden |

## Pre-Flight

1. `bridge/state.json` existiert + Schema-Validate PASS
2. This_session_id ∈ {state.roles.advisor.session_id, state.roles.worker.session_id}
3. State.phase ∈ {scope-lock, iterate, execute, verify} (nicht init / close)
4. Round-Type ist mit aktueller Phase kompatibel:
   - scope-lock: nur status, question, initial-advice
   - iterate: alles ausser execute, verify
   - execute: pre-flight, execute, status, question
   - verify: verify, status, question

## Ablauf

```python
# 1. State-Read + CAS-init
state = read_state()
read_at = state["updated_at"]

# 2. Status-Snapshot generieren (PFLICHT D1, FM-1)
worker_phase = read_worker_phase()  # eigener Status oder via session_info
worker_focus = read_worker_focus()
status_verified_at = now_iso()

# 3. Frontmatter bauen
this_role = "advisor" if state.roles.advisor.session_id == this_session_id else "worker"
other_role = "worker" if this_role == "advisor" else "advisor"
new_round = state.current_round + 1
short_uuid = uuid.uuid4().hex[:8]

frontmatter = {
    "pair_id": state.pair_id,
    "round": new_round,
    "from": this_role,
    "to": other_role,
    "type": args.type,
    "timestamp": now_iso(),
    "worker_phase": worker_phase,
    "worker_focus": worker_focus,
    "status_verified_at": status_verified_at,
    "references": args.references,
    **({"related_blockers": args.blockers} if args.blockers else {}),
    **({"related_decisions": args.decisions} if args.decisions else {}),
    **({"acceptance_criteria": args.acceptance} if args.acceptance else {}),
    **({"rollback_triggers": args.rollback} if args.rollback else {}),
    **({"wallclock_estimate_min": args.wallclock_min} if args.wallclock_min else {}),
    **({"decided_by": args.decided_by} if args.decided_by else {})
}

# 4. Schema-Validate VOR Persistierung
validate(frontmatter, handover_frontmatter_v1_schema)
# Schema enforced allOf-Pflichten (z.B. acceptance_criteria bei type=pre-patch)

# 5. Handover-File schreiben
artifact_path = f"bridge/handover/{new_round}-{this_role}-{other_role}-{short_uuid}.md"
write_handover_file(artifact_path, frontmatter, body=args.summary)

# 6. State.json updaten (Atomic-CAS)
state.rounds.append({
    "round": new_round,
    "type": args.type,
    "initiator": this_role,
    "artifact_path": artifact_path,
    "timestamp": now_iso()
})
state.current_round = new_round
state.updated_at = now_iso()

# Phase-Auto-Übergänge:
if state.phase == "scope-lock" and args.type == "initial-advice":
    state.phase = "iterate"
elif state.phase == "iterate" and args.type == "decision-lock":
    pass  # Phase bleibt iterate, execute kommt erst nach pre-flight
elif state.phase == "iterate" and args.type == "pre-flight":
    state.phase = "execute"
elif state.phase == "execute" and args.type == "verify":
    state.phase = "verify"

# Wallclock-Estimate tracken
if args.wallclock_min:
    state.wallclock_estimates.append({
        "round": new_round,
        "estimated_min": args.wallclock_min,
        "actual_min": None,
        "drift_factor": None
    })

# Decision-Log bei decision-lock
if args.type == "decision-lock":
    state.decision_log.append({
        "round": new_round,
        "decision": args.summary,
        "rationale": "...",  # Body-extracted
        "decided_by": args.decided_by,
        "alternatives_considered": []
    })

write_atomic_cas(state, expected_updated_at=read_at)
```

## Akzeptanz

- Handover-File existiert + Frontmatter-Schema-Validate PASS
- State.json round=N+1 + neuer rounds-Eintrag
- Schema-allOf-Pflichten erfüllt für Round-Type

## Anti-Pattern

- NICHT ohne references[] schreiben (Schema-Pflicht ≥1)
- NICHT type=execute ohne acceptance_criteria + rollback_triggers + wallclock-min
- NICHT type=decision-lock ohne --decided-by
- NICHT in Phase=init oder close (Phase-Inkompatibilität)

## Cross-Refs

- ADR_0029 §4.2 Round-Type-Tabelle
- ADR_0029 §4.3 Handover-Frontmatter-Schema
- ADR_0029 §5 Lifecycle
- ADR_0029 §13.2 Concurrency
