---
description: Initialisiert ein neues session-bridge Pair als Initiator-Session (rolle wählbar advisor|worker). Generiert pair_id (UUIDv4), legt bridge/state.json an, schreibt eigene Rolle mit pending-attach-Sentinel für die andere Rolle. Andere Session muss anschließend /bridge-attach <pair_id> ausführen — Plugin generiert dafür ready-to-paste-Prompt.
argument-hint: --role=<advisor|worker> --topic="<string>" [--shared-path=<absolute-path>] [--expertise-source="<string>"] [--expertise-profile=<path>] [--worker-focus="<string>"] [--worker-session-id=<string>]
---

# /bridge-init

Initialisiert neuen Session-Bridge-Pair.

## Argumente

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--role=<advisor\|worker>` | ja | Rolle dieser Session im Pair |
| `--topic="<string>"` | ja | Bridge-Topic. **Bei missing → ABBRUCH + User-Question** (siehe §Argument-Resolution-Protokoll, Anti-Pattern: NICHT inferieren) |
| `--shared-path=<absolute-path>` | nein | Pfad zum gemeinsam mountbaren Verzeichnis. **Default: NICHT eigenes Working-Dir** — User-Frage falls nicht gegeben (siehe §Argument-Resolution-Protokoll) |
| `--expertise-source="<string>"` | nur wenn role=advisor | z.B. "escape-game-generator P.1+P.2" |
| `--expertise-profile=<path>` | optional bei role=advisor | Pfad zu einem Expertise-Profile-Verzeichnis (siehe ADR_0030). Z.B. `expertise-profiles/process-consulting` (relativ ab Plugin-Repo) oder `private-notes/expertise-profiles/process-consulting` (relativ ab shared-path) oder absoluter Pfad. Schema v1.1.0 Field. |
| `--worker-focus="<string>"` | nur wenn role=worker | z.B. "phase-1.6 implementation" |
| `--domain-hint=<plugin-self-dev\|use-case\|architecture-spec\|investigation-trace\|methodology-improvement\|other>` | optional (NEU v0.1.5 / PB-007 / ADR_0031 §4.2) | Domain-Klassifikation fuer state.topic_metadata.domain_hint. Aktiviert Domain-aware Threshold-Kalibrierung in Phase D PB-002 (Reflection-Action-Ratio) + advisor-Skill-Domain-Adaptation. Bei missing: state.topic_metadata fehlt komplett (backward-compat). |
| `--worker-session-title="<title>"` | **primaer empfohlen** wenn role=advisor (NEU v0.1.4 / F-RP-24) | Worker-Session-Title (User-friendly, sichtbar in Cowork-UI). Skill resolved intern via `mcp__session_info__list_sessions` exact-title-match. Bei multi-match: User-Disambiguation-Question. Bei no-match: User-Question mit verfuegbaren Sessions. |
| `--worker-session-id=<string>` | Fallback / Power-User wenn role=advisor | Session-ID der Worker-Session direkt. Bleibt akzeptiert fuer Power-User die Session-ID kennen (z.B. via session_info MCP). Bei v0.1.4+ ist `--worker-session-title` primaer empfohlen weil User-friendly. |

## Argument-Resolution-Protokoll (PFLICHT — Anti-Inferenz)

**Bei fehlenden Pflicht-Argumenten KEINE Inferenz, sondern strukturierte User-Question.** Empirisch (Real-User-Pilot 2026-04-26): Inferenz aus eigenem Session-Kontext führte zu Topic-Mismatch (Advisor-Topic "c-archi-audit" vs Worker-Topic "track-p2") — User musste manuell korrigieren.

### Bei missing `--topic`

ABBRUCH mit folgender User-Question (statt Inferenz aus eigener Session):

```
TOPIC fehlt. Bridge-Topic muss explizit gesetzt werden.

Schritt 1: Worker-Session identifizieren via session_info MCP:
  → Aufrufen: mcp__session_info__list_sessions
  → User-Question: "Welche Session ist Worker (Session-ID + Title)?"

