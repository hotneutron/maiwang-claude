---
artifact_type: brainstorm
authority: speculative
generated_by: llm-brainstorm-web-probe
convergence: n/a
parent_artifacts:
  - AGENTS.md
  - .plan/260715-2146-brainstorm-paper-map-brain-map.md
  - .plan/260715-2301-proposal-paper-map-spike-consensus.md
  - .plan/260716-0005-study-existing-art-paper-map-tools.md
  - .plan/260716-0128-brainstorm-brainmap-query-layer.md
  - paper-library/schemas/edges.schema.json
  - paper-library/graph/graph.json
  - paper-library/trace_check.py
tags: [graphrag, llm-wiki, no-chunking, markdown, continual-learning, brain-map, read-layer]
---

# Brainstorm — GraphRAG-as-store, the Wiki approach, and Continual-Learning migration

*Status: speculative brainstorm. Answers three design questions about building the smart library.
Grounded in the local `.plan/` design history (C1–C8 consensus, S0 study, S7 read-layer
brainstorm) and the built spike under `paper-library/` (schemas, `graph/graph.json`,
`trace_check.py`), plus a web probe of the LLM-Wiki pattern and current continual-learning work.
Not a plan or a decision. Timestamp from `date`: 2026-07-17 18:27 PDT.*

*Convergence: `n/a` — a speculative synthesis over the local spike and external prior art, no
corroboration claim. The overlap between our prior `.plan/` design and the external wiki-critique
corpus is a shared GraphRAG / "LLM proposes, code disposes" prior, not independent measurement.*

---

## 0. TL;DR

- **Q1 (GraphRAG + claim/abstraction edges, no chunking, rewrite-in-markdown): viable — it is
  ~90% the architecture already in `.plan/`.** The one load-bearing correction: *markdown must be
  the Projection/Personal layer rendered from a structured graph, not the semantic store.*
  Collapsing that distinction is the LLM-Wiki move and it discards the exact thing that makes the
  library "smart" — the typed, verifiable edge.
- **Q2 (wiki approach): right about the symptom (RAG is stateless) and the interface (markdown,
  local, navigable); wrong as a system of record.** The web evidence converges on a hybrid:
  structured graph as truth, wiki as a rendered projection — which is our C1 + C3 verbatim. Our
  system is best positioned as *the LLM-Wiki with its four gaps closed.*
- **Q3 (CL migration): the typed-edge graph migrates far more cleanly and safely than the wiki**,
  because the graph already carries the metadata a continual-learner needs to decide what to
  preserve vs. overwrite vs. unlearn. The best "CL" for a research library is likely
  *external continual memory* (keep the graph, keep weights frozen), escalating to
  LoRA-per-region distillation only when latency/offline use forces it.

---

## 1. Q1 — GraphRAG + claim/abstraction edges, no chunking, "rewrite in markdown"

**Verdict: viable, and it is the design we already spec'd — with one correction about what
"markdown" is allowed to be.**

Decomposing the four moves in the ask:

### 1.1 "Leveraging GraphRAG" — already settled
S7 §10 and the S0 GraphRAG addendum already ratified the stance:
**GraphRAG-for-structure, our-code-for-disposal.** Adopt its two proven ideas — community
summaries and local/global dual retrieval — and keep the hardening layer. Nothing to reopen.

### 1.2 "Added edges for claims and abstractions" — this IS the differentiator
- *Claim edges* = the typed vocabulary already in `edges.schema.json`
  (`supports | contradicts | extends | shares_assumption_with | …`) carrying `evidence_tier` +
  `lifecycle`. This is the one thing stock GraphRAG cannot express — its edges are free-text LLM
  descriptions. The S7 §2 query "every contradiction resting on measured evidence" is only
  expressible because the edges are typed.
- *Abstraction edges* = the S7 §9 super-nodes / community summaries as **materialized views with
  region-scoped staleness** (`region_hash` invalidation). That is the "abstraction" layer, already
  sketched.

### 1.3 "I don't want to use chunking" — correct, with two honest caveats
The spike already replaced chunks with **stable passages + claims** (`paper.schema.json` passages
`p1..pN`; claims cite them). Strictly better for typed relations and provenance — chunk-RAG "can
only surface text that sounds similar" (S7 §2). Two things to keep straight:

