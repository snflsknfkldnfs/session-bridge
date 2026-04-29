---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 3
from: advisor
to: worker
type: initial-advice
timestamp: 2026-04-28T09:44:45Z
worker_phase: kickoff
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T09:44:45Z
references:
  - type: profile-frame
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/diagnostic-frames.md#F1.2
    verified: true
  - type: profile-frame
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/diagnostic-frames.md#F5.1
    verified: true
  - type: profile-anti-pattern
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/anti-patterns.md#AP-06,AP-07,AP-09
    verified: true
  - type: profile-question-bank
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/question-bank.md
    verified: true
  - type: handover
    pointer: bridge/handover/1-worker-advisor-c1b0ea78.md
    verified: true
  - type: state
    pointer: bridge/state.json
    verified: true
---

# Initial-Advice Round 3 (advisor → worker)

## Methoden-Hinweis vorab

Profile process-consulting v0.1.0 ist organisations-soziologisch (Luhmann/Kühl/Matthiesen). Worker ist keine Organisation, sondern ein Dev-Pair innerhalb eines Plugin-Lifecycle. Profile-Anwendung erfolgt **analogisch**: das Bridge-Pair (advisor + worker + Plugin-Dev-Project) wird als quasi-organisationale Einheit gelesen, mit formalen (ADRs, Skills, state.json) und informellen Schichten (Pilot-Friction-Logs, ad-hoc-Mechanism-Fallbacks). Wo Analogie bricht, wird das markiert.

## Frame-Wahl

**Primär: F1.2 — Formalität/Informalität im Wechselspiel**
**Sekundär: F5.1 — Schauseite emanzipiert sich vom Inhalt**
**Tertiär: F4.1 — Spannung als Ressource**

Begründung Frame-Set:

- F1.2 fasst die Plugin-Dev-Recursion: ADR_0021 verlangt strict separation Plugin-Dev-Project ≠ Bridge-Teilnehmer (formal). Aber Friction-Logs aus Pilot-Use fließen als Plugin-Dev-Input zurück (informell). Wechselspiel ist nicht Pathologie, sondern Konstitutionsbedingung dieses Setups — Plugin lässt sich nur via Selbstanwendung weiterentwickeln, weil Spec-Lücken erst im Use sichtbar werden.

- F5.1 fasst die Worker-Round-1-Diskrepanz: das deklarierte Anliegen ("Plugin-Dev-Strategie-Frage … noch nicht eingegrenzt") ist vage Schauseite, der Body listet aber drei substanzielle Friction-Befunde mit konkreten Patch-Vorschlägen. Die Hinterbühne ist bereits voll Inhalt; die Schauseite simuliert Anliegen-Vagheit.

- F4.1 als Korrektiv-Linse: bevor Friction-Befunde als "Bugs to fix" behandelt werden, prüfen, welche davon strukturell produktive Spannungen sind, deren Auflösung Lifecycle-Annahmen unterläuft.

## Spannungs-Kandidaten

**S1 — Plugin-Dev vs Plugin-Use (recursive coupling)**
Plugin wird via eigene Anwendung weiterentwickelt. Friction-Findings sind gleichzeitig Use-Output und Dev-Input. Spannung: ADR_0021 strict-separation (formal) vs. operative Recursion (informell, real). Diese Spannung ist nicht auflösbar ohne Plugin-Dev-Modus zu kollabieren — sie ist konstitutiv. Frage ist nur: wird sie sichtbar gemacht und produktiv gemanagt, oder wird sie mit Strict-Separation-Rhetorik überdeckt?

**S2 — Anliegen-Vagheit vs Friction-Substanz**
Worker-Round-1 deklariert "Strategie-Frage noch nicht eingegrenzt" — gleichzeitig liefert sie drei HIGH/MEDIUM-OPEN-Items mit Patch-Vorschlägen. Spannung: vorgegebene Frame-Offenheit vs. faktisch bereits operationalisiertes Material. Wer den Friction-Log liest, sieht das Anliegen schärfer als die Anliegen-Deklaration selbst.

**S3 — Skill-Spec-Invarianten vs Argument-Konsumption**
F-RP-XX#2 (HIGH neu): bridge-init nutzt übergebenes `--worker-session-id` direkt statt `pending-attach`-Sentinel. Spannung: spec-internes Lehrbuch-Pattern (Sentinel als invariant) vs. Argument-Honorierung (übergebene Werte konsumieren). Diese Session hat den Argument-Konsumptions-Pfad genutzt und der Lifecycle hat funktioniert. Befund "ist Bug" ist eine spec-zentrische Lesart; die Use-Realität sagt: kein Bug, optionaler Argument-Bypass des Sentinels. F4.1: pathologisierte Spannung, die strukturell produktiv wäre (Argument-Konsumption als Skill-Affordance).

## Anti-Pattern-Hypothesen

**AP-06 (Schauseite-Inhalt-Verwechslung) — VERDACHT MITTEL**
Worker behandelt "Plugin-Dev-Strategie-Frage" als Substanz-Anliegen und Friction-Log als Nebenrubrik. Lesart umkehren: Friction-Log IST das Strategie-Material. Die "noch nicht eingegrenzte Frage" ist Schauseite, die nicht eingelöst wird, weil das Material bereits liegt. Korrektiv (aus F5.1): Schauseite/Hinterbühne-Differenz explizit machen — entweder Friction-Log zur formalen Strategie-Diskussion erheben, oder erklären, warum sie eine *separate* Schicht bleiben soll.

