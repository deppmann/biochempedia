"""Why doubling substrate stops doubling speed.

COLOR MAP
  BLUE   enzyme booths, busy fraction, velocity curve
  YELLOW substrate and [S]
  GREEN  product and measured velocity
  RED    Vmax ceiling / rejected prediction
  GOLD   Km and the half-speed construction
  GREY   axes and supporting structure

The film stays in one schematic toll-plaza world.  All plotted values are computed with
v = 60[S]/(4+[S]); nothing is drawn as a molecular structure.
"""
from bp_style import *  # noqa: F401,F403


K_M = 4.0
V_MAX = 60.0
GOLD_KM = GOLD


def mm(s, vmax=V_MAX, km=K_M):
    return vmax * s / (km + s)


def booth_row(y=-0.35, scale=1.0, busy=2, x0=-3.9, spacing=2.6):
    """Four large schematic enzyme booths, kept at identical landmarks between scenes."""
    booths = VGroup()
    for i in range(4):
        box = RoundedRectangle(
            width=1.75 * scale, height=1.72 * scale, corner_radius=0.16,
            stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
            fill_opacity=0.28 if i < busy else 0.08,
        )
        gate = Line(LEFT * 0.58 * scale, RIGHT * 0.58 * scale,
                    color=GREEN if i >= busy else RED, stroke_width=7)
        gate.move_to(box.get_bottom() + UP * 0.34 * scale)
        state = T("BUSY" if i < busy else "EMPTY", 28,
                  BLUE if i < busy else TEXT, weight=BOLD).scale(scale)
        state.move_to(box.get_center() + UP * 0.30 * scale)
        b = VGroup(box, gate, state).move_to([x0 + i * spacing * scale, y, 0])
        b.box, b.gate, b.state = box, gate, state
        booths.add(b)
    return booths


def set_booth_state(booth, busy):
    box = booth[0].copy().set_fill(BLUE, 0.28 if busy else 0.08)
    gate = booth[1].copy().set_color(RED if busy else GREEN)
    state = T("BUSY" if busy else "EMPTY", 28, BLUE if busy else TEXT, weight=BOLD)
    state.move_to(booth[2])
    return VGroup(box, gate, state)


def car(label="S", color=YELLOW, scale=1.0):
    body = RoundedRectangle(width=0.74, height=0.42, corner_radius=0.11,
                            stroke_width=0, fill_color=color, fill_opacity=1)
    parts = VGroup(body)
    if label:
        parts.add(T(label, 30, BG, weight=BOLD).move_to(body))
    return parts.scale(scale)


def add_flow(scene, y_values=(-2.2, -1.55), speed=1.0, opacity=0.85, x_range=(-6.5, 6.5)):
    """Autonomous substrate traffic: visible motion continues through cue waits."""
    flow = VGroup()
    for row, y in enumerate(y_values):
        for j in range(5):
            c = car(label=None, scale=0.70).set_opacity(opacity)
            c.move_to([x_range[0] + j * 2.8 + row * 0.8, y, 0])
            c.vx = speed * (0.82 + 0.08 * j)

            def drift(m, dt, lo=x_range[0], hi=x_range[1]):
                m.shift(RIGHT * m.vx * dt)
                if m.get_left()[0] > hi:
                    m.shift(LEFT * (hi - lo + m.width + 0.4))

            c.add_updater(drift)
            flow.add(c)
    scene.add(flow)
    return flow


def pulse_gates(booths, speed=2.2):
    """Give each working booth a staggered, slow gate cadence."""
    for i, booth in enumerate(booths):
        booth[1].phase = i * 0.9

        def breathe(m, dt, phase=i * 0.9):
            m.phase += dt * speed
            m.set_stroke(opacity=0.55 + 0.45 * (0.5 + 0.5 * np.sin(m.phase + phase)))

        booth[1].add_updater(breathe)
    return booths


def counter_box(title, value, color, center, width=2.45):
    box = RoundedRectangle(width=width, height=1.05, corner_radius=0.14,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.10)
    lab = T(title, 28, color, weight=BOLD).next_to(box.get_top(), DOWN, buff=0.12)
    num = M(value, 30, TEXT).next_to(box.get_bottom(), UP, buff=0.12)
    g = VGroup(box, lab, num).move_to(center)
    return g


def busy_gauge(frac, center=(5.4, -0.2, 0), height=4.0, label=True):
    box = RoundedRectangle(width=0.72, height=height, corner_radius=0.10,
                           stroke_color=GREY, stroke_width=3)
    fh = max(0.06, (height - 0.12) * frac)
    fill = Rectangle(width=0.60, height=fh, stroke_width=0,
                     fill_color=BLUE, fill_opacity=0.9)
    fill.move_to(box.get_bottom() + UP * (0.06 + fh / 2))
    pct = M(f"{round(frac * 100):d}%", 28, BLUE, weight=BOLD).next_to(box, DOWN, buff=0.14)
    parts = VGroup(box, fill, pct).move_to(center)
    if label:
        lab = T("busy fraction", 28, BLUE).rotate(PI / 2).next_to(box, LEFT, buff=0.18)
        parts.add(lab)
    return parts


