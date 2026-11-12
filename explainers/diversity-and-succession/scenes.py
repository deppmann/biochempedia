"""How Many Species Is It Worth? (Diversity, Disturbance and Succession), levelled-up film.

COLOUR MAP: species 1 TEAL, 2 GOLD, 3 VIOLET, 4 CORAL (dots, bars); effective number = NAVY columns;
order dial = semicircle q = 0, 1, 2; storm = grey cloud. Every number on screen is computed (Hill numbers)
or labelled schematic. One world: plot A left, plot B right, same places in every scene.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

VIOLET = "#A78BFA"
CORAL = "#FF7F6B"
NAVY = "#5B7CFA"
SP = [TEAL, GOLD, VIOLET, CORAL]
SPSW = [VIOLET, CORAL, TEAL, GOLD]
CA = [25, 25, 25, 25]
CB = [40, 40, 10, 10]
KEEP = [4, 4, 1, 1]
LX, RX = -3.4, 3.4
GY, DD = -0.05, 0.27
ROWY, COLH, COLW, COLS = 1.6, 1.2, 0.5, 0.6
BASEY, UNIT, BARW, BARSP = -3.45, 3.2, 0.55, 0.82
DC, DR = np.array([0.0, 1.65, 0.0]), 1.2


def hill(counts, q):
    p = np.array(counts, float)
    p = p / p.sum()
    if abs(q - 1) < 1e-3:
        return float(np.exp(-(p * np.log(p)).sum()))
    return float((p ** q).sum() ** (1.0 / (1 - q)))


def shares(c):
    return [x / sum(c) for x in c]


def build_grid(cx, counts, seed, cols):
    sp = [k for k, c in enumerate(counts) for _ in range(c)]
    random.Random(seed).shuffle(sp)
    dots = VGroup()
    seen = [0] * 4
    for i, k in enumerate(sp):
        r_, c_ = divmod(i, 10)
        d = Dot(radius=0.085, color=cols[k]).move_to([cx + (c_ - 4.5) * DD, GY + (4.5 - r_) * DD, 0])
        d.sp = k
        seen[k] += 1
        d.bx, d.by = d.get_x(), d.get_y()
        d.ph = random.Random(i + seed).uniform(0, 6.28)
        dots.add(d)
    for k in range(4):
        mem = [d for d in dots if d.sp == k]
        n = len(mem)
        for d in mem:
            d.keep = False
        for i in range(KEEP[k]):
            mem[int((i + 0.5) * n / KEEP[k])].keep = True
    dots.t = 0.0

    def shimmer(g, dt):
        g.t += dt
        for d in g.submobjects:
            d.move_to([d.bx + 0.025 * np.sin(1.7 * g.t + d.ph), d.by + 0.025 * np.cos(1.3 * g.t + d.ph), 0])
    dots.add_updater(shimmer)
    frame = RoundedRectangle(corner_radius=0.12, width=10 * DD + 0.25, height=10 * DD + 0.25,
                             stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, GY, 0])
    return frame, dots


def bar_rects(cx, sh, cols):
    bars, labs = VGroup(), VGroup()
    for k, s in enumerate(sh):
        x = cx + (k - 1.5) * BARSP
        h = UNIT * s
        r = Rectangle(width=BARW, height=h, stroke_width=0, fill_color=cols[k], fill_opacity=0.9).move_to([x, BASEY + h / 2, 0])
        bars.add(r)
        labs.add(M(f"{s:.2f}".rstrip("0").rstrip(".") if s not in (0.25,) else "0.25", 22).move_to([x, BASEY + h + 0.28, 0]))
    base = Line([cx - 1.6, BASEY, 0], [cx + 1.6, BASEY, 0], color=GREY, stroke_width=3)
    return bars, labs, base


def row_mob(cx, val):
    g = VGroup()
    for i in range(4):
        f = min(max(val - i, 0), 1)
        if f <= 0.001:
            continue
        x = cx + (i - 1.5) * COLS
        g.add(Rectangle(width=COLW, height=COLH, stroke_color=NAVY, stroke_width=2.5, fill_opacity=0).move_to([x, ROWY + COLH / 2, 0]))
        g.add(Rectangle(width=COLW, height=COLH * f, stroke_width=0, fill_color=NAVY, fill_opacity=0.9).move_to([x, ROWY + COLH * f / 2, 0]))
    return g


class W:
    """The world, rebuilt identically in every scene."""

    def __init__(self, swapped=False):
        self.cb = SPSW if swapped else SP
        self.fa, self.da = build_grid(LX, CA, 3, SP)
        self.fb, self.db = build_grid(RX, CB, 7, self.cb)
        self.labA = T("plot A", 30).move_to([LX, 3.4, 0])
        self.labB = T("plot B", 30).move_to([RX, 3.4, 0])
        self.q = ValueTracker(0)
        self.nA = ValueTracker(4)
        self.nB = ValueTracker(hill(CB, 1))
        self.rowA = always_redraw(lambda: row_mob(LX, self.nA.get_value()))
        self.rowB = always_redraw(lambda: row_mob(RX, self.nB.get_value()))
        self.mode = "static"   # "static" tag 'order 1 computed', "q" tag from tracker
        self.readA = always_redraw(lambda: self._read(self.nA.get_value(), -5.45))
        self.readB = always_redraw(lambda: self._read(self.nB.get_value(), 5.45))
        self.barsA = bar_rects(LX, shares(CA), SP)
        self.barsB = bar_rects(RX, shares(CB), self.cb)
        self.needle = always_redraw(self._needle)
        arc = Arc(radius=DR, start_angle=0, angle=PI, arc_center=DC, color=GREY, stroke_width=4)
        base = Line(DC + LEFT * DR, DC + RIGHT * DR, color=GREY, stroke_width=3)
        l0 = T("q = 0", 26).move_to(DC + [-1.35, -0.38, 0])
        l1 = T("q = 1", 26).move_to(DC + [0, DR + 0.38, 0])
        l2 = T("q = 2", 26).move_to(DC + [1.35, -0.38, 0])
        self.dial_static = VGroup(arc, base, l0, l1, l2)
        self.dial_static.set_z_index(0)

    def _read(self, val, x):
        lines = [M(f"{val:.2f}", 32)]
        if self.mode == "static":
            lines += [T("order 1", 22), T("computed", 22)]
        else:
            lines += [T(f"order {self.q.get_value():.1f}", 22)]
        return VGroup(*lines).arrange(DOWN, buff=0.08).move_to([x, 2.2, 0])

    def _needle(self):
        th = PI * (1 - self.q.get_value() / 2)
        return Line(DC, DC + 0.95 * np.array([np.cos(th), np.sin(th), 0]), color=GOLD, stroke_width=6)

    def link_q(self, scene, q0):
        self.q.set_value(q0)
        self.mode = "q"
        self.nA.set_value(4)
        self.nB.set_value(hill(CB, q0))
        self.nB.add_updater(lambda m: m.set_value(hill(CB, self.q.get_value())))
        bars = self.barsB[0]
        labs = self.barsB[1]

        def fade(_):
            o = 1 - 0.6 * min(1, self.q.get_value() / 2)
            for k in (2, 3):
                bars[k].set_fill(opacity=0.9 * o)
                labs[k].set_opacity(o)
        bars.add_updater(fade)
        scene.add(self.q, self.nB)
        fade(None)

    def grids(self):
        return [self.fa, self.da, self.fb, self.db, self.labA, self.labB]

    def bars(self, which="AB"):
        out = []
        for w, b in (("A", self.barsA), ("B", self.barsB)):
            if w in which:
                out += list(b)
        return out

    def rows(self):
        return [self.rowA, self.rowB, self.readA, self.readB]

    def dial(self):
        return [self.dial_static, self.needle]


def txt(lines, size=28, color=TEXT, y=0.0, x=0.0):
    return VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, buff=0.12).move_to([x, y, 0])


def ring(sc, *mobs, rt=1.4, color=WHITE):
    rs = [SurroundingRectangle(m, color=color, buff=0.12, stroke_width=5) for m in mobs]
    sc.play(*[Create(r) for r in rs], run_time=rt * 0.45)
    sc.play(*[FadeOut(r) for r in rs], run_time=rt * 0.55)


def sweep(sc, w, q1, rt):
    sc.play(w.q.animate.set_value(q1), run_time=rt, rate_func=smooth)


def lift_marks(w, cx):
    """One dot of each species out of the grid into a row of four (richness)."""
    g = VGroup(*[Dot(radius=0.17, color=SP[k]) for k in range(4)]).arrange(RIGHT, buff=0.45).move_to([cx, 2.25, 0])
    return g


class S00Title(TitleCard):
    LESSON = "Diversity, Disturbance and Succession"
    TITLE = "How Many Species Is It Worth?"


class S01Question(SpokenScene):
    def construct(self):
        w = W()
        self.play(FadeIn(w.fa), FadeIn(w.fb), LaggedStart(*[FadeIn(d, scale=0.5) for d in list(w.da) + list(w.db)], lag_ratio=0.006), FadeIn(w.labA), FadeIn(w.labB), run_time=1.6)
        self.add(w.da, w.db)
        self.at("hundred")
        t1, t2 = T("100 individuals", 28).move_to([LX, -2.4, 0]), T("100 individuals", 28).move_to([RX, -2.4, 0])
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.8)
        self.at("Can")
        q = T("?", 80, GOLD).move_to([0, GY, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.7)
        self.at("Count")
        s1, s2 = T("species: 4", 30).move_to([LX, -2.4, 0]), T("species: 4", 30).move_to([RX, -2.4, 0])
        eq = T("=", 80, GOLD).move_to([0, GY, 0])
        self.play(ReplacementTransform(t1, s1), ReplacementTransform(t2, s2), ReplacementTransform(q, eq), run_time=1.0)
        self.at("tie")
        self.play(Indicate(s1, scale_factor=1.15), Indicate(s2, scale_factor=1.15), run_time=1.0)
        self.at("Look")
        q2 = T("?", 80, GOLD).move_to([0, GY, 0])
        self.play(ReplacementTransform(eq, q2), Indicate(w.db, color=VIOLET, scale_factor=1.04), run_time=1.2)
        self.at("alike")
        self.play(Indicate(w.da, scale_factor=1.04), Indicate(w.db, scale_factor=1.04), run_time=1.5)
        self.finish()


class S02Richness(SpokenScene):
    def construct(self):
        w = W()
        s1, s2 = T("species: 4", 30).move_to([LX, -2.4, 0]), T("species: 4", 30).move_to([RX, -2.4, 0])
        q = T("?", 80, GOLD).move_to([0, GY, 0])
        self.add(w.fa, w.fb, w.da, w.db, w.labA, w.labB, s1, s2, q)
        rA, rB = lift_marks(w, LX), lift_marks(w, RX)
        srcA = [next(d for d in w.da if d.sp == k) for k in range(4)]
        srcB = [next(d for d in w.db if d.sp == k) for k in range(4)]
        self.at("Richness", lead=0.0)
        self.play(*[ReplacementTransform(srcA[k].copy().clear_updaters(), rA[k]) for k in range(4)],
                  *[ReplacementTransform(srcB[k].copy().clear_updaters(), rB[k]) for k in range(4)], run_time=2.0)
        self.at("Both")
        head = T("richness S = 4", 30, TEXT).move_to([0, 3.4, 0])
        self.play(FadeIn(head), FadeOut(s1), FadeOut(s2), run_time=1.0)
        self.at("tie")
        eq = T("=", 80, GOLD).move_to([0, GY, 0])
        self.play(ReplacementTransform(q, eq), run_time=0.8)
        self.at("But")
        vio = [d for d in w.db if d.sp in (2, 3)]
        self.play(*[Indicate(d, scale_factor=2.0, color=WHITE) for d in vio], Indicate(rB[2], scale_factor=1.8), Indicate(rB[3], scale_factor=1.8), run_time=1.8)
        self.at("once")
        self.play(*[Indicate(m, scale_factor=1.4) for m in list(rA) + list(rB)], run_time=1.5)
        self.at("ignores")
        ig = txt(["ignores", "abundance"], 30, GOLD, y=-2.5)
        self.play(FadeIn(ig), run_time=0.8)
        self.play(*[Indicate(d, scale_factor=1.6, color=TEAL) for d in w.db if d.sp == 0][:20], run_time=1.5)
        self.finish()


class S03Shares(SpokenScene):
    def construct(self):
        w = W()
        rA, rB = lift_marks(w, LX), lift_marks(w, RX)
        head = T("richness S = 4", 30).move_to([0, 3.4, 0])
        eq = T("=", 80, GOLD).move_to([0, GY, 0])
        ig = txt(["ignores", "abundance"], 30, GOLD, y=-2.5)
        self.add(w.fa, w.fb, w.da, w.db, w.labA, w.labB, rA, rB, head, eq, ig)
        self.play(FadeOut(rA), FadeOut(rB), FadeOut(head), FadeOut(eq), FadeOut(ig), run_time=1.0)
        bA, lA, baseA = w.barsA
        bB, lB, baseB = w.barsB
        ax = txt(["share of", "individuals"], 26, TEXT, y=-2.4)
        self.at("evenly")
        self.play(Create(baseA), Create(baseB), FadeIn(ax), run_time=1.2)
        self.at("In", lead=0.0) if False else None
        self.at("plot A")
        grpA = [VGroup(*[d.copy().clear_updaters() for d in w.da if d.sp == k]) for k in range(4)]
        self.play(*[ReplacementTransform(grpA[k], bA[k]) for k in range(4)], run_time=1.3)
        self.play(FadeIn(lA), run_time=0.4)
        self.at("same share")
        self.play(*[Indicate(b, scale_factor=1.1) for b in bA], run_time=1.0)
        self.at("plot B", nth=1) if False else None
        self.at("B,")
        grpB = [VGroup(*[d.copy().clear_updaters() for d in w.db if d.sp == k]) for k in range(4)]
        self.play(*[ReplacementTransform(grpB[k], bB[k]) for k in range(4)], run_time=1.3)
        self.play(FadeIn(lB), run_time=0.4)
        self.at("two species hold")
        self.play(Indicate(bB[0], scale_factor=1.1), Indicate(bB[1], scale_factor=1.1), run_time=1.2)
        self.at("rare")
        self.play(Indicate(bB[2], scale_factor=1.3, color=WHITE), Indicate(bB[3], scale_factor=1.3, color=WHITE), run_time=1.5)
        self.finish()


def base_bars(sc, w, ax=True):
    sc.add(*w.bars("AB"), w.barsA[2], w.barsB[2])
    if ax:
        sc.add(txt(["share of", "individuals"], 26, TEXT, y=-2.4))


def scale_mob(n):
    ang = -0.28 * (1 - min(n, 3.3) / 3.3)
    piv = np.array([0, 2.2, 0.0])
    R = lambda v: np.array([v[0] * np.cos(ang) - v[1] * np.sin(ang), v[0] * np.sin(ang) + v[1] * np.cos(ang), 0])
    eL, eR = piv + R([-1.4, 0]), piv + R([1.4, 0])
    g = VGroup(Polygon(piv, piv + [-0.3, -0.5, 0], piv + [0.3, -0.5, 0], color=GREY, stroke_width=3),
               Line(eL, eR, color=TEXT, stroke_width=5))
    for e, kind in ((eL, "n"), (eR, "b")):
        ty = e[1] - 0.55
        tl, tr = np.array([e[0] - 0.4, ty, 0]), np.array([e[0] + 0.4, ty, 0])
        g.add(Line(e, tl, color=GREY, stroke_width=2), Line(e, tr, color=GREY, stroke_width=2), Line(tl, tr, color=TEXT, stroke_width=4))
        if kind == "n":
            h = max(0.02, 0.5 * min(n, 3.3) / 3.3)
            g.add(Rectangle(width=0.5, height=h, stroke_width=0, fill_color=NAVY, fill_opacity=0.9).move_to([e[0], ty + h / 2, 0]))
        else:
            for k, s in enumerate([0.4, 0.4, 0.1, 0.1]):
                hh = 0.5 * s / 0.4
                g.add(Rectangle(width=0.14, height=hh, stroke_width=0, fill_color=SP[k], fill_opacity=0.9).move_to([e[0] + (k - 1.5) * 0.17, ty + hh / 2, 0]))
    return g


class S04Effective(SpokenScene):
    def construct(self):
        w = W()
        w.nB.set_value(0)
        self.add(w.fa, w.fb, w.da, w.db, w.labA, w.labB, *w.bars("AB"), w.barsA[2], w.barsB[2])
        self.add(txt(["share of", "individuals"], 26, TEXT, y=-2.4))
        sc = always_redraw(lambda: scale_mob(w.nB.get_value()))
        self.add(w.rowB, w.nB)
        self.add(sc)
        self.play(FadeIn(sc), run_time=1.0)
        self.wait(1.2)
        self.at("Imagine")
        self.play(w.nB.animate.set_value(1), run_time=1.6, rate_func=smooth)
        self.at("every")
        self.play(w.nB.animate.set_value(2), run_time=1.4, rate_func=smooth)
        self.at("equally")
        self.play(w.nB.animate.set_value(3), run_time=1.4, rate_func=smooth)
        self.at("How many")
        self.play(w.nB.animate.set_value(hill(CB, 1)), run_time=2.4, rate_func=smooth)
        self.at("That count")
        cap = txt(["effective number", "of species"], 30, TEXT, y=0.4)
        self.play(FadeIn(cap), run_time=1.0)
        ring(self, w.rowB, rt=1.5)
        self.finish()


class S05Equal(SpokenScene):
    def construct(self):
        w = W()
        w.nA.set_value(0)
        self.add(w.fa, w.fb, w.da, w.db, w.labA, w.labB, *w.bars("AB"), w.barsA[2], w.barsB[2])
        self.add(txt(["share of", "individuals"], 26, TEXT, y=-2.4))
        cap = txt(["effective number", "of species"], 30, TEXT, y=0.4)
        self.add(w.rowB, w.nB, w.nA, w.rowA, cap)
        sc = scale_mob(hill(CB, 1))
        self.add(sc)
        self.play(FadeOut(sc), FadeOut(cap), run_time=0.8)
        self.play(w.nA.animate.set_value(4), run_time=1.6)
        self.add(w.readA)
        self.at("same as")
        ring(self, w.rowA, rt=1.5)
        self.at("For plot B", nth=0) if False else None
        self.at("fewer")
        self.add(w.readB)
        self.wait(0.8)
        self.at("because")
        self.play(Indicate(w.barsB[0][0], scale_factor=1.1), Indicate(w.barsB[0][1], scale_factor=1.1), run_time=1.4)
        self.at("individuals")
        ring(self, w.rowB, rt=1.5)
        self.finish()


def full_static(sc, w, bars_b=True):
    sc.add(w.fa, w.fb, w.da, w.db, w.labA, w.labB, *w.bars("AB" if bars_b else "A"), w.barsA[2], w.rowA, w.rowB, w.readA, w.readB)
    if bars_b:
        sc.add(w.barsB[2])


class S06Order(SpokenScene):
    def construct(self):
        w = W()
        full_static(self, w)
        self.add(w.nA, w.nB)
        self.wait(0.3)
        self.play(FadeIn(w.dial_static), FadeIn(w.needle), run_time=1.2)
        self.play(w.nB.animate.set_value(4), run_time=1.0)
        w.link_q(self, 0)
        self.at("order zero")
        cap = txt(["order 0 =", "richness S"], 30, GOLD, y=0.2)
        self.play(FadeIn(cap), run_time=0.9)
        self.at("every species")
        ring(self, w.rowB, rt=1.0)
        self.at("rises")
        self.play(FadeOut(cap), w.q.animate.set_value(0.8), run_time=1.6, rate_func=smooth)
        self.at("common species")
        self.play(Indicate(w.barsB[0][0], scale_factor=1.1), Indicate(w.barsB[0][1], scale_factor=1.1), run_time=1.4)
        self.at("rare ones")
        self.wait(0.4)
        self.play(w.q.animate.set_value(0), run_time=1.6, rate_func=smooth)
        self.finish()


class S07Dial(SpokenScene):
    def construct(self):
        w = W()
        full_static(self, w)
        self.add(w.nA, w.nB, *w.dial())
        w.link_q(self, 0)
        w.nB.set_value(4)
        self.add(w.readA, w.readB)
        self.wait(0.3)
        self.play(w.q.animate.set_value(0.3), run_time=1.8, rate_func=smooth)
        self.at("shrinks")
        self.play(w.q.animate.set_value(1), run_time=1.8, rate_func=smooth)
        self.at("step by step")
        self.wait(0.3)
        self.at("rare species")
        self.play(w.q.animate.set_value(2), run_time=2.4, rate_func=smooth)
        self.at("Plot A")
        ring(self, w.rowA, w.readA, rt=1.6)
        self.at("nothing")
        self.play(Indicate(w.fa, color=TEAL, scale_factor=1.03), run_time=1.5)
        self.finish()


def world_q(sc, q, swapped=False, bars_b=True):
    w = W(swapped)
    full_static(sc, w, bars_b)
    sc.add(w.nA, w.nB, *w.dial())
    w.link_q(sc, q)
    sc.add(w.readA, w.readB)
    return w


def stamp(w):
    return always_redraw(lambda: chip("", NAVY)) if False else None


class S08Name(SpokenScene):
    def construct(self):
        w = world_q(self, 2)
        st = VGroup(T("effective number", 24, NAVY), T("order 2", 24, NAVY)).arrange(DOWN, buff=0.1)
        box = SurroundingRectangle(st, color=NAVY, buff=0.12, corner_radius=0.12)
        stamp_g = VGroup(box, st).move_to([0, -2.5, 0])
        self.at("order you", lead=0.0) if False else None
        self.play(FadeIn(stamp_g, scale=1.5), run_time=0.8)
        self.at("changes")
        ring(self, w.readB, rt=1.2)
        self.at("order zero")
        self.play(FadeOut(stamp_g), w.q.animate.set_value(0), run_time=2.0, rate_func=smooth)
        b1 = txt(["order 0 =", "richness S"], 30, GOLD, y=-0.3)
        self.at("just the richness")
        self.play(FadeIn(b1), run_time=0.8)
        self.at("ties")
        ring(self, w.rowA, w.rowB, rt=1.6)
        self.at("Above")
        b2 = txt(["above order 0:", "= S only if all", "equally common"], 28, GOLD, y=-0.5)
        self.play(FadeOut(b1), w.q.animate.set_value(2), run_time=2.4, rate_func=smooth)
        self.play(FadeIn(b2), run_time=0.8)
        self.at("equally")
        ring(self, w.rowB, rt=1.5)
        self.at("Always")
        self.play(FadeOut(b2), FadeIn(stamp_g, scale=1.4), run_time=0.9)
        self.play(Indicate(stamp_g, scale_factor=1.12), run_time=1.2)
        self.finish()


def swap_anim(w):
    anims = []
    for d in w.db:
        anims.append(d.animate.set_fill(SPSW[d.sp]).set_stroke(SPSW[d.sp]))
    bars = w.barsB[0]
    for k in range(4):
        anims.append(bars[k].animate.set_fill(SPSW[k]))
    return anims


class S09Identity(SpokenScene):
    def construct(self):
        w = world_q(self, 2)
        stamp_g = VGroup(SurroundingRectangle(VGroup(T("effective number", 24), T("order 2", 24)).arrange(DOWN, buff=0.1), color=NAVY, buff=0.12, corner_radius=0.12),
                         VGroup(T("effective number", 24, NAVY), T("order 2", 24, NAVY)).arrange(DOWN, buff=0.1)).move_to([0, -2.5, 0])
        stamp_g[1].move_to(stamp_g[0])
        self.add(stamp_g)
        self.wait(0.3)
        self.play(*swap_anim(w), run_time=2.8)
        self.at("Nothing")
        ck = T("same", 30, GOLD).move_to([0, 0.4, 0])
        self.play(FadeIn(ck), run_time=0.6)
        ring(self, w.rowB, w.readB, rt=1.2)
        self.at("These")
        lab = txt(["count-based", "indices: blind", "to identity"], 28, GOLD, y=-0.8)
        self.play(FadeOut(ck), FadeIn(lab), run_time=0.9)
        self.at("never")
        self.play(Indicate(w.db, color=WHITE, scale_factor=1.04), run_time=1.6)
        self.at("none")
        self.play(Indicate(w.da, color=WHITE, scale_factor=1.04), Indicate(w.db, color=WHITE, scale_factor=1.04), run_time=1.6)
        self.finish()


def cloud():
    g = VGroup(*[Circle(radius=r, stroke_width=0, fill_color="#6B7385", fill_opacity=0.95).move_to([x, y, 0])
                 for x, y, r in [(-0.7, 0, 0.55), (0, 0.25, 0.7), (0.75, 0, 0.55), (0.1, -0.1, 0.6)]])
    bolt = Polygon([0.1, -0.5, 0], [-0.25, -1.1, 0], [0.0, -1.1, 0], [-0.2, -1.8, 0], [0.4, -0.95, 0], [0.12, -0.95, 0], [0.3, -0.5, 0],
                   stroke_width=0, fill_color=YELLOW, fill_opacity=1)
    return VGroup(g, bolt)


def sub_world(sc, q=2, bars_b=True):
    return world_q(sc, q, swapped=True, bars_b=bars_b)


class S10Predict(SpokenScene):
    def construct(self):
        w = sub_world(self)
        self.wait(0.5)
        self.at("storm")
        cl = cloud().move_to([RX - 4.2, GY + 2.2, 0])
        self.add(cl)
        self.play(cl.animate.move_to([RX, GY + 0.4, 0]), run_time=2.4, rate_func=linear)
        self.at("kills")
        dying = [d for d in w.db if not d.keep]
        tx = txt(["same share killed", "in every species"], 28, GOLD, y=0.0)
        self.play(*[d.animate.set_fill(GREY).set_stroke(GREY) for d in dying], FadeOut(VGroup(*w.barsB)), FadeIn(tx), run_time=1.0)
        self.play(cl.animate.move_to([RX + 4.2, GY + 2.2, 0]).set_opacity(0), *[FadeOut(d) for d in dying], run_time=1.6)
        w.db.remove(*dying)
        self.remove(cl)
        self.at("Most")
        self.play(Indicate(w.fb, color=WHITE, scale_factor=1.03), run_time=1.5)
        self.at("What happens")
        ring(self, w.rowB, rt=1.2)
        q = T("?", 64, GOLD).move_to([5.45, 2.2, 0])
        self.play(FadeOut(w.readB), FadeIn(q), run_time=0.8)
        self.play(Indicate(q, scale_factor=1.4), run_time=0.8)
        ring(self, w.rowB, rt=1.0)
        self.finish()


def after_storm(sc, bars_b=False):
    w = sub_world(sc, bars_b=bars_b)
    dying = [d for d in w.db if not d.keep]
    w.db.remove(*dying)
    return w


class S11Pause(NarratedScene):
    def construct(self):
        w = after_storm(self)
        self.remove(w.readB)
        q = T("?", 64, GOLD).move_to([5.45, 2.2, 0])
        tx = txt(["same share killed", "in every species"], 28, GOLD, y=0.35)
        pr = txt(["Predict:", "up, down or", "unchanged?"], 30, TEXT, y=-1.4)
        self.add(q, tx, pr)
        ring_t = ValueTracker(1)
        ring = always_redraw(lambda: VGroup(Circle(radius=0.45, color=GREY, stroke_width=4),
                                            Arc(radius=0.45, start_angle=PI / 2, angle=2 * PI * ring_t.get_value(), color=GOLD, stroke_width=7)
                                            ).move_to([0, -3.0, 0]))
        self.add(ring, ring_t)
        self.play(ring_t.animate.set_value(0.001), run_time=4.9, rate_func=linear)
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        w = after_storm(self)
        self.remove(w.readB)
        q = T("?", 64, GOLD).move_to([5.45, 2.2, 0])
        tx = txt(["same share killed", "in every species"], 28, GOLD, y=0.2)
        self.add(q, tx)
        self.wait(0.3)
        self.remove(q)
        self.add(w.readB)
        self.wait(0.4)
        ring(self, w.rowB, rt=1.0)
        self.at("counts")
        keepd = [d for d in w.db]
        bB, lB, baseB = w.barsB
        for m in list(bB) + list(lB):
            m.set_opacity(0) if False else None
        grp = [VGroup(*[d.copy().clear_updaters() for d in keepd if d.sp == k]) for k in range(4)]
        self.play(Create(baseB), *[ReplacementTransform(grp[k], bB[k]) for k in range(4)], run_time=2.4)
        for k in (2, 3):
            bB[k].set_fill(opacity=0.9 * 0.4)
        for k in (2, 3):
            lB[k].set_opacity(0.4)
        self.play(FadeIn(lB), run_time=0.6)
        self.at("share")
        t2 = txt(["counts fell;", "shares did not"], 28, GOLD, y=-0.4)
        self.play(ReplacementTransform(tx, t2), run_time=1.0)
        self.at("stays")
        self.play(w.q.animate.set_value(1), run_time=1.3, rate_func=smooth)
        ring(self, w.readB, rt=0.7)
        self.play(w.q.animate.set_value(2), run_time=1.3, rate_func=smooth)
        self.finish()


def icon_beaker():
    body = Polygon([-0.3, 0.45, 0], [-0.3, -0.35, 0], [-0.15, -0.5, 0], [0.15, -0.5, 0], [0.3, -0.35, 0], [0.3, 0.45, 0],
                   stroke_color=TEAL, stroke_width=4, fill_opacity=0)
    liq = Polygon([-0.28, 0.0, 0], [-0.28, -0.34, 0], [-0.14, -0.48, 0], [0.14, -0.48, 0], [0.28, -0.34, 0], [0.28, 0.0, 0],
                  stroke_width=0, fill_color=TEAL, fill_opacity=0.6)
    return VGroup(liq, body).scale(1.4)


def icon_boulder():
    return Polygon([-0.6, -0.4, 0], [-0.45, 0.2, 0], [0, 0.5, 0], [0.5, 0.25, 0], [0.62, -0.4, 0],
                   stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.5)


class S13Rule(SpokenScene):
    def construct(self):
        w = after_storm(self, bars_b=True)
        self.wait(0.2)
        rowB = row_mob(RX, hill(CB, 2))
        self.remove(w.rowB)
        self.add(rowB)
        gone = [w.fa, w.fb, w.da, w.db, w.labA, w.labB, w.rowA, w.readA, w.readB, w.dial_static, w.needle] + w.bars("AB") + [w.barsA[2], w.barsB[2]]
        self.play(*[FadeOut(m) for m in gone], run_time=1.2)
        self.play(rowB.animate.shift(DOWN * 1.6 + RIGHT * 0.9).scale(1.6), run_time=1.4)
        tgt = rowB.get_left() + LEFT * 0.25
        self.at("only two")
        y0 = 2.5
        def arrow_row(y, label, color):
            lab = T(label, 30, color).align_to([-6.4, 0, 0], LEFT).set_y(y)
            ar = Arrow(lab.get_right() + RIGHT * 0.2, [tgt[0], tgt[1] + (y - 0.2) * 0.15, 0], buff=0.05, color=color, stroke_width=6)
            return lab, ar
        l1, a1 = arrow_row(2.5, "who is present", TEAL)
        self.at("present")
        self.play(FadeIn(l1), GrowArrow(a1), run_time=1.2)
        l2, a2 = arrow_row(0.9, "how evenly they are shared", GOLD)
        self.at("evenly")
        self.play(FadeIn(l2), GrowArrow(a2), run_time=1.4)
        l3, a3 = arrow_row(-0.7, "killing the same share of all", GREY)
        self.at("survivors")
        self.play(FadeIn(l3), GrowArrow(a3), run_time=1.0)
        mid = a3.get_center()
        cross = VGroup(Line(mid + [-0.3, -0.3, 0], mid + [0.3, 0.3, 0], color=RED, stroke_width=8), Line(mid + [-0.3, 0.3, 0], mid + [0.3, -0.3, 0], color=RED, stroke_width=8))
        self.play(Create(cross), run_time=0.8)
        self.at("Whether")
        tag = T("raise or lower? test it", 32, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(tag), run_time=1.0)
        self.at("experiments")
        be, bo = icon_beaker().move_to([-4.9, -2.9, 0]), icon_boulder().move_to([4.9, -2.9, 0])
        self.play(FadeIn(be, scale=0.5), FadeIn(bo, scale=0.5), run_time=1.0)
        self.play(Indicate(be, color=TEAL), Indicate(bo, color=WHITE), run_time=1.4)
        self.finish()


class S14End(EndCard):
    LINE = "Diversity is how many equally common species a community is worth."
