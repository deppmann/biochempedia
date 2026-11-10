"""How Earth Got Its Oxygen (web film, 16:9).

One carried world: a cross-section of sky, sea, shallow shelf, deep basin and a volcanic shore. It is
built once (World) and changed through the film; each scene rebuilds it in the same place at the
stage the last scene left it. Close-ups are the same world seen through a moving camera.

COLOR MAP (one colour per concept, both cuts)
  BLUE    free oxygen: bubbles in water, pips in air, the gauge fill, the event band
  YELLOW  electrons: a small dot that rides on a giver and jumps to a taker
  GREEN   cyanobacteria: the one cell, its "food" block, the mat, the span on the scrubber
  GREY    takers that have not met oxygen: dissolved iron, volcanic gas, methane, land rock, silica stripes
  RED     rust: iron after it gave up its electron (flakes, red stripes). Only iron turns red
  TEAL    water: the sea's tint, the droplets the cell takes in
  GOLD    energy: sunlight
  PURPLE  the microbes that were here first (anaerobes)

Honesty: the gauge is schematic and says so; the time scrubber is linear and computed (age_x);
no cause is drawn for the rise; no path is drawn between the event and today; no molecular
structures (oxygen is a plain disc with four sockets, never two joined circles).

REUSABLE BUILDERS (plain functions; scenes_social.py imports them): band_stack, soft_glow, pip,
iron_disc, hero_bubble, jag_bubble, rust_flake, cyano_cell, droplet, microbe, pick_icon, bracket,
bookmark, gauge_parts, scrubber_parts, and the closed-form motion helpers (surf_y, hsh, ease).
Ambient motion is closed-form in film time, so it runs on across scene cuts.
"""
import json
import math
import os
import random
from pathlib import Path

import numpy as np
from bp_style import *

PURPLE = "#A78BFA"
FW, FH = 14.2222, 8.0
VIEW = np.array([-1.4, 0.6, 0.0])          # middle of the screen area the gauge and scrubber leave free
_HERE = Path(__file__).resolve().parent

# ----------------------------------------------------------------------------- film clock
try:
    _IDS = [s["id"] for s in json.loads((_HERE / "script.json").read_text())["scenes"]]
    _DUR = json.loads((_HERE / "audio" / "durations.json").read_text())
except Exception:  # imported from somewhere without the audio (the social cut sets its own clock)
    _IDS, _DUR = [], {}


def scene_t0(sid):
    """Film time at which a scene starts (each segment is its narration + the 0.4 s tail)."""
    t = 0.0
    for k in _IDS:
        if k == sid:
            return t
        t += _DUR.get(k, 0.0) + 0.4
    return 0.0


# ----------------------------------------------------------------------------- small maths
def P(x, y):
    return np.array([float(x), float(y), 0.0])


def lerp(a, b, u):
    return a + (b - a) * u


def clip01(x):
    return 0.0 if x < 0 else (1.0 if x > 1 else float(x))


def ease(u):
    u = clip01(u)
    return u * u * (3 - 2 * u)


def hsh(a, b=0.0, c=0.0):
    """Repeatable pseudo-random number in 0..1 from up to three numbers."""
    x = math.sin(a * 12.9898 + b * 78.233 + c * 37.719) * 43758.5453
    return x - math.floor(x)


# ----------------------------------------------------------------------------- world geometry
SEA_Y, SHELF_Y, BASIN_Y, MUD_Y = 0.9, -0.9, -2.3, -2.75
SHORE_X, SHELF_X0, SHELF_X1, BASIN_X0 = -4.45, -4.2, -0.8, 0.1
XL, XR, YB, YT = -9.0, 9.0, -5.6, 5.6
SUN = P(-3.0, 3.15)
CRATER = P(-5.95, 2.5)
MAT_X0, MAT_X1 = -4.05, -1.75          # the mat carpets the shelf; its right end leaves room for the old microbes
CELL_AT = P(-2.9, SHELF_Y + 0.085)          # where the first cyanobacterium sits
STRIPE_H = 0.12
SKY_TOP, SKY_LOW = "#04060D", "#1A2340"
SEA_TOP, SEA_DEEP = "#1B6672", "#06161F"
ROCK, ROCK_HI, MUD, LAND = "#1F1D26", "#3A3744", "#2B2030", "#0A0B10"
SILICA = "#AEB4BF"

# camera framings: (centre, frame width)
FULL = (P(0, 0), FW)
TIGHT_SKY = (P(0.9, 2.5), 5.4)
SEABED = (P(1.6, -1.31), 8.4)              # the sea floor (shelf edge and basin) fills the lower two thirds
BASIN = (P(3.04, -1.13), 8.53)
LIFT = (P(3.75, -1.0), 8.53)               # the water over the basin, with the shelf and its bubbles out of frame
TAKECAM = (P(-2.545, 2.01), 7.5)           # the sky and the shore, close enough to see each taking
SKYLAND = (P(-0.37, 0.5), 12.46)


def floor_y(x):
    """Height of the sea floor at x."""
    if x <= SHORE_X:
        return SEA_Y
    if x <= SHELF_X0:
        return lerp(SEA_Y, SHELF_Y, (x - SHORE_X) / (SHELF_X0 - SHORE_X))
    if x <= SHELF_X1:
        return SHELF_Y
    if x <= BASIN_X0:
        return lerp(SHELF_Y, BASIN_Y, (x - SHELF_X1) / (BASIN_X0 - SHELF_X1))
    return BASIN_Y


def slope_x(y):
    """x of the slope between shelf and basin at height y."""
    return SHELF_X1 + (y - SHELF_Y) / (BASIN_Y - SHELF_Y) * (BASIN_X0 - SHELF_X1)


def sea_color(y):
    u = clip01((SEA_Y - y) / (SEA_Y - (BASIN_Y - 0.4)))
    return interpolate_color(ManimColor(SEA_TOP), ManimColor(SEA_DEEP), u ** 0.8)


def surf_y(x, t):
    """The travelling sea surface (never stops)."""
    return SEA_Y + 0.034 * np.sin(1.9 * x - 0.9 * t) + 0.018 * np.sin(4.3 * x + 1.3 * t)


# time scrubber: LINEAR, 3.0 billion years ago at the left end, today at the right end
SCR_X0, SCR_X1, SCR_Y = -5.2, 2.9, -3.4     # "today" ends well left of the gauge column
SCR_UP = 0.22                              # how far the scrubber rises while it is the subject (s11)


def age_x(ga):
    """Screen x on the scrubber for an age in billions of years (computed, linear)."""
    return SCR_X1 - ga * (SCR_X1 - SCR_X0) / 3.0


SPAN_X = -4.7        # the GREEN span is solid from here to the playhead; left of here it breaks into fading dashes
PH_3GA, PH_S08, PH_GOE0, PH_GOE1, PH_LATER, PH_TODAY = age_x(3.0), -4.2, age_x(2.4), age_x(2.1), -0.2, age_x(0.0)

# gauge (screen coordinates)
G_X, G_Y0, G_Y1, G_W, G_TICK = 4.9, -1.6, 2.95, 0.6, 2.58       # the tube ends high enough for the tag to sit clear above the scrubber row
G_SLIVER, G_HAIR, G_LOW = 0.012, 0.03, 0.085


def gauge_h(level):
    return max(0.05, level * (G_TICK - G_Y0 - 0.06))


# ----------------------------------------------------------------------------- reusable builders
def band_stack(x0, x1, y_top, y_bot, c_top, c_bot, n=24, power=1.0):
    """A graded field: n flat bands, each running from its top edge to the bottom (no seams)."""
    g = VGroup()
    for i in range(n):
        yt = lerp(y_top, y_bot, i / n)
        col = interpolate_color(ManimColor(c_top), ManimColor(c_bot), (i / (n - 1)) ** power)
        g.add(Rectangle(width=x1 - x0, height=yt - y_bot, stroke_width=0, fill_color=col, fill_opacity=1)
              .move_to([(x0 + x1) / 2, (yt + y_bot) / 2, 0]))
    return g


def soft_glow(pos, r0, r1, color, n=6, peak=0.12):
    """A soft halo: stacked translucent discs from r1 (outer) in to r0."""
    return VGroup(*[Circle(radius=lerp(r1, r0, i / (n - 1)), stroke_width=0, fill_color=color,
                           fill_opacity=peak * (i + 1) / n).move_to(pos) for i in range(n)])


def poly(pts, color, opacity=1.0, stroke=0, stroke_color=None):
    m = VMobject(stroke_width=stroke, stroke_color=stroke_color or color, fill_color=color, fill_opacity=opacity)
    m.set_points_as_corners([P(*p) for p in pts] + [P(*pts[0])])
    return m


def pip(r=0.075, color=BLUE):
    """Oxygen in the air or water: a plain disc with a soft halo. Never two joined circles."""
    return VGroup(Dot(ORIGIN, radius=r * 2.4, color=color).set_opacity(0.16), Dot(ORIGIN, radius=r, color=color))


def iron_disc(r=0.085, dot=True, scale=1.0):
    """Dissolved iron: a GREY disc; the YELLOW dot on its rim is the electron it can give."""
    d = Circle(radius=r * scale, stroke_color="#C2C8D2", stroke_width=0.35 * scale, fill_color=GREY, fill_opacity=1)
    g = VGroup(d)
    if dot:
        g.add(Dot(d.get_center() + r * scale * RIGHT, radius=0.26 * r * scale, color=YELLOW))
    return g


SOCKET_ANG = [45, 135, 225, 315]


def hero_bubble(R=1.0, filled=0):
    """The oxygen token close up: a BLUE disc with four sockets for electrons (a token, not a molecule).
    Returns VGroup(glow, disc, sockets, dots); `filled` sockets already hold a YELLOW dot."""
    glow = soft_glow(ORIGIN, R, R * 1.5, BLUE, n=5, peak=0.10)
    disc = Circle(radius=R, stroke_color="#BFEAF5", stroke_width=4, fill_color=BLUE, fill_opacity=0.92)
    socks, dots = VGroup(), VGroup()
    for k, a in enumerate(SOCKET_ANG):
        c = 0.58 * R * np.array([math.cos(math.radians(a)), math.sin(math.radians(a)), 0])
        hole = Circle(radius=0.2 * R, stroke_width=0, fill_color="#0B2C3B", fill_opacity=0.95).move_to(c)
        ring = DashedVMobject(Circle(radius=0.2 * R, stroke_color=TEXT, stroke_width=3).move_to(c), num_dashes=9)
        socks.add(VGroup(hole, ring))
        if k < filled:
            dots.add(Dot(c, radius=0.15 * R, color=YELLOW))
    return VGroup(glow, disc, socks, dots)


def jag_bubble(R=1.0, n=14, depth=0.16):
    """The dangerous state: the same disc with a jagged rim."""
    pts = [R * (1 + (depth if i % 2 == 0 else -depth)) * np.array([math.cos(2 * math.pi * i / (2 * n)),
                                                                   math.sin(2 * math.pi * i / (2 * n)), 0])
           for i in range(2 * n)]
    m = VMobject(stroke_color="#BFEAF5", stroke_width=4, fill_color=BLUE, fill_opacity=0.92)
    m.set_points_as_corners(pts + [pts[0]])
    return m


def rust_flake(size=1.0, color=RED):
    """Rust: a small rough diamond."""
    pts = [(0, 0.62), (0.28, 0.2), (0.52, 0.02), (0.22, -0.3), (0.04, -0.6), (-0.3, -0.22), (-0.5, 0.05), (-0.2, 0.26)]
    body = poly([(x * size, y * size) for x, y in pts], color)
    facet = poly([(x * size, y * size) for x, y in [(0, 0.62), (0.28, 0.2), (0.02, 0.0), (-0.2, 0.26)]], "#FF9A8F", 0.55)
    return VGroup(body, facet)


def droplet(r=0.42, color=TEAL):
    """A water droplet (a teardrop) holding two electrons tight. Returns VGroup(body, shine, dots)."""
    pts = []
    for a in np.linspace(-math.pi * 0.83, math.pi * 0.83, 30):
        pts.append((r * math.sin(a), -r * math.cos(a)))
    pts.append((0, r * 1.75))
    body = VMobject(stroke_color="#A6EDF1", stroke_width=3, fill_color=color, fill_opacity=0.95)
    body.set_points_smoothly([P(*p) for p in pts[:-1]])
    body.add_line_to(P(*pts[-1])).add_line_to(P(*pts[0]))
    shine = Arc(radius=r * 0.62, start_angle=2.2, angle=0.9, stroke_color=WHITE, stroke_width=3).set_stroke(opacity=0.55)
    dots = VGroup(Dot(P(-0.19 * r / 0.42, -0.06), radius=0.14 * r / 0.42, color=YELLOW),
                  Dot(P(0.19 * r / 0.42, -0.06), radius=0.14 * r / 0.42, color=YELLOW))
    return VGroup(body, shine, dots)


def cyano_cell(L=6.0, H=2.6):
    """The cyanobacterium close up: a GREEN capsule with a mouth (upper left, with a lid) and a vent
    (upper right). Returns a VGroup with named parts as attributes: body, lid, hinge, mouth, vent_tip, food, inside."""
    body = RoundedRectangle(width=L, height=H, corner_radius=H / 2 - 0.02, stroke_color=GREEN, stroke_width=7,
                            fill_color="#2F5B2A", fill_opacity=0.96)
    inner = RoundedRectangle(width=L - 0.55, height=H - 0.55, corner_radius=(H - 0.55) / 2 - 0.02, stroke_width=0,
                             fill_color="#173018", fill_opacity=0.9)
    folds = VGroup(*[ArcBetweenPoints(P(x - 0.5, -H * 0.2), P(x + 0.5, -H * 0.2), angle=-0.9, stroke_color=GREEN,
                                      stroke_width=3).set_stroke(opacity=0.35) for x in (-1.9,)])
    mx, vx = -L * 0.27, L * 0.27
    gap = Rectangle(width=0.8, height=0.34, stroke_width=0, fill_color="#173018", fill_opacity=1).move_to(P(mx, H / 2))
    hinge = P(mx - 0.4, H / 2)
    lid = Line(hinge, hinge + RIGHT * 0.84, stroke_color="#B6E3A0", stroke_width=9)
    gap2 = Rectangle(width=0.5, height=0.34, stroke_width=0, fill_color="#173018", fill_opacity=1).move_to(P(vx, H / 2))
    vent = VGroup(Line(P(vx - 0.27, H / 2 - 0.05), P(vx - 0.27, H / 2 + 0.5), stroke_color=GREEN, stroke_width=7),
                  Line(P(vx + 0.27, H / 2 - 0.05), P(vx + 0.27, H / 2 + 0.5), stroke_color=GREEN, stroke_width=7))
    food = RoundedRectangle(width=1.0, height=0.62, corner_radius=0.12, stroke_color="#C9EDB5", stroke_width=3,
                            fill_color=GREEN, fill_opacity=1).move_to(P(L * 0.2, -H * 0.2))
    g = VGroup(body, inner, folds, gap, gap2, vent, lid, food)
    g.body, g.lid, g.hinge, g.food = body, lid, hinge, food
    g.mouth, g.vent_tip, g.inside = P(mx, H / 2), P(vx, H / 2 + 0.5), P(-L * 0.18, 0.05)
    return g


def microbe(kind=0, size=1.0, color=PURPLE):
    """An old microbe: a small PURPLE rod (kind 0) or sphere (kind 1)."""
    if kind == 0:
        return RoundedRectangle(width=0.21 * size, height=0.086 * size, corner_radius=0.042 * size, stroke_color="#D9CCFF",
                                stroke_width=0.6 * size, fill_color=color, fill_opacity=0.95)
    return Circle(radius=0.056 * size, stroke_color="#D9CCFF", stroke_width=0.6 * size, fill_color=color, fill_opacity=0.95)


def bracket(h, w=0.16, left=True, color=TEXT, sw=4):
    m = VMobject(stroke_color=color, stroke_width=sw)
    sx = 1 if left else -1
    m.set_points_as_corners([P(sx * w, h / 2), P(0, h / 2), P(0, -h / 2), P(sx * w, -h / 2)])
    return m


def bookmark(size=1.0):
    """The 'remember this' tick: a small white ribbon."""
    return poly([(x * size, y * size) for x, y in [(-0.07, 0.13), (0.07, 0.13), (0.07, -0.13), (0, -0.06), (-0.07, -0.13)]], TEXT)


def pick_icon(size=1.0):
    """A plain pick and a block (mining), in TEXT white."""
    handle = Line(P(-0.28, -0.3), P(0.2, 0.26), stroke_color=WHITE, stroke_width=9)
    head = ArcBetweenPoints(P(-0.12, 0.42), P(0.42, 0.0), angle=-1.1, stroke_color=WHITE, stroke_width=11)
    return VGroup(handle, head).scale(size, about_point=ORIGIN)


def gauge_parts():
    """The O2 gauge in screen coordinates: a tall glass tube with a dashed 'today' tick. Schematic."""
    panel = VGroup(*[Rectangle(width=3.3 + 0.12 * i, height=9.2, stroke_width=0, fill_color=BG, fill_opacity=o)
                     .move_to(P(4.3 + (3.3 + 0.12 * i) / 2 - 0.12 * i, 0)) for i, o in enumerate([0.8, 0.4, 0.25])])
    tube = RoundedRectangle(width=G_W, height=G_Y1 - G_Y0, corner_radius=0.1, stroke_color=TEXT, stroke_width=3,
                            fill_color="#080B12", fill_opacity=0.75).move_to(P(G_X, (G_Y0 + G_Y1) / 2))
    shine = Line(P(G_X - 0.19, G_Y0 + 0.25), P(G_X - 0.19, G_Y1 - 0.25), stroke_color=WHITE, stroke_width=3).set_stroke(opacity=0.22)
    tick = DashedLine(P(G_X - 0.4, G_TICK), P(G_X + 0.4, G_TICK), dash_length=0.09, stroke_color=TEXT, stroke_width=3)
    today = T("today", size=28).next_to(tick, RIGHT, buff=0.08)
    head = T("O₂ in air", size=28).move_to(P(5.36, 3.28))
    return dict(panel=panel, tube=tube, shine=shine, tick=tick, today=today, head=head)


def gauge_tag(long=False):
    if long:
        # three short lines: "levels uncertain" on one line at size 28 is 2.76 wide and the column inside the safe frame is 2.2.
        # The block ends 0.5 above the scrubber's "today", which itself now ends 0.85 to the left of it.
        g = VGroup(T("schematic;", size=28), T("levels", size=28), T("uncertain", size=28)).arrange(DOWN, buff=0.1)
        return g.move_to(P(5.36, -1.98 - g.height / 2 + g[0].height / 2))
    return T("schematic", size=28).move_to(P(5.36, -1.98))


def scrubber_parts():
    """The time scrubber in screen coordinates (linear scale; positions from age_x)."""
    strip = VGroup(*[Rectangle(width=11.6, height=1.3 + 0.1 * i, stroke_width=0, fill_color=BG, fill_opacity=o)
                     .move_to(P(-7.3 + 5.8, -4.08 + (1.3 + 0.1 * i) / 2)) for i, o in enumerate([0.55, 0.3, 0.2])])
    bar = Line(P(SCR_X0, SCR_Y), P(SCR_X1, SCR_Y), stroke_color="#B9BECA", stroke_width=5)
    ends = VGroup(Line(P(SCR_X0, SCR_Y - 0.13), P(SCR_X0, SCR_Y + 0.13), stroke_color="#B9BECA", stroke_width=4),
                  Line(P(SCR_X1, SCR_Y - 0.13), P(SCR_X1, SCR_Y + 0.13), stroke_color="#B9BECA", stroke_width=4))
    today = T("today", size=28).next_to(P(SCR_X1, SCR_Y), RIGHT, buff=0.3)
    return dict(strip=strip, bar=bar, ends=ends, today=today)


