"""Breaking the proton gradient  (Biochemistrypedia: The proton-motive force and ATP synthase)

COLOR MAP (one color per concept, whole video)
  BLUE   = electron transport chain, oxygen use / respiration rate
  YELLOW = protons (H+), the proton gradient, low pH
  GREEN  = ATP synthase, ATP, ATP output
  GOLD   = ADP, call-outs
  RED    = anything that breaks or blocks: the leak (uncoupler), the brake on the chain, reverse mode, heat
  TEAL   = IF1, the emergency brake protein
  TEXT   = neutral labels;  GREY = membrane, axes, secondary labels
NO molecular structures are drawn: only labelled blocks, particle streams, meters, arrows and a curve computed
from a simple model of isolated mitochondria (state 4 -> ADP added -> state 3 -> ADP used up -> state 4).
"""
import numpy as np

from bp_style import *

# ----------------------------------------------------------------------------- stage geometry
MEM_Y = -0.2          # centre line of the inner membrane band
CX, SX, LX = -3.6, 3.3, 0.0   # chain, ATP synthase, leak x positions


class Flow(VGroup):
    """Particles marching along a polyline. rate>0 forward, <0 reverse, 0 hidden. Runs in updaters."""

    def __init__(self, pts, n, rate, color=YELLOW, shape="dot", size=0.09, speed=0.55):
        super().__init__()
        self.pts = [np.array(p, float) for p in pts]
        self.seg = [float(np.linalg.norm(self.pts[i + 1] - self.pts[i])) for i in range(len(self.pts) - 1)]
        self.cum = np.concatenate([[0.0], np.cumsum(self.seg)])
        self.L = float(self.cum[-1])
        self.rate, self.n, self.speed, self.phase = rate, n, speed, 0.0
        for _ in range(n):
            if shape == "dot":
                m = Dot(radius=size, color=color)
            else:
                m = RoundedRectangle(corner_radius=0.05, width=size * 2.4, height=size * 2.0, stroke_width=0,
                                     fill_color=color, fill_opacity=1)
            self.add(m)
        self.add_updater(self._upd)
        self._upd(self, 0)

    def _at(self, u):
        d = u * self.L
        i = int(np.clip(np.searchsorted(self.cum, d, side="right") - 1, 0, len(self.seg) - 1))
        f = (d - self.cum[i]) / max(self.seg[i], 1e-6)
        return self.pts[i] + f * (self.pts[i + 1] - self.pts[i])

    def _upd(self, mob, dt):
        r = self.rate.get_value()
        self.phase = (self.phase + dt * self.speed * r) % 1.0
        for i, m in enumerate(self.submobjects):
            u = (i / self.n + self.phase) % 1.0
            m.move_to(self._at(u))
            fade = min(1.0, u / 0.1, (1 - u) / 0.1)
            m.set_opacity(float(np.clip(abs(r) * 3, 0, 1)) * fade)


class Pool(VGroup):
    """Protons in the intermembrane space; how many are visible = the gradient g (0..1)."""

    def __init__(self, g, n=26, seed=3):
        super().__init__()
        self.g, self.n = g, n
        rng = np.random.default_rng(seed)
        pts = []
        while len(pts) < n:
            p = np.array([rng.uniform(-5.9, 5.9), rng.uniform(0.62, 2.0)])
            if all(np.linalg.norm(p - q) > 0.62 for q in pts):
                pts.append(p)
        pts.sort(key=lambda p: p[1] + 0.3 * rng.random())   # fill from the membrane upward? no: random order
        order = rng.permutation(n)
        for k in order:
            self.add(Dot([pts[k][0], pts[k][1], 0], radius=0.1, color=YELLOW))
        self.add_updater(self._upd)
        self._upd(self, 0)

    def _upd(self, mob, dt):
        lvl = self.g.get_value() * self.n
        for i, m in enumerate(self.submobjects):
            m.set_opacity(float(np.clip(lvl - i, 0, 1)))


def membrane(label=True):
    band = Rectangle(width=12.4, height=0.5, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                     fill_opacity=0.22).move_to([0, MEM_Y, 0])
    ims = T("intermembrane space", 24, GREY).move_to([-6.2, 2.4, 0], aligned_edge=LEFT)
    mat = T("matrix", 24, GREY).move_to([-6.2, -2.75, 0], aligned_edge=LEFT)
    inner = T("membrane", 24, GREY).move_to([5.3, MEM_Y, 0])
    return VGroup(band, ims, mat, inner)


def chain_block():
    r = RoundedRectangle(corner_radius=0.16, width=3.5, height=1.3, stroke_color=BLUE, stroke_width=3,
                         fill_color=BLUE, fill_opacity=0.2).move_to([CX, MEM_Y, 0])
    t = T("electron\ntransport chain", 24, BLUE, line_spacing=0.8).move_to(r).shift(LEFT * 0.3)
    return VGroup(r, t)


def synth_block():
    fo = RoundedRectangle(corner_radius=0.14, width=1.2, height=0.8, stroke_color=GREEN, stroke_width=3,
                          fill_color=GREEN, fill_opacity=0.25).move_to([SX, MEM_Y, 0])
    f1 = RoundedRectangle(corner_radius=0.4, width=1.7, height=1.1, stroke_color=GREEN, stroke_width=3,
                          fill_color=GREEN, fill_opacity=0.25).move_to([SX, -1.2, 0])
    lab_o = T("Fo", 24, GREEN).move_to(fo).shift(LEFT * 0.2)
    lab_1 = T("F1", 24, GREEN).move_to(f1).shift(LEFT * 0.2 + DOWN * 0.3)
    name = T("ATP synthase", 24, GREEN).move_to([SX, -2.12, 0])
    return VGroup(fo, f1, lab_o, lab_1, name)


