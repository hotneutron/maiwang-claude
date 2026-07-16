# paper-library — local paper-map / brain-map spike

**Status: local spike (S1 complete).** This is a *consumer* of the shared `cross-team/`
substrate (the `artifact_types` evidence vocabulary), **not** an amendment to it. Per the
converged cross-team spike proposal ([proposal](../.plan/260715-2301-proposal-paper-map-spike-consensus.md))
and gpt's ack, the first schema stays **local** (constraint C8) until a corpus spike proves the
shape with ≥2 consumers under divergent machinery (promotion bar D5).

## What this is

Two views over one graph (constraint C2):
- **paper map** — the corpus organized by topic + reading order (nodes).
- **brain map** — the claim graph: claims, evidence, typed relations (edges).

A survey is a *render target*, not the storage format (C1). The durable object is the graph;
surveys / maps / reading queues are regenerable projections.

## Layout

| Path | What |
|---|---|
| `schemas/paper.schema.json` | Source Layer: canonical paper identity, external ids, stable passage ids. |
| `schemas/edges.schema.json` | Semantic Layer: claims (multi-evidence), typed edges (lifecycle+provenance), reversible merges. |
| `schemas/study.frontmatter.schema.json` | Personal Layer: the per-paper `study` doc frontmatter (also the reading queue). |
| `validate.py` | Zero-dependency (stdlib) draft-07-subset validator + `--selftest` (+ optional jsonschema cross-check). |
| `fixtures/` | Valid + malformed instances per schema (the S1 DoD proof). |
| `papers/` | Source-Layer paper records (S2 import): one JSON per paper, with passages. |
| `studies/` | Personal-Layer `study` docs (S2): one per paper; claims cite passage ids. |
| `corpus_check.py` | Consistency gate: every study claim traces to a real source passage (the S2 DoD, repeatable). |
| `graph/proposals.json` | S3 LLM-proposed layer: extraction + inference claims, typed edges, merges. |
| `graph/graph.json` | S4 COMPILED graph state (built, validated, idempotent). Do not hand-edit except `owner: human`. |
| `build_graph.py` | S4 builder: compiles proposals → graph, applies reversible merges, preserves human edits, idempotent. |
| `test_idempotency.py` | S4 DoD: rebuild is byte-identical AND manual edits survive. |
| `render.py` | S5 renderers: `paper-map`, `brain-map <claim>`, `survey <claim>`, `all` — each stamped with the graph SHA. |
| `render/` | S5 projections (regenerable): `paper_map.md`, `brain_map.md`, `survey.md`. |
| `trace_check.py` | Overall DoD gate: survey + graph view both trace to the same committed graph SHA. |
| `260716-0039-findings-spike-decision-log.md` | S6 decision log + D4 storage-friction findings. |

## The five gaps this closes (from S0)

The S0 existing-art study ([study](../.plan/260716-0005-study-existing-art-paper-map-tools.md))
found five things missing from the shared `claims_index`, all now carried locally:

1. **Multiple evidence refs per claim** — `claims[].evidence[]`.
2. **Manual-correction ownership** — `claims[].owner` (`human` never overwritten by regen).
3. **Edge lifecycle** — `edges[].lifecycle` = `proposed|confirmed|rejected|superseded`.
4. **Reversible merge records** — `merges[]` (a merge is a link, not a destructive rewrite).
5. **Projection provenance** — `model_version` on generated atoms; projections trace to a
   committed graph snapshot (S5, upcoming).

## Run

```
python3 validate.py --selftest                              # S1 DoD: accept valid, reject malformed
python3 validate.py schemas/paper.schema.json fixtures/paper.valid.json
```

The validator is pure-stdlib and authoritative for the DoD. If the optional `jsonschema`
library is importable, `--selftest` additionally **cross-checks** each fixture against the
canonical implementation and asserts it agrees (`[xcheck ✓]`), guarding against draft-07
subset-semantics drift; it degrades gracefully when the library is absent. To enable it:

```
python3.12 -m venv .venv && .venv/bin/pip install jsonschema
.venv/bin/python validate.py --selftest                    # runs with cross-check active
```

## Spike roadmap (converged S0–S6)

- **S0** — bounded existing-art study. ✅ done.
- **S1** — local schemas + validator + fixtures. ✅ this directory.
- **S2** — import 3 papers into `study` docs with stable passage ids. ✅ done (`papers/`, `studies/`, `corpus_check.py`).
- **S3** — extract a small claim + relation set (LLM-proposed, gated). ✅ `graph/proposals.json` (12 claims, 9 edges).
- **S4** — idempotency: re-extraction adds no dupes, preserves manual edits. ✅ `build_graph.py` + `test_idempotency.py`.
- **S5** — render two views (paper map + one claim-neighborhood brain map) from one committed
  graph state. ✅ `render.py` + `render/`.
- **S6** — decision log: where each identity/merge decision was auto / LLM / manual; and any
  git-native query awkward enough to stress storage (records D4 as a measured constraint). ✅ `260716-0039-findings-spike-decision-log.md`.

**Overall DoD:** one regenerated survey section AND one graph view, each traceable back to the
same committed graph state. ✅ enforced by `trace_check.py`.

## Run the full spike gate suite

```
python3 validate.py --selftest        # S1
python3 corpus_check.py               # S2
python3 build_graph.py                # S4 (idempotent build)
python3 test_idempotency.py           # S4 DoD
python3 render.py all                 # S5 projections
python3 trace_check.py                # overall DoD
```

## Governance

Machinery here diverges by design (the cross-team independence that makes a future cross-check
meaningful). The only candidate shared interface is the semantic-layer schema
(`edges.schema.json` node/edge/provenance shape), and only after this spike + gpt's spike prove
it — promoted via proposal → independent review → bilateral agreement → version bump, never by
editing `cross-team/` first.
