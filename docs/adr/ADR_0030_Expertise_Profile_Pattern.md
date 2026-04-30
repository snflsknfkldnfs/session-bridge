# ADR 0030 — Expertise-Profile-Pattern

**Status:** LOCKED (2026-04-26)
**Datum:** 2026-04-26
**Autor:** session-bridge Plugin-Project
**Kontext:** v0.1.1 Real-User-Pilot empirisch validiert, User-Wunsch nach Domain-Spezialisierung des bridge-advisor (Prozess-/Organisationsberatung als erste Anwendung).

---

## 1. Context

session-bridge v0.1.1 ist ein domain-agnostisches Cross-Session-Coordination-Plugin. Real-User-Pilot 2026-04-26 zeigte funktionalen Bridge-Lifecycle. User signalisiert Bedarf an domain-spezifischer Beratungs-Qualifikation für bridge-advisor — konkret: Prozess-/Organisationsberatung mit ~340 organisationssoziologischen Zettelkasten-Notizen (Kühl, Humanisierung der Organisation, Luhmann) als methodische Basis.

Naive Lösungs-Ansätze sind defekt:
- **Inline in bridge-advisor SKILL.md:** Plugin verliert Generizität, Skill-Description-Drift, kein Reuse für andere Domains
- **Eigenes Plugin pro Domain:** Plugin-Dependency-Mechanik in CC schwach, Doppel-Plugin-Pflege
- **Spec inline in plugin.json:** Schema-Constraint (CC-Validator) limitiert Custom-Felder

→ Architektur muss **Plugin-Generizität bewahren** + **Domain-Expertise als externe Resource-Layer** modellieren.

---

## 2. Drivers

| ID | Driver | Quelle |
|---|---|---|
| D1 | Plugin bleibt domain-agnostisch — Reuse für N Domains skalierbar | session-bridge v0.1.0 MVP-Design |
| D2 | Domain-Expertise als externe, austauschbare Resource | analog zu DiSoAn-Framework / PATA-Standards-Layer aus META_PROZESSE-Korpus |
| D3 | Profile sind self-contained (standalone) — Plugin funktioniert auf jedem Endgerät ohne user-spezifische Vault-Pfade | User-Entscheidung 2026-04-26 |
| D4 | Profile-Schema einheitlich → Multi-Profile-Setup zukunftsfähig | Skalierung |
| D5 | Profile-Loading hat klaren Lifecycle-Punkt (init-time-Lock) — kein per-handover-switching | Vermeidet Mid-Pair-State-Drift |
| D6 | Lizenzrecht-aware: Profile-Inhalt eigenformuliert, Quellen-Verweise statt Reproduktion | User-Datenschutz-/Compliance-Bewusstsein |
| D7 | Datenschutz-Pfad: Profile-Files können in `private-notes/expertise-profiles/` lokal liegen, später opt-in public | analog zu Mining-Notes-Pattern (filter-repo-Cleanup-Erfahrung 2026-04-26) |
| D8 | Versionierung: Profile-Schema-Bump entkoppelt von Plugin-Schema-Bump | Profile evoluieren unabhängig |

---

## 3. Decision

**Wir bauen einen Expertise-Profile-Layer als Schicht-1 über dem bridge-advisor:**

### 3.1 Layer-Modell

```
┌─────────────────────────────────────────┐
│ Plugin-Core (session-bridge)            │ ← Coordination-Backbone (agnostic)
│   bridge-init, bridge-advisor, ...      │
└─────────────────────────────────────────┘
                  ▲
                  │ loads
                  │
┌─────────────────────────────────────────┐
│ Expertise-Profile-Layer                 │ ← Domain-Spezialisierung (extern)
│   expertise-profiles/<profile-name>/    │
│     PROFILE.md (frontmatter + body)     │
│     diagnostic-frames.md                │
│     anti-patterns.md                    │
│     question-bank.md                    │
└─────────────────────────────────────────┘
```

### 3.2 Schema-Erweiterung v1.0.0 → v1.1.0 (Minor-Bump per ADR_0029 §13.1)

`bridge_state_v1.json` erweitert um optionale Felder in `roles.advisor`:

