---
name: metanorma-transcription
description: Transcribe standards documents (Word files, ISO-style PDFs, HTML exports, legacy machine conversions) into publication-grade Metanorma AsciiDoc, and validate the result compiles and renders correctly. Use when converting a standards document to Metanorma, choosing between Word, PDF and HTML extraction, repairing a converted document's structure, encoding terminological entries, setting up a transcription repository, or diagnosing why a Metanorma document renders text as source code.
---

# Transcribing documents into Metanorma

Transcribe a source document into Metanorma AsciiDoc that compiles clean,
renders correctly, and preserves every section of the source. The workflow
is: intake, front matter, structure, terms, furniture, tables, validation.
The reference files carry the details; this file carries the rules that
decide success or failure.

## The workflow

1. **Intake.** Identify the source kind and pick the pipeline:

   - **Word (.docx) — preferred when available.** Convert with the
     corpus's style-map importer. Style-map importers are per-corpus:
     the map keys on the publisher's own Word style names (the IALA
     importer keys on the secretariat's French and English style
     names). Prove the map by round trip — it must reproduce a
     hand-encoded document of the same family byte-identical before it
     converts anything new. See `references/sources.md` for the limits
     that stay manual (direct-formatted lists, revision tables).
   - **PDF — when no Word source exists.** Hand transcription;
     `references/sources.md` states the extraction tools (`pdftotext
     -layout`, `pdftohtml -xml`, pymupdf, ImageMagick renders) and the
     designation- and figure-recovery techniques.
   - **HTML exports** (structure-bearing, typography-degraded): with
     both HTML and PDF, take the skeleton from the HTML and the truth
     from the PDF. A Word file saved as HTML feeds the same route when
     direct Word import is unavailable.

   Set up the target layout per `references/structure.md`: the
   single-document layout (one `sources/<doc-slug>/` directory with
   `document.adoc`, `sections/`, and `images/`), or the corpus layout
   for structured publications (parts, language variants, amendment
   editions). Sources of record live in `reference-docs/` and are
   committed with the encoding PR that uses them; the pipeline is
   committed under `tools/` or `bin/`. Keep the source files
   untouched; the pipeline reruns from them, never from
   already-transcribed output.

2. **Front matter.** Every document carries the flavor attribute
   (`:mn-document-class:`) — the compile resolves the flavor from it, and
   a missing attribute is the most common CI failure. The identifier
   attributes (`:doctype:`, `:series:`, `:docnumber:`, `:edition:`,
   `:published-date:`, `:urn:`) come from the printed cover, verified
   against the publisher's authoritative catalogue; printed spelling
   variants are recorded, never normalized. See `references/encoding.md`
   for the attribute set, identifier conventions, doctype mapping, and
   the imagesdir rule.

3. **Structure.** Reconstruct the heading hierarchy from the source's own
   table of contents; strip bookmark anchors and pasted covers; declare
   annexes with `[appendix]`. See `references/pitfalls.md` for the annex
   rules that break builds.

4. **Terms.** Encode the terms and definitions clause in Metanorma term
   form: anchored term clauses, `alt:` designations, definition as the
   first paragraph, `NOTE:` lines, `[example]` blocks, `[.source]`
   citations, and `{{<<anchor>>,term}}` concept mentions. See
   `references/encoding.md`.

5. **Furniture.** Remove licence watermarks ("Licensed to", "Downloaded"),
   page headers and footers, copyright blocks, reference numbers, and
   bookmark cruft. The rendered document must not carry them.

6. **Tables.** Normalize ragged rows to the declared column count; handle
   row-span markers when counting cells; strip trailing empty cells on
   spanned rows. Broken tables abort the compile.

7. **Validate.** Local `metanorma compile -x html` green is the gate —
   fleet CI may be red for unrelated in-flight fixes, so report which
   gates passed and which workflow is red, never a bare color. Then run
   the XML and HTML checks: `scripts/validate_metanorma.py` performs
   the structural battery — fence balance, dangling cross-references,
   prose trapped in source blocks, and term-element counts. Validate
   the XML before waiting for PDF; PDF rendering is the slow step.
   After any bundle or toolchain change, regression-compile
   previously-green exemplars, and instrument schema (RNG) validation —
   compile-green does not prove schema-clean.

8. **Deliver.** Compile XML and HTML first; produce PDF once the XML and
   HTML checks pass. Re-run the full pipeline from the source on any
   correction — a fix applied only to the output is lost on the next
   run, and a manual workaround left in place duplicates what the
   pipeline later converts natively.

