"""Radial migration, chapter 1: The Front Goes First  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by every chapter of this lesson)
  BLUE   = the migrating neuron (soma outline, leading process, swelling)
  ORANGE = the nucleus
  YELLOW = centrosome
  GREEN  = radial glial fiber (the ladder)
  TEAL   = microtubules
  PURPLE = dynein, and LIS1 (its regulator)       (later chapters)
  PINK   = myosin II                              (later chapters)
  RED    = stalled / blocked / "not migration"
  GOLD   = a caution note ("not cortical neurons")
  GREY   = tissue zones, ventricle and surface, labels, de-emphasized
  ROSE   = birth date, as the FILL of a neuron's disc: deep rose = early-born, pale rose = later-born (this chapter only)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E87FB0"
NEURON_FILL = "#16303c"   # BLUE at about 25 percent over the background, but opaque
EARLY = "#E0558F"         # early-born fill
LATE = "#F8CFE0"          # later-born fill
GREYL = "#C3C9D1"         # lighter grey for notes that must be read


class Sp(SpokenScene):
    """SpokenScene plus until(t): wait until t seconds into the scene."""

    def until(self, t):
        r = t - self.elapsed()
        if r > 0.02:
            self.wait(r)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def lab_left(text, color, x, y, tip, size=26):
    """text whose right edge sits at x, with an arrow to `tip`."""
    t = T(text, size, color)
    t.move_to([x - t.width / 2, y, 0])
    a = arr([x + 0.12, y, 0], tip, color)
    return VGroup(t, a)


def lab_right(text, color, x, y, tip, size=26):
    """text whose left edge sits at x, with an arrow to `tip`."""
    t = T(text, size, color)
    t.move_to([x + t.width / 2, y, 0])
    a = arr([x - 0.12, y, 0], tip, color)
    return VGroup(t, a)


def text_left(text, color, x, y, size=26, **kw):
    """text whose left edge sits at x."""
    t = T(text, size, color, **kw)
    return t.move_to([x + t.width / 2, y, 0])


def fiber(x, y0=-3.0, y1=3.0, rungs=False, width=5):
    g = VGroup(Line([x, y0, 0], [x, y1, 0], color=GREEN, stroke_width=width))
    if rungs:
        for y in np.arange(y0 + 0.2, y1, 0.6):
            g.add(Line([x - 0.14, y, 0], [x + 0.14, y, 0], color=GREEN, stroke_width=2.5, stroke_opacity=0.7))
    return g


def chipfix(text, color, size=26):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ring(pos, color, r=0.34, w=5):
    return Circle(radius=r, stroke_color=color, stroke_width=w).move_to(pos)


def mini(pos, fill=NEURON_FILL, r=0.2):
    return Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=fill, fill_opacity=1).move_to(pos)


def make_card(spec, cx, cy, w, pad=0.3):
    """A credit card: rounded box with stacked lines. spec = [(text, size, color, font, weight)].
    Returns (box, [line mobjects]) with every line already in its final place."""
    texts = []
    for t, size, col, font, weight in spec:
        m = T(t, size, col, font=font, weight=weight)
        assert m.width < w - 0.5, f"card line too wide: {t!r} {m.width:.2f} > {w - 0.5:.2f}"
        texts.append(m)
    g = VGroup(*texts).arrange(DOWN, buff=0.2)
    g.move_to([cx, cy, 0])
    box = RoundedRectangle(corner_radius=0.18, width=w, height=g.height + 2 * pad, stroke_color=GREY,
                           stroke_width=3, fill_color=GREY, fill_opacity=0.09).move_to(g)
    return box, texts


class Cell:
    """A migrating neuron drawn from a few trackers (local y, scaled by sc, placed at x, y0).
    The nucleus sits a little below the soma centre so the centrosome has room inside the soma, between
    the nucleus and the leading process (the same place in every scene)."""
    RX, RY = 0.55, 0.7   # soma half-width and half-height
    NUC_DY = -0.12       # nucleus centre relative to the soma centre

    def __init__(self, x=0.0, y0=0.0, sc=1.0, **kw):
        d = dict(soma=-2.4, tip=-0.4, tail=-3.35, ws=0.0, wy=-0.4, cs=-1.92, csx=0.22, op=0.0, cs_op=0.0,
                 nuc_op=1.0, x=x, y0=y0, sc=sc)
        d.update(kw)
        self.t = {k: ValueTracker(v) for k, v in d.items()}
        self.mob = always_redraw(self.build)

    def P(self, x, y):
        return np.array([self.v("x") + self.v("sc") * x, self.v("y0") + self.v("sc") * y, 0.0])

    def v(self, k):
        return self.t[k].get_value()

    def set(self, **kw):
        for k, val in kw.items():
            self.t[k].set_value(val)

    def to(self, **kw):
        return [self.t[k].animate.set_value(val) for k, val in kw.items()]

    def build(self):
        sc = self.v("sc")
        op = self.v("op")
        if op < 0.02:
            return VGroup()
        soma, tip, tail = self.v("soma"), self.v("tip"), self.v("tail")
        ws, wy, cs, csx = self.v("ws"), self.v("wy"), self.v("cs"), self.v("csx")
        lw = 10 * sc
        g = VGroup()
        if tail < soma - self.RY - 0.02:
            g.add(Line(self.P(0, tail), self.P(0, soma - self.RY), color=BLUE, stroke_width=lw))
            g.add(Dot(self.P(0, tail), radius=0.09 * sc, color=BLUE))
        if tip > soma + self.RY + 0.02:
            g.add(Line(self.P(0, soma + self.RY), self.P(0, tip), color=BLUE, stroke_width=lw))
            g.add(Dot(self.P(0, tip), radius=0.13 * sc, color=BLUE))
        if ws > 0.03:
            g.add(Ellipse(width=1.0 * ws * sc, height=2.0 * ws * sc, stroke_color=BLUE, stroke_width=5 * sc,
                          fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, wy)))
        g.add(Ellipse(width=2 * self.RX * sc, height=2 * self.RY * sc, stroke_color=BLUE, stroke_width=5 * sc,
                      fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, soma)))
        g.add(Ellipse(width=0.74 * sc, height=0.84 * sc, stroke_color=ORANGE, stroke_width=4 * sc,
                      fill_color=ORANGE, fill_opacity=0.55 * self.v("nuc_op")).set_stroke(opacity=self.v("nuc_op"))
              .move_to(self.P(0, soma + self.NUC_DY)))
        cso = self.v("cs_op")
        if cso > 0.02:
            g.add(Dot(self.P(csx, cs), radius=0.11 * sc, color=YELLOW).set_opacity(cso))
        if op < 0.99:
            for m in g.family_members_with_points():
                m.set_stroke(opacity=m.get_stroke_opacity() * op)
                m.set_fill(opacity=m.get_fill_opacity() * op)
        return g

    def nuc_y(self, soma=None):
        """screen y of the nucleus centre (for the soma height given, or the current one)."""
        s = self.v("soma") if soma is None else soma
        return self.v("y0") + self.v("sc") * (s + self.NUC_DY)


# the resting cycle cell used by chapters of this lesson (local coordinates).
# The centrosome rests inside the soma, between the nucleus and the leading process.
REST_CS, REST_CSX = -1.86, 0.14
REST = dict(soma=-2.4, tip=1.1, tail=-3.35, ws=0.0, wy=-0.4, cs=REST_CS, csx=REST_CSX, cs_op=1.0, op=1.0)
ONE = dict(ws=1.0, cs=-0.05, csx=REST_CSX)      # stroke one: swelling, centrosome in it
TWO = dict(soma=-0.5, ws=0.0)                   # stroke two: nucleus jumps up to the centrosome; trailing end stays
CYC = dict(sc=1.5, y0=1.45)                    # screen scale for the cycle scenes


def cell_at(x, state, **geo):
    d = dict(REST)
    d.update(state)
    g = dict(CYC)
    if "op" in geo:
        d["op"] = geo.pop("op")
    g.update(geo)
    return Cell(x=x, **g, **d)


# ---------------------------------------------------------------------------------------------
# the cortical wall (scenes 1 to 4)
# ---------------------------------------------------------------------------------------------
WX0, WX1 = -3.8, 2.6
WW = WX1 - WX0
WCX = (WX0 + WX1) / 2
Y_VENT, Y_PIA = -3.3, 3.1
NEUX = -3.0
LABX = 2.9
ZONES = [("ventricular zone", -3.3, -2.1, 0.30),
         ("subventricular zone", -2.1, -1.1, 0.22),
         ("intermediate zone", -1.1, 0.5, 0.13),
         ("cortical plate", 0.5, 2.45, 0.30),
         ("marginal zone", 2.45, 3.1, 0.14)]
VZ_Y = -2.7


def wall_frame():
    return Rectangle(width=WW, height=Y_PIA - Y_VENT, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(
        [WCX, (Y_PIA + Y_VENT) / 2, 0])


def zone_band(i):
    """the fill of zone i plus its upper dividing line: (group, fill, line-or-None)."""
    n, y0, y1, op = ZONES[i]
    fill = Rectangle(width=WW, height=y1 - y0, stroke_width=0, fill_color=GREY, fill_opacity=op).move_to(
        [WCX, (y0 + y1) / 2, 0])
    line = Line([WX0, y1, 0], [WX1, y1, 0], color=GREY, stroke_width=2, stroke_opacity=0.7) if i < 4 else None
    g = VGroup(fill, line) if line is not None else VGroup(fill)
    return g, fill, line


def zone_label(i):
    n, y0, y1, op = ZONES[i]
    y = (y0 + y1) / 2
    t = text_left(n, TEXT, LABX, y, 26)
    ld = Line([WX1 + 0.1, y, 0], [LABX - 0.12, y, 0], color=GREY, stroke_width=3)
    return VGroup(t, ld)


def pia_parts():
    line = Line([WX0, Y_PIA, 0], [WX1, Y_PIA, 0], color=TEXT, stroke_width=7)
    t = text_left("pial surface", TEXT, LABX, 3.5, 26)
    ld = Line([WX1 + 0.1, Y_PIA, 0], [LABX - 0.1, 3.42, 0], color=GREY, stroke_width=3)
    return line, VGroup(t, ld)


def wall_state(n_zones):
    """Everything the wall scenes share: frame, filled zones with dividers, and labels up to n_zones."""
    parts = [zone_band(i)[0] for i in range(n_zones)] + [wall_frame()]
    labs = [zone_label(i) for i in range(n_zones)]
    return parts, labs


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Radial Migration: Climbing the Glial Ladder"
    TITLE = "The Front Goes First"


# ---------------------------------------------------------------------------------------------
class S01Q(Sp):
    """a neuron about 10 micrometres across at the foot of a wall many times its size: how does it get across?"""

    def construct(self):
        # Centre this opening wall; later zone scenes retain their label-panel layout.
        nx = NEUX + 0.6
        n = mini([nx, VZ_Y, 0])
        tick_y = VZ_Y - 0.38
        span = VGroup(Line([nx - 0.2, tick_y, 0], [nx + 0.2, tick_y, 0], color=TEXT, stroke_width=3),
                      Line([nx - 0.2, tick_y - 0.07, 0], [nx - 0.2, tick_y + 0.07, 0], color=TEXT, stroke_width=3),
                      Line([nx + 0.2, tick_y - 0.07, 0], [nx + 0.2, tick_y + 0.07, 0], color=TEXT, stroke_width=3))
        size_t = VGroup(T("about 10", 26, TEXT), T("micrometres across", 26, TEXT)).arrange(DOWN, buff=0.08,
                                                                                        aligned_edge=LEFT)
        size_t.move_to([nx + 0.7 + size_t.width / 2, VZ_Y + 0.08, 0])
        size_a = arr([nx + 0.62, VZ_Y - 0.2, 0], [nx + 0.24, tick_y + 0.03, 0], TEXT, w=3, tip=0.16)

        self.at("newborn neuron")
        self.play(FadeIn(n, scale=0.4), FadeIn(span), run_time=0.5)
        self.play(FadeIn(size_t, shift=RIGHT * 0.1), FadeIn(size_a), run_time=0.5)

        wall = wall_frame().shift(RIGHT * 0.6)
        wl = lab_right("cortical wall", TEXT, LABX + 0.6, 1.5, [WX1 + 0.64, 1.5, 0])
        self.at("wall")
        self.play(Create(wall), FadeIn(wl, shift=LEFT * 0.1), run_time=0.9)

        ys = np.arange(VZ_Y + 0.46, 3.0, 0.46)
        ghosts = VGroup(*[Circle(radius=0.2, stroke_color=GREY, stroke_width=3, stroke_opacity=0.9).move_to(
            [nx, y, 0]) for y in ys])
        by = Y_VENT
        brace = DoubleArrow([WX0 + 0.2, Y_VENT, 0], [WX0 + 0.2, Y_PIA, 0], color=GREYL, stroke_width=4,
                            tip_length=0.22, buff=0)
        bl = T("many times its own size", 26, GREYL).rotate(PI / 2).move_to([WX0 - 0.4, (Y_VENT + Y_PIA) / 2, 0])
        self.at("its own size")
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in ghosts], lag_ratio=0.1), run_time=1.4)
        self.play(GrowFromCenter(brace), FadeIn(bl), run_time=0.6)

        self.at("no legs")
        self.play(Indicate(n, color=BLUE, scale_factor=1.5), run_time=0.9)

        q = T("?", 120, TEXT, weight=BOLD).move_to([0.0, 0.3, 0])
        self.at("how does it")
        self.play(FadeIn(q, scale=0.6), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Zones(Sp):
    """the wall builds one zone at a time from the ventricle outward: an empty box first."""

    def construct(self):
        frame = wall_frame()
        n = mini([NEUX, VZ_Y, 0])
        self.add(frame, n)
        self.at("layers")
        self.play(Indicate(frame, color=TEXT, scale_factor=1.02), run_time=0.9)

        self.at("born in")
        self.play(Indicate(n, color=BLUE, scale_factor=1.6), run_time=0.7)
        b0, f0, l0 = zone_band(0)
        lab0 = zone_label(0)
        self.at("ventricular zone")
        self.play(GrowFromEdge(f0, DOWN), Create(l0), FadeIn(lab0, shift=LEFT * 0.15), run_time=0.8)

        bar = Line([WX0, Y_VENT, 0], [WX1, Y_VENT, 0], color=TEXT, stroke_width=7)
        inside = lab_left("inside", GREY, WX0 - 0.75, Y_VENT + 0.3, [WX0 - 0.04, Y_VENT + 0.04, 0])
        self.at("inside")
        self.play(Create(bar), FadeIn(inside, shift=RIGHT * 0.1), run_time=0.7)

        b1, f1, l1 = zone_band(1)
        self.at("subventricular")
        self.play(GrowFromEdge(f1, DOWN), Create(l1), FadeIn(zone_label(1), shift=LEFT * 0.15), run_time=0.8)
        b2, f2, l2 = zone_band(2)
        self.at("intermediate")
        self.play(GrowFromEdge(f2, DOWN), Create(l2), FadeIn(zone_label(2), shift=LEFT * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Zones2(Sp):
    """two more zones, and the pial surface at the top."""

    def construct(self):
        parts, labs = wall_state(3)
        n = mini([NEUX, VZ_Y, 0])
        self.add(*parts, *labs, n)

        b3, f3, l3 = zone_band(3)
        self.at("cortical plate")
        self.play(GrowFromEdge(f3, DOWN), Create(l3), FadeIn(zone_label(3), shift=LEFT * 0.15), run_time=0.8)
        self.at("settle")
        self.play(Indicate(f3, color=GREY, scale_factor=1.03), run_time=0.8)

        b4, f4, l4 = zone_band(4)
        self.at("marginal zone")
        self.play(GrowFromEdge(f4, DOWN), FadeIn(zone_label(4), shift=LEFT * 0.15), run_time=0.8)

        pia, pia_l = pia_parts()
        self.at("just under the surface")
        self.play(Create(pia), FadeIn(pia_l, shift=LEFT * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Birth(Sp):
    """neurons coloured by birth date. Born in the ventricular zone, they must travel: early-born settle deep,
    later-born nearer the surface."""

    def construct(self):
        parts, labs = wall_state(5)
        pia, pia_l = pia_parts()
        n0 = mini([NEUX, VZ_Y, 0])
        self.add(*parts, *labs, pia, pia_l, n0)

        # keep the ventricular zone and cortical plate labels; the others make room
        self.at("birth date")
        self.play(FadeOut(labs[1]), FadeOut(labs[2]), FadeOut(labs[4]), FadeOut(pia_l), run_time=0.6)
        ex = [NEUX, NEUX + 2.0, NEUX + 4.0]
        early = VGroup(n0, *[mini([x, VZ_Y, 0], fill=EARLY) for x in ex[1:]])
        self.play(n0.animate.set_fill(EARLY, 1), *[GrowFromCenter(e) for e in early[1:]], run_time=0.6)

        self.at("early born")
        self.play(early.animate.shift(UP * (0.95 - VZ_Y)), run_time=1.4, rate_func=smooth)
        e_lab = lab_left("early-born", EARLY, WX0 - 0.3, 0.95, [WX0 - 0.03, 0.95, 0], 26)
        self.at("deep")
        self.play(FadeIn(e_lab, shift=RIGHT * 0.1), run_time=0.5)

        lx = [NEUX + 1.0, NEUX + 3.0, NEUX + 4.9]
        late = VGroup(*[mini([x, VZ_Y, 0], fill=LATE) for x in lx])
        self.at("later born")
        self.play(*[FadeIn(m, scale=0.3) for m in late], late.animate.shift(UP * (1.95 - VZ_Y)), run_time=0.85,
                  rate_func=smooth)
        l_lab = lab_left("later-born", LATE, WX0 - 0.3, 1.95, [WX0 - 0.03, 1.95, 0], 26)
        self.at("near the surface")
        self.play(FadeIn(l_lab, shift=RIGHT * 0.1), run_time=0.5)

        trav = arr([WX1 - 0.18, VZ_Y, 0], [WX1 - 0.18, 2.2, 0], TEXT, w=7, tip=0.3)
        tl = T("must travel", 26, TEXT)
        tl.move_to([WX1 - 0.55 - tl.width / 2, -0.3, 0])
        self.at("every neuron")
        self.play(GrowArrow(trav), run_time=1.0)
        self.at("must travel")
        self.play(FadeIn(tl, shift=RIGHT * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Parts(Sp):
    """a bipolar neuron: leading process, cell body, nucleus."""
    G = dict(x=0.0, y0=1.6, sc=1.5)
    S = dict(soma=-2.2, tip=1.0, tail=-3.4, cs_op=0.0)

    def construct(self):
        c = Cell(**self.G, **self.S, op=0.0)
        self.add(c.mob)
        P = c.P
        self.at("migrating neuron")
        self.play(c.t["op"].animate.set_value(1), run_time=0.8)

        ly = P(0, 0.4)[1]
        lp = lab_left("leading process", BLUE, -0.9, ly, [P(0, 0.4)[0] - 0.14, ly, 0])
        self.at("leading process")
        self.play(FadeIn(lp, shift=RIGHT * 0.1), run_time=0.5)

        arm = Line(P(0, -1.5), P(0, 1.0), color=TEXT, stroke_width=12)
        self.at("long arm")
        self.play(ShowPassingFlash(arm, time_width=0.7), run_time=0.6)

        up = arr([1.05, 0.5, 0], [1.05, 2.7, 0], TEXT, w=7, tip=0.3)
        ul = text_left("direction of travel", TEXT, 1.4, 1.6, 26)
        self.at("pointing the way")
        self.play(GrowArrow(up), FadeIn(ul, shift=RIGHT * 0.1), run_time=0.9)

        sy = P(0, -2.2)[1]
        sring = Ellipse(width=2 * c.RX * 1.5 + 0.2, height=2 * c.RY * 1.5 + 0.2, stroke_color=GREYL, stroke_width=3
                        ).move_to(P(0, -2.2))
        self.at("behind it")
        self.play(Create(sring), run_time=0.5)
        cb = lab_right("cell body (soma)", BLUE, 1.35, sy, [P(c.RX, -2.2)[0] + 0.1, sy, 0])
        self.at("cell body")
        self.play(FadeIn(cb, shift=LEFT * 0.1), run_time=0.5)
        self.play(FadeOut(sring), run_time=0.3)

        ny = c.nuc_y()
        nl = lab_left("nucleus", ORANGE, -1.35, ny, [P(-0.37, -2.2 - 0.12)[0] - 0.05, ny, 0])
        self.at("nucleus")
        rg = ring(P(0, -2.2 - 0.12), ORANGE, r=0.75, w=4)
        self.play(FadeIn(nl, shift=RIGHT * 0.1), FadeIn(rg, scale=1.4), run_time=0.6)
        self.play(FadeOut(rg), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Centro(Sp):
    """zoom on the cell body: the centrosome beside the nucleus, microtubules radiating from it."""
    CX, CY = 1.6, -0.2      # centre of the magnified cell body
    A, B = 2.5, 3.2         # its half-width and half-height

    def ray_end(self, p, ang):
        """where a ray from p at angle `ang` meets the magnified body outline (a little short of it)."""
        d = np.array([np.cos(ang), np.sin(ang)])
        o = np.array([p[0] - self.CX, p[1] - self.CY])
        a, b = d[0] / self.A, d[1] / self.B
        c0, c1, c2 = a * a + b * b, 2 * (o[0] * d[0] / self.A ** 2 + o[1] * d[1] / self.B ** 2), \
            (o[0] / self.A) ** 2 + (o[1] / self.B) ** 2 - 1
        tt = (-c1 + np.sqrt(c1 * c1 - 4 * c0 * c2)) / (2 * c0)
        return np.array([p[0] + d[0] * (tt - 0.14), p[1] + d[1] * (tt - 0.14), 0.0])

    def on_outline(self, deg):
        a = np.deg2rad(deg)
        return np.array([self.CX + self.A * np.cos(a), self.CY + self.B * np.sin(a), 0.0])

    def construct(self):
        c = Cell(x=0.0, y0=1.6, sc=1.5, soma=-2.2, tip=1.0, tail=-3.4, cs_op=0.0, op=1.0)
        self.add(c.mob)
        self.at("near the nucleus")
        self.play(c.t["x"].animate.set_value(-4.4), run_time=0.5)
        sp = c.P(0, -2.2)
        rg = ring(sp, GREY, r=1.3, w=3)
        big = Ellipse(width=2 * self.A, height=2 * self.B, stroke_color=BLUE, stroke_width=6,
                      fill_color=NEURON_FILL, fill_opacity=1).move_to([self.CX, self.CY, 0])
        nuc = Ellipse(width=2.9, height=3.8, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE,
                      fill_opacity=0.55).move_to([self.CX, self.CY - 0.7, 0])
        s1 = sp + 1.3 * np.array([np.cos(np.deg2rad(35)), np.sin(np.deg2rad(35)), 0])
        s2 = sp + 1.3 * np.array([np.cos(np.deg2rad(-35)), np.sin(np.deg2rad(-35)), 0])
        l1 = Line(s1, self.on_outline(125), color=GREY, stroke_width=2)
        l2 = Line(s2, self.on_outline(235), color=GREY, stroke_width=2)
        self.play(Create(rg), run_time=0.25)
        self.play(Create(l1), Create(l2), FadeIn(big), run_time=0.45)
        nl = lab_right("nucleus", ORANGE, 4.5, -1.9, [self.CX + 1.2, -1.9, 0])
        self.play(FadeIn(nuc), FadeIn(nl, shift=LEFT * 0.1), run_time=0.45)

        cpos = np.array([self.CX + 0.6, 1.85, 0.0])
        cdot = Dot(cpos, radius=0.24, color=YELLOW)
        cdot.set_z_index(4)
        cl = lab_right("centrosome", YELLOW, 4.0, 2.6, [cpos[0] + 0.2, cpos[1] + 0.2, 0])
        self.at("centrosome")
        self.play(FadeIn(cdot, scale=2.0), FadeIn(cl, shift=LEFT * 0.1), run_time=0.6)

        rays = VGroup(*[Line(cpos, self.ray_end(cpos, np.deg2rad(a)), color=TEAL, stroke_width=3.5,
                             stroke_opacity=0.65) for a in range(-20, 201, 22)])
        self.at("organizing")
        self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.12), run_time=1.5)
        r0 = rays[0]
        tipp = r0.get_start() + 0.62 * (r0.get_end() - r0.get_start())
        ml = lab_right("microtubules", TEAL, 4.45, 0.45, tipp + np.array([0.05, -0.03, 0]), 24)
        self.at("microtubules")
        self.play(FadeIn(ml, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
PANEL_X0, PANEL_X1 = -6.3, 0.9        # left picture panel
CARDX, CARDW = 3.95, 5.5              # right credit card
RAK_FX = [-5.5, -4.3, -3.1, -1.9]     # radial glial fibres
# (fibre, side, y) of each young neuron pressed along a fibre
RAK_SPEC = [(0, 1, -2.4), (0, 1, 0.3), (0, -1, 1.7), (1, -1, -1.2), (1, 1, 1.4), (2, 1, -2.4), (2, -1, 0.0),
            (2, 1, 1.7), (3, -1, -0.8), (3, 1, 1.2)]
NEU_HALF = 0.17                      # half-width of a neuron lying along a fibre


def wall_picture():
    """Schematic of the wall with radial glial fibres and young neurons pressed along them (Rakic scene).
    Returns bars, fibres, neurons (placed a small gap off their fibre), their pressed positions, gap positions."""
    bars = VGroup(*[RoundedRectangle(corner_radius=0.07, width=5.3, height=0.14, stroke_width=0, fill_color=GREY,
                                     fill_opacity=0.6).move_to([-3.65, y, 0]) for y in (-3.3, 3.1)])
    fibs = VGroup(*[Line([x, -3.2, 0], [x, 3.0, 0], color=GREEN, stroke_width=5) for x in RAK_FX])
    final = [[RAK_FX[f] + s * NEU_HALF, y, 0] for f, s, y in RAK_SPEC]
    start = [[RAK_FX[f] + s * (NEU_HALF + 0.2), y, 0] for f, s, y in RAK_SPEC]
    ns = VGroup(*[Ellipse(width=2 * NEU_HALF, height=0.95, stroke_color=BLUE, stroke_width=4, fill_color=NEURON_FILL,
                          fill_opacity=1).move_to(p) for p in start])
    return bars, fibs, ns, final, start


class S07Rakic(Sp):
    """Rakic 1972: young neurons from fetal monkey cortex, pressed along radial glial fibres."""

    def construct(self):
        bars, fibs, ns, final, start = wall_picture()
        box, lines = make_card([("1972", 54, TEXT, TITLE_FONT, NORMAL), ("Pasko Rakic", 38, TEXT, FONT, BOLD),
                                ("serial electron micrographs", 26, GREY, FONT, NORMAL),
                                ("fetal rhesus monkey cortex", 26, GREY, FONT, NORMAL)], CARDX, 0.2, CARDW)
        # the picture first: the two surfaces and the four fibres that span the wall
        self.play(FadeIn(bars), LaggedStart(*[Create(f) for f in fibs], lag_ratio=0.2), FadeIn(box),
                  FadeIn(lines[0], shift=UP * 0.1), run_time=1.5)
        self.at("rakic")
        self.play(FadeIn(lines[1], shift=UP * 0.1), run_time=0.6)
        self.at("rebuilt")
        self.play(FadeIn(lines[2], shift=UP * 0.1), run_time=0.5)
        self.at("young neurons")
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in ns], lag_ratio=0.08), run_time=1.0)
        self.at("fetal monkey cortex")
        self.play(FadeIn(lines[3], shift=UP * 0.1), run_time=0.5)

        self.at("pressed along")
        touch = VGroup(*[Dot([RAK_FX[f], y, 0], radius=0.09, color=GREEN) for f, s, y in RAK_SPEC])
        self.play(*[n.animate.move_to(p) for n, p in zip(ns, final)], FadeIn(touch, scale=2.0), run_time=0.8)
        # Opaque backing keeps the bright label clear of the fibres below the surface bar.
        fl = chipfix("radial glial fibres", GREEN, 26).move_to([-3.65, 2.65, 0])
        fl[2].set_color("#B6E5A5")
        fl.set_z_index(5)
        fa = arr([-2.0, 2.4, 0], [-1.9, 1.9, 0], GREEN, w=3, tip=0.14)
        self.at("fibers", lead=0.4)
        self.play(FadeIn(fl), FadeIn(fa), FadeOut(touch), run_time=0.2)

        span = DoubleArrow([-0.95, -3.2, 0], [-0.95, 3.0, 0], color=GREEN, stroke_width=5, tip_length=0.25, buff=0)
        sl = T("spans the wall", 24, GREEN).rotate(PI / 2).move_to([-0.45, 0, 0])
        self.at("spanning")
        self.play(GrowFromCenter(span), FadeIn(sl), run_time=1.0)
        self.finish()


class S08Fixed(Sp):
    """the same image, frozen: fixed tissue shows contact, not motion."""

    def construct(self):
        bars, fibs, ns, final, start = wall_picture()
        for n, p in zip(ns, final):
            n.move_to(p)
        self.add(bars, fibs, ns)
        pause = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.2, height=0.75, stroke_width=0, fill_color=TEXT,
                                          fill_opacity=0.9).move_to([x, 2.0, 0]) for x in (2.2, 2.6)])
        t1 = text_left("fixed tissue", TEXT, 3.2, 2.0, 44, weight=BOLD)
        self.at("fixed tissue")
        self.play(FadeIn(pause), FadeIn(t1, shift=RIGHT * 0.1), run_time=0.5)
        t2 = text_left("shows contact,", TEXT, 1.9, 0.8, 42)
        self.at("shows contact")
        touch = VGroup(*[Dot([RAK_FX[f], y, 0], radius=0.09, color=TEXT) for f, s, y in RAK_SPEC])
        self.play(FadeIn(t2, shift=RIGHT * 0.1), FadeIn(touch, scale=2.0), run_time=0.6)
        t3 = text_left("not motion", RED, 1.9, -0.4, 42, weight=BOLD)
        self.at("cannot show")
        self.play(FadeIn(t3, shift=RIGHT * 0.1), run_time=0.5)
        qs = VGroup(*[T("?", 44, RED, weight=BOLD).move_to([final[i][0], final[i][1] + 0.8, 0])
                      for i in (1, 4, 6)])
        self.at("which cell moved")
        self.play(LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
DISH_REST = dict(soma=-2.3, tip=-0.7, tail=-3.15, cs_op=0.0)   # the dish cell at rest (scenes 9 and 10)
FIBX = -2.38


def dish():
    """Hatten's dish: a coverslip panel on the left, with one glial fibre."""
    cx = (PANEL_X0 + PANEL_X1) / 2
    slip = RoundedRectangle(corner_radius=0.2, width=PANEL_X1 - PANEL_X0, height=7.0, stroke_color=GREY,
                            stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([cx, 0, 0])
    lab = text_left("coverslip", GREY, -1.8, -3.15, 24)
    fib = fiber(FIBX, -3.3, 3.3, rungs=True)
    return slip, lab, fib


def fibre_label():
    t = text_left("glial fibre", GREEN, -1.55, 2.9, 26)
    a = arr([-1.67, 2.9, 0], [FIBX + 0.17, 2.9, 0], GREEN, w=3, tip=0.14)
    return VGroup(t, a)


class S09Hatten(Sp):
    """Edmondson and Hatten 1987: living neurons filmed on glial fibres in a dish."""

    def construct(self):
        slip, lab, fib = dish()
        c = Cell(x=-4.4, y0=0.0, sc=1.0, op=0.0, **DISH_REST)
        self.add(c.mob)
        box, lines = make_card([("1987", 54, TEXT, TITLE_FONT, NORMAL),
                                ("Edmondson and Hatten", 30, TEXT, FONT, BOLD),
                                ("granule neurons and astroglia", 24, GREY, FONT, NORMAL),
                                ("early postnatal mouse cerebellum", 22, GREY, FONT, NORMAL)], CARDX, 0.2, CARDW)
        # the dish and its fibre first: settle the ladder before the cell climbs onto it
        self.play(FadeIn(box), FadeIn(lines[0], shift=UP * 0.1), FadeIn(slip), FadeIn(lab), Create(fib), run_time=1.4)
        self.at("edmondson")
        self.play(FadeIn(lines[1], shift=UP * 0.1), run_time=0.6)
        self.at("filmed")
        self.play(FadeIn(lines[2], shift=UP * 0.1), run_time=0.5)
        self.at("living neurons")
        self.play(c.t["op"].animate.set_value(1), c.t["x"].animate.set_value(-3.0), FadeIn(lines[3], shift=UP * 0.1),
                  run_time=1.0)
        fl = fibre_label()
        self.at("glial fibers")
        self.play(FadeIn(fl, shift=LEFT * 0.1), run_time=0.5)
        self.play(Indicate(fib, color=GREEN, scale_factor=1.0), run_time=0.8)
        self.finish()


class S10Stop(Sp):
    """time-lapse in the dish: the cell body steps in bursts; the tip reaches and pulls back on its own schedule.
    The body's path is computed from the lesson's numbers (bursts of 56 micrometres an hour, 33 an hour overall);
    the plot on the right is drawn from the very same functions that move the cell."""
    T_END = 6.6                  # seconds of film = 60 minutes of time-lapse
    MIN_PER_S = 60.0 / 6.6
    BURSTS = [(0.3, 2.2), (4.6, 6.6)]        # moving 3.9 s of 6.6 s: 59 percent, which is 33 / 56
    U2S = 0.0909                 # screen units per micrometre
    SOMA0 = -2.3

    @staticmethod
    def sm(t, a, b):
        u = min(max((t - a) / (b - a), 0.0), 1.0)
        return u * u * (3 - 2 * u)

    def soma_um(self, t):
        moving = sum(max(0.0, min(t, b) - a) for a, b in self.BURSTS)
        return 56.0 / 60.0 * self.MIN_PER_S * moving

    def len_f(self, t):
        """schematic tip length beyond the soma centre, in screen units."""
        s = self.sm
        return 1.6 + 0.8 * s(t, 3.3, 4.0) - 1.2 * s(t, 4.3, 4.9) + 0.6 * s(t, 5.3, 5.8) - 0.5 * s(t, 6.0, 6.5)

    def soma_f(self, t):
        return self.SOMA0 + self.U2S * self.soma_um(min(t, self.T_END))

    def tip_um(self, t):
        t = min(t, self.T_END)
        return self.soma_um(t) + self.len_f(t) / self.U2S

    def construct(self):
        assert abs(self.soma_um(self.T_END) - 33.0) < 0.5, self.soma_um(self.T_END)
        slip, lab, fib = dish()
        self.add(slip, lab, fib, fibre_label())
        c = Cell(x=-3.0, y0=0.0, sc=1.0, op=1.0, **DISH_REST)
        self.add(c.mob)
        drv = Mobject()

        def drive(m, dt):
            t = self.elapsed()
            sm_ = self.soma_f(t)
            c.set(soma=sm_, tail=sm_ - 0.85, tip=sm_ + self.len_f(min(t, self.T_END)))
        drv.add_updater(drive)
        self.add(drv)

        # the plot: fills the right side of the frame
        ox, oy, gx, gy = 2.7, -2.5, 3.9, 5.2
        YMAX = 60.0
        axes = VGroup(Line([ox, oy, 0], [ox + gx, oy, 0], color=GREYL, stroke_width=3),
                      Line([ox, oy, 0], [ox, oy + gy, 0], color=GREYL, stroke_width=3))
        ticks = VGroup()
        for m in (0, 20, 40, 60):
            x = ox + gx * m / 60.0
            ticks.add(Line([x, oy, 0], [x, oy - 0.1, 0], color=GREYL, stroke_width=3))
            ticks.add(M(str(m), 26, GREYL).move_to([x, oy - 0.42, 0]))
        for u in (0, 20, 40, 60):
            y = oy + gy * u / YMAX
            ticks.add(Line([ox, y, 0], [ox - 0.1, y, 0], color=GREYL, stroke_width=3))
            tt = M(str(u), 26, GREYL)
            ticks.add(tt.move_to([ox - 0.2 - tt.width / 2, y, 0]))
        ax_t = T("time (minutes)", 26, GREYL).move_to([ox + gx / 2, oy - 0.95, 0])
        ax_p = text_left("position (µm)", GREYL, ox - 0.4, oy + gy + 0.4, 26)

        def mapx(t):
            return ox + gx * min(t, self.T_END) / self.T_END

        def mapy(um):
            return oy + gy * um / YMAX

        def trace(fn, color):
            def build():
                t = self.elapsed()
                ts = np.linspace(0, min(t, self.T_END), max(2, int(min(t, self.T_END) * 24) + 2))
                m = VMobject(stroke_color=color, stroke_width=5)
                m.set_points_as_corners([[mapx(u), mapy(fn(u)), 0] for u in ts])
                return m
            return always_redraw(build)

        tr_s = trace(self.soma_um, ORANGE)
        tr_t = trace(self.tip_um, BLUE)
        # legend inside the empty upper-left of the plot
        lg = VGroup()
        for k, (name, col) in enumerate([("cell body", ORANGE), ("tip", BLUE)]):
            y = oy + gy - 0.35 - 0.6 * k
            lg.add(Line([ox + 0.25, y, 0], [ox + 0.8, y, 0], color=col, stroke_width=6))
            lg.add(text_left(name, col, ox + 0.95, y, 26))
        note = VGroup(T("tip trace:", 24, GREY), T("schematic", 24, GREY)).arrange(DOWN, buff=0.05)
        note.move_to([ox + gx - 1.0, oy + 0.55, 0])
        self.play(FadeIn(axes), FadeIn(ticks), FadeIn(ax_t), FadeIn(ax_p), FadeIn(lg), FadeIn(note), run_time=0.4)
        self.add(tr_s, tr_t)

        P = c.P
        body_l = always_redraw(lambda: lab_left("cell body", ORANGE, -3.95, P(0, c.v("soma"))[1],
                                                [P(-c.RX, c.v("soma"))[0] - 0.06, P(0, c.v("soma"))[1], 0]))
        self.at("neurons moved")
        self.add(body_l)
        tip_l = always_redraw(lambda: lab_left("tip", BLUE, -3.55, P(0, c.v("tip"))[1],
                                               [P(0, c.v("tip"))[0] - 0.17, P(0, c.v("tip"))[1], 0]))
        self.at("tip reached")
        self.add(tip_l)
        self.at("out of step")
        self.wait(1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11Schaar(Sp):
    """Schaar and McConnell 2005: single cycles in neuroblasts of newborn rats, in a gel. Not cortical neurons."""

    def construct(self):
        cx = (PANEL_X0 + PANEL_X1) / 2
        gel = RoundedRectangle(corner_radius=0.2, width=PANEL_X1 - PANEL_X0, height=7.0, stroke_color=GREY,
                               stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([cx, 0, 0])
        rng = np.random.RandomState(4)
        specks = VGroup(*[Dot([rng.uniform(PANEL_X0 + 0.3, PANEL_X1 - 0.3), rng.uniform(-3.2, 3.2), 0], radius=0.05,
                              color=GREY).set_opacity(0.45) for _ in range(34)])
        gel_l = text_left("gel", GREYL, -1.0, 3.1, 26)
        c = Cell(x=-2.7, y0=0.4, sc=1.1, soma=-2.4, tip=0.9, tail=-3.3, cs_op=0.0, op=0.0)
        self.add(c.mob)
        box, lines = make_card([("2005", 54, TEXT, TITLE_FONT, NORMAL),
                                ("Schaar and McConnell", 30, TEXT, FONT, BOLD),
                                ("neuroblasts from newborn rats", 24, GREY, FONT, NORMAL),
                                ("anterior subventricular zone", 24, GREY, FONT, NORMAL),
                                ("migrating in a gel", 24, GREY, FONT, NORMAL),
                                ("not cortical neurons", 30, GOLD, FONT, BOLD)], CARDX, 0.2, CARDW)
        self.play(FadeIn(box), FadeIn(lines[0]), FadeIn(lines[1], shift=UP * 0.1), run_time=0.6)
        specks.set_z_index(-3)
        gel.set_z_index(-4)
        self.at("then watched")
        self.play(FadeIn(gel), FadeIn(specks), FadeIn(gel_l), c.t["op"].animate.set_value(1),
                  run_time=0.8)
        P = c.P
        cyc = T("cycle 1", 26, GREYL)
        cyc.move_to([-1.0 - 0.0 + cyc.width / 2 - 0.0, 2.35, 0])
        cyc.move_to([-1.9 + cyc.width / 2, 2.35, 0])

        def jump(rt=0.8):
            return [*c.to(soma=c.v("soma") + 0.55, tail=c.v("tail") + 0.55, tip=c.v("tip") + 0.55)], rt

        # three plain jumps of the whole cell: single cycles, with nothing drawn inside it
        a, rt = jump()
        self.at("single cycles")
        self.play(*a, FadeIn(cyc, shift=UP * 0.1), run_time=rt)
        nb = always_redraw(lambda: lab_left("neuroblast", BLUE, -3.95, P(0, c.v("soma"))[1],
                                            [P(-c.RX, c.v("soma"))[0] - 0.06, P(0, c.v("soma"))[1], 0]))
        self.at("neuroblasts")
        self.add(nb)
        self.play(*[FadeIn(l, shift=UP * 0.1) for l in lines[2:5]], run_time=0.6)
        self.until(4.3)
        cyc2 = T("cycle 2", 26, GREYL).move_to(cyc)
        a, rt = jump()
        self.play(*a, Transform(cyc, cyc2), run_time=rt)
        self.at("young migrating")
        self.play(Indicate(nb, color=TEXT, scale_factor=1.12), run_time=0.8)
        self.until(5.7)
        cyc3 = T("cycle 3", 26, GREYL).move_to(cyc)
        a, rt = jump()
        self.play(*a, Transform(cyc, cyc3), run_time=rt)
        self.at("newborn rats")
        self.play(Indicate(gel_l, color=TEXT, scale_factor=1.3), Indicate(lines[2], color=TEXT, scale_factor=1.06),
                  run_time=0.9)
        self.at("not cortical")
        self.play(FadeIn(lines[5], shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
CELLX = -1.2          # the cycle cell sits left of centre; the right panel holds the labels
RPX = 3.95            # centre of the right panel


def pred_labels(c):
    """Labels for the centrosome and the nucleus, riding on the cell (left side)."""
    P = c.P
    cl = always_redraw(lambda: lab_left("centrosome", YELLOW, -3.0, P(c.v("csx"), c.v("cs"))[1] + 0.35,
                                        [P(c.v("csx"), c.v("cs"))[0] - 0.18, P(c.v("csx"), c.v("cs"))[1] + 0.05, 0]))
    nl = always_redraw(lambda: lab_left("nucleus", ORANGE, -3.0, c.nuc_y() - 0.35,
                                        [P(-0.37, c.v("soma") + c.NUC_DY)[0] - 0.05, c.nuc_y() - 0.2, 0]))
    return cl, nl


def predict_block():
    """right panel of the pause-and-predict question."""
    x = 1.8
    cap = text_left("Pause and predict", TEXT, x, 2.6, 40, weight=BOLD)
    qa = text_left("Which moves into", TEXT, x, 1.2, 38)
    qb = text_left("the swelling first?", TEXT, x, 0.5, 38)
    qc = text_left("the centrosome", YELLOW, x, -0.6, 38)
    qd = text_left("or the nucleus?", ORANGE, x, -1.3, 38)
    return cap, qa, qb, qc, qd


def swelling_label(c):
    sy = c.P(0, -0.4)[1]
    return lab_right("swelling", BLUE, -0.05, sy, [c.P(0.5, -0.4)[0] + 0.04, sy, 0])


class S12Predq(Sp):
    """a swelling forms ahead of the nucleus. Which moves into it first?"""

    def construct(self):
        c = cell_at(CELLX, {}, op=0.0)
        self.add(c.mob)
        self.play(c.t["op"].animate.set_value(1), run_time=0.2)
        self.at("swelling forms")
        self.play(*c.to(ws=1.0), run_time=1.5)
        sw = swelling_label(c)
        self.play(FadeIn(sw, shift=LEFT * 0.1), run_time=0.4)
        cap, qa, qb, qc, qd = predict_block()
        q = T("?", 80, TEXT, weight=BOLD).move_to(c.P(0, -0.4))
        self.at("which moves")
        self.play(FadeIn(cap, shift=DOWN * 0.1), FadeIn(qa, shift=UP * 0.1), FadeIn(qb, shift=UP * 0.1),
                  FadeIn(q, scale=0.6), run_time=0.7)
        cl, nl = pred_labels(c)
        P = c.P
        self.at("the centrosome")
        self.add(cl)
        fl = ring(P(REST_CSX, REST_CS), YELLOW, r=0.3, w=4)
        self.play(FadeIn(cl), FadeIn(qc, shift=UP * 0.1), FadeIn(fl, scale=1.8), run_time=0.6)
        self.play(FadeOut(fl), run_time=0.3)
        self.at("or the nucleus")
        self.add(nl)
        self.play(FadeIn(nl), FadeIn(qd, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S13Pause(NarratedScene):
    """still: the question stays on screen while the viewer predicts."""

    def construct(self):
        c = cell_at(CELLX, dict(ws=1.0))
        self.add(c.mob)
        q = T("?", 80, TEXT, weight=BOLD).move_to(c.P(0, -0.4))
        cl, nl = pred_labels(c)
        self.add(*predict_block(), q, cl, nl, swelling_label(c))
        self.finish()


S1_Y, N1_Y, N2_Y, S2_Y = 2.5, 1.35, 0.3, -1.0     # right column: stroke one / note / note / stroke two


def stroke_chip(text, hot, y):
    col = TEXT if hot else GREY
    return chipfix(text, col, 30).move_to([RPX, y, 0])


def lit(ch, on):
    col = TEXT if on else GREY
    return [ch[1].animate.set_stroke(col).set_fill(col, 0.16), ch[2].animate.set_color(col)]


def note_block(lines, y, size=26):
    g = VGroup(*[T(t, size, GREYL) for t in lines]).arrange(DOWN, buff=0.1)
    return g.move_to([RPX, y, 0])


class S14Reveal(Sp):
    """the centrosome moves into the swelling first; then the nucleus jumps forward."""

    def construct(self):
        c = cell_at(CELLX, dict(ws=1.0))
        self.add(c.mob)
        cl, nl = pred_labels(c)
        self.add(cl, nl)
        s1 = stroke_chip("stroke one", True, S1_Y)
        s2 = stroke_chip("stroke two", False, S2_Y)
        n1 = note_block(["centrosome ahead in cells", "fixed mid-cycle"], N1_Y)
        n2 = note_block(["later tracked live in", "rat cortical slices"], N2_Y)
        P = c.P

        self.at("centrosome goes")
        self.play(FadeIn(s1, shift=LEFT * 0.2), *c.to(cs=ONE["cs"], csx=ONE["csx"]), run_time=1.4)
        self.at("cells fixed")
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.6)
        ahead = ring(P(ONE["csx"], ONE["cs"]), YELLOW, r=0.3, w=4)
        self.at("show it ahead")
        self.play(FadeIn(ahead, scale=1.8), run_time=0.4)
        self.play(FadeOut(ahead), run_time=0.4)
        self.at("later movies")
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.6)
        trail = DashedLine(P(REST_CSX, REST_CS), P(ONE["csx"], ONE["cs"]), color=YELLOW, stroke_width=4,
                           dash_length=0.12)
        self.at("tracked")
        self.play(Create(trail), run_time=0.9)
        self.at("then the nucleus")
        self.play(FadeIn(s2, shift=LEFT * 0.2), *lit(s1, False), *lit(s2, True), FadeOut(trail),
                  *c.to(soma=TWO["soma"], ws=0.0, y0=0.6, tail=-2.5), run_time=0.9)
        self.finish()


class S15Beat(NarratedScene):
    """a beat: the end of the cycle holds still."""

    def construct(self):
        c = cell_at(CELLX, dict(ONE, **TWO, tail=-2.5), y0=0.6)
        self.add(c.mob)
        cl, nl = pred_labels(c)
        s1 = stroke_chip("stroke one", False, S1_Y)
        s2 = stroke_chip("stroke two", True, S2_Y)
        n1 = note_block(["centrosome ahead in cells", "fixed mid-cycle"], N1_Y)
        n2 = note_block(["later tracked live in", "rat cortical slices"], N2_Y)
        self.add(cl, nl, s1, s2, n1, n2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S16Rule(Sp):
    """the one idea: the front goes first; the cell has moved only when its nucleus catches up."""
    X = -3.7

    def construct(self):
        # start where the last scene left the cell, then reset it quietly to the left while the rule appears
        c = cell_at(CELLX, dict(ONE, **TWO, tail=-2.5), y0=0.6)
        self.add(c.mob)
        P = c.P
        idea = T("THE ONE IDEA", 28, GOLD, weight=BOLD).move_to([3.7, 3.2, 0])
        head = T("typical bipolar climb", 32, GREYL).move_to([3.7, 2.3, 0])
        l1 = T("The front goes first.", 44, TEXT, weight=BOLD).move_to([3.7, 0.9, 0])
        l2 = VGroup(T("The cell has moved only", 32, TEXT), T("when its nucleus catches up.", 32, TEXT,
                                                              t2c={"nucleus": ORANGE})).arrange(DOWN, buff=0.15)
        l2.move_to([3.7, -1.0, 0])
        if l2.width > 5.9:
            l2.scale(5.9 / l2.width)
        rule = [idea, head, l1, l2]
        for m in rule:
            m.set_opacity(0.3)
        self.play(*[FadeIn(m) for m in rule],
                  *c.to(x=self.X, y0=CYC["y0"], tail=REST["tail"],
                        soma=REST["soma"], ws=0.0, cs=REST_CS, csx=REST_CSX), run_time=1.0)
        y_old = c.nuc_y()
        self.at("one idea")
        self.play(idea.animate.set_opacity(1), run_time=0.5)
        self.at("typical bipolar")
        self.play(head.animate.set_opacity(1), run_time=0.5)
        self.at("front goes first")
        self.play(l1.animate.set_opacity(1), *c.to(ws=ONE["ws"], cs=ONE["cs"], csx=ONE["csx"]), run_time=1.4)

        ref = DashedLine([self.X - 1.5, y_old, 0], [self.X + 1.5, y_old, 0], color=GREYL, stroke_width=4,
                         dash_length=0.12)
        self.at("cell has moved")
        self.play(l2.animate.set_opacity(1), Create(ref), run_time=0.9)
        self.at("nucleus catches")
        self.play(*c.to(soma=TWO["soma"], ws=0.0), run_time=1.0)
        y_new = c.nuc_y()
        moved = DoubleArrow([self.X + 1.2, y_old, 0], [self.X + 1.2, y_new, 0], color=ORANGE, stroke_width=6,
                            tip_length=0.25, buff=0)
        ml = VGroup(T("nucleus", 26, ORANGE), T("has moved", 26, ORANGE)).arrange(DOWN, buff=0.06,
                                                                                 aligned_edge=LEFT)
        ml.move_to([self.X + 1.5 + ml.width / 2, (y_old + y_new) / 2, 0])
        self.play(GrowFromCenter(moved), FadeIn(ml, shift=RIGHT * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tissue_grid():
    g = VGroup()
    for y in np.arange(-3.6, 3.7, 0.9):
        g.add(Line([-6.6, y, 0], [6.6, y, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.25))
    for x in np.arange(-6.6, 6.7, 1.2):
        g.add(Line([x, -3.6, 0], [x, 3.6, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.25))
    return g


def tick_mark(cx, cy, color=GREEN, s=1.0, w=9):
    return VGroup(Line([cx - 0.3 * s, cy - 0.02 * s, 0], [cx - 0.1 * s, cy - 0.25 * s, 0], color=color, stroke_width=w),
                  Line([cx - 0.1 * s, cy - 0.25 * s, 0], [cx + 0.35 * s, cy + 0.3 * s, 0], color=color, stroke_width=w))


class S17Tip(Sp):
    """two neurons against a fixed grid of tissue: in one the tip grows while the nucleus stays put."""
    GEO = dict(sc=1.2, y0=0.88)
    S = dict(soma=-2.4, tip=0.5, tail=-3.2, cs_op=0.0, op=1.0)
    TIP_END = 1.9

    def construct(self):
        grid = tissue_grid()
        grid.set_z_index(-5)
        self.add(grid)
        xl, xr = -4.0, 1.8
        cl = Cell(x=xl, **self.GEO, **self.S)
        cr = Cell(x=xr, **self.GEO, **self.S)
        self.add(cl.mob, cr.mob)
        ly = cl.nuc_y()
        ref_l = DashedLine([xl - 1.0, ly, 0], [xl + 1.0, ly, 0], color=ORANGE, stroke_width=4, dash_length=0.16)
        ref_r = DashedLine([xr - 1.0, ly, 0], [xr + 1.0, ly, 0], color=ORANGE, stroke_width=4, dash_length=0.16)
        ref_l.set_z_index(5)
        ref_r.set_z_index(5)
        self.play(Create(ref_l), Create(ref_r), run_time=0.3)

        self.at("tip can keep")
        self.play(*cl.to(tip=self.TIP_END), *cr.to(tip=self.TIP_END), run_time=1.3)
        cross = VGroup(Line([xl + 1.3, ly - 0.35, 0], [xl + 1.95, ly + 0.35, 0], color=RED, stroke_width=9),
                       Line([xl + 1.3, ly + 0.35, 0], [xl + 1.95, ly - 0.35, 0], color=RED, stroke_width=9))
        nm = chipfix("not migration", RED, 26)
        nm.move_to([xl + 2.2 + nm.width / 2, ly, 0])
        self.at("stays put")
        self.play(FadeIn(cross, scale=0.6), FadeIn(nm, shift=UP * 0.1), run_time=0.5)

        self.at("so track")
        self.play(*cr.to(soma=-0.9), run_time=0.7)
        yn = cr.nuc_y()
        mv = Arrow([xr + 1.15, ly, 0], [xr + 1.15, yn, 0], color=ORANGE, stroke_width=7, tip_length=0.3, buff=0)
        self.play(GrowArrow(mv), run_time=0.3)
        ok = VGroup(tick_mark(xr + 2.0, (ly + yn) / 2, GREEN, 1.0), T("migration", 28, GREEN, weight=BOLD))
        ok[1].move_to([xr + 2.45 + ok[1].width / 2, (ly + yn) / 2, 0])
        tl = chipfix("tissue", GREYL, 26)
        tl.move_to([6.6 - 0.1 - tl.width / 2, 3.3, 0])
        self.at("against the tissue")
        self.play(FadeIn(tl, shift=DOWN * 0.1), FadeIn(ok, shift=UP * 0.1), grid.animate.set_stroke(opacity=0.6),
                  run_time=0.7)
        self.play(grid.animate.set_stroke(opacity=0.25), run_time=0.4)
        tips = [ring(cl.P(0, self.TIP_END), BLUE, r=0.3, w=4), ring(cr.P(0, self.TIP_END), BLUE, r=0.3, w=4)]
        self.at("not the tip")
        self.play(*[FadeIn(t, scale=1.8) for t in tips], run_time=0.4)
        self.play(*[FadeOut(t) for t in tips], run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18Speed(Sp):
    """a ruler and a clock: 6 micrometres a step, 4 steps an hour, 24 micrometres an hour."""
    NY = [-2.2, -1.3, -0.4, 0.5, 1.4]     # nucleus height after 0, 1, 2, 3, 4 steps (screen y)
    SC = 1.9
    CX = -4.4
    RX = -2.9
    CLK = np.array([3.8, 1.55, 0.0])

    def kw(self, k):
        ny = self.NY[k]
        return dict(soma=ny / self.SC - Cell.NUC_DY, tail=(ny - 1.3) / self.SC, tip=min(3.3, ny + 3.2) / self.SC)

    def cell(self, k):
        return Cell(x=self.CX, y0=0.0, sc=self.SC, cs_op=0.0, op=1.0, **self.kw(k))

    def ruler(self):
        g = VGroup(Line([self.RX, self.NY[0], 0], [self.RX, self.NY[4], 0], color=TEXT, stroke_width=4))
        labs = VGroup()
        for k, y in enumerate(self.NY):
            g.add(Line([self.RX - 0.14, y, 0], [self.RX + 0.14, y, 0], color=TEXT, stroke_width=4))
            labs.add(M(str(6 * k), 26, GREYL).move_to([self.RX + 0.55, y, 0]))
        unit = T("µm", 26, GREYL).move_to([self.RX + 0.1, self.NY[4] + 0.5, 0])
        return g, labs, unit

    def clock(self):
        face = Circle(radius=1.5, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(
            self.CLK)
        ticks = VGroup(*[Line(self.CLK + 1.35 * np.array([np.sin(a), np.cos(a), 0]),
                              self.CLK + 1.5 * np.array([np.sin(a), np.cos(a), 0]), color=TEXT, stroke_width=4)
                         for a in np.deg2rad([0, 90, 180, 270])])
        return VGroup(face, ticks)

    def hand(self, ang):
        a = np.deg2rad(ang)
        return Line(self.CLK, self.CLK + 1.15 * np.array([np.sin(a), np.cos(a), 0]), color=TEXT, stroke_width=6)

    def texts(self):
        eq1 = M("6 µm per step", 38, TEXT).move_to([3.8, -0.4, 0])
        eq2 = T("× 4 steps an hour", 38, TEXT).move_to([3.8, -1.2, 0])
        eq3 = M("= 24 µm an hour", 38, ORANGE).move_to([3.8, -2.2, 0])
        rule = Line([1.6, -1.65, 0], [6.0, -1.65, 0], color=GREY, stroke_width=3)
        ex = chip("example values", GOLD, size=26).move_to([3.8, -3.1, 0])
        hour_l = T("one hour", 26, GREYL).move_to(self.CLK + np.array([0, 1.95, 0]))
        return eq1, eq2, eq3, rule, ex, hour_l

    def brackets(self):
        b1 = Arrow([self.RX + 1.1, self.NY[0], 0], [self.RX + 1.1, self.NY[1], 0], color=ORANGE,
                         stroke_width=5, tip_length=0.2, buff=0)
        tot = Arrow([self.RX + 1.6, self.NY[0], 0], [self.RX + 1.6, self.NY[4], 0], color=ORANGE,
                          stroke_width=6, tip_length=0.25, buff=0)
        return b1, tot

    def construct(self):
        c = self.cell(0)
        self.add(c.mob)
        rl, rlab, unit = self.ruler()
        clk = self.clock()
        k_tr = ValueTracker(0.0)    # quarter-hours elapsed
        hand = always_redraw(lambda: self.hand(90 * k_tr.get_value()))
        eq1, eq2, eq3, rule, ex, hour_l = self.texts()
        b1, tot = self.brackets()
        self.play(Create(rl), FadeIn(rlab), FadeIn(unit), FadeIn(clk), FadeIn(hand), run_time=0.8)

        def step(k):
            return [*c.to(**self.kw(k)), k_tr.animate.set_value(k)]

        # the first step, slowly, with its 0 to 6 bracket and the clock moving to a quarter
        self.play(*step(1), GrowFromCenter(b1), run_time=1.8)
        self.at("micrometers")
        self.play(FadeIn(eq1, shift=UP * 0.1), run_time=0.5)
        self.at("four steps", lead=0.3)
        self.play(*step(2), run_time=0.5)
        self.at("steps an hour", lead=0.15)
        self.play(*step(3), FadeIn(eq2, shift=UP * 0.1), FadeIn(hour_l), run_time=0.5)
        self.play(*step(4), Create(rule), run_time=0.5)
        self.at("gives")
        self.play(FadeIn(eq3, shift=UP * 0.1), GrowFromCenter(tot), run_time=0.7)
        self.at("micrometers an hour")
        self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S19Beat(S18Speed):
    """a beat: the finished measurement holds still."""

    def construct(self):
        c = self.cell(4)
        self.add(c.mob)
        rl, rlab, unit = self.ruler()
        clk = self.clock()
        hand = self.hand(360)
        eq1, eq2, eq3, rule, ex, hour_l = self.texts()
        b1, tot = self.brackets()
        self.add(rl, rlab, unit, clk, hand, hour_l, eq1, eq2, eq3, rule, ex, b1, tot)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20Take(Sp):
    """closing card: follow the nucleus, not the tip. A matched pair above one line of text."""

    def construct(self):
        disc = Ellipse(width=1.5, height=2.0, stroke_color=ORANGE, stroke_width=6, fill_color=ORANGE,
                       fill_opacity=0.55)
        tipd = Dot(radius=0.45, color=BLUE)
        cross = VGroup(Line([-0.7, -0.7, 0], [0.7, 0.7, 0], color=RED, stroke_width=10),
                       Line([-0.7, 0.7, 0], [0.7, -0.7, 0], color=RED, stroke_width=10))
        crossed_tip = VGroup(tipd, cross)
        pair = VGroup(disc, crossed_tip).arrange(RIGHT, buff=1.0).move_to([0, 1.0, 0])
        line = T("Follow the nucleus, not the tip.", 48, TEXT, font=TITLE_FONT)
        fit(line, max_w=11.8)
        line.move_to([0, -1.0, 0])
        # Complete the matched icons before any of the single-line takeaway appears.
        self.play(FadeIn(disc, scale=0.6), FadeIn(tipd, scale=0.6), run_time=0.25)
        self.play(Create(cross), run_time=0.25)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.4)
        self.finish()


class S21End(EndCard):
    LINE = "The cell has moved only when its nucleus catches up."
