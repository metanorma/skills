#!/usr/bin/env python3
"""Validation battery for transcribed Metanorma documents.

Checks the AsciiDoc source, the compiled XML, and the compiled HTML for
the failure classes that transcription pipelines actually produce:
missing flavor attributes, broken fence balance, dangling cross-
references, prose trapped in source blocks, and term-element counts.

Usage:
    validate_metanorma.py document.adoc [--xml document.xml] [--html document.html]

Exit status is non-zero when any check fails.
"""
import argparse
import html as htmllib
import re
import sys

FAILURES = []
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, ok, detail))
    if not ok:
        FAILURES.append(f"{name}: {detail}")


def check_adoc(path):
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")

    check("flavor attribute", ":mn-document-class:" in text,
          "missing :mn-document-class: — the compile fails without it")

    # docnumber+partnumber pair trips metanorma-iho docidentifier cleanup
    # (metanorma-iho#577): carry one glued docnumber until the flavor is fixed
    flavor_m = re.search(r"^:mn-document-class:\s*(\S+)", text, re.M)
    flavor = flavor_m.group(1) if flavor_m else ""
    check("no :partnumber: split on iho-family documents",
          not (flavor in ("iho", "iala") and re.search(r"^:partnumber:", text, re.M)),
          ":docnumber: + :partnumber: crashes metanorma-iho docidentifier "
          "cleanup (metanorma-iho#577) — carry one glued :docnumber: "
          "with a source comment until the flavor is fixed")

    # imagesdir must be absent when body paths already carry images/
    has_imagesdir = bool(re.search(r"^:imagesdir:", text, re.M))
    body_img = bool(re.search(r"^image:?s?images/", text, re.M))
    check("imagesdir omitted", not (has_imagesdir and body_img),
          "imagesdir double-prefixes body image paths")

    # fence balance
    for tok in ("----", "====", "....", "++++"):
        opens = sum(1 for l in lines if l.rstrip() == tok)
        check(f"fence balance {tok!r}", opens % 2 == 0,
              f"{opens} unpaired '{tok}' lines — text will be trapped in blocks")

    # example fences must follow an [example] opener
    bad_fences = []
    open_pending = False
    for i, l in enumerate(lines):
        if l == "====":
            prev = lines[i - 1].rstrip() if i else ""
            if not open_pending and prev != "[example]":
                bad_fences.append(i + 1)
            open_pending = not open_pending
    check("example fence pairing", not bad_fences,
          f"==== fences not opened by [example] at lines {bad_fences}")

    # math: the block style selects the parser; flag mismatches
    check("no [$latexmath] role", not re.search(r"^\[\$latexmath\]", text, re.M),
          "[$latexmath] sets a role, not the block style — use [latexmath]")

    stem_paras = [i + 1 for i, l in enumerate(lines)
                  if re.match(r"^\\\[($|\s)", l)
                  or re.match(r"^\\\[.*\\\]$", l.strip())]
    check("no bare \\[...] stem paragraphs", not stem_paras,
          f"LaTeX in stem paragraphs parses as asciimath: lines {stem_paras[:6]}")

    latex_cmds = re.compile(r"\\(frac|sqrt|int|exp|sum|prod|left|right|text|mathrm|tag)\b")
    bad_stem_blocks = []
    for i, l in enumerate(lines):
        if l.rstrip() == "[stem]":
            j = i + 1
            if j < len(lines) and lines[j].strip() == "++++":
                k = j + 1
                while k < len(lines) and lines[k].strip() != "++++":
                    if latex_cmds.search(lines[k]):
                        bad_stem_blocks.append(i + 1)
                        break
                    k += 1
    check("no LaTeX inside [stem] passthroughs", not bad_stem_blocks,
          f"asciimath parser sees LaTeX commands at lines {bad_stem_blocks[:6]}")

    bad_delims = []
    for i, l in enumerate(lines):
        if l.rstrip() == "[latexmath]":
            j = i + 1
            while j < len(lines) and lines[j].strip() != "----":
                j += 1
            j += 1
            while j < len(lines) and lines[j].strip() != "----":
                if lines[j].strip().startswith("\\[") or lines[j].strip().endswith("\\]"):
                    bad_delims.append(j + 1)
                j += 1
    check("latexmath blocks free of \\[ \\] delimiters", not bad_delims,
          f"delimiters are stem-paragraph syntax, not formula content: lines {bad_delims[:6]}")

    # annex style and depth
    check("annex style", "[annex]" not in text,
          "use [appendix] — the annex style is unknown to asciidoctor")
    in_annex = False
    deep = []
    for i, l in enumerate(lines, 1):
        if l.startswith("[appendix]"):
            in_annex = True
            continue
        m = re.match(r"^(=+) ", l)
        if m:
            depth = len(m.group(1))
            if l.startswith("== ") and "Appendix" not in l:
                in_annex = in_annex and depth >= 2
            if in_annex and depth >= 5:
                deep.append((i, l[:40]))
            if depth == 2:
                in_annex = l.startswith("== ") and False
    check("annex heading depth", not deep,
          f"depth-5 headings inside annexes at {deep[:4]}")

    # UML stereotypes must be guillemets
    stereotypes = re.findall(r"\\?<<(?:interface|enumeration)[^»\n]{0,12}", text)
    check("stereotype guillemets", not stereotypes,
          f"double-angle stereotypes parse as xrefs: {stereotypes[:4]}")

    # no hardcoded self clause numbers in headings (=== 4.1 Title)
    hard = [l.strip() for l in lines
            if re.match(r"^={2,4} \d+(\.\d+)*[ 	]", l)]
    check("no hardcoded heading numbers", not hard, f"{hard[:4]}")

    # hand-written note/example numbers double-number after rendering
    numbered = [(i + 1, l.strip()[:40]) for i, l in enumerate(lines)
                if re.match(r"^NOTE \d+[:.]", l)
                or re.match(r"^EXAMPLE \d+[:.]", l)
                or re.match(r"^\s*-?\+?Note \d+ to entry[:.]", l)]
    check("no hand-numbered notes/examples", not numbered,
          f"auto-numbered content carries manual numbers: {numbered[:4]}")

    # cell-spec order: span comes before alignment
    bad_spec = [(i + 1, l.strip()[:50]) for i, l in enumerate(lines)
                if re.search(r"\^[\d.]+\+?h?\||\^[\d.]+\+\^", l)]
    check("cell-spec span before alignment", not bad_spec,
          f"alignment-before-span cell specs parse wrong: {bad_spec[:4]}")

    # [sourcecode] is not a Metanorma style
    sc = [i + 1 for i, l in enumerate(lines) if "[sourcecode" in l]
    check("no [sourcecode] style", not sc,
          f"use [source%unnumbered,lang] — [sourcecode] is unknown: lines {sc[:4]}")

    # adaptation is a block role, not a locality
    adapted = [l.strip()[:50] for l in lines
               if re.search(r"<<[^>]*,[Aa]dapted>>", l)]
    check("adapted as block role", not adapted,
          f"Adapted belongs on the block ([.source%adapted]), not in the xref: {adapted[:4]}")

    # [bibliography] styling is legal only on leaf sections
    biblio_mid = [i + 1 for i, l in enumerate(lines)
                  if l.strip() == "[bibliography]"
                  and any(re.match(r"^== ", x)
                          for x in lines[i + 1:i + 4])]
    check("bibliography style on leaf sections only", not biblio_mid,
          f"[bibliography] heading followed by nested sections at lines {biblio_mid[:6]}")

    # bracket-led lines parse as block attributes (phantom figures)
    phantom = [l.strip()[:40] for l in lines
               if re.match(r"^\s+[*]?\[.+?\][*]?\s*$", l)]
    check("no bracket-led lines", not phantom,
          f"lines starting with '[' parse as attributes: {phantom[:4]}")

    # shifted fences: a ---- closer followed by record content without a
    # blank line leaks that content into the page as raw text
    shifted = []
    for i, l in enumerate(lines):
        if l.rstrip() == "----":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            prev = lines[i - 1].rstrip() if i else ""
            nxt = lines[j].strip() if j < len(lines) else ""
            if nxt and not prev.startswith(("[source", "[example")) \
               and re.match(r"^(id|termid|data|status|terms|definition|"
                            r"scores|entry|reviewer|date|-)", nxt):
                shifted.append(i + 1)
    check("fences not shifted", not shifted,
          f"---- followed directly by record content at lines {shifted[:4]}")

    # markdown fences are not AsciiDoc; they render as literal text
    md_fences = [i + 1 for i, l in enumerate(lines) if re.match(r"^```\w*$", l)]
    check("no markdown fences", not md_fences,
          f"``` lines render as visible text: {md_fences[:6]}")

    # one level-0 title per document (merged-copy signature)
    l0 = [i + 1 for i, l in enumerate(lines) if re.match(r"^= \S", l)]
    check("single level-0 title", len(l0) <= 1,
          f"{len(l0)} level-0 titles at lines {l0[:6]} — merged document copies")

    # leaked model-refusal text from AI-assisted conversions
    refusals = [i + 1 for i, l in enumerate(lines)
                if re.search(r"I (?:can't|cannot|won't) turn this|"
                             r"I (?:can't|cannot) (?:assist|provide|reproduce)|"
                             r"I (?:can|will) summarize", l, re.I)]
    check("no model-refusal text", not refusals,
          f"leaked AI refusal/summary text at lines {refusals[:6]}")

    return text


