---
description: Zeigt den aktuellen State eines session-bridge Pairs — Phase, Rollen, current_round, letzte 3 Handovers, offene Blocker, decision_log, drift_factors. Read-only, schreibt nicht in state.json.
argument-hint: '[--shared-path=<absolute-path>] [--verbose]'
---

# /bridge-status

Read-only Statusbericht über den aktuellen Bridge-Pair-Zustand.

## Argumente

| Flag | Beschreibung |
|---|---|
| `--shared-path=<absolute-path>` | Default: aktuelles Working-Dir |
| `--verbose` | Zeigt vollen rounds[]-History statt nur letzte 3 |

## Pre-Flight

1. `<shared-path>/bridge/state.json` existiert
2. Schema-Validate PASS (sonst Warning, dann raw output)

## Ablauf (NEU v0.1.3 / F-RP-31 CRITICAL)

```python
# 1. State-Read
state = read_state(shared_path)

# 2. Eigene Rolle bestimmen
this_role = "advisor" if state.roles.advisor.session_id == this_session_id else "worker"
other_role = "worker" if this_role == "advisor" else "advisor"

# 3. Other-Session-Title via session_info MCP (graceful_degrade falls FAIL)
try:
    other_session_info = session_info.get(state.roles[other_role].session_id)
    other_title = other_session_info.title
    other_status = other_session_info.status  # running | idle
    other_last_activity = other_session_info.last_activity_min_ago
except:
    other_title = "(unbekannt)"
    other_status = "(degraded)"
    other_last_activity = None

# 4. Letzte 3 Rounds + Phase + Decision-Log + Blocker
last_rounds = state.rounds[-3:]
phase = state.phase
decision_count = len(state.decision_log)
open_blockers = state.open_blockers

# 5. Nächste erwartete Aktion inferieren aus letzter Round + Phase
next_action = infer_next_action(state, this_role)

# 6. Forward-Pointer-Drift-Check (NEU v0.1.3 §forward-pointer-warning)
# pre-allocated shared_artifacts ohne active-Status seit ≥3 Rounds → WARN
forward_pointer_warnings = [
    a for a in state.shared_artifacts
    if a.get("status") == "pre-allocated"
    and (state.current_round - a.get("round_allocated", state.current_round)) >= 3
]

# 7. Format Output
print_status_block(this_role, other_role, other_title, other_status,
                   other_last_activity, last_rounds, phase, decision_count,
                   open_blockers, next_action, forward_pointer_warnings)
```

## Output-Format (NEU v0.1.3 / F-RP-31)

```
============================================================
BRIDGE-PAIR <pair_id> — Phase: <phase>
============================================================
Diese Session:    <role> (<title>)
Andere Session:   <other-role> (<other-title>)
                  Status: <running|idle> · Last activity: <X min ago>

Letzte 3 Rounds:
  R<n> [<type>]   <from>→<to>   <timestamp>   <bytes>
  R<n-1> [<type>] <from>→<to>   <timestamp>
  R<n-2> [<type>] <from>→<to>   <timestamp>

Decision-Log: <count> Decisions locked
Open Blockers: <count> (siehe state.open_blockers)

Nächste erwartete Aktion (this session):
  <inferred-action-text>

Mögliche Skill-Calls:
  /bridge-handover --type=<a|b|c>
  /bridge-close (wenn Pair-Lifecycle-Ende erreicht)
============================================================
```

## §forward-pointer-warning (NEU v0.1.3 / D-003)

Wenn `shared_artifacts[]` Einträge mit `status: pre-allocated` und
`round_allocated <= current_round - 3` vorliegen:

```
WARNUNG: Forward-Pointer-Drift erkannt.
  artifact: bridge/artifacts/<file>.md
  round_allocated: <N>  (current: <N+3+>)
Folge-Round-Materialisierung mit status=active fehlt.
Siehe bridge-handover.md §forward-pointer-rationale.
```

## Polling-Hint (NEU v0.1.3 per F-RP-31 Patch 3)

Wenn `other_last_activity_min_ago > 30`:
```
HINWEIS: Other session inactive für >30 min.
Möglicherweise in Plan-Phase (siehe F-RP-29).
Erwäge Polling oder Worker-Probe-Round.
```

## Output (Beispiel)

```
Bridge-Pair 7c4f1d2e-5a8b-4c9d-9e0f-1a2b3c4d5e6f
  topic:         plugin-migration-variante-c
  phase:         iterate
  current_round: 7
  created_at:    2026-04-26T09:00:00Z
  updated_at:    2026-04-26T15:30:42Z

Rollen:
  advisor: local_a1b2c3 (escape-game-generator P.1+P.2)
  worker:  local_d4e5f6 (focus: plugin-migration, phase: phase-1.6)

Letzte 3 Rounds:
  #5 [counter]      worker→advisor (2026-04-26T14:10:22Z)
  #6 [re-sync]      advisor→worker (2026-04-26T14:45:10Z)
  #7 [decision-lock] advisor→worker (2026-04-26T15:30:42Z)

Offene Blocker:
  B-2 [medium] GH-Visibility public/private (raised in round 7 by advisor)

Decision-Log:
  R#7: Variante C gewählt (by user)

Wall-Clock-Drift (avg): 0.87x (3 samples)
```

## Akzeptanz

- Read-only, schreibt KEINE Files
- Output strukturiert, lesbar
- Bei Schema-Validate-Fail: Warning + raw output
- (NEU v0.1.3) Output enthält: Diese Session-Rolle, Other-Session-Title, Other-Last-Activity, letzte 3 Rounds, nächste erwartete Aktion, Forward-Pointer-Warnings (falls applicable)
- (NEU v0.1.3) Bei other-session-inactive > 30 min: Polling-Hint im Output

## Cross-Refs

- ADR_0029 §4.1 State-Schema
- v0.1.3-Patch-Pipeline F-RP-31 (User-Lifecycle-Visibility CRITICAL)
- v0.1.3-Patch-Pipeline D-003 F-RP-33 (forward-pointer-rationale)
