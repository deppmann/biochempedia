"""A Room With No Way Out — lysosomal storage as a tap-and-drain story.

COLOR MAP (fixed throughout)
  BLUE = every membrane and the lysosome skin
  GOLD = GM2 / gangliosides (small lozenges)
  TEAL = HexA (closing jaws) and clearance
  GREEN = delivery (tap and incoming vesicles)
  PURPLE = small parts and transporter doors
  RED = trouble (storage, broken genes, empty enzyme bars)
  WHITE/TEXT = oxygen; PALE_YELLOW = oily core; PINK = acidic interior

All molecules and proteins are schematic cartoons; no molecular structure is drawn.
"""
import random

from bp_style import *  # noqa: F401,F403


PURPLE = "#B68CFF"
PALE_YELLOW = "#F3DF8B"
PINK = "#E889A8"
WHITE = TEXT
ROOM_C = np.array([-1.0, 0.15, 0.0])


def lozenge(pos=ORIGIN, scale=1.0, color=GOLD):
    return RoundedRectangle(corner_radius=0.15, width=0.52, height=0.26,
                            stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.9).scale(scale).move_to(pos)


def add_bob(mob, amount=0.02, speed=1.5):
    mob._base_height = mob.height
    mob._phase = mob.get_x()

    def bob(m, dt):
        target = 1 + amount * np.sin(m.get_scene().renderer.time * speed + m._phase) if hasattr(m, "get_scene") else 1
        # A tiny vertical breath avoids cumulative scaling and keeps the feet planted visually.
        m.shift(UP * 0.003 * np.sin(m._phase + speed * dt))
    mob.add_updater(bob)
    return mob


def person(x, child=False, color=TEXT, scale=1.0):
    h = 1.82 if child else 2.18
    head = Circle(radius=0.43, color=color, stroke_width=5).move_to([x, 1.08, 0])
    body = RoundedRectangle(corner_radius=0.48, width=1.18, height=h,
                            color=color, stroke_width=5, fill_color=color,
                            fill_opacity=0.04).next_to(head, DOWN, buff=0.08)
    legs = VGroup(Line(body.get_bottom() + LEFT * 0.3, body.get_bottom() + LEFT * 0.3 + DOWN * 0.7,
                       color=color, stroke_width=5),
                  Line(body.get_bottom() + RIGHT * 0.3, body.get_bottom() + RIGHT * 0.3 + DOWN * 0.7,
                       color=color, stroke_width=5))
    return VGroup(head, body, legs).scale(scale)


def bar_gauge(x, height=2.45, fraction=0.5, color=TEAL, label=True):
    frame = RoundedRectangle(corner_radius=0.12, width=0.48, height=height,
                             stroke_color=TEXT, stroke_width=3)
    fill_h = max(0.04, (height - 0.12) * fraction)
    fill = Rectangle(width=0.36, height=fill_h, stroke_width=0,
                     fill_color=color, fill_opacity=1).align_to(frame, DOWN).shift(UP * 0.06)
    g = VGroup(frame, fill).move_to([x, -0.05, 0])
    if label:
        g.add(T("HexA", 30, color=color).next_to(frame, DOWN, buff=0.16))
    return g


def jaw(pos=ORIGIN, scale=1.0, color=TEAL):
    top = Arc(radius=0.28, start_angle=PI, angle=PI, color=color, stroke_width=6)
    bottom = Arc(radius=0.28, start_angle=0, angle=PI, color=color, stroke_width=6)
    return VGroup(top.shift(UP * 0.07), bottom.shift(DOWN * 0.07)).scale(scale).move_to(pos)


def add_chomp(mob, speed=2.0, phase=0.0):
    """Keep a schematic enzyme visibly working without cumulative drift."""
    mob._chomp_t = phase

    def chomp(m, dt):
        m._chomp_t += dt
        top, bottom = m[0], m[1]
        current = top.get_y() - bottom.get_y()
        target = 0.10 + 0.12 * (0.5 + 0.5 * np.sin(speed * m._chomp_t))
        delta = (target - current) / 2
        top.shift(UP * delta)
        bottom.shift(DOWN * delta)
    mob.add_updater(chomp)
    return mob


def add_ring_breathe(mob, amount=0.016, speed=1.5):
    """Make a newly formed compartment visibly settle while narration continues."""
    mob._ring_t = 0.0
    mob._ring_scale = 1.0

    def breathe_ring(m, dt):
        m._ring_t += dt
        target = 1.0 + amount * np.sin(speed * m._ring_t)
        m.scale(target / m._ring_scale)
        m._ring_scale = target
    mob.add_updater(breathe_ring)
    return mob


def falling_drops(center, radius=1.1, n=3, speed=0.28, phase=0.0):
    """Visible tap flow for compact carried-world diagrams."""
    drops = VGroup()
    for i in range(n):
        d = lozenge(center + UP * (radius - 0.25 - i * 0.52), 0.42)
        d._top = center[1] + radius - 0.25
        d._bottom = center[1] - radius + 0.35
        d._speed = speed * (0.9 + 0.08 * i)
        d.shift(DOWN * phase * i)

        def fall(m, dt):
            m.shift(DOWN * m._speed * dt)
            if m.get_y() < m._bottom:
                m.move_to([m.get_x(), m._top, 0])
        d.add_updater(fall)
        drops.add(d)
    return drops


