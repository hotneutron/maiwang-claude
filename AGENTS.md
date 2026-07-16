Working rules. Keep them terse.

## Authority

- Local behavior: this file and `SKILL.md`.
- Partner claims enter local methodology only through Parallax plus a local adoption artifact.
- Dirty working trees are evidence of local state, not committed truth.
- Specificity is not authority; verify speculative claims before building on
  them.

## Partner Access

Do not read partner repos directly. Use Parallax (`detect`, `read`, `prepare`,
`relay`) for op/ds4m material so reads are committed-state and logged. Shared
submodules already checked out in this repo may be read locally.

## Sync Protocol

- Run `detect <partner>` before partner sync.
- Read only T1/T2 obligations through `parallax.py read`.
- Treat T3 as optional context and T4 as unread.
- Write at most one local reaction per partner sync cycle.
- Reconcile only committed artifacts; dirty partner state is not shared truth.
- Relay only committed-clean local artifacts.
- Advance ledger only for a real sync, not empty housekeeping.
- No third prose round on a dispute without new measurement.

## Convergence Tags

- `independent`: pre-registered, measurement-forced, no read-ahead.
- `propagated`: adopted or negotiated from another lane.
- `modal`: shared prompt, prior, textbook, or shared tool explains agreement.
- `n/a`: no corroboration claim.

## Work Rules

Before proposing: name the source artifact and its authority.

Before accepting a critique: verify at the relevant commit through Parallax.

Before implementing novel tooling, protocol, compiler, or ISA surface: cite or
produce an existing-art study, or explicitly mark the study-gate warning.

After adding an instrument, axis, report, check, or simulator surface, exercise
the new observability before moving on, or explicitly record why it is
deferred. Example: adding `cp_degree` is incomplete until a sweep/report uses it
or records its blocker.

For shared repos: use public GitHub remotes, add conformance for behavior
changes, and never pin broken commits.

## Repo Style

- Keep root docs focused on this repo.
- Name docs `{YYMMDD}-{HHMM}-{type}-{topics}.md`; get timestamp from `date`.
- Doc types: `findings`, `reaction`, `reflection`, `cross-check`, `brainstorm`.
- Any amendment to an existing artifact must add/update timestamped `## Revision History`.
- Prefer local adoption notes over copied partner history.
- Push only on explicit user signal. No `Co-Authored-By` trailer.

