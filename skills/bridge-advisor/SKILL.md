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

## §Cowork-Mode-Composition-Pattern (NEU v0.1.9 / Pattern-#76+#77+#80 aus p7-upp-praxis-validation)

**Empirisch (p7-praxis R5):** Plugin-Skills im Cowork-Mode sind **Reading-Pattern-Skills**, NICHT Auto-Pipeline-Skills. Skill-Spec gibt Anleitungen für Claude/User, ruft aber selbst keine Sub-Skills automatisch auf.

**Konsequenz für bridge-advisor:**

- SKILL.md §Schritt 0 (Profile-Loading) ist Anleitung an Claude, was zu lesen ist
- Multi-Pass-Workflows aus workflows.md sind Anleitungen, was sequentiell durchzuführen ist
- Composition-Sektion = "Empfohlene Reihenfolge", NICHT Auto-Aufruf

**Anti-Pattern:** Skill-Spec als Auto-Pipeline interpretieren produziert Pseudo-Garantien. Tatsächlich wird die Komposition durch Claude-Reasoning umgesetzt — Spec muss als Reading-Pattern-Skill formuliert sein.

**Cowork-Mode-Composition-Reihenfolge bridge-advisor (Empfehlung):**
1. Schritt 0 Profile-Loading
2. Schritt 1 Status-Snapshot via session_info
3. Schritt 2 References sammeln (Pflicht: ≥1 reference)
4. **Schritt 2.5 (NEU v0.1.9) Phase-Gate-Audit** (siehe §Phase-Gate-Audit-Pflicht unten)
5. Schritt 3 Handover-File schreiben
6. Schritt 4 State.json updaten

## §Profile-Activation-Decision-Tree (NEU v0.1.12 / Empirie aus p12/p13/p14 = 0 Profile-Aktivierungen)

**Empirie:** p12 (architecture-spec-patch, closed) + p13 (architecture-spec, iterate) + p14 (architecture-spec, scope-lock) = 3 Pairs ohne Profile-Aktivierung. Implikation: Profile-Mechanik wird empirisch nicht für alle Use-Cases gebraucht. Spec-vs-Empirie-Drift (AP-T01 aus architecture-archaeology-Profile).

**Methodische Erkenntnis:** Profile-Layer ist Use-Case-spezifisch. Architecture-Patches benötigen es nicht; Bildungs-/Org-/Kultur-Use-Cases benötigen es substantiell.

**Decision-Tree für `--expertise-profile`-Flag bei /bridge-init:**

| Topic-Klasse | Profile-Aktivierung | Begründung |
|---|---|---|
| **Plugin-/Spec-Patch / Schema-Validation / Schema-Refactor** | **NICHT empfohlen** | Architecture-Pairs sind Single-Domain, Profile-Layer ist over-engineering. Bisher empirisch alle architecture-spec-patch-Pairs erfolgreich ohne Profile (p8/p9/p10/p12). |
| **Plugin-Audit / Recursive Self-Audit / Token-Effizienz-Diagnose** | **`architecture-archaeology` empfohlen** | Use-Case-Anker des Profile (TC-AA1). Hermeneutik + Token-Forensik substantieller Mehrwert. |
| **Bildungs-/Curricular-Beratung (UE / Sequenz / Lehrplan)** | **`klafki-didaktik` empfohlen** | Empirisch validiert in p7-klafki-validation (8 Rounds, 9 DLs, alle 6 F-Cluster aktiviert). |
| **Bildungs-/Kulturkritik-Diskurs** | **`adorno-halbbildung-kritik` empfohlen** | Negative Dialektik + Halbbildungs-Diagnose. Multi-Pass-Workflow methodisch geboten. |
| **Schule-als-Disziplinarinstitution / Macht-Wissen-Analyse** | **`foucault-genealogie` empfohlen** | Use-Case-Anker (F5.2 Schule als Disziplinar-Apparat). |
| **Erziehungssystem-Operation / Code-Programm-Diagnose** | **`luhmann-erziehungssystem` empfohlen** | Funktionssystem-Theorie operationalisiert. |
| **Organisations-Spannung / Person-Funktion-Trennung** | **`process-consulting` empfohlen** | Systemtheoretisch-luhmannsch eng auf Org-Beratung. |
| **Cross-Profile-Diskurs (z.B. Klafki + Adorno + Foucault)** | **Primär-Profile aktivieren + Lookup-Pattern v0.1.11 nutzen** | tools/profile_frame_lookup.py für punktuelle Sekundär-Profile-Anwendung. ADR_0030 Annex E. |