def lysosome(center=ROOM_C, radius=2.55, opacity=0.08):
    # The room is a living compartment: its broad, slow tint pulse keeps long explanations alive.
    # Its outline never opens or breaks.
    base = max(opacity, 0.22)
    wall = Circle(radius=radius, stroke_color=BLUE, stroke_width=7,
                  fill_color=PINK, fill_opacity=base).move_to(center)
    wall._pulse_t = 0.0

    def breathe(m, dt, floor=base):
        m._pulse_t += dt
        m.set_fill(PINK, opacity=floor + 0.055 * (0.5 + 0.5 * np.sin(2.3 * m._pulse_t)))
        m.set_stroke(BLUE, width=7.0 + 0.8 * np.sin(2.3 * m._pulse_t))
    wall.add_updater(breathe)
    return wall


def tap(center=ROOM_C, radius=2.55, label=True):
    p = center + np.array([-1.45, radius + 0.02, 0])
    pipe = VGroup(Line(p + UP * 0.65, p + DOWN * 0.02, color=GREEN, stroke_width=9),
                  Line(p + UP * 0.63, p + RIGHT * 0.75 + UP * 0.63, color=GREEN, stroke_width=9),
                  Line(p + RIGHT * 0.75 + UP * 0.63, p + RIGHT * 0.75 + UP * 0.35,
                       color=GREEN, stroke_width=9))
    if label:
        pipe.add(T("delivery in", 30, color=GREEN).next_to(pipe, LEFT, buff=0.2))
    return pipe


def drain(center=ROOM_C, radius=2.55, width=1.25, label=True):
    y = center[1] - radius
    funnel = Polygon([center[0] - width / 2, y + 0.15, 0], [center[0] + width / 2, y + 0.15, 0],
                     [center[0] + 0.16, y - 0.48, 0], [center[0] - 0.16, y - 0.48, 0],
                     color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.14)
    g = VGroup(funnel)
    if label:
        g.add(T("clearance: HexA", 30, color=TEAL).next_to(funnel, DOWN, buff=0.15))
    return g


def room_gauge(x=5.75, level=0.18, height=4.4, label=True):
    frame = RoundedRectangle(corner_radius=0.12, width=0.62, height=height,
                             stroke_color=GOLD, stroke_width=3)
    fill = Rectangle(width=0.46, height=max(0.08, (height - 0.16) * level), stroke_width=0,
                     fill_color=GOLD, fill_opacity=0.9).align_to(frame, DOWN).shift(UP * 0.08)
    g = VGroup(frame, fill).move_to([x, 0.1, 0])
    if label:
        lab = T("GM2 in\nthe room", 30, color=GOLD, line_spacing=0.8).next_to(frame, UP, buff=0.12)
        g.add(lab)
    return g


def drifting_lozenges(center=ROOM_C, radius=2.15, n=8, seed=7, speed=0.28):
    rng = random.Random(seed)
    items = VGroup()
    for i in range(n):
        a = rng.uniform(0, TAU)
        r = radius * np.sqrt(rng.uniform(0.05, 0.82))
        m = lozenge(center + np.array([r * np.cos(a), r * np.sin(a), 0]), 0.82)
        b = rng.uniform(0, TAU)
        m.vel = np.array([np.cos(b), np.sin(b), 0]) * speed * rng.uniform(0.7, 1.25)

        def drift(q, dt, c=center.copy(), rr=radius):
            q.shift(q.vel * dt)
            d = q.get_center() - c
            if np.linalg.norm(d[:2]) > rr:
                nrm = d / max(np.linalg.norm(d), 1e-6)
                q.vel = q.vel - 2 * np.dot(q.vel, nrm) * nrm
                q.move_to(c + nrm * rr)
        m.add_updater(drift)
        items.add(m)
    return items


def schematic_room(center=ROOM_C, radius=2.55, drain_width=1.25, gauge_x=5.75,
                   gauge_level=0.18, jaws=6, labels=True):
    wall = lysosome(center, radius)
    tp = tap(center, radius, labels)
    dr = drain(center, radius, drain_width, labels)
    cargo = drifting_lozenges(center, radius - 0.43, 7, seed=13, speed=0.17)
    js = VGroup(*[jaw(center + np.array([0.85 * np.cos(i * TAU / max(jaws, 1)),
                                         0.72 * np.sin(i * TAU / max(jaws, 1)), 0]), 0.62)
                  for i in range(jaws)]) if jaws else VGroup()
    gauge = room_gauge(gauge_x, gauge_level, height=4.0, label=labels)
    return VGroup(wall, tp, dr, cargo, js, gauge)


def small_room(center, radius=1.25, drain_width=0.62, level=0.18, tap_on=True):
    wall = lysosome(center, radius, opacity=0.06)
    dr = drain(center, radius, drain_width, label=False)
    tp = tap(center, radius, label=False).scale(0.55, about_point=center + UP * radius)
    fill = Rectangle(width=1.4, height=0.18 + 1.2 * level, stroke_width=0,
                     fill_color=GOLD, fill_opacity=0.75).move_to(center + DOWN * (radius - (0.18 + 1.2 * level) / 2 - 0.12))
    fill.set_clip_path(Circle(radius=radius - 0.1).move_to(center))
    return VGroup(wall, tp if tap_on else VGroup(), dr, fill)


