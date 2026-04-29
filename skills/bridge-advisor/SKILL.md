---
name: bridge-advisor
description: Cross-Session Advisor — liest Worker-Session-Transcript via session_info MCP, produziert strukturierte Handover-Artefakte mit Empfehlungen, Patches, Counter-Beratung. Trigger bei "evaluiere session", "berate die andere session", "advisor-handover", "cross-session-eval", "/bridge-handover --type=initial-advice|re-sync|pre-patch", oder wenn ein Pair als advisor-Rolle aktiv ist und User um Beratung bittet.
---

# bridge-advisor — Skill

## Zweck

Diese Session ist `advisor` in einem session-bridge Pair. Sie hat Expertise / Beobachter-Position und produziert strukturierte Handover-Artefakte für die Worker-Session.

**Plugin-Referenz:** ADR_0029 §3.1 Rollen-Modell.

## Vorbedingungen pro Trigger

1. `bridge/state.json` existiert und diese Session ist als `roles.advisor.session_id` eingetragen.
2. session_info MCP verfügbar (sonst degraded mode).
3. Falls `state.roles.advisor.expertise_profile` gesetzt (ADR_0030, schema v1.1.0): Profile-Verzeichnis existiert + alle `required_files` lesbar. Bei FAIL: WARN + degraded-mode (advisor agiert generic, references[].verified=false markieren).

## Pflicht-Output-Header (NEU v0.1.3 / F-RP-31 Patch 4)

Jeder bridge-advisor Skill-Output beginnt mit:

```
[bridge-advisor mode | profile=<profile-name oder "none"> v<version>]
```

Dies erlaubt User klare Mode-Identifikation, verhindert Plan-vs-Execution-Drift-Confusion.

## §Anti-Plan-Drift (NEU v0.1.3, CRITICAL — F-RP-29 / D-001 Advisor-Pos)

bridge-advisor Skill darf NICHT detaillierten Plan-Text als Antwort an User
produzieren ohne nachfolgenden Skill-Aufruf. Empirisch validiert in
bridge-pair p3-real-user (4× Live-Reproduktion advisor-side R6→7, R7→8,
R10→11, R16→17).

**Format-Regel (Pflicht):**

| Plan-Text-Länge | Erlaubt? | Bedingung |
|---|---|---|
| ≤ 5 Sätze | OK | als Plan-Outline + sofortiger Skill-Aufruf |
| > 5 Sätze | NICHT OK | außer als Skill-Body bei tatsächlicher Skill-Invocation |

**Anti-Pattern AP-Plan-vs-Execution-Drift:**

Plan-Text > 5 Sätze ohne Skill-Aufruf = AP-Drift. Konsequenz:
- User interpretiert Plan-Text als Bridge-Write-done
- Worker erwartet Bridge-Artefakt
- F-RP-29 Plan-vs-Execution-Layer-Konfusion entsteht

**Pre-Flight-Erweiterung (NEU v0.1.3):**

Vor advisor-Skill-Output-Persistierung:
- Wenn Body Plan-Text-Pattern enthält ("ich werde", "geplant", "Inhalt der Round",
  "next steps", > 5 Sätze ohne konkrete State-Mutation)
- → WARN "AP-Plan-vs-Execution-Drift-Verdacht. Plan-Text ohne Skill-Aufruf
  reproduziert F-RP-29 (4× live in p3-real-user). Erwäge: kompakter
  Plan-Outline ≤5 Sätze + sofortige Skill-Invocation."

## §User-Translation-Konvention (NEU v0.1.3 / D-001 Advisor-Pos)

Wenn advisor-Session vermittelt zwischen User und Worker-Session via Mensch-
Translator: Konvention für Plan-vs-Done-Distinktion.

**advisor-Output an User darf nicht implizieren "Bridge-Write done" durch:**
- Hohen Detail-Grad ohne Skill-Aufruf-Marker
- Strukturierte Listen ohne `BRIDGE-WRITE COMPLETED`-Block
- Konkrete Ausführungs-Sprache ("ich schreibe", "geplant für Round X")
  ohne nachfolgendes Skill-Invocation

**Konvention für advisor-Output:**

| Modus | Marker am Anfang |
|---|---|
| Plan-Diskussion | `[plan-layer | no-bridge-write]` |
| Skill-Invocation | normal (Skill-Output enthält BRIDGE-WRITE-Block) |
| Status-Bericht ohne Skill | `[status-only | no-bridge-write]` |

User-side erwartet bei Forward an Worker:
- Bei `[plan-layer]`: User sagt "advisor diskutiert Plan, kein Bridge-Write"
- Bei BRIDGE-WRITE-Block: User sagt "advisor hat Round X geschrieben + persistiert"
- Bei `[status-only]`: User sagt "advisor evaluiert, kein Bridge-Write geplant"

## Pflicht-Workflow pro Handover

### Schritt 0 — Profile-Loading (ADR_0030 §3.4, nur wenn expertise_profile gesetzt)

```python
# Pseudocode
profile_path = state["roles"]["advisor"].get("expertise_profile")
if profile_path:
    profile = load_profile(profile_path)
    # profile = {
    #   "frontmatter": {profile_name, methodology_pillars, sources, pflicht_workflows, linkage_to_bridge_rounds, ...},
    #   "diagnostic_frames": [...],   # aus diagnostic-frames.md
    #   "anti_patterns": [...],        # aus anti-patterns.md
    #   "question_bank": {...}         # aus question-bank.md
    # }
    profile_workflow_modifier = profile["frontmatter"]["linkage_to_bridge_rounds"].get(round_type, "")
    pflicht_workflows = profile["frontmatter"]["pflicht_workflows"]
else:
    profile = None
    pflicht_workflows = []
```