**Decision-Trigger-Frage bei /bridge-init:**

advisor stellt User folgende Frage, wenn `--expertise-profile` NICHT explizit gesetzt + Topic ist NICHT eindeutig architecture-patch:

```
Profile-Aktivierung erwägen?
- Topic klassifiziert: <category>
- Vorgeschlagenes Profile: <profile-name oder "kein Profile">
- Begründung: <warum>
- Akzeptieren / anpassen / ohne Profile fortsetzen?
```

**Anti-Pattern:** Profile-Aktivierung ohne Use-Case-Match produziert AP-T07 Multi-Pass-Over-Engineering (architecture-archaeology) + AP-T08 Profile-Eager-Loading. Profile-Layer ist nicht universal-anwendbar.

**Architecture-Patch-Selbst-Diagnose:** Spec-Patch-Pairs (p8/p9/p10/p12) sind drift-effizient (0.05-0.13) auch ohne Profile. Profile würde Token-Overhead ohne methodischen Mehrwert produzieren.

## §Profile-Frame-Dispatch-Pattern (NEU v0.1.11, Option B-Plus)

**Empirie:** 6 Profile-Familie produziert. User-Use-Cases wechseln Domain häufig (z.B. architecture-archaeology-Pair will Adorno-AP für Marketing-Text-Diagnose). Aktuell: Profile-Wechsel via neuer Pair = ~36000 Tokens (Pair-Setup + Profile-Loading × 2). Punktuelle Lookup ist Token-effizient.

**Pattern (Option B-Plus aus ADR_0030 Annex E):**
- Single-Primär-Profile bleibt aktiv (methodische Kohärenz, ADR_0030 D5 Single-Profile-Pinning erhalten)
- Sekundär-Profile-Elemente (Frames / APs / Questions / Workflow-Passes) können punktuell abgerufen werden via `tools/profile_frame_lookup.py`
- Token-Cost: ~500-1500 Tokens pro Lookup statt ~18000 für Profile-Aktivierung
- Methodische-Konsistenz-Marker im Output Pflicht: User sieht "punktuelle Anwendung, nicht voll-Methodik"

**API:**

```python
from tools.profile_frame_lookup import (
    lookup_frame,           # lookup_frame("adorno", "F5.1") → AP-Frame mit body
    lookup_ap,              # lookup_ap("adorno", "AP-A05") → AP mit Selbstanwendung
    lookup_question,        # lookup_question("klafki", frame_id="F2.1", round_type="counter")
    lookup_workflow_pass,   # lookup_workflow_pass("adorno", "W-A-Multi", pass_n=3)
    list_available_profiles,
    list_frames,
    list_aps,
    lookup_token_cost_estimate,
)
```

**Wann Lookup verwenden (advisor-Skill-Anweisung):**

| Anliegen-Typ | Aktion |
|---|---|
| Domain-fremde Aspekt-Diagnose innerhalb laufender Pair | Frame-/AP-Lookup statt Profile-Wechsel |
| Cross-Profile-Cross-Reference im handover | Lookup + Methodische-Konsistenz-Marker |
| Methodische Tiefe für Sekundär-Aspekt erforderlich | Lookup + bei Bedarf separater Pair mit Sekundär-Profile (User-Decision) |
| Worker fragt explizit nach Cross-Profile-Lesart | Lookup-Output mit Marker, dass volle Methodik nicht aktiv |

