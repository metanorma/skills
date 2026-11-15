---
name: metanorma-corpus
description: Manage multi-document Metanorma site repositories — the collection manifest, per-document directory layout, artifact hygiene, and the site build/publish pipeline with its STS conversion gate. Use when setting up or restructuring a corpus repository that builds many Metanorma documents as one site, registering documents in metanorma.yml, migrating directory layouts, triaging site-build or mnconvert failures, or merging waves of document PRs.
---

# Managing Metanorma corpus repositories

A corpus repository builds many documents as one site. The workflow
is: manifest, layout, artifacts, gates, waves. The reference files
carry the details; this file carries the rules that decide success or
failure.

## The workflow

1. **Manifest.** `metanorma.yml` lists exactly the `document.adoc`
   paths that build. Every publish-clean document is registered; the
   rest are noted as pending in manifest comments. An unregistered
   document silently drops out of the site; a phantom entry fails CI.
   Registration newly exposes a document to the publish step — see
   rule below.

2. **Layout.** One directory per edition with stable names —
   `sources/<family>/<year>/`, language tiers (`en/`, `fr/`) for
   multilingual editions. Migrations are pure renames (`git mv`, R100
   in `git diff -M`); superseded machine conversions leave version
   control when their replacement lands. See `references/site.md`.

3. **Artifacts.** Compile outputs (`document.xml`, `document.html`,
   `document.doc`, `document.pdf`, `document.sts.xml`,
   `document.pdf.fo.xml`, `document.xml.abort`, `relaton/`) are
   gitignored and never committed. Purge commits are a legitimate PR
   body (−10k lines of committed debris).

4. **Gates.** The site pipeline runs site generate, the mnconvert STS
   conversion per document, and (where installed) a completeness
   gate comparing source clause titles against the compiled XML.
   Compile-clean is not publish-clean. See `references/site.md`.

5. **Waves.** Document PRs land as waves (encode → review →
   re-review). Sequential manifest edits conflict pairwise — merge,
   fetch, rebase the next branch locally, push, merge. Rename/modify
   conflicts resolve as corrected content at the renamed path.

## The rules that decide success

- **Register only publish-clean documents.** A manifest entry is a
  promise the document survives all gates. Broken encodes stay
  unregistered with a manifest comment stating what blocks them
  (restructuring pending; STS failure class).

- **Year-only names.** Edition metadata lives in the document header,
  never the path; `2014-a1`-style suffixes are acceptable where the
  edition genuinely is an amendment. Never slug the edition into the
  directory and the header.

- **One edition per directory.** Superseded conversions are removed
  in the same change that lands the replacement — not left side by
  side.

- **The manifest count is the site's document count.** After any wave,
  manifest entries resolve, contain no duplicates, and equal the
  documents that should publish. Verify the arithmetic when language
  tiers make one directory publish two documents.

- **Waves land sequentially with rebases.** Merge order within a wave
  is arbitrary only when the PRs touch disjoint directories; any
  manifest edit makes the wave a clique — pick an order, rebase each
  successor, and never merge two manifest-editing branches blind.
