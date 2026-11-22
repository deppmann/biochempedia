"""Axon guidance assays, timed to the recorded narration."""
from bp_parts import *
from bp_style import EndCard

# COLOR MAP: teal axons, gold attractive cues and dates, red repulsive cues,
# blue pipette, purple Eph/ephrin, grey tissue and dish structure.
PURPLE = "#B58CD9"
FLOOR = "#294553"
RIM = "#7697AA"
FIBRE = "#609392"
CELL = "#A9DEE0"
NEUTRAL = "#365767"
STRIPE = "#563B61"
REPELLENT_LANE = "#583C4D"
ATTRACT = GOLD
REPEL = RED
TITLE = "Testing What Steers a Growing Axon"
LESSON = "Axon Guidance Assays"
QUESTION = "If avoidance is active repulsion, what happens?"
QUESTION_CARD = dict(y=3.35, size=34, max_w=11.6)
CENTER = (-0.55, -0.03)
RADIUS = 2.95


def p(x, y):
    return np.array([x, y, 0.0])


def label(text, x, y, color=TEXT, size=32):
    return T(text, size, color).move_to(p(x, y))


def timekeeper(start=0):
    clock = ValueTracker(start)
    clock.add_updater(lambda m, dt: m.increment_value(dt))
    return clock


def disk(center=CENTER, radius=RADIUS, color=FLOOR):
    return VGroup(
        Circle(radius=radius + 0.045, fill_color=color, fill_opacity=1,
               stroke_color=RIM, stroke_width=2).move_to(p(*center)),
        Circle(radius=radius - 0.045, stroke_color=FIBRE, stroke_width=1,
               stroke_opacity=0.45).move_to(p(*center)),
    )


def stripes(center=CENTER, radius=RADIUS, tint=STRIPE, neutral_first=True):
    x, y = center
    r = radius - 0.075
    cuts = np.array([-1, -0.77, -0.51, -0.25, 0, 0.25, 0.51, 0.77, 1]) * (r - 0.002)
    bands = VGroup()
    for i, (a, b) in enumerate(zip(cuts, cuts[1:])):
        xs = np.linspace(a, b, 25)
        edge = np.sqrt(r * r - xs * xs)
        vertices = [p(x + u, y + v) for u, v in zip(xs, edge)]
        vertices += [p(x + u, y - v) for u, v in zip(xs[::-1], edge[::-1])]
        bands.add(Polygon(*vertices, stroke_width=0, fill_opacity=1,
                          fill_color=NEUTRAL if (i % 2 == 0) == neutral_first else tint))
    return bands


def gel_mesh(center=CENTER, radius=RADIUS):
    rng = np.random.default_rng(29)
    fibers = VGroup()
    for _ in range(82):
        xy = rng.uniform(-1, 1, 2)
        uv = xy + rng.uniform(-0.21, 0.21, 2)
        if max(np.linalg.norm(xy), np.linalg.norm(uv)) < 0.96:
            a, b = [p(*(np.array(center) + radius * v)) for v in (xy, uv)]
            fibers.add(Line(a, b, color=FIBRE, stroke_width=rng.uniform(0.8, 3.2),
                            stroke_opacity=rng.uniform(0.19, 0.5)))
    return fibers


def tissue(x, y, size=0.55, color=GREY, tall=1):
    angles = np.linspace(0, TAU, 17)[:-1]
    radius = size * (1 + 0.11 * np.sin(5 * angles) + 0.08 * np.cos(7 * angles))
    shape = VMobject(fill_color=color, fill_opacity=0.68, stroke_color=color, stroke_width=2.5)
    path = [p(x + r * np.cos(a), y + tall * r * np.sin(a)) for a, r in zip(angles, radius)]
    shape.set_points_smoothly(path + [path[0]])
    nuclei = VGroup(*[Dot(p(x + size * u, y + tall * size * v), radius=size * 0.085,
                            color=FLOOR, fill_opacity=0.6)
                      for u, v in [(-0.55, 0.15), (-0.1, 0.48), (0.42, 0.31),
                                   (0.2, -0.48), (-0.37, -0.39), (0.49, -0.11)]])
    return VGroup(shape, nuclei)


