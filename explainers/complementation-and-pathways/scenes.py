"""Complementation and pathways: one phenotype can hide many genes  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  MAROON = pigment / the red (wild-type) eye
  WHITE  = a pale (white) eye, no pigment
  BLUE   = gene A, and complementation group one
  YELLOW = gene B, and complementation group two
  PURPLE = gene C, the group of mutant four
  RED    = broken / mutant (cross over a gene or station, mutant result)
  GREEN  = working / wild-type result, a cross whose offspring are wild type
  TEXT   = a working station on the assembly line
  GREY   = chromosomes, frames, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
MAROON = "#B5304A"
PALE = "#F2F2F2"
GENE = {"A": BLUE, "B": YELLOW, "C": PURPLE}


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def eye(kind="white", r=0.5):
    fill = MAROON if kind == "red" else PALE
    c = Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=fill, fill_opacity=1)
    p = Circle(radius=r * 0.34, stroke_width=0, fill_color=BG, fill_opacity=1)
    return VGroup(c, p)


def eye_to(e, kind):
    return [e[0].animate.set_fill(MAROON if kind == "red" else PALE, 1)]


def xmark(w, h, color=RED, sw=5):
    return VGroup(Line([-w, h, 0], [w, -h, 0], color=color, stroke_width=sw),
                  Line([-w, -h, 0], [w, h, 0], color=color, stroke_width=sw))


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Complementation and gene function"
    TITLE = "One Phenotype Can Hide Many Genes"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        y = 1.9
        e1 = eye("white", 0.62).move_to([-4.0, y, 0])
        e2 = eye("white", 0.62).move_to([-1.2, y, 0])
        times = T("×", 48, GREY).move_to([-2.6, y, 0])
        l1 = T("white-eyed line", 24, GREY).next_to(e1, DOWN, buff=0.2)
        l2 = T("white-eyed line", 24, GREY).next_to(e2, DOWN, buff=0.2)
        self.play(FadeIn(e1, scale=0.8), FadeIn(l1), run_time=0.6)
        self.play(FadeIn(times), FadeIn(e2, scale=0.8), FadeIn(l2), run_time=0.6)
        self.at("Both have white eyes")
        self.play(Indicate(e1, color=TEXT, scale_factor=1.15), Indicate(e2, color=TEXT, scale_factor=1.15), run_time=0.8)

        self.at("Yet the offspring")
        a = arr([0.0, y, 0], [1.9, y, 0], GREY)
        q = bchip("?", GREY, 44).move_to([3.3, y, 0])
        self.play(GrowArrow(a), FadeIn(q, scale=0.8), run_time=0.7)
        self.at("ordinary red eyes")
        e3 = eye("red", 0.62).move_to([3.3, y, 0])
        l3 = T("offspring", 24, GREY).next_to(e3, DOWN, buff=0.2)
        self.play(ReplacementTransform(q, e3), FadeIn(l3), run_time=0.8)
        self.at("How can that be")
        self.play(Indicate(e3, color=MAROON, scale_factor=1.2), run_time=0.9)

        # --- the pigment chain -----------------------------------------------------------------
        cy = -1.6
        xs = [-5.0, -2.7, -0.4, 1.9]
        pig = Circle(radius=0.6, stroke_color=GREY, stroke_width=3, fill_color=MAROON, fill_opacity=1).move_to([4.7, cy, 0])
        pig_l = T("pigment", 24, GREY).next_to(pig, DOWN, buff=0.2)
        self.at("A red eye needs pigment")
        self.play(VGroup(e1, e2, times, l1, l2, a, e3, l3).animate.set_opacity(0.3), run_time=0.5)
        self.play(FadeIn(pig, scale=0.7), FadeIn(pig_l), run_time=0.6)
        chips = [bchip(f"step {i+1}", GREY, 26).move_to([x, cy, 0]) for i, x in enumerate(xs)]
        arrows = []
        pts = xs + [4.7]
        for i in range(4):
            r = chips[i].get_right()[0] + 0.05 if i < 4 else 0
            l = (chips[i + 1].get_left()[0] - 0.05) if i < 3 else pig.get_left()[0] - 0.05
            arrows.append(arr([chips[i].get_right()[0] + 0.05, cy, 0], [l, cy, 0], GREY))
        self.at("made in several steps")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(c, shift=RIGHT * 0.2), GrowArrow(a_)) for c, a_ in zip(chips, arrows)],
                              lag_ratio=0.35), run_time=2.4)
        self.at("Losing any one step")
        cr = xmark(0.2, 0.2).next_to(chips[2], UP, buff=0.15)
        self.play(chips[2][1].animate.set_stroke(RED).set_fill(RED, 0.16), chips[2][2].animate.set_color(RED),
                  Create(cr), pig[0].animate.set_fill(PALE, 1), run_time=0.8)
        pale = T("pale", 24, GREY).next_to(pig, DOWN, buff=0.2)
        self.play(ReplacementTransform(pig_l, pale), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class Station(VGroup):
    def __init__(self, n, x, y):
        box = RoundedRectangle(corner_radius=0.14, width=0.95, height=0.95, stroke_color=TEXT, stroke_width=3,
                               fill_color=TEXT, fill_opacity=0.1)
        lab = T(str(n), 30, TEXT)
        cross = xmark(0.5, 0.5, RED, 6).set_stroke(opacity=0)
        super().__init__(box, cross, lab)
        self.box, self.lab, self.cross = box, lab, cross
        self.move_to([x, y, 0])

    def bad(self):
        return [self.box.animate.set_stroke(RED).set_fill(RED, 0.15), self.lab.animate.set_color(RED),
                self.cross.animate.set_stroke(opacity=0.6)]

    def good(self):
        return [self.box.animate.set_stroke(TEXT).set_fill(TEXT, 0.1), self.lab.animate.set_color(TEXT),
                self.cross.animate.set_stroke(opacity=0)]


class Line5:
    def __init__(self, y, name, broken=(), xs=None):
        self.y = y
        self.st = [Station(i + 1, -3.9 + 1.6 * i, y) for i in range(5)]
        self.arrows = [arr([self.st[i].get_right()[0] + 0.03, y, 0], [self.st[i + 1].get_left()[0] - 0.03, y, 0], GREY)
                       for i in range(4)]
        self.arrows.append(arr([self.st[4].get_right()[0] + 0.03, y, 0], [3.75, y, 0], GREY))
        self.prod = Circle(radius=0.5, stroke_color=GREY, stroke_width=3, fill_color=MAROON, fill_opacity=1).move_to([4.5, y, 0])
        self.label = T(name, 24, GREY).move_to([-5.55, y, 0])
        for i in broken:
            s = self.st[i]
            s.box.set_stroke(RED).set_fill(RED, 0.15); s.lab.set_color(RED); s.cross.set_stroke(opacity=0.6)
        if broken:
            self.prod.set_fill(PALE, 1)

    def group(self):
        return VGroup(self.label, *self.st, *self.arrows, self.prod)

    def prod_to(self, kind):
        return self.prod.animate.set_fill(MAROON if kind == "red" else PALE, 1)


class S02Line(SpokenScene):
    def construct(self):
        L1 = Line5(2.1, "line one")
        self.at("assembly line")
        self.play(FadeIn(L1.label), LaggedStart(*[FadeIn(s, shift=DOWN * 0.15) for s in L1.st], lag_ratio=0.2),
                  LaggedStart(*[GrowArrow(a) for a in L1.arrows], lag_ratio=0.2), FadeIn(L1.prod, scale=0.7), run_time=1.8)
        pl = T("pigment", 22, GREY).next_to(L1.prod, UP, buff=0.15)
        self.play(FadeIn(pl), run_time=0.3)

        self.at("A broken station")
        self.play(*L1.st[1].bad(), run_time=0.6)
        self.at("stops the product")
        self.play(L1.prod_to("pale"), FadeOut(pl), run_time=0.5)
        self.at("looks the same")
        self.play(Indicate(L1.prod, color=TEXT, scale_factor=1.25), run_time=0.8)
        self.at("One line has station two")
        self.play(Indicate(L1.st[1], color=RED, scale_factor=1.2), run_time=0.8)

        L2 = Line5(0.2, "line two", broken=[3])
        self.at("Another has")
        self.play(FadeIn(L2.group()), run_time=0.8)
        self.at("four broken")
        self.play(Indicate(L2.st[3], color=RED, scale_factor=1.2), run_time=0.8)

        # borrow the working stations into a third line
        L3 = Line5(-2.0, "borrowed")
        self.at("Borrow the working stations")
        self.play(FadeIn(L3.label), run_time=0.3)
        L3.prod.set_fill(PALE, 1)
        anims = []
        for i in range(5):
            src = L2.st[i] if i == 1 else L1.st[i]
            anims.append(TransformFromCopy(src, L3.st[i]))
        self.play(LaggedStart(*anims, lag_ratio=0.2), run_time=1.6)
        self.play(*[GrowArrow(a) for a in L3.arrows], FadeIn(L3.prod), run_time=0.4)
        self.at("you get a working line")
        self.play(L3.prod_to("red"), Flash(L3.prod, color=MAROON, line_length=0.25, flash_radius=0.8), run_time=0.8)

        # reset: both lines broke station two
        self.at("both lines broke station two")
        self.play(*L2.st[3].good(), *L2.st[1].bad(), *L3.st[1].bad(), L3.prod_to("pale"), run_time=0.9)
        self.at("borrowing helps nothing")
        self.play(Indicate(L3.st[1], color=RED, scale_factor=1.2), Indicate(L3.prod, color=TEXT, scale_factor=1.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class Gene(VGroup):
    def __init__(self, gid, x, y, label="+", broken=False, w=1.9, h=1.0):
        gcol = GENE[gid]
        box = Rectangle(width=w, height=h, stroke_color=gcol, stroke_width=4, fill_color=gcol,
                        fill_opacity=0.05 if broken else 0.6)
        cross = xmark(w / 2, h / 2, RED, 4).set_stroke(opacity=1 if broken else 0)
        back = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.6, stroke_width=0, fill_color=BG, fill_opacity=1)
        lab = T(label, 34, TEXT)
        super().__init__(box, cross, back, lab)
        self.box, self.cross, self.back, self.lab, self.gcol = box, cross, back, lab, gcol
        self.move_to([x, y, 0])

    def morph(self, label, broken):
        new = T(label, 34, TEXT).move_to(self.box)
        return [self.box.animate.set_fill(self.gcol, 0.05 if broken else 0.6),
                self.cross.animate.set_stroke(opacity=1 if broken else 0),
                Transform(self.lab, new)]


def bar(y):
    return RoundedRectangle(corner_radius=0.25, width=10.8, height=0.55, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.35).move_to([0, y, 0])


Y1, Y2 = 1.7, 0.1
XA, XB = -2.6, 2.6


def result(kind, y=-2.55):
    """kind: None (neutral), 'wt' or 'mut'."""
    if kind is None:
        return VGroup(bchip("?", GREY, 34)).move_to([0, y, 0])
    if kind == "wt":
        c = bchip("wild type", GREEN, 34)
        e = eye("red", 0.4)
    else:
        c = bchip("mutant", RED, 34)
        e = eye("white", 0.4)
    e.next_to(c, RIGHT, buff=0.4)
    g = VGroup(c, e)
    return g.move_to([0, y, 0])


def diploid_frame():
    r = RoundedRectangle(corner_radius=0.2, width=11.9, height=4.1, stroke_color=GREY, stroke_width=2,
                         fill_opacity=0).move_to([0, 1.05, 0])
    r.set_stroke(opacity=0.6)
    t = T("one diploid", 22, GREY).move_to([-5.0, 2.85, 0])
    return VGroup(r, t)


class S03Trans(SpokenScene):
    def construct(self):
        frame = diploid_frame()
        c1, c2 = bar(Y1), bar(Y2)
        gA1, gB1 = Gene("A", XA, Y1), Gene("B", XB, Y1)
        gA2, gB2 = Gene("A", XA, Y2), Gene("B", XB, Y2)
        nA = T("gene A", 28, BLUE).move_to([XA, 2.7, 0])
        nB = T("gene B", 28, YELLOW).move_to([XB, 2.7, 0])
        res = result(None)
        self.at("Now do the same")
        self.play(FadeIn(frame), run_time=0.6)
        self.at("Combine the two")
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(g, scale=0.9) for g in (gA1, gB1, gA2, gB2)], lag_ratio=0.15),
                  FadeIn(nA), FadeIn(nB), FadeIn(res), run_time=1.0)
        self.at("called trans")
        trans = T("trans: one mutation on each chromosome", 26, GREY).move_to([0, -1.55, 0])
        self.play(FadeIn(trans, shift=UP * 0.1), run_time=0.6)
        self.at("One mutation")
        self.play(*gA1.morph("a", True), Indicate(nA, color=BLUE, scale_factor=1.15), run_time=0.8)
        self.at("The other is")
        self.play(*gB2.morph("b", True), Indicate(nB, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("Each chromosome supplies")
        r1 = SurroundingRectangle(gB1, color=GREEN, buff=0.12, stroke_width=5)
        r2 = SurroundingRectangle(gA2, color=GREEN, buff=0.12, stroke_width=5)
        self.play(Create(r1), Create(r2), run_time=0.8)
        self.at("The phenotype is")
        self.play(ReplacementTransform(res, result("wt")), run_time=0.8)
        self.at("The mutations complement")
        self.play(Indicate(r1, color=GREEN, scale_factor=1.1), Indicate(r2, color=GREEN, scale_factor=1.1), run_time=0.9)
        self.finish()


class S04Same(SpokenScene):
    def construct(self):
        frame = diploid_frame()
        c1, c2 = bar(Y1), bar(Y2)
        gA1, gB1 = Gene("A", XA, Y1, "a", True), Gene("B", XB, Y1)
        gA2, gB2 = Gene("A", XA, Y2), Gene("B", XB, Y2, "b", True)
        nA = T("gene A", 28, BLUE).move_to([XA, 2.7, 0])
        nB = T("gene B", 28, YELLOW).move_to([XB, 2.7, 0])
        res = result("wt")
        trans = T("trans: one mutation on each chromosome", 26, GREY).move_to([0, -1.55, 0])
        r1 = SurroundingRectangle(gB1, color=GREEN, buff=0.12, stroke_width=5)
        r2 = SurroundingRectangle(gA2, color=GREEN, buff=0.12, stroke_width=5)
        self.add(frame, c1, c2, gA1, gB1, gA2, gB2, nA, nB, res, trans, r1, r2)
        self.at("Now try two alleles")
        neutral = result(None)
        self.play(FadeOut(r1), FadeOut(r2), ReplacementTransform(res, neutral), *gB2.morph("+", False), run_time=0.9)
        self.at("of one gene")
        self.play(*gA2.morph("a2", True), *gA1.morph("a1", True), Indicate(nA, color=BLUE, scale_factor=1.2), run_time=0.9)
        self.at("Each chromosome carries")
        self.play(Indicate(VGroup(gA1, gA2), color=BLUE, scale_factor=1.06), run_time=0.8)
        self.at("has no working copy")
        self.play(Indicate(VGroup(gA1, gA2), color=RED, scale_factor=1.08), run_time=0.9)
        self.at("stays mutant")
        self.play(ReplacementTransform(neutral, result("mut")), run_time=0.8)
        self.at("fail to complement")
        self.play(Indicate(VGroup(gA1, gA2), color=BLUE, scale_factor=1.08), run_time=0.8)
        self.at("complementation group")
        grp = DashedVMobject(Rectangle(width=2.4, height=2.8, color=BLUE, stroke_width=5), num_dashes=40)
        grp.move_to([XA, (Y1 + Y2) / 2, 0])
        gl = T("one complementation group", 24, BLUE).move_to([0, (Y1 + Y2) / 2, 0]).align_to([-1.0, 0, 0], LEFT)
        self.play(Create(grp), FadeIn(gl), run_time=0.9)
        self.at("In the simple model")
        sm = T("in the simple model: one gene", 26, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(sm, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Sort(SpokenScene):
    def construct(self):
        cx, cy, R = -2.4, 0.0, 2.45
        pos = {}
        for i in range(1, 7):
            ang = np.radians(90 - 60 * (i - 1))
            pos[i] = np.array([cx + R * np.cos(ang), cy + R * np.sin(ang), 0])
        nodes = {}
        for i in range(1, 7):
            c = Circle(radius=0.42, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(pos[i])
            t = T(str(i), 30, TEXT).move_to(pos[i])
            nodes[i] = VGroup(c, t)
        pairs = [(a, b) for a in range(1, 7) for b in range(a + 1, 7)]
        fails = {(1, 3), (1, 5), (2, 6), (3, 5)}
        lines = {}
        for a, b in pairs:
            d = pos[b] - pos[a]; d = d / np.linalg.norm(d)
            lines[(a, b)] = Line(pos[a] + d * 0.42, pos[b] - d * 0.42, color=GREEN, stroke_width=2.5).set_stroke(opacity=0.55)
        self.at("worked problem")
        self.play(LaggedStart(*[FadeIn(nodes[i], scale=0.8) for i in range(1, 7)], lag_ratio=0.12), run_time=1.2)
        self.at("crossed in all")
        self.play(LaggedStart(*[Create(lines[p]) for p in pairs], lag_ratio=0.06), run_time=2.0)

        panel_x = 4.2
        hd = T("stay white", 28, RED).move_to([panel_x, 2.5, 0])
        flist = [(1, 3), (1, 5), (2, 6), (3, 5)]
        rows = VGroup(*[M(f"{a} × {b}", 32, RED) for a, b in flist]).arrange(DOWN, buff=0.28).move_to([panel_x, 0.9, 0])
        self.at("stay white")
        self.play(*[lines[p].animate.set_stroke(RED, 7, 1.0) for p in flist],
                  *[lines[p].animate.set_stroke(opacity=0.12) for p in pairs if p not in fails],
                  FadeIn(hd), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.3), run_time=1.6)

        def paint(ids, col):
            return [nodes[i][0].animate.set_stroke(col).set_fill(col, 0.45) for i in ids]

        gl1 = T("group: 1, 3, 5", 28, BLUE)
        gl2 = T("group: 2, 6", 28, YELLOW)
        gl3 = T("group: 4", 28, PURPLE)
        gl = VGroup(gl1, gl2, gl3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([panel_x, -1.5, 0])
        self.at("Mutant one fails")
        self.play(Indicate(nodes[1], color=RED, scale_factor=1.2), run_time=0.7)
        self.at("form a group")
        self.play(*paint([1, 3, 5], BLUE), FadeIn(gl1, shift=LEFT * 0.2), run_time=0.8)
        self.at("Mutant two fails only")
        self.play(Indicate(nodes[2], color=RED, scale_factor=1.2), run_time=0.7)
        self.at("Those two form")
        self.play(*paint([2, 6], YELLOW), FadeIn(gl2, shift=LEFT * 0.2), run_time=0.8)
        self.at("complements all")
        four = [lines[(a, b)] for a, b in pairs if 4 in (a, b)]
        self.play(*[l.animate.set_stroke(GREEN, 6, 1.0) for l in four], *paint([4], PURPLE), FadeIn(gl3, shift=LEFT * 0.2), run_time=0.9)
        self.at("three complementation groups")
        tally = T("at least three genes", 30, TEXT, weight=BOLD).move_to([panel_x, -2.85, 0])
        self.play(FadeIn(tally, shift=UP * 0.1), run_time=0.7)
        self.at("because other genes")
        note = T("other genes may not have been hit", 22, GREY).move_to([panel_x, -3.35, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mini_gene(gid, label="+"):
    return Gene(gid, 0, 0, label, False, w=1.3, h=0.7)


class S06Rule(SpokenScene):
    def construct(self):
        frame = diploid_frame()
        c1, c2 = bar(Y1), bar(Y2)
        gA1, gB1 = Gene("A", XA, Y1, "a", True), Gene("B", XB, Y1)
        gA2, gB2 = Gene("A", XA, Y2), Gene("B", XB, Y2, "b", True)
        nA = T("gene A", 28, BLUE).move_to([XA, 2.7, 0])
        nB = T("gene B", 28, YELLOW).move_to([XB, 2.7, 0])
        res = result("wt")
        trans = T("trans: one mutation on each chromosome", 26, GREY).move_to([0, -1.55, 0])
        self.add(frame, c1, c2, gA1, gB1, gA2, gB2, nA, nB, res, trans)
        self.at("Both mutations must be")
        rt1 = T("recessive", 24, GREY).next_to(gA1, DOWN, buff=0.12)
        rt2 = T("recessive", 24, GREY).next_to(gB2, DOWN, buff=0.12)
        self.play(FadeIn(rt1), FadeIn(rt2), run_time=0.7)
        self.at("A dominant allele")
        dom = T("dominant", 24, RED).move_to(rt1)
        neutral = result(None)
        self.play(Transform(rt1, dom), ReplacementTransform(res, neutral),
                  gA1.box.animate.set_fill(RED, 0.6).set_stroke(RED), gA1.cross.animate.set_stroke(opacity=0),
                  Transform(gA1.lab, T("D", 34, TEXT).move_to(gA1.box)), run_time=0.9)
        self.at("gives a mutant phenotype")
        self.play(ReplacementTransform(neutral, result("mut")), run_time=0.8)
        self.at("opposite any partner")
        self.play(Indicate(gB2, color=YELLOW, scale_factor=1.1), Indicate(gA2, color=BLUE, scale_factor=1.1), run_time=0.9)
        self.at("says nothing")
        sn = T("the trans result says nothing", 26, GREY).move_to([0, -3.2, 0])
        self.play(FadeIn(sn, shift=UP * 0.1), run_time=0.7)

        self.at("keep this rule")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        head = T("recessive mutations, in trans", 30, GREY).move_to([0, 3.0, 0])
        self.play(FadeIn(head), run_time=0.4)

        def card(x, col, lamp, kinds, txt):
            box = RoundedRectangle(corner_radius=0.25, width=5.8, height=4.4, stroke_color=col, stroke_width=3,
                                   fill_color=col, fill_opacity=0.08).move_to([x, 0.0, 0])
            lp = result(lamp, 1.15)
            lp.move_to([x, 1.15, 0])
            g1, g2 = mini_gene(kinds[0]).move_to([x - 0.9, -0.15, 0]), mini_gene(kinds[1]).move_to([x + 0.9, -0.15, 0])
            tx = T(txt, 38, col, weight=BOLD).move_to([x, -1.3, 0])
            return box, lp, g1, g2, tx

        b1, l1, a1, a2, t1 = card(-3.3, GREEN, "wt", "AB", "different genes")
        b2, l2, c1_, c2_, t2 = card(3.3, RED, "mut", "AA", "one gene")
        self.at("In the simple")
        self.play(Transform(head, T("recessive mutations, in trans, in the simple model", 30, GREY).move_to([0, 3.0, 0])), run_time=0.6)
        self.at("Wild type", nth=0)
        self.play(FadeIn(b1), FadeIn(l1), run_time=0.5)
        self.play(FadeIn(a1), FadeIn(a2), run_time=0.4)
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.at("means one gene")
        self.play(FadeIn(b2), FadeIn(l2), run_time=0.5)
        self.play(FadeIn(c1_), FadeIn(c2_), run_time=0.4)
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "In the simple model, wild type in trans means different genes."
