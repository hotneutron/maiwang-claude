#!/usr/bin/env python3
"""
test_idempotency.py (S4 DoD) — prove the builder is idempotent AND preserves manual edits.

Two invariants:
  1. IDEMPOTENT: build twice from the same proposals → byte-identical graph.json (no dup
     accumulation, stable ordering).
  2. MANUAL EDITS SURVIVE: plant a human-owned claim (owner=human) with an edited statement
     into graph.json, rebuild, and confirm the human version is NOT overwritten by the machine
     proposal of the same id.

Runs on a temp copy so it never mutates the committed graph. Exit 0 = both hold.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def _build(cwd):
    r = subprocess.run([sys.executable, os.path.join(cwd, "build_graph.py")],
                       cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout + r.stderr)
    return r.returncode == 0


def main():
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        # Mirror the package into tmp so builds don't touch the committed tree.
        for sub in ("schemas", "graph"):
            shutil.copytree(os.path.join(HERE, sub), os.path.join(tmp, sub))
        for f in ("validate.py", "build_graph.py"):
            shutil.copy(os.path.join(HERE, f), os.path.join(tmp, f))
        graph_path = os.path.join(tmp, "graph", "graph.json")
        if os.path.exists(graph_path):
            os.remove(graph_path)  # start clean

        # ---- Invariant 1: idempotency ----
        assert _build(tmp), "first build failed"
        b1 = open(graph_path, "rb").read()
        assert _build(tmp), "second build failed"
        b2 = open(graph_path, "rb").read()
        idem = b1 == b2
        print(f"  [{'PASS' if idem else 'FAIL'}] idempotent: rebuild is byte-identical")
        ok = ok and idem

        # ---- Invariant 2: manual edits survive regeneration ----
        g = json.loads(b2.decode())
        target = g["claims"][0]["claim_id"]
        EDITED = "HUMAN-EDITED: " + g["claims"][0]["statement"]
        for c in g["claims"]:
            if c["claim_id"] == target:
                c["owner"] = "human"
                c["statement"] = EDITED
        json.dump(g, open(graph_path, "w"), indent=2, ensure_ascii=False)

        assert _build(tmp), "rebuild after manual edit failed"
        g2 = json.load(open(graph_path))
        kept = next((c for c in g2["claims"] if c["claim_id"] == target), None)
        survived = kept is not None and kept.get("owner") == "human" and kept["statement"] == EDITED
        print(f"  [{'PASS' if survived else 'FAIL'}] manual edit on {target} survived rebuild "
              f"(owner=human not overwritten)")
        ok = ok and survived

        # ---- No-dup sanity: claim ids unique after rebuild ----
        ids = [c["claim_id"] for c in g2["claims"]]
        no_dups = len(ids) == len(set(ids))
        print(f"  [{'PASS' if no_dups else 'FAIL'}] no duplicate claim ids after rebuild "
              f"({len(ids)} claims)")
        ok = ok and no_dups

    print("\nS4 DoD:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
