---
artifact_type: study
authority: derived
generated_by: s2-import
paper_id: arxiv:2503.23076
topics: [perf-modeling/cpu, ml-for-systems, design-space-exploration, analytical-models]
reading_status: read
reading_tier: 2
claims: [C-CONCORDE-1, C-CONCORDE-2, C-CONCORDE-3]
---

# Study — Concorde: Fast and Accurate CPU Performance Modeling with Compositional Analytical-ML Fusion

*Per-paper synthesis (S2 import). Source record: `papers/arxiv-2503.23076.json`. Claims below
each cite a stable passage id — the traceability atom (S0/argument-mining finding).*

## TL;DR
Cycle-level CPU simulators (gem5) are accurate but far too slow for large design-space
exploration. Concorde learns a fast surrogate by representing a program as **compact
performance distributions** derived from **simple analytical bounds** per microarchitectural
component, then fuses that with ML — reaching ~2% CPI error while being 5+ orders of magnitude
faster.

## Key claims (→ brain map)
- **C-CONCORDE-1** — Cycle-level simulators are prohibitively slow for large-scale DSE (the
  problem). *(evidence: p1, measured/background.)*
- **C-CONCORDE-2** — Compositional analytical bounds per microarch component, fused with ML,
  yield a compact yet rich program-performance representation (the method). *(evidence: p2, p3.)*
- **C-CONCORDE-3** — The surrogate is >5 orders of magnitude faster than a reference cycle-level
  simulator at ~2% average CPI error (the result). *(evidence: p4.)*

## Method / evidence
Analytical models estimate per-component performance bounds → compact distributions → ML fusion
predicts CPI across a large microarch parameter space. Validated on SPEC + open-source +
proprietary benchmarks; enabled a first-of-its-kind fine-grained perf attribution (~150M CPI
evals in ~1h, p5).

## Relations (proposed edges)
- `uses_method` of the analytical-ML-fusion idea; `compares_with` cycle-level simulation (gem5).
- Shares the **"analytical model + ML surrogate for expensive simulation"** motif with the
  reader's own simulation-modeling domain (M4/Accorde-style flow-level surrogates).

## My notes
The compositional analytical-bound representation is the transferable idea: it's the same
"cheap analytical prior shrinks the ML learning problem" pattern used in flow-level network
simulators. Candidate cross-domain claim, not yet corroborated.
