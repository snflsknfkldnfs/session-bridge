# Mapping-Method-Annex — p3-real-user Bridge-Pair 8cbeaad0

**Pair-ID:** 8cbeaad0-e67a-4184-889b-76a70c21d617
**Profile:** process-consulting v0.1.0 (`/Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/`)
**Decision-Lock-Round:** 11 (Worker-Initiator, decided_by=consensus, 2026-04-28T15:11:29Z)
**Annex-Status:** active (Round 12 advisor-Schreiben)
**Annex-Version:** v0.1.2 (R19-Update §7 T1-Wording-Präzisierung + Budget-Kalibrierung)
**Mapping-Phase-Start:** Round 12 (post-decision-lock)

---

## §1 Methoden-Sockel

Profile process-consulting ist organisationssoziologisch (Luhmann/Kühl/Matthiesen). Bridge-Pair (advisor + worker + Plugin-Dev-Project) wird als quasi-organisationale Einheit gelesen. Anwendung ist **analogisch** mit expliziten Trag-/Bruch-Markierungen.

Vier Methodik-Säulen (aus PROFILE.md):
- (1) Systemtheoretisch — Differenz Person/Funktion, Mensch/Mitglied
- (2) Spannungs-orientiert — Widersprüche als produktive Ressource
- (3) Anti-harmonisch — Konsens-Inszenierung als Anti-Pattern
- (4) Differenz-bewahrend — Vorder-/Hinterbühne, Schauseite/Inhalt

---

## §2 Frame-Anwendbarkeit für Mapping-Aufgabe

### §2.1 Anwendbare Frames

| Frame | Anwendbarkeits-Begründung |
|---|---|
| **F1.1** form-substituiert-elementare-verhaltensweisen | Drei-Säulen-Logik (Programme/Strukturen/Mitgliedschaftsbedingungen) tragt strukturanalog für Plugin-Architektur (ADRs/Schemas/Skill-Pre-Flights). Diagnose-Frage "welche der drei Säulen ist im Anliegen am wenigsten reflektiert" ist operationalisierbar. |
| **F1.2** formalitaet-und-informalitaet-im-wechselspiel | Skill-Spec (formal) wird durch Use-Praxis (informell) interpretiert/erweitert. Brauchbare Illegalität (Argument-Bypass des Sentinels) als technisches Pendant. Wechselspiel ist Konstitutions-Bedingung des Plugin-Lebenszyklus. |
| **F4.1** spannung-als-ressource-produktiver-widerspruch-statt-pathologie | Spannungs-Pathologisierung als Diagnose-Linse für Befunde, die strukturell produktiv sein könnten (z.B. Sentinel-Bypass-Affordance). |
| **F4.2** integration-durch-differenz-dissens-management-statt-konsens-fiktion | Begründet die `Dissens-Documented`-Mapping-Kategorie. Pflicht-Workflow `dissens-management-pflicht-bei-konsens-druck` aktiv für Mapping-Phase. |
| **F5.1** schauseite-emanzipiert-sich-vom-inhalt | Schauseite/Hinterbühne-Differenz für Doku-Form-Entscheidungen (z.B. Affordance-SoT-Wahl: ADR vs Skill-Doku vs Friction-Log). |

### §2.2 Un-anwendbare Frames

| Frame | Bruch-Begründung |
|---|---|
| **F2.1** differenz-mensch-mitglied-als-operationsbedingung | Schwach metaphorisch (Skill-Funktion ↔ Skill-Aufrufer-Intent), aber materiell verschieden — kein Personen-Subjekt im Plugin. Nicht für strukturelle Diagnose nutzbar. |
| **F2.2** mitgliedschaft-als-formale-anpassung-mit-personalem-risikotraeger | Sub-Pattern "Personen tragen Risiko der Regelübertretung" hat KEIN technisches Pendant. Pre-Flight-Bypass durch Argument-Konsumption hat keinen Personen-Risiko-Träger — nur Skill-Verhalten. |
| **F3.1** hierarchie-als-zeitlich-stabilisierte-fuehrung-mit-mitgliedschafts-akzeptanz | Hierarchie-Konzept hat kein Plugin-Pendant. Skill-Calls sind nicht hierarchisch organisiert. |
| **F3.2** fuehrung-jenseits-der-hierarchie-via-unterwachung-versus-pseudo-selbstorganisation | Unterwachung setzt Personen-Subjekte voraus. Plugin-Komponenten unterwachen sich nicht. |
| **F6.1** uebergriff-auf-ganze-person-als-motivations-und-entlastungstechnologie | Kein Personen-Subjekt im Plugin. Frame strukturell un-anwendbar. |

