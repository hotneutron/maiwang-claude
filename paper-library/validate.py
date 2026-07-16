#!/usr/bin/env python3
"""
Paper-library reference validator (S1) — zero external deps (pure stdlib).

Validates instance JSON against the LOCAL paper-library schemas. Implements the
draft-07 subset the S1 schemas actually use — no jsonschema install required,
matching the parallax/warrant pure-stdlib philosophy so it runs anywhere.

Supported keywords: type, required, enum, const, pattern, minimum, maximum,
minItems, maxItems, properties, additionalProperties, items, allOf, if/then.

Usage:
  python3 validate.py <schema.json> <instance.json>       # validate one instance
  python3 validate.py --selftest                          # run the fixture suite (S1 DoD)

Exit: 0 = valid / all selftests pass; 1 = invalid / a selftest regressed.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _type_ok(val, t):
    if t == "object":
        return isinstance(val, dict)
    if t == "array":
        return isinstance(val, list)
    if t == "string":
        return isinstance(val, str)
    if t == "integer":
        return isinstance(val, int) and not isinstance(val, bool)
    if t == "number":
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    if t == "boolean":
        return isinstance(val, bool)
    if t == "null":
        return val is None
    return True


def validate(instance, schema, path="$", errors=None):
    """Return a list of error strings ([] = valid)."""
    if errors is None:
        errors = []

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: {instance!r} != const {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} not in enum {schema['enum']}")

    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_type_ok(instance, tt) for tt in types):
            errors.append(f"{path}: type {type(instance).__name__} not in {types}")
            return errors  # further checks assume the type matched

    if isinstance(instance, str):
        pat = schema.get("pattern")
        if pat and not re.search(pat, instance):
            errors.append(f"{path}: {instance!r} does not match pattern {pat}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: {instance} > maximum {schema['maximum']}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: {len(instance)} items < minItems {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: {len(instance)} items > maxItems {schema['maxItems']}")
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(instance):
                validate(item, item_schema, f"{path}[{i}]", errors)

    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}: missing required '{req}'")
        props = schema.get("properties", {})
        addl = schema.get("additionalProperties", True)
        for k, v in instance.items():
            if k in props:
                validate(v, props[k], f"{path}.{k}", errors)
            elif addl is False:
                errors.append(f"{path}: additional property '{k}' not allowed")
            elif isinstance(addl, dict):
                validate(v, addl, f"{path}.{k}", errors)

    for sub in schema.get("allOf", []):
        if "if" in sub:
            cond_errs = validate(instance, sub["if"], path, [])
            if not cond_errs and "then" in sub:
                validate(instance, sub["then"], path, errors)
        else:
            validate(instance, sub, path, errors)

    return errors


def validate_file(schema_path, instance_path):
    schema = json.load(open(schema_path))
    instance = json.load(open(instance_path))
    return validate(instance, schema)


def _jsonschema_passes(schema_path, instance_path):
    """Cross-check oracle: validate with the canonical `jsonschema` lib if available.
    Returns (available, passed). available=False when the lib isn't installed."""
    try:
        import jsonschema  # optional; the stdlib validator is authoritative for the DoD
    except ImportError:
        return False, None
    schema = json.load(open(schema_path))
    instance = json.load(open(instance_path))
    try:
        jsonschema.validate(instance, schema)
        return True, True
    except jsonschema.ValidationError:
        return True, False


# ---- S1 DoD: the validator must ACCEPT the valid fixture and REJECT the malformed one ----
def selftest():
    sch = os.path.join(HERE, "schemas")
    fx = os.path.join(HERE, "fixtures")
    cases = [
        ("paper.schema.json", "paper.valid.json", True),
        ("paper.schema.json", "paper.invalid.json", False),
        ("edges.schema.json", "edges.valid.json", True),
        ("edges.schema.json", "edges.invalid.json", False),
    ]
    ok = True
    xcheck_seen = False
    for schema, inst, should_pass in cases:
        spath = os.path.join(sch, schema)
        ipath = os.path.join(fx, inst)
        errs = validate_file(spath, ipath)
        passed = len(errs) == 0
        verdict = "PASS" if passed == should_pass else "REGRESSED"
        if passed != should_pass:
            ok = False
        exp = "accept" if should_pass else "reject"
        # Optional cross-check against canonical jsonschema: it must AGREE with the
        # stdlib validator's accept/reject verdict (guards subset-semantics drift).
        available, js_passed = _jsonschema_passes(spath, ipath)
        xtag = ""
        if available:
            xcheck_seen = True
            if js_passed != passed:
                ok = False
                xtag = f"  [XCHECK-DISAGREE: jsonschema {'accepted' if js_passed else 'rejected'}]"
            else:
                xtag = "  [xcheck ✓]"
        print(f"  [{verdict}] {schema} vs {inst}: expected to {exp}, "
              f"{'accepted' if passed else f'rejected ({len(errs)} err)'}{xtag}")
        if not passed and not should_pass:
            print(f"        first error: {errs[0]}")
    if not xcheck_seen:
        print("  (jsonschema not installed — stdlib validator only; cross-check skipped)")
    return ok


def main():
    if "--selftest" in sys.argv:
        print("S1 validator selftest (DoD: accept valid, reject malformed):")
        sys.exit(0 if selftest() else 1)
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    errs = validate_file(sys.argv[1], sys.argv[2])
    if errs:
        print(f"INVALID — {len(errs)} error(s):")
        for e in errs:
            print(f"  ✗ {e}")
        sys.exit(1)
    print("VALID ✓")


if __name__ == "__main__":
    main()
