# Changelog

All notable changes to session-bridge are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) — Semver pinned per ADR_0029 §13.1.

---

## [0.1.6] — 2026-04-30 — Profile-with-workflows.md-Pattern + advisor-Skill-Patches + plugin.json-bridge-update-Eintrag

### Source: klafki-didaktik-Profile-Aufbau (Phase 7 Functional-Anchoring) → V-1/V-2 Open-Points uncovered

bridge-advisor SKILL.md hatte Hardcoding auf 4 Profile-Files (PROFILE.md + frames + APs + question-bank). pflicht_workflows-Frontmatter-Liste war soft-hint ohne operative Spec-Backbone. klafki-didaktik-Profile mit 5 ausspezifizierten Workflows (W-01..W-05) konnte nicht regulär geladen werden.

### Added

- **bridge-advisor SKILL.md** §Schritt 0 Profile-Loading erweitert um workflows.md-Loading (optional, Vorrang vor frontmatter-pflicht_workflows-Liste)
- **bridge-advisor SKILL.md** Anti-Pattern-Liste:
  - "NICHT workflows.md-Output-Formate ignorieren wenn Workflow getriggert"
  - "NICHT Workflow-Verweigerungs-Logik skippen"
- **bridge-advisor SKILL.md** Round-Type-Heuristik:
  - "Worker-Plan unvollständig + Workflow-Verweigerungs-Bedingung erfüllt → status mit Klärungs-Anforderung statt initial-advice"
- **docs/adr/ADR_0030_Expertise_Profile_Pattern.md Annex B** (NEU 2026-04-30) Profile-with-workflows.md-Pattern dokumentiert (Schema-Konvention + Vorrang-Regel + Backward-Compatibility)
- **plugin.json commands** Eintrag commands/bridge-update.md ergänzt (war v0.1.5-Lücke)
- **tests/smoke_self_test.py** T54 + T55 + T56 NEU
  - T54: ADR_0030 Annex B workflows.md-Pattern dokumentiert
  - T55: bridge-advisor SKILL.md workflows.md-Loading-Patch
  - T56: klafki-didaktik Reference-Profile Vollständigkeit (skip-if-private)

### Changed

- **bridge-advisor SKILL.md** Cross-Refs erweitert um ADR_0030 Annex B + v0.1.6 SKILL-Patch-Hinweis

### Reference-Implementation

- `private-notes/expertise-profiles/klafki-didaktik/` — erstes Profile mit workflows.md (5 Workflows + Meta-Halbierungs-Diagnose)
- `private-notes/expertise-profiles/process-consulting/` — bleibt v0.1.0 ohne workflows.md (Backward-Compat-Beispiel)

### Verification

- Self-Test 59/59 PASS (T1-T53 + T54/T55/T56 NEU)
- claude plugin validate (in User-Terminal-Session zu pruefen)
- Profile-Schema-Version unverändert v1.0.0 (workflows.md ist optionale Erweiterung, kein Schema-Break)

### Backward-Compatibility

- Profiles ohne workflows.md (z.B. process-consulting v0.1.0) funktionieren unverändert
- bridge-advisor degradiert sauber wenn workflows.md fehlt

### Deferred to v0.1.7+ (DEFERRED-Phase-2)

- PB-004 Auto-Trigger-Hooks (Trigger: ≥2 reale Pairs mit "haette geholfen"-Befund)
- PB-005 N-Pair-Topologie (Trigger: ≥3 parallele Sessions Use-Case)
- PB-006 Cross-Pair-Memory (Trigger: n≥5 Pairs pro Domain — aktuell n=1-3, ADR_0031 §5)
- PB-008 4-Layer-Meta-Architecture (Trigger: PB-006 Foundation + n≥10 Pairs)
- klafki-didaktik Live-Pilot (Phase 8) pending User-Aktion in p9-klafki-pilot-Workspace

---

## [0.1.5] — 2026-04-30 — Foundation Library + Lifecycle-Robustheit + ADR_0031-Decisions

### Source: v0.1.5-Roadmap Phasen B + D + G + H + I (Foundation + Lifecycle-Robustheit Release)

