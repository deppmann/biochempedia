"""Natural selection and speciation: selection sorts differences that already exist  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = a beak (the trait; its height is "beak depth"; deeper beak = taller bar)
  GREY   = bodies of birds, outlines, islands, neutral labels
  ORANGE = the drought and the large, hard seeds
  GREEN  = lived / survived (survivors, success)
  RED    = died / crossed out / "can no longer interbreed"
  PURPLE = inheritance (genes passing from parent to young) and the adaptation label
  MINT   = variation and mutation (new versions of genes)
  TEAL   = offspring (young), fitness, and the river (geographic isolation barrier)
  GOLD   = the question and the take-home rule
Bird tokens are schematic: a body block and a beak bar. Beak heights are an illustration, never
measurements. The histograms are a labelled sketch in relative units.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
MINT = "#6FE3B0"
TEAL2 = "#3FB8C0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bird(depth=0.25, s=1.0, body=GREY, beak=BLUE):
    """A labelled-block finch: a body block with a beak bar whose HEIGHT is the beak depth."""
    b = RoundedRectangle(corner_radius=0.2, width=0.9, height=0.62, stroke_color=body, stroke_width=3,
                         fill_color=body, fill_opacity=0.25)
    bk = Rectangle(width=0.3, height=depth, stroke_width=0, fill_color=beak, fill_opacity=0.95)
    bk.next_to(b, RIGHT, buff=0)
    eye = Dot(b.get_center() + np.array([0.18, 0.12, 0]), radius=0.05, color=TEXT)
    g = VGroup(b, bk, eye)
    g.body, g.beak, g.depth = b, bk, depth
    return g.scale(s)


def cross(mob, w=0.3):
    c = mob.get_center()
    return VGroup(Line(c + [-w, -w, 0], c + [w, w, 0], color=RED, stroke_width=7),
                  Line(c + [-w, w, 0], c + [w, -w, 0], color=RED, stroke_width=7))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def lines(*txt, size=26, color=TEXT, buff=0.12, weight=NORMAL):
    return VGroup(*[T(t, size, color, weight=weight) for t in txt]).arrange(DOWN, buff=buff)


def cchip(txt, color, size=26):
    return chip(txt, color, size=size)


DEPTHS = [0.10, 0.14, 0.18, 0.22, 0.12, 0.16, 0.20, 0.26, 0.15, 0.19,
          0.23, 0.28, 0.13, 0.17, 0.21, 0.25, 0.30, 0.18, 0.24, 0.32]
SURV = [10, 11, 15, 16, 18, 19]          # 6 of 20 lived ("most died"); they lean deeper


class S00Title(TitleCard):
    LESSON = "Natural selection and new species"
    TITLE = "Selection Sorts Differences That Already Exist"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """a drought, most finches die, the ones left have deeper beaks: did it change the birds or which were left?"""

    def construct(self):
        cxi = -2.3
        island = RoundedRectangle(corner_radius=0.5, width=7.4, height=4.7, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.08).move_to([cxi, -0.2, 0])
        head = T("Daphne Major, an island in the Galápagos", 30, TEXT).to_edge(UP, buff=0.45)
        nt = T("birds are tokens; beak heights are an illustration", 22, GREY).move_to([cxi, -3.2, 0])
        birds = []
        for i, d in enumerate(DEPTHS):
            b = bird(d)
            b.move_to([cxi + (i % 5 - 2) * 1.4, 1.2 - (i // 5) * 1.05, 0])
            b.idx = i
            birds.append(b)

        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(island), FadeIn(nt),
                  LaggedStart(*[FadeIn(b, scale=0.7) for b in birds], lag_ratio=0.04), run_time=1.4)

        drought = cchip("drought, 1977", ORANGE, 30).move_to([4.2, 2.1, 0])
        self.at("severe drought")
        self.play(FadeIn(drought, shift=LEFT * 0.2), island.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.1), run_time=0.7)

        dead = [b for b in birds if b.idx not in SURV]
        crosses = [cross(b) for b in dead]
        died = lines("most died", size=34, color=RED, weight=BOLD).move_to([4.2, 0.9, 0])
        self.at("Most of its")
        self.play(LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.05), FadeIn(died), run_time=1.4)
        self.play(FadeOut(VGroup(*dead, *crosses), scale=0.6), run_time=0.8)

        surv = [b for b in birds if b.idx in SURV]
        grid = [[-4.9 + (k % 3) * 1.8, 0.7 - (k // 3) * 1.4, 0] for k in range(len(surv))]
        left = lines("the birds left:", "deeper beaks,", "on average", size=28, color=GREEN).move_to([4.2, -0.6, 0])
        self.at("The birds left")
        self.play(*[b.animate.move_to(grid[k]) for k, b in enumerate(surv)], FadeIn(left, shift=LEFT * 0.2),
                  run_time=1.2)
        self.play(*[Indicate(b.beak, color=BLUE, scale_factor=1.4) for b in surv], run_time=0.9)

        tipb = surv[2]                      # a survivor at the end of the top row
        mk = DoubleArrow(tipb.beak.get_corner(UR) + RIGHT * 0.2, tipb.beak.get_corner(DR) + RIGHT * 0.2,
                         color=TEXT, stroke_width=3, buff=0, tip_length=0.12)
        mkt = T("beak depth", 22, TEXT).next_to(mk, RIGHT, buff=0.1)
        meas = T("measured before the drought", 26, TEXT).move_to([cxi, -2.0, 0])
        self.at("Researchers had measured")
        self.play(FadeIn(mk), FadeIn(mkt), FadeIn(meas, shift=UP * 0.1), run_time=0.7)

        q1 = cchip("changed\nthe birds?", GOLD, 30)
        q2 = cchip("changed which\nwere left?", GOLD, 30)
        qg = VGroup(q1, q2).arrange(DOWN, buff=0.5).move_to([4.2, 0.0, 0])
        self.at("So did the drought")
        self.play(FadeOut(VGroup(drought, died, left)), run_time=0.6)
        self.at("change the birds")
        self.play(FadeIn(q1, shift=LEFT * 0.2), run_time=0.5)
        self.at("which were left")
        self.play(FadeIn(q2, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Three(SpokenScene):
    """three conditions drawn as three small pictures, then mutation as a changed block."""

    def construct(self):
        def label(num, name, color):
            return VGroup(T(num, 34, color, weight=BOLD), T(name, 32, color)).arrange(RIGHT, buff=0.25)

        ys = [2.2, 0.7, -0.7]
        # row 1: variation
        l1 = label("1", "Variation", MINT).move_to([-4.2, ys[0], 0])
        l1.align_to([-6.2, 0, 0], LEFT)
        ds = [0.12, 0.26, 0.18, 0.34, 0.2]
        r1 = VGroup(*[bird(d, 1.0) for d in ds]).arrange(RIGHT, buff=0.45).move_to([2.6, ys[0], 0])
        t1 = T("differences among individuals", 24, GREY).next_to(r1, DOWN, buff=0.22)
        # row 2: inheritance
        l2 = label("2", "Inheritance", PURPLE).move_to([-4.2, ys[1], 0])
        l2.align_to([-6.2, 0, 0], LEFT)
        par = bird(0.34, 0.95).move_to([-0.2, ys[1], 0])
        gen = arr([0.9, ys[1], 0], [2.7, ys[1], 0], PURPLE)
        gtxt = T("genes", 24, PURPLE).next_to(gen, UP, buff=0.05)
        young = bird(0.34, 0.6, body=TEAL2).move_to([3.7, ys[1], 0])
        t2 = T("parent to young", 24, GREY).move_to([5.4, ys[1] - 0.0, 0])
        t2.set_opacity(0)
        # row 3: unequal success
        l3 = label("3", "Unequal success", GREEN).move_to([-4.2, ys[2], 0])
        l3.align_to([-6.2, 0, 0], LEFT)
        pa = bird(0.34, 0.9).move_to([0.2, ys[2], 0])
        ya = VGroup(*[bird(0.34, 0.5, body=TEAL2) for _ in range(3)]).arrange(RIGHT, buff=0.18).move_to([2.0, ys[2], 0])
        pb = bird(0.12, 0.9).move_to([3.9, ys[2], 0])
        yb = VGroup(bird(0.12, 0.5, body=TEAL2)).move_to([5.3, ys[2], 0])
        t3 = T("offspring", 22, TEAL2).next_to(VGroup(ya, yb), DOWN, buff=0.14)
        t3.move_to([3.65, ys[2] - 0.62, 0])

        hd = T("Natural selection needs three things at once", 32, TEXT).to_edge(UP, buff=0.4)
        self.at("Natural selection needs")
        self.play(FadeIn(hd, shift=DOWN * 0.1), run_time=0.8)
        self.at("First variation")
        self.play(FadeIn(l1, shift=RIGHT * 0.2), LaggedStart(*[FadeIn(b, scale=0.7) for b in r1], lag_ratio=0.12), run_time=1.0)
        self.at("Variation means")
        self.play(FadeIn(t1), run_time=0.5)
        self.at("Second inheritance")
        self.play(FadeIn(l2, shift=RIGHT * 0.2), FadeIn(par), run_time=0.6)
        self.at("carried in genes")
        self.play(GrowArrow(gen), FadeIn(gtxt), run_time=0.5)
        self.play(FadeIn(young, shift=LEFT * 0.2), run_time=0.5)
        self.at("Third unequal success")
        self.play(FadeIn(l3, shift=RIGHT * 0.2), FadeIn(pa), FadeIn(pb), run_time=0.6)
        self.at("how many offspring")
        self.play(LaggedStart(*[FadeIn(y, scale=0.6) for y in ya], lag_ratio=0.2), FadeIn(yb), FadeIn(t3), run_time=1.2)

        # mutation: a row of DNA blocks where one block changes
        dna_lbl = T("DNA", 28, GREY).move_to([-4.6, -2.15, 0])
        blocks = VGroup(*[Square(0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
                          for _ in range(7)]).arrange(RIGHT, buff=0.08).move_to([-1.4, -2.15, 0])
        self.at("A mutation")
        self.play(FadeIn(dna_lbl), FadeIn(blocks), run_time=0.6)
        newb = blocks[3].copy().set_stroke(MINT).set_fill(MINT, 0.6)
        mlab = T("mutation: a change in DNA", 26, MINT).move_to([3.5, -1.95, 0])
        self.play(Transform(blocks[3], newb), FadeIn(mlab), run_time=0.6)
        self.at("new versions of genes")
        nv = T("new version of a gene", 24, MINT).move_to([3.5, -2.4, 0])
        self.play(FadeIn(nv), Indicate(blocks[3], color=MINT, scale_factor=1.3), run_time=0.7)

        rule = T("Selection does not make variation. It sorts the variation that is there.", 28, GOLD, weight=BOLD)
        fit(rule, max_w=12.0)
        rule.move_to([0, -3.3, 0])
        self.at("Selection does not make")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Fitness(SpokenScene):
    """fitness and adaptation as two definitions, then a deep beak cracking a large, hard seed."""

    def construct(self):
        # --- fitness ------------------------------------------------------------------------
        fh = cchip("fitness", TEAL2, 40).move_to([-4.6, 2.7, 0])
        par = bird(0.3, 1.7).move_to([-4.2, 1.1, 0])
        young = VGroup(*[bird(0.3, 1.0, body=TEAL2) for _ in range(3)]).arrange(RIGHT, buff=0.4).move_to([2.2, 1.1, 0])
        ar = arr([-2.3, 1.1, 0], [-0.1, 1.1, 0], TEAL2)
        ft = lines("offspring that survive to reproduce", size=30, color=TEAL2).move_to([2.2, 0.0, 0])
        self.at("Fitness is")
        self.play(FadeIn(fh, shift=DOWN * 0.1), FadeIn(par), run_time=0.7)
        self.at("how many offspring")
        self.play(GrowArrow(ar), LaggedStart(*[FadeIn(y, scale=0.6) for y in young], lag_ratio=0.25), FadeIn(ft), run_time=1.5)

        # --- adaptation ---------------------------------------------------------------------
        ah = cchip("adaptation", PURPLE, 40).move_to([-4.2, -1.5, 0])
        at = lines("an inherited trait that helps an organism", "survive and reproduce in its present environment",
                   size=28, color=PURPLE)
        at.next_to(ah, DOWN, buff=0.45).align_to([-6.2, 0, 0], LEFT)
        self.at("An adaptation")
        self.play(FadeIn(ah, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(at), run_time=0.8)

        # --- the finch and the seed ---------------------------------------------------------
        self.at("On Daphne Major")
        self.play(FadeOut(VGroup(fh, par, young, ar, ft, ah, at)), run_time=0.6)
        deep = bird(0.34, 2.4).move_to([-3.9, 0.5, 0])
        seed = RoundedRectangle(corner_radius=0.35, width=1.8, height=1.8, stroke_color=ORANGE, stroke_width=4,
                                fill_color=ORANGE, fill_opacity=0.4).move_to([0.4, 0.5, 0])
        sl = lines("large, hard seed", size=28, color=ORANGE).next_to(seed, DOWN, buff=0.4)
        bl = T("deep beak", 30, BLUE).next_to(deep, UP, buff=0.4)
        self.play(FadeIn(deep, shift=RIGHT * 0.3), FadeIn(seed, shift=LEFT * 0.3), FadeIn(sl), run_time=0.8)
        self.at("a deep beak was")
        tag = cchip("adaptation", PURPLE, 32).move_to([4.6, 2.5, 0])
        self.play(FadeIn(bl), Indicate(deep.beak, color=BLUE, scale_factor=1.5), FadeIn(tag, shift=LEFT * 0.2), run_time=0.9)

        best = lines("Large birds,", "especially males with", "large beaks,", "survived best", size=28, color=GREEN).move_to([4.6, 0.3, 0])
        self.at("Large birds")
        self.play(FadeIn(best, shift=LEFT * 0.2), run_time=0.8)

        self.at("They could crack")
        self.play(deep.animate.shift(RIGHT * 2.0), bl.animate.shift(RIGHT * 2.0), run_time=0.8)
        self.play(seed.animate.scale([0.5, 1, 1]).shift(LEFT * 0.4), run_time=0.3)
        right_half = seed.copy().shift(RIGHT * 1.0)
        ok = T("cracked", 32, GREEN, weight=BOLD).next_to(seed, UP, buff=0.55).shift(RIGHT * 0.5)
        self.play(FadeIn(right_half), FadeIn(ok), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Change(SpokenScene):
    """a labelled sketch histogram: before, who lived, then the next generation shifted deeper."""

    def construct(self):
        n = 8
        i = np.arange(n)
        before = 24.0 * np.exp(-((i - 3.0) ** 2) / (2 * 1.5 ** 2))
        p = 0.12 + 0.76 * i / (n - 1)            # chance of living rises with beak depth (sketch)
        lived = before * p
        died = before - lived
        nxt = np.convolve(lived, [0.2, 0.6, 0.2], mode="same")
        nxt = nxt * before.sum() / nxt.sum()
        k = 3.1 / before.max()
        x0, bw, ybase = -6.0, 0.8, -1.7
        cx = lambda j: x0 + (j + 0.5) * bw

        def bars(h, color, op=0.85, base=None):
            out = VGroup()
            for j in range(n):
                hh = max(h[j] * k, 0.001)
                r = Rectangle(width=bw - 0.06, height=hh, stroke_width=0, fill_color=color, fill_opacity=op)
                r.move_to([cx(j), (ybase if base is None else base[j]) + hh / 2, 0])
                out.add(r)
            return out

        axis = Line([x0 - 0.1, ybase, 0], [x0 + n * bw + 0.1, ybase, 0], color=GREY, stroke_width=3)
        xl = T("beak depth (relative units)", 24, GREY).next_to(axis, DOWN, buff=0.15)
        sh = T("shallower", 22, GREY).move_to([x0 + 0.5, ybase - 0.75, 0])
        de = T("deeper", 22, GREY).move_to([x0 + n * bw - 0.4, ybase - 0.75, 0])
        yl = T("number of birds", 22, GREY).rotate(PI / 2).move_to([x0 - 0.55, ybase + 1.6, 0])
        sk = T("a sketch in relative units, not the measurements", 22, GREY).to_edge(UP, buff=0.4).shift(LEFT * 2.4)

        b_before = bars(before, GREY, 0.8)
        cap1 = T("before the drought", 28, GREY).move_to([-3.2, 1.75, 0])
        self.play(FadeIn(sk), FadeIn(axis), FadeIn(xl), FadeIn(sh), FadeIn(de), FadeIn(yl),
                  LaggedStart(*[GrowFromEdge(b, DOWN) for b in b_before], lag_ratio=0.05), FadeIn(cap1), run_time=0.9)

        # one bird: no beak grew
        one = bird(0.3, 1.8).move_to([3.7, 1.0, 0])
        ghost_bk = DashedVMobject(Rectangle(width=0.54, height=1.0, stroke_color=RED, stroke_width=3, fill_opacity=0))
        ghost_bk.next_to(one.body, RIGHT, buff=0).align_to(one.beak, LEFT)
        grew = cross(ghost_bk, 0.35)
        gt = lines("this bird's beak", "did not grow", size=28, color=TEXT).move_to([4.4, -0.7, 0])
        self.at("beak grew")
        self.play(FadeIn(one), run_time=0.4)
        self.play(FadeIn(ghost_bk), Create(grew), FadeIn(gt), run_time=0.8)

        # lived / died
        b_lived = bars(lived, GREEN, 0.9)
        b_died = bars(died, RED, 0.8, base=[ybase + h * k for h in lived])
        leg = VGroup(VGroup(Square(0.3, stroke_width=0, fill_color=GREEN, fill_opacity=0.9), T("lived", 28, GREEN)).arrange(RIGHT, buff=0.2),
                     VGroup(Square(0.3, stroke_width=0, fill_color=RED, fill_opacity=0.8), T("died", 28, RED)).arrange(RIGHT, buff=0.2)
                     ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.4, 1.3, 0])
        self.at("birds that died")
        self.play(FadeOut(VGroup(one, ghost_bk, grew, gt)), ReplacementTransform(b_before, VGroup(b_lived, b_died)),
                  FadeOut(cap1), run_time=1.0)
        self.play(FadeIn(leg), run_time=0.5)
        cap2 = lines("on average, the", "two groups differ", size=26, color=TEXT).move_to([4.4, -0.2, 0])
        self.play(FadeIn(cap2), run_time=0.5)

        # next generation, shifted deeper
        b_next = bars(nxt, PURPLE, 0.85)
        ghost = bars(before, GREY, 0.0)
        for g in ghost:
            g.set_stroke(GREY, 2, opacity=0.7)
        mean_b = (i * before).sum() / before.sum()
        mean_n = (i * nxt).sum() / nxt.sum()
        mb = DashedLine([cx(mean_b), ybase, 0], [cx(mean_b), ybase + 3.3, 0], color=GREY, stroke_width=3)
        mn = DashedLine([cx(mean_n), ybase, 0], [cx(mean_n), ybase + 3.3, 0], color=PURPLE, stroke_width=3)
        ml_b = T("mean before", 22, GREY).next_to(mb, UP, buff=0.05).shift(LEFT * 1.0)
        ml_n = T("mean, next generation", 22, PURPLE).next_to(mn, UP, buff=0.05).shift(RIGHT * 1.4)
        inh = lines("beak size is", "strongly inherited", size=28, color=PURPLE, weight=BOLD).move_to([4.4, 0.6, 0])
        self.at("strongly inherited")
        self.play(FadeOut(VGroup(leg, cap2)), FadeIn(inh, shift=LEFT * 0.2), run_time=0.5)
        self.play(ReplacementTransform(VGroup(b_lived, b_died), b_next), FadeIn(ghost), run_time=1.3)
        self.play(Create(mb), Create(mn), FadeIn(ml_b), FadeIn(ml_n), run_time=0.9)
        nxt_cap = lines("next generation:", "deeper beaks", size=28, color=PURPLE).move_to([4.4, -0.7, 0])
        self.play(FadeIn(nxt_cap), run_time=0.5)

        last = cchip("selection can make a population better suited, but not perfectly", GOLD, 24)
        fit(last, max_w=12.0)
        last.move_to([0, -3.3, 0])
        self.at("Over many generations")
        self.play(FadeIn(last, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Species(SpokenScene):
    """one species, two groups that can no longer interbreed; a river splits groups that change in different ways."""

    def construct(self):
        BS = 1.15

        def gbox(cx, w=4.7):
            return RoundedRectangle(corner_radius=0.3, width=w, height=3.3, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.06).move_to([cx, 0.2, 0])

        def slot(cx, k):                      # 4 birds per group, 2 x 2
            return [cx + (k % 2 - 0.5) * 2.0, 0.85 - (k // 2) * 1.3, 0]

        qh = T("one species, or two?", 36, GOLD, weight=BOLD).to_edge(UP, buff=0.4)
        box = RoundedRectangle(corner_radius=0.3, width=11.4, height=3.3, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.06).move_to([0, 0.2, 0])
        dl = [0.18, 0.26, 0.2, 0.3, 0.14, 0.24, 0.22, 0.28]
        pos = [[-4.2 + (k % 4) * 2.8, 0.85 - (k // 4) * 1.3, 0] for k in range(8)]
        birds = [bird(d, BS).move_to(pos[k]) for k, d in enumerate(dl)]
        one = T("one species", 30, GREY).next_to(box, UP, buff=0.12)
        self.at("How can one species")
        self.play(FadeIn(qh, shift=DOWN * 0.1), FadeIn(box), FadeIn(one),
                  LaggedStart(*[FadeIn(b, scale=0.7) for b in birds], lag_ratio=0.05), run_time=1.5)

        # species definition: two birds interbreed, fertile young
        a = bird(0.26, 1.4).move_to([-3.4, 0.9, 0])
        b2 = bird(0.18, 1.4).move_to([3.0, 0.9, 0])
        link = DoubleArrow([-1.7, 0.9, 0], [1.4, 0.9, 0], color=PURPLE, stroke_width=6, buff=0)
        lt = T("interbreed", 30, PURPLE).next_to(link, UP, buff=0.1)
        fy = bird(0.22, 1.0, body=TEAL2).move_to([-0.3, -0.6, 0])
        fl = T("fertile young", 30, TEAL2).next_to(fy, RIGHT, buff=0.5)
        down = arr([-0.3, 0.7, 0], [-0.3, -0.1, 0], TEAL2, 5, 0.2)
        self.at("interbreed and produce")
        self.play(FadeOut(VGroup(*birds)), FadeIn(a), FadeIn(b2), run_time=0.5)
        self.play(GrowFromCenter(link), FadeIn(lt), run_time=0.6)
        self.at("fertile offspring")
        self.play(GrowArrow(down), FadeIn(fy, scale=0.5), FadeIn(fl), run_time=0.7)

        # speciation: the group splits
        bL, bR = gbox(-3.7), gbox(3.7)
        spec = cchip("speciation: one species splits into groups", GOLD, 30).to_edge(DOWN, buff=0.45)
        self.at("Speciation is")
        self.play(FadeOut(VGroup(a, b2, link, lt, fy, fl, down, qh)), FadeIn(VGroup(*birds)),
                  FadeIn(spec, shift=UP * 0.1), run_time=0.6)
        moves = [birds[k].animate.move_to(slot(-3.7, k)) for k in range(4)] + \
                [birds[4 + k].animate.move_to(slot(3.7, k)) for k in range(4)]
        self.at("splits into groups")
        self.play(ReplacementTransform(box, VGroup(bL, bR)), FadeOut(one), *moves, run_time=1.2)
        sideL = T("group A", 28, GREY).next_to(bL, UP, buff=0.12)
        sideR = T("group B", 28, GREY).next_to(bR, UP, buff=0.12)
        x_arrow = DoubleArrow([-0.8, 0.2, 0], [0.8, 0.2, 0], color=RED, stroke_width=5, buff=0)
        x_c = cross(x_arrow, 0.3)
        noint = lines("no longer", "interbreed", size=24, color=RED).move_to([0, -0.6, 0])
        self.at("no longer do that")
        self.play(FadeIn(sideL), FadeIn(sideR), GrowFromCenter(x_arrow), Create(x_c), FadeIn(noint), run_time=0.9)

        # geographic isolation: a river in the gap
        river = Rectangle(width=0.9, height=3.9, stroke_color=TEAL2, stroke_width=3, fill_color=TEAL2,
                          fill_opacity=0.35).move_to([0, 0.2, 0])
        rl = T("river", 26, TEAL2).move_to([0, -2.1, 0])
        geo = cchip("geographic isolation: a barrier between groups", TEAL2, 30).to_edge(DOWN, buff=0.45)
        self.at("geographic isolation")
        self.play(FadeOut(VGroup(x_arrow, x_c, noint)), ReplacementTransform(spec, geo), run_time=0.6)
        self.at("such as a river")
        self.play(FadeIn(river, scale=0.9), FadeIn(rl), run_time=0.7)

        # different mutations, different traits
        sqL = [Square(0.3, stroke_color=MINT, stroke_width=3, fill_color=MINT, fill_opacity=0.6).move_to([-3.7 + dx, 2.0, 0]) for dx in (-0.4, 0.0, 0.4)]
        sqR = [Square(0.3, stroke_color=MINT, stroke_width=3, fill_color=MINT, fill_opacity=0.6).move_to([3.7 + dx, 2.0, 0]) for dx in (-0.2, 0.2)]
        lab_diff = T("different mutations on each side", 26, MINT).move_to([0, 2.75, 0])
        self.at("different mutations")
        self.play(FadeOut(VGroup(geo, sideL, sideR)), FadeIn(lab_diff), *[FadeIn(q, scale=0.5) for q in sqL + sqR], run_time=0.9)
        deeper = [birds[k].beak.animate.stretch_to_fit_height(0.5) for k in range(4)]
        shallow = [birds[4 + k].beak.animate.stretch_to_fit_height(0.1) for k in range(4)]
        tl = T("for example: deeper beaks favoured", 24, BLUE).move_to([-3.7, -1.85, 0])
        tr = T("for example: shallower beaks favoured", 24, BLUE).move_to([3.7, -1.85, 0])
        self.at("different traits")
        self.play(*deeper, *shallow, FadeIn(tl), FadeIn(tr), run_time=1.2)

        sep = T("Separation alone is not speciation", 32, GOLD, weight=BOLD).to_edge(DOWN, buff=0.4)
        q = T("?", 64, GOLD, weight=BOLD).move_to([0, 0.2, 0])
        self.at("Separation alone")
        self.play(FadeOut(VGroup(lab_diff, *sqL, *sqR, rl, river)), FadeIn(q), FadeIn(sep, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """the question, the three-step answer, the split, the rule."""

    def construct(self):
        q = lines("How do traits become more common in a population,", "and how can one species become two?",
                  size=30, color=GOLD, weight=BOLD, buff=0.1)
        fit(q, max_w=12.4)
        q.move_to([0, 3.0, 0])
        self.at("Back to the question")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=1.0)

        bd = bird(0.3, 1.3).move_to([-5.3, 1.7, 0])
        gh = DashedVMobject(Rectangle(width=0.4, height=0.8, stroke_color=RED, stroke_width=3, fill_opacity=0))
        gh.next_to(bd.body, RIGHT, buff=0).align_to(bd.beak, LEFT)
        gx = cross(gh, 0.3)
        nogrow = T("no beak was reshaped", 26, RED).next_to(bd, RIGHT, buff=0.9).shift(RIGHT * 0.1)
        self.at("did not reshape")
        self.play(FadeIn(bd, scale=0.8), FadeIn(gh), Create(gx), FadeIn(nogrow), run_time=0.9)

        c1 = cchip("some birds lived to breed", GREEN, 26).move_to([-3.2, 0.4, 0])
        c2 = cchip("young inherited deeper beaks", PURPLE, 26).move_to([-3.2, -0.9, 0])
        for c in (c1, c2):
            c.set_x(-3.4)
        a1 = arr(c1.get_bottom(), c2.get_top(), GREY, 4, 0.18)
        self.at("which")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.7)
        self.at("young inherited")
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.2), run_time=0.7)

        # species split, stacked on the right
        def grp(cy, d):
            box = RoundedRectangle(corner_radius=0.3, width=4.3, height=1.5, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.06).move_to([4.0, cy, 0])
            bs = VGroup(*[bird(d, 0.85) for _ in range(3)]).arrange(RIGHT, buff=0.35).move_to(box)
            return VGroup(box, bs)

        gA = grp(0.9, 0.15)
        gB = grp(-1.7, 0.15)
        self.at("One species can become two")
        self.play(FadeIn(gA), FadeIn(gB), run_time=0.8)
        diff = T("change in different ways", 26, MINT).move_to([4.0, 1.95, 0])
        self.play(*[b.beak.animate.stretch_to_fit_height(0.45) for b in gA[1]],
                  *[b.beak.animate.stretch_to_fit_height(0.07) for b in gB[1]], FadeIn(diff), run_time=1.4)
        xa = DoubleArrow([4.0, 0.0, 0], [4.0, -0.8, 0], color=RED, stroke_width=5, buff=0)
        xc = cross(xa, 0.25)
        nl = T("no longer interbreed", 24, RED).move_to([4.0, -0.4, 0]).shift(RIGHT * 0.0)
        xa.shift(LEFT * 2.2)
        xc.shift(LEFT * 2.2)
        nl.shift(RIGHT * 0.2)
        self.at("no longer interbreed")
        self.play(GrowFromCenter(xa), Create(xc), FadeIn(nl), run_time=0.8)

        rule = T("Selection sorts the differences that already exist.", 32, GOLD, weight=BOLD)
        fit(rule, max_w=12.2)
        rule.move_to([0, -3.2, 0])
        self.at("Selection sorts")
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Selection sorts the differences that already exist."
