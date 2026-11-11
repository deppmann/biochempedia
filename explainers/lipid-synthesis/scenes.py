"""The cholesterol gauge — one carried cell world, timed to audio/words.json.

COLOR MAP
  YELLOW  cholesterol and LDL cargo
  BLUE    membranes, ER, and the cholesterol gauge
  GREEN   working import / synthesis flow
  RED     statin inhibition and non-working receptors
  TEAL    regulatory machinery (SCAP / SREBP-2)
  GREY    structure and inactive paths

All pathway drawings are explicitly schematic; no molecular structures are shown.
"""
from bp_style import *  # noqa: F401,F403


# ---------- carried-world geometry -------------------------------------------------
MEM_X = -4.35
ER_X = 2.75
ER_Y = 0.25
GOLD = YELLOW
DARK = "#252a35"


def arrow(a, b, color=GREEN, width=7, dashed=False):
    cls = DashedLine if dashed else Arrow
    kw = dict(color=color, stroke_width=width)
    if not dashed:
        kw.update(buff=0, max_tip_length_to_length_ratio=0.12)
    return cls(a, b, **kw)


def ldl(pos, r=0.25, opacity=1):
    ring = Circle(r, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.16)
    core = Dot(radius=r * 0.35, color=GOLD)
    return VGroup(ring, core).move_to(pos).set_opacity(opacity)


def cholesterol(pos, r=0.11):
    return Dot(pos, radius=r, color=GOLD)


def membrane(x=MEM_X):
    return VGroup(
        Line([x - 0.13, -3.05, 0], [x - 0.13, 3.05, 0], color=BLUE, stroke_width=5),
        Line([x + 0.13, -3.05, 0], [x + 0.13, 3.05, 0], color=BLUE, stroke_width=5),
    )


def receptor(y=1.5, color=GREEN):
    # A simple cup at the surface, open to blood on the left.
    return VGroup(
        Arc(radius=0.34, start_angle=-PI / 2, angle=PI, color=color, stroke_width=7),
        Line([0.0, -0.33, 0], [0.32, -0.33, 0], color=color, stroke_width=7),
        Line([0.0, 0.33, 0], [0.32, 0.33, 0], color=color, stroke_width=7),
    ).move_to([MEM_X - 0.08, y, 0])


def gauge(level=0.55, center=(ER_X, ER_Y, 0), scale=1.0):
    c = np.array(center, dtype=float)
    arc = Arc(radius=1.05 * scale, start_angle=PI, angle=-PI,
              color=BLUE, stroke_width=9).move_arc_center_to(c)
    ticks = VGroup(*[
        Line(c + np.array([np.cos(PI - i * PI / 6), np.sin(PI - i * PI / 6), 0]) * 0.84 * scale,
             c + np.array([np.cos(PI - i * PI / 6), np.sin(PI - i * PI / 6), 0]) * 1.03 * scale,
             color=TEXT, stroke_width=3)
        for i in range(7)
    ])
    ang = PI - np.clip(level, 0, 1) * PI
    needle = Line(c, c + np.array([np.cos(ang), np.sin(ang), 0]) * 0.78 * scale,
                  color=GOLD, stroke_width=7)
    hub = Dot(c, radius=0.10 * scale, color=GOLD)
    lab = T("ER cholesterol", 28, BLUE, weight=BOLD).next_to(arc, DOWN, buff=0.22)
    return VGroup(arc, ticks, needle, hub, lab)


def er_ribbon():
    top = CubicBezier([0.75, 0.8, 0], [1.5, 1.25, 0], [3.7, 1.25, 0], [4.85, 0.75, 0])
    bot = CubicBezier([0.75, 0.45, 0], [1.5, 0.9, 0], [3.7, 0.9, 0], [4.85, 0.4, 0])
    return VGroup(top, bot).set_stroke(BLUE, width=6)


def synth_valve(blocked=False):
    body = RoundedRectangle(corner_radius=0.16, width=1.55, height=0.92,
                            stroke_color=GREEN, stroke_width=4,
                            fill_color=GREEN, fill_opacity=0.12)
    lab = T("build", 30, GREEN, weight=BOLD).move_to(body)
    g = VGroup(body, lab).move_to([-1.8, -2.15, 0])
    if blocked:
        stop = VGroup(Line(UL * 0.38, DR * 0.38, color=RED, stroke_width=9),
                      Line(DL * 0.38, UR * 0.38, color=RED, stroke_width=9)).move_to(g)
        g.add(stop)
    return g