def growth_cone(clock, pose, scale=1, highlight=None):
    """An axon shaft and a fan with probing filopodia. Pose gives base, tip, angle, spread."""
    shaft = VMobject(stroke_color=TEAL, stroke_width=5 * scale + 1)
    fan = VMobject(fill_color=TEAL, fill_opacity=0.65, stroke_color=CELL, stroke_width=2)
    sheets = VMobject(fill_color=CELL, fill_opacity=0.24, stroke_width=0)
    spikes = VGroup(*[VMobject(stroke_color=CELL, stroke_width=1.4 + scale) for _ in range(9)])
    receptors = VGroup(*[Dot(radius=0.037 * scale, color=PURPLE) for _ in range(5)])
    drawing = VGroup(shaft, fan, sheets, spikes, receptors)
    angles = np.linspace(-1.25, 1.25, len(spikes))

    def draw(_):
        t = clock.get_value()
        base, nose, direction, spread = pose(t)
        forward = p(np.cos(direction), np.sin(direction))
        side = p(-np.sin(direction), np.cos(direction))
        neck = nose - forward * (0.55 * scale)

        def point(u, v):
            return nose + scale * (u * forward + v * side * spread)

        bend = neck - forward * (0.44 * scale)
        shaft.set_points_smoothly([base, interpolate(base, bend, 0.5) + DOWN * 0.08,
                                   bend, neck])
        tips = [point(0.24 * np.cos(a), 0.46 * np.sin(a)) for a in angles]
        outline = [neck, point(-0.32, -0.17), *tips, point(-0.32, 0.17), neck]
        fan.set_points_smoothly(outline)
        web = [point(-0.20, -0.28), *[point(0.31 * np.cos(a), 0.52 * np.sin(a)) for a in angles],
               point(-0.20, 0.28), point(-0.20, -0.28)]
        sheets.set_points_smoothly(web)
        mode = highlight() if highlight else None
        sheets.set_fill(CELL, opacity=0.50 if mode == "sheets" else 0.18)
        for i, (a, start, spike) in enumerate(zip(angles, tips, spikes)):
            reach = spread * (0.29 + 0.17 * np.sin(4.7 * t + i * 0.93))
            end = point(0.24 * np.cos(a) + reach * np.cos(a),
                        0.46 * np.sin(a) + reach * np.sin(a * 1.15))
            spike.set_points_smoothly([start, (start + end) / 2 + side * 0.06 * spread *
                                        np.sin(5.4 * t + i), end])
            spike.set_stroke(width=(3.2 if mode == "spikes" else 1.5) * scale,
                             opacity=min(1, spread * 1.5))
        for marker, k in zip(receptors, (0, 2, 4, 6, 8)):
            marker.move_to(tips[k]).set_opacity(
                (1 if mode == "receptors" else 0.48) * min(1, spread))

    draw(drawing)
    return drawing.add_updater(draw)


def cloud(clock, color, center, spread=(0.8, 0.48), count=29, seed=3, square=False, radius=1):
    """A drifting plume of schematic cue dots."""
    rng = np.random.default_rng(seed)
    phases = rng.uniform(0, TAU, (count, 3))
    offsets = rng.uniform(-1, 1, (count, 2))
    offsets = offsets[np.linalg.norm(offsets, axis=1).argsort()]
    particles = VGroup()
    for d in rng.uniform(0.026, 0.083, count) * radius:
        if square:
            particles.add(Square(side_length=d * 1.7, fill_color=color,
                                 fill_opacity=0.8, stroke_width=0).rotate(PI / 4))
        else:
            particles.add(Dot(radius=d, color=color))

    def drift(_):
        t = clock.get_value()
        c = center(t) if callable(center) else center
        for dot, (u, v), (a, b, h) in zip(particles, offsets, phases):
            dot.move_to(p(c[0] + spread[0] * (u + 0.16 * np.sin(2.2 * t + a)),
                          c[1] + spread[1] * (v + 0.20 * np.sin(1.9 * t + b))))
            dot.set_opacity(0.64 + 0.24 * np.sin(2.7 * t + h))

    drift(particles)
    return particles.add_updater(drift)


def bath(clock, center=CENTER, radius=RADIUS, color=REPEL, square=True, count=57):
    """Cue spread throughout the bath, clipped inside the physical rim."""
    rng = np.random.default_rng(15)
    xy = [rng.uniform(0, TAU, count), rng.uniform(0.08, 0.87, count) ** 0.65]
    particles = VGroup()
    for r in rng.uniform(0.032, 0.065, count) * radius / RADIUS:
        shape = (Square(side_length=2 * r, fill_color=color, stroke_width=0).rotate(PI / 4)
                 if square else Dot(radius=r, color=color))
        particles.add(shape)

    def stir(_):
        t = clock.get_value()
        for dot, a, r in zip(particles, *xy):
            u = a + 0.14 * t * (1.4 - r)
            v = min(0.91, r + 0.035 * np.sin(1.2 * t + 3 * a))
            dot.move_to(p(center[0] + radius * v * np.cos(u), center[1] + radius * v * np.sin(u)))
            dot.set_opacity(0.58 + 0.23 * np.sin(2 * t + 9 * a))

    stir(particles)
    return particles.add_updater(stir)


def pipette(x=1.35, y=0.80):
    return Polygon(p(x, y), p(x + 0.3, y + 0.27), p(x + 1.55, y + 1.06),
                   p(x + 1.73, y + 0.79), p(x + 0.43, y + 0.12),
                   stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.28)


def hook_world(clock):
    def pose(t):
        return (p(-3.32, -0.18), p(-0.05 + 0.10 * np.sin(t * 1.4),
                                     -0.10 + 0.11 * np.sin(t * 1.8)),
                0.04 + 0.09 * np.sin(t * 1.65), 1)

    cone = growth_cone(clock, pose, 1.63)
    upper = cloud(clock, ATTRACT, (0.65, 1.40), (0.86, 0.55), count=24)
    lower = cloud(clock, REPEL, (0.72, -1.45), (0.85, 0.54), count=24, seed=7)
    return disk(), cone, VGroup(upper, lower)