def playhead_shapes():
    def shape(hollow):
        tri = poly([(-0.14, 0.27), (0.14, 0.27), (0, 0.07)], TEXT, 0.0 if hollow else 1.0, stroke=3, stroke_color=TEXT)
        stem = Line(P(0, 0.09), P(0, -0.16), stroke_color=TEXT, stroke_width=4)
        knob = Circle(radius=0.09, stroke_color=TEXT, stroke_width=3, fill_color=BG if hollow else TEXT, fill_opacity=1)
        return VGroup(tri, stem, knob)
    return shape(False), shape(True)


# ----------------------------------------------------------------------------- the camera move
class Zoom(Animation):
    """Move the camera frame to (centre, width) as one zoom about a fixed point (width changes
    geometrically, so a deep push-in does not rush at the end)."""

    def __init__(self, frame, center, width, **kw):
        self.c1, self.w1 = np.array(center, dtype=float), float(width)
        super().__init__(frame, **kw)

    def begin(self):
        self.c0, self.w0 = self.mobject.get_center().copy(), float(self.mobject.width)
        super().begin()

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        w = self.w0 * (self.w1 / self.w0) ** a
        k = (w - self.w0) / (self.w1 - self.w0) if abs(self.w1 - self.w0) > 1e-9 else a
        f = self.mobject
        f.scale(w / f.width)
        f.move_to(self.c0 + (self.c1 - self.c0) * k)


# ----------------------------------------------------------------------------- the carried world
STAGE0 = dict(
    cam=FULL,
    pips=3.0,            # how many oxygen pips stand in the sky
    gauge=G_SLIVER, gauge2=0.0, tag="short",
    scrub=True, ph=PH_3GA, hollow=0.0, readout="about 3 billion years ago", band=0.0, bandlit=0.0, span=0.0,
    iron=0.0, edots=0.0, microbes=0.0, split=0.0, split2=0.0, methane=False, tick=False,
    mat=0.0, bubbles=False, bglow=0.0, flakes=0.0, stack=0.4, blocks=False,
    strays=0.0, nearfade=0.0, shade=0.0, mglow=0.0, dim=0.0, hole=0.0, sheldim=0.0, quiet=0.0,
    bfade=0.0,           # 1: bubbles fade out as they pass the shelf edge (the deep water is airless)
    scrdy=0.0,           # how far the scrubber is raised
)
TRACKED = ["pips", "gauge", "gauge2", "ph", "hollow", "band", "bandlit", "span", "iron", "edots", "microbes", "split",
           "split2", "mat", "bglow", "flakes", "stack", "strays", "nearfade", "shade", "mglow", "dim", "hole", "sheldim", "quiet", "bfade", "scrdy"]

# film times at which things begin (so ambient motion is the same on both sides of a cut)
T_METHANE = scene_t0("s03_life") + 9.5
T_BUBBLES = scene_t0("s05_puzzle") + 7.2
T_IRONMODE = scene_t0("s07_iron") + 16.5
T_FLAKES = scene_t0("s07_iron") + 15.5
T_LEAK = scene_t0("s09_takers") - 3.0
T_STAY = scene_t0("s12_goe") + 6.3
T_TODAY = scene_t0("s18_close") + 0.8
if not _IDS:
    T_METHANE = T_BUBBLES = T_IRONMODE = T_FLAKES = T_LEAK = T_STAY = T_TODAY = -1e9

N_PIPS, N_IRON, N_BUB, N_FLAKE, N_RING, N_PUFF, N_STRAY = 64, 40, 46, 28, 5, 7, 5
BUB_P, FLAKE_P, RING_P, PUFF_P, STRAY_P = 7.5, 13.0, 26.0, 9.0, 6.5
LEAKERS = (2, 9, 16, 27, 38)
TAKER_PTS = [P(-4.9, 3.25), P(2.75, 2.1), P(-4.75, 1.3)]     # plume, methane column, shore rock
RING_X = 2.9
HERO_IRON = P(1.55, -0.55)
MOTE_SITES = [HERO_IRON, P(-2.9, SHELF_Y + 0.15), P(-1.2, 0.0), P(-1.3, SHELF_Y + 0.15)]
BOOK_AT = P(1.55, BASIN_Y + 0.09)         # the bookmarked cluster of old microbes
BOOK_DY = 0.52                            # the tick sits this far above it
SHELF_CELLS = (-1.55, -1.25, -0.95)       # the old microbes on the shelf edge, beside the mat
MS = 1.4                                  # the old microbes are drawn this much larger than their design size


def static_world():
    """Everything that never moves: graded sky and sea, the shore with its cone, the sea floor, the mud."""
    g = VGroup()
    g.add(band_stack(XL, XR, YT, SEA_Y - 0.2, SKY_TOP, SKY_LOW, n=26, power=1.3))
    g.add(soft_glow(SUN, 0.38, 2.3, GOLD, n=16, peak=0.07))
    g.add(Circle(radius=0.36, stroke_width=0, fill_color="#F6DC8C", fill_opacity=1).move_to(SUN))
    g.add(band_stack(XL, XR, SEA_Y - 0.1, YB, SEA_TOP, SEA_DEEP, n=30, power=0.8))
    # a lighter, sunlit wedge of water over the shelf
    for i, o in enumerate([0.05, 0.05, 0.05]):
        g.add(poly([(SHORE_X, SEA_Y - 0.1), (0.6 - 0.5 * i, SEA_Y - 0.1), (SHELF_X1 - 0.3 * i, SHELF_Y), (SHELF_X0, SHELF_Y)], "#5FD0D6", o))
    # sea floor
    g.add(poly([(XL, YB), (XL, SEA_Y), (SHORE_X, SEA_Y), (SHELF_X0, SHELF_Y), (SHELF_X1, SHELF_Y), (BASIN_X0, BASIN_Y),
                (XR, BASIN_Y), (XR, YB)], ROCK))
    for d, c in [(0.32, "#2A2732"), (0.7, "#262430"), (1.12, "#2A2732"), (1.6, "#23212B")]:
        y = SHELF_Y - d
        xe = SHELF_X1 + (y - SHELF_Y) / (BASIN_Y - SHELF_Y) * (BASIN_X0 - SHELF_X1) - 0.1
        pts = [P(x, y + 0.035 * math.sin(1.7 * x + d * 9)) for x in np.linspace(XL, xe, 40)]
        g.add(VMobject(stroke_color=c, stroke_width=3).set_points_smoothly(pts))
    rng = random.Random(11)
    for _ in range(46):
        x = rng.uniform(-8.5, -0.9)
        y = rng.uniform(-3.0, -1.05)
        if y > floor_y(x) - 0.12:
            continue
        w = rng.uniform(0.08, 0.2)
        g.add(poly([(x - w, y), (x - w * 0.2, y + w * 0.5), (x + w, y + w * 0.15), (x + w * 0.5, y - w * 0.4)], "#35323E", 0.7))
    g.add(poly([(BASIN_X0 - 0.25, BASIN_Y), (XR, BASIN_Y), (XR, MUD_Y), (BASIN_X0 + 0.05, MUD_Y)], MUD))
    for _ in range(60):
        g.add(Dot(P(rng.uniform(BASIN_X0, 8.5), rng.uniform(MUD_Y + 0.04, BASIN_Y - 0.04)), radius=rng.uniform(0.012, 0.028),
                  color=rng.choice(["#3A2C40", "#1D1522"])))
    edge = VMobject(stroke_color=ROCK_HI, stroke_width=3)
    edge.set_points_as_corners([P(SHORE_X, SEA_Y), P(SHELF_X0, SHELF_Y), P(SHELF_X1, SHELF_Y), P(BASIN_X0, BASIN_Y), P(XR, BASIN_Y)])
    g.add(edge)
    # the shore and its volcanic cone (a dark silhouette with a thin sunlit rim)
    land = [(XL, SEA_Y - 0.02), (XL, 1.5), (-7.4, 1.48), (-6.75, 1.78), (-6.2, 2.56), (-5.95, 2.42), (-5.7, 2.56), (-5.2, 1.68),
            (-4.8, 1.2), (SHORE_X, SEA_Y - 0.02)]
    g.add(poly(land, LAND))
    rim = VMobject(stroke_color="#5A5136", stroke_width=3)
    rim.set_points_as_corners([P(*p) for p in land[5:]])
    g.add(rim)
    g.set_z_index(-100)
    return g


