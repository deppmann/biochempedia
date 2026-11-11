"""Touch in autism models, chapter 2: One Touch Behaviour, Several Routes.
Same colour map as chapter 1: GOLD sensory neuron, TEAL dorsal horn, BLUE brain, RED movement gauge.
"""
import numpy as np
from bp_style import *  # noqa

ORANGE = "#F29E4C"
PTS = [(-4.3, 0.0), (-2.9, 0.0), (0.4, 0.0), (1.8, 0.0), (3.3, 0.0), (4.6, 1.2)]
GY0, GH = -2.6, 2.4          # gauge bottom and height
GX = 5.4


def P(x, y):
    return np.array([x, y, 0.0])


def badge(color, at):
    return RoundedRectangle(corner_radius=0.06, width=0.34, height=0.34, stroke_color=TEXT, stroke_width=2,
                            fill_color=color, fill_opacity=0.95).move_to(P(*at))


class World:
    def __init__(s, scene, badges=("gold", "teal", "blue"), labels=(), gauge=0.35, pulse=True, gauge_lbl=True, gy0=GY0, gh=GH, gauge_on=True):
        s.gy0, s.gh = gy0, gh
        s.sc = scene
        s.t, s.g, s.bend = ValueTracker(0), ValueTracker(gauge), ValueTracker(0)
        s.pulse_on = pulse
        scene.add(s.t)
        s.t.add_updater(lambda m, dt: m.increment_value(dt))
        s.skin = RoundedRectangle(corner_radius=0.12, width=2.2, height=2.6, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.15).move_to(P(-5.4, -0.2))
        s.hairs = VGroup(*[Line(P(x, 1.1), P(x, 2.1), color=TEXT, stroke_width=5) for x in (-5.95, -5.4, -4.85)])
        s.cord = RoundedRectangle(corner_radius=0.14, width=3.6, height=2.6, stroke_color=TEAL, stroke_width=3,
                                  fill_color=TEAL, fill_opacity=0.12).move_to(P(1.5, 0))
        s.brain = RoundedRectangle(corner_radius=0.14, width=2.4, height=2.2, stroke_color=BLUE, stroke_width=3,
                                   fill_color=BLUE, fill_opacity=0.12).move_to(P(5.4, 1.6))
        s.link = DashedLine(P(3.3, 0.4), P(4.2, 1.0), color=GREY, stroke_width=4)
        axon = Line(P(-4.3, 0), P(0.4, 0), color=GOLD, stroke_width=6)
        stem = Line(P(-2.9, 0), P(-2.9, 0.6), color=GOLD, stroke_width=6)
        s.soma = Circle(radius=0.5, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.25).move_to(P(-2.9, 1.1))
        s.ending = Dot(P(-4.3, 0), radius=0.14, color=GOLD)
        s.term = Ellipse(width=0.8, height=0.55, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.35).move_to(P(0.4, 0))
        s.neuron = VGroup(axon, stem, s.soma, s.ending, s.term)
        s.gout = Rectangle(width=1.0, height=gh, stroke_color=GREY, stroke_width=3).move_to(P(GX, gy0 + gh / 2))
        s.gfill = Rectangle(width=0.94, height=0.1, stroke_width=0, fill_color=RED, fill_opacity=0.75)
        s.gauge = VGroup(s.gout, s.gfill)
        s.pulse = Dot(P(-4.3, 0), radius=0.15, color=WHITE).set_opacity(0)
        s.gold_b = VGroup(badge(GOLD, (-2.9, 1.1)), badge(GOLD, (0.4, 0)))
        s.teal_b = VGroup(badge(TEAL, (0.9, -0.8)), badge(TEAL, (1.9, 0.8)), badge(TEAL, (2.7, -0.6)))
        s.blue_b = VGroup(badge(BLUE, (4.8, 1.1)), badge(BLUE, (5.4, 1.5)), badge(BLUE, (6.0, 1.1)))
        s.lbl = {
            "neuron": T("sensory neuron", 28, GOLD).move_to(P(-0.9, 1.55)),
            "cord": T("dorsal horn", 28, TEAL).move_to(P(1.8, 1.75)),
            "brain": T("brain", 30, BLUE).move_to(P(5.4, 2.2)),
            "gauge": T("movement\nschematic", 24, RED, line_spacing=0.6).move_to(P(GX, gy0 - 0.6)),
        }
        parts = [s.skin, s.hairs, s.cord, s.brain, s.link, s.neuron, s.pulse]
        if gauge_on:
            parts.append(s.gauge)
        for b in badges:
            parts.append(getattr(s, b + "_b"))
        for k in labels:
            if k != "gauge" or gauge_lbl:
                parts.append(s.lbl[k])
        s.body = VGroup(*parts)
        s._set_gauge()

    def _set_gauge(s):
        h = max(0.03, s.gh * float(np.clip(s.g.get_value() + 0.012 * np.sin(3 * s.t.get_value()), 0, 1)))
        s.gfill.stretch_to_fit_height(h)
        s.gfill.move_to(P(GX, s.gy0 + h / 2 + 0.03))

    def start(s):
        t = s.t
        for i, h in enumerate(s.hairs):
            base = h.get_start()
            h.add_updater(lambda m, b=base, i=i: m.put_start_and_end_on(
                b, b + P(0.07 * np.sin(2.1 * t.get_value() + i) + 0.4 * s.bend.get_value(), 0.98 - 0.12 * s.bend.get_value())))
        s.gfill.add_updater(lambda m: s._set_gauge())
        cum = np.cumsum([0] + [np.hypot(PTS[i + 1][0] - PTS[i][0], PTS[i + 1][1] - PTS[i][1]) for i in range(len(PTS) - 1)])
        xs, ys = [p[0] for p in PTS], [p[1] for p in PTS]

        def pul(m):
            ph = (t.get_value() % 3.0) / 3.0
            if s.pulse_on and ph < 0.9:
                d = ph / 0.9 * cum[-1]
                m.move_to(P(np.interp(d, cum, xs), np.interp(d, cum, ys)))
                m.set_opacity(1)
            else:
                m.set_opacity(0)
        s.pulse.add_updater(pul)
        s.cord.add_updater(lambda m: m.set_fill(TEAL, opacity=0.12 + 0.05 * np.sin(1.3 * t.get_value())))
        s.brain.add_updater(lambda m: m.set_fill(BLUE, opacity=0.12 + 0.05 * np.sin(1.1 * t.get_value() + 1)))
        s.soma.add_updater(lambda m: m.set_fill(GOLD, opacity=0.25 + 0.1 * np.sin(1.7 * t.get_value())))

    def show(s):
        s.sc.add(s.body)
        s.start()

    def puff(s):
        return VGroup(*[Arrow(P(x, 3.4), P(x, 2.35), buff=0, color=TEXT, stroke_width=6, tip_length=0.22,
                              max_tip_length_to_length_ratio=0.4) for x in (-5.95, -5.4, -4.85)])