def gel_assay(clock, progress, steering, center=CENTER, radius=RADIUS, history=False):
    x, y = center
    s = radius / RADIUS
    left = tissue(x - 1.77 * s, y - 0.24 * s, size=0.53 * s, tall=1.12)
    right = tissue(x + 1.77 * s, y + 0.65 * s, size=0.49 * s)
    cones = VGroup()
    for i in range(3):
        def pose(t, i=i):
            length = progress.get_value()
            turn = steering.get_value()
            level = (i - 1) * 0.40
            return (p(x + s * -1.65, y + s * (-0.24 + level * 0.50)),
                    p(x + s * (-1.15 + (1.95 + 0.15 * i + min(0, turn) * 0.54) * length),
                      y + s * (-0.24 + level + length * turn * (0.62 + 0.15 * i) +
                               0.16 * np.sin(3 * t + i))),
                    0.12 * (i - 1) + 0.84 * turn * length, 0.83)
        cones.add(growth_cone(clock, pose, 0.66 * s))
    plume = cloud(clock, ATTRACT,
                  lambda t: (x + s * (1.56 - 1.25 * progress.get_value() + 0.14 * np.sin(1.4 * t)),
                             y + s * (0.69 + 0.14 * np.sin(1.2 * t))),
                  (0.93 * s, 0.62 * s), count=33 if not history else 34, radius=1 if not history else 0.84)
    return disk(center, radius), gel_mesh(center, radius), left, right, cones, plume


def stripe_axons(clock, travel, retract, turn):
    cones = VGroup()
    for i, y in enumerate((-1.34, -0.22, 1.02)):
        def pose(t, i=i, y=y):
            u, bend = travel.get_value(), turn.get_value()
            return (p(-2.85, y * 0.74), p(-2.46 + 3.08 * u - i * 0.10,
                     y + 0.69 * bend + 0.13 * np.sin(3 * t + i)),
                    0.08 * np.sin(2.5 * t + i) + 1.75 * bend, retract.get_value())
        cones.add(growth_cone(clock, pose, 0.76))
    return cones


CELL_SITES = [(-2.39, -1.05), (-0.93, 0.22), (0.56, 1.07), (0.56, -1.26)]
CELL_DESTINATIONS = [(-1.68, -1.53), (-0.19, 0.28), (0.54, 1.22), (0.54, -1.40)]
PREDICT_POSE_S = 20.0


def crest_cells(clock, response, occupancy, hold_at=None):
    """Cell positions stay on neutral lanes until the response allows a crossing."""
    group = VGroup()
    for i, (start, end) in enumerate(zip(CELL_SITES, CELL_DESTINATIONS)):
        body = VMobject(stroke_color=CELL, stroke_width=2, fill_color=TEAL, fill_opacity=0.66)
        nucleus = Dot(radius=0.09, color=FLOOR)
        markers = VGroup(*[Circle(radius=0.043, stroke_color=PURPLE, stroke_width=2) for _ in range(7)])
        cell = VGroup(body, nucleus, markers)
        angles = np.linspace(0, TAU, 19)

        def migrate(_, i=i, start=start, end=end, body=body, nucleus=nucleus,
                    markers=markers, angles=angles):
            t = clock.get_value() if hold_at is None else min(hold_at, clock.get_value())
            hx, hy = interpolate(np.array(start), np.array(end), response.get_value())
            c = p(hx + 0.13 * np.sin(1.6 * t + 2 * i),
                  hy + 0.47 * np.sin(0.98 * t + i * 1.1))
            shape = 1 + 0.16 * np.sin(3 * angles + 4.1 * t + i)
            points = [c + p(0.26 * r * np.cos(a), 0.35 * r * np.sin(a))
                      for a, r in zip(angles, shape)]
            body.set_points_smoothly(points)
            nucleus.move_to(c)
            for marker, j in zip(markers, (0, 3, 5, 8, 10, 13, 15)):
                marker.move_to(points[j]).set_fill(PURPLE, opacity=occupancy.get_value())

        migrate(cell)
        group.add(cell.add_updater(migrate))
    return group


def crest_world(clock, crossing, occupied, hold_at=None):
    return (disk(), stripes(neutral_first=False),
            crest_cells(clock, crossing, occupied, hold_at=hold_at))


def prediction_world(clock):
    occupied = ValueTracker(0)
    return (*crest_world(clock, ValueTracker(0), occupied, hold_at=PREDICT_POSE_S),
            bath(clock, color=PURPLE, square=False, count=47))


class S01Hook(SpokenScene, TitleCard):
    TITLE = TITLE
    LESSON = LESSON

    def construct(self):
        clock = timekeeper()
        floor, cone, cues = hook_world(clock)
        question = label("?", 4.3, 0.25, GOLD, 105)
        self.add(floor, clock, cone, cues, question, scope_tag(size=28, color=TEXT))
        self.at("that fiber is", lead=0.35)
        axon = label("axon", -4.92, 0.25, CELL)
        self.play(FadeOut(question), FadeIn(axon), run_time=0.42)
        self.at("flat moving fan")
        growth = label("growth cone", 4.15, 0.25, CELL)
        self.play(FadeIn(growth), run_time=0.42)
        self.at("molecules outside")
        guide = label("guidance cues", 4.30, -1.19, GOLD)
        self.play(FadeIn(guide), run_time=0.40)
        self.finish()


class S02Title(TitleCard):
    TITLE = TITLE
    LESSON = LESSON

    def construct(self):
        clock = timekeeper(14.07)
        self.add(clock, *hook_world(clock))
        veil = Circle(radius=RADIUS + 0.09, fill_color=BG, fill_opacity=0.89,
                      stroke_width=0).move_to(p(*CENTER))
        title = T(self.TITLE.replace(" a Growing", "\na Growing"), 44, TEXT,
                  font=TITLE_FONT).move_to(p(CENTER[0], 0.85))
        backing = RoundedRectangle(corner_radius=0.14, width=title.width + 0.48,
                                   height=title.height + 0.36, fill_color=BG,
                                   fill_opacity=1, stroke_width=0).move_to(title)
        self.play(FadeIn(veil), FadeIn(backing), run_time=0.26)
        self.play(FadeIn(title), run_time=0.27)
        self.wait(11 / 15)
        self.play(FadeOut(title), run_time=0.22)
        self.play(FadeOut(veil), FadeOut(backing), run_time=0.20)


