# Encoding reference

## Front matter

A transcribed document carries, as a minimum:

```adoc
= Document title
:title-intro-en: …
:docnumber: 19104
:edition: 1
:copyright-year: 2016
:revdate: 2016-10-01
:language: en
:doctype: international-standard
:docstage: 60
:docsubstage: 60
:technical-committee: …
:mn-output-extensions: xml,html,doc,pdf,rxl
:mn-document-class: iso
:data-uri-image:
:local-cache-only:
```

- `:mn-document-class:` selects the flavor; the compile fails with
  "Please specify a standard type" when it is missing. Never supply
  `-t <flavor>` on the command line — it masks the missing attribute.
- Doctypes not mapped by a taste pass through to the base flavor
  (`report` and `directive` work without a taste mapping).
- `:imagesdir:` is omitted when body image paths carry the `images/…`
  prefix; adding it double-prefixes and fails the build with
  FATAL "Image not found".
- `:local-cache-only:` avoids network access during validation.
- A provenance note goes in an AsciiDoc comment above the title
  (`// …`), not as visible body text.

## Headings

- Reconstruct hierarchy from the source's own table of contents when the
  body headings carry bookmark anchors instead of levels.
- Bookmark-wrapped lines are headings only when their text matches the
  bookmark's table-of-contents entry; conversion anchors tables, cells,
  figures and paragraphs the same way as headings.
- Annexes: `[appendix] == Title`. The bare `Annex X` letter line and the
  title line that follows collapse into one annex heading. Annex
  normativity (`(normative)` / `(informative)`) stays as a first
  paragraph.
- Annex depth caps at 4. ATS-style labels — test purpose, test method,
  reference, test type — become bold-label paragraphs
  (`*Test purpose:* …`), not headings.
- Document-title repeats on body pages are dropped; `Foreword`,
  `Introduction` (with `[.introduction]`) and `Bibliography`
  (with `[bibliography]`) are special clauses.
- Never hardcode the document's own clause numbers in headings or
  cross-references; Metanorma numbers them. Anchor and reference by
  `[[id]]` / `<<id>>`.

## Terms and definitions

The canonical entry form:

```adoc
[[term-designation]]
==== designation
alt:[admitted synonym]
deprecated:[discouraged form]

representation of a concept by a sign which denotes it

NOTE: Notes to entry are NOTE lines; Metanorma numbers them as
"Note 1 to entry" inside term clauses.

[example]
a single-paragraph example follows the [example] style directly

[example]
====
multi-paragraph examples use the open-block form
====

[.source]
ISO 1087-1, 3.4.1
```

- Term anchors are stable slugs: `[[term-<slug>]]`.
- The definition is the first paragraph of the term clause.
- Admitted and deprecated designations use `alt:` / `deprecated:`.
- Domain annotations (`<general vocabulary>`) lead the definition.
- Notes are `NOTE:` lines, one per note, prefix stripped.
- Examples: `[example]` + paragraph for single-paragraph examples;
  `[example]` + `====` open block for multi-paragraph ones. Body-level
  `EXAMPLE` lines outside term clauses convert as single-paragraph
  examples only — continuation blocks stay in the text flow.
- **Multi-record listings share one fence pair.** Listing several YAML
  records inside one `[source]` block uses a single `----` … `----`;
  a fence per record closes the block after the first record and the
  remaining records leak into the page as raw text, while a later
  stray fence swallows the following section as source code.
- A line whose first non-space character opens a bracket
  (` *[SOURCE: …]*`) parses as block attributes, not text — it
  renders as a phantom empty figure. Citations inside blocks are
  `[.source]`-styled paragraphs.
- Sources are `[.source]` blocks; the modification text follows the
  citation (`ISO 10241-1, 3.1.2, modified — …`).

### Concept mentions

Mentions of another term use the concept macro, not plain xrefs:

```adoc
part of a terminological data collection which contains the
terminological data {{<<term-terminological-data>>,terminological data}}
related to one concept {{<<term-concept>>,concept}}
```

- `{{<<anchor>>,term}}` renders the term italicized and linked.
- `{{<<anchor>>,term,rendered text}}` overrides the rendered form.
- Plain `(<<term-x>>)` parenthesized xrefs are not concept mentions;
  the XML must carry `<concept>` elements.
- The designations of converted entries (preferred vs admitted
  synonyms) can be recovered from the source PDF by font analysis:
  designations are the wholly-bold lines that follow the bold
  term-number line.

## Tables

- Normalize rows to the declared `[cols=]` count; a `[cols=",",]`
  empty spec derives the target from the first row.
- Count cells with the row-span markers in mind: `.2+|` and `2+|` open
  a cell; `|` after space or start opens a cell.
- Rows that follow a row-span row need one cell fewer; strip the
  trailing empty cell instead of padding into an over-full row
  ("dropping cells from incomplete row" aborts the build).
- Blank lines inside `|===` regions terminate cells — drop them.
- Table titles become block captions (`. Table title`) above the table,
  not headings.

## Inline cleanup

- Remove: bookmark wrappers (`[#bookmark12]##‌##…`), zero-width
  non-joiners, font-size role spans (`[.s12]#…#`), passthrough
  markers (`++…++`), entity escapes (`&#44;`), watermark lines
  (licence holder, download date, "All rights reserved", ICS and
  price lines), and page furniture.
- UML stereotypes become guillemets: `«interface»`, `«enumeration»`.
  Double angle brackets parse as cross-reference macros.
- List punctuation: multi-sentence list items keep their full stops;
  colon-fragment items end with `;`. The style checker reports both.
- Image dividers (height ≤ 10 px rules) are dropped; content figures
  stay.
