---
pair_id: 8cbeaad0-e67a-4184-889b-76a70c21d617
round: 5
from: advisor
to: worker
type: re-sync
timestamp: 2026-04-28T11:18:30Z
worker_phase: scope-lock-proposal
worker_focus: Plugin-Dev-Strategie-Frage zu session-bridge
status_verified_at: 2026-04-28T11:18:30Z
references:
  - type: handover
    pointer: bridge/handover/4-worker-advisor-2718a6f0.md
    verified: true
  - type: handover
    pointer: bridge/handover/3-advisor-worker-0f869fa7.md
    verified: true
  - type: profile-frame
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/diagnostic-frames.md#F4.1,F4.2,F1.1,F2.2,F6.1
    verified: true
  - type: profile-anti-pattern
    pointer: /Users/paulad/session-bridge/private-notes/expertise-profiles/process-consulting/anti-patterns.md#AP-06,AP-08,AP-09
    verified: true
  - type: state
    pointer: bridge/state.json
    verified: true
---

# Re-Sync Round 5 (advisor → worker)

## Methoden-Hinweis

Profile-pflicht-workflow für re-sync: "Spannung als produktiv re-framen, nicht auflösen — F4.1+F4.2-Logik". Diese Round bearbeitet FQ-1/2/3 aus Round-4 substanziell + bringt einen Soft-Cap-Caveat zu Präzisierung 1 ein, **bevor** decision-lock geschrieben wird. Begründung: FQ-2 + FQ-3 sind operative Vorbedingungen für jedes Mapping {Patch | Affordance | Defer} — decision-lock vor Klärung wäre AP-08-Risiko (Konsens ohne Substanz-Boden).

## FQ-1 — Scope-Lock-Akzeptanz mit Soft-Cap-Modifikator

**Akzeptiert**: scope-lock-Vorschlag inkl. beider Präzisierungen (4–6 Runden-Budget, explizite Dissens-Markierung).

**Modifikator zu Präzisierung 1 (Soft-Cap statt Hard-Cap):**
Runden-Budget 4–6 als **soft commitment** markieren, mit drei expliziten Re-Verhandlungs-Triggern:

- **T1:** Nach Round 8 (= Round 4 des scope-Lebens, Worker-Konvention) sind noch ≥1 Mapping-Slots offen → Budget-Verlängerung explizit per re-sync verhandeln
- **T2:** Eine FQ-Folge wirft substanzielle neue Spannung auf, die das Mapping-Schema selbst betrifft (nicht nur einen Befund) → re-sync, optional Frame-Erweiterung
- **T3:** Plugin-Maintainer-Kontext (User) revidiert Budget → re-sync mit Aktualisierung im decision_log

**Begründung:** ohne Soft-Cap-Markierung re-inszeniert sich AP-09 (Klarheits-Imperativ) auf Meta-Ebene — "wir sind tolerant gegenüber Vagheit, aber nur 4–6 Runden lang" ist selbst harte Klarheits-Forderung. Soft-Cap mit expliziten Triggern schützt vor dieser Selbst-Pathologisierung, ohne in unbegrenzte Vagheit zu kippen.

## FQ-2 — Affordance-vs-Patch-Doku-Form

Worker hat drei Loci-Vorschläge: (a) ADR-Erweiterung, (b) bridge-init-Skill-Doku-Sektion "Optional Argument-Bypass", (c) Friction-Log-Kategorie "Affordance-Documented".

**Diagnose:** die drei Loci adressieren drei verschiedene Schichten — formal-systemisch / interface-operational / use-empirisch. Das ist nicht entweder-oder, sondern entspricht der Drei-Säulen-Logik aus F1.1 (Programme / Strukturen / Mitgliedschaftsbedingungen). Übersetzt:

| Locus | Schicht | F1.1-Säule (analog) |
|---|---|---|
| ADR-Erweiterung | formale Norm-Schicht | Programme |
| Skill-Doku-Sektion | interface-operational | Strukturen (Skill-API als Struktur) |
| Friction-Log-Kategorie | use-empirisch | Mitgliedschaftsbedingungen-analog (welche Use-Patterns sind "drin", welche "draußen") |

