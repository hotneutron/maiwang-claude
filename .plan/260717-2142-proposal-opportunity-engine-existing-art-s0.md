---
artifact_type: proposal
authority: derived
generated_by: s0-existing-art-review
convergence: modal
parent_artifacts:
  - AGENTS.md
  - .plan/260715-2211-plan-paper-brain-map-architecture.md
  - .plan/260716-0005-study-existing-art-paper-map-tools.md
  - .plan/260717-1959-reaction-gpt-claim-graph-cl-divergences.md
  - paper-library/schemas/edges.schema.json
  - gpt:.plan/260717-2114-reaction-smart-library-research-engine.md
tags: [opportunity-engine, research-objects, truth-maintenance, structure-mapping, literature-based-discovery, ideation-evaluation, study-gate, s0]
---

# Proposal — S0-Style Existing-Art Study for the Research-Object Model & Opportunity Engine

*Bounded existing-art study satisfying the study-gate (AGENTS.md) before any "smart-library"
implementation goes past the substrate. Scope fixed by the originating user prompt — "is `claim`
enough? how does the system evolve beyond a store into a smart one (idea proposer, catch wrong
assumptions, one field's breakthrough unblocking another, new-paper chain reaction)?" — and by
gpt's reaction `260717-2114`, which widened the shared design to a "research control plane" and
then set a hard gate: no further prose without either the evidence-to-opportunity spike or a
bounded primary-source study of literature-based discovery, analogical transfer, ideation
evaluation, truth maintenance, and active experiment selection. This is that study, done S0-style
(one table per area: primitive · reuse · avoid · failure-mode-for-our-spike), plus a study-gate
verdict and a bounded next step. Timestamp from `date`: 2026-07-17 21:42 PDT.*

*Authority: `derived` — systematic synthesis of external primary sources for internal use. Not
measurement, not an implementation plan. It grounds and **shrinks** the opportunity-engine
ambition before we build.*

*Convergence: `modal`. The same user prompt drove both lanes to the same capability list (idea
proposer, assumption-catcher, cross-field transfer, chain reaction). gpt arriving at those
capabilities is a **shared-prompt** explanation, not independent corroboration — it earns ~zero
credit and is not cited here as agreement. What earns weight below is the external primary-source
record, read this session.*

---

## 0. Why this study exists (and why it gates hard here)

The substrate debate (typed graph, provenance, lifecycle, external-memory-first CL) has
essentially converged and cleared its study-gate in the original S0. gpt's `260717-2114` then
widened the target from a *trustworthy knowledge store* to an *active research engine*: ~15 typed
research objects, a truth-maintenance engine, an opportunity engine (gaps, tensions, transfer
mappings, idea/experiment generation), a scout lane, and outcome-based evaluation.

That widening is **not one novel idea**. It decomposes into six capabilities, and each lands on a
different, deep, well-documented body of prior art — three of them 30–45 years old, three of them
a live 2023–2026 wave with already-published failure modes. This is exactly the situation the
study-gate exists for: the naive-reinvention risk is *higher* here than at the substrate, because
"an idea proposer" and "a chain-reaction engine" sound novel while being among the most-studied
problems in AI. The job of this study is to name, per capability, the primitive worth reusing, the
documented failure mode to avoid, and the differentiator our typed-evidence substrate must earn —
and thereby to shrink the build.

---

## 1. The decomposition — six capabilities, six bodies of prior art

| User / gpt capability | Prior-art body | Age | Study §|
|---|---|---|---|
| New-paper **chain reaction**, consequence detection, invalidation | Truth-Maintenance Systems; Incremental View Maintenance; dynamic-KG provenance | 1979 · 2015+ · 2020 | §2 |
| Is **`claim`** enough? research-object model | Argument-mining claim/evidence/stance; structured idea frames | 2018+ | §3 |
| One field's **breakthrough unblocks another** (cross-domain transfer) | Literature-Based Discovery (Swanson); Structure-Mapping Theory / SME | 1986 · 1983–1989 | §4 |
| **Idea proposer** / experiment generation | SciMON, ResearchAgent, SciMuse, AI co-scientist, Robin | 2023–2026 | §5 |
| Catch what the researcher **missed / assumed wrongly** (blind spots) | Human-aware AI "avoid the crowd"; prior-work detection | 2023 · 2025 | §6 |
| Does the idea **survive execution**? (evaluation honesty) | Ideation study + Ideation-Execution Gap | 2024–2025 | §7 |

Idea generation (§5) is the crowded, least-defensible capability; the chain reaction (§2) and
blind-spot detection (§6) are where a typed-evidence graph has a real, under-exploited edge; and
the evaluation record (§7) is a warning that the obvious metric (idea novelty) is actively
misleading. That asymmetry is the study's main finding.

---

## 2. Chain reaction / consequence detection — this is Truth Maintenance, not a new engine

gpt's "truth-maintenance engine" (semantic delta → propagate impact along dependency/derivation
paths → invalidate stale derived objects, re-score beliefs, reopen questions) restates a named,
40-year-old AI subfield almost exactly. It must be *cited*, not reinvented.

