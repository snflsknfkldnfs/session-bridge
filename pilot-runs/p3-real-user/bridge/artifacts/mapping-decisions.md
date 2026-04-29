# Mapping-Decisions-Log — p3-real-user Bridge-Pair 8cbeaad0

**Pair-ID:** 8cbeaad0-e67a-4184-889b-76a70c21d617
**Methodischer Boden:** `bridge/artifacts/mapping-method-annex.md` (v0.1.1)
**Decision-Log Schema-Version:** v0.1.5
**Mapping-Phase-Start:** Round 12 (decision-locked Round 11)
**Konvention:** Append-only Decisions-Liste D-001…D-NNN. Pro Decision: actionable Worker-Schritte + Plugin-Dev-Schritte (separate Tracks).

---

## Format pro Decision

```
### D-NNN — <Befund-ID> → <Mapping-Kategorie>

**Round-Decided:** R<n> (<advisor|worker>-initiator)
**Konvergenz-Status:** <pending | accepted | counter-pending | locked>
**Frame:** <F1.1 | F1.2 | F4.1 | F4.2 | F5.1> aus Annex §2.1
**Real-friction-log-Match:** <F-RP-NN | NEW | NONE>
**Severity:** <CRITICAL | HIGH | MEDIUM | LOW | BEOBACHTUNG>

#### Befund-Beschreibung (Kurz)
<2-3 Sätze>

#### Decision
<Kategorie + Sub-Spec>

#### Worker-Action (im Bridge-Pair)
<konkrete Schritte für Worker-Session>

#### Plugin-Dev-Action (out-of-pair, in plugin-dev workflow)
<konkrete Schritte für Plugin-Dev-Session, getrennter Track per ADR_0021>

#### Migration (per Annex §5)
<status-Übergang in friction-log + Pflicht-Felder>

#### Pflicht-Felder (per Annex §3 Mapping-Kategorie)
<spec'd structured data>

#### Cross-References
<handover-pointer + andere Decisions + Annex-§-pointer>
```

---

## Decisions

### D-001 — F-RP-29 (Bridge-Pair "F-RP-YY") → DISSENS-DOCUMENTED §3.4.2

**Round-Decided:** R12 (advisor-initiator, retrospektiv hier formalisiert post Round 15 Konvergenz)
**Konvergenz-Status:** locked (R15 Teil F-D 5/5 Akzeptanz inkl. Sub-Typ §3.4.2)
**Frame:** F1.2 primär (Skill-Spec formal / User-Translation informell im Wechselspiel) + F5.1 sekundär (Schauseite Plan-Text vs Inhalt Bridge-Write)
**Real-friction-log-Match:** F-RP-29 CRITICAL (existiert seit 2026-04-26)
**Severity:** CRITICAL

#### Befund-Beschreibung

Plan-vs-Execution-Layer-Konfusion: Advisor schreibt Plan-Text in Chat ohne Skill-Aufruf, User interpretiert als Bridge-Write, Worker erwartet Bridge-Artefakt. Reproduziert sich 3× live im Pair (Round 6→7, 7→8, 10→11).

#### Decision

DISSENS-DOCUMENTED, Sub-Typ §3.4.2 Skopus-Differenz (X ⊆ Y). Worker-Position ist echte Teilmenge der Advisor-Position; nicht kompetitiv, sondern Schicht-Differenz.

#### Worker-Action (im Bridge-Pair)

1. friction-log-Eintrag F-RP-29 status updaten: `OPEN` → `DISSENS-DOCUMENTED`
2. Pflicht-Sub-Pointer im friction-log eintragen:
   - `worker_position_pointer: bridge/handover/8-worker-advisor-f5653416.md#teil-d`
   - `advisor_position_pointer: bridge/handover/9-advisor-worker-ced96be3.md#teil-c`
3. Reconcile-Status `TBD` markieren mit Beschreibung "Skill-Spec-Patch + Multi-Layer-Konvention parallel; F-RP-29 RESOLVED bei Merge beider Items"

#### Plugin-Dev-Action (out-of-pair)

**Worker-Position-Patch (Schicht 1, Skill-Spec):**
- bridge-handover SKILL.md ergänzen um §Re-Sync-Sub-Typen (plan-layer / execution-layer / hybrid)
- Pre-Flight für execution-layer-resync: ≥1 reference muss type=evidence sein mit advisor-side-Pointer
- Estimated-Aufwand: 1.5h Self-Edit + Self-Test-Erweiterung

**Advisor-Position-Patch (Schichten 2+3, User-Translation + Advisor-Chat):**
- bridge-advisor SKILL.md §Plan-vs-Execution-Konvention: Plan-Text > 5 Sätze ohne Skill-Aufruf = AP-Plan-vs-Execution-Drift
- bridge-handover SKILL Output-Marker BRIDGE-WRITE-COMPLETED-Block (Pflicht)
- Doku-Sektion User-Translation-Konvention für Plugin-User-Onboarding
- Estimated-Aufwand: 2.5h Self-Edit + Doku-Update

**Beide Items im v0.1.3-Patch-Backlog markieren.** F-RP-29 wird `RESOLVED-IN-V0.1.3` bei Merge beider Patches.

#### Migration

```yaml
friction_log_status: OPEN → DISSENS-DOCUMENTED
worker_position_pointer: bridge/handover/8-worker-advisor-f5653416.md#teil-d
advisor_position_pointer: bridge/handover/9-advisor-worker-ced96be3.md#teil-c
reconcile_pointer: TBD
reconcile_condition: "beide Patch-Items merged in v0.1.3"
```

#### Pflicht-Felder

```yaml
befund_id: F-RP-29
mapping_category: DISSENS-DOCUMENTED
sub_type: §3.4.2 Skopus-Differenz (X ⊆ Y)
empirical_validation:
  - "Round 6→7: Plan-Text ohne Skill-Aufruf, Worker-Visibility-Probe"
  - "Round 7→8: zweiter Plan-Loop, Worker-Doppel-Re-Sync"
  - "Round 10→11: Worker-Unilateral-Decision-Lock nach User-Inferenz"
```

#### Cross-References

- Annex §9 (Live-Test-Case) — diese Decision IST der Test-Case
- Annex §3.4 (Dissens-Documented-Spec)
- handover R12 Teil D (Initial-Mapping)
- handover R15 Teil F-D (Konvergenz-Akzeptanz)
- friction-log F-RP-29 (Quell-Befund)

---

### D-002 — F-RP-XX#worker-focus-validation + M-6-Erweiterung → PATCH

