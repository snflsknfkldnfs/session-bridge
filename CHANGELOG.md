# Changelog

All notable changes to session-bridge are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) — Semver pinned per ADR_0029 §13.1.

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