def fraction_booths(busy, center=(4.6, 0.5, 0), label=None):
    """Four compact, unlabelled booths plus one readable summary label.

    The full plaza labels become too small when squeezed beside a graph.  These boxes carry
    the same blue/empty visual language without creating unreadable or colliding text.
    """
    boxes = VGroup()
    for i in range(4):
        box = RoundedRectangle(
            width=0.68, height=0.82, corner_radius=0.10,
            stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
            fill_opacity=0.55 if i < busy else 0.06,
        )
        gate = Line(LEFT * 0.22, RIGHT * 0.22,
                    color=RED if i < busy else GREEN, stroke_width=5)
        gate.move_to(box.get_bottom() + UP * 0.16)
        boxes.add(VGroup(box, gate))
    boxes.arrange(RIGHT, buff=0.18).move_to(center)
    if label is None:
        label = f"{busy} of 4 busy"
    summary = T(label, 30, BLUE, weight=BOLD).next_to(boxes, UP, buff=0.22)
    return VGroup(boxes, summary)


def low_s_comparison(center=(4.75, 0.15, 0), width=3.35):
    """Readable computed comparison for the crowded low-[S] end of the main graph."""
    panel = RoundedRectangle(width=width, height=3.45, corner_radius=0.16,
                             stroke_color=GREY, stroke_width=2,
                             fill_color=GREY, fill_opacity=0.16)
    title = T("LOW [S] (mM)", 28, YELLOW, weight=BOLD)
    title.move_to(panel.get_top() + DOWN * 0.32)
    baseline = Line(LEFT * 1.18, RIGHT * 1.18, color=GREY, stroke_width=3)
    baseline.move_to(panel.get_bottom() + UP * 0.60)
    bars = VGroup()
    for x, substrate, velocity in [(-0.62, 0.2, mm(0.2)), (0.62, 0.4, mm(0.4))]:
        h = 1.65 * velocity / mm(0.4)
        bar = Rectangle(width=0.56, height=h, stroke_width=0,
                        fill_color=GREEN, fill_opacity=0.9)
        bar.move_to(baseline.get_center() + RIGHT * x + UP * h / 2)
        value = M(f"{velocity:.1f}", 28, GREEN, weight=BOLD).next_to(bar, UP, buff=0.10)
        amount = M(f"{substrate:.1f}", 28, YELLOW).next_to(
            baseline.get_center() + RIGHT * x, DOWN, buff=0.14
        )
        bars.add(bar, value, amount)
    group = VGroup(panel, title, baseline, bars).move_to(center)
    return group


def graph_world(vmax=V_MAX, y_max=70, origin=(-5.0, -2.55), width=10.5, height=5.0):
    ax = Axes(
        x_range=[0, 32, 4], y_range=[0, y_max, 10], x_length=width, y_length=height,
        axis_config={"include_numbers": False, "include_ticks": False, "color": GREY,
                     "stroke_width": 3, "tip_width": 0.16, "tip_height": 0.16}, tips=True,
    )
    ax.shift(np.array([origin[0], origin[1], 0]) - ax.c2p(0, 0))
    # A single dark plotting field keeps the computed world visually substantial without
    # adding a new claim.  It also matches the broad roadway used by the toll-plaza scenes.
    panel = RoundedRectangle(width=min(12.35, width + 1.55), height=min(6.65, height + 1.35),
                             corner_radius=0.18, stroke_color=GREY, stroke_width=2,
                             fill_color=GREY, fill_opacity=0.24).move_to(ax)
    panel.set_z_index(-2)
    ax.add_to_back(panel)
    cv = ax.plot(lambda x: mm(x, vmax), x_range=[0, 32], color=BLUE, stroke_width=7)
    xl = T("substrate concentration [S]", 28, YELLOW).next_to(ax, DOWN, buff=0.25)
    yl = T("initial velocity", 28, GREEN).rotate(PI / 2).next_to(ax, LEFT, buff=0.25)
    return ax, cv, xl, yl


def moving_curve_dot(scene, ax, vmax=V_MAX, lo=1.0, hi=30.0, period=4.0,
                     show_tag=True, gate=False, stem_to_bottom=False, opaque=False):
    # The travelling booth is intentionally large enough to read as the carried plaza icon,
    # rather than as a decorative pulse on a mostly still graph.
    get_vmax = vmax.get_value if isinstance(vmax, ValueTracker) else (lambda v=vmax: v)
    box = RoundedRectangle(width=1.12, height=0.86, corner_radius=0.12,
                           stroke_color=BLUE, stroke_width=4,
                           fill_color="#13222E" if opaque else BLUE,
                           fill_opacity=0.96 if opaque else 0.38)
    parts = [box]
    if show_tag:
        parts.append(T("E", 28, TEXT, weight=BOLD).move_to(box))
    if gate:
        parts.append(Line(LEFT * 0.28, RIGHT * 0.28, color=RED, stroke_width=5).move_to(box.get_bottom() + UP * 0.18))
    dot = VGroup(*parts).move_to(ax.c2p(lo, mm(lo, get_vmax())))
    if opaque:
        dot.set_z_index(4)
    dot.clock = 0.0

    def travel(m, dt):
        m.clock += dt
        u = 0.5 + 0.5 * np.sin(TAU * m.clock / period - PI / 2)
        s = lo + (hi - lo) * u
        m.move_to(ax.c2p(s, mm(s, get_vmax())))

    dot.add_updater(travel)
    if stem_to_bottom:
        def mk_stem():
            y0 = ax.c2p(0, 0)[1]
            y_top = dot.get_bottom()[1]
            if y_top <= y0 + 0.05:
                return VMobject()
            return DashedLine([dot.get_x(), y0, 0], [dot.get_x(), y_top, 0],
                              color=YELLOW, stroke_width=5, dash_length=0.12).set_opacity(0.58)
        stem = always_redraw(mk_stem)
    else:
        stem = DashedLine(ax.c2p(lo, 0), ax.c2p(lo, mm(lo, get_vmax())),
                          color=YELLOW, stroke_width=5, dash_length=0.12).set_opacity(0.58)

        def follow(m, dt):
            m.put_start_and_end_on([dot.get_x(), ax.c2p(0, 0)[1], 0], dot.get_center())

        stem.add_updater(follow)
    scene.add(stem, dot)
    return dot