**Round-Decided:** R16 (advisor-initiator, dieser Eintrag)
**Konvergenz-Status:** pending (Worker-Antwort R17 erwartet)
**Frame:** F1.1 (Mitgliedschaftsbedingungen-Säule der Plugin-Drei-Säulen-Logik; Skill-Pre-Flights aktuell unzureichend für required-Args)
**Real-friction-log-Match:** NONE (kein direkter Match — verwandt zu F-RP-26 BEOBACHTUNG worker.phase stuck, materiell anders). Bridge-Pair-Output: neuer friction-log-Eintrag empfohlen.
**Severity:** HIGH

#### Befund-Beschreibung

bridge-attach SKILL hat keine Pre-Flight-Validation für required-Args wie `--worker-focus`. Bei missing Args wird via Elicitation-Form gefragt. Funktional, aber: Korrektheit hängt vom Modell-Verhalten ab, nicht von Skill-Robustheit. Bei terse-User-Pref (Absolute Mode) verschiebt sich Robustheits-Garantie auf Modell-Quality.

M-6-Erweiterung: Plugin-Marketplace-Adoption-Argument (Cross-Reference F-RP-24) — Plugin darf nicht von Modell-Quality abhängen, sonst UX-Adoption-Blocker.

#### Decision

PATCH. Skill-Pre-Flight hard-enforce für required-Args. Trade-off Robustheit > Flexibility. Elicitation-Fallback bleibt operativ-erlaubt aber sekundär; primärer Pfad ist Pre-Flight-FAIL bei missing required.

#### Worker-Action (im Bridge-Pair)

1. friction-log-Neueintrag erstellen: F-RP-32 HIGH (oder nächste freie ID): "Skill-Pre-Flight required-Args nicht hard-enforced; Modell-Abhängigkeit für Robustheit"
2. Inhalt: Befund-Beschreibung wie oben + M-6-Erweiterung + Cross-Reference F-RP-24 + Patch-Vorschlag (siehe Plugin-Dev-Action)
3. Status: `OPEN` mit `mapping_decision: D-002 (Bridge-Pair p3-real-user, R16)`
4. Im Mapping-Decisions-Log diese D-002-Entry als pointer eintragen

#### Plugin-Dev-Action (out-of-pair)

**Patch-Spec für v0.1.3-Backlog:**

1. **bridge-attach SKILL Pre-Flight (NEU Punkt 5):**
   ```
   5. Pflicht-Args-Validation:
      - --worker-focus muss gesetzt sein
      - Bei missing → ABBRUCH mit User-Question (NICHT Elicitation-Form-Fallback)
      - Diagnose-Output: "Pre-Flight FAIL Punkt 5 — required-Arg --worker-focus missing"
   ```

2. **bridge-handover SKILL Pre-Flight (NEU Punkt 5):**
   ```
   5. Type-spezifische required-Args-Validation:
      - type=execute: --acceptance + --rollback + --wallclock-min Pflicht
      - type=decision-lock: --decided-by Pflicht
      - type=pre-patch: --acceptance + --wallclock-min Pflicht
      - Bei missing → ABBRUCH mit Type-spezifischer Diagnose
   ```

3. **bridge-init SKILL** existing Pre-Flight 5 (Profile-Validation) als Vorbild — gleiche Hard-FAIL-Logik

4. **Doku-Update bridge-handover.md + bridge-attach.md:** "Required-Args werden hard-enforced via Pre-Flight, NICHT via Elicitation-Fallback. Elicitation ist sekundär für optional-Args oder strukturierte Eingabe."

5. **Self-Test-Erweiterung (smoke_self_test.py):** T16-T18 für required-Args-Pre-Flight (negative cases: missing arg → FAIL erwartet)

6. **Estimated-Aufwand:** 2h Self-Edit (3 Skill-Edits + 3 Self-Tests + Doku-Updates)

**Migration friction-log-Eintrag:** Status `OPEN` → `RESOLVED-IN-V0.1.3` bei Merge.

#### Migration

```yaml
friction_log_neuer_eintrag:
  id: F-RP-32 (Vorschlag, finale ID bei friction-log-Schreiben)
  severity: HIGH
  status: OPEN
  mapping_decision: D-002
  resolved_in_version: V0.1.3 (geplant)
```

#### Pflicht-Felder

```yaml
befund_id: F-RP-XX#worker-focus-validation (Bridge-Pair-Bezeichnung)
real_id: NEW (friction-log-Eintrag in Worker-Action #1)
mapping_category: PATCH
patch_target_files:
  - skills/bridge-attach/SKILL.md
  - skills/bridge-handover/SKILL.md
  - tests/smoke_self_test.py
patch_acceptance_criteria:
  - bridge-attach Pre-Flight 5 enforced + Self-Test PASS
  - bridge-handover Pre-Flight 5 type-spezifisch enforced + Self-Test PASS
  - Doku-Update verifiziert
substanz_boden:
  - "F-RP-24 Plugin-Marketplace-Adoption-Argument"
  - "M-6 Modell-Abhängigkeits-Argument"
  - "Annex §6.3 AP-09-Schutz: hard-enforce ist nicht Klarheits-Imperativ wenn substanz-begründet"
```

#### Cross-References

- Annex §3.1 (Patch-Definitions-Kriterien)
- Annex §2.1 F1.1 (Frame-Anwendbarkeit Mitgliedschaftsbedingungen-Säule)
- Annex §5 (SoT-Migrations-Pfad Patch-Kategorie)
- friction-log F-RP-24 (Marketplace-Adoption-Cross-Reference)
- friction-log F-RP-26 BEOBACHTUNG (verwandt, aber materiell anders)
- handover R13 Teil M-6 (Worker-Beobachtung Original)
- handover R14 Teil A M-6 (Advisor-Lesart-Wahl)
- handover R15 Teil A M-6 (Worker-Konvergenz)

---

### D-002 R17-Klarstellung-Annex (R17-Update v0.1.1)

**Anlass:** Worker-Question zu R16-Anweisungs-Unklarheit (Bündelung vs Trennung als Worker-Wahl übergeben war Konsens-Druck-Vermeidung übertrieben → Anweisungs-Vakuum). Live-Reproduktion F-RP-29 zum vierten Mal. Klarstellung mit klarer Direktive:

#### Workflow-Direktive für R17 (verbindlich, kein Pluralismus)

**Option A — Bündelung. Voto eindeutig.** R17 = Konvergenz-Antwort + friction-log-Updates D-001 + D-002 in einem Worker-Move.

Begründung: friction-log gehört zum Bridge-Pair-Lifecycle (Pilot-Empirie auf shared-path). ADR_0021 strict-separation gilt für Plugin-Code-Edits (`/Users/paulad/session-bridge/skills/...`), NICHT für `pilot-runs/p3-real-user/setup-friction-log.md`. Trennung in zwei Rounds wäre redundant.

**Optionen B (Trennung), D (Counter Estimated), E (Counter eigenes Wording):** verworfen.

**Option C (F-RP-26 Match-Prüfung):** geklärt unten.

#### F-RP-26 vs F-RP-32 Match-Prüfung (Klärung Option C)

