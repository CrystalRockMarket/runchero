"""Pixel art for every cut of beef.

The shop needs each cut to be recognisable at 16 pixels: a shopper scans a
grid of 76 items and has to tell a ribeye from a brisket at a glance. That
means the silhouette has to carry the cut (a bone-in ribeye has a bone, a
flank is a thin wedge, a brisket flat is a wide slab) and the colour has to
carry the material (dark red muscle, cream fat, pale bone).

So the sprites are built rather than typed by hand. A tiny character grid
acts as the canvas, and each cut is described as a set of shapes: an ellipse
for a round steak, a bar for a bone, a wedge for a flank, a fat cap for a
picanha. The grid is then outlined in ink and marbled, the way real muscle
is flecked with fat.

Every sprite is 16x16 and uses the shared palette in ``app/palette.py``.
"""
from __future__ import annotations

import random

SIZE = 16

# Palette characters used here.
MEAT = "M"      # muscle
DARK = "A"      # shadowed muscle, cooked edge, liver
LIGHT = "H"     # marbling, lighter muscle
FAT = "F"       # fat cap, tallow
BONE = "B"      # bone
MARROW = "E"    # marrow
CURED = "U"     # cured and smoked meat
CRUST = "Q"     # smoked crust, jerky
INK = "k"       # outline