1. **No chunking ≠ no retrieval.** A seed-finder is still needed to *enter* the graph (embedding
   on claim statements, or BM25). S7 §5 already flags "add the embedding index only when corpus
   scale demands it." Do not let "no chunks" silently become "no retrieval index."
2. **GraphRAG chunks on ingest to extract entities/relations.** Dropping chunking as *storage* is
   right; the *extraction* step still needs to digest long full-text papers
   (section/passage-level extraction — chunks-as-transient-input, not chunks-as-storage). Decide
   this explicitly via the S2 `import_method` field when moving past abstract-first import.

### 1.4 "Just rewrite in markdowns" — the crux and the correction
Our own **C1** already ratified *"survey is a render target, not storage; the durable object is a
graph."* "Rewrite everything into markdown as the store" is the **Karpathy LLM-Wiki move**, and it
contradicts C1. Concretely, for *this* system:

- The "smart" lives in the **edges**. In the graph they are typed, lifecycle-tracked,
  evidence-linked, code-validated. Rewritten into prose + `[[wikilinks]]` they degrade to untyped
  "related" links — the exact Obsidian anti-pattern S0 flagged ("the graph view is decorative, not
  operational"). That is rebuilding the *worse* version the study-gate told us not to build.
- Markdown has no referential integrity (rename → silent 404), no schema (`ML` vs
  `Machine Learning` split), no lifecycle (a superseded claim keeps equal authority), no queryable
  relation layer. `warrant` + `trace_check.py` give all of that over the graph for free — and give
  up nothing when markdown is rendered *from* it.
- The verify gate (S7 §4 — "every cited id exists in `graph.json`; no invented edges") has nothing
  to check against if the store is prose. That gate is the whole reason an answer is *trustworthy*
  rather than *plausible*.

**Resolution (the layer table we already hold, applied to this phrasing):**

| Role | Store as | Owner | Source of truth? |
|---|---|---|---|
| Source (papers, passages) | JSON, append-only | machine | yes (immutable) |
| **Semantic (claims, typed + abstraction edges)** | **structured graph** (`graph.json` / small store) | machine, compiled | **yes — the durable object** |
| Personal (your synthesis, notes) | **markdown** (`study` docs) | **human, never overwritten** | yes for the human layer |
| Projection (wiki pages, surveys, super-node summaries) | **markdown**, rendered, SHA-stamped | machine | **no — disposable** |

You *do* get the markdown wiki — as the Projection + Personal layers. What must not happen is
LLM-rewritten markdown becoming the semantic store. Build the GraphRAG shape with typed claim +
abstraction edges and no chunk-storage, and render markdown liberally on top; keep the graph as
truth. That is not a compromise on the idea — it is the hardened form, and most of it already runs
in `paper-library/`.

---

## 2. Q2 — For and against the wiki approach (web probe)

Probed **Karpathy's LLM Wiki** (LLM maintains a folder of markdown; ~5k stars, April 2026),
**OpenDeepWiki** (AIDotNet, MIT — incremental update, MCP, multi-DB backends) and
**DeepWiki-Open** (AsyncFuncAI — clone → embed → LLM writes docs → RAG Q&A), plus a large critique
corpus.

### 2.1 For
1. **Fixes a real defect: statelessness.** Plain RAG rediscovers knowledge every query; the wiki
   *compounds* — multi-doc synthesis pre-compiled into pages, contradictions flagged at compile
   time, cross-refs pre-drawn. Karpathy ran his to ~100 articles / 400k words and still found it
   faster and more accurate than RAG for research.
2. **Local-first, git-native, portable, transparent** — plain markdown, diffable, no infra.
   Matches our D4 preference.
3. **Answers questions that live *between* pages** (the graph-of-links effect) — real, and exactly
   what a *typed* edge graph does better.
4. **It productizes.** OpenDeepWiki / DeepWiki-Open show the pattern working at codebase scale with
   incremental update + agent access + Q&A.
5. **Low activation energy** — the markdown *is* the UI (Obsidian graph view, backlinks). Good for
   a solo researcher starting today.

### 2.2 Against
1. **No knowledge lifecycle / no invalidation.** The sharpest critique (the "four structural gaps"
   response): pages are created and updated but never invalidated, stress-tested, or retired —
   "hallucinations become permanently embedded as facts." A living system needs
   `emergence → validation → crystallization → dormancy → invalidation`. Our edge `lifecycle` +
   region-hash staleness + reversible merges are precisely the missing machinery.
2. **Markdown is not a database.** No foreign keys (links break silently on rename), no schema
   (duplicate concepts multiply), no real query language (every question is a probabilistic LLM
   guess), no field-level audit trail.
3. **It doesn't escape RAG.** The hand-maintained index "works at 100 files, dies at 1,000"; then
   BM25 + vector search + re-ranking gets bolted on = "RAG with extra steps." Tellingly, the
   *scaled* open implementations reintroduce databases + embeddings, conceding the pure-markdown
   claim fails at scale.
4. **Truth maintenance is where LLMs fail *quietly*** — bad synthesis, stale claims surviving new
   evidence, false consistency. Practitioners report the manual cross-checking "basically cancels
   out the time-saving benefit." "The LLM owns this layer entirely" is fine for low-stakes personal
   use, too aggressive for accuracy-critical work.
5. **Provenance is only page-level.** The tutorial itself grades source traceability "Moderate." A
   research library needs passage-level "trace every statement to source" — our
   `evidence[].passage_id` enforces it; a pure wiki does not.
6. **It can outsource the understanding you are trying to build.** If the LLM writes all the
   synthesis you get an information store, not understanding — "you can report what the model
   produced, you can't argue from something you built yourself." This bites the stated goal: we
   want a **brain map**, not just a paper map. A fully-LLM-written wiki is a paper map in a
   brain-map costume — which is why the Personal layer (`owner: human`, never overwritten) is
   load-bearing.

### 2.3 Synthesis
The balanced reading — reached independently by several reviewers and already embodied in our
`.plan/` — is that the wiki is **right about the symptom and the interface, wrong to make
LLM-maintained markdown the system of record.** The fix is a hybrid: structured, provenance-checked
graph as truth; wiki as rendered projection (C1 + C3). So the honest framing is not "wiki vs. our
system" — **our system is the hardened wiki**, with the four gaps closed: lifecycle, negentropy
(staleness / merge / contradiction detection), grounding (passage provenance + verify gate).

---

## 3. Q3 — Which approach migrates to a continual-learning system more easily

*Calibration (memory/web-derived, fast-moving): the "CL is on the verge of practical" premise is
directionally supported — Google's Nested Learning / "Hope" (Continuum Memory System,
multi-frequency updates), ReCoLoRA (recursive LoRA consolidation), and MSSR (memory-aware replay)
all target catastrophic forgetting. Readiness for a personal library today is the aspirational
part; treat the trend as real and the readiness as not-yet-verified.*