| Befund | Inhalt | Materielle Identität |
|---|---|---|
| F-RP-26 BEOBACHTUNG | `state.roles.worker.phase` bleibt `kickoff` während Pair durch scope-lock + iterate progressiert | Worker-State-Tracking-Hygiene |
| F-RP-32 (D-002) | Skill-Pre-Flight required-Args nicht hard-enforced (bridge-attach `--worker-focus`, bridge-handover type-spezifische required) | Skill-Robustheit-Pre-Flight |

**Verdikt:** materiell verschieden. Verwandt nur in der Meta-Kategorie "Skill-Spec-Laxity", nicht im Befund-Inhalt. **F-RP-32 NEW ist korrekt, kein Match-Merge mit F-RP-26.**

Worker-Action für friction-log-Eintrag F-RP-32: Cross-Reference "verwandt zu F-RP-26 BEOBACHTUNG (gemeinsame Meta-Kategorie Skill-Spec-Tracking-Laxity), aber materiell verschieden".

#### Konvergenz-Erwartung pro D-002-Pflicht-Feld

Worker antwortet pro Feld mit "Akzeptanz" oder "Counter zu <Feld>". Substantieller Counter-Boden ist nicht ersichtlich (alle Felder sind Worker-R15-akzeptiert oder triviale Konsequenzen davon). Default-Erwartung: 6/6 Akzeptanz.

#### Methodische Selbst-Diagnose (advisor-side)

R16-Body-Sektion "Worker-Action-Anweisung" enthielt am Ende: *"können in R17 gebündelt werden ODER getrennt — Worker-Wahl"*. Das war Konsens-Druck-Vermeidung übertrieben → Anweisungs-Vakuum bei Workflow-Routine-Frage. Methoden-Pluralismus gehört in Substanz-Decisions (Frame, Mapping-Kategorie), nicht in Workflow-Routine.

**Korrektur-Konvention für Folge-Rounds:** Bei Workflow-Routine-Fragen klare Direktive statt Worker-Wahl-Übergabe.

---

### D-003 — M-3 (`pre-allocated`-Pattern für decision-lock-forward-pointer) → AFFORDANCE

**Round-Decided:** R19 (advisor-initiator, dieser Eintrag)
**Konvergenz-Status:** pending (Worker-Antwort R20 erwartet)
**Frame:** F1.2 primär (formal-spec erlaubt / informell-typisch ist anders, beide tragen) + F4.2 sekundär (decision-lock ohne erzwungene Annex-Vorbedingungs-Konsens)
**Real-friction-log-Match:** NONE — Bridge-Pair-Origin in Worker-R11 decision-lock erfunden, in M-3 (Worker-R13) als Plugin-Spec-Implikation ausformuliert
**Severity:** BEOBACHTUNG (kein Lifecycle-Bruch, gut erfundenes operatives Pattern)

#### Befund-Beschreibung

Worker hat in R11 unilateral decision-lock geschrieben mit Pointer auf Annex-Datei, die noch nicht existierte. State-Schema `shared_artifacts[].status="pre-allocated"` als Forward-Pointer-Marker erfunden. Pattern entkoppelt decision-lock (formal) von Annex-Materialisierung (substantiell), verhindert Block-Schleife bei async-Artefakt-Schreiben.

#### Decision

AFFORDANCE. `pre-allocated`-Pattern als doku'ble Konvention in bridge-handover SKILL §forward-pointer-rationale. Pre-Flight-Pflicht für rationale-File-Existenz wäre AP-09-Reflex (Klarheits-Imperativ ohne Substanz-Bedarf) — verworfen.

#### Worker-Action (im Bridge-Pair)

1. friction-log-Neueintrag erstellen: F-RP-33 BEOBACHTUNG (oder nächste freie ID): "decision-lock forward-pointer via shared_artifacts.status=pre-allocated als operative Affordance"
2. Status direkt auf `Affordance-Documented` (kein OPEN-Zwischenstadium, weil Pattern bereits funktional verifiziert in R11/R12)
3. Pointer auf SoT: `bridge-handover SKILL.md §forward-pointer-rationale` (nach Plugin-Patch in v0.1.3 verfügbar)
4. mapping_decision-Pointer: `bridge/artifacts/mapping-decisions.md#d-003`

#### Plugin-Dev-Action (out-of-pair)

**Patch-Spec für v0.1.3-Backlog:**

1. **bridge-handover SKILL.md neue Sektion §forward-pointer-rationale:**
   ```
   §forward-pointer-rationale (Affordance-Documented):
   
   decision-lock-Round darf rationale-File pointer enthalten der zum
   Schreib-Zeitpunkt noch nicht existiert. Pflicht-Markierung:
   shared_artifacts[].status = "pre-allocated", round_allocated = N
   (= decision-lock-Round). Folge-Round (typischerweise N+1) materialisiert
   File und setzt status = "active", round_active = N+1.
   
   Rationale: entkoppelt formale decision-lock von substantieller
   Artefakt-Materialisierung, verhindert Block-Schleife bei async-Schreiben.
   
   Anti-Pattern: pre-allocated-Status ohne Materialisierungs-Plan in
   Folge-Rounds = Forward-Pointer-Drift, nach 3 Rounds ohne active-Status
   FAIL-Markierung in bridge-status.
   ```

2. **bridge-status SKILL.md Output-Erweiterung:** zeigt `pre-allocated` shared_artifacts mit Warnung wenn Pre-Allocation > 3 Rounds alt.

3. **Doku-Update bridge-handover.md + decision-lock-Sub-Sektion:** Beispiel mit pre-allocated-Pattern aus p3-real-user-Pilot.

4. **Estimated-Aufwand:** ~30min Self-Edit (Skill-Doku-Sektion + bridge-status-Output-Patch + Doku-Update)

#### Migration

```yaml
friction_log_neuer_eintrag:
  id: F-RP-33 (Vorschlag, finale ID bei friction-log-Schreiben)
  severity: BEOBACHTUNG
  status: Affordance-Documented (direkt, kein OPEN)
  mapping_decision: D-003
  sot_pointer: bridge-handover SKILL.md §forward-pointer-rationale (nach v0.1.3-Patch)
  empirical_origin: bridge-pair p3-real-user R11 worker-decision-lock
```

#### Pflicht-Felder

