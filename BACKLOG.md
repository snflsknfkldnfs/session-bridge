# session-bridge — Backlog

**Status:**
- Phase 1 (v0.1.0 MVP) abgeschlossen 2026-04-26
- v0.1.1 Hotfix abgeschlossen 2026-04-26 (Real-User-Pilot-Patches P-RP-01..04 + P-RP-08)
- v0.1.2 Phase a (Expertise-Profile-Layer ADR_0030) abgeschlossen 2026-04-26
- v0.1.2 Phase b (process-consulting Profile, private-notes/) abgeschlossen 2026-04-27
- v0.1.3 (Plugin-Marketplace-Robustheit + F-RP-29-Disziplin) abgeschlossen 2026-04-29
- Phase 2 **AKTIV** seit 2026-04-26 — Real-Use-Case-Pull erfüllt via EG_DEV_ADVISOR + UPP-Pair Pilot

**v0.1.4 Closure-Marker (2026-04-30):**

- 4 Phasen abgeschlossen (A + C + E + F) — Mini-Release-Strategie
- 9 Items resolved: F-RP-24, F-RP-26, PB-001 (Bilanz-Schema), mapping_decisions-Schema (NEU), artifact_type-Enum (NEU), PB-003, PB-011, PB-010, ADR_0031 (NEU)
- 14 neue Self-Tests T26-T39 — Total 42/42 PASS
- 4 ADR-Decisions in ADR_0031 deferred auf v0.1.5: PB-002 Domain-aware Threshold, PB-007 Activation, bilanz_v1-Migration enforcement, ADR_0029 §5.6 Filename-Annex
- Phase B (Foundation tools/-Library + bridge-update) + Phase D (PB-009 + PB-002) deferred auf v0.1.5 (eigener Major-Patch)
- Cross-Pair-Empirie-Foundation (ADR_0031) ermoeglicht PB-006 Cross-Pair-Memory-Spec sobald n>=5 Pairs pro Domain-Klasse erreicht
- v0.1.5-Roadmap: `pilot-runs/p3-real-user/v0.1.5-roadmap.md` (zu schreiben)

**v0.1.3 Closure-Marker (2026-04-29):**

- 5 Mapping-Decisions aus Bridge-Pair p3-real-user gepatched (D-001..D-005)
- 4 existing-Backlog-Items gepatched (F-RP-30, F-RP-31, F-RP-22 partial, F-RP-25)
- Plus F-RP-19 (Visualization-Widget BEOBACHTUNG) als Doku-Affordance
- Total: 11 Items, ~17-20h Self-Edit + 12 neue Self-Tests T14-T25
- Schema-Bump v1.1.0 → v1.1.1
- ADR_0030-Annex-Update: scope-lock-Phase mit Profile-Pin Spec-Default revidiert
  (drift_factor 2.4 in p3-Pilot)
- Bridge-Pair-Bilanz: `pilot-runs/p3-real-user/bridge/bilanz_8cbeaad0.md`
- v0.1.3-Patch-Pipeline-Doku: `pilot-runs/p3-real-user/v0.1.3-patch-pipeline.md`

**Phase-2 weiter aktiv** seit 2026-04-26. Tier-1-Items aus META_PROZESSE-Mining
(PB-001..PB-013) bleiben pending bei User-Pull-Trigger.

### Tier-2-Backlog-Befunde-Status (post-v0.1.3)

| ID | Befund | Severity | Status v0.1.3 |
|---|---|---|---|
| F-RP-15 | Mount-Inkonsistenz | HIGH | RESOLVED (D-005 Sub-A) |
| F-RP-23 | Sentinel-Bypass-Spec-Inkonsistenz | CRITICAL | RESOLVED (D-004) |
| F-RP-29 | Plan-vs-Execution-Layer-Konfusion | CRITICAL | DISSENS-DOCUMENTED §3.4.2 (D-001) |
| F-RP-30 | Worker-Skill-Role-Drift | CRITICAL | RESOLVED |
| F-RP-31 | User-Lifecycle-Visibility | CRITICAL | RESOLVED |
| F-RP-32 | Skill-Pre-Flight-Args | HIGH | RESOLVED (D-002) |
| F-RP-33 | pre-allocated-Pattern | BEOBACHTUNG | Affordance-Documented (D-003) |
| F-RP-34 | Konvergenz-Skip-Konvention | BEOBACHTUNG | Affordance-Documented (D-005 Sub-B) |
| F-RP-22 | Conversational-Memory-Cache | HIGH | RESOLVED (Pre-Flight 2 PFLICHT-Tool-Call) |
| F-RP-24 | Title-statt-Session-ID | HIGH | RESOLVED-IN-V0.1.4 (Phase A.1) |
| F-RP-25 | F-RP-XX-Placeholder-ID-Resolution | LOW | RESOLVED |
| F-RP-26 | worker.phase-Konsistenz | BEOBACHTUNG | RESOLVED-IN-V0.1.4 (Phase A.2 Auto-Propagation) |
| F-RP-19 | Visualization-Widget-UX | BEOBACHTUNG | DOCUMENTED (Phase A.3) |

