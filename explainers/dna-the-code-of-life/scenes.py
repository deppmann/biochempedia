"""DNA: the code of life  (Biochemistrypedia grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = DNA / a gene (a section of DNA)
  GREY   = the sugar-phosphate sides of the ladder, outlines
  YELLOW = base A      TEAL = base T      GREEN = base C      PINK = base G
  PURPLE = protein
  ORANGE = trait (flower colour)
  RED    = a change in the gene / the protein stops working
  TEXT   = living things, labels, plain words
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB0"
LET = {"A": YELLOW, "T": TEAL, "C": GREEN, "G": PINK}

XS = [-3.6, -1.2, 1.2, 3.6]
SIDEY = 1.75
TOPY, BOTY = 1.0, -1.0


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def blk(letter, x, y, w=1.5, h=1.25, size=46):
    c = LET[letter]
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=c, stroke_width=3,
                         fill_color=c, fill_opacity=0.3)
    t = T(letter, size, c, weight=BOLD).move_to(r)
    return VGroup(r, t).move_to([x, y, 0])


def empty_blk(x, y, w=1.5, h=1.25):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=GREY, stroke_width=3,
                         fill_opacity=0)
    t = T("?", 46, TEXT, weight=BOLD).move_to(r)
    return VGroup(r, t).move_to([x, y, 0])


def join(x):
    return Line([x, TOPY - 0.625, 0], [x, BOTY + 0.625, 0], color=GREY, stroke_width=6)


def sides():
    top = RoundedRectangle(corner_radius=0.1, width=10.6, height=0.28, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.5).move_to([0, SIDEY, 0])
    bot = top.copy().move_to([0, -SIDEY, 0])
    return top, bot


def rung(x):
    return Line([x, SIDEY - 0.12, 0], [x, -SIDEY + 0.12, 0], color=GREY, stroke_width=7)


def strip(letters, y, w=1.15, h=1.15, gap=0.15, size=42):
    bs = [blk(l, 0, 0, w, h, size) for l in letters]
    g = VGroup(*bs).arrange(RIGHT, buff=gap).move_to([0, y, 0])
    return g


class S00Title(TitleCard):
    LESSON = "DNA: The Code of Life"
    TITLE = "A Four-Letter Code Builds Proteins"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        names = ["strawberry", "mushroom", "bacterium", "person"]
        things = VGroup(*[chip(n, TEXT, size=30) for n in names]).arrange(RIGHT, buff=0.45).move_to([0, 2.5, 0])
        for i, nm in enumerate(["Strawberries", "mushrooms", "bacteria", "people"]):
            self.at(nm)
            self.play(FadeIn(things[i], scale=0.9), run_time=0.4)
        tags = VGroup(*[chip("DNA", BLUE, size=28) for _ in names])
        for t, th in zip(tags, things):
            t.next_to(th, DOWN, buff=0.5)
        links = VGroup(*[Line(th.get_bottom(), t.get_top(), color=BLUE, stroke_width=3) for th, t in zip(things, tags)])
        self.at("all have")
        self.play(LaggedStart(*[AnimationGroup(Create(l), FadeIn(t)) for l, t in zip(links, tags)], lag_ratio=0.2),
                  run_time=1.2)
        q1 = T("One kind of molecule.", 38, font=TITLE_FONT)
        q2 = T("Such different living things.", 38, font=TITLE_FONT)
        qa = VGroup(q1, q2).arrange(DOWN, buff=0.2).move_to([0, -0.5, 0])
        self.at("How can one kind")
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.5)
        e1 = T("How can a tiny code inside my cells", 36, YELLOW)
        e2 = T("decide what I look like?", 36, YELLOW)
        eq = VGroup(e1, e2).arrange(DOWN, buff=0.2).move_to([0, -2.6, 0])
        self.at("tiny code")
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ladder(SpokenScene):
    def construct(self):
        dna = chip("DNA", BLUE, size=64).move_to([-3.8, 0, 0])
        prot = chip("proteins", PURPLE, size=64).move_to([3.8, 0, 0])
        a = arr(dna.get_right(), prot.get_left(), GREY, w=7)
        lab = T("instructions", 30, TEXT).next_to(a, UP, buff=0.2)
        self.at("is a molecule")
        self.play(FadeIn(dna, scale=0.9), run_time=0.5)
        self.at("carries the instructions")
        self.play(GrowArrow(a), FadeIn(lab), run_time=0.6)
        self.play(FadeIn(prot, shift=LEFT * 0.2), run_time=0.5)
        top, bot = sides()
        rungs = VGroup(*[rung(x) for x in XS])
        self.at("twisted ladder")
        self.play(FadeOut(VGroup(dna, prot, a, lab)), run_time=0.4)
        self.play(GrowFromCenter(top), GrowFromCenter(bot), run_time=0.7)
        self.play(LaggedStart(*[Create(r) for r in rungs], lag_ratio=0.2), run_time=0.9)
        hel = chip("double helix", BLUE, size=36)
        note = T("a ladder twisted around itself (drawn flat)", 24, GREY)
        hg = VGroup(hel, note).arrange(RIGHT, buff=0.4).move_to([0, 3.15, 0])
        self.at("double helix")
        self.play(FadeIn(hg, shift=DOWN * 0.1), run_time=0.6)
        l1 = T("sugar and phosphate", 28, TEXT).move_to([0, 2.3, 0])
        l2 = T("sugar and phosphate", 28, TEXT).move_to([0, -2.3, 0])
        self.at("sugar and phosphate")
        self.play(FadeIn(l1), FadeIn(l2), top.animate.set_fill(GREY, 0.8), bot.animate.set_fill(GREY, 0.8),
                  run_time=0.6)
        same = T("The same in every living thing", 34, YELLOW, weight=BOLD).move_to([0, -3.1, 0])
        self.at("the same in every")
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Pairs(SpokenScene):
    def construct(self):
        top, bot = sides()
        rungs = [rung(x) for x in XS]
        self.add(top, bot, *rungs)
        cap = T("The code is in the rungs", 36, TEXT).move_to([0, 3.0, 0])
        TL, BL = "ACGT", "TGCA"
        tb = [blk(TL[i], XS[i], TOPY) for i in range(4)]
        bb = [blk(BL[i], XS[i], BOTY) for i in range(4)]
        jn = [join(x) for x in XS]
        eb = [empty_blk(XS[i], BOTY) for i in range(4)]
        self.at("The code sits")
        self.play(FadeIn(cap, shift=DOWN * 0.1), *[r.animate.set_color(TEXT) for r in rungs], run_time=0.5)
        self.play(*[r.animate.set_color(GREY) for r in rungs], run_time=0.3)

        def make_pair(i):
            return [FadeOut(rungs[i]), FadeIn(tb[i], scale=0.9), FadeIn(bb[i], scale=0.9), FadeIn(jn[i])]

        self.at("Each rung is")
        self.play(*make_pair(0), run_time=0.7)
        lb = T("base", 28, TEXT).move_to([XS[0], 2.45, 0])
        lp = T("base pair", 28, TEXT).move_to([XS[0], -2.4, 0])
        self.at("two bases joined")
        self.play(FadeIn(lb), FadeIn(lp), run_time=0.5)
        # legend
        cl = T("the four bases:", 26, TEXT)
        chips = [chip(l, LET[l], size=30) for l in "ATCG"]
        leg = VGroup(cl, *chips).arrange(RIGHT, buff=0.35).move_to([0, -3.15, 0])
        self.at("four bases have")
        self.play(FadeIn(leg, shift=UP * 0.1), run_time=0.7)
        self.at("always pairs with", nth=0)
        self.play(Indicate(VGroup(tb[0], bb[0]), color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.at("always pairs with", nth=1)
        self.play(*make_pair(1), run_time=0.5)
        self.play(Indicate(VGroup(tb[1], bb[1]), color=GREEN, scale_factor=1.08), run_time=0.7)
        self.at("So if one side")
        # clear the old answer: bottom side goes blank, the other two rungs get tops only
        self.play(FadeOut(lb), FadeOut(lp), FadeOut(cap),
                  ReplacementTransform(bb[0], eb[0]), ReplacementTransform(bb[1], eb[1]),
                  FadeOut(rungs[2]), FadeOut(rungs[3]),
                  FadeIn(tb[2], scale=0.9), FadeIn(tb[3], scale=0.9), FadeIn(eb[2]), FadeIn(eb[3]),
                  FadeIn(jn[2]), FadeIn(jn[3]), run_time=0.8)
        cap2 = T("one side reads A C G T", 34, TEXT).move_to([0, 3.0, 0])
        self.play(FadeIn(cap2), run_time=0.4)
        self.at("the other side")
        bb2 = [blk(BL[i], XS[i], BOTY) for i in range(4)]
        cap3 = T("the other side reads T G C A", 34, TEXT).move_to([0, 3.0, 0])
        self.play(ReplacementTransform(cap2, cap3), run_time=0.3)
        for i in range(4):
            self.play(ReplacementTransform(eb[i], bb2[i]), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Sequence(SpokenScene):
    def construct(self):
        s1 = strip("ATTGCAC", 1.2)
        self.at("The order of")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in s1], lag_ratio=0.12), run_time=1.0)
        oa = arr([-4.5, 2.35, 0], [4.5, 2.35, 0], TEXT, w=4)
        ol = T("order along the DNA", 26, TEXT).next_to(oa, UP, buff=0.1)
        self.play(GrowArrow(oa), FadeIn(ol), run_time=0.5)
        sq = chip("sequence", BLUE, size=36).move_to([-3.2, -0.45, 0])
        self.at("called the sequence")
        self.play(FadeIn(sq, shift=UP * 0.1), run_time=0.5)
        code = chip("the code", YELLOW, size=36).move_to([2.6, -0.45, 0])
        eq = T("=", 40, TEXT).move_to([-0.3, -0.45, 0])
        self.at("is the code")
        self.play(FadeIn(eq), FadeIn(code, shift=UP * 0.1), run_time=0.5)
        s2 = strip("CCAGTTA", -1.6)
        t2 = T("same letters, new order: different instructions", 30, TEXT).move_to([0, -2.85, 0])
        self.at("A different order")
        self.play(FadeOut(VGroup(sq, eq, code)), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in s2], lag_ratio=0.12), run_time=0.9)
        self.play(FadeIn(t2), run_time=0.4)
        # words
        self.at("Think of letters")
        self.play(FadeOut(VGroup(s1, s2, oa, ol, t2)), run_time=0.5)
        ws = [T(c, 110, TEXT, font=TITLE_FONT, weight=BOLD) for c in "EAT"]
        wg = VGroup(*ws).arrange(RIGHT, buff=0.35).move_to([0, 0.7, 0])
        self.play(FadeIn(wg, scale=0.9), run_time=0.5)
        wcap = T("same letters, new order, new word", 34, TEXT).move_to([0, -1.5, 0])
        self.at("The same letters")
        pos = [w.get_center().copy() for w in ws]
        self.play(ws[0].animate.move_to(pos[2]), ws[1].animate.move_to(pos[0]), ws[2].animate.move_to(pos[1]),
                  FadeIn(wcap), run_time=1.0)
        self.at("But a cell")
        self.play(FadeOut(VGroup(wg, wcap)), run_time=0.4)
        s3 = strip("ATTGCAC", 0.9)
        note = T("A cell does not understand words.", 34, TEXT).move_to([0, 2.7, 0])
        self.play(FadeIn(s3), FadeIn(note), run_time=0.6)
        mol = chip("molecules", TEXT, size=30)
        ptr = Triangle(color=TEXT, fill_opacity=1, stroke_width=0).scale(0.2)
        mol.move_to([s3[0].get_center()[0], -1.0, 0])
        ptr.next_to(s3[0], DOWN, buff=0.12)
        self.at("Its molecules")
        self.play(FadeIn(mol), FadeIn(ptr), run_time=0.4)
        self.at("simply follow")
        note2 = T("They follow the bases in order.", 34, YELLOW).move_to([0, -2.4, 0])
        self.play(FadeIn(note2), run_time=0.4)
        for b in s3:
            x = b.get_center()[0]
            self.play(mol.animate.move_to([x, -1.0, 0]), ptr.animate.move_to([x, -0.05, 0]),
                      Indicate(b, color=TEXT, scale_factor=1.12), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Chain(SpokenScene):
    def construct(self):
        line = Line([-6, 2.2, 0], [6, 2.2, 0], color=BLUE, stroke_width=5)
        top = T("DNA: very long and thin", 32, TEXT).move_to([0, 3.1, 0])
        self.at("very long and thin", lead=1.0)
        self.play(Create(line), FadeIn(top), run_time=0.9)
        bar = RoundedRectangle(corner_radius=0.3, width=7.0, height=0.8, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.2).move_to([0, 2.2, 0])
        top2 = T("chromosome: DNA wound up tightly with proteins", 32, TEXT).move_to([0, 3.1, 0])
        self.at("A chromosome is")
        self.play(FadeOut(line), FadeOut(top), run_time=0.35)
        self.play(FadeIn(bar), run_time=0.55)
        self.at("wound up tightly")
        self.play(FadeIn(top2), run_time=0.5)
        gene_hl = RoundedRectangle(corner_radius=0.15, width=1.5, height=0.8, stroke_color=BLUE, stroke_width=4,
                                   fill_color=BLUE, fill_opacity=0.9).move_to([-0.6, 2.2, 0])
        gl = T("gene", 30, BLUE, weight=BOLD).move_to([-0.6, 1.4, 0])
        self.at("A gene is")
        self.play(FadeIn(gene_hl), FadeIn(gl, shift=UP * 0.1), run_time=0.6)

        def desc(lines, x):
            return VGroup(*[T(s, 24, TEXT) for s in lines]).arrange(DOWN, buff=0.08).move_to([x, -1.7, 0])

        cg = chip("gene", BLUE, size=38).move_to([-4.2, -0.1, 0])
        cp = chip("protein", PURPLE, size=38).move_to([0, -0.1, 0])
        ct = chip("trait", ORANGE, size=38).move_to([4.2, -0.1, 0])
        dg = desc(["many carry the", "code for a particular", "protein"], -4.2)
        dp = desc(["builds cells and", "does most of the", "work in cells"], 0)
        dt = desc(["a feature of a", "living thing, like", "flower colour"], 4.2)
        a1 = arr(cg.get_right(), cp.get_left(), GREY, w=6)
        a2 = arr(cp.get_right(), ct.get_left(), GREY, w=6)
        self.at("genes carry")
        self.play(TransformFromCopy(gene_hl, cg), run_time=0.6)
        self.play(FadeIn(dg), run_time=0.4)
        self.at("A protein builds")
        self.play(GrowArrow(a1), FadeIn(cp, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(dp), run_time=0.4)
        self.at("Proteins affect traits")
        self.play(GrowArrow(a2), FadeIn(ct, shift=LEFT * 0.2), run_time=0.5)
        self.at("A trait is")
        self.play(FadeIn(dt), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        pea = T("pea plants", 34, TEXT, weight=BOLD).move_to([0, 2.2, 0])
        cg = chip("gene", BLUE, size=34)
        cp = chip("working protein", PURPLE, size=34)
        ct = chip("purple flowers", ORANGE, size=34)
        row = VGroup(cg, cp, ct).arrange(RIGHT, buff=1.5).move_to([0, 0.6, 0])
        a1 = arr(cg.get_right(), cp.get_left(), GREY, w=6)
        a2 = arr(cp.get_right(), ct.get_left(), GREY, w=6)
        self.at("In pea plants")
        self.play(FadeIn(pea), run_time=0.4)
        self.at("purple flowers")
        self.play(FadeIn(ct, shift=LEFT * 0.2), run_time=0.5)
        self.at("working protein")
        self.play(GrowArrow(a2), FadeIn(cp, shift=LEFT * 0.2), run_time=0.5)
        self.at("one gene")
        self.play(GrowArrow(a1), FadeIn(cg, shift=LEFT * 0.2), run_time=0.5)
        tag = chip("a change can stop the protein", RED, size=28).next_to(cg, DOWN, buff=0.5)
        tag.shift(RIGHT * max(0.0, -6.2 - tag.get_left()[0]))
        tl = Line([cg.get_center()[0], cg.get_bottom()[1], 0], [cg.get_center()[0], tag.get_top()[1], 0], color=RED, stroke_width=4)
        self.at("A change")
        self.play(FadeIn(tag), Create(tl), run_time=0.5)
        cp2 = chip("no working protein", RED, size=34).move_to(cp)
        a1b = arr(cg.get_right(), cp2.get_left(), GREY, w=6)
        a2b = arr(cp2.get_right(), ct.get_left(), GREY, w=6)
        ct2 = chip("white flowers", TEXT, size=34).move_to(ct)
        self.at("stop the protein")
        self.play(ReplacementTransform(ct, ct2), ReplacementTransform(cp, cp2), FadeOut(a1), FadeOut(a2), FadeIn(a1b), FadeIn(a2b), run_time=0.6)
        q = T("Why are they so different?", 44, TEXT, font=TITLE_FONT).move_to([0, 0, 0])
        self.at("So how do")
        self.play(FadeOut(VGroup(pea, a1b, a2b, cg, cp2, ct2, tag, tl)), run_time=0.4)
        self.play(FadeIn(q), run_time=0.4)
        ys = [2.6, 0.9, -0.8, -2.5]
        c1 = chip("same sugar, phosphate, four bases", GREY, size=30).move_to([0, ys[0], 0])
        c2 = chip("different order of the bases", BLUE, size=30).move_to([0, ys[1], 0])
        c3 = chip("different proteins", PURPLE, size=30).move_to([0, ys[2], 0])
        c4 = chip("such different living things", TEXT, size=30).move_to([0, ys[3], 0])
        b1 = arr(c1.get_bottom(), c2.get_top(), GREY, w=5)
        b2 = arr(c2.get_bottom(), c3.get_top(), GREY, w=5)
        b3 = arr(c3.get_bottom(), c4.get_top(), GREY, w=5)
        self.at("They all build")
        self.play(FadeOut(q), FadeIn(c1, shift=DOWN * 0.1), run_time=0.5)
        self.at("The order of the bases")
        self.play(GrowArrow(b1), FadeIn(c2, shift=DOWN * 0.1), run_time=0.6)
        self.at("so their genes")
        self.play(GrowArrow(b2), FadeIn(c3, shift=DOWN * 0.1), run_time=0.6)
        self.at("different proteins")
        self.play(GrowArrow(b3), FadeIn(c4, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "The order of the bases is the code."