**Verdict: the typed-edge graph migrates far more easily and safely than the rewrite-in-markdown
wiki. And the best CL move for a research library is likely to keep the graph as *external*
continual memory rather than pushing knowledge into weights until there is a hard reason to.**

### 3.1 Why the graph migrates cleanly
CL's real difficulty is not learning new things — it is **knowing what to overwrite vs. preserve**
and **unlearning** what is now wrong, without catastrophic forgetting. The graph already carries
exactly that metadata:

- `evidence_tier` + `confidence` → a ready-made **importance signal** for replay (replay methods
  must *estimate* sample importance; we store it) and for EWC-style protection (guard
  `measured`+`confirmed`; let `conjectural`+`proposed` be cheaply overwritten).
- `lifecycle` (proposed/confirmed/rejected/superseded) + `supersedes` edges + retired claims → an
  **invalidation / unlearning signal**. This is CL's hardest half, and the wiki has none of it.
- `owner: human` + reversible merges → **protected anchors** (never overwrite) and reversible
  consolidation.
- passage-level provenance + the verify gate → fine-tune on **validated, deduplicated,
  contradiction-resolved atoms**, not raw prose. An error caught at the gate never reaches the
  weights — and a fact in weights is far harder to reverse than a line in a file.

Structural match: Nested Learning's trick is **multi-frequency updates** so "knowledge does not
change everywhere at once." Our layers *are* that partition on the data side — Source (never) /
confirmed claims (slow) / proposed + projections + super-nodes (fast); region-scoped hashing =
targeted/sparse update. We have pre-organized knowledge along the exact axis (stability ×
update-rate) a Continuum-Memory model consumes.

