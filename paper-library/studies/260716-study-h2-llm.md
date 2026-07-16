---
artifact_type: study
authority: derived
generated_by: s2-import
paper_id: doi:10.1145/3695053.3731008
topics: [llm-inference/edge, hybrid-bonding, near-memory-processing, dataflow, design-space-exploration]
reading_status: read
reading_tier: 2
claims: [C-H2LLM-1, C-H2LLM-2, C-H2LLM-3]
---

# Study — H2-LLM: Hardware-Dataflow Co-Exploration for Heterogeneous Hybrid-Bonding-based Low-Batch LLM Inference

*Per-paper synthesis (S2 import). Source record: `papers/doi-10.1145-3695053.3731008.json`.
Claims cite stable passage ids.*

## TL;DR
Edge low-batch LLM inference needs near-memory processing, but in-die NMP has limited compute
capacity. H2-LLM uses **hybrid-bonding** to rebalance the compute/bandwidth trade-off, adds a
**data-centric dataflow abstraction**, and uses a **DSE framework** to auto-find the optimal
design — 2.72x geomean speedup and 1.48x better energy vs in-die NMP heterogeneous accelerators.

## Key claims (→ brain map)
- **C-H2LLM-1** — In-die NMP designs have limited compute capacity, restricting edge-side
  low-batch LLM acceleration (the problem). *(evidence: p2.)*
- **C-H2LLM-2** — A hybrid-bonding heterogeneous architecture + data-centric dataflow
  abstraction + DSE framework co-explores hardware and dataflow (the method). *(evidence: p3, p4.)*
- **C-H2LLM-3** — H2-LLM achieves 2.72x geomean speedup and 1.48x geomean better energy
  efficiency vs in-die NMP heterogeneous accelerators (the result). *(evidence: p5.)*

## Method / evidence
Extract the hybrid-bonding architecture design space; a data-centric dataflow abstraction;
automated DSE over the whole space to find the optimal point. Open-sourced DSE framework.

## Relations (proposed edges)
- `addresses` edge LLM inference; `uses_method` DSE (shared with Concorde's DSE motivation);
  `compares_with` in-die NMP accelerators.
- Cross-paper: **both H2-LLM and Concorde motivate DSE frameworks** — a `shares_assumption_with`
  edge (DSE is the enabling tool), from opposite sides (H2-LLM builds one for hardware; Concorde
  makes the per-point evaluation cheap enough to run one).

## My notes
The DSE connection to Concorde is the most interesting cross-paper edge: Concorde attacks the
"each DSE point is too slow to evaluate" problem; H2-LLM *is* a DSE over a hardware/dataflow
space. Candidate `shares_assumption_with` on "DSE is the design vehicle."