```yaml
befund_id: M-3 (Bridge-Pair-Bezeichnung aus Worker-R13)
real_id: NEW (friction-log-Neueintrag F-RP-33 in Worker-Action #1)
mapping_category: AFFORDANCE
sot_locus: skill-doku-sektion (mittlere Hürde, per Annex §5 SoT-Loci-Tabelle)
sot_target: bridge-handover SKILL.md §forward-pointer-rationale
substanz_boden:
  - "Worker-R11 operativ-erfundene Konvention war funktional"
  - "Annex §3.2 Affordance-Definitions-Kriterien erfüllt: beide Pfade funktional, Use-Pattern hat Affordance-Wert"
  - "Annex §3.4.0 Inflations-Schutz: keine zwei substantiellen Positionen, keine Skopus-Differenz → AFFORDANCE statt Dissens-Documented"
inflation_protection_check:
  - "Default-Kategorie für operative Pattern mit Doku-Konsequenz = AFFORDANCE ✓"
  - "Keine Worker- vs Advisor-Position-Differenz vorhanden ✓"
```

#### Cross-References

- Annex §3.2 (Affordance-Definitions-Kriterien)
- Annex §3.4.0 (Inflations-Schutz, hier angewandt)
- Annex §5 SoT-Loci-Tabelle (Skill-Doku-Sektion mittlere Hürde)
- handover R11 Teil shared_artifacts pre-allocated (Origin)
- handover R13 Teil M-3 (Worker-Beobachtung Original)
- handover R14 Teil A M-3 (advisor-Lesart-Wahl AFFORDANCE)
- handover R15 Teil A M-3 (Worker-Konvergenz)

---

### D-004 — F-RP-23 (Sentinel-Bypass via --worker-session-id) → AFFORDANCE (advisor-Position)

**Round-Decided:** R21 (advisor-initiator, dieser Eintrag)
**Konvergenz-Status:** pending (Worker-Antwort R22 erwartet — möglicherweise Counter zu PATCH-Position)
**Frame:** F1.2 primär (Spec-formal verlangt Sentinel / informell-empirisch funktioniert Argument-Konsumption — Wechselspiel) + F4.1 sekundär (zwei Pfade nebeneinander = produktiv, nicht zu lösen)
**Real-friction-log-Match:** F-RP-23 CRITICAL (existiert seit 2026-04-26 mit Patch-Empfehlung Option v1)
**Severity:** CRITICAL (per friction-log; Bridge-Pair-Empirie zeigt aber: kein Lifecycle-Block in Praxis)

#### Befund-Beschreibung

friction-log F-RP-23 CRITICAL: bridge-init schreibt mit `--worker-session-id` direkt `state.roles.worker.session_id = <id>` (kein Sentinel). bridge-attach Pre-Flight 4 erwartet Sentinel `pending-attach`, findet direkten Pin → FAIL. Vorhersage: blockiert Lifecycle-Progression bei Standard-Use-Path "Advisor kennt Worker-Session-ID".

friction-log empfiehlt Option v1 (PATCH zur Sentinel-Invariante): bridge-init schreibt IMMER Sentinel; `--worker-session-id` wird nur für Worker-Notification-Block verwendet.

**Pilot-Empirie aus dieser Bridge-Pair widerspricht F-RP-23-Block-Vorhersage:**
- bridge-init R0 mit `--worker-session-id=local_e9ba7337` direkt übergeben → state.worker.session_id=local_e9ba7337 (kein Sentinel)
- bridge-attach in BP-WORKER-Session lief erfolgreich, Lifecycle R0→R20 sauber
- Pre-Flight 4 hat NICHT FAIL geworfen — entweder Plugin-Version-Path-Diff oder Pre-Flight 4 ist toleranter implementiert als Spec angibt

#### Decision (advisor-Position)

**AFFORDANCE.** Argument-Konsumption ist legitime Power-User-Affordance, in p3-real-user-Pilot empirisch funktional verifiziert. Pre-Flight 4 in bridge-attach lockern (Option v2 aus friction-log) statt Argument entfernen (Option v1). Sentinel-Pfad bleibt Default für Standard-Use; Argument-Pin als optionaler Power-User-Pfad mit explizitem `--worker-session-id`.

**Methodische Begründung:** F4.1-pflicht_workflow — Spannung produktiv führen, nicht auflösen. Sub-Pattern "brauchbare Illegalität" (Annex §2.1 F1.2): operativ funktional trotz formaler Abweichung. PATCH-Reflex (Option v1) hätte funktionierende Affordance entfernt.

#### Worker-Action (im Bridge-Pair)

**Wahrscheinlicher Counter-Punkt:** Worker könnte PATCH-Position vertreten (folgt friction-log-Empfehlung Option v1 wörtlich). Falls Counter:
- R22 = Worker-re-sync mit PATCH-Begründung (Sentinel-Invariante)
- R23 = advisor-re-sync mit DISSENS-DOCUMENTED §3.4.1 KOMPETITIV (Worker-PATCH ⊥ Advisor-AFFORDANCE)
- R24 = Worker-Konvergenz auf Dissens-Lock

Falls Akzeptanz advisor-AFFORDANCE-Position:
1. friction-log F-RP-23 status `OPEN` → `Affordance-Documented` mit:
   - sot_pointer: bridge-attach SKILL.md §sentinel-bypass-affordance (Plugin-Dev-Action, v0.1.3)
   - empirical_origin: bridge-pair p3-real-user R0-R20 sauberer Lifecycle mit Argument-Pin
   - mapping_decision: D-004
   - relation_to_friction_log_v1_recommendation: "v1 verworfen, v2-Variante akzeptiert (Pre-Flight 4 lockern statt Argument entfernen)"
2. Konvergenz-Antwort R22 als type=re-sync

#### Plugin-Dev-Action (out-of-pair)

**Patch-Spec für v0.1.3-Backlog (AFFORDANCE-Pfad, Option v2 aus friction-log):**

1. **bridge-attach SKILL.md Pre-Flight 4 Erweiterung:**
   ```
   4. session_id-Pre-Check (toleranter):
      - Akzeptiert: state.worker.session_id == "pending-attach" (Sentinel-Pfad, Standard)
      - ODER: state.worker.session_id == this_session_id MIT fehlenden Sub-Feldern
        (current_focus, phase) → auto-recover: ergänzt Felder, transition init → scope-lock
      - FAIL nur bei: session_id != Sentinel UND != this_session_id
        → Diagnose "session-id-mismatch: state hat <X>, this session ist <Y>"
   ```

2. **bridge-attach SKILL.md neue Sektion §sentinel-bypass-affordance:**
   ```
   §sentinel-bypass-affordance (Affordance-Documented):
   
   bridge-init darf --worker-session-id direkt eintragen statt Sentinel.
   Voraussetzung: advisor kennt Worker-Session-ID vorab (z.B. via session_info MCP).
   bridge-attach Pre-Flight 4 erkennt diesen Pfad und macht auto-recover statt FAIL.
   
   Standard-Use bleibt Sentinel-Pfad. Power-User-Pfad ist Argument-Konsumption.
   Beide Pfade sind funktional.
   
   Empirische Validierung: bridge-pair p3-real-user R0-R20 sauberer Lifecycle
   mit Argument-Pin (kein Sentinel).
   ```

