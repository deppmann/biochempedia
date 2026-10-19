"""One Stretch, Two Opposite Commands  (Biochemistrypedia neuroscience explainer, motor-units-reflexes)

Timed to the SPOKEN words with self.at("..."). A flat schematic only: two muscle blocks, a spindle,
a spinal cord cross-section (circle with a dashed midline, dorsal at the top, ventral at the bottom)
and labelled neurons. No body, no leg, no drawn limb. Every neuron sits on ONE half of the cord (the
half on the same side as the stretched muscle); the other half is labelled and left empty.

COLOR MAP (one color per concept, whole video)
  BLUE   = neurons (Ia afferent, alpha motor neurons, their axons)
  GREEN  = excitation (excitatory synapse, the muscle that is excited)
  RED    = inhibition (inhibitory interneuron, inhibitory synapse, the muscle that relaxes)
  YELLOW = the stretch and the spikes it sends
  TEAL   = the muscle spindle (the sensor)
  GREY   = muscles at rest, the cord, structure, the crossed-extensor reflex (not part of the circuit)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

C = np.array([3.2, 0.0, 0.0])   # cord centre
R = 2.9
AY, BY = 1.9, -2.55             # muscle A (stretched) and B (antagonist) centre y
AX = -4.7


def P(x, y):
    return np.array([x, y, 0.0])


def poly(pts, color=BLUE, w=5, dashed=False):
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_as_corners([P(*p) for p in pts])
    return m


def inhib_end(a, b, color=RED, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.24, b - perp * 0.24, color=color, stroke_width=w + 1))


def exc_arrow(a, b, color=GREEN, w=6):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=20)


def num(text, x, y, color):
    return T(text, 28, color, weight=BOLD).move_to(P(x, y))


class Rig:
    """Everything that stays the same in every scene; scenes add/fade the parts they need."""

    def __init__(self):
        # muscles
        self.mA = Rectangle(width=2.8, height=0.95, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                            fill_opacity=0.22).move_to(P(AX, AY))
        self.mB = Rectangle(width=2.8, height=1.0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                            fill_opacity=0.22).move_to(P(AX, BY))
        self.fibres = VGroup(*[Line(P(-5.85, AY + dy), P(-3.55, AY + dy), color=GREY, stroke_width=2).set_opacity(0.7)
                               for dy in (-0.3, 0.3)])
        self.labA = T("muscle", 22, GREY).move_to(P(-5.5, AY))
        self.labB = T("antagonist", 22, GREY).move_to(P(AX, BY))
        # spindle: parallel to the ordinary fibres
        self.spindle = RoundedRectangle(corner_radius=0.17, width=0.8, height=0.34, stroke_color=TEAL,
                                        stroke_width=3.5, fill_color=TEAL, fill_opacity=0.35).move_to(P(-4.2, AY))
        # cord cross-section
        self.cord = Circle(radius=R, stroke_color=GREY, stroke_width=3.5, fill_color=GREY, fill_opacity=0.10).move_to(C)
        self.mid = DashedLine(C + UP * R, C + DOWN * R, color=GREY, stroke_width=2.5, dash_length=0.14).set_opacity(0.7)
        self.dors = T("dorsal", 22, GREY).move_to(P(3.2, 2.45))
        self.vent = T("ventral", 22, GREY).move_to(P(3.2, -2.2))
        self.same = T("same side", 24, TEXT).move_to(P(1.15, -2.95))
        self.other = T("other side", 24, GREY).move_to(P(5.2, -2.95))
        # neurons
        self.aff = poly([(-3.8, AY), (1.7, AY), (1.7, 0.8)], BLUE, 5)
        self.br1 = poly([(1.7, 0.8), (1.08, -0.38)], BLUE, 5)
        self.br2 = poly([(1.7, 0.8), (2.38, 0.22)], BLUE, 5)
        self.mnA = Circle(radius=0.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to(P(1.0, -0.7))
        self.axA = poly([(0.7, -0.7), (-3.6, -0.7), (-3.6, AY - 0.475)], BLUE, 5)
        self.mnB = Circle(radius=0.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to(P(1.9, -1.8))
        self.axB = poly([(1.6, -1.8), (-4.0, -1.8), (-4.0, BY + 0.5)], BLUE, 5)
        self.inn = Circle(radius=0.28, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.25).move_to(P(2.55, 0.0))
        self.inax = poly([(2.5, -0.28), (2.0, -1.5)], RED, 5)
        self.inend = inhib_end(P(2.1, -1.2), P(2.0, -1.5), RED, 5)
        # synapse ends
        self.syn1 = exc_arrow(P(1.2, -0.12), P(1.08, -0.4))
        self.syn2 = exc_arrow(P(2.2, 0.35), P(2.33, 0.25))
        # labels
        self.lAff = T("Ia afferent", 22, BLUE).move_to(P(-1.5, AY + 0.35))
        self.lDR = T("dorsal root", 22, GREY).move_to(P(-0.55, AY - 0.4))
        self.lMN = T("motor neuron", 22, BLUE).move_to(P(-1.9, -0.4))
        self.lMNB = T("motor neuron", 22, BLUE).move_to(P(-1.9, -1.5))

    def base(self):
        return VGroup(self.cord, self.mid, self.dors, self.vent, self.same, self.other,
                      self.mA, self.fibres, self.labA, self.mB, self.labB, self.spindle)

    def circuit(self):
        return VGroup(self.aff, self.br1, self.br2, self.mnA, self.axA, self.mnB, self.axB, self.inn, self.inax, self.inend,
                      self.syn1, self.syn2)


def slot(text, color, which):
    c = chip(text, color, size=22, pad=0.16)
    c.move_to(P(-4.4 if which == 0 else -1.2, 3.05))
    return c


def spike(path, color=YELLOW):
    d = Dot(radius=0.14, color=color)
    d.move_to(path.get_start())
    return d


def run_spike(scene, dot, path, t):
    scene.play(FadeIn(dot, run_time=0.1))
    scene.play(MoveAlongPath(dot, path), run_time=t, rate_func=linear)


class S00Title(TitleCard):
    LESSON = "Motor Units, Reflexes and Locomotion"
    TITLE = "One Stretch, Two Opposite Commands"


class S01Puzzle(SpokenScene):
    def construct(self):
        r = Rig()
        self.add(r.base())
        tap = slot("tendon tap", YELLOW, 0)
        # the unknown path: sensor -> ? -> motor neuron -> muscle
        q1 = chip("?", YELLOW, size=34, pad=0.2).move_to(P(1.7, 1.0))
        qa = DashedLine(P(-3.8, AY), P(1.7, 1.4), color=BLUE, stroke_width=4, dash_length=0.15)
        qb = DashedLine(P(1.7, 0.6), P(1.1, -0.38), color=BLUE, stroke_width=4, dash_length=0.15)
        mn = Circle(radius=0.3, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to(P(1.0, -0.7))
        qc = DashedVMobject(r.axA.copy(), num_dashes=40)
        sensor = T("sensor", 22, TEAL).move_to(P(-4.45, AY - 0.8))
        mnl = T("motor neuron", 22, BLUE).move_to(P(-1.9, -0.4))
        self.at("Tap the tendon")
        self.play(FadeIn(tap, shift=DOWN * 0.1), run_time=0.5)
        self.at("your leg kicks")
        self.play(Indicate(r.mA, color=YELLOW, scale_factor=1.06), run_time=0.7)
        self.at("only one synapse")
        self.play(Create(qa), FadeIn(q1), Create(qb), FadeIn(mn), Create(qc), FadeIn(mnl), run_time=1.4)
        self.at("sensor")
        self.play(FadeIn(sensor), Indicate(r.spindle, color=TEAL, scale_factor=1.3), run_time=0.6)
        self.at("Why only one")
        self.play(Indicate(q1, color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.at("other side of the joint")
        self.play(Indicate(r.mB, color=RED, scale_factor=1.06), run_time=0.7)
        self.finish()


class S02Spindle(SpokenScene):
    def construct(self):
        r = Rig()
        self.add(r.base())
        tap = slot("brief stretch", YELLOW, 0)
        # scene one's leftovers, rebuilt in place so they can be replaced
        self.add(tap)
        stretch = DoubleArrow(P(-6.05, AY + 0.72), P(-3.35, AY + 0.72), color=YELLOW, stroke_width=5, tip_length=0.2, buff=0)
        self.at("muscle spindle")
        self.play(Indicate(r.spindle, color=TEAL, scale_factor=1.3), FadeIn(T("muscle spindle", 22, TEAL).move_to(P(-4.1, AY - 0.8))), run_time=0.7)
        self.at("parallel to")
        self.play(Indicate(r.fibres, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("tendon tap")
        self.play(FadeIn(stretch), run_time=0.5)
        self.at("stretches the spindle")
        self.play(r.spindle.animate.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW), run_time=0.4)
        self.at("afferents")
        self.play(Create(r.aff), FadeIn(r.lAff), run_time=0.8)
        d = spike(r.aff)
        self.at("respond")
        run_spike(self, d, r.aff, 1.3)
        self.at("dorsal root")
        self.play(FadeIn(r.lDR), run_time=0.4)
        self.at("they branch")
        self.play(Create(r.br1), Create(r.br2), run_time=0.8)
        self.finish()


def build_state(scene, r, upto):
    """Rebuild the circuit as it stood at the end of the previous scene."""
    parts = [r.aff, r.lAff, r.lDR, r.br1, r.br2]
    if upto >= 3:
        parts += [r.mnA, r.axA, r.syn1]
    if upto >= 4:
        parts += [r.inn, r.inax, r.inend, r.syn2, r.mnB, r.axB]
    scene.add(*parts)


class S03Mono(SpokenScene):
    def construct(self):
        r = Rig()
        self.add(r.base())
        r.spindle.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW)
        self.add(r.aff, r.lAff, r.lDR, r.br1, r.br2)
        mono = slot("monosynaptic", GREEN, 0)
        one = num("1", 0.7, 0.05, GREEN)
        self.at("One branch excites")
        self.play(Indicate(r.br1, color=GREEN, scale_factor=1.0), run_time=0.7)
        self.play(FadeIn(r.mnA), FadeIn(r.syn1), run_time=0.6)
        d = spike(r.aff)
        path = poly([(-3.8, AY), (1.7, AY), (1.7, 0.8), (1.08, -0.38)])
        self.at("directly")
        run_spike(self, d, path, 1.2)
        self.play(FadeOut(d), FadeIn(one), r.mnA.animate.set_fill(YELLOW, opacity=0.6), run_time=0.4)
        self.at("one synapse")
        self.play(FadeIn(mono), Indicate(one, color=GREEN, scale_factor=1.5), run_time=0.7)
        self.at("alpha motor neurons")
        self.play(FadeIn(r.lMN), run_time=0.4)
        self.at("ventral horn")
        self.play(Indicate(r.mnA, color=BLUE, scale_factor=1.3), run_time=0.7)
        self.at("ventral root")
        self.play(Create(r.axA), run_time=0.8)
        self.at("The muscle contracts")
        d2 = spike(r.axA)
        run_spike(self, d2, r.axA, 1.0)
        shrunk = Rectangle(width=2.5, height=1.1, stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN,
                           fill_opacity=0.35).move_to(P(AX, AY))
        self.play(FadeOut(d2), Transform(r.mA, shrunk), Transform(r.labA, T("contracts", 22, GREEN).move_to(P(-5.3, AY))),
                  run_time=0.6)
        self.at("Only this branch")
        self.play(Indicate(mono, color=GREEN, scale_factor=1.15), run_time=0.7)
        self.at("as a whole")
        self.play(Indicate(r.br2, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.finish()


class S04Disyn(SpokenScene):
    def construct(self):
        r = Rig()
        self.add(r.base())
        r.spindle.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW)
        r.mA.become(Rectangle(width=2.5, height=1.1, stroke_color=GREEN, stroke_width=3.5, fill_color=GREEN,
                              fill_opacity=0.35).move_to(P(AX, AY)))
        r.labA.become(T("contracts", 22, GREEN).move_to(P(-5.3, AY)))
        r.mnA.set_fill(YELLOW, opacity=0.6)
        mono = slot("monosynaptic", GREEN, 0)
        self.add(r.aff, r.lAff, r.lDR, r.br1, r.br2, r.mnA, r.axA, r.syn1, mono, r.lMN, num("1", 0.7, 0.05, GREEN))
        dis = slot("inhibitory interneuron", RED, 1)
        o1 = num("1", 2.22, 0.78, GREEN)
        o2 = num("2", 2.6, -1.1, RED)
        # fade the first-case lamps so the old answer does not linger under the new case
        self.at("other branch")
        self.play(r.mA.animate.set_stroke(GREY).set_fill(GREY, opacity=0.22), Transform(r.labA, T("muscle", 22, GREY).move_to(P(-5.35, AY))),
                  r.mnA.animate.set_fill(BLUE, opacity=0.25), Indicate(r.br2, color=TEXT, scale_factor=1.0), FadeIn(r.inn), FadeIn(r.syn2), run_time=0.6)
        d = spike(r.aff)
        path = poly([(-3.8, AY), (1.7, AY), (1.7, 0.8), (2.38, 0.22)])
        run_spike(self, d, path, 0.7)
        self.play(FadeOut(d), FadeIn(o1), r.inn.animate.set_fill(YELLOW, opacity=0.6), run_time=0.4)
        self.at("inhibitory interneuron")
        self.play(FadeIn(dis), run_time=0.4)
        self.at("same side of the cord")
        self.play(Indicate(r.same, color=YELLOW, scale_factor=1.25), run_time=0.7)
        self.at("inhibits the motor neurons")
        self.play(Create(r.inax), FadeIn(r.inend), FadeIn(r.mnB), run_time=0.8)
        d2 = spike(r.inax)
        run_spike(self, d2, r.inax, 0.9)
        self.play(FadeOut(d2), FadeIn(o2), r.mnB.animate.set_fill(RED, opacity=0.4), run_time=0.4)
        self.at("antagonist")
        self.play(Create(r.axB), FadeIn(r.lMNB), run_time=0.7)
        self.at("two synapses")
        self.play(Transform(dis, slot("disynaptic", RED, 1)), Indicate(o2, color=RED, scale_factor=1.5), run_time=0.7)
        self.at("It stays")
        self.play(Indicate(r.same, color=YELLOW, scale_factor=1.25), Indicate(r.other, color=GREY, scale_factor=1.15), run_time=0.8)
        self.finish()


def full_circuit(scene, r):
    scene.add(r.base())
    scene.add(r.aff, r.lAff, r.lDR, r.br1, r.br2, r.mnA, r.axA, r.syn1, r.inn, r.inax, r.inend, r.syn2, r.mnB, r.axB, r.lMN, r.lMNB)
    scene.add(slot("monosynaptic", GREEN, 0), slot("disynaptic", RED, 1))
    scene.add(num("1", 0.7, 0.05, GREEN), num("1", 2.22, 0.78, GREEN), num("2", 2.6, -1.1, RED))


class S05Pair(SpokenScene):
    def construct(self):
        r = Rig()
        full_circuit(self, r)
        r.spindle.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW)
        d1 = spike(r.aff)
        p1 = poly([(-3.8, AY), (1.7, AY), (1.7, 0.8), (1.08, -0.38)])
        p2 = poly([(-3.8, AY), (1.7, AY), (1.7, 0.8), (2.38, 0.22)])
        self.at("Sherrington found")
        d2 = spike(r.aff)
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.1)
        self.play(MoveAlongPath(d1, p1), MoveAlongPath(d2, p2), run_time=1.3, rate_func=linear)
        self.play(FadeOut(d1), FadeOut(d2), r.mnA.animate.set_fill(YELLOW, opacity=0.6), r.inn.animate.set_fill(YELLOW, opacity=0.6), run_time=0.3)
        self.play(r.mA.animate.set_stroke(GREEN).set_fill(GREEN, opacity=0.35), run_time=0.4)
        relax = VGroup(T("antagonist", 22, RED), T("relaxes", 22, RED)).arrange(DOWN, buff=0.05).move_to(P(AX, BY))
        self.at("the muscle that opposes")
        self.play(r.mB.animate.set_stroke(RED).set_fill(RED, opacity=0.22), Transform(r.labB, relax), run_time=0.8)
        self.at("reciprocal innervation")
        pair = T("reciprocal innervation", 22, TEXT).move_to(P(-1.75, 0.6))
        self.play(FadeIn(pair), run_time=0.6)
        veil = Rectangle(width=14.4, height=8.1, stroke_width=0, fill_color=BG, fill_opacity=0.72)
        cross = DashedLine(P(3.55, 1.5), P(4.65, 0.5), color=GREY, stroke_width=5, dash_length=0.16)
        cross.add_tip(tip_length=0.22)
        clab = VGroup(T("opposite leg:", 22, TEXT), T("extensor contracts", 22, TEXT)).arrange(DOWN, buff=0.06)
        box = SurroundingRectangle(clab, color=GREY, buff=0.15, corner_radius=0.1)
        clab = VGroup(box, clab).move_to(P(4.65, -0.05))
        self.at("is the one that crosses")
        self.play(FadeIn(veil), run_time=0.5)
        self.add(cross, clab)
        self.play(Create(cross), FadeIn(clab), run_time=0.9)
        self.at("painful stimulus")
        self.play(Indicate(cross, color=TEXT, scale_factor=1.1), run_time=0.7)
        self.at("polysynaptic")
        self.play(Indicate(clab, color=TEXT, scale_factor=1.1), run_time=0.7)
        self.at("reflex is local")
        self.play(FadeOut(veil), FadeOut(clab), FadeOut(cross), run_time=0.6)
        self.play(Indicate(r.same, color=YELLOW, scale_factor=1.25), run_time=0.7)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        r = Rig()
        self.add(r.base())
        r.spindle.set_fill(YELLOW, opacity=0.6).set_stroke(YELLOW)
        r.mA.set_stroke(GREEN).set_fill(GREEN, opacity=0.35)
        r.mB.set_stroke(RED).set_fill(RED, opacity=0.22)
        r.labB.become(VGroup(T("antagonist", 22, RED), T("relaxes", 22, RED)).arrange(DOWN, buff=0.05).move_to(P(AX, BY)))
        r.mnA.set_fill(YELLOW, opacity=0.6)
        self.add(r.aff, r.br1, r.br2, r.mnA, r.axA, r.syn1, r.inn, r.inax, r.inend, r.syn2, r.mnB, r.axB, r.lAff)
        self.add(slot("monosynaptic", GREEN, 0), slot("disynaptic", RED, 1))
        g1 = VGroup(T("excites the same muscle", 22, GREEN), T("1 synapse", 26, GREEN, weight=BOLD)).arrange(DOWN, buff=0.05).move_to(P(-1.55, 0.4))
        g2 = VGroup(T("inhibits the antagonist", 22, RED), T("2 synapses", 26, RED, weight=BOLD)).arrange(DOWN, buff=0.05).move_to(P(-1.5, -1.25))
        self.at("one stretch")
        self.play(Indicate(r.mA, color=YELLOW, scale_factor=1.06), run_time=0.7)
        self.at("One synapse")
        self.play(FadeIn(g1), Indicate(r.syn1, color=GREEN, scale_factor=1.6), run_time=0.8)
        self.at("Two synapses")
        self.play(FadeIn(g2), Indicate(r.inend, color=RED, scale_factor=1.4), run_time=0.8)
        self.at("on the same side")
        self.play(Indicate(r.same, color=YELLOW, scale_factor=1.25), run_time=0.7)
        self.at("The rule to keep")
        self.play(Indicate(g1, color=GREEN, scale_factor=1.08), Indicate(g2, color=RED, scale_factor=1.08), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "A stretch excites the same muscle and inhibits its antagonist."
