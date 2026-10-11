"""Who switches Erk on?  (Biochemistrypedia section film, lesson: Ras to MAPK)

Section: "Three kinases in a row". The experiment: how MAP kinase (Erk) was found, and how
Natalie Ahn's activators showed that Erk was not switching itself on.

COLOR MAP (one color per concept, whole video)
  BLUE   = Erk (the MAP kinase)
  PURPLE = the activator, later named Mek
  ORANGE = Raf
  YELLOW = the stimulus (insulin, growth factor)
  GOLD   = a phosphate badge
  GREEN  = active / on
  RED    = ruled out / taken off
  GREY   = structure, columns, yeast kinases, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pbadge(r=0.24):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    return VGroup(c, T("P", 24, BG, weight=BOLD).move_to(c))


def recolor(c, color):
    return [c[0].animate.set_stroke(color).set_fill(color, 0.16), c[1].animate.set_color(color)]


def cross(center, s=0.35, color=RED):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=7),
                  Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=7))


class S00Title(TitleCard):
    LESSON = "Ras to MAPK: The Kinase Cascade"
    TITLE = "Who switches Erk on?"


# ---------------------------------------------------------------------------------------------
class S01Columns(SpokenScene):
    def construct(self):
        dot = Circle(radius=0.42, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.9).move_to([0, 0.5, 0])
        lab = T("kinase activity", 34, BLUE).move_to([0, -0.5, 0])
        self.at("following an activity")
        self.play(FadeIn(dot, scale=0.6), FadeIn(lab), run_time=0.6)
        ins = chip("insulin", YELLOW, 36).move_to([0, 2.7, 0])
        ia = arr([0, 2.2, 0], [0, 1.05, 0], YELLOW)
        self.at("insulin switched on")
        self.play(FadeIn(ins, shift=DOWN * 0.2), GrowArrow(ia), run_time=0.6)
        lab2 = T("insulin-stimulated kinase activity", 34, BLUE).move_to([0, -0.5, 0])
        self.play(Transform(lab, lab2), run_time=0.5)

        # eight columns
        xs = [-5.25 + 1.5 * i for i in range(8)]
        cols = VGroup(*[RoundedRectangle(corner_radius=0.15, width=0.8, height=3.2, stroke_color=GREY, stroke_width=3,
                                         fill_color=GREY, fill_opacity=0.18).move_to([x, 0.9, 0]) for x in xs])
        nums = VGroup(*[T(str(i + 1), 24, GREY).move_to([x, -1.0, 0]) for i, x in enumerate(xs)])
        self.at("eight chromatography columns")
        self.play(FadeOut(ins), FadeOut(ia), FadeOut(lab), dot.animate.move_to([-6.3, 0.9, 0]),
                  LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cols], lag_ratio=0.08), run_time=0.8)
        cap = T("chromatography columns", 28, GREY).move_to([0, -1.6, 0])
        self.play(FadeIn(nums), FadeIn(cap), run_time=0.2)
        self.play(dot.animate.move_to([6.3, 0.9, 0]), run_time=1.2, rate_func=linear)

        gene = chip("gene cloned", GREY, 34).move_to([-2.6, -2.7, 0])
        self.at("cloned its gene")
        self.play(FadeIn(gene, shift=UP * 0.2), run_time=0.5)
        erk = chip("ERK", BLUE, 44).move_to([2.6, -2.7, 0])
        ga = arr(gene.get_right() + RIGHT * 0.1, erk.get_left() + LEFT * 0.1, GREY)
        self.at("named the enzyme")
        self.play(GrowArrow(ga), FadeIn(erk, scale=0.8), run_time=0.6)

        # yeast
        self.at("resembled two yeast")
        erk_t = chip("ERK", BLUE, 52).move_to([-4.6, 0.4, 0])
        y1 = chip("yeast kinase", GREY, 34).move_to([0.9, 1.7, 0])
        y2 = chip("yeast kinase", GREY, 34).move_to([0.9, -0.9, 0])
        self.play(FadeOut(cols), FadeOut(nums), FadeOut(cap), FadeOut(dot), FadeOut(gene), FadeOut(ga),
                  Transform(erk, erk_t), run_time=0.6)
        a1 = arr([-3.6, 0.7, 0], [y1.get_left()[0] - 0.1, 1.5, 0], GREY)
        a2 = arr([-3.6, 0.1, 0], [y2.get_left()[0] - 0.1, -0.7, 0], GREY)
        sim = T("sequence resembled", 28, GREY).move_to([-1.6, 0.45, 0])
        self.play(FadeIn(y1, shift=LEFT * 0.2), FadeIn(y2, shift=LEFT * 0.2), GrowArrow(a1), GrowArrow(a2),
                  FadeIn(sim), run_time=0.8)
        self.at("mating pheromone")
        brace = Brace(VGroup(y1, y2), RIGHT, color=GREY)
        tag = T("respond to\nmating pheromone", 28, YELLOW).next_to(brace, RIGHT, buff=0.15)
        self.play(GrowFromCenter(brace), FadeIn(tag), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Extracts(SpokenScene):
    def construct(self):
        who = T("Natalie Ahn, Edwin Krebs's laboratory", 28, GREY).move_to([0, 3.0, 0])
        erk = chip("ERK", BLUE, 72).move_to([0, -0.3, 0])
        self.play(FadeIn(who, shift=DOWN * 0.1), FadeIn(erk, scale=0.8), run_time=0.6)
        q = chip("?", GREY, 64).move_to([0, 1.8, 0])
        qa = arr([0, 1.2, 0], [0, 0.4, 0], GREY)
        self.at("what switches")
        self.play(FadeIn(q, shift=DOWN * 0.2), GrowArrow(qa), run_time=0.6)
        # extracts
        ext = chip("extract of cells\nwith growth factor", YELLOW, 26).move_to([-4.5, 0.3, 0])
        act1 = chip("activity 1", PURPLE, 30).move_to([-0.6, 1.7, 0])
        act2 = chip("activity 2", PURPLE, 30).move_to([-0.6, -1.1, 0])
        e1 = arr(ext.get_right() + [0.05, 0.3, 0], act1.get_left() + [-0.1, 0, 0], PURPLE)
        e2 = arr(ext.get_right() + [0.05, -0.3, 0], act2.get_left() + [-0.1, 0, 0], PURPLE)
        self.at("two activities")
        self.play(FadeOut(erk), FadeOut(q), FadeOut(qa), FadeIn(ext, shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(act1), FadeIn(act2), run_time=0.8)
        tube = RoundedRectangle(corner_radius=0.4, width=3.6, height=2.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.1).move_to([4.2, 0.3, 0])
        mk = chip("MAP kinase\ninactive", GREY, 26).move_to(tube)
        tl = T("test tube", 26, GREY).next_to(tube, DOWN, buff=0.2)
        ta1 = arr(act1.get_right() + [0.1, 0, 0], tube.get_left() + [-0.05, 0.4, 0], PURPLE)
        ta2 = arr(act2.get_right() + [0.1, 0, 0], tube.get_left() + [-0.05, -0.2, 0], PURPLE)
        self.at("switched on")
        self.play(FadeIn(tube), FadeIn(mk), GrowArrow(ta1), GrowArrow(ta2), run_time=0.7)
        mk_on = chip("MAP kinase\nactive", GREEN, 26).move_to(tube)
        self.at("test tube")
        self.play(FadeIn(tl), Transform(mk, mk_on), tube.animate.set_stroke(GREEN), run_time=0.6)
        qs = T("?", 54, YELLOW, weight=BOLD).move_to([-0.6, 0.3, 0])
        self.at("switching itself")
        loop = CurvedArrow(tube.get_top() + [0.6, 0.05, 0], tube.get_top() + [-0.6, 0.05, 0], angle=TAU / 4 * 1.4, color=BLUE)
        lq = T("?", 54, YELLOW, weight=BOLD).next_to(loop, UP, buff=0.05)
        self.play(Create(loop), FadeIn(lq), run_time=0.7)
        self.at("something else do it")
        self.play(FadeIn(qs, scale=0.7), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Column(SpokenScene):
    def construct(self):
        col = RoundedRectangle(corner_radius=0.3, width=1.6, height=5.0, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.15).move_to([-3.6, 0.2, 0])
        cl = T("column", 28, GREY).move_to([-3.6, -2.75, 0])
        self.play(FadeIn(col), FadeIn(cl), run_time=0.7)
        dB = Circle(radius=0.26, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.9).move_to([-3.6, 2.0, 0])
        dP = Circle(radius=0.2, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.95).move_to([-3.6, 2.0, 0])
        lb = T("ERK", 32, BLUE).move_to([-1.5, 2.0, 0])
        lp = T("activator", 32, PURPLE).move_to([-1.2, 1.5, 0])
        self.at("run down a column")
        self.play(FadeIn(dB), FadeIn(dP), FadeIn(lb), FadeIn(lp), run_time=0.5)
        self.play(dB.animate.move_to([-3.6, 0.7, 0]), dP.animate.move_to([-3.6, 0.7, 0]),
                  lb.animate.move_to([-1.5, 0.9, 0]), lp.animate.move_to([-1.2, 0.4, 0]), run_time=1.0)
        self.at("comes apart")
        self.play(dB.animate.move_to([-3.6, 1.0, 0]), dP.animate.move_to([-3.6, -1.1, 0]),
                  lb.animate.move_to([-1.5, 1.0, 0]), lp.animate.move_to([-1.2, -1.1, 0]), run_time=1.0)
        ide = T("idealised", 26, GREY).move_to([-3.6, -3.25, 0])
        self.play(FadeIn(ide), run_time=0.3)
        self.at("different protein")
        diff = chip("a different protein", PURPLE, 36).move_to([3.4, 1.6, 0])
        da = arr(lp.get_right() + [0.15, 0.1, 0], diff.get_bottom() + [-0.5, -0.1, 0], PURPLE)
        self.play(FadeIn(diff, shift=LEFT * 0.2), GrowArrow(da), run_time=0.7)
        self.at("not switching itself")
        erk = chip("ERK", BLUE, 52).move_to([3.4, -1.2, 0])
        loop = CurvedArrow(erk.get_top() + [0.6, 0.05, 0], erk.get_top() + [-0.6, 0.05, 0], angle=TAU / 4 * 1.4, color=BLUE)
        self.play(FadeIn(erk, scale=0.8), Create(loop), run_time=0.7)
        x = cross(loop.get_center() + [0, 0.15, 0], 0.4)
        sw = T("switching itself on", 28, RED).next_to(erk, DOWN, buff=0.45)
        self.play(Create(x), FadeIn(sw), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Purified(SpokenScene):
    def construct(self):
        act = chip("activator", PURPLE, 44).move_to([-3.5, 0.3, 0])
        erk = chip("ERK", BLUE, 52).move_to([3.5, 0.3, 0])
        self.play(FadeIn(act, scale=0.8), FadeIn(erk, scale=0.8), run_time=0.5)
        tag = T("Natalie Ahn, with Rony Seger", 26, GREY).next_to(act, DOWN, buff=0.4)
        self.at("purified the activator")
        self.play(FadeIn(tag), Indicate(act, color=PURPLE, scale_factor=1.12), run_time=0.7)
        pa = arr(act.get_right() + [0.05, 0, 0], erk.get_left() + [-0.05, 0, 0], PURPLE)
        self.at("phosphorylates")
        self.play(GrowArrow(pa), run_time=0.5)
        b1, b2 = pbadge(), pbadge()
        b1.move_to(act.get_top() + [0.6, 0.5, 0]); b2.move_to(act.get_top() + [0.6, 0.5, 0])
        t1 = T("threonine", 26, GOLD).move_to([2.6, 1.9, 0])
        t2 = T("tyrosine", 26, GOLD).move_to([4.4, 1.9, 0])
        self.at("threonine")
        self.play(FadeIn(b1), run_time=0.2)
        self.play(b1.animate.move_to([2.6, 1.2, 0]), FadeIn(t1), run_time=0.6)
        self.at("tyrosine")
        self.play(FadeIn(b2), run_time=0.2)
        self.play(b2.animate.move_to([4.4, 1.2, 0]), FadeIn(t2), run_time=0.6)
        labs = VGroup(*[chip("lab", GREY, 26).move_to([-6.0, y, 0]) for y in (1.7, 0.3, -1.1)])
        las = VGroup(*[arr(l.get_right() + [0.05, 0, 0], [-4.95, 0.3 + (l.get_center()[1] - 0.3) * 0.3, 0], GREY) for l in labs])
        self.at("Several laboratories")
        self.play(FadeOut(tag), FadeOut(pa), FadeIn(labs, shift=RIGHT * 0.2), FadeIn(las), run_time=0.7)
        mek = chip("MEK", PURPLE, 52).move_to(act)
        self.at("now called")
        self.play(ReplacementTransform(act, mek), FadeOut(labs), FadeOut(las), run_time=0.7)

        # chain
        raf = chip("Raf", ORANGE, 52).move_to([-4.6, 0.3, 0])
        erk_g = VGroup(erk, b1, b2, t1, t2)
        self.at("sits between")
        self.play(mek.animate.move_to([0, 0.3, 0]), erk_g.animate.shift([1.0, 0, 0]), FadeIn(raf, shift=RIGHT * 0.2), run_time=0.9)
        ra = arr(raf.get_right() + [0.05, 0, 0], mek.get_left() + [-0.05, 0, 0], ORANGE)
        ma = arr(mek.get_right() + [0.05, 0, 0], erk.get_left() + [-0.05, 0, 0], PURPLE)
        self.play(GrowArrow(ra), GrowArrow(ma), run_time=0.5)
        on = T("active", 28, GREEN, weight=BOLD).next_to(erk, DOWN, buff=0.35)
        self.at("needs both")
        self.play(FadeIn(on, shift=UP * 0.1), Indicate(b1, color=GOLD), Indicate(b2, color=GOLD), run_time=0.7)
        self.at("either one off")
        off = T("quiet", 28, GREY, weight=BOLD).move_to(on)
        self.play(b2.animate.shift([0.8, 0.9, 0]).set_opacity(0), FadeOut(t2), run_time=0.6)
        self.play(ReplacementTransform(on, off), run_time=0.4)
        self.at("comes apart from")
        two = T("two different proteins", 30, TEXT)
        br = Brace(VGroup(mek, erk), DOWN, color=GREY, buff=0.9)
        two.next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(two), run_time=0.6)
        self.finish()


class S05End(EndCard):
    LINE = "An activator that comes apart from ERK is a different protein."
