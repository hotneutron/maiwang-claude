---
artifact_type: proposal
authority: derived
generated_by: cross-team-repo-proposal
convergence: n/a
parent_artifacts:
  - AGENTS.md
  - .gitmodules
  - cross-team/.gitignore
  - cross-team/partners.json
  - cross-team/tiers.json
  - cross-team/policy.json
  - cross-team/parallax/README.md
  - cross-team/warrant/reference/README.md
tags: [cross-team, tooling, submodules, config, agent-guide, portability]
---

# Proposal - Cross-team Tool Bundle Repo with Defaults and Agent Guide

*Status: proposal, not implementation. Timestamp from `date`: 2026-07-16 11:26 PDT.*

## 0. Source Artifacts and Authority

- `AGENTS.md` is the local authority for workflow: partner reads must go through Parallax,
  shared repos use public GitHub remotes, dirty trees are local state rather than committed
  truth, and pushes require explicit user signal.
- `.gitmodules`, `cross-team/*.json`, and `cross-team/.gitignore` are observed local state.
  They show the current adoption friction but are not themselves a portable design.
- `cross-team/parallax/README.md` and `cross-team/warrant/reference/README.md` define the
  current tool contracts: Parallax uses a sync home with `partners.json`/`tiers.json`; Warrant
  uses a consumer `policy.json`.
- Current workspace note: an interrupted implementation left `cross-team/parallax` pointing at
  local commit `7db3394` that removes its nested `artifact_types` submodule. Treat that as
  local implementation state until it is intentionally adopted, pushed, or replaced.

## 1. Problem

The cross-team tools are useful, but adoption is too expensive and too easy to get subtly
wrong:

1. A consumer repo currently has to wire **three submodules** directly:
   `artifact_types`, `parallax`, and `warrant`.
2. The consumer must hand-author three config files:
   `partners.json`, `tiers.json`, and `policy.json`.
3. Those config files mix two things that should be separate:
   shared defaults and local consumer state.
4. The same registry is nested under `parallax/artifact_types` and `warrant/artifact_types`,
   even though the registry should be a sibling dependency owned once by the tool bundle.
5. Warrant path resolution is brittle for consumers: docs can be discovered through a relative
   `docs_dir`, but `parent_artifacts` are checked against the Warrant engine repo root, which
   causes false missing-parent errors for repo-relative parents.
6. Agent operating rules are spread across the consuming repo, Parallax docs, Warrant docs, and
   local memory. A new project should not need to rediscover those rules.

The real issue is not the existence of JSON config. It is that every consumer has to invent
the same JSON shape and path conventions from scratch.

## 2. Proposal

Create a new standalone public repo:

```text
hotneutron/cross-team
```

This repo is a **tool bundle and adoption boundary**. A consumer project adds one submodule:

```bash
git submodule add https://github.com/hotneutron/cross-team cross-team
git -C cross-team submodule update --init --recursive
```

The `cross-team` repo owns the shared defaults, agent guide, and the three tool submodules:

```text
cross-team/
  AGENTS.md
  README.md
  .gitignore
  partners.default.json
  tiers.default.json
  policy.default.json
  artifact_types/        # submodule: hotneutron/artifact_types
  parallax/              # submodule: hotneutron/parallax
  warrant/               # submodule: hotneutron/warrant
```

Consumers keep only local, ignored concrete config:

```text
cross-team/
  partners.json          # ignored, copied from partners.default.json and edited locally
  tiers.json             # ignored, copied from tiers.default.json and edited locally
  policy.json            # ignored, copied from policy.default.json and edited locally
  sync_ledger.json       # ignored/local state
  _inbox*.json           # ignored/local state
  _detect*.json          # ignored/local state
```

This gives every project the same starting point while keeping consumer identity, partner
paths, pins, and local document roots out of the reusable bundle.

## 3. The Three Default JSON Files

### 3.1 `partners.default.json`

Purpose: portable Parallax sync-home template.

Requirements:

- Contains `_doc`, `version`, and an empty `partners` object.
- Includes an example under a non-runtime key such as `_example_partner`.
- Does **not** carry any real `last_pinned` or `last_sync` from a consumer.
- Uses paths relative to `cross-team/partners.json` when copied.

Sketch:

```json
{
  "_doc": "Copy to partners.json and edit locally. partners.json is ignored.",
  "version": "1.0",
  "partners": {},
  "_example_partner": {
    "gpt": {
      "path": "../sibling-repo",
      "team_name": "example-team",
      "protocol_version": "2.2",
      "last_pinned": null,
      "last_sync": null
    }
  }
}
```