class World:
    """The carried world. Build it at the stage the last scene left it; change it through trackers
    (W.v[name]) and helpers. One clock updater drives every ambient motion from film time."""

    def __init__(self, scene, sid, **stage):
        self.sc = scene
        self.st = dict(STAGE0)
        self.st.update(stage)
        self.t0 = scene_t0(sid)
        self.t = self.t0
        self.s, self.c = 1.0, P(0, 0)
        self.v = {k: ValueTracker(float(self.st[k])) for k in TRACKED}
        self.hud, self.fns, self.pre = [], [], []
        self.ph_a = 1.0
        self.hole_at = P(0, 0)
        self.hole_r = 0.3
        self.gauge_shake = 0.0
        fr = getattr(scene.camera, "frame", None)
        if fr is not None:
            fr.set_z_index(-200)
            c, w = self.st["cam"]
            fr.scale(w / fr.width).move_to(c)
        self.static = static_world()
        scene.add(self.static)
        self.clock = Mobject()
        self.clock.set_z_index(-60)
        self.clock.add_updater(lambda m, dt: self.tick())
        scene.add(self.clock)
        self._build_ambient()
        self._build_hud()
        self.tick()

    # ---- helpers for scenes
    def val(self, k):
        return self.v[k].get_value()

    def to(self, k, value):
        """An animation that moves one world value."""
        return self.v[k].animate.set_value(value)

    def ramp(self, k, target, dur, delay=0.0):
        """Ease one world value to a target over `dur` seconds of film time, starting `delay` from now.
        It runs on the clock, so it carries across play() calls and camera moves."""
        t_start, st = self.t + delay, {}

        def fn(t):
            if t < t_start:
                return
            if "v0" not in st:
                st["v0"] = self.val(k)
            u = clip01((t - t_start) / dur) if dur > 0 else 1.0
            self.v[k].set_value(lerp(st["v0"], target, ease(u)))
            if u >= 1 and fn in self.pre:
                self.pre.remove(fn)
        self.pre.append(fn)

    def world_of(self, sx, sy):
        """Screen point -> world point under the camera as it is now."""
        return self.c + self.s * P(sx, sy)

    # ---- ambient systems
    def _build_ambient(self):
        sc, st = self.sc, self.st
        rng = random.Random(7)
        # sun rays (GOLD): three slow shafts reaching into the shelf water
        self.rays = VGroup(*[VMobject(stroke_width=0, fill_color=GOLD, fill_opacity=0.08) for _ in range(3)]).set_z_index(1)
        # soft bands of light under the surface (slow, never still)
        self.caus = VGroup(*[VMobject(stroke_color="#8FE8EA", stroke_width=[9, 12, 14, 16][k]).set_stroke(opacity=0.06) for k in range(4)]).set_z_index(1.2)
        self.cx = [np.linspace(SHORE_X + 0.08 + 0.05 * k, XR, 70) for k in range(4)]
        # the banded stack on the basin floor
        self.stripes = VGroup(*[Rectangle(width=XR - BASIN_X0 - 0.05, height=0.01, stroke_width=0,
                                          fill_color=(RED if j % 2 == 0 else SILICA), fill_opacity=1.0 if j % 2 == 0 else 0.8)
                                for j in range(8)]).set_z_index(6.5)      # above the dark band of s17: the record stays readable
        self._stack_last = None
        # rust flakes
        self.flakes = VGroup(*[rust_flake(0.085 + 0.03 * hsh(k, 5)) for k in range(N_FLAKE)]).set_z_index(3)
        for k, m in enumerate(self.flakes):
            m._p, m._a, m._ang = m.get_center(), 1.0, 0.0
            m._x = lerp(-1.2, 7.6, hsh(k, 1) ** 0.8) if k % 5 else lerp(-3.6, -1.0, hsh(k, 2))
            m._y0 = lerp(-0.45, 0.55, hsh(k, 3))
        # dissolved iron
        self.iron = VGroup().set_z_index(4)
        homes = [HERO_IRON]
        tries = 0
        while len(homes) < N_IRON and tries < 4000:
            tries += 1
            x = rng.uniform(-4.0, 7.6)
            if rng.random() < 0.35 and x > -0.6:
                continue
            fy = floor_y(x)
            y = rng.uniform(fy + 0.3, SEA_Y - 0.28) if x < -0.3 else rng.uniform(fy + 0.25, SEA_Y - 0.25) ** 1.0
            if x > 0 and rng.random() < 0.45:
                y = rng.uniform(fy + 0.25, -0.6)
            p = P(x, y)
            if all(np.linalg.norm(p - h) > 0.42 for h in homes):
                homes.append(p)
        self.iron_spec = []
        for i, h in enumerate(homes):
            g = iron_disc()
            g.move_to(h)
            g[0]._p, g[1]._p, g[0]._a, g[1]._a = g[0].get_center(), g[1].get_center(), 1.0, 1.0
            amp = (0.012, 0.01) if i == 0 else (rng.uniform(0.22, 0.5), rng.uniform(0.1, 0.24))
            self.iron_spec.append((h, amp, rng.uniform(0.1, 0.24), rng.uniform(0.09, 0.2), rng.uniform(0, 6.28), rng.uniform(0, 6.28),
                                   rng.uniform(0.25, 0.6) * rng.choice([-1, 1]), rng.uniform(0, 6.28)))
            self.iron.add(g)
        self.motes = VGroup().set_z_index(1.5)
        self.mote_spec = []
        for site in MOTE_SITES:
            for k in range(26):
                r = rng.choice([0.004, 0.006, 0.009, 0.014])
                h = site + P(rng.uniform(-0.6, 0.6), rng.uniform(-0.12, 0.45))
                m = Dot(h, radius=r, color="#BDEFF2").set_opacity(0)
                m._p, m._a = m.get_center(), 0.0
                self.motes.add(m)
                self.mote_spec.append((h, rng.uniform(0.03, 0.09), rng.uniform(0.02, 0.06), rng.uniform(0.15, 0.4), rng.uniform(0, 6.28),
                                       0.55 if r < 0.008 else (0.3 if r < 0.012 else 0.16)))
        # methane rings (GREY ring, one electron on the rim)
        self.rings = VGroup(*[VGroup(Circle(radius=0.075, stroke_color="#B4BAC6", stroke_width=2.2), Dot(ORIGIN, radius=0.024, color=YELLOW))
                              for _ in range(N_RING)]).set_z_index(5)
        for g in self.rings:
            g._p, g._a = g.get_center(), 1.0
        # the dark band (s17 on): a soft-edged shade over mud and deep basin
        self.shade = VGroup(*[poly([(SHELF_X1 + 0.02, -0.4 - 0.13 * i), (XR, -0.4 - 0.13 * i), (XR, MUD_Y), (BASIN_X0 + 0.05, MUD_Y),
                                    (BASIN_X0 - 0.2, BASIN_Y), (SHELF_X1 + 0.02, SHELF_Y)], "#02040A", 1.0) for i in range(6)]).set_z_index(6)
        self.shade._a = -1
        # old microbes (PURPLE): shelf edge, slope, basin floor, mud, deep water; then two sets of daughters
        spots = []
        for x in SHELF_CELLS:
            spots.append((x, SHELF_Y + 0.085, "shelf"))
        for x in (-0.72, -0.55, -0.38):
            spots.append((x, floor_y(x) + 0.12, "slope"))
        for x in np.linspace(0.35, 7.9, 22):
            spots.append((x + rng.uniform(-0.1, 0.1), BASIN_Y + 0.09, "floor"))
        for x in np.linspace(0.45, 7.8, 17):
            spots.append((x + rng.uniform(-0.12, 0.12), rng.uniform(MUD_Y + 0.09, BASIN_Y - 0.1), "mud"))
        for k in range(9):
            spots.append((0.7 + 0.85 * k + rng.uniform(-0.2, 0.2), rng.uniform(-1.12, -0.5), "deep"))
        # the bookmarked cluster: three cells tight together on the floor
        for dx, dy in [(-0.2, 0.0), (0.14, 0.02), (0.0, 0.17)]:
            spots.append((BOOK_AT[0] + dx, BOOK_AT[1] + dy, "floor"))
        self.mic = VGroup().set_z_index(8)
        self.mic_spec = []
        self.mglow = VGroup().set_z_index(7)
        for i, (x, y, where) in enumerate(spots):
            m = microbe(i % 3 == 1, MS * (1.0 if where != "deep" else 0.9))
            m.move_to(P(x, y))
            m._p, m._a, m._ang, m._sc = m.get_center(), 1.0, 0.0, 1.0
            self.mic.add(m)
            self.mic_spec.append(dict(home=P(x, y), where=where, ph=rng.uniform(0, 6.28), w=rng.uniform(0.9, 1.7), mom=None, gen=0))
        base_n = len(spots)
        # daughters: gen 1 split on the shelf in s03 ("fermenting"), gen 2 in mud and deep water in s16
        for i in range(base_n):
            wh = self.mic_spec[i]["where"]
            gen = 1 if wh == "shelf" else (2 if (wh in ("mud", "deep", "floor") and i % 3 == 0) else 0)
            if gen:
                h = self.mic_spec[i]["home"]
                off = P(0.15, 0.15) if wh == "shelf" else P(0.2 if wh != "deep" else 0.22, 0.13 if wh == "floor" else (0.0 if wh == "mud" else 0.16))
                m = microbe(i % 3 == 1, MS * (1.0 if wh != "deep" else 0.9))
                m.move_to(h)
                m._p, m._a, m._ang, m._sc = m.get_center(), 1.0, 0.0, 1.0
                self.mic.add(m)
                self.mic_spec.append(dict(home=h + off, where=wh, ph=rng.uniform(0, 6.28), w=rng.uniform(0.9, 1.7), mom=h, gen=gen))
        for i, sp in enumerate(self.mic_spec):
            if sp["where"] in ("mud", "deep", "floor"):
                at = sp["home"] + (P(0, STRIPE_H * float(st["stack"]) - 0.02) if sp["where"] == "floor" else P(0, 0))
                gl = Dot(at, radius=0.23, color=PURPLE).set_opacity(0.0)
                gl._a, gl._i = 0.0, i
                self.mglow.add(gl)
        # a z_index set on an empty group does not reach members added later: set it on the cells and their glows
        # themselves, so they are drawn above the dark band of s16-s18 and glow inside it
        for m in self.mic:
            m.set_z_index(8)
        for gl in self.mglow:
            gl.set_z_index(6.2)               # above the dark band, under the striped stack
        # the dim layer ("everything else dims") sits under the mat and its bubbles
        self.dim = Rectangle(width=XR - XL, height=YT - YB, stroke_width=0, fill_color="#02030A", fill_opacity=0).set_z_index(9)
        self.dim._a = 0.0
        # the mat: a row of GREEN lumps that breathe
        self.mat = VGroup().set_z_index(10)
        xs = np.linspace(MAT_X0 + 0.14, MAT_X1 - 0.14, 21)
        for j, x in enumerate(xs):
            e = Ellipse(width=0.4, height=0.4 + 0.1 * hsh(j, 9), stroke_width=0, fill_color=[GREEN, "#6FAE58", "#93D174"][j % 3], fill_opacity=1)
            e.move_to(P(x, SHELF_Y + 0.19))
            e._x, e._f, e._a, e._p = x, 1.0, 1.0, e.get_center()
            self.mat.add(e)
        self.matglow = VGroup(*[Ellipse(width=(MAT_X1 - MAT_X0) * (1.05 + 0.1 * i), height=0.85 + 0.4 * i, stroke_width=0, fill_color=GREEN,
                                        fill_opacity=0.05).move_to(P((MAT_X0 + MAT_X1) / 2, SHELF_Y + 0.22)) for i in range(3)]).set_z_index(9.5)
        self.matglow._a = -1
        # oxygen bubbles from the mat, and strays that wander toward the old microbes
        self.bub = VGroup(*[Dot(ORIGIN, radius=0.07, color=BLUE) for _ in range(N_BUB)]).set_z_index(11)
        self.bubglow = VGroup(*[Dot(ORIGIN, radius=0.15, color=BLUE).set_opacity(0) for _ in range(N_BUB)]).set_z_index(10.5)
        for m in list(self.bub) + list(self.bubglow):
            m._p, m._a, m._sc = m.get_center(), 1.0, 1.0
        self.stray = VGroup(*[Dot(ORIGIN, radius=0.07, color=BLUE) for _ in range(N_STRAY)]).set_z_index(11)
        for m in self.stray:
            m._p, m._a = m.get_center(), 1.0
        self.stray_pos = [None] * N_STRAY
        # volcanic puffs (GREY) and the oxygen pips in the air
        self.puffs = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color="#9AA1AE", fill_opacity=0.5) for _ in range(N_PUFF)]).set_z_index(12)
        for m in self.puffs:
            m._p, m._a, m._r = m.get_center(), 0.5, 0.1
        self.pips = VGroup().set_z_index(13)
        homes = [P(0.6, 2.3), P(-1.6, 3.0), P(2.7, 1.75), P(-2.6, 1.85), P(1.5, 2.72), P(3.5, 2.6)]
        tries = 0
        while len(homes) < N_PIPS and tries < 6000:
            tries += 1
            p = P(rng.uniform(-6.9, 4.05), rng.uniform(1.3, 3.85))
            if p[0] < -4.5 and p[1] < 3.0:
                continue
            if np.linalg.norm(p - SUN) < 0.75:
                continue
            if all(np.linalg.norm(p - h) > 0.52 for h in homes):
                homes.append(p)
        self.pip_spec = []
        for i, h in enumerate(homes):
            g = pip()
            g.move_to(h)
            g._p, g._a = g.get_center(), 1.0
            self.pips.add(g)
            self.pip_spec.append((h, rng.uniform(0.2, 0.42), rng.uniform(0.1, 0.2), rng.uniform(0.14, 0.3), rng.uniform(0.11, 0.24),
                                  rng.uniform(0, 6.28), rng.uniform(0, 6.28)))
        # the travelling sea surface
        self.sx = np.linspace(SHORE_X - 0.02, XR, 120)
        self.skin = VMobject(stroke_width=0, fill_color=SEA_TOP, fill_opacity=1).set_z_index(14)
        self.surf = VMobject(stroke_color="#A9E7EA", stroke_width=3).set_z_index(14.2)
        self.glints = VGroup(*[Line(ORIGIN, RIGHT * 0.22, stroke_color=WHITE, stroke_width=3) for _ in range(9)]).set_z_index(14.4)
        for m in self.glints:
            m._p, m._a = m.get_center(), 1.0
        # land rock that can take oxygen (s09 on) and the bookmark tick (s03 on)
        self.blocks = VGroup()
        if st["blocks"]:
            self.blocks = self.shore_blocks()
        self.book = None
        if st["tick"]:
            self.book = bookmark(1.0).move_to(BOOK_AT + UP * BOOK_DY).set_z_index(15)
            self.book._p, self.book._a = self.book.get_center(), 1.0
        # add in layer order (z_index sorts them; only what this stage needs goes in)
        sc.add(self.caus, self.rays, self.stripes)
        if st["flakes"] is not False:
            sc.add(self.flakes)
        sc.add(self.motes, self.iron, self.rings, self.shade, self.mglow, self.mic, self.dim, self.matglow, self.mat, self.bubglow, self.bub, self.stray,
               self.puffs, self.pips, self.skin, self.surf, self.glints)
        if st["blocks"]:
            sc.add(self.blocks)
        if self.book is not None:
            sc.add(self.book)

    def shore_blocks(self):
        """Land rock (GREY blocks, one electron each) along the shore."""
        g = VGroup()
        for k, (x, y) in enumerate([(-5.33, 1.92), (-5.08, 1.62), (-4.86, 1.36), (-4.66, 1.14)]):
            b = RoundedRectangle(width=0.3, height=0.24, corner_radius=0.04, stroke_color="#C2C8D2", stroke_width=1.5,
                                 fill_color=GREY, fill_opacity=1).move_to(P(x, y)).rotate(-0.75)
            d = Dot(P(x + 0.13, y + 0.12), radius=0.045, color=YELLOW)
            g.add(VGroup(b, d))
        return g.set_z_index(15)

    # ---- HUD
    def _build_hud(self):
        sc, st = self.sc, self.st
        gp = gauge_parts()
        self.g = gp
        self.g_fill = Rectangle(width=G_W - 0.12, height=0.1, stroke_width=0, fill_color=BLUE, fill_opacity=1).set_z_index(32)
        self.g_fill2 = Rectangle(width=G_W - 0.12, height=0.1, stroke_width=0, fill_color=BLUE, fill_opacity=0).set_z_index(32.1)
        self.g_glow = Rectangle(width=G_W + 0.3, height=0.1, stroke_width=0, fill_color=BLUE, fill_opacity=0.16).set_z_index(30.5)
        self.g_cap = Line(LEFT, RIGHT, stroke_color="#D8F4FB", stroke_width=3).set_z_index(32.2)
        self.g_fill2._a = 0.0
        gp["panel"].set_z_index(30)
        gp["tube"].set_z_index(31)
        gp["shine"].set_z_index(32.5)
        for k in ("tick", "today", "head"):
            gp[k].set_z_index(33)
        self.tag = gauge_tag(st["tag"] == "long").set_z_index(33) if st["tag"] else None
        hud = [gp["panel"], gp["tube"], gp["shine"], gp["tick"], gp["today"], gp["head"]] + ([self.tag] if self.tag is not None else [])
        sc.add(gp["panel"], self.g_glow, gp["tube"], self.g_fill, self.g_fill2, self.g_cap, *hud[2:])
        for m in hud:
            self.pin(m, placed=False)
        self._hz_panel = -1.0
        self.scr = None
        if st["scrub"]:
            self.add_scrubber(animate=False)

    def add_scrubber(self, animate=False):
        """Build the time scrubber (call with the camera at rest). Returns the parts to fade in."""
        sc, st = self.sc, self.st
        sp = scrubber_parts()
        self.scr = sp
        sp["strip"].set_z_index(30)
        sp["bar"].set_z_index(31)
        sp["ends"].set_z_index(31)
        sp["today"].set_z_index(33)
        self.band_out = Rectangle(width=PH_GOE1 - PH_GOE0, height=0.3, stroke_color=BLUE, stroke_width=3, fill_color=BG, fill_opacity=0.6
                                  ).move_to(P((PH_GOE0 + PH_GOE1) / 2, SCR_Y)).set_z_index(31.5)
        self.band_fill = Rectangle(width=PH_GOE1 - PH_GOE0, height=0.3, stroke_width=0, fill_color=BLUE, fill_opacity=1
                                   ).move_to(P((PH_GOE0 + PH_GOE1) / 2, SCR_Y)).set_z_index(31.6)
        self.band_out._a, self.band_fill._a = -1, -1
        self.ph_solid, self.ph_hollow = playhead_shapes()
        self.ph_solid.set_z_index(34)
        self.ph_hollow.set_z_index(34)
        self.span_solid = Line(LEFT, RIGHT, stroke_color=GREEN, stroke_width=6).set_z_index(31.8)
        self.span_dash = VGroup(*[Line(LEFT, RIGHT, stroke_color=GREEN, stroke_width=6) for _ in range(4)]).set_z_index(31.8)
        self.readout = None
        parts = [sp["strip"], sp["bar"], sp["ends"], sp["today"], self.band_out, self.band_fill]
        for m in parts[1:]:
            m.shift(UP * float(st["scrdy"]))
        for r in sp["strip"]:
            r.stretch((r.height + float(st["scrdy"])) / r.height, 1, about_edge=DOWN)
        for m in parts:
            self.pin(m, placed=False)
        self._hz_strip = -1.0
        for m in list(self.ph_solid.get_family()) + list(self.ph_hollow.get_family()) + [self.span_solid] + list(self.span_dash):
            m._bsw = float(m.get_stroke_width())
            m._bfo = float(m.get_fill_opacity())
        dyn = [self.span_dash, self.span_solid, self.ph_solid, self.ph_hollow]
        sc.add(*parts, *dyn)
        if st["readout"]:
            self.readout = self.readout_text(st["readout"])
            sc.add(self.readout)
        self.tick()
        return parts + dyn + ([self.readout] if self.readout is not None else [])

    def readout_text(self, text, color=TEXT):
        m = T(text, size=28, color=color)
        m.move_to(P(2.45 - m.width / 2, -2.98 + self.val("scrdy"))).set_z_index(33)
        return self.pin(m, placed=False)

    def scr_shift(self, dy):
        """Animations that raise (dy > 0) or lower the whole scrubber by dy, its dark strip growing with it, so the readout
        never leaves the strip. Camera at rest."""
        an = [m.animate.shift(UP * dy) for m in self.scr_static()]
        an += [r.animate.stretch((r.height + dy) / r.height, 1, about_edge=DOWN) for r in self.scr["strip"]]
        return an + [self.to("scrdy", self.val("scrdy") + dy)]

    def scr_static(self):
        """The scrubber's fixed parts (to raise or lower it by hand with the camera at rest)."""
        return [self.scr["bar"], self.scr["ends"], self.scr["today"], self.band_out, self.band_fill] + ([self.readout] if self.readout is not None else [])

    def set_readout(self, text, rt=0.4):
        """Swap the scrubber's readout (camera must be at rest)."""
        new = self.readout_text(text)
        old, self.readout = self.readout, new
        anims = [FadeIn(new, shift=UP * 0.12 * self.s)]
        if old is not None:
            self.unpin(old)
            anims.append(FadeOut(old, shift=UP * 0.12 * self.s))
        self.sc.play(*anims, run_time=rt)

    def pin(self, m, placed=True):
        """Keep a mobject fixed on screen while the camera moves. placed=False: m is in screen
        coordinates and is mapped to where the camera is now."""
        for fm in m.get_family():
            fm._bsw = float(fm.get_stroke_width()) / (self.s if placed else 1.0)
        if placed:
            m._s, m._c = self.s, self.c.copy()
        else:
            m._s, m._c = 1.0, P(0, 0)
        if m not in self.hud:
            self.hud.append(m)
        self._pin_one(m)
        return m

    def unpin(self, m):
        if m in self.hud:
            self.hud.remove(m)

    def _pin_one(self, m):
        s, c = self.s, self.c
        if abs(s - m._s) > 1e-9 or abs(c[0] - m._c[0]) > 1e-9 or abs(c[1] - m._c[1]) > 1e-9:
            m.scale(s / m._s, about_point=m._c)
            m.shift(c - m._c)
            for fm in m.get_family():
                b = getattr(fm, "_bsw", 0.0)
                if b:
                    fm.stroke_width = b * s
            m._s, m._c = s, c.copy()

    # ---- the clock
    def tick(self):
        sc = self.sc
        self.t = t = self.t0 + sc.renderer.time + getattr(sc, "last_t", 0.0)
        fr = getattr(sc.camera, "frame", None)
        if fr is not None:
            self.s, self.c = fr.width / FW, fr.get_center()
        for fn in list(self.pre):
            fn(t)
        self._t_surface(t)
        self._t_sky(t)
        self._t_water(t)
        self._t_life(t)
        self._t_layers(t)
        for m in self.hud:
            self._pin_one(m)
        self._t_hud(t)
        for fn in list(self.fns):
            fn(t)

    @staticmethod
    def _place(m, p):
        d = p - m._p
        if abs(d[0]) > 1e-7 or abs(d[1]) > 1e-7:
            m.shift(d)
            m._p = p

    @staticmethod
    def _alpha(m, a, base=1.0):
        if abs(a - m._a) > 0.004:
            m.set_fill(opacity=a * base)
            if m.get_stroke_width() > 0:
                m.set_stroke(opacity=a)
            m._a = a

    def _excl(self, p, pad=0.0):
        h = self.val("hole")
        if h > 0.001:
            d = p - self.hole_at
            n = math.hypot(d[0], d[1])
            R = self.hole_r + pad
            if n < R:
                if n < 1e-6:
                    d, n = P(1, 0), 1.0
                p = self.hole_at + d / n * (n + (R - n) * h)
        return p

    def _t_surface(self, t):
        ys = surf_y(self.sx, t)
        pts = np.column_stack([self.sx, ys, np.zeros_like(ys)])
        self.surf.set_points_as_corners(pts)
        self.skin.set_points_as_corners(np.vstack([pts, [[XR, SEA_Y - 0.14, 0], [self.sx[0], SEA_Y - 0.14, 0], pts[0]]]))
        for k, m in enumerate(self.caus):
            x = self.cx[k]
            d = (0.2, 0.42, 0.68, 1.0)[k]
            y = SEA_Y - d + 0.05 * np.sin(1.3 * x + 0.5 * t + 1.9 * k) + 0.03 * np.sin(3.1 * x - 0.7 * t + k)
            m.set_points_as_corners(np.column_stack([x, y, np.zeros_like(x)]))
            m.set_stroke(opacity=(0.085 - 0.014 * k) * (1 + 0.3 * math.sin(0.6 * t + 2.2 * k)))
        span = XR - SHORE_X - 0.6
        for i, m in enumerate(self.glints):
            x = SHORE_X + 0.3 + ((i * 1.93 + 0.22 * t * (1 + 0.15 * (i % 3))) % span)
            self._place(m, P(x, float(surf_y(x, t)) + 0.012))
            a = 0.25 + 0.35 * (0.5 + 0.5 * math.sin(1.7 * t + i * 2.1))
            if abs(a - m._a) > 0.02:
                m.set_stroke(opacity=a)
                m._a = a
        for i, m in enumerate(self.rays):
            tx = (-3.5, -2.55, -1.6)[i] + 0.3 * math.sin(0.23 * t + 2.1 * i)
            a = 0.075 + 0.04 * math.sin(0.41 * t + 1.7 * i)
            o = SUN + P(0.1 * (i - 1), -0.3)
            m.set_points_as_corners([o + P(-0.05, 0), o + P(0.05, 0), P(tx + 0.34, SHELF_Y), P(tx - 0.34, SHELF_Y), o + P(-0.05, 0)])
            m.set_fill(opacity=a)

    def _t_sky(self, t):
        for i, m in enumerate(self.puffs):
            u = (t / PUFF_P + i / N_PUFF) % 1.0
            p = CRATER + P(1.9 * u + 0.13 * math.sin(6.28 * (1.4 * u + 0.37 * i)), 0.05 + 1.5 * u)
            self._place(m, p)
            r = 0.09 + 0.36 * u
            m.scale(r / m._r)
            m._r = r
            a = 0.55 * (1 - u) ** 1.2 * min(1.0, u / 0.07)
            if abs(a - m._a) > 0.004:
                m.set_fill(opacity=a)
                m._a = a
        n = self.val("pips")
        for i, m in enumerate(self.pips):
            a = clip01(n - i)
            if a != m._a:
                m[0].set_fill(opacity=0.16 * a)
                m[1].set_fill(opacity=a)
                m._a = a
            if a > 0:
                h, ax, ay, wx, wy, px, py = self.pip_spec[i]
                self._place(m, h + P(ax * math.sin(wx * t + px), ay * math.sin(wy * t + py)))

    def pip_pos(self, i, t=None):
        t = self.t if t is None else t
        h, ax, ay, wx, wy, px, py = self.pip_spec[i]
        return h + P(ax * math.sin(wx * t + px), ay * math.sin(wy * t + py))

    def iron_pos(self, i, t=None):
        t = self.t if t is None else t
        h, amp, wx, wy, px, py, wd, pd = self.iron_spec[i]
        return h + P(amp[0] * math.sin(wx * t + px), amp[1] * math.sin(wy * t + py))

    def _t_water(self, t):
        # dissolved iron
        qt = 1 - 0.6 * self.val("quiet")
        ai, ae = self.val("iron") * qt, self.val("edots")
        # fine drifting motes: too small to see in the wide view, they give the close-ups depth
        am = clip01((0.3 - self.s) / 0.15)
        if am > 0 or self.motes[0]._a > 0:
            for k, m in enumerate(self.motes):
                h, ax, ay, w, ph, base = self.mote_spec[k]
                self._place(m, h + P(ax * math.sin(w * t + ph) + 0.02 * math.sin(0.11 * t + k), ay * math.cos(0.8 * w * t + 2 * ph)))
                a = am * base
                if abs(a - m._a) > 0.004:
                    m.set_fill(opacity=a)
                    m._a = a
        if ai > 0 or self.iron[0][0]._a > 0:
            for i, g in enumerate(self.iron):
                h, amp, wx, wy, px, py, wd, pd = self.iron_spec[i]
                p = h + P(amp[0] * math.sin(wx * t + px), amp[1] * math.sin(wy * t + py))
                if i:
                    p = self._excl(p, 0.1)
                self._place(g[0], p)
                ang = wd * t + pd
                self._place(g[1], p + 0.085 * P(math.cos(ang), math.sin(ang)))
                self._alpha(g[0], ai)
                self._alpha(g[1], ai * ae)
        # methane rings
        on = self.st["methane"]
        for i, g in enumerate(self.rings):
            q = (t - T_METHANE) / RING_P - i / N_RING
            if not on or q < 0:
                a = 0.0
            else:
                u = q % 1.0
                y = lerp(BASIN_Y + 0.2, 3.7, u)
                self._place(g, P(RING_X + 0.16 * math.sin(2.3 * u * 6.28 + i), y))
                a = min(1.0, u / 0.03) * clip01((1 - u) / 0.12)
            if abs(a - g._a) > 0.004:
                g[0].set_stroke(opacity=a)
                g[1].set_fill(opacity=a)
                g._a = a
        # rust flakes
        af = self.val("flakes") * qt
        top = BASIN_Y + STRIPE_H * self.val("stack")
        for k, m in enumerate(self.flakes):
            q = (t - T_FLAKES) / FLAKE_P - hsh(k, 7)
            a = 0.0
            if af > 0 and q >= 0 and (T_FLAKES + (math.floor(q) + hsh(k, 7)) * FLAKE_P) < T_TODAY:
                u = q % 1.0
                x = m._x
                yb = (top if x > BASIN_X0 else floor_y(x)) + 0.04
                y = lerp(m._y0, yb, min(1.0, u / 0.9) ** 1.1)
                p = self._excl(P(x + 0.1 * math.sin(5 * u * 6.28 + k), y), 0.15)
                self._place(m, p)
                a = af * min(1.0, u / 0.05) * clip01((1 - u) / 0.08)
            if abs(a - m._a) > 0.004:
                m[0].set_fill(opacity=a)
                m[1].set_fill(opacity=0.55 * a)
                m._a = a
        # oxygen bubbles from the mat
        on, gl, bf = self.st["bubbles"], self.val("bglow"), self.val("bfade")
        for j, m in enumerate(self.bub):
            a, sc_, p = 0.0, 1.0, None
            ph = (j * 0.618) % 1.0
            q = (t - T_BUBBLES) / BUB_P - ph
            if on and q >= 0:
                n = math.floor(q)
                u = q - n
                ts = T_BUBBLES + (n + ph) * BUB_P
                h1, h2, h3 = hsh(j, n, 1), hsh(j, n, 2), hsh(j, n, 3)
                sx = lerp(MAT_X0 + 0.15, MAT_X1 - 0.15, hsh(j, 4))
                start = P(sx, SHELF_Y + 0.42)
                wob = 0.05 * math.sin(9 * u * 6.28 + j)
                leak = j in LEAKERS
                if ts >= T_TODAY or (leak and ts >= T_LEAK):
                    top_pt = P(sx + 0.3 + 0.9 * h1, SEA_Y)
                    if u < 0.42:
                        p = lerp(start, top_pt, ease(u / 0.42)) + P(wob, 0)
                        a = min(1.0, u / 0.05)
                    elif ts >= T_STAY:
                        end = top_pt + P(lerp(-1.5, 1.5, h2), lerp(0.7, 2.3, h3))
                        p = lerp(top_pt, end, ease((u - 0.42) / 0.5))
                        a = clip01((0.95 - u) / 0.2)
                    else:
                        end = TAKER_PTS[(j + n) % 3]
                        p = lerp(top_pt, end, ease((u - 0.42) / 0.45))
                        a = clip01((0.93 - u) / 0.05)
                        if u > 0.87:
                            sc_ = 1 + 16 * (u - 0.87)
                elif ts >= T_IRONMODE:
                    end = P(sx + 0.3 + 3.0 * h1 ** 1.3, lerp(-0.4, 0.6, h2))
                    if u < 0.62:
                        p = lerp(start, end, ease(u / 0.62)) + P(wob, 0)
                        a = min(1.0, u / 0.05)
                    elif u < 0.72:
                        p = end
                        sc_ = 1 + 22 * (u - 0.62)
                        a = clip01((0.72 - u) / 0.1)
                else:
                    end = P(sx + 0.3 + 1.6 * h1, lerp(-0.3, 0.7, h2))
                    p = lerp(start, end, ease(u / 0.7)) + P(wob, 0)
                    uf = 0.38 + 0.3 * h3
                    a = min(1.0, u / 0.05) * clip01((uf - u) / 0.12)
            if p is not None and a > 0:
                if bf > 0 and p[1] < SEA_Y - 0.03:
                    a *= 1 - bf * clip01((p[0] - (SHELF_X1 - 0.2)) / 0.5)
                p = self._excl(p, 0.25)
                self._place(m, p)
                self._place(self.bubglow[j], p)
            if abs(sc_ - m._sc) > 0.01:
                m.scale(sc_ / m._sc)
                m._sc = sc_
            self._alpha(m, a)
            self._alpha(self.bubglow[j], a * gl * 0.35)
        # strays that wander along the shelf toward the old microbes
        astr = self.val("strays")
        for j, m in enumerate(self.stray):
            a = 0.0
            self.stray_pos[j] = None
            if astr > 0:
                u = (t / STRAY_P + j / N_STRAY) % 1.0
                p = P(lerp(MAT_X1 - 0.05, -1.0 + 0.5 * hsh(j, 3), ease(u)), SHELF_Y + 0.22 + 0.1 * math.sin(6.28 * u * 2 + j) + 0.25 * u * hsh(j, 8))
                self._place(m, p)
                a = astr * min(1.0, u / 0.08) * clip01((1 - u) / 0.15)
                if a > 0.2:
                    self.stray_pos[j] = p
            self._alpha(m, a)

    def _t_life(self, t):
        am = self.val("microbes")
        s1, s2, nf, sd = self.val("split"), self.val("split2"), self.val("nearfade"), self.val("sheldim")
        lift = STRIPE_H * self.val("stack") - 0.02
        if self.book is not None:
            self._place(self.book, BOOK_AT + P(0, BOOK_DY + lift))
            a = clip01((self.s - 0.42) / 0.12)          # in a close-up elsewhere it would be a huge grey shape: hide it
            if abs(a - self.book._a) > 0.004:
                self.book.set_fill(opacity=a)
                self.book._a = a
        if am <= 0 and self.mic[0]._a <= 0:
            return
        for i, m in enumerate(self.mic):
            sp = self.mic_spec[i]
            a = am
            home = sp["home"]
            if sp["gen"]:
                g = s1 if sp["gen"] == 1 else s2
                if g <= 0:
                    self._alpha(m, 0.0)
                    continue
                home = lerp(sp["mom"], home, ease(g))
            if sp["where"] == "floor":
                home = home + P(0, lift)
            p = home + P(0.012 * math.sin(sp["w"] * t + sp["ph"]), 0.012 * math.sin(1.31 * sp["w"] * t + 2 * sp["ph"]))
            sc_ = 1.0
            if sp["where"] == "shelf":
                # flinch from any stray bubble that comes close; the nearest to the mat may dim (nearfade)
                f, side = 0.0, 1.0
                for q in self.stray_pos:
                    if q is not None:
                        fq = clip01(1 - math.hypot(q[0] - home[0], (q[1] - home[1]) * 0.6) / 0.5)
                        if fq > f:
                            f, side = fq, (1.0 if home[0] >= q[0] else -1.0)
                if f > 0:
                    f = ease(f)
                    p = p + P(0.17 * f * side, -0.02 * f)       # it shrinks back from the bubble
                    sc_ = 1 - 0.45 * f
                a = am * (1 - sd)
                if home[0] < -1.35:
                    a = a * (1 - 0.85 * nf)
            self._place(m, p)
            if abs(sc_ - m._sc) > 0.01:
                m.scale(sc_ / m._sc)
                m._sc = sc_
            ang = 0.3 * math.sin(sp["w"] * 0.8 * t + sp["ph"])
            if abs(ang - m._ang) > 0.004:
                m.rotate(ang - m._ang)
                m._ang = ang
            self._alpha(m, a, 0.95)
        gl = self.val("mglow")
        for h in self.mglow:
            a = gl * (0.2 + 0.08 * math.sin(1.1 * t + h._i)) * am
            if abs(a - h._a) > 0.004:
                h.set_fill(opacity=a)
                h._a = a

    def _t_layers(self, t):
        k = self.val("stack")
        if k != self._stack_last:
            for j, r in enumerate(self.stripes):
                h = STRIPE_H * clip01(k - j)
                y0 = BASIN_Y + STRIPE_H * j
                hh = max(h, 0.001)
                xa, xb = slope_x(y0) + 0.01, slope_x(y0 + hh) + 0.01
                r.set_points_as_corners([P(xa, y0), P(XR, y0), P(XR, y0 + hh), P(xb, y0 + hh), P(xa, y0)])
                o = (1.0 if j % 2 == 0 else 0.85) if h > 0.002 else 0.0
                r.set_fill(opacity=o * (lerp(0.62, 1.0, clip01((k - 0.4) / 0.6)) if j == 0 else 1.0))
            self._stack_last = k
        a = self.val("shade")
        if abs(a - self.shade._a) > 0.003:
            for r in self.shade:
                r.set_fill(opacity=0.2 * a)
            self.shade._a = a
        a = self.val("dim")
        if abs(a - self.dim._a) > 0.003:
            self.dim.set_fill(opacity=a)
            self.dim._a = a
        # the mat spreads from the first cell, then breathes
        e = self.val("mat")
        if e > 0 or self.mat[0]._a > 0:
            reach = e * (max(CELL_AT[0] - MAT_X0, MAT_X1 - CELL_AT[0]) + 0.3)
            for j, m in enumerate(self.mat):
                a = clip01((reach - abs(m._x - CELL_AT[0])) / 0.25)
                self._alpha(m, a)
                f = (0.55 + 0.45 * a) * (1 + 0.1 * math.sin(0.9 * t + 1.3 * j))
                if abs(f - m._f) > 0.004:
                    m.stretch(f / m._f, 1, about_point=P(m._x, SHELF_Y))
                    m._f = f
            ag = 0.05 * e * (1 + 0.5 * math.sin(0.9 * t)) * (1 + 2.5 * self.val("bglow"))
            if abs(ag - self.matglow._a) > 0.002:
                for r in self.matglow:
                    r.set_fill(opacity=ag)
                self.matglow._a = ag

    def _t_hud(self, t):
        s, c = self.s, self.c
        W_ = lambda x, y: c + s * P(x, y)
        # the gauge column and the scrubber strip are see-through at full frame and solid in any close-up,
        # so nothing zoomed shows through them
        hz = clip01((1.0 - s) / 0.08)
        if abs(hz - self._hz_panel) > 0.01:
            for r, o in zip(self.g["panel"], (0.8, 0.4, 0.25)):
                r.set_fill(opacity=lerp(o, 1.0, hz))
            self._hz_panel = hz
        hs = max(hz, clip01(self.val("scrdy") / 0.1))        # ...and solid while the scrubber is raised (s11), so its readout is clean
        if self.scr is not None and abs(hs - self._hz_strip) > 0.01:
            for r, o in zip(self.scr["strip"], (0.55, 0.3, 0.2)):
                r.set_fill(opacity=lerp(o, 1.0, hs))
            self._hz_strip = hs
        lvl = self.val("gauge")
        lvl_eff = lvl * (1 + 0.035 * math.sin(2.3 * t) + self.gauge_shake * 0.12 * math.sin(11 * t))
        h = gauge_h(lvl_eff)
        x0, x1, yb = G_X - G_W / 2 + 0.06, G_X + G_W / 2 - 0.06, G_Y0 + 0.06
        self.g_fill.set_points_as_corners([W_(x0, yb), W_(x1, yb), W_(x1, yb + h), W_(x0, yb + h), W_(x0, yb)])
        self.g_glow.set_points_as_corners([W_(x0 - 0.2, yb - 0.12), W_(x1 + 0.2, yb - 0.12), W_(x1 + 0.2, yb + h + 0.14), W_(x0 - 0.2, yb + h + 0.14), W_(x0 - 0.2, yb - 0.12)])
        self.g_glow.set_fill(opacity=0.14 + 0.06 * math.sin(1.9 * t))
        a2 = self.val("gauge2")
        h2 = gauge_h(1.0 * (1 + 0.004 * math.sin(2.3 * t)))
        if a2 > 0 or self.g_fill2._a > 0:
            self.g_fill2.set_points_as_corners([W_(x0, yb), W_(x1, yb), W_(x1, yb + h2), W_(x0, yb + h2), W_(x0, yb)])
            self.g_fill2.set_fill(opacity=a2)
            self.g_fill2._a = a2
        ytop = yb + (h2 if a2 > 0.5 else h)
        self.g_cap.put_start_and_end_on(W_(x0, ytop), W_(x1, ytop))
        self.g_cap.stroke_width = 3 * s
        if self.scr is None:
            return
        ph = self.val("ph")
        hol = self.val("hollow")
        dy = self.val("scrdy")
        for shp, a in ((self.ph_solid, (1 - hol) * self.ph_a), (self.ph_hollow, hol * self.ph_a)):
            pos = W_(ph, SCR_Y + dy)
            cur = getattr(shp, "_at", None)
            if cur is None:
                shp._at, shp._s_ = P(0, 0), 1.0
            if abs(s - shp._s_) > 1e-9:
                shp.scale(s / shp._s_, about_point=shp._at)
                shp._s_ = s
            shp.shift(pos - shp._at)
            shp._at = pos
            for fm in shp.get_family():
                if getattr(fm, "_bsw", 0):
                    fm.stroke_width = fm._bsw * s
                    fm.set_stroke(opacity=a, family=False)
                if getattr(fm, "_bfo", 0):
                    fm.set_fill(opacity=a * fm._bfo, family=False)
        b, bl = self.val("band"), self.val("bandlit")
        if abs(b - self.band_out._a) > 0.003:
            self.band_out.set_stroke(opacity=b)
            self.band_out.set_fill(opacity=0.6 * b)
            self.band_out._a = b
        if abs(bl - self.band_fill._a) > 0.003:
            self.band_fill.set_fill(opacity=bl)
            self.band_fill._a = bl
        # the GREEN span: cyanobacteria were here before the rise; the start is not known, so it has no left end
        sp = self.val("span")
        ys = SCR_Y + dy
        xs_solid = SPAN_X
        if sp > 0:
            xa = lerp(ph, xs_solid, min(1.0, sp / 0.25))
            self.span_solid.put_start_and_end_on(W_(xa, ys + 0.2), W_(ph, ys + 0.2))
            self.span_solid.stroke_width = 6 * s
            self.span_solid.set_stroke(opacity=1.0)
            n = len(self.span_dash)
            reach = clip01((sp - 0.25) / 0.75) * n
            for i, d in enumerate(self.span_dash):
                xr = xs_solid - 0.05 - i * 0.1          # the last dash ends inside the axis: no claim about before its start
                d.put_start_and_end_on(W_(xr - 0.065, ys + 0.2), W_(xr, ys + 0.2))
                d.stroke_width = 6 * s
                fade = (1 - i / n) ** 1.3
                d.set_stroke(opacity=clip01(reach - i) * fade * (0.75 + 0.25 * math.sin(3.0 * t - 0.8 * i)))
        else:
            self.span_solid.set_stroke(opacity=0)
            for d in self.span_dash:
                d.set_stroke(opacity=0)


