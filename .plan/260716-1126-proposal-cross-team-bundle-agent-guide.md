---
artifact_type: proposal
authority: derived
generated_by: cross-team-repo-proposal
convergence: propagated
parent_artifacts:
  - AGENTS.md
  - .gitmodules
  - cross-team/.gitignore
  - cross-team/partners.json
  - cross-team/tiers.json
  - cross-team/policy.json
  - cross-team/parallax/README.md
  - cross-team/warrant/reference/README.md
  - gpt:.plan/260716-1142-reaction-cross-team-bundle-agent-guide.md
tags: [cross-team, tooling, submodules, config, agent-guide, portability]
---

# Proposal - Cross-team Tool Bundle Repo with Defaults and Agent Guide

*Status: proposal, not implementation. Timestamp from `date`: 2026-07-16 11:26 PDT.*
*Revision 2 incorporates GPT feedback read via Parallax at gpt HEAD `16a219b`.
Convergence: `propagated` — this revision adopts and counters partner critique rather than
claiming independent corroboration.*

## 0. Source Artifacts and Authority

- `AGENTS.md` is the local authority for workflow: partner reads must go through Parallax,
  shared repos use public GitHub remotes, dirty trees are local state rather than committed
  truth, and pushes require explicit user signal.
- `.gitmodules`, `cross-team/*.json`, and `cross-team/.gitignore` are observed local state.
  They show the current adoption friction but are not themselves a portable design.
- `cross-team/parallax/README.md` and `cross-team/warrant/reference/README.md` define the
  current tool contracts: Parallax uses a sync home with `partners.json`/`tiers.json`; Warrant
  uses a consumer `policy.json`.
- `gpt:.plan/260716-1142-reaction-cross-team-bundle-agent-guide.md` is a propagated critique,
  read through Parallax at gpt HEAD `16a219b`. It reframes the Warrant path issue as a general
  upstream defect, not a per-repo workaround.
- Current workspace note: local submodule dirt or local-only commits are **not** design truth.
  Do not gate the bundle on `7db3394` or any other unpushed implementation state.

## 1. Problem

The cross-team tools are useful, but adoption is too expensive and too easy to get subtly
wrong:

1. A consumer repo currently has to wire **three submodules** directly:
   `artifact_types`, `parallax`, and `warrant`.
2. The consumer currently has to hand-author three fragmented config files:
   `partners.json`, `tiers.json`, and `policy.json`.
3. Those config files mix two things that should be separate:
   shared defaults and local consumer state.
4. The same registry is nested under `parallax/artifact_types` and `warrant/artifact_types`,
   even though the registry should be a sibling dependency owned once by the tool bundle.
5. Warrant path resolution is a general upstream defect for submodule consumers: docs can be
   discovered through a relative `docs_dir`, but `parent_artifacts` are checked against the
   Warrant engine repo root, which causes false missing-parent errors for repo-relative parents
   and can also create false positives when a similarly named file exists inside the tool
   submodule.
6. Agent operating rules are spread across the consuming repo, Parallax docs, Warrant docs, and
   local memory. A new project should not need to rediscover those rules.
7. A bundle-level `AGENTS.md` will coexist with each consumer's local `AGENTS.md`; without a
   precedence rule, the shared tool bundle can accidentally launder authority into local
   project behavior.
8. The tool repos still carry too much local/default residue: hardcoded default configs in
   implementation/docs, plus project/team-specific text such as `ds4m`, `op`, and `gpt`. A
   reusable toolchain should not leak one consumer's names into another consumer's setup.
9. Reusable configs and tool code should not carry hardcoded project parameters. The only
   allowed default project convention is `.plan/` as a document directory, and it may appear
   only in committed `cross-team.default.json`, not in Parallax/Warrant/artifact_types runtime
   code.

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
  cross-team.default.json
  artifact_types/        # submodule: hotneutron/artifact_types
  parallax/              # submodule: hotneutron/parallax
  warrant/               # submodule: hotneutron/warrant
