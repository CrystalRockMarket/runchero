"""Customer accounts: sign up, sign in, profile, preferences, order history.

Demo note: there is no mailer wired up yet. Sign-up and email changes mark the
address verified immediately and say so on screen, instead of sending a
confirmation link. The schema and the service keep the verified flag so a real
mailer can be dropped in later without changing the account pages.
"""
from __future__ import annotations

import re
import time
from urllib.parse import quote

from .. import db, web
from ..services import customers
from ..services import fulfillment
from . import cart_count, flash, page_context, redirect

_DAY_CHOICES = list(range(1, 29))


def register(add) -> None:
    add("GET", re.compile(r"^/account$"), dashboard)
    add("GET", re.compile(r"^/account/login$"), login_form)
    add("POST", re.compile(r"^/account/login$"), login_submit)
    add("GET", re.compile(r"^/account/signup$"), signup_form)
    add("POST", re.compile(r"^/account/signup$"), signup_submit)
    add("POST", re.compile(r"^/account/logout$"), logout)
    add("GET", re.compile(r"^/account/orders$"), order_history)
    add("GET", re.compile(r"^/account/profile$"), profile)
    add("POST", re.compile(r"^/account/profile$"), profile_submit)
    add("GET", re.compile(r"^/account/password$"), password)
    add("POST", re.compile(r"^/account/password$"), password_submit)
    add("GET", re.compile(r"^/account/preferences$"), preferences)
    add("POST", re.compile(r"^/account/preferences$"), preferences_submit)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _safe_next(value: str | None, default: str = "/account") -> str:
    value = (value or "").strip()
    if (value.startswith("/") and not value.startswith("//")
            and not value.startswith("/\\")):
        return value
    return default


def _login_redirect(req) -> str:
    return "/account/login?next=" + quote(req.path, safe="/")


def _account_context(conn, req, customer, **extra):
    extra.setdefault("errors", {})
    return page_context(
        conn, req, customer=customer, csrf=req.csrf_token(),
        cart_count=cart_count(conn, req), **extra)


def _guard(conn, req):
    customer = customers.current(conn, req)
    if customer is None:
        return None, redirect(_login_redirect(req))
    return customer, None


def _start_session(req, customer) -> None:
    # A fresh CSRF token on sign-in, so a token minted before login cannot be
    # reused afterwards.
    req.session_pop("_csrf")
    req.session_set("customer_id", customer["id"])


# --------------------------------------------------------------------------
# sign in / sign up / sign out
# --------------------------------------------------------------------------

def login_form(conn, req, **_):
    if customers.current(conn, req) is not None:
        return redirect("/account")
    nxt = _safe_next(req.query.get("next"))
    context = _account_context(
        conn, req, None, next=nxt, email="",
        demo=True)
    return 200, "text/html; charset=utf-8", web.render("account_login.html",
                                                       **context)


def login_submit(conn, req, **_):
    if not req.csrf_ok():
        return redirect("/account/login")
    email = customers.normalise_email(req.form.get("email") or "")
    password = req.form.get("password") or ""
    nxt = _safe_next(req.form.get("next"))
    row = customers.authenticate(conn, email, password)
    if row is None:
        time.sleep(0.3)
        context = _account_context(
            conn, req, None, next=nxt, email=email,
            errors={"login": "That email and password do not match."},
            demo=True)
        return 200, "text/html; charset=utf-8", web.render("account_login.html",
                                                           **context)
    _start_session(req, row)
    flash(req, f"Welcome back, {row['name'].split()[0] or 'friend'}.", "ok")
    return redirect(nxt)


def signup_form(conn, req, **_):
    if customers.current(conn, req) is not None:
        return redirect("/account")
    context = _account_context(conn, req, None, values={}, demo=True)
    return 200, "text/html; charset=utf-8", web.render("account_signup.html",
                                                       **context)


