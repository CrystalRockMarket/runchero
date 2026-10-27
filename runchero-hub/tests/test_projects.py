from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, projects


class ProjectListTests(unittest.TestCase):
    def test_only_allowed_projects(self):
        slugs = [p.slug for p in projects.visible_projects()]
        self.assertEqual(
            slugs,
            ["info-depo", "shop", "map", "mirrors", "links"],
        )

    def test_excluded_tokens_are_never_present(self):
        for project in projects.visible_projects():
            haystack = " ".join([project.slug, project.name, project.description]).lower()
            for token in config.EXCLUDED_TOKENS:
                self.assertNotIn(token, haystack)

    def test_is_excluded(self):
        for text in ("earth.love", "EARTH_LOVE", "games-earth", "Games.Earth"):
            self.assertTrue(projects.is_excluded(text), text)
        self.assertFalse(projects.is_excluded("Runchero Beef"))

    def test_project_url_uses_request_host(self):
        project = projects.find("links")
        self.assertIsNotNone(project)
        url = projects.project_url(project, "192.168.1.179:8092")
        self.assertEqual(url, "http://192.168.1.179:8091/")

    def test_all_screenshots_exist(self):
        for project in projects.visible_projects():
            target = config.STATIC_DIR / "img" / "shots" / project.screenshot
            self.assertTrue(target.exists(), str(target))


if __name__ == "__main__":
    unittest.main()