Phase B (PB-012 + PB-013) — Foundation:
- tools/bridge_state.py NEU (7 Library-Funktionen): read_state, write_atomic_cas (atomic-CAS via temp+rename + Pre-Atomic-Backup), validate_against_schema, pending_attach_replace (D-004 R23-Revidierung strict-mode), append_round (mit F-RP-26 Auto-Propagation), archive_shared_artifact, calibrate_wallclock_post_hoc
- commands/bridge-update.md NEU (PB-013): /bridge-update --field=<topic|expertise-source|worker-focus|domain-hint> --value=<new>; Pre-Flight whitelisting + phase-block + status_observations Update-Trail

Phase D — Lifecycle-Robustheit:
- D.1 PB-009 Drift-Plausibility-Check: Library check_drift_plausibility(domain_hint, drift_factor) Domain-aware mit DRIFT_RANGES (plugin-self-dev / use-case / default); Empirie-Anker p3 drift 1.14-2.4
- D.2 PB-002 Anti-Endless-Loop Reflection-Action-Ratio Domain-aware: Library compute_reflection_action_ratio + check_ratio_threshold per ADR_0031 §4.1 RATIO_THRESHOLDS (plugin-self-dev: 15.0, use-case: 4.0, default: 4.0)
- bridge-handover.md §lifecycle-health-checks-Sektion mit drift + ratio Library-Aufrufen

Phase G — PB-007 Domain-Hint-Field Activation:
- bridge_state_v1.json: topic_metadata.domain_hint-Enum (6 Werte: plugin-self-dev, use-case, architecture-spec, investigation-trace, methodology-improvement, other)
- schema_version-Enum erweitert auf 1.2.0
- bridge-init.md: --domain-hint optional Argument

Phase H — bilanz_v1-Schema Migration enforcement (PB-001 follow-up / ADR_0031 §4.3):
- Library validate_bilanz_against_schema NEU
- bridge-close.md §bilanz-schema-enforcement-Sektion mit ADR_0031 Cross-Refs

Phase I — ADR_0029 §5.6 Annex B (ADR_0031 §4.4):
- Filename-Konvention: bridge/bilanz_<pair_id>.md
- Schema-Pointer: schemas/bilanz_v1.json
- Migration-Kandidat: p4-eg-dev/bridge/BILANZ.md

### Added

- **tools/bridge_state.py** (NEU, 11 API-Funktionen + 2 Konstanten DRIFT_RANGES + RATIO_THRESHOLDS)
- **commands/bridge-update.md** (NEU, PB-013)
- **commands/bridge-close.md** §bilanz-schema-enforcement
- **commands/bridge-handover.md** §lifecycle-health-checks (drift + ratio)
- **commands/bridge-init.md** --domain-hint Argument (PB-007)
- **schemas/bridge_state_v1.json** topic_metadata.domain_hint-Enum + schema_version v1.2.0
- **docs/adr/ADR_0029_Session_Bridge_Pattern.md** Annex B (Bilanz-Filename-Konvention)

### Changed

- **state-Schema** v1.1.2 → v1.2.0 (topic_metadata.domain_hint, backward-compat mit v1.1.0/v1.1.1)

### Verification

- Self-Test 56/56 PASS (T40-T53 NEU, +14 Tests gegenueber v0.1.4)
- claude plugin validate (in User-Terminal-Session zu pruefen)
- ADR_0031-Decisions §4.1 (PB-002 Domain-aware), §4.2 (PB-007 Activation), §4.3 (bilanz Migration), §4.4 (Filename-Konvention) alle implementiert

### Deferred to v0.1.6+

- PB-004 Auto-Trigger-Hooks (Trigger: ≥2 reale Pairs mit "haette geholfen"-Befund)
- PB-005 N-Pair-Topologie (Trigger: ≥3 parallele Sessions Use-Case)
- PB-006 Cross-Pair-Memory (Trigger: n≥5 Pairs pro Domain — aktuell n=1-3, ADR_0031 §5)
- PB-008 4-Layer-Meta-Architecture (Trigger: PB-006 Foundation + n≥10 Pairs)
- Profile-Public-Release process-consulting (Trigger: post-juristische-Beratung User-Decision)

