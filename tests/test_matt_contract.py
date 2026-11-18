"""Local check that the Matt Pocock skills this skill hands off to still exist.

Skipped where they are not installed (e.g. CI); set MATT_SKILLS_DIR to point elsewhere.
A rename upstream (like CONTEXT.md -> GLOSSARY.md before) fails here instead of
leaving a dead hand-off in SKILL.md.
"""

import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "skills" / "agent-ready" / "SKILL.md"
SKILLS = Path(os.environ.get("MATT_SKILLS_DIR", Path.home() / ".agents" / "skills"))
SETUP = SKILLS / "setup-matt-pocock-skills" / "SKILL.md"
HANDOFFS = ["writing-for-agents", "setup-matt-pocock-skills", "domain-modeling", "retro", "code-review"]


@unittest.skipUnless(SETUP.is_file(), "Matt Pocock skills are not installed")
class MattContractTests(unittest.TestCase):
    def test_handoff_table_names_installed_skills(self):
        table = ENTRY.read_text()
        for name in HANDOFFS:
            with self.subTest(skill=name):
                self.assertRegex(table, rf"(?m)^\| {re.escape(name)} \|")
                skill = SKILLS / name / "SKILL.md"
                self.assertTrue(skill.is_file())
                self.assertRegex(skill.read_text(), rf"(?m)^name: {re.escape(name)}$")

    def test_setup_still_owns_agent_skills_block(self):
        self.assertIn("## Agent skills", SETUP.read_text())


if __name__ == "__main__":
    unittest.main()