```json
"advisor": {
  "type": "object",
  "required": ["session_id", "active_since"],
  "properties": {
    "session_id": {"type": "string"},
    "expertise_source": {"type": "string"},
    "expertise_profile": {
      "type": ["string", "null"],
      "description": "Relativer Pfad zum Profile-Verzeichnis (z.B. 'expertise-profiles/process-consulting'). Null bei generic advisor."
    },
    "profile_version": {
      "type": ["string", "null"],
      "description": "Version des geladenen Profile, gepinnt zum init-Zeitpunkt"
    },
    "active_since": {"type": "string", "format": "date-time"}
  }
}
```

`schema_version` springt auf `1.1.0`. Migration-Skript `core/migrate_state_v1_0_0_to_v1_1_0.py` (sentinel-fields-add).

### 3.3 Profile-Schema (`PROFILE.md` Frontmatter)

```yaml
---
profile_name: <kebab-case-name>
profile_version: <semver>
profile_schema_version: 1.0.0
domain: <string>                                    # z.B. "organizational-consulting"
methodology_pillars: [<string>, ...]                # Methodik-Säulen, frei
sources:                                            # Quellen-Zitations-Anker
  - <author> (<year>): <work>
trigger_phrases:                                    # zusätzliche advisor-Trigger
  - <phrase>
pflicht_workflows:                                  # Domain-Workflows die advisor-Skill ausführen muss
  - <workflow-id>
linkage_to_bridge_rounds:                           # round-type → workflow-modifier
  initial-advice: <string>
  counter: <string>
  re-sync: <string>
  decision-lock: <string>
  pre-patch: <string>
required_files:                                     # Profile-Dateien-Pflicht
  - PROFILE.md
  - diagnostic-frames.md
  - anti-patterns.md
  - question-bank.md
---

# <Profile-Name>
<Methodik-Sockel-Text in eigenformulierter Sprache>
```

### 3.4 Loading-Lifecycle

- **init-time-Lock:** Profile wird beim `/bridge-init --expertise-profile=<path>` geladen, Pfad in `state.json:roles.advisor.expertise_profile` gepinnt. **Kein per-handover-switching** (Anti-Drift).
- **Profile-Validation beim Init:** alle 4 required_files existieren, frontmatter parsebar, profile_schema_version supported.
- **Bei jedem advisor-Skill-Trigger:** Profile-Frontmatter + Body-Files lesen, Pflicht-Workflows in Skill-Pflicht-Workflow-Sequenz integrieren.
- **Profile-Updates während Pair-Lifecycle:** verboten. Profile-Pin via init zementiert Methodik für gesamte Pair-Dauer.

### 3.5 Standalone-Pflicht

Profile-Dateien sind self-contained. **Keine externen Vault-Links, keine absolute User-Pfade.** Plugin funktioniert auf jedem Endgerät ohne User-spezifische Mounts.

Ableitung: Curation muss Profile-Inhalte als **eigenformulierte didaktische Reduktion** mit Quellen-Verweisen erzeugen, NICHT als Vault-Zettel-Aggregation.

---

## 4. Profile-Verzeichnis-Konvention

### 4.1 Pfad-Optionen

| Pfad | Visibility | Use-Case |
|---|---|---|
| `<plugin-repo>/expertise-profiles/<name>/` | public (mit Plugin) | Generic Profiles für Community |
| `private-notes/expertise-profiles/<name>/` | lokal, .gitignored | User-spezifische Profiles, Pre-Publication-Stage |
| `<separates-repo>/expertise-profiles/<name>/` | je nach Repo | Domain-Spezialisierungen mit eigener Distribution |

### 4.2 Pfad-Auflösung in `--expertise-profile=<path>`

- **Absolute Pfade:** unterstützt
- **Relative Pfade ab Plugin-Repo:** Default für public Profiles
- **Relative Pfade ab Cowork-Project-Working-Dir:** Default für lokale Profile

### 4.3 process-consulting Profile (initial)

Phase b der PB-014-Roadmap erstellt erstes Profile:
- Pfad: `private-notes/expertise-profiles/process-consulting/`
- Domain: organizational-consulting
- Sources: Matthiesen/Muster/Laudenbach (2023), Kühl, Luhmann
- Curation aus Zettelkasten-Vault (siehe `curation-spec.md`)

---

## 5. Constraints

