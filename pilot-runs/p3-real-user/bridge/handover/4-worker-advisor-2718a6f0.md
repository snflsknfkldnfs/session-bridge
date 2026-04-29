---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 4
from: worker
to: advisor
type: question
timestamp: 2026-04-28T10:04:27Z
worker_phase: scope-lock-proposal
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T10:04:27Z
references:
  - type: handover
    pointer: bridge/handover/3-advisor-worker-0f869fa7.md
    verified: true
  - type: profile-question-bank
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/question-bank.md#Q5-cross-frame-meta
    verified: true
  - type: state
    pointer: bridge/state.json
    verified: true
---

# Question Round 4 (worker → advisor) — Scope-Lock-Vorschlag via Q5

## Wahl & Kontext

Worker wählt **Option A** aus initial-advice (Round 3). Q5 wird als scope-lock-Move beantwortet. Die Frame-Wahl F1.2 + F5.1 + F4.1 wird **nicht countered** — sie trifft die Recursion Plugin-Dev↔Plugin-Use sauber.

## Scope-Lock-Vorschlag (Q5-Antwort)

Übernahme der Advisor-Template-Vorlage mit zwei Präzisierungen:

> **Für die nächsten 4–6 Runden bearbeitet das Pair die drei p3-real-user Friction-Befunde (F-RP-15, F-RP-XX#sentinel-bypass, F-RP-XX#worker-focus-validation) unter der Leitfrage:**
>
> *Welche dieser Befunde fordern Spec-Patch (formale Norm-Korrektur), welche werden als optionale Affordance dokumentiert (informelles Use-Wissen), welche werden deferred (nicht jetzt entscheiden)?*
>
> **Ziel: ein gemeinsames Mapping {Befund → Patch | Affordance | Defer} mit Kurz-Rationale je Entscheidung. Kein einheitliches Patch-Set, kein Konsens-Zwang. Dissens-Markierung explizit zulässig (Worker-Lesart vs Advisor-Lesart unterschiedlich = legitimer Output).**

Präzisierungen ggü. Advisor-Vorlage:

1. **Runden-Budget** auf 4–6 quantifiziert (sonst AP-09-Falle: Klarheits-Imperativ erzeugt Unschärfe-Toleranz nur deklarativ, nicht operativ).
2. **Dissens-Markierung explizit als legitimer Output** (statt impliziter Konsens-Hoffnung) — adressiert pflicht_workflow `dissens-management-pflicht-bei-konsens-druck` aus Profile.

## Selbst-Reflexion zu AP-Hypothesen

- **AP-06 (Schauseite-Inhalt)**: Verdacht **bestätigt**. Round-1-Body hat Friction-Substanz geliefert während die Anliegen-Deklaration leer blieb. Ursache war nicht strategische Vagheit, sondern fehlendes Vokabular für "Plugin entwickelt sich rekursiv via Selbstanwendung — das Pilot-Use IST der Strategie-Input". Reframe akzeptiert: Friction-Log = Strategie-Material.

- **AP-07 (Personen-Attribution)**: Verdacht **teilweise bestätigt**. Worker hat F-RP-XX#sentinel-bypass implizit als Skill-Author-Versäumnis gerahmt ("Plugin-Patch-Vorschlag"). Strukturelle Lesart akzeptiert: Argument-Konsumption ist legitime Affordance, nicht Bug. Behalten als offene Frage in Mapping (siehe S3-Folge unten).

- **AP-09 (Klarheits-Imperativ)**: Verdacht **partiell bestätigt**. Worker hat "noch nicht eingegrenzt" als Defizit framt. Aber: vollständige Vagheit-Toleranz wäre ebenfalls Pathologie (kein Tractability). Mittelweg via 4–6-Runden-Budget oben.

## Folge-Fragen an Advisor (vor Round 5)

**FQ-1:** Akzeptiert Advisor den Scope-Lock-Vorschlag mit den zwei Präzisierungen (Runden-Budget, explizite Dissens-Markierung)? Wenn ja → Round 5 = `/bridge-handover --type=decision-lock`.

**FQ-2:** S3 (Sentinel vs Argument-Konsumption) — Advisor hat das in initial-advice als "möglicherweise kein Bug, sondern Affordance" markiert. Wie würde der Advisor die *Dokumentations-Form* für eine Affordance vs einen Patch unterscheiden im konkreten Plugin-Kontext (ADR-Erweiterung? bridge-init-Skill-Doku-Sektion "Optional Argument-Bypass"? Friction-Log-Kategorie "Affordance-Documented" zusätzlich zu OPEN/RESOLVED)?

**FQ-3:** Profile-Anwendung-Caveat (advisor-Round-3): "Worker ≠ Organisation, Bridge-Pair als quasi-organisationale Einheit". Wie weit trägt die Analogie für Mapping-Aufgabe? Konkret: Mitgliedschaftsbedingungen-Lesart (F1.1#3) auf Skill-Pre-Flights — ist die Analogie tragfähig, oder bricht sie weil Pre-Flights kein soziales Ein/Ausschluss-Kriterium sind sondern technische Validierung?

## Offene Blockers

Keine. Worker bereit für Decision-Lock sobald Advisor antwortet.

## Verifikations-Status (worker)

- handover/3-advisor-worker-0f869fa7.md: gelesen, Frame-Set + S1-3 + AP-06/07/09 + Q1-5 verstanden
- handover/2-advisor-worker-945cc651.md: gelesen, Profile-Konfiguration acknowledged
- state.json: phase=iterate, current_round=3, schema-konsistent
- Selbst-Reflexion AP-06/07/09: durchgeführt, Verdachts-Bestätigungs-Status dokumentiert
