"""A reflex is not the pain  (Biochemistrypedia explainer for 'When Pain Persists')

COLOR MAP (one color per concept, whole video)
  PURPLE = the basolateral amygdala ensemble (outline = identified, filled = active)
  BLUE   = withdrawal reflex (the measured endpoint)
  ORANGE = escape and avoidance (the affective-motivational endpoint)
  YELLOW = noxious stimulus
  TEAL   = innocuous stimulus
  GOLD   = the genetic tag
  RED    = silenced / not shown
  GREY   = other cells, frames, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

# cells are a schematic; positions are unit-box layout, not data
POS = [(-3.2, 1.4), (-1.6, 1.2), (0.0, 1.5), (1.6, 1.3), (3.2, 1.4),
       (-3.1, 0.0), (-1.7, -0.2), (0.0, 0.1), (1.7, -0.1), (3.0, 0.2),
       (-3.2, -1.4), (-1.5, -1.5), (0.1, -1.3), (1.5, -1.5), (3.1, -1.4)]
ENS = [1, 4, 6, 9, 12, 14]
BOXW, BOXH = 8.0, 4.8


def cell(p):
    soma = Circle(radius=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
    stubs = VGroup(*[Line(ORIGIN, 0.26 * np.array([np.cos(a), np.sin(a), 0]), color=GREY, stroke_width=3)
                     .shift(0.3 * np.array([np.cos(a), np.sin(a), 0])) for a in (0.5, 2.4, 4.2)])
    g = VGroup(soma, stubs)
    g.move_to([p[0], p[1] - 0.3, 0])
    return g


def make_box(center, scale=1.0):
    frame = RoundedRectangle(corner_radius=0.3, width=BOXW, height=BOXH, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.05).move_to([0, -0.3, 0])
    cells = [cell(p) for p in POS]
    g = VGroup(frame, *cells)
    g.scale(scale).move_to(center)
    g.frame, g.cells = frame, cells
    return g


def style(c, state):
    """state: grey | ident | lit | silent"""
    soma, stubs = c[0], c[1]
    if state == "grey":
        return [soma.animate.set_stroke(GREY).set_fill(GREY, 0.12), stubs.animate.set_color(GREY)]
    if state == "ident":
        return [soma.animate.set_stroke(PURPLE).set_fill(PURPLE, 0.1), stubs.animate.set_color(PURPLE)]
    if state == "lit":
        return [soma.animate.set_stroke(PURPLE).set_fill(PURPLE, 0.95), stubs.animate.set_color(PURPLE)]
    if state == "silent":
        return [soma.animate.set_stroke(PURPLE, opacity=0.5).set_fill(PURPLE, 0.0), stubs.animate.set_color(PURPLE).set_opacity(0.4)]


def setstyle(c, state):
    soma, stubs = c[0], c[1]
    if state == "grey":
        soma.set_stroke(GREY).set_fill(GREY, 0.12); stubs.set_color(GREY)
    elif state == "ident":
        soma.set_stroke(PURPLE).set_fill(PURPLE, 0.1); stubs.set_color(PURPLE)
    elif state == "lit":
        soma.set_stroke(PURPLE).set_fill(PURPLE, 0.95); stubs.set_color(PURPLE)


def ring(c, color=GOLD):
    return Circle(radius=c[0].width / 2 + 0.12, stroke_color=color, stroke_width=4).move_to(c[0])


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


MY0 = -2.2  # meter bottom
MH = 3.3


def meter_fill(x, color, level, w=1.1):
    r = Rectangle(width=w - 0.1, height=max(0.02, MH * level), stroke_width=0, fill_color=color, fill_opacity=0.85)
    r.move_to([x, MY0 + max(0.02, MH * level) / 2, 0])
    return r


def meter(x, color, label, level, w=1.1):
    frame = Rectangle(width=w, height=MH + 0.1, stroke_color=color, stroke_width=3).move_to([x, MY0 + MH / 2 - 0.0 + 0.0, 0])
    frame.move_to([x, MY0 + (MH + 0.1) / 2 - 0.05, 0])
    fill = meter_fill(x, color, level, w)
    lab = T(label, 24, color).next_to(frame, DOWN, buff=0.18)
    return VGroup(frame, fill, lab)


class S00Title(TitleCard):
    LESSON = "When pain persists"
    TITLE = "A reflex is not the pain"


DASH_X = 4.7
BM_X = 1.9
CL_C = [-3.2, -0.2, 0]
CL_S = 0.75


def dashed_q():
    box = RoundedRectangle(corner_radius=0.25, width=1.7, height=MH + 0.1, stroke_color=ORANGE, stroke_width=3)
    box = DashedVMobject(box, num_dashes=36)
    qm = T("?", 90, ORANGE, weight=BOLD)
    cy = MY0 + (MH + 0.1) / 2 - 0.05
    box.move_to([DASH_X, cy, 0])
    qm.move_to(box.get_center())
    lab = T("unpleasant\nexperience", 24, ORANGE).next_to(box, DOWN, buff=0.18)
    return VGroup(box, qm, lab)


class S01Reflex(SpokenScene):
    def construct(self):
        inj = chip("nerve injury", GREY, size=24).to_corner(UL, buff=0.6)
        self.play(FadeIn(inj), run_time=0.5)
        touch = chip("touch", TEXT, size=28).move_to([-3.4, -0.4, 0])
        m = meter(BM_X, BLUE, "withdrawal\nreflex", 0.0)
        self.at("a touch makes")
        self.play(FadeIn(touch, shift=RIGHT * 0.2), run_time=0.5)
        a = arr(touch.get_right() + RIGHT * 0.05, [BM_X - 1.0, -0.4, 0], TEXT)
        self.play(GrowArrow(a), FadeIn(m), run_time=0.7)
        paw = T("paw pulls away", 24, BLUE).next_to(m[0], UP, buff=0.2)
        self.play(Transform(m[1], meter_fill(BM_X, BLUE, 0.8)), FadeIn(paw), run_time=0.8)
        self.at("cheap to measure")
        self.play(Indicate(m[0], color=BLUE, scale_factor=1.05), run_time=0.7)
        self.at("unpleasant experience")
        q = dashed_q()
        self.play(FadeIn(q, scale=0.9), run_time=0.8)
        self.at("Most pain assays")
        tag = T("what most pain assays record", 24, TEXT).move_to([BM_X, 3.0, 0])
        br = Line([BM_X - 1.2, 2.55, 0], [BM_X + 1.2, 2.55, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(tag), Create(br), run_time=0.7)
        self.at("where does the second")
        self.play(Indicate(q[1], color=ORANGE, scale_factor=1.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Two(SpokenScene):
    def construct(self):
        m1 = meter(BM_X, BLUE, "withdrawal\nreflex", 0.8)
        q = dashed_q()
        self.add(m1, q)
        self.wait(0.3)
        self.at("defined set of neurons")
        box = make_box(CL_C, CL_S)
        cap = T("a defined set of neurons?", 24, PURPLE).next_to(box.frame, UP, buff=0.2)
        self.play(FadeIn(box), FadeIn(cap), run_time=0.8)
        self.at("second measurement")
        self.play(Indicate(q[1], color=ORANGE, scale_factor=1.25), run_time=0.8)
        self.at("male mice")
        c1 = chip("male mice", GREY, size=24)
        c2 = chip("nerve-injury model", GREY, size=24)
        VGroup(c1, c2).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.35)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.7)
        self.at("Two endpoints can")
        head = T("two measured endpoints", 24, GREY).move_to([3.3, 2.5, 0])
        self.play(FadeIn(head), run_time=0.5)
        self.at("withdrawal reflex")
        self.play(Indicate(m1[0], color=BLUE, scale_factor=1.05), run_time=0.6)
        self.at("such as escape")
        m2 = meter(5.5, ORANGE, "affective-\nmotivational\nendpoint", 0.8)
        m2[2].scale(22 / 24)
        self.play(m1.animate.shift(LEFT * 0.7), q.animate.shift(LEFT * 1.3), head.animate.shift(LEFT * 0.8), run_time=0.6)
        self.play(FadeIn(m2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Ensemble(SpokenScene):
    def construct(self):
        title = T("Basolateral amygdala, in male mice", 30, font=TITLE_FONT).move_to([1.2, 3.0, 0])
        box = make_box([1.2, -0.3, 0], 1.0)
        self.at("principal neurons")
        self.play(Write(title), FadeIn(box), run_time=1.2)
        self.at("repeated sessions")
        im = T("imaging, repeated sessions; cells drawn for illustration", 22, GREY).move_to([1.2, -3.2, 0])
        self.play(FadeIn(im), box.frame.animate.set_stroke(TEAL), run_time=0.4)
        self.play(box.frame.animate.set_stroke(GREY), run_time=0.3)
        self.play(box.frame.animate.set_stroke(TEAL), run_time=0.3)
        self.play(box.frame.animate.set_stroke(GREY), run_time=0.3)
        self.at("identified an ensemble")
        ens = chip("ensemble", PURPLE, size=26).move_to([-4.7, 0.1, 0])
        self.play(*[a for i in ENS for a in style(box.cells[i], "ident")], FadeIn(ens), run_time=0.8)
        self.at("responded to noxious")
        stim = chip("noxious\nstimulus", YELLOW, size=24).move_to([-4.7, 1.7, 0])
        a = arr(stim.get_right() + RIGHT * 0.05, [-2.9, 1.2, 0], YELLOW)
        self.play(FadeIn(stim), GrowArrow(a), run_time=0.5)
        self.play(*[a2 for i in ENS for a2 in style(box.cells[i], "lit")], run_time=0.6)
        self.at("negative valence")
        val = chip("negative\nvalence", PURPLE, size=24).move_to([-4.7, -1.5, 0])
        self.play(FadeIn(val, shift=UP * 0.1), run_time=0.6)
        self.at("how bad or good")
        ln = Line([-6.0, -2.7, 0], [-3.4, -2.7, 0], color=GREY, stroke_width=3)
        bad = T("bad", 22, GREY).next_to(ln, UP, buff=0.12).align_to(ln, LEFT)
        good = T("good", 22, GREY).next_to(ln, UP, buff=0.12).align_to(ln, RIGHT)
        dot = Dot([-5.8, -2.7, 0], color=PURPLE, radius=0.12)
        self.play(Create(ln), FadeIn(bad), FadeIn(good), FadeIn(dot), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Injury(SpokenScene):
    def construct(self):
        title = T("Basolateral amygdala, in male mice", 30, font=TITLE_FONT).move_to([1.2, 3.0, 0])
        box = make_box([1.2, -0.3, 0], 1.0)
        for i in ENS:
            setstyle(box.cells[i], "ident")
        ens = chip("ensemble", PURPLE, size=26).move_to([-4.7, 0.1, 0])
        val = chip("negative\nvalence", PURPLE, size=24).move_to([-4.7, -1.5, 0])
        self.add(title, box, ens, val)
        self.wait(0.3)
        self.at("nerve injury in these")
        inj = chip("after nerve injury", GREY, size=26).move_to([1.2, 3.0, 0])
        self.play(FadeOut(title), FadeIn(inj), run_time=0.6)
        self.at("innocuous stimuli also")
        stim = chip("innocuous\nstimulus", TEAL, size=24).move_to([-4.7, 1.7, 0])
        a = arr(stim.get_right() + RIGHT * 0.05, [-2.9, 1.2, 0], TEAL)
        self.play(FadeIn(stim), GrowArrow(a), run_time=0.5)
        self.play(*[a2 for i in ENS for a2 in style(box.cells[i], "lit")], run_time=0.6)
        self.at("normally not painful")
        note = T("normally not painful", 22, TEAL).next_to(stim, UP, buff=0.15)
        self.play(FadeIn(note), run_time=0.5)
        self.at("encoded negative valence")
        self.play(Indicate(ens, color=PURPLE, scale_factor=1.12), Indicate(val, color=PURPLE, scale_factor=1.12),
                  run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Silence(SpokenScene):
    def construct(self):
        inj = chip("nerve injury", GREY, size=24).to_corner(UL, buff=0.6)
        box = make_box([1.2, -0.3, 0], 1.0)
        for i in ENS:
            setstyle(box.cells[i], "lit")
        ens = chip("ensemble", PURPLE, size=26).move_to([-4.7, 0.1, 0])
        self.add(box, ens)
        self.wait(0.3)
        self.play(box.animate.scale(CL_S).move_to(CL_C), FadeOut(ens), FadeIn(inj), run_time=1.2)
        self.at("endpoints could")
        m1 = meter(BM_X, BLUE, "withdrawal\nreflex", 0.8)
        m2 = meter(DASH_X, ORANGE, "escape and\navoidance", 0.8)
        note = T("schematic, heights not data", 22, GREY).move_to([3.3, -3.45, 0])
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(note), run_time=0.8)
        self.at("tagged the active")
        rings = VGroup(*[ring(box.cells[i]) for i in ENS])
        tg = chip("tagged", GOLD, size=24).next_to(box.frame, UP, buff=0.25)
        self.play(Create(rings), FadeIn(tg), run_time=0.8)
        self.at("silenced the tagged")
        sil = T("silenced", 26, RED, weight=BOLD).move_to(tg)
        self.play(*[a for i in ENS for a in style(box.cells[i], "silent")], FadeOut(rings), FadeOut(tg), FadeIn(sil), run_time=0.9)
        self.at("behaviors fell")
        self.play(Transform(m2[1], meter_fill(DASH_X, ORANGE, 0.15)), run_time=1.0)
        fell = T("fell", 26, ORANGE, weight=BOLD).next_to(m2[0], UP, buff=0.15)
        self.play(FadeIn(fell), run_time=0.3)
        self.at("reflexes were preserved")
        pres = T("preserved", 26, BLUE, weight=BOLD).next_to(m1[0], UP, buff=0.15)
        self.play(FadeIn(pres), Indicate(m1[1], color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("came apart")
        br = Line([BM_X - 0.6, 2.35, 0], [DASH_X + 0.6, 2.35, 0], color=TEXT, stroke_width=3)
        sep = T("two endpoints, separated", 24, TEXT).next_to(br, UP, buff=0.12)
        self.play(Create(br), FadeIn(sep), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Scope(SpokenScene):
    def construct(self):
        # carry over the end of the last scene, then clear it when the scope begins
        box = make_box(CL_C, CL_S)
        for i in ENS:
            setstyle(box.cells[i], "silent")
            box.cells[i][0].set_stroke(PURPLE, opacity=0.5).set_fill(PURPLE, 0.0)
            box.cells[i][1].set_color(PURPLE).set_opacity(0.4)
        sil = T("silenced", 26, RED, weight=BOLD).next_to(box.frame, UP, buff=0.25)
        m1 = meter(BM_X, BLUE, "withdrawal\nreflex", 0.8)
        m2 = meter(DASH_X, ORANGE, "escape and\navoidance", 0.15)
        pres = T("preserved", 26, BLUE, weight=BOLD).next_to(m1[0], UP, buff=0.15)
        fell = T("fell", 26, ORANGE, weight=BOLD).next_to(m2[0], UP, buff=0.15)
        inj = chip("nerve injury", GREY, size=24).to_corner(UL, buff=0.6)
        note = T("schematic, heights not data", 22, GREY).move_to([3.3, -3.45, 0])
        old = VGroup(box, sil, m1, m2, pres, fell, inj, note)
        self.add(old)
        self.wait(0.2)
        self.at("male mice")
        c1 = chip("male mice", GREY, size=24)
        c2 = chip("nerve-injury model", GREY, size=24)
        c3 = chip("behaviours the authors chose", GREY, size=24)
        VGroup(c1, c2, c3).arrange(RIGHT, buff=0.25).move_to([0, 3.1, 0])
        self.play(FadeOut(old), FadeIn(c1), run_time=0.6)
        self.at("nerve injury model")
        self.play(FadeIn(c2), run_time=0.4)
        self.at("authors chose")
        self.play(FadeIn(c3), run_time=0.4)
        self.at("verbal report")
        nv = T("a mouse gives no verbal report", 24, GREY).move_to([0, 2.4, 0])
        self.play(FadeIn(nv), run_time=0.5)
        self.at("measurable endpoints")
        h1 = T("It shows", 28, TEXT, weight=BOLD).move_to([-3.3, 1.65, 0])
        r1 = chip("reflex preserved", BLUE, size=24)
        r2 = chip("escape and avoidance fell", ORANGE, size=24)
        r1.move_to([-3.3, 0.75, 0])
        r2.move_to([-3.3, -0.4, 0])
        self.play(FadeIn(h1), FadeIn(r1), run_time=0.5)
        self.play(FadeIn(r2), run_time=0.5)
        self.at("unpleasantness is made")
        h2 = T("It does not show", 28, TEXT, weight=BOLD).move_to([3.3, 1.65, 0])
        x1 = chip("unpleasantness is made\nin the basolateral amygdala", RED, size=24).move_to([3.3, 0.75, 0])
        x2 = chip("silencing abolishes\nsensing the stimulus", RED, size=24).move_to([3.3, -0.4, 0])
        x3 = chip("anything about\nother regions", RED, size=24).move_to([3.3, -1.55, 0])
        self.play(FadeIn(h2), FadeIn(x1), run_time=0.5)
        self.at("abolishes sensing")
        self.play(FadeIn(x2), run_time=0.4)
        self.at("other regions")
        self.play(FadeIn(x3), run_time=0.4)
        self.at("Keep this rule")
        rule = T("A withdrawal reflex is not a measure\nof how unpleasant a stimulus is.", 30, TEXT, font=TITLE_FONT)
        rule.move_to([0, -3.0, 0])
        fit(rule)
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "A withdrawal reflex is not a measure of unpleasantness."