def full_world(cell_name="liver cell", level=0.55, blocked=False, receptor_count=1,
               fh=False, question=False):
    """Same landmarks in every full-cell scene."""
    interior = RoundedRectangle(corner_radius=0.28, width=10.55, height=6.3,
                                stroke_width=0, fill_color=BLUE,
                                fill_opacity=0.22).move_to([1.05, 0, 0])
    mem = membrane()
    blood = RoundedRectangle(corner_radius=0.2, width=1.65, height=6.3,
                             stroke_color=BLUE, stroke_width=3,
                             fill_color=BLUE, fill_opacity=0.06).move_to([-5.55, 0, 0])
    blood_lab = T("blood", 28, BLUE, weight=BOLD).move_to([-5.55, 2.78, 0])
    cell_lab = T(cell_name, 28, TEXT, weight=BOLD).move_to([-3.15, 3.2, 0])
    recs = VGroup(*[receptor(1.75 - i * 0.72, RED if fh else GREEN) for i in range(receptor_count)])
    if fh:
        # Keep the disease tag clear of both the membrane and the import arrow.
        recs.add(T("FH", 28, RED, weight=BOLD).move_to([MEM_X + 0.75, 2.35, 0]))
    er = er_ribbon()
    g = gauge(level)
    build = synth_valve(blocked)
    import_path = arrow([MEM_X + 0.45, 1.75, 0], [1.15, 0.72, 0], GREEN, 8)
    make_path = arrow([-0.95, -2.15, 0], [2.05, -0.62, 0], GREEN, 8)
    schematic = T("schematic", 28, GREY).move_to([5.15, -3.22, 0])
    group = VGroup(blood, blood_lab, mem, cell_lab, recs, er, g, build,
                   import_path, make_path, schematic)
    group.add_to_back(interior)
    if question:
        q = T("?", 70, GOLD, weight=BOLD).move_to([-3.45, 1.75, 0])
        group.add(q)
    return group


def drifting_ldl(scene, ys=(-2.4, -1.2, 0.1, 1.25, 2.35), speed=0.30):
    dots = VGroup(*[ldl([-5.55, y, 0], 0.22) for y in ys])
    for i, d in enumerate(dots):
        d.phase = (i * 1.07) % 6.0

        def drift(m, dt):
            m.phase = (m.phase + speed * dt) % 6.0
            # Leave a clean label lane at the top of the blood channel.
            m.set_y(-2.45 + m.phase * 0.78)
        d.add_updater(drift)
    scene.add(dots)
    return dots


def belt_tokens(scene, y=-2.15, x0=-1.05, x1=2.0, n=5, speed=0.25):
    toks = VGroup(*[cholesterol([x0, y, 0]) for _ in range(n)])
    for i, d in enumerate(toks):
        d.u = i / n

        def move(m, dt):
            m.u = (m.u + speed * dt) % 1
            u = m.u
            m.move_to([interpolate(x0, x1, u), interpolate(y, -0.65, u), 0])
        d.add_updater(move)
    scene.add(toks)
    return toks


# ---------- scenes ----------------------------------------------------------------
class S00Hook(SpokenScene):
    def construct(self):
        world = full_world("skin cell", level=0.18, receptor_count=1)
        # Reveal the puzzle before naming it.
        self.play(FadeIn(world[0:5]), FadeIn(world[6:]), run_time=0.9)
        ldls = drifting_ldl(self, ys=(-2.5, -1.6, -0.7, 0.3, 1.3, 2.25), speed=0.36)
        belt = belt_tokens(self, speed=0.32)
        self.play(FadeIn(ldls), FadeIn(belt), FadeIn(world[5]), run_time=0.7)
        self.at("Why would a cell")
        question = T("Why keep making more?", 40, GOLD, font=TITLE_FONT).move_to([0.15, 2.55, 0])
        self.play(Write(question), run_time=0.8)
        self.at("Brown and Goldstein")
        names = T("Brown + Goldstein", 28, TEXT).move_to([0.15, 1.90, 0])
        self.play(FadeIn(names), run_time=0.5)
        self.at("skin cells")
        self.play(Indicate(world[4], color=TEXT, scale_factor=1.08), run_time=0.7)
        self.at("familial hypercholesterolemia")
        fh = chip("familial hypercholesterolemia", RED, 28).move_to([0.15, 1.90, 0])
        self.play(FadeOut(names), FadeIn(fh), run_time=0.8)
        self.at("LDL crowded")
        self.play(LaggedStart(*[Indicate(d, color=GOLD, scale_factor=1.25) for d in ldls], lag_ratio=0.08), run_time=1.1)
        self.at("cholesterol were scarce")
        self.play(Indicate(world[7], color=BLUE, scale_factor=1.08), run_time=0.8)
        self.finish()


