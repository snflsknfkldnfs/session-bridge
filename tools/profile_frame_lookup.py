#!/usr/bin/env python3
"""
tools/profile_frame_lookup.py — Profile-Frame-Dispatch v0.1.11 (Option B-Plus).

NEU v0.1.11: Erlaubt punktuelle Profile-Element-Lookups ohne volle Profile-Aktivierung.

Use-Case: architecture-archaeology-advisor will Adorno-AP-A05 anwenden auf Plugin-Marketing-Text
- Statt voll-Adorno-Profile (~18000 Tokens) nur AP-A05 laden (~800 Tokens)
- Methodische Konsistenz-Marker im Output (User sieht: punktuelle Anwendung, nicht voll-Methodik)
- ADR_0030 D5 Single-Profile-Pinning bleibt erhalten (Primär-Profile dominiert)

API:
- lookup_frame(profile_name, frame_id) -> dict
- lookup_ap(profile_name, ap_id) -> dict
- lookup_question(profile_name, frame_id=None, round_type=None) -> list
- lookup_workflow_pass(profile_name, workflow_id, pass_n=None) -> dict
- list_available_profiles() -> list
- list_frames(profile_name) -> list
- list_aps(profile_name) -> list

Cache: per-Session in-memory (LRU).

Cross-Refs:
- ADR_0030 §3.4 Profile-Loading (Single-Profile-Pinning)
- ADR_0030 Annex E (Profile-Frame-Dispatch-Pattern v0.1.11)
- expertise-profiles/architecture-archaeology/token-efficiency-patterns.md OP-1 (Skill-Trigger-Phrase-Filter — Profile-Lookup ist Spezialfall)
"""

import re
from functools import lru_cache
from pathlib import Path
from typing import Optional

# Profile-Search-Dirs (analog tools/bridge_state.py PROFILE_SEARCH_DIRS)
PROFILE_SEARCH_DIRS = [
    Path.home() / "session-bridge" / "private-notes" / "expertise-profiles",
    Path.home() / "session-bridge" / "expertise-profiles",
]

# Profile-Short-Names (analog tools/bridge_state.py PROFILE_SHORT_NAMES)
PROFILE_SHORT_NAMES = {
    "klafki": "klafki-didaktik",
    "adorno": "adorno-halbbildung-kritik",
    "foucault": "foucault-genealogie",
    "luhmann": "luhmann-erziehungssystem",
    "process-consulting": "process-consulting",
    "process": "process-consulting",
    "arch": "architecture-archaeology",
    "architecture": "architecture-archaeology",
    "plugin-dev": "claude-plugin-dev",
    "claude-plugin-dev": "claude-plugin-dev",
}

# File-Aliase (analog ADR_0030 Annex C, v0.1.7)
FILE_ALIASES = {
    "diagnostic_frames": ["diagnostic-frames.md", "konstellations-anker.md"],
    "anti_patterns": ["anti-patterns.md"],
    "question_bank": ["question-bank.md", "negative-diagnose-fragen.md"],
    "workflows": ["workflows.md"],
    "token_efficiency_patterns": ["token-efficiency-patterns.md"],
}


def _resolve_profile_dir(profile_name: str) -> Path:
    """Resolve Profile-Name (Short oder Full) zu absolutem Verzeichnis."""
    expanded = PROFILE_SHORT_NAMES.get(profile_name, profile_name)
    for sd in PROFILE_SEARCH_DIRS:
        if not sd.exists():
            continue
        candidate = sd / expanded
        if candidate.exists():
            return candidate
        # Glob-Match
        matches = list(sd.glob(f"{expanded}*"))
        if len(matches) == 1:
            return matches[0]
    raise FileNotFoundError(
        f"Profile '{profile_name}' (expanded '{expanded}') nicht in {PROFILE_SEARCH_DIRS} gefunden"
    )


def _load_file_with_alias(profile_dir: Path, alias_key: str) -> str:
    """Lade Profile-File mit Alias-Resolution."""
    for fname in FILE_ALIASES.get(alias_key, [alias_key]):
        f = profile_dir / fname
        if f.exists():
            return f.read_text()
    raise FileNotFoundError(
        f"Kein File für '{alias_key}' in {profile_dir} (gesucht: {FILE_ALIASES.get(alias_key, [alias_key])})"
    )


@lru_cache(maxsize=64)
def _load_profile_section(profile_name: str, file_key: str) -> str:
    """LRU-cached File-Read pro Profile + File."""
    pd = _resolve_profile_dir(profile_name)
    return _load_file_with_alias(pd, file_key)


