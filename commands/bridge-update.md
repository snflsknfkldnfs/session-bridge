# /bridge-update

NEU v0.1.5 (PB-013) — Post-Init Korrektur einzelner state-Felder ohne Re-Init.

## Argumente

| Flag | Pflicht | Beschreibung |
|---|---|---|
| `--field=<topic\|expertise-source\|worker-focus\|domain-hint>` | ja | Feld zum Update (whitelisted) |
| `--value="<new-value>"` | ja | Neuer Wert |
| `--shared-path=<absolute-path>` | nein | Default: aktuelles Working-Dir |

## Pre-Flight

1. `bridge/state.json` existiert + Schema-Validate PASS (via `tools/bridge_state.py:read_state` + `:validate_against_schema`)
2. This_session_id ∈ {state.roles.advisor.session_id, state.roles.worker.session_id} (oder pending-attach-Sentinel)
3. State.phase ∈ {init, scope-lock, iterate} — NICHT execute/verify/close (wuerde Decision-Log brechen)
4. `--field` ist whitelisted: topic | expertise-source | worker-focus | domain-hint
5. `--value` ist non-empty + valid (z.B. domain-hint muss Enum-Member sein per Phase G)

## Ablauf

```python
from tools.bridge_state import read_state, write_atomic_cas, validate_against_schema

# 1. State-Read + CAS-init
state = read_state(shared_path)
read_at = state["updated_at"]

# 2. Pre-Flight 4: Field-Whitelist
WHITELIST = {"topic", "expertise-source", "worker-focus", "domain-hint"}
if args.field not in WHITELIST:
    abort(f"Pre-Flight 4 FAIL: --field='{args.field}' nicht whitelisted (erlaubt: {WHITELIST})")

# 3. Feld-Update via Mapping
field_map = {
    "topic": ("topic", None),                                          # top-level
    "expertise-source": ("roles.advisor.expertise_source", "advisor"), # role-specific
    "worker-focus": ("roles.worker.current_focus", "worker"),
    "domain-hint": ("topic_metadata.domain_hint", None)                # PB-007 v0.1.5
}
path, role_check = field_map[args.field]
# ... (apply path-update)

# 4. status_observations[] Update-Trail (Pflicht)
state.setdefault("status_observations", []).append({
    "type": "bridge_update",
    "field": args.field,
    "old_value": old_val,
    "new_value": args.value,
    "by": this_role,
    "timestamp": now_iso()
})

# 5. Validate post-update + Atomic-CAS
errors = validate_against_schema(state)
if errors:
    abort(f"Post-Update Schema-Validate FAIL: {errors}")
write_atomic_cas(shared_path, state, expected_updated_at=read_at)
```

## Output (Pflicht-Marker per F-RP-29-Disziplin)

```
============================================================
BRIDGE-UPDATE COMPLETED
============================================================
field:             <field>
old_value:         <old>
new_value:         <new>
state.updated_at:  <new-timestamp>
============================================================
```

## Akzeptanz

- state.json updated mit neuem Feld-Wert
- status_observations[] Update-Trail-Eintrag (Pflicht)
- Schema-Validate post-Update PASS

## Anti-Pattern

- NICHT in phase ∈ {execute, verify, close} aufrufen — Decision-Log-Bruch-Risk
- NICHT --field ausserhalb Whitelist akzeptieren — Sicherheits-Risk fuer state-Schema-Verletzung
- NICHT ohne status_observations-Entry persistieren — Update-Trail-Verlust

## Use-Cases

**1. Topic-Mismatch-Korrektur post-init** (p3-Empirie):
```
/bridge-update --field=topic --value="bridge-plugin development (revidiert)"
```

**2. Domain-Hint nachtraeglich setzen** (PB-007 v0.1.5):
```
/bridge-update --field=domain-hint --value=plugin-self-dev
```

**3. Worker-Focus-Update (Phase-Wechsel im Worker-Project):**
```
/bridge-update --field=worker-focus --value="phase-2.3 implementation"
```

## Cross-Refs

- PB-013 v0.1.5 Implementation
- ADR_0029 §13.2 Concurrency (Atomic-CAS)
- tools/bridge_state.py (Library-Foundation v0.1.5 Phase B.1)
- ADR_0031 §4.2 / PB-007 (domain-hint via Phase G)

---

**Status:** v0.1.5 Phase B.2 implementation pending. Pseudocode-Spec ready, full implementation in v0.1.5+ Plugin-Code.
