---
artifact_type: study
authority: derived
generated_by: s0-existing-art-review
convergence: n/a
parent_artifacts:
  - AGENTS.md
  - .plan/260717-1827-brainstorm-graphrag-wiki-cl-migration.md
  - .plan/260717-2142-proposal-opportunity-engine-existing-art-s0.md
  - .plan/260719-1336-reaction-gpt-execution-proposal-moat.md
  - paper-library/schemas/edges.schema.json
tags: [gray-literature, white-papers, tech-reports, conflicting-claims, verification, provenance, content-drift, sponsorship-bias, argumentation, truth-discovery, dispute-node, stake, study-gate, s0]
---

# S0 — Existing-Art Study: Gray Literature, Conflicting Claims, and What "Verification" Can Mean on the Graph

*Bounded existing-art study satisfying the study-gate (AGENTS.md) before the corpus is widened from
peer-reviewed papers to **white papers and tech reports**, and before any "claim verification"
machinery is built. Scope fixed by the originating user prompt — expand beyond peer-reviewed papers
to white papers and tech reports; in a field where multiple such sources cover related topics with
**conflicting claims**, how do we address that? Do we envision a system to **verify their claims**?
what are the **implications of verification and how do we represent them in the graph**? Done
S0-style: one table per body (primitive · reuse · avoid · failure-mode-for-our-graph), a
representation synthesis, a study-gate verdict, and a bounded spike. Timestamp from `date`:
2026-07-20 10:00 PDT.*

*Authority: `derived` — systematic synthesis of external primary sources for internal use. Not
measurement, not an implementation plan. It grounds and **bounds** the corpus-expansion ambition
before we build.*

*Convergence: `n/a` — a local study over external primary art; this expansion was not shared with
gpt, so there is no corroboration claim. What earns weight below is the web-verified primary-source
record, read this session (see the verification ledger before Sources — several items are
explicitly flagged as substance-verified-but-quotation-pending).*

---

## 0. Why this study exists — the expansion is not "more sources," it is "less warrant"

The tempting framing is that white papers and tech reports are *lower-quality papers* and need a
quality filter. That framing is wrong twice.

First, it is **factually wrong about ML**: in this field the tech report often *is* the primary
literature — frontier model reports, system cards, benchmark releases — and a vendor white paper
with released code and standard benchmarks is more *checkable* than a peer-reviewed paper with no
artifacts. The axis is not quality.

Second, it hides what actually changes. Peer review supplied four weak, implicit guarantees. Drop
it and each one must become **explicit graph content** — a field, an edge, or a check the code owns
— or the graph silently inherits an assumption that no longer holds:

| Implicit guarantee under peer review | Holds for papers | Breaks for gray lit | What must become explicit |
|---|---|---|---|
| Source is **immutable** (DOI, frozen) | yes | URLs edited silently; versions superseded | captured-state anchor: `retrieved_at` + content hash + snapshot; drift detection |
| Claimant is **disinterested** | weakly | vendor claims about own product; lab about own model | **stake represented as edges**, not assumed away |
| Method is **disclosed** | usually | "leading competitor", unnamed baseline, self-selected benchmark | **checkability** as a first-class, computable property |
| Sources are **independent** | mostly | whitepaper→blog→whitepaper laundering; shared funders | independence **computed** from the graph, not counted |

So the study's spine is: the expansion breaks these four assumptions, each broken assumption has a
mature prior-art body that says how to repair it *without* a bespoke engine, and the repair in every
case is a typed-graph move our substrate is already built to make. As with the opportunity-engine
S0 (`260717-2142`), the main result is **subtraction** — and one sharp boundary on what "verify"
is even allowed to mean.

---

## 1. The decomposition — the user's three questions, six bodies of prior art

| User question | Sub-problem | Prior-art body | Study § |
|---|---|---|---|
| (implicit) sources are now mutable & interested | source drift, versioning, stake, citation laundering | reference rot / Memento / W3C PROV / Model Cards / Greenberg | §2 |
| how to address conflicting claims of varying quality? | appraise a body of mixed evidence **without a scalar** | GRADE · Cochrane RoB 2 / ROBINS-I · AMSTAR 2 | §3 |
| why do the conflicts even arise? | gray-lit effect inflation; **sponsorship bias orthogonal to quality** | AACODS · Lundh (Cochrane) · McAuley (Lancet) · preprint-vs-published | §4 |
| how to represent conflicting claims without adjudicating? | formal semantics of dispute; hold conflict side-by-side | Dung AF · Bipolar AF · ASPIC+ · AGM | §5 |
| should the system infer which claim is true? | joint source-reliability + fact-truth estimation — the tempting wrong turn | TruthFinder · copy detection · Knowledge-Based Trust | §6 |
| do we envision a system to verify claims? | what automated verification can and cannot do | FEVER · SciFact / SciFact-Open · fact-checking survey · decontextualization · sycophancy | §7 |

The load-bearing findings, up front: conflicts mostly **aren't** conflicts until claims are aligned
on scope (§3/§5); the correct representation of a real conflict is a **first-class dispute the
system never adjudicates** (§5), because the one literature that *does* adjudicate relies on an
independence assumption that gray literature specifically destroys (§6); and "verify" must be
scoped to **warrant, not truth** (§7), where the graph's real, under-exploited edge is that stake
and independence become **computable** rather than annotated (§2).

---

## 2. Source mutability, stake, and citation laundering — immutability was misplaced onto the wrong object

The immutability assumption is not *broken* by gray literature; it was attached to the wrong thing.
Two independent standards bodies converge on the same fix: the citable unit is a **state, not a
locator**.

