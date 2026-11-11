"""How to Prove a Gut Synapse  (Biochemistrypedia explainer for gut-brain-sensing)

COLOR MAP (one colour per concept, whole film)
  GOLD  = enteroendocrine sensor cell        BLUE = vagal neuron / axon / firing
  TEAL  = glutamate / the synapse            GREY = diffuse hormone route
  WHITE (TEXT) = unidentified or unanswered  GREEN = active / restored result
  RED   = blocked or silenced result
Every curve is computed: the current is I(t) = -A * (exp(-(t-60)/260) - exp(-(t-60)/45)) after a
60 ms onset (schematic shape, drawn from that equation); rasters thin a fixed random grid by a rate.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

_ic = interpolate_color


def interpolate_color(a, b, t):
    return _ic(ManimColor(a), ManimColor(b), t)

WHITE = TEXT
PI_ = np.pi
V = lambda x, y: np.array([x, y, 0.0])

# --------------------------------------------------------------------------- the carried gut world
CELL_C = V(-3.0, 0.75)
PROC_FULL = CubicBezier(V(-3.0, -0.4), V(-3.0, -1.6), V(-1.8, -2.0), V(-0.45, -2.0))
AXON_FULL = CubicBezier(V(0.0, -2.0), V(1.8, -2.0), V(3.0, -0.6), V(6.8, -0.6))
PROC_END, AXON_START = V(-0.45, -2.0), V(0.0, -2.0)
CONTACT = V(-0.225, -2.0)
SMALL_S, SMALL_SH = 0.55, V(-3.1, 1.0)


def hl(m, c, w, op=1.0):
    m.set_stroke(c, w, opacity=op)
    return m


def proc_mob(reach=1.0):
    p = PROC_FULL.copy().pointwise_become_partial(PROC_FULL, 0, reach)
    return hl(p, GOLD, 9)


def route_pt(a):
    """tracer path: down the process, across the contact, along the axon to the right."""
    if a < 0.45:
        return PROC_FULL.point_from_proportion(a / 0.45)
    if a < 0.5:
        return PROC_END + (AXON_START - PROC_END) * ((a - 0.45) / 0.05)
    return AXON_FULL.point_from_proportion((a - 0.5) / 0.5)


def drift_dots(n, x0, x1, y0, y1, color=GREY, seed=1, r=0.07, speed=1.0):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=r, color=color).move_to([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
        d.v = np.array([rng.uniform(0.3, 0.7) * speed * (1 if rng.rand() > 0.3 else -1), rng.uniform(-0.2, 0.2), 0])

        def up(m, dt, x0=x0, x1=x1, y0=y0, y1=y1):
            m.shift(m.v * dt)
            p = m.get_center()
            if p[0] > x1:
                m.move_to([x0, p[1], 0])
            if p[0] < x0:
                m.move_to([x1, p[1], 0])
            if p[1] > y1 or p[1] < y0:
                m.v[1] *= -1
                m.shift(np.array([0, m.v[1] * dt * 2, 0]))
        d.add_updater(up)
        g.add(d)
    return g


def travelers(path, n=4, color=BLUE, speed=0.16, r=0.09):
    """dots that keep running along a path (ambient motion that means something)."""
    g = VGroup()
    for i in range(n):
        d = Dot(radius=r, color=color)
        d.t = i / n
        d.move_to(path.point_from_proportion(d.t))

        def up(m, dt, path=path, speed=speed):
            m.t = (m.t + dt * speed) % 1
            m.move_to(path.point_from_proportion(m.t))
        d.add_updater(up)
        g.add(d)
    return g


def pulse_ring(center, r=0.45, color=WHITE):
    ring = Circle(radius=r, color=color, stroke_width=4).move_to(center)
    ring.t = 0.0

    def up(m, dt):
        m.t += dt
        m.set_stroke(opacity=0.45 + 0.4 * np.sin(m.t * 4))
    ring.add_updater(up)
    return ring


def world(reach=1.0, labels=True, lumen_dots=True, seed=3):
    """cross-section: lumen above, epithelial sheet, tissue below; sensor cell + vagal axon."""
    W = {}
    lumen = Rectangle(width=13.2, height=1.9, stroke_width=0, fill_color=TEAL, fill_opacity=0.22).move_to([0, 2.85, 0])
    tissue = Rectangle(width=13.2, height=3.4, stroke_width=0, fill_color=GREY, fill_opacity=0.24).move_to([0, -2.1, 0])
    neigh = VGroup(*[RoundedRectangle(width=1.7, height=2.3, corner_radius=0.3, stroke_color=GREY, stroke_width=2,
                                      fill_color=GREY, fill_opacity=0.32).move_to([x, 0.75, 0]) for x in (-4.85, -1.15, 0.7, 2.55, 4.4)])
    W["epi"] = VGroup(lumen, tissue, neigh)
    W["cell"] = RoundedRectangle(width=1.7, height=2.3, corner_radius=0.3, stroke_color=GOLD, stroke_width=5,
                                 fill_color=GOLD, fill_opacity=0.35).move_to(CELL_C)
    W["cell"].t = 0.0
    W["cell"].add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_fill(GOLD, 0.35 + 0.12 * np.sin(m.t * 2.5))))
    W["proc"] = proc_mob(reach)
    W["axon"] = hl(AXON_FULL.copy(), BLUE, 14)
    W["bulb"] = Dot(AXON_START, radius=0.2, color=BLUE)
    if lumen_dots:
        W["dots"] = drift_dots(8, -6.5, 6.5, 2.05, 2.75, GREY, seed)
    W["trav"] = travelers(AXON_FULL, 5, BLUE, 0.14, 0.13)
    if labels:
        W["lab_cell"] = T("gut cell", 28, GOLD).move_to([-4.9, -0.95, 0])
        W["lab_axon"] = T("vagal axon", 28, BLUE).move_to([5.2, -1.45, 0])
    return W


def small_world(w, extra=()):
    g = VGroup(w["epi"], w["cell"], w["proc"], w["axon"], w["bulb"], *extra)
    g.scale(SMALL_S, about_point=ORIGIN).shift(SMALL_SH)
    return g


def new_ring():
    return pulse_ring(CONTACT, 0.45, WHITE)


# --------------------------------------------------------------------------- current plot
AXC = V(3.65, -1.05)
XL, YL = 5.2, 3.5
AX = Axes(x_range=[0, 1000, 250], y_range=[-1.6, 0.4, 0.5], x_length=XL, y_length=YL,
          axis_config={"stroke_opacity": 0, "include_ticks": False}, tips=False).move_to(AXC)


def shape(t):
    u = t - 60.0
    return 0.0 if u <= 0 else (np.exp(-u / 260.0) - np.exp(-u / 45.0)) / 0.573


def cur(t, amp, ph):
    return -amp * shape(t) + 0.05 * np.sin(t / 38.0 + ph * 6.0) * (0.6 + 0.4 * np.sin(t / 130.0 - ph * 2.0))


def plot_frame(with_label=True):
    p = AX.c2p
    left = Line(p(0, -1.6), p(0, 0.4), color=TEXT, stroke_width=3)
    bottom = Line(p(0, -1.6), p(1000, -1.6), color=TEXT, stroke_width=3)
    ticks = VGroup(*[Line(p(t, -1.6), p(t, -1.5), color=TEXT, stroke_width=3) for t in (0, 250, 500, 750, 1000)])
    nums = VGroup(*[M(s, 24).move_to(p(t, -1.6) + DOWN * 0.3) for t, s in ((0, "0"), (500, "500"), (1000, "1000 ms"))])
    nums[2].shift(LEFT * 0.25)
    g = VGroup(left, bottom, ticks, nums)
    if with_label:
        g.add(T("current", 28).move_to(p(0, 0.4) + UP * 0.28 + RIGHT * 0.6))
    return g


def make_trace(amp, sweep, ph, colorfn):
    def build():
        s = max(sweep.get_value(), 0.03) * 1000
        a, pp = amp.get_value(), ph.get_value()
        g = AX.plot(lambda t: cur(t, a, pp), x_range=[0, s, s / 120], color=colorfn(a), stroke_width=6, use_smoothing=False)
        head = Dot(AX.c2p(s, cur(s, a, pp)), radius=0.1, color=colorfn(a))
        return VGroup(g, head)
    return always_redraw(build)


class Base(SpokenScene):
    def clock(self):
        self.ph = ValueTracker(0.0)
        self.ph.add_updater(lambda m, dt: m.increment_value(dt * 1.5))
        self.add(self.ph)

    def plot(self, amp=0.0, sweep=1.0, colorfn=None, with_label=True):
        self.amp, self.sweep = ValueTracker(amp), ValueTracker(sweep)
        colorfn = colorfn or (lambda a: interpolate_color(WHITE, GREEN, min(1.0, a * 3)))
        self.frame = plot_frame(with_label)
        self.trace = make_trace(self.amp, self.sweep, self.ph, colorfn)
        return self.frame, self.trace


def fly(d, f):
    return UpdateFromAlphaFunc(d, lambda m, a: m.move_to(f(a)))


def recolor(c, color):
    c[0].set_stroke(color)
    c[0].set_fill(interpolate_color(BG, color, 0.2), opacity=1)
    c[1].set_color(color)
    return c


def pop(self, *mobs, rt=1.0):
    self.play(*[m.animate.scale(1.15) for m in mobs], rate_func=there_and_back, run_time=rt)


def solid_chip(text, color=TEXT, size=28, pad=0.22):
    c = chip(text, color, size, pad)
    c[0].set_fill(interpolate_color(BG, color, 0.2), opacity=1)
    return c


# --------------------------------------------------------------------------- the dish
DISH_C = V(-3.5, -1.2)
CELL_D = V(-4.2, 0.3)
TIP_D = V(-3.6, -1.05)
KNOB_C = V(-3.6, -2.65)
PROC_D = CubicBezier(V(-4.2, -0.45), V(-4.2, -0.9), V(-3.6, -0.7), TIP_D)
AXON_D = CubicBezier(V(-2.3, -2.65), V(-1.5, -2.65), V(-1.3, -2.2), V(-1.15, -1.8))
BLOCK_X = (-4.3, -3.6, -2.9)


def dish(blocks=False):
    D = {}
    D["out"] = RoundedRectangle(width=6.4, height=5.1, corner_radius=0.9, stroke_color=TEXT, stroke_width=4,
                                fill_color=TEAL, fill_opacity=0.2).move_to(DISH_C)
    D["cell"] = RoundedRectangle(width=1.7, height=1.5, corner_radius=0.3, stroke_color=GOLD, stroke_width=5,
                                 fill_color=GOLD, fill_opacity=0.35).move_to(CELL_D)
    D["proc"] = hl(PROC_D.copy(), GOLD, 9)
    D["knob"] = Ellipse(width=2.8, height=1.1, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to(KNOB_C)
    D["axon"] = hl(AXON_D.copy(), BLUE, 12)
    D["soma"] = Circle(radius=0.6, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to([-1.1, -1.4, 0])
    D["lab_cell"] = T("gut cell", 28, GOLD).move_to([-2.5, 0.5, 0])
    D["lab_n"] = T("nodose neuron", 28, BLUE).move_to([-1.85, -0.1, 0])
    D["body"] = VGroup(D["cell"], D["proc"], D["knob"], D["axon"], D["soma"])
    if blocks:
        D["blocks"] = receptors()
    return D


def receptors():
    sq = Square(0.34, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8).move_to([BLOCK_X[0], -2.05, 0])
    tr = Triangle(stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8).scale(0.22).rotate(PI_).move_to([BLOCK_X[1], -2.05, 0])
    pe = RegularPolygon(5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.8).scale(0.2).move_to([BLOCK_X[2], -2.05, 0])
    return VGroup(sq, tr, pe)


def crossing_dots(n=3, color=WHITE, speed=0.5, r=0.1, target_y=-1.85, xs=None):
    """messenger dots hopping from the cell's process tip to the receptors (looping)."""
    g = VGroup()
    xs = xs or BLOCK_X
    for i in range(n):
        d = Dot(radius=r, color=color)
        d.t = i / n
        d.x = xs[i % len(xs)]

        def up(m, dt, speed=speed, ty=target_y):
            m.t = (m.t + dt * speed) % 1
            a = m.t
            m.move_to(TIP_D + (V(m.x, ty) - TIP_D) * a)
            m.set_opacity(min(1, a * 6, (1 - a) * 6 + 0.0) if a > 0.85 else min(1, a * 6))
        d.add_updater(up)
        g.add(d)
    return g