Schritt 2: Worker-Session-Kontext lesen:
  → mcp__session_info__read_transcript <worker_session_id> limit=10
  → Topic-Vorschlag aus Worker-Title oder Worker-Working-Subject ableiten

Schritt 3: User-Confirmation:
  "Vorgeschlagenes Topic basierend auf Worker-Session: <X>. Akzeptieren oder anpassen?"

Schritt 4: Erst nach User-Bestätigung → /bridge-init mit korrektem --topic erneut aufrufen.
```

### Bei missing `--shared-path` (NEU v0.1.4 PB-011: tools/find_shared_path.sh Helper)

ABBRUCH mit User-Question. Default-Heuristik (v0.1.4 erweitert):

1. Wenn beide Sessions gleiches Cowork-Project nutzen: deren gemeinsamer Working-Dir.
2. Falls Working-Dirs unterschiedlich: Plugin ruft `tools/find_shared_path.sh <session-id-1> <session-id-2>` auf, schlaegt groessten gemeinsamen Mount-Pfad via Filesystem-Inspektion vor (z.B. `/Users/paulad/<project>/`).
3. Bei Ambiguitaet (mehrere gemeinsame Praefixe): User-explizit-Pfad-Frage mit Kandidaten-Liste.
4. Niemals eigenes Cowork-Outputs-Verzeichnis als Default — Worker-Session sieht das nicht.

**Helper-Tool:** `tools/find_shared_path.sh` (PB-011 v0.1.4) — Stub fuer Filesystem-Heuristik. Voll-Implementation v0.1.5+ wenn session_info Working-Dir-API stabil.

### Bei missing `--worker-session-title` (advisor-only, primaerer Pfad NEU v0.1.4)

Empfohlen aber nicht hart-blockierend. Wenn missing:
- Plugin ruft `mcp__session_info__list_sessions` auf
- Listet aktive Sessions mit Title (User-friendly) + ID (Debug-info)
- User waehlt Worker-Session via Title aus
- Skill resolved Title → Session-ID intern via exact-title-match

### Bei `--worker-session-title` mit multi-match (advisor-only)

- Plugin praesentiert User strukturierte Disambiguation-Question:
  ```
  Title "<X>" matched mehrere Sessions:
  1. <session-id-1> (created <timestamp>)
  2. <session-id-2> (created <timestamp>)
  Welche?
  ```
- User waehlt Index → Skill resolved zu konkreter ID

### Bei `--worker-session-title` mit no-match (advisor-only)

- Plugin praesentiert User: "Title `<X>` nicht in aktiven Sessions gefunden. Verfuegbare Sessions:" + Liste
- User korrigiert Title oder gibt `--worker-session-id` direkt ein

### Bei `--worker-session-id` direkt (Power-User, Fallback)

Akzeptiert ohne Title-Resolution. State-Verhalten identisch (Sentinel-Pfad in v0.1.3+).

`worker.session_id` im state.json wird IMMER auf `pending-attach`-Sentinel gesetzt (D-004 R23-Revidierung, Sentinel-Invariante v0.1.3+) — bridge-attach replaced das spaeter.

## Pre-Flight Phase A (NEU v0.1.8 — Auto-Resolution + Mount-Request)

Vor dem ATOMAR-Pre-Flight läuft eine Auto-Resolution-Phase, die fehlende Args + Mounts auflöst. Reduziert User-Setup-Reibung von 8 manuellen Schritten auf 3 Approve-Klicks + 1 Auswahl-Klick.

**Skip-Klausel:** Wenn alle Pflicht-Args explizit übergeben + alle Pfade bereits in Cowork-Mounts → Phase A komplett übersprungen (backward-compat zu v0.1.7-Manual-Mode).

### Phase A.1: shared-path Auto-Generation + Mount

Wenn `--shared-path` NICHT übergeben (oder = `auto`):

1. Default-Pfad generieren via `tools/bridge_state.py:resolve_shared_path_default(topic)`:
   - Pattern: `~/session-bridge/pilot-runs/p<auto-id>-<topic-slug>/`
   - `auto-id` = nächste freie p-Nummer in `pilot-runs/` (Scan vorhandener `p<N>-`-Folder)
   - `topic-slug` = topic lowercased, Bindestrich-separiert, max 30 Zeichen
2. User-Confirmation: "Default-Pfad: `<path>`. Verwenden? (Y/n oder eigener Pfad)"
3. Bei User-Override: User-Pfad nehmen
4. Folder anlegen: `mkdir -p <path>/bridge`

**Mount-Resolution:**

5. Mount-Check: Wenn `<path>` NICHT in Cowork-Session-Mounts:
   - `mcp__cowork__request_cowork_directory(path=<path>)` aufrufen
   - User sieht Approve-Dialog in Cowork-UI
6. Bei User-Decline: ABBRUCH mit Diagnose "shared-path nicht zugreifbar ohne Mount"

### Phase A.2: profile-path Mount-Request (falls `--expertise-profile`)

Wenn `--expertise-profile=<arg>` gesetzt:

1. Profile-Pfad-Resolution via `tools/bridge_state.py:resolve_profile_path(arg)`:
   - **Absolut-Pfad** (`/...`) → wie übergeben
   - **Relativ-Pfad** → resolve gegen Cowork-Working-Dir
   - **Kurz-Name** (z.B. `klafki`, `adorno`, `foucault`, `luhmann`, `process-consulting`, `arch`, `plugin-dev`) → Lookup-Reihenfolge:
     1. `~/session-bridge/private-notes/expertise-profiles/<name>*/`
     2. `~/session-bridge/expertise-profiles/<name>*/` (public)
     3. Glob-Match (z.B. `klafki` → `klafki-didaktik`); bei multi-match: User-Disambiguation
   - **Kurz-Name-Mapping** (Auto-Auflösung):
     - `klafki` → `klafki-didaktik`
     - `adorno` → `adorno-halbbildung-kritik`
     - `foucault` → `foucault-genealogie`
     - `luhmann` → `luhmann-erziehungssystem`
     - `process-consulting` / `process` → `process-consulting`
     - `arch` / `architecture` → `architecture-archaeology`
     - `plugin-dev` / `claude-plugin-dev` → `claude-plugin-dev`

2. Mount-Check: Wenn Profile-Pfad NICHT in Cowork-Mounts:
   - `mcp__cowork__request_cowork_directory(path=<resolved-profile-path>)`
3. Bei User-Decline: WARN "Profile-Mount verweigert — degraded-mode, Profile wird nicht geladen, advisor agiert generic"

### Phase A.3: worker-session-id Auto-Resolution (advisor-only)

Wenn `--worker-session-id` UND `--worker-session-title` NICHT übergeben (oder Title = `auto`):

1. `mcp__session_info__list_sessions()` aufrufen
2. Sessions filtern: nur aktive Cowork-Sessions ≠ `this_session_id`
3. Auswahl-Logik:
   - **0 Sessions** → ABBRUCH "Keine andere Cowork-Session aktiv. Worker-Session vorher öffnen + UE-/Material-Generation starten, dann /bridge-init erneut"
   - **1 Session** → Auto-Wahl + User-Confirmation: "Worker-Session: `<title>` (id: `<short-id>`). OK? (Y/n)"
   - **N Sessions** → User-Auswahl-Liste:
     ```
     Aktive Sessions:
     [1] <title-1> (id: <short-id-1>, created <timestamp>)
     [2] <title-2> (id: <short-id-2>, created <timestamp>)
     ...
     Welche ist Worker? [1-N]
     ```

4. Resolved Session-ID → `worker_session_id_hint` (für Notification-Block, nicht für state-pin per D-004)

### Phase A.4: Pair-ID-Anzeige für Worker-Attach (vereinfacht)

Output am Ende von Phase A enthält:
- Generierter `pair_id`
- Resolved `shared_path` (mit Mount-Bestätigung)
- Resolved `expertise_profile` (Pfad + Profile-Name)
- Identified Worker-Session (Title + Short-ID)
- **Copy-Paste-Block für Worker** (siehe §Worker-Notification-Block, vereinfacht durch Auto-Resolution: keine manuelle Path-Eingabe mehr nötig)

---

## Pre-Flight (PFLICHT, ATOMAR — alle 5 Punkte VOR state.json-Write)

**Empirisch (Real-User-Pilot): Pre-Flight Punkt 4 wurde "deferred" — Spec-Bruch.** Pre-Flight ist atomar, kein Punkt darf deferred werden.

1. `<shared-path>/bridge/` ist beschreibbar (test: `mkdir -p <shared-path>/bridge && touch <shared-path>/bridge/.write-test && rm <shared-path>/bridge/.write-test`). **Bei FAIL → ABBRUCH** mit Diagnose "shared-path nicht beschreibbar via Sandbox. Fallback: Host-MCP osascript verwenden (siehe §Sandbox-vs-Host-MCP)".
2. `<shared-path>/bridge/state.json` existiert NICHT (sonst Konflikt mit bestehendem Pair). **Bei FAIL → ABBRUCH** mit Hinweis auf existierende pair_id.

   **PFLICHT-Tool-Call (NEU v0.1.3 / F-RP-22, NICHT Conversational-Memory):**
   Bei JEDEM /bridge-init-Aufruf:
   ```bash
   mcp__workspace__bash 'test -f <shared-path>/bridge/state.json && echo EXISTS || echo MISSING'
   ```
   ODER (falls shared-path außerhalb sandbox):
   ```applescript
   mcp__Control_your_Mac__osascript 'do shell script "test -f <state.json> && echo EXISTS || echo MISSING"'
   ```

   Read-Result als Text-Output anzeigen ('filesystem read: state.json [exists|missing]').

   **NIEMALS** auf Conversational-Memory verlassen ("habe state.json vor X Min selbst erstellt"). In-Session-Re-Init nach external-cleanup muss state als MISSING erkennen, nicht Cache.
3. `python3 -c "import jsonschema"` PASS oder `graceful_degrade=True` setzen (Heuristik-Fallback, references[].verified=false markieren).
4. `mcp__session_info__list_sessions` callable. **NICHT deferrable.** Bei FAIL → degraded-mode mit explizitem User-Hinweis "advisor-Skill funktioniert eingeschränkt ohne session_info — references[].verified=false durchgängig".
5. **Profile-Validation falls `--expertise-profile=<path>` gesetzt** (ADR_0030 §3.4, ERWEITERT v0.1.3 für F-RP-15 / D-005 Sub-A):

   5.a Profile-Pfad existiert auf Host (Read-Tool-Check):
   - Profile-Verzeichnis existiert
   - `<profile>/PROFILE.md` existiert + frontmatter parsebar
   - Frontmatter hat Pflicht-Felder: `profile_name`, `profile_version`, `profile_schema_version`, `domain`, `methodology_pillars`, `sources`, `pflicht_workflows`, `linkage_to_bridge_rounds`, `required_files`
   - Alle `required_files` aus Frontmatter existieren im Profile-Verzeichnis
   - `profile_schema_version` ist supported (`1.0.0` oder `1.1.0` — v1.1.0 erlaubt 6. Profile-File, z.B. `plugin-dev-patterns.md` / `token-efficiency-patterns.md`)
   - **Bei FAIL → ABBRUCH** mit Profile-Diagnose. Empfehlung: Profile-Pfad korrigieren oder ohne `--expertise-profile` initialisieren (generic advisor).

   5.b **Profile-Pfad sandbox-erreichbar (NEU v0.1.3 / D-005 Sub-A F-RP-15):**
   - Test via `mcp__workspace__bash 'test -d <profile-path>'`
   - Bei FAIL: WARN "Profile-Pfad nicht sandbox-mounted — Subprocess-Aufrufe werden scheitern. Add-Dir im Cowork-Project setzen oder Profile in Working-Dir verschieben."
   - WARN nicht hard-FAIL: bridge-init kann fortgesetzt werden, aber Profile-Subprocess-Loading wird zur Laufzeit scheitern

   5.c Profile-Frontmatter-Pflicht-Felder validieren — siehe 5.a.

**Bei FAIL eines Pre-Flight-Punkts: ABBRUCH + Diagnose. NIEMALS Pre-Flight teilweise überspringen.**

## §sandbox-mount-prerequisite (NEU v0.1.3 / F-RP-15 / D-005 Sub-A)

Plugin-Use-Project Setup-Pflicht für `--expertise-profile`-Pfad:

- Profile-Pfad muss entweder im Cowork-Project Working-Dir liegen
  ODER als Add-Dir im Cowork-Project konfiguriert sein
- Sonst: Subprocess-Aufrufe via workspace-bash auf Profile-Files scheitern
  mit "No such file or directory" trotz Pre-Flight 5a PASS

**Empirische Validierung (bridge-pair p3-real-user):**
- Profile-Pfad: `/Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/`
- Erforderte Add-Dir in beiden Cowork-Projects (advisor + worker)
- Workaround: jeweils Add-Dir setzen vor /bridge-init

**Setup-Vorschlag für künftige Plugin-Dev-Pilots:**

1. Cowork-Project erstellen mit Working-Dir
2. Add-Dirs setzen (mind. shared-path, ggf. Profile-Pfad falls nicht in Working-Dir)
3. /bridge-init aufrufen — Pre-Flight 5b prüft sandbox-Erreichbarkeit
4. Bei WARN 5b: Add-Dir-Setup nachholen, Re-Init

## §--worker-session-id (REVIDIERT v0.1.3 / D-004 F-RP-23 PATCH)

`--worker-session-id` ist jetzt **UX-Hint für Worker-Notification-Block**,
NICHT state-Pin.

**Verhalten v0.1.3+:**
- bridge-init schreibt IMMER `state.roles.worker.session_id = "pending-attach"` (Sentinel)
- `--worker-session-id` (falls übergeben) wird NUR für Worker-Notification-Block-Generierung verwendet
- bridge-attach Pre-Flight 4 bleibt strikt auf Sentinel-String

**Migration für v0.1.2-Use-Cases:**
- Bestehende `state.json` mit direktem session_id-Pin: bridge-attach FAIL
- Workaround: state.json-Patch (session_id zurück auf "pending-attach")
- Empfehlung: Re-Init in v0.1.3+

**Begründung (D-004 R23-Position-Revidiert):**
- Sentinel-Pfad-Invariante als Spec-Kontrakt
- Plugin-Marketplace-Adoption-Argument konsistent mit D-002/D-005-A
- p3-Pilot-Empirie als Cross-Reference behalten (Implementation-Bug-Verdacht
  oder Version-Path-Diff in v0.1.2 Pre-Flight 4 Tolerance)

## Sandbox-vs-Host-MCP-Mechanismus

**Empirisch (Real-User-Pilot): Sandbox-bash kann shared-path außerhalb Cowork-Mount nicht beschreiben.**

Konvention für Schreib-Operationen auf state.json:

| Pfad-Typ | Mechanismus |
|---|---|
| `<shared-path>` ist Cowork-Project-Mount der eigenen Session | `mcp__workspace__bash` ok |
| `<shared-path>` ist außerhalb Cowork-Mount (z.B. anderes Project) | **Host-MCP `mcp__Control_your_Mac__osascript`** erforderlich |

Plugin testet beim Pre-Flight Punkt 1 implizit. Falls write-test via Sandbox fail → automatischer Fallback auf Host-MCP (User wird informiert).

## Ablauf (operational, mit Anti-Inferenz + atomarem Pre-Flight)

```python
# 0. Argument-Resolution: Bei missing Pflicht-Args → User-Question, KEINE Inferenz
if not topic:
    abort_with_user_question("topic")  # siehe §Argument-Resolution-Protokoll
