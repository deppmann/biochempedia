"""Field manipulation experiments, in one schematic grassland."""
from bp_parts import *

# COLOR MAP (shared palette from patch clamp)
# GREEN plants, BLUE water, ORANGE added material or warmth, YELLOW light,
# TEAL assigned treatment, GREY control and structures, RED interference,
# PURPLE diversity and predator cues, GOLD questions and time.
PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SOILS = ("#48614E", "#405346", "#37463D")
PALE_SOILS = ("#635F49", "#534F40", "#474537")
LEAVES = ("#A6CD79", "#83C167", "#629961", "#C1D797")
PALE_LEAVES = ("#D5CA93", "#A79B6B", "#A6B487", "#CEB87C")
QUESTION = "What else does the roof change? What extra plot checks?"
QUESTION_STYLE = dict(y=3.16, size=34, max_w=11.8)
ASSIGNMENT = (0, 1, 0)
BLOCK_Y = (1.37, -0.16, -1.69)
SHELTER_X = (-4.08, 0, 4.08)
TITLE_ZOOM = 1.045


def pt(x, y):
    return np.array([x, y, 0])


def segment(a, b, color=GREY, width=3):
    return Line(pt(*a), pt(*b), color=color, stroke_width=width)


def shape(points, color, opacity=1, stroke=None, width=2):
    return Polygon(*(pt(*p) for p in points), fill_color=color, fill_opacity=opacity,
                   stroke_color=stroke or color, stroke_width=width if stroke else 0)


def label(text, x=0, y=2.76, color=TEXT, size=32, max_w=11.8):
    return fit_text(text, max_w=max_w, size=size, min_size=28, color=color).move_to(pt(x, y))


def schematic():
    return scope_tag(size=28, color=TEXT)


def grass(xs, ground, height=1.0, palette=LEAVES, seed=1):
    rng = np.random.default_rng(seed)
    group = VGroup()
    for i, x in enumerate(xs):
        y = ground(x)
        h = height * rng.uniform(0.48, 1)
        spread = min(0.38, height * 0.36)
        for j, direction in enumerate((-1, 0.28, 1)):
            tip = spread * direction * rng.uniform(0.75, 1.15)
            top = h * (1 if j == 1 else 0.68)
            blade = shape([(x - 0.032, y), (x + tip * 0.33 - 0.046, y + top * 0.64),
                           (x + tip, y + top), (x + tip * 0.50 + 0.035, y + top * 0.53),
                           (x + 0.04, y)], palette[(i + j) % len(palette)])
            group.add(blade)
    return group


def wind(blades, phase=0, strength=0.22):
    # Tip displacement varies across the stand. The roots stay anchored.
    profiles = [(blade, blade.points.copy()) for blade in blades]
    clock = phase

    def sway(group, dt):
        nonlocal clock
        clock += dt
        for blade, points in profiles:
            new = points.copy()
            height = points[:, 1] - points[:, 1].min()
            new[:, 0] += strength * height * np.sin(clock * 2.2 + points[:, 0] * 0.85)
            blade.set_points(new)

    blades.add_updater(sway)
    return blades


def hillside(left=-6.36, right=6.36, sparse=False, zoom=1):
    mid = (left + right) / 2
    half = (right - left) / 2

    def surface(x):
        u = (x - mid) / half
        return 0.62 - (1.22 if sparse else 0.64) * u - 0.76 * u * u

    xs = np.linspace(left, right, 34)
    colors = PALE_SOILS if sparse else SOILS
    contours = [[(x, surface(x) - d * (1 + 0.075 * np.sin(1.9 * x))) for x in xs]
                for d in (0, 0.58, 1.3)]
    lower = [(x, -2.52) for x in xs]
    strata = VGroup(*(shape(a + b[::-1], col) for a, b, col in
                      zip(contours, [*contours[1:], lower], colors)))
    stems = grass(np.linspace(left + 0.22, right - 0.22, 11 if sparse else int(3.4 * half) + 6),
                  surface, height=0.76 if sparse else 1.38,
                  palette=PALE_LEAVES if sparse else LEAVES)
    return strata.scale(zoom, about_point=ORIGIN), stems.scale(zoom, about_point=ORIGIN)


def flower(x, y, height=0.57, color=PURPLE, kind=0):
    tip = pt(x, y + height)
    stem = Line(pt(x, y), tip, color=GREEN, stroke_width=3)
    if kind == 1:
        bloom = shape([(x - 0.14, tip[1]), (x, tip[1] + 0.17), (x + 0.14, tip[1]),
                       (x, tip[1] - 0.11)], color)
    elif kind == 2:
        bloom = VGroup(*(Dot(tip + d * 0.095, radius=0.066, color=color) for d in (LEFT, UP, RIGHT)))
    else:
        bloom = Dot(tip, radius=0.127, color=color)
    return VGroup(stem, bloom)


def soil_tile(x, y, width, depth, color=SOILS[0], boundary=None):
    a, b = x - width / 2, x + width / 2
    return VGroup(
        shape([(a, y), (b, y), (b, y - depth), (a, y - depth)], color,
              stroke=boundary, width=3),
        shape([(a + 0.02, y - depth * 0.57), (b - 0.02, y - depth * 0.72),
               (b - 0.02, y - depth + 0.025), (a + 0.02, y - depth + 0.025)],
              "#343E36", opacity=0.57),
    )