def signup_submit(conn, req, **_):
    if not req.csrf_ok():
        return redirect("/account/signup")
    form = req.form
    values = {
        "name": (form.get("name") or "").strip(),
        "email": customers.normalise_email(form.get("email") or ""),
        "phone": (form.get("phone") or "").strip(),
        "market_updates": form.get("market_updates") == "on",
    }
    errors: dict[str, str] = {}
    password = form.get("password") or ""
    confirm = form.get("password2") or ""

    if len(values["name"]) < 2:
        errors["name"] = "Tell us your name."
    if not customers.email_ok(values["email"]):
        errors["email"] = "That does not look like an email address."
    elif customers.by_email(conn, values["email"]) is not None:
        errors["email"] = ("An account already uses that email. "
                           "Try signing in instead.")
    if len(password) < customers.MIN_PASSWORD:
        errors["password"] = (f"Use at least {customers.MIN_PASSWORD} "
                              "characters.")
    if password != confirm:
        errors["password2"] = "The two passwords do not match."
    if values["phone"] and len(values["phone"]) < 7:
        errors["phone"] = "That phone number looks too short."

    if errors:
        context = _account_context(conn, req, None, values=values,
                                   errors=errors, demo=True)
        return 200, "text/html; charset=utf-8", web.render(
            "account_signup.html", **context)

    row = customers.create(
        conn, email=values["email"], password=password,
        name=values["name"], phone=values["phone"], verify=True)
    if values["market_updates"]:
        conn.execute("UPDATE customers SET market_updates = 1 WHERE id = ?",
                     (row["id"],))
        conn.commit()
        row = customers.by_id(conn, row["id"])
    _start_session(req, row)
    flash(req, "Account created. Demo mode: no email was sent, so your "
               "address is marked verified.", "ok")
    return redirect("/account")


def logout(conn, req, **_):
    if req.csrf_ok():
        req.session_pop("customer_id")
        req.session_pop("_csrf")
        flash(req, "Signed out.", "ok")
    return redirect("/")


# --------------------------------------------------------------------------
# dashboard and order history
# --------------------------------------------------------------------------

def dashboard(conn, req, **_):
    customer, denied = _guard(conn, req)
    if denied:
        return denied
    recent = customers.orders_for(conn, customer, limit=5)
    stats = customers.order_stats(conn, customer)
    subscriber = customers.subscriber_for(conn, customer)
    context = _account_context(
        conn, req, customer, recent_orders=recent, stats=stats,
        subscriber=subscriber, prefs=_prefs(conn, customer))
    return 200, "text/html; charset=utf-8", web.render("account.html",
                                                       **context)


def order_history(conn, req, **_):
    customer, denied = _guard(conn, req)
    if denied:
        return denied
    orders = customers.orders_for(conn, customer)
    stats = customers.order_stats(conn, customer)
    context = _account_context(conn, req, customer, orders=orders,
                               stats=stats)
    return 200, "text/html; charset=utf-8", web.render("account_orders.html",
                                                       **context)


# --------------------------------------------------------------------------
# profile, password, preferences
# --------------------------------------------------------------------------

def profile(conn, req, **_):
    customer, denied = _guard(conn, req)
    if denied:
        return denied
    context = _account_context(conn, req, customer, values=_profile_values(customer))
    return 200, "text/html; charset=utf-8", web.render("account_profile.html",
                                                       **context)


def _profile_values(customer) -> dict[str, str]:
    return {
        "name": customer["name"],
        "email": customer["email"],
        "phone": customer["phone"],
    }


def profile_submit(conn, req, **_):
    customer, denied = _guard(conn, req)
    if denied:
        return denied
    if not req.csrf_ok():
        return redirect("/account/profile")
    form = req.form
    values = {
        "name": (form.get("name") or "").strip(),
        "email": customers.normalise_email(form.get("email") or ""),
        "phone": (form.get("phone") or "").strip(),
    }
    errors: dict[str, str] = {}
    email_changed = values["email"] != customer["email"]

    if len(values["name"]) < 2:
        errors["name"] = "Tell us your name."
    if not customers.email_ok(values["email"]):
        errors["email"] = "That does not look like an email address."
    elif email_changed and customers.by_email(conn, values["email"]) is not None:
        errors["email"] = "Another account already uses that email."
    if values["phone"] and len(values["phone"]) < 7:
        errors["phone"] = "That phone number looks too short."

    current_password = form.get("current_password") or ""
    if email_changed:
        from ..services import auth
        if not auth.check_password(current_password, customer["passhash"]):
            errors["current_password"] = ("Confirm your current password to "
                                          "change your email.")

    if errors:
        context = _account_context(conn, req, customer, values=values,
                                   errors=errors)
        return 200, "text/html; charset=utf-8", web.render(
            "account_profile.html", **context)

    customers.update_profile(conn, customer["id"], name=values["name"],
                             phone=values["phone"])
    if email_changed:
        customers.update_email(conn, customer["id"], values["email"],
                               verify=True)
        flash(req, "Profile saved. Demo mode: your new email is marked "
                   "verified, with no confirmation message sent.", "ok")
    else:
        flash(req, "Profile saved.", "ok")
    return redirect("/account/profile")


def password(conn, req, **_):
    customer, denied = _guard(conn, req)
    if denied:
        return denied
    context = _account_context(conn, req, customer)
    return 200, "text/html; charset=utf-8", web.render("account_password.html",
                                                       **context)


