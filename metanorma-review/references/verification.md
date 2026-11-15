# Verification battery

Three layers, run in order. Each layer has a failure class the previous
one cannot see.

## Layer 1 — mechanical (source-side, fast)

- Scope: `git diff -M --name-status origin/main...origin/<branch>` —
  one document family per PR; renames R100; no cache, secret, or
  artifact files (`document.sts.xml`, `document.pdf.fo.xml`,
  `document.xml.abort`, `document.doc/pdf/html`).
- Site manifest consistency: every registered path resolves on the
  branch, no duplicate entries, entry count change accounted for
  (relocation = replace; new language = add; new edition = add).
- AsciiDoc integrity: balanced open blocks (`--`) and table delimiters
  (`|===`); anchors `[[…]]` resolve against xrefs `<<…>>` both ways;
  `image::` references ↔ files in `images/` 1:1.
- Structural inventory: section-file lists old vs new — every old
  section has a counterpart or an accounted rename; heading counts do
  not silently shrink (a shrink needs a stated reason; a growth is a
  coverage gain to verify).
- Encoding: no mojibake, no leaked model-refusal text, no markdown
  fences, no duplicate level-0 titles.

## Layer 2 — ground truth (source-of-record, decisive)

- Clause coverage: the PDF's contents page (or OCR headings) vs the
  encode's section list — every printed clause/annex/bibliography
  entry present.
- Numeric spot-checks: 5-9 substantive hunks per PR against
  `pdftotext` output — test levels, severities, durations, tolerances,
  table rows. Corrections must match the print exactly, including
  decimal-comma conventions.
- Meaning-change watchlist: shall/should/may swaps, units changed,
  rows added or dropped, sentences absent from the source (checking a
  suspicious sentence exists in BOTH OCR and pdftotext before calling
  it a fabrication).
- Bilingual check: grep the PDF text for the other language before
  declaring the language tree unverifiable.

## Layer 3 — pipeline gates (compile + publish)

- Compile: `metanorma compile -x xml,html` (no `-t` flag) — zero
  FATAL, zero plurimath "Failed to parse", zero asciidoctor ERRORs.
  Non-fatal warning signatures are compared against the pre-PR state:
  a pass that FIXES a warning class is a credit.
- Completeness gate: source clause-level titles (plus term names)
  against compiled-XML titles and `term/preferred/name` elements,
  unicode/entity-normalized; presentation-generated titles
  (`<definitions type="abbreviated_terms">`, `<references>` sections)
  are exempted by element presence.
- Publish: mnconvert STS output validates — compile-clean is not
  publish-clean. In CI this runs on every PR; locally, only the
  structural pre-checks are available, so CI is the STS verdict.
- The pre-existing warning classes that are known non-fatal on main
  (e.g. one legacy encode's bibliography-nesting notices) are not
  failures — compare signatures, do not demand zero.

## What each layer uniquely catches

| Layer | Catches what the others miss |
|---|---|
| Mechanical | scope creep, artifact commits, broken syntax, dangling refs |
| Ground truth | fabricated or dropped content, meaning changes, wrong values |
| Pipeline | parser-type math failures, termbase/preformat STS rejections, mid-body bibliography rejections |

## Verdicts

- **approve-quality** — all layers pass; remaining notes are cosmetic
  and non-blocking.
- **concerns** — specific findings to fix before merge; each ships as
  a fix-up commit or is waived by the owner with a reason.
- **problem** — content loss, fabrication, or meaning change; merge
  blocked until resolved.