LILAC = "#B79CED"   # GABA-A route
PINK = "#E58FB0"    # Ih route


def pop(group, color):
    return AnimationGroup(*[Indicate(b, color=color, scale_factor=1.5) for b in group])


class Bar:
    """A gauge that fills inside its own box, tied to its own tracker."""
    def __init__(s, cx, cy, w, h, color, v=0.5, horizontal=False):
        s.v = ValueTracker(v)
        s.cx, s.cy, s.w, s.h, s.hor = cx, cy, w, h, horizontal
        s.box = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3).move_to(P(cx, cy))
        s.fill = Rectangle(stroke_width=0, fill_color=color, fill_opacity=0.8)
        s.grp = VGroup(s.box, s.fill)
        s.fill.add_updater(s._upd)
        s._upd(s.fill)

    def _upd(s, m):
        v = float(np.clip(s.v.get_value(), 0.02, 1))
        if s.hor:
            L = (s.w - 0.08) * v
            m.stretch_to_fit_width(L)
            m.stretch_to_fit_height(s.h - 0.08)
            m.move_to(P(s.cx - s.w / 2 + 0.04 + L / 2, s.cy))
        else:
            L = (s.h - 0.08) * v
            m.stretch_to_fit_width(s.w - 0.08)
            m.stretch_to_fit_height(L)
            m.move_to(P(s.cx, s.cy - s.h / 2 + 0.04 + L / 2))


def clock(scene):
    t = ValueTracker(0)
    scene.add(t)
    t.add_updater(lambda m, dt: m.increment_value(dt))
    return t


def left(scene, margin=0.15):
    return max(0.4, scene.narration_s + 0.3 - scene.elapsed() - margin)


def route_chips():
    c1 = chip("GABA-A route", LILAC, size=26).move_to(P(-4.2, -2.4))
    c2 = chip("Ih route", PINK, size=26).move_to(P(-1.2, -3.3))
    return c1, c2


