---
name: metanorma-ballot-dispositions
description: Manage ISO ballot and systematic-review comment dispositions end to end — import comment sheets (DOCX/DOC/OSD XLSX exports) into canonical Commenter YAML, post one GitHub issue per comment, drive one-commit-per-comment dispositions in per-document PRs, retrieve dispositions from issues, and generate the disposition sheets for distribution. Use when processing a new round of ballot or systematic-review comments for a Metanorma-managed ISO document, creating or re-syncing comment issues on GitHub, writing or validating dispositions, exporting disposition DOCX sheets, running a comment-disposition meeting, or deciding between OSD-based and Git-based development lanes for a project.
---

# Managing ISO ballot comment dispositions

Carry a round of ISO comments from intake to the distributed disposition
sheet. The ledger model: **one comment = one issue = one disposition = one
commit** (in one PR per document), with the disposition text living as an
issue comment and the generated disposition sheet as the distribution
artifact. The lifecycle is the ISO/IEC Directives Part 1 cycle — ballot,
intake, issue posting, disposition commits, generated meeting pack, stage
advancement, release — repeated per stage until publication. See
`references/lifecycle.md` for the Directives-anchored stage table and
`references/osd-interop.md` for the OSD-vs-Git lanes and the bridges between
them.

## The workflow

1. **Intake & import.** Convert every received comment sheet to YAML with
   `commenter import` (ISO 2012-03 DOCX, OSD XLSX resolved/comments-only
   exports, redline DOCX are auto-detected). Legacy `.doc` needs a
   LibreOffice conversion first (textutil output lacks `word/styles.xml`).
   Hand-fill `date` / `document` / `project` — header extraction is broken.
   Embedded formulas and images are lost on import: when a comment references
   a formula, consult the original sheet before dispositioning.

2. **Canonicalize & deduplicate.** Pick ONE canonical sheet per document per
   round — usually the newest collation. Older snapshots are provenance,
   never merged: collations renumber comments between rounds (the same ID
   names different comments), so merging rounds creates near-duplicate
   issues. Merge only disjoint sets (`commenter merge`), then
   `commenter validate`. Split mixed-document sheets before merging. Drop
   empty stub rows, noting the drop.

3. **Post issues.** Always `--dry-run` first. Run documents serially — the
   GitHub search API rate-limits mid-run, and failed creations are recovered
   by re-running (existing issues skip via the marker). The duplicate marker
   MUST be document-qualified
   (`[STAGE] DOCUMENT COMMENT_ID` /
   `urn:commenter:repo:stage:document:comment-id`): identical comment IDs
   across documents of one repository collide otherwise, and the run then
   writes the wrong issue numbers into the YAML. The `github:` blocks in the
   YAML are machine-written truth — never hand-edit them, and never derive
   issue numbers from comment order (read the YAML).

4. **Dispositions.** One commit per open issue on the per-document PR
   (`fixes #NN`), and the disposition posted as a comment on the issue —
   that comment is the proposed answer in the generated sheet. Wording
   leads with the verdict (Accepted / Accepted with modification / Noted /
   Already resolved), then what changed and where. Content changes go to the
   *draft edition block* of the dataset (`edition: '202x'`); the published
   editions stay frozen at `edition = "2019"` with their own edition pins —
   without the pins the published documents render both blocks and PDF
   generation fails on duplicate anchors. Math edits keep each complete
   expression inside one `stem:[...]` (never `stem:[n] > 0`).

5. **Retrieve & export.** `commenter github-retrieve` fills YAML
   observations from the issues (last-comment fallback; closed issues
   only). Before export, check for entries with empty `observations` — each
   one is a missed disposition comment, not a formatting problem. Then
   `commenter export ... --shading` produces the disposition DOCX. The
   export is idempotent.

6. **Distribute.** Per document: the disposition DOCX + the fixed document
   in PDF and DOC + the STS XML. Everything is generated; nothing is
   hand-assembled.

## The rules that decide success

- **One ledger of record per lane, per moment.** If the project runs in OSD
  and Git simultaneously, exactly one is authoritative at a time; the other
  is synced through the bridges only (see `references/osd-interop.md`).
- **Fix-backed issues close on merge; noted issues close with a documented
  disposition comment.** An issue without a disposition comment or a closing
  commit is unfinished work.
- **Generic process documentation does not go into the project repository.**
  Project repos carry project state (sheets, YAML, dispositions, a
  quickstart README); reusable process docs belong in metanorma.org
  documentation and skills.
- **Comment formulas lost on import are a lookup obligation**, not an
  acceptable gap — resolve against the original sheet before dispositioning.
- **CI/site builds share a concurrency group and are serial.** A 45-minute
  site build is normal; a 23-second "failure" is a cancellation, not a bug —
  rerun after the competing build finishes.
- **Include paths never escape the document directory** (asciidoctor jail):
  generators and common-files are copied into place, not referenced with
  `../`.
- **Cite stages by name + stage code** (10.99, 20.20, 30.99, 40.20,
  50.20, 60.60 — stable across editions per
  https://www.iso.org/stage-codes.html), never by clause number (clause
  numbering changes between Directives editions).

## OSD interoperability

When the project runs in OSD, is moving between lanes, or needs a fallback:
use the four bridges (B1 STS document, B2 comments OSD→Git, B3 dispositions
Git→OSD, B4 milestones), the EXTRACT chain (E1–E5), the IMPORT chain
(I1–I5), and the fallback procedures (F1–F4) — all detailed with today's
automation state in `references/osd-interop.md`. At any moment exactly one
lane is the ledger of record; every bridge crossing ends with a validation
artifact before the other ledger changes.