### 3.2 `tiers.default.json`

Purpose: registry-aligned Parallax tier defaults.

Requirements:

- Mirrors `artifact_types/artifact_types.json` for `default_tier`.
- Includes `doc_dirs: ["docs/", ".plan/"]` because local planning artifacts are part of the
  exchange workflow in this project.
- Includes triggers for `AGENTS.md`, `.plan/`, `docs/`, shared schemas, and protocol files.
- Leaves `self_name` as an obvious placeholder that the consumer must edit.

This file should be useful as-is after changing only `self_name`.

### 3.3 `policy.default.json`

Purpose: registry-aligned Warrant authority defaults.

Requirements:

- Mirrors `artifact_types/artifact_types.json` for `default_authority`.
- Points registry validation at the sibling registry in the bundle:
  `artifact_types/artifact_types.json`.
- Does not bake in this repo's `.plan/` or `paper-library/` paths.
- Supports consumer-local document roots after copy.

The current Warrant engine makes this hard because `parent_artifacts` are resolved against the
engine repo root. The bundle should therefore require one of these before claiming portability:

1. Preferred: Warrant supports `config.consumer_root`, and both `docs_dir` and
   `parent_artifacts` are resolved relative to that root.
2. Acceptable: `cross-team` provides a small wrapper that materializes an absolute temporary
   policy before invoking Warrant.

Without one of those, the same false missing-parent problem will recur in every consumer.

## 4. Remove Nested `artifact_types` from Parallax and Warrant

`artifact_types` should be owned once by the bundle, not nested inside each tool repo.

Target state:

```text
cross-team/artifact_types/              # one registry checkout
cross-team/parallax/                    # no parallax/artifact_types
cross-team/warrant/                     # no warrant/artifact_types
```

Required upstream changes:

- In `parallax`, remove `.gitmodules` entry and gitlink for `artifact_types`.
- In `warrant`, remove `.gitmodules` entry and gitlink for `artifact_types`.
- Update docs to say the registry is a sibling supplied by `hotneutron/cross-team`, not a
  nested submodule.
- Add or update conformance where behavior changes. Removing an unused nested submodule is
  packaging behavior, but Warrant's `consumer_root` fix is runtime behavior and needs a test.

Until those commits are pushed to the public remotes, the bundle must not pin local-only
submodule commits.

## 5. Cross-team `AGENTS.md`

The new repo needs its own agent guide because it is the adoption boundary. The guide should
be short and operational.

Minimum content:

```text
# Cross-team Agent Guide

## Authority
- This repo is the tool bundle for cross-team methodology.
- Tool source lives in submodules; defaults and adoption docs live here.
- Consumer-local config is ignored and is not shared truth.

## Setup
- Copy partners.default.json -> partners.json.
- Copy tiers.default.json -> tiers.json.
- Copy policy.default.json -> policy.json.
- Edit only consumer identity, partner paths, document roots, and pins.

## Parallax
- Use PARALLAX_HOME=<consumer>/cross-team.
- Run detect before any partner sync.
- Read partner artifacts only via parallax.py read.
- Relay only committed-clean local artifacts.
- Advance the ledger only for a real sync.

## Warrant
- Run Warrant through the cross-team policy or wrapper.
- Treat parent path errors as blocking unless they are confirmed resolver bugs.

## Submodules
- Do not edit parallax, warrant, or artifact_types from a consumer task.
- Upstream tool changes require a focused commit in the tool repo, conformance where behavior
  changes, then a bundle submodule bump.

## Commit Rules
- Do not commit local partners.json, tiers.json, policy.json, ledgers, inboxes, or detect logs.
- Push only on explicit user signal.
```

## 6. `.gitignore`

The bundle `.gitignore` should separate reusable defaults from local state.

Recommended entries:

```gitignore
# Consumer-local config copied from *.default.json
partners.json
tiers.json
policy.json
*.local.json

# Parallax runtime state
sync_ledger.json
embargo_registry.json
_quarantine/
_sync_read_log.json
_sync_detect.json
_sync_entry_draft.json
_sync_entry_draft_*.json
_sync_reaction_draft.md
_detect.json
_detect_*.json
_inbox.json
_inbox_*.json
_parallax_read_log.json
_relay.json
.sync_mode
.parallax_sync_mode

# Local environment
.env
.DS_Store
__pycache__/
*.pyc
```

If a team wants to publish a reusable config example, it should live under `examples/`, not as
the live `partners.json`/`tiers.json`/`policy.json`.