# ---------------------------------------------------------------------------------------------
class S00LinkHook(SpokenScene):
    def construct(self):
        w = World(self, badges=(), gauge=0.1, pulse=True, labels=(), gauge_on=False)
        self.play(FadeIn(w.body), run_time=1.5)
        w.start()
        self.at("first touch neuron")
        self.play(Indicate(w.neuron, color=GOLD, scale_factor=1.04), run_time=1.4)
        self.at("several mice")
        bars, labs = [], []
        for i, x in enumerate((-4.4, 0.0, 4.4)):
            b = Bar(x + 0.5, -2.8, 2.6, 0.5, RED, v=0.05, horizontal=True)
            lb = T(f"mouse {i + 1}", 26, TEXT).move_to(P(x + 0.5, -3.45))
            bars.append(b)
            labs.append(lb)
        self.play(LaggedStart(*[FadeIn(VGroup(b.grp, lb)) for b, lb in zip(bars, labs)], lag_ratio=0.3), run_time=1.8)
        self.at("same puff")
        puff = w.puff()
        self.play(FadeIn(puff, shift=DOWN * 0.3), w.bend.animate.set_value(1), bars[0].v.animate.set_value(0.8),
                  bars[1].v.animate.set_value(0.78), bars[2].v.animate.set_value(0.82), run_time=1.2)
        self.play(FadeOut(puff), w.bend.animate.set_value(0), run_time=0.3)
        self.at("did the same circuit")
        qs = [T("?", 64, RED).move_to(P(x, y)) for x, y in ((-1.5, -0.9), (2.0, -0.45), (5.4, 1.4))]
        for i, q in enumerate(qs):
            q.add_updater(lambda m, i=i: m.set_opacity(0.75 + 0.25 * np.sin(2.2 * w.t.get_value() + i)))
        self.play(LaggedStart(*[FadeIn(q, scale=0.4) for q in qs], lag_ratio=0.3), run_time=2.0)
        self.at("gold sensory neuron")
        self.play(FadeIn(w.lbl["neuron"]), Indicate(w.neuron, color=GOLD, scale_factor=1.03), run_time=1.0)
        self.at("teal dorsal horn")
        self.play(FadeIn(w.lbl["cord"]), Indicate(w.cord, color=TEAL, scale_factor=1.03), run_time=0.9)
        self.at("blue brain")
        self.play(FadeIn(w.lbl["brain"]), Indicate(w.brain, color=BLUE, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S01GabaRoute(SpokenScene):
    def construct(self):
        t = clock(self)
        cx, cy, a, b = -2.6, 0.5, 2.1, 1.3
        border = RoundedRectangle(corner_radius=0.2, width=12.6, height=6.8, stroke_color=TEAL, stroke_width=4,
                                  fill_color=TEAL, fill_opacity=0.2).move_to(P(0, -0.1))
        axon = Line(P(-6.3, cy), P(cx - a, cy), color=GOLD, stroke_width=9)
        term = Ellipse(width=2 * a, height=2 * b, stroke_color=GOLD, stroke_width=5, fill_color=GOLD,
                       fill_opacity=0.3).move_to(P(cx, cy))
        term.add_updater(lambda m: m.set_fill(GOLD, opacity=0.28 + 0.08 * np.sin(1.7 * t.get_value())))
        pulse = Dot(radius=0.18, color=WHITE)

        def pul(m):
            ph = (t.get_value() % 2.4) / 2.4
            m.move_to(P(-6.3 + ph * (6.3 + cx - a), cy))
            m.set_opacity(1 if ph < 0.95 else 0)
        pulse.add_updater(pul)
        self.play(FadeIn(border), Create(axon), GrowFromCenter(term), run_time=0.9)
        self.add(pulse)
        self.at("gold neurons terminal")
        l1 = T("gold terminal", 30, GOLD).move_to(P(cx, 2.35))
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.7)
        self.at("teal dorsal horn")
        l2 = T("dorsal horn", 30, TEAL).move_to(P(-5.0, 3.0))
        self.play(FadeIn(l2, shift=DOWN * 0.1), run_time=0.7)
        # vesicles (release), shown from the start at a low rate
        rel = ValueTracker(0.25)
        ves = VGroup(*[Dot(radius=0.1, color=ORANGE) for _ in range(10)])
        for i, d in enumerate(ves):
            def mv(m, i=i):
                u = (t.get_value() * 0.55 + i / 10.0) % 1
                m.move_to(P(cx + a + 0.15 + u * 3.3, cy + 0.7 * np.sin(i * 2.1) + 0.15 * np.sin(3 * t.get_value() + i)))
                m.set_opacity(float(np.clip(rel.get_value() * 10 - i, 0, 1)) * (1 - 0.6 * u))
            d.add_updater(mv)
        self.add(ves)
        self.at("in mecp2")
        ang = [20, 60, 100, 140, -20, -60, -100, -140]
        blocks = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.44, height=0.44, stroke_color=TEXT, stroke_width=2,
                                           fill_color=LILAC, fill_opacity=0.95).move_to(
            P(cx + (a + 0.12) * np.cos(np.radians(d)), cy + (b + 0.12) * np.sin(np.radians(d)))) for d in ang])
        self.play(LaggedStart(*[FadeIn(bk, scale=0.3) for bk in blocks], lag_ratio=0.25), run_time=2.4)
        self.at("gabrb3")
        leg = T("GABA-A receptors", 28, LILAC).move_to(P(cx, -1.5))
        self.play(FadeIn(leg, shift=UP * 0.1), run_time=0.8)
        self.at("reduced")
        self.play(pop(blocks, LILAC), run_time=1.4)
        self.at("presynaptic inhibition")
        inh = T("presynaptic inhibition", 28, LILAC).move_to(P(cx, -2.15))
        self.play(FadeIn(inh, shift=UP * 0.1), run_time=0.9)
        self.at("receptor associated")
        gone = list(blocks)[3:] if False else [blocks[i] for i in (1, 2, 3, 4, 6)]
        self.play(LaggedStart(*[FadeOut(g, scale=0.3) for g in gone], lag_ratio=0.3),
                  inh.animate.set_opacity(0.4), run_time=2.2)
        self.at("afferent evoked")
        gb = Bar(5.2, 0.9, 0.9, 2.6, ORANGE, v=0.25)
        gl = T("release\nschematic", 24, ORANGE, line_spacing=0.6).move_to(P(5.2, -1.0))
        self.play(FadeIn(VGroup(gb.grp, gl)), gb.v.animate.set_value(0.9), rel.animate.set_value(0.95), run_time=1.5)
        # dorsal root potential trace, computed from a two-exponential shape
        amp = ValueTracker(0.95)
        x0, x1, yb = -0.2, 4.4, -2.75
        base = Line(P(x0, yb), P(x1, yb), color=GREY, stroke_width=3)
        trace = VMobject(color=RED, stroke_width=6)

        def draw(m):
            u = np.linspace(0, 1, 60)
            f = (np.exp(-4 * u) - np.exp(-14 * u)) / 0.4327
            pts = [P(x0 + 0.1 + ui * (x1 - x0 - 0.1), yb + 1.0 * amp.get_value() * fi) for ui, fi in zip(u, f)]
            m.set_points_as_corners(pts)
        trace.add_updater(draw)
        draw(trace)
        sweep = Dot(radius=0.12, color=WHITE)
        sweep.add_updater(lambda m: m.move_to(trace.point_from_proportion((t.get_value() % 2.5) / 2.5)))
        tl = T("dorsal root potential (schematic)", 24, RED).move_to(P(1.72, -1.5))
        self.play(FadeIn(VGroup(base, trace, tl)), run_time=0.5)
        self.add(sweep)
        self.at("dorsal root")
        self.play(amp.animate.set_value(0.3), run_time=1.2)
        lab = chip("authors' presynaptic-inhibition account", LILAC, size=28).move_to(P(0.3, -3.0))
        group = VGroup(gb.grp, gl, base, trace, tl, sweep, leg, inh)
        trace.clear_updaters()
        sweep.clear_updaters()
        self.play(ReplacementTransform(group, lab), FadeOut(ves), run_time=left(self))
        self.finish()


