# Profile-Curation-Spec

**Zweck:** Methodischer Ablauf für Curation eines Expertise-Profile aus einem Zettelkasten-Korpus oder vergleichbarer Quellen-Sammlung. Schützt vor Subagent-Halluzination + Lizenzrecht-Verletzung. Anwendbar auf erstes Profile `process-consulting` (Phase b) sowie zukünftige Profile.

**ADR-Referenz:** ADR_0030 §3.5 (Standalone-Pflicht), §5 C2 (Eigenformulierung).

---

## Stufen-Übersicht

| Stufe | Ziel | Modus | Output |
|---|---|---|---|
| 0 | Scope-Lock + Akzeptanz | Self-Edit | `curation-spec.md` (dieses Dokument) — pro Profile angepasst |
| 1 | Tag-Inventur | Self-Edit (bash) | `<profile>-curation/tag-inventory.md` |
| 2 | Cluster-Bildung | Self-Edit | `<profile>-curation/clusters.md` |
| 3 | Frame-Synthese | Subagent (1 pro Cluster, sequentiell) | `<profile>-curation/frames-cluster-N.md` |
| 4 | Anti-Pattern-Extraktion | Self-Edit | `<profile>-curation/anti-patterns-draft.md` |
| 5 | Question-Bank-Generierung | Self-Edit | `<profile>-curation/question-bank-draft.md` |
| 6 | Self-Validation + Lizenz-Pre-Check | Self-Edit | `<profile>-curation/validation-report.md` |
| 7 | Profile-Konsolidierung | Self-Edit | `expertise-profiles/<profile>/{PROFILE.md, diagnostic-frames.md, anti-patterns.md, question-bank.md}` |

`<profile>-curation/` ist Arbeitsverzeichnis (z.B. `private-notes/process-consulting-curation/`), wird **nicht** ins Plugin-Repo committed. Nur das finale Profile in Stufe 7 wird in `expertise-profiles/<profile>/` deployed.

---

## Stufe 0 — Scope-Lock + Akzeptanz

**Pro Profile vor Stufe 1 festlegen** (im Curation-Arbeitsverzeichnis als `00_scope-lock.md`):

| Field | process-consulting Default |
|---|---|
| Quell-Korpus | `/Users/paulad/Library/Mobile Documents/iCloud~md~obsidian/Documents/Zettelkasten/Literature Notes/{Die Humanisierung der Organisation, Kühl Stefan}` (~342 Files) |
| Ergänzende Cluster | Luhmann nur für Cross-Reference (nicht als eigener Cluster-Mining-Scope) |
| Frame-Anzahl-Range | 6-8 |
| Anti-Pattern-Anzahl-Range | 8-10 |
| Subagent-Strategie | 1 Subagent pro Cluster, sequentiell |
| Profile-Pfad | `private-notes/expertise-profiles/process-consulting/` (Pre-Publication-Stage) |
| Lizenzrecht-Kontext | Matthiesen/Muster/Laudenbach 2023 + Kühl ≤2010 — wörtliche Zitate ≤1 Satz, Belege mit Seitenzahl, Eigenformulierung Pflicht |

**Akzeptanz-Kriterien (atomar, alle Pflicht für Profile-Release):**

| ID | Kriterium |
|---|---|
| A1 | Stufe-1-Output: Tag-Inventar-Tabelle mit Tag → File-Count, basiert auf realer grep-Suche (verifizierbar) |
| A2 | Stufe-2-Output: 5-10 Cluster, jeder mit ≥3 Tag-Signal-Tags + ≥10 Filename-Belegen |
| A3 | Stufe-3-Output: pro Cluster-Frame: Aussage in Eigenformulierung + ≥3 Quell-Zettel + Anti-Aussage-Abgrenzung |
| A4 | Stufe-4-Output: Anti-Patterns mit Beobachtbarkeit, Begründung, Quell-Belegen, Korrektiv |
| A5 | Stufe-5-Output: 3-5 Diagnose-Fragen pro Frame, aus Frame-Inhalt abgeleitet (NICHT erfunden) |
| A6 | Stufe-6-Validation: Reverse-Check zu jedem Frame/Anti-Pattern: ≥3 Quell-Zettel als Belege existieren + Quell-Inhalt frame-tragend (kein cherry-picked) |
| A7 | Stufe-6-Lizenz-Pre-Check: keine wörtlichen Zitate >1 Satz, alle Citations haben Seitenzahl + Author-Year, KEINE 1:1-Reproduktion von Buch-Kapitel-Strukturen |
| A8 | Stufe-7-Output: Schema-konformes Profile, alle 4 required_files, frontmatter parsebar, Plugin-Pre-Flight-Schritt 5 PASS bei Test-Init |

---

