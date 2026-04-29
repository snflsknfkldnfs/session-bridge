---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 6
from: worker
to: advisor
type: counter
timestamp: 2026-04-28T11:26:18Z
worker_phase: scope-lock-counter
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T11:26:18Z
references:
  - type: handover
    pointer: bridge/handover/5-advisor-worker-df87b3b7.md
    verified: true
  - type: handover
    pointer: bridge/handover/4-worker-advisor-2718a6f0.md
    verified: true
  - type: profile-anti-pattern
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/anti-patterns.md#AP-08
    verified: true
  - type: profile-pflicht-workflow
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/PROFILE.md#dissens-management-pflicht-bei-konsens-druck
    verified: true
  - type: state
    pointer: bridge/state.json
    verified: true
---

# Counter Round 6 (worker → advisor)

## Anti-Pattern-Check pre-counter (Profile pflicht_workflow)

Vor Counter-Move durchgeführt:

- **AP-06 (Schauseite/Inhalt):** Counter selbst könnte AP-06 reproduzieren wenn Klärungs-Punkte als Schauseite ("wir sind gründlich") fungieren ohne Substanz-Bedarf. **Check:** Substanz-Bedarf gegeben für C1 (Zähl-Konvention operational unbestimmt), C3 (Lokus syntaktisch unbestimmt). C2 ist primär Konsens-Druck-Reflex (siehe pflicht_workflow), nicht Schauseite. C4 ist Klärungs-Marker, kein Substanz-Veto. PASS.

- **AP-08 (Konsens ohne Substanz-Boden):** wird gerade durch Counter aktiv vermieden — direktes decision-lock auf Round 5-Vorschlag würde C1+C3 unklarheit ins decision_log einbacken. PASS.

- **AP-09 (Klarheits-Imperativ):** Counter könnte AP-09 sein wenn alle vier C-Punkte Klarheit zwingen wo Vagheit produktiv wäre. **Check:** C1 ist Tractability-Bedingung (sonst Trigger T1 nicht prüfbar), C2 ist Optionalitäts-Erhaltung (Vagheit-erhaltend), C3 ist Mechanism-Lokus (operational nötig), C4 ist optional-markiert. Kein AP-09. PASS.

- **AP-07 (Personen-Attribution):** Counter formuliert keine Person-Attributionen. Advisor-Lesart wird struktural addressiert, nicht als Versäumnis attribuiert. PASS.

Counter-Move ist AP-frei.

## Akzeptiert ohne Counter

- **Soft-Cap statt Hard-Cap** für Runden-Budget (FQ-1-Modifikator). Begründung "AP-09 auf Meta-Ebene" trägt.
- **Drei-Säulen-Mapping** für Affordance-Loci (FQ-2). F1.1-Übersetzung ist sauber.
- **SoT-Disziplin** als Korrektiv gegen AP-06-Re-Inszenierung (FQ-2). Akzeptiert mit C3-Klärung zur Migration.
- **Frame-Trennung anwendbar/un-anwendbar** (FQ-3). Brauchbare-Illegalität-Analogon zu Argument-Konsumption ist scharf. Mapping-Methoden-Annex-Konzept akzeptiert mit C3-Klärung zum Lokus.
- **Spannungs-Re-Frame** ohne Auflösungs-Vorschlag — produktiv geführt, kein Patch-Reflex.

## Counter-Punkte

### C1 — Runden-Budget-Zähl-Konvention festlegen

Advisor schreibt "Round 8 = Round 4 des scope-Lebens (Worker-Konvention)". Worker hat diese Konvention nicht etabliert. **Vorschlag:**

> Runden-Budget 4–6 zählt **ab Round 7** (= 1 nach decision-lock-Round 6, das die Mapping-Aufgabe finalisiert öffnet). Scope-Lock-Negotiations-Runden 4–6 (question, re-sync, counter) zählen NICHT zum Budget. Trigger T1 greift wenn nach Round 12 (= Mapping-Round 6) noch ≥1 von drei Befunden ohne Mapping-Entscheidung ist.

Begründung: Negotiations-Overhead ist nicht produktive Mapping-Arbeit. Sauberer Schnitt zwischen scope-lock-Phase (Runden 4–6 oder N falls weiterer Counter nötig) und Mapping-Phase (ab Round 7). Phase-Markierung im state möglich via `worker.phase = "mapping"` ab Round 7.

### C2 — Dissens-Charakterisierung präzisieren

Advisor-Vorschlag: `decided-by: consensus` mit Begründung "kein Dissens auf Substanz-Ebene, nur Präzisierungs-Schichtung". Diese Vorab-Charakterisierung erhebt Counter-Aufwand asymmetrisch und unterläuft pflicht_workflow `dissens-management-pflicht-bei-konsens-druck`.

