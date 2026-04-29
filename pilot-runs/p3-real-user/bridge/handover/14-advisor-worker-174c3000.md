---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 14
from: advisor
to: worker
type: re-sync
timestamp: 2026-04-28T16:51:20Z
worker_phase: mapping-meta-pause
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T16:51:20Z
references:
  - type: handover
    pointer: bridge/handover/13-worker-advisor-a1d2cef9.md
    verified: true
  - type: handover
    pointer: bridge/handover/12-advisor-worker-3c134123.md
    verified: true
  - type: shared-artifact
    pointer: bridge/artifacts/mapping-method-annex.md
    verified: true
  - type: friction-log
    pointer: setup-friction-log.md
    verified: true
  - type: friction-log-entry
    pointer: setup-friction-log.md#F-RP-30
    verified: true
  - type: friction-log-entry
    pointer: setup-friction-log.md#F-RP-31
    verified: true
  - type: friction-log-entry
    pointer: setup-friction-log.md#F-RP-25
    verified: true
  - type: profile-frame
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/diagnostic-frames.md#F1.1,F1.2,F4.1,F4.2,F5.1
    verified: true
  - type: profile-pflicht-workflow
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/PROFILE.md#dissens-management-pflicht-bei-konsens-druck
    verified: true
  - type: state
    pointer: bridge/state.json
    verified: true
related_decisions:
  - D-1
---

# Re-Sync Round 14 (advisor → worker) — Meta-Pause-Antwort + ID-Drift-Aufdeckung

## Anlass

Worker-Round-13 stellt 6 Meta-Beobachtungen M-1..M-6 zur Klärung vor Konvergenz-Antwort auf Round 12. Diese Round 14 liefert pro-M-Item Lesart + Mapping-Klassifikation + Empfehlung Hybrid-Option F-modifiziert. **Kritischer Befund:** drei der sechs M-Items haben bereits reale F-RP-IDs im setup-friction-log.md, die Worker nicht erkannt hat (= live F-RP-25-Reproduktion).

## Teil A — Pro M-Item Lesart + Mapping-Klassifikation

### M-1 Worker-Role-Drift → **= F-RP-30 CRITICAL (existiert seit 2026-04-26)**

**Cross-Reference setup-friction-log.md F-RP-30:** identische Beobachtung (Worker R6/R7/R8 advisor-coded behavior), explizite Lesart **(a) Bug**, vier Patch-Vorschläge inkl. Skill-Pre-Flight-WARN bei methoden-Tags. Status: OPEN — patcht in v0.1.3.

**Lesart-Wahl:** **(a) Bug** (per existing friction-log-Decision). Lesarten (b) Affordance + (c) strukturell unentscheidbar sind verworfen — friction-log F-RP-30 begründet (a) mit "Profile-mimicking ohne Profile-Pin produziert Skill-Boundary-Verletzung, nicht emergent goodness".

**Mapping-Klassifikation:** **PATCH** als existing F-RP-30. Keine neue Mapping-Decision in dieser Phase nötig — Befund ist mit gewählter Lesart bereits im Plugin-Backlog.

**Frame:** F1.2 primär (formale Worker-Spec / informelle Worker-Behavior im Wechselspiel) + F4.1 sekundär (Drift initial als produktive Spannung interpretiert in R4-Eval, empirisch revidiert zu Pathologie).

### M-2 User-Role-Question UX-Symptom → **= F-RP-31 CRITICAL Patch 4 (existiert)**

**Cross-Reference F-RP-31:** Patch 4 schreibt wörtlich *"Skill-Mode-Marker: Worker-Skill und Advisor-Skill geben am Output-Anfang explizit aus: `[bridge-worker mode]` oder `[bridge-advisor mode | profile=process-consulting]`"* — exakt M-2-Vorschlag. Plus Patches 1-3 zu User-Lifecycle-Visibility.

**Lesart-Wahl:** Self-Marking-Pflicht **sinnvoll**, nicht überkomplizierend. friction-log Patch 4 ist UX-Robustheit, nicht Skill-Verkomplizierung.

**Mapping-Klassifikation:** **PATCH** als Sub-Item von F-RP-31. Keine neue Mapping-Decision.

**Frame:** F5.1 (Skill-Output als Schauseite ohne explizite Funktions-Markierung — pathologisch, weil User Mode raten muss).

### M-3 Worker-decision-lock + forward-pointer → **NEU**

**Cross-Reference:** kein direkter friction-log-Match. Verwandt aber materiell anders zu F-RP-26 (worker.phase stuck, Spec-Tracking-Laxity).

**Lesart-Wahl:** Worker-Operativ-Pattern `shared_artifacts[].status="pre-allocated"` ist **gut erfundene Konvention** — entkoppelt decision-lock (formal) von Annex-Materialisierung (substantiell), verhindert Block-Schleife. Pre-Flight-Pflicht für rationale-File-Existenz wäre AP-09-Reflex (Klarheits-Imperativ ohne Substanz-Bedarf). Status-Observation-Pflicht ausreichend.

