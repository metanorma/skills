# Target directory and repository structure

A transcription project is a repository that reproduces its output from
its sources. The layout below is what converges in practice.

## Repository layout

```
<repo>/
├── README.adoc              # provenance, contents, quality notes, build
├── LICENSE                  # (public repos)
├── NOTICE                   # third-party content statement, if needed
├── metanorma.yml            # collection manifest: lists every document.adoc
├── Gemfile                  # metanorma toolchain (metanorma-cli, flavor gems)
├── .gitignore               # build artifacts (see below)
├── reference-docs/          # SOURCE OF RECORD — original PDFs/HTML exports
│   ├── <doc>.pdf
│   └── …
├── sources/
│   └── <doc-slug>/          # one directory per document
│       ├── document.adoc    # front matter + includes (or monolithic)
│       ├── sections/        # section files, split at clause granularity
│       │   ├── 00-foreword.adoc
│       │   ├── 01-scope.adoc
│       │   ├── 03-terms.adoc
│       │   ├── 04-….adoc
│       │   ├── aa-annex-a.adoc
│       │   └── az-bibliography.adoc
│       └── images/          # per-document images, referenced relative
│           └── Image_001.png
└── tools/                   # the transcription pipeline, committed
    ├── extract-designations.py
    └── rebuild.py
```

## Conventions

- **One directory per document**, named by slug (`iso-19104`,
  `enosema-entry-quality`). The document's `document.adoc` is the compile
  unit; `metanorma.yml` lists exactly that path per document.
- **Images live beside the document** (`sources/<slug>/images/`), and
  body paths are relative to `document.adoc` (`images/Image_001.png`).
  Do NOT set `:imagesdir:` for this layout — relative paths already
  resolve, and imagesdir double-prefixes them.
- **Sections split at clause granularity** for anything longer than a
  few hundred lines; `document.adoc` carries the front matter and
  `include::` lines only. Annex files sort to the end (`aa-…`,
  `ab-…`), the bibliography last (`az-bibliography.adoc`).
- **Sources of record are committed** for private transcription repos
  (copyrighted source PDFs stay in private repositories); public repos
  reference the sources and commit only the transcription.
- **tools/ is committed** — the pipeline is part of the record. A fix
  applied to generated output without a pipeline change is lost on the
  next rerun; every correction lands in the pipeline, then the pipeline
  reruns from `reference-docs/`.
- **The pipeline reads from the sources of record**, never from HEAD:
  rerunning against already-transcribed output fails (the cover
  headings it anchors on are gone) or worse, double-applies. Restore
  originals before rerunning; pin the commit or path that holds them.

## .gitignore for build artifacts

```
sources/**/document.xml
sources/**/document.presentation.xml
sources/**/document.html
sources/**/document.err.html
sources/**/document.rxl
sources/**/document.doc
sources/**/document.pdf
sources/**/*.asciidoc.log.txt
relaton/
.cache/
```

Compiled artifacts are reproducible; never commit them.

## Build

```sh
bundle install
bundle exec metanorma compile -x xml,html sources/<doc-slug>/document.adoc
```

No `-t`/`--type` flag — the flavor resolves from `:mn-document-class:`
in the document, and a local flag would mask a missing attribute until
CI fails.
