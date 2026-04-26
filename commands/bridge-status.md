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

## Ablauf

```python
state = read_state(shared_path)

# Aktuelle Übersicht
print(f"""
Bridge-Pair {state.pair_id}
  topic:         {state.topic}
  phase:         {state.phase}
  current_round: {state.current_round}
  created_at:    {state.created_at}
  updated_at:    {state.updated_at}

Rollen:
  advisor: {state.roles.advisor.session_id} ({state.roles.advisor.expertise_source})
  worker:  {state.roles.worker.session_id} (focus: {state.roles.worker.current_focus}, phase: {state.roles.worker.phase})

Letzte 3 Rounds:
""")

for r in state.rounds[-3:]:
    print(f"  #{r.round} [{r.type}] {r.initiator}→{other_role(r.initiator)} ({r.timestamp})")

# Offene Blocker
if state.open_blockers:
    print("\nOffene Blocker:")
    for b in state.open_blockers:
        print(f"  {b.id} [{b.severity}] {b.summary} (raised in round {b.raised_in_round} by {b.raised_by})")
else:
    print("\nKeine offenen Blocker.")

# Decision-Log
if state.decision_log:
    print("\nDecision-Log:")
    for d in state.decision_log:
        print(f"  R#{d.round}: {d.decision} (by {d.decided_by})")

# Wall-Clock-Drift (nur falls actual_min != null)
drifts = [we for we in state.wallclock_estimates if we.actual_min is not None]
if drifts:
    avg_drift = sum(d.drift_factor for d in drifts) / len(drifts)
    print(f"\nWall-Clock-Drift (avg): {avg_drift:.2f}x ({len(drifts)} samples)")

# Shared-Artifacts
active = [a for a in state.shared_artifacts if a.lifecycle_state == "active"]
if active:
    print(f"\nAktive Shared-Artifacts ({len(active)}):")
    for a in active[:5]:
        print(f"  {a.path} — {a.purpose}")
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

## Cross-Refs

- ADR_0029 §4.1 State-Schema