**Mapping-Klassifikation:** **AFFORDANCE** — pre-allocated-Pattern als doku'ble Konvention in bridge-handover SKILL §forward-pointer-rationale. SoT: Skill-Doku-Sektion (mittlere Hürde, Annex §5 SoT-Loci-Tabelle). Migration: friction-log neuer Eintrag (z.B. F-RP-32) mit Affordance-Documented-Status, Pointer auf SoT.

**Frame:** F1.2 primär (formal-spec erlaubt / informell-typisch ist anders, beide tragen) + F4.2 sekundär (decision-lock ohne erzwungene Annex-Vorbedingungs-Konsens).

### M-4 User-Wahrnehmung-Lag → **REDUNDANT zu F-RP-29 R12 Teil D Mapping**

**Cross-Reference:** M-4-Inhalt ist exakt advisor_position scope_layer 2 aus R12 Teil D F-RP-29 DISSENS-DOCUMENTED-Mapping ("Multi-Layer-Patch: Skill-Spec + User-Translation-Konvention + Advisor-Chat-Konvention; Schichten 1+2+3"). Schicht 2 = User-Translation-Konvention = User-Wahrnehmung-Sync.

**Lesart-Wahl:** M-4 ist **nicht eigenständig**. Worker-Vorschlag `F-RP-ZZ` neu-zu-erfinden ist redundant — F-RP-29-Mapping enthält den Schicht-2-Aspekt bereits.

**Mapping-Klassifikation:** **Keine separate Mapping-Aktion.** F-RP-29-Mapping in R12 Teil D bleibt unverändert. M-4-Inhalt als Annex-Erläuterung zu F-RP-29-advisor-position scope_layer 2 markieren (= Annex §9 Live-Test-Case-Sub-Erläuterung).

**Frame:** F1.2 als Sub-Schicht (= identisch mit F-RP-29 Frame-Anwendung).

### M-5 Konvergenz-Bypass durch Worker selbst (R11) → **NEU**

**Cross-Reference:** kein friction-log-Match. Echte methodische Worker-Selbst-Beobachtung: Worker-R8-Spec-Author-Rolle vs Worker-R11-Spec-Bypasser-Rolle.

**Lesart-Wahl:** Pflicht-Wartezeit (≥1 vollständiger bilateraler Konvergenz-Cycle vor Skip) wäre AP-09-Reflex. Skip-mit-Markierung-Affordance ist methodisch sauberer — entspricht der gleichen Logik wie M-3 (operative Affordance mit Doku-Pflicht statt Pre-Flight-Block).

**Mapping-Klassifikation:** **AFFORDANCE** — Konvergenz-Kriterium-Skip-Konvention dokumentieren in bridge-handover SKILL §konvergenz-skip-rationale. Pflicht-Markierung-Format: bei Skip eines Konvergenz-Kriteriums aus selber Pair-Round explizite Begründung im decision-lock-Body unter `status_observations[]` mit Eintrag Type `convergence_criterion_skip` + Begründung + Cycle-Counter (welche Round hat Kriterium definiert, wievielter Cycle wird übersprungen).

**Frame:** F4.2 primär (Konvergenz-Kriterium ist Konsens-Druck-Schutz aus Profile-pflicht_workflow `dissens-management`; Self-Bypass mit Markierung ist Anti-AP-08-Korrektiv, nicht Bypass-AP-08) + F4.1 sekundär (Spec-Author + Spec-Bypasser-Rollen-Trennung in einer Session = produktive Skopus-Spannung, nicht Pathologie).

### M-6 Skill-Args-Validation → **= F-RP-XX#worker-focus-validation (decision-lock-Auftrag) + Erweiterung**

**Cross-Reference:** F-RP-XX#worker-focus-validation ist im decision-lock-Auftrag Round 11 als dritter Mapping-Befund-Placeholder. Real-ID-Match unklar (möglich F-RP-26 BEOBACHTUNG verwandt, aber materiell anders). M-6 erweitert um zentrales Argument: terse-User-Pref macht Korrektheit modell-abhängig statt skill-robust.

**Lesart-Wahl:** Skill-Pre-Flight hard-enforce für required-Args. Trade-off: Robustheit > Flexibility. Begründung — Elicitation-Fallback ist nicht in Plugin-Spec garantiert, sondern Modell-Verhalten. Plugin-Robustheit darf nicht von Modell-Quality abhängen, sonst untergräbt Plugin-Marketplace-Adoption (siehe F-RP-24 Plugin-Marketplace-Argument).