| ID | Constraint | Begründung |
|---|---|---|
| C1 | Profile ist init-time-gelockt | Vermeidet Mid-Pair-Methodik-Drift |
| C2 | Profile-Inhalt eigenformuliert + Quellen-Verweise | Lizenzrecht-Compliance |
| C3 | Profile-Files standalone | Plugin-Portabilität |
| C4 | profile_schema_version pflichtig in Frontmatter | Schema-Migrations-Pfad |
| C5 | required_files-Liste enforced beim Loading | Profile-Vollständigkeits-Garantie |
| C6 | Profile-Loading-FAIL → bridge-init ABBRUCH | Anti-Half-Init-Pattern |
| C7 | Profile mit Bridge-Schema-Version inkompatibel → Loading-FAIL mit klarer Diagnose | UX |

---

## 6. Alternatives Considered

### 6.1 Inline in bridge-advisor SKILL.md (verworfen)

**Verworfen.** Plugin verliert Generizität, Skill-Description-Drift, kein Reuse für andere Domains. Architektur-Schmutz.

### 6.2 Eigenes Plugin `consulting-bridge` (verworfen)

**Verworfen.** Plugin-Dependency-Mechanik in CC schwach. Doppel-Plugin-Pflege. Coordinations-Logik würde dupliziert.

### 6.3 Custom-Felder in plugin.json (verworfen)

**Verworfen.** CC-Validator rejected unbekannte Top-Level-Keys (siehe Memory `feedback_plugin_dev_workflow.md` Punkt 2). External Files sind cleaner.

### 6.4 Vault-Link-Pattern (deferred)

**Deferred.** User-Entscheidung 2026-04-26: Profile standalone, keine Vault-Links. Reduziert Portabilitäts-Komplexität für v0.2.0. Vault-Link-Pattern als Phase-2-Erweiterung möglich (PB-021+ falls Bedarf).

### 6.5 Per-Handover-Profile-Switching (verworfen)

**Verworfen.** Methodik-Drift mid-Pair. Profile-Lock zur init-Zeit ist saubere Konstante.

### 6.6 Multi-Profile-Stack (deferred)

**Deferred.** N Profile gleichzeitig pro Pair (z.B. process-consulting + code-review). Komplexer Konflikt-Resolution-Mechanism. Für MVP nicht nötig — 1 Profile pro Pair reicht.

---

## 7. Consequences

### 7.1 Positiv

- Plugin bleibt agnostic + reusable für N Domains
- Profile-Curation getrennt vom Plugin-Code-Cycle
- Lizenzrechtliche Sauberkeit durch Eigenformulierungs-Pflicht
- Skalierung: weitere Profile (Code-Review, Pilot-Audit, Kritische-Theorie, etc.) als zusätzliche Verzeichnisse
- Datenschutz-Pfad klar: lokal in private-notes/, später opt-in public

### 7.2 Negativ

- Profile-Schema-Pflege als zusätzlicher Maintenance-Layer
- Loading-Logik in bridge-advisor erhöht Skill-Komplexität
- Profile-Curation ist arbeitsintensiv (Stufen 1-7 in `curation-spec.md`)

### 7.3 Operational

- Schema-Migration v1.0.0 → v1.1.0 erfordert State-File-Updates für laufende Pairs (Migration-Skript)
- Profile-Validation als Pre-Flight-Schritt 5 (additional zu den 4 bestehenden)
- Self-Test extension: Profile-Loading-Pfad (Empty-Profile als Fixture)

---

## 8. Acceptance-Kriterien (für ADR-Lock)

| # | Kriterium | Verifikation |
|---|---|---|
| A1 | State-Schema v1.1.0 inline spezifiziert mit `expertise_profile` + `profile_version` | §3.2 |
| A2 | Profile-Schema (PROFILE.md Frontmatter) inline spezifiziert | §3.3 |
| A3 | Loading-Lifecycle 4 Phasen (init-pin, validate, on-trigger-load, no-mid-pair-update) | §3.4 |
| A4 | Standalone-Pflicht explizit | §3.5 |
| A5 | 3 Pfad-Optionen (public/private-notes/separates-repo) | §4.1 |
| A6 | 7 Constraints C1-C7 | §5 |
| A7 | ≥5 Alternativen verworfen oder deferred mit Begründung | §6 |
| A8 | Migration-Skript v1.0.0→v1.1.0 spezifiziert (Profile-Felder optional, Default null) | §3.2 |

Alle 8 erfüllt → ADR_0030 LOCKED.

---

## 9. Open Questions