def lookup_frame(profile_name: str, frame_id: str) -> dict:
    """
    Lookup eines spezifischen Frames aus einem Profile, ohne voll-Profile-Aktivierung.

    Args:
        profile_name: Profile-Short-Name (z.B. "adorno") oder Full-Name
        frame_id: Frame-ID (z.B. "F5.1", "A1", "F1.2")

    Returns:
        dict mit: profile_name, frame_id, body (text), file_source, token_estimate

    Raises:
        FileNotFoundError: Profile oder File fehlt
        ValueError: Frame-ID nicht gefunden
    """
    text = _load_profile_section(profile_name, "diagnostic_frames")

    # Pattern: Adorno verwendet "## A1 — name", andere "### Frame F1.1 — name"
    patterns = [
        rf"^### Frame {re.escape(frame_id)} .*?(?=^### Frame |^## Frame-Anwendungs|^## Konstellations-Anwendungs|\Z)",
        rf"^## {re.escape(frame_id)} .*?(?=^## A\d+ |^## Konstellations-Anwendungs|^## Frame-Anwendungs|\Z)",
    ]
    for p in patterns:
        m = re.search(p, text, re.DOTALL | re.MULTILINE)
        if m:
            body = m.group(0).strip()
            return {
                "profile_name": profile_name,
                "frame_id": frame_id,
                "body": body,
                "file_source": "diagnostic-frames.md or konstellations-anker.md",
                "token_estimate": len(body) // 4,  # rough char-to-token
                "lookup_type": "frame",
            }
    raise ValueError(f"Frame '{frame_id}' nicht in Profile '{profile_name}' gefunden")


def lookup_ap(profile_name: str, ap_id: str) -> dict:
    """
    Lookup eines spezifischen Anti-Patterns aus einem Profile.

    Args:
        profile_name: Profile-Short-Name oder Full-Name
        ap_id: AP-ID (z.B. "AP-01", "AP-A05", "AP-T10")

    Returns:
        dict mit profile_name, ap_id, body, file_source, token_estimate
    """
    text = _load_profile_section(profile_name, "anti_patterns")

    # Pattern: ## AP-01: ... oder ## AP-A05: ... oder ## AP-T10: ...
    pattern = rf"^## {re.escape(ap_id)}:.*?(?=^## AP-|^## Cross-AP|^## Anwendungs|\Z)"
    m = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    if not m:
        raise ValueError(f"AP '{ap_id}' nicht in Profile '{profile_name}' gefunden")

    body = m.group(0).strip()
    return {
        "profile_name": profile_name,
        "ap_id": ap_id,
        "body": body,
        "file_source": "anti-patterns.md",
        "token_estimate": len(body) // 4,
        "lookup_type": "ap",
    }


def lookup_question(
    profile_name: str,
    frame_id: Optional[str] = None,
    round_type: Optional[str] = None,
) -> list:
    """
    Lookup von Diagnose-Fragen, optional gefiltert nach Frame oder Round-Type.

    Args:
        profile_name: Profile-Short-Name oder Full-Name
        frame_id: Optional Frame-ID-Filter
        round_type: Optional Round-Type-Filter (initial-advice / counter / re-sync / decision-lock / pre-patch)

    Returns:
        list of dicts mit question, frame_ref (falls vorhanden), round_type (falls vorhanden)
    """
    text = _load_profile_section(profile_name, "question_bank")

    # Wenn frame_id: nur Sektion dieses Frames
    if frame_id:
        section_pattern = rf"^## Frame {re.escape(frame_id)} .*?(?=^## )|^## A{re.escape(frame_id[1:]) if frame_id.startswith('A') else 'NEVER'} .*?(?=^## )"
        sm = re.search(section_pattern, text, re.DOTALL | re.MULTILINE)
        if not sm:
            return []
        scope = sm.group(0)
    else:
        scope = text

    # Fragen-Pattern: nummerierte Liste
    question_blocks = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*\n((?:[ \t]+\*.+?\n?)*)", scope, re.MULTILINE)
    results = []
    for q_text, q_meta in question_blocks:
        meta_dict = {}
        for line in q_meta.split("\n"):
            line = line.strip().lstrip("*").strip()
            if line.startswith("Round:") or line.startswith("*Round:*"):
                meta_dict["round_type"] = line.split(":", 1)[-1].strip().rstrip("*")
            elif line.startswith("Werkphase:") or line.startswith("*Werkphase:*"):
                meta_dict["werkphase"] = line.split(":", 1)[-1].strip().rstrip("*")
            elif line.startswith("AP-Bezug:") or line.startswith("*AP-Bezug:*"):
                meta_dict["ap_ref"] = line.split(":", 1)[-1].strip().rstrip("*")
        # Round-Type-Filter
        if round_type and meta_dict.get("round_type", "").strip("*") != round_type:
            continue
        results.append({
            "question": q_text.strip(),
            "frame_ref": frame_id,
            **meta_dict,
        })
    return results


