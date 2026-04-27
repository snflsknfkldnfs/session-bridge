---
profile_name: _empty-test
profile_version: 0.0.1
profile_schema_version: 1.0.0
domain: testing
methodology_pillars: []
sources: []
trigger_phrases: []
pflicht_workflows: []
linkage_to_bridge_rounds:
  initial-advice: ""
  counter: ""
  re-sync: ""
  decision-lock: ""
  pre-patch: ""
required_files:
  - PROFILE.md
  - diagnostic-frames.md
  - anti-patterns.md
  - question-bank.md
---

# _empty-test Profile

**Zweck:** Fixture für Profile-Loading-Tests. Enthält keine Methodik, nur Schema-Pflicht-Felder.

Bei aktiviertem Profile sollte advisor-Skill keine zusätzlichen Workflows ausführen — generic-mode bleibt aktiv.

**Verwendung:** `--expertise-profile=expertise-profiles/_empty-test` in `/bridge-init` für Architektur-Smoke-Test.