| OQ-ID | Frage | Klärung |
|---|---|---|
| OQ-1 | Wie wird Profile-Bump (z.B. process-consulting v0.1.0 → v0.2.0) zu laufenden Pairs propagiert? | Nicht. Profile-Pin via init zementiert Version. Neuer Pair = neueste Profile-Version. |
| OQ-2 | Was passiert wenn Profile-Datei fehlt während aktivem Pair? | bridge-advisor-Skill detektiert beim nächsten Trigger, WARN, degraded mode (=advisor agiert generic). |
| OQ-3 | Können Profile MCP-Server-Dependencies haben? | Phase 2. MVP: Profile sind Doc-Layer, keine MCP-Pflichten. |

---

## 10. References

- ADR_0029 §13.1 (Schema-Bump-Regeln)
- Memory `feedback_real_user_pilot_lessons.md` (User-Wunsch Domain-Spezialisierung)
- Memory `feedback_plugin_dev_workflow.md` (Custom-Feld-Constraints)
- META_PROZESSE_INVENTORY_v2.md KB-08 DiSoAn Luhmann Framework (theoretische Verwandtschaft)
- BACKLOG.md PB-014 Expertise-Profile-Layer
- `curation-spec.md` (Phase b Curation-Methodik)

---

**Lock-Status:** LOCKED. A1-A8 PASS. Phase a Implementation freigegeben (PB-014.1..5).

---

## Annex A — scope-lock-Phase-Spec-Default-Revidierung (post-p3-real-user-Pilot, 2026-04-29)

**Empirie aus Bridge-Pair p3-real-user (R0-R26):**

| Phase | ADR_0029-Default-Erwartung | p3-Pilot-Empirie | drift_factor |
|---|---|---|---|
| init + scope-lock + decision-lock-negotiations (R0-R11) | 4-6 Rounds | 12 Rounds | 2.4 |
| Mapping-Phase (R12-R26) | 14 Rounds (ad-hoc Spec) | 16 Rounds | 1.14 |

**Befund:** scope-lock-Phase mit Profile-Pin braucht 2-3× mehr Rounds als
ADR_0029-Default. Begründung:

1. **Profile-Pflicht-Workflows aktiviert** — `dissens-management-pflicht-bei-konsens-druck`
   produziert Counter-Sequenzen (R5→R6→R8→R9→R10)
2. **Konvergenz-Kriterium-Institutionalisierung** — Pflicht-explizite-pro-Punkt-Antwort
   verlangt mehrere Klarstellungs-Rounds
3. **Method-Annex-Substanz** — Profile-Frame-Anwendbarkeit muss substantiv
   geklärt werden (anwendbare vs un-anwendbare Frames)
4. **Counter-Konvergenz-Cycles** — substantielle Counter (R6 vier C-Punkte)
   produzieren 3-4 Re-Sync-Rounds bis Lock

**Spec-Default-Revidierung für künftige Plugin-Dev-Pilots:**

| scope-lock-Phase-Aspekt | Default v0.1.3+ |
|---|---|
| Rounds für init + scope-lock | 8-12 Rounds (statt 4-6) |
| Mapping-Rounds-pro-Befund | 2 Rounds (Decision + Konvergenz) |
| Klarstellungs-Reserve | 2 Rounds |
| Total Pair-Lifecycle für 5-6 Mapping-Items | 24-28 Rounds |

**Empfehlung:** ADR_0029 §5 Lifecycle-Sektion explizit auf Profile-Pin-Use-Cases
erweitern. Spec-Default soll Profile-Pflicht-Workflow-Overhead reflektieren.

**Annex-Lock:** 2026-04-29 als Teil v0.1.3 Patch-Welle.

---

## Annex B — Profile-with-workflows.md-Pattern (NEU v0.1.6, 2026-04-30)

**Status:** LOCKED 2026-04-30 als Teil v0.1.6 Profile-Activation-Erweiterung
**Trigger:** klafki-didaktik-Profile-Aufbau zeigte, dass Pflicht-Workflows operativ ausspezifiziert werden müssen (Trigger / Pflicht-Schritte / Output-Format / Linkage / Verweigerungs-Logik), nicht nur als Frontmatter-IDs gelistet.

### B.1 Problem

Das ADR_0030-§3.2-Schema definiert `pflicht_workflows`-Liste im PROFILE.md-Frontmatter als Workflow-IDs (z.B. `diagnose-frame-anwenden-pre-initial-advice`). Der bridge-advisor-Skill liest diese Liste, hat aber keine operative Spec — Workflow-IDs werden zu soft-hints ohne Enforcement-Backbone.

