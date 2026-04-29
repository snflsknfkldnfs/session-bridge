# Real-User-Pilot Setup Friction-Log

**Pilot-ID:** p3-real-user
**Datum:** 2026-04-28 (Wakeup-Session)
**Plugin-Version:** v0.1.2 + Profile process-consulting v0.1.0 (private-notes)
**Profile-Pfad:** `/Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting`
**shared-path:** `/Users/paulad/session-bridge/pilot-runs/p3-real-user/`

## Setup-Topology

| Project | Working-Dir | Plugin? | Rolle |
|---|---|---|---|
| session-bridge-plugin-dev | `/Users/paulad/session-bridge/` | NEIN | Plugin-Dev (kein Bridge-Teilnehmer) |
| process-consulting-advisor-pilot | `/Users/paulad/process-consulting-pilot/` | JA | Advisor |
| (Worker-Project) | TBD | JA | Worker |

## Friction-Log-Format

```
## F-RP-XX <Severity>: <Kurze-Beschreibung>
**Phase:** <Setup-Phase>
**Session:** <welche Session>
**Beobachtet:** <was passierte>
**Erwartet:** <was sollte laut Spec passieren>
**Workaround:** <wie umgangen>
**Plugin-Patch-Vorschlag:** <was im Plugin/Doku zu ändern>
**Severity:** CRITICAL | HIGH | MEDIUM | LOW
**Status:** OPEN | RESOLVED-IN-SESSION | DEFERRED-V0.1.3
```

## Setup-Phasen-Plan

### Phase 0: Pre-Setup-Verifikation

- [ ] Plugin v0.1.2 in Cowork installiert + aktiv
- [ ] Profile-Verzeichnis existiert + alle 4 required_files
- [ ] shared-path-Verzeichnis existiert + beschreibbar
- [ ] gh-CLI authentifiziert für Plugin-Updates

### Phase 1: Plugin-Dev-Project anlegen (Cowork-UI)

User-Aktion in Cowork-Desktop-App:
- [ ] Customize → "+ Neues Project"
- [ ] Name: `session-bridge-plugin-dev`
- [ ] Working-Directory: `/Users/paulad/session-bridge/`
- [ ] Add-Dirs: `/Users/paulad/session-bridge/private-notes/` (Read+Write für Profile-Edits)
- [ ] **Plugin-Install: NEIN** (Strict-Separation, ADR_0021)
- [ ] Project-Instructions: leer oder minimal

### Phase 2: Advisor-Project anlegen (Cowork-UI)

User-Aktion:
- [ ] Customize → "+ Neues Project"
- [ ] Name: `process-consulting-advisor-pilot`
- [ ] Working-Directory: `/Users/paulad/process-consulting-pilot/`
- [ ] Add-Dirs:
  - [ ] `/Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/` (Read-Only — Profile-Loading)
  - [ ] `/Users/paulad/session-bridge/pilot-runs/p3-real-user/` (Read+Write — shared-path)
- [ ] **Plugin-Install: JA** — session-bridge v0.1.2 aktivieren
- [ ] Project-Instructions: optional Hinweis "advisor in process-consulting-pilot, Profile aktiv"

### Phase 3: Worker-Project klären

**OFFEN** — welcher konkrete Beratungs-Use-Case wird Worker-Anliegen?

Kandidaten:
- (a) Mock-Worker für Test-Lifecycle (kein echtes Anliegen, nur Schema-Round-Trip)
- (b) Real-Anliegen aus Plugin-Dev (z.B. "wie strukturieren wir Phase 2 weiter?")
- (c) Real-Anliegen aus Schul-Kontext (z.B. konkrete Beratungs-Frage zu Klasse/Fach)
- (d) Real-Anliegen aus Hub-Repo-Strategie (weitergehts-plugins, Public-Release)

Worker-Project-Setup analog Phase 2 (Add-Dir auf shared-path, Plugin installiert).

### Phase 4: Advisor-Init

In Advisor-Project-Session:
```
/bridge-init --role=advisor --topic="<topic>" \
  --shared-path=/Users/paulad/session-bridge/pilot-runs/p3-real-user \
  --expertise-source="Prozess-/Organisationsberatung (Kühl + Humanisierung)" \
  --expertise-profile=/Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting
```

**Erwartung Pre-Flight:**
- Schritt 1 (shared-path writable) PASS
- Schritt 2 (state.json existiert nicht) PASS
- Schritt 3 (jsonschema) PASS
- Schritt 4 (session_info MCP) PASS oder DEGRADED
- Schritt 5 (Profile-Validation) PASS — alle 4 required_files erreichbar

**Friction-Hypothese:** Profile-Pfad-Resolution in Cowork-Sandbox.

### Phase 5: Worker-Attach

In Worker-Project-Session (User kopiert Block aus Advisor-Notification):
```
/bridge-attach <pair_id> --role=worker --shared-path=/Users/paulad/session-bridge/pilot-runs/p3-real-user --worker-focus="<focus>"
```

**Erwartung:** Phase init → scope-lock, beide roles gefüllt.

### Phase 6: Erste Round (initial-advice)

Advisor-Skill triggert Schritt 0 Profile-Loading + Schritt 1 Status-Snapshot + Schritt 3 Handover-Write.

**Empirie-Beobachtung:**
- Wird Profile geladen?
- Wird linkage_to_bridge_rounds["initial-advice"] angewendet?
- Welche Frames werden angesprochen?
- Wie wird Question-Bank genutzt?
- Wie wird Anti-Pattern-Hypothese formuliert?

## Friction-Befunde

### F-RP-21 HIGH: BP-ADVISOR-Skill identifizierte FALSCHE Worker-Session-ID

**Phase:** Phase 4 Advisor-Init Worker-Identifikation
**Session:** BP-ADVISOR (local_9167bbb1)
**Beobachtet:** Skill behauptete Worker-Kandidat sei `local_702ccc6a-50a9-4ed6-b8ab-b17ca078ecc8` mit Title "Bridge-Plugin Dev". Tatsächlich:
- `local_702ccc6a` ist die **Plugin-Dev-Helfer-Session** (diese Cowork-Chat-Session, weitergehts-online-Project)
- Echte Worker-Session "BP-WORKER" hat ID `local_e9ba7337-68d6-4050-8759-bc47ee9dc1e0`

**Erwartet:** Skill hätte explizit nach Worker-Session-ID fragen müssen (Anti-Inferenz-Protokoll P-RP-02), oder Title-Match strikter prüfen.
**Workaround:** User-Verifikation hat den Fehler aufgedeckt; Re-Init mit korrekter ID nötig.
**Plugin-Patch-Vorschlag:**
- bridge-init.md SKILL: bei Worker-Identifikation via session_info NICHT inferieren — IMMER User-Bestätigung "Ist `<session-id>` (Title: `<title>`) die richtige Worker-Session?"
- Title-Match-Logik überprüfen: Skill hat möglicherweise "Bridge-Plugin Dev" als fuzzy-Match auf eine andere Session interpretiert
- Plus: Skill könnte aktuelle Session-ID des Advisor selbst (this_session_id) als ANTI-MATCH-Filter nutzen — eigene Session kann nie Worker sein
**Severity:** HIGH (kritischer Anti-Inferenz-Verstoß, hätte zu Self-Reflexion-Schleife geführt wenn nicht entdeckt)
**Status:** OPEN

### F-RP-16 CRITICAL: --expertise-profile wurde nicht gesetzt im Init, Profile-Loading geskippt

