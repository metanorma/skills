# Encoding reference

## Front matter

A transcribed document carries, as a minimum:

```adoc
= Document title
:title-intro-en: …
:docnumber: 19104
:partnumber:
:edition: 1
:copyright-year: 2016
:published-date: 2016-10-01
:language: en
:doctype: international-standard
:docstage: 60
:docsubstage: 60
:technical-committee: …
:library-ics: 35.030, 03.040
:mn-output-extensions: xml,html,doc,pdf,rxl
:mn-document-class: iso
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
- Deprecated attributes are removed, not updated: `:data-uri-image:`,
  `:docfile:` are gone from the toolchain.
- Multi-part documents split the identifier: `:docnumber: 17021` plus
  `:partnumber: 1` — unless the flavor's docidentifier cleanup crashes
  on the split (metanorma-iho#577), in which case carry a single glued
  docnumber (`0103-1`) with a source comment until the flavor is
  fixed. Publication dates are full ISO dates when the source carries
  the day.
- `:library-ics:` is comma-separated (`35.030, 03.040`), never
  semicolon-separated.
- A non-default foreword (European foreword, national foreword) needs
  `[heading=foreword]` on its heading, or the flavor numbers it as a
  clause.
- Bare emails become `mailto:addr[]` — the trailing empty `[]` is
  required. Bare URLs become `link:url[]` with the full URL as target
  and the printed text as display:
  `link:https://www.iso.org/directives[www.iso.org/directives]`.
- Committee metadata decomposes: `:technical-committee-type:`,
  `:technical-committee-number:`, and the name-only
  `:technical-committee:` — never one combined value.
- Changing `:mn-document-class:` is a vocabulary remap, not a
  search-replace: each flavor owns its attribute set (`csd`→`cc`
  remaps `:technical-committee:`→`:committee:` + `:committee-type:`
  and `:docstage:`/`:docsubstage:`→`:status:`; IETF validates
  `:intended-series:` against `informational`/`full-standard`; IHO
  pubid-parses `:docnumber:`, so display-only strings park in a dummy
  attribute, e.g. `:docnumberx:`).
- Illustrative code blocks are `[source%unnumbered,xml]` — the style
  is `source[,lang]`; `[sourcecode,…]` is not a Metanorma style.
- A quote attribution containing commas is quoted in the attribute
  list: `[quote, The Ware Report, "Defense Science Board Task Force on
  Computer Security, 1970"]`.
