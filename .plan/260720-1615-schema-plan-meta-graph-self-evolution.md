---
artifact_type: schema_plan
authority: speculative
generated_by: llm-design-discussion
convergence: modal
parent_artifacts:
  - AGENTS.md
  - .plan/260720-1614-brainstorm-self-evolving-library-northstar.md
  - .plan/260720-0024-brainstorm-rl-harness-graph-reward-functions.md
  - .plan/260720-1000-study-gray-literature-conflicting-claims-verification-s0.md
  - paper-library/schemas/edges.schema.json
  - gpt:.plan/260720-1433-brainstorm-self-evolving-smart-library-harness.md
tags: [meta-graph, self-evolution, schema, fixtures, harness, invariants, reflexivity, diagram]
---

# Schema Plan — The Meta-Graph for Self-Evolution

*Status: speculative schema plan. The concrete node/edge spec behind the self-evolving-library
brainstorm (`260720-1614`). The core move is reflexive: the meta-graph is the **object graph's own
schema applied to a corpus whose "papers" are measurement runs and whose "claims" are findings about
the machinery** — so it reuses all six object-graph relation families and adds only three new
members. That reuse is the correctness argument. Not a migration and not executable yet; the
next step (offered) is `meta_edges.schema.json` in the `paper-library/` style. Timestamp from
`date`: 2026-07-20 16:15 PDT.*

*Convergence: `modal` — same-prompt parallel with gpt `260720-1433`; the six absorbed items (§ Node
types / Relations / Fixture families notes) are credited inline.*

---

## 1. At a glance

```
        THE ANCHORS — the only nodes that cannot self-evolve
   ┌─────────────────────────┐   ┌─────────────────────┐   ┌─────────────────────────┐
   │  HUMAN (Personal)       │   │  FROZEN PAST (time) │   │  REALIZED OUTCOME (time)│
   │  disposition = gold     │   │  holdout=ungameable │   │  did it pay off = util. │
   └───────────┬─────────────┘   └──────────┬──────────┘   └───────────┬─────────────┘
               │ selected_for (ratify)      │ anchors (fit)            │ anchors (utility)
               ▼                            ▼                          ▼
 ╔══════════════════════════════════════════════════════════════════════════════════╗
 ║  META-GRAPH — machinery as research objects                                        ║
 ║                                                                                   ║
 ║   measurement_run ──measured_on──▶ fixture ──guards_against──▶ failure_mode        ║
 ║      │  (evidence, snapshot-pinned)                                                ║
 ║      │ grounded_in                        supports/refutes                         ║
 ║      ▼                                          │                                  ║
 ║   finding ──motivated_by──▶ change_proposal ──targets──▶ ┌ schema_element          ║
 ║                                   │                       ├ check                  ║
 ║                                   │ gated by check(I3)    ├ fixture                ║
 ║                                   ▼                       ├ policy   (Axis-2 cache) ║
 ║                            disposition.selected_for       ├ prompt   (Axis-2 cache) ║
 ║                                                           └ organization_state      ║
 ╚═══════════════════════════════════════│═══════════════════════════════════════════╝
                                          │ evolves / evaluates  (reflexive)
                                          ▼
 ┌──────────────────────────────────────────────────────────────────────────────────┐
 │  OBJECT GRAPH — the library (assertions · disputes · sources · stake)             │
 └──────────────────────────────────────────────────────────────────────────────────┘
 ┌──────────────────────────────────────────────────────────────────────────────────┐
 │  CONSTITUTION — invariants + anchors · human-amendable ONLY · bedrock             │
 └──────────────────────────────────────────────────────────────────────────────────┘
```

Three anchors, not two (the utility dig, brainstorm §5): the human defines the target; the frozen
past measures *fit*; realized outcomes measure *utility*. The past and the outcome are two ungameable
time-clocks.

## 2. Node types — and the object-graph role each plays (the reflexivity proof)

| Meta node | Plays role of (object graph) | Key fields | Lifecycle | Mutable by |
|---|---|---|---|---|
| `measurement_run` | **source** (immutable evidence) | `snapshot_sha`, `checks_ran[]`, `fixtures[]`, `scores{}` | frozen | — (append-only) |
| `finding` (`system_finding`) | **assertion/observation** | `frame`, `severity`, `about` | proposed → confirmed → resolved \| dismissed | code+human |
| `change_proposal` | **opportunity + experiment** | `rationale`, `expected_effect`, `falsifier`, `rollback` | proposed → screened → measured → {ratified\|rejected\|deferred} → applied → superseded | lifecycle |
| `disposition` | **decision** | `verdict`, `reason` | terminal | **human only** |
| `schema_element` | **artifact** (under study) | `kind: node_type\|relation_member\|frame_slot`, `consumer_count` | shadow → candidate → promoted → deprecated → retired | code+human |
| `check` | **artifact** (under study) | `kind: lint\|metric\|reward\|anchor`, `dual_of` | proposed → active → deprecated | code; **anchor: human only** |
| `fixture` | **artifact** (under study) | `kind: gold\|silver`, `split: train\|eval\|holdout`, `family`, `mined_from`, `expected`, `expected_not` | silver → gold → stale → retired | code proposes; **gold: human ratifies** |
| `policy` | **artifact** (Axis-2 **cache**) | `cache: true`, `derived_from`, `allowed_mutations` | trained → active → superseded | code (freely — deletable) |
| `prompt` | **artifact** (Axis-2 **cache**) *(absorb: gpt §5)* | `cache: true`, `version`, `derived_from` | drafted → active → superseded | code (freely — deletable) |
| `organization_state` | **projection** (fast-clock) *(absorb: gpt §1)* | `views`, `workspaces`, `queues`, `aliases`, `indexes`, `uses_policy` | regenerated; never source-of-record | code (freely) |
| `invariant` | **constraint** (Personal) | `rule`, `owner: human`, `mutable: false` | constitutional | **human only** |
| `anchor` | **goal** (Personal) | `protects[]`, `kind: human\|frozen_past\|realized_outcome` | constitutional | **human only** |

