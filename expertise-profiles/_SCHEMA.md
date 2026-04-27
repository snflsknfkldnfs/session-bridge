# Expertise-Profile Schema v1.0.0

**ADR-Referenz:** ADR_0030 §3.3

## Verzeichnis-Layout

```
expertise-profiles/<profile-name>/
├── PROFILE.md              (Pflicht — Frontmatter + Body)
├── diagnostic-frames.md    (Pflicht)
├── anti-patterns.md        (Pflicht)
└── question-bank.md        (Pflicht)
```

## PROFILE.md Frontmatter (Pflicht-Felder)

```yaml
profile_name: <kebab-case-name>           # Verzeichnis-Name muss matchen
profile_version: <semver>                 # z.B. "0.1.0"
profile_schema_version: 1.0.0             # aktuelle Schema-Version
domain: <string>                          # z.B. "organizational-consulting"
methodology_pillars:                      # Methodik-Säulen
  - <string>
sources:                                  # Quellen-Zitations-Anker
  - <author> (<year>): <work>
trigger_phrases:                          # zusätzliche advisor-Trigger (optional)
  - <phrase>
pflicht_workflows:                        # Domain-Workflows
  - <workflow-id>
linkage_to_bridge_rounds:                 # round-type → workflow-modifier
  initial-advice: <string>
  counter: <string>
  re-sync: <string>
  decision-lock: <string>
  pre-patch: <string>
required_files:                           # Pflicht-Files-Liste
  - PROFILE.md
  - diagnostic-frames.md
  - anti-patterns.md
  - question-bank.md
```

## Body-File-Konventionen

### diagnostic-frames.md

N Frames pro Frame eine Sektion mit:
- **Frame-ID** (kebab-case, eindeutig)
- **Aussage** (1-2 Sätze, eigenformuliert)
- **Sub-Patterns** (2-4 Verfeinerungen)
- **Quell-Belege** (Citation mit Seitenzahl)
- **Anti-Aussage** (was Frame *nicht* meint)

### anti-patterns.md

N Anti-Patterns pro Anti-Pattern eine Sektion mit:
- **Anti-Pattern-Name**
- **Beobachtbarkeit** (woran erkennt man's)
- **Begründung** (warum problematisch)
- **Quell-Belege**
- **Korrektiv** (was statt dessen)

### question-bank.md

Fragen pro Frame gruppiert. Pro Frame 3-5 Diagnose-Fragen.

## Lizenzrecht-Constraints (ADR_0030 §5 C2)

- Frame-Aussagen + Anti-Pattern-Beschreibungen in **eigenformulierter Sprache** mit Quellen-Verweisen
- Wörtliche Zitate ≤1 Satz (Belege), mit Seitenzahl
- KEINE Reproduktion von Buch-Kapitel-Strukturen 1:1
- KEINE Reproduktion ganzer Zettel-Inhalte aus User-Vault

## Validierung

`/bridge-init --expertise-profile=<path>` Pre-Flight-Schritt 5 prüft:
1. `<path>/PROFILE.md` existiert + parsebar
2. Frontmatter hat alle Pflicht-Felder
3. `profile_schema_version` ist supported (`1.0.0`)
4. Alle `required_files` existieren

Bei FAIL → ABBRUCH mit Diagnose.
