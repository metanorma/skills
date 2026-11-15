# Flavor reference

Encoding work runs along two dimensions:

1. **Flavor-specific document practices** — how the organization
   structures its documents: clause conventions, title composition,
   forewords and prefaces, revision records, identifier handling.
   One section per flavor below.
2. **Object-type practices** — how each object type is encoded:
   number encoding, bibliographies, tables, the site manifest,
   section splitting, units, math. These are **flavor-independent** —
   one set of rules holds in every flavor; where a corpus genuinely
   deviates, the deviation is noted inline as an exception, never as
   a second set of rules.

The document's `:mn-document-class:` selects the flavor. Changing it
is a vocabulary migration, not a string replace.

## ISO

- Terms and definitions at clause 3, per the ISO/IEC directives;
  terms carry `[.source]` citations to ISO 10241-1 or IEV.
- Directive-style foreword; boilerplate (the numbered items, the
  terms intro, the "no normative references" sentence) is injected at
  compile time from isodoc i18n — never transcribed.
- `:docnumber:` plus `:partnumber:` as separate attributes; stage
  vocabulary via `:docstage:`/`:docsubstage:` (60/60 published).
- Numeric bracket citations in text (`[1]`, `[3]`) tied to the
  bibliography order.
- Annexes as `[appendix]` with obligation attributes.

## IEC

- Foreword boilerplate injected language-aware: the IEC flavor ships
  English and French boilerplate and selects by document language —
  the basis for bilingual `en/` + `fr/` trees.