3. **bridge-init SKILL.md `--worker-session-id`-Doku:**
   ```
   --worker-session-id (optional, Power-User-Affordance):
     Wenn übergeben: state.worker.session_id wird direkt gepinnt
     (kein Sentinel pending-attach).
     Sentinel-Pfad bleibt Default bei missing Argument.
     Beide Pfade kompatibel mit bridge-attach Pre-Flight 4 (siehe §sentinel-bypass-affordance).
   ```

4. **friction-log F-RP-23 Status-Markierung:**
   - Falls Mapping-Lock AFFORDANCE: Status `OPEN` → `Affordance-Documented`
   - Falls Mapping-Lock DISSENS: Status `OPEN` → `DISSENS-DOCUMENTED §3.4.1` mit Sub-Pointern
   - Falls Mapping-Lock PATCH: Status `OPEN` → `RESOLVED-IN-V0.1.3` bei Merge der Sentinel-Invariante

5. **Self-Test T19-T20:** beide Pfade (Sentinel + Argument-direkt) PASS in `tests/smoke_self_test.py`

6. **Estimated-Aufwand:** ~1.5h Self-Edit (Pre-Flight-Lockerung + zwei Doku-Sektionen + Self-Test-Erweiterung)

#### Migration

```yaml
friction_log_status: OPEN → Affordance-Documented (advisor-Position)
ODER (bei Worker-Counter): OPEN → DISSENS-DOCUMENTED §3.4.1 mit Sub-Pointern
relation_to_v1_recommendation: "v1 verworfen via empirische Pilot-Empirie; v2 akzeptiert"
mapping_decision: D-004
mapping_decision_pointer: bridge/artifacts/mapping-decisions.md#d-004
empirical_validation: "bridge-pair p3-real-user R0-R20 sauberer Lifecycle mit Argument-Pin"
```

#### Pflicht-Felder

```yaml
befund_id: F-RP-23
real_id: F-RP-23 (existiert)
mapping_category: AFFORDANCE (advisor-Position; ggf. DISSENS-DOCUMENTED §3.4.1 nach Worker-Counter)
sot_locus: bridge-attach SKILL.md §sentinel-bypass-affordance
substanz_boden:
  - "Pilot-Empirie p3-real-user R0-R20: Argument-Konsumption funktional, kein Lifecycle-Block"
  - "Annex §2.1 F1.2 Sub-Pattern brauchbare Illegalität — operativ funktional trotz formaler Abweichung"
  - "Annex §2.1 F4.1 pflicht_workflow Spannung produktiv führen, nicht auflösen"
  - "Annex §3.2 Affordance-Definitions-Kriterien erfüllt: beide Pfade funktional, Use-Pattern hat Affordance-Wert (advisor-Komfort wenn Worker-Session-ID bereits bekannt)"
inflation_protection_check:
  - "AFFORDANCE-Default für operative Pattern mit Doku-Konsequenz ✓"
  - "ABER: möglicher Worker-Counter mit PATCH-Position (folgt friction-log-Empfehlung Option v1) → könnte zu DISSENS-DOCUMENTED §3.4.1 KOMPETITIV werden"
  - "Bei Dissens-Lock: explizite zwei Positionen + Sub-Typ-Wahl §3.4.1 (kompetitiv: PATCH ⊥ AFFORDANCE)"
counter_to_friction_log_recommendation: "v1 (PATCH) verworfen via empirische Pilot-Empirie; v2 (AFFORDANCE mit Pre-Flight-Lockerung) akzeptiert"
```

#### Cross-References

- Annex §2.1 F1.2 (brauchbare Illegalität Sub-Pattern)
- Annex §2.1 F4.1 (Spannung als Ressource pflicht_workflow)
- Annex §3.2 (Affordance-Definitions-Kriterien)
- Annex §3.4.0 (Inflations-Schutz — möglicher Übergang zu §3.4.1 bei Worker-Counter)
- friction-log F-RP-23 (Quell-Befund + Original-Patch-Empfehlung Option v1)
- handover R3 Spannung S3 (Sentinel-vs-Argument-Konsumption als initial-advice-Spannungs-Kandidat)
- handover R5 Teil C (Frame-Anwendung Sentinel-Spec vs Argument-Konsumption)
- bridge-init R0 (empirische Argument-Konsumption)

---

### D-004 R23-Revision (advisor Position-Revidierung post Worker-Counter R22)

**Anlass:** Worker-Counter R22 mit 4 Substanz-Argumenten + Frame-Counter F1.1+F4.2. Argument 3 (Konsistenz mit D-002 Marketplace-Adoption-Methodik) ist methoden-logischer Treffer — advisor-eigene D-002-Argumentation wird hier inkonsistent angewandt.

**advisor Selbst-Diagnose:**

In D-002 (F-RP-32) habe ich Plugin-Marketplace-Adoption-Argument **PRO PATCH** verwendet (Robustheit > Flexibility). In D-004 habe ich **gleiches Argument ignoriert** und für AFFORDANCE plädiert. Das ist Methoden-Inkonsistenz advisor-side, nicht Substanz-Differenz. Worker-Counter ist kein "andere Meinung", sondern "deine Position widerspricht eigener Methodik".

Plus: F4.2 Profile-Frame "strukturelle Quelle vor lokaler" verlangt Spec-Author-Empfehlung > Pilot-n=1. Auch das spricht gegen ursprüngliche AFFORDANCE-Position.

#### Position-Revidierung

| Pflicht-Feld | Original-D-004 | Revidiert R23 |
|---|---|---|
| **mapping_category** | AFFORDANCE | **PATCH** |
| **frame** | F1.2 primär + F4.1 sekundär | **F1.1 primär + F4.2 sekundär** (Worker-Frame übernommen) |
| **sot_locus** | bridge-attach §sentinel-bypass-affordance | **(entfällt)** — kein Skill-Doku-Sektions-SoT, sondern friction-log-RESOLVED-Status |
| **substanz_boden** | Pilot-Empirie + brauchbare Illegalität + Spannung-produktiv | **friction-log Option v1 + CRITICAL-Severity + Marketplace-Adoption-Konsistenz mit D-002 + n=1-Methoden-Disziplin** |
| **migration** | OPEN → Affordance-Documented | **OPEN → RESOLVED-IN-V0.1.3** (bei Patch-Merge Option v1) |
| **counter_to_friction_log_recommendation** | "v1 verworfen" | **revidiert: "v1 akzeptiert nach Worker-Counter R22"** |
| **inflation_protection_check** | AFFORDANCE-Default | **nicht anwendbar** (substanziv-begründeter Counter, akzeptiert Worker-Methoden-Position-Differenzierung) |

#### Pilot-Empirie-Status

Pilot-Empirie p3-R0-R20 (Argument-Konsumption funktional, kein Lifecycle-Block) wird **nicht verloren**:

- als Plugin-Dev-Action-Cross-Reference dokumentiert: "Empirie zeigt: Pre-Flight 4 in v0.1.2 toleranter als Spec angegeben — möglicherweise Implementation-Bug oder Plugin-Version-Path-Diff. Pre-Flight 4 Strict-Enforcement-Patch sollte beide Pfade testen (positive case Sentinel + negative case Argument-direkt FAIL erwartet)."
- als historischer Affordance-Test-Case: "Argument-Konsumption hat in p3-Pilot funktional gewirkt; PATCH-Decision priorisiert Spec-Konsistenz + Marketplace-Adoption über lokale Empirie."

Empirie wird Methoden-Beleg statt Decision-Boden.

#### Plugin-Dev-Action-Spec PATCH-Pfad (revidiert, übernommen aus Worker-R22 Teil C)

1. **bridge-init SKILL** — `--worker-session-id`-Flag enforcen Sentinel-Pfad (entweder Argument entfernen oder WARN-mit-Auto-Sentinel-Override)
2. **bridge-attach SKILL** Pre-Flight 4 strikt auf Sentinel-String (kein auto-recover-Branch)
3. **Worker-Notification-Block** post-init: Worker-Session-ID intern resolven (z.B. via session_info MCP), state.json schreibt immer Sentinel
4. **Self-Test T19-T20** für Sentinel-Pfad-Invariante (positive cases)
5. **Self-Test T21** negative case: bridge-init mit `--worker-session-id` hard-FAIL oder WARN-mit-Auto-Sentinel-Override
6. **Doku-Update bridge-init.md** §worker-session-id-Resolution: explizit Sentinel-Pfad-Invariante markieren
7. **Empirie-Test in Plugin-Dev-Cycle:** Pre-Flight 4 v0.1.2 Tolerance-Befund verifizieren (war p3-Pilot Implementation-Bug oder Version-Path-Diff?)
8. **Estimated-Aufwand:** ~2-3h Self-Edit (Worker-R22 Teil C Estimated übernommen)

#### Sub-Typ-Klarstellung

**KEIN Dissens-Documented-Lock.** Position-Revidierung ist Konsens-Konvergenz nach Counter, nicht Dissens. §3.4.1 KOMPETITIV (Worker-Vorschlag) und §3.4.2 SKOPUS-Differenz (alternative advisor-Lesart) sind beide nicht angewandt — D-004 wird PATCH-locked nach Worker-R24-Konvergenz.

#### Pflicht-Felder (revidiert)

```yaml
befund_id: F-RP-23
real_id: F-RP-23
mapping_category: PATCH (revidiert R23)
mapping_category_history:
  - {round: 21, position: "AFFORDANCE", initiator: advisor}
  - {round: 22, counter: "PATCH", initiator: worker}
  - {round: 23, position_revidiert: "PATCH", initiator: advisor, basis: "Worker-Argument 3 Methoden-Logik-Treffer + F4.2 strukturelle Quelle vor lokaler"}
sot_locus: friction-log F-RP-23 mit RESOLVED-IN-V0.1.3-Status (kein Skill-Doku-SoT bei PATCH)
substanz_boden:
  - "friction-log Option v1 explizite Spec-Author-Empfehlung"
  - "CRITICAL-Severity → Spec-Konsistenz priorität gegenüber AFFORDANCE-Pfad"
  - "Plugin-Marketplace-Adoption-Argument konsistent mit D-002-Methodik"
  - "n=1 Pilot-Empirie nicht generalisierbar gegen Spec-Author-Empfehlung"
methoden_konsistenz_check: "D-002 + D-004 nutzen jetzt gleiche Marketplace-Adoption-Argumentation für Robustheit > Flexibility bei Lifecycle-kritischen Pfaden"
inflation_protection_check: "nicht anwendbar — Position-Revidierung nach methoden-logischem Counter, nicht Default-Inflation"
```

#### Worker-Action R24

1. friction-log F-RP-23 Status `OPEN` → `RESOLVED-IN-V0.1.3` mit:
   - `resolved_in_version: V0.1.3 (bei Patch-Merge)`
   - `mapping_decision: D-004`
   - `mapping_decision_pointer: bridge/artifacts/mapping-decisions.md#d-004-r23-revision`
   - `position_revidierung_note: "advisor R21-AFFORDANCE → R23-PATCH nach Worker-Counter R22 mit 4 Substanz-Argumenten"`
   - `pilot_empirie_cross_reference: "p3-real-user R0-R20 Argument-Konsumption funktional — als historischer Affordance-Test-Case + Implementation-Bug-Verdacht für Pre-Flight 4 Tolerance v0.1.2"`
2. Konvergenz-Antwort R24 als type=re-sync mit per-Pflicht-Feld-Akzeptanz der Revidierung

---

### D-005 — F-RP-15 + M-5 (gebündelt, ZWEI KATEGORIEN) → PATCH + AFFORDANCE

**Round-Decided:** R25 (advisor-initiator, dieser Eintrag)
**Konvergenz-Status:** pending (Worker-Antwort R26 erwartet)
**Bündelung-Format:** ein D-Eintrag mit zwei Sub-Befunden + zwei Kategorien (Counter zu Worker-Bündelungs-Erwartung "beide AFFORDANCE" aus R15)
**Methoden-Konsistenz-Begründung für Sub-A PATCH-Wahl:** D-002 (F-RP-32 PATCH wegen Marketplace-Adoption) + D-004-Sequence (R21-AFFORDANCE → R23-PATCH-Revidierung) etablieren Plugin-Marketplace-Adoption-Argument als advisor-Methodik — F-RP-15 HIGH-Severity-Setup-Blocker fällt unter gleiche Argumentation.

#### Sub-A: F-RP-15 (Mount-Inkonsistenz `~/session-bridge/`) → PATCH

**Real-friction-log-Match:** F-RP-15 HIGH (existiert seit 2026-04-26)
**Severity:** HIGH ("Setup-Blocker wenn nicht dokumentiert")
**Frame:** F1.1 (Mitgliedschaftsbedingungen-Säule — Sandbox-Mount-Konvention als Operations-Eintritts-Bedingung für Profile-Loading via Subprocess) + F4.2 sekundär (strukturelle Quelle Plugin-Spec vs lokale User-Workaround Add-Dir)

##### Befund-Beschreibung

`~/session-bridge/` ist nicht in jeder Cowork-Session sandbox-mounted (workspace-bash). Profile-Loading via Subprocess-Aufruf scheitert wenn Plugin auf Profile-Files zugreifen will. User-Workaround: Add-Dirs in jeweiligen Cowork-Projects setzen.

friction-log Patch-Vorschlag (übernommen):
- Pre-Flight Schritt 5 differenziert "Profile existiert auf Host (Read-Tool)" vs "Profile sandbox-erreichbar (workspace-bash)"
- bridge-init.md Doku-Erweiterung: "Plugin-Use-Project muss `--expertise-profile`-Pfad als Add-Dir oder im Working-Dir haben"