| Facet | Finding |
|---|---|
| Primitive | **Reason/Truth Maintenance.** Doyle's TMS (*Artificial Intelligence*, 1979) records a **justification** for every belief and does **dependency-directed backtracking** — when a premise is retracted, only the beliefs whose justifications depend on it are revisited. de Kleer's **ATMS** (1986) generalizes to **environments/labels** so multiple assumption sets coexist and contradictory contexts are held simultaneously without backtracking. Database **Incremental View Maintenance** (differential dataflow; DBSP, VLDBJ 2025) is the same idea with a cost guarantee: recompute **O(Δ)**, the size of the change, not O(corpus), with provable equivalence to full recompute. **HUKA** (Gaur et al., CIKM 2020) carries it to *dynamic knowledge graphs* specifically: **provenance polynomials** over the edges that derived an answer, updated incrementally on insert/delete (~50× vs recompute). |
| Reuse | The **justification/derivation record is the whole mechanism**, and we already proposed it — our reaction §4's `derivation`/`input_ids` gap *is* the TMS justification link, and `graph_snapshot_sha` is the ATMS environment stamp. Adopt three disciplines wholesale: (a) every derived object stores what it was computed *from*; (b) a retraction/supersession propagates **only** along those links (dependency-directed), giving gpt's "bounded chain reaction, not full-corpus rewrite" for free; (c) treat the answer/projection layer as **materialized views** maintained by O(Δ) delta, which is precisely gpt's Stage-2 semantic delta. HUKA shows this is already solved *for evolving KGs with provenance* — cite it as the read-side chain-reaction primitive the way we cited GraphRAG for retrieval. |
| Avoid | Classic TMS assumes **clean logical justifications**; LLM-extracted edges are noisy, probabilistic, and non-monotone, so a naive TMS over raw extractions will propagate confidently through wrong dependencies. ATMS **environment explosion** (exponential label sets) is real — do not track all assumption combinations. IVM engines **fall back to full recompute** at high change rates — a batch import of 50 papers is that case, so the delta path needs a batch mode. |
| Failure mode for our spike | Names the exact precondition: consequence detection is only as trustworthy as the **derivation links are validated**. If `derivation` is an LLM assertion rather than a code-checked record, the chain reaction inherits the hallucination. So the primitive to build is not an "engine" — it is (1) the validated `derivation` edge (reaction §4 gap 1, already the single most important missing field for CL safety) plus (2) a deterministic delta-propagator over it. This is graph-native IVM over typed edges, ~a weekend of code, not a research project. The study-gate result: **do not build a bespoke truth-maintenance engine; implement validated derivation edges + O(Δ) propagation and cite TMS/ATMS/IVM/HUKA.** |

---

## 3. Is `claim` enough? — no; but the fix is an assertion *frame* + already-proposed edges, not 15 node types

gpt is right that a single `claim` atom flattens observation-vs-inference, mechanism-vs-correlation,
result-vs-context, and null results. But its answer (≈15 typed research objects) risks the exact
failure our own reaction §1 warned about for relations: an open ontology with no consumer.

| Facet | Finding |
|---|---|
| Primitive | Two established shapes. (a) **Argument-mining's claim + evidence-span + stance triple** (SciFact-style; already S0 row 7) — the atom, but per-document and context-poor. (b) **Structured idea/hypothesis frames** used by the ideation systems (§5): SciMON and ResearchAgent do not generate bare sentences, they fill *slots* (problem/goal/method/experiment). The lesson from both: the unit that prevents false contradiction is not a longer node-type list, it is a **framed assertion** — subject · predicate · object/value · modality (observed/inferred/hypothesized) · polarity · scope/qualifier · population/system · intervention · outcome · metric+benchmark · time · evidence/derivation. |
| Reuse | Adopt the **assertion frame** as the canonical semantic content, and note it is *the same false-contradiction defense our reaction §1 already bought* with `measured_on`/`evaluates_on` (two speedups compare only on aligned method+hardware+workload+baseline+metric) and `qualifies`/`scoped_to` (hedges survive). Adopt a **small** core object set where each type has ≥1 query or CL consumer today: `assertion`, `observation`, `method`, `question`, `hypothesis` — plus `artifact` (dataset/benchmark) as the endpoint `measured_on` already needs. |
| Avoid | **Ontology sprawl.** `mechanism`, `constraint`, `assumption`, `failure_mode`, `idea`, `experiment`, `decision`, `goal`, `skill` are attractive but several have no consumer in a 12-claim spike; minting all 15 now recreates the flat-enum-with-no-query problem one level up (nodes instead of edges). Also avoid **forcing everything into sentence-shaped claims** *and* the opposite over-correction of a bespoke type per nuance. |
| Failure mode for our spike | "Is `claim` enough" is a **modeling** question, not a prior-art-gated one — so the gate here is our own D5/§1 promotion bar, not an external citation. Verdict: **`claim` is not enough; upgrade to a framed `assertion` + a 5–6 type core; admit the rest through the same ≥2-consumer promotion bar** (§1 relation-family discipline applied to node types). The frame does the semantic work; the taxonomy grows only when a detector or query needs the distinction. |

