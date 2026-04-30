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
5. Type-spezifische Pflicht-Args-Validation (NEU v0.1.3, hard-enforce, F-RP-32 / D-002):
   - type=execute: `--acceptance` + `--rollback` + `--wallclock-min` Pflicht
   - type=decision-lock: `--decided-by` Pflicht
   - type=pre-patch: `--acceptance` + `--wallclock-min` Pflicht
   - type=execute / pre-patch: `--acceptance` muss valid JSON-Array sein
   - Bei missing → ABBRUCH mit Type-spezifischer Diagnose: "Pre-Flight FAIL Punkt 5 — required-Arg `<name>` missing for type=`<type>`. Skill-Spec verlangt hard-enforce v0.1.3+ (F-RP-32). Bitte mit vollständigen Args erneut aufrufen."
   - Re-Sync-Sub-Typ-Marker (nur bei type=re-sync): Body MUSS `resync_sub_type`-Marker enthalten (`plan-layer` | `execution-layer` | `hybrid`). Bei `execution-layer`/`hybrid`: ≥1 reference type=evidence Pflicht. Bei missing → WARN "Re-Sync-Sub-Typ-Konfusion-Verdacht (F-RP-29)".
6. Konvergenz-Kriterium-Skip-Check (NEU v0.1.3 / D-005 Sub-B):
   Wenn vorherige Round (N-1) Konvergenz-Kriterium definiert hat und diese Round (N) das Kriterium übersprungen hat:
   - Body MUSS `status_observations[]` mit `type=convergence_criterion_skip` enthalten
   - Bei missing → WARN "Konvergenz-Bypass ohne Markierung — AP-08-Verdacht"

## §forward-pointer-rationale (Affordance-Documented, NEU v0.1.3 / D-003 F-RP-33)

decision-lock-Round darf rationale-File pointer enthalten der zum
Schreib-Zeitpunkt noch nicht existiert. Pflicht-Markierung im state.json:

```yaml
shared_artifacts:
  - path: bridge/artifacts/<file>.md
    owner: <role>
    status: pre-allocated   # NICHT active
    round_allocated: <N>    # decision-lock-Round
    purpose: "<beschreibung>"
```

Folge-Round (typischerweise N+1) materialisiert File und setzt:

```yaml
status: active
round_active: <N+1>
```

**Rationale:** entkoppelt formale decision-lock von substantieller
Artefakt-Materialisierung, verhindert Block-Schleife bei async-Schreiben.

**Anti-Pattern:** pre-allocated-Status ohne Materialisierungs-Plan in
Folge-Rounds = Forward-Pointer-Drift. Nach 3 Rounds ohne active-Status
WARN-Markierung in bridge-status (siehe bridge-status.md §forward-pointer-warning).

**Empirische Validierung:** bridge-pair p3-real-user R11 worker-decision-lock
mit pre-allocated annex; R12 advisor-Materialisierung mit status active.

## §konvergenz-skip-rationale (Affordance-Documented, NEU v0.1.3 / D-005 Sub-B F-RP-34)

Konvergenz-Kriterium aus eigener Pair-Round darf in nachfolgender Round
übersprungen werden, wenn Substanz-Konvergenz bilateral schon erreicht ist
(z.B. via Plan-Layer-Akzeptanz aus früherer Round).

**Pflicht-Markierung:** Skip-Round Body enthält `status_observations[]`-Eintrag:

```yaml
status_observations:
  - type: convergence_criterion_skip
    defined_in_round: <N>      # Round, die Kriterium definiert hat
    skipped_in_round: <M>      # diese Round
    skip_basis: "<Begründung — z.B. bilaterale Substanz-Konvergenz>"
    cycle_counter: <Anzahl Cycles seit Definition>
```

**Anti-Pattern:**
- Skip ohne Markierung = AP-08-Bypass-Verdacht (Konsens-Inszenierung)
- Skip-mit-Markierung = legitime Affordance

**Empirische Validierung:** bridge-pair p3-real-user R11 (Worker-Self-Bypass
eigener R8-Konvergenz-Kriterium-Definition).