class S01Title(Scene):
    def construct(self):
        world = full_world("skin cell", level=0.18)
        world.set_opacity(0.28)
        self.add(world)
        drifting_ldl(self, speed=0.27).set_opacity(0.28)
        belt_tokens(self, speed=0.25).set_opacity(0.35)
        shade = Rectangle(width=13.6, height=2.3, fill_color=BG, fill_opacity=0.72,
                          stroke_width=0)
        title = T("THE CHOLESTEROL GAUGE", 48, TEXT, font=TITLE_FONT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, 0.28)
        self.play(FadeIn(shade), Write(title), GrowFromCenter(rule), run_time=1.0)
        self.wait(0.55)
        self.play(FadeOut(VGroup(shade, title, rule)), run_time=0.45)


class S02TwoLines(SpokenScene):
    def construct(self):
        world = full_world("liver cell", level=0.42)
        self.play(FadeIn(world[0:8]), run_time=0.8)
        ldls = drifting_ldl(self, speed=0.28)
        self.at("two supply lines")
        self.play(FadeIn(world[8]), GrowArrow(world[10]), run_time=0.7)
        self.play(FadeIn(world[5]), GrowArrow(world[9]), run_time=0.7)
        make = belt_tokens(self, speed=0.25)
        self.at("build cholesterol")
        self.play(Indicate(world[8], color=GREEN), FadeIn(make), run_time=0.7)
        self.at("pull LDL from blood")
        incoming = ldl([-5.55, 1.75, 0])
        path = Line([-5.55, 1.75, 0], [1.15, 0.72, 0])
        self.add(incoming)
        self.play(MoveAlongPath(incoming, path), run_time=1.2, rate_func=linear)
        self.at("does not measure LDL outside")
        self.play(LaggedStart(*[Indicate(d, color=GOLD) for d in ldls], lag_ratio=0.08), run_time=1.0)
        self.at("cholesterol reaching")
        token = cholesterol([0.9, 0.75, 0], 0.15)
        self.add(token)
        self.play(token.animate.move_to([ER_X, ER_Y + 0.45, 0]), run_time=1.1)
        high = gauge(0.70)
        self.play(Transform(world[7], high), FadeOut(token, incoming), run_time=0.8)
        self.finish()


class S03Import(SpokenScene):
    def construct(self):
        # Zoomed upper route; landmarks retain the same left-to-right ordering.
        blood_fill = Rectangle(width=4.1, height=6.5, stroke_width=0,
                               fill_color=BLUE, fill_opacity=0.19).move_to([-4.15, 0, 0])
        cell_fill = Rectangle(width=8.0, height=6.5, stroke_width=0,
                              fill_color=TEAL, fill_opacity=0.09).move_to([2.25, 0, 0])
        bars = VGroup(Line([-2.1, -3.1, 0], [-2.1, 3.1, 0], color=BLUE, stroke_width=8),
                      Line([-1.75, -3.1, 0], [-1.75, 3.1, 0], color=BLUE, stroke_width=8))
        outside = T("blood", 30, BLUE, weight=BOLD).move_to([-4.8, 3.1, 0])
        inside = T("cell interior", 30, TEXT, weight=BOLD).move_to([2.3, 3.1, 0])
        rec = VGroup(Arc(0.72, -PI / 2, PI, color=GREEN, stroke_width=12),
                     Line([0, -0.7, 0], [0.7, -0.7, 0], color=GREEN, stroke_width=12),
                     Line([0, 0.7, 0], [0.7, 0.7, 0], color=GREEN, stroke_width=12)).move_to([-2.05, 0.9, 0])
        rec_lab = T("LDL receptor", 30, GREEN, weight=BOLD).next_to(rec, DOWN, 0.35)
        sch = T("schematic", 28, GREY).to_corner(DR, buff=0.45)
        er = VGroup(Line([2.2, -1.7, 0], [5.5, -1.7, 0], color=BLUE, stroke_width=8),
                    T("ER pool", 28, BLUE, weight=BOLD).move_to([3.8, -2.15, 0]), gauge(0.25, (4.65, 0.35, 0), 0.75))
        self.play(FadeIn(blood_fill, cell_fill), Create(bars), FadeIn(outside, inside, sch), run_time=0.8)
        particle = ldl([-4.8, 0.9, 0], 0.46)
        self.play(FadeIn(particle), run_time=0.4)
        self.at("receptor captures")
        self.play(FadeIn(rec, rec_lab), particle.animate.move_to([-2.35, 0.9, 0]), run_time=0.9)
        self.at("particle enters")
        caught = VGroup(rec, particle)
        self.play(caught.animate.shift(RIGHT * 1.4), FadeIn(er), run_time=1.1)
        self.at("its cholesterol joins")
        cargo = cholesterol([-0.95, 0.9, 0], 0.18)
        self.add(cargo)
        self.play(cargo.animate.move_to([3.8, -1.55, 0]), FadeOut(particle), run_time=1.2)
        pool_flow = VGroup(*[cholesterol([2.4 + i * 0.65, -1.55, 0], 0.13) for i in range(5)])
        for i, d in enumerate(pool_flow):
            d.u = i / 5

            def circulate(m, dt):
                m.u = (m.u + 0.16 * dt) % 1
                m.move_to([2.2 + 3.0 * m.u, -1.55 + 0.13 * np.sin(TAU * m.u), 0])
            d.add_updater(circulate)
        self.add(pool_flow)
        self.at("working receptor")
        self.play(Indicate(rec, color=GREEN, scale_factor=1.1), run_time=0.7)
        self.at("gauge can see")
        self.play(Transform(er[2], gauge(0.68, (4.65, 0.35, 0), 0.75)), run_time=0.8)
        # A second, slower capture maintains the causal motion as the sentence lands.
        p2 = ldl([-4.8, -0.5, 0], 0.34)
        self.play(FadeIn(p2), p2.animate.move_to([-0.9, -0.5, 0]), run_time=1.2)
        self.finish()


