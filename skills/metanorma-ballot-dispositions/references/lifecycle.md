# The ISO development lifecycle (Directives-anchored reference)

The cycle every ISO document follows, per the
[ISO/IEC Directives, Part 1 — Procedures for the technical work](https://www.iso.org/sites/directives/current/consolidated/index.html).
Stage codes are the stable identifiers (authoritative table:
[iso.org/stage-codes.html](https://www.iso.org/stage-codes.html)); cite
stages by name + code, never by clause number (clause numbering moved across
the 2012 → 2021 → 2026 editions).

## The eight steps

1. **A ballot or systematic review is held** and collects comments from
   national bodies and liaison organizations.
2. **The secretariat and project leader receive those comments** as DOCX or
   DOC files — ISO balloting templates, legacy collations, OSD exports.
3. **The project leader posts individual comments into the GitHub issue
   tracker** — each comment becomes exactly one issue (commenter import +
   github-create).
4. **The project team discusses and proposes dispositions** for every
   comment, linking each to a commit — one commit per issue, one PR per
   document.
5. **For a meeting or comments disposition**, commenter gathers all
   dispositions and fills the comment sheet DOCX; distribute it with the
   fixed document (PDF, DOC) and the STS XML.
6. **Steps 4–5 repeat** until the dispositions are final.
7. **Once finalized, a ballot is launched at the next stage**, the last
   disposition round is done, the new stage is set, and the approved
   document is released as an artifact (metanorma-release conventions).
8. **Steps 1–7 repeat** at every stage until the document is published as an
   International Standard.

## Stage table (codes per iso.org/stage-codes.html)

| Stage | Codes | Ballot / obligation |
|---|---|---|
| 10 Proposal | 10.20 → 10.99 | NP to P-members, 3 months; approval creates the project |
| 20 Preparatory | 20.00 → 20.20 | Project registered (AWI); WD by the project team; no international ballot |
| 30 Committee | 30.x → 30.99 | CD comment/ballot within the committee; 30.99 = approved for registration as DIS |
| 40 Enquiry | 40.00 → 40.60 | DIS to all national bodies; 40.20 = ballot initiated, **12 weeks**; 40.92 = full report circulated / referred back |
| 50 Approval | 50.00 → 50.99 | FDIS yes/no vote, 2 months; mandatory after technical changes at 40 |
| 60 Publication | 60.00 → 60.60 | Proof (PRF) → International Standard published |
| Maintenance | 5 years after 60.60 | Systematic review: confirm / amend / revise / withdraw |

## The disposition obligation

After every ballot, the ballot report presents the vote results and all
comments received, and for every comment the project editor records the
disposition on which consensus is achieved (or, failing that, the
proposition). This obligation is what the issue comments + generated
disposition sheet implement. Ballots are direct (yes/no) at FDIS — no
comments are permitted there, so the ledger is final before 50.00.

## Editions note

Stage codes are stable across Directives editions; clause numbers are not
(2012 edition: stages in clause 2; 2021 edition: clause 4; 2026 consolidated
edition renumbers again — systematic-review guidance cites clauses 2.3–2.8
for the revision path).