| Facet | Finding |
|---|---|
| Primitive | **Content drift is silent and is the default, not the exception.** Klein et al., *PLoS ONE* 2014 ("Scholarly Context Not Found") separate **link rot** (dereference fails — detectable) from **content drift** (resource silently changes — a `200 OK` is *not* evidence of stability); ~1 in 5 STM articles suffer reference rot, 7 in 10 among those citing the web. Jones et al., *PLoS ONE* 2016 ("Scholarly Context Adrift"): **76.35% (184,065/241,091)** of references had drifted from their referenced state, drift monotonic in age. The remedy standard is a **triple, not a URL**: Robust Links (Los Alamos/Hiberlink) stores `(data-originalurl, data-versionurl, data-versiondate)`; Memento (**RFC 7089**, Informational) adds time-based content negotiation (`Accept-Datetime` → `Memento-Datetime`, TimeMap version enumeration). **W3C PROV** (PROV-DM/PROV-O, W3C Rec 2013) supplies the modeling: `specializationOf` (the URL names a general entity; each captured snapshot is a more-constrained entity), `wasDerivedFrom` + `prov:Revision` (v2 from v1, each a separate immutable entity with its own hash), and — the key one for stake — **`actedOnBehalfOf`**: "assignment of authority… to a delegate… **while the agent it acts on behalf of retains some responsibility for the outcome**." Documentation artifacts already concede mutability: **Model Cards** (Mitchell et al., FAT* 2019) mandate `model version` + `model date` + `citation`; **Datasheets** (Gebru et al., CACM 2021) mandate a *Maintenance* section (update cadence, old-version retention, errata). Greenberg (*BMJ* 2009) documents **citation laundering** empirically: 242 papers / 675 citations / 220,553 citation paths inflated an unfounded claim to fact; 94% of primary-data citations flowed to 4 supportive papers, 6% to 6 refuting ones — "amplification" and "dead-end citation" turned hypothesis into fact by citation alone. |
| Reuse | Anchor immutability to the **captured state**: `original_uri` + `snapshot_uri` + `retrieved_at` + `content_hash` (Robust Links + the hash it lacks), the document a mutable entity with `wasDerivedFrom`/`Revision` edges between immutable versions — immutability survives intact, exactly the position our brainstorm `260717-1827` Q1 defended (graph is truth, render is disposable), now extended to the source layer. **Stake becomes a path, not an attribute**: model author→employer→funder as an `actedOnBehalfOf` chain with `qualifiedDelegation` carrying the *kind* (employment/funding/advisory); interest is then a graph traversal. This is what makes **independence computable** — two supporting sources are independent iff no shared author/org/funder path connects them, which upgrades our existing single-provenance-chain lint (opportunity-engine §6) into an independence-aware corroboration count that citation counting structurally cannot do. Greenberg gives a typed vocabulary of **bad citation edges** (`cites-supporting-primary-data` vs `amplification` (no data) vs `dead-end` (nothing relevant) vs `diversion` (altered meaning)); amplification and dead-end are detectable **from topology + a `has_primary_data` flag alone**, no reading required. Adopt Model Card / Datasheet field names verbatim as typed properties for tech-report sources — interoperability with artifacts that already ship in that format. |
| Avoid | A `200 OK` or an unchanged hash of *archive-rendered* HTML is not proof of stability — RFC 7089 warns Mementos differ by format migration/branding, so hash the canonicalized payload you captured, not the live or archived render; prose needs a **similarity fingerprint** (Simhash) beside the exact hash or every whitespace/analytics-token change is a false-positive drift. PROV has **no vocabulary for stake, conflict, or bias** — `actedOnBehalfOf` means "spoke for," not "was compromised by"; keep the adversarial-interest edge distinct or the two conflate. All of Model Cards / Datasheets / System Cards are **self-reported and unaudited by design** — they are claims by an interested agent (`wasAttributedTo` the vendor), never ground truth. "System Card" has **no citable standard** (Meta 2022 tech report, no DOI/schema) — itself a live instance of the problem. Greenberg's distortion taxonomy needs human judgment to attribute intent; topology flags structure, not bad faith. |
| Failure mode for our graph | The expansion's first requirement is a **content-drift detector** (hash + Simhash over captured state, fork-into-versions on change, emit a delta event → the existing chain-reaction machinery, opportunity-engine §2 — no new engine). Its second is that **stake and independence must be edges the code can traverse**, or every downstream check that says "corroborated" is counting laundered copies. Neither is new machinery; both are the typed graph doing what prose provenance cannot. |

---

## 3. Appraising mixed-quality evidence — the field's answer is *never a single score*

Medicine spent forty years learning not to reduce a body of conflicting evidence to one number.
That is directly our "don't collapse source quality to a credibility scalar" instinct, with the
receipts.