## The rules that decide success

- **Math: the block style selects the parser.** LaTeX formulas go in
  `[latexmath]` + `----` open blocks with no `\[ \]` delimiters inside.
  Bare `\[...\]` stem paragraphs and `[stem]++++` passthroughs parse as
  **asciimath** and fail plurimath with "Failed to parse … type
  `asciimath`"; `[$latexmath]` is a role, not a style — it does not
  select the parser. Re-encoding the content as genuine asciimath in a
  `[stem]` block is equally valid; the parser type must match the
  content syntax. See `references/encoding.md`.

- **Boilerplate is injected at compile time — never transcribe it.** The
  numbered foreword items (1)/2)/3)…), the terms-clause intro ("For the
  purposes of this document…" + Electropedia/ISO-OBP bullets), and the
  "There are no normative references in this document." sentence are
  generated by the flavor (metanorma-iec ships language-aware boilerplate;
  the rest comes from isodoc i18n). Their absence from the source is
  correct, and flagging that absence as content loss is a review error.
  See `references/encoding.md`.

- **Bilingual editions keep the English clause keyword.** Metanorma only
  recognizes clause semantics ("Normative references", foreword
  detection) from the English heading text; a French tree keeps the
  English "Normative references" heading and carries the French display
  via `[heading=…]` attributes where needed. Renaming it to "Références
  normatives" silently reclassifies the section as informative. See
  `references/encoding.md`.

- **Annexes are `[appendix]`, never `[annex]`.** The unknown `annex`
  style raises "annex sections do not support nested sections". Annexes
  support heading depth 3 and 4 only — convert deeper structures
  (test-purpose/test-method labels) to bold-label paragraphs.

- **Printed text is transcribed verbatim.** Printed typos are kept as
  printed — never repaired while transcribing; official-text oddities
  are facts of the edition, not transcription defects. Form variants
  between print locations (cover vs footer URN, contents page vs body
  numbering, recital vs cover title) are recorded verbatim in source
  comments as open questions for the publisher, never silently
  normalized; where numbering conflicts, the body numbering is encoded
  and the contents-page variant noted.

- **Document categories come from the publisher's catalogue.** Verify a
  document's category against the publisher's authoritative catalogue
  before encoding a doctype — a doctype invented from the document's
  shape misroutes every doctype-dependent branch (cover band colors,
  XSL routing, bibdata). The IALA catalogue, for instance, carries
  exactly five technical categories, and every registered doctype
  should be exercised by a real corpus document.

- **Update history is structured data, not prose.** Revision and
  approval tables are captured as structured records (per-section
  `updates.yaml`, or verbatim comments pending the corpus layout) that
  feed derived Record of Updates pages — a hand-built table is lost
  work the generator must duplicate. Capture the data even when no
  template renders it yet.

- **`imagesdir` is omitted** when body image paths already carry the
  `images/…` prefix — any `:imagesdir:` value double-prefixes the path
  and fails the build as FATAL "Image not found".

- **Fence balance is absolute.** An unpaired `----` turns the rest of the
  document into source code; interleaved example fences trap prose inside
  blocks; multi-record listings share one fence pair.

- **UML stereotypes use guillemets** («interface», «enumeration»), never
  double angle brackets — `<<interface>>` parses as a cross-reference
  macro and leaves dangling targets.

- **Cross-references resolve.** Every `<<target>>` must hit an existing
  anchor; the validator reports dangling targets. Self-references use
  anchors (`<<scope>>`), never hardcoded clause numbers; only other
  documents' clauses are cited by number.

- **Assert every rewrite.** Count replacements against the expected
  number; digit-count mistakes (`iso-19\d\d/` against `iso-19104/`) and
  invisible-detail defeats (trailing spaces, shifted capture groups)
  are silent no-ops that produce wrong output with no error.

- **Compile-clean is not publish-clean.** The site pipeline's mnconvert
  STS step rejects structures the compile accepts: bibliography-styled
  sections mid-body, preformatted content inside term entries, multiple
  level-0 titles. Validate against the STS output before delivery, and
  register only publish-clean documents in the site manifest. See
  `references/pitfalls.md`.

- **Transcribe the whole document.** Every section of the source appears
  in the output — transcribed, or flagged as out of scope before delivery.
  Unnumbered sections (forewords, appreciations, display boxes) are not
  optional.