Every meta node maps onto an existing object-graph type — nothing here is a new *kind* of thing.
`policy`, `prompt`, and `organization_state` are all Axis-2: deletable, rebuildable, never
source-of-record.

## 3. Relation catalog — six reused families + three new members

Reused verbatim (object-graph member → meta endpoints):

| Family | Member | Endpoints (meta) | Auto? |
|---|---|---|---|
| structural | `grounded_in` | `finding → measurement_run` | auto |
| evaluation | `measured_on` (≡ gpt `evaluated_on`) | `measurement_run → fixture` | auto |
| evaluation | `compares_with` | `policy → policy` (vs baseline) | auto |
| evaluation | `reproduces` | `measurement_run → measurement_run` | auto |
| epistemic | `supports` / `refutes` | `measurement_run → change_proposal` | auto |
| epistemic | `contradicts` | `measurement_run → policy` (proxy-up/anchor-flat = hack) | auto |
| epistemic | `depends_on` | `schema_element → schema_element` | auto |
| temporal | `supersedes` / `merged_into` | `{schema_element\|check\|fixture\|policy\|prompt}` self | auto (cache) / human (anchor) |
| work | `motivated_by` | `change_proposal → finding`; `policy_change → system_finding` | auto |
| work | `derived_from` | `{policy\|prompt} → {fixture_set + schema_snapshot}` (rebuild recipe) | auto |
| work | `selected_for` (**= ratify**) | `disposition → change_proposal` | **human** |
| work | `blocks` | `invariant → change_proposal` (constitution vetoes) | auto-enforced |

New members — each with a distinct consumer (passes our own ≥2-consumer bar, reflexively):

| Family | New member | Endpoints | Why it can't reduce to an existing one |
|---|---|---|---|
| evaluation | `dual_of` (symmetric) | `check ↔ check` | encodes the **purity/coverage pair**; a metric without a dual is invalid (I3) — no member carries "these two must co-exist" |
| work | `gates` | `check → schema_element` | the **AMSTAR-2 critical-flaw** promotion precondition; distinct from `blocks` (a veto) — `gates` is a *promotion gate* |
| governance | `protects` | `anchor → check` | the **append-only** guarantee; makes "this check cannot be weakened from inside" traversable |
| *(absorb: gpt)* work | `guards_against` | `fixture → failure_mode` | makes a fixture's *purpose* a traversable edge (why it exists) |
| *(absorb: gpt)* work | `uses_policy` | `organization_state → policy` | binds the fast-clock workspace layer to the policy version it runs |

*(Note: `guards_against` and `uses_policy` are absorbed from gpt `260720-1433`; they raise the new
member count from three to five, still a small delta over the reused six families.)*

## 4. Lifecycle states (per node)

```
change_proposal : proposed → screened → measured → {ratified | rejected | deferred} → applied → superseded
schema_element  : shadow(role/tag) → candidate → promoted → deprecated → retired
fixture         : silver → gold(ratified) → stale → retired      ; split ∈ {train, eval, holdout}
check           : proposed → active → deprecated(human-only)       ; kind ∈ {lint, metric, reward, anchor}
policy | prompt : trained/drafted → active → superseded            ; cache:true, derived_from required
finding         : proposed → confirmed(by run) → resolved | dismissed
measurement_run : immutable, snapshot-pinned (no lifecycle)
invariant|anchor: constitutional (mutable:false, owner:human)
```

## 5. Invariants — encoded as graph constraints, not prose

- **I1 · constitution is human-only.** A `change_proposal` whose `targets ∈ {invariant, anchor,
  check{kind:anchor}}` cannot reach `applied` without a human `disposition --selected_for-->` it.
  Auto-apply forbidden at the type level.
- **I2 · anchor checks are append-only.** `anchor --protects--> check{kind:anchor}`; a proposal to
  supersede/weaken a protected check is auto-`blocks`-ed unless human-ratified. New checks add
  freely.
- **I3 · no unpaired optimizer.** Every `check{kind ∈ metric|reward}` MUST have a `dual_of` edge. A
  metric without a dual is an invalid-schema lint — this is what structurally prevents optimizing
  one number into its degenerate optimum (RL brainstorm §4).