class S04Synthesis(SpokenScene):
    def construct(self):
        title = T("synthesis line  •  schematic", 28, GREY).to_edge(UP, buff=0.35)
        pipe1 = RoundedRectangle(corner_radius=0.32, width=4.8, height=1.25,
                                 stroke_color=GREEN, stroke_width=5,
                                 fill_color=GREEN, fill_opacity=0.18).move_to([-3.75, 0, 0])
        pipe2 = RoundedRectangle(corner_radius=0.32, width=4.8, height=1.25,
                                 stroke_color=GREEN, stroke_width=5,
                                 fill_color=GREEN, fill_opacity=0.18).move_to([3.75, 0, 0])
        valve_body = RoundedRectangle(corner_radius=0.18, width=2.8, height=1.45,
                                      stroke_color=TEAL, stroke_width=6,
                                      fill_color=DARK, fill_opacity=1)
        valve_lab = T("HMG-CoA reductase", 28, TEAL, weight=BOLD).next_to(
            valve_body, UP, buff=0.28
        )
        valve = VGroup(valve_body, valve_lab)
        acetyl = chip("acetyl-CoA", GOLD, 28).move_to([-5.0, 1.55, 0])
        hmg = chip("HMG-CoA", GOLD, 28).move_to([-2.75, 1.55, 0])
        meval = chip("mevalonate", GOLD, 28).move_to([3.0, 1.55, 0])
        self.play(FadeIn(title), FadeIn(pipe1), FadeIn(pipe2), run_time=0.8)
        self.at("acetylcoenzyme A")
        self.play(FadeIn(acetyl), run_time=0.5)
        flow_speed = ValueTracker(0.11)
        flow = VGroup(*[cholesterol([-5.55 + i * 1.25, -0.28, 0], 0.20) for i in range(4)])
        for i, d in enumerate(flow):
            d.u = i / len(flow)

            def synth_flow(m, dt):
                m.u = (m.u + flow_speed.get_value() * dt) % 1
                # Upstream motion stops short of the labelled valve.
                m.move_to([-5.6 + 4.05 * m.u, -0.28 + 0.12 * np.sin(TAU * m.u), 0])
            d.add_updater(synth_flow)
        self.add(flow)
        self.at("long road")
        self.play(ReplacementTransform(acetyl, hmg), run_time=1.1)
        self.at("main throttle")
        self.play(FadeIn(valve, scale=0.9), run_time=0.7)
        self.at("HMG coenzyme reductase")
        self.play(Indicate(valve, color=TEAL, scale_factor=1.05), run_time=0.8)
        self.at("makes mevalonate")
        self.play(hmg.animate.move_to([0, 0, 0]), run_time=0.8)
        meval.move_to([2.55, 0, 0])
        self.play(Transform(hmg, meval), run_time=0.7)
        self.play(FadeOut(hmg), run_time=0.35)
        tokens = VGroup(*[cholesterol([3.2 + i * 0.55, -0.18, 0], 0.14) for i in range(5)])
        self.play(LaggedStartMap(FadeIn, tokens, lag_ratio=0.12), run_time=0.8)
        self.at("rate limiting")
        self.play(valve.animate.scale(1.06), run_time=0.5)
        self.at("statins inhibit")
        stop_ring = Circle(0.72, color=RED, stroke_width=10)
        stop = VGroup(stop_ring,
                      Line(UL * 0.5, DR * 0.5, color=RED, stroke_width=10),
                      T("statin", 28, RED, weight=BOLD).next_to(stop_ring, DOWN, 0.28)).move_to(valve_body)
        queue_blocks = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.52, height=0.42,
                                                  color=GOLD, stroke_width=3,
                                                  fill_color=GOLD, fill_opacity=0.25).move_to([-2.0 - i * 0.68, -1.75, 0]) for i in range(5)])
        queue_lab = T("HMG-CoA queue", 28, GOLD).next_to(queue_blocks, DOWN, 0.25)
        queue = VGroup(queue_blocks, queue_lab)
        self.play(FadeIn(stop), tokens.animate.set_opacity(0.25), flow_speed.animate.set_value(0.018), run_time=0.7)
        self.play(LaggedStartMap(FadeIn, queue, lag_ratio=0.15), run_time=1.0)
        self.finish()


