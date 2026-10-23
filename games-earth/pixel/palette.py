"""The games directory palette.

One shared colour table used by three consumers:

* the CSS theme (generated into ``_WEB/_STYLES/EL_SS_PIXEL.css`` by
  tools/build_assets.py)
* the pixel art renderer (PIL)
* the seed data (game category accents)

The colours are deliberately saturated and limited: a 29-colour "video game"
ramp that reads well on a cheap panel in a barn, at night, with the sun low.
``ink`` and ``ink2`` carry the dark arcade chrome, ``paper``/``paper2`` carry
the light read-aloud surfaces.
"""
from __future__ import annotations

# Key -> (hex, css-name)
PALETTE: dict[str, str] = {
    "ink": "#1b1b23",        # near black, outlines
    "ink2": "#2f3140",       # soft dark, secondary text
    "paper": "#fdf6e3",      # cream page
    "paper2": "#f3e7c8",     # cream page, shaded
    "white": "#ffffff",
    "cream": "#ffe9b0",
    "sky": "#6ab0f3",        # blue
    "sky2": "#3f7fd6",
    "navy": "#24427a",
    "grass": "#6cc24a",
    "grass2": "#3f8f2f",
    "grass3": "#8fdc6a",
    "soil": "#8a5a34",
    "soil2": "#5c3a1e",
    "sun": "#ffd24a",
    "sun2": "#f0a92e",
    "tomato": "#e04b4b",
    "tomato2": "#a32e2e",
    "orange": "#f0902e",
    "brown": "#a8763f",
    "wood": "#b9834f",
    "silver": "#c3ccd8",
    "grey": "#8a94a6",
    "grey2": "#5b6474",
    "teal": "#3fc4b0",
    "teal2": "#2a8d80",
    "plum": "#9b4dab",
    "pink": "#f28ab2",
    "cyan": "#57c7d4",
}

#: Mini palette used by the pixel icons. Keys are the single characters used
#: inside the icon maps, values are palette names.
ICON_LEGEND: dict[str, str] = {
    ".": None,          # transparent
    "k": "ink",         # outline
    "K": "ink2",
    "w": "white",
    "W": "paper",
    "g": "grass",
    "G": "grass2",
    "l": "grass3",
    "b": "sky",
    "B": "sky2",
    "n": "navy",
    "r": "tomato",
    "R": "tomato2",
    "y": "sun",
    "Y": "sun2",
    "o": "orange",
    "N": "soil2",
    "d": "soil",
    "s": "silver",
    "S": "grey2",
    "t": "teal",
    "T": "teal2",
    "p": "plum",
    "c": "cyan",
    "m": "pink",
}


def rgb(name_or_hex: str) -> tuple[int, int, int]:
    """Resolve a palette name or literal hex into an RGB tuple."""
    if name_or_hex in PALETTE:
        value = PALETTE[name_or_hex]
    elif name_or_hex in ICON_LEGEND.values():
        value = name_or_hex
    else:
        value = name_or_hex
    value = value.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def shade(colour: str, factor: float) -> str:
    """Darken (factor < 1) or lighten (factor > 1) a palette colour."""
    r, g, b = rgb(colour)
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return f"#{r:02x}{g:02x}{b:02x}"


def mix(colour_a: str, colour_b: str, t: float) -> str:
    """Blend two palette colours, t=0 gives a, t=1 gives b."""
    ra, ga, ba = rgb(colour_a)
    rb, gb, bb = rgb(colour_b)
    return "#{:02x}{:02x}{:02x}".format(
        int(ra + (rb - ra) * t),
        int(ga + (gb - ga) * t),
        int(ba + (bb - ba) * t),
    )


def css_vars() -> str:
    """Emit the palette as CSS custom properties, grouped and commented."""
    lines = []
    for name, value in PALETTE.items():
        lines.append(f"  --px-{name}: {value};")
    return "\n".join(lines)


#: Semantic aliases the templates and CSS use instead of raw palette names.
#: Kept here so art and stylesheet can never drift apart.
SEMANTIC: dict[str, str] = {
    "bg": "ink",
    "bg-alt": "ink2",
    "surface": "paper",
    "surface-alt": "paper2",
    "text": "ink",
    "text-muted": "ink2",
    "text-invert": "paper",
    "accent": "sun",
    "accent-2": "tomato",
    "accent-3": "teal",
    "accent-4": "sky",
    "accent-5": "plum",
    "line": "ink",
}


def semantic_vars() -> str:
    """Emit the semantic aliases as CSS custom properties."""
    return "\n".join(
        f"  --px-{alias}: var(--px-{palette_name});"
        for alias, palette_name in SEMANTIC.items()
    )