def model_values(f, tmax=22.0, dt=0.025):
    """Euler integration of dS/dt = 0.1 - f*S/(1+S), S(0)=0."""
    ts = np.arange(0.0, tmax + dt, dt)
    vals = np.zeros_like(ts)
    for i in range(1, len(ts)):
        s = vals[i - 1]
        vals[i] = max(0.0, s + dt * (0.1 - f * s / (1.0 + s)))
    return ts, vals


def model_axes():
    panel = RoundedRectangle(corner_radius=.18, width=6.35, height=5.05, stroke_width=0,
                             fill_color="#1E3442", fill_opacity=.95).move_to([3.15, .45, 0])
    ax = Axes(x_range=[0, 22, 5], y_range=[0, 2.2, 0.5], x_length=5.6, y_length=4.15,
              axis_config={"color": TEXT, "stroke_width": 2, "include_ticks": False,
                           "include_tip": True}).move_to([3.15, 0.35, 0])
    xl = T("time", 28).next_to(ax.x_axis, DOWN, buff=0.12)
    yl = T("GM2 in room", 28).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.1)
    tag = T("toy model, illustrative", 28, color=GREY).move_to([3.55, 3.12, 0])
    panel.set_z_index(-2)
    return ax, VGroup(panel, xl, yl, tag)


def curve_for(ax, f, color=TEAL, dashed=False):
    ts, ss = model_values(f)
    pts = [ax.c2p(t, min(s, 2.35)) for t, s in zip(ts, ss)]
    path = VMobject(color=color, stroke_width=5).set_points_as_corners(pts)
    return DashedVMobject(path, num_dashes=38, dashed_ratio=0.55) if dashed else path


def question_card():
    lab = T("Half drain—does it fill?", 36, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.2, width=lab.width + 0.7, height=lab.height + 0.48,
                           stroke_color=GOLD, stroke_width=4, fill_color=BG, fill_opacity=0.96)
    # Keep the card clear of the carried room's bottom drain and the right-hand gauge.
    return VGroup(box, lab).move_to([2.65, -2.85, 0])


class S00Hook(SpokenScene):
    def construct(self):
        adults = VGroup(person(-4.2), person(-0.8))
        child = person(3.25, child=True)
        gauges = VGroup(bar_gauge(-2.98, fraction=1.0), bar_gauge(0.42, fraction=1.0),
                        bar_gauge(4.45, height=2.1, fraction=1.0))
        people = VGroup(adults, child, gauges)
        self.add(people)
        for p in [*adults, child]:
            p.add_updater(lambda m, dt: m.shift(UP * 0.004 * np.sin(self.renderer.time * 1.7 + m.get_x())))

        self.at("one missing enzyme")
        empty = bar_gauge(4.45, height=2.1, fraction=0.02, color=RED)
        red_child = person(3.25, child=True, color=RED)
        self.play(ReplacementTransform(gauges[2], empty), Transform(child, red_child), run_time=0.7)

        self.at("her parents")
        halves = VGroup(bar_gauge(-2.98, fraction=0.5), bar_gauge(0.42, fraction=0.5))
        half_chips = VGroup(chip("half", TEAL, 30).move_to([-3.0, 2.6, 0]),
                            chip("half", TEAL, 30).move_to([0.4, 2.6, 0]))
        self.play(Transform(gauges[0], halves[0]), Transform(gauges[1], halves[1]),
                  FadeIn(half_chips, shift=DOWN * 0.2), run_time=0.65)

        self.at("are fine")
        ticks = VGroup(T("✓", 42, color=GREEN).move_to([-4.2, 3.05, 0]),
                       T("✓", 42, color=GREEN).move_to([-0.8, 3.05, 0]))
        self.play(GrowFromCenter(ticks), run_time=0.45)

        self.at("a room with no way out")
        small = VGroup(people, half_chips, ticks).copy().clear_updaters().scale(0.48).move_to([-4.75, -0.25, 0])
        room = lysosome([2.25, 0, 0], 2.55, opacity=0.02)
        cargo = drifting_lozenges(np.array([2.25, 0, 0]), 2.08, 8, seed=4, speed=0.35)
        badge = chip("?", GOLD, 40).move_to([4.75, 2.35, 0])
        self.play(Transform(VGroup(people, half_chips, ticks), small), Create(room),
                  LaggedStart(*[FadeIn(x) for x in cargo], lag_ratio=0.08), run_time=0.85)
        self.play(GrowFromCenter(badge), run_time=0.35)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        room = lysosome([2.25, 0, 0], 2.55, opacity=0.01).set_opacity(0.25)
        cargo = drifting_lozenges(np.array([2.25, 0, 0]), 2.08, 8, seed=4, speed=0.35).set_opacity(0.25)
        brand = T("BIOCHEMISTRYPEDIA", 28, color=TEAL, weight=BOLD)
        title = T("A Room With No Way Out", 54, font=TITLE_FONT)
        rule = Line(LEFT * 1.5, RIGHT * 1.5, color=GOLD, stroke_width=4)
        card = VGroup(brand, title, rule).arrange(DOWN, buff=0.38)
        self.add(room, cargo)
        self.play(FadeIn(card, shift=UP * 0.15), run_time=0.45)
        self.wait(1.05)
        band = RoundedRectangle(corner_radius=0.08, width=12.0, height=1.6,
                                stroke_color=BLUE, stroke_width=6).set_fill(BLUE, 0.03)
        self.play(FadeOut(card), Transform(room, band), FadeOut(cargo), run_time=0.5)