class S05GaugeHigh(SpokenScene):
    def construct(self):
        er_field = RoundedRectangle(corner_radius=0.5, width=9.4, height=2.2,
                                    stroke_width=0, fill_color=BLUE,
                                    fill_opacity=0.18).move_to([0, -0.35, 0])
        ribbon = er_ribbon().scale(1.22).move_to([0, -0.4, 0])
        g = gauge(0.78, (0, 2.15, 0), 0.9)
        routes = VGroup(arrow([-5.6, -2.7, 0], [-2.3, -0.55, 0], GREEN, 7),
                        arrow([5.6, -2.7, 0], [2.3, -0.55, 0], GREEN, 7))
        labs = VGroup(T("import", 28, GREEN).move_to([-4.5, -2.8, 0]),
                      T("synthesis", 28, GREEN).move_to([4.45, -2.8, 0]))
        lipids = VGroup(*[Dot([x, -0.35 + 0.18 * np.sin(x), 0], radius=0.055, color=BLUE)
                          for x in np.linspace(-4.2, 4.2, 18)])
        for i, d in enumerate(lipids):
            d.u = i / len(lipids)

            def drift_lipid(m, dt):
                m.u = (m.u + 0.045 * dt) % 1
                x = -4.2 + 8.4 * m.u
                m.move_to([x, -0.35 + 0.18 * np.sin(1.5 * x), 0])
            d.add_updater(drift_lipid)
        self.play(FadeIn(er_field), Create(ribbon), FadeIn(g), GrowArrow(routes[0]), GrowArrow(routes[1]), FadeIn(labs, lipids), run_time=1.2)
        self.at("sets both synthesis")
        self.play(Indicate(routes, color=GREEN, scale_factor=1.03), run_time=0.8)
        cart = VGroup(RoundedRectangle(corner_radius=0.15, width=2.0, height=0.82,
                                       color=TEAL, stroke_width=4, fill_color=DARK, fill_opacity=1),
                      T("SCAP", 30, TEAL, weight=BOLD)).move_to([-1.2, -0.2, 0])
        passenger = chip("SREBP-2", TEAL, 28, fill_opacity=1).move_to([-1.2, 0.82, 0])
        passenger[0].set_fill(DARK, opacity=1)
        self.at("SCAP is the sensor")
        self.play(FadeIn(cart, shift=UP * 0.15), run_time=0.6)
        self.at("SREBP2 is the passenger")
        self.play(FadeIn(passenger, shift=DOWN * 0.15), run_time=0.6)
        # Use the otherwise silent lead-in to the next clause for a visible
        # sensor-cart drift; the small membrane motes alone do not register
        # as meaningful motion in the freeze detector.
        bind_target = self.t_of("cholesterol binds SCAP") - 0.2
        bind_run = max(0.1, bind_target - self.elapsed())
        self.play(VGroup(cart, passenger).animate.shift(RIGHT * 0.45),
                  run_time=bind_run, rate_func=linear)
        self.at("cholesterol binds SCAP")
        token = cholesterol([-4.8, 1.2, 0], 0.2)
        self.add(token)
        self.play(token.animate.move_to(cart.get_center() + LEFT * 0.82),
                  Transform(g, gauge(0.68, (0, 2.15, 0), 0.9)), run_time=1.0)
        self.at("Insig grips")
        clasp_arc = Arc(0.7, PI / 2, PI, color=RED, stroke_width=10).move_to([0.05, -0.2, 0])
        clasp_lab = T("Insig", 28, RED, weight=BOLD).move_to([0.35, -1.35, 0])
        clasp = VGroup(clasp_arc, clasp_lab)
        self.play(FadeIn(clasp, shift=LEFT * 0.25),
                  Transform(g, gauge(0.82, (0, 2.15, 0), 0.9)), run_time=0.9)
        golgi = VGroup(*[Arc(radius=0.42 + i * 0.18, start_angle=-PI / 3, angle=2 * PI / 3,
                             color=GREY, stroke_width=5) for i in range(3)]).move_to([4.6, 0.0, 0])
        golgi_lab = T("Golgi", 28, GREY).next_to(golgi, DOWN, 0.30)
        self.at("complex stays")
        held = VGroup(cart, passenger, clasp, token)
        self.play(FadeIn(golgi, golgi_lab), held.animate.shift(RIGHT * 0.55), run_time=1.2)
        self.play(held.animate.shift(LEFT * 0.55),
                  Transform(g, gauge(0.74, (0, 2.15, 0), 0.9)), run_time=1.2)
        self.play(held.animate.shift(RIGHT * 0.35), run_time=1.0)
        self.finish()


