# Sources: Word, PDF, HTML

A standards document reaches transcription through three kinds of
source, and they fail differently. Preference order: the publisher's
Word file when it exists; otherwise the PDF, transcribed by hand; HTML
exports support or replace the PDF route where structure is available.
Use every source that exists — each carries what the others lack.

## Word (.docx) — preferred when available

Word is the publisher's own structure: named styles carry heading
levels, list types, caption and reference styles, so conversion is
mechanical where the styles are mapped.

Conversion is a **style-map importer, and style-map importers are
per-corpus**: the map keys on the publisher's template style names,
which differ per secretariat (the IALA map keys on the secretariat's
French and English style names — Titre/Heading levels, Abbreviations,
Figurecaption/Tablecaption with French variants, Reference/Furtherreading,
Bullet). A map built for one publisher's template does not transfer.

- **Prove the map by round trip.** Run the importer on a document of
  the same family that was already hand-encoded and require
  byte-identical output (compile artifacts excluded) before converting
  anything new. A round-trip-clean importer turns future documents of
  that family into a review task instead of a transcription task.
- **Limits that stay manual:**
  - Direct-formatted lists (no named style) fall out as plain
    paragraphs — restore the bullets and ordered runs.
  - Revision tables are skipped by design. Capture their data
    manually; it feeds the derived Record of Updates.
  - Each new document family brings styles outside the map — extend
    the map per family when that family's exemplar arrives.
- **Do not substitute a generic converter for the corpus importer.**
  A generic docx converter carries no corpus style map, and its CLI
  may be broken in ways the library API is not; the corpus importer is
  the verified path.

Front matter (doctype, edition, published date, URN, approval body)
usually survives the conversion only as cover text — mine it from the
cover and revision table, then write the attribute block by hand; the
converter cannot know flavor attributes. Discard the Word TOC field,
list-of-figures text, cover tables and pasted furniture before
encoding.

## Word saved as HTML — the fallback route

When direct Word import is unavailable (unmapped styles, no importer
for the family yet), save the Word file as HTML and run the HTML route:
extract with the HTML tooling, verify the text against the Word or PDF
original, and treat the result as a skeleton for the manual pass, not
as finished encoding.

## HTML exports (of a PDF)

What they carry:

- pre-extracted text with reading order already applied;
- navigation anchors — PDF bookmarks surface as `#bookmarkN` links, and
  the table of contents gives the full heading map with levels;
- inline formatting partially preserved, often as font-size role spans
  (`[.s12]#…#`) rather than semantic markup;
- tables pre-converted (usually with `[cols=]` specs, often ragged);
- exported assets in `*_files/` directories;
- pasted covers, licence watermarks, "Licensed to"/"Downloaded" stamps
  as plain text blocks.

What they lose or corrupt:

- typography — bold designations, admitted-synonym distinction and
  superscripts degrade into plain or role-spanned text; designations of
  one entry merge onto one line;
- diagrams — vector text scatters as garbage lines around the real
  figure images;
- font-size-based heading levels (the export may flatten them).

HTML is the structure skeleton: build the heading hierarchy from its
bookmarks and table of contents, take its tables, and clean its
furniture. Verify nothing was dropped: check entries whose numbering
is wrapped in cruft (`[#bookmark12]##‌##4.37[#bookmark13]##‌##…`) before
concluding content is missing — wrapped numbering hides entries from
naive line matching.

## PDFs

What they carry:

- authoritative typography — font runs distinguish bold preferred
  designations from admitted synonyms, italics from plain text;
- layout information — `pdftotext -layout` preserves reading order and
  column structure; `pdftohtml -xml` yields per-line font runs;
- the terms and definitions clause with correct designation separation.

What they lack:

- structure — heading levels, clause nesting and table cell boundaries
  must be reconstructed from fonts, sizes and layout, not read off.

PDF is the typographic truth. The reliable extraction tools:

- `pdftotext -layout` — reading-order text, clause-number and
  designation discovery;
- `pdftohtml -xml -stdout` — per-line font runs; group lines by
  vertical position, classify runs as bold/italic, and recover
  designation lists (the wholly-bold lines that follow a bold
  term-number line), including multi-designation entries the HTML
  export merged;
- pymupdf — programmatic text extraction and embedded-image recovery
  (`get_images`) for figure objects the text tools cannot address;
- font-spec inspection before writing rules — dump one page of XML and
  read the actual `<fontspec>`/`<b>`/`<i>` patterns rather than guessing.

### Renders and figures

- ImageMagick renders (`magick -density 100 page.pdf[N]`) serve layout
  and visual checks. **Flatten transparency to white first** —
  transparent backgrounds rasterize black, and a black render is an
  artifact of the rasterizer, not evidence about the document.
- Figures: extract embedded images where they exist as objects; crop
  from high-density renders (200 dpi) where they do not (vector art,
  scanned plates). Crop figures cleanly out of surrounding legends.
- Legends and caption boxes under figures are transcribed as real
  content (paragraphs, tables), never baked into the bitmap — other
  language editions translate them.
- Double-page spreads: de-spread per page before transcribing; each
  printed page is one encoded page.

## The hybrid workflow (HTML + PDF)

1. Skeleton from the HTML export: headings from the bookmark map, body
   text, tables, images.
2. Truth from the PDF: designation lists per term number, formatting
   classes, anything the export merged or flattened. Cross-check each
   designation list against the merged line in the HTML conversion
   (the joined PDF designations should equal the merged line modulo
   whitespace); fall back to the merged line when extraction misses an
   entry, and record the fallback.
3. Character PDFs (scanned or broken encodings) may yield nothing to
   pdftotext — treat them as image sources only, and keep the HTML
   export as the text authority.

## Rules that hold for any source

- Keep the source files untouched and present; the pipeline reruns
  from them.
- Sample before scripting: dump real regions of the source (raw lines
  or XML) and read them — conversion artifacts differ per document and
  per extraction run.
- Assert every rewrite: count replacements and compare against the
  expected count; a regex that never matches is a silent no-op
  (digit-count mistakes are the classic — `iso-19\d\d/` never matches
  `iso-19104/`).
- Printed typos are transcribed verbatim — never fixed while
  transcribing. A repair is a post-transcription editorial decision,
  recorded and attributable, not a silent change in the encoding.