def stopped_dots(color=TEAL, stop_y=-1.62, speed=0.5, r=0.1):
    g = VGroup()
    for i in range(3):
        d = Dot(radius=r, color=color)
        d.t = i / 3
        d.x = BLOCK_X[i]

        def up(m, dt, speed=speed, sy=stop_y):
            m.t = (m.t + dt * speed * 0.7) % 1
            y = TIP_D[1] + (sy - TIP_D[1]) * min(1.0, m.t / 0.8)
            m.move_to([TIP_D[0] + (m.x - TIP_D[0]) * min(1.0, m.t / 0.8), y, 0])
            m.set_opacity(1 if m.t < 0.8 else 0.9)
        d.add_updater(up)
        g.add(d)
    return g


def shimmer(ph, n=2):
    out = VGroup()
    for k in range(n):
        out.add(always_redraw(lambda k=k: FunctionGraph(
            lambda x: 0.07 * np.sin(2.4 * x + ph.get_value() * 2.0 + k), x_range=[-1.7, -0.5, 0.1],
            color=TEAL, stroke_width=3, stroke_opacity=0.5).shift(DOWN * (3.55 + 0.12 * k))))
    return out


# --------------------------------------------------------------------------- raster
def raster(center, w, h, rate, ph, rows=4, seed=5, color=BLUE):
    rng = np.random.RandomState(seed)
    U = rng.rand(rows, 50)

    def build():
        r = rate.get_value()
        m = VMobject().set_stroke(color, 4)
        any_ = False
        for i in range(rows):
            y = center[1] + h / 2 - (i + 0.5) * h / rows
            for k in range(50):
                if U[i, k] < r * 0.08:
                    x = ((k * 0.08 - ph.get_value() * 0.5) % 4.0) / 4.0
                    xx = center[0] - w / 2 + 0.1 + x * (w - 0.2)
                    m.start_new_path(V(xx, y - h / rows * 0.32))
                    m.add_line_to(V(xx, y + h / rows * 0.32))
                    any_ = True
        if not any_:
            m.start_new_path(V(center[0] - w / 2, y))
            m.add_line_to(V(center[0] - w / 2, y))
        return m
    return always_redraw(build)


