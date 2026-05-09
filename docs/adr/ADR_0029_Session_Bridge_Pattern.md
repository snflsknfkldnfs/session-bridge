# ADR 0029 — Session-Bridge-Pattern

**Status:** LOCKED (2026-04-26 nach Self-Review-Pass A1-A9 PASS)
**Datum:** 2026-04-26
**Autor:** session-bridge-Plugin-Project
**Korpus-Quelle:** `../pattern-mining/CORPUS_ANALYSIS.md`
**Schema-Version:** 1.0.0

---

## 1. Context

Cowork-Mode unterstützt parallele Sessions, aber kein natives Pattern für strukturierte Zusammenarbeit zwischen zwei Sessions. In der Praxis (siehe Korpus-Analyse: WiB7c Plugin-Migration über 3 Tage, 27 Beratungs-Artefakte) wurde wiederholt das Pattern **Advisor-Session berät Worker-Session via User-mediierte Übergaben** rekonstruiert. Diese Rekonstruktion war fragil:

- 9 empirisch dokumentierte Failure-Modes (FM-1..FM-9 in CORPUS_ANALYSIS).
- Pro Pairing wurden Schema, Lifecycle, Rollback-Plan, Akzeptanz-Kriterien neu erfunden.
- Beratungs-Artefakte akkumulierten ohne Lifecycle-Marker (FM-9 Beratungs-Drift).

`session_info`-MCP existiert (read_transcript, list_sessions) und bietet die Infrastruktur, ist aber kein Plugin-Pattern. `agent-teams`-Plugin existiert für parent→child-Spawning, deckt aber keinen Peer-to-Peer-Use-Case zweier User-Cowork-Sessions ab.

Diese ADR definiert ein **wiederverwendbares Pattern + Plugin-Implementierung** zur Koordination zweier paralleler Cowork-Sessions im **Advisor/Worker-Modell** mit **Polling-basierter** Übergabe via Shared-Filesystem.

---

## 2. Drivers

| ID | Driver | FM-Mapping | Quelle |
|---|---|---|---|
| D1 | Status-Verifikation pflichtig (Pre-Round-Status-Re-Check) | FM-1, FM-7 | CORPUS_ANALYSIS §3 |
| D2 | Faktencheck-Tiebreaker (Memory + Capability-Probe als Verifikations-Quelle) | FM-3 | CORPUS_ANALYSIS §3 |
| D3 | File-Ownership-Pre-Lock (verhindert Edit-Konflikte) | FM-4 | CORPUS_ANALYSIS §3 |
| D4 | Wall-Clock-Empirie (Schätzung+Drift-Logging) | FM-2 | CORPUS_ANALYSIS §3 |
| D5 | Artefakt-Lifecycle (active/archived/superseded) | FM-9 | CORPUS_ANALYSIS §3 |
| D6 | Rollback-Vorab-Spezifikation pflichtig | strukturell (Runbook-Pattern) | CORPUS_ANALYSIS §2.2 |
| D7 | Round-Typisierung (encoded round-types statt Freitext) | strukturell | CORPUS_ANALYSIS §2.3 |
| D8 | Strict-Separation Advisor vs Worker auf Identitäts-Ebene | FM-6 | CORPUS_ANALYSIS §3 |
| D9 | Cleanup-Enforcement bei Memory-/Artefakt-Migration (Pflicht-Schritt im close, nicht optional) | FM-5 | CORPUS_ANALYSIS §3 |
| D10 | Shared-Filesystem-Authority statt computer://-URIs (Pfad-Auflösung über Cowork-Mount) | FM-8 | CORPUS_ANALYSIS §3 |

---

## 3. Decision

**Wir bauen ein Plugin `session-bridge` mit folgendem Modell:**

### 3.1 Rollen-Modell

Genau **zwei Rollen** im MVP:

- **`advisor`** — Cowork-Session mit dominanter Expertise / Beobachter-Position. Liest Worker-Transcript via `session_info`, produziert strukturierte Handover-Artefakte mit Empfehlungen / Patches / Counter-Beratung.
- **`worker`** — Cowork-Session mit operativer Verantwortung. Führt Plan aus, schreibt Status-Snapshots in shared State, fragt nach Beratung.

**User** ist nicht Bridge-Teilnehmer, sondern **Round-Trigger** (jede Round wird durch User-Prompt in einer der beiden Sessions getriggert; kein Auto-Tick).

### 3.2 Kommunikations-Modell

**Polling via Shared-Filesystem.** Kein IPC, kein Push.

- Beide Sessions haben Lese/Schreib-Zugriff auf einen gemeinsamen Cowork-Project-Pfad: `<shared-project>/bridge/`.
- `bridge/state.json` ist Single-Source-of-Truth für Pair-State.
- `bridge/handover/<round>-<from>-<to>.md` sind unveränderliche Handover-Artefakte.

### 3.3 Round-Modell

10 encoded Round-Typen (siehe §4.2): 8 procedural (initial-advice, counter, re-sync, decision-lock, pre-patch, pre-flight, execute, verify) + 2 utility (status, question). Rounds sind streng aufsteigend nummeriert. Jede Round produziert genau **eine** Handover-Datei. Round-Numbering ist atomic increment via state.json (siehe §13 Concurrency).

### 3.4 Lifecycle

```
init → scope-lock → iterate (rounds) → execute → verify → close
                          ^   |
                          | counter / re-sync
                          +-----+
```

Phase-Übergänge sind in `state.json` getrackt. Phase-Rückwärts ist erlaubt nur bei `iterate` ↔ `execute` (Re-Sync nach Counter).

---

## 4. Schema-Spezifikation

### 4.1 State-Schema (`bridge/state.json`)