**The wiki is harder**: to feed CL you must first re-extract structure from prose (re-embed,
re-derive relations) — i.e. rebuild the graph anyway, later and lossily — and its lack of lifecycle
means you cannot tell the CL system what is stable vs. tentative. "Hallucinations become permanent
facts" becomes "hallucinations become permanent **weights**."

### 3.2 CL-migration paths (ranked)
1. **Keep the graph as external continual memory — don't touch weights (recommended default).**
   Model frozen (or slowly updated); the graph is the continually-updated memory read through the
   verify-gated `ask.py` loop. Zero catastrophic forgetting (nothing overwritten in weights; the
   lifecycle handles invalidation). This is the S7 read layer we already designed — the library
   *is* the continual memory.
2. **Adapter/LoRA consolidation, one adapter per region (when weights are needed).** Distill only
   `confirmed` + `measured` subgraphs into a LoRA per domain/cluster; super-node regions become
   adapter boundaries. ReCoLoRA's recursive consolidation maps directly. Reversible: drop an
   adapter to unlearn a domain.
3. **Graph-seeded replay (MSSR-style).** When weights are touched, use the graph as a principled
   replay buffer: priority = `confidence × evidence_tier × recency`.
4. **Multi-frequency consolidation mapped to our layers (Nested-Learning-style).** Formalize update
   cadence per layer (Source never / confirmed slow / proposed+projections fast).
5. **Test-time / activated memory (weakest learning, strongest safety).** Load the verified
   subgraph as persistent context (KV-cache / memory tokens) — continual behavior, no forgetting
   risk. Fallback if weight-updating proves unstable.

**Recommendation:** stay memory-based (1) as the CL substrate; add LoRA-per-region distillation (2)
only when latency/offline forces it, and only from confirmed+measured claims; use the graph as the
replay/importance oracle (3) whenever weights are touched. Non-negotiable across all paths:
**keep the lifecycle + verify gate as the unlearning mechanism** — CL's hard half is safely
forgetting wrong things, and the graph is the only one of the two options that can *tell* the CL
system what to forget.

---

## 4. Consolidated recommendation

Build the GraphRAG-shaped, typed-edge, no-chunk-storage design already in `.plan/` and running in
`paper-library/`. Render markdown liberally as Projection + Personal layers, but keep the
structured graph as the source of truth and the verify gate as the trust boundary. Treat the wiki
not as a competitor but as the un-hardened ancestor of this system. For continual learning, keep
the graph as external memory first; escalate to region-scoped LoRA distillation only under a
measured latency/offline pressure, and let the graph's `evidence_tier` / `lifecycle` metadata drive
what a continual learner preserves, replays, and unlearns.

This brainstorm stays **local machinery (C8)**: nothing here amends the shared `claims_index` or
Parallax. It is a speculative design synthesis over the local spike and external prior art, not a
shared-schema change.

## Sources (external prior art, cited inline; not repo parent_artifacts)

- Karpathy LLM Wiki tutorial — datasciencedojo.com/blog/llm-wiki-tutorial/
- "Your LLM Wiki Will Collapse — four structural gaps" — gist.sharingeye.com/V-interactions/a0d2a62c1b16d1fecf1bd81e8f611fba
- "The Great LLM-Wiki Delusion" / Hyperscope-vs-LLM-Wiki — gnu.support
- DeepWiki (Cognition/Devin); AIDotNet/OpenDeepWiki; DeepWiki-Open (AsyncFuncAI)
- Google Nested Learning / Hope; ReCoLoRA; MSSR; JHU "sparse memory updates for continual learning"

## Revision History

| Rev | Date | Change | Driver |
|---|---|---|---|
| 1 | 2026-07-17 18:27 PDT | Initial brainstorm synthesizing Q1 (GraphRAG-as-store), Q2 (wiki for/against, web-probed), Q3 (CL migration) against the local `.plan/` design and the `paper-library/` spike. | user request: persist the brainstorm |
