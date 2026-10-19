"""Where glia come from: three birthplaces, one name  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = neural tube, radial glia (the CNS stem cell lineage)
  GREEN  = astrocytes, GFAP "on"
  TEAL   = oligodendrocyte lineage (precursors)
  ORANGE = yolk sac and microglia
  PURPLE = neural crest, Schwann cells, satellite glia
  TEXT   = neurons (white)
  PINK   = relay proteins (JAK, STAT3)
  YELLOW = a signal or a mark that is passed on (cytokine, tamoxifen mark, neuregulin, hedgehog)
  RED    = the question, a block, a loss
  GREY   = outlines, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E58FB4"

ROWX = [-4.5, -1.5, 1.5, 4.5]
ROWY = 0.4
KINDS = [("astro", "astrocyte", GREEN), ("oligo", "oligodendrocyte", TEAL),
         ("micro", "microglia", ORANGE), ("schwann", "Schwann cell", PURPLE)]


# ---------------------------------------------------------------- helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def glia(kind, pos=ORIGIN, s=1.0):
    pos = np.array(pos, dtype=float)
    if kind == "astro":
        g = Star(n=7, outer_radius=0.4, inner_radius=0.18, color=GREEN, stroke_width=3,
                 fill_color=GREEN, fill_opacity=0.45)
    elif kind == "oligo":
        arms = [Line(ORIGIN, 0.5 * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)), 0]),
                     color=TEAL, stroke_width=7) for a in (30, 150, 270)]
        body = Circle(radius=0.2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.6)
        g = VGroup(*arms, body)
    elif kind == "micro":
        arms = [Line(ORIGIN, 0.42 * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)), 0]),
                     color=ORANGE, stroke_width=2.5) for a in range(15, 360, 60)]
        body = Circle(radius=0.14, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.8)
        g = VGroup(*arms, body)
    elif kind == "schwann":
        ax = Line([-0.7, 0, 0], [0.7, 0, 0], color=TEXT, stroke_width=3)
        body = RoundedRectangle(corner_radius=0.15, width=0.85, height=0.34, stroke_color=PURPLE, stroke_width=3,
                                fill_color=PURPLE, fill_opacity=0.5)
        g = VGroup(ax, body)
    elif kind == "satellite":
        cell = Circle(radius=0.2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.8)
        dots = [Circle(radius=0.08, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
                .move_to(0.36 * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)), 0])) for a in range(0, 360, 60)]
        g = VGroup(cell, *dots)
    else:
        raise ValueError(kind)
    return g.scale(s).move_to(pos)


def neuron(pos, s=1.0, tail=True):
    body = Circle(radius=0.16, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.85)
    parts = [body]
    if tail:
        parts.append(Line([0.16, 0, 0], [0.5, 0, 0], color=TEXT, stroke_width=3))
    return VGroup(*parts).scale(s).move_to(pos)


def row_cells():
    return [glia(k, [x, ROWY, 0], 2.0) for (k, _, _), x in zip(KINDS, ROWX)]


def row_labels(y=-1.1, size=26):
    return [T(n, size, c).move_to([x, y, 0]) for (_, n, c), x in zip(KINDS, ROWX)]


def row_qs():
    return [T("?", 80, RED, weight=BOLD).move_to([x, 2.2, 0]) for x in ROWX]


class S00Title(TitleCard):
    LESSON = "Where glia come from"
    TITLE = "Three birthplaces, one name"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        emb = Ellipse(width=6.0, height=5.4, stroke_color=GREY, stroke_width=3).move_to([-2.6, -0.2, 0])
        emb_l = T("embryo", 24, GREY).move_to([-2.6, -2.3, 0])
        brain = Circle(radius=1.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                       fill_opacity=0.12).move_to([-2.6, -0.1, 0])
        brain_l = T("brain", 26, BLUE).move_to([-2.6, 0.75, 0])
        mg = glia("micro", [-2.9, -0.5, 0], 1.3)
        self.at("in your brain")
        self.play(FadeIn(emb), FadeIn(emb_l), FadeIn(brain), FadeIn(brain_l), FadeIn(mg, scale=0.5), run_time=0.9)
        self.at("not made by")
        made = T("made here?", 30, RED).move_to([-2.6, 3.0, 0])
        self.play(FadeIn(made), run_time=0.4)
        self.play(Create(Cross(made, stroke_color=RED, stroke_width=6)), run_time=0.5)
        self.at("yolk sac")
        yolk = Ellipse(width=3.8, height=3.4, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                       fill_opacity=0.12).move_to([3.4, -0.2, 0])
        yl = T("yolk sac", 28, ORANGE).move_to([3.4, 1.95, 0])
        cells = [Circle(radius=0.2, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.75)
                 .move_to(p) for p in ([2.7, -0.7, 0], [3.7, 0.2, 0], [3.1, 0.6, 0], [4.1, -0.9, 0])]
        self.play(FadeIn(yolk), FadeIn(yl), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in cells], lag_ratio=0.2), run_time=0.8)
        self.at("outside the embryo")
        out = T("outside the embryo", 24, ORANGE).move_to([3.4, -2.3, 0])
        self.play(FadeIn(out), Indicate(yolk, color=ORANGE, scale_factor=1.03), run_time=0.9)
        self.at("before the brain had")
        tr = cells[0].copy()
        path = ArcBetweenPoints(cells[0].get_center(), np.array([-1.7, -0.5, 0]), angle=-PI / 3)
        self.play(MoveAlongPath(tr, path), run_time=1.6)
        tr2 = glia("micro", tr.get_center(), 1.3)
        self.play(ReplacementTransform(tr, tr2), run_time=0.4)
        self.at("job description")
        cs, ls, qs = row_cells(), row_labels(), row_qs()
        self.play(FadeOut(VGroup(emb, emb_l, brain, brain_l, mg, made, yolk, yl, out, tr2, *cells)),
                  *[FadeOut(m) for m in self.mobjects if isinstance(m, Cross)], run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cs], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(l) for l in ls], lag_ratio=0.15), run_time=1.6)
        self.at("where does each")
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
TC = np.array([-3.2, 0.9, 0])       # neural tube centre
YC = np.array([1.0, 0.9, 0])        # yolk sac centre
CC = np.array([4.6, 1.9, 0])        # crest column: mini tube centre


def pol(c, r, deg):
    return np.array(c) + r * np.array([np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg)), 0])


class S02Three(SpokenScene):
    def construct(self):
        cs, ls, qs = row_cells(), row_labels(), row_qs()
        self.add(*cs, *ls, *qs)
        astro, oligo, micro, schw = cs

        tube = Circle(radius=1.5, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.1).move_to(TC)
        tube_l = T("neural tube", 26, BLUE).move_to([TC[0], -1.0, 0])
        yolk = Ellipse(width=3.2, height=3.0, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                       fill_opacity=0.12).move_to(YC)
        yolk_l = T("yolk sac", 26, ORANGE).move_to([YC[0], -1.0, 0])
        mini = Circle(radius=0.7, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.1).move_to(CC)
        mini_l = T("neural tube", 22, BLUE).move_to([CC[0], 3.2, 0])
        crest_l = T("neural crest", 26, PURPLE).move_to([CC[0], -1.0, 0])

        self.at("Lineage methods")
        self.play(*[FadeOut(q) for q in qs],
                  *[c.animate.scale(0.5).move_to([x, -2.1, 0]) for c, x in zip(cs, ROWX)],
                  *[l.animate.scale(0.85).move_to([x, -3.05, 0]) for l, x in zip(ls, ROWX)],
                  FadeIn(tube), FadeIn(yolk), FadeIn(mini), FadeIn(tube_l), FadeIn(yolk_l), FadeIn(mini_l),
                  FadeIn(crest_l), run_time=1.6)

        # radial glia lines (drawn when named)
        lum = Circle(radius=0.3, stroke_color=GREY, stroke_width=2).move_to(TC)
        rays = VGroup(*[Line(pol(TC, 0.35, a), pol(TC, 1.4, a), color=BLUE, stroke_width=2.5).set_opacity(0.7)
                        for a in range(0, 360, 45)])
        rg_l = T("radial glia", 24, BLUE).move_to([TC[0], 2.8, 0])

        self.at("Astrocytes")
        self.play(astro.animate.scale(1.1).move_to(pol(TC, 0.9, 160)), run_time=0.9)
        self.at("oligodendrocytes")
        self.play(oligo.animate.scale(1.1).move_to(pol(TC, 0.9, 20)), run_time=0.9)
        self.at("radial glia")
        self.play(FadeIn(lum), Create(rays), FadeIn(rg_l), run_time=1.0)
        self.at("also made the neurons")
        ns = [neuron(pol(TC, 0.95, a), 0.8, tail=False) for a in (100, 250, 300)]
        self.play(LaggedStart(*[FadeIn(n, scale=0.4) for n in ns], lag_ratio=0.2), run_time=0.8)
        self.at("Microglia come from")
        self.play(micro.animate.scale(1.6).move_to(YC + np.array([0, 0.1, 0])), run_time=1.0)
        self.at("Schwann cells")
        # crest cells leave the top edges of the mini tube
        dots = VGroup(*[Circle(radius=0.11, stroke_width=0, fill_color=PURPLE, fill_opacity=1).move_to(p)
                        for p in (pol(CC, 0.72, 125), pol(CC, 0.72, 55), pol(CC, 0.72, 160), pol(CC, 0.72, 20))])
        self.play(FadeIn(dots, scale=0.3), run_time=0.25)
        self.play(dots[0].animate.shift(LEFT * 0.9 + DOWN * 1.6), dots[2].animate.shift(LEFT * 0.9 + DOWN * 1.3),
                  dots[1].animate.shift(RIGHT * 0.9 + DOWN * 1.6), dots[3].animate.shift(RIGHT * 0.9 + DOWN * 1.3),
                  schw.animate.scale(1.3).move_to([CC[0] - 0.9, 0.2, 0]), run_time=0.8)
        self.play(FadeOut(dots), run_time=0.2)
        self.at("satellite glia")
        sat = glia("satellite", [CC[0] + 1.1, 0.2, 0], 1.5)
        self.play(FadeIn(sat, scale=0.4), run_time=0.7)
        self.at("closing neural tube")
        self.play(Indicate(mini, color=BLUE, scale_factor=1.2), run_time=1.0)
        self.at("Three birthplaces")
        self.play(Indicate(tube, color=BLUE, scale_factor=1.06), Indicate(yolk, color=ORANGE, scale_factor=1.06),
                  Indicate(VGroup(mini, crest_l), color=PURPLE, scale_factor=1.06), run_time=0.8)
        self.at("one name")
        one = T("one name: glia", 34, TEXT, font=TITLE_FONT).move_to([1.0, 3.1, 0])
        self.play(FadeIn(one, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Switch(SpokenScene):
    def construct(self):
        CX = -4.8
        cell = RoundedRectangle(corner_radius=0.55, width=1.2, height=5.6, stroke_color=BLUE, stroke_width=4,
                                fill_color=BLUE, fill_opacity=0.15).move_to([CX, 0, 0])
        rg_l = T("radial glia", 24, BLUE).move_to([CX, 3.2, 0])
        self.at("neural tube")
        self.play(FadeIn(cell), FadeIn(rg_l), run_time=0.8)

        # phase A: output over time
        ns = [neuron([CX + 0.9, 0.6, 0], 1.8) for _ in range(3)]
        nx = [-2.6, -1.1, 0.4]
        n_l = T("neurons", 30, TEXT).move_to([-1.1, 1.9, 0])
        self.at("make neurons first")
        for n, x in zip(ns, nx):
            self.add(n)
            self.play(n.animate.move_to([x, 0.6, 0]), run_time=0.45)
        self.play(FadeIn(n_l), run_time=0.3)
        self.at("astrocytes appear late")
        asx = [2.0, 3.4, 4.8]
        astros = [glia("astro", [CX + 0.9, 0.6, 0], 1.5) for _ in range(3)]
        a_l = T("astrocytes", 30, GREEN).move_to([3.4, 1.9, 0])
        tline = arr([-3.4, -0.9, 0], [5.6, -0.9, 0], GREY, 4)
        t_l = T("time", 26, GREY).move_to([1.1, -1.5, 0])
        self.play(GrowArrow(tline), FadeIn(t_l), run_time=0.5)
        for a, x in zip(astros, asx):
            self.add(a)
            self.play(a.animate.move_to([x, 0.6, 0]), run_time=0.4)
        self.play(FadeIn(a_l), run_time=0.3)
        self.at("change their output")
        self.play(Indicate(cell, color=BLUE, scale_factor=1.04), run_time=0.8)

        # phase B: the cell grows into the wide cell where the signal runs
        big = RoundedRectangle(corner_radius=0.6, width=7.6, height=4.4, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.1).move_to([-1.0, -0.3, 0])
        big_l = T("radial glial cell", 24, BLUE).move_to([-1.0, -2.85, 0])
        cyt = chip("CNTF", YELLOW, size=26).move_to([-3.6, 3.0, 0])
        self.at("In cultured rodent")
        self.play(FadeOut(VGroup(*ns, *astros, n_l, a_l, tline, t_l)), run_time=0.4)
        self.play(ReplacementTransform(cell, big), ReplacementTransform(rg_l, big_l), run_time=1.0)
        self.at("the cytokine")
        self.play(FadeIn(cyt, shift=DOWN * 0.2), run_time=0.5)
        a1 = arr([-3.6, 2.6, 0], [-3.6, 1.0, 0], YELLOW, 5)
        self.play(GrowArrow(a1), run_time=0.5)
        star = glia("astro", [1.7, 0.95, 0], 1.0)
        star.set_opacity(0.25)
        gf_l = T("GFAP", 24, GREY).move_to([1.7, 0.15, 0])
        self.at("to make")
        self.play(FadeIn(star, scale=0.3), FadeIn(gf_l), run_time=0.6)
        self.at("astrocyte marker")
        self.play(Indicate(gf_l, color=GREY, scale_factor=1.2), run_time=0.7)
        jak = chip("JAK", PINK, size=26).move_to([-3.6, 0.5, 0])
        stat = chip("STAT3", PINK, size=26).move_to([-3.6, -0.9, 0])
        a2 = arr([-3.6, 0.1, 0], [-3.6, -0.5, 0], PINK, 4, 0.18)
        self.at("acts through")
        self.play(FadeOut(a1), FadeIn(jak, scale=0.6), run_time=0.5)
        self.play(FadeIn(a2), FadeIn(stat, scale=0.6), run_time=0.6)
        # nucleus, gene, STAT3 site: methylated (off), then demethylated (can be switched on)
        nuc = Circle(radius=1.25, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([-0.4, -1.0, 0])
        gene = Rectangle(width=2.2, height=0.55, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.25).move_to([-0.35, -0.7, 0])
        gene_l = T("GFAP gene", 20, TEXT).move_to([-0.05, -0.7, 0])
        site = Rectangle(width=0.35, height=0.55, stroke_color=RED, stroke_width=2, fill_color=RED,
                         fill_opacity=0.7).move_to([-1.275, -0.7, 0])
        st_l = VGroup(T("early: site methylated", 22, RED), T("GFAP off", 22, RED)).arrange(DOWN, buff=0.08).move_to([-1.1, 1.15, 0])
        a3 = arr([-2.95, -0.9, 0], [-1.75, -0.75, 0], PINK, 4, 0.18)
        self.at("Early on")
        self.play(FadeIn(nuc), FadeIn(gene), FadeIn(gene_l), FadeIn(site), run_time=0.6)
        self.play(FadeIn(st_l), GrowArrow(a3), run_time=0.7)
        self.at("cannot read")
        self.play(Indicate(site, color=RED, scale_factor=1.3), run_time=0.8)
        self.at("Later")
        st_l2 = VGroup(T("later: site demethylated", 22, GREEN), T("GFAP can be switched on", 22, GREEN)).arrange(DOWN, buff=0.08).move_to([-1.1, 1.15, 0])
        self.play(FadeOut(st_l), run_time=0.25)
        self.play(FadeIn(st_l2), site.animate.set_fill(GREEN, 0.7).set_stroke(GREEN),
                  gene.animate.set_fill(GREEN, 0.4).set_stroke(GREEN), star.animate.set_opacity(1.0),
                  gf_l.animate.set_color(GREEN), run_time=0.8)
        # newborn neurons: a different cytokine, proposed
        CARD = "#9FA8FF"
        nn = [neuron([4.9, y, 0], 1.0, tail=False) for y in (1.0, -0.3, -1.6)]
        nn_l = T("newborn neurons", 24, TEXT).move_to([4.5, 2.2, 0])
        card_l = VGroup(T("cardiotrophin-1", 22, CARD), T("(proposed)", 22, CARD)).arrange(DOWN, buff=0.08).move_to([4.6, -2.5, 0])
        self.at("newborn neurons")
        self.play(FadeIn(nn_l), LaggedStart(*[FadeIn(n, scale=0.4) for n in nn], lag_ratio=0.2), run_time=0.8)
        dots = []
        for n in nn:
            for k in range(2):
                d = Circle(radius=0.1, stroke_width=0, fill_color=CARD, fill_opacity=1).move_to(n.get_center() + LEFT * 0.3)
                dots.append(d)
        anims = [d.animate.move_to(d.get_center() + LEFT * 1.5) for d in dots]
        self.at("different cytokine")
        self.play(FadeIn(card_l), *[FadeIn(d) for d in dots], run_time=0.3)
        self.play(*anims, run_time=1.0)
        self.play(*[FadeOut(d) for d in dots], run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Olig(SpokenScene):
    def construct(self):
        SX = -3.9
        ys = [-1.95, -1.05, -0.15, 0.75]
        fp = Rectangle(width=2.6, height=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                       fill_opacity=0.5).move_to([SX, -2.9, 0])
        fp_l = T("floor plate", 22, TEXT).move_to(fp)
        bars = [Rectangle(width=2.6, height=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.15).move_to([SX, y, 0]) for y in ys]
        pmn = bars[1]
        pmn_l = T("pMN: Olig2", 24, BLUE).move_to(pmn)
        dom_l = T("progenitor domains", 24, GREY).move_to([SX, 2.4, 0])
        self.at("Oligodendrocytes start")
        self.play(FadeIn(fp), FadeIn(fp_l), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars], lag_ratio=0.15), run_time=1.0)
        self.at("Sonic hedgehog")
        hh = arr([-5.75, -2.9, 0], [-5.75, 0.9, 0], YELLOW, 6)
        hh_l = T("Sonic hedgehog", 24, YELLOW).move_to([-4.9, 1.6, 0])
        self.play(GrowArrow(hh), FadeIn(hh_l), run_time=1.0)
        self.at("progenitor domains")
        self.play(FadeIn(dom_l), run_time=0.5)
        self.at("One of them")
        self.play(pmn.animate.set_stroke(BLUE).set_fill(BLUE, 0.35), FadeIn(pmn_l), run_time=0.8)
        # outputs
        mns = [neuron([-2.5, -1.05, 0], 1.6) for _ in range(3)]
        mx = [-1.0, 0.3, 1.6]
        mn_l = T("motor neurons", 26, TEXT).move_to([0.3, -0.05, 0])
        first = T("first", 26, GREY).move_to([0.3, -2.05, 0])
        opcs = [glia("oligo", [-2.5, -1.05, 0], 1.2) for _ in range(3)]
        ox = [3.4, 4.6, 5.8]
        op_l = VGroup(T("oligodendrocyte", 26, TEAL), T("precursors", 26, TEAL)).arrange(DOWN, buff=0.08).move_to([4.6, 0.0, 0])
        then = T("then", 26, GREY).move_to([4.6, -2.05, 0])
        sp = T("mouse and chick", 22, GREY).move_to([4.6, 2.5, 0])
        self.at("mice and chicks")
        self.play(FadeIn(sp), run_time=0.4)
        self.at("first makes motor neurons")
        for n, x in zip(mns, mx):
            self.add(n)
            self.play(n.animate.move_to([x, -1.05, 0]), run_time=0.4)
        self.play(FadeIn(mn_l), FadeIn(first), run_time=0.3)
        self.at("then oligodendrocyte")
        for o, x in zip(opcs, ox):
            self.add(o)
            self.play(o.animate.move_to([x, -1.05, 0]), run_time=0.4)
        self.play(FadeIn(op_l), FadeIn(then), run_time=0.3)
        # mutant: reset every result before the new case
        self.at("lacking both")
        case = T("Olig1 and Olig2 removed", 26, RED).move_to([1.6, 2.0, 0])
        x_pmn = Cross(pmn, stroke_color=RED, stroke_width=6)
        self.play(FadeOut(VGroup(*mns, *opcs, mn_l, op_l, first, then, sp)),
                  pmn.animate.set_stroke(GREY).set_fill(GREY, 0.1), pmn_l.animate.set_color(GREY),
                  FadeIn(case), Create(x_pmn), run_time=1.0)
        d1 = DashedVMobject(Circle(radius=0.4, color=GREY, stroke_width=3), num_dashes=14).move_to([0.3, -1.05, 0])
        d2 = DashedVMobject(Circle(radius=0.4, color=GREY, stroke_width=3), num_dashes=14).move_to([4.6, -1.05, 0])
        self.at("no spinal motor neurons")
        l1 = T("almost no motor neurons", 26, RED).move_to([0.3, -0.05, 0])
        self.play(FadeIn(d1), Create(Cross(d1, stroke_color=RED, stroke_width=5)), FadeIn(l1), run_time=0.8)
        self.at("no spinal oligodendrocytes")
        l2 = VGroup(T("no oligodendrocytes", 24, RED)).move_to([4.5, -0.05, 0])
        self.play(FadeIn(d2), Create(Cross(d2, stroke_color=RED, stroke_width=5)), FadeIn(l2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Micro(SpokenScene):
    def construct(self):
        YX, YY = -3.6, 0.5
        yolk = Ellipse(width=4.4, height=3.4, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                       fill_opacity=0.12).move_to([YX, YY, 0])
        yl = T("yolk sac", 28, ORANGE).move_to([YX, -1.6, 0])
        pos = [[YX - 1.2, YY + 0.5], [YX - 0.3, YY + 0.9], [YX + 0.9, YY + 0.5], [YX - 0.8, YY - 0.5],
               [YX + 0.2, YY - 0.2], [YX + 1.2, YY - 0.6]]
        cells = [Circle(radius=0.27, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.7)
                 .move_to([p[0], p[1], 0]) for p in pos]
        self.at("odd ones out")
        self.play(FadeIn(yolk), FadeIn(yl), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in cells], lag_ratio=0.12), run_time=0.8)
        tam = chip("tamoxifen", YELLOW, size=28).move_to([0.2, 2.7, 0])
        self.at("one dose")
        self.play(FadeIn(tam, shift=DOWN * 0.2), run_time=0.5)
        ta = arr([-1.1, 2.55, 0], [-2.2, 1.7, 0], YELLOW, 5)
        self.play(GrowArrow(ta), run_time=0.4)
        day = M("embryonic day 7.5", 26, GREY).move_to([YX, 2.75, 0])
        mouse_t = T("mouse, about", 24, GREY).move_to([YX, 3.25, 0])
        self.at("embryonic day")
        self.play(FadeIn(day), FadeIn(mouse_t), *[c.animate.set_fill(YELLOW, 0.95).set_stroke(YELLOW) for c in cells], run_time=0.8)
        leg_dot = Circle(radius=0.16, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95)
        leg_t = T("marked", 26, YELLOW)
        leg = VGroup(leg_dot, leg_t).arrange(RIGHT, buff=0.2).move_to([YX, -2.4, 0])
        self.at("permanently marked")
        self.play(FadeOut(tam), FadeOut(ta), FadeIn(leg), run_time=0.7)
        self.at("all their descendants")
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.3) for c in cells], run_time=0.9)
        # adult rows
        mg_l = T("adult microglia", 28, ORANGE).move_to([2.8, 2.1, 0])
        bl_l = T("adult blood cells", 28, GREY).move_to([2.8, -0.3, 0])

        def dotrow(n, x0, dx, y, base, r):
            return [Circle(radius=r, stroke_color=base, stroke_width=3, fill_color=base,
                           fill_opacity=0.25).move_to([x0 + dx * i, y, 0]) for i in range(n)]

        mrow = dotrow(9, -0.2, 0.75, 1.2, ORANGE, 0.22)
        brow = dotrow(20, -0.2, 0.31, -1.2, GREY, 0.12)
        illus = T("illustrative counts", 22, GREY).move_to([4.4, 2.9, 0])
        self.at("In adults")
        self.play(FadeIn(mg_l), FadeIn(illus), LaggedStart(*[FadeIn(d, scale=0.3) for d in mrow], lag_ratio=0.06), run_time=1.0)
        self.at("about a third")
        self.play(*[mrow[i].animate.set_fill(YELLOW, 0.95).set_stroke(YELLOW) for i in (1, 4, 7)], run_time=0.8)
        self.at("Very few blood cells")
        self.play(FadeIn(bl_l), LaggedStart(*[FadeIn(d, scale=0.3) for d in brow], lag_ratio=0.03), run_time=1.0)
        self.play(brow[11].animate.set_fill(YELLOW, 0.95).set_stroke(YELLOW), run_time=0.5)
        # new case: reset everything, then the brain
        brain = Circle(radius=1.6, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.12).move_to([3.4, 0.2, 0])
        brain_l = T("brain", 28, BLUE).move_to([3.4, 1.1, 0])
        nohb = T("no heartbeat", 30, RED).move_to([0.3, 2.7, 0])
        self.at("without a heartbeat")
        self.play(FadeOut(VGroup(*mrow, *brow, mg_l, bl_l, day, leg, mouse_t, illus)),
                  *[c.animate.set_fill(ORANGE, 0.7).set_stroke(ORANGE) for c in cells],
                  FadeIn(brain), FadeIn(brain_l), FadeIn(nohb), run_time=1.0)
        self.at("macrophages")
        self.play(Indicate(VGroup(*cells), color=ORANGE, scale_factor=1.15), run_time=0.8)
        nomg = T("no microglia", 28, RED).move_to([3.4, -0.4, 0])
        self.at("no brain microglia")
        self.play(FadeIn(nomg), run_time=0.4)
        # circulation case
        self.at("travel in")
        route_a = ArcBetweenPoints(np.array([-1.3, 1.5, 0]), np.array([1.9, 0.7, 0]), angle=-PI / 4)
        route = DashedVMobject(route_a.copy().set_stroke(ORANGE, 4), num_dashes=22)
        circ = T("early circulation", 26, ORANGE).move_to([0.3, 2.0, 0])
        self.play(FadeOut(nohb), FadeOut(nomg), Create(route), FadeIn(circ), run_time=0.9)
        movers = [cells[1].copy(), cells[2].copy()]
        self.add(*movers)
        self.play(LaggedStart(*[MoveAlongPath(m, route_a.copy()) for m in movers], lag_ratio=0.35), run_time=2.0)
        mg = [glia("micro", [3.0, -0.2, 0], 1.5), glia("micro", [4.1, -0.9, 0], 1.5)]
        self.play(FadeOut(VGroup(*movers)), *[FadeIn(m, scale=0.4) for m in mg], run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def prec(pos, s=1.0):
    body = RoundedRectangle(corner_radius=0.13, width=0.7, height=0.28, stroke_color=PURPLE, stroke_width=3,
                            fill_color=PURPLE, fill_opacity=0.5)
    return VGroup(body).scale(s).move_to(pos)


class S06Schwann(SpokenScene):
    def construct(self):
        tag = T("peripheral nervous system", 24, GREY).move_to([0, 3.3, 0])
        c1 = chip("crest cell", PURPLE, size=22)
        c2 = chip("Schwann cell precursor", PURPLE, size=22)
        c3 = chip("immature Schwann cell", PURPLE, size=22)
        chain = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.95).move_to([0, 2.5, 0])
        ar1 = arr(c1.get_right() + RIGHT * 0.08, c2.get_left() + LEFT * 0.08, PURPLE, 4, 0.18)
        ar2 = arr(c2.get_right() + RIGHT * 0.08, c3.get_left() + LEFT * 0.08, PURPLE, 4, 0.18)
        self.at("peripheral nervous system")
        self.play(FadeIn(tag), run_time=0.6)
        self.at("neural crest")
        self.play(FadeIn(c1, scale=0.7), run_time=0.5)
        self.at("then Schwann cell precursor")
        self.play(GrowArrow(ar1), FadeIn(c2, scale=0.7), run_time=0.6)
        self.at("immature")
        self.play(GrowArrow(ar2), FadeIn(c3, scale=0.7), run_time=0.6)
        # dishes
        DY = -0.7
        d1 = RoundedRectangle(corner_radius=0.3, width=5.4, height=3.6, stroke_color=GREY, stroke_width=3).move_to([-3.1, DY, 0])
        d2 = RoundedRectangle(corner_radius=0.3, width=5.4, height=3.6, stroke_color=GREY, stroke_width=3).move_to([3.0, DY, 0])
        d1_l = T("alone", 26, GREY).move_to([-3.1, DY + 2.15, 0])
        d2_l = T("with neurons", 26, GREY).move_to([3.0, DY + 2.15, 0])
        p1 = prec([-3.1, DY, 0], 1.9)
        p2 = prec([1.4, DY, 0], 1.9)
        nb = neuron([4.9, DY, 0], 1.9, tail=False)
        axon = Line([4.7, DY, 0], [0.5, DY, 0], color=TEXT, stroke_width=3)
        axon.set_z_index(0)
        p2.set_z_index(2)
        self.at("In culture")
        self.play(FadeIn(d1), FadeIn(d1_l), FadeIn(p1, scale=0.5), run_time=0.7)
        self.at("die")
        x1 = Cross(p1, stroke_color=RED, stroke_width=6, scale_factor=1.4)
        self.play(p1.animate.set_opacity(0.25), Create(x1), run_time=0.8)
        self.at("neurons are present")
        self.play(FadeIn(d2), FadeIn(d2_l), FadeIn(axon), FadeIn(nb), FadeIn(p2, scale=0.5), run_time=0.9)
        nrg_l = T("neuregulin", 26, YELLOW).move_to([3.0, DY - 1.35, 0])
        dots = [Circle(radius=0.12, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([3.9 - 0.6 * k, DY + 0.3, 0])
                for k in range(3)]
        self.at("a growth factor")
        self.play(FadeIn(nrg_l), *[FadeIn(d, scale=0.3) for d in dots], run_time=0.6)
        self.play(*[d.animate.shift(LEFT * 0.9) for d in dots], run_time=0.9)
        self.at("keep them alive")
        self.play(Indicate(p2, color=GREEN, scale_factor=1.2), run_time=1.0)
        # nerve case: reset everything first
        ys = [0.6, -0.5, -1.6, -2.7]
        axons = [Line([-5.8, y, 0], [5.8, y, 0], color=TEXT, stroke_width=4).set_opacity(0.8) for y in ys]
        pxy = [(-4.4, 0.6), (-1.6, -0.5), (1.2, -1.6), (3.6, 0.6), (4.6, -2.7), (-3.0, -2.7), (-0.2, 0.6), (2.0, -0.5)]
        precs = [prec([x, y, 0], 1.7) for x, y in pxy]
        n_l = T("mouse nerve", 28, GREY).move_to([0, 1.7, 0])
        self.at("Mice without")
        self.play(FadeOut(VGroup(d1, d2, d1_l, d2_l, p1, p2, x1, axon, nb, nrg_l, *dots, chain, ar1, ar2)),
                  FadeIn(n_l), *[FadeIn(a) for a in axons], *[FadeIn(p, scale=0.5) for p in precs], run_time=0.9)
        gone = T("without ErbB3", 28, RED).move_to([0, 1.7, 0])
        self.at("lack precursors")
        self.play(ReplacementTransform(n_l, gone), *[FadeOut(p) for p in precs], run_time=0.9)
        # the rule
        k1 = chip("where it was born", BLUE, size=32)
        k2 = chip("which signal it needs", YELLOW, size=32)
        keep = VGroup(k1, k2).arrange(DOWN, buff=0.6).move_to([0, 0.0, 0])
        self.at("So ask")
        self.play(FadeOut(VGroup(*axons, gone, tag)), run_time=0.6)
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.7)
        self.at("which signal")
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Ask where a glial cell was born, and which signal it needs."
