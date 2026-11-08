"""Reading pedigrees: every fact removes some outcomes  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the normal allele A (chromosome band and letter)
  ORANGE = the recessive allele a
  GREEN  = carrier (Aa): symbol outline, cell outline, the answer 2/3
  YELLOW = the woman we are asking about
  RED    = an outcome that is ruled out (the cross-out)
  GREY   = outlines, labels, the discarded old answer 1/2, assumptions
  TEXT   = pedigree symbols, equations, rule lines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
AC, ac = BLUE, ORANGE


def col(ch):
    return AC if ch == "A" else ac


def capsule(ch, h=1.15):
    body = RoundedRectangle(corner_radius=0.26, width=0.52, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.14)
    band = Rectangle(width=0.52, height=0.46, stroke_width=0, fill_color=col(ch), fill_opacity=1).move_to(body)
    return VGroup(body, band, M(ch, 28, BG, weight=BOLD).move_to(band))


def pair(s, h=1.15):
    return VGroup(*[capsule(c, h) for c in s]).arrange(RIGHT, buff=0.14)


def gamete(ch, r=0.4):
    c = col(ch)
    ci = Circle(radius=r, stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.2)
    return VGroup(ci, M(ch, 34, c, weight=BOLD).move_to(ci))


def geno(s, size=40):
    return VGroup(*[M(ch, size, col(ch), weight=BOLD) for ch in s]).arrange(RIGHT, buff=0.05)


def person(kind, filled=False, stroke=TEXT, side=1.1):
    if kind == "sq":
        s = Square(side_length=side)
    else:
        s = Circle(radius=side / 2)
    s.set_stroke(stroke, 4)
    s.set_fill(TEXT if filled else BG, 0.9 if filled else 1)
    return s


def cross_out(mob, color=RED):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=7),
                  Line(mob.get_corner(UR), mob.get_corner(DL), color=color, stroke_width=7))


TX = -2.0   # centre of the family tree
FX, MX = TX - 1.7, TX + 1.7
PY, SY, CY = 2.0, 0.3, -1.1


def family(sis_mark=True):
    """The pedigree: unaffected parents, affected brother (filled), the woman (yellow ?)."""
    father = person("sq").move_to([FX, PY, 0])
    mother = person("c").move_to([MX, PY, 0])
    pline = Line([FX + 0.55, PY, 0], [MX - 0.55, PY, 0], color=TEXT, stroke_width=4)
    drop = Line([TX, PY, 0], [TX, SY, 0], color=TEXT, stroke_width=4)
    sib = Line([FX, SY, 0], [MX, SY, 0], color=TEXT, stroke_width=4)
    d1 = Line([FX, SY, 0], [FX, CY + 0.55, 0], color=TEXT, stroke_width=4)
    d2 = Line([MX, SY, 0], [MX, CY + 0.55, 0], color=TEXT, stroke_width=4)
    bro = person("sq", True).move_to([FX, CY, 0])
    sis = person("c", False, YELLOW).move_to([MX, CY, 0])
    q = T("?", 40, YELLOW, weight=BOLD).move_to(sis)
    blab = T("cystic fibrosis", 24, GREY).move_to([FX, CY - 1.0, 0])
    slab = T("she", 26, YELLOW).move_to([MX, CY - 1.0, 0])
    parts = dict(father=father, mother=mother, lines=VGroup(pline, drop, sib, d1, d2), bro=bro, sis=sis, q=q,
                 blab=blab, slab=slab)
    return parts


def legend():
    a = person("sq", True, side=0.34)
    at = T("affected", 22, GREY)
    b = person("sq", False, side=0.34)
    bt = T("unaffected", 22, GREY)
    g = VGroup(VGroup(a, at).arrange(RIGHT, buff=0.15), VGroup(b, bt).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.7)
    return g.move_to([TX, -3.05, 0])


class S00Title(TitleCard):
    LESSON = "Reading Pedigrees: Human Inheritance"
    TITLE = "A fact changes what you know"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        p = family()
        self.at("brother")
        self.play(FadeIn(p["father"]), FadeIn(p["mother"]), Create(p["lines"]), FadeIn(p["bro"]), run_time=0.8)
        self.at("cystic fibrosis")
        lg = legend()
        self.play(FadeIn(p["blab"]), FadeIn(lg), Indicate(p["bro"], color=TEXT, scale_factor=1.12), run_time=0.8)
        self.at("neither does she")
        self.play(FadeIn(p["sis"]), FadeIn(p["q"]), FadeIn(p["slab"]), run_time=0.7)
        self.at("What is the chance")
        ask = T("Is she a carrier?", 32, YELLOW).move_to([4.2, 2.1, 0])
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.6)
        self.at("answer is one half")
        half = chip("1/2", GREY, size=48).move_to([3.0, 0.4, 0])
        self.play(FadeIn(half, shift=UP * 0.15), run_time=0.5)
        self.at("two thirds")
        two = chip("2/3", GREEN, size=48).move_to([5.4, 0.4, 0])
        self.play(FadeIn(two, shift=UP * 0.15), run_time=0.5)
        self.play(Indicate(two, color=GREEN, scale_factor=1.12), run_time=0.7)
        self.at("cross people")
        note = T("pedigree", 30, GREY).move_to([TX, 3.15, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("pedigrees")
        self.play(Indicate(note, color=TEXT, scale_factor=1.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Parents(SpokenScene):
    def construct(self):
        p = family()
        lg = legend()
        self.add(p["father"], p["mother"], p["lines"], p["bro"], p["sis"], p["q"], p["blab"], p["slab"], lg)
        self.at("Start with her parents")
        self.play(VGroup(p["father"], p["mother"]).animate.scale(1.12), rate_func=there_and_back, run_time=0.8)
        self.at("so both must be carriers")
        self.play(p["father"].animate.set_stroke(GREEN, 6), p["mother"].animate.set_stroke(GREEN, 6), run_time=0.6)
        self.at("affected person")
        aa = pair("aa").move_to([FX - 1.55, CY, 0])
        self.play(FadeIn(aa, shift=RIGHT * 0.2), run_time=0.7)
        self.at("carrier has one copy")
        gf = pair("Aa").move_to([FX - 1.55, PY, 0])
        gm = pair("Aa").move_to([MX + 1.55, PY, 0])
        self.play(FadeIn(gf, shift=RIGHT * 0.2), FadeIn(gm, shift=LEFT * 0.2), run_time=0.8)
        self.at("shows no trait")
        self.play(Indicate(VGroup(gf, gm), color=TEXT, scale_factor=1.1), run_time=0.7)
        self.at("genotype as")
        word = T("carrier", 30, GREEN)
        gtxt = geno("Aa", 72)
        panel = VGroup(word, gtxt).arrange(DOWN, buff=0.25).move_to([4.4, 1.6, 0])
        self.play(FadeIn(word), Write(gtxt), run_time=0.9)
        self.at("full penetrance")
        c1 = chip("full penetrance", GREY, size=22).move_to([4.4, -0.2, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("no new mutations")
        c2 = chip("no new mutations", GREY, size=22).move_to([4.4, -1.1, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        self.at("correct relationships")
        c3 = chip("correct relationships", GREY, size=22).move_to([4.4, -2.0, 0])
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
GX = [1.9, 4.7]          # grid column centres (mother's allele A, a)
GY = [0.8, -1.4]         # grid row centres (father's allele A, a)
CW, CH = 2.8, 2.1


def cell(mo, fa):
    """one Punnett cell: box, genotype as a chromosome pair (mother's left), probability label."""
    box = RoundedRectangle(corner_radius=0.12, width=CW, height=CH, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.06)
    g = pair(mo + fa, 1.25).move_to(box).shift(UP * 0.2)
    pr = M("1/4", 26, GREY).move_to(box).shift(DOWN * 0.78)
    ci = (0 if mo == "A" else 1)
    ri = (0 if fa == "A" else 1)
    grp = VGroup(box, g, pr).move_to([GX[ci], GY[ri], 0])
    grp.box, grp.g, grp.pr = box, g, pr
    return grp


def headers():
    cols = [gamete("A").move_to([GX[0], 2.65, 0]), gamete("a").move_to([GX[1], 2.65, 0])]
    rows = [gamete("A").move_to([-0.1, GY[0], 0]), gamete("a").move_to([-0.1, GY[1], 0])]
    lm = T("from the mother", 24, GREY).move_to([3.3, 3.35, 0])
    lf = T("from the father", 24, GREY).rotate(PI / 2).move_to([-0.95, -0.3, 0])
    return cols, rows, lm, lf


class S03Cross(SpokenScene):
    def construct(self):
        mg = pair("Aa").move_to([-4.8, 1.5, 0])
        fg = pair("Aa").move_to([-4.8, -1.2, 0])
        ml = T("mother", 26, GREY).next_to(mg, DOWN, buff=0.25)
        fl = T("father", 26, GREY).next_to(fg, DOWN, buff=0.25)
        self.play(FadeIn(mg), FadeIn(fg), FadeIn(ml), FadeIn(fl), run_time=0.8)
        cols, rows, lm, lf = headers()
        self.at("giving one allele")
        self.play(*[ReplacementTransform(mg[i].copy(), cols[i]) for i in range(2)],
                  *[ReplacementTransform(fg[i].copy(), rows[i]) for i in range(2)],
                  FadeIn(lm), FadeIn(lf), run_time=1.2)
        self.at("Four outcomes")
        cells = {k: cell(*k) for k in ["AA", "Aa", "aA", "aa"]}
        for c in cells.values():
            c.pr.set_opacity(0)
        self.play(*[FadeIn(c.box) for c in cells.values()], run_time=0.7)
        self.at("capital A capital A")
        self.play(FadeIn(cells["AA"].g, scale=0.8), run_time=0.5)
        self.at("with the A from the mother")
        self.play(FadeIn(cells["Aa"].g, scale=0.8), run_time=0.5)
        self.at("small a capital A")
        self.play(FadeIn(cells["aA"].g, scale=0.8), run_time=0.5)
        self.at("with the A from the father")
        self.play(Indicate(cells["aA"].g[1], color=AC, scale_factor=1.15), run_time=0.6)
        self.at("and small a small a")
        self.play(FadeIn(cells["aa"].g, scale=0.8), run_time=0.5)
        self.at("Each outcome")
        self.play(*[c.pr.animate.set_opacity(1) for c in cells.values()], run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def full_grid():
    cols, rows, lm, lf = headers()
    cells = {k: cell(*k) for k in ["AA", "Aa", "aA", "aa"]}
    return cols, rows, lm, lf, cells


class S04Unaffected(SpokenScene):
    def construct(self):
        cols, rows, lm, lf, cells = full_grid()
        self.add(*cols, *rows, lm, lf, *cells.values())
        mg = pair("Aa").move_to([-4.8, 1.5, 0])
        fg = pair("Aa").move_to([-4.8, -1.2, 0])
        ml = T("mother", 26, GREY).next_to(mg, DOWN, buff=0.25)
        fl = T("father", 26, GREY).next_to(fg, DOWN, buff=0.25)
        old = VGroup(mg, fg, ml, fl)
        self.add(old)
        self.at("Before this fact")
        self.play(FadeOut(old), run_time=0.6)
        self.play(LaggedStart(*[Indicate(c.box, color=TEXT, scale_factor=1.05) for c in cells.values()],
                              lag_ratio=0.25), run_time=1.6)
        self.at("she is unaffected")
        w = person("c", False, YELLOW).move_to([-4.8, 1.0, 0])
        wl = T("she", 26, YELLOW).next_to(w, DOWN, buff=0.2)
        wu = T("unaffected", 26, GREY).next_to(wl, DOWN, buff=0.1)
        self.play(FadeIn(w), FadeIn(wl), FadeIn(wu), run_time=0.7)
        self.at("impossible")
        x = cross_out(cells["aa"].box)
        self.play(Create(x), cells["aa"].g.animate.set_opacity(0.25), cells["aa"].pr.animate.set_opacity(0.25),
                  cells["aa"].box.animate.set_stroke(RED, 3), run_time=0.8)
        self.at("Three equal outcomes remain")
        self.play(*[cells[k].box.animate.set_stroke(TEXT, 4) for k in ["AA", "Aa", "aA"]], run_time=0.6)
        self.at("two of them are carriers")
        self.play(*[cells[k].box.animate.set_stroke(GREEN, 6).set_fill(GREEN, 0.15) for k in ["Aa", "aA"]],
                  run_time=0.7)
        self.at("two out of three")
        res = M("2 of 3", 56, GREEN, weight=BOLD).move_to([-4.8, -1.9, 0])
        rl = T("are carriers", 26, GREEN).next_to(res, DOWN, buff=0.15)
        self.play(FadeIn(res, shift=UP * 0.15), FadeIn(rl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
BX = [-3.6, -1.2, 1.2, 3.6]
BY = 1.3


def block(k, x, w=2.3, y=BY):
    carrier = k in ("Aa", "aA")
    box = RoundedRectangle(corner_radius=0.12, width=w, height=1.2,
                           stroke_color=GREEN if carrier else GREY, stroke_width=5 if carrier else 3,
                           fill_color=GREEN if carrier else GREY, fill_opacity=0.15 if carrier else 0.06)
    g = geno(k, 44).move_to(box)
    grp = VGroup(box, g).move_to([x, y, 0])
    grp.box, grp.g = box, g
    return grp


class S05Arithmetic(SpokenScene):
    def construct(self):
        blocks = {k: block(k, x) for k, x in zip(["AA", "Aa", "aA", "aa"], BX)}
        self.at("Check the arithmetic")
        self.play(*[FadeIn(b) for b in blocks.values()], run_time=0.6)
        x = cross_out(blocks["aa"].box)
        self.play(Create(x), blocks["aa"].g.animate.set_opacity(0.25), blocks["aa"].box.animate.set_stroke(RED, 3),
                  run_time=0.6)
        self.at("conditional probability")
        cp = M("P(carrier | unaffected)", 30, TEXT).move_to([0, 2.95, 0])
        self.play(FadeIn(cp, shift=DOWN * 0.1), run_time=0.6)
        self.at("Carriers hold one half")
        br1 = Brace(VGroup(blocks["Aa"], blocks["aA"]), direction=DOWN, color=GREEN, buff=0.12)
        l1 = M("1/2", 34, GREEN, weight=BOLD).next_to(br1, DOWN, buff=0.1)
        self.play(GrowFromCenter(br1), FadeIn(l1), run_time=0.7)
        self.at("three remaining outcomes")
        br2 = Brace(VGroup(blocks["AA"], blocks["Aa"], blocks["aA"]), direction=DOWN, color=GREY, buff=0.12)
        br2.shift(DOWN * 0.95)
        l2 = M("3/4", 34, TEXT, weight=BOLD).next_to(br2, DOWN, buff=0.1)
        self.play(GrowFromCenter(br2), FadeIn(l2), run_time=0.7)
        self.at("One half divided")
        e1 = M("(1/2)", 40, GREEN, weight=BOLD)
        e2 = M("/", 40, TEXT)
        e3 = M("(3/4)", 40, TEXT, weight=BOLD)
        e4 = M("=", 40, TEXT)
        e5 = M("2/3", 44, GREEN, weight=BOLD)
        eq = VGroup(e1, e2, e3, e4, e5).arrange(RIGHT, buff=0.2).move_to([0, -2.3, 0])
        self.play(ReplacementTransform(l1.copy(), e1), ReplacementTransform(l2.copy(), e3), FadeIn(e2), run_time=1.0)
        self.at("is two thirds")
        self.play(FadeIn(e4), Write(e5), run_time=0.7)
        self.at("The old answer")
        old = chip("1/2 : before she is unaffected", GREY, size=24).move_to([0, -3.2, 0])
        self.play(FadeIn(old, shift=UP * 0.1), Indicate(l1, color=GREY, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        blocks = {k: block(k, x, y=1.2) for k, x in zip(["AA", "Aa", "aA", "aa"], BX)}
        den = M("denominator: 4", 32, TEXT).move_to([0, 2.85, 0])
        self.play(*[FadeIn(b) for b in blocks.values()], FadeIn(den), run_time=0.7)
        self.at("Knowing she is unaffected")
        self.play(Indicate(VGroup(blocks["Aa"], blocks["aA"]), color=GREEN, scale_factor=1.05), run_time=0.8)
        self.at("removed one of four")
        x = cross_out(blocks["aa"].box)
        self.play(Create(x), blocks["aa"].box.animate.set_stroke(RED, 3), run_time=0.5)
        self.play(FadeOut(VGroup(blocks["aa"], x), shift=RIGHT * 0.5), run_time=0.6)
        self.at("to three")
        new = {k: block(k, xx, w=3.0, y=1.2) for k, xx in zip(["AA", "Aa", "aA"], [-3.1, 0, 3.1])}
        den3 = M("denominator: 3", 32, TEXT).move_to(den)
        self.play(*[ReplacementTransform(blocks[k], new[k]) for k in new], ReplacementTransform(den, den3),
                  run_time=1.0)
        self.at("Conditioning can use")
        r1 = chip("prior: what you believed before", TEXT, size=28)
        r2 = chip("likelihood: how likely the new evidence is", YELLOW, size=28)
        rules = VGroup(r1, r2).arrange(DOWN, buff=0.4).move_to([0, -1.5, 0])
        self.at("what you believed before")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.at("how likely the new evidence")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.at("exercise in the logic")
        ex = T("an exercise in the logic, not a risk figure", 26, GREY).move_to([0, -3.1, 0])
        self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A fact changes what you know, not her genotype."
