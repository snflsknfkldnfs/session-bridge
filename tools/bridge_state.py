#!/usr/bin/env python3
"""
tools/bridge_state.py — session-bridge Shared State-Library v0.1.5 (PB-012).

Eliminiert Code-Duplication ueber 5 Commands (bridge-init, bridge-attach,
bridge-handover, bridge-status, bridge-close). Pseudocode in MD-Dateien
wird durch echte Library-Aufrufe ersetzt.

API:
- read_state(shared_path) -> dict
- write_atomic_cas(shared_path, state, expected_updated_at) -> bool
- validate_against_schema(state) -> list[str]  # error messages, empty if valid
- pending_attach_replace(state, role, real_session_id, worker_focus=None) -> dict
- append_round(state, round_data) -> dict
- archive_shared_artifact(state, path) -> dict
- calibrate_wallclock_post_hoc(state, phases) -> dict

Schema-Cross-Refs:
- bridge_state_v1.json (state-Schema, v1.0.0..v1.2.0)
- handover_frontmatter_v1.json (handover-Schema)
- bilanz_v1.json (Bilanz-Schema, NEU v0.1.4)
- mapping_decisions_v1.json (Mapping-Decisions-Schema, NEU v0.1.4)
"""

import json
import os
import re
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# --- Constants ---
SENTINEL_PENDING_ATTACH = "pending-attach"
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = PLUGIN_ROOT / "schemas"
STATE_SCHEMA_PATH = SCHEMAS_DIR / "bridge_state_v1.json"


