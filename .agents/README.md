# Profile map

The files in this directory are reusable working defaults for research agents. Keep them compact, concrete, and easy to apply.

## Modules

- `writing.md` — scientific prose, structure, claims, literature, captions.
- `math.md` — derivations, notation, assumptions, approximations, interpretation.
- `coding.md` — scientific code, repositories, validation, and builds.
- `figures.md` — scientific plots, typography, labels, legends, panels, and visual validation.
- `templates.md` — compact writing, figure, and code patterns at several scales.

Do not add another module unless a durable class of behavior cannot fit cleanly into these files.

## How an agent should use the profile

Read only the modules required by the current task.

Rules are defaults, not a reason to rewrite functioning project conventions. Existing project behavior takes precedence when it is deliberate and correct.

Templates are examples. They are not checklists and should not be copied mechanically. Use them to recover the preferred shape of a paragraph, subsection, caption, script, or compute/plot split.

## How to change the profile

A profile change should encode a durable behavior.

Good reasons:
- the user explicitly states a preference;
- the same correction appears repeatedly;
- a pattern is clearly supported across current source work.

Bad reasons:
- one task happened to need a special case;
- one old repository contains a historical implementation;
- an agent prefers a convention that the user has not expressed.

When editing:
- change the smallest relevant rule;
- merge overlapping rules;
- remove a replaced rule;
- keep examples short;
- avoid exceptions that require agents to infer hidden intent.

## Evidence hierarchy

For all profile changes:

1. explicit user preference;
2. repeated patterns in the user's current work;
3. repeated patterns across older work.

Current maintained projects should outweigh old coursework or one-off historical choices.

## Portability

`install.sh` copies `AGENTS.md` and every Markdown file in `.agents/` into another project.

Adding files therefore increases the context every installed agent may need to reason about. Keep the profile small.
