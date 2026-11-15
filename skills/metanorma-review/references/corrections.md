# Correction conventions

How corrections are applied and how PRs land.

## Applying corrections

- Fix-ups go on the PR branch: rebase the branch locally, apply the
  fix, push with `--force-with-lease`. CI re-runs on the fresh push.
- One logical fix per commit; commit messages state the correction in
  the imperative ("Restore the printed symbol in the discharge-resistance formula").
  No attribution trailers, no generated-by footers.
- Stage by explicit path only; verify the staged set before
  committing.
- Fix only what ground truth proves wrong. Plausible-but-unverified
  improvements are review notes, not commits.
- When a review pass and a later pass touch the same document
  (encode → review → re-review), each pass lands as its own commit
  history on top of the previous — rewrites of sibling encodes use the
  same section-file conventions so diffs stay comparable.

## Landing PRs

- Rebase-merge keeps linear history: `gh pr merge --rebase`. When the
  base moved, rebase locally first; GitHub's conflict detection lags a
  force-push by seconds — retry once before hand-resolving.
- Conflict classes seen in practice:
  - Site-manifest list edits anchor on the same list lines — resolve
    by keeping both insertions in corpus order; relocations replace
    their old path.
  - Rename/modify (one side relocated a directory, the other edited
    files inside it): take the renamed path with the corrected
    content — `git show origin/main:<old-path> > <new-path>` per file,
    `git rm` the deleted ones, keep the rename.
  - Comment-block anchors (`# NOT YET REGISTERED …`) — resolve to the
    post-merge truth, not either side's stale note.
- Sequence multi-PR waves touching the same manifest: merge, fetch,
  rebase the next, push, merge — the manifest conflict is trivial but
  never skip the rebase.
- After a wave lands: fetch, fast-forward, confirm the site CI run on
  the final tip, and verify the manifest count equals the registered
  document count.

## What to fix vs what to note

| Finding | Action |
|---|---|
| Numeric value off vs print | fix (commit) |
| Modal verb swapped | fix (commit) |
| Fabricated sentence (absent from OCR AND pdftotext) | fix (commit) |
| Dropped clause/annex | fix (commit) or flag before merge |
| Faithful source typo | note only — transcribing it was correct |
| Stripped bibliography titles (house practice split) | note; corpus owner decides |
| Empty open-block leftovers | note (cosmetic); fix opportunistically |
| Stale comment blocks in manifest | fix in the same change that makes them stale |

## Per-corpus policies

Record the corpus's standing decisions and apply them without
relitigating: term-source "modified —" marker kept or stripped,
bibliography titles stripped or kept, keyword headings kept English in
translated trees, boilerplate left untranscribed. A review that
reverses a standing policy is wrong even when the other corpus does
the opposite.