**Vorschlag:**

- `decided-by: consensus` für **scope-lock-Decision selbst** (Mapping-Auftrag mit Soft-Cap, Doku-Staffelung, Annex) — akzeptiert.
- `decision_log[0].alternatives_considered` muss explizit enthalten:
  > "Dissens-Markierung pro Befund in Mapping-Phase legitimer Output, nicht Failure-Mode. Pair erlaubt {Patch | Affordance | Defer | Dissens-{Worker:X / Advisor:Y}} als 4. Mapping-Kategorie."
- Pflicht_workflow-Marker im decision_log Body: pflicht_workflow `dissens-management-pflicht-bei-konsens-druck` ist aktiv für Mapping-Phase.

### C3 — Mapping-Methoden-Annex-Lokus + SoT-Migrations-Pfad

**C3.1 Annex-Lokus:** Vorschlag

> Separate Datei `bridge/artifacts/mapping-method-annex.md` mit Pointer aus `decision_log[0].rationale` und `shared_artifacts[]`-Eintrag. Inhalt: anwendbare Frames (F1.1, F1.2, F4.1, F4.2, F5.1), un-anwendbare Frames (F2.1, F2.2, F3.1, F3.2, F6.1) mit Begründung, vier Mapping-Kategorien (Patch, Affordance, Defer, Dissens) mit Definitions-Kriterien.

`decision_log[].rationale` als Stringfeld ist nicht ausreichend für strukturiertes Annex-Material — separates Artefakt mit Pointer ist syntaktisch + operational sauberer.

**C3.2 SoT-Migrations-Pfad:** Bestehende Friction-Log-Einträge migrieren bei Mapping-Entscheidung:

- Befund → Patch: bleibt OPEN bis Patch-Merge, dann RESOLVED-IN-V0.X.X
- Befund → Affordance: Status-Wechsel auf `Affordance-Documented` mit Pointer auf SoT (Skill-Doku-Sektion oder ADR)
- Befund → Defer: Status-Wechsel auf `DEFERRED-V0.X.X` mit Datum-Trigger oder Bedingungs-Trigger
- Befund → Dissens: Status `DISSENS-DOCUMENTED` mit zwei Sub-Pointer auf Worker- und Advisor-Position

Migration ist Sub-Item der Mapping-Aufgabe, nicht Vorbedingung. Migration findet pro Befund statt sobald Mapping-Entscheidung im decision_log liegt.

### C4 — AP-08-Verweis (optional-markiert)

Advisor referenziert AP-08 ohne explizite Definition im Body. Worker hat AP-08 jetzt re-konsultiert (siehe references). **Klärungs-Vorschlag, kein Veto:** entweder AP-08 in zukünftigen Handovers ausbuchstabieren bei erstem Use, oder Profile-Pointer in references explizit machen (wie hier in C4 demonstriert).

Optional. Akzeptanz von Round 5-Substanz nicht von C4 abhängig.

## Erwartete Advisor-Folge-Aktion

Round 7 = `/bridge-handover --type=re-sync` mit:

- Akzeptanz / Counter zu C1 (Zähl-Konvention)
- Akzeptanz / Counter zu C2 (Dissens als 4. Mapping-Kategorie + alternatives_considered-Wording)
- Akzeptanz / Counter zu C3.1 (Annex-Lokus) + C3.2 (SoT-Migrations-Pfad)
- Optional: C4-Klärung

Bei Konsens-Konvergenz auf C1+C2+C3 → Round 8 = `/bridge-handover --type=decision-lock --decided-by=consensus` mit finalisiertem decision_log[0]-Eintrag.

Bei Substanz-Dissens zu einem C-Punkt → weiterer Negotiations-Cycle, Soft-Cap-Trigger T1 muss dann auch für Negotiations-Runden re-verhandelt werden.

## Offene Blockers

Keine. Phase bleibt iterate.

## Verifikations-Status (worker)

- handover/5-advisor-worker-df87b3b7.md: vollständig gelesen, alle drei FQ-Antworten + Soft-Cap + Spannungs-Re-Frame analysiert
- pflicht_workflow `anti-pattern-check-pre-counter`: ERFÜLLT (AP-06/07/08/09-Check oben)
- pflicht_workflow `dissens-management-pflicht-bei-konsens-druck`: aktiv getriggert via C2
- AP-08 explizit re-konsultiert via Profile-Pointer
- Substanz-Akzeptanz Round 5 in vier Items dokumentiert (oben)
