# ADR_0031 — Cross-Pair-Patterns aus Real-Use-Empirie

**Status:** ACCEPTED (v0.1.4 Phase F)
**Datum:** 2026-04-30
**Autor:** Bridge-Pair-Empirie-Synthese aus 4 Pilot-Runs (p3-real-user + p4-eg-dev + p5-eg-v06-spec + p6-upp-eg-advice)
**Schema-Bump:** keiner direkt; PB-002 + PB-007 Re-Kalibrierungs-Empfehlungen
**Foundation fuer:** PB-006 Cross-Pair-Memory (DEFERRED-Phase-2)

---

## §1 Scope + Empirie-Sample

**Ziel:** Cross-Pair-Patterns aus 4 Real-Use-Pilot-Runs identifizieren als Foundation fuer:
- PB-002 Anti-Endless-Loop Reflection-Action-Ratio-Threshold-Kalibrierung (Domain-aware)
- PB-006 Cross-Pair-Memory (DEFERRED — benoetigt Pattern-Inventar)
- PB-007 Domain-Hint-Field (Spec-Foundation aus Empirie)
- bilanz_v1-Schema (v0.1.4 C.1) Migration-Kandidaten-Identifikation

**Empirie-Sample (4 Pairs):**

| Pair | Topic | Domain-Klasse | Profile-Pin | Total Rounds | Status |
|---|---|---|---|---|---|
| p3-real-user | bridge-plugin development | **Plugin-Self-Dev** | process-consulting v0.1.0 | 28 | closed |
| p4-eg-dev | escape game development | **Use-Case** | NONE | 16 | closed |
| p5-eg-v06-spec | v06-architektur-spec | **Use-Case** | NONE | 10 | closed |
| p6-upp-eg-advice | upp-improvement-via-eg-expertise | **Use-Case** | NONE | 3 (in-progress) | iterate |

---

## §2 Empirie-Tabelle (Round-Type-Verteilung + Ratios)

| Pair | status | initial-advice | question | counter | re-sync | decision-lock | pre-flight | execute | verify | bridge-close | TOTAL | reflection | action | **R/A-ratio** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **p3-real-user** | 4 | 1 | 2 | 1 | 18 | 1 | 0 | 0 | 0 | 1 | 28 | 25 | 2 | **12.50** |
| **p4-eg-dev** | 6 | 1 | 1 | 3 | 0 | 2 | 1 | 0 | 2 | 0 | 16 | 10 | 6 | 1.67 |
| **p5-eg-v06-spec** | 2 | 1 | 0 | 2 | 0 | 2 | 1 | 0 | 2 | 0 | 10 | 4 | 6 | 0.67 |
| **p6-upp-eg-advice** | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 2 | 1 | 2.00 |

**Reflection-Action-Klassifikation (Plugin v0.1.4 PB-002):**
- reflection-Rounds: counter, re-sync, status, question
- action-Rounds: execute, verify, decision-lock, pre-flight, pre-patch, initial-advice
- ratio = reflection / action

**Befund:** PB-002-Threshold 4.0 (= 80% reflection) wird in p3 (12.50) **massiv ueberschritten** — alle anderen Pairs liegen bei 0.67-2.00 (deutlich unter Threshold).

---

## §3 Cross-Pair-Patterns

### §3.1 Pair-Lifecycle-Profil pro Domain

**Pattern A — Plugin-Self-Dev mit Profile-Pin** (Empirie: p3):
- **Round-Count:** 25-30 (3-5x laenger als ADR_0029 §5 Default)
- **R/A-ratio:** 10-15 (re-sync-heavy)
- **Decision-Log-Count:** 1 single scope-lock-decision (Mapping-Phase enthaelt Sub-Decisions D-NNN in shared_artifact)
- **shared_artifacts:** 2 (mapping-method-annex + mapping-decisions-log)
- **Charakteristik:** scope-lock-Negotiation-Cycles + Methoden-Klaerungs-Pausen + Mapping-Phase mit substantiv-Decisions in shared_artifact

