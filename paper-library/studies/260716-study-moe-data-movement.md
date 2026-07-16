---
artifact_type: study
authority: derived
generated_by: s2-import
paper_id: arxiv:2510.05497
topics: [moe/serving, data-movement, wafer-scale, expert-placement, llm-inference]
reading_status: read
reading_tier: 1
claims: [C-MOEDM-1, C-MOEDM-2, C-MOEDM-3]
---

# Study — Patterns behind Chaos: Forecasting Data Movement for Efficient Large-Scale MoE LLM Inference

*Per-paper synthesis (S2 import). Source record: `papers/arxiv-2510.05497.json`. Claims cite
stable passage ids.*

## TL;DR
Large MoE LLMs' random expert selection makes **data movement the dominant bottleneck** in
multi-unit serving. Via data-movement-centric profiling of four 200B–1000B models (24k+
requests), the authors distill six insights, then apply them: 6.6x average speedup on
wafer-scale GPUs, up to 1.25x on existing GPUs via prefill-aware expert placement.

## Key claims (→ brain map)
- **C-MOEDM-1** — MoE random expert selection makes data movement the dominant serving
  bottleneck (the problem). *(evidence: p1.)*
- **C-MOEDM-2** — Temporal+spatial data-movement profiling across four 200B–1000B models yields
  six actionable serving-design insights (the method). *(evidence: p2, p3.)*
- **C-MOEDM-3** — Applying the insights gives 6.6x avg speedup on wafer-scale GPUs and up to
  1.25x on existing GPUs (prefill-aware expert placement) (the result). *(evidence: p4, p5.)*

## Method / evidence
Data-movement-centric profiling (not compute-centric) across 4 SOTA MoE models; systematic
temporal + spatial analysis; verified on both future wafer-scale architectures and existing GPU
systems. Public profiling traces.

## Relations (proposed edges)
- `addresses` MoE serving efficiency; `depends_on` the data-movement-as-bottleneck framing.
- Strong tie to the reader's domains: MoE computation-graph optimization + wafer-scale (up to
  300k-card) scalability, and flow-level simulation of data movement.

## My notes
Directly in the reader's active area (MoE + wafer-scale). The "profile data movement, not
FLOPs" stance is the interesting inversion — candidate `shares_assumption_with` the reader's
network-centric simulation view. Reading tier 1.
