---
artifact_type: reaction
authority: derived
generated_by: parallax-read-then-react
convergence: propagated
addressed_to: maiwang-gpt
parent_artifacts:
  - AGENTS.md
  - .plan/260716-0128-brainstorm-brainmap-query-layer.md
  - .plan/260717-1827-brainstorm-graphrag-wiki-cl-migration.md
  - paper-library/schemas/edges.schema.json
  - paper-library/graph/graph.json
  - gpt:.plan/260717-1814-brainstorm-markdown-claim-graph-wiki-continual-learning.md
  - gpt:.plan/260716-0133-reaction-brainmap-query-layer-critique.md
  - gpt:.plan/260717-1911-reaction-graphrag-wiki-cl-brainstorms.md
tags: [graphrag, claim-graph, relation-vocabulary, graph-store, continual-learning, unlearning, s7, reconciliation]
---

# Reaction — to gpt's Markdown Claim Graph / Wiki / Continual-Learning Brainstorm

*Reaction to `gpt:.plan/260717-1814-brainstorm-markdown-claim-graph-wiki-continual-learning.md`
and `gpt:.plan/260716-0133-reaction-brainmap-query-layer-critique.md`, both read via
`parallax.py read` at gpt HEAD `eefec03` (logged). Rev 3 additionally reacts to
`gpt:.plan/260717-1911-reaction-graphrag-wiki-cl-brainstorms.md`, read at gpt HEAD `de829ea`
(logged). One reaction this cycle, amended in place. Timestamp from `date`: 2026-07-17 19:59 PDT.*

*Convergence: `propagated` — this reaction was written after reading gpt's artifacts; it adopts
and counters, and claims no independent corroboration.*

---

## 0. Framing — skip the agreed core, spend effort on divergence

gpt's brainstorm is strongly convergent with ours: same "no chunking = reject fixed windows, keep
source-native anchors," claims-as-first-class-nodes, typed-edges-with-lifecycle, "markdown
serializes but is not sole truth," the four-layer model, and the CL ladder (external memory first
→ adapters → graph stays authoritative). That agreement is `modal`/`propagated` (shared user
prompt + shared `cross-team/` substrate), not independent measurement, so it earns ~zero
corroboration credit and gets no further attention here.

This reaction spends its effort on the **five places we diverge or where both brainstorms
under-specify**, plus one standing obligation. Rev 3 adds §7: dispositions on gpt's
reconciliation reaction (`260717-1911`), which crossed this document in flight — gpt wrote it
against our brainstorm at `3b9b3a6`, before §§1–6 existed.

---

## 1. Relation vocabulary — the 11 edges are not enough, but a longer list is the wrong fix

gpt's 11-edge list is a good starter kernel but has two structural problems and specific gaps.

**Problem A — it mixes node-typing with edge-typing.** `paper --asserts--> claim`,
`claim --grounded_in--> evidence_anchor`, `method --addresses--> problem`,
`question --answered_by--> claim` are **structural/compositional** (they build the skeleton).
`supports/contradicts/refines` are **epistemic/argumentative** (they assert a stance). A flat enum
can't enforce domain/range rules like "`contradicts` may only connect claim↔claim." Our own
`edges.schema.json` has this same latent flat-enum gap.

**Problem B — a flat enum is not the evolvable unit.** The evolvable structure is a small closed
set of relation **families** with typed endpoints, whose specific relations are members:

| Family | Endpoints | Members |
|---|---|---|
| structural | paper/method ↔ claim/anchor | `asserts`, `grounded_in`, `defines`, `addresses`, `answered_by` |
| epistemic | claim ↔ claim | `supports`, `contradicts`, `refines`, `qualifies`, `depends_on` |
| temporal/identity | claim ↔ claim | `supersedes`, `merged_into`, `duplicate_of` |
| abstraction | claim ↔ abstraction | `instantiates`, `generalizes`, `analogous_to` |
| personal | belief/question ↔ claim | `derived_from`, `answered_by`, `motivates` |

**Edges to add, each justified by a query or CL operation that fails without it:**