**Pattern B — Use-Case ohne Profile-Pin** (Empirie: p4 + p5):
- **Round-Count:** 10-16 (innerhalb ADR_0029 §5 Default)
- **R/A-ratio:** 0.67-1.67 (action-heavy, klassisch)
- **Decision-Log-Count:** 5-7 explizite decisions (alle direkt in state.decision_log)
- **shared_artifacts:** 4-6 (domain-spezifische Files im Worker-Project)
- **Charakteristik:** kompakter scope-lock + execute-Phase mit Quality-Gates + verify-Cycle

**Pattern C — Use-Case in-progress** (Empirie: p6):
- noch nicht klassifizierbar (3 Rounds, keine Verify), tendiert zu Pattern B basierend auf early R/A-ratio 2.00 + 6 Decisions in 3 Rounds

### §3.2 Reflection-Action-Ratio-Ranges pro Domain

| Domain-Klasse | R/A-ratio-Range | Threshold-Anwendbarkeit (PB-002) |
|---|---|---|
| Plugin-Self-Dev mit Profile | 10-15 | aktueller Default 4.0 zu eng — Threshold 15.0 angemessen |
| Use-Case ohne Profile | 0.5-2.5 | Default 4.0 ok |
| Use-Case mit Profile (n=0) | unbekannt — Empirie fehlt | Hypothese: 3-5 (Profile-Effekt + Use-Case-action-Bias) |

**ADR-Decision (siehe §4.1):** PB-002 Threshold soll **Domain-Hint-aware** kalibriert werden (depends on PB-007).

### §3.3 Profile-Pin-Effekt auf Pair-Laenge

**Empirie-Vergleich (gleiche Domain-Klasse mit/ohne Profile waere ideal — n=0 fuer Use-Case-mit-Profile):**

p3 (Plugin-Self-Dev mit Profile) vs p4 (Use-Case ohne Profile):
- Round-Count: 28 vs 16 → Profile-Effekt ~+75% (aber Domain-Differenz konfundiert)
- re-sync-Anteil: 18 vs 0 → klares Profile-Effekt-Indiz (Profile-pflicht-workflows produzieren Methoden-Klaerung)
- Decision-Log-Count: 1 vs 7 → Profile-Effekt: Decisions wandern in shared_artifact (mapping-decisions) statt state.decision_log

**Kausal-Hypothese:** Profile-Pin produziert:
1. dissens-management-pflicht-Workflow → mehr counter/re-sync-Cycles
2. Konvergenz-Kriterium-Institutionalisierung → Pflicht-explizite-pro-Punkt-Antworten
3. Mapping-Method-Annex + Mapping-Decisions-Log Schema-Adoption → strukturierte Decisions in shared_artifact statt state.decision_log

**Empfehlung fuer kuenftige Empirie:** Use-Case-Pair MIT Profile-Pin durchfuehren um Domain-vs-Profile-Effekt zu disambiguieren.

### §3.4 shared_artifacts.artifact_type-Patterns

**Pattern A (Plugin-Self-Dev p3):** shared_artifacts sind **Bridge-Pair-interne Methoden-Artefakte**:
- mapping-method-annex (artifact_type=mapping-method-annex per v0.1.4 C.3)
- mapping-decisions-log (artifact_type=mapping-decisions-log)

**Pattern B (Use-Case p4 + p5):** shared_artifacts sind **Domain-Project-Files** im Worker-Project:
- p4: BEFUND_TRACE_RE_RUN4.md, findings.jsonl, anti_drift_sub_investigation.md, etc. (escape-game-generator-Repo)
- p5: PLUGIN_v0_6_ARCHITEKTUR_SPEC.md, sprint_dependency_graph.md (escape-game-generator-Repo)
- artifact_type Default: 'custom' (per v0.1.4 C.3 Enum)

**Cross-Pair-Befund:** v0.1.4 C.3 artifact_type-Enum reflektiert diese Differenzierung korrekt. Plugin-Self-Dev-Pairs adoptieren mapping-* artifact_types; Use-Case-Pairs nutzen 'custom' fuer domain-specific Artefakte.

### §3.5 BILANZ-Format-Konsistenz