class S00Hook(SpokenScene, TitleCard):
    """The required first TitleCard class is used as the narrated visual hook."""
    LESSON = "Enzyme kinetics"
    TITLE = "Why doubling substrate stops doubling speed"

    def construct(self):
        booths = booth_row(y=-0.25, scale=0.92, busy=3, x0=-4.25, spacing=2.8)
        pulse_gates(booths)
        heading = T("ONE ENZYME ASSAY", 28, TEAL, weight=BOLD).to_edge(UP, buff=0.30)
        sub = counter_box("[S]", "12 mM", YELLOW, (-2.0, 2.35, 0))
        vel = counter_box("velocity", "45 micromoles/min", GREEN, (2.25, 2.35, 0), width=3.8)
        self.play(FadeIn(heading), FadeIn(booths), run_time=1.0)
        add_flow(self, y_values=(-2.65,), speed=1.25)
        self.at("Watch this enzyme")
        self.play(FadeIn(sub, shift=DOWN * 0.15), run_time=0.6)
        self.at("make 45")
        self.play(FadeIn(vel, shift=DOWN * 0.15), run_time=0.7)
        self.at("What happens")
        sub24 = counter_box("[S]", "24 mM", YELLOW, sub.get_center())
        q = counter_box("velocity", "?", GREEN, vel.get_center(), width=3.8)
        self.play(Transform(sub, sub24), Transform(vel, q), run_time=1.1)
        self.play(Indicate(vel, color=YELLOW, scale_factor=1.05), run_time=0.7)
        self.finish()


class S01Predict(Scene):
    def construct(self):
        booths = booth_row(y=-0.45, scale=0.90, busy=3, x0=-4.2, spacing=2.8)
        pulse_gates(booths)
        question = T("At 24 mM: 90 micromoles/min?", 48, TEXT, font=TITLE_FONT)
        fit(question, max_w=11.8)
        question.to_edge(UP, buff=0.45)
        q = M("?", 58, YELLOW).move_to([0, 2.0, 0])
        self.add(booths, question, q)
        add_flow(self, y_values=(-2.7, -2.15), speed=1.35)
        q.add_updater(lambda m, dt: m.set_opacity(0.62 + 0.38 * (0.5 + 0.5 * np.sin(self.renderer.time * 3))))
        self.wait(4.5)


class S02Title(Scene):
    def construct(self):
        booths = booth_row(y=-1.20, scale=0.82, busy=3, x0=-4.1, spacing=2.7).set_opacity(0.28)
        pulse_gates(booths)
        title = T("Why doubling substrate\nstops doubling speed", 52, TEXT,
                  font=TITLE_FONT, line_spacing=0.9).move_to(UP * 1.05)
        rule = Line(LEFT * 1.5, RIGHT * 1.5, color=GOLD, stroke_width=5).next_to(title, DOWN, buff=0.32)
        self.add(booths)
        add_flow(self, y_values=(-2.75,), speed=1.2, opacity=0.30)
        self.play(Write(title), GrowFromCenter(rule), run_time=1.2)
        self.wait(0.8)


class S03NoQueue(SpokenScene):
    def construct(self):
        schematic = T("SCHEMATIC", 28, GREY, weight=BOLD).to_edge(UP, buff=0.28)
        booths = booth_row(y=0.15, scale=1.0, busy=2, x0=-4.0, spacing=2.65)
        pulse_gates(booths)
        self.play(FadeIn(schematic), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in booths], lag_ratio=0.15), run_time=1.4)
        self.at("picture each enzyme")
        labels = VGroup(*[T("E", 30, BLUE, weight=BOLD).next_to(b, UP, buff=0.12) for b in booths])
        self.play(FadeIn(labels), run_time=0.5)
        self.at("with no waiting lane")
        no_queue = T("NO WAITING LANE", 32, RED, weight=BOLD).move_to([0, -2.7, 0])
        self.play(FadeIn(no_queue), run_time=0.5)
        self.at("A substrate car")
        s = car().move_to([-6.1, -1.55, 0])
        self.play(FadeIn(s), s.animate.move_to(booths[2].get_center()), run_time=1.0)
        self.at("only an empty booth")
        self.play(Transform(booths[2], set_booth_state(booths[2], True)), run_time=0.55)
        self.at("converts that car")
        p = car("P", GREEN).move_to(s)
        self.play(Transform(s, p), run_time=0.45)
        self.at("to product")
        self.play(s.animate.move_to([6.2, -1.55, 0]), run_time=0.8)
        self.at("then opens again")
        rejected = car().move_to([-6.0, -2.0, 0])
        loop = ArcBetweenPoints([-2.8, -1.8, 0], [-5.6, -2.55, 0], angle=-1.2, color=YELLOW, stroke_width=4)
        self.play(Transform(booths[2], set_booth_state(booths[2], False)), FadeIn(rejected), Create(loop), run_time=0.65)
        self.play(MoveAlongPath(rejected, loop), run_time=0.8)
        self.finish()


