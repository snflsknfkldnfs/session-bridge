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

# 4.5 NEU v0.1.10: Memory-Symmetrie-Plan generieren (Pattern-#103)
memory_plan = generate_memory_symmetry_plan(state)
state["memory_symmetry_status"] = "pending"  # pending|partial|complete
prompt_user_for_memory_persist(memory_plan)

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

## §Memory-Symmetrie-Pflicht-Workflow (NEU v0.1.10 / Pattern-#103, CRITICAL)

**Empirie:** 4 Pairs (p6/p7-klafki/p10/p11) hatten alle Memory-Symmetrie als Out-of-Bridge-Task. Aktuell ist Memory-Persistierung User-Selbst-Disziplin → asymmetrische Wissens-Lücken bei Cross-Pair-Coordination.

### Memory-Plan-Generierung (Schritt 4.5)

bridge-close generiert vor `phase=close` einen **Memory-Symmetrie-Plan** für beide Sessions:

**Quelle für Memory-Items:**
- §Pattern-Inventar-Updates aus BILANZ
- §Decision-Log-Items mit hoher Tragweite (>= "hoch")
- §Out-of-Bridge-Tasks
- §Lessons-Learned-Items
- §Cross-Pair-Anker

**Item-Klassifikation:**

| Type | advisor-Memory | worker-Memory |
|---|---|---|
| **feedback** (Methodik, Lehren) | Cross-Session-Beratungs-Pattern, Audit-Methodik, Profile-Anwendung | Operative-Patterns, Drift-Empirie, Workflow-Erfahrung |
| **project** (was-getan, was-locked) | Snapshot-Anker (was wurde wann locked) | DONE-State, Backlog-Inventar |
| **reference** (Cross-Pair-Anker) | Cross-Pair-Pointer auf Predecessor-/Successor-Pairs | Pattern-Inventar-Pointer |
| **user** (User-Profile) | User-Vorlieben aus Pair-Verlauf | (selten worker-side) |

**Symmetrie ≠ identische Items.** Komplementär:
- advisor speichert **wie man berät** (Methodik)
- worker speichert **was funktioniert hat** (Operative-Empirie)
- Beide speichern **was wurde gemacht** (Project-Snapshot) + **Cross-Pair-Pointer**

**Typische Item-Anzahl:** 2-4 advisor-Items + 2-4 worker-Items.

### Memory-Plan-Block in BILANZ.md

bridge-close schreibt §Memory-Symmetrie-Plan-Sektion in die generierte BILANZ:

```markdown
## §Memory-Symmetrie-Plan (Pattern-#103, v0.1.10-Pflicht)

### Advisor-Memory (Pflicht post-Closure in advisor-Session):

- **Item:** <name>.md
  - **Type:** feedback | project | reference | user
  - **Description:** <one-liner>
  - **Body-Skizze:** <was wird gespeichert>

- **Item:** ...

### Worker-Memory (Pflicht post-Closure parallel in worker-Session):

- **Item:** <name>.md
  - **Type:** ...
  - **Description:** ...
  - **Body-Skizze:** ...

### Persistierungs-Aktion (User in beiden Sessions):

1. In dieser <role>-Session: Memory-Items akzeptieren
2. In <other-role>-Session (Title <X>): parallel Memory-Items akzeptieren
3. Memory-Symmetrie-Status: pending → complete

### Cross-Project-Memory-Marker (NEU bei domain-hint=cross-project)

Bei Cross-Project-Bridges: Memory-Items in beiden Sessions tragen Cross-Project-Coordination-Marker:
- Source-Project: <name>
- Target-Project: <name>
- Cross-Bridge-Pair-ID: <pair_id>
```

### state.json Tracking

bridge-close setzt `state.memory_symmetry_status`:
- `pending`: Plan generiert, noch nicht persistiert
- `partial`: nur eine Session hat Memory persistiert
- `complete`: beide Sessions haben persistiert (User-bestätigt im next /bridge-init oder via /bridge-status)

**Nicht hard-erzwingbar** — Plugin operiert nur in einer Session zur Zeit. Schema-Field hilft beim Tracking + Pre-Init-WARN.

### Pre-Init-WARN bei nächstem Pair (NEU v0.1.10)

Wenn /bridge-init startet während ein vorheriger Pair (gleiche advisor- oder worker-Session) `memory_symmetry_status != complete` hatte:

```
WARN: Vorheriger Pair <pair_id_old> hat memory_symmetry_status=<status>.
Memory-Items aus letztem Pair sind nicht in beiden Sessions persistiert.
Empfehlung: Memory-Items aus bridge/bilanz_<pair_id_old>.md §Memory-Symmetrie-Plan akzeptieren VOR dem neuen Pair-Init.
```

WARN nicht hard-blockierend — User kann override.

### Bilanz-Schema-Erweiterung (additive)

`schemas/bilanz_v1.json` bekommt optional `memory_symmetry_plan`-Field:

```yaml
memory_symmetry_plan:
  advisor_items:
    - {name: "...", type: "feedback|project|reference|user", description: "..."}
  worker_items:
    - {name: "...", type: "...", description: "..."}
  persistence_status: pending|partial|complete
  cross_project_marker: {source_project: "...", target_project: "..."}  # nur bei domain-hint=cross-project
```

### Cross-Refs

- Pattern-#103 in p6-BILANZ.md §3.4 + p7-klafki BILANZ §13 + p10-BILANZ §10 + p11-BILANZ §5
- ADR_0029 Annex D Cross-Pair-Empirie-Konsolidierung (NEU v0.1.10)
- ADR_0030 §3.4 Profile-Loading (Memory-Items mit Profile-Pin-Tracking)

## Anti-Pattern

- NICHT close in Phase=init (kein Round geschehen)
- NICHT close ohne Bilanz-Datei
- NICHT mehrfach close (idempotent? — NEIN: zweiter close erkennt Phase=close + ABBRUCH)

## Cross-Refs

- ADR_0029 §5.6 close-Phase
- ADR_0029 §6.4 Wall-Clock-Drift