class S03Logic(SpokenScene):
    def construct(self):
        clock = timekeeper()
        turn, part = ValueTracker(0), ValueTracker(0)
        modes = (None, "spikes", "sheets", "receptors")

        def pose(t):
            u = turn.get_value()
            return (p(-3.35, -0.2),
                    p(-0.33 + 0.15 * u + 0.25 * np.sin(1.25 * t),
                      -0.18 + 0.58 * u + 0.32 * np.sin(1.7 * t)),
                    0.63 * u + 0.29 * np.sin(1.9 * t), 1.04 + 0.20 * np.sin(2.4 * t))

        cone = growth_cone(clock, pose, 1.65, lambda: modes[int(part.get_value())])
        self.add(clock, disk(), cone, scope_tag(size=28, color=TEXT))
        self.at("probes its surface")
        part.set_value(1)
        spikes = label("actin spikes", 4.03, 0.95, CELL)
        self.play(FadeIn(spikes), run_time=0.40)
        self.at("sheets", lead=0.38)
        part.set_value(2)
        sheets = label("sheets", 4.03, 0.95, CELL)
        self.play(swap(spikes, sheets), run_time=0.42)
        self.at("cue -sensing receptors")
        part.set_value(3)
        receptors = label("receptors", 4.03, 0.95, PURPLE)
        self.play(swap(sheets, receptors), run_time=0.38)
        self.at("when a cue")
        part.set_value(0)
        upper = cloud(clock, ATTRACT, lambda t: (0.90, 1.44 + 0.17 * np.sin(t)),
                      (0.7, 0.42), count=26)
        self.play(FadeOut(receptors), FadeIn(upper, shift=DOWN * 0.24), run_time=0.62)
        self.at("it turns toward")
        self.play(turn.animate.set_value(1), run_time=0.65)
        self.at("away", lead=0.35)
        lower = cloud(clock, REPEL, (0.75, -1.4), (0.62, 0.36), seed=8)
        self.play(FadeOut(upper), FadeIn(lower), run_time=0.42)
        self.play(turn.animate.set_value(1.55), run_time=0.82)
        self.at("cues act on")
        fixed = VGroup(*[Dot(p(4.25 + i * 0.28, 1.46), 0.068, color=REPEL) for i in range(4)])
        contact = label("on contact", 4.67, 0.92, TEXT, 30)
        self.play(FadeOut(lower), FadeIn(fixed), FadeIn(contact), run_time=0.42)
        self.at("across distance")
        drift = cloud(clock, ATTRACT, (4.62, -0.50), (0.48, 0.22), count=12)
        distance = label("across distance", 4.66, -1.03, TEXT, 30)
        self.play(FadeIn(drift), FadeIn(distance), run_time=0.42)
        self.at("its own dish")
        self.play(FadeOut(fixed), FadeOut(contact), FadeOut(drift), FadeOut(distance), run_time=0.52)
        self.finish()


class S04Collagen(SpokenScene):
    def construct(self):
        clock = timekeeper()
        progress, steering = ValueTracker(0.05), ValueTracker(0)
        floor, mesh, left, right, cones, plume = gel_assay(clock, progress, steering)
        self.add(clock, floor, scope_tag(size=28, color=TEXT))
        self.at("cues across distance", lead=0.45)
        self.play(FadeIn(mesh), run_time=0.84)
        self.at("embed living tissue")
        self.play(FadeIn(left), FadeIn(right), run_time=0.72)
        self.at("called explants", lead=0.40)
        explants = label("explants", -4.97, 0.10, TEXT)
        self.play(FadeIn(explants), FadeIn(cones), run_time=0.37)
        self.at("in a collagen")
        gel = label("collagen gel", 4.36, -0.10, TEXT)
        self.play(FadeIn(gel), progress.animate.set_value(0.32), run_time=1.48)
        self.at("a secreted cue")
        self.play(FadeIn(plume), progress.animate.set_value(0.68), run_time=1.65)
        self.at("drawing axons toward", lead=0.45)
        attract = label("attract", 4.16, 1.13, ATTRACT, 36)
        self.play(FadeIn(attract, run_time=0.35), steering.animate(run_time=0.64).set_value(0.98),
                  progress.animate(run_time=0.64).set_value(0.90))
        self.at("pushing them away", lead=0.10)
        repel = label("repel", 4.16, 1.13, REPEL, 36)
        red_plume = cloud(clock, REPEL, (0.12, 0.72), (1.02, 0.66), count=35, seed=9)
        self.play(swap(attract, repel, run_time=0.66), FadeOut(plume), FadeIn(red_plume),
                  steering.animate.set_value(-1.02), progress.animate.set_value(1),
                  right[0].animate.set_fill(REPEL, opacity=0.65), run_time=0.74)
        self.finish()