class S02Wall(SpokenScene):
    def construct(self):
        xs = np.linspace(-5.8, 5.8, 20)
        core = Rectangle(width=12.0, height=0.76, stroke_width=0, fill_color=PALE_YELLOW,
                         fill_opacity=0.28)
        top = VGroup(*[Dot([x, 0.62, 0], radius=0.16, color=BLUE) for x in xs])
        bot = VGroup(*[Dot([x, -0.62, 0], radius=0.16, color=BLUE) for x in xs])
        wall = VGroup(core, top, bot)
        sides = VGroup(T("outside", 30).move_to([-5.25, 2.9, 0]),
                       T("inside", 30).move_to([-5.25, -2.9, 0]))
        self.play(Create(Line(LEFT * 6, RIGHT * 6, color=BLUE, stroke_width=10)), run_time=0.75)
        self.at("A cell membrane")
        self.play(FadeIn(top, shift=DOWN * 0.2), FadeIn(bot, shift=UP * 0.2), FadeIn(sides), run_time=0.7)
        self.at("double layer")
        self.play(Indicate(top, color=BLUE), Indicate(bot, color=BLUE), run_time=0.7)
        self.at("oily core")
        oily = T("oily core", 30, color=PALE_YELLOW).move_to([4.65, 1.35, 0])
        self.play(FadeIn(core), FadeIn(oily), run_time=0.6)

        self.at("like oxygen")
        oxygen = VGroup(*[Dot([x, 2.25 + 0.25 * (i % 2), 0], radius=0.13, color=WHITE)
                          for i, x in enumerate((-2.2, -0.7, 0.8, 2.3))])
        o_lab = chip("oxygen", WHITE, 30).move_to([4.25, 2.35, 0])
        self.play(FadeOut(oily), FadeIn(oxygen), FadeIn(o_lab), run_time=0.45)
        self.play(oxygen.animate.shift(DOWN * 4.7), run_time=1.15, rate_func=linear)
        for i, d in enumerate(oxygen):
            d.add_updater(lambda m, dt, k=i: m.shift(UP * dt * (0.26 + 0.03 * k)) if m.get_y() < 2.8 else m.shift(DOWN * 5.6))

        self.at("Glucose and ions")
        blocked = VGroup(chip("glucose", GOLD, 30).move_to([-2.0, 2.2, 0]),
                         chip("K+", GOLD, 30).move_to([0.1, 2.2, 0]),
                         chip("K+", GOLD, 30).move_to([1.45, 2.2, 0]))
        self.play(FadeOut(o_lab), FadeIn(blocked), run_time=0.4)
        self.play(blocked.animate(rate_func=there_and_back).shift(DOWN * 1.18), run_time=0.85)

        self.at("doors the cell builds")
        doors = VGroup(RoundedRectangle(corner_radius=0.12, width=1.0, height=1.85,
                                        stroke_color=PURPLE, stroke_width=5).move_to([-1.25, 0, 0]),
                       RoundedRectangle(corner_radius=0.28, width=1.35, height=1.85,
                                        stroke_color=PURPLE, stroke_width=5).move_to([1.15, 0, 0]))
        lab = T("doors", 30, color=PURPLE).move_to([4.35, 1.45, 0])
        self.play(FadeIn(doors), FadeIn(lab), run_time=0.45)
        self.play(blocked.animate.move_to([0, -2.25, 0]), run_time=0.75)
        self.finish()