```

Consumers keep one live config file, owned and versioned by the consumer repo outside the
`cross-team/` submodule:

```text
cross-team/              # reusable bundle submodule; no live consumer config
cross-team.json          # copied from cross-team/cross-team.default.json, edited, versioned
_cross-team/             # ignored runtime scratch (read logs, inboxes, detect output)
```

This gives every project the same starting point while keeping consumer identity, partner
paths, pins, and local document roots out of the reusable bundle while still versioning them in
the consuming project. "One live config" means `cross-team.json`; generated read logs, inboxes,
and detect outputs are runtime scratch, not config.

### 2.1 Two Tracks: Owner-side Upstream vs Consumer-side Adoption

Split the work explicitly:

| Track | Owner | What ships |
|---|---|---|
| **Owner-side upstream** | maintainers of `warrant`, `parallax`, `artifact_types`, then `cross-team` | Warrant `consumer_root` fix + conformance; one-file `cross-team.json` config support; removal of nested `artifact_types`; removal of hardcoded default configs and consumer-specific `ds4m`/`op`/`gpt` text; bundle submodule pins to public commits |
| **Consumer-side adoption** | each project consuming the bundle | after upstream prerequisites land, copy `cross-team.default.json` -> versioned `cross-team.json` outside `cross-team/`; local partner paths/pins live in that one file |

This distinction is load-bearing. No consumer should switch to the new bundle flow until both
upstream prerequisites are landed and conformance-tested:

1. Parallax/Warrant can consume the unified `cross-team.json` shape directly.
2. Warrant resolves consumer repo-relative `parent_artifacts` via `consumer_root`.

Temporary split-config shims are explicitly out of scope.

## 3. One Default JSON, One Live Consumer Config

Global config rule:

- `cross-team.default.json` may contain neutral schema/config shape, registry-derived type
  mappings, and the default `.plan/` document directory.
- Defaults must not contain hardcoded consumer parameters: real partner names, team names,
  local paths, ledger pins, sync dates, project stopword lists, promotion thresholds,
  domain-specific trigger lists, or consumer-specific policy choices.
- Tool code must not hardcode `.plan/` or any other consumer document root; code reads those
  values from explicit config.
- Any value that a consumer is expected to tune belongs in versioned consumer config outside
  `cross-team/` (`cross-team.json`) or must be a neutral placeholder.

### 3.1 `cross-team.default.json`

Purpose: portable unified template for Parallax and Warrant.

Requirements:

- Contains `_doc`, `version`, and top-level sections for `parallax` and `warrant`.
- Consolidates what used to be `partners.json`, `tiers.json`, and `policy.json` into one
  consumer-owned file after copy.
- Includes an example under a non-runtime key such as `_example_partner`.
- Does **not** carry any real `last_pinned` or `last_sync` from a consumer.
- Uses paths relative to the consumer repo root when copied to `cross-team.json`.

Sketch:

```json
{
  "_doc": "Copy to ../cross-team.json and edit locally. This live config is committed by the consumer repo.",
  "version": "1.0",
  "parallax": {
    "partners": {},
    "tiers": {
      "self_name": "<consumer>",
      "doc_dirs": [".plan/"]
    }
  },
  "warrant": {
    "type_authority": {},
    "config": {
      "consumer_root": ".",
      "docs_dir": ".plan",
      "registry": "cross-team/artifact_types/artifact_types.json"
    }
  },
  "_example_partner": {
    "team-b": {
      "path": "../sibling-repo",
      "team_name": "team-b",
      "protocol_version": "2.2",
      "last_pinned": null,
      "last_sync": null
    }
  }
}
```

### 3.2 Parallax Section

Purpose: registry-aligned Parallax tier defaults inside `cross-team.json`.

Requirements:

- Mirrors `artifact_types/artifact_types.json` for `default_tier`.
- Includes `doc_dirs: [".plan/"]` as the only hardcoded document-directory convention in
  `cross-team.default.json`.
- Does not hardcode trigger/contract path sets for `AGENTS.md`, `docs/`, schemas, protocol
  files, or project-specific directories. Consumers add those in their versioned `cross-team.json`
  if their repo needs them.
- Leaves `self_name` as an obvious placeholder that the consumer must edit.

This file should be useful as-is after changing only `self_name`.

### 3.3 Warrant Section

Purpose: registry-aligned Warrant authority defaults inside `cross-team.json`.

Requirements:

- Mirrors `artifact_types/artifact_types.json` for `default_authority`.
- Points registry validation at the sibling registry in the bundle:
  `artifact_types/artifact_types.json`.
- Does not bake in this repo's `.plan/` or `paper-library/` paths.
- Supports consumer-local document roots after copy to `cross-team.json`.

The current Warrant engine makes this hard because `parent_artifacts` are resolved against the
engine repo root. The bundle must not be used for consumer migration until Warrant supports
`consumer_root`:

1. Required: Warrant supports `config.consumer_root`, and both `docs_dir` and
   `parent_artifacts` are resolved relative to that root. Resolution precedence:
   `config.consumer_root` > environment override > `methodology_state.json` walk > git
   toplevel fallback. That preserves existing consumers while fixing the submodule case.

Without this, the same false missing-parent problem will recur in every consumer. A temporary
wrapper that materializes an absolute policy is unacceptable for the migration target.

## 4. Remove Nested `artifact_types` from Parallax and Warrant

`artifact_types` should be owned once by the bundle, not nested inside each tool repo.

Target state:

```text
cross-team/artifact_types/              # one registry checkout
cross-team/parallax/                    # no parallax/artifact_types
cross-team/warrant/                     # no warrant/artifact_types
```

Required owner-side upstream changes:

- In `parallax`, remove `.gitmodules` entry and gitlink for `artifact_types`.
- In `warrant`, remove `.gitmodules` entry and gitlink for `artifact_types`.
- Update docs to say the registry is a sibling supplied by `hotneutron/cross-team`, not a
  nested submodule.
- Verify each tool's own conformance after removal. "Packaging only" is a hypothesis until the
  repo proves it.
- Add Warrant conformance for the runtime `consumer_root` behavior. The fixture: a fresh
  consumer repo vendors Warrant as a submodule, has docs under `.plan/`, and a document whose
  `parent_artifacts` points to another repo-relative `.plan/` file. Expected result: zero
  missing-parent errors.

Until those commits are pushed to the public remotes, the bundle must not pin local-only
submodule commits.

### 4.1 Remove Hardcoded Defaults and Consumer-specific Text

The bundle should make defaults explicit at the adoption boundary. The tool repos should not
carry hidden, consumer-flavored runtime defaults.

Owner-side cleanup request:

- **Parallax:** remove or minimize inline `DEFAULTS` that duplicate registry-derived tier
  config. Runtime tiering should come from the unified consumer config (`cross-team.json`) or
  from neutral self-test fixtures. Any fallback that remains must be clearly bootstrap-only and
  neutral.
- **Warrant:** remove or minimize hardcoded authority maps that duplicate
  `cross-team.default.json` / `artifact_types`. Runtime authority should come from the consumer
  config's Warrant section. The reference policy can remain only as a neutral self-conformance
  fixture, not a consumer template.
- **Artifact_types:** remain the vocabulary registry, not a consumer config carrier. It may
  define registry fields such as `default_tier` and `default_authority`; it should not contain
  Parallax/Warrant live config, partner names, ledger examples, or consumer-specific prose.
- **All three repos:** scrub `ds4m`, `op`, `gpt`, `maiwang`, and similar project/team names from
  default configs, READMEs, examples, and tests unless the name is deliberately part of a
  fixture whose purpose is to prove namespace handling. Prefer neutral placeholders:
  `team-a`, `team-b`, `<partner>`, `<consumer>`.
- **Config defaults:** remove hardcoded parameters from reusable configs. The exception is
  the default `.plan/` document directory, and that exception lives only in committed
  `cross-team.default.json`, not in runtime code. Everything else that smells local — partner names,
  repo paths, pins, dates, stopword lists, thresholds, document-root overrides beyond `.plan/`,
  and domain-specific triggers — must move to versioned consumer config outside `cross-team/`
  or become a neutral placeholder.

Acceptance check:

```bash
rg -n "\\b(ds4m|op|gpt|maiwang)\\b" artifact_types parallax warrant
```

Any hit must be either removed, moved into a clearly named conformance fixture, or justified in
the release notes. The point is not cosmetic; it prevents consumer-specific language from
becoming accidental method authority.

## 5. Cross-team `AGENTS.md`

The new repo needs its own agent guide because it is the adoption boundary. The guide should
be short and operational.

Minimum content:

```text
# Cross-team Agent Guide

