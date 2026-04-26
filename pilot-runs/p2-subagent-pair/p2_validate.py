#!/usr/bin/env python3
"""P2-Pilot Final-Validation: prüft beide Subagent-Handovers nach Schema + Cross-Konsistenz."""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPT_DIR.parent.parent  # Repo-Root (post-Restructure)
SHARED = SCRIPT_DIR / "shared"
BRIDGE = SHARED / "bridge"
HANDOVER_DIR = BRIDGE / "handover"
HANDOVER_SCHEMA = PLUGIN_ROOT / "schemas" / "handover_frontmatter_v1.json"


def parse_frontmatter(md_text: str) -> dict | None:
    """Parse YAML-Frontmatter aus Markdown (zwischen --- und ---)."""
    m = re.match(r"^---\n(.*?)\n---", md_text, re.DOTALL)
    if not m:
        return None
    try:
        import yaml
        return yaml.safe_load(m.group(1))
    except ImportError:
        # Fallback: naive parse for our subset
        result = {}
        for line in m.group(1).splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            v = v.strip()
            if v.startswith("[") or v.startswith("{"):
                v = json.loads(v)
            elif v in ("true", "false"):
                v = v == "true"
            elif v.isdigit():
                v = int(v)
            result[k.strip()] = v
        return result


def main() -> int:
    try:
        import jsonschema
    except ImportError:
        print("[FATAL] jsonschema not available")
        return 2

    results = []

    # P2-V1: Beide Handover-Files existieren
    advisor_files = list(HANDOVER_DIR.glob("1-advisor-worker-*.md"))
    worker_files = list(HANDOVER_DIR.glob("2-worker-advisor-*.md"))

    results.append(("P2-V1 advisor handover exists", len(advisor_files) == 1, f"found={len(advisor_files)}"))
    results.append(("P2-V1 worker handover exists", len(worker_files) == 1, f"found={len(worker_files)}"))

    if not advisor_files or not worker_files:
        for name, ok, det in results:
            mark = "✓" if ok else "✗"
            print(f"{mark} {name} — {det}")
        print("\nP2 FAIL — fehlende Handovers, kann nicht weiter validieren.")
        return 1

    # P2-V2: Frontmatter parse + schema-validate
    schema = json.loads(HANDOVER_SCHEMA.read_text())

    advisor_ho = parse_frontmatter(advisor_files[0].read_text())
    worker_ho = parse_frontmatter(worker_files[0].read_text())

    results.append(("P2-V2 advisor frontmatter parsed", advisor_ho is not None, ""))
    results.append(("P2-V2 worker frontmatter parsed", worker_ho is not None, ""))

    if advisor_ho:
        try:
            jsonschema.validate(advisor_ho, schema)
            results.append(("P2-V3 advisor schema validate", True, ""))
        except jsonschema.ValidationError as e:
            results.append(("P2-V3 advisor schema validate", False, e.message[:200]))

    if worker_ho:
        try:
            jsonschema.validate(worker_ho, schema)
            results.append(("P2-V3 worker schema validate", True, ""))
        except jsonschema.ValidationError as e:
            results.append(("P2-V3 worker schema validate", False, e.message[:200]))

    # P2-V4: pair_id konsistent
    state = json.loads((BRIDGE / "state.json").read_text())
    state_pair_id = state["pair_id"]

    if advisor_ho and worker_ho:
        results.append(("P2-V4 advisor pair_id matches state",
                        advisor_ho["pair_id"] == state_pair_id,
                        f"a={advisor_ho['pair_id'][:8]} s={state_pair_id[:8]}"))
        results.append(("P2-V4 worker pair_id matches state",
                        worker_ho["pair_id"] == state_pair_id,
                        f"w={worker_ho['pair_id'][:8]} s={state_pair_id[:8]}"))
        results.append(("P2-V4 advisor==worker pair_id",
                        advisor_ho["pair_id"] == worker_ho["pair_id"], ""))

    # P2-V5: Round-Numbering korrekt
    if advisor_ho and worker_ho:
        results.append(("P2-V5 advisor round=1", advisor_ho["round"] == 1, f"round={advisor_ho['round']}"))
        results.append(("P2-V5 worker round=2", worker_ho["round"] == 2, f"round={worker_ho['round']}"))

    # P2-V6: Round-Type-Korrektheit
    if advisor_ho and worker_ho:
        results.append(("P2-V6 advisor type=initial-advice",
                        advisor_ho["type"] == "initial-advice", f"type={advisor_ho['type']}"))
        results.append(("P2-V6 worker type=counter",
                        worker_ho["type"] == "counter", f"type={worker_ho['type']}"))

    # P2-V7: From/To-Konsistenz
    if advisor_ho and worker_ho:
        results.append(("P2-V7 advisor from=advisor to=worker",
                        advisor_ho["from"] == "advisor" and advisor_ho["to"] == "worker", ""))
        results.append(("P2-V7 worker from=worker to=advisor",
                        worker_ho["from"] == "worker" and worker_ho["to"] == "advisor", ""))

    # P2-V8: References ≥1
    if advisor_ho and worker_ho:
        results.append(("P2-V8 advisor references ≥1",
                        len(advisor_ho.get("references", [])) >= 1,
                        f"count={len(advisor_ho.get('references', []))}"))
        results.append(("P2-V8 worker references ≥1",
                        len(worker_ho.get("references", [])) >= 1,
                        f"count={len(worker_ho.get('references', []))}"))

    # P2-V9: Body-Substantialität (counter darf nicht trivial sein)
    worker_body = worker_files[0].read_text()
    body_after_frontmatter = re.split(r"^---\s*$", worker_body, flags=re.MULTILINE)[2]
    word_count = len(body_after_frontmatter.split())
    results.append(("P2-V9 worker body ≥80 words (substantielle Falsifikation)",
                    word_count >= 80, f"words={word_count}"))

    # P2-V10: Body keine Trivial-Phrase
    trivial_phrases = ["passt nicht", "doesn't fit", "nicht geeignet"]
    has_trivial = any(p.lower() in body_after_frontmatter.lower() for p in trivial_phrases)
    has_substantive_marker = any(m in body_after_frontmatter.lower()
                                 for m in ["wallclock", "schema", "ac", "frontmatter", "pre-patch", "konsistenz"])
    results.append(("P2-V10 worker body substantielle Begründung",
                    has_substantive_marker and not has_trivial,
                    f"substantive={has_substantive_marker} trivial={has_trivial}"))

    # Summary
    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print(f"\n{'='*70}")
    print(f"P2 Subagent-Pair Validation: {passed}/{total} steps PASS")
    print(f"{'='*70}")
    for name, ok, det in results:
        mark = "✓" if ok else "✗"
        print(f"  {mark} {name}" + (f" — {det}" if det else ""))

    failed = total - passed
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