# =========================================================================== scenes
class S00Hook(Base):
    def construct(self):
        self.clock()
        w = world(0.72, labels=False)
        tip = PROC_FULL.point_from_proportion(0.72)
        qm = T("?", 56, WHITE).move_to((tip + AXON_START) / 2 + UP * 0.42)
        qm.t = 0.0

        def qup(m, dt):
            m.t += dt
            m.set_opacity(0.55 + 0.45 * np.sin(m.t * 4))
        qm.add_updater(qup)
        q = T("How does this cell reach the nerve?", 36, TEXT).move_to([0, 3.3, 0])
        self.add(w["dots"])
        self.play(FadeIn(w["epi"]), GrowFromCenter(w["cell"]), run_time=1.0)
        self.at("is not a neuron")
        self.play(Indicate(w["cell"], color=GOLD, scale_factor=1.08), run_time=1.2)
        self.at("How could it")
        self.play(Write(q), Create(w["axon"]), FadeIn(w["bulb"]), run_time=1.2)
        self.add(w["trav"])
        self.play(Create(w["proc"]), run_time=1.0)
        self.add(qm)
        lab_c = T("gut cell", 28, GOLD).move_to([-4.9, -0.95, 0])
        lab_a = T("vagal axon", 28, BLUE).move_to([5.2, -1.45, 0])
        self.at("a vagal sensory")
        self.play(FadeIn(lab_c), FadeIn(lab_a), run_time=0.8)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Sensing the Gut: Enteroendocrine Cells and Nutrient Signals"
    TITLE = "How to Prove a Gut Synapse"


class S02Routes(Base):
    def construct(self):
        self.clock()
        w = world(0.72, labels=False)
        tip = PROC_FULL.point_from_proportion(0.72)
        qm = T("?", 56, WHITE).move_to((tip + AXON_START) / 2 + UP * 0.42)
        qm.t = 0.0
        qm.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_opacity(0.55 + 0.45 * np.sin(m.t * 4))))
        self.add(*[w[k] for k in ("epi", "cell", "proc", "axon", "bulb", "dots", "trav")], qm)
        # hormone puff: grey dots fanning out through the tissue
        rng = np.random.RandomState(9)
        puff = VGroup()
        for i in range(16):
            d = Dot(radius=0.075, color=GREY)
            d.a = rng.uniform(-2.9, -0.2)
            d.t = -rng.uniform(0, 3.0)
            d.sp = rng.uniform(0.55, 0.9)

            def up(m, dt):
                m.t += dt
                r = max(m.t, 0.0)
                if r > 4.2:
                    m.t = 0.0
                    r = 0.0
                m.move_to(V(-3.0, -0.45) + V(np.cos(m.a), np.sin(m.a)) * (0.9 * r ** 0.9 * m.sp * 1.5))
                m.set_opacity(0 if m.t < 0 else max(0.0, 1 - r / 4.4))
            d.add_updater(up)
            puff.add(d)
        targets = VGroup(*[Circle(radius=0.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.25).move_to(p)
                           for p in (V(-5.6, -1.9), V(-4.2, -2.8), V(-2.4, -2.8))]).set_opacity(0.55)
        lab_h = T("hormone (schematic)", 28, WHITE).move_to([-3.9, -3.5, 0])
        lab_s = T("synapse (schematic)", 28, TEAL).move_to([2.6, -3.35, 0])
        self.at("One possibility")
        self.play(FadeIn(targets), run_time=0.8)
        self.at("hormone released")
        self.add(puff)
        self.play(FadeIn(lab_h), run_time=0.8)
        self.at("Another is")
        self.play(UpdateFromAlphaFunc(w["proc"], lambda m, a: m.pointwise_become_partial(PROC_FULL, 0, 0.72 + 0.28 * a)),
                  qm.animate.move_to(CONTACT + UP * 0.5), run_time=0.7)
        self.at("point to point")
        self.play(FadeIn(lab_s), Indicate(w["bulb"], color=TEAL, scale_factor=1.8), run_time=1.0)
        # clock appears, then splits: neither route wins
        clk = VGroup(Circle(radius=0.5, color=WHITE, stroke_width=4), Line(ORIGIN, UP * 0.38, color=WHITE, stroke_width=4)).move_to([0, 3.0, 0])
        hand = clk[1]
        hand.add_updater(lambda m, dt: m.rotate(-dt * 2.4, about_point=clk[0].get_center()))
        self.at("Speed alone")
        self.play(FadeIn(clk, scale=0.6), run_time=0.8)
        self.at("settle the choice")
        c1 = clk.copy().scale(0.7).move_to([-1.35, -3.35, 0])
        c2 = clk.copy().scale(0.7).move_to([5.6, -3.35, 0])
        for c in (c1, c2):
            c[1].clear_updaters()
            c[1].add_updater(lambda m, dt, c=c: m.rotate(-dt * 2.4, about_point=c[0].get_center()))
        hand.clear_updaters()
        self.play(ReplacementTransform(clk, VGroup(c1)), FadeIn(c2, scale=0.6), run_time=1.0)
        self.finish()


class S03Connection(Base):
    def construct(self):
        self.clock()
        w = world(1.0)
        ring = new_ring()
        self.add(*[w[k] for k in ("epi", "cell", "proc", "axon", "bulb", "dots", "trav", "lab_cell", "lab_axon")])
        qm = T("?", 48, WHITE).move_to(CONTACT + DOWN * 0.75)
        self.add(qm)
        head = T("anatomy", 40, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        self.at("Start with")
        self.play(FadeIn(head), run_time=0.8)
        head2 = T("rabies tracing", 40, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        self.at("Modified")
        self.play(Transform(head, head2), run_time=0.6)
        rng = np.random.RandomState(2)
        sparks = VGroup()
        for i in range(6):
            d = Dot(radius=0.1, color=WHITE).move_to(CELL_C + V(rng.uniform(-0.5, 0.5), rng.uniform(-0.7, 0.7)))
            d.base = d.get_center().copy()
            d.t = rng.uniform(0, 6)
            d.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.move_to(m.base + V(0.12 * np.sin(m.t * 3), 0.12 * np.cos(m.t * 2.3)))))
            sparks.add(d)
        self.at("begins in")
        self.play(FadeIn(sparks, scale=0.5), run_time=0.9)
        self.at("labels connected")
        for d in sparks:
            d.clear_updaters()
        self.play(LaggedStart(*[fly(d, route_pt) for d in sparks], lag_ratio=0.12), run_time=2.4, rate_func=linear)
        self.play(FadeIn(ring), run_time=0.3)
        chip_m = solid_chip("some mice", TEXT, 28).move_to([-5.2, 3.3, 0])
        self.at("In some mice")
        self.play(FadeIn(chip_m), run_time=0.6)
        oval = Ellipse(width=1.5, height=1.1, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.35).move_to([6.0, -0.6, 0])
        lab_o = T("nodose neurons", 28, BLUE).move_to([5.0, -1.6, 0])
        self.at("labeling reaches")
        self.play(FadeIn(oval), FadeOut(w["lab_axon"]), FadeIn(lab_o), run_time=0.8)
        self.play(oval.animate.set_fill(WHITE, 0.55), run_time=0.8)
        self.finish()