def block_field():
    bands, outlines, stands = VGroup(), VGroup(), VGroup()
    for row, (y, color) in enumerate(zip(BLOCK_Y, SOILS)):
        bands.add(soil_tile(-0.42 + row * 0.42, y - 0.16, 11.58, 1.15, color))
        borders, pair = VGroup(), VGroup()
        for j, x in enumerate((-2.69, 2.69)):
            borders.add(RoundedRectangle(corner_radius=0.09, width=4.79, height=1.03,
                                         stroke_width=2.6, stroke_color=GREY)
                        .move_to(pt(x, y - 0.13)))
            pair.add(grass(np.linspace(x - 1.89, x + 1.89, (10 if j == 0 else 8) if row == 0 else 9),
                           lambda _: y - 0.41, height=0.70 if row == 0 and j == 0 else 0.57,
                           seed=8 + row + j))
        outlines.add(borders)
        stands.add(pair)
    return bands, outlines, stands


def assignment_style(outlines):
    for borders, treated in zip(outlines, ASSIGNMENT):
        borders[treated].set_stroke(TEAL, 4)
        borders[1 - treated].set_stroke(GREY, 3)


def roof(x, ground=-1.25, width=3.52, height=2.60, pitch=1, pane_depth=0.12):
    a, b = x - width / 2, x + width / 2
    y = ground + height
    left, right = (a - 0.12, y + 0.43 * pitch), (b + 0.12, y - 0.17 * pitch)
    posts = VGroup(segment((a + 0.18, ground), (a + 0.18, y + 0.38 * pitch), width=4),
                   segment((b - 0.18, ground), (b - 0.18, y - 0.12 * pitch), width=4))
    pane = shape([left, right, (right[0], right[1] + pane_depth), (left[0], left[1] + pane_depth + 0.01)],
                 "#A4CAD2", opacity=0.55, stroke="#A4CAD2")
    return VGroup(posts, pane)


def sheltered(open_plot=False):
    bases, stands, roofs = VGroup(), VGroup(), VGroup()
    for i, x in enumerate(SHELTER_X[:3 if open_plot else 2]):
        bases.add(soil_tile(x, -1.24, 3.72, 1.28))
        stands.add(grass(np.linspace(x - 1.58, x + 1.58, 11), lambda _: -1.24, 1.08, seed=11))
        if i < 2:
            roofs.add(roof(x))
    return bases, stands, roofs


def cage(x, y, width=3.50, height=3.05):
    l, r = x - width / 2, x + width / 2
    top = y + height
    net = VGroup(*(segment((u, y), (u, top), "#697A79", 1.2)
                   for u in np.linspace(l, r, 11)[1:-1]),
                 *(segment((l, v), (r, v), "#697A79", 1.2)
                   for v in np.linspace(y, top, 11)[1:-1]))
    frame = Rectangle(width=width, height=height, stroke_color=GREY, stroke_width=3,
                      fill_color=GREY, fill_opacity=0.075).move_to(pt(x, y + height / 2))
    return VGroup(frame, net)


def drops(x, width, bottom, top, count=18, mode="fall", speed=1.6, seed=8):
    rng = np.random.default_rng(seed)
    xs = rng.uniform(x - width / 2, x + width / 2, count)
    offsets = rng.uniform(0, 1, count)
    streaks = VGroup(*(segment((u, top), (u + 0.05, top + 0.13), BLUE, 3) for u in xs))
    clock = 0.0

    def flow(group, dt):
        nonlocal clock
        clock += dt
        for line, u, offset in zip(group, xs, offsets):
            floor = bottom - (u - x) * 0.16 if mode == "roof" else bottom
            travel = (offset + clock * speed / (top - floor)) % 1
            y = top - min(travel / 0.86, 1) * (top - floor) if mode == "roof" else top - travel * (top - floor)
            side = max(0, travel - 0.86) if mode == "roof" else 0
            line.put_start_and_end_on(pt(u + side, y + side * 1.4),
                                      pt(u + side + (0.12 if side else 0.04), y + 0.12 + side * 1.6))
            if mode in ("gentle", "burst"):
                line.set_stroke(opacity=1 if clock % (1.12 if mode == "gentle" else 3.36) <
                                (0.54 if mode == "gentle" else 0.73) else 0)
    flow(streaks, 0)
    return streaks.add_updater(flow)


def sun(x, y, radius=0.32):
    return VGroup(Dot(pt(x, y), radius=radius, color=YELLOW),
                  *(segment((x + 1.25 * radius * np.cos(a), y + 1.25 * radius * np.sin(a)),
                            (x + 1.70 * radius * np.cos(a), y + 1.70 * radius * np.sin(a)), YELLOW, 3)
                    for a in np.arange(8) * TAU / 8))


def dated_years(x, y):
    year = ValueTracker(1)
    return year, counter("Year {:.0f} / 4", year, at=pt(x, y), size=30, color=GOLD)


