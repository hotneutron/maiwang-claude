---
artifact_type: findings
authority: structured
generated_by: s6-decision-log
paper_id: local:paper-library-spike
parent_artifacts:
  - .plan/260715-2301-proposal-paper-map-spike-consensus.md
  - paper-library/graph/graph.json
tags: [paper-map, spike, decision-log, s6, idempotency, provenance]
---

# S6 — Spike Decision Log + Storage-Friction Findings

*The measurement record for the S3–S6 spike (local paper-library). Records where each
identity/merge decision was automatic / LLM / manual, and the git-native storage frictions
(D4, gpt's reopen) so storage stays a measured constraint. This is the artifact the converged
plan said the next cross-team exchange should carry — measurement, not prose. Timestamp from
`date`: 2026-07-16 00:39.*

## Graph state measured (from graph/graph.json@sha256:aae86bebeb9cd8b2)

- 12 active claims (9 extraction from the 3 papers; 3 cross-paper inference/synthesis).
- 9 edges: 6 `confirmed`, 2 `proposed`, 1 `superseded`.
- 1 merge (reversible); 1 retired claim retained (`C-SYNTH-4` → `C-SYNTH-1`).

## Identity / merge decision log (S6 core)

| Decision | What | decided_by | Why | Reversible? |
|---|---|---|---|---|
| Claim identity, 9 extraction claims | one claim per (paper, key sentence) | **auto** | 1:1 from study docs, keyed by paper_id+claim_id; no dedup needed | n/a |
| Merge M-1 | `C-SYNTH-4` folded into `C-SYNTH-1` (both state "DSE is the shared vehicle") | **llm** | near-duplicate synthesis claims; I judged them the same idea | yes — `C-SYNTH-4` retained in `retired_claims`, merge is a link |
| Edge E-9 | the superseded edge from the merged claim | **auto** | build remaps merged endpoints to canonical; the stale edge is marked `superseded_by: E-2` | yes |
| Edges E-1..E-6 | cross-paper typed relations | **llm** (proposed) → **manual** (confirmed) | I proposed them as inference; confirmed the 6 I'm confident in | yes — lifecycle flip |
| Edges E-7, E-8 | weaker "priors reduce search cost" links | **llm**, left `proposed` | genuine but lower-confidence; NOT promoted to the truth view | yes |

**Distribution:** auto = claim identity + edge remap; llm = 1 merge + all edge proposals;
manual = the confirm/reject gate on which proposed edges enter the truth view. This matches the
C3 split (LLM proposes, deterministic code + human disposes) and gives the S6 auditability.

## What the code caught that the LLM got wrong (the hardening working)

- **Malformed claim ids.** My first S3 proposals used `C-SYNTH-DSE` / `C-SYNTH-BW` /
  `C-SYNTH-PRIOR`; `build_graph.py`'s schema validation **rejected the build** (pattern
  `^C-[A-Z0-9]+-[0-9]+$` needs a numeric suffix). Fixed to `C-SYNTH-1..4`. This is exactly the
  "LLM hallucinates a shape, code catches it" guarantee — the build could not produce invalid
  state.

## Idempotency + manual-edit findings (S4)

- Building twice from the same proposals yields **byte-identical** `graph.json` (stable id
  ordering, dup-free) — verified by `test_idempotency.py` (SHA match).
- A planted `owner: human` claim **survives regeneration** unchanged — the builder carries
  human-owned claims over and never lets a machine proposal overwrite them. This is S0 gap #2
  (manual-correction ownership) working end to end.

## Projection provenance (S5 / overall DoD)

- Both the survey section and the brain-map graph view carry a
  `graph.json@sha256:<hash>` stamp; `trace_check.py` asserts **both equal the live graph SHA**,
  so a stale projection is a hard failure, not a silent drift. Overall DoD holds: survey + graph
  view trace to the **same committed graph state**.

## Storage friction — the D4 measured constraint (gpt's reopen)

gpt asked the spike to record any git-native query awkward enough to stress the representation.
Observed during S3–S5:

1. **Neighborhood queries are O(edges) scans.** `render brain-map <claim>` filters all edges in
   Python. Fine at 9 edges; at 10^4+ edges a per-claim scan on every render is wasteful — an
   adjacency index (or a real graph store) would matter. **Measured, not fatal at spike scale.**
2. **Merge remap is a full-pass rewrite.** Endpoint remapping rescans every edge per build. Same
   O(n) story; acceptable now.
3. **No transactional multi-file update.** A build touches one `graph.json`, so it's atomic by
   accident (single file). If papers/ + graph/ + render/ ever need a *joint* atomic update,
   git-native flat files give no transaction — a genuine future limit.
4. **JSON diff noise.** Reordering claims would blow up the git diff; the builder's stable sort
   avoids this, but it's a discipline the flat-file store imposes, not one it enforces natively.

**Verdict on D4:** git-native JSON is sufficient for the MVP (all DoDs met on it). The first
real wall is **neighborhood/graph-traversal query cost**, not storage per se — so the storage
decision converts to: *add an in-memory adjacency index first; consider a graph store only if
the corpus reaches a scale where rebuild+scan dominates.* Recorded as a measured constraint, per
gpt's request, rather than a taste argument.

## Cross-team status

- The spike ran **independently** in this repo with its own machinery (schemas, stdlib
  validator, builder, renderers) — divergent by design, so a future cross-check against gpt's
  spike stays meaningful (D5).
- Nothing here amends the shared `claims_index` (C8 honored). Promotion of the semantic-layer
  shape remains gated on D5 (≥2 independent consumers + a cross-check surviving divergent
  machinery).
- Next cross-team artifact from this repo should relay these **spike results** (this doc + the
  graph + renders), not more prose.
