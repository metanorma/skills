# OSD ↔ Git interoperability (lanes, bridges, chains, fallbacks)

An ISO project can run in one of two lanes — the
[OSD platform](https://www.iso.org/it-tools-for-standards-development.html)
(the ISO/IEC default since January 2025, with exemptions available) or the
Git-native lane (Metanorma + commenter + GitHub). Both satisfy the same
Directives obligations; they differ in the ledger and the tooling. Full
comparison with diagrams:
[metanorma.org/learn/ballot-comment-dispositions](https://metanorma.org/learn/ballot-comment-dispositions/).

## The four bridges

At any moment exactly one lane is the ledger of record. Bridges move the
delta across, and every crossing ends with a validation artifact (rendered
document, validated YAML, generated sheet) before the other ledger changes.

| Bridge | Direction | What crosses | Automation today |
|---|---|---|---|
| B1 — STS (document) | both | Draft content | Metanorma emits ISO STS (Git→OSD); OSD exports STS, `mnconvert` converts STS→Metanorma XML (OSD→Git) |
| B2 — Comments | OSD→Git | New ballot comments | OSD comment export XLSX → `commenter import` (auto-detected); one issue per comment |
| B3 — Dispositions | Git→OSD | Proposed answers | `commenter fill`/`export` produce the ISO comment sheet; OSD collates. Direct upload is the convergence target |
| B4 — Milestones | events | Ballot opens/closes, stage codes | Procedural: mirrored as GitHub milestones |

## EXTRACT — OSD → Git (E1–E5)

- **E1 Export**: STS XML + comment XLSX exports from OSD.
- **E2 Convert**: `mnconvert` STS→Metanorma XML (or keep STS canonical).
  *Exit check*: rendered PDF matches the OSD view.
- **E3 Import comments**: `commenter import` on the OSD XLSX; one issue per
  comment with document-qualified markers.
- **E4 Stand up the ledger**: repo + CI (render + validate), stage labels,
  milestone for the current stage code, published block frozen.
  *Exit check*: CI green.
- **E5 Declare**: committee notes the exemption/transfer; Git becomes the
  ledger of record; OSD read-only until re-sync.

## IMPORT — Git → OSD (I1–I5)

- **I1 Freeze**: tag the ballot commit; CI renders STS XML + PDF + DOC.
- **I2 Import the document**: today Word import / secretariat-uploaded PDF;
  direct STS import is emerging.
- **I3 Seed comments**: issues with proposed dispositions emitted through the
  ISO commenting template (`commenter fill`) — OSD auto-collates.
- **I4 Ballot**: members comment/vote in OSD; the Git ledger mirrors the
  ballot window as a milestone (40.20 → 40.60).
- **I5 Close the loop**: ballot results export feeds E1. Import and extract
  are one round trip.

## FALLBACK — when OSD is unavailable (F1–F4)

- **F1 Freeze** the last known-good state (STS snapshot + comment export) —
  the recovery anchor.
- **F2 Continue offline**: drafting in Metanorma/Git with full CI; the
  Directives do not prescribe an editing tool.
- **F3 Ballots via the secretariat**: PDF/DOC ballots + comment sheets
  through ISO CS — fully valid under the Directives.
- **F4 Re-sync**: on recovery, run IMPORT I1–I4 from the newest tag; the
  delta is the commits since the F1 anchor.

## Decision inputs

Committee OSD position (default vs exemption); need for Git history and
CI-rendered artifacts; stage timing (about-to-ballot argues OSD, heavy
drafting argues Git); secretariat distribution requirements (disposition
DOCX + fixed document + STS XML — both lanes produce all three). When OSD
gains STS round-trip and structured comment upload, E1–E3 and I2–I3 collapse
to single steps.
