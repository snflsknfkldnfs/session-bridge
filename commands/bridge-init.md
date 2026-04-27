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
| `--worker-session-id=<string>` | empfohlen wenn role=advisor | Session-ID der Worker-Session (für Status-Verifikation via session_info MCP). Falls unbekannt: Skill listet via list_sessions + fragt User |

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

### Bei missing `--shared-path`

ABBRUCH mit User-Question. Default-Heuristik:

1. Wenn beide Sessions gleiches Cowork-Project nutzen: deren gemeinsamer Working-Dir.
2. Falls Working-Dirs unterschiedlich: User-explizit-Pfad-Frage. Plugin schlägt vor: "größter gemeinsamer Mount-Pfad" via Filesystem-Inspektion (z.B. `/Users/paulad/<project>/`).
3. Niemals eigenes Cowork-Outputs-Verzeichnis als Default — Worker-Session sieht das nicht.

### Bei missing `--worker-session-id` (advisor-only)

Empfohlen aber nicht hart-blockierend. Wenn missing:
- Plugin ruft `mcp__session_info__list_sessions` auf
- Listet aktive Sessions
- User wählt Worker-Session aus

`worker.session_id` im state.json wird auf `pending-attach`-Sentinel gesetzt falls keine Worker-Session-ID bekannt — bridge-attach replaced das später.

## Pre-Flight (PFLICHT, ATOMAR — alle 5 Punkte VOR state.json-Write)

**Empirisch (Real-User-Pilot): Pre-Flight Punkt 4 wurde "deferred" — Spec-Bruch.** Pre-Flight ist atomar, kein Punkt darf deferred werden.

1. `<shared-path>/bridge/` ist beschreibbar (test: `mkdir -p <shared-path>/bridge && touch <shared-path>/bridge/.write-test && rm <shared-path>/bridge/.write-test`). **Bei FAIL → ABBRUCH** mit Diagnose "shared-path nicht beschreibbar via Sandbox. Fallback: Host-MCP osascript verwenden (siehe §Sandbox-vs-Host-MCP)".
2. `<shared-path>/bridge/state.json` existiert NICHT (sonst Konflikt mit bestehendem Pair). **Bei FAIL → ABBRUCH** mit Hinweis auf existierende pair_id.
3. `python3 -c "import jsonschema"` PASS oder `graceful_degrade=True` setzen (Heuristik-Fallback, references[].verified=false markieren).
4. `mcp__session_info__list_sessions` callable. **NICHT deferrable.** Bei FAIL → degraded-mode mit explizitem User-Hinweis "advisor-Skill funktioniert eingeschränkt ohne session_info — references[].verified=false durchgängig".
5. **Profile-Validation falls `--expertise-profile=<path>` gesetzt** (ADR_0030 §3.4):
   - Profile-Verzeichnis existiert
   - `<profile>/PROFILE.md` existiert + frontmatter parsebar
   - Frontmatter hat Pflicht-Felder: `profile_name`, `profile_version`, `profile_schema_version`, `domain`, `methodology_pillars`, `sources`, `pflicht_workflows`, `linkage_to_bridge_rounds`, `required_files`
   - Alle `required_files` aus Frontmatter existieren im Profile-Verzeichnis
   - `profile_schema_version` ist supported (aktuell `1.0.0`)
   - **Bei FAIL → ABBRUCH** mit Profile-Diagnose. Empfehlung: Profile-Pfad korrigieren oder ohne `--expertise-profile` initialisieren (generic advisor).

**Bei FAIL eines Pre-Flight-Punkts: ABBRUCH + Diagnose. NIEMALS Pre-Flight teilweise überspringen.**

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
    worker_obj = {
        "session_id": worker_session_id if worker_session_id else SENTINEL_PENDING,
        "active_since": now
    }
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
    "schema_version": "1.1.0",  # ADR_0030 Expertise-Profile-Layer
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
    "rollback_plan_path": None
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

## Cross-Refs

- ADR_0029 §5.1 Lifecycle init-Phase
- ADR_0029 §13.2 Concurrency Atomic-Write
- BACKLOG.md Phase-2 Activation-Trigger erfüllt 2026-04-26 via Real-User-Pilot
- Empirisch validiert: Real-User-Pilot 2026-04-26 (EG_DEV_ADVISOR-Session, F-RP-01..04)
