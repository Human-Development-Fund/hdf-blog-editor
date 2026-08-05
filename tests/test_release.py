from __future__ import annotations

import hashlib
import importlib.util
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release_tool", ROOT / "tools" / "release.py")
assert SPEC and SPEC.loader
RELEASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RELEASE)


class ReleaseTests(unittest.TestCase):
    def test_canonical_skill(self) -> None:
        RELEASE.check_skill()
        RELEASE.check_markup_fixtures()
        RELEASE.check_retrofit_fixtures()
        RELEASE.check_evals()

    def test_builds_expected_archives(self) -> None:
        paths = RELEASE.build()
        self.assertEqual(len(paths), 3)
        for path in paths:
            self.assertTrue(path.is_file())
            self.assertGreater(path.stat().st_size, 0)
            with zipfile.ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())

    def test_chatgpt_and_claude_have_skill_root(self) -> None:
        RELEASE.build()
        for platform in ("chatgpt", "claude"):
            path = ROOT / "dist" / f"hdf-blog-editor-{platform}-v{RELEASE.VERSION}.zip"
            with zipfile.ZipFile(path) as archive:
                self.assertIn("hdf-blog-editor/SKILL.md", archive.namelist())
                self.assertIn("hdf-blog-editor/scripts/check_retrofit.py", archive.namelist())

    def test_antigravity_has_skill_and_workflow(self) -> None:
        RELEASE.build()
        path = ROOT / "dist" / f"hdf-blog-editor-antigravity-v{RELEASE.VERSION}.zip"
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            self.assertIn(".agent/skills/hdf-blog-editor/SKILL.md", names)
            self.assertIn(".agent/skills/hdf-blog-editor/scripts/check_retrofit.py", names)
            self.assertIn(".agents/workflows/review-hdf-blog.md", names)

    def test_build_is_reproducible(self) -> None:
        first = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in RELEASE.build()
        }
        second = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in RELEASE.build()
        }
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
