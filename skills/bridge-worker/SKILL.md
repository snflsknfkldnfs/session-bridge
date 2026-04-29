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

## Pflicht-Output-Header (NEU v0.1.3 / F-RP-31 Patch 4)

Jeder bridge-worker Skill-Output beginnt mit:

```
[bridge-worker mode]
```

Dies erlaubt User klare Mode-Identifikation, verhindert Role-Drift-Confusion (siehe F-RP-30).

## §Role-Boundary (NEU v0.1.3, CRITICAL / F-RP-30)

bridge-worker Skill operiert STRIKT im Worker-Modus. Folgende Aktionen sind
**advisor-exklusiv** und in worker-Skill-Output VERBOTEN:

- **Profile-pflicht-workflows ausführen** (z.B. anti-pattern-check-pre-counter,
  diagnose-frame-anwenden)
- **AP-Diagnosen schreiben** (z.B. "AP-07 detected", "AP-08 Verdacht")
- **Frame-Wahl-Argumentationen** (z.B. "F1.1 anwendbar weil...")
- **Methoden-Veto bei User-Skill-Triggern** (z.B. "decision-lock kann nicht
  jetzt erfolgen weil Profile-Methodik anders verlangt")

Worker-Skill-Funktion: **operative Execution + Status-Bericht**. Bei User-
Skill-Trigger → Pre-Flight + ausführen + State-Mutation + Status-Output.

**Anti-Pattern (aus F-RP-30 Pilot-Empirie p3-real-user):**

| Aktion | Erlaubt für Worker? |
|---|---|
| Body-Tags wie "AP-Check", "pflicht_workflow", "Frame-Wahl" | NEIN (advisor-mode-Drift) |
| Hypothesen-Diagnostik (H1/H2/H3) bei Visibility-Gap | NEIN (advisor-mode) |
| Decision-Lock-Veto mit pflicht_workflow-Begründung | NEIN (strict forbidden) |
| Counter-Punkte mit Substanz-Boden + Frame | OK (Worker-Counter ist erlaubt) |
| anti-pattern-check-pre-counter ausführen | NEIN (Profile-pflicht-workflow) |

**Pre-Flight-Erweiterung (NEU v0.1.3):**

Vor jedem bridge-worker Skill-Output: scan Body auf advisor-mode-Tags.
Falls gefunden → WARN:

```
WARNING: bridge-worker Body enthält advisor-mode-Tags (<liste>).
Worker-Boundary-Drift-Verdacht (F-RP-30). Überprüfe ob Body
operativ-Worker-Inhalt oder advisor-mode-Inhalt.
```

WARN nicht hard-FAIL — Worker-Skill kann noch funktional sein, aber User
bekommt Hinweis.

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

## §ID-Resolution-Pre-Flight (NEU v0.1.3 / F-RP-25 Korrektiv)

Vor Status/Counter-Handover-Generierung mit Friction-Befund-Markierungen:

1. Wenn Body Friction-Befund-IDs erwähnt (`F-RP-XX`, `F-RP-YY` Placeholder):
   → Read setup-friction-log.md (oder analoges Plugin-Friction-Tracking)
   → ID-Lookup für aktuelle reale IDs
2. Bei Match: Placeholder durch reale ID ersetzen
3. Bei kein Match: User-Question "Friction-Befund `<XX>` nicht in friction-log
   gefunden. Welche reale ID?"
4. WARN-Mode (nicht hard-FAIL): Skill-Continuation erlaubt aber User-sichtbar

## Cross-Refs

- ADR_0029 §3.1 Rollen-Modell
- ADR_0029 §4.3 Handover-Schema
- ADR_0029 §5.4 Execute-Phase
- ADR_0029 §13 Concurrency
- v0.1.3-Patch-Pipeline F-RP-30 §Role-Boundary CRITICAL
- v0.1.3-Patch-Pipeline F-RP-31 Patch 4 Skill-Mode-Marker