JSON-Schema-Datei: `plugin/schemas/bridge_state_v1.json`. Pflicht-Felder:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "pair_id", "schema_version", "created_at", "updated_at",
    "roles", "topic", "phase", "current_round", "rounds",
    "open_blockers", "decision_log", "status_observations",
    "file_ownership", "shared_artifacts", "wallclock_estimates"
  ],
  "properties": {
    "pair_id": {"type": "string", "format": "uuid"},
    "schema_version": {"const": "1.0"},
    "created_at": {"type": "string", "format": "date-time"},
    "updated_at": {"type": "string", "format": "date-time"},
    "phase": {
      "enum": ["init", "scope-lock", "iterate", "execute", "verify", "close"]
    },
    "roles": {
      "type": "object",
      "required": ["advisor", "worker"],
      "properties": {
        "advisor": {
          "type": "object",
          "required": ["session_id", "active_since"],
          "properties": {
            "session_id": {"type": "string"},
            "expertise_source": {"type": "string"},
            "active_since": {"type": "string", "format": "date-time"}
          }
        },
        "worker": {
          "type": "object",
          "required": ["session_id", "active_since"],
          "properties": {
            "session_id": {"type": "string"},
            "current_focus": {"type": "string"},
            "phase": {"type": "string"},
            "active_since": {"type": "string", "format": "date-time"}
          }
        }
      }
    },
    "topic": {"type": "string"},
    "current_round": {"type": "integer", "minimum": 0},
    "rounds": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["round", "type", "initiator", "artifact_path", "timestamp"],
        "properties": {
          "round": {"type": "integer"},
          "type": {
            "enum": [
              "initial-advice", "counter", "re-sync",
              "decision-lock", "pre-patch", "pre-flight",
              "execute", "verify", "status", "question"
            ]
          },
          "initiator": {"enum": ["advisor", "worker"]},
          "artifact_path": {"type": "string"},
          "timestamp": {"type": "string", "format": "date-time"}
        }
      }
    },
    "open_blockers": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "summary", "raised_by", "raised_in_round", "severity"],
        "properties": {
          "id": {"type": "string"},
          "summary": {"type": "string"},
          "raised_by": {"enum": ["advisor", "worker"]},
          "raised_in_round": {"type": "integer"},
          "severity": {"enum": ["low", "medium", "high", "critical"]},
          "resolution_needed_before": {
            "enum": ["scope-lock", "iterate", "execute", "verify", "close"]
          }
        }
      }
    },
    "decision_log": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["round", "decision", "rationale", "decided_by"],
        "properties": {
          "round": {"type": "integer"},
          "decision": {"type": "string"},
          "rationale": {"type": "string"},
          "decided_by": {"enum": ["user", "consensus"]},
          "alternatives_considered": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "status_observations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["round", "observed_by", "fact", "verified_against"],
        "properties": {
          "round": {"type": "integer"},
          "observed_by": {"enum": ["advisor", "worker"]},
          "fact": {"type": "string"},
          "verified_against": {
            "enum": ["memory", "capability-probe", "filesystem", "transcript", "none"]
          }
        }
      }
    },
    "file_ownership": {
      "type": "object",
      "additionalProperties": {
        "enum": ["advisor", "worker", "shared-readonly"]
      }
    },
    "shared_artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "purpose", "lifecycle_state"],
        "properties": {
          "path": {"type": "string"},
          "purpose": {"type": "string"},
          "lifecycle_state": {
            "enum": ["active", "archived", "superseded"]
          },
          "last_referenced_in_round": {"type": "integer"}
        }
      }
    },
    "wallclock_estimates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["round", "estimated_min"],
        "properties": {
          "round": {"type": "integer"},
          "estimated_min": {"type": "integer"},
          "actual_min": {"type": ["integer", "null"]},
          "drift_factor": {"type": ["number", "null"]}
        }
      }
    },
    "rollback_plan_path": {"type": ["string", "null"]}
  }
}
```

### 4.2 Round-Type-Spezifikation

| Type | Initiator (Author) | Wann | Output-Pflicht |
|---|---|---|---|
| `initial-advice` | advisor | Round 0 nach scope-lock | N Optionen mit Empfehlung |
| `counter` | worker | wenn worker Falsifikation hat | Begründete Falsifikation |
| `re-sync` | advisor | nach counter | Revidiertes Modell |
| `decision-lock` | advisor *oder* worker | nach iterate-Konvergenz, encoded User-Decision via `decided_by: user` im Frontmatter | Entscheidung im decision_log |
| `pre-patch` | advisor | vor execute | Konkrete Patches mit Aufwand-Schätzung |
| `pre-flight` | worker | vor execute | Pre-Flight-Verifikations-Output |
| `execute` | worker | execute-Phase | Step-Verify-Output |
| `verify` | worker | verify-Phase | Smoke-Test-Output |
| `status` | advisor *oder* worker | jederzeit | Status-Snapshot |
| `question` | advisor *oder* worker | jederzeit | Frage mit Kontext |

**Anmerkung:** User ist nie `initiator` einer Round (§3.1: User ist Round-Trigger, nicht Bridge-Teilnehmer). User-Entscheidungen werden encoded via `decided_by: user` im Frontmatter der `decision-lock`-Round.

### 4.3 Handover-Schema (`bridge/handover/<round>-<from>-<to>.md`)

YAML-Frontmatter (Pflicht-validiert) + Markdown-Body:

```yaml
---
pair_id: <uuid>
round: <integer>
from: advisor|worker
to: advisor|worker
type: <round-type aus 4.2>
timestamp: <ISO-8601>

worker_phase: <string>          # PFLICHT (D1)
worker_focus: <string>          # PFLICHT (D1)
status_verified_at: <ISO-8601>  # PFLICHT (D1)

references:                     # PFLICHT mind. 1 Eintrag (D2)
  - type: transcript|memory|capability-probe|filesystem|shared-artifact
    pointer: <string>
    verified: true|false

related_blockers: [B-1, B-2]
related_decisions: [D-1]

acceptance_criteria:            # PFLICHT bei type in {pre-patch, execute, verify} (D6)
  - <string>

rollback_triggers:              # PFLICHT bei type in {execute} (D6)
  - condition: <string>
    action: <string>

wallclock_estimate_min: <integer>  # PFLICHT bei type in {pre-patch, execute} (D4)
---

