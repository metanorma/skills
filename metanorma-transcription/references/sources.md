# Sources: PDF vs HTML

A standards document reaches transcription through two kinds of source,
and they fail differently. Use both when both exist.

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
- font-spec inspection before writing rules — dump one page of XML and
  read the actual `<fontspec>`/`<b>`/`<i>` patterns rather than guessing.

## The hybrid workflow (recommended)

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

## Rules that hold for either source

- Keep the source files untouched and present; the pipeline reruns
  from them.
- Sample before scripting: dump real regions of the source (raw lines
  or XML) and read them — conversion artifacts differ per document and
  per extraction run.
- Assert every rewrite: count replacements and compare against the
  expected count; a regex that never matches is a silent no-op
  (digit-count mistakes are the classic — `iso-19\d\d/` never matches
  `iso-19104/`).