def password_submit(conn, req, **_):
    customer, denied = _guard(conn, req)
    if denied:
        return denied
    if not req.csrf_ok():
        return redirect("/account/password")
    from ..services import auth
    form = req.form
    current = form.get("current_password") or ""
    new = form.get("password") or ""
    confirm = form.get("password2") or ""
    errors: dict[str, str] = {}

    if not auth.check_password(current, customer["passhash"]):
        errors["current_password"] = "That is not your current password."
    if len(new) < customers.MIN_PASSWORD:
        errors["password"] = f"Use at least {customers.MIN_PASSWORD} characters."
    if new != confirm:
        errors["password2"] = "The two passwords do not match."
    if new and current and new == current:
        errors["password"] = "Choose a password you have not used here before."

    if errors:
        context = _account_context(conn, req, customer, errors=errors)
        return 200, "text/html; charset=utf-8", web.render(
            "account_password.html", **context)

    customers.change_password(conn, customer["id"], new)
    flash(req, "Password changed.", "ok")
    return redirect("/account")


def _prefs(conn, customer) -> dict[str, object]:
    address = customers.address(conn, customer)
    return {
        "fulfillment": customer["fulfillment"],
        "line1": address["line1"], "line2": address["line2"],
        "city": address["city"], "state": address["state"],
        "zip": address["zip"], "county": customer["county"],
        "delivery_notes": customer["delivery_notes"],
        "recurring_day": customer["recurring_day"],
        "contact_method": customer["contact_method"],
        "market_updates": bool(customer["market_updates"]),
    }


def preferences(conn, req, **_):
    customer, denied = _guard(conn, req)
    if denied:
        return denied
    context = _account_context(
        conn, req, customer, values=_prefs(conn, customer),
        days=_DAY_CHOICES, counties=fulfillment.DELIVERY_COUNTIES,
        contact_methods=customers.CONTACT_METHODS)
    return 200, "text/html; charset=utf-8", web.render(
        "account_preferences.html", **context)


def preferences_submit(conn, req, **_):
    customer, denied = _guard(conn, req)
    if denied:
        return denied
    if not req.csrf_ok():
        return redirect("/account/preferences")
    form = req.form
    values = {
        "fulfillment": form.get("fulfillment") or "pickup",
        "line1": (form.get("line1") or "").strip(),
        "line2": (form.get("line2") or "").strip(),
        "city": (form.get("city") or "").strip(),
        "state": (form.get("state") or "KY").strip().upper(),
        "zip": (form.get("zip") or "").strip(),
        "county": (form.get("county") or "").strip().title(),
        "delivery_notes": (form.get("delivery_notes") or "").strip(),
        "recurring_day": 0,
        "contact_method": form.get("contact_method") or "email",
        "market_updates": form.get("market_updates") == "on",
    }
    try:
        values["recurring_day"] = int(form.get("recurring_day") or 0)
    except ValueError:
        values["recurring_day"] = -1
    errors: dict[str, str] = {}

    if values["fulfillment"] not in customers.FULFILLMENT_KINDS:
        errors["fulfillment"] = "Choose pickup or delivery."
    if values["contact_method"] not in customers.CONTACT_METHODS:
        errors["contact_method"] = "Choose how we should reach you."
    if not 0 <= values["recurring_day"] <= 28:
        errors["recurring_day"] = "Pick a day from 1 to 28, or no preference."

    if values["fulfillment"] == "delivery":
        if len(values["line1"]) < 4:
            errors["line1"] = "We need a street address to deliver."
        if len(values["city"]) < 2:
            errors["city"] = "Which town?"
        if not re.match(r"^\d{5}$", values["zip"]):
            errors["zip"] = "A five digit ZIP, please."
        if not values["county"]:
            errors["county"] = "Choose the county we deliver to."
        elif not fulfillment.county_allowed(values["county"]):
            errors["county"] = ("We deliver to " +
                                ", ".join(fulfillment.DELIVERY_COUNTIES) +
                                " counties.")

    if errors:
        context = _account_context(
            conn, req, customer, values=values, errors=errors,
            days=_DAY_CHOICES, counties=fulfillment.DELIVERY_COUNTIES,
            contact_methods=customers.CONTACT_METHODS)
        return 200, "text/html; charset=utf-8", web.render(
            "account_preferences.html", **context)

    customers.save_preferences(
        conn, customer["id"], fulfillment=values["fulfillment"],
        address={"line1": values["line1"], "line2": values["line2"],
                 "city": values["city"], "state": values["state"],
                 "zip": values["zip"]},
        county=values["county"], delivery_notes=values["delivery_notes"],
        recurring_day=values["recurring_day"],
        contact_method=values["contact_method"],
        market_updates=values["market_updates"])
    flash(req, "Preferences saved.", "ok")
    return redirect("/account/preferences")
