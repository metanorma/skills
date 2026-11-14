---
name: metanorma-transcription
description: Transcribe standards documents (ISO-style PDFs, HTML exports, legacy machine conversions) into publication-grade Metanorma AsciiDoc, and validate the result compiles and renders correctly. Use when converting a standards document to Metanorma, repairing a converted document's structure, encoding terminological entries, or diagnosing why a Metanorma document renders text as source code.
---

# Transcribing documents into Metanorma

Transcribe a source document into Metanorma AsciiDoc that compiles clean,
renders correctly, and preserves every section of the source. The workflow
is: intake, front matter, structure, terms, furniture, tables, validation.
The reference files carry the details; this file carries the rules that
decide success or failure.

## The workflow

1. **Intake.** Identify the source: a PDF, an HTML export, or an existing
   machine conversion (pandoc-class dumps with bookmark cruft, page
   furniture, pasted covers). Keep the source files untouched and present
   — they are the source of record. Note the provenance in an AsciiDoc
   comment above the document title. Never delete a source file.

2. **Front matter.** Every document carries the flavor attribute
   (`:mn-document-class:`) — the compile resolves the flavor from it, and
   a missing attribute is the most common CI failure. See
   `references/encoding.md` for the attribute set, doctype mapping, and
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

7. **Validate.** Run the compile without a `-t` flag (a flag masks a
   missing flavor attribute), then run the XML and HTML checks:
   `scripts/validate_metanorma.py` performs the structural battery —
   fence balance, dangling cross-references, prose trapped in source
   blocks, and term-element counts. Validate the XML before waiting for
   PDF; PDF rendering is the slow step.

8. **Deliver.** Compile XML and HTML first; produce PDF once the XML and
   HTML checks pass. Re-run the full pipeline from the source on any
   correction — a fix applied only to the output is lost on the next run.

## The rules that decide success

- **Annexes are `[appendix]`, never `[annex]`.** The unknown `annex`
  style raises "annex sections do not support nested sections". Annexes
  support heading depth 3 and 4 only — convert deeper structures
  (test-purpose/test-method labels) to bold-label paragraphs.

- **`imagesdir` is omitted** when body image paths already carry the
  `images/…` prefix — any `:imagesdir:` value double-prefixes the path
  and fails the build as FATAL "Image not found".

- **Fence balance is absolute.** An unpaired `----` turns the rest of the
  document into source code; interleaved example fences trap prose inside
  blocks. Convert display-box delimiters deliberately (`[example]` +
  `====` … `====`), and keep body-level examples single-paragraph.

- **UML stereotypes use guillemets** («interface», «enumeration»), never
  double angle brackets — `<<interface>>` parses as a cross-reference
  macro and leaves dangling targets.

- **Cross-references resolve.** Every `<<target>>` must hit an existing
  anchor; the validator reports dangling targets. Self-references use
  anchors (`<<scope>>`), never hardcoded clause numbers; only other
  documents' clauses are cited by number.

- **Transcribe the whole document.** Every section of the source appears
  in the output — transcribed, or flagged as out of scope before delivery.
  Unnumbered sections (forewords, appreciations, display boxes) are not
  optional.