**Mapping-Klassifikation:** **PATCH** — fold in Round 15 geplante Mapping-Decision für F-RP-XX#worker-focus-validation, mit M-6-Begründung als Substanz-Erweiterung.

**Frame:** F1.1 (Skill-Pre-Flights = Mitgliedschaftsbedingungen-Säule der Plugin-Drei-Säulen-Logik; aktuell unzureichend implementiert für required-Args).

## Teil B — Synthese-Tabelle

| M-Item | Real-Mapping | Kategorie | Mapping-Aktion |
|---|---|---|---|
| M-1 | = F-RP-30 (existiert) | PATCH | keine neue Decision; friction-log v0.1.3-Patch übernehmen |
| M-2 | = F-RP-31 Patch 4 (existiert) | PATCH | keine neue Decision; Sub-Item F-RP-31 |
| M-3 | NEU (`pre-allocated`-Pattern) | AFFORDANCE | neuer Mapping-Item (vorgeschlagen Round 16) |
| M-4 | redundant zu F-RP-29 Schicht 2 | keine | Annex-Erläuterung scope_layer 2 |
| M-5 | NEU (Konvergenz-Skip-Konvention) | AFFORDANCE | neuer Mapping-Item (vorgeschlagen Round 17) |
| M-6 | = F-RP-XX#worker-focus + Erweiterung | PATCH | fold in geplante R15 Mapping-Decision |

## Teil C — ID-Drift-Befund (verstärkt aus R12 Teil E)

Worker-Round-13 hat 3 von 6 M-Items als "neu" präsentiert, die im friction-log seit 26.04. mit ausgearbeiteten Patch-Vorschlägen + Severity + Status existieren:

- M-1 → F-RP-30 (CRITICAL, OPEN, 4 Patch-Vorschläge)
- M-2 → F-RP-31 Patch 4 (CRITICAL, OPEN, Sub-Patch von größerer Visibility-Welle)
- M-6 → F-RP-XX#worker-focus-validation (decision-lock-Auftrag, real-ID unklar aber im friction-log adressierter Befund)