**v0.1.1 Hotfix-Closure-Marker (2026-04-26):**
- 5 Patches appliziert: Schema-Konsistenz, Anti-Inferenz-Protokoll, Pre-Flight-Atomarität, Worker-Notification-Block, Sentinel-Replacement
- Validator + Self-Test 12/12 PASS post-Patch
- Commit `5bb36a9` auf main, gepusht zu github.com/snflsknfkldnfs/session-bridge
- Empirie-Quellen: EG_DEV_ADVISOR-Session (5 Bugs), UPP-Pair (funktionierender Lifecycle bis Round 11, 2 zusätzliche LOW/MED-Befunde)

**Phase-1-Closure-Marker (v0.1.0 MVP, 2026-04-26):**
- ADR_0029 LOCKED
- Validator: `claude plugin validate` PASS
- Self-Test: `tests/smoke_self_test.py` 12/12 PASS
- Pilot P1 Script-Mock: 20/20 PASS
- Pilot P2 Subagent-Pair: 19/19 PASS
- META_PROZESSE-Korpus-Mining: 32 Bausteine, 11 Cluster (private-notes/, gitignored)

---

## Tier 1 — Direct-Match aus META_PROZESSE-Mining

### PB-001 Bilanz-Schema für `bridge/bilanz_<pair_id>.md`

**Driver:** ADR_0029 §5.6 erwähnt Bilanz-Datei in close-Phase, aber kein Schema spezifiziert.

**Quelle:** META_PROZESSE_INVENTORY_v2.md KB-32 — Nachdokumentation 5-Stufen-Standard (`Nachdokumentation_UE_Standard.md`):
- Datensammlung → Professionelle Strukturierung → Reflexion (✅⚠️→) → Sequenz-Integration → Versionierung
- Pflicht-Sektionen: Metadaten / Tatsächlicher Verlauf / Erreichte Ergebnisse / Reflexion / Sequenz-Anschluss
- Anti-Pattern: Idealisierung statt rekonstruktiver Ehrlichkeit

**Phase-2-Spec:** `plugin/schemas/bilanz_v1.json` mit Pflicht-Frontmatter:
```yaml
pair_id, total_rounds, phase_sequence, decision_log_summary,
wallclock_drift_avg, lessons_learned[], successful_patterns[],
challenges[], anti_patterns_detected[]
```
Plus Body-Sektionen: §1 Tatsächlicher Verlauf / §2 Reflexion ✅⚠️→ / §3 Cross-Pair-Transfer-Hinweise.

**Aufwand-Schätzung:** ~2h Self-Edit (Schema + Smoke-Test + ADR §5.6 Referenz-Patch).


**Status v0.1.4:** RESOLVED-IN-V0.1.4 Phase C.1
---

### PB-002 Anti-Endless-Loop / Reflection-Action-Ratio-Threshold

**Driver:** ADR_0029 spezifiziert max 3 CAS-Retries, aber kein Schutz gegen iterate↔execute-Pingpong oder counter↔re-sync-Endlos-Schleifen.

**Quelle:** META_PROZESSE_INVENTORY_v2.md KB-02 PATA-3-Systemische-Reflexion-Regel:
- "Reflection-Action-Ratio < 20%" als Anti-Paralysis-Threshold
- Infinite-Regress-Protection mit explizitem Stopp wenn Reflexions-Anteil > 20% übersteigt

