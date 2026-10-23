"""Market price engine.

Three keyless public feeds, so the shop can show a real, sourced comparison
without anyone signing up for an API key:

* USDA AMS ``ams_3228`` - Weekly Grocery Store Beef Feature Activity.
  Advertised prices at major grocery outlets, split by US region. Kentucky
  sits in the MIDWEST REGION block, so we get Kentucky-relevant weekly
  prices per cut.
* USDA ERS - monthly retail prices and price spreads, with a few cut level
  series (ground beef, round roast, sirloin steak, Choice beef retail).
* BLS public API - monthly consumer price series for ground beef.

Every provider degrades quietly. If a feed is unreachable the last known
value stays live, and the shop shows the date it was observed so a stale
number never masquerades as a fresh one.
"""
from __future__ import annotations

import csv
import datetime as _dt
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Iterable

from .. import config, db

AMS_3228_URL = "https://www.ams.usda.gov/mnreports/ams_3228.pdf"
ERS_CSV_URL = ("https://www.ers.usda.gov/media/5025/"
               "summary-of-retail-prices-and-price-spreads.csv")
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/{series_id}"

#: Kentucky's AMS region block.
AMS_REGION = "MIDWEST"

#: ERS series we track, keyed by our own series key.
ERS_SERIES = {
    "ers:choice_beef_retail": "Retail prices or values: Choice beef retail value",
    "ers:all_fresh_beef": "Retail prices or values: all-fresh beef retail value",
    "ers:ground_beef": "Retail prices or values: ground beef",
    "ers:round_roast": ("Retail prices or values: round roast, USDA Choice "
                        "boneless"),
    "ers:sirloin_steak": ("Retail prices or values: sirloin steak, USDA Choice "
                           "boneless"),
    "ers:beef_cpi": "Consumer price index, beef and veal",
    "ers:farmers_share": ("Price spread: Farmers' share of retail beef dollar, "
                          "percent"),
    "ers:wholesale_retail": "Price spread: beef wholesale to retail",
    "ers:farm_wholesale": "Price spread: beef farm to wholesale",
}

#: BLS series we track.
BLS_SERIES = {
    "bls:APU0000703111": "Ground chuck, 100% beef, per lb",
    "bls:APU0000703112": "Ground beef, 100% beef, per lb",
    "bls:APU0000703113": "Ground beef, lean/extra lean, per lb",
}

#: Quality grades we will not use as the benchmark: they are either budget
#: store brands or premium programs, so they are not a fair comparison for a
#: USDA Choice product.
_AMS_SKIP_QUALITY = {"value"}

#: Grade preference for the benchmark row when one item is advertised in
#: several grades. Branded products are Choice-level store brands, so they
#: rank with Choice; Ungraded/Other is the budget tier.
_AMS_QUALITY_RANK = {
    "choice": 0,
    "branded": 1,
    "branded - choice": 1,
    "branded - prime": 1,
    "select": 2,
    "standard": 3,
    "prime": 4,
    "ungrade": 5,
    "ungraded": 5,
    "ungraded/other": 5,
}


@dataclass
class Observation:
    series_key: str
    label: str
    value: float
    source: str
    region: str = "National"
    unit: str = "lb"
    observed_at: str = ""
    stores: int = 0
    low: float = 0.0
    high: float = 0.0
    note: str = ""


@dataclass
class ProviderResult:
    provider: str
    ok: bool
    observations: list[Observation] = field(default_factory=list)
    error: str = ""


# --------------------------------------------------------------------------
# http
# --------------------------------------------------------------------------

def fetch(url: str, timeout: int | None = None) -> bytes:
    request = urllib.request.Request(url, headers={
        "User-Agent": config.USER_AGENT,
        "Accept": "*/*",
    })
    with urllib.request.urlopen(request,
                                timeout=timeout or config.HTTP_TIMEOUT) as resp:
        return resp.read()


def _today() -> str:
    return _dt.date.today().isoformat()


# --------------------------------------------------------------------------
# USDA AMS weekly grocery beef feature activity
# --------------------------------------------------------------------------

