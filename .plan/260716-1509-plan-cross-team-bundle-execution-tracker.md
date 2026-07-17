---
artifact_type: plan
authority: derived
generated_by: cross-team-execution-tracker
convergence: propagated
parent_artifacts:
  - AGENTS.md
  - .plan/260716-1126-proposal-cross-team-bundle-agent-guide.md
  - cross-team/parallax/README.md
  - cross-team/warrant/reference/README.md
provenance_note: "Execution tracker for an already-reviewed OSS repo packaging proposal; conformance tests, not a separate prior-art study, are the gate."
tags: [cross-team, execution-tracker, tooling, bundle, conformance, migration]
---

# Plan - Cross-team Bundle Execution Tracker

*Status: execution tracker, migration completed. Initial timestamp from `date`: 2026-07-16 15:09 PDT.*

## 0. Source Artifacts and Authority

- `AGENTS.md` is the local authority for workflow: public GitHub remotes for shared repos,
  conformance for behavior changes, no broken pins, no push without explicit signal.
- `.plan/260716-1126-proposal-cross-team-bundle-agent-guide.md` is the source proposal. This
  tracker executes that proposal after GPT critique and local OQ decisions were folded in.
- `cross-team/parallax/README.md` and `cross-team/warrant/reference/README.md` define the
  current tool contracts being changed.

Convergence: `propagated` because the source proposal incorporated GPT feedback read through
Parallax; this tracker does not claim independent corroboration.

## 1. Fixed Decisions

These are not open during execution:

1. New public bundle repo: `hotneutron/cross-team`.
2. Local implementation/test workspace: `/Users/bytedance/wk/cross-team/`.
3. Bundle repo contains exactly three tool submodules:
   `artifact_types`, `parallax`, `warrant`.
4. Bundle ships one default config: `cross-team.default.json`.
5. Each consumer owns and commits one live config outside the submodule: `cross-team.json`.
6. No temporary split-config shim. Consumers do **not** switch until both upstream gates land:
   one-file config support and Warrant `consumer_root`.
7. `.plan/` may appear only in `cross-team.default.json`, never hardcoded in runtime code.
8. No `examples/`; `README.md` and `AGENTS.md` must be sufficient.
9. No formal prior-art/study doc for OSS repo packaging; tests/conformance are the gate.
10. Remove hardcoded consumer defaults and `ds4m`/`op`/`gpt`/`maiwang` residue from shipped
    defaults/docs unless a hit is deliberately inside a named conformance fixture.

## 2. Tracker

| ID | Work item | Status | Output | Gate |
|---|---|---|---|---|
| T0 | Create/prepare workspace `/Users/bytedance/wk/cross-team/` | completed | bundle repo exists and public remote is reachable | local workspace and GitHub remote available |
| T1 | Patch Warrant upstream: add `config.consumer_root` and repo-relative parent resolution | completed | Warrant submodule pinned at `e174732` through bundle `8dfd45a` | Warrant check passes from this consumer |
| T2 | Patch Parallax upstream: read unified `cross-team.json` via `CROSS_TEAM_CONFIG` | completed | Parallax submodule pinned at `c6eef7d` through bundle `8dfd45a` | Parallax detect reads root `cross-team.json` |
| T3 | Patch Warrant upstream: read unified `cross-team.json` via `CROSS_TEAM_CONFIG` | completed | Warrant submodule pinned at `e174732` through bundle `8dfd45a` | Warrant reads root `cross-team.json` |
| T4 | Remove nested `artifact_types` from `parallax` | completed | Parallax submodule pinned at `c6eef7d` | no `cross-team/parallax/artifact_types` submodule |
| T5 | Remove nested `artifact_types` from `warrant` | completed | Warrant submodule pinned at `e174732` | no `cross-team/warrant/artifact_types` submodule |
| T6 | Scrub hardcoded defaults and consumer text from `artifact_types`, `parallax`, `warrant` | completed | shipped bundle/tool docs pass residue scan | residue scan clean |
| T7 | Create bundle repo contents in `/Users/bytedance/wk/cross-team/` | completed | `README.md`, `AGENTS.md`, `.gitignore`, `cross-team.default.json` | no examples shipped |
| T8 | Add bundle submodules | completed | submodules `artifact_types`, `parallax`, `warrant` | recursive status shows exactly those first-level tool submodules |
| T9 | Add bundle launch surface after upstream support lands | completed | `bin/parallax`, `bin/warrant-check` | launchers pass through `CROSS_TEAM_CONFIG`; no split live config |
| T10 | Fresh consumer integration test in `/Users/bytedance/wk/cross-team/` | completed | `test-fixtures/consumer-basic-152851/` | `cross-team.json` drives both Parallax and Warrant |
| T11 | Migration rehearsal for this repo | completed | `maiwang-claude` now uses one `cross-team` SSH submodule plus root `cross-team.json` | Parallax detect and Warrant check pass |
| T12 | Final release/pin decision | completed | consumer pins public bundle commit `8dfd45a`; no local-only tool pins remain | submodule remote is `git@github.com:hotneutron/cross-team.git` |

