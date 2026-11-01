"""How signaling evolved: copy a gene, then rewire it  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the receptor and its gene, and every copy of it
  TEAL   = human kinase count (the human bar)
  ORANGE = baker's yeast kinase count (the yeast bar)
  PURPLE = downstream partners: core kinases, PI 3-kinase, Ras
  PINK   = the reading domain (the two-pronged SH2 reader of PI 3-kinase)
  YELLOW = a change: a mutation, an altered amino acid, a copy that has changed
  GREEN  = a tissue tag: where a gene is switched on (gut, nerve)
  GOLD   = a phosphate (the round "P" badge)
  RED    = lost or ruled out (the crossed-out pseudogene, the crossed-out invented pathways)
  GREY   = membrane, labels, ghosts, the parts not yet known

No molecular structures: genes and receptors are labelled chips and bars, amino acids are plain
labelled boxes in a row, the reader is a two-legged bracket, a phosphate is a "P" badge.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#E8A06A"
PURPLE = "#B58CD9"
PINK = "#F08BB4"
TEAL_BAR = TEAL


def bchip(text, color=BLUE, size=26, pad=0.2, **kw):
    c = chip(text, color, size=size, pad=pad, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ghost_chip(text, size=24):
    t = T(text, size, GREY)
    box = RoundedRectangle(corner_radius=0.14, width=t.width + 0.4, height=t.height + 0.32)
    return VGroup(DashedVMobject(box, num_dashes=max(18, int(box.width * 9))).set_color(GREY), t)


def strike(m, color=RED):
    return Line(m.get_corner(DL) + [-0.08, -0.04, 0], m.get_corner(UR) + [0.08, 0.04, 0], color=color, stroke_width=7)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(k=1.0):
    c = Circle(radius=0.18 * k, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 22 * k, BG, weight=BOLD).move_to(c))


def pop(m, s=1.3):
    return m.animate(rate_func=there_and_back).scale(s)


def glow(*mobs, s=1.1, color=TEXT):
    return [Indicate(m, color=color, scale_factor=s) for m in mobs]


class Film(SpokenScene):
    def end(self):
        """hold to the last word, clear the stage, then the tail."""
        rest = self.narration_s - 0.02 - self.elapsed()
        if rest > 0:
            self.wait(rest)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.38)
        self.finish()


# ---------------------------------------------------------------------------------------------
# the two bars (scenes 1 and 6 share them)
# ---------------------------------------------------------------------------------------------
BX = -6.0
KS = 0.02                      # 1 unit of bar per 50 kinases
HY, YY = 1.55, -0.3            # bar centres
BH = 1.0
X_YEAST = BX + 2.5             # the yeast bar ends here (roughly 125 kinases; the lesson says 120 to 130)
X_HUMAN = BX + 518 * KS


def lbar(width, y, color):
    r = Rectangle(width=width, height=BH, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    return r.move_to([BX + width / 2, y, 0])


def extra_box():
    w = X_HUMAN - X_YEAST
    r = Rectangle(width=w, height=BH).move_to([(X_YEAST + X_HUMAN) / 2, HY, 0])
    return DashedVMobject(r, num_dashes=60).set_color(GREY)


def left_label(text, y, color, size=28):
    t = T(text, size, color)
    return t.move_to([BX + t.width / 2, y, 0])


class S00Title(TitleCard):
    LESSON = "How Signaling Evolved"
    TITLE = "Copy a Gene, Then Rewire It"


# ---------------------------------------------------------------------------------------------
class S01Question(Film):
    def construct(self):
        hb, yb = lbar(518 * KS, HY, TEAL), lbar(2.5, YY, ORANGE)
        hl = left_label("human: 518 protein kinases", HY + 0.85, TEAL)
        yl = left_label("baker's yeast: roughly 120 to 130", YY + 0.85, ORANGE)
        self.at("a human has")
        self.play(GrowFromEdge(hb, LEFT), FadeIn(hl, shift=DOWN * 0.1), run_time=0.9)
        self.at("yeast has roughly")
        self.play(GrowFromEdge(yb, LEFT), FadeIn(yl, shift=DOWN * 0.1), run_time=0.7)
        guide = DashedLine([X_YEAST, YY + BH / 2, 0], [X_YEAST, HY - BH / 2, 0], color=GREY, stroke_width=3, dash_length=0.1)
        ex = extra_box()
        q = T("?", 44, TEXT, weight=BOLD).move_to(ex)
        exl = T("the extra parts", 26, GREY).move_to([2.4, HY + 0.85, 0])
        self.at("where did the")
        self.play(Create(guide), Create(ex), FadeIn(q), FadeIn(exl), run_time=0.9)
        self.play(pop(q, 1.4), run_time=0.6)

        ghosts = VGroup(*[ghost_chip("new pathway") for _ in range(3)]).arrange(RIGHT, buff=0.6).move_to([0, -2.4, 0])
        crosses = VGroup(*[strike(g) for g in ghosts])
        self.at("inventing one new")
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in ghosts], lag_ratio=0.3), run_time=0.9)
        self.at("after another")
        self.play(LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.3), run_time=0.8)

        rc = bchip("receptors at the top", BLUE, 26).move_to([-3.9, -1.8, 0])
        kc = bchip("kinases in the core", PURPLE, 26).move_to([-3.9, -2.95, 0])
        a1 = arr([-1.7, -1.8, 0], [3.9, -1.8, 0], BLUE, w=8, tip=0.3)
        a2 = arr([-1.7, -2.95, 0], [0.9, -2.95, 0], PURPLE, w=8, tip=0.3)
        self.at("receptors")
        self.play(FadeOut(ghosts), FadeOut(crosses), FadeIn(rc), run_time=0.5)
        self.at("multiplied more than")
        self.play(GrowArrow(a1), run_time=0.8)
        self.at("the core")
        self.play(FadeIn(kc), GrowArrow(a2), run_time=0.7)
        self.end()


# ---------------------------------------------------------------------------------------------
class S02Copy(Film):
    def construct(self):
        orig = bchip("receptor gene", BLUE, 34).move_to([0, 0.8, 0])
        self.play(FadeIn(orig, scale=0.9), run_time=0.5)
        self.at("duplicate a single")
        spare = orig.copy()
        self.add(spare)
        self.play(orig.animate.shift(LEFT * 2.9), spare.animate.shift(RIGHT * 2.9), run_time=0.9)
        cp = T("copied", 28, YELLOW).move_to([0, 0.8, 0])
        self.at("gene is copied")
        self.play(FadeIn(cp), run_time=0.3)
        l1 = T("keeps the old job", 28, GREY).next_to(orig, DOWN, buff=0.4)
        self.at("keeps doing the")
        self.play(FadeOut(cp), FadeIn(l1, shift=UP * 0.1), pop(orig, 1.06), run_time=0.7)
        l2 = T("spare: free to change", 28, YELLOW).next_to(spare, DOWN, buff=0.4)
        self.at("spare copy is")
        self.play(FadeIn(l2, shift=UP * 0.1), spare[1].animate.set_stroke(YELLOW), run_time=0.7)

        # a fly has one, a human four
        fly = bchip("EGF receptor", BLUE, 26)
        fl = T("fly: one", 30, TEXT, weight=BOLD)
        flyg = VGroup(fl, fly).arrange(DOWN, buff=0.35).move_to([-4.4, 0.6, 0])
        pos = [(1.9, 1.3), (4.6, 1.3), (1.9, -0.2), (4.6, -0.2)]
        hum = VGroup(*[bchip("EGF receptor", BLUE, 26).move_to([x, y, 0]) for x, y in pos])
        hl = T("human: four", 30, TEXT, weight=BOLD).move_to([3.25, 2.4, 0])
        self.at("a fly has")
        self.play(FadeOut(VGroup(orig, spare, l1, l2)), FadeIn(flyg, shift=UP * 0.1), run_time=0.7)
        self.at("a human has")
        self.play(FadeIn(hl), LaggedStart(*[FadeIn(h, scale=0.8) for h in hum], lag_ratio=0.2), run_time=1.0)
        route = DoubleArrow([-2.9, 0.6, 0], [0.2, 0.6, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        cmpl = T("compare two\nliving animals", 24, GREY, line_spacing=0.8).move_to([-1.35, 1.2, 0])
        self.play(GrowArrow(route), FadeIn(cmpl), run_time=0.6)
        dbl = T("two whole-genome doublings: x2, x2", 24, GREY).move_to([3.25, -1.3, 0])
        likely = T("the likely route", 26, GOLD).move_to([3.25, -1.9, 0])
        self.at("traces of two")
        self.play(FadeIn(dbl, shift=UP * 0.1), FadeIn(likely, shift=UP * 0.1), run_time=0.8)
        self.at("from one to")
        self.play(pop(fly, 1.08), LaggedStart(*[pop(h, 1.06) for h in hum], lag_ratio=0.15), run_time=0.9)
        self.end()


# ---------------------------------------------------------------------------------------------
def tagchips(cx, y=-0.75):
    g = bchip("gut", GREEN, 24, pad=0.14).move_to([cx - 0.85, y, 0])
    n = bchip("nerve", GREEN, 24, pad=0.14).move_to([cx + 0.95, y, 0])
    return g, n


class S03Fates(Film):
    def construct(self):
        orig = bchip("receptor gene", BLUE, 32).move_to([-3.2, 0.5, 0])
        spare = bchip("spare copy", BLUE, 32).move_to([3.2, 0.5, 0])
        self.play(FadeIn(orig), FadeIn(spare), run_time=0.5)
        head = T("three fates", 34, TEXT, weight=BOLD).move_to([0, 2.7, 0])
        self.at("three main fates")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        h1 = T("Fate 1: loss", 34, RED, weight=BOLD).move_to([0, 2.7, 0])
        self.at("the common one")
        self.play(FadeOut(head), FadeIn(h1), run_time=0.5)
        head = h1
        mut = T("mutation", 28, YELLOW).next_to(spare, UP, buff=0.35)
        self.at("disables the copy")
        self.play(FadeIn(mut, shift=DOWN * 0.1), spare[1].animate.set_stroke(GREY), spare[1].animate.set_fill(GREY, 0.08),
                  spare[2].animate.set_color(GREY), run_time=0.7)
        x = strike(spare)
        pl = T("pseudogene", 30, GREY).next_to(spare, DOWN, buff=0.4)
        self.at("decays into")
        self.play(Create(x), FadeIn(pl, shift=UP * 0.1), FadeOut(mut), run_time=0.8)
        self.wait(0.6)

        # case 2: clear every result of case 1 in the same beat that the new label comes in
        h2 = T("Fate 2: divide the job", 34, GREEN, weight=BOLD).move_to([0, 2.7, 0])
        self.at("second fate")
        self.play(FadeOut(spare), FadeOut(x), FadeOut(pl), FadeOut(head), FadeIn(h2),
                  orig.animate.move_to([0, 0.5, 0]), run_time=0.8)
        tg, tn = tagchips(0)
        self.at("worked in gut")
        self.play(FadeIn(tg, shift=UP * 0.1), run_time=0.4)
        self.at("and in nerve")
        self.play(FadeIn(tn, shift=UP * 0.1), run_time=0.4)
        grpA = VGroup(orig, tg, tn)
        grpB = grpA.copy()
        self.add(grpB)
        self.at("if one copy")
        self.play(grpA.animate.shift(LEFT * 3.2), grpB.animate.shift(RIGHT * 3.2), run_time=0.9)
        tgA, tnA = grpA[1], grpA[2]
        tgB, tnB = grpB[1], grpB[2]

        def lose(tag):
            return [tag[1].animate.set_stroke(GREY, opacity=0.5).set_fill(GREY, 0.05), tag[2].animate.set_color(GREY)]
        sA = strike(tgA)
        self.at("regulatory DNA for")
        self.play(*lose(tgA), Create(sA), run_time=0.6)
        sB = strike(tnB)
        self.at("loses it for nerve")
        self.play(*lose(tnB), Create(sB), run_time=0.6)
        both = T("the animal needs both", 30, TEXT).move_to([0, -2.2, 0])
        self.at("needs both")
        self.play(FadeIn(both, shift=UP * 0.1), pop(grpA[0], 1.08), pop(grpB[0], 1.08), run_time=0.8)
        self.end()


# ---------------------------------------------------------------------------------------------
YROW = -1.35
XS = [-3.4, -1.45, 0.5, 2.45]


def residue(x, text="", color=GREY):
    r = RoundedRectangle(corner_radius=0.1, width=1.6, height=1.0, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.15).move_to([x, YROW, 0])
    t = T(text, 38, color, weight=BOLD) if text else T(" ", 38, color)
    return VGroup(r, t.move_to(r))


def reader(shift=0.0):
    xl, xr, yb, yt = XS[0], XS[3], -0.72, 0.15
    br = VMobject(color=PINK, stroke_width=9)
    br.set_points_as_corners([[xl, yb, 0], [xl, yt, 0], [xr, yt, 0], [xr, yb, 0]])
    chp = bchip("PI 3-kinase", PURPLE, 28).move_to([(xl + xr) / 2, yt + 0.55, 0])
    g = VGroup(br, chp)
    g.br, g.chp = br, chp
    return g.shift(UP * shift)


class S04Site(Film):
    def construct(self):
        spare = bchip("spare copy", BLUE, 34).move_to([0, 0.6, 0])
        head = T("Fate 3: a new job", 34, YELLOW, weight=BOLD).move_to([0, 2.7, 0])
        self.play(FadeIn(spare), run_time=0.4)
        self.at("third fate")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)

        mem = RoundedRectangle(corner_radius=0.1, width=12.6, height=0.28, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([0, 2.7, 0])
        bar = RoundedRectangle(corner_radius=0.12, width=0.3, height=4.5, stroke_color=BLUE, stroke_width=3,
                               fill_color=BLUE, fill_opacity=0.4).move_to([-5.3, 0.95, 0])
        link = Line([-5.15, YROW, 0], [XS[0] - 0.8, YROW, 0], color=BLUE, stroke_width=6)
        rl = T("receptor copy", 26, BLUE).move_to([-3.2, 3.2, 0])
        row = [residue(XS[0], "Y"), residue(XS[1]), residue(XS[2]), residue(XS[3])]
        tl = T("tail", 24, GREY).move_to([-4.2, YROW + 0.75, 0])
        self.at("tail may change")
        self.play(FadeOut(spare), FadeOut(head), FadeIn(mem), GrowFromEdge(bar, UP), run_time=0.8)
        illus = T("an illustration", 24, GREY).move_to([4.9, YROW, 0])
        self.play(FadeIn(rl), Create(link), FadeIn(illus), LaggedStart(*[FadeIn(r, shift=LEFT * 0.15) for r in row], lag_ratio=0.2), run_time=0.9)
        self.at("set of tyrosines")
        self.play(*glow(row[0][0], row[0][1], s=1.12), run_time=0.6)

        br = Brace(VGroup(*row), DOWN, color=GREY, buff=0.1)
        fa = T("a few amino acids", 28, GREY).next_to(br, DOWN, buff=0.15)
        self.at("only a few")
        self.play(GrowFromCenter(br), FadeIn(fa), run_time=0.7)

        rd = reader(shift=1.2)
        self.at("domains of")
        self.play(FadeOut(br), FadeOut(fa), FadeIn(rd, shift=DOWN * 0.3), run_time=0.7)
        pb = pbadge().move_to([XS[0] + 0.62, YROW + 0.5, 0])
        pyl = T("pY", 26, PINK, weight=BOLD).move_to([XS[0], 0.2, 0])
        self.at("kinase read")
        self.play(FadeIn(pb, scale=0.5), FadeIn(pyl), Indicate(rd.br, color=TEXT, scale_factor=1.0), run_time=0.7)
        poss = [T(p, 24, GREY).move_to([x, YROW - 0.75, 0]) for p, x in zip(["+1", "+2", "+3"], XS[1:])]
        self.at("followed three")
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in poss], lag_ratio=0.35), run_time=0.9)
        ml = T("M", 28, PINK, weight=BOLD).move_to([XS[3], 0.2, 0])
        self.at("later by")
        self.play(FadeIn(ml), Indicate(poss[2], color=TEXT, scale_factor=1.3), run_time=0.6)

        # one blank box turns into M; only then does the reader come down
        newM = residue(XS[3], "M", YELLOW)
        self.at("point mutations")
        self.play(Transform(row[3], newM), FadeOut(poss[2]), run_time=0.7)
        self.play(*glow(row[3][0], row[3][1], s=1.15, color=YELLOW), run_time=0.5)
        self.at("make such")
        self.play(FadeOut(pyl), FadeOut(ml), rd.animate.shift(DOWN * 1.2), run_time=0.8)
        link2 = T("a new line", 28, PURPLE).next_to(rd.chp, RIGHT, buff=0.5)
        self.at("and with it")
        self.play(FadeIn(link2, shift=RIGHT * 0.1), *glow(rd.br, rd.chp, s=1.06), run_time=0.8)
        self.end()


# ---------------------------------------------------------------------------------------------
RX = [-4.8, -1.6, 1.6, 4.8]


class S05Network(Film):
    def construct(self):
        recs = VGroup(*[bchip("receptor", BLUE, 26).move_to([x, 2.5, 0]) for x in RX])
        self.at("carry the duplication")
        self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in recs], lag_ratio=0.2), run_time=1.0)
        k1 = VGroup(*[bchip("kinase", PURPLE, 24).move_to([x, 0.9, 0]) for x in RX])
        k2 = VGroup(*[bchip("kinase", PURPLE, 24).move_to([x, -0.6, 0]) for x in RX])
        wires = VGroup(*[arr(recs[i].get_bottom(), k1[i].get_top(), GREY) for i in range(4)],
                       *[arr(k1[i].get_bottom(), k2[i].get_top(), GREY) for i in range(4)])
        self.at("everything downstream")
        self.play(LaggedStart(*[FadeIn(k) for k in k1], lag_ratio=0.15), LaggedStart(*[FadeIn(k) for k in k2], lag_ratio=0.15),
                  FadeIn(wires), run_time=1.0)
        o1 = T("Outcome 1: four wires, kept apart", 30, GREY).move_to([0, -2.2, 0])
        self.at("stay apart")
        self.play(FadeIn(o1, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        # case 2: the wires and their label go in the same beat that the new label comes in
        o2 = T("Outcome 2: a shared core", 30, TEXT).move_to([0, -2.2, 0])
        self.at("in the other")
        self.play(FadeOut(k1), FadeOut(k2), FadeOut(wires), FadeOut(o1), FadeIn(o2), run_time=0.7)
        ras = bchip("Ras", PURPLE, 36).move_to([0, 0.7, 0])
        core = bchip("shared kinases", PURPLE, 26).move_to([0, -0.8, 0])
        to_ras = VGroup(*[arr(recs[i].get_bottom(), ras.get_top() + [(-0.5, 0, 0), (-0.2, 0, 0), (0.2, 0, 0), (0.5, 0, 0)][i], GREY, w=4, tip=0.16) for i in range(4)])
        down = arr(ras.get_bottom(), core.get_top(), GREY)
        self.at("sharing downstream parts")
        self.play(FadeIn(ras, scale=0.8), FadeIn(core, scale=0.8), LaggedStart(*[GrowArrow(a) for a in to_ras], lag_ratio=0.15),
                  GrowArrow(down), run_time=1.1)
        links = VGroup(*[DashedLine(recs[i].get_right(), recs[i + 1].get_left(), color=YELLOW, stroke_width=4, dash_length=0.1) for i in range(3)])
        self.at("and gain")
        self.play(Create(links), run_time=0.8)
        self.at("funnel into")
        self.play(pop(ras, 1.12), *[Indicate(a, color=TEXT, scale_factor=1.0) for a in to_ras], run_time=0.9)
        hub = T("a hub", 26, GOLD).next_to(ras, RIGHT, buff=0.4)
        self.at("hubs")
        self.play(FadeIn(hub, shift=LEFT * 0.1), run_time=0.4)
        ptr = T("the counts fit this", 28, GOLD).move_to([0, -3.05, 0])
        self.at("counts fit")
        self.play(FadeIn(ptr, shift=UP * 0.1), pop(o2, 1.04), run_time=0.7)
        self.end()


# ---------------------------------------------------------------------------------------------
class S06Rule(Film):
    def construct(self):
        hb, yb = lbar(518 * KS, HY, TEAL), lbar(2.5, YY, ORANGE)
        hl = left_label("human: 518 protein kinases", HY + 0.85, TEAL)
        yl = left_label("baker's yeast: roughly 120 to 130", YY + 0.85, ORANGE)
        guide = DashedLine([X_YEAST, YY + BH / 2, 0], [X_YEAST, HY - BH / 2, 0], color=GREY, stroke_width=3, dash_length=0.1)
        ex = extra_box()
        q = T("?", 44, TEXT, weight=BOLD).move_to(ex)
        exl = T("the extra parts", 26, GREY).move_to([2.4, HY + 0.85, 0])
        self.add(hb, yb, hl, yl, guide, ex, q, exl)
        self.at("the extra kinases")
        self.play(pop(q, 1.4), run_time=0.6)
        ghosts = VGroup(*[ghost_chip("new pathway") for _ in range(3)]).arrange(RIGHT, buff=0.6).move_to([0, -2.4, 0])
        crosses = VGroup(*[strike(g) for g in ghosts])
        self.at("a list of")
        self.play(LaggedStart(*[FadeIn(g) for g in ghosts], lag_ratio=0.2), run_time=0.6)
        self.play(LaggedStart(*[Create(c) for c in crosses], lag_ratio=0.2), run_time=0.6)

        # copies fill only part of the region: most toward the receptor end, little in the core, the rest still unknown
        w = 0.95
        rx = [1.6, 2.7, 3.8]
        tiles = VGroup(*[Rectangle(width=w, height=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.4)
                         .move_to([x, HY, 0]) for x in rx])
        core = Rectangle(width=w, height=0.7, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3).move_to([0.3, HY, 0])
        marks = VGroup(*[Square(side_length=0.2, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
                         .move_to(t.get_corner(UR) + [-0.2, -0.2, 0]) for t in tiles])
        copied = T("the record shows old pathways copied", 24, BLUE).move_to([2.2, HY + 0.85, 0])
        rl = T("mostly at the receptor end", 24, BLUE).move_to([3.3, 0.05, 0])
        cl = T("core", 24, PURPLE).move_to([0.3, 0.05, 0])
        ticks = VGroup(Line([0.3, HY - 0.4, 0], [0.3, 0.3, 0], color=PURPLE, stroke_width=3), Line([2.7, HY - 0.4, 0], [2.7, 0.3, 0], color=BLUE, stroke_width=3))
        self.at("old pathways copied")
        self.play(FadeOut(ghosts), FadeOut(crosses), FadeOut(exl), FadeIn(copied), q.animate.move_to([-1.7, HY, 0]),
                  LaggedStart(*[FadeIn(t, scale=0.8) for t in tiles], lag_ratio=0.15), FadeIn(core, scale=0.8), run_time=1.3)
        self.play(FadeIn(rl), FadeIn(cl), FadeIn(ticks), run_time=0.5)
        self.at("and the copies changed")
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in marks], lag_ratio=0.15), run_time=0.8)
        few = bchip("a few amino acids", YELLOW, 26).move_to([2.7, -0.9, 0])
        self.at("a few amino")
        self.play(FadeIn(few, shift=UP * 0.1), *[pop(m, 1.9) for m in marks], run_time=0.8)
        self.at("get copied")
        self.play(*[pop(t, 1.06) for t in tiles], run_time=0.7)
        self.at("get rewired")
        self.play(*glow(*marks, s=1.8, color=YELLOW), run_time=0.8)
        self.end()


class S07End(EndCard):
    LINE = "Old pathways get copied, and the copies get rewired."