## §Re-Sync-Sub-Typen (NEU v0.1.3 / D-001 Worker-Pos)

`/bridge-handover --type=re-sync` differenziert zwei Sub-Typen via Body-Marker
und Pre-Flight-Pflicht:

### plan-layer-resync

**Inhalt:** Erwartung, Hypothesen, Plan über advisor-side / worker-side-Status.
**Pre-Flight-Pflicht:** keine zusätzliche.
**Pflicht-Body-Marker:**
```yaml
resync_sub_type: plan-layer
```

### execution-layer-resync

**Inhalt:** Verifikation tatsächlicher persistierter State, Round-Counter,
shared-path-Inhalte.
**Pre-Flight-Pflicht (NEU v0.1.3):** ≥1 reference muss `type=evidence` sein
mit advisor-side/worker-side-Pointer (z.B. via `mcp__session_info__read_transcript`
oder Filesystem-State-Pointer).
**Pflicht-Body-Marker:**
```yaml
resync_sub_type: execution-layer
evidence_pointers:
  - type: filesystem-state
    pointer: bridge/state.json#current_round
    verified_at: <ISO-timestamp>
```

### hybrid

**Inhalt:** beide Layer im selben Body.
**Pflicht-Body-Marker:**
```yaml
resync_sub_type: hybrid
```
Plus execution-layer-Pflicht erfüllt + plan-layer-Markierung im Body.

**Anti-Pattern:** re-sync ohne `resync_sub_type`-Marker = Layer-Konfusions-
Verdacht (F-RP-29). Pre-Flight 5 (NEU): WARN bei missing Marker.

## §Output-Marker (NEU v0.1.3, F-RP-29 Korrektiv / D-001 Advisor-Pos)

Skill darf NICHT erfolgreich-Output produzieren ohne folgenden Block:

```
============================================================
BRIDGE-WRITE COMPLETED — Round <n>
============================================================
artifact:           bridge/handover/<n>-<from>-<to>-<hash>.md
state.updated_at:   <timestamp>
state.current_round: <n>
phase:              <phase>
============================================================
```

Block referenziert verifizierbare Filesystem-Pointer. User sieht direkt
ob Bridge-Write erfolgte. Bei Skill-FAIL: NICHT diesen Block ausgeben,
sondern explicit FAIL-Diagnose.

## §Required-Args-Hard-Enforcement (NEU v0.1.3 / D-002 F-RP-32)

Required-Args werden in Pre-Flight 5 hard-enforced. Elicitation-Fallback ist
sekundär für optional-Args oder strukturierte Eingabe (z.B. JSON-Arrays für
acceptance_criteria), NICHT für missing required.

Begründung: Plugin-Robustheit-Garantie unabhängig von Modell-Verhalten
(F-RP-32 Mapping-Decision D-002 PATCH).

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

# NEU v0.1.4 (F-RP-26 Auto-Propagation): worker.phase auto-update aus Worker-Frontmatter
if this_role == "worker":
    state.roles.worker.phase = frontmatter.get("worker_phase")  # Pflicht-Feld im handover-Schema

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

## §worker.phase-Auto-Propagation (NEU v0.1.4 / F-RP-26)

Bei type ∈ {alle Round-Types} und this_role=worker: state.roles.worker.phase wird automatisch aus handover-Frontmatter `worker_phase`-Pflichtfeld auf state.json propagiert. Verhindert worker.phase-Stagnation (F-RP-26 Beobachtung in p3-real-user: phase=kickoff durch 28 Rounds unveraendert trotz Phase-Transitions).

**Empirie-Anker:** p3-real-user R1-R28 — worker.phase blieb "kickoff" obwohl Worker-self-reported sub-phases (mapping, scope-lock-counter, etc.) im Frontmatter standen. Auto-Propagation behebt diese State-Inkonsistenz.

**Self-Test T29:** Worker-Handover mit worker_phase="X" → state.roles.worker.phase=="X" post-Skill.

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