# Body Sections (Empfehlung, nicht Pflicht-Schema)

## Zusammenfassung
## Konkrete Empfehlung / Frage / Status
## Wall-Clock-Schätzung mit Bottleneck-Marker
## Cross-Refs
```

JSON-Schema-Datei: `plugin/schemas/handover_frontmatter_v1.json`.

---

## 5. Lifecycle-Operationen

### 5.1 `init`

Auslöser: User-Prompt `/bridge-init` in einer Session (Initiator-Session).

Ablauf:
1. Initiator-Session generiert `pair_id` (UUID).
2. Schreibt `bridge/state.json` mit `phase=init`, eigene Rolle gefüllt, andere Rolle als Placeholder.
3. Initiator-Session präsentiert User folgende Info: "Pair-ID: X. Andere Session muss `/bridge-attach <pair_id>` ausführen."
4. Bei `/bridge-attach`-Aufruf in zweiter Session: ergänzt eigene Rolle, setzt `phase=scope-lock`.

### 5.2 `scope-lock`

Auslöser: Phase-Übergang nach `init`.

Ablauf:
1. Beide Sessions schreiben Status-Snapshot via `/bridge-handover --type=status`.
2. Advisor schreibt erste handover-Datei vom Typ `initial-advice` mit IN/OUT-Scope-Vorschlag + Acceptance-Kriterien.
3. Phase wechselt zu `iterate`.

### 5.3 `iterate`

Round-Loop bis `decision-lock`.

Pflicht pro Round:
- Status-Snapshot validiert (FM-1)
- references[] ≥ 1 (FM-3)
- ggf. acceptance_criteria, ggf. rollback_triggers

### 5.4 `execute`

Auslöser: nach `decision-lock` mit anschließendem `pre-patch` + `pre-flight`.

Ablauf:
1. Worker führt Pre-Flight aus, dokumentiert in handover type=`pre-flight`.
2. Bei FAIL: zurück zu `iterate`.
3. Bei PASS: Worker führt Plan-Schritte aus, dokumentiert pro Schritt in handover type=`execute`.

### 5.5 `verify`

Smoke-Test + Akzeptanz-Verifikation. Worker schreibt handover type=`verify` mit Test-Output.

### 5.6 `close`

Auslöser: User-Prompt `/bridge-close <pair_id> --bilanz=<path>`.

Ablauf:
1. Setzt `phase=close`, schreibt Bilanz-Datei in `bridge/bilanz_<pair_id>.md`.
2. Markiert alle `shared_artifacts` als `archived` falls nicht explizit `active`.
3. Aktualisiert `wallclock_estimates[].actual_min` + `drift_factor` für jede Round (post-hoc-Kalibrierung, D4).

---

## 6. Conflict-Resolution

### 6.1 Status-Konflikt

**Symptom:** Advisor's Annahme über Worker-Phase weicht von Worker-Status-Snapshot ab.

**Resolution:**
1. Worker's eigener Status-Snapshot ist authoritativ wenn `verified_against` ∈ {`filesystem`, `capability-probe`}.
2. Advisor's Annahme via `transcript`-Verification ist nachrangig.
3. Memory-Refs sind Tiebreaker NUR wenn explizit referenziert UND Datum < 7 Tage.

### 6.2 Decision-Konflikt

**Symptom:** Advisor empfiehlt X, Worker führt Y aus ohne Counter-Round.

**Resolution:** Bridge erzwingt `counter`-Round vor `execute`. Worker darf nicht direkt von `iterate` zu `execute` ohne `decision-lock` mit User-Bestätigung.

### 6.3 File-Ownership-Konflikt

**Symptom:** Beide Sessions edit gleicher File.

**Resolution:** `file_ownership`-Map in state.json ist Pre-Lock. Bei Konflikt: Pre-Tool-Use-Hook (Phase 2 Plugin-Erweiterung, NICHT MVP) blockiert.

### 6.4 Wall-Clock-Drift

**Symptom:** Estimate vs Actual driftet.

**Resolution:** `drift_factor` wird in `close` geloggt. Bridge-Plugin liest historische `drift_factor`-Werte als Selbst-Kalibrierung (Phase 2 Feature).

---

## 7. Constraints

| ID | Constraint | Begründung |
|---|---|---|
| C1 | Polling-Only | Plattform-Limitation: kein IPC zwischen Cowork-Sessions |
| C2 | Read-Only-Cross-Session | `session_info` MCP API |
| C3 | Shared-Filesystem-Pflicht | Beide Sessions müssen mind. einen gemeinsamen Project-Mount haben |
| C4 | User-Mediated-Rounds | Sessions reagieren nur auf User-Input oder eigene Tool-Loops |
| C5 | Memory-Reference-Authority bedingt | Memory ist Tiebreaker nur wenn explizit + frisch |
| C6 | Status-Snapshot-Required pro Handover | FM-1 Strukturelle Verhinderung |
| C7 | Wall-Clock-Cost-Model bekannt | Self-Edit ~1-5min, Subagent ~25-50min FEST, User variabel |

---

## 8. Alternatives Considered

### 8.1 `agent-teams`-Plugin nutzen

**Verworfen.** `agent-teams` orchestriert parent→child-Spawning innerhalb einer Session. Zwei User-Cowork-Sessions sind Peers, keine Parent-Child-Relation. Tools sind unterschiedlich (parent kann nicht Worker's Tools dispatchen).

### 8.2 Manuelle Coordination ohne Plugin

**Verworfen.** Empirisch fragil — siehe 9 Failure-Modes im Korpus. Pro Pairing müssen Schema, Lifecycle, Rollback neu erfunden werden.

### 8.3 Push-basierte Bridge via Webhooks

**Verworfen.** Plattform unterstützt keinen Push zwischen Cowork-Sessions. Webhook-Server außerhalb Cowork wäre zusätzliche Infrastruktur, gegen Plugin-Self-Contained-Prinzip.

### 8.4 N-Pair-Topologie (>2 Sessions)

**Deferred.** Topologisch komplexer (Konsens-Probleme bei N≥3). MVP fokussiert 2-Pair.

### 8.5 Auto-Trigger-Hooks

**Deferred.** Pre-Tool-Use-Hooks für `[BRIDGE-CRITICAL]`-Tag erhöht Komplexität. MVP ist polling-only mit User-mediierten Rounds.

---

## 9. Consequences

### 9.1 Positiv

- Wiederverwendbares Pattern für N zukünftige Pairings.
- Strukturelle Verhinderung von 9 empirisch dokumentierten Failure-Modes.
- Lifecycle-Tracking verhindert Beratungs-Drift.
- Wall-Clock-Drift-Logging ermöglicht Selbst-Kalibrierung der Schätz-Heuristik.

### 9.2 Negativ

- Polling-Latenz: User muss in beiden Sessions aktiv prompten.
- Schema-Lock-Risiko: Schema-Drift bei zukünftigen Round-Typen erfordert breaking-change-Migration.
- Plattform-Bindung: Bricht wenn `session_info`-MCP API ändert.

### 9.3 Operational

- Plugin-Repo: `~/session-bridge/` (eigenes Repo, nicht in domain-spezifischem Plugin).
- Plugin-Manifest: separates Plugin, kein Dependency auf andere Plugins.
- Distribution: post-MVP via lokales Plugin-Install, später ggf. Marketplace.

---

## 10. Acceptance-Kriterien

### 10.1 ADR-Lock-Akzeptanz (Phase 3)

| # | Kriterium | Verifikation |
|---|---|---|
| A1 | State-Schema im ADR §4.1 inline vollständig | Manuelle Inspektion + jsonschema-Syntax-Check |
| A2 | Handover-Frontmatter-Schema im ADR §4.3 inline vollständig | Manuelle Inspektion |
| A3 | 10 Round-Typen encoded (8 procedural + 2 utility) | Enum-Konsistenz §3.3 ↔ §4.2 ↔ State-Schema |
| A4 | 9 Failure-Modes mit Driver-Mapping (D1-D10) | FM-Mapping in §2 Drivers nachweisbar |
| A5 | Lifecycle 6 Phasen + Übergänge spezifiziert | §5 vollständig |
| A6 | Conflict-Resolution für 4 Konflikt-Typen | §6 vollständig |
| A7 | Constraints C1-C7 explizit | §7 vollständig |
| A8 | ≥5 Alternativen mit Begründung (verworfen ODER deferred) | §8 vollständig |
| A9 | Concurrency-Mechanismus + Schema-Versionierung spezifiziert | §13 vollständig |

### 10.2 Plugin-MVP-Akzeptanz (Phase 4)

| # | Kriterium | Verifikation |
|---|---|---|
| M1 | `plugin/schemas/bridge_state_v1.json` existiert + jsonschema-validate | Validator-Lauf |
| M2 | `plugin/schemas/handover_frontmatter_v1.json` existiert + jsonschema-validate | Validator-Lauf |
| M3 | Skills `bridge-advisor` + `bridge-worker` lauffähig | Smoke-Test in Phase 5 |
| M4 | Commands `/bridge-init`, `/bridge-attach`, `/bridge-handover`, `/bridge-status`, `/bridge-close` lauffähig | Smoke-Test in Phase 5 |
| M5 | `claude plugin validate` PASS | Validator-Lauf |
| M6 | Synthetischer Pilot Round 0..6 PASS | Phase 5 Pilot-Test |

---

## 11. Open Questions

| OQ-ID | Frage | Klärung |
|---|---|---|
| OQ-1 | Wie wird `pair_id` zwischen Sessions kommuniziert? | User kopiert manuell aus `/bridge-init`-Output zu `/bridge-attach`. Auto-Discovery via Filesystem-Scan wäre Phase-2-Erweiterung. |
| OQ-2 | Was passiert bei `session_info`-MCP-Ausfall? | Bridge degraded: handover ohne transcript-Verifikation; alle `references[].verified=false`; advisor-Quality reduziert auf User-mediated-Snapshots. |
| OQ-3 | `pair_id`-Kollision bei neuem Pair? | UUIDv4-Kollisions-Wahrscheinlichkeit negligible. Bei dennoch eintretender Kollision: state.json hat `created_at` als Tiebreaker. |
| OQ-5 | Soll `close` automatisch Memory-Persist auslösen? | Deferred. MVP: User triggert separat via `consolidate-memory`. |
| OQ-6 | Wie wird `bridge/`-Subdirectory zwischen Sessions geteilt wenn beide auf verschiedene Cowork-Projects mounten? | C3 erzwingt mind. einen gemeinsamen Mount. Plugin-Convention: `bridge/` lebt im **gemeinsam mountbaren** Project. Default-Konvention: `<gemeinsam-mountbarer-pfad>/bridge/`. `/bridge-init` validiert Existenz dieses Pfads vor State-File-Anlage. |

---

## 12. References

- CORPUS_ANALYSIS: `../pattern-mining/CORPUS_ANALYSIS.md`
- Prior-Art `agent-teams`: Peer-Plugin, anderes Modell
- `session_info`-MCP: read-Backbone
- Auto-Memory `feedback_self_edit_fallback.md`: Wall-Clock-Cost-Model (C7)
- Auto-Memory `feedback_git_host_mcp.md`: Filesystem-Authority-Pattern (D10)

---

## 13. Schema-Versioning & Concurrency

### 13.1 Schema-Versioning

State-Schema und Handover-Schema tragen explizit `schema_version` Feld. Aktuell `1.0`.

**Bump-Regeln:**

- **Patch-Bump (1.0 → 1.0.1):** Backwards-kompatible Erweiterung (neue optionale Felder). Keine Migration nötig.
- **Minor-Bump (1.0 → 1.1):** Neue Pflicht-Felder mit Default. Auto-Migration via `core/migrate_state_v1_0_to_v1_1.py`.
- **Major-Bump (1.0 → 2.0):** Breaking Change (Feld entfernt, Enum-Wert entfernt). Pflicht-Migration-Skript + Deprecation-Phase ≥30 Tage. Pair-Closing ist Pflicht vor Major-Bump.

**Migration-Pflicht:** Plugin liefert Migration-Skripte für jeden Minor/Major-Bump. State-Files mit veraltetem `schema_version` werden vor Lese-Zugriff migriert (in-place via temp-File + atomic-rename).

### 13.2 Concurrency-Mechanismus

**Atomic-Write-Pattern (alle Schreib-Operationen auf state.json):**

```
1. Read state.json → state_dict
2. Validate state_dict gegen schema (jsonschema)
3. Mutate state_dict (lokal in-memory)
4. Write state.json.tmp.<uuid> mit neuem state_dict
5. Atomic rename state.json.tmp.<uuid> → state.json
```

**Optimistic-Locking via `updated_at`-Field:**

```
1. read_at = read state.json["updated_at"]
2. mutate
3. compare-and-swap: rename nur wenn current state.json["updated_at"] == read_at
4. Bei CAS-Failure: re-read + re-mutate (max 3 retries)
```

**Round-Counter-Atomicity:**

`current_round` wird ausschließlich beim Append zu `rounds[]`-Array atomar inkrementiert. Plugin-Code-Pflicht: NIE `current_round` ohne entsprechenden `rounds[]`-Append schreiben.

**Handover-File-Naming:**

Format: `<round>-<from>-<to>-<short-uuid>.md` wo `short-uuid` 8 Zeichen UUID4. Eindeutigkeit: garantiert auch bei race-Conditions zwischen zwei Sessions (sehr seltener Edge-Case bei gleichzeitigem Schreiben).

### 13.3 Failure-Recovery

**Crash während Write:**

- `state.json.tmp.<uuid>` bleibt liegen → Plugin-Init prüft + räumt auf.
- `state.json` ist atomic (rename ist POSIX-atomic auf gleichem Filesystem).

**Session stirbt mid-Round:**

- handover-File ist `complete` falls atomic-rename gelungen, sonst inkomplett liegengelassen.
- Plugin-Init prüft handover/-Dir gegen rounds[]-Array; orphane handover-Files werden in `bridge/orphans/` archiviert.

**Diverging State (zwei Sessions schrieben parallel ohne CAS):**

- Bei CAS-Failure ist Recovery automatisch (re-read + re-mutate).
- Bei manueller Korruption: `bridge/state.json.bak.<timestamp>` wird vor jedem Write angelegt (Pre-Atomic-Write-Step).

---

**Lock-Status:** LOCKED. A1-A9 PASS verifiziert 2026-04-26. Phase 4 (MVP-Plugin-Scaffold) freigegeben. Schema-Bumps ab hier nur via §13.1-Bump-Regeln.


---

## Annex B — Bilanz-Filename-Konvention + Schema-Pointer (NEU v0.1.5 / ADR_0031 §4.4)

**Empirie aus Bridge-Pair p3-real-user (closed 2026-04-29) + Cross-Pair-Analyse p4/p5/p6 (ADR_0031):**

ADR_0029 §5.6 erwähnt Bilanz-Datei in close-Phase ohne Filename-Konvention oder Schema-Pointer. Empirie zeigte zwei verschiedene Naming-Patterns:

| Pair | Bilanz-Filename |
|---|---|
| p3-real-user | `bridge/bilanz_8cbeaad0.md` (mit Pair-ID-Suffix) |
| p4-eg-dev | `bridge/BILANZ.md` (uppercase, kein Suffix) |

**Decision:** ab v0.1.5 ist die Filename-Konvention `bridge/bilanz_<pair_id>.md` (analog state.json + handover-Files mit Pair-ID-Suffix für Cross-Pair-Eindeutigkeit).

**Schema-Pointer:** Bilanz-File-Inhalt MUSS `schemas/bilanz_v1.json` (NEU v0.1.4 PB-001) folgen. Pflicht-Sektionen:
- pair_id, pair_topic, created_at, closed_at
- total_rounds, phase_sequence, decision_log_summary
- wallclock_drift_calibrated
- reflection (mit Pflicht-Sub-Feldern was_funktionierte / was_problematisch / was_als_naechstes)
- successful_patterns, anti_patterns_detected, cross_pair_transfer_hinweise

**Empirie-Anker:** `pilot-runs/p3-real-user/bridge/bilanz_8cbeaad0.md` als Reference-Implementation (12-Sektionen-Schema-strikt, Stufe-7-Konsolidierung).

**Migration:**
- p4-BILANZ als Migration-Kandidat (rename + Schema-konform machen) — v0.1.5 Phase H (optional, nicht hard-enforced für historische Pairs)
- bridge-close-Skill v0.1.5 enforced bilanz_v1-Schema bei Generierung neuer Bilanzen

**Cross-Refs:**
- ADR_0031 §4.3 + §4.4 (Decision-Source)
- schemas/bilanz_v1.json (Schema-Spec)
- pilot-runs/p3-real-user/bridge/bilanz_8cbeaad0.md (Reference-Implementation)
- pilot-runs/p4-eg-dev/bridge/BILANZ.md (Migration-Kandidat)

---

## Annex C — Cross-Pair-Empirie-Konsolidierung post-v0.1.8 (NEU v0.1.9, 2026-05-05)

**Status:** LOCKED 2026-05-05 als Teil v0.1.9 Empirie-driven-Patches
**Trigger:** 5 Bridge-Pairs seit v0.1.7 (p6/p7-praxis/p7-klafki/p8/p9) liefern empirische Substanz für Plugin-Optimierung. Konsolidierung als ADR-Annex.

### C.1 Pair-Inventar post-v0.1.7

| Pair | Topic | Domain | Rounds | Status | Wichtigste Patterns |
|---|---|---|---|---|---|
| p6-upp-eg-advice | escape-game-generator-Beratung | use-case | aktiv | many artifacts | Tooling-Effizienz-Cycles |
| p7-klafki-validation | Klafki-Profile-Validation | use-case-with-profile | 8 | close-prep | 9 DLs, F-Cluster F1.1+F2.1+F4.1+F4.2+F5.1+F6.1 aktiviert |
| p7-upp-praxis-validation | UPP-Plugin-Live-Test | use-case | 16+1 | finalisiert | 26 Findings + 14 Patterns + 16 NEU-Tracks |
| p8-self-sustained-ux | Spec-Patch v0.5.4 | use-case | 10 | close-prep | drift 0.05 (Best-Performer), Pre-Flight-Vorlage-Pattern |
| p9-klafki-ue-eval | Klafki UE-Eval | use-case-with-profile | 3 | aktiv (kurz) | (in Bewegung) |

### C.2 Drift-Faktor-Empirie für DRIFT_RANGES-Update

| Pair | RT | drift_factor | Trigger-Mechanik |
|---|---|---|---|
| p4 RT-4 | 0.10 | 3-File-Diff-Self-Audit + jq-Aggregation Subagent-Pattern |
| p5 RT-2 | 0.21 | Spec-Schreibung in-place-Edit-Modus |
| p7-praxis RT-2 | 0.23 | Spec-Patch-Schreibung Pre-Vorarbeit-Reuse |
| p8 RT-1 | 0.05 | 3-Patch-Lokationen-Sequential-Edit + Pre-Flight-Vorlage-Reuse |

**4 erfolgreiche Self-Disclosure-Tooling-Effizienz-Pattern-Cycles.**

**Decision:** DRIFT_RANGES["use-case"] empirisch updated zu min=0.05/max=2.0/stddev=0.4 (v0.1.9 tools/bridge_state.py). RATIO_THRESHOLDS["use-case-with-profile"] bleibt 5.0, jetzt mit n=2-Empirie statt n=0.

### C.3 Profile-Pin-Empirie (Klafki-Validation p7)

p7-klafki-validation produzierte 9 Decision-Locks in 8 Rounds (1.1 DL/Round) mit allen 6 Klafki-Frame-Cluster aktiviert: F1.1 (DL-K03 maximal), F2.1 (DL-K03), F4.1 (DL-K02a/b/c+K04), F4.2 (DL-K04), F5.1 (DL-K06), F6.1 (DL-K06).

**Empirisch:** Klafki-Profile-Pin-Mechanik (ADR_0030) funktioniert + produziert substantielle Validation-Empirie. **Profile-Adoption-Argument empirisch belegt.**

### C.4 Patterns mit Bridge-Plugin-Implikation

5 Patterns aus p7-upp-praxis-validation mit direkter Bridge-Plugin-Relevanz:

- **Pattern-#76+#77+#80 (Cowork-Mode-Reading-Pattern):** bridge-advisor + bridge-worker SKILL.md sind Reading-Pattern-Skills, NICHT Auto-Pipeline → §Cowork-Mode-Composition-Header in beiden SKILL-Files (v0.1.9)
- **Pattern-#82 (Lehrkraft-Realbedingungen-Validation-Pflicht):** Worker-Bilanz allein reicht nicht → user_validation_required-Marker (deferred v0.1.10)
- **Pattern-#88 (Phase-Gate-Audit-vor-Phase-Transition):** p7-R6→R8 ohne Gate-Audit produzierte 4 CRITICAL-Findings unentdeckt → §Phase-Gate-Audit-Pflicht in advisor + Spiegel in worker SKILL.md (v0.1.9)
- **Pattern-#89 (User-Methodik-Veto-Authority):** p7-R10→R11 Worker-Patches durch User-Veto verworfen → §User-Veto-Authority-Sektion in worker SKILL.md (v0.1.9), Schema-Update deferred v0.1.10

### C.5 L-p8-01-Pattern (Pre-Flight-Vorlage-Vollständigkeit)

p8 erreichte drift 0.05 durch: Pre-Flight-Patch-Plan-Vorlage in Round 3+4 (3 Edit-Lokationen + 9 ACs + Inhalt-Skelette vollständig vor execute) → Round 5 execute war reine Edit-Sequenz.

**Empirisch:** v0.1.8 Pre-Flight Phase A entspricht diesem Pattern für /bridge-init + /bridge-attach. L-p8-01 ist methodische Validierung von v0.1.8.

### C.6 Cross-Pair-Pause/Resume-Pattern (deferred v0.2.0)

p6 paused-for-praxis-validation-p7 → p6 resume nach p7-Closure. **Decision:** state.phase-Enum braucht "paused"/"resumed"-Werte. v0.2.0 mit Multi-Pair-Topologie (PB-005) zusammen designen.

### C.7 v0.1.9-Patches abgeleitet aus Empirie

| Patch-ID | Patch | Empirie-Quelle |
|---|---|---|
| 9-A | bridge-advisor §Phase-Gate-Audit-Pflicht | Pattern-#88 (p7-praxis R16) |
| 9-B | bridge-advisor + bridge-worker §Cowork-Mode-Composition-Header | Pattern-#76+#77+#80 (p7-praxis R5) |
| 9-B' | bridge-worker §User-Veto-Authority + §Phase-Gate-Spiegel | Pattern-#89 + Pattern-#88 (Spiegel) |
| 9-C | DRIFT_RANGES["use-case"] empirisch update | p4/5/7-praxis/8-Empirie n=4 |
| 9-D | Diese Annex C | Konsolidierungs-Pflicht |
| 9-E | Smoke-Tests T68-T70 | Test-Coverage |

### C.8 v0.1.10+ Deferred Patches aus Empirie

| Patch | Empirie-Quelle | Begründung Deferred |
|---|---|---|
| user_veto_log-Schema-Field | Pattern-#89 | Schema-Bump, braucht mehr Empirie zu Field-Struktur |
| Pause/Resume-state.phase-Enum | Cross-Pair p6/p7 | mit Multi-Pair-Topologie v0.2.0 |
| user-validation-Round-Type NEU | Pattern-#82 | Use-Case-Test-Bedarf |
| bilanz_v1.json tooling-cycles-Field | p4-p8 Drift-Pattern-Cycles | additive Erweiterung |

### C.9 Cross-Refs

- pilot-runs/p7-upp-praxis-validation/bridge/artifacts/praxis_validation_befunde.md (Quell-Befund §9.7+§9.8)
- pilot-runs/p7-klafki-validation/bridge/BILANZ.md (Profile-Pin-Empirie)
- pilot-runs/p8-self-sustained-ux/bridge/BILANZ.md (drift 0.05 Best-Performer + L-p8-01)
- ADR_0030 Annex D (v0.1.8 Pre-Flight-Auto-Resolution = L-p8-01-Implementation)
- ADR_0031 §3+§4 (Cross-Pair-Patterns Source-Document)
- tools/bridge_state.py DRIFT_RANGES + RATIO_THRESHOLDS (v0.1.9 update)
- skills/bridge-advisor/SKILL.md §Phase-Gate-Audit-Pflicht + §Cowork-Mode-Composition (v0.1.9 NEU)
- skills/bridge-worker/SKILL.md §Phase-Gate-Spiegel + §User-Veto-Authority + §Cowork-Mode-Composition (v0.1.9 NEU)

---

## Annex D — Cross-Pair-Empirie-Konsolidierung post-v0.1.9 (NEU v0.1.10, 2026-05-09)

**Status:** LOCKED 2026-05-09 als Teil v0.1.10 Empirie-driven-Patches Round 2
**Trigger:** 3 neue Pairs seit v0.1.9 (p10/p11/p12) + p6-BILANZ ausgewertet liefern weitere empirische Substanz. Pattern-#103 Memory-Symmetrie etabliert sich als Pflicht-Workflow (n=4). Cross-Project-Bridge p11 als 1. Empirie-Datenpunkt für neue Domain-Klasse.

### D.1 Pair-Inventar post-v0.1.9

| Pair | Topic | Domain | Rounds | Status | Wichtigste Patterns |
|---|---|---|---|---|---|
| p10-phase1a-foundation-audit | Phase-1A Foundation-Audit (process-consulting Profile aktiv) | architecture-spec | 6 | closed | Pattern-#109 HYPOTHESE Drift-Korridor-Track-Typ + Iteration-Cycle-4-Round-Pattern + Memory-Symmetrie |
| p11-eg-schsch-architektur-import | Cross-Project-Persona-Pipeline-Import UPP→EG | architecture-spec (cross-project) | 11 | closed | **1. Cross-Project-Bridge** + Source-of-Truth-Lock + Anti-Drift-#6 + drift 0.27-0.41 |
| p12-eg-r5-spec-patch | EG-R5-Spec-Patch P0-Implementation-Substanz | architecture-spec-patch | 0 | active (init) | (in Bewegung, kein Pattern noch) |

### D.2 Pattern-#103 Memory-Cross-Session-Symmetrie als Pflicht-Workflow

**Empirie:** 4 von 5 closed-Pairs haben Memory-Symmetrie als Out-of-Bridge-Task (p6/p7-klafki/p10/p11). Pattern empirisch konsolidiert n=4 — Pflicht-Workflow gerechtfertigt.

**Decision:** v0.1.10 erweitert bridge-close.md §Memory-Symmetrie-Pflicht-Workflow:
- Memory-Plan-Generierung aus BILANZ-Substanz (2-4 Items pro Session)
- §Memory-Symmetrie-Plan-Block in BILANZ.md
- state.json `memory_symmetry_status`-Field (pending/partial/complete/skipped)
- Pre-Init-WARN bei nächstem Pair wenn vorheriger Pair `!= complete`

**Symmetrie-Definition:**
- Komplementär (nicht identisch): advisor speichert Methodik, worker speichert Operative-Empirie
- Beide speichern Project-Snapshot + Cross-Pair-Pointer
- Asynchron persistiert (kein gleichzeitiges Locking)
- Plugin kann nicht hard-erzwingen — nur dokumentieren + erinnern

### D.3 Cross-Project-Bridge als domain-Subtype

**Empirie p11 (n=1, HYPOTHESE):** Cross-Project-Bridges haben strukturell andere Drift-Range (~+50% Aufschlag sup-Single-Project).

**Decision v0.1.10:**
- bridge_state_v1.json topic_metadata.domain_hint-Enum erweitert um `cross-project`
- DRIFT_RANGES["cross-project"] = {min:0.20, max:0.5, stddev:0.1}
- RATIO_THRESHOLDS["cross-project"] = 6.0 (höher wegen counter+counter-disposition für Cross-Project-Komplexität)
- Plus: `architecture-spec-patch` als Subtype (p8/p12 Empirie)
- Plus: `use-case-with-profile` jetzt explizit als enum-Wert (vorher nur in DRIFT_RANGES)

### D.4 Source-of-Truth-Lock-Field im handover-Schema

**Empirie p11-R4-02:** UGG-Skizze hatte K-Index-Drift gegenüber operativer r_rl_sketch+ADR_0046-Definition. Source-of-Truth-Lock in Round-4-counter-disposition verhinderte Spec-Patch-Korruption.

**Decision v0.1.10:** handover_frontmatter_v1.json optional `source_of_truth_locked`-Array:
```yaml
source_of_truth_locked:
  - ref: "ADR_0046 K-Komponenten-Definition"
    at_round: 4
    reason: "UGG-Skizze K-Index-Drift gegenueber operativer Definition"
    drift_against: "UGG-Skizze §2.3 K3+K4 vertauscht"