##### Decision (advisor-Position)

**PATCH.** Pre-Flight 5 erweitern + Doku-Pflicht. Begründung:

1. **Methoden-Konsistenz mit D-002/D-004:** Plugin-Marketplace-Adoption-Argument konsistent angewandt — Robustheit > Flexibility bei Lifecycle-kritischen Pfaden. F-RP-15 HIGH ist Setup-Blocker = Lifecycle-relevant.
2. **CRITICAL/HIGH-Severity-Spec-Konsistenz-Priorität (Worker-R22-Argument 2):** HIGH-Items haben Spec-Konsistenz-Priorität gegenüber AFFORDANCE-Pfaden. AFFORDANCE-Pfade sollten BEOBACHTUNG/MEDIUM-Severity-Befunde sein.
3. **n=1-Empirie nicht generalisierbar (Worker-R22-Argument 4):** User-Workaround "Add-Dir setzen" ist 1-User-Empirie. Spec-Patch ist robuster Rahmen.
4. **F4.2 strukturelle Quelle vor lokaler:** friction-log-Spec-Author hat Patch-Vorschlag explizit gemacht — Counter dazu mit lokaler Workaround-Empirie wäre Methoden-Inkonsistenz.

##### Worker-Action (im Bridge-Pair) — Sub-A

1. friction-log F-RP-15 Status `OPEN` → `RESOLVED-IN-V0.1.3` mit:
   - resolved_in_version: V0.1.3 (bei Pre-Flight 5 Differenzierungs-Patch-Merge)
   - mapping_decision: D-005 Sub-A
   - frame: F1.1 + F4.2
   - sot_locus: bridge-init SKILL.md Pre-Flight 5 erweitert + Doku-Sektion §sandbox-mount-prerequisite

##### Plugin-Dev-Action (out-of-pair) — Sub-A

1. **bridge-init SKILL.md Pre-Flight 5 Erweiterung:**
   ```
   5. Profile-Validation (erweitert):
      a. Profile-Pfad existiert auf Host (Read-Tool-Check) — bestehender Test
      b. Profile-Pfad sandbox-erreichbar (workspace-bash test -d <profile-path>)
         → bei FAIL: WARN "Profile-Pfad nicht sandbox-mounted —
            Subprocess-Aufrufe werden scheitern. Add-Dir im Cowork-Project
            setzen oder Profile in Working-Dir verschieben."
   ```
2. **bridge-init SKILL.md neue Sektion §sandbox-mount-prerequisite:**
   ```
   Plugin-Use-Project Setup-Pflicht:
   - --expertise-profile-Pfad muss entweder im Cowork-Project Working-Dir
     liegen ODER als Add-Dir im Cowork-Project konfiguriert sein
   - Sonst: Subprocess-Aufrufe via workspace-bash auf Profile-Files scheitern
     mit "No such file or directory" trotz Pre-Flight Schritt 5a PASS
   - Empirie: bridge-pair p3-real-user — Profile-Pfad
     `/Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/`
     erforderte Add-Dir in beiden Cowork-Projects (advisor + worker)
   ```
3. **Self-Test T22:** Pre-Flight 5b sandbox-erreichbar negative case
4. **Estimated-Aufwand:** ~1.5h Self-Edit (Pre-Flight-Erweiterung + Doku-Sektion + Self-Test)

##### Pflicht-Felder Sub-A

```yaml
befund_id: F-RP-15
real_id: F-RP-15
mapping_category: PATCH
frame: F1.1 primär + F4.2 sekundär
sot_locus: bridge-init SKILL.md Pre-Flight 5 + §sandbox-mount-prerequisite
substanz_boden:
  - "Plugin-Marketplace-Adoption-Argument konsistent mit D-002/D-004 (Methodik-Konsistenz)"
  - "HIGH-Severity-Spec-Konsistenz-Priorität (Worker-R22-Argument 2)"
  - "n=1 User-Workaround-Empirie nicht generalisierbar"
  - "F4.2 strukturelle Quelle (friction-log-Spec-Author-Patch-Vorschlag) vor lokaler"
counter_to_worker_bundling_expectation: "Bündelungs-Wahl AFFORDANCE/AFFORDANCE aus R15 wird durch Sub-A PATCH-Position ersetzt; Worker-R20 hat D-002-Marketplace-Adoption-Argumentation explizit akzeptiert + Worker-R24 dissens-management-Pointe anerkannt → Methoden-Konsistenz-Erwartung"
methoden_konsistenz_check: "D-002 + D-004 + D-005-Sub-A nutzen jetzt einheitliche Marketplace-Adoption-Argumentation für Robustheit > Flexibility bei HIGH/CRITICAL-Severity"
```

#### Sub-B: M-5 (Konvergenz-Skip-Konvention durch Worker selbst R11) → AFFORDANCE

**Real-friction-log-Match:** NEW (Bridge-Pair-Origin in Worker-R8 Spec-Author + R11 Self-Bypass)
**Severity:** BEOBACHTUNG
**Frame:** F4.2 primär (Anti-AP-08-Korrektiv) + F4.1 sekundär (Spec-Author + Spec-Bypasser-Rollen-Trennung als produktive Skopus-Spannung)

##### Befund-Beschreibung

Worker-R8 Teil C definierte Konvergenz-Kriterium ("Folge-Round muss explizit pro-Punkt antworten"). Worker-R11 schrieb decision-lock OHNE Advisor-Antwort auf R10 → Self-Bypass eigener procedural Spec. Worker hat in R8 Selbst-Reflexion AP-08-VERDACHT NIEDRIG markiert + Konsens-Konvergenz-Kriterium institutionalisiert.

##### Decision (advisor-Position)

**AFFORDANCE.** Konvergenz-Kriterium-Skip-Konvention dokumentieren. Begründung:

1. **Annex §3.4.0 Inflation-Schutz:** AFFORDANCE-Default für operative Pattern mit Doku-Konsequenz — M-5 ist genau das.
2. **F4.2 Anti-AP-08-Korrektiv:** Skip-mit-Markierung ist methoden-sauberer als Pflicht-Wartezeit (AP-09-Reflex).
3. **F4.1 Spec-Author + Bypasser-Rollen-Trennung:** Worker hat in R8 Spec-Author-Rolle + in R11 Spec-Bypasser-Rolle gespielt. Das ist nicht Pathologie, sondern produktive Skopus-Spannung — beide Rollen in einer Session sind methodisch zulässig wenn explizit markiert.
4. **Empirisch funktional:** R11-Bypass hat keinen Lifecycle-Schaden produziert (R12 Teil C bestätigte started_round=12 nachträglich).

##### Worker-Action (im Bridge-Pair) — Sub-B