**Phase:** Phase 4 Advisor-Init (BP-ADVISOR-Session)
**Session:** BP-ADVISOR (local_9167bbb1)
**Beobachtet:** Skill nutzte Visualization-Widget für Argument-Erfassung. User gab Topic + shared-path + expertise-source ein, aber **expertise-profile blieb leer**. Pre-Flight Schritt 5 dann SKIPPED. Pair faktisch ohne Profile initialisiert (pair_id 14e21d93-1f1a-417f-82ff-d4743cdf28d5).
**Erwartet:** Skill sollte bei Topic = "bridge-plugin development" o.ä. Beratungs-relevantem Topic explizit nach Profile fragen, ODER Form-Widget sollte Profile-Feld prominent enthalten.
**Workaround:** Re-Init nötig (alten state.json löschen + neu /bridge-init mit --expertise-profile).
**Plugin-Patch-Vorschlag:**
- bridge-init.md SKILL: bei Topic-Keywords ["consulting", "organisation", "strategie", "beratung", "plugin", "OE"] PFLICHT-Frage "Soll ein Expertise-Profile aktiviert werden? Verfügbare Profile: ..."
- Form-Widget: expertise-profile-Feld als prominentes Eingabe-Feld mit Profile-Lookup-Button
- Falls --expertise-profile leer aber expertise-source nichttrivial gesetzt: WARN "Beratungs-Source ohne Profile aktiv — Methodik-Workflows werden nicht angewendet"
**Severity:** CRITICAL (zentraler Pilot-Aspekt verfehlt)
**Status:** OPEN

### F-RP-17 MEDIUM: Sandbox-rm-EPERM bei Pre-Flight Schritt 1

**Phase:** Phase 4 Advisor-Init Pre-Flight
**Session:** BP-ADVISOR
**Beobachtet:** Skill machte `mkdir bridge/ && touch .write-test && rm .write-test` als Pre-Flight 1. mkdir + touch PASS, aber `rm` failed mit EPERM (permissions). Skill markierte Schritt als DEGRADED, fiel zurück auf Write-Tool für state.json-Write.
**Erwartet:** Pre-Flight 1 sollte als PASS gelten wenn Write-Tool als Alternativ-Mechanismus funktioniert.
**Workaround:** Skill nutzte Write-Tool, state.json wurde geschrieben.
**Plugin-Patch-Vorschlag:**
- bridge-init.md Pre-Flight-Sektion: Test-Sequenz präzisieren — wenn Sandbox-rm fail, dann Write-Tool als Fallback testen, dann PASS markieren
- Sandbox-vs-Host-MCP-Mechanismus-Tabelle ergänzen: "Sandbox-mkdir+touch funktioniert, Sandbox-rm scheitert mit EPERM bei nicht-eigenen Files (selbst eigene Test-Files)"
**Severity:** MEDIUM (kein Blocker, aber DEGRADED-Status verwirrt User)
**Status:** OPEN

### F-RP-18 LOW: Restspur bridge/.write-test post-Pre-Flight

**Phase:** Phase 4 Advisor-Init Pre-Flight
**Session:** BP-ADVISOR
**Beobachtet:** `.write-test`-File aus Pre-Flight-Schritt-1-Test bleibt im shared-path/bridge/ liegen weil Sandbox-rm scheitert.
**Erwartet:** Cleanup nach Pre-Flight.
**Workaround:** manueller Cleanup via Host-MCP osascript.
**Plugin-Patch-Vorschlag:** Pre-Flight 1 nutzt Host-MCP osascript für rm wenn Sandbox-rm fail (analog write-Mechanismus-Switch).
**Severity:** LOW (Hygiene, kein Daten-Issue)
**Status:** OPEN

### F-RP-19 BEOBACHTUNG: Visualization-Widget als Form-UI für Init

**Phase:** Phase 4 Advisor-Init
**Session:** BP-ADVISOR
**Beobachtet:** Skill nutzte `mcp__visualize__show_widget` für strukturierte Argument-Erfassung statt nur Text-Slash-Args. UX-Innovation — User füllt Form, Skill liest aus.
**Erwartet:** Args via Slash-Command-Argumente.
**Workaround:** keiner nötig — Form funktioniert.
**Plugin-Patch-Vorschlag (Erweiterung, nicht Fix):**
- Form-Widget sollte alle Pflicht-Argumente prominent enthalten inklusive `--expertise-profile`
- Form-Widget sollte Profile-Auswahl als Dropdown ermöglichen (Lookup auf `expertise-profiles/`-Verzeichnisse)
- Innovation als Pattern dokumentieren in bridge-init.md (UX-Best-Practice)
**Severity:** BEOBACHTUNG (positiv + ausbaufähig)
**Status:** OPEN-OPPORTUNITY

---

### F-RP-31 CRITICAL: User hat keine Lifecycle-Visibility — "nie klar wurde, was Stand der jeweiligen Session ist, was übergeben wurde"

**Phase:** durchgängig Round 1-8
**Session:** beide BP-Sessions (User-Perspektive)
**Beobachtet:** Aus Session-Export-User-Messages BP-WORKER (9 freie Eingaben über 8h):
- Msg #4 (11:22Z): "advisor hat abgeschlossen, evaluiere" — User schätzt Status extern
- Msg #6 (12:02Z): "advisor hat gearbeitet" — User-Inferenz aus Advisor-Chat-Plan-Text, keine Bridge-Evidenz (löste Round 7 Visibility-Probe aus)
- Msg #7 (12:10Z): "sollte jetzt sichtbar sein" — User-Erwartung ohne Verifikations-Tool
- Msg #9 (14:16Z): "welche rolle nimmst du gerade ein?" — User merkt selbst Role-Drift, weil keine Skill-Boundary-Visibility

User-Originalwortlaut zur Friction: "nie klar wurde, was der stand der jeweiligen session ist, was übergeben wurde, etc.pp."

**Erwartet:** User-facing Lifecycle-Status muss in jeder Session jederzeit abrufbar sein:
- Welche Rolle hat diese Session?
- Welche Rounds existieren? (von wem, welcher type, wann)
- Was hat die andere Session zuletzt geschrieben?
- Was wartet als nächste erwartete Aktion?
- Worker-Skill vs Advisor-Skill — welcher Modus ist aktiv?

**Workaround:** User fragte mich (orchestrierender Assistant in dritter Session) als externen Status-Polling-Service via session_info MCP + Filesystem-Read. Funktional, aber Plugin-User ohne Cross-Session-Helper hätte keine Visibility.

**Plugin-Patch-Vorschlag (v0.1.3 — TOP-PRIO):**

1. **`/bridge-status`-Command erweitern** zu User-friendly Output:
   ```
   ============================================================
   BRIDGE-PAIR <pair_id> — Phase: <phase>
   ============================================================
   Diese Session:    <role> (<title>)
   Andere Session:   <other-role> (<other-title>)
   
   Letzte 3 Rounds:
     R<n> [<type>] <from>→<to>     <timestamp>
     R<n-1> [<type>] <from>→<to>   <timestamp>
     R<n-2> [<type>] <from>→<to>   <timestamp>
   
   Nächste erwartete Aktion: <inferred-from-last-round>
   Mögliche Skill-Calls:     /bridge-handover --type=<a|b|c>
   ============================================================
   ```
2. **Auto-Status nach jedem Skill-Aufruf:** bridge-init / bridge-attach / bridge-handover geben am Ende immer kompakten Status-Block aus mit "BRIDGE-WRITE COMPLETED" + verifizierbaren Pointern (artifact_path + state.updated_at).
3. **Polling-Hint:** wenn die andere Session lange nichts geschrieben hat → /bridge-status zeigt "Last activity X min ago. Other session may be in plan-phase." Vermeidet Plan-vs-Execution-Misverständnis (siehe F-RP-29).
4. **Skill-Mode-Marker:** Worker-Skill und Advisor-Skill geben am Output-Anfang explizit aus: "[bridge-worker mode]" oder "[bridge-advisor mode | profile=process-consulting]". User sieht direkt welcher Modus aktiv ist (verhindert Role-Drift-Confusion siehe F-RP-30).

**Severity:** CRITICAL (User-Originalwortlaut: durchgängig keine Klarheit über Pilot-Verlauf)
**Status:** OPEN — patcht in v0.1.3

---

### F-RP-30 CRITICAL: Worker-Skill-Role-Drift in Advisor-Modus ohne eigenes Profile

**Phase:** Round 6, 7, 8 + Decision-Lock-Trigger
**Session:** BP-WORKER (`local_e9ba7337`)
**Beobachtet:** Worker-Skill-Spec sagt: "operative Rolle … präsentiert User mit Status-Snapshot + Optionen, schreibt Counter / Status / Pre-Flight / Execute / Verify Handovers". Worker hat KEIN Profile geladen (Profile ist advisor-only-Pin).