class Spinner(VGroup):
    """The rotating stalk inside F1: a short stick that turns; spin>0 forward (clockwise), <0 reverse."""

    def __init__(self, spin, color=TEXT):
        super().__init__()
        self.spin, self.ang = spin, 0.0
        self.ctr = np.array([SX - 0.2, -1.2 + 0.15, 0.0])
        self.stick = Line(self.ctr, self.ctr + np.array([0.0, 0.27, 0.0]), color=color, stroke_width=6)
        self.hub = Dot(self.ctr, radius=0.07, color=color)
        self.add(self.stick, self.hub)
        self.add_updater(self._upd)

    def _upd(self, mob, dt):
        s = self.spin.get_value()
        da = -dt * s * TAU * 0.9
        self.ang += da
        self.stick.rotate(da, about_point=self.ctr)


def meter(label, color, val, cx, cy, w=2.9):
    lab = T(label, 24, color)
    track = Rectangle(width=w, height=0.28, stroke_color=GREY, stroke_width=2, fill_opacity=0)
    row = VGroup(lab, track).arrange(RIGHT, buff=0.25).move_to([cx, cy, 0])

    def fill():
        ww = max(0.002, w * float(np.clip(val.get_value(), 0, 1)))
        return Rectangle(width=ww, height=0.28, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(
            track.get_left() + RIGHT * ww / 2)

    return VGroup(row, always_redraw(fill))


def pumpstream(rate, n=5):
    return Flow([[CX + 1.4, -1.6, 0], [CX + 1.4, 1.0, 0]], n, rate, YELLOW, speed=0.6)


def synthstream(rate, n=6):
    return Flow([[SX + 0.38, 1.0, 0], [SX + 0.38, -0.3, 0], [SX + 1.15, -0.62, 0]], n, rate, YELLOW, speed=0.6)


def leakstream(rate, n=5):
    return Flow([[LX, 1.0, 0], [LX, -1.35, 0]], n, rate, YELLOW, speed=0.7)


def atpstream(rate, n=3):
    return Flow([[4.35, -1.2, 0], [5.9, -1.2, 0]], n, rate, GREEN, shape="sq", size=0.11, speed=0.7)


class Sp(SpokenScene):
    """SpokenScene + room(): seconds until the next cue, so an animation ends right when the words land."""

    def room(self, phrase, nth=0, lead=0.2, lo=0.3, hi=99.0):
        return float(np.clip(self.t_of(phrase, nth) - lead - self.elapsed(), lo, hi))


# ----------------------------------------------------------------------------- cards
class S00Title(TitleCard):
    LESSON = "The proton-motive force and ATP synthase"
    TITLE = "Breaking the proton gradient"


class S05End(EndCard):
    LINE = "The gradient couples respiration to the cell's ATP demand."


# ----------------------------------------------------------------------------- s01: uncoupling
class S01Uncoupling(Sp):
    def construct(self):
        mem = membrane()
        chain, synth = chain_block(), synth_block()
        g = ValueTracker(0.0)
        pool = Pool(g)
        pump_r, syn_r, leak_r, atp_r, spin = (ValueTracker(0) for _ in range(5))
        pump, syn, leak, atp = pumpstream(pump_r), synthstream(syn_r), leakstream(leak_r), atpstream(atp_r)
        spinner = Spinner(spin)

        # "Picture the electron transport chain and ATP synthase as a couple ..."
        self.play(FadeIn(mem), run_time=0.7)
        self.add(pool, pump, syn, leak, atp)
        self.at("electron transport chain")
        self.play(FadeIn(chain, shift=RIGHT * 0.2), run_time=self.room("ATP synthase", lo=0.5))
        self.at("ATP synthase")
        self.play(FadeIn(synth, shift=LEFT * 0.2), FadeIn(spinner), run_time=self.room("couple", lo=0.5))
        # the pair is joined by a bracket
        y = -2.55
        left_ln = VGroup(Line([CX, y, 0], [(CX + SX) / 2, y, 0], color=TEXT, stroke_width=4),
                         Line([CX, y, 0], [CX, y + 0.18, 0], color=TEXT, stroke_width=4))
        right_ln = VGroup(Line([(CX + SX) / 2, y, 0], [SX, y, 0], color=TEXT, stroke_width=4),
                          Line([SX, y, 0], [SX, y + 0.18, 0], color=TEXT, stroke_width=4))
        self.at("couple")
        self.play(Create(left_ln), Create(right_ln), run_time=self.room("tightly coupled", lo=0.5))
        lab_c = T("coupled", 28, TEXT).move_to([(CX + SX) / 2, y - 0.42, 0])
        self.at("tightly coupled")
        self.play(FadeIn(lab_c, shift=UP * 0.1), run_time=0.5)

        # "The chain builds the proton gradient"
        self.at("The chain builds")
        pump_r.set_value(1)
        self.play(g.animate.set_value(0.85), run_time=self.room("and ATP synthase spends", lo=1.0), rate_func=linear)
        grad_lab = T("H⁺ gradient", 24, YELLOW).move_to([3.6, 2.4, 0])
        self.add(grad_lab)
        # "and ATP synthase spends it to make ATP"
        self.at("and ATP synthase spends")
        syn_r.set_value(1); spin.set_value(0.5)
        self.play(g.animate.set_value(0.6), run_time=self.room("make ATP", lo=0.6), rate_func=smooth)
        self.at("make ATP")
        atp_r.set_value(1)
        atp_lab = T("ATP", 24, GREEN).move_to([5.1, -1.65, 0])
        self.play(FadeIn(atp_lab), run_time=0.4)
        # meters
        o2v, atpv = ValueTracker(0.35), ValueTracker(0.6)
        m_o2 = meter("oxygen use", BLUE, o2v, -3.1, 3.15)
        m_atp = meter("ATP made", GREEN, atpv, 3.1, 3.15)
        self.play(FadeIn(m_o2), FadeIn(m_atp), run_time=self.room("Uncoupling is", lo=0.6))

        # "Uncoupling is the breakup."
        self.at("Uncoupling is the breakup")
        self.wait(0.3)
        self.at("breakup", lead=0.25)
        left_ln.generate_target(); right_ln.generate_target()
        left_ln.target.shift(LEFT * 0.4).set_color(RED)
        right_ln.target.shift(RIGHT * 0.4).set_color(RED)
        self.play(MoveToTarget(left_ln), MoveToTarget(right_ln),
                  Transform(lab_c, T("uncoupled", 28, RED).move_to(lab_c)), run_time=0.8)

        # "Protons find another way back across the membrane"
        self.at("Protons find another way")
        leak_ch = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.62, stroke_color=RED, stroke_width=3,
                                   fill_color=RED, fill_opacity=0.5).move_to([LX, MEM_Y, 0])
        leak_lab = T("leak", 24, RED).move_to([LX, -1.55, 0])
        self.play(FadeIn(leak_ch, scale=1.4), FadeIn(leak_lab), run_time=0.6)
        leak_r.set_value(1.3)
        self.play(g.animate.set_value(0.4), run_time=self.room("instead of going through", lo=0.8), rate_func=smooth)
        # "instead of going through ATP synthase": the synthase goes quiet
        self.at("instead of going through")
        self.play(syn_r.animate.set_value(0), spin.animate.set_value(0), atp_r.animate.set_value(0),
                  synth.animate.set_opacity(0.35), atp_lab.animate.set_opacity(0.35),
                  run_time=self.room("so the energy", lo=0.6))
        # "so the energy of the gradient is released as heat"
        self.at("released as heat")
        heat = VGroup(*[
            FunctionGraph(lambda x: 0.07 * np.sin(9 * x), x_range=[-0.5, 0.5], color=RED, stroke_width=4).shift(
                [LX, -1.95 - 0.2 * k, 0]) for k in range(3)])
        heat_lab = T("heat", 24, RED).move_to([LX + 1.1, -2.15, 0])
        self.play(Create(heat), FadeIn(heat_lab), run_time=self.room("rather than captured", lo=0.6))
        # "rather than captured as ATP"
        self.at("captured as ATP")
        self.play(atpv.animate.set_value(0.0), run_time=0.9)

        # "The chain keeps pumping furiously, oxygen consumption climbs"
        self.at("The chain keeps pumping")
        self.play(pump_r.animate.set_value(2.4), run_time=self.room("oxygen consumption", lo=0.6))
        self.at("oxygen consumption")
        self.play(o2v.animate.set_value(0.92), run_time=self.room("but the partnership", lo=0.8))
        # "but the partnership no longer produces anything useful"
        self.at("anything useful")
        none = T("no ATP\nmade", 24, RED, line_spacing=0.8).move_to([5.25, -1.75, 0])
        self.play(Transform(atp_lab, none), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s02: the prediction table
def row_icon(kind):
    """Tiny schematic: membrane line, chain (blue), synthase (green), and what the agent does (red)."""
    mem = Line([-0.7, 0, 0], [0.7, 0, 0], color=GREY, stroke_width=6)
    ch = RoundedRectangle(corner_radius=0.06, width=0.36, height=0.5, stroke_color=BLUE, stroke_width=2,
                          fill_color=BLUE, fill_opacity=0.35).move_to([-0.45, 0, 0])
    sy = RoundedRectangle(corner_radius=0.06, width=0.36, height=0.5, stroke_color=GREEN, stroke_width=2,
                          fill_color=GREEN, fill_opacity=0.35).move_to([0.45, 0, 0])
    g = VGroup(mem, ch, sy)
    x = lambda c: VGroup(Line(c + np.array([-0.2, 0.2, 0]), c + np.array([0.2, -0.2, 0]), color=RED, stroke_width=5),
                         Line(c + np.array([-0.2, -0.2, 0]), c + np.array([0.2, 0.2, 0]), color=RED, stroke_width=5))
    if kind == "etc":
        mark = x(np.array([-0.45, 0, 0]))
    elif kind == "syn":
        mark = x(np.array([0.45, 0, 0]))
    else:
        mark = RoundedRectangle(corner_radius=0.04, width=0.16, height=0.5, stroke_color=RED, stroke_width=2,
                                fill_color=RED, fill_opacity=0.9).move_to([0, 0, 0])
    return g, mark


COLS = [-0.125, 2.425, 4.975]      # O2, ATP, gradient column centres
ROWS = [1.05, -0.75, -2.55]
COL_COLORS = [BLUE, GREEN, YELLOW]


def table_cell(col, row, up, word):
    cx, cy = COLS[col], ROWS[row]
    a = Arrow([0, 0.35, 0] if not up else [0, -0.35, 0], [0, -0.35, 0] if not up else [0, 0.35, 0],
              color=COL_COLORS[col], buff=0, stroke_width=8, max_tip_length_to_length_ratio=0.5)
    a.move_to([cx - 0.5, cy, 0])
    w = T(word, 28, COL_COLORS[col]).move_to([cx + 0.45, cy, 0])
    return VGroup(a, w)


class S02Table(Sp):
    def construct(self):
        # header
        heads = VGroup(*[T(s, 28, c, line_spacing=0.8).move_to([x, 2.65, 0]) for s, c, x in
                         zip(["O₂\nconsumption", "ATP\nsynthesis", "proton\ngradient"], COL_COLORS, COLS)])
        agent_h = T("agent", 28, GREY).move_to([-4.6, 2.65, 0], aligned_edge=LEFT)
        rule = Line([-6.2, 1.85, 0], [6.25, 1.85, 0], color=GREY, stroke_width=2)
        seps = VGroup(*[Line([-6.2, y, 0], [6.25, y, 0], color=GREY, stroke_width=1).set_opacity(0.5)
                        for y in (0.15, -1.65)])

        def agent_cell(i, name, sub, kind):
            ic, mark = row_icon(kind)
            sh = np.array([-5.5, ROWS[i], 0])
            ic.shift(sh); mark.shift(sh)
            t1 = T(name, 28, TEXT, line_spacing=0.8)
            t2 = T(sub, 24, GREY)
            tx = VGroup(t1, t2).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-4.55, ROWS[i], 0],
                                                                                   aligned_edge=LEFT)
            return VGroup(ic, tx, mark)

        r1 = agent_cell(0, "ETC inhibitor", "rotenone, cyanide", "etc")
        r2 = agent_cell(1, "ATP synthase\ninhibitor", "oligomycin", "syn")
        r3 = agent_cell(2, "Uncoupler", "e.g. DNP, FCCP", "unc")
        c = {}
        c[0, 0] = table_cell(0, 0, False, "falls")
        c[0, 1] = table_cell(1, 0, False, "falls")
        c[0, 2] = table_cell(2, 0, False, "falls")
        c[1, 0] = table_cell(0, 1, False, "falls")
        c[1, 1] = table_cell(1, 1, False, "falls")
        c[1, 2] = table_cell(2, 1, True, "rises")
        c[2, 0] = table_cell(0, 2, True, "rises")
        c[2, 1] = table_cell(1, 2, False, "falls")
        c[2, 2] = table_cell(2, 2, False, "falls")
        hi1 = SurroundingRectangle(c[1, 2], color=GOLD, buff=0.2, corner_radius=0.12, stroke_width=3)
        hi2 = SurroundingRectangle(c[2, 0], color=GOLD, buff=0.2, corner_radius=0.12, stroke_width=3)

        # "This table forces you to reason like the chain itself."
        self.play(FadeIn(agent_h), run_time=0.5)
        self.play(FadeIn(heads, shift=DOWN * 0.1), Create(rule), run_time=self.room("An ETC inhibitor", lo=0.8))
        # "An ETC inhibitor, such as rotenone or cyanide, shuts everything down."
        self.at("An ETC inhibitor")
        self.play(FadeIn(r1[0]), FadeIn(r1[1][0]), Create(seps[0]), run_time=0.7)
        self.at("rotenone")
        self.play(FadeIn(r1[1][1]), run_time=0.5)
        self.at("shuts everything down")
        self.play(FadeIn(r1[2], scale=1.4), run_time=0.4)
        self.at("Oxygen consumption")
        self.play(FadeIn(c[0, 0], shift=DOWN * 0.1), run_time=0.5)
        self.at("ATP synthesis and")
        self.play(FadeIn(c[0, 1], shift=DOWN * 0.1), run_time=0.5)
        self.at("the proton gradient")
        self.play(FadeIn(c[0, 2], shift=DOWN * 0.1), run_time=0.5)
        # "An ATP synthase inhibitor, oligomycin, blocks the exit for protons"
        self.at("An ATP synthase inhibitor")
        self.play(FadeIn(r2[0]), FadeIn(r2[1][0]), Create(seps[1]), run_time=0.7)
        self.at("oligomycin")
        self.play(FadeIn(r2[1][1]), run_time=0.5)
        self.at("blocks the exit")
        self.play(FadeIn(r2[2], scale=1.4), run_time=0.4)
        self.at("so synthesis falls")
        self.play(FadeIn(c[1, 1], shift=DOWN * 0.1), run_time=0.5)
        self.at("and consumption falls")
        self.play(FadeIn(c[1, 0], shift=DOWN * 0.1), run_time=0.5)
        self.at("the gradient backs up")
        self.play(FadeIn(c[1, 2], shift=UP * 0.1), Create(hi1), run_time=0.7)
        # "The uncoupler is the counterintuitive case."
        self.at("The uncoupler")
        self.play(FadeIn(r3[0]), FadeIn(r3[1]), FadeIn(r3[2], scale=1.4), run_time=0.7)
        self.at("ATP synthesis falls")
        self.play(FadeIn(c[2, 1], shift=DOWN * 0.1), run_time=0.5)
        self.at("the gradient collapses")
        self.play(FadeIn(c[2, 2], shift=DOWN * 0.1), run_time=0.5)
        self.at("oxygen consumption increases")
        self.play(FadeIn(c[2, 0], shift=UP * 0.1), Create(hi2), run_time=0.7)

        # "Why?"  -> clear the table, show the mechanism
        table = VGroup(heads, agent_h, rule, seps, r1, r2, r3, hi1, hi2, *c.values())
        self.at("Why?")
        q = T("Why?", 56, GOLD).move_to([0, 0.5, 0])
        self.play(FadeOut(table), run_time=0.4)
        self.play(FadeIn(q), run_time=0.3)
        self.at("Because with")
        mem = membrane()
        chain = chain_block()
        g = ValueTracker(0.0)
        pool = Pool(g)
        pump_r, leak_r = ValueTracker(0), ValueTracker(0)
        pump, leak = pumpstream(pump_r), leakstream(leak_r)
        leak_ch = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.62, stroke_color=RED, stroke_width=3,
                                   fill_color=RED, fill_opacity=0.5).move_to([LX, MEM_Y, 0])
        leak_lab = T("leak", 24, RED).move_to([LX, -1.55, 0])
        grad_lab = T("H⁺ gradient", 24, YELLOW).move_to([3.6, 2.4, 0])
        self.play(FadeOut(q), run_time=0.25)
        self.add(pool, pump, leak)
        self.play(FadeIn(mem), FadeIn(chain), FadeIn(leak_ch), FadeIn(leak_lab), FadeIn(grad_lab),
                  g.animate.set_value(0.85), run_time=0.6)
        self.at("leaking away")
        leak_r.set_value(1.3)
        self.play(g.animate.set_value(0.3), run_time=self.room("the chain races", lo=0.8), rate_func=smooth)
        # "the chain races to rebuild it, pumping faster and burning more oxygen"
        self.at("the chain races")
        pump_r.set_value(1)
        o2v = ValueTracker(0.3)
        m_o2 = meter("oxygen use", BLUE, o2v, -3.1, 3.15)
        self.play(g.animate.set_value(0.45), FadeIn(m_o2), run_time=self.room("pumping faster", lo=0.8))
        self.at("pumping faster")
        self.play(pump_r.animate.set_value(2.4), run_time=1.0)
        self.at("burning more oxygen")
        self.play(o2v.animate.set_value(0.92), run_time=self.room("If you can predict", lo=0.8))

        # "If you can predict each row, you understand how coupling actually works."
        self.at("If you can predict")
        stage = Group(mem, chain, leak_ch, leak_lab, grad_lab, pool, pump, leak, m_o2)
        for m in (pool, pump, leak):
            m.clear_updaters()          # freeze the particles so they fade with the stage
        self.play(FadeOut(stage), run_time=0.6)
        self.play(FadeIn(table), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------- s03: acceptor control
def respiration_model():
    """Isolated mitochondria in an oxygen electrode chamber (illustrative numbers).
    State 4 idle rate 8 nmol O2/min; ADP (150 nmol) added at 1.0 min; at ~P/O 2.5, each O2 phosphorylates
    5 ADP, so the extra O2 above idle consumes the ADP; rate follows ADP / (ADP + Ka). The rate is passed
    through a causal first-order lag (~1.5 s, electrode response) so nothing rises before ADP is added."""
    dt = 0.001
    ts = np.arange(0, 3.0 + dt, dt)
    r4, r3, ka = 8.0, 50.0, 15.0
    adp, o2, rates, adps = 0.0, 0.0, [], []
    for t in ts:
        if abs(t - 1.0) < dt / 2:
            adp += 150.0
        rate = r4 + (r3 - r4) * adp / (adp + ka)
        adp = max(0.0, adp - 5.0 * (rate - r4) * dt)
        rates.append(rate); adps.append(adp)
    rates = np.array(rates)
    sm = rates.copy()                       # causal smoothing: electrode response time ~0.025 min
    for i in range(1, len(sm)):
        sm[i] = sm[i - 1] + (rates[i] - sm[i - 1]) * dt / 0.025
    rates = sm
    o2 = np.concatenate([[0], np.cumsum(rates[:-1] * dt)])
    return ts, rates, o2, np.array(adps)


class S03Acceptor(Sp):
    def construct(self):
        # ---------- part A: the chain will not run without ADP
        mem = membrane()
        chain, synth = chain_block(), synth_block()
        g = ValueTracker(0.85)
        pool = Pool(g)
        pump_r, syn_r, atp_r, spin, e_r = (ValueTracker(0) for _ in range(5))
        spinner = Spinner(spin)
        syn, atp = synthstream(syn_r), atpstream(atp_r)
        pump = pumpstream(pump_r)
        # electrons arrive from the matrix side and wait at a brake in front of the chain
        epath = [[-5.9, -1.6, 0], [-4.3, -1.6, 0], [-3.9, -0.9, 0]]
        efl = Flow(epath, 4, e_r, TEXT, size=0.08, speed=0.5)
        self.add(pool, pump, syn, atp, efl)
        queue = VGroup(*[Dot([-5.9 + 0.33 * k, -1.6, 0], radius=0.09, color=TEXT) for k in range(3)])
        e_lab = T("electrons", 24, TEXT).next_to(queue, DOWN, buff=0.22)
        self.play(FadeIn(mem), FadeIn(chain), FadeIn(synth), FadeIn(spinner), FadeIn(queue), FadeIn(e_lab),
                  run_time=0.7)
        brake = Rectangle(width=0.16, height=0.75, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(
            [-4.75, -1.6, 0])
        brake_lab = T("brake", 24, RED).next_to(brake, RIGHT, buff=0.2)
        self.at("refuse", lead=0.45)
        self.play(FadeIn(brake, scale=1.5), FadeIn(brake_lab), run_time=0.5)
        # "...to flow through the transport chain": the electrons bump the brake and stop
        self.at("through the transport chain")
        self.play(queue.animate.shift(RIGHT * 0.22), run_time=0.35)
        self.play(queue.animate.shift(LEFT * 0.22), run_time=0.35)
        # "unless ADP is available to be turned into ATP"
        adp = chip("ADP", GOLD, 26).move_to([0.9, -1.4, 0])
        self.at("unless ADP")
        self.play(FadeIn(adp, shift=LEFT * 0.2), run_time=0.6)
        self.at("to be turned into")
        atp_chip = chip("ATP", GREEN, 26)
        self.play(adp.animate.move_to([SX, -1.2, 0]).scale(0.6), run_time=0.5)
        atp_chip.move_to([SX, -1.2, 0]).scale(0.6)
        self.play(ReplacementTransform(adp, atp_chip), run_time=0.3)
        self.play(atp_chip.animate.move_to([5.3, -1.2, 0]).scale(1 / 0.6), run_time=0.5)
        # the brake lifts, the electrons flow, the chain pumps and the synthase turns
        self.play(FadeOut(brake, shift=UP * 0.4), FadeOut(brake_lab), FadeOut(queue), FadeOut(atp_chip),
                  run_time=0.35)
        e_r.set_value(1); pump_r.set_value(1); syn_r.set_value(1); atp_r.set_value(1); spin.set_value(0.5)
        self.wait(self.room("Watch the oxygen", lo=0.3))

        # ---------- part B: the oxygen trace
        self.at("Watch the oxygen")
        stageA = Group(mem, chain, synth, spinner, pool, pump, syn, atp, efl, e_lab)
        for m in (pool, pump, syn, atp, efl, spinner):
            m.clear_updaters()          # freeze the particles so they fade with the stage
        self.play(FadeOut(stageA), run_time=0.4)
        self.remove(stageA)

        ts, rates, o2, adps = respiration_model()
        ymax = 60.0
        ax = Axes(x_range=[0, 3, 1], y_range=[0, ymax, 20], x_length=7.2, y_length=4.2, tips=False,
                  axis_config={"include_numbers": False, "include_ticks": True, "color": GREY, "stroke_width": 3,
                               "tick_size": 0.08}).move_to([-2.0, -0.05, 0])
        deco = VGroup()
        for v in (0, 1, 2, 3):
            deco.add(M(str(v), 24, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.15))
        for v in (20, 40, 60):
            deco.add(M(str(v), 24, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.15))
        xl = T("time (min)", 26, GREY).next_to(ax.x_axis, DOWN, buff=0.6)
        yl = T("O₂ consumed (nmol)", 26, BLUE).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.6)
        ill = T("illustrative trace", 24, GREY).move_to([-2.0, 3.05, 0])
        deco.add(xl, yl)
        tt = ValueTracker(0.0)
        idx = lambda t: int(np.clip(round(t * 1000), 0, len(ts) - 1))

        def curve():
            n = idx(tt.get_value())
            pts = [ax.c2p(ts[i], o2[i]) for i in range(0, n + 1, 10)] + [ax.c2p(ts[n], o2[n])]
            if len(pts) < 2:
                pts = [ax.c2p(0, 0), ax.c2p(0.001, 0)]
            return VMobject(stroke_color=BLUE, stroke_width=5).set_points_as_corners(pts)

        def head():
            n = idx(tt.get_value())
            return Dot(ax.c2p(ts[n], o2[n]), radius=0.1, color=YELLOW)

        # rate gauge
        gx, gy0, gh = 4.9, -2.1, 3.2
        gtrack = Rectangle(width=0.6, height=gh, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(
            [gx, gy0 + gh / 2, 0])
        glab = T("respiration\nrate", 26, BLUE, line_spacing=0.8).move_to([gx, 2.05, 0])

        def gfill():
            h = max(0.003, gh * float(rates[idx(tt.get_value())]) / 60.0)
            return Rectangle(width=0.6, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to(
                [gx, gy0 + h / 2, 0])

        def gnum():
            return M(f"{rates[idx(tt.get_value())]:.0f} nmol O₂/min", 24, TEXT).move_to([gx, -2.55, 0])

        curve_m, head_m, gfill_m, gnum_m = always_redraw(curve), always_redraw(head), always_redraw(gfill), \
            always_redraw(gnum)
        self.at("Watch the oxygen")
        self.play(Create(ax), FadeIn(deco), FadeIn(ill), run_time=self.room("trace", lo=0.7))
        self.at("trace")
        self.play(FadeIn(gtrack), FadeIn(glab), FadeIn(gnum_m), FadeIn(gfill_m), FadeIn(curve_m), FadeIn(head_m),
                  run_time=0.5)
        # idle phase up to 1.0 min while "respiration idles until ADP is added"
        self.at("respiration idles")
        self.play(tt.animate.set_value(1.0), run_time=self.room("ADP is added", lo=0.8), rate_func=linear)
        self.at("ADP is added")
        adp_arrow = Arrow(ax.c2p(1.0, 31), ax.c2p(1.0, 12), color=GOLD, buff=0, stroke_width=7)
        adp_lab = T("ADP added", 26, GOLD).next_to(adp_arrow, UP, buff=0.12)
        self.play(GrowArrow(adp_arrow), FadeIn(adp_lab), run_time=0.6)
        # "then the rate jumps"
        self.at("then the rate jumps")
        t_knee = float(ts[np.argmax((ts > 1.05) & (rates < 22.0))])
        self.play(tt.animate.set_value(1.5), run_time=self.room("and it falls again", lo=0.7), rate_func=linear)
        # "and it falls again once the supply of ADP is nearly exhausted"
        self.at("and it falls again")
        self.play(tt.animate.set_value(1.85), run_time=self.room("nearly exhausted", lo=1.0), rate_func=linear)
        k_o2 = float(o2[int(round(t_knee * 1000))])
        ex_lab = T("ADP nearly used up", 24, GOLD).move_to(ax.c2p(2.35, 20))
        ex_arrow = Arrow(ex_lab.get_top() + UP * 0.08, ax.c2p(t_knee + 0.04, k_o2 - 3), color=GOLD, buff=0,
                         stroke_width=6, max_tip_length_to_length_ratio=0.25)
        self.at("nearly exhausted")
        self.play(FadeIn(ex_arrow), FadeIn(ex_lab), tt.animate.set_value(3.0), run_time=self.room("This is acceptor control", lo=1.0),
                  rate_func=linear)

        # ---------- part C: name it
        self.at("This is acceptor control")
        plot = Group(ax, deco, ill, gtrack, glab, gnum_m, gfill_m, curve_m, head_m, adp_arrow, adp_lab, ex_arrow,
                     ex_lab)
        self.play(FadeOut(plot), run_time=0.6)
        self.remove(plot)
        name1 = T("acceptor control", 60, GOLD, font=TITLE_FONT).move_to([0, 0.6, 0])
        self.play(Write(name1), run_time=self.room("also called respiratory control", lo=0.8))
        self.at("also called respiratory control")
        name2 = T("= respiratory control", 40, TEXT, font=TITLE_FONT).move_to([0, -0.5, 0])
        self.play(FadeIn(name2, shift=UP * 0.1), run_time=0.6)
        # "the cell's way of matching fuel burning to demand"
        self.at("the cell's way")
        self.play(FadeOut(name2), name1.animate.scale(0.55).move_to([0, 2.95, 0]), run_time=0.7)
        dem, fuel = ValueTracker(0.2), ValueTracker(0.2)
        bar_d = meter("ATP demand", GREEN, dem, 0, 1.2, w=5.0)
        bar_f = meter("fuel burning (O₂)", BLUE, fuel, 0, 0.1, w=5.0)
        # line the two tracks up
        bar_f.shift(RIGHT * (bar_d[0][1].get_left()[0] - bar_f[0][1].get_left()[0]))
        self.at("matching fuel burning")
        self.play(FadeIn(bar_d), FadeIn(bar_f), run_time=0.6)
        self.play(dem.animate.set_value(0.85), fuel.animate.set_value(0.85), run_time=0.8)
        self.at("to demand")
        self.play(dem.animate.set_value(0.35), fuel.animate.set_value(0.35), run_time=0.5)
        # "ADP is the signal for need."
        self.at("ADP is the signal")
        self.play(FadeOut(VGroup(bar_d, bar_f, name1)), run_time=0.5)
        self.remove(bar_d, bar_f)
        adp_c = chip("ADP", GOLD, 44).move_to([0, 0.2, 0])
        sig = T("the signal for need", 36, GOLD).next_to(adp_c, DOWN, buff=0.45)
        self.play(FadeIn(adp_c, scale=0.8), run_time=0.6)
        self.at("signal for need")
        self.play(FadeIn(sig, shift=UP * 0.1), run_time=0.6)
        # "When the cell has spent its ATP, the ADP it generates lifts the brake on the chain."
        self.at("When the cell has spent")
        self.play(FadeOut(sig), adp_c.animate.move_to([0, 0.5, 0]), run_time=0.6)
        spend = chip("cell spends ATP", GREEN, 30).move_to([-4.4, 0.5, 0])
        self.play(FadeIn(spend, shift=RIGHT * 0.2), run_time=0.6)
        self.at("the ADP it generates")
        a1 = Arrow(spend.get_right(), adp_c.get_left(), color=TEXT, buff=0.15, stroke_width=6)
        self.play(GrowArrow(a1), Indicate(adp_c, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.at("lifts the brake")
        ch = chip("chain", BLUE, 34).move_to([4.7, 0.5, 0])
        brk = Rectangle(width=0.14, height=0.95, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(
            ch.get_left() + LEFT * 0.12)
        a2 = Arrow(adp_c.get_right(), brk.get_left() + LEFT * 0.1, color=TEXT, buff=0.15, stroke_width=6)
        self.play(FadeIn(ch), FadeIn(brk), GrowArrow(a2), run_time=0.7)
        self.play(FadeOut(brk, shift=UP * 0.9), run_time=self.room("on the chain", lo=0.4))
        self.at("on the chain")
        fast = T("runs faster", 30, BLUE).next_to(ch, DOWN, buff=0.35)
        self.play(FadeIn(fast, shift=UP * 0.1), run_time=0.5)

        # ---------- part D: the take-home
        self.at("This is a clean example")
        self.play(FadeOut(Group(spend, a1, adp_c, a2, ch, fast)), run_time=0.6)
        l1 = T("metabolism governed by", 36, TEXT).move_to([0, 0.9, 0])
        l2 = T("energy charge", 64, GOLD, font=TITLE_FONT).move_to([0, -0.15, 0])
        l3 = T("rather than by substrate alone", 32, GREY).move_to([0, -1.3, 0])
        self.at("metabolism being")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.6)
        self.at("energy charge")
        self.play(Write(l2), run_time=0.8)
        self.at("rather than by substrate")
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s04: IF1 and reverse mode
class S04If1(Sp):
    def construct(self):
        mem = membrane()
        chain, synth = chain_block(), synth_block()
        g = ValueTracker(0.12)
        pool = Pool(g)
        pump_r, syn_r, atp_r, spin = (ValueTracker(0) for _ in range(4))
        pump, syn, atp = pumpstream(pump_r), synthstream(syn_r), atpstream(atp_r)
        spinner = Spinner(spin)
        o2v, atpv = ValueTracker(0.9), ValueTracker(0.85)
        m_o2 = meter("oxygen", BLUE, o2v, -3.1, 3.2)
        m_atp = meter("cell ATP", GREEN, atpv, 3.1, 3.2)

        def eq(txt, color):
            return T(txt, 28, color).move_to([SX, -2.95, 0])

        # "ATP synthase is reversible."
        self.add(pool, pump, syn, atp)
        self.play(FadeIn(mem), FadeIn(chain), FadeIn(synth), FadeIn(spinner), run_time=0.9)
        self.at("reversible")
        eq1 = eq("ADP + Pi   ⇄   ATP", TEXT)
        self.play(FadeIn(eq1, shift=UP * 0.1), run_time=0.7)
        # "During normal respiration, the proton gradient drives it forward to make ATP."
        self.at("During normal respiration")
        TAG_X, TAG_Y = -5.55, -1.8      # condition tag sits in the matrix under the chain, clear of the meters
        tag = T("normal respiration", 28, TEXT).move_to([TAG_X, TAG_Y, 0], aligned_edge=LEFT)
        pump_r.set_value(1)
        self.play(FadeIn(tag), FadeIn(m_o2), FadeIn(m_atp), g.animate.set_value(0.85),
                  run_time=self.room("the proton gradient drives", lo=1.0), rate_func=linear)
        self.at("the proton gradient drives")
        syn_r.set_value(1); spin.set_value(0.5)
        self.play(g.animate.set_value(0.6), Transform(eq1, eq("ADP + Pi   →   ATP", GREEN)),
                  run_time=self.room("to make ATP", lo=0.6), rate_func=smooth)
        self.at("to make ATP")
        atp_r.set_value(1)
        self.wait(self.room("But in ischemia", lo=0.3))

        # "But in ischemia or severe hypoxia, oxygen runs low"
        self.at("But in ischemia")
        tag2 = T("ischemia", 28, RED).move_to([TAG_X, TAG_Y, 0], aligned_edge=LEFT)
        self.play(Transform(tag, tag2), run_time=0.6)
        self.at("severe hypoxia")
        tag3 = T("ischemia / severe hypoxia", 28, RED).move_to([TAG_X, TAG_Y, 0], aligned_edge=LEFT)
        self.play(Transform(tag, tag3), o2v.animate.set_value(0.7), run_time=0.6)
        self.at("oxygen runs low")
        self.play(o2v.animate.set_value(0.08), run_time=self.room("the chain stalls", lo=0.8))
        # "the chain stalls, and the gradient collapses"
        self.at("the chain stalls")
        self.play(pump_r.animate.set_value(0), chain.animate.set_opacity(0.4), run_time=0.6)
        self.at("and the gradient collapses")
        self.play(g.animate.set_value(0.03), run_time=self.room("Now the enzyme", lo=1.0), rate_func=linear)
        self.play(syn_r.animate.set_value(0), spin.animate.set_value(0), atp_r.animate.set_value(0), run_time=0.01)
        # "Now the enzyme can spin backward"
        self.at("Now the enzyme can spin")
        self.play(spin.animate.set_value(-0.5), run_time=self.room("backward", lo=0.5))
        self.at("hydrolyzing")
        eq2 = eq("ATP   →   ADP + Pi", RED)
        atp_r.set_value(-1)
        self.play(Transform(eq1, eq2), run_time=0.6)
        self.play(atpv.animate.set_value(0.6), run_time=self.room("in a futile attempt", lo=0.6), rate_func=linear)
        # "in a futile attempt to rebuild the gradient"
        self.at("in a futile attempt")
        syn_r.set_value(-0.8)
        self.play(g.animate.set_value(0.2), atpv.animate.set_value(0.5), run_time=self.room("wasting precious", lo=0.8),
                  rate_func=linear)
        # "wasting precious energy exactly when it is scarcest"
        self.at("wasting precious energy")
        waste = T("wasting\nATP", 26, RED, line_spacing=0.8).move_to([5.3, -2.05, 0])
        self.play(FadeIn(waste), atpv.animate.set_value(0.32), run_time=self.room("The inhibitory factor", lo=1.0),
                  rate_func=linear)

        # "The inhibitory factor IF1 is the emergency brake."
        self.at("The inhibitory factor")
        if1 = chip("IF1", TEAL, 28).move_to([0.5, -1.45, 0])
        self.play(FadeIn(if1, shift=UP * 0.2), run_time=0.6)
        self.at("emergency brake")
        brake_lab = T("emergency brake", 24, TEAL).move_to([0.5, -2.15, 0])
        self.play(FadeIn(brake_lab), run_time=0.5)
        # "It binds at low pH, which marks oxygen deprivation"
        self.at("It binds at low pH")
        ph = T("low pH", 26, YELLOW).move_to([0.5, -0.82, 0])
        self.play(FadeIn(ph, shift=DOWN * 0.1), run_time=0.5)
        self.at("which marks oxygen deprivation")
        self.play(Indicate(tag, color=RED, scale_factor=1.1), run_time=0.8)
        # "and blocks the reverse rotation"
        self.at("and blocks the reverse")
        dock = [SX - 0.85 - 0.62, -1.2, 0]
        self.play(if1.animate.move_to(dock), FadeOut(ph), FadeOut(brake_lab), run_time=0.8)
        self.play(spin.animate.set_value(0), syn_r.animate.set_value(0), atp_r.animate.set_value(0),
                  FadeOut(waste), run_time=0.5)
        stop = T("blocked", 28, TEAL).move_to([0.5, -1.45, 0])
        self.at("reverse rotation")
        self.play(Transform(eq1, eq("ATP preserved", GREEN)), FadeIn(stop), run_time=0.5)
        # "protecting cellular ATP."
        self.at("protecting cellular ATP")
        self.play(Indicate(m_atp, color=GREEN, scale_factor=1.12), run_time=1.0)
        self.finish()