**Output-Format-Pflicht bei Cross-Profile-Lookup:**

```
§Cross-Profile-Lookup (B-Plus, v0.1.11):
- Primär-Profile: <name>
- Lookup-Profile: <name>
- Lookup-Element: <frame-id / ap-id / workflow-pass>
- Token-Cost: <estimate> (vs voll-Profile ~18000)
- Anwendungs-Diagnose: <Befund>
- Methodische-Konsistenz-Hinweis: Punktuelle Anwendung von <element>. Voll-Methodik (Selbstanwendung / Multi-Pass / Reflexivität) NICHT aktiv. Bei Bedarf separater Pair mit <profile> empfohlen.
```

**Anti-Pattern (CRITICAL):**

- **NICHT** Cross-Profile-Lookup als Ersatz für vollständige Methodik präsentieren — Marker-Pflicht
- **NICHT** mehrere Profile-Lookups akkumulieren ohne Methodik-Konsistenz-Reflexion
- **NICHT** Cross-Profile-Lookup ohne Triangulation in Architektur-Audit-Anliegen (Anti-Kosmetik AP-T10 aus arch-Profile)

**Cross-Refs:** ADR_0030 Annex E (v0.1.11), tools/profile_frame_lookup.py, expertise-profiles/architecture-archaeology/token-efficiency-patterns.md OP-1.

## §Phase-Gate-Audit-Pflicht (NEU v0.1.9 / Pattern-#88 aus p7-upp-praxis-validation)

**Empirisch (p7-praxis R16-Advisor-Cross-Check):** Worker-R6→R8 ohne expliziten Phase-Gate-Audit produzierte Lehrkraft-Realbedingungen-Defizit (4 CRITICAL-Findings übersehen). Phase-Transition ohne Validation der vorherigen Phase-Outputs ist methodische Lücke.

**Pflicht-Klausel (CRITICAL):**

bridge-advisor MUSS bei jedem handover (außer initial-advice + status) einen **Phase-Gate-Audit** der Worker-vorherigen-Phase durchführen, bevor inhaltliche Beratung erfolgt.

**Phase-Gate-Audit-Schritte:**

1. **Phase-Identifikation:** In welcher Phase ist Worker aktuell? (state.roles.worker.phase oder aus letztem Worker-handover)
2. **Phase-Output-Inventar:** Welche Outputs/Artefakte hat Worker in vorheriger Phase produziert? (shared_artifacts + handover-Body)
3. **Gate-Kriterien-Pflicht-Check:**
   - Sind Outputs der vorherigen Phase **vollständig** (gegen Phase-spezifische Acceptance-Criteria)?
   - Sind Outputs **validiert** (User-Authority oder methodische Pflicht-Workflows angewandt)?
   - Liegen **CRITICAL-Findings** unbehandelt vor?
4. **Audit-Verdikt:** PASS / WARN / FAIL
   - PASS → fortsetzen mit inhaltlicher Beratung
   - WARN → Beratung mit explizitem Audit-Hinweis im handover-§
   - FAIL → STOP-handover mit Klärungs-Anforderung an Worker (status-handover statt inhaltlich)

**Output-Format-Pflicht:**

```
§Phase-Gate-Audit (v0.1.9-Pflicht):
- Worker-Phase aktuell: <phase-name>
- Output-Inventar vorherige Phase: <Liste>
- Gate-Kriterien-Check:
  - Vollständigkeit: [PASS/WARN/FAIL] — <Begründung>
  - Validation: [PASS/WARN/FAIL] — <Begründung>
  - CRITICAL-Findings: [keine / <Liste>]
- Audit-Verdikt: [PASS/WARN/FAIL]
- Konsequenz: [Beratung-fortgesetzt / Audit-Warning-eingebaut / Klärungs-Anforderung]
```

