---
description: Attached die zweite Session an einen bestehenden Bridge-Pair (von Initiator-Session per /bridge-init angelegt). Ergänzt die fehlende Rolle in bridge/state.json, setzt phase auf scope-lock. Erfordert pair_id + Rollen-Wahl.
argument-hint: <pair_id> --role=<advisor|worker> [--shared-path=<absolute-path>] [--expertise-source="<string>"] [--worker-focus="<string>"]
---

# /bridge-attach

Attaches diese Session als zweite Rolle zu einem bestehenden Bridge-Pair.

## Argumente

| Pos / Flag | Pflicht | Beschreibung |
|---|---|---|
| `<pair_id>` (positional) | ja | UUIDv4 aus `/bridge-init`-Output |
| `--role=<advisor\|worker>` | ja | Rolle dieser Session (Komplement zur Initiator-Rolle) |
| `--shared-path=<absolute-path>` | nein | Default: aktuelles Working-Dir |
| `--expertise-source="<string>"` | wenn role=advisor | analog /bridge-init |
| `--worker-focus="<string>"` | wenn role=worker | analog /bridge-init |

## Pre-Flight

1. `<shared-path>/bridge/state.json` existiert
2. State.pair_id == argument.pair_id
3. State.phase == "init"
4. State.roles[<role>] ist leer / not yet attached
5. State.roles[<other-role>].session_id != this_session_id (kein Self-Attach)

Bei FAIL: ABBRUCH + Diagnose.

## Ablauf

```python
# 1. State-Read + Schema-Validate
state = read_state(shared_path)
validate(state, bridge_state_v1_schema)

# 2. Pre-Flight-Checks (siehe oben)
assert_preflight(state, pair_id, role)

# 3. Eigene Rolle eintragen
state["roles"][role] = {
    "session_id": this_session_id,
    "active_since": now_iso(),
    **{"expertise_source": expertise_source} if role == "advisor" else {},
    **{"current_focus": worker_focus, "phase": worker_phase} if role == "worker" else {}
}

# 4. Phase-Übergang init → scope-lock
state["phase"] = "scope-lock"
state["updated_at"] = now_iso()

# 5. CAS-Write
write_atomic_cas(state)

# 6. Output an User
print(f"""
An Bridge-Pair angeschlossen.

  pair_id: {pair_id}
  role:    {role}
  phase:   scope-lock

Nächster Schritt: beide Sessions schreiben Status-Snapshot via
  /bridge-handover --type=status

Anschließend (advisor-Session): erste initial-advice via
  /bridge-handover --type=initial-advice
""")
```

## Akzeptanz

- State.roles[role].session_id == this_session_id
- State.phase == "scope-lock"
- Schema-Validate PASS

## Anti-Pattern

- NICHT mit gleicher session_id attachen (Self-Attach)
- NICHT attachen wenn beide Rollen schon gefüllt
- NICHT attachen wenn pair_id ≠ state.pair_id

## Cross-Refs

- ADR_0029 §5.1 Lifecycle init-Phase
- ADR_0029 §5.2 scope-lock Phase
