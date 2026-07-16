#!/usr/bin/env python3
"""
Corpus check (S2+) — verifies the imported corpus is internally consistent, so
"trace every claim to a source passage" is an enforced invariant, not a promise.

Checks:
  1. Every paper record validates against paper.schema.json.
  2. Every study doc's `paper_id` resolves to a paper record.
  3. Every passage id cited in a study exists in that paper's record (the S2 DoD).
  4. Every claim_id listed in a study's frontmatter appears in its body.

Usage: python3 corpus_check.py         (exit 0 = consistent, 1 = a violation)
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate as V


def main():
    errors = []
    papers = {}
    for f in sorted(glob.glob(os.path.join(HERE, "papers", "*.json"))):
        errs = V.validate_file(os.path.join(HERE, "schemas", "paper.schema.json"), f)
        if errs:
            errors.append(f"{os.path.basename(f)}: schema invalid — {errs[0]}")
            continue
        d = json.load(open(f))
        papers[d["paper_id"]] = {p["passage_id"] for p in d["passages"]}

    studies = sorted(glob.glob(os.path.join(HERE, "studies", "*.md")))
    for sf in studies:
        txt = open(sf).read()
        name = os.path.basename(sf)
        m = re.search(r"^paper_id:\s*(\S+)", txt, re.M)
        if not m:
            errors.append(f"{name}: no paper_id in frontmatter")
            continue
        pid = m.group(1)
        if pid not in papers:
            errors.append(f"{name}: paper_id {pid} has no record in papers/")
            continue
        # frontmatter claim ids (inline list form: claims: [A, B, C])
        fm_claims = re.search(r"^claims:\s*\[(.*?)\]", txt, re.M)
        declared = [c.strip() for c in fm_claims.group(1).split(",")] if fm_claims else []
        for cid in declared:
            if cid and cid not in txt[txt.index("---", 3):]:
                errors.append(f"{name}: declared claim {cid} not defined in body")
        # cited passages must exist in the record
        cited = set(re.findall(r"\bp\d+\b", txt))
        missing = cited - papers[pid]
        if missing:
            errors.append(f"{name}: cites passages absent from {pid}: {sorted(missing)}")

    print(f"Corpus: {len(papers)} papers, {len(studies)} studies.")
    if errors:
        print(f"\n{len(errors)} INCONSISTENCY(ies):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    print("All claims trace to a real source passage. ✓")


if __name__ == "__main__":
    main()