Empirie aus klafki-didaktik-Profile (Phase 6 Pflicht-Workflows-Definition):
- 5 Klafki-Workflows (W-01..W-05) plus Meta-Workflow brauchen je: Trigger-Bedingung, 5-7 Pflicht-Schritte, Output-Format-Vorlage (Tabellen/§-Sektionen), Linkage zu Frames+APs+Fragen, Verweigerungs-Klausel
- Inline-Spec im PROFILE.md-Frontmatter würde Frontmatter-Größe explodieren lassen (>500 Zeilen)
- Inline-Spec im PROFILE.md-Body würde Methodik-Sockel + Workflow-Spec mischen (Trennungs-Verlust)

### B.2 Decision

**Optionales workflows.md-File** als 5. Profile-File neben den 4 bestehenden:

```
expertise-profiles/<profile-name>/
├── PROFILE.md                # Methodik-Sockel + Frontmatter
├── diagnostic-frames.md      # Frames in Cluster
├── anti-patterns.md          # APs mit Korrektiv-Verweisen
├── question-bank.md          # Diagnose-Fragen Cluster-zugeordnet
└── workflows.md              # NEU v0.1.6 (optional): operative Workflow-Specs
```

`required_files`-Frontmatter listet `workflows.md` falls vorhanden.

### B.3 workflows.md Schema-Konvention

Pro Workflow Pflicht-Sektionen:

```markdown
## W-NN: <workflow-id-aus-pflicht_workflows>

**Trigger:**
- Bedingung 1
- Bedingung 2

**Pflicht-Schritte:**
1. Schritt 1
2. Schritt 2
...

**Output-Format (im handover):**
```
§Section-Name (W-NN):
<Tabelle oder Struktur-Vorlage>
```

**Linkage:** F-IDs, AP-IDs, Question-Bank-Refs

**Verweigerungs-Logik (optional):** Bedingung, unter der advisor Beratung verweigert / status-handover mit Klärungs-Anforderung schreibt
```

Plus optionaler Meta-Workflow für Cross-Frame-Diagnostik.

### B.4 Vorrang-Regel

`workflows.md` hat **Vorrang** vor `pflicht_workflows`-Frontmatter-Liste:
- Frontmatter listet Workflow-IDs (Profile-Lookup)
- workflows.md enthält operative Spec
- Skill-Implementation MUSS workflows.md-Specs anwenden, nicht nur frontmatter-IDs erwähnen

Bei Konflikt zwischen frontmatter-pflicht_workflows und workflows.md-Workflow-IDs: WARN, workflows.md ist authoritative.

### B.5 Profile-Schema-Version-Bump

| Aspekt | Vor v0.1.6 | Ab v0.1.6 |
|---|---|---|
| `required_files` | 4 fixed | 4 + optional `workflows.md` |
| `profile_schema_version` | 1.0.0 | 1.0.0 (kompatibel) — workflows.md ist optionale Erweiterung, kein Schema-Break |

Backward-Compatibility: Profiles ohne workflows.md (z.B. process-consulting v0.1.0) funktionieren unverändert.

### B.6 SKILL-Patches v0.1.6

bridge-advisor-Skill SKILL.md erhält in §Schritt 0 Profile-Loading:
- workflows.md-Loading falls in required_files
- workflow_specs als Profile-Substruktur
- Vorrang-Regel-Klausel

bridge-advisor-Skill Anti-Pattern-Liste:
- "NICHT workflows.md-Output-Formate ignorieren wenn Workflow getriggert"
- "NICHT Workflow-Verweigerungs-Logik skippen"

bridge-advisor-Skill Round-Type-Heuristik:
- "Worker-Plan unvollständig + Verweigerungs-Bedingung erfüllt → status mit Klärungs-Anforderung"

### B.7 Reference-Implementation

`expertise-profiles/klafki-didaktik/` ist erste Profile mit workflows.md (5 Workflows W-01..W-05 + Meta-Halbierungs-Diagnose). process-consulting bleibt v0.1.0 ohne workflows.md (backward-compat).

### B.8 Cross-Refs

- ADR_0030 §3.2 Profile-Schema (Annex B erweitert required_files-Liste)
- ADR_0030 §3.4 Profile-Loading (Annex B erweitert Loading-Logik)
- bridge-advisor SKILL.md §Schritt 0 (v0.1.6 Patch)
- expertise-profiles/klafki-didaktik/workflows.md (Reference-Implementation)
- expertise-profiles/process-consulting/PROFILE.md (Backward-Compat-Beispiel ohne workflows.md)