**Empirie:**
- p3 hat `bridge/bilanz_8cbeaad0.md` (12-Sektionen-Schema-strikt, Stufe-7-Konsolidierung)
- p4 hat `bridge/BILANZ.md` (freier Format, aber substantiell mit Round-Verlauf + Decision-Log)
- p5 + p6: noch zu pruefen

**Naming-Inkonsistenz:** p3 verwendet `bilanz_<pair_id>.md`, p4 verwendet `BILANZ.md`. **Plugin-Spec-Befund (NEU):**
- ADR_0029 §5.6 spezifiziert "Bilanz-Datei in close-Phase" ohne Filename-Konvention
- bilanz_v1.json (v0.1.4 C.1) spezifiziert Schema-Inhalt aber nicht Filename
- **Empfehlung:** ADR_0029 §5.6 Update mit Filename-Konvention `bridge/bilanz_<pair_id>.md` (analog state.json + handover-Files)

**Schema-Adoption:**
- p3-bilanz: bilanz_v1-Schema-konform (12 Sektionen vorhanden)
- p4-BILANZ: nicht v1-Schema-konform (Round-Verlauf + Decision-Log vorhanden, Pflicht-Felder reflection.was_funktionierte/was_problematisch/was_als_naechstes fehlen)
- **Migration-Kandidat:** p4-BILANZ als Schema-Erweiterung (oder p4-BILANZ als bilanz_v1-Migration-Test)

---

## §4 Decisions

### §4.1 PB-002 Reflection-Action-Ratio Threshold soll Domain-Hint-aware sein

**Decision:** PB-002 Implementation in v0.1.5+ verwendet Domain-Hint (PB-007) zur Threshold-Kalibrierung:

```yaml
ratio_thresholds:
  plugin-self-dev-with-profile: 15.0  # p3-Empirie: 12.5 ist normal
  use-case-without-profile: 4.0        # p4+p5+p6: 0.67-2.00, 4.0 als WARN-Schwelle
  use-case-with-profile: 5.0           # Hypothese, Empirie n=0
  default: 4.0                         # Fallback wenn Domain-Hint fehlt
```

**Status:** zur Implementation in v0.1.5 mit PB-007 als Pre-Condition.

### §4.2 PB-007 Domain-Hint-Field — Empirie-Driven Activation

**Decision:** PB-007 (DEFERRED-Phase-2) wird **aktiviert** durch ADR_0031-Empirie. Konkrete Implementation:

```yaml
state.topic_metadata:
  domain_hint:
    enum:
      - plugin-self-dev          # p3-Pattern
      - use-case                 # p4+p5+p6-Pattern
      - architecture-spec        # p5-Sub-Pattern
      - investigation-trace      # p4-Sub-Pattern
      - methodology-improvement  # p6-Sub-Pattern
      - other
```

**Status:** zur Implementation in v0.1.5 als state-Schema-Erweiterung v1.1.2 → v1.2.0.

### §4.3 bilanz_v1-Schema-Migration fuer Use-Case-Pairs

**Decision:** p4-BILANZ als Migration-Test fuer bilanz_v1-Schema-Konformitaet:
- p4 bilanz_v1-konform machen (reflection.was_funktionierte/was_problematisch/was_als_naechstes Pflicht-Felder ergaenzen)
- p5 + p6 zu ihrem close-Zeitpunkt bilanz_v1-konform schreiben
- Filename-Konvention `bilanz_<pair_id>.md` ab v0.1.4+

**Status:** dokumentations-only in v0.1.4 (kein Code-Patch). Voll-Enforcement in bridge-close-Skill (v0.1.5+).

### §4.4 ADR_0029 §5.6 Update — Filename-Konvention

**Decision:** ADR_0029 §5.6 Bilanz-Sektion Update mit:
- Filename-Konvention: `bridge/bilanz_<pair_id>.md`
- Schema-Pointer: `schemas/bilanz_v1.json` (NEU v0.1.4 C.1)
- Empirie-Anker: p3-real-user als Reference-Implementation

**Status:** als Annex B in ADR_0029 schreiben (analog ADR_0030 Annex A v0.1.3).

---

## §5 Foundation fuer PB-006 Cross-Pair-Memory (DEFERRED-Phase-2)