Bei Profile-Load-FAIL: WARN, set `degraded_mode = True`, weiter ohne Profile.

### Schritt 1 — Status-Snapshot validieren (D1, FM-1, FM-7)

Worker-Session-Status NICHT annehmen, sondern verifizieren:

```python
# Pseudocode
worker_session_id = state["roles"]["worker"]["session_id"]
transcript = read_transcript(worker_session_id, limit=5)  # session_info MCP
worker_phase_observed = extract_phase_from_transcript(transcript)
worker_focus_observed = extract_focus_from_transcript(transcript)
status_verified_at = now()
```

Wenn session_info nicht verfügbar: setze `references[].verified=false`. Status-Snapshot dann aus jüngster shared_artifact-Lifecycle-Beobachtung ableiten.

### Schritt 2 — References sammeln (D2, FM-3)

Mindestens 1 reference ist Pflicht. Bevorzugte Reihenfolge:

1. `transcript` (frischer als Memory, primär)
2. `filesystem` (shared artifact)
3. `capability-probe` (für faktische Behauptungen wie "tool X installed")
4. `memory` (Tiebreaker, NUR wenn explizit + jünger als 7 Tage)
5. `shared-artifact` (cross-Pair-Referenz)
6. `expertise-profile` (NEU v1.1.0, ADR_0030): Frame/Anti-Pattern/Quote aus geladenem Profile als methodische Referenz. Format: `pointer: "<profile_path>:<file>:<frame_id>"`, z.B. `"expertise-profiles/process-consulting:diagnostic-frames.md:vorderbuhne-hinterbuhne"`

### Schritt 3 — Handover-File schreiben (Atomic-Write D5)

Pfad: `bridge/handover/<round>-advisor-worker-<short-uuid>.md`

YAML-Frontmatter gegen `schemas/handover_frontmatter_v1.json` validieren VOR Persistierung. Bei Validierungs-FAIL: ABBRUCH, Nutzer informieren.

Body-Sections (Empfehlung):
- Zusammenfassung
- Konkrete Empfehlung / Patches / Counter / Status
- Wall-Clock-Schätzung mit Bottleneck-Marker
- Cross-Refs

### Schritt 4 — State.json updaten (Atomic, §13.2)

Read-Validate-Mutate-CAS-Write Pattern:

1. Read state.json + read_at = state["updated_at"]
2. Validate state gegen Schema
3. Append neuen rounds-Eintrag (round=N+1, type, initiator=advisor, artifact_path, timestamp)
4. Append status_observation falls neuer Fact dokumentiert
5. Inkrementiere current_round
6. Update updated_at
7. CAS-Write (rename .tmp.<uuid> → state.json nur wenn updated_at unverändert)

Bei CAS-Failure: max 3 Retries, dann ABBRUCH + Nutzer informieren.

## Round-Type-Heuristik

| Trigger | Round-Type |
|---|---|
| "Evaluiere die session" / "Erste Beratung" | `initial-advice` |
| Worker hat in counter-Round Falsifikation gemeldet | `re-sync` |
| Vor execute, Patches identifiziert | `pre-patch` |
| Worker fragt Status-Update an / Advisor will Snapshot teilen | `status` |
| Advisor stellt Klarheits-Frage | `question` |
| User-Entscheidung soll encoded werden | `decision-lock` (mit `decided_by: user` im Frontmatter) |

## Anti-Pattern (FM-Mapping)

- **NICHT** ohne Status-Snapshot ein Handover schreiben (FM-1)
- **NICHT** Memory blind als Tiebreaker nehmen (FM-3) — frisch + explizit
- **NICHT** Pattern aus anderem Pair ungeprüft übertragen (FM-7) — Status-Verifikation pflichtig
- **NICHT** acceptance_criteria oder rollback_triggers überspringen wenn Round-Type es fordert (Schema-allOf-Pflicht)
- **NICHT** state.json schreiben ohne CAS — sonst Race-Condition mit Worker-Session
- **NICHT** Profile-Workflows skippen wenn expertise_profile gesetzt (ADR_0030 §3.4 — Pflicht-Loading bei jedem Trigger)
- **NICHT** Profile mid-Pair switchen — Profile ist init-time-gepinnt (ADR_0030 §3.4, C1)
- **NICHT** Profile-Inhalt wörtlich in Handover kopieren — Eigenformulierung mit profile-Reference (Lizenzrecht-Constraint, ADR_0030 §5 C2)

## Output-Konvention

Nach erfolgreichem Handover-Write:

```
Handover #<round> geschrieben: bridge/handover/<round>-advisor-worker-<short-uuid>.md
Type: <round-type>
Status-Verified-At: <ISO-8601>
References: <count>
Open Blockers updated: <count>
```

## Constraints

- Max 1 Handover pro User-Trigger (kein Auto-Loop)
- Bei CAS-Failure 3x in Folge: ABBRUCH + Manual-Recovery-Hinweis
- Bei session_info MCP-Failure: degraded mode (references[].verified=false), informiere Nutzer explizit

## Cross-Refs

- ADR_0029 §3.1 Rollen-Modell
- ADR_0029 §4.3 Handover-Schema
- ADR_0029 §6 Conflict-Resolution
- ADR_0029 §13 Concurrency
- v0.1.3-Patch-Pipeline §Anti-Plan-Drift CRITICAL (F-RP-29)
- v0.1.3-Patch-Pipeline §User-Translation-Konvention (D-001 Advisor-Pos)
- v0.1.3-Patch-Pipeline F-RP-31 Patch 4 Skill-Mode-Marker
