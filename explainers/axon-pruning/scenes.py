"""Axon pruning: one neuron, two ways to lose axons (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the neuron (cell body and axon)
  YELLOW = NGF (the dots)
  VIOLET = caspases
  ORANGE = Apaf-1 and the apoptosome it builds
  RED    = degeneration, death, and a crossed-out item (not needed / lost)
  GREEN  = survival (cell bodies live, neurons resist death)
  GREY   = chamber, labels, structure
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

VIOLET = "#A98BE0"
ORANGE = "#F29E4C"

AY = [1.2, 0.0, -1.2]       # the three axon rows in the chamber
BX, BR = -4.6, 0.42          # cell body column and radius
CH = 2.1                     # chamber half height
GX0, GX1 = -0.9, 0.9         # barrier with grooves
AX_END = 5.6
NSEG = 8
BOT_Y = -3.1                # outcome chips
CASE_Y = -2.5               # case label under the chamber

DOTS_L = [(-5.8, 1.8), (-3.3, 1.8), (-2.0, 0.6), (-5.6, -0.6), (-3.2, -0.6), (-1.6, 1.8),
          (-5.5, -1.8), (-3.6, -1.8), (-2.2, -1.8), (-1.5, -0.6)]
DOTS_R = [(1.6, 1.8), (3.0, 0.6), (4.3, 1.8), (5.5, 0.6), (2.0, -0.6), (3.6, -0.6), (5.2, -0.6),
          (1.8, -1.8), (3.5, -1.8), (5.2, -1.8)]


def P(x, y):
    return np.array([x, y, 0.0])


def compartment(x0, x1):
    return RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=2 * CH, stroke_color=GREY,
                            stroke_width=3, fill_opacity=0).move_to(P((x0 + x1) / 2, 0))


def barrier():
    ys = [CH] + [v for y in AY for v in (y + 0.1, y - 0.1)] + [-CH]
    parts = VGroup()
    for i in range(0, len(ys), 2):
        top, bot = ys[i], ys[i + 1]
        parts.add(Rectangle(width=GX1 - GX0, height=top - bot, stroke_width=0, fill_color=GREY,
                            fill_opacity=0.35).move_to(P(0, (top + bot) / 2)))
    return parts


def dots(pts):
    return VGroup(*[Dot(P(*p), radius=0.1, color=YELLOW) for p in pts])


class Chamber:
    """All parts of the two-compartment chamber, in their starting (healthy, NGF on both sides) state."""

    def __init__(self, with_dots=True):
        self.cl = compartment(-6.2, GX0)
        self.cr = compartment(GX1, 6.2)
        self.bar = barrier()
        self.lab_l = T("cell bodies", 26, GREY).move_to(P(-3.55, CH + 0.42))
        self.lab_r = T("axons", 26, GREY).move_to(P(3.55, CH + 0.42))
        self.bodies = VGroup(*[Circle(radius=BR, stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                                      fill_opacity=0.35).move_to(P(BX, y)) for y in AY])
        self.ax_in = VGroup(*[Line(P(BX + BR, y), P(GX1, y), color=BLUE, stroke_width=6) for y in AY])
        xs = np.linspace(GX1, AX_END, NSEG + 1)
        self.ax_out = [[Line(P(xs[i], y), P(xs[i + 1], y), color=BLUE, stroke_width=6) for i in range(NSEG)]
                       for y in AY]
        self.tips = VGroup(*[Dot(P(AX_END, y), radius=0.11, color=BLUE) for y in AY])
        self.dl = dots(DOTS_L) if with_dots else VGroup()
        self.dr = dots(DOTS_R) if with_dots else VGroup()
        self.frame = VGroup(self.cl, self.cr, self.bar, self.lab_l, self.lab_r)
        self.axons_out = VGroup(*[s for row in self.ax_out for s in row], self.tips)

    def all(self):
        return VGroup(self.frame, self.bodies, self.ax_in, self.axons_out, self.dl, self.dr)


def legend():
    d = Dot(P(-0.5, CH + 0.42), radius=0.1, color=YELLOW)
    t = T("NGF", 26, YELLOW).move_to(P(0.1, CH + 0.42))
    return VGroup(d, t)


def case_label(text, color=GREY):
    return T(text, 26, color).move_to(P(0, CASE_Y))


def out_chip(text, color, x):
    return chip(text, color, size=26, pad=0.16).move_to(P(x, BOT_Y))


def drain(dots_group, rt=1.0):
    """The NGF dots drift upward and vanish."""
    return LaggedStart(*[d.animate.shift(UP * 0.35).set_opacity(0) for d in dots_group], lag_ratio=0.12,
                       run_time=rt)


def degenerate(scene, rows, extra=(), rt=1.4):
    """Break axon segments apart, turn them red, and fade them."""
    rng = random.Random(4)
    segs = [s for row in rows for s in row]
    scene.play(*[s.animate.set_color(RED).shift(P(rng.uniform(-0.08, 0.08), rng.uniform(-0.28, 0.28)))
                 .scale(0.7) for s in segs], *[Indicate(e, color=RED) for e in extra], run_time=rt * 0.6)
    scene.play(*[FadeOut(s) for s in segs], *[FadeOut(e) for e in extra], run_time=rt * 0.45)


def cross(mob, color=RED, w=5):
    l, r, t, b = mob.get_left(), mob.get_right(), mob.get_top(), mob.get_bottom()
    pad = 0.05
    return VGroup(Line(P(l[0] - pad, t[1] + pad), P(r[0] + pad, b[1] - pad), color=color, stroke_width=w),
                  Line(P(l[0] - pad, b[1] - pad), P(r[0] + pad, t[1] + pad), color=color, stroke_width=w))


def link(a, b, color=GREY):
    return Arrow(a.get_right() + RIGHT * 0.08, b.get_left() - RIGHT * 0.08, buff=0, color=color, stroke_width=5,
                 tip_length=0.22, max_tip_length_to_length_ratio=0.5)


def die(body_group):
    return [body_group.animate.set_stroke(RED).set_fill(RED, 0.5).scale(0.7)]


# chain used in scene 4 and 6
CX = [-4.6, -1.5, 1.6, 4.7]


def chain_chips(y, size=30):
    a = chip("Apaf-1", ORANGE, size=size).move_to(P(CX[0], y))
    b = chip("apoptosome", ORANGE, size=size).move_to(P(CX[1], y))
    c = chip("caspase-9", VIOLET, size=size).move_to(P(CX[2], y))
    d = chip("neurons die", RED, size=size).move_to(P(CX[3], y))
    return a, b, c, d


class S00Title(TitleCard):
    LESSON = "Pruning Without Dying"
    TITLE = "One Neuron, Two Ways to Lose Axons"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        body = Circle(radius=0.95, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.35)
        body.move_to(P(-4.3, 0.3))
        trunk = Line(P(-3.35, 0.3), P(0.4, 0.3), color=BLUE, stroke_width=9)
        a_end, b_end, c_end = P(4.6, 2.2), P(5.0, 0.3), P(4.6, -1.6)
        brA = Line(P(0.4, 0.3), a_end, color=BLUE, stroke_width=7)
        brB = Line(P(0.4, 0.3), b_end, color=BLUE, stroke_width=7)
        cxs = np.linspace(0, 1, 7)
        brC = [Line(P(0.4, 0.3) + (c_end - P(0.4, 0.3)) * cxs[i], P(0.4, 0.3) + (c_end - P(0.4, 0.3)) * cxs[i + 1],
                    color=BLUE, stroke_width=7) for i in range(6)]
        brCg = VGroup(*brC)
        neuron = VGroup(body, trunk, brA, brB, brCg)
        self.at("How can a neuron")
        self.play(FadeIn(body, scale=0.8), Create(trunk), Create(brA), Create(brB), Create(brCg), run_time=0.9)
        self.at("cut off a branch")
        self.play(Indicate(brCg, color=RED, scale_factor=1.05), run_time=0.8)
        self.at("could kill the whole")
        self.play(Indicate(body, color=RED, scale_factor=1.12), run_time=0.8)
        self.at("Pruning means")
        keep = T("pruning: a branch goes, the neuron survives", 26, GREY).move_to(P(0, -3.0))
        self.play(FadeIn(keep, shift=UP * 0.1), run_time=0.5)
        self.at("The enzymes are")
        cas = chip("caspases", VIOLET, size=34).move_to(P(-4.3, 2.5))
        self.play(FadeIn(cas, shift=DOWN * 0.1), run_time=0.5)
        self.at("proteases that dismantle")
        self.play(Indicate(cas, color=VIOLET, scale_factor=1.15), run_time=0.8)
        self.at("Yet a neuron")
        self.play(FadeOut(keep), run_time=0.3)
        seeds = VGroup(*[Dot(brC[i].get_center(), radius=0.12, color=VIOLET) for i in range(6)])
        self.play(FadeIn(seeds, scale=0.4), run_time=0.5)
        self.at("one axon and live")
        rng = random.Random(2)
        self.play(*[s.animate.set_color(RED).shift(P(rng.uniform(-0.08, 0.08), rng.uniform(-0.2, 0.2))).scale(0.7)
                    for s in brC], run_time=0.6)
        self.play(*[FadeOut(s) for s in brC], FadeOut(seeds), run_time=0.5)
        lives = chip("the neuron lives", GREEN, size=28).move_to(P(-4.3, -1.5))
        self.play(FadeIn(lives, shift=UP * 0.1), run_time=0.5)
        self.at("Mouse sympathetic neurons")
        lab = T("mouse sympathetic neurons", 28, GREY).move_to(P(2.5, -2.4))
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Chamber(SpokenScene):
    def construct(self):
        C = Chamber()
        self.at("built a chamber")
        self.play(FadeIn(C.cl), FadeIn(C.cr), FadeIn(C.bar), run_time=0.9)
        self.at("two compartments")
        self.play(Indicate(C.cl, color=TEXT, scale_factor=1.02), Indicate(C.cr, color=TEXT, scale_factor=1.02),
                  run_time=0.8)
        self.at("The cell bodies")
        self.play(FadeIn(C.lab_l, shift=DOWN * 0.1), FadeIn(C.bodies, scale=0.6), run_time=0.7)
        self.at("Their axons grew")
        grooves = T("narrow grooves", 26, GREY).move_to(P(0, CH + 0.42))
        self.play(*[Create(l) for l in C.ax_in], FadeIn(grooves, shift=DOWN * 0.1), FadeIn(C.lab_r), run_time=1.0)
        self.play(*[Create(s) for row in C.ax_out for s in row], FadeIn(C.tips), run_time=1.1)
        self.at("Many sympathetic")
        self.play(Indicate(C.axons_out, color=BLUE, scale_factor=1.03), run_time=0.8)
        self.at("Both sides held")
        lg = legend()
        self.play(FadeOut(grooves), run_time=0.2)
        self.play(FadeIn(lg, shift=DOWN * 0.1), LaggedStart(*[FadeIn(d, scale=0.3) for d in C.dl], lag_ratio=0.08),
                  LaggedStart(*[FadeIn(d, scale=0.3) for d in C.dr], lag_ratio=0.08), run_time=1.5)
        self.at("a growth factor")
        self.play(Indicate(lg, color=YELLOW, scale_factor=1.2), run_time=0.7)
        self.at("This setup")
        self.play(Circumscribe(C.cr, color=TEXT, run_time=1.0))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Local(SpokenScene):
    def construct(self):
        C = Chamber()
        lg = legend()
        self.add(C.all(), lg)
        self.at("from the axons alone")
        cl = case_label("NGF removed from the axons only")
        self.play(drain(C.dr, 1.1), FadeIn(cl, shift=UP * 0.1))
        self.at("The axons degenerate")
        degenerate(self, C.ax_out, extra=[C.tips], rt=1.5)
        chip_a = out_chip("axons degenerate", RED, 3.4)
        self.play(FadeIn(chip_a, shift=UP * 0.1), run_time=0.4)
        self.at("bodies live")
        chip_b = out_chip("cell bodies live", GREEN, -3.4)
        self.play(FadeIn(chip_b, shift=UP * 0.1), Indicate(C.bodies, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.at("still have")
        self.play(Indicate(C.dl, color=YELLOW, scale_factor=1.0), run_time=0.9)
        self.at("the local route")
        self.play(Indicate(chip_a, color=RED, scale_factor=1.08), run_time=0.7)
        self.at("needs three")
        names = ["caspase-9", "caspase-3", "caspase-6"]
        cs = VGroup(*[chip(n, VIOLET, size=28).move_to(P(3.55, y)) for n, y in zip(names, [1.5, 0.5, -0.5])])
        self.play(FadeIn(cs[0], scale=0.8), run_time=0.4)
        self.at("caspase 3")
        self.play(FadeIn(cs[1], scale=0.8), run_time=0.4)
        self.at("and caspase 6")
        self.play(FadeIn(cs[2], scale=0.8), run_time=0.4)
        self.at("It does not need")
        ap = chip("Apaf-1", ORANGE, size=28).move_to(P(3.55, -1.5))
        self.play(FadeIn(ap, scale=0.8), run_time=0.4)
        self.play(Create(cross(ap)), run_time=0.4)
        self.at("Keep that name")
        self.play(Indicate(ap, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Global(SpokenScene):
    def construct(self):
        C = Chamber()
        lg = legend()
        self.add(C.all(), lg)
        self.at("start again")
        self.wait(0.3)
        self.at("the whole dish")
        cl = case_label("NGF removed from the whole dish")
        self.play(drain(C.dl, 1.0), drain(C.dr, 1.0), FadeIn(cl, shift=UP * 0.1), FadeOut(lg))
        self.at("the neurons die")
        rows = C.ax_out
        chip_d = chip("neurons die", RED, size=26, pad=0.16).move_to(P(0, BOT_Y))
        self.play(*die(C.bodies), C.ax_in.animate.set_color(RED), FadeIn(chip_d, shift=UP * 0.1), run_time=0.6)
        degenerate(self, rows, extra=[C.tips], rt=0.9)
        self.at("This is the")
        self.play(Indicate(chip_d, color=RED, scale_factor=1.1), run_time=0.7)
        self.at("Their death needs")
        self.play(FadeOut(C.all()), FadeOut(cl), FadeOut(chip_d), run_time=0.6)
        a, b, c, dd = chain_chips(0.5, 32)
        self.play(FadeIn(dd, shift=UP * 0.1), run_time=0.4)
        self.at("apaf")
        self.play(FadeIn(a, shift=UP * 0.1), run_time=0.5)
        self.at("builds the apoptosome")
        l1 = link(a, b, ORANGE)
        self.play(GrowArrow(l1), FadeIn(b, shift=RIGHT * 0.1), run_time=0.7)
        self.at("usual activator")
        l2 = link(b, c, VIOLET)
        self.play(GrowArrow(l2), FadeIn(c, shift=RIGHT * 0.1), run_time=0.7)
        self.at("in apoptosis")
        l3 = link(c, dd, RED)
        self.play(GrowArrow(l3), run_time=0.5)
        W = VGroup(a, b, c, dd, l1, l2, l3)
        self.at("When")
        self.play(W.animate.shift(UP * 1.7), run_time=0.5)
        Cm = Chamber(with_dots=False)
        for m in Cm.bodies:
            m.set_stroke(RED).set_fill(RED, 0.5)
        for m in Cm.ax_in:
            m.set_color(RED)
        for row in Cm.ax_out:
            for m in row:
                m.set_color(RED)
        Cm.tips.set_color(RED)
        Cm.lab_l.set_opacity(0)
        Cm.lab_r.set_opacity(0)
        panel = Cm.all().scale(0.5).move_to(P(-2.4, -1.0))
        self.play(FadeIn(panel), run_time=0.5)
        self.at("loss of caspase 6")
        c6 = chip("caspase-6", VIOLET, size=32).move_to(P(4.3, -0.4))
        self.play(FadeIn(c6, shift=UP * 0.1), run_time=0.4)
        self.play(Create(cross(c6)), run_time=0.4)
        self.at("no longer protects")
        note = T("axons not protected", 28, RED).move_to(P(4.3, -1.6))
        self.play(FadeIn(note, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Test(SpokenScene):
    def construct(self):
        C = Chamber()
        lg = legend()
        self.add(C.all(), lg)
        self.at("test the idea")
        self.wait(0.3)
        self.at("away from the neurons")
        no = T("Apaf-1 removed from the neurons", 30, ORANGE).move_to(P(0, 3.15))
        self.play(FadeIn(no, shift=DOWN * 0.1), run_time=0.6)
        self.at("from the axons alone")
        cl = case_label("NGF removed from the axons only")
        self.play(drain(C.dr, 1.0), FadeIn(cl, shift=UP * 0.1))
        self.at("still degenerate")
        degenerate(self, C.ax_out, extra=[C.tips], rt=1.3)
        chip_a = out_chip("axons degenerate", RED, 3.4)
        self.play(FadeIn(chip_a, shift=UP * 0.1), run_time=0.4)
        self.at("cell bodies live")
        chip_b = out_chip("cell bodies live", GREEN, -3.4)
        self.play(FadeIn(chip_b, shift=UP * 0.1), run_time=0.5)
        # reset to a neutral, healthy chamber with no result and no case label
        self.at("Now remove")
        C2 = Chamber()
        self.play(FadeOut(VGroup(C.frame, C.bodies, C.ax_in, C.dl, C.dr)), FadeOut(cl), FadeOut(chip_a),
                  FadeOut(chip_b), FadeIn(C2.all()), run_time=0.7)
        self.at("the whole dish")
        cl2 = case_label("NGF removed from the whole dish")
        self.play(drain(C2.dl, 1.0), drain(C2.dr, 1.0), FadeIn(cl2, shift=UP * 0.1), FadeOut(lg))
        self.at("resist death")
        chip_c = out_chip("neurons resist death", GREEN, 0)
        self.play(FadeIn(chip_c, shift=UP * 0.1), Indicate(C2.bodies, color=GREEN, scale_factor=1.15), run_time=0.9)
        self.at("route is blocked")
        self.play(Indicate(no, color=ORANGE, scale_factor=1.1), run_time=0.8)
        self.at("route needs")
        self.play(FadeOut(C2.all()), FadeOut(cl2), FadeOut(chip_c), FadeOut(no), run_time=0.6)
        a = chip("Apaf-1", ORANGE, size=36).move_to(P(-2.4, 0))
        c = chip("caspase-9", VIOLET, size=36).move_to(P(2.4, 0))
        self.play(FadeIn(a, shift=UP * 0.1), run_time=0.4)
        self.at("to activate")
        self.play(GrowArrow(link(a, c, ORANGE)), FadeIn(c, shift=RIGHT * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        yt, yb = 1.3, -1.7
        lab_t = T("local route", 28, GREY)
        lab_t.move_to(P(-6.0 + lab_t.width / 2, yt + 1.0))
        lab_b = T("whole-cell route", 28, GREY)
        lab_b.move_to(P(-6.0 + lab_b.width / 2, yb + 1.0))
        # bottom row: Apaf-1 -> apoptosome -> caspase-9 -> neurons die
        a, b, c, d = chain_chips(yb, 28)
        l1, l2, l3 = link(a, b, ORANGE), link(b, c, VIOLET), link(c, d, RED)
        # top row: crossed Apaf-1 ... caspase-9, -3, -6 -> axons degenerate
        ta = chip("Apaf-1", ORANGE, size=28).move_to(P(CX[0], yt))
        tc = chip("caspase-9, -3, -6", VIOLET, size=28).move_to(P(-0.4, yt))
        td = chip("axons degenerate", RED, size=28).move_to(P(4.4, yt))
        tl2, tl3 = link(tc, td, RED), None
        self.at("same caspases")
        self.play(FadeIn(tc, shift=UP * 0.1), FadeIn(c, shift=UP * 0.1), run_time=0.7)
        self.at("two routes")
        self.play(FadeIn(lab_t), FadeIn(lab_b), run_time=0.5)
        self.at("one local")
        self.play(GrowArrow(tl2), FadeIn(td, shift=RIGHT * 0.1), run_time=0.7)
        self.at("one global")
        self.play(FadeIn(a), FadeIn(b), FadeIn(d), GrowArrow(l1), GrowArrow(l2), GrowArrow(l3), run_time=1.0)
        self.at("The local route uses")
        self.play(Indicate(tc, color=VIOLET, scale_factor=1.1), run_time=0.8)
        self.at("but not")
        self.play(FadeIn(ta, shift=RIGHT * 0.1), run_time=0.4)
        self.play(Create(cross(ta)), run_time=0.4)
        self.at("route needs the apoptosome")
        self.play(Indicate(b, color=ORANGE, scale_factor=1.15), run_time=0.8)
        self.at("share enzymes")
        self.play(Indicate(VGroup(tc, c), color=VIOLET, scale_factor=1.12), run_time=0.9)
        self.at("wired differently")
        self.play(Indicate(VGroup(tl2, l1, l2, l3), color=TEXT, scale_factor=1.05), run_time=0.9)
        self.at("lose one branch")
        self.play(Indicate(td, color=RED, scale_factor=1.12), run_time=0.7)
        self.at("Remember")
        self.play(Indicate(VGroup(a, b), color=ORANGE, scale_factor=1.15), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Only the whole-cell route needs Apaf-1."