class S03TraceLimit(Base):
    def construct(self):
        self.clock()
        w = world(1.0)
        ring = new_ring()
        w["axon"].set_stroke(interpolate_color(BLUE, WHITE, 0.45))
        self.add(*[w[k] for k in ("epi", "cell", "proc", "axon", "bulb", "dots", "trav", "lab_cell", "lab_axon")], ring)
        line = DashedLine(V(-6.6, -0.4), V(6.6, -0.4), color=WHITE, stroke_width=4)
        lab_b = T("epithelial boundary", 28, WHITE).move_to([0.0, -0.85, 0])
        self.at("across the")
        self.play(Create(line), FadeIn(lab_b), run_time=1.0)
        sp = VGroup(*[Dot(radius=0.1, color=WHITE) for _ in range(4)])
        self.add(sp)
        self.play(LaggedStart(*[fly(d, lambda a: route_pt(a * 0.5)) for d in sp], lag_ratio=0.25), run_time=2.6, rate_func=linear)
        self.play(FadeOut(sp), run_time=0.2)
        self.at("It cannot show")
        g = VGroup(w["epi"], w["cell"], w["proc"], w["axon"], w["bulb"], ring)
        self.play(FadeOut(line), FadeOut(lab_b), FadeOut(w["dots"]), FadeOut(w["trav"]), FadeOut(w["lab_cell"]), FadeOut(w["lab_axon"]),
                  g.animate.scale(SMALL_S, about_point=ORIGIN).shift(SMALL_SH), run_time=0.8)
        cards = VGroup(*[solid_chip(s, WHITE, 30).move_to([-3.3, y, 0]) for s, y in
                         (("how fast?", -1.6), ("which messenger?", -2.45), ("changes firing?", -3.3))])
        self.at("rapid transmission")
        self.play(FadeIn(cards[0], shift=UP * 0.2), run_time=0.4)
        self.at("identify the messenger")
        self.play(FadeIn(cards[1], shift=UP * 0.2), run_time=0.5)
        self.at("whether the connection")
        self.play(FadeIn(cards[2], shift=UP * 0.2), run_time=0.5)
        self.at("The picture must")
        frame, trace = self.plot(0.0, 1.0, lambda a: WHITE)
        self.play(g.animate.set_fill(opacity=0).set_stroke(opacity=0.7), FadeOut(ring), Create(frame), run_time=1.6)
        self.add(trace)
        self.finish()


class S04Limit(Base):
    def construct(self):
        self.clock()
        w = world(1.0, labels=False, lumen_dots=False)
        w["axon"].set_stroke(interpolate_color(BLUE, WHITE, 0.45))
        ring = new_ring()
        g = small_world(w, (ring,))
        g.set_fill(opacity=0).set_stroke(opacity=0.7)
        cards = VGroup(*[solid_chip(s, WHITE, 30).move_to([-3.3, y, 0]) for s, y in
                         (("how fast?", -1.6), ("which messenger?", -2.45), ("changes firing?", -3.3))])
        frame, trace = self.plot(0.0, 1.0, lambda a: WHITE)
        self.add(g, cards, frame, trace)
        # the connection compresses into a 'connected' card
        c_box = RoundedRectangle(width=4.8, height=2.5, corner_radius=0.25, stroke_color=WHITE, stroke_width=4,
                                 fill_color=WHITE, fill_opacity=0.06).move_to([-3.6, -1.6, 0])
        c_dots = VGroup(Dot(radius=0.2, color=GOLD).move_to([-4.6, -1.2, 0]), Line([-4.4, -1.2, 0], [-2.8, -1.2, 0], color=WHITE, stroke_width=5),
                        Dot(radius=0.2, color=BLUE).move_to([-2.6, -1.2, 0]))
        c_lab = T("connected", 34, WHITE).move_to([-3.6, -2.1, 0])
        self.at("That establishes")
        self.play(FadeOut(cards), ReplacementTransform(g, c_box), run_time=1.4)
        self.play(FadeIn(c_dots), FadeIn(c_lab), run_time=0.8)
        # VGLUT1 transcript card
        gbox = RoundedRectangle(width=4.8, height=2.5, corner_radius=0.25, stroke_color=GOLD, stroke_width=4,
                                fill_color=GOLD, fill_opacity=0.2).move_to([-3.6, 1.5, 0])
        sq = always_redraw(lambda: FunctionGraph(lambda x: 0.14 * np.sin(5 * x + self.ph.get_value() * 3), x_range=[-5.6, -1.6, 0.05],
                                                  color=TEAL, stroke_width=5).shift(UP * 2.15))
        self.at("The cells also")
        self.play(FadeIn(gbox, scale=0.9), FadeIn(sq), run_time=1.2)
        glab = T("VGLUT1 transcript", 30, TEAL).move_to([-3.6, 1.2, 0])
        self.at("vesicular")
        self.play(Write(glab), run_time=1.5)
        self.at("Those transcripts fit")
        self.play(Indicate(glab, color=TEAL, scale_factor=1.12), run_time=1.4)
        notyet = T("not yet", 52, WHITE, weight=BOLD).move_to([3.65, 2.35, 0])
        self.at("still do not")
        self.play(Write(notyet), run_time=1.0)
        self.finish()