if not shared_path:
    abort_with_user_question("shared-path")

# 1. Pre-Flight ATOMAR (alle 4 Punkte VOR Write)
preflight_results = []
for check in [shared_path_writable, state_not_exists, jsonschema_available, session_info_callable]:
    result = check()
    preflight_results.append(result)
    if not result.ok and not result.degraded_acceptable:
        abort(f"Pre-Flight FAIL: {result.diagnosis}")

# 2. UUID generieren
pair_id = str(uuid.uuid4())

# 3. State-Skeleton mit pending-attach-Sentinel für die NICHT-eigene Rolle
# (P-RP-01 Schema-Konsistenz: schema verlangt session_id+active_since als required für BEIDE roles)
SENTINEL_PENDING = "pending-attach"
now = now_iso()

if role == "advisor":
    # ADR_0030: Profile-Pin zur init-Zeit
    profile_data = load_and_validate_profile(expertise_profile) if expertise_profile else None
    advisor_obj = {
        "session_id": this_session_id,
        "expertise_source": expertise_source,
        "expertise_profile": expertise_profile if expertise_profile else None,
        "profile_version": profile_data["frontmatter"]["profile_version"] if profile_data else None,
        "active_since": now
    }
    # REVIDIERT v0.1.3 (D-004 F-RP-23): IMMER Sentinel, --worker-session-id ist UX-Hint
    worker_obj = {
        "session_id": SENTINEL_PENDING,
        "active_since": now
    }
    # worker_session_id (falls übergeben) → NUR für Notification-Block (Schritt 7), NICHT in state pinnen