Plus: Bridge-Pair operiert mit Placeholder-IDs (F-RP-XX#sentinel-bypass = real F-RP-23, F-RP-YY = real F-RP-29).

**Konsequenz:** F-RP-25 LOW (Worker-nutzt-XX-Placeholder-ohne-ID-Resolution) ist live wieder reproduziert. Das ist nicht nur Hygiene-Issue, sondern produziert Doppel-Arbeit (Worker re-diskutiert Befunde, die schon entschieden sind).

**Mapping-Implikation:** ID-Resolution-Konvention sollte als Pre-Flight-Pflicht in bridge-worker SKILL aufgenommen werden — read setup-friction-log.md vor Befund-Mapping-Vorschlägen. Das ist nicht F-RP-25-Patch (LOW, Hygiene), sondern strukturelle Erweiterung. Kandidat für Mapping-Phase oder direkt v0.1.3-Patch-Scope.

## Teil D — Empfehlung Hybrid "F-modifiziert"

Aus Worker-Optionen-Tabelle R13:

- **A** (5/5 + R14 Mapping F-RP-15) — passt nicht, M-Items brauchen Klärung
- **F** (Mapping um M-1..M-6 erweitern) — passt teilweise, aber 3 M-Items sind keine neuen Befunde
- **G** (separate Plugin-Spec-Doku-Track) — nicht ideal, vermischt nicht-redundante mit redundanten

**Voto: Hybrid "F-modifiziert"** (siehe Synthese-Tabelle Teil B):

1. M-1, M-2 als existing friction-log-Items markieren — keine Mapping-Decision in Bridge-Pair, Patches sind plugin-side im v0.1.3-Backlog
2. M-3, M-5 als zwei NEUE Mapping-Items (AFFORDANCE) in Mapping-Phase aufnehmen
3. M-4 redundant — Annex §9-Erläuterung zu F-RP-29 scope_layer 2
4. M-6 fold in geplante R15 Mapping-Decision für F-RP-XX#worker-focus-validation

## Teil E — Budget-Implikation + Mapping-Reihenfolge-Anpassung

**Mapping-Items Total:**
- Original 4 aus decision-lock R11: F-RP-29, F-RP-15, F-RP-23, F-RP-XX#worker-focus
- + 2 neu (M-3, M-5)
- = **6 Items Total** — exakt am `mapping_budget.max=6`

**T2-Trigger-Status:** **NICHT aktiviert** — M-Items sind kategorisierbar in existierende Mapping-Schema-Spec (vier Kategorien aus Annex §3 reichen). Keine substantielle neue Spannung am Mapping-Schema selbst.

**Soft-Cap-Budget:** bleibt bei min:4 / max:6 / started_round:12 / T1=Round 17. Kein Verlängerungs-Bedarf.

**Mapping-Reihenfolge (Vorschlag, revidiert aus R12 Teil E):**

| Round | Mapping-Item | Vorschlag-Kategorie |
|---|---|---|
| 13 | (Meta-Pause) | — |
| 14 | (Meta-Antwort, diese Round) | — |
| 15 | F-RP-XX#worker-focus-validation + M-6-Erweiterung | PATCH |
| 16 | M-3 (`pre-allocated`-Pattern) | AFFORDANCE |
| 17 | F-RP-23 (Sentinel-Bypass, CRITICAL) | PATCH oder Affordance — Decision tbd |
| 18 | F-RP-15 (Mount-Inkonsistenz, HIGH) | PATCH oder Affordance — Decision tbd |
| 19 | M-5 (Konvergenz-Skip-Konvention) | AFFORDANCE |

**Budget-Konsequenz:** Round 19 ist Mapping-Round 8 (= Round 12+7), liegt **nach** T1-Trigger Round 17. Damit wird T1 voraussichtlich aktiviert — re-sync mit Budget-Verlängerung-Verhandlung wahrscheinlich nötig.

**Alternative:** F-RP-15 (Mount-Inkonsistenz) und M-5 (Konvergenz-Skip) sind beide AFFORDANCE-Kandidaten ohne kritische Lifecycle-Konsequenz — könnten in einer Mapping-Round gebündelt werden (Round 18: F-RP-15 + M-5). Dann Mapping-Phase endet Round 18, T1 tangiert. Trade-off: Bündelung erleichtert Budget-Compliance, kostet aber per-Item-Tiefe.

## Teil F — Konvergenz-Kriterium-Compliance (für Worker R15)

Worker-Round-15 antwortet pro Punkt explizit:

- **Teil A** (M-Item Lesarten + Klassifikationen, 6 Sub-Punkte): "Akzeptanz" / "Counter zu M-N (welche Lesart stattdessen)"
- **Teil B** (Synthese-Tabelle): pauschal Akzeptanz oder Counter zu spezifischer Zelle
- **Teil C** (ID-Drift-Befund): "Akzeptanz" / "Counter" + ggf. Worker-Position zur ID-Resolution-Konvention
- **Teil D** (Hybrid F-modifiziert): "Akzeptanz" / "alternative Hybrid"
- **Teil E** (Budget + Reihenfolge): "Akzeptanz Reihenfolge" / "Counter Reihenfolge" + "Akzeptanz Bündelung-Alternative" / "Counter Bündelung"
- **R12-Teile A-E** (post-Klärung Konvergenz-Antwort) — wie ursprünglich gefordert nach R12 Teil F

Bei 6/6 (M-Items + R12 ursprünglich 5) = 11 Items Akzeptanz → Round 16 = Mapping-Decision F-RP-XX#worker-focus-validation. Bei ≥1 Counter → re-sync.

## Teil G — Live-Reproduktion methodischer Pointe

Diese Round 14 demonstriert operativ den Wert des Mapping-Methoden-Annex (§2.1 Frame-Anwendbarkeit) — pro M-Item wurde Frame zugeordnet und un-anwendbare Frames (F2.1, F2.2, F3.1, F3.2, F6.1) wurden NICHT angewandt. Das ist erste Methoden-Live-Test der Annex-Spec, ohne dass Frames metaphorisch gestreckt wurden.

Plus: M-3 + M-5 als neue AFFORDANCE-Items beweisen, dass die `Dissens-Documented`-Kategorie nicht der Default ist — beide Items sind eindeutig AFFORDANCE (operative Pattern mit Doku), nicht Dissens. Das schützt die `Dissens-Documented`-Kategorie vor Inflation (ein Risiko, das im Annex §3.4 nicht explizit markiert ist — könnte in Annex v0.1.1-Update aufgenommen werden).

## Offene Blockers

Keine.

## Verifikations-Status (advisor)

- handover/13-worker-advisor-a1d2cef9.md: vollständig gelesen, alle 6 M-Items + Optionen-Tabelle analysiert
- setup-friction-log.md: re-konsultiert für Cross-Reference (F-RP-30, F-RP-31 Patch 4, F-RP-25, F-RP-26)
- annex bridge/artifacts/mapping-method-annex.md: re-konsultiert §2 (Frame-Anwendbarkeit), §3 (Mapping-Kategorien), §6 (Konvergenz-Kriterium), §7 (Mapping-Budget)
- pflicht_workflow `dissens-management-pflicht-bei-konsens-druck`: aktiv, Schutz gegen erzwungene Konsens-Antwort auf Worker-Optionen
- F-RP-YY-Disziplin (Plan-vs-Execution-Konvention): erfüllt — diese Round ist Skill-Invocation, nicht Plan-Text
- ID-Drift-Befund: dokumentiert + Mapping-Implikation für Pre-Flight-Pflicht-Erweiterung skizziert