class S05Current(Base):
    def construct(self):
        self.clock()
        # carried from the last scene: two cards at left, empty plot at right
        gbox = RoundedRectangle(width=4.8, height=2.5, corner_radius=0.25, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.2).move_to([-3.6, 1.5, 0])
        glab = T("VGLUT1 transcript", 30, TEAL).move_to([-3.6, 1.2, 0])
        c_box = RoundedRectangle(width=4.8, height=2.5, corner_radius=0.25, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.06).move_to([-3.6, -1.6, 0])
        c_dots = VGroup(Dot(radius=0.2, color=GOLD).move_to([-4.6, -1.2, 0]), Line([-4.4, -1.2, 0], [-2.8, -1.2, 0], color=WHITE, stroke_width=5), Dot(radius=0.2, color=BLUE).move_to([-2.6, -1.2, 0]))
        c_lab = T("connected", 34, WHITE).move_to([-3.6, -2.1, 0])
        sq = always_redraw(lambda: FunctionGraph(lambda x: 0.14 * np.sin(5 * x + self.ph.get_value() * 3), x_range=[-5.6, -1.6, 0.05], color=TEAL, stroke_width=5).shift(UP * 2.15))
        notyet = T("not yet", 52, WHITE, weight=BOLD).move_to([3.65, 2.35, 0])
        frame, trace = self.plot(0.0, 1.0, lambda a: interpolate_color(WHITE, GREEN, min(1, a * 3)))
        self.add(gbox, glab, sq, c_box, c_dots, c_lab, notyet, frame, trace)
        d = dish()
        light = Arrow(V(-4.2, 3.4), V(-4.2, 1.2), buff=0, color=GREEN, stroke_width=8, tip_length=0.3)
        lab_l = T("light", 30, GREEN).move_to([-3.2, 2.5, 0])
        self.at("Now move")
        self.play(FadeOut(VGroup(gbox, glab, sq, c_box, c_dots, c_lab, notyet)), run_time=0.9)
        self.play(Create(d["out"]), run_time=1.0)
        self.play(FadeIn(d["body"], scale=0.9), run_time=1.1)
        self.play(FadeIn(d["lab_cell"]), FadeIn(d["lab_n"]), run_time=0.6)
        sch = T("schematic trace", 28, WHITE).move_to([3.65, 1.55, 0])
        self.at("Light activates")
        self.play(GrowArrow(light), FadeIn(lab_l), d["cell"].animate.set_fill(GOLD, 0.8), run_time=1.0)
        msg = crossing_dots(3, WHITE, 0.45)
        self.add(msg)
        self.play(FadeIn(sch), run_time=0.8)
        # time bar 60 -> 800 ms, computed on the plot's own axis
        bar_y = -1.45
        bar = VGroup(Line(AX.c2p(60, bar_y), AX.c2p(800, bar_y), color=TEAL, stroke_width=7),
                     Line(AX.c2p(60, bar_y) + DOWN * 0.15, AX.c2p(60, bar_y) + UP * 0.15, color=TEAL, stroke_width=6),
                     Line(AX.c2p(800, bar_y) + DOWN * 0.15, AX.c2p(800, bar_y) + UP * 0.15, color=TEAL, stroke_width=6))
        lab_b = T("measured range", 28, TEAL).move_to(AX.c2p(560, -1.05))
        self.at("Within")
        self.play(Create(bar), FadeIn(lab_b), run_time=1.4)
        self.at("an excitatory current")
        self.amp.set_value(1.0)
        self.sweep.set_value(0.03)
        self.play(self.sweep.animate.set_value(1.0), run_time=3.0, rate_func=linear)
        self.finish()


def dish_stage(self, amp=1.0, blocks=False, colorfn=None, light=False):
    """rebuild the dish + plot exactly as the last scene left them."""
    d = dish(blocks)
    frame, trace = self.plot(amp, 1.0, colorfn)
    sch = T("schematic trace", 28, WHITE).move_to([3.65, 1.55, 0])
    parts = [d["out"], d["body"], d["lab_cell"], d["lab_n"], frame, trace, sch]
    self.add(*parts)
    return d, sch


def time_bar():
    bar_y = -1.45
    return VGroup(Line(AX.c2p(60, bar_y), AX.c2p(800, bar_y), color=TEAL, stroke_width=7),
                  Line(AX.c2p(60, bar_y) + DOWN * 0.15, AX.c2p(60, bar_y) + UP * 0.15, color=TEAL, stroke_width=6),
                  Line(AX.c2p(800, bar_y) + DOWN * 0.15, AX.c2p(800, bar_y) + UP * 0.15, color=TEAL, stroke_width=6),
                  T("measured range", 28, TEAL).move_to(AX.c2p(560, -1.05)))


class S05CurrentLimit(Base):
    def construct(self):
        self.clock()
        d, sch = dish_stage(self, 1.0)
        bar = time_bar()
        self.add(bar)
        msg = crossing_dots(3, WHITE, 0.6)
        self.add(msg)
        badge = solid_chip("direct neuronal response", GREEN, 28).move_to([3.65, 2.5, 0])
        self.at("directly")
        self.play(FadeIn(badge, shift=DOWN * 0.2), self.trace.animate.set_stroke(width=9), run_time=1.0)
        self.at("subsecond latency")
        self.play(Indicate(bar, color=TEAL, scale_factor=1.06), run_time=1.6)
        self.at("supports a fast")
        self.play(Indicate(badge, color=GREEN, scale_factor=1.08), run_time=1.2)
        rec = receptors()
        self.at("But one current")
        self.play(LaggedStart(*[FadeIn(r, scale=0.4) for r in rec], lag_ratio=0.4), run_time=1.6)
        qs = VGroup(*[T("?", 40, WHITE).move_to([x, -1.55, 0]) for x in BLOCK_X])
        self.at("which receptors")
        self.play(LaggedStart(*[FadeIn(q, shift=DOWN * 0.15) for q in qs], lag_ratio=0.25), run_time=1.2)
        self.finish()


class S06Predict(Base):
    def construct(self):
        self.clock()
        d, sch = dish_stage(self, 1.0, blocks=True, colorfn=lambda a: interpolate_color(RED, GREEN, min(1, a * 3)))
        bar_t = time_bar()
        self.add(bar_t)
        msg = crossing_dots(3, TEAL, 0.6)
        self.add(msg)
        red = RoundedRectangle(width=2.5, height=0.45, corner_radius=0.1, stroke_color=RED, stroke_width=4,
                               fill_color=RED, fill_opacity=0.45).move_to([-3.6, -2.0, 0])
        lab_k = T("kynurenic acid", 26, RED).move_to([-3.4, -3.45, 0])
        self.at("blocks ionotropic")
        self.play(FadeOut(bar_t), FadeIn(red, shift=DOWN * 0.4), FadeIn(lab_k), run_time=1.2)
        msg.clear_updaters()
        self.remove(msg)
        stop = stopped_dots(TEAL, -1.62, 0.6)
        self.add(stop)
        self.at("the current")
        self.play(self.amp.animate.set_value(0.0), run_time=1.4)
        q = T("Blocked receptors\nor damaged cells?", 44, TEXT).move_to([0.3, 2.65, 0])
        self.at("If receptors")
        self.play(Write(q), run_time=2.0)
        bottle = VGroup(RoundedRectangle(width=0.7, height=0.9, corner_radius=0.15, stroke_color=TEXT, stroke_width=4),
                        Rectangle(width=0.25, height=0.3, stroke_color=TEXT, stroke_width=4).shift(UP * 0.6)).scale(0.5).move_to([6.3, 3.2, 0])
        wl = T("wash", 24, TEXT).next_to(bottle, LEFT, buff=0.15)
        self.at("what should")
        self.play(FadeIn(bottle), FadeIn(wl), run_time=1.0)
        self.finish()