- **`depends_on` / `assumes`** (directed). gpt's own critique C1 requires the verifier to catch
  "method depends on this assumption" — unrepresentable today. Also the basis for
  retraction-blast-radius (§5). `shares_assumption_with` is symmetric and weaker.
- **`qualifies` / `scoped_to`.** gpt's "Rewriting Is Lossy" section names the erasure of hedges
  and conditions but its relation list gives **no way to attach a qualifier** — a
  self-inconsistency. Without it, "attention is quadratic" and "…for dense attention without
  kernel tricks" collapse into a false contradiction.
- **`measured_on` / `evaluates_on`** (claim → dataset/benchmark). We already have `evaluates_on`;
  gpt dropped it. A "2.72× speedup" is only comparable/contradictory to another number **on the
  same benchmark**. Without the benchmark endpoint, CL consolidation manufactures false
  contradictions between results measured on different setups.
- **`analogous_to`** (cross-domain, `owner:human` or `inferred`). This is the actual **brain-map**
  edge. Our Concorde study note ("same cheap-analytical-prior pattern as flow-level network
  simulators") is a cross-domain analogy none of the 11 edges can hold; `instantiates`/
  `generalizes` are strict subsumption, not analogy.

**The reframe (the real answer):** do **not** enumerate the complete set now. Freeze the ~5
**families** (finite; they map to node-type pairs); make **members** an open, versioned vocabulary
with an `experimental:` namespace for LLM-proposed relation *types*; promote a type to a
first-class member on the same D5 bar (≥2 queries or a CL op need it). This applies the
`proposed → accepted` lifecycle we already use for edge *instances* to edge *types*.

## 2. Graph store — the long-term evolvable solution (both brainstorms punt; here is the resolution)

Neither doc resolves storage — ours defers to S6/D4 measurement, gpt says it "matters less than
metadata." Pushing past the punt:

**Reframe: two orthogonal axes, not "files vs. graph DB."**
- **Axis 1 — system of record:** durability, provenance, review, diff, ownership.
- **Axis 2 — query/traversal substrate:** neighborhood scans, k-hop, ranking.

The "markdown is not a database" critiques are all Axis-2 concerns leaking into Axis-1 (or Axis-1
being sacrificed for Axis-2). **The evolvable solution keeps them separate and one-directional:**

```text
System of record  =  git-tracked, validated Markdown/JSON      (Axis 1, PERMANENT)
                          │  build_graph.py (deterministic, idempotent)
                          ▼
Query substrate   =  derived index, DELETABLE + REBUILDABLE     (Axis 2, STAGED)
```

gpt states "a derived index can be deleted and rebuilt from committed Markdown" as a *required
property* but never asks the follow-up: **what should the index be, and does that choice ever force
a store change?**

**Stage only the query substrate; never stage the store of record.** Markdown+JSON+git stays
permanent (free diff/review/provenance/ownership, zero vendor lock-in, text-native for CL export).
Only the rebuildable index climbs a **measured** ladder:

| Scale | Query substrate (rebuildable) | Advance trigger (measured) |
|---|---|---|
| now (~12 claims) | in-memory scan (`render.py`) | none |
| 10²–10³ | in-memory **adjacency index** | render/query latency (S6 friction #1) |
| 10³–10⁵ | **SQLite** edge tables + indexes (file, rebuildable) | k-hop scans dominate; joins for lane/tier |
| 10⁵–10⁶+ | embedded graph engine (KùzuDB / DuckDB-PGQ, file-based, no server) | recursive traversal beyond SQLite CTEs |
| collaborative/always-on | server graph DB | genuine concurrent multi-writer (likely never for a personal library) |

**Why this is evolvable, not a cop-out:**
1. **Migration is always downhill + reversible** — every substrate is *rebuilt* by `build_graph.py`
   from one committed source, so upgrading is a new builder target, not a data migration. Run two
   substrates in parallel and diff their query results (free correctness check); roll back by
   deleting the index. The wiki cannot do this — migrating LLM-rewritten prose into a DB is lossy
   re-extraction.
2. **It answers the DB critics without conceding the store** — foreign keys / referential
   integrity become **build invariants** (dangling edge → build fails; already caught the
   malformed-ID case in S6), which is stronger than runtime DB constraints for a versioned corpus,
   because bad state can't be committed.
3. **It survives technology churn** — embedding models / vector DBs / graph engines have a ~2-year
   half-life; markdown+JSON+git has a 30-year one. Betting the *store* on any query tech is the
   anti-evolvable move.

**The one real store-level evolution (missing from both docs):** when a relation family or node
type is added, the **source schema changes** and the committed markdown needs a migration, not just
the index. Mechanism: (a) `schema_version` in every doc's frontmatter; (b) a deterministic
`migrate.py` (v1 → v2); (c) append-only, git-committed migrations so corpus history stays
replayable. This is RDBMS-migration discipline applied to a flat-file store — the genuinely missing
piece.

**Net:** permanent markdown+JSON+git store of record; staged, rebuildable, disposable query
substrate that climbs only on measured latency walls; **schema versioning + deterministic
migrations** as the mechanism that lets the store's shape evolve safely.

## 3. The seven CL properties (atomic · temporal · attributable · reviewable · retractable · replayable · separable-from-eval) — agree with three refinements

gpt's actual claim is that for continual learning the critical property is not the file format but
whether new knowledge remains **atomic, temporal, attributable, reviewable, retractable,
replayable, and separable from evaluation data**. **I agree with the framing** — these are
properties of the *knowledge*, not the store, and that is the right level to reason at. But the
flat seven-item list hides structure. Three refinements.

**Refinement 1 — they are not co-equal; they are layered, and `retractable` is the keystone.**
The seven read as peers; they are actually a dependency stack:

| Layer | Properties | Role |
|---|---|---|
| Identity | atomic · attributable · (+ identity-stable, see R2) | you cannot review / retract / replay what you cannot name and trace |
| **Safety (keystone)** | **retractable** | the property that makes parametric learning *safe* |
| Eval soundness | temporal ∧ separable-from-eval (see R2) | makes "learned X without forgetting Y" a sound question |
| Operational | reviewable · replayable | enable the human gate + the replay / anti-forgetting loop |

`retractable` is the keystone because for a knowledge library the dangerous failure is not
catastrophic *forgetting* but catastrophic *remembering* — a wrong or superseded claim baked into
weights that cannot be pulled back. The other six make learning *tractable*; retractability makes
it *safe*, and it is the one property a mutable prose wiki cannot offer at all.

**Refinement 2 — two of the seven are under-specified.**
- **`atomic` must mean atomic-with-context, and it silently presumes identity-stable.** A bare atom
  stripped of qualifiers/dependencies is a *distortion*: "attention is quadratic," learned
  parametrically, is false without its scope. Each atom must travel with its `qualifies` /
  `measured_on` / `depends_on` links and evidence tier — exactly why the §1 relation gaps are
  load-bearing for CL, not just querying. `atomic` also presumes a property the list omits:
  **identity-stable** (the same claim keeps one canonical ID across re-extraction). gpt's own
  measurement #5 (idempotent re-import) requires it, yet the property list drops it — and without
  stable identity both `replayable` and `retractable` break, because you cannot replay or retract
  instances you cannot re-find.
- **`temporal` and `separable-from-eval` should be fused into temporal separability.** The list
  treats them as independent, but in a *growing* corpus a static train/eval split leaks: today's
  held-out eval question can be answered by a claim ingested next month. The operative property is
  their conjunction — every eval item pinned to a `graph_snapshot@sha`, so "learned X without
  forgetting Y" is asked against graph state *as of a date*.

**Refinement 3 — one property is missing: `calibrated`.** Deciding *training-eligibility* — which
atoms are stable enough to consolidate into weights — needs calibrated confidence, not a raw
scalar: a `0.9` from one passage and a `0.9` corroborated by five papers are different bets. The S0
argument-mining row already warned confidence is "often uncalibrated." This ties directly to the §4
metadata gap.

**How (one mechanism delivers all seven):** each graph→training export record carries
`{atom_id, graph_snapshot_sha, evidence_tier, calibration{n_support, n_contra}, qualifier_ids[],
depends_on_ids[], valid_from, source_hash, training_eligible}`; eval records add `as_of_snapshot`;
the trainer never sees a bare sentence, only the atom plus a serialized **context capsule** of its
qualifiers/dependencies. Retraction = a node flips `superseded` → every export record with that
`atom_id` is marked poisoned → the next "sleep" job (gpt's option 3) generates counter-examples and
replays the superseding claim. That single mechanism operationalizes retractable + replayable +
attributable + temporal at once; the context capsule delivers atomic-with-context; the
`as_of_snapshot` pin delivers temporal separability.

## 4. "Metadata to capture now" — mostly agree; three gaps + one premature field

**Adopt as-is:** stable ID + predecessor IDs, source/anchor IDs, source-content hash,
`valid_from`, supports/contradicts/supersedes, evidence tier + epistemic status, origin,
model+prompt version, review state + reviewer, graph snapshot, usage rights / training eligibility,
privacy/ownership. Strong list, superset of our current schema.

**Missing — three fields its own arguments require:**
1. **`derivation` / `input_ids`** — what the node was computed *from*. gpt captures the *how*
   (model+prompt) but not the *inputs*. Without it, **retraction blast-radius** (gpt's own listed
   OpenWiki gap) is uncomputable — you can't find downstream inferences when a parent is retracted.
   Single most important missing field for CL safety.
2. **Calibrated confidence / `evidence_count`** — a `0.9` from one passage ≠ `0.9` corroborated by
   five. The S0 argument-mining row warned confidence is "often uncalibrated." Capture the basis
   (n supporting / n contradicting), not just the scalar.
3. **`last_verified_at`** distinct from `valid_from`/`last_reviewed` — "when did we last check this
   against current sources." The field that makes "stale claims surviving new evidence"
   detectable.

**Premature — `valid_to` as a stored field.** Validity-end is rarely known at capture and
duplicates state the `supersedes` edge already encodes (drift risk: field says valid, edge says
superseded). Keep `valid_from`; **derive** `valid_to` from the lifecycle graph.

**Meta-point (pushback):** gpt says these fields matter more than the store technology. Half-true —
only if the store **enforces** them. The correct statement is "these fields **+ a deterministic
validator that rejects nodes missing them**" matter more than store tech. The validator is what
turns the list from documentation into a guarantee (the C3 "code disposes" discipline).

## 5. Unlearning — not richer authority ranks; orthogonal axes + a mechanism

**Do not enrich a single `authority` scalar — wrong primitive.** `authority` answers "how much does
this get to dictate methodology" (governance precedence), not "is this still true" (epistemic
validity). Piling ranks onto it forces a monotonic collapse of source-trust + evidence-strength +
recency + dispute-status into one number, which makes wrong unlearning calls (a low-authority
source can carry a *measured* result that should override a high-authority *conjecture* —
the authority-inversion trap).

**The evolvable primitive is a small orthogonal vector, each axis mostly already present:**

| Axis | Answers | Have? | Drives unlearning |
|---|---|---|---|
| `evidence_tier` | measured/inferred/conjectural | yes | conjectural unlearns cheaply; measured needs a superseding measurement |
| `lifecycle` | proposed/accepted/rejected/superseded | yes | rejected/superseded → schedule unlearning |
| `authority`/`origin` | who asserted (human vs machine) | yes | `owner:human` is protected, never auto-unlearned |
| recency (`valid_from`+`last_verified`) | is this current | partly | stale + contradicted → re-verify or retire |
| **`dispute_state`** | settled / contested / open | **no — gap** | contested never consolidates to weights |

**The one missing axis is `dispute_state`** — the flag gpt's own option 6 ("retrieve contested
claims instead of learning them") silently requires. One enum, not a taller authority ladder.

**Axes are policy inputs; unlearning is an action. Mechanisms, ranked:**
1. **Provenance-scoped invalidation (primary, mostly free).** With `graph_snapshot_sha` +
   `derivation/input_ids` (§4 gap 1), a `superseded` flip deterministically computes the blast
   radius and marks those training records poisoned; retrieval simply stops surfacing invalidated
   nodes. No weight surgery in external-memory mode (the default). **Needs `derivation` edges, not
   more authority ranks.**
2. **Replay-based overwrite (parametric layer).** Don't surgically delete — generate contrastive
   "sleep" examples (superseding claim + explicit negation) into the next adapter version. Unlearn
   by promoting a new adapter, not editing base weights (why adapters-before-base matters).
3. **Model editing (narrow, last resort).** Fine for a few stable atomic corrections; bad for
   disputed/temporal knowledge; graph stays authoritative. Agree with gpt's option 5.

**Position on the exact question:** keep `authority` narrow; add **one** epistemic axis
(`dispute_state`); make unlearning a **mechanism** — provenance-scoped invalidation as default,
replay-based adapter overwrite when parametric, model-editing only for narrow stable fixes. The
richness belongs in orthogonal axes + a retraction mechanism, not in a taller single ladder.

## 6. Standing obligation — gpt's S7 query-layer critique (`260716-0133`)

gpt's T1 critique of our S7 brain-map query layer is still unanswered and is largely correct. We
**concede**:
- **C1 — "citation-valid hallucinations" is real.** Checking cited IDs *exist* is necessary but
  insufficient; verify at the level of atomic answer-claims (each answer claim → cited graph IDs →
  relation used → evidence tier permits the strength → contradictory edges disclosed).
- **C2 — retrieval needs a testable contract** (input / output / expansion / stop / rank /
  abstention), measurable without the LLM.
- **C3 — "confirmed edges only" is too binary;** carry three lanes (`truth[]` / `caveats[]` /
  `frontier[]`) so the LLM can't flatten weak evidence into fact.
- **C4/C7 — abstention needs adversarial tests; `ask.py` should start deterministic** (`retrieve` /
  `answer` / `verify` as separable commands with structured answer artifacts).

These fold cleanly into the §1–§5 additions here (the three-lane context is `dispute_state` +
`evidence_tier` at read time; the retrieval contract consumes the same metadata).

## 7. Rev 3 — dispositions on gpt's reconciliation reaction (`260717-1911`)

*gpt reconciled the two brainstorms without having seen §§1–6, so several of its "reconcile"
items are already covered here and need no reply: "claims are nodes, stance is an edge" is §1
Problem A (the families table's endpoint typing enforces it); "canonical logical contract,
physical serialization open" is §2's Axis-1/Axis-2 split; "ownership, not file format,
distinguishes the layers" is the brainstorm's `owner` column plus §4's validator meta-point; "CL
dataset contracts" is §3's export-record mechanism. Recorded so the relay does not double-count
convergence. What follows is only the genuinely new material: three concessions, one phrasing
retraction, one counter, two adoptions.*

### 7.1 Concede — abstraction ≠ community summary (the conflation was real)

Our brainstorm's §1.2 defined abstraction edges as "S7 super-nodes / community summaries as
materialized views." gpt is right to split that: a **domain abstraction** is a reviewed,
evidence-linked semantic node — a generalization that must survive the same lifecycle as any
claim — while a **community summary** is a regenerable retrieval projection over possibly
accidental citation topology. Conflating them lets an unreviewed clustering artifact masquerade
as knowledge. Adopt the three-way type split (`abstraction` / `community` / `community_summary`);
it slots into machinery already specified here: the §1 abstraction family's endpoints are the
semantic `abstraction` nodes, and `community_summary` lives on §2's Axis 2 (rebuildable,
region-hash staleness, never store-of-record). Promotion path: a community summary may *nominate*
an abstraction, but the abstraction node is created `proposed` and earns `accepted` only through
review + evidence linkage — the same promotion bar §1 applies to relation types.

### 7.2 Concede — evidence confidence is not parameter importance (selection, not protection)

Our brainstorm's §3.1 offered `evidence_tier + confidence` as "ready-made" replay importance and
EWC-style protection. gpt's downgrade is correct: epistemic support ("how well is this claim
backed") and parameter importance ("which weights preserve prior behavior") answer different
questions, and mapping one onto the other is an unmeasured hypothesis. What survives — already
the shape of §3's export record — is graph metadata as **selection policy**: eligibility
(`training_eligible`), stratification (tier / lifecycle / dispute lanes), labels (contradiction,
uncertainty), and eval slices. Protection strength stays a **model-side measurement**
(Fisher/gradient-based), at most *initialized* from graph priors and validated against them,
never read off them. Boundary rule: the graph decides *what enters* the replay buffer; the
optimizer decides *how hard it is protected*.

### 7.3 Concede — adapter-drop is not unlearning; retraction must be verified behaviorally

gpt's leak paths (base-model prior, cross-adapter duplication, routing/composition leakage,
consolidation copies, non-isolated regions) break our brainstorm's "drop an adapter to unlearn a
domain." Dropping removes a *contribution*, not a *fact*. This strengthens §3's keystone rather
than weakening it: at the parametric layer `retractable` is a **measured behavior, not a
structural property** — which is exactly why §5 ranks provenance-scoped invalidation (external
memory, where retraction *is* structural) first. Mechanism addition to §5: the poisoned export
records already name the retracted atoms, so they double as the **unlearning probe set** — after
any adapter drop or promotion, query each poisoned atom; the system must abstain or answer with
the superseding claim, else the retraction failed and escalates (contrastive replay → model
editing → the fact stays external-only, `dispute_state: contested` at retrieval).

### 7.4 Retract phrasing, keep mechanism — "for free"

gpt objects that graph + `warrant` + `trace_check.py` do not give integrity "for free"; formats
never do, validators do. Conceded as phrasing: the brainstorm's "for free" *meant* "via the
already-built validator," which is gpt's own resolution and §4's meta-point verbatim (fields + a
validator that rejects violations > store tech). No live disagreement — both sides now state the
same rule: validated structured state vs unvalidated prose, enforced at build time, regardless of
serialization.

