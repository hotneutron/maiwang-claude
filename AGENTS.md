Working rules. Keep them terse.

## Authority

- Local behavior: this file.
- Dirty working trees are evidence of local state, not committed truth.
- Specificity is not authority; verify speculative claims before building on
  them.

## Work Rules

Before proposing: name the source artifact and its authority.

Before implementing novel tooling, protocol, compiler, or ISA surface: cite or
produce an existing-art study, or explicitly mark the study-gate warning.

After adding an instrument, axis, report, check, or simulator surface, exercise
the new observability before moving on, or explicitly record why it is
deferred. Example: adding `cp_degree` is incomplete until a sweep/report uses it
or records its blocker.

## Repo Style

- Keep root docs focused on this repo.
- Name docs `{YYMMDD}-{HHMM}-{type}-{topics}.md`; get timestamp from `date`.
- Doc types: `findings`, `reaction`, `reflection`, `cross-check`, `brainstorm`.
- Any amendment to an existing artifact must add/update timestamped `## Revision History`.
- Prefer local adoption notes over copied partner history.
- No `Co-Authored-By` trailer.