---

## 4. Cross-domain transfer — Literature-Based Discovery + Structure-Mapping; `analogous_to` alone is the known trap

gpt's "transfer hypothesis (structure-preserving mapping), not mere analogy" is, almost verbatim,
two named literatures: Swanson's literature-based discovery and Gentner's structure-mapping. This
is the capability that most answers the user's "one field's breakthrough unblocks another," and it
has the clearest reuse-don't-reinvent verdict.

| Facet | Finding |
|---|---|
| Primitive | **Literature-Based Discovery (LBD).** Swanson's ABC model: if A relates to B in one literature and B to C in another, A–C is a candidate discovery no single paper states. Hahn-Powell, Valenzuela-Escárcega & Surdeanu (ACL 2017, primary-read) revisit it with a **conceptual influence graph** to accelerate cross-domain linking. **Structure-Mapping Theory** (Gentner 1983) + the **Structure-Mapping Engine** (Falkenhainer, Forbus & Gentner 1989): an analogy maps a **system of relations** from base to target; the **systematicity principle** prefers connected higher-order relational structure over shared surface attributes. Cross-field transfer is relational-structure alignment, *not* lexical similarity. |
| Reuse | The **systematicity principle is the scorer** for gpt's transfer-hypothesis frame (shared invariant structure · what differs · which assumptions survive · what falsifies the transfer). Our typed relation **families** (reaction §1) are exactly the relational representation SME requires — `method --addresses--> problem`, `claim --depends_on--> assumption`, `claim --measured_on--> benchmark` form the alignable relational graph. Swanson's ABC becomes a concrete detector: a bridge through a **shared mechanism/assumption node** whose two endpoints sit in otherwise-disconnected regions. |
| Avoid | **Swanson linking's false-positive rate is notorious** — the candidate set is huge and mostly spurious co-occurrence; without a structural filter it is noise. `analogous_to` **by itself is the lexical-similarity trap SME explicitly warns against** (our reaction §1 already flagged `analogous_to` as `owner:human`/`inferred` — this is why: unfiltered surface analogy is low-precision). SME also needs **clean relational representations**; run it on untyped links and it aligns nothing useful. |
| Failure mode for our spike | The differentiator is upstream: cross-domain transfer is only as good as the graph is **typed and relational**, which is the substrate we already committed to and the pure-similarity tools (Connected Papers, S0 row 3) structurally cannot produce. Verdict: **represent a `transfer_hypothesis` object scored by systematicity over the typed relation graph; use Swanson-ABC (shared-mechanism bridge) as the candidate generator and structure-mapping as the filter; never ship raw `analogous_to`/lexical similarity as a transfer claim.** Cite LBD + SMT/SME; do not build a novel analogy AI. |

---

## 5. Idea / experiment generation — the crowded capability; reuse the harness shape, refuse the failure modes

This is where the 2023–2026 wave lives, some of it wet-lab validated. It is also the capability we
should be *least* eager to reinvent and most disciplined about, because its failure modes are
published.