# ----------------------------------------------------------------------------- scene base
class WorldScene(SpokenScene, MovingCameraScene):
    """A scene in the carried world. self.world(**stage) builds it; self.zoom(...) moves the camera."""
    SID = None

    def world(self, **stage):
        self.W = World(self, os.environ.get("KX_SCENE_ID", self.SID or ""), **stage)
        return self.W

    # camera
    def zoom(self, framing, **kw):
        c, w = framing
        return Zoom(self.camera.frame, c, w, **kw)

    def on(self, world_pt, width, screen_at=VIEW):
        """Framing that shows world_pt at the middle of the free screen area, at the given frame width."""
        return (np.array(world_pt) - (width / FW) * np.array(screen_at), width)

    # placing things designed in screen units
    def place(self, mob, s, origin, z=22):
        """Scale a mobject designed in screen units about ORIGIN (strokes too) and shift it to `origin`."""
        mob.scale(s, about_point=ORIGIN)
        for fm in mob.get_family():
            w = fm.get_stroke_width()
            if w:
                fm.set_stroke(width=float(w) * s, family=False)
        mob.shift(P(*origin[:2]))
        mob.set_z_index(z)
        return mob

    def put(self, mob, at=None, world=None, z=22):
        s, c = self.W.s, self.W.c
        mob.scale(s, about_point=ORIGIN)
        for fm in mob.get_family():
            w = fm.get_stroke_width()
            if w:
                fm.set_stroke(width=float(w) * s, family=False)
        if world is not None:
            mob.move_to(P(*world[:2]))
        elif at is not None:
            mob.move_to(c + s * P(*at))
        else:
            mob.shift(c)
        mob.set_z_index(z)
        return mob

    def hudput(self, mob, at=None, z=33):
        """Place a mobject designed in screen units and keep it fixed on screen."""
        self.put(mob, at=at, z=z)
        return self.W.pin(mob, placed=True)

    def hold(self, t):
        """Wait until scene time t."""
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

    def ripple(self, world_pt, color=TEXT, r=0.25, z=24, sw=4):
        """A ring that opens and fades (returns the animation)."""
        ring = self.put(Circle(radius=r, stroke_color=color, stroke_width=sw), world=world_pt, z=z)
        self.add(ring)
        return FadeOut(ring, scale=2.6)

    def spin(self, mob, rate=0.5, about=None):
        """Slow continuous rotation driven by the world clock (returns the function, to remove later)."""
        st = dict(last=self.W.t)

        def fn(t):
            mob.rotate(rate * (t - st["last"]), about_point=about() if callable(about) else about)
            st["last"] = t
        self.W.fns.append(fn)
        return fn

    def fly(self, mob, path, dur, delay=0.0):
        """Move a mobject along a path over `dur` seconds of film time, on the clock (so other plays can run meanwhile)."""
        t_a = self.W.t + delay

        def fn(t):
            u = clip01((t - t_a) / dur)
            mob.move_to(path.point_from_proportion(min(0.9999, ease(u) * 0.35 + u * 0.65)))
            if u >= 1:
                self.stop(fn)
        self.W.fns.append(fn)
        return fn

    def stop(self, fn):
        if fn in self.W.fns:
            self.W.fns.remove(fn)


def plate(mob, pad=0.13, opacity=0.66):
    """Put a soft dark plate behind a label so it reads over a busy part of the world."""
    r = RoundedRectangle(width=mob.width + 2 * pad, height=mob.height + 2 * pad, corner_radius=0.12, stroke_width=0,
                         fill_color="#04060C", fill_opacity=opacity).move_to(mob)
    return VGroup(r, mob)


def LBL(text, size=28, color=TEXT, **kw):
    return plate(T(text, size=size, color=color, **kw))


def ochip(text, size=28, color=TEXT, pad=0.16, **kw):
    """A label on an opaque chip with a thin outline: for words that sit on a busy or bright part of the world."""
    t = T(text, size=size, color=color, **kw)
    box = RoundedRectangle(width=t.width + 2 * pad + 0.1, height=t.height + 2 * pad, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                           fill_color="#04060C", fill_opacity=0.96).move_to(t)
    return VGroup(box, t)


# shared, rebuilt-in-place screen furniture ------------------------------------------------------
def question_puzzle():
    g = VGroup(T("The mats release oxygen.", size=34), T("Why does the air not fill?", size=34)).arrange(DOWN, buff=0.22)
    return VGroup(plate(g, pad=0.2, opacity=0.6)[0], g[0], g[1]).move_to(P(0.75, 2.5))


def question_microbes():
    return VGroup(T("What happened to the old microbes?", size=34), T("A mass die-off?", size=34)).arrange(DOWN, buff=0.22)


def guiding_line():
    a = Text("The air keeps only the oxygen", font=FONT, font_size=36, color=TEXT, t2c={"oxygen": BLUE})
    b = Text("that nothing else takes first.", font=FONT, font_size=36, color=TEXT)
    g = VGroup(a, b).arrange(DOWN, buff=0.24)
    return VGroup(plate(g, pad=0.22, opacity=0.9)[0], a, b).move_to(P(-0.3, 1.8))