def lookup_workflow_pass(profile_name: str, workflow_id: str, pass_n: Optional[int] = None) -> dict:
    """
    Lookup eines spezifischen Workflows oder Workflow-Passes.

    Args:
        profile_name: Profile-Short-Name oder Full-Name
        workflow_id: Workflow-ID (z.B. "W-01", "W-A-Multi", "W-F-Genea", "W-A-Triangulate")
        pass_n: Optional Pass-Nummer (1-4 für Multi-Pass-Workflows)

    Returns:
        dict mit profile_name, workflow_id, pass_n, body, token_estimate
    """
    text = _load_profile_section(profile_name, "workflows")

    # Workflow-Block extrahieren
    pattern = rf"^## {re.escape(workflow_id)}[: ].*?(?=^## W-|^## Workflow-Anwendungs|\Z)"
    m = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    if not m:
        raise ValueError(f"Workflow '{workflow_id}' nicht in Profile '{profile_name}' gefunden")

    block = m.group(0).strip()

    if pass_n is None:
        return {
            "profile_name": profile_name,
            "workflow_id": workflow_id,
            "pass_n": None,
            "body": block,
            "token_estimate": len(block) // 4,
            "lookup_type": "workflow_full",
        }

    # Pass-Block extrahieren
    pass_pattern = rf"^### Pass {pass_n} .*?(?=^### Pass \d+|^\*\*Output-Format|^\*\*Linkage|\Z)"
    pm = re.search(pass_pattern, block, re.DOTALL | re.MULTILINE)
    if not pm:
        raise ValueError(f"Pass {pass_n} nicht in Workflow '{workflow_id}' gefunden")

    pass_body = pm.group(0).strip()
    return {
        "profile_name": profile_name,
        "workflow_id": workflow_id,
        "pass_n": pass_n,
        "body": pass_body,
        "token_estimate": len(pass_body) // 4,
        "lookup_type": "workflow_pass",
    }


def list_available_profiles() -> list:
    """Listet alle verfügbaren Profile in PROFILE_SEARCH_DIRS."""
    profiles = []
    for sd in PROFILE_SEARCH_DIRS:
        if not sd.exists():
            continue
        for entry in sd.iterdir():
            if entry.is_dir() and (entry / "PROFILE.md").exists():
                profiles.append({
                    "name": entry.name,
                    "path": str(entry),
                    "search_dir": str(sd),
                })
    return profiles


def list_frames(profile_name: str) -> list:
    """Listet alle Frame-IDs eines Profile."""
    text = _load_profile_section(profile_name, "diagnostic_frames")
    # Pattern für beide Konventionen
    frames = re.findall(r"^### Frame (F\d+\.\d+) ", text, re.MULTILINE)
    if not frames:
        # Adorno-Style: ## A1 -- ##
        frames = re.findall(r"^## (A\d+) ", text, re.MULTILINE)
    return frames


def list_aps(profile_name: str) -> list:
    """Listet alle AP-IDs eines Profile."""
    text = _load_profile_section(profile_name, "anti_patterns")
    return re.findall(r"^## (AP-[A-Z]?\d+):", text, re.MULTILINE)


def lookup_token_cost_estimate(lookup_results: list) -> dict:
    """
    Aggregiert Token-Cost-Schätzung über mehrere Lookups.

    Vergleicht mit voll-Profile-Aktivierung (~18000 Tokens) als Anti-Kosmetik-Indikator.
    """
    total = sum(r.get("token_estimate", 0) for r in lookup_results)
    full_profile_cost = 18000  # estimate
    savings = max(0, full_profile_cost - total)
    return {
        "total_lookup_tokens": total,
        "full_profile_estimate": full_profile_cost,
        "savings_estimate": savings,
        "savings_pct": round(savings / full_profile_cost * 100, 1) if full_profile_cost > 0 else 0,
        "lookup_count": len(lookup_results),
    }


__all__ = [
    "PROFILE_SEARCH_DIRS",
    "PROFILE_SHORT_NAMES",
    "FILE_ALIASES",
    "lookup_frame",
    "lookup_ap",
    "lookup_question",
    "lookup_workflow_pass",
    "list_available_profiles",
    "list_frames",
    "list_aps",
    "lookup_token_cost_estimate",
]