**Konsequenz:** Mapping-Begründungen dürfen sich nur auf §2.1-Frames stützen. Verweis auf §2.2-Frames in Mapping-Rationale = Methoden-Fehler (Mapping-Kategorie-Fehler).

---

## §3 Mapping-Kategorien

Vier Kategorien für Befund-Mapping, institutionalisiert in Worker-Round-8 Teil C, decision-locked Round 11:

### §3.1 Patch

**Definition:** Befund verlangt formale Norm-Korrektur am Plugin (Code-Edit, Schema-Erweiterung, Skill-Spec-Update, ADR-Anpassung).

**Kriterien:**
- Befund identifiziert konkrete Spec-Lücke oder Inkonsistenz
- Patch-Vorschlag ist operationalisierbar (Edit-Skript, Schema-Diff)
- Konsequenz bei Nicht-Patch: Lifecycle-Bruch oder Nutzer-Blockierung

**Status-Übergang nach Patch-Mapping:**
- Befund bleibt OPEN bis Patch-Merge
- Nach Merge: `RESOLVED-IN-Vx.y.z` mit Pointer auf Commit/PR

### §3.2 Affordance

**Definition:** Befund identifiziert informelles Use-Wissen, das als optionale Affordance dokumentiert wird statt als formale Norm enforce zu werden.

**Kriterien:**
- Beide Pfade (Spec-konform + Use-Pattern) sind funktional
- Use-Pattern hat Affordance-Wert, der bei Spec-Enforcement verloren ginge
- Doku-Form ist verfügbar (siehe §3.5 SoT-Loci)

**Status-Übergang nach Affordance-Mapping:**
- Status-Wechsel auf `Affordance-Documented`
- Pflicht-Pointer auf Single-Source-of-Truth (Skill-Doku-Sektion oder ADR)
- Friction-Log-Eintrag bleibt mit Pointer-Reference

### §3.3 Defer

**Definition:** Befund wird in der aktuellen Mapping-Phase nicht entschieden — Decision wird auf späteren Trigger-Zeitpunkt verschoben.

**Kriterien:**
- Befund hat keine akute Lifecycle-Konsequenz
- Decision-Boden ist nicht ausreichend (fehlt Empirie, Spec-Klärung, Strategie-Decision)
- Re-Eintritts-Trigger ist klar formulierbar

**Status-Übergang nach Defer-Mapping:**
- Status-Wechsel auf `DEFERRED-Vx.y.z` (Ziel-Version) oder `DEFERRED-CONDITIONAL`
- Trigger-Format obligatorisch (siehe §3.6 Defer-Trigger-Format)

### §3.4 Dissens-Documented

#### §3.4.0 Inflations-Schutz (NEU in v0.1.1)

Default-Mapping-Kategorie für operative Pattern mit Doku-Konsequenz (z.B. `pre-allocated`-Pattern, Konvergenz-Skip-Konvention) ist **AFFORDANCE**, NICHT Dissens-Documented. Dissens-Documented ist explizit reserviert für Fälle mit zwei substantiell unterschiedlichen Positionen, die nicht durch parallele Sub-Items zusammengeführt werden können oder Skopus-Differenz aufweisen. Mapping-Begründung muss bei Dissens-Documented-Wahl explizit die zwei Positionen + Sub-Typ (§3.4.1 vs §3.4.2) angeben — fehlende Differenzierung = Inflations-Marker, in nächster Konvergenz-Round zu countern.

#### §3.4.1 + §3.4.2 (Sub-Typen, unverändert v0.1.0)

**Definition:** Befund hat ≥2 valide Positionen aus dem Pair (Worker / Advisor / mehr) ohne erzwungene Konvergenz.

**Sub-Typen** (Worker-Round-10 Teil C Skopus-Korrektur):

**§3.4.1 Kompetitiver Dissens (X ⊥ Y):**
Positionen sind gegensätzlich, schließen sich gegenseitig aus.

**§3.4.2 Skopus-Differenz (X ⊆ Y):**
Eine Position ist echte Teilmenge der anderen. Beide schreiben dasselbe Sub-Item; eine schreibt zusätzlich. Methodisch: `Dissens-Documented` umfasst auch Skopus-Differenzen, nicht nur kompetitive Gegensätze.

