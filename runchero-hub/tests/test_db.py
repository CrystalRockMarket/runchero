from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import db


class RequestStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = db.connect(Path(self.tmp.name) / "hub.db")
        db.init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_create_list_update_delete(self):
        first = db.create_request(
            self.conn, name="Ada", contact="ada@example.com",
            title="Seed swap", description="A board for trading seeds.",
            category="Community",
        )
        second = db.create_request(
            self.conn, name="", contact="", title="Tool library",
            description="Lend tools to neighbours.", category="Other",
        )
        rows = db.list_requests(self.conn)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["id"], second)
        self.assertEqual(db.counts(self.conn)["new"], 2)

        db.update_request(self.conn, first, status="planned", note="Looks good")
        row = db.get_request(self.conn, first)
        self.assertEqual(row["status"], "planned")
        self.assertEqual(row["admin_note"], "Looks good")
        self.assertEqual(db.counts(self.conn)["planned"], 1)

        db.delete_request(self.conn, second)
        self.assertEqual(len(db.list_requests(self.conn)), 1)
        self.assertIsNone(db.get_request(self.conn, second))

    def test_search_and_status_filter(self):
        db.create_request(
            self.conn, name="Ada", contact="", title="Seed swap",
            description="Trade seeds.", category="Community",
        )
        db.create_request(
            self.conn, name="Bo", contact="", title="Tool library",
            description="Lend tools.", category="Other",
        )
        self.assertEqual(len(db.list_requests(self.conn, query="seed")), 1)
        self.assertEqual(len(db.list_requests(self.conn, query="Bo")), 1)
        self.assertEqual(len(db.list_requests(self.conn, status="planned")), 0)


if __name__ == "__main__":
    unittest.main()