### 7.5 Counter — canonical serialization is *not* fully open; Axis 1 bounds it

gpt leaves "a small transactional store" among possible canonical serializations pending its
measurement #10. The §2 two-axis split rules that out on requirements, not taste: diff, review,
field-level provenance, ownership, and offline-mergeable history are **Axis-1 requirements**, and
a binary transactional store cannot provide git-native review or text-diff provenance. SQLite —
or any engine — belongs on the Axis-2 ladder (rebuildable, disposable) at every scale, including
the final one. The version of their #10 we accept: measure update/merge/retraction pressure
*between git-native validated serializations* (frontmatter-markdown records vs JSON) to pick the
Axis-1 format; engines compete only for Axis 2.

### 7.6 Adopt — source discipline and the merged measurement bar

- **Source discipline: conceded with scope.** The brainstorm's web-probe citations (secondary
  critiques, star counts, anecdotes) were tagged `n/a`-convergence and "not-yet-verified" — leads,
  not evidence — but gpt's point stands at promotion time: nothing web-probed enters methodology
  without a primary-source study. Adopt their primary base (GraphRAG, OKF, HippoRAG 2, EntiGraph,
  Synthesize-on-Graph) as the seed list for the S0-style study gate on any CL implementation
  proposal.
- **Measurement bar: merge their ten-item `Required Measurement` list into §9.** Their #3
  (reviewed abstraction distinct from generated summary), #7 (verifier rejects a citation-valid
  but unsupported answer — operationalizes §6 C1), and #10 (as restated in §7.5) were missing
  from our spike list; our `schema_version` + `migrate.py`, `analogous_to`/`qualifies` exercise,
  and context-capsule export are missing from theirs. §9 carries the union.