else:  # role == "worker"
    advisor_obj = {
        "session_id": SENTINEL_PENDING,
        "expertise_profile": None,
        "profile_version": None,
        "active_since": now
    }
    worker_obj = {
        "session_id": this_session_id,
        "current_focus": worker_focus,
        "phase": worker_phase,
        "active_since": now
    }

state = {
    "pair_id": pair_id,
    "schema_version": "1.2.0",  # v0.1.5 PB-007 + v0.1.10 memory_symmetry
    "created_at": now,
    "updated_at": now,
    "phase": "init",
    "roles": {"advisor": advisor_obj, "worker": worker_obj},
    "topic": topic,
    "current_round": 0,
    "rounds": [],
    "open_blockers": [],
    "decision_log": [],
    "status_observations": [],
    "file_ownership": {},
    "shared_artifacts": [],
    "wallclock_estimates": [],
    "rollback_plan_path": None,
    # v0.1.12 12-A: memory_symmetry_status-Init bei Bridge-Init (statt erst bei close)
    # Empirisch (p12/p13/p14 n=3): Field war unset → blockierte Pattern-#103-Mechanik
    "memory_symmetry_status": "pending"
}

# 4. Schema-Validate (M1' Akzeptanz) — sentinel-pending-attach ist String, schema-konform
validate(state, bridge_state_v1_schema)