## Authority
- This repo is the tool bundle for cross-team methodology.
- Tool source lives in submodules; defaults and adoption docs live here.
- Consumer live config is outside this repo, committed by the consumer repo, and not shared
  bundle truth.
- Scope rule: this guide governs bundle mechanics only. The consumer repo's AGENTS.md remains
  authoritative for local behavior, domain rules, and commit/push policy.

## Setup
- Copy cross-team/cross-team.default.json -> ../cross-team.json.
- Edit only consumer identity, partner paths, document roots, and pins in ../cross-team.json.
- Keep live consumer config outside cross-team/ and committed by the consumer repo.

## Parallax
- Use Parallax with CROSS_TEAM_CONFIG=<consumer>/cross-team.json only after upstream one-file
  config support lands.
- Run detect before any partner sync.
- Read partner artifacts only via parallax.py read.
- Relay only committed-clean local artifacts.
- Advance the ledger only for a real sync.

## Warrant
- Run Warrant with CROSS_TEAM_CONFIG=<consumer>/cross-team.json only after upstream
  `consumer_root` and one-file config support land.
- Treat parent path errors as blocking unless they are confirmed resolver bugs.
- Do not use temporary split-config or absolute-policy shims as the migration path.

## Submodules
- Do not edit parallax, warrant, or artifact_types from a consumer task.
- Upstream tool changes require a focused commit in the tool repo, conformance where behavior
  changes, then a bundle submodule bump.

