"""Pixel palette - matches Runchero style."""
from __future__ import annotations

PALETTE: dict[str, str] = {
    "ink": "#1b1b23",
    "ink2": "#2f3140",
    "paper": "#fdf6e3",
    "paper2": "#f3e7c8",
    "white": "#ffffff",
    "cream": "#ffe9b0",
    "sky": "#6ab0f3",
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

ICON_LEGEND: dict[str, str] = {
    ".": None,
    "k": "ink", "K": "ink2", "w": "white", "W": "paper",
    "g": "grass", "G": "grass2", "l": "grass3", "b": "sky", "B": "sky2", "n": "navy",
    "r": "tomato", "R": "tomato2", "y": "sun", "Y": "sun2", "o": "orange",
    "N": "soil2", "d": "soil", "s": "silver", "S": "grey2",
    "t": "teal", "T": "teal2", "p": "plum", "c": "cyan", "m": "pink",
}


def rgb(name_or_hex: str):
    if name_or_hex in PALETTE:
        value = PALETTE[name_or_hex]
    elif name_or_hex in ICON_LEGEND.values():
        value = name_or_hex
    else:
        value = name_or_hex
    value = value.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def css_vars() -> str:
    return "\n".join(f"  --{name}: {value};" for name, value in PALETTE.items())
