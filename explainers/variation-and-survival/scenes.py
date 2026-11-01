"""Variation and survival: who survives changes the population  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = an animal WITH tusks (token with two short tusk bars)
  YELLOW = an animal with NO tusks (plain token); also the "no tusks" share in the bars
  RED    = the pressure: war, poaching, "killed" crosses
  GREEN  = survival (survivors, "some survive more")
  PURPLE = variation and the common alleles (the two squares already in the population)
  ORANGE = the second existing allele
  MINT   = a NEW allele made by mutation
  PINK   = alleles that arrive by gene flow
  TEAL   = young (crab eggs, calf)
  GOLD   = the take-home idea (population changes) and the question
  GREY   = outlines, labels, neutral animals (the elephant and calf in the numbers scene)
Animal tokens are an illustration, not counts. The share bars use only the lesson's "about 1 in 5"
and "about half".
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MINT = "#6FE3B0"
PINK = "#E88FB4"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def animal(tusked, s=1.0, color=None):
    """A schematic labelled-block animal: a rounded token; two short bars below it mean tusks."""
    c = color or (BLUE if tusked else YELLOW)
    body = RoundedRectangle(corner_radius=0.12, width=0.62, height=0.48, stroke_color=c, stroke_width=3,
                            fill_color=c, fill_opacity=0.3)
    parts = [body]
    if tusked:
        for dx in (-0.17, 0.17):
            parts.append(Line([dx, -0.22, 0], [dx, -0.46, 0], color=TEXT, stroke_width=6))
    g = VGroup(*parts)
    g.tusked = tusked
    return g.scale(s)


TUSKLESS = {3, 9, 14, 20, 26, 31, 35, 38}                       # 8 of 40 = 1 in 5
TUSKED = [i for i in range(40) if i not in TUSKLESS]            # 32
KILLED_TUSKED = [i for k, i in enumerate(TUSKED) if k % 4 != 0]  # 24 of 32
KILLED_TUSKLESS = [14]                                           # 1 of 8
SURVIVORS = [i for i in range(40) if i not in KILLED_TUSKED and i not in KILLED_TUSKLESS]  # 15


def herd(cx=-3.4, cy=0.35):
    toks = []
    for i in range(40):
        t = animal(i not in TUSKLESS)
        t.move_to([cx + (i % 8 - 3.5) * 0.9, cy + (2 - i // 8) * 0.82, 0])
        t.idx = i
        toks.append(t)
    return toks


def legend(cx=-3.4, y=-2.35):
    a = animal(True, 0.8)
    la = T("has tusks", 24, BLUE)
    b = animal(False, 0.8)
    lb = T("no tusks", 24, YELLOW)
    g = VGroup(VGroup(a, la).arrange(RIGHT, buff=0.2), VGroup(b, lb).arrange(RIGHT, buff=0.2)).arrange(RIGHT, buff=0.9)
    return g.move_to([cx, y, 0])


def note(text, y=-3.1, cx=-3.4):
    return T(text, 22, GREY).move_to([cx, y, 0])


def cross(mob):
    w = 0.34
    c = mob.get_center()
    return VGroup(Line(c + [-w, -w, 0], c + [w, w, 0], color=RED, stroke_width=7),
                  Line(c + [-w, w, 0], c + [w, -w, 0], color=RED, stroke_width=7))


def bar(frac_no_tusk, width=6.0, height=0.6):
    """stacked share bar: yellow = no tusks (left), blue = tusks (right)."""
    y = Rectangle(width=width * frac_no_tusk, height=height, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
    b = Rectangle(width=width * (1 - frac_no_tusk), height=height, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
    b.next_to(y, RIGHT, buff=0)
    g = VGroup(y, b)
    g.yel, g.blu = y, b
    return g


class S00Title(TitleCard):
    LESSON = "Variation and survival"
    TITLE = "Who Survives Changes the Population"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """the puzzle: a herd before the war, the survivors after, and no elephant lost her tusks."""

    def construct(self):
        toks = herd()
        grp = VGroup(*toks)
        leg = legend()
        nt = note("tokens are an illustration, not counts")
        head = T("Gorongosa National Park, Mozambique", 30, TEXT).to_edge(UP, buff=0.5)

        self.at("Gorongosa National Park")
        self.play(FadeIn(head, shift=DOWN * 0.1), LaggedStart(*[FadeIn(t, scale=0.7) for t in toks], lag_ratio=0.03),
                  FadeIn(leg), FadeIn(nt), run_time=2.2)

        war = chip("civil war, 1977 to 1992", RED, 28).move_to([3.5, 2.15, 0])
        self.at("The war lasted")
        self.play(FadeIn(war, shift=LEFT * 0.2), run_time=0.6)

        b1 = VGroup(T("Before the war", 26, GREY), T("about 1 in 5", 44, YELLOW, weight=BOLD),
                    T("sampled females had no tusks", 26, TEXT)).arrange(DOWN, buff=0.12).move_to([3.5, 0.55, 0])
        self.at("Before the war")
        self.play(FadeIn(b1, shift=LEFT * 0.2), run_time=0.6)
        self.play(*[Indicate(toks[i], color=YELLOW, scale_factor=1.25) for i in sorted(TUSKLESS)], run_time=1.0)

        b2 = VGroup(T("Females that survived", 26, GREY), T("about half", 44, YELLOW, weight=BOLD),
                    T("had no tusks", 26, TEXT)).arrange(DOWN, buff=0.12).move_to([3.5, -1.3, 0])
        self.at("Among the females")
        gone = [toks[i] for i in range(40) if i not in SURVIVORS]
        self.play(FadeOut(VGroup(*gone), scale=0.6), FadeIn(b2, shift=LEFT * 0.2), run_time=1.0)

        self.at("did not come")
        keep = [toks[i] for i in SURVIVORS if toks[i].tusked]
        self.play(*[Indicate(t, color=BLUE, scale_factor=1.25) for t in keep], run_time=1.2)

        q = T("How did the population change?", 26, GOLD, weight=BOLD).move_to([3.3, -2.95, 0])
        self.at("So how did")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Vary(SpokenScene):
    """individuals differ; alleles; mutation adds one; gene flow brings some; sexual reproduction regroups."""

    def construct(self):
        # row of different individuals
        pat = [1, 1, 0, 1, 1, 0, 1]
        row = VGroup(*[animal(bool(p), 1.1) for p in pat]).arrange(RIGHT, buff=0.7).move_to([0, 2.65, 0])
        vlab = T("variation: the differences among individuals", 28, PURPLE).move_to([0, 1.75, 0])
        self.at("Individuals differ")
        self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in row], lag_ratio=0.12), run_time=1.5)
        self.at("Variation means")
        self.play(FadeIn(vlab, shift=UP * 0.1), run_time=0.6)

        # box of alleles
        box1 = RoundedRectangle(corner_radius=0.2, width=5.2, height=2.6, stroke_color=GREY, stroke_width=3).move_to([-3.2, -0.85, 0])
        box2 = RoundedRectangle(corner_radius=0.2, width=3.6, height=2.6, stroke_color=GREY, stroke_width=3).move_to([4.1, -0.85, 0])
        t1 = T("one population", 24, GREY).next_to(box1, UP, buff=0.12)
        t2 = T("another population", 24, GREY).next_to(box2, UP, buff=0.12)
        cols = [PURPLE, ORANGE]
        sq = []
        for k in range(8):
            s = Square(0.4, stroke_color=cols[k % 2], stroke_width=3, fill_color=cols[k % 2], fill_opacity=0.5)
            s.move_to([-3.2 + (k % 4 - 1.5) * 0.9, -0.85 + (0.5 - k // 4) * 0.9, 0])
            sq.append(s)
        cap = T("alleles: versions of one gene", 26, TEXT).move_to([-3.2, -2.9, 0])
        self.at("An allele is one")
        self.play(FadeIn(box1), FadeIn(t1), LaggedStart(*[FadeIn(s, scale=0.6) for s in sq], lag_ratio=0.08),
                  FadeIn(cap), run_time=1.6)

        # mutation: a new allele
        new = Square(0.4, stroke_color=MINT, stroke_width=3, fill_color=MINT, fill_opacity=0.7).move_to([-3.2 + 2.25, -0.85 + 0.45, 0])
        cap2 = T("mutation: a change in DNA", 26, MINT).move_to([-3.2, -2.9, 0])
        cap2b = T("mutation: source of new alleles", 26, MINT).move_to([-3.2, -2.9, 0])
        self.at("A mutation is")
        self.play(ReplacementTransform(cap, cap2), run_time=0.6)
        self.at("original source")
        self.play(FadeIn(new, scale=2.0), ReplacementTransform(cap2, cap2b), run_time=0.6)
        self.play(Flash(new, color=MINT, flash_radius=0.5), run_time=0.5)
        sq.append(new)

        # gene flow
        pk = []
        for k in range(3):
            s = Square(0.4, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.6)
            s.move_to([4.1 + (k - 1) * 0.9, -0.85, 0])
            pk.append(s)
        flow = Arrow([2.1, -0.85, 0], [-0.55, -0.85, 0], color=PINK, stroke_width=6, buff=0.0)
        cap3 = T("gene flow: alleles move between populations", 26, PINK).move_to([0.2, -2.9, 0])
        self.at("Gene flow is")
        self.play(FadeIn(box2), FadeIn(t2), FadeIn(VGroup(*pk), scale=0.7), ReplacementTransform(cap2b, cap3), run_time=0.9)
        self.play(GrowArrow(flow), run_time=0.5)
        dest = [[-5.45, -0.4, 0], [-5.45, -1.3, 0], [-0.95, -1.3, 0]]
        self.play(*[p.animate.move_to(d) for p, d in zip(pk, dest)], run_time=1.4)
        sq += pk

        # sexual reproduction: regroup into pairs
        order = [0, 5, 2, 9, 4, 11, 1, 8, 3, 10, 6, 7]
        pair_cx = [-4.5, -3.2, -1.9]
        moves, rects = [], []
        for pi in range(6):
            cx = pair_cx[pi % 3]
            cy = -0.85 + (0.5 - pi // 3) * 0.9
            for j in range(2):
                moves.append(sq[order[pi * 2 + j]].animate.move_to([cx + (j - 0.5) * 0.46, cy, 0]))
            r = RoundedRectangle(corner_radius=0.1, width=1.06, height=0.62, stroke_color=GREY, stroke_width=2).move_to([cx, cy, 0])
            rects.append(r)
        cap4 = T("sexual reproduction: new combinations", 26, TEXT).move_to([-3.2, -2.9, 0])
        self.at("Sexual reproduction shuffles")
        self.play(FadeOut(flow), FadeOut(box2), FadeOut(t2), ReplacementTransform(cap3, cap4), *moves, run_time=1.8)
        self.play(*[Create(r) for r in rects], run_time=0.8)
        self.at("already exist")
        self.play(*[Indicate(r, color=TEXT, scale_factor=1.12) for r in rects], run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Surplus(SpokenScene):
    """more young than can survive: crab egg mass fades to a few; an elephant has one calf."""

    def construct(self):
        head = T("more young than the environment can support", 30, TEXT).to_edge(UP, buff=0.5)
        self.at("Populations tend")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.8)

        cx, cy = -3.3, -0.15
        block = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.5, stroke_color=TEAL, stroke_width=3).move_to([cx, cy, 0])
        dots = []
        for r in range(9):
            for c in range(15):
                d = Dot(radius=0.075, color=TEAL).move_to([cx + (c - 7) * 0.34, cy + (4 - r) * 0.34, 0])
                dots.append(d)
        lab = T("blue crab: one egg mass", 28, TEAL).move_to([cx, cy + 2.2, 0])
        cnt = T("about 750,000 to 8 million eggs", 26, TEXT).move_to([cx, cy - 2.2, 0])
        src = T("Chesapeake Bay, reported range; dots not to scale", 22, GREY).move_to([cx, cy - 2.75, 0])
        self.at("A female blue crab")
        self.play(FadeIn(block), FadeIn(lab), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.006),
                  run_time=1.6)
        self.at("an egg mass")
        self.play(FadeIn(cnt, shift=UP * 0.1), FadeIn(src), run_time=0.8)

        keep = [dots[i] for i in (20, 47, 71, 96, 119)]
        rest = [d for d in dots if d not in keep]
        small = T("a small fraction become adult crabs", 26, GREEN).move_to([cx, cy - 2.2, 0])
        self.at("Only a small fraction")
        self.play(*[d.animate.set_opacity(0.12) for d in rest], *[d.animate.set_color(GREEN).scale(1.7) for d in keep],
                  ReplacementTransform(cnt, small), run_time=1.0)
        self.at("Most die young")
        self.play(FadeOut(VGroup(*rest)), *[Indicate(d, color=GREEN, scale_factor=1.5) for d in keep], run_time=1.0)

        # elephant: one calf
        ex = 3.6
        mom = animal(False, 1.7, GREY).move_to([ex - 0.8, 0.6, 0])
        calf = animal(False, 0.9, GREY).move_to([ex + 0.95, 0.35, 0])
        for p in (mom, calf):
            p.set_stroke(GREY)
        ml = T("elephant", 26, GREY).next_to(mom, DOWN, buff=0.25)
        cl = T("calf", 26, TEAL).next_to(calf, DOWN, buff=0.25)
        calf.set_color(TEAL)
        one = T("usually one calf at a birth", 28, TEXT).move_to([ex, -1.35, 0])
        self.at("An elephant usually")
        self.play(FadeIn(mom, scale=0.8), FadeIn(ml), run_time=0.7)
        self.play(FadeIn(calf, scale=0.5), FadeIn(cl), FadeIn(one, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Pressure(SpokenScene):
    """the pressure: poachers want ivory, tusked elephants are killed more often, tuskless survive more often."""

    def construct(self):
        toks = herd()
        leg = legend()
        nt = note("tokens are an illustration, not counts")
        self.at("Now add a pressure")
        self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in toks], lag_ratio=0.02), FadeIn(leg), FadeIn(nt), run_time=1.0)

        sp = chip("selective pressure", RED, 30).move_to([3.5, 2.4, 0])
        sp_sub = T("makes some variants more likely", 24, TEXT).move_to([3.5, 1.7, 0])
        sp_sub2 = T("to survive or reproduce than others", 24, TEXT).next_to(sp_sub, DOWN, buff=0.08)
        self.at("A selective pressure")
        self.play(FadeIn(sp, shift=LEFT * 0.2), run_time=0.6)
        self.at("makes some variants")
        self.play(FadeIn(sp_sub), FadeIn(sp_sub2), run_time=0.6)

        po = chip("poachers want ivory", RED, 28).move_to([3.5, 0.45, 0])
        pa = Arrow([po.get_left()[0] - 0.05, 0.45, 0], [-0.1, 0.45, 0], color=RED, stroke_width=6, buff=0.05)
        self.at("poachers wanted ivory")
        self.play(FadeIn(po, shift=LEFT * 0.2), GrowArrow(pa), run_time=0.8)

        kt = T("tusked: killed more often", 28, BLUE).move_to([3.5, -0.75, 0])
        crosses = [cross(toks[i]) for i in KILLED_TUSKED]
        self.at("tusked elephants were killed")
        self.play(FadeIn(kt, shift=LEFT * 0.2),
                  LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.03), run_time=1.5)
        ct = cross(toks[14])
        self.play(Create(ct), run_time=0.3)
        gone = VGroup(*[toks[i] for i in KILLED_TUSKED + KILLED_TUSKLESS], *crosses, ct)
        self.play(FadeOut(gone, scale=0.6), FadeOut(pa), run_time=0.6)

        ut = T("no tusks: survived more often", 28, YELLOW).move_to([3.5, -1.65, 0])
        self.at("Tuskless females already existed")
        self.play(FadeIn(ut, shift=LEFT * 0.2),
                  *[Indicate(toks[i], color=YELLOW, scale_factor=1.3) for i in sorted(TUSKLESS - {14})], run_time=1.3)

        ns = chip("natural selection", GOLD, 30).move_to([3.5, -2.75, 0])
        self.at("That is natural selection")
        self.play(FadeIn(ns, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Count(SpokenScene):
    """count the survivors: share bars, then individuals versus populations."""

    def construct(self):
        toks = herd()
        surv = VGroup(*[toks[i] for i in SURVIVORS])
        legc = legend(cx=-4.3, y=-1.5)
        self.add(surv)
        self.at("Now count the survivors")
        # compact the survivors into a 5 x 3 block on the left
        moves = []
        for k, i in enumerate(SURVIVORS):
            moves.append(toks[i].animate.move_to([-4.3 + (k % 5 - 2) * 0.95, 1.0 + (1 - k // 5) * 1.0, 0]))
        sl = T("females that survived", 26, GREEN).move_to([-4.3, 3.0, 0])
        self.play(*moves, FadeIn(sl), FadeIn(legc), run_time=1.6)

        bx = 3.1
        b1 = bar(0.2).move_to([bx, 1.3, 0])
        b2 = bar(0.5).move_to([bx, -0.7, 0])
        l1 = T("Before the war: about 1 in 5 had no tusks", 24, TEXT).next_to(b1, UP, buff=0.18)
        l2 = T("Survivors: about half had no tusks", 24, TEXT).next_to(b2, UP, buff=0.18)
        src = T("Gorongosa: survivors, not their young", 22, GREY).next_to(b2, DOWN, buff=0.5)
        self.at("The share of females")
        self.play(FadeIn(l1), GrowFromEdge(b1, LEFT), run_time=1.0)
        self.at("went up")
        self.play(FadeIn(l2), GrowFromEdge(b2, LEFT), FadeIn(src), run_time=1.0)

        mo = VGroup(T("tuskless survivors left more", 24, GREEN), T("of the next generation", 24, GREEN)).arrange(DOWN, buff=0.08).move_to([-4.3, -2.5, 0])
        self.at("Tuskless survivors left")
        self.play(FadeIn(mo, shift=UP * 0.1), run_time=0.7)
        lg = T("more common in later generations", 24, TEAL, weight=BOLD)
        lg.move_to([3.1, -3.25, 0])
        self.at("later generations")
        self.play(FadeIn(lg, shift=UP * 0.1), run_time=0.6)

        # individuals versus populations
        self.at("No single elephant")
        self.play(FadeOut(VGroup(surv, sl, legc, b1, b2, l1, l2, src, mo, lg)), run_time=0.6)
        one = animal(True, 2.0).move_to([-3.4, 0.6, 0])
        ring = Circle(radius=1.3, color=GOLD, stroke_width=3).move_to(one).shift(DOWN * 0.1)
        ih = T("one elephant", 32, TEXT, weight=BOLD).move_to([-3.4, 2.3, 0])
        isub = T("her tusks do not change", 28, GREY).move_to([-3.4, -1.3, 0])
        self.play(FadeIn(one, scale=0.7), Create(ring), FadeIn(ih), FadeIn(isub), run_time=1.0)

        ph = T("the population", 32, TEXT, weight=BOLD).move_to([3.4, 2.3, 0])
        pb1 = bar(0.2, 3.6, 0.5).move_to([3.4, 0.9, 0])
        pb2 = bar(0.5, 3.6, 0.5).move_to([3.4, -0.2, 0])
        pl1 = T("before", 22, GREY).next_to(pb1, UP, buff=0.1)
        pl2 = T("survivors", 22, GREY).next_to(pb2, UP, buff=0.1)
        psub = T("its makeup changed", 28, GOLD).move_to([3.4, -1.3, 0])
        self.at("The population changed")
        self.play(FadeIn(ph), FadeIn(pl1), FadeIn(pl2), GrowFromEdge(pb1, LEFT), GrowFromEdge(pb2, LEFT), FadeIn(psub),
                  run_time=1.2)

        i2 = T("Individuals do not evolve", 30, TEXT, weight=BOLD).move_to([-3.4, -2.6, 0])
        p2 = T("Populations do", 30, GOLD, weight=BOLD).move_to([3.4, -2.6, 0])
        self.at("Individuals do not")
        self.play(FadeIn(i2, shift=UP * 0.1), run_time=0.6)
        self.at("Populations do")
        self.play(FadeIn(p2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """the question answered, the chain, and strong versus weak pressure as a sketch."""

    def construct(self):
        q1 = T("Why do some individuals survive and reproduce", 34, TEXT)
        q2 = T("while others do not?", 34, TEXT)
        q = VGroup(q1, q2).arrange(DOWN, buff=0.15).move_to([0, 2.6, 0])
        self.at("Back to the question")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=1.0)

        c1 = chip("individuals differ", PURPLE, 28)
        c2 = chip("some survive more", GREEN, 28)
        c3 = chip("the population changes", GOLD, 28)
        chain = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.75).move_to([0, 0.2, 0])
        a1 = arr_between(c1, c2)
        a2 = arr_between(c2, c3)
        self.at("Because they differ")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.6)
        self.at("Those individuals leave")
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.15), run_time=0.8)
        self.at("become more common")
        self.play(GrowArrow(a2), FadeIn(c3, shift=UP * 0.15), run_time=0.8)

        # make room for the sketch
        grp = VGroup(chain, a1, a2)
        self.at("A strong pressure")
        self.play(FadeOut(q), grp.animate.scale(0.7).move_to([0, -3.0, 0]), run_time=0.9)

        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.15, 0.25], x_length=7.0, y_length=3.3,
                  axis_config={"include_ticks": False, "include_numbers": False, "stroke_color": GREY, "stroke_width": 3,
                               "tip_length": 0.18}).move_to([0, 0.35, 0])
        xl = T("time", 24, GREY).next_to(ax.x_axis, DOWN, buff=0.12)
        yl = T("share with the trait", 24, GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
        sk = T("a sketch, not data", 22, GREY).next_to(ax.x_axis, DOWN, buff=0.12).align_to(ax, RIGHT)
        k1, k2 = 1.2, 0.3
        f1 = lambda t: 1 / (1 + np.exp(-k1 * (t - 1.386 / k1)))
        f2 = lambda t: 1 / (1 + np.exp(-k2 * (t - 1.386 / k2)))
        c_strong = ax.plot(f1, x_range=[0, 10], color=RED, stroke_width=6)
        c_weak = ax.plot(f2, x_range=[0, 10], color=GREY, stroke_width=6)
        ls = T("strong pressure: a few decades", 24, RED).move_to(ax.c2p(6.0, 1.12))
        lw = T("weak pressure: slowly", 24, TEXT).move_to(ax.c2p(7.4, 0.3))
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sk), run_time=0.9)
        self.play(Create(c_strong), FadeIn(ls), run_time=1.6)
        self.at("A weak pressure")
        self.play(Create(c_weak), FadeIn(lw), run_time=1.6)

        self.at("Remember this rule")
        self.play(Indicate(grp, color=GOLD, scale_factor=1.12), run_time=1.5)
        self.finish()


def arr_between(a, b):
    return Arrow(a.get_right(), b.get_left(), buff=0.1, color=GREY, stroke_width=5, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.5)


class S07End(EndCard):
    LINE = "Individuals differ, some survive more, and the population changes."
