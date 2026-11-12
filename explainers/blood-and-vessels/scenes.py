"""Downhill in Pressure: Q = (P_in - P_out) / R, and why blood is slowest in the narrowest vessels.

COLOR MAP (one color per concept, whole film)
  ORANGE = pressure / hydrostatic push        BLUE   = oncotic pull (river inset flow lines)
  RED    = red cells (dots)                   PURPLE = resistance bars
  TEAL   = total cross-section bars           PINK   = smooth muscle cuffs
  GOLD   = highlights, gates                  SLATE  = vessel walls (charcoal on dark)
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B07CE0"
PINK = "#D77AB8"
SLATE = "#7A86A3"
TAN = "#C9A66B"
Y0 = -0.8


# ------------------------------------------------------------------ helpers
def eq_pinned(size=32):
    parts = [M("Q = (P", size), M("in", 22), M("  − P", size), M("out", 22), M(") / R", size)]
    g = VGroup(*parts).arrange(RIGHT, buff=0.03, aligned_edge=DOWN)
    parts[1].shift(DOWN * 0.07)
    parts[3].shift(DOWN * 0.07)
    g.move_to([-6.6 + g.width / 2, 3.4, 0])
    return g


def stream(x0, x1, n, speed, geom, seed=1, r=0.085, color=RED, gate=None):
    """dots drifting right in a tube; speed() gives units/s, geom(x) gives (centre y, half height)."""
    rnd = random.Random(seed)
    g = VGroup()
    L = x1 - x0
    for k in range(n):
        d = Dot(radius=r, color=color)
        d.px = x0 + (k + rnd.random() * 0.7 + 0.15) * L / n
        d.j = rnd.uniform(-1, 1)
        d.k = k

        def up(m, dt):
            m.px += speed() * dt
            if m.px > x1 - 0.1:
                m.px -= (L - 0.2)
            cy, hh = geom(m.px)
            m.move_to([m.px, cy + m.j * hh, 0])
            if gate:
                m.set_opacity(gate(m))
        d.add_updater(up)
        up(d, 0)
        g.add(d)
    return g


def tube_rect(x0, x1, cy, h, color=SLATE, fo=0.18):
    return RoundedRectangle(corner_radius=min(0.2, h / 2.5), width=x1 - x0, height=h, stroke_color=color,
                            stroke_width=4, fill_color=color, fill_opacity=fo).move_to([(x0 + x1) / 2, cy, 0])


def sup4(base, size=34, color=TEXT):
    a = M(base, size, color)
    b = M("4", 24, color)
    b.next_to(a, RIGHT, buff=0.03).shift(UP * 0.17)
    return VGroup(a, b)


# ------------------------------------------------------------------ pressure world (s02, s03)
def pressure_world(hl, hr, R):
    HL, HR, RR = ValueTracker(hl), ValueTracker(hr), ValueTracker(R)
    tube = tube_rect(-3.8, 3.8, -1.9, 0.9)
    colL = always_redraw(lambda: Rectangle(width=1.0, height=max(HL.get_value(), 0.02), stroke_color=ORANGE, stroke_width=3,
                                           fill_color=ORANGE, fill_opacity=0.5).move_to([-4.3, -3.2 + HL.get_value() / 2, 0]))
    colR = always_redraw(lambda: Rectangle(width=1.0, height=max(HR.get_value(), 0.02), stroke_color=ORANGE, stroke_width=3,
                                           fill_color=ORANGE, fill_opacity=0.5).move_to([4.3, -3.2 + HR.get_value() / 2, 0]))
    dots = stream(-3.7, 3.7, 14, lambda: 1.6 * (HL.get_value() - HR.get_value()) / RR.get_value(), lambda x: (-1.9, 0.28), seed=4, r=0.12)
    return dict(HL=HL, HR=HR, RR=RR, tube=tube, colL=colL, colR=colR, dots=dots)


# ------------------------------------------------------------------ tree
CY = Y0 + np.linspace(-1.9, 1.9, 12)
AL = [(CY[2 * j] + CY[2 * j + 1]) / 2 for j in range(6)]
AR = [(AL[2 * k] + AL[2 * k + 1]) / 2 for k in range(3)]
VY = AR
W = dict(aorta=44, arteries=30, arterioles=18, caps=10, veins=20, trunk=38)


def seg(a, b, w):
    ln = Line([a[0], a[1], 0], [b[0], b[1], 0]).set_stroke(SLATE, w)
    ln.set_cap_style(CapStyleType.ROUND)
    return ln


def heart_shape():
    f = lambda t: np.array([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0])
    h = ParametricFunction(f, t_range=[0, TAU], fill_color=RED, fill_opacity=0.85, stroke_width=0)
    h.set_fill(RED, 0.85)
    h.set_height(1.1)
    return h.move_to([5.9, Y0, 0])


def make_tree():
    G = {k: VGroup() for k in ["aorta", "arteries", "arterioles", "caps", "veins", "trunk"]}
    G["aorta"].add(seg((-6.5, Y0), (-5.4, Y0), W["aorta"]))
    for k in range(3):
        G["arteries"].add(seg((-5.4, Y0), (-5.0, AR[k]), W["arteries"]), seg((-5.0, AR[k]), (-3.8, AR[k]), W["arteries"]))
        for j in (2 * k, 2 * k + 1):
            G["arterioles"].add(seg((-3.8, AR[k]), (-3.4, AL[j]), W["arterioles"]), seg((-3.4, AL[j]), (-1.6, AL[j]), W["arterioles"]))
    for j in range(6):
        for i in (2 * j, 2 * j + 1):
            G["caps"].add(seg((-1.6, AL[j]), (-1.2, CY[i]), W["caps"]), seg((-1.2, CY[i]), (1.1, CY[i]), W["caps"]))
    for i in range(12):
        G["veins"].add(seg((1.1, CY[i]), (1.5, VY[i // 4]), W["veins"]))
    for k in range(3):
        G["veins"].add(seg((1.5, VY[k]), (3.2, VY[k]), W["veins"]))
        G["trunk"].add(seg((3.2, VY[k]), (3.7, Y0), W["trunk"]))
    G["trunk"].add(seg((3.7, Y0), (5.4, Y0), W["trunk"]))
    heart = heart_shape()
    return G, heart


LEVELS = [("aorta", -5.95, "aorta"), ("arteries", -4.4, "arteries"), ("arterioles", -2.5, "arterioles"),
          ("caps", -0.05, "capillaries"), ("veins", 2.35, "veins")]


def level_label(name):
    for k, x, t in LEVELS:
        if k == name:
            return T(t, 28).move_to([x, -3.45, 0])
    return T("heart", 28).move_to([5.9, Y0 - 1.0, 0])


def path_pts(i):
    k, j = i // 4, i // 2
    return [(-6.5, Y0), (-5.4, Y0), (-5.0, AR[k]), (-3.8, AR[k]), (-3.4, AL[j]), (-1.6, AL[j]), (-1.2, CY[i]), (1.1, CY[i]),
            (1.5, VY[k]), (3.2, VY[k]), (3.7, Y0), (5.3, Y0)]


PX = np.array([p[0] for p in path_pts(0)])
PROF = np.array([3.0, 3.0, 2.2, 2.2, 1.2, 1.2, 0.25, 0.25, 0.8, 0.8, 1.5, 1.5])
HW = np.array([0.12, 0.12, 0.08, 0.08, 0.04, 0.04, 0.0, 0.0, 0.05, 0.05, 0.1, 0.1])


def tree_flow(tm, reach, per=6, seed=3):
    rnd = random.Random(seed)
    g = VGroup()
    P = [np.array(path_pts(i)) for i in range(12)]
    for i in range(12):
        for k in range(per):
            d = Dot(radius=0.08, color=RED)
            d.px = -6.5 + (k + rnd.random() * 0.8) * 11.8 / per
            d.j = rnd.uniform(-1, 1)
            d.pi = i

            def up(m, dt):
                mm = tm.get_value()
                v = (1 - mm) * 1.4 + mm * np.interp(m.px, PX, PROF)
                m.px += v * dt
                if m.px > 5.25:
                    m.px = -6.45
                y = np.interp(m.px, P[m.pi][:, 0], P[m.pi][:, 1]) + m.j * np.interp(m.px, PX, HW)
                m.move_to([m.px, y, 0])
                m.set_opacity(1.0 if m.px < reach.get_value() else 0.0)
            d.add_updater(up)
            up(d, 0)
            g.add(d)
    return g


class TreeBase(SpokenScene):
    """carries the finished tree, labels, heart, flow dots and pinned rule."""
    def tree(self, labels=True, uniform=True, pinned=True):
        self.G, self.heart = make_tree()
        self.tm = ValueTracker(0.0 if uniform else 1.0)
        self.reach = ValueTracker(99)
        self.dots = tree_flow(self.tm, self.reach)
        self.lab = VGroup(*[level_label(k) for k, _, _ in LEVELS], level_label("heart")) if labels else VGroup()
        self.add(self.tm, self.reach, *self.G.values(), self.heart, self.lab, self.dots)
        if pinned:
            self.eq = eq_pinned()
            self.add(self.eq)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Blood Vessels, Blood and Lymph"
    TITLE = "Downhill in Pressure"

    def construct(self):
        G, heart = make_tree()
        faint = VGroup(*G.values(), heart).set_opacity(0.14)
        self.add(faint)
        super().construct()


class S01Hook(SpokenScene):
    def construct(self):
        aorta = tube_rect(-6.4, -0.6, 1.5, 1.5)
        cap = tube_rect(0.6, 6.4, 1.5, 0.2)
        la = T("aorta", 32).move_to([-3.5, 2.85, 0])
        lc = T("capillary", 32).move_to([3.5, 2.85, 0])
        da = stream(-6.3, -0.7, 9, lambda: 3.2, lambda x: (1.5, 0.5), seed=2)
        dc = stream(0.7, 6.3, 5, lambda: 0.35, lambda x: (1.5, 0.05), seed=5, r=0.06)
        self.play(Create(aorta), run_time=0.8)
        self.add(da)
        self.play(FadeIn(la), FadeIn(da), run_time=0.6)
        self.at("slowest")
        self.play(Create(cap), FadeIn(lc), run_time=0.8)
        self.add(dc)
        self.at("How can narrower")
        q = T("?", 90, GOLD, weight=BOLD).move_to([0, 1.5, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.play(Indicate(q, color=GOLD, scale_factor=1.2), run_time=1.0)
        self.at("river channel")
        cyc = -1.75
        wf = lambda x: 2.0 - 1.15 * np.exp(-(x / 1.7) ** 2)
        xs = np.linspace(-6, 6, 80)
        top = [[x, cyc + wf(x) / 2, 0] for x in xs]
        bot = [[x, cyc - wf(x) / 2, 0] for x in xs][::-1]
        ch = VMobject().set_points_as_corners(top + bot + [top[0]]).set_stroke(GREY, 4).set_fill(BLUE, 0.12)
        self.play(Create(ch), run_time=1.0)
        rd = stream(-6, 6, 22, lambda: 0, lambda x: (cyc, wf(x) * 0.4), seed=9, r=0.07, color=BLUE)
        for d in rd:  # speed ~ 1 / width
            d.clear_updaters()

            def up(m, dt, wf=wf):
                m.px += 2.9 / wf(m.px) * dt
                if m.px > 5.9:
                    m.px -= 11.8
                m.move_to([m.px, cyc + m.j * wf(m.px) * 0.4, 0])
            d.add_updater(up)
        self.add(rd)
        self.at("Where its cross")
        ar = Arrow([-1.3, cyc + 1.25, 0], [-0.1, cyc + 0.55, 0], color=GOLD, buff=0, stroke_width=6)
        ar2 = Arrow([1.3, cyc + 1.25, 0], [0.1, cyc + 0.55, 0], color=GOLD, buff=0, stroke_width=6)
        self.play(FadeIn(ar), FadeIn(ar2), run_time=0.6)
        self.at("speed up")
        st = T("one channel, same water: smaller cross-section = faster", 28, BLUE).move_to([0, -3.35, 0])
        self.play(FadeIn(st, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S02Rule(SpokenScene):
    def construct(self):
        w = pressure_world(5.0, 2.5, 1.0)
        self.play(Create(w["tube"]), FadeIn(w["colL"]), FadeIn(w["colR"]), run_time=1.2)
        self.add(w["HL"], w["HR"], w["RR"])
        self.add(w["dots"])
        self.play(FadeIn(w["dots"]), run_time=0.6)
        self.at("level tube")
        lab = T("level tube, no pump inside", 28).move_to([0, -0.75, 0])
        self.play(FadeIn(lab), run_time=0.6)
        self.at("fluid flows only")
        self.play(Indicate(w["colL"], color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("Equal pressure")
        self.play(w["HR"].animate.set_value(5.0), run_time=2.0, rate_func=smooth)
        line = DashedLine([-3.8, 1.8, 0], [3.8, 1.8, 0], color=ORANGE, stroke_width=3)
        eqp = T("equal pressure", 30, ORANGE).move_to([0, 1.3, 0])
        self.play(Create(line), FadeIn(eqp), FadeOut(lab), run_time=0.8)
        self.at("however high")
        nd = T("no difference, no flow", 32).move_to([0, 0.4, 0])
        self.play(FadeIn(nd, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S03Equation(SpokenScene):
    def construct(self):
        w = pressure_world(5.0, 2.5, 1.0)
        self.add(w["tube"], w["colL"], w["colR"], w["HL"], w["HR"], w["RR"], w["dots"])
        self.wait(0.3)
        self.at("pressure difference between")
        d1 = DashedLine([-3.8, 1.8, 0], [2.2, 1.8, 0], color=ORANGE, stroke_width=3)
        d2 = DashedLine([2.2, -0.7, 0], [3.8, -0.7, 0], color=ORANGE, stroke_width=3)
        arr = DoubleArrow([2.2, -0.7, 0], [2.2, 1.8, 0], color=ORANGE, buff=0, stroke_width=6)
        lab = T("P in − P out", 30, ORANGE).move_to([0.5, 0.55, 0])
        self.play(Create(d1), Create(d2), run_time=0.7)
        self.play(GrowFromCenter(arr), FadeIn(lab), run_time=0.8)
        self.at("resistance in")
        blk = Rectangle(width=0.7, height=1.15, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.8).move_to([0, 0.6, 0])
        rl = T("R", 34, TEXT, weight=BOLD).move_to(blk)
        grp = VGroup(blk, rl)
        self.play(FadeIn(grp), run_time=0.3)
        self.play(grp.animate.move_to([0, -1.9, 0]), run_time=1.0)
        self.play(w["RR"].animate.set_value(2.4), run_time=1.4)
        self.at("Flow equals")
        eq = eq_pinned()
        fl = T("Q = flow", 28, GOLD).move_to([-6.6 + 0.5 + T("Q = flow", 28).width / 2 - 0.5, 2.75, 0])
        self.play(Write(eq), run_time=2.0)
        self.play(FadeIn(fl), run_time=0.6)
        self.finish()


class S04Tree(TreeBase):
    def construct(self):
        self.eq = eq_pinned()
        self.add(self.eq)
        G, heart = make_tree()
        self.G, self.heart = G, heart
        tm, reach = ValueTracker(0.0), ValueTracker(-7)
        dots = tree_flow(tm, reach)
        self.add(tm, reach, dots)
        w = pressure_world(5.0, 2.5, 2.4)
        blk = Rectangle(width=0.7, height=1.15, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.8).move_to([0, -1.9, 0])
        self.add(w["tube"], w["colL"], w["colR"], w["HL"], w["HR"], w["RR"], w["dots"], blk)
        ghost = VGroup(*[g.copy() for g in G.values()], heart.copy()).set_opacity(0.15)
        self.play(FadeOut(VGroup(w["colL"], w["colR"], w["dots"], blk)), Transform(w["tube"], G["aorta"][0].copy()), run_time=1.5)
        self.play(FadeOut(w["tube"]), run_time=0.1)
        self.play(LaggedStart(*[Create(m) for m in ghost], lag_ratio=0.06), run_time=2.6)
        sch = T("schematic, not to scale", 26, GREY).move_to([4.2, 3.35, 0])
        self.play(FadeIn(sch), run_time=0.5)
        self.at("aorta")
        self.play(Create(G["aorta"]), FadeIn(level_label("aorta")), run_time=0.7)
        reach.set_value(-5.4)
        self.add(dots)
        self.at("splits into")
        self.play(Create(G["arteries"]), FadeIn(level_label("arteries")), run_time=0.7)
        reach.set_value(-3.8)
        self.at("then arterials")
        self.play(Create(G["arterioles"]), FadeIn(level_label("arterioles")), run_time=0.7)
        reach.set_value(-1.6)
        self.at("then capillaries")
        self.play(Create(G["caps"]), FadeIn(level_label("caps")), run_time=0.9)
        reach.set_value(1.1)
        self.at("gather again")
        self.play(Create(G["veins"]), FadeIn(level_label("veins")), run_time=1.0)
        reach.set_value(3.2)
        self.at("return to the")
        self.play(Create(G["trunk"]), FadeIn(self.heart), FadeIn(level_label("heart")), run_time=1.0)
        reach.set_value(99)
        self.play(FadeOut(ghost), run_time=0.4)
        self.finish()


class S05Pressure(TreeBase):
    def construct(self):
        self.tree()
        sch = T("schematic, not to scale", 26, GREY).move_to([4.2, 3.35, 0])
        self.add(sch)
        px = [-6.5, -5.0, -3.8, -3.4, -1.6, -1.2, 1.1, 1.5, 3.2, 5.0]
        pv = [93, 91, 88, 84, 40, 35, 15, 12, 5, 3]
        yy = lambda p: 1.7 + 1.2 * p / 93
        pts = [[x, yy(p), 0] for x, p in zip(px, pv)]
        line = VMobject().set_points_as_corners(pts).set_stroke(ORANGE, 8)
        self.at("pressure")
        dot0 = Dot([-6.5, yy(93), 0], color=ORANGE, radius=0.12)
        l93 = T("93 mmHg", 30, ORANGE).move_to([-5.4, 2.38, 0])
        self.play(FadeIn(dot0), FadeIn(l93), run_time=0.6)
        self.at("falls all the way")
        self.play(Create(line), run_time=3.0, rate_func=linear)
        self.at("right atrium")
        l3 = T("3 mmHg", 30, ORANGE).move_to([5.4, 2.25, 0])
        self.play(FadeIn(l3), run_time=0.6)
        self.at("most steeply")
        hl = VMobject().set_points_as_corners(pts[3:5]).set_stroke(GOLD, 14)
        sd = T("steepest drop", 30, GOLD).move_to([-2.2, 1.55, 0])
        self.play(Create(hl), FadeIn(sd), run_time=1.0)
        self.play(Indicate(hl, color=GOLD, scale_factor=1.0), run_time=1.0)
        self.finish()


class S06Lever(SpokenScene):
    def construct(self):
        eq = eq_pinned()
        self.add(eq)
        G, heart = make_tree()
        tm, reach = ValueTracker(0), ValueTracker(99)
        dots = tree_flow(tm, reach)
        self.add(tm, reach, *G.values(), heart, dots)
        r = ValueTracker(0.85)
        cy = 0.3
        body = always_redraw(lambda: Rectangle(width=7.0, height=2 * r.get_value(), stroke_color=SLATE, stroke_width=6,
                                               fill_color=SLATE, fill_opacity=0.25).move_to([-2.0, cy, 0]))
        cuffs = always_redraw(lambda: VGroup(
            *[RoundedRectangle(corner_radius=0.12, width=1.6, height=0.4, stroke_color=PINK, fill_color=PINK, fill_opacity=0.55)
              .move_to([-2.4, cy + s * (r.get_value() + 0.2), 0]) for s in (1, -1)]))
        H = lambda: 0.9 * (0.85 / r.get_value()) ** 4
        bar = always_redraw(lambda: Rectangle(width=1.0, height=H(), stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.75)
                            .move_to([4.8, -1.9 + H() / 2, 0]))
        dd = stream(-5.4, 1.4, 9, lambda: 2.4 * 0.9 / H(), lambda x: (cy, 0.6 * r.get_value()), seed=6)
        self.add(r)
        self.play(FadeOut(VGroup(*G.values(), heart, dots)), FadeIn(body), run_time=1.0)
        self.add(dd)
        self.play(FadeIn(dd), run_time=0.4)
        self.at("smooth muscle")
        sm = T("smooth muscle", 30, PINK).move_to([-2.4, 2.35, 0])
        self.play(FadeIn(cuffs), FadeIn(sm), run_time=0.8)
        self.at("When the muscle")
        self.play(r.animate.set_value(0.6), run_time=2.3, rate_func=smooth)
        self.at("In an ideal")
        self.play(r.animate.set_value(0.85), run_time=1.0)
        rule = VGroup(sup4("R ∝ 1 / r"), T("(ideal tube)", 24, GREY)).arrange(RIGHT, buff=0.3).move_to([3.4, 3.4, 0])
        self.play(FadeIn(rule), run_time=0.6)
        self.at("resistance rises")
        bl = T("resistance", 28, PURPLE).move_to([4.8, -2.45, 0])
        self.play(FadeIn(bar), FadeIn(bl), run_time=0.7)
        self.at("fourth power")
        self.play(r.animate.set_value(0.6), run_time=2.0, rate_func=smooth)
        self.at("small squeeze")
        self.play(r.animate.set_value(0.85), run_time=1.2)
        self.play(r.animate.set_value(0.6), run_time=1.2)
        self.finish()


class S07Taps(SpokenScene):
    def construct(self):
        eq = eq_pinned()
        self.add(eq)
        trunk = seg((-6.3, -0.5), (-4.6, -0.5), 24)
        up_b = VGroup(seg((-4.6, -0.5), (-3.9, 1.2), 16), seg((-3.9, 1.2), (0.6, 1.2), 16))
        lo_b = VGroup(seg((-4.6, -0.5), (-3.9, -2.2), 16), seg((-3.9, -2.2), (0.6, -2.2), 16))
        gut = chip("gut", TAN, 32).move_to([1.9, 1.2, 0])
        mus = chip("muscle", TAN, 32).move_to([2.0, -2.2, 0])
        gt = ValueTracker(0.0)
        cuff = lambda y, t: always_redraw(lambda: RoundedRectangle(corner_radius=0.12, width=0.55, height=0.52 - 0.22 * t(),
                                                                    stroke_color=PINK, fill_color=PINK, fill_opacity=0.35).move_to([-1.7, y, 0]))
        cg, cm = cuff(1.2, lambda: gt.get_value()), cuff(-2.2, lambda: 0.0)
        barG = always_redraw(lambda: Rectangle(width=0.4, height=0.4 + 1.0 * gt.get_value(), stroke_color=PURPLE, fill_color=PURPLE,
                                               fill_opacity=0.75).move_to([-0.4, 1.2, 0]))
        barM = Rectangle(width=0.4, height=0.4, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.75).move_to([-0.4, -2.2, 0])
        dt_ = stream(-6.2, -4.7, 4, lambda: 1.6, lambda x: (-0.5, 0.15), seed=3, r=0.07)
        dg = stream(-3.8, 0.5, 8, lambda: 1.8 * (1 - 0.8 * gt.get_value()), lambda x: (1.2, 0.1), seed=7, r=0.07,
                    gate=lambda m: 1.0 if m.k % 2 == 0 else 1 - 0.85 * gt.get_value())
        dm = stream(-3.8, 0.5, 8, lambda: 1.8, lambda x: (-2.2, 0.1), seed=8, r=0.07)
        self.add(gt)
        self.play(Create(trunk), Create(up_b), Create(lo_b), run_time=1.2)
        self.add(dt_, dg, dm)
        self.play(FadeIn(gut), FadeIn(mus), FadeIn(cg), FadeIn(cm), FadeIn(barG), FadeIn(barM), run_time=1.0)
        tags = []
        for txt, ph, x in [("nerves", "Nerves", -5.2), ("hormones", "hormones", -3.4), ("local signals", "local signals", -1.1)]:
            self.at(ph)
            tg = T(txt, 28, GOLD).move_to([x, 2.65, 0])
            ar = Arrow(tg.get_bottom() + DOWN * 0.05, [-1.7, 1.55, 0], color=GOLD, buff=0.05, stroke_width=4, tip_length=0.2)
            self.play(FadeIn(tg), Create(ar), run_time=0.5)
            tags += [tg, ar]
        self.at("tightening one")
        self.play(FadeOut(VGroup(*tags)), gt.animate.set_value(1.0), run_time=1.6)
        box = Rectangle(width=2.7, height=0.5, stroke_color=GREY, stroke_width=3).move_to([5.2, 1.2, 0])
        fillw = ValueTracker(2.6)
        fl = always_redraw(lambda: Rectangle(width=max(fillw.get_value(), 0.02), height=0.42, stroke_width=0, fill_color=RED,
                                             fill_opacity=0.8).move_to([3.85 + fillw.get_value() / 2, 1.2, 0]))
        self.at("cuts that")
        self.add(fillw)
        self.play(FadeIn(box), FadeIn(fl), run_time=0.5)
        self.play(fillw.animate.set_value(0.9), run_time=1.4)
        lbl = T("gut's share falls", 28, RED).move_to([5.1, 0.55, 0])
        self.play(FadeIn(lbl), run_time=0.5)
        self.finish()


def s8_layout(scene, with_note=True, with_card=True):
    """arteriole + capillary tubes, purple bars, question card, buttons. Returns a dict."""
    o = {}
    o["ta"] = tube_rect(-6.4, -3.6, 1.7, 0.9)
    o["tc"] = tube_rect(-6.4, -3.6, 0.2, 0.3)
    o["la"] = T("arteriole", 28).move_to([-5.0, 2.45, 0])
    o["lc"] = T("capillary", 28).move_to([-5.0, 0.8, 0])
    o["da"] = stream(-6.3, -3.7, 6, lambda: 1.8, lambda x: (1.7, 0.28), seed=2, r=0.08)
    o["dc"] = stream(-6.3, -3.7, 4, lambda: 1.0, lambda x: (0.2, 0.04), seed=5, r=0.06)
    o["ba"] = Rectangle(width=0.9, height=1.0, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.75).move_to([0.4, -0.7 + 0.5, 0])
    o["bc"] = Rectangle(width=0.9, height=2.1, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.75).move_to([4.0, -0.7 + 1.05, 0])
    o["bla"] = T("arteriole", 28).move_to([0.4, -1.15, 0])
    o["blc"] = T("capillary", 28).move_to([4.0, -1.15, 0])
    o["note"] = VGroup(T("one vessel: length and", 26, GREY), T("blood's thickness count too", 26, GREY)).arrange(DOWN, buff=0.1).move_to([-4.2, -0.85, 0])
    o["card"] = VGroup(RoundedRectangle(corner_radius=0.2, width=9.2, height=0.8, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.1),
                       T("Which level sets most of the resistance?", 30)).move_to([0, -2.0, 0])
    o["card"][1].move_to(o["card"][0])
    o["b1"] = chip("arterioles", GREEN, 30).move_to([-2.4, -3.1, 0])
    o["b2"] = chip("capillaries", GREEN, 30).move_to([2.4, -3.1, 0])
    return o


class S08Predict(SpokenScene):
    def construct(self):
        self.add(eq_pinned())
        o = s8_layout(self)
        self.play(Create(o["ta"]), Create(o["tc"]), FadeIn(o["la"]), FadeIn(o["lc"]), run_time=1.0)
        self.add(o["da"], o["dc"])
        self.at("narrower than")
        self.play(Indicate(o["tc"], color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("resist more")
        self.play(GrowFromEdge(o["ba"], DOWN), FadeIn(o["bla"]), run_time=0.8)
        self.play(GrowFromEdge(o["bc"], DOWN), FadeIn(o["blc"]), run_time=1.0)
        self.play(FadeIn(o["note"]), run_time=0.6)
        self.at("So which level")
        self.play(FadeIn(o["card"], shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(o["b1"]), FadeIn(o["b2"]), run_time=0.7)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        self.add(eq_pinned())
        o = s8_layout(self)
        for k in ["ta", "tc", "la", "lc", "da", "dc", "ba", "bc", "bla", "blc", "note", "card", "b1", "b2"]:
            self.add(o[k])
        fr = ValueTracker(1.0)
        ring = always_redraw(lambda: VGroup(Circle(radius=0.38, stroke_color=GREY, stroke_width=3),
                                            Arc(radius=0.38, start_angle=PI / 2, angle=-TAU * max(fr.get_value(), 0.001), stroke_color=GOLD,
                                                stroke_width=8)).move_to([6.0, -3.1, 0]))
        self.add(fr, ring)
        self.play(fr.animate.set_value(0.0), run_time=4.8, rate_func=linear)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        self.add(eq_pinned())
        o = s8_layout(self)
        for k in ["ta", "tc", "la", "da", "dc", "ba", "bc", "bla", "blc", "note", "card", "b1", "b2"]:
            self.add(o[k])
        self.add(o["lc"])
        self.at("arterials")
        self.play(o["b1"][0].animate.set_fill(GOLD, 0.6).set_stroke(GOLD), FadeOut(o["card"]), run_time=0.8)
        self.at("Most capillaries")
        self.play(FadeOut(o["note"]), FadeOut(o["lc"]), run_time=0.5)
        # capillary slides to the arteriole's end: one arteriole feeds it
        man = Line([-3.4, 1.7, 0], [-3.4, -2.3, 0]).set_stroke(SLATE, 10)
        self.play(Create(man), run_time=0.8)
        newc = tube_rect(-3.2, -0.6, 0.2, 0.16)
        self.play(FadeOut(o["tc"]), FadeOut(o["dc"]), FadeIn(newc), run_time=1.0)
        d0 = stream(-3.1, -0.7, 4, lambda: 1.0, lambda x: (0.2, 0.02), seed=5, r=0.05)
        self.add(d0)
        self.play(Indicate(newc, color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("side by side in")
        tubes, dd = [], []
        for n, y in enumerate([0.7, -0.3, -0.8, -1.3, -1.8, -2.3]):
            t = tube_rect(-3.2, -0.6, y, 0.16)
            d = stream(-3.1, -0.7, 4, lambda: 0.8, lambda x, y=y: (y, 0.02), seed=20 + n, r=0.05)
            tubes.append(t)
            dd.append(d)
            self.play(Create(t), run_time=0.35)
            self.add(d)
        fl1 = T("many side by side", 28).move_to([2.8, -1.75, 0])
        fl2 = T("schematic: real beds also branch and rejoin", 22, GREY).move_to([2.8, -2.3, 0])
        self.play(FadeIn(fl1), FadeIn(fl2), run_time=0.6)
        self.at("share the flow")
        self.play(*[Indicate(t, color=GOLD, scale_factor=1.0) for t in tubes], run_time=1.2)
        self.at("resist less")
        nl = T("capillaries together", 28).move_to([4.0, -1.15, 0])
        self.play(o["bc"].animate.stretch_to_fit_height(0.5, about_edge=DOWN), Transform(o["blc"], nl), run_time=1.6)
        self.finish()


class S11Sameflow(TreeBase):
    def construct(self):
        self.tree()
        self.at("In this simplified")
        n1 = T("steady state", 26, GREY).move_to([4.6, 3.45, 0])
        n2 = T("simplified tree, no shunts", 26, GREY).move_to([4.2, 3.0, 0])
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.6)
        self.at("bypasses the")
        box = SurroundingRectangle(self.G["caps"], color=GOLD, buff=0.15, stroke_width=4)
        self.play(Create(box), run_time=0.8)
        self.play(FadeOut(box), run_time=0.8)
        self.at("same flow")
        ga = Line([-5.95, Y0 - 0.5, 0], [-5.95, Y0 + 0.5, 0], color=GOLD, stroke_width=8)
        gc = Line([-0.05, CY[0] - 0.2, 0], [-0.05, CY[-1] + 0.2, 0], color=GOLD, stroke_width=8)
        la = T("5 L per min", 28, GOLD).move_to([-5.5, 0.9, 0])
        lc = T("5 L per min", 28, GOLD).move_to([-0.05, 2.2, 0])
        ph = ValueTracker(0)
        self.add(ph)
        tick = lambda x, y: always_redraw(lambda: Dot([x, y, 0], radius=0.1 + 0.08 * max(0, np.sin(ph.get_value())), color=GOLD))
        ta, tc = tick(-5.95, Y0 + 0.75), tick(-0.05, CY[-1] + 0.55)
        self.play(Create(ga), Create(gc), run_time=0.7)
        self.play(FadeIn(la), FadeIn(lc), FadeIn(ta), FadeIn(tc), run_time=0.5)
        self.play(ph.animate.set_value(6 * PI), run_time=3.0, rate_func=linear)
        self.finish()


class S12Area(TreeBase):
    def construct(self):
        self.tree()
        v = M("velocity = flow / total area", 28, TEAL).move_to([3.4, 3.4, 0])
        self.play(FadeIn(v), run_time=0.7)
        slots = {"aorta": (-5.95, 0.9, 0.3), "arteries": (-4.4, 1.0, 0.6), "arterioles": (-2.5, 1.6, 1.2),
                 "caps": (-0.05, 2.2, 4.4), "veins": (2.35, 1.5, 1.8)}
        bars = {}
        for k, (x, w, h) in slots.items():
            b = Rectangle(width=w, height=h, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to([x, -3.0 + h / 2, 0])
            b.set_z_index(-1)
            bars[k] = b
        self.at("total cross")
        for k in ["aorta", "arteries", "arterioles", "veins"]:
            self.play(GrowFromEdge(bars[k], DOWN), run_time=0.5)
        l4 = VGroup(T("about 4", 26, TEAL), T("cm\u00b2", 26, TEAL)).arrange(DOWN, buff=0.05).move_to([-5.95, -2.05, 0])
        self.play(FadeIn(l4), run_time=0.4)
        self.at("Each capillary")
        one = Line([-1.2, CY[5], 0], [1.1, CY[5], 0]).set_stroke(GOLD, 8)
        self.play(Create(one), run_time=0.6)
        self.play(Indicate(one, color=GOLD, scale_factor=1.0), run_time=1.0)
        self.at("But together")
        self.play(FadeOut(one), GrowFromEdge(bars["caps"], DOWN), run_time=2.2)
        l3k = T("about 3,000 cm²", 28, TEAL).move_to([-0.05, 1.8, 0])
        self.play(FadeIn(l3k), run_time=0.5)
        self.finish()


class S13Slow(TreeBase):
    def construct(self):
        self.tree()
        v = M("velocity = flow / total area", 28, TEAL).move_to([3.4, 3.4, 0])
        self.add(v)
        slots = {"aorta": (-5.95, 0.9, 0.3), "arteries": (-4.4, 1.0, 0.6), "arterioles": (-2.5, 1.6, 1.2),
                 "caps": (-0.05, 2.2, 4.4), "veins": (2.35, 1.5, 1.8)}
        bars = {}
        for k, (x, w, h) in slots.items():
            b = Rectangle(width=w, height=h, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to([x, -3.0 + h / 2, 0])
            b.set_z_index(-1)
            bars[k] = b
            self.add(b)
        self.play(self.tm.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
        self.wait(0.1)
        la = T("about 21 cm/s", 28, RED).move_to([-5.3, 0.95, 0])
        self.play(FadeIn(la), run_time=0.5)
        self.at("slowly")
        lc = T("about 0.03 cm/s", 28, RED).move_to([-0.05, 1.8, 0])
        self.play(FadeIn(lc), run_time=0.5)
        self.at("creeps through")
        for _ in range(2):
            self.play(bars["caps"].animate.set_fill(TEAL, 0.75), run_time=0.5)
            self.play(bars["caps"].animate.set_fill(TEAL, 0.4), run_time=0.5)
        self.at("narrowest vessels")
        self.play(Indicate(self.G["caps"], color=GOLD, scale_factor=1.0), run_time=1.3)
        self.finish()


class S14Answer(SpokenScene):
    def construct(self):
        self.add(eq_pinned())
        sp = ValueTracker(3.4)
        one = tube_rect(-6.3, 2.8, 0.5, 0.7)
        d1 = stream(-6.2, 2.7, 12, lambda: sp.get_value(), lambda x: (0.5, 0.22), seed=3, r=0.09)
        self.play(Create(one), run_time=0.8)
        self.add(sp, d1)
        self.play(FadeIn(d1), run_time=0.4)
        self.at("narrow tube carrying")
        l1 = T("one narrow tube: faster", 36, YELLOW).move_to([0, -2.5, 0])
        self.play(FadeIn(l1), run_time=0.6)
        self.at("What matters")
        ys = [2.1, 1.3, -0.3, -1.1]
        tubes, ds = [], []
        for n, y in enumerate(ys):
            t = tube_rect(-6.3, 2.8, y, 0.7)
            d = stream(-6.2, 2.7, 6, lambda: sp.get_value(), lambda x, y=y: (y, 0.22), seed=30 + n, r=0.09)
            tubes.append(t)
            ds.append(d)
        l2 = T("many in parallel: slower", 36, TEAL).move_to([0, -2.5, 0])
        self.play(*[FadeIn(t) for t in tubes], *[FadeIn(d) for d in ds], sp.animate.set_value(0.7), FadeOut(l1), run_time=2.0)
        for d in ds:
            self.add(d)
        self.play(FadeIn(l2), run_time=0.5)
        br = Brace(VGroup(tubes[0], tubes[-1]), direction=RIGHT, color=TEAL)
        tw = T("total width", 28, TEAL).next_to(br, RIGHT, buff=0.15)
        self.play(Create(br), FadeIn(tw), run_time=0.9)
        self.finish()


class S15Bridge(SpokenScene):
    def construct(self):
        eq = eq_pinned()
        self.add(eq)
        cap = tube_rect(-5.5, 5.5, 0.0, 1.3)
        dd = stream(-5.4, 5.4, 14, lambda: 0.5, lambda x: (0.0, 0.4), seed=11, r=0.09)
        self.play(Create(cap), run_time=0.8)
        self.add(dd)
        self.play(FadeIn(dd), run_time=0.5)
        self.at("trade with")
        self.play(Indicate(cap, color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("fluid crossing")
        ars = []
        for x in [-4.0, -2.4, -0.8, 0.8, 2.4, 4.0]:
            for s in (1, -1):
                ars.append(Arrow([x, s * 0.5, 0], [x, s * 1.7, 0], color=ORANGE, buff=0, stroke_width=7, tip_length=0.25))
        self.play(LaggedStart(*[GrowArrow(a) for a in ars], lag_ratio=0.08), run_time=1.5)
        bl = []
        for x in [-3.2, 3.2]:
            for s in (1, -1):
                bl.append(Arrow([x, s * 2.4, 0], [x, s * 0.7, 0], color=BLUE, buff=0, stroke_width=7, tip_length=0.25))
        self.play(LaggedStart(*[GrowArrow(a) for a in bl], lag_ratio=0.1), run_time=1.0)
        self.at("pressure difference")
        box = SurroundingRectangle(eq, color=GOLD, buff=0.12, stroke_width=4)
        self.play(Create(box), run_time=0.6)
        self.play(Indicate(eq, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.finish()


class S16End(EndCard):
    LINE = "Flow follows a pressure difference, divided by the resistance."
