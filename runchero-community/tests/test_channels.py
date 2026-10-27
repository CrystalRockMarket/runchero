from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import channels


class ChannelTests(unittest.TestCase):
    def test_facebook_handle(self) -> None:
        parsed, errors = channels.parse_channels({"facebook": "@beef.coop"})
        self.assertEqual(errors, [])
        self.assertEqual(parsed[0]["kind"], "link")
        self.assertEqual(parsed[0]["value"], "https://www.facebook.com/beef.coop")

    def test_website_without_scheme(self) -> None:
        parsed, errors = channels.parse_channels({"website": "example.com"})
        self.assertEqual(errors, [])
        self.assertEqual(parsed[0]["value"], "https://example.com")

    def test_facebook_link_without_scheme(self) -> None:
        parsed, errors = channels.parse_channels(
            {"facebook": "facebook.com/runchero"}
        )
        self.assertEqual(errors, [])
        self.assertEqual(parsed[0]["value"], "https://facebook.com/runchero")

    def test_full_instagram_link_kept(self) -> None:
        parsed, errors = channels.parse_channels(
            {"instagram": "https://instagram.com/runchero"}
        )
        self.assertEqual(errors, [])
        self.assertEqual(parsed[0]["value"], "https://instagram.com/runchero")

    def test_invalid_email_reported(self) -> None:
        parsed, errors = channels.parse_channels({"email": "not-an-email"})
        self.assertEqual(parsed, [])
        self.assertTrue(any("Email" in error for error in errors))

    def test_short_phone_reported(self) -> None:
        parsed, errors = channels.parse_channels({"phone": "123"})
        self.assertEqual(parsed, [])
        self.assertTrue(any("Phone" in error for error in errors))

    def test_custom_link_and_custom_contact(self) -> None:
        parsed, errors = channels.parse_channels({
            "custom_label_1": "Signal",
            "custom_value_1": "https://signal.me/#p/+15550100",
            "custom_label_2": "Market stall",
            "custom_value_2": "Saturday mornings",
        })
        self.assertEqual(errors, [])
        self.assertEqual(parsed[0]["kind"], "link")
        self.assertEqual(parsed[0]["label"], "Signal")
        self.assertEqual(parsed[1]["kind"], "contact")
        self.assertEqual(parsed[1]["value"], "Saturday mornings")

    def test_no_channels(self) -> None:
        parsed, errors = channels.parse_channels({})
        self.assertEqual(parsed, [])
        self.assertEqual(errors, [])

    def test_hrefs(self) -> None:
        email = channels.decorate([{"kind": "contact", "label": "Email",
                                    "value": "hi@example.com"}])[0]
        phone = channels.decorate([{"kind": "contact", "label": "Phone",
                                    "value": "555 0100"}])[0]
        address = channels.decorate([{"kind": "contact", "label": "Address",
                                      "value": "1 Main St"}])[0]
        self.assertEqual(email["href"], "mailto:hi@example.com")
        self.assertEqual(phone["href"], "tel:5550100")
        self.assertEqual(address["href"], "")

    def test_split_for_edit_keeps_fixed_and_custom(self) -> None:
        stored = [
            {"kind": "contact", "label": "Phone", "value": "555 0100"},
            {"kind": "link", "label": "Website", "value": "https://example.com"},
            {"kind": "contact", "label": "Signal", "value": "555 0199"},
        ]
        split = channels.split_for_edit(stored)
        self.assertEqual(split["fixed"]["phone"], "555 0100")
        self.assertEqual(split["fixed"]["website"], "https://example.com")
        self.assertEqual(split["custom"][0]["label"], "Signal")
        self.assertEqual(len(split["custom"]), 3)


if __name__ == "__main__":
    unittest.main()
