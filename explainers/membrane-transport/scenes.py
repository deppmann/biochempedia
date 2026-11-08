"""Membrane transport: voltage can reverse an ion's flow  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the ion (K+, Cl-) and its net flux
  BLUE   = channel protein (pillars in the membrane)
  GREY   = membrane, outlines, labels
  ORANGE = concentration (the concentration push, the mM labels)
  TEAL   = membrane voltage Vm (the voltage push, the Vm mark)
  GREEN  = equilibrium potential (E_K, E_X), balance, zero net flux
  PURPLE = the difference Vm - E (the driving force)
  PINK   = carrier (only in the rate comparison)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB5"

RX = 5.0   # x of the voltage ruler


def vy(v):
    """y on screen of a membrane voltage v (mV): 0 mV at the top of the ruler, -120 mV at the bottom."""
    return 2.9 + v * (5.8 / 120.0)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=6, tip=0.26):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def ion(label="K⁺", r=0.28, size=22, color=YELLOW):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.95)
    return VGroup(c, T(label, size, BG, weight=BOLD).move_to(c))


def wall(x0, x1, y, xs, s=1.0, t=0.4, plugs=True):
    """A membrane bar with a channel (two blue pillars) at each x in xs. Gap half-width 0.55*s."""
    g = 0.55 * s
    edges = [x0] + [v for x in xs for v in (x - g, x + g)] + [x1]
    segs = VGroup()
    for i in range(0, len(edges), 2):
        a, b = edges[i], edges[i + 1]
        segs.add(RoundedRectangle(corner_radius=0.08, width=b - a, height=t, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.35).move_to([(a + b) / 2, y, 0]))
    pillars = VGroup()
    for x in xs:
        for sd in (-1, 1):
            pillars.add(RoundedRectangle(corner_radius=0.07, width=0.2 * s, height=t + 0.35 * s, stroke_color=BLUE,
                                         stroke_width=3, fill_color=BLUE, fill_opacity=0.55).move_to([x + sd * 0.45 * s, y, 0]))
    plug = VGroup()
    if plugs:
        for x in xs:
            plug.add(Rectangle(width=2 * 0.35 * s, height=t, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to([x, y, 0]))
    out = VGroup(segs, pillars, plug)
    out.segs, out.pillars, out.plug = segs, pillars, plug
    return out


def ruler():
    line = Line([RX, 2.9, 0], [RX, -2.9, 0], color=GREY, stroke_width=4)
    ticks = VGroup(*[Line([RX - 0.12, vy(v), 0], [RX + 0.12, vy(v), 0], color=GREY, stroke_width=3)
                     for v in (0, -20, -40, -60, -80, -100, -120)])
    top = T("0 mV", 22, GREY).move_to([RX, 3.3, 0])
    bot = T("−120", 22, GREY).move_to([RX, -3.3, 0])
    return VGroup(line, ticks, top, bot)


def marker(v, color, name, side):
    ln = Line([RX - 0.3, vy(v), 0], [RX + 0.3, vy(v), 0], color=color, stroke_width=8)
    lab = T(name, 24, color, weight=BOLD)
    if side == "L":
        lab.next_to(ln, LEFT, buff=0.12)
    else:
        lab.next_to(ln, RIGHT, buff=0.12)
    return VGroup(ln, lab)


def mv(m, old, new):
    return m.animate.shift(UP * (vy(new) - vy(old)))


def place(m, x, y, edge=LEFT):
    return m.move_to([x, y, 0], aligned_edge=edge)


def gap_bar(a, b):
    return Line([RX, vy(a), 0], [RX, vy(b), 0], color=PURPLE, stroke_width=12)


class S00Title(TitleCard):
    LESSON = "Transport across membranes"
    TITLE = "Voltage can reverse an ion's flow"


# ---------------------------------------------------------------------------------------------
class S01Reversal(SpokenScene):
    def construct(self):
        xs = [-4.2, -1.2]
        w = wall(-6.3, 2.9, 0.0, xs)
        self.add(w)
        self.at("Which way does potassium flow")
        q = T("?", 72, YELLOW, weight=BOLD).move_to([-2.7, 1.0, 0])
        q2 = T("?", 72, YELLOW, weight=BOLD).move_to([-2.7, -1.0, 0])
        self.play(FadeIn(q, scale=0.6), FadeIn(q2, scale=0.6), run_time=0.5)
        self.play(Indicate(q, color=YELLOW), Indicate(q2, color=YELLOW), run_time=1.0)

        inside_pos = [(-5.5, -1.1), (-4.2, -1.2), (-2.7, -1.0), (-1.2, -1.2), (0.3, -1.0), (1.7, -1.3),
                      (-3.4, -2.1), (-0.2, -2.2), (-5.2, -2.0), (1.5, -2.2)]
        ins = [ion().move_to([x, y, 0]) for x, y in inside_pos]
        A, B = ins[1], ins[3]
        outs = [ion().move_to([x, y, 0]) for x, y in [(-3.2, 1.3), (-0.2, 1.5), (-5.4, 1.5), (1.6, 1.3)]]
        C, D = outs[0], outs[1]
        lab_in = place(T("inside   140 mM", 26, ORANGE), -6.3, -3.05)
        lab_out = place(T("outside   5 mM", 26, ORANGE), -6.3, 3.05)

        self.at("potassium inside")
        self.play(FadeOut(q), FadeOut(q2), LaggedStart(*[FadeIn(i, scale=0.7) for i in ins], lag_ratio=0.06),
                  FadeIn(lab_in), run_time=1.0)
        self.at("outside")
        self.play(LaggedStart(*[FadeIn(o, scale=0.7) for o in outs], lag_ratio=0.1), FadeIn(lab_out), run_time=0.7)

        rl = ruler()
        vm = marker(-70, TEAL, "Vm", "L")
        vm_read = place(M("Vm = −70 mV", 30, TEAL), 0.0, 3.05)
        self.at("hold it at minus")
        self.play(FadeIn(rl), FadeIn(vm), FadeIn(vm_read), run_time=0.8)

        self.at("Open the channels")
        self.play(FadeOut(w.plug), *[Indicate(p, color=BLUE, scale_factor=1.15) for p in w.pillars], run_time=0.8)

        net = T("net K⁺ flux: out", 24, YELLOW).move_to([1.5, -3.05, 0])
        self.at("potassium leaves")
        self.play(A.animate.move_to([-4.2, 0.0, 0]), B.animate.move_to([-1.2, 0.0, 0]), run_time=0.5)
        self.play(A.animate.move_to([-4.2, 1.5, 0]), B.animate.move_to([-1.2, 1.5, 0]), FadeIn(net), run_time=0.6)

        # --- second case: reset every result, then the new case ---
        net2 = T("net K⁺ flux: in", 24, YELLOW).move_to([1.5, -3.05, 0])
        vm_read2 = place(M("Vm = −100 mV", 30, TEAL), 0.0, 3.05)
        self.at("hold it at minus", nth=1)
        self.play(A.animate.move_to([inside_pos[1][0], inside_pos[1][1], 0]),
                  B.animate.move_to([inside_pos[3][0], inside_pos[3][1], 0]),
                  FadeOut(net), mv(vm, -70, -100), ReplacementTransform(vm_read, vm_read2), run_time=0.9)
        self.at("potassium comes in")
        self.play(C.animate.move_to([-4.2, 0.9, 0]), D.animate.move_to([-1.2, 0.9, 0]), run_time=0.4)
        self.play(C.animate.move_to([-4.2, -0.2, 0]), D.animate.move_to([-1.2, -0.2, 0]), run_time=0.4)
        self.play(C.animate.move_to([-3.45, -0.7, 0]), D.animate.move_to([-0.4, -0.7, 0]), FadeIn(net2), run_time=0.5)
        fold = chip("28-fold", ORANGE, size=24).move_to([-1.9, 2.0, 0])
        self.at("concentration difference")
        self.play(FadeIn(fold, scale=0.8), run_time=0.5)
        self.at("Only the voltage")
        self.play(Indicate(vm_read2, color=TEAL, scale_factor=1.12), Indicate(vm, color=TEAL), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pushes(SpokenScene):
    def construct(self):
        w = wall(-6.3, 6.3, 0.0, [0.0], s=1.6, t=0.5, plugs=False)
        lab_out = place(T("outside", 24, GREY), -6.3, 3.05)
        lab_in = place(T("inside", 24, GREY), -6.3, -3.05)
        k = ion(r=0.4, size=28)
        self.at("An ion feels")
        self.play(FadeIn(w), FadeIn(lab_out), FadeIn(lab_in), FadeIn(k, scale=0.7), run_time=0.8)

        o_arr = arr([0, 0.5, 0], [0, 2.0, 0], ORANGE, w=10)
        o_lab = T("concentration difference", 26, ORANGE)
        o_lab.move_to([-0.45 - o_lab.width / 2, 1.3, 0])
        self.at("concentration difference")
        self.play(GrowArrow(o_arr), FadeIn(o_lab), run_time=0.7)

        t_arr = arr([0, -0.5, 0], [0, -1.2, 0], TEAL, w=10)
        t_lab = place(T("voltage", 26, TEAL), 0.45, -1.3)
        self.at("membrane potential")
        self.play(GrowArrow(t_arr), FadeIn(t_lab), run_time=0.6)

        vm_txt = M("Vm = inside − outside", 28, TEAL).move_to([0, -3.15, 0])
        self.at("the inside minus")
        self.play(FadeIn(vm_txt), run_time=0.5)

        t_long = arr([0, -0.5, 0], [0, -2.6, 0], TEAL, w=10)
        self.at("pulls cations in")
        self.play(Transform(t_arr, t_long), run_time=0.8)

        t_bal = arr([0, -0.5, 0], [0, -2.0, 0], TEAL, w=10)
        self.at("balances")
        self.play(Transform(t_arr, t_bal), run_time=0.8)

        eq = chip("equilibrium potential", GREEN, size=28).move_to([0, 2.7, 0])
        self.at("equilibrium potential")
        self.play(FadeIn(eq, shift=DOWN * 0.15), run_time=0.5)

        k3 = ion(r=0.4, size=28).move_to([1.4, 1.5, 0])
        self.at("Ions still cross")
        self.play(FadeOut(o_arr), FadeOut(t_arr), FadeOut(o_lab), FadeOut(t_lab), run_time=0.3)
        self.play(k.animate.move_to([0, 1.0, 0]), run_time=0.3)
        self.play(k.animate.move_to([-1.4, 1.5, 0]), FadeIn(k3), run_time=0.3)
        self.play(k3.animate.move_to([0, -0.9, 0]), run_time=0.3)
        self.play(k3.animate.move_to([1.4, -1.5, 0]), run_time=0.3)
        net0 = M("net flux = 0", 28, GREEN).move_to([0, -2.5, 0])
        self.at("equal numbers")
        self.play(FadeIn(net0), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Nernst(SpokenScene):
    def construct(self):
        parts = ["E_X =", "(", "RT", "/", "zF", ")", "× ln(", "[X]out / [X]in", ")"]
        mobs = [M(s, 40, TEXT) for s in parts]
        eq = VGroup(*mobs).arrange(RIGHT, buff=0.3)
        fit(eq, max_w=12.2)
        eq.move_to([0, 0.6, 0])
        self.at("equation gives")
        self.play(Write(eq), run_time=1.6)

        zl = T("charge", 28, YELLOW).next_to(mobs[4], UP, buff=0.7)
        zl_line = Line(zl.get_bottom() + DOWN * 0.05, mobs[4].get_top() + UP * 0.08, color=YELLOW, stroke_width=3)
        self.at("the charge")
        self.play(FadeIn(zl), Create(zl_line), run_time=0.5)
        tl = T("temperature", 28, GREY).next_to(mobs[2], DOWN, buff=0.7)
        tl_line = Line(tl.get_top() + UP * 0.05, mobs[2].get_bottom() + DOWN * 0.08, color=GREY, stroke_width=3)
        self.at("the temperature")
        self.play(FadeIn(tl), Create(tl_line), run_time=0.5)
        rl_ = T("ratio of outside to\ninside concentration", 28, ORANGE).next_to(mobs[7], DOWN, buff=0.7)
        rl_line = Line(rl_.get_top() + UP * 0.05, mobs[7].get_bottom() + DOWN * 0.08, color=ORANGE, stroke_width=3)
        self.at("ratio of outside")
        self.play(FadeIn(rl_), Create(rl_line), run_time=0.6)

        # make room: shrink the equation to the top left, bring in the potassium numbers
        eq_small = eq.copy().scale(0.8)
        eq_small.move_to([-6.3 + eq_small.width / 2, 3.05, 0])
        ZERO = -3.0
        sc = 4.2 / 140.0
        bar_in = Rectangle(width=0.8, height=140 * sc, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                           fill_opacity=0.35).move_to([3.8, ZERO + 140 * sc / 2, 0])
        bar_out = Rectangle(width=0.8, height=5 * sc, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                            fill_opacity=0.35).move_to([2.6, ZERO + 5 * sc / 2, 0])
        lb_in = M("140 mM", 22, ORANGE).move_to([3.8, ZERO + 140 * sc + 0.3, 0])
        lb_out = M("5 mM", 22, ORANGE).move_to([2.6, ZERO + 5 * sc + 0.3, 0])
        lb_in2 = T("inside", 22, GREY).move_to([3.8, ZERO - 0.3, 0])
        lb_out2 = T("outside", 22, GREY).move_to([2.6, ZERO - 0.3, 0])
        self.at("teaching values")
        self.play(FadeOut(VGroup(zl, zl_line, tl, tl_line, rl_, rl_line)), Transform(eq, eq_small), run_time=0.9)
        self.play(GrowFromEdge(bar_in, DOWN), GrowFromEdge(bar_out, DOWN),
                  FadeIn(VGroup(lb_in, lb_out, lb_in2, lb_out2)), run_time=0.9)

        zt = place(T("K⁺:  z = +1,  37 °C", 26, GREY), -6.3, 2.1)
        rowC = place(M("E_K = 26.73 mV × ln( 5 / 140 )", 28, TEXT), -6.3, 1.0)
        self.at("For potassium")
        self.play(FadeIn(zt), run_time=0.4)
        self.play(Indicate(bar_out, color=ORANGE), Indicate(bar_in, color=ORANGE), run_time=1.0)
        self.play(Write(rowC), run_time=1.2)

        rowD = place(M("ln( 5 / 140 ) = −3.332", 28, TEXT), -6.3, -0.2)
        self.at("natural log")
        self.play(Write(rowD), run_time=1.0)

        rowE = place(M("E_K = 26.73 × (−3.332) = −89.1 mV", 28, GREEN), -6.3, -1.6)
        rl = ruler()
        ek = marker(-89.1, GREEN, "E_K", "R")
        self.at("Multiply by")
        self.play(Write(rowE), FadeIn(rl), run_time=1.3)
        self.at("potassium is")
        self.play(FadeIn(ek, shift=LEFT * 0.4), Indicate(rowE, color=GREEN, scale_factor=1.04), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
WX1 = 1.9      # right end of the big single-channel diagram
CHX = -2.2     # its channel


class S04Compare(SpokenScene):
    def construct(self):
        YW = 1.2
        w = wall(-6.3, WX1, YW, [CHX], s=1.5, t=0.5)
        w.remove(w.plug)
        lab_out = place(T("outside   5 mM", 24, ORANGE), -6.3, 3.1)
        lab_in = place(T("inside   140 mM", 24, ORANGE), -6.3, -0.35)
        rl = ruler()
        ek = marker(-89.1, GREEN, "E_K", "R")
        ek_txt = place(M("E_K = −89.1 mV", 26, GREEN), -2.6, -1.4)
        self.play(FadeIn(w), FadeIn(lab_out), FadeIn(lab_in), FadeIn(rl), FadeIn(ek), FadeIn(ek_txt), run_time=0.8)

        vm = marker(-70, TEAL, "Vm", "L")
        r1 = place(M("Vm = −70 mV", 26, TEAL), -6.3, -1.4)
        self.play(Indicate(ek, color=GREEN), run_time=1.0)
        self.at("At minus 70")
        self.play(FadeIn(vm, shift=RIGHT * 0.3), FadeIn(r1), run_time=0.7)

        gap = gap_bar(-70, -89.1)
        r2 = place(M("Vm − E_K = +19.1 mV", 28, PURPLE), -6.3, -2.2)
        self.at("the difference is")
        self.play(Create(gap), FadeIn(r2), run_time=0.7)

        r3 = place(T("K⁺ in: uphill,  +1.84 kJ/mol", 26, TEXT), -6.3, -3.0)
        self.at("uphill")
        self.play(FadeIn(r3), run_time=0.5)

        k = ion(r=0.4, size=28).move_to([CHX, 0.3, 0])
        arrow = arr([CHX, 0.55, 0], [CHX, 1.75, 0], YELLOW, w=9)
        net = place(T("net K⁺ flux: out", 26, YELLOW), CHX + 0.8, 2.4)
        self.at("net flow is outward")
        self.play(FadeIn(k), run_time=0.2)
        self.play(k.animate.move_to([CHX, 2.3, 0]), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(net), run_time=0.4)

        # reset every result, then the second case
        r1b = place(M("Vm = −100 mV", 26, TEAL), -6.3, -1.4)
        gap2 = gap_bar(-100, -89.1)
        self.at("At minus 100")
        self.play(FadeOut(k), FadeOut(arrow), FadeOut(net), FadeOut(r2), FadeOut(r3), FadeOut(gap),
                  mv(vm, -70, -100), ReplacementTransform(r1, r1b), run_time=0.9)

        r2b = place(M("Vm − E_K = −10.9 mV", 28, PURPLE), -6.3, -2.2)
        self.at("the difference is", nth=1)
        self.play(Create(gap2), FadeIn(r2b), run_time=0.7)

        r3b = place(T("K⁺ in: downhill,  −1.06 kJ/mol", 26, TEXT), -6.3, -3.0)
        self.at("downhill")
        self.play(FadeIn(r3b), run_time=0.5)

        k2 = ion(r=0.4, size=28).move_to([CHX, 2.3, 0])
        arrow2 = arr([CHX, 1.75, 0], [CHX, 0.65, 0], YELLOW, w=9)
        net2 = place(T("net K⁺ flux: in", 26, YELLOW), CHX + 0.8, 2.4)
        self.at("net flow is inward")
        self.play(FadeIn(k2), run_time=0.2)
        self.play(k2.animate.move_to([CHX, 0.3, 0]), run_time=0.8)
        self.play(GrowArrow(arrow2), FadeIn(net2), run_time=0.4)
        self.at("outweighs")
        self.play(Indicate(r2b, color=PURPLE, scale_factor=1.05), Indicate(vm, color=TEAL), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Current(SpokenScene):
    def construct(self):
        # carried over from the end of the last scene
        YW = 1.2
        w = wall(-6.3, WX1, YW, [CHX], s=1.5, t=0.5)
        w.remove(w.plug)
        lab_out = place(T("outside   5 mM", 24, ORANGE), -6.3, 3.1)
        lab_in = place(T("inside   140 mM", 24, ORANGE), -6.3, -0.35)
        k = ion(r=0.4, size=28).move_to([CHX, 0.3, 0])
        arrow = arr([CHX, 1.75, 0], [CHX, 0.65, 0], YELLOW, w=9)
        net = place(T("net K⁺ flux: in", 26, YELLOW), CHX + 0.8, 2.4)
        rl = ruler()
        ek = marker(-89.1, GREEN, "E_K", "R")
        vm = marker(-100, TEAL, "Vm", "L")
        gap0 = gap_bar(-100, -89.1)
        diagram = VGroup(w, lab_out, lab_in, k, arrow, net)
        self.add(diagram, rl, ek, vm, gap0)
        self.at("The same difference")
        self.play(Indicate(gap0, color=PURPLE, scale_factor=1.3), run_time=0.8)

        # trace panel
        x0, x1, yb, yo = -5.4, 2.3, 0.6, 2.2
        axes = VGroup(Line([x0, yb, 0], [x1, yb, 0], color=GREY, stroke_width=2),
                      Line([x0, yb - 0.3, 0], [x0, yo + 0.4, 0], color=GREY, stroke_width=3))
        zero = T("0", 24, GREY).move_to([x0 - 0.3, yb, 0])
        head = place(T("current through one K⁺ channel", 26, GREY), -6.3, 3.05)
        self.at("one channel")
        self.play(FadeOut(diagram), FadeIn(axes), FadeIn(zero), FadeIn(head), run_time=0.8)

        r1 = place(M("γ = 20 pS", 30, TEXT), -6.3, -0.4)
        self.at("conductance")
        self.play(FadeIn(r1), run_time=0.5)

        gap = gap_bar(-40, -89.1)
        gl = M("49.1 mV", 24, PURPLE).move_to([RX - 1.2, (vy(-40) + vy(-89.1)) / 2, 0])
        self.at("sits at minus")
        self.play(mv(vm, -100, -40), FadeOut(gap0), run_time=0.7)
        self.at("The difference is")
        self.play(Create(gap), FadeIn(gl), run_time=0.7)

        r2 = place(M("i = γ × (Vm − E_K)", 30, TEXT), -6.3, -1.3)
        r3 = place(M("= 20 pS × 49.1 mV = 0.98 pA", 30, YELLOW), -6.3, -2.2)
        self.at("so the current is")
        self.play(Write(r2), run_time=0.8)
        self.play(Write(r3), run_time=0.8)

        # the trace: closed 0 pA, open 0.98 pA, outward = up
        opens = [(0.06, 0.20), (0.27, 0.32), (0.40, 0.63), (0.70, 0.74), (0.82, 0.95)]
        pts = [[x0, yb, 0]]
        for a, b in opens:
            xa, xb = x0 + a * (x1 - x0), x0 + b * (x1 - x0)
            pts += [[xa, yb, 0], [xa, yo, 0], [xb, yo, 0], [xb, yb, 0]]
        pts.append([x1, yb, 0])
        tr = VMobject(color=YELLOW, stroke_width=5).set_points_as_corners(pts)
        lvl = place(M("0.98 pA", 24, YELLOW), x1 + 0.2, yo)
        self.at("picoamps outward")
        self.play(Create(tr, rate_func=linear), FadeIn(lvl), run_time=2.4)

        r4 = place(T("about 6.1 million ions per second", 34, YELLOW, weight=BOLD), -6.3, -3.1)
        self.at("ions per second")
        self.play(FadeIn(r4, shift=UP * 0.15), run_time=0.6)

        # rate comparison on a log axis
        ax0, ax1 = -5.4, 5.4
        per = (ax1 - ax0) / 7.0
        X = lambda e: ax0 + e * per
        base = Line([ax0, -2.3, 0], [ax1, -2.3, 0], color=GREY, stroke_width=3)
        tks = VGroup()
        for e, s in ((0, "1"), (2, "100"), (4, "10,000"), (6, "1,000,000")):
            tks.add(Line([X(e), -2.3, 0], [X(e), -2.45, 0], color=GREY, stroke_width=3))
            tks.add(M(s, 22, GREY).move_to([X(e), -2.8, 0]))
        axt = T("per second (log scale)", 22, GREY).move_to([0, -3.3, 0])
        chb = Rectangle(width=X(np.log10(6.1e6)) - ax0, height=0.6, stroke_color=BLUE, stroke_width=3,
                        fill_color=BLUE, fill_opacity=0.5).move_to([(ax0 + X(np.log10(6.1e6))) / 2, 1.2, 0])
        chl = place(T("one channel: ions", 26, BLUE), ax0, 1.85)
        title = T("about 6.1 million ions per second", 29, YELLOW, weight=BOLD).move_to([0, 3.0, 0])
        self.at("A carrier cycling")
        self.play(*[FadeOut(m) for m in (rl, ek, vm, gap, gl, axes, zero, head, r1, r2, r3, tr, lvl, r4)], run_time=0.5)
        self.play(FadeIn(title), Create(base), FadeIn(tks), FadeIn(axt), GrowFromEdge(chb, LEFT), FadeIn(chl), run_time=0.7)
        cab = Rectangle(width=X(np.log10(3000)) - X(2), height=0.6, stroke_color=PINK, stroke_width=3,
                        fill_color=PINK, fill_opacity=0.5).move_to([(X(2) + X(np.log10(3000))) / 2, -0.7, 0])
        cal = place(T("a carrier: cycles, a range of hundreds to a few thousand", 26, PINK), ax0, -0.05)
        self.at("hundreds or a few thousand")
        self.play(FadeIn(cab, scale=0.9), FadeIn(cal), run_time=0.8)
        self.at("could not carry that")
        self.play(Indicate(cab, color=PINK, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        YW = 1.0
        w = wall(-6.3, WX1, YW, [CHX], s=1.5, t=0.5)
        w.remove(w.plug)
        lab_out = place(T("[X] outside", 24, ORANGE), -6.3, 3.1)
        lab_in = place(T("[X] inside", 24, ORANGE), -6.3, -0.55)
        rl = ruler()
        self.at("Here is the rule")
        self.play(FadeIn(w), FadeIn(rl), run_time=0.7)

        ex = marker(-89.1, GREEN, "E_X", "R")
        self.at("Find the equilibrium potential")
        self.play(FadeIn(ex, shift=LEFT * 0.4), FadeIn(lab_out), FadeIn(lab_in), run_time=0.8)

        chipc = chip("cation  K⁺:  z = +1", YELLOW, size=26).move_to([-3.2, -1.8, 0])
        self.at("sign of the charge")
        self.play(FadeIn(chipc, shift=UP * 0.15), run_time=0.6)

        vm = marker(-70, TEAL, "Vm", "L")
        k = ion(r=0.4, size=28).move_to([CHX, 0.1, 0])
        arrow = arr([CHX, 0.35, 0], [CHX, 1.55, 0], YELLOW, w=9)
        net = place(T("net flow: out", 26, YELLOW), CHX + 0.8, 2.2)
        self.at("less negative than")
        self.play(FadeIn(vm, shift=RIGHT * 0.3), FadeIn(k), run_time=0.5)
        self.play(k.animate.move_to([CHX, 2.1, 0]), run_time=0.8)
        self.play(GrowArrow(arrow), FadeIn(net), run_time=0.4)

        arrow_in = arr([CHX, 1.55, 0], [CHX, 0.45, 0], YELLOW, w=9)
        net_in = place(T("net flow: in", 26, YELLOW), CHX + 0.8, 2.2)
        k_in = ion(r=0.4, size=28).move_to([CHX, 2.1, 0])
        self.at("more negative voltage")
        self.play(FadeOut(k), FadeOut(arrow), FadeOut(net), mv(vm, -70, -100), run_time=0.7)
        self.play(FadeIn(k_in), run_time=0.2)
        self.play(k_in.animate.move_to([CHX, 0.1, 0]), run_time=0.8)
        self.play(GrowArrow(arrow_in), FadeIn(net_in), run_time=0.4)

        chipa = chip("anion  Cl⁻:  z = −1", YELLOW, size=26).move_to([-3.2, -1.8, 0])
        cl = ion("Cl⁻", r=0.42, size=26).move_to([CHX, 0.1, 0])
        arrow_out = arr([CHX, 0.35, 0], [CHX, 1.55, 0], YELLOW, w=9)
        net_out = place(T("net flow: out", 26, YELLOW), CHX + 0.8, 2.2)
        self.at("For an anion")
        self.play(mv(ex, -89.1, -60), FadeOut(lab_out), FadeOut(lab_in), ReplacementTransform(chipc, chipa), FadeOut(k_in), FadeOut(arrow_in), FadeOut(net_in), run_time=0.7)
        self.at("the rule flips")
        self.play(FadeIn(cl), run_time=0.3)
        self.play(cl.animate.move_to([CHX, 2.1, 0]), run_time=0.8)
        self.play(GrowArrow(arrow_out), FadeIn(net_out), run_time=0.4)

        gapb = gap_bar(-100, -60)
        cmp_t = M("compare  Vm  with  E_X", 28, TEXT).move_to([-3.0, -3.0, 0])
        self.at("Compare the membrane voltage")
        self.play(Create(gapb), FadeOut(chipa), FadeIn(cmp_t), run_time=0.8)
        self.at("passive flow goes")
        self.play(Indicate(arrow_out, color=YELLOW), Indicate(cl), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Compare the membrane voltage with the equilibrium potential."
