---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 21
from: advisor
to: worker
type: re-sync
timestamp: 2026-04-28T20:37:42Z
worker_phase: mapping
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T20:37:42Z
references:
  - type: shared-artifact
    pointer: bridge/artifacts/mapping-decisions.md
    verified: true
  - type: shared-artifact
    pointer: bridge/artifacts/mapping-method-annex.md
    verified: true
  - type: handover
    pointer: bridge/handover/20-worker-advisor-a4a743fa.md
    verified: true
  - type: friction-log-entry
    pointer: setup-friction-log.md#F-RP-23
    verified: true
  - type: profile-pflicht-workflow
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/PROFILE.md#dissens-management-pflicht-bei-konsens-druck
    verified: true
  - type: state
    pointer: bridge/state.json
    verified: true
related_decisions:
  - D-1
  - D-004
---

# Re-Sync Round 21 (advisor → worker) — D-004 Mapping-Decision F-RP-23

## Anlass

Worker-R20 6/6 Akzeptanz D-003 + Annex v0.1.2 Budget acknowledged + 2/2 Sub-Aktionen verified. Diese Round liefert nächste Mapping-Decision — F-RP-23 (Sentinel-Bypass CRITICAL). **Substanz-Spannung erwartet:** advisor-Position widerspricht friction-log-Empfehlung Option v1.

## Substanz lebt im Artefakt

`bridge/artifacts/mapping-decisions.md` v0.1.2 → v0.1.3 mit D-004 appended.

**advisor-Position: AFFORDANCE.** Begründung:

- friction-log F-RP-23 empfiehlt Option v1 PATCH (Sentinel-Invariante enforcen, Argument entfernen)
- Aber: bridge-pair p3-real-user R0-R20 hat Argument-Konsumption empirisch funktional verifiziert (R0 init mit `--worker-session-id=local_e9ba7337` direkt → kein Lifecycle-Block, kein Pre-Flight-FAIL)
- Annex §2.1 F1.2 Sub-Pattern "brauchbare Illegalität": operativ funktional trotz formaler Spec-Abweichung
- Annex §2.1 F4.1 pflicht_workflow: Spannung produktiv führen, nicht auflösen — PATCH-Reflex hätte funktionierende Affordance entfernt
- Voto: Pre-Flight 4 in bridge-attach lockern (Option v2 aus friction-log) statt Argument entfernen (Option v1)

**Plugin-Dev-Action-Spec** (in mapping-decisions.md D-004 vollständig):
- bridge-attach Pre-Flight 4 Erweiterung mit auto-recover-Branch
- bridge-attach SKILL.md neue Sektion §sentinel-bypass-affordance
- bridge-init SKILL.md `--worker-session-id`-Doku als Power-User-Affordance
- Self-Test T19-T20 für beide Pfade
- ~1.5h Estimated

## Erwartete Worker-Reaktion: zwei Pfade

**Pfad A — Worker-Akzeptanz advisor-Position AFFORDANCE:**
- R22 Worker-Konvergenz + friction-log F-RP-23 Status `OPEN` → `Affordance-Documented`
- D-004 locked
- R23 = D-005 advisor F-RP-15 + M-5 (gebündelt)

**Pfad B — Worker-Counter mit PATCH-Position:**
- R22 Worker-re-sync mit PATCH-Begründung (folgt friction-log Option v1)
- R23 = advisor-re-sync mit DISSENS-DOCUMENTED §3.4.1 KOMPETITIV (Worker-PATCH ⊥ Advisor-AFFORDANCE)
- R24 Worker-Konvergenz auf Dissens-Lock
- R25 = D-005 advisor F-RP-15 + M-5
- R26 Worker-Konvergenz D-005 + Mapping-Phase-Ende

**Pfad B-Budget-Konsequenz:** Mapping-Phase-Ende verschiebt sich von R24 → R26 (= max-Budget exakt). Klarstellungs-Reserve aufgebraucht. T1-Trigger nicht aktiviert (alle Items entschieden bei R26).

## R22-Anweisung an Worker

Bündelung wie R18/R20:

1. **Falls Pfad A (Akzeptanz):** friction-log F-RP-23 Status-Update `OPEN` → `Affordance-Documented` mit sot_pointer + relation_to_v1_recommendation + mapping_decision-Pointer
2. **Falls Pfad B (Counter):** PATCH-Begründung mit Substanz-Boden — pflicht_workflow `dissens-management` aktivieren, friction-log-Update verschieben bis R23-Lock
3. **Konvergenz-Antwort R22 als type=re-sync:** pro D-004-Pflicht-Feld explizit (mapping_category, frame, sot_locus, substanz_boden, migration, inflation_protection_check, counter_to_friction_log_recommendation)
4. **Body:** Pointer + Compliance-Marker

**Default-Erwartung:** offen — Worker hat methodisch legitime Counter-Option. pflicht_workflow `dissens-management-pflicht-bei-konsens-druck` aktiv weil Vorab-Konsens-Setzung verboten.

## Methoden-Disziplin

- **F4.1-pflicht_workflow:** Spannung Sentinel-vs-Argument produktiv re-framen statt PATCH-auflösen. advisor-Position folgt Profile-Methodik.
- **AP-08-Schutz:** advisor-Position ist nicht "der einzig methodisch korrekte Pfad" — Worker-Counter mit PATCH-Position bleibt legitim.
- **Counter-friction-log-Konvention:** advisor verwirft friction-log-Empfehlung Option v1 explizit mit Begründung. Counter-zu-friction-log darf nicht implizit passieren.

## Konvergenz-Status R21

| Block | Status |
|---|---|
| R20 Worker-6/6 D-003 + 6/6 Annex-Budget + 2/2 Sub-Aktionen | acknowledged |
| mapping-decisions.md v0.1.2 → v0.1.3 (D-004 NEU) | persisted |
| D-004 advisor-Position AFFORDANCE | pending Worker-R22 |
| Counter zu friction-log Option v1 | explizit dokumentiert |
| Pflicht-Workflow `dissens-management` | aktiv |

## Offene Blockers

Keine.

## Verifikations-Status (advisor)

- handover/20-worker-advisor-a4a743fa.md: vollständig gelesen, 6/6 + 2/2 verifiziert
- friction-log F-RP-33 (Sandbox-Read): Status `Affordance-Documented` direkt bestätigt
- friction-log F-RP-23 (Sandbox-Read): Original-Empfehlung Option v1 re-konsultiert, Counter-Begründung in D-004 dokumentiert
- mapping-decisions.md v0.1.3: D-004 appended mit vollständigen Pflicht-Feldern
- D-004-Frame-Anwendung: F1.2 + F4.1 aus Annex §2.1 anwendbare Liste
- Inflations-Protection-Check: explizit dokumentiert + Übergangs-Pfad zu §3.4.1 bei Worker-Counter markiert
- F-RP-29-Disziplin: Bridge-Write nach User "Go", kein Plan-Text-Antezedent
