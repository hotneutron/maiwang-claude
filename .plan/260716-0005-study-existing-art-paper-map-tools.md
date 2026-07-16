---
artifact_type: study
authority: derived
generated_by: s0-existing-art-review
parent_artifacts:
  - .plan/260715-2301-proposal-paper-map-spike-consensus.md
  - gpt:.plan/260715-2346-reaction-paper-map-spike-consensus.md
tags: [paper-map, brain-map, existing-art, study-gate, s0]
---

# S0 — Existing-Art Study: Paper-Map / Brain-Map Tools

*Bounded existing-art study satisfying the study-gate (AGENTS.md) before any paper-map
implementation. Scope fixed by the converged spike proposal + gpt's ack (read via Parallax at
gpt HEAD `43f6d95`): **one table per tool**, purpose = **block naive reinvention**, NOT
benchmark the literature-tool market. No UI feature inventory. Timestamp from `date`:
2026-07-16 00:05 PDT.*

*Authority: `derived` (systematic synthesis of external references for internal use). This is
not measurement; it is prior-art grounding.*

---

## Why this study exists (and why it's bounded)

Two independent lanes converged on the same architecture (survey-as-projection, one graph, LLM
proposes / code disposes, identity-is-hard). AGENTS.md's study-gate blocks implementing novel
tooling without citing existing art — the risk is *rebuilding a worse version of known tooling*.
gpt's counter constrained S0 to a short study: the goal is to know, per tool, **one primitive
worth reusing, one thing to avoid, and one failure mode it exposes for our spike** — nothing
more. Everything below is deliberately terse.

## The seven tools

Each row: the **primitive** the tool is built on · what to **reuse** · what to **avoid** ·
the **failure mode** it exposes for *our* spike (S1–S6).

### 1. Zotero — reference manager

| Facet | Finding |
|---|---|
| Primitive | Canonical item identity: dedup by DOI / ISBN / arXiv-id, with attachments + user notes hung off a stable item record. |
| Reuse | The **canonical-identity-first** discipline — resolve a paper to one record with tracked external ids *before* anything else. This is our S2 "one canonical identity per paper." |
| Avoid | Notes are free-text blobs, not linked to source passages; tags are a flat folksonomy. No claim/evidence structure. |
| Failure mode for our spike | Shows that *storage without a claim/passage layer* degenerates into unsearchable note soup — validates our C4 (evidence ≠ retrieval) and S3 (claims tied to passages). |

### 2. Obsidian-style note graphs — personal knowledge graph

| Facet | Finding |
|---|---|
| Primitive | Bidirectional `[[wikilinks]]` between markdown notes; the graph is *emergent* from links, files are the source of truth. |
| Reuse | **Git-native markdown files as the durable substrate**, links as edges — directly validates our git-native MVP (D4) and "personal notes durable" (C-personal-layer). |
| Avoid | Untyped links (a link means only "related"); no provenance, no confidence, no distinction between authored and generated edges. The graph view is decorative, not operational. |
| Failure mode for our spike | Proves gpt's UX point: an untyped node-link graph does not scale to operation. Forces our `edges.schema.json` to carry **typed relations + lifecycle + provenance**, not bare links. |

### 3. Connected Papers — similarity graph

| Facet | Finding |
|---|---|
| Primitive | A single-seed similarity graph from co-citation + bibliographic coupling (not citation edges directly); layout by similarity. |
| Reuse | Co-citation / coupling as a **candidate-neighbor retrieval** signal (cheap, no LLM) to seed relation discovery — feeds S3's candidate generation. |
| Avoid | One seed → one throwaway graph; nothing persists, nothing is typed, no notion of claim-level agreement/conflict. It answers "what's nearby," never "do these agree." |
| Failure mode for our spike | Confirms C4 concretely: **similarity ≠ relation type**. A similarity graph cannot express supports/contradicts. Our value-add must be the typed, evidence-backed edge it can't produce. |

### 4. ResearchRabbit — citation-network explorer

| Facet | Finding |
|---|---|
| Primitive | Citation-network traversal with collections; "similar / earlier / later work" expansion around a set of seed papers. |
| Reuse | **Citation structure as historical/explicit edge scaffolding** (depends_on / extends / reproduces candidates) — a deterministic edge source that doesn't need the LLM (complements S3). |
| Avoid | Discovery-only; collections are folders, not a semantic layer. No claims, no notes-as-first-class, no regenerable projections. |
| Failure mode for our spike | Shows citation edges are necessary but not sufficient: they give the *skeleton* but not the *claim-level* graph. Our spike must layer extracted claims on top of citation scaffolding, not stop at citations. |

### 5. Litmaps — living citation map