class S06GaugeLow(SpokenScene):
    def construct(self):
        er_field = RoundedRectangle(corner_radius=0.5, width=6.0, height=2.0,
                                    stroke_width=0, fill_color=BLUE,
                                    fill_opacity=0.18).move_to([-2.0, -1.35, 0])
        ribbon = er_ribbon().scale(1.08).move_to([-2.0, -1.5, 0])
        g = gauge(0.72, (-2.0, 1.7, 0), 0.82)
        cart = chip("SCAP", TEAL, 28, fill_opacity=1).move_to([-2.55, -0.95, 0])
        passenger = chip("SREBP-2", TEAL, 28, fill_opacity=1).move_to([-2.55, 0.05, 0])
        clasp = chip("Insig", RED, 28, fill_opacity=1).move_to([-0.65, -0.95, 0])
        for c in (cart, passenger, clasp):
            c[0].set_fill(DARK, opacity=1)
        golgi = VGroup(*[Arc(0.42 + i * 0.18, -PI / 3, 2 * PI / 3, color=BLUE, stroke_width=5) for i in range(3)]).move_to([1.5, -0.75, 0])
        golgi_lab = T("Golgi", 28, BLUE).next_to(golgi, DOWN, 0.30)
        nucleus = Circle(1.48, color=BLUE, stroke_width=5, fill_color=DARK, fill_opacity=1).move_to([4.65, 0.3, 0])
        nuc_lab = T("nucleus", 28, BLUE).next_to(nucleus, DOWN, buff=0.30)
        draining = VGroup(*[cholesterol([-4.2 + i * 0.72, -1.25, 0], 0.23) for i in range(6)])
        for i, d in enumerate(draining):
            d.u = i / len(draining)

            def drain(m, dt):
                m.u = (m.u + 0.28 * dt) % 1
                m.move_to([-4.4 + 4.8 * m.u, -1.65 - 0.35 * m.u, 0])
                m.set_opacity(1.0 - 0.65 * m.u)
            d.add_updater(drain)
        self.add(er_field, ribbon, g, cart, passenger, clasp, draining)
        self.at("cholesterol falls")
        self.play(Transform(g, gauge(0.14, (-2.0, 1.7, 0), 0.82)), run_time=1.1)
        self.at("SCAP escapes")
        self.play(FadeOut(clasp, shift=RIGHT * 0.4), run_time=0.6)
        self.at("carries SREBP2")
        processing = np.array([0.15, -0.45, 0])
        route = DashedVMobject(ArcBetweenPoints(cart.get_center(), processing, angle=-0.35), num_dashes=14).set_color(TEAL)
        self.play(FadeIn(golgi, golgi_lab), Create(route), run_time=0.8)
        self.play(VGroup(cart, passenger).animate.move_to(processing), run_time=1.0)
        self.at("enzymes release")
        active = chip("active SREBP-2", TEAL, 28, fill_opacity=1).move_to([2.45, 1.65, 0])
        active[0].set_fill(DARK, opacity=1)
        self.play(TransformFromCopy(passenger, active), passenger.animate.set_opacity(0.25), run_time=0.7)
        self.at("enters the nucleus")
        self.play(FadeIn(nucleus, nuc_lab), active.animate.move_to(nucleus), run_time=1.0)
        self.at("raises both")
        out1 = arrow([4.05, -0.25, 0], [2.0, -2.20, 0], GREEN, 6)
        out2 = arrow([5.25, -0.75, 0], [5.55, -2.30, 0], GREEN, 6)
        reductases = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.65, height=0.5,
                                                color=GREEN, stroke_width=3,
                                                fill_color=GREEN, fill_opacity=0.22).move_to([1.75 + i * 0.8, -2.45, 0]) for i in range(3)])
        reductases.add(T("reductase ×3", 28, GREEN).next_to(reductases, DOWN, 0.25))
        receptors = VGroup(*[receptor(-2.1 - i * 0.42).scale(0.55).shift(RIGHT * 10.1) for i in range(3)])
        self.play(GrowArrow(out1), GrowArrow(out2), run_time=0.6)
        self.at("HMG coenzyme irreductase")
        self.play(LaggedStartMap(FadeIn, reductases, lag_ratio=0.15), run_time=0.8)
        self.at("LDL receptor")
        self.play(LaggedStartMap(FadeIn, receptors, lag_ratio=0.15), run_time=0.8)
        self.finish()