---

## [0.1.4] — 2026-04-30 — DEFERRED-Items + Schema-Formalisierungen + Lower-Priority + Cross-Pair-Patterns

### Source: v0.1.3-Roadmap Phasen A + C + E + F (Mini-Release)

Phase A (DEFERRED-V0.1.4-Items aus v0.1.3):
- F-RP-24 HIGH RESOLVED: Title-statt-Session-ID — `--worker-session-title` als primaerer UX-Flag, `--worker-session-id` als Fallback
- F-RP-26 BEOBACHTUNG RESOLVED: worker.phase Auto-Propagation aus Worker-Frontmatter

Phase C (Schema-Formalisierungen aus p3-Empirie):
- PB-001 RESOLVED: bilanz_v1.json Schema (12 Sektionen Reference-Implementation aus p3-bilanz_8cbeaad0.md)
- NEU: mapping_decisions_v1.json Schema (D-NNN-Format mit allOf-Pflicht DISSENS-DOCUMENTED requires sub_type)
- NEU: bridge_state_v1.json shared_artifacts.artifact_type-Enum (mapping-method-annex / mapping-decisions-log / bilanz / custom)

Phase E (Lower-Priority HIGH/MEDIUM):
- PB-003 RESOLVED: Pre-Decision-Verification Pflicht-Feld in handover-Frontmatter (allOf type=decision-lock, minItems=1, maxItems=2)
- PB-011 RESOLVED: shared-path-Default-Heuristik mit `tools/find_shared_path.sh` Helper-Stub
- PB-010 RESOLVED: bridge-handover §body-number-konsistenz optional Hook (WARN-Mode Tippfehler-Detection)

Phase F (Cross-Pair-Empirie-Synthese):
- ADR_0031 NEU: Cross-Pair-Patterns aus 4 Pilot-Run-Empirie (p3+p4+p5+p6) — 7 §-Sektionen + 9 §-Sub-Sektionen
- 4 ADR-Decisions: PB-002 Domain-aware Threshold, PB-007 Activation, bilanz_v1-Migration, ADR_0029 §5.6 Filename-Konvention

### Added

- **schemas/bilanz_v1.json** (NEU, PB-001) — Bilanz-File-Schema mit 12 Pflicht-Sektionen
- **schemas/mapping_decisions_v1.json** (NEU) — D-NNN-Decisions-Log-Schema mit allOf-Constraints
- **tools/find_shared_path.sh** (NEU, PB-011) — Helper-Script Stub fuer shared-path-Heuristik (executable)
- **docs/adr/ADR_0031_Cross-Pair-Patterns.md** (NEU) — Cross-Pair-Empirie-Synthese aus 4 Pilots
- **commands/bridge-init.md** §--worker-session-title (primaer) + Argument-Resolution title-first 3 Pfade (multi-match, no-match, direct-id)
- **commands/bridge-attach.md** §--this-session-title + §worker.phase-Initial-Set
- **commands/bridge-handover.md** §worker.phase-Auto-Propagation + §pre-decision-verification + §body-number-konsistenz
- **schemas/handover_frontmatter_v1.json** pre_decision_verification array property + allOf type=decision-lock requires it
- **schemas/bridge_state_v1.json** shared_artifacts.artifact_type-Enum + worker.phase Auto-propagation description

### Changed

- **synth_valid_handover** in tests/smoke_self_test.py — decision-lock-Cases include pre_decision_verification (1 Eintrag)
- **bridge-init.md** Argument-Resolution-Protokoll — title-first jetzt primaerer Pfad

### Deferred to v0.1.5

- Phase B (Foundation tools/-Library + bridge-update) — substantielles Refactoring, eigener Major-Patch
- Phase D (PB-009 Drift-Plausibility + PB-002 Anti-Endless-Loop) — depends on Phase B
- ADR_0031 Decisions §4.1 (PB-002 Domain-aware Threshold) + §4.2 (PB-007 Activation) + §4.3 (bilanz_v1 Migration enforcement) + §4.4 (ADR_0029 §5.6 Annex B Filename-Konvention)