class S04LowSubstrate(SpokenScene):
    def construct(self):
        booths = booth_row(y=0.25, scale=0.92, busy=1, x0=-4.15, spacing=2.75)
        pulse_gates(booths)
        inc = counter_box("substrate in", "2", YELLOW, (-2.1, 2.4, 0))
        out = counter_box("product out", "2", GREEN, (2.1, 2.4, 0))
        self.add(booths)
        flow = add_flow(self, y_values=(-2.5,), speed=0.75)
        self.play(FadeIn(inc), FadeIn(out), run_time=0.8)
        self.at("most booths stand empty")
        self.play(LaggedStart(*[Indicate(b, color=TEXT, scale_factor=1.03) for b in booths[1:]], lag_ratio=0.18), run_time=1.1)
        self.at("Nearly every extra car")
        extra = car().move_to([-6.0, -1.45, 0])
        self.play(extra.animate.move_to(booths[1].get_center()), run_time=0.8)
        self.play(Transform(extra, car("P", GREEN).move_to(extra)), extra.animate.move_to([6.0, -1.45, 0]), run_time=0.8)
        self.at("adding substrate")
        inc4 = counter_box("substrate in", "4", YELLOW, inc.get_center())
        out4 = counter_box("product out", "4", GREEN, out.get_center())
        self.play(Transform(inc, inc4), Transform(out, out4), flow.animate.set_opacity(1), run_time=0.8)
        self.at("almost proportionally")
        together = DoubleArrow(inc.get_right(), out.get_left(), color=TEXT, stroke_width=4, buff=0.15)
        self.play(GrowArrow(together), run_time=0.6)
        self.at("limiting factor is arrivals")
        limit = T("LIMIT: ARRIVALS", 34, YELLOW, weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(limit, shift=UP * 0.1), run_time=0.6)
        self.at("not the booth's working speed")
        self.play(Indicate(VGroup(*[b[1] for b in booths]), color=BLUE, scale_factor=1.0), run_time=0.8)
        self.finish()


class S05FillingUp(SpokenScene):
    def construct(self):
        booths = booth_row(y=0.25, scale=0.88, busy=1, x0=-4.2, spacing=2.8)
        pulse_gates(booths)
        inc = counter_box("substrate in", "4", YELLOW, (-2.2, 2.45, 0))
        out = counter_box("product out", "4", GREEN, (1.7, 2.45, 0))
        gauge = busy_gauge(0.25, center=(5.65, 0.65, 0), height=3.35)
        self.add(booths, inc, out, gauge)
        thin = add_flow(self, y_values=(-2.55,), speed=1.0)
        self.at("Add more substrate")
        thick = add_flow(self, y_values=(-2.05,), speed=1.35)
        inc12 = counter_box("substrate in", "12", YELLOW, inc.get_center())
        self.play(Transform(inc, inc12), FadeIn(thick), run_time=0.7)
        self.at("empty booths become scarce")
        target = booth_row(y=0.25, scale=0.88, busy=3, x0=-4.2, spacing=2.8)
        self.play(Transform(booths, target), Transform(gauge, busy_gauge(0.75, gauge.get_center(), 3.35)), run_time=1.0)
        self.at("Cars finding busy booths")
        rejected = car().move_to([-5.9, -1.35, 0])
        loop = ArcBetweenPoints([-1.9, -1.25, 0], [-5.7, -2.75, 0], angle=-1.0, color=YELLOW, stroke_width=5)
        self.play(FadeIn(rejected), Create(loop), run_time=0.5)
        self.play(MoveAlongPath(rejected, loop), run_time=1.0)
        self.at("Product still flows")
        out9 = counter_box("product out", "9", GREEN, out.get_center())
        self.play(Transform(out, out9), run_time=0.6)
        self.at("each added car")
        taper = T("+8 arrivals  →  +5 products", 32, TEXT, weight=BOLD,
                  t2c={"+8": YELLOW, "+5": GREEN}).move_to([0, -3.15, 0])
        self.play(FadeIn(taper, shift=UP * 0.1), run_time=0.7)
        self.at("less extra speed")
        self.play(Indicate(out, color=GREEN, scale_factor=1.06), run_time=0.7)
        self.finish()


class S06GuidingIdea(SpokenScene):
    def construct(self):
        booths = booth_row(y=-0.55, scale=0.62, busy=2, x0=-5.4, spacing=1.7)
        pulse_gates(booths, speed=2.0)
        flow = add_flow(self, y_values=(-2.55,), speed=1.2, x_range=(-6.5, 0.5))
        self.add(booths)
        title = T("THE GUIDING IDEA", 30, TEAL, weight=BOLD).move_to([3.4, 2.6, 0])
        self.at("Here is the guiding idea")
        self.play(FadeIn(title), run_time=0.5)
        self.at("Velocity equals")
        v = T("velocity", 42, GREEN, weight=BOLD).move_to([1.35, 1.35, 0])
        eq = M("=", 42).next_to(v, RIGHT, buff=0.25)
        self.play(FadeIn(v), FadeIn(eq), run_time=0.6)
        self.at("kcat")
        kcat = T("kcat", 42, GREEN, weight=BOLD).next_to(eq, RIGHT, buff=0.25)
        metro = VGroup(*[Line(ORIGIN, UP * 0.55, color=GREEN, stroke_width=6).rotate(a) for a in (-0.35, 0.35)])
        metro.next_to(kcat, DOWN, buff=0.35)
        self.play(FadeIn(kcat), Create(metro), run_time=0.6)
        self.at("one busy enzyme's turnover pace")
        self.play(Indicate(booths[0], color=GREEN, scale_factor=1.08), run_time=0.8)
        self.at("times the amount")
        times = M("×", 42).next_to(kcat, RIGHT, buff=0.25)
        busy = T("busy enzyme", 42, BLUE, weight=BOLD).next_to(times, RIGHT, buff=0.25)
        formula = VGroup(v, eq, kcat, times, busy)
        fit(formula, max_w=6.2)
        formula.move_to([3.25, 1.25, 0])
        self.play(FadeIn(times), FadeIn(busy), run_time=0.7)
        self.at("Substrate changes the busy amount")
        more = booth_row(y=-0.55, scale=0.62, busy=4, x0=-5.4, spacing=1.7)
        self.play(Transform(booths, more), flow.animate.set_opacity(1), run_time=1.0)
        self.at("cannot make each busy enzyme")
        same = T("same turnover pace", 32, GREEN, weight=BOLD).move_to([3.4, -1.0, 0])
        self.play(FadeIn(same), Indicate(metro, color=GREEN, scale_factor=1.0), run_time=0.7)
        self.at("work faster")
        self.play(Indicate(booths[0], color=BLUE, scale_factor=1.04), run_time=0.7)
        self.finish()