def prediction_world(scene, pulse=False):
    world = full_world("liver cell", level=0.30, blocked=True)
    scene.add(world)
    ldls = drifting_ldl(scene, speed=0.28)
    q = T("?", 82, GOLD, weight=BOLD).move_to([-3.2, 1.7, 0])
    choices = VGroup(*[chip(x, GREY, 28) for x in ("fewer", "more", "unchanged")]).arrange(RIGHT, buff=0.35).move_to([0.75, 2.65, 0])
    scene.add(q, choices)
    return world, ldls, q, choices


class S07Predict(SpokenScene):
    def construct(self):
        world = full_world("liver cell", level=0.65, blocked=True)
        self.play(FadeIn(world), run_time=0.8)
        drifting_ldl(self, speed=0.28)
        self.at("Predict the statin's")
        self.play(Indicate(world[8], color=RED), run_time=0.6)
        self.at("synthesis falls")
        self.play(Transform(world[7], gauge(0.28)), run_time=1.1)
        self.at("what happens")
        q = T("?", 82, GOLD, weight=BOLD).move_to([-3.2, 1.7, 0])
        self.play(FadeIn(q, scale=0.7), run_time=0.5)
        self.at("Fewer")
        choices = VGroup(*[chip(x, GREY, 28) for x in ("fewer", "more", "unchanged")]).arrange(RIGHT, buff=0.35).move_to([0.75, 2.65, 0])
        self.play(LaggedStartMap(FadeIn, choices, lag_ratio=0.18), run_time=0.9)
        self.finish()


