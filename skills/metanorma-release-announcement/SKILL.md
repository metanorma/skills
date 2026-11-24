---
name: metanorma-release-announcement
description: Write Metanorma release announcement blog posts for metanorma.org, grounded in verified change data. Covers the full workflow: diff the actual dependency ledger (metanorma/versions manifests plus the frozen docker lock, not just gemspec floors), audit which changes are Ribose/lutaml gems, benchmark performance claims in the released container, follow 2026 release-announcement conventions (Node.js release posts, Red Hat release notes, GitHub changelog), and structure the post as AsciiDoc with the metanorma.org front-matter. Use when cutting a Metanorma CLI or flavor release that needs a public announcement, or when asked to draft, review, or rewrite a Metanorma release post.
---

# Writing Metanorma release announcements

Produce a release post that is grounded, deep, and house-styled. Every
claim traces to an artifact you inspected: a diffed lockfile, a built
gem, a benchmark you ran. Research first, write second.

## Phase 1: gather the ground truth

1. **The dependency ledger.** Diff the release-to-release lock, not the
   gemspec. Gemspec floors are minimums; the ledger is what ships.
   - Older releases: `metanorma/versions` repo, `data/gemfile/vX.Y.Z/Gemfile.lock.archived`.
   - Current releases: `metanorma-docker` tag `vX.Y.Z`,
     `metanorma-debian/Gemfile.lock` (the frozen image lock).
   - Produce added / removed / changed counts and the full lists. The
     structural story (families consolidated, engines replaced, runtime
     default gems dropped) lives in the removed list.
2. **The floor diff** from the cli gemspec between release tags, as the
   guarantee set.
3. **Flavor and coverage inventories.** For consolidated monogems, list
   the actual contents from the gem source tree
   (`gh api repos/<org>/<repo>/contents/lib/<namespace>`): identifier
   authorities in pubid, bibliographic sources in relaton. State what
   users can newly cite. Distinguish genuinely new flavors from old
   flavors returning to the default bundle.
4. **Which changes are ours.** Tag every added or changed gem as a
   Ribose/lutaml-org gem (uniword, leptris, yeptris, moxml, coradoc,
   canon, emfsvg, vectory, omml, fontisan, metanorma-mirror,
   metanorma-release, lutaml-*) or third-party. Our gems get the
   narrative; third-party bumps get the changelog line.
5. **Benchmark any performance claim in the released container.** Run
   the measurement yourself against a real Metanorma document of the
   relevant size, report the method (parse + walk + serialize round
   trip, iterations, container), and never publish an unbenchmarked
   number.

## Phase 2: conventions (verified 2026)

- **Node.js release posts** (nodejs.org blog): one-paragraph lede that
  announces the release and names three or four highlights inline; then
  a "Notable changes" section whose items carry feature-name headers
  with two to three sentence descriptions; attribution of contributors.
- **Red Hat release notes**: fixed categories. "Technology preview" is
  the established term for experimental features offered for feedback.
- **GitHub changelog**: title-as-headline, dated, short, linked.
- House writing style: complete sentences, declarative, grounded
  claims.

**Never**: AI slop phrasing ("battle-tested", "seamless",
"cutting-edge", "robust"), testing-effort narration (never describe how
or how much anything was tested), quoting or paraphrasing users'
verdicts, em-dashes, exclamation marks, fragments.

## Phase 3: structure

Write AsciiDoc with the metanorma.org `_posts` front-matter (layout
post, title, date, categories `news release`, authors, excerpt). Body:

1. **Lede** (one paragraph): announce; the headline items inline; where
   to get it (gem version, docker tags).
2. **Notable changes**: several paragraphs per change, each under a
   feature-name `===` header. Order by user impact. For consolidations,
   name the family counts, the surviving gem, the model basis, and the
   coverage list (new flavors, what users can cite now). For engine
   replacements, give the measured numbers with their method. For new
   capabilities, state what the capability is for, not only what it is.
3. **Fixed**: terse verb-led bullets for defect classes, with the
   observable symptom.
4. **Technology preview**: experimental features with the invitation
   for feedback (uniword DOCX, alpha flavors).
5. **Compatibility notes**: what a user must act on (Ruby line, pin
   changes, restored flavors).
6. **Upgrading**: fenced install and pull commands; the ledger link.
7. **Acknowledgments**: one short paragraph, full names with
   affiliations, thanks for testing and filing findings.

Depth rule: each notable change is worth several paragraphs. A bullet
list is not a release post. If a section would run under a paragraph,
merge it into another.

## Phase 4: deliver

Draft as a branch on `metanorma.org` replacing the existing
`_posts/YYYY-MM-DD-*.adoc` file, PR, and merge on green. Post titles
state that the release happened ("X released"), never a maturity
adjective.