class S07CurveEmerges(SpokenScene):
    def construct(self):
        booths = booth_row(y=-1.55, scale=0.45, busy=2, x0=-5.75, spacing=1.2)
        self.add(booths)
        self.at("transform the toll plaza")
        ax, cv, xl, yl = graph_world()
        tiny_plaza = fraction_booths(2, center=(-4.55, -1.90, 0), label="toll plaza")
        tiny_plaza.remove(tiny_plaza[1])
        tiny_plaza.scale(0.72)
        self.play(Transform(booths, tiny_plaza), Create(ax), run_time=0.8)
        self.play(FadeOut(booths), run_time=0.3)
        icon = moving_curve_dot(self, ax, period=3.5)
        self.at("Substrate concentration")
        self.play(FadeIn(xl, shift=UP * 0.1), run_time=0.55)
        self.at("Initial velocity")
        self.play(FadeIn(yl, shift=RIGHT * 0.1), run_time=0.55)
        samples = [0.5, 1, 2, 4, 8, 12, 20, 32]
        dots = VGroup(*[Dot(ax.c2p(s, mm(s)), radius=0.10, color=GREEN) for s in samples])
        self.at("moving car counter becomes points")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.12), run_time=1.5)
        self.at("Michaelis")
        self.play(Create(cv), run_time=1.5)
        self.at("computed from the equation")
        tag = T("COMPUTED", 30, TEAL, weight=BOLD).move_to([4.7, 2.85, 0])
        self.play(FadeIn(tag), run_time=0.6)
        self.finish()


class S08Equation(SpokenScene):
    def construct(self):
        ax, cv, xl, yl = graph_world(origin=(-5.25, -2.70), width=8.15, height=4.05)
        self.add(ax, cv, xl, yl)
        moving_curve_dot(self, ax, period=3.5)
        self.at("Velocity equals")
        equation = M("v = Vmax × [S] / (Km + [S])", 34, TEXT,
                     t2c={"Vmax": RED, "[S]": YELLOW, "Km": GOLD_KM})
        equation.to_edge(UP, buff=0.25)
        self.play(Write(equation), run_time=1.5)
        self.at("The fraction")
        fraction = M("[S] / (Km + [S])", 32, BLUE, weight=BOLD).move_to([4.55, 1.55, 0])
        self.play(FadeIn(fraction), run_time=0.6)
        self.at("share of enzyme")
        row = fraction_booths(1, center=(4.55, 0.15, 0))
        self.play(FadeIn(row), run_time=0.6)
        self.at("As that share approaches one")
        self.play(Transform(row, fraction_booths(4, center=(4.55, 0.15, 0))), run_time=1.0)
        self.at("velocity approaches Vmax")
        ceiling = DashedLine(ax.c2p(0, V_MAX), ax.c2p(32, V_MAX), color=RED, stroke_width=4)
        lab = T("Vmax = 60", 28, RED, weight=BOLD).next_to(ceiling, UP, buff=0.10).align_to(ceiling, RIGHT)
        self.play(Create(ceiling), FadeIn(lab), run_time=0.8)
        self.finish()


class S09Km(SpokenScene):
    def construct(self):
        ax, cv, xl, yl = graph_world(origin=(-5.25, -2.65), width=8.15, height=4.25)
        ceiling = DashedLine(ax.c2p(0, 60), ax.c2p(32, 60), color=RED, stroke_width=3)
        self.add(ax, cv, xl, yl, ceiling)
        self.at("Km marks")
        point = Dot(ax.c2p(4, 30), radius=0.14, color=GOLD_KM)
        vline = DashedLine(ax.c2p(4, 0), ax.c2p(4, 30), color=GOLD_KM, stroke_width=4)
        hline = DashedLine(ax.c2p(0, 30), ax.c2p(4, 30), color=GOLD_KM, stroke_width=4)
        self.play(Create(vline), FadeIn(point), run_time=0.75)
        km = T("Km = 4 mM", 30, GOLD_KM, weight=BOLD).next_to(ax.c2p(4, 0), DOWN, buff=0.12)
        self.play(FadeIn(km), run_time=0.5)
        self.at("busy fraction is one")
        row = fraction_booths(2, center=(4.55, 1.45, 0))
        self.play(FadeIn(row), run_time=0.7)
        self.at("Therefore")
        self.play(Create(hline), run_time=0.65)
        self.at("half of Vmax")
        half = T("30 = one half Vmax", 30, GOLD_KM, weight=BOLD).next_to(hline, UP, buff=0.12).shift(RIGHT * 0.7)
        self.play(FadeIn(half), run_time=0.6)
        self.at("half speed point")
        meaning = chip("half-speed point", GOLD_KM, size=30).move_to([4.55, -0.35, 0])
        self.play(FadeIn(meaning), run_time=0.6)
        self.at("not automatically")
        affinity = chip("affinity", RED, size=30).move_to([4.55, -1.65, 0])
        cross = Cross(affinity, stroke_color=RED, stroke_width=6)
        self.play(FadeIn(affinity), Create(cross), run_time=0.7)
        self.finish()


