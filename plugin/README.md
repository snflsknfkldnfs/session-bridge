# session-bridge Plugin

Cross-Session Advisor/Worker coordination via shared filesystem (polling-based).

**Spec:** `../docs/adr/ADR_0029_Session_Bridge_Pattern.md` (LOCKED)
**Pattern-Mining:** `../docs/pattern-mining/CORPUS_ANALYSIS.md`

## Komponenten

| Datei | Zweck |
|---|---|
| `.claude-plugin/plugin.json` | Plugin-Manifest (CC-Validator-konform) |
| `.claude-plugin/dependencies.json` | External-Deps-Spec (ADR_0028-Pattern, separat weil CC-Validator keine custom keys akzeptiert) |
| `schemas/bridge_state_v1.json` | JSON-Schema für `bridge/state.json` |
| `schemas/handover_frontmatter_v1.json` | JSON-Schema für Handover-File-Frontmatter |
| `skills/bridge-advisor/SKILL.md` | Skill für advisor-Rolle |
| `skills/bridge-worker/SKILL.md` | Skill für worker-Rolle |
| `commands/bridge-init.md` | Command: Pair initialisieren |
| `commands/bridge-attach.md` | Command: 2. Session anschließen |
| `commands/bridge-handover.md` | Command: Handover schreiben |
| `commands/bridge-status.md` | Command: State anzeigen |
| `commands/bridge-close.md` | Command: Pair schließen + Bilanz |
| `tests/smoke_self_test.py` | Self-Test M7 (12 Tests) |

## Akzeptanz-Status (Phase 4)

| # | Kriterium | Status |
|---|---|---|
| M1' | bridge_state_v1.json syntaktisch valid | PASS |
| M2' | handover_frontmatter_v1.json syntaktisch valid | PASS |
| M5' | claude plugin validate | PASS |
| M7 | smoke_self_test.py | 12/12 PASS |

Phase 4 abgeschlossen 2026-04-26.

## Verwendung (Quick-Reference)

```bash
# Session A (Initiator, z.B. advisor):
/bridge-init --role=advisor --topic="my-topic" --expertise-source="..." --shared-path=/path/shared

# Output: pair_id=<uuid>

# Session B (Attacher, z.B. worker):
/bridge-attach <pair_id> --role=worker --worker-focus="..." --shared-path=/path/shared

# Beide Sessions anschließend:
/bridge-handover --type=<round-type> --references=<json> [--acceptance=<json>] [--rollback=<json>]
/bridge-status
/bridge-close --bilanz=bilanz.md --archive-orphans
```

## Self-Test ausführen

```bash
cd plugin && python3 tests/smoke_self_test.py
# Erwartet: 12/12 PASS, exit 0
```

Bei degraded mode (jsonschema fehlt): exit 2, Hinweis im Output.

## Constraints (ADR_0029 §7)

- Polling-only, kein IPC zwischen Sessions
- Read-only Cross-Session via `session_info` MCP
- Shared-Filesystem-Pflicht: beide Sessions müssen mind. einen gemeinsamen Project-Mount haben
- User-mediated Rounds (kein Auto-Tick)

## Phase 5 (Pilot)

Skript-Mock + Subagent-Pair-Smoke. Siehe Roadmap im Repo-Root README.