class S05Stripes(SpokenScene):
    def construct(self):
        clock = timekeeper()
        travel, retract, bend = ValueTracker(0.20), ValueTracker(0.9), ValueTracker(0)
        mesh = gel_mesh()
        lanes = stripes(tint=REPELLENT_LANE)
        self.add(clock, disk(), mesh, scope_tag(size=28, color=TEXT))
        self.at("lay alternating")
        self.play(FadeOut(mesh), FadeIn(lanes), run_time=1.03)
        self.at("like a striped")
        carpet = label("striped carpet", 4.43, 0.25, TEXT)
        self.play(FadeIn(carpet), run_time=0.49)
        self.at("place axons across", lead=0.55)
        source = tissue(-2.84, -0.07, size=0.27, tall=4.35)
        self.play(FadeIn(source), run_time=0.40)
        self.add(stripe_axons(clock, travel, retract, bend))
        self.play(travel.animate.set_value(0.24), run_time=1.14)
        self.play(travel.animate.set_value(0.42), lanes[2].animate.set_fill("#587686"),
                  run_time=0.77)
        self.at("meets border after")
        self.play(retract.animate.set_value(0.30), run_time=0.36)
        self.play(travel.animate.set_value(0.57), retract.animate.set_value(0.88),
                  lanes[2].animate.set_fill(NEUTRAL), run_time=0.42)
        self.play(retract.animate.set_value(0.31), run_time=0.36)
        self.at("chooses a lane", lead=0.12)
        self.play(travel.animate.set_value(0.76), run_time=0.36)
        self.play(bend.animate.set_value(0.82), retract.animate.set_value(0.9),
                  lanes[4].animate.set_fill("#587686"), run_time=0.74)
        self.finish()


class S06CollapseTurning(SpokenScene):
    def construct(self):
        clock = timekeeper()
        spread, turn = ValueTracker(1), ValueTracker(0)

        def pose(t):
            u = turn.get_value()
            return (p(-0.75, -2.52), p(-0.70 - 0.95 * u, 0.06 + 0.38 * u),
                    1.45 + 0.88 * u + 0.09 * np.sin(3 * t), spread.get_value())

        cone = growth_cone(clock, pose, 1.93)
        membranes = bath(clock)
        self.add(clock, disk(), cone, scope_tag(size=28, color=TEXT))
        self.at("flood a dish")
        self.play(FadeIn(membranes), run_time=1.23)
        self.at("responsive fans", lead=0.08)
        self.play(spread.animate.set_value(0.07), run_time=1.25)
        self.at("collapse into thin", lead=0)
        collapse = label("collapse", 4.20, 0.18, REPEL, 37)
        self.play(FadeIn(collapse), run_time=0.37)
        self.at("within minutes", lead=0)
        self.wait(0.70)
        self.play(FadeOut(collapse), FadeOut(membranes), spread.animate.set_value(1), run_time=0.92)
        self.at("release the cue")
        glass = pipette()
        plume = cloud(clock, REPEL, (0.42, 0.88), (0.85, 0.46), seed=11)
        self.play(FadeIn(glass, shift=DL * 0.55), run_time=0.60)
        self.play(FadeIn(plume, shift=RIGHT * 0.40), run_time=0.66)
        self.at("the cone turns")
        turning = label("turning", 4.25, 0.18, REPEL, 37)
        self.play(FadeIn(turning, run_time=0.40), turn.animate(run_time=1.12).set_value(0.93))
        self.at("every assay places")
        self.play(FadeOut(turning), run_time=0.40)
        self.at("so motion separates")
        self.play(turn.animate.set_value(1.22), run_time=1.74)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        clock = timekeeper()
        floor, lanes, cells, soluble = prediction_world(clock)
        self.add(clock, floor, lanes, cells, scope_tag(size=28, color=TEXT))
        self.at("migrating neural crest")
        crest = label("neural crest cells", 4.45, 1.08, CELL, 30)
        self.play(FadeIn(crest), run_time=0.48)
        self.at("carry f receptors")
        receptors = label("Eph receptors", 4.45, 1.08, PURPLE, 30)
        self.play(swap(crest, receptors), run_time=0.52)
        self.at("avoid stripes")
        ephrin = label("ephrin-B1", -4.92, 0.95, PURPLE, 30)
        neutral = label("neutral", -4.92, -0.75, CELL, 30)
        stripe_key = Square(side_length=0.27, stroke_color=PURPLE, stroke_width=1.5,
                            fill_color=STRIPE, fill_opacity=1).move_to(p(-6.11, 0.95))
        neutral_key = Square(side_length=0.27, stroke_color=RIM, stroke_width=1.5,
                              fill_color=NEUTRAL, fill_opacity=1).move_to(p(-6.11, -0.75))
        self.play(FadeIn(ephrin), FadeIn(neutral), FadeIn(stripe_key), FadeIn(neutral_key),
                  run_time=0.55)
        self.at("a skeptic says")
        doubt = label("poor surface?", 4.45, 1.08, GOLD)
        self.play(swap(receptors, doubt), run_time=0.55)
        self.at("now add soluble")
        self.play(FadeOut(doubt), FadeIn(soluble), run_time=0.85)
        free = label("soluble ephrin-B1", 4.60, -0.50, PURPLE, 30)
        self.play(FadeIn(free), run_time=0.45)
        self.at("leaving the stripe's")
        self.play(FadeOut(neutral), FadeOut(ephrin), FadeOut(stripe_key), FadeOut(neutral_key),
                  run_time=0.48)
        self.at("if avoidance is")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_CARD)), run_time=0.45)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_CARD
    SECONDS = 4.5

    def construct(self):
        clock = timekeeper(23.90)
        frame, lanes, cells, soluble = prediction_world(clock)
        progress = ValueTracker(0)
        rail = Line(p(-2.35, -3.36), p(1.25, -3.36), color=RIM, stroke_width=4)
        fill = Line(rail.get_start(), rail.get_start() + RIGHT * 0.01, color=GOLD, stroke_width=4)
        fill.add_updater(lambda m: m.put_start_and_end_on(
            rail.get_start(), rail.point_from_proportion(max(0.003, progress.get_value()))))
        self.add(clock, frame, lanes, cells, soluble, question_card(self.QUESTION, **self.CARD),
                 label("soluble ephrin-B1", 4.60, -0.50, PURPLE, 30),
                 scope_tag(size=28, color=TEXT), rail, fill)
        self.play(progress.animate.set_value(1), rate_func=linear, run_time=self.SECONDS)