**Phase-2-Spec:** Bridge berechnet pro Pair Verhältnis `count(rounds[type ∈ {counter, re-sync, status, question}]) / count(rounds[type ∈ {execute, verify, decision-lock, pre-flight, pre-patch}])`. Bei Ratio > 4:1 (= >80% Reflection): WARN-Marker in state.json + advisor-Skill triggert "Lifecycle-Health-Alert" in nächstem Handover.

**Aufwand-Schätzung:** ~3h Self-Edit (State-Schema-Erweiterung + bridge-status-Command-Output + Skill-Body-Patch).

---

### PB-003 Pre-Decision-Verification in `decision-lock`-Round

**Driver:** ADR_0029 §4.2 hat decision-lock-Round mit `decided_by: user` Pflicht im Frontmatter, aber keine Pflicht-Pre-Decision-Klärungs-Sektion.

**Quelle:** META_PROZESSE_INVENTORY_v2.md KB-07 Bewertungsrichtung-Verification (`CRITICAL_Bewertungsrichtung_Verification_Protocol.md`):
- Vor jeder fundamentalen Transformation: Explizite User-Klärung
- Niemals automatische Annahmen über fundamentale Bewertungs-Direktionen
- Plus KB-10 Reverse-Questioning-Bank: max 2 Klärungsfragen, binäre Entscheidungen bevorzugen

**Phase-2-Spec:** `decision-lock`-Handover hat zusätzliches Pflicht-Frontmatter-Feld:
```yaml
pre_decision_verification:
  - question: "<konkrete binäre Frage>"
    answer: "<user-Antwort>"
    timestamp: <ISO-8601>
```
Mind. 1 Eintrag, max 2. Schema-allOf-Pflicht für type=decision-lock.

**Aufwand-Schätzung:** ~2h Self-Edit (Handover-Schema + bridge-handover-Command-Logik + bridge-advisor-Skill-Update).


**Status v0.1.4:** RESOLVED-IN-V0.1.4 Phase E.1
---

## Tier 2 — Adaptable / Phase-2-Erweiterung (deferred)

### PB-004 Auto-Trigger-Hooks (pre-tool-use für `[BRIDGE-CRITICAL]`-Tag)

**Driver:** ADR_0029 §8.5 Deferred. Korpus-Bestätigung KB-01 PATA-PATA Pre-Action-Zwangscheck.

**Phase-2-Spec:** Plugin-Hook im Plugin-Manifest, der bei Task-Description mit `[BRIDGE-CRITICAL]`-Marker pausiert + advisor-Konsultation erzwingt vor Execute.

**Trigger-Bedingung:** mind. 2 reale Pairs durchlaufen + User meldet wiederholt Konflikt-Fälle wo Auto-Hook geholfen hätte.

---

### PB-005 N-Pair-Topologie (>2 Sessions)

**Driver:** ADR_0029 §8.4 Deferred. Korpus-Quelle KB-27 Stakeholder-Integration-Mapping.

**Phase-2-Spec:** State-Schema-Erweiterung von `roles.{advisor,worker}` zu `roles[]` Array mit role-types `advisor | worker | observer | mediator`. Konsens-Resolution über Voting-Mechanismus.

**Trigger-Bedingung:** Real-Use-Case mit ≥3 parallelen Sessions auftaucht.

---

### PB-006 Cross-Pair-Memory-Aggregation

**Driver:** ADR_0029 §9 OOS-Findings + Korpus KB-23 Selbstlernende Reflexion-Engine 4-Phasen-Pipeline.

**Phase-2-Spec:** Beim `close` einer Pair: extrahiere Patterns (drift_factors, decision-log-Outcomes, blocker-resolutions), aggregiere in globalem `~/.session-bridge/memory/patterns.jsonl`. Künftige Pairs lesen + injizieren in advisor-Skill als Pattern-Hint.

**Trigger-Bedingung:** ≥5 abgeschlossene Pairs als Korpus + Real-Pull für Pattern-Reuse.

---

### PB-007 Domain-Hint-Field im Topic

**Driver:** Korpus KB-15+KB-16 Project-Description-Generator + Project-Routing.

**Phase-2-Spec:** State-Schema `topic` wird ergänzt um optionales `domain_hint: programming | writing | analysis | review | migration | other`-Enum für advisor-Skill-Domain-Adaptation.

**Trigger-Bedingung:** Real-Use über mehrere Domains hinweg.

