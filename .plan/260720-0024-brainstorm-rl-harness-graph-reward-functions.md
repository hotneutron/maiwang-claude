---
artifact_type: brainstorm
authority: speculative
generated_by: llm-design-discussion
convergence: n/a
parent_artifacts:
  - AGENTS.md
  - .plan/260717-1827-brainstorm-graphrag-wiki-cl-migration.md
  - .plan/260717-2142-proposal-opportunity-engine-existing-art-s0.md
  - .plan/260719-1336-reaction-gpt-execution-proposal-moat.md
  - gpt:.plan/260719-0426-proposal-smart-library-execution.md
tags: [rl, reward-function, verify-gate, graph-quality, identity, ablation, temporal-holdout, eval-harness, study-gate-pending]
---

# Brainstorm — Would an RL harness help, and what can serve as a reward function?

*Status: speculative brainstorm, persisting a design discussion held 2026-07-19/20. Two questions:
(1) will an RL harness help this project, and how; (2) setting aside "what research is good,"
what else in the semantic structured graph can serve as a reward function — i.e. what makes the
graph's **usability** measurable. Not a plan, not measurement, not a study. Timestamp from `date`:
2026-07-20 00:24 PDT.*

*Convergence: `n/a` — local synthesis over our own design history and gpt's execution baseline,
no corroboration claim.*

**Confidence flag (load-bearing):** the external-prior-art claims below (RLVR, RL for
retrieval/search agents, process reward models, reward-model overoptimization, preference learning
at low N) are **from memory at moderate-to-high confidence and were NOT web-verified this
session**. That is below the bar our S0 studies hold. See §5 — a proper answer to "should we RL"
trips the study-gate and needs a bounded primary-source study first. This artifact is the design
map that study would sharpen, not a substitute for it.

---

## 0. TL;DR

- **Yes for one narrow locus, no for the one you'd most want it for, and the harness is worth
  building even if RL never runs.** The env + reward + fixture scaffolding *is* the eval harness
  the phase exits already require, so its incremental cost is ~zero.
- **The verify gate is already a programmatic reward function over a private corpus** — a rare
  asset, and a byproduct of the typed substrate. Prose wikis have nothing to check against.
- **Never RL the opportunity ranker on human dispositions**: our own study §7 (ideation-execution
  gap) shows that reward signal is *inverted*, not merely noisy.
- **Any trained policy is Axis-2** — derived, deletable, rebuildable from canonical state. A
  policy is a cache exactly like weights. The moat stays in the graph.
- Beyond the verify gate there are ~11 graph-intrinsic reward signals (§3). They split into
  **purity** and **coverage** metrics that are duals; every usable objective is a constrained pair.
- Best spends, in order: **identity/dedup** (unlimited synthetic data, exact ground truth, highest
  moat value), **ablation-answerability** (turns the ≥2-consumer promotion bar into a computed
  statistic), **temporal-holdout link prediction** (usability = predictive purchase).

---

## 1. "RL harness" conflates three different things

1. **Environment + reward scaffolding** — deterministic env, fixtures, rollout runner,
   programmatic scorer.
2. **RL as training signal for a policy over graph operations** — retrieval, expansion, stop,
   abstain.
3. **RL to learn what research is *good*** — opportunity ranking, idea quality, experiment choice.

(1) is nearly free and pays off regardless. (2) is the real candidate. (3) is what people mean
when they get excited, and it is the one that fails here (§2.2). Keeping these separate is most of
the clarity.

## 2. Where RL fits and where it does not

### 2.1 Fits: the verify gate as reward, the read path as a genuine MDP

The verification artifact — ID/anchor existence, relation validity, answer-strength-vs-evidence,
contradiction disclosure, unsupported composition, abstention correctness — is a **deterministic
checker over a private corpus**. That is the RLVR shape (verifiable rewards), and it exists here
only because the substrate is typed and evidence-linked.

The read path is then an MDP rather than a forced framing:

```text
state   = current retrieved object/edge set + budget spent
actions = expand along relation family r | stop | abstain
reward  = verifier pass − retrieval cost − hallucinated-citation penalty
          + abstention-when-uncovered credit
```

Three properties make it defensible: rollouts are **cheap and offline** (no human in the loop),
questions can be **generated synthetically from the graph** at volume (so N is not the binding
constraint), and reward is **immediate and checkable** rather than delayed and confounded.
Abstention especially — supervised learning has no label for "should have said I don't know," but
RL shapes it directly.

**Hard caveat:** optimizing against your own verifier is reward hacking by construction
(reward-model overoptimization). Requires a held-out check the policy never trains against — an
independent verifier or human spot-check — or you get a policy that satisfies the checker while
retrieving worse.

