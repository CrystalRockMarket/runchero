#!/usr/bin/env python3
"""Daily market price refresh, plus the slot calendar top-up.

Cron line:

    17 6 * * *  cd /home/barn/projects/runchero-shop && \
        python3 app/jobs/market_daily.py >> /home/barn/logs/market-job.log 2>&1
"""
from __future__ import annotations

import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app import config, db  # noqa: E402
from app.services import fulfillment, market  # noqa: E402


def main() -> int:
    config.ensure_dirs()
    with db.session() as conn:
        results = market.refresh(conn)
        slots = fulfillment.ensure_slots(conn)
        for result in results:
            if result.ok:
                print(f"{result.provider}: {len(result.observations)} series")
            else:
                print(f"{result.provider}: unavailable ({result.error})")
        print(f"slots: {slots} new windows opened")
        # Keep the promise honest after every refresh: anything that drifted
        # above its benchmark gets flagged for the owner.
        from app.services import pricing
        flagged = pricing.claim_integrity(conn)
        print(f"claim integrity: {len(flagged)} cuts at or above market")
        if flagged:
            for cut in flagged:
                print(f"  over market: {cut['name']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)