def control_inset(clock, nonbinding=False):
    center, radius = (4.5, -0.40), 1.52
    x, y = center
    body = VMobject(stroke_color=CELL, stroke_width=2, fill_color=TEAL, fill_opacity=0.77)
    receptors = VGroup(*[Circle(radius=0.03, stroke_color=PURPLE, stroke_width=2)
                         for _ in range(5)])

    def migrate(_):
        t = clock.get_value()
        c = p(x - 0.18 - 0.015 * np.cos(t * 1.9), y + 0.52 * np.sin(t * 0.98))
        ang = np.linspace(0, TAU, 17)
        points = [c + p(0.11 * np.cos(a) * (1 + 0.12 * np.sin(t * 3 + a)),
                        0.18 * np.sin(a)) for a in ang]
        body.set_points_smoothly(points)
        for marker, j in zip(receptors, (0, 3, 6, 10, 13)):
            marker.move_to(points[j])

    migrate(body)
    body.add_updater(migrate)
    protein = cloud(clock, BLUE, (x + 0.63, y), (0.44, 0.67), count=16,
                    square=True, seed=35, radius=0.85) if nonbinding else VGroup()
    return VGroup(disk(center, radius), stripes(center, radius, neutral_first=False), body, receptors, protein)


class S09Controls(SpokenScene):
    def construct(self):
        clock = timekeeper()
        crossing, occupied = ValueTracker(0), ValueTracker(0)
        floor, lanes, cells = crest_world(clock, crossing, occupied)
        soluble = bath(clock, color=PURPLE, square=False, count=47)
        study = label("1997 chick study", 4.45, 1.98, GOLD, 30)
        self.add(clock, floor, lanes, soluble, cells, scope_tag(size=28, color=TEXT))
        self.at("the cells cross")
        self.play(crossing.animate.set_value(0.94), run_time=2.8)
        self.at("as the 1997")
        self.play(FadeIn(study), run_time=0.46)
        self.at("free ephrin fills")
        self.play(occupied.animate.set_value(1), run_time=2.06)
        self.at("the border no longer")
        self.play(crossing.animate.set_value(0.82), run_time=1.72)
        self.at("a merely poor")
        poor = control_inset(clock)
        expect = label("Expected", 4.50, 2.58, GOLD, 30)
        poor_label = label("poor surface", 4.50, 1.67, TEXT, 30)
        self.play(FadeOut(study), run_time=0.30)
        self.play(FadeIn(poor), FadeIn(expect), FadeIn(poor_label), run_time=0.55)
        self.at("the stripe itself")
        self.play(crossing.animate.set_value(1), run_time=1.1)
        self.at("a protein that")
        negative = control_inset(clock, nonbinding=True)
        negative_label = label("non-binding control", 4.50, 1.67, TEXT, 30)
        self.play(swap(poor_label, negative_label), FadeOut(poor), run_time=0.55)
        self.play(FadeIn(negative), run_time=0.48)
        self.finish()


