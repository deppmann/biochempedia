"""Glia feed the axons they wrap  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the neuron / axon
  TEAL   = myelinating glia (oligodendrocyte / the glial cell that wraps axons)
  PURPLE = astrocyte
  ORANGE = lactate (and pyruvate, its partner)
  YELLOW = ATP
  GREY   = myelin, membranes, transporter gates, ions, outlines
  GREEN  = evidence for / axon intact
  RED    = blocked, failure, evidence against
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rrect(w, h, color, fo=0.15, sw=3, r=0.2):
    return RoundedRectangle(corner_radius=min(r, w / 2, h / 2), width=w, height=h, stroke_color=color,
                            stroke_width=sw, fill_color=color, fill_opacity=fo)


def dot(label, color, r=0.27, size=22, fo=0.3):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fo)
    return VGroup(c, T(label, size, TEXT).move_to(c))


def mito(x, y, w=1.0, h=0.55, color=YELLOW):
    o = Ellipse(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.18)
    pts = [[-w * .30, 0, 0], [-w * .18, h * .22, 0], [-w * .06, -h * .22, 0], [w * .06, h * .22, 0],
           [w * .18, -h * .22, 0], [w * .30, 0, 0]]
    ins = VMobject(color=color, stroke_width=3).set_points_as_corners(pts)
    return VGroup(o, ins).move_to([x, y, 0])


def gate(x, y, color=GREY, h=0.95):
    """a transporter shown as a small gate: two blocks with a narrow passage between them."""
    a = rrect(0.5, h, color, 0.5, 3, 0.1).move_to([x - 0.45, y, 0])
    b = rrect(0.5, h, color, 0.5, 3, 0.1).move_to([x + 0.45, y, 0])
    return VGroup(a, b)


def ferry(scene, src, name="lactate", end_y=-0.95):
    """a lactate dot leaves the chip at `src`, passes the gate, and becomes a chip in the axon."""
    d0 = Circle(radius=0.14, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(src)
    scene.play(FadeIn(d0, scale=0.5), run_time=0.25)
    scene.play(d0.animate.move_to([GATE_X, 1.25, 0]), run_time=0.7)
    scene.play(d0.animate.move_to([GATE_X, GATE_Y, 0]), run_time=0.5)
    scene.play(d0.animate.move_to([GATE_X, -0.7, 0]), run_time=0.5)
    c2 = chip(name, ORANGE, 22).move_to([GATE_X, end_y, 0])
    scene.play(ReplacementTransform(d0, c2), run_time=0.3)
    return c2


def cross(c, color=RED, s=0.3):
    return VGroup(Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=7),
                  Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=7))


def card(title, lines, color, w=6.0):
    t = T(title, 26, color, weight=BOLD)
    ls = VGroup(*[T(l, 22, TEXT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    g = VGroup(t, ls).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    box = rrect(g.width + 0.6, g.height + 0.4, color, 0.1, 3, 0.15).move_to(g)
    g.move_to(box)
    return VGroup(box, g)


# geometry shared by scenes 3, 5, 6: glia on top, axon below, a gap with the transporter between
GLIA_C = np.array([0, 2.0, 0]); GLIA_W, GLIA_H = 11.8, 2.7
AX_C = np.array([0, -1.75, 0]); AX_W, AX_H = 11.8, 2.9
GATE_X = 3.6; GATE_Y = 0.175


def glia_axon(glia_label="myelinating glial cell"):
    glia = rrect(GLIA_W, GLIA_H, TEAL, 0.14, 4, 0.7).move_to(GLIA_C)
    ax = rrect(AX_W, AX_H, BLUE, 0.14, 4, 0.7).move_to(AX_C)
    gl = T(glia_label, 24, TEAL).move_to([-3.6, 2.85, 0])
    al = T("axon", 24, BLUE).move_to([-4.7, -2.75, 0])
    return glia, ax, gl, al


class S00Title(TitleCard):
    LESSON = "Glia as metabolic partners"
    TITLE = "Glia Feed the Axons They Wrap"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        base = Line([-4.0, -2.4, 0], [4.0, -2.4, 0], color=GREY, stroke_width=3)
        b1 = Rectangle(width=1.8, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.9)
        b2 = Rectangle(width=1.8, height=3.0, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        b1.move_to([-2.0, -2.4 + 0.15, 0]); b2.move_to([2.0, -2.4 + 1.5, 0])
        l1 = T("body weight", 26, GREY).move_to([-2.0, -2.8, 0])
        l2 = T("resting energy", 26, YELLOW).move_to([2.0, -2.8, 0])
        brain = T("The brain", 44, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(FadeIn(brain), Create(base), run_time=0.8)
        self.at("your weight")
        v1 = M("about 2%", 32, GREY).next_to(b1, UP, buff=0.2)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), FadeIn(v1), run_time=0.8)
        self.at("energy you spend")
        v2 = M("about 20%", 32, YELLOW).next_to(b2, UP, buff=0.2)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), FadeIn(v2), run_time=1.2)
        self.at("axons and synapses")
        self.play(FadeOut(VGroup(brain, base, b1, b2, l1, l2, v1, v2)), run_time=0.6)

        soma = Circle(radius=0.75, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to([-5.5, 0, 0])
        soma_l = T("cell body", 24, BLUE).next_to(soma, DOWN, buff=0.2)
        self.play(FadeIn(soma), FadeIn(soma_l), run_time=0.6)
        tube = Rectangle(width=10.9, height=0.24, stroke_width=0, fill_color=BLUE, fill_opacity=0.9)
        tube.move_to([-5.0 + 5.45, 0, 0])
        self.at("motor axon")
        self.play(GrowFromEdge(tube, LEFT), run_time=1.6)
        end = Circle(radius=0.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3).move_to([5.95, 0, 0])
        self.add(end)
        brace = DoubleArrow([-4.9, -1.35, 0], [6.1, -1.35, 0], color=GREY, buff=0, stroke_width=4, tip_length=0.2)
        blab = T("about a metre", 28, GREY).next_to(brace, DOWN, buff=0.15)
        self.play(GrowFromCenter(brace), FadeIn(blab), run_time=0.8)
        sheaths = VGroup(*[rrect(1.7, 0.9, GREY, 0.5, 3, 0.35).move_to([-3.7 + i * 1.95, 0, 0]) for i in range(5)])
        myl = T("myelin", 28, GREY).move_to([0.2, 1.05, 0])
        self.at("myelin wraps")
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sheaths], lag_ratio=0.25), FadeIn(myl), run_time=1.6)
        fluid = T("fluid outside", 26, TEAL).move_to([0.2, 3.0, 0])
        xs_x = [sheaths[1].get_center()[0], sheaths[3].get_center()[0]]
        ars = VGroup(*[arr([x, 2.6, 0], [x, 0.7, 0], TEAL, 4) for x in xs_x])
        xs = T("limited access", 26, TEAL).move_to([0.2, 1.7, 0])
        self.at("limits access")
        self.play(FadeIn(fluid), FadeIn(ars), run_time=0.6)
        self.play(FadeIn(xs), run_time=0.4)
        qs = T("?", 64, YELLOW, weight=BOLD).move_to([5.95, 0.85, 0])
        self.at("far end fed")
        self.play(FadeIn(qs, scale=0.5), Indicate(end, color=YELLOW, scale_factor=1.4), run_time=0.9)
        self.play(Indicate(qs, color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Pumps(SpokenScene):
    def construct(self):
        MY = 0.3
        # membrane with a leak channel (x=-3) and the pump (x=2.2); gaps are exactly filled by the proteins
        chan = rrect(0.9, 0.7, BLUE, 0.35, 3, 0.1).move_to([-3.0, MY, 0])
        pump = rrect(1.7, 1.0, BLUE, 0.35, 3, 0.2).move_to([2.2, MY, 0])
        pieces = VGroup(
            rrect(2.85, 0.45, GREY, 0.4, 3, 0.1).move_to([(-6.3 - 3.45) / 2, MY, 0]),
            rrect(3.95, 0.45, GREY, 0.4, 3, 0.1).move_to([(-2.55 + 1.4) / 2, MY, 0]),
            rrect(3.3, 0.45, GREY, 0.4, 3, 0.1).move_to([(3.0 + 6.3) / 2, MY, 0]),
        )
        chan_l = T("channel", 22, BLUE).move_to([-5.2, -0.55, 0])
        pump_l = T("sodium-potassium pump", 22, BLUE).move_to([2.2, -0.65, 0])
        out_l = T("outside the axon", 24, GREY).move_to([-4.6, 3.2, 0])
        in_l = T("inside the axon", 24, GREY).move_to([-4.6, -3.2, 0])
        self.play(FadeIn(pieces), FadeIn(chan), FadeIn(pump), FadeIn(out_l), FadeIn(in_l), FadeIn(chan_l), FadeIn(pump_l), run_time=0.9)
        na = [dot("Na+", TEXT, 0.3, 20) for _ in range(3)]
        for i, n in enumerate(na):
            n.move_to([-3.7 + i * 0.7, 1.7, 0])
        ks = [dot("K+", GREY, 0.3, 20) for _ in range(2)]
        for i, k in enumerate(ks):
            k.move_to([-3.4 + i * 0.8, -1.9, 0])
        self.at("lets sodium in")
        self.play(*[FadeIn(n) for n in na], *[FadeIn(k) for k in ks], run_time=0.5)
        self.play(*[n.animate.move_to([-3.9 + i * 0.9, -1.0, 0]) for i, n in enumerate(na)], run_time=1.1)
        self.at("potassium out")
        self.play(*[k.animate.move_to([-3.4 + i * 0.8, 1.7, 0]) for i, k in enumerate(ks)], run_time=1.1)
        self.at("puts them back")
        atp = chip("ATP", YELLOW, 24).move_to([5.0, -1.6, 0])
        self.play(FadeIn(atp), pump.animate.set_fill(BLUE, 0.7), run_time=0.5)
        self.at("spends")
        self.play(Indicate(atp, color=YELLOW, scale_factor=1.25), run_time=0.7)
        self.at("three sodium out")
        self.play(*[n.animate.move_to([1.4 + i * 0.8, 2.2, 0]) for i, n in enumerate(na)], run_time=1.5)
        self.at("two potassium in")
        self.play(*[k.animate.move_to([1.8 + i * 0.8, 1.2, 0]) for i, k in enumerate(ks)], run_time=0.8)
        self.play(*[k.animate.move_to([1.8 + i * 0.8, -1.6, 0]) for i, k in enumerate(ks)], run_time=1.0)
        spent = T("1 ATP spent", 26, YELLOW).move_to([5.0, -2.4, 0])
        self.play(FadeOut(atp), pump.animate.set_fill(BLUE, 0.35), FadeIn(spent), run_time=0.5)
        self.at("never rest")
        self.play(Indicate(pump, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.play(Indicate(pump, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("cannot send")
        old = VGroup(pieces, chan, pump, chan_l, pump_l, out_l, in_l, spent, *na, *ks)
        self.play(FadeOut(old), run_time=0.6)
        soma = Circle(radius=0.8, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to([-5.4, 0, 0])
        tube = Rectangle(width=11.0, height=0.8, stroke_width=0, fill_color=BLUE, fill_opacity=0.35).move_to([0.5, 0, 0])
        atp2 = chip("ATP", YELLOW, 26).move_to([-3.6, 1.6, 0])
        a1 = arr([-3.0, 1.45, 0], [-0.6, 0.9, 0], YELLOW, 5)
        xx = cross(np.array([-1.8, 1.35, 0]), RED, 0.32)
        far = T("a metre away", 28, GREY).move_to([4.0, 1.6, 0])
        self.play(FadeIn(soma), GrowFromEdge(tube, LEFT), run_time=0.8)
        self.play(FadeIn(atp2), GrowArrow(a1), run_time=0.7)
        self.play(FadeIn(xx), FadeIn(far), run_time=0.5)
        self.at("locally")
        ms = VGroup(*[mito(x, 0, 1.0, 0.5) for x in (-2.8, -0.6, 1.6, 3.8)])
        ml = T("ATP made on the spot", 28, YELLOW).move_to([0.5, -1.4, 0])
        self.play(LaggedStart(*[GrowFromCenter(m) for m in ms], lag_ratio=0.25), FadeIn(ml), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Lactate(SpokenScene):
    def construct(self):
        glia, ax, gl, al = glia_axon()
        self.play(FadeIn(ax), FadeIn(al), run_time=0.6)
        self.play(FadeIn(glia), FadeIn(gl), run_time=0.8)
        cand = T("candidate supplier?", 30, YELLOW).move_to([3.0, 3.0, 0])
        self.at("candidate suppliers")
        self.play(FadeIn(cand, shift=DOWN * 0.1), run_time=0.5)
        glu = chip("glucose", TEXT, 26).move_to([-4.9, 1.75, 0])
        pyr = chip("pyruvate", ORANGE, 26).move_to([-1.9, 1.75, 0])
        lac = chip("lactate", ORANGE, 26).move_to([1.2, 1.75, 0])
        a1 = arr(glu.get_right() + RIGHT * 0.05, pyr.get_left(), GREY)
        a2 = DoubleArrow(pyr.get_right() + RIGHT * 0.05, lac.get_left() + LEFT * 0.05, color=ORANGE, buff=0,
                         stroke_width=5, tip_length=0.2)
        self.at("Glucose becomes")
        self.play(FadeIn(glu), run_time=0.4)
        self.play(GrowArrow(a1), FadeIn(pyr), run_time=0.7)
        self.at("become lactate")
        self.play(GrowArrow(a2) if False else GrowFromCenter(a2), FadeIn(lac), run_time=0.8)
        self.at("both directions")
        self.play(Indicate(a2, color=ORANGE, scale_factor=1.25), run_time=0.9)
        g = gate(GATE_X, GATE_Y)
        gl2 = T("MCT", 24, GREY).move_to([GATE_X + 1.25, GATE_Y, 0])
        self.at("transporters")
        self.play(FadeIn(g), FadeIn(gl2), run_time=0.6)
        c2 = ferry(self, lac.get_center())
        mt = mito(-2.2, -1.9, 2.2, 1.1)
        mtl = T("mitochondrion", 24, YELLOW).move_to([-2.2, -2.75, 0])
        self.at("turn it back")
        pyr2 = chip("pyruvate", ORANGE, 26).move_to([1.0, -0.95, 0])
        self.play(c2.animate.move_to([1.0, -0.95, 0]), run_time=0.6)
        self.play(ReplacementTransform(c2, pyr2), run_time=0.5)
        self.at("burn it")
        self.play(FadeIn(mt), FadeIn(mtl), run_time=0.5)
        self.play(pyr2.animate.move_to([-2.2, -1.9, 0]).scale(0.5), run_time=0.9)
        atp = chip("ATP", YELLOW, 26).move_to([-4.6, -1.0, 0])
        self.play(FadeOut(pyr2), FadeIn(atp, shift=LEFT * 0.4), run_time=0.6)
        self.at("portable fuel")
        self.play(Indicate(lac, color=ORANGE, scale_factor=1.25), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Astrocyte(SpokenScene):
    def construct(self):
        astro = Ellipse(width=4.9, height=3.0, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.14).move_to([-3.8, 1.9, 0])
        astro_l = T("astrocyte", 26, PURPLE).move_to([-3.8, 2.8, 0])
        neuron = Ellipse(width=4.9, height=3.0, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.14).move_to([3.8, 1.9, 0])
        neuron_l = T("neuron", 26, BLUE).move_to([3.8, 2.8, 0])
        self.play(FadeIn(astro), FadeIn(astro_l), run_time=0.8)
        glu = chip("glucose analogue", TEXT, 22).move_to([-4.3, 1.5, 0])
        lac = chip("lactate", ORANGE, 24).move_to([-2.2, 1.5, 0])
        a0 = arr([-4.0, 1.5, 0], [-3.6, 1.5, 0], GREY, 4, 0.15)
        self.at("take up more")
        self.play(FadeIn(glu, shift=RIGHT * 0.3), run_time=0.6)
        self.at("release lactate")
        self.play(FadeIn(lac), run_time=0.6)
        self.at("shuttle idea")
        self.play(FadeIn(neuron), FadeIn(neuron_l), run_time=0.7)
        syn = chip("active synapse", BLUE, 24).move_to([0, 2.7, 0])
        shuttle = arr([-1.6, 1.5, 0], [2.7, 1.5, 0], ORANGE, 6)
        lac_go = lac.copy()
        self.at("active synapse")
        self.play(FadeIn(syn), run_time=0.5)
        self.at("neuron burns it")
        self.play(GrowArrow(shuttle), lac_go.animate.move_to([3.8, 1.5, 0]), run_time=1.3)
        for_c = card("For", ["lactate gradient from astrocytes", "to neurons (mouse cortex)"], GREEN).move_to([-3.2, -1.1, 0])
        ag_c = card("Against", ["single neurons raise their own", "glycolysis; no lactate import seen"], RED).move_to([3.2, -1.1, 0])
        self.at("lactate gradient")
        self.play(FadeIn(for_c, shift=UP * 0.2), run_time=0.8)
        self.at("own glycolysis")
        self.play(FadeIn(ag_c, shift=UP * 0.2), run_time=0.8)
        dashed = DashedLine([-1.6, 1.5, 0], [2.7, 1.5, 0], color=ORANGE, stroke_width=6, dash_length=0.2)
        q = T("?", 52, YELLOW, weight=BOLD).move_to([0, 1.1, 0])
        hyp = T("a hypothesis with partial support", 32, YELLOW).move_to([0, -3.2, 0])
        self.at("partial support")
        self.play(FadeOut(shuttle), FadeIn(dashed), FadeOut(lac_go), run_time=0.7)
        self.play(FadeIn(q), FadeIn(hyp), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Oligo(SpokenScene):
    def construct(self):
        glia, ax, gl, al = glia_axon("oligodendrocyte (mice)")
        self.play(FadeIn(ax), FadeIn(al), FadeIn(glia), FadeIn(gl), run_time=0.9)
        mt = mito(-3.6, 1.9, 1.8, 0.95)
        mtl = T("respiration", 24, YELLOW).move_to([-3.6, 1.0, 0])
        gly = chip("glycolysis", ORANGE, 26).move_to([-0.7, 1.75, 0])
        g = gate(GATE_X, GATE_Y)
        gtl = T("MCT1", 24, GREY).move_to([GATE_X + 1.35, GATE_Y, 0])
        self.at("firmer")
        self.play(FadeIn(mt), FadeIn(mtl), FadeIn(gly), FadeIn(g), FadeIn(gtl), run_time=0.8)
        self.at("no longer respire")
        x = cross(np.array([-3.6, 1.9, 0]), RED, 0.55)
        self.play(FadeIn(x), mt.animate.set_stroke(opacity=0.35).set_fill(opacity=0.05), mtl.animate.set_opacity(0.4), run_time=0.7)
        self.at("glycolysis alone")
        self.play(Indicate(gly, color=ORANGE, scale_factor=1.2), run_time=0.8)
        ok = T("axons stay healthy (mice)", 30, GREEN).move_to([0.0, -1.2, 0])
        sub = T("Cox10 deleted in oligodendrocytes, adult CNS", 24, GREY).move_to([0.0, -1.85, 0])
        self.at("largely preserved")
        self.play(FadeIn(ok), FadeIn(sub), run_time=0.7)
        self.at("does not show it")
        self.play(Indicate(ok, color=YELLOW, scale_factor=1.04), run_time=0.9)
        self.at("the transporter")
        self.play(FadeOut(ok), FadeOut(sub), FadeOut(x), FadeOut(mt), FadeOut(mtl), run_time=0.6)
        self.at("motor neurons died")
        blocked = cross(np.array([GATE_X, GATE_Y, 0]), RED, 0.5)
        self.play(g.animate.set_color(RED), gtl.animate.set_color(RED), FadeIn(blocked), run_time=0.6)
        died = T("MCT1 lowered: motor neurons die (mice)", 28, RED).move_to([-0.5, -0.9, 0])
        self.play(FadeIn(died), run_time=0.6)
        sw = VGroup(*[Ellipse(width=0.9, height=1.0, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.3).move_to([x0, -1.9, 0])
                      for x0 in (-3.4, -1.9, -0.4)])
        swl = T("axon swellings (mice)", 26, RED).move_to([2.4, -1.9, 0])
        self.at("also swelled")
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sw], lag_ratio=0.3), FadeIn(swl), run_time=1.2)
        self.at("In culture")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        panel = rrect(11.4, 4.6, GREY, 0.08, 3, 0.25).move_to([0, 0.2, 0])
        ptitle = T("in culture: MCT1 inhibitor plus brief glucose removal", 26, GREY).move_to([0, 2.0, 0])
        stressed = chip("stressed neurons", BLUE, 26).move_to([-3.6, 0.0, 0])
        lc = chip("add lactate", ORANGE, 26).move_to([0.0, 0.9, 0])
        pa = arr([-1.8, 0.0, 0], [1.8, 0.0, 0], ORANGE, 6)
        prot = T("protected", 32, GREEN, weight=BOLD).move_to([3.7, 0.0, 0])
        self.play(FadeIn(panel), FadeIn(ptitle), FadeIn(stressed), run_time=0.8)
        self.at("lactate protected")
        self.play(FadeIn(lc, shift=DOWN * 0.2), GrowArrow(pa), run_time=0.7)
        self.play(FadeIn(prot), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        glia, ax, gl, al = glia_axon("oligodendrocyte (mice)")
        self.add(ax, al, glia, gl)
        glu = chip("glucose", TEXT, 26).move_to([-4.9, 1.75, 0])
        gly = chip("glycolysis", ORANGE, 26).move_to([-2.2, 1.75, 0])
        lac = chip("lactate or pyruvate", ORANGE, 26).move_to([1.5, 1.75, 0])
        a1 = arr(glu.get_right(), gly.get_left(), GREY)
        a2 = arr(gly.get_right(), lac.get_left(), ORANGE)
        g = gate(GATE_X, GATE_Y)
        gtl = T("MCT1", 24, GREY).move_to([GATE_X + 1.35, GATE_Y, 0])
        self.at("Oligodendrocytes take up glucose")
        self.play(FadeIn(glu), FadeIn(g), FadeIn(gtl), run_time=0.5)
        self.at("run glycolysis")
        self.play(GrowArrow(a1), FadeIn(gly), run_time=0.7)
        self.at("export lactate")
        self.play(GrowArrow(a2), FadeIn(lac), run_time=0.7)
        lax = ferry(self, lac.get_center(), "lactate or pyruvate", end_y=-0.95)
        lax.scale(0.9)
        mt = mito(-2.0, -1.9, 2.2, 1.1)
        mtl = T("mitochondrion", 24, YELLOW).move_to([-2.0, -2.75, 0])
        self.at("takes it in")
        self.play(lax.animate.move_to([0.4, -1.0, 0]), run_time=0.7)
        self.at("burns it")
        self.play(FadeIn(mt), FadeIn(mtl), lax.animate.move_to([-2.0, -1.9, 0]).scale(0.4), run_time=1.0)
        atp = chip("ATP", YELLOW, 26).move_to([-4.6, -1.0, 0])
        self.play(FadeOut(lax), FadeIn(atp), run_time=0.5)
        self.at("In mice")
        self.play(FadeOut(VGroup(glu, gly, lac, a1, a2, g, gtl, mt, mtl, atp, gl, al, glia, ax)), run_time=0.7)
        rule = T("In mice, myelinating glia appear to support axon metabolism.", 34, GREEN, font=TITLE_FONT)
        fit(rule, max_w=12.2)
        rule.move_to([0, 3.0, 0])
        gc = chip("myelinating glia", TEAL, 30).move_to([-3.9, 1.2, 0])
        axc = chip("axon", BLUE, 30).move_to([4.2, 1.2, 0])
        ar1 = DashedLine([-1.8, 1.2, 0], [3.2, 1.2, 0], color=ORANGE, stroke_width=6, dash_length=0.2)
        ar1.add_tip(tip_length=0.22)
        ar1l = T("lactate or pyruvate?", 26, ORANGE).move_to([0.7, 1.75, 0])
        self.play(Write(rule), FadeIn(gc), FadeIn(axc), run_time=1.2)
        self.play(Create(ar1), FadeIn(ar1l), run_time=0.7)
        unsettled = T("route and size of the contribution: unsettled", 26, YELLOW).move_to([0, 0.15, 0])
        self.at("still unsettled")
        self.play(FadeIn(unsettled), run_time=0.6)
        ac = chip("astrocyte", PURPLE, 30).move_to([-3.9, -1.2, 0])
        nc = chip("neuron", BLUE, 30).move_to([4.2, -1.2, 0])
        ar2 = DashedLine([-2.0, -1.2, 0], [3.2, -1.2, 0], color=ORANGE, stroke_width=6, dash_length=0.2)
        q2 = T("?", 48, YELLOW, weight=BOLD).move_to([0.6, -0.7, 0])
        deb = T("The astrocyte shuttle is still debated.", 32, PURPLE).move_to([0, -2.7, 0])
        self.at("astrocyte shuttle")
        self.play(FadeIn(ac), FadeIn(nc), FadeIn(ar2), FadeIn(q2), FadeIn(deb), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "In mice, myelinating glia appear to support axons."
