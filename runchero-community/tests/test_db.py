from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import db


def listing(**overrides):
    data = {
        "name": "Marta Ruiz",
        "category": "Neighbours",
        "description": "Long-time north-side neighbour.",
        "location": "North Runchero",
        "published": True,
        "submitter_contact": "secret@example.com",
        "admin_note": "",
    }
    data.update(overrides)
    return data


CHANNELS = [
    {"kind": "contact", "label": "Phone", "value": "555 0100", "sort_order": 10},
    {"kind": "link", "label": "Website", "value": "https://example.com",
     "sort_order": 20},
]


class DatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "community.db"
        self.conn = db.connect(self.path)
        db.init_db(self.conn)

    def tearDown(self) -> None:
        self.conn.close()
        self.tmp.cleanup()

    def test_entries_table_has_no_kind_column(self) -> None:
        columns = {row["name"] for row in self.conn.execute(
            "PRAGMA table_info(entries)"
        )}
        self.assertNotIn("kind", columns)

    def test_create_and_get(self) -> None:
        entry_id = db.create_entry(self.conn, listing(), CHANNELS)
        entry = db.get_entry(self.conn, entry_id)
        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry["name"], "Marta Ruiz")
        self.assertTrue(entry["published"])
        self.assertEqual([channel["label"] for channel in entry["channels"]],
                         ["Phone", "Website"])

    def test_search_matches_channels(self) -> None:
        db.create_entry(self.conn, listing(), CHANNELS)
        db.create_entry(
            self.conn,
            listing(name="Sam Okafor", category="Skills & Help"),
            [{"kind": "contact", "label": "Email", "value": "ferment@example.com",
              "sort_order": 10}],
        )
        by_name = db.list_entries(self.conn, q="Marta Ruiz")
        by_channel = db.list_entries(self.conn, q="ferment@example.com")
        self.assertEqual([entry["name"] for entry in by_name], ["Marta Ruiz"])
        self.assertEqual([entry["name"] for entry in by_channel], ["Sam Okafor"])

    def test_filters(self) -> None:
        db.create_entry(self.conn, listing(), CHANNELS)
        db.create_entry(self.conn, listing(name="June Halvorsen", category="Garden & Farm"),
                        [{"kind": "contact", "label": "Phone", "value": "555 0111",
                          "sort_order": 10}])
        self.assertEqual(len(db.list_entries(self.conn, category="Neighbours")), 1)
        self.assertEqual(len(db.list_entries(self.conn, category="Garden & Farm")), 1)
        self.assertEqual(len(db.list_entries(self.conn, category="Health")), 0)

    def test_update_replaces_channels(self) -> None:
        entry_id = db.create_entry(self.conn, listing(), CHANNELS)
        db.update_entry(
            self.conn,
            entry_id,
            listing(name="Marta Ruiz Garcia", published=False),
            [{"kind": "contact", "label": "Email", "value": "beef@example.com",
              "sort_order": 10}],
        )
        entry = db.get_entry(self.conn, entry_id)
        assert entry is not None
        self.assertEqual(entry["name"], "Marta Ruiz Garcia")
        self.assertFalse(entry["published"])
        self.assertEqual(len(entry["channels"]), 1)
        self.assertEqual(entry["channels"][0]["value"], "beef@example.com")

    def test_hidden_entry_absent_from_public_queries(self) -> None:
        entry_id = db.create_entry(self.conn, listing(), CHANNELS)
        db.set_published(self.conn, entry_id, False)
        self.assertEqual(db.list_entries(self.conn), [])
        self.assertIsNone(db.get_entry(self.conn, entry_id, published_only=True))
        self.assertIsNotNone(db.get_entry(self.conn, entry_id))
        counts = db.counts(self.conn)
        self.assertEqual(counts, {"total": 1, "published": 0, "hidden": 1})

    def test_delete_removes_channels(self) -> None:
        entry_id = db.create_entry(self.conn, listing(), CHANNELS)
        db.delete_entry(self.conn, entry_id)
        self.assertIsNone(db.get_entry(self.conn, entry_id))
        remaining = self.conn.execute("SELECT COUNT(*) FROM channels").fetchone()[0]
        self.assertEqual(remaining, 0)

    def test_listing_order(self) -> None:
        db.create_entry(self.conn, listing(name="Zoe Adams"), CHANNELS)
        db.create_entry(self.conn, listing(name="Aaron Bell"), CHANNELS)
        names = [entry["name"] for entry in db.list_entries(self.conn)]
        self.assertEqual(names, ["Aaron Bell", "Zoe Adams"])


if __name__ == "__main__":
    unittest.main()