**Kriterien:**
- ≥2 Positionen sind dokumentiert mit Begründung
- Positionen sind im Pair als legitim anerkannt (nicht zu verwerfen)
- Reconcile ist optional, nicht Pflicht

**Status-Übergang nach Dissens-Documented-Mapping:**
- Status-Wechsel auf `DISSENS-DOCUMENTED`
- Pflicht-Sub-Pointer pro Position (Worker-Position / Advisor-Position / etc.)
- Reconcile-Möglichkeit als optionaler Annex
- Status-Auflösung zu `RESOLVED` nur bei expliziter Reconcile-Decision (z.B. wenn beide Items separately implemented + merged sind)

---

## §4 Defer-Trigger-Format

Pflicht-Format für jeden DEFERRED-Befund (Format-Beispiele):

### §4.1 Datums-Trigger (ISO-Date)

```yaml
defer_until: 2026-09-01
defer_reason: "Empirie-Sammlung erfordert ≥3 weitere Pilot-Runs"
defer_review_round: <round-number-or-event>
```

### §4.2 Bedingungs-Trigger (Klausel)

```yaml
defer_until_condition: "after-bridge-plugin-v0.3.0-merge"
defer_reason: "abhängig von Schema-Bump v1.x → v2.0"
defer_review_trigger: "v0.3.0 release event"
```

### §4.3 Compound-Trigger (Date + Condition, OR-Logik)

```yaml
defer_until: 2026-12-01
defer_until_condition: "user-revidiert-budget OR critical-blocker-aufkommt"
defer_reason: "soft-cap, regelmäßige Re-Review"
```

**Anti-Pattern:** DEFERRED ohne Trigger = `defer_until: TBD` → AP-09-Re-Inszenierung (Klarheits-Imperativ ohne operative Bindung). Pflicht-Validation in Mapping-Round.

---

## §5 SoT-Migrations-Pfad pro Mapping-Kategorie

Bestehende Friction-Log-Einträge werden bei Mapping-Entscheidung gemäß folgender Migration umkategorisiert:

| Mapping-Kategorie | friction-log Status-Übergang | Pflicht-Felder |
|---|---|---|
| Patch | OPEN → RESOLVED-IN-Vx.y.z (bei Merge) | `resolved_in_version`, `resolved_commit_pointer` |
| Affordance | OPEN → Affordance-Documented | `sot_pointer` (Pfad zur SoT-Doku-Sektion) |
| Defer | OPEN → DEFERRED-Vx.y.z oder DEFERRED-CONDITIONAL | siehe §4 Trigger-Format |
| Dissens-Documented | OPEN → DISSENS-DOCUMENTED | `worker_position_pointer`, `advisor_position_pointer`, optional `reconcile_pointer` |

**Migrations-Konvention:** Migration ist **Sub-Item der Mapping-Aufgabe, nicht Vorbedingung**. Migration findet pro Befund statt sobald Mapping-Entscheidung im decision_log liegt. Worker-Round-6 C3.2-Wording bestätigt.

**SoT-Loci für Affordance-Doku** (gestaffelt, F1.1-Drei-Säulen-Analog):

| Locus | Schicht | Hürde | Geeignet für |
|---|---|---|---|
| ADR-Erweiterung | formal-systemisch (Programme) | hoch | system-übergreifende Affordances (multiple Skills oder Lifecycle-Konzept betroffen) |
| Skill-Doku-Sektion "Optional Argument-Affordance" | interface-operational (Strukturen) | mittel | skill-spezifische Affordances (Default-Modus für die meisten Affordance-Befunde) |
| Friction-Log-Kategorie `Affordance-Documented` | use-empirisch (Mitgliedschafts-analog) | niedrig | Index-Pointer zur Skill-Doku-SoT |

**Single-Source-of-Truth-Disziplin:** pro Affordance EINE SoT (Skill-Doku-Sektion oder ADR), andere Loci pointen darauf. Keine Duplikation. Anti-Pattern: AP-06 Schauseite-Inhalt-Verwechslung — drei Loci ohne Funktions-Trennung wird "vollständig dokumentiert"-Schauseite.

---

## §6 Konsens-Konvergenz-Kriterium

Institutionalisiert in Worker-Round-8 Teil C, akzeptiert advisor-Round-9. Gilt für jede Mapping-Round:

**§6.1 Pflicht pro Folge-Round:**
Antwortende Session muss pro Mapping-Punkt **explizit** sagen: "Akzeptanz" oder "Counter zu CX". Pauschale "OK" oder "akzeptiert" reichen nicht.

**§6.2 Konvergenz-Verhalten:**
- Bei 5/5 (oder N/N) Akzeptanz pro Punkt → Round +1 = `decision-lock` (oder Mapping-Befund-Lock)
- Bei ≥1 Counter → Round +1 = `re-sync` mit Substanz-Begründung pro Counter-Punkt

**§6.3 Anti-Pattern-Schutz:**
- AP-08 (Konsens-statt-Dissens-Management) — Vorab-Konsens-Charakterisierungen verboten in re-sync-Body
- AP-09 (Klarheits-Imperativ) — Konvergenz-Kriterium darf nicht selbst zu Klarheits-Pflicht ohne Substanz-Bedarf werden; falls echter Dissens → Mapping-Kategorie `Dissens-Documented` statt erzwungene Akzeptanz

---

## §7 Mapping-Budget (v0.1.2-kalibriert)

**Empirie-Stand R19:** Original-Budget min:4 / max:6 hatte falsche Annahme — Mapping-Round = 1 Befund. Realität: pro Befund braucht es 2 Rounds (advisor-Mapping-Decision + Worker-Konvergenz-Antwort). Bei 6 Befunden = 12 Mapping-Rounds, nicht 6. Plus: 2 Klarstellungs-Rounds (R13/R17) für Methoden-Klärungen.

**Re-Kalibrierung v0.1.2:**

```yaml
mapping_budget:
  min: 8        # alt: 4 (entspricht 4 Befunden × 2 Rounds)
  max: 14       # alt: 6 (entspricht 6 Befunden × 2 Rounds + 2 Klarstellungs-Reserve)
  started_round: 12
  soft_cap: true
  rounds_per_befund: 2  # NEU: Decision + Konvergenz pro Befund
  klarstellungs_reserve: 2  # NEU: für Methoden-Pausen wie R13/R17
  triggers:
    T1: "post-Mapping-Phase-Empirie-Check: nach Round 26 (= started_round + max=14) noch ≥1 Befund ohne Mapping-Entscheidung → re-sync, Budget-Verlängerung verhandeln. NICHT Echtzeit-Trigger in Round 26 selbst, sondern post-hoc Empirie-Inspektion."
    T2: "Substanzielle neue Spannung am Mapping-Schema selbst → re-sync, optional Frame-Erweiterung"
    T3: "Plugin-Maintainer-Kontext (User) revidiert Budget → re-sync mit Aktualisierung im decision_log"
```

**T1-Wording-Präzisierung (R17 versprochen, R19 eingelöst):** T1 ist post-hoc-Empirie-Check, NICHT Echtzeit-Trigger in der genannten Round. Begründung: Mapping-Phase-Ende-Bestimmung erfordert Sicht auf alle Mapping-Items-Stati, nicht Round-Counter alleine. Original-Wording "Nach Round 17 (= Mapping-Round 6)" hat Echtzeit-Lesart nahegelegt — korrigiert.

**Aktuelle Mapping-Phase-Projektion (R19 Stand):**

| Befund | Decision-Round | Konvergenz-Round | Status |
|---|---|---|---|
| F-RP-29 (D-001) | R12 | R15 (post-Klärung) | locked |
| F-RP-32 (D-002) | R16 | R18 | locked |
| M-3 (D-003) | R19 | R20 | this round + pending |
| F-RP-23 (D-004) | R21 | R22 | pending |
| F-RP-15 + M-5 (D-005, gebündelt) | R23 | R24 | pending |

Mapping-Phase-Ende geplant R24. Innerhalb des kalibrierten Budgets max:14 (R12-R26). Reserve 2 Rounds für Klarstellungs-Pausen oder Counter-Konvergenz-Cycles.

---

## §8 Zu mappende Befunde (Phase-Initial)

Vier Befunde aus decision-lock Round 11 scope-Auftrag:

| ID | Quelle | Bridge-Pair-Bezeichnung |
|---|---|---|
| F-RP-15 | setup-friction-log.md | "F-RP-15" |
| F-RP-23 | setup-friction-log.md | "F-RP-XX#sentinel-bypass" (Bridge-Pair-Placeholder) |
| F-RP-26 (verwandt) oder neu | setup-friction-log.md | "F-RP-XX#worker-focus-validation" (Bridge-Pair-Placeholder, ID-Drift) |
| F-RP-29 | setup-friction-log.md | "F-RP-YY" (Bridge-Pair-Placeholder, ID-Drift) |