# 5. Atomic-Write (via Sandbox-bash ODER Host-MCP osascript je nach Pre-Flight-Result)
write_atomic(f"{shared_path}/bridge/state.json", state, mechanism=preflight_results.write_mechanism)

# 6. mkdir bridge/handover/, bridge/artifacts/, bridge/orphans/
ensure_dirs([
    f"{shared_path}/bridge/handover",
    f"{shared_path}/bridge/artifacts",
    f"{shared_path}/bridge/orphans"
])

# 7. Worker-Notification-Block generieren (P-RP-04 — kritisch, sonst Pair stuck in init)
print_worker_notification_block(pair_id, role, shared_path)
```

## Worker-Notification-Block (PFLICHT-Output bei role=advisor)

**Empirisch (Real-User-Pilot): Worker-Session hat nie attached → Pair faktisch tot.** Plugin generiert daher einen ready-to-paste-Block für die Worker-Session.

Format:

```
============================================================
BRIDGE-PAIR INITIALISIERT — pair_id: <pair_id>
============================================================

  role (this):  <role>
  topic:        <topic>
  shared-path:  <shared-path>
  phase:        init

============================================================
KRITISCH: Worker-Session muss jetzt attachen.
============================================================

In der Worker-Session (Session-Title: "<worker_title>") folgendes
EXAKT als User-Prompt eingeben:

