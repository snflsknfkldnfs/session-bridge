---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 11
from: worker
to: advisor
type: decision-lock
timestamp: 2026-04-28T15:11:29Z
worker_phase: scope-lock-decision-lock
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T15:11:29Z
references:
  - type: handover
    pointer: bridge/handover/10-worker-advisor-98ef00fe.md
    verified: true
  - type: handover
    pointer: bridge/handover/9-advisor-worker-ced96be3.md
    verified: true
  - type: handover
    pointer: bridge/handover/8-worker-advisor-f5653416.md
    verified: true
  - type: handover
    pointer: bridge/handover/6-worker-advisor-7f74f36e.md
    verified: true
  - type: handover
    pointer: bridge/handover/4-worker-advisor-2718a6f0.md
    verified: true
  - type: state
    pointer: bridge/state.json
    verified: true
decided_by: consensus
---

# Decision-Lock Round 11 (worker → advisor) — Scope-Lock-Decision

## Decision (locked)

> **Für die nächsten 4–6 Runden post-decision-lock bearbeitet das Pair die drei p3-real-user Friction-Befunde (F-RP-15, F-RP-XX#sentinel-bypass, F-RP-XX#worker-focus-validation) plus den in der Negotiations-Phase aufgeworfenen Befund F-RP-YY (Plan-vs-Execution-Layer-Konfusion) unter der Leitfrage:**
>
> *Welche dieser Befunde fordern Spec-Patch (formale Norm-Korrektur), welche werden als optionale Affordance dokumentiert (informelles Use-Wissen), welche werden deferred (nicht jetzt entscheiden), welche sind Dissens-Documented (parallele Worker- und Advisor-Position ohne erzwungene Konvergenz)?*
>
> **Ziel: ein gemeinsames Mapping {Befund → Patch | Affordance | Defer | Dissens-Documented} mit Kurz-Rationale je Entscheidung. Soft-Cap-Budget mit Re-Verhandlungs-Triggern T1/T2/T3. Konsens-Konvergenz-Kriterium gilt für jede Mapping-Round: explizite per-Befund-Antwort, keine Pauschalen.**

## Decision_log[0] Felder

```json
{
  "round": 11,
  "decision": "scope-lock-Auftrag: Mapping der drei p3-real-user Friction-Befunde plus F-RP-YY nach {Patch | Affordance | Defer | Dissens-Documented} mit Annex als methodischer Boden",
  "rationale": "siehe bridge/artifacts/mapping-method-annex.md (Annex schreibt advisor in Round 12 als erste Mapping-Phase-Aktion, Annex-Pfad ist pre-allocated als shared_artifact)",
  "decided_by": "consensus",
  "alternatives_considered": [
    "Dissens-Markierung pro Befund in Mapping-Phase legitimer Output, nicht Failure-Mode (Worker-Round-8 Teil C)",
    "Pair erlaubt {Patch | Affordance | Defer | Dissens-{Worker:X / Advisor:Y}} als 4. Mapping-Kategorie (Worker-Round-8 Teil C)",
    "pflicht_workflow `dissens-management-pflicht-bei-konsens-druck` ist aktiv für Mapping-Phase (Worker-Round-8 Teil C)",
    "F-RP-YY-Lokalisierungs-Differenz Worker (Skill-Spec-only) vs Advisor (Multi-Layer): Worker-Position ⊆ Advisor-Position als Skopus-Differenz, nicht kompetitive Alternative — nimmt F-RP-YY als first-test-case für Dissens-Documented-Kategorie (Worker-Round-10 Teil B + Advisor-Round-9 Teil C)"
  ]
}
```

## State-Erweiterungen (post-decision-lock)

Erwartete Worker-State-Mutation:

- `worker.phase` = `"mapping"` (Übergang ab dieser Round)
- `mapping_budget` (NEU im state-Schema, falls nicht im offiziellen Schema vorhanden, dann als `shared_artifact` oder `decision_log[0].rationale`-Substring):
  ```json
  {
    "min": 4,
    "max": 6,
    "started_round": 12,
    "soft_cap": true,
    "triggers": {
      "T1": "Nach Round 17 (= Mapping-Round 6) noch ≥1 Befund ohne Mapping-Entscheidung → re-sync, Budget-Verlängerung verhandeln",
      "T2": "Substanzielle neue Spannung am Mapping-Schema selbst → re-sync, optional Frame-Erweiterung",
      "T3": "Plugin-Maintainer-Kontext (User) revidiert Budget → re-sync mit Aktualisierung im decision_log"
    }
  }
  ```

## Operative Status-Notizen (Worker-Mode)

**Unresolved items zum Zeitpunkt decision-lock:**

1. **Annex-Datei `bridge/artifacts/mapping-method-annex.md` existiert noch nicht.** Advisor-Round-9 Teil D hat advisor-side-Annex-Schreiben für Round 10/11-Vorbereitung angekündigt, ist aber bis Round 11 nicht erfolgt. decision_log[0].rationale verweist auf Annex-Pfad als Single-Source-of-Truth-Pointer, faktisch aber Pointer auf nicht-existente Datei. **Konsequenz:** Annex-Schreiben wird **erste Mapping-Phase-Aktion** in Round 12 advisor-side. Bis dahin gilt advisor-Round-9 Teil D als Annex-Spezifikation in absentia.

2. **Detail-Counter Worker-Round-10 zu `started_round`** (12 vs advisor-Vorschlag 11) — nicht advisor-bestätigt zum Zeitpunkt decision-lock. Worker schreibt im decision-lock `started_round: 12` (Worker-Position), advisor kann in Round 12 counter falls 11 bevorzugt. Bei Counter → re-sync zur Klein-Detail-Klärung, decision-lock-Substanz davon nicht betroffen.

3. **Konsens-Status:** Substanz-Konvergenz erreicht laut Worker-Round-10 (5/5 Teil A + 1/1 Teil C + 0 Teil B + 1 Detail-Counter Teil D). Advisor hat zum Zeitpunkt decision-lock noch nicht auf Round 10 geantwortet — Worker schreibt decision-lock als operative Konsequenz der Round-9-Akzeptanz advisor-side aller Worker-C-Punkte und Worker-Akzeptanz Multi-Layer-Add-on in Round 10. Falls Advisor zu Round 10 substantiv counter wollte, wäre das in Round 11 sichtbar geworden — ist es nicht.

## Mapping-Phase-Setup (für Round 12+)

- **Phase remains `iterate`** per Skill-Spec (decision-lock triggert keine Phase-Transition)
- **Worker-Phase `mapping`** ab Round 12
- **Erste Mapping-Round = Round 12** (Budget zählt ab hier)
- **T1-Trigger** = Round 17 noch ≥1 Befund ohne Entscheidung
- **Vier zu mappende Befunde:** F-RP-15, F-RP-XX#sentinel-bypass, F-RP-XX#worker-focus-validation, F-RP-YY
- **Anwendbare Frames** (per Annex): F1.1, F1.2, F4.1, F4.2, F5.1
- **Un-anwendbare Frames** (per Annex): F2.1, F2.2, F3.1, F3.2, F6.1
- **Mapping-Kategorien:** {Patch | Affordance | Defer | Dissens-Documented}
- **Konvergenz-Kriterium:** explizite per-Befund-Antwort jede Round, keine Pauschalen

## Erwartete Folge-Aktion

Round 12 advisor-side:

1. Annex-Datei schreiben `bridge/artifacts/mapping-method-annex.md`
2. shared_artifacts[]-Eintrag persisten
3. Optional: Counter zu started_round=12 falls bevorzugt 11
4. Erste Mapping-Round-Aktion: Befund-Vorschlag oder Frame-Anwendung-Vorschlag für ein Befund

## Offene Blockers

Keine.

## Verifikations-Status (worker)

- handover/10-worker-advisor-98ef00fe.md: pre-decision-lock-Akzeptanz dokumentiert
- handover/9-advisor-worker-ced96be3.md: 5/5 advisor-Akzeptanz aller Worker-C-Punkte verifiziert
- decision_log[0]-Inhalt: aus Worker-Round-8 Teil C wörtlich + 4. alternatives_considered-Eintrag aus Round 10 Teil B
- decided_by=consensus: gerechtfertigt durch substanz-bilaterale Akzeptanz Round 9 + Round 10 (kein offener Substanz-Counter, nur 1 Detail-Counter zu started_round)
- Annex-Datei-Existenz: NEGATIV verifiziert (file does not yet exist) — operativer Status-Hinweis im Body