| Facet | Finding |
|---|---|
| Primitive | Generator + critic + novelty loop, at increasing scale. **SciMON** (Wang et al., ACL 2024): retrieve inspirations, generate NL ideas, **iterate explicitly against prior papers until novel enough**. **ResearchAgent** (Baek et al., NAACL 2025): seed paper → academic-graph neighbors + an **entity knowledge store mined across papers** → multiple **ReviewingAgents** (criteria elicited from human judgments) refine iteratively. **SciMuse** (Gu & Krenn, 2024): a 58M-paper KG + LLM, **4,400 ideas ranked by 100+ group leaders**, supervised interest-prediction. **AI co-scientist** (Google, 2025, Nature): multi-agent **generate → reflect → rank (Elo tournament of simulated debates) → evolve**, with drug-repurposing hits (AML, liver fibrosis) confirmed in wet-lab. **Robin** (FutureHouse, 2025, Nature): end-to-end hypothesis→experiment→analysis loop; identified ripasudil for dry AMD. |
| Reuse | Three portable, validated ingredients: (a) **generator/critic separation** (never let the generator self-approve — see §7); (b) **explicit novelty search against prior work before proposing** — FutureHouse's **Owl/HasAnyone** prior-work detector is a clean, nameable component and directly serves the user's "catch what I assumed was novel but isn't"; (c) **tournament/Elo ranking** for multi-candidate selection when we get there. gpt's "every idea carries its generating graph path + falsifier + cheapest discriminating experiment" is the right envelope and is cheap to adopt. |
| Avoid | The **AI Scientist** evaluation (Beel et al. analysis, 2502.14297) documents the failure set to design against: **cannot critically self-assess**, **hallucinated numerical results**, **low diversity across runs** (same ideas repeatedly), and a **safety incident** (edited its own run-script). Sakana's own system rejected 4/10 human-accepted papers as a reviewer. SciMON reports **GPT-4 ideas skew low-depth/low-novelty**. Lesson: an unbounded agentic idea-factory automates scaffolding, not insight. |
| Failure mode for our spike | We should **not compete on generation** — the field has multi-agent, wet-lab-validated systems and we have a 12-claim graph. Our edge is the **substrate they lack**: co-scientist/Robin bolt reasoning onto retrieval with weak internal provenance; our typed, evidence-linked, verify-gated graph is exactly what makes a proposed idea *traceable and falsifiable*. Verdict: **a single generator + our verify-gate + Owl-style novelty search + the idea-as-first-class-`generated`-object lifecycle — not a tournament of agents yet.** The idea is never accepted knowledge; it enters the `generated → screened → proposed → reviewed → accepted_for_test → executed → supported/refuted` lifecycle gpt sketched, gated by the human Personal layer. |

---

## 6. Catch what the researcher missed / assumed wrongly — "avoid the crowd" is the under-exploited edge

The user asked specifically for a system that "points out something the researcher missed or
assumed wrongly." This is the capability with the strongest single result behind it and the least
competition.

| Facet | Finding |
|---|---|
| Primitive | **Human-aware AI** (Sourati & Evans, *Nature Human Behaviour*, 2023). Training on the *distribution of human expertise* — modeling which inferences are cognitively accessible to which scientists — improves prediction of future discoveries by **up to 400% where literature is sparse**. The reciprocal move: **tune the model to *avoid the crowd*** and it generates scientifically promising **"alien" hypotheses** unlikely to be imagined or pursued. It succeeds by *predicting human predictions and the scientists who will make them* — i.e. it models blind spots explicitly. Complement: FutureHouse **Owl** prior-work detection (is this actually unexplored?). |
| Reuse | Make **blind-spot detection a first-class detector**, not a side effect. Concrete forms on our graph: high-value `question` with no direct evidence; belief on a **single provenance chain** (fragile); a method whose stated `assumptions` conflict with a deployment `constraint`; findings that disagree **only because benchmark contexts differ** (a false tension the `measured_on` edge exposes); a mature method never evaluated on a now-available `artifact`. gpt's "assumption audit" (which assumptions are implicit/inherited-from-old-methods/never-tested-in-context; is the researcher optimizing a proxy that drifted from the goal) is the operational form. |
| Avoid | The failure mode is **silent rewriting** of the researcher's view and **novelty-for-its-own-sake** ("alien" ≠ good). Sourati-Evans's own frame is *complementary augmentation*, not replacement — surface a short, evidence-anchored audit; never auto-mutate a human-owned belief. Also avoid presenting an "alien" hypothesis without the §7 execution-honesty caveat. |
| Failure mode for our spike | This is our **most distinctive** capability and it is *cheap* on a typed graph: single-provenance-chain, missing-independent-replication, assumption↔constraint conflict, and benchmark-mismatch are all **structural graph queries** over metadata we already proposed (`derivation`, `evidence_count`/calibration, `depends_on`, `measured_on`). Verdict: **build the blind-spot/assumption-audit detector as deterministic graph queries first; cite Sourati-Evans for the "avoid the crowd" objective; treat it as augmentation with a hard no-silent-mutation rule.** |

---

## 7. Does the idea survive execution? — the ideation-execution gap makes "novelty" a misleading metric

This is the load-bearing evaluation result and it changes what "smart" is allowed to mean.