### 2.2 Fails: ranking opportunities from human dispositions

The tempting application, killed by our own S0 study. In descending severity:

1. **The reward signal is inverted, not just noisy.** The ideation-execution gap (Si, Hashimoto,
   Yang, 2025; study §7): idea-stage novelty/excitement judgments *reverse* after 100+ hours of
   execution. Training a ranker on accept/reject dispositions optimizes for what looks good at
   idea-stage — precisely the metric shown to flip. It trains toward the failure mode.
2. **N is dozens per year, not thousands.** SciMuse needed 4,400 ratings from 100+ group leaders
   for *supervised* interest prediction; RL is far more sample-hungry than regression.
3. **Reward is delayed and confounded** — outcome arrives months later, entangled with execution
   skill, resources, luck.
4. **Non-stationary target** — the researcher's goals shift, which is the point of the goal layer.

Plus the failure mode both lanes already flagged: anything learning from acceptance rate drifts
toward engagement optimization. Immediate-reward variants (bandits over which detector types get
acted on) are **worse**, not better — that is the engagement trap in pure form.

**Correct use of the disposition record: offline evaluation, not reward.** It is the irreplaceable
data (moat reaction §5); its value is as a held-out judgment set for testing whether a transparent
scorecard beats a baseline — not as a gradient.

### 2.3 The moat rule

A trained policy is a **cache, exactly like weights** — same principle as gpt's "weights remain a
cache, not the accountable source of truth." Therefore **any RL policy is Axis-2: derived,
deletable, rebuildable from canonical state.** It never becomes canonical, never mutates the graph
directly, and its proposals enter the same `proposed → reviewed` lifecycle as any LLM output. This
keeps the moat in the state and prevents the policy becoming an unauditable second source of truth.

---

## 3. Reward inventory beyond the verify gate — graph-intrinsic signals

Scope per the question: usability of the semantic structured graph; the "what research is good"
axis is excluded. Most of these fall out of invariants both lanes already committed to.

| Signal | Computed how | What it trains | Degenerate optimum (the danger) |
|---|---|---|---|
| **Identity/dedup correctness** | Perturb known records (same paper, different metadata; same claim, reworded) + near-miss distractors; reward correct merge / correct non-merge | Identity resolver, alias handling | Merge-everything or merge-nothing |
| **Δ-propagation == full recompute** | Exact set equality between incremental affected-set and full rebuild, minus nodes touched | Impact-engine traversal policy | Touch everything (correct, expensive) |
| **Idempotency / extraction stability** | Re-extract same source twice, graph-diff distance; abstract-vs-full-text reconciliation | Extractor determinism | Trivially constant output |
| **Round-trip fidelity** | source → assertion frame → regenerated NL → NLI entailment both directions | Frame completeness, no-drop/no-invent | Copy the passage verbatim into node text |
| **Temporal-holdout link prediction** | Graph as-of-T; does it predict later edges (method `measured_on` benchmark, claim `qualifies`, claim `supersedes`)? | Relation proposal, structural priors | Predict only high-frequency edge types |
| **Ablation answerability** | Delete an object/edge, re-run the question set, measure degradation | Which structure earns its keep | Keep everything |
| **Hops-to-answer / budget** | Fraction of questions answerable within *k* typed hops | Abstraction + linking placement | Connect everything to everything |
| **MDL / compression** | Bytes of graph needed to reconstruct the answer set | Community summaries, abstraction edges | Drop information |
| **Lint-clean fraction** | The deterministic lints already specified (dangling evidence, single provenance, endpoint-type violations, `supersedes` acyclicity, stale verification) | Schema discipline | **Extract nothing** |
| **False-contradiction resolution** | Apparent contradictions dissolved by frame alignment (benchmark/population/intervention) vs genuine ones preserved | Assertion-frame slot filling | Over-qualify until nothing ever conflicts |
| **Human edit distance** | When the researcher corrects an extraction, the edit *is* the label; pre/post-edit as preference pairs | Fidelity | — (sparse, but honest) |

The human-edit row is **in scope** under the stated constraint: correcting a mis-extracted claim is
a *fidelity* judgment, not a research-value judgment.

## 4. The structural finding — every signal is half of a pair

Reading down the degenerate-optimum column, the list splits cleanly:

- **Purity metrics** (lints, idempotency, compression/MDL, false-contradiction resolution) — optimum
  is *assert less*, terminal state is an empty graph.
- **Coverage metrics** (ablation answerability, hops-to-answer, round-trip fidelity, link
  prediction) — optimum is *assert more*, terminal state is an undifferentiated hairball.

