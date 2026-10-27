"""Control of breathing: carbon dioxide sets the breath  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Every number on screen is the lesson's own. Plots are shape sketches ("in this sketch", relative units):
  carbon dioxide line  V = 2 + 0.5 (PCO2 - 40)                      (roughly straight, per the lesson)
  oxygen curve         V = 2 + 0.5 exp((60 - PO2) / 8)             (shallow above 60, steepens toward 50-60)
Both are drawn so that the resting point (PCO2 about 40, PO2 about 100 mmHg, adult at rest at sea level)
sits at the same relative ventilation. Nothing in them is a measurement; no slope is stated.
Scene 6 uses the lesson's own means (Pernett and colleagues, 18 volunteers, face in cold water).

COLOR MAP (one color per concept, whole video)
  TEAL   = carbon dioxide and its signal (PCO2)
  ORANGE = oxygen and its signal (PO2)
  PURPLE = hydrogen ions
  BLUE   = the brainstem controller (pre-Botzinger complex, retrotrapezoid nucleus)
  GREEN  = ventilation, the size of the drive
  YELLOW = the resting point, and what to look at
  RED    = removed or stopped (and nothing else)
  GREY   = structure, axes, hedges
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

BLUE = "#6F8CF5"      # the brainstem controller (deeper than the house cyan, which sits too close to TEAL)
ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
CO2 = "CO₂"
PCO2 = "PCO₂"
PO2 = "PO₂"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def btext(text, size=24, color=GREY, **kw):
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def cross(center, s=0.3, color=RED, w=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


class S00Title(TitleCard):
    LESSON = "Control of breathing, altitude and diving"
    TITLE = "Carbon dioxide sets the breath"


# ---------------------------------------------------------------------------------------------
# the two response plots, shared by scenes 4 and 5 (same place both times)
# ---------------------------------------------------------------------------------------------
class Plot:
    def __init__(self, x0, x1, y0, y1, xmin, xmax, ymax):
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.xmin, self.xmax, self.ymax = xmin, xmax, ymax

    def pt(self, x, v):
        return np.array([self.x0 + (x - self.xmin) / (self.xmax - self.xmin) * (self.x1 - self.x0),
                         self.y0 + v / self.ymax * (self.y1 - self.y0), 0.0])

    def axes(self):
        return VGroup(Line([self.x0, self.y0, 0], [self.x1 + 0.1, self.y0, 0], color=GREY, stroke_width=3),
                      Line([self.x0, self.y0, 0], [self.x0, self.y1 + 0.1, 0], color=GREY, stroke_width=3))

    def curve(self, f, a, b, color, w=7, n=40):
        xs = np.linspace(a, b, n)
        m = VMobject(color=color, stroke_width=w)
        m.set_points_smoothly([self.pt(x, f(x)) for x in xs])
        return m

    def tick(self, x, label, color=GREY):
        p = self.pt(x, 0)
        return VGroup(Line(p, p + DOWN * 0.1, color=GREY, stroke_width=2),
                      M(label, 22, color).move_to(p + DOWN * 0.38))


def f_co2(p):
    return 2 + 0.5 * (p - 40)


def f_o2(p):
    return 2 + 0.5 * np.exp((60 - p) / 8)


PL = Plot(-5.6, -0.8, -1.5, 2.4, 36, 56, 8.5)
PR = Plot(1.6, 6.1, -1.5, 2.4, 40, 105, 8.5)


def plot_frames():
    """axes, titles, axis labels for both plots."""
    left = VGroup(
        PL.axes(),
        T("against arterial " + PCO2, 24, TEAL).move_to([-3.2, 3.25, 0]),
        T("relative units, in this sketch", 22, GREY).move_to([-3.2, 2.85, 0]),
        T("arterial " + PCO2 + " (mmHg)", 22, GREY).move_to([-3.2, -2.35, 0]),
        T("ventilation", 22, GREEN).rotate(PI / 2).move_to([-6.1, 0.45, 0]),
    )
    right = VGroup(
        PR.axes(),
        T("against alveolar " + PO2, 24, ORANGE).move_to([3.85, 3.25, 0]),
        T("relative units, in this sketch", 22, GREY).move_to([3.85, 2.85, 0]),
        T("alveolar " + PO2 + " (mmHg)", 22, GREY).move_to([3.85, -2.35, 0]),
        T("ventilation", 22, GREEN).rotate(PI / 2).move_to([1.1, 0.45, 0]),
    )
    return left, right


def line_co2():
    return PL.curve(f_co2, 37, 52, TEAL, 7, 12)


def curve_o2_a():
    return PR.curve(f_o2, 105, 60, ORANGE, 7, 40)


def curve_o2_b():
    return PR.curve(f_o2, 60, 40.6, ORANGE, 7, 40)


def o2_band():
    a, b = PR.pt(50, 0), PR.pt(60, 8.5)
    r = Rectangle(width=b[0] - a[0], height=b[1] - a[1], stroke_width=0, fill_color=ORANGE, fill_opacity=0.16)
    return r.move_to((a + b) / 2)


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """breath held: a carbon dioxide gauge rises, an oxygen gauge falls, a question over the controller."""

    def gauge(self, x, color, level):
        tube = RoundedRectangle(corner_radius=0.2, width=1.3, height=4.2, stroke_color=GREY, stroke_width=3)
        tube.move_to([x, -0.2, 0])
        return tube, self.fill(x, color, level)

    def fill(self, x, color, level):
        h = 4.0 * level
        r = Rectangle(width=1.1, height=h, stroke_width=0, fill_color=color, fill_opacity=0.7)
        return r.move_to([x, -2.3 + 0.1 + h / 2, 0])

    def construct(self):
        top = bchip("breath held, airway closed", GREY, 26).move_to([0, 3.05, 0])
        t1, f1 = self.gauge(-4.0, TEAL, 0.25)
        t2, f2 = self.gauge(4.0, ORANGE, 0.9)
        l1 = T("carbon dioxide", 28, TEAL).move_to([-4.0, 2.4, 0])
        l2 = T("oxygen", 28, ORANGE).move_to([4.0, 2.4, 0])
        self.at("Hold your breath")
        self.play(FadeIn(top, shift=DOWN * 0.15), Create(t1), Create(t2), FadeIn(l1), FadeIn(l2), FadeIn(f1), FadeIn(f2),
                  run_time=1.0)

        self.at("dioxide accumulates")
        a1 = arr([-5.2, -1.2, 0], [-5.2, 1.0, 0], TEAL, 7)
        n1 = self.fill(-4.0, TEAL, 0.85)
        self.play(Transform(f1, n1), GrowArrow(a1), run_time=2.0)
        self.at("and oxygen falls")
        a2 = arr([5.2, 1.0, 0], [5.2, -1.2, 0], ORANGE, 7)
        n2 = self.fill(4.0, ORANGE, 0.55)
        self.play(Transform(f2, n2), GrowArrow(a2), run_time=1.6)

        self.at("mostly the carbon dioxide")
        ring = SurroundingRectangle(VGroup(t1, l1), color=YELLOW, buff=0.2, stroke_width=5, corner_radius=0.2)
        most = T("mostly", 28, YELLOW, weight=BOLD).move_to([-4.0, -3.05, 0])
        self.play(Create(ring), FadeIn(most, shift=UP * 0.1), run_time=0.8)
        self.at("not oxygen running out")
        self.play(*[m.animate.set_opacity(0.35) for m in (t2, f2, l2, a2)], run_time=0.8)

        self.at("Why is the controller")
        ctrl = bchip("the controller", BLUE, 34, pad=0.3).move_to([0, -0.2, 0])
        c1 = arr([-3.2, -0.2, 0], ctrl.get_left() + LEFT * 0.05, TEAL, 6)
        c2 = arr([3.2, -0.2, 0], ctrl.get_right() + RIGHT * 0.05, ORANGE, 6)
        c2.set_opacity(0.35)
        self.play(FadeIn(ctrl, scale=0.9), GrowArrow(c1), GrowArrow(c2), run_time=0.8)
        self.at("built that way")
        q = T("?", 96, YELLOW, weight=BOLD).move_to([0, 1.5, 0])
        self.play(FadeIn(q, scale=0.6), Indicate(VGroup(*ctrl[1:]), color=YELLOW, scale_factor=1.08), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Rhythm(SpokenScene):
    """a medulla block with the pre-Botzinger complex sending a rhythm to the muscles; chemistry sets its size."""

    def construct(self):
        head = T("control of breathing", 36, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.at("Two questions")
        self.play(Write(head), run_time=0.7)
        q1 = bchip("1  rhythm:\nwhere does it come from?", BLUE, 26).move_to([-3.1, 1.95, 0])
        q2 = bchip("2  drive:\nwhat sets how hard?", GREEN, 26).move_to([3.5, 1.95, 0])
        self.at("where does the rhythm")
        self.play(FadeIn(q1, shift=UP * 0.15), FadeIn(q2, shift=UP * 0.15), run_time=0.5)

        box = RoundedRectangle(corner_radius=0.3, width=6.0, height=3.2, stroke_color=GREY, stroke_width=3).move_to([-3.1, -1.1, 0])
        box_l = T("medulla", 24, GREY).move_to([-5.3, 0.1, 0])
        pre = bchip("pre-Botzinger complex", BLUE, 28).move_to([-3.1, -1.3, 0])
        mus = bchip("diaphragm,\nintercostals", GREY, 26).move_to([4.6, -1.1, 0])
        a0 = arr([-0.1, -1.1, 0], mus.get_left() + LEFT * 0.05, GREY, 6)
        out = arr([-0.1, -1.1, 0], mus.get_left() + LEFT * 0.05, GREY, 6)
        qm = T("?", 90, YELLOW, weight=BOLD).move_to([-3.1, -1.2, 0])
        rl = T("rhythm", 26, BLUE).move_to([1.5, -0.55, 0])
        self.at("come from")
        self.play(Indicate(q1, color=BLUE, scale_factor=1.06), Create(box), FadeIn(box_l), FadeIn(qm, scale=0.6),
                  FadeIn(mus), GrowArrow(out), run_time=0.9)
        self.at("what sets how hard")
        self.play(Indicate(q2, color=GREEN, scale_factor=1.06), run_time=0.7)
        self.at("from the medulla")
        self.play(Indicate(box, color=YELLOW, scale_factor=1.02), run_time=0.7)
        self.at("a small region")
        blue_out = arr([-0.1, -1.1, 0], mus.get_left() + LEFT * 0.05, BLUE, 6)
        self.play(FadeOut(qm), FadeIn(pre, scale=0.9), Transform(out, blue_out), FadeIn(rl), run_time=0.8)
        pulses = [Dot([-0.1, -1.1, 0], radius=0.11, color=BLUE) for _ in range(2)]
        self.play(LaggedStart(*[d.animate.move_to([3.3, -1.1, 0]).set_opacity(0) for d in pulses], lag_ratio=0.5),
                  *[FadeIn(d) for d in pulses], run_time=1.2)

        # the rat preparation
        prep = T("neonatal rat brainstem, in a dish", 24, GREY).move_to([-3.1, -3.1, 0])
        self.at("Smith and colleagues")
        self.play(FadeIn(prep), run_time=0.5)
        ghost = DashedVMobject(pre[1].copy().set_fill(opacity=0), num_dashes=40).set_color(RED)
        stop = T("output stops", 26, RED).move_to([1.5, -1.75, 0])
        self.at("found it")
        grey_out = arr([-0.1, -1.1, 0], mus.get_left() + LEFT * 0.05, GREY, 6)
        self.play(FadeOut(pre), FadeIn(ghost), Transform(out, grey_out), FadeOut(rl), FadeIn(stop), run_time=0.8)
        self.at("reduced preparation")
        note = T("a reduced preparation,\nnot the adult human circuit", 24, YELLOW, line_spacing=0.9).move_to([3.4, 0.45, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.at("adult human circuit")
        self.play(Indicate(note, color=YELLOW, scale_factor=1.04), run_time=0.6)

        # back to the whole story: chemistry sets the size
        self.at("At rest")
        self.play(FadeOut(ghost), FadeOut(stop), FadeOut(note), FadeOut(prep), FadeIn(pre), Transform(out, blue_out),
                  FadeIn(rl), run_time=0.8)
        self.at("largely chemical")
        chem = bchip("chemistry", GREEN, 28).move_to([1.5, -2.75, 0])
        up = arr(chem.get_top() + UP * 0.02, [1.5, -1.3, 0], GREEN, 6)
        big = arr([-0.1, -1.1, 0], mus.get_left() + LEFT * 0.05, GREEN, 16, tip=0.4)
        sz = T("size of the drive", 26, GREEN).move_to([1.5, -0.55, 0])
        self.play(FadeIn(chem, shift=UP * 0.2), GrowArrow(up), run_time=0.7)
        self.play(Transform(out, big), ReplacementTransform(rl, sz), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Sensors(SpokenScene):
    """left: CO2 crosses into brain fluid and is sensed as H+; right: the carotid body senses arterial oxygen."""

    def construct(self):
        blood = Rectangle(width=5.6, height=0.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([-3.3, -3.0, 0])
        blood_l = T("blood", 24, GREY).move_to([-5.5, -3.0, 0])
        barrier = Rectangle(width=5.6, height=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([-3.3, -1.95, 0])
        barrier_l = T("blood-brain barrier", 22, TEXT).move_to(barrier)
        brain = Rectangle(width=5.6, height=4.4, stroke_color=GREY, stroke_width=3).move_to([-3.3, 0.65, 0])
        brain_l = T("brain fluid", 22, GREY).move_to([-5.3, 2.6, 0])
        co2 = bchip("carbon dioxide", TEAL, 24).move_to([-3.3, -3.0, 0])
        self.at("Carbon dioxide crosses")
        self.play(FadeIn(blood), FadeIn(blood_l), FadeIn(barrier), FadeIn(barrier_l), Create(brain), FadeIn(brain_l),
                  FadeIn(co2), run_time=1.0)
        self.play(co2.animate.move_to([-3.3, -0.75, 0]), run_time=1.3)

        self.at("releases hydrogen ions")
        hs = [bchip("H⁺", PURPLE, 28).move_to([x, -0.75, 0]) for x in (-4.4, -3.3, -2.2)]
        lbl_h = T("hydrogen ions", 22, PURPLE).move_to([-3.3, -1.33, 0])
        self.play(ReplacementTransform(co2, hs[1]), FadeIn(hs[0], shift=LEFT * 0.3), FadeIn(hs[2], shift=RIGHT * 0.3), run_time=0.9)
        self.at("mainly senses")
        self.play(*[Indicate(h, color=PURPLE, scale_factor=1.12) for h in hs], FadeIn(lbl_h), run_time=0.9)
        self.at("not the molecule")
        ghost = bchip("CO₂", TEAL, 22).move_to([-1.1, -0.75, 0])
        x = T("not mainly", 22, GREY).move_to([-1.1, -0.2, 0])
        self.play(FadeIn(ghost.set_opacity(0.55)), FadeIn(x), run_time=0.7)

        self.at("In mice")
        rtn = bchip("retrotrapezoid\nnucleus", BLUE, 24).move_to([-3.3, 0.5, 0])
        mice = T("in mice", 22, GREY).move_to([-5.3, 0.5, 0])
        ar = [arr(h.get_top(), [h.get_center()[0], rtn.get_bottom()[1], 0], PURPLE, 4, 0.18) for h in hs]
        self.play(FadeIn(rtn, shift=DOWN * 0.15), FadeIn(mice), LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.2),
                  FadeOut(ghost), FadeOut(x), run_time=1.2)
        self.at("and project to")
        pre = bchip("pre-Botzinger\ncomplex", BLUE, 24).move_to([-3.3, 2.0, 0])
        pa = arr(rtn.get_top(), pre.get_bottom(), BLUE, 6)
        self.play(FadeIn(pre, shift=DOWN * 0.15), GrowArrow(pa), run_time=0.9)
        self.at("still open")
        q = T("?", 56, YELLOW, weight=BOLD).move_to([-1.3, 0.5, 0])
        which = T("which cells?", 22, YELLOW).move_to([-1.5, 1.15, 0])
        self.play(FadeIn(q, scale=0.6), FadeIn(which), run_time=0.7)

        # peripheral arm
        self.at("The carotid body")
        art = Line([2.2, -3.2, 0], [2.2, -0.8, 0], color=GREY, stroke_width=22)
        b1 = Line([2.2, -0.8, 0], [1.4, 1.1, 0], color=GREY, stroke_width=22)
        b2 = Line([2.2, -0.8, 0], [3.0, 1.1, 0], color=GREY, stroke_width=22)
        art_l = T("carotid\nartery", 22, GREY, line_spacing=0.85).move_to([0.95, -2.5, 0])
        body = bchip("carotid body", ORANGE, 24).move_to([4.2, -0.8, 0])
        link = Line([2.2, -0.8, 0], body.get_left(), color=GREY, stroke_width=4)
        self.play(Create(art), Create(b1), Create(b2), FadeIn(art_l), run_time=0.8)
        self.play(Create(link), FadeIn(body, shift=LEFT * 0.2), run_time=0.6)
        self.at("fork of each")
        self.play(Indicate(VGroup(art, b1, b2), color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.at("main peripheral")
        sig = arr(body.get_top() + UP * 0.02, [4.2, 2.1, 0], GREY, 6)
        to = T("to the\nbrainstem", 22, GREY, line_spacing=0.85).move_to([5.45, 1.3, 0])
        self.play(GrowArrow(sig), FadeIn(to), run_time=0.8)
        self.at("arterial oxygen")
        o2 = T("arterial oxygen", 24, ORANGE).move_to([4.7, -1.85, 0])
        co = T("carbon dioxide", 24, TEAL).move_to([4.7, -2.3, 0])
        ph = T("pH", 24, PURPLE).move_to([4.7, -2.75, 0])
        oa = arr([4.4, -1.55, 0], body.get_bottom() + DOWN * 0.02, GREY, 5)
        self.play(FadeIn(o2), GrowArrow(oa), run_time=0.7)
        self.at("carbon dioxide", nth=1)
        self.play(FadeIn(co), run_time=0.4)
        self.play(FadeIn(ph), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Curves(SpokenScene):
    """two response curves, drawn in turn; the isocapnia clamp; what happens without it."""

    def construct(self):
        left, right = plot_frames()
        self.at("Against arterial")
        self.play(FadeIn(left), run_time=0.8)
        line = line_co2()
        self.at("rises along")
        self.play(Create(line), run_time=1.2)
        self.at("roughly straight")
        rs = T("roughly straight", 24, TEAL).move_to([-1.95, 0.0, 0])
        self.play(FadeIn(rs), run_time=0.5)

        self.at("Against alveolar")
        self.play(FadeIn(right), FadeIn(PR.tick(50, "50")), FadeIn(PR.tick(60, "60")), run_time=0.8)
        ca, cb = curve_o2_a(), curve_o2_b()
        self.at("shallow above")
        self.play(Create(ca), run_time=1.5)
        band = o2_band()
        self.at("It steepens")
        self.play(FadeIn(band), Create(cb), run_time=1.4)
        st = T("steepens", 24, ORANGE).move_to([3.85, 2.0, 0])
        self.play(FadeIn(st), run_time=0.4)

        self.at("under isocapnia")
        clamp = bchip("isocapnia", TEAL, 26).move_to([3.85, -3.1, 0])
        self.play(FadeIn(clamp, shift=UP * 0.15), run_time=0.6)
        self.at("held alveolar")
        clamp2 = bchip("isocapnia: alveolar " + PCO2 + "\nheld at its resting value", TEAL, 22).move_to([3.85, -3.1, 0])
        self.play(FadeOut(clamp), run_time=0.3)
        self.play(FadeIn(clamp2), run_time=0.4)

        self.at("Without that clamp")
        c1 = bchip("breathing harder", GREEN, 24)
        c2 = bchip(PCO2 + " falls", TEAL, 24)
        c3 = bchip("ventilation", GREEN, 24)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.55).move_to([0, -3.1, 0])
        a1 = arr(c1.get_right(), c2.get_left(), GREY, 5)
        a2 = inhib(c2.get_right() + RIGHT * 0.06, c3.get_left() + LEFT * 0.06, RED, 6)
        self.play(FadeOut(clamp2), FadeIn(c1, shift=RIGHT * 0.2), run_time=0.7)
        self.at("harder lowers")
        self.play(GrowArrow(a1), FadeIn(c2), run_time=0.7)
        self.at("restrains")
        self.play(Create(a2), FadeIn(c3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Point(SpokenScene):
    """the resting point on each curve; a small error on each."""

    def construct(self):
        left, right = plot_frames()
        line = line_co2()
        ca, cb = curve_o2_a(), curve_o2_b()
        band = o2_band()
        ticks = VGroup(PR.tick(50, "50"), PR.tick(60, "60"))
        st = T("steepens", 24, ORANGE).move_to([3.85, 2.0, 0])
        self.add(left, right, line, ca, cb, band, ticks, st)
        # the earlier "roughly straight" label is not repeated; keep the line plain
        self.at("Take an adult")
        rest = bchip("adult at rest, sea level", GREY, 26).move_to([0, -3.1, 0])
        self.play(FadeIn(rest, shift=UP * 0.15), FadeOut(st), run_time=0.7)

        pL, pR = PL.pt(40, f_co2(40)), PR.pt(100, f_o2(100))
        dotL = Dot(pL, radius=0.17, color=YELLOW)
        dotR = Dot(pR, radius=0.17, color=YELLOW)
        gvL = DashedLine(PL.pt(40, 0), pL, color=YELLOW, stroke_width=3, dash_length=0.12)
        gvR = DashedLine(PR.pt(100, 0), pR, color=YELLOW, stroke_width=3, dash_length=0.12)
        tL = PL.tick(40, "40", YELLOW)
        tR = PR.tick(100, "100", YELLOW)
        self.at("Arterial", nth=0)
        self.play(Create(gvL), FadeIn(tL), FadeIn(dotL, scale=0.4), run_time=0.8)
        self.at("Arterial", nth=1)
        note_a = T("arterial value, read\non the alveolar axis", 22, GREY, line_spacing=0.85).move_to([4.7, 1.35, 0])
        self.play(Create(gvR), FadeIn(tR), FadeIn(dotR, scale=0.4), FadeIn(note_a), run_time=0.8)

        self.at("steep part")
        hl = PL.curve(f_co2, 38.4, 41.6, YELLOW, 11, 6)
        steep = T("steep", 26, YELLOW, weight=BOLD).move_to([-3.5, -0.8, 0])
        self.play(FadeIn(hl), FadeIn(steep), run_time=0.6)
        self.at("flat part")
        hr = PR.curve(f_o2, 95, 105, YELLOW, 11, 8)
        flat = T("flat", 26, YELLOW, weight=BOLD).move_to([5.0, 0.1, 0])
        self.play(FadeIn(hr), FadeIn(flat), run_time=0.6)

        # a small PCO2 error: large change
        self.at("A small", nth=0)
        newL = PL.pt(44, f_co2(44))
        yl = PL.pt(40, f_co2(40))
        h0 = DashedLine([PL.x0, yl[1], 0], yl, color=YELLOW, stroke_width=3, dash_length=0.12)
        h1 = DashedLine([PL.x0, newL[1], 0], newL, color=YELLOW, stroke_width=3, dash_length=0.12)
        br = DoubleArrow([PL.x0 + 0.3, yl[1], 0], [PL.x0 + 0.3, newL[1], 0], color=YELLOW, stroke_width=5, tip_length=0.18, buff=0)
        big = T("large change", 24, YELLOW).move_to([PL.x0 + 1.45, 1.45, 0])
        self.play(FadeOut(hl), FadeOut(steep), dotL.animate.move_to(newL), Create(h0), Create(h1), run_time=1.0)
        self.play(GrowFromCenter(br), FadeIn(big), run_time=0.6)

        # a small PO2 error: almost none
        self.at("A small", nth=1)
        newR = PR.pt(96, f_o2(96))
        h2 = DashedLine([PR.x0, pR[1], 0], pR, color=YELLOW, stroke_width=3, dash_length=0.12)
        self.play(FadeOut(hr), FadeOut(flat), dotR.animate.move_to(newR), Create(h2), run_time=1.0)
        none = T("almost none", 24, YELLOW).move_to([4.6, 0.1, 0])
        self.at("almost none")
        self.play(FadeIn(none, shift=UP * 0.1), run_time=0.5)

        self.at("leverage lies")
        lev = T("oxygen's leverage", 22, ORANGE).move_to([4.3, 2.0, 0])
        la = arr([3.3, 1.6, 0], [2.75, 1.05, 0], ORANGE, 4, 0.18)
        self.play(FadeIn(lev), GrowArrow(la), band.animate.set_fill(ORANGE, 0.32), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Hold(SpokenScene):
    """the breath hold: hyperventilation first lowers starting PCO2, lengthens the hold, lowers the saturation nadir."""

    def construct(self):
        # the break point, and the carbon dioxide signal usually arriving first (order only, not to scale)
        tl = Line([-5.4, 0.2, 0], [5.4, 0.2, 0], color=GREY, stroke_width=4)
        tla = arr([5.0, 0.2, 0], [5.8, 0.2, 0], GREY, 4)
        time_l = T("time in the breath hold", 24, GREY).move_to([-3.2, -0.3, 0])
        bpl = Line([4.6, 1.15, 0], [4.6, -0.25, 0], color=YELLOW, stroke_width=7)
        bp = bchip("apnea break point", YELLOW, 26).move_to([4.2, 1.6, 0])
        bpn = T("the breath hold ends", 24, GREY).move_to([4.2, -0.75, 0])
        m1 = bchip("carbon dioxide signal", TEAL, 28).move_to([-3.0, 1.6, 0])
        d1 = DashedLine([-3.0, 1.2, 0], [-3.0, 0.2, 0], color=TEAL, stroke_width=4, dash_length=0.12)
        usual = T("usually first, not to scale", 24, GREY).move_to([-3.0, 2.55, 0])
        cav = T("no simple blood-gas rule fully explains it", 28, YELLOW).move_to([0, -2.1, 0])
        self.at("breath hold ends")
        self.play(Create(tl), FadeIn(tla), FadeIn(time_l), run_time=0.6)
        self.at("at the apnea")
        self.play(FadeIn(bp, shift=DOWN * 0.15), Create(bpl), FadeIn(bpn), run_time=0.8)
        self.at("signal usually")
        self.play(FadeIn(m1, shift=DOWN * 0.15), Create(d1), FadeIn(usual), run_time=0.8)
        self.at("no simple")
        self.play(FadeIn(cav, shift=UP * 0.1), run_time=0.8)
        old = VGroup(tl, tla, time_l, m1, d1, usual, bp, bpl, bpn, cav)

        # the two series
        who = T("18 volunteers, little or no freediving experience\nrepeated maximal breath holds, face in cold water, mean values",
                22, GREY, line_spacing=0.85).move_to([0, 3.1, 0])
        hdr1 = T("starting end-tidal " + PCO2 + "\n(13 of 18 volunteers)", 22, TEAL, line_spacing=0.85).move_to([-4.0, 2.15, 0])
        hdr2 = T("breath hold", 22, YELLOW).move_to([0.05, 2.1, 0])
        hdr3 = T("peripheral\nsaturation nadir", 22, ORANGE, line_spacing=0.85).move_to([4.9, 2.15, 0])
        lab1 = T("series without hyperventilation", 24, TEXT).move_to([-5.7, 1.45, 0], aligned_edge=LEFT)
        lab2 = T("series after 15 s of hyperventilation", 24, GREEN).move_to([-5.7, -0.35, 0], aligned_edge=LEFT)
        y1, y2 = 0.8, -1.0
        self.at("volunteers with")
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(who), FadeIn(lab1), FadeIn(lab2), run_time=0.7)

        def pc(v, y):
            return M(v, 34, TEAL).move_to([-4.0, y, 0])

        def nd(v, y):
            return M(v, 34, ORANGE).move_to([4.9, y, 0])

        def bar(sec, y):
            w = sec * 0.04
            return Rectangle(width=w, height=0.7, stroke_width=0, fill_color=YELLOW, fill_opacity=0.75).move_to([-2.4 + w / 2, y, 0])

        self.at("of hyperventilation")
        self.play(Indicate(lab2, color=GREEN, scale_factor=1.04), run_time=0.7)
        self.at("starting end tidal")
        p1, p2 = pc("29.0 mmHg", y1), pc("29.0 mmHg", y2)
        self.play(FadeIn(hdr1), FadeIn(p1), FadeIn(p2), run_time=0.7)
        self.at("It fell")
        p2b = pc("17.4 mmHg", y2)
        dn = arr([-4.0, y2 - 0.45, 0], [-4.0, y2 - 0.95, 0], TEAL, 5, 0.18)
        self.play(Transform(p2, p2b), GrowArrow(dn), run_time=0.9)

        self.at("mean hold")
        b1, b2 = bar(111, y1), bar(133, y2)
        bt1 = M("111 s", 28, BG, weight=BOLD).move_to(b1.get_right() + LEFT * 0.7)
        bt2 = M("133 s", 28, BG, weight=BOLD).move_to(b2.get_right() + LEFT * 0.7)
        b1s = b1.copy().stretch_to_fit_width(0.05).move_to(b1.get_left(), aligned_edge=LEFT)
        b2s = b2.copy().stretch_to_fit_width(0.05).move_to(b2.get_left(), aligned_edge=LEFT)
        self.add(b1s, b2s)
        self.play(FadeIn(hdr2), Transform(b1s, b1), FadeIn(bt1), run_time=1.0)
        self.play(Transform(b2s, b2), FadeIn(bt2), run_time=1.1)

        self.at("saturation nadir")
        n1, n2 = nd("93.6 %", y1), nd("93.6 %", y2)
        self.play(FadeIn(hdr3), FadeIn(n1), FadeIn(n2), run_time=0.7)
        n2b = nd("90.6 %", y2)
        dn2 = arr([4.9, y2 - 0.45, 0], [4.9, y2 - 0.95, 0], ORANGE, 5, 0.18)
        self.wait(0.7)
        self.play(Transform(n2, n2b), GrowArrow(dn2), run_time=0.9)

        # the reading
        self.at("lowers the carbon dioxide signal")
        r1 = bchip("carbon dioxide signal: lowered", TEAL, 26).move_to([-3.0, -2.85, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.7)
        self.at("adds almost no oxygen")
        r2 = bchip("oxygen added: almost none", ORANGE, 26).move_to([3.2, -2.85, 0])
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.7)

        self.at("In an adult")
        keep = VGroup(who, hdr1, hdr2, hdr3, lab1, lab2, p1, p2, b1s, b2s, bt1, bt2, n1, n2, dn, dn2, r1, r2)
        rule = Text("In an adult at rest, breathing is a\ncarbon dioxide controller.", font=TITLE_FONT, font_size=46,
                    line_spacing=0.9, color=TEXT, t2c={"carbon dioxide controller": TEAL}).move_to([0, 0, 0])
        self.play(FadeOut(keep), run_time=0.5)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "In an adult at rest, breathing is a carbon dioxide controller."