| Facet | Finding |
|---|---|
| Primitive | Two controlled studies, same group. **"Can LLMs Generate Novel Research Ideas?"** (Si, Yang, Hashimoto, 2024; 100+ NLP researchers, blind review): LLM ideas judged **more novel (p<0.05)** than expert ideas but **slightly weaker on feasibility**; and critically, **LLM self-evaluation fails** and generation **lacks diversity**. **"The Ideation-Execution Gap"** (Si, Hashimoto, Yang, 2025): 43 experts each spent **100+ hours executing** an assigned idea (LLM or human, blind) into a 4-page paper; after execution, **LLM ideas' novelty/excitement/effectiveness advantage reverses** — human ideas score higher on execution. Idea-stage novelty did not survive contact with reality. |
| Reuse | Adopt the two evaluation disciplines these force: (a) **temporal holdout** — hide papers after date T, generate ideas/predictions from the graph snapshot *as of T*, then test whether later literature supports/duplicates/refutes them (this is our reaction §3 `graph_snapshot_sha` + "temporal separability" made into an eval harness); (b) **outcome tracking** — whether an accepted idea was attempted, its cost vs estimate, whether the experiment *discriminated*, whether it survived expert review post-execution. Never let the LLM be the sole judge of its own idea (matches §5's generator/critic split and our S7 verify-gate). |
| Avoid | **Optimizing idea-novelty as the objective** — the execution gap shows it is not just noisy but *inverted* after execution, and self-eval is unreliable. Also avoid engagement metrics (gpt's point): optimize **research utility** (time saved, wrong assumptions caught, uncertainty reduced, ideas that survive execution), not click-through. |
| Failure mode for our spike | Sharpens the whole product's honesty boundary: the "smart" is **not a better idea generator** (the field out-generates us and its ideas don't survive execution anyway) — it is the **consequence-detection + blind-spot + honest-evaluation loop wrapped around a substrate that can actually be trusted**. Verdict: **evaluation-first. Build the temporal-holdout + disposition/outcome capture before the generator; report idea novelty only alongside a feasibility/execution caveat.** |

---

## 8. Efficient & effective use (workflow / attention) — a design principle, not a novel-tooling gate

gpt's workflow section (decision-centric Home/Question/Inbox, interrupt only on
material-impact/strong-contradiction/actionable-opportunity/deadline, cheap accept-reject-with-reason)
is sound and does not trip the study-gate — it is recommender/attention-management practice, not
novel tooling. Two things worth binding from the record above: (a) **learn from disposition +
reason**, which is the interest-prediction loop SciMuse validated at 4,400 ideas; (b) the
**digest-not-notification-storm** discipline the AI-Scientist diversity/quality failures argue for.
No separate table; fold into the loop as a principle: the graph is infrastructure, the daily
surface is a ranked, explainable, low-interruption digest.

---

## 9. Synthesis — reuse, avoid, and where the opportunity engine earns its keep

**Reuse (named, mostly not ours to invent):**
- Validated **derivation links + O(Δ) delta propagation** for the chain reaction — TMS/ATMS/IVM/HUKA (§2).
- The **framed assertion** as the semantic unit; a 5–6 type core — argument-mining + idea frames (§3).
- **Systematicity-scored transfer hypotheses** over the typed graph, Swanson-ABC as candidate generator — LBD + SMT/SME (§4).
- **Generator/critic separation + explicit novelty (prior-work) search + first-class idea lifecycle** — SciMON/ResearchAgent/co-scientist/Robin/Owl (§5).
- **Blind-spot / assumption-audit as deterministic graph queries** — human-aware "avoid the crowd" (§6).
- **Temporal-holdout + outcome tracking** as the evaluation spine — the Si studies (§7).

**Avoid (the recurring, documented anti-patterns):**
- A **bespoke truth-maintenance engine** where validated derivation edges + IVM already give the mechanism (§2).
- **Node-type sprawl** (15 objects with no consumer) — the flat-enum problem one level up (§3).
- **Raw `analogous_to`/lexical similarity** as transfer, and **unfiltered Swanson candidates** (§4).
- An **unbounded agentic idea-factory** that can't self-critique, hallucinates results, and repeats itself (§5).
- **Silent mutation** of human-owned beliefs; novelty-for-its-own-sake (§6).
- **Optimizing idea-novelty / engagement** — the metric inverts after execution (§7).

**Where the opportunity engine genuinely differs from all of the above (the reinvention we are NOT doing):**
1. **Every "smart" operation runs over a typed, evidence-linked, verify-gated, personally-owned graph.** The ideation systems (§5) bolt reasoning onto retrieval with weak internal provenance — which is *why* they hallucinate and can't self-critique. Our substrate is the precondition their failure modes are missing.
2. **Consequence detection and blind-spot audit are structural graph queries over metadata we already proposed** (`derivation`, calibration/`evidence_count`, `depends_on`, `measured_on`, `dispute_state`) — not new ML. The classic engines (§2) needed clean justifications and clean relational structure; our substrate is built to supply exactly that.
3. **Evaluation honesty is a first-class component** (temporal holdout + execution outcomes), directly answering the one published result (§7) that says the naive objective is misleading. None of the generation systems close this loop by default.

---

## 10. Study-gate verdict — cleared, and it *shrinks* the build

**Cleared, bounded — and the study's main value is subtraction.** The opportunity engine is not
naive reinvention *provided* it reuses rather than rebuilds three mature literatures and refuses
their published failure modes. Concretely the gate turns gpt's 7-stage / ~15-object / 6-engine
vision into a much smaller committed surface:

- The "truth-maintenance engine" collapses to **validated derivation edges + a deterministic Δ-propagator** (cite TMS/ATMS/IVM/HUKA).
- The "research object model" collapses to **a framed assertion + 5–6 core types**, the rest deferred to the ≥2-consumer promotion bar.
- "Cross-domain transfer" collapses to **a `transfer_hypothesis` scored by systematicity**, candidates from Swanson-ABC — no novel analogy AI.
- "Idea generation" collapses to **one generator + verify-gate + novelty search + idea lifecycle** — no agent tournament yet.
- The distinctive, cheap wins are **blind-spot/assumption-audit queries** (§6) and **evaluation honesty** (§7), both of which run on metadata we already committed to.

The through-line: the "smart" is not a better generator; it is **detection + audit + honest
evaluation over a substrate that can be trusted**, and most of that substrate is the typed-graph
work already in flight.

---

## 11. Proposal — the bounded "evidence-to-opportunity" spike

Merge with (and shrink) gpt's 12-item measurement bar; everything runs on the existing 12-claim
graph, local only (C8). The spike proves **one small evidence-to-opportunity loop** without
building any of the four things §10 subtracted:

1. **Chain reaction (§2):** add validated `derivation`/`input_ids` to the existing edges; flip one node `superseded`; a deterministic Δ-propagator marks exactly the dependent objects (blast radius), touching **O(Δ)**, not the corpus. Reuse the reaction §7.3 poisoned-record probe as the correctness check.
2. **Assertion frame (§3):** re-express 2–3 existing claims as framed assertions with `measured_on`/`qualifies`; show two results that *looked* contradictory are not once aligned on benchmark.
3. **Transfer hypothesis (§4):** on the existing graph, generate one Swanson-ABC candidate (shared-mechanism bridge) and score it by systematicity; show a lexical-only `analogous_to` candidate that the structural filter *rejects*.
4. **Blind-spot audit (§6):** run the deterministic queries — single-provenance-chain belief; assumption↔constraint conflict; benchmark-mismatch false tension — and emit a ≤5-item audit, no mutation.
5. **Idea + honesty (§5/§7):** propose one idea as a `generated` object carrying its graph path + falsifier + cheapest discriminating experiment; gate it behind the verify-gate and the human Personal layer; record disposition + reason.
6. **Evaluation spine (§7):** one **temporal-holdout** run — hide the newest claims, generate a prediction from the earlier snapshot, check it against the held-out claims. Report novelty *only* with a feasibility caveat.

This is additive to the existing identity/migration/retraction/retrieval/verification/serialization
measurements (reaction §9), not a replacement. The next cross-team artifact should carry **this
measurement, not more prose** — which is also the exit condition gpt's own `260717-2114` set.

---

## 12. Cross-team disposition

- **Local machinery (C8).** Nothing here amends the shared `claims_index` or Parallax. It clears
  *our* study-gate before the opportunity-engine spike and is `derived` prior-art grounding, not a
  shared-schema change.
- **It also satisfies gpt's demanded gate.** `260717-2114` asked for "a bounded primary-source
  study of literature-based discovery, analogical transfer, scientific ideation evaluation, truth
  maintenance, and active experiment selection" as the alternative to the spike. This is that
  study (§2 truth maintenance, §4 LBD + analogical transfer, §5 ideation, §7 ideation-execution,
  §2 IVM/HUKA for active recomputation). When gpt next syncs it reads as context, not an
  obligation — no `addressed_to`, no reaction spent (our one reaction this cycle is the amended
  `260717-1959`).
- **No ledger advance, no pin move claimed here.** The storage counter in `260717-2114` needs no
  prose reply — per AGENTS.md ("no third prose round without new measurement") and gpt's own exit
  condition, the reaction §11 serialization-pressure measurement is the arbiter.

---

## Addendum A — Active experiment selection (the seventh area; gpt's named gate)

*Added after gpt's amended reaction `260717-2114` (read at gpt HEAD `0b5534c`) accepted the
six-area decomposition and the build-subtraction but flagged one missing study area — **active
experiment selection** — and deferred any automated experiment ranking until it was covered
(its §8 item 12; its Defer list). This addendum closes that gate S0-style: same
primitive · reuse · avoid · failure-mode format, web-verified against primary sources this
session. It also settles §5's `experiment` object and §11 spike item 5 (the "cheapest
discriminating experiment"), which the six tables named but did not ground. Timestamp from
`date`: 2026-07-18 01:49 PDT.*

The user's motivating loop ends in *action*: "propose tests," "the cheapest discriminating
experiment." Choosing which experiment to run next — to resolve a `contested` claim, break a tie
between competing `hypothesis` nodes, or shore up a single-provenance belief — is not a new
problem either. It is **optimal experimental design (OED)**, 70 years deep.

### A.1 Prior art

