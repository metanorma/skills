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
| `nil.next=` NoMethodError in docidentifier cleanup | the `:docnumber:` + `:partnumber:` pair hits the flavor's typed-identifier crash (metanorma-iho#577) | carry one glued `:docnumber:` with a source comment until the flavor is fixed |
| compiles green locally, ancient behavior in CI | stale committed `Gemfile.lock` pins an old toolchain while local builds float forward | refresh and commit the lock with every toolchain change; diff resolved gem versions when local-green/CI-red |

## Publish failures (site pipeline)

A document that compiles clean can still fail the site pipeline's
mnconvert STS step (Metanorma XML → NISO STS). These cost three red CI
rounds in one corpus before they were catalogued:

- `bibliography sections do not support nested sections` — a
  `[bibliography]`-styled section in the body with subsections beneath
  it (typical of AI monoliths that merged two document copies).
  Bibliography styling is legal only on the final bibliography and on
  clause 2; nothing nests beneath either.
- `Invalid content was found starting with element 'preformat'` in the
  STS termbase — listing/literal/tabular blocks inside term
  definitions or term notes. Structured content in clause 3 moves to
  `[example]` blocks or regular clause content, never inside a term.
- `Invalid content was found starting with element 'references'` — the
  same monolith duplication: a `[bibliography]`-styled section sitting
  mid-body among ordinary clauses.
- Multiple level-0 titles (`= Title` more than once per document) —
  merged document copies; the site compiles them into unrecognizable
  STS. One level-0 title per document, always.
- **Leaked model-refusal text.** AI-assisted conversions embed their
  refusals ("I can't turn this into a verbatim transcription…") as
  document content, often in the front matter of the very chunk they
  refused. Grep the converted output for refusal phrasing before
  delivery.
- **Markdown fences render as literal text.** ` ``` ` and
  ` ```asciidoc ` lines from pandoc-class dumps are not AsciiDoc
  fences; they pass through as visible junk. Strip them in cleanup.

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
- **`****` used as a comment wrapper.** Four asterisks delimit an
  example block: licence notices and encoding remarks wrapped in them
  render as visible examples and can suppress the heading that
  follows. Meta-notes are `//` comments.
- **Hand-written note and example numbers.** `NOTE 1:` and `EXAMPLE 1:`
  prefixes double-number after Metanorma auto-numbers them; strip to
  bare `NOTE:` / `[example]`, and split multi-paragraph notes into
  `[NOTE]` open blocks.
- **Publisher "About" boilerplate transcribed.** The BSI/IEC/CENELEC
  "About the publisher" front-matter sections are furniture — deleted,
  not transcribed (the auto-injected boilerplate family extends to
  these).

## Process failures

- **Flagging injected boilerplate as lost content.** The numbered
  foreword items, the terms-clause intro, and the "no normative
  references" sentence are compile-time injections; their absence from
  sources is the correct state. Reviews and agents must not restore
  them — each restoration is a wasted review cycle.
- **Localizing clause keywords.** Renaming "Normative references" to a
  translated heading in a non-English tree breaks the flavor's clause
  detection and silently reclassifies the section as informative.
  Keep the English keyword; localize display with `[heading=…]`.
- **Taking the edition from the document ID.** The edition comes from
  the PDF cover and foreword ("This third edition…"), not from the
  identifier or filename — restructured editions have been encoded with
  the wrong edition number twice from ID-derived metadata.
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
- **Gem shadows behind a stale bundle.** An installed gem or a stale
  bundle can shadow the code under test: the bundle activates an old
  core gem over the fixed one, and the symptom reads as an unfixed
  flavor bug. List activated versions (`gem list`, `bundle list`)
  before diagnosing, and regression-compile previously-green exemplars
  after any bundle change.
- **CI path filters that skip lockfile-only changes.** A workflow
  triggered on changed paths does not fire for a lockfile-only commit —
  the render/regression job silently skips. Push an empty commit (or
  touch a tracked path) to force it.
- **Trusting an unflattened PDF render.** Transparent backgrounds
  rasterize black in ImageMagick renders. Flatten alpha to white before
  any visual comparison or palette claim; a black render is a
  rasterizer artifact, not evidence about the document.
- **Typed-value assumptions.** Edition, date, URN and title forms vary
  per printing (`Edition 1.0` / `Ed1.0` / `ed.1.0`; cover vs footer).
  Assuming one canonical form normalizes away the publisher's own
  spellings — record printed variants verbatim as open questions,
  never silently.
- **Inventing doctypes from document shape.** A category guessed from
  what the document looks like misroutes cover bands, XSL routing and
  bibdata. Verify against the publisher's authoritative catalogue
  first (the IALA catalogue carries exactly five technical categories);
  where no exemplar exists for a registered doctype, request one
  before encoding.
- **Repairing print errors while transcribing.** Editorial repairs get
  lost on the next pipeline rerun and are indistinguishable from
  transcription defects in review. Keep the printed text verbatim;
  record the oddity in a source comment as an open question.
- **Reading fleet CI as the gate.** Fleet CI may be red for unrelated
  in-flight fixes. Local `metanorma compile -x html` green is the
  gate; report which local gates passed and which workflow is red,
  never a bare color.