ADR_0031 liefert Pattern-Inventar das PB-006 als Foundation braucht:

**Aggregations-Felder fuer Cross-Pair-Memory:**
1. **Domain-Hint** (PB-007 Decision §4.2)
2. **R/A-ratio-Empirie pro Domain** (Threshold-Kalibrierung)
3. **artifact_type-Verteilung pro Domain** (mapping-* fuer Self-Dev, custom fuer Use-Case)
4. **Round-Count-Range pro Domain** (Pattern A: 25-30, Pattern B: 10-16)
5. **Decision-Lock-Count-Pattern** (Self-Dev: 1 single, Use-Case: 5-7 multiple)

**Aggregations-Trigger:** PB-006 wird aktiviert wenn ≥5 Pairs pro Domain-Klasse abgeschlossen sind. Aktuell:
- Plugin-Self-Dev mit Profile: n=1 (p3)
- Use-Case ohne Profile: n=2 closed + 1 in-progress (p4 + p5 + p6)
- Use-Case mit Profile: n=0

**Empfehlung:** PB-006 weiterhin DEFERRED bis n≥5 in einer Domain-Klasse. ADR_0031 definiert die Inventur-Schema-Spec.

---

## §6 Implications fuer ADR_0029 Lifecycle-Spec

ADR_0029 §5 Lifecycle-Sektion sollte **Domain-aware Default-Profiles** beruecksichtigen:

| ADR_0029 §5 Sub-Sektion | Aktueller Default | ADR_0031-Empfehlung |
|---|---|---|
| §5.1 init Phase | nicht spezifiziert | bleibt 1 Round |
| §5.2 scope-lock Phase | 4-6 Rounds (revidiert ADR_0030 Annex A: bis zu 12 mit Profile) | Domain-aware: Use-Case 1-3 Rounds, Plugin-Self-Dev mit Profile 8-12 |
| §5.3 iterate Phase | ad-hoc | Use-Case 4-8 Rounds, Plugin-Self-Dev 14-20 (Mapping-Phase) |
| §5.4 execute Phase | ad-hoc | Use-Case 1-3 Rounds, Plugin-Self-Dev 0 (out-of-pair per ADR_0021) |
| §5.5 verify Phase | ad-hoc | Use-Case 1-2 Rounds, Plugin-Self-Dev 0 |
| §5.6 close Phase | 1 Round | bleibt 1 Round, plus Bilanz-Pflicht-Schema (siehe §4.4) |

**Total Pair-Lifecycle:**
- Use-Case-Pair-Default: 8-15 Rounds
- Plugin-Self-Dev-mit-Profile-Default: 24-32 Rounds

---

## §7 Cross-Refs

- **ADR_0021** Strict-Separation Plugin-Dev-Project ≠ Bridge-Teilnehmer (Pattern A nur post-close anwendbar)
- **ADR_0029** Session-Bridge-Pattern §5 Lifecycle (Domain-aware Defaults Empfehlung §6)
- **ADR_0030** Expertise-Profile-Pattern Annex A (scope-lock-Phase mit Profile-Pin Spec-Default revidiert)
- **bilanz_v1.json** (v0.1.4 C.1) Schema fuer Bilanz-Files
- **mapping_decisions_v1.json** (v0.1.4 C.2) Schema fuer Mapping-Decisions-Log
- **bridge_state_v1.json** v1.1.2 (v0.1.4 C.3) artifact_type-Enum
- **PB-002** Anti-Endless-Loop Reflection-Action-Ratio (Threshold-Kalibrierung in v0.1.5)
- **PB-006** Cross-Pair-Memory (DEFERRED, Foundation in §5)
- **PB-007** Domain-Hint-Field (Activation in §4.2)
- **p3-real-user/bridge/bilanz_8cbeaad0.md** Pattern-A-Reference
- **p4-eg-dev/bridge/BILANZ.md** Pattern-B-Reference (Migration-Kandidat)
- **p5-eg-v06-spec/bridge/state.json** Pattern-B-Empirie
- **p6-upp-eg-advice/bridge/state.json** Pattern-C-Empirie (in-progress)