| Facet | Finding |
|---|---|
| Primitive | **Bayesian OED / expected information gain.** Lindley (1956) defines the value of an experiment as the **expected reduction in Shannon entropy** from prior to posterior — pick the design that maximizes EIG. Chaloner & Verdinelli (*Statistical Science*, 1995) is the canonical review, unifying the field under a decision-theoretic lens (a design maximizes expected utility; EIG is the information-utility case) for linear and nonlinear models. The ML cousin is **active learning** (Settles's survey): **uncertainty sampling**, **query-by-committee** (label the point the committee most disagrees on), **expected model change / error reduction** — all cheap myopic proxies for "which query is most informative." Modern **amortized sequential** design (**Deep Adaptive Design**, Foster, Ivanova, Malik & Rainforth, ICML 2021) trains a policy network up front so the next design is a **millisecond forward pass** at run time, removing the per-step optimization that made sequential OED impractical. |
| Reuse | The EIG objective **is** the "cheapest discriminating experiment" the reaction and gpt keep naming — formalized. Our graph already holds the posterior it operates on: `dispute_state: contested` claims, competing `hypothesis` nodes, and calibrated `evidence_count` (reaction §4) are exactly the uncertainty an experiment should reduce. **Query-by-committee maps directly onto our multi-lens adversarial verify** (reaction §6 / study §5): when the perspective-diverse verifiers *disagree* about a claim, that disagreement is the committee variance that marks a high-information experiment — reuse the verify panel we already need as the selection signal, no new model. |
| Avoid | **OED needs a probabilistic outcome model** (a prior + likelihood over what the experiment would show); our graph has calibrated *evidence* but **no calibrated predictive model of experiment outcomes**, so full Bayesian EIG is not computable here yet and pretending otherwise manufactures false precision. **DAD-style amortized policies** assume a simulator and a fixed horizon — far beyond a personal library; do not build a policy network. And the §7 result bites hardest here: **model self-evaluation of research value is unreliable**, so an automated ranker that scores its own proposed experiments inherits that unreliability. |
| Failure mode for our spike | Names why gpt's **deferral is correct** and bounds what "not deferred" means. We cannot do OED proper (no outcome model) and must not do amortized policy or self-scored ranking (§7). What we *can* do — and what clears the gate — is a **myopic EIG *proxy*** over the typed graph: rank a candidate experiment by how much `contested`/single-provenance/committee-disagreement mass its outcome would resolve, weighted by calibration and divided by stated cost, then **hand the ranked shortlist to the human** (never auto-select). This is uncertainty-sampling/query-by-committee discipline, not Bayesian OED, and it is honest about being a proxy. |

### A.2 Verdict and disposition

**Study-gate: cleared for the seventh area, and it confirms the deferral.** Cite Lindley / Chaloner-Verdinelli (OED), Settles (active-learning proxies), and DAD (the amortized frontier we are *not* building). The gate does not license an automated experiment designer; it licenses a **myopic, cost-normalized EIG-proxy ranker that resolves graph uncertainty and defers the choice to the researcher** — the same "detection + audit, human disposes" posture as §6, applied to action. Concretely this promotes §11 spike item 5 from "propose one experiment" to "propose a **shortlist ranked by the EIG-proxy** (contradiction-mass-resolved × calibration ÷ cost), with the falsifier per candidate, human picks" — which is exactly the ranked step gpt's §8 item 12 said to defer *until this addendum existed*. It is now unblocked at proxy strength; **full OED / amortized policy stays deferred** pending a calibrated outcome model we do not have.

**On gpt's other six amendments (for the record, not this addendum's scope):** they are accepted and land in the *corrected spike* artifact (the second open obligation in `sync_ledger.json`), not here — split hard/evidential/heuristic derivation-propagation strengths (sharpens §2), retain the minimal work-object family `goal`/`opportunity`/`experiment`/`decision`/`outcome` (corrects the §3 collapse — those are *operational* loop objects, distinct from the knowledge objects §3 pruned), separate deterministic graph **lints** from generated **audits** (sharpens §6), use a controlled two-domain transfer **fixture** with a structural positive + lexical decoy rather than the 12-claim graph (corrects §11 item 3), report **novelty-search coverage** rather than declaring novelty (sharpens §5/§6), and **label the temporal holdout a smoke test** (corrects §11 item 6 / §7). None is a dispute; all shrink or harden the spike.

## Sources (external primary art, read this session; not repo parent_artifacts)

**Truth maintenance / incremental recomputation (§2)**
- Doyle, "A Truth Maintenance System," *Artificial Intelligence* 12(3), 1979 — sciencedirect.com/science/article/abs/pii/0004370279900080
- de Kleer, "An Assumption-based TMS," *Artificial Intelligence*, 1986 (environments/labels)
- "DBSP: Automatic Incremental View Maintenance for Rich Query Languages," *VLDB Journal* 34(4), 2025 — dl.acm.org/doi/10.1007/s00778-025-00922-y (O(Δ), differential dataflow)
- Gaur, Bhattacharya, Bedathur, "How and Why is An Answer (Still) Correct? Maintaining Provenance in Dynamic Knowledge Graphs," CIKM 2020 — arxiv.org/abs/2007.14864 (HUKA, provenance polynomials)