**Anti-Pattern:** Phase-Gate-Audit-Skip produziert das p7-R16-Pattern (Worker-Bilanz-Defizit unentdeckt). Skip ist nur akzeptabel bei initial-advice (keine vorherige Phase) und status (Diagnose-only, keine Beratung).

**Cross-Ref:** Pattern-#88 in `pilot-runs/p7-upp-praxis-validation/bridge/artifacts/praxis_validation_befunde.md §9.7`.

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
    #   "frontmatter": {profile_name, methodology_pillars, sources, pflicht_workflows, linkage_to_bridge_rounds, required_files, ...},
    #   "diagnostic_frames": [...],   # aus diagnostic-frames.md
    #   "anti_patterns": [...],        # aus anti-patterns.md
    #   "question_bank": {...},        # aus question-bank.md
    #   "workflows": {...}             # NEU v0.1.6: aus workflows.md (optional, falls in required_files)
    # }
    profile_workflow_modifier = profile["frontmatter"]["linkage_to_bridge_rounds"].get(round_type, "")
    pflicht_workflows = profile["frontmatter"]["pflicht_workflows"]
    # NEU v0.1.6: Workflow-Spec laden, falls vorhanden
    workflow_specs = profile.get("workflows", {})  # workflow_id → {trigger, pflicht_schritte, output_format, linkage}
else:
    profile = None
    pflicht_workflows = []
    workflow_specs = {}