class S07Pause(Base):
    def construct(self):
        self.clock()
        d, sch = dish_stage(self, 0.0, blocks=True, colorfn=lambda a: interpolate_color(RED, GREEN, min(1, a * 3)))
        red = RoundedRectangle(width=2.5, height=0.45, corner_radius=0.1, stroke_color=RED, stroke_width=4,
                               fill_color=RED, fill_opacity=0.45).move_to([-3.6, -2.0, 0])
        red.t = 0.0
        red.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_fill(RED, 0.35 + 0.15 * np.sin(m.t * 3))))
        lab_k = T("kynurenic acid", 26, RED).move_to([-3.4, -3.45, 0])
        q = T("Blocked receptors\nor damaged cells?", 44, TEXT).move_to([0.3, 2.65, 0])
        bottle = VGroup(RoundedRectangle(width=0.7, height=0.9, corner_radius=0.15, stroke_color=TEXT, stroke_width=4),
                        Rectangle(width=0.25, height=0.3, stroke_color=TEXT, stroke_width=4).shift(UP * 0.6)).scale(0.5).move_to([6.3, 3.2, 0])
        wl = T("wash", 24, TEXT).next_to(bottle, LEFT, buff=0.15)
        self.add(red, lab_k, q, bottle, wl, stopped_dots(TEAL, -1.62, 0.6), shimmer(self.ph))
        self.finish()


class S08Washout(Base):
    def construct(self):
        self.clock()
        d, sch = dish_stage(self, 0.0, blocks=True, colorfn=lambda a: interpolate_color(RED, GREEN, min(1, a * 3)))
        red = RoundedRectangle(width=2.5, height=0.45, corner_radius=0.1, stroke_color=RED, stroke_width=4,
                               fill_color=RED, fill_opacity=0.45).move_to([-3.6, -2.0, 0])
        lab_k = T("kynurenic acid", 26, RED).move_to([-3.4, -3.45, 0])
        q = T("Blocked receptors\nor damaged cells?", 44, TEXT).move_to([0.3, 2.65, 0])
        bottle = VGroup(RoundedRectangle(width=0.7, height=0.9, corner_radius=0.15, stroke_color=TEXT, stroke_width=4),
                        Rectangle(width=0.25, height=0.3, stroke_color=TEXT, stroke_width=4).shift(UP * 0.6)).scale(0.5).move_to([6.3, 3.2, 0])
        wl = T("wash", 24, TEXT).next_to(bottle, LEFT, buff=0.15)
        stop = stopped_dots(TEAL, -1.62, 0.6)
        self.add(red, lab_k, q, bottle, wl, stop)
        wave = Rectangle(width=1.2, height=4.4, stroke_width=0, fill_color=TEAL, fill_opacity=0.3).move_to([-6.1, -1.2, 0])
        self.at("Washout removes")
        self.add(wave)
        self.play(wave.animate.move_to([-0.9, -1.2, 0]), red.animate.shift(RIGHT * 2.5).set_opacity(0),
                  FadeOut(lab_k), run_time=1.5, rate_func=linear)
        self.play(FadeOut(wave), run_time=0.2)
        self.remove(stop)
        msg = crossing_dots(3, TEAL, 0.6)
        self.add(msg)
        self.play(d["blocks"].animate.set_fill(BLUE, 0.8), run_time=0.3)
        self.at("the current returns")
        self.amp.set_value(1.0)
        self.sweep.set_value(0.03)
        self.play(self.sweep.animate.set_value(1.0), run_time=2.0, rate_func=linear)
        self.at("Recovery supports")
        self.play(Indicate(d["blocks"], color=BLUE), run_time=1.6)
        b1 = solid_chip("fast current", GREEN, 30).move_to([-2.4, 2.6, 0])
        b2 = solid_chip("reversible glutamate block", TEAL, 30).move_to([3.4, 2.6, 0])
        self.at("Together")
        self.play(FadeOut(q), FadeOut(bottle), FadeOut(wl), run_time=0.5)
        self.play(FadeIn(b1), run_time=0.5)
        self.at("reversible pharmacology")
        self.play(FadeIn(b2), run_time=1.0)
        link = Line(b1.get_right(), b2.get_left(), color=WHITE, stroke_width=5)
        self.at("identify fast")
        self.play(Create(link), run_time=1.0)
        self.finish()


CHIP_NAMES = ("anatomy", "timing", "pharmacology", "causality")
RING_POS = (V(-0.2, -0.6), V(2.6, -1.95), V(-0.2, -3.1), V(-3.0, -1.95))


def chain_chips(color=WHITE):
    return [solid_chip(n, color, 32).move_to(p) for n, p in zip(CHIP_NAMES, RING_POS)]


class S09Rule(Base):
    def construct(self):
        self.clock()
        w = world(1.0, labels=False)
        w["axon"].set_stroke(interpolate_color(BLUE, WHITE, 0.45))
        parts = [w[k] for k in ("epi", "cell", "proc", "axon", "bulb", "dots", "trav")]
        d = dish_stage  # noqa
        old = VGroup(*[dish(True)[k] for k in ("out", "body")])
        frame, trace = self.plot(1.0, 1.0)
        self.add(old, frame, trace)
        self.at("Here is")
        self.play(FadeOut(old), FadeOut(frame), FadeOut(trace), run_time=0.8)
        self.add(*parts)
        sp = VGroup(*[Dot(radius=0.1, color=WHITE) for _ in range(4)])
        self.add(sp)
        self.play(LaggedStart(*[fly(x, route_pt) for x in sp], lag_ratio=0.2), run_time=1.5, rate_func=linear)
        self.remove(sp)
        one = solid_chip("one result", WHITE, 30).move_to([2.6, 0.6, 0])
        cross = VGroup(Line(UL, DR, color=RED, stroke_width=7), Line(UR, DL, color=RED, stroke_width=7)).scale(0.4).move_to([2.6, -0.3, 0])
        self.at("No single")
        self.play(FadeIn(one), run_time=0.8)
        self.play(Create(cross), run_time=0.8)
        self.at("A fast synapse")
        self.play(FadeOut(one), FadeOut(cross), run_time=0.7)
        chips = chain_chips()
        for c in chips:
            c.set_z_index(3)
        links = [Line(RING_POS[i], RING_POS[(i + 1) % 4], color=WHITE, stroke_width=5) for i in range(4)]
        for i, (txt, ph) in enumerate((("anatomy", None), ("timing", None), ("pharmacology", None), ("causal", None))):
            self.at(txt)
            anims = [FadeIn(chips[i], scale=0.7)]
            if i > 0:
                anims.append(Create(links[i - 1]))
            self.play(*anims, run_time=0.8)
        glow = Circle(radius=0.2, stroke_color=TEAL, stroke_width=6, fill_color=TEAL, fill_opacity=0.4).move_to(CONTACT)
        self.at("converge")
        self.play(Create(links[3]), run_time=0.7)
        for c in chips:
            recolor(c, TEAL)
        self.play(*[l.animate.set_color(TEAL) for l in links],
                  GrowFromCenter(glow), glow.animate.scale(2.6), run_time=1.0)
        self.finish()


