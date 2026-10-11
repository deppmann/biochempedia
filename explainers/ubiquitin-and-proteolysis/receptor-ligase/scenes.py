"""Section film: a hormone receptor that is a ligase (auxin, TIR1)

COLOR MAP (one colour per concept, whole film)
  YELLOW = auxin (the hormone)
  BLUE   = TIR1 (the F-box protein / receptor)
  PURPLE = the Aux/IAA repressor (the target)
  ORANGE = ubiquitin tags
  GREEN  = genes ON
  RED    = broken / destroyed / held off
  GREY   = membrane, SCF ligase body, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

TIR_Y = -0.6      # TIR1 centre in s02 to s04
BW, BH = 6.0, 1.9  # blob size


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def notched(color, top, h=BH, w=BW, r=0.45, label=None, size=30):
    """A rounded blob with a half-round pocket cut in its top (top=True) or bottom edge."""
    rect = RoundedRectangle(corner_radius=0.3, width=w, height=h)
    cut = Circle(radius=r).move_to(rect.get_top() if top else rect.get_bottom())
    shape = Difference(rect, cut)
    shape.set_stroke(color, 4).set_fill(color, 0.28)
    g = VGroup(shape)
    if label:
        g.add(T(label, size, color).move_to(shape.get_center() + (DOWN * 0.18 if top else UP * 0.18) + LEFT * 0.0))
    return g


def make_tir(label="TIR1"):
    return notched(BLUE, True, label=label)


def make_rep(label="Aux/IAA repressor"):
    return notched(PURPLE, False, h=1.7, label=label, size=28)


def scf_body(tir):
    bar = RoundedRectangle(corner_radius=0.15, width=BW, height=0.7, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.3)
    bar.next_to(tir, DOWN, buff=0.0)
    lab = T("SCF ligase", 26, GREY).move_to(bar)
    return VGroup(bar, lab)


def auxin(r=0.32):
    c = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.95)
    return c


def gene_chip(state):
    col = GREEN if state else RED
    txt = "genes ON" if state else "genes held off"
    return chip(txt, col, size=26)


class S00Title(TitleCard):
    LESSON = "Ubiquitin and Regulated Proteolysis as Signals"
    TITLE = "A Receptor Built Into the Destroyer"


# -------------------------------------------------------------------------------------------
class S01Search(SpokenScene):
    """expected surface receptor -> broken TIR1 plant -> TIR1 is an F-box protein."""

    def construct(self):
        # --- what animal biology said -------------------------------------------------
        head = T("What animal biology said", 30, GREY).to_edge(UP, buff=0.5)
        mem = RoundedRectangle(corner_radius=0.1, width=9.0, height=0.34, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.35).move_to([0, 0.9, 0])
        rec = RoundedRectangle(corner_radius=0.2, width=1.6, height=1.2, stroke_color=BLUE, stroke_width=4,
                               fill_color=BLUE, fill_opacity=0.3).move_to([0, 0.9, 0])
        aux = auxin(0.3).move_to([-3.6, 2.4, 0])
        aux_l = T("auxin", 26, YELLOW).next_to(aux, UP, buff=0.12)
        rec_l = T("receptor at the cell surface", 26, BLUE).move_to([3.4, 2.2, 0])
        self.at("cell surface")
        self.play(Write(head), FadeIn(mem), FadeIn(rec), FadeIn(rec_l), FadeIn(aux), FadeIn(aux_l), run_time=0.9)
        self.at("catches the hormone")
        self.play(aux.animate.move_to([0, 1.65, 0]), aux_l.animate.move_to([0, 2.35, 0]),
                  rec_l.animate.set_opacity(0), run_time=0.8)
        self.at("changes shape")
        self.play(rec.animate.stretch(1.3, 0), run_time=0.5)
        self.at("starts a cascade")
        steps = VGroup(*[chip(t, GREY, size=30) for t in ("step", "step", "step")]).arrange(RIGHT, buff=0.9)
        steps.move_to([0, -1.2, 0])
        a0 = arr([0, 0.45, 0], [0, -0.55, 0], GREY)
        a1 = arr(steps[0].get_right(), steps[1].get_left(), GREY)
        a2 = arr(steps[1].get_right(), steps[2].get_left(), GREY)
        casc = T("a cascade", 28, GREY).move_to([0, -2.4, 0])
        self.play(GrowArrow(a0), FadeIn(steps[0]), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(steps[1]), GrowArrow(a2), FadeIn(steps[2]), FadeIn(casc), run_time=0.7)
        old = VGroup(head, mem, rec, aux, aux_l, rec_l, steps, a0, a1, a2, casc)

        # --- the mutant ---------------------------------------------------------------
        self.at("But plants with a broken")
        plant = chip("Arabidopsis plant", GREEN, size=30).move_to([-3.6, 0.6, 0])
        gene = chip("TIR1 gene: broken", RED, size=30).move_to([-3.6, -0.9, 0])
        outcome = chip("responds poorly to auxin", YELLOW, size=30).move_to([3.1, -0.15, 0])
        link = arr([-1.3, -0.15, 0], [0.2, -0.15, 0], GREY)
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(plant), FadeIn(gene), run_time=0.5)
        self.at("respond poorly")
        self.play(GrowArrow(link), FadeIn(outcome, shift=LEFT * 0.2), run_time=0.6)

        # --- TIR1 is an F-box protein -------------------------------------------------
        self.at("is an F box")
        tir = make_tir().move_to([0, TIR_Y, 0])
        lab = T("an F-box protein", 30, BLUE).move_to([0, TIR_Y + 1.6, 0])
        self.play(FadeOut(VGroup(plant, gene, outcome, link)), run_time=0.4)
        self.play(FadeIn(tir, scale=0.9), run_time=0.5)
        self.at("F box protein")
        self.play(FadeIn(lab, shift=DOWN * 0.15), run_time=0.5)
        self.finish()


# -------------------------------------------------------------------------------------------
class S02Surprise(SpokenScene):
    """F-box = interchangeable part of SCF; thought to sense nothing; two labs report TIR1 binds auxin."""

    def construct(self):
        tir = make_tir().move_to([0, TIR_Y, 0])
        lab = T("an F-box protein", 30, BLUE).move_to([0, TIR_Y + 1.6, 0])
        self.add(tir, lab)
        body = scf_body(tir)
        self.at("interchangeable part")
        self.play(FadeIn(body, shift=UP * 0.1), Indicate(tir[0], color=BLUE, scale_factor=1.05), run_time=0.8)
        # thought to grab targets
        self.at("thought to grab targets")
        tgt = chip("target", PURPLE, size=28).move_to([-5.4, TIR_Y + 0.2, 0])
        grab = arr(tgt.get_right(), [-3.15, TIR_Y + 0.2, 0], PURPLE)
        note = T("thought: grabs targets", 24, GREY).move_to([-5.0, TIR_Y + 1.5, 0])
        self.play(FadeIn(tgt), GrowArrow(grab), FadeIn(note), run_time=0.7)
        self.at("sense nothing")
        aux = auxin().move_to([5.0, TIR_Y + 0.2, 0])
        aux_l = T("auxin", 24, YELLOW).next_to(aux, UP, buff=0.12)
        note2 = T("thought: senses nothing", 24, GREY).move_to([5.0, TIR_Y + 1.5, 0])
        miss = Cross(aux, stroke_color=RED, stroke_width=5).scale(1.4)
        self.play(FadeIn(aux), FadeIn(aux_l), FadeIn(note2), run_time=0.5)
        self.play(Create(miss), run_time=0.4)
        # clear the old idea
        self.at("Then, in the same issue")
        self.play(FadeOut(VGroup(tgt, grab, note, note2, miss, lab)), run_time=0.4)
        card1 = VGroup(T("Estelle's laboratory", 26, TEXT), T("Indiana University", 24, GREY)).arrange(DOWN, buff=0.1)
        card2 = VGroup(T("Leyser and Kepinski", 26, TEXT), T("University of York", 24, GREY)).arrange(DOWN, buff=0.1)
        card1.move_to([-4.3, 2.8, 0]); card2.move_to([4.3, 2.8, 0])
        nat = T("same issue of Nature, 2005", 26, GOLD).move_to([0, 2.8, 0])
        self.play(FadeIn(nat), run_time=0.4)
        self.at("laboratory at Indiana")
        self.play(FadeIn(card1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("independently")
        self.play(FadeIn(card2, shift=LEFT * 0.2), run_time=0.5)
        self.at("reported that")
        top = tir[0].get_top()
        self.play(aux.animate.move_to(top + DOWN * 0.0), aux_l.animate.move_to(top + UP * 0.8),
                  run_time=0.8)
        said = T("TIR1 binds auxin itself", 32, YELLOW).move_to([0, -3.0, 0])
        self.play(FadeIn(said, shift=UP * 0.1), tir[0].animate.set_stroke(YELLOW, 6), run_time=0.6)
        self.finish()


# -------------------------------------------------------------------------------------------
class S03Glue(SpokenScene):
    """repressor holds genes off, binds TIR1 poorly; auxin in the pocket, grip tightens; destroyed; genes on."""

    def construct(self):
        tir = make_tir().move_to([0, TIR_Y, 0])
        body = scf_body(tir)
        self.add(tir, body)
        top_y = TIR_Y + BH / 2
        gap_far = 0.5
        rep = make_rep().move_to([0, top_y + gap_far + 0.85, 0])
        genes = gene_chip(False).move_to([4.9, 1.7, 0])
        genes_cap = T("genes that auxin\nswitches on", 24, GREY, line_spacing=0.8).next_to(genes, UP, buff=0.15)
        bar = VGroup(Line([3.1, 1.7, 0], [3.5, 1.7, 0], color=RED, stroke_width=5),
                     Line([3.5, 1.45, 0], [3.5, 1.95, 0], color=RED, stroke_width=6))
        self.at("repressor proteins")
        self.play(FadeIn(genes), FadeIn(genes_cap), FadeIn(rep, shift=DOWN * 0.2), run_time=0.7)
        self.play(Create(bar), run_time=0.4)
        self.at("binds one of them poorly")
        loose = DashedLine(rep.get_bottom() + LEFT * 1.6, tir[0].get_top() + LEFT * 1.6, color=GREY, dash_length=0.1)
        loose2 = DashedLine(rep.get_bottom() + RIGHT * 1.6, tir[0].get_top() + RIGHT * 1.6, color=GREY, dash_length=0.1)
        wl = T("a poor grip", 26, GREY).move_to([-4.6, top_y + gap_far / 2, 0])
        self.play(Create(loose), Create(loose2), FadeIn(wl), run_time=0.6)
        # auxin arrives
        self.at("fits into a pocket")
        ax = auxin().move_to([5.6, top_y + gap_far / 2, 0])
        axl = T("auxin", 26, YELLOW).move_to([4.6, top_y + gap_far / 2 - 0.65, 0])
        self.play(FadeIn(ax), FadeIn(axl), run_time=0.4)
        self.play(ax.animate.move_to([0, top_y + gap_far / 2, 0]), run_time=0.8)
        self.at("grip tightens")
        shift = gap_far
        self.play(rep.animate.shift(DOWN * shift), ax.animate.move_to([0, top_y, 0]),
                  FadeOut(axl),
                  FadeOut(loose), FadeOut(loose2), FadeOut(wl), run_time=0.7)
        tight = T("tight grip", 26, YELLOW).move_to([-4.6, top_y + 0.2, 0])
        self.play(FadeIn(tight), rep[0].animate.set_stroke(YELLOW, 6), tir[0].animate.set_stroke(YELLOW, 6), run_time=0.4)
        # ubiquitin tags
        self.at("ubiquitinated")
        ubs = VGroup(*[chip("Ub", ORANGE, size=24, pad=0.14) for _ in range(3)]).arrange(RIGHT, buff=0.25)
        ubs.next_to(rep, UP, buff=0.25)
        self.play(LaggedStart(*[FadeIn(u, shift=DOWN * 0.2) for u in ubs], lag_ratio=0.3), run_time=0.8)
        self.at("destroyed")
        self.play(FadeOut(VGroup(rep, ubs, tight, ax), scale=0.4), FadeOut(bar),
                  tir[0].animate.set_stroke(BLUE, 4), run_time=0.8)
        self.at("genes come on")
        on = gene_chip(True).move_to(genes)
        self.play(ReplacementTransform(genes, on), run_time=0.6)
        self.finish()


# -------------------------------------------------------------------------------------------
class S04OneEvent(SpokenScene):
    """2007 structure: auxin in the joint; molecular glue; detecting = acting."""

    def construct(self):
        tir = make_tir().move_to([0, TIR_Y, 0])
        body = scf_body(tir)
        top_y = TIR_Y + BH / 2
        rep = make_rep().move_to([0, top_y + 0.85, 0])
        ax = auxin().move_to([0, top_y, 0])
        self.add(tir, body, rep, ax)
        self.at("In 2007")
        yr = T("2007 · crystal structure", 30, GOLD).move_to([-3.6, 3.0, 0])
        who = T("Estelle's group, with Ning Zheng", 26, GREY).next_to(yr, DOWN, buff=0.15)
        self.play(FadeIn(yr), FadeIn(who), run_time=0.7)
        self.at("sitting in the joint")
        ring = Circle(radius=0.62, color=YELLOW, stroke_width=4).move_to(ax)
        pt = arr([3.4, top_y + 2.05, 0], [0.62, top_y + 0.12, 0], YELLOW)
        lbl = T("auxin in the joint", 26, YELLOW).move_to([4.5, top_y + 2.3, 0])
        self.play(Create(ring), run_time=0.5)
        self.play(GrowArrow(pt), FadeIn(lbl), run_time=0.6)
        self.at("molecular glue")
        glue = T("a molecular glue", 32, YELLOW).move_to(lbl)
        self.play(ReplacementTransform(lbl, glue), Indicate(ax, color=YELLOW, scale_factor=1.4), run_time=0.8)
        self.at("detecting the hormone")
        det = chip("detecting the hormone", YELLOW, size=28)
        eff = chip("carrying out its effect", PURPLE, size=28)
        eq = T("=", 40, TEXT)
        row = VGroup(det, eq, eff).arrange(RIGHT, buff=0.35).move_to([0, -3.0, 0])
        self.play(FadeIn(det), run_time=0.4)
        self.at("carrying out its effect")
        self.play(FadeIn(eff), run_time=0.4)
        self.at("single event")
        self.play(FadeIn(eq), run_time=0.3)
        self.finish()


class S05End(EndCard):
    LINE = "Detecting the hormone and acting on it can be one event."