## Commit Rules
- Commit cross-team.json in the consumer repo.
- Do not commit generated runtime scratch, inboxes, or detect logs.
- Push only on explicit user signal.
```

The precedence clause is not optional. Without it, the bundle `AGENTS.md` becomes a shared
policy surface that could override a consumer's local project rules by accident.

## 6. `.gitignore`

The bundle `.gitignore` should ignore only bundle-local scratch. The live consumer config is
outside `cross-team/`, so the bundle must not ignore it.

Recommended entries:

```gitignore
# Bundle-local runtime scratch only
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

The consumer repo's own `.gitignore` should ignore generated scratch such as `_cross-team/`,
not `cross-team.json`.

## 7. Adoption Flow for a New Consumer

A fresh consumer project should need this sequence:

```bash
git submodule add https://github.com/hotneutron/cross-team cross-team
git -C cross-team submodule update --init --recursive

cp cross-team/cross-team.default.json cross-team.json
$EDITOR cross-team.json
```

Then:

```bash
CROSS_TEAM_CONFIG=cross-team.json cross-team/bin/parallax detect <partner>
CROSS_TEAM_CONFIG=cross-team.json cross-team/bin/warrant-check
```

These commands are valid only after upstream one-file config support and Warrant
`consumer_root` both land. Before that, do **not** switch consumers to the new bundle flow; keep
the current explicit config wiring.

Later, if repeated adoption proves painful, add a tiny bootstrap script. That script is
convenience tooling, not the core design, and should come with a smoke test.

## 8. Migration Plan for This Repo

1. Stop treating local submodule dirt or local-only commits as accepted design. Either upstream
   the needed tool changes intentionally through public remotes, or replace them with the
   eventual public commits.
2. File owner-side upstream work:
   - Warrant `consumer_root` + regression fixture.
   - Parallax and Warrant direct support for `CROSS_TEAM_CONFIG=<consumer>/cross-team.json`.
   - removal of nested `artifact_types` from `parallax` and `warrant`.
3. Create `hotneutron/cross-team` as a new public repo.
4. Add the three submodules inside it:
   `artifact_types`, `parallax`, `warrant`.