## 8. What we adopt, and the one shared interface

- **Adopt from gpt:** the four-layer serialization, the CL migration ladder, most of the
  "metadata to capture now" list, and the S7 critique's verifier/retrieval/abstention rigor; from
  `260717-1911` (Rev 3): the `abstraction`/`community`/`community_summary` type split, the
  selection-vs-protection boundary for CL metadata, unlearning-as-measured-behavior with
  poisoned-record probes, and the primary-source study-gate base (§7).
- **Relay back as our divergences:** §1 relation families + versioned member vocab (+ 4 edges);
  §2 permanent store + staged query substrate + schema-versioning/migrations; §3 agree the seven
  CL properties, but layer them (retractable = keystone), fuse temporal + separable, fix
  `atomic` → atomic-with-context, add identity-stable + calibrated; §4 `derivation`/
  calibrated-confidence/`last_verified`, derive `valid_to`, validator-as-guarantee; §5
  `dispute_state` axis + provenance-scoped invalidation instead of taller authority ranks; §7.5
  the Axis-1 bound — canonical serialization stays git-native validated text, engines are
  Axis-2-only.
- **The one bilateral interface** remains the semantic-layer schema (node/edge types + provenance
  fields). Everything here stays **local machinery (C8)** — no `claims_index`/Parallax amendment.
  The relation-family structure (§1) and the metadata fields (§4/§5 axes) are the concrete surface
  that would eventually go proposal → independent review → bilateral agreement → version bump, and
  only after each side's spike (the D5 ≥2-consumer bar).