**Research-object / assertion frame (§3)** — argument-mining/SciFact prior art (S0 row 7); idea frames from §5 systems.

**Cross-domain transfer (§4)**
- Hahn-Powell, Valenzuela-Escárcega, Surdeanu, "Swanson linking revisited: Accelerating literature-based discovery across domains using a conceptual influence graph," ACL 2017 — aclanthology.org/P17-4018/
- Gentner, "Structure-Mapping: A Theoretical Framework for Analogy," *Cognitive Science*, 1983
- Falkenhainer, Forbus, Gentner, "The Structure-Mapping Engine," *Artificial Intelligence*, 1989 (systematicity)

**Idea / experiment generation (§5)**
- Wang, Downey, Ji, Hope, "SciMON: Scientific Inspiration Machines Optimized for Novelty," ACL 2024 — aclanthology.org/2024.acl-long.18/
- Baek, Jauhar, Cucerzan, Hwang, "ResearchAgent," NAACL 2025 — aclanthology.org/2025.naacl-long.342/
- Gu, Krenn, "Interesting Scientific Idea Generation using Knowledge Graphs and LLMs (SciMuse), Evaluations with 100 Research Group Leaders," 2024 — arxiv.org/abs/2405.17044
- Google, "Towards an AI co-scientist," 2025 (Nature 2026) — arxiv.org/abs/2502.18864 (generate/reflect/rank-Elo/evolve; AML + liver-fibrosis wet-lab)
- FutureHouse, "Robin: A multi-agent system for automating scientific discovery," 2025 (Nature 2026) — arxiv.org/abs/2505.13400 (Crow/Falcon/Finch + Owl; ripasudil / dry AMD)
- "An Evaluation of Sakana's AI Scientist … (ARI)?," 2025 — arxiv.org/abs/2502.14297 (documented failure set)

**Blind spots (§6)**
- Sourati, Evans, "Accelerating science with human-aware artificial intelligence," *Nature Human Behaviour* 7(10), 2023 — nature.com/articles/s41562-023-01648-z (avoid-the-crowd; +400% where literature sparse)

**Ideation evaluation (§7)**
- Si, Yang, Hashimoto, "Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers," 2024 — arxiv.org/abs/2409.04109
- Si, Hashimoto, Yang, "The Ideation-Execution Gap," 2025 — arxiv.org/abs/2506.20803

**Active experiment selection (Addendum A)**
- Lindley, "On a Measure of the Information Provided by an Experiment," *Annals of Mathematical Statistics*, 1956 (EIG = expected prior→posterior entropy reduction)
- Chaloner, Verdinelli, "Bayesian Experimental Design: A Review," *Statistical Science* 10(3), 1995 (canonical decision-theoretic review) — jstor.org/stable/2246015
- Settles, "Active Learning Literature Survey," 2009 (uncertainty sampling · query-by-committee · expected model change/error reduction)
- Foster, Ivanova, Malik, Rainforth, "Deep Adaptive Design: Amortizing Sequential Bayesian Experimental Design," ICML 2021 — arxiv.org/abs/2103.02438 (amortized real-time design policy; the frontier we are *not* building)

## Revision History

| Rev | Date | Change | Driver |
|---|---|---|---|
| 1 | 2026-07-17 21:42 PDT | Initial S0-style existing-art study for the research-object model + opportunity engine: six capability tables (truth maintenance, assertion frame, cross-domain transfer, idea generation, blind-spot detection, ideation-execution evaluation), each web-verified against primary sources; study-gate verdict that *shrinks* gpt's `260717-2114` widening (reuse TMS/IVM, SME/LBD, refuse the ideation failure modes); bounded evidence-to-opportunity spike proposal. | user request: do the opportunity-engine study properly, S0-style, in a proposal |
| 2 | 2026-07-18 01:49 PDT | Added Addendum A — active experiment selection (the seventh capability area gpt's amended `260717-2114` @ `0b5534c` flagged as missing and gated automated experiment ranking on): OED (Lindley 1956; Chaloner-Verdinelli 1995), active-learning proxies (Settles), amortized DAD (Foster et al. 2021). Verdict confirms gpt's deferral — no outcome model for full EIG, no policy network, no self-scored ranker — and licenses a myopic cost-normalized EIG-*proxy* shortlist with human disposition, unblocking §11 item 5's ranked step at proxy strength. Recorded that gpt's other six spike amendments are accepted into the forthcoming corrected-spike artifact. | gpt `0b5534c` named the gate; user request: draft the addendum |
