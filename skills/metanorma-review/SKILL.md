---
name: metanorma-review
description: Review, correct, and validate existing Metanorma transcriptions against their source documents (PDFs, OCR exports, HTML ground truth). Use when editorially reviewing an AI-migrated or machine-converted Metanorma encode, applying or validating correction PRs, verifying an encode against its source, deciding whether a Metanorma content PR can merge, or diagnosing whether differences are corrections or regressions.
---

# Reviewing and correcting Metanorma transcriptions

Review an existing Metanorma encode against its source of record, apply
or validate corrections, and decide merge-readiness. The workflow is:
scope, ground truth, verification battery, verdict, correction. The
reference files carry the details; this file carries the rules that
decide success or failure.

## The workflow

1. **Scope.** Establish what the PR claims to touch: the diff must be
   limited to one document family's directory (plus the site manifest
   where the layout migrates); no caches, secrets, or generated
   artifacts. Map changed files old→new with `git diff -M
   --name-status` — relocations must be pure renames (R100); anything
   outside the claimed scope is a finding.

2. **Ground truth.** Identify the authoritative source: the PDF (via
   `pdftotext`), the OCR export, the HTML export — and CHECK WHETHER IT
   IS BILINGUAL before concluding there is no French (or other
   language) ground truth; the other side of the same PDF is
   authoritative for that language's tree. Where a sibling corpus
   carries the same standard in a corrected encode, it is a
   cross-reference, never the authority.

3. **Verification battery.** Run the mechanical checks, the
   ground-truth spot-checks, and the completeness gate — see
   `references/verification.md`. CI green means the site builds; it
   does not mean the content matches the source.

4. **Verdict.** Classify: approve-quality (corrections move toward the
   source), concerns (findings that need fixing before merge), problem
   (content loss or fabrication). Every finding carries file:line and
   the wrong→corrected evidence. Minor cosmetics are noted, not
   blocking.

5. **Correction.** Fix-ups go on the PR branch itself (force-with-lease
   push), never as uncommitted advice. Only fix what is provably wrong
   against ground truth; source typos are transcribed, not repaired.
   See `references/corrections.md`.

## The rules that decide success

- **CI green is not content-verified.** The site building proves the
  encode compiles and passes the publish gates; only the ground-truth
  spot-checks prove fidelity. Both are required for a verdict.

- **Corrections must move toward the source.** Every substantive hunk
  is judged against the PDF/OCR: if the change cannot be explained by
  the source, it is a regression regardless of how plausible it reads.
  Watch the meaning-change classes: modal verbs (shall/should/may),
  numeric values and units, table rows, deleted clauses, added
  sentences absent from the source (fabrications — an encode once
  carried a requirement sentence the printed standard never
  contained).

- **Faithful oddities are not findings.** Printed typos — a
  misspelled term, a wrong identifier digit, an odd construction —
  transcribed verbatim are correct. A "typo introduced" flag against a source-
  faithful encode is a review error.

- **Content coverage is a gain when it grows.** A review pass that adds
  annexes, restores dropped sections, or converts structure (tables →
  definition lists inside terms clauses) is a positive finding, not
  scope creep — verify the additions against the source and credit
  them.

- **No uncommitted advice.** A validated finding ships as a commit on
  the PR branch with a normal commit message, or as a review comment
  with file:line — never as a loose suggestion the author must guess
  at.

- **Per-corpus policies are recorded, not unified.** Some conventions
  legitimately differ between corpora (the "modified —" term-source
  marker is kept in one corpus and stripped in another; bibliography
  title stripping is split house practice). Match the corpus under
  review; never "fix" across corpora.
