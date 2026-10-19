"""Where the touch change begins  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept, whole film)
  BLUE   = the primary sensory neuron (the peripheral cell)
  YELLOW = the air puff (the stimulus)
  GREY   = skin, spinal cord, brain: structure and boxes
  RED    = gene deleted / not rescued / missing
  GREEN  = gene present or restored / rescued
  PURPLE = GABA-A receptors and GABA inhibition
  ORANGE = the behavioural readout (startle-like movement, assays)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def box(label, w, h, color=GREY, size=24, fill=0.12):
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=fill)
    t = T(label, size, color)
    return VGroup(r, t.move_to(r))


def arrow(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhibit(a, b, color=PURPLE, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.06
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def pathway(cy=1.3, scale=1.0):
    """skin | sensory neuron | spinal cord | brain, left to right. Returns a VGroup with named parts."""
    skin = box("skin", 1.9, 1.5).move_to([-5.2, cy, 0])
    skin_lbl = T("mouse", 22, GREY).next_to(skin, DOWN, buff=0.12)
    ending = Circle(radius=0.14, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.9).move_to([-4.0, cy, 0])
    axon1 = Line([-3.86, cy, 0], [-2.0, cy, 0], color=BLUE, stroke_width=5)
    stem = Line([-2.0, cy, 0], [-2.0, cy + 0.7, 0], color=BLUE, stroke_width=5)
    soma = Circle(radius=0.5, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to([-2.0, cy + 1.2, 0])
    axon2 = Line([-2.0, cy, 0], [0.6, cy, 0], color=BLUE, stroke_width=5)
    cord = box("", 3.3, 1.5, GREY, fill=0.08).move_to([1.9, cy, 0])
    cord_lbl = T("spinal dorsal horn", 22, GREY).next_to(cord, DOWN, buff=0.12)
    term = Ellipse(width=0.8, height=0.55, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to([0.9, cy, 0])
    brain = box("brain", 1.9, 1.5).move_to([5.2, cy, 0])
    onward = DashedLine([3.6, cy, 0], [4.2, cy, 0], color=GREY, stroke_width=4)
    nlbl = T("sensory neuron", 24, BLUE).next_to(soma, RIGHT, buff=0.4)
    g = VGroup(skin, skin_lbl, ending, axon1, stem, soma, axon2, cord, cord_lbl, term, brain, onward, nlbl)
    g.skin, g.skin_lbl, g.ending, g.soma, g.term, g.brain, g.cord, g.nlbl, g.cord_lbl, g.onward = \
        skin, skin_lbl, ending, soma, term, brain, cord, nlbl, cord_lbl, onward
    g.axons = VGroup(axon1, stem, axon2)
    g.cy = cy
    return g


def bar(h, color, w=0.9, base=None):
    r = Rectangle(width=w, height=max(h, 0.02), stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.4)
    if base is not None:
        r.move_to(base, aligned_edge=DOWN)
    return r


class S00Title(TitleCard):
    LESSON = "Touch over-reactivity in autism models"
    TITLE = "Where the touch change begins"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        p = pathway(cy=1.0)
        ob = T("Orefice and colleagues, 2016", 24, GREY).move_to([3.6, -0.5, 0])
        qn = T("?", 60, YELLOW, weight=BOLD).move_to(p.soma.get_center())
        qb = T("?", 60, YELLOW, weight=BOLD).move_to(p.brain.get_center() + UP * 0.0)
        self.at("Does a mouse react more")
        self.play(FadeIn(p.skin), FadeIn(p.skin_lbl), FadeIn(p.brain), FadeIn(p.cord), FadeIn(p.cord_lbl), run_time=0.8)
        self.at("because of its brain")
        self.play(Indicate(p.brain, color=YELLOW, scale_factor=1.08), FadeIn(qb), run_time=1.0)
        self.at("the first neuron")
        self.play(FadeOut(qb), FadeIn(p.axons), FadeIn(p.ending), FadeIn(p.soma), FadeIn(p.term), FadeIn(p.nlbl),
                  FadeIn(qn), FadeIn(p.onward), run_time=1.0)
        self.play(Indicate(p.soma, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("mutations in genes")
        self.play(FadeOut(qn), FadeIn(ob), run_time=0.4)
        # puff
        puff = VGroup(*[arrow([-6.4 + 0.0, 3.6 - 0.3 * k, 0], [-5.4, 3.6 - 0.3 * k, 0], YELLOW, w=3, tip=0.12) for k in range(0)])
        pa = arrow([-5.2, 3.3, 0], [-5.2, p.cy + 0.85, 0], YELLOW, w=7, tip=0.25)
        pl = T("air puff: 0.9 psi, 50 ms, back hairy skin", 24, YELLOW).move_to([-1.0, 3.5, 0])
        self.at("The puff was fixed")
        self.play(GrowArrow(pa), FadeIn(pl), run_time=0.8)
        self.at("size of a startle")
        base = np.array([-3.4, -3.1, 0])
        bc = bar(0.9, ORANGE).move_to(base, aligned_edge=DOWN)
        lc = T("control", 22, GREY).next_to(bc, DOWN, buff=0.12)
        ax = Line([-4.3, -3.1, 0], [-2.5, -3.1, 0], color=GREY, stroke_width=3)
        title = T("startle-like movement, in this sketch", 24, ORANGE).move_to([-3.0, -0.7, 0])
        self.play(FadeIn(bc), FadeIn(lc), Create(ax), FadeIn(title), run_time=0.8)
        self.at("All four mouse lines")
        names = ["Mecp2-null", "Mecp2 R306C", "Shank3B heterozygous", "Fmr1-null"]
        chips = VGroup(*[chip(n, GREY, size=22, pad=0.15) for n in names]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        chips.move_to([3.6, -2.2, 0])
        mb = bar(1.7, ORANGE, w=0.9).move_to([-1.6, -3.1, 0], aligned_edge=DOWN)
        ml = T("mouse line", 22, GREY).next_to(mb, DOWN, buff=0.12)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in chips], lag_ratio=0.25), run_time=1.0)
        self.play(FadeIn(mb, shift=UP * 0.2), FadeIn(ml), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Restrict(SpokenScene):
    def construct(self):
        p = pathway(cy=0.5)
        self.add(p)
        gene_n = chip("Mecp2 or Gabrb3", GREEN, size=24, pad=0.14).next_to(p.soma, LEFT, buff=0.35)
        gene_b = chip("same gene", GREEN, size=24, pad=0.14).next_to(p.brain, UP, buff=0.3)
        gene_s = chip("same gene", GREEN, size=22, pad=0.14).next_to(p.skin, UP, buff=0.3)
        self.at("Then came the restriction")
        self.play(FadeIn(gene_n, shift=RIGHT * 0.2), FadeIn(gene_b, shift=DOWN * 0.2), run_time=0.8)
        cre = chip("Advillin-Cre", BLUE, size=24, pad=0.14).move_to([-3.4, 3.2, 0])
        self.at("Cree supplies")
        self.play(FadeIn(cre, shift=DOWN * 0.2), run_time=0.6)
        halo = Circle(radius=0.68, stroke_color=BLUE, stroke_width=5).move_to(p.soma)
        cap = VGroup(T("peripheral sensory neurons:", 24, BLUE), T("dorsal root, trigeminal; also sympathetic ganglia", 22, BLUE)).arrange(DOWN, buff=0.1).move_to([-2.6, -1.5, 0])
        self.at("peripheral sensory neurons")
        self.play(Create(halo), FadeIn(cap), cre.animate.next_to(halo, UP, buff=0.25), run_time=0.9)
        self.at("not one subtype")
        self.wait(0.1)
        self.at("Crossed to a floxed allele")
        fl = T("floxed allele", 24, GREEN)
        self.play(Indicate(gene_n, color=GREEN, scale_factor=1.1), run_time=0.7)
        self.at("it removes that gene")
        cross = Cross(gene_n[0], stroke_color=RED, stroke_width=6)
        self.play(gene_n[0].animate.set_stroke(RED).set_fill(RED, 0.16), gene_n[1].animate.set_color(RED), Create(cross), run_time=0.8)
        dele = T("deleted in the sensory neuron", 24, RED).next_to(p.soma, LEFT, buff=0.1).shift(DOWN * 1.5 + LEFT * 0.0)
        dele.move_to([-3.6, 3.15 - 0.0, 0]); dele.shift(DOWN * 0.0)
        self.play(FadeIn(T("deleted in peripheral neurons", 24, RED).move_to([-3.6, -2.4, 0])), run_time=0.5)
        self.at("The brain keeps its copy")
        keep = T("brain: gene intact", 24, GREEN).next_to(p.brain, DOWN, buff=0.45).shift(DOWN * 0.45 + LEFT * 0.5)
        self.play(Indicate(gene_b, color=GREEN, scale_factor=1.15), FadeIn(keep), run_time=0.9)
        self.at("two genes")
        self.play(Indicate(gene_n, color=RED, scale_factor=1.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Enough(SpokenScene):
    def construct(self):
        p = pathway(cy=0.0).scale(0.85).shift(UP * 2.0)
        self.add(p)
        gene = chip("gene deleted", RED, size=22, pad=0.12).next_to(p.soma, LEFT, buff=0.25)
        self.add(gene)
        ctrl_b = bar(0.9, ORANGE, w=1.0).move_to([-4.6, -3.2, 0], aligned_edge=DOWN)
        ctrl_l = T("control", 22, GREY).next_to(ctrl_b, DOWN, buff=0.1)
        base = Line([-5.6, -3.2, 0], [-3.6, -3.2, 0], color=GREY, stroke_width=3)
        cap = T("air-puff response, in this sketch", 22, ORANGE).move_to([-4.6, -0.0, 0])
        self.add(ctrl_b, ctrl_l, base)
        self.at("stronger air puff responses")
        del_b = bar(1.7, ORANGE, w=1.0).move_to([-2.9, -3.2, 0], aligned_edge=DOWN)
        del_l = T("deleted", 22, RED).next_to(del_b, DOWN, buff=0.1)
        self.play(FadeIn(cap), FadeIn(del_b, shift=UP * 0.3), FadeIn(del_l), run_time=0.9)
        self.at("It was also sufficient")
        c1 = chip("anxiety-like differences", ORANGE, size=24).move_to([3.0, -0.2, 0])
        c2 = chip("social-interaction differences", ORANGE, size=24).move_to([3.0, -1.2, 0])
        c3 = T("in the assays tested", 22, GREY).next_to(c2, DOWN, buff=0.25)
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.6)
        self.play(FadeIn(c2, shift=LEFT * 0.2), FadeIn(c3), run_time=0.6)
        self.at("Sufficient does not")
        w = T("sufficient = enough to produce the change", 28, TEXT).move_to([2.2, -2.5, 0])
        self.play(FadeIn(w), run_time=0.7)
        self.at("the whole story")
        nw = T("not the whole story", 28, RED).move_to([2.2, -3.3, 0])
        self.play(FadeIn(nw, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Restore(SpokenScene):
    def construct(self):
        p = pathway(cy=0.0).scale(0.85).shift(UP * 2.0)
        self.add(p)
        gene = chip("gene deleted", RED, size=22, pad=0.12).next_to(p.soma, LEFT, buff=0.25)
        self.add(gene)
        self.at("The reverse test")
        gene2 = chip("Mecp2 restored", GREEN, size=22, pad=0.12).move_to(gene)
        gb = chip("all other cells: Mecp2 null", GREY, size=22, pad=0.12).next_to(p.brain, DOWN, buff=0.3)
        self.play(ReplacementTransform(gene, gene2), FadeIn(gb), run_time=0.9)
        left = VGroup(T("rescued", 30, GREEN, weight=BOLD)).move_to([-3.3, 0.2, 0])
        right = VGroup(T("not rescued", 30, RED, weight=BOLD)).move_to([3.3, 0.2, 0])
        self.at("Tactile sensitivity was rescued")
        self.play(FadeIn(left), run_time=0.4)
        r1 = chip("tactile sensitivity", GREEN, size=24).move_to([-3.3, -0.8, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.5)
        self.at("so were selected")
        r2 = chip("selected anxiety-like and social measures", GREEN, size=22).move_to([-3.3, -1.9, 0])
        fit(r2, max_w=5.8)
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.6)
        self.at("Lethality")
        self.play(FadeIn(right), run_time=0.4)
        n1 = chip("lethality", RED, size=24).move_to([3.3, -0.8, 0])
        self.play(FadeIn(n1, shift=UP * 0.15), run_time=0.4)
        self.at("memory deficits")
        n2 = chip("memory deficits", RED, size=24).move_to([3.3, -1.9, 0])
        self.play(FadeIn(n2, shift=UP * 0.15), run_time=0.4)
        self.at("motor deficits")
        n3 = chip("motor deficits", RED, size=24).move_to([3.3, -3.0, 0])
        self.play(FadeIn(n3, shift=UP * 0.15), run_time=0.4)
        self.at("explains part of the phenotype")
        self.play(Indicate(VGroup(left, r1, r2), color=GREEN, scale_factor=1.04), run_time=0.8)
        self.at("not the rest")
        self.play(Indicate(VGroup(right, n1, n2, n3), color=RED, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Terminal(SpokenScene):
    def construct(self):
        hdr = T("in mouse dorsal horn", 28, GREY).move_to([-3.0, 2.95, 0])
        cord = box("", 12.2, 5.4, GREY, fill=0.06).move_to([0, -0.4, 0])
        cx, cy = -1.8, 0.1
        axon = Line([-6.1, cy, 0], [cx - 2.0, cy, 0], color=BLUE, stroke_width=7)
        term = Ellipse(width=4.0, height=2.6, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to([cx, cy, 0])
        tl = T("central terminal", 26, BLUE).move_to(term)
        tl2 = T("Aβ / Aδ LTMR afferent", 24, BLUE).next_to(term, DOWN, buff=0.2)
        self.at("In mouse dorsal horn")
        self.play(FadeIn(hdr), FadeIn(cord), Create(axon), FadeIn(term), FadeIn(tl), run_time=1.0)
        recs = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.5, height=0.3, stroke_color=PURPLE, stroke_width=3,
                                         fill_color=PURPLE, fill_opacity=0.5) for _ in range(5)])
        for r, x in zip(recs, np.linspace(-1.3, 1.3, 5)):
            r.move_to([cx + x, cy + 1.3 * np.sqrt(max(0.0, 1 - (x / 2.0) ** 2)), 0])
        rl = T("GABRB3-containing GABA-A receptors", 24, PURPLE).move_to([cx, 2.95, 0])
        self.at("sit on the central terminals")
        self.play(FadeIn(recs, shift=DOWN * 0.1), FadeIn(rl), FadeOut(hdr), run_time=0.9)
        self.play(FadeIn(tl2), run_time=0.5)
        self.at("puncta next to")
        bx, by = 3.5, -1.6
        bc = bar(1.6, PURPLE, w=0.8).move_to([bx - 1.0, by, 0], aligned_edge=DOWN)
        bm = bar(0.48, PURPLE, w=0.8).move_to([bx + 1.0, by, 0], aligned_edge=DOWN)
        base = Line([bx - 1.9, by, 0], [bx + 1.9, by, 0], color=GREY, stroke_width=3)
        l1 = T("control", 22, GREY).next_to(base, DOWN, buff=0.1).set_x(bx - 1.0)
        l2 = VGroup(T("Mecp2", 22, RED), T("mutant", 22, RED)).arrange(DOWN, buff=0.05).next_to(base, DOWN, buff=0.1).set_x(bx + 1.0)
        bt = T("puncta, relative", 22, PURPLE).move_to([bx, by + 2.1, 0])
        self.play(FadeIn(bc), FadeIn(base), FadeIn(l1), FadeIn(bt), run_time=0.6)
        self.play(FadeIn(bm), FadeIn(l2), recs.animate.set_opacity(0.2), run_time=0.9)
        note = T("about 70 per cent fewer, fixed tissue", 22, RED).move_to([3.0, -2.95, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.at("authors attributed")
        self.play(FadeOut(bt), run_time=0.2)
        g = chip("GABA", PURPLE, size=26).move_to([-4.9, 1.6, 0])
        inh = inhibit([-4.2, 1.5, 0], [cx - 1.15, 1.2, 0])
        itl = T("presynaptic inhibition", 24, PURPLE).move_to([-4.0, 2.95, 0])
        self.play(FadeOut(rl), recs.animate.set_opacity(0.5), run_time=0.3)
        self.play(FadeIn(g), Create(inh), FadeIn(itl), run_time=0.8)
        self.at("such a terminal")
        dep = T("GABA depolarises the terminal", 24, TEXT).move_to([-2.9, -2.2, 0])
        rel = T("the study reads this as reducing release", 24, TEXT).next_to(dep, DOWN, buff=0.15)
        self.play(FadeIn(dep), run_time=0.6)
        self.play(FadeIn(rel), run_time=0.6)
        self.at("not the same as exciting")
        self.play(Indicate(VGroup(dep, rel), color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Limits(SpokenScene):
    def construct(self):
        top = box("same air-puff behaviour", 6.0, 0.8, ORANGE, size=28).move_to([0, 3.0, 0])
        cardA = box("", 5.6, 3.4, GREY, fill=0.08).move_to([-3.3, 0.4, 0])
        cardB = box("", 5.6, 3.4, GREY, fill=0.08).move_to([3.3, 0.4, 0])
        ta = T("Gabrb3 and Mecp2 models", 24, TEXT, weight=BOLD).move_to([-3.3, 1.6, 0])
        da = chip("fewer GABRB3 puncta at terminals", PURPLE, size=22).move_to([-3.3, 0.6, 0])
        fit(da, max_w=5.2)
        tb = T("Shank3 mutants", 24, TEXT, weight=BOLD).move_to([3.3, 1.75, 0])
        mem = RoundedRectangle(corner_radius=0.08, width=4.2, height=0.28, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.4).move_to([3.3, 0.7, 0])
        ih = chip("Ih reduced", RED, size=22, pad=0.1).next_to(mem, DOWN, buff=0.2).shift(LEFT * 1.1)
        ex = chip("excitability higher", ORANGE, size=22, pad=0.1).next_to(mem, DOWN, buff=0.2).shift(RIGHT * 1.2)
        ntc = VGroup(T("cultured large dorsal root ganglion", 22, GREY), T("neurons; no altered GABRB3", 22, GREY), T("at terminals", 22, GREY)).arrange(DOWN, buff=0.05).move_to([3.3, -0.72, 0])
        mlb = T("membrane", 22, GREY).next_to(mem, UP, buff=0.05)
        self.at("One model does not fit")
        self.play(FadeIn(top), FadeIn(cardA), FadeIn(ta), FadeIn(da), run_time=0.9)
        self.at("cultured large dorsal")
        self.play(FadeIn(cardB), FadeIn(tb), FadeIn(mem), FadeIn(mlb), run_time=0.6)
        self.at("was reduced")
        self.play(FadeIn(ih, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(ntc), run_time=0.5)
        self.at("different cellular defect")
        ar1 = arrow([-3.3, 2.0, 0], [-1.2, 2.55, 0], ORANGE, w=4, tip=0.15)
        ar2 = arrow([3.3, 2.0, 0], [1.2, 2.55, 0], ORANGE, w=4, tip=0.15)
        dif = T("different cellular defect", 28, RED, weight=BOLD).move_to([0, -1.75, 0])
        self.play(GrowArrow(ar1), GrowArrow(ar2), Indicate(top, color=ORANGE, scale_factor=1.05), run_time=0.9)
        self.play(FadeIn(dif), run_time=0.6)
        self.at("sufficiency tests")
        l1 = chip("sufficiency tests", GREY, size=24).move_to([-3.3, -2.6, 0])
        l2 = chip("one species", GREY, size=24).move_to([0.0, -2.6, 0])
        l3 = chip("assays, not experiences", GREY, size=24).move_to([3.6, -2.6, 0])
        self.play(LaggedStart(FadeIn(l1), FadeIn(l2), FadeIn(l3), lag_ratio=0.4), run_time=1.3)
        self.at("Keep the rule")
        rule = T("In these mouse models, part of a tactile phenotype can begin outside the brain.", 28, GREEN, weight=BOLD)
        fit(rule, max_w=12.0)
        rule.move_to([0, -3.3, 0])
        self.play(FadeOut(dif), FadeIn(rule), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Part of a tactile phenotype can begin outside the brain, in mice."
