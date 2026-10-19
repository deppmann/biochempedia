"""Nervous control: a reflex is a route  (Biochemistrypedia organismal biology explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = the nerve signal (the impulse dot that travels)
  BLUE   = input side: stimulus, receptor, sensory neuron
  GREEN  = output side: motor neuron, effector muscle
  PURPLE = interneurons
  ORANGE = chemical released at a synapse; the one-synapse node
  RED    = inhibition, the unknown route
  GREY   = outlines, the central nervous system box, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=6, tip=0.24):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=14)


def path(points, color, w=6, tip=0.24, head=True):
    """A bent line through points; the last segment carries an arrowhead."""
    pts = [np.array([p[0], p[1], 0.0]) for p in points]
    g = VGroup()
    for i in range(len(pts) - 2):
        g.add(Line(pts[i], pts[i + 1], color=color, stroke_width=w))
    if head:
        g.add(arr(pts[-2], pts[-1], color, w, tip))
    else:
        g.add(Line(pts[-2], pts[-1], color=color, stroke_width=w))
    g.pts = pts
    return g


def stop_bar(a, b, color=RED, w=6):
    a, b = np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0])
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.3, b - perp * 0.3, color=color, stroke_width=w + 2))


def run_dot(points, color=YELLOW, rt=2.0, r=0.17):
    """Animation list: a dot that follows a polyline."""
    pts = [np.array([p[0], p[1], 0.0]) for p in points]
    dot = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to(pts[0])
    pm = VMobject()
    pm.set_points_as_corners(pts)
    return dot, MoveAlongPath(dot, pm, run_time=rt, rate_func=linear)


class S00Title(TitleCard):
    LESSON = "Nervous control: a first look"
    TITLE = "A reflex is a route"


# ---------------------------------------------------------------------------------------------
class S01Speed(SpokenScene):
    """Helmholtz hook: a nerve signal has a finite speed; then the question of the route."""

    def construct(self):
        Y = 0.9
        head = T("1850 · isolated frog nerve and calf muscle", 32, font=TITLE_FONT).to_edge(UP, buff=0.5)
        shock = chip("electric shock", BLUE, 34).move_to([-4.7, Y, 0])
        muscle = chip("muscle", GREEN, 34).move_to([4.9, Y, 0])
        bar = RoundedRectangle(corner_radius=0.16, width=5.4, height=0.4, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.4).move_to([0.1, Y, 0])
        nlab = T("frog nerve", 28, GREY).next_to(bar, UP, buff=0.35)
        self.at("1850")
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(shock), FadeIn(muscle), GrowFromCenter(bar), FadeIn(nlab),
                  run_time=1.2)
        self.at("timed a nerve signal")
        dot, anim = run_dot([[-2.5, Y], [2.7, Y]], rt=2.4)
        self.add(dot)
        self.play(anim)
        self.remove(dot)
        self.play(Indicate(muscle, color=GREEN, scale_factor=1.12), run_time=0.5)
        self.at("a few tens")
        speed = VGroup(M("a few tens of metres per second", 38, YELLOW),
                       T("frog nerve, room temperature", 28, GREY)).arrange(DOWN, buff=0.22).move_to([0, -0.7, 0])
        self.play(FadeIn(speed, shift=UP * 0.1), run_time=0.7)
        self.at("motorway")
        car = chip("about the speed of a car on a motorway", GREY, 32).move_to([0, -2.6, 0])
        self.play(FadeIn(car, shift=UP * 0.1), run_time=0.6)
        self.at("what route")
        sense = chip("sense organ", BLUE, 34).move_to(shock)
        q = VGroup(*[chip("?", RED, 40, pad=0.3) for _ in range(3)]).arrange(RIGHT, buff=0.8).move_to([0.1, Y, 0])
        self.play(FadeOut(speed), FadeOut(car), FadeOut(nlab), FadeOut(head), run_time=0.5)
        self.play(ReplacementTransform(shock, sense), ReplacementTransform(bar, q), run_time=0.9)
        route = T("what route?", 40, RED).move_to([0, -0.9, 0])
        self.play(FadeIn(route, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Neuron(SpokenScene):
    """A motor neuron as labelled blocks; the impulse; the chemical gap."""

    def construct(self):
        cy = 0.1
        body = Circle(radius=1.1, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.25).move_to([-4.2, cy, 0])
        dend = VGroup(*[Line([-5.05, cy + dy * 0.45, 0], [-6.2, cy + dy, 0], color=GREEN, stroke_width=7)
                        for dy in (1.8, 0.0, -1.8)])
        axon = RoundedRectangle(corner_radius=0.1, width=6.6, height=0.38, stroke_color=GREEN, stroke_width=4,
                                fill_color=GREEN, fill_opacity=0.25).move_to([-0.8, cy, 0])
        term = VGroup(*[Line([2.5, cy, 0], [3.7, cy + dy, 0], color=GREEN, stroke_width=7) for dy in (1.1, 0.0, -1.1)])
        bulbs = VGroup(*[Circle(radius=0.2, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([3.8, cy + dy, 0])
                         for dy in (1.1, 0.0, -1.1)])
        nxt = RoundedRectangle(corner_radius=0.15, width=1.5, height=3.8, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.2).move_to([5.55, cy, 0])
        nxt_l = T("next cell", 26, GREY).move_to([5.55, cy - 1.45, 0])
        l_dend = T("dendrites", 28, GREEN).move_to([-5.5, cy + 2.55, 0])
        l_body = T("cell body", 28, GREEN).move_to([-4.2, cy - 1.9, 0])
        l_axon = T("axon", 28, GREEN).move_to([-0.8, cy + 0.7, 0])
        l_term = T("axon terminals", 28, GREEN).move_to([2.0, cy + 2.2, 0])
        title = T("a typical vertebrate motor neuron", 32, font=TITLE_FONT).to_edge(UP, buff=0.5)
        ghost = VGroup(dend.copy(), body.copy(), axon.copy(), term.copy(), bulbs.copy(), nxt.copy())
        ghost.set_stroke(GREY, opacity=0.35).set_fill(GREY, opacity=0.06)

        self.add(ghost)
        self.at("neurons")
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.6)
        self.at("dendrites")
        self.play(Create(dend), FadeIn(l_dend), run_time=0.7)
        self.at("cell body")
        self.play(GrowFromCenter(body), FadeIn(l_body), run_time=0.7)
        self.at("long axon")
        self.play(GrowFromEdge(axon, LEFT), FadeIn(l_axon), run_time=0.9)
        self.at("axon terminals")
        self.play(Create(term), FadeIn(bulbs), FadeIn(l_term), FadeIn(nxt_l), run_time=0.8)
        self.at("is an impulse")
        dot, anim = run_dot([[-3.1, cy], [2.5, cy]], rt=1.6)
        self.add(dot)
        self.play(anim)
        self.at("all or none")
        full = chip("full size, or not at all", YELLOW, 28).move_to([-0.8, cy - 1.9, 0])
        self.play(FadeIn(full, shift=UP * 0.1), run_time=0.5)
        self.at("releases a chemical")
        self.remove(dot)
        ch = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to([4.05, cy + dy, 0])
                      for dy in (1.1, 0.0, -1.1)])
        self.play(FadeIn(ch), run_time=0.3)
        self.play(*[c.animate.move_to([4.75, cy + (0.7 - 0.7 * i), 0]) for i, c in enumerate(ch)], run_time=1.2)
        gl = T("chemical crosses the gap", 26, ORANGE).move_to([4.0, cy - 2.55, 0])
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
BOX_C = np.array([0.0, -0.6, 0.0])
IN_P = [(-4.6, 1.55), (-4.6, -0.6), (-2.55, -0.6)]
OUT_P = [(2.55, -0.6), (4.6, -0.6), (4.6, 1.55)]


def arc_base(rec="receptor", eff="effector", rec_col=BLUE, eff_col=GREEN):
    rec_c = chip(rec, rec_col, 26).move_to([-4.6, 2.3, 0])
    eff_c = chip(eff, eff_col, 26).move_to([4.6, 2.3, 0])
    cns = RoundedRectangle(corner_radius=0.2, width=5.1, height=2.6, stroke_color=GREY, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.12).move_to(BOX_C)
    cns_l = T("central nervous system", 26, GREY).move_to([0, -2.55, 0])
    sens = path(IN_P, BLUE)
    mot = path(OUT_P, GREEN)
    return rec_c, eff_c, cns, cns_l, sens, mot


class S03Arc(SpokenScene):
    """The five parts of the reflex arc, then the signal runs the whole arc."""

    def construct(self):
        rec_c, eff_c, cns, cns_l, sens, mot = arc_base()
        sens_l = T("sensory neuron", 26, BLUE).move_to([-3.15, 0.95, 0])
        mot_l = T("motor neuron", 26, GREEN).move_to([3.15, 0.95, 0])
        ic = T("integrating centre", 28, GREY).move_to([0, 0.1, 0])
        stim = chip("stimulus", BLUE, 26).move_to(rec_c)
        resp = chip("response", GREEN, 26).move_to(eff_c)
        self.add(cns, cns_l)
        self.play(FadeIn(stim), run_time=0.4)
        self.at("automatic response")
        self.play(FadeIn(resp, shift=DOWN * 0.1), run_time=0.5)
        self.at("receptor")
        self.play(ReplacementTransform(stim, rec_c), run_time=0.6)
        self.at("sensory neuron")
        self.play(Create(sens), FadeIn(sens_l), run_time=0.9)
        self.at("integrating center")
        self.play(FadeIn(ic), run_time=0.6)
        self.at("motor neuron")
        self.play(Create(mot), FadeIn(mot_l), run_time=0.9)
        self.at("the effector")
        self.play(ReplacementTransform(resp, eff_c), run_time=0.6)
        self.at("a muscle or a gland")
        dot, anim = run_dot([IN_P[0], IN_P[1], IN_P[2], OUT_P[0], OUT_P[1], OUT_P[2]], rt=3.2)
        self.add(dot)
        self.play(anim)
        self.play(Indicate(eff_c, color=GREEN, scale_factor=1.12), run_time=0.6)
        self.remove(dot)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Knee(SpokenScene):
    """Knee jerk: sensory fibre synapses directly on the motor neuron."""

    def construct(self):
        rec_c, eff_c, cns, cns_l, sens, mot = arc_base()
        sens_l = T("sensory neuron", 26, BLUE).move_to([-3.15, 0.95, 0])
        mot_l = T("motor neuron", 26, GREEN).move_to([3.15, 0.95, 0])
        self.add(cns, cns_l, rec_c, eff_c, sens, mot, sens_l, mot_l)
        cns_t = T("spinal cord", 28, GREY).move_to([0, 0.3, 0])
        self.add(cns_t)
        tap = chip("tap on the tendon", BLUE, 26).move_to([0, 3.1, 0])
        self.at("knee jerk")
        self.play(FadeIn(tap, shift=DOWN * 0.1), run_time=0.6)
        self.at("stretches the quadriceps")
        eff2 = chip("quadriceps muscle", GREEN, 26).move_to(eff_c)
        stretch = T("stretched", 26, GREEN).next_to(eff2, UP, buff=0.2)
        ta = arr(tap.get_right() + RIGHT * 0.05, eff2.get_top() + LEFT * 1.0 + UP * 0.05, BLUE, 5, 0.2)
        self.play(ReplacementTransform(eff_c, eff2), FadeIn(stretch), Create(ta), run_time=0.8)
        self.at("stretch receptors")
        rec2 = chip("muscle spindles", BLUE, 26).move_to(rec_c)
        conn = DashedLine(rec2.get_right() + RIGHT * 0.05, eff2.get_left() + LEFT * 0.05, color=GREY, stroke_width=3)
        conn_l = T("spindles lie in the muscle", 22, GREY).move_to([0, 1.95, 0])
        self.play(ReplacementTransform(rec_c, rec2), FadeOut(tap), FadeOut(ta), Create(conn), FadeIn(conn_l), run_time=0.7)
        self.play(Indicate(rec2, color=YELLOW, scale_factor=1.1), run_time=0.5)
        self.at("sensory fibers enter")
        dot, anim = run_dot([IN_P[0], IN_P[1], IN_P[2], (-0.35, -0.6)], rt=1.8)
        self.add(dot)
        self.play(anim)
        node = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.5).move_to([0, -0.6, 0])
        link_in = Line([-2.55, -0.6, 0], [-0.3, -0.6, 0], color=BLUE, stroke_width=6)
        link_out = Line([0.3, -0.6, 0], [2.55, -0.6, 0], color=GREEN, stroke_width=6)
        self.play(FadeIn(node), Create(link_in), Create(link_out), run_time=0.6)
        self.at("synapse directly")
        syn_l = T("one synapse", 26, ORANGE).move_to([0, 0.15, 0])
        self.play(Indicate(node, color=ORANGE, scale_factor=1.3), FadeOut(cns_t), FadeIn(syn_l), run_time=0.8)
        self.at("those neurons")
        self.remove(dot)
        dot2, anim2 = run_dot([(0.3, -0.6), OUT_P[0], OUT_P[1], OUT_P[2]], rt=1.7)
        self.add(dot2)
        self.play(anim2)
        self.remove(dot2)
        kick = T("leg kicks", 26, GREEN).next_to(eff2, UP, buff=0.2)
        self.play(Indicate(eff2, color=GREEN, scale_factor=1.12), ReplacementTransform(stretch, kick), run_time=0.7)
        self.at("one synapse in the cord")
        mono = chip("monosynaptic", ORANGE, 28).move_to([0, 1.4, 0])
        self.play(FadeOut(conn_l), FadeIn(mono, shift=DOWN * 0.1), run_time=0.6)
        ham = chip("hamstring", PURPLE, 22).move_to([4.6, -2.4, 0])
        inn = chip("interneuron", PURPLE, 22).move_to([0.2, -1.45, 0])
        br = path([(-1.3, -0.6), (-1.3, -1.45), (-0.8, -1.45)], BLUE, w=4, tip=0.16)
        inh = VGroup(Line([1.25, -1.45, 0], [4.6, -1.45, 0], color=RED, stroke_width=4),
                     stop_bar([4.6, -1.45], [4.6, -1.95], w=4))
        faint = VGroup(inn, br, inh, ham)
        faint.set_opacity(0.55)
        self.play(FadeIn(faint), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Withdraw(SpokenScene):
    """Withdrawal reflex: interneurons from the start; flexors excited, extensors inhibited."""

    def construct(self):
        rec_c, eff_c, cns, cns_l, sens, mot = arc_base()
        sens_l = T("sensory neuron", 26, BLUE).move_to([-3.15, 0.95, 0])
        mot_l = T("motor neuron", 26, GREEN).move_to([3.15, 0.95, 0])
        self.add(cns, cns_l, rec_c, eff_c, sens, mot, sens_l, mot_l)
        cns_t = T("spinal cord", 28, GREY).move_to([0, 0.3, 0])
        self.add(cns_t)
        self.at("withdrawal reflex")
        rec2 = chip("pain receptors", BLUE, 26).move_to(rec_c)
        self.play(ReplacementTransform(rec_c, rec2), run_time=0.7)
        self.play(Indicate(rec2, color=YELLOW, scale_factor=1.1), run_time=0.5)
        self.at("interneurons from the start")
        up = chip("interneurons", PURPLE, 26).move_to([0.1, 0.0, 0])
        lo = chip("interneurons", PURPLE, 26).move_to([0.1, -1.3, 0])
        self.play(FadeOut(cns_t), FadeIn(up, shift=UP * 0.1), FadeIn(lo, shift=UP * 0.1), run_time=0.8)
        self.at("pain receptors excite")
        dot, anim = run_dot([IN_P[0], IN_P[1], IN_P[2]], rt=1.5)
        self.add(dot)
        self.play(anim)
        b_up = path([(-2.55, -0.6), (-1.5, -0.6), (-1.5, 0.0), (-1.2, 0.0)], BLUE, w=5, tip=0.2)
        b_lo = path([(-1.5, -0.6), (-1.5, -1.3), (-1.2, -1.3)], BLUE, w=5, tip=0.2)
        self.at("these excite")
        self.play(Create(b_up), Create(b_lo), run_time=0.7)
        self.remove(dot)
        self.at("interneurons activate")
        m_up = path([(1.45, 0.0), (1.95, 0.0), (1.95, -0.6), (2.55, -0.6)], GREEN, w=5, tip=0.2)
        eff2 = chip("flexor muscles", GREEN, 26).move_to(eff_c)
        self.play(Create(m_up), ReplacementTransform(eff_c, eff2), run_time=0.8)
        dot2, anim2 = run_dot([(1.95, 0.0), (1.95, -0.6), OUT_P[0], OUT_P[1], OUT_P[2]], rt=1.5)
        self.add(dot2)
        self.play(anim2)
        self.remove(dot2)
        lift = T("the limb lifts", 26, GREEN).next_to(eff2, UP, buff=0.2)
        self.play(Indicate(eff2, color=GREEN, scale_factor=1.12), FadeIn(lift), run_time=0.6)
        self.at("inhibit the opposing")
        ext = chip("extensor muscles", RED, 26).move_to([4.6, -2.35, 0])
        inh = VGroup(Line([1.45, -1.3, 0], [4.6, -1.3, 0], color=RED, stroke_width=5),
                     stop_bar([4.6, -1.3], [4.6, -1.85]))
        self.play(Create(inh), FadeIn(ext), run_time=0.9)
        inh_l = T("inhibited", 24, RED).move_to([3.55, -0.95, 0])
        self.play(FadeIn(inh_l), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """The five parts in a row, the two variants beneath, somatic note, final rule."""

    def construct(self):
        names = [("receptor", BLUE), ("sensory neuron", BLUE), ("integrating centre", GREY),
                 ("motor neuron", GREEN), ("effector", GREEN)]
        chips = [chip(n, c, 26, pad=0.18) for n, c in names]
        row = VGroup(*chips).arrange(RIGHT, buff=0.5).move_to([0, 2.5, 0])
        fit(row, max_w=12.4)
        arrows = [arr(chips[i].get_right(), chips[i + 1].get_left(), GREY, 4, 0.16) for i in range(4)]
        cx = chips[2].get_x()
        k_title = T("knee jerk: somatic, because its effector is skeletal muscle", 28, GREEN).move_to([0, 0.7, 0])
        nov = T("somatic does not mean voluntary", 28, GREY).move_to([0, 0.7, 0])
        k_syn = chip("knee jerk: the direct path has one synapse", ORANGE, 28).move_to([0, -0.6, 0])
        w_chip = chip("interneurons also inhibit the hamstring", PURPLE, 28).move_to([0, -1.9, 0])
        w_chip2 = chip("many other reflexes use interneurons", PURPLE, 28).move_to([0, -1.9, 0])
        k_ln = Line(chips[2].get_bottom(), [cx, 0.95, 0], color=GREY, stroke_width=3)
        t1 = Line([cx, 0.2, 0], k_syn.get_top(), color=ORANGE, stroke_width=3)

        self.at("somatic reflex")
        self.play(*[FadeIn(c) for c in chips], *[Create(a) for a in arrows], run_time=1.0)
        self.play(FadeIn(k_title, shift=UP * 0.1), run_time=0.6)
        self.at("does not mean voluntary")
        self.play(ReplacementTransform(k_title, nov), run_time=0.7)
        self.at("its direct path")
        self.play(FadeOut(nov), FadeIn(k_syn, shift=UP * 0.1), run_time=0.8)
        self.at("interneurons also")
        self.play(FadeIn(w_chip, shift=UP * 0.1), run_time=0.8)
        self.at("many other reflexes")
        self.play(ReplacementTransform(w_chip, w_chip2), run_time=0.7)
        self.at("five parts")
        dot, anim = run_dot([chips[0].get_left() + UP * 0.6, chips[4].get_right() + UP * 0.6], rt=2.8)
        self.add(dot)
        self.play(anim)
        self.remove(dot)
        self.finish()


class S07End(EndCard):
    LINE = "Trace any reflex: receptor, sensory neuron, integrating centre, motor neuron, effector."
