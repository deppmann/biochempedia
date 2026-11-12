"""Landis's Blocked Capillary (film 2 of Blood Vessels, Blood and Lymph).

Same look as film 1 (../scenes.py): dark ground, one colour per concept.
COLOR MAP
  ORANGE = hydrostatic push (pressure)   BLUE  = oncotic pull (plasma proteins, albumin)
  RED    = red cells                     GREEN = lymph
  SLATE  = capillary wall (charcoal)     GOLD  = highlights, questions
  GLASS  = pipette and rod               WATER = small white droplets
Capillary world: horizontal tube, wall at y = +-0.75, x -5.6..5.0 (film 1's closing picture).
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B07CE0"
SLATE = "#7A86A3"
TAN = "#C9A66B"
GLASS = "#BFD7EA"
WATER = "#EAF2FA"

CX0, CX1 = -5.6, 5.0     # capillary wall extent
CH = 2.4                  # capillary height (film 1's closing tube, made taller to fill the frame)


# ------------------------------------------------------------------ helpers
def L(text, size=30, color=TEXT, **kw):
    """Label with a dark halo so it stays readable over moving cells."""
    t = T(text, size, color, **kw)
    t.set_stroke(BG, 6, background=True)
    return t


def sub(base, s, size=34, color=TEXT):
    a = T(base, size, color)
    b = T(s, max(22, int(size * 0.7)), color)
    b.next_to(a, RIGHT, buff=0.02).shift(DOWN * 0.1)
    return VGroup(a, b)


def row(*parts, buff=0.14):
    return VGroup(*parts).arrange(RIGHT, buff=buff, aligned_edge=DOWN)


def wall(y=0.0, x0=CX0, x1=CX1, h=CH, color=SLATE, solid=False):
    fill = Rectangle(width=x1 - x0, height=h, stroke_width=0, fill_color=color, fill_opacity=0.12).move_to([(x0 + x1) / 2, y, 0])
    if solid:
        edges = VGroup(Line([x0, y + h / 2, 0], [x1, y + h / 2, 0]), Line([x0, y - h / 2, 0], [x1, y - h / 2, 0])).set_stroke(color, 7)
    else:
        edges = VGroup(DashedLine([x0, y + h / 2, 0], [x1, y + h / 2, 0], dash_length=0.32, dashed_ratio=0.62),
                       DashedLine([x0, y - h / 2, 0], [x1, y - h / 2, 0], dash_length=0.32, dashed_ratio=0.62)).set_stroke(color, 7)
    return VGroup(fill, edges)


def cells(y, flow, x0=-5.4, x1=4.5, hh=0.9, n=17, seed=1, r=0.15, color=RED, ramp=0.6, blk=None):
    """Red cells (or other dots) carried along a tube; flow() is units per second, may be negative."""
    rnd = random.Random(seed)
    g = VGroup()
    Ln = x1 - x0
    for k in range(n):
        d = Dot(radius=r, color=color)
        d.px = x0 + (k + rnd.random() * 0.7 + 0.15) * Ln / n
        d.j = rnd.uniform(-1, 1)

        def up(m, dt):
            m.px += flow() * dt
            if m.px > x1:
                m.px -= Ln
            if m.px < x0:
                m.px += Ln
            m.move_to([m.px, y + m.j * hh, 0])
            op = min(1.0, (m.px - x0) / ramp, (x1 - m.px) / ramp)
            if blk is not None and blk() > 0.5:
                op = 1.0
            m.set_opacity(max(0.0, op))
        d.add_updater(up)
        up(d, 0)
        g.add(d)
    return g


def seep(y, h, xs, rate, direction, seed=2, color=WATER, reach=1.15, r=0.09, speed=0.5, sides=(1, -1)):
    """Droplets crossing the wall at the given x positions; rate() gates opacity, direction() is +1 out, -1 in."""
    rnd = random.Random(seed)
    g = VGroup()
    for x in xs:
        for s in sides:
            d = Dot(radius=r, color=color)
            d.ph = rnd.random()
            d.x = x + rnd.uniform(-0.2, 0.2)
            d.s = s

            def up(m, dt):
                m.ph = (m.ph + dt * speed) % 1.0
                p = m.ph if direction() > 0 else 1.0 - m.ph
                m.move_to([m.x, y + m.s * (h / 2 + 0.12 + reach * p), 0])
                m.set_opacity(max(0.0, rate()) * math.sin(PI * m.ph))
            d.add_updater(up)
            up(d, 0)
            g.add(d)
    return g


def breathe(mob, amp=0.3, speed=2.2, base=0.85):
    st = {"t": 0.0}

    def up(m, dt):
        st["t"] += dt
        m.set_opacity(min(1.0, base + amp * math.sin(st["t"] * speed)))
    mob.add_updater(up)
    return mob


def arr(x, y0, y1, color, w=8, tip=0.26):
    return Arrow([x, y0, 0], [x, y1, 0], color=color, buff=0, stroke_width=w, tip_length=tip, max_tip_length_to_length_ratio=0.5)


def push_arrows(xs=(-3.6, -1.2, 1.2, 3.6), y=0.0, h=CH, length=1.4, color=ORANGE, w=8, outward=True):
    g = VGroup()
    for x in xs:
        for s in (1, -1):
            a = y + s * (h / 2 - 0.55)
            b = a + s * length
            g.add(arr(x, a if outward else b, b if outward else a, color, w))
    return g


def pipette(x, y_tip, y_top=3.9):
    return Polygon([x - 0.12, y_top, 0], [x + 0.12, y_top, 0], [x + 0.12, y_tip + 0.6, 0], [x + 0.025, y_tip, 0],
                   [x - 0.025, y_tip, 0], [x - 0.12, y_tip + 0.6, 0], stroke_color=GLASS, stroke_width=3,
                   fill_color=GLASS, fill_opacity=0.35)


def rod(x, y_bot, y_top=3.9):
    return RoundedRectangle(corner_radius=0.12, width=0.34, height=y_top - y_bot, stroke_color=GLASS, stroke_width=3,
                            fill_color=GLASS, fill_opacity=0.35).move_to([x, (y_top + y_bot) / 2, 0])


def gauge_bar(cx, cy, w, h, tr, color=ORANGE, jitter=0.0):
    box = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3)
    box.move_to([cx, cy, 0])
    st = {"t": 0.0}

    def fill():
        st["t"] += 0.03
        v = max(0.02, min(1.0, tr.get_value() + jitter * math.sin(st["t"] * 9)))
        return Rectangle(width=w * v, height=h - 0.06, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to(
            [cx - w / 2 + w * v / 2, cy, 0])
    return box, always_redraw(fill)


def balance(cx, cy, half, wp, wq, sway=None, push_label="push", pull_label="pull", with_weights=True, ww=1.15, fs=28):
    """Balance scale. wp (orange push) and wq (blue pull) are trackers; the heavier side sinks."""
    def build():
        a = wp.get_value() - wq.get_value()
        th = max(-0.3, min(0.3, 0.14 * a))
        if sway is not None:
            th += 0.035 * math.sin(sway.get_value())
        ex = half * math.cos(th)
        ey = half * math.sin(th)
        lt = np.array([cx - ex, cy - ey, 0.0])
        rt = np.array([cx + ex, cy + ey, 0.0])
        g = VGroup()
        g.add(Line(lt, rt).set_stroke(TEXT, 8))
        g.add(Dot([cx, cy, 0], radius=0.14, color=GOLD))
        for e, w, col, lab in ((lt, wp, ORANGE, push_label), (rt, wq, BLUE, pull_label)):
            pan = e + DOWN * 1.0
            g.add(Line(e, pan + LEFT * (ww / 2)).set_stroke(GREY, 3), Line(e, pan + RIGHT * (ww / 2)).set_stroke(GREY, 3))
            g.add(Line(pan + LEFT * (ww / 2 + 0.1), pan + RIGHT * (ww / 2 + 0.1)).set_stroke(TEXT, 7))
            if with_weights:
                hh = 0.42 + 0.26 * max(0.0, w.get_value())
                bx = RoundedRectangle(corner_radius=0.08, width=ww, height=hh, stroke_color=col, stroke_width=3,
                                      fill_color=col, fill_opacity=0.7).move_to(pan + UP * (hh / 2 + 0.04))
                g.add(bx, T(lab, fs, TEXT, weight=BOLD).move_to(bx))
        return g
    return always_redraw(build)


def post(cx, cy, base_y):
    return VGroup(Line([cx, cy, 0], [cx, base_y, 0]).set_stroke(SLATE, 10),
                  Line([cx - 0.9, base_y, 0], [cx + 0.9, base_y, 0]).set_stroke(SLATE, 12))


# ------------------------------------------------------------------ the plot of Landis's data
GX, GY, GW, GH = 0.6, -0.65, 9.4, 4.6     # graph centre and size (large version)
PM = 0.35                                   # oncotic pull of frog plasma, schematic units
RIGHT_P = [0.43, 0.52, 0.61, 0.70, 0.80, 0.90]
LEFT_P = [0.05, 0.12, 0.19, 0.26, 0.31]


def Jrate(p):
    return 1.0 * (p - PM)


def make_axes(cx=GX, cy=GY, w=GW, h=GH):
    ax = Axes(x_range=[0, 1, 0.5], y_range=[-0.5, 1.0, 0.5], x_length=w, y_length=h, tips=False,
              axis_config={"include_numbers": False, "include_ticks": False, "stroke_color": GREY, "stroke_width": 3}).move_to([cx, cy, 0])
    return ax


def data_pts(ax, ps, seed):
    rnd = random.Random(seed)
    out = []
    for p in ps:
        j = Jrate(p) + rnd.uniform(-0.035, 0.035)
        out.append((p, ax.c2p(p, j)))
    return out


class PlotBase(SpokenScene):
    """The pipette strip on top and the big graph below, rebuilt in the same place for scenes 9 to 12."""
    SX0, SX1, SY = -5.0, 1.0, 3.0

    def strip(self, drift=0.35):
        self.sw = wall(self.SY, self.SX0, self.SX1, 0.72, solid=True)
        self.rodm = rod(self.SX1 - 0.15, self.SY - 0.36, 3.7)
        self.tip = pipette(-2.5, self.SY - 0.1, 3.7)
        self.P = ValueTracker(0.5)
        self.dr = ValueTracker(drift)
        self.sc = cells(self.SY, lambda: self.dr.get_value(), self.SX0 + 0.2, self.SX1 - 0.4, 0.2, n=9, seed=5, r=0.09, ramp=0.4)
        box, fill = gauge_bar(4.05, 2.85, 3.4, 0.38, self.P, ORANGE, 0.012)
        self.rd = VGroup(box, fill)
        self.rdl = L("pressure", 28, ORANGE).move_to([4.05, 3.4, 0])
        self.add(self.P, self.dr, self.sw, self.rodm, self.tip, self.sc, self.rd, self.rdl)

    def graph(self, right=True, left=False, line=False, marker=False):
        self.ax = make_axes()
        ax = self.ax
        self.xl = T("capillary pressure", 28).move_to([GX, -3.55, 0])
        self.yl = T("fluid crossing the wall", 28).rotate(PI / 2).move_to([GX - GW / 2 - 0.55, GY, 0])
        self.outl = T("out (+)", 24, GREY).move_to(ax.c2p(0.0, 0.95) + RIGHT * 0.65)
        self.inl = T("in (−)", 24, GREY).move_to(ax.c2p(0.0, -0.45) + RIGHT * 0.6)
        self.sch = T("schematic points", 24, GREY).move_to([GX + 3.6, -3.55, 0])
        self.add(ax, self.xl, self.yl, self.outl, self.inl, self.sch)
        self.dotsR = VGroup(*[Dot(pt, radius=0.1, color=TEXT) for _, pt in data_pts(ax, RIGHT_P, 11)])
        self.dotsL = VGroup(*[Dot(pt, radius=0.1, color=TEXT) for _, pt in data_pts(ax, LEFT_P, 12)])
        if right:
            self.add(self.dotsR)
        if left:
            self.add(self.dotsL)
        self.fit = Line(ax.c2p(0.02, Jrate(0.02)), ax.c2p(1.0, Jrate(1.0))).set_stroke(GOLD, 6)
        if line:
            self.add(self.fit)
        self.mk = Line(ax.c2p(PM, -0.5), ax.c2p(PM, 1.0)).set_stroke(BLUE, 6)
        self.mkl = L("oncotic pull of frog plasma", 28, BLUE).move_to(ax.c2p(PM, 0.97) + RIGHT * 2.6)
        if marker:
            self.add(self.mk, self.mkl)
        # shaded region left of the marker (the question region)
        self.shade = Rectangle(width=ax.c2p(PM, 0)[0] - ax.c2p(0, 0)[0], height=GH, stroke_width=0, fill_color=GOLD, fill_opacity=0.09
                               ).move_to([(ax.c2p(PM, 0)[0] + ax.c2p(0, 0)[0]) / 2, GY, 0])
        self.card = VGroup(T("which way will", 30, GOLD, weight=BOLD), T("fluid go?", 30, GOLD, weight=BOLD)).arrange(DOWN, buff=0.12)
        self.card.move_to([self.shade.get_center()[0], GY + 1.0, 0])


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Blood Vessels, Blood and Lymph"
    TITLE = "Landis's Blocked Capillary"

    def construct(self):
        faint = VGroup(wall(0.0, solid=False))
        faint.set_opacity(0.16)
        self.add(faint)
        super().construct()


class S01Hook(SpokenScene):
    def construct(self):
        w = wall()
        flow = ValueTracker(1.1)
        rate = ValueTracker(0.0)
        dr = ValueTracker(1.0)
        rc = cells(0.0, lambda: flow.get_value(), seed=1)
        sp = seep(0.0, CH, [-4.4, -2.4, -0.4, 1.6, 3.6], lambda: rate.get_value(), lambda: dr.get_value(), seed=3)
        self.add(flow, rate, dr)
        self.play(Create(w[1]), FadeIn(w[0]), run_time=0.6)
        self.add(rc, sp)
        self.play(FadeIn(rc), rate.animate.set_value(1.0), run_time=0.6)
        self.at("water")
        tis = L("tissue", 30, TEXT).move_to([-5.9, 2.75, 0])
        self.play(FadeIn(tis), run_time=0.5)
        self.at("small solutes")
        lk = L("water and small solutes leak out", 32, TEXT).move_to([0.0, -3.4, 0])
        self.play(FadeIn(lk, shift=UP * 0.1), run_time=0.6)
        self.at("So why")
        lvl = ValueTracker(1.0)
        gb = Rectangle(width=0.7, height=5.6, stroke_color=GREY, stroke_width=3).move_to([6.25, -0.2, 0])
        gf = always_redraw(lambda: Rectangle(width=0.62, height=5.5 * lvl.get_value(), stroke_width=0, fill_color=RED, fill_opacity=0.75
                                             ).move_to([6.25, -2.95 + 2.75 * lvl.get_value(), 0]))
        gl = L("plasma", 28, RED).move_to([6.25, -3.35, 0])
        self.add(lvl)
        self.play(FadeOut(lk), FadeIn(gb), FadeIn(gf), FadeIn(gl), run_time=0.7)
        self.at("end up")
        self.play(lvl.animate.set_value(0.5), run_time=2.6, rate_func=linear)
        self.at("Something")
        q = chip("What holds plasma in?", GOLD, 36, fill_opacity=0.2).move_to([-0.3, 3.25, 0])
        self.play(FadeIn(q, scale=1.25), run_time=0.6)
        self.play(Indicate(q, color=GOLD, scale_factor=1.08), run_time=1.0)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        eq = row(T("Q = (P", 40, TEXT), T("in", 26, TEXT), T("− P", 40, TEXT), T("out", 26, TEXT), T(") / R", 40, TEXT), buff=0.04)
        eq[1].shift(DOWN * 0.07)
        eq[3].shift(DOWN * 0.07)
        eq.move_to([-6.6 + eq.width / 2, 3.35, 0])
        w = wall(solid=True)
        flow = ValueTracker(1.4)
        rc = cells(0.0, lambda: flow.get_value(), seed=2)
        self.add(flow, w, rc)
        self.play(Write(eq), run_time=1.6)
        self.at("pressure difference")
        pl = Line([-5.0, 2.45, 0], [4.4, 1.75, 0]).set_stroke(ORANGE, 8)
        pin = L("P in", 30, ORANGE).move_to([-5.0, 2.8, 0])
        pout = L("P out", 30, ORANGE).move_to([4.4, 2.2, 0])
        self.play(Create(pl), FadeIn(pin), FadeIn(pout), run_time=1.4)
        self.at("divided by")
        blk = Rectangle(width=0.9, height=2.0, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.8).move_to([0.2, 0.0, 0])
        rl = T("R", 34, TEXT, weight=BOLD).move_to(blk)
        self.play(FadeIn(VGroup(blk, rl), shift=DOWN * 0.1), run_time=0.7)
        self.at("Across")
        self.play(FadeOut(VGroup(blk, rl)), FadeOut(pl), run_time=0.8)
        da = DoubleArrow([-2.2, 0.0, 0], [-2.2, 2.2, 0], color=ORANGE, buff=0, stroke_width=8, tip_length=0.25)
        self.play(GrowArrow(da), Transform(pin, L("inside", 32, ORANGE).move_to([-1.0, 0.0, 0])),
                  Transform(pout, L("outside", 32, ORANGE).move_to([-0.9, 2.2, 0])), run_time=1.1)
        self.at("same rule")
        self.play(Indicate(eq, color=GOLD, scale_factor=1.06), run_time=0.8)
        self.at("which way")
        q = T("?", 90, GOLD, weight=BOLD).move_to([1.6, 2.2, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.6)
        self.play(Indicate(q, color=GOLD, scale_factor=1.25), run_time=1.0)
        self.finish()


class S03Push(SpokenScene):
    def construct(self):
        w = wall()
        flow = ValueTracker(1.1)
        rate = ValueTracker(0.0)
        rc = cells(0.0, lambda: flow.get_value(), seed=1)
        sp = seep(0.0, CH, [-4.4, -2.4, -0.4, 1.6, 3.6], lambda: rate.get_value(), lambda: 1.0, seed=3)
        tis = L("tissue", 30, TEXT).move_to([-5.9, 2.75, 0])
        self.add(flow, rate, w, rc, sp, tis)
        self.wait(0.6)
        self.at("The first")
        self.play(Indicate(rc, color=GOLD, scale_factor=1.0), run_time=0.8)
        self.at("blood pressure")
        big = push_arrows()
        pc = row(T("P", 36, ORANGE), T("c", 26, ORANGE)).move_to([-0.1, 0.0, 0])
        pc.set_stroke(BG, 6, background=True)
        pc.set_z_index(20)
        self.play(LaggedStart(*[GrowArrow(a) for a in big], lag_ratio=0.1), run_time=1.3)
        self.play(FadeIn(pc), run_time=0.5)
        breathe(big)
        self.at("minus")
        small = VGroup(*[arr(x, s * 2.95, s * 1.65, ORANGE, 6, 0.2) for x in (-2.4, 0.0, 2.4) for s in (1, -1)])
        pi_ = row(T("P", 34, ORANGE), T("i", 24, ORANGE)).move_to([4.4, 2.55, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in small], lag_ratio=0.12), FadeIn(pi_), run_time=1.3)
        breathe(small, base=0.8)
        self.at("It pushes")
        lab = VGroup(T("push:", 36, ORANGE, weight=BOLD), sub("P", "c", 36, ORANGE), sub("− P", "i", 36, ORANGE)).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        lab.move_to([-0.3, 3.45, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), rate.animate.set_value(1.0), run_time=1.0)
        self.at("outward")
        self.play(Indicate(big, color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("Physiologists")
        hp = chip("hydrostatic pressure", ORANGE, 34, fill_opacity=0.2).move_to([0.0, -3.4, 0])
        self.play(FadeIn(hp, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S04Pull(SpokenScene):
    def construct(self):
        w = wall()
        flow = ValueTracker(1.0)
        rate = ValueTracker(1.0)
        rc = cells(0.0, lambda: flow.get_value(), seed=1, n=11)
        big = push_arrows()
        big.set_opacity(0.4)
        lab = VGroup(T("push:", 36, ORANGE, weight=BOLD), sub("P", "c", 36, ORANGE), sub("− P", "i", 36, ORANGE)).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        lab.move_to([-0.3, 3.45, 0])
        lab.set_opacity(0.5)
        tis = L("tissue", 30, TEXT).move_to([-5.9, 2.75, 0])
        sp = seep(0.0, CH, [-4.4, -2.4, -0.4, 1.6, 3.6], lambda: rate.get_value(), lambda: 1.0, seed=3)
        self.add(flow, rate, w, rc, sp, big, lab, tis)
        self.wait(0.4)
        self.at("plasma proteins")
        alb = cells(0.0, lambda: 0.6 * flow.get_value(), seed=8, n=13, r=0.16, color=BLUE, hh=0.85)
        self.play(FadeIn(alb), run_time=0.8)
        self.at("mostly albumin")
        al = L("albumin", 34, BLUE).move_to([-5.3, 2.2, 0])
        self.play(FadeIn(al), run_time=0.6)
        self.at("Few cross")
        coat = VGroup(*[DashedLine([CX0, s * (CH / 2 - 0.1), 0], [CX1, s * (CH / 2 - 0.1), 0], dash_length=0.12, dashed_ratio=0.5).set_stroke(TAN, 9) for s in (1, -1)])
        coat.set_opacity(0.55)
        self.play(FadeIn(coat), run_time=0.6)
        # two albumin molecules slip through; a few sit in the tissue already
        slip = VGroup(*[Dot(radius=0.13, color=BLUE) for _ in range(2)])
        for k, d in enumerate(slip):
            d.k = k
            d.t = 0.0

            def up(m, dt):
                m.t += dt * 0.35
                p = (m.t % 1.0)
                m.move_to([1.0 + 2.2 * m.k, 0.3 + 2.3 * p * (1 if m.k == 0 else -1), 0])
                m.set_opacity(math.sin(PI * min(1.0, p * 1.0)) * 0.9 + 0.1)
            d.add_updater(up)
            up(d, 0)
        tp = VGroup(Dot([-2.9, 2.6, 0], radius=0.16, color=BLUE), Dot([3.9, 2.7, 0], radius=0.16, color=BLUE),
                    Dot([-3.3, -2.7, 0], radius=0.16, color=BLUE))
        few = L("few cross", 32, BLUE).move_to([5.4, 2.9, 0])
        self.play(FadeIn(slip), FadeIn(tp), FadeIn(few), run_time=0.9)
        self.at("pull water")
        bl = VGroup(*[arr(x, s * 3.0, s * 0.8, BLUE, 8) for x in (-2.4, 0.0, 2.4) for s in (1, -1)])
        self.play(FadeOut(few), LaggedStart(*[GrowArrow(a) for a in bl], lag_ratio=0.1), big.animate.set_opacity(0.9), run_time=1.5)
        breathe(bl)
        self.at("Protein outside")
        self.play(Indicate(tp, color=BLUE, scale_factor=1.5), run_time=1.3)
        small = VGroup(*[Arrow([x, s * 1.7, 0], [x, s * 2.2, 0], color=BLUE, buff=0, stroke_width=5, tip_length=0.18) for x in (-3.6,) for s in (1,)])
        self.at("difference counts")
        pl = VGroup(T("pull:", 36, BLUE, weight=BOLD), sub("π", "c", 36, BLUE), T("− π outside", 36, BLUE)).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        pl.move_to([0.0, -3.5, 0])
        self.play(FadeIn(pl, shift=UP * 0.1), run_time=0.8)
        self.at("oncotic pressure")
        oc = chip("oncotic pressure", BLUE, 34, fill_opacity=0.2).move_to([-0.3, 3.45, 0])
        self.play(FadeOut(lab), FadeIn(oc, shift=DOWN * 0.1), run_time=0.8)
        self.play(Indicate(bl, color=GOLD, scale_factor=1.0), run_time=1.2)
        self.finish()


class S05Starling(SpokenScene):
    def construct(self):
        wp, wq, sw = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        bal = balance(0.0, 1.4, 4.2, wp, wq, sw, ww=1.7, fs=34)
        pst = post(0.0, 1.4, -1.0)
        self.add(wp, wq, sw)
        sw.add_updater(lambda m, dt: m.increment_value(dt * 1.6))
        self.play(Create(pst), FadeIn(bal), run_time=0.6)
        self.at("1896")
        yr = T("1896", 44, GOLD, weight=BOLD).move_to([0.0, 3.35, 0])
        self.play(FadeIn(yr, scale=1.2), run_time=0.6)
        self.at("Ernest")
        nm = T("Ernest Starling,", 44, TEXT).next_to(yr, LEFT, buff=0.25)
        self.play(FadeIn(nm, shift=RIGHT * 0.2), run_time=0.6)
        self.at("argued")
        self.play(wp.animate.set_value(1.0), wq.animate.set_value(1.0), run_time=1.4)
        self.at("direction of flow")
        self.play(Indicate(bal, color=GOLD, scale_factor=1.0), run_time=1.0)
        self.at("but neither")
        cy = -2.85
        cap = wall(cy, -4.2, 3.4, 1.0, solid=True)
        fl = ValueTracker(0.9)
        rc = cells(cy, lambda: fl.get_value(), -4.0, 3.2, 0.3, n=11, seed=4, r=0.11, ramp=0.4)
        gc = Circle(radius=0.7, stroke_color=GOLD, stroke_width=5).move_to([5.3, cy, 0])
        gq = T("?", 64, GOLD, weight=BOLD).move_to(gc)
        self.add(fl)
        self.play(Create(cap), FadeIn(rc), run_time=0.9)
        self.play(FadeIn(gc), FadeIn(gq, scale=1.3), run_time=0.7)
        self.at("single capillary")
        self.play(Indicate(cap, color=GOLD, scale_factor=1.0), Indicate(gq, color=GOLD, scale_factor=1.3), run_time=1.4)
        self.finish()


def frog():
    body = Ellipse(width=2.9, height=1.7, stroke_color=TEXT, stroke_width=4, fill_color=GREEN, fill_opacity=0.12)
    head = Circle(radius=0.55, stroke_color=TEXT, stroke_width=4, fill_color=GREEN, fill_opacity=0.12).move_to([1.5, 0.35, 0])
    eye = Dot([1.7, 0.7, 0], radius=0.09, color=TEXT)
    leg = VMobject().set_points_as_corners([[-1.0, -0.6, 0], [-1.9, -1.4, 0], [-0.8, -1.5, 0], [-0.2, -0.75, 0]]).set_stroke(TEXT, 4)
    leg2 = VMobject().set_points_as_corners([[0.6, -0.7, 0], [1.0, -1.5, 0], [1.9, -1.4, 0]]).set_stroke(TEXT, 4)
    return VGroup(body, head, eye, leg, leg2)


class S06Landis(SpokenScene):
    def construct(self):
        fr = frog().scale(1.3).move_to([-4.1, 0.3, 0])
        self.play(Create(fr), run_time=1.6)
        self.at("Eugene")
        yr = T("1927", 44, GOLD, weight=BOLD).move_to([0.0, 3.35, 0])
        nm = T("Eugene Landis,", 44, TEXT).next_to(yr, LEFT, buff=0.25)
        self.play(FadeIn(nm, shift=RIGHT * 0.2), FadeIn(yr), run_time=0.7)
        self.at("frogs")
        self.play(Indicate(fr, color=GOLD, scale_factor=1.06), run_time=1.2)
        self.at("He spread out")
        pts = [[-0.3, 2.3, 0], [2.0, 2.55, 0], [4.4, 2.35, 0], [5.9, 1.5, 0], [6.3, -0.4, 0], [5.4, -1.9, 0], [3.0, -2.3, 0], [0.9, -1.8, 0], [-0.1, -0.4, 0], [-0.3, 2.3, 0]]
        sheet = VMobject().set_points_as_corners(pts).set_stroke(TEXT, 3).set_fill(BLUE, 0.07)
        self.play(FadeIn(sheet, shift=RIGHT * 0.6), run_time=0.9)
        self.at("mesentery")
        ml = L("mesentery", 34, TEXT).move_to([3.2, -2.85, 0])
        self.play(FadeIn(ml), run_time=0.5)
        self.at("the thin sheet")
        gut = VMobject().set_points_smoothly([[-0.55, 2.0, 0], [-0.9, 0.6, 0], [-0.4, -0.6, 0], [-0.9, -1.6, 0], [-0.3, -2.4, 0]]).set_stroke(TAN, 22)
        gl = L("gut", 32, TAN).move_to([-1.5, 2.55, 0])
        self.play(Create(gut), FadeIn(gl), run_time=0.9)
        # fine network of capillaries
        rnd = random.Random(7)
        net = VGroup()
        trunks = [[(0.2, 1.8), (2.0, 1.2), (3.8, 1.6), (5.4, 0.9)], [(0.1, 0.4), (1.8, 0.0), (3.4, 0.3), (5.6, -0.2)],
                  [(0.2, -1.0), (2.0, -1.2), (3.6, -0.9), (5.3, -1.4)]]
        for tr in trunks:
            net.add(VMobject().set_points_smoothly([[x, y, 0] for x, y in tr]).set_stroke(SLATE, 4))
        for tr in trunks:
            for k in range(3):
                x, y = tr[k]
                net.add(Line([x, y, 0], [x + rnd.uniform(-0.4, 0.4), y + rnd.choice([-1, 1]) * rnd.uniform(0.5, 0.8), 0]).set_stroke(SLATE, 3))
        self.at("holds the gut")
        self.play(Create(net), run_time=1.0)
        self.at("watched")
        lens = Circle(radius=0.55, stroke_color=GOLD, stroke_width=6).move_to([3.4, 0.3, 0])
        self.play(Create(lens), run_time=0.5)
        self.at("single capillaries")
        big = Circle(radius=1.9, stroke_color=GOLD, stroke_width=7, fill_color=BG, fill_opacity=0.96).move_to([3.0, -0.2, 0])
        tube = wall(-0.2, 1.4, 4.6, 1.7, solid=True)
        fl = ValueTracker(0.9)
        rc = cells(-0.2, lambda: fl.get_value(), 1.55, 4.45, 0.6, n=8, seed=6, r=0.14, ramp=0.4)
        self.add(fl)
        self.play(Transform(lens, big), run_time=0.7)
        self.play(FadeIn(tube), FadeIn(rc), run_time=0.5)
        self.at("under a")
        sc = T("schematic", 24, GREY).move_to([5.9, -3.35, 0])
        self.play(FadeIn(sc), run_time=0.5)
        self.finish()


class S07Pipette(SpokenScene):
    def construct(self):
        w = wall(solid=True)
        flow = ValueTracker(1.1)
        blk = ValueTracker(0.0)
        rc = cells(0.0, lambda: flow.get_value(), seed=1, x1=4.1, blk=lambda: blk.get_value())
        sp = seep(0.0, CH, [-4.0, -1.0, 2.0], lambda: 0.8, lambda: 1.0, seed=3, speed=0.4)
        self.add(flow, blk, w, rc, sp)
        pp = pipette(-2.0, 0.3, 3.7)
        self.play(FadeIn(pp, shift=DOWN * 0.8), run_time=0.7)
        self.at("glass pipette")
        pl = L("glass pipette", 32, GLASS).move_to([0.2, 3.3, 0])
        self.play(FadeIn(pl), run_time=0.6)
        self.at("to record")
        P = ValueTracker(0.55)
        box, fill = gauge_bar(-4.5, 2.7, 2.8, 0.45, P, ORANGE, 0.02)
        rl = L("pressure", 32, ORANGE).move_to([-4.5, 3.3, 0])
        self.add(P)
        self.play(FadeIn(box), FadeIn(fill), FadeIn(rl), run_time=0.7)
        self.play(P.animate.set_value(0.7), run_time=1.0)
        self.at("Then he")
        rd2 = rod(4.6, 3.3, 3.7)
        self.add(rd2)
        self.play(Transform(rd2, rod(4.6, -1.25, 3.7)), run_time=1.3)
        self.at("shut")
        self.play(flow.animate.set_value(0.0), run_time=1.0)
        blk.set_value(1.0)
        self.at("glass rod")
        rl2 = L("glass rod", 32, GLASS).move_to([3.1, 3.3, 0])
        self.play(FadeIn(rl2), Indicate(rd2, color=GOLD, scale_factor=1.0), run_time=1.0)
        self.finish()


class S08Drift(SpokenScene):
    X0, X1, H = -4.0, 5.0, 1.5
    YT, YB = 1.95, -1.95

    def panel(self, y, flowtr, seed):
        w = wall(y, self.X0, self.X1, self.H, solid=True)
        rd = rod(self.X1 - 0.1, y - 0.5, y + 0.5)
        rd.stretch_to_fit_height(1.9).move_to([self.X1 - 0.1, y, 0])
        rc = cells(y, lambda: flowtr.get_value(), self.X0 + 0.3, self.X1 - 0.5, 0.5, n=10, seed=seed, r=0.12, ramp=0.4)
        return w, rd, rc

    def construct(self):
        ft, fb = ValueTracker(0.0), ValueTracker(0.0)
        wt, rt, ct = self.panel(self.YT, ft, 2)
        wb, rb, cb = self.panel(self.YB, fb, 3)
        self.add(ft, fb)
        self.play(FadeIn(wt), FadeIn(wb), FadeIn(rt), FadeIn(rb), FadeIn(ct), FadeIn(cb), run_time=1.0)
        self.at("trapped")
        self.play(ft.animate.set_value(0.12), fb.animate.set_value(0.12), run_time=1.4)
        # top panel: push wins
        rate_t, dir_t = ValueTracker(0.0), ValueTracker(1.0)
        spt = seep(self.YT, self.H, [-2.5, -0.5, 1.5, 3.5], lambda: rate_t.get_value(), lambda: dir_t.get_value(), seed=4, reach=0.75, speed=0.55)
        rate_b, dir_b = ValueTracker(0.0), ValueTracker(-1.0)
        spb = seep(self.YB, self.H, [-2.5, -0.5, 1.5, 3.5], lambda: rate_b.get_value(), lambda: dir_b.get_value(), seed=5, reach=0.75, speed=0.55)
        self.add(rate_t, dir_t, rate_b, dir_b, spt, spb)
        self.at("toward the block")
        bigT = push_arrows((-2.5, -0.5, 1.5, 3.5), self.YT, self.H, 0.8, ORANGE, 8)
        smT = VGroup(*[Arrow([x, self.YT + s * 1.45, 0], [x, self.YT + s * 1.1, 0], color=BLUE, buff=0, stroke_width=4, tip_length=0.14) for x in (-1.5, 0.5, 2.5) for s in (1, -1)])
        smT = VGroup()
        self.play(LaggedStart(*[GrowArrow(a) for a in bigT], lag_ratio=0.1), rate_t.animate.set_value(1.0), ft.animate.set_value(0.4), run_time=1.5)
        breathe(bigT)
        self.at("leaving")
        ll = L("fluid leaving", 32, ORANGE).move_to([-5.45, self.YT, 0])
        self.play(FadeIn(ll), run_time=0.6)
        self.at("away")
        bigB = VGroup(*[arr(x, self.YB + s * (self.H / 2 + 0.75), self.YB + s * (self.H / 2 + 0.05), BLUE, 8, 0.24) for x in (-2.5, -0.5, 1.5, 3.5) for s in (1, -1)])
        self.play(LaggedStart(*[GrowArrow(a) for a in bigB], lag_ratio=0.1), rate_b.animate.set_value(1.0), fb.animate.set_value(-0.4), ft.animate.set_value(0.12), run_time=1.1)
        breathe(bigB)
        self.at("entered")
        le = L("fluid entering", 32, BLUE).move_to([-5.4, self.YB, 0])
        self.play(FadeIn(le), run_time=0.6)
        self.finish()


class S09Plot(PlotBase):
    def construct(self):
        # big blocked capillary, cells drifting toward the rod
        w = wall(0.2, CX0, CX1, CH, solid=True)
        rd = rod(4.75, 0.2 - CH / 2, 0.2 + CH / 2)
        rd.stretch_to_fit_height(2.9).move_to([4.75, 0.2, 0])
        dr = ValueTracker(0.45)
        rc = cells(0.2, lambda: dr.get_value(), -5.2, 4.2, hh=0.9, n=12, seed=2, ramp=0.5)
        self.add(dr, w, rd, rc)
        self.wait(0.3)
        self.at("speed")
        tgt = rc[3]
        ar = Arrow([0, 0, 0], [0.8, 0, 0], color=GOLD, buff=0, stroke_width=7, tip_length=0.22)
        ar.add_updater(lambda m: m.put_start_and_end_on(tgt.get_center() + UP * 0.42 + LEFT * 0.2, tgt.get_center() + UP * 0.42 + RIGHT * 0.8))
        sl = L("speed", 34, GOLD).move_to([-3.5, 2.0, 0])
        sl.add_updater(lambda m: m.move_to(tgt.get_center() + UP * 0.9 + RIGHT * 0.3))
        self.play(FadeIn(ar), FadeIn(sl), run_time=0.6)
        self.at("size")
        da = DoubleArrow([0, -CH / 2, 0], [0, CH / 2, 0], color=GOLD, buff=0, stroke_width=6, tip_length=0.2).move_to([-6.3, 0.2, 0])
        szl = L("size", 34, GOLD).move_to([-6.3, 1.7, 0])
        self.play(FadeOut(ar), FadeOut(sl), GrowArrow(da), FadeIn(szl), run_time=0.8)
        self.at("fluid crossing")
        patch = Line([-1.0, 0.2 + CH / 2, 0], [0.8, 0.2 + CH / 2, 0]).set_stroke(GOLD, 12)
        oa = arr(-0.1, 0.2 + CH / 2 - 0.3, 0.2 + CH / 2 + 1.1, ORANGE, 8)
        pl = L("fluid across a patch", 34, ORANGE).move_to([-0.1, 3.0, 0])
        self.play(Create(patch), GrowArrow(oa), FadeIn(pl), run_time=1.0)
        self.at("Then he")
        self.play(FadeOut(VGroup(w, rd, rc, da, szl, patch, oa, pl)), run_time=0.4)
        self.strip(drift=0.35)
        self.P.set_value(0.5)
        self.add(self.P)
        self.play(FadeIn(VGroup(self.sw, self.rodm, self.tip, self.sc, self.rd, self.rdl)), run_time=0.4)
        # graph
        self.graph(right=False)
        self.remove(self.sch, self.outl, self.inl, self.xl, self.yl, self.ax)
        self.play(Create(self.ax), run_time=0.6)
        self.add(self.xl, self.yl, self.outl, self.inl)
        self.play(FadeIn(self.xl), FadeIn(self.yl), FadeIn(self.outl), FadeIn(self.inl), run_time=0.3)
        self.at("against the")
        P = self.P
        P.set_value(0.4)
        for d, p in zip(self.dotsR, RIGHT_P):
            d.set_opacity(0)
            d.add_updater(lambda m, p=p: m.set_opacity(1.0 if P.get_value() >= p - 0.005 else 0.0))
        self.add(self.dotsR, self.sch)
        self.play(P.animate.set_value(0.92), run_time=2.2, rate_func=linear)
        for d in self.dotsR:
            d.clear_updaters()
            d.set_opacity(1.0)
        self.finish()


class S10Predict(PlotBase):
    def construct(self):
        self.strip(drift=0.35)
        self.graph(right=True)
        self.wait(0.4)
        self.at("what should happen")
        self.play(Create(self.mk), run_time=1.2)
        self.at("falls below")
        self.play(FadeIn(self.shade), run_time=0.8)
        self.at("the pull of")
        self.play(FadeIn(self.mkl), run_time=0.7)
        self.at("Which way")
        self.play(FadeIn(self.card, scale=1.15), run_time=0.7)
        self.play(Indicate(self.card, color=GOLD, scale_factor=1.1), run_time=1.0)
        self.finish()


class S11Pause(PlotBase):
    def construct(self):
        # rebuild the question picture without a SpokenScene setup
        self.strip(0.35)
        self.graph(right=True, marker=True)
        self.add(self.shade, self.card)
        fr = ValueTracker(1.0)
        ring = always_redraw(lambda: VGroup(Circle(radius=0.38, stroke_color=GREY, stroke_width=3),
                                            Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * max(fr.get_value(), 0.001), stroke_color=GOLD,
                                                stroke_width=8)).move_to([6.2, -3.2, 0]))
        self.add(fr, ring)
        self.play(fr.animate.set_value(0.0), run_time=4.8, rate_func=linear)
        self.finish()


class S12Reveal(PlotBase):
    def construct(self):
        self.strip(drift=0.35)
        self.graph(right=True, marker=True)
        self.add(self.shade, self.card)
        self.wait(0.3)
        self.play(FadeOut(self.card), FadeOut(self.shade), run_time=0.5)
        # fluid comes in: the hidden dots appear below zero
        self.play(LaggedStart(*[FadeIn(d, scale=2.0) for d in self.dotsL], lag_ratio=0.25), run_time=1.6)
        self.play(self.dr.animate.set_value(-0.3), run_time=1.0)
        self.at("Filtration")
        self.play(Create(self.fit), run_time=2.2, rate_func=linear)
        pr = VGroup(L("roughly", 30, GOLD), L("proportional", 30, GOLD)).arrange(DOWN, buff=0.08).move_to([self.ax.c2p(PM, 0)[0] - 1.45, self.ax.c2p(0, 0.62)[1], 0])
        self.play(FadeIn(pr), run_time=0.6)
        self.at("It fell to zero")
        z = Dot(self.ax.c2p(PM, 0), radius=0.17, color=GOLD)
        zl = VGroup(L("zero, near the oncotic", 28, GOLD), L("pressure of frog plasma", 28, GOLD)).arrange(DOWN, buff=0.08).move_to(self.ax.c2p(0.8, -0.18))
        self.play(FadeIn(z, scale=2.0), FadeIn(zl), run_time=0.8)
        self.play(Indicate(z, color=GOLD, scale_factor=1.8), run_time=0.8)
        self.at("then reversed")
        rv = L("reversed: fluid enters", 28, BLUE)
        rv.next_to(self.mk, RIGHT, buff=0.2).set_y(self.ax.c2p(0, -0.46)[1])
        self.play(FadeIn(rv), Indicate(self.dotsL, color=BLUE, scale_factor=1.6), run_time=1.2)
        self.finish()


class S13Rule(PlotBase):
    def construct(self):
        # carry the finished graph from the last scene
        self.strip(drift=0.0)
        P0 = 0.5
        self.graph(right=True, left=True, line=True, marker=True)
        self.remove(self.mkl, self.sch, self.outl, self.inl, self.xl, self.yl)
        old = VGroup(self.sw, self.rodm, self.tip, self.sc, self.rd, self.rdl)
        self.remove(*old)
        gr = VGroup(self.ax, self.dotsR, self.dotsL, self.fit, self.mk)
        self.wait(0.2)
        for _m in self.sc.get_family():
            _m.clear_updaters()
        self.play(FadeOut(old), gr.animate.scale(0.6).move_to([3.7, -0.1, 0]), run_time=1.0)
        gx = T("capillary pressure", 24).move_to([3.7, -2.0, 0])
        gy = T("fluid across wall", 24).rotate(PI / 2).move_to([0.4, -0.1, 0])
        self.play(FadeIn(gx), FadeIn(gy), run_time=0.3)
        wp, wq, sw = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.add(wp, wq, sw)
        sw.add_updater(lambda m, dt: m.increment_value(dt * 1.6))
        pst = post(-3.4, 1.2, -0.6)
        bal = balance(-3.4, 1.2, 2.2, wp, wq, sw, ww=1.3, fs=30)
        self.at("driving pressure")
        eq = VGroup(T("net pressure", 36), T("=", 36), T("push", 36, ORANGE, weight=BOLD), T("−", 36), T("pull", 36, BLUE, weight=BOLD)).arrange(RIGHT, buff=0.22)
        eq.move_to([0.0, 3.3, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), Create(pst), FadeIn(bal), run_time=1.0)
        self.at("push")
        self.play(wp.animate.set_value(1.0), run_time=0.7)
        self.at("pull")
        self.play(wq.animate.set_value(1.0), run_time=0.7)
        fm = VGroup(T("(", 26), sub("P", "c", 26, ORANGE), sub("− P", "i", 26, ORANGE), T(") − σ (", 26), sub("π", "c", 26, BLUE), T("− π outside", 26, BLUE), T(")", 26)).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        fm.move_to([0.0, 2.65, 0])
        sg = T("σ: the share of the protein pull that counts, since a few albumin cross", 22, GREY).move_to([0.0, -3.55, 0])
        self.play(FadeIn(fm), FadeIn(sg), run_time=0.6)
        # small capillary: arrows follow the sign of push minus pull
        cy = -2.2
        sc = wall(cy, -5.6, -1.4, 0.7, solid=True)
        net = lambda: wp.get_value() - wq.get_value()

        def arrows():
            n = net()
            g = VGroup()
            for x in (-4.6, -3.5, -2.4):
                for s in (1, -1):
                    if abs(n) < 0.05:
                        continue
                    ln = 0.25 + 0.45 * min(1.0, abs(n))
                    a0 = cy + s * 0.35
                    a1 = a0 + s * ln * (1 if n > 0 else -1)
                    g.add(Arrow([x, a0, 0], [x, a1, 0], color=ORANGE if n > 0 else BLUE, buff=0, stroke_width=6, tip_length=0.18))
            return g
        sa = always_redraw(arrows)
        fl = ValueTracker(0.8)
        sr = cells(cy, lambda: fl.get_value(), -5.4, -1.6, 0.18, n=6, seed=9, r=0.08, ramp=0.4)
        self.add(fl)
        self.play(FadeIn(sc), FadeIn(sa), run_time=0.5)
        self.add(sr)
        # marker on the graph follows the net pressure
        axs = self.ax

        def mk():
            n = net()
            p = max(0.05, min(0.95, PM + 0.45 * n))
            return Dot(axs.c2p(p, Jrate(p)), radius=0.14, color=GOLD)
        mdot = always_redraw(mk)
        self.add(mdot)
        self.at("more the push wins")
        self.play(wp.animate.set_value(2.0), run_time=1.2)
        self.at("faster fluid leaves")
        self.play(Indicate(sa, color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("When the pull wins")
        self.play(wp.animate.set_value(0.4), wq.animate.set_value(1.6), run_time=1.6)
        self.at("fluid comes in")
        self.play(Indicate(mdot, color=BLUE, scale_factor=1.6), run_time=1.2)
        self.finish()


class S14Limit(SpokenScene):
    def construct(self):
        fr = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.9, stroke_color=TEXT, stroke_width=5).move_to([-3.9, 0.9, 0])
        net = VGroup()
        rnd = random.Random(4)
        for k in range(6):
            y = 0.9 + (k - 2.5) * 0.55
            net.add(VMobject().set_points_smoothly([[-6.4 + i * 0.9, y + rnd.uniform(-0.15, 0.15), 0] for i in range(6)]).set_stroke(SLATE, 5))
        gut = VMobject().set_points_smoothly([[-6.4, 2.45, 0], [-5.2, 2.25, 0], [-4.0, 2.45, 0], [-2.8, 2.25, 0], [-1.6, 2.45, 0]]).set_stroke(TAN, 14)
        self.play(Create(fr), run_time=0.8)
        self.play(Create(net), Create(gut), run_time=1.4)
        self.at("one frog tissue")
        fl = VGroup(L("one tissue,", 36, TEXT), L("one species", 36, TEXT)).arrange(DOWN, buff=0.1).move_to([-3.9, -1.7, 0])
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.7)
        self.at("His result")
        self.play(Indicate(fr, color=GOLD, scale_factor=1.04), run_time=1.3)
        self.at("It did not show")
        c0 = np.array([1.2, 1.2, 0])
        clk = Circle(radius=1.4, stroke_color=TEXT, stroke_width=6).move_to(c0)
        ticks = VGroup(*[Line(c0 + 1.15 * np.array([math.cos(a), math.sin(a), 0]), c0 + 1.32 * np.array([math.cos(a), math.sin(a), 0])).set_stroke(TEXT, 5)
                         for a in np.linspace(0, TAU, 12, endpoint=False)])
        hand = Line(c0, c0 + UP * 1.05).set_stroke(GOLD, 8)
        hand.add_updater(lambda m, dt: m.rotate(-dt * 1.6, about_point=c0))
        self.play(Create(clk), Create(ticks), Create(hand), run_time=0.9)
        self.at("every capillary")
        orgs = VGroup()
        shapes = [Ellipse(width=1.9, height=1.4), RoundedRectangle(corner_radius=0.5, width=1.8, height=1.6), Ellipse(width=1.6, height=1.9)]
        for k, sh in enumerate(shapes):
            sh.set_stroke(TEXT, 5)
            sh.set_fill(TAN, 0.14)
            sh.move_to([5.2 + (0.0 if k != 1 else -0.6), 2.4 - k * 2.0, 0])
            q = T("?", 56, GOLD, weight=BOLD).move_to(sh)
            orgs.add(VGroup(sh, q))
        self.play(LaggedStart(*[FadeIn(o, scale=1.2) for o in orgs], lag_ratio=0.3), run_time=1.4)
        self.at("over hours")
        hl = L("hours?", 40, GOLD).move_to([1.2, -0.9, 0])
        self.play(FadeIn(hl, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(hl, color=GOLD, scale_factor=1.15), run_time=1.0)
        self.finish()


class S15Lymph(SpokenScene):
    Y = 0.75

    def construct(self):
        Y = self.Y
        w = wall(Y, solid=False)
        flow = ValueTracker(1.0)
        rate = ValueTracker(1.0)
        rc = cells(Y, lambda: flow.get_value(), seed=1)
        sp = seep(Y, CH, [-4.4, -2.4, -0.4, 1.6, 3.6], lambda: rate.get_value(), lambda: 1.0, seed=3, sides=(-1,), reach=0.7, speed=0.4)
        self.add(flow, rate, w, rc, sp)
        al = L("arterial end", 32, TEXT).move_to([-4.3, 3.45, 0])
        vl = L("venous end", 32, TEXT).move_to([3.7, 3.45, 0])
        small = VGroup(*[arr(x, Y + 0.6, Y + 1.5, ORANGE, 6, 0.2) for x in np.linspace(-4.7, 4.1, 8)])
        small.add(*[arr(x, Y - 0.6, Y - 1.2, ORANGE, 6, 0.2) for x in np.linspace(-4.7, 4.1, 8)])
        big = VGroup(*[arr(x, 3.0, 2.0, BLUE, 10, 0.3) for x in (2.8, 4.1)] + [arr(x, -1.9, -0.65, BLUE, 10, 0.3).rotate(PI, about_point=[x, -1.275, 0]) for x in ()])
        big.add(*[Arrow([x, -1.9, 0], [x, -0.7, 0], color=BLUE, buff=0, stroke_width=10, tip_length=0.3) for x in (2.8, 4.1)])
        self.play(FadeIn(al), FadeIn(vl), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in small], lag_ratio=0.05), run_time=1.2)
        breathe(small, base=0.8)
        self.at("venous end")
        self.play(LaggedStart(*[GrowArrow(a) for a in big], lag_ratio=0.15), run_time=1.0)
        breathe(big)
        self.at("lacks")
        stamp = L("not supported as a general account", 34, GOLD).move_to([0.9, -1.75, 0])
        self.play(FadeOut(big), FadeIn(stamp, scale=1.2), run_time=1.2)
        self.at("In most tissues")
        ly = -2.85
        lt = VMobject().set_points_as_corners([[-4.6, ly, 0], [4.4, ly, 0], [6.0, ly + 0.9, 0]])
        lt.set_stroke(GREEN, 22).set_fill(opacity=0).set_opacity(0.55)
        lt.set_cap_style(CapStyleType.ROUND)
        lcap = Dot([-4.6, ly, 0], radius=0.2, color=GREEN)
        ll = L("lymph vessel", 34, GREEN).move_to([-3.0, -3.6, 0])
        self.play(Create(lt), FadeIn(lcap), FadeOut(stamp), run_time=1.5)
        self.play(FadeIn(ll), run_time=0.5)
        self.at("filter slowly")
        self.play(Indicate(small, color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("lymph vessels carry")
        ld = cells(ly, lambda: 1.1, -4.3, 4.3, 0.1, n=8, seed=12, r=0.11, color=GREEN, ramp=0.5)
        self.play(FadeIn(ld), run_time=0.6)
        self.at("fluid back")
        vein = Line([6.0, ly + 0.9, 0], [6.0, 0.2, 0]).set_stroke(SLATE, 22).set_opacity(0.7)
        vn = L("vein", 34, TEXT).move_to([6.0, 0.7, 0])
        self.play(Create(vein), FadeIn(vn), run_time=0.8)
        self.finish()


class S16End(EndCard):
    LINE = "Push minus pull decides which way fluid crosses the wall."
