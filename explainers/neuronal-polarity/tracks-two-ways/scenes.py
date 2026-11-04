"""Neuronal polarity, chapter 5: Tracks That Point Two Ways  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept; shared with the other chapters of this lesson, from scenes.old.py)
  YELLOW = the axon (lane outline, axonal cargo)
  BLUE   = dendrites (lane outline, dendritic cargo)
  GREY   = cell body, outlines, an unchosen neurite, "toward the cell body"
  TEAL   = a microtubule (a track), before its direction is coded; also "stable"
  ORANGE = kinesin (new in this chapter; ORANGE was actin in chapter 1)
  PINK   = dynein (new in this chapter; PINK was "fixed for good" in chapter 2)
  GREEN  = a plus-end-out track and its hook (new use in this chapter; taught from the first picture of it)
  PURPLE = a minus-end-out track and its hook (new use in this chapter)
  GOLD   = the open question, the "reading", the rule
  RED    = the gate in the closing teaser (and the red cross on a case that cannot happen)
  TEXT   = labels, the plus sign, cargo outlines
  (series colours not used here: ankyrin G purple is not used for the gate in this chapter, because purple
   already means minus-end-out here)

Geometry is a schematic. A "lane" is a process (axon above, dendrite below) with tracks drawn as arrows
inside it: the arrow head is the plus end. Nothing here is a measurement; the axon-versus-dendrite orientation
mixes (nearly all plus-end-out in the axon, a large fraction each way in vertebrate dendrites) follow the lesson.
Motors that ride the axon hang below its lowest track and motors in the dendrite stand on its top track, so
they sit in the gap between the lanes and never cover a track.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F28DB2"
GOLD_BR = "#F2CF66"
SOMA_FILL = "#262b36"
PLUS_OUT = GREEN
MINUS_OUT = PURPLE
KIN = ORANGE
DYN = PINK

SOMA_C = np.array([-5.85, 0.0, 0.0])
SOMA_R = 0.9

AX6 = [1.95 + 0.24 * i for i in range(6)]          # axon tracks, lowest (next to the gap) first
DE6 = [-1.95 - 0.24 * i for i in range(6)]         # dendrite tracks, top (next to the gap) first
AX_ORI = [True, True, True, True, True, False]    # five plus-end-out, one minus-end-out (the s13 strip)
DE_ORI = [False, True, False, True, True, False]  # mixed: three each way
FLY_DE = [False, False, False, True, False, False]


# ---------------------------------------------------------------- tracks (arrows whose head is the plus end)
class MT(VGroup):
    """A microtubule drawn as a flat-tailed arrow. The head is the plus end, the tail the minus end.
    Everything comes from trackers: c (centre along the axis), half (half length), o (+1 head to the right,
    -1 head to the left, values between flip it), yt (offset across the axis)."""

    def __init__(self, cx=0.0, half=2.0, o=1.0, y=0.0, origin=(0, 0), ang=0.0, h=0.05, H=0.16, hl=0.3,
                 color=TEAL, signs=False, ssize=36, sgap=0.42, auto_color=False):
        super().__init__()
        self.auto_color = auto_color
        self.c = ValueTracker(cx)
        self.half = ValueTracker(half)
        self.o = ValueTracker(o)
        self.yt = ValueTracker(y)
        self.origin = np.array([origin[0], origin[1], 0.0])
        self.ang = ang
        self.h, self.H, self.hl, self.sgap = h, H, hl, sgap
        self.poly = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
        self.add(self.poly)
        self.plus = self.minus = None
        if signs:
            self.plus = T("+", ssize, TEXT, weight=BOLD)
            self.minus = T("−", ssize, GREY, weight=BOLD)
            self.add(self.plus, self.minus)
        self._upd(self)
        self.add_updater(self._upd)

    def _tf(self, x, y):
        ca, sa = math.cos(self.ang), math.sin(self.ang)
        return self.origin + np.array([x * ca - y * sa, x * sa + y * ca, 0.0])

    def _upd(self, _=None):
        c, half, o, y = self.c.get_value(), self.half.get_value(), self.o.get_value(), self.yt.get_value()
        s = 1.0 if o >= 0 else -1.0
        tail, head = c - o * half, c + o * half
        L = max(abs(head - tail), 0.03)
        if abs(head - tail) < 0.03:
            head = tail + s * 0.03
        hl = min(self.hl, 0.6 * L)
        h, H = self.h, self.H
        pts = [(tail, y + h), (head - s * hl, y + h), (head - s * hl, y + H), (head, y),
               (head - s * hl, y - H), (head - s * hl, y - h), (tail, y - h)]
        P = [self._tf(*p) for p in pts]
        self.poly.set_points_as_corners(P + [P[0]])
        if self.auto_color:       # green when the head points out, purple when it points back, blended in between
            self.poly.set_fill(interpolate_color(ManimColor(MINUS_OUT), ManimColor(PLUS_OUT), (max(-1.0, min(1.0, o)) + 1) / 2))
        if self.plus is not None:
            self.plus.move_to(self._tf(head + s * self.sgap, y))
            self.minus.move_to(self._tf(tail - s * self.sgap, y))

    def grow(self):
        """Prepare for a grow-in from the tail; returns the animations (play them with a run_time)."""
        c1, h1, o = self.c.get_value(), self.half.get_value(), self.o.get_value()
        tail = c1 - o * h1
        self.half.set_value(0.02)
        self.c.set_value(tail + o * 0.02)
        self._upd(self)
        return [self.c.animate.set_value(c1), self.half.animate.set_value(h1)]

    def set_signs_opacity(self, v):
        if self.plus is not None:
            self.plus.set_opacity(v)
            self.minus.set_opacity(v)


def lane_track(y, out, thick=False, x0=-3.1, x1=5.9, color=None):
    """A track in a lane: out=True is plus-end-out (head to the right, away from the cell body)."""
    o = 1.0 if out else -1.0
    col = color or (PLUS_OUT if out else MINUS_OUT)
    return MT(cx=(x0 + x1) / 2, half=(x1 - x0) / 2, o=o, y=y, h=0.065 if thick else 0.045,
              H=0.18 if thick else 0.14, hl=0.3, color=col)


def lane_track(y, out, x0=-3.1, x1=5.9, color=None, h=0.05, H=0.11):
    """A track in a lane: out=True is plus-end-out (head to the right, away from the cell body)."""
    o = 1.0 if out else -1.0
    col = color or (PLUS_OUT if out else MINUS_OUT)
    return MT(cx=(x0 + x1) / 2, half=(x1 - x0) / 2, o=o, y=y, h=h, H=H, hl=0.3, color=col)


# ---------------------------------------------------------------- motors
class Motor(VGroup):
    """A cartoon motor on a track: a body, two legs whose feet alternate as it walks, optional cargo, a name.
    flip=1 stands on the track (body above), flip=-1 hangs from it (body below).
    Its position comes from two trackers: xt (along the track) and yt (the y of the track it holds)."""

    def __init__(self, kind, x, ry, sc=1.0, cargo=None, name=True, flip=1, lab_side=1, leg_extra=0.0):
        super().__init__()
        self.kind, self.sc, self.flip, self.lab_side = kind, sc, flip, lab_side
        col = KIN if kind == "kin" else DYN
        self.xt, self.yt = ValueTracker(x), ValueTracker(ry)
        self.w = (0.55 if kind == "kin" else 0.9) * sc
        self.h = 0.36 * sc
        self.leg = 0.38 * sc + leg_extra
        self.stance = (0.11 if kind == "kin" else 0.30) * sc
        self.body = RoundedRectangle(corner_radius=0.09 * sc, width=self.w, height=self.h, fill_color=col,
                                     fill_opacity=1, stroke_color=col, stroke_width=2)
        self.legs = [Line(ORIGIN, RIGHT, color=col, stroke_width=4 * sc) for _ in range(2)]
        self.feet = [Dot(radius=0.05 * sc, color=col) for _ in range(2)]
        parts = [*self.legs, *self.feet, self.body]
        self.cargo = None
        if cargo is not None:
            self.tether = Line(ORIGIN, RIGHT, color=GREY, stroke_width=3)
            self.cargo = Circle(radius=0.2 * sc, fill_color=cargo, fill_opacity=1, stroke_color=TEXT,
                                stroke_width=1.5)
            parts = [self.tether, self.cargo] + parts
        self.label = T("kinesin" if kind == "kin" else "dynein", 26, col) if name else None
        if self.label is not None:
            parts.append(self.label)
        self.add(*parts)
        self._upd(self)
        self.add_updater(self._upd)

    def _upd(self, _=None):
        x, ry, sc, s = self.xt.get_value(), self.yt.get_value(), self.sc, self.flip
        fy = ry + s * 0.05
        by = fy + s * (self.leg + self.h / 2)
        self.body.move_to([x, by, 0])
        ph = math.sin(x * 9.0)
        for i, sg in enumerate((-1, 1)):
            d = 0.12 * sc * (ph if i == 0 else -ph)
            fx = x + sg * self.stance + d
            self.legs[i].put_start_and_end_on([x + sg * self.stance * 0.6, by - s * self.h / 2, 0], [fx, fy, 0])
            self.feet[i].move_to([fx, fy, 0])
        if self.cargo is not None:
            cy = by + s * (self.h / 2 + 0.34 * sc)
            self.cargo.move_to([x, cy, 0])
            self.tether.put_start_and_end_on([x, by + s * self.h / 2, 0], [x, cy - s * 0.2 * sc, 0])
        if self.label is not None:
            off = self.w / 2 + 0.12 + self.label.width / 2
            self.label.move_to([x + self.lab_side * off, by, 0])

    def hide_label(self):
        if self.label is not None:
            self.label.set_opacity(0)
        return self

    def show_label(self):
        return self.label.animate.set_opacity(1)


def walk(scene, motor, x, rt, y=None):
    anims = [motor.xt.animate.set_value(x)]
    if y is not None:
        anims.append(motor.yt.animate.set_value(y))
    scene.play(*anims, run_time=rt, rate_func=linear)


class Sc(SpokenScene):
    """SpokenScene with a shorter lead, so a result appears when it is named and not before."""

    def at(self, phrase, lead=0.08, nth=0):
        return super().at(phrase, lead=lead, nth=nth)


# ---------------------------------------------------------------- the fork: soma, axon lane above, dendrite lane below
def lane_poly(s, col, op=0.10):
    pts = [(-5.2, 0.0), (-3.7, s * 1.6), (6.5, s * 1.6), (6.5, s * 3.8), (-3.7, s * 3.8)]
    p = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=op)
    p.round_corners(0.16)
    return p


def make_soma(c=SOMA_C, r=SOMA_R):
    return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=SOMA_FILL, fill_opacity=1).move_to(c)


def lane_labels():
    """The lane names sit inside each lane, above (axon) or below (dendrite) its tracks, so the gap stays free."""
    return T("axon", 28, YELLOW).move_to([-2.3, 3.55, 0]), T("dendrite", 28, BLUE).move_to([-2.3, -3.55, 0])


def ax_tracks():
    return [lane_track(y, o) for y, o in zip(AX6, AX_ORI)]


def de_tracks(ori=None):
    return [lane_track(y, o) for y, o in zip(DE6, ori or DE_ORI)]


def base(tracks=True, de_ori=None):
    """Everything the fork scenes share. Returns (list of mobjects to add, dict of the parts)."""
    P = dict(soma=make_soma(), ax=lane_poly(1, YELLOW), de=lane_poly(-1, BLUE))
    P["la"], P["ld"] = lane_labels()
    P["axT"] = ax_tracks() if tracks else []
    P["deT"] = de_tracks(de_ori) if tracks else []
    parts = [P["ax"], P["de"], P["soma"], P["la"], P["ld"], *P["axT"], *P["deT"]]
    return parts, P


def kin_ax(x, cargo=None, sc=1.3, **kw):
    """Kinesin in the axon: hangs from the lowest axon track (a plus-end-out one)."""
    return Motor("kin", x, AX6[0], sc=sc, cargo=cargo, flip=-1, **kw)


def dyn_ax(x, cargo=None, sc=1.3, **kw):
    return Motor("dyn", x, AX6[0], sc=sc, cargo=cargo, flip=-1, **kw)


def dyn_de(x, cargo=None, sc=1.3, **kw):
    """Dynein in the dendrite: stands on the top dendrite track (a minus-end-out one)."""
    return Motor("dyn", x, DE6[0], sc=sc, cargo=cargo, flip=1, **kw)


def kin_de(x, cargo=None, sc=1.3, **kw):
    """Kinesin in the dendrite: stands on the first plus-end-out track (its legs cross the one track above)."""
    return Motor("kin", x, DE6[1], sc=sc, cargo=cargo, flip=1, leg_extra=0.15, **kw)


def arr(x0, y0, x1, y1, col=TEXT, sw=6):
    return Arrow([x0, y0, 0], [x1, y1, 0], color=col, buff=0, stroke_width=sw, max_tip_length_to_length_ratio=0.4)


def leader(a, b, col=GREY, sw=3):
    return Line(a, b, color=col, stroke_width=sw)


# ---------------------------------------------------------------- hooks and cross-sections
def ring_hook(cx, cy, r, cw, hook_col=TEXT, ring_col=TEAL):
    ring = Circle(radius=r, stroke_color=ring_col, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([cx, cy, 0])
    ra = r * 0.62
    P0 = np.array([cx, cy + r, 0.0])
    C = P0 + UP * ra
    hook = Arc(radius=ra, start_angle=-PI / 2, angle=(-1.25 * PI if cw else 1.25 * PI), arc_center=C,
               stroke_color=hook_col, stroke_width=5)
    return ring, hook


def make_field(cx, cy, cols, rows, dx, dy, r, flags, colored=False):
    rings, hooks = VGroup(), VGroup()
    k = 0
    for j in range(rows):
        for i in range(cols):
            x = cx + (i - (cols - 1) / 2) * dx
            y = cy + ((rows - 1) / 2 - j) * dy
            col = (PLUS_OUT if flags[k] else MINUS_OUT) if colored else TEXT
            ring, hook = ring_hook(x, y, r, flags[k], hook_col=col)
            rings.add(ring)
            hooks.add(hook)
            k += 1
    return dict(rings=rings, hooks=hooks, group=VGroup(rings, hooks), flags=flags)


def mixed_flags(n, seed):
    rng = np.random.RandomState(seed)
    f = [True] * (n // 2) + [False] * (n - n // 2)
    rng.shuffle(f)
    return f


FIELD_A = dict(cx=0.0, cy=-1.0, cols=8, rows=4, dx=1.4, dy=1.45, r=0.36)
FLAGS_A = mixed_flags(32, 3)
BAND = dict(cx=0.0, cy=-2.2, cols=9, rows=2, dx=1.3, dy=1.25, r=0.27)
BAND_AXON = [True] * 18
BAND_AXON[13] = False                         # one of 18 points back (the lesson: 196 of 200 point out)
BAND_DEND = [True, False, False, True, False, True, True, False, False,
             False, True, True, False, True, False, False, True, True]

# arrows in the long strip: (x_left, x_right) for each, row y, orientation
STRIP_Y = [0.95, 1.4, 1.85, 2.3, 2.75, 3.2]
STRIP_X = [(-4.3, 6.0), (-3.6, 5.6), (-4.4, 6.2), (-3.9, 5.9), (-4.2, 6.1), (-3.5, 5.5)]
STRIP_AX = [True, True, True, False, True, True]
STRIP_DE = [True, False, False, True, False, True]
STRIP_SOMA = np.array([-5.95, 2.05, 0.0])


def strip_arrows(ori):
    out = []
    for y, (xl, xr), o in zip(STRIP_Y, STRIP_X, ori):
        out.append(MT(cx=(xl + xr) / 2, half=(xr - xl) / 2, o=1.0 if o else -1.0, y=y, h=0.04, H=0.13, hl=0.28,
                      color=PLUS_OUT if o else MINUS_OUT, auto_color=True))
    return out


def strip_lane(col):
    return RoundedRectangle(corner_radius=0.2, width=11.8, height=3.0, stroke_color=col, stroke_width=3.5,
                            fill_color=col, fill_opacity=0.10).move_to([0.6, 2.05, 0])


def band_outline(col):
    return RoundedRectangle(corner_radius=0.2, width=13.0, height=2.9, stroke_color=col, stroke_width=3.5,
                            fill_color=col, fill_opacity=0.06).move_to([0, -2.05, 0])


def mini_neuron(c, sc=1.0):
    c = np.array(c, float)
    g = VGroup()
    for deg, L in ((20, 1.0), (110, 0.85), (200, 0.95), (290, 0.9)):
        d = np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg)), 0])
        g.add(Line(c, c + d * L * sc, color=BLUE, stroke_width=10))
    g.add(Line(c, c + np.array([2.0 * sc, 0.55 * sc, 0]), color=YELLOW, stroke_width=14))
    g.add(Circle(radius=0.3 * sc, stroke_color=GREY, stroke_width=3, fill_color=SOMA_FILL, fill_opacity=1).move_to(c))
    return g


def flash(mob, color=GOLD, k=1.05):
    return Indicate(mob, color=color, scale_factor=k)


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "One Axon, Many Dendrites: Neuronal Polarity"
    TITLE = "Tracks That Point Two Ways"


class S01(Sc):
    def construct(self):
        parts, P = base(tracks=False)
        offs = [((-0.33, 0.33, 0), YELLOW), ((0.33, 0.33, 0), BLUE), ((0.33, -0.33, 0), YELLOW),
                ((-0.33, -0.33, 0), BLUE)]
        beads = VGroup(*[Dot(SOMA_C + np.array(p), radius=0.26, color=c) for p, c in offs])
        cl = T("cargo", 28, TEXT).move_to(SOMA_C + DOWN * 1.45)
        qa = T("?", 96, GOLD, weight=BOLD).move_to([-2.9, 2.6, 0])
        qd = T("?", 96, GOLD, weight=BOLD).move_to([-2.9, -2.6, 0])
        self.at("once an axon")
        self.play(FadeIn(P["soma"]), FadeIn(P["ax"]), FadeIn(P["de"]), run_time=0.6)
        self.at("axon is")
        self.play(FadeIn(P["la"]), FadeIn(P["ld"]), run_time=0.4)
        self.at("how does cargo")
        self.play(LaggedStart(*[GrowFromCenter(b) for b in beads], lag_ratio=0.2), FadeIn(cl), run_time=0.9)
        self.at("which branch")
        self.play(FadeIn(qa, scale=0.6), FadeIn(qd, scale=0.6), run_time=0.6)
        self.play(flash(P["ax"], YELLOW, 1.02), flash(P["de"], BLUE, 1.02), run_time=0.6)
        self.finish()


class S02(Sc):
    def construct(self):
        parts, P = base(tracks=False)
        self.add(*parts)
        trs = [MT(cx=1.4, half=4.5, o=1, y=y, h=0.06, H=0.06, hl=0.01, color=TEAL) for y in AX6]
        anims = []
        for t in trs:
            anims += t.grow()
        self.add(*trs)
        lab = T("stable microtubules", 30, TEAL).move_to([0.3, 0.3, 0])
        self.play(*anims, FadeIn(lab), run_time=0.9, rate_func=smooth)
        self.at("choosing the axon")
        ch = T("choosing", 30, GOLD_BR, weight=BOLD).move_to([4.7, 0.95, 0])
        chl = leader([5.0, 1.2, 0], [5.4, 1.7, 0], GOLD_BR)
        self.play(FadeIn(ch), Create(chl), flash(P["ax"], YELLOW, 1.02), run_time=0.7)
        self.at("holding it")
        ho = T("holding", 30, GOLD_BR, weight=BOLD).move_to([-1.6, 0.95, 0])
        hol = leader([-1.6, 1.2, 0], [-1.6, 1.7, 0], GOLD_BR)
        self.play(FadeIn(ho), Create(hol), *[flash(t, TEAL, 1.03) for t in trs], run_time=0.7)
        self.finish()


class S03(Sc):
    def construct(self):
        # Start large; the guides mark the original ends so both growth rates can be read.
        mt = MT(cx=0.0, half=3.1, o=1, y=0.2, h=0.3, H=0.75, hl=1.1,
                color=TEAL, signs=True, ssize=52, sgap=0.55)
        guides = VGroup(*[DashedLine([x, -0.9, 0], [x, 1.3, 0], color=GREY,
                                    stroke_width=3, dash_length=0.12) for x in (-3.1, 3.1)])
        pl = T("plus end: fast-growing", 34, TEXT).move_to([3.5, 1.85, 0])
        ml = T("minus end: slower", 34, GREY).move_to([-3.6, -1.5, 0])
        self.add(mt, guides, pl, ml)
        self.at("fast growing")
        # Right end advances 2.1 units; left end advances only 0.5.
        self.play(mt.c.animate.set_value(0.8), mt.half.animate.set_value(4.4),
                  run_time=2.0, rate_func=linear)
        self.finish()


def s04_tracks():
    A = MT(cx=0.1, half=5.1, o=1, y=1.6, h=0.13, H=0.34, hl=0.6, color=TEAL, signs=True, ssize=48, sgap=0.6)
    B = MT(cx=0.1, half=5.1, o=1, y=-1.7, h=0.13, H=0.34, hl=0.6, color=TEAL, signs=True, ssize=48, sgap=0.6)
    return A, B


class S04(Sc):
    def construct(self):
        A, B = s04_tracks()
        kin = Motor("kin", -3.0, 1.6, sc=2.2).hide_label()
        dyn = Motor("dyn", 3.4, -1.7, sc=2.2).hide_label()
        tk = VGroup(T("toward +", 30, TEXT).move_to([0.0, 0.9, 0]), arr(-1.3, 0.45, 1.3, 0.45, TEXT))
        td = VGroup(T("toward −", 30, TEXT).move_to([0.0, -2.75, 0]), arr(1.3, -3.25, -1.3, -3.25, TEXT))
        self.add(A, B)
        self.at("motor proteins")
        self.play(FadeIn(kin), FadeIn(dyn), run_time=0.6)
        self.at("that direction")
        self.play(flash(A.plus, TEXT, 1.4), flash(B.plus, TEXT, 1.4), flash(A.minus, GREY, 1.4),
                  flash(B.minus, GREY, 1.4), run_time=0.7)
        self.at("most kinesins")
        self.play(kin.show_label(), FadeIn(tk), run_time=0.2)
        self.at("kinesins walk")
        walk(self, kin, 4.0, 1.9)
        self.at("walks toward minus")
        self.play(dyn.show_label(), FadeIn(td), run_time=0.3)
        walk(self, dyn, -3.6, 1.6)
        self.finish()


# ---- the process view (s05 to s07)
def process_view():
    soma = make_soma(SOMA_C, 0.9)
    proc = RoundedRectangle(corner_radius=0.3, width=11.6, height=4.6, stroke_color=GREY, stroke_width=3.5,
                            fill_color=GREY, fill_opacity=0.08).move_to([0.85, 0, 0])
    return soma, proc


def proc_track(o=1.0):
    return MT(cx=0.5, half=4.5, o=o, y=0.0, h=0.20, H=0.46, hl=0.65, color=PLUS_OUT, signs=True, ssize=44,
              sgap=0.5, auto_color=True)


def cb_label():
    return T("cell body", 26, GREY).move_to([-5.9, -1.5, 0])


def chip_out(minus=False):
    return chip("minus-end-out" if minus else "plus-end-out", MINUS_OUT if minus else PLUS_OUT, 26,
                pad=0.18).move_to([4.4, 3.42, 0])


def away_arrow():
    return VGroup(arr(-3.6, 2.65, 1.2, 2.65, TEXT, sw=12), T("away from cell body", 28, TEXT).move_to([-1.2, 3.15, 0]))


def toward_arrow():
    return VGroup(arr(1.2, -2.65, -3.6, -2.65, GREY, sw=12), T("toward cell body", 28, GREY).move_to([-1.2, -3.15, 0]))


class S05(Sc):
    def construct(self):
        soma, proc = process_view()
        cb = cb_label()
        mt = proc_track()
        mt.set_signs_opacity(0)
        anims = mt.grow()
        chip_ = chip_out()
        away = away_arrow()
        self.at("picture a")
        self.play(FadeIn(soma), FadeIn(proc), run_time=0.6)
        self.at("plus end out track")
        self.add(mt)
        self.play(*anims, run_time=1.0)
        self.play(mt.plus.animate.set_opacity(1), mt.minus.animate.set_opacity(1), FadeIn(chip_), run_time=0.3)
        self.at("plus end points")
        self.play(Indicate(mt.plus, color=TEXT, scale_factor=1.5), run_time=0.7)
        self.at("away from")
        self.play(GrowArrow(away[0]), FadeIn(away[1]), run_time=0.7)
        self.at("cell body")
        self.play(FadeIn(cb), flash(soma, GREY, 1.12), run_time=0.5)
        self.finish()


def s06_motors():
    kin = Motor("kin", -3.0, 0.0, sc=3.1, flip=1, lab_side=-1).hide_label()
    dyn = Motor("dyn", 3.6, 0.0, sc=3.1, flip=-1, lab_side=-1)
    return kin, dyn


class S06(Sc):
    def construct(self):
        soma, proc = process_view()
        mt = proc_track()
        self.add(proc, soma, cb_label(), mt, chip_out(), away_arrow())
        kin, dyn = s06_motors()
        toward = toward_arrow()
        self.play(FadeIn(kin), FadeIn(dyn), run_time=0.4)
        self.at("walks outward")
        self.play(kin.show_label(), run_time=0.2)
        walk(self, kin, 4.2, 1.4)
        self.at("walks home")
        self.play(dyn.show_label(), run_time=0.2)
        self.play(AnimationGroup(dyn.xt.animate(run_time=1.7, rate_func=linear).set_value(-3.2),
                                 Succession(Wait(0.6), AnimationGroup(GrowArrow(toward[0]), FadeIn(toward[1]),
                                                                      run_time=0.5))))
        self.finish()


class S07(Sc):
    def construct(self):
        soma, proc = process_view()
        mt = proc_track()
        chip1 = chip_out()
        chip2 = chip_out(minus=True)
        kin = Motor("kin", 4.2, 0.0, sc=3.1, flip=1, lab_side=-1)
        dyn = Motor("dyn", -3.2, 0.0, sc=3.1, flip=-1, lab_side=-1)
        self.add(proc, soma, cb_label(), mt, chip1, away_arrow(), toward_arrow(), kin, dyn)
        self.at("minus end out", lead=0.4)
        self.play(mt.plus.animate.set_opacity(0), mt.minus.animate.set_opacity(0), run_time=0.15)
        self.play(mt.o.animate.set_value(-1.0), ReplacementTransform(chip1, chip2), run_time=0.5)
        self.play(mt.plus.animate.set_opacity(1), mt.minus.animate.set_opacity(1), run_time=0.15)
        self.at("it is the reverse", lead=0.5)
        self.play(kin.xt.animate.set_value(-3.0), dyn.xt.animate.set_value(3.6), run_time=1.15, rate_func=linear)
        self.finish()


class S08(Sc):
    def construct(self):
        parts, P = base(tracks=False)
        dl_a = DashedLine([-3.1, 2.4, 0], [5.0, 2.4, 0], color=TEAL, stroke_width=5, dash_length=0.18)
        dl_d = DashedLine([-3.1, -2.4, 0], [5.0, -2.4, 0], color=TEAL, stroke_width=5, dash_length=0.18)
        qa = T("?", 90, GOLD, weight=BOLD).move_to([5.75, 2.4, 0])
        qd = T("?", 90, GOLD, weight=BOLD).move_to([5.75, -2.4, 0])
        self.play(*[FadeIn(p) for p in parts], run_time=0.3)
        self.at("which way")
        self.play(Create(dl_a), Create(dl_d), run_time=0.5)
        self.at("tracks point")
        self.play(FadeIn(qa, scale=0.5), FadeIn(qd, scale=0.5), run_time=0.5)
        self.at("real neuron")
        self.play(flash(qa, GOLD, 1.25), flash(qd, GOLD, 1.25), run_time=0.6)
        self.finish()


class S09(Sc):
    def construct(self):
        yr = T("1988", 90, GOLD, font=TITLE_FONT).move_to([3.4, 2.4, 0])
        who = T("Baas and colleagues", 40, TEXT).move_to([3.4, 1.15, 0])
        hk = chip("hook decoration", TEAL, 36).move_to([3.4, -0.1, 0])
        dish = Ellipse(width=6.8, height=5.8, stroke_color=GREY, stroke_width=4).move_to([-3.4, 0.1, 0])
        neuron = mini_neuron([-4.9, -0.1, 0.0], sc=1.8)
        cap = T("cultured rat hippocampal neurons", 30, TEXT).move_to([-3.4, -3.4, 0])
        self.at("1988", lead=0.5)
        self.play(Create(dish), FadeIn(neuron), FadeIn(yr, shift=UP * 0.15), run_time=0.9)
        self.at("peter")
        self.play(FadeIn(who, shift=UP * 0.1), run_time=0.6)
        self.at("hook decoration")
        self.play(FadeIn(hk, scale=0.8), run_time=0.6)
        self.at("cultured rat")
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---- the hook legend (shared by s10 and s11)
LEG_Y = 2.65
LEG_L, LEG_R = -5.9, 0.6


def legend_rings(white=True):
    a = ring_hook(LEG_L, LEG_Y, 0.38, True, hook_col=TEXT)
    b = ring_hook(LEG_R, LEG_Y, 0.38, False, hook_col=TEXT)
    return a, b


def legend_side():
    """Side-view arrow and name for each hook (the colour pair is the key)."""
    ga = MT(cx=-4.85, half=0.45, o=1, y=LEG_Y, h=0.06, H=0.2, hl=0.34, color=PLUS_OUT)
    gb = MT(cx=1.45, half=0.45, o=-1, y=LEG_Y, h=0.06, H=0.2, hl=0.34, color=MINUS_OUT)
    ta = T("plus-end-out", 30, PLUS_OUT).move_to([-2.7, LEG_Y, 0])
    tb = T("minus-end-out", 30, MINUS_OUT).move_to([3.5, LEG_Y, 0])
    return ga, gb, ta, tb


class S10(Sc):
    def construct(self):
        ring, hook = ring_hook(0, -0.1, 1.35, True)
        under = T("microtubule, cut across", 30, TEAL).move_to([0, -2.2, 0])
        self.add(ring)
        self.play(GrowFromCenter(ring), FadeIn(under), run_time=0.6)
        self.at("adds curved sheets")
        self.play(Create(hook), run_time=1.0)
        hm = hook.point_from_proportion(0.97)
        sheet = T("curved sheet", 30, TEXT).move_to([3.2, 1.9, 0])
        sl = leader([1.75, 1.9, 0], hm + np.array([0.06, 0.02, 0]), TEXT)
        self.play(FadeIn(sheet), Create(sl), run_time=0.5)
        self.at("wall")
        wall = T("wall", 30, TEAL).move_to([-3.1, -0.1, 0])
        wl = leader([-2.55, -0.1, 0], [-1.37, -0.1, 0], TEAL)
        self.play(FadeIn(wall), Create(wl), flash(ring, TEAL, 1.05), run_time=0.7)
        F = make_field(flags=FLAGS_A, **FIELD_A)
        k = FLAGS_A.index(True, 11)
        rest_r = VGroup(*[m for i, m in enumerate(F["rings"]) if i != k])
        rest_h = VGroup(*[m for i, m in enumerate(F["hooks"]) if i != k])
        head = T("cross section", 34, TEXT).move_to([0, 3.15, 0])
        self.at("cross section")
        self.play(FadeOut(sheet), FadeOut(sl), FadeOut(wall), FadeOut(wl), FadeOut(under),
                  ReplacementTransform(ring, F["rings"][k]), ReplacementTransform(hook, F["hooks"][k]),
                  FadeIn(rest_r), FadeIn(rest_h), FadeIn(head), run_time=1.1)
        self.at("hooks curve")
        self.wait(0.1)
        la, lb = legend_rings()
        self.at("one way")
        cw = [h for h, f in zip(F["hooks"], FLAGS_A) if f]
        ccw = [h for h, f in zip(F["hooks"], FLAGS_A) if not f]
        self.play(FadeOut(head), FadeIn(VGroup(*la)), *[Indicate(h, color=GOLD, scale_factor=1.35) for h in cw],
                  run_time=0.5)
        self.at("or the other")
        self.play(FadeIn(VGroup(*lb)), *[Indicate(h, color=GOLD, scale_factor=1.35) for h in ccw], run_time=0.8)
        self.finish()


class S11(Sc):
    def construct(self):
        F = make_field(flags=FLAGS_A, **FIELD_A)
        la, lb = legend_rings()
        self.add(F["group"], *la, *lb)
        ga, gb, ta, tb = legend_side()
        self.play(FadeIn(ga), FadeIn(ta), FadeIn(gb), FadeIn(tb), run_time=0.6)
        self.at("microtubule")
        self.play(AnimationGroup(*[h.animate.set_color(PLUS_OUT if f else MINUS_OUT)
                                   for h, f in zip(F["hooks"], FLAGS_A)], lag_ratio=0.015),
                  la[1].animate.set_color(PLUS_OUT), lb[1].animate.set_color(MINUS_OUT), run_time=0.8)
        self.finish()


class S12(Sc):
    def construct(self):
        lane = strip_lane(YELLOW)
        soma = make_soma(STRIP_SOMA, 0.55)
        arrows = strip_arrows(STRIP_AX)
        out = band_outline(YELLOW)
        F = make_field(flags=BAND_AXON, colored=True, **BAND)
        who = T("axon", 32, YELLOW, weight=BOLD).move_to([-6.0, 0.0, 0])
        lab = T("nearly all", 34, TEXT).move_to([-3.6, 0.0, 0])
        away_a = arr(-2.2, 0.0, -0.3, 0.0, TEXT)
        away_t = T("away from the cell body", 28, TEXT).move_to([2.0, 0.0, 0])
        self.at("in the axon")
        self.play(FadeIn(lane), FadeIn(soma), FadeIn(out), FadeIn(who), run_time=0.5)
        self.at("nearly all")
        self.play(FadeIn(F["group"]), FadeIn(lab), run_time=0.4)
        self.at("microtubules point")
        anims = []
        for a in arrows:
            anims += a.grow()
        self.add(*arrows)
        self.play(*anims, run_time=1.0)
        self.at("away from the")
        self.play(GrowArrow(away_a), FadeIn(away_t), run_time=0.6)
        self.finish()


class S13(Sc):
    def construct(self):
        lane = strip_lane(YELLOW)
        soma = make_soma(STRIP_SOMA, 0.55)
        arrows = strip_arrows(STRIP_AX)
        out = band_outline(YELLOW)
        FA = make_field(flags=BAND_AXON, colored=True, **BAND)
        FD = make_field(flags=BAND_DEND, colored=True, **BAND)
        who = T("axon", 32, YELLOW, weight=BOLD).move_to([-6.0, 0.0, 0])
        lab = T("nearly all", 34, TEXT).move_to([-3.6, 0.0, 0])
        away_a = arr(-2.2, 0.0, -0.3, 0.0, TEXT)
        away_t = T("away from the cell body", 28, TEXT).move_to([2.0, 0.0, 0])
        self.add(lane, soma, out, FA["group"], *arrows, who, lab, away_a, away_t)
        mixed = T("mixed", 34, TEXT).move_to([-3.6, 0.0, 0])
        dend = T("dendrite", 32, BLUE, weight=BOLD).move_to([-6.0, 0.0, 0])
        self.at("dendrites")
        self.play(FadeOut(away_a), FadeOut(away_t), FadeOut(lab), ReplacementTransform(who, dend),
                  lane.animate.set_color(BLUE), out.animate.set_color(BLUE), run_time=0.7)
        self.at("is mixed")
        anims = [Transform(a, b) for a, b in zip(FA["hooks"], FD["hooks"])]
        for a, o in zip(arrows, STRIP_DE):
            anims.append(a.o.animate.set_value(1.0 if o else -1.0))
        self.play(*anims, FadeIn(mixed), run_time=0.9)
        self.at("a large fraction")
        self.play(*[flash(a, MINUS_OUT, 1.02) for a, o in zip(arrows, STRIP_DE) if not o], run_time=0.7)
        self.at("each way")
        la = arr(-0.6, 0.0, 0.8, 0.0, PLUS_OUT)
        lb = arr(-0.8, 0.0, -2.2, 0.0, MINUS_OUT)
        both = T("a large fraction each way", 28, TEXT).move_to([3.4, 0.0, 0])
        self.play(GrowArrow(la), GrowArrow(lb), FadeIn(both), run_time=0.6)
        self.finish()


# ---- the question (s14, s15): the s13 track sets stay in both lanes
QTXT = "Which motor can carry\ncargo outward into\na dendrite, but hardly\never into the axon?"


def s14_parts():
    parts, P = base(tracks=True)
    # Open the fork vertically while retaining exactly the same six tracks in each lane.
    for key, sign, col in (("ax", 1, YELLOW), ("de", -1, BLUE)):
        P[key].become(Polygon(*[[-5.2, 0, 0], [-3.7, sign * 2.1, 0], [6.5, sign * 2.1, 0],
                                [6.5, sign * 3.8, 0], [-3.7, sign * 3.8, 0]],
                             stroke_color=col, stroke_width=3.5, fill_color=col,
                             fill_opacity=0.10).round_corners(0.16))
    for i, t in enumerate(P["axT"]):
        t.yt.set_value(2.25 + 0.2 * i)
        t._upd()
    for i, t in enumerate(P["deT"]):
        t.yt.set_value(-2.25 - 0.2 * i)
        t._upd()
    # The motors wait at the fork itself; no disconnected track stubs.
    kin = Motor("kin", -3.1, -1.65, sc=2.7, cargo=YELLOW, name=False)
    dyn = Motor("dyn", -0.2, -1.65, sc=2.7, cargo=BLUE, name=False)
    kl = T("kinesin", 28, KIN).move_to([-3.1, -1.93, 0])
    dl = T("dynein", 28, DYN).move_to([-0.2, -1.93, 0])
    q = T(QTXT, 28, GOLD_BR).move_to([4.6, 0.55, 0])
    return parts, P, [kl, dl, kin, dyn], q


class S14(Sc):
    def construct(self):
        parts, P, mot, q = s14_parts()
        self.play(*[FadeIn(p) for p in parts], run_time=0.3)
        self.at("which motor can carry")
        self.play(*[FadeIn(m) for m in mot], run_time=0.7)
        self.at("outward into a dendrite")
        self.play(FadeIn(q), flash(P["de"], BLUE, 1.02), run_time=0.8)
        self.at("but hardly ever")
        self.play(flash(P["ax"], YELLOW, 1.02), run_time=0.6)
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        parts, P, mot, q = s14_parts()
        self.add(*parts, *mot, q)
        think = T("THINK", 36, GOLD_BR).move_to([4.5, -0.5, 0])
        w = ValueTracker(3.4)
        bar = Rectangle(width=3.4, height=0.44, fill_color=GOLD_BR, fill_opacity=1, stroke_width=0)

        def upd(b):
            b.stretch_to_fit_width(max(w.get_value(), 0.02))
            b.move_to([2.8 + max(w.get_value(), 0.02) / 2, -0.95, 0])
        bar.add_updater(upd)
        upd(bar)
        self.add(think, bar)
        self.play(w.animate.set_value(0.02), run_time=4.7, rate_func=linear)
        self.finish()


class S16(Sc):
    def construct(self):
        parts, P, mot, q = s14_parts()
        kl, dl, kin, dyn = mot
        self.add(*parts, *mot, q)
        self.play(FadeOut(q), FadeOut(kin), FadeOut(kl), FadeOut(dl), flash(dyn, DYN, 1.1), run_time=0.7)
        answer = dyn_de(-2.9, cargo=BLUE)
        answer.yt.set_value(DE6[0] - 0.3)
        answer._upd()
        self.play(ReplacementTransform(dyn, answer), run_time=0.7)
        dyn = answer
        self.at("it can carry")
        walk(self, dyn, 1.2, 1.9)
        self.at("only on")
        mchip = T("minus-end-out", 28, MINUS_OUT, weight=BOLD).move_to([5.3, -0.45, 0])
        ml = leader([5.3, -0.75, 0], [5.3, -2.14, 0], MINUS_OUT)
        self.play(FadeIn(mchip), Create(ml), run_time=0.4)
        self.at("minus end out tracks")
        self.play(flash(P["deT"][0], MINUS_OUT, 1.05), run_time=0.7)
        self.finish()


class S17(Sc):
    def construct(self):
        parts, P = base(tracks=True)
        dyn = dyn_de(1.2, cargo=BLUE)
        mchip = T("minus-end-out", 28, MINUS_OUT, weight=BOLD).move_to([5.3, -0.45, 0])
        ml = leader([5.3, -0.75, 0], [5.3, -1.84, 0], MINUS_OUT)
        self.add(*parts, dyn, mchip, ml)
        self.play(FadeOut(dyn), FadeOut(mchip), FadeOut(ml), run_time=0.5)
        self.at("those tracks")
        purple = [t for t, o in zip(P["deT"], DE_ORI) if not o]
        self.play(*[flash(t, MINUS_OUT, 1.04) for t in purple], run_time=0.9)
        self.at("the axon has")
        # An explicit green track carries dynein home, with its feet on that track.
        rail = MT(cx=1.6, half=4.0, o=1, y=0.75, color=PLUS_OUT, h=0.09, H=0.20)
        d2 = Motor("dyn", 4.2, 0.75, sc=1.3, flip=-1, lab_side=-1)
        tw = VGroup(T("toward cell body", 28, GREY).move_to([1.4, -0.85, 0]),
                    arr(2.8, -1.25, 0.0, -1.25, GREY, sw=9))
        tag = chip("almost none", MINUS_OUT, 30, pad=0.12).move_to([3.9, 3.52, 0])
        tag_line = leader([3.9, 3.2, 0], [3.9, AX6[5], 0], MINUS_OUT, sw=4)
        self.play(FadeIn(rail), FadeIn(d2), FadeIn(tw), FadeIn(tag), Create(tag_line), run_time=0.25)
        self.play(d2.xt.animate.set_value(-0.6), run_time=1.65, rate_func=linear)
        self.finish()


class S18(Sc):
    def construct(self):
        parts, P = base(tracks=True)
        k1 = kin_ax(-2.8)
        k2 = kin_de(-2.8)
        self.add(*parts)
        self.play(FadeIn(k1), FadeIn(k2), run_time=0.4)
        self.at("walk outward")
        self.play(k1.xt.animate.set_value(3.4), k2.xt.animate.set_value(3.4), run_time=1.9, rate_func=linear)
        self.at("plus")
        greens = [t for t, o in zip(P["axT"], AX_ORI) if o] + [t for t, o in zip(P["deT"], DE_ORI) if o]
        self.play(*[flash(t, PLUS_OUT, 1.04) for t in greens], run_time=0.8)
        self.finish()


def seated_axon(parts, P, x, cargo=YELLOW, name=True):
    """Expose a top green rail so an upright motor has room for its cargo."""
    for t, y in zip(P["axT"], (1.8, 1.62, 1.44, 1.26, 1.08, 0.90)):
        t.yt.set_value(y)
        t._upd()
    # Widen the axon lane downward to contain the entire unchanged 5:1 track set.
    P["ax"].become(Polygon(*[[-5.2, 0, 0], [-3.7, 0.65, 0], [6.5, 0.65, 0],
                              [6.5, 3.8, 0], [-3.7, 3.8, 0]], stroke_color=YELLOW,
                           stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.10).round_corners(0.16))
    return Motor("kin", x, 1.8, sc=1.25, cargo=cargo, flip=1, name=name)


class S19(Sc):
    def construct(self):
        parts, P = base(tracks=True)
        kin = seated_axon(parts, P, -4.5)
        kin.yt.set_value(0.0)
        kin._upd()
        to_ax = DashedLine([-4.5, 0.0, 0], [-2.8, 1.8, 0], color=GOLD_BR, stroke_width=7, dash_length=0.18)
        to_de = DashedLine([-4.5, 0.0, 0], [-2.8, -1.95, 0], color=GOLD_BR, stroke_width=7, dash_length=0.18)
        pref = T("prefers stable plus-end-out tracks", 28, TEXT).move_to([2.4, 0.1, 0])
        bundle = RoundedRectangle(corner_radius=0.12, width=9.5, height=1.35, stroke_color=TEAL, stroke_width=4,
                                  fill_color=TEAL, fill_opacity=0.07).move_to([1.4, 1.35, 0])
        stable = T("stable", 28, TEAL, weight=BOLD).move_to([1.4, 3.55, 0])
        self.add(*parts)
        self.at("kinesin")
        self.play(FadeIn(kin), Create(to_ax), Create(to_de), run_time=0.7)
        self.at("prefers")
        self.play(FadeIn(pref), run_time=0.25)
        self.at("stable")
        self.play(Create(bundle), FadeIn(stable), run_time=0.7)
        self.at("plus end out")
        self.play(*[flash(t, PLUS_OUT, 1.04) for t, o in zip(P["axT"], AX_ORI) if o], run_time=0.7)
        self.at("can be steered")
        self.play(FadeOut(to_de), to_ax.animate.set_stroke(width=9),
                  kin.xt.animate.set_value(-2.8), kin.yt.animate.set_value(1.8), run_time=0.7)
        self.play(FadeOut(to_ax), run_time=0.15)
        walk(self, kin, 2.6, 1.3)
        self.finish()


class S20(Sc):
    def construct(self):
        rows = [(0.25, True), (-2.95, False)]
        banner = T("The tracks limit the motors", 34, GOLD_BR, font=TITLE_FONT).move_to([0, 3.55, 0])
        tracks, chips = [], []
        for ry, o in rows:
            tracks.append(MT(cx=0.1, half=6.3, o=1.0 if o else -1.0, y=ry, h=0.08, H=0.22, hl=0.45,
                             color=PLUS_OUT if o else MINUS_OUT))
            chips.append(T("plus-end-out" if o else "minus-end-out", 28, PLUS_OUT if o else MINUS_OUT,
                           weight=BOLD).move_to([-4.7, ry - 0.42, 0]))
        motors, arrows, ghosts = [], [], []
        for (ry, o), tr in zip(rows, tracks):
            for kind, x in (("kin", -2.9), ("dyn", 3.2)):
                m = Motor(kind, x, ry, sc=1.6, lab_side=-1)
                motors.append(m)
                out_ok = (kind == "kin") == o            # kinesin goes out on plus-end-out, dynein on minus-end-out
                if out_ok:
                    arrows.append(VGroup(arr(x - 1.0, ry + 1.72, x + 1.0, ry + 1.72, PLUS_OUT),
                                         T("outward", 28, PLUS_OUT).move_to([x, ry + 2.16, 0])))
                else:
                    arrows.append(VGroup(arr(x + 1.0, ry + 1.72, x - 1.0, ry + 1.72, GREY),
                                         T("toward cell body", 28, GREY).move_to([x, ry + 2.16, 0])))
                    gx = x + 2.0
                    g = arr(gx - 0.85, ry + 0.7, gx + 0.85, ry + 0.7, PLUS_OUT, sw=10)
                    cross = VGroup(Line([gx - 0.4, ry + 1.1, 0], [gx + 0.4, ry + 0.3, 0], color=RED, stroke_width=10),
                                   Line([gx - 0.4, ry + 0.3, 0], [gx + 0.4, ry + 1.1, 0], color=RED, stroke_width=10))
                    cannot = T("cannot", 28, RED, weight=BOLD).move_to([gx, ry + 1.35, 0])
                    ghosts.append(VGroup(g, cross, cannot))
        a1, a2 = tracks[0].grow(), tracks[1].grow()
        self.add(*tracks)
        self.play(*a1, *a2, FadeIn(chips[0]), FadeIn(chips[1]), run_time=0.8)
        self.at("limits")
        self.play(FadeIn(banner), run_time=0.5)
        self.at("which motors")
        self.play(*[FadeIn(m) for m in motors], run_time=0.5)
        self.at("cargo outward")
        self.play(*[FadeIn(a) for a in arrows], run_time=0.6)
        self.at("a process")
        self.play(*[FadeIn(g) for g in ghosts], run_time=0.5)
        self.finish()


class S21(Sc):
    def construct(self):
        parts, P = base(tracks=True)
        kin = seated_axon(parts, P, -2.8)
        dyn = dyn_de(-2.8, cargo=BLUE, sc=1.2)
        rule = T("a sorting rule", 36, GOLD_BR, weight=BOLD).move_to([3.6, 0.4, 0])
        one = T("one way it works", 28, TEXT).move_to([3.6, -0.25, 0])
        self.add(*parts)
        self.play(FadeIn(kin), FadeIn(dyn), run_time=0.3)
        self.play(AnimationGroup(kin.xt.animate(run_time=1.5, rate_func=linear).set_value(0.4),
                                 dyn.xt.animate(run_time=1.5, rate_func=linear).set_value(0.4),
                                 Succession(Wait(0.9), FadeIn(rule, run_time=0.4)),
                                 Succession(Wait(1.2), FadeIn(one, run_time=0.4))))
        self.finish()


# ---- stage 3 replay (s22, s23): zoomed so the neuron fills the frame
NC = np.array([-3.9, -0.2, 0.0])
SIB = [(90, True, 3.7), (155, False, 2.9), (205, False, 2.9), (270, True, 3.4)]
L0, L1 = 4.5, 10.2                       # axon length at the start of s22 and at its end


class Neurite(VMobject):
    """A neurite as a bar from the soma; length from a tracker, any direction."""

    def __init__(self, deg, Lt, width, col, op=0.12, col2=None):
        super().__init__(stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=op)
        self.deg, self.Lt, self.wd = math.radians(deg), Lt, width
        self.col0, self.col1 = col, (col2 or col)
        self.ct = ValueTracker(0.0)          # 0 = first colour, 1 = second colour
        self.add_updater(self._upd)
        self._upd(self)

    def _upd(self, _=None):
        c = interpolate_color(ManimColor(self.col0), ManimColor(self.col1), self.ct.get_value())
        self.set_stroke(color=c)
        self.set_fill(color=c)
        d = np.array([math.cos(self.deg), math.sin(self.deg), 0.0])
        n = np.array([-d[1], d[0], 0.0])
        a, b = NC + d * 1.40, NC + d * max(self.Lt.get_value(), 0.6)
        h = self.wd / 2
        P = [a + n * h, b + n * h, b - n * h, a - n * h]
        self.set_points_as_corners(P + [P[0]])


def ax_arrow_geom(L):
    start, end = 1.65, L - 0.3
    return (start + end) / 2, (end - start) / 2


def stage3(L_ax=L0, ax_ori=(-1, 1, -1), ax_col=GREY):
    Lt = ValueTracker(L_ax)
    nax = Neurite(0, Lt, 3.1, GREY, col2=YELLOW)
    nax.ct.set_value(1.0 if ax_col == YELLOW else 0.0)
    nax._upd(nax)
    sibs, sib_arrows = [], []
    for deg, o, Ls_ in SIB:
        Ls = ValueTracker(Ls_)
        sibs.append(Neurite(deg, Ls, 0.72, GREY))
        d = math.radians(deg)
        sc_, sh_ = ax_arrow_geom(Ls_)
        sib_arrows.append(MT(cx=sc_, half=sh_, o=1.0 if o else -1.0, y=0, origin=NC, ang=d, h=0.06, H=0.17,
                             hl=0.32, color=PLUS_OUT if o else MINUS_OUT, auto_color=True))
    arrows = []
    cx, half = ax_arrow_geom(L_ax)
    for k, o in enumerate(ax_ori):
        arrows.append(MT(cx=cx, half=half, o=float(o), y=(k - 1) * 0.95, origin=NC, ang=0.0, h=0.06, H=0.17,
                         hl=0.34, color=PLUS_OUT if o > 0 else MINUS_OUT, auto_color=True))
    soma = make_soma(NC, 1.25)
    return dict(Lt=Lt, nax=nax, sibs=sibs, sib_arrows=sib_arrows, arrows=arrows, soma=soma)


def stage_parts(S):
    return [*S["sibs"], S["nax"], *S["sib_arrows"], *S["arrows"], S["soma"]]


class S22(Sc):
    def construct(self):
        S = stage3()
        self.play(*[FadeIn(p) for p in stage_parts(S)], run_time=0.3)
        self.at("uniform")
        D = 2.8
        kw = dict(run_time=D, rate_func=smooth)
        cx, half = ax_arrow_geom(L1)
        anims = [S["Lt"].animate(**kw).set_value(L1), S["nax"].ct.animate(**kw).set_value(1.0)]
        for a in S["arrows"]:
            anims += [a.c.animate(**kw).set_value(cx), a.half.animate(**kw).set_value(half),
                      a.o.animate(**kw).set_value(1.0)]
        ax_lab = T("axon", 32, YELLOW, weight=BOLD).move_to([1.6, 2.05, 0])
        lab = chip("one reading", GOLD_BR, 32).move_to([1.8, -2.25, 0])
        self.play(AnimationGroup(*anims, Succession(Wait(2.3), FadeIn(ax_lab, run_time=0.4)),
                                 Succession(Wait(2.55), FadeIn(lab, run_time=0.4))))
        self.finish()


class S23(Sc):
    def construct(self):
        S = stage3(L_ax=L1, ax_ori=(1, 1, 1), ax_col=YELLOW)
        ax_lab = T("axon", 32, YELLOW, weight=BOLD).move_to([1.6, 2.05, 0])
        lab = chip("one reading", GOLD_BR, 32).move_to([1.8, -2.25, 0])
        self.add(*stage_parts(S), ax_lab, lab)
        self.at("the tracks may help")
        self.play(*[flash(a, PLUS_OUT, 1.02) for a in S["arrows"]], run_time=0.7)
        self.at("choose the axon")
        ch = T("choose?", 34, GOLD_BR, weight=BOLD).move_to([-1.6, 2.15, 0])
        chl = leader([-2.3, 1.95, 0], [-2.5, 1.35, 0], GOLD_BR)
        self.play(FadeIn(ch, shift=UP * 0.1), Create(chl), run_time=0.5)
        self.at("as well", lead=0.15)
        kp = T("keep", 34, GOLD_BR, weight=BOLD).move_to([5.4, 2.15, 0])
        kpl = leader([5.6, 1.92, 0], [6.3, 1.35, 0], GOLD_BR)
        self.play(FadeIn(kp, shift=UP * 0.1), Create(kpl), run_time=0.3)
        self.wait(2.0)
        self.finish()


class S24(Sc):
    def construct(self):
        parts, P = base(tracks=False)
        ax = [lane_track(y, True) for y in AX6]
        de = [lane_track(y, o) for y, o in zip(DE6, FLY_DE)]
        fly = T("fly", 48, GOLD_BR, font=TITLE_FONT, weight=BOLD).move_to([-5.85, -1.75, 0])
        for t in de:
            t.set_opacity(0)
        self.add(*de)
        dan = []
        for t in de:
            dan += t.grow()
        self.at("flies differ", lead=0.2)
        self.play(*[FadeIn(p) for p in parts], *[FadeIn(t) for t in ax], FadeIn(fly), run_time=0.7)
        self.at("their dendrites")
        self.play(*[t.animate.set_opacity(1) for t in de], run_time=0.2)
        self.play(*dan, run_time=0.7)
        self.at("mostly minus end out")
        mc = T("mostly minus-end-out", 30, MINUS_OUT, weight=BOLD).move_to([1.6, -0.8, 0])
        self.play(FadeIn(mc), *[flash(t, MINUS_OUT, 1.04) for t, o in zip(de, FLY_DE) if not o], run_time=0.9)
        self.finish()


# ---- vertebrate and fly side by side
def mini_fork(xs, ax_ori, de_ori, title, tcol=TEXT):
    soma = make_soma([xs, 0, 0], 0.45)
    xl, xr = xs + 1.2, xs + 6.2

    def lane(s, col):
        pts = [(xs + 0.4, 0), (xl, s * 0.45), (xr, s * 0.45), (xr, s * 3.0), (xl, s * 3.0)]
        p = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=col, stroke_width=3.5, fill_color=col, fill_opacity=0.10)
        p.round_corners(0.14)
        return p
    ax, de = lane(1, YELLOW), lane(-1, BLUE)
    ys = [0.95, 1.4, 1.85, 2.3]
    mk = lambda y, o: MT(cx=(xl + xr) / 2 + 0.05, half=(xr - xl) / 2 - 0.4, o=1.0 if o else -1.0, y=y, h=0.05,
                         H=0.13, hl=0.28, color=PLUS_OUT if o else MINUS_OUT)
    arrows_a = [mk(y, o) for y, o in zip(ys, ax_ori)]
    arrows_d = [mk(-y, o) for y, o in zip(ys, de_ori)]
    t = T(title, 34, tcol, weight=BOLD).move_to([(xl + xr) / 2, 3.52, 0])
    la = T("axon", 26, YELLOW).move_to([xl + 0.8, 0.0, 0])
    ld = T("dendrite", 26, BLUE).move_to([xl + 2.5, 0.0, 0])
    return dict(soma=soma, ax=ax, de=de, aa=arrows_a, ad=arrows_d, title=t, la=la, ld=ld)


class S25(Sc):
    def construct(self):
        V = mini_fork(-6.35, [True] * 4, [True, False, False, True], "vertebrate")
        Fl = mini_fork(0.7, [True] * 4, [False, False, True, False], "fly")
        gv = VGroup(V["ax"], V["de"], V["soma"], *V["aa"], *V["ad"], V["title"])
        gf = VGroup(Fl["ax"], Fl["de"], Fl["soma"], *Fl["aa"], *Fl["ad"], Fl["title"])
        self.at("the details")
        self.play(FadeIn(gv), run_time=0.6)
        self.at("depend on the animal")
        self.play(FadeIn(gf), run_time=0.7)
        self.at("axon and")
        self.play(FadeIn(V["la"]), FadeIn(Fl["la"]), flash(V["ax"], YELLOW, 1.02), flash(Fl["ax"], YELLOW, 1.02),
                  run_time=0.4)
        self.at("dendrites")
        self.play(FadeIn(V["ld"]), FadeIn(Fl["ld"]), flash(V["de"], BLUE, 1.02), flash(Fl["de"], BLUE, 1.02),
                  run_time=0.6)
        self.at("different tracks")
        dt = T("different tracks", 32, GOLD_BR, weight=BOLD).move_to([0.0, -3.5, 0])
        self.play(FadeIn(dt), run_time=0.5)
        self.finish()


def s26_state():
    parts, P = base(tracks=True)
    kin = seated_axon(parts, P, 3.4, name=False)
    dyn = dyn_de(3.4, cargo=BLUE, sc=1.2, name=False)
    return parts, P, kin, dyn


class S26(Sc):
    def construct(self):
        parts, P, kin, dyn = s26_state()
        self.add(*parts, kin, dyn)
        l1 = T("different\ntracks", 28, TEAL, weight=BOLD, line_spacing=0.6).move_to([-2.2, 0.0, 0])
        l1a, l1b = leader([-2.2, 0.45, 0], [-2.2, 1.7, 0], TEAL), leader([-2.2, -0.45, 0], [-2.2, -1.7, 0], TEAL)
        l2 = T("different\nmotors", 28, TEXT, weight=BOLD, line_spacing=0.6).move_to([0.2, 0.0, 0])
        kb, db = kin.body.get_center(), dyn.body.get_center()
        l2a, l2b = leader([1.1, 0.3, 0], kb + np.array([-0.4, -0.05, 0]), TEXT), \
            leader([1.1, -0.3, 0], db + np.array([-0.4, 0.05, 0]), TEXT)
        l3 = T("different\ncargo", 28, TEXT, weight=BOLD, line_spacing=0.6).move_to([5.7, 0.0, 0])
        kc, dc = kin.cargo.get_center(), dyn.cargo.get_center()
        l3a, l3b = leader([5.1, 0.3, 0], kc + np.array([0.3, 0.0, 0]), TEXT), \
            leader([5.1, -0.3, 0], dc + np.array([0.3, 0.0, 0]), TEXT)
        self.at("different tracks")
        self.play(FadeIn(l1), Create(l1a), Create(l1b), run_time=0.7)
        self.at("different motors")
        self.play(FadeIn(l2), Create(l2a), Create(l2b), flash(kin.body, KIN, 1.3), flash(dyn.body, DYN, 1.3),
                  run_time=0.7)
        self.at("different cargo", lead=0.35)
        self.play(FadeIn(l3), Create(l3a), Create(l3b), flash(kin.cargo, YELLOW, 1.4), flash(dyn.cargo, BLUE, 1.4),
                  run_time=0.7)
        hold = RoundedRectangle(corner_radius=0.15, width=9.5, height=1.35, stroke_color=GOLD_BR, stroke_width=5
                                ).move_to([1.4, 1.35, 0])
        hl = T("may be part of the hold", 34, GOLD_BR, weight=BOLD).move_to([1.4, 0.0, 0])
        self.at("the tracks may")
        self.play(Create(hold), run_time=0.4)
        self.wait(0.9)
        self.play(*[FadeOut(m) for m in (l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, kin, dyn)], run_time=0.35)
        self.play(FadeIn(hl), run_time=0.35)
        self.at("next", lead=0.0)
        nxt = VGroup(T("NEXT", 28, GOLD_BR, weight=BOLD),
                     T("The Gate, and the Race Reopened", 36, TEXT, font=TITLE_FONT)
                     ).arrange(DOWN, buff=0.3).move_to([0, 2.7, 0])
        s_ = make_soma([-5.0, -0.8, 0], 1.6)
        axb = Line([-3.5, -0.8, 0], [6.2, -0.8, 0], color=YELLOW, stroke_width=70)
        gate = Line([-3.3, -0.8, 0], [-0.2, -0.8, 0], color=RED, stroke_width=70)
        gl = T("the gate", 38, RED, weight=BOLD).move_to([-1.75, -2.15, 0])
        self.play(*[FadeOut(m) for m in list(self.mobjects)], FadeIn(nxt), FadeIn(s_), FadeIn(axb), run_time=0.4)
        self.at("gate")
        self.play(Create(gate), FadeIn(gl), run_time=0.5)
        self.finish()


class S27End(EndCard):
    LINE = "The tracks may be part of the hold."