### Verification

- Self-Test 42/42 PASS (T26-T39 NEU, +14 Tests)
- claude plugin validate (in User-Terminal-Session zu pruefen)
- Cross-Pair-Empirie-Validation via ADR_0031 (4 Pilot-Runs analysiert)

---

## [0.1.3] — 2026-04-29 — Plugin-Marketplace-Robustheit + F-RP-29-Disziplin

### Source: Bridge-Pair p3-real-user (Mapping-Phase R12-R26, 5 Decisions)

5 Mapping-Decisions D-001..D-005 covering 6 Items:
- D-001 F-RP-29 → DISSENS-DOCUMENTED §3.4.2 (Plan-vs-Execution-Layer-Konfusion)
- D-002 F-RP-32 → PATCH (Pre-Flight required-Args hard-enforce)
- D-003 F-RP-33 → AFFORDANCE (pre-allocated-Pattern-Doku)
- D-004 F-RP-23 → PATCH (Sentinel-Invariante, R23-revidiert nach Worker-Counter R22)
- D-005 Sub-A F-RP-15 → PATCH (sandbox-mount-Pre-Flight)
- D-005 Sub-B F-RP-34 → AFFORDANCE (Konvergenz-Skip-Konvention-Doku)

Plus existing v0.1.3-Backlog: F-RP-30 (Worker-Role-Boundary), F-RP-31
(User-Lifecycle-Visibility), F-RP-22 (Filesystem-Read), F-RP-24 (Title-statt-ID DEFERRED-V0.1.4),
F-RP-25 (ID-Resolution).

### Added

- **bridge-handover §forward-pointer-rationale-Sektion** (D-003) — pre-allocated-
  Pattern für decision-lock vor Annex-Materialisierung
- **bridge-handover §konvergenz-skip-rationale + Pre-Flight 6** (D-005 Sub-B)
- **bridge-handover §Re-Sync-Sub-Typen + Pre-Flight 5** (D-001 Worker-Pos) —
  plan-layer / execution-layer / hybrid Differenzierung
- **bridge-handover §Output-Marker BRIDGE-WRITE-COMPLETED** (D-001 Advisor-Pos)
- **bridge-attach + bridge-handover Pre-Flight 5 hard-enforce** required-Args (D-002)
- **bridge-init Pre-Flight 5b sandbox-mount + §sandbox-mount-prerequisite** (D-005 Sub-A)
- **bridge-init Pre-Flight 2 PFLICHT-Tool-Call** (F-RP-22) — Filesystem-Read statt Conversational-Memory
- **bridge-advisor §Anti-Plan-Drift + §User-Translation-Konvention** (D-001 Advisor-Pos, F-RP-29)
- **bridge-worker §Role-Boundary** (F-RP-30, CRITICAL) — keine Profile-pflicht-workflows
  oder AP-Diagnosen worker-side
- **bridge-worker §ID-Resolution-Pre-Flight** (F-RP-25) — Friction-Befund-ID-Lookup
- **bridge-status erweitert** (F-RP-31, CRITICAL) — User-friendly Output mit Rolle,
  Rounds, nächster Aktion, Polling-Hint, Forward-Pointer-Warnings
- **Skill-Mode-Marker `[bridge-worker mode]` / `[bridge-advisor mode | profile=...]`** (F-RP-31 Patch 4)
- **bridge-init §Visualization-Widget UX-Pattern** (F-RP-19 BEOBACHTUNG)

### Changed

- **bridge-init `--worker-session-id`** ist jetzt UX-Hint, nicht state-Pin (D-004,
  Breaking-Change). worker_obj setzt IMMER `session_id: SENTINEL_PENDING`.
- **bridge-attach Pre-Flight 4** strict-Sentinel (D-004) — kein auto-recover-Branch.
- **state-Schema v1.1.0 → v1.1.1** — `mapping_budget` als top-level optional, `mapping_category_history`
  per Decision, `shared_artifacts.{owner,status,round_allocated,round_active}` (forward-pointer),
  `status_observations.{type,defined_in_round,skipped_in_round,skip_basis,cycle_counter}` (convergence-skip).