def analogy_words():
    """'analogy', 'tap', 'drains' and four short ticks at the takers (full-frame coordinates)."""
    tag = VGroup(RoundedRectangle(width=1.9, height=0.56, corner_radius=0.2, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=0.6),
                 T("analogy", size=28)).move_to(P(-0.2, 3.5))
    # "tap" sits on the rock under the mat, clear of the bubble stream, and points up at it
    tw = ochip("tap", size=34, weight=BOLD).move_to(P(-2.9, -1.62))
    tap = VGroup(tw, Line(tw.get_top() + UP * 0.04, P(-2.9, SHELF_Y - 0.06), stroke_color=TEXT, stroke_width=5).add_tip(tip_length=0.2, tip_width=0.2))
    # "drains" is tied to each of the four takers by its own arrow
    drains = ochip("drains", size=34, weight=BOLD).move_to(P(-0.9, 1.95))
    targets = [P(2.9, -0.2), P(-4.65, 3.05), P(2.6, 2.6), P(-4.45, 1.55)]      # iron, plume, methane, shore
    ticks = VGroup()
    hw, hh = drains.width / 2 + 0.08, drains.height / 2 + 0.08
    for q in targets:
        d = q - drains.get_center()
        n = np.linalg.norm(d)
        d = d / n
        k = min(hw / max(abs(d[0]), 1e-6), hh / max(abs(d[1]), 1e-6))
        ticks.add(Line(drains.get_center() + d * k, q - d * 0.24, stroke_color=TEXT, stroke_width=5).add_tip(tip_length=0.26, tip_width=0.26))
    return tag, tap, drains, ticks, targets


def goe_name():
    return plate(T("Great Oxygenation Event", size=34, color=BLUE, weight=BOLD), pad=0.16, opacity=0.9).move_to(P(1.1, 3.5))


def goe_tag():
    return T("Great Oxygenation Event", size=28, color=BLUE).move_to(P((PH_GOE0 + PH_GOE1) / 2 + 0.2, -2.98))


# ============================================================================= the scenes
class S00Hook(WorldScene):
    def construct(self):
        W = self.world(cam=TIGHT_SKY, pips=N_PIPS, gauge=1.0, scrub=False, ph=PH_TODAY, readout=None)
        self.at("next breath")
        self.play(self.zoom((P(0.9, 2.5), 4.5)), run_time=2.7)
        self.at("Leftovers from")
        q = self.hudput(T("?", size=130, weight=BOLD), at=(3.25, 0.5))
        self.play(FadeIn(q, scale=0.4), run_time=0.45)
        self.play(q.animate.scale(1.15), rate_func=there_and_back, run_time=1.5)
        # Rewind: the scrubber draws on, the playhead sweeps back, the sky drains, the gauge falls, the view pulls back
        self.at("Rewind", lead=0.3)
        W.ph_a = 0.0
        parts = W.add_scrubber()
        W.unpin(q)
        self.play(FadeOut(q, scale=0.6), *[FadeIn(m) for m in parts[:4]], UpdateFromAlphaFunc(Mobject(), lambda m, a: setattr(W, "ph_a", a)), run_time=0.45)
        W.ramp("ph", PH_3GA, 1.5)
        W.ramp("gauge", G_SLIVER, 2.9)
        W.ramp("pips", 3, 2.9)
        self.wait(1.0)
        ro = W.readout_text("about 3 billion years ago")
        W.readout = ro
        self.play(FadeIn(ro, shift=UP * 0.1 * W.s), run_time=0.3)
        self.play(self.zoom(FULL), run_time=1.6)
        # Watch the gauge: the tube brightens and a bracket closes on the sliver
        self.at("Watch the gauge")
        yb = G_Y0 + 0.06
        halo = W.g["tube"].copy().set_fill(opacity=0).set_stroke(WHITE, width=9, opacity=0.9).set_z_index(35)
        bl = bracket(0.46, left=True).move_to(P(G_X - 1.0, yb + 0.05)).set_z_index(35)
        br = bracket(0.46, left=False).move_to(P(G_X + 1.0, yb + 0.05)).set_z_index(35)
        self.play(FadeIn(halo), FadeIn(bl), FadeIn(br), run_time=0.35)
        self.play(FadeOut(halo), bl.animate.move_to(P(G_X - 0.42, yb + 0.05)), br.animate.move_to(P(G_X + 0.42, yb + 0.05)), run_time=0.7)
        self.at("almost no oxygen")
        W.gauge_shake = 1.0
        self.play(self.ripple(P(G_X, yb), BLUE, r=0.3, z=36), *[self.ripple(W.pip_pos(i), BLUE, r=0.2) for i in range(3)], run_time=1.1)
        W.gauge_shake = 0.0
        # Something had to fill this sky: a ghost of the full level flashes up, then sinks back
        self.at("had to fill")
        gh = DashedVMobject(Rectangle(width=G_W - 0.14, height=G_TICK - yb, stroke_color=BLUE, stroke_width=4), num_dashes=40)
        gh.move_to(P(G_X, (G_TICK + yb) / 2)).set_z_index(34)
        ghf = Rectangle(width=G_W - 0.14, height=G_TICK - yb, stroke_width=0, fill_color=BLUE, fill_opacity=0.28).move_to(gh).set_z_index(33.5)
        ghost = VGroup(ghf, gh)
        self.play(GrowFromEdge(ghost, DOWN), run_time=0.8)
        self.at("held it back", lead=0.35)
        q2 = T("?", size=110, weight=BOLD).move_to(P(3.7, 0.3)).set_z_index(35)
        self.play(ghost.animate.stretch_to_fit_height(0.08, about_edge=DOWN).set_opacity(0.0), run_time=0.9)
        self.remove(ghost)
        self.play(FadeIn(q2, shift=DOWN * 0.2), run_time=0.4)
        self.finish()


class S01Title(WorldScene, TitleCard):
    LESSON = "Oxidative Phosphorylation"
    TITLE = "How Earth Got Its Oxygen"

    def construct(self):
        self.world()
        veil = Rectangle(width=FW + 1, height=FH + 1, stroke_width=0, fill_color="#03040A", fill_opacity=0).set_z_index(40)
        brand = T("BIOCHEMISTRYPEDIA", size=28, color=TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), size=28, color=TEXT)
        title = T(self.TITLE, size=58, font=TITLE_FONT)
        rule = Line(LEFT * 1.3, RIGHT * 1.3, color=GOLD, stroke_width=4)
        card = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32).set_z_index(41)
        self.add(veil)
        self.play(veil.animate.set_fill(opacity=0.74), FadeIn(card, shift=UP * 0.15), run_time=0.5)
        self.play(rule.animate.stretch(1.25, 0), run_time=1.2, rate_func=there_and_back)
        self.play(veil.animate.set_fill(opacity=0), FadeOut(card, shift=UP * 0.3), run_time=0.5)
        self.finish()


class S02World(WorldScene):
    def construct(self):
        W = self.world()
        # rebuilt from ancient rocks: the sea-floor rock brightens for a beat
        self.at("ancient rocks", lead=0.6)
        hi = poly([(SHELF_X1 + 0.1, SHELF_Y - 0.25), (BASIN_X0, BASIN_Y), (XR, BASIN_Y), (XR, YB), (SHELF_X1 - 1.6, YB)], "#C9C2DC", 0.0).set_z_index(1.5)
        edge = VMobject(stroke_color=WHITE, stroke_width=6).set_points_as_corners([P(SHELF_X1 + 0.1, SHELF_Y - 0.25), P(BASIN_X0, BASIN_Y), P(XR, BASIN_Y)])
        edge.set_stroke(opacity=0).set_z_index(7)
        lab = self.put(ochip("rebuilt from ancient rocks", size=28), world=(1.45, -1.5))
        ptr = Line(lab.get_bottom(), P(1.45, BASIN_Y + 0.05), stroke_color=TEXT, stroke_width=4).set_z_index(22)
        self.add(hi, edge)
        self.play(hi.animate.set_fill(opacity=0.5), edge.animate.set_stroke(opacity=0.9), FadeIn(lab, shift=UP * 0.1), Create(ptr), run_time=0.5)
        self.play(hi.animate.set_fill(opacity=0.3), run_time=1.45, rate_func=there_and_back)
        self.play(hi.animate.set_fill(opacity=0), edge.animate.set_stroke(opacity=0), FadeOut(lab), FadeOut(ptr), run_time=0.5)
        self.remove(hi, edge)
        # the sea held dissolved iron: the discs fade in, then are named
        self.at("The sea held", lead=0.3)
        W.ramp("iron", 1.0, 1.2)
        self.hold(5.95)
        lab2 = self.put(LBL("dissolved iron", size=30), world=(2.0, 0.25))
        self.play(FadeIn(lab2, shift=UP * 0.1), run_time=0.35)
        self.hold(6.85)
        self.play(FadeOut(lab2), run_time=0.25)             # gone before the push-in, so it is never enlarged or cut
        # show, then tell: push in on one disc; a yellow dot rides its rim
        W.hole_at, W.hole_r = HERO_IRON, 0.5
        W.ramp("hole", 1.0, 0.6)
        W.ramp("edots", 1.0, 0.8, delay=0.3)
        self.play(self.zoom(self.on(HERO_IRON, 0.92)), run_time=1.25)
        self.at("electrons to give")
        dot = W.iron[0][1]
        el = self.put(LBL("electron", size=32, color=YELLOW), world=W.world_of(VIEW[0] + 3.0, VIEW[1] + 1.6)[:2])
        ptr = Line(ORIGIN, RIGHT, stroke_color=YELLOW, stroke_width=3 * W.s).set_z_index(22)
        aim = lambda t: ptr.put_start_and_end_on(el.get_corner(DL) + W.s * P(-0.05, -0.05), dot.get_center() + W.s * P(0.35, 0.3))
        aim(0)
        W.fns.append(aim)
        self.play(self.ripple(dot.get_center(), YELLOW, r=0.5, sw=5), FadeIn(el), FadeIn(ptr), run_time=0.6)
        self.wait(1.3)
        self.play(FadeOut(el), FadeOut(ptr), run_time=0.35)
        self.stop(aim)
        # little oxygen: widen; nothing blue is near; three pips in the sky are too few to matter
        self.at("with little oxygen", lead=0.35)
        self.play(self.zoom((P(2.2, 0.65), 9.5)), run_time=1.4)
        self.play(*[self.ripple(W.pip_pos(i), BLUE, r=0.24) for i in range(3)], run_time=1.0)
        self.at("stayed dissolved", lead=0.5)
        W.ramp("hole", 0.0, 1.0)
        self.play(self.zoom(FULL), run_time=1.3)
        self.play(*[self.ripple(W.iron[i][1].get_center(), YELLOW, r=0.1, sw=3) for i in (3, 8, 13, 19, 24, 31)], run_time=0.6)
        self.finish()


class S03Life(WorldScene):
    def construct(self):
        W = self.world(iron=1, edots=1, methane=True)
        W.ramp("microbes", 1.0, 1.5, delay=0.5)
        self.play(self.zoom(SEABED), run_time=1.5)
        self.hold(3.0)
        lab = self.put(LBL("microbes", size=32, color=TEXT), world=(2.6, -1.5))
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        # without oxygen: a look up at the empty water, and back down
        self.at("without oxygen", lead=0.9)
        self.play(self.zoom((SEABED[0] + P(0, 0.55), SEABED[1])), FadeOut(lab), run_time=1.0)
        self.wait(0.4)
        self.play(self.zoom(SEABED), run_time=0.9)
        # fermenting: a patch on the shelf pulses and its cells split in two
        self.at("fermenting", lead=0.1)
        W.ramp("split", 1.0, 1.0, delay=0.2)
        patch = P(SHELF_CELLS[1] + 0.07, SHELF_Y + 0.16)
        glow = self.put(Circle(radius=0.95, stroke_width=0, fill_color=PURPLE, fill_opacity=0.0), world=patch, z=7.5)
        self.add(glow)
        self.play(glow.animate.set_fill(opacity=0.3), self.ripple(patch, PURPLE, r=0.7, sw=5), run_time=0.5)
        self.play(glow.animate.set_fill(opacity=0.0), self.ripple(patch, PURPLE, r=0.9, sw=5), run_time=0.6)
        self.remove(glow)
        # making methane: grey rings, each carrying an electron, start to rise (and never stop)
        self.at("making methane", lead=0.0)
        self.play(self.ripple(P(RING_X, BASIN_Y + 0.1), TEXT, r=0.3), run_time=0.5)
        ml = self.put(LBL("methane", size=28), world=(RING_X - 0.9, BASIN_Y + 0.4))
        ride = lambda t: ml.move_to(W.rings[0]._p + W.s * P(-1.2, 0.0))
        ride(0)
        W.fns.append(ride)
        self.play(FadeIn(ml), run_time=0.3)
        self.wait(1.0)
        self.play(FadeOut(ml), run_time=0.35)
        self.stop(ride)
        # Remember them: a ring closes on one cluster, then shrinks to a bookmark
        self.at("Remember them", lead=0.3)
        ring = self.put(Circle(radius=0.7, stroke_color=TEXT, stroke_width=4), world=BOOK_AT + UP * 0.07)
        ring.scale(2.2)
        self.add(ring)
        self.play(ring.animate.scale(1 / 2.2), run_time=0.8)
        self.play(ring.animate.scale(1.1), rate_func=there_and_back, run_time=1.1)
        self.at("come back", lead=0.3)
        bk = bookmark(1.0).move_to(BOOK_AT + UP * (BOOK_DY + STRIPE_H * 0.4 - 0.02)).set_z_index(15)
        self.play(ReplacementTransform(ring, bk), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- the one cell, close up
CELL_S = 0.06
CELL_K = 1.22                                  # how much bigger than its design size the cell is shown
CELLCAM = (CELL_AT - (CELL_S / CELL_K) * P(-1.4, 0.0), FW * CELL_S / CELL_K)


def cellpt(x, y):
    """A point given in the cell's own (screen-size) coordinates -> world."""
    return CELL_AT + CELL_S * P(x, y)


# the two droplets, in the cell's coordinates: where they appear (inside the frame), where they bump the closed
# mouth, where they bounce to, and where they rest inside the cell
DROP_A = [(-3.85, 2.4), (-2.25, 2.0), (-2.8, 2.4), (-2.1, 0.12)]
DROP_B = [(-3.0, 1.3), (-1.15, 2.1), (-0.7, 2.5), (-1.1, 0.12)]


class S04Trick(WorldScene):
    def construct(self):
        W = self.world(cam=SEABED, iron=1, edots=1, microbes=1, split=1, methane=True, tick=True)
        pl = lambda m, q, z=17: self.place(m, CELL_S, cellpt(*q), z)
        # the date of this trick is debated: the playhead goes hollow and does not move
        W.ramp("hollow", 1.0, 0.4)
        W.set_readout("when? debated", rt=0.45)
        cell = pl(cyano_cell(), (0, 0), 16)
        W.hole_at, W.hole_r = CELL_AT + P(0, 0.08), 0.62
        W.ramp("hole", 1.0, 0.8)
        self.play(FadeIn(cell), self.zoom(CELLCAM), run_time=2.0)
        # Water holds its electrons tightly: two droplets bump the closed mouth and bounce
        self.at("Water holds", lead=0.5)
        A, B = DROP_A, DROP_B
        d1, d2 = pl(droplet(0.36), A[0]), pl(droplet(0.36), B[0])
        dots = list(d1[2]) + list(d2[2])
        for k, e in enumerate(dots):
            e._o = P(0, 0)

        def jitter(t):
            for k, e in enumerate(dots):
                o = CELL_S * 0.045 * P(math.sin(9 * t + 1.7 * k), math.cos(11 * t + 2.3 * k))
                e.shift(o - e._o)
                e._o = o
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.25)
        W.fns.append(jitter)
        self.play(d1.animate.move_to(cellpt(*A[1])), d2.animate.move_to(cellpt(*B[1])), run_time=0.8, rate_func=rush_from)
        for _ in range(2):
            self.play(d1.animate.shift(DOWN * 0.3 * CELL_S), d2.animate.shift(DOWN * 0.3 * CELL_S), cell.lid.animate.shift(DOWN * 0.05 * CELL_S),
                      run_time=0.36, rate_func=there_and_back)
        self.play(d1.animate.move_to(cellpt(*A[2])), d2.animate.move_to(cellpt(*B[2])), run_time=0.7, rate_func=rush_from)
        self.at("Cyanobacteria", lead=0.1)
        name = pl(T("cyanobacterium", size=32, color=GREEN), (0, -1.95), 22)
        name.move_to(cellpt(0, -1.95))
        self.play(FadeIn(name, shift=UP * 0.1 * CELL_S), run_time=0.45)
        # learned to pull them out: the mouth opens and takes both droplets in
        self.at("pull them out", lead=0.3)
        self.play(Rotate(cell.lid, 1.25, about_point=cellpt(*cell.hinge[:2])), run_time=0.3)
        self.play(d1.animate.move_to(cellpt(*A[3])), d2.animate.move_to(cellpt(*B[3])), run_time=0.65)
        # powered by sunlight: a GOLD ray strikes, the cell flashes, four electrons are torn out
        self.at("powered by sunlight", lead=0.25)
        ray = pl(VGroup(poly([(-6.4, 6.3), (-3.9, 6.3), (1.0, 1.28), (-1.2, 1.28)], GOLD, 0.3),
                        poly([(-5.5, 6.3), (-4.8, 6.3), (0.2, 1.28), (-0.4, 1.28)], "#FFE9A8", 0.35)), (0, 0), 15.5)
        flash = pl(RoundedRectangle(width=6.0, height=2.6, corner_radius=1.28, stroke_width=0, fill_color="#D9FFB0", fill_opacity=0.0), (0, 0), 18)
        self.add(flash)
        self.play(FadeIn(ray), flash.animate.set_fill(opacity=0.45), run_time=0.3)
        self.stop(jitter)
        for d in (d1, d2):
            d.remove(d[2])
        self.add(*dots)
        for e in dots:
            e.set_z_index(19)
        kept = [(-0.3, 0.42), (0.2, 0.42), (-0.3, -0.08), (0.2, -0.08)]
        self.play(flash.animate.set_fill(opacity=0.0), d1[0].animate.set_fill(BLUE, opacity=0.6), d2[0].animate.set_fill(BLUE, opacity=0.6),
                  *[e.animate(path_arc=-1.0).move_to(cellpt(x - 0.35, y + 0.25)) for e, (x, y) in zip(dots, kept)], run_time=0.9)
        self.remove(flash)
        # They kept the electrons: the four dots slide deep into the cell and glow
        self.at("kept the electrons", lead=0.2)
        halos = [pl(Dot(ORIGIN, radius=0.24, color=YELLOW).set_opacity(0.28), (0, 0), 18.5).move_to(e) for e in dots]
        pairs = [VGroup(h, e) for h, e in zip(halos, dots)]
        self.play(*[FadeIn(h) for h in halos], ray.animate.set_opacity(0.12), run_time=0.3)
        self.play(*[pr.animate.move_to(cellpt(x + 0.25, y)) for pr, (x, y) in zip(pairs, kept)],
                  d1.animate.move_to(cellpt(1.3, 0.72)), d2.animate.move_to(cellpt(1.85, 0.7)), run_time=1.0)
        # to build their own food: the dots sink into a plain GREEN block, which grows by a notch
        self.at("build their own", lead=0.2)
        fpt = cell.food.get_center()
        self.play(*[pr.animate.move_to(fpt).scale(0.5) for pr in pairs], run_time=0.6)
        self.play(*[FadeOut(pr) for pr in pairs], cell.food.animate.stretch(1.35, 0, about_edge=LEFT).set_fill("#B5F08F"), run_time=0.35)
        fl = pl(T("food", size=32, color=TEXT, weight=BOLD), (0, 0), 22).move_to(cellpt(0.0, -0.52))
        self.play(cell.food.animate.set_fill(GREEN), FadeIn(fl), run_time=0.4)
        # The waste was oxygen gas: what is left of the water swells at the vent as one BLUE bubble
        self.at("The waste", lead=0.4)
        bub = pl(VGroup(Circle(radius=0.5, stroke_color="#BFEAF5", stroke_width=4, fill_color=BLUE, fill_opacity=0.95),
                        Arc(radius=0.33, start_angle=2.0, angle=0.9, stroke_color=WHITE, stroke_width=4).set_stroke(opacity=0.6)), (0, 0), 19)
        bub.move_to(cellpt(cell.vent_tip[0], cell.vent_tip[1] + 0.52))
        self.play(ReplacementTransform(VGroup(d1, d2), bub), run_time=0.9)
        self.play(bub.animate.scale(1.08), run_time=0.9, rate_func=there_and_back)
        # and they let it go
        self.at("let it go", lead=0.25)
        self.play(bub.animate.shift(UP * 4.6 * CELL_S), FadeOut(fl), run_time=0.75, rate_func=rush_into)
        self.remove(bub)
        # the cycle starts again (two more droplets, straight in)
        d3, d4 = pl(droplet(0.36), A[0]), pl(droplet(0.36), B[0])
        self.play(FadeIn(d3), FadeIn(d4), run_time=0.2)
        self.play(d3.animate.move_to(cellpt(*A[3])), d4.animate.move_to(cellpt(*B[3])), run_time=max(0.3, self.narration_s + 0.38 - self.elapsed()))
        self.finish()