5. Add `cross-team.default.json`, `.gitignore`, `README.md`, `AGENTS.md`, and thin launcher
   entry points (`bin/parallax`, `bin/warrant-check`) only after upstream tools can read one
   config directly. Launchers must not synthesize split live config as a compatibility shim.
6. Remove nested `artifact_types` from `parallax` and `warrant` through their own upstream
   commits, then bump the bundle submodule pins.
7. In this consumer repo, replace the three direct root submodules with one direct submodule:
   `cross-team`.
8. Consolidate current consumer-specific config into versioned root `cross-team.json`.
9. Run the smoke tests in section 9.
10. Commit the consumer repo only after the bundle repo and tool submodule pins are
   committed-clean.

## 9. Acceptance Tests

A bundle release is acceptable only if these pass from a fresh consumer clone:

1. `git submodule status --recursive` shows exactly three first-level bundle submodules:
   `artifact_types`, `parallax`, `warrant`.
2. No nested `parallax/artifact_types` or `warrant/artifact_types` appears.
3. `CROSS_TEAM_CONFIG=cross-team.json cross-team/bin/parallax detect <partner>` reads the
   `parallax` section of the versioned consumer config without generating split live config.
4. `CROSS_TEAM_CONFIG=cross-team.json cross-team/bin/warrant-check` reads the `warrant` section
   of the same versioned consumer config and validates a known-good doc whose
   `parent_artifacts` use normal consumer repo-relative paths through upstream `consumer_root`.
   This must be a fresh-clone regression fixture, not this repo's current checkout.
5. After setup and one detect, `git -C cross-team status --short` shows no tracked dirt from
   consumer config or runtime state.
6. A second consumer can adopt the bundle by editing only its versioned root `cross-team.json`,
   with no changes to committed bundle defaults.
7. Tool conformance passes after removing nested `artifact_types` from `parallax` and
   `warrant`.
8. The bundle `AGENTS.md` explicitly says consumer `AGENTS.md` wins for local behavior.
9. `artifact_types`, `parallax`, and `warrant` have no unexplained consumer-specific text hits
   for `ds4m`, `op`, `gpt`, or `maiwang` in shipped defaults/docs.
10. Runtime defaults are not hidden in tool code: Parallax tier defaults and Warrant authority
   defaults are supplied through `cross-team.default.json` or explicit `cross-team.json`, with any remaining
   fallback documented as neutral bootstrap behavior.
11. Reusable default configs contain no hardcoded consumer parameters except the default `.plan/`
   document directory in `cross-team.default.json`; consumer-tuned values live only in versioned
   `cross-team.json` or neutral placeholders.
12. Parallax/Warrant/artifact_types runtime code contains no hardcoded `.plan/` document-root
   default; `.plan/` is supplied by bundle default JSON or consumer live config.
13. Migration is blocked unless upstream one-file config support and upstream Warrant
   `consumer_root` are both present. No temporary split-config or absolute-policy shim is an
   acceptable substitute.

## 10. Non-goals

- Do not turn `cross-team` into a monorepo for tool source. Tool source stays in submodules.
- Do not copy Parallax or Warrant implementation history into the bundle.
- Do not make consumer-specific read logs, inboxes, or scratch portable. Partner pins live in
  the consumer's versioned `cross-team.json`; generated runtime scratch stays ignored.
- Do not push local submodule commits until explicitly requested.
- Do not promote project-specific paper-library schema decisions into this bundle.
- Do not make the bundle `AGENTS.md` authoritative over consumer project behavior.
- Do not preserve `ds4m`/`op`/`gpt`/consumer-specific text in shared defaults for historical
  convenience.
- Do not keep hardcoded config parameters in tool code or shared defaults. The only exception
  is the default `.plan/` document directory, and only inside committed
  `cross-team.default.json`.

## 11. Resolved Decisions

Resolution rule: `accept` means "accept the recommendation" unless explicitly overridden.