class S10Vmax(SpokenScene):
    def construct(self):
        ax, cv, xl, yl = graph_world(origin=(-5.25, -2.45), width=6.8, height=4.15, y_max=130)
        # graph_world computes the curve at the requested Vmax; here start at 60 on a 130 scale
        cv60 = ax.plot(lambda x: mm(x, 60), x_range=[0, 32], color=BLUE, stroke_width=7)
        cv.become(cv60)
        ceiling = DashedLine(ax.c2p(0, 60), ax.c2p(32, 60), color=RED, stroke_width=4)
        self.add(ax, cv, xl, yl, ceiling)
        vmax_tr = ValueTracker(60.0)
        moving_curve_dot(self, ax, vmax_tr, lo=14, hi=31, period=5.0,
                         show_tag=False, gate=True, stem_to_bottom=True, opaque=True)
        self.at("nearly every enzyme is busy")
        row = fraction_booths(4, center=(4.85, 1.85, 0))
        self.play(FadeIn(row), run_time=0.7)
        self.at("It equals")
        equation = T("Vmax = kcat ×\ntotal enzyme", 30, TEXT, weight=BOLD,
                     line_spacing=0.82,
                     t2c={"Vmax": RED, "kcat": GREEN, "enzyme": BLUE})
        equation.move_to([4.85, 0.75, 0])
        self.play(FadeIn(equation), run_time=0.75)
        self.at("More substrate")
        cars = VGroup(*[car(label=None, scale=0.55).move_to([3.29 + i * 0.78, -0.35, 0]) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in cars], lag_ratio=0.10), run_time=0.8)
        self.at("cannot raise that ceiling")
        self.play(Indicate(ceiling, color=RED, scale_factor=1.0), run_time=0.7)
        self.at("adding enzyme can")
        cv120 = ax.plot(lambda x: mm(x, 120), x_range=[0, 32], color=BLUE, stroke_width=7)
        ceiling120 = DashedLine(ax.c2p(0, 120), ax.c2p(32, 120), color=RED, stroke_width=4)
        gauge_box = RoundedRectangle(width=2.55, height=0.68, corner_radius=0.14,
                                     stroke_color=BLUE, stroke_width=3,
                                     fill_color=BLUE, fill_opacity=0.10)
        gauge_num = M("1×  →  2×", 30, TEXT).move_to(gauge_box)
        gauge_lab = T("enzyme amount", 28, BLUE, weight=BOLD).next_to(gauge_box, UP, buff=0.14)
        gauge = VGroup(gauge_box, gauge_lab, gauge_num).move_to((4.85, -1.65, 0))
        self.play(FadeOut(cars), FadeOut(row), FadeIn(gauge),
                  Transform(cv, cv120), Transform(ceiling, ceiling120),
                  vmax_tr.animate.set_value(120.0), run_time=1.3)
        self.finish()