class S05Puzzle(WorldScene):
    def construct(self):
        W = self.world(cam=CELLCAM, iron=1, edots=1, microbes=1, split=1, methane=True, tick=True, hollow=1, readout="when? debated",
                       bubbles=True, hole=1)
        W.hole_at, W.hole_r = CELL_AT + P(0, 0.08), 0.62
        pl = lambda m, q, z=17: self.place(m, CELL_S, cellpt(*q), z)
        cell = cyano_cell()
        cell.lid.rotate(1.25, about_point=cell.hinge)
        cell.food.stretch(1.35, 0, about_edge=LEFT)
        pl(cell, (0, 0), 16)
        ray = pl(poly([(-6.4, 6.3), (-3.9, 6.3), (1.0, 1.28), (-1.2, 1.28)], GOLD, 0.12), (0, 0), 15.5)
        d3, d4 = pl(droplet(0.36), (0, 0)).move_to(cellpt(-2.1, 0.12)), pl(droplet(0.36), (0, 0)).move_to(cellpt(-1.1, 0.12))
        bub = pl(Circle(radius=0.5, stroke_color="#BFEAF5", stroke_width=4, fill_color=BLUE, fill_opacity=0.95), (0, 0), 19)
        bub.move_to(cellpt(cell.vent_tip[0], cell.vent_tip[1] + 0.52))
        self.add(ray, cell, d3, d4)
        self.play(GrowFromCenter(bub), FadeOut(d3, scale=0.5), FadeOut(d4, scale=0.5), run_time=0.45)
        # pull back; the one cell multiplies sideways into a mat
        W.ramp("hole", 0.0, 1.5)
        W.ramp("mat", 1.0, 2.0, delay=1.0)
        self.play(self.zoom(FULL), bub.animate.shift(UP * 0.5), FadeOut(ray), run_time=1.9)
        self.play(FadeOut(cell), FadeOut(bub), run_time=0.7)
        lab = self.put(LBL("cyanobacterial mats", size=28, color=GREEN), world=(-2.9, -1.5))
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.4)
        # here is a puzzle: frame mat, water column and gauge together
        self.at("here is a puzzle", lead=0.2)
        self.play(self.zoom(PUZZLE_CAM), run_time=2.2)
        # the mats were releasing oxygen: bubbles stream up and fade part-way, with no visible cause yet
        self.at("releasing oxygen", lead=0.2)
        W.ramp("bglow", 1.0, 0.6)
        self.play(self.ripple(P(-2.9, SHELF_Y + 0.15), BLUE, r=0.5), run_time=0.9)
        W.ramp("bglow", 0.0, 1.5)
        # Why did the air not fill: the gauge has not moved
        self.at("Why did the", lead=0.5)
        halo, bl, br = sliver_marks(self)
        self.play(FadeOut(lab), FadeIn(halo), FadeIn(bl), FadeIn(br), run_time=0.35)
        ql = self.put(question_puzzle(), world=(0.75, 2.5))
        self.play(FadeOut(halo), bl.animate.shift(RIGHT * 0.58 * W.s), br.animate.shift(LEFT * 0.58 * W.s), FadeIn(ql[0]), Write(ql[1]), run_time=0.8)
        self.play(Write(ql[2]), run_time=0.8)
        W.gauge_shake = 0.6
        self.finish()


PUZZLE_CAM = (P(-0.3, 0.12), 13.1)


def sliver_marks(scene, closed=False):
    """A white halo on the gauge tube and a bracket either side of its thin sliver (screen-fixed)."""
    W = scene.W
    yb = G_Y0 + 0.06
    halo = scene.hudput(W.g["tube"].copy().scale(1 / W.s, about_point=W.c).shift(-W.c).set_fill(opacity=0).set_stroke(WHITE, width=9, opacity=0.9), z=35)
    off = 0.42 if closed else 1.0
    bl = scene.hudput(bracket(0.46, left=True), at=(G_X - off, yb + 0.05), z=35)
    br = scene.hudput(bracket(0.46, left=False), at=(G_X + off, yb + 0.05), z=35)
    return halo, bl, br


class S06Pause(WorldScene):
    def construct(self):
        W = self.world(cam=PUZZLE_CAM, iron=1, edots=1, microbes=1, split=1, methane=True, tick=True, hollow=1, readout="when? debated",
                       bubbles=True, mat=1)
        W.gauge_shake = 0.6
        _, bl, br = sliver_marks(self, closed=True)
        ql = self.put(question_puzzle(), world=(0.75, 2.5))
        self.add(bl, br, ql)
        self.play(self.zoom(FULL), run_time=self.narration_s + 0.35, rate_func=linear)
        self.finish()


HB = P(-1.2, 0.0)          # where the hero bubble is met in mid-water
HB_S = 0.07
HB_K = 1.9                 # the bubble is shown this much larger than its design size: about half the frame height
IRON_OFF = (1.79, 1.0)     # where each iron disc comes to rest, from the bubble's centre (design units)