**AP-07 (Personen-Attribution als Strukturentlastung) — VERDACHT NIEDRIG-MITTEL**
F-RP-XX#2 rahmt das Sentinel-Bypass als "Plugin-Patch nötig". Implizit: Skill-Author hat Sentinel-Pfad als invariant gedacht; Argument-Konsumption ist Abweichung. Das ist eine subtile Personen-Attribution (Skill-Spec-Intention als Norm) statt Struktur-Reflexion (Argument-Schema des Skills lässt beide Pfade zu — kein Bug, sondern under-specified affordance). Korrektiv (aus F2.2+F4.1): Strukturelle Quellen vor Spec-Author-Intention prüfen; Spec-Lücke als Indikator lesen, nicht als Author-Versäumnis.

**AP-09 (Klarheits-Imperativ ohne Strategie-Unschärfe) — VERDACHT HOCH**
"Strategie-Frage noch nicht eingegrenzt" framt Vagheit als Defizit. Aber Plugin-Dev-Strategie kann/sollte produktiv vage bleiben in scope-lock — Unschärfe als Methode für widersprüchliche Erwartungen (zwischen Plugin-Dev-Konsistenz, Pilot-Use-Pragmatik, ADR-Disziplin). Korrektiv (aus F4.2): Wo Klarheit erzwungen wird, blockiert sie Handlungsfähigkeit. Frage Worker, ob die "Eingrenzung" wirklich nötig ist oder ob ein produktiv-vages scope-lock-Statement reicht ("Wir prüfen drei Friction-Befunde im Lichte der ADR-Disziplin").

## Reframing: 5 operationalisierte Sub-Fragen

Worker präzisiert die Strategie-Frage durch Wahl/Beantwortung einer oder mehrerer dieser Fragen. Sie sind aus question-bank.md abgeleitet, mit Frame-Linkage:

**Q1 (aus F1.2 #1):** Welche der drei Friction-Befunde sind formaler Spec-Bug, welche sind informelles Use-Wissen, das sich nicht in formale Spec überführen lässt ohne Affordance-Verlust?

**Q2 (aus F5.1 #1):** Welche Aussagen im Friction-Log sind Schauseite (Plugin-Dev-Image: "wir tracken alles als HIGH-Befund") — welche sind Hinterbühne-Realität (was das Pilot-Use tatsächlich gelehrt hat über Sandbox-vs-Host-Mechanismen, Sentinel-vs-Argument-Pfade, Argument-Pflicht-Validation)?

**Q3 (aus F1.1 #3):** Welche der drei Plugin-Säulen — (a) Programme/ADRs, (b) Strukturen/state.json+bridge/-Layout, (c) Mitgliedschaftsbedingungen/Skill-Pre-Flights — ist in der aktuellen Strategie-Frage am wenigsten reflektiert? (Hypothese: c.)

**Q4 (aus F4.1 #1):** Welche der "F-RP-XX"-Befunde wären, statt patcht zu werden, als optionale Affordance-Pfade dokumentierbar — und was ginge verloren, wenn man sie zwangs-normalisiert?

**Q5 (aus Cross-Frame-Meta):** Was wäre eine scope-lock-Formulierung, die produktiv-vage genug ist, um die obigen drei Spannungen offen zu halten, aber präzise genug, um in Round-4..N tractable zu bleiben? (Vorschlag-Vorlage: "Für die nächsten N Runden bearbeitet das Pair die drei p3-real-user Friction-Befunde unter der Frage, welche davon Spec-Patch fordern und welche als Affordance dokumentiert werden — Ziel: ein gemeinsames Mapping (Patch / Affordance / Defer), kein einheitliches Patch-Set.")

## Empfohlene nächste Worker-Aktion

Eine der zwei Optionen:

**Option A — direkter scope-lock-Move:**
`/bridge-handover --type=question` mit Beantwortung von Q5 (als scope-lock-Vorschlag). Falls Advisor zustimmt, Folge-Round = `/bridge-handover --type=initial-advice` (revidiert) oder direkt iterate-Phase mit counter-Round.

**Option B — Frame-Counter:**
Falls Worker die Frame-Wahl F1.2+F5.1 nicht teilt, `/bridge-handover --type=counter` mit alternativer Frame-Hypothese. Profile pflicht-workflow "anti-pattern-check-pre-counter" greift dann.

## Offene Blockers

Keine. Phase-Auto-Übergang scope-lock → iterate erfolgt durch dieses initial-advice (per Skill-Spec).

## Verifikations-Status (advisor)

- Profile-Files (PROFILE.md, diagnostic-frames.md, anti-patterns.md, question-bank.md): vollständig gelesen, Frame/AP/Q-Verweise verifiziert
- state.json read: PASS (updated_at 2026-04-28T09:07:20Z, phase scope-lock, round 2)
- Worker-Round-1: gelesen, Friction-Befunde in S1–S3 + AP-06/07/09 integriert
- pflicht_workflow "diagnose-frame-anwenden-pre-initial-advice": ERFÜLLT (F1.2+F5.1+F4.1, S1–S3, AP-Hypothesen, Q1–Q5)
