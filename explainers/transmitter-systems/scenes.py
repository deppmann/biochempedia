"""Transmitter systems and drugs: a drug acts on one step  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = the source (presynaptic terminal)
  YELLOW = the transmitter (acetylcholine, glutamate, a peptide, serotonin)
  BLUE   = readers (receptors)
  TEAL   = the off switch (enzyme, peptidase, transporter, SERT)
  PURPLE = a drug (paroxetine and the other drug classes)
  GREEN  = response / established
  PINK   = glia
  GOLD   = the question or the take-home rule
  GREY   = membranes, outlines, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FB0"

SYX = -2.0          # x centre of the synapse stack
SW = 8.4            # width of terminal / post membrane
Y_TERM = 2.3        # terminal centre
Y_TEDGE = 1.3       # bottom edge of the terminal
Y_POST = -1.75      # postsynaptic membrane centre
CH_X, GP_X, TR_X = -4.4, -1.0, 1.0


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def xmark(center, r=0.28, color=RED):
    c = np.array([center[0], center[1], 0])
    return VGroup(Line(c + [-r, -r, 0], c + [r, r, 0], color=color, stroke_width=7),
                  Line(c + [-r, r, 0], c + [r, -r, 0], color=color, stroke_width=7))


def late(anim, d=0.45):
    """start an animation after a pause inside the same play() call (so old text clears first)."""
    return Succession(Wait(d), anim)


def chip_at(text, color, pos, size=22):
    c = chip(text, color, size=size, pad=0.16)
    return c.move_to(pos)


def dot(color=YELLOW, r=0.13, pos=(0, 0, 0)):
    return Dot(radius=r, color=color).move_to([pos[0], pos[1], 0])


def terminal(color=ORANGE, op=0.14):
    return RoundedRectangle(corner_radius=0.35, width=SW, height=2.0, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=op).move_to([SYX, Y_TERM, 0])


def post_membrane():
    return Rectangle(width=SW, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.35).move_to([SYX, Y_POST, 0])


def post_cell():
    return RoundedRectangle(corner_radius=0.2, width=SW, height=1.5, stroke_color=GREY, stroke_width=2,
                            fill_color=GREY, fill_opacity=0.06).move_to([SYX, -2.65, 0])


def channel(x=CH_X, color=BLUE):
    a = RoundedRectangle(corner_radius=0.1, width=0.36, height=0.95, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.35).move_to([x - 0.27, -1.5, 0])
    b = a.copy().move_to([x + 0.27, -1.5, 0])
    g = VGroup(a, b)
    g.top = np.array([x, -1.02, 0])
    return g


def gpcr(x=GP_X, color=BLUE):
    a = RoundedRectangle(corner_radius=0.15, width=0.62, height=1.05, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.35).move_to([x, -1.45, 0])
    a.top = np.array([x, -0.92, 0])
    return a


def transporter(x=TR_X, color=TEAL):
    return RoundedRectangle(corner_radius=0.12, width=0.7, height=0.95, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=0.3).move_to([x, Y_TEDGE, 0])


def cleft_dots(n, xs, ys, color=YELLOW):
    return VGroup(*[dot(color, 0.13, (x, y)) for x, y in zip(xs, ys)][:n])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Transmitter systems and drugs"
    TITLE = "A drug acts on one step"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """a drug fills half the transporters; does that explain why people improve? -> the answer is not in this picture."""

    def construct(self):
        yrow = 1.0
        mem = Rectangle(width=8.8, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                        fill_opacity=0.35).move_to([0, yrow, 0])
        xs = [-3.9 + 0.867 * i for i in range(10)]
        sert = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.5, height=0.95, stroke_color=TEAL, stroke_width=3,
                                         fill_color=TEAL, fill_opacity=0.3).move_to([x, yrow + 0.1, 0]) for x in xs])
        sert_lbl = T("human serotonin transporters (SERT)", 26, TEAL).move_to([0, 0.0, 0])
        mem_lbl = T("membranes from cultured cells", 22, GREY).move_to([0, -0.55, 0])
        self.play(FadeIn(mem), LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in sert], lag_ratio=0.06), run_time=1.2)
        self.play(FadeIn(sert_lbl), FadeIn(mem_lbl), run_time=0.5)

        # ten drug dots hover above; five dock
        dock = [1, 2, 5, 7, 8]
        drugs = VGroup(*[dot(PURPLE, 0.17, (xs[i], 2.55 + 0.25 * (k % 2))) for k, i in enumerate(range(10))])
        drug_lbl = T("paroxetine", 28, PURPLE).move_to([-4.6, 3.2, 0])
        self.at("the drug")
        self.play(FadeIn(drugs, shift=DOWN * 0.2), FadeIn(drug_lbl), run_time=0.7)
        self.at("fills half")
        docked = [drugs[i].animate.move_to([xs[i], yrow + 0.78, 0]) for i in dock]
        self.play(*docked, *[drugs[i].animate.set_opacity(0.0) for i in range(10) if i not in dock], run_time=1.0)
        half = T("half filled", 28, PURPLE).move_to([3.9, 2.4, 0])
        conc = M("0.08 nM", 32, PURPLE).move_to([3.9, 3.1, 0])
        self.at("at only")
        self.play(FadeIn(conc, shift=DOWN * 0.1), FadeIn(half), run_time=0.5)

        # the question
        self.at("depressed people improve")
        arrow = arr([0, -0.85, 0], [0, -1.7, 0], GREY)
        q = chip("Why do some depressed people improve?", GOLD, size=32, pad=0.3).move_to([0, -2.55, 0])
        self.play(GrowArrow(arrow), FadeIn(q, shift=UP * 0.15), run_time=0.8)
        self.at("It does not")
        cross = xmark([0, -1.27])
        self.play(Create(cross), run_time=0.4)
        self.at("what the drug acts on")
        self.wait(0.2)
        self.at("works as a system")
        self.play(FadeOut(VGroup(mem, sert, sert_lbl, mem_lbl, drugs, drug_lbl, half, conc, arrow, cross, q)),
                  run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Parts(SpokenScene):
    """build the synapse: source, readers (fast and slow), off switch."""

    def construct(self):
        term = terminal(GREY, 0.05)
        pm, pc = post_membrane(), post_cell()
        self.at("transmitter system")
        self.play(FadeIn(term), FadeIn(pm), FadeIn(pc), run_time=0.9)

        # source
        self.at("The source")
        self.play(term.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.14), run_time=0.5)
        src = T("source", 30, ORANGE, weight=BOLD).move_to([4.5, 2.3, 0])
        sline = Line([2.3, 2.3, 0], [3.6, 2.3, 0], color=ORANGE, stroke_width=3)
        self.play(FadeIn(src), Create(sline), run_time=0.5)
        self.at("make and release")
        xs0 = [-5.0, -4.0, -3.0, -1.6, -0.6, 0.4]
        ds = VGroup(*[dot(YELLOW, 0.14, (x, 2.5 + 0.2 * ((i % 2) - 0.5))) for i, x in enumerate(xs0)])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in ds], lag_ratio=0.1), run_time=0.8)
        tgt = [(-4.8, 0.4), (-3.9, 0.9), (-2.7, 0.2), (-1.5, 0.6), (-0.5, 0.1), (0.3, 0.7)]
        self.play(*[d.animate.move_to([x, y, 0]) for d, (x, y) in zip(ds, tgt)], run_time=1.1)
        trans_lbl = T("transmitter", 26, YELLOW).move_to([-2.4, 3.0, 0])
        self.play(FadeIn(trans_lbl), run_time=0.3)

        # readers
        self.at("The readers")
        ch, gp = channel(), gpcr()
        readers = T("readers", 30, BLUE, weight=BOLD).move_to([4.5, -1.6, 0])
        rline = Line([2.3, -1.6, 0], [3.6, -1.6, 0], color=BLUE, stroke_width=3)
        self.play(FadeIn(ch, shift=UP * 0.2), FadeIn(gp, shift=UP * 0.2), FadeIn(readers), Create(rline), run_time=0.8)
        self.at("ion channels")
        ch_lbl = VGroup(T("ion channel", 24, BLUE), T("about 1 ms", 24, TEXT)).arrange(DOWN, buff=0.08).move_to([CH_X, -2.7, 0])
        self.play(FadeIn(ch_lbl), run_time=0.4)
        self.play(ds[0].animate.move_to([CH_X, -0.7, 0]), run_time=0.7)
        self.play(ch.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), run_time=0.15)
        self.play(ch.animate.set_stroke(BLUE).set_fill(BLUE, 0.35), run_time=0.5)
        self.at("Others are")
        gp_lbl = VGroup(T("G-protein-coupled", 24, BLUE), T("tens of ms to seconds", 24, TEXT)).arrange(DOWN, buff=0.08).move_to([GP_X + 0.2, -2.7, 0])
        self.play(FadeIn(gp_lbl), ds[4].animate.move_to([GP_X, -0.55, 0]), run_time=0.8)
        self.play(gp.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), run_time=0.2)
        self.play(gp.animate.set_stroke(BLUE).set_fill(BLUE, 0.35), run_time=0.9)

        # off switch
        self.at("The off switch")
        tr = transporter()
        off = T("off switch", 30, TEAL, weight=BOLD).move_to([4.5, 0.6, 0])
        oline = Line([1.5, 0.95, 0], [3.5, 0.65, 0], color=TEAL, stroke_width=3)
        self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(off), Create(oline), run_time=0.7)
        self.at("ends the signal")
        self.play(ds[5].animate.move_to([TR_X, 1.3, 0]), run_time=0.5)
        self.play(ds[5].animate.move_to([TR_X, 2.3, 0]).set_opacity(0), ds[1].animate.set_opacity(0.0),
                  ds[2].animate.set_opacity(0), ds[3].animate.set_opacity(0), ds[0].animate.set_opacity(0),
                  ds[4].animate.set_opacity(0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Off(SpokenScene):
    """four off switches: enzyme, transporters, peptidase, SERT."""

    def construct(self):
        term, pm, pc = terminal(), post_membrane(), post_cell()
        ch, gp = channel(), gpcr()
        src = T("source", 30, ORANGE, weight=BOLD).move_to([4.5, 2.3, 0])
        readers = T("readers", 30, BLUE, weight=BOLD).move_to([4.5, -1.6, 0])
        off = T("off switch", 30, TEAL, weight=BOLD).move_to([4.5, 0.6, 0])
        self.add(term, pm, pc, ch, gp, src, readers)
        self.play(FadeIn(off), run_time=0.5)

        def case_label(name, lines):
            n = T(name, 32, YELLOW, weight=BOLD).move_to([SYX, 2.55, 0])
            sub = VGroup(*[T(l, 24, TEAL) for l in lines]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            sub.move_to([4.5, -0.45, 0]).align_to([2.8, 0, 0], LEFT)
            return n, sub

        # --- acetylcholine -> enzyme -------------------------------------------------------
        self.at("The off switch depends")
        n1, s1 = case_label("acetylcholine", ["enzyme:", "acetylcholinesterase"])
        enz = chip_at("enzyme", TEAL, [-1.0, 0.1, 0], 24)
        d1 = cleft_dots(4, [-4.5, -3.2, -2.2, -1.7], [0.4, 0.7, 0.2, 0.6])
        self.play(FadeIn(n1), FadeIn(d1), run_time=0.6)
        self.at("broken down by an enzyme")
        self.play(FadeIn(enz), FadeIn(s1), run_time=0.5)
        self.play(*[d.animate.move_to(enz.get_center() + np.array([0.0 + 0.0 * i, 0.0, 0])).scale(0.1).set_opacity(0)
                    for i, d in enumerate(d1)], lag_ratio=0.0, run_time=1.4)
        self.at("at many synapses")
        self.wait(0.5)

        # --- glutamate -> transporters (terminal and glia) ----------------------------------
        self.at("Glutamate is cleared")
        n2, s2 = case_label("glutamate", ["transporters in", "glia and terminals", "no enzyme in cleft"])
        glia = Ellipse(width=1.7, height=1.1, stroke_color=PINK, stroke_width=3, fill_color=PINK,
                       fill_opacity=0.15).move_to([1.5, -0.55, 0])
        glia_lbl = T("glia", 24, PINK).move_to(glia).shift(DOWN * 0.12)
        tr_g = RoundedRectangle(corner_radius=0.1, width=0.55, height=0.7, stroke_color=TEAL, stroke_width=3.5,
                                fill_color=TEAL, fill_opacity=0.3).move_to([1.5, -0.05, 0])
        tr_t = transporter(-1.6)
        d2 = cleft_dots(4, [-1.9, -1.4, 1.1, 1.8], [0.2, 0.55, 0.5, 0.35])
        self.play(FadeOut(n1), late(FadeIn(n2)), FadeOut(s1), late(FadeIn(s2)), FadeOut(enz),
                  FadeIn(glia), FadeIn(glia_lbl), FadeIn(tr_g), FadeIn(tr_t), FadeIn(d2), run_time=0.8)
        self.play(d2[0].animate.move_to([-1.6, 1.4, 0]), d2[1].animate.move_to([-1.6, 1.4, 0]),
                  d2[2].animate.move_to([1.5, -0.3, 0]), d2[3].animate.move_to([1.5, -0.3, 0]), run_time=1.0)
        self.play(*[d.animate.set_opacity(0) for d in d2], run_time=0.5)
        self.at("No enzyme in the cleft")
        self.wait(0.8)

        # --- peptides -> peptidase -----------------------------------------------------------
        self.at("Peptides are cut")
        n3, s3 = case_label("peptide", ["peptidases cut", "them into inactive", "fragments"])
        pep = enz.copy().become(chip_at("peptidase", TEAL, [-1.0, 0.1, 0], 24))
        bar = RoundedRectangle(corner_radius=0.09, width=0.9, height=0.2, stroke_color=YELLOW, stroke_width=2,
                               fill_color=YELLOW, fill_opacity=0.9).move_to([-3.6, 0.5, 0])
        self.play(FadeOut(n2), late(FadeIn(n3)), late(FadeIn(s3)),
                  FadeOut(s2), FadeOut(VGroup(glia, glia_lbl, tr_g, tr_t)), FadeIn(pep), FadeIn(bar), run_time=0.8)
        self.play(bar.animate.move_to([-1.9, 0.5, 0]), run_time=0.8)
        f1 = RoundedRectangle(corner_radius=0.07, width=0.4, height=0.2, stroke_color=GREY, stroke_width=2,
                              fill_color=GREY, fill_opacity=0.8).move_to([-2.15, 0.5, 0])
        f2 = f1.copy().move_to([-1.65, 0.5, 0])
        self.play(FadeOut(bar), FadeIn(f1), FadeIn(f2), run_time=0.2)
        self.play(f1.animate.shift(LEFT * 0.5 + DOWN * 0.2), f2.animate.shift(RIGHT * 0.5 + DOWN * 0.2), run_time=0.8)

        # --- serotonin -> SERT --------------------------------------------------------------
        self.at("The amines")
        n4, s4 = case_label("serotonin", ["transporter:", "SERT"])
        tr = transporter()
        sert_lbl = T("SERT", 26, TEAL, weight=BOLD).move_to([TR_X, 0.62, 0])
        d4 = cleft_dots(4, [-1.0, -0.3, 0.3, 0.9], [0.2, 0.6, 0.15, 0.45])
        self.play(FadeOut(n3), late(FadeIn(n4)), FadeOut(s3), late(FadeIn(s4)), FadeOut(pep), FadeOut(VGroup(f1, f2)),
                  FadeIn(tr), FadeIn(d4), run_time=0.8)
        self.at("carried back into the terminal")
        self.play(*[d.animate.move_to([TR_X, 1.0, 0]) for d in d4], lag_ratio=0.0, run_time=0.9)
        self.play(*[d.animate.move_to([TR_X - 1.2 + 0.7 * i, 2.4, 0]) for i, d in enumerate(d4)], run_time=1.0)
        self.at("is called")
        self.play(FadeIn(sert_lbl), tr.animate.set_stroke(YELLOW), run_time=0.4)
        self.play(tr.animate.set_stroke(TEAL), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Drugs(SpokenScene):
    """the same synapse; a drug (purple) acts on a different step in each case."""

    def construct(self):
        term, pm, pc = terminal(), post_membrane(), post_cell()
        rx = 2.6  # right column left edge
        # receptor with a main site (top) and a second site (side)
        rec = RoundedRectangle(corner_radius=0.14, width=0.95, height=1.0, stroke_color=BLUE, stroke_width=3.5,
                               fill_color=BLUE, fill_opacity=0.35).move_to([CH_X, -1.45, 0])
        main = Circle(radius=0.17, stroke_color=BLUE, stroke_width=3).move_to([CH_X, -0.95, 0])
        side = Circle(radius=0.17, stroke_color=BLUE, stroke_width=3).move_to([CH_X + 0.62, -1.25, 0])
        site_a = T("own site", 22, BLUE).move_to([CH_X - 1.25, -0.95, 0])
        site_b = T("other site", 22, BLUE).move_to([CH_X + 1.8, -1.25, 0])
        bar_bg = Rectangle(width=2.6, height=0.32, stroke_color=GREY, stroke_width=2, fill_color=BG,
                           fill_opacity=1).move_to([-3.2, -2.65, 0])
        bar_lbl = T("response", 22, GREEN).move_to([-5.55, -2.65, 0])
        enz = chip_at("enzyme", TEAL, [-1.6, 0.15, 0], 24)
        tr = transporter()
        sert_lbl = T("SERT", 24, TEAL, weight=BOLD).move_to([TR_X, 0.62, 0])
        self.add(term, pm, pc, rec, main, side)
        self.play(FadeIn(enz), FadeIn(tr), FadeIn(sert_lbl), FadeIn(bar_bg), FadeIn(bar_lbl), FadeIn(site_a),
                  FadeIn(site_b), run_time=0.8)

        def fill(frac, color=GREEN):
            f = Rectangle(width=max(0.001, 2.6 * frac), height=0.32, stroke_width=0, fill_color=color, fill_opacity=0.85)
            f.align_to(bar_bg, LEFT).align_to(bar_bg, UP)
            return f

        def cls(name, sub):
            n = T(name, 30, PURPLE, weight=BOLD).move_to([4.45, 1.95, 0])
            s = VGroup(*[T(l, 24, TEXT) for l in sub]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            s.align_to([rx + 0.2, 0, 0], LEFT).move_to([4.45, 0.9, 0], aligned_edge=LEFT) if False else None
            s.move_to([4.45, 0.9, 0]).align_to([rx + 0.1, 0, 0], LEFT)
            return n, s

        # --- agonist ------------------------------------------------------------------------
        self.at("A drug changes one step")
        self.wait(0.3)
        self.at("An agonist")
        n, s = cls("agonist", ["activates a reader"])
        d = dot(PURPLE, 0.17, (-2.5, 0.2))
        self.play(FadeIn(n), FadeIn(s), FadeIn(d), run_time=0.5)
        self.play(d.animate.move_to(main.get_center()), run_time=0.9)
        f = fill(0.6)
        self.play(rec.animate.set_stroke(GREEN), GrowFromEdge(f, LEFT), run_time=0.7)
        self.wait(0.6)

        # --- competitive antagonist ---------------------------------------------------------
        self.at("A competitive antagonist")
        n2, s2 = cls("competitive antagonist", ["takes the reader's", "own site"])
        n2.scale(0.8).move_to([4.45, 1.95, 0])
        y = dot(YELLOW, 0.13, (-3.3, 0.3))
        d2 = dot(PURPLE, 0.17, (-2.5, 0.2))
        self.play(FadeOut(n), late(FadeIn(n2)), FadeOut(s), late(FadeIn(s2)), FadeOut(d), FadeOut(f),
                  rec.animate.set_stroke(BLUE), FadeIn(d2), FadeIn(y), run_time=0.6)
        self.play(d2.animate.move_to(main.get_center()), run_time=0.8)
        self.at("prevents activation")
        self.play(y.animate.move_to([CH_X - 0.1, -0.6, 0]), run_time=0.6)
        self.play(y.animate.move_to([CH_X - 0.9, 0.0, 0]), run_time=0.6)
        blk = T("no response", 22, RED).move_to([-0.6, -2.65, 0])
        self.play(FadeIn(blk), run_time=0.3)

        # --- PAM ----------------------------------------------------------------------------
        self.at("A positive allosteric modulator")
        n3, s3 = cls("allosteric modulator", ["binds a different site", "and strengthens", "the effect"])
        n3.scale(0.9).move_to([4.45, 1.95, 0])
        y3 = dot(YELLOW, 0.13, (-3.3, 0.3))
        d3 = dot(PURPLE, 0.17, (-3.2, 1.0))
        self.play(FadeOut(n2), late(FadeIn(n3)), FadeOut(s2), late(FadeIn(s3)), FadeOut(d2), FadeOut(y), FadeOut(blk),
                  FadeIn(y3), FadeIn(d3), run_time=0.6)
        self.play(y3.animate.move_to(main.get_center()), run_time=0.8)
        f3 = fill(0.5)
        self.play(rec.animate.set_stroke(GREEN), GrowFromEdge(f3, LEFT), run_time=0.5)
        self.at("strengthens the effect")
        self.play(d3.animate.move_to(side.get_center()), run_time=0.7)
        f3b = fill(0.9)
        self.play(Transform(f3, f3b), run_time=0.7)
        self.wait(0.4)

        # --- enzyme inhibitor ---------------------------------------------------------------
        self.at("An enzyme inhibitor")
        n4, s4 = cls("enzyme inhibitor", ["slows the", "breakdown"])
        n4.scale(0.9).move_to([4.45, 1.95, 0])
        y4 = dot(YELLOW, 0.13, (-3.2, 0.35))
        d4 = dot(PURPLE, 0.17, (-1.0, 0.8))
        self.play(FadeOut(n3), late(FadeIn(n4)), FadeOut(s3), late(FadeIn(s4)), FadeOut(d3), FadeOut(y3), FadeOut(f3),
                  rec.animate.set_stroke(BLUE), FadeIn(y4), FadeIn(d4), run_time=0.6)
        self.play(d4.animate.move_to(enz.get_top() + UP * 0.12), run_time=0.7)
        self.at("slows the breakdown")
        self.play(y4.animate.move_to(enz.get_left() + LEFT * 0.35), run_time=0.9)
        self.wait(0.5)

        # --- reuptake blocker ---------------------------------------------------------------
        self.at("A reuptake blocker")
        n5, s5 = cls("reuptake blocker", ["occupies the", "transporter"])
        n5.scale(0.9).move_to([4.45, 1.95, 0])
        y5 = dot(YELLOW, 0.13, (0.2, 0.2))
        d5 = dot(PURPLE, 0.17, (-0.8, 0.9))
        self.play(FadeOut(n4), late(FadeIn(n5)), FadeOut(s4), late(FadeIn(s5)), FadeOut(d4), FadeOut(y4),
                  FadeIn(y5), FadeIn(d5), run_time=0.6)
        self.play(d5.animate.move_to([TR_X, 1.05, 0]), run_time=0.8)
        self.at("occupies the transporter")
        self.play(y5.animate.move_to([TR_X - 0.5, 0.2, 0]), run_time=0.5)
        self.at("Paroxetine sits")
        parox = T("paroxetine", 26, PURPLE, weight=BOLD).move_to([4.45, 0.1, 0]).align_to([2.7, 0, 0], LEFT)
        self.play(FadeIn(parox), run_time=0.4)
        self.at("where serotonin binds")
        self.play(y5.animate.move_to([TR_X - 0.3, 0.75, 0]), run_time=0.4)
        self.play(y5.animate.move_to([TR_X - 0.9, 0.5, 0]), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Fill(SpokenScene):
    """occupancy curve computed from f = L / (KD + L)."""

    def construct(self):
        KD = 0.08
        ox, oy, w, h = -5.2, -2.3, 9.4, 4.7
        X = lambda L: ox + w * L                     # x axis 0..1 nM
        Y = lambda f: oy + h * f
        xaxis = Line([ox, oy, 0], [ox + w + 0.1, oy, 0], color=GREY, stroke_width=3)
        yaxis = Line([ox, oy, 0], [ox, oy + h + 0.15, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for v in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            ticks.add(M(f"{v:g}", 22, GREY).move_to([X(v), oy - 0.38, 0]))
        for v, s in [(0, "0"), (0.5, "50%"), (0.9, "90%"), (1.0, "100%")]:
            ticks.add(M(s, 22, GREY).move_to([ox - 0.55, Y(v), 0]))
        xl = T("free drug, L (nM)", 24, GREY).move_to([-1.4, oy - 0.9, 0])
        yl = T("fraction of transporters filled", 24, PURPLE).move_to([-2.5, oy + h + 0.5, 0])
        tag = T("computed from the equation", 22, GREY).move_to([3.6, oy - 0.9, 0])
        self.play(Create(xaxis), Create(yaxis), run_time=0.7)
        self.play(FadeIn(ticks), FadeIn(xl), FadeIn(yl), FadeIn(tag), run_time=0.6)
        self.at("The fraction filled")
        curve = ParametricFunction(lambda t: np.array([X(t), Y(t / (KD + t)), 0]), t_range=[0.0015, 1.0, 0.004],
                                   color=PURPLE, stroke_width=5)
        eq = M("f = L / (KD + L)", 34, TEXT).move_to([2.9, oy + h + 0.5, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), Create(curve), run_time=2.0)
        self.at("dissociation constant")
        self.wait(0.2)
        self.at("fills half the sites")
        p1 = Dot([X(KD), Y(0.5), 0], radius=0.11, color=YELLOW)
        v1 = DashedLine([ox, Y(0.5), 0], [X(KD), Y(0.5), 0], color=YELLOW, stroke_width=2.5)
        v1b = DashedLine([X(KD), Y(0.5), 0], [X(KD), oy, 0], color=YELLOW, stroke_width=2.5)
        self.play(Create(v1), Create(v1b), FadeIn(p1), run_time=0.8)
        self.at("For paroxetine")
        kd_lbl = M("KD = 0.08 nM", 26, YELLOW).move_to([X(KD) + 2.0, Y(0.5) - 0.65, 0])
        self.play(FadeIn(kd_lbl), run_time=0.5)
        self.at("are filled")
        p2 = Dot([X(0.72), Y(0.9), 0], radius=0.11, color=YELLOW)
        v2 = DashedLine([ox, Y(0.9), 0], [X(0.72), Y(0.9), 0], color=YELLOW, stroke_width=2.5)
        v2b = DashedLine([X(0.72), Y(0.9), 0], [X(0.72), oy, 0], color=YELLOW, stroke_width=2.5)
        l2 = M("0.72 nM: 90%", 26, YELLOW).move_to([X(0.72) + 1.65, Y(0.9) - 0.9, 0])
        self.play(Create(v2), Create(v2b), FadeIn(p2), FadeIn(l2), run_time=0.8)
        self.at("flattens at the top")
        self.play(Indicate(curve, color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Cause(SpokenScene):
    """filling a transporter is not a clinical effect; mechanism is not cause."""

    def construct(self):
        # beat 1: filled transporter is not a clinical effect
        a = chip("transporter filled", PURPLE, size=34, pad=0.3).move_to([-3.7, 0.3, 0])
        ne = T("is not", 36, TEXT).move_to([0, 0.3, 0])
        b = chip("clinical effect", GOLD, size=34, pad=0.3).move_to([3.7, 0.3, 0])
        self.at("Filling the transporter")
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.5)
        self.at("not a clinical effect")
        self.play(FadeIn(ne), FadeIn(b, shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.4)

        # beat 2: established vs separate claim
        self.at("is established")
        yb = 2.7
        boxA = chip("these drugs block SERT", GREEN, size=30, pad=0.3).move_to([-3.7, yb, 0])
        tagA = T("established", 26, GREEN, weight=BOLD).next_to(boxA, DOWN, buff=0.15)
        boxB = chip("low serotonin causes\ndepression", GREY, size=30, pad=0.3).move_to([3.4, yb - 0.1, 0])
        self.play(FadeOut(VGroup(a, ne, b)), FadeIn(boxA, shift=UP * 0.1), FadeIn(tagA), run_time=0.7)
        self.at("separate claim")
        link = arr([boxA.get_right()[0] + 0.1, yb, 0], [boxB.get_left()[0] - 0.1, yb, 0], GREY)
        qm = T("?", 44, GOLD, weight=BOLD).move_to([-0.05, yb + 0.6, 0])
        tagB = T("a separate claim", 26, GREY, weight=BOLD).next_to(boxB, DOWN, buff=0.15)
        self.play(FadeIn(boxB), GrowArrow(link), FadeIn(qm), FadeIn(tagB), run_time=0.8)

        # beat 3: the two reviews
        self.at("umbrella review")
        hB = T("Is low serotonin the cause?", 26, GOLD).move_to([3.4, 0.5, 0])
        rB = VGroup(T("2022 umbrella review", 28, TEXT, weight=BOLD), T("no consistent support", 28, TEXT),
                    T("for it", 28, TEXT)).arrange(DOWN, buff=0.12).move_to([3.4, -0.7, 0])
        self.play(FadeIn(hB), FadeIn(rB, shift=UP * 0.1), run_time=0.6)
        self.at("network meta analysis")
        hA = T("Do the drugs help?", 26, GOLD).move_to([-3.6, 0.5, 0])
        rA = VGroup(T("2018 network meta-analysis", 28, TEXT, weight=BOLD),
                    T("all 21 antidepressants it included", 28, TEXT), T("more effective than placebo", 28, TEXT),
                    T("acute major depression, adults", 28, TEXT), T("certainty: moderate to very low", 28, GREY)
                    ).arrange(DOWN, buff=0.12).move_to([-3.6, -1.15, 0])
        self.play(FadeIn(hA), FadeIn(rA, shift=UP * 0.1), run_time=0.8)
        self.at("Both can be true")
        both = T("both can be true", 34, GOLD, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(both, shift=UP * 0.1), run_time=0.5)

        # beat 4: aspirin
        self.at("Aspirin relieves a headache")
        self.play(FadeOut(VGroup(boxA, tagA, boxB, tagB, link, qm, rA, rB, hA, hB, both)), run_time=0.6)
        asp = chip("aspirin", PURPLE, size=36, pad=0.28).move_to([-4.0, 1.9, 0])
        hrel = chip("headache relieved", GREEN, size=36, pad=0.28).move_to([3.5, 1.9, 0])
        l1 = arr([asp.get_right()[0] + 0.1, 1.9, 0], [hrel.get_left()[0] - 0.1, 1.9, 0], GREY)
        self.play(FadeIn(asp), GrowArrow(l1), FadeIn(hrel), run_time=0.8)
        self.at("not caused by a lack")
        lack = chip("lack of aspirin", PURPLE, size=36, pad=0.28).move_to([-4.0, 0.2, 0])
        hd = chip("headache", GREEN, size=36, pad=0.28).move_to([3.5, 0.2, 0])
        l2 = arr([lack.get_right()[0] + 0.1, 0.2, 0], [hd.get_left()[0] - 0.1, 0.2, 0], GREY)
        x2 = xmark([(lack.get_right()[0] + hd.get_left()[0]) / 2, 0.2])
        self.play(FadeIn(lack), GrowArrow(l2), FadeIn(hd), run_time=0.8)
        self.play(Create(x2), run_time=0.4)

        self.at("A drug's mechanism")
        rule = VGroup(T("A drug's mechanism does not prove", 38, GOLD, font=TITLE_FONT),
                      T("what causes the disease.", 38, GOLD, font=TITLE_FONT)).arrange(DOWN, buff=0.15).move_to([0, -2.2, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "A drug's mechanism does not prove what causes the disease."
