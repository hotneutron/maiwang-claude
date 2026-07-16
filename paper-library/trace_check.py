#!/usr/bin/env python3
"""
trace_check.py (overall spike DoD) — prove the two projections trace to ONE committed graph state.

The converged Definition of Done: "one regenerated survey section AND one graph view must be
traceable back to the same committed graph state." This gate:
  1. computes the live sha256 of graph/graph.json;
  2. reads the provenance stamp embedded in render/survey.md and render/brain_map.md;
  3. asserts BOTH stamps equal the live graph sha (so neither projection is stale);
  4. asserts every claim/passage the survey cites still exists in the graph + paper records.

Exit 0 = the DoD holds (projections are faithful to the committed graph).
"""
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph", "graph.json")


def main():
    live = hashlib.sha256(open(GRAPH, "rb").read()).hexdigest()[:16]
    errors = []

    stamps = {}
    for name in ("survey.md", "brain_map.md", "paper_map.md"):
        path = os.path.join(HERE, "render", name)
        if not os.path.exists(path):
            errors.append(f"{name}: not rendered")
            continue
        m = re.search(r"graph\.json@sha256:([0-9a-f]+)", open(path).read())
        stamps[name] = m.group(1) if m else None
        if stamps[name] != live:
            errors.append(f"{name}: provenance {stamps[name]} != live graph {live} (stale render)")

    # Survey citations must still resolve in the graph + paper records.
    g = json.load(open(GRAPH))
    claim_ids = {c["claim_id"] for c in g["claims"]}
    passages = {}
    for f in glob.glob(os.path.join(HERE, "papers", "*.json")):
        p = json.load(open(f))
        passages[p["paper_id"]] = {x["passage_id"] for x in p["passages"]}
    survey = os.path.join(HERE, "render", "survey.md")
    if os.path.exists(survey):
        txt = open(survey).read()
        for cid in re.findall(r"\((C-[A-Z0-9]+-[0-9]+),", txt):
            if cid not in claim_ids:
                errors.append(f"survey cites claim {cid} absent from graph")
        for pid, pas in re.findall(r"source \[([^\s]+)\s+(p\d+)\]", txt):
            if pas not in passages.get(pid, set()):
                errors.append(f"survey cites passage {pid}:{pas} absent from records")

    print(f"Live graph.json sha256:{live}")
    for name, s in stamps.items():
        mark = "✓" if s == live else "✗"
        print(f"  {mark} render/{name} @ {s}")
    if errors:
        print(f"\n{len(errors)} DoD VIOLATION(s):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    print("\nOverall DoD: survey + graph view both trace to the SAME committed graph state. ✓")


if __name__ == "__main__":
    main()
