# Changelog

All notable changes to session-bridge are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) — Semver pinned per ADR_0029 §13.1.

---

## [0.1.15] — 2026-05-15 — 7. Expertise-Profile: claude-plugin-dev (konstruktiv-prospektiv) + 4. Sub-Agent

### Added

- **expertise-profiles/claude-plugin-dev/** (NEU v0.1.15, 7. Profile — privat in private-notes/):
  - **Konstruktiv-prospektives** Plugin-Development-Profile — Twin zu architecture-archaeology (gleiche Methodik-Familie Brooks/Parnas/Conway + LLM-Forschung, gegensätzliche Zeitrichtung: BAUEN vs AUDITIEREN)
  - 7 Methodik-Säulen: spec-first / trigger-praezision / token-budget-bewusst / empirie-driven / schema-disziplin / cowork-mode-reading-pattern-bewusst / inkrementell-versioniert
  - 6 Files (PROFILE + diagnostic-frames + anti-patterns + question-bank + workflows + **plugin-dev-patterns.md** als 6. File, profile_schema_version 1.1.0)
  - 10 Frames in 5 Cluster: C1 Plugin-Struktur / C2 Trigger-Engineering / C3 Token-Architektur / C4 Schema-Disziplin / C5 Empirie-Iteration — je mit session-bridge-Empirie-Sektion
  - 10 Anti-Patterns AP-D01..D10 mit Selbstanwendungs-Pflicht (AP-D10 Empirie-Ignoranz konstitutiv enforced)
  - ~50 Diagnose-Fragen + 5 Empirie-Pflicht-Fragen als Pre-Check vor jeder Iterations-Empfehlung
  - 7 Workflows (6 Standard hybrid Multi-/Single-Pass + W-D-Empirie-Pflicht-Pre-Check)
  - plugin-dev-patterns.md: PSP/TEP/TAP/SDP/RP je ≥5 Patterns + Cowork-vs-Claude-Code-Differenzen + session-bridge-Empirie-Reference (15 Versionen als Best-Practice-Case) + Anti-PDP + Recursive-Self-Audit
  - Quellen-Sockel: Anthropic Plugin-/Agent-SDK-/MCP-/Cowork-Doku + Brooks/Parnas/Conway + ReAct/Reflexion/Toolformer/Voyager/MRKL + Semver + Keep a Changelog
- **agents/claude-plugin-dev-berater.md** (NEU v0.1.15, 4. Sub-Agent):
  - Sub-Agent-Dispatch-Zugriff auf claude-plugin-dev-Profile für **Einzelsession-Nutzung ohne bridge-pairing** (vom User benannter Primär-Use-Case)
  - Twin-Differenzierung zu architecture-archaeology explizit (prospektiv-konstruktiv vs retrospektiv-diagnostisch)
  - Empirie-Pflicht-Pre-Check (5 Fragen) im Output-Format Pflicht — AP-D10-Schutz
  - Recursive-Self-Audit-Klausel bei Beratung über session-bridge selbst
- **plugin.json agents-Array** erweitert auf 4 Sub-Agents
- **bridge-advisor SKILL.md §Profile-Activation-Decision-Tree** erweitert (claude-plugin-dev-Row für prospektiv-konstruktive Plugin-Dev-Use-Cases)
- **tools/bridge_state.py + tools/profile_frame_lookup.py** PROFILE_SHORT_NAMES erweitert: `arch`/`architecture` (zuvor in bridge_state.py fehlend) + `plugin-dev`/`claude-plugin-dev`
- **commands/bridge-init.md** Kurz-Name-Mapping erweitert + profile_schema_version-Support-Hinweis korrigiert (1.0.0 + 1.1.0)
- **docs/adr/ADR_0030 Annex D.6** PROFILE_SHORT_NAMES-Beispiel synchronisiert
- **tests/smoke_self_test.py** T84-T85 erweitert (4 Agents, version-agnostischer Dispatch-Marker) + T88 NEU (claude-plugin-dev Reference-Profile skip-if-private) + T89 NEU (claude-plugin-dev-berater Sub-Agent)

### Methodische Architektur

Profile-Familie wächst auf **7 Profile** mit klarer Twin-Struktur:

| Profile | Methodik-Familie | Zeitrichtung |
|---|---|---|
| **claude-plugin-dev** | Software-Engineering + LLM-Forschung | **prospektiv-konstruktiv** (Plugin BAUEN) |
| architecture-archaeology | Software-Engineering + LLM-Forschung + Hermeneutik | retrospektiv-diagnostisch (Plugin AUDITIEREN) |
| klafki / adorno / foucault / luhmann / process-consulting | Bildungs-/Sozial-Theorie | je nach Profile |

claude-plugin-dev adressiert den vom User benannten Bedarf: Profile werden häufig in Einzelsessions ohne bridge-pairing genutzt — der Sub-Agent macht das Profile ohne Pair-Setup zugänglich (~1-2k Tokens statt ~18000 Profile-Pin).

### Verification

- Profile-Struktur-Self-Test 104/104 PASS
- Plugin Smoke-Test 92/92 PASS (T1-T87 + T88 + T89 NEU, erweiterte T84+T85)
- Schema unverändert (profile_schema_version 1.1.0 bereits seit v0.1.7 supported)
- Backward-Compat: v0.1.14-Pairs unverändert funktional; PROFILE_SHORT_NAMES rein additiv

---

## [0.1.14] — 2026-05-12 — 3. Sub-Agent: instructional-design-berater (US-ID-Tradition komplementär zu klafki-advisor)

### Added

- **agents/instructional-design-berater.md** (NEU v0.1.14, 3. Pilot-Agent):
  - US-Instructional-Design-Tradition (kognitivistisch, empirisch, prozessual)
  - 7 Methodik-Säulen: ADDIE / Mager-Quartett + Bloom Revised / CLT (Sweller) + Multimedia Principles (Mayer) / Evidenz-basiert (Hattie) / Gagné Nine Events / Iterativ-evaluativ / Tradition-bewusst
  - Quellen-Sockel: Mager 1997, Gagné 1985, Bloom/Anderson/Krathwohl 1956/2001, Sweller 1988, Mayer 2009, Merrill 2002, Reigeluth 1979, Dick/Carey/Carey 2014, Carroll 1990, Hattie 2009
  - **Methodik-Tradition-Differenz zu klafki-advisor explizit**: ID fragt "wie effektiv lernen?", Klafki fragt "wozu Bildung?"
  - Komplementaritäts-Tabelle für 6 Anliegen-Typen (Lernziel/Material/Sequenzierung — operational vs bildungstheoretisch)
  - Worker-vs-Advisor-Bias-Pattern (Worker operational, Advisor methodisch-reflektierend)
  - Klafki-Tradition-Differenz im Output-Format Pflicht
- **plugin.json agents-Array** erweitert auf 3 Pilot-Agents
- **bridge-advisor SKILL.md §Sub-Agent-Dispatch-Pattern** Tabelle erweitert (3 Sub-Agents statt 2)
- **docs/adr/ADR_0030 Annex F.2** Pilot-Agents-Tabelle erweitert
- **tests/smoke_self_test.py** T84-T85 erweitert (3 Agents) + T87 NEU (ID-Berater Klafki-Differenz + Quellen-Sockel)

### Methodische Architektur

Sub-Agent-Trio bildet **methodische Familien-Differenzierung**:

| Sub-Agent | Tradition | Frage-Typ | Wann |
|---|---|---|---|
| klafki-advisor | deutsche Didaktik (geisteswissenschaftlich, normativ, bildungstheoretisch) | "wozu Bildung?" | Bildungsgehalt / Mündigkeit / Schlüsselproblem |
| **instructional-design-berater** | **US-ID (kognitivistisch, empirisch, operational)** | **"wie effektiv lernen?"** | **Lernziel-Operationalisierung / Material-Design / Assessment** |
| projektentwicklungs-advisor | PM/Agile (operational, prozessual) | "wie umsetzen?" | Track-Decomposition / Sprint / Critical-Path |

Beide Lehr-/Lern-Sub-Agents (Klafki + ID) sind **komplementär nicht-konkurrierend**:
- Klafki: bildungstheoretische Reflexion über Mündigkeits-Anschluss
- ID: operationale Spec via Mager-Quartett + Bloom + Mayer-Principles
- advisor kann beide nacheinander dispatchen + Synthese in handover

### Verification

- Self-Test 91/91 PASS (T1-T86 + T87 NEU, plus erweiterte T84+T85)
- Schema unverändert
- Backward-Compat: v0.1.13-Pairs unverändert funktional

### Cross-Use-Case Differenzierung

User-Hypothese: bei Bildungs-Use-Cases werden Klafki + ID **gemeinsam** sinnvoll:
- ID-Sub-Agent für operationale Lernziel-Spec
- Klafki-Sub-Agent für bildungstheoretische Reflexion + Mündigkeits-Anschluss
- advisor synthetisiert beide Antworten

Empirie: Mager-Quartett ist bereits in unterrichtsplanung-core verankert (Cross-Use-Case-Anker).

### Deferred to v0.2.0+

- Voll-Roll-out alle 6 Profile als Sub-Agents (Trigger: 3-5 Pairs Sub-Agent-Empirie positiv)
- 2-4 weitere Worker-Sub-Agents
- Multi-Sub-Agent-Coordination-Skill (Lead-Agent + Worker-Agents Pattern)
- Auto-Trigger via Pattern-Erkennung

---

## [0.1.13] — 2026-05-12 — Profile-Sub-Agent-Pattern Pilot (Option C): 2 Sub-Agents + Decision-Tree

### Source: User-Vorschlag aktive Sub-Agent-Dispatch zusätzlich zu v0.1.11 passive Lookup

v0.1.11 B-Plus Lookup wurde in p12/p13/p14 nicht aktiv genutzt. p13 macht Cross-Profile-Bildungs-Audits manuell. User-Bedarf: aktive Sub-Agent-Beratung mit präzisen Fragen + integrierten Antworten. Standard-Multi-Agent-Pattern aus LLM-Research (MRKL/ReAct/AutoGen/CrewAI/LangGraph/Voyager/Anthropic-Multi-Agent).

### Added

- **agents/klafki-advisor.md** (NEU v0.1.13, Theoretiker-Pilot):
  - Bildungstheoretische Sub-Agent-Antworten auf Basis Klafki 1958/1963/1985/1996
  - Pflicht-Profile-Pre-Read (4 Klafki-Profile-Files)
  - 5 Methodik-Säulen + 5 Frame-Cluster + Anti-Antwort-Klausel
  - Methodische-Konsistenz-Hinweis-Pflicht im Output
  - Tools: Read, Glob, Grep
- **agents/projektentwicklungs-advisor.md** (NEU v0.1.13, Worker-Pilot):
  - Operative Sub-Agent-Beratung (Track-Decomposition / Sprint-Priorisierung / Acceptance-Criteria / Risk-Mitigation)
  - 5 Methodik-Säulen aus PMBOK + Agile/Scrum + Brooks + Lehman + Cohn INVEST
  - Worker-Bias-Pattern empirisch dokumentiert (p7-praxis/p11/p12/p13)
  - Tools: Read, Glob, Grep, Bash
- **plugin.json `agents`-Array** mit 2 Pilot-Agents
- **bridge-advisor SKILL.md §Sub-Agent-Dispatch-Pattern** (NEU v0.1.13):
  - Decision-Tree: Lookup (B-Plus v0.1.11) vs Sub-Agent-Dispatch (v0.1.13)
  - Output-Pflicht-Format §Sub-Agent-Dispatch im handover
  - Anti-Pattern-Liste (Akkumulation / Antwort-ungekürzt-übernehmen / Methodische-Konsistenz-Hinweis-Skip)
- **bridge-worker SKILL.md §Worker-Sub-Agent-Pattern** (NEU v0.1.13):
  - Primärer Worker-Use-Case projektentwicklungs-advisor
  - Worker-Bias-Pattern dokumentiert (operativ vs evaluativ)
  - Worker-Authority bleibt final (Sub-Agent ist Vorschlag)
- **docs/adr/ADR_0030 Annex F** (NEU 2026-05-12):
  - F.1 Problem (v0.1.11 nicht aktiv genutzt)
  - F.2 Decision (Option C Pilot mit 2 Agents)
  - F.3 Decision-Tree Lookup vs Sub-Agent-Dispatch
  - F.4 Agent-Markdown-Format
  - F.5 Worker- vs Advisor-Sub-Agent-Bias-Pattern
  - F.6 Methodische-Konsistenz-Marker (Pflicht)
  - F.7 Anti-Pattern für Sub-Agent-Dispatch
  - F.8 Cynefin-Klassifikation (Pilot-Mitigation Complex-Risk)
  - F.9 Schema-Auswirkungen (KEINE)
  - F.10 Forschungs-Bezüge (MRKL/ReAct/AutoGen/CrewAI/LangGraph/Voyager/Anthropic)
  - F.11 v0.2.0 Roll-out-Plan (deferred bis Empirie)
- **tests/smoke_self_test.py** T84-T86 NEU:
  - T84: agents/ Verzeichnis + plugin.json agents-Array
  - T85: Agent-Markdown Frontmatter + Methodische-Konsistenz-Marker
  - T86: SKILL.md §Sub-Agent-Dispatch + §Worker-Sub-Agent + ADR_0030 Annex F

### Verification

- Self-Test 89/89 PASS (T1-T83 + T84-T86 NEU)
- Schema unverändert (kein Bump)
- Backward-Compat: v0.1.12-Pairs unverändert funktional

### Use-Case-Beispiel

```
[advisor-session, architecture-archaeology primär]
advisor benötigt Klafki-Einschätzung zu Bildungsgehalt-Frage X
→ Agent(subagent_type="session-bridge:klafki-advisor",
        prompt="Wie würde Klafki Bildungsgehalt-Hypothese X bewerten?")
→ klafki-advisor lädt Klafki-Profile, antwortet methodisch-konsistent (~1-2k Tokens)
→ advisor integriert in handover mit §Sub-Agent-Dispatch-Marker
```

```
[worker-session]
worker benötigt Track-Decomposition für 8 Sub-Tracks
→ Agent(subagent_type="session-bridge:projektentwicklungs-advisor",
        prompt="Track-β in Sub-Tracks aufteilen, Critical-Path identifizieren")
→ projektentwicklungs-advisor antwortet mit Plan + Trade-offs + ACs + Risks
→ worker integriert in handover mit §Worker-Sub-Agent-Dispatch-Marker
```

### Worker- vs Advisor-Bias (empirisch dokumentiert)

| Session-Rolle | Bias | Use-Cases |
|---|---|---|
| Worker | operative Sub-Agents | Track-Decomposition / Sprint-Priorisierung / Acceptance-Criteria / Dependency-Analyse / Risk-Mitigation |
| Advisor | theoretische Sub-Agents | Klafki / Adorno / Foucault / Luhmann / process / arch — methodische Distanz |

Methodisch konsistent zur Rollen-Differenzierung (Worker operativ, Advisor evaluativ).

### Decision-Tree: 3 Mechaniken komplementär

| Mechanik | Wann | Token-Cost |
|---|---|---|
| **Profile-Pin** (`/bridge-init --expertise-profile=`) | voll-Methodik über Pair-Lifecycle | ~18000 Tokens |
| **B-Plus Lookup** (v0.1.11) | punktuelle Frame-Text-Retrieval | ~500-1500 Tokens |
| **Sub-Agent-Dispatch** (v0.1.13 NEU) | aktive methodische Beratung | ~1-2k Tokens Antwort |

### Backward-Compatibility

- v0.1.12-Pairs funktionieren unverändert
- agents/ additive Plugin-Erweiterung
- ADR_0030 D5 Single-Profile-Pinning vollständig erhalten
- Kein Schema-Bump

### Deferred to v0.2.0+

- Voll-Roll-out alle 6 Profile als Sub-Agents (Trigger: 3-5 Pairs B-Plus + Sub-Agent-Pilot-Empirie positiv)
- 2-4 weitere Worker-Sub-Agents (implementation-pattern / workflow-design / empirie-validation)
- Multi-Sub-Agent-Coordination-Skill (Lead-Agent + Worker-Agents Pattern)
- PB-004 Auto-Trigger-Hooks (auto-detect wann Sub-Agent vs manual-Dispatch)

---

## [0.1.12] — 2026-05-12 — Empirie-driven Patches Round 3: memory_symmetry_status-Init + DRIFT VALIDE + audit_anker + Profile-Activation-Decision-Tree

### Source: 3 neue Pairs seit v0.1.11 (p12-eg-r5-spec-patch / p13-track-beta / p14-design-track-recon)

p12 produzierte NEU Anti-Drift-#7 HTML-Inline-Comment-Audit-Anker-Pattern. p13 läuft mid-flight mit Cross-Profile-Bildungs-Audits (Klafki/Adorno/Freire/Foucault) manuell — direkter v0.1.11-Lookup-Use-Case nicht genutzt. p14 just-init. Plus Schema-Bug: `memory_symmetry_status` blieb unset in allen 3 Pairs trotz v0.1.10-Implementation. Plus Empirie: 0 Profile-Aktivierungen in p12/p13/p14 → Profile-Activation-Decision-Tree dokumentiert.

### Added

- **commands/bridge-init.md** memory_symmetry_status-Init bei Bridge-Init mit Default "pending" + schema_version-Bump 1.1.0 → 1.2.0
  - Empirie-Bug: p12/p13/p14 hatten memory_symmetry_status=unset (v0.1.10 hatte Field nur in bridge-close gesetzt)
- **tools/bridge_state.py DRIFT_RANGES["architecture-spec-patch"]** NEU VALIDE n=4 (p8 0.05 + p9 0.09 + p10 0.10 + p12 0.10):
  - Range {min:0.05, max:0.30, stddev:0.05}
- **tools/bridge_state.py TRACK_TYPE_DRIFT_EMPIRIE["spec-patch"]** auf n=5 (mit p10/p12 als zusätzliche Datapoints)
- **schemas/handover_frontmatter_v1.json audit_anker-Array-Field** (Pattern aus p12 Anti-Drift-#7):
  - Pflicht-Felder: anchor_id (Pattern ^[A-Z][0-9]?-[A-Za-z0-9_-]+$) + source_ref
  - Optional: patch_location + category (P0/P1/P2/P3/RISK/DEFERRED/INFO)
  - Kompatibel zu HTML-Inline-Comment-Pattern: <!-- Audit-Anker: P0-X / AUDIT_RECOMMENDATION §1 -->
- **bridge-advisor SKILL.md §Profile-Activation-Decision-Tree** (NEU v0.1.12):
  - 8 Topic-Klassen mit Profile-Empfehlung
  - Architecture-Patches: KEIN Profile (Empirie p8-p12 drift-effizient ohne Profile)
  - Bildungs-/Org-/Kultur-Use-Cases: Profile empfohlen
  - Plugin-Audit: architecture-archaeology empfohlen
  - Decision-Trigger-Frage bei /bridge-init wenn Topic nicht-eindeutig
- **tests/smoke_self_test.py** T80-T83 NEU:
  - T80: bridge-init memory_symmetry_status-Init + schema_version 1.2.0
  - T81: DRIFT_RANGES architecture-spec-patch VALIDE + TRACK_TYPE n=5
  - T82: handover_frontmatter audit_anker + Validation gegen Sample
  - T83: SKILL.md §Profile-Activation-Decision-Tree

### Changed

- **schema_version** in bridge-init-state-Initialisierung: 1.1.0 → 1.2.0 (v0.1.5 PB-007 hatte Schema bereits, aber bridge-init schrieb noch alten Wert)

### Verification

- Self-Test 86/86 PASS (T1-T79 + T80-T83 NEU)
- handover_frontmatter v1 audit_anker-Validation gegen Sample PASS
- DRIFT_RANGES Backward-Compat (architecture-spec-patch ist additive Erweiterung)

### Empirie-Befunde aus p12/p13/p14

- **0 Profile-Aktivierungen in 3 Pairs** → Profile-Layer ist Use-Case-spezifisch, nicht universal
- **memory_symmetry_status=unset in allen 3 Pairs** → v0.1.10-Bug (Field nur in bridge-close gesetzt) jetzt gefixt
- **HTML-Inline-Comment-Audit-Anker-Pattern** (p12 Anti-Drift-#7) → strukturierte Variante als handover-Frontmatter-Field
- **DRIFT-Konvergenz architecture-spec-patch** n=4 konsistent 0.05-0.10 → HYPOTHESE→VALIDE Promotion

### Methodische Schlüssel-Erkenntnis

Profile-Layer ist **Use-Case-spezifisch erfolgreich**:
- ✓ Bildungs-/Org-/Kultur-Diskurs (p7-klafki validiert 8 Rounds, 9 DLs)
- ✗ Plugin-Self-Spec-Patches (p8/p9/p10/p12 alle Profile-frei drift-effizient)

Plugin differenziert jetzt via Decision-Tree statt Profile als universal-anwendbar zu suggerieren.

### Backward-Compatibility

- v0.1.11-Pairs unverändert funktional
- audit_anker-Field optional in handover-Frontmatter (additive)
- DRIFT_RANGES["architecture-spec-patch"] ist NEU (kein Override existierender Werte)
- schema_version bridge-init-Update 1.1.0 → 1.2.0 ist Bug-Fix (v0.1.5 hatte Schema bereits)

### Deferred to v0.1.13+

- Phase-Gate-Audit-Output-Format-Compliance-Check (klärung wie validiert: schema-pre-validation oder post-hoc check)
- ADR_0029 Annex F Cross-Pair-Empirie post-v0.1.11 (kann mit nächstem Patch)
- Long-Pair-WARN (p6 Empirie n=1 noch zu schwach)
- Auto-Lookup-Trigger via Pattern-Erkennung (architecture-archaeology-Use-Cases)

---

## [0.1.11] — 2026-05-09 — Profile-Frame-Dispatch (Option B-Plus): Multi-Profile-Access via Lookup-Tool

### Source: User-Vorschlag Multi-Profile-Access innerhalb laufender advisor-Sessions

6-Profile-Familie produziert (klafki/adorno/foucault/luhmann/process/arch). User-Use-Cases sind häufig multi-domain — z.B. architecture-archaeology-Pair will Adorno-AP-A05 für Plugin-Marketing-Text-Diagnose. Aktueller Workflow: Profile-Wechsel via neuer Pair = ~36000 Tokens. Punktuelle Cross-Profile-Lookup ist Token-effizient (~500-1500 Tokens vs ~18000, 95%+ Einsparung).

### Decision: Option B-Plus (Profile-Frame-Dispatch)

3 Alternativen bewertet:
- A: Sub-Agent via Agent-Tool (verworfen: subagent_types fest, Skill-Inflation)
- **B-Plus: Frame-Dispatch (gewählt)** — Token-effizient + ADR_0030 D5-erhaltend
- C: Multi-Profile-Pair (deferred v0.2.0 — Schema-Bump)
- D: Cross-Pair-Bridge-of-Bridges (deferred PB-006)

### Added

- **tools/profile_frame_lookup.py** (NEU v0.1.11):
  - `lookup_frame(profile, frame_id)` — Frame ohne voll-Profile-Aktivierung
  - `lookup_ap(profile, ap_id)` — AP punktuell
  - `lookup_question(profile, frame_id, round_type)` — Fragen mit Filter
  - `lookup_workflow_pass(profile, workflow_id, pass_n)` — Workflow oder Pass
  - `list_available_profiles()` / `list_frames()` / `list_aps()` — Discovery
  - `lookup_token_cost_estimate()` — Cost-Aggregation
  - LRU-Cache (maxsize=64) per-Session
  - PROFILE_SHORT_NAMES + FILE_ALIASES (geteilt mit tools/bridge_state.py + ADR_0030 Annex C)
- **bridge-advisor SKILL.md §Profile-Frame-Dispatch-Pattern** (NEU v0.1.11):
  - Wann-Lookup-Tabelle (4 Anliegen-Typen)
  - Output-Format-Pflicht: §Cross-Profile-Lookup mit Methodische-Konsistenz-Hinweis
  - Anti-Pattern-Liste: Lookup-Akkumulation / Lookup-Ersatz-Methodik / Lookup-Anti-Kosmetik
- **docs/adr/ADR_0030 Annex E** (NEU 2026-05-09):
  - E.1 Problem-Beschreibung
  - E.2 Decision (B-Plus mit Optionen-Vergleich)
  - E.3 Lookup-API
  - E.4 D5-Konstanz erhalten
  - E.5 Methodische-Konsistenz-Marker (Pflicht)
  - E.6 Anti-Pattern für Cross-Profile-Lookup
  - E.7 Cynefin-Klassifikation (Complicated, konsistent zu Original-Architektur)
  - E.8 Schema-Auswirkungen (KEINE)
  - E.9 Forschungs-Bezüge (MRKL/ReAct/Voyager/Toolformer)
  - E.10 Future Work (deferred)
- **tests/smoke_self_test.py** T77-T79 NEU:
  - T77: profile_frame_lookup API + Konstanten + Aliase
  - T78: lookup-Funktionen mit Mock-Profile
  - T79: SKILL.md §Dispatch + ADR_0030 Annex E

### Changed

- **bridge-advisor SKILL.md** Cross-Refs erweitert (ADR_0030 Annex E + tools/profile_frame_lookup.py)

### Verification

- Self-Test 82/82 PASS (T1-T76 + T77-T79 NEU)
- Profile-Schema unverändert v1.1.0
- state-Schema unverändert v1.2.0
- ADR_0030 D5 Single-Profile-Pinning UNVERÄNDERT (Backward-Compat 100%)

### Empirie-Validation (Mock-Test)

- 2 Lookups (Klafki F1.1 + Adorno AP-A05) = 777 Tokens
- vs voll-Profile-Aktivierung ~18000 Tokens
- Einsparung: 95.7%

### Token-Efficiency-Patterns OP-1 / OP-4 manifestiert

Lookup-Tool ist konkrete Implementation der Optimierungs-Patterns aus architecture-archaeology/token-efficiency-patterns.md:
- OP-1 (Skill-Trigger-Phrase-Filter): Frame/AP-Lookup statt Profile-Eager-Loading
- OP-4 (Cross-Reference-als-Pointer): Lookup ist on-demand-Pointer-Resolution

### Backward-Compatibility

- ADR_0030 D5 Single-Profile-Pinning vollständig erhalten
- v0.1.10-Pairs unverändert funktional
- Lookup-Tool ist additive Erweiterung (opt-in via advisor-Skill-Anweisung)
- Kein Schema-Bump

### Forschungs-Bezüge

- MRKL (Karpas et al. 2022) — Modular Reasoning + Knowledge + Language Multi-Module-Composition
- ReAct (Yao et al. 2022) — Reasoning-then-Acting mit Tool-Selection
- Voyager (Wang et al. 2023) — Skill-Library mit task-relevant Skill-Loading
- Toolformer (Schick et al. 2023) — Self-Supervised Tool-Use
- Anthropic Multi-Agent-Pattern (B-Plus = abgeschwächte Variante: Lead-Agent + Lookup-Tool statt Sub-Agent-Spawn)

### Deferred to v0.2.0+

- Option C Multi-Profile-Pair (Trigger: 3-5 Pairs B-Plus-Empirie + User-Bedarf für vollständige Sekundär-Methodik)
- Option D Cross-Pair-Bridge-of-Bridges (PB-006: n≥10 Pairs Empirie)
- Auto-Lookup-Trigger via Pattern-Erkennung
- Cross-Profile-Konsistenz-Audit-Workflow

---

## [0.1.10] — 2026-05-09 — Empirie-driven Patches Round 2: Memory-Symmetrie + Cross-Project-Domain + Source-of-Truth-Lock + Track-Type-Tracking

### Source: 3 neue Pairs seit v0.1.9 (p10/p11/p12) + p6-BILANZ ausgewertet — Cross-Pair-Empirie-Konsolidierung Round 2

p10-phase1a-foundation-audit lieferte Pattern-#109 HYPOTHESE Drift-Korridor-Track-Typ + Iteration-Cycle-4-Round-Pattern. p11-eg-schsch-architektur-import als 1. Cross-Project-Bridge mit Source-of-Truth-Lock-Pattern + Anti-Drift-#6. p6-upp-eg-advice (56 Rounds, Long-Pair) konsolidiert Pattern-#103 Memory-Symmetrie als Pflicht-Workflow (n=4 mit p7-klafki/p10/p11).

### Added

- **commands/bridge-close.md §Memory-Symmetrie-Pflicht-Workflow** (NEU v0.1.10 / Pattern-#103, CRITICAL):
  - Memory-Plan-Generierung aus BILANZ-Substanz (2-4 Items pro Session)
  - §Memory-Symmetrie-Plan-Block in BILANZ.md (advisor + worker, komplementär)
  - state.json memory_symmetry_status-Tracking (pending|partial|complete|skipped)
  - Pre-Init-WARN bei nächstem Pair wenn vorheriger != complete
  - Cross-Project-Memory-Marker bei domain-hint=cross-project
  - Item-Klassifikation: feedback (Methodik) / project (Snapshot) / reference (Cross-Pair) / user
- **schemas/bridge_state_v1.json domain_hint-Enum erweitert** (v0.1.10):
  - NEU `cross-project` (Empirie p11)
  - NEU `architecture-spec-patch` (Empirie p8/p12)
  - NEU `use-case-with-profile` (jetzt explizit, vorher nur in DRIFT_RANGES)
- **schemas/bridge_state_v1.json memory_symmetry_status-Field** NEU
- **schemas/handover_frontmatter_v1.json source_of_truth_locked-Array** (NEU v0.1.10 / p11-R4-02):
  - Pflicht-Felder: ref + at_round
  - Optional: reason + drift_against
  - Anti-Drift-#6 Cross-Project-Konsistenz strukturell sichtbar
- **tools/bridge_state.py DRIFT_RANGES erweitert** (v0.1.10):
  - NEU `cross-project` {min:0.20, max:0.5, stddev:0.1} (p11 n=1, drift 0.27-0.41)
  - NEU `architecture-spec` {min:0.04, max:1.5, stddev:0.3} (p5/p7-quellen/p8/p10/p11 n=5)
- **tools/bridge_state.py RATIO_THRESHOLDS erweitert** (v0.1.10):
  - NEU `cross-project: 6.0` (p11-Empirie 11 Rounds für Cross-Project-Komplexität)
- **tools/bridge_state.py TRACK_TYPE_DRIFT_EMPIRIE-Konstante** (NEU v0.1.10 / Pattern-#109):
  - schema/doku/validator: HYPOTHESE n=1 mit Korridor [0.6, 1.4]
  - spec-patch: VALIDE n=4 (p4/p5/p7/p8/p9) mit Range [0.05, 0.5]
  - code: UNGETESTET n=0
  - Re-Klassifikations-Trigger HYPOTHESE→VALIDE: ≥3 diverse Datenpunkte pro Track-Typ
- **docs/adr/ADR_0029_Session_Bridge_Pattern.md Annex D** (NEU 2026-05-09):
  - D.1 Pair-Inventar p10/p11/p12
  - D.2 Pattern-#103 Memory-Symmetrie als Pflicht-Workflow
  - D.3 Cross-Project-Bridge als domain-Subtype
  - D.4 Source-of-Truth-Lock-Field-Justification
  - D.5 Pattern-#109 Track-Type-Differenzierung
  - D.6 Iteration-Cycle-4-Round-Pattern
  - D.7 Long-Pair-Pattern (deferred)
  - D.8 5. Tooling-Effizienz-Cycle
  - D.9 v0.1.10-Patches Tabelle
  - D.10 v0.1.11+ Deferred Patches
- **tests/smoke_self_test.py** T71-T75 NEU:
  - T71: bridge-close §Memory-Symmetrie-Pflicht-Workflow
  - T72: bridge_state_v1 cross-project + memory_symmetry_status
  - T73: handover_frontmatter source_of_truth_locked
  - T74: DRIFT_RANGES cross-project + TRACK_TYPE_DRIFT_EMPIRIE
  - T75: ADR_0029 Annex D

### Changed

- **DRIFT_RANGES["use-case-with-profile"]** Empirie-Markierung empirisch validiert (war v0.1.9 Hypothese, jetzt mit p7-klafki + p11 cross-validated)
- **schemas/bridge_state_v1.json** domain_hint-Enum-Erweiterung (additive, backward-compat — alte Pairs ohne neue Werte funktionieren weiter)

### Verification

- Self-Test 78/78 PASS (T1-T70 + T71-T75 NEU)
- schema_version unverändert v1.2.0 (additive Erweiterung im topic_metadata-Subschema + neues optional Field memory_symmetry_status)

### Backward-Compatibility

- v0.1.9-Pairs unverändert funktional
- Alte `domain_hint`-Werte (use-case, architecture-spec, etc.) bleiben gültig
- `memory_symmetry_status`-Field optional — alte state.json bleiben valid
- `source_of_truth_locked`-Field optional in handover-Frontmatter

### Empirisch-validiert

- Pattern-#103 Memory-Cross-Session-Symmetrie n=4 (p6/p7-klafki/p10/p11)
- Cross-Project-Bridge-Drift-Aufschlag ~+50% sup-Single (p11 vs p4-p10-Single-Project-Pairs)
- Iteration-Cycle-4-Round-Pattern (counter→decision-lock→iteration-cycle→verify) als Bridge-Best-Practice
- 5 Tooling-Effizienz-Pattern-Cycles (p4-p11) — methodisch verfestigt

### Deferred to v0.1.11+

- Long-Pair-WARN bei Round-Counter > 30 (p6 n=1)
- Mid-Pair-Memory-Snapshot-Pattern (Long-Pair-Folge)
- bilanz_v1.json cross_project_metadata-Field
- Konsensus-Lock vs Decision-Lock-Differenzierung
- AD.1A-Konstanten als Profile-Style-Header

---

## [0.1.9] — 2026-05-05 — Empirie-driven Patches: Phase-Gate-Audit + Cowork-Mode-Composition + DRIFT-Update + ADR_0029 Annex C

### Source: 5 Bridge-Pairs seit v0.1.7 (p6/p7-praxis/p7-klafki/p8/p9) — Cross-Pair-Empirie-Konsolidierung

p7-upp-praxis-validation lieferte 26 Findings + 14 Patterns + 16 NEU-Tracks. Davon 5 Patterns mit direkter Bridge-Plugin-Implikation: #76+#77+#80 (Cowork-Mode-Reading-Pattern), #82 (Lehrkraft-Realbedingungen-Validation, deferred), #88 (Phase-Gate-Audit), #89 (User-Veto-Authority). p7-klafki-validation produzierte empirische Validation der Profile-Pin-Mechanik (9 DLs in 8 Rounds, alle 6 Klafki-Frame-Cluster aktiviert). p8-self-sustained-ux drift 0.05 als Best-Performer mit L-p8-01-Pattern (Pre-Flight-Vorlage-Vollständigkeit) — methodische Validation von v0.1.8 Phase A.

### Added

- **bridge-advisor SKILL.md §Cowork-Mode-Composition-Pattern** (NEU v0.1.9 / Pattern-#76+#77+#80):
  - Reading-Pattern-Skill-Klärung: Skills sind Anleitungen, nicht Auto-Pipeline
  - Composition-Reihenfolge mit Phase-Gate-Audit-Schritt
- **bridge-advisor SKILL.md §Phase-Gate-Audit-Pflicht** (NEU v0.1.9 / Pattern-#88, CRITICAL):
  - Pflicht bei jedem handover (außer initial-advice + status)
  - 4-stufiger Phase-Gate-Audit: Phase-ID + Output-Inventar + Gate-Kriterien-Check + Audit-Verdikt
  - Output-Format-Pflicht: §Phase-Gate-Audit-Sektion mit Verdikt PASS/WARN/FAIL
  - Konsequenz: PASS → Beratung / WARN → Audit-Hinweis / FAIL → Klärungs-Anforderung statt Beratung
- **bridge-worker SKILL.md §Cowork-Mode-Composition-Pattern** (NEU v0.1.9):
  - Reading-Pattern-Skill-Klärung
  - Composition-Reihenfolge mit Phase-Gate-Pflicht + User-Veto-Anerkennung
- **bridge-worker SKILL.md §Phase-Gate-Pflicht-Spiegel-Klausel** (NEU v0.1.9):
  - Spiegel zu advisor §Phase-Gate-Audit-Pflicht
  - Worker MUSS Phase-Gate-Self-Audit vor Phase-Transition durchführen
- **bridge-worker SKILL.md §User-Veto-Authority** (NEU v0.1.9 / Pattern-#89):
  - User-Direktive ist Final-Authority über Worker-Iteration
  - Worker akzeptiert Verwurf ohne Diskurs-Schleife
  - Veto-Dokumentation im nächsten handover §User-Veto-Befund
- **tools/bridge_state.py DRIFT_RANGES["use-case"] empirisch updated** (v0.1.9):
  - Vorher: min=0.4/max=2.0/stddev=0.5 (Hypothese p4+p5+p6)
  - Nachher: min=0.05/max=2.0/stddev=0.4 (n=4 Empirie p4 0.10 + p5 0.21 + p7-praxis 0.23 + p8 0.05)
  - NEU `use-case-with-profile`-Range explizit (vorher nur in RATIO_THRESHOLDS)
  - default min=0.05 statt 0.5 (extreme-low aus p8 berücksichtigt)
- **tools/bridge_state.py RATIO_THRESHOLDS["use-case-with-profile"]** Empirie-Status updated:
  - Vorher: 5.0 (Hypothese, Empirie n=0)
  - Nachher: 5.0 (empirisch validiert, p7-klafki 1.1 DL/Round + p8 0.9 AC/Round)
- **docs/adr/ADR_0029_Session_Bridge_Pattern.md Annex C** (NEU 2026-05-05):
  - Cross-Pair-Empirie-Konsolidierung post-v0.1.8
  - C.1 Pair-Inventar (5 Pairs)
  - C.2 Drift-Faktor-Empirie (4 Tooling-Effizienz-Pattern-Cycles)
  - C.3 Profile-Pin-Empirie Klafki (alle 6 Frame-Cluster aktiviert)
  - C.4 Patterns mit Bridge-Plugin-Implikation
  - C.5 L-p8-01-Pattern als Validation v0.1.8 Phase A
  - C.6 Cross-Pair-Pause/Resume-Pattern (deferred v0.2.0)
  - C.7 v0.1.9-Patches Tabelle
  - C.8 v0.1.10+ Deferred Patches
- **tests/smoke_self_test.py** T68-T70 NEU:
  - T68: bridge-advisor §Phase-Gate-Audit + §Cowork-Mode-Composition
  - T69: bridge-worker §Phase-Gate-Spiegel + §User-Veto + §Cowork-Mode-Composition
  - T70: DRIFT_RANGES + ADR_0029 Annex C

### Changed

- **tools/bridge_state.py DRIFT_RANGES** struktur erweitert + Werte empirisch kalibriert
- **bridge-advisor + bridge-worker SKILL.md** Cross-Refs erweitert (Pattern-#76/#77/#80/#88/#89 + ADR_0029 Annex C)

### Verification

- Self-Test 73/73 PASS (T1-T67 + T68-T70 NEU)
- Profile-Schema unverändert v1.1.0
- state-Schema unverändert v1.2.0

### Backward-Compatibility

- v0.1.8-Pairs unverändert funktional
- DRIFT_RANGES-Update ist additive Empirie-Kalibrierung — bestehende Pairs werden gegen neuen Range geprüft, alte Pairs nicht migriert

### Empirisch-validiert

- Klafki-Profile-Pin-Mechanik (ADR_0030) funktioniert
- v0.1.8 Pre-Flight Phase A entspricht L-p8-01-Pattern (drift 0.05 Best-Performer)
- 4 Tooling-Effizienz-Pattern-Cycles als Bridge-Best-Practice

### Deferred to v0.1.10+

- user_veto_log-Schema-Field (Pattern-#89, braucht Empirie-Konsolidierung)
- Pause/Resume-state.phase-Enum (mit Multi-Pair-Topologie v0.2.0)
- user-validation-Round-Type NEU (Pattern-#82)
- bilanz_v1.json tooling-cycles-Field (additive Erweiterung)
- v0.1.8 Phase A Live-Test (User-Aktion erforderlich)

---

## [0.1.8] — 2026-05-01 — Pre-Flight Auto-Resolution + Profile-Short-Names + UX-Reibung-Reduktion

### Source: User-Wunsch nach reibungslosem Bridge-Pair-Setup für Live-Pilot

Plugin v0.1.7-Setup verlangte 8 manuelle Schritte (mkdir + 2× Folder-Mount + Session-ID-Lookup + Profile-Pfad-Mount + /bridge-init mit allen Flags + pair-id-Copy + /bridge-attach). Hochreibungs-Workflow blockiert spontane Plugin-Nutzung. v0.1.8 reduziert auf 3 Approve-Klicks + 1 Auswahl-Klick (~70% Reduktion).

### Added

- **commands/bridge-init.md** §Pre-Flight Phase A (NEU):
  - A.1 shared-path Auto-Generation via `resolve_shared_path_default(topic)` + `request_cowork_directory`-Mount
  - A.2 profile-path Mount-Request via `resolve_profile_path(arg)` + Short-Name-Lookup
  - A.3 worker-session-id Auto-Resolution via `mcp__session_info__list_sessions`
  - A.4 Vereinfachter Worker-Notification-Block (Auto-Resolved Path)
- **commands/bridge-attach.md** §Pre-Flight Phase A (NEU):
  - A.1 shared-path-Resolution aus paste
  - A.2 Mount-Request via `request_cowork_directory`
  - A.3 own-session-id Auto-Detect via Skill-Context
- **tools/bridge_state.py** v0.1.8 Pre-Flight-Helpers:
  - `resolve_shared_path_default(topic)` — Default-Pfad-Generator mit p<N>-<slug>-Pattern
  - `resolve_profile_path(arg)` — Short-Name + Glob + Absolute-Resolution
  - `_slugify_topic(topic)` — URL-safe Slug für Pfad-Namen
  - `_next_pilot_id(base_dir)` — Scan vorhandener p<N>-Folder
  - `PROFILE_SHORT_NAMES` Konstante: klafki/adorno/foucault/luhmann/process-consulting/process Aliases
  - `PROFILE_SEARCH_DIRS` Konstante: ~/session-bridge/private-notes/expertise-profiles + ~/session-bridge/expertise-profiles
- **docs/adr/ADR_0030_Expertise_Profile_Pattern.md Annex D** (NEU 2026-05-01) Pre-Flight-Auto-Resolution-Pattern
- **tests/smoke_self_test.py** T62-T67 NEU:
  - T62: bridge_state Pre-Flight-Helpers verfügbar + __all__-Export
  - T63: slugify + next_pilot_id + resolve_shared_path_default Logik
  - T64: resolve_profile_path Short-Names + Absolute + Not-Found
  - T65: bridge-init.md Pre-Flight Phase A dokumentiert
  - T66: bridge-attach.md Pre-Flight Phase A dokumentiert
  - T67: ADR_0030 Annex D dokumentiert

### Changed

- **tests/smoke_self_test.py** sys.path setup für tools/-Modul-Import
- **bridge-advisor SKILL.md** Cross-Refs erweitert (siehe v0.1.8-Patch-Hinweis)

### Verification

- Self-Test 70/70 PASS (T1-T61 + T62-T67 NEU)
- Backward-Compatibility: Wenn alle Args explizit + Mounts vorhanden → Phase A übersprungen, v0.1.7-Manual-Mode unverändert
- Profile-Schema-Version unverändert v1.1.0 (reine Skill-/Command-Erweiterung)

### Profile-Short-Names verfügbar

```
--expertise-profile=klafki   → klafki-didaktik
--expertise-profile=adorno   → adorno-halbbildung-kritik
--expertise-profile=foucault → foucault-genealogie
--expertise-profile=luhmann  → luhmann-erziehungssystem
--expertise-profile=process  → process-consulting
```

### User-Reibung-Reduktion

Vorher (v0.1.7, manuell):
1. shared-path-Pfad ausdenken + per Terminal mkdir
2. shared-path Folder-Mount in advisor-Session
3. shared-path Folder-Mount in worker-Session
4. Worker-Session-ID finden + abtippen
5. Profile-Pfad ausdenken + Mount
6. /bridge-init mit allen Flags
7. pair-id kopieren
8. /bridge-attach in Worker

Nachher (v0.1.8, Auto-Resolution):
1. /bridge-init --topic="..." --expertise-profile=klafki
   → 3× Approve-Dialog (shared-path-Mount, profile-Mount, list_sessions-Auto-Wahl)
2. /bridge-attach <pair-id> in Worker
   → 1× Approve-Dialog (shared-path-Mount)

### Voraussetzung für PB-004 (Auto-Trigger-Hooks)

Pre-Flight-Auto-Resolution ist Voraussetzung für PB-004 (DEFERRED-Phase-2). Wenn Bridge-Pair-Setup ein-Klick wird, werden Auto-Trigger-Hooks adoptierbar.

### Deferred to v0.1.9+

- PB-004 Auto-Trigger-Hooks
- PB-005 N-Pair-Topologie
- PB-006 Cross-Pair-Memory
- PB-008 4-Layer-Meta-Architecture
- Multi-Profile-Loading v0.2.0+

---

## [0.1.7] — 2026-04-30 — Multi-Pass-Workflow-Pattern + File-Aliase + Selbstkritik-Klausel-Enforcement

### Source: adorno-halbbildung-kritik-Profile-Aufbau (theoretisch-tiefe Profile-Klasse)

Klafki-/Luhmann-Profile sind systematisch — Single-Pass-Workflows aus v0.1.6 reichen. Adorno-Linie ist anti-systematisch (Negative Dialektik) und erfordert mehr-stufige Lese-Pässe (literal → konzeptuell-immanent → anti-identifikatorische-konstellation → meta-kritisch). Außerdem: Adorno-Profile-Begriffe ("Konstellations-Anker" statt "Frames", "Negative Diagnose-Fragen" statt "Question-Bank") brauchen File-Naming-Aliase.

### Added

- **bridge-advisor SKILL.md** §Schritt 0:
  - Multi-Pass-Workflow-Loading (passes optional in workflows.md)
  - File-Aliase-Mapping (konstellations-anker.md → diagnostic_frames, negative-diagnose-fragen.md → question_bank)
- **bridge-advisor SKILL.md** Anti-Pattern-Liste:
  - "NICHT Multi-Pass-Workflow-passes überspringen"
  - "NICHT Selbstkritik-Klauseln in Profile-Workflows ignorieren"
- **docs/adr/ADR_0030_Expertise_Profile_Pattern.md Annex C** (NEU 2026-04-30) Multi-Pass-Workflow-Pattern + File-Aliase + Selbstkritik-Klausel-Enforcement
- **tests/smoke_self_test.py** T57 + T58 + T59 NEU
  - T57: ADR_0030 Annex C Multi-Pass + File-Aliase dokumentiert
  - T58: SKILL.md Multi-Pass-Loading + File-Aliase + Selbstkritik-Enforcement
  - T59: adorno-halbbildung-kritik Reference-Profile vollständig (skip-if-private)

### Changed

- **profile_schema_version** 1.0.0 → 1.1.0 (additive Erweiterung, backward-compat — passes + Aliase + selbstkritik_klausel optional)
- **bridge-advisor SKILL.md** Cross-Refs erweitert um ADR_0030 Annex C + v0.1.7 SKILL-Patch-Hinweis

### Reference-Implementation

- `private-notes/expertise-profiles/adorno-halbbildung-kritik/` — erstes Profile mit Multi-Pass-Workflows + File-Aliasen + Selbstkritik-Klauseln
  - 5 Files: PROFILE.md + konstellations-anker.md (10 Anker A1-A10) + anti-patterns.md (10 APs mit Selbstanwendungs-Pflicht) + negative-diagnose-fragen.md (45 Fragen) + workflows.md (6 Multi-Pass-Workflows W-A-Multi/Halb/Kult/Jarg/Verd/Reflex je 4 passes)

### Verification

- Self-Test 62/62 PASS (T1-T56 + T57/T58/T59 NEU)
- Profile-Schema bleibt backward-compatible: klafki-didaktik (v0.1.6) + process-consulting (v0.1.0) funktionieren unverändert
- Multi-Pass-Workflow ist optional — Single-Pass-Workflows weiter unterstützt

### Methodische Spannung (CRITICAL, dokumentiert in ADR_0030 Annex C §C.8)

Profile-Pattern selbst ist eine Identifikations-Operation. Adorno-Profile reproduziert Strukturproblem (System-Form), kann es aber nicht aufheben. Selbstkritik-Klauseln in Profile-Workflows halten diese Spannung explizit — sie heben sie nicht auf.

### Deferred to v0.1.8+

- Adorno-Profile Phase 8 Live-Pilot (TC Halbbildungs-Diagnose) pending User-Aktion
- PB-004/005/006/008 weiterhin DEFERRED-Phase-2

---

## [0.1.6] — 2026-04-30 — Profile-with-workflows.md-Pattern + advisor-Skill-Patches + plugin.json-bridge-update-Eintrag

### Source: klafki-didaktik-Profile-Aufbau (Phase 7 Functional-Anchoring) → V-1/V-2 Open-Points uncovered

bridge-advisor SKILL.md hatte Hardcoding auf 4 Profile-Files (PROFILE.md + frames + APs + question-bank). pflicht_workflows-Frontmatter-Liste war soft-hint ohne operative Spec-Backbone. klafki-didaktik-Profile mit 5 ausspezifizierten Workflows (W-01..W-05) konnte nicht regulär geladen werden.

### Added

- **bridge-advisor SKILL.md** §Schritt 0 Profile-Loading erweitert um workflows.md-Loading (optional, Vorrang vor frontmatter-pflicht_workflows-Liste)
- **bridge-advisor SKILL.md** Anti-Pattern-Liste:
  - "NICHT workflows.md-Output-Formate ignorieren wenn Workflow getriggert"
  - "NICHT Workflow-Verweigerungs-Logik skippen"
- **bridge-advisor SKILL.md** Round-Type-Heuristik:
  - "Worker-Plan unvollständig + Workflow-Verweigerungs-Bedingung erfüllt → status mit Klärungs-Anforderung statt initial-advice"
- **docs/adr/ADR_0030_Expertise_Profile_Pattern.md Annex B** (NEU 2026-04-30) Profile-with-workflows.md-Pattern dokumentiert (Schema-Konvention + Vorrang-Regel + Backward-Compatibility)
- **plugin.json commands** Eintrag commands/bridge-update.md ergänzt (war v0.1.5-Lücke)
- **tests/smoke_self_test.py** T54 + T55 + T56 NEU
  - T54: ADR_0030 Annex B workflows.md-Pattern dokumentiert
  - T55: bridge-advisor SKILL.md workflows.md-Loading-Patch
  - T56: klafki-didaktik Reference-Profile Vollständigkeit (skip-if-private)

### Changed

- **bridge-advisor SKILL.md** Cross-Refs erweitert um ADR_0030 Annex B + v0.1.6 SKILL-Patch-Hinweis

### Reference-Implementation

- `private-notes/expertise-profiles/klafki-didaktik/` — erstes Profile mit workflows.md (5 Workflows + Meta-Halbierungs-Diagnose)
- `private-notes/expertise-profiles/process-consulting/` — bleibt v0.1.0 ohne workflows.md (Backward-Compat-Beispiel)

### Verification

- Self-Test 59/59 PASS (T1-T53 + T54/T55/T56 NEU)
- claude plugin validate (in User-Terminal-Session zu pruefen)
- Profile-Schema-Version unverändert v1.0.0 (workflows.md ist optionale Erweiterung, kein Schema-Break)

### Backward-Compatibility

- Profiles ohne workflows.md (z.B. process-consulting v0.1.0) funktionieren unverändert
- bridge-advisor degradiert sauber wenn workflows.md fehlt

### Deferred to v0.1.7+ (DEFERRED-Phase-2)

- PB-004 Auto-Trigger-Hooks (Trigger: ≥2 reale Pairs mit "haette geholfen"-Befund)
- PB-005 N-Pair-Topologie (Trigger: ≥3 parallele Sessions Use-Case)
- PB-006 Cross-Pair-Memory (Trigger: n≥5 Pairs pro Domain — aktuell n=1-3, ADR_0031 §5)
- PB-008 4-Layer-Meta-Architecture (Trigger: PB-006 Foundation + n≥10 Pairs)
- klafki-didaktik Live-Pilot (Phase 8) pending User-Aktion in p9-klafki-pilot-Workspace

---

## [0.1.5] — 2026-04-30 — Foundation Library + Lifecycle-Robustheit + ADR_0031-Decisions

### Source: v0.1.5-Roadmap Phasen B + D + G + H + I (Foundation + Lifecycle-Robustheit Release)

Phase B (PB-012 + PB-013) — Foundation:
- tools/bridge_state.py NEU (7 Library-Funktionen): read_state, write_atomic_cas (atomic-CAS via temp+rename + Pre-Atomic-Backup), validate_against_schema, pending_attach_replace (D-004 R23-Revidierung strict-mode), append_round (mit F-RP-26 Auto-Propagation), archive_shared_artifact, calibrate_wallclock_post_hoc
- commands/bridge-update.md NEU (PB-013): /bridge-update --field=<topic|expertise-source|worker-focus|domain-hint> --value=<new>; Pre-Flight whitelisting + phase-block + status_observations Update-Trail

Phase D — Lifecycle-Robustheit:
- D.1 PB-009 Drift-Plausibility-Check: Library check_drift_plausibility(domain_hint, drift_factor) Domain-aware mit DRIFT_RANGES (plugin-self-dev / use-case / default); Empirie-Anker p3 drift 1.14-2.4
- D.2 PB-002 Anti-Endless-Loop Reflection-Action-Ratio Domain-aware: Library compute_reflection_action_ratio + check_ratio_threshold per ADR_0031 §4.1 RATIO_THRESHOLDS (plugin-self-dev: 15.0, use-case: 4.0, default: 4.0)
- bridge-handover.md §lifecycle-health-checks-Sektion mit drift + ratio Library-Aufrufen

Phase G — PB-007 Domain-Hint-Field Activation:
- bridge_state_v1.json: topic_metadata.domain_hint-Enum (6 Werte: plugin-self-dev, use-case, architecture-spec, investigation-trace, methodology-improvement, other)
- schema_version-Enum erweitert auf 1.2.0
- bridge-init.md: --domain-hint optional Argument

Phase H — bilanz_v1-Schema Migration enforcement (PB-001 follow-up / ADR_0031 §4.3):
- Library validate_bilanz_against_schema NEU
- bridge-close.md §bilanz-schema-enforcement-Sektion mit ADR_0031 Cross-Refs

Phase I — ADR_0029 §5.6 Annex B (ADR_0031 §4.4):
- Filename-Konvention: bridge/bilanz_<pair_id>.md
- Schema-Pointer: schemas/bilanz_v1.json
- Migration-Kandidat: p4-eg-dev/bridge/BILANZ.md

### Added

- **tools/bridge_state.py** (NEU, 11 API-Funktionen + 2 Konstanten DRIFT_RANGES + RATIO_THRESHOLDS)
- **commands/bridge-update.md** (NEU, PB-013)
- **commands/bridge-close.md** §bilanz-schema-enforcement
- **commands/bridge-handover.md** §lifecycle-health-checks (drift + ratio)
- **commands/bridge-init.md** --domain-hint Argument (PB-007)
- **schemas/bridge_state_v1.json** topic_metadata.domain_hint-Enum + schema_version v1.2.0
- **docs/adr/ADR_0029_Session_Bridge_Pattern.md** Annex B (Bilanz-Filename-Konvention)

### Changed

- **state-Schema** v1.1.2 → v1.2.0 (topic_metadata.domain_hint, backward-compat mit v1.1.0/v1.1.1)

### Verification

- Self-Test 56/56 PASS (T40-T53 NEU, +14 Tests gegenueber v0.1.4)
- claude plugin validate (in User-Terminal-Session zu pruefen)
- ADR_0031-Decisions §4.1 (PB-002 Domain-aware), §4.2 (PB-007 Activation), §4.3 (bilanz Migration), §4.4 (Filename-Konvention) alle implementiert

### Deferred to v0.1.6+

- PB-004 Auto-Trigger-Hooks (Trigger: ≥2 reale Pairs mit "haette geholfen"-Befund)
- PB-005 N-Pair-Topologie (Trigger: ≥3 parallele Sessions Use-Case)
- PB-006 Cross-Pair-Memory (Trigger: n≥5 Pairs pro Domain — aktuell n=1-3, ADR_0031 §5)
- PB-008 4-Layer-Meta-Architecture (Trigger: PB-006 Foundation + n≥10 Pairs)
- Profile-Public-Release process-consulting (Trigger: post-juristische-Beratung User-Decision)

---

## [0.1.4] — 2026-04-30 — DEFERRED-Items + Schema-Formalisierungen + Lower-Priority + Cross-Pair-Patterns

### Source: v0.1.3-Roadmap Phasen A + C + E + F (Mini-Release)

Phase A (DEFERRED-V0.1.4-Items aus v0.1.3):
- F-RP-24 HIGH RESOLVED: Title-statt-Session-ID — `--worker-session-title` als primaerer UX-Flag, `--worker-session-id` als Fallback
- F-RP-26 BEOBACHTUNG RESOLVED: worker.phase Auto-Propagation aus Worker-Frontmatter

Phase C (Schema-Formalisierungen aus p3-Empirie):
- PB-001 RESOLVED: bilanz_v1.json Schema (12 Sektionen Reference-Implementation aus p3-bilanz_8cbeaad0.md)
- NEU: mapping_decisions_v1.json Schema (D-NNN-Format mit allOf-Pflicht DISSENS-DOCUMENTED requires sub_type)
- NEU: bridge_state_v1.json shared_artifacts.artifact_type-Enum (mapping-method-annex / mapping-decisions-log / bilanz / custom)

Phase E (Lower-Priority HIGH/MEDIUM):
- PB-003 RESOLVED: Pre-Decision-Verification Pflicht-Feld in handover-Frontmatter (allOf type=decision-lock, minItems=1, maxItems=2)
- PB-011 RESOLVED: shared-path-Default-Heuristik mit `tools/find_shared_path.sh` Helper-Stub
- PB-010 RESOLVED: bridge-handover §body-number-konsistenz optional Hook (WARN-Mode Tippfehler-Detection)

Phase F (Cross-Pair-Empirie-Synthese):
- ADR_0031 NEU: Cross-Pair-Patterns aus 4 Pilot-Run-Empirie (p3+p4+p5+p6) — 7 §-Sektionen + 9 §-Sub-Sektionen
- 4 ADR-Decisions: PB-002 Domain-aware Threshold, PB-007 Activation, bilanz_v1-Migration, ADR_0029 §5.6 Filename-Konvention

### Added

- **schemas/bilanz_v1.json** (NEU, PB-001) — Bilanz-File-Schema mit 12 Pflicht-Sektionen
- **schemas/mapping_decisions_v1.json** (NEU) — D-NNN-Decisions-Log-Schema mit allOf-Constraints
- **tools/find_shared_path.sh** (NEU, PB-011) — Helper-Script Stub fuer shared-path-Heuristik (executable)
- **docs/adr/ADR_0031_Cross-Pair-Patterns.md** (NEU) — Cross-Pair-Empirie-Synthese aus 4 Pilots
- **commands/bridge-init.md** §--worker-session-title (primaer) + Argument-Resolution title-first 3 Pfade (multi-match, no-match, direct-id)
- **commands/bridge-attach.md** §--this-session-title + §worker.phase-Initial-Set
- **commands/bridge-handover.md** §worker.phase-Auto-Propagation + §pre-decision-verification + §body-number-konsistenz
- **schemas/handover_frontmatter_v1.json** pre_decision_verification array property + allOf type=decision-lock requires it
- **schemas/bridge_state_v1.json** shared_artifacts.artifact_type-Enum + worker.phase Auto-propagation description

### Changed

- **synth_valid_handover** in tests/smoke_self_test.py — decision-lock-Cases include pre_decision_verification (1 Eintrag)
- **bridge-init.md** Argument-Resolution-Protokoll — title-first jetzt primaerer Pfad

### Deferred to v0.1.5

- Phase B (Foundation tools/-Library + bridge-update) — substantielles Refactoring, eigener Major-Patch
- Phase D (PB-009 Drift-Plausibility + PB-002 Anti-Endless-Loop) — depends on Phase B
- ADR_0031 Decisions §4.1 (PB-002 Domain-aware Threshold) + §4.2 (PB-007 Activation) + §4.3 (bilanz_v1 Migration enforcement) + §4.4 (ADR_0029 §5.6 Annex B Filename-Konvention)

### Verification

- Self-Test 42/42 PASS (T26-T39 NEU, +14 Tests)
- claude plugin validate (in User-Terminal-Session zu pruefen)
- Cross-Pair-Empirie-Validation via ADR_0031 (4 Pilot-Runs analysiert)

---

## [0.1.3] — 2026-04-29 — Plugin-Marketplace-Robustheit + F-RP-29-Disziplin

### Source: Bridge-Pair p3-real-user (Mapping-Phase R12-R26, 5 Decisions)

5 Mapping-Decisions D-001..D-005 covering 6 Items:
- D-001 F-RP-29 → DISSENS-DOCUMENTED §3.4.2 (Plan-vs-Execution-Layer-Konfusion)
- D-002 F-RP-32 → PATCH (Pre-Flight required-Args hard-enforce)
- D-003 F-RP-33 → AFFORDANCE (pre-allocated-Pattern-Doku)
- D-004 F-RP-23 → PATCH (Sentinel-Invariante, R23-revidiert nach Worker-Counter R22)
- D-005 Sub-A F-RP-15 → PATCH (sandbox-mount-Pre-Flight)
- D-005 Sub-B F-RP-34 → AFFORDANCE (Konvergenz-Skip-Konvention-Doku)

Plus existing v0.1.3-Backlog: F-RP-30 (Worker-Role-Boundary), F-RP-31
(User-Lifecycle-Visibility), F-RP-22 (Filesystem-Read), F-RP-24 (Title-statt-ID DEFERRED-V0.1.4),
F-RP-25 (ID-Resolution).

### Added

- **bridge-handover §forward-pointer-rationale-Sektion** (D-003) — pre-allocated-
  Pattern für decision-lock vor Annex-Materialisierung
- **bridge-handover §konvergenz-skip-rationale + Pre-Flight 6** (D-005 Sub-B)
- **bridge-handover §Re-Sync-Sub-Typen + Pre-Flight 5** (D-001 Worker-Pos) —
  plan-layer / execution-layer / hybrid Differenzierung
- **bridge-handover §Output-Marker BRIDGE-WRITE-COMPLETED** (D-001 Advisor-Pos)
- **bridge-attach + bridge-handover Pre-Flight 5 hard-enforce** required-Args (D-002)
- **bridge-init Pre-Flight 5b sandbox-mount + §sandbox-mount-prerequisite** (D-005 Sub-A)
- **bridge-init Pre-Flight 2 PFLICHT-Tool-Call** (F-RP-22) — Filesystem-Read statt Conversational-Memory
- **bridge-advisor §Anti-Plan-Drift + §User-Translation-Konvention** (D-001 Advisor-Pos, F-RP-29)
- **bridge-worker §Role-Boundary** (F-RP-30, CRITICAL) — keine Profile-pflicht-workflows
  oder AP-Diagnosen worker-side
- **bridge-worker §ID-Resolution-Pre-Flight** (F-RP-25) — Friction-Befund-ID-Lookup
- **bridge-status erweitert** (F-RP-31, CRITICAL) — User-friendly Output mit Rolle,
  Rounds, nächster Aktion, Polling-Hint, Forward-Pointer-Warnings
- **Skill-Mode-Marker `[bridge-worker mode]` / `[bridge-advisor mode | profile=...]`** (F-RP-31 Patch 4)
- **bridge-init §Visualization-Widget UX-Pattern** (F-RP-19 BEOBACHTUNG)

### Changed

- **bridge-init `--worker-session-id`** ist jetzt UX-Hint, nicht state-Pin (D-004,
  Breaking-Change). worker_obj setzt IMMER `session_id: SENTINEL_PENDING`.
- **bridge-attach Pre-Flight 4** strict-Sentinel (D-004) — kein auto-recover-Branch.
- **state-Schema v1.1.0 → v1.1.1** — `mapping_budget` als top-level optional, `mapping_category_history`
  per Decision, `shared_artifacts.{owner,status,round_allocated,round_active}` (forward-pointer),
  `status_observations.{type,defined_in_round,skipped_in_round,skip_basis,cycle_counter}` (convergence-skip).
- **Self-Test 15 → 28 Tests** (NEU T14-T25 für v0.1.3 Mapping-Decisions). Alle 28/28 PASS.

### Migration v0.1.2 → v0.1.3 (Breaking-Change F-RP-23)

`state.json` mit direktem session_id-Pin (v0.1.2-Use-Case mit `--worker-session-id`):
- Patch nötig:
  ```bash
  jq '.roles.worker.session_id = "pending-attach"' state.json > state.tmp && mv state.tmp state.json
  ```
- Anschließend: bridge-attach erneut ausführen

### Verification

- `claude plugin validate` PASS (erwartet)
- Self-Test 28/28 PASS (T14-T25 NEU)
- Bridge-Pair p3-real-user-Bilanz: `pilot-runs/p3-real-user/bridge/bilanz_8cbeaad0.md`
- Patch-Pipeline-Doku: `pilot-runs/p3-real-user/v0.1.3-patch-pipeline.md`

---

## [0.1.2-phase-b] — 2026-04-27 — process-consulting Profile (PB-014 Phase b, private)

### Added (private-notes/, NICHT im Plugin-Repo committed)

- **process-consulting Profile** v0.1.0 in `private-notes/expertise-profiles/process-consulting/`:
  - `PROFILE.md` (4 Methodik-Säulen, 3 Quellen, 4 Pflicht-Workflows, 8 Trigger-Phrasen, Frontmatter Pre-Flight 5/5 PASS)
  - `diagnostic-frames.md` (10 Frames in 6 Cluster-Gruppen — Organisation-als-Form, Mitgliedschaft+Rollen, Macht/Führung, Spannung+Integration, Schauseite/Simulation, Personalisierung)
  - `anti-patterns.md` (10 Anti-Patterns AP-01..10 mit Beobachtbarkeit + Begründung + Belege + Korrektiv)
  - `question-bank.md` (47 Diagnose-Fragen, gruppiert nach Frames + Bridge-Round-Type)
- **Curation-Workspace** `private-notes/process-consulting-curation/` mit Stufen 0-7 (Tag-Inventur 342 Files, 6 Cluster, 6 Subagent-Frame-Synthesen, Validation-Report)

### Empirie

- 6 Subagent-Calls (1 pro Cluster, sequentiell) — Wall-Clock 1.8-5.8 min pro Call (skaliert linear mit File-Count, ~3-5 sec/File)
- Total Subagent-Wall-Clock: ~18 min für 199 File-Reads
- 0 AMBIGUOUS-Findings, 10 Frames + 10 Anti-Patterns alle PASS
- Hypothesen-Revision durchgeführt: F3.1 von Foucault-Linie zu Luhmann/Kühl-Systemtheorie umformuliert (Subagent-Befund)
- 3 Lizenz-Issues paraphrasiert (S. 158/174/218, F4.2)

### Quellen

- Matthiesen/Muster/Laudenbach (2023): Die Humanisierung der Organisation. Vahlen
- Kühl, S. (2020): Organisationen — Eine sehr kurze Einführung. Springer
- Luhmann, N. (1964): Funktionen und Folgen formaler Organisation (zit. via Matthiesen + Kühl)

### Pre-Publication-Pflicht (deferred)

Profile bleibt in `private-notes/` (gitignored). Für öffentliche Distribution erforderlich: Lizenzrecht-Check + Cherry-Picking-Vollaudit + Empirie-Test in Real-User-Pair.

---

## [0.1.2] — 2026-04-26 — Expertise-Profile-Layer (PB-014 Phase a)

### Added

- **ADR_0030 Expertise-Profile-Pattern** LOCKED — neue Schicht-1-Architektur über bridge-advisor. Plugin bleibt domain-agnostisch, Domain-Expertise als externe Resource.
- **State-Schema v1.1.0** — `roles.advisor.expertise_profile` + `profile_version` als optionale Felder. Backward-compatible mit v1.0.0.
- **bridge-init `--expertise-profile=<path>` Flag** — Profile wird init-time-gepinnt im state.json.
- **Pre-Flight Punkt 5** — Profile-Validation (4 required_files + Frontmatter-Pflicht-Felder + supported profile_schema_version) vor state.json-Write.
- **bridge-advisor Schritt 0 Profile-Loading-Workflow** — bei jedem Trigger Profile lesen, Pflicht-Workflows + Round-Linkage anwenden.
- **References-Type `expertise-profile`** — methodische Referenzen aus Profile als Beleg-Quelle in Handovers.
- **`expertise-profiles/_SCHEMA.md`** — Profile-Layout-Konvention dokumentiert.
- **`expertise-profiles/_empty-test/`** — Empty-Profile-Fixture für Architektur-Smoke-Test.
- **`expertise-profiles/curation-spec.md`** — 7-Stufen-Curation-Methodik mit Anti-Halluzinations- und Lizenzrecht-Constraints. Vorbereitung für PB-014 Phase b (process-consulting Profile).

### Changed

- Self-Test erweitert von 12 auf 15 Tests (T11 expertise_profile-Field, T12 v1.0.0 backward-compat, T13 schema_version-enum). Alle 15/15 PASS.
- bridge-advisor Anti-Pattern-Section um 3 Profile-bezogene Regeln erweitert (Profile-Workflow-Skip, Mid-Pair-Switch-Verbot, Wörtliche-Zitat-Verbot).

### Phase-2-Roadmap

PB-014 Phase a (Architektur) abgeschlossen mit v0.1.2. **PB-014 Phase b** (process-consulting Profile-Curation, ~9-11 h) pending bei User-Pull-Trigger.

### Verification

- `claude plugin validate` PASS
- Self-Test 15/15 PASS
- ADR_0030 LOCKED (A1-A8 PASS)

---

## [0.1.1] — 2026-04-26 — Real-User-Pilot Hotfix

### Added

- **Worker-Notification-Block** (P-RP-04, CRITICAL) — `bridge-init` generiert ready-to-paste-Prompt für Worker-Session inkl. exakter `/bridge-attach`-Kommando. Verhindert Pair-stuck-in-init.
- **Argument-Resolution-Protokoll** (P-RP-02, HIGH) — bei missing `--topic` ABBRUCH + strukturierte User-Question via session_info MCP zur Worker-Session-Identifikation. Anti-Inferenz-Pattern explizit dokumentiert.
- **Sandbox-vs-Host-MCP-Mechanismus-Konvention** — bridge-init.md dokumentiert wann Sandbox-bash ausreicht und wann Host-MCP osascript-Fallback erforderlich ist.
- **pending-attach-Sentinel-Stubs** (P-RP-01, HIGH) — explizite String-Stubs für nicht-eigene Rolle bei init statt schema-invalides leeres Object.
- **bridge-attach Pre-Flight 4** (P-RP-08, LOW) — Sentinel-Detection (`session_id == "pending-attach"`) plus Replacement-Assertion garantiert sauberen Sentinel-zu-real-Session-Übergang.

### Fixed

- **Schema-Spec-Inkonsistenz im Init-Pseudocode** (F-RP-01) — Pseudocode produzierte `{}` für nicht-eigene Rolle, Schema verlangte `session_id` + `active_since`. Fix via pending-attach-Sentinel-Stubs (siehe Added).
- **Pre-Flight Punkt 4 deferred** (F-RP-03) — Skill-Spec war "Bei FAIL: ABBRUCH", aber Punkt 4 (session_info MCP) wurde in Real-User-Pilot deferred. Fix: alle 4 Punkte als atomar markiert, NICHT deferrable.
- **Worker-Session attached nie** (F-RP-04, CRITICAL) — Pair faktisch tot weil keine Worker-Notification. Fix: Pflicht-Output-Block in bridge-init.

### Changed

- bridge-init.md `argument-hint` erweitert um `--worker-session-id` (empfohlen für advisor-Rolle).
- bridge-init.md `description` erweitert: Plugin generiert ready-to-paste-Prompt.
- shared-path-Default-Heuristik verschärft: kein eigenes Working-Dir als Default, User-Question wenn nicht explizit gegeben.
- bridge-attach Anti-Pattern-Section: 5 statt 3 Items, inkl. Self-Attach-Detection und Sentinel-Replacement-Pflicht.

### Empirie-Quelle

- **EG_DEV_ADVISOR-Session** (2026-04-26): 5 HIGH/CRITICAL-Befunde im Init-Prozess (F-RP-01..04, F-RP-09).
- **UPP-DEV-WORKER + UPP-DEV-ADVISOR Pair** (2026-04-26): Funktionierender Bridge-Lifecycle bis Round 11 + 2 zusätzliche LOW/MED-Befunde (F-RP-10 Drift-Plausibility, F-RP-11 Number-Konsistenz).
- 11 Befunde insgesamt, 5 in v0.1.1 gepatched, 6 deferred zu Phase-2-Backlog (PB-009..013 + PB-005..008).

### Verification

- `claude plugin validate` PASS
- `tests/smoke_self_test.py` 12/12 PASS
- Plugin-Manifest + Marketplace-Manifest Version 0.1.0 → 0.1.1 gebumpt

---

## [0.1.0] — 2026-04-26 — Initial MVP Release

### Added

- **ADR_0029 Session-Bridge-Pattern** LOCKED — 13 Sektionen, 8 Drivers (D1-D10), 7 Constraints (C1-C7), 9 Akzeptanz-Kriterien (A1-A9 PASS).
- **Plugin-Manifest** `.claude-plugin/plugin.json` (CC-Validator-konform, v0.1.0).
- **Dependencies-Spec** `.claude-plugin/dependencies.json` (ADR_0028-Pattern, separat ausgelagert).
- **State-Schema** `schemas/bridge_state_v1.json` — JSON-Schema-Draft-7 für `bridge/state.json`.
- **Handover-Schema** `schemas/handover_frontmatter_v1.json` — YAML-Frontmatter-Validation für Handover-Files.
- **Skills**:
  - `skills/bridge-advisor/SKILL.md` — Cross-Session Advisor-Rolle, polling-based Status-Verifikation via session_info MCP.
  - `skills/bridge-worker/SKILL.md` — operative Worker-Rolle, schreibt Status/Counter/Pre-Flight/Execute/Verify Handovers.
- **Commands** (5):
  - `/bridge-init` — Pair initialisieren
  - `/bridge-attach` — zweite Session anschließen
  - `/bridge-handover` — Round-typisiertes Handover schreiben
  - `/bridge-status` — read-only State-Anzeige
  - `/bridge-close` — Pair schließen + Bilanz
- **Self-Test** `tests/smoke_self_test.py` — 12 Tests gegen Schema-Konsistenz, allOf-Pflichten, negative-Cases.
- **Pilot-Skripte**:
  - `pilot-runs/p1-script-mock/pilot_lifecycle_mock.py` — 12-Round-Lifecycle gegen Schemas, 20/20 PASS.
  - `pilot-runs/p2-subagent-pair/p2_validate.py` — Subagent-Pair-Validation, 19/19 PASS.

### Verification

- `claude plugin validate` PASS
- 39/39 Pilot-Tests PASS (12 self-test + 20 P1 script-mock + 7 P2 subagent-pair)

---

## Unreleased — Phase-2 Backlog

Siehe [`BACKLOG.md`](BACKLOG.md) für 13 Tier-1-Items (8 aus META_PROZESSE-Korpus-Mining + 5 aus Real-User-Pilot 2026-04-26).

**Aktivierungs-Reihenfolge:**

1. PB-012 tools/-Library (Foundation)
2. PB-013 /bridge-update-Command
3. PB-001 Bilanz-Schema
4. PB-009 Drift-Plausibility-Check
5. PB-002 Anti-Endless-Loop
6. PB-003 Pre-Decision-Verification
7. PB-011 shared-path-Heuristik
8. PB-010 Number-Konsistenz
