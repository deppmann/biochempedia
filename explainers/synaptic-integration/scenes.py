"""Inhibition That Moves Nothing  (Biochemistrypedia neuroscience explainer, synaptic-integration)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Numbers are the lesson's worked problem (illustrative isopotential cell: C 200 pF, gL 10 nS,
EL -65 mV, threshold -50 mV; gE 5 nS at 0 mV; gI 10 nS at -65 mV).

COLOR MAP (one color per concept, whole video)
  BLUE   = the neuron (cell outline)
  GREEN  = excitatory input / excitatory conductance
  RED    = inhibitory input / inhibitory (shunting) conductance, and "no spike"
  GREY   = leak conductance, membrane, structure
  YELLOW = the membrane voltage (dot, trace)
  TEAL   = spike threshold (dashed line)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

EL, EE, EI, THR = -65.0, 0.0, -65.0, -50.0
GX = 3.7            # gauge axis x
DX = 5.4            # dot x
K = 0.0074          # arrow length per (nS x mV)


def yv(v):          # voltage -> screen y (0 mV at 3.0, -70 mV at -3.0)
    return 3.0 + v * (6.0 / 70.0)


def vss(gL, gE, gI):
    return (gL * EL + gE * EE + gI * EI) / (gL + gE + gI)


def fmt(v):
    return f"{v:.1f}".replace("-", "−")


def rlabel(text, y, x=GX - 0.2, size=22, color=TEXT, font="M"):
    t = (M if font == "M" else T)(text, size, color)
    return t.move_to([x - t.width / 2, y, 0])


def pull(x, y0, length, up, color):
    """a vertical pull arrow from y0 (up or down) with a given length, hidden if tiny"""
    if length < 0.22:
        return VGroup()
    y1 = y0 + (length if up else -length)
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, color=color, stroke_width=7, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20)


class Stage:
    """voltage gauge (right), channel rows on a membrane bar (left), tug-of-war arrows."""

    def __init__(self, scene, gL=10, gE=0, gI=0, rows=True, values=True):
        self.s = scene
        self.gL, self.gE, self.gI = ValueTracker(gL), ValueTracker(gE), ValueTracker(gI)
        self.values = values
        # --- gauge
        axis = Line([GX, yv(0) + 0.15, 0], [GX, yv(-70), 0], color=GREY, stroke_width=3)
        l0 = Line([GX, yv(0), 0], [6.3, yv(0), 0], color=GREEN, stroke_width=2).set_opacity(0.45)
        l65 = Line([GX, yv(-65), 0], [6.3, yv(-65), 0], color=GREY, stroke_width=2).set_opacity(0.6)
        thr = DashedLine([GX, yv(THR), 0], [6.3, yv(THR), 0], color=TEAL, stroke_width=4, dash_length=0.15)
        self.lab0 = rlabel("0 mV", yv(0), color=GREEN)
        self.lab65 = rlabel("−65 mV", yv(-65), color=GREY)
        self.labthr = VGroup(rlabel("threshold", yv(THR) + 0.22, size=22, color=TEAL, font="T"),
                             rlabel("−50 mV", yv(THR) - 0.12, color=TEAL))
        self.gauge = VGroup(axis, l0, l65, thr, self.lab0, self.lab65, self.labthr)
        # --- live dot and arrows
        def V():
            return vss(self.gL.get_value(), self.gE.get_value(), self.gI.get_value())
        self.V = V
        self.dot = always_redraw(lambda: Dot([DX, yv(V()), 0], radius=0.17, color=YELLOW))

        def exc():
            return pull(DX, yv(V()) + 0.17, self.gE.get_value() * (EE - V()) * K, True, GREEN)

        def leak():
            return pull(DX - 0.32, yv(V()) - 0.17, self.gL.get_value() * max(V() - EL, 0) * K, False, GREY)

        def inh():
            return pull(DX + 0.32, yv(V()) - 0.17, self.gI.get_value() * max(V() - EI, 0) * K, False, RED)
        self.arrows = [always_redraw(exc), always_redraw(leak), always_redraw(inh)]
        # --- rows on a membrane bar
        self.rows = {}
        self.membrane = Rectangle(width=0.24, height=3.9, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.35).move_to([-5.9, 0.7, 0])
        if rows:
            spec = [("leak", "Leak", GREY, "10 nS", "E = −65 mV", 2.0),
                    ("exc", "Excitatory", GREEN, "5 nS", "E = 0 mV", 0.8),
                    ("inh", "Inhibitory", RED, "10 nS", "E = −65 mV", -0.8)]
            for key, name, col, g, e, y in spec:
                c = chip(name, col, size=30)
                c.move_to([-4.4, y, 0])
                tick = Line([-5.78, y, 0], [c.get_left()[0], y, 0], color=col, stroke_width=3)
                info = VGroup(M(g, 28, col), M(e, 24, col)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
                info.move_to([-1.7, y, 0], aligned_edge=LEFT)
                if not values:
                    info.set_opacity(0)
                self.rows[key] = VGroup(tick, c, info)
                self.rows[key].chipbox, self.rows[key].info = c, info

    @staticmethod
    def _state(r, on):
        box, lab = r.chipbox[0], r.chipbox[1]
        return [r[0].animate.set_stroke(opacity=1 if on else 0.3),
                box.animate.set_stroke(opacity=1 if on else 0.3).set_fill(opacity=0.16 if on else 0.04),
                lab.animate.set_opacity(1 if on else 0.3),
                r.info.animate.set_opacity(1 if on else 0)]

    def dim(self, key):
        return self._state(self.rows[key], False)

    def bright(self, key):
        return self._state(self.rows[key], True)

    def set_now(self, key, on):
        r = self.rows[key]
        r[0].set_stroke(opacity=1 if on else 0.3)
        r.chipbox[0].set_stroke(opacity=1 if on else 0.3).set_fill(opacity=0.16 if on else 0.04)
        r.chipbox[1].set_opacity(1 if on else 0.3)
        r.info.set_opacity(1 if on else 0)

    def add_static(self, rows_dim=()):
        for k in self.rows:
            self.set_now(k, k not in rows_dim)
        self.s.add(self.gauge, self.dot, *self.arrows)
        if self.rows:
            self.s.add(self.membrane, *self.rows.values())

    def eq(self, lines, y=-2.45):
        g = VGroup(*[M(t, 22, YELLOW if i == len(lines) - 1 else TEXT) for i, t in enumerate(lines)])
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fit(g, max_w=6.2, max_h=1.6)
        return g.move_to([-5.9 + g.width / 2, y, 0])


def btext(text, size=24, color=GREY, font="T"):
    t = (T if font == "T" else M)(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def inhib_end(a, b, color=RED, w=6):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def exc_arrow(a, b, color=GREEN, w=6):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=0.26,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Integration, Inhibition and Neuromodulation"
    TITLE = "Inhibition That Moves Nothing"


class S01Puzzle(SpokenScene):
    def construct(self):
        st = Stage(self, rows=False)
        self.add(st.gauge, st.dot)
        cx, cy = -1.9, 0.2
        soma = Circle(radius=1.15, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18).move_to([cx, cy, 0])
        d1 = Line([cx - 0.8, cy + 0.8, 0], [cx - 2.6, cy + 1.9, 0], color=BLUE, stroke_width=5)
        d2 = Line([cx - 0.8, cy - 0.8, 0], [cx - 2.6, cy - 1.5, 0], color=BLUE, stroke_width=5)
        ax = Line([cx + 1.15, cy, 0], [cx + 2.6, cy, 0], color=BLUE, stroke_width=5)
        neuron = VGroup(soma, d1, d2, ax)
        nlab = T("neuron", 26, BLUE).move_to([cx, cy, 0])
        inh_in = inhib_end([cx - 4.0, cy - 2.6, 0], [cx - 2.68, cy - 1.56, 0])
        inh_lab = T("inhibitory input", 26, RED).move_to([cx - 3.2, cy - 2.95, 0])
        exc_in = exc_arrow([cx - 4.0, cy + 2.9, 0], [cx - 2.64, cy + 1.95, 0])
        exc_lab = T("excitatory input", 26, GREEN).move_to([cx - 3.2, cy + 3.2, 0])
        spike = chip("spike", GREY, size=28).move_to([cx + 3.5, cy, 0])
        nospike = chip("no spike", RED, size=28).move_to([cx + 3.5, cy, 0])
        how = T("How?", 52, YELLOW, weight=BOLD).move_to([cx + 0.2, cy + 2.2, 0])
        delta = btext("change in Vm: 0 mV", 24, YELLOW, font="M").move_to([2.1, -3.3, 0])
        usual = T("inputs are voltages that add and subtract", 24, GREY).move_to([-0.6, -1.9, 0])
        strike = Line(usual.get_left() + LEFT * 0.1, usual.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)

        self.at("A neuron can receive")
        self.play(FadeIn(neuron), FadeIn(nlab), run_time=0.6)
        self.at("inhibitory input")
        self.play(Create(inh_in), FadeIn(inh_lab), run_time=0.6)
        self.at("zero millivolts")
        self.play(FadeIn(delta), Indicate(st.dot, color=YELLOW, scale_factor=1.5), run_time=0.7)
        self.at("stop the cell")
        self.play(Create(exc_in), FadeIn(exc_lab), FadeIn(spike), FadeOut(delta), run_time=0.6)
        self.play(Transform(spike, nospike), run_time=0.5)
        self.at("How")
        self.play(FadeIn(how, scale=1.2), run_time=0.4)
        self.at("voltages that add")
        self.play(FadeIn(usual), run_time=0.5)
        self.at("cannot explain")
        self.play(Create(strike), run_time=0.5)
        self.finish()


class S02Conductance(SpokenScene):
    def construct(self):
        st = Stage(self)
        st.add_static(rows_dim=("leak", "exc", "inh"))
        self.remove(*st.rows.values(), st.membrane)
        self.at("conductance instead")
        self.play(FadeIn(st.membrane), run_time=0.4)
        self.play(*[FadeIn(st.rows[k]) for k in ("leak", "exc", "inh")], run_time=0.8)
        self.at("opens channels")
        self.play(*st.bright("exc"), run_time=0.5)
        self.play(Indicate(st.rows["exc"].chipbox, color=GREEN), run_time=0.6)
        self.at("measured in")
        unit = M("g in nS", 28, TEXT).move_to([-1.7 + 0.55, 3.05, 0])
        self.play(FadeIn(unit), run_time=0.4)
        self.at("reversal potential")
        etag = T("reversal potential", 24, GREEN).move_to([2.0, yv(0) - 0.5, 0])
        self.play(FadeIn(etag), Indicate(st.lab0, color=GREEN), run_time=0.7)
        self.at("current through them is zero")
        zero = T("current is zero here", 24, GREEN).move_to([2.0, yv(0) - 0.95, 0])
        self.play(FadeIn(zero), run_time=0.4)
        self.at("Every open conductance")
        self.play(*st.bright("leak"), run_time=0.4)
        self.play(st.gE.animate.set_value(5), run_time=1.3)
        self.at("pulls the membrane")
        self.play(Indicate(VGroup(*st.arrows), color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.finish()


class S03Excite(SpokenScene):
    def construct(self):
        st = Stage(self)
        st.add_static(rows_dim=("leak", "exc", "inh"))
        e1 = st.eq(["V = (10 \u00d7 \u221265 + 5 \u00d7 0) / (10 + 5)", "  = \u221243.3 mV"])
        note = T("illustrative values, same voltage everywhere", 24, GREY).move_to([-2.9, -3.3, 0])
        self.at("made up cell")
        self.play(FadeIn(note), run_time=0.5)
        self.at("leak conductance")
        self.play(*st.bright("leak"), run_time=0.5)
        self.at("reversing at minus")
        self.play(Indicate(st.lab65, color=YELLOW, scale_factor=1.15), run_time=0.7)
        self.at("Threshold")
        self.play(Indicate(st.labthr, color=TEAL, scale_factor=1.15), run_time=0.7)
        self.at("open an excitatory")
        self.play(*st.bright("exc"), run_time=0.4)
        self.play(st.gE.animate.set_value(5), run_time=1.6)
        self.at("average of the reversal")
        self.play(FadeIn(e1), run_time=0.8)
        self.at("above threshold")
        self.play(Indicate(st.dot, color=YELLOW, scale_factor=1.6), run_time=0.7)
        self.finish()


class S04Shunt(SpokenScene):
    def construct(self):
        st = Stage(self, gE=5)
        st.add_static(rows_dim=("inh",))
        e0 = st.eq(["V = (10 \u00d7 \u221265 + 5 \u00d7 0) / (10 + 5)", "  = \u221243.3 mV"])
        e1 = st.eq(["V = (10 \u00d7 \u221265 + 5 \u00d7 0 + 10 \u00d7 \u221265) / 25", "  = \u221252.0 mV"])
        e2 = st.eq(["V = (10 \u00d7 \u221265 + 10 \u00d7 \u221265) / 20", "  = \u221265 mV"])
        self.add(e0)
        nospike = chip("no spike", RED, size=28).move_to([0.7, -1.45, 0])
        trace = btext("trace unmoved", 26, YELLOW).move_to([0.9, -1.85, 0])
        self.at("add an inhibitory")
        self.play(*st.bright("inh"), run_time=0.5)
        self.play(st.gI.animate.set_value(10), Transform(e0, e1), run_time=1.6)
        self.at("below threshold")
        self.play(FadeIn(nospike, shift=UP * 0.1), Indicate(st.dot, color=YELLOW, scale_factor=1.6), run_time=0.7)
        self.at("Take the excitation away")
        self.play(FadeOut(nospike), *st.dim("exc"), st.gE.animate.set_value(0), Transform(e0, e2), run_time=1.6)
        self.at("does not move")
        self.play(FadeIn(trace), Indicate(st.dot, color=YELLOW, scale_factor=1.6), run_time=0.6)
        self.at("vetoed the spike")
        self.play(Indicate(st.rows["inh"].chipbox, color=RED, scale_factor=1.15), run_time=0.8)
        self.finish()


class S05Time(SpokenScene):
    def construct(self):
        X0, X1, Y0, Y1 = -5.2, 5.6, -2.7, 1.9      # plot box (ms 0..30, mV 0..4)
        tx = lambda t: X0 + (X1 - X0) * t / 30.0
        my = lambda v: Y0 + (Y1 - Y0) * v / 4.0
        axx = Line([X0, Y0, 0], [X1, Y0, 0], color=GREY, stroke_width=3)
        axy = Line([X0, Y0, 0], [X0, Y1 + 0.1, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for t in (0, 10, 20, 30):
            ticks.add(M(str(t), 22, GREY).move_to([tx(t), Y0 - 0.32, 0]))
        for v in (0, 2, 4):
            ticks.add(M(str(v), 22, GREY).move_to([X0 - 0.3, my(v), 0]))
        xl = T("time (ms)", 22, GREY).move_to([(X0 + X1) / 2, Y0 - 0.7, 0])
        yl = T("depolarization (mV)", 22, GREY).rotate(PI / 2).move_to([X0 - 0.75, (Y0 + Y1) / 2, 0])
        sketch = T("in this sketch", 24, TEAL).move_to([4.6, 3.3, 0])
        axes = VGroup(axx, axy, ticks, xl, yl)
        ts = np.linspace(0, 30, 301)

        def tr(tau):
            pts = []
            for t in ts:
                v = 2 * np.exp(-t / tau) + (2 * np.exp(-(t - 10) / tau) if t >= 10 else 0)
                pts.append([tx(t), my(v), 0])
            i = next(k for k, t in enumerate(ts) if t >= 10)
            pts.insert(i, [tx(10), my(2 * np.exp(-10 / tau)), 0])
            m = VMobject(stroke_width=6)
            m.set_points_as_corners(pts)
            return m
        yel, red = tr(20).set_color(YELLOW), tr(10).set_color(RED)

        def one(tau):
            m = VMobject(stroke_width=6)
            m.set_points_as_corners([[tx(t), my(2 * np.exp(-t / tau)), 0] for t in ts])
            return m
        yel0, red0 = one(20).set_color(YELLOW), one(10).set_color(RED)
        leg1 = VGroup(Line(ORIGIN, RIGHT * 0.6, color=YELLOW, stroke_width=6), M("time constant 20 ms", 24, YELLOW)).arrange(RIGHT, buff=0.2)
        leg2 = VGroup(Line(ORIGIN, RIGHT * 0.6, color=RED, stroke_width=6), M("time constant 10 ms", 24, RED)).arrange(RIGHT, buff=0.2)
        leg = VGroup(leg1, leg2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-1.2, 3.0, 0])
        p1 = VGroup(exc_arrow([tx(0), my(3.0), 0], [tx(0), my(2.1), 0]), M("+2 mV", 22, GREEN).move_to([tx(0) + 0.85, my(2.9), 0]))
        p2 = VGroup(exc_arrow([tx(10), my(4.3), 0], [tx(10), my(3.45), 0]), M("+2 mV", 22, GREEN).move_to([tx(10) + 0.85, my(4.1), 0]))
        pk1 = Dot([tx(10), my(2 + 2 * np.exp(-0.5)), 0], radius=0.11, color=YELLOW)
        pk2 = Dot([tx(10), my(2 + 2 * np.exp(-1.0)), 0], radius=0.11, color=RED)
        l1 = btext("3.21 mV", 24, YELLOW, font="M").move_to([tx(10) + 1.15, my(3.21) + 0.1, 0])
        l2 = btext("2.74 mV", 24, RED, font="M").move_to([tx(10) - 1.15, my(2.74) + 0.05, 0])
        r1 = Dot([tx(10), my(2 * np.exp(-0.5)), 0], radius=0.09, color=YELLOW)
        r2 = Dot([tx(10), my(2 * np.exp(-1.0)), 0], radius=0.09, color=RED)
        rl1 = btext("1.21 mV", 22, YELLOW, font="M").move_to([tx(10) + 0.95, my(1.21) + 0.05, 0])
        rl2 = btext("0.74 mV", 22, RED, font="M").move_to([tx(10) + 0.95, my(0.74) - 0.05, 0])

        self.at("Inhibition like this")
        self.play(FadeIn(axes), FadeIn(sketch), run_time=0.8)
        self.at("It lowers the input")
        self.play(Create(p1), run_time=0.5)
        self.play(Create(yel0), Create(red0), run_time=1.5)
        self.at("shortens the time constant")
        self.play(FadeIn(leg1), run_time=0.5)
        self.at("milliseconds to")
        self.play(FadeIn(leg2), run_time=0.5)
        self.at("two brief pulses")
        self.play(Create(p2), run_time=0.5)
        self.at("Without the shunt")
        self.play(FadeOut(red0), Transform(yel0, yel), run_time=1.2)
        self.at("they add up to")
        self.play(FadeIn(pk1), FadeIn(l1), run_time=0.4)
        self.at("With the shunt")
        self.play(Create(red), run_time=1.2, rate_func=linear)
        self.at("shunt only")
        self.play(FadeIn(pk2), FadeIn(l2), run_time=0.4)
        self.at("did not shrink each jump")
        self.play(Indicate(p1, color=GREEN), run_time=0.9)
        self.at("left less of the first pulse")
        self.play(FadeIn(r1), FadeIn(r2), FadeIn(rl1), FadeIn(rl2), run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        st = Stage(self, gE=0, gI=10)
        st.add_static(rows_dim=("exc",))
        rule1 = T("defined by its effect on firing", 28, RED).move_to([-2.9, -2.45, 0])
        rule2 = T("not by which way the trace moves", 28, YELLOW).move_to([-2.9, -3.0, 0])
        nospike = chip("no spike", RED, size=28).move_to([0.7, -1.45, 0])
        self.at("So an inhibitory input")
        self.play(FadeIn(rule1), run_time=0.6)
        self.at("which way the trace moves")
        self.play(FadeIn(rule2), run_time=0.6)
        self.at("Inputs add as conductances")
        self.play(*st.bright("exc"), run_time=0.4)
        self.play(Indicate(VGroup(*[st.rows[k].chipbox for k in st.rows]), color=TEXT, scale_factor=1.08), run_time=0.8)
        self.at("pulls the voltage toward")
        self.play(st.gE.animate.set_value(5), run_time=1.0)
        self.play(Indicate(VGroup(*st.arrows), color=YELLOW, scale_factor=1.1), run_time=0.6)
        self.at("A shunt can leave")
        self.play(*st.dim("exc"), st.gE.animate.set_value(0), run_time=1.2)
        self.at("still veto")
        self.play(*st.bright("exc"), st.gE.animate.set_value(5), FadeIn(nospike), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Inputs add as conductances; inhibition is defined by firing."
