"""A Field Is a Sum: biodiversity and ecosystem function (chapter 1).

COLOUR MAP: species A GOLD; B TEAL; others CORAL, SLATE, SAND; complementarity GREEN;
selection VIOLET; a plot's total = a white OUTLINE (dark outline on a cream ground; the film
ground is dark); expected yield = DASHED grey bar. Bars from stated numbers are labelled
computed; the rest schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403
from bp_style import SpokenScene, TitleCard, EndCard, T, M, chip, GOLD, TEAL

CORAL = "#FF7F6B"
SLATE = "#7C8FE8"
SAND = "#E8D5A3"
VIOLET = "#B28DFF"
OUT = "#FFFFFF"
SP = [GOLD, TEAL, CORAL, SLATE]

BASE = -2.7
K = 0.0115
BW = 1.9
X_A, X_B, X_E, X_M, X_G = -5.0, -3.0, -0.6, 1.8, 4.4
XS, SW = -4.9, 2.4          # stack column
K8, K9 = 0.04, 0.015        # vertical scales (one species alone / four stacked)
CX0, CXS = -1.2, 0.84       # chart x of year 0 and spacing


def yy(v, k=K):
    return BASE + v * k


# ---------------------------------------------------------------- data
def _make_z():
    rng = np.random.default_rng(11)
    for _ in range(3000):
        rows = []
        for _i in range(4):
            v = rng.standard_normal(10)
            v -= v.mean()
            for r in rows:
                v -= (v @ r) / (r @ r) * r
            rows.append(v)
        Zs = [r / np.sqrt((r @ r) / 10) for r in rows]
        mn = min((50 + 25 * z).min() for z in Zs)
        tot = sum(50 + 25 * z for z in Zs)
        if mn > 3 and max(abs(z).max() for z in Zs) < 2.1:
            return Zs
    return Zs


Z = _make_z()


def year_val(j, i, s):
    return 50 + 25 * ((1 - s) * Z[i][j] + s * Z[0][j])


def interp_val(yr, i, s):
    i0 = int(yr) % 10
    i1 = (i0 + 1) % 10
    f = yr - int(yr)
    f = f * f * (3 - 2 * f)
    return year_val(i0, i, s) * (1 - f) + year_val(i1, i, s) * f


class Run:
    def __init__(self, kk=K9, nsp=4):
        self.yr = ValueTracker(0.0)
        self.sync = ValueTracker(0.0)
        self.kk = ValueTracker(kk)
        self.nsp = ValueTracker(nsp)
        self.ol = ValueTracker(0.0)
        self.speed = 0.0
        self.cyc = False

        def up(m, dt):
            v = m.get_value() + dt * self.speed
            v = v % 10 if self.cyc else min(v, 9.0)
            m.set_value(v)
        self.yr.add_updater(up)

    def vals(self):
        return [interp_val(self.yr.get_value(), i, self.sync.get_value()) for i in range(4)]


def stack(R, x=XS, w=SW, base=BASE):
    def f():
        g = VGroup()
        y = base
        k = R.kk.get_value()
        n = R.nsp.get_value()
        vs = R.vals()
        for i, (v, c) in enumerate(zip(vs, SP)):
            a = float(np.clip(n - i, 0, 1))
            h = max(v * k * a, 0.001)
            r = Rectangle(width=w, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.7)
            r.move_to([x, y + h / 2, 0])
            g.add(r)
            y += h
        if R.ol.get_value() > 0.5:
            g.add(Rectangle(width=w + 0.08, height=y - base, stroke_color=OUT, stroke_width=6).move_to([x, (y + base) / 2, 0]))
        return g
    return always_redraw(f)


def trace(R, kind, color, tot_mult=1):
    """kind: species index, or 'tot'."""
    def f():
        v = R.yr.get_value()
        k = R.kk.get_value()
        s = R.sync.get_value()
        n = int(v)

        def val(j):
            if kind == "tot":
                return sum(year_val(j, i, s) for i in range(4))
            return year_val(j, kind, s)
        if kind != "tot" and R.nsp.get_value() < kind + 0.5:
            return VGroup()
        pts = [[CX0 + j * CXS, BASE + val(j) * k, 0] for j in range(n + 1)]
        if n < 9:
            fr = v - n
            fr = fr * fr * (3 - 2 * fr)
            val_now = val(n) * (1 - fr) + val(n + 1) * fr
            pts.append([CX0 + v * CXS, BASE + val_now * k, 0])
        if len(pts) < 2:
            pts.append([pts[0][0] + 0.01, pts[0][1], 0])
        m = VMobject(stroke_color=color, stroke_width=5 if kind == "tot" else 3.5)
        m.set_points_as_corners(pts)
        d = Dot(pts[-1], radius=0.07, color=color)
        return VGroup(m, d)
    return always_redraw(f)


# ---------------------------------------------------------------- pictures
def tuft(color, h=1.0, w=1.0):
    g = VGroup(*[Line(ORIGIN, [dx * w, hh * h, 0], color=color, stroke_width=5)
                 for dx, hh in [(-0.22, 0.7), (0, 1), (0.22, 0.85)]])
    base = Dot(ORIGIN, radius=0.001).set_opacity(0)
    g.add(base)
    g.base = base
    return g


def sway(g, amp=0.07, speed=1.5, phase=0.0):
    st = {"t": phase, "a": 0.0}

    def up(m, dt):
        st["t"] += dt
        a = amp * np.sin(speed * st["t"])
        m.rotate(a - st["a"], about_point=m.base.get_center())
        st["a"] = a
    g.add_updater(up)
    return g


def put(g, x, y):
    g.shift(np.array([x, y, 0]) - g.base.get_center())
    return g


COLS16 = ([GOLD, TEAL, CORAL, SLATE, SAND] * 4)[:16]


def plot_box(cx, cy, size, colors, n, hs=None, seed=0):
    box = Rectangle(width=size, height=size, stroke_color=GREY, stroke_width=3,
                    fill_color="#1b2a1f", fill_opacity=1).move_to([cx, cy, 0])
    rng = np.random.default_rng(seed)
    tufts = VGroup()
    sp = size / n
    for idx, c in enumerate(colors):
        i, j = divmod(idx, n)
        t = tuft(c, h=(hs[idx] if hs else 0.55 + 0.2 * rng.random()), w=1.0)
        put(t, cx + (j - (n - 1) / 2) * sp, cy + ((n - 1) / 2 - i) * sp - sp * 0.42)
        sway(t, phase=rng.random() * 6)
        tufts.add(t)
    return box, tufts


def hbar(x, v, color, k=K, w=BW, op=0.55):
    return Rectangle(width=w, height=v * k, stroke_color=color, stroke_width=3,
                     fill_color=color, fill_opacity=op).move_to([x, BASE + v * k / 2, 0])


def baseline(x0=-6.4, x1=6.4):
    return Line([x0, BASE, 0], [x1, BASE, 0], color=GREY, stroke_width=3)


def name(text, x, color=TEXT, size=28):
    return T(text, size, color).move_to([x, BASE - 0.45, 0])


def vlabel(text, mob, color=TEXT, size=30):
    return M(text, size, color).next_to(mob, UP, buff=0.12)


def tag(text, y=-3.62, x=0.0):
    return T(text, 22, GREY).move_to([x, y, 0])


def mix_group(x, k, base=BASE, w=BW):
    ga = Rectangle(width=w, height=300 * k, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.55)
    ga.move_to([x, base + 150 * k, 0])
    gb = Rectangle(width=w, height=100 * k, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.55)
    gb.move_to([x, base + 350 * k, 0])
    ol = Rectangle(width=w + 0.08, height=400 * k, stroke_color=OUT, stroke_width=6).move_to([x, base + 200 * k, 0])
    return VGroup(ga, gb, ol)


def dashed_bar(x, v=250, k=K, base=BASE, w=BW):
    r = Rectangle(width=w, height=v * k).move_to([x, base + v * k / 2, 0])
    d = DashedVMobject(r, num_dashes=40).set_stroke(GREY, 4)
    fill = Rectangle(width=w, height=v * k, stroke_width=0, fill_color=GREY, fill_opacity=0.12).move_to(r)
    return VGroup(fill, d)


def bracket(x, y0, y1, color=YELLOW):
    return VGroup(Line([x, y0, 0], [x, y1, 0]), Line([x - 0.15, y0, 0], [x + 0.15, y0, 0]),
                  Line([x - 0.15, y1, 0], [x + 0.15, y1, 0])).set_stroke(color, 5)


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    TITLE = "A Field Is a Sum"
    LESSON = "Biodiversity and Ecosystem Function"


class S01Question(SpokenScene):
    def construct(self):
        boxR, tR = plot_box(4.2, -0.3, 3.6, [COLS16[i] if i < 15 else GREEN for i in range(16)], 4, seed=1)
        boxL, tL = plot_box(-4.2, -0.3, 3.6, [GOLD] * 9, 3, hs=[0.8] * 9, seed=2)
        self.play(FadeIn(boxR), run_time=0.3)
        self.play(LaggedStart(*[GrowFromPoint(t, t.base.get_center()) for t in tR], lag_ratio=0.06, run_time=1.4))
        lR = T("16 species", 32).next_to(boxR, DOWN, buff=0.25)
        self.play(FadeIn(lR), run_time=0.3)
        self.at("instead of one")
        self.play(FadeIn(boxL), run_time=0.3)
        self.play(LaggedStart(*[GrowFromPoint(t, t.base.get_center()) for t in tL], lag_ratio=0.08, run_time=0.8))
        lL = T("1 species", 32).next_to(boxL, DOWN, buff=0.25)
        self.play(FadeIn(lL), run_time=0.3)
        self.at("Why would that field grow more")
        bio = VGroup(T("biomass", 38), T("?", 60, YELLOW)).arrange(RIGHT, buff=0.2).move_to([0, 1.5, 0])
        self.play(FadeIn(bio, scale=1.2), run_time=0.6)
        self.play(Indicate(bio[1], color=YELLOW, scale_factor=1.4), run_time=1.0)
        self.at("And why would its total change less")
        tt = ValueTracker(0)
        tt.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(tt)
        wig = always_redraw(lambda: ParametricFunction(
            lambda u: np.array([u, 0.28 * np.sin(5 * u + 3 * tt.get_value()) * (1 + 0.4 * np.sin(2 * u)), 0]),
            t_range=[-1.5, 1.5], stroke_color=TEXT, stroke_width=5).move_to([0, -0.2, 0]))
        yl = VGroup(T("year to year", 34), T("?", 60, YELLOW)).arrange(RIGHT, buff=0.2).move_to([0, -1.2, 0])
        self.play(FadeIn(wig), FadeIn(yl, scale=1.2), run_time=0.8)
        self.play(Indicate(yl[1], color=YELLOW, scale_factor=1.4), run_time=1.0)
        self.add(tag("schematic"))
        self.finish()


class S02Sum(SpokenScene):
    def construct(self):
        boxR, tR = plot_box(4.2, -0.3, 3.6, [COLS16[i] if i < 15 else GREEN for i in range(16)], 4, seed=1)
        self.add(boxR, tR)
        self.at("A plot's production")
        for t in tR:
            t.clear_updaters()
        w = np.array([0.7, 1.2, 0.9, 1.4, 0.6, 1.1, 1.0, 0.8, 1.3, 0.7, 1.2, 0.9, 1.0, 0.6, 1.4, 0.9])
        hs = 4.8 * w / w.sum()
        bars = VGroup()
        y = BASE
        for i in range(16):
            r = Rectangle(width=2.0, height=hs[i], stroke_color=BG, stroke_width=1.5, fill_color=tR[i][0].get_color(), fill_opacity=0.8)
            r.move_to([0.4, y + hs[i] / 2, 0])
            y += hs[i]
            bars.add(r)
        self.play(LaggedStart(*[t.animate.shift(UP * 0.35) for t in tR], lag_ratio=0.03, run_time=0.5))
        self.play(LaggedStart(*[ReplacementTransform(tR[i], bars[i]) for i in range(16)], lag_ratio=0.07, run_time=2.0))
        self.at("produces")
        ol = Rectangle(width=2.08, height=4.8, stroke_color=OUT, stroke_width=6).move_to([0.4, BASE + 2.4, 0])
        self.play(Create(ol), run_time=0.6)
        lab = T("total =\nsum of species", 32, TEXT).move_to([-3.9, 1.6, 0])
        self.play(FadeIn(lab, shift=RIGHT * 0.2), run_time=0.5)
        self.at("Every year")
        each = T("each year", 30, GREY).move_to([-3.9, 0.0, 0])
        self.play(FadeIn(each), run_time=0.5)
        xs = [-5.4, -3.9, -2.4]
        # shears
        sh = VGroup(Line([-.3, .35, 0], [.3, -.35, 0]), Line([-.3, -.35, 0], [.3, .35, 0])).set_stroke(SAND, 5)
        sh.add(Circle(0.12, color=SAND).move_to([-.3, -.35, 0]), Circle(0.12, color=SAND).move_to([.3, -.35, 0]))
        sh.move_to([xs[0], -0.9, 0])
        ov = VGroup(RoundedRectangle(corner_radius=0.1, width=0.9, height=0.75, stroke_color=CORAL, stroke_width=4),
                    *[Line([dx, -.15, 0], [dx, .15, 0]).set_stroke(CORAL, 4) for dx in (-.25, 0, .25)])
        ov.move_to([xs[1], -0.9, 0])
        pan = VGroup(Line([-.45, .2, 0], [.45, .2, 0]), Triangle().scale(0.2).move_to([0, -.15, 0]),
                     Arc(radius=.2, start_angle=PI, angle=PI).move_to([-.4, .0, 0]).rotate(PI),
                     Arc(radius=.2, start_angle=PI, angle=PI).move_to([.4, .0, 0]).rotate(PI)).set_stroke(TEAL, 4)
        pan.move_to([xs[2], -0.9, 0])
        words = [T("clip", 28), T("dry", 28), T("weigh", 28)]
        icons = [sh, ov, pan]
        for wd, ic, x in zip(words, icons, xs):
            wd.move_to([x, -1.7, 0])
        self.play(FadeIn(sh, shift=RIGHT * 0.4), FadeIn(words[0]), run_time=0.7)
        self.play(Rotate(sh, angle=0.3, rate_func=there_and_back), run_time=0.6)
        self.at("dry them")
        self.play(FadeIn(ov, shift=RIGHT * 0.4), FadeIn(words[1]), run_time=0.7)
        self.at("weigh them")
        self.play(FadeIn(pan, shift=RIGHT * 0.4), FadeIn(words[2]), run_time=0.7)
        self.play(Rotate(pan, angle=0.15, rate_func=there_and_back), run_time=0.9)
        self.add(tag("schematic", x=-3.9))
        self.finish()


def mono_world(scene, with_B=True, tickers=True):
    bl = baseline()
    unit = tag("g dry biomass per m², computed")
    head = T("monoculture", 34).move_to([-4.0, 3.3, 0])
    barA = hbar(X_A, 400, GOLD)
    barB = hbar(X_B, 100, TEAL)
    return bl, unit, head, barA, barB


class S03Mono(SpokenScene):
    def construct(self):
        bl, unit, head, barA, barB = mono_world(self)
        self.play(FadeIn(bl), FadeIn(unit), FadeIn(head), run_time=0.6)
        tA = put(tuft(GOLD, 1.0, 1.4), X_A, BASE)
        sway(tA)
        nA = name("A alone", X_A, GOLD)
        self.play(GrowFromPoint(tA, tA.base.get_center()), FadeIn(nA), run_time=0.8)
        self.at("gold")
        self.play(Indicate(tA, color=GOLD, scale_factor=1.3), run_time=0.9)
        self.at("It makes a tall")
        barA.save_state()
        vA = always_redraw(lambda: M(str(int(round(barA.height / K))), 30, GOLD).next_to(barA, UP, buff=0.12))
        self.add(vA)
        self.play(FadeOut(tA), GrowFromEdge(barA, DOWN), run_time=2.0)
        self.at("Grow species B")
        tB = put(tuft(TEAL, 0.8, 1.2), X_B, BASE)
        sway(tB, phase=1)
        nB = name("B alone", X_B, TEAL)
        self.play(GrowFromPoint(tB, tB.base.get_center()), FadeIn(nB), run_time=0.8)
        self.at("teal")
        self.play(Indicate(tB, color=TEAL, scale_factor=1.3), run_time=0.9)
        self.at("It makes a short")
        vB = always_redraw(lambda: M(str(int(round(barB.height / K))), 30, TEAL).next_to(barB, UP, buff=0.12))
        self.add(vB)
        self.play(FadeOut(tB), GrowFromEdge(barB, DOWN), run_time=1.0)
        self.play(Indicate(barA, color=GOLD, scale_factor=1.03), run_time=1.0)
        self.finish()


class S04Expect(SpokenScene):
    def construct(self):
        bl, unit, head, barA, barB = mono_world(self)
        nA, nB = name("A alone", X_A, GOLD), name("B alone", X_B, TEAL)
        vA, vB = vlabel("400", barA, GOLD), vlabel("100", barB, TEAL)
        self.add(bl, unit, head, barA, barB, nA, nB, vA, vB)
        self.at("them half and half")
        box, tf = plot_box(-0.6, 2.75, 1.3, [GOLD, GOLD, TEAL, TEAL], 2, hs=[0.35] * 4, seed=3)
        sown = T("sown 50 : 50", 30).move_to([2.6, 2.75, 0])
        self.play(FadeIn(box), FadeIn(sown), run_time=0.5)
        self.play(LaggedStart(*[GrowFromPoint(t, t.base.get_center()) for t in tf], lag_ratio=0.2, run_time=1.2))
        self.at("If mixing neither")
        no = T("no help, no harm", 32, YELLOW).move_to([-0.6, 1.4, 0])
        self.play(Write(no), run_time=1.2)
        self.at("each species would")
        self.play(FadeOut(no), run_time=0.3)
        cA = Rectangle(width=BW, height=200 * K, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.8).move_to([X_A, yy(100), 0])
        cB = Rectangle(width=BW, height=50 * K, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.8).move_to([X_B, yy(25), 0])
        tA = M("200", 26, BG).move_to(cA)
        tB = M("50", 26, BG).move_to(cB)
        gA, gB = VGroup(cA, tA), VGroup(cB, tB)
        self.add(gA, gB)
        self.play(gA.animate.move_to([X_E, yy(100), 0]), run_time=0.9)
        self.at("half of its yield")
        self.play(gB.animate.move_to([X_E, yy(225), 0]), run_time=1.4)
        self.at("That gives the dashed bar")
        db = dashed_bar(X_E)
        self.play(FadeOut(gA), FadeOut(gB), FadeIn(db), run_time=1.3)
        self.at("expected yield")
        nE = name("expected", X_E, GREY)
        vE = vlabel("250", db, GREY)
        self.play(FadeIn(nE), FadeIn(vE), Indicate(db, color=GREY, scale_factor=1.04), run_time=1.2)
        self.finish()


class S05Extra(SpokenScene):
    def construct(self):
        bl = baseline()
        unit = tag("g dry biomass per m², computed")
        db = dashed_bar(X_E)
        nE = name("expected", X_E, GREY)
        vE = vlabel("250", db, GREY)
        ghost = hbar(X_A, 400, GOLD, op=0.18)
        nG = name("A alone", X_A, GOLD)
        self.add(bl, unit, db, nE, vE, ghost, nG)
        self.at("real mixture")
        mg = mix_group(X_M, K)
        self.play(GrowFromEdge(mg[0], DOWN), run_time=1.5)
        self.play(GrowFromEdge(mg[1], DOWN), run_time=0.9)
        nM = name("mixture", X_M)
        self.play(Create(mg[2]), FadeIn(nM), run_time=0.8)
        self.at("That gap")
        guide = DashedLine([X_E + BW / 2, yy(250), 0], [X_M - BW / 2, yy(250), 0], color=GREY, stroke_width=3)
        br = bracket(0.6, yy(250), yy(400))
        self.play(Create(guide), Create(br), run_time=1.0)
        ex = VGroup(T("extra yield:", 32), M("+150", 32, YELLOW)).arrange(RIGHT, buff=0.2)
        ex.move_to([-1.9, 1.3, 0])
        ex.align_to(np.array([0.35, 0, 0]), RIGHT)
        self.play(FadeIn(ex, shift=LEFT * 0.2), run_time=0.8)
        self.at("With an even sowing")
        bm = T("benchmark =\naverage monoculture", 30).move_to([-3.4, 3.0, 0])
        self.play(FadeIn(bm), run_time=0.8)
        self.at("average monoculture")
        self.play(Indicate(db, color=GREY, scale_factor=1.05), run_time=1.0)
        self.at("not the best one")
        self.play(FadeOut(bm), FadeOut(ghost), FadeOut(nG), run_time=0.6)
        ghost.move_to([X_G, yy(200), 0])
        nG.move_to([X_G, BASE - 0.45, 0])
        self.play(FadeIn(ghost), FadeIn(nG), run_time=0.9)
        vG = vlabel("400", ghost, GOLD)
        bst = T("best monoculture", 28, GOLD).next_to(vG, UP, buff=0.1)
        self.play(FadeIn(vG), FadeIn(bst), run_time=0.6)
        self.at("only matches")
        eq = Line([X_M - BW / 2 - 0.1, yy(400), 0], [X_G - BW / 2, yy(400), 0], color=OUT, stroke_width=4)
        eqm = M("=", 44, OUT).move_to([3.1, yy(400) - 0.45, 0])
        self.play(Create(eq), FadeIn(eqm), Indicate(mg[2], color=OUT), Indicate(ghost, color=GOLD), run_time=1.5)
        self.finish()


class S06Two(SpokenScene):
    def construct(self):
        bl = baseline()
        db = dashed_bar(X_E)
        nE = name("expected", X_E, GREY)
        mg = mix_group(X_M, K)
        nM = name("mixture", X_M)
        guide = DashedLine([X_E + BW / 2, yy(250), 0], [X_M - BW / 2, yy(250), 0], color=GREY, stroke_width=3)
        br = bracket(0.6, yy(250), yy(400))
        ex = M("+150", 32, YELLOW).move_to([0.6, yy(325), 0]).shift(LEFT * 0.0)
        ex.next_to(br, LEFT, buff=0.12).shift(UP * 0.0)
        self.add(bl, db, nE, mg, nM, guide, br, ex)
        q = T("?", 64, YELLOW).move_to([-1.9, 1.4, 0])
        self.play(FadeIn(q, scale=1.4), Indicate(br, color=YELLOW), run_time=1.2)
        self.at("Perhaps the species")
        self.play(FadeOut(q), run_time=0.3)
        # left panel: roots and light
        ground = Line([-6.4, -0.2, 0], [-2.8, -0.2, 0], color=SAND, stroke_width=4)
        tg = put(tuft(GOLD, 1.0, 1.2), -5.6, -0.2)
        tt = put(tuft(TEAL, 0.7, 1.0), -3.8, -0.2)
        sway(tg)
        sway(tt, phase=2)
        rg = VGroup(Line([-5.6, -0.2, 0], [-5.6, -2.3, 0]), Line([-5.6, -1.3, 0], [-5.3, -1.9, 0]),
                    Line([-5.6, -1.0, 0], [-5.9, -1.6, 0])).set_stroke(GOLD, 4)
        rt = VGroup(Line([-3.8, -0.2, 0], [-3.1, -0.8, 0]), Line([-3.8, -0.2, 0], [-4.5, -0.8, 0]),
                    Line([-3.8, -0.2, 0], [-3.8, -0.9, 0])).set_stroke(TEAL, 4)
        sun = Circle(0.3, color=YELLOW, fill_opacity=0.9, stroke_width=0).move_to([-4.6, 1.9, 0])
        rays = VGroup(*[Line(0.45 * np.array([np.cos(a), np.sin(a), 0]), 0.65 * np.array([np.cos(a), np.sin(a), 0])).set_stroke(YELLOW, 4)
                        for a in np.linspace(0, 2 * PI, 9)[:-1]]).move_to(sun)
        rays.add_updater(lambda m, dt: m.rotate(0.6 * dt, about_point=sun.get_center()))
        self.play(Create(ground), FadeIn(tg), FadeIn(tt), run_time=0.8)
        self.play(Create(rg), Create(rt), FadeIn(sun), FadeIn(rays), run_time=1.5)
        self.at("help each other")
        nod = VGroup(*[Circle(0.1, color=GREEN, fill_opacity=1, stroke_width=0).move_to(p) for p in ([-4.5, -0.8, 0], [-3.1, -0.8, 0], [-3.8, -0.9, 0])])
        nl = T("nodule", 26, GREEN).move_to([-3.8, -1.35, 0])
        self.play(FadeIn(nod, scale=2), FadeIn(nl), run_time=0.9)
        self.at("That is complementarity")
        ch = chip("complementarity", GREEN, 30).move_to([-4.6, 3.1, 0])
        self.play(FadeIn(ch, shift=DOWN * 0.2), run_time=0.8)
        # right panel
        self.at("Or a richer draw")
        xs = [3.8, 4.9, 6.0]
        mono = [0.9, 1.2, 3.2]
        mixh = [1.0, 1.3, 4.3]
        cols = [CORAL, SAND, SLATE]
        monos = VGroup()
        mixs = VGroup()
        for x, m_, h, c in zip(xs, mono, mixh, cols):
            monos.add(Rectangle(width=0.4, height=m_, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.1).move_to([x - 0.22, BASE + m_ / 2, 0]))
            mixs.add(Rectangle(width=0.4, height=h, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.6).move_to([x + 0.22, BASE + h / 2, 0]))
        self.play(GrowFromEdge(monos[0], DOWN), GrowFromEdge(monos[1], DOWN), run_time=1.0)
        self.at("a species that yields")
        self.play(GrowFromEdge(monos[2], DOWN), run_time=1.2)
        hy = T("high yield alone", 26, SLATE).move_to([5.2, BASE + 3.2 + 0.4, 0])
        self.play(FadeIn(hy), run_time=0.6)
        self.at("If such high yielding")
        self.play(FadeOut(hy), LaggedStart(*[GrowFromEdge(m, DOWN) for m in mixs], lag_ratio=0.2, run_time=2.2))
        self.at("gain the most relative")
        box = SurroundingRectangle(VGroup(monos[2], mixs[2]), color=VIOLET, buff=0.1, stroke_width=4)
        self.play(Create(box), run_time=0.8)
        self.at("that is selection")
        cs = chip("selection", VIOLET, 30).move_to([4.8, 3.1, 0])
        self.play(FadeIn(cs, shift=DOWN * 0.2), run_time=0.8)
        self.at("Both can act")
        plus = M("+", 50, TEXT).move_to([0.9, 3.1, 0])
        both = T("both can act at once", 28, TEXT).move_to([0.9, 2.5, 0])
        self.play(FadeIn(plus, scale=1.5), FadeIn(both), run_time=0.9)
        self.add(tag("schematic", x=0.0))
        self.finish()


class S07Random(SpokenScene):
    def construct(self):
        meadow = Rectangle(width=5.6, height=3.8, stroke_color=GREY, stroke_width=3, fill_color="#1b2a1f", fill_opacity=1).move_to([-3.4, -0.2, 0])
        rng = np.random.default_rng(5)
        cs = [GOLD, TEAL, CORAL, SLATE, SAND, GREEN]
        tufts = VGroup()
        for i in range(22):
            t = tuft(cs[i % 6], 0.5 + 0.3 * rng.random())
            put(t, -3.4 + rng.uniform(-2.5, 2.5), -0.2 + rng.uniform(-1.6, 1.4))
            sway(t, phase=rng.random() * 6)
            tufts.add(t)
        self.play(FadeIn(meadow), run_time=0.4)
        self.play(LaggedStart(*[GrowFromPoint(t, t.base.get_center()) for t in tufts], lag_ratio=0.04, run_time=1.4))
        self.at("a wet patch")
        wet = Ellipse(width=2.6, height=1.5, stroke_color="#4AA3E0", stroke_width=4, fill_color="#4AA3E0", fill_opacity=0.35).move_to([-3.0, -0.9, 0])
        wl = T("wet soil", 30, "#4AA3E0").move_to([-3.4, -2.7, 0])
        self.play(FadeIn(wet, scale=0.5), FadeIn(wl), run_time=1.0)
        self.at("raise both")
        ms = T("more species", 34).move_to([3.4, 1.4, 0])
        mb = T("more biomass", 34).move_to([3.4, -0.9, 0])
        a1 = Arrow([-1.7, -0.6, 0], [1.2, 1.3, 0], color="#4AA3E0", buff=0.05, stroke_width=5)
        a2 = Arrow([-1.7, -0.9, 0], [1.2, -0.9, 0], color="#4AA3E0", buff=0.05, stroke_width=5)
        self.play(GrowArrow(a1), FadeIn(ms), run_time=0.9)
        self.play(GrowArrow(a2), FadeIn(mb), run_time=0.9)
        cf = T("wet soil: a confounder", 30, YELLOW).move_to([-3.4, -2.7, 0])
        self.play(Transform(wl, cf), run_time=0.9)
        self.at("To separate richness")
        self.play(FadeOut(VGroup(meadow, tufts, wet, ms, mb, a1, a2, wl)), run_time=0.4)
        n, cell = 4, 1.15
        cx, cy = -3.4, -0.3
        cells = VGroup()
        wetset = {1, 2, 6, 7, 8, 13}
        for idx in range(16):
            i, j = divmod(idx, n)
            c = Square(cell, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1)
            c.move_to([cx + (j - 1.5) * cell, cy + (1.5 - i) * cell, 0])
            cells.add(c)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.03, run_time=0.8))
        self.at("soil")
        self.play(*[cells[i].animate.set_fill("#4AA3E0", 0.35) for i in wetset], run_time=1.0)
        self.at("ecologists sow")
        rich = [2, 8, 1, 4, 16 if False else 8, 2, 4, 1, 4, 8, 2, 1, 1, 4, 8, 2]
        dots = VGroup()
        for idx, r_ in enumerate(rich):
            c = cells[idx]
            g = VGroup()
            for k_ in range(r_):
                a, b = divmod(k_, 3)
                g.add(Dot(c.get_center() + np.array([(b - 1) * 0.28, 0.3 - a * 0.28, 0]), radius=0.08, color=cs[k_ % 6]))
            dots.add(g)
        die = VGroup(RoundedRectangle(corner_radius=0.15, width=1.4, height=1.4, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1),
                     *[Dot([dx, dy, 0], radius=0.11, color=TEXT) for dx, dy in [(-.4, .4), (.4, .4), (0, 0), (-.4, -.4), (.4, -.4)]])
        die.move_to([3.4, 1.2, 0])
        die.add_updater(lambda m, dt: m.rotate(1.8 * dt))
        rl = T("richness assigned\nat random", 32).move_to([3.6, -0.6, 0])
        self.play(FadeIn(die), FadeIn(rl), LaggedStart(*[FadeIn(g, scale=1.5) for g in dots], lag_ratio=0.18, run_time=2.6))
        self.add(tag("schematic", x=0.0))
        self.finish()


def chart_frame(R, band=False):
    bl = Line([-1.8, BASE, 0], [6.5, BASE, 0], color=GREY, stroke_width=3)
    return bl


def year_counter(R):
    return always_redraw(lambda: T(f"year {int(R.yr.get_value()) % 10 + 1}", 30, GREY).move_to([-1.0, 3.3, 0]))


class S08Years(SpokenScene):
    def construct(self):
        R = Run(kk=K8, nsp=1)
        self.add(R.yr, R.kk)
        bl = baseline()
        R.ol.set_value(0)
        st = stack(R)
        trg = trace(R, 0, GOLD)
        mean_line = DashedLine([-1.5, yy(50, K8), 0], [6.5, yy(50, K8), 0], color=GREY, stroke_width=3)
        band = Rectangle(width=8.0, height=50 * K8, stroke_width=0, fill_color=GOLD, fill_opacity=0.14).move_to([2.5, yy(50, K8), 0])
        nm = name("one species", XS, GOLD)
        self.add(bl, st, nm)
        self.play(FadeIn(mean_line), FadeIn(band), run_time=0.8)
        self.at("pass")
        self.add(trg, year_counter(R))
        R.speed = 9 / 7.2
        self.at("bounces up and down")
        self.at("For its size")
        lab = T("mean 50, typical swing 25", 32, TEXT).move_to([3.0, 3.3, 0])
        self.at("swings a lot")
        self.play(FadeIn(lab), Indicate(band, color=GOLD), run_time=1.2)
        self.add(tag("computed from independent draws", x=2.5))
        self.finish()


class S09Four(SpokenScene):
    def construct(self):
        R = Run(kk=K8, nsp=1)
        self.add(R.yr, R.kk, R.nsp)
        bl = baseline()
        st = stack(R)
        tr = [trace(R, i, SP[i]) for i in range(4)]
        self.add(bl, st, tr[0], year_counter(R), name("species", XS, TEXT))
        R.speed = 9 / 8.2
        self.play(R.nsp.animate.set_value(4), R.kk.animate.set_value(K9), run_time=1.6)
        for t in tr[1:]:
            self.add(t)
        self.at("each swinging")
        lab = T("each: mean 50, swing 25", 30, TEXT).move_to([3.3, 3.3, 0])
        self.play(FadeIn(lab), run_time=0.8)
        self.at("independently")
        ind = T("out of step", 30, YELLOW).move_to([3.3, 2.6, 0])
        self.play(FadeIn(ind), run_time=0.8)
        self.at("The dark outline")
        R.ol.set_value(1)
        tot = trace(R, "tot", OUT)
        mean_t = DashedLine([-1.5, yy(200, K9), 0], [6.5, yy(200, K9), 0], color=GREY, stroke_width=3)
        self.add(tot, mean_t)
        R.yr.set_value(0)
        R.speed = 9 / 2.4
        self.play(FadeIn(mean_t), FadeOut(ind), run_time=0.8)
        self.add(tag("computed from independent draws", x=2.5))
        self.finish()


def lead_stack():
    R = Run(kk=K9)
    R.cyc = True
    R.ol.set_value(1)
    R.speed = 0.9
    return R


class S10Predict(SpokenScene):
    def construct(self):
        R = lead_stack()
        R.yr.set_value(2.0)
        st = stack(R)
        self.add(R.yr, R.kk, bl := baseline(), st, name("4 species", XS, TEXT))
        self.at("Each species swings")
        each = T("each species: swing 25", 32, TEXT).move_to([2.4, 2.8, 0])
        self.play(FadeIn(each), run_time=0.8)
        self.at("Will the total")
        q = T("Will the total swing 4× as much?", 34, YELLOW).move_to([2.4, 1.6, 0])
        self.play(Write(q), run_time=0.9)
        self.at("four times")
        o1 = chip("swing ×4", GOLD, 38).move_to([1.4, 0.2, 0])
        self.play(FadeIn(o1, shift=UP * 0.2), run_time=0.7)
        o2 = chip("less than ×4", TEAL, 38).move_to([3.6, -1.2, 0])
        self.at("single species")
        self.play(FadeIn(o2, shift=UP * 0.2), run_time=0.7)
        bob = ValueTracker(0)
        bob.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(bob)
        o1.add_updater(lambda m: m.shift(UP * 0.004 * np.cos(2 * bob.get_value())))
        o2.add_updater(lambda m: m.shift(UP * 0.004 * np.sin(2 * bob.get_value())))
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        R = Run(kk=K9)
        R.yr.set_value(2.0)
        R.ol.set_value(1)
        st = stack(R)
        self.add(R.yr, baseline(), st, name("4 species", XS, TEXT))
        cap = T("Predict: how much does the total swing?", 34, YELLOW).move_to([2.4, 1.8, 0])
        o1 = chip("swing ×4", GOLD, 38).move_to([1.4, 0.4, 0])
        o2 = chip("less than ×4", TEAL, 38).move_to([3.6, -0.9, 0])
        self.add(cap, o1, o2)
        bar = Rectangle(width=5.0, height=0.18, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([2.4, -2.2, 0])
        self.add(bar)
        self.play(bar.animate.stretch_to_fit_width(0.01).align_to([-0.1, 0, 0], LEFT), run_time=5.0, rate_func=linear)
        self.finish()


def best_pairs():
    sc = []
    for j in range(9):
        d = [year_val(j + 1, i, 0) - year_val(j, i, 0) for i in range(4)]
        if d[1] > 0 and d[2] < 0:
            sc.append((min(d[1], -d[2]) - abs(sum(d)), j))
    sc.sort(reverse=True)
    out = [j for _, j in sc]
    return out


class S12Reveal(SpokenScene):
    def construct(self):
        R = lead_stack()
        R.yr.set_value(0.0)
        st = stack(R)
        self.add(R.yr, baseline(), st, name("4 species", XS, TEXT))
        L = -1.6
        l1 = T("swing: 25 to 50 (×2)", 34).move_to([0, 2.9, 0])
        l2 = T("mean: 50 to 200 (×4)", 34).move_to([0, 2.0, 0])
        l3 = T("mean / swing: 2 to 4", 34, YELLOW).move_to([0, 1.1, 0])
        for l in (l1, l2, l3):
            l.align_to([L, 0, 0], LEFT)
        self.at("twice as much")
        self.play(FadeIn(l1, shift=LEFT * 0.2), run_time=0.8)
        self.at("four times larger")
        self.play(FadeIn(l2, shift=LEFT * 0.2), run_time=0.8)
        self.play(FadeIn(l3, shift=LEFT * 0.2), run_time=0.8)
        self.at("Good and bad years")
        pairs = best_pairs()
        j = pairs[0] if pairs else 2
        R.speed = 0
        R.cyc = False
        self.play(R.yr.animate.set_value(float(j)), run_time=0.8)
        lab = T("swings partly cancel", 34, TEAL).move_to([0, -0.3, 0]).align_to([L, 0, 0], LEFT)
        k = R.kk.get_value()
        c_y = BASE + sum(year_val(j, i, 0) for i in range(2)) * k + year_val(j, 2, 0) * k / 2
        t_y = BASE + year_val(j, 0, 0) * k + year_val(j, 1, 0) * k / 2
        ac = Arrow([-3.3, c_y + 0.4, 0], [-3.3, c_y - 0.4, 0], color=CORAL, buff=0, stroke_width=8)
        at_ = Arrow([-3.3, t_y - 0.4, 0], [-3.3, t_y + 0.4, 0], color=TEAL, buff=0, stroke_width=8)
        top = BASE + sum(year_val(j, i, 0) for i in range(4)) * k
        lvl = DashedLine([-6.4, top, 0], [-3.4, top, 0], color=OUT, stroke_width=3)
        self.play(FadeIn(lab), FadeIn(ac), FadeIn(at_), Create(lvl), run_time=0.6)
        self.play(R.yr.animate.set_value(float(j + 1)), run_time=1.8)
        self.play(Indicate(lab, color=TEAL), run_time=0.6)
        self.at("statistical averaging")
        sa = T("statistical averaging", 34, GREEN).move_to([0, -1.4, 0]).align_to([L, 0, 0], LEFT)
        self.play(Write(sa), run_time=1.2)
        R.cyc = True
        R.speed = 0.6
        self.add(tag("computed from independent draws", x=2.5))
        self.finish()


class S13Sync(SpokenScene):
    def construct(self):
        R = lead_stack()
        R.yr.set_value(0.0)
        st = stack(R)
        self.add(R.yr, R.sync, baseline(), st, name("4 species", XS, TEXT))
        L = -1.6
        self.at("out of step")
        oo = T("out of step: swings cancel", 34, TEAL).move_to([0, 2.9, 0]).align_to([L, 0, 0], LEFT)
        self.play(FadeIn(oo), run_time=0.7)
        self.at("If all four")
        h = T("all in step", 38, CORAL).move_to([0, 2.0, 0]).align_to([L, 0, 0], LEFT)
        self.play(FadeOut(oo), FadeIn(h), R.sync.animate.set_value(1.0), run_time=2.4)
        self.at("nothing would cancel")
        nc = T("no cancelling", 34, YELLOW).move_to([0, 1.1, 0]).align_to([L, 0, 0], LEFT)
        l1 = T("mean ×4, swing ×4", 34).move_to([0, 0.2, 0]).align_to([L, 0, 0], LEFT)
        self.play(FadeIn(nc), run_time=0.7)
        self.play(FadeIn(l1), run_time=0.8)
        self.at("no steadier")
        l3 = T("mean / swing stays 2", 34, YELLOW).move_to([0, -0.8, 0]).align_to([L, 0, 0], LEFT)
        self.play(FadeIn(l3, shift=LEFT * 0.2), run_time=0.8)
        self.add(tag("computed from independent draws", x=2.5))
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        PB = -0.9
        big = mix_group(-2.3, 0.0125)
        txt = T("a field is a sum", 44, TITLE_FONT if False else TEXT, font=TITLE_FONT).move_to([2.6, 0.5, 0])
        self.play(GrowFromEdge(big, DOWN), run_time=1.2)
        self.play(FadeIn(txt), run_time=0.8)
        self.at("Its extra")
        k2 = 0.0095
        tgt = mix_group(-3.6, k2, base=PB, w=1.5)
        dsh = dashed_bar(-5.5, 250, k2, base=PB, w=1.5)
        self.play(FadeOut(txt), Transform(big, tgt), FadeIn(dsh), run_time=1.5)
        q1 = T("?", 56, GREEN).move_to([-5.9, 2.2, 0])
        q2 = T("?", 56, VIOLET).move_to([-5.2, 2.2, 0])
        c1 = T("judged against\nexpected", 30, line_spacing=0.8).move_to([-4.5, -2.1, 0])
        self.at("monocultures predict")
        self.play(FadeIn(q1, scale=1.5), FadeIn(q2, scale=1.5), FadeIn(c1), run_time=1.0)
        self.at("When species swing")
        R2 = Run(kk=0.0105)
        R2.cyc = True
        R2.speed = 0.9
        R2.ol.set_value(1)
        R2.yr.set_value(1.0)
        s2 = stack(R2, x=0.4, w=1.8, base=PB)
        c2 = T("swings partly\ncancel", 30, TEAL, line_spacing=0.8).move_to([0.4, -2.1, 0])
        self.add(R2.yr)
        self.play(FadeIn(s2), FadeIn(c2), run_time=1.0)
        self.at("that can steady")
        R3 = Run(kk=0.0105)
        R3.cyc = True
        R3.speed = 0.9
        R3.ol.set_value(1)
        R3.sync.set_value(1.0)
        R3.yr.set_value(1.0)
        s3 = stack(R3, x=4.7, w=1.8, base=PB)
        c3 = T("not in\nlockstep", 30, CORAL, line_spacing=0.8).move_to([4.7, -2.1, 0])
        self.add(R3.yr)
        self.play(FadeIn(s3), FadeIn(c3), run_time=1.0)
        cross = VGroup(Line([3.8, 2.6, 0], [5.6, -0.8, 0]), Line([3.8, -0.8, 0], [5.6, 2.6, 0])).set_stroke(RED, 7)
        self.play(Create(cross), run_time=0.8)
        self.finish()


class S15End(EndCard):
    LINE = "A field is a sum, judged against expected; out-of-step swings partly cancel."
