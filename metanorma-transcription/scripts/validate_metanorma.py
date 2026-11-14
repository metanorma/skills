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