def check_xml(path):
    xml = open(path, encoding="utf-8").read()

    ids = set(re.findall(r'anchor="([^"]+)"', xml))
    ids |= set(re.findall(r'id="([^"]+)"', xml))
    xrefs = set(re.findall(r'<xref target="([^"]+)"', xml))
    dangling = sorted(t for t in xrefs if t not in ids and not t.startswith("_"))
    check("xml xrefs resolve", not dangling, f"dangling targets: {dangling[:6]}")

    id_list = re.findall(r'id="([^"]+)"', xml)
    dupes = sorted({i for i in id_list if id_list.count(i) > 1
                    and not i.startswith("_")})
    check("xml ids unique", not dupes, f"duplicate ids: {dupes[:6]}")

    counts = {
        "terms": xml.count("<term "),
        "concept mentions": xml.count("<concept"),
        "termnotes": xml.count("<termnote"),
        "termexamples": xml.count("<termexample"),
    }
    for k, v in counts.items():
        CHECKS.append((f"xml {k}", True, str(v)))
    return counts


def check_html(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    prose_blocks = []
    for p in re.findall(r"<pre[^>]*>(.*?)</pre>", raw, re.S):
        txt = htmllib.unescape(re.sub(r"<[^>]+>", "", p)).strip()
        words = len(txt.split())
        if words == 0:
            continue
        sig = sum(txt.count(c) for c in ("{}", ":", "#", "|", "=", ">", "@")) / words
        if words > 40 and sig < 0.10:
            prose_blocks.append(txt[:70].replace("\n", " "))
    check("html prose not in source blocks", not prose_blocks,
          f"{len(prose_blocks)} prose-like <pre> blocks: {prose_blocks[:3]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("adoc")
    ap.add_argument("--xml")
    ap.add_argument("--html")
    args = ap.parse_args()

    check_adoc(args.adoc)
    if args.xml:
        check_xml(args.xml)
    if args.html:
        check_html(args.html)

    for name, ok, detail in CHECKS:
        mark = "PASS" if ok else "FAIL"
        line = f"[{mark}] {name}"
        if detail and (not ok or name.startswith("xml ")):
            line += f" — {detail}"
        print(line)

    failed = sum(1 for _, ok, _ in CHECKS if not ok)
    print(f"\n{len(CHECKS) - failed}/{len(CHECKS)} checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
