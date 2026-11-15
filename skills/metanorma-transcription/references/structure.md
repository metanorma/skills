# Target directory and repository structure

A transcription project is a repository that reproduces its output from
its sources. Two layouts converge in practice: the single-document
layout for one-off conversions, and the corpus layout for structured
publications — parts, language variants, amendment editions.

## Single-document layout

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

## Single-document conventions

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

## Corpus layout (structured publications)

Loose-leaf and multilingual publications (parts, language variants,
per-section amendment histories, editions) converge on a folder-per-unit
layout. The folder is the unit — a section or a part; `[lang].adoc`
files are its language variants; editions are git tags over the single
tree.

```
<repo>/
├── metanorma.yml            # manifest: part stitch documents per language,
│                            #   entries carry identifiers, not just paths
├── Gemfile + Gemfile.lock   # lock COMMITTED and refreshed
├── bin/                     # conversion tooling (per-corpus importers)
├── scripts/
│   ├── anchor-parity        # language variants carry identical anchors
│   ├── anchor-lint          # every section file carries its canonical anchor
│   └── edition-diff         # tag-to-tag semantic diff per section file
├── reference-docs/
│   ├── en/  fr/  es/        # published editions — ground truth per language
│   └── circulars/           # amendment circular letters (citation sources)
└── sources/
    ├── sections/
    │   ├── s0120-title-scope/
    │   │   ├── en.adoc      # one self-contained file per variant;
    │   │   │                #   the anchor inside is the authoritative identity
    │   │   ├── fr.adoc      # materializes at the EN anchor freeze;
    │   │   │                #   an absent file = untranslated (visible)
    │   │   ├── es.adoc
    │   │   ├── updates.yaml # this section's amendment record (language-
    │   │   │                #   independent), seeded from day one
    │   │   └── images/      # section-local figures, shared across variants
    │   └── …
    └── parts/
        └── part-a/
            ├── en.adoc      # stitch: front matter (edition, part identifier,
            │                #   amendment state) + include:: of section files
            ├── fr.adoc
            ├── es.adoc
            └── assets/      # part-shared figures
```

Conventions:

- **The anchor inside the file is authoritative**; the filename
  (section number + slug) is for ordering only. Anchors are
  edition-independent: cross-edition renumbering resolves through an
  alias registry maintained at edition boundaries, not by rewriting
  anchors.
- **Editions and amendment states are git tags** (`ed10`, `ed10-amd1`).
  Compile an edition by checking out its tag; change reports and
  loose-leaf replacement packets are tag-to-tag diffs per section file
  (`scripts/edition-diff`). Pre-git history is folded from the
  amendment records instead.
- **`updates.yaml` carries the amendment history** (affected unit by
  anchor, edition or event, promulgated/approved citations, note).
  Derived Record of Updates pages are generated from these records —
  never hand-built tables.
- **Part stitch documents carry front matter and `include::` lines
  only.** Includes reach outside the stitch document's directory, so
  the compile needs an explicit base-dir/include-dir (jail-reaching
  includes are supported).
- **Parity is `ls`**: a missing translation is a missing file in the
  folder; `scripts/anchor-parity` additionally asserts identical
  anchors across variants. Variants materialize only after the master
  language's anchor freeze.
- **Manifest entries carry identifiers** (edition, part, section,
  doctype, series), not just paths — the manifest is the machine-
  readable table of contents of the corpus.
- **`Gemfile.lock` is committed and refreshed.** A stale lock compiles
  an ancient toolchain in CI while local builds float forward; refresh
  and commit it with every toolchain change.
- **Every encoding PR commits the ground-truth documents it encoded
  from** (subject to the repository's licence for source
  redistribution — see the single-document sources-of-record rule).
- **Document sources are node-shaped**: self-contained, anchor-
  authoritative, identifier-carrying. A future projection engine
  stitches editions as queries over the same corpus with no rework;
  every rule above exists to keep that true.

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

## Verification gates

- **Local `metanorma compile -x html` green is the gate.** Fleet CI may
  be red for unrelated in-flight fixes; report which local gates passed
  and which workflow is red, never a bare "CI is red".
- **Instrument schema (RNG) validation.** Compile-green does not prove
  schema-clean; run the flavor's schema check explicitly.
- **Regression-compile previously-green exemplars** after any bundle or
  toolchain change — a dependency bump that breaks one document breaks
  others silently.
- **Visual checks are evidence-based.** Render the cover to PNG and
  compare against the published original (PDF transparency flattened to
  white first); grep the rendered HTML for wrong-organization strings;
  count palette hex values against the brand reference.