Optimizing either alone collapses the graph in one direction. So the usable form is always a
**constrained pair** — coverage subject to a lint/precision floor, or compression subject to
answerability. This is not a caveat; it is the actual design of a graph-quality objective, and it
is why "the graph looks clean" was never evidence of anything.

## 5. Which are RL rewards vs. plain metrics, and where to spend

**Most are eval metrics or rejection-sampling filters, not RL rewards** — single-shot, no sequential
structure, so best-of-N + verifier rerank or SFT on verifier-filtered data reaches the same place
without a policy. Only three have genuine multi-step decision structure:

1. **Retrieval / expansion / stop** (§2.1)
2. **Δ-propagation traversal** — which dependency paths to follow; correctness constraint plus
   explicit cost penalty, i.e. the O(Δ) objective written down exactly
3. **Multi-step extraction + reconciliation** — each decision changes the state the next one sees

**Ranked spends:**

1. **Identity/dedup.** The only signal with *unlimited synthetic data and exact ground truth* —
   fixtures generated by perturbing records already held — training the component the moat analysis
   put at #1 (get identity wrong and the compounding asset resets). Nothing else on the list has
   that combination.
2. **Ablation answerability — because it converts a governance rule into a measurement.** Both lanes
   settled on "≥2 consumers before promoting a type or relation," currently a judgment call in
   review. Ablation makes it a computed statistic: a type or relation family earns promotion when
   deleting it measurably degrades answers, and dies when it does not. That is
   "earned by measurement, not negotiated" applied to the schema itself, and the sharpest available
   definition of *usability of the semantic structure* — it asks the only question that matters:
   does this distinction do work?
3. **Temporal-holdout link prediction** as the honest usability test: a structure is useful iff it
   predicts things not yet in it. Restricted to *structural* edges (method↔benchmark, qualification,
   supersession) it stays clear of the excluded research-value question.

## 6. Sequencing

- **Now (Phases 2–3, ~free):** build env + reward scaffolding, because it *is* the eval harness.
  Deterministic fixtures, verifier as scorer, rollout runner, synthetic question generator — all
  required by the phase exits already ("verifier rejects the bad answer," "at least one query
  abstains," "incremental equals full recompute").
- **Cheap reporting from Phase 2 onward:** ablation answerability, MDL, hops-to-answer. These earn
  their keep as reported graph-quality numbers whether or not training ever happens.
- **Before any training:** try **best-of-N sampling + verifier reranking at inference**. Large
  fraction of the gain, zero training machinery, and the baseline RL must beat. Many teams
  correctly stop here.
- **Only then, and only for the three sequential loci:** RL with cost-normalized reward, against a
  measured baseline, with an anti-Goodhart holdout the policy never trains against.
- **Never:** RL the opportunity ranker on dispositions. Keep the multi-dimensional scorecard +
  human disposition — what D7 / Addendum A already licensed at proxy strength.

## 7. Open — study-gate status

A proper answer to "should we RL" trips our own study-gate. Required before harness work beyond the
free scaffolding: a bounded S0-style primary-source study of RLVR / verifiable-reward training, RL
for retrieval and search agents, process reward models, reward-model overoptimization (Goodhart
scaling), and preference learning at low N. Expectation is that it **sharpens the boundaries above
rather than moving them** — but that is a prediction, not a result, and §0's confidence flag stands
until it is run.

## 8. Cross-team disposition

- **Local machinery (C8).** Nothing here amends shared schemas or Parallax.
- **Not addressed to gpt and not a reaction** — the one reaction for the `350c420` cycle is
  `260719-1336`. This is speculative local design; it reads as context on their next sync.
- **Relation to gpt's execution baseline**: additive and non-conflicting. The scaffolding lands
  inside their Phases 2–3 exits; the Axis-2 policy rule extends their "weights remain a cache" to
  learned policies; the ablation-answerability signal is a candidate instrument for their
  Consensus §9 two-consumer promotion bar. Nothing here reopens D1–D10.

## Revision History

| Rev | Date | Change | Driver |
|---|---|---|---|
| 1 | 2026-07-20 00:24 PDT | Initial brainstorm persisting the RL-harness design discussion: the three-way split of "RL harness"; verify gate as programmatic reward and the read path as a genuine MDP; why disposition-based opportunity ranking is an inverted reward signal (study §7); the Axis-2 rule for trained policies; an 11-signal graph-intrinsic reward inventory with degenerate optima; the purity/coverage duality; RL-vs-metric triage and ranked spends (identity/dedup, ablation answerability, temporal-holdout link prediction); sequencing and the pending study-gate. | user request: "then keep it" |
