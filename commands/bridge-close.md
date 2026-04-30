---
description: Schließt einen session-bridge Pair. Setzt phase=close, schreibt Bilanz-Datei, archiviert alle nicht-active shared_artifacts, kalibriert wallclock_estimates (drift_factor post-hoc). Schreib-Operation ist final, keine weiteren Handovers mehr möglich.
argument-hint: --bilanz=<path> [--shared-path=<absolute-path>] [--archive-orphans]
---

# /bridge-close

Schließt einen Bridge-Pair und persistiert Bilanz.

## Argumente

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--bilanz=<path>` | ja | Pfad zur Bilanz-Markdown-Datei (relativ zu `<shared-path>/bridge/`) |
| `--shared-path=<absolute-path>` | nein | Default: aktuelles Working-Dir |
| `--archive-orphans` | nein | Verschiebt orphane handover-Files (nicht in rounds[]) nach `bridge/orphans/` |

## Pre-Flight

1. `bridge/state.json` existiert + Schema-Validate PASS
2. State.phase ∈ {iterate, execute, verify} (init kann nicht direkt geschlossen werden, scope-lock auch nicht — erst nach mind. 1 Round)
3. Mind. 1 Round in state.rounds[] (sonst trivialer Pair)
4. `<bilanz-path>` existiert nicht oder leer (kein Overwrite)

## Ablauf

```python
state = read_state(shared_path)
read_at = state["updated_at"]

# 1. Wallclock-Drift-Kalibrierung (D4)
for we in state.wallclock_estimates:
    if we.actual_min is None:
        # User-Prompt: actual Wall-Clock für Round we.round abfragen
        actual = prompt_user(f"Actual Wall-Clock für Round #{we.round} (Min)?")
        we.actual_min = actual
        we.drift_factor = actual / we.estimated_min if we.estimated_min > 0 else None

# 2. Shared-Artifact-Lifecycle (D5)
for a in state.shared_artifacts:
    if a.lifecycle_state == "active":
        # User-Prompt: bleibt active oder archive?
        keep_active = prompt_user(f"Artifact {a.path}: bleibt active? (y/n)")
        if not keep_active:
            a.lifecycle_state = "archived"

# 3. Orphan-Handover-Archivierung (optional)
if args.archive_orphans:
    handover_files = list_files("bridge/handover/*.md")
    rounds_paths = [r.artifact_path for r in state.rounds]
    orphans = [f for f in handover_files if f not in rounds_paths]
    for orphan in orphans:
        move(orphan, f"bridge/orphans/{basename(orphan)}")

# 4. Bilanz-Datei schreiben
bilanz = generate_bilanz_markdown(state)
write(f"bridge/{args.bilanz}", bilanz)

# 5. State final
state.phase = "close"
state.updated_at = now_iso()

write_atomic_cas(state, expected_updated_at=read_at)

# 6. Output
print(f"""
Bridge-Pair {state.pair_id} geschlossen.

  Phase:                close
  Total Rounds:         {len(state.rounds)}
  Decisions:            {len(state.decision_log)}
  Wall-Clock-Drift Avg: {avg_drift:.2f}x
  Bilanz:               bridge/{args.bilanz}
  Orphans archiviert:   {len(orphans) if args.archive_orphans else 0}

Pair ist geschlossen. Weitere /bridge-handover-Aufrufe sind blockiert.
""")
```

## Bilanz-Datei-Format

```markdown
# Bridge-Pair-Bilanz: <topic>

**Pair-ID:** <uuid>
**Phase-Sequenz:** init → scope-lock → iterate → execute → verify → close
**Total Rounds:** <N>
**Total Decisions:** <M>

## Round-Verlauf
<table mit allen rounds>

## Decision-Log
<alle decisions>

## Wall-Clock-Bilanz
| Round | Estimated | Actual | Drift |
|---|---|---|---|
| ... | ... | ... | ... |

**Average Drift:** <X.YY>x

## Lessons-Learned
<freitext, optional User-Input>

## Geschlossene Blocker
<alle initially raised blockers>

## Shared-Artifacts Final-Lifecycle
<table>
```

## Akzeptanz

- State.phase == "close"
- Bilanz-Datei existiert
- Wall-Clock-Drift kalibriert (alle wallclock_estimates haben actual_min ≠ null oder explizit null=skipped)
- Orphane handovers archiviert (falls --archive-orphans)

## §bilanz-schema-enforcement (NEU v0.1.5 Phase H / PB-001 follow-up / ADR_0031 §4.3)

bridge-close MUSS generierte Bilanz gegen `schemas/bilanz_v1.json` (NEU v0.1.4 PB-001) validieren.

```python
from tools.bridge_state import validate_bilanz_against_schema

errors = validate_bilanz_against_schema(bilanz_data)
if errors:
    abort(f"Bilanz-Schema-Validate FAIL: {errors}")
```

**Filename-Konvention (ADR_0029 Annex B v0.1.5 Phase I):** `bridge/bilanz_<pair_id>.md`

**Migration-Kandidaten:**
- p4-eg-dev/bridge/BILANZ.md → soft-Migration (User-Aktion optional, kein hard-FAIL fuer historische Pairs pre-v0.1.5)
- pre-v0.1.5 Bilanz-Files bleiben ohne Schema-Enforcement

**Empirie-Anker:** pilot-runs/p3-real-user/bridge/bilanz_8cbeaad0.md als Reference-Implementation (12-Sektionen-konform, Stufe-7-Konsolidierung).

## Anti-Pattern

- NICHT close in Phase=init (kein Round geschehen)
- NICHT close ohne Bilanz-Datei
- NICHT mehrfach close (idempotent? — NEIN: zweiter close erkennt Phase=close + ABBRUCH)

## Cross-Refs

- ADR_0029 §5.6 close-Phase
- ADR_0029 §6.4 Wall-Clock-Drift