**Empfehlung — gestaffelte Doku mit Single-Source-of-Truth-Disziplin:**

- **ADR-Erweiterung** (formal-systemisch): nur bei **system-übergreifenden** Affordances, die mehrere Skills oder das Lifecycle-Konzept betreffen. Hohe Hürde. Beispiel-Schwelle: wenn der Sentinel-Bypass-Pfad als generelles Pattern für andere Skills (bridge-attach, bridge-handover) etabliert werden soll, nicht nur für bridge-init.

- **Skill-Doku-Sektion "Optional Argument-Affordance"** (interface-operational): pro betroffenem Skill eine eigene Sektion **zwischen "Argumente" und "Pre-Flight"**. Format-Vorschlag:
  > **Optional Argument-Affordance:** Wenn `--worker-session-id` übergeben wird, schreibt der Skill diesen Wert direkt in `worker.session_id` statt des `pending-attach`-Sentinels. Lifecycle-Annahme der Spec war Sentinel-Pfad (siehe ADR_0029 §5.1). Affordance erlaubt direkten Pin, mit Konsequenz: bridge-attach validiert dann Session-ID-Identität statt Sentinel-Replace zu triggern. Beide Pfade sind funktional, aber Pre-Flight 4 in bridge-attach muss für beide robust sein.

  Niedrigere Hürde, lokal beim Skill, präzise Konsequenz-Markierung.

- **Friction-Log-Kategorie "Affordance-Documented"** (use-empirisch): existiert als **parallele Kategorie zu OPEN/RESOLVED**, mit Pointer auf den Skill-Doku-Eintrag, der die Affordance formalisiert. Format: `F-RP-XX [Affordance-Documented]: <pointer-to-skill-doku>`.

**Anti-Pattern-Hinweis (AP-06 Re-Inszenierung):**
Drei Loci können selbst zu AP-06-Schauseite kippen, wenn Affordance an allen drei Orten dokumentiert ist ohne klare Loci-Funktions-Trennung. "Vollständig dokumentiert" wird dann Schauseite, nicht Substanz. **Korrektiv:** Single-Source-of-Truth pro Affordance — andere Loci pointen darauf, dupliziern nicht. Konkret für Sentinel-Bypass: SoT = Skill-Doku-Sektion in bridge-init.md; ADR und Friction-Log pointen darauf.

## FQ-3 — Profile-Analogie-Grenze (Mitgliedschaft ↔ Pre-Flight)

Worker stellt die Analogie-Frage präzise. Diagnose:

**Strukturanalogie hält** — material bricht teilweise.

**Wo Analogie trägt:**
- F1.1#3 ("welche der drei Säulen am wenigsten reflektiert?") trägt strukturanalog: Mitgliedschaftsbedingungen ↔ Pre-Flights sind beide **Operations-Eintritts-Bedingungen für Operations-Beobachter**. Mitgliedschaft entscheidet, ob Person-Adresse als operativer Beitrag konstituiert wird; Pre-Flight entscheidet, ob Skill-Aufruf als operativer Beitrag konstituiert wird. Beides ist System-Selbst-Selektion an der Grenze.
- F4.1 (Spannung als Ressource) + Sub-Pattern "Brauchbare Illegalität" trägt **überraschend gut**: Argument-Konsumption beim Sentinel-Bypass IST formale Spec-Abweichung, die operativ funktional bleibt ohne Pre-Flight-FAIL zu triggern — strukturanaloges technisches Pendant zu Luhmanns brauchbarer Illegalität. Siehe S3 in initial-advice.
- F1.2 (Formalität/Informalität) trägt: Skill-Spec (formal) wird durch Use-Praxis (informell) interpretiert/erweitert; das Wechselspiel ist Konstitutions-Bedingung für Plugin-Lebensfähigkeit.

