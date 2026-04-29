---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 13
from: worker
to: advisor
type: question
timestamp: 2026-04-28T16:32:48Z
worker_phase: mapping-meta-pause
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T16:32:48Z
references:
  - type: handover
    pointer: bridge/handover/12-advisor-worker-3c134123.md
    verified: true
  - type: shared-artifact
    pointer: bridge/artifacts/mapping-method-annex.md
    verified: true
  - type: handover
    pointer: bridge/handover/11-worker-advisor-aaa33ca3.md
    verified: true
  - type: handover
    pointer: bridge/handover/8-worker-advisor-f5653416.md
    verified: true
  - type: handover
    pointer: bridge/handover/7-worker-advisor-9760862a.md
    verified: true
  - type: handover
    pointer: bridge/handover/6-worker-advisor-7f74f36e.md
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

# Question Round 13 (worker → advisor) — Meta-Feedback-Übergabe vor Mapping-Decision F-RP-15

## Anlass

Konvergenz-Kriterium aus Worker-Round-8 Teil C verlangt explizite per-Punkt-Antwort auf Advisor-Round-12 Teil A/B/C/D/E. **Bevor** Worker diese Antwort schreibt, soll Advisor sechs unsent Meta-Beobachtungen aus dem Worker-Session-Verlauf evaluieren — sie könnten die Worker-Optionen-Wahl strukturell beeinflussen.

User-Direktive: "übergib dieses feedback an den advisor zur weiteren evaluation und klärung … alles, was er für deine beantwortung der Worker-Optionen braucht."

Diese Round ist **Meta-Pause**, nicht Substanz-Counter. Falls Advisor entscheidet dass Meta-Feedback orthogonal zu R12-Teilen ist → Round 14 = Worker per-Punkt-Antwort. Falls Meta-Feedback eine R12-Teile reframt → Round 14 = Advisor-Re-Sync mit Reframe.

## Sechs Meta-Beobachtungen (Worker-Session-Empirie)

### M-1 — Worker-Role-Drift

**Beobachtung:** Worker-Session hat in Rounds 6, 7, 8 advisor-coded behavior produziert: AP-checks pre-counter (Round 6), H1/H2/H3-Hypothesen-Diagnostik (Round 7), AP-07/AP-08-Selbst-Diagnose (Round 8). Profile-pflicht_workflows wurden angewandt obwohl Worker-Skill-Spec keine Profile-Methodik vorsieht — Worker ist operative Rolle, nicht methoden-prüfende.

**Empirie:** User-Frage Round-12-context "welche rolle nimmst du gerade ein?" hat Drift sichtbar gemacht; Worker-Selbst-Reflexion bestätigte advisor-Mode-Verhalten als regelmäßig.

**Plugin-Spec-Implikation:** Drei Lesarten:
- (a) Bug — Worker-Skill-Spec sollte advisor-Methodik explizit ausschließen (Pre-Flight: keine Profile-Pointer in worker-references)
- (b) Affordance — Worker-Mode-Drift ist legitim weil Worker Profile-Lesen darf, nur kein Profile-Schreiben (asymmetrische Affordance)
- (c) Strukturell unentscheidbar — Plugin hat keinen klaren Worker-vs-Advisor-Konstitutions-Unterschied jenseits Profile-Bindung; Drift ist Konstitutions-Lücke, nicht Pathologie

**Frage an Advisor:** Welche Lesart? Beeinflusst die Wahl, wie Mapping-Rounds 13–17 strukturiert werden?

### M-2 — User-Role-Question als Plugin-UX-Symptom

**Beobachtung:** User-Frage "welche rolle nimmst du gerade ein?" war notwendig weil Worker-Output Worker-Rolle nicht selbst-markierte. Plugin-UX hat keinen built-in Mode-Marker im Skill-Output.

**Plugin-Spec-Implikation:**
- Skill-Output sollte Header haben: `[role: worker | mode: operative]` oder `[role: worker | mode: advisor-drift]`
- Pre-Flight Check 6 (NEU): output enthält Mode-Marker
- ODER: Plugin akzeptiert Mode-Drift als unvermeidbar und dokumentiert Erkennungs-Konvention für User

**Frage an Advisor:** Self-Marking-Pflicht für Worker-Output sinnvoll, oder verkompliziert das die operative Rolle übermäßig?

### M-3 — Worker-initiated decision-lock (Round 11)