- **Self-Test 15 → 28 Tests** (NEU T14-T25 für v0.1.3 Mapping-Decisions). Alle 28/28 PASS.

### Migration v0.1.2 → v0.1.3 (Breaking-Change F-RP-23)

`state.json` mit direktem session_id-Pin (v0.1.2-Use-Case mit `--worker-session-id`):
- Patch nötig:
  ```bash
  jq '.roles.worker.session_id = "pending-attach"' state.json > state.tmp && mv state.tmp state.json
  ```
- Anschließend: bridge-attach erneut ausführen

### Verification

- `claude plugin validate` PASS (erwartet)
- Self-Test 28/28 PASS (T14-T25 NEU)
- Bridge-Pair p3-real-user-Bilanz: `pilot-runs/p3-real-user/bridge/bilanz_8cbeaad0.md`
- Patch-Pipeline-Doku: `pilot-runs/p3-real-user/v0.1.3-patch-pipeline.md`

---

## [0.1.2-phase-b] — 2026-04-27 — process-consulting Profile (PB-014 Phase b, private)

### Added (private-notes/, NICHT im Plugin-Repo committed)

- **process-consulting Profile** v0.1.0 in `private-notes/expertise-profiles/process-consulting/`:
  - `PROFILE.md` (4 Methodik-Säulen, 3 Quellen, 4 Pflicht-Workflows, 8 Trigger-Phrasen, Frontmatter Pre-Flight 5/5 PASS)
  - `diagnostic-frames.md` (10 Frames in 6 Cluster-Gruppen — Organisation-als-Form, Mitgliedschaft+Rollen, Macht/Führung, Spannung+Integration, Schauseite/Simulation, Personalisierung)
  - `anti-patterns.md` (10 Anti-Patterns AP-01..10 mit Beobachtbarkeit + Begründung + Belege + Korrektiv)
  - `question-bank.md` (47 Diagnose-Fragen, gruppiert nach Frames + Bridge-Round-Type)
- **Curation-Workspace** `private-notes/process-consulting-curation/` mit Stufen 0-7 (Tag-Inventur 342 Files, 6 Cluster, 6 Subagent-Frame-Synthesen, Validation-Report)

### Empirie

- 6 Subagent-Calls (1 pro Cluster, sequentiell) — Wall-Clock 1.8-5.8 min pro Call (skaliert linear mit File-Count, ~3-5 sec/File)
- Total Subagent-Wall-Clock: ~18 min für 199 File-Reads
- 0 AMBIGUOUS-Findings, 10 Frames + 10 Anti-Patterns alle PASS
- Hypothesen-Revision durchgeführt: F3.1 von Foucault-Linie zu Luhmann/Kühl-Systemtheorie umformuliert (Subagent-Befund)
- 3 Lizenz-Issues paraphrasiert (S. 158/174/218, F4.2)

### Quellen

- Matthiesen/Muster/Laudenbach (2023): Die Humanisierung der Organisation. Vahlen
- Kühl, S. (2020): Organisationen — Eine sehr kurze Einführung. Springer
- Luhmann, N. (1964): Funktionen und Folgen formaler Organisation (zit. via Matthiesen + Kühl)

### Pre-Publication-Pflicht (deferred)

Profile bleibt in `private-notes/` (gitignored). Für öffentliche Distribution erforderlich: Lizenzrecht-Check + Cherry-Picking-Vollaudit + Empirie-Test in Real-User-Pair.

---

## [0.1.2] — 2026-04-26 — Expertise-Profile-Layer (PB-014 Phase a)

### Added

