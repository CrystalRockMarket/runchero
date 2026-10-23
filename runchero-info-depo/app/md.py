"""A small, safe Markdown renderer.

The community articles are written in Markdown by people who are thinking about
tractors, not about HTML. This supports the subset that actually shows up in
farm notes:

* headings, paragraphs, lists, block quotes, rules
* fenced code blocks and inline code
* **bold**, *italic*
* tables
* `[text](url)` links (only safe schemes survive)
* `[[wiki-slug]]` cross references between articles

Everything is HTML-escaped before any markup is produced, so article bodies
cannot inject scripts. There is no raw-HTML passthrough.
"""
from __future__ import annotations

import html
import re
from typing import Callable

Resolver = Callable[[str], tuple[str, str] | None]

SAFE_SCHEMES = ("http://", "https://", "mailto:", "/", "#")


def _safe_url(url: str) -> str | None:
    url = url.strip()
    lowered = url.lower()
    if lowered.startswith(SAFE_SCHEMES):
        return url
    if ":" not in url:
        return url  # relative
    return None


def _inline(text: str, resolver: Resolver | None) -> str:
    # Protect code spans first so their contents are never re-parsed.
    stash: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        stash.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00{len(stash) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash_code, text)

    def wiki(match: re.Match[str]) -> str:
        inner = match.group(1)
        if "|" in inner:
            slug, label = inner.split("|", 1)
        else:
            slug, label = inner, inner
        slug = slug.strip()
        label = label.strip()
        if resolver:
            found = resolver(slug)
            if found:
                url, resolved_label = found
                label = label if label != slug else resolved_label
                return f'<a class="wikilink" href="{html.escape(url)}">{html.escape(label)}</a>'
        return f'<span class="wikilink missing">[{html.escape(label)}]</span>'

    text = re.sub(r"\[\[([^\]]+)\]\]", wiki, text)

    def link(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2)
        safe = _safe_url(url)
        if not safe:
            return html.escape(label)
        external = safe.startswith("http")
        attrs = ' rel="noopener noreferrer" target="_blank"' if external else ""
        return f'<a href="{html.escape(safe)}"{attrs}>{label}</a>'

    # links: [label](url) - label may already contain escaped entities
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+)_(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)

    # restore code spans
    text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text


def _table(rows: list[list[str]], resolver: Resolver | None) -> str:
    if not rows:
        return ""
    def cell(value: str, tag: str) -> str:
        return f"<{tag}>{_inline(value.strip(), resolver)}</{tag}>"

    head, *body = rows
    out = ["<table class='md-table'><thead><tr>"]
    out += [cell(c, "th") for c in head]
    out.append("</tr></thead><tbody>")
    for line in body:
        out.append("<tr>")
        out += [cell(c, "td") for c in line]
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render(text: str, resolver: Resolver | None = None) -> str:
    """Render Markdown to a safe HTML fragment."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # fenced code
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            i += 1
            code: list[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            cls = f" class=\"lang-{html.escape(lang)}\"" if lang else ""
            body = html.escape("\n".join(code))
            out.append(f"<pre{cls}><code>{body}</code></pre>")
            continue

        # blank
        if not line.strip():
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"\s*([-*_])\1{2,}\s*", line):
            out.append("<hr>")
            i += 1
            continue

        # heading
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            level = min(len(heading.group(1)), 6)
            out.append(f"<h{level}>{_inline(heading.group(2).strip(), resolver)}</h{level}>")
            i += 1
            continue

        # table
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:\-|]+\|[\s:\-|]*$", lines[i + 1]):
            table_rows: list[list[str]] = []
            def split_row(raw: str) -> list[str]:
                raw = raw.strip()
                if raw.startswith("|"):
                    raw = raw[1:]
                if raw.endswith("|"):
                    raw = raw[:-1]
                return [c for c in raw.split("|")]
            table_rows.append(split_row(line))
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                table_rows.append(split_row(lines[i]))
                i += 1
            out.append(_table(table_rows, resolver))
            continue

        # block quote
        if line.lstrip().startswith(">"):
            quote: list[str] = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = render("\n".join(quote), resolver)
            out.append(f"<blockquote>{inner}</blockquote>")
            continue

        # lists
        bullet = re.match(r"^\s*[-*+]\s+(.*)$", line)
        ordered = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        if bullet or ordered:
            tag = "ul" if bullet else "ol"
            items: list[str] = []
            while i < n:
                m_bullet = re.match(r"^\s*[-*+]\s+(.*)$", lines[i])
                m_ordered = re.match(r"^\s*\d+[.)]\s+(.*)$", lines[i])
                if bullet and not m_bullet:
                    if m_ordered:
                        break
                    if lines[i].strip() and lines[i].startswith("  "):
                        if items:
                            items[-1] += " " + lines[i].strip()
                        i += 1
                        continue
                    break
                if ordered and not m_ordered:
                    if m_bullet:
                        break
                    if lines[i].strip() and lines[i].startswith("  "):
                        if items:
                            items[-1] += " " + lines[i].strip()
                        i += 1
                        continue
                    break
                value = (m_bullet or m_ordered).group(1)  # type: ignore[union-attr]
                items.append(value)
                i += 1
            out.append(f"<{tag}>" + "".join(
                f"<li>{_inline(item, resolver)}</li>" for item in items) + f"</{tag}>")
            continue

        # paragraph
        para: list[str] = []
        while i < n and lines[i].strip():
            nxt = lines[i]
            if (nxt.lstrip().startswith(">") or nxt.strip().startswith("```")
                    or re.match(r"^\s*[-*+]\s+", nxt) or re.match(r"^\s*\d+[.)]\s+", nxt)
                    or re.match(r"^#{1,6}\s+", nxt)):
                break
            para.append(nxt.strip())
            i += 1
        if para:
            out.append(f"<p>{_inline(' '.join(para), resolver)}</p>")

    return "\n".join(out)


def excerpt(text: str, length: int = 180) -> str:
    """Plain-text summary of a Markdown body."""
    stripped = re.sub(r"```.*?```", " ", text, flags=re.S)
    stripped = re.sub(r"[#*_>`\[\]()]", " ", stripped)
    stripped = re.sub(r"\s+", " ", stripped).strip()
    return stripped[:length].rsplit(" ", 1)[0] + "..." if len(stripped) > length else stripped


def snippet(text: str, resolver: Resolver | None = None) -> str:
    """Render a search snippet.

    FTS5 marks the words it matched with control characters. Those markers can
    land inside a ``[[wiki-slug]]``, which would break the link, so they are
    taken out of the links first and turned into bold tags afterwards.
    """
    def clean(match: re.Match[str]) -> str:
        return match.group(0).replace("\x01", "").replace("\x02", "")

    text = re.sub(r"\[\[[^\]]+\]\]", clean, text)
    out = render(text, resolver)
    return out.replace("\x01", "<b>").replace("\x02", "</b>")