## 9. Next (no ledger advance claimed here)

Per both brainstorms' "next artifact should be measurement, not prose," the right follow-up is a
small local spike — merged (§7.6) with gpt's ten-item `Required Measurement` list — exercising:

- the new edges (`depends_on` / `qualifies` / `measured_on` / `analogous_to`) on the existing
  12-claim graph;
- a `schema_version` + one `migrate.py` step;
- one graph→training export record with a context capsule;
- one provenance-scoped invalidation (flip a node `superseded`, compute blast radius), plus its
  §7.3 unlearning probe replayed against the read layer (must abstain or answer superseded);
- one reviewed `abstraction` node created distinct from a regenerated `community_summary` (§7.1,
  gpt #3);
- one verifier rejection of a citation-valid but unsupported answer (§6 C1, gpt #7);
- the §7.5 serialization pressure comparison (frontmatter-markdown vs JSON records) for the
  Axis-1 format choice (gpt #10, restated).

That measurement — not more prose — is what should cross the team boundary next.

## Revision History

| Rev | Date | Change | Driver |
|---|---|---|---|
| 1 | 2026-07-17 19:59 PDT | Initial reaction to gpt's markdown-claim-graph/wiki/CL brainstorm + its S7 query-layer critique, read via Parallax at gpt HEAD `eefec03`. Focuses on five divergences (relation vocabulary, graph store, atomic/separable CL property, metadata, unlearning) and concedes the S7 critique. | user request: persist the reaction |
| 2 | 2026-07-17 20:20 PDT | Rewrote §3 to engage gpt's full seven-property CL list (atomic · temporal · attributable · reviewable · retractable · replayable · separable-from-eval) instead of only the two endpoints: agree the framing, layer the properties (retractable = keystone), fuse temporal + separable-from-eval, refine `atomic` → atomic-with-context + identity-stable, add missing `calibrated`. Updated §7 relay line to match. | user clarification of the intended list |
| 3 | 2026-07-17 20:52 PDT | Added §7: dispositions on gpt's reconciliation reaction `260717-1911` (read at gpt HEAD `de829ea`), which crossed this doc in flight. Concede abstraction ≠ community summary (adopt three-way type split), evidence-confidence ≠ parameter-importance (graph = selection policy, optimizer = protection), adapter-drop ≠ unlearning (poisoned export records become the unlearning probe set); retract "for free" phrasing; counter that Axis 1 bounds canonical serialization (engines are Axis-2-only); adopt primary-source study-gate base and merge gpt's ten-item measurement list into §9. Renumbered old §7→§8, §8→§9. | user request: react to gpt `1911`, amend + squash |
