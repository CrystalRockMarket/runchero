"""The Runchero palette.

One shared colour table used by three consumers:

* the CSS theme (generated into ``static/css/pixel.css`` by tools/build_assets.py)
* the pixel art renderer (PIL)
* the seed data (book cover palettes, section accents)

Colours are deliberately saturated and limited: a 32-colour "video game" ramp
that reads well on a cheap panel in a barn, at night, with the sun low.
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
    # meat. raw beef is a deep red with cream fat and pale bone. these are
    # used by the cut sprites so a steak looks like a steak.
    "meat": "#a3272f",      # raw beef, the main muscle colour
    "meat2": "#6b1622",     # shadowed edge, cooked crust, liver
    "meat3": "#c9504f",     # marbling, ground beef, lighter muscle
    "fat": "#f0dfba",       # fat cap, tallow, cream
    "bone": "#ece0c6",      # bone
    "marrow": "#d8a441",    # marrow, suet in the light
    "cured": "#bf6274",     # cured and smoked meat
    "crust": "#7a3a1e",     # smoked crust, jerky, bologna
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
    # meat sprites
    "M": "meat",      # raw beef muscle
    "A": "meat2",     # dark edge, cooked crust, liver
    "H": "meat3",     # marbling, lighter muscle
    "F": "fat",       # fat cap and tallow
    "B": "bone",      # bone
    "E": "marrow",    # marrow
    "U": "cured",     # cured and smoked
    "Q": "crust",     # smoked crust, jerky
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
    return "\n".join(f"  --{name}: {value};" for name, value in PALETTE.items())