---

### PB-008 4-Layer-Meta-Architecture-Erweiterung

**Driver:** Korpus KB-11 4-Layer-Meta-Architecture (Meta⁴ Invisible Intelligence / Meta³ Routing / Meta² Memory / Meta¹ Standards).

**Phase-2-Spec:** Bridge-MVP ist Meta¹-Layer (Schema-Standards). Erweitern zu Meta²-Memory (PB-006) + Meta³-Routing (auto-pair-recommendation basierend auf vergangenen Pairs).

**Trigger-Bedingung:** Aggregations-Bibliothek (PB-006) + ≥10 Pairs als Lernmaterial.

---

## Tier-1-Items aus Real-User-Pilot (2026-04-26) — neue Empirie

### PB-009 Drift-Plausibility-Check für Wallclock-Estimates

**Driver:** Real-User-Pilot UPP-Pair Round 9 — Worker meldete Drift 0.58 als ungewöhnlich. Advisor musste manuell verifizieren via Stichprobe + Heuristik-Re-Run. Plugin hat keinen Plausibilitäts-Check für Drift-Werte.

**Quelle:** F-RP-10 (MEDIUM-Befund aus UPP-Empirie).

**Phase-2-Spec:** bridge-handover-Command bei type=verify oder type=execute mit `actual_min`-Wert: Berechnet `drift_factor = actual_min / estimated_min`, prüft gegen Memory-historische Drift-Range pro Pair-Topic-Pattern. Bei Abweichung > 2×Std-Dev: WARN-Marker im Output + Empfehlung an User "Drift ungewöhnlich, manuelle Stichprobe empfohlen".

**Aufwand-Schätzung:** ~3h Self-Edit (Schema-Erweiterung wallclock_estimates + Heuristik-Code in bridge-handover-Command + Self-Test).

---

### PB-010 Number-Konsistenz-Validation in Handover-Body-Listen

**Driver:** Real-User-Pilot UPP-Pair Round 9 — Worker schrieb in Handover "4 atomar gelistet=8" (Tippfehler, real 8 Items). Plugin validiert Frontmatter-Schema, aber nicht Body-Konsistenz.

**Quelle:** F-RP-11 (LOW-Befund aus UPP-Empirie).

**Phase-2-Spec:** Optional-Validator-Hook in bridge-handover-Command: parse Body-Lists, count Items, vergleiche mit explizit genannten Zahlen ("X atomar"). Bei Diskrepanz: WARN.

**Aufwand-Schätzung:** ~1.5h Self-Edit. Niedrige Prio (kosmetisch, kein Daten-Bug).


**Status v0.1.4:** RESOLVED-IN-V0.1.4 Phase E.3
---

### PB-011 shared-path-Default-Heuristik mit Filesystem-Inspektion

**Driver:** Real-User-Pilot — bridge-init `--shared-path` ist optional, aber Default "Working-Dir der eigenen Session" funktioniert nicht wenn Sessions in unterschiedlichen Cowork-Projects laufen.

**Quelle:** F-RP-05 / P-RP-05 (deferred aus v0.1.1 Hotfix).

**Phase-2-Spec:** Plugin-Helper-Tool `tools/find_shared_path.sh` — sucht via Mount-Point-Inspektion + session_info.list_sessions den größten gemeinsamen Pfad. Fallback auf User-Question wenn ambig.

**Aufwand-Schätzung:** ~2h Self-Edit + Empirie-Test in 2-Project-Pilot.


**Status v0.1.4:** RESOLVED-IN-V0.1.4 Phase E.2
---

### PB-012 tools/-Library für Atomic-Write + State-Mutation

**Driver:** Real-User-Pilot — `write_atomic(...)` ist Pseudocode-Funktion in jedem Command separat. Code-Duplication-Risiko über N Commands.

**Quelle:** F-RP-07 / P-RP-06 (deferred aus v0.1.1 Hotfix).

**Phase-2-Spec:** `tools/bridge_state.py` als shared Python-Library mit:
- `read_state(shared_path) -> dict`
- `write_atomic_cas(shared_path, state, expected_updated_at) -> bool`
- `validate_against_schema(state) -> list[errors]`
- `pending_attach_replace(state, role, real_session_id, ...) -> dict`

