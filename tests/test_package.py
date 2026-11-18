"""Offline distribution checks; they make no claim about agent behavior."""

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "agent-ready"
LINK = re.compile(r"\[[^\]]*\]\(([^\s)]+)\)")


def slug(heading):
    # GitHub-style anchor: lowercase, drop punctuation (CJK letters survive \w), spaces -> "-".
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def anchors(path):
    return {slug(h) for h in re.findall(r"(?m)^#{1,6} (.+)$", path.read_text())}


def local_links(path):
    for link in LINK.findall(path.read_text()):
        target = urlsplit(link)
        if not target.scheme and not target.netloc:
            yield link, target


class PackageTests(unittest.TestCase):
    def test_slug_matches_github(self):
        self.assertEqual(slug("仓库专属 Skill"), "仓库专属-skill")
        self.assertEqual(slug("一份标准，多方读取"), "一份标准多方读取")
        self.assertEqual(slug("报错与 lint 消息"), "报错与-lint-消息")

    def test_entry_metadata(self):
        text = (SKILL / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        metadata = text.split("---", 2)[1]
        self.assertRegex(metadata, r"(?m)^name: agent-ready$")
        self.assertRegex(metadata, r"(?m)^description: .+")
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file())

    def test_relative_links_and_anchors_resolve(self):
        for path in ROOT.rglob("*.md"):
            boundary = SKILL if path.is_relative_to(SKILL) else ROOT
            for link, target in local_links(path):
                resolved = (path.parent / unquote(target.path)).resolve() if target.path else path
                with self.subTest(file=path.relative_to(ROOT), link=link):
                    self.assertTrue(resolved.is_relative_to(boundary))
                    self.assertTrue(resolved.exists())
                    if target.fragment and resolved.suffix == ".md":
                        self.assertIn(unquote(target.fragment), anchors(resolved))

    def test_every_reference_is_routed_from_entry(self):
        routed = {
            (SKILL / unquote(t.path)).resolve()
            for _, t in local_links(SKILL / "SKILL.md")
            if t.path
        }
        for path in [*SKILL.glob("references/*"), *SKILL.glob("assets/*")]:
            with self.subTest(file=path.relative_to(SKILL)):
                self.assertIn(path.resolve(), routed)

    def test_skill_contains_no_machine_paths(self):
        for path in SKILL.rglob("*"):
            if path.is_file():
                with self.subTest(file=path.relative_to(SKILL)):
                    self.assertNotRegex(path.read_text(), r"(?:/Users/|/home/|/var/folders/|[A-Z]:\\)")


if __name__ == "__main__":
    unittest.main()