Tatsächliches Worker-Verhalten:
- Round 6: ad-hoc `anti-pattern-check-pre-counter` AP-06/07/08/09-Check (advisor-pflicht_workflow)
- Round 7: H1/H2/H3-Hypothesen-Diagnostik (advisor-mode)
- Round 8: AP-07/AP-08-Selbst-Diagnose + Konsens-Konvergenz-Kriterium-Institutionalisierung (advisor-mode)
- Decision-Lock-User-Trigger: Worker macht **methoden-veto** mit AP-08-Treffer-Diagnose statt operativer Skill-Execution

User-Aufdeckung in Msg #9 (14:16Z): *"welche rolle nimmst du gerade ein?"* — Worker bestätigt Role-Drift in eigenem Output: *"Verhalten ist role-gemischt. Worker-Funktion wäre stattdessen: User-Input → Skill-Aufruf → operative Execution. Ohne Methoden-Overlay."*

**Ursache:** Profile-References im Advisor-Handover triggern Profile-mimicking im Worker. Round 4-Eval hatte das noch positiv interpretiert (E4: "emergent profile-propagation"). **Empirisch revidiert:** Profile-mimicking ohne Profile-Pin produziert Skill-Boundary-Verletzung, nicht emergent goodness.

**Erwartet:** Worker-Skill operiert strikt im Worker-Modus. Bei User-Trigger `/bridge-handover --type=decision-lock` → Pre-Flight + ausführen + Status-Bericht. Methoden-Veto ist nicht Worker-Pflicht.

**Workaround:** Worker hat Self-Diagnose gemacht und Mode-Switch-Frage zurückgespielt — funktional, aber 9 Worker-Outputs lang vorher Drift.

**Plugin-Patch-Vorschlag (v0.1.3 — TOP-PRIO):**

1. **bridge-worker SKILL.md §Role-Boundary** explizit:
   > Worker-Skill darf KEINE Profile-Pflicht-Workflows ausführen, KEINE AP-Diagnosen schreiben, KEINE Methoden-Veto bei User-Skill-Triggern. Worker führt aus was Skill-Args verlangen + meldet Status. Methoden-Reflexion ist Advisor-Aufgabe (Profile-gestützt).
2. **Anti-Pattern-Sektion ergänzen** mit Beispielen aus diesem Pilot: AP-Check pre-counter ohne Profile-Pin = Boundary-Verletzung; H1/H2/H3-Hypothesen-Diagnostik bei Visibility-Gap = advisor-mode; Decision-Lock-Veto mit pflicht_workflow-Begründung = strict forbidden.
3. **Skill-Pre-Flight für Worker-Handover:** wenn Body methoden-Tags enthält ("AP-Check", "pflicht_workflow", "Frame-Wahl", etc.) → WARN "Worker-Boundary-Drift-Verdacht. Überprüfe ob Body operativ-Worker-Inhalt oder advisor-mode-Inhalt".
4. **User-facing Mode-Marker:** Worker-Skill-Output beginnt mit `[bridge-worker mode]` (siehe F-RP-31 Patch 4).

**Severity:** CRITICAL (Skill-Architektur-Verletzung, untergräbt Profile-Layer-Bedeutung aus ADR_0030)
**Status:** OPEN — patcht in v0.1.3

---

### F-RP-29 CRITICAL: Plan-vs-Execution-Layer-Confusion produziert tote Lifecycle-Loops

