---
description: Initialisiert ein neues session-bridge Pair als Initiator-Session (rolle wählbar advisor|worker). Generiert pair_id (UUIDv4), legt bridge/state.json an, schreibt eigene Rolle. Andere Session muss anschließend /bridge-attach <pair_id> ausführen.
argument-hint: --role=<advisor|worker> --topic="<string>" [--shared-path=<absolute-path>] [--expertise-source="<string>"] [--worker-focus="<string>"]
---

# /bridge-init

Initialisiert neuen Session-Bridge-Pair.

## Argumente

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--role=<advisor\|worker>` | ja | Rolle dieser Session im Pair |
| `--topic="<string>"` | ja | Bridge-Topic (z.B. "plugin-migration-variante-c") |
| `--shared-path=<absolute-path>` | nein | Pfad zum gemeinsam mountbaren Verzeichnis. Default: aktuelles Working-Dir des Cowork-Project. |
| `--expertise-source="<string>"` | nur wenn role=advisor | z.B. "escape-game-generator P.1+P.2" |
| `--worker-focus="<string>"` | nur wenn role=worker | z.B. "phase-1.6 implementation" |

## Pre-Flight (PFLICHT, ADR_0029 OQ-6)

1. `<shared-path>/bridge/` ist beschreibbar (test: `mkdir -p <shared-path>/bridge && touch <shared-path>/bridge/.write-test && rm <shared-path>/bridge/.write-test`)
2. `<shared-path>/bridge/state.json` existiert NICHT (sonst Konflikt mit bestehendem Pair)
3. `python3 -c "import jsonschema"` PASS (oder graceful_degrade=True merken)
4. `mcp__session_info__list_sessions` callable (für Status-Verifikation in advisor-Rolle relevant)

Bei FAIL: ABBRUCH + Diagnose ausgeben.

## Ablauf

```python
# 1. UUID generieren
pair_id = str(uuid.uuid4())

# 2. State-Skeleton bauen
state = {
    "pair_id": pair_id,
    "schema_version": "1.0.0",
    "created_at": now_iso(),
    "updated_at": now_iso(),
    "phase": "init",
    "roles": {
        "advisor": {} if role == "worker" else {
            "session_id": this_session_id,
            "expertise_source": expertise_source,
            "active_since": now_iso()
        },
        "worker": {} if role == "advisor" else {
            "session_id": this_session_id,
            "current_focus": worker_focus,
            "phase": worker_phase,
            "active_since": now_iso()
        }
    },
    "topic": topic,
    "current_round": 0,
    "rounds": [],
    "open_blockers": [],
    "decision_log": [],
    "status_observations": [],
    "file_ownership": {},
    "shared_artifacts": [],
    "wallclock_estimates": [],
    "rollback_plan_path": None
}

# 3. Schema-Validate (M1' Akzeptanz)
validate(state, bridge_state_v1_schema)

# 4. Atomic-Write
write_atomic(f"{shared_path}/bridge/state.json", state)

# 5. mkdir bridge/handover/, bridge/artifacts/, bridge/orphans/
ensure_dirs([
    f"{shared_path}/bridge/handover",
    f"{shared_path}/bridge/artifacts",
    f"{shared_path}/bridge/orphans"
])

# 6. Output an User
print(f"""
Bridge-Pair initialisiert.

  pair_id:      {pair_id}
  role (this):  {role}
  topic:        {topic}
  shared-path:  {shared_path}
  phase:        init

Nächster Schritt: andere Session muss
  /bridge-attach {pair_id} --role={"worker" if role=="advisor" else "advisor"} --shared-path={shared_path}
ausführen.
""")
```

## Akzeptanz

- `bridge/state.json` existiert + jsonschema-validate PASS
- `bridge/handover/`, `bridge/artifacts/`, `bridge/orphans/` existieren
- pair_id im Output angezeigt
- Phase = `init`

## Anti-Pattern

- NICHT init aufrufen wenn bereits state.json existiert (würde überschreiben)
- NICHT ohne `--topic` initialisieren (Schema-Pflicht)

## Cross-Refs

- ADR_0029 §5.1 Lifecycle init-Phase
- ADR_0029 §13.2 Concurrency Atomic-Write
