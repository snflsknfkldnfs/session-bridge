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
4. **State.roles[<role>].session_id == "pending-attach"** (Sentinel-Check, REVIDIERT v0.1.3 strict / D-004 F-RP-23) — eigene Rolle ist Pending-Stub aus init-Phase, NICHT bereits attached. Bei Mismatch (z.B. direkter session_id-Pin aus v0.1.2-Pre-v0.1.3): FAIL. Diagnose: "Pre-Flight 4 FAIL — expected 'pending-attach', found '<X>'. Möglicher v0.1.2-Use-Case mit deprecated --worker-session-id-Pin. Empfehlung: state.json patch (session_id zurück auf 'pending-attach') und Re-attach. Siehe v0.1.3 Migration-Doku." KEIN auto-recover-Branch.
5. **Pflicht-Args-Validation (NEU v0.1.3, hard-enforce / D-002 F-RP-32):**
   - `--worker-focus` muss gesetzt sein (wenn role=worker)
   - `--expertise-source` muss gesetzt sein (wenn role=advisor)
   - Bei missing → ABBRUCH mit User-Question (NICHT Elicitation-Form-Fallback)
   - Diagnose-Output: "Pre-Flight FAIL Punkt 5 — required-Arg `<name>` missing. Skill-Spec verlangt hard-enforce v0.1.3+ (F-RP-32). Bitte mit vollständigen Args erneut aufrufen."
6. State.roles[<other-role>].session_id != this_session_id (kein Self-Attach)
7. State.roles[<other-role>].session_id != "pending-attach" (andere Rolle muss bereits gefüllt sein durch init)

Bei FAIL: ABBRUCH + Diagnose.

## §Required-Args-Hard-Enforcement (NEU v0.1.3 / D-002 F-RP-32)

Required-Args werden in Pre-Flight 5 hard-enforced. Elicitation-Fallback ist
sekundär für optional-Args, NICHT für missing required.

Begründung: Plugin-Robustheit-Garantie unabhängig von Modell-Verhalten
(F-RP-32 Mapping-Decision D-002 PATCH).

**Hinweis:** bridge-init Pre-Flight 5 (Profile-Validation) ist Vorbild für
hard-enforce-Logik. Keine Elicitation-Form-Fallback bei missing required.
Plugin-Robustheit darf nicht von Modell-Quality abhängen (F-RP-24
Marketplace-Adoption-Argument).

## Ablauf

```python
# 1. State-Read + Schema-Validate
state = read_state(shared_path)
validate(state, bridge_state_v1_schema)

# 2. Pre-Flight-Checks (siehe oben — pending-attach-Sentinel-Check P-RP-08)
assert_preflight(state, pair_id, role)

# 3. Eigene Rolle eintragen — REPLACE pending-attach-Sentinel mit echten Werten
SENTINEL_PENDING = "pending-attach"
assert state["roles"][role]["session_id"] == SENTINEL_PENDING, \
    f"Pre-Flight 4 broken: erwartet pending-attach, gefunden {state['roles'][role]['session_id']}"

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

- State.roles[role].session_id == this_session_id (NICHT mehr "pending-attach")
- State.roles[<other-role>].session_id != "pending-attach" (Initiator hat echte Session-ID)
- State.phase == "scope-lock"
- Schema-Validate PASS post-attach

## Anti-Pattern

- NICHT mit gleicher session_id attachen (Self-Attach Pre-Flight 5)
- NICHT attachen wenn beide Rollen schon gefüllt (kein pending-attach mehr → Pre-Flight 4 FAIL)
- NICHT attachen wenn pair_id ≠ state.pair_id (Pre-Flight 2 FAIL)
- NICHT bridge-attach in Initiator-Session aufrufen — diese Session hat ihre Rolle bereits via /bridge-init gesetzt
- NICHT pending-attach-Sentinel-Replacement überspringen — sonst wird state.json ungültig (Sentinel als reale session_id-Antwort)

## Cross-Refs

- ADR_0029 §5.1 Lifecycle init-Phase
- ADR_0029 §5.2 scope-lock Phase
- v0.1.3-Patch-Pipeline D-002 F-RP-32 hard-enforce required-Args
- v0.1.3-Patch-Pipeline D-004 F-RP-23 Sentinel-Invariante (Migration-Hinweis im CHANGELOG)