## Stufe 1 — Tag-Inventur (Self-Edit)

**Methode:**
```bash
cd "<korpus-pfad>"
# Tag-Extraktion aus Zettelkasten-Tags (#tag1 #tag2 ...)
grep -rh "^#[A-Za-zÄÖÜäöüß]" *.md 2>/dev/null | \
  grep -oE "#[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß0-9-]+" | \
  sort | uniq -c | sort -rn > tag-frequency.txt

# File-pro-Tag-Mapping (für Top-30 Tags)
for tag in $(head -30 tag-frequency.txt | awk '{print $2}'); do
  echo "## $tag"
  grep -lE "$tag\b" *.md 2>/dev/null | head -20
  echo ""
done > tag-to-files.md
```

**Output `<profile>-curation/tag-inventory.md`:**
- Tag-Frequenz-Top-50
- Pro Tag (Top-20): vollständige Filename-Liste (oder ersten 20 plus Count-Marker)
- Cross-Cluster-Tags identifizieren (Tags die in mehreren Subordnern auftauchen)

**Akzeptanz A1:** Tabelle ist via bash reproducible.

---

## Stufe 2 — Cluster-Bildung (Self-Edit)

**Methode:** Tag-Co-Occurrence + Filename-Pattern-Matching.

Heuristik:
- Cluster-Anker = Top-Frequenz-Tag (z.B. `#Personalisierung`)
- Sekundär-Tags die häufig mit Anker auftauchen → Cluster-Tag-Signature
- Filenames die ≥2 Cluster-Signature-Tags enthalten → Cluster-Member

**Output `<profile>-curation/clusters.md`:**
- 5-10 Cluster, pro Cluster:
  - Cluster-Name (ableitbar aus Tags + Filename-Pattern)
  - Tag-Signature
  - Filename-Liste (vollständig)
  - Hypothese welcher Frame daraus emergiert

**Akzeptanz A2:** ≥3 Signal-Tags pro Cluster, ≥10 Filenames pro Cluster.

---

## Stufe 3 — Frame-Synthese (Subagent, kritisch)

**1 Subagent pro Cluster.** Sequentiell, NICHT parallel.

### Subagent-Brief-Template (Pflicht-Format)

```
Du bist Profile-Curation-Subagent für Cluster <N>: <Cluster-Name>.

**Pflicht-Read (vollständig, kein Sampling):**
<Liste aller N Filenames aus Cluster-Member-Liste>

**Anti-Halluzinations-Constraints:**
- KEINE Frame-Aussagen ohne Quell-Zettel-Belege (≥3 Zettel pro Frame)
- KEINE wörtlichen Zitate >1 Satz (Lizenzrecht-Constraint)
- KEINE Frame-Erfindung — nur was im Korpus tatsächlich aussagbar ist
- Bei Unsicherheit: STATUS=AMBIGUOUS markieren, nicht auflösen

**Output-Format pro Frame:**

```markdown
## Frame-<id>: <kurzer-name>

**Aussage (eigenformuliert, 1-2 Sätze):**
<text>

**Sub-Patterns (2-4 Verfeinerungen):**
- <text>
- <text>

**Quell-Belege (≥3):**
- <filename1.md> (Kühl 2011, S. 47): "<≤1 Satz wörtliches Zitat als Beleg>"
- <filename2.md> (Matthiesen et al. 2023, S. 89): "<≤1 Satz>"
- <filename3.md> (...): "<≤1 Satz>"

**Anti-Aussage (was Frame *nicht* meint):**
<1-2 Sätze Abgrenzung>

**Status:** PASS | AMBIGUOUS (mit Begründung)
```

**Pflicht-Output-Section "Files-Read-Audit":**
Liste jeden Filename aus Pflicht-Read-Liste mit `[OPENED]`-Status. Bei FAILED: Begründung. Vollständigkeit ist Akzeptanz-Kriterium.

**Wall-Clock-Erwartung:** 15-25 min für 30-50 Cluster-Files.

**Akzeptanz pro Subagent-Output:** 1-3 Frames pro Cluster, alle mit Status=PASS oder explizit AMBIGUOUS.
```

### Subagent-Output-Validation post-Run

- File-Read-Audit gegen reale Filename-Liste (Diff-Check via shell)
- Wall-Clock <3 min = Sampling-Verdacht (siehe Memory `feedback_subagent_thoroughness_drift.md`)
- Stichprobe: 2-3 Quell-Zettel selbst nachlesen → Frame-Aussage muss frame-tragend sein, nicht cherry-picked

---

## Stufe 4 — Anti-Pattern-Extraktion (Self-Edit)

**Methode:** Aus Korpus selbst extrahieren (nicht via Subagent — Domain-Kontext + Lizenzrecht-Awareness erfordern Self-Edit).

