"""Homeostasis in action: steady inside, changing outside  (Biochemistrypedia high school Biology film)

COLOR MAP (one color per concept, whole film)
  ORANGE = the change / the variable that is pushed (warming, dry air, the drifting line)
  GREEN  = the stable range (band, "inside" box)
  BLUE   = sensor
  PURPLE = control center
  YELLOW = effector (sweat glands, guard cells)
  TEAL   = the response that pushes back
  GREY   = outlines, axes, leaf surface, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CY = -0.3          # centre line of the graph


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


# ---------------------------------------------------------------- graph helpers (a sketch, not data)
def GX(t):
    return -5.0 + t * 0.92


def base(t):
    return 0.2 * np.sin(1.4 * t) + 0.12 * np.sin(3.3 * t + 1)


def full(t):
    u = max(t - 4.0, 0.0)
    return base(t) + 1.9 * (u / 1.2) * np.exp(1 - u / 1.2)


def curve(f, a, b, color):
    return ParametricFunction(lambda t: [GX(t), CY + f(t), 0], t_range=[a, b, 0.02], color=color, stroke_width=6)


def graph_frame(ylabel):
    ax_y = Line([-5.2, CY - 1.7, 0], [-5.2, 2.5, 0], color=GREY, stroke_width=3)
    ax_x = Line([-5.2, CY - 1.7, 0], [4.5, CY - 1.7, 0], color=GREY, stroke_width=3)
    yl = T(ylabel, 24, GREY).move_to([-5.2, 2.85, 0]).align_to([-5.2, 0, 0], LEFT)
    xl = T("time", 24, GREY).next_to(ax_x, DOWN, buff=0.15).align_to(ax_x, RIGHT)
    note = T("a sketch, not measured data", 22, GREY).move_to([0, -3.3, 0])
    return VGroup(ax_y, ax_x, yl, xl), note


def band():
    r = Rectangle(width=9.7, height=1.2, stroke_width=0, fill_color=GREEN, fill_opacity=0.22).move_to([-0.35, CY, 0])
    lab = T("stable\nrange", 24, GREEN, line_spacing=0.8).move_to([5.45, CY, 0])
    return r, lab


# ---------------------------------------------------------------- leaf helpers
def gcell(side, narrow, s, cy):
    w = 0.5 * s
    x = 0.4 * s if narrow else 0.9 * s
    return RoundedRectangle(corner_radius=0.12 * s, width=w, height=1.0 * s, stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.12 if narrow else 0.3).move_to([side * x, cy, 0])


def epidermis(s, cy):
    bars = VGroup()
    for side in (-1, 1):
        r = Rectangle(width=2.9 * s, height=0.6 * s, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        r.move_to([side * (1.35 * s + 1.45 * s), cy, 0])
        bars.add(r)
    return bars


class S00Title(TitleCard):
    LESSON = "Homeostasis in Action"
    TITLE = "Steady Inside, Changing Outside"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        lx, rx = -3.4, 3.4
        # left: heart
        ltitle = T("running up stairs", 30, TEXT).move_to([lx, 2.4, 0])
        heart = chip("heart", ORANGE, size=36).move_to([lx, 0.9, 0])
        axis = Line([lx - 2.4, -1.2, 0], [lx + 2.4, -1.2, 0], color=GREY, stroke_width=3)
        fast = [lx - 2.3 + 0.28 * i for i in range(8)]
        slow = [fast[-1] + 0.5 + 0.62 * i for i in range(4)]
        ticks_f = VGroup(*[Line([x, -1.2, 0], [x, -0.6, 0], color=ORANGE, stroke_width=5) for x in fast])
        ticks_s = VGroup(*[Line([x, -1.2, 0], [x, -0.6, 0], color=ORANGE, stroke_width=5) for x in slow])
        l_fast = T("faster", 28, ORANGE).move_to([lx - 1.2, -1.85, 0])
        l_slow = T("then slower", 28, ORANGE).move_to([lx + 1.3, -1.85, 0])
        self.at("Run up a flight of stairs")
        self.play(FadeIn(ltitle, shift=UP * 0.1), FadeIn(heart, scale=0.9), Create(axis), run_time=0.8)
        self.at("pounds faster")
        self.play(LaggedStart(*[Create(t) for t in ticks_f], lag_ratio=0.2), FadeIn(l_fast),
                  Succession(Indicate(heart, scale_factor=1.12), Indicate(heart, scale_factor=1.12)),
                  run_time=1.3)
        self.at("slows again")
        self.play(LaggedStart(*[Create(t) for t in ticks_s], lag_ratio=0.3), FadeIn(l_slow), run_time=1.2)
        # right: leaf pore
        rtitle = T("hot, dry afternoon", 30, TEXT).move_to([rx, 2.4, 0])
        s = 0.62
        bars = epidermis(s, 0.9).shift(RIGHT * rx)
        gl, gr = gcell(-1, False, s, 0.9).shift(RIGHT * rx), gcell(1, False, s, 0.9).shift(RIGHT * rx)
        pl = T("pores", 28, TEXT).move_to([rx, -0.2, 0])
        self.at("On a hot, dry afternoon")
        self.play(FadeIn(rtitle, shift=UP * 0.1), FadeIn(bars), FadeIn(gl), FadeIn(gr), FadeIn(pl), run_time=0.9)
        self.at("narrow")
        self.play(Transform(gl, gcell(-1, True, s, 0.9).shift(RIGHT * rx)), Transform(gr, gcell(1, True, s, 0.9).shift(RIGHT * rx)),
                  run_time=0.8)
        sch1 = T("schematic, not to scale", 22, GREY).move_to([rx, -0.9, 0])
        self.add(sch1)
        l_nar = T("pores narrow", 28, ORANGE).move_to([rx, -0.2, 0])
        self.play(ReplacementTransform(pl, l_nar), run_time=0.4)
        self.wait(0.1)
        # fold into the question
        self.at("The world outside keeps changing")
        allg = VGroup(sch1, ltitle, heart, axis, ticks_f, ticks_s, l_fast, l_slow, rtitle, bars, gl, gr, l_nar)
        self.play(FadeOut(allg), run_time=0.6)
        box = RoundedRectangle(corner_radius=0.2, width=4.6, height=2.8, stroke_color=GREEN, stroke_width=5,
                               fill_color=GREEN, fill_opacity=0.12).move_to([0, -0.1, 0])
        inside = T("inside", 34, GREEN, weight=BOLD).move_to(box.get_top() + DOWN * 0.5)
        ins = []
        for p, q in [([-6.0, -0.1, 0], [-2.6, -0.1, 0]), ([6.0, -0.1, 0], [2.6, -0.1, 0]),
                     ([0, 3.4, 0], [0, 1.5, 0]), ([0, -3.4, 0], [0, -1.7, 0])]:
            ins.append(arr(p, q, ORANGE, w=7))
        outside = T("outside keeps changing", 28, ORANGE).move_to([0, 3.5, 0])
        ins[2] = arr([0, 3.1, 0], [0, 1.45, 0], ORANGE, w=7)
        outside.move_to([0, 3.45, 0])
        self.play(FadeIn(box), FadeIn(inside), run_time=0.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in ins], lag_ratio=0.2), FadeIn(outside), run_time=1.2)
        self.at("how do living things")
        q = T("steady?", 48, TEXT, weight=BOLD).move_to([0, -0.5, 0])
        self.play(FadeIn(q, scale=0.8), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Range(SpokenScene):
    def construct(self):
        axes, note = graph_frame("body temperature")
        chip_h = chip("homeostasis", GREEN, size=34).move_to([0, 3.2, 0])
        bnd, blab = band()
        self.at("Biologists call this homeostasis")
        self.play(FadeIn(axes), FadeIn(note), FadeIn(chip_h, scale=0.9), run_time=0.8)
        self.at("Homeostasis means keeping")
        self.play(FadeIn(bnd), run_time=0.8)
        self.at("within a stable range")
        self.play(FadeIn(blab), Indicate(bnd, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.at("The word range matters")
        self.play(Indicate(bnd, color=GREEN, scale_factor=1.06), Indicate(blab, color=GREEN), run_time=1.0)
        self.at("usually near")
        l37 = T("usually near 37 °C", 28, TEXT).move_to([-2.2, CY + 1.45, 0])
        a37 = arr([-2.2, CY + 1.1, 0], [-2.2, CY + 0.15, 0], TEXT, w=4)
        self.play(FadeIn(l37, shift=UP * 0.1), GrowArrow(a37), run_time=0.5)
        self.at("shifts a little")
        c = curve(base, 0, 10, ORANGE)
        self.play(Create(c), run_time=2.0, rate_func=linear)
        self.at("fixed at one number")
        flat = DashedLine([GX(0), CY, 0], [GX(10), CY, 0], color=RED, stroke_width=5)
        no = T("not one fixed number", 28, RED).move_to([2.0, CY + 1.45, 0])
        self.play(Create(flat), FadeIn(no), c.animate.set_opacity(0.35), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Negative(SpokenScene):
    def construct(self):
        axes, note = graph_frame("a variable")
        bnd, blab = band()
        c0 = curve(base, 0, 4, ORANGE)
        up = curve(full, 4, 5.2, ORANGE)
        down = curve(full, 5.2, 10, TEAL)
        self.add(axes, note, bnd, blab, c0)
        self.at("Most homeostasis works")
        chip_n = chip("negative feedback", TEAL, size=34).move_to([0, 3.2, 0])
        self.play(FadeIn(chip_n, scale=0.9), run_time=0.7)
        self.at("In negative feedback")
        a_up = arr([GX(3.7), CY + 0.8, 0], [GX(3.7), CY + 2.0, 0], ORANGE, w=7)
        l_ch = T("change", 28, ORANGE).next_to(a_up, LEFT, buff=0.15)
        self.play(Create(up), GrowArrow(a_up), FadeIn(l_ch), run_time=1.4)
        self.at("the response opposes")
        a_dn = arr([GX(7.3), CY + 2.1, 0], [GX(7.3), CY + 1.35, 0], TEAL, w=7)
        l_rs = T("response", 28, TEAL).next_to(a_dn, RIGHT, buff=0.15)
        self.play(Create(down), GrowArrow(a_dn), FadeIn(l_rs), run_time=2.0)
        self.at("Negative does not mean bad")
        t1 = T("negative does not mean bad", 30, TEXT).move_to([-0.4, -2.55, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.at("pushes the other way")
        t2 = T("negative = pushes the other way", 30, TEAL).move_to([-0.4, -2.55, 0])
        self.play(ReplacementTransform(t1, t2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
NODE_POS = [np.array(p) for p in ([0, 2.3, 0], [3.9, 0.57, 0], [2.9, -2.4, 0], [-2.9, -2.4, 0], [-3.9, 0.57, 0])]
NODE_COL = [ORANGE, BLUE, PURPLE, YELLOW, TEAL]
GENERIC = ["change", "sensor", "control center", "effector", "response"]


def node(i, text):
    return chip(text, NODE_COL[i], size=26, pad=0.2).move_to(NODE_POS[i])


def edge_pt(n, toward):
    c = n.get_center()
    d = toward - c
    w, h = n.width / 2 + 0.1, n.height / 2 + 0.1
    t = min(w / max(abs(d[0]), 1e-6), h / max(abs(d[1]), 1e-6))
    return c + d * t


def link(a, b, color=GREY):
    return arr(edge_pt(a, b.get_center()), edge_pt(b, a.get_center()), color, w=6)


class S04Parts(SpokenScene):
    def construct(self):
        nodes = [node(i, GENERIC[i]) for i in range(5)]
        links = [link(nodes[i], nodes[(i + 1) % 5]) for i in range(5)]
        mid = T("negative\nfeedback loop", 30, GREY, line_spacing=0.8).move_to([0, 0.0, 0])
        self.at("Every loop has the same parts")
        self.play(FadeIn(mid), run_time=0.6)
        self.at("a change pushes")
        self.play(FadeIn(nodes[0], scale=0.9), run_time=0.6)
        self.at("A sensor is")
        self.play(GrowArrow(links[0]), FadeIn(nodes[1], scale=0.9), run_time=0.7)
        self.at("The control center compares")
        self.play(GrowArrow(links[1]), FadeIn(nodes[2], scale=0.9), run_time=0.7)
        self.at("In your body")
        brain = T("usually the brain", 24, PURPLE).move_to([2.9, -3.15, 0])
        self.play(FadeIn(brain, shift=UP * 0.1), run_time=0.5)
        self.at("An effector is")
        self.play(GrowArrow(links[2]), FadeIn(nodes[3], scale=0.9), run_time=0.7)
        self.at("carries out the response")
        self.play(GrowArrow(links[3]), FadeIn(nodes[4], scale=0.9), run_time=0.7)
        self.play(GrowArrow(links[4]), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Hotday(SpokenScene):
    def construct(self):
        nodes = [node(i, GENERIC[i]) for i in range(5)]
        links = [link(nodes[i], nodes[(i + 1) % 5]) for i in range(5)]
        self.add(*nodes, *links)

        def relink(*idx):
            return [Transform(links[j], link(nodes[j], nodes[(j + 1) % 5])) for j in idx]
        # temperature bar in the centre
        y0, y1 = -0.85, 1.15
        outline = Rectangle(width=0.55, height=y1 - y0, stroke_color=GREY, stroke_width=3).move_to([0, (y0 + y1) / 2, 0])
        bnd = Rectangle(width=0.55, height=0.5, stroke_width=0, fill_color=GREEN, fill_opacity=0.35).move_to([0, 0.1, 0])
        val = ValueTracker(0.1)
        level = always_redraw(lambda: VGroup(
            Line([-0.45, val.get_value(), 0], [0.45, val.get_value(), 0], color=ORANGE, stroke_width=8),
            Triangle(color=ORANGE, fill_opacity=1, stroke_width=0).scale(0.14).rotate(-PI / 2).move_to([0.62, val.get_value(), 0])))
        lab = T("body temperature", 22, GREY).move_to([0, -1.3, 0])
        self.play(FadeIn(outline), FadeIn(bnd), FadeIn(lab), run_time=0.5)
        self.add(level)

        def swap(i, text, **kw):
            new = node(i, text)
            return ReplacementTransform(nodes[i], new), new

        self.at("Your body warms")
        a, n0 = swap(0, "body warms")
        nodes[0] = n0
        self.play(a, *relink(4, 0), val.animate.set_value(0.95), run_time=1.0)
        self.at("Temperature sensors in the skin")
        a, n1 = swap(1, "temperature sensors\nin skin and brain")
        nodes[1] = n1
        self.play(a, *relink(0, 1), run_time=0.9)
        self.play(Indicate(links[0], color=BLUE), run_time=0.5)
        self.at("The control center in the brain")
        a, n2 = swap(2, "control center\nin the brain")
        nodes[2] = n2
        self.play(a, *relink(1, 2), run_time=0.9)
        self.play(Indicate(links[1], color=PURPLE), run_time=0.5)
        self.at("Sweat glands release sweat")
        a, n3 = swap(3, "sweat glands\nrelease sweat")
        nodes[3] = n3
        self.play(a, *relink(2, 3), run_time=0.9)
        self.play(Indicate(links[2], color=YELLOW), run_time=0.5)
        self.at("The sweat evaporates")
        a, n4 = swap(4, "sweat evaporates,\nskin cools")
        nodes[4] = n4
        self.play(a, *relink(3, 4), val.animate.set_value(0.1), run_time=1.4)
        self.play(Indicate(links[3], color=TEAL), run_time=0.5)
        self.at("pushes the change back")
        self.play(Indicate(links[4], color=TEAL, scale_factor=1.3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        s, cy, cx = 1.3, -0.4, 0.0
        bars = epidermis(s, cy)
        gl, gr = gcell(-1, False, s, cy), gcell(1, False, s, cy)
        self.at("Plants respond")
        self.play(FadeIn(bars), run_time=0.6)
        sch = T("schematic, not to scale", 22, GREY).move_to([0, -3.3, 0])
        self.add(sch)
        self.at("tiny pores called stomata")
        l_sto = T("stomata", 30, TEXT).move_to([0, cy - 1.7, 0])
        pa = arr([0, cy - 1.3, 0], [0, cy - 0.15, 0], TEXT, w=4)
        self.play(FadeIn(l_sto, shift=UP * 0.1), GrowArrow(pa), run_time=0.7)
        self.at("between two guard cells")
        l_gc = T("guard cells", 30, YELLOW).move_to([-3.6, cy - 1.7, 0])
        l_gc2 = T("guard cells", 30, YELLOW).move_to([3.6, cy - 1.7, 0])
        g1 = arr([-3.0, cy - 1.35, 0], [-1.15, cy - 0.65, 0], YELLOW, w=4)
        g2 = arr([3.0, cy - 1.35, 0], [1.15, cy - 0.65, 0], YELLOW, w=4)
        self.play(FadeIn(gl), FadeIn(gr), FadeIn(l_gc), FadeIn(l_gc2), GrowArrow(g1), GrowArrow(g2), run_time=0.8)
        self.at("change shape")
        self.play(Transform(gl, gcell(-1, True, s, cy)), Transform(gr, gcell(1, True, s, cy)), run_time=0.8)
        self.play(Transform(gl, gcell(-1, False, s, cy)), Transform(gr, gcell(1, False, s, cy)), run_time=0.8)
        # dry air above, water vapor out of the pore
        dry = RoundedRectangle(corner_radius=0.15, width=8.4, height=0.95, stroke_color=ORANGE, stroke_width=4,
                               fill_color=ORANGE, fill_opacity=0.14).move_to([0, 3.0, 0])
        dry_l = T("dry air", 32, ORANGE, weight=BOLD).move_to(dry)
        vap = [arr([x, cy + 0.45, 0], [x * 1.0, 2.35, 0], GREY, w=5) for x in (-0.45, 0.0, 0.45)]
        vap_l = T("water vapor", 24, GREY).move_to([2.6, 1.3, 0])
        self.at("Dry air makes a leaf lose water faster")
        self.play(FadeIn(dry), FadeIn(dry_l), run_time=0.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in vap], lag_ratio=0.2), FadeIn(vap_l), run_time=0.9)
        self.at("guard cells can close the pores")
        self.play(Transform(gl, gcell(-1, True, s, cy)), Transform(gr, gcell(1, True, s, cy)),
                  FadeOut(vap[0]), FadeOut(vap[2]), run_time=1.0)
        self.at("slows water loss")
        slow = T("slower loss", 24, TEAL).move_to([2.6, 1.3, 0])
        self.play(ReplacementTransform(vap_l, slow), Indicate(vap[1], color=TEAL), run_time=0.7)
        self.at("So how do living things stay steady")
        leaf_all = VGroup(sch, bars, gl, gr, l_sto, pa, l_gc, l_gc2, g1, g2, dry, dry_l, vap[1], slow)
        self.play(FadeOut(leaf_all), run_time=0.6)
        c1 = chip("sense a change", BLUE, size=34)
        c2 = chip("respond", YELLOW, size=34)
        c3 = chip("pushes it back", TEAL, size=34)
        grp = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.0).move_to([0, 0.2, 0])
        a1, a2 = link(c1, c2), link(c2, c3)
        self.at("They sense a change")
        self.play(FadeIn(c1, scale=0.9), run_time=0.6)
        self.at("Then they respond")
        self.play(GrowArrow(a1), FadeIn(c2, scale=0.9), run_time=0.6)
        self.at("pushes it back")
        self.play(GrowArrow(a2), FadeIn(c3, scale=0.9), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Sense a change. Respond in a way that pushes it back."