#: The report is split into regional blocks. Kentucky sits in the Midwest
#: block, so that is the one we quote.
_REGION_NAMES = (
    "NATIONAL", "NORTHEAST", "SOUTHEAST", "MIDWEST", "SOUTH CENTRAL",
    "SOUTHWEST", "NORTHWEST", "ALASKA", "HAWAII",
)
_REGION_RE = re.compile(
    r"^(" + "|".join(name.replace(" ", r"\s+") for name in _REGION_NAMES)
    + r")\b")

#: Every page of a regional block repeats the column header. The report uses
#: two column widths, and the price unit column is blank on continuation
#: rows, so the header is what tells us where each column starts.
_COLUMN_NAMES = ("Section", "Quality", "Price Unit", "Item", "Environment",
                 "Condition", "Stores", "Price Range", "Wtd Avg")


def _column_positions(header: str) -> list[tuple[str, int]] | None:
    """Where each column starts in this block, read off the header line."""
    found: list[tuple[str, int]] = []
    cursor = 0
    for name in _COLUMN_NAMES:
        index = header.find(name, cursor)
        if index < 0:
            return None
        found.append((name, index))
        cursor = index + len(name)
    return found


def _slice_columns(line: str,
                   columns: list[tuple[str, int]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for index, (name, start) in enumerate(columns):
        end = columns[index + 1][1] if index + 1 < len(columns) else len(line)
        out[name] = line[start:end].strip()
    return out


_NUMBER_RE = re.compile(r"^[\d,]+$")
_RANGE_RE = re.compile(r"^([\d.]+)\s*-\s*([\d.]+)$")
_AMS_VALUE_ITEM_RE = re.compile(r",\s*Value$|^Value$", re.IGNORECASE)


def _pdf_to_text(pdf_bytes: bytes) -> str:
    """Extract text from the AMS PDF.

    The report is a text PDF, so poppler's pdftotext is used when it is
    installed. Without it we fall back to a small extractor that pulls the
    Flate-compressed text operators out of the content streams. If neither
    works the provider reports itself unavailable and the shop keeps using
    the last known values.
    """
    if shutil.which("pdftotext"):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as handle:
            handle.write(pdf_bytes)
            path = handle.name
        try:
            result = subprocess.run(
                ["pdftotext", "-layout", path, "-"],
                capture_output=True, timeout=90, check=False)
            if result.returncode == 0 and result.stdout:
                return result.stdout.decode("utf-8", "replace")
        except (OSError, subprocess.SubprocessError):
            pass
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass
    return _pdf_to_text_fallback(pdf_bytes)


def _pdf_to_text_fallback(pdf_bytes: bytes) -> str:
    """Minimal PDF text scrape: inflate the streams, pull the show-text
    operands. Good enough for the fixed layout of this one report.
    """
    import zlib

    chunks: list[str] = []
    for match in re.finditer(rb"stream\r?\n(.*?)endstream", pdf_bytes,
                             re.DOTALL):
        blob = match.group(1)
        try:
            data = zlib.decompress(blob)
        except zlib.error:
            continue
        if b"Tj" not in data and b"TJ" not in data:
            continue
        text: list[str] = []
        for piece in re.finditer(rb"\((?:\\.|[^\\()])*\)", data):
            raw = piece.group(0)[1:-1]
            raw = re.sub(rb"\\([()\\])", rb"\1", raw)
            text.append(raw.decode("latin-1", "replace"))
        if text:
            chunks.append("".join(text))
    return "\n".join(chunks)


def _parse_ams(text: str, region: str = AMS_REGION) -> list[Observation]:
    """Pull the region block out of the report text and read its rows.

    Each page of the report repeats the column header, so the column
    boundaries are recomputed whenever a header appears. Rows that leave the
    section or quality column blank continue the row above, which is how the
    report groups a cut across several grades.
    """
    observations: list[Observation] = []
    current = ""
    in_block = False
    columns: list[tuple[str, int]] | None = None
    section = ""
    quality = ""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        header = _REGION_RE.match(stripped)
        if header:
            current = " ".join(header.group(1).split()).upper()
            in_block = current.startswith(region[:7])
            columns = None
            section = ""
            quality = ""
            continue
        if not in_block:
            continue
        if "Price Range" in line and "Wtd Avg" in line:
            columns = _column_positions(line)
            continue
        if columns is None:
            continue
        cells = _slice_columns(line, columns)
        item = cells.get("Item", "")
        env = cells.get("Environment", "")
        cond = cells.get("Condition", "")
        if not item or cond not in ("Fresh", "Frozen", "Prepared"):
            continue
        if cells.get("Section"):
            section = cells["Section"]
            quality = cells.get("Quality", "")
        elif cells.get("Quality"):
            quality = cells["Quality"]
        elif not quality:
            quality = cells.get("Quality", "")
        note = quality.strip()
        # The report right-aligns "Per lb" in its column while the header is
        # left-aligned, so the quality cell sometimes ends with a fragment of
        # the price unit ("Ungrade Pe", "Branded Per"). Real grade names never
        # end in those letters, so the fragments are trimmed off.
        note = re.sub(r"\s*Per\s*lb$", "", note)
        note = re.sub(r"\s*Pe?r?\s*l?b?$", "", note).strip()
        if note.lower() in _AMS_SKIP_QUALITY:
            continue
        # "Value" rows are the budget store-brand tier, not a fair benchmark
        # for a USDA Choice product.
        if _AMS_VALUE_ITEM_RE.search(item):
            continue
        lowered = env.lower()
        if "grass fed" in lowered or "organic" in lowered:
            continue
        if lowered.startswith("abf") or "antibiotic" in lowered:
            continue
        stores_text = cells.get("Stores", "")
        wtd_text = cells.get("Wtd Avg", "")
        if not _NUMBER_RE.match(stores_text) or not wtd_text:
            continue
        try:
            stores = int(stores_text.replace(",", ""))
            wtd = float(wtd_text)
        except ValueError:
            continue
        lo = hi = 0.0
        range_match = _RANGE_RE.match(cells.get("Price Range", ""))
        if range_match:
            lo = float(range_match.group(1))
            hi = float(range_match.group(2))
        if wtd <= 0:
            continue
        observations.append(Observation(
            series_key=f"ams:{item}",
            label=item,
            value=wtd,
            source="USDA AMS",
            region=f"{current.title()} Region",
            unit="lb",
            observed_at=_today(),
            stores=stores,
            low=lo,
            high=hi,
            note=note,
        ))
    return observations


def _best_per_item(observations: Iterable[Observation]) -> list[Observation]:
    """One benchmark per item: the row advertised by the most outlets is the
    typical shelf price, so store coverage decides and the closest grade to
    USDA Choice breaks ties. Premium programs and the budget Value tier are
    filtered out before this runs.
    """
    best: dict[str, Observation] = {}
    for obs in observations:
        current = best.get(obs.series_key)
        if current is None:
            best[obs.series_key] = obs
            continue
        new_key = (-obs.stores, _AMS_QUALITY_RANK.get(obs.note.lower(), 99))
        cur_key = (-current.stores,
                   _AMS_QUALITY_RANK.get(current.note.lower(), 99))
        if new_key < cur_key:
            best[obs.series_key] = obs
    return list(best.values())


class Ams3228Provider:
    """USDA AMS weekly grocery store beef feature activity."""

    name = "USDA AMS"
    source = "USDA AMS"

    def __init__(self, region: str = AMS_REGION):
        self.region = region

    def fetch(self) -> ProviderResult:
        try:
            data = fetch(AMS_3228_URL)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            return ProviderResult(self.name, False, error=str(exc))
        try:
            text = _pdf_to_text(data)
        except Exception as exc:  # pragma: no cover - defensive
            return ProviderResult(self.name, False, error=f"pdf: {exc}")
        if not text:
            return ProviderResult(self.name, False, error="no text extracted")
        observations = _best_per_item(_parse_ams(text, self.region))
        if not observations:
            return ProviderResult(self.name, False, error="no rows parsed")
        return ProviderResult(self.name, True, observations)


# --------------------------------------------------------------------------
# USDA ERS monthly retail prices
# --------------------------------------------------------------------------

_MONTHS = {name: index for index, name in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}


class ErsProvider:
    """USDA ERS monthly retail price series."""

    name = "USDA ERS"
    source = "USDA ERS"

    def fetch(self) -> ProviderResult:
        try:
            data = fetch(ERS_CSV_URL)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            return ProviderResult(self.name, False, error=str(exc))
        text = data.decode("utf-8-sig", "replace")
        reader = csv.DictReader(io.StringIO(text))
        rows = [row for row in reader if row.get("Year")]
        if not rows:
            return ProviderResult(self.name, False, error="empty csv")
        latest_year = max(row["Year"] for row in rows)
        latest: dict[str, tuple[int, str, float]] = {}
        for row in rows:
            if row["Year"] != latest_year:
                continue
            month = _MONTHS.get(row.get("Month", ""))
            if month is None:
                continue
            item = row.get("Data_Item", "")
            for key, label in ERS_SERIES.items():
                if item != label:
                    continue
                try:
                    value = float(row["Value"])
                except (KeyError, TypeError, ValueError):
                    continue
                stamp = f"{latest_year}-{month:02d}-01"
                previous = latest.get(key)
                if previous is None or stamp > previous[1]:
                    latest[key] = (month, stamp, value)
        observations = []
        for key, (_month, stamp, value) in latest.items():
            unit = "lb"
            if "index" in ERS_SERIES[key].lower() or "percent" in ERS_SERIES[key].lower():
                unit = "index"
            observations.append(Observation(
                series_key=key,
                label=ERS_SERIES[key],
                value=value / 100.0 if unit == "lb" else value,
                source=self.source,
                region="National",
                unit=unit,
                observed_at=stamp,
            ))
        if not observations:
            return ProviderResult(self.name, False, error="no series matched")
        return ProviderResult(self.name, True, observations)


# --------------------------------------------------------------------------
# BLS monthly consumer prices
# --------------------------------------------------------------------------

class BlsProvider:
    """BLS public API, no key required for our volume."""

    name = "BLS"
    source = "BLS"

    def fetch(self) -> ProviderResult:
        observations: list[Observation] = []
        errors: list[str] = []
        for series_id, label in BLS_SERIES.items():
            url = BLS_API_URL.format(series_id=series_id)
            try:
                data = fetch(url)
                payload = json.loads(data.decode("utf-8"))
            except (urllib.error.URLError, OSError, ValueError) as exc:
                errors.append(f"{series_id}: {exc}")
                continue
            series = (payload.get("Results") or {}).get("series") or []
            if not series:
                errors.append(f"{series_id}: no data")
                continue
            points = series[0].get("data") or []
            if not points:
                errors.append(f"{series_id}: empty")
                continue
            point = points[0]
            try:
                value = float(point["value"])
            except (KeyError, TypeError, ValueError):
                errors.append(f"{series_id}: bad value")
                continue
            year = point.get("year", "")
            period = point.get("period", "")
            month = period[1:] if period.startswith("M") else "01"
            observations.append(Observation(
                series_key=f"bls:{series_id}",
                label=label,
                value=value,
                source=self.source,
                region="National",
                unit="lb",
                observed_at=f"{year}-{month}-01",
            ))
        if not observations:
            return ProviderResult(self.name, False, error="; ".join(errors))
        return ProviderResult(self.name, True, observations)


# --------------------------------------------------------------------------
# the engine
# --------------------------------------------------------------------------

PROVIDERS = (Ams3228Provider, ErsProvider, BlsProvider)


def refresh(conn: db.sqlite3.Connection,
            providers: Iterable[Any] | None = None) -> list[ProviderResult]:
    """Fetch every provider and store what came back."""
    results: list[ProviderResult] = []
    for provider in (providers or PROVIDERS):
        try:
            instance = provider() if isinstance(provider, type) else provider
            result = instance.fetch()
        except Exception as exc:  # pragma: no cover - defensive
            result = ProviderResult(getattr(provider, "name", "provider"),
                                    False, error=str(exc))
        results.append(result)
        if not result.ok:
            continue
        for obs in result.observations:
            conn.execute(
                "INSERT INTO market_prices(series_key, label, source, region, "
                "value, unit, observed_at) VALUES(?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(series_key, source, observed_at) DO UPDATE SET "
                "value = excluded.value, label = excluded.label, "
                "region = excluded.region, unit = excluded.unit, "
                "fetched_at = datetime('now')",
                (obs.series_key, obs.label, obs.source, obs.region, obs.value,
                 obs.unit, obs.observed_at),
            )
    conn.commit()
    return results


def latest(conn: db.sqlite3.Connection, series_key: str) -> db.sqlite3.Row | None:
    """The most recent observation for one series."""
    return db.one(conn,
                  "SELECT * FROM market_prices WHERE series_key = ? "
                  "ORDER BY observed_at DESC, fetched_at DESC LIMIT 1",
                  (series_key,))


def latest_many(conn: db.sqlite3.Connection,
                series_keys: Iterable[str]) -> dict[str, db.sqlite3.Row]:
    keys = [k for k in series_keys if k]
    if not keys:
        return {}
    placeholders = ",".join("?" * len(keys))
    rows = db.rows(conn,
                   f"SELECT * FROM market_prices WHERE series_key IN ({placeholders}) "
                   "ORDER BY observed_at DESC", keys)
    out: dict[str, db.sqlite3.Row] = {}
    for row in rows:
        out.setdefault(row["series_key"], row)
    return out


def cut_market_key(cut: db.sqlite3.Row) -> str:
    """Which market series a cut should be measured against."""
    key = (cut["market_series_key"] or "").strip()
    return key


def compare(conn: db.sqlite3.Connection, cut: db.sqlite3.Row) -> dict[str, Any]:
    """Our price against the market benchmark for one cut."""
    key = cut_market_key(cut)
    if not key:
        return {"available": False}
    row = latest(conn, key)
    if row is None:
        return {"available": False, "series_key": key}
    market = float(row["value"])
    ours = float(cut["runchero_price"])
    per_lb_market = market
    per_lb_ours = float(cut["price_per_lb"]) or ours
    delta = per_lb_market - per_lb_ours
    pct = (delta / per_lb_market * 100.0) if per_lb_market else 0.0
    return {
        "available": True,
        "series_key": key,
        "label": row["label"],
        "source": row["source"],
        "region": row["region"],
        "observed_at": row["observed_at"],
        "value": market,
        "our_per_lb": per_lb_ours,
        "delta": delta,
        "pct": pct,
        "under": delta > 0,
        "stale": _is_stale(row["observed_at"]),
    }


def _is_stale(observed_at: str, days: int = 21) -> bool:
    try:
        stamp = _dt.date.fromisoformat((observed_at or "")[:10])
    except ValueError:
        return True
    return (_dt.date.today() - stamp).days > days


def market_table(conn: db.sqlite3.Connection) -> list[db.sqlite3.Row]:
    """Every tracked series with its latest value, for the public table."""
    rows = db.rows(conn, "SELECT * FROM market_prices")
    best: dict[tuple[str, str], db.sqlite3.Row] = {}
    for row in rows:
        key = (row["series_key"], row["source"])
        current = best.get(key)
        if current is None or row["observed_at"] > current["observed_at"]:
            best[key] = row
    return sorted(best.values(),
                  key=lambda r: (r["source"], r["label"]))


def snapshot_for(conn: db.sqlite3.Connection,
                 series_keys: Iterable[str]) -> dict[str, Any]:
    """The market figures behind one order, stored so a later dispute can be
    settled against the numbers the customer actually saw.
    """
    out: dict[str, Any] = {}
    for key, row in latest_many(conn, series_keys).items():
        out[key] = {
            "label": row["label"],
            "value": row["value"],
            "unit": row["unit"],
            "source": row["source"],
            "region": row["region"],
            "observed_at": row["observed_at"],
        }
    return out
