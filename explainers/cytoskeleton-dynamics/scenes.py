"""Why microtubule ends fall apart: the GTP cap  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the microtubule lattice behind the end (GDP-tubulin; also a microtubule drawn whole)
  ORANGE = tubulin that still carries GTP: free dimers about to join, and the GTP cap
  GREEN  = growth (growth line on the trace, "grows")
  RED    = shortening (shortening line on the trace, the peeling end)
  YELLOW = events and the question: catastrophe, rescue, the highlighted ratio, the "?"
  GREY   = seed, axes, labels, not-the-subject
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def beadcol(x, y, color, r=0.17, dy=0.36, rows=5):
    """one column of beads across the protofilaments (a tube seen from the side)."""
    return VGroup(*[Dot([x, y + (k - (rows - 1) / 2) * dy, 0], radius=r, color=color) for k in range(rows)])


def tube(x0, y, colors, r=0.17, dx=0.5, dy=0.36):
    return [beadcol(x0 + i * dx, y, c, r, dy) for i, c in enumerate(colors)]


def peel(cols, y, lag=0.12, rt=0.8, spread=0.55):
    """beads of the last columns swing outward from the axis and fade: protofilaments peeling."""
    anims = []
    for col in cols:
        sub = []
        for d in col:
            off = d.get_center()[1] - y
            sgn = 0 if abs(off) < 1e-3 else np.sign(off)
            sub.append(d.animate.shift([0.45, sgn * (spread + 0.9 * abs(off)), 0]).set_opacity(0))
        anims.append(AnimationGroup(*sub, run_time=rt))
    return LaggedStart(*anims, lag_ratio=lag)


def lab(text, color=GREY, size=26, weight=NORMAL):
    return T(text, size, color, weight=weight)


class Plot:
    """Tiny axes with no LaTeX: maps data (x, y) onto the frame."""

    def __init__(self, origin, w, h, xmax, ymax):
        self.o = np.array([origin[0], origin[1], 0.0]); self.w, self.h, self.xm, self.ym = w, h, xmax, ymax

    def p(self, x, y):
        return self.o + np.array([x / self.xm * self.w, y / self.ym * self.h, 0.0])

    def axes(self):
        xa = Line(self.o, self.o + RIGHT * self.w, color=GREY, stroke_width=3)
        ya = Line(self.o, self.o + UP * self.h, color=GREY, stroke_width=3)
        return VGroup(xa, ya)

    def xtick(self, x, label, size=24):
        t = T(label, size, GREY).next_to(self.p(x, 0), DOWN, buff=0.14)
        k = Line(self.p(x, 0), self.p(x, 0) + DOWN * 0.1, color=GREY, stroke_width=3)
        return VGroup(k, t)

    def ytick(self, y, label, size=22):
        t = M(label, size, GREY).next_to(self.p(0, y), LEFT, buff=0.14)
        k = Line(self.p(0, y), self.p(0, y) + LEFT * 0.1, color=GREY, stroke_width=3)
        return VGroup(k, t)

    def seg(self, a, b, color, w=7):
        return Line(self.p(*a), self.p(*b), color=color, stroke_width=w)


PL = Plot((-5.6, -2.5), 11.0, 5.0, 330, 10)
A, B, C = (0, 5.0), (180, 9.5), (192, 3.5)      # start, peak, trough of the lesson's made-up trace
D, E = (312, 6.5), (325, 0.0)


def plot_frame():
    ax = PL.axes()
    ticks = VGroup(*[PL.ytick(v, s) for v, s in [(0, "0"), (3.5, "3.5"), (5.0, "5.0"), (9.5, "9.5")]],
                   PL.xtick(0, "0"), PL.xtick(180, "180 s"))
    yl = T("length from the seed (µm)", 24, GREY).move_to([-3.4, PL.o[1] + PL.h + 0.4, 0])
    xl = T("time (s)", 24, GREY).move_to([4.9, PL.o[1] - 0.55, 0])
    return ax, ticks, yl, xl


# tube geometry shared by the large side-view scenes
TX0, TY = -6.0, 0.1
BIG = dict(r=0.32, dx=0.72, dy=0.68)


def big_tube(n_blue, n_cap, y=TY):
    return tube(TX0, y, [BLUE] * n_blue + [ORANGE] * n_cap, **BIG)


def until(scene, phrase, margin=0.35, floor=0.4, nth=0):
    """seconds from now until just before the narrator says `phrase` (so an animation can fill the gap)."""
    return max(floor, scene.t_of(phrase, nth) - 0.2 - scene.elapsed() - margin)


class S00Title(TitleCard):
    LESSON = "Cytoskeletal polymers and dynamics"
    TITLE = "Why microtubule ends fall apart"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """the puzzle: a tube grows slowly, shrinks many times faster, grows again. Why built to fail?"""

    def construct(self):
        y = -0.1
        dx, x0 = 0.62, -5.2
        kw = dict(r=0.3, dy=0.62)
        seed = Rectangle(width=0.7, height=3.4, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.4).move_to([-5.7, y, 0])
        seed_l = lab("seed", GREY, 26).move_to([-5.7, y - 2.05, 0])
        rng = np.random.RandomState(4)
        dots = VGroup()
        while len(dots) < 26:
            px, py = rng.uniform(-6.0, 6.0), rng.choice([rng.uniform(2.35, 3.3), rng.uniform(-3.3, -2.5)])
            if py < 0 and abs(px) < 2.4:
                continue
            dots.add(Dot([px, py, 0], radius=0.09, color=ORANGE))
        dish = lab("purified tubulin", ORANGE, 26).move_to([0, -3.0, 0])
        cols = [beadcol(x0 + i * dx, y, BLUE, **kw) for i in range(16)]

        self.at("Watch one microtubule")
        self.play(FadeIn(seed), FadeIn(seed_l), run_time=0.8)
        self.at("grow from")
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.4) for c in cols[:3]], lag_ratio=1.0, run_time=1.8))
        self.at("purified tubulin")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.03), FadeIn(dish), run_time=1.4)

        slow = lab("slow growth", GREEN, 32, BOLD).move_to([-1.0, 2.0, 0])
        self.at("lengthens slowly")
        self.play(FadeIn(slow), LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in cols[3:15]], lag_ratio=1.0,
                                             run_time=until(self, "then shrinks many times faster")))
        fast = lab("rapid shortening", RED, 32, BOLD).move_to([-1.0, 2.0, 0])
        self.at("then shrinks many times faster")
        self.play(ReplacementTransform(slow, fast),
                  LaggedStart(*[FadeOut(c, shift=RIGHT * 0.1) for c in reversed(cols[5:15])], lag_ratio=0.1, run_time=0.9))
        again = lab("growing again", GREEN, 32, BOLD).move_to([-1.0, 2.0, 0])
        self.at("starts growing again")
        self.play(ReplacementTransform(fast, again),
                  LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in cols[5:11]], lag_ratio=1.0,
                              run_time=until(self, "Why would a polymer", margin=0.2)))
        q = T("?", 140, YELLOW, weight=BOLD).move_to([4.9, y, 0])
        self.at("Why would a polymer")
        self.play(FadeOut(again), FadeIn(q, scale=0.5), run_time=0.6)
        head = T("Why build a polymer to fail?", 40, font=TITLE_FONT).move_to([-0.5, 1.9, 0])
        self.play(Write(head), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Trace(SpokenScene):
    """length versus time: slow growth, then a drop 20 times faster."""

    def construct(self):
        ax, ticks, yl, xl = plot_frame()
        head = T("One plus end: a made-up trace", 34, font=TITLE_FONT).to_edge(UP, buff=0.35)
        self.at("Plot the length")
        self.play(Create(ax), FadeIn(ticks), FadeIn(yl), FadeIn(xl), run_time=1.4)

        g1 = PL.seg(A, B, GREEN)
        tip = Dot(PL.p(*A), radius=0.13, color=YELLOW)
        pe = lab("plus end", YELLOW, 28, BOLD).move_to(PL.p(45, 7.6))
        pe_a = Arrow(pe.get_bottom() + DOWN * 0.05, PL.p(3, 5.2), buff=0, color=YELLOW, stroke_width=4, tip_length=0.2,
                     max_tip_length_to_length_ratio=0.5)
        self.at("plus end")
        self.play(FadeIn(tip, scale=2.0), FadeIn(pe), GrowArrow(pe_a), run_time=0.6)
        self.at("made up")
        self.play(Write(head), run_time=1.2)
        self.at("It grows")
        self.play(FadeOut(pe), FadeOut(pe_a), run_time=0.3)
        self.play(Create(g1), MoveAlongPath(tip, g1), run_time=until(self, "That is", margin=0.9), rate_func=linear)
        drop_ref = DashedLine(PL.p(180, 0), PL.p(180, 9.5), color=GREY, stroke_width=2)
        self.play(Create(drop_ref), run_time=0.4)
        self.at("That is")
        gl = lab("growth: 1.5 µm per min", GREEN, 28, BOLD).move_to(PL.p(95, 2.6))
        self.play(FadeIn(gl, shift=UP * 0.15), run_time=0.5)

        g2 = PL.seg(B, C, RED)
        self.at("Then it loses")
        self.play(Create(g2), tip.animate.move_to(PL.p(*C)), run_time=0.5, rate_func=linear)
        l6 = lab("loses 6 µm in 12 s", RED, 28).move_to([3.5, 1.3, 0])
        self.at("loses six")
        self.play(FadeIn(l6, shift=LEFT * 0.15), run_time=0.5)
        self.at("and the line")
        self.play(Indicate(g2, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.at("That is", nth=1)
        sl = lab("shortening: 30 µm per min", RED, 28, BOLD).move_to([3.5, 0.6, 0])
        self.play(FadeIn(sl, shift=LEFT * 0.15), run_time=0.5)
        self.at("times faster")
        ff = lab("20 times faster", YELLOW, 32, BOLD).move_to([3.5, -0.1, 0])
        self.play(FadeIn(ff, scale=0.8), Indicate(sl, color=YELLOW, scale_factor=1.05), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cap(SpokenScene):
    """zoom on the plus end: dimers join with GTP, the ones behind turn to GDP, the cap holds the end."""

    def construct(self):
        head = T("The growing plus end", 38, font=TITLE_FONT).to_edge(UP, buff=0.4)
        cols = big_tube(9, 0)
        self.at("Why does an end")
        self.play(Write(head), FadeIn(VGroup(*cols)), run_time=1.0)
        tipx = TX0 + 8 * BIG["dx"]
        pe = lab("plus end", TEXT, 30, BOLD).move_to([tipx + 2.2, TY + 1.7, 0])
        pe_a = Arrow([tipx + 1.9, TY + 1.4, 0], [tipx + 0.5, TY + 0.6, 0], buff=0, color=TEXT, stroke_width=4,
                     tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(pe), GrowArrow(pe_a), run_time=0.5)

        new = [beadcol(TX0 + (9 + i) * BIG["dx"], TY, ORANGE, BIG["r"], BIG["dy"]) for i in range(5)]
        chip_d = chip("tubulin dimer with GTP", ORANGE, 26).move_to([4.0, 2.55, 0])
        self.at("Each tubulin dimer")
        self.play(FadeIn(chip_d), FadeOut(pe), FadeOut(pe_a), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 2.0) for c in new], lag_ratio=0.5,
                              run_time=until(self, "soon after", margin=1.2)))

        gdp_chip = chip("GDP-tubulin", BLUE, 26).move_to([-3.2, -2.55, 0])
        self.at("soon after")
        self.play(new[0].animate.set_color(BLUE), run_time=0.6)
        self.at("once the dimer")
        self.play(new[1].animate.set_color(BLUE), run_time=0.6)
        self.at("behind the end")
        self.play(FadeOut(chip_d), FadeIn(gdp_chip), Indicate(VGroup(*cols[6:], new[0], new[1]), color=BLUE, scale_factor=1.06),
                  run_time=0.9)

        lat = VGroup(*cols[:9])
        br1 = Brace(lat, UP, color=BLUE, buff=0.15)
        t1 = lab("held only by its neighbours", BLUE, 28).next_to(br1, UP, buff=0.12)
        self.at("held in")
        self.play(GrowFromCenter(br1), run_time=0.7)
        self.at("only by")
        self.play(FadeIn(t1), run_time=0.6)

        cap = VGroup(*new[2:])
        br2 = Brace(cap, DOWN, color=ORANGE, buff=0.15)
        t2 = lab("GTP cap", ORANGE, 32, BOLD).next_to(br2, DOWN, buff=0.12)
        self.at("stays intact")
        self.play(FadeOut(br1), FadeOut(t1), FadeOut(gdp_chip), run_time=0.3)
        self.play(GrowFromCenter(br2), FadeIn(t2), run_time=0.7)
        self.at("cap of dimers")
        self.play(Indicate(cap, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Catastrophe(SpokenScene):
    """cap lost -> peeling -> catastrophe, rescue, dynamic instability on the trace."""

    def construct(self):
        cols = tube(TX0, TY, [BLUE] * 11 + [ORANGE] * 3, **BIG)
        cap = VGroup(*cols[11:])
        br2 = Brace(cap, DOWN, color=ORANGE, buff=0.15)
        t2 = lab("GTP cap", ORANGE, 32, BOLD).next_to(br2, DOWN, buff=0.12)
        tipx = TX0 + 13 * BIG["dx"]
        add_a = Arrow([tipx + 2.8, TY, 0], [tipx + 0.8, TY, 0], buff=0, color=ORANGE, stroke_width=7, tip_length=0.28,
                      max_tip_length_to_length_ratio=0.5)
        add_l = VGroup(lab("dimers", ORANGE, 26), lab("added", ORANGE, 26)).arrange(DOWN, buff=0.08).next_to(add_a, UP, buff=0.15)
        self.add(VGroup(*cols), br2, t2, add_a, add_l)

        self.at("addition slows")
        slow_l = VGroup(lab("addition", ORANGE, 26), lab("slows", ORANGE, 26)).arrange(DOWN, buff=0.08).move_to(add_l)
        self.play(add_a.animate.set_opacity(0.25), ReplacementTransform(add_l, slow_l), run_time=0.7)
        lost = lab("cap lost", RED, 32, BOLD).move_to(t2)
        self.at("hydrolysis")
        self.play(LaggedStart(*[c.animate.set_color(BLUE) for c in cols[11:]], lag_ratio=1.0,
                              run_time=until(self, "cap is lost", margin=0.1, floor=1.0)))
        self.at("cap is lost")
        self.play(FadeOut(br2), ReplacementTransform(t2, lost), run_time=0.5)
        self.at("comes apart")
        self.play(FadeOut(slow_l), FadeOut(add_a), FadeOut(lost), run_time=0.3)
        self.play(peel(cols[12:][::-1], TY, lag=0.5, rt=0.8, spread=0.8), run_time=1.6)
        self.at("peeling outward")
        self.play(peel(cols[8:12][::-1], TY, lag=0.5, rt=0.8, spread=0.8),
                  run_time=until(self, "shortens fast", margin=0.3, floor=1.0))
        sf = lab("shortens fast", RED, 34, BOLD).move_to([0.0, 2.6, 0])
        self.at("shortens fast")
        self.play(FadeIn(sf, scale=0.9), run_time=0.5)

        # --- the whole trace comes back -------------------------------------------------------
        ax, ticks, yl, xl = plot_frame()
        g1, g2 = PL.seg(A, B, GREEN), PL.seg(B, C, RED)
        g3, g4 = PL.seg(C, D, GREEN), PL.seg(D, E, RED)
        self.at("That switch")
        self.play(FadeOut(sf), FadeOut(VGroup(*cols[:8])), Create(ax), FadeIn(ticks), FadeIn(yl), FadeIn(xl), run_time=0.6)
        self.play(Create(g1), run_time=0.7, rate_func=linear)
        self.play(Create(g2), run_time=0.25, rate_func=linear)
        cat1 = chip("catastrophe", YELLOW, 26).move_to([2.8, 2.3, 0])
        self.at("is a catastrophe")
        self.play(FadeIn(cat1, shift=LEFT * 0.2), run_time=0.5)
        self.at("The switch back")
        self.play(Create(g3), run_time=0.9, rate_func=linear)
        res = chip("rescue", YELLOW, 26).move_to([0.8, -1.2, 0])
        self.at("a rescue")
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.5)
        self.play(Create(g4), run_time=0.3, rate_func=linear)
        cat2 = chip("catastrophe", YELLOW, 24).move_to([4.7, 1.45, 0])
        self.play(FadeIn(cat2), run_time=0.4)
        path = VMobject()
        path.set_points_as_corners([PL.p(*q) for q in (A, B, C, D, E)])
        tip = Dot(PL.p(*A), radius=0.14, color=YELLOW)
        self.at("Each end switches")
        self.add(tip)
        self.play(MoveAlongPath(tip, path), run_time=until(self, "dynamic instability", margin=0.2, floor=2.0), rate_func=linear)
        head = T("dynamic instability", 40, font=TITLE_FONT, color=YELLOW).to_edge(UP, buff=0.3)
        self.at("dynamic instability")
        self.play(Write(head), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Tests(SpokenScene):
    """two tests of the cap: slowed hydrolysis lengthens it; more tubulin makes catastrophes rarer."""

    def row(self, y, n_blue, n_cap, x0=-6.2):
        return tube(x0, y, [BLUE] * n_blue + [ORANGE] * n_cap, r=0.22, dx=0.58, dy=0.46)

    def construct(self):
        y1, y2 = 1.35, -1.45
        head = T("Human tubulin with slowed hydrolysis", 34, font=TITLE_FONT).to_edge(UP, buff=0.35)
        r1 = self.row(y1, 7, 3)
        r2 = self.row(y2, 7, 3)
        l1 = lab("normal hydrolysis", TEXT, 32, BOLD).move_to([3.4, y1 + 0.25, 0])
        l1c = lab("a short GTP cap", ORANGE, 28).next_to(l1, DOWN, buff=0.15)
        self.at("The cap idea")
        self.play(FadeIn(VGroup(*r1)), FadeIn(VGroup(*r2)), run_time=0.8)
        self.at("a team used")
        self.play(Write(head), run_time=0.7)
        self.at("recombinant human")
        self.play(FadeIn(l1), FadeIn(l1c), run_time=0.8)
        l2 = lab("slowed hydrolysis", TEXT, 32, BOLD).move_to([3.4, y2 + 0.25, 0])
        self.at("mutations that slow")
        self.play(FadeIn(l2), run_time=0.5)
        l2c = lab("a longer GTP cap", ORANGE, 28).next_to(l2, DOWN, buff=0.15)
        self.at("grew longer")
        self.play(LaggedStart(*[c.animate.set_color(ORANGE) for c in r2[3:7]], lag_ratio=0.4,
                              run_time=until(self, "Earlier work", margin=0.3, floor=0.8)),
                  FadeIn(l2c))

        # --- part B: more tubulin ---------------------------------------------------------------
        self.at("Earlier work")
        self.play(FadeOut(VGroup(*r1, *r2, l1, l1c, l2, l2c, head)), run_time=0.5)
        head2 = T("Pig brain tubulin, free of other proteins", 34, font=TITLE_FONT).to_edge(UP, buff=0.35)
        b1 = self.row(y1, 8, 2)
        b2 = self.row(y2, 6, 4)
        rng = np.random.RandomState(7)
        d1 = VGroup(*[Dot([0.0 + i * 0.9 + rng.uniform(-0.15, 0.15), y1 + rng.uniform(-0.6, 0.6), 0], radius=0.11,
                          color=ORANGE) for i in range(3)])
        d2 = VGroup(*[Dot([-0.1 + (i % 5) * 0.55, y2 + (i // 5 - 0.5) * 0.55, 0], radius=0.11, color=ORANGE)
                      for i in range(10)])
        m1 = VGroup(lab("less tubulin", TEXT, 30, BOLD)).move_to([4.9, y1, 0])
        m2 = VGroup(lab("more tubulin", TEXT, 30, BOLD), lab("catastrophes rarer", GREEN, 26),
                    lab("(fits a larger cap)", ORANGE, 26)).arrange(DOWN, buff=0.1).move_to([4.9, y2, 0])
        self.play(FadeIn(head2), FadeIn(VGroup(*b1)), FadeIn(VGroup(*b2)), run_time=0.9)
        self.at("free of other")
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.8)
        self.at("more tubulin")
        self.play(FadeIn(m1[0]), FadeIn(m2[0]), run_time=0.4)
        self.play(Indicate(d2, color=ORANGE, scale_factor=1.15), run_time=0.5)
        self.at("rarer")
        self.play(FadeIn(m2[1], shift=LEFT * 0.15), run_time=0.6)
        self.at("larger cap")
        cb = Brace(VGroup(*b2[6:]), DOWN, color=ORANGE, buff=0.12)
        self.play(GrowFromCenter(cb), FadeIn(m2[2]), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """the rule: assembly, hydrolysis behind, cap holds the end; lose the cap and it shortens fast."""

    def construct(self):
        cols = big_tube(9, 0)
        tipx = TX0 + 8 * BIG["dx"]
        self.add(VGroup(*cols))
        new = [beadcol(TX0 + (9 + i) * BIG["dx"], TY, ORANGE, BIG["r"], BIG["dy"]) for i in range(5)]
        a1 = Arrow([tipx + 6.2, TY, 0], [tipx + 5.0, TY, 0], buff=0, color=ORANGE, stroke_width=7, tip_length=0.28,
                   max_tip_length_to_length_ratio=0.5)
        self.at("Binding drives")
        self.play(GrowArrow(a1), LaggedStart(*[FadeIn(c, shift=LEFT * 1.6) for c in new], lag_ratio=0.35,
                                              run_time=until(self, "hydrolysis comes", margin=0.2)))
        self.at("hydrolysis comes")
        self.play(new[0].animate.set_color(BLUE), FadeOut(a1), run_time=0.6)
        self.at("afterwards")
        self.play(new[1].animate.set_color(BLUE), run_time=0.6)
        self.at("old lattice")
        self.play(Indicate(VGroup(*cols[6:], new[0], new[1]), color=BLUE, scale_factor=1.05), run_time=0.9)
        cap = VGroup(*new[2:])
        br = Brace(cap, DOWN, color=ORANGE, buff=0.15)
        t = lab("GTP cap", ORANGE, 32, BOLD).next_to(br, DOWN, buff=0.12)
        self.at("A cap of dimers")
        self.play(GrowFromCenter(br), FadeIn(t), run_time=0.7)
        self.at("holds the end")
        self.play(Indicate(cap, color=ORANGE, scale_factor=1.12), run_time=0.7)

        ql = lab("what commits an end to shortening?", YELLOW, 32, BOLD).move_to([0.0, 2.7, 0])
        self.at("Exactly what commits")
        self.play(FadeIn(ql, shift=DOWN * 0.15), run_time=0.7)
        self.at("still argued")
        self.play(Indicate(ql, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("Keep the rule")
        self.play(FadeOut(ql), run_time=0.4)
        self.at("Lose the cap")
        lost = lab("cap lost", RED, 32, BOLD).move_to(t)
        self.play(*[c.animate.set_color(BLUE) for c in new[2:]], FadeOut(br), ReplacementTransform(t, lost), run_time=0.7)
        allc = cols + new
        self.play(FadeOut(lost), run_time=0.2)
        sf = lab("shortens rapidly", RED, 40, BOLD).move_to([0.0, 2.4, 0])
        self.play(peel(allc[-8:][::-1], TY, lag=0.2, rt=0.7, spread=0.8),
                  run_time=until(self, "shortens rapidly", margin=0.2, floor=1.2))
        self.at("shortens rapidly")
        self.play(FadeIn(sf, scale=0.9), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Lose the GTP cap, and a microtubule end shortens fast."