```

Anti-Drift-#6 Cross-Project-Konsistenz wird via dieses Field strukturell sichtbar.

### D.5 Pattern-#109 Track-Type-Differenzierung (Re-Klassifikations-Vorbereitung)

**Empirie p10 (n=2, HYPOTHESE):** Schema/Doku/Validator-Tracks deutlich-unter-Korridor 0.6-1.4 (drift 0.04-0.06). Re-Klassifikations-Trigger HYPOTHESE→VALIDE: ≥3 diverse Empirie-Datenpunkte pro Track-Typ.

**Decision v0.1.10:** tools/bridge_state.py neue Konstante `TRACK_TYPE_DRIFT_EMPIRIE`:
- schema/doku/validator: HYPOTHESE n=1 mit Korridor [0.6, 1.4]
- spec-patch: VALIDE n=4 (p4/p5/p7/p8/p9) mit Range [0.05, 0.5]
- code: UNGETESTET n=0
- Empirie-Sammlung weiter pro Pair-DONE → Re-Klassifikations-Trigger bei n≥3 pro Track-Typ

### D.6 Iteration-Cycle-4-Round-Pattern (p10-Empirie)

**Pattern (etabliert in p10):** counter → decision-lock → iteration-cycle → verify (4 Rounds für Audit-Cycle).

p10 Round-Sequenz: R1 initial-advice → R2 counter-mit-acknowledge-und-iteration-plan → R3 decision-lock → R4 worker iteration-cycle (9/9 Items DONE) → R5 advisor verify → R6 close.

**Empirie:** Iteration-Cycle 9/9 Items DONE in 1.4h Wallclock vs Forecast 4.4d → Drift 0.04-0.06. Pattern-#82-Realbedingungen-Validation erfüllt + AD.1A.12-Pflicht-Self-Audit.

**Status:** Bridge-Best-Practice. Nicht hard-codiert in Skill, aber als Reference-Implementation in ADR-Annex dokumentiert.

### D.7 Long-Pair-Pattern (p6 mit 56 Rounds)

p6-upp-eg-advice mit 56 Rounds + 24 Konsensus-Locks differenziert von Decision-Locks. Empirie n=1 — kein hard-WARN-Pattern, aber Vermerk: bei sehr langen Pairs könnte Memory-Symmetrie multi-step erfolgen (Mid-Pair-Memory-Snapshots).

**Deferred v0.1.11+:** Mid-Pair-Memory-Snapshot-Pattern wenn n≥2 Long-Pairs.

### D.8 5. Tooling-Effizienz-Pattern-Cycle bestätigt

| Pair | RT | Drift | Trigger-Mechanik |
|---|---|---|---|
| p4 RT-4 | 0.10 | 3-File-Diff-Self-Audit + jq-Aggregation Subagent-Pattern |
| p5 RT-2 | 0.21 | Spec-Schreibung in-place-Edit-Modus |
| p7-praxis RT-2 | 0.23 | Spec-Patch-Schreibung Pre-Vorarbeit-Reuse |
| p8 RT-1 | 0.05 | Pre-Flight-Vorlage-Reuse + Briefing-Inhalt-Vorlage |
| p9 (=p11) RT-1 | 0.09 | Cross-Project-Pattern-Konsolidierung + Pre-Flight-Vorlage-Reuse + Klafki-Synthese-Volltext-Inline-Reuse |

**5 erfolgreiche Self-Disclosure-Cycles** = stable empirie. Methodologie verfestigt.

### D.9 v0.1.10-Patches abgeleitet aus Empirie

| Patch-ID | Patch | Empirie-Quelle |
|---|---|---|
| 10-A | bridge-close §Memory-Symmetrie-Pflicht-Workflow (Pattern-#103) + state.memory_symmetry_status | p6+p7-klafki+p10+p11 (n=4) |
| 10-B | bridge_state_v1 domain_hint cross-project + architecture-spec-patch + use-case-with-profile | p11 (n=1) + p8/p12 + Klafki-Pairs |
| 10-B' | DRIFT_RANGES["cross-project"] + ["architecture-spec"] + RATIO_THRESHOLDS["cross-project"] | p4-p11-Empirie |
| 10-C | handover_frontmatter_v1 source_of_truth_locked-Field | p11-R4-02 (n=1) |
| 10-D | tools/bridge_state TRACK_TYPE_DRIFT_EMPIRIE-Konstante (Pattern-#109 Tracking) | p10 (n=2 HYPOTHESE) |
| 10-E | Diese Annex D | Konsolidierungs-Pflicht |

### D.10 v0.1.11+ Deferred Patches

| Patch | Empirie-Quelle | Begründung Deferred |
|---|---|---|
| Long-Pair-WARN bei Round-Counter > 30 | p6 (n=1) | mehr Long-Pair-Empirie nötig |
| Mid-Pair-Memory-Snapshot-Pattern | p6 (n=1) | mit Long-Pair-Pattern zusammen |
| bilanz_v1 cross_project_metadata-Field | p11 (n=1) | additive Erweiterung, low-Priorität |
| Konsensus-Lock vs Decision-Lock-Differenzierung | p6 (n=1) | n=1 Empirie zu schwach |
| AD.1A-Konstanten als Profile-Style-Header | p10 process-consulting | v0.2.0 |

### D.11 Cross-Refs

- pilot-runs/p10-phase1a-foundation-audit/bridge/BILANZ.md (Iteration-Cycle-Pattern + Pattern-#109 + Memory-Symmetrie §10)
- pilot-runs/p11-eg-schsch-architektur-import/bridge/BILANZ.md (Cross-Project-Bridge + Source-of-Truth-Lock + Anti-Drift-#6)
- pilot-runs/p6-upp-eg-advice/bridge/BILANZ.md (Long-Pair + 56 Rounds + Pattern-#103-Memory)
- ADR_0029 Annex C v0.1.9 (Pre-Patch-Empirie post-v0.1.8)
- ADR_0030 Annex D v0.1.8 (Pre-Flight-Auto-Resolution = L-p8-01-Implementation)
- ADR_0031 §3+§4 (Cross-Pair-Patterns Source-Document)
- tools/bridge_state.py DRIFT_RANGES + RATIO_THRESHOLDS + TRACK_TYPE_DRIFT_EMPIRIE (v0.1.10 update)
- commands/bridge-close.md §Memory-Symmetrie-Pflicht-Workflow (v0.1.10 NEU)
- schemas/bridge_state_v1.json domain_hint-Enum erweitert + memory_symmetry_status (v0.1.10 NEU)
- schemas/handover_frontmatter_v1.json source_of_truth_locked (v0.1.10 NEU)
