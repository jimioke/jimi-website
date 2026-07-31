#!/usr/bin/env python3
"""Generate Hugo publication pages directly from a Zotero library.

This replaces the manual "export Publications.csv from Zotero, then run
bib_generator.py" workflow: it pulls items straight from the Zotero Web API
and writes theme-compliant markdown into content/publications/.

It reproduces the frontmatter that bib_generator.py emits (title, author,
status, type, citation, doi, file, date + abstract body), so the site theme
renders the results identically.

Configuration comes from environment variables (never hardcode your key):

    ZOTERO_LIBRARY_ID     required  numeric library id
    ZOTERO_LIBRARY_TYPE   optional  "user" (default) or "group"
    ZOTERO_API_KEY        required for private libraries; optional for public groups
    ZOTERO_COLLECTION_KEY optional  restrict to one collection (recommended)

Find your library id + create a key at https://www.zotero.org/settings/keys
(the "userID for use in API calls" is your ZOTERO_LIBRARY_ID for a user library).

Usage:
    python3 zotero_sync.py                 # create missing pages; report diffs & orphans
    python3 zotero_sync.py --overwrite     # also rewrite existing pages that changed
    python3 zotero_sync.py --prune         # delete orphaned pages (with confirmation summary)
    python3 zotero_sync.py --dry-run       # show what would happen, write nothing
"""

import argparse
import os
import re
import sys

import requests

CONTENT_DIR = "./content/publications"
PAPERS_DIR = "./static/papers"          # where the referenced PDFs must live
API_ROOT = "https://api.zotero.org"
PAGE_SIZE = 100

# Item types that are not publications (skip these entirely).
SKIP_TYPES = {"attachment", "note", "annotation"}

STOPWORDS = {
    "in", "for", "and", "a", "an", "the", "of", "on", "this", "to",
    "who", "whom", "whose", "why", "how", "where", "is", "my", "from",
}

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def fix_datestring(d):
    """Normalise a free-form Zotero date into Hugo's required yyyy-mm-dd.

    Ported from jsonparser.py — Zotero dates come in many shapes.
    Returns the string unchanged if nothing matches (so you can spot it).
    """
    d = (d or "").strip()
    if not d:
        return ""

    def clamp(part):  # "00"/"0" -> "01"; otherwise zero-pad
        return "01" if part in ("0", "00") else part.zfill(2)

    # YYYY-MM-DD or YYYY/MM/DD (day/month may be 00 when only partly known)
    m = re.match(r"^([0-9]{4})[-/]([0-9]{1,2})[-/]([0-9]{1,2})", d)
    if m:
        return f"{m.group(1)}-{clamp(m.group(2))}-{clamp(m.group(3))}"
    # YYYY-MM or YYYY/MM
    m = re.match(r"^([0-9]{4})[-/]([0-9]{1,2})$", d)
    if m:
        return f"{m.group(1)}-{clamp(m.group(2))}-01"
    # YYYY
    if re.match(r"^[0-9]{4}$", d):
        return d + "-01-01"

    # MM/DD/YYYY (US order — first group is 1-2 digits, so no year/month clash above)
    m = re.match(r"^([0-9]{1,2})\/([0-9]{1,2})\/([0-9]{2,4})", d)
    if m:
        month, day, year = clamp(m.group(1)), clamp(m.group(2)), m.group(3)
        if len(year) < 4:
            year = ("20" + year) if int(year) < 30 else ("19" + year)
        return f"{year}-{month}-{day}"

    # "December 19, 2019" / "Dec 19 2019"
    m = re.match(r"([A-Za-z\.]+)\s+([0-9]{1,2}),?\s+([0-9]{4})", d)
    if m and m.group(1)[:3].lower() in MONTHS:
        return f"{m.group(3)}-{MONTHS[m.group(1)[:3].lower()]:02}-{int(m.group(2)):02}"

    # "September 2024" style (month + year, no day)
    m = re.match(r"([A-Za-z\.]+)\s+([0-9]{4})$", d)
    if m and m.group(1)[:3].lower() in MONTHS:
        return f"{m.group(2)}-{MONTHS[m.group(1)[:3].lower()]:02}-01"

    return d  # unrecognised — caller warns