# ---------------------------------------------------------------------------------------------
def spikes(t, spacing, n=7):
    """Schematic spikes: little ticks travelling along the gold axon, closer together as spacing falls."""
    g = VGroup(*[Line(P(0, -0.3), P(0, 0.3), color=WHITE, stroke_width=5) for _ in range(n)])
    for i, tk in enumerate(g):
        def mv(m, i=i):
            sp = spacing.get_value()
            x = -4.3 + ((t.get_value() * 1.1 - i * sp) % 4.7)
            m.move_to(P(x, 0.0))
            m.set_opacity(1 if i * sp < 4.7 else 0)
        tk.add_updater(mv)
    return g


class S02ShankRoute(SpokenScene):
    def construct(self):
        w = World(self, badges=(), gauge=0.2, labels=(), pulse=False)
        self.play(FadeIn(w.body), run_time=1.0)
        w.start()
        rim = [(0.4 + 0.52 * np.cos(np.radians(d)), 0.38 * np.sin(np.radians(d))) for d in (30, 90, 150, 210, 270, 330)]
        blocks = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.2, height=0.2, stroke_color=TEXT, stroke_width=1.5,
                                           fill_color=LILAC, fill_opacity=0.95).move_to(P(x, y)) for x, y in rim])
        self.at("reset the pathway")
        self.play(LaggedStart(*[FadeIn(bk, scale=0.3) for bk in blocks], lag_ratio=0.2), run_time=1.5)
        self.at("that terminal")
        nc = T("no change", 30, LILAC).move_to(P(1.53, -0.75))
        self.play(FadeIn(nc), Indicate(blocks, color=LILAC, scale_factor=1.4), run_time=1.4)
        self.at("cultured large")
        self.play(FadeOut(nc), Indicate(w.neuron, color=GOLD, scale_factor=1.03), run_time=1.0)
        cl = T("cultured large sensory neurons", 28, GOLD).move_to(P(-2.2, 3.3))
        self.play(FadeIn(cl, shift=DOWN * 0.1), run_time=0.8)
        self.at("reduced ih")
        ih = Bar(-1.0, 1.5, 0.6, 1.8, PINK, v=0.85)
        il = T("Ih", 32, PINK).move_to(P(-1.0, 2.65))
        self.play(FadeIn(VGroup(ih.grp, il)), FadeOut(cl), ih.v.animate.set_value(0.3), run_time=1.6)
        self.at("greater excitability")
        sp = ValueTracker(1.2)
        sk = spikes(w.t, sp)
        self.play(FadeIn(sk), sp.animate.set_value(0.5), run_time=1.8)
        self.at("shank 3 model therefore")
        c1, c2 = route_chips()
        self.play(FadeIn(c1), FadeIn(c2), run_time=1.0)
        self.at("similar tactile")
        a1 = Arrow(c1.get_right(), P(4.85, -1.2), buff=0.1, color=LILAC, stroke_width=5)
        a2 = Arrow(c2.get_right(), P(4.85, -2.3), buff=0.1, color=PINK, stroke_width=5)
        gl = w.lbl["gauge"]
        gl.move_to(P(GX, -3.3))
        self.play(Create(a1), Create(a2), FadeIn(gl), w.g.animate.set_value(0.8), run_time=2.0)
        self.at("different measured")
        self.play(Indicate(c1, color=LILAC), Indicate(c2, color=PINK), run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03TwoRoutes(SpokenScene):
    def construct(self):
        t = clock(self)
        g = Bar(5.4, 0.4, 1.0, 4.8, RED, v=0.8)
        gl = T("mouse assay\nendpoint", 26, RED, line_spacing=0.6).move_to(P(5.4, -2.75))
        g.fill.add_updater(lambda m: m.set_opacity(0.75 + 0.1 * np.sin(2 * t.get_value())))
        self.play(FadeIn(g.grp), run_time=1.0)
        self.at("tactile endpoint")
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.8)
        c1, c2 = route_chips()
        self.at("different defects")
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.8)
        self.play(c1.animate.move_to(P(-4.4, 2.1)), c2.animate.move_to(P(-4.4, 0.4)), run_time=1.4)
        self.at("mecp2")
        b1 = Bar(-0.4, 2.1, 4.0, 0.5, LILAC, v=0.95, horizontal=True)
        t1 = T("GABA-A brake", 28, LILAC).move_to(P(-0.4, 2.7))
        self.play(FadeIn(VGroup(b1.grp, t1)), run_time=1.0)
        a1 = Arrow(P(1.75, 2.1), P(4.85, 2.0), buff=0.05, color=LILAC, stroke_width=5)
        self.play(Create(a1), run_time=0.8)
        self.at("reduced presynaptic")
        self.play(b1.v.animate.set_value(0.25), run_time=2.4)
        self.at("shank3 model")
        b2 = Bar(-0.4, 0.4, 4.0, 0.5, PINK, v=0.9, horizontal=True)
        t2 = T("Ih", 28, PINK).move_to(P(-0.4, 0.95))
        a2 = Arrow(P(1.75, 0.4), P(4.85, 0.4), buff=0.05, color=PINK, stroke_width=5)
        self.play(FadeIn(VGroup(b2.grp, t2)), Create(a2), run_time=1.0)
        self.at("reduced ih")
        self.play(b2.v.animate.set_value(0.25), run_time=1.6)
        self.at("greater sensory")
        sp = ValueTracker(1.2)
        n = 9
        ticks = VGroup(*[Line(P(0, -0.3), P(0, 0.3), color=WHITE, stroke_width=5) for _ in range(n)])
        for i, tk in enumerate(ticks):
            def mv(m, i=i):
                s = sp.get_value()
                m.move_to(P(-2.2 + ((t.get_value() * 0.9 - i * s) % 3.8), -1.2))
                m.set_opacity(1 if i * s < 3.8 else 0)
            tk.add_updater(mv)
        t3 = T("spike density", 28, TEXT).move_to(P(-4.4, -1.2))
        a3 = Arrow(P(1.75, -1.2), P(4.85, -0.9), buff=0.05, color=TEXT, stroke_width=5)
        self.play(FadeIn(VGroup(ticks, t3)), Create(a3), run_time=0.8)
        self.play(sp.animate.set_value(0.45), run_time=2.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
LANES = ["Gabrb3", "Mecp2", "Nlgn2", "Rorb"]
LY = [1.3, 0.2, -0.9, -2.0]
XP4, XAD, XL = -1.4, 4.2, -4.9
CURSOR_TOP, CURSOR_BOT = 1.9, -2.5


class Timeline:
    def __init__(s, scene, cursor_x):
        s.t = clock(scene)
        s.labels = VGroup(*[T(n, 34, TEXT).move_to(P(XL, y)) for n, y in zip(LANES, LY)])
        s.lines = VGroup(*[Line(P(XP4 + 0.5, y), P(XAD - 0.5, y), color=GREY, stroke_width=6) for y in LY])
        s.p4 = VGroup(*[Square(0.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to(P(XP4, y)) for y in LY])
        s.ad = VGroup(*[Square(0.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to(P(XAD, y)) for y in LY])
        s.hdr = VGroup(T("P4", 34, TEXT).move_to(P(XP4, 2.15)), T("adult", 34, TEXT).move_to(P(XAD, 2.15)))
        s.marks = VGroup(*[Dot(P(XAD, y), radius=0.26, color=RED) for y in LY])
        for i, m in enumerate(s.marks):
            m.add_updater(lambda mm, i=i: mm.set_fill(RED, opacity=0.6 + 0.4 * np.sin(2.0 * s.t.get_value() + i)))
        s.bands = VGroup(*[Rectangle(width=12.6, height=1.0, stroke_width=0, fill_color=GREY, fill_opacity=0.2).move_to(P(0, y)) for y in LY])
        s.runners = VGroup(*[Dot(radius=0.2, color=TEAL) for _ in LY])
        for i, d in enumerate(s.runners):
            d.add_updater(lambda m, i=i: m.move_to(P(XP4 + 0.55 + ((0.22 + 0.04 * i) * s.t.get_value() + 0.25 * i) % 1 * (XAD - XP4 - 1.1), LY[i])))
        s.qs = VGroup(*[T("?", 40, GREY).move_to(P(XP4, y)) for y in LY])
        s.cx = ValueTracker(cursor_x)
        scene.add(s.cx)
        s.cursor = DashedLine(P(0, CURSOR_TOP), P(0, CURSOR_BOT), color=TEXT, stroke_width=4)
        s.cursor.add_updater(lambda m: m.move_to(P(s.cx.get_value(), (CURSOR_TOP + CURSOR_BOT) / 2)))
        s.cursor.move_to(P(cursor_x, (CURSOR_TOP + CURSOR_BOT) / 2))
        s.cx.add_updater(lambda m, dt: m.increment_value(0.16 * dt) if m.get_value() < XAD - 0.8 else None)

    def base(s):
        return VGroup(s.bands, s.labels, s.lines, s.p4, s.ad, s.hdr, s.runners)


QTEXT = "Must every adult phenotype already be present at P4?"


class S04Predict(SpokenScene):
    def construct(self):
        t = clock(self)
        mech = T("mechanism", 36, TEXT).move_to(P(-5.0, 3.2))
        c1 = chip("GABA-A route", LILAC, size=28).move_to(P(-1.6, 3.2))
        c2 = chip("Ih route", PINK, size=28).move_to(P(2.0, 3.2))
        c1.add_updater(lambda m: m.set_stroke(LILAC, 2.5 + 1.2 * np.sin(2 * t.get_value())))
        self.play(FadeIn(mech), run_time=0.8)
        self.play(FadeIn(c1), FadeIn(c2), run_time=1.0)
        self.at("slide a timeline")
        tl = Timeline(self, XP4)
        self.add(tl.runners)
        self.play(Create(tl.lines), FadeIn(tl.bands), run_time=1.2)
        self.at("four mouse model lanes")
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in tl.labels], lag_ratio=0.3), run_time=1.6)
        self.at("postnatal day four")
        self.add(tl.cursor)
        self.play(FadeIn(tl.p4), FadeIn(tl.hdr[0]), tl.cx.animate.set_value(-1.0), run_time=1.2)
        self.at("adult testing")
        self.play(FadeIn(tl.ad), FadeIn(tl.hdr[1]), tl.cx.animate.set_value(-0.6), run_time=1.2)
        self.at("every lane later")
        self.play(LaggedStart(*[FadeIn(m, scale=0.3) for m in tl.marks], lag_ratio=0.3),
                  FadeOut(VGroup(mech, c1, c2)), tl.cx.animate.set_value(-0.1), run_time=2.4)
        self.at("must every adult")
        q = T(QTEXT, 32, TEXT).move_to(P(0, -3.3))
        self.play(FadeIn(q, shift=UP * 0.1), tl.cx.animate.set_value(0.2), run_time=1.0)
        self.at("postnatal day four", nth=1)
        self.play(LaggedStart(*[FadeIn(x, scale=0.4) for x in tl.qs], lag_ratio=0.2),
                  tl.cx.animate.set_value(0.4), run_time=left(self))
        self.finish()