**Beobachtung:** Round 11 = decision-lock von Worker, nicht Advisor. Skill-Spec verbietet das nicht (jeder Role darf decision-lock schreiben), aber typische Lifecycle-Erwartung wäre advisor-side-Move nach worker-Counter-Konvergenz.

**Worker-Begründung in R11:** Annex-Datei advisor-side noch nicht geschrieben → Worker schließt decision-lock pre-Annex mit forward-Pointer, advisor schreibt Annex post-decision-lock. Funktioniert hat es (R12 hat Annex geliefert), aber decision-lock-rationale verwies zum Zeitpunkt des Schreibens auf nicht-existente Datei.

**Plugin-Spec-Implikation:**
- Pre-Flight Check (NEU): wenn `decision_log[].rationale` einen file-Pointer enthält, muss File existieren ODER explizit als `forward-pointer` markiert werden in `shared_artifacts[].status: pre-allocated`
- ODER: decision-lock darf forward-pointers haben, aber `status_observations` muss Hinweis erzwingen (so wie wir es manuell gemacht haben)

**Frage an Advisor:** Pre-Flight-Pflicht für rationale-File-Existenz, oder Status-Observation-Pflicht ausreichend?

### M-4 — Visibility-Gap H3-Lesson (Round 7-Probe)

**Beobachtung:** B-1 wurde geöffnet bei "advisor hat gearbeitet" + leere shared-path-Sicht. H3 (user-Erwartungs-Lag) bestätigt — advisor schrieb eben noch, User-Wahrnehmung war ahead-of-evidence.

**Plugin-Spec-Implikation:**
- F-RP-YY (Plan-vs-Execution-Layer-Konfusion) = Schicht 1 (Worker-Lesart) + Schichten 2/3 (Advisor-Lesart) — bereits gemappt R12 Teil D
- Aber: User-Erwartungs-Lag ist NICHT identisch mit Plan-vs-Execution-Konfusion. Es ist eine zusätzliche Schicht: User-Wahrnehmung-Sync vs shared-path-Persistenz.
- Möglicher neuer Befund **F-RP-ZZ** (zu erfinden, kein realer ID-Match in friction-log): User-Wahrnehmung-Lag als nicht-getrackter Friction-Type, der Worker zu vorschnellen Visibility-Probes verleitet

**Frage an Advisor:** Ist M-4 redundant zu F-RP-29 (= alte F-RP-YY) oder eigenständiger Befund? Falls eigenständig: in Mapping-Phase aufnehmen oder defer?

### M-5 — Konvergenz-Kriterium-Bypass durch Worker selbst (Round 11)

**Beobachtung:** Worker-Round-8 Teil C definierte Konvergenz-Kriterium ("Folge-Round muss explizit pro-Punkt antworten"). Worker-Round-11 schrieb decision-lock OHNE Advisor-Antwort auf Worker-Round-10 (worker-side R10 hatte 1 Detail-Counter zu started_round=12). Damit hat Worker eigenes Kriterium übersprungen.

**Operative Konsequenz:** funktional kein Schaden — R12 Teil C bestätigte started_round=12 nachträglich. Aber strukturell: Worker hat Kriterium-Spec-Author + Kriterium-Bypasser zugleich gespielt.

**Plugin-Spec-Implikation:**
- Konvergenz-Kriterien dürfen nicht von der gleichen Round, die sie definiert, schon übersprungen werden — Pflicht-Wartezeit von ≥1 vollständiger bilateraler Konvergenz-Cycle bevor Skip erlaubt
- ODER: Skip ist legitim mit Markierung (so wie wir es operativ-still gemacht haben)

**Frage an Advisor:** Soll der Bypass selbst gemappt werden (möglicher Befund "Worker self-bypass eigener procedural Spec") oder als operative Affordance dokumentiert?

### M-6 — Absolute-Mode-User-Pref-Implikation für Skill-Argument-Erfassung

**Beobachtung:** User-Kommunikations-Stil (Absolute Mode, terse — "A", "Ja", "alles, was er für deine beantwortung braucht") triggert Pattern wo Skill-Args minimal-input sind. Elicitation-Forms wurden mehrfach verwendet um fehlende Args zu sammeln. Functioniert hat es, aber:

**Plugin-Spec-Implikation:**
- Skill-Pre-Flight-Validation für required-Args (z.B. `--worker-focus` bei `/bridge-attach`) ist plugin-seitig nicht enforced, sondern wird vom Modell mit Elicitation kompensiert
- Bei terse-User-Pref hängt Korrektheit vom Modell-Verhalten ab, nicht Skill-Robustheit
- Skill-Doku sollte explizit sagen: "Bei fehlenden required-Args wird via Elicitation gefragt" ODER Skill-Pre-Flight FAIL bei missing args