def fetch_items(library_type, library_id, api_key, collection_key):
    """Yield every item's `data` dict from the library/collection, paginated."""
    base = f"{API_ROOT}/{library_type}s/{library_id}"
    url = f"{base}/collections/{collection_key}/items" if collection_key else f"{base}/items"
    headers = {"Zotero-API-Version": "3"}
    if api_key:
        headers["Zotero-API-Key"] = api_key

    start = 0
    while True:
        resp = requests.get(
            url,
            headers=headers,
            params={"format": "json", "include": "data", "limit": PAGE_SIZE, "start": start},
            timeout=30,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        for entry in batch:
            yield entry["data"]
        total = int(resp.headers.get("Total-Results", "0"))
        start += PAGE_SIZE
        if start >= total:
            break


def format_authors(creators):
    """"Last, First" Zotero creators -> "First Last, First Last" (authors only)."""
    names = []
    first_last = ""
    for c in creators or []:
        if c.get("creatorType") != "author":
            continue
        if "name" in c:  # single-field creator (institution etc.)
            names.append(c["name"])
            if not first_last:
                first_last = c["name"]
            continue
        last = c.get("lastName", "").strip()
        first = c.get("firstName", "").strip()
        names.append(f"{first} {last}".strip())
        if not first_last:
            first_last = last
    return ", ".join(names), first_last


def slug_from_title(title):
    words = [w.lower() for w in title.split(" ")]
    words = [w for w in words if w not in STOPWORDS][:3]
    words = [re.sub(r"[^\w]", "", w) for w in words]
    return "-".join(w for w in words if w)


def build_page(data):
    """Return (filename, content, warning, raw_date) for a Zotero item, or None to skip."""
    item_type = data.get("itemType", "")
    if item_type in SKIP_TYPES:
        return None

    title = data.get("title", "").strip()
    if not title:
        return None

    authors, first_last = format_authors(data.get("creators"))
    raw_date = data.get("date", "")
    date = fix_datestring(raw_date)
    url = data.get("url", "").strip()
    year = date[:4] if re.match(r"^[0-9]{4}", date) else "nd"
    doi = data.get("DOI", "").strip()
    abstract = data.get("abstractNote", "").strip()

    status = "Unpublished" if item_type == "manuscript" else "Published"

    if item_type == "report":
        publisher = data.get("publisher") or data.get("institution") or ""
        number = data.get("number") or data.get("reportNumber") or ""
        citation = f"<em>{publisher}</em>, No. <b>{number}</b>"
    elif item_type == "manuscript":
        citation = f"<em>{data.get('place', '')}</em>"
    else:  # journalArticle, conferencePaper, preprint, ...
        venue = data.get("publicationTitle") or data.get("proceedingsTitle") or ""
        issue = data.get("issue", "")
        issue_part = f"({issue})" if issue else ""  # omit empty parens
        citation = (
            f"<em>{venue}</em>, "
            f"<b>{data.get('volume', '')}</b>{issue_part}:{data.get('pages', '')}"
        )

    name = f"{year}-{first_last}-{slug_from_title(title)}".lower()

    lines = ["---", f'title: "{title}"', f"author: {authors}",
             f"status: {status}", f"type: {item_type}",
             f'citation: "{citation}"', f"doi: {doi}"]
    # PDF/link (smart fallback): prefer a locally hosted PDF in static/papers/;
    # otherwise use the Zotero URL. Never emit a broken local link — if neither
    # exists, the DOI badge stands alone. Manuscripts get neither.
    if status == "Published":
        if os.path.exists(os.path.join(PAPERS_DIR, f"{name}.pdf")):
            lines.append(f"file: {name}.pdf")
        elif url:
            lines.append(f"link: {url}")
    lines += [f"date: {date}", "---", "", abstract, ""]
    content = "\n".join(lines)

    warning = None
    if not date:
        warning = f"{name}: could not parse date '{raw_date}'"
    elif item_type == "report" and url and not url.startswith("http"):
        warning = f"{name}: report link is not an absolute URL ('{url}') — fix in Zotero"
    elif item_type == "report" and not (data.get("publisher") or data.get("institution")):
        warning = f"{name}: report has no publisher/institution — citation venue is blank"
    return f"{name}.md", content, warning, raw_date


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--overwrite", action="store_true",
                    help="rewrite existing pages whose content changed")
    ap.add_argument("--prune", action="store_true",
                    help="delete publication pages no longer in the library")
    ap.add_argument("--dry-run", action="store_true",
                    help="report actions without writing anything")
    ap.add_argument("--output-dir", default=CONTENT_DIR,
                    help="where to write pages (default: %(default)s; use a scratch dir to audit)")
    ap.add_argument("--verbose", action="store_true",
                    help="print each page's raw Zotero date -> normalized date")
    args = ap.parse_args()
    content_dir = args.output_dir

    library_id = os.environ.get("ZOTERO_LIBRARY_ID")
    if not library_id:
        sys.exit("ZOTERO_LIBRARY_ID is not set. See the header of this file for setup.")
    library_type = os.environ.get("ZOTERO_LIBRARY_TYPE", "user")
    api_key = os.environ.get("ZOTERO_API_KEY")
    collection_key = os.environ.get("ZOTERO_COLLECTION_KEY")

    os.makedirs(content_dir, exist_ok=True)

    created, updated, unchanged, warnings, dates = [], [], [], [], []
    generated_files = set()

    try:
        items = list(fetch_items(library_type, library_id, api_key, collection_key))
    except requests.HTTPError as e:
        sys.exit(f"Zotero API error: {e} (check library id/type/key/collection)")

    for data in items:
        result = build_page(data)
        if result is None:
            continue
        filename, content, warning, raw_date = result
        if warning:
            warnings.append(warning)
        dates.append(f"{filename[:-3]:55s}  {raw_date!r:22} -> {fix_datestring(raw_date) or '(unparsed)'}")
        generated_files.add(filename)

        path = os.path.join(content_dir, filename)
        existing = None
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                existing = f.read()

        if existing is None:
            created.append(filename)
            if not args.dry_run:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
        elif existing.rstrip() != content.rstrip():
            if args.overwrite:
                updated.append(filename)
                if not args.dry_run:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
            else:
                updated.append(filename + "  (differs — rerun with --overwrite to apply)")
        else:
            unchanged.append(filename)

    # Orphans: pages on disk that no longer correspond to a library item.
    on_disk = {f for f in os.listdir(content_dir) if f.endswith(".md")}
    orphans = sorted(on_disk - generated_files)

    # DOI-only pages: Published items with neither a hosted PDF nor an external
    # link. Adding static/papers/<slug>.pdf and re-running upgrades them to file:.
    doi_only = []
    for filename in generated_files:
        path = os.path.join(content_dir, filename)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            body = f.read()
        if "status: Published" in body and "\nfile:" not in body and "\nlink:" not in body:
            doi_only.append(filename[:-3] + ".pdf")

    def report(label, items):
        print(f"\n{label} ({len(items)}):")
        for it in sorted(items):
            print(f"  {it}")

    print("=" * 60)
    print(f"Zotero sync — {len(items)} items fetched"
          + (" [DRY RUN]" if args.dry_run else ""))
    print("=" * 60)
    if args.verbose:
        report("Dates (raw -> normalized)", dates)
    report("Created", created)
    report("Updated", updated)
    print(f"\nUnchanged: {len(unchanged)}")
    if orphans:
        report("Orphaned pages (no matching library item)", orphans)
        if args.prune and not args.dry_run:
            for o in orphans:
                os.remove(os.path.join(CONTENT_DIR, o))
            print("  -> deleted (--prune)")
        elif not args.prune:
            print("  (rerun with --prune to delete these)")
    if doi_only:
        report("Info: DOI-only pages (drop static/papers/<slug>.pdf + re-run to add a PDF badge)", doi_only)
    if warnings:
        report("WARNING: date issues", warnings)
    print()


if __name__ == "__main__":
    main()