Anti-Patterns sind Aussagen wie:
- "Purpose-Driven-Übergriffigkeit" (aus Humanisierung-Cluster)
- "Transformationale Führung als Spirituelle Vorbild-Falle" (Humanisierung)
- "One-Company-Harmonie-Fiktion" (Humanisierung)

Pro Anti-Pattern:
- Beobachtbarkeit: woran erkennbar?
- Begründung: warum problematisch (mit Quell-Belegen)
- Korrektiv: was statt dessen (aus Frame-Synthese)

**Output `<profile>-curation/anti-patterns-draft.md`:** 8-12 Anti-Patterns.

---

## Stufe 5 — Question-Bank-Generierung (Self-Edit)

Pro Frame: 3-5 Diagnose-Fragen abgeleitet von Frame-Aussage.

**Format pro Frage:**
- Frage (kurz, eindeutig, beantwortbar im Beratungs-Kontext)
- Linkage zum Frame
- Erwartete Anwendungs-Situation (z.B. "vor pre-patch", "in counter-Round")

**Output `<profile>-curation/question-bank-draft.md`:** 18-40 Fragen.

---

## Stufe 6 — Self-Validation + Lizenz-Pre-Check (Self-Edit)

### Validation-Pass 1: Reverse-Check

Pro Frame + Anti-Pattern:
- Mindestens 3 Quell-Zettel-Belege?
- Quell-Inhalt tatsächlich frame-tragend (Stichprobe-Read)?
- Eigenformulierung deutlich (kein 1:1-Zitat-Ketten)?

### Validation-Pass 2: Lizenzrecht-Pre-Check

- Wörtliche Zitate-Audit: jedes Zitat ≤1 Satz, mit Seitenzahl + Author-Year?
- Buch-Struktur-Check: keine 1:1-Kapitel-Reproduktion?
- Kontext-Check: Zitate sind Belege im Eigentext, nicht Hauptinhalt?

### Output

`<profile>-curation/validation-report.md` mit:
- PASS-Liste (Frame/Anti-Pattern → 3 Quell-Belege OK)
- AMBIGUOUS-Liste (Frame mit Begründung warum AMBIGUOUS, Resolution-Vorschlag)
- Lizenz-Findings (falls Constraints verletzt)

**Akzeptanz A6+A7:** Alle Frames/Anti-Patterns Status=PASS, alle Lizenz-Constraints eingehalten.

---

## Stufe 7 — Profile-Konsolidierung (Self-Edit)

Aus Stufen 1-6 → finale Profile-Files:

### `expertise-profiles/<profile>/PROFILE.md`

Frontmatter aus Stufe-2-Cluster + Stufe-3-Frames + Stufe-4-Anti-Patterns. Body mit Methodik-Sockel-Text (eigenformuliert, ~500 Wörter).

### `expertise-profiles/<profile>/diagnostic-frames.md`

Aus Stufe-3-Output konsolidiert. Pro Frame: Aussage + Sub-Patterns + Belege (kompakt) + Anti-Aussage.

### `expertise-profiles/<profile>/anti-patterns.md`

Aus Stufe-4-Output. Pro Anti-Pattern: Name, Beobachtbarkeit, Begründung, Belege, Korrektiv.

### `expertise-profiles/<profile>/question-bank.md`

Aus Stufe-5-Output. Frage-Cluster pro Frame.

**Akzeptanz A8:** Test-Init mit `--expertise-profile=private-notes/expertise-profiles/<profile>` → Pre-Flight-Schritt 5 PASS.

---

## Curation-Aufwand-Schätzung (process-consulting Default)

| Stufe | Aufwand | Modus |
|---|---|---|
| 0 Scope-Lock | 0.5 h | Self-Edit |
| 1 Tag-Inventur | 0.5 h | Self-Edit + bash |
| 2 Cluster-Bildung | 1 h | Self-Edit |
| 3 Frame-Synthese | 2-3 h | 5-7 Subagent-Calls (sequentiell, 15-25 min FEST) |
| 4 Anti-Patterns | 1.5 h | Self-Edit |
| 5 Question-Bank | 1 h | Self-Edit |
| 6 Validation | 1.5 h | Self-Edit + Stichproben |
| 7 Konsolidierung | 1 h | Self-Edit |
| **Total** | **9-11 h** | |

---

## Cross-Refs

- ADR_0030 Expertise-Profile-Pattern (Schema-Spec)
- `_SCHEMA.md` (Profile-Layout-Konvention)
- Memory `feedback_subagent_thoroughness_drift.md` (Anti-Halluzinations-Pattern)
- Memory `feedback_real_user_pilot_lessons.md` (Anti-Pattern Inferenz-statt-Frage)
- BACKLOG.md PB-014 (Architektur-Item)