- **I4 · policies and prompts are caches.** Every `policy`/`prompt` has `cache:true` + a
  `derived_from` recipe; can never be an `anchor` or a `gates` source; deletion is always safe.
- **I5 · no contamination.** A `measurement_run` that `supports`/`refutes` an anchor-gated proposal
  must be `measured_on fixture{kind:gold, split:holdout}` only — enforced by split tag + snapshot
  boundary, so the system cannot test on what it trained on.
- **I6 · provenance-complete evolution.** An `applied` proposal requires the chain
  `motivated_by → finding → grounded_in → measurement_run`, a `supports` edge, and (`selected_for`
  by a human **or** auto-eligible = reversible ∧ non-anchor). A change lacking the chain is a lint.
- **I7 · rate limit.** `schema_element: shadow → promoted` requires ≥N cycles of `consumer_count`
  evidence across distinct runs; schema/harness edits on the slow clock, parameters on the fast one.

## 6. Fixture families *(absorbed wholesale from gpt `260720-1433` §6)*

Each `fixture` carries a `family`, minimal inputs, `expected`, `expected_not` (negative expectation),
a regression command, protected invariants, and its originating failure/design-question:

`identity_collision` · `wording_variant_duplicate` · `benchmark_mismatch_false_contradiction` ·
`genuine_same_scope_dispute` · `source_drift` · `stakeholder_gray_lit` ·
`citation_valid_unsupported_answer` · `uncheckable_vendor_claim` · `cross_domain_structural_transfer`
· `lexical_analogy_decoy` · `temporal_holdout` · `user_rejected_with_reason` ·
`accepted_idea_failed_after_execution`

The `expected_not` field is load-bearing: the lexical-decoy fixture guards a *rejection*, not an
output — a fixture protects a behavior and its complement.

## 7. Two worked traces

**A — a type earns promotion (schema self-evolves):**
`transfer_hypothesis` lives as a `role` tag (`shadow`) → the ablation audit run `SRC1`
`measured_on` an ablation fixture emits `finding` "dropping the tag costs 18% dispute-resolution
recall," `grounded_in SRC1` → `change_proposal` "promote to node type" `motivated_by` it → the
`≥2-consumer check` `gates` the element (dispute node + digest both consume it) and `SRC2 supports`
(ablation reproduced) → schema change is slow-clock, so human `disposition.selected_for` ratifies →
`applied`: `shadow → promoted`, `supersedes` the role, full chain in the ledger.

**B — a reward hack is caught (harness self-defends):**
`policy POL1` trains, `compares_with` baseline, improves on `check{metric: answerability}` → but the
anchor run `SRC3 measured_on fixture{gold,holdout}` shows no gain → `SRC3 contradicts POL1` (proxy
up, anchor flat) → `finding` "improves proxy not anchor," proposal to adopt `POL1` is `refuted`,
auto-rejected → `POL1` stays a deletable cache, never promoted. If `answerability` lacked its
`dual_of` precision-floor (I3 violated), the missing dual is itself a lint spawning an append-only
proposal to add it — human ratifies.

## 8. Human surface *(absorb: gpt `260720-1433`)*

Self-evolution noise stays off the default surface. A compact **System-Health page** (fixture-suite
status, validator failures, stale-projection count, unresolved schema pressure, detector
precision/review-yield, abstention rate, drift events, top recurring rejection reasons, proposed
changes awaiting review) and a **Harness Queue** of typed items (add fixture / promote schema /
adjust detector / retire projection / split workspace / review prompt regression / approve
migration) with actions {approve · reject-with-reason · request-smaller-fixture · run-expanded-eval
· defer}.

## 9. Cross-team disposition

- **Local machinery (C8).** Nothing here amends shared schemas or Parallax.
- Reflexive and additive to gpt's execution baseline: the `organization_state` layer, `prompt`
  node, `guards_against`/`uses_policy` edges, and the fixture families are shared vocabulary; the
  three-anchor model and I1–I7 are the constitutional spine. Not a reaction — the cycle's reaction
  is the amended `260719-1336`.
- **Next step (offered, not done):** `paper-library/schemas/meta_edges.schema.json` — the executable
  form, endpoint-constrained like the object graph's `edges.schema.json`.

## Revision History

| Rev | Date | Change | Driver |
|---|---|---|---|
| 1 | 2026-07-20 16:15 PDT | Initial meta-graph schema: at-a-glance diagram (three anchors: human/frozen-past/realized-outcome), 12 node types each mapped to an object-graph role (reflexivity proof), relation catalog (six reused families + three new members dual_of/gates/protects + two absorbed guards_against/uses_policy), per-node lifecycles, invariants I1–I7 as graph constraints, the 13 fixture families absorbed from gpt `260720-1433`, two worked traces (schema promotion; reward-hack catch), and the System-Health/Harness-Queue surface. Companion to brainstorm `260720-1614`. | user request: persist the whole self-evolving cycle incl. diagrams |