class S10Limits(SpokenScene):
    def construct(self):
        clock = timekeeper()
        turn, spread, part, gmp = (ValueTracker(v) for v in (0, 1, 0, 0.3))
        floor = disk()
        plume = cloud(clock, REPEL, (0.86, 1.05), (0.55, 0.39), count=19, seed=11)
        glass = pipette()
        membranes = bath(clock, count=70)

        def pose(t):
            u = turn.get_value()
            return (p(-1.57, -2.35), p(-0.83 + 0.68 * u, 0.12 + 0.12 * np.sin(t * 1.3)),
                    1.45 - 0.75 * u + 0.10 * np.sin(2.1 * t), spread.get_value())

        cone = growth_cone(clock, pose, 2.25,
                           lambda: "receptors" if part.get_value() else None)
        factors = label("layout, dose, time", 4.52, 0.36, TEXT, 30)
        self.add(clock, floor, glass, plume, cone, factors, scope_tag(size=28, color=TEXT))
        self.at("layout dose")
        self.play(turn.animate.set_value(-0.79), run_time=2.64)
        self.at("a cone turns")
        self.play(FadeOut(glass), FadeOut(plume), FadeIn(membranes), run_time=0.50)
        self.play(spread.animate.set_value(0.08), run_time=1.00)
        self.at("receptors decide", lead=0.55)
        self.play(FadeOut(membranes), FadeOut(factors), FadeIn(glass), FadeIn(plume),
                  spread.animate.set_value(1), turn.animate.set_value(0), run_time=0.66)
        part.set_value(1)
        receptor = label("receptors", 4.52, 0.36, PURPLE)
        self.play(FadeIn(receptor), run_time=0.40)
        self.at("a cone answers")
        self.play(turn.animate.set_value(-0.80), run_time=1.42)
        self.at("internal state")
        part.set_value(0)
        gauge_label = label("cyclic GMP", 4.52, 0.36, TEXT)
        # A level without numerical units or a direction-of-effect label.
        def level():
            center = pose(clock.get_value())[1] + DOWN * 0.36
            w, h = 0.49, 0.12
            track = Line(center - RIGHT * (w / 2), center + RIGHT * (w / 2),
                         color=FLOOR, stroke_width=10)
            fill = Line(track.get_start(), track.point_from_proportion(gmp.get_value()),
                        color=GOLD, stroke_width=6)
            return VGroup(track, fill)

        gauge = always_redraw(level)
        self.play(swap(receptor, gauge_label), FadeIn(gauge), run_time=0.58)
        self.at("cyclic gmp level")
        self.play(gmp.animate.set_value(0.72), run_time=1.12)
        self.at("can decide which")
        self.play(turn.animate.set_value(0.84), run_time=1.45)
        self.at("and a gel")
        progress, steering = ValueTracker(0.70), ValueTracker(0.63)
        _, mesh, left, right, axons, diffusing = gel_assay(clock, progress, steering)
        self.play(FadeOut(cone), FadeOut(gauge), FadeOut(gauge_label), FadeOut(glass),
                  FadeOut(plume), run_time=0.38)
        self.play(FadeIn(mesh), FadeIn(left), FadeIn(right), FadeIn(axons), FadeIn(diffusing),
                  run_time=0.55)
        self.play(progress.animate.set_value(0.98), run_time=1.22)
        self.at("the molecule itself", lead=0.42)
        mark = label("?", 3.67, 1.56, GOLD, 60)
        molecule = label("which molecule?", 4.43, 0.34, GOLD, 30)
        self.play(FadeIn(mark), FadeIn(molecule), run_time=0.42)
        self.finish()


class S11Unlocked1(SpokenScene):
    def construct(self):
        clock = timekeeper()
        panes = TwoPanel("1988 · Tessier-Lavigne", "1990 · Raper & Kapfhammer",
                         colors=(GOLD, GOLD), top=3.4, bottom=-3.02, size=30)
        left_at, right_at = (-3.3, -0.3), (3.3, -0.3)
        progress, steering, spread = ValueTracker(0.16), ValueTracker(0), ValueTracker(1)
        floor, mesh, dorsal, plate, axons, plume = gel_assay(
            clock, progress, steering, center=left_at, radius=1.70, history=True)
        right_dish = disk(right_at, radius=1.70)
        chick = VGroup()
        for i, x in enumerate((2.47, 3.30, 4.13)):
            def pose(t, i=i, x=x):
                return (p(x, -1.47), p(x + 0.04 * np.sin(2.2 * t + i), -0.05 + i * 0.11),
                        1.50 + 0.15 * np.sin(2 * t + i), spread.get_value())
            chick.add(growth_cone(clock, pose, 0.70))
        wash = bath(clock, center=right_at, radius=1.70, count=42)
        lab = label("Jessell lab", -3.30, 2.50, TEXT, 28)
        self.add(clock, panes.left_frame, floor, scope_tag(size=28, color=TEXT))
        self.at("in 1988", lead=0)
        self.play(FadeIn(panes.left_head), run_time=0.52)
        self.at("in thomas")
        self.play(FadeIn(lab), FadeIn(mesh), floor[0].animate.set_fill("#3E626D"), run_time=1.60)
        self.at("set embryonic")
        self.play(FadeIn(dorsal, shift=RIGHT * 0.22), FadeIn(plate, shift=LEFT * 0.22), run_time=0.75)
        names = VGroup(label("dorsal spinal cord", -4.30, -2.42, TEXT, 28),
                       label("floor plate", -2.21, 1.64, TEXT, 28))
        self.at("explants in collagen")
        self.play(FadeIn(names), FadeIn(axons), progress.animate.set_value(0.40),
                  floor[0].animate.set_fill("#294553"), run_time=1.24)
        self.at("something from the floor")
        unknown = label("?", -1.80, -2.42, GOLD, 32)
        diffusion = ValueTracker(0)

        def cue_halo():
            spread = diffusion.get_value()
            return VGroup(*[Ellipse(width=scale * (0.45 + 2.11 * spread),
                                     height=scale * (0.47 + 1.23 * spread),
                                     fill_color=ATTRACT, fill_opacity=0.20 + 0.16 * spread,
                                     stroke_width=0).move_to(p(-2.43 - 0.78 * spread, 0.08))
                            for scale in (1.0, 0.78, 0.50)])

        halo = always_redraw(cue_halo)
        halo.set_z_index(1)
        plume.set_z_index(2)
        axons.set_z_index(3)
        self.play(FadeIn(unknown), FadeIn(halo), FadeIn(plume, shift=LEFT * 0.52),
                  progress.animate.set_value(0.66), diffusion.animate.set_value(0.68), run_time=1.42)
        self.at("drawing midline")
        self.play(steering.animate.set_value(0.92), progress.animate.set_value(1),
                  diffusion.animate.set_value(1), run_time=2.13)
        self.at("later named")
        netrin = label("netrin", -1.80, -2.42, GOLD, 30)
        self.play(swap(unknown, netrin), run_time=0.53)
        self.at("in 1990")
        self.play(FadeIn(panes.right_frame), FadeIn(panes.right_head), FadeIn(right_dish), run_time=0.73)
        self.play(FadeIn(chick), run_time=0.62)
        self.at("added embryonic brain")
        brain = label("brain membranes", 3.30, 1.68, REPEL, 28)
        self.play(FadeIn(wash), right_dish[0].animate.set_fill("#553C48"), run_time=0.81)
        self.play(FadeIn(brain), run_time=0.39)
        self.at("chick dorsal root")
        ganglion = label("dorsal root ganglion", 3.30, -2.42, TEXT, 28)
        self.play(FadeIn(ganglion), run_time=0.56)
        self.at("cones collapsed")
        self.play(spread.animate.set_value(0.06), run_time=1.24)
        self.at("recovering once")
        self.play(FadeOut(wash), FadeOut(brain), right_dish[0].animate.set_fill(FLOOR), run_time=0.53)
        self.play(spread.animate.set_value(1), run_time=0.85)
        self.finish()