class S03Room(SpokenScene):
    def construct(self):
        band = RoundedRectangle(corner_radius=0.08, width=12.0, height=1.6,
                                stroke_color=BLUE, stroke_width=6).set_fill(BLUE, 0.03)
        self.add(band)
        self.at("into a bag")
        room = lysosome(ROOM_C, 2.55, opacity=0.02)
        self.play(ReplacementTransform(band, room), run_time=1.0)
        add_ring_breathe(room)
        lys_lab = T("lysosome", 34, color=BLUE).next_to(room, UP, buff=0.16)
        self.at("recycling room")
        self.play(FadeIn(lys_lab), room.animate.set_fill(PINK, 0.08), run_time=0.6)

        self.at("digestive enzymes")
        jaws = VGroup(*[jaw(ROOM_C + np.array([1.25 * np.cos(i * TAU / 6),
                                               1.15 * np.sin(i * TAU / 6), 0]), 0.8)
                        for i in range(6)])
        for i, j in enumerate(jaws):
            add_chomp(j, speed=1.8, phase=i * 0.55)
        self.play(LaggedStart(*[GrowFromCenter(j) for j in jaws], lag_ratio=0.12), run_time=0.8)
        self.at("in acid")
        self.play(FadeOut(lys_lab), run_time=0.2)
        acid = chip("acidic", PINK, 30).move_to([-1.0, 2.05, 0])
        self.play(FadeIn(acid), room.animate.set_fill(PINK, 0.15), run_time=0.55)

        self.at("delivered in")
        cargo = T("old\nmembrane", 28, line_spacing=.75)
        ves = VGroup(Circle(radius=1.0, color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.06),
                     cargo).move_to([-5.1, 1.75, 0])
        delivery = T("delivery in", 30, color=GREEN).move_to([-4.6, 3.05, 0])
        self.play(FadeOut(acid), FadeIn(ves), FadeIn(delivery), run_time=0.45)
        self.play(ves.animate.move_to(ROOM_C + LEFT * 1.05 + UP * 0.35).scale(0.75), run_time=0.8)

        self.at("small parts")
        parts = VGroup(*[Dot(ROOM_C + np.array([-.55 + .22 * (i % 5), -.3 + .22 * (i // 5), 0]),
                                  radius=0.09, color=PURPLE) for i in range(15)])
        self.play(FadeOut(ves), FadeIn(parts),
                  LaggedStart(*[Indicate(j, color=TEAL, scale_factor=1.15) for j in jaws], lag_ratio=0.08),
                  run_time=0.8)

        self.at("leave through transporters")
        door = RoundedRectangle(corner_radius=0.12, width=0.58, height=1.05,
                                stroke_color=PURPLE, stroke_width=5).rotate(-0.55).move_to(ROOM_C + RIGHT * 2.25 + DOWN * 0.9)
        tr_lab = T("transporter", 30, color=PURPLE).move_to([4.35, -2.0, 0])
        self.play(FadeOut(delivery), FadeIn(door), FadeIn(tr_lab), run_time=0.45)
        self.play(parts.animate.move_to([4.6, -2.65, 0]).set_opacity(0), run_time=1.0)
        self.finish()


class S04Gm2(SpokenScene):
    def construct(self):
        room = lysosome(ROOM_C, 2.55, opacity=0.1)
        add_ring_breathe(room)
        jaws = VGroup(*[jaw(ROOM_C + np.array([1.15 * np.cos(i * TAU / 6),
                                               1.05 * np.sin(i * TAU / 6), 0]), 0.72)
                        for i in range(6)])
        for i, j in enumerate(jaws):
            add_chomp(j, speed=1.9, phase=i * 0.48)
        door = RoundedRectangle(corner_radius=0.12, width=0.58, height=1.05,
                                stroke_color=PURPLE, stroke_width=5).rotate(-0.55).move_to(ROOM_C + RIGHT * 2.25 + DOWN * 0.9)
        self.add(room, jaws, door)
        self.at("follow one lipid")
        strip = Line([-4.8, 1.65, 0], [-2.0, 1.65, 0], color=BLUE, stroke_width=8)
        heads = VGroup(*[lozenge([-4.5 + 0.72 * i, 1.98, 0], 0.92) for i in range(4)])
        gm2 = T("GM2", 32, color=GOLD).next_to(heads, UP, buff=0.16)
        self.play(Create(strip), LaggedStart(*[FadeIn(h, shift=DOWN * 0.25) for h in heads], lag_ratio=0.15),
                  FadeIn(gm2), run_time=0.85)

        self.at("One enzyme")
        for j in jaws[1:]:
            j.set_opacity(0.35)
        hexa = T("HexA", 32, color=TEAL).move_to([0.35, 1.55, 0])
        self.play(jaws[0].animate.scale(1.25), FadeIn(hexa), run_time=0.55)
        self.at("snips one sugar")
        target = heads[2]
        tip = Dot(target.get_top() + UP * 0.13, radius=0.11, color=PURPLE)
        next_jaw = jaw([-0.35, -1.05, 0], 0.8, color=TEXT)
        next_lab = T("next enzymes", 28).next_to(next_jaw, DOWN, buff=0.12)
        self.play(jaws[0].animate.move_to(target.get_center() + DOWN * 0.1), run_time=0.42)
        self.play(FadeIn(tip, scale=0.2), target.animate.scale(0.78), run_time=0.4)
        self.play(target.animate.move_to(next_jaw), FadeIn(next_jaw), FadeIn(next_lab), run_time=0.55)
        dots = VGroup(*[Dot([1.0 + .2 * i, -1.1, 0], radius=.09, color=PURPLE) for i in range(3)])
        self.play(FadeOut(target), FadeIn(dots), dots.animate.move_to([4.2, -2.1, 0]).set_opacity(0), run_time=0.75)

        self.at("cannot cross")
        stuck = heads[0].copy().move_to(ROOM_C + LEFT * 0.35)
        self.play(FadeOut(VGroup(next_jaw, next_lab, hexa, strip, heads, tip, gm2)), FadeIn(stuck), run_time=0.35)
        self.play(stuck.animate(rate_func=there_and_back).shift(RIGHT * 2.25),
                  room.animate(rate_func=there_and_back).stretch(1.03, 0), run_time=0.8)

        self.at("no transporter carries")
        self.play(stuck.animate(rate_func=there_and_back).move_to(door.get_center() + LEFT * 0.25),
                  Indicate(door, color=RED, scale_factor=1.08), run_time=0.9)
        self.finish()


class S05Balance(SpokenScene):
    def construct(self):
        room = lysosome(ROOM_C, 2.55, opacity=0.1)
        gold = lozenge(ROOM_C + UP * 0.2)
        ambient = drifting_lozenges(ROOM_C, 1.72, 3, seed=31, speed=.62)
        hexa = jaw(ROOM_C + RIGHT * 0.65, 1.0)
        others = VGroup(*[jaw(ROOM_C + np.array([-1.1 + .55 * i, -0.85, 0]), .65) for i in range(5)]).set_opacity(.4)
        self.add(room, ambient, gold, hexa, others)
        self.at("Nothing else")
        self.play(LaggedStart(*[j.animate(rate_func=there_and_back).shift(UP * .4) for j in others], lag_ratio=.16),
                  gold.animate.shift(RIGHT * .25), run_time=1.0)
        self.at("job well enough")
        self.play(hexa.animate(rate_func=there_and_back).move_to(gold), Flash(gold, color=PURPLE), run_time=.7)

        self.at("tap and a drain")
        scheme = schematic_room(ROOM_C, 2.55, 1.25, 5.75, .18, jaws=6, labels=True)
        self.play(FadeOut(VGroup(ambient, gold, hexa, others)), Transform(room, scheme[0]),
                  FadeIn(VGroup(*scheme[1:])), run_time=1.0)

        self.at("delivery in")
        self.play(Indicate(scheme[1], color=GREEN, scale_factor=1.04), run_time=.55)
        self.at("clearance out")
        self.play(Indicate(scheme[2], color=TEAL, scale_factor=1.06),
                  scheme[5][1].animate(rate_func=there_and_back).stretch(1.18, 1, about_edge=DOWN), run_time=.65)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        scheme = schematic_room(ROOM_C, 2.55, 1.25, 5.75, .18, jaws=6, labels=False)
        self.add(scheme)
        self.at("one working copy")
        adult = person(-5.35, child=False, scale=.48)
        genes = VGroup(chip("HEXA", TEAL, 30), chip("HEXA ×", RED, 30)).arrange(DOWN, buff=.15).move_to([-4.2, 2.25, 0])
        self.play(FadeIn(adult), FadeIn(genes, shift=RIGHT * .25), run_time=.7)

        self.at("half the normal amount")
        half_jaws = VGroup(*[scheme[4][i] for i in range(3)])
        new_drain = drain(ROOM_C, 2.55, .625, label=False)
        self.play(FadeOut(VGroup(*[scheme[4][i] for i in range(3, 6)])),
                  Transform(scheme[2], new_drain), run_time=.75)

        self.at("So have the drain")
        self.play(Indicate(scheme[2], color=TEAL, scale_factor=1.08), run_time=.55)
        self.at("Does their lysosome fill up")
        q = question_card()
        self.play(FadeOut(VGroup(adult, genes)), FadeIn(q, shift=UP * .45), run_time=.65)
        self.finish()


class S07Think(Scene):
    def construct(self):
        scheme = schematic_room(ROOM_C, 2.55, .625, 5.75, .18, jaws=3, labels=False)
        q = question_card()
        self.add(scheme, q)
        self.wait(4.5)


class S08Carrier(SpokenScene):
    def construct(self):
        # Rebuild the carried room first, then make space for the computed plot.
        scheme = schematic_room(ROOM_C, 2.55, .625, 5.75, .18, jaws=3, labels=False)
        q = question_card()
        self.add(scheme, q)
        self.at("Now")
        left_scheme = schematic_room(np.array([-4.5, .25, 0]), 1.55, .38, -2.55, .18, jaws=3, labels=False)
        self.play(FadeOut(q, shift=DOWN * .35), ReplacementTransform(scheme, left_scheme), run_time=.75)
        scheme = left_scheme
        ax, labs = model_axes()
        self.play(Create(ax), FadeIn(labs), run_time=.65)

        self.at("far more")
        normal = curve_for(ax, 1.0, TEAL)
        nlab = T("normal", 28, color=TEAL).move_to(ax.c2p(17.8, .43))
        self.play(Create(normal), FadeIn(nlab), run_time=1.0)

        self.at("many times faster")
        arr_in = Arrow([-5.5, -2.85, 0], [-4.95, -2.85, 0], color=GREEN, buff=0, stroke_width=5)
        arr_out = Arrow([-4.7, -2.85, 0], [-2.3, -2.85, 0], color=TEAL, buff=0, stroke_width=5)
        self.play(GrowArrow(arr_in), GrowArrow(arr_out), run_time=.6)
        self.play(FadeOut(VGroup(arr_in, arr_out)), run_time=.25)

        self.at("Half the drain")
        carrier = curve_for(ax, .5, TEAL, dashed=True)
        clab = T("half: carrier", 28, color=TEAL).move_to(ax.c2p(17.0, .68))
        self.play(Create(carrier), FadeIn(clab),
                  scheme[5][1].animate.stretch(1.35, 1, about_edge=DOWN), run_time=1.0)
        self.at("stays low")
        high = DashedLine(ax.c2p(0, 1.5), ax.c2p(22, 1.5), color=RED, stroke_width=3)
        highlab = T("high storage, schematic", 28, color=RED).move_to(ax.c2p(14.5, 1.88))
        tick = T("✓", 40, color=GREEN).next_to(clab, RIGHT, buff=.12)
        self.play(Create(high), FadeIn(highlab), GrowFromCenter(tick), run_time=.65)
        self.finish()


class S09Infant(SpokenScene):
    def construct(self):
        scheme = schematic_room(np.array([-4.5, .25, 0]), 1.55, .38, -2.55, .25, jaws=3, labels=False)
        ax, labs = model_axes()
        normal = curve_for(ax, 1.0, TEAL)
        carrier = curve_for(ax, .5, TEAL, dashed=True)
        high = DashedLine(ax.c2p(0, 1.5), ax.c2p(22, 1.5), color=RED, stroke_width=3)
        self.add(scheme, ax, labs, normal, carrier, high)
        self.at("almost no working enzyme")
        child = person(5.25, child=True, color=RED, scale=.36).move_to([5.25, 2.35, 0])
        genes = VGroup(chip("HEXA ×", RED, 28), chip("HEXA ×", RED, 28)).arrange(RIGHT, buff=.16).move_to([2.65, 2.38, 0])
        shut = drain(np.array([-4.5, .25, 0]), 1.55, .10, label=False)
        self.play(FadeIn(child), FadeIn(genes), FadeOut(scheme[4]), Transform(scheme[2], shut), run_time=.8)

        self.at("delivery goes on")
        self.play(FadeOut(child), FadeOut(genes), Indicate(scheme[1], color=GREEN, scale_factor=1.08), run_time=.55)
        zero = curve_for(ax, 0.0, RED)
        zlab = T("zero: toy model", 28, color=RED).move_to(ax.c2p(13.8, .70))
        self.play(Create(zero), FadeIn(zlab), run_time=1.0)

        self.at("GM2 piles up")
        pile = VGroup(*[lozenge([-5.25 + .38 * (i % 4), -.55 + .3 * (i // 4), 0], .55)
                        for i in range(16)])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * .25) for x in pile], lag_ratio=.06),
                  scheme[5][1].animate.stretch(3.0, 1, about_edge=DOWN), run_time=1.0)

        self.at("lysosomes swell")
        self.play(scheme[0].animate.scale(1.28), pile.animate.scale(1.15),
                  scheme[5].animate.shift(RIGHT * .75), run_time=.8)
        self.at("room stays intact")
        self.play(Flash(scheme[0], color=BLUE, flash_radius=2.05, line_length=.28),
                  scheme[0].animate.set_stroke(width=9), run_time=.65)
        self.at("cannot empty")
        self.play(LaggedStart(*[x.animate.shift(UP * .08) for x in pile], lag_ratio=.05), run_time=.55)
        self.finish()


class S10Threshold(SpokenScene):
    def construct(self):
        room = schematic_room(np.array([-4.5, .75, 0]), 1.45, .38, -2.55, .22, jaws=3, labels=False)
        ax, labs = model_axes()
        zero = curve_for(ax, 0.0, RED)
        self.add(room, ax, labs, zero)

        self.at("drain falls below the tap")
        dial = NumberLine(x_range=[0, 1, .25], length=5.2, color=TEAL,
                          include_numbers=False).move_to([2.9, -3.02, 0])
        dial_nums = VGroup(*[M(str(v), 28, color=TEXT).next_to(dial.n2p(v), DOWN, buff=.12)
                             for v in (0, .25, .5, .75, 1)])
        dlab = T("HexA left", 30, color=TEAL).move_to([-1.0, -3.02, 0])
        knob = Dot(dial.n2p(.5), radius=.16, color=TEAL)
        self.play(Create(dial), FadeIn(dial_nums), FadeIn(dlab), FadeIn(knob), run_time=.65)
        self.play(knob.animate.move_to(dial.n2p(.2)), Transform(room[2], drain(np.array([-4.5, .75, 0]), 1.45, .16, False)), run_time=.65)
        c20 = curve_for(ax, .2, TEAL, dashed=True)
        l20 = T("0.2", 28, color=TEAL).move_to(ax.c2p(18.7, .43))
        self.play(Create(c20), FadeIn(l20), knob.animate.move_to(dial.n2p(.1)), run_time=.65)
        c10 = curve_for(ax, .1, TEAL)
        l10 = T("0.1", 28, color=TEAL).move_to(ax.c2p(18.7, 1.42))
        self.play(Create(c10), FadeIn(l10), run_time=.55)

        self.at("10 to 15 percent")
        band = Line(dial.n2p(.10), dial.n2p(.15), color=RED, stroke_width=16)
        cutoff = T("measured cut-off", 28, color=RED).move_to([.15, -2.5, 0])
        self.play(Create(band), FadeIn(cutoff), run_time=.55)
        self.at("far below half")
        bracket = Brace(Line(dial.n2p(.15), dial.n2p(.5)), UP, color=TEAL)
        keeps = T("still keeps up", 28, color=TEAL).move_to([4.55, -2.5, 0])
        self.play(GrowFromCenter(bracket), FadeIn(keeps), run_time=.55)

        self.at("slows the rise")
        later = chip("later onset", TEXT, 30).move_to([3.25, 2.42, 0])
        self.play(FadeOut(VGroup(band, cutoff, bracket, keeps)),
                  Indicate(c10, color=TEAL, scale_factor=1.02), Indicate(zero, color=RED, scale_factor=1.02),
                  FadeIn(later), run_time=.8)
        self.finish()


def neuron(center, scale=1.0, color=TEXT):
    soma = Circle(radius=.68, color=color, stroke_width=5, fill_color=color, fill_opacity=.04).move_to(center)
    arms = VGroup(*[Line(center + .55 * np.array([np.cos(a), np.sin(a), 0]),
                         center + 1.35 * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=4)
                    for a in (0.5, 1.8, 3.0, 4.0)])
    axon = Line(center + RIGHT * .6, center + RIGHT * 2.05, color=color, stroke_width=5)
    return VGroup(arms, axon, soma).scale(scale, about_point=center)


class S11Neurons(SpokenScene):
    def construct(self):
        divider = Line([0, -3.45, 0], [0, 3.45, 0], color=GREY, stroke_width=2).set_opacity(.45)
        cell = Circle(radius=2.45, color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=.025).move_to([-3.45, .05, 0])
        neu = neuron(np.array([3.25, .1, 0]), 1.38)
        labs = VGroup(T("dividing cell", 30).move_to([-3.45, 3.05, 0]), T("neuron", 30).move_to([3.25, 3.05, 0]))
        rooms = VGroup(small_room(np.array([-3.45, .05, 0]), .95, .08, .25),
                       small_room(np.array([3.25, .1, 0]), .95, .08, .25))
        self.play(FadeIn(divider), Create(cell), Create(neu), FadeIn(labs), FadeIn(rooms), run_time=.8)

        self.at("rich in gangliosides")
        high = chip("high delivery", GREEN, 30).move_to([4.55, -2.55, 0])
        drops = VGroup(*[lozenge([2.55 + .34 * i, 1.55 - .18 * (i % 2), 0], .48) for i in range(5)])
        self.play(FadeIn(high), LaggedStart(*[FadeIn(x, shift=UP * .35) for x in drops], lag_ratio=.15), run_time=.75)
        self.at("do not divide")
        no_div = chip("no division", RED, 28).move_to([1.65, -2.55, 0])
        self.play(FadeOut(high), FadeIn(no_div), Indicate(neu, color=RED, scale_factor=1.03), run_time=.55)

        self.at("splits its stored")
        daughter_l = Circle(radius=1.45, color=TEXT, stroke_width=5).move_to([-5.05, .0, 0])
        daughter_r = Circle(radius=1.45, color=TEXT, stroke_width=5).move_to([-1.8, .0, 0])
        room_l = small_room(np.array([-5.05, 0, 0]), .72, .06, .12)
        room_r = small_room(np.array([-1.8, 0, 0]), .72, .06, .12)
        self.play(FadeOut(no_div), Transform(cell, VGroup(daughter_l, daughter_r)),
                  Transform(rooms[0], VGroup(room_l, room_r)), run_time=1.0)
        self.play(rooms[0].animate(rate_func=there_and_back).shift(UP * .12), run_time=.55)

        self.at("cannot dilute")
        growing = VGroup(*[lozenge([2.78 + .31 * (i % 4), -.55 + .26 * (i // 4), 0], .45) for i in range(12)])
        self.play(FadeOut(drops), LaggedStart(*[FadeIn(x, shift=DOWN * .2) for x in growing], lag_ratio=.08),
                  rooms[1][3].animate.stretch(2.2, 1, about_edge=DOWN), run_time=1.0)
        self.finish()


class S12Return(SpokenScene):
    def construct(self):
        xs = (-4.45, 0, 4.45)
        figures = VGroup(person(xs[0], scale=.48), person(xs[1], scale=.48),
                         person(xs[2], child=True, color=RED, scale=.45)).move_to([0, -2.25, 0])
        bars = VGroup(bar_gauge(-3.72, 1.25, .5, TEAL, False), bar_gauge(.72, 1.25, .5, TEAL, False),
                      bar_gauge(5.12, 1.1, .03, RED, False)).shift(DOWN * 2.15)
        ticks = VGroup(T("✓", 34, color=GREEN).move_to([-4.45, -1.0, 0]),
                       T("✓", 34, color=GREEN).move_to([0, -1.0, 0]))
        rooms = VGroup(small_room(np.array([-4.45, 1.25, 0]), 1.12, .34, .14),
                       small_room(np.array([0, 1.25, 0]), 1.12, .34, .14),
                       small_room(np.array([4.45, 1.25, 0]), 1.12, .06, .30))
        flows = VGroup(falling_drops(np.array([-4.45, 1.25, 0]), .95, phase=.08),
                       falling_drops(np.array([0, 1.25, 0]), .95, phase=.14),
                       falling_drops(np.array([4.45, 1.25, 0]), .95, phase=.20))
        for p in figures:
            p.add_updater(lambda m, dt: m.shift(UP * .0025 * np.sin(self.renderer.time * 1.8 + m.get_x())))
        self.play(FadeIn(figures), FadeIn(bars), FadeIn(ticks), FadeIn(rooms), FadeIn(flows), run_time=.75)
        self.at("sealed room")
        self.play(*[Indicate(r[0], color=BLUE, scale_factor=1.05) for r in rooms], run_time=.65)
        self.at("still keeps up")
        self.play(rooms[0][3].animate(rate_func=there_and_back).stretch(1.2, 1, about_edge=DOWN),
                  rooms[1][3].animate(rate_func=there_and_back).stretch(1.2, 1, about_edge=DOWN), run_time=.7)
        self.at("parents are fine")
        self.play(Indicate(ticks, color=GREEN, scale_factor=1.15), run_time=.45)
        self.at("almost no drain")
        self.play(rooms[2][3].animate.stretch(2.4, 1, about_edge=DOWN),
                  rooms[2][0].animate.scale(1.18), run_time=.85)
        self.at("hit hardest")
        n = neuron(np.array([5.7, -.7, 0]), .34, color=GOLD)
        self.play(FadeIn(n), Flash(n, color=GOLD, flash_radius=.7), run_time=.65)
        self.finish()


class S13End(EndCard):
    LINE = "What a room holds: delivery in, against clearance out."

    def construct(self):
        room = schematic_room(np.array([0, 0, 0]), 2.65, 1.2, 5.6, .2, jaws=4, labels=False).set_opacity(.20)
        room[3].set_opacity(.42)
        line = T(self.LINE, 40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", 28, color=TEAL)
        card = VGroup(line, sub).arrange(DOWN, buff=.48)
        backing = RoundedRectangle(corner_radius=.18, width=12.15, height=1.72,
                                   stroke_width=0, fill_color=BG, fill_opacity=.94).move_to(card)
        self.add(room)
        self.play(FadeIn(backing), FadeIn(card, shift=UP * .18), run_time=.65)
        self.wait(max(0, self.narration_s - .65))