- Edition lineage lives in attributes: `:replaces:` and
  `:updated-date:`; corrigendum statements ("This corrected version
  corrects…") are real content, transcribed.

### Identifiers, editions and URNs

The identifier block comes from the printed cover and the publisher's
catalogue, and every value is verified against print before encoding:

- The identifier-carrying attributes: `:doctype:`, `:series:`,
  `:docnumber:` (with the part glued in where the publisher numbers
  parts), `:edition:`, `:published-date:`, and the language attribute.
  `:docidentifier:` may be set explicitly where the flavor does not
  compose it.
- Doctypes come from the publisher's authoritative catalogue, never
  from the transcriber's taxonomy — a wrong doctype misroutes every
  doctype-dependent branch (cover band colors, XSL routing, bibdata).
  The IALA catalogue, for instance, carries exactly five technical
  categories, and every registered doctype should be exercised by a
  real corpus document.
- `:urn:` is written as a fallback attribute; minting through the
  publisher's pubid grammar supersedes it wherever a grammar exists.
- Verify a minted or hand-written URN against the forms printed on the
  cover and in the page footers. Printed spelling variants (cover
  `ed.1.0`, footer `Ed1.0`) are recorded verbatim in a source comment
  as open questions for the publisher — never silently normalized to
  the corpus convention without a note.
- Editions are typed values with varying printed forms (`Edition 1.0`,
  `Ed 1.0`, `4.10.0`). Take the edition from the cover/foreword, not
  from the identifier, and record the printed form.
- Do not split `:docnumber:` and `:partnumber:` while the flavor's
  docidentifier cleanup crashes on the pair (metanorma-iho#577): carry
  a single glued docnumber (`0103-1`) with a source comment until the
  flavor is fixed.

### Site-scale conventions

In a corpus that builds as one site, manifest registration, directory
slots, and artifact policy are corpus concerns — see the
metanorma-corpus skill (`references/site.md`). The per-document rule
that remains: the document compiles publish-clean before it is
registered.

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
- Annex normativity is an attribute, `[appendix,obligation=normative]` —
  `subtype=` is not the annex key.
- `{blank}` is a placeholder for genuinely untitled subclauses only;
  migrations that blanked real subclause titles must have them
  restored.
- Document-title repeats on body pages are dropped; `Foreword`,
  `Introduction` (with `[.introduction]`) and `Bibliography`
  (with `[bibliography]`) are special clauses.
- Never hardcode the document's own clause numbers in headings or
  cross-references; Metanorma numbers them. Anchor and reference by
  `[[id]]` / `<<id>>`.

## Verbatim transcription

The transcription records what the edition prints; it does not edit it.

- Printed typos are kept as printed — never repaired while
  transcribing. An official-text oddity (a missing conjunction, a
  broken cross-reference, a spaced hyphen) is a fact of the edition;
  repairs belong to a post-transcription editorial pass that is
  recorded and attributable.
- Form variants between print locations are recorded, not reconciled:
  cover vs footer URNs, recital vs cover titles, running-header vs
  cover case. Each variant lands verbatim in a source comment as an
  open question for the publisher.
- Where the contents page and the body disagree on numbering, the body
  numbering is encoded and the contents-page variant noted in a
  comment.
- Heading case follows the corpus convention (the common one is
  sentence-cased level-1 clauses with acronyms preserved); where a
  template renders typed lower case in capitals, the typed case of
  sub-clauses is kept as printed.
- Running headers, folios and template artifacts (`gnnnn` placeholder
  URNs, staged edition lines) are furniture and drop out; real data
  under them (the actual URN, the actual edition) is front matter.

## Amendment and revision records

Loose-leaf and amended publications carry their update history in
Record of Updates / Document Revision tables. Encode that history as
structured data, not as hand-built output:

- Per-section `updates.yaml` in the corpus layout; pending that
  layout, the table data captured verbatim as comments at the top of
  `document.adoc`. One record carries: affected unit (anchor),
  edition or event string, promulgated citation, approved citation
  (nullable — "t.b.a." is a state), note.
- Derived Record of Updates pages are generated from these records.
  A hand-encoded table duplicates work the generator must redo, and
  the data gates the flavor's revision-page template work even when
  no template renders it yet.
- Approval and recital pages (council decisions, adoption resolutions)
  are captured the same way — they are metadata the flavor's cover and
  revision templates will consume, not body prose to retype.
- Amendment rows cite units at sub-clause and lettered-item
  granularity (`A-202.1d`); compound and range citations are lists of
  references, not single values.

## Amendment encoding

Amended documents encode the change structure, not strikethrough
passthroughs:

- Deleted and inserted text uses the `del:[…]` / `add:[…]` inline
  macros — `[strike]#P#` and `[underline]#IEEE#` are passthrough
  leftovers, not change markup.
- Every amended clause carries change attributes on the heading:
  `[change=modify,locality="clause=4.3"]`; an inserted annex is
  `[change=add,locality="clause=B",path="."]` plus
  `[appendix,obligation=informative]`.
- A replacement figure resumes base-document numbering with
  `autonumber:figure[N]`, not a manual caption.
- Flavor-generated front matter is deleted from the source, never
  transcribed: IEEE supplies "Acknowledgements"/"Word usage" and the
  amendment editing-instructions note. Participants render from
  `item::` / `role:::` / `name:::` lines under
  `== Participants` (with `===` Working Group / Balloting Group /
  Standards Board groups), not from `{fullname_N}` attributes.
- IEEE metadata is hyphenated, never underscored: `:docnumber: 987.6`
  bare (no `P`, ™, or `/D2` — drafts carry `:draft: 2` with
  `:docstage: draft`), `:society:`/`:committee:`/`:working-group:`/
  `:balloting-group:`, `:isbn-pdf:` bare, `:updates-document-type:`
  mirroring the base document's type, and drafts omit
  `:confirmed-date:` (confirmation is post-approval re-review).
- Bibliography sections are never anchored — no `[[…]]` on norm-refs
  or bibliography headings.
- Table-level options beat per-cell markers:
  `options="unnumbered,header"` on the table, `h|` only where a table
  deliberately demonstrates cell-level header marking.
- Consecutive `include::` lines are separated by blank lines.

## Cross-references and localities

- Multi-locality references chain full locality tokens with `;and!` /
  `;to!` — never quoted locality lists:
  `<<gum6,clause=5.1;and!clause=5.3;and!clause=5.8>>`,
  `<<scls-7-5-1;to!scls-7-5-4>>`, ranges of clauses
  `<<cls-5;to!cls-10>>`.
- External-document xrefs carry locality parameters the same way:
  `<<iso19011,clause=4>>`, `<<iso17000_2004,clause=5.2,note=1>>`,
  `<<iso_iec_17021_1_2015,annex=A>>`.
- Term-source citations use `locality:definition=`:
  `<<iso17000,locality:definition="5.3">>`.
- Notes referenced from prose get their own anchors: `[[note-7-1-2]]`
  on the note, `See <<note-7-1-2>>` in the text. List items are
  anchorable too (`<<scls-9-5-1-2-b>>`).
- `<<ref15, fn>>` renders the reference as a footnote.
- `<<annex-a,style=full%>>` renders number plus title.
- Prose mentions of clauses, annexes and tables become anchored xrefs —
  add `[[cls-4]]` / `[[annex-a]]` / `[[table-b-1]]` and reference them;
  an intro list of annexes becomes `* <<annex-a>>: description`.
- Plain-language citations of other documents ("ISO 19011:2011, Clause
  4.") are converted, not left as text.
- Citation labels must carry the true document stage and publisher
  (`ISO/IEC TS 17021-2`, not `ISO/IEC 17021-2`; `IEC 31010`, not
  `ISO 31010`).
- Reviewer annotations (when the corpus records review positions) use
  paired inline anchors plus an empty styled block:
  `[[review_1s]]…[[review_1f]]` in the text and
  `[reviewer=C1,from=review_1s,to=review_1f,type=corrigenda]` on an
  empty open block.

## Auto-injected boilerplate

The pipeline generates standard furniture at compile time. Never
transcribe it, and never "restore" it in review:

- The foreword's numbered items (1) The formal decisions…, 2) They have
  the form…, 3) In order to promote…) — the IEC flavor ships
  `boilerplate-en.adoc` / `boilerplate-fr.adoc` and selects by document
  language.
- The terms-clause intro ("For the purposes of this document, the
  following terms and definitions apply." plus the Electropedia /
  ISO Online Browsing Platform bullets) — isodoc i18n.
- "There are no normative references in this document." — injected when
  clause 2 carries no bibitems; the source keeps the (empty) clause.
- Presentation-time clause titles: an `Abbreviations` subclause
  compiles to `<definitions type="abbreviated_terms">` with no title
  element, and normative-references sections compile to `<references>`
  whose title the renderer generates. Their presence in the compiled
  XML is the proof of presence; source-side title comparisons must
  exempt them.

A source-tree review that flags these absences as content loss wastes a
review cycle every time.

## Bilingual editions

- A source PDF may be bilingual (IEC/EN adoptions frequently carry an
  English and a French side in one file). Check the OCR text for French
  before deciding there is no French ground truth — the French side of
  the same PDF is authoritative for the `fr/` tree.
- Multilingual trees live side by side:
  `sources/<family>/<year>/en/…` and `…/fr/…`, file-for-file mirrors.
  Figures are extracted per language (labels differ between the two
  sides of the PDF); in the corpus layout, section-local `images/`
  directories are shared across variants instead of duplicated.
- **Language variants carry identical anchors.** The anchor set is
  frozen on the master language at the anchor freeze; `fr`/`es` files
  mirror it exactly, and `scripts/anchor-parity` asserts the identity.
  The numbering system is identical across language editions of a
  publication — anchors are how a clause is cited across languages.
- The `fr` tree keeps the English clause keyword "Normative references"
  so the flavor's clause detection fires; French display headings use
  `[heading=…]` attributes where the rendered text must differ.
- Both trees register in the site manifest; a tree that is not
  registered will not build or publish.
- National-adoption prefaces carry preface roles, not plain headings:
  `[.preface,type=european-foreword,heading=foreword,keeptitle=true]`
  on the body, and per-language national forewords as
  `[.preface,type=national-foreword,language=et,heading=foreword,
  keeptitle=true]` — each language's foreword in its own section.

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
- Sources are `[.source]` blocks; the citation targets a bibliography
  anchor with the right locality form —
  `<<iso17000,locality:definition="5.3">>` for definitions,
  `<<IEC_60050_161_1990,clause=161-01-20>>` for clauses — not a bare
  string.
- Whether the modification marker ("modified — …") is kept is a
  per-corpus editorial decision: corpora differ (some keep it, some
  strip it and carry only the modification text). Match the corpus
  before editing; do not "fix" either direction across corpora.
- A bibitem cited from a term source must be a real, visible entry —
  not `[[[anchor,hidden(X)]]]` — and the term source's anchor must
  match the bibitem anchor exactly (year-less where the bibliography
  entry is year-less).
- Bibitem list items carry only the `[[[anchor,id]]]` anchor: relaton
  fetches and renders the citation — never append `, _Title_` by hand.
  The display string in the anchor must equal what the fetch returns
  (`ISO/IEC 15408-1`, not `ISO 15408-1`; `IETF RFC 4949`, not
  `IETF 4949`) — it overrides the fetched metadata.
- Anchor ids follow the corpus convention — canonical author-year
  forms (`CIPM1989`, `Hill2003`), one reference per bibitem,
  duplicates disambiguated (`Pavese2003a`); non-ISO entries keep their
  display id (`W3C did-resolution-1.0`).
- An alternate-name footnote lives inside the cite label:
  `[[[ref,(ISO/IEC Guide 99:2007 footnote:[Also known as JCGM
  200])ISO/IEC Guide 99:2007]]]` — not fake superscripts after the
  entry.
- Adapted terms from multilingual sources designate per language with
  the `lang:` role, not quoting roles: `=== lang:en[paddy]
  lang:fr[paddy]`.
- An admitted synonym under the term heading is an `alt:[…]` line as
  the first line of the entry — no blank line between heading and
  `alt:`; an equally-abbreviation-bearing term uses
  `preferred:[…]` (`alt:` is only for admitted alternates), and the
  abbreviation class is metadata inside the term:
  `[%metadata]` + `abbreviation-type:: initialism`.
- A terms clause that imports all its terms carries the sources on the
  heading — `[source=iso17000]` or the multi-source form
  `[source="ISO_IEC_Guide_99_2007,ISO_IEC_17000_2004"]` — with no
  transcribed intro; each terms-group heading
  (`== Terms related to …`) keeps `[heading=terms and definitions]`.
- Adaptation is marked on the source block, never inside the locality:
  `[.source%adapted]` + `<<ISO_15026_1>>`, not `<<ISO_15026_1,Adapted>>`.
- Hanging paragraphs that print as sub-clauses get
  `[[scls-X-Y-Z]]` + `==== {blank}` at depth (dots + 2) — never
  `[.subclause="X.Y.Z"]` attributes, never invented titles; the
  converse holds too: a `{blank}`-headed paragraph-clause that prints a
  title gets that title restored.
- Identical stems in definition-list terms derive identical ids — give
  them explicit distinct anchors.

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
- No manual parentheses around a mention — `({{process}})` becomes
  `{{process}}`; the clause number is never hand-written —
  `{{proficiency testing item}} (3.8)` drops the `(3.8)`.
- Plural/inflected forms pass the rendered text:
  `{{participant,participants}}`, `{{policy, policies}}` — the plural
  goes inside the braces, never `{{X}}s`.
- Option control matches the print: `{{term,options="noref,noital"}}`
  for mentions in note/example prose of vocabulary documents (plain,
  unlinked), `{{term,options="ref"}}` for the "new terms" foreword list
  (auto clause number), `{{term,options="noref"}}` with a rendered form
  for grammatical variants (`{{suspension,suspend,options="noref"}}`,
  `{{approval,Approval,options="noref"}}`). Do not over-apply
  `noref` to ordinary standards' mentions, and never use `<<…>>` for a
  concept mention.
- The designations of converted entries (preferred vs admitted
  synonyms) can be recovered from the source PDF by font analysis:
  designations are the wholly-bold lines that follow the bold
  term-number line.

## Math

The block style attribute selects which parser (plurimath) sees the
content — mismatches are the most expensive math failure class because
they surface only at compile time, after everything else is clean:

```adoc
[latexmath]
----
I(t) = \frac{I_1}{k_1} \times \exp\left(\frac{-t}{\tau_2}\right)
----
```

- LaTeX content MUST use the `[latexmath]` + `----` open-block form,
  with no `\[ \]` delimiters inside the block. The delimiters are stem
  -paragraph syntax, not part of the formula.
- Bare `\[ ... \]` stem paragraphs and `[stem]` / `++++` passthrough
  blocks containing LaTeX commands parse as **asciimath** and fail with
  "Malformed MathML: [plurimath] Failed to parse … type `asciimath`".
- `[$latexmath]` sets a role, not the block style — it does not select
  the parser. `[latexmath]` (no `$`) does.
- The reverse direction is legitimate: re-encoding the content as
  genuine asciimath inside `[stem]` blocks works and matches the
  corpus-wide default. The requirement is parser-content agreement, not
  a specific dialect.
- Asciimath reserves function names — `min` must be written
  `rm(min)`, and multi-word identifiers are quoted:
  `"min-entropy" = -log_2 (p)`.
- Units in math are UnitsML strings, upright and machine-readable:
  `stem:[0.5 "unitsml(K)"]`, `"unitsml(degC)"` — not `" rm(K)"` or
  literal `°C`.
- Titles and attribute values are plain text: a document title carries
  `0.9 mK`, not `stem:[0.9 "unitsml(mK)"]` (keep the stem form as a
  trailing comment if it matters).
- Formula numbering: give numbered formulas `[[eq-<id>]]` anchors above
  the block and reference with `<<eq-<id>>>`; do not put `\tag{}` inside
  the formula body.
- Only the compile reveals a parser mismatch — there is no reliable
  source-side static check. Run the compile before declaring math done;
  grep the log for "Failed to parse".
- A single failing formula aborts the whole document with FATAL
  ERRORS listing only the first few failures; convert every formula,
  not just the ones in the log.

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
  not headings — numbering is automatic, so no manual "Table 1 — " in
  the caption.
- **Two-level grouped headers do not survive `options="header"`.**
  Metanorma emits a single-row `<thead>`, and a row-span crossing the
  thead/tbody boundary fails validation ("rows cannot go outside
  thead/tbody"). Keep the grouped header rows in tbody with `.2+`
  row-spans and bold cells; the semantics survive even though the
  printed two-row header becomes one header row plus a styled row.
- Span specs and cell markers interact: `.2+|` opens a cell with a
  row-span, but a span spec following a stray `|` silently creates an
  empty cell. Re-count cells per row after any span edit.
- Merged cells, stacked ranges (`+` line breaks inside one cell) and
  superscript ranges (bit numbers, scale bands) need explicit spans —
  encode the print's merge structure, not its visual approximation,
  and verify the rendered table against the print row by row.
- Multi-row headers declare `options="header",headerrows=2` where the
  flavor supports it; otherwise keep grouped header rows in tbody with
  bold cells (see the grouped-header rule above).
- Footnotes inside tables use the `footnote:` machinery, not text:
  `footnote:a[…text…]` defined under the spanned header cell,
  referenced as `| 1 footnote:a[]` in cells.
- Paired correspondence rows are joined into one physical row with all
  cells present — asciidoctor silently DROPS incomplete rows, and a
  short pair-half lands its cells in the wrong columns with no error.

## Figures

- Figures and tables are captioned or unnumbered **per the printed
  document**, even when the flavor numbers them by default. Style
  warnings about untitled figures reflect Metanorma's default
  expectation, not the source's practice — leave genuinely unnumbered
  print figures uncaptioned.
- Legends and caption boxes are real content (paragraphs, tables), not
  part of the image — other language editions translate them.
- Word-sourced figures arrive with the caption paragraph after the
  image; Metanorma wants `. Caption` above the block. Move it up and
  strip printed "Figure N" prefixes where the flavor renumbers.
- Keep original image filenames from the source (Word `word/media`
  names, PDF object names) unless the corpus convention says otherwise;
  renumbering images breaks the mapping back to the source.
- Word-sourced figure keys (shape-glyph legends) are
  `[%unnumbered,cols="a,a"]` tables with `image::` cells; key entries
  drop trailing punctuation and match print case.
- A figure whose asset is not yet extracted gets a `// TODO` comment
  with the PDF page and OCR bounding box — never a placeholder image.
- A printed "Source: …" tail inside a figure/table caption moves out of
  the caption into a `[type="source"]` `[NOTE]` block below.

## Lists

- Source lettered items (`a) … b) …`) become arabic auto-lists (`.`
  items) — the letters are never hand-written, and continuation lines
  are dedented (flush with the item text).
- Sub-items nest with `..`; an intro item with a bold lead becomes
  `. *Term*: definition` with `..` children.
- Source bullet glyphs (—, •) are list markers, not text: `— EN
  18239…` becomes `* EN 18239…`.
- A lettered sequence interrupted by prose resumes with `[start=2]`,
  `[start=4]` — the printed letters are preserved without hand-writing
  them.
- Warnings follow the note family: `*WARNING 1* — text` becomes a
  plain `WARNING:` admonition; no hand-written numbers.
- An intentionally empty list item is `. {blank}`.
- Footnote-style citations ("HTTPfootnote:[RFC 7540, …]") become
  bibliography xrefs: a bibitem plus `HTTP <<RFC7540>>`.
- `****` is an example-block delimiter — text wrapped in it renders as
  a visible example and can suppress the following heading. Meta-notes
  (licence notices, encoding remarks) are `//` comments.
- A two-column bilingual foreword (national-language | English) is an
  `[%unnumbered,cols="<.<50,<.<50",options="header"]` table.

## Inline cleanup

- Remove: bookmark wrappers (`[#bookmark12]##‌##…`), zero-width
  non-joiners, font-size role spans (`[.s12]#…#`), passthrough
  markers (`++…++`), entity escapes (`&#44;`), watermark lines
  (licence holder, download date, "All rights reserved", ICS and
  price lines), and page furniture.
- UML stereotypes become guillemets: `«interface»`, `«enumeration»`.
  Double angle brackets parse as cross-reference macros.
- The source is ASCII-only unless the language requires otherwise:
  typographic quotes (“…”), curly apostrophes (’) and accents absent
  from the source are normalized (`organization's`, `"technical
  area"`).
- Dashes: attribute values and titles use `--`; parenthetical en-dash
  asides in prose become `-- such as this --`. To preserve a literal
  double hyphen from the source, insert a zero-width
  non-joiner entity (`Simulation-&#x200c;-Application`).
- Names and document-series titles mentioned in forewords are
  italicized per the source (“ISO _Conformity Assessment_ Committee”,
  series titles, each “_Part N: …_”).
- Inline math typed as italics + subscripts (`_θ~1~_`) becomes
  `stem:[θ_1]`.
- Unnumbered annex clauses carry `[%unnumbered]`.
- List punctuation: multi-sentence list items keep their full stops;
  colon-fragment items end with `;`. The style checker reports both.
- Image dividers (height ≤ 10 px rules) are dropped; content figures
  stay.