1. **OQ1 default file names — revised.** Use one bundle default file
   (`cross-team.default.json`) and one consumer-owned live config (`cross-team.json`) outside
   `cross-team/`. The live config is committed by the consumer repo.
2. **OQ2 Warrant root semantics — accepted.** Add `consumer_root` to Warrant with conformance;
   do not migrate consumers until it lands upstream.
3. **OQ3 bootstrap script — accepted.** No bootstrap script initially; documented `cp` is the
   first adoption path. Add a script only after repeated adoption pain is measured.
4. **OQ4 examples — overridden: no examples.** Do not ship `examples/`. The `README.md` and
   `AGENTS.md` must be sufficient; the agent guide must work without example scaffolding.
5. **OQ5 bundle version coupling — accepted.** Make bundle releases the unit of upgrade and
   document when a consumer should temporarily pin a tool repo independently.
6. **OQ6 prior-art note — rejected.** This is an open-source repo packaging/adoption problem,
   not a paper. Do not add a formal prior-art/study artifact for repo bundling. Runtime changes
   still need tests/conformance; prose study is not the gate here.
7. **OQ7 hardcoded fallback policy — accepted.** Keep only the smallest neutral self-test
   fallback in code, and make real consumer operation require explicit `cross-team.json`.
8. **OQ8 default `.plan/` exception — overridden.** `.plan/` is **not** hardcoded in runtime
   code. It may appear only in committed `cross-team.default.json`; consumers can override it in
   versioned `cross-team.json`.
9. **OQ9 migration gate — resolved.** Upstream one-file config support and Warrant
   `consumer_root` must both land before any consumer switches. Temporary compatibility shims
   are unacceptable.

## 12. Recommendation

Proceed with the new `hotneutron/cross-team` repo, but do it as a packaging/adoption layer:
one bundle submodule for consumers, one sibling `artifact_types` checkout inside the bundle,
and one versioned consumer config (`cross-team.json`) copied from the bundle default. The key
portability fix is not merely moving JSON files; it is making the boundary explicit:

- committed defaults are shared in `cross-team/`;
- live config is consumer-owned and versioned outside `cross-team/`;
- generated scratch is ignored;
- tool source remains in upstream submodules;
- `AGENTS.md` in the bundle tells agents exactly how to operate the tooling.

Do not claim the bundle is easy to adopt until Warrant validates repo-relative parent artifacts
from a fresh consumer without false missing-parent errors and both tools consume
`cross-team.json` directly.

## Revision History

| Rev | Date | Change | Driver |
|---|---|---|---|
| 1 | 2026-07-16 11:26 PDT | Initial proposal for `hotneutron/cross-team` bundle repo with defaults, `.gitignore`, agent guide, migration plan, and acceptance tests. | user request |
| 2 | 2026-07-16 11:54 PDT | Incorporated GPT critique: Warrant root issue reframed as upstream defect; owner-side vs consumer-side tracks added; `consumer_root` precedence and regression fixture specified; bundle `AGENTS.md` scoped below consumer `AGENTS.md`; version-coupling and prior-art notes added. | GPT T1 reaction via Parallax at `16a219b` |
| 3 | 2026-07-16 11:59 PDT | Added upstream cleanup request to remove hardcoded default configs and consumer-specific `ds4m`/`op`/`gpt` text from `parallax`, `warrant`, and `artifact_types`. | user request |
| 4 | 2026-07-16 12:02 PDT | Added rule that reusable configs must remove hardcoded parameters except the default `.plan/` document directory. | user request |
| 5 | 2026-07-16 12:12 PDT | Resolved OQ1-OQ8: accepted recommendations except no examples, no prior-art paper/study for OSS packaging, and `.plan/` allowed only in default config, not runtime code. | user request |
| 6 | 2026-07-16 12:17 PDT | Consolidated live consumer config into one versioned root `cross-team.json` outside the `cross-team/` submodule; bundle now ships one `cross-team.default.json`. | user request |
| 7 | 2026-07-16 12:23 PDT | Made upstream one-file config support and Warrant `consumer_root` hard prerequisites before switching consumers; removed temporary split-config / absolute-policy shim path. | user request |