class S11Calculation(SpokenScene):
    def construct(self):
        ax, cv, xl, yl = graph_world(origin=(-5.15, -1.25), width=6.75, height=3.20)
        vmax_line = DashedLine(ax.c2p(0, 60), ax.c2p(32, 60), color=RED, stroke_width=3)
        booths = fraction_booths(0, center=(4.65, 1.35, 0), label="enzyme booths")
        pulse_gates(booths[0])
        self.add(ax, cv, xl, yl, vmax_line, booths)

        s_tr = ValueTracker(2.0)
        marker_box = RoundedRectangle(width=0.66, height=0.48, corner_radius=0.10,
                                      stroke_color=BLUE, stroke_width=4,
                                      fill_color=BLUE, fill_opacity=0.40)
        marker_gate = Line(LEFT * 0.20, RIGHT * 0.20, color=RED, stroke_width=4)
        marker_gate.move_to(marker_box.get_bottom() + UP * 0.11)
        marker = VGroup(marker_box, marker_gate)
        marker.add_updater(lambda m: m.move_to(ax.c2p(s_tr.get_value(), mm(s_tr.get_value()))))
        stem = DashedLine(ax.c2p(2.0, 0), ax.c2p(2.0, mm(2.0)),
                          color=YELLOW, stroke_width=4, dash_length=0.12).set_opacity(0.65)
        stem.add_updater(lambda m: m.put_start_and_end_on(
            ax.c2p(s_tr.get_value(), 0),
            ax.c2p(s_tr.get_value(), mm(s_tr.get_value())),
        ))
        self.add(stem, marker)

        self.at("60")
        vmax_lab = T("Vmax = 60 µmol/min", 28, RED, weight=BOLD).move_to([-3.65, 3.15, 0])
        self.play(FadeIn(vmax_lab), Indicate(vmax_line, color=RED, scale_factor=1.0), run_time=0.6)

        self.at("4 millimolar")
        km_lab = T("Km = 4 mM", 28, GOLD_KM, weight=BOLD).move_to([0.35, 3.15, 0])
        sub_strip = M("v = 60 × [S]/(4+[S])", 26, TEXT, t2c={"60": RED}).move_to([4.65, -1.40, 0])
        self.play(FadeIn(km_lab), FadeIn(sub_strip), run_time=0.55)

        self.at("At 12")
        p12 = Dot(ax.c2p(12, mm(12)), radius=0.13, color=GREEN).set_z_index(5)
        s_lab = T("[S] = 12 mM", 28, YELLOW, weight=BOLD).move_to([4.65, 3.15, 0])
        v_readout = T("v = ?", 34, GREEN, weight=BOLD).move_to([4.65, -0.35, 0])
        sub_12 = M("v = 60 × 12/(4+12)", 26, TEXT, t2c={"60": RED}).move_to(sub_strip)
        self.play(
            s_tr.animate.set_value(12.0),
            FadeIn(p12),
            FadeIn(s_lab),
            FadeIn(v_readout),
            Succession(FadeOut(sub_strip, run_time=0.22), FadeIn(sub_12, run_time=0.28)),
            run_time=0.8,
        )
        sub_strip = sub_12

        s12_1 = M("12/(4+12)", 28, YELLOW)
        s12_2 = M("= 12/16", 28, TEXT)
        s12_3 = M("= 3/4", 28, BLUE)
        s12_4 = M("→ 45", 28, GREEN)
        VGroup(s12_1, s12_2, s12_3, s12_4).arrange(RIGHT, buff=0.22).move_to([0, -3.12, 0])

        self.at("12 over 4")
        self.play(FadeIn(s12_1), run_time=0.5)

        self.at("12 sixteenths")
        self.play(FadeIn(s12_2), run_time=0.5)

        self.at("three quarters")
        booths_3 = fraction_booths(3, center=(4.65, 1.35, 0), label="3/4 busy")
        self.play(FadeIn(s12_3), Transform(booths, booths_3), run_time=0.65)

        self.at("Three quarters of 60")
        self.play(Indicate(s12_3, color=BLUE, scale_factor=1.06),
                  Indicate(sub_strip, color=RED, scale_factor=1.03), run_time=0.6)

        self.at("is 45")
        v_45 = T("v = 45", 34, GREEN, weight=BOLD).move_to(v_readout)
        self.play(
            FadeIn(s12_4),
            Succession(FadeOut(v_readout, run_time=0.18), FadeIn(v_45, run_time=0.27)),
            run_time=0.45,
        )
        v_readout = v_45

        self.at("24", lead=0.1)
        p24 = Dot(ax.c2p(24, mm(24)), radius=0.13, color=YELLOW).set_z_index(5)
        s_lab_24 = T("[S] = 24 mM", 28, YELLOW, weight=BOLD).move_to(s_lab)
        sub_24 = M("v = 60 × 24/(4+24)", 26, TEXT, t2c={"60": RED}).move_to(sub_strip)
        v_q2 = T("v = ?", 34, GREEN, weight=BOLD).move_to(v_readout)

        g_box = RoundedRectangle(width=0.72, height=1.75, corner_radius=0.10,
                                 stroke_color=GREY, stroke_width=3).move_to([5.45, 1.25, 0])
        g_frac = ValueTracker(0.0)
        g_fill = always_redraw(lambda: Rectangle(
            width=0.60,
            height=max(0.02, (1.75 - 0.12) * g_frac.get_value()),
            stroke_width=0, fill_color=BLUE, fill_opacity=0.9,
        ).move_to(g_box.get_bottom() + UP * (0.06 + max(0.02, (1.75 - 0.12) * g_frac.get_value()) / 2)))
        g_lab = T("? busy", 28, BLUE, weight=BOLD).next_to(g_box, LEFT, buff=0.28)
        for b in booths[0]:
            b[1].clear_updaters()
        self.play(
            s_tr.animate.set_value(24.0),
            FadeIn(p24),
            Succession(FadeOut(s_lab, run_time=0.25), FadeIn(s_lab_24, run_time=0.35)),
            Succession(FadeOut(sub_strip, run_time=0.25), FadeIn(sub_24, run_time=0.35)),
            Succession(FadeOut(v_readout, run_time=0.25), FadeIn(v_q2, run_time=0.35)),
            Succession(FadeOut(booths, run_time=0.25), AnimationGroup(FadeIn(g_box), FadeIn(g_lab), run_time=0.35)),
            FadeOut(VGroup(s12_1, s12_2, s12_3, s12_4)),
            run_time=0.85,
        )
        self.add(g_fill)
        s_lab = s_lab_24
        sub_strip = sub_24
        v_readout = v_q2

        s24_1 = M("24/(4+24)", 28, YELLOW)
        s24_2 = M("= 24/28", 28, TEXT)
        s24_3 = M("= 6/7", 28, BLUE)
        s24_4 = M("→ about 51", 28, GREEN)
        VGroup(s24_1, s24_2, s24_3, s24_4).arrange(RIGHT, buff=0.22).move_to([0, -3.12, 0])

        self.at("4 plus 24")
        self.play(FadeIn(s24_1), run_time=0.5)

        self.at("28")
        self.play(FadeIn(s24_2), run_time=0.55)

        self.at("six sevenths")
        g_lab_67 = T("6/7 busy", 28, BLUE, weight=BOLD).next_to(g_box, LEFT, buff=0.28)
        self.play(
            FadeIn(s24_3),
            g_frac.animate.set_value(6 / 7),
            Succession(FadeOut(g_lab, run_time=0.2), FadeIn(g_lab_67, run_time=0.3)),
            run_time=0.65,
        )
        g_lab = g_lab_67

        self.at("sevenths of 60")
        self.play(Indicate(s24_3, color=BLUE, scale_factor=1.06),
                  Indicate(sub_strip, color=RED, scale_factor=1.03), run_time=0.6)

        self.at("about 51")
        v_51 = T("v ≈ 51", 34, GREEN, weight=BOLD).move_to(v_readout)
        self.play(
            FadeIn(s24_4),
            Succession(FadeOut(v_readout, run_time=0.18), FadeIn(v_51, run_time=0.27)),
            Indicate(p24, color=YELLOW, scale_factor=1.3),
            run_time=0.5,
        )
        self.finish()