def _now_iso() -> str:
    """ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _state_path(shared_path: str) -> Path:
    """Compute state.json path from shared-path."""
    return Path(shared_path) / "bridge" / "state.json"


def read_state(shared_path: str) -> dict:
    """Read state.json from shared-path. Raises FileNotFoundError if missing."""
    p = _state_path(shared_path)
    if not p.exists():
        raise FileNotFoundError(f"state.json missing at {p}")
    with p.open() as f:
        return json.load(f)


def write_atomic_cas(shared_path: str, state: dict, expected_updated_at: str) -> bool:
    """
    Atomic compare-and-swap write. Returns True if write succeeded,
    False if expected_updated_at mismatch (CAS-FAIL).

    Uses POSIX-atomic rename via temp file. Pre-Atomic-Backup als
    state.json.bak.<timestamp> per ADR_0029 §13.3 Failure-Recovery.
    """
    state_p = _state_path(shared_path)
    if state_p.exists():
        with state_p.open() as f:
            current = json.load(f)
        if current.get("updated_at") != expected_updated_at:
            return False
        # Pre-Atomic-Backup
        backup_p = state_p.parent / f"state.json.bak.{_now_iso().replace(':', '')}"
        backup_p.write_text(state_p.read_text())

    # Atomic-Write via temp + rename
    state["updated_at"] = _now_iso()
    tmp_uuid = uuid.uuid4().hex[:8]
    tmp_p = state_p.parent / f"state.json.tmp.{tmp_uuid}"
    tmp_p.parent.mkdir(parents=True, exist_ok=True)
    with tmp_p.open("w") as f:
        json.dump(state, f, indent=2)
    os.rename(tmp_p, state_p)
    return True


def validate_against_schema(state: dict, schema_path: Optional[Path] = None) -> list:
    """
    Validate state against bridge_state_v1.json (or other schema).
    Returns list of error messages (empty if valid).
    Requires jsonschema library; returns ["jsonschema-not-available"] if missing.
    """
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema-not-available"]

    if schema_path is None:
        schema_path = STATE_SCHEMA_PATH

    with schema_path.open() as f:
        schema = json.load(f)

    errors = []
    validator = jsonschema.Draft7Validator(schema)
    for err in validator.iter_errors(state):
        errors.append(f"{'.'.join(str(p) for p in err.absolute_path) or 'root'}: {err.message}")
    return errors


def pending_attach_replace(
    state: dict,
    role: str,
    real_session_id: str,
    worker_focus: Optional[str] = None
) -> dict:
    """
    Replace pending-attach Sentinel mit real session_id. Per D-004 R23-Revidierung
    (v0.1.3): Sentinel-Invariante; bridge-attach Pre-Flight 4 strict-mode.

    Returns updated state. Caller responsible for atomic write.
    Raises ValueError if state.roles.<role>.session_id != SENTINEL_PENDING_ATTACH.
    """
    if role not in state.get("roles", {}):
        raise ValueError(f"role {role} not in state.roles")

    role_data = state["roles"][role]
    if role_data.get("session_id") != SENTINEL_PENDING_ATTACH:
        raise ValueError(
            f"Pre-Flight 4 FAIL: expected '{SENTINEL_PENDING_ATTACH}', "
            f"found '{role_data.get('session_id')}' (D-004 strict-mode v0.1.3+)"
        )

    role_data["session_id"] = real_session_id
    role_data["active_since"] = _now_iso()
    if worker_focus is not None:
        role_data["current_focus"] = worker_focus
    if role == "worker":
        # Initial worker.phase per F-RP-26 v0.1.4 Phase A.2
        role_data.setdefault("phase", "kickoff")

    state["roles"][role] = role_data
    return state


def append_round(state: dict, round_data: dict) -> dict:
    """
    Append round to state.rounds[] + auto-increment current_round + update updated_at.
    Per ADR_0029 §13.2 Round-Counter-Atomicity: NIE current_round ohne entsprechenden Append.

    round_data must contain: round, type, initiator, artifact_path, timestamp.
    Auto-propagiert worker.phase aus round_data.frontmatter.worker_phase falls
    initiator=worker (F-RP-26 Auto-Propagation v0.1.4 Phase A.2).
    """
    required_round_keys = {"round", "type", "initiator", "artifact_path", "timestamp"}
    missing = required_round_keys - set(round_data.keys())
    if missing:
        raise ValueError(f"round_data missing keys: {missing}")

    state.setdefault("rounds", []).append(round_data)
    state["current_round"] = round_data["round"]
    state["updated_at"] = _now_iso()

    # Auto-Propagation worker.phase (F-RP-26 v0.1.4)
    if round_data.get("initiator") == "worker":
        wp = round_data.get("frontmatter", {}).get("worker_phase")
        if wp and "worker" in state.get("roles", {}):
            state["roles"]["worker"]["phase"] = wp

    return state


def archive_shared_artifact(state: dict, path: str) -> dict:
    """
    Markiere shared_artifact als 'closed-active' (Pair-Close-Aktion per ADR_0029 §5.6).
    Returns updated state. Raises ValueError if path not in shared_artifacts.
    """
    artifacts = state.get("shared_artifacts", [])
    found = False
    for art in artifacts:
        if art.get("path") == path:
            art["status"] = "closed-active"
            art["round_closed"] = state.get("current_round")
            found = True
            break
    if not found:
        raise ValueError(f"shared_artifact path={path} not found in state")
    return state


def calibrate_wallclock_post_hoc(state: dict, phases: list) -> dict:
    """
    Post-hoc-Kalibrierung wallclock-drift_factors per Phase. phases ist Liste von
    {phase, rounds_range, estimated_rounds, actual_rounds, note}.
    drift_factor = actual / estimated.

    Per ADR_0030 Annex A (v0.1.3): scope-lock-Phase mit Profile-Pin braucht 2-3x
    mehr Rounds als ADR_0029-Default; Empirie via post-hoc-Kalibrierung dokumentiert.
    """
    calibrated = []
    for phase_data in phases:
        est = phase_data["estimated_rounds"]
        act = phase_data["actual_rounds"]
        drift = act / est if est > 0 else float("inf")
        calibrated.append({
            "phase": phase_data["phase"],
            "rounds_range": phase_data.get("rounds_range", ""),
            "estimated_rounds": est,
            "actual_rounds": act,
            "drift_factor": round(drift, 2),
            "note": phase_data.get("note", "")
        })
    state["wallclock_estimates"] = calibrated
    return state




# ============================================================
# v0.1.5 Phase H + D — Lifecycle-Robustheit
# ============================================================

def validate_bilanz_against_schema(bilanz: dict, schema_path: Optional[Path] = None) -> list:
    """
    Validate Bilanz-File gegen schemas/bilanz_v1.json (NEU v0.1.5 Phase H, PB-001 follow-up).
    Per ADR_0031 §4.3: bridge-close enforced bilanz_v1-Schema.
    Returns list of errors (empty if valid).
    """
    if schema_path is None:
        schema_path = SCHEMAS_DIR / "bilanz_v1.json"
    return validate_against_schema(bilanz, schema_path)


# Drift-Plausibility-Ranges per Domain-Klasse (ADR_0031 §3.2 Empirie)
# v0.1.9 Update: use-case-Ranges empirisch kalibriert mit n=4 Pairs
# (p4 RT-4 0.10 / p5 RT-2 0.21 / p7 RT-2 0.23 / p8 RT-1 0.05 — Tooling-Effizienz-Pattern-Cycles)
DRIFT_RANGES = {
    "plugin-self-dev": {"min": 0.8, "max": 3.5, "stddev": 0.6},  # p3-Empirie 1.14-2.4
    "use-case": {"min": 0.05, "max": 2.0, "stddev": 0.4},        # v0.1.9 NEU: p4-p8-Empirie n=4, drift 0.05-0.23 + p3-Range 0.4-2.0
    "use-case-with-profile": {"min": 0.05, "max": 2.0, "stddev": 0.4},  # v0.1.9 NEU: Klafki-Profile p7 + Profile-aktiv-Pairs
    "default": {"min": 0.05, "max": 2.5, "stddev": 0.5},
}


def check_drift_plausibility(domain_hint: Optional[str], drift_factor: float) -> dict:
    """
    NEU v0.1.5 Phase D.1 (PB-009).
    Prueft drift_factor gegen Domain-Range. Bei Abweichung > 2x stddev: WARN.

    Returns: {"status": "OK"|"WARN", "expected_range": ..., "diagnosis": ...}
    """
    domain = domain_hint or "default"
    ranges = DRIFT_RANGES.get(domain, DRIFT_RANGES["default"])

    in_range = ranges["min"] <= drift_factor <= ranges["max"]
    # 2x-stddev-Outlier-Check (annaehernd)
    midpoint = (ranges["min"] + ranges["max"]) / 2
    deviation = abs(drift_factor - midpoint)
    is_outlier = deviation > 2 * ranges["stddev"]

    if in_range and not is_outlier:
        return {"status": "OK", "expected_range": ranges, "diagnosis": "drift in range"}
    return {
        "status": "WARN",
        "expected_range": ranges,
        "diagnosis": f"drift_factor {drift_factor} ausserhalb 2-stddev-Range fuer domain={domain}. Manuelle Stichprobe empfohlen."
    }


# Reflection-Action-Ratio Thresholds per Domain (ADR_0031 §4.1 Decision)
# v0.1.9 Update: use-case-with-profile empirisch kalibriert (p7-klafki-validation 8 Rounds + p8-self-sustained-ux 10 Rounds)
RATIO_THRESHOLDS = {
    "plugin-self-dev": 15.0,                  # p3-Empirie 12.5
    "use-case": 4.0,                          # p4+p5+p6 0.67-2.00, default
    "architecture-spec": 4.0,                 # Sub-Pattern p5
    "investigation-trace": 4.0,               # Sub-Pattern p4
    "methodology-improvement": 5.0,           # Sub-Pattern p6 (early-stage)
    "use-case-with-profile": 5.0,             # v0.1.9 EMPIRISCH validiert: p7-klafki Decision-Lock-Density 1.1/Round, p8 0.9/Round
    "default": 4.0,
}


def compute_reflection_action_ratio(state: dict) -> float:
    """
    NEU v0.1.5 Phase D.2 (PB-002).
    Berechnet Reflection-Action-Ratio per ADR_0031 §2 Klassifikation.

    Reflection = counter, re-sync, status, question
    Action = execute, verify, decision-lock, pre-flight, pre-patch, initial-advice
    """
    REFLECTION_TYPES = {"counter", "re-sync", "status", "question"}
    ACTION_TYPES = {"execute", "verify", "decision-lock", "pre-flight", "pre-patch", "initial-advice"}

    rounds = state.get("rounds", [])
    refl = sum(1 for r in rounds if r.get("type") in REFLECTION_TYPES)
    act = sum(1 for r in rounds if r.get("type") in ACTION_TYPES)
    return refl / act if act > 0 else float("inf")


def check_ratio_threshold(state: dict, ratio: Optional[float] = None) -> dict:
    """
    NEU v0.1.5 Phase D.2 (PB-002).
    Domain-aware Threshold-Check per ADR_0031 §4.1.
    Lookup via state.topic_metadata.domain_hint (PB-007 v0.1.5 Phase G).

    Returns: {"status": "OK"|"WARN", "ratio": float, "threshold": float, "domain": str}
    """
    if ratio is None:
        ratio = compute_reflection_action_ratio(state)

    domain = state.get("topic_metadata", {}).get("domain_hint", "default")
    threshold = RATIO_THRESHOLDS.get(domain, RATIO_THRESHOLDS["default"])

    status = "WARN" if ratio > threshold else "OK"
    return {
        "status": status,
        "ratio": round(ratio, 2),
        "threshold": threshold,
        "domain": domain,
        "diagnosis": (
            f"R/A-ratio {round(ratio, 2)} ueberschreitet Threshold {threshold} fuer domain={domain}. "
            "Lifecycle-Health-Alert: Pair tendiert zu Negotiations-Inflation."
        ) if status == "WARN" else "ratio in expected range"
    }

# --- v0.1.8 Pre-Flight Auto-Resolution Helpers ---

# Profile-Kurz-Name-Mapping (NEU v0.1.8) — User-friendly Aliases
PROFILE_SHORT_NAMES = {
    "klafki": "klafki-didaktik",
    "adorno": "adorno-halbbildung-kritik",
    "foucault": "foucault-genealogie",
    "luhmann": "luhmann-erziehungssystem",
    "process-consulting": "process-consulting",
    "process": "process-consulting",
}

# Standard-Lookup-Verzeichnisse für Profile
PROFILE_SEARCH_DIRS = [
    Path.home() / "session-bridge" / "private-notes" / "expertise-profiles",
    Path.home() / "session-bridge" / "expertise-profiles",
]


def _slugify_topic(topic: str, max_len: int = 30) -> str:
    """Topic → URL-safe slug (lowercase, dashes, no special chars, max_len)."""
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    return slug[:max_len].rstrip("-")


def _next_pilot_id(base_dir: Path) -> int:
    """Scan pilot-runs/ for highest p<N>-* folder, return N+1."""
    if not base_dir.exists():
        return 1
    max_n = 0
    pattern = re.compile(r"^p(\d+)-")
    for entry in base_dir.iterdir():
        if entry.is_dir():
            m = pattern.match(entry.name)
            if m:
                max_n = max(max_n, int(m.group(1)))
    return max_n + 1


def resolve_shared_path_default(
    topic: str,
    base_dir: Optional[Path] = None,
) -> Path:
    """
    Generate default shared-path for new bridge-pair (v0.1.8 Pre-Flight A.1).

    Pattern: <base_dir>/p<auto-id>-<topic-slug>/

    Args:
        topic: Bridge-Topic für slug-Generation
        base_dir: pilot-runs/ Verzeichnis (default: ~/session-bridge/pilot-runs/)

    Returns:
        Path object für vorgeschlagenen shared-path (NICHT erstellt)
    """
    if base_dir is None:
        base_dir = Path.home() / "session-bridge" / "pilot-runs"
    base_dir.mkdir(parents=True, exist_ok=True)
    next_n = _next_pilot_id(base_dir)
    slug = _slugify_topic(topic)
    return base_dir / f"p{next_n}-{slug}"


def resolve_profile_path(
    profile_arg: str,
    search_dirs: Optional[list] = None,
) -> Path:
    """
    Resolve profile argument to absolute path (v0.1.8 Pre-Flight A.2).

    Resolution order:
    1. Absolute path → as-is (verify exists)
    2. Short-name (in PROFILE_SHORT_NAMES) → expand + lookup
    3. Relative or partial-name → glob-match in search_dirs

    Args:
        profile_arg: User-Eingabe (absolut / kurz-name / relativ / partial)
        search_dirs: Lookup-Verzeichnisse (default: PROFILE_SEARCH_DIRS)

    Returns:
        Absoluter Path zum Profile-Verzeichnis

    Raises:
        FileNotFoundError: wenn nicht eindeutig auflösbar
        ValueError: wenn multi-match
    """
    if search_dirs is None:
        search_dirs = PROFILE_SEARCH_DIRS

    # Case 1: Absolute path
    p = Path(profile_arg).expanduser()
    if p.is_absolute():
        if p.exists():
            return p
        raise FileNotFoundError(f"Profile-Pfad existiert nicht: {p}")

    # Case 2: Short-name lookup
    expanded = PROFILE_SHORT_NAMES.get(profile_arg, profile_arg)

    # Case 3: Direct + glob lookup in search_dirs
    candidates = []
    for d in search_dirs:
        if not d.exists():
            continue
        # Exact match
        exact = d / expanded
        if exact.exists():
            return exact
        # Glob match (e.g. "klafki" → "klafki-didaktik")
        for match in d.glob(f"{expanded}*"):
            if match.is_dir():
                candidates.append(match)

    if len(candidates) == 0:
        raise FileNotFoundError(
            f"Profile '{profile_arg}' (expanded: '{expanded}') nicht gefunden in {search_dirs}"
        )
    if len(candidates) > 1:
        raise ValueError(
            f"Profile '{profile_arg}' multi-match: {[str(c) for c in candidates]}"
        )
    return candidates[0]


__all__ = [
    "SENTINEL_PENDING_ATTACH",
    "DRIFT_RANGES",
    "RATIO_THRESHOLDS",
    "PROFILE_SHORT_NAMES",
    "PROFILE_SEARCH_DIRS",
    "read_state",
    "write_atomic_cas",
    "validate_against_schema",
    "validate_bilanz_against_schema",
    "pending_attach_replace",
    "append_round",
    "archive_shared_artifact",
    "calibrate_wallclock_post_hoc",
    "check_drift_plausibility",
    "compute_reflection_action_ratio",
    "check_ratio_threshold",
    "resolve_shared_path_default",
    "resolve_profile_path",
]