Skills/Commands rufen via `${CLAUDE_PLUGIN_ROOT}/tools/bridge_state.py` (subprocess oder Python-Import). Pseudocode in MD-Dateien wird zu echtem Library-Aufruf.

**Aufwand-Schätzung:** ~5h Self-Edit (Library + 5 Commands refactoren + Self-Test extension).

---

### PB-013 /bridge-update-Command für post-Init-Korrekturen

**Driver:** Real-User-Pilot — Topic-Mismatch wurde via direkter state.json-Edit durch Advisor-Skill korrigiert. Kein dedicated Command für post-Init-Updates (Topic, expertise-source, worker-focus).

**Quelle:** F-RP-08 / P-RP-07 (deferred aus v0.1.1 Hotfix).

**Phase-2-Spec:** `commands/bridge-update.md` mit Argumenten `--field=<topic|expertise-source|worker-focus> --value="<new>"`. Pre-Flight: phase ∈ {init, scope-lock, iterate} (nicht in execute/verify/close — würde Decision-Log brechen).

**Aufwand-Schätzung:** ~2h Self-Edit.

---

## Tier-1-Activation-Reihenfolge (post-v0.1.1)

Empfehlung basierend auf User-Pull-Wahrscheinlichkeit:

1. **PB-012 tools/-Library** — Foundation für sauberen Code in PB-013/PB-009
2. **PB-013 /bridge-update** — Adressiert konkrete Pain-Point aus EG_DEV_ADVISOR-Pilot
3. **PB-001 Bilanz-Schema** — Plugin-Closure-UX-Verbesserung
4. **PB-009 Drift-Plausibility** — Quality-of-Life für Advisor
5. **PB-002 Anti-Endless-Loop** — defensiv, niedrige Prio
6. **PB-003 Pre-Decision-Verification** — Edge-Case-Härtung
7. **PB-011 shared-path-Heuristik** — UX, niedrige Prio
8. **PB-010 Number-Konsistenz** — kosmetisch

---

## Activation-Trigger für Phase 2

Phase-2-Entwicklung startet **nicht** bei Spec-Reife oder Roadmap-Plan, sondern **nur** wenn folgende Real-Use-Indikatoren auftreten:

| Indikator | Trigger-Schwelle |
|---|---|
| Real-User-Pilot durchlaufen | ≥1 vollständiger 6-Round-Lifecycle mit zwei aktiven Cowork-Sessions |
| Wiederholte User-Anfrage nach session-bridge | ≥2 unabhängige Cross-Session-Beratungen über Bridge initialisiert |
| Konkrete Lücke aus Real-Use | User berichtet konkretes Bridge-Failure das Phase-2-Item adressiert |
| Marketplace-Submit-Vorbereitung | Plan, session-bridge öffentlich zu distribuieren |

**Anti-Trigger:** Spec-Wachstum ohne empirische Falsifikation = Memory `feedback_ebenen_testrun_vs_infra.md` Anti-Pattern. Phase-2 ohne Real-Pull verboten.

---

## Phase-2-Methodik (wenn aktiviert)

1. **Re-Lock ADR_0029** mit Schema-Bump v1.0.0 → v1.1.0 (Minor-Bump per §13.1) bei jedem Tier-1-Item.
2. **Pflicht-Migration-Skript** für State-Files mit altem schema_version.
3. **Self-Test-Erweiterung** in `tests/smoke_self_test.py` für jedes neue Schema-Feature.
4. **Real-Pilot-Re-Run** nach jedem Tier-1-Item zur Falsifikation.
5. **Memory-Update** `project_session_bridge_state.md` nach jedem Item-Closure.

---

**Snapshot-Date:** 2026-04-27 (post PB-014 Phase a + b).
**Phase-1-Closed:** 2026-04-26 (39/39 Tests + Validator PASS + Korpus-Mining v2 LOCKED).
**v0.1.1 Hotfix-Closed:** 2026-04-26 (5 Real-User-Pilot-Patches, commit 5bb36a9).
**v0.1.2 Closed:** 2026-04-26 (PB-014 Phase a Expertise-Profile-Layer ADR_0030 LOCKED, commit fe5a2d5).
**PB-014 Phase b Closed:** 2026-04-27 (process-consulting Profile in private-notes/, 10 Frames + 10 Anti-Patterns + 47 Diagnose-Fragen, Profile-Pre-Flight 5/5 PASS).
**Phase-2-Active:** ✅ aktiviert 2026-04-26 via Real-User-Pilot. **PB-014 abgeschlossen** (Phase a Architektur + Phase b erstes Profile). 12 weitere Tier-1-Items pending (7 META_PROZESSE-Mining + 5 Real-User-Pilot).

