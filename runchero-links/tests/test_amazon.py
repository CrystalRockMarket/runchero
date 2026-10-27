from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services import amazon

TAG = "runchero-20"


class ProductTests(unittest.TestCase):
    def test_plain_dp(self):
        result = amazon.convert("https://www.amazon.com/dp/B08N5WRWNW", TAG)
        self.assertTrue(result.ok)
        self.assertEqual(result.affiliate_url, f"https://www.amazon.com/dp/B08N5WRWNW?tag={TAG}")
        self.assertEqual(result.kind, "product")
        self.assertEqual(result.asin, "B08N5WRWNW")

    def test_named_product_strips_tracking(self):
        raw = (
            "https://www.amazon.com/Echo-Dot-4th-Gen/dp/B08N5WRWNW/"
            "ref=sr_1_1?keywords=echo&qid=123&sr=8-1&th=1&psc=1&tag=old-20"
        )
        result = amazon.convert(raw, TAG)
        self.assertTrue(result.ok)
        self.assertEqual(result.affiliate_url, f"https://www.amazon.com/dp/B08N5WRWNW?tag={TAG}")

    def test_gp_product(self):
        result = amazon.convert("https://www.amazon.com/gp/product/B08N5WRWNW/ref=abc", TAG)
        self.assertTrue(result.ok)
        self.assertEqual(result.affiliate_url, f"https://www.amazon.com/dp/B08N5WRWNW?tag={TAG}")

    def test_mobile_product(self):
        result = amazon.convert("https://m.amazon.com/gp/aw/d/B08N5WRWNW?ref=abc", TAG)
        self.assertTrue(result.ok)
        self.assertEqual(result.affiliate_url, f"https://m.amazon.com/dp/B08N5WRWNW?tag={TAG}")

    def test_invalid_product_id(self):
        result = amazon.convert("https://www.amazon.com/dp/SHORT", TAG)
        self.assertFalse(result.ok)
        self.assertIn("product ID", result.error)

    def test_page_fallback(self):
        result = amazon.convert("https://www.amazon.com/gp/yourstore?ref=nav", TAG)
        self.assertTrue(result.ok)
        self.assertEqual(result.kind, "page")
        self.assertEqual(result.affiliate_url, f"https://www.amazon.com/gp/yourstore?tag={TAG}")


class SearchTests(unittest.TestCase):
    def test_search_link(self):
        raw = "https://www.amazon.com/s?k=canning+jars&ref=nb_sb_noss&qid=42"
        result = amazon.convert(raw, TAG)
        self.assertTrue(result.ok)
        self.assertEqual(result.kind, "search")
        self.assertEqual(result.affiliate_url, f"https://www.amazon.com/s?k=canning%20jars&tag={TAG}")

    def test_search_keeps_department(self):
        raw = "https://www.amazon.com/s?k=cast+iron&i=garden&ref=abc&crid=XYZ"
        result = amazon.convert(raw, TAG)
        self.assertTrue(result.ok)
        self.assertEqual(
            result.affiliate_url,
            f"https://www.amazon.com/s?k=cast%20iron&i=garden&tag={TAG}",
        )

    def test_build_search_url(self):
        url = amazon.build_search_url("pressure canner", TAG)
        self.assertEqual(
            url,
            f"https://www.amazon.com/s?k=pressure%20canner&tag={TAG}",
        )

    def test_build_search_url_requires_text(self):
        with self.assertRaises(ValueError):
            amazon.build_search_url("   ", TAG)


class SafetyTests(unittest.TestCase):
    def test_non_amazon_host(self):
        result = amazon.convert("https://example.com/dp/B08N5WRWNW", TAG)
        self.assertFalse(result.ok)
        self.assertIn("Only Amazon", result.error)

    def test_lookalike_host(self):
        result = amazon.convert("https://amazon.com.evil.com/dp/B08N5WRWNW", TAG)
        self.assertFalse(result.ok)

    def test_userinfo_rejected(self):
        result = amazon.convert("https://user@www.amazon.com/dp/B08N5WRWNW", TAG)
        self.assertFalse(result.ok)

    def test_ftp_rejected(self):
        result = amazon.convert("ftp://www.amazon.com/dp/B08N5WRWNW", TAG)
        self.assertFalse(result.ok)

    def test_unexpected_port(self):
        result = amazon.convert("https://www.amazon.com:8080/dp/B08N5WRWNW", TAG)
        self.assertFalse(result.ok)

    def test_short_link_flag(self):
        result = amazon.convert("https://a.co/d/abc123", TAG, allow_short=False)
        self.assertFalse(result.ok)
        self.assertEqual(result.kind, "short")

    def test_short_link_resolved(self):
        def fake_resolver(url):
            return "https://www.amazon.com/dp/B08N5WRWNW?ref=abc"

        result = amazon.convert("https://a.co/d/abc123", TAG, resolver=fake_resolver)
        self.assertTrue(result.ok)
        self.assertEqual(result.original, "https://a.co/d/abc123")
        self.assertEqual(result.affiliate_url, f"https://www.amazon.com/dp/B08N5WRWNW?tag={TAG}")

    def test_short_link_failure(self):
        def broken(url):
            raise RuntimeError("The shortcut service could not be reached.")

        result = amazon.convert("https://amzn.to/abc123", TAG, resolver=broken)
        self.assertFalse(result.ok)
        self.assertIn("could not be reached", result.error)


class BulkTests(unittest.TestCase):
    def test_bulk_skips_blank_lines(self):
        text = "https://www.amazon.com/dp/B08N5WRWNW\n\nhttps://www.amazon.com/dp/B09XYZ1234\n"
        results, total = amazon.convert_many(text, TAG)
        self.assertEqual(total, 2)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r.ok for r in results))

    def test_bulk_limit(self):
        text = "\n".join(["https://www.amazon.com/dp/B08N5WRWNW"] * 60)
        results, total = amazon.convert_many(text, TAG, limit=50)
        self.assertEqual(total, 60)
        self.assertEqual(len(results), 50)


if __name__ == "__main__":
    unittest.main()
