"""Rest is where the leaks cancel  (Biochemistrypedia Neuroscience explainer)

Everything is the lesson's made-up neuron (37 C): EK -95 mV, ENa +60.6 mV, Vm -71.2 mV.

COLOR MAP (one color per concept, whole video)
  BLUE   = potassium (K+, EK, gK, PK)
  ORANGE = sodium (Na+, ENa, gNa, PNa)
  YELLOW = the membrane voltage Vm
  GREEN  = zero net current / the rule
  PURPLE = the Na+/K+ pump
  GREY   = cell outline, membrane, axes, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
KC, NAC, VC, NETC = BLUE, ORANGE, YELLOW, GREEN

SpokenScene.q = lambda self, f: min(max(self.beat(f), 0.5), 1.1)

AX = -3.2
def Y(v):
    return (v + 100) * 0.036 - 3.0


def bchip(text, color=BLUE, size=24, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def axis_line():
    ln = Line([AX, Y(-100), 0], [AX, Y(64), 0], color=GREY, stroke_width=3)
    zero = VGroup(Line([AX - 0.12, Y(0), 0], [AX + 0.12, Y(0), 0], color=GREY, stroke_width=3),
                  T("0", 22, GREY).next_to([AX - 0.15, Y(0), 0], LEFT, buff=0.1))
    unit = T("mV", 22, GREY).move_to([AX, Y(64) + 0.35, 0])
    return VGroup(ln, zero, unit)


def ref(v, color, label, ext=False, size=26):
    parts = [Line([AX, Y(v), 0], [AX + 0.5, Y(v), 0], color=color, stroke_width=5)]
    if ext:
        parts.append(DashedLine([AX + 0.5, Y(v), 0], [6.2, Y(v), 0], color=color, stroke_width=2,
                                dash_length=0.12).set_opacity(0.45))
    lab = T(label, size, color).next_to([AX - 0.15, Y(v), 0], LEFT, buff=0.12)
    return VGroup(*parts, lab)


def vm_marker(v, label=None):
    dot = Dot([AX, Y(v), 0], radius=0.14, color=VC)
    parts = [dot]
    if label:
        parts.append(T(label, 26, VC).next_to([AX - 0.2, Y(v), 0], LEFT, buff=0.12))
    return VGroup(*parts)


def vbracket(v1, v2, color, x=AX + 0.45):
    return Arrow([x, Y(v1), 0], [x, Y(v2), 0], buff=0, color=color, stroke_width=6, tip_length=0.2,
                 max_tip_length_to_length_ratio=0.5)


def seg(text, size, color, **kw):
    return M(text, size, color, **kw)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The Resting Membrane and Passive Signals"
    TITLE = "Rest Is Where the Leaks Cancel"


# ---------------------------------------------------------------------------------------------
class S01Standoff(SpokenScene):
    def construct(self):
        cell = Ellipse(width=5.4, height=4.0, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08)
        cell.move_to([-2.6, -0.3, 0])
        name = T("made-up neuron", 28, TEXT).move_to(cell.get_center() + UP * 0.35)
        vmt = M("Vm = −71 mV", 28, VC).move_to(cell.get_center() + DOWN * 0.45)
        self.play(Create(cell), run_time=self.q(0.08))
        self.play(FadeIn(name), run_time=self.q(0.05))
        self.at("resting at minus")
        self.play(FadeIn(vmt), run_time=self.q(0.05))

        self.at("Potassium current leaves")
        ka = Arrow([-2.6, 1.75, 0], [-2.6, 3.2, 0], buff=0, color=KC, stroke_width=8, tip_length=0.3)
        kl = T("K+ out, about 200 pA", 28, KC).next_to(ka, RIGHT, buff=0.25)
        self.play(GrowArrow(ka), FadeIn(kl), run_time=self.q(0.07))

        self.at("Sodium current enters")
        na = Arrow([-2.6, -3.35, 0], [-2.6, -2.35, 0], buff=0, color=NAC, stroke_width=8, tip_length=0.3)
        nl = T("Na+ in, about 200 pA", 28, NAC).next_to(na, RIGHT, buff=0.25)
        self.play(GrowArrow(na), FadeIn(nl), run_time=self.q(0.07))

        self.at("Neither ion")
        note = T("no ion at its equilibrium", 28, GREY).move_to([3.6, -1.7, 0])
        self.play(FadeIn(note), run_time=self.q(0.05))

        self.at("Yet the voltage")
        ax = VGroup(Line([2.2, -0.6, 0], [2.2, 2.0, 0], color=GREY, stroke_width=3),
                    Line([2.2, -0.6, 0], [6.2, -0.6, 0], color=GREY, stroke_width=3),
                    T("time", 22, GREY).move_to([5.8, -0.95, 0]),
                    T("Vm", 26, VC).move_to([1.75, 1.75, 0]))
        trace = Line([2.2, 0.9, 0], [6.2, 0.9, 0], color=VC, stroke_width=6)
        self.play(FadeIn(ax), run_time=self.q(0.04))
        self.play(Create(trace), run_time=self.q(0.10))

        self.at("Why")
        q = T("Why?", 72, VC, weight=BOLD).move_to([3.6, -2.8, 0])
        self.play(FadeIn(q, scale=1.3), run_time=self.q(0.05))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Driving(SpokenScene):
    def construct(self):
        axis = axis_line()
        self.play(Create(axis), run_time=self.q(0.05))

        self.at("equilibrium potential")
        d1 = T("equilibrium potential E: electrical force", 26, TEXT)
        d2 = T("balances the concentration gradient", 26, TEXT)
        d = VGroup(d1, d2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([1.6, 1.5, 0])
        d.align_to([-2.2, 0, 0], LEFT)
        self.play(FadeIn(d, shift=UP * 0.1), run_time=self.q(0.07))

        self.at("For potassium", nth=0)
        ek = ref(-95, KC, "EK  −95 mV", ext=True)
        self.play(FadeIn(ek, shift=RIGHT * 0.3), run_time=self.q(0.06))

        self.at("For sodium", nth=0)
        ena = ref(60.6, NAC, "ENa  +60.6 mV", ext=True)
        self.play(FadeIn(ena, shift=RIGHT * 0.3), run_time=self.q(0.06))

        self.at("Driving force is")
        df = T("driving force = Vm − E", 34, TEXT).move_to([1.6, 1.5, 0]).align_to([-2.2, 0, 0], LEFT)
        vm = vm_marker(-71.2, "Vm  −71.2 mV")
        vmline = DashedLine([AX + 0.5, Y(-71.2), 0], [6.2, Y(-71.2), 0], color=VC, stroke_width=2,
                            dash_length=0.12).set_opacity(0.45)
        self.play(FadeOut(d), FadeIn(df), FadeIn(vm), FadeIn(vmline), run_time=self.q(0.07))

        self.at("For potassium", nth=1)
        kb = vbracket(-95, -71.2, KC, x=AX + 0.8)
        kt = M("−71.2 − (−95) = +23.8 mV", 26, KC).move_to([1.0, Y(-83.1), 0]).align_to([-2.0, 0, 0], LEFT)
        self.play(GrowArrow(kb), FadeIn(kt), run_time=self.q(0.06))
        self.at("so the current goes outward")
        ko = bchip("outward", KC, size=24).next_to(kt, RIGHT, buff=0.3)
        self.play(FadeIn(ko), run_time=self.q(0.04))

        self.at("For sodium", nth=1)
        nb = vbracket(60.6, -71.2, NAC, x=AX + 0.8)
        nt = M("−71.2 − 60.6 = −131.8 mV", 26, NAC).move_to([1.0, Y(-5), 0]).align_to([-1.8, 0, 0], LEFT)
        self.play(GrowArrow(nb), FadeIn(nt), run_time=self.q(0.08))
        self.at("so the current goes inward")
        no = bchip("inward", NAC, size=24).next_to(nt, RIGHT, buff=0.3)
        self.play(FadeIn(no), run_time=self.q(0.04))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cancel(SpokenScene):
    def construct(self):
        axis = axis_line()
        ek = ref(-95, KC, "EK  −95 mV")
        ena = ref(60.6, NAC, "ENa  +60.6 mV")
        vm = vm_marker(-71.2, "Vm  −71.2 mV")
        self.add(axis, ek, ena, vm)
        X0 = -2.4

        self.at("Current is conductance")
        f = M("current = g × driving force", 30, TEXT).move_to([2.0, 3.0, 0])
        self.play(FadeIn(f, shift=UP * 0.1), run_time=self.q(0.06))

        def row(y, parts, color):
            g, dfc, res = parts
            a = bchip(g, color, size=24)
            t1 = T("×", 28, TEXT)
            b = bchip(dfc, color, size=24)
            t2 = T("=", 28, TEXT)
            c = bchip(res, color, size=24)
            grp = VGroup(a, t1, b, t2, c).arrange(RIGHT, buff=0.18)
            grp.move_to([0, y, 0]).align_to([X0, 0, 0], LEFT)
            return grp

        self.at("Potassium has")
        kr = row(2.0, ("gK = 8.47 nS", "+23.8 mV", "+202 pA out"), KC)
        # reveal g first, rest on following cues
        self.play(FadeIn(kr[0]), run_time=self.q(0.05))
        self.at("That gives about")
        self.play(FadeIn(kr[1:]), run_time=self.q(0.07))

        self.at("Sodium has only")
        nr = row(1.0, ("gNa = 1.53 nS", "−131.8 mV", "−202 pA in"), NAC)
        self.play(FadeIn(nr[0]), run_time=self.q(0.05))
        self.at("But its driving force")
        self.play(FadeIn(nr[1]), run_time=self.q(0.05))
        self.at("It gives")
        self.play(FadeIn(nr[2:]), run_time=self.q(0.05))

        # bars
        base = Line([1.8, -2.45, 0], [1.8, 0.0, 0], color=GREY, stroke_width=3)
        kbar = Rectangle(width=2.4, height=0.5, stroke_width=0, fill_color=KC, fill_opacity=0.85)
        kbar.move_to([1.8 + 1.2, -0.6, 0])
        nbar = Rectangle(width=2.4, height=0.5, stroke_width=0, fill_color=NAC, fill_opacity=0.85)
        nbar.move_to([1.8 - 1.2, -1.5, 0])
        kl = T("+202 pA", 24, KC).next_to(kbar, RIGHT, buff=0.15)
        nl = T("−202 pA", 24, NAC).next_to(nbar, LEFT, buff=0.15)
        self.at("The two cancel")
        net = bchip("net current = 0", NETC, size=28).move_to([1.8, -2.45 - 0.0 + 0.0, 0]).shift(DOWN * 0.1)
        self.play(Create(base), GrowFromEdge(kbar, LEFT), GrowFromEdge(nbar, RIGHT),
                  FadeIn(kl), FadeIn(nl), FadeIn(net, scale=1.1), run_time=0.8)

        self.at("Rest means zero")
        nt = T("not zero for each ion", 28, TEXT).move_to([1.8, -3.25, 0])
        self.play(FadeIn(nt), run_time=self.q(0.05))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Pump(SpokenScene):
    def construct(self):
        mem = Rectangle(width=12.2, height=1.1, stroke_color=GREY, stroke_width=3,
                        fill_color=GREY, fill_opacity=0.25).move_to([0, 0, 0])
        out = T("outside", 26, GREY).move_to([-5.4, 0.95, 0])
        ins = T("inside", 26, GREY).move_to([-5.4, -0.95, 0])
        kleak = bchip("K+ leak", KC, size=28).move_to([-3.4, 0, 0])
        naleak = bchip("Na+ leak", NAC, size=28).move_to([-0.8, 0, 0])
        self.add(mem, out, ins, kleak, naleak)

        self.at("Left alone")
        ka = Arrow([-3.4, 0.7, 0], [-3.4, 2.6, 0], buff=0, color=KC, stroke_width=8, tip_length=0.3)
        na = Arrow([-0.8, 2.6, 0], [-0.8, 0.7, 0], buff=0, color=NAC, stroke_width=8, tip_length=0.3)
        kt = T("K+ out", 28, KC).next_to(ka, RIGHT, buff=0.15)
        nt = T("Na+ in", 28, NAC).next_to(na, RIGHT, buff=0.15)
        self.play(GrowArrow(ka), GrowArrow(na), FadeIn(kt), FadeIn(nt), run_time=0.6)
        warn = T("leaks alone: the gradients run down", 30, RED).move_to([-1.8, -2.4, 0])
        self.play(FadeIn(warn), run_time=0.5)

        self.at("The sodium potassium pump")
        pump = bchip("Na+/K+ pump", PURPLE, size=28).move_to([3.9, 0, 0])
        self.play(FadeIn(pump, scale=1.2), run_time=0.6)

        def ion(sym, color):
            c = Circle(radius=0.32, color=color, stroke_width=3, fill_color=color, fill_opacity=0.25)
            return VGroup(c, T(sym, 22, color).move_to(c))

        self.at("three sodium out")
        nas = VGroup(*[ion("Na", NAC) for _ in range(3)]).arrange(RIGHT, buff=0.12).move_to([3.2, -1.5, 0])
        self.add(nas)
        self.play(nas.animate.move_to([3.2, 1.8, 0]), run_time=1.0)
        nlab = T("3 Na+ out", 28, NAC).next_to(nas, UP, buff=0.2)
        self.play(FadeIn(nlab), run_time=0.4)

        self.at("two potassium in")
        ks = VGroup(*[ion("K", KC) for _ in range(2)]).arrange(RIGHT, buff=0.12).move_to([5.3, 1.8, 0])
        self.add(ks)
        self.play(ks.animate.move_to([5.3, -1.5, 0]), run_time=1.0)
        klab = T("2 K+ in", 28, KC).next_to(ks, DOWN, buff=0.2)
        self.play(FadeIn(klab), run_time=0.4)

        self.at("Its main job")
        job = T("main job: keep the gradients", 30, PURPLE).move_to([-1.8, -2.4, 0])
        self.play(FadeOut(warn), FadeIn(job), run_time=0.5)

        self.at("So rest is")
        ss = bchip("rest = steady state, not equilibrium", NETC, size=30).move_to([0, -3.2, 0])
        self.play(FadeOut(job), FadeIn(ss), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def pbar(x, h, color, label, name):
    base_y = -2.3
    r = Rectangle(width=1.0, height=max(h, 0.04), stroke_width=0, fill_color=color, fill_opacity=0.85)
    r.move_to([x, base_y + max(h, 0.04) / 2, 0])
    lab = T(label, 26, color).move_to([x, base_y - 0.45, 0])
    return r, lab


class S05Weights(SpokenScene):
    def construct(self):
        axis = axis_line()
        ek = ref(-95, KC, "EK  −95 mV")
        ena = ref(60.6, NAC, "ENa  +60.6 mV")
        self.add(axis, ek, ena)

        self.at("The Goldman Hodgkin Katz equation")
        ghk = T("Goldman-Hodgkin-Katz: passive currents sum to 0", 26, TEXT).move_to([1.6, 3.0, 0])
        ghk.align_to([-2.2, 0, 0], LEFT)
        self.play(FadeIn(ghk, shift=UP * 0.1), run_time=self.q(0.07))

        self.at("Each ion counts")
        rp = T("relative permeability", 26, GREY).move_to([3.4, 2.1, 0])
        self.play(FadeIn(rp), run_time=self.q(0.05))

        self.at("potassium is")
        kb, kl = pbar(2.3, 3.6, KC, "PK = 1", "k")
        self.play(GrowFromEdge(kb, DOWN), FadeIn(kl), run_time=self.q(0.06))
        nb, nl = pbar(4.6, 3.6 * 0.04, NAC, "PNa = 0.04", "na")
        self.play(GrowFromEdge(nb, DOWN), FadeIn(nl), run_time=self.q(0.04))

        self.at("The result is")
        vm = vm_marker(-71.2, "Vm  −71.2 mV")
        self.play(FadeIn(vm, scale=1.4), run_time=self.q(0.06))

        self.at("That's its")
        br = vbracket(-95, -71.2, KC)
        bt = T("24 mV above EK", 26, KC).move_to([-2.2, Y(-83.1), 0]).align_to([-2.2, 0, 0], LEFT)
        self.play(GrowArrow(br), FadeIn(bt), run_time=self.q(0.06))

        self.at("The small sodium leak")
        self.play(Indicate(VGroup(nb, nl), color=NAC, scale_factor=1.25), run_time=self.q(0.08))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        axis = axis_line()
        ek = ref(-95, KC, "EK  −95 mV")
        ena = ref(60.6, NAC, "ENa  +60.6 mV")
        vm = vm_marker(-71.2, "Vm  −71.2 mV")
        rp = T("relative permeability", 26, GREY).move_to([3.4, 2.1, 0])
        kb, kl = pbar(2.3, 3.6, KC, "PK = 1", "k")
        nb, nl = pbar(4.6, 3.6 * 0.04, NAC, "PNa = 0.04", "na")
        self.add(axis, ek, ena, vm, rp, kb, kl, nb, nl)

        self.at("Now double")
        nb2, nl2 = pbar(4.6, 3.6 * 0.08, NAC, "PNa = 0.08", "na")
        self.play(Transform(nb, nb2), Transform(nl, nl2), run_time=self.q(0.07))

        self.at("The balance point")
        ghost = Dot([AX, Y(-71.2), 0], radius=0.14, color=VC).set_opacity(0.35)
        self.add(ghost)
        new_lab = T("Vm  −58.9 mV", 26, VC).next_to([AX - 0.2, Y(-58.9), 0], LEFT, buff=0.12)
        new_dot = Dot([AX, Y(-58.9), 0], radius=0.14, color=VC)
        old_lab = vm[1]
        self.play(FadeOut(old_lab), vm[0].animate.move_to([AX, Y(-58.9), 0]), run_time=self.q(0.07))
        self.play(FadeIn(new_lab), run_time=self.q(0.03))
        br = vbracket(-71.2, -58.9, NAC)
        bt = T("12 mV toward ENa", 26, NAC).move_to([-2.2, -2.0, 0]).align_to([-2.2, 0, 0], LEFT)
        bt.shift(DOWN * 0.0)
        self.play(GrowArrow(br), FadeIn(bt), run_time=self.q(0.05))

        self.at("Raising one")
        self.play(FadeOut(VGroup(rp, kb, kl, nb, nl)), run_time=self.q(0.04))
        r1 = bchip("raise one ion's permeability", TEXT, size=28).move_to([1.8, 2.9, 0]).align_to([-2.2, 0, 0], LEFT)
        r1[1].set_stroke(GREY); r1[1].set_fill(GREY, 0.12)
        r2 = bchip("Vm moves toward that ion's E", YELLOW, size=28).next_to(r1, DOWN, buff=0.3).align_to(r1, LEFT)
        self.play(FadeIn(r1, shift=RIGHT * 0.2), run_time=self.q(0.04))
        self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=self.q(0.05))

        self.at("Other cells")
        oc = T("other cells, other ratios:", 28, GREY).move_to([1.8, 1.05, 0]).align_to([-2.2, 0, 0], LEFT)
        oc2 = T("no universal resting potential", 28, GREY).next_to(oc, DOWN, buff=0.15).align_to(oc, LEFT)
        self.play(FadeIn(oc), FadeIn(oc2), run_time=self.q(0.05))

        self.at("Keep this rule")
        rule = bchip("Rest is where the leaks cancel", NETC, size=30)
        rule2 = bchip("permeability sets where", NETC, size=30)
        rg = VGroup(rule, rule2).arrange(DOWN, buff=0.2).move_to([1.8, -0.8, 0]).align_to([-2.2, 0, 0], LEFT)
        self.play(FadeIn(rg, scale=1.05), run_time=self.q(0.06))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Rest is where the leaks cancel; permeability sets where."
