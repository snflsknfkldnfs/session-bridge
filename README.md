# session-bridge

Plugin zur Koordination zweier paralleler Cowork-Sessions im Advisor/Worker-Pattern.

## Status

Build-Stage: **outputs/session-bridge/** (Spike-Lokation)
Ziel-Lokation: **~/session-bridge/** (eigenes Repo, post-ADR-Lock)
Phase: **Phase 0 — Repo-Setup**

## Repo-Struktur

```
session-bridge/
├── README.md                              # this
├── docs/
│   ├── adr/
│   │   └── ADR_0029_Session_Bridge_Pattern.md   # Lock-Pflicht vor Code
│   └── pattern-mining/
│       └── CORPUS_ANALYSIS.md             # Korpus-Anforderungen
└── plugin/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── skills/
    │   ├── bridge-advisor/
    │   └── bridge-worker/
    └── commands/
        ├── bridge-init.md
        ├── bridge-handover.md
        └── bridge-status.md
```

## Roadmap

| Phase | Inhalt | Status |
|---|---|---|
| 0 | Repo-Setup | in_progress |
| 1 | Pattern-Mining (Korpus: Cross-Session-Beratungs-Artefakte) | blocked-by 0 |
| 2 | ADR_0029 Draft | blocked-by 1 |
| 3 | ADR Self-Review + Lock | blocked-by 2 |
| 4 | MVP-Plugin-Scaffold | blocked-by 3 |
| 5 | Pilot-Test synthetisch | blocked-by 4 |

## Scope-Lock

**IN:** Polling-only MVP, 2-Pair-Topologie, manuelle Commands.
**OUT:** Auto-Trigger-Hooks, N-Pair-Topologie, Cross-Plugin-Bridges.

## Constraints

- session_info MCP als Read-Backbone (read_transcript, list_sessions).
- Kein IPC zwischen Sessions möglich — Polling via shared state-file.
- Schreib-Operationen nur in shared Cowork-Project-Pfad oder eigenes Repo.