| Facet | Finding |
|---|---|
| Primitive | A persistent, auto-updating citation map with a time axis; "monitor" alerts when new citing work appears. |
| Reuse | The **living-map** idea: the map is a *projection that re-renders* as the corpus grows, not a hand-maintained artifact — validates C1 (survey/map as render target) and our "can't go stale" goal. |
| Avoid | Still citation-similarity underneath; the "map" is nodes+citation edges, no claim/evidence semantics, no personal-synthesis layer. |
| Failure mode for our spike | Confirms the projection must be **regenerable from committed graph state** (S5 DoD), and that "living" is worthless without a typed semantic layer to re-project *from*. |

### 6. Semantic Scholar graph — scholarly knowledge graph + API

| Facet | Finding |
|---|---|
| Primitive | Large-scale scholarly KG: papers/authors/venues + citation edges with **citation intent** (background / method / result) and TLDR summaries, exposed via API. |
| Reuse | **Citation *intent* classification** as a real typed-edge precedent (method vs result vs background maps onto our uses_method / evaluates_on / extends), and the **API as a metadata/passage source** for S2 import. |
| Avoid | Intent is coarse and paper-to-paper, not claim-to-claim; it's a global corpus, not personal synthesis; no manual-correction ownership. |
| Failure mode for our spike | Sets the bar: typed edges are achievable at scale, but our differentiator is **claim-level, evidence-linked, personally-owned** edges — anchor S3/S1 there, don't re-derive a global KG. |

### 7. Claim/evidence extraction systems — argument mining / SciFact-style

| Facet | Finding |
|---|---|
| Primitive | NLP pipelines that extract claims + supporting/refuting evidence spans and classify a claim–evidence stance (support / contradict / NEI). |
| Reuse | The **claim + evidence-span + stance** triple — this *is* our brain-map atom (claim, passage-level `evidence_ref`, supports/contradicts edge with evidence_tier). Directly shapes `claims_index` + `edges.schema.json`. |
| Avoid | These systems assume closed benchmarks and a fixed label set; identity/dedup of claims across papers is out of scope (they operate per-document). Confidence is often uncalibrated. |
| Failure mode for our spike | Names our hardest problem exactly (C6): extraction is solved-ish *per document*, but **cross-paper claim identity / dedup / merge is not** — that's where S3/S4 and the decision log (S6) must concentrate. |

## Synthesis — what to reuse, avoid, and where the spike must earn its keep

**Reuse (composable, mostly deterministic):**
- Canonical paper identity by external ids (Zotero) → S2.
- Git-native markdown+links as substrate (Obsidian) → D4/MVP.
- Co-citation/coupling + citation-network + citation-*intent* as **candidate-edge retrieval** (Connected Papers, ResearchRabbit, Semantic Scholar) → S3 candidate generation without burning LLM calls.
- Living-projection re-render (Litmaps) → S5.
- Claim + evidence-span + stance triple (argument mining) → the brain-map atom, S1/S3.

**Avoid (the recurring anti-patterns):**
- Untyped edges / "related" links with no provenance (Obsidian, Connected Papers).
- Throwaway single-seed graphs that persist nothing (Connected Papers).
- Free-text notes divorced from source passages (Zotero).
- Stopping at the citation skeleton and never reaching claim-level semantics (ResearchRabbit, Litmaps).
- Global-KG scale ambitions that skip personal ownership + manual correction (Semantic Scholar).

**Where our spike genuinely differs from all seven (the reinvention we are NOT doing):**
1. **Claim-level, evidence-linked, personally-owned typed edges** — no tool combines all three. Similarity/citation tools stop at paper-level; extraction tools stop at per-document; note graphs are untyped.
2. **Cross-paper claim identity / dedup / reversible merge** (C6) — unsolved everywhere; this is the design center of S3/S4/S6.
3. **Every projection traceable to a committed graph snapshot** (the S5 DoD) — none of the seven offer projection provenance.

## Study-gate verdict

**Cleared, bounded.** The three differentiators above are real gaps in the existing art, so the
spike is not naive reinvention. The study also *shrinks* the spike: identity resolution, citation
scaffolding, and claim/evidence extraction have reusable prior art — the spike's novel effort is
concentrated on **cross-paper claim identity/merge** and **projection provenance**, exactly the
two places C6 and the S5 DoD already pointed.

## Next (per the converged plan)

- Proceed to **S1** — local `paper.schema.json`, `study` frontmatter, `edges.schema.json`
  (relation vocab + lifecycle `proposed|confirmed|rejected|superseded` + reversible merge record
  + multiple evidence refs + projection provenance). Local only (C8).
- Record in S6 any git-native query that feels awkward (D4, gpt's reopen) so storage stays a
  measured constraint, not a taste argument.
- The next cross-team artifact should carry **spike measurement**, not prose.