## PB-014 Phase b Closure-Marker (2026-04-27)

- Quell-Korpus: 342 organisationssoziologische Zettel (Kühl 119 + Humanisierung 223)
- Curation-Stufen 0-7 abgearbeitet, alle 8 Akzeptanz-Kriterien PASS (siehe `private-notes/process-consulting-curation/06_validation-report.md`)
- 6 Subagent-Calls (sequentiell, je Cluster) für Frame-Synthese — total ~18 min Subagent-Wall-Clock
- Profile-Files in `private-notes/expertise-profiles/process-consulting/` (PROFILE.md, diagnostic-frames.md, anti-patterns.md, question-bank.md)
- Cherry-Picking-Stichprobe 5/10 PASS, Lizenz-Pre-Check OK (3 Belege paraphrasiert in Stufe 7)
- Profile-Pre-Flight (bridge-init Schritt 5) Self-Test: 5/5 PASS

## PB-014 Phase b deferred (Pre-Publication-Path) — DEFERRED-V0.2.0+

**Status (2026-04-30):** Public-Release DEFERRED bis post-juristischer-Beratung. Audit-Status sauber, Migration kann ohne Re-Audit erfolgen.

### Pre-Publication-Pflicht-Aktionen Status

| # | Aktion | Status |
|---|---|---|
| 1 | Lizenzrecht-Check (User-Aktion + juristische Beratung) | **PENDING** — Scope kommerzielle Distribution erfordert juristische Vorab-Klärung |
| 2 | Cherry-Picking-Vollaudit (alle 10 Frames + 10 APs gegen Quell-Zettel) | **PASS** — Stufe-8-Report `private-notes/process-consulting-curation/08_validation-report-vollaudit.md` |
| 3 | Empirie-Test in Real-User-Pair mit aktiviertem Profile | **PASS** — Bridge-Pair p3-real-user 28 Rounds, Bilanz `pilot-runs/p3-real-user/bridge/bilanz_8cbeaad0.md` |
| 4 | Profile in `expertise-profiles/process-consulting/` (public-Repo) verschieben | **DEFERRED** — Migration-Plan in Stufe-8-Report §9 bereit |

### Re-Check-Trigger

- **post-juristischer-Beratung User-Decision Lizenz-Modell:** entweder (a) Open-Source-with-Citation-Pflicht (z.B. CC-BY-NC-SA), (b) Commercial-License, (c) Hybrid (Open-Source-Profile + Commercial-Tooling), oder (d) weiterhin private-notes/ defer
- **Audit-Status:** Stufe 8 PASS — Migration kann ohne Re-Audit erfolgen
- **Pre-Migration-Pflicht:** User-Decision (1) + Migration-Plan §9 ausführen

### Lizenz-Beratungs-Vorbereitungs-Doku

`private-notes/process-consulting-curation/09_juristische-beratung-vorbereitung.md` — strukturiertes Material für Anwalts-Termin (Quellen, Charakter, Distribution-Optionen, Disclaimers, konkrete Fragen).

Aktuell: Profile bleibt in `private-notes/` (gitignored). Public-Release-Aktivierung post-juristische-Beratung.

## Smoke-Test-Befunde aus 2026-04-27 (Tier-2-Backlog)

| ID | Befund | Severity |
|---|---|---|
| **F-RP-12** | Pre-Flight Punkt 4 wurde "smoke-context" deferred trotz P-RP-03-Patch — Skill-Interpretation neigt weiter zu pragmatischem Skip | LOW |
| **F-RP-13** | Sandbox-/tmp vs Host-/tmp shared-path-Mapping unklar — für 2-Session-Pair-Tests muss Path host-zugänglich sein | LOW |
| **F-RP-14** | Session-ID-Marker "smoke-test-advisor-session" als Stub — Plugin sollte Smoke- vs Real-Mode-Distinction handhaben | LOW |

Aufnahme als PB-019..021 in zukünftiger Hotfix-Welle (deferred bis User-Pull).