1. friction-log-Neueintrag erstellen: F-RP-34 BEOBACHTUNG (oder nächste freie ID): "Konvergenz-Kriterium-Self-Bypass-Konvention via Skip-mit-Markierung"
2. Status direkt `Affordance-Documented` (kein OPEN-Zwischenstadium, weil Pattern bereits funktional verifiziert)
3. SoT-Pointer: `bridge-handover SKILL.md §konvergenz-skip-rationale` (Plugin-Dev-Action ausstehend in v0.1.3)
4. mapping_decision: D-005 Sub-B
5. mapping_decision_pointer: `bridge/artifacts/mapping-decisions.md#d-005`

##### Plugin-Dev-Action (out-of-pair) — Sub-B

1. **bridge-handover SKILL.md neue Sektion §konvergenz-skip-rationale:**
   ```
   §konvergenz-skip-rationale (Affordance-Documented):
   
   Konvergenz-Kriterium aus eigener Pair-Round darf in nachfolgender Round
   übersprungen werden, wenn Substanz-Konvergenz bilateral schon erreicht ist
   (z.B. via Plan-Layer-Akzeptanz aus früherer Round).
   
   Pflicht-Markierung: Skip-Round Body enthält status_observations[]-Eintrag:
     type: convergence_criterion_skip
     defined_in_round: <N>  (Round, die Kriterium definiert hat)
     skipped_in_round: <M>  (diese Round)
     skip_basis: "<Begründung — z.B. bilaterale Substanz-Konvergenz>"
     cycle_counter: <Anzahl Cycles seit Definition>
   
   Anti-Pattern: Skip ohne Markierung = AP-08-Bypass-Verdacht.
   Skip mit Markierung = legitime Affordance.
   ```

2. **bridge-handover SKILL.md Pre-Flight 6 (NEU):** wenn Round-N-Body methoden-Tags enthält ("Konvergenz-Kriterium definiert"), check in Round-N+1 ob Skip-Markierung vorhanden falls Konvergenz-Kriterium übersprungen wird.
3. **Estimated-Aufwand:** ~30min Self-Edit (klein, reine Doku + Pre-Flight-Check)

##### Pflicht-Felder Sub-B

```yaml
befund_id: M-5 (Bridge-Pair-Bezeichnung aus Worker-R13)
real_id: NEW (friction-log-Neueintrag F-RP-34 in Worker-Action #1)
mapping_category: AFFORDANCE
frame: F4.2 primär + F4.1 sekundär
sot_locus: bridge-handover SKILL.md §konvergenz-skip-rationale
substanz_boden:
  - "Annex §3.4.0 Inflation-Schutz: AFFORDANCE-Default für operative Pattern mit Doku-Konsequenz"
  - "F4.2 Anti-AP-08-Korrektiv: Skip-mit-Markierung > Pflicht-Wartezeit"
  - "F4.1 Spec-Author + Bypasser-Rollen-Trennung als produktive Skopus-Spannung"
  - "Empirisch funktional: R11-Bypass keine Lifecycle-Schäden"
inflation_protection_check:
  - "AFFORDANCE-Default angewandt — keine Worker-vs-Advisor-Position-Differenz ✓"
  - "BEOBACHTUNG-Severity konsistent mit AFFORDANCE-Kategorie ✓"
```

#### Bündelungs-Begründung

Beide Items sind v0.1.3-Patch-Welle-Items mit verschiedenen Kategorien (PATCH + AFFORDANCE), aber:

- Beide haben SoT-Locus in bridge-init bzw. bridge-handover SKILL-Doku-Sektionen → gemeinsame Plugin-Dev-Workflow-Pipeline
- Beide haben kleine Estimated-Aufwände (~1.5h + ~30min = 2h gesamt)
- Beide werden in der gleichen v0.1.3-Patch-Welle gemerged
- Bündelung in einer Mapping-Round spart Round-Overhead trotz Kategorien-Differenz

#### Pending-Decisions Update

| Round | Befund | Vorschlag-Kategorie |
|---|---|---|
| R26 | (Worker-Konvergenz D-005 Sub-A PATCH + Sub-B AFFORDANCE + friction-log F-RP-15 RESOLVED-IN-V0.1.3 + F-RP-34 NEU) | — |

**Mapping-Phase-Ende: R26.** Innerhalb max-Budget 14 (R12-R26). Klarstellungs-Reserve aufgebraucht (R13/R17). T1-Trigger nicht aktiviert wenn alle 5 Decisions bei R26 entschieden.

---

## Pending-Decisions (geplant, post R25-D-005)

| Round | Befund | Vorschlag-Kategorie |
|---|---|---|
| R26 | (Worker-Konvergenz D-005 Sub-A + Sub-B + Mapping-Phase-Ende) | — |

**Budget-Konsequenz:** R26 = max-Budget exakt 14 (R12-R26).

---

## Decision-Log Versionierung

| Version | Datum | Änderung |
|---|---|---|
| v0.1.0 | 2026-04-28 (R16) | Initial: D-001 retrospektiv formalisiert + D-002 NEU |
| v0.1.1 | 2026-04-28 (R17) | D-002 R17-Klarstellung-Annex: Workflow-Direktive Option A + F-RP-26-Match-Klärung + advisor-Selbst-Diagnose |
| v0.1.2 | 2026-04-28 (R19) | D-003 NEU: M-3 (`pre-allocated`-Pattern) → AFFORDANCE; Pending-Decisions-Tabelle aktualisiert (R20-R24) |
| v0.1.3 | 2026-04-28 (R21) | D-004 NEU: F-RP-23 (Sentinel-Bypass) → AFFORDANCE (advisor-Position); Counter-friction-log-Empfehlung v1 explizit dokumentiert; Pending-Tabelle für möglichen DISSENS-Pfad erweitert |
| v0.1.4 | 2026-04-29 (R23) | D-004 R23-Revision: AFFORDANCE → PATCH nach Worker-Counter R22 mit 4 Substanz-Argumenten; advisor-Selbst-Diagnose Methoden-Inkonsistenz mit D-002 explizit; Pilot-Empirie als Cross-Reference behalten; mapping_category_history-Feld hinzugefügt |
| v0.1.5 | 2026-04-29 (R25) | D-005 NEU: F-RP-15 + M-5 (gebündelt, ZWEI KATEGORIEN — Sub-A PATCH + Sub-B AFFORDANCE); Counter zu Worker-Bündelungs-Erwartung "beide AFFORDANCE" mit Methoden-Konsistenz-Begründung (D-002/D-004-Marketplace-Adoption-Argumentation); letzte Mapping-Decision der Phase |

**Update-Konvention:** Append-only. Pro neuer Decision: D-NNN-Eintrag + Pending-Decisions-Tabelle aktualisieren. Konvergenz-Status-Update bei Worker-Antwort.