- **ADR_0030 Expertise-Profile-Pattern** LOCKED — neue Schicht-1-Architektur über bridge-advisor. Plugin bleibt domain-agnostisch, Domain-Expertise als externe Resource.
- **State-Schema v1.1.0** — `roles.advisor.expertise_profile` + `profile_version` als optionale Felder. Backward-compatible mit v1.0.0.
- **bridge-init `--expertise-profile=<path>` Flag** — Profile wird init-time-gepinnt im state.json.
- **Pre-Flight Punkt 5** — Profile-Validation (4 required_files + Frontmatter-Pflicht-Felder + supported profile_schema_version) vor state.json-Write.
- **bridge-advisor Schritt 0 Profile-Loading-Workflow** — bei jedem Trigger Profile lesen, Pflicht-Workflows + Round-Linkage anwenden.
- **References-Type `expertise-profile`** — methodische Referenzen aus Profile als Beleg-Quelle in Handovers.
- **`expertise-profiles/_SCHEMA.md`** — Profile-Layout-Konvention dokumentiert.
- **`expertise-profiles/_empty-test/`** — Empty-Profile-Fixture für Architektur-Smoke-Test.
- **`expertise-profiles/curation-spec.md`** — 7-Stufen-Curation-Methodik mit Anti-Halluzinations- und Lizenzrecht-Constraints. Vorbereitung für PB-014 Phase b (process-consulting Profile).

### Changed

- Self-Test erweitert von 12 auf 15 Tests (T11 expertise_profile-Field, T12 v1.0.0 backward-compat, T13 schema_version-enum). Alle 15/15 PASS.
- bridge-advisor Anti-Pattern-Section um 3 Profile-bezogene Regeln erweitert (Profile-Workflow-Skip, Mid-Pair-Switch-Verbot, Wörtliche-Zitat-Verbot).

### Phase-2-Roadmap

PB-014 Phase a (Architektur) abgeschlossen mit v0.1.2. **PB-014 Phase b** (process-consulting Profile-Curation, ~9-11 h) pending bei User-Pull-Trigger.

### Verification

- `claude plugin validate` PASS
- Self-Test 15/15 PASS
- ADR_0030 LOCKED (A1-A8 PASS)

---

## [0.1.1] — 2026-04-26 — Real-User-Pilot Hotfix

### Added

- **Worker-Notification-Block** (P-RP-04, CRITICAL) — `bridge-init` generiert ready-to-paste-Prompt für Worker-Session inkl. exakter `/bridge-attach`-Kommando. Verhindert Pair-stuck-in-init.
- **Argument-Resolution-Protokoll** (P-RP-02, HIGH) — bei missing `--topic` ABBRUCH + strukturierte User-Question via session_info MCP zur Worker-Session-Identifikation. Anti-Inferenz-Pattern explizit dokumentiert.
- **Sandbox-vs-Host-MCP-Mechanismus-Konvention** — bridge-init.md dokumentiert wann Sandbox-bash ausreicht und wann Host-MCP osascript-Fallback erforderlich ist.
- **pending-attach-Sentinel-Stubs** (P-RP-01, HIGH) — explizite String-Stubs für nicht-eigene Rolle bei init statt schema-invalides leeres Object.
- **bridge-attach Pre-Flight 4** (P-RP-08, LOW) — Sentinel-Detection (`session_id == "pending-attach"`) plus Replacement-Assertion garantiert sauberen Sentinel-zu-real-Session-Übergang.

### Fixed

- **Schema-Spec-Inkonsistenz im Init-Pseudocode** (F-RP-01) — Pseudocode produzierte `{}` für nicht-eigene Rolle, Schema verlangte `session_id` + `active_since`. Fix via pending-attach-Sentinel-Stubs (siehe Added).
- **Pre-Flight Punkt 4 deferred** (F-RP-03) — Skill-Spec war "Bei FAIL: ABBRUCH", aber Punkt 4 (session_info MCP) wurde in Real-User-Pilot deferred. Fix: alle 4 Punkte als atomar markiert, NICHT deferrable.
- **Worker-Session attached nie** (F-RP-04, CRITICAL) — Pair faktisch tot weil keine Worker-Notification. Fix: Pflicht-Output-Block in bridge-init.

### Changed

