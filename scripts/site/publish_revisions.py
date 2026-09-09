"""Publish archived Markdown and verify every current/archive route after Jekyll builds."""

import hashlib
import json
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path


def entries(docs):
    return json.loads((docs / "_data/page-revisions.json").read_text(encoding="utf-8"))["pages"]


def archive_errors(docs):
    pages = entries(docs)
    errors = [] if pages else ["The revision manifest is empty."]
    downloads = json.loads((docs / "_data/page-revisions.json").read_text(encoding="utf-8")).get("downloads", [])
    for page in pages + downloads:
        archive = docs / page["archive"]
        if not archive.is_file():
            errors.append(f"Missing archive: {page['archive']}")
        elif hashlib.sha256(archive.read_bytes()).hexdigest() != page["sha256"]:
            errors.append(f"Archive changed: {page['archive']}")
    return errors


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.hrefs = set()
        self.noindex = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.hrefs.add(attrs.get("href"))
        if tag == "meta" and attrs.get("name") == "robots":
            self.noindex = "noindex" in attrs.get("content", "")


def publish(site, docs):
    errors = archive_errors(docs)
    if errors:
        return errors
    pages = entries(docs)
    for page in pages:
        for key, other in (("url", "old_url"), ("old_url", "url")):
            url = page[key]
            output = site / ("index.html" if url == "/" else url.lstrip("/"))
            if not output.is_file():
                errors.append(f"Missing rendered page: {url}")
                continue
            parsed = Links(output.read_text(encoding="utf-8"))
            if page[other] not in parsed.hrefs:
                errors.append(f"Missing version link: {url} -> {page[other]}")
            if key == "old_url" and not parsed.noindex:
                errors.append(f"Archive lacks noindex: {url}")
        target = site / page["archive"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(docs / page["archive"], target)

    search = json.loads((site / "search.json").read_text(encoding="utf-8"))
    indexed = {page["u"] for page in search}
    for page in pages:
        if page["old_url"] in indexed:
            errors.append(f"Archive appears in current-page search: {page['old_url']}")
        if page["url"] not in indexed:
            errors.append(f"Current page is missing from search: {page['url']}")
    print(f"Checked {len(pages)} current/archive pairs and published {len(pages)} exact Markdown archives.")
    return errors


if __name__ == "__main__":
    site = Path(sys.argv[1])
    docs = Path(__file__).resolve().parents[2] / "docs"
    failures = publish(site, docs)
    if failures:
        sys.exit("\n".join(failures))