class S10Mouse(Base):
    def construct(self):
        self.clock()
        w = world(1.0, labels=False)
        w["axon"].set_stroke(interpolate_color(BLUE, WHITE, 0.45))
        self.add(*[w[k] for k in ("epi", "cell", "proc", "axon", "bulb", "dots", "trav")])
        for p in (w["epi"], w["cell"]):
            pass
        mouse = solid_chip("mouse", WHITE, 28).move_to([-5.5, 3.3, 0])
        rate = ValueTracker(0.8)
        box = Rectangle(width=3.3, height=1.7, stroke_color=GREY, stroke_width=3).move_to([4.95, -2.6, 0])
        ras = raster(V(4.95, -2.6), 3.3, 1.7, rate, self.ph)
        lab_f = T("vagal firing", 28, BLUE).move_to([4.95, -1.5, 0])
        lab_s = T("schematic", 24, WHITE).move_to([4.95, -3.65, 0])
        self.at("Causality comes")
        self.play(FadeIn(mouse), FadeIn(box), FadeIn(lab_f), FadeIn(lab_s), run_time=1.0)
        self.add(ras)
        block_sq = Square(0.5, stroke_color=TEXT, stroke_width=4, fill_color=TEAL, fill_opacity=0.6).move_to([-3.0, 1.95, 0])
        stream = VGroup()
        for i in range(6):
            dd = Dot(radius=0.1, color=GOLD)
            dd.t = i / 6
            dd.x = -3.0 + (i % 3 - 1) * 0.3
            dd.blk = ValueTracker(0)

            def up(m, dt, bt=None):
                m.t = (m.t + dt * 0.3) % 1
                y = 3.4 - m.t * 2.4
                if self.blocked and y < 2.35:
                    y = 2.35 + 0.05 * (m.x + 3)
                m.move_to([m.x, y, 0])
                m.set_opacity(1 if y > 1.75 else 0.0)
            dd.add_updater(up)
            stream.add(dd)
        self.blocked = False
        self.at("Intestinal sucrose")
        self.play(w["dots"].animate.set_color(GOLD), FadeIn(block_sq), run_time=1.0)
        self.add(stream)
        self.at("raises cervical")
        self.play(rate.animate.set_value(4.0), run_time=1.4)
        x = VGroup(Line(UL, DR, color=RED, stroke_width=8), Line(UR, DL, color=RED, stroke_width=8)).scale(0.42).move_to([-3.0, 1.95, 0])
        self.at("Blocking")
        self.blocked = True
        self.play(Create(x), block_sq.animate.set_fill(RED, 0.5), run_time=0.8)
        lab_sg = T("SGLT1", 28, TEAL).move_to([-1.45, 2.4, 0])
        self.at("sodium glucose")
        self.play(FadeIn(lab_sg), run_time=0.6)
        self.at("removes that response")
        self.play(rate.animate.set_value(0.8), run_time=1.5)
        self.at("placing the sugar")
        self.play(Indicate(w["cell"], color=GOLD, scale_factor=1.08), run_time=1.6)
        self.finish()


def half_panel(cx, ph, rate, seed, sucrose=False):
    P = {}
    P["tis"] = Rectangle(width=6.2, height=7.2, stroke_width=0, fill_color=GREY, fill_opacity=0.2).move_to([cx, 0, 0])
    P["cell"] = RoundedRectangle(width=1.5, height=1.7, corner_radius=0.3, stroke_color=GOLD, stroke_width=5,
                                 fill_color=GOLD, fill_opacity=0.45).move_to([cx - 1.6, 0.45, 0])
    cl = T("CCK", 28, TEXT).move_to(P["cell"])
    P["cell"] = VGroup(P["cell"], cl)
    pr = CubicBezier(V(cx - 1.6, -0.4), V(cx - 1.6, -1.0), V(cx - 1.0, -1.0), V(cx - 0.3, -1.0))
    ax = CubicBezier(V(cx + 0.1, -1.0), V(cx + 1.2, -1.0), V(cx + 1.8, -0.8), V(cx + 3.05, -0.8))
    P["nerve"] = VGroup(hl(pr, GOLD, 8), hl(ax, BLUE, 12))
    P["ras"] = raster(V(cx, -2.9), 5.4, 1.2, rate, ph, rows=3, seed=seed)
    P["box"] = Rectangle(width=5.4, height=1.2, stroke_color=GREY, stroke_width=3).move_to([cx, -2.9, 0])
    P["mouse"] = T("mouse", 28, WHITE).move_to([cx + 1.9, 3.3, 0])
    if sucrose:
        P["suc"] = drift_dots(5, cx - 2.9, cx + 2.9, 2.2, 3.0, GOLD, seed + 3, 0.09, 0.8)
    return P


class S11Necessity(Base):
    def construct(self):
        self.clock()
        rl, rr = ValueTracker(4.0), ValueTracker(0.8)
        L = half_panel(-3.4, self.ph, rl, 11, True)
        R = half_panel(3.4, self.ph, rr, 12)
        div = Line([0, 3.7, 0], [0, -3.7, 0], color=WHITE, stroke_width=3)
        self.play(FadeIn(div), *[FadeIn(L[k]) for k in ("tis", "cell", "nerve", "box", "mouse")],
                  *[FadeIn(R[k]) for k in ("tis", "cell", "nerve", "box", "mouse")], run_time=0.4)
        self.add(L["ras"], R["ras"], L["suc"])
        beamL = Arrow(V(-5.0, 3.5), V(-5.0, 1.45), buff=0, color=RED, stroke_width=8, tip_length=0.3)
        beamR = Arrow(V(1.8, 3.5), V(1.8, 1.45), buff=0, color=GREEN, stroke_width=8, tip_length=0.3)
        labL = T("necessary in this test", 28, RED).move_to([-3.4, -1.75, 0])
        labR = T("sufficient in this test", 28, GREEN).move_to([3.4, -1.75, 0])
        self.at("Light that silences")
        self.play(GrowArrow(beamL), L["cell"][0].animate.set_fill(RED, 0.15).set_stroke(RED), run_time=1.0)
        self.at("abolishes")
        self.play(rl.animate.set_value(0.4), FadeIn(labL), run_time=1.4)
        self.at("Light that activates")
        self.play(GrowArrow(beamR), R["cell"][0].animate.set_fill(GOLD, 0.9), run_time=1.0)
        self.at("raises vagal")
        self.play(rr.animate.set_value(4.0), FadeIn(labR), run_time=1.4)
        self.at("necessity")
        self.play(Indicate(labL, color=RED), run_time=1.0)
        self.at("sufficiency")
        self.play(Indicate(labR, color=GREEN), run_time=1.0)
        self.finish()


def _row():
    g = VGroup(*chain_chips()).arrange(RIGHT, buff=0.6).move_to([0, 3.0, 0])
    return [c.get_center() for c in g]


ROW = _row()


def row_links(chips):
    return [Line(chips[i].get_right(), chips[i + 1].get_left(), color=WHITE, stroke_width=5) for i in range(3)]


