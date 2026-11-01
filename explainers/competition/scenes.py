"""Competition: competitors coexist when each limits itself more than it limits the other.

COLOR MAP (one color per concept, whole video)
  GOLD   = Chthamalus (the upper barnacle)
  TEAL   = Balanus (the lower barnacle)
  BLUE   = species 1 in the Lotka-Volterra sketch (its N, its isocline, its conditions)
  ORANGE = species 2 in the sketch
  GREEN  = coexistence / a condition that holds
  RED    = exclusion / a condition that fails
  GREY   = rock, axes, labels, "in this sketch"
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
CT = GOLD       # Chthamalus
BA = TEAL       # Balanus


def cone(color, s=0.3, op=0.85):
    return Polygon([-s, -s * 0.55, 0], [s, -s * 0.55, 0], [s * 0.45, s * 0.7, 0], [-s * 0.45, s * 0.7, 0],
                   stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def dot(color, r=0.17):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9)


# ----------------------------------------------------------------------------------------------
# the Lotka-Volterra sketch: computed from the lesson's equation
# ----------------------------------------------------------------------------------------------
R1, R2, K1, K2 = 0.5, 0.25, 100.0, 80.0


def path(a12, a21, n1=20.0, n2=20.0, days=140, dt=0.05):
    pts = [(n1, n2)]
    for _ in range(int(days / dt)):
        d1 = R1 * n1 * (1 - (n1 + a12 * n2) / K1)
        d2 = R2 * n2 * (1 - (n2 + a21 * n1) / K2)
        n1, n2 = max(n1 + d1 * dt, 0), max(n2 + d2 * dt, 0)
        pts.append((n1, n2))
    return pts[::4]


AX_C = np.array([-2.0, 0.0, 0])


def make_axes():
    ax = Axes(x_range=[0, 200, 50], y_range=[0, 200, 50], x_length=6.8, y_length=5.3,
              axis_config={"include_numbers": False, "include_tip": False, "stroke_color": GREY, "stroke_width": 3,
                           "tick_size": 0.06}).move_to(AX_C)
    xl = T("species 1 individuals", 22, BLUE).next_to(ax, DOWN, buff=0.5)
    yl = T("species 2 individuals", 22, ORANGE).rotate(PI / 2).next_to(ax, LEFT, buff=0.65)
    tag = T("in this sketch", 22, GREY).next_to(ax, UP, buff=0.1).align_to(ax, RIGHT)
    return ax, xl, yl, tag


def iso1(ax, a12=0.5):
    return Line(ax.c2p(K1, 0), ax.c2p(0, K1 / a12), color=BLUE, stroke_width=6)


def iso2(ax, a21=0.5):
    return Line(ax.c2p(0, K2), ax.c2p(K2 / a21, 0), color=ORANGE, stroke_width=6)


def tick(ax, x, y, text, color, side):
    m = M(text, 22, color)
    if side == "below":
        return m.next_to(ax.c2p(x, 0), DOWN, buff=0.1)
    return m.next_to(ax.c2p(0, y), LEFT, buff=0.1)


def trace(ax, pts, color=GREEN):
    v = VMobject(color=color, stroke_width=5)
    v.set_points_as_corners([ax.c2p(a, b) for a, b in pts])
    return v


class S00Title(TitleCard):
    LESSON = "Competition"
    TITLE = "Competitors Coexist When Each Limits Itself More"


# ----------------------------------------------------------------------------------------------
class S01Shore(SpokenScene):
    def construct(self):
        cx = -1.4
        hi = Rectangle(width=10.2, height=2.6, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.12).move_to([cx, 1.75, 0])
        lo = Rectangle(width=10.2, height=2.6, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.28).move_to([cx, -0.85, 0])
        hi_l = T("high on the shore", 24, GREY).move_to([5.3, 1.2, 0])
        lo_l = T("just below", 24, GREY).move_to([5.3, -0.2, 0])
        self.at("rocky shore")
        self.play(FadeIn(hi), FadeIn(lo), run_time=0.6)
        # adult Chthamalus high up
        rng = np.random.RandomState(4)
        hi_pts = [[cx - 4.4 + 1.25 * i + 0.1 * rng.randn(), 1.75 + (0.55 if i % 2 else -0.55), 0] for i in range(8)]
        hiC = VGroup(*[cone(CT, 0.38).move_to(p) for p in hi_pts])
        hiC_l = T("Chthamalus", 26, CT).move_to([5.3, 1.75, 0])
        self.at("one barnacle lives high")
        self.play(FadeIn(hiC, lag_ratio=0.1), FadeIn(hi_l), FadeIn(hiC_l), run_time=0.9)
        # Balanus covering the lower band, with three marked Chthamalus among them
        marks = [[cx - 2.6, -0.85, 0], [cx + 0.5, -0.85, 0], [cx + 3.1, -0.85, 0]]
        bal = VGroup()
        for i in range(10):
            for j in range(3):
                p = np.array([cx - 4.5 + 0.95 * i + (0.47 if j == 1 else 0), -1.75 + 0.9 * j, 0])
                if min(np.linalg.norm(p - np.array(m)) for m in marks) < 0.8:
                    continue
                bal.add(cone(BA, 0.36).move_to(p))
        balL = T("Balanus", 26, BA).move_to([5.3, -1.1, 0])
        mC = VGroup(*[cone(CT, 0.38).move_to(m) for m in marks])
        self.at("Another covers the rock")
        self.play(FadeIn(bal, lag_ratio=0.03), FadeIn(lo_l), FadeIn(balL), run_time=1.1)
        self.play(FadeIn(mC), run_time=0.5)
        ring = VGroup(*[Circle(radius=0.7, stroke_color=CT, stroke_width=2.5).move_to(m) for m in marks])
        self.at("removed the lower one")
        near = VGroup(*[b for b in bal if min(np.linalg.norm(b.get_center() - np.array(m)) for m in marks) < 1.3])
        self.play(Create(ring), run_time=0.4)
        self.play(FadeOut(near), run_time=0.8)
        ok = T("survives well", 26, CT).move_to([cx, -2.95, 0])
        self.at("survived well")
        self.play(Indicate(mC, color=CT, scale_factor=1.25), FadeIn(ok), run_time=0.9)
        q = T("What had held it back?", 28, TEXT, font=TITLE_FONT).move_to([cx, 3.5, 0])
        self.at("held it back")
        self.play(FadeIn(q), run_time=0.5)
        self.at("mother")
        self.play(FadeOut(ok), FadeIn(near), run_time=0.6)
        arrs = VGroup()
        for g in near:
            c = g.get_center()
            m = min(marks, key=lambda m: np.linalg.norm(c - np.array(m)))
            d = np.array(m) - c
            if np.linalg.norm(d) < 0.3:
                continue
            u = d / np.linalg.norm(d)
            arrs.add(arr(c + u * 0.28, np.array(m) - u * 0.4, BA, w=4, tip=0.15))
        note = T("Balanus left in place", 22, GREY).move_to([cx, -2.95, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.08), FadeIn(note), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Model(SpokenScene):
    def construct(self):
        # --- a shared resource, used by two kinds of individual
        bar = RoundedRectangle(corner_radius=0.2, width=10.0, height=1.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.12).move_to([0, 0.2, 0])
        bar_l = T("a resource in short supply", 34, GREY).move_to(bar)
        A = VGroup(*[dot(BLUE, 0.25) for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([-3.4, 2.7, 0])
        B = VGroup(*[dot(ORANGE, 0.25) for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([3.4, 2.7, 0])
        self.at("That is competition")
        self.play(FadeIn(bar), FadeIn(bar_l), run_time=0.5)
        self.at("Individuals use a resource")
        self.play(FadeIn(A, lag_ratio=0.1), FadeIn(B, lag_ratio=0.1), run_time=0.7)
        lines = VGroup(arr(A.get_bottom() + DOWN * 0.1, [-2.6, 0.95, 0], BLUE, w=4), arr(B.get_bottom() + DOWN * 0.1, [2.6, 0.95, 0], ORANGE, w=4))
        self.play(*[GrowArrow(a) for a in lines], run_time=0.6)
        low = T("each lowers the survival, growth or reproduction of the others", 30, TEXT).move_to([0, -1.5, 0])
        self.at("each lowers the survival")
        self.play(FadeIn(low), Indicate(bar, color=RED, scale_factor=1.03), run_time=0.8)

        # --- the equation
        self.at("asks when two competitors")
        self.play(FadeOut(VGroup(bar, bar_l, A, B, lines, low)), run_time=0.5)
        parts = [("dN1/dt =", GREY), ("r1", GREY), ("N1", BLUE), ("[ 1 -", GREY), ("(", GREY), ("N1", BLUE), ("+", GREY),
                 ("α12 N2", ORANGE), (")", GREY), ("/", GREY), ("K1", BLUE), ("]", GREY)]
        ms = [M(t, 38, c) for t, c in parts]
        eq = VGroup(*ms).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        fit(eq, max_w=12.4).move_to([0, 1.7, 0])
        eqtag = T("species 1, in the model", 28, BLUE).next_to(eq, UP, buff=0.3)
        self.play(FadeIn(eq), FadeIn(eqtag), run_time=0.8)
        own = ms[5]
        brace1 = Brace(own, DOWN, color=BLUE)
        l1 = T("its own numbers", 28, BLUE).next_to(brace1, DOWN, buff=0.1)
        self.at("own numbers")
        self.play(GrowFromCenter(brace1), FadeIn(l1), Indicate(own, color=BLUE), run_time=0.7)
        kk = ms[10]
        brace3 = Brace(kk, DOWN, color=BLUE)
        l3 = T("carrying capacity", 28, BLUE).next_to(brace3, DOWN, buff=0.1)
        self.at("carrying capacity")
        self.play(GrowFromCenter(brace3), FadeIn(l3), Indicate(kk, color=BLUE), run_time=0.7)
        oth = ms[7]
        brace2 = Brace(oth, UP, color=ORANGE)
        l2 = T("the other species, in species 1 units", 28, ORANGE).next_to(brace2, UP, buff=0.1)
        # keep label inside the frame and clear of the equation tag
        eqtag.generate_target()
        self.at("slowed by the other species")
        self.play(FadeOut(eqtag), GrowFromCenter(brace2), FadeIn(l2), Indicate(oth, color=ORANGE), run_time=0.7)
        self.at("Alpha")
        a_def = VGroup(T("α12", 34, ORANGE, weight=BOLD),
                       T("effect of one species 2 individual", 26, ORANGE),
                       T("on species 1", 26, BLUE)).arrange(DOWN, buff=0.12).move_to([0, -1.3, 0])
        self.play(FadeOut(VGroup(brace1, l1, brace3, l3)), FadeIn(a_def), run_time=0.6)
        self.at("one half")
        self.play(FadeOut(a_def), run_time=0.3)
        o1, o2 = dot(ORANGE, 0.4), dot(ORANGE, 0.4)
        pair = VGroup(o1, o2).arrange(RIGHT, buff=0.25)
        eqs = M("=", 40, TEXT)
        b1 = dot(BLUE, 0.4)
        conv = VGroup(pair, eqs, b1).arrange(RIGHT, buff=0.5).move_to([0, -1.2, 0])
        cap = T("α12 = 0.5: two species 2 individuals crowd species 1 as much as one of its own", 28, TEXT).move_to([0, -2.7, 0])
        fit(cap, max_w=12.3)
        self.play(FadeIn(pair, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(eqs), FadeIn(b1), run_time=0.5)
        self.play(FadeIn(cap), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
def plot_base(scene, with_iso=False, a21=0.5):
    ax, xl, yl, tag = make_axes()
    g = VGroup(ax, xl, yl, tag)
    i1, i2 = iso1(ax), iso2(ax, a21)
    ticks = VGroup(tick(ax, 100, 0, "100", BLUE, "below"), tick(ax, 0, 200, "200", BLUE, "left"),
                   tick(ax, 0, 80, "80", ORANGE, "left"), tick(ax, 160, 0, "160", ORANGE, "below"))
    return ax, g, i1, i2, ticks


class S03Isoclines(SpokenScene):
    def construct(self):
        ax, g, i1, i2, ticks = plot_base(self)
        side = VGroup(T("practice values", 24, GREY),
                      T("K1 = 100", 28, BLUE), T("K2 = 80", 28, ORANGE), T("α12 = α21 = 0.5", 28, TEXT),
                      T("N1 = N2 = 20", 28, TEXT), T("r1 = 0.5, r2 = 0.25 per day", 22, TEXT)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.7, 1.8, 0])
        self.at("invented for practice")
        self.play(FadeIn(side), run_time=0.8)
        self.at("Big K is")
        self.play(Indicate(side[1], color=BLUE), run_time=0.6)
        self.at("for species", nth=1)
        self.play(Indicate(side[2], color=ORANGE), run_time=0.6)
        self.at("Both alphas")
        self.play(Indicate(side[3], color=TEXT), run_time=0.6)
        self.at("of each")
        self.play(Indicate(side[4], color=TEXT), run_time=0.5)
        grow = VGroup(T("species 1 grows", 26, BLUE), M("+7 per day", 30, BLUE)).arrange(DOWN, buff=0.12).move_to([4.7, -1.2, 0])
        self.at("individuals per day")
        self.play(FadeIn(grow, shift=UP * 0.15), run_time=0.6)
        self.at("draw each isocline")
        self.play(FadeOut(grow), Create(g), run_time=1.0)
        d0 = Dot(ax.c2p(20, 20), color=TEXT, radius=0.09)
        iso_def = T("isocline: growth is zero", 26, GREY).move_to([4.7, -0.5, 0])
        self.play(FadeIn(d0), FadeIn(iso_def), run_time=0.4)
        self.at("stops on a line")
        self.play(Create(i1), FadeIn(ticks[0]), FadeIn(ticks[1]), run_time=1.6)
        self.at("stops on a line", nth=1)
        self.play(Create(i2), FadeIn(ticks[2]), FadeIn(ticks[3]), run_time=1.6)
        eqp = Dot(ax.c2p(80, 40), color=GREEN, radius=0.16)
        eql = VGroup(T("both stop changing", 26, GREEN), M("80 and 40", 30, GREEN)).arrange(DOWN, buff=0.1).move_to([4.7, -1.7, 0])
        self.at("cross at")
        self.play(FadeOut(iso_def), GrowFromCenter(eqp), FadeIn(eql), run_time=0.8)
        self.finish()


class S04Coexist(SpokenScene):
    def construct(self):
        ax, g, i1, i2, ticks = plot_base(self)
        eqp = Dot(ax.c2p(80, 40), color=GREEN, radius=0.16)
        self.add(g, i1, i2, ticks, eqp)
        hd = T("stable?", 34, TEXT, font=TITLE_FONT).move_to([4.7, 2.6, 0])
        self.at("Is that crossing stable")
        self.play(FadeIn(hd), Indicate(eqp, color=GREEN, scale_factor=1.8), run_time=0.8)
        a1 = arr(ax.c2p(4, 80), ax.c2p(40, 80), BLUE, w=7, tip=0.25)
        t1 = VGroup(T("species 1 rare", 26, BLUE), M("+0.3", 30, BLUE), T("per individual per day", 22, BLUE)).arrange(DOWN, buff=0.08).move_to([4.6, 1.3, 0])
        self.at("rare among species")
        self.play(GrowArrow(a1), FadeIn(t1), run_time=0.9)
        a2 = arr(ax.c2p(100, 4), ax.c2p(100, 44), ORANGE, w=7, tip=0.25)
        t2 = VGroup(T("species 2 rare", 26, ORANGE), M("+0.094", 30, ORANGE), T("per individual per day", 22, ORANGE)).arrange(DOWN, buff=0.1).move_to([4.7, -0.5, 0])
        self.at("rare among species", nth=1)
        self.play(GrowArrow(a2), FadeIn(t2), run_time=0.9)
        both = T("both can increase when rare", 26, GREEN).move_to([4.6, -1.9, 0])
        self.at("Each can increase")
        self.play(FadeIn(both), run_time=0.6)
        p = trace(ax, path(0.5, 0.5))
        d = Dot(ax.c2p(20, 20), color=TEXT, radius=0.09)
        self.at("stable coexistence")
        self.play(FadeOut(VGroup(a1, a2)), FadeIn(d), run_time=0.4)
        self.play(Create(p), MoveAlongPath(d, p), run_time=3.2, rate_func=linear)
        end = T("coexist at 80 and 40", 28, GREEN).move_to([4.6, -2.8, 0])
        self.play(FadeIn(end), run_time=0.5)
        self.finish()


class S05Exclude(SpokenScene):
    def construct(self):
        ax, g, i1, i2, ticks = plot_base(self)
        eqp = Dot(ax.c2p(80, 40), color=GREEN, radius=0.16)
        self.add(g, i1, i2, ticks, eqp)
        chg = VGroup(T("change one number", 26, GREY), M("α21 = 1.0", 36, ORANGE)).arrange(DOWN, buff=0.15).move_to([4.7, 2.3, 0])
        self.at("coefficient")
        self.play(FadeIn(chg), run_time=0.6)
        new2 = iso2(ax, 1.0)
        self.at("Raise alpha")
        self.play(Transform(i2, new2), FadeOut(eqp), FadeOut(ticks[2]), FadeOut(ticks[3]), Indicate(chg[1], color=ORANGE), run_time=1.4)
        a2 = arr(ax.c2p(100, 22), ax.c2p(100, 4), RED, w=7, tip=0.25)
        t2 = VGroup(T("species 2 rare", 26, ORANGE), M("-0.0625", 30, RED), T("per individual per day", 22, RED)).arrange(DOWN, buff=0.1).move_to([4.7, 0.6, 0])
        self.at("rare among species")
        self.play(GrowArrow(a2), FadeIn(t2), run_time=0.9)
        a1 = arr(ax.c2p(4, 80), ax.c2p(40, 80), BLUE, w=7, tip=0.25)
        t1 = VGroup(T("species 1 rare", 26, BLUE), T("can still increase", 26, BLUE)).arrange(DOWN, buff=0.1).move_to([4.7, -1.1, 0])
        self.at("still can")
        self.play(GrowArrow(a1), FadeIn(t1), run_time=0.9)
        p = trace(ax, path(0.5, 1.0), RED)
        d = Dot(ax.c2p(20, 20), color=TEXT, radius=0.09)
        self.at("excludes species")
        self.play(FadeOut(VGroup(a1, a2)), FadeIn(d), run_time=0.4)
        self.play(Create(p), MoveAlongPath(d, p), run_time=3.0, rate_func=linear)
        end = T("species 1 excludes species 2", 26, RED).move_to([4.6, -2.6, 0])
        self.play(FadeIn(end), run_time=0.5)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        title = T("Coexistence needs both", 36, font=TITLE_FONT).move_to([0, 3.1, 0])
        c1 = VGroup(T("species 1:", 28, BLUE), M("K1 > α12 K2", 34, BLUE)).arrange(RIGHT, buff=0.4)
        c2 = VGroup(T("species 2:", 28, ORANGE), M("K2 > α21 K1", 34, ORANGE)).arrange(RIGHT, buff=0.4)
        rows = VGroup(c1, c2).arrange(DOWN, buff=0.9, aligned_edge=LEFT).move_to([-3.6, 1.7, 0])
        y1, y2 = c1.get_center()[1], c2.get_center()[1]
        n1 = VGroup(M("100 > 0.5 x 80 = 40", 30, GREEN), M("holds", 30, GREEN, weight=BOLD)).arrange(RIGHT, buff=0.35).move_to([3.3, y1, 0])
        n2 = VGroup(M("80 > 0.5 x 100 = 50", 30, GREEN), M("holds", 30, GREEN, weight=BOLD)).arrange(RIGHT, buff=0.35).move_to([3.3, y2, 0])
        x2 = VGroup(M("80 > 1.0 x 100", 30, RED), M("fails", 30, RED, weight=BOLD)).arrange(RIGHT, buff=0.35).move_to([3.3, y2 - 0.9, 0])
        x2l = T("with α21 = 1.0", 24, RED).next_to(x2, DOWN, buff=0.1).align_to(x2, LEFT)
        self.play(FadeIn(title), run_time=0.5)
        self.at("needs K1")
        self.play(FadeIn(c1), FadeIn(n1), run_time=0.7)
        self.at("needs K2")
        self.play(FadeIn(c2), FadeIn(n2), run_time=0.7)
        self.at("above alpha", nth=1)
        self.play(FadeIn(x2), FadeIn(x2l), run_time=0.6)
        grow = T("growth rate r appears nowhere in these conditions", 26, GREY).move_to([0, -1.1, 0])
        self.at("growth rate never appears")
        self.play(FadeIn(grow), run_time=0.6)
        self.at("fastest grower need not win")
        self.play(Indicate(grow, color=TEXT), run_time=0.6)
        rule = T("each limits itself more than it limits the other", 34, TEXT, font=TITLE_FONT)
        fit(rule, max_w=11.0)
        rule.move_to([0, -2.6, 0])
        box = SurroundingRectangle(rule, color=GOLD, buff=0.3, stroke_width=3)
        self.at("Keep the rule")
        self.play(FadeOut(grow), run_time=0.3)
        self.play(FadeIn(rule), Create(box), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Competitors coexist when each limits itself more than the other."