## 3. Test Workspace Layout

Use `/Users/bytedance/wk/cross-team/` for bundle implementation and integration testing:

```text
/Users/bytedance/wk/cross-team/
  .git/
  AGENTS.md
  README.md
  .gitignore
  cross-team.default.json
  artifact_types/        # submodule
  parallax/              # submodule
  warrant/               # submodule
  test-fixtures/
    consumer-basic/
      cross-team/        # bundle as submodule in a fresh consumer fixture
      cross-team.json    # versioned consumer config
      .plan/
```

`test-fixtures/consumer-basic/` can be created and destroyed during testing. It is not an
example shipped to users; it is a regression fixture.

## 4. Required Test Gates

### G1 - Warrant `consumer_root`

Fixture:

```text
test-fixtures/consumer-basic/
  cross-team/warrant/...
  cross-team.json
  .plan/parent.md
  .plan/child.md     # parent_artifacts: [.plan/parent.md]
```

Command shape:

```bash
CROSS_TEAM_CONFIG=cross-team.json cross-team/bin/warrant-check
```

Pass condition: zero missing-parent errors. The parent must resolve at the consumer root, not
inside `cross-team/warrant`.

### G2 - One-file Parallax Config

Fixture:

```text
test-fixtures/consumer-basic/cross-team.json
```

Pass condition: Parallax reads partner registry and tier config from `cross-team.json` directly
via `CROSS_TEAM_CONFIG`, without `partners.json`, `tiers.json`, or generated split live config.

### G3 - One-file Warrant Config

Pass condition: Warrant reads authority map, `consumer_root`, docs root, registry path, and
skip/extra-root settings from the `warrant` section of `cross-team.json`.

### G4 - No Nested Registry

Pass condition:

```bash
test ! -e parallax/artifact_types
test ! -e warrant/artifact_types
git submodule status --recursive
```

The recursive submodule listing must show `artifact_types`, `parallax`, and `warrant` as the
bundle's first-level submodules, with no nested registry checkout under either tool.

### G5 - No Consumer Residue

Pass condition:

```bash
rg -n "\\b(ds4m|op|gpt|maiwang)\\b" artifact_types parallax warrant README.md AGENTS.md cross-team.default.json
```

Every hit is either removed or justified as a deliberately named conformance fixture.

### G6 - No Runtime `.plan/` Default

Pass condition:

```bash
rg -n '"\\.plan/?"|\\.plan/' parallax warrant artifact_types
```

No runtime-code hit is allowed. `.plan/` may appear in `cross-team.default.json` and in test
fixtures only.

## 5. Execution Order

1. Create or clone `/Users/bytedance/wk/cross-team/`.
2. Land upstream Warrant `consumer_root` with conformance.
3. Land upstream unified `cross-team.json` support in Parallax and Warrant.
4. Remove nested `artifact_types` from Parallax and Warrant.
5. Clean hardcoded defaults and consumer-specific text from all three tool repos.
6. Create the bundle repo files and submodule pins.
7. Run G1-G6 in `/Users/bytedance/wk/cross-team/`.
8. Only after all gates pass, plan consumer migration for `maiwang-claude`.

## 6. Do Not Do

- Do not switch this repo or any consumer before upstream one-file config and Warrant
  `consumer_root` both land.
- Do not use temporary split-config or absolute-policy shims.
- Do not push tool or bundle repos without explicit user signal.
- Do not pin a bundle submodule to an unpushed local-only commit.
- Do not ship `examples/`; make `README.md` and `AGENTS.md` sufficient.

## 7. Current State

- Source proposal is committed at `8791cf8`.
- This tracker is now part of the migration commit.
- `maiwang-claude` has switched from three direct tool submodules under `cross-team/` to one
  SSH bundle submodule:
  - `.gitmodules`: `cross-team -> git@github.com:hotneutron/cross-team.git`
  - `cross-team`: `8dfd45a`
  - `cross-team/artifact_types`: `a42ef56`
  - `cross-team/parallax`: `c6eef7d`
  - `cross-team/warrant`: `e174732`
- The old live files `cross-team/partners.json`, `cross-team/tiers.json`, and
  `cross-team/policy.json` were consolidated into root `cross-team.json`.
- Smoke checks passed from the consumer root:
  - `CROSS_TEAM_CONFIG=cross-team.json cross-team/bin/parallax detect gpt`
  - `CROSS_TEAM_CONFIG=cross-team.json cross-team/bin/warrant-check`
- Warrant also caught and then passed after updating stale proposal parent refs from the old
  three-file config to `cross-team.json` and `cross-team/cross-team.default.json`.
- No pushes were performed by this consumer migration step.

## Revision History

| Rev | Timestamp | Change | Source |
|---|---|---|---|
| 1 | 2026-07-16 22:57 PDT | Recorded completed T11/T12 migration state, public bundle pins, consolidated root config, and consumer smoke checks. | local migration |