```

**File-Loading-Logik (v0.1.6):** Lade alle in `frontmatter.required_files` aufgelisteten Files. Bekannte Files: `PROFILE.md` (Frontmatter-Quelle), `diagnostic-frames.md`, `anti-patterns.md`, `question-bank.md`, `workflows.md` (NEU v0.1.6, optional). Unbekannte Files in `required_files` werden als Profile-Annex geladen und in `profile["annexes"][filename]` abgelegt — dürfen advisor-Workflow nicht blockieren.

**File-Aliase (NEU v0.1.7):** Profile-Konvention erlaubt Datei-Naming-Varianten — Skill akzeptiert beide:
- `diagnostic-frames.md` ODER `konstellations-anker.md` (Adorno-Profile-Style)
- `question-bank.md` ODER `negative-diagnose-fragen.md` (Adorno-Profile-Style)

Mapping: Aliase werden in derselben profile-Substruktur abgelegt (z.B. `profile["diagnostic_frames"]` enthält Inhalt aus `konstellations-anker.md` falls statt `diagnostic-frames.md` vorhanden).

**workflows.md-Vorrang-Regel (NEU v0.1.6):** Wenn `workflows.md` geladen ist, hat es Vorrang vor `pflicht_workflows`-Frontmatter-Liste. Frontmatter listet Workflow-IDs (z.B. `perspektivenschema-vollstaendigkeits-check-pre-stundenfrage`); workflows.md enthält die operative Spec (Trigger / Pflicht-Schritte / Output-Format / Linkage / Verweigerungs-Logik). Advisor MUSS workflows.md-Specs anwenden, nicht nur frontmatter-IDs erwähnen.

**Multi-Pass-Workflow-Loading (NEU v0.1.7):** Workflow-Specs in workflows.md können `passes` als geschachtelte Schritt-Liste enthalten:
```python
# workflows = {
#   "W-A-Multi": {
#     "trigger": "...",
#     "passes": [
#       {"pass": 1, "lesart": "literal", "pflicht_schritte": [...]},
#       {"pass": 2, "lesart": "konzeptuell-immanent", "pflicht_schritte": [...]},
#       {"pass": 3, "lesart": "anti-identifikatorische-konstellation", "pflicht_schritte": [...]},
#       {"pass": 4, "lesart": "meta-kritisch", "pflicht_schritte": [...]}
#     ],
#     "output_format": "...",
#     "linkage": [...],
#     "verweigerungs_logik": "...",
#     "selbstkritik_klausel": "..."
#   }
# }
```

Wenn `passes` vorhanden: advisor MUSS alle passes sequentiell durchlaufen, kein Pass darf übersprungen werden. Pass-Verkürzung produziert AP-A03 (identifizierende Subsumtion) bei Adorno-style-Profilen oder analoge Verfehlungen bei anderen Profile-Schulen.

Bei `passes`-Absent: Workflow funktioniert single-pass wie v0.1.6 (Backward-Compatibility).

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
| Worker-Plan unvollständig + Profile-Workflow-Verweigerungs-Bedingung erfüllt (NEU v0.1.6) | `status` mit Klärungs-Anforderung statt `initial-advice` |

## Anti-Pattern (FM-Mapping)

- **NICHT** ohne Status-Snapshot ein Handover schreiben (FM-1)
- **NICHT** Memory blind als Tiebreaker nehmen (FM-3) — frisch + explizit
- **NICHT** Pattern aus anderem Pair ungeprüft übertragen (FM-7) — Status-Verifikation pflichtig
- **NICHT** acceptance_criteria oder rollback_triggers überspringen wenn Round-Type es fordert (Schema-allOf-Pflicht)
- **NICHT** state.json schreiben ohne CAS — sonst Race-Condition mit Worker-Session
- **NICHT** Profile-Workflows skippen wenn expertise_profile gesetzt (ADR_0030 §3.4 — Pflicht-Loading bei jedem Trigger)
- **NICHT** Profile mid-Pair switchen — Profile ist init-time-gepinnt (ADR_0030 §3.4, C1)
- **NICHT** Profile-Inhalt wörtlich in Handover kopieren — Eigenformulierung mit profile-Reference (Lizenzrecht-Constraint, ADR_0030 §5 C2)
- **NICHT** workflows.md-Output-Formate ignorieren wenn Workflow getriggert (NEU v0.1.6) — wenn workflow_specs[w_id]["output_format"] vorhanden, MUSS advisor das Format in handover §-Sektionen einbetten
- **NICHT** Workflow-Verweigerungs-Logik skippen (NEU v0.1.6) — wenn workflow_specs[w_id]["verweigerungs_klausel"] erfüllt (z.B. W-01 N≥3 leere Perspektiven), advisor schreibt status-handover mit Klärungs-Anforderung statt fortzufahren
- **NICHT** Multi-Pass-Workflow-passes überspringen (NEU v0.1.7) — wenn workflow_specs[w_id]["passes"] vorhanden, MUSS advisor alle Pässe sequentiell durchlaufen; Pass-Verkürzung produziert identifizierende Subsumtion oder analoge methodische Verfehlung
- **NICHT** Selbstkritik-Klauseln in Profile-Workflows ignorieren (NEU v0.1.7) — wenn workflow_specs[w_id]["selbstkritik_klausel"] vorhanden, MUSS advisor diese Selbstkritik im Output-§ ausführen

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
- ADR_0030 Expertise-Profile-Pattern §3.4 Profile-Loading
- ADR_0030 Annex B (NEU v0.1.6) Profile-with-workflows.md-Pattern
- ADR_0030 Annex C (NEU v0.1.7) Multi-Pass-Workflow-Pattern + File-Aliase
- v0.1.3-Patch-Pipeline §Anti-Plan-Drift CRITICAL (F-RP-29)
- v0.1.3-Patch-Pipeline §User-Translation-Konvention (D-001 Advisor-Pos)
- v0.1.3-Patch-Pipeline F-RP-31 Patch 4 Skill-Mode-Marker
- v0.1.6 SKILL-Patch §Schritt 0 workflows.md-Loading + §Anti-Pattern Workflow-Output-Format-Enforcement
- v0.1.7 SKILL-Patch §Schritt 0 Multi-Pass-Loading + File-Aliase + §Anti-Pattern Pass-Skip-Verbot + Selbstkritik-Klausel-Enforcement
