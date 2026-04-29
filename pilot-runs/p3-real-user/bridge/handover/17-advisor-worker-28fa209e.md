---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 17
from: advisor
to: worker
type: re-sync
timestamp: 2026-04-28T18:06:54Z
worker_phase: mapping
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T18:06:54Z
references:
  - type: shared-artifact
    pointer: bridge/artifacts/mapping-decisions.md
    verified: true
  - type: handover
    pointer: bridge/handover/16-advisor-worker-58dd0018.md
    verified: true
  - type: friction-log-entry
    pointer: setup-friction-log.md#F-RP-29
    verified: true
  - type: friction-log-entry
    pointer: setup-friction-log.md#F-RP-26
    verified: true
  - type: state
    pointer: bridge/state.json
    verified: true
related_decisions:
  - D-1
---

# Re-Sync Round 17 (advisor → worker) — R16-Klarstellung + F-RP-29 4. Live-Reproduktion

## Anlass

Worker-Question zu R16-Anweisungs-Unklarheit: 5 Optionen aufgelistet, klare Direktive angefragt. Ursache: R16-Body-Sektion "Worker-Action-Anweisung" hat Bündelung vs Trennung als "Worker-Wahl" übergeben statt klare Direktive zu geben (Konsens-Druck-Vermeidung übertrieben → Anweisungs-Vakuum).

**Plus:** F-RP-29 (Plan-vs-Execution-Layer-Konfusion, in D-001 als DISSENS-DOCUMENTED gemappt) reproduziert sich live zum **vierten Mal** — diese R17-Klarstellung war zunächst nur Plan-Text in advisor-Chat, kein Bridge-Write. User-Korrektur-Frage hat Reproduktion sichtbar gemacht.

## Substanz lebt im Artefakt

Inhalt ist in `bridge/artifacts/mapping-decisions.md` v0.1.1 (UPDATE) appended: D-002-Sub-Sektion "R17-Klarstellung-Annex" mit:

1. **Workflow-Direktive (verbindlich):** Option A — Bündelung. Konvergenz-Antwort + friction-log-Updates D-001 + D-002 in R18 Worker-Move (nicht R17, weil R17 jetzt diese advisor-Klarstellung ist).
2. **F-RP-26 vs F-RP-32 Match-Klärung:** materiell verschieden. F-RP-32 NEW ist korrekt mit Cross-Reference zu F-RP-26.
3. **Konvergenz-Erwartung:** 6/6 Akzeptanz default, kein substantieller Counter-Boden ersichtlich.
4. **Methodische Selbst-Diagnose advisor-side:** R16-Anweisungs-Vakuum als Korrektur-Konvention für Folge-Rounds dokumentiert.

## Round-Zähl-Korrektur

R17 = diese advisor-Klarstellung (statt erwartetem Worker-Konvergenz-Move).
R18 = Worker-Konvergenz-Move + friction-log-Updates (Option A Bündelung).
R19 = D-003 advisor-Mapping-Decision M-3.

Mapping-Phase-Ende verschiebt sich um 1 Round: R20 (statt R19). T1-Trigger Round 17 wäre erreicht; aber **T1 ist nicht aktiviert**, weil "T1: nach Round 17 noch ≥1 Befund ohne Mapping-Entscheidung" — bei R20-Ende ist bei Erfolg 0 Befunde offen. T1-Definition prüft post-hoc nach Round 17, nicht in Round 17.

**Korrektur:** Annex-§7 mapping_budget T1-Wording muss präzisiert werden auf "post-Round-17 Empirie-Check, nicht Round-17-Echtzeit-Trigger". Update in nächstem Annex-v0.1.2 (verschoben).

## R18-Anweisung an Worker (verbindlich, kein Pluralismus)

Per D-002 R17-Klarstellung-Annex:

1. **friction-log F-RP-29 status update:** OPEN → DISSENS-DOCUMENTED + Sub-Pointer per D-001-Spec
2. **friction-log F-RP-32 NEU erstellen:** HIGH-Severity, Inhalt aus D-002 + Cross-Reference F-RP-26 (verwandt-aber-verschieden) + F-RP-24 (Marketplace) + mapping_decision: D-002
3. **Konvergenz-Antwort R18 als type=re-sync:** pro D-002-Pflicht-Feld explizit (real_id, patch_target_files, patch_acceptance_criteria, substanz_boden, frame, migration). Default-Erwartung: 6/6 Akzeptanz.
4. **Body:** Pointer auf friction-log-Sektionen die geupdated wurden + Konvergenz-Compliance-Marker
5. **Optional:** Counter zu shared_artifacts schema_version-Schema-Erweiterung — keine Pflicht.

## Methodische Lehre (für advisor-side, ab R17)

Bei Workflow-Routine-Fragen (Bündelung, Reihenfolge, Format) klare Direktive geben statt Worker-Wahl-Übergabe. Methoden-Pluralismus reservieren für Substanz-Decisions (Frame-Wahl, Mapping-Kategorie, Sub-Typ, Counter-Boden).

Plus F-RP-29-Disziplin verschärft: jede Klarstellung MUSS Bridge-Write sein, nicht Chat-Text. Vier Live-Reproduktionen in 17 Rounds = struktureller Befund advisor-side, nicht einmaliges Versäumnis.

## Konvergenz-Status R17

| Block | Status |
|---|---|
| R16-Anweisungs-Unklarheit | acknowledged + korrigiert |
| F-RP-29 4. Live-Reproduktion | acknowledged + dokumentiert |
| Workflow-Direktive Option A | verbindlich für R18 |
| F-RP-26 vs F-RP-32 Match-Klärung | NEW korrekt |
| Round-Zähl-Verschiebung +1 | T1-Wording-Update verschoben in Annex v0.1.2 |
| mapping-decisions.md v0.1.1 | updated |
| state.json mutations | persistiert post-Skill-Invocation |

## Offene Blockers

Keine.

## Verifikations-Status (advisor)

- Worker-Question (User-forwarded) vollständig adressiert
- mapping-decisions.md v0.1.0 → v0.1.1 mit D-002 R17-Klarstellung-Annex
- friction-log F-RP-26 re-konsultiert für Match-Prüfung
- F-RP-29-Reproduktion advisor-side dokumentiert (4. Mal)
- F-RP-29-Disziplin-Verschärfung als Konvention markiert
- R18-Anweisung verbindlich, kein Pluralismus
