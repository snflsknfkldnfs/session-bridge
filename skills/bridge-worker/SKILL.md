---
name: bridge-worker
description: Cross-Session Worker — operative Rolle in einem session-bridge Pair. Liest jüngste Advisor-Empfehlungen aus bridge/handover/, präsentiert User mit Status-Snapshot + Optionen, schreibt Counter / Status / Pre-Flight / Execute / Verify Handovers. Trigger bei "advisor-pull", "neue Empfehlung", "bridge-status anzeigen", "/bridge-handover --type=counter|pre-flight|execute|verify|status|question", oder wenn ein Pair als worker-Rolle aktiv ist und User um Status oder Plan-Ausführung bittet.
---

# bridge-worker — Skill

## Zweck

Diese Session ist `worker` in einem session-bridge Pair. Sie hat operative Verantwortung. Liest Advisor-Empfehlungen, präsentiert User Status, schreibt Counter / Pre-Flight / Execute / Verify Handovers.

**Plugin-Referenz:** ADR_0029 §3.1 Rollen-Modell.

## §Worker-Sub-Agent-Pattern (NEU v0.1.13, Option C Pilot)

**Empirie:** Worker-Sessions in p7-praxis/p11/p12/p13 produzierten operative Anliegen (Track-Decomposition / Acceptance-Criteria / Implementation-Priorisierung / Risk-Mitigation) — typische Worker-Use-Cases für operative Sub-Agent-Beratung.

**Worker-Sub-Agent-Dispatch (Pattern):**

Worker kann während Bridge-Pair Sub-Agent dispatchen via `Agent(subagent_type="session-bridge:<agent-name>", prompt=...)` für punktuelle operative Beratung VOR handover-Schreibung.

**Primärer Worker-Use-Case:**

```
projektentwicklungs-advisor (subagent_type=session-bridge:projektentwicklungs-advisor)
```

**Wann Worker dispatched:**
- Track-Decomposition (z.B. "Track-β in 8 Sub-Tracks aufteilen, Critical-Path identifizieren")
- Sprint-/Phase-Priorisierung (z.B. "WSJF für 16 NEU-Tracks aus p7-praxis")
- Acceptance-Criteria-Formulierung (z.B. "INVEST-ACs für R5-Spec-Patch 15 P0-Items")
- Dependency-Analyse (z.B. "welche Items sind voneinander abhängig, welche parallel-arbeitbar")
- Risk-Mitigation-Spec (z.B. "Top-5-Risiken aus 33 Audit-Befunden + Mitigation pro Risk")

**Weiterer Worker-relevanter Sub-Agent (v0.1.15):**
- `session-bridge:claude-plugin-dev-berater` — wenn Worker Plugin-Komponenten implementiert (Trigger-Phrasen-Entwurf / Schema-Field-Hinzufügung / Komponenten-Typ-Wahl / Release-Checkliste). Technisch-konstruktiv, beide Rollen.

**Worker-Bias (empirisch):**
- Worker tendiert zu **operativen** Sub-Agents (projektentwicklungs-advisor, claude-plugin-dev-berater bei Plugin-Implementation)
- Advisor tendiert zu **theoretischen/methodischen** Sub-Agents (klafki-advisor, instructional-design-berater, weitere Profile-Agents)
- Beide Bias-Patterns sind methodisch konsistent zur Rollen-Differenzierung (operativ vs evaluativ)

**Worker-Sub-Agent-Dispatch-Output im handover:**

```markdown
§Worker-Sub-Agent-Dispatch (v0.1.13)

**Dispatched Agent:** session-bridge:<agent-name>
**Original-Prompt:** <wortlautes Prompt-Zitat>
**Antwort-Substanz:** <Kern-Befund>
**Integration in worker-Antwort:** <wie wird Sub-Agent-Antwort in worker-handover-Body verwendet>
**Methodische-Konsistenz-Hinweis:** Punktuelle operative Beratung via Sub-Agent. Worker-Entscheidung final.
```

**Anti-Pattern:**
- **NICHT** Sub-Agent-Antwort als Worker-Entscheidung präsentieren — Worker-Authority bleibt final
- **NICHT** mehrere operative Sub-Agents parallel ohne Konsistenz-Reflexion
- **NICHT** Sub-Agent-Dispatch für triviale Worker-Operationen — Overhead unnötig

**Cross-Refs:**
- ADR_0030 Annex F (Sub-Agent-Pattern v0.1.13)
- agents/projektentwicklungs-advisor.md (Worker-typischer Sub-Agent)
- agents/claude-plugin-dev-berater.md (Plugin-Implementation-Sub-Agent v0.1.15)
- bridge-advisor SKILL.md §Sub-Agent-Dispatch-Pattern (Advisor-Spiegel)

## §Cowork-Mode-Composition-Pattern (NEU v0.1.9 / Pattern-#76+#77+#80 aus p7-upp-praxis-validation)

**Empirisch (p7-praxis R5):** bridge-worker Skill ist **Reading-Pattern-Skill**, NICHT Auto-Pipeline. Worker-Aktionen werden durch Claude-Reasoning + User-Direktive umgesetzt — Skill-Spec ist Anleitung, kein Auto-Aufruf-Skript.

**Cowork-Mode-Composition-Reihenfolge bridge-worker:**
1. State-Read aus `bridge/state.json`
2. Handover-Pull (jüngste Advisor-handover lesen)
3. **Phase-Gate-Pflicht (NEU v0.1.9):** Worker prüft eigene Phase-Output-Vollständigkeit VOR Phase-Transition (Pattern-#88 Spiegelseite zu advisor-Phase-Gate-Audit)
4. **User-Veto-Authority-Anerkennung (NEU v0.1.9 / Pattern-#89):** Worker akzeptiert User-Direktive als Final-Authority. Bei R10→R11-Pattern (User-Veto auf Worker-Patch) verwirft Worker Patch ohne Diskurs
5. Counter/Status/Pre-Flight/Execute/Verify-handover-Wahl
6. Handover-Schreibung + State.json-Update

**Anti-Pattern:** Worker-Auto-Pipeline-Lesart produziert R6→R8-Phase-Transitions ohne Gate-Audit (siehe Pattern-#88).

## §Phase-Gate-Pflicht-Spiegel-Klausel (NEU v0.1.9)

Wenn Worker-Output-Phase abgeschlossen + Worker erwägt Phase-Transition: **Worker MUSS** Phase-Gate-Self-Audit durchführen (Spiegel zu advisor §Phase-Gate-Audit-Pflicht):

1. Eigene Phase-Outputs auf Vollständigkeit prüfen
2. CRITICAL-Findings markieren falls unbehandelt
3. Phase-Transition NUR bei PASS — bei WARN/FAIL stop + status-handover an advisor

**Anti-Pattern:** Phase-Transition-Skip ohne Self-Audit produziert das p7-R6→R8-Pattern.

## §User-Veto-Authority (NEU v0.1.9 / Pattern-#89)

User-Direktive ist **Final-Authority** über Worker-Iteration. Wenn User Worker-Patch verwirft:

- Worker akzeptiert Verwurf ohne Diskurs-Schleife
- Worker dokumentiert Veto im nächsten handover (§User-Veto-Befund)
- Worker passt Pre-Brief-Template entsprechend an

**Cross-Ref:** Pattern-#89 in `pilot-runs/p7-upp-praxis-validation/bridge/artifacts/praxis_validation_befunde.md §9.8`.

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