class Grid:
    """A character grid to draw a sprite on."""

    def __init__(self, size: int = SIZE) -> None:
        self.size = size
        self.px: list[list[str]] = [["." for _ in range(size)]
                                     for _ in range(size)]

    # -- basics ---------------------------------------------------------
    def get(self, x: int, y: int) -> str:
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.px[y][x]
        return "."

    def set(self, x: int, y: int, ch: str) -> None:
        if 0 <= x < self.size and 0 <= y < self.size:
            self.px[y][x] = ch

    def rect(self, x: int, y: int, w: int, h: int, ch: str) -> None:
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, ch)

    def ellipse(self, cx: float, cy: float, rx: float, ry: float,
                ch: str) -> None:
        for y in range(self.size):
            for x in range(self.size):
                dx = (x + 0.5 - cx) / rx
                dy = (y + 0.5 - cy) / ry
                if dx * dx + dy * dy <= 1.0:
                    self.set(x, y, ch)

    def poly(self, points: list[tuple[float, float]], ch: str) -> None:
        """Fill a polygon using a scanline test."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(max(0, int(min(ys))), min(self.size,
                                                 int(max(ys)) + 1)):
            centre = y + 0.5
            xs: list[float] = []
            for i in range(len(points)):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % len(points)]
                if (y0 <= centre < y1) or (y1 <= centre < y0):
                    xs.append(x0 + (centre - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(round(xs[i])), int(round(xs[i + 1]))):
                    self.set(x, y, ch)

    def line(self, x0: int, y0: int, x1: int, y1: int, ch: str) -> None:
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, ch)
            if x0 == x1 and y0 == y1:
                break
            err2 = 2 * err
            if err2 > -dy:
                err -= dy
                x0 += sx
            if err2 < dx:
                err += dx
                y0 += sy

    # -- finishing ------------------------------------------------------
    def outline(self, ch: str = INK) -> None:
        """Put an outline around every filled area."""
        add: list[tuple[int, int]] = []
        for y in range(self.size):
            for x in range(self.size):
                if self.get(x, y) != ".":
                    continue
                if (self.get(x - 1, y) != "." or self.get(x + 1, y) != "."
                        or self.get(x, y - 1) != "." or self.get(x, y + 1) != "."):
                    add.append((x, y))
        for x, y in add:
            self.set(x, y, ch)

    def marble(self, count: int = 6, seed: int = 1,
               ch: str | tuple[str, ...] = ()) -> None:
        """Fleck the muscle with fat, the way real beef is marbled."""
        rnd = random.Random(seed)
        colours = (LIGHT, FAT) if not ch else ((ch,) if isinstance(ch, str)
                                               else tuple(ch))
        placed = 0
        tries = 0
        while placed < count and tries < 400:
            tries += 1
            x = rnd.randrange(1, self.size - 1)
            y = rnd.randrange(1, self.size - 1)
            if self.get(x, y) != MEAT:
                continue
            self.set(x, y, rnd.choice(colours))
            placed += 1

    def shade(self, ch: str = DARK) -> None:
        """Darken the lower right edge, so the shape reads as solid."""
        for y in range(self.size):
            for x in range(self.size):
                if self.get(x, y) in (MEAT, LIGHT):
                    if (self.get(x + 1, y) == "." or self.get(x, y + 1) == "."
                            or self.get(x + 1, y + 1) == "."):
                        self.set(x, y, ch)

    def top_fat(self, ch: str = FAT) -> None:
        """A fat cap along the top edge of the shape."""
        for x in range(self.size):
            for y in range(self.size):
                if self.get(x, y) == MEAT and self.get(x, y - 1) == ".":
                    self.set(x, y, ch)
                    break

    def bottom_fat(self, ch: str = FAT) -> None:
        for x in range(self.size):
            for y in range(self.size - 1, -1, -1):
                if self.get(x, y) == MEAT and self.get(x, y + 1) == ".":
                    self.set(x, y, ch)
                    break

    def rows(self) -> tuple[str, ...]:
        return tuple("".join(row) for row in self.px)


# ---------------------------------------------------------------------------
# building blocks
# ---------------------------------------------------------------------------
def _bone_bar(g: Grid, x0: int, x1: int, y: int, thick: int = 2,
              marrow: bool = False) -> None:
    """A length of bone with knobs at each end."""
    g.rect(x0, y, x1 - x0 + 1, thick, BONE)
    g.ellipse(x0, y + thick / 2 - 0.5, 1.6, thick / 2 + 0.6, BONE)
    g.ellipse(x1, y + thick / 2 - 0.5, 1.6, thick / 2 + 0.6, BONE)
    if marrow:
        g.rect(x0 + 2, y, x1 - x0 - 3, thick, MARROW)


def _steak(g: Grid, x0: int, y0: int, w: int, h: int) -> None:
    """A slab of meat with a rounded corner, the base of most cuts."""
    g.rect(x0, y0, w, h, MEAT)
    g.ellipse(x0 + h / 2 - 0.5, y0 + h / 2 - 0.5, h / 2, h / 2, MEAT)
    g.ellipse(x0 + w - h / 2 - 0.5, y0 + h / 2 - 0.5, h / 2, h / 2, MEAT)


def _tbone_shape(g: Grid, cx: int, top: int, bottom: int,
                 spread: int) -> None:
    """A T shaped bone, for t-bone and porterhouse."""
    g.rect(cx, top, 2, bottom - top + 1, BONE)
    g.rect(cx - spread, bottom - 1, spread * 2 + 2, 2, BONE)
    g.ellipse(cx - spread, bottom, 1.6, 1.6, BONE)
    g.ellipse(cx + spread + 1, bottom, 1.6, 1.6, BONE)
    g.ellipse(cx, top, 1.8, 1.8, BONE)


def _ribs(g: Grid, count: int, y0: int, step: int) -> None:
    """Curved rib bones, cut side by side."""
    for i in range(count):
        x = 2 + i * 4
        y = y0 + i % 2
        g.line(x, y + 3, x + 2, y, BONE)
        g.line(x + 2, y, x + 4, y + 3, BONE)
        g.rect(x, y + 3, 4, 2, MEAT)
        g.set(x + 1, y + 3, FAT)


def _chunks(g: Grid, spots: list[tuple[int, int, int, int]],
            ch: str = MEAT) -> None:
    for x, y, w, h in spots:
        g.rect(x, y, w, h, ch)
        g.rect(x, y, w, 1, LIGHT)


def _roll(g: Grid, x0: int, y0: int, w: int, h: int, tie: int = 2) -> None:
    """A tied roast: a rounded log with strings of fat across it."""
    g.ellipse(x0 + w / 2 - 0.5, y0 + h / 2 - 0.5, w / 2, h / 2, MEAT)
    g.rect(x0, y0, w, h, MEAT)
    for i in range(tie):
        x = x0 + 2 + i * max(2, (w - 4) // max(1, tie))
        g.rect(x, y0, 1, h, FAT)


# ---------------------------------------------------------------------------
# the cuts
# ---------------------------------------------------------------------------
def _ribeye() -> Grid:
    g = Grid()
    g.ellipse(8, 9.5, 6, 4.5, MEAT)
    g.top_fat()
    g.marble(9, 3)
    _bone_bar(g, 4, 12, 2, 2)
    g.outline()
    return g


def _ribeye_boneless() -> Grid:
    g = Grid()
    g.ellipse(8, 9, 6.5, 5, MEAT)
    g.top_fat()
    g.marble(10, 3)
    g.shade()
    g.outline()
    return g


def _striploin(bone: bool) -> Grid:
    g = Grid()
    _steak(g, 3, 7, 11, 5)
    g.top_fat()
    if bone:
        _bone_bar(g, 4, 12, 4, 2)
        g.rect(6, 6, 1, 1, BONE)
    g.marble(5, 7)
    g.shade()
    g.outline()
    return g


def _tenderloin() -> Grid:
    g = Grid()
    g.ellipse(8, 8.5, 5.5, 3.6, MEAT)
    g.rect(3, 6, 11, 5, MEAT)
    g.rect(4, 5, 8, 1, LIGHT)
    g.rect(6, 5, 1, 7, FAT)
    g.rect(10, 5, 1, 7, FAT)
    g.marble(4, 11)
    g.outline()
    return g


def _tbone() -> Grid:
    g = Grid()
    g.ellipse(8, 7, 6, 4, MEAT)
    g.rect(2, 4, 12, 7, MEAT)
    g.top_fat()
    _tbone_shape(g, 7, 8, 13, 4)
    g.marble(7, 21)
    g.outline()
    return g


def _porterhouse() -> Grid:
    g = Grid()
    g.ellipse(9, 7, 6, 4.5, MEAT)
    g.rect(3, 4, 11, 7, MEAT)
    g.top_fat()
    _tbone_shape(g, 5, 8, 13, 3)
    g.marble(8, 33)
    g.outline()
    return g


def _sirloin() -> Grid:
    g = Grid()
    g.poly([(2, 12), (6, 4), (13, 6), (14, 11), (8, 13)], MEAT)
    g.top_fat()
    g.marble(7, 5)
    g.shade()
    g.outline()
    return g


def _sirloin_bone(bone: bool) -> Grid:
    g = Grid()
    g.poly([(2, 11), (5, 5), (13, 6), (13, 11), (7, 12)], MEAT)
    if bone:
        _bone_bar(g, 4, 13, 3, 2)
    g.top_fat()
    g.marble(6, 9)
    g.shade()
    g.outline()
    return g


def _petite_sirloin() -> Grid:
    g = Grid()
    g.ellipse(8, 8, 4.5, 4, MEAT)
    g.top_fat()
    g.marble(4, 13)
    g.shade()
    g.outline()
    return g


def _tri_tip() -> Grid:
    g = Grid()
    g.poly([(3, 12), (12, 4), (14, 11)], MEAT)
    g.top_fat()
    g.marble(6, 17)
    g.shade()
    g.outline()
    return g


def _ball_tip() -> Grid:
    g = Grid()
    g.ellipse(8, 9, 5, 4.5, MEAT)
    g.ellipse(11, 7, 2.4, 2.4, LIGHT)
    g.marble(5, 23)
    g.shade()
    g.outline()
    return g


def _picanha() -> Grid:
    g = Grid()
    g.ellipse(8, 9.5, 5.5, 4.5, MEAT)
    g.rect(3, 8, 11, 4, MEAT)
    g.rect(3, 5, 11, 2, FAT)
    g.rect(3, 4, 11, 1, DARK)
    g.marble(5, 29)
    g.outline()
    return g


def _flank() -> Grid:
    g = Grid()
    g.poly([(2, 6), (13, 5), (14, 9), (3, 11)], MEAT)
    g.top_fat()
    g.marble(5, 31)
    g.shade()
    g.outline()
    return g


def _skirt() -> Grid:
    g = Grid()
    g.poly([(2, 7), (5, 4), (13, 6), (14, 9), (6, 12), (2, 10)], MEAT)
    g.top_fat()
    g.marble(5, 37)
    g.shade()
    g.outline()
    return g


def _hanger() -> Grid:
    g = Grid()
    g.poly([(2, 5), (8, 6), (14, 9), (11, 12), (4, 10)], MEAT)
    g.top_fat()
    g.marble(5, 41)
    g.shade()
    g.outline()
    return g


def _bavette() -> Grid:
    g = Grid()
    g.ellipse(7, 8, 4.5, 4.5, MEAT)
    g.poly([(9, 5), (14, 9), (10, 12)], MEAT)
    g.marble(5, 43)
    g.shade()
    g.outline()
    return g


def _flat_iron() -> Grid:
    g = Grid()
    _steak(g, 2, 6, 12, 4)
    g.top_fat()
    g.marble(6, 47)
    g.shade()
    g.outline()
    return g


def _denver() -> Grid:
    g = Grid()
    _steak(g, 3, 5, 10, 6)
    g.top_fat()
    for i in range(3):
        g.line(4 + i * 3, 6, 4 + i * 3, 10, LIGHT)
    g.outline()
    return g


def _cube_steak() -> Grid:
    g = Grid()
    g.rect(4, 4, 8, 8, MEAT)
    for i in range(4):
        g.set(5 + i * 2, 5 + i * 2, LIGHT)
        g.set(5 + i * 2, 10 - i * 2, LIGHT)
    g.outline()
    return g


def _chuck_eye() -> Grid:
    g = Grid()
    g.ellipse(8, 9, 5.5, 4.5, MEAT)
    g.ellipse(9, 9, 1.8, 1.8, LIGHT)
    g.marble(5, 53)
    g.shade()
    g.outline()
    return g


def _round_steak() -> Grid:
    g = Grid()
    g.ellipse(8, 8.5, 5.5, 5, MEAT)
    g.top_fat()
    g.marble(6, 59)
    g.shade()
    g.outline()
    return g


def _eye_round() -> Grid:
    g = Grid()
    g.ellipse(8, 8.5, 5.5, 5, MEAT)
    g.ellipse(8, 9, 2, 1.8, LIGHT)
    g.ellipse(8, 9, 1, 0.9, FAT)
    g.marble(5, 61)
    g.shade()
    g.outline()
    return g


def _london_broil() -> Grid:
    g = Grid()
    _steak(g, 3, 5, 10, 6)
    g.top_fat()
    g.marble(6, 67)
    g.shade()
    g.outline()
    return g


def _chuck_steak() -> Grid:
    g = Grid()
    g.poly([(3, 11), (4, 5), (8, 4), (12, 6), (13, 11), (7, 12)], MEAT)
    g.top_fat()
    g.marble(7, 71)
    g.shade()
    g.outline()
    return g


def _ribs_rack() -> Grid:
    g = Grid()
    for i in range(3):
        y = 4 + i * 3
        g.line(3, y + 3, 8, y, BONE)
        g.line(8, y, 13, y + 3, BONE)
        g.rect(3, y + 3, 10, 2, MEAT)
        g.set(4, y + 3, FAT)
    g.outline()
    return g


def _ribs_short() -> Grid:
    g = Grid()
    for i in range(2):
        x = 3 + i * 6
        g.rect(x, 6, 5, 5, MEAT)
        g.rect(x, 11, 5, 2, BONE)
        g.set(x + 1, 6, FAT)
    g.outline()
    return g


def _country_ribs() -> Grid:
    g = Grid()
    for i in range(3):
        y = 4 + i * 3
        g.rect(4, y, 9, 2, MEAT)
        g.set(4, y, FAT)
        g.rect(11, y + 1, 2, 1, BONE)
    g.outline()
    return g


def _roast_chunk() -> Grid:
    g = Grid()
    g.ellipse(8, 8, 6, 4.5, MEAT)
    g.rect(2, 5, 12, 7, MEAT)
    g.rect(2, 5, 12, 1, LIGHT)
    g.marble(6, 73)
    g.shade()
    g.outline()
    return g


def _roast_bone() -> Grid:
    g = Grid()
    g.ellipse(8, 9, 6, 4, MEAT)
    g.rect(2, 6, 12, 6, MEAT)
    g.rect(2, 5, 12, 1, LIGHT)
    for i in range(3):
        g.rect(3 + i * 4, 3, 2, 4, BONE)
        g.ellipse(3 + i * 4, 3, 1.5, 1.5, BONE)
    g.marble(5, 79)
    g.outline()
    return g


def _roast_round() -> Grid:
    g = Grid()
    g.ellipse(8, 8.5, 5.5, 5, MEAT)
    g.rect(2, 6, 12, 5, MEAT)
    g.marble(7, 83)
    g.shade()
    g.outline()
    return g


def _roast_eye() -> Grid:
    g = Grid()
    g.ellipse(8, 8.5, 5.5, 5, MEAT)
    g.rect(2, 6, 12, 5, MEAT)
    g.ellipse(8, 9, 2, 1.8, LIGHT)
    g.marble(5, 89)
    g.outline()
    return g


def _rump_roast() -> Grid:
    g = Grid()
    g.ellipse(7, 8.5, 5, 4.5, MEAT)
    g.poly([(9, 5), (14, 8), (9, 11)], MEAT)
    g.marble(6, 97)
    g.shade()
    g.outline()
    return g


def _brisket_flat() -> Grid:
    g = Grid()
    g.rect(2, 6, 12, 6, MEAT)
    g.rect(2, 5, 12, 1, FAT)
    g.rect(2, 11, 12, 1, FAT)
    g.marble(8, 101)
    g.shade()
    g.outline()
    return g


def _brisket_point() -> Grid:
    g = Grid()
    g.poly([(2, 12), (3, 6), (13, 5), (13, 9), (7, 13)], MEAT)
    g.top_fat()
    g.marble(6, 103)
    g.shade()
    g.outline()
    return g


def _brisket_whole() -> Grid:
    g = Grid()
    g.poly([(2, 11), (3, 6), (7, 4), (13, 5), (14, 10), (8, 13)], MEAT)
    g.rect(4, 5, 8, 2, FAT)
    g.marble(7, 107)
    g.shade()
    g.outline()
    return g


def _tenderloin_whole() -> Grid:
    g = Grid()
    g.ellipse(8, 8.5, 6, 3, MEAT)
    g.rect(2, 6, 12, 5, MEAT)
    g.rect(4, 6, 1, 5, FAT)
    g.rect(11, 6, 1, 5, FAT)
    g.marble(5, 109)
    g.outline()
    return g


def _shin() -> Grid:
    g = Grid()
    g.ellipse(8, 8, 5.5, 5.5, MEAT)
    g.ellipse(8, 8, 2.6, 2.6, LIGHT)
    g.ellipse(8, 8, 1.2, 1.2, BONE)
    g.marble(4, 113)
    g.outline()
    return g


def _stew_chunks() -> Grid:
    g = Grid()
    _chunks(g, [(2, 3, 4, 4), (8, 2, 4, 4), (4, 9, 4, 4), (10, 8, 4, 4)])
    g.outline()
    return g


def _filet_tips() -> Grid:
    g = Grid()
    _chunks(g, [(2, 3, 3, 3), (6, 2, 3, 3), (10, 4, 3, 3), (3, 8, 3, 3),
                 (8, 8, 3, 3)])
    g.outline()
    return g


def _rib_fingers() -> Grid:
    g = Grid()
    for i in range(3):
        y = 4 + i * 3
        g.rect(3 + i, y, 9, 2, MEAT)
        g.set(3 + i, y, FAT)
        g.rect(11 + i, y, 2, 2, BONE)
    g.outline()
    return g


def _ground() -> Grid:
    g = Grid()
    g.ellipse(8, 11, 6, 4, MEAT)
    g.rect(2, 9, 12, 3, MEAT)
    g.marble(16, 127)
    g.shade()
    g.outline()
    return g


def _patties() -> Grid:
    g = Grid()
    g.ellipse(6, 6.5, 4.2, 3.2, MEAT)
    g.ellipse(10, 10, 4.2, 3.2, MEAT)
    g.marble(9, 131)
    g.shade()
    g.outline()
    return g


def _sausage() -> Grid:
    g = Grid()
    g.ellipse(8, 8, 5.5, 3.2, CURED)
    g.rect(3, 6, 10, 5, CURED)
    g.rect(3, 6, 10, 1, LIGHT)
    g.set(5, 5, LIGHT)
    g.set(11, 5, LIGHT)
    g.outline()
    return g


def _bacon() -> Grid:
    g = Grid()
    for i in range(3):
        y = 3 + i * 4
        g.rect(3, y, 10, 3, CRUST)
        for x in range(3, 13, 3):
            g.rect(x, y, 2, 3, FAT)
    g.outline()
    return g


def _jerky() -> Grid:
    g = Grid()
    for i in range(2):
        y = 4 + i * 5
        g.rect(4, y, 9, 3, CRUST)
        g.rect(4, y, 9, 1, DARK)
        g.set(6, y + 1, MEAT)
    g.outline()
    return g


def _bologna() -> Grid:
    g = Grid()
    g.ellipse(6, 8, 3.4, 5, CURED)
    g.rect(3, 4, 6, 9, CURED)
    g.ellipse(12, 8, 2.4, 2.4, LIGHT)
    g.ellipse(12, 8, 1.4, 1.4, CURED)
    g.outline()
    return g


def _corned_beef() -> Grid:
    g = Grid()
    g.rect(3, 4, 10, 8, CURED)
    g.rect(3, 4, 10, 1, LIGHT)
    g.marble(6, 137, ch=LIGHT)
    g.outline()
    return g


def _sliced_roast() -> Grid:
    g = Grid()
    for i in range(3):
        y = 4 + i * 3
        g.ellipse(8, y + 1, 5.5, 1.6, MEAT)
        g.rect(3, y, 10, 2, MEAT)
        g.set(4, y, FAT)
    g.outline()
    return g


def _snack_sticks() -> Grid:
    g = Grid()
    for i in range(3):
        x = 3 + i * 4
        g.rect(x, 4, 2, 8, CURED)
        g.set(x, 4, LIGHT)
    g.outline()
    return g


def _cheek() -> Grid:
    g = Grid()
    g.ellipse(8, 8.5, 5, 4.5, MEAT)
    g.poly([(3, 6), (6, 3), (10, 4), (11, 8)], MEAT)
    g.marble(6, 139)
    g.shade()
    g.outline()
    return g


def _liver() -> Grid:
    g = Grid()
    g.ellipse(8, 8, 6, 4.5, DARK)
    g.poly([(2, 7), (6, 4), (9, 6), (7, 10), (3, 10)], DARK)
    g.marble(5, 149, ch=MEAT)
    g.outline()
    return g


def _tongue() -> Grid:
    g = Grid()
    g.ellipse(8, 8, 4.5, 5.5, MEAT)
    g.rect(5, 3, 6, 11, MEAT)
    g.rect(5, 3, 6, 1, LIGHT)
    g.set(9, 6, LIGHT)
    g.outline()
    return g


def _heart() -> Grid:
    g = Grid()
    g.poly([(8, 13), (3, 7), (4, 4), (7, 5), (8, 6), (9, 5), (12, 4),
            (13, 7)], MEAT)
    g.set(6, 7, LIGHT)
    g.set(10, 7, LIGHT)
    g.outline()
    return g


def _kidney() -> Grid:
    g = Grid()
    g.ellipse(8, 8, 5, 4.5, DARK)
    g.ellipse(8, 8, 1.6, 1.6, DARK)
    g.set(7, 8, DARK)
    g.set(9, 8, DARK)
    g.marble(4, 151, ch=MEAT)
    g.outline()
    return g


def _oxtail() -> Grid:
    g = Grid()
    for i in range(3):
        x = 3 + i * 4
        g.ellipse(x + 1, 8, 1.8, 2.6, MEAT)
        g.rect(x + 1, 8, 3, 1, BONE)
    g.outline()
    return g


def _marrow_bone() -> Grid:
    g = Grid()
    g.rect(4, 6, 8, 4, BONE)
    g.ellipse(4, 8, 1.8, 2.4, BONE)
    g.ellipse(12, 8, 1.8, 2.4, BONE)
    g.rect(5, 7, 6, 2, MARROW)
    g.outline()
    return g


def _soup_bones() -> Grid:
    g = Grid()
    for x, y in ((3, 3), (9, 4), (5, 9)):
        g.rect(x, y, 4, 3, BONE)
        g.ellipse(x, y + 1, 1.4, 1.8, BONE)
        g.ellipse(x + 3, y + 1, 1.4, 1.8, BONE)
    g.outline()
    return g


def _suet() -> Grid:
    g = Grid()
    g.rect(3, 4, 10, 8, FAT)
    g.rect(3, 4, 10, 2, MARROW)
    g.rect(3, 10, 10, 2, MARROW)
    g.outline()
    return g


#: name -> sprite. The names are used as the ``icon`` column on a cut.
SPRITES: dict[str, tuple[str, ...]] = {}


def _build() -> None:
    makers = {
        "ribeye": _ribeye,
        "ribeye_boneless": _ribeye_boneless,
        "striploin": lambda: _striploin(True),
        "striploin_boneless": lambda: _striploin(False),
        "tenderloin": _tenderloin,
        "tbone": _tbone,
        "porterhouse": _porterhouse,
        "sirloin": _sirloin,
        "sirloin_bone": lambda: _sirloin_bone(True),
        "sirloin_boneless": lambda: _sirloin_bone(False),
        "petite_sirloin": _petite_sirloin,
        "tri_tip": _tri_tip,
        "ball_tip": _ball_tip,
        "picanha": _picanha,
        "flank": _flank,
        "skirt": _skirt,
        "hanger": _hanger,
        "bavette": _bavette,
        "flat_iron": _flat_iron,
        "denver": _denver,
        "cube_steak": _cube_steak,
        "chuck_eye": _chuck_eye,
        "round_steak": _round_steak,
        "eye_round": _eye_round,
        "london_broil": _london_broil,
        "chuck_steak": _chuck_steak,
        "ribs_rack": _ribs_rack,
        "ribs_short": _ribs_short,
        "country_ribs": _country_ribs,
        "roast_chunk": _roast_chunk,
        "roast_bone": _roast_bone,
        "roast_round": _roast_round,
        "roast_eye": _roast_eye,
        "rump_roast": _rump_roast,
        "brisket_flat": _brisket_flat,
        "brisket_point": _brisket_point,
        "brisket_whole": _brisket_whole,
        "tenderloin_whole": _tenderloin_whole,
        "shin": _shin,
        "stew_chunks": _stew_chunks,
        "filet_tips": _filet_tips,
        "rib_fingers": _rib_fingers,
        "ground": _ground,
        "patties": _patties,
        "sausage": _sausage,
        "bacon": _bacon,
        "jerky": _jerky,
        "bologna": _bologna,
        "corned_beef": _corned_beef,
        "sliced_roast": _sliced_roast,
        "snack_sticks": _snack_sticks,
        "cheek": _cheek,
        "liver": _liver,
        "tongue": _tongue,
        "heart": _heart,
        "kidney": _kidney,
        "oxtail": _oxtail,
        "marrow_bone": _marrow_bone,
        "soup_bones": _soup_bones,
        "suet": _suet,
    }
    for name, maker in makers.items():
        SPRITES[name] = maker().rows()


_build()