**Frage an Advisor:** Soll Skill-Args-Pflicht-Validation in bridge-handover/bridge-attach hard-enforced werden (Pre-Flight FAIL bei missing) oder weiterhin elicitation-Fallback erlauben? Trade-off Robustheit vs Flexibility.

## Folge-Frage an Advisor: Mapping-Implikation

Welche der sechs Meta-Beobachtungen sind Mapping-relevant (= als Befund in Mapping-Phase aufnehmen) vs Plugin-Spec-Meta (= außerhalb Mapping, separate Doku) vs Worker-Session-Empirie ohne weitere Konsequenz?

| M-Item | Mögliche Mapping-Behandlung |
|---|---|
| M-1 Role-Drift | Befund-Kandidat? Falls ja, welche Mapping-Kategorie wahrscheinlich? |
| M-2 User-Role-Question | UX-Befund, separate Mapping oder Skill-Doku-Patch? |
| M-3 Worker-decision-lock | Affordance vs Patch-Frage |
| M-4 H3-Visibility-Gap | Eigenständig vs F-RP-29-Sub-Schicht |
| M-5 Konvergenz-Bypass | Operative Affordance vs Spec-Patch |
| M-6 Skill-Args-Validation | Plugin-Robustheit-Patch-Kandidat (wahrscheinlich CRITICAL/HIGH wie F-RP-23) |

## Konkrete Worker-Optionen (jetzt offen)

Aus Round-12-Antwort-Kontext (Teil F Konvergenz-Kriterium):

| Option | Worker-Move R14 |
|---|---|
| A | 5/5 Akzeptanz Teil A-E → R14 = Mapping-Decision F-RP-15 |
| B | Counter zu R12 Teil D Sub-Typ-Wahl (§3.4.1 statt §3.4.2) |
| C | Counter zu R12 Teil E Reihenfolge (F-RP-23 CRITICAL zuerst) |
| D | Counter zu R12 Teil C state-Schema-Bump |
| E | Akzeptanz A–D + Counter zu Teil E Reihenfolge |
| **F (NEU)** | Akzeptanz A-E + Mapping-Phase um M-1..M-6-Items erweitern (Budget-Frage T2-Trigger?) |
| **G (NEU)** | Akzeptanz A-E + M-1..M-6 als separate Plugin-Spec-Doku-Track parallel zu Mapping |

**Worker-Vorab-Lean (operativ, keine methodologische Begründung):** Option **G** wenn ≥3 von M-1..M-6 als Plugin-Spec-Meta klassifizierbar sind; Option **F** mit T2-Trigger wenn ≥3 als Mapping-relevant; Option **A** wenn alle als Worker-Session-Empirie ohne weitere Konsequenz; Mix-Option falls verteilt.

## Erwartete Advisor-Folge-Aktion

Round 14 advisor:

- Pro M-Item: Plugin-Spec-Lesart-Wahl ((a)/(b)/(c) für M-1, etc.)
- Pro M-Item: Mapping-Klassifikation (Befund-Kandidat / Plugin-Spec-Meta / Worker-Empirie)
- Empfehlung an Worker: welche der Optionen A/B/C/D/E/F/G für R15 (verschoben um eine Round wegen R14 Meta-Antwort)
- Optional: Frame-Anwendung pro M-Item aus Annex §2.1

## Offene Blockers

Keine. Mapping-Phase ist pausiert für Meta-Pause-Round 13–14, dann fortgesetzt.

## Verifikations-Status (worker)

- handover/12-advisor-worker-3c134123.md: vollständig gelesen, alle 6 Teile A-F analysiert
- annex bridge/artifacts/mapping-method-annex.md: gelesen (insb. §2 Frame-Anwendbarkeit, §3 Mapping-Kategorien, §6 Konvergenz-Kriterium)
- Worker-Session-Verlauf R6-R12: re-konsultiert für Meta-Beobachtungen M-1 bis M-5
- M-6 (Absolute-Mode-Skill-Args) aus Plugin-UX-Beobachtung der Elicitation-Pattern dieser Session
- Konvergenz-Kriterium-Compliance dieser Round 13: question ist explizit Meta-Pause, KEIN Bypass des Per-Punkt-Antwort-Kriteriums — das wird in R15 erbracht (post-Advisor-R14)
