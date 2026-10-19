"""Smell reads patterns, taste reads cells (Biochemistrypedia explainer)

Every self.at("...") cue waits for that phrase in audio/words.json.
No traces here: the receptor matrix is the lesson's invented example (labelled "invented example").

COLOR MAP (one color per concept, whole video)
  BLUE   = odorant receptors / the smell side (headers, receptor chips, receptor-sharing neurons, their glomeruli)
  YELLOW = odorants (dots, odorant row labels, concentration)
  GREEN  = on: a receptor that responds, a lamp that is lit
  RED    = removed or lost (crossed-out receptor, crossed-out PLCb2)
  TEAL   = the shared enzyme PLCb2
  ORANGE = sweet cell      PINK = umami cell      PURPLE = bitter cell
  TEXT (white) = sour and salty cells, plain labels;  GREY = structure, off states, tags
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PINK = "#E88FB4"
PURPLE = "#B58CE8"
RECEPTOR, ODORANT, ON, GONE, ENZ = BLUE, YELLOW, GREEN, RED, TEAL


def tag(text="mouse", x=5.6, y=3.35):
    return T(text, 22, GREY).move_to([x, y, 0])


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def xmark(center, s=0.3, color=GONE, w=7):
    c = np.array([center[0], center[1], 0.0])
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


# ------------------------------------------------------------------ matrix (the lesson's invented example)
COLX = {"A": -3.4, "B": -2.1, "C": -0.8, "D": 0.5}
ROWY = {2: 1.0, 3: -0.3, 1: -1.8}
HEADY = 2.3
PATX = 3.0
PAT = {2: "B C", 3: "A B C", 1: "A B"}


def header(l):
    return chip(l, RECEPTOR, size=30).move_to([COLX[l], HEADY, 0])


def pat_title():
    return T("pattern", 22, GREY).move_to([PATX, HEADY, 0])


def cell(l, n, on=False):
    c = Circle(radius=0.27, stroke_color=ON if on else GREY, stroke_width=3,
               fill_color=ON, fill_opacity=0.9 if on else 0).move_to([COLX[l], ROWY[n], 0])
    return c


def row_label(n):
    return T(f"odorant {n}", 24, ODORANT).move_to([-5.4, ROWY[n], 0])


def pat_text(n, s=None):
    return M(s or PAT[n], 32).move_to([PATX, ROWY[n], 0])


def make_row(n, on_letters):
    cells = {l: cell(l, n, False) for l in "ABCD"}
    return row_label(n), cells, pat_text(n), on_letters


def static_row(n, letters=None):
    """row with its final state (no animation)"""
    on = PAT[n].replace(" ", "") if letters is None else letters
    cells = {l: cell(l, n, l in on) for l in "ABCD"}
    return row_label(n), cells, pat_text(n)


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Smell and Taste"
    TITLE = "Smell Reads Patterns, Taste Reads Cells"


class S01Question(SpokenScene):
    def construct(self):
        sm = chip("SMELL", RECEPTOR, size=40)
        ta = chip("TASTE", TEXT, size=40)
        q = T("?", 72, GREY)
        g = VGroup(sm, q, ta).arrange(RIGHT, buff=1.0).move_to([0, 0.7, 0])
        both = T("both detect chemicals", 30, GREY).move_to([0, -1.1, 0])
        self.at("Smell and taste")
        self.play(FadeIn(sm, shift=RIGHT * 0.3), FadeIn(ta, shift=LEFT * 0.3), run_time=0.8)
        self.at("detect chemicals")
        self.play(FadeIn(both), run_time=0.6)
        self.at("so differently")
        self.play(GrowFromCenter(q), run_time=0.6)
        self.at("In a mouse")
        self.play(FadeOut(VGroup(g, both)), run_time=0.6)

        # a grid of receptor genes
        cells = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.42, height=0.3, stroke_width=0,
                                          fill_color=RECEPTOR, fill_opacity=0.5)
                         for _ in range(60)]).arrange_in_grid(6, 10, buff=0.12)
        cells.move_to([-3.1, 0.7, 0])
        glab = T("roughly a thousand receptor genes", 24, RECEPTOR).next_to(cells, DOWN, buff=0.3)
        mt = tag("mouse")
        self.play(FadeIn(cells, lag_ratio=0.02), FadeIn(glab), FadeIn(mt), run_time=1.0)

        # one olfactory neuron
        soma = Circle(radius=0.38, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.15)
        soma.move_to([4.0, -1.1, 0])
        dend = Line([4.0, -0.72, 0], [4.0, 0.9, 0], color=TEXT, stroke_width=3)
        knob = Circle(radius=0.1, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.4).move_to([4.0, 0.95, 0])
        cilia = VGroup(*[Line([4.0, 1.0, 0], [4.0 + dx, 1.6, 0], color=GREY, stroke_width=3) for dx in (-0.4, 0, 0.4)])
        nlab = T("olfactory neuron", 22, TEXT).move_to([4.0, -2.0, 0])
        neuron = VGroup(soma, dend, knob, cilia, nlab)
        self.at("most mature olfactory neurons")
        self.play(FadeIn(neuron, shift=UP * 0.2), run_time=0.8)

        self.at("chosen from roughly a thousand")
        pick = cells[23]
        others = VGroup(*[c for i, c in enumerate(cells) if i != 23])
        rec = chip("receptor", RECEPTOR, size=22).move_to([4.0, 2.25, 0])
        self.play(others.animate.set_fill(opacity=0.15), pick.animate.set_fill(opacity=1.0).scale(1.5), run_time=0.7)
        self.play(Transform(pick.copy(), rec), run_time=0.9)
        self.add(rec)

        self.at("statement about genes")
        self.play(Indicate(cells, color=RECEPTOR, scale_factor=1.04), run_time=0.9)
        self.at("many odorants")
        dots = VGroup(*[Dot(radius=0.12, color=ODORANT) for _ in range(3)])
        starts = [np.array([6.2, 3.0, 0]), np.array([6.4, 2.25, 0]), np.array([6.2, 1.5, 0])]
        ends = [np.array([5.05, 2.55, 0]), np.array([5.05, 2.25, 0]), np.array([5.05, 1.95, 0])]
        for d, s in zip(dots, starts):
            d.move_to(s)
        self.add(dots)
        self.play(*[d.animate.move_to(e) for d, e in zip(dots, ends)], run_time=1.0)
        olab = T("odorants", 22, ODORANT).move_to([5.9, 2.25, 0])
        self.play(FadeIn(olab), run_time=0.4)
        self.finish()


class S02Glomeruli(SpokenScene):
    def construct(self):
        epi = RoundedRectangle(corner_radius=0.1, width=11.6, height=0.34, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.3).move_to([0, -2.8, 0])
        epl = T("olfactory epithelium", 22, GREY).move_to([-4.3, -3.4, 0])
        bulb = RoundedRectangle(corner_radius=0.2, width=11.6, height=0.7, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.18).move_to([0, 2.75, 0])
        bl = T("olfactory bulb", 22, GREY).move_to([-4.6, 3.45, 0])
        mt = tag("mouse", 5.6, 3.45)
        gx = [-5.2 + 1.3 * i for i in range(9)]
        gl = VGroup(*[Circle(radius=0.2, stroke_color=GREY, stroke_width=3).move_to([x, 2.62, 0]) for x in gx])
        bx = [-5.5, -3.2, -1.0, 0.8, 3.4, 5.5]            # neurons that share the receptor
        gx_idx = [2, 2, 2, 6, 6, 6]
        greys = [(-4.4, 0), (-2.2, 1), (-0.1, 3), (1.9, 4), (2.6, 5), (4.3, 7), (4.9, 8)]
        gsoma = [Circle(radius=0.15, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5)
                 .move_to([x, -2.4, 0]) for x, _ in greys]
        bsoma = [Circle(radius=0.15, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5)
                 .move_to([x, -2.4, 0]) for x in bx]
        gax = [Line([x, -2.25, 0], [gx[i], 2.42, 0], color=GREY, stroke_width=2, stroke_opacity=0.45) for x, i in greys]
        bax = [Line([x, -2.25, 0], [gx[i], 2.42, 0], color=RECEPTOR, stroke_width=4) for x, i in zip(bx, gx_idx)]
        # greys must be drawn inside the epithelium columns: keep the grey (-6.0) neuron inside the bar
        self.at("Where do their axons go")
        self.play(FadeIn(VGroup(epi, epl, bulb, bl, mt)), FadeIn(gl), FadeIn(VGroup(*gsoma, *bsoma)), run_time=1.0)
        self.play(*[Create(a) for a in gax], run_time=0.8)
        self.at("share one receptor")
        self.play(*[s.animate.set_stroke(RECEPTOR).set_fill(RECEPTOR, 0.9) for s in bsoma], run_time=0.7)
        self.at("converge on two fixed")
        self.play(*[Create(a) for a in bax], run_time=1.6)
        gl_lab = T("two fixed glomeruli", 22, RECEPTOR).move_to([0, 3.45, 0])
        self.play(FadeIn(gl_lab), *[gl[i].animate.set_stroke(RECEPTOR, 5) for i in (2, 6)], run_time=0.6)
        self.at("each glomerulus collects")
        self.play(*[gl[i].animate.set_fill(RECEPTOR, 0.8) for i in (2, 6)], run_time=0.8)
        self.at("map of receptor identity")
        m = bchip("a map of receptor identity", RECEPTOR, 28).move_to([0, 0.2, 0])
        self.play(FadeIn(m), run_time=0.7)
        self.finish()


class S03Matrix(SpokenScene):
    def construct(self):
        tg = T("invented example", 22, GREY).move_to([0, 3.35, 0])
        heads = [header(l) for l in "ABCD"]
        pt = pat_title()
        self.at("Here is an invented example")
        self.play(FadeIn(tg), LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in heads], lag_ratio=0.15), FadeIn(pt),
                  run_time=1.2)
        rows = {}
        for n, key in ((2, "activates B and C"), (3, "activates A B and C")):
            lab, cells, pat = row_label(n), {l: cell(l, n, False) for l in "ABCD"}, pat_text(n)
            rows[n] = (lab, cells, pat)
            self.at(key)
            self.play(FadeIn(lab), *[FadeIn(c) for c in cells.values()], run_time=0.6)
            self.play(*[cells[l].animate.set_fill(ON, 0.9).set_stroke(ON) for l in PAT[n].replace(" ", "")], run_time=0.8)
            self.play(FadeIn(pat), run_time=0.5)
        self.at("One receptor recognized")
        colB = SurroundingRectangle(VGroup(heads[1], rows[2][1]["B"], rows[3][1]["B"]), color=RECEPTOR, buff=0.15, stroke_width=4)
        self.play(Create(colB), run_time=0.7)
        self.at("One odorant was recognized")
        row3 = SurroundingRectangle(VGroup(rows[3][0], *rows[3][1].values()), color=ODORANT, buff=0.15, stroke_width=4)
        self.play(FadeOut(colB), Create(row3), run_time=0.7)
        self.finish()


class S04Remove(SpokenScene):
    def construct(self):
        tg = T("invented example", 22, GREY).move_to([0, 3.35, 0])
        heads = [header(l) for l in "ABCD"]
        pt = pat_title()
        r2, r3 = static_row(2), static_row(3)
        self.add(tg, pt, *heads, r2[0], *r2[1].values(), r2[2], r3[0], *r3[1].values(), r3[2])
        # --- remove A
        self.at("remove receptor")
        cx = xmark([COLX["A"], HEADY], 0.3)
        a3 = r3[1]["A"]
        new3 = pat_text(3, "B C")
        self.play(Create(cx), heads[0].animate.set_opacity(0.3),
                  a3.animate.set_stroke(GONE).set_fill(GONE, 0.0), run_time=0.8)
        self.play(a3.animate.set_stroke(opacity=0.25), Transform(r3[2], new3), run_time=0.7)
        eq = M("=", 44, GONE).move_to([PATX, 0.35, 0])
        self.at("no longer be told apart")
        self.play(FadeIn(eq), run_time=0.5)
        note = T("same pattern: not told apart in this model", 24, TEXT).move_to([0, -3.3, 0])
        self.play(FadeIn(note), run_time=0.5)
        # --- reset, then odorant one
        self.at("activates A and B")
        self.play(FadeOut(eq), FadeOut(note), FadeOut(cx), Transform(heads[0], header("A")),
                  a3.animate.set_stroke(ON, opacity=1.0).set_fill(ON, 0.9),
                  Transform(r3[2], pat_text(3, "A B C")), run_time=0.8)
        lab1 = row_label(1)
        cells1 = {l: cell(l, 1, False) for l in "ABCD"}
        pat1 = pat_text(1, "A B")
        lowlab = T("low concentration", 22, ODORANT).move_to([-5.25, ROWY[1] - 0.5, 0])
        self.play(FadeIn(lab1), FadeIn(lowlab), *[FadeIn(c) for c in cells1.values()], run_time=0.5)
        self.play(*[cells1[l].animate.set_fill(ON, 0.9).set_stroke(ON) for l in "AB"], FadeIn(pat1), run_time=0.7)
        self.at("At tenfold concentration")
        ten = T("tenfold", 22, ODORANT).move_to([-5.4, ROWY[1] - 0.5, 0])
        ring = Circle(radius=0.36, stroke_color=ODORANT, stroke_width=5).move_to([COLX["C"], ROWY[1], 0])
        pat1b = pat_text(1, "A B C")
        self.play(FadeOut(lowlab), FadeIn(ten), cells1["C"].animate.set_fill(ON, 0.9).set_stroke(ON), Create(ring),
                  Transform(pat1, pat1b), run_time=0.8)
        self.at("now matches")
        eq2 = M("=", 44, GONE).move_to([PATX, -1.05, 0])
        self.play(FadeIn(eq2), run_time=0.5)
        self.at("could be mistaken")
        note2 = T("could be mistaken for odorant three, in this model", 24, TEXT).move_to([0, -3.3, 0])
        self.play(FadeIn(note2), run_time=0.5)
        self.at("toy model")
        note3 = T("a toy model, not a count of smells", 24, GREY).move_to([0, -3.3, 0])
        self.play(FadeOut(note2), FadeIn(note3), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------ taste
CX = {"sweet": -5.0, "umami": -2.9, "bitter": -0.8, "sour": 3.2, "salty": 5.3}
CCOL = {"sweet": ORANGE, "umami": PINK, "bitter": PURPLE, "sour": TEXT, "salty": TEXT}
RECS = {"sweet": "T1R2\nT1R3", "umami": "T1R1\nT1R3", "bitter": "T2Rs"}


def taste_cell(k):
    return RoundedRectangle(corner_radius=0.35, width=1.8, height=3.2, stroke_color=CCOL[k], stroke_width=4,
                            fill_color=CCOL[k], fill_opacity=0.1).move_to([CX[k], 0.0, 0])


def cname(k):
    return T(k.upper(), 22, CCOL[k]).move_to([CX[k], -1.95, 0])


def lamp(k, on):
    return Circle(radius=0.26, stroke_color=ON if on else GREY, stroke_width=3,
                  fill_color=ON, fill_opacity=0.95 if on else 0).move_to([CX[k], -2.6, 0])


def recchip(k):
    return chip(RECS[k], RECEPTOR, size=22, pad=0.14).move_to([CX[k], 2.45, 0])


def plc(k):
    return chip("PLCβ2", ENZ, size=22, pad=0.13).move_to([CX[k], 0.1, 0])


class S05Taste(SpokenScene):
    def construct(self):
        mt = tag("mouse", 5.6, 3.45)
        cells = {k: taste_cell(k) for k in ("sweet", "umami", "bitter")}
        names = {k: cname(k) for k in cells}
        lamps = {k: lamp(k, False) for k in cells}
        recs = {k: recchip(k) for k in cells}
        plcs = {k: plc(k) for k in cells}
        cap = T("lit lamp = responds to its tested stimulus", 22, GREY).move_to([0, -3.4, 0])
        self.at("Taste works differently")
        self.play(FadeIn(mt), run_time=0.4)
        self.at("sweet, umami and bitter cells")
        self.play(*[FadeIn(cells[k]) for k in cells], *[FadeIn(names[k]) for k in cells], run_time=0.9)
        self.at("carry different receptors")
        self.play(*[FadeIn(recs[k], shift=DOWN * 0.25) for k in recs], run_time=0.8)
        self.play(*[FadeIn(lamps[k]) for k in lamps], FadeIn(cap), run_time=0.5)
        self.play(*[lamps[k].animate.set_fill(ON, 0.95).set_stroke(ON) for k in lamps], run_time=0.4)
        self.at("share the same steps")
        link = VGroup(Line([CX["sweet"] + 0.85, 0.1, 0], [CX["umami"] - 0.85, 0.1, 0], color=ENZ, stroke_width=3),
                      Line([CX["umami"] + 0.85, 0.1, 0], [CX["bitter"] - 0.85, 0.1, 0], color=ENZ, stroke_width=3))
        self.play(*[FadeIn(plcs[k], scale=0.7) for k in plcs], Create(link), run_time=0.9)
        self.at("what keeps sweet and bitter apart")
        self.play(Indicate(cells["sweet"], color=ORANGE), Indicate(cells["bitter"], color=PURPLE), run_time=1.2)
        self.at("removed")
        xs = {k: xmark([CX[k], 0.1], 0.5) for k in plcs}
        self.play(FadeOut(link), *[Create(xs[k]) for k in xs], *[plcs[k].animate.set_opacity(0.25) for k in plcs], run_time=0.9)
        self.at("responses were lost")
        self.play(*[lamps[k].animate.set_fill(opacity=0).set_stroke(GREY) for k in lamps], run_time=0.8)
        self.at("Sour and salty")
        sc, sn, sl = {}, {}, {}
        for k in ("sour", "salty"):
            sc[k], sn[k], sl[k] = taste_cell(k), cname(k), lamp(k, False)
        self.play(*[FadeIn(sc[k]) for k in sc], *[FadeIn(sn[k]) for k in sn], *[FadeIn(sl[k]) for k in sl], run_time=0.8)
        self.at("were spared")
        self.play(*[sl[k].animate.set_fill(ON, 0.95).set_stroke(ON) for k in sl], run_time=0.6)
        self.finish()


class S06Rescue(SpokenScene):
    def construct(self):
        mt = tag("mouse", 5.6, 3.45)
        ks3 = ("sweet", "umami", "bitter")
        cells = {k: taste_cell(k) for k in CX}
        names = {k: cname(k) for k in CX}
        recs = {k: recchip(k) for k in ks3}
        plcs = {k: plc(k).set_opacity(0.25) for k in ks3}
        xs = {k: xmark([CX[k], 0.1], 0.5) for k in ks3}
        lamps = {k: lamp(k, k in ("sour", "salty")) for k in CX}
        cap = T("lit lamp = responds to its tested stimulus", 22, GREY).move_to([0, -3.4, 0])
        self.add(mt, cap, *cells.values(), *names.values(), *recs.values(), *plcs.values(), *xs.values(), *lamps.values())
        self.at("only in cells")
        fresh = plc("bitter")
        self.play(FadeOut(xs["bitter"]), FadeIn(fresh, scale=1.3), FadeOut(plcs["bitter"]),
                  Indicate(cells["bitter"], color=PURPLE), run_time=0.9)
        self.at("Bitter responses returned")
        self.play(lamps["bitter"].animate.set_fill(ON, 0.95).set_stroke(ON), run_time=0.7)
        self.at("did not")
        self.play(Indicate(lamps["sweet"], color=GREY, scale_factor=1.3), Indicate(lamps["umami"], color=GREY, scale_factor=1.3),
                  run_time=1.0)
        self.at("wired to report")
        rule = T("the cell sets the quality", 30, TEXT).move_to([0, -3.4, 0])
        self.play(FadeOut(cap), FadeIn(rule), run_time=0.6)
        self.at("mouse experiments on the periphery")
        self.play(Indicate(mt, color=TEXT, scale_factor=1.3), run_time=0.8)
        self.at("Smell reads a pattern")
        allm = VGroup(*cells.values(), *names.values(), *recs.values(), *plcs.values(), *xs.values(), *lamps.values(),
                      fresh, rule, mt)
        self.play(FadeOut(allm), run_time=0.7)
        # final split
        sm = chip("SMELL", RECEPTOR, size=34).move_to([-3.3, 2.5, 0])
        ta = chip("TASTE", TEXT, size=34).move_to([3.3, 2.5, 0])
        pat = [[1, 0, 1, 0], [1, 1, 0, 0], [0, 1, 1, 1]]
        grid = VGroup()
        for r in range(3):
            for c in range(4):
                on = pat[r][c]
                grid.add(Circle(radius=0.27, stroke_color=ON if on else GREY, stroke_width=3,
                                fill_color=ON, fill_opacity=0.9 if on else 0).move_to([-4.6 + 0.92 * c, 1.0 - 0.95 * r, 0]))
        sl = T("a pattern across receptors", 26, TEXT).move_to([-3.3, -1.9, 0])
        tc = VGroup(*[RoundedRectangle(corner_radius=0.2, width=0.9, height=2.4, stroke_color=GREY, stroke_width=3)
                      .move_to([1.8 + 1.1 * i, 0.0, 0]) for i in range(4)])
        tc[2].set_stroke(ON).set_fill(ON, 0.9)
        tl = T("which cell fires", 26, TEXT).move_to([3.3, -1.9, 0])
        self.play(FadeIn(sm), FadeIn(grid, lag_ratio=0.05), FadeIn(sl), run_time=1.0)
        self.at("Taste reads which cell fires")
        self.play(FadeIn(ta), FadeIn(tc), FadeIn(tl), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Smell reads a pattern. Taste reads which cell fires."