| Facet | Finding |
|---|---|
| Primitive | **GRADE** (Guyatt et al., *BMJ* 2008;336:924) rates certainty of a *body* of evidence per outcome on four ordered levels — **High / Moderate / Low / Very low** — by moving down **five downgrade domains** (risk of bias, inconsistency, indirectness, imprecision, publication bias) and up **three upgrade factors** (large effect, dose-response gradient, plausible residual confounding would shrink the effect); it keeps *certainty* and *recommendation strength* as **separate axes** and presents them as an Evidence Profile / Summary-of-Findings **table**, never a scalar. **Cochrane RoB 2** (Sterne et al., *BMJ* 2019;366:l4898) assesses bias at the **result** level across five domains (randomization; deviations from intended interventions; missing outcome data; measurement of the outcome; selection of the reported result) via **signalling questions → deterministic algorithm → categorical judgement** (Low / Some concerns / High). **ROBINS-I** (Sterne et al., *BMJ* 2016;355:i4919), for non-randomized studies, adds a confounding domain and a finer ordered scale (Low / Moderate / Serious / Critical / No information). **AMSTAR 2** (Shea et al., *BMJ* 2017;358:j4008) rates overall confidence (High / Moderate / Low / Critically low) by **critical vs non-critical** flaws: one *critical* flaw drops confidence regardless of how many other items pass — an explicitly **non-additive** rule. |
| Reuse | The five downgrade domains + three upgrade factors are a **fixed, named appraisal vocabulary** — store each as a typed qualifier on the evidence/derivation frame, never summed. The **signalling-question → algorithm → category** shape *is* our "LLM proposes, deterministic code disposes": the model answers Yes/Probably-yes/…, the code runs the algorithm and owns the judgement. Two structural borrows are load-bearing: (a) **keep certainty and normative strength separate** — mirrors our assertion frame's `modality: normative` vs `observed/inferred` split; (b) **AMSTAR 2's critical-flaw rule is a non-monotone deterministic gate** — a single disqualifying failure (e.g. undisclosed method, §2 stake) forces a claim to low trust *regardless of supporting-edge count*, which is exactly the aggregation discipline that stops "many laundered copies" from reading as strong support. Appraisal binds to a **claim/result**, not a whole source (RoB 2's result-level unit = our per-assertion granularity). |
| Avoid | Every one of these requires **human judgment at each domain** and has **documented low inter-rater reliability** — for RoB 2, overall-judgement agreement as low as **κ ≈ 0.16** and near-zero/negative in reliability studies (Minozzi et al., *J Clin Epidemiol* 2020;126:37 and 2022;141:99). So this is a **structured-elicitation aid, not an oracle**: adopt the *vocabulary and the non-additive algorithm*, not a pretense of reproducible scoring. GRADE's "publication bias" and "risk of bias" domains **assume disclosed methods and independent sources** — both violated by our new corpus, so they must be adapted, not imported. The canonical warning against the thing we already reject: summing domain scores weights non-exchangeable bias mechanisms arbitrarily and **masks a single fatal flaw** (Jüni et al., *JAMA* 1999;282:1054, "The hazards of scoring the quality of clinical trials"). |
| Failure mode for our graph | The representation of "how good is this evidence" must be a **structured multi-domain record with a non-additive combination rule**, not a number — and it must be honest that the *domain judgements* are noisy LLM-proposed values the human can override. This is cheap (a typed qualifier bundle + a deterministic critical-flaw rule) and it is the direct answer to the user's "conflicting claims of varying quality": you do not rank them by a quality scalar, you **display the appraisal axes and let the disqualifying flaws gate**. |

---

## 4. Why the conflicts arise — gray-lit effect inflation and sponsorship bias *orthogonal to quality*

This body supplies the empirical warrant for treating **stake as an independent axis** (§2/§3) and
for **including** gray literature rather than filtering it.

| Facet | Finding |
|---|---|
| Primitive | **AACODS** (Tyndall, Flinders 2010) is the gray-lit appraisal checklist where peer-review tools don't apply — **Authority · Accuracy · Coverage · Objectivity · Date · Significance** — with *Objectivity* the explicit interest/bias prompt. "Gray literature" is formally the Luxembourg/Prague definition: "produced on all levels of government, academics, business and industry… **not controlled by commercial publishers**, i.e. where publishing is not the primary activity of the producing body" — explicitly including **white papers and technical reports**. The empirical core: **Lundh et al.**, "Industry sponsorship and research outcome," *Cochrane Database Syst Rev* 2017;MR000033 — industry-sponsored studies more often report favourable **results (RR 1.27, 95% CI 1.17–1.37)** and favourable **conclusions (RR 1.34, 1.19–1.51)**, with **lower** results-vs-conclusion concordance (**RR 0.83, 0.70–0.98** = measurable "spin"), and the load-bearing sentence: *"an industry bias that cannot be explained by standard 'Risk of bias' assessments."* **McAuley et al.** (*Lancet* 2000): excluding gray literature inflates pooled effect by **~15%** (ratio of ORs 1.15, 1.04–1.28; 1.33 excluding abstracts); Hopewell et al. (*Cochrane* 2007) corroborate **~9%** (ROR 1.09, 1.03–1.16). Preprint→published conclusion stability: Brierley et al. (*PLOS Biology* 2022) — abstract conclusions changed in 7.2% (non-COVID)/17.2% (COVID), only **1/184 (0.5%)** directly contradicted; hedging tends to *increase* through review. |
| Reuse | **Lundh is the citation that justifies a separate `stake` axis**: sponsorship bias is *orthogonal to methodological quality*, so a low-RoB rating must **not** clear the conflict flag — the code enforces them as independent (a well-conducted vendor study is still ~1.3× more likely to favour its own product). The results-vs-conclusion discordance (RR 0.83) says **store the conclusion and its underlying result as separately-provenanced nodes** so "spin" surfaces as a mismatch — which our assertion frame (`modality`, `outcome`, `metric`) already supports. AACODS's six criteria map onto per-source provenance fields (Objectivity → the stake flag from §2; Date → drift posture; Coverage → scope tags). McAuley/Hopewell justify a **corpus-completeness / publication-bias indicator**: a claim cluster supported *only* by published, favourable, interested sources carries an expected ~9–15% upward bias — a computable flag, not a correction factor. Brierley licenses treating a preprint as a **versioned node** (`peer_review_status` lifecycle, preprint→published version edge, claim-diff on publication). |
| Avoid | The risk ratios are **population-level signals, not per-study correction factors** (evidence graded moderate-to-very-low; the harms RR crosses 1). "Industry sponsorship" is heterogeneous (funding ≠ authorship ≠ data control) and the mechanism is unidentified — do not arithmetically discount. Gray lit is **not automatically less biased**: Hartling et al. (*BMC MRM* 2017) found unpublished studies were 1.9% of included studies and "rarely impacted results/conclusions" — *except* where studies are few or "there are questionable vested interests in the published literature" (exactly our white-paper case). So **include and weight, do not privilege**. Preprint-stability priors (~90% survive) come from literatures with an eventual peer-review backstop; a vendor white paper has **none**, so do not transfer that prior to stakeholder gray lit. |
| Failure mode for our graph | Stake is not a quality problem to be scored away — it is a **structural axis** that (a) must be represented as edges (§2), (b) must not be absorbed into any quality rating (Lundh), and (c) gates aggregation (a corroboration count that ignores shared funders is measuring laundering). The "conflicting claims" the user asks about are, empirically, often **stake-driven favourability differences on the same underlying measurement** — which points straight at alignment-before-adjudication (§5). |

---

## 5. Representing conflict without adjudicating — abstract argumentation, cheaply

There is a formal, decades-old apparatus for holding conflicting claims side-by-side and
characterizing which sets are jointly tenable **without asserting truth** — exactly the user's
requirement. The lesson is to borrow its *vocabulary and its cheapest semantics*, not its engine.

| Facet | Finding |
|---|---|
| Primitive | **Dung's abstract argumentation framework** (*Artificial Intelligence* 1995;77:321) is a pair ⟨arguments, attack-relation⟩ with **extensions** = sets of jointly-defensible arguments under a chosen semantics: **conflict-free ⊂ admissible ⊂ complete**, then **grounded** (unique, ⊆-minimal, *skeptical* — accepts only what must be), **preferred** (⊆-maximal admissible, *credulous* — multiple coherent viewpoints), **stable** (attacks everything outside; may not exist). **Bipolar AF** (Cayrol & Lagasquie-Schiex, ECSQARU 2005; survey *IJAR* 2013) adds an independent **support** relation beside attack — the direct formal answer to "we have both `supports` and `contradicts`" — but flags that "support" is **not one primitive**: deductive vs necessary vs evidential support induce different semantics. **ASPIC+** (Modgil & Prakken, *Argument & Computation* 2014) gives arguments internal structure and a conflict taxonomy — **rebut** (conflicting conclusions), **undercut** (attack an inference), **undermine** (attack a premise). **AGM belief revision** (Alchourrón, Gärdenfors, Makinson, *JSL* 1985) formalizes expansion/revision/contraction under **success** (new info accepted) and **consistency** postulates. |
| Reuse | Our `contradicts` edge **is** Dung's attack relation; reporting "these claims form a mutual-attack cycle with no stable extension" is dispute-characterization, not adjudication — precisely what the user wants. The **grounded extension** gives a cheap, unique, always-exists **in / out / undecided** labeling of "what is uncontested vs disputed," and it is **polynomial** (§complexity below). Bipolar AF validates keeping `supports` and `contradicts` as *independent* typed relations (our design) rather than compiling to pure attack; and its "support is ambiguous" warning maps onto our own distinctions — `depends_on` ≈ **necessary** support, evidential `supports` ≈ **evidential** support — telling us to *tag the variant*. ASPIC+'s rebut/undercut/undermine become **edge subtypes**: our `qualifies` ≈ undercut (challenges applicability without denying the conclusion — the §3 scope move), `contradicts` ≈ rebut/undermine. AGM supplies the *vocabulary* for the `supersedes`/versioning axis (success = a newer/authoritative claim overrides; minimal change = don't discard more than needed). |
| Avoid | **Do not run the acceptability closure.** Only grounded is tractable: credulous acceptance under preferred/stable is **NP-complete**, skeptical under **preferred is Π₂ᵖ-complete** (Dvořák & Dunne, *Handbook of Formal Argumentation* 2018) — computing "all coherent maximal viewpoints" on demand is worse than NP for a personal library. Abstract AF also *discards the reason* for a conflict (it knows "a attacks b," not why) — which is why §3's typed appraisal and §2's stake edges have to carry the substance. **AGM is the wrong model for the conflict axis**: it assumes a logically-closed belief set (**logical omniscience**, computationally unreal) and *resolves* conflict by **deletion** — the opposite of holding claims side-by-side. Full ASPIC+ re-introduces a derivation engine; borrow the taxonomy, skip the machinery. |
| Failure mode for our graph | The right build is **a first-class `dispute` node + grounded-style labeling**, nothing heavier. An edge `A contradicts B` cannot carry an n-way disagreement, the alignment status, the dispute *type*, or what would resolve it; a dispute node can, and it clears the promotion bar (opportunity-engine §3) because it has real consumers — the digest (open disputes), the answer path (contradiction disclosure), the blind-spot audit, and **experiment selection** (a dispute is where the Addendum-A EIG-proxy finds contested mass to resolve). The system computes the grounded in/out/undecided view and **never picks a winner** — same discipline as "never machine-declare novel." |

---

## 6. The tempting wrong turn — truth discovery fails on exactly our corpus

There is a whole literature that *does* infer which conflicting claim is true, by jointly estimating
source reliability and fact confidence. It is worth naming precisely so we can **refuse it for the
right reason**: its three core assumptions are the three gray literature destroys.

| Facet | Finding |
|---|---|
| Primitive | **Truth discovery / data fusion** jointly estimates source trustworthiness and fact veracity by iterative fixpoint — verbatim (**TruthFinder**, Yin, Han, Yu, KDD 2007, pp. 1048–1052; *IEEE TKDE* 20(6):796, 2008): "a web site is trustworthy if it provides many pieces of true information, and a piece of information is likely to be true if it is provided by many trustworthy web sites"; its motivating example shows high-authority (popular) sources were often the *less* accurate ones — link-authority ≠ correctness. The **critical** result for us is source-dependence work: Dong, Berti-Équille & Srivastava, "Integrating Conflicting Data: The Role of Source Dependence" (*PVLDB* 2(1):550–561, 2009) and "Truth Discovery and Copying Detection in a Dynamic World" (*PVLDB* 2(1):562–573, 2009). Their detection principle, verbatim: "sharing the same false value is a rare event when the sources are fully independent. Thus, if two data sources share a lot of false values, they are more likely to be dependent" — and the direction heuristic: the source whose common data is *less* accurate is the likely **copier**. Their Table-1 example is exactly our worry: a copy cluster (S3→S4,S5 sharing the same errors) makes "a naive voting consider them as the majority and so make wrong decisions." **Knowledge-Based Trust** (Dong et al., *PVLDB* 8(9):938–949, 2015; arXiv:1502.03519) scores a source by the correctness of facts it extracts (endogenous), separating *extraction* errors from *source* errors — over 2.8B facts / 119M pages. The survey (Li et al., "A Survey on Truth Discovery," *SIGKDD Explorations* 17(2):1–16, 2016) names the three standing **assumptions** verbatim: **single truth** ("one and only one truth for each object," strengthened so a source "votes against other possible claimed values"), **source consistency** ("a source is likely to provide true information with the same probability for all the objects" — one reliability scalar), and **source independence** ("sources make their observations independently instead of copying from each other"). |
| Reuse | Almost none as an *adjudicator* — but two ideas transfer as **detectors, not deciders**: (a) the copy/dependence model is the one method that *drops* the independence assumption, and its "shared-false-value ⇒ dependent" discounting ports directly onto our graph — where we often already **know** the copy edges (citations), strictly easier than Dong's snapshot-only inference, and the "rare agreement is suspicious" heuristic generalizes to shared funders (co-funded sources agreeing on a stake-favourable claim are treated like copiers, not independent votes) — this is §2's independence-by-traversal and the laundering flag, made algorithmic; (b) KBT's separation of **extraction error vs source error** is a good latent-variable pattern ("we mis-parsed the claim" ≠ "the source is wrong"). |
| Avoid | All **three** named assumptions **fail on our corpus**. *Independence* is violated by design — laundering and shared funders are the norm (§2, §4) and the dependence literature shows this is exactly where vote-counting inverts; worse, stake-motivated sources can **deliberately converge** on the same false claim (collusion without copying), which the shared-false-value signal still flags but whose "who copied whom" story becomes meaningless. *Single truth* is false whenever two "conflicting" numbers are measured under different conditions — **both true at different scope**, not a conflict (§3/§5); truth-discovery has no native scope and its "votes against all other values" rule would **suppress one true value** (the survey's own Honolulu/Hawaii/USA example is non-mutually-exclusive and handled only by a hand-encoded implication function). *Consistent reliability* collapses under stake — an interested source is reliable on background, biased on its own product (Lundh). **KBT specifically begs the question**: it needs a reference base of "true" facts to score against, when the truth is exactly what's contested. So truth discovery here would **launder stake and scope differences into a confident, wrong "truth."** |
| Failure mode for our graph | This body is the **named `avoid` for the whole verification question**: do **not** build a source-reliability-to-fact-truth estimator. Keep only the **dependence-discounting detector**, run over our known citation/co-funder/co-author edges, feeding the independence flag — never a truth verdict. And take the survey's sharpest lesson as a design rule: **resolve scope by keying measurement conditions into object identity**, so differently-scoped claims are about *different objects* and never compete for a single truth; dependence-discounting is then reserved for claims that genuinely share scope (§3 alignment first). Adopting the adjudicator would convert honest disputes (§5) and scope differences (§3) into machine-declared truths — the opposite of the product. |

---

## 7. What "verify" can mean — warrant, not truth

The user asks whether we envision a system to verify claims. The verification literature answers
sharply: automated verification does **faithfulness, checkability, and consistency — never truth** —
and even those degrade hard from benchmark to reality.

| Facet | Finding |
|---|---|
| Primitive | The four things conflated under "verify a claim" are distinct: **is it true** (needs re-running the experiment — out of scope, that's science), **is it faithfully extracted** (does the source say this), **is it checkable** (does the source disclose enough), **is it consistent** (does it clash with the graph). The benchmarks target the last three. **FEVER** (Thorne et al., NAACL 2018; 185,445 claims) labels **SUPPORTED / REFUTED / NOTENOUGHINFO** against retrieved evidence — its own baseline is **31.87%** with required evidence retrieval vs 50.91% label-only, i.e. finding evidence is the hard part. **SciFact** (Wadden et al., EMNLP 2020; 1,409 expert claims) adds **rationale sentences** — verdict *plus the minimal supporting span*. **SciFact-Open** (Wadden et al., Findings EMNLP 2022; ~500K-abstract pool) is the reality check: systems drop **≥15 F1** when evidence must be *found* in a realistic corpus rather than a curated pair. |
| Reuse | This is the exact scope of our **verify gate**, and the literature ratifies its design: SciFact's rationale layer = our "emit the minimal supporting span, not just a verdict" ((b) faithfulness); SciFact-Open = our (d) consistency check at realistic scale; FEVER's **NOTENOUGHINFO** *is* our (c) checkability gate firing — the honest output when a gray-lit source doesn't disclose enough. The fact-checking survey (Guo, Schlichtkrull & Vlachos, *TACL* 2022) is our citable authority that (a) truth over open evidence is unsolved and that justifications should be **extractive (point at spans), not generated**. **Decontextualization** (Choi et al., *TACL* 2021) is the named pre-check: a claim must carry its population/method/conditions before it can be verified — our assertion frame's scope slots, made a pipeline step. |
| Avoid | Two documented traps. **Dataset artifacts**: a **claim-only classifier reaches ~0.61 vs ~0.33 chance on FEVER** without reading any evidence (Schuster et al., EMNLP-IJCNLP 2019) — high accuracy can mean the model is reading *claim style*, not evidence, so any faithfulness scorer **must be ablated against claim-only** and against polarity-flip. **Sycophancy**: RLHF models match the user's stated belief over the truth (Sharma et al., 2023) — an LLM asked "is this claim supported?" is biased to **agree with the claim as framed**, converting a (b)/(d) check into "does this sound assertive." The benchmark-to-real collapse (≥15 F1) means gate performance **must be reported under open retrieval**, never oracle evidence. |
| Failure mode for our graph | The verify gate must (1) be scoped to **warrant, not truth** and say so; (2) be **extractive** (spans, not generated reasons); (3) fire **NOTENOUGHINFO/checkability** as a first-class outcome for undisclosed gray-lit claims — which is *itself the answer* to "can we verify this vendor claim?": often the honest verdict is "the source does not disclose enough to check," and that is a valuable, storable result; (4) be validated with **claim-only and polarity-flip ablations** and **open-retrieval** metrics, or it will overclaim exactly where gray literature is weakest. |

---

## 8. Synthesis — reuse, avoid, and where the graph earns its keep

**Reuse (named, mostly not ours to invent):**
- **Captured-state anchoring + `actedOnBehalfOf` stake chains + version edges** — Robust Links / Memento / PROV (§2).
- **Multi-domain appraisal with a non-additive critical-flaw rule**, certainty separate from strength — GRADE / RoB 2 / AMSTAR 2 (§3).
- **A separate `stake` axis, orthogonal to quality; conclusion-vs-result stored separately** — Lundh / AACODS (§4).
- **A first-class `dispute` node + polynomial grounded labeling**; rebut/undercut/undermine as edge subtypes — Dung / Bipolar AF / ASPIC+ (§5).
- **Copy/dependence detection as a *detector*** feeding the independence flag — truth-discovery's one salvageable part (§6).
- **An extractive, span-emitting verify gate scoped to warrant**, with NOTENOUGHINFO first-class — FEVER / SciFact / SciFact-Open (§7).

**Avoid (the documented anti-patterns):**
- Treating a `200 OK`/unchanged-render hash as stability; overloading `actedOnBehalfOf` as "biased-by"; trusting self-reported cards as ground truth (§2).
- **Any single credibility/quality scalar** — it masks fatal flaws and has poor reproducibility even in medicine (§3, Jüni 1999).
- Folding **stake into quality**, or arithmetically discounting by a population RR (§4).
- Running argumentation's **acceptability closure** (NP-hard→Π₂ᵖ) or adopting **AGM's delete-to-resolve** model (§5).
- Building a **truth-discovery adjudicator** — its independence assumption is exactly what gray lit destroys (§6).
- A verify gate that claims **truth**, generates its justifications, or is scored on **oracle evidence** (§7).

**Where the graph genuinely differs from all of the above (the reinvention we are NOT doing):**
1. **Stake and independence become *computable* from typed provenance edges** (`actedOnBehalfOf` chains, shared-funder paths) — the one move that citation-counting, prose wikis, and truth-discovery all structurally cannot make, and the direct fix for the sponsorship-bias and laundering results (§2/§4/§6).
2. **Conflicts are aligned on scope *before* they count as conflicts** (assertion frame → §3/§5), so most apparent gray-lit contradictions resolve to `qualifies`/scope differences, and only genuine opposed-at-same-scope claims become a `dispute` node the system characterizes but never adjudicates.
3. **"Verification" is honestly bounded to warrant** and its **NOTENOUGHINFO/checkability verdict is a feature** — the correct, storable answer to most undisclosed vendor claims — rather than an over-reaching truth engine.

---

## 9. The representation answer — verification and its implications on the graph

Directly answering the user's third question. Six representation commitments, each grounded above:

1. **Verification results are themselves scoped, timestamped claims — not booleans on a node.** A claim verified against v1.2 is not verified for v2.0. `last_verified_at` (already in the substrate) becomes load-bearing rather than hygienic, and a verification is an object with its own provenance, evidence spans (§7), and scope (§3). Re-verification is a first-class event.
2. **Appraisal is a structured multi-domain record with a non-additive combination rule (§3), never a scalar.** Domain judgements are LLM-proposed, human-overridable; a single *critical* flaw (undisclosed method; §2 stake) gates the claim's trust regardless of supporting-edge count (AMSTAR 2's rule).
3. **Stake is edges, not an attribute (§2).** `author --actedOnBehalfOf--> org`, `org --funds--> study`, `claim --about--> artifact`; interest and independence are **traversals**. A `supports` edge from an interested source toward its own product is down-weighted or held pending an **independent** corroborating claim (independence computed, not counted).
4. **A genuine conflict is a first-class `dispute` node (§5)**, carrying: each `source --asserts--> position` (system never picks), alignment status (aligned-and-opposed vs scope-difference, §3), dispute *type* (measurement / scope / definitional / methodological / interest-driven), the discriminating observation that would resolve it, and resolution status (`open | resolved_by_scope | resolved_by_supersession | resolved_by_replication | unresolvable_as_stated`). Scope is kept out of the dispute set **structurally**: measurement conditions are **keyed into object identity (§6)**, so differently-scoped claims are about *different objects* and never form a `contradicts` edge in the first place — only genuinely same-scope opposition reaches a dispute node. The system publishes the polynomial **grounded** in/out/undecided view; it does not compute winners.
5. **Warrant collapse propagates by dependency strength (§2 + opportunity-engine §2).** Source retracted / drift detected / replication failed → **hard derivation invalidates, evidential recomputes confidence, heuristic notifies** — the existing Δ-propagator with the impact-state enum gpt already specified (`invalid/dirty/confidence_changed/scope_changed/review_required/notification_only`). No new engine.
6. **Failed verification is information, never deletion.** A refuted or uncheckable claim plus *why* is an asset — a negative example, an unlearning probe (moat reaction §5 / CL), and the on-record defense when someone cites it at you. This also makes **"these sources disagree, here is the axis they differ on" a legitimate answer type**, alongside abstention.

Two second-order implications worth stating: **content drift is the sharpest new mechanic** — a hash change forks the source into versions, re-extracts against the new snapshot, and emits a delta event → chain reaction (§2), entirely inside planned machinery; and **verification is a budget** — which claims earn the effort is `high downstream-dependents × high uncertainty × low checkability`, the same EIG-proxy as experiment selection (Addendum A), so disputes (§5) are exactly where verification effort should concentrate.

---

## 10. Study-gate verdict — cleared, bounded, and it *shrinks* the build

**Cleared, and once again the value is subtraction.** Widening to white papers and tech reports is
not naive reinvention *provided* it reuses the six mature bodies and refuses their failure modes.
Concretely the gate turns "verify claims from untrusted sources" into a small, mostly-already-planned
surface:

- "Handle mutable sources" → **captured-state anchor + Simhash drift detector + version edges** (§2); cite Memento/Robust Links/PROV.
- "Represent stake" → **`actedOnBehalfOf` edges + independence-by-traversal** (§2); the sponsorship literature (§4) says it must be *separate from quality*.
- "Appraise mixed quality" → **multi-domain record + non-additive critical-flaw rule** (§3); no scalar, cite GRADE/AMSTAR 2/Jüni.
- "Address conflicting claims" → **align on scope first (assertion frame), then a first-class `dispute` node + grounded labeling** (§3/§5); no argumentation engine, no truth-discovery adjudicator.
- "Verify claims" → **extractive, span-emitting gate scoped to warrant, NOTENOUGHINFO first-class** (§7); cite FEVER/SciFact-Open; do **not** claim truth.

The through-line: the expansion adds **two genuinely new mechanics** — content-drift detection and
stake-as-edges — and both land inside machinery already in flight (the Δ-propagator, the typed
provenance graph). Everything else the corpus-expansion seemed to demand (a credibility scorer, a
truth engine, an argumentation solver) is **refused with a citation**.

---

## 11. Proposal — the bounded "conflicting-gray-lit" spike

Additive to the corrected evidence-to-opportunity spike (the open ledger obligation), local only
(C8). Runs on a small fixture of **one field with 3–4 mixed sources** (≥1 peer-reviewed paper, ≥1
vendor white paper about its own artifact, ≥1 tech report), deliberately containing one genuine
opposed-at-same-scope conflict and one *apparent* conflict that is really a scope difference:

1. **Drift (§2):** capture each source as `(original_uri, snapshot, retrieved_at, content_hash, simhash)`; mutate one source; show the detector forks it into versions and emits a delta event, re-anchoring old claims to the old snapshot.
2. **Stake (§2/§4):** encode `actedOnBehalfOf` chains; show independence computed as a shared-funder/author traversal — two "corroborating" sources that share a funder are flagged **not independent**; the laundering flag fires on an amplification/dead-end citation subgraph with no primary-data leaf.
3. **Alignment before conflict (§3/§5):** re-express the two "conflicting" claims as framed assertions; show the scope-difference pair resolves to `qualifies` (not a conflict), and the genuine pair becomes a **`dispute` node** with dispute-type and a discriminating-observation field.
4. **Appraisal (§3):** attach the multi-domain record; show one *critical* flaw (undisclosed method on the white paper) gates its trust **regardless** of how many `supports` edges point at it — the non-additive rule.
5. **Verify gate scoped to warrant (§7):** run the gate on the disclosed claims (span-emitting) and on the undisclosed vendor claim → **NOTENOUGHINFO/uncheckable**; validate with a claim-only and a polarity-flip ablation to prove the gate reads evidence, not style.
6. **Grounded view (§5):** publish the polynomial in/out/undecided labeling over the `contradicts`/`supports` edges; confirm the system reports the dispute and **never emits a winner**.

Exit: independence correctly distinguishes the shared-funder pair from a genuinely independent one;
the scope-difference is *not* recorded as a conflict while the genuine one *is*; the critical-flaw
rule gates trust non-additively; the gate returns NOTENOUGHINFO on the undisclosed claim and
survives both ablations; no machine-declared truth anywhere. This is the next *measurement* on the
gray-lit question, not more prose.

---

## 12. Cross-team disposition

- **Local machinery (C8).** Nothing here amends the shared `claims_index` or Parallax; it clears
  our study-gate for the corpus expansion and is `derived` prior-art grounding.
- **Not addressed to gpt, not a reaction.** The one reaction for the current cycle is `260719-1336`;
  this is a local study that reads as context on gpt's next sync. It is additive to their execution
  baseline: the **content-drift detector** and **stake-as-edges** land inside their Source layer and
  Δ-engine (their Consensus §1/§3), the **dispute node** is a candidate promotion under their §9
  two-consumer bar, and the **warrant-scoped verify gate** sharpens their verification artifact
  (their Read-Side Contract) with the NOTENOUGHINFO/checkability outcome and the anti-sycophancy
  ablation discipline.
- **Relation to open obligations.** Independent of the corrected evidence-to-opportunity spike; the
  §11 gray-lit spike is a *separate* fixture and should not be merged into it. Storage counter stays
  parked. Pin/ledger advance for the `350c420` cycle still awaits explicit user signal.

## Verification ledger (read before citing)

- **Fully web-verified this session:** all of §2 (Klein 2014 PLoS ONE; Jones 2016 PLoS ONE 76.35%; RFC 7089; Robust Links; PROV-DM/PROV-O relations incl. `actedOnBehalfOf`; Model Cards FAT* 2019; Datasheets CACM 2021; Greenberg BMJ 2009 with the 94%/6% split); §4 (AACODS six criteria + Flinders cite; Luxembourg/Prague definition from the Schöpfel PDF; Lundh Cochrane 2017 RRs 1.27/1.34/0.83 and the "cannot be explained by standard Risk of bias" sentence; McAuley Lancet 2000 ROR 1.15; Hopewell 1.09; Hartling 1.9%; Brierley PLOS Biology 2022 7.2%/17.2%, 1/184); §5 (Dung 1995 AIJ 77:321; Cayrol & Lagasquie-Schiex ECSQARU 2005 + IJAR 2013; Modgil & Prakken 2014; AGM 1985 JSL 50:510; Dvořák & Dunne complexity classes); §7 (FEVER NAACL 2018 185,445/31.87%/50.91%; Schuster EMNLP-IJCNLP 2019 ~0.61 claim-only; SciFact EMNLP 2020 1,409; SciFact-Open Findings EMNLP 2022 ≥15 F1; Guo et al. TACL 2022; Choi et al. TACL 2021; Sharma et al. 2023 sycophancy). §3 core facts (GRADE 4 levels + 5 downgrade + 3 upgrade, Guyatt 2008 BMJ 336:924; RoB 2 five domains + judgements + algorithm from Cochrane Handbook Ch.8; ROBINS-I seven domains + BMJ 2016;355:i4919; AMSTAR 2 four ratings + critical/non-critical, Shea 2017 BMJ 358:j4008; RoB 2 low IRR — Minozzi 2020/2022, κ≈0.16).
- **Substance-verified, exact quotation/number pending:** RoB 2's explicit *discouragement of numeric summary scores* (verified in substance via Handbook Ch.8; the clean verbatim sentence should be pulled from riskofbias.info RoB 2 guidance or Handbook §7.5 before being quoted); the 2011 *J Clin Epidemiol* GRADE-series article numbers; AMSTAR 2's specific 7-critical-item list; GRADE-specific inter-rater κ values (RoB 2's are verified; GRADE's are not — do not quote GRADE κ without fetching Mustafa et al. / Berkman).
- **§6 (truth discovery) — now web-verified from primary PDFs:** TruthFinder (KDD 2007 pp. 1048–1052, primary PDF; verbatim fixpoint) with the *TKDE 20(6):796–808, 2008* record **flagged** (aggregators dblp/Semantic Scholar were down — cite the DOI before publishing); Dong/Berti-Équille/Srivastava dependence (PVLDB 2(1):550–561) + copy-detection (PVLDB 2(1):562–573), 2009, both from primary PDFs incl. the "shared false value is rare among independents" principle and the Table-1 copy-cluster example; Knowledge-Based Trust (PVLDB 8(9):938–949, 2015; arXiv:1502.03519); Li et al. survey (SIGKDD Explorations 17(2):1–16, 2016; arXiv:1505.02463, full text) with the three named assumptions verbatim and the Honolulu/Hawaii/USA scope example. Exact page ranges on the two 2009 papers flagged as established-record (PDFs lack pagination).

## Sources (external primary art, read this session; not repo parent_artifacts)

**Source mutability / provenance / laundering (§2)**
- Klein et al., "Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot," *PLoS ONE* 9(12):e115253, 2014 — link rot vs content drift.
- Jones et al., "Scholarly Context Adrift: Three out of Four URI References Lead to Changed Content," *PLoS ONE* 11(12):e0167475, 2016 — 76.35% drift.
- Van de Sompel, Nelson, Sanderson, "HTTP Framework for Time-Based Access to Resource States — Memento," RFC 7089, IETF, 2013 (Informational).
- Klein, Jones, et al., "Robust Links" specification, Hiberlink/LANL — `(originalurl, versionurl, versiondate)`.
- Moreau & Missier (eds.), "PROV-DM: The PROV Data Model," W3C Recommendation, 2013; Lebo et al., "PROV-O: The PROV Ontology," W3C Rec 2013 — `actedOnBehalfOf`, `specializationOf`, `wasDerivedFrom`/`Revision`.
- Mitchell et al., "Model Cards for Model Reporting," FAT* 2019 — arXiv:1810.03993.
- Gebru et al., "Datasheets for Datasets," *CACM* 64(12):86, 2021 — arXiv:1803.09010.
- Greenberg, "How citation distortions create unfounded authority: analysis of a citation network," *BMJ* 339:b2680, 2009.

**Structured appraisal without a scalar (§3)**
- Guyatt et al., "GRADE: an emerging consensus on rating quality of evidence and strength of recommendations," *BMJ* 336(7650):924, 2008.
- Guyatt et al., "GRADE guidelines: 1. Introduction—GRADE evidence profiles and summary of findings tables," *J Clin Epidemiol* 64(4):383, 2011. *(series article numbers pending)*
- Sterne et al., "RoB 2: a revised tool for assessing risk of bias in randomised trials," *BMJ* 366:l4898, 2019.
- Sterne et al., "ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions," *BMJ* 355:i4919, 2016.
- Shea et al., "AMSTAR 2: a critical appraisal tool for systematic reviews…," *BMJ* 358:j4008, 2017.
- Jüni, Witschi, Bloch, Egger, "The hazards of scoring the quality of clinical trials for meta-analysis," *JAMA* 282(11):1054, 1999.
- Minozzi et al., reliability of RoB 2, *J Clin Epidemiol* 126:37 (2020) and 141:99 (2022) — κ≈0.16 overall.

**Gray literature / sponsorship bias (§4)**
- Tyndall, "AACODS Checklist," Flinders University, 2010 — Authority/Accuracy/Coverage/Objectivity/Date/Significance.
- Schöpfel, "Towards a Prague Definition of Grey Literature," GL12, 2010 — Luxembourg/Prague definition.
- Lundh, Lexchin, Mintzes, Schroll, Bero, "Industry sponsorship and research outcome," *Cochrane Database Syst Rev* MR000033, 2017 — RR 1.27/1.34/0.83; "cannot be explained by standard Risk of bias."
- McAuley, Pham, Tugwell, Moher, "Does the inclusion of grey literature influence estimates of intervention effectiveness…," *Lancet* 356(9237):1228, 2000 — ROR 1.15.
- Hopewell et al., "Grey literature in meta-analyses of randomized trials…," *Cochrane Database Syst Rev* MR000010, 2007 — ROR 1.09.
- Hartling et al., "Grey literature in systematic reviews…," *BMC Med Res Methodol* 17:64, 2017.
- Brierley et al., "Tracking changes between preprint posting and journal publication during a pandemic," *PLOS Biology* 20(2):e3001285, 2022.

**Formal treatment of conflict (§5)**
- Dung, "On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games," *Artificial Intelligence* 77(2):321, 1995.
- Cayrol & Lagasquie-Schiex, "On the Acceptability of Arguments in Bipolar Argumentation Frameworks," ECSQARU 2005; "Bipolarity in argumentation graphs," *IJAR* 54(7):876, 2013.
- Modgil & Prakken, "The ASPIC+ framework for structured argumentation: a tutorial," *Argument & Computation* 5(1):31, 2014.
- Dvořák & Dunne, "Computational Problems in Formal Argumentation and their Complexity," Handbook of Formal Argumentation, 2018 — grounded P; preferred skeptical Π₂ᵖ-complete.
- Alchourrón, Gärdenfors, Makinson, "On the logic of theory change: Partial meet contraction and revision functions," *J. Symbolic Logic* 50(2):510, 1985.

**Truth discovery / data fusion (§6)**
- Yin, Han, Yu, "Truth Discovery with Multiple Conflicting Information Providers on the Web," KDD 2007, pp. 1048–1052; *IEEE TKDE* 20(6):796–808, 2008 *(TKDE record flagged — DOI unverified this session)*.
- Dong, Berti-Équille, Srivastava, "Integrating Conflicting Data: The Role of Source Dependence," *PVLDB* 2(1):550–561, 2009; "Truth Discovery and Copying Detection in a Dynamic World," *PVLDB* 2(1):562–573, 2009.
- Dong, Gabrilovich, Murphy, et al., "Knowledge-Based Trust: Estimating the Trustworthiness of Web Sources," *PVLDB* 8(9):938–949, 2015 — arXiv:1502.03519.
- Li, Gao, Meng, Li, Su, Zhao, Fan, Han, "A Survey on Truth Discovery," *SIGKDD Explorations* 17(2):1–16, 2016 — arXiv:1505.02463.

**Automated claim verification (§7)**
- Thorne, Vlachos, Christodoulopoulos, Mittal, "FEVER: a Large-scale Dataset for Fact Extraction and VERification," NAACL 2018.
- Schuster et al., "Towards Debiasing Fact Verification Models," EMNLP-IJCNLP 2019 — claim-only ~0.61.
- Wadden et al., "Fact or Fiction: Verifying Scientific Claims," EMNLP 2020; "SciFact-Open," Findings of EMNLP 2022 — ≥15 F1 drop.
- Guo, Schlichtkrull, Vlachos, "A Survey on Automated Fact-Checking," *TACL* 10:178, 2022.
- Choi et al., "Decontextualization: Making Sentences Stand-Alone," *TACL* 9, 2021.
- Sharma et al., "Towards Understanding Sycophancy in Language Models," arXiv:2310.13548, 2023.

## Revision History

| Rev | Date | Change | Driver |
|---|---|---|---|
| 1 | 2026-07-20 10:00 PDT | Initial S0-style existing-art study for expanding the corpus to white papers and tech reports: six capability tables (source mutability/provenance/laundering; structured appraisal without a scalar; gray-lit & sponsorship bias; formal treatment of conflict; truth-discovery as the named wrong turn; automated-verification limits), each web-verified against primary sources (all six bodies confirmed, incl. §6 truth-discovery from primary PDFs — the survey's three named assumptions and the copy-detection "shared-false-value" principle); a six-point graph-representation synthesis (verification-as-scoped-claim, multi-domain appraisal, stake-as-edges, first-class dispute node with scope keyed into object identity, warrant-collapse propagation, failed-verification-as-information); study-gate verdict that adds only two new mechanics (content-drift detection, stake-as-edges) and refuses a credibility scorer / truth engine / argumentation solver with citations; bounded conflicting-gray-lit spike. Residual flags in the verification ledger (RoB 2 no-score verbatim; GRADE κ; TKDE/PVLDB page strings). | user request: proper S0-style study of gray-literature expansion, conflicting claims, and verification |