- bridge-init.md `argument-hint` erweitert um `--worker-session-id` (empfohlen für advisor-Rolle).
- bridge-init.md `description` erweitert: Plugin generiert ready-to-paste-Prompt.
- shared-path-Default-Heuristik verschärft: kein eigenes Working-Dir als Default, User-Question wenn nicht explizit gegeben.
- bridge-attach Anti-Pattern-Section: 5 statt 3 Items, inkl. Self-Attach-Detection und Sentinel-Replacement-Pflicht.

### Empirie-Quelle

- **EG_DEV_ADVISOR-Session** (2026-04-26): 5 HIGH/CRITICAL-Befunde im Init-Prozess (F-RP-01..04, F-RP-09).
- **UPP-DEV-WORKER + UPP-DEV-ADVISOR Pair** (2026-04-26): Funktionierender Bridge-Lifecycle bis Round 11 + 2 zusätzliche LOW/MED-Befunde (F-RP-10 Drift-Plausibility, F-RP-11 Number-Konsistenz).
- 11 Befunde insgesamt, 5 in v0.1.1 gepatched, 6 deferred zu Phase-2-Backlog (PB-009..013 + PB-005..008).

### Verification

- `claude plugin validate` PASS
- `tests/smoke_self_test.py` 12/12 PASS
- Plugin-Manifest + Marketplace-Manifest Version 0.1.0 → 0.1.1 gebumpt

---

## [0.1.0] — 2026-04-26 — Initial MVP Release

### Added

- **ADR_0029 Session-Bridge-Pattern** LOCKED — 13 Sektionen, 8 Drivers (D1-D10), 7 Constraints (C1-C7), 9 Akzeptanz-Kriterien (A1-A9 PASS).
- **Plugin-Manifest** `.claude-plugin/plugin.json` (CC-Validator-konform, v0.1.0).
- **Dependencies-Spec** `.claude-plugin/dependencies.json` (ADR_0028-Pattern, separat ausgelagert).
- **State-Schema** `schemas/bridge_state_v1.json` — JSON-Schema-Draft-7 für `bridge/state.json`.
- **Handover-Schema** `schemas/handover_frontmatter_v1.json` — YAML-Frontmatter-Validation für Handover-Files.
- **Skills**:
  - `skills/bridge-advisor/SKILL.md` — Cross-Session Advisor-Rolle, polling-based Status-Verifikation via session_info MCP.
  - `skills/bridge-worker/SKILL.md` — operative Worker-Rolle, schreibt Status/Counter/Pre-Flight/Execute/Verify Handovers.
- **Commands** (5):
  - `/bridge-init` — Pair initialisieren
  - `/bridge-attach` — zweite Session anschließen
  - `/bridge-handover` — Round-typisiertes Handover schreiben
  - `/bridge-status` — read-only State-Anzeige
  - `/bridge-close` — Pair schließen + Bilanz
- **Self-Test** `tests/smoke_self_test.py` — 12 Tests gegen Schema-Konsistenz, allOf-Pflichten, negative-Cases.
- **Pilot-Skripte**:
  - `pilot-runs/p1-script-mock/pilot_lifecycle_mock.py` — 12-Round-Lifecycle gegen Schemas, 20/20 PASS.
  - `pilot-runs/p2-subagent-pair/p2_validate.py` — Subagent-Pair-Validation, 19/19 PASS.

### Verification

- `claude plugin validate` PASS
- 39/39 Pilot-Tests PASS (12 self-test + 20 P1 script-mock + 7 P2 subagent-pair)

---

## Unreleased — Phase-2 Backlog

Siehe [`BACKLOG.md`](BACKLOG.md) für 13 Tier-1-Items (8 aus META_PROZESSE-Korpus-Mining + 5 aus Real-User-Pilot 2026-04-26).

**Aktivierungs-Reihenfolge:**

1. PB-012 tools/-Library (Foundation)
2. PB-013 /bridge-update-Command
3. PB-001 Bilanz-Schema
4. PB-009 Drift-Plausibility-Check
5. PB-002 Anti-Endless-Loop
6. PB-003 Pre-Decision-Verification
7. PB-011 shared-path-Heuristik
8. PB-010 Number-Konsistenz