----- COPY-PASTE-BLOCK -----

/bridge-attach <pair_id> --role=worker --shared-path=<shared-path>

----- ENDE COPY-PASTE-BLOCK -----

Nach Worker-Attach:
  - Worker-Session bestätigt: "Pair attached. Phase: scope-lock."
  - Beide Sessions können dann /bridge-handover-Commands ausführen.

WARNUNG: Solange Worker nicht attached → state.json hat
"pending-attach"-Sentinel. Pair-Lifecycle ist blockiert.
============================================================
```

Bei role=worker: Block ist umgekehrt (Advisor muss attachen).

## Akzeptanz (verschärft)

- `bridge/state.json` existiert + jsonschema-validate PASS (mit pending-attach-Sentinel als String akzeptiert)
- `bridge/handover/`, `bridge/artifacts/`, `bridge/orphans/` existieren
- pair_id im Output angezeigt
- Phase = `init`
- **Worker-Notification-Block im Output präsent** (P-RP-04)
- Pre-Flight alle 4 Punkte explizit dokumentiert mit PASS/DEGRADED/FAIL (P-RP-03)

## Anti-Pattern (verschärft)

- NICHT init aufrufen wenn bereits state.json existiert (würde überschreiben)
- NICHT ohne `--topic` initialisieren — User-Question statt Inferenz (P-RP-02)
- NICHT Pre-Flight teilweise deferren — alle 4 Punkte atomar VOR Write (P-RP-03)
- NICHT shared-path aus eigenem Working-Dir inferieren — User-Question (P-RP-02)
- NICHT Worker-Notification-Block weglassen — sonst kann Worker nicht attachen (P-RP-04)

## UX-Pattern: Visualization-Widget für Argument-Erfassung (NEU v0.1.3 / F-RP-19)

Bei missing required-Args nutzt bridge-init `mcp__visualize__show_widget`
mit elicitation-Form für strukturierte Eingabe. Pattern empfohlen für:

- `--topic` (free text)
- `--shared-path` (file path picker mit Default-Heuristik)
- `--expertise-source` (free text)
- `--expertise-profile` (dropdown mit Lookup auf `expertise-profiles/`-Verzeichnisse)
- `--worker-session-id` (dropdown mit Lookup via session_info MCP)

**Empirische Validierung:** bridge-pair p3-real-user R0 nutzte Visualization-Widget
für Argument-Erfassung; Form-Vollständigkeit hat Pre-Flight 5 Profile-Validation
ermöglicht.

**Anti-Pattern:** missing required-Args ohne Elicitation-Form ist Modell-abhängig
(siehe F-RP-32 hard-enforce-Patch in v0.1.3).

## Cross-Refs

- ADR_0029 §5.1 Lifecycle init-Phase
- ADR_0029 §13.2 Concurrency Atomic-Write
- BACKLOG.md Phase-2 Activation-Trigger erfüllt 2026-04-26 via Real-User-Pilot
- Empirisch validiert: Real-User-Pilot 2026-04-26 (EG_DEV_ADVISOR-Session, F-RP-01..04)
- v0.1.3-Patch-Pipeline (`pilot-runs/p3-real-user/v0.1.3-patch-pipeline.md`) — UX-Pattern + Sentinel-Invariante (D-004)
