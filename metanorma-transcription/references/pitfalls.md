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
| `Malformed MathML: [plurimath] Failed to parse … type \`asciimath\`` | LaTeX content in a stem paragraph or `[stem]++++` passthrough — the block style selects the parser | `[latexmath]` + `----` blocks for LaTeX, no `\[ \]` delimiters; `[$latexmath]` is a role, not a style |
| math fails one formula at a time across runs | plurimath aborts on the first unparseable formula; the FATAL list is truncated | convert every formula in one pass; grep the log for "Failed to parse" until zero |

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
- **PDF first.** PDF rendering is the slow step; validate XML and HTML
  first, produce PDF last.
- **Validating with the flag on.** `metanorma compile -t iso` hides a
  missing `:mn-document-class:`; CI compiles without it and fails. Local
  validation must match CI.