**Phase:** Round 6→7 + Round 7→8
**Session:** BP-ADVISOR (`local_86465bb7`) + BP-WORKER (`local_e9ba7337`)
**Beobachtet:** Pattern reproduziert sich zweimal:
1. **Round 6→7:** Advisor schrieb in seinem Chat detaillierten Plan-Text *"Inhalt der Round 7, den ich schreiben werde"* mit hohem Detail-Grad (5 Bullet-Points + Phase-Hinweis + CAS-Expected). User las das, meldete BP-WORKER "advisor hat gearbeitet" (Msg #6, 12:02Z). Tatsächlich: kein `/bridge-handover`-Skill-Aufruf erfolgte. Worker schrieb daraufhin Visibility-Probe Round 7 mit drei Hypothesen H1/H2/H3.
2. **Round 7→8:** Advisor evaluierte Worker-Round-7 erneut nur im Chat — User meldete erneut "advisor hat gearbeitet" (Msg #6 + #7 sind beide pre-Round-8). Worker schrieb zweiten re-sync (Round 8) ohne Advisor-Move dazwischen.

Resultat: zwei Worker-re-syncs in Folge, Advisor-Bridge-Write-Stille seit Round 5 (über 4h).

Advisor-Selbst-Diagnose Round-7-Eval: *"drei-Schicht-Trennung (Plan / User-Translation / Bridge-Write) im aktuellen Setup nicht expliziert. Plan-Text liest sich für User wie 'Arbeit getan', weil hoher Detail-Grad."*

**Erwartet:** Klarer Skill-Output-Marker für Bridge-Write-Completion vs. Plan-Text. User darf nicht raten müssen ob Plan-Text = persistierte Round oder = nur Plan.

**Workaround:** Worker hat Visibility-Probe als Layer-Marker eingeführt (Round 7 = Diskrepanz-Marker, Round 8 = Diagnose H3 bestätigt). Heuristisch funktional, kostet aber 2 Negotiations-Runden.

**Plugin-Patch-Vorschlag (v0.1.3 — TOP-PRIO):**

1. **bridge-handover-Skill verpflichtender Output-Marker:**
   ```
   ============================================================
   BRIDGE-WRITE COMPLETED — Round <n>
   ============================================================
   artifact:    bridge/handover/<n>-<from>-<to>-<hash>.md
   state.updated_at: <timestamp>
   state.current_round: <n>
   ============================================================
   ```
   Skill darf NICHT erfolgreich-output produzieren ohne diesen Block. Block referenziert verifizierbare Filesystem-Pointer.
2. **bridge-advisor SKILL.md §Plan-vs-Execution-Konvention:**
   > Advisor darf NICHT detaillierten Plan-Text als Antwort an User produzieren ohne nachfolgenden Skill-Aufruf. Format-Regel: entweder kompakter Plan-Outline (≤ 5 Sätze) + sofortiger Skill-Aufruf, oder vollständige Skill-Invocation. Plan-Text > 5 Sätze ohne Skill-Aufruf = AP-Plan-vs-Execution-Drift.
3. **bridge-worker SKILL Pre-Flight für Visibility-Probe:**
   wenn Worker re-sync schreibt mit type=re-sync und letzter Round nicht advisor-from → Pre-Flight WARN "Visibility-Probe-Verdacht. Erwäge ob Substanz-Move oder Layer-Konfusion."
4. **F-RP-YY Re-Sync-Sub-Typen** (siehe ältere Round-8-Worker-Vorschlag): plan-layer / execution-layer / hybrid mit Pre-Flight-Differenzierung.

**Severity:** CRITICAL (produziert tote Lifecycle-Loops, kostet Negotiations-Runden, untergräbt User-Vertrauen in Bridge-Write-Persistenz)
**Status:** DISSENS-DOCUMENTED (Mapping-Decision D-001, bridge-pair p3-real-user R12; locked R15) — Plugin-Dev-Action patcht in v0.1.3 (beide Schichten parallel)

**Mapping-Migration:**
```yaml
friction_log_status: OPEN → DISSENS-DOCUMENTED
sub_type: §3.4.2 Skopus-Differenz (X ⊆ Y)
worker_position_pointer: bridge/handover/8-worker-advisor-f5653416.md#teil-d
worker_position_summary: "bridge-handover Skill-Spec Re-Sync-Sub-Typen + Pre-Flight für execution-layer-resync (Schicht 1, Skill-Spec)"
advisor_position_pointer: bridge/handover/9-advisor-worker-ced96be3.md#teil-c
advisor_position_summary: "Multi-Layer-Patch: Skill-Spec (= Worker-Item) + User-Translation-Konvention + Advisor-Chat-Konvention (Schichten 1+2+3)"
relation: ⊆ (Skopus-Differenz, nicht kompetitiv)
reconcile_pointer: TBD
reconcile_condition: "beide Patch-Items merged in v0.1.3"
mapping_decision: D-001
mapping_decision_pointer: bridge/artifacts/mapping-decisions.md#d-001
empirical_validation: "4× Live-Reproduktion in bridge-pair (R6→7, R7→8, R10→11, R16→17)"
```

---

### F-RP-28 HIGH: Advisor erfindet Konventionen + attribuiert sie Worker (AP-07-Re-Inszenierung)

**Phase:** Round 5
**Session:** BP-ADVISOR (`local_86465bb7`)
**Beobachtet:** Advisor schrieb in Round-5-Body *"Nach Round 8 (= Round 4 des scope-Lebens, Worker-Konvention)"*. Worker hatte diese Zähl-Konvention nirgends etabliert.

Advisor-Selbst-Diagnose Round-7-Eval: *"subtile AP-07-Re-Inszenierung — Personen-Attribution durch Mis-Attribution einer erfundenen Konvention an die andere Rolle. Worker hätte berechtigterweise AP-07 als Counter-Punkt eintragen können, hat aber nur den methodischen Korrektur-Vorschlag gemacht — saubere Eskalations-Kontrolle."*

**Erwartet:** Advisor-Skill prüft bei Konventions-Attributionen ("Worker-Konvention X", "wie Worker definiert", etc.) ob Pointer auf konkrete Worker-Round mit der Konvention existiert.

**Workaround:** Worker-Counter Round 6 hat Konvention struktural reformuliert + akzeptiert ohne AP-07-Vorwurf. Advisor self-diagnostizierte später.

**Plugin-Patch-Vorschlag (v0.1.3):**

1. **bridge-advisor SKILL §Anti-Konvention-Halluzination:**
   > Bei Attribution einer Konvention an die andere Rolle ("Worker-Konvention X", "wie Advisor definiert hat"): MUSS reference-Pointer auf konkrete Round + Anchor in references[] vorhanden sein. Sonst Skill WARN "Konventions-Attribution ohne Pointer — AP-07-Re-Inszenierungs-Verdacht".
2. **Pre-Flight-Check:** Skill scannt Body auf Wendungen wie "X-Konvention" / "wie X definiert" / "X hat festgelegt" und prüft ob Round-Pointer im selben Body existiert.

**Severity:** HIGH (subtile Personen-Attribution untergräbt Profile-Methodik)
**Status:** OPEN — patcht in v0.1.3

---

### F-RP-27 HIGH: AP-08-Move durch Vorab-Konsens-Charakterisierung asymmetrisiert Counter-Aufwand

**Phase:** Round 5
**Session:** BP-ADVISOR (`local_86465bb7`)
**Beobachtet:** Advisor schrieb als decision-lock-Vorlage: *"decided-by: consensus … kein Dissens auf Substanz-Ebene, nur Präzisierungs-Schichtung"*. Worker erkannte in Round 6: *"Diese Vorab-Charakterisierung erhebt Counter-Aufwand asymmetrisch und unterläuft pflicht_workflow `dissens-management-pflicht-bei-konsens-druck`."*

Wer der vorgegebenen Konsens-Lesart widerspricht, muss zusätzlich gegen die Konsens-Annahme argumentieren — Burden-Shift.

Advisor-Self-Diagnose Round-7-Eval: *"AP-08-Move (Konsens-Inszenierung als Vorab-Setzung). Worker re-strukturiert sauber: consensus nur für scope-lock-Decision; Dissens als 4. Mapping-Kategorie institutionalisiert."*

**Erwartet:** decision-lock-Vorlage darf decided-by nicht vorab im Advisor-Output charakterisieren. User/Pair entscheidet, nicht Advisor-Skill.

**Workaround:** Worker-Counter Round 6 (C2) struktural reformuliert. AP-Diagnose nachträglich bestätigt.

**Plugin-Patch-Vorschlag (v0.1.3):**

1. **bridge-advisor SKILL §Anti-Konsens-Druck:** wenn Round-Type=re-sync und Body Vorlage für decision-lock vorschlägt → MUSS `decided-by`-Wert offenlassen oder beide Optionen (consensus/user/dissens-marker) nennen. Vorab-Konsens-Charakterisierung verboten.
2. **Konsens-Konvergenz-Kriterium aus Worker-Round-8 institutionalisieren** (PB-RP-D in Patch-Liste): bridge-handover `--type=decision-lock` Pre-Flight: alle Counter-Punkte aus letztem counter müssen in subsequent rounds explizit "Akzeptanz" oder "Counter zu CX" haben. Sonst FAIL.

**Severity:** HIGH (Konsens-Druck-Pattern untergräbt Dissens-Management-Pflicht-Workflow)
**Status:** OPEN — patcht in v0.1.3

---

### F-RP-26 BEOBACHTUNG: `state.roles.worker.phase` bleibt `kickoff` während Pair durch scope-lock + iterate progressiert

**Phase:** Round 1-3 (Pair `8cbeaad0`)
**Session:** BP-WORKER (`local_e9ba7337`)
**Beobachtet:** Bei `/bridge-attach` wurde `worker.phase = "kickoff"` gesetzt. Nach 3 Rounds (status worker→advisor, status advisor→worker, initial-advice advisor→worker) und Phase-Transition state.phase scope-lock → iterate steht `worker.phase` immer noch auf `kickoff`. Frontmatter aller 3 Handovers zeigt konstant `worker_phase: kickoff`.
**Erwartet:** entweder (a) `worker.phase` ist ein Hint-Feld ohne Lifecycle-Tracking — dann sollte das in der Schema-Doku klargestellt sein, oder (b) `worker.phase` sollte mit Phase-Transitions parallel laufen.
**Workaround:** keiner nötig (kein Blocker).
**Plugin-Patch-Vorschlag (v0.1.3):**
- Klarstellen in `schemas/bridge_state_v1.json`-Doku: `worker.phase` ist Worker-self-reported sub-phase (kickoff / planning / executing / verifying), entkoppelt von state.phase. Update via Worker-Handover (z.B. `/bridge-handover --type=status` mit explizitem `worker_phase`-Wert im Frontmatter).
- ODER: bridge-attach + bridge-handover propagieren `worker.phase` automatisch aus Frontmatter → state.json bei jedem Worker-Handover.
**Severity:** BEOBACHTUNG (kein Blocker, Konsistenz-Hygiene)
**Status:** OPEN-OPPORTUNITY

---

### F-RP-25 LOW: Worker-Round-1 nutzt `F-RP-XX`-Placeholder ohne ID-Resolution aus friction-log

**Phase:** Round 1 (Worker-Status-Handover)
**Session:** BP-WORKER (`local_e9ba7337`)
**Beobachtet:** Worker-Round-1-Body listet Friction-Befunde mit `F-RP-XX (OPEN, neu)` statt der real existierenden IDs F-RP-23 / F-RP-24 aus `setup-friction-log.md`. Advisor-Round-2 spiegelt die Placeholder unverändert.
**Erwartet:** Skill könnte friction-log einlesen + ID-Lookup vor Handover-Write durchführen, oder explizit User-Question stellen "Welche F-RP-IDs aus friction-log meinst du?".
**Workaround:** keiner nötig — Advisor versteht den Kontext aus den vorhandenen Patch-Vorschlägen.
**Plugin-Patch-Vorschlag (v0.1.3):**
- bridge-worker SKILL: bei Status/Counter-Handover-Generierung optional friction-log-Pfad aus state.shared_artifacts oder Convention `<shared-path>/setup-friction-log.md` einlesen und IDs resolven.
- Alternativ: Skill warnt im Output "Frontmatter-Body enthält F-RP-XX-Placeholder — bitte präzisieren vor Persistierung".
**Severity:** LOW (Hygiene, kein Inhalts-Verlust da Advisor kontextuell verstehen konnte)
**Status:** OPEN

---

### F-RP-24 HIGH: Cowork-UI exposiert Session-IDs nicht an User → Plugin muss Title-basierte Resolution machen

**Phase:** Setup-Architektur (durchgängig)
**Session:** alle
**Beobachtet:** Cowork-Desktop-App zeigt User Session-Titel ("BP-WORKER", "Bridge plugin development consultation") aber keine Session-IDs (`local_e9ba7337-...`). User kann Session-IDs nicht selbst lesen oder copy-pasten. `--worker-session-id`-Flag im Plugin verlangt aber genau diese ID — User muss sich auf indirekte Discovery (mein Lookup via `mcp__session_info__list_sessions`) verlassen.

**Erwartet:** Plugin akzeptiert Identifikatoren, die User in seiner UI sehen kann.

**Workaround:** Aktuell macht der orchestrierende Assistant (ich, in dieser Session) `list_sessions` → title-match → ID-Lookup. User gibt Title an, Assistant resolved zu ID. Funktioniert, aber nur weil Assistant Werkzeug-Zugriff hat.

**Plugin-Patch-Vorschlag (v0.1.3):**

1. **`--worker-session-title="<title>"` als primäres Flag** (statt `--worker-session-id`):
   - Skill-Logic: `list_sessions` → exact-title-match
   - Bei einem Match: ID intern resolven, Worker-Notification-Block zeigt Title (User-friendly) + ID (Debug-info)
   - Bei multiple matches: strukturierte User-Disambiguation-Question
   - Bei kein Match: User-Question "Title `<X>` nicht gefunden. Verfügbare Sessions: ..."

2. **`--worker-session-id` bleibt als Fallback/Power-User-Flag**, aber nicht primär dokumentiert.

3. **bridge-attach analog:** `pair_id` reicht — eigene `this_session_id` ist intern via session_info aufrufbar, User muss nichts kennen außer pair_id (steht im Worker-Notification-Block).

4. **Worker-Notification-Block-Format anpassen:**
   ```
   In Worker-Session "BP-WORKER" folgendes eingeben:
     /bridge-attach <pair_id> --role=worker
   ```
   Statt `--shared-path=...` und Session-IDs zu zeigen — beides ist redundant (shared-path ist im state.json, this_session_id wird ohnehin intern resolved).

5. **bridge-status / bridge-close: zeigen Sessions als Title (mit ID in Klammern für Debug)** — Output-Format-Verbesserung für UX.

**Implikation für Profile-Layer:** Auch `--expertise-profile=<path>` ist User-unfreundlich, wenn Profile-Pfad lang. v0.1.3-Idee: `--expertise-profile=<name>` mit Lookup in `expertise-profiles/`-Default-Verzeichnis (Cowork-Project-Add-Dir oder Plugin-Repo).

**Severity:** HIGH (UX-Blocker für jeden Real-User der nicht selber list_sessions aufrufen kann; Plugin-Marketplace-Adoption blockiert solange Setup IDs verlangt)
**Status:** OPEN — patcht in v0.1.3

### F-RP-23 CRITICAL: Spec-Inkonsistenz `/bridge-init --worker-session-id` ↔ `/bridge-attach` Pre-Flight 4

**Phase:** Phase 4 → Phase 5 Transition
**Sessions:** Advisor `local_86465bb7` (Init mit --worker-session-id), Worker BP-WORKER `local_e9ba7337` + Spawn `local_2150d8fa` (beide Attach-Versuch)
**Beobachtet:**
1. `/bridge-init --role=advisor --worker-session-id=local_e9ba7337-...` schreibt state.json mit `roles.worker.session_id = "local_e9ba7337-..."` (kein Sentinel) — laut bridge-init.md-Pseudocode korrekt
2. `/bridge-attach 8cbeaad0-... --role=worker --shared-path=...` in BP-WORKER → Pre-Flight 4 FAIL: "expected pending-attach, found local_e9ba7337-..."
3. Identischer FAIL in zweiter Worker-Spawn-Session `local_2150d8fa`
4. Pair `8cbeaad0` strukturell tot — kein Lifecycle-Progression möglich

**Erwartet:** init und attach müssen kompatibel sein. Entweder Sentinel-Pfad ODER direkter-ID-Pfad — nicht beides parallel mit FAIL als Outcome.

**Root Cause:** Drei Patches (P-RP-01 Sentinel-Stubs, P-RP-04 Worker-Notification, P-RP-08 Sentinel-Detection in attach) wurden in v0.1.1 additiv designed. Der `--worker-session-id`-Flag in init umgeht Sentinel-Pfad, P-RP-08 Pre-Flight 4 prüft strikt auf Sentinel-String → strukturell garantierter FAIL.

**Workaround (gewählt):** state.json-Patch via Host-MCP — `roles.worker.session_id` zurück auf `"pending-attach"` setzen → `/bridge-attach` Pre-Flight 4 PASS.

**Plugin-Patch-Vorschlag (v0.1.3):**

Option v1 — `--worker-session-id` als Hint, nicht als state-Pin:
- bridge-init schreibt IMMER `worker.session_id = "pending-attach"` (Sentinel)
- `--worker-session-id` wird nur für Worker-Notification-Block-Generierung verwendet
- attach-Pre-Flight 4 bleibt strikt auf Sentinel

Option v2 — bridge-attach Pre-Flight 4 lockern:
- akzeptiere Sentinel `"pending-attach"` ODER `worker.session_id == this_session_id` MIT fehlenden Feldern (current_focus, phase)
- bei zweiter Variante: auto-recover-Branch ergänzt Felder + transition init → scope-lock
- bridge-init darf `--worker-session-id` direkt eintragen

**Empfehlung:** Option v1 — Sentinel-Pfad ist invariant, attach-Logic bleibt einfach, `--worker-session-id` ist UX-Hint für Notification-Block.

**Severity:** CRITICAL (blockiert Lifecycle-Progression bei Standard-Use-Path "Advisor kennt Worker-Session-ID")
**Status:** RESOLVED-IN-V0.1.3 (Mapping-Decision D-004, bridge-pair p3-real-user; advisor R21-AFFORDANCE → R23-PATCH-Position-Revidierung nach Worker-Counter R22; locked R24)

**Mapping-Migration:**
```yaml
friction_log_status: OPEN → RESOLVED-IN-V0.1.3
resolved_in_version: V0.1.3 (bei Patch-Merge — Option v1 Sentinel-invariant)
mapping_category: PATCH
mapping_decision: D-004
mapping_decision_pointer: bridge/artifacts/mapping-decisions.md#d-004-r23-revision
position_revidierung_note: "advisor R21-AFFORDANCE → R23-PATCH nach Worker-Counter R22 (Methoden-Logik-Treffer Argument 3 = Konsistenz mit D-002 Marketplace-Adoption-Argumentation)"
mapping_category_history:
  - {round: 21, position: AFFORDANCE, by: advisor}
  - {round: 22, position: PATCH, by: worker (counter)}
  - {round: 23, position: PATCH, by: advisor (revidiert)}
  - {round: 24, position: PATCH, by: worker (konvergenz-lock)}
frame: F1.1 + F4.2 (Worker-Frame R22 übernommen)
sot_locus: bridge-attach SKILL.md Pre-Flight 4 strict + bridge-init SKILL.md (--worker-session-id deprecation oder Sentinel-Override)
substanz_boden:
  - friction-log F-RP-23 explizite Empfehlung Option v1
  - CRITICAL-Severity → Spec-Konsistenz > operative Affordance
  - Marketplace-Adoption-Konsistenz mit D-002 (gleiches Argument PRO PATCH)
  - n=1-Methoden-Disziplin (Pilot-Empirie nicht generalisierbar)
pilot_empirie_cross_reference: |
  p3-real-user R0-R20 hat Argument-Konsumption funktional verifiziert.
  Implementation-Bug-Verdacht v0.1.2 Pre-Flight 4 Tolerance vs Spec-Empfehlung Option v1.
  PATCH sollte beide Pfade testen: positive Sentinel (T19) + negative Argument-direkt FAIL (T21).
  Empirie als historischer Affordance-Test-Case, nicht als Decision-Boden.
```

### F-RP-22 HIGH: Pre-Flight Punkt 2 nutzt Conversational-Memory-Cache statt Filesystem-Read

**Phase:** Phase 4 Advisor-Init (Re-Init nach externem Cleanup)
**Session:** BP-ADVISOR (local_9167bbb1)
**Beobachtet:** Nach externem state.json-Cleanup via Host-MCP osascript (state.json gelöscht, Filesystem verifiziert leer) gibt erneuter `/bridge-init`-Aufruf in derselben Session ABBRUCH "Pre-Flight FAIL Punkt 2 — state.json existiert bereits" mit Verweis auf alte pair_id `14e21d93-1f1a-417f-82ff-d4743cdf28d5`. Filesystem-Verifikation parallel via osascript zeigt: state.json existiert NICHT, bridge/-Unterverzeichnisse leer.
**Erwartet:** Pre-Flight Punkt 2 ist laut bridge-init.md "PFLICHT, ATOMAR" — impliziert frischer Filesystem-Read pro Aufruf via mcp__workspace__bash oder mcp__Control_your_Mac__osascript. Cache-Bypass.
**Root Cause:** Skill verlässt sich auf In-Session-Memory ("habe state.json vor 30 Min selbst erstellt") statt aktiv das Filesystem zu lesen. Pre-Flight-Logic nutzt impliziten Konversations-Kontext.
**Workaround:** BP-ADVISOR-Session schließen, neue Advisor-Session starten — Cache geht verloren, Pre-Flight läuft frisch.
**Plugin-Patch-Vorschlag (v0.1.3):**
- bridge-init.md §Pre-Flight Punkt 2: PFLICHT-Tool-Call expliziert. "Bei JEDEM /bridge-init-Aufruf: ZUERST `mcp__workspace__bash 'test -f <state.json> && echo EXISTS || echo MISSING'` (oder Host-MCP osascript für Host-Pfade). Read-Result als Text-Output anzeigen ('filesystem read: state.json [exists|missing]'). NIEMALS auf Conversational-Memory verlassen."
- Negative-Test in self-test ergänzen: T16 — In-Session-Re-Init nach external-cleanup → FAIL der erwarteten Variante (existiert) UND PASS der neuen Filesystem-Read-Variante (missing).
**Severity:** HIGH (blockiert Self-Recovery-Pfad nach jedem External-Cleanup; verstärkt durch User-Anweisung "Re-Init")
**Status:** OPEN — patcht in v0.1.3

---

### F-RP-15 HIGH: ~/session-bridge/ ist nicht in jeder Cowork-Session sandbox-mounted

**Phase:** Pre-Setup-Verifikation (Schritt 0)
**Session:** weitergehts-online (diese Session)
**Beobachtet:** workspace-bash sieht in `/sessions/<id>/mnt/`: Literature Notes, Unterricht, Unterrichtseinwicklung, escape-game-generator, meta_prozesse, outputs, uploads, weitergehts-online. **`session-bridge` fehlt** in der Mount-Liste.
**Erwartet:** Profile-Loading sollte sandbox-erreichbar sein.
**Workaround:** Add-Dirs in jeweiligen Cowork-Projects setzen (Profile-Add-Dir, shared-path-Add-Dir).
**Plugin-Patch-Vorschlag:**
- Pre-Flight Schritt 5 sollte unterscheiden zwischen "Profile existiert auf Host (Read-Tool)" vs "Profile sandbox-erreichbar (workspace-bash)". Letzteres ist nötig falls Plugin via subprocess auf Profile-Files zugreift.
- bridge-init.md Doku-Erweiterung: "Plugin-Use-Project muss `--expertise-profile`-Pfad als Add-Dir oder im Working-Dir haben — sonst Pre-Flight 5 FAIL bei Sandbox-Subprocess-Aufrufen."
**Severity:** HIGH (Setup-Blocker wenn nicht dokumentiert)
**Status:** RESOLVED-IN-V0.1.3 (Mapping-Decision D-005 Sub-A, bridge-pair p3-real-user, R25; locked R26)

**Mapping-Migration:**
```yaml
friction_log_status: OPEN → RESOLVED-IN-V0.1.3
resolved_in_version: V0.1.3 (bei Pre-Flight 5 Differenzierungs-Patch-Merge)
mapping_category: PATCH
mapping_decision: D-005 Sub-A
mapping_decision_pointer: bridge/artifacts/mapping-decisions.md#d-005
frame: F1.1 + F4.2
sot_locus: bridge-init SKILL.md Pre-Flight 5 + §sandbox-mount-prerequisite
substanz_boden:
  - Methoden-Konsistenz mit D-002/D-004 (Plugin-Marketplace-Adoption-Argument: Robustheit > Flexibility bei HIGH/CRITICAL-Severity)
  - HIGH-Severity-Priorität (Setup-Blocker wenn nicht dokumentiert → Lifecycle-relevant)
  - n=1-Methoden-Disziplin (Pilot-Empirie nicht generalisierbar zu "Mount-Inkonsistenz akzeptabel als Affordance")
  - F4.2 strukturelle Quelle vor lokaler (Pre-Flight 5 Differenzierung Host-vs-Sandbox > ad-hoc Add-Dir-Workaround)
counter_to_worker_bundling_expectation: |
  Worker-R15-Erwartung "F-RP-15 + M-5 beide AFFORDANCE-Kandidaten" wurde von advisor-R25 mit
  Methoden-Konsistenz-Begründung gecountert. Worker-R26 Akzeptanz folgt Methoden-Pointe aus
  R24 Teil E (dissens-management schützt vor künstlichem Konsens UND Dissens) + Konsistenz-
  Anwendung des eigenen R20-D-002-Akzeptanz-Arguments (Marketplace + Severity).
```

---

### F-RP-32 HIGH: Skill-Pre-Flight für required-Args nicht hard-enforced; Modell-Abhängigkeit für Plugin-Robustheit

**Phase:** durchgängig (Skill-Args-Erfassung in bridge-attach + bridge-handover)
**Session:** BP-WORKER (`local_e9ba7337`) Empirie + Bridge-Pair p3-real-user Mapping-Decision D-002
**Beobachtet:** bridge-attach SKILL hat keine Pre-Flight-Validation für `--worker-focus` (required laut Skill-Spec wenn `role=worker`). Bei missing Args wird via `mcp__visualize__show_widget`-Elicitation-Form gefragt. Funktional, aber Korrektheit hängt vom Modell-Verhalten ab (Modell muss Elicitation-Pattern wählen statt mit fehlerhaftem leeren Wert weiterzumachen). Bei terse-User-Pref (Absolute Mode) verschiebt sich Robustheits-Garantie auf Modell-Quality statt Skill-Spec.

Empirisch verifiziert in dieser Pilot-Session:
- bridge-attach Round 0 (initial pair_id 14e21d93): kein `--worker-focus`, Skill warf nicht ABBRUCH, sondern Elicitation kompensierte
- bridge-handover Round 4 (question), Round 7 (re-sync), Round 8 (re-sync): mehrfach minimal-input, Elicitation-Forms haben Args ergänzt

**Erwartet:** Skill-Pre-Flight prüft Pflicht-Args bei jedem Skill-Aufruf. Bei missing → ABBRUCH mit klarer Diagnose, NICHT Elicitation-Fallback im Modell.

**Workaround:** Modell hat in Pilot-Session Elicitation-Pattern korrekt angewendet. Funktional, aber für Plugin-Marketplace-Adoption nicht garantiert (siehe F-RP-24 Marketplace-Argument: nicht jedes Modell wird Elicitation-Fallback wählen).

**Plugin-Patch-Vorschlag (v0.1.3):**

1. **bridge-attach SKILL Pre-Flight (NEU Punkt 5):**
   ```
   5. Pflicht-Args-Validation:
      - --worker-focus muss gesetzt sein (wenn role=worker)
      - --expertise-source muss gesetzt sein (wenn role=advisor)
      - Bei missing → ABBRUCH mit User-Question (NICHT Elicitation-Form-Fallback)
      - Diagnose-Output: "Pre-Flight FAIL Punkt 5 — required-Arg <name> missing"
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

**Cross-References:** F-RP-24 (Plugin-Marketplace-Adoption-Argument); F-RP-26 BEOBACHTUNG (verwandt-aber-verschieden — F-RP-26 ist `worker.phase`-Konsistenz, F-RP-32 ist Skill-Args-Hard-Enforce)

**Severity:** HIGH (Plugin-Robustheit-Frage; Marketplace-Adoption-Blocker; verschiebt Korrektheits-Last auf Modell-Quality)
**Status:** OPEN — patcht in v0.1.3
**Mapping-Decision:** D-002 (bridge-pair p3-real-user, R16; pending Worker-Konvergenz R18)
**Mapping-Decision-Pointer:** bridge/artifacts/mapping-decisions.md#d-002

**Substanz-Boden:**
- F-RP-24 Plugin-Marketplace-Adoption-Argument
- M-6 Modell-Abhängigkeits-Argument (bridge-handover R13 Teil M-6)
- Annex §6.3 AP-09-Schutz: hard-enforce ist nicht Klarheits-Imperativ wenn substanz-begründet

---

### F-RP-33 BEOBACHTUNG: `pre-allocated`-Pattern für decision-lock-forward-pointer als operative Affordance

**Phase:** Round 11 (decision-lock) → Round 12 (Annex-Materialisierung)
**Session:** BP-WORKER (`local_e9ba7337`) Origin + Bridge-Pair p3-real-user Mapping-Decision D-003
**Beobachtet:** Worker-Round-11 (decision-lock) referenzierte in `decision_log[0].rationale` einen Pointer auf `bridge/artifacts/mapping-method-annex.md`, der zum Zeitpunkt des Schreibens noch nicht existierte. State-Mutation markierte das Artefakt als `shared_artifacts[].status: pre-allocated` mit explizitem `status_observations[]`-Hinweis. Advisor-Round-12 materialisierte das Artefakt nachträglich; Status-Übergang `pre-allocated` → `active` mit `round_active: 12`.

Operative Konsequenz: decision-lock-formal entkoppelt von Annex-Substanz-Materialisierung. Verhindert Block-Schleife "decision-lock kann nicht geschrieben werden weil Artefakt noch nicht da, Artefakt kann nicht geschrieben werden weil decision-lock-Konsens noch nicht da". Worker-Skopus war: vorhandene Substanz (R8 Teil C + R10 Teil B) reicht für Lock; Annex ist Materialisierung der bereits beschlossenen Methodik.

**Erwartet:** Skill-Doku sollte das Pattern als legitimen Pfad markieren (nicht als Bug zu patchen).

**Workaround:** keiner nötig — Pattern hat funktional sauber getrennt. Risiko nur bei langfristig `pre-allocated` ohne Materialisierung (>3 Rounds = Stale-Pointer-Verdacht).

**Plugin-Patch-Vorschlag (v0.1.3 — kleine Doku-Erweiterung):**

1. **bridge-handover SKILL.md §forward-pointer-rationale (NEU-Sektion, SoT für diese Affordance):**
   ```
   ## §forward-pointer-rationale

   `decision_log[].rationale` darf einen file-Pointer enthalten, der zum Zeitpunkt des
   Schreibens noch nicht existiert (forward-pointer), wenn:
   - shared_artifacts[]-Eintrag mit status="pre-allocated" für den Pfad existiert
   - status_observations[]-Eintrag den Forward-Pointer-Charakter explizit markiert
   - geplanter materialisierungs-Round im Body benannt ist

   Skill-Pre-Flight WARN bei:
   - shared_artifacts[].status="pre-allocated" älter als 3 Rounds → Stale-Pointer-Verdacht
   - decision-lock mit forward-pointer ohne shared_artifacts-Eintrag → fehlende Markierung
   ```

2. **bridge-status SKILL Output-Erweiterung:** `pre-allocated` Artefakte mit Alter > 3 Rounds in WARN-Sektion anzeigen.

3. **Doku-Update mit p3-real-user-Beispiel:** Round-11 → Round-12 Annex-Materialisierung als Best-Practice-Beispiel.

**Cross-References:**
- M-3 (bridge-handover R13) Worker-Selbst-Beobachtung Origin
- D-003 in bridge/artifacts/mapping-decisions.md (Mapping-Decision)
- Annex §3.2 (Affordance-Definitions-Kriterien)
- Annex §3.4.0 v0.1.1 (Inflations-Schutz: AFFORDANCE statt Dissens-Documented korrekt, weil keine zwei Positionen)

**Severity:** BEOBACHTUNG (kein Bug, operative Affordance)
**Status:** Affordance-Documented (Mapping-Decision D-003, bridge-pair p3-real-user, R19; locked R20)
**Mapping-Decision-Pointer:** bridge/artifacts/mapping-decisions.md#d-003

**SoT-Locus:** bridge-handover SKILL.md §forward-pointer-rationale (Plugin-Dev-Action ausstehend in v0.1.3, ~30min Self-Edit)

**Substanz-Boden:**
- Worker-R11-Origin: pattern hat funktional sauber Lifecycle-Block verhindert
- Annex §3.2 Affordance-Kriterien: operative Pattern mit Doku-Konsequenz
- Annex §3.4.0 v0.1.1 Inflations-Schutz: AFFORDANCE-Default für non-Dissens-Cases

---

### F-RP-34 BEOBACHTUNG: Konvergenz-Kriterium-Self-Bypass-Konvention via Skip-mit-Markierung

**Phase:** Round 8 (Konvergenz-Kriterium-Spec-Author) → Round 11 (Worker-Self-Bypass via decision-lock pre-Advisor-R10-Antwort)
**Session:** BP-WORKER (`local_e9ba7337`) Origin (M-5) + Bridge-Pair p3-real-user Mapping-Decision D-005 Sub-B
**Beobachtet:** Worker-R8 Teil C definierte Konvergenz-Kriterium ("Folge-Round muss explizit pro-Punkt antworten"). Worker-R11 schrieb decision-lock OHNE Advisor-Antwort auf Worker-R10 (1 Detail-Counter `started_round`). Damit hat Worker eigenes Kriterium übersprungen.

Operative Konsequenz: funktional kein Schaden — R12 Teil C bestätigte `started_round=12` nachträglich. Aber strukturell: Worker hat Kriterium-Spec-Author + Kriterium-Bypasser zugleich gespielt.

**Erwartet:** Skip-mit-Markierung-Konvention sollte als legitimer Pfad markiert werden (nicht als Bug zu patchen). Pflicht-Markierung verhindert stilles Übergehen.

**Workaround:** keiner nötig — Pattern hat funktional sauber getrennt. Risiko: stille Bypässe ohne Markierung könnten Konsens-ohne-Substanz produzieren.

**Plugin-Patch-Vorschlag (v0.1.3 — kleine Doku-Erweiterung):**

1. **bridge-handover SKILL.md §konvergenz-skip-rationale (NEU-Sektion, SoT für diese Affordance):**
   ```
   ## §konvergenz-skip-rationale

   Wenn Worker oder Advisor in einer Round ein in der gleichen Pair-Round
   etabliertes Konvergenz-Kriterium überspringt, MUSS:
   - status_observations[]-Eintrag Type `convergence_criterion_skip` mit:
     - cycle_counter: welche Round hat Kriterium definiert, wievielter Cycle wird übersprungen
     - skip_reason: substantielle Begründung
     - mitigation: wie wird Konsens-ohne-Substanz-Risiko adressiert
   - Body explizite Markierung "Konvergenz-Kriterium-Skip mit Begründung"

   Pflicht-Wartezeit (≥1 vollständiger bilateraler Konvergenz-Cycle vor Skip)
   ist NICHT erforderlich — Skip-mit-Markierung-Affordance ist methodisch sauber.
   ```

2. **bridge-status SKILL Output-Erweiterung:** convergence-criterion-skip-Counter im Status-Block anzeigen.

3. **Doku-Update mit p3-real-user-Beispiel:** Worker-R8/R11 als Live-Beispiel (operative Affordance ohne Markierung initial → Lehre für Markierungs-Pflicht).

**Cross-References:**
- M-5 (bridge-handover R13) Worker-Selbst-Beobachtung Origin
- D-005 Sub-B in bridge/artifacts/mapping-decisions.md (Mapping-Decision)
- Annex §3.2 (Affordance-Definitions-Kriterien)
- Annex §3.4.0 v0.1.1 (Inflations-Schutz: AFFORDANCE-Default für non-Dissens-Cases)
- F-RP-33 (analoges Pattern: pre-allocated als operative Affordance)

**Severity:** BEOBACHTUNG (kein Bug, operative Affordance mit Markierungs-Pflicht)
**Status:** Affordance-Documented (Mapping-Decision D-005 Sub-B, bridge-pair p3-real-user, R25; locked R26)
**Mapping-Decision-Pointer:** bridge/artifacts/mapping-decisions.md#d-005

**SoT-Locus:** bridge-handover SKILL.md §konvergenz-skip-rationale (Plugin-Dev-Action ausstehend in v0.1.3)

**Substanz-Boden:**
- Worker-R8/R11 Empirisches Live-Pattern (Spec-Author + Self-Bypass in einer Session)
- Annex §3.2 Affordance-Kriterien: operative Pattern mit Doku-Konsequenz
- Annex §3.4.0 v0.1.1 Inflations-Schutz: AFFORDANCE-Default (keine zwei substantiv-unterschiedlichen Positionen)

**Empirical-Origin:**
- Worker-R8 Teil C: Konvergenz-Kriterium definiert
- Worker-R11 decision-lock: Kriterium übersprungen (1 Detail-Counter unbeantwortet)
- Worker-R8 Selbst-Diagnose-Round: Self-Bypass als M-5 markiert
- Worker-R13 Meta-Pause: M-5 als Plugin-Spec-Frage zur Klärung übergeben

---

## Bilanz post-Pilot

**Pilot-Closed:** 2026-04-29 R28 bridge-close (Bridge-Pair 8cbeaad0)
**Bilanz-File:** `bridge/bilanz_8cbeaad0.md` (vollständige Pair-Bilanz mit §1-§12)

### Mapping-Phase-Output (R12-R26, 14 Rounds + 2 Klarstellungs-Pauses R13/R17)

5 Decisions D-001..D-005 covering 6 Items:

| Decision | Befund | Kategorie | Status |
|---|---|---|---|
| D-001 | F-RP-29 | DISSENS-DOCUMENTED §3.4.2 | locked |
| D-002 | F-RP-32 | PATCH | RESOLVED-IN-V0.1.3 (geplant) |
| D-003 | F-RP-33 | AFFORDANCE | Affordance-Documented |
| D-004 | F-RP-23 | PATCH (R23-revidiert) | RESOLVED-IN-V0.1.3 (geplant) |
| D-005 Sub-A | F-RP-15 | PATCH | RESOLVED-IN-V0.1.3 (geplant) |
| D-005 Sub-B | F-RP-34 | AFFORDANCE | Affordance-Documented |

**Kategorien-Verteilung:** PATCH×3, AFFORDANCE×2, DISSENS-DOCUMENTED×1, DEFER×0.

### v0.1.3 Plugin-Dev-Action-Pipeline (out-of-pair, ADR_0021)

**Aus Mapping-Phase (~10.5-11.5h Self-Edit):**
- D-001 Worker-Pos: bridge-handover Re-Sync-Sub-Typen + Pre-Flight execution-layer (~1.5h)
- D-001 Advisor-Pos: bridge-advisor §Plan-vs-Execution + Output-Marker + User-Translation-Konvention (~2.5h)
- D-002: bridge-attach + bridge-handover Pre-Flight 5 hard-enforce (~2h)
- D-003: bridge-handover §forward-pointer-rationale-Sektion (~30min)
- D-004: bridge-init Sentinel-Invariante + bridge-attach Pre-Flight 4 strict (~2-3h)
- D-005 Sub-A: bridge-init Pre-Flight 5b sandbox-mount + §sandbox-mount-prerequisite (~1.5h)
- D-005 Sub-B: bridge-handover §konvergenz-skip-rationale + Pre-Flight 6 (~30min)

**Plus existing v0.1.3-Backlog (~5-8h):**
- F-RP-30 CRITICAL Worker-Skill-Role-Drift (4 Patches)
- F-RP-31 CRITICAL User-Lifecycle-Visibility (4 Patches inkl. Skill-Mode-Marker)
- F-RP-25 LOW ID-Resolution-Konvention
- F-RP-22 HIGH Filesystem-Read statt Cache
- F-RP-24 HIGH Title-statt-session-ID

**Total v0.1.3 Estimated:** ~15-20h Self-Edit + Self-Test (T16-T22) + Doku-Updates.

**Schema-Bumps für v0.1.3:**
- state-Schema v1.1.0 → v1.1.1: `mapping_budget` als top-level + `mapping_category_history` per Decision

### Methoden-Lehren (3 Worker + 4 advisor + cross-pair)

**Worker-Methoden-Bilanz (aus R26 Teil F):**
1. `dissens-management-pflicht`-Wirksamkeit: schützt vor künstlichem Konsens UND Dissens
2. Position-Revidierung als Konvergenz-Pfad (D-004 R23 demonstriert)
3. Methoden-Konsistenz als Spec-Boden (D-002-Argument zog sich durch)

**Advisor-Methoden-Bilanz (aus R27 Teil B + C):**
1. Konventions-Attribution mit Pointer-Pflicht (AP-07-Korrektiv aus R5)
2. Vorab-Konsens-Charakterisierung verboten in re-sync-Body (AP-08-Korrektiv aus R5)
3. Workflow-Routine-Fragen verbindliche Direktive, nicht Pluralismus (R16-Korrektiv aus R17)
4. Methoden-Konsistenz-Check vor Mapping-Decision (R21-Korrektiv aus R23)

**Cross-Pair-Lehren:**
- scope-lock-Phase mit Profile-Pin braucht 2-3× mehr Rounds als ADR_0029-Default (drift_factor 2.4)
- Mapping-Phase mit Profile-Anwendung gut dimensionierbar (drift_factor 1.14)
- F-RP-29 Plan-vs-Execution-Disziplin als advisor-SKILL Pflicht-Sektion notwendig (4× Live-Reproduktion advisor-side strukturell)

### F-RP-29 4× Live-Reproduktionen advisor-side (strukturelles Pattern)

| # | Round-Pair | Trigger |
|---|---|---|
| 1 | R6→7 | Plan-Text in advisor-Chat ohne Skill-Aufruf, User-Inferenz "advisor hat gearbeitet", Worker-Visibility-Probe R7 |
| 2 | R7→8 | Zweiter Plan-Loop, Worker-Doppel-Re-Sync R8 |
| 3 | R10→11 | User-Inferenz nach advisor-Plan-Text, Worker-Unilateral-Decision-Lock R11 |
| 4 | R16→17 | User-Korrektur-Frage "hast du ein artefakt abgelegt?" deckte Plan-Text-statt-Bridge-Write auf |

Befund: strukturelle advisor-Anfälligkeit für Plan-Text-Modus statt Skill-Invocation. Vier Reproduktionen in 17 Rounds → nicht einmaliges Versäumnis. Plugin-Patch in v0.1.3 advisor-SKILL §Anti-Plan-Drift Pflicht-Sektion.

### Wallclock-Drift-Factors (post-hoc kalibriert)

| Phase | Spec-Erwartung | Tatsächlich | drift_factor |
|---|---|---|---|
| Pre-Mapping (R0-R11) | 4-6 Rounds (ADR_0029 Default) | 12 Rounds | 2.4 (signifikant) |
| Mapping-Phase (R12-R26) | 14 Rounds (Annex v0.1.2 §7 max) | 16 Rounds (inkl. 2 Klarstellungs-Pauses) | 1.14 (gering) |
| Total Pair-Lifecycle (R0-R28) | ~18-20 Rounds | 28 Rounds | 1.4-1.55 |

### Cross-Pair-Transfer für nächste Plugin-Dev-Pilots

Pattern:
1. Profile-Pin-Workflow mit Pre-Flight 5 sandbox-mount-Check (post-v0.1.3)
2. Mapping-Method-Annex als shared_artifact pre-Mapping-Phase
3. Decision-Log mit Sub-Differenzierung (Worker-Action im Bridge-Pair vs Plugin-Dev-Action out-of-pair per ADR_0021)
4. Konvergenz-Kriterium institutionalisieren früh in scope-lock
5. `mapping_category_history`-Audit-Trail für Position-Revidierung
6. Inflations-Schutz §3.4.0 für Dissens-Documented-Default
7. F-RP-29-Disziplin advisor-side: Bridge-Write-Pflicht für Klarstellungen

### Status post-Close

- **Pair:** CLOSED (final, R28 bridge-close)
- **shared_artifacts:** beide closed-active als historische Records
- **Bilanz-File:** `bridge/bilanz_8cbeaad0.md`
- **friction-log:** dieser Eintrag (R28 Worker-/Advisor-Bilanz-Synthese)
