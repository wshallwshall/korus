"""Archived prose keeps its bytes and has a distinct, linked page in the built site."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import _ccxtest as t


def load_publisher():
    spec = importlib.util.spec_from_file_location(
        "publish_revisions", t.REPO_ROOT / "scripts/site/publish_revisions.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PageRevisions(unittest.TestCase):
    def test_the_manifest_covers_every_original_page(self):
        manifest = json.loads(t.read(t.REPO_ROOT / "docs/_data/page-revisions.json"))
        entries = manifest["pages"]
        self.assertEqual(50, len(entries))
        self.assertEqual(50, len({p["source"] for p in entries}))
        self.assertEqual(50, len({p["old_url"] for p in entries}))
        self.assertFalse({p["url"] for p in entries} & {p["old_url"] for p in entries})
        for entry in entries:
            with self.subTest(page=entry["source"]):
                self.assertEqual(
                    str(Path(entry["source"]).with_suffix(".old.md")).replace("\\", "/"),
                    entry["archive"],
                )
                self.assertTrue((t.REPO_ROOT / "docs" / entry["source"]).is_file())

    def test_every_archive_keeps_its_original_bytes(self):
        self.assertEqual([], load_publisher().archive_errors(t.REPO_ROOT / "docs"))

    def test_a_changed_archive_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            (docs / "_data").mkdir()
            (docs / "A.old.md").write_text("changed", encoding="ascii")
            (docs / "_data/page-revisions.json").write_text(json.dumps({"pages": [
                {"archive": "A.old.md", "sha256": "0" * 64}
            ]}), encoding="ascii")
            self.assertTrue(load_publisher().archive_errors(docs))

    def test_missing_archives_and_an_empty_manifest_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            (docs / "_data").mkdir()
            manifest = docs / "_data/page-revisions.json"
            for entries in ([], [{"archive": "absent.old.md", "sha256": "0" * 64}]):
                manifest.write_text(json.dumps({"pages": entries}), encoding="ascii")
                self.assertTrue(load_publisher().archive_errors(docs))

    def test_only_named_archives_are_outside_the_current_prose_corpus(self):
        import test_prose_rules_hold as prose
        self.assertNotIn("docs/FAQ.old.md", prose.docs_prose_files())
        self.assertIn("docs/FAQ.md", prose.docs_prose_files())
        self.assertEqual(["docs/unregistered.old.md"], prose.unread_pages(["docs/unregistered.old.md"]))

    def test_heading_aliases_resolve_but_code_examples_do_not(self):
        from test_internal_links_resolve import parse
        slugs, _ = parse('<a id="old-heading"></a>\n\n## New heading\n\n```html\n<a id="example"></a>\n```')
        self.assertIn("old-heading", slugs)
        self.assertIn("new-heading", slugs)
        self.assertNotIn("example", slugs)

    def test_aliases_inside_inline_code_and_comments_do_not_resolve(self):
        from test_internal_links_resolve import parse, resolvable_anchors
        text = (
            'Use `<a id="inline-example"></a>` as an example.\n'
            '<!-- <a id="comment-example"></a> -->\n'
            '<!--\n<span id="multiline-example"></span>\n-->\n'
            'The literal `<!--` does not open a comment.\n'
            '<a id="real-anchor"></a>\n'
        )
        self.assertEqual({"real-anchor"}, resolvable_anchors(parse(text)[0]))

    def test_explicit_ids_do_not_get_heading_suffixes(self):
        from test_internal_links_resolve import parse, resolvable_anchors
        text = (
            '<a id="repeat"></a>\n<span id="repeat"></span>\n'
            '<a id="heading"></a>\n## Heading\n## Heading\n'
        )
        self.assertEqual(
            {"repeat", "heading", "heading-1"},
            resolvable_anchors(parse(text)[0]),
        )


if __name__ == "__main__":
    unittest.main()