class S05Pause(NarratedScene):
    def construct(self):
        tl = Timeline(self, 0.4)
        q = T(QTEXT, 32, TEXT).move_to(P(0, -3.3))
        self.add(tl.base(), tl.marks, tl.qs, tl.cursor, q)
        self.play(tl.cx.animate.set_value(1.6), run_time=self.narration_s, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06TimingReveal(SpokenScene):
    def construct(self):
        tl = Timeline(self, 1.6)
        self.add(tl.base(), tl.marks, tl.qs, tl.cursor)
        self.at("and mecp")
        self.play(Indicate(tl.labels[0], color=RED), Indicate(tl.labels[1], color=RED), run_time=1.2)
        self.at("already more reactive")
        red4 = VGroup(*[Dot(P(XP4, LY[i]), radius=0.26, color=RED) for i in (0, 1)])
        self.play(FadeOut(VGroup(tl.qs[0], tl.qs[1])), LaggedStart(*[FadeIn(d, scale=0.3) for d in red4], lag_ratio=0.4),
                  run_time=1.4)
        self.at("and rorb")
        self.play(Indicate(tl.labels[2], color=GREY), Indicate(tl.labels[3], color=GREY), run_time=1.2)
        self.at("were not")
        neutral = VGroup(*[Dot(P(XP4, LY[i]), radius=0.12, color=GREY) for i in (2, 3)])
        self.play(FadeOut(VGroup(tl.qs[2], tl.qs[3])), FadeIn(neutral), run_time=1.0)
        self.at("tactile abnormalities")
        self.play(tl.cx.animate.set_value(XAD), run_time=1.6)
        self.play(Indicate(VGroup(tl.marks[2], tl.marks[3]), color=RED, scale_factor=1.6), run_time=1.2)
        self.at("two sampled ages")
        br = BraceBetweenPoints(P(XP4 - 0.4, -2.55), P(XAD + 0.4, -2.55), direction=DOWN, color=TEXT)
        self.play(GrowFromCenter(br), Indicate(tl.p4, color=TEXT, scale_factor=1.05),
                  Indicate(tl.ad, color=TEXT, scale_factor=1.05), run_time=1.6)
        self.at("identify the onset")
        lab = T("onset day unknown", 32, TEXT).move_to(P(1.4, -3.35))
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07SpinalLocus(SpokenScene):
    def construct(self):
        w = World(self, badges=("gold", "teal", "blue"), gauge=0.2, labels=("gauge",), pulse=True)
        self.play(FadeIn(w.body), run_time=1.5)
        w.start()
        self.at("locus")
        self.play(Indicate(w.cord, color=TEAL, scale_factor=1.03), run_time=1.2)
        self.at("deleting it")
        chp = chip("Nlgn2", TEAL, size=30).move_to(P(1.5, 3.1))
        self.play(FadeIn(chp, shift=DOWN * 0.2), run_time=0.8)
        self.at("dorsal horn neurons")
        self.play(chp.animate.move_to(P(1.5, 1.9)), run_time=1.0)
        self.at("sufficient for")
        self.play(LaggedStart(*[FadeOut(b, scale=0.3) for b in w.teal_b], lag_ratio=0.3), run_time=1.5)
        self.at("adult tactile")
        self.play(FadeOut(chp), w.g.animate.set_value(0.85), run_time=2.0)
        self.at("teal spinal block")
        cordgrp = VGroup(w.cord)
        self.play(cordgrp.animate.scale(1.25), run_time=1.4)
        self.at("gold afferent")
        self.play(w.neuron.animate.set_opacity(0.3), w.gold_b.animate.set_opacity(0.3), run_time=1.2)
        self.at("across these models")
        er = chip("early reactivity", GREY, size=28).move_to(P(-4.6, -2.9))
        self.play(FadeIn(er), run_time=0.8)
        self.at("tracked selected")
        lt = chip("later behaviors", ORANGE, size=28).move_to(P(1.2, -2.9))
        ar = DashedLine(er.get_right() + RIGHT * 0.1, lt.get_left() + LEFT * 0.1, color=TEXT, stroke_width=5)
        ar.add_tip(tip_length=0.25)
        self.play(Create(ar), FadeIn(lt), run_time=1.5)
        self.at("that association")
        nc = T("association, not causation", 30, TEXT).move_to(P(-1.6, -2.15))
        self.play(FadeIn(nc, shift=UP * 0.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Takeaway(SpokenScene):
    def construct(self):
        t = clock(self)
        ys = (2.4, 0.3, -1.9)
        names = ("locus", "mechanism", "timing")
        labs = [T(n, 32, TEXT).move_to(P(-6.0, y)).align_to(P(-6.2, 0), LEFT) for n, y in zip(names, ys)]
        # row 1: location blocks with a moving spotlight
        g_b = RoundedRectangle(corner_radius=0.12, width=2.6, height=1.0, stroke_color=GOLD, fill_color=GOLD, fill_opacity=0.4,
                               stroke_width=4).move_to(P(-2.0, ys[0]))
        t_b = RoundedRectangle(corner_radius=0.12, width=2.6, height=1.0, stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.4,
                               stroke_width=4).move_to(P(1.2, ys[0]))
        gt = T("sensory", 26, GOLD).move_to(g_b)
        tt = T("dorsal horn", 26, TEAL).move_to(t_b)
        spot = RoundedRectangle(corner_radius=0.14, width=2.9, height=1.3, stroke_color=WHITE, stroke_width=6)
        spot.add_updater(lambda m: m.move_to(P(-0.4 + 1.6 * np.sign(np.sin(0.9 * t.get_value())), ys[0])))
        # row 2: mechanism fork
        m1 = chip("GABA-A", LILAC, size=28).move_to(P(-2.0, ys[1]))
        m2 = chip("Ih", PINK, size=28).move_to(P(1.2, ys[1]))
        fork = RoundedRectangle(corner_radius=0.14, width=2.9, height=1.2, stroke_color=WHITE, stroke_width=6)
        fork.add_updater(lambda m: m.move_to(P(-0.4 + 1.6 * np.sign(np.sin(0.7 * t.get_value() + 1)), ys[1])))
        # row 3: timeline cursor
        tline = Line(P(-3.2, ys[2]), P(2.6, ys[2]), color=GREY, stroke_width=5)
        p4 = T("P4", 28, TEXT).move_to(P(-3.2, ys[2] - 0.6))
        ad = T("adult", 28, TEXT).move_to(P(2.6, ys[2] - 0.6))
        cur = Dot(radius=0.24, color=TEXT)
        cur.add_updater(lambda m: m.move_to(P(-3.2 + 5.8 * ((t.get_value() * 0.15) % 1), ys[2])))
        g = Bar(5.4, 0.0, 1.0, 5.0, RED, v=0.2)
        gl = T("mouse assay", 26, RED).move_to(P(5.4, -3.2))
        self.at("locus")
        self.play(FadeIn(labs[0]), FadeIn(VGroup(g_b, t_b, gt, tt)), FadeIn(spot), run_time=1.0)
        self.at("mechanism")
        self.play(FadeIn(labs[1]), FadeIn(VGroup(m1, m2)), FadeIn(fork), run_time=0.9)
        self.at("developmental timing")
        self.add(cur)
        self.play(FadeIn(labs[2]), FadeIn(VGroup(tline, p4, ad)), run_time=1.0)
        self.at("a shared mouse")
        arrows = VGroup(*[Arrow(P(2.7, y), P(4.85, 0.0 + 0.5 * (y - 0.3) / 2), buff=0.05, color=GREY, stroke_width=5)
                          for y in ys])
        self.play(FadeIn(VGroup(g.grp, gl)), Create(arrows), run_time=1.2)
        self.play(g.v.animate.set_value(0.8), run_time=1.8)
        self.at("conditional genetics")
        self.play(FadeOut(arrows), Indicate(VGroup(g_b, t_b), color=WHITE, scale_factor=1.06), run_time=1.5)
        self.at("physiology tests")
        self.play(Indicate(VGroup(m1, m2), color=WHITE, scale_factor=1.12), run_time=1.5)
        self.at("measurements at different")
        self.play(Indicate(VGroup(tline, p4, ad), color=WHITE, scale_factor=1.05), run_time=1.5)
        self.at("without turning")
        self.play(Indicate(g.grp, color=RED, scale_factor=1.04), run_time=1.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Limits(SpokenScene):
    def construct(self):
        w = World(self, badges=("gold", "teal", "blue"), gauge=0.2, labels=(), pulse=True, gy0=-1.7, gh=1.5)
        self.play(FadeIn(w.body), run_time=1.5)
        w.start()
        self.at("one endpoint")
        self.play(Indicate(w.gout, color=RED, scale_factor=1.08), run_time=1.2)
        self.at("air puff movement")
        puff = w.puff()
        self.play(FadeIn(puff, shift=DOWN * 0.3), w.bend.animate.set_value(1), w.g.animate.set_value(0.8), run_time=1.4)
        self.play(FadeOut(puff), w.bend.animate.set_value(0), run_time=0.6)
        self.at("mouse development")
        ta = Arrow(P(-3.4, -0.55), P(-3.4, -2.3), buff=0, color=TEXT, stroke_width=6)
        tl = T("P4 to adult", 28, TEXT).move_to(P(-1.9, -1.6))
        self.play(GrowArrow(ta), FadeIn(tl), run_time=1.6)
        self.at("human window")
        bd = DashedLine(P(-6.6, -2.4), P(6.6, -2.4), color=GREY, stroke_width=4)
        hx, hy = -4.6, -3.05
        human = VGroup(Circle(radius=0.2, color=TEXT, stroke_width=4).move_to(P(hx, hy + 0.5)),
                       Line(P(hx, hy + 0.3), P(hx, hy - 0.25), color=TEXT, stroke_width=4),
                       Line(P(hx - 0.3, hy + 0.15), P(hx + 0.3, hy + 0.15), color=TEXT, stroke_width=4),
                       Line(P(hx, hy - 0.25), P(hx - 0.22, hy - 0.7), color=TEXT, stroke_width=4),
                       Line(P(hx, hy - 0.25), P(hx + 0.22, hy - 0.7), color=TEXT, stroke_width=4))
        self.play(Create(bd), FadeIn(human), run_time=1.4)
        self.at("translation questions")
        fr = DashedRectangle if False else RoundedRectangle(corner_radius=0.12, width=6.2, height=1.1, stroke_color=GREY, stroke_width=4)
        fr.move_to(P(0.8, -3.1))
        nl = T("new evidence needed", 30, TEXT).move_to(fr)
        self.play(Create(fr), FadeIn(nl), run_time=1.4)
        self.at("own measurements")
        self.play(Indicate(fr, color=TEXT, scale_factor=1.03), Indicate(w.gout, color=RED, scale_factor=1.06), run_time=1.4)
        self.finish()


class S10End(EndCard):
    LINE = "Test locus, mechanism and timing separately."
