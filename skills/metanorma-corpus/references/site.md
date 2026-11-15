# Site pipeline reference

## The gates, in order

1. **Site generate** — every registered document compiles. Failure
   classes: missing `:mn-document-class:`, ragged tables, broken
   fences, math parser mismatches (see the transcription skill's
   references).
2. **mnconvert STS** — per-document Metanorma XML → NISO STS with XSD
   validation. Compile-clean documents fail here on structure the
   compiler accepts:
   - `[bibliography]`-styled sections mid-body, or nested sections
     under any bibliography-styled heading;
   - listing/literal/tabular content inside term definitions or
     termnotes (`<preformat>` illegal in the termbase);
   - multiple level-0 titles per document (merged-copy signature);
   - duplicate anchors derived from identical stems.
3. **Completeness gate** (where installed) — source clause-level
   titles vs compiled XML titles plus `term/preferred/name` elements,
   unicode/entity-normalized, layout-agnostic (resolve compiled output
   by glob + year + language tier). Presentation-generated titles
   (`abbreviated_terms` definitions, `<references>` sections) are
   exempted by element presence. Phrase-exact exemption strings —
   `%w` word-splitting has biten multi-word titles before.

## Manifest discipline

```yaml
metanorma:
  source:
    files:
      # comment group headers per family
      - sources/<family>/<year>/document.adoc
      - sources/<family>/<year>/en/document.adoc
      - sources/<family>/<year>/fr/document.adoc
      # pending: sources/<family>/<year2>/ — restructuring pending
```

- Entries resolve on the branch; duplicates fail; comments document
  pending work with the blocking reason.
- Language tiers publish two documents from one directory — count
  documents, not directories.

## Layout migration

- `git mv` per document directory; verify with
  `git diff -M --name-status` (expect R100).
- Update the manifest paths in the same commit.
- Relocations of documents under active review conflict with the
  review branches — resolve as corrected content at the renamed path:
  `git show origin/main:<old-path> > <new-path>` per conflicted file,
  delete files removed on main.
- `find sources -type d -empty -delete` after moves (git does not
  track directories).

## Artifact hygiene

```gitignore
sources/**/document.xml
sources/**/document.presentation.xml
sources/**/document.html
sources/**/document.err.html
sources/**/document.rxl
sources/**/document.doc
sources/**/document.pdf
sources/**/document.sts.xml
sources/**/document.pdf.fo.xml
sources/**/document.xml.abort
sources/**/*.asciidoc.log.txt
relaton/
.cache/
```

Purge commits are valid PRs (large deletions of committed debris);
verify nothing source-shaped is lost with the debris.

## Wave mechanics

- Merge one, fetch, rebase the next locally, resolve the manifest
  (keep both insertions in corpus order), `--force-with-lease` push,
  merge. Repeat.
- CI runs per PR on the merge result; a green PR that was rebased
  after a sibling merged needs one more CI cycle before its merge.
- After the wave: fetch, fast-forward local main, confirm the site run
  on the final tip, reconcile the manifest count.
