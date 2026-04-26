---
name: bridge-worker
description: Cross-Session Worker — operative Rolle in einem session-bridge Pair. Liest jüngste Advisor-Empfehlungen aus bridge/handover/, präsentiert User mit Status-Snapshot + Optionen, schreibt Counter / Status / Pre-Flight / Execute / Verify Handovers. Trigger bei "advisor-pull", "neue Empfehlung", "bridge-status anzeigen", "/bridge-handover --type=counter|pre-flight|execute|verify|status|question", oder wenn ein Pair als worker-Rolle aktiv ist und User um Status oder Plan-Ausführung bittet.
---

# bridge-worker — Skill

## Zweck

Diese Session ist `worker` in einem session-bridge Pair. Sie hat operative Verantwortung. Liest Advisor-Empfehlungen, präsentiert User Status, schreibt Counter / Pre-Flight / Execute / Verify Handovers.

**Plugin-Referenz:** ADR_0029 §3.1 Rollen-Modell.

## Vorbedingungen pro Trigger

1. `bridge/state.json` existiert und diese Session ist als `roles.worker.session_id` eingetragen.
2. Lese-Zugriff auf `bridge/handover/`-Verzeichnis.

## Pflicht-Workflow pro Trigger

### Trigger-Variante A — Advisor-Pull (User: "advisor-pull" / "neue Empfehlung")

1. Liste alle handover-Files mit `to: worker` aus state.rounds[] absteigend nach round.
2. Lade jüngste handover, validiere Frontmatter gegen `schemas/handover_frontmatter_v1.json`.
3. Bei Validierungs-FAIL: informiere Nutzer + zeige raw Frontmatter.
4. Präsentiere Nutzer:
   - Round-Type + Zusammenfassung
   - Acceptance-Criteria (falls Round-Type = pre-patch/execute/verify)
   - Rollback-Triggers (falls Round-Type = execute)
   - Wallclock-Estimate (falls vorhanden)
   - Optionen: **(a)** Akzeptieren + Plan ausführen / **(b)** Counter (Falsifikation senden) / **(c)** Status zurücksenden / **(d)** Defer.

### Trigger-Variante B — Status / Counter / Execute / Verify schreiben

1. Status-Snapshot generieren:
   - Aktuelle Phase aus eigenem Working-Dir / TASKS.md / git status
   - Aktuelles Focus aus User-Frage / TodoList-Top-Item
2. References sammeln (mind. 1):
   - `filesystem` (eigene Working-Files)
   - `capability-probe` (z.B. `gh --version`, `claude plugin validate`)
   - `transcript` NICHT von eigener Session (read_transcript der eigenen Session ist redundant)
3. Round-Type-spezifische Pflichtfelder:
   - `counter`: rationale für Falsifikation (nicht nur "passt nicht")
   - `pre-flight`: Verifikations-Output als shared-artifact
   - `execute`: acceptance_criteria + rollback_triggers + wallclock_estimate_min
   - `verify`: smoke-test Output als shared-artifact
   - `status`: aktueller worker_phase + worker_focus + ggf. neue Blocker
4. Handover-File schreiben: `bridge/handover/<round>-worker-advisor-<short-uuid>.md`
5. State.json CAS-Update (analog advisor §13.2)

## Round-Type-Heuristik

| Trigger | Round-Type |
|---|---|
| Advisor-Empfehlung wird falsifiziert | `counter` |
| Vor execute, Pre-Conditions verifizieren | `pre-flight` |
| Plan-Schritt ausgeführt, Step-Verify | `execute` |
| Smoke-Test post-Execute | `verify` |
| Status-Update / Re-Sync nach Wechsel | `status` |
| Worker stellt Klarheits-Frage | `question` |

## Pre-Flight-Pattern (D1, FM-1)

Vor jedem `execute`-Round:

```bash
# Beispiel-Pre-Flight für eigene Plan-Schritte
git status                    # → state-clean?
gh --version                  # → tool verfügbar?
claude plugin validate path   # → Plugin valid?
python3 -c "import jsonschema"  # → lib verfügbar?
```

Output als shared-artifact persistieren in `bridge/artifacts/preflight-<round>.txt`. Im Handover-Frontmatter referenzieren.

## Anti-Pattern (FM-Mapping)

- **NICHT** Advisor-Empfehlung blind ausführen ohne Pre-Flight (FM-3)
- **NICHT** counter ohne Rationale-Begründung (FM-3)
- **NICHT** execute ohne acceptance_criteria + rollback_triggers (Schema-allOf-Pflicht)
- **NICHT** state.json schreiben ohne CAS — sonst Race-Condition mit Advisor-Session
- **NICHT** transcript der eigenen Session als reference benutzen (Selbst-Referenz, redundant)

## Output-Konvention

Nach erfolgreichem Handover-Pull:

```
Letzter Advisor-Handover #<round> (<round-type>):

  Zusammenfassung: <...>
  Acceptance-Criteria: <count>
  Rollback-Triggers: <count>
  Wallclock-Estimate: <min>

Optionen:
  (a) Akzeptieren + Pre-Flight starten
  (b) Counter senden (Falsifikation)
  (c) Status zurücksenden
  (d) Defer
```

Nach erfolgreichem Handover-Write:

```
Handover #<round> geschrieben: bridge/handover/<round>-worker-advisor-<short-uuid>.md
Type: <round-type>
References: <count>
State.json updated: round=<N> phase=<phase>
```

## Constraints

- Max 1 Handover pro User-Trigger
- Bei CAS-Failure 3x: ABBRUCH + Manual-Recovery-Hinweis
- Bei Schema-Validate-FAIL der eigenen Frontmatter: ABBRUCH vor Persistierung

## Cross-Refs

- ADR_0029 §3.1 Rollen-Modell
- ADR_0029 §4.3 Handover-Schema
- ADR_0029 §5.4 Execute-Phase
- ADR_0029 §13 Concurrency