class S12Unlocked2(SpokenScene):
    def construct(self):
        clock = timekeeper()
        floor, lanes = disk(), stripes(tint=REPELLENT_LANE)
        travel, advance, spread = ValueTracker(0.12), ValueTracker(0), ValueTracker(0.92)

        def pose(t, y, test):
            pos = travel.get_value() + (advance.get_value() if test else 0)
            return (p(-2.88, y * 0.82), p(-2.60 + 3.3 * pos, y + 0.15 * pos +
                                         0.075 * np.sin(t * 2.3)),
                    0.10 * np.sin(t * 1.9), spread.get_value() if test else 0.92)

        axons = VGroup(*[growth_cone(clock, lambda t, y=y, i=i: pose(t, y, i == 1), 0.68)
                         for i, y in enumerate((-1.22, -0.04, 1.06))])
        retina = tissue(-2.88, 0.06, 0.27, tall=4.0)
        date = label("1987 · Walter & Bonhoeffer", -0.6, 3.37, GOLD, 32)
        self.add(clock, floor, scope_tag(size=28, color=TEXT))
        self.at("in 1987")
        self.play(FadeIn(date), run_time=0.58)
        self.at("jochen walter")
        self.play(LaggedStart(*[FadeIn(band) for band in lanes], lag_ratio=0.22), run_time=2.65)
        self.remove(*lanes)
        self.add(lanes)
        self.at("colleagues striped", lead=0)
        anterior = label("anterior", 4.53, 1.15, CELL, 30)
        posterior = label("posterior tectum", 4.53, -0.62, REPEL, 30)
        self.play(FadeIn(anterior), FadeIn(posterior), run_time=0.52)
        self.at("for retinal axons")
        retina_label = label("retina", -4.96, 0.22, TEXT, 30)
        self.play(FadeIn(retina), FadeIn(axons), run_time=0.42)
        self.play(FadeIn(retina_label), travel.animate.set_value(0.56), run_time=1.65)
        self.at("in 1995")
        later = label("1995 · Drescher & Bonhoeffer", -0.6, 3.37, GOLD, 32)
        self.play(swap(date, later), travel.animate.set_value(0.71), run_time=1.12)
        self.at("used that assay")
        selected = VGroup(*[Dot(p(0.51, 0.29 + i * 0.24), radius=0.074, color=REPEL)
                            for i in range(5)])
        sample = cloud(clock, REPEL, (4.56, 0.22), (0.50, 0.38), count=16, seed=20)
        self.play(FadeIn(selected), lanes[5].animate.set_fill("#89505F"), run_time=0.55)
        self.at("posterior tectum repellent")
        self.play(FadeOut(anterior), FadeIn(sample, shift=LEFT * 0.8),
                  advance.animate.set_value(0.10), run_time=0.76)
        self.play(spread.animate.set_value(0.13), advance.animate.set_value(-0.06), run_time=0.88)
        self.at("it is now called")
        ephrin = label("ephrin-A5", 4.53, -0.62, REPEL, 34)
        self.play(swap(posterior, ephrin), run_time=0.50)
        self.at("across gels stripes")
        self.play(FadeOut(later), FadeOut(ephrin), FadeOut(retina_label),
                  FadeOut(sample), FadeOut(retina), FadeOut(selected), FadeOut(axons), run_time=0.42)
        mesh = gel_mesh()
        close_turn = ValueTracker(-0.62)

        def close_pose(t):
            u = close_turn.get_value()
            return (p(-3.20, -0.17), p(-0.40 + 0.25 * np.sin(t * 1.6), 0.50 * u),
                    0.68 * u, 1)

        single = growth_cone(clock, close_pose, 2.03).set_z_index(2)
        bath_cues = bath(clock, count=43)
        self.play(FadeIn(single), FadeOut(lanes), FadeIn(mesh), run_time=0.68)
        lanes[5].set_fill(REPELLENT_LANE)
        self.play(FadeOut(mesh), FadeIn(lanes), close_turn.animate.set_value(0.03), run_time=0.74)
        self.play(FadeOut(lanes), FadeIn(bath_cues), run_time=0.62)
        self.at("growth cones show")
        self.play(close_turn.animate.set_value(0.72), run_time=1.04)
        self.at("attracts or repels")
        self.play(close_turn.animate.set_value(-0.71), run_time=1.15)
        self.finish()


class S13End(EndCard):
    LINE = "Place cues around growth cones; their motion separates attraction from repulsion."