def spider(x, y, scale=1, sealed=False, face_left=False):
    body = VGroup(Ellipse(width=0.65, height=0.39, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
                  .move_to(pt(x - 0.18, y)),
                  Dot(pt(x + 0.16, y), radius=0.15, color=PURPLE))
    legs = VGroup()
    for i in range(4):
        b = x - 0.26 + 0.14 * i
        for s in (-1, 1):
            legs.add(segment((b, y), (b + 0.12, y + s * (0.22 + i * 0.025)), PURPLE, 3),
                     segment((b + 0.12, y + s * (0.22 + i * 0.025)),
                             (b - 0.12 + i * 0.10, y + s * 0.36), PURPLE, 3))
    marker = Dot(pt(x + 0.28, y), radius=0.085, color=RED)
    center = pt(x, y)
    animal = VGroup(legs, body, *([marker] if sealed else [])).scale(scale, about_point=center)
    if face_left:
        animal.stretch(-1, 0, about_point=center)
    return animal


def hopper(x, y):
    body = shape([(x - 0.47, y + 0.02), (x - 0.29, y + 0.18), (x + 0.25, y + 0.22),
                  (x + 0.36, y + 0.10), (x + 0.08, y)], "#B4D76F")
    return VGroup(body, Dot(pt(x + 0.31, y + 0.16), radius=0.095, color=GREEN),
                  segment((x + 0.33, y + 0.22), (x + 0.49, y + 0.38), GREEN, 2),
                  segment((x + 0.02, y + 0.10), (x - 0.22, y - 0.17), GREEN, 4),
                  segment((x - 0.22, y - 0.17), (x + 0.13, y - 0.18), GREEN, 3))


def arm_wind(stands):
    for i, blades in enumerate(stands):
        wind(blades, phase=i * 0.37)


class S01Hook(SpokenScene):
    def construct(self):
        left, lush = hillside(-6.36, -0.25)
        right, sparse = hillside(0.25, 6.36, sparse=True)
        self.add(left, right, wind(lush), wind(sparse, phase=0.9), schematic())
        self.at("why")
        mark = T("?", 100, GOLD, weight=BOLD).move_to(pt(0, 1.97))
        self.play(FadeIn(mark, shift=UP * 0.46), run_time=0.65)
        self.at("in soil")
        self.play(FadeOut(mark), run_time=0.28)
        xs = [-3.93, -1.31, 1.31, 3.93]
        layers = VGroup(*(RoundedRectangle(width=1.53, height=0.22, corner_radius=0.065,
                                          fill_color=c, fill_opacity=1, stroke_width=0)
                          for c in ("#A79B6B", "#7F865C", "#546A54"))).arrange(DOWN, buff=0.03)
        incline = shape([(-0.79, -0.41), (0.79, -0.41), (0.79, 0.48)], TEAL, 0.33, TEAL)
        rain = VGroup(*(segment((u, v), (u + 0.12, v + 0.27), BLUE, 4)
                        for u, v in zip(np.linspace(-0.56, 0.50, 6), (0.15, -0.30, 0.26, -0.17, 0.16, -0.28))))
        history = VGroup(segment((-0.8, 0), (0.80, 0), GOLD, 4),
                         *(Dot(pt(u, 0), radius=0.085, color=GOLD) for u in (-0.64, -0.04, 0.62)))
        icons = VGroup(layers, incline, rain, history)
        for i, (cue, word) in enumerate(zip(("in soil", "slope", "rain and history", "and history"),
                                            ("Soil", "Slope", "Rain", "History"))):
            if i:
                self.at(cue, lead=0.27)
            icon = icons[i].move_to(pt(xs[i], 2.21))
            self.play(FadeIn(icon, shift=UP * 0.13),
                      FadeIn(label(word, xs[i], 3.08, size=30)), run_time=0.29)
        self.at("watching nature alone")
        threads = VGroup()
        for i, x in enumerate(xs):
            curve = CubicBezier(pt(x, 1.69), pt(-x * 0.78, 1.09), pt(x * 0.5, 0.35), pt(-x * 0.66, -0.16))
            threads.add(curve.set_stroke((GREEN, TEAL, BLUE, GOLD)[i], 5))
        self.play(LaggedStart(*(Create(t) for t in threads), lag_ratio=0.22), run_time=2.8)
        self.at("field manipulation experiment")
        single, blades = hillside()
        lush.clear_updaters()
        sparse.clear_updaters()
        old = Group(*[m for m in self.mobjects if m not in (left, lush)])
        self.play(FadeOut(old), Transform(left, single), FadeOut(lush), FadeIn(blades), run_time=1.5)
        self.add(wind(blades), schematic())
        self.finish()


class S02Title(TitleCard):
    TITLE = "Testing Ecological Cause in the Field"
    LESSON = "Field Manipulation Experiments"

    def construct(self):
        ground, stems = hillside()
        self.add(ground, wind(stems))
        title = label(self.TITLE, y=2.64, size=51)
        title.set_z_index(2)
        self.play(FadeIn(title, shift=UP * 0.10), run_time=0.46)
        stems.clear_updaters()
        self.play(VGroup(ground, stems).animate.scale(TITLE_ZOOM, about_point=ORIGIN),
                  run_time=0.94)
        wind(stems)
        self.play(FadeOut(title), run_time=0.55)


class S03BlocksAndRandom(SpokenScene):
    def construct(self):
        hill, stems = hillside(zoom=TITLE_ZOOM)
        self.add(hill, wind(stems), schematic())
        bands, boxes, stands = block_field()
        self.at("divide the slope")
        self.play(FadeOut(hill), FadeOut(stems),
                  LaggedStart(*(FadeIn(band, shift=UP * 0.22) for band in bands), lag_ratio=0.36),
                  run_time=1.67)
        ident = label("Matched blocks")
        self.play(FadeIn(ident), run_time=0.44)
        self.at("mark equal plots")
        even = label("Equal plots")
        self.play(swap(ident, even), LaggedStart(*(Create(b) for b in boxes), lag_ratio=0.18),
                  FadeIn(stands), run_time=0.95)
        arm_wind([stand for pair in stands for stand in pair])
        self.at("flip a coin")
        coins = VGroup(*[Circle(radius=0.25, stroke_color=GOLD, stroke_width=4, fill_color=GOLD,
                                  fill_opacity=0.28).move_to(pt(0, y - 0.15)) for y in BLOCK_Y])
        self.play(FadeIn(coins), run_time=0.26)
        self.play(LaggedStart(*(Rotate(c, TAU, axis=UP, about_point=c.get_center()) for c in coins),
                              lag_ratio=0.19), run_time=1.18)
        self.at("plots receive the treatment")
        self.play(FadeOut(coins), *(b[j].animate.set_stroke(TEAL, 4) for b, j in zip(boxes, ASSIGNMENT)),
                  run_time=0.72)
        treatment = label("Treatment", -1.38, color=TEAL)
        control = label("Controls", 1.75, color=TEXT)
        # Heading key uses matching border samples because assignment changes sides by block.
        key = VGroup(segment((-3.18, 2.76), (-2.68, 2.76), TEAL, 5),
                     segment((0.14, 2.76), (0.64, 2.76), GREY, 5))
        self.play(FadeOut(even), run_time=0.28)
        self.play(FadeIn(treatment), FadeIn(key[0]), run_time=0.35)
        self.at("serve as controls")
        self.play(FadeIn(control), FadeIn(key[1]), run_time=0.42)
        self.at("choosing by eye")
        pointer = shape([(-5.6, 2.18), (-5.05, 1.48), (-5.62, 1.66), (-5.82, 1.35)],
                        TEXT, 0.64, TEXT)
        slash = segment((-5.94, 1.40), (-4.92, 2.26), RED, 7)
        self.play(FadeIn(pointer, shift=RIGHT * 0.32 + DOWN * 0.28), run_time=0.84)
        self.play(Create(slash), run_time=0.48)
        self.at("random assignment")
        self.play(FadeOut(pointer), FadeOut(slash), run_time=0.42)
        marks = VGroup()
        for row, y in enumerate(BLOCK_Y):
            for column, x in enumerate((-2.69, 2.69)):
                for i in range(6):
                    marks.add(Dot(pt(x - 1.77 + i * 0.7, y - 0.55 - 0.09 * ((i + row + column) % 2)),
                                  radius=0.045, color="#A5A78B"))
        self.play(LaggedStart(*(FadeIn(d, shift=DOWN * 0.12) for d in marks), lag_ratio=0.05), run_time=2.1)
        self.play(FadeOut(marks), FadeOut(treatment), FadeOut(control), FadeOut(key), run_time=0.68)
        self.finish()


class S04ThreeMoves(SpokenScene):
    def construct(self):
        bands, boxes, stands = block_field()
        assignment_style(boxes)
        self.add(bands, boxes, stands, schematic())
        arm_wind([stand for pair in stands for stand in pair])
        border = [pair[1 - i] for pair, i in zip(boxes, ASSIGNMENT)]
        self.at("plot area alike")
        self.play(*(b.animate.set_stroke(TEXT, 3.2) for b in border), run_time=0.68)
        extra = VGroup(*(flower(x, BLOCK_Y[0] - 0.41) for x in (-4.12, -2.88, -1.44)))
        self.play(FadeIn(extra), run_time=0.65)
        self.at("remove a species", lead=0.4)
        name = label("Removal", color=PURPLE)
        self.play(FadeOut(extra, shift=UP * 0.65, run_time=0.88), FadeIn(name, run_time=0.34))
        self.at("add a resource")
        shower = drops(2.69, 3.75, BLOCK_Y[1] - 0.38, BLOCK_Y[1] + 0.65, count=9, speed=1.1)
        addition = label("Addition", color=BLUE)
        self.play(FadeIn(shower), swap(name, addition), run_time=0.56)
        self.at("or light")
        rays = VGroup(*(segment((x, 0.58), (x + 0.26, 0.04), YELLOW, 4) for x in (1.63, 2.46, 3.29)))
        self.play(FadeOut(shower), Create(rays), run_time=0.58)
        self.at("build an exclosure")
        mesh = cage(-2.69, -2.22, 4.24, 0.86)
        self.play(FadeOut(rays), FadeIn(mesh, shift=DOWN * 0.40), run_time=0.70)
        exclosure = label("Exclosure")
        self.play(swap(addition, exclosure), run_time=0.49)
        self.at("cage or shelter")
        cover = roof(-2.69, -2.22, 4.11, height=0.68, pitch=0.05, pane_depth=0.025)
        self.play(FadeOut(mesh), FadeIn(cover), run_time=0.96)
        self.at("test cause in nature")
        rule = label("Change one factor", color=TEAL)
        self.play(swap(exclosure, rule), run_time=0.67)
        self.at("while matched controls")
        self.play(*(Indicate(b, color=TEXT, scale_factor=1.035) for b in border), run_time=1.49)
        self.finish()


class S05PredictQuestion(SpokenScene):
    def construct(self):
        bands, boxes, stands = block_field()
        assignment_style(boxes)
        self.add(bands, boxes, stands, schematic())
        bases, plants, shelters = sheltered()
        self.at("picture rainout shelters")
        self.play(FadeOut(VGroup(bands, boxes, stands)), FadeIn(VGroup(bases, plants)), run_time=0.86)
        arm_wind(plants)
        self.play(LaggedStart(*(FadeIn(r, shift=DOWN * 0.50) for r in shelters), lag_ratio=0.35),
                  run_time=1.33)
        self.at("roofs block natural rain")
        outer = VGroup(*(drops(x, 3.35, 1.52, 2.72, mode="roof", speed=1.15) for x in SHELTER_X[:2]))
        self.play(FadeIn(outer), run_time=0.64)
        self.at("irrigation then returns")
        nozzles = VGroup()
        for x in SHELTER_X[:2]:
            bar = segment((x - 1.58, 0.82), (x + 1.58, 0.82), BLUE, 5)
            tips = VGroup(*(segment((x + dx, 0.82), (x + dx, 0.70), BLUE, 3)
                            for dx in (-1.10, -0.55, 0, 0.55, 1.10)))
            nozzles.add(VGroup(bar, tips))
        self.play(FadeOut(outer), Create(nozzles), run_time=0.68)
        same = label("Same total water", x=-2.04, color=BLUE)
        self.at("the same total")
        self.play(FadeIn(same), run_time=0.45)
        self.at("natural pattern")
        gentle = drops(SHELTER_X[0], 2.26, -0.71, 0.70, count=14, speed=1.3, mode="gentle")
        self.add(gentle)
        left = label("Natural timing", SHELTER_X[0], -2.89, size=30)
        self.play(FadeIn(left), run_time=0.40)
        self.at("fewer larger storms")
        bursts = drops(SHELTER_X[1], 2.62, -0.72, 0.71, count=30, speed=2.5, mode="burst")
        self.add(bursts)
        right = label("Fewer, larger storms", SHELTER_X[1], -2.89, size=30)
        self.play(FadeIn(right), run_time=0.41)
        self.at("each roof stays")
        solar = sun(3.68, 0.14, 0.36)
        arc = CubicBezier(pt(3.68, 0.14), pt(3.85, 2.63), pt(5.65, 2.69), pt(6.22, 0.61))
        self.remove(gentle, bursts)
        self.play(FadeOut(nozzles), FadeOut(same), FadeOut(left), FadeOut(right), FadeIn(solar), run_time=0.54)
        self.play(MoveAlongPath(solar, arc), run_time=2.28)
        self.play(FadeOut(solar), run_time=0.33)
        self.at("what side effect")
        self.play(FadeIn(question_card(QUESTION, **QUESTION_STYLE)), run_time=0.55)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5

    def construct(self):
        bases, stands, roofs = sheltered()
        self.add(bases, stands, roofs, schematic(), question_card(self.QUESTION, **self.CARD))
        self.wait(self.SECONDS, frozen_frame=True)


def moisture_curve(altered):
    """Schematic trace constrained by Knapp et al. (2002), Fig. 1A–B.

    Both schedules deliver one normalized unit of rain. The response uses
    first-order drainage. Centre and scale each record using the reported mean
    and the estimated mean consecutive difference in the 2000 season.
    """
    n = 8 if altered else 28
    intervals = np.linspace(0.02, 0.95, n) + 0.012 * np.sin(np.arange(n) * 2.4)

    def response(t):
        return sum(np.exp(-(t - rain) / 0.081) / n for rain in intervals if t >= rain)

    sample = np.array([response(t) for t in np.linspace(0, 0.98, 20)])
    mean, variability = (27.1, 9.0) if altered else (29.5, 4.0)
    gain = variability / np.abs(np.diff(sample)).mean()
    return lambda t: mean + gain * (response(t) - sample.mean())


def moisture_pair():
    plots, curves, heads = VGroup(), VGroup(), VGroup()
    for i, x in enumerate(SHELTER_X[:2]):
        plot = Plot((x - 1.72, x + 1.73, -2.69, -1.61),
                    (0, 1), (0, 61), stroke=2.5)
        plots.add(plot)
        curves.add(plot.curve(moisture_curve(i == 1), color=BLUE, width=4, n=350))
        heads.add(label(("Natural timing", "Fewer, larger storms")[i], x, -3.10, size=28, max_w=3.85))
    return plots, curves, heads


class S07Controls(SpokenScene):
    def construct(self):
        bases, stands, roofs = sheltered(open_plot=True)
        self.add(bases[0], bases[1], stands[0], stands[1], roofs, schematic())
        arm_wind(stands)
        self.at("cast shade")
        shadows = VGroup(*(shape([(x - 1.55, -1.23), (x + 1.55, -1.23),
                                  (x + 1.55, 0.11), (x - 1.40, 0.58)], "#304353", 0.39)
                           for x in SHELTER_X[:2]))
        for shade in shadows:
            shade.set_z_index(1)
        shade_label = label("Possible shade and warming", -2.04, color=YELLOW)
        self.play(FadeIn(shadows), run_time=0.75)
        self.at("warm the air")
        shimmer = VGroup()
        for site in SHELTER_X[:2]:
            for i, dx in enumerate((-0.82, 0, 0.79)):
                x = site + dx
                stroke = CubicBezier(pt(x, -0.36), pt(x - 0.46, 0.12),
                                     pt(x + 0.34, 0.47), pt(x, 0.94)).set_stroke(ORANGE, 3)
                shimmer.add(bob(stroke, amp=0.14, speed=3.2, seed=i).set_z_index(2))
        self.play(FadeIn(shimmer), FadeIn(shade_label), run_time=0.55)
        self.at("add unsheltered plots")
        self.play(FadeIn(bases[2], shift=LEFT * 0.38), FadeIn(stands[2], shift=LEFT * 0.38), run_time=0.84)
        open_tag = label("No roof", SHELTER_X[2], 0.92, size=30)
        self.play(FadeIn(open_tag), run_time=0.48)
        self.at("whether the roof itself")
        self.play(FadeOut(shimmer), FadeOut(shadows), run_time=0.80)
        self.at("log soil moisture")
        plots, curves, heads = moisture_pair()
        moisture = label("Soil moisture over time", -2.04, color=BLUE)
        self.play(swap(shade_label, moisture), FadeIn(plots), FadeIn(heads), run_time=0.62)
        self.play(LaggedStart(*(Create(c) for c in curves), lag_ratio=0.28), run_time=3.0)
        self.at("cage exclosures")
        self.play(FadeOut(open_tag), run_time=0.38)
        net = cage(SHELTER_X[2], -1.25, 3.50, 2.66)
        self.play(FadeIn(net, shift=DOWN * 0.25), run_time=0.73)
        self.at("report how well")
        bug = spider(6.44, -0.26, 0.56)
        self.play(FadeIn(bug), run_time=0.25)
        self.play(bug.animate.move_to(pt(6.20, -0.08)), run_time=0.82)
        test = label("Predator check", SHELTER_X[2], 2.30, color=PURPLE, size=30, max_w=3.55)
        self.play(FadeIn(test), net[1].animate.set_stroke(TEXT, 1.6), run_time=0.57)
        self.play(bug.animate.shift(UP * 0.42), run_time=0.88)
        self.finish()


def weather(x, y):
    bright = sun(x + 0.50, y + 0.19, 0.37)
    cloud = VGroup(
        RoundedRectangle(width=1.43, height=0.50, corner_radius=0.25,
                         fill_color=GREY, fill_opacity=1, stroke_width=0).move_to(pt(x - 0.18, y - 0.09)),
        Dot(pt(x - 0.31, y + 0.06), radius=0.34, color=GREY),
        Dot(pt(x + 0.10, y), radius=0.24, color=GREY),
    )
    return bright, cloud


def shore():
    water = shape([(1.03, -0.93), (6.32, -0.93), (6.32, -2.52), (1.03, -2.52)], "#356071")
    stones = VGroup()
    for i, (x, y, s) in enumerate(((1.58, -1.27, 1.01), (2.58, -1.71, 0.64), (3.15, -2.14, 0.52),
                                   (2.44, -2.30, 0.83), (1.45, -2.33, 0.76), (3.89, -2.27, 0.45))):
        stones.add(shape([(x - s, y - 0.14), (x - s * 0.39, y + s * 0.44),
                          (x + s * 0.40, y + s * 0.51), (x + s * 0.81, y - 0.12),
                          (x + s * 0.18, y - 0.22)], ("#77858B", "#5D6D75")[i % 2]))
    ripples = VGroup(*(segment((x, y), (x + 0.93, y), BLUE, 2)
                       for x, y in ((3.26, -1.23), (4.86, -1.13), (4.69, -1.69), (5.02, -2.18))))
    bob(ripples, amp=0.08, speed=2)
    return VGroup(water, stones, ripples)


class S08Limits(SpokenScene):
    def construct(self):
        bands, boxes, stands = block_field()
        assignment_style(boxes)
        focus = VGroup(bands[0], boxes[0], stands[0])
        focus.save_state()
        pivot = pt(0, 1.35)
        focus.stretch(2.40, 1, about_point=pivot)
        self.add(focus, schematic())
        self.play(focus.animate.stretch(0.92, 1, about_point=pivot), run_time=2.82)
        for i, blades in enumerate(stands[0]):
            wind(blades, phase=i * 0.37, strength=0.31)
        self.at("only one treated block")
        first = label("One block", color=TEAL)
        self.play(FadeIn(first), run_time=0.51)
        self.at("chance differences")
        doubt = T("?", 76, GOLD).move_to(pt(0, -2.31))
        self.play(FadeIn(doubt, shift=UP * 0.13), run_time=0.72)
        self.at("treatments must be replicated", lead=0.50)
        for blades in stands[0]:
            blades.clear_updaters()
        self.play(FadeOut(doubt), Restore(focus), run_time=0.84)
        self.play(LaggedStart(*(FadeIn(VGroup(bands[i], boxes[i], stands[i]), shift=DOWN * 0.33)
                                for i in (1, 2)), lag_ratio=0.29), run_time=1.03)
        arm_wind(stands[0])
        arm_wind([stand for pair in stands[1:] for stand in pair])
        replicated = label("Replicate blocks", color=TEAL)
        self.play(swap(first, replicated), run_time=0.56)
        self.at("one unusual year")
        year, year_tag = dated_years(-4.42, 2.85)
        solar, cloud = weather(0, 2.74)
        self.play(FadeOut(replicated), run_time=0.33)
        self.play(FadeIn(year_tag), FadeIn(cloud, shift=RIGHT * 0.35), run_time=0.54)
        self.at("tracked for several years")
        self.play(year.animate.set_value(2), FadeIn(solar), cloud.animate.shift(LEFT * 0.76), run_time=0.78)
        rain = drops(-0.8, 1.30, 1.95, 2.45, count=10)
        self.play(year.animate.set_value(3), FadeIn(rain), run_time=0.76)
        self.play(year.animate.set_value(4), FadeOut(cloud), FadeOut(rain), run_time=0.87)
        self.at("field result applies")
        local, plants = hillside(-6.36, -0.49)
        self.play(FadeOut(VGroup(bands, boxes, stands, year_tag, solar)), FadeIn(VGroup(local, plants)),
                  run_time=0.90)
        wind(plants)
        one = label("This site", -3.47, 2.46, color=TEAL)
        self.play(FadeIn(one), run_time=0.41)
        self.at("another grassland")
        other, other_plants = hillside(0.65, 6.36, sparse=True)
        beach = shore()
        self.play(FadeIn(VGroup(other, other_plants)), run_time=0.64)
        wind(other_plants)
        self.at("or shore", lead=0.3)
        self.play(FadeOut(VGroup(other, other_plants)), run_time=0.25)
        self.play(FadeIn(beach), run_time=0.36)
        ask = T("?", 78, GOLD).move_to(pt(3.46, 2.01))
        self.play(FadeIn(ask), run_time=0.42)
        self.finish()


def study_bed(x, ground=-1.47, width=2.40, height=1.13, seed=2):
    base = soil_tile(x, ground, width, 0.80)
    plants = grass(np.linspace(x - width * 0.41, x + width * 0.41, 10),
                   lambda _: ground, height, seed=seed)
    return base, plants


def study_variation():
    plot = Plot((-5.81, -0.65, -0.20, 1.19), (0, 1), (0, 61), stroke=2.5)
    natural = plot.curve(moisture_curve(False), color="#A7CCD5", width=3, n=300)
    large = plot.curve(moisture_curve(True), color=BLUE, width=4, n=300)
    return plot, natural, large


class S09UnlockedGrassland(SpokenScene):
    def construct(self):
        panels = TwoPanel("Knapp and colleagues, 2002", "Hautier, Niklaus and Hector, 2009",
                          colors=(BLUE, YELLOW), top=2.94, bottom=-2.70, size=29)
        left_base, left_plants = study_bed(-3.30, width=5.25, height=1.10)
        pair = VGroup(roof(-4.64, width=2.26, ground=-1.47, height=2.59),
                      roof(-1.96, width=2.26, ground=-1.47, height=2.59))
        self.add(panels.left_frame, left_base, wind(left_plants), schematic())
        self.at("these designs unlocked")
        self.play(LaggedStart(*(FadeIn(r, shift=DOWN * 0.32) for r in pair),
                              lag_ratio=0.36), run_time=1.66)
        self.at("2002")
        self.play(FadeIn(panels.left_head), run_time=0.37)
        self.at("ran those shelters")
        storms = drops(-3.30, 4.88, 1.56, 1.76, count=18, speed=1.65)
        self.add(storms)
        year, digits = dated_years(-3.30, 2.06)
        self.play(FadeIn(digits), run_time=0.20)
        self.play(year.animate.set_value(4), run_time=0.80, rate_func=linear)
        self.at("in a grassland", lead=0)
        self.play(FadeOut(storms), FadeOut(pair), FadeOut(digits), run_time=0.42)
        plot, natural, larger = study_variation()
        baseline = label("Natural timing", -3.30, 1.57, size=28)
        self.play(FadeIn(plot), Create(natural), run_time=0.60)
        self.play(FadeIn(baseline), run_time=0.32)
        self.at("fewer larger events")
        self.play(FadeOut(natural), FadeOut(baseline), run_time=0.25)
        self.play(Create(larger), run_time=0.86)
        self.at("raised soil moisture variability")
        moisture = label("Wider soil moisture swings", -3.30, 1.57, color=BLUE, size=28)
        self.play(FadeIn(moisture), run_time=0.35)
        self.at("lowered plant growth")
        left_plants.clear_updaters()
        self.play(left_plants.animate.stretch(0.81, 1, about_point=pt(-3.30, -1.47)), run_time=0.81)
        wind(left_plants)
        self.at("raised species diversity")
        varieties = VGroup(flower(-4.98, -1.47, color=PURPLE), flower(-3.66, -1.47, height=0.60, kind=1, color=RED),
                           flower(-1.67, -1.47, height=0.54, kind=2, color=TEXT))
        self.play(LaggedStart(*(GrowFromEdge(m, DOWN) for m in varieties), lag_ratio=0.32), run_time=1.39)
        self.at("fertilized experimental grassland")
        comparison = (1.93, 4.67)
        beds = [study_bed(x, height=0.84, seed=3) for x in comparison]
        short = [VGroup(flower(x - 0.48, -1.47), flower(x + 0.56, -1.47, kind=1, color=RED))
                 for x in comparison]
        self.play(FadeIn(panels.right_frame), FadeIn(VGroup(*beds[0], short[0])), run_time=0.53)
        granules = VGroup(*(Dot(pt(comparison[0] + dx, 0.67 + 0.17 * (i % 3)),
                                radius=0.061, color=ORANGE)
                            for i, dx in enumerate(np.linspace(-0.88, 0.88, 12))))
        self.play(FadeIn(granules), run_time=0.23)
        self.play(FadeOut(granules, shift=DOWN * 1.94),
                  beds[0][1].animate.stretch(2.03, 1, about_point=pt(comparison[0], -1.47)),
                  run_time=0.74)
        wind(beds[0][1])
        self.at("communities lose species")
        self.play(FadeOut(short[0], shift=DOWN * 0.20), run_time=0.86)
        self.at("2009")
        self.play(FadeIn(panels.right_head), run_time=0.48)
        shaded = label("Fertilizer only", comparison[0], 1.13, size=28, max_w=2.5)
        self.play(FadeIn(shaded), run_time=0.45)
        self.at("added light")
        x = comparison[1]
        beds[1][1].stretch(2.03, 1, about_point=pt(x, -1.47))
        lamp = VGroup(segment((x + 0.82, -1.44), (x + 0.82, -0.38), GREY, 4),
                      shape([(x + 0.53, -0.30), (x + 0.83, -0.30), (x + 0.93, -0.47),
                             (x + 0.42, -0.47)], YELLOW))
        beam = shape([(x + 0.48, -0.47), (x + 0.86, -0.47), (x + 0.56, -1.41), (x - 1.07, -1.41)],
                     YELLOW, 0.25)
        # The beam sits behind the short flowers so the treatment remains visible.
        short[1].set_z_index(2)
        self.play(FadeIn(VGroup(*beds[1], short[1])), FadeIn(lamp), run_time=0.55)
        self.play(FadeIn(beam), run_time=0.40)
        wind(beds[1][1], phase=0.35)
        lit = label("Fertilizer + light", x, 1.13, color=YELLOW, size=28, max_w=2.8)
        self.play(FadeIn(lit), run_time=0.41)
        self.at("prevented the loss")
        self.play(beam.animate.set_fill(opacity=0.35), run_time=0.70)
        self.at("competition for light")
        self.play(beam.animate.set_fill(opacity=0.25), run_time=0.86)
        self.finish()


class S10UnlockedPredationClose(SpokenScene):
    def construct(self):
        plots, plants, nets, hoppers = VGroup(), VGroup(), VGroup(), VGroup()
        for i, x in enumerate(SHELTER_X):
            earth, grassland = study_bed(x, ground=-1.47, width=3.64, height=0.97, seed=i)
            plots.add(earth)
            plants.add(grassland)
            nets.add(cage(x, -1.47, 3.49, 3.55))
            hoppers.add(hopper(x - 0.39, -0.73))
        self.add(plots, plants, schematic())
        arm_wind(plants)
        credit = label("Beckerman, Uriarte and Schmitz, 1997", y=2.78, size=34, color=GOLD)
        self.at("1997")
        self.play(FadeIn(credit), run_time=0.57)
        self.play(LaggedStart(*(FadeIn(net, shift=DOWN * 0.22) for net in nets),
                              lag_ratio=0.23), run_time=1.28)
        self.at("tested grasshoppers")
        self.play(LaggedStart(*(FadeIn(b, shift=DOWN * 0.18) for b in hoppers), lag_ratio=0.26), run_time=1.38)
        for i, b in enumerate(hoppers):
            bob(b, amp=0.13, speed=2.3, seed=i)
        self.at("compared enclosures")
        self.play(*(net[0].animate.set_stroke(TEXT, opacity=0.84) for net in nets),
                  run_time=0.71)
        self.at("with no spiders")
        labels = [label(s, x, -2.87, color=TEXT if i == 0 else PURPLE, size=30, max_w=3.75)
                  for i, (s, x) in enumerate(zip(("No spiders", "Hunting spiders", "Glued mouthparts"), SHELTER_X))]
        self.play(FadeIn(labels[0]), run_time=0.42)
        self.at("hunting spiders")
        hunter = spider(0.83, 0.17, 1.12, face_left=True)
        self.play(FadeIn(hunter), run_time=0.42)
        self.play(FadeIn(labels[1]), hunter.animate.shift(LEFT * 0.20 + DOWN * 0.20), run_time=0.64)
        self.at("or spiders with")
        sealed = spider(4.92, 0.07, 1.12, sealed=True, face_left=True)
        self.play(FadeIn(sealed), run_time=0.50)
        self.at("glued mouthparts")
        self.play(FadeIn(labels[2]), run_time=0.52)
        self.at("any effect of glued spiders")
        self.play(sealed.animate.shift(LEFT * 0.22 + DOWN * 0.12), run_time=1.33)
        self.at("come from fear")
        fear = label("Fear", 4.08, -2.87, color=PURPLE)
        self.play(swap(labels[2], fear), run_time=0.60)
        self.at("by changing one factor")
        bands, boxes, stands = block_field()
        assignment_style(boxes)
        self.play(FadeOut(VGroup(fear, credit, *labels[:2])), run_time=0.28)
        self.play(FadeOut(VGroup(plots, plants, nets, hoppers, hunter, sealed)),
                  FadeIn(VGroup(bands, boxes, stands)), run_time=1.03)
        arm_wind([stand for pair in stands for stand in pair])
        self.at("beside matched controls")
        for b, j in zip(boxes, ASSIGNMENT):
            b[1 - j].set_stroke(TEXT, 3)
        self.play(LaggedStart(*(Indicate(b, color=TEAL, scale_factor=1.025) for pair in boxes for b in pair),
                              lag_ratio=0.17), run_time=2.3)
        self.at("testable causes")
        closing = label("A test of cause", color=TEAL)
        self.play(FadeIn(closing), run_time=0.52)
        self.finish()


class S11End(EndCard):
    LINE = "Randomly change one factor against matched controls to test ecological cause."
