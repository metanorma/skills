# Pitfalls — the failures that break builds and renderings

Each of these cost a build cycle in real transcriptions. They are the
first things to check when a converted document fails or renders wrong.

## Build failures

| Symptom | Cause | Fix |
|---|---|---|
| `Please specify a standard type` | missing `:mn-document-class:` | add the flavor attribute; never mask with `-t` |
| `annex sections do not support nested sections` | `[annex]` style, or depth-5 headings inside annexes | `[appendix]`; cap depth at 4; label paragraphs for ATS labels |
| `FATAL Image not found: images/x/images/y` | `:imagesdir:` double-prefixing | omit `:imagesdir:`; body paths carry `images/…` |
| `dropping cells from incomplete row` | ragged rows, trailing cells after row spans | normalize to column count; strip trailing empties on spanned rows |
| `table missing leading separator` | content line inside a table without a cell marker | move the line out or give it a cell |
| `ID … has already been used` | duplicate anchors (inserted terms duplicating converted ones) | one emission path per entry |
| compile passes with `-t` but fails in CI | the flag masks a missing flavor attribute | compile without `-t` |

## Rendering failures

- **Document text as source code.** An unpaired `----` literal fence, or
  interleaved `[example]`/`====` fences, traps prose in blocks. Audit the
  rendered HTML: a `<pre>` whose text is prose (long, no code signature)
  is a broken wrapper. Fence balance in the source is absolute.
- **Phantom figures.** A paragraph line starting with `[` (e.g.
  `[SOURCE: …]`) parses as block attributes and renders as an empty
  figure with a `<pre>`. Write citations as `[.source]` blocks.
- **Dangling cross-references.** `<<interface>>`-style stereotypes parse
  as xrefs; use guillemets. The validator reports any `<xref>` whose
  target has no anchor.
- **Notes numbered wrong.** Notes inside term clauses must be `NOTE:`
  lines (termnote); a prose "Note 1 to entry:" prefix retained in the
  text double-numbers after rendering.
- **Stale markup remnants.** `[.s12]#` role spans, `++` passthroughs and
  `{plus}` escapes leaking into output text — clean inline before
  delivery.

## Process failures

- **Rebuilding from originals loses manual output edits.** Every
  correction goes into the pipeline (the script), then the pipeline reruns
  from the source. A fix applied only to the generated file is lost on
  the next run.
- **Assuming the conversion dropped content.** Before reconstructing
  "missing" entries, check whether the source carries them behind
  cruft — wrapped numbering (`[#b12]##‌##4.37[#b13]##‌##…`) hides entries
  from naive patterns. Match the cruft, don't re-author from the PDF.
- **Regexes that never match.** Digit-count mistakes (`iso-19\d\d/`
  against `iso-19104/`) fail silently — verify each rewrite by counting
  replacements, and assert on the expected count.
- **Silent no-op matches.** A match condition defeated by an invisible
  detail — a trailing space from joined lines defeating an
  `endswith('.')`, a capture index shifting when a helper pattern gains
  a group — produces wrong output with no error. Print the matched text
  while developing rules; assert on counters.
- **Structure edits that eat headings.** Inserting a section before an
  existing heading and replacing without re-including the heading line
  deletes it silently — requirement lists lose their parent clause and
  the next section absorbs them. If an edit's replacement does not end
  with the heading it precedes, the heading belongs in the replacement.
- **Two emission paths for one content.** A manual workaround (hand-
  inserted terms, hand-fixed sections) plus a pipeline that later gains
  the same capability produce duplicates — duplicate-anchor build
  failures or repeated content. When the pipeline learns to emit
  something, delete the workaround in the same change.
- **Rerunning against already-transcribed output.** The pipeline anchors
  on the source's cover headings and cruft; running it against HEAD
  fails outright (its landmarks are gone) or double-applies. Restore
  the originals from the source of record before every rerun.
- **Assuming the conversion dropped content.** Before reconstructing
  "missing" entries, check whether the source carries them behind
  cruft — wrapped numbering (`[#b12]##‌##4.37[#b13]##‌##…`) hides entries
  from naive line patterns. Match the cruft, don't re-author from the
  PDF.
- **PDF first.** PDF rendering is the slow step; validate XML and HTML
  first, produce PDF last.
- **Validating with the flag on.** `metanorma compile -t iso` hides a
  missing `:mn-document-class:`; CI compiles without it and fails. Local
  validation must match CI.
