"""Payments. A mock provider keeps the demo fully offline; the Stripe
provider sits behind the same interface and calls Stripe's REST API over
urllib, so no SDK ever needs installing."""
from __future__ import annotations

import json
import secrets
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from .. import config


@dataclass
class ChargeResult:
    ok: bool
    reference: str = ""
    error: str = ""
    raw: dict[str, Any] | None = None


class PaymentProvider:
    name = "base"

    def charge(self, amount: float, description: str,
               details: dict[str, Any]) -> ChargeResult:  # pragma: no cover
        raise NotImplementedError


class MockProvider(PaymentProvider):
    """Approves everything, records a fake reference. Demo mode."""

    name = "mock"

    def charge(self, amount: float, description: str,
               details: dict[str, Any]) -> ChargeResult:
        reference = f"mock_{secrets.token_hex(8)}"
        return ChargeResult(True, reference=reference,
                            raw={"amount": amount,
                                 "description": description,
                                 "last4": (details.get("card") or "")[-4:]})


class StripeProvider(PaymentProvider):
    """Stripe PaymentIntents over the REST API, urllib only."""

    name = "stripe"
    endpoint = "https://api.stripe.com/v1/payment_intents"

    def __init__(self, secret_key: str = ""):
        self.secret_key = secret_key or config.STRIPE_SECRET_KEY

    def charge(self, amount: float, description: str,
               details: dict[str, Any]) -> ChargeResult:
        if not self.secret_key:
            return ChargeResult(False, error="Stripe is not configured.")
        body = {
            "amount": int(round(amount * 100)),
            "currency": config.CURRENCY,
            "description": description,
            "confirm": "true",
            "payment_method": details.get("payment_method", ""),
            "automatic_payment_methods[enabled]": "true",
        }
        data = "&".join(f"{key}={value}" for key, value in body.items()
                        if value).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint, data=data, method="POST",
            headers={
                "Authorization": f"Bearer {self.secret_key}",
                "User-Agent": config.USER_AGENT,
                "Content-Type": "application/x-www-form-urlencoded",
            })
        try:
            with urllib.request.urlopen(request, timeout=config.HTTP_TIMEOUT) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            try:
                payload = json.loads(exc.read().decode("utf-8"))
                message = (payload.get("error") or {}).get("message", str(exc))
            except (ValueError, UnicodeDecodeError):
                message = str(exc)
            return ChargeResult(False, error=message, raw=payload)
        except (urllib.error.URLError, OSError) as exc:
            return ChargeResult(False, error=str(exc))
        return ChargeResult(True, reference=payload.get("id", ""),
                            raw=payload)


def provider() -> PaymentProvider:
    if config.PAYMENT_PROVIDER == "stripe":
        return StripeProvider()
    return MockProvider()