- Clause detection keys on the English heading keyword ("Normative
  references"); non-English trees keep the English keyword and
  localize display via `[heading=…]` attributes.
- National adoptions encode prefaces as
  `[.preface,type=european-foreword,…]` /
  `[.preface,type=national-foreword,language=…,keeptitle=true]`,
  one section per language, with EN-adoption endorsement notes as
  tables ("Harmonized as EN …").
- `:library-ics:` is comma-separated; TC/SC decomposition into
  `:technical-committee-number:` and `:technical-committee:`.

## OIML

OIML's own publications compile through the dedicated `oiml` flavor
(`metanorma-oiml`) — distinct from the standards OIML references,
which encode through the IEC flavor.

- Identifiers carry the composed form explicitly:
  `:docidentifier: OIML R 7` alongside `:docnumber: 7`;
  `:doctype: international-recommendation` for R documents.
- The OIML X 999:2026 profile governs identifier schemes, document
  types, and languages — three normative constraints every OIML
  publication shall satisfy.
- Publications come in English and French editions.
- OIML STS is a taste output format, not the generic mnconvert path:
  `metanorma compile -t oiml -x oimlsts` produces OIML NISO STS XML
  validated against the OIML X 999 Clause 6 rules.

## IHO

- `:docnumber:` is PubID-parsed by the flavor: display-only strings
  park in a dummy attribute (`:docnumberx:`) rather than breaking the
  identifier mint.
- S-series guideline structures.
- The docidentifier cleanup crash on split docnumber/partnumber pairs
  (metanorma-iho#577) is worked around with a single glued docnumber
  plus a source comment until the flavor is fixed.

## NIST

- Special-publication structure with authority and abstract front
  matter.
- OSCAL YAML (with liquid templates) can emit control tables whose
  cross-references are generated (`<<{{ id }},{{ display }}>>`).
- XML attribute mentions in prose use the `_@href_` italic
  convention.

## BIPM

- JCGM guide conventions (`:doctype: jcgm-guide`).
- Titles and attribute values are plain text — a document title
  carries `0.9 mK`, not `stem:[0.9 "unitsml(mK)"]` (keep the stem
  form as a trailing comment if it matters).

## OGC

- A literal double hyphen in source text is preserved through a
  zero-width non-joiner entity (`Simulation-&#x200c;-Application`) —
  AsciiDoc would otherwise render it as an em dash.
- Unnumbered annex clauses carry `[%unnumbered]`.
- Inline math typed as italics plus subscripts (`_θ~1~_`) converts to
  `stem:[θ_1]`.

## IALA

- Doctype-catalogue discipline: the catalogue carries a fixed set of
  technical categories, and every registered doctype is exercised by
  a real corpus document.
- Verbatim transcription with form variants (cover vs footer URNs,
  running-header vs cover case) recorded as source comments — open
  questions for the publisher, never silently normalized.
- Amendment and revision records are structured data: per-section
  `updates.yaml` records (affected unit anchor, edition/event string,
  promulgated and approved citations, note) from which Record of
  Updates pages are generated.
- Identifier blocks come from the printed cover; where the
  organization's URN grammar exists
  (`urn:mrn:iala:pub:{docidentifier}:ed{edition}`), minting supersedes
  a hand-written `:urn:` fallback.
- Correspondence heads as unnumbered blank-titled sections; part
  dividers as level-1 clauses.

## IEEE

- Amendment documents encode change structure: `del:[…]`/`add:[…]`
  inline macros (never `[strike]#`/`[underline]#` passthroughs),
  `[change=modify,locality="clause=4.3"]` on amended clause headings,
  `[change=add,…,path="."]` plus `[appendix,obligation=informative]`
  for inserted annexes.
- Replacement figures resume base-document numbering via
  `autonumber:figure[N]`.
- Participants render from `item::` / `role:::` / `name:::` lines
  under `== Participants` (grouped `===` Working Group / Balloting
  Group / Standards Board) — the flavor generates
  Acknowledgements/Word-usage front matter itself, so it is deleted
  from the source.
- Metadata vocabulary is hyphenated, never underscored: bare
  `:docnumber: 987.6` (drafts carry `:draft:` + `:docstage: draft`),
  `:society:`/`:committee:`/`:working-group:`/`:balloting-group:`,
  bare `:isbn-pdf:`, `:updates-document-type:` mirroring the base
  document's type; drafts omit `:confirmed-date:`.
- Bibliography sections are never anchored.

## Other flavors (ietf, cc, itu, ribose, csa, pdfa, …)

- IETF validates `:intended-series:` values and requires a body
  clause even in stub corpora; `<CODE BEGINS>`/`<CODE ENDS>` markers
  are preserved in source blocks.
- `csd`→`cc` remaps `:technical-committee:`→`:committee:` +
  `:committee-type:` and `:docstage:`/`:docsubstage:`→`:status:`.
- Ribose drops deprecated attributes outright.
- PDF/A-style aggregate references use
  `[[[ISO_14289_all,hidden(ISO 14289 (all parts))]]]` for
  parts-unspecified citations.

## Object-type practices (flavor-independent)

One set of rules, applied in every flavor. Corpus deviations are
noted inline as exceptions.

### Number encoding

- Decimal comma or point as the document prints it — per SDO
  convention and per language variant (e.g. IEC French trees print
  decimal comma); never normalized across a corpus.

### Bibliography encoding

- Relaton anchor-only entries: `[[[anchor,id]]]` — the citation is
  fetched and rendered; display strings must equal the fetched
  metadata; never append `, _Title_` by hand.
- Canonical author-year anchors where the corpus uses them
  (`CIPM1989`), one reference per bibitem, duplicates disambiguated
  (`Pavese2003a`). *(Exception: BIPM corpora.)*
- Alternate-name footnotes live inside the cite label; aggregated
  (all-parts) references use `hidden()`.

### Tables

- Table-level options beat per-cell markers
  (`options="unnumbered,header"`); `h|` only where a table
  deliberately demonstrates cell-level header marking.
- Cell-spec order is span before alignment (`.2+^h|`, never
  `^.2+h|`); multi-row headers declare `headerrows=2` where
  supported; in-table footnotes use the `footnote:` machinery.

### Site manifest (metanorma.yml)

- One registration per edition; language tiers publish two documents
  from one directory; pending documents noted as comments with their
  blocking reason; register only publish-clean documents.

### Section splitting

- Clause-granularity files; annexes filed to the end (`aa-…`,
  `aza-…`), bibliography last (`b0-`/`az-`); conventions stay
  comparable across review waves.

### Units

- UnitsML strings for unitful values in math: `"unitsml(K)"`,
  `"unitsml(degC)"`, `stem:[0.5 "unitsml(K)"]` — upright and
  machine-readable. Plain text in titles and attribute values.

### Math (stem)

- Asciimath `[stem]` blocks by default; reserved function names
  wrapped (`rm(min)`); multi-word identifiers quoted
  (`"min-entropy" = …`).
- `[latexmath]` + `----` open blocks for LaTeX content, no `\[ \]`
  delimiters; `[[eq-<id>]]` anchors for numbered formulas instead of
  `\tag{}`.