class S08PredictHold(Scene):
    def construct(self):
        world, ldls, q, choices = prediction_world(self)
        # Deliberate thinking pause: same frame, with only slow meaningful motion.
        self.play(Transform(world[7], gauge(0.22)), run_time=2.0, rate_func=linear)
        self.play(Indicate(q, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.play(Transform(world[7], gauge(0.17)), run_time=1.7, rate_func=linear)


class S09StatinAnswer(SpokenScene):
    def construct(self):
        world = full_world("liver cell", level=0.18, blocked=True, receptor_count=1)
        self.add(world)
        ldls = drifting_ldl(self, speed=0.30)
        choices = VGroup(*[chip(x, GREY, 28) for x in ("fewer", "more", "unchanged")]).arrange(RIGHT, 0.35).move_to([0.75, 2.65, 0])
        self.add(choices)
        self.at("statin lowers")
        self.play(Indicate(world[8], color=RED), run_time=0.7)
        self.at("gauge reads low")
        self.play(Indicate(world[7], color=BLUE), run_time=0.7)
        self.play(choices[1].animate.set_color(GREEN).scale(1.12), choices[0].animate.set_opacity(0.25), choices[2].animate.set_opacity(0.25), run_time=0.6)
        self.at("SREBP2 then")
        active = chip("active SREBP-2", TEAL, 28, fill_opacity=1).move_to([-0.3, -0.25, 0])
        active[0].set_fill(DARK, opacity=1)
        nucleus = Circle(1.28, color=BLUE, stroke_width=4, fill_color=DARK, fill_opacity=1).move_to([-2.55, -0.25, 0])
        self.play(FadeOut(choices), FadeIn(active, nucleus), active.animate.move_to(nucleus), run_time=1.0)
        self.at("turns up the LDL")
        new_recs = VGroup(receptor(1.05), receptor(0.35), receptor(-0.35))
        self.play(FadeOut(active, nucleus), LaggedStartMap(FadeIn, new_recs, lag_ratio=0.18), run_time=0.9)
        self.at("More receptors")
        count = M("receptors  1 → 4", 28, GREEN).move_to([-2.55, -2.95, 0])
        self.play(FadeIn(count), run_time=0.5)
        self.at("pull more LDL")
        paths = [Line([-5.55, y, 0], [MEM_X + 0.5, y, 0]) for y in (1.75, 1.05, 0.35, -0.35)]
        caps = VGroup(*[ldl([-5.55, y, 0], 0.20) for y in (1.75, 1.05, 0.35, -0.35)])
        self.add(caps)
        self.play(*[MoveAlongPath(d, p) for d, p in zip(caps, paths)], run_time=1.0, rate_func=linear)
        meter_box = RoundedRectangle(corner_radius=0.12, width=1.0, height=2.0,
                                     color=GOLD, stroke_width=3, fill_color=DARK, fill_opacity=1)
        meter_fill = Rectangle(width=0.70, height=1.25, fill_color=GOLD,
                               fill_opacity=0.7, stroke_width=0).align_to(meter_box, DOWN).shift(UP * 0.12)
        meter_lab = T("blood LDL", 28, GOLD).next_to(meter_box, UP, buff=0.25)
        meter = VGroup(meter_box, meter_fill, meter_lab).move_to([-3.25, -1.35, 0])
        self.at("from blood")
        self.play(FadeIn(meter), meter_fill.animate.stretch(0.45, 1).align_to(meter_box, DOWN).shift(UP * 0.12), run_time=0.9)
        self.at("drug closes")
        self.play(Indicate(world[8], color=RED), run_time=0.6)
        self.at("gauge opens the import")
        self.play(world[9].animate.set_stroke(width=14), Indicate(new_recs, color=GREEN), run_time=0.9)
        self.finish()


class S10Fh(SpokenScene):
    def construct(self):
        world = full_world("liver cell", level=0.18, receptor_count=1, fh=True)
        self.play(FadeIn(world), run_time=0.8)
        ldls = drifting_ldl(self, ys=(-2.65, -2.0, -1.35, -0.7, 0, 0.7, 1.4, 2.1, 2.65), speed=0.22)
        self.at("opposite direction")
        self.play(world[9].animate.set_stroke(opacity=0.18), run_time=0.7)
        self.at("too few working receptors")
        self.play(Indicate(world[5], color=RED, scale_factor=1.1), run_time=0.8)
        self.at("little LDL cholesterol")
        miss = ldl([-5.55, 1.75, 0])
        self.add(miss)
        self.play(miss.animate.shift(DOWN * 1.0), run_time=0.8)
        self.at("In the dish")
        skin = T("skin cell", 28, TEXT, weight=BOLD).move_to(world[4])
        self.play(Transform(world[4], skin), run_time=0.6)
        self.at("gauge stayed low")
        self.play(Indicate(world[7], color=BLUE), run_time=0.7)
        self.at("synthesis kept running")
        belt = belt_tokens(self, speed=0.33)
        self.play(FadeIn(belt), world[10].animate.set_stroke(width=11), run_time=0.8)
        self.at("In the body")
        liver = T("liver cell", 28, TEXT, weight=BOLD).move_to(world[4])
        self.play(Transform(world[4], liver), run_time=0.6)
        meter_box = RoundedRectangle(corner_radius=0.12, width=0.9, height=3.0,
                                     color=GOLD, stroke_width=3, fill_color=DARK,
                                     fill_opacity=1).move_to([-5.55, -1.05, 0])
        fill = Rectangle(width=0.62, height=0.45, fill_color=GOLD, fill_opacity=0.7,
                         stroke_width=0).align_to(meter_box, DOWN).shift(UP * 0.15)
        meter_lab = T("LDL", 28, GOLD).move_to([-5.55, 0.12, 0])
        meter_box.set_z_index(5)
        fill.set_z_index(6)
        meter_lab.set_z_index(7)
        self.play(FadeIn(meter_box, fill, meter_lab), run_time=0.5)
        self.at("blood LDL rises")
        self.play(fill.animate.stretch(3.4, 1).align_to(meter_box, DOWN).shift(UP * 0.15), run_time=1.2)
        self.at("clearance is slow")
        self.play(LaggedStart(*[Indicate(d, color=GOLD, scale_factor=1.15) for d in ldls], lag_ratio=0.06), run_time=1.1)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        world = full_world("liver cell", level=0.25, receptor_count=2)
        self.add(world)
        drifting_ldl(self, speed=0.24)
        self.at("Follow cholesterol")
        particle = ldl([-5.55, 1.75, 0], 0.28)
        self.add(particle)
        self.play(particle.animate.move_to([MEM_X - 0.1, 1.75, 0]), run_time=0.7)
        self.play(particle.animate.move_to([-2.0, 1.1, 0]), run_time=0.7)
        token = cholesterol(particle.get_center(), 0.17)
        self.add(token)
        self.play(FadeOut(particle), token.animate.move_to([ER_X, ER_Y + 0.35, 0]), run_time=0.9)
        self.at("puzzle dissolves")
        self.play(Transform(world[7], gauge(0.72)), world[9].animate.set_stroke(width=4, opacity=0.45), world[10].animate.set_stroke(width=4, opacity=0.45), run_time=0.9)
        self.at("cholesterol it can sense")
        self.play(Indicate(world[7], color=BLUE, scale_factor=1.08), run_time=0.8)
        self.at("not cholesterol merely nearby")
        outside = ldl([-5.55, -0.7, 0], 0.34)
        self.play(FadeIn(outside), outside.animate.shift(UP * 0.8), run_time=0.9)
        self.at("Low ER cholesterol")
        self.play(Transform(world[7], gauge(0.14)), run_time=0.8)
        self.at("turns up both")
        self.play(world[9].animate.set_stroke(width=14, opacity=1), world[10].animate.set_stroke(width=14, opacity=1), run_time=0.8)
        self.at("making and importing")
        self.play(Indicate(VGroup(world[9], world[10]), color=GREEN, scale_factor=1.03), run_time=0.8)
        self.finish()


class S12End(EndCard):
    LINE = "Low ER cholesterol turns up both making and importing."

