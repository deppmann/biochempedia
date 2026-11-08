"""Mapping the Cortex: Areas and Arealization, chapter 1: A Sheet with No Borders  (Biochemistrypedia chaptered film)

The recurring picture is ONE mouse cortical hemisphere seen from above: front on the LEFT, back on the RIGHT,
the medial edge (midline) along the TOP, the lateral (outer) edge along the BOTTOM.

COLOR MAP (one color per concept, whole chapter series; same as the lesson's earlier film plus the new ones)
  PURPLE = motor area
  GREEN  = somatosensory (touch) area, and its barrels
  PINK   = visual area
  SAND   = auditory area
  ORANGE = Emx2 (later chapters)
  BLUE   = Pax6 (later chapters)
  YELLOW = signalling centres / FGF8, the signal from the edge (ONLY that: never questions or emphasis)
  TEAL   = neurons (made by the progenitors)
  TEXT   = thalamus and thalamic axons (the input)
  QCOL   = pale periwinkle: question marks, "what is this?" cards (the open question, nothing else)
  RED    = a blocker / something removed (later chapters)
  GREY   = the sheet, progenitors, labels, de-emphasised things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB5"
SAND = "#D9B77E"
QCOL = "#A9B8FF"
NEURON = TEAL
AXON = TEXT


# ---------------------------------------------------------------------------------------------
# geometry helpers
def catmull(pts, n=14):
    """Closed Catmull-Rom spline through the control points, densely sampled."""
    P = np.array(pts, float)
    m = len(P)
    out = []
    for i in range(m):
        p0, p1, p2, p3 = P[(i - 1) % m], P[i], P[(i + 1) % m], P[(i + 2) % m]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return np.array(out)


def shape(D, s=1.0, c=(0, 0), color=GREY, fill=GREY, fo=0.0, sw=3, closed=True):
    pts = [[c[0] + s * x, c[1] + s * y, 0.0] for x, y in D]
    if closed:
        pts.append(pts[0])
    m = VMobject(stroke_color=color, stroke_width=sw, fill_color=fill, fill_opacity=fo)
    m.set_points_as_corners(pts)
    return m


def blobpts(cx, cy, rx, ry, ph=0.0, n=90):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1 + 0.06 * np.sin(3 * th + ph) + 0.035 * np.sin(5 * th + 2 * ph)
    return np.stack([cx + rx * r * np.cos(th), cy + ry * r * np.sin(th)], 1)


def inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


# the hemisphere (map units: x -4.8..4.8 front to back, y -2.4..2.4 lateral to medial; top edge = medial)
HB = [(0.0, -2.55), (1.6, -2.5), (2.9, -2.25), (3.9, -1.8), (4.55, -1.0), (4.8, 0.0), (4.7, 1.0), (4.2, 1.9),
      (3.3, 2.35), (2.5, 2.4), (1.0, 2.4), (-0.5, 2.4), (-2.0, 2.4), (-3.4, 2.3), (-4.2, 1.95), (-4.65, 1.2),
      (-4.75, 0.3), (-4.4, -0.5), (-3.7, -1.1), (-2.6, -1.75), (-1.3, -2.3)]
DH = catmull(HB, 12)
MED = DH[DH[:, 1] > 2.35]
_lat = np.where(DH[:, 1] < -0.9)[0]
_gap = np.where(np.diff(_lat) > 1)[0]
LAT = DH[np.concatenate([_lat[_gap[0] + 1:], _lat[:_gap[0] + 1]])] if len(_gap) else DH[_lat]

PATCH = {  # name: (cx, cy, rx, ry, color, phase)
    "motor": (-3.15, 1.1, 1.2, 0.95, PURPLE, 0.3),
    "touch": (-0.3, 0.35, 1.7, 1.3, GREEN, 1.1),
    "auditory": (1.95, -1.55, 1.15, 0.65, SAND, 2.0),
    "visual": (3.55, 0.45, 0.95, 1.3, PINK, 0.6),
}
AREAS = ("motor", "touch", "auditory", "visual")
BARREL_C = (-0.15, -0.05)
BAR_KW = dict(cols=5, rows=3, sp=0.36, r=0.11, c=BARREL_C)   # the barrel grid: 3 rows of 5, same in every scene


class CMap:
    """The mouse hemisphere, scaled s and centred c; P() converts map units to scene coordinates."""

    def __init__(self, s=1.0, c=(0.0, -0.15)):
        self.s, self.c = s, c

    def P(self, x, y):
        return np.array([self.c[0] + self.s * x, self.c[1] + self.s * y, 0.0])

    def outline(self, color=GREY, fill=GREY, fo=0.16, sw=3):
        return shape(DH, self.s, self.c, color, fill, fo, sw)

    def patch(self, name, fo=0.42, sw=2.5):
        cx, cy, rx, ry, col, ph = PATCH[name]
        return shape(blobpts(cx, cy, rx, ry, ph), self.s, self.c, col, col, fo, sw)

    def dashed(self, name, n=36, sw=3):
        cx, cy, rx, ry, col, ph = PATCH[name]
        return DashedVMobject(shape(blobpts(cx, cy, rx, ry, ph), self.s, self.c, col, col, 0.0, sw), num_dashes=n)

    def patches(self, names=AREAS, fo=0.42, sw=2.5):
        return VGroup(*[self.patch(n, fo, sw) for n in names])

    def label(self, name, text=None, size=26, color=TEXT, dx=0.0, dy=0.0):
        cx, cy = PATCH[name][:2]
        return T(text or name, size, color).move_to(self.P(cx + dx, cy + dy))

    def barrels(self, cols=5, rows=3, sp=0.36, r=0.11, c=BARREL_C, op=0.85):
        g = VGroup()
        for j in range(rows):
            for i in range(cols):
                g.add(Circle(radius=r * self.s, stroke_color=GREEN, stroke_width=2, fill_color=GREEN,
                             fill_opacity=op).move_to(self.P(c[0] + (i - (cols - 1) / 2) * sp,
                                                             c[1] + (j - (rows - 1) / 2) * sp)))
        return g

    def medial(self, color=TEXT, sw=8):
        return shape(MED, self.s, self.c, color, color, 0, sw, closed=False)

    def lateral(self, color=TEXT, sw=8):
        return shape(LAT, self.s, self.c, color, color, 0, sw, closed=False)


MAIN = CMap(1.2, (0.45, 0.25))     # the recurring map, about three quarters of the frame height
SHEET = CMap(1.2, (0.0, 0.0))      # the plain embryonic sheet (cells scenes)
SMALL = CMap(1.05, (0.0, -0.45))   # the map with room above it for brackets


def fb_axis(y=-3.6):
    """front-to-back arrow under the map."""
    ar = Arrow([-4.2, y, 0], [4.9, y, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
    return VGroup(ar, T("front", 26, GREY).move_to([-5.25, y, 0]), T("back", 26, GREY).move_to([5.75, y, 0]))


def edge_labels():
    """grey 'medial (midline)' above the top edge and 'lateral' below the lower edge."""
    return VGroup(T("medial (midline)", 26, GREY).move_to([0.45, 3.55, 0]), T("lateral", 26, GREY).move_to([0.45, -3.14, 0]))


def halo(t):
    return t.set_stroke(BG, 8, background=True)


def plate(mob, pad=0.12, op=0.88):
    """a dark backing plate behind a label, so dots never sit under text."""
    r = RoundedRectangle(corner_radius=0.1, width=mob.width + 2 * pad, height=mob.height + 2 * pad, stroke_width=0,
                         fill_color=BG, fill_opacity=op).move_to(mob)
    return VGroup(r, mob)


def mouse_head(s=1.0, c=(0, 0), color=GREY, whisk=True):
    cx, cy = c
    g = VGroup()
    for sx in (-1, 1):
        g.add(Circle(radius=0.34 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.15)
              .move_to([cx + sx * 0.62 * s, cy + 0.55 * s, 0]))
    g.add(Ellipse(width=1.5 * s, height=1.2 * s, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1)
          .move_to([cx, cy, 0]))
    for sx in (-1, 1):
        g.add(Dot([cx + sx * 0.3 * s, cy + 0.15 * s, 0], radius=0.06 * s, color=TEXT))
    g.add(Dot([cx, cy - 0.22 * s, 0], radius=0.1 * s, color=PINK))
    if whisk:
        for sx in (-1, 1):
            for dy in (0.14, -0.02, -0.18):
                g.add(Line([cx + sx * 0.3 * s, cy - 0.28 * s, 0], [cx + sx * 1.15 * s, cy - 0.28 * s + dy * s * 1.4, 0],
                           stroke_color=color, stroke_width=2.5))
    return g


def nose_icon():
    """the one mouse head, beside the FRONT end of the map, nose pointing away from the brain."""
    return mouse_head(0.8, (0, 0)).rotate(-PI / 2).move_to([-6.1, 0.3, 0])


def eye_icon(s=1.0, c=(0, 0), color=TEXT):
    cx, cy = c
    a = ArcBetweenPoints([cx - 0.6 * s, cy, 0], [cx + 0.6 * s, cy, 0], angle=-1.4, stroke_color=color, stroke_width=3.5)
    b = ArcBetweenPoints([cx - 0.6 * s, cy, 0], [cx + 0.6 * s, cy, 0], angle=1.4, stroke_color=color, stroke_width=3.5)
    return VGroup(a, b, Circle(radius=0.19 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)
                  .move_to([cx, cy, 0]))


def ear_icon(s=1.0, c=(0, 0), color=TEXT):
    cx, cy = c
    outer = Arc(radius=0.45 * s, start_angle=-0.4, angle=4.2, stroke_color=color, stroke_width=3.5).move_arc_center_to([cx, cy, 0])
    inner = Arc(radius=0.22 * s, start_angle=0.6, angle=3.3, stroke_color=color, stroke_width=3.5).move_arc_center_to([cx + 0.02 * s, cy - 0.02 * s, 0])
    return VGroup(outer, inner)


def hand_icon(s=1.0, c=(0, 0), color=TEXT):
    """a simple open hand: palm, four fingers, thumb."""
    cx, cy = c
    kw = dict(stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.15)
    g = VGroup(RoundedRectangle(corner_radius=0.2 * s, width=0.95 * s, height=0.8 * s, **kw).move_to([cx, cy - 0.2 * s, 0]))
    for dx, h in ((-0.34, 0.62), (-0.11, 0.8), (0.12, 0.74), (0.35, 0.56)):
        g.add(RoundedRectangle(corner_radius=0.09 * s, width=0.2 * s, height=h * s, **kw).move_to([cx + dx * s, cy + 0.15 * s + h * s / 2, 0]))
    g.add(RoundedRectangle(corner_radius=0.09 * s, width=0.2 * s, height=0.55 * s, **kw).rotate(0.9).move_to([cx - 0.62 * s, cy - 0.05 * s, 0]))
    return g


def thalamus_blob(c=(0, 0), w=1.0, color=AXON, label="thalamus", size=26):
    b = shape(blobpts(0, 0, 1.25 * w, 0.62 * w, 0.5), 1.0, c, color, color, 0.18, 3)
    return VGroup(b, T(label, size, color).move_to([c[0], c[1], 0]))


# ---- human brain (Brodmann) ----
HUM = [(-3.2, 0.1), (-3.0, 1.1), (-2.3, 1.85), (-1.1, 2.2), (0.3, 2.25), (1.6, 1.95), (2.5, 1.2), (3.0, 0.3),
       (2.9, -0.45), (2.2, -0.85), (1.2, -1.0), (0.4, -1.55), (-0.7, -1.55), (-1.6, -1.05), (-2.6, -0.65)]
DHUM = catmull(HUM, 12)
HPATCH = {  # label: (cx, cy, rx, ry)
    "9": (-2.25, 1.0, 0.4, 0.5),
    "44": (-1.75, -0.15, 0.42, 0.38),
    "4": (-0.35, 1.55, 0.3, 0.52),
    "3": (0.55, 1.55, 0.3, 0.52),
    "41": (0.0, -0.95, 0.5, 0.28),
    "17": (2.55, 0.4, 0.33, 0.58),
}


class Human:
    def __init__(self, s=1.2, c=(2.6, -0.1)):
        self.s, self.c = s, c

    def P(self, x, y):
        return np.array([self.c[0] + self.s * x, self.c[1] + self.s * y, 0.0])

    def body(self):
        cer = shape(blobpts(2.0, -1.45, 0.95, 0.5, 0.3), self.s, self.c, GREY, GREY, 0.1, 3)
        stem = shape(blobpts(0.9, -1.6, 0.3, 0.55, 0.0)[::1], self.s, self.c, GREY, GREY, 0.1, 3)
        out = shape(DHUM, self.s, self.c, GREY, GREY, 0.16, 3.5)
        sul = VGroup()
        for pts in (((-0.9, 1.9), (-0.8, 1.2), (-1.0, 0.6)), ((0.0, 2.05), (0.1, 1.2), (0.0, 0.4)),
                    ((1.2, -0.7), (0.2, -0.45), (-0.9, -0.5), (-1.5, -0.2))):
            m = VMobject(stroke_color=GREY, stroke_width=2.5, stroke_opacity=0.55)
            m.set_points_smoothly([[self.c[0] + self.s * x, self.c[1] + self.s * y, 0] for x, y in pts])
            sul.add(m)
        return VGroup(cer, stem, out, sul)

    def patch(self, key, lit=None, fo=0.5):
        """a grey numbered patch; pass a colour in `lit` to light it."""
        cx, cy, rx, ry = HPATCH[key]
        if lit:
            return shape(blobpts(cx, cy, rx, ry, 0.4, 60), self.s, self.c, lit, lit, fo, 2.5)
        return shape(blobpts(cx, cy, rx, ry, 0.4, 60), self.s, self.c, GREY, GREY, 0.12, 2.5)

    def num(self, key, size=26, color=TEXT):
        cx, cy = HPATCH[key][:2]
        return T(key, size, color).move_to(self.P(cx, cy))


def stained_section(c=(-4.95, 0.1), w=3.2, h=4.8):
    """a stained slice: alternating bands of densely and sparsely packed cells.  Returns frame, dots, lines, band rectangles."""
    rng = np.random.RandomState(7)
    bands = [(0.10, 0.10), (0.90, 0.12), (0.10, 0.10), (0.95, 0.14), (0.08, 0.10), (1.0, 0.16), (0.10, 0.10), (0.90, 0.18)]
    tot = sum(b[1] for b in bands)
    frame = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=NEURON, fill_opacity=0.05).move_to([c[0], c[1], 0])
    dots, rects, y = VGroup(), [], c[1] + h / 2
    edges = []
    for dens, frac in bands:
        bh = h * frac / tot
        n = int(dens * 62)
        cols = max(1, int(round(np.sqrt(n * w / bh))))
        rows = max(1, int(np.ceil(n / cols)))
        k = 0
        for ri in range(rows):
            for ci in range(cols):
                if k >= n:
                    break
                px = c[0] - w / 2 + 0.14 + (w - 0.28) * (ci + 0.5 + 0.35 * (ri % 2)) / (cols + 0.35) + rng.uniform(-0.04, 0.04)
                py = y - 0.07 - (bh - 0.14) * (ri + 0.5) / rows + rng.uniform(-0.03, 0.03)
                dots.add(Dot([px, py, 0], radius=0.05, color=NEURON).set_opacity(0.9))
                k += 1
        rects.append(Rectangle(width=w, height=bh, stroke_color=NEURON, stroke_width=2, fill_color=NEURON, fill_opacity=0.3)
                     .move_to([c[0], y - bh / 2, 0]))
        y -= bh
        edges.append(y)
    lines = VGroup(*[Line([c[0] - w / 2, e, 0], [c[0] + w / 2, e, 0], stroke_color=GREY, stroke_width=2, stroke_opacity=0.7)
                     for e in edges[:-1]])
    return frame, dots, lines, rects


# ---- timeline (bottom panel) ----
TLX0, TLPX = -2.6, 0.585
ROW = {"sig": -0.3, "neu": -1.0, "thal": -1.7, "bar": -2.4}
AXY = -3.0
SIG0, SIG_SOLID, SIG_END = 9.5, 11.2, 13.8   # the signalling bar starts at E9.5 and fades away with no stated end


def tx(d):
    return TLX0 + (d - 9) * TLPX


def tl_axis():
    g = VGroup(Line([tx(9), AXY, 0], [tx(24.5), AXY, 0], stroke_color=GREY, stroke_width=2.5))
    for d, lab in [(9, "E9"), (11, "E11"), (13, "E13"), (15, "E15"), (17, "E17"), (19.5, "birth"), (23.5, "P4")]:
        g.add(Line([tx(d), AXY - 0.08, 0], [tx(d), AXY + 0.08, 0], stroke_color=GREY, stroke_width=2.5))
        g.add(T(lab, 26, GREY).move_to([tx(d), AXY - 0.36, 0]))
    return g


def tl_label(key, text, color):
    t = T(text, 26, color)
    t.move_to([tx(9) - 0.32 - t.width / 2, ROW[key], 0])
    return t


def tl_bar(key, d0, d1, color, op=0.8, h=0.34, sw=2.5):
    return Rectangle(width=(d1 - d0) * TLPX, height=h, stroke_color=color, stroke_width=sw, fill_color=color,
                     fill_opacity=op).move_to([tx((d0 + d1) / 2), ROW[key], 0])


def e95_label():
    """E9.5 sits on top of the start of the signalling bar, not between rows."""
    return T("E9.5", 26, YELLOW).move_to([tx(9.5) + 0.3, ROW["sig"] + 0.42, 0])


def sig_bar(h=0.34, n=14):
    """E9.5 solid, then fading to nothing: the lesson gives a start, not a stop."""
    solid = Rectangle(width=(SIG_SOLID - SIG0) * TLPX, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85)
    solid.move_to([tx((SIG0 + SIG_SOLID) / 2), ROW["sig"], 0])
    fade = VGroup()
    w = (SIG_END - SIG_SOLID) / n
    for k in range(n):
        d0 = SIG_SOLID + k * w
        fade.add(Rectangle(width=w * TLPX + 0.01, height=h, stroke_width=0, fill_color=YELLOW,
                           fill_opacity=0.85 * (1 - (k + 0.5) / n)).move_to([tx(d0 + w / 2), ROW["sig"], 0]))
    return solid, fade


def tl_dashed(key, d0, d1, color):
    return DashedLine([tx(d0), ROW[key], 0], [tx(d1), ROW[key], 0], dash_length=0.14, stroke_color=color, stroke_width=4)


def tl_birth(y1=-0.05):
    return DashedLine([tx(19.5), AXY + 0.1, 0], [tx(19.5), y1, 0], dash_length=0.1, stroke_color=GREY, stroke_width=2).set_opacity(0.6)


def tl_ticklabel(axis, i):
    return axis[2 + 2 * i]  # the label of tick i (axis[0] is the line; then tick, label pairs)


def glow(x, y, r=0.34, dim=1.0):
    g = VGroup()
    for k, o in ((2.6, 0.08), (1.9, 0.14), (1.35, 0.25)):
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=YELLOW, fill_opacity=o * dim))
    g.add(Circle(radius=r, stroke_color=YELLOW, stroke_width=3, stroke_opacity=max(0.3, dim), fill_color=YELLOW,
                 fill_opacity=0.95 * dim))
    return g.move_to([x, y, 0])


def cell(x, y, r=0.1, color=GREY, fo=0.55):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fo).move_to([x, y, 0])


def neuron_dot(x, y, r=0.1):
    return Circle(radius=r, stroke_color=NEURON, stroke_width=2, fill_color=NEURON, fill_opacity=0.85).move_to([x, y, 0])


def sheet_cells(cm, spacing=0.6, seed=3, margin=0.28, r=0.12):
    """progenitor dots across the hemisphere, kept inside its outline."""
    rng = np.random.RandomState(seed)
    out = VGroup()
    xs = np.arange(-4.4, 4.5, spacing)
    ys = np.arange(-2.2, 2.3, spacing)
    for ix, x in enumerate(xs):
        for iy, y in enumerate(ys):
            px = x + 0.25 * (iy % 2) + rng.uniform(-0.12, 0.12)
            py = y + rng.uniform(-0.12, 0.12)
            if inside(DH, px, py) and np.min(np.hypot(DH[:, 0] - px, DH[:, 1] - py)) > margin:
                out.add(cell(*cm.P(px, py)[:2], r=r))
    return out


def bracket(x0, x1, y, color=TEXT, d=-0.2):
    return VGroup(Line([x0, y, 0], [x1, y, 0], stroke_color=color, stroke_width=4),
                  Line([x0, y, 0], [x0, y + d, 0], stroke_color=color, stroke_width=4),
                  Line([x1, y, 0], [x1, y + d, 0], stroke_color=color, stroke_width=4))


def tl_final(with_bar=False):
    """the finished timeline rows (as at the end of the answer scene)."""
    sb = sig_bar()
    g = VGroup(tl_label("sig", "signalling centres", YELLOW), *sb,
               tl_label("neu", "neurons made", NEURON), tl_bar("neu", 11, 17, NEURON),
               tl_label("thal", "thalamic axons", AXON), tl_bar("thal", 14, 15, AXON, 0.85),
               tl_dashed("thal", 15, 19.2, AXON), tl_bar("thal", 19.2, 20.6, AXON, 0.85), tl_birth())
    if with_bar:
        g.add(tl_label("bar", "barrels visible", GREEN), tl_bar("bar", 23, 24.1, GREEN, 0.9))
    return g


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Mapping the Cortex: Areas and Arealization"
    TITLE = "A Sheet with No Borders"


# ---------------------------------------------------------------------------------------------
BIG = CMap(1.15, (0.0, 0.5))
PL, PR = CMap(0.64, (-3.45, 0.95)), CMap(0.64, (3.45, 0.95))   # the two maps side by side, as large as the width allows


def adult_group(cm):
    return VGroup(cm.outline(fo=0.08), *[cm.patch(n, 0.5, 2.5) for n in AREAS])


class S01(SpokenScene):
    """the adult map drawn large; the embryonic sheet joins it after it has moved aside; the question."""

    def construct(self):
        big = adult_group(BIG)
        small = adult_group(PL)
        tag_big = T("adult cortex", 36, TEXT).move_to([0, -3.0, 0])
        tag_small = T("adult cortex", 38, TEXT).move_to([-3.45, -1.2, 0])
        e_sheet = PR.outline(fo=0.24)
        tag_e = T("embryo cortex", 38, TEXT).move_to([3.45, -1.2, 0])
        self.play(Create(big[0]), run_time=0.35)
        self.at("adult cortex")
        self.play(FadeIn(tag_big), run_time=0.4)
        self.at("into areas")
        self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in big[1:]], lag_ratio=0.3), run_time=1.2)
        self.at("embryo's")
        self.play(Transform(big, small), Transform(tag_big, tag_small), run_time=0.7)
        self.play(FadeIn(e_sheet), FadeIn(tag_e), run_time=0.4)
        self.at("no borders")
        self.play(Indicate(e_sheet, color=TEXT, scale_factor=1.04), run_time=0.7)
        q = T("So where do the areas come from?", 52, TEXT, font=TITLE_FONT).move_to([0, -2.6, 0])
        mark = T("?", 84, QCOL, weight=BOLD).move_to([0, 0.95, 0])
        self.at("So where")
        self.play(FadeIn(q), run_time=0.4)
        self.at("where do the areas")
        self.play(FadeIn(mark, scale=0.6), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
FORE = [(-4.6, -0.5), (-4.5, 0.5), (-3.9, 1.4), (-2.8, 2.1), (-1.3, 2.5), (0.5, 2.55), (2.2, 2.2), (3.6, 1.4), (4.3, 0.2),
        (4.0, -1.0), (3.0, -1.6), (1.6, -1.85), (0.0, -1.95), (-1.6, -1.8), (-3.1, -1.4)]


class S02(SpokenScene):
    """a mouse brain from the side, forebrain drawn as the big dome; the outer sheet highlights."""

    def construct(self):
        s, c = 0.95, (0.2, 0.4)
        D = catmull(FORE, 14)
        bulb = shape(blobpts(-5.25, -0.1, 0.8, 0.5, 0.4), 1.0, (0, 0), GREY, GREY, 0.1, 3)
        cereb = shape(blobpts(3.6, -1.95, 1.35, 0.75, 0.3), 1.0, (0, 0), GREY, GREY, 0.1, 3)
        stem = shape(blobpts(1.0, -2.85, 0.55, 0.85, 0.0), 1.0, (0, 0), GREY, GREY, 0.1, 3)
        brain = shape(D, s, c, GREY, GREY, 0.2, 4)
        rim = shape(D, s, c, NEURON, NEURON, 0, 14)
        step = max(1, len(D) // 44)
        dots = VGroup(*[Circle(radius=0.1, stroke_color=NEURON, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(
            [c[0] + s * x, c[1] + s * y, 0]) for x, y in D[::step]])
        l_cortex = T("cortex", 40, NEURON, weight=BOLD).move_to([0.6, 3.45, 0])
        lead = Line([0.6, 3.15, 0], [0.6, c[1] + s * 2.55 + 0.1, 0], stroke_color=NEURON, stroke_width=3)
        l_fore = T("forebrain", 48, TEXT).move_to([0.2, 0.45, 0])
        self.play(FadeIn(VGroup(bulb, cereb, stem), shift=UP * 0.1), FadeIn(brain, shift=UP * 0.1), run_time=0.5)
        self.at("cortex")
        self.play(Create(rim), FadeIn(l_cortex), Create(lead), run_time=0.85)
        self.at("sheet of neurons")
        self.play(FadeIn(dots, lag_ratio=0.04), run_time=1.0)
        self.at("forebrain")
        self.play(FadeIn(l_fore), Indicate(brain, color=TEXT, scale_factor=1.02), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
H3 = Human(1.3, (2.2, -0.1))
SEC_C, SEC_W, SEC_H = (-4.95, 0.1), 3.2, 4.8


def s03_state():
    """everything on screen at the end of the Brodmann scene (rebuilt at the start of the next one)."""
    frame, dots, lines, _rects = stained_section(SEC_C, SEC_W, SEC_H)
    sect = VGroup(frame, dots, lines)
    title = T("Brodmann, 1909", 44, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
    cap = VGroup(T("cells packed", 26, TEXT), T("and layered", 26, TEXT)).arrange(DOWN, buff=0.1).move_to([SEC_C[0], -3.05, 0])
    arr = Arrow([-3.2, 0.1, 0], [-2.25, 0.1, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.22)
    body = H3.body()
    patches = VGroup(*[H3.patch(k) for k in HPATCH])
    nums = VGroup(*[H3.num(k) for k in HPATCH])
    return dict(sect=sect, title=title, cap=cap, arr=arr, body=body, patches=patches, nums=nums)


class S03(SpokenScene):
    """Brodmann, 1909: a stained section first, then the human brain with numbered patches growing out of its dense bands."""

    def construct(self):
        st = s03_state()
        sect = st["sect"]
        rects = stained_section(SEC_C, SEC_W, SEC_H)[3]
        sect_c = T("stained section", 26, GREY).move_to([SEC_C[0], -3.05, 0])
        self.play(FadeIn(st["title"], shift=DOWN * 0.15), FadeIn(sect[0]), run_time=0.6)
        self.play(FadeIn(sect[1], lag_ratio=0.002), FadeIn(sect_c), run_time=1.0)
        self.at("human cortex")
        self.play(FadeIn(st["body"], shift=LEFT * 0.2), FadeOut(sect_c), run_time=0.8)
        self.at("into areas")
        src = [rects[i] for i in (7, 5, 3, 1, 3, 5)]
        self.play(LaggedStart(*[AnimationGroup(TransformFromCopy(r, p), FadeIn(n)) for r, p, n in zip(src, st["patches"], st["nums"])],
                              lag_ratio=0.25), run_time=1.6)
        self.at("how its cells")
        self.play(FadeIn(st["cap"]), GrowArrow(st["arr"]), Indicate(sect[1], color=NEURON, scale_factor=1.03), run_time=0.9)
        self.at("layered")
        self.play(Create(sect[2]), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
H4 = Human(1.45, (-1.0, 0.25))
L17 = [3.7, 0.0]


def s04_state():
    """final picture of the Brodmann-function scene (carried into the next scene)."""
    H = H4
    body = H.body()
    patches = VGroup(*[H.patch(k, PINK if k == "17" else None, 0.9 if k == "17" else 0.12) for k in HPATCH])
    nums = VGroup(*[H.num(k) for k in HPATCH])
    l17 = T("area 17", 40, PINK, weight=BOLD).move_to([5.0, 1.95, 0])
    lv = VGroup(T("primary visual", 30, TEXT), T("cortex", 30, TEXT)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([5.0, 1.1, 0])
    lv.align_to(l17, LEFT)
    eye = eye_icon(1.5, (5.4, -1.9))
    l_eye = T("eyes", 28, GREY).move_to([5.4, -2.8, 0])
    return dict(body=body, patches=patches, nums=nums, l17=l17, lv=lv, eye=eye, l_eye=l_eye)


class S04(SpokenScene):
    """area 17 lights up at the back; the eye connects to it."""

    def construct(self):
        st3 = s03_state()
        body, patches, nums = st3["body"], st3["patches"], st3["nums"]
        self.add(*st3.values())
        H = H4
        body2 = H.body()
        patches2 = VGroup(*[H.patch(k) for k in HPATCH])
        nums2 = VGroup(*[H.num(k) for k in HPATCH])
        self.play(FadeOut(st3["sect"]), FadeOut(st3["title"]), FadeOut(st3["cap"]), FadeOut(st3["arr"]),
                  Transform(body, body2), Transform(patches, patches2), Transform(nums, nums2), run_time=0.9)
        st = s04_state()
        self.at("match borders")
        self.play(Indicate(patches, color=TEXT, scale_factor=1.06), run_time=1.1)
        self.at("area 17")
        self.play(Transform(patches[5], st["patches"][5]), FadeIn(st["l17"], shift=LEFT * 0.15), run_time=0.8)
        self.at("primary visual cortex")
        self.play(FadeIn(st["lv"], shift=UP * 0.1), run_time=0.8)
        route = ArcBetweenPoints([4.75, -1.25, 0], [3.1, -0.1, 0], angle=0.5, stroke_color=PINK, stroke_width=5)
        route.add_tip(tip_length=0.24)
        self.at("first cortical stop")
        self.play(FadeIn(st["eye"]), FadeIn(st["l_eye"]), Create(route), run_time=1.2)
        self.at("signals from the eyes")
        pulse = Dot(route.get_start(), radius=0.12, color=TEXT)
        self.play(MoveAlongPath(pulse, ArcBetweenPoints([4.75, -1.25, 0], [3.1, -0.1, 0], angle=0.5)), run_time=1.3)
        self.play(Indicate(patches[5], color=TEXT, scale_factor=1.15), FadeOut(pulse), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    """transition to the mouse hemisphere: the map used throughout."""

    def construct(self):
        st = s04_state()
        route = ArcBetweenPoints([4.75, -1.25, 0], [3.1, -0.1, 0], angle=0.5, stroke_color=PINK, stroke_width=5)
        route.add_tip(tip_length=0.24)
        old = VGroup(*st.values(), route)
        self.add(old)
        mouse = nose_icon()
        tag = T("mouse", 34, TEXT, font=TITLE_FONT).move_to([-6.1, -1.15, 0])
        outline = MAIN.outline(fo=0.16)
        self.play(FadeOut(old), run_time=0.5)
        self.at("mouse")
        self.play(FadeIn(outline, scale=0.95), FadeIn(mouse), FadeIn(tag), run_time=0.8)
        note = T("one hemisphere, seen from above", 30, GREY).move_to([0.45, 0.25, 0])
        self.at("Here is the map")
        self.play(FadeOut(tag), FadeIn(note), Indicate(outline, color=TEXT, scale_factor=1.03), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06(SpokenScene):
    """front to back."""

    def construct(self):
        outline = MAIN.outline(fo=0.16)
        nose = nose_icon()
        self.add(outline, nose)
        fb = fb_axis()
        self.at("Front to back")
        self.play(GrowArrow(fb[0]), FadeIn(fb[1]), run_time=1.5)
        self.at("nose end")
        self.play(Indicate(nose, color=TEXT, scale_factor=1.25), Indicate(fb[1], color=TEXT), run_time=0.8)
        self.at("back of the head")
        self.play(FadeIn(fb[2]), Indicate(fb[2], color=TEXT), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07(SpokenScene):
    """medial and lateral: the edges themselves are marked."""

    def construct(self):
        outline = MAIN.outline(fo=0.16)
        fb = fb_axis()
        nose = nose_icon()
        self.add(outline, fb, nose)
        el = edge_labels()
        med = MAIN.medial()
        self.at("medial edge")
        self.play(Create(med), FadeIn(el[0]), run_time=1.2)
        self.at("midline")
        self.play(Indicate(med, color=TEXT, scale_factor=1.0), run_time=0.9)
        lat = MAIN.lateral()
        self.at("lateral edge")
        self.play(FadeOut(med), Create(lat), FadeIn(el[1]), run_time=1.2)
        self.at("outer side")
        self.play(Indicate(lat, color=TEXT, scale_factor=1.0), run_time=0.9)
        self.play(FadeOut(lat), run_time=0.4)
        self.finish()


def base_map():
    """outline, axes, head and grey edge labels, carried from the earlier scenes."""
    return VGroup(MAIN.outline(fo=0.16), fb_axis(), nose_icon(), edge_labels())


# ---------------------------------------------------------------------------------------------
class S08(SpokenScene):
    def construct(self):
        self.add(base_map())
        p = MAIN.patch("motor", 0.5)
        lab = MAIN.label("motor")
        self.at("Motor")
        self.play(FadeIn(p, scale=0.6), run_time=0.8)
        self.play(FadeIn(lab), run_time=0.4)
        self.finish()


def barrel_labels():
    return (T("barrel field", 26, GREEN).move_to(MAIN.P(-0.3, -1.4)), T("whisker rows", 26, GREEN).move_to(MAIN.P(-0.3, -1.85)))


class S09(SpokenScene):
    def construct(self):
        bm = base_map()
        self.add(bm)
        self.add(MAIN.patch("motor", 0.5), MAIN.label("motor"))
        p = MAIN.patch("touch", 0.5)
        lab = MAIN.label("touch", "somatosensory", 26, dy=0.72)
        sub = MAIN.label("touch", "touch", 26, GREEN, dy=0.38)
        self.at("Somatosensory")
        self.play(FadeIn(p, scale=0.6), run_time=0.8)
        self.play(FadeIn(lab), run_time=0.4)
        self.at("touch area")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
        dots = MAIN.barrels(**BAR_KW)
        l_bf, l_wr = barrel_labels()
        self.at("barrel field")
        self.play(FadeIn(dots, lag_ratio=0.06), FadeIn(l_bf), run_time=1.0)
        nose = bm[2]
        self.at("whisker map")
        self.play(FadeIn(l_wr), nose[-6:].animate.set_color(GREEN), Indicate(nose, color=GREEN, scale_factor=1.25), run_time=1.1)
        self.finish()


def map_so_far(upto):
    """carry-over of the area patches named so far (upto = number of areas)."""
    g = VGroup(base_map())
    if upto >= 1:
        g.add(MAIN.patch("motor", 0.5), MAIN.label("motor"))
    if upto >= 2:
        g.add(MAIN.patch("touch", 0.5), MAIN.label("touch", "somatosensory", 26, dy=0.72), MAIN.label("touch", "touch", 26, GREEN, dy=0.38),
              MAIN.barrels(**BAR_KW), *barrel_labels())
    if upto >= 3:
        g.add(MAIN.patch("auditory", 0.5), MAIN.label("auditory", "auditory"))
    return g


class S10(SpokenScene):
    def construct(self):
        self.add(map_so_far(2))
        p = MAIN.patch("auditory", 0.5)
        lab = MAIN.label("auditory", "auditory")
        self.at("Auditory")
        self.play(FadeIn(p, scale=0.6), run_time=0.8)
        self.play(FadeIn(lab), run_time=0.4)
        lat = MAIN.lateral()
        self.at("lateral side")
        self.play(Create(lat), run_time=0.9)
        self.at("toward the back")
        ar = Arrow(MAIN.P(3.15, -1.5), MAIN.P(4.15, -1.25), buff=0, color=SAND, stroke_width=6, tip_length=0.22)
        self.play(GrowArrow(ar), FadeOut(lat), run_time=0.9)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        self.add(map_so_far(3))
        p = MAIN.patch("visual", 0.5)
        lab = MAIN.label("visual", "visual")
        self.at("Visual")
        self.play(FadeIn(p, scale=0.6), run_time=0.8)
        self.play(FadeIn(lab), run_time=0.4)
        self.at("back")
        self.play(Indicate(p, color=PINK, scale_factor=1.06), run_time=0.9)
        self.finish()


def map_pieces(cm):
    """the whole labelled map at any scale: outline, patches, labels, barrels."""
    g = VGroup(cm.outline(fo=0.16))
    for n in AREAS:
        g.add(cm.patch(n, 0.5))
    g.add(cm.label("motor"), cm.label("touch", "somatosensory", 26, dy=0.72), cm.label("touch", "touch", 26, GREEN, dy=0.38),
          cm.barrels(**BAR_KW), cm.label("auditory", "auditory"), cm.label("visual", "visual"))
    return g


def s12_brackets():
    yb = 2.55
    x0, x1 = SMALL.P(-4.4, 0)[0], SMALL.P(1.5, 0)[0]
    vx0, vx1 = SMALL.P(2.5, 0)[0], SMALL.P(4.6, 0)[0]
    br = bracket(x0, x1, yb, TEXT)
    lab = T("front-and-middle areas", 30, TEXT).move_to([(x0 + x1) / 2, yb + 0.45, 0])
    br2 = bracket(vx0, vx1, yb, PINK)
    lab2 = T("back area", 30, PINK).move_to([(vx0 + vx1) / 2, yb + 0.45, 0])
    return br, lab, br2, lab2


class S12(SpokenScene):
    def construct(self):
        old = VGroup(map_pieces(MAIN), fb_axis(), nose_icon(), edge_labels())
        self.add(old)
        new = map_pieces(SMALL)
        self.play(FadeOut(old), FadeIn(new), run_time=0.7)
        br, lab, br2, lab2 = s12_brackets()
        self.at("motor and somatosensory")
        self.play(Create(br), run_time=0.8)
        self.at("front and middle")
        self.play(FadeIn(lab, shift=UP * 0.1), Indicate(VGroup(new[1], new[2]), color=TEXT, scale_factor=1.02), run_time=1.0)
        self.at("visual is")
        self.play(Create(br2), Indicate(new[4], color=PINK, scale_factor=1.05), run_time=0.7)
        self.at("back area")
        self.play(FadeIn(lab2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13(SpokenScene):
    """a smooth sheet of progenitors, cells that divide to make neurons."""

    def construct(self):
        new = map_pieces(SMALL)
        br, lab, br2, lab2 = s12_brackets()
        self.add(new, br, lab, br2, lab2)
        self.wait(0.2)
        big = SHEET.outline(fo=0.24)
        cells = sheet_cells(SHEET)
        self.play(FadeOut(VGroup(br, lab, br2, lab2)), run_time=0.5)
        self.at("smooth sheet")
        self.play(FadeOut(VGroup(*new[1:])), Transform(new[0], big), run_time=1.0)
        lg_p = VGroup(cell(0, 0, 0.13), T("progenitors", 30, GREY)).arrange(RIGHT, buff=0.2).move_to([-2.4, 3.45, 0])
        self.at("progenitors")
        self.play(FadeIn(cells, lag_ratio=0.02, scale=0.5), FadeIn(lg_p), run_time=1.1)
        pick = [cells[i] for i in range(2, len(cells), 5)]
        kids = []
        self.at("cells that divide")
        anims = []
        for c in pick:
            k = c.copy()
            kids.append(k)
            self.add(k)
            anims += [c.animate.shift(LEFT * 0.16), k.animate.shift(RIGHT * 0.16)]
        self.play(*anims, run_time=1.0)
        lg_n = VGroup(cell(0, 0, 0.13, NEURON, 0.85), T("neurons", 30, NEURON)).arrange(RIGHT, buff=0.2).move_to([2.0, 3.45, 0])
        self.at("make neurons")
        self.play(*[k.animate.set_color(NEURON).set_fill(NEURON, 0.85) for k in kids], FadeIn(lg_n), run_time=1.0)
        self.finish()


class S14(SpokenScene):
    """the sheet looks the same from front to back; future outlines flicker and fade."""

    def construct(self):
        sheet = SHEET.outline(fo=0.24)
        cells = sheet_cells(SHEET).set_opacity(0.3)
        self.add(sheet, cells)
        d_bar = DashedVMobject(shape(blobpts(-0.3, -0.35, 1.05, 0.75, 0.4), SHEET.s, SHEET.c, GREEN, GREEN, 0, 4), num_dashes=36)
        d_vis = SHEET.dashed("visual", 40, 4)
        lb = plate(T("whisker map", 28, GREEN, weight=BOLD)).move_to(SHEET.P(-0.3, -0.35))
        lv = plate(T("visual map", 28, PINK, weight=BOLD)).move_to(SHEET.P(3.55, 0.45))
        self.at("whisker map")
        self.play(Create(d_bar), FadeIn(lb), run_time=0.8)
        self.at("visual map")
        self.play(Create(d_vis), FadeIn(lv), run_time=0.8)
        self.at("looks the same")
        self.play(FadeOut(d_bar), FadeOut(d_vis), FadeOut(lb), FadeOut(lv), run_time=0.9)
        fb = fb_axis()
        band = Rectangle(width=0.7, height=5.9, stroke_width=0, fill_color=TEXT, fill_opacity=0.18).move_to([-5.8, 0.0, 0])
        self.at("front to back")
        self.add(band)
        self.play(GrowArrow(fb[0]), FadeIn(fb[1]), FadeIn(fb[2]), band.animate.move_to([5.8, 0.0, 0]), run_time=1.3, rate_func=linear)
        self.play(FadeOut(band), run_time=0.2)
        self.finish()


class S15(SpokenScene):
    """arealization: sheet becomes map; the word on screen."""

    def construct(self):
        sheet = SHEET.outline(fo=0.24)
        cells = sheet_cells(SHEET).set_opacity(0.3)
        fb = fb_axis()
        self.add(sheet, cells, fb)
        top, bot = CMap(0.55, (-2.9, 1.95)), CMap(0.55, (-2.9, -1.75))
        sheet_s = top.outline(fo=0.24)
        self.at("Making")
        self.play(ReplacementTransform(sheet, sheet_s), FadeOut(cells), FadeOut(fb), run_time=0.7)
        adult = VGroup(bot.outline(fo=0.08), bot.patches(fo=0.5, sw=2.5))
        arrow = Arrow([-2.9, 0.42, 0], [-2.9, -0.3, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.28)
        l_arrow = T("make the areas", 28, TEXT).move_to([-0.5, 0.12, 0])
        self.at("areas from it")
        self.play(GrowArrow(arrow), FadeIn(l_arrow), FadeIn(adult, shift=UP * 0.2), run_time=1.0)
        word = T("arealization", 64, TEXT, font=TITLE_FONT).move_to([3.6, -1.5, 0])
        rule = Line(LEFT * 2.6, RIGHT * 2.6, color=TEXT, stroke_width=4).next_to(word, DOWN, buff=0.2)
        self.at("called")
        self.play(Write(word), Create(rule), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
SIGSHEET = CMap(0.62, (-1.9, 1.97))     # the small sheet that sits above the timeline in the timeline scenes


def sheet_with_spots(cm, r):
    return VGroup(cm.outline(fo=0.24),
                  VGroup(glow(*cm.P(-4.7, 0.4)[:2], r), glow(*cm.P(-1.0, 2.4)[:2], r), glow(*cm.P(2.2, 2.4)[:2], r)))


class S16(SpokenScene):
    """signalling centres at the edges, active by E9.5, running on into neurogenesis."""

    def construct(self):
        B = CMap(0.95, (0.0, -0.1))
        big = sheet_with_spots(B, 0.17)
        small = sheet_with_spots(SIGSHEET, 0.1)
        axis = tl_axis()
        self.play(FadeIn(big[0]), run_time=0.6)
        self.at("edges of the sheet")
        near = T("signalling centres", 32, YELLOW).move_to(B.P(0.5, 2.4) + UP * 1.25)
        self.play(FadeIn(big[1], scale=0.4, lag_ratio=0.25), FadeIn(near), run_time=1.0)
        self.play(Indicate(big[1], color=YELLOW, scale_factor=1.4), run_time=0.8)
        lab = tl_label("sig", "signalling centres", YELLOW)
        near2 = T("signalling centres", 30, YELLOW).move_to([2.9, 3.07, 0])
        lead = Line([1.3, 3.07, 0], [-0.3, 3.27, 0], stroke_color=YELLOW, stroke_width=3)
        self.at("embryonic day")
        self.play(ReplacementTransform(big, small), ReplacementTransform(near, near2), Create(lead), FadeIn(axis), FadeIn(lab), run_time=1.1)
        spots = small[1]
        solid, fade = sig_bar()
        e95 = e95_label()
        self.at("nine and a half")
        self.play(FadeIn(e95), Indicate(spots, color=YELLOW, scale_factor=1.3), GrowFromEdge(solid, LEFT), run_time=0.9)
        self.at("keep signaling")
        self.play(LaggedStart(*[FadeIn(r) for r in fade], lag_ratio=0.12), Indicate(spots, color=YELLOW, scale_factor=1.3), run_time=1.5)
        n_lab = tl_label("neu", "neurons made", NEURON)
        first = Dot([tx(11), ROW["neu"], 0], radius=0.15, color=NEURON)
        self.at("first neurons")
        self.play(FadeIn(n_lab), FadeIn(first, scale=0.4), run_time=0.8)
        self.finish()


def s16_final():
    """timeline state at the end of the signalling scene: axis, signalling row, 'neurons made' with its first dot."""
    sb = sig_bar()
    return VGroup(tl_axis(), tl_label("sig", "signalling centres", YELLOW), *sb,
                  e95_label(),
                  tl_label("neu", "neurons made", NEURON), Dot([tx(11), ROW["neu"], 0], radius=0.15, color=NEURON))


class S17(SpokenScene):
    """progenitors make neurons from about E11 to E17; neurons pile up above the progenitors."""

    def construct(self):
        tl = s16_final()
        axis = tl[0]
        self.add(tl)
        xs = [-3.0 + i * 0.75 for i in range(9)]
        Y0 = 0.7
        base = Rectangle(width=7.0, height=0.34, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3).move_to([0, Y0, 0])
        prog = VGroup(*[cell(x, Y0, 0.12) for x in xs])
        l_prog = T("progenitors", 30, GREY).move_to([-5.3, Y0, 0])
        self.play(FadeIn(base), FadeIn(prog), FadeIn(l_prog), run_time=0.6)
        levels = [VGroup(*[neuron_dot(x, 1.2 + k * 0.4, 0.14) for x in xs]) for k in range(6)]
        l_neu = T("neurons", 30, NEURON).move_to([-5.3, 2.3, 0])
        self.at("make the")
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in levels[0]], lag_ratio=0.08), FadeIn(l_neu), run_time=1.0)
        bar_n = tl_bar("neu", 11, 17, NEURON, 0.8)
        self.at("embryonic day")
        self.play(Indicate(tl_ticklabel(axis, 1), color=NEURON), run_time=0.6)
        self.at("11")
        self.play(GrowFromEdge(bar_n, LEFT, rate_func=linear), LaggedStart(*[FadeIn(lv, shift=UP * 0.15) for lv in levels[1:]], lag_ratio=1.0),
                  run_time=1.3)
        self.play(Indicate(tl_ticklabel(axis, 4), color=NEURON), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18(SpokenScene):
    """the thalamus is the relay station for signals from eyes, ears and skin."""

    def construct(self):
        E = CMap(0.45, (0.0, 2.3))
        sheet = E.outline(fo=0.2)
        self.add(sheet, T("cortex", 28, NEURON).move_to(E.P(0, 0.2)))
        thal = thalamus_blob((0, -0.05), 1.2, AXON, "thalamus", 32)
        self.at("thalamus")
        self.play(FadeIn(thal, shift=UP * 0.2), run_time=0.9)
        self.at("relay station")
        self.play(Indicate(thal[0], color=TEXT, scale_factor=1.08), run_time=1.0)
        eye = eye_icon(1.6, (-4.2, -2.35))
        ear = ear_icon(1.6, (0.0, -2.35))
        skin = hand_icon(1.1, (4.2, -2.3))
        labs = [T("eyes", 28, GREY).move_to([-4.2, -3.4, 0]), T("ears", 28, GREY).move_to([0, -3.4, 0]),
                T("skin", 28, GREY).move_to([4.2, -3.4, 0])]
        arrows = [Arrow([-3.3, -1.8, 0], [-1.2, -0.55, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.24),
                  Arrow([0, -1.5, 0], [0, -0.88, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.24),
                  Arrow([3.3, -1.7, 0], [1.2, -0.55, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.24)]
        for key, ic, lb, ar in zip(("eyes", "ears", "skin"), (eye, ear, skin), labs, arrows):
            self.at(key)
            self.play(FadeIn(ic, scale=0.6), FadeIn(lb), GrowArrow(ar), run_time=0.8)
        self.finish()


def question_frame():
    axis = tl_axis()
    q = T("Which comes first?", 72, TEXT, font=TITLE_FONT).move_to([0, 2.7, 0])
    c1 = chip("neurons made", NEURON, 38).move_to([-3.4, 0.95, 0])
    c2 = chip("thalamic axons arrive", AXON, 38).move_to([3.6, 0.95, 0])
    or_ = T("or", 38, GREY).move_to([-0.1, 0.95, 0])
    m1 = T("?", 90, QCOL, weight=BOLD).move_to([-0.6, -1.1, 0])
    m2 = T("?", 90, QCOL, weight=BOLD).move_to([0.6, -1.1, 0])
    return axis, q, c1, c2, or_, m1, m2


class S19(SpokenScene):
    def construct(self):
        axis, q, c1, c2, or_, m1, m2 = question_frame()
        self.add(axis, m1, m2)   # the neutral pair of markers is there from the start, tied to no date
        self.at("which comes first")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.at("neurons of the cortex")
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.9)
        self.at("thalamic axons")
        self.play(FadeIn(or_), FadeIn(c2, shift=DOWN * 0.2), run_time=0.9)
        self.finish()


class S20Pause(NarratedScene):
    """silent: the question holds still; a quiet cue says 'think'."""

    def construct(self):
        axis, q, c1, c2, or_, m1, m2 = question_frame()
        self.add(axis, q, c1, c2, or_, m1, m2)
        think = T("think about it", 34, GREY).move_to([0, -2.3, 0])
        self.play(FadeIn(think), run_time=0.6)
        for _ in range(2):
            rings = VGroup(*[Circle(radius=0.55, stroke_color=QCOL, stroke_width=4, stroke_opacity=0.9).move_to(m.get_center()) for m in (m1, m2)])
            self.add(rings)
            self.play(*[r.animate.scale(1.35).set_stroke(opacity=0) for r in rings], run_time=2.1, rate_func=linear)
            self.remove(rings)
        self.wait(0.2)


# ---------------------------------------------------------------------------------------------
STK_C = (-1.4, -4.1)    # centre of the circles that make the side-view arcs
R_CTX, R_SUB = (6.9, 7.4), (6.5, 6.85)
ANG = 34


def arc_pt(R, deg, c=STK_C):
    a = np.radians(deg)
    return np.array([c[0] + R * np.sin(a), c[1] + R * np.cos(a), 0.0])


def stack_parts():
    """a side view: cortex sheet, the layer just under it, thalamus below. A picture of places, not of time."""
    kw = dict(angle=np.radians(2 * ANG), start_angle=np.radians(90 - ANG), arc_center=[STK_C[0], STK_C[1], 0])
    cortex = AnnularSector(inner_radius=R_CTX[0], outer_radius=R_CTX[1], stroke_color=NEURON, stroke_width=3,
                           fill_color=NEURON, fill_opacity=0.18, **kw)
    sub = AnnularSector(inner_radius=R_SUB[0], outer_radius=R_SUB[1], stroke_color=GREY, stroke_width=3,
                        fill_color=GREY, fill_opacity=0.3, **kw)
    thal = thalamus_blob((STK_C[0], 0.8), 1.05, AXON, "thalamus", 28)
    l_cx = T("cortex", 30, NEURON).move_to([4.1, 2.85, 0])
    lead_c = Line([3.35, 2.75, 0], arc_pt(7.15, 31) + RIGHT * 0.1, stroke_color=NEURON, stroke_width=3)
    return cortex, sub, thal, l_cx, lead_c


class S21(SpokenScene):
    """the answer: neurons first; thalamic axons arrive around E14-15, wait, enter near birth."""

    def construct(self):
        q = question_frame()
        axis = q[0]
        self.add(*q)
        cortex, sub, thal, l_cx, lead_c = stack_parts()
        solid, fade = sig_bar()
        sig_rows = VGroup(tl_label("sig", "signalling centres", YELLOW), solid, fade)
        n_lab = tl_label("neu", "neurons made", NEURON)
        t_lab = tl_label("thal", "thalamic axons", AXON)
        self.play(FadeOut(VGroup(*q[1:])), FadeIn(VGroup(cortex, sub, thal, l_cx, lead_c)), FadeIn(sig_rows), run_time=0.4)
        # neurons already in the cortex band
        a_first = [-16, -8, 0, 8, 16]
        a_more = [-28, -23, -12, -4, 4, 12, 23, 28]
        first = VGroup(*[neuron_dot(*arc_pt(7.15, a)[:2], 0.1) for a in a_first])
        more = VGroup(*[neuron_dot(*arc_pt(7.15, a)[:2], 0.1) for a in a_more])
        nbar1 = tl_bar("neu", 11, 13, NEURON, 0.8, sw=0)
        nbar2 = tl_bar("neu", 12.97, 17, NEURON, 0.8, sw=0)
        self.at("first neurons")
        self.play(FadeIn(n_lab), FadeIn(first, lag_ratio=0.15), GrowFromEdge(nbar1, LEFT), run_time=1.4)
        # axons rise from the thalamus to the layer just under the sheet
        degs = [-20, -7, 7, 20]
        tops = [arc_pt(6.68, d) for d in degs]
        axons = VGroup(*[CubicBezier([STK_C[0] + (t[0] - STK_C[0]) * 0.35, 1.35, 0], [STK_C[0] + (t[0] - STK_C[0]) * 0.35, 1.8, 0],
                                     t - UP * 0.5, t, stroke_color=AXON, stroke_width=4) for t in tops])
        self.at("axons reach")
        self.play(LaggedStart(*[Create(a) for a in axons], lag_ratio=0.15), run_time=2.2)
        arr_bar = tl_bar("thal", 14, 15, AXON, 0.85)
        call = T("E14 to 15", 26, AXON).move_to([tx(14.5), ROW["thal"] - 0.4, 0])
        self.at("14 to 15")
        self.play(FadeIn(t_lab), GrowFromEdge(arr_bar, LEFT), FadeIn(call), Indicate(tl_ticklabel(axis, 3), color=AXON), run_time=1.0)
        wait_line = tl_dashed("thal", 15, 19.2, AXON)
        wait_l = T("waiting", 26, AXON).move_to([tx(18.2), ROW["thal"] - 0.4, 0])
        stops = VGroup(*[Dot(t, radius=0.1, color=AXON) for t in tops])
        self.at("wait in the layer")
        self.play(Create(wait_line), FadeIn(wait_l), FadeIn(stops), run_time=0.6)
        l_sub = T("layer just under", 28, GREY).move_to([4.95, 1.45, 0])
        lead_s = Line([3.55, 1.45, 0], arc_pt(6.68, 31) + RIGHT * 0.1, stroke_color=GREY, stroke_width=3)
        self.at("layer just under")
        self.play(FadeIn(l_sub), Create(lead_s), run_time=0.8)
        self.at("More neurons")
        self.play(FadeIn(more, lag_ratio=0.1), GrowFromEdge(nbar2, LEFT), run_time=1.3)
        into = VGroup(*[Line(t, arc_pt(7.2, d), stroke_color=AXON, stroke_width=4) for t, d in zip(tops, degs)])
        enter_bar = tl_bar("thal", 19.2, 20.6, AXON, 0.85)
        enter_l = plate(VGroup(T("grow into the cortex,", 26, AXON), T("near birth", 26, AXON)).arrange(DOWN, buff=0.06)).move_to([5.0, ROW["thal"] - 0.55, 0])
        bl = tl_birth()
        self.at("axons grow into")
        self.play(FadeOut(wait_l), run_time=0.25)
        self.play(GrowFromEdge(enter_bar, LEFT), FadeIn(enter_l),
                  LaggedStart(*[Create(i) for i in into], lag_ratio=0.15), run_time=1.55)
        self.at("around birth")
        self.play(Create(bl), Indicate(tl_ticklabel(axis, 5), color=AXON), run_time=1.0)
        self.finish()


class S22(SpokenScene):
    """barrels are visible around P4: blurred dots sharpen into rows as the bar grows."""

    def construct(self):
        axis = tl_axis()
        rows = tl_final(False)
        self.add(axis, rows)
        b_lab = tl_label("bar", "barrels visible", GREEN)
        # barrel field: the same 3 rows of 5 as on the map, large
        pos = [(-2.0 + i * 1.0, 3.0 - j * 1.05) for j in range(3) for i in range(5)]
        soft = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color=GREEN, fill_opacity=0.28).move_to([x - 0.9, y, 0]) for x, y in pos])
        crisp = VGroup(*[Circle(radius=0.3, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.85).move_to([x - 0.9, y, 0]) for x, y in pos])
        cap = VGroup(T("barrel field", 32, GREEN), T("whisker rows", 28, GREEN)).arrange(DOWN, buff=0.12).move_to([4.2, 2.1, 0])
        self.play(FadeIn(soft), FadeIn(cap), run_time=0.9)
        self.at("postnatal week")
        seg = Line([tx(19.5), AXY, 0], [tx(23.5), AXY, 0], stroke_color=GREEN, stroke_width=7)
        self.play(Create(seg), run_time=0.9)
        bar = tl_bar("bar", 23, 24.1, GREEN, 0.9)
        self.at("postnatal day")
        self.play(ReplacementTransform(soft, crisp, rate_func=linear), FadeIn(b_lab), GrowFromEdge(bar, LEFT, rate_func=linear), Indicate(tl_ticklabel(axis, 6), color=GREEN), run_time=1.8)
        self.finish()


def tinted_sheet(cm):
    """the embryonic sheet with the signalling spots and a faint graded tint spreading from each."""
    out = cm.outline(fo=0.24)
    g = VGroup(out)
    spots = [(-4.7, 0.4), (-1.0, 2.4), (2.2, 2.4)]
    for (x, y) in spots:
        for rr, op in ((2.2, 0.06), (1.5, 0.08), (0.85, 0.12)):
            circ = Circle(radius=rr * cm.s, stroke_width=0, fill_color=YELLOW, fill_opacity=op).move_to(cm.P(x, y))
            try:
                part = Intersection(circ, out, stroke_width=0, fill_color=YELLOW, fill_opacity=op)
                g.add(part)
            except Exception:
                pass
    g.add(VGroup(*[glow(*cm.P(x, y)[:2], 0.075) for x, y in spots]))
    return g


class S23(SpokenScene):
    """before the axons arrive the sheet is already patterned and making neurons."""

    def construct(self):
        axis = tl_axis()
        rows = tl_final(True)
        self.add(axis, rows)
        E = CMap(0.6, (3.95, 1.6))
        yb = 0.12
        x0, x1 = tx(9.3), tx(14.0)
        br = bracket(x0, x1, yb, TEXT, -0.2)
        lab = T("before the axons arrive", 30, TEXT).move_to([(x0 + x1) / 2 - 0.3, yb + 0.42, 0])
        sheet = tinted_sheet(E)
        neurons = VGroup(*[cell(*E.P(x, y)[:2], r=0.08, color=NEURON, fo=0.85) for x, y in
                           [(-3, 0), (-2, -1), (-1, 0.5), (0, -0.8), (1, 0.4), (2, -1), (3, 0.3), (-2, 1.2), (1, -1.6), (3.2, -1.2)]])
        l_sheet = VGroup(T("marked by signals,", 36, TEXT), T("making neurons", 36, TEXT)).arrange(DOWN, buff=0.15).move_to([-3.2, 2.45, 0])
        self.at("So the sheet")
        self.play(Create(br), FadeIn(lab, shift=UP * 0.1), FadeIn(sheet[0]), run_time=0.8)
        self.at("already patterned")
        self.play(FadeIn(VGroup(*sheet[1:])), FadeIn(l_sheet[0]), run_time=0.9)
        self.at("making neurons")
        self.play(FadeIn(neurons, lag_ratio=0.1), FadeIn(l_sheet[1]), run_time=0.9)
        self.at("thalamic axons")
        self.play(Indicate(rows[6], color=AXON, scale_factor=1.0), Indicate(rows[7], color=AXON, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
CW, CH = 4.1, 6.4
ART_Y = 1.15


def card(n, lines, color, c=(0, 0)):
    box = RoundedRectangle(corner_radius=0.2, width=CW, height=CH, stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=0.08)
    badge = VGroup(Circle(radius=0.3, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.25), T(str(n), 30, color, weight=BOLD))
    text = VGroup(*[T(l, 30, TEXT) for l in lines]).arrange(DOWN, buff=0.14)
    g = VGroup(box, badge, text)
    box.move_to([c[0], c[1], 0])
    badge.move_to([c[0] - CW / 2 + 0.5, c[1] + CH / 2 - 0.5, 0])
    text.move_to([c[0], c[1] - 1.4, 0])
    return g


def card_art(n, c, line_dx=0.0):
    """art that fills the upper part of the card (about 3 units tall). Card 1: a smooth sheet and a question. Card 2: a progenitor on a gradient and a line
    that can slide. Card 3: thalamus, cortex and unknown axon input."""
    x, y = c
    if n == 1:
        m = CMap(0.385, (x, y + 1.4))
        sheet = m.outline(fo=0.24)
        q = T("?", 150, QCOL, weight=BOLD).move_to([x - 0.1, y + 1.4, 0])
        return VGroup(sheet, q)
    if n == 2:
        n_col = 16
        W = 3.5
        sw = W / n_col
        strip = VGroup(*[Rectangle(width=sw + 0.005, height=1.5, stroke_width=0, fill_color=ORANGE,
                                   fill_opacity=0.06 + 0.7 * k / (n_col - 1)).move_to([x - W / 2 + sw * (k + 0.5), y + 0.95, 0])
                         for k in range(n_col)])
        frame = Rectangle(width=W, height=1.5, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to([x, y + 0.95, 0])
        prog = cell(x - 0.5, y + 2.35, 0.42, GREY, 0.7)
        q = T("?", 96, QCOL, weight=BOLD).move_to([x + 0.55, y + 2.35, 0])
        line = Line([x + 1.0 + line_dx, y + 0.05, 0], [x + 1.0 + line_dx, y + 1.85, 0], stroke_color=TEXT, stroke_width=6)
        return VGroup(strip, frame, prog, q, line)
    th = thalamus_blob((x, y + 0.85), 0.85, AXON, "", 22)
    sh = Rectangle(width=2.8, height=0.5, stroke_color=NEURON, stroke_width=3, fill_color=NEURON, fill_opacity=0.25).move_to([x + 0.3, y + 2.3, 0])
    ax = VGroup(*[DashedLine([x - 0.75 + i * 0.5, y + 1.35, 0], [x - 0.75 + i * 0.5, y + 2.05, 0], dash_length=0.1, stroke_color=AXON, stroke_width=3.5) for i in range(4)])
    q = T("?", 110, QCOL, weight=BOLD).move_to([x + 1.4, y + 1.2, 0])
    return VGroup(th, sh, ax, q)


C1_TEXT = ["Where do the", "borders come", "from?"]
C2_TEXT = ["What tells a", "progenitor", "where it sits?"]
C3_TEXT = ["What does", "thalamic input", "add?"]


def card2_sub(x):
    return VGroup(T("Can a border", 26, TEXT), T("be moved?", 26, TEXT)).arrange(DOWN, buff=0.06).move_to([x, -2.72, 0])


class S24(SpokenScene):
    def construct(self):
        c1 = card(1, C1_TEXT, QCOL, (0, 0))
        art = card_art(1, (0, 0))
        self.at("Where do")
        self.play(FadeIn(VGroup(c1, art), scale=0.92), run_time=0.8)
        self.at("sheet that shows none")
        self.play(Indicate(art[1], color=QCOL, scale_factor=1.25), run_time=0.9)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        c1 = card(1, C1_TEXT, QCOL, (0, 0))
        art1 = card_art(1, (0, 0))
        g1 = VGroup(c1, art1)
        self.add(g1)
        c2 = card(2, C2_TEXT, ORANGE, (2.4, 0))
        art2 = card_art(2, (2.4, 0))
        g2 = VGroup(c2, art2)
        self.play(g1.animate.shift(LEFT * 2.4), FadeIn(g2, shift=LEFT * 0.3), run_time=0.9)
        sub = card2_sub(2.4)
        self.at("can that be changed")
        self.play(FadeIn(sub), run_time=0.3)
        line = art2[4]
        self.play(line.animate.shift(LEFT * 0.9), run_time=0.7)
        self.play(line.animate.shift(RIGHT * 1.3), run_time=0.8)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        c1 = card(1, C1_TEXT, QCOL, (-2.4, 0))
        art1 = card_art(1, (-2.4, 0))
        c2 = card(2, C2_TEXT, ORANGE, (2.4, 0))
        art2 = card_art(2, (2.4, 0), 0.4)
        sub = card2_sub(2.4)
        self.add(c1, art1, c2, art2, sub)
        g1, g2 = VGroup(c1, art1), VGroup(c2, art2, sub)
        c3 = card(3, C3_TEXT, AXON, (4.5, 0))
        art3 = card_art(3, (4.5, 0))
        self.play(g1.animate.shift(LEFT * 2.1), g2.animate.shift(LEFT * 2.4), run_time=0.7)
        self.at("input from the thalamus")
        self.play(FadeIn(VGroup(c3, art3), shift=LEFT * 0.3), run_time=0.8)
        self.at("already been marked")
        self.play(Indicate(art3[3], color=QCOL, scale_factor=1.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S27(SpokenScene):
    """the adult map, then the smooth sheet beside it with a question between them."""

    def construct(self):
        big = adult_group(BIG)
        small = adult_group(PL)
        tag_big = T("adult cortex", 36, TEXT).move_to([0, -3.0, 0])
        tag_small = T("adult cortex", 38, TEXT).move_to([-3.45, -1.2, 0])
        e_sheet = PR.outline(fo=0.24)
        tag_e = T("embryo cortex", 38, TEXT).move_to([3.45, -1.2, 0])
        self.add(big, tag_big)
        self.at("areas are real")
        self.play(Indicate(big[1:], color=TEXT, scale_factor=1.04), run_time=0.9)
        self.at("embryonic sheet")
        self.play(Transform(big, small), Transform(tag_big, tag_small), run_time=0.6)
        self.play(FadeIn(e_sheet), FadeIn(tag_e), run_time=0.4)
        real = T("areas are real", 48, TEXT, font=TITLE_FONT).move_to([-3.45, -2.5, 0])
        nb = T("no borders yet", 48, TEXT, font=TITLE_FONT).move_to([3.45, -2.5, 0])
        self.at("no borders")
        self.play(FadeIn(nb, shift=UP * 0.15), FadeIn(real, shift=UP * 0.15), Indicate(e_sheet, color=TEXT, scale_factor=1.04), run_time=0.8)
        mark = T("?", 84, QCOL, weight=BOLD).move_to([0, 0.95, 0])
        self.at("next chapters")
        self.play(FadeIn(mark, scale=0.6), run_time=0.8)
        self.at("draws them")
        self.play(Indicate(mark, color=QCOL, scale_factor=1.3), run_time=1.0)
        self.finish()


class S28End(EndCard):
    LINE = "The areas are real;\nthe embryonic sheet shows no borders for them."