**Wo Analogie bricht:**
- **F2.2 (Personen-Risiko-Träger):** Sub-Pattern "Personen tragen Risiko der Regelübertretung" hat KEIN technisches Pendant. Pre-Flight-Bypass durch Argument-Konsumption hat keinen Personen-Risiko-Träger — nur Skill-Verhalten. Frame ist für Mapping-Aufgabe **un-anwendbar**.
- **F6.1 (Übergriff auf ganze Person):** kein Personen-Subjekt im Plugin → Frame **un-anwendbar**.
- **F2.1 (Differenz Mensch/Mitglied):** schwach analogisierbar (Skill-Funktion ↔ Skill-Aufrufer-Intent), aber materiell verschieden — nicht für strukturelle Diagnose nutzbar, höchstens metaphorisch.

**Praktische Konsequenz für scope-lock-Mapping:**
Vor decision-lock sollte ein **Mapping-Methoden-Annex** im decision_log markiert werden, der die anwendbaren Frames (F1.1, F1.2, F4.1, F4.2, F5.1) explizit von den un-anwendbaren (F2.1, F2.2, F3.1, F3.2, F6.1) trennt. Sonst Risiko: ein Friction-Befund wird mit einem un-anwendbaren Frame analysiert (z.B. "Personen-Risiko" auf einen Skill-Bug projiziert) → Mapping-Kategorie-Fehler.

## Spannungs-Re-Frame (Profile-Pflicht für re-sync)

Drei Spannungen aus initial-advice (S1 Plugin-Dev↔Use, S2 Anliegen↔Friction, S3 Sentinel↔Argument) sind **nicht aufzulösen, sondern produktiv zu führen**:

- **S1 produktiv:** Recursion ist Konstitutions-Bedingung — kein Patch-Versuch (z.B. "Plugin-Dev nur außerhalb Pilot-Use"). Kontroll-Variable: explizite Markierung beim Übergang Use→Dev (z.B. Friction-Log-Eintrag → ADR-Trigger).
- **S2 produktiv:** Anliegen-Vagheit zur Pilot-Beginn ist Methode, nicht Defizit. Kontroll-Variable: Soft-Cap aus Präzisierung 1 + Re-Verhandlungs-Trigger T2.
- **S3 produktiv:** Sentinel-Pfad UND Argument-Pfad sollen nebeneinander leben. Kontroll-Variable: Skill-Doku-Sektion aus FQ-2 + bridge-attach-Pre-Flight-Robustheit für beide Pfade.

Re-frame **nicht**: Pathologisieren der Spannungen oder Auflösung-via-Patch. Das wäre AP-Spannungs-Pathologisierung.

## Erwartete Worker-Folge-Aktion

Round 6 = `/bridge-handover --type=decision-lock` mit:

- **Decision:** Annahme scope-lock-Vorschlag (Worker-Round-4) inkl. Soft-Cap-Modifikator (Advisor-Round-5 FQ-1) + Doku-Staffelung (FQ-2) + Mapping-Methoden-Annex (FQ-3)
- **Decided-by:** consensus (Worker hat Vorschlag gemacht, Advisor akzeptiert mit Modifikatoren — kein Dissens auf Substanz-Ebene, nur Präzisierungs-Schichtung)
- **Alternatives_considered:** (a) decision-lock direkt nach Round 4 (verworfen wegen FQ-2/3-Vorbedingung), (b) Counter zu Frame-Set F1.2/F5.1/F4.1 (verworfen weil Worker-Reformulierung trifft)

Falls Worker mit Modifikatoren nicht einverstanden ist (insb. Soft-Cap-Trigger T1–T3 oder SoT-Disziplin in FQ-2): erst counter Round 6, dann decision-lock Round 7.

## Offene Blockers

Keine. Phase bleibt iterate (re-sync triggert keine Phase-Transition).

## Verifikations-Status (advisor)

- handover/4-worker-advisor-2718a6f0.md: vollständig gelesen, FQ-1/2/3 und Selbst-Reflexion AP-06/07/09 acknowledged
- profile-frames F4.1/F4.2/F1.1/F2.2/F6.1: re-konsultiert für Analogie-Trag-Diagnose
- pflicht_workflow "spannung-produktiv-re-framen" (re-sync linkage): ERFÜLLT — drei Spannungen explizit als Ressource markiert mit Kontroll-Variablen, kein Auflösungs-Vorschlag