## 7. Adoption Flow for a New Consumer

A fresh consumer project should need this sequence:

```bash
git submodule add https://github.com/hotneutron/cross-team cross-team
git -C cross-team submodule update --init --recursive

cp cross-team/partners.default.json cross-team/partners.json
cp cross-team/tiers.default.json cross-team/tiers.json
cp cross-team/policy.default.json cross-team/policy.json

$EDITOR cross-team/partners.json
$EDITOR cross-team/tiers.json
$EDITOR cross-team/policy.json
```

Then:

```bash
PARALLAX_HOME=cross-team python3 cross-team/parallax/parallax.py detect <partner>
python3 cross-team/warrant/reference/_check_frontmatter.py --policy cross-team/policy.json
```

Later, if repeated adoption proves painful, add a tiny bootstrap script. That script is
convenience tooling, not the core design, and should come with a smoke test.

## 8. Migration Plan for This Repo

1. Stop treating the interrupted local `parallax` commit as accepted design. Either upstream it
   intentionally or replace it with the eventual public commit.
2. Create `hotneutron/cross-team` as a new public repo.
3. Add the three submodules inside it:
   `artifact_types`, `parallax`, `warrant`.
4. Add `partners.default.json`, `tiers.default.json`, `policy.default.json`, `.gitignore`,
   `README.md`, and `AGENTS.md`.
5. Remove nested `artifact_types` from `parallax` and `warrant` through their own upstream
   commits, then bump the bundle submodule pins.
6. In this consumer repo, replace the three direct root submodules with one direct submodule:
   `cross-team`.
7. Copy current consumer-specific config into ignored local files:
   `cross-team/partners.json`, `cross-team/tiers.json`, `cross-team/policy.json`.
8. Run the smoke tests in section 9.
9. Commit the consumer repo only after the bundle repo and tool submodule pins are
   committed-clean.

## 9. Acceptance Tests

A bundle release is acceptable only if these pass from a fresh consumer clone:

1. `git submodule status --recursive` shows exactly three first-level bundle submodules:
   `artifact_types`, `parallax`, `warrant`.
2. No nested `parallax/artifact_types` or `warrant/artifact_types` appears.
3. `PARALLAX_HOME=cross-team python3 cross-team/parallax/parallax.py detect <partner>` reads
   `cross-team/partners.json` and `cross-team/tiers.json`.
4. `python3 cross-team/warrant/reference/_check_frontmatter.py --policy cross-team/policy.json`
   validates a known-good doc whose `parent_artifacts` use normal consumer repo-relative
   paths.
5. After setup and one detect, `git -C cross-team status --short` shows no tracked dirt from
   local config or runtime state.
6. A second consumer can adopt the bundle by editing only the three ignored local JSON files,
   with no changes to committed defaults.

## 10. Non-goals

- Do not turn `cross-team` into a monorepo for tool source. Tool source stays in submodules.
- Do not copy Parallax or Warrant implementation history into the bundle.
- Do not make consumer-specific partner ledgers portable. Pins and sync ledgers are local
  state.
- Do not push local submodule commits until explicitly requested.
- Do not promote project-specific paper-library schema decisions into this bundle.

## 11. Open Decisions

1. **Default file names:** use `*.default.json` plus ignored live copies, or commit live
   `partners.json`/`tiers.json`/`policy.json` with placeholders? Recommendation:
   `*.default.json` plus ignored live copies.
2. **Warrant root semantics:** add `consumer_root` to Warrant, or provide a wrapper that
   generates an absolute policy? Recommendation: add `consumer_root` with conformance.
3. **Bootstrap script:** no script initially, just documented `cp`. Add a script only after
   a second consumer adopts the bundle and repeats the same setup pain.
4. **Examples:** include `examples/maiwang-claude/`? Recommendation: yes, but keep it clearly
   non-runtime and scrub local pins unless the example is meant to be replayable.

## 12. Recommendation

Proceed with the new `hotneutron/cross-team` repo, but do it as a packaging/adoption layer:
one bundle submodule for consumers, one sibling `artifact_types` checkout inside the bundle,
and ignored local config copied from committed defaults. The key portability fix is not merely
moving JSON files; it is making the boundary explicit:

- committed defaults are shared;
- live config and ledgers are consumer-local;
- tool source remains in upstream submodules;
- `AGENTS.md` in the bundle tells agents exactly how to operate the tooling.

Do not claim the bundle is easy to adopt until Warrant validates repo-relative parent artifacts
from a fresh consumer without false missing-parent errors.