class S12Scope(Base):
    def construct(self):
        self.clock()
        chips = chain_chips(TEAL)
        links = [Line(RING_POS[i], RING_POS[(i + 1) % 4], color=TEAL, stroke_width=5) for i in range(4)]
        for c in chips:
            c.set_z_index(3)
        self.add(*links, *chips)
        self.at("The chain")
        rl = row_links([c.copy().move_to(p) for c, p in zip(chips, ROW)])
        for c in chips:
            recolor(c, WHITE)
        self.play(FadeOut(VGroup(*links)), *[c.animate.move_to(p) for c, p in zip(chips, ROW)], run_time=1.4)
        self.play(*[Create(l) for l in rl], run_time=0.8)
        dishr = SurroundingRectangle(VGroup(chips[1], chips[2]), buff=0.18, corner_radius=0.3, color=WHITE, stroke_width=4)
        dl = T("coculture dish", 28, WHITE).move_to(dishr.get_bottom() + DOWN * 0.35)
        self.at("Cocultures are")
        self.play(Create(dishr), FadeIn(dl), run_time=1.2)
        cells = VGroup(*[RoundedRectangle(width=1.1, height=1.4, corner_radius=0.25, stroke_color=GOLD, stroke_width=4,
                                          fill_color=GOLD, fill_opacity=0.35).move_to([-5.0 + 2.0 * i, 0.6, 0]) for i in range(6)])
        fib = VGroup(Line([-6.2, -1.7, 0], [6.2, -1.7, 0], color=BLUE, stroke_width=12), Line([-6.2, -2.4, 0], [6.2, -2.4, 0], color=BLUE, stroke_width=12))
        stubs = VGroup()
        cont = VGroup()
        for i in range(6):
            x = -5.0 + 2.0 * i
            if i in (1, 4):
                cont.add(Line([x, -0.1, 0], [x, -1.65, 0], color=GOLD, stroke_width=6))
                cont.add(Dot([x, -1.62, 0], radius=0.13, color=TEAL))
            else:
                stubs.add(Line([x, -0.1, 0], [x, -0.65, 0], color=GOLD, stroke_width=6))
        labc = T("CCK cells", 28, GOLD).move_to([-5.2, 1.65, 0])
        labf = T("sensory fibers", 28, BLUE).move_to([-4.3, -3.05, 0])
        self.at("Only a minority")
        self.play(FadeIn(cells, lag_ratio=0.15), FadeIn(labc), run_time=1.6)
        self.add(stubs)
        self.at("contacted sensory")
        self.play(FadeIn(fib), FadeIn(labf), run_time=1.0)
        self.play(Create(cont), run_time=1.4)
        frame = RoundedRectangle(width=13.2, height=7.4, corner_radius=0.3, stroke_color=WHITE, stroke_width=3).set_stroke(opacity=0.6)
        labm = T("mouse evidence", 28, WHITE).move_to([4.6, -3.15, 0])
        self.at("in fixed")
        self.play(Create(frame), FadeIn(labm), run_time=1.2)
        rng = np.random.RandomState(4)
        hdots = VGroup()
        for i in range(14):
            d = Dot(radius=0.075, color=GREY)
            d.c = V(-5.0 + 2.0 * rng.randint(0, 6), -0.2)
            d.a = rng.uniform(-2.7, -0.4)
            d.t = -rng.uniform(0, 2)

            def up(m, dt):
                m.t += dt
                r = max(m.t, 0)
                if r > 3.4:
                    m.t = 0
                    r = 0
                m.move_to(m.c + V(np.cos(m.a), np.sin(m.a)) * 0.8 * r)
                m.set_opacity(0 if m.t < 0 else max(0, 1 - r / 3.4))
            d.add_updater(up)
            hdots.add(d)
        self.at("A synapse does")
        self.add(hdots)
        self.play(*[d.animate.scale(1.8) for d in cont if isinstance(d, Dot)], rate_func=there_and_back, run_time=1.6)
        self.finish()


class S13Handoff(Base):
    def construct(self):
        self.clock()
        chips = [solid_chip(n, WHITE, 28).move_to(p) for n, p in zip(CHIP_NAMES, ROW)]
        rl = row_links(chips)
        self.add(*chips, *rl)
        Y = -0.5
        gold = RoundedRectangle(width=2.6, height=1.7, corner_radius=0.3, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.3).move_to([-4.75, Y, 0])
        gl = T("gut sensor", 32, GOLD).move_to(gold)
        syn = Circle(radius=1.0, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.25).move_to([-1.8, Y, 0])
        sl = T("synapse", 30, TEAL).move_to(syn)
        blue = RoundedRectangle(width=2.6, height=1.7, corner_radius=0.3, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to([1.15, Y, 0])
        bl = T("vagus", 32, BLUE).move_to(blue)
        box = RoundedRectangle(width=2.8, height=1.9, corner_radius=0.3, stroke_color=WHITE, stroke_width=4).move_to([4.5, Y, 0])
        q = T("?", 72, WHITE).move_to(box)
        a1 = Arrow(gold.get_right(), syn.get_left(), buff=0.05, color=WHITE, stroke_width=5)
        a2 = Arrow(syn.get_right(), blue.get_left(), buff=0.05, color=WHITE, stroke_width=5)
        a3 = Arrow(blue.get_right(), box.get_left(), buff=0.05, color=WHITE, stroke_width=5)
        self.at("Anatomy found")
        pop(self, chips[0])
        self.play(FadeIn(VGroup(gold, gl)), FadeIn(VGroup(blue, bl)), run_time=1.6)
        self.play(Create(a1), Create(a2), run_time=0.8)
        self.at("Physiology identified")
        self.play(FadeIn(VGroup(syn, sl)), run_time=1.0)
        pop(self, chips[1], chips[2], rt=0.8)
        self.play(Indicate(syn, color=TEAL, scale_factor=1.12), run_time=1.2)
        pul = VGroup()
        pts = [V(-4.75, Y - 0.6), V(-1.8, Y - 0.6), V(1.15, Y - 0.6), V(4.5, Y - 0.6)]
        for i in range(3):
            d = Dot(radius=0.14, color=GREEN)
            d.t = i / 3
            d.add_updater(lambda m, dt: (setattr(m, "t", (m.t + dt * 0.28) % 1),
                                         m.move_to(pts[0] + (pts[3] - pts[0]) * m.t) if False else None,
                                         m.move_to(pts[int(m.t * 3)] + (pts[int(m.t * 3) + 1] - pts[int(m.t * 3)]) * ((m.t * 3) % 1))))
            pul.add(d)
        self.at("Acute manipulations")
        self.play(FadeIn(pul), run_time=0.6)
        pop(self, chips[3], rt=0.8)
        self.add(pul)
        self.at("The next question")
        self.play(Create(box), Create(a3), run_time=1.0)
        self.play(Write(q), run_time=1.0)
        self.finish()


class S14End(EndCard):
    LINE = "A fast gut synapse requires a chain of evidence."