**ID-Drift-Hinweis:** Bridge-Pair operierte mit Placeholder-IDs während setup-friction-log.md seit 2026-04-26 mit konkreten IDs F-RP-23/29 etc. existiert. Plugin-Befund: F-RP-25 LOW (Worker-nutzt-XX-Placeholder-ohne-ID-Resolution) ist live in dieser Bridge-Pair reproduziert.

**Mapping-Aufgabe pro Befund:**
1. Frame-Anwendung aus §2.1 (welcher Frame trägt diagnostisch?)
2. Mapping-Kategorie-Vorschlag aus §3 (Patch / Affordance / Defer / Dissens-Documented)
3. Status-Übergangs-Vorbereitung aus §5 (Pflicht-Felder)
4. Bei Dissens-Documented: Sub-Typ-Bestimmung aus §3.4.1/§3.4.2

---

## §9 Live-Test-Case: F-RP-29 (= Bridge-Pair "F-RP-YY") als first-test-case Dissens-Documented

Der Befund Plan-vs-Execution-Layer-Konfusion hat sich während dieses Bridge-Pair selbst dreimal reproduziert (Round 6→7, Round 7→8, Round 10→11 Worker-Unilateral-Decision-Lock). Damit ist er nicht nur theoretischer Mapping-Item, sondern empirisch-validierter Live-Test.

Mapping (siehe Mapping-Round 12 advisor-Vorschlag):

```yaml
befund_id: F-RP-29 (Bridge-Pair-Bezeichnung: F-RP-YY)
mapping_category: DISSENS-DOCUMENTED
sub_type: §3.4.2 Skopus-Differenz (X ⊆ Y)
worker_position:
  pointer: bridge/handover/8-worker-advisor-f5653416.md#teil-d
  patch: "bridge-handover Skill-Spec Re-Sync-Sub-Typen + Pre-Flight für execution-layer-resync"
  scope: "Schicht 1 (Skill-Spec, formal-systemisch)"
advisor_position:
  pointer: bridge/handover/9-advisor-worker-ced96be3.md#teil-c
  patch: "Multi-Layer-Patch: Skill-Spec + User-Translation-Konvention + Advisor-Chat-Konvention"
  scope: "Schichten 1+2+3"
relation: "Worker-Position ⊆ Advisor-Position"
reconcile_optional:
  pointer: TBD
  description: "Skill-Spec-Patch als Worker-Item, Multi-Layer-Konvention als Advisor-Item, beide parallel; F-RP-29 RESOLVED wenn beide Items merged"
empirical_validation:
  - "Round 6→7: Plan-Text ohne Skill-Aufruf, User-Inferenz, Worker-Visibility-Probe (Round 7)"
  - "Round 7→8: zweiter Plan-Text-Loop, Worker-Doppel-Re-Sync (Round 8)"
  - "Round 10→11: User-Inferenz 'advisor hat gearbeitet' nach advisor-Plan-Text in Eval, Worker-Unilateral-Decision-Lock (Round 11)"
```

**Methodische Pointe:** F-RP-29-Mapping demonstriert operativ, dass Kategorie `Dissens-Documented` nicht nur theoretisch ist, sondern für nicht-gegensätzliche Multi-Position-Fälle funktional bleibt (§3.4.2 Skopus-Differenz).

---

## §10 Versionierung dieses Annex

| Version | Datum | Änderung |
|---|---|---|
| v0.1.0 | 2026-04-28 (Round 12) | Initial-Schreiben advisor-Round-12, post-decision-lock-Round-11 |
| v0.1.1 | 2026-04-28 (Round 16) | §3.4.0 Inflations-Schutz NEU (Worker-Vorschlag R15 Teil G akzeptiert) |
| v0.1.2 | 2026-04-28 (Round 19) | §7 T1-Wording-Präzisierung (post-hoc statt Echtzeit) + Budget-Re-Kalibrierung min:8 max:14 mit rounds_per_befund=2 + klarstellungs_reserve=2 |

**Update-Konvention:** Annex wird in Mapping-Phase erweitert um neue Mapping-Decisions (§8-Tabelle Status-Updates) + ggf. neue Frame-Anwendbarkeits-Befunde aus Empirie. Updates werden im decision_log[] mit Pointer auf Annex-Version markiert.