class S12Payoff(SpokenScene):
    def construct(self):
        ax, cv, xl, yl = graph_world(origin=(-5.35, -2.45), width=6.8, height=4.55)
        self.add(ax, cv, xl, yl)
        moving_curve_dot(self, ax, lo=0.2, hi=24, period=3.5,
                         show_tag=False, gate=True, stem_to_bottom=True, opaque=True)
        low_a, low_b = 0.2, 0.4
        self.at("Doubling substrate")
        p12 = Dot(ax.c2p(12, mm(12)), radius=0.14, color=YELLOW).set_z_index(5)
        p24 = Dot(ax.c2p(24, mm(24)), radius=0.14, color=YELLOW).set_z_index(5)
        bracket = DoubleArrow(ax.c2p(12, 8), ax.c2p(24, 8), color=YELLOW, stroke_width=5, buff=0)
        self.play(FadeIn(p12), FadeIn(p24), GrowArrow(bracket), run_time=0.8)
        self.at("only about 14 percent")
        gain = T("45 → 51\n+14%", 38, GREEN, weight=BOLD, line_spacing=0.85).move_to([4.95, 2.15, 0])
        self.play(FadeIn(gain, shift=UP * 0.1), run_time=0.65)
        self.at("one quarter")
        gauge = busy_gauge(0.75, center=(5.45, -0.25, 0), height=2.7, label=False)
        empty = T("1/4 empty", 30, BLUE, weight=BOLD).next_to(gauge[0], LEFT, buff=0.22)
        self.play(FadeIn(gauge), FadeIn(empty), run_time=0.7)
        self.at("Far below Km")
        pa = Dot(ax.c2p(low_a, mm(low_a)), radius=0.14, color=GREEN).set_z_index(5)
        pb = Dot(ax.c2p(low_b, mm(low_b)), radius=0.14, color=GREEN).set_z_index(5)
        low = low_s_comparison(center=(4.95, 0.15, 0), width=3.1)
        self.play(
            Succession(
                AnimationGroup(FadeOut(bracket), FadeOut(gain), FadeOut(gauge), FadeOut(empty), run_time=0.35),
                AnimationGroup(FadeIn(pa), FadeIn(pb), FadeIn(low), run_time=0.55),
            )
        )
        self.at("nearly doubles velocity")
        almost = T("NEARLY 2×", 32, GREEN, weight=BOLD).move_to([4.95, -2.05, 0])
        self.play(FadeIn(almost), run_time=0.6)
        self.at("Near saturation")
        self.play(FadeOut(VGroup(pa, pb, low, almost)), FadeIn(p12), FadeIn(p24), run_time=0.7)
        self.at("barely helps")
        small = T("45 → 51\nsmall gain", 34, GREEN, weight=BOLD, line_spacing=0.85).move_to([4.95, 0.25, 0])
        self.play(FadeIn(small), run_time=0.6)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        question = T("How much enzyme is still empty?", 46, TEXT, font=TITLE_FONT).to_edge(UP, buff=0.35)
        booths = booth_row(y=0.0, scale=0.95, busy=1, x0=-4.2, spacing=2.8)
        pulse_gates(booths)
        self.at("ask how much enzyme")
        self.play(FadeIn(question), FadeIn(booths), run_time=1.1)
        add_flow(self, y_values=(-2.35,), speed=1.0)
        self.at("before predicting")
        predict = T("PREDICT THE SUBSTRATE EFFECT", 30, YELLOW, weight=BOLD).move_to([0, -3.15, 0])
        self.play(FadeIn(predict), run_time=0.55)
        self.at("The curve bends")
        more = booth_row(y=0.0, scale=0.95, busy=3, x0=-4.2, spacing=2.8)
        self.play(Transform(booths, more), run_time=1.0)
        self.at("busy fraction approaches one")
        frac = T("busy fraction → 1", 34, BLUE, weight=BOLD).move_to([0, 2.4, 0])
        self.play(Transform(question, frac), run_time=0.7)
        self.at("not because catalysis stops")
        working = T("STILL WORKING", 32, GREEN, weight=BOLD).move_to([0, -2.8, 0])
        self.play(FadeOut(predict), FadeIn(working), Indicate(booths, color=GREEN, scale_factor=1.02), run_time=0.8)
        self.at("More substrate adds speed")
        takeaway = T("More substrate adds speed only by filling empty enzymes.", 36, TEXT, font=TITLE_FONT)
        fit(takeaway, max_w=12.1)
        takeaway.move_to([0, -3.15, 0])
        self.play(FadeOut(working), FadeIn(takeaway), run_time=0.75)
        self.finish()


class S14End(EndCard):
    LINE = "More substrate adds speed only by filling empty enzymes."