class S07Iron(WorldScene):
    def construct(self):
        W = self.world(iron=1, edots=1, microbes=1, split=1, methane=True, tick=True, hollow=1, readout="when? debated", bubbles=True, mat=1)
        pl = lambda m, q, z=20: self.place(m, HB_S, HB + HB_S * P(*q), z)
        _, bl, br = sliver_marks(self, closed=True)
        ql = question_puzzle().set_z_index(22)
        self.add(bl, br, ql)
        self.play(FadeOut(ql, shift=UP * 0.4), FadeOut(bl), FadeOut(br), run_time=0.6)
        # other places to go: dive after one bubble
        hb = pl(hero_bubble(1.0), (0, 0))
        glow, disc, socks, edots = hb
        socks.set_opacity(0)
        hb.move_to(P(-2.4, SHELF_Y + 0.45))
        self.add(hb)
        W.hole_at, W.hole_r = HB, 0.52
        W.ramp("hole", 1.0, 1.4, delay=0.3)
        self.play(hb.animate.move_to(HB), self.ripple(P(-2.4, SHELF_Y + 0.45), BLUE, r=0.3), run_time=1.0)
        self.play(self.zoom(self.on(HB, FW * HB_S / HB_K)), run_time=2.2)
        # Oxygen strongly pulls in electrons: four empty sockets, each tugging at the water (streaks run inward to each)
        self.at("strongly pulls in", lead=0.5)
        for sk in socks:
            sk[0].set_fill(opacity=0.95)
            sk[1].set_stroke(opacity=1)
        socks.set_opacity(0)
        self.play(*[sk[0].animate.set_fill(opacity=0.95) for sk in socks], *[sk[1].animate.set_stroke(opacity=1.0) for sk in socks], run_time=0.5)
        dirs = [P(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in SOCKET_ANG]
        streaks = VGroup(*[Line(ORIGIN, RIGHT * HB_S, stroke_color=TEXT, stroke_width=5 * HB_S).set_stroke(opacity=0) for _ in range(12)]).set_z_index(19.5)
        self.add(streaks)
        tug = dict(on=1.0)

        def pull(t):
            for i, m in enumerate(streaks):
                k, lane = i % 4, i // 4 - 1
                u = (0.85 * t + i * 0.29) % 1.0
                side = P(-dirs[k][1], dirs[k][0]) * (0.2 * lane)
                r1 = lerp(1.85, 1.1, u * u)                      # just outside the rim, running inward
                ln = 0.42 * (1 - 0.5 * u)
                m.put_start_and_end_on(HB + HB_S * (dirs[k] * (r1 + ln) + side), HB + HB_S * (dirs[k] * r1 + side * 0.7))
                m.set_stroke(opacity=tug["on"] * 0.9 * math.sin(math.pi * u) ** 0.8)
        W.fns.append(pull)
        # Each oxygen molecule can take four: four GREY iron discs are already on their way in, from the four corners
        self.at("Each oxygen", lead=0.25)
        irons, idots, offs = [], [], []
        for d in dirs:
            o = P(IRON_OFF[0] * (1 if d[0] > 0 else -1), IRON_OFF[1] * (1 if d[1] > 0 else -1))
            g = pl(iron_disc(0.46, dot=False), (0, 0), 21)
            e = pl(Dot(ORIGIN, radius=0.14, color=YELLOW), (0, 0), 21.5)
            irons.append(g)
            idots.append(e)
            offs.append(o)
        t_in, dur_in = W.t, 4.7

        def approach(t):
            u = clip01((t - t_in) / dur_in)
            f = lerp(3.3, 1.0, 1 - (1 - u) ** 3)
            for k, (g, e, o) in enumerate(zip(irons, idots, offs)):
                c = HB + HB_S * (o * f + 0.045 * P(math.sin(1.3 * t + 1.9 * k), math.cos(1.1 * t + 2.3 * k)))
                g.move_to(c)
                e.move_to(c - HB_S * 0.46 * o / np.linalg.norm(o))
        approach(W.t)
        self.add(*irons, *idots)
        W.fns.append(approach)
        # ...the sockets light in turn, one, two, three, four, and stay lit
        self.at("can take four", lead=0.35)
        rings, nums = [], []
        for n, k in enumerate((1, 0, 2, 3)):
            c = socks[k][0].get_center()
            ring = pl(Circle(radius=0.2, stroke_color=YELLOW, stroke_width=9), (0, 0), 20.6).move_to(c)
            num = pl(T(str(n + 1), size=24, weight=BOLD), (0, 0), 20.7).move_to(c)
            rings.append(ring)
            nums.append(num)
            self.play(FadeIn(ring, scale=1.7), FadeIn(num, scale=0.4), self.ripple(c, YELLOW, r=0.42, z=23, sw=7), run_time=0.3)
            self.wait(0.06)
        # the sea held iron with electrons to give: the discs arrive, each with its YELLOW dot on the rim facing the bubble
        self.at("iron with electrons", lead=0.3)
        self.play(*[FadeOut(m, scale=0.6) for m in nums], run_time=0.4)
        self.play(*[self.ripple(e.get_center(), YELLOW, r=0.3, z=23) for e in idots], run_time=0.9)
        # iron handed its electrons to oxygen: four jumps; each iron disc turns RED as its dot leaves
        self.at("handed its electrons", lead=0.25)
        self.stop(approach)
        tug["on"] = 0.5
        for k in range(4):
            tgt = socks[k][0].get_center()
            self.play(idots[k].animate(path_arc=0.8).move_to(tgt), irons[k][0].animate.set_fill(RED).set_stroke("#FFB3AA"), run_time=0.3)
            self.play(self.ripple(tgt, YELLOW, r=0.3, z=23), run_time=0.14)
        tug["on"] = 0.0
        # formed rust-like minerals: the four red discs pull into one flake; the bubble is used up
        self.at("formed rust", lead=0.45)
        flake = pl(rust_flake(1.5), (0, 0), 21)
        self.play(ReplacementTransform(VGroup(*irons), flake), FadeOut(VGroup(glow, disc, socks, *idots, *rings), scale=0.2), FadeOut(streaks), run_time=0.7)
        self.stop(pull)
        lab = self.put(LBL("rust-like mineral", size=32, color=RED), world=HB + HB_S * P(0, 1.42))
        self.play(FadeIn(lab, shift=UP * 0.1 * HB_S), flake.animate.rotate(0.25), run_time=0.3)
        W.ramp("flakes", 1.0, 0.5)
        # and sank; pull back: it is happening everywhere
        self.play(flake.animate.rotate(-0.35), run_time=max(0.2, self.t_of("and sank") - 0.1 - self.elapsed()), rate_func=there_and_back)
        W.ramp("hole", 0.0, 1.0, delay=0.3)
        self.play(flake.animate.shift(DOWN * 2.2 * HB_S).rotate(0.4), FadeOut(lab), run_time=0.4, rate_func=rush_into)
        self.play(flake.animate.shift(DOWN * 0.75).rotate(0.6), self.zoom(FULL), run_time=max(0.4, self.narration_s + 0.35 - self.elapsed()))
        self.finish()


class S08Bands(WorldScene):
    def construct(self):
        W = self.world(iron=1, edots=1, microbes=1, split=1, methane=True, tick=True, hollow=1, readout="when? debated", bubbles=True, mat=1, flakes=1)
        # the clock runs again (no number until the band lights)
        W.ramp("hollow", 0.0, 0.4)
        W.ramp("stack", 1.0, 1.7)
        W.ramp("ph", PH_S08, 16.6)
        W.set_readout("before the rise", rt=0.45)
        self.play(self.zoom(BASIN), run_time=1.4)
        # and silica: a pale stripe grows on the red one, and the word gets its picture
        self.at("and silica", lead=0.1)
        W.ramp("stack", 2.0, 0.7)
        si = self.put(LBL("silica", size=28), world=(1.0, BASIN_Y + 0.72))
        ptr = Line(si.get_bottom(), P(1.0, BASIN_Y + 0.2), stroke_color=TEXT, stroke_width=3 * W.s).set_z_index(22)
        self.play(FadeIn(si), Create(ptr), run_time=0.4)
        W.ramp("stack", 8.0, 2.7, delay=0.5)
        self.wait(0.7)
        self.play(FadeOut(si), FadeOut(ptr), run_time=0.35)
        # banded iron formations: named after the stack is seen
        self.at("banded iron formations", lead=0.0)
        bif = self.put(LBL("banded iron formations", size=30), world=(3.45, -0.12))
        self.play(FadeIn(bif, shift=UP * 0.1), run_time=0.45)
        # much of the iron we mine: a bracket closes on the stack and a pick taps it
        self.at("iron we mine", lead=0.4)
        top = BASIN_Y + 8 * STRIPE_H
        # the left arm runs along the slope, where the stack really ends
        b1 = VMobject(stroke_color=TEXT, stroke_width=5 * W.s).set_z_index(22)
        b1.set_points_as_corners([P(slope_x(top + 0.06) - 0.02, top + 0.06), P(slope_x(top + 0.06) - 0.12, top + 0.06),
                                  P(slope_x(BASIN_Y - 0.06) - 0.12, BASIN_Y - 0.06), P(slope_x(BASIN_Y - 0.06) - 0.02, BASIN_Y - 0.06)])
        b2 = self.put(bracket((top - BASIN_Y + 0.12) / W.s, left=False, sw=5), world=(5.3, (top + BASIN_Y) / 2))
        pick = self.put(pick_icon(1.3), world=(2.75, top + 0.36))
        tag = self.put(LBL("mined today", size=28), world=(3.95, top + 0.3))
        self.play(FadeIn(b1, shift=RIGHT * 0.3), FadeIn(b2, shift=LEFT * 0.3), FadeIn(pick), run_time=0.45)
        tip = pick.get_corner(DL)
        self.play(Rotate(pick, 0.7, about_point=tip), run_time=0.22, rate_func=rush_into)
        self.play(Rotate(pick, -0.7, about_point=tip), FadeIn(tag), run_time=0.3)
        self.play(Rotate(pick, 0.7, about_point=tip), run_time=0.22, rate_func=rush_into)
        self.play(Rotate(pick, -0.7, about_point=tip), run_time=0.3)
        self.play(Rotate(pick, 0.7, about_point=tip), run_time=0.22, rate_func=rush_into)
        self.play(Rotate(pick, -0.7, about_point=tip), run_time=0.3)
        # Some layers may be the work of microbes that rust iron without any oxygen (dim sunlit water, one gold ray)
        self.at("Some layers may", lead=0.75)
        MB = P(1.9, 0.18)
        W.hole_at, W.hole_r = MB + P(0.3, 0), 0.95
        W.ramp("hole", 1.0, 0.8)
        W.ramp("bfade", 1.0, 0.7)             # no blue bubble anywhere in this shot
        self.play(FadeOut(VGroup(b1, b2, pick, tag, bif)), self.zoom(LIFT), run_time=1.1)
        mb = self.place(microbe(0, 3.0), 1.0, MB, 21)
        ray = poly([(1.35, SEA_Y), (1.75, SEA_Y), (2.25, 0.0), (1.55, 0.0)], GOLD, 0.2).set_z_index(15)
        fe = self.place(iron_disc(0.13), 1.0, P(3.6, 0.42), 21)
        self.play(FadeIn(mb, scale=0.6), FadeIn(ray), FadeIn(fe), run_time=0.5)
        wob = self.spin(mb, 0.0)
        self.play(fe.animate.move_to(MB + P(0.62, 0.05)), mb.animate.rotate(0.25), run_time=1.5)
        self.at("rust iron", lead=0.2)
        e = fe[1]
        fe.remove(e)
        self.add(e)
        e.set_z_index(22)
        self.play(e.animate(path_arc=1.0).move_to(MB), fe[0].animate.set_fill(RED).set_stroke("#FFB3AA"), run_time=0.45)
        tg = self.put(LBL("without oxygen?", size=28), world=(3.45, -0.42))
        self.play(fe.animate.shift(DOWN * 0.5), VGroup(mb, e).animate.rotate(-0.4), FadeIn(tg), run_time=0.6)
        self.play(fe.animate.move_to(P(2.5, top + 0.05)), VGroup(mb, e).animate.rotate(0.3), run_time=max(0.4, self.narration_s - 0.2 - self.elapsed()), rate_func=linear)
        self.play(FadeOut(fe), run_time=0.3)
        self.finish()


# stages of the world carried from scene to scene
ST9 = dict(iron=1, edots=1, microbes=1, split=1, methane=True, tick=True, readout="before the rise", ph=PH_S08, bubbles=True, mat=1,
           flakes=1, stack=8)
ST12 = dict(ST9, blocks=True, gauge=G_HAIR, ph=PH_GOE0, band=1)
ST13 = dict(ST12, bandlit=1, gauge=G_LOW, pips=5, tag="long", readout="about 2.4 to 2.1 billion years ago", ph=PH_GOE1)
ST14 = dict(ST13, readout="later", ph=PH_LATER)
MB = P(1.9, 0.18)            # the microbe that may rust iron without oxygen (dim sunlit water)


def hero_pip(scene, at, r=0.09, z=21):
    return scene.place(pip(r), 1.0, at, z)


def smooth_path(pts, color=BLUE, sw=3):
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_smoothly([P(*p) for p in pts])
    return m


class S09Takers(WorldScene):
    def construct(self):
        W = self.world(cam=LIFT, **dict(ST9, bfade=1))
        mb = self.place(microbe(0, 3.0), 1.0, MB, 21).rotate(0.15)
        e = Dot(MB, radius=0.034, color=YELLOW).set_z_index(22)
        ray = poly([(1.35, SEA_Y), (1.75, SEA_Y), (2.25, 0.0), (1.55, 0.0)], GOLD, 0.2).set_z_index(15)
        tg = self.put(LBL("without oxygen?", size=28), world=(3.45, -0.42))
        self.add(mb, e, ray, tg)
        W.blocks = W.shore_blocks()
        W.ramp("bfade", 0.0, 1.2)
        # Iron was not the only taker: push in on the sky and the shore; three pips have got past the iron
        starts = [P(-4.0, SEA_Y), P(-1.45, SEA_Y), P(-3.1, SEA_Y)]
        holds = [P(-4.5, 3.1), P(-1.5, 2.3), P(-3.55, 1.8)]
        pp = [hero_pip(self, st_ - UP * 0.4, r=0.13) for st_ in starts]
        self.play(FadeOut(VGroup(mb, e, ray, tg)), run_time=0.3)        # gone before the camera moves, so the tag is never cut
        self.play(FadeIn(W.blocks), self.zoom(TAKECAM), *[FadeIn(p) for p in pp], run_time=1.4)
        self.play(*[p.animate(path_arc=0.5 * (-1) ** k).move_to(h) for k, (p, h) in enumerate(zip(pp, holds))], run_time=1.1)
        pop = lambda q: self.ripple(q, TEXT, r=0.5, sw=6)
        # Volcanic gases: a grey puff with an electron meets the first pip; the dot jumps, the pip is gone, the puff goes dull
        self.at("Volcanic gases", lead=0.5)
        puff = VGroup(Circle(radius=0.3, stroke_width=0, fill_color="#A7ADB9", fill_opacity=0.85), Dot(P(0.24, -0.12), radius=0.06, color=YELLOW))
        self.place(puff, 1.0, CRATER + P(0.45, 0.4), 20.5)
        self.play(FadeIn(puff, scale=0.5), run_time=0.2)
        self.play(puff.animate.move_to(holds[0] + P(-0.45, 0.1)), run_time=0.6)
        self.play(puff[1].animate(path_arc=-1.2).move_to(holds[0]), run_time=0.3)
        self.play(FadeOut(pp[0], scale=0.2), FadeOut(puff[1], scale=0.2), puff[0].animate.set_fill("#4A4F5A", opacity=0.8), pop(holds[0]), run_time=0.4)
        l1 = self.put(LBL("volcanic gas", size=28), world=(-4.55, 3.68))
        # methane: a grey ring rising from the old microbes takes the second
        self.play(FadeIn(l1, shift=UP * 0.05), run_time=max(0.1, self.t_of("methane") - 0.45 - self.elapsed()))
        ring = VGroup(Circle(radius=0.19, stroke_color="#C2C8D2", stroke_width=5), Dot(P(0.16, 0.1), radius=0.06, color=YELLOW))
        self.place(ring, 1.0, P(-1.1, SEA_Y + 0.15), 20.5)
        self.play(FadeIn(ring, shift=UP * 0.2), puff.animate.shift(P(0.3, 0.25)).set_opacity(0.0), run_time=0.25)
        self.remove(puff)
        self.play(ring.animate.move_to(holds[1] + P(0.32, -0.2)), run_time=0.5)
        self.play(ring[1].animate(path_arc=1.2).move_to(holds[1]), run_time=0.25)
        self.play(FadeOut(pp[1], scale=0.2), FadeOut(ring[1], scale=0.2), ring[0].animate.set_stroke("#555A66"), pop(holds[1]), run_time=0.35)
        l2 = self.put(LBL("methane", size=28), world=(-1.5, 2.95))
        # minerals on land: the third pip drifts to the shore; one rock block takes it and goes dull (only iron turns red)
        blk = W.blocks[2]
        tgt = blk[0].get_center() + P(0.34, 0.3)
        self.play(FadeIn(l2, shift=UP * 0.05), pp[2].animate.move_to(tgt), ring.animate.shift(UP * 0.4).set_opacity(0.0), run_time=0.75)
        self.remove(ring)
        self.play(blk[1].animate(path_arc=-1.2).move_to(tgt), run_time=0.25)
        self.play(FadeOut(pp[2], scale=0.2), blk[1].animate.set_opacity(0.0), blk[0].animate.set_fill("#4A4F5A"), pop(tgt), run_time=0.35)
        l3 = self.put(LBL("land minerals", size=28), world=(-3.55, 1.3))
        self.play(FadeIn(l3, shift=UP * 0.05), run_time=0.3)
        self.hold(8.3)
        self.play(FadeOut(VGroup(l1, l2, l3)), self.zoom(FULL), run_time=1.1)
        # As an analogy, picture a bathtub (no bathtub is drawn): the mats are the tap, every taker is a drain
        self.at("As an analogy", lead=0.05)
        tag, tap, drains, ticks, targets = analogy_words()
        self.play(FadeIn(tag, shift=DOWN * 0.15), run_time=0.5)
        self.play(tag.animate.scale(1.06), rate_func=there_and_back, run_time=1.2)
        self.at("mats are the", lead=0.1)
        W.ramp("bglow", 1.0, 0.5)
        self.play(FadeIn(tap, shift=UP * 0.15), self.ripple(P(-2.9, SHELF_Y + 0.25), BLUE, r=0.6), run_time=0.6)
        self.at("Every one of", lead=0.0)
        self.play(FadeIn(drains, shift=UP * 0.15), run_time=0.4)
        for k, q in enumerate(targets):
            b = hero_pip(self, q + P(0.3 * (-1) ** k, -0.34), r=0.09)
            self.play(Create(ticks[k]), FadeIn(b), run_time=0.22)
            self.play(b.animate.move_to(q), run_time=0.14)
            self.play(FadeOut(b, scale=0.2), self.ripple(q, TEXT, r=0.22), run_time=0.2)
        halo = W.g["tube"].copy().set_fill(opacity=0).set_stroke(WHITE, width=9, opacity=0.9).set_z_index(35)
        W.ramp("bglow", 0.4, 0.8)
        self.play(FadeIn(halo), run_time=0.25)
        self.play(FadeOut(halo), run_time=max(0.2, self.narration_s + 0.3 - self.elapsed()))
        self.finish()


class S10Idea(WorldScene):
    def construct(self):
        W = self.world(**dict(ST9, blocks=True, bglow=0.4))
        tag, tap, drains, ticks, targets = analogy_words()
        words = VGroup(tag, tap, drains, ticks)
        self.add(words)
        self.at("hold on to", lead=0.3)
        self.play(FadeOut(words), run_time=0.6)
        # Making oxygen is only half of the story: the mat's stream brightens, everything else dims
        self.at("Making oxygen", lead=0.1)
        W.ramp("dim", 0.5, 0.9)
        W.ramp("bglow", 1.0, 0.9)
        self.at("only half", lead=0.0)
        self.play(self.ripple(P(-2.9, SHELF_Y + 0.2), BLUE, r=0.6), run_time=1.2)
        # The air keeps only the oxygen that nothing else takes first: ONE bubble is followed all the way to the gauge
        # while the line is written with the voice
        self.at("The air keeps", lead=0.45)
        W.ramp("dim", 0.0, 0.6)
        W.ramp("bglow", 0.0, 0.8)
        yb = G_Y0 + 0.12
        path = smooth_path([(-2.6, SHELF_Y + 0.42), (-1.7, -0.05), (0.0, 0.3), (1.9, 0.5), (3.0, SEA_Y), (3.6, 1.35), (4.0, 0.55), (4.2, -0.6), (4.5, -1.25), (G_X, yb)])
        hero = hero_pip(self, P(-2.6, SHELF_Y + 0.42), r=0.11, z=36)
        trail = TracedPath(hero.get_center, stroke_color=BLUE, stroke_width=4, dissipating_time=0.9).set_z_index(35.5)
        self.add(trail, hero)
        self.fly(hero, path, 2.7)
        W.ramp("gauge", G_HAIR, 0.3, delay=2.7)
        gl = guiding_line()
        self.play(FadeIn(gl[0]), Write(gl[1]), run_time=1.3)
        self.play(Write(gl[2]), run_time=1.2)
        self.hold(self.t_of("air") - 0.45 + 2.72)
        halo = W.g["tube"].copy().set_fill(opacity=0).set_stroke(WHITE, width=9, opacity=0.9).set_z_index(35)
        up = Line(P(G_X + 0.62, yb + 0.02), P(G_X + 0.62, yb + 0.5), stroke_color=BLUE, stroke_width=6).add_tip(tip_length=0.2, tip_width=0.2).set_z_index(36)
        self.play(FadeOut(hero, scale=0.3), self.ripple(P(G_X, yb), BLUE, r=0.4, z=36, sw=6), FadeIn(halo), GrowFromEdge(up, DOWN), run_time=0.4)
        self.remove(trail)
        # under the line, a second bubble sets out on the same path and is taken half-way up
        b2 = hero_pip(self, P(-3.1, SHELF_Y + 0.42), r=0.085)
        self.play(FadeOut(halo), FadeOut(up, shift=UP * 0.15), FadeIn(b2), run_time=0.3)
        self.play(b2.animate.move_to(P(-2.5, 0.05)), run_time=0.7)
        fl = self.place(rust_flake(0.13), 1.0, P(-2.5, 0.05), 21)
        self.play(FadeOut(b2, scale=2.2), FadeIn(fl), self.ripple(P(-2.5, 0.05), TEXT, r=0.18), run_time=0.3)
        self.play(fl.animate.shift(DOWN * 0.4), run_time=max(0.2, self.narration_s + 0.35 - self.elapsed()), rate_func=linear)
        self.finish()


class S11When(WorldScene):
    def construct(self):
        W = self.world(**dict(ST9, blocks=True, gauge=G_HAIR))
        gl = guiding_line()
        self.add(gl)
        W.ramp("ph", PH_GOE0, 14.3)
        bar = W.scr["bar"]
        # the scrubber is the subject now: it thickens and rises a little
        self.play(*W.scr_shift(SCR_UP), run_time=0.35)
        self.play(bar.animate.set_stroke(WHITE, width=8), run_time=0.2)
        W.ramp("band", 1.0, 0.8)
        self.play(FadeOut(gl), run_time=0.4)
        # when did the tap turn on? a GREEN span draws back from the playhead
        self.at("turn on", lead=0.1)
        tap = analogy_words()[1]
        W.ramp("bglow", 1.0, 0.4)
        W.ramp("span", 0.25, 1.0, delay=0.3)
        self.play(FadeIn(tap, shift=UP * 0.15), run_time=0.4)
        self.play(tap.animate.scale(1.12), rate_func=there_and_back, run_time=1.0)
        W.ramp("bglow", 0.0, 0.8)
        self.play(FadeOut(tap), run_time=0.4)
        # well before oxygen built up: the span runs on leftward and breaks into fading dashes (no left end)
        self.at("most likely arose", lead=0.0)
        W.ramp("span", 1.0, 3.2)
        self.at("is debated", lead=0.35)
        sd = start_debated()
        self.play(FadeIn(sd, shift=UP * 0.1), run_time=0.45)
        # brief whiffs: three small blips on the gauge, each taken back
        self.at("brief whiffs", lead=0.75)
        wt = plate(T("whiffs?", size=28)).move_to(P(3.3, -1.0)).set_z_index(33)
        for k in range(3):
            W.ramp("gauge", 0.065, 0.2)
            W.ramp("gauge", G_HAIR, 0.3, delay=0.35)
            c = P(-3.2 + 0.5 * k, 2.2 + 0.25 * k)
            puffs = VGroup(*[hero_pip(self, c + P(0.22 * math.cos(2.1 * j + k), 0.2 * math.sin(2.1 * j + k)), r=0.06) for j in range(4)])
            self.play(FadeIn(puffs, scale=0.5), *([FadeIn(wt, shift=LEFT * 0.1)] if k == 0 else []), run_time=0.25)
            self.play(puffs.animate.move_to(TAKER_PTS[0] + P(0.7, -0.2)).scale(0.5).set_opacity(0.0), run_time=0.42)
            self.remove(puffs)
        # before the lasting rise: the playhead arrives at the edge of the still-unlit band
        self.at("lasting rise", lead=0.2)
        self.play(self.ripple(P(PH_GOE0, SCR_Y), TEXT, r=0.22, z=36), bar.animate.set_stroke("#B9BECA", width=5), run_time=0.9)
        self.finish()


def start_debated():
    """The tag over the fading end of the GREEN span, with a clear gap above the dashes (scrubber raised)."""
    return plate(T("start debated", size=28, color=GREEN), pad=0.1, opacity=0.8).move_to(P(-5.0, SCR_Y + SCR_UP + 0.2 + 0.5)).set_z_index(33)


def analogy_group(z=22):
    tag, tap, drains, ticks, targets = analogy_words()
    return VGroup(tag, tap, drains, ticks).set_z_index(z), targets


class S12Goe(WorldScene):
    def construct(self):
        W = self.world(**dict(ST12, span=1, scrdy=SCR_UP))
        sd = start_debated()
        wt = plate(T("whiffs?", size=28)).move_to(P(3.3, -1.0)).set_z_index(33)
        self.add(sd, wt)
        W.ramp("span", 0.0, 0.5)
        self.play(FadeOut(sd), FadeOut(wt), run_time=0.5)
        self.play(*W.scr_shift(-SCR_UP), run_time=0.4)       # the scrubber settles back
        # Then came the change: the band lights
        self.at("the change", lead=0.0)
        W.ramp("bandlit", 1.0, 0.6)
        self.play(self.ripple(P((PH_GOE0 + PH_GOE1) / 2, SCR_Y), BLUE, r=0.45, z=36), run_time=0.9)
        self.hold(2.5)
        W.set_readout("about 2.4 to 2.1 billion years ago", rt=0.5)
        W.ramp("ph", PH_GOE1, 6.4)
        # oxygen rose, wavered, and finally stayed (no cause is drawn: only the outcome)
        self.at("oxygen rose", lead=0.2)
        W.ramp("gauge", 0.11, 1.1)
        W.ramp("pips", 6, 1.1)
        self.at("wavered", lead=0.1)
        for g, n, d in ((0.04, 2, 0.0), (0.095, 6, 0.36), (0.065, 3, 0.72)):
            W.ramp("gauge", g, 0.33, delay=d)
            W.ramp("pips", n, 0.33, delay=d)
        self.at("finally stayed", lead=0.0)
        W.ramp("gauge", G_LOW, 0.6)
        W.ramp("pips", 4, 0.6)
        new = gauge_tag(True).set_z_index(33)
        old = W.tag
        W.unpin(old)
        self.play(FadeOut(old), FadeIn(new), run_time=0.6)
        W.pin(new, placed=True)
        W.tag = new
        # In bathtub terms, more was now arriving than the drains could take: one bubble gets past every drain and stays
        self.at("bathtub terms", lead=0.25)
        words, targets = analogy_group()
        halo = W.g["tube"].copy().set_fill(opacity=0).set_stroke(WHITE, width=9, opacity=0.9).set_z_index(35)
        self.play(FadeIn(words), FadeIn(halo), run_time=0.5)
        self.play(FadeOut(halo), run_time=0.6)
        self.at("more was now", lead=0.2)
        path = smooth_path([(-2.6, SHELF_Y + 0.42), (-0.9, 0.1), (1.3, -0.25), (1.9, SEA_Y), (2.05, 2.2), (0.2, 2.8), (-2.1, 2.5), (-3.7, 2.35), (-3.75, 1.8)])
        hero = hero_pip(self, P(-2.6, SHELF_Y + 0.42), r=0.1, z=23)
        trail = TracedPath(hero.get_center, stroke_color=BLUE, stroke_width=4, dissipating_time=1.0).set_z_index(22.5)
        self.add(trail, hero)
        self.play(MoveAlongPath(hero, path), run_time=3.0, rate_func=linear)
        self.play(self.ripple(hero.get_center(), BLUE, r=0.22), run_time=0.5)
        self.remove(trail)
        # Why the balance tipped then is still debated: the same kind of tag as "when? debated"
        self.at("still debated", lead=1.4)
        W.set_readout("why then? debated", rt=0.4)
        # Geologists call this the Great Oxygenation Event
        self.at("Geologists call", lead=0.0)
        W.set_readout("about 2.4 to 2.1 billion years ago", rt=0.4)
        self.play(FadeOut(words), run_time=0.5)
        name = goe_name().set_z_index(22)
        self.play(FadeIn(name[0]), Write(name[1]), run_time=1.3)
        st = dict(t=W.t)

        def bob(t):
            hero.shift(P(0.0, 0.002 * math.sin(1.4 * t)))
        W.fns.append(bob)
        self.finish()


def far_below():
    """The double arrow between the low level and the 'today' tick, with its tag (screen coordinates)."""
    y0, y1 = G_Y0 + 0.06 + gauge_h(G_LOW) + 0.05, G_TICK - 0.05
    arrow = DoubleArrow(P(4.42, y0), P(4.42, y1), buff=0, stroke_width=4, tip_length=0.2, color=TEXT).set_z_index(34)
    tag = T("far below today", size=28).move_to(P(2.7, (y0 + y1) / 2)).set_z_index(34)
    return arrow, plate(tag).set_z_index(34)


LATE_CAM = (P(0.45, 0.12), 13.1)


class S13After(WorldScene):
    def construct(self):
        W = self.world(**ST13)
        name = goe_name().set_z_index(33)
        self.add(name)
        W.pin(name, placed=True)
        # the tub was nowhere near full: the gap between the level and "today"
        arrow, tag = far_below()
        self.hold(0.6)
        self.play(GrowFromCenter(arrow), run_time=0.8)
        W.pin(arrow, placed=True)
        self.play(self.zoom(LATE_CAM), run_time=1.6)
        self.at("far below", lead=0.5)
        self.hudput(tag.shift(-tag.get_center()), at=(2.7, (G_Y0 + G_TICK) / 2 + 0.3), z=34)
        self.play(FadeIn(tag, shift=RIGHT * 0.15 * W.s), run_time=0.45)
        # for a very long time: the clock creeps on; the level trembles and does not rise; one pip taken, one arrives
        self.at("for a very", lead=0.5)
        W.gauge_shake = 0.6
        W.ramp("ph", PH_LATER, 2.4)
        W.set_readout("later", rt=0.35)
        W.ramp("pips", 4, 0.4)
        gt = self.hudput(goe_tag().shift(-goe_tag().get_center()), at=((PH_GOE0 + PH_GOE1) / 2 + 0.2, -2.98), z=33)
        W.unpin(name)
        W.unpin(gt)
        self.play(ReplacementTransform(name, gt), self.ripple(W.pip_pos(4), TEXT, r=0.2), run_time=0.8)
        W.pin(gt, placed=True)
        W.ramp("pips", 5, 0.5)
        self.play(self.ripple(W.pip_pos(4), BLUE, r=0.2), run_time=max(0.3, self.narration_s + 0.3 - self.elapsed()))
        self.finish()


# ----------------------------------------------------------------------------- the old microbes and oxygen
MC = P(SHELF_CELLS[1], SHELF_Y + 0.11)  # one of the old microbes on the shelf, near the mat
MC_S, MC_K = 0.05, 1.25
MC_CAM = (MC + MC_S * P(-1.6, 0.55) - (MC_S / MC_K) * VIEW, FW * MC_S / MC_K)
SHELFCAM = (P(-1.7, -0.475), 5.6)       # the whole mat and every purple cell on the shelf edge, uncut
SHELFCAM2 = (P(-1.62, -0.46), 5.85)     # where the slow drift of the pause ends
DEEPCAM = (P(1.8, -1.04), 9.2)          # the basin, its mud and deep water; the bare shelf rock at left is where the inset opens
ST15 = dict(ST14, strays=1, quiet=1)


def old_cell(w=4.6, h=2.9):
    """One old microbe close up: a PURPLE outline holding two plain chips, DNA and protein (no structures)."""
    body = RoundedRectangle(width=w, height=h, corner_radius=1.2, stroke_color="#D9CCFF", stroke_width=6, fill_color="#2B2145", fill_opacity=0.97)
    tint = RoundedRectangle(width=w - 0.5, height=h - 0.5, corner_radius=1.0, stroke_width=0, fill_color=PURPLE, fill_opacity=0.16)
    dna = chip("DNA", TEXT, size=30).move_to(P(-0.85, 0.5))
    prot = chip("protein", TEXT, size=30).move_to(P(0.55, -0.5))
    g = VGroup(body, tint, dna, prot)
    g.dna, g.prot = dna, prot
    return g


def crack(mob, s=1.0):
    """A jagged white line across a chip."""
    a, b = mob.get_corner(UL) + P(0.25, 0.06) * s, mob.get_corner(DR) + P(-0.25, -0.06) * s
    pts = [lerp(a, b, u) + P(0, (0.09 if i % 2 else -0.09) * s) for i, u in enumerate(np.linspace(0, 1, 7))]
    return VMobject(stroke_color=WHITE, stroke_width=4 * s).set_points_as_corners(pts)


def microbe_question():
    q1 = plate(T("What happened to the old microbes?", size=34), pad=0.16).move_to(P(-1.4, 3.05))
    q2 = plate(T("A mass die-off?", size=34), pad=0.16).move_to(P(-1.4, 2.32))
    return q1.set_z_index(34), q2.set_z_index(34)


class S14Ask(WorldScene):
    def construct(self):
        W = self.world(cam=LATE_CAM, **ST14)
        arrow, tag = far_below()
        self.hudput(arrow.shift(-arrow.get_center()), at=(4.42, (G_Y0 + 0.11 + gauge_h(G_LOW) + G_TICK - 0.05) / 2), z=34)
        self.hudput(tag.shift(-tag.get_center()), at=(2.7, (G_Y0 + G_TICK) / 2 + 0.3), z=34)
        gt = self.hudput(goe_tag().shift(-goe_tag().get_center()), at=((PH_GOE0 + PH_GOE1) / 2 + 0.2, -2.98), z=33)
        self.add(arrow, tag, gt)
        W.unpin(arrow)
        W.unpin(tag)
        self.play(FadeOut(arrow), FadeOut(tag), run_time=0.4)
        # remember the old microbes: sink to the seabed; the bookmark flares
        self.play(self.zoom(SEABED), run_time=1.0)
        bk = W.book
        self.play(self.ripple(bk.get_center(), TEXT, r=0.4), bk.animate.scale(1.6), run_time=0.35)
        self.play(bk.animate.scale(1 / 1.6), run_time=0.3)
        # push in on the shelf near the mat until ONE purple cell is large; a hero bubble holding one electron drifts in
        MCC = MC + P(0, 0.035)
        pl = lambda m, q, z=20: self.place(m, MC_S, MCC + MC_S * P(*q), z)
        cell = pl(old_cell(), (0, 0), 19)
        W.hole_at, W.hole_r = MCC + MC_S * P(-1.5, 0.25), 0.5
        W.ramp("hole", 1.0, 1.0)
        W.ramp("sheldim", 1.0, 1.2)
        hb = pl(hero_bubble(1.0, filled=1), (0, 0))
        glow, disc, socks, dots = hb
        hb.move_to(MCC + MC_S * P(-10.5, 2.2))
        self.add(hb)
        self.play(FadeIn(cell), self.zoom(MC_CAM), hb.animate.move_to(MCC + MC_S * P(-4.3, 0.45)), run_time=1.5)
        self.play(hb.animate.shift(MC_S * P(0.12, -0.1)), run_time=max(0.2, self.t_of("only partly filled") - 0.2 - self.elapsed()), rate_func=there_and_back)
        # only partly filled: the three empty sockets pulse; the bubble turns jagged and flickers
        self.at("partly", lead=0.2)
        self.play(*[sk[1].animate.set_stroke(WHITE, width=7 * MC_S).scale(1.3) for sk in socks[1:]], run_time=0.3)
        jag = pl(jag_bubble(1.0), (0, 0)).move_to(disc)
        self.play(*[sk[1].animate.set_stroke(TEXT, width=3 * MC_S).scale(1 / 1.3) for sk in socks[1:]], Transform(disc, jag), run_time=0.45)
        st = dict(a=0.0)

        def flick(t):
            a = 0.1 * math.sin(23 * t) + 0.06 * math.sin(41 * t)
            disc.rotate(a - st["a"])
            st["a"] = a
            disc.set_fill(opacity=0.78 + 0.16 * math.sin(29 * t))
        W.fns.append(flick)
        # can damage DNA and proteins: it brushes the cell, and the two chips crack and dim
        self.at("can damage", lead=0.1)
        self.play(hb.animate.shift(MC_S * P(1.15, -0.2)), run_time=0.8, rate_func=rush_into)
        self.at("DNA", lead=0.15)
        c1 = crack(cell.dna, MC_S).set_z_index(21)
        self.play(Create(c1), cell.dna.animate.set_opacity(0.4).rotate(-0.08), self.ripple(cell.dna.get_center(), WHITE, r=0.5), run_time=0.4)
        self.play(hb.animate.shift(MC_S * P(-0.25, 0.1)), run_time=0.5, rate_func=there_and_back)
        self.at("proteins", lead=0.15)
        c2 = crack(cell.prot, MC_S).set_z_index(21)
        self.play(Create(c2), cell.prot.animate.set_opacity(0.4).rotate(0.07), self.ripple(cell.prot.get_center(), WHITE, r=0.5), run_time=0.4)
        self.play(hb.animate.shift(MC_S * P(-0.3, 0.12)), run_time=1.2, rate_func=there_and_back)
        # For many of those microbes, oxygen was toxic: pull back to the shelf; cells near the mat shrink from stray bubbles
        self.at("For many of", lead=0.25)
        W.ramp("strays", 1.0, 1.0)
        W.ramp("hole", 0.0, 2.2)
        W.ramp("sheldim", 0.0, 1.2)
        W.ramp("quiet", 1.0, 1.5)
        self.stop(flick)
        self.play(self.zoom(SHELFCAM), FadeOut(VGroup(cell, c1, c2)), FadeOut(hb), run_time=1.7)
        self.at("what happened", lead=0.2)
        q1, q2 = microbe_question()
        for q in (q1, q2):
            self.hudput(q.shift(-q.get_center()), at=(-1.4, 3.05 if q is q1 else 2.32), z=34)
        self.play(FadeIn(q1[0]), Write(q1[1]), run_time=1.1)
        self.at("mass die", lead=0.2)
        self.play(FadeIn(q2, shift=UP * 0.1 * W.s), run_time=0.5)
        self.finish()


def pinned_question(scene, both=True):
    q1, q2 = microbe_question()
    out = []
    for q, y in ((q1, 3.05), (q2, 2.32)):
        scene.hudput(q.shift(-q.get_center()), at=(-1.4, y), z=34)
        out.append(q)
    return out


class S15Pause(WorldScene):
    def construct(self):
        W = self.world(cam=SHELFCAM, **ST15)
        gt = self.hudput(goe_tag().shift(-goe_tag().get_center()), at=((PH_GOE0 + PH_GOE1) / 2 + 0.2, -2.98), z=33)
        q1, q2 = pinned_question(self)
        self.add(gt, q1, q2)
        W.ramp("nearfade", 0.6, 3.5, delay=0.5)
        self.play(self.zoom(SHELFCAM2), run_time=self.narration_s + 0.35, rate_func=linear)
        self.finish()


GUT_AT, GUT_R = (-4.9, -0.95), 1.4        # the inset sits over the bare rock at lower left (screen coordinates)


def gut_inset():
    """A plain dark tube cross-section packed with the same purple cells, about 40% of the frame height
    (built around ORIGIN, in screen units)."""
    k = GUT_R / 1.15
    disc = Circle(radius=GUT_R, stroke_color=TEXT, stroke_width=4, fill_color="#120C16", fill_opacity=1)
    wall = Circle(radius=0.96 * k, stroke_color="#6A5A66", stroke_width=12)
    rng = random.Random(3)
    cells = VGroup()
    while len(cells) < 15:
        q = P(rng.uniform(-0.7, 0.7), rng.uniform(-0.7, 0.7))
        if np.linalg.norm(q) < 0.7 and all(np.linalg.norm(q * k - m.get_center()) > 0.27 * k for m in cells):
            cells.add(microbe(len(cells) % 3 == 1, 1.85 * k).move_to(q * k).rotate(rng.uniform(-1, 1)))
    lab = ochip("your gut, today", size=28).move_to(P(0, GUT_R + 0.08))
    return VGroup(disc, wall, cells, lab).set_z_index(34), cells


def deep_labels(scene):
    la = scene.put(LBL("anaerobes", size=32, color=PURPLE), world=(1.8, -0.12))
    lm = scene.put(LBL("mud", size=28), world=(0.75, -2.53))
    ld = scene.put(LBL("deep water", size=28), world=(3.4, -0.72))
    return la, lm, ld


class S16Survive(WorldScene):
    def construct(self):
        W = self.world(cam=SHELFCAM2, nearfade=0.6, **ST15)
        gt = self.hudput(goe_tag().shift(-goe_tag().get_center()), at=((PH_GOE0 + PH_GOE1) / 2 + 0.2, -2.98), z=33)
        q1, q2 = pinned_question(self)
        self.add(gt, q1, q2)
        W.unpin(q1)
        self.play(FadeOut(q1), run_time=0.6)
        # the evidence is thin: the tempting answer goes hollow and thins away
        self.at("the evidence", lead=0.3)
        W.unpin(q2)
        self.play(q2[1].animate.set_fill(opacity=0.0).set_stroke(TEXT, width=2.2 * W.s, opacity=1.0), run_time=0.6)
        self.play(q2[1].animate.set_stroke(width=0.3 * W.s, opacity=0.0), q2[0].animate.set_fill(opacity=0.0), run_time=1.0)
        self.remove(q2)
        # drop into mud and deep water: dark, no blue (the bubbles fade at the shelf edge), full of busy purple cells
        W.ramp("nearfade", 1.0, 2.5)
        W.ramp("quiet", 0.8, 2.0)
        W.ramp("bfade", 1.0, 1.0)
        W.ramp("shade", 0.55, 2.2, delay=0.4)
        self.play(self.zoom(DEEPCAM), run_time=1.8)
        la, lm, ld = deep_labels(self)
        self.at("are called", lead=0.0)
        self.play(FadeIn(la, shift=UP * 0.1), run_time=0.5)
        # They clearly survived, in mud, deep water: they pulse and some split in two
        self.at("clearly survived", lead=0.1)
        W.ramp("split2", 1.0, 1.4, delay=0.2)
        self.play(*[self.ripple(P(x, y), PURPLE, r=0.4) for x, y in ((1.2, -2.5), (3.2, -2.5), (2.0, -0.85), (3.8, -0.8))], run_time=1.1)
        self.at("in mud", lead=0.1)
        self.play(FadeIn(lm), run_time=0.3)
        self.at("deep water", lead=0.1)
        self.play(FadeIn(ld), run_time=0.3)
        # the two place labels go before the inset opens (at most six things on screen)
        self.at("thrive there still", lead=0.95)
        self.play(FadeOut(lm), FadeOut(ld), run_time=0.5)
        # They thrive there still, including in your own gut: an inset (the label carries the date)
        inset, cells = gut_inset()
        self.hudput(inset, at=GUT_AT, z=34)
        for k, m in enumerate(cells):
            m._ang = 0.0

        def wob(t):
            for k, m in enumerate(cells):
                a = 0.35 * math.sin(1.6 * t + 1.9 * k)
                m.rotate(a - m._ang)
                m._ang = a
        self.play(GrowFromCenter(inset), run_time=0.7)
        W.fns.append(wob)
        self.finish()


class S17Shadows(WorldScene):
    def construct(self):
        W = self.world(cam=DEEPCAM, nearfade=1, split2=1, **dict(ST15, quiet=0.8, shade=0.55, bfade=1))
        gt = self.hudput(goe_tag().shift(-goe_tag().get_center()), at=((PH_GOE0 + PH_GOE1) / 2 + 0.2, -2.98), z=33)
        la, lm, ld = deep_labels(self)
        inset, cells = gut_inset()
        self.hudput(inset, at=GUT_AT, z=34)
        for m in cells:
            m._ang = 0.0

        def wob(t):
            for k, m in enumerate(cells):
                a = 0.35 * math.sin(1.6 * t + 1.9 * k)
                m.rotate(a - m._ang)
                m._ang = a
        W.fns.append(wob)
        self.add(gt, la, inset)
        self.hold(0.75)
        self.stop(wob)
        W.unpin(inset)
        self.play(FadeOut(inset, scale=0.3), FadeOut(la), run_time=0.5)
        # the oxygen that was left over: pull back; blue only where it was allowed to stay
        W.ramp("mglow", 1.0, 1.4, delay=0.9)
        W.ramp("quiet", 0.0, 1.5)
        self.play(self.zoom(FULL), run_time=1.6)
        # It pushed it into the shadows: a soft dark band settles over mud and deep basin; the purple cells glow inside it
        # (the striped stack is drawn above the band, so the record of what the sea took stays readable)
        self.at("It pushed", lead=0.2)
        W.ramp("shade", 1.0, 1.6)
        self.finish()


ST18 = dict(ST15, nearfade=1, split2=1, shade=1, mglow=1, quiet=0, bfade=1)
BREATH_PIP = P(0.4, 2.75)
# from the mat, out over the red striped stack (the record of what the sea once took), up through the surface, to the pip
BREATH_PATH = [(-2.9, SHELF_Y + 0.42), (-1.9, -0.15), (-0.5, -0.7), (0.9, -1.12), (2.1, -1.08), (2.75, -0.35), (2.35, SEA_Y), (1.75, 1.75), (1.0, 2.45),
               (BREATH_PIP[0], BREATH_PIP[1])]


class S18Close(WorldScene):
    def construct(self):
        W = self.world(**ST18)
        gt = self.hudput(goe_tag().shift(-goe_tag().get_center()), at=((PH_GOE0 + PH_GOE1) / 2 + 0.2, -2.98), z=33)
        self.add(gt)
        # run the clock forward: the playhead moves on while the gauge HOLDS low; then, as a second step, it climbs to "today"
        self.at("run the clock", lead=0.15)
        ph_mid = PH_LATER + 0.8 * (PH_TODAY - PH_LATER)
        W.ramp("ph", ph_mid, max(1.0, self.t_of("rose again") - self.elapsed() - 0.2))
        W.ramp("strays", 0.0, 1.5)
        # Oxygen stayed low for well over a billion years: the label lands and the level stays put
        self.at("stayed low", lead=0.2)
        W.gauge_shake = 0.35
        old = W.readout
        W.unpin(old)
        W.readout = None
        lab = plate(T("low for over a billion years", size=28), pad=0.12).set_z_index(34)
        self.hudput(lab.shift(-lab.get_center()), at=(2.45 - lab.width / 2, -2.42), z=34)
        self.play(FadeOut(old), FadeIn(lab, shift=UP * 0.12 * W.s), run_time=0.5)
        # Then, much later, it rose again: a second, separate step up to "today"
        self.at("rose again", lead=0.35)
        W.gauge_shake = 0.0
        W.ramp("ph", PH_TODAY, 2.0)
        W.ramp("gauge", 1.0, 2.6)
        W.ramp("iron", 0.0, 2.2, delay=0.3)
        W.ramp("flakes", 0.0, 1.8, delay=0.3)
        W.ramp("pips", N_PIPS, 2.4, delay=0.4)
        self.hold(self.t_of("today") + 0.3)
        self.play(W.scr["today"].animate.scale(1.25), run_time=0.3)
        self.play(W.scr["today"].animate.scale(1 / 1.25), run_time=0.25)
        # Take that breath again: rise to the opening framing
        self.at("Take that breath", lead=0.25)
        self.play(FadeOut(lab), self.zoom(TIGHT_SKY), run_time=2.0)
        W.unpin(lab)
        # It began as waste: one pip is traced by a thin blue line back down toward the mat
        self.play(self.zoom((P(0.9, 2.5), 4.9)), run_time=max(0.2, self.t_of("began as waste") - 0.3 - self.elapsed()), rate_func=linear)
        hero = self.place(pip(0.1), 1.0, BREATH_PIP, 23)
        full = smooth_path(BREATH_PATH[::-1], BLUE, 3).set_z_index(22)
        shown = VMobject(stroke_color=BLUE, stroke_width=3).set_z_index(22)
        head = Dot(BREATH_PIP, radius=0.05, color=WHITE).set_z_index(23.5)
        t_a, dur = W.t + 0.5, 4.3

        def trace(t):
            u = ease(clip01((t - t_a) / dur)) if t > t_a else 0.0
            u = max(u, 0.002)
            shown.pointwise_become_partial(full, 0, u)
            head.move_to(full.point_from_proportion(min(u, 0.999)))
        self.add(shown)
        self.play(FadeIn(hero, scale=0.3), self.ripple(BREATH_PIP, BLUE, r=0.35), run_time=0.5)
        self.add(head)
        W.fns.append(trace)
        # what reaches your lungs is what the rest of the planet left behind: pull back to the whole world
        self.at("what reaches", lead=0.1)
        self.play(self.zoom(FULL), run_time=2.2)
        self.at("left behind", lead=0.3)
        self.play(self.ripple(TAKER_PTS[0], TEXT, r=0.3), self.ripple(TAKER_PTS[2], TEXT, r=0.25), self.ripple(P(1.5, BASIN_Y + 0.5), RED, r=0.6, sw=5),
                  run_time=1.0)
        self.finish()


class S19End(WorldScene, EndCard):
    LINE = "The air keeps only the oxygen that nothing else takes first."

    def construct(self):
        W = self.world(**dict(ST18, iron=0, flakes=0, pips=N_PIPS, gauge2=1, ph=PH_TODAY, readout=None, strays=0))
        gt = goe_tag().set_z_index(33)
        hero = self.place(pip(0.1), 1.0, BREATH_PIP, 23)
        full = smooth_path(BREATH_PATH[::-1], BLUE, 3).set_z_index(22)
        self.add(gt, hero, full)
        veil = Rectangle(width=FW + 1, height=FH + 1, stroke_width=0, fill_color="#03040A", fill_opacity=0).set_z_index(40)
        a = Text("The air keeps only the oxygen", font=TITLE_FONT, font_size=44, color=TEXT, t2c={"oxygen": BLUE})
        b = Text("that nothing else takes first.", font=TITLE_FONT, font_size=44, color=TEXT)
        line = VGroup(a, b).arrange(DOWN, buff=0.28)
        sub = T("biochemistrypedia.com", size=28, color=TEAL)
        card = VGroup(line, sub).arrange(DOWN, buff=0.5).set_z_index(41)
        self.add(veil)
        self.play(veil.animate.set_fill(opacity=0.76), FadeOut(full), run_time=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), FadeIn(sub, shift=UP * 0.15), run_time=0.7)      # the sentence and the address arrive together
        self.finish()
