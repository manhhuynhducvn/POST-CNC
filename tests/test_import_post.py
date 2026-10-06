"""Metadata intake tests only; these do not exercise the Autodesk post engine."""

from __future__ import annotations

import hashlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import import_post


class ImportPostTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        original = import_post.ROOT
        for relative in (
            "upstream/MANIFEST.md",
            "machines/_template-machine.md",
            "posts/_template-post/README.md",
            "posts/_template-post/RELEASE-CHECKLIST.md",
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original / relative, target)
        self.patch_root = patch.object(import_post, "ROOT", self.root)
        self.patch_root.start()
        self.addCleanup(self.patch_root.stop)
        self.cps = Path(self.temp.name) / "base.cps"
        self.data = b"// Synthetic bytes for metadata testing ONLY\r\n"
        self.cps.write_bytes(self.data)

    def invoke(self, answers: list[str]) -> None:
        with patch.object(sys, "argv", ["import_post.py", "--path", str(self.cps)]):
            with patch("builtins.input", side_effect=answers), patch("sys.stdout", new=io.StringIO()):
                import_post.main()

    def test_import_profile_and_repeat_are_non_destructive(self) -> None:
        # First six prompts: base, revision, official source, engine, license, machine ID.
        first = ["vendor-base", "", "", "", "", "MC-001"]
        # Machine prompts + manual. Unknown values remain unknown.
        intake = ["ACME Mill 3", "Controller X", "3-axis", ""] + [""] * 7 + [""]
        self.invoke(first + intake)
        digest = hashlib.sha256(self.data).hexdigest()
        relative = f"upstream/vendor-base/unverified-{digest[:12]}/base.cps"
        stored = self.root / relative
        self.assertEqual(stored.read_bytes(), self.data)
        manifest = (self.root / "upstream/MANIFEST.md").read_text(encoding="utf-8")
        self.assertIn(f"| {relative} | UNKNOWN | UNKNOWN | local:base.cps |", manifest)
        self.assertIn(digest, manifest)
        machine = self.root / "machines/MC-001.md"
        self.assertIn("| Hãng/model máy | ACME Mill 3 |", machine.read_text(encoding="utf-8"))
        self.assertIn("| Quy trình ATC | UNKNOWN |", machine.read_text(encoding="utf-8"))
        self.assertTrue((self.root / "posts/MC-001/RELEASE-CHECKLIST.md").exists())
        self.assertFalse(list((self.root / "posts/MC-001").glob("*.cps")))
        before = machine.read_bytes()
        self.invoke(first)
        self.assertEqual(machine.read_bytes(), before)
        self.assertEqual((self.root / "upstream/MANIFEST.md").read_text(encoding="utf-8"), manifest)

    def test_same_path_new_content_does_not_overwrite(self) -> None:
        answers = ["vendor-base", "r123", "", "", "", ""]
        self.invoke(answers)
        stored = self.root / "upstream/vendor-base/r123/base.cps"
        manifest = (self.root / "upstream/MANIFEST.md").read_bytes()
        self.cps.write_bytes(b"// changed source")
        with self.assertRaises(FileExistsError):
            self.invoke(answers)
        self.assertEqual(stored.read_bytes(), self.data)
        self.assertEqual((self.root / "upstream/MANIFEST.md").read_bytes(), manifest)

    def test_rejects_unsafe_ids_and_url_query(self) -> None:
        for candidate in ["..", "../../out", "UNKNOWN", "foo|bar"]:
            with self.assertRaises(ValueError):
                import_post.safe_id(candidate)
        with self.assertRaises(ValueError):
            import_post.read_source("https://example.org/base.cps?token=private")


if __name__ == "__main__":
    unittest.main()
