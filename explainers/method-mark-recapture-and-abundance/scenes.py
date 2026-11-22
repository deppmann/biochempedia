"""A pond, two catches and the difference between missing and gone."""

from bp_parts import *  # noqa: F401,F403

# Patch-clamp palette: BLUE = apparatus, GREY = structure, TEAL = water,
# GOLD = dates and marks, GREEN = confirmed detections, RED = bias or loss.
WATER = "#226D76"
SHALLOWS = "#2B8790"
BANK = "#244B49"
REEDS = "#748B59"
ROCK = "#735047"
INK = "#B5EBE6"
FIELD = "#9E6D53"

FIRST, SECOND, OVERLAP = 50, 90, 20
ESTIMATE = FIRST * SECOND // OVERLAP
CHAPMAN = (FIRST + 1) * (SECOND + 1) // (OVERLAP + 1) - 1
FORMULA = "N = n₁ × n₂ ÷ m₂"
QUESTION = "Trap-shy marked animals: estimate too high or too low?"
LEFT_CENTER = np.array([-3.25, -0.15, 0.0])
RIGHT_X = 3.38


def p(x, y):
    return np.array([x, y, 0.0])


def label(words, x=RIGHT_X, y=0, size=32, color=TEXT):
    return T(words, size, color).move_to(p(x, y))


def equation(words, y=0, size=34, color=TEXT):
    return M(words, size, color).move_to(p(RIGHT_X, y))


def outline(points, color, fill=1, width=0):
    return Polygon(*(p(x, y) for x, y in points), color=color,
                   stroke_width=width, fill_color=color, fill_opacity=fill)


def fish(marked=False, spotted=False, color=INK, width=0.4):
    tail = outline([(-0.23, 0), (-0.48, 0.20), (-0.43, 0), (-0.48, -0.20)], color)
    body = Ellipse(width=0.82, height=0.37, stroke_width=0, fill_color=color, fill_opacity=1)
    mark = Dot(p(-0.10, 0), radius=0.135, color=GOLD).set_opacity(int(marked))
    animal = VGroup(tail, body)
    if width >= 0.26:
        animal.add(Dot(p(0.27, 0.045), radius=0.035, color=WATER))
    if spotted:
        animal.add(*[Dot(p(x, y), radius=0.049, color=WATER)
                     for x, y in [(-0.25, -0.01), (-0.15, 0.08), (0.02, -0.08), (0.10, 0.08)]])
    animal.add(mark).set_width(width)
    animal.mark = mark
    return animal


def shore(cx=LEFT_CENTER[0], cy=LEFT_CENTER[1], width=6.75, height=5.44):
    def contour(rx, ry, offset=0):
        a = np.linspace(0, TAU, 80, endpoint=False)
        return [(cx + rx * np.cos(t) * (1 + 0.07 * np.sin(3 * t + offset)),
                 cy + ry * np.sin(t) * (1 + 0.06 * np.cos(5 * t))) for t in a]

    bank = outline(contour(width / 2, height / 2), BANK)
    shallow = outline(contour(width * 0.468, height * 0.466), SHALLOWS)
    water = outline(contour(width * 0.417, height * 0.407), WATER)
    return VGroup(bank, shallow, water)


def water_light(surface, phase=0, speed=2.06):
    dark = ManimColor(WATER)
    bright = ManimColor("#378993")
    clock = 0.0

    def shimmer(mob, dt):
        nonlocal clock
        clock += dt
        amount = 0.5 - 0.5 * np.cos(speed * clock + phase)
        mob.set_fill(interpolate_color(dark, bright, amount))

    surface.add_updater(shimmer)


def ripples(center=LEFT_CENTER, scale=1, animate=True):
    g = VGroup()
    rng = np.random.default_rng(7)
    for i in range(13):
        x, y = rng.uniform(-1.7, 1.7), rng.uniform(-1.67, 1.67)
        ends = (p(x - 0.38, y) * scale + center, p(x + 0.38, y) * scale + center)
        arc = ArcBetweenPoints(*ends, angle=0.22, color=INK, stroke_width=2.7)
        arc.set_stroke(opacity=0.48)
        if animate:
            bob(arc, amp=0.17 * scale, speed=1.4, seed=i)
        g.add(arc)
    return g


def reed_patch(x, y, width, height):
    base = Ellipse(width=width, height=height, stroke_width=0, fill_color=BANK, fill_opacity=1)
    reeds = VGroup(base.move_to(p(x, y)))
    for i in range(14):
        a = i * 2.4
        pos = p(x + 0.38 * width * np.cos(a), y + 0.37 * height * np.sin(a))
        reed = Ellipse(width=0.10, height=0.44, stroke_width=0,
                       fill_color=REEDS if i % 3 else "#A3A46D", fill_opacity=1)
        reeds.add(reed.rotate(0.48 * np.sin(a)).move_to(pos))
    return reeds


def pond(closed=False, cover=True, animate=True, light_speed=2.06):
    ground = shore()
    water_motion = ripples(animate=animate)
    if animate:
        water_light(ground[-1], speed=light_speed)
    reeds = VGroup(reed_patch(-4.88, 1.16, 1.55, 0.92),
                   reed_patch(-2.22, 0.69, 1.62, 1.20),
                   reed_patch(-3.48, -1.2, 2.06, 1.26)) if cover else VGroup()
    reeds.set_z_index(3)
    boundary = ground[0].copy().set_fill(opacity=0).set_stroke(TEAL, 3.5)
    picture = VGroup(ground, water_motion)
    if closed:
        picture.add(boundary)
    return picture, reeds, boundary


def school(count, marked=0, width=0.19, animate=True):
    animals = VGroup()
    # Equal-area spiral gives a repeatable position for every individual.
    for i, slot in enumerate(np.random.default_rng(11).permutation(count)):
        r, a = np.sqrt((slot + 0.5) / count), slot * PI * (3 - np.sqrt(5))
        pos = LEFT_CENTER + p(2.68 * r * np.cos(a), 2.04 * r * np.sin(a))
        animal = fish(i < marked, width=width).rotate(PI if i % 3 == 0 else 0).move_to(pos)
        if animate:
            swim(animal, i)
        animals.add(animal)
    return animals


def swim(animal, phase=0):
    center = animal.get_center().copy()
    clock = 0.0

    def drift(mob, dt):
        nonlocal clock
        clock += dt
        mob.move_to(center + p(0.25 * (np.sin(1.38 * clock + phase) - np.sin(phase)),
                               0.10 * (np.sin(2.10 * clock + phase) - np.sin(phase))))
    animal.add_updater(drift)


def catch_slots(count, center, rx, ry):
    for i in range(count):
        r, theta = np.sqrt((i + 0.5) / count), i * PI * (3 - np.sqrt(5))
        yield center + p(rx * r * np.cos(theta), ry * r * np.sin(theta))


def second_catch(animals):
    inside = list(animals[:OVERLAP]) + list(animals[FIRST:FIRST + SECOND - OVERLAP])
    outside = list(animals[OVERLAP:FIRST]) + list(animals[FIRST + SECOND - OVERLAP:])
    # Interleave the marked fish throughout the second catch.
    np.random.default_rng(21).shuffle(inside)
    slots = list(zip(inside, catch_slots(len(inside), LEFT_CENTER, 2.04, 1.57)))
    for i, animal in enumerate(outside):
        a = TAU * (i + 0.5) / len(outside)
        slots.append((animal, LEFT_CENTER + p(2.75 * np.cos(a), 2.15 * np.sin(a))))
    ring = Ellipse(width=4.75, height=3.75, stroke_color=BLUE, stroke_width=4)
    ring.move_to(LEFT_CENTER)
    return slots, ring


def sweep_net(at, radius=1.24):
    hoop = Ellipse(width=radius * 2, height=radius * 1.53, color=BLUE, stroke_width=5)
    wire = VGroup(*[Line(p(-0.84, v), p(0.84, v), color=BLUE, stroke_width=1.5)
                    for v in [-0.30, -0.15, 0, 0.15, 0.30]]).set_opacity(0.45)
    handle = Line(p(-radius + 0.02, -0.08), p(-radius - 0.66, -0.60), color=BLUE, stroke_width=8)
    g = VGroup(hoop, wire, handle)
    g.hoop = hoop
    return g.shift(at)


def strip(ratio, x=RIGHT_X, y=0, width=5.3, height=0.52, color=GOLD):
    frame = RoundedRectangle(corner_radius=0.09, width=width, height=height,
                             stroke_color=GREY, stroke_width=2.5,
                             fill_color=TEAL, fill_opacity=0.24).move_to(p(x, y))
    fill = Rectangle(width=(width - 0.13) * ratio, height=height - 0.12,
                     stroke_width=0, fill_color=color, fill_opacity=1)
    fill.move_to(frame.get_left() + RIGHT * (0.065 + fill.width / 2))
    return VGroup(frame, fill)


def ratio_board():
    return VGroup(label("Second catch", y=2.21, size=29),
                  equation("20 ÷ 90", 1.67, 38, GOLD),
                  strip(OVERLAP / SECOND, y=1.13),
                  label("Whole pond", y=0.18, size=29),
                  equation("50 ÷ N", -0.36, 38, GOLD),
                  strip(FIRST / ESTIMATE, y=-0.90))


def trap():
    cage = VGroup()
    for x in [-0.80, -0.48, -0.16, 0.16, 0.48, 0.80]:
        cage.add(Line(p(x, -0.80), p(x, 0.80), color=BLUE, stroke_width=2))
    for y in [-0.80, -0.40, 0, 0.40, 0.80]:
        cage.add(Line(p(-0.8, y), p(0.8, y), color=BLUE, stroke_width=2))
    cage.add(Rectangle(width=1.72, height=1.72, color=BLUE, stroke_width=4))
    cage.add(outline([(-0.84, -0.44), (-0.20, -0.17), (-0.20, 0.17), (-0.84, 0.44)],
                     BLUE, 0.26, 3))
    return cage.move_to(p(-2.20, -0.05))


def trap_animals(after=False, settled=False):
    gold_pos = [(-4.48, 0.82), (-4.16, -0.88), (-3.40, 1.42), (-3.63, -1.42), (-2.59, 1.17)]
    pale_pos = [(-3.70, -0.37), (-3.59, 0.44), (-4.3, 0.16)]
    if after:
        pale_pos = [(-2.50, -0.37), (-1.99, 0.44), (-2.12, 0.03)]
    if settled:
        gold_pos = [(-5.03, 0.62), (-4.68, -0.65), (-3.70, 1.56), (-3.28, -1.62), (-2.27, 1.51)]
    return VGroup(*[fish(i < len(gold_pos), width=0.58).move_to(p(*xy))
                    for i, xy in enumerate(gold_pos + pale_pos)])


def predict_card():
    return question_card(QUESTION, y=-3.35, size=32, left=-6.27, max_w=10.4)


def field_heading(place, date):
    return VGroup(label(place, -3.10, 3.13, 40), label(date, 3.35, 3.13, 28, GOLD))


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Mark-recapture and abundance surveys"
    TITLE = "Estimating Populations You Cannot All See"

    def construct(self):
        world, reeds, _ = pond()
        animals = school(44, width=0.37)
        self.add(world, animals, reeds, scope_tag())
        self.at("how do you")
        query = label("?", y=0.35, size=152, color=GOLD)
        self.play(FadeIn(query, shift=UP * 0.28), run_time=0.8)

        self.at("one visit misses")
        tracked = fish(marked=True, width=0.65).move_to(p(-3.68, 0.67))
        lost = VGroup(label("×", 2.65, 0.18, 72, RED),
                      label("→", 4.13, 0.18, 72, BLUE))
        self.play(FadeOut(query), FadeIn(tracked), run_time=0.42)
        self.play(tracked.animate.move_to(p(-2.09, 0.64)), run_time=1.25)
        self.play(GrowFromCenter(lost), run_time=0.45)

        self.at("may not be dead", lead=-0.18)
        title = fit_text(self.TITLE, max_w=5.95, size=43, min_size=34,
                         font=TITLE_FONT).move_to(p(RIGHT_X, 1.10))
        self.play(FadeOut(lost), FadeIn(title), run_time=0.4)
        self.at("repeated sightings", lead=0.35)
        self.play(FadeOut(title), run_time=0.28)
        for cue, word, y, color in [("estimate abundance", "Abundance", 1.41, TEAL),
                                     ("survival and", "Survival", 0.16, GREEN),
                                     ("occupancy", "Occupancy", -1.09, GOLD)]:
            self.at(cue)
            self.play(FadeIn(boxed_label(word, color, size=33).move_to(p(RIGHT_X, y))),
                      run_time=0.32)
        self.finish()


class S02MarkRecapture(SpokenScene):
    def construct(self):
        world, reeds, boundary = pond()
        animals = school(144, width=0.19)
        self.add(world, animals, reeds, scope_tag())
        self.at("closed pond", lead=0.65)
        self.play(Create(boundary), run_time=0.65)
        closed = label("Closed pond", y=2.27, size=42, color=TEAL)
        self.play(FadeIn(closed), run_time=0.35)

        self.at("catch and mark", lead=1.0)
        for a in animals:
            a.clear_updaters()
        original = [a.get_center().copy() for a in animals]
        first = list(animals[:FIRST])
        net = sweep_net(p(-4.94, -0.22))
        self.add(net.set_z_index(4))
        first_slots = catch_slots(len(first), p(-3.07, -0.22), 1.08, 0.77)
        others = list(animals[FIRST:])
        ordinary = VGroup(*[part for a in others for part in a if part is not a.mark])
        self.play(net.animate.shift(RIGHT * 1.86), reeds.animate.set_opacity(0.0),
                  ordinary.animate.set_opacity(0.13),
                  *[a.animate.move_to(spot) for a, spot in zip(first, first_slots)], run_time=0.75)
        self.at("mark 50")
        n1 = equation(f"n₁ = {FIRST}", 1.16, 40, GOLD)
        self.play(*[a.mark.animate.set_opacity(1) for a in first], FadeIn(n1), run_time=0.62)
        self.at("release them")
        self.play(FadeOut(net), ordinary.animate.set_opacity(1),
                  *[a.animate.move_to(xy) for a, xy in zip(first, original)], run_time=1.85)
        for i, a in enumerate(animals):
            swim(a, i)

        self.at("later catch", lead=0.28)
        for a in animals:
            a.clear_updaters()
        slots, ring = second_catch(animals)
        net2 = sweep_net(p(-4.8, -0.12))
        self.add(net2.set_z_index(4))
        self.play(net2.animate.shift(RIGHT * 1.7), Create(ring),
                  *[a.animate.move_to(spot) for a, spot in slots], run_time=0.80)
        n2 = equation(f"n₂ = {SECOND}", 0.17, 40, BLUE)
        self.play(FadeOut(net2), FadeIn(n2), run_time=0.31)
        self.at("20 already carry")
        m2 = equation(f"m₂ = {OVERLAP}", -0.82, 40, GOLD)
        self.play(FadeIn(m2), *[a.mark.animate.scale(1.40) for a in first[:OVERLAP]],
                  run_time=0.51)
        self.finish()


class S03Math(SpokenScene):
    def construct(self):
        world, _, _ = pond(closed=True, cover=False)
        animals = school(144, marked=FIRST, animate=False)
        slots, ring = second_catch(animals)
        for animal, spot in slots:
            animal.move_to(spot)
        for animal in animals[:OVERLAP]:
            animal.mark.scale(1.40)
        self.add(world, animals, ring, scope_tag())
        bars = ratio_board()
        self.at("the marked share of the second")
        self.play(FadeIn(VGroup(*bars[:2])), GrowFromEdge(bars[2], LEFT), run_time=0.90)
        self.at("the whole pond", lead=0.80)
        mixed = school(144, marked=FIRST, animate=False)
        self.play(FadeOut(ring), FadeIn(VGroup(*bars[3:5])), GrowFromEdge(bars[5], LEFT),
                  *[a.animate.move_to(b) for a, b in zip(animals, mixed)], run_time=1.05)
        for i, fish_glyph in enumerate(animals):
            swim(fish_glyph, i)
        equals = equation("≈", 0.66, 33, TEAL)
        self.play(FadeIn(equals), run_time=0.28)

        self.at("multiply first catch")
        product = equation("n₁ × n₂", 0.54, 52)
        self.play(FadeOut(VGroup(*bars, equals)), run_time=0.38)
        self.play(FadeIn(product), run_time=0.5)
        self.at("divide by marked")
        formula = equation(FORMULA, 0.54, 40)
        self.play(swap(product, formula), run_time=0.62)
        self.at("the lincoln", lead=0.25)
        method = label("Lincoln–Petersen", y=1.58, size=30, color=TEAL)
        self.play(FadeIn(method), run_time=0.42)

        self.at("50 times 90", lead=0.10)
        first_count = equation("50", -0.37, 35)
        self.play(FadeIn(first_count), run_time=0.21)
        self.at("90 is", lead=0.08)
        operands = equation("50 × 90", -0.37, 35)
        self.play(swap(first_count, operands), run_time=0.35)
        self.at("is 4", lead=-0.04)
        product = equation(f"50 × 90 = {FIRST * SECOND:,}", -0.37, 35)
        self.play(swap(operands, product), run_time=0.42)
        self.at("divided by 20")
        division = equation("4,500 ÷ 20", -1.20, 35)
        self.play(FadeIn(division), run_time=0.36)
        self.at("gives 225", lead=0.05)
        result = equation(f"4,500 ÷ 20 = {ESTIMATE}", -1.20, 36, GOLD)
        self.play(swap(division, result), FadeOut(animals), run_time=0.55)
        revealed = school(ESTIMATE, marked=FIRST, width=0.15)
        self.play(FadeIn(revealed), run_time=0.65)
        self.finish()


class S03bChapman(SpokenScene):
    def construct(self):
        world, _, _ = pond(closed=True, cover=False)
        self.add(world, school(ESTIMATE, marked=FIRST, width=0.15), scope_tag())
        plain = equation(f"{ESTIMATE}", 2.11, 43, TEXT).set_x(1.95)
        plain_heading = label("Plain", 1.95, 2.80, 28, TEAL)
        correction = label("Chapman", 4.77, 2.80, 28, TEAL)
        self.add(plain_heading, plain)
        self.at("runs high", lead=0.2)
        note = label("Small samples", y=0.75, color=RED)
        self.play(FadeIn(note), run_time=0.40)

        self.at("version adds one", lead=0.5)
        self.play(FadeOut(note), FadeIn(correction), run_time=0.36)
        counts = [ValueTracker(n) for n in (FIRST, SECOND, OVERLAP)]
        count_line = VGroup(*[counter(f"{name} = {{:.0f}}", n, p(x, 0.80), 29, color)
                              for name, n, x, color in zip(("n₁", "n₂", "m₂"), counts,
                                                          (1.49, 3.39, 5.30), (TEXT, BLUE, GOLD))])
        self.add(count_line)
        self.play(LaggedStart(*[n.animate.increment_value(1) for n in counts], lag_ratio=0.43),
                  run_time=1.20)

        self.at("51 times", lead=0.15)
        first_input = equation("51", -0.23, 34)
        self.play(FadeIn(first_input), run_time=0.23)
        self.at("91 over", lead=0.08)
        expr = equation("(51 × 91)", -0.23, 34)
        self.play(swap(first_input, expr), run_time=0.33)
        self.at("over 21")
        quot = equation("(51 × 91) ÷ 21", -0.23, 34)
        self.play(swap(expr, quot), run_time=0.40)
        self.at("minus 1")
        adjusted = equation("(51 × 91) ÷ 21 − 1", -0.23, 34)
        self.play(swap(quot, adjusted), run_time=0.43)
        self.at("gives 220")
        simpl = equation("= 4,641 ÷ 21 − 1", -1.14, 34)
        self.play(FadeIn(simpl), run_time=0.25)
        answer = equation(f"{CHAPMAN}", 2.11, 43, GOLD).set_x(4.77)
        self.play(FadeIn(answer), run_time=0.36)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world, _, _ = pond(closed=True, cover=False, light_speed=2.32)
        animals = trap_animals()
        cage = trap()
        formula = equation(FORMULA, 1.00, 40)
        self.add(world, animals, formula, scope_tag())
        self.at("marks stay readable")
        readable = label("Readable marks", y=-0.05, color=GOLD)
        self.play(FadeIn(readable), run_time=0.42)
        self.at("every animal is")
        fair = label("Equal catchability", y=-0.05)
        self.play(swap(readable, fair), run_time=0.56)
        self.at("suppose marked animals", lead=0.74)
        self.play(FadeOut(fair), FadeIn(cage, shift=DOWN * 1.02), run_time=0.85)
        self.at("learn to avoid")
        avoid = [p(-3.8, 1.47), p(-3.86, -1.56), p(-2.6, 1.58), p(-2.7, -1.48), p(-1.1, 1.0)]
        self.play(*[a.animate.move_to(x) for a, x in zip(animals[:5], avoid)], run_time=1.27)
        self.at("enter the second catch")
        target = trap_animals(after=True)
        self.play(*[a.animate.move_to(b) for a, b in zip(animals, target)], run_time=1.52)
        self.at("will the estimate")
        self.play(FadeIn(predict_card()), run_time=0.48)
        self.at("too high or too low", lead=0)
        settled = trap_animals(after=True, settled=True)
        self.play(*[a.animate.move_to(b) for a, b in zip(animals[:5], settled[:5])],
                  run_time=2.12, rate_func=linear)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        config.background_color = BG
        self.camera.background_color = BG
        world, _, _ = pond(closed=True, cover=False, animate=False)
        self.add(world, trap(), trap_animals(after=True, settled=True), equation(FORMULA, 1.00, 40),
                 predict_card(), scope_tag())
        self.wait(4.5)


def dog_photo(x, spotted=False):
    frame = RoundedRectangle(corner_radius=0.18, width=2.36, height=3.02,
                             stroke_color=GREY, stroke_width=3,
                             fill_color=SHALLOWS, fill_opacity=0.34)
    coat = "#DAB792"
    neck = Ellipse(width=1.36, height=0.85, fill_color=coat, fill_opacity=1,
                   stroke_width=0).shift(DOWN * 0.56)
    head = Ellipse(width=1.25, height=1.36, fill_color=coat, fill_opacity=1, stroke_width=0)
    ears = VGroup(outline([(-0.55, 0.46), (-0.87, 0.56), (-0.74, -0.24), (-0.44, 0.05)], ROCK),
                  outline([(0.55, 0.46), (0.87, 0.56), (0.74, -0.24), (0.44, 0.05)], ROCK))
    patch = Ellipse(width=0.46, height=0.49, stroke_width=0, fill_color=ROCK, fill_opacity=1)
    patch.move_to(p(0.29 if spotted else -0.31, 0.21))
    face = VGroup(Dot(p(-0.23, 0.17), radius=0.058, color=BG),
                  Dot(p(0.23, 0.17), radius=0.058, color=BG),
                  Dot(p(0, -0.15), radius=0.105, color=BG))
    return VGroup(frame, neck, ears, head, patch, face).move_to(p(x, -0.16))


class S06Catchability(SpokenScene):
    def construct(self):
        world, _, _ = pond(closed=True, cover=False)
        cage = trap()
        animals = trap_animals(after=True, settled=True)
        formula = equation(FORMULA, 1.00, 40)
        schematic = scope_tag()
        self.add(world, cage, animals, formula, schematic)
        overlap = ValueTracker(OVERLAP)
        def current_overlap():
            return round(overlap.get_value())

        out = Readout([("m₂", current_overlap, "{:.0f}", GOLD),
                       ("N", lambda: FIRST * SECOND / current_overlap(), "{:.0f}", TEXT)],
                      at=p(RIGHT_X, -0.32), size=34, widest=[99, 450], pad=0.3)
        similarity = 1.55
        track = Line(p(1.45, -1.70), p(5.35, -1.70), color=GREY, stroke_width=8)
        gauge = Dot(p(3.40, -1.70), radius=0.145, color=GOLD)
        gauge.add_updater(lambda dot: dot.move_to(p(3.40 + similarity *
                                                    (OVERLAP / current_overlap() - 1), -1.70)))
        example = label("Illustrative counts", y=-2.34, size=28, color=GREY)
        self.at("too high")
        high = label("Too high", y=2.05, color=RED, size=43)
        self.add(high)
        self.play(FadeIn(out), FadeIn(track), FadeIn(gauge), FadeIn(example), run_time=0.55)
        self.at("shrink the overlap", lead=0.58)
        self.play(overlap.animate.set_value(12),
                  *[a.animate.shift(LEFT * 0.45) for a in animals[:5]], run_time=3.20)

        self.at("animals do the reverse", lead=0.75)
        low = label("Too low", y=2.05, color=RED, size=43)
        destinations = [(-2.72, 0.57), (-2.36, -0.59), (-2.13, 0.31), (-1.72, -0.30), (-1.83, 0.63)]
        self.play(FadeOut(high), overlap.animate.set_value(OVERLAP), run_time=0.77)
        self.play(FadeIn(low), overlap.animate.set_value(30),
                  *[a.animate.move_to(p(*xy)) for a, xy in zip(animals[:5], destinations)],
                  run_time=1.60)

        self.at("photo identification", lead=0.75)
        self.play(*[FadeOut(m) for m in (cage, animals, formula, schematic, low, out, track, gauge, example)],
                  run_time=0.33)
        camera = VGroup(RoundedRectangle(width=1.38, height=0.89, corner_radius=0.16,
                                         stroke_color=BLUE, stroke_width=4),
                        Circle(radius=0.27, color=BLUE, stroke_width=4),
                        RoundedRectangle(width=0.40, height=0.22, corner_radius=0.06,
                                         fill_color=BLUE, fill_opacity=1, stroke_width=0).move_to(p(-0.35, 0.53)))
        camera.move_to(p(-3.25, -0.15))
        self.play(GrowFromCenter(camera), run_time=0.54)
        pics = VGroup(dog_photo(1.90), dog_photo(4.81, spotted=True))
        self.play(Flash(camera, color=TEXT, flash_radius=0.94), FadeIn(pics[0], shift=UP * 0.2),
                  run_time=0.80)
        self.at("as in a 2018", lead=0.4)
        place = label("Quito, 2018", y=2.22, color=GOLD, size=34)
        self.play(FadeIn(place), FadeIn(pics[1], shift=UP * 0.2), run_time=0.8)
        self.at("can mismatch")
        mismatch = label("Possible mismatch", y=-2.22, size=30, color=RED)
        self.play(Indicate(pics, color=RED, scale_factor=1.035), FadeIn(mismatch), run_time=1.34)
        self.at("every result is an", lead=0.3)
        takeaway = label("Estimate, not head count", y=-2.36, size=34, color=GOLD)
        self.play(FadeOut(mismatch), FadeIn(takeaway), run_time=0.54)
        self.finish()


def open_pond():
    world, reeds, boundary = pond(closed=True)
    neighbor_center = p(3.82, -0.72)
    neighbor = VGroup(shore(3.82, -0.72, width=5.30, height=3.78),
                      ripples(neighbor_center, scale=0.73),
                      reed_patch(4.97, -1.43, 1.26, 0.64))
    water_light(neighbor[0][-1], phase=1.18)
    channel = outline([(-1.05, -0.42), (0.30, -0.34), (1.59, -0.66),
                       (1.63, -1.29), (0.29, -1.0), (-1.05, -1.11)], SHALLOWS)
    channel.set_z_index(-1)
    return world, reeds, boundary, neighbor, channel


class S07SurvivalControls(SpokenScene):
    def construct(self):
        world, reeds, boundary, neighbor, channel = open_pond()
        marked = fish(True, width=0.95).move_to(p(-3.28, -0.32)).set_z_index(2)
        self.add(world, reeds, marked, scope_tag())

        self.at("populations open", lead=0.58)
        self.play(FadeOut(boundary), GrowFromEdge(channel, LEFT), FadeIn(neighbor),
                  run_time=1.55)

        self.at("on repeated visits", lead=0.5)
        tags = VGroup(*[label(f"Visit {i}", x, 3.07, 28, TEXT)
                        for i, x in enumerate([1.10, 3.04, 4.98], 1)])
        self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.30), run_time=1.30)
        records = [label("1", 1.10, 2.29, 52, GREEN), label("0", 3.04, 2.29, 52, GOLD),
                   label("1", 4.98, 2.29, 52, GREEN)]
        self.at("an animal seen", lead=0.40)
        self.play(FadeIn(records[0]), marked.animate.move_to(p(-2.85, 0.30)), run_time=0.74)
        self.at("after a gap", lead=0.52)
        self.play(FadeIn(records[1]), marked.animate.move_to(p(-2.11, 0.64)), run_time=0.76)
        self.at("was alive and missed", lead=0.46)
        self.play(FadeIn(records[2]), marked.animate.move_to(p(-1.90, -0.37)), run_time=0.70)
        missed = label("Alive and missed", 3.04, 1.55, 29, GOLD)
        self.play(FadeIn(missed), run_time=0.50)

        self.at("a survivor that leaves", lead=0.62)
        direction = DashedLine(p(-1.26, -0.65), p(2.56, -0.79), dash_length=0.16,
                               color=BLUE, stroke_width=4)
        tip = Triangle(stroke_width=0, fill_color=BLUE, fill_opacity=1).scale(0.13)
        tip.rotate(-PI / 2).move_to(p(2.59, -0.79))
        self.play(FadeOut(VGroup(tags, *records, missed)), Create(direction),
                  FadeIn(tip), marked.animate.move_to(p(3.12, -0.79)), run_time=1.70)

        self.at("apparent survival", lead=0.35)
        formula_title = label("Apparent survival", 3.07, 3.05, 39, GOLD)
        self.play(FadeIn(formula_title), run_time=0.48)
        self.at("true survival", lead=0.38)
        true_survival = label("= true survival", 1.75, 2.27, 31)
        self.play(FadeIn(true_survival), run_time=0.5)
        self.at("sight fidelity", lead=0.30)
        fidelity = label("× site fidelity", 4.45, 2.27, 31)
        self.play(FadeIn(fidelity), run_time=0.48)
        self.at("the chance a survivor", lead=0.28)
        meaning = label("Chance of staying", 4.45, 1.65, 28, BLUE)
        self.play(FadeIn(meaning), marked.animate.shift(RIGHT * 0.86), run_time=1.65)

        self.at("searching nearby sites", lead=0.27)
        search = Ellipse(width=4.67, height=3.17, stroke_color=GREEN,
                         stroke_width=4).move_to(p(3.82, -0.72))
        self.play(FadeOut(VGroup(direction, tip, formula_title, true_survival, fidelity, meaning)),
                  Create(search), run_time=1.30)
        self.play(search.animate.stretch(1.11, 0).stretch(1.08, 1), run_time=1.25)
        self.at("and double marking", lead=0.22)
        second_mark = Dot(marked.get_center() + p(0.18, 0.015), radius=0.107, color=GREEN).set_z_index(3)
        double = caption("Double marking catches mark loss", size=31)
        self.play(GrowFromCenter(second_mark), FadeIn(double), run_time=0.58)
        self.play(VGroup(marked, second_mark).animate.shift(p(0.73, 0.46)), run_time=1.8)
        self.finish()


def finch(size=1.0, deeper=False):
    coat = "#CFAD8F"
    tail = outline([(-0.42, 0.04), (-1.08, -0.25), (-0.95, -0.42), (-0.30, -0.22)], ROCK)
    feet = VGroup(Line(p(-0.22, -0.30), p(-0.28, -0.64), color=coat, stroke_width=4),
                  Line(p(0.08, -0.28), p(0.13, -0.65), color=coat, stroke_width=4))
    breast = Ellipse(width=1.25, height=0.78, stroke_width=0, fill_color=coat,
                     fill_opacity=1).rotate(0.34)
    upper = Circle(radius=0.42, stroke_width=0, fill_color=coat, fill_opacity=1).move_to(p(0.42, 0.36))
    beak = outline([(0.73, 0.47), (1.19 if deeper else 1.06, 0.29),
                    (0.72, 0.08 if deeper else 0.19)], "#FFCB87")
    wing = Ellipse(width=0.82, height=0.39, stroke_width=0, fill_color=ROCK,
                   fill_opacity=0.82).rotate(0.31).move_to(p(-0.28, 0))
    pupil = Dot(p(0.55, 0.48), radius=0.065, color=BG)
    band = RoundedRectangle(width=0.18, height=0.12, corner_radius=0.04,
                            fill_color=GOLD, fill_opacity=1, stroke_width=0).move_to(p(-0.26, -0.49))
    result = VGroup(tail, feet, breast, upper, wing, beak, pupil, band).scale(size)
    result.band = band
    result.beak = beak
    return result


def volcanic_ground():
    ridge = outline([(-6.25, -2.50), (-6.25, -0.40), (-5.10, -0.10), (-4.30, 0.62),
                     (-2.70, 0.40), (-1.58, 1.14), (0.49, 0.72), (1.86, 0.12),
                     (3.02, 0.48), (4.60, 0.15), (6.25, -0.69), (6.25, -2.50)], ROCK)
    lower = outline([(-6.25, -2.50), (-6.25, -1.38), (-4.56, -1.67), (-2.86, -1.52),
                     (-1.19, -1.80), (1.27, -1.37), (3.63, -1.77), (6.25, -1.40),
                     (6.25, -2.50)], "#593B37")
    stones = VGroup()
    rng = np.random.default_rng(19)
    for _ in range(36):
        x, y = rng.uniform(-6.10, 6.10), rng.uniform(-2.44, -1.85)
        stones.add(Dot(p(x, y), radius=rng.uniform(0.027, 0.075), color=FIELD))
    return VGroup(ridge, lower, stones)


class S08UnlockedFinches(SpokenScene):
    def construct(self):
        ground = volcanic_ground()
        birds = VGroup(*[finch(s, deep).move_to(p(x, -0.56 + s * 0.17))
                         for x, s, deep in [(-4.78, 0.88, False), (-2.08, 1.10, False),
                                            (0.92, 1.25, True), (4.12, 1.52, True)]])
        for bird in birds:
            bird.band.set_opacity(0)
        self.add(ground, scope_tag())
        self.at("marking and revisiting")
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.24) for b in birds], lag_ratio=0.29),
                  run_time=2.0)
        self.play(*[b.animate.shift(RIGHT * 0.24) for b in birds], run_time=1.54)
        for i, bird in enumerate(birds):
            bob(bird, amp=0.15, speed=2.1, seed=i)
        self.at("on the galapagos", lead=0.4)
        heading = field_heading("Daphne Major", "Galápagos  ·  1977–1981")
        self.play(FadeIn(heading), run_time=0.64)

        self.at("grant banded", lead=0.34)
        self.play(LaggedStart(*[b.band.animate.set_opacity(1) for b in birds], lag_ratio=0.35),
                  run_time=1.27)
        ruler = VGroup(Line(p(-5.80, -1.69), p(5.72, -1.69), color=BLUE, stroke_width=3),
                       *[Line(p(x, -1.69), p(x, -1.55), color=BLUE, stroke_width=2.5)
                         for x in np.linspace(-5.8, 5.72, 21)])
        self.play(Create(ruler), run_time=1.1)
        self.at("1977 drought", lead=0.75)
        survivors = strip(1, x=0, y=1.61, width=8.10, height=0.74, color=GREEN)
        drought = label("1977 drought", 0, 2.35, 31, RED)
        self.play(FadeOut(ruler), FadeIn(drought), GrowFromEdge(survivors, LEFT), run_time=0.80)
        self.at("roughly 85", lead=0.28)
        loss = label("≈85% died", 0, -2.93, 35, RED)
        third = strip(1 - 0.85, x=0, y=1.61, width=8.10, height=0.74, color=GREEN)
        self.play(Transform(survivors[1], third[1]), FadeIn(loss), run_time=2.15)
        self.at("report showed larger", lead=0.55)
        for bird in birds:
            bird.clear_updaters()
        large = caption("Larger birds survived best", 34, GREEN)
        self.play(swap(loss, large), FadeOut(VGroup(drought, survivors)),
                  *[b.animate.set_opacity(0.36).shift(DOWN * 0.21) for b in birds[:2]],
                  *[b.animate.shift(UP * 0.55) for b in birds[2:]], run_time=1.95)
        for i, bird in enumerate(birds[2:]):
            bob(bird, amp=0.17, speed=2.4, seed=i)
        self.at("males with larger", lead=0.45)
        beaks = caption("Larger-beaked males survived best", 34, GREEN)
        self.play(swap(large, beaks),
                  *[Indicate(b.beak, color=GOLD, scale_factor=1.22) for b in birds[2:]],
                  run_time=1.32)
        self.at("beak and body size", lead=0.2)
        linked = caption("Beak and body size correlated", 34, GOLD)
        self.play(swap(beaks, linked), run_time=0.7)
        self.finish()


def stream_pool(cx, inverse=False):
    center = p(cx, -0.13)
    water = shore(cx, -0.13, 5.78, 4.52)
    water_light(water[-1], phase=0.40 if inverse else 0)
    pool = VGroup(water, ripples(center, scale=0.78))
    points = [(-1.42, 0.84), (0.50, 0.80), (-0.93, -0.72), (1.24, -0.59)]
    guppies = VGroup(*[fish(marked=True, spotted=(i != 3 if inverse else i == 3), width=1.00).move_to(
        center + p(*xy)) for i, xy in enumerate(points)])
    rare = Circle(radius=0.63, color=GOLD, stroke_width=4).move_to(guppies[-1])
    return pool, guppies, rare


class S09UnlockedGuppies(SpokenScene):
    def construct(self):
        left, a, rare_a = stream_pool(-3.27)
        right, b, rare_b = stream_pool(3.27, inverse=True)
        heading = field_heading("Trinidad streams", "2006")
        self.add(left, right, heading, scope_tag())
        self.at("recaptured marked male", lead=0.55)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.37) for m in [*a, *b]],
                              lag_ratio=0.12), run_time=1.83)
        self.at("three trinidad streams")
        source = label("Three streams", 0, -2.91, 30, TEAL)
        self.play(FadeIn(source), run_time=0.47)

        self.at("about three common", lead=0.45)
        count_a = label("3 plain : 1 spotted", -3.27, -2.74, 31)
        count_b = label("3 spotted : 1 plain", 3.27, -2.74, 31)
        self.play(FadeOut(source), Create(rare_a), FadeIn(count_a), run_time=0.85)
        self.at("reversing which pattern", lead=0.40)
        self.play(Create(rare_b), FadeIn(count_b), run_time=1.04)

        self.at("after 15 or 17", lead=0.5)
        gap = label("15 or 17 days", 0, 2.45, 32, GOLD)
        self.play(FadeOut(VGroup(count_a, count_b)), FadeIn(gap), run_time=0.55)
        self.play(*[m.animate.shift(RIGHT * 0.26) for m in [*a, *b]],
                  rare_a.animate.shift(RIGHT * 0.26), rare_b.animate.shift(RIGHT * 0.26),
                  run_time=1.48)
        self.at("rare males had higher", lead=0.35)
        higher = caption("Higher estimated survival", 35, GREEN)
        self.play(FadeIn(higher),
                  *[m.animate.set_opacity(0.38) for m in [*a[:3], *b[:3]]], run_time=1.12)
        self.at("if missing fish", lead=0.25)
        assumption = label("Assumes missing fish died,\nrather than moved", 0, -3.01, 30, GOLD)
        self.play(swap(higher, assumption), run_time=0.65)
        pulse(rare_a, 4.5, 1.8, 3.2)
        pulse(rare_b, 4.5, 1.8, 3.2)
        self.finish()


def wetland_grid():
    pools = VGroup()
    for i in range(29):
        row, col = divmod(i, 6)
        x, y = -5.85 + col * 1.23, 1.71 - row * 0.93
        tile = shore(x, y, 1.12, 0.79)
        water_light(tile[-1], phase=0.23 * row + 0.18 * col)
        pools.add(tile)
    return pools


def toad(size=0.30):
    body = Ellipse(width=0.81, height=1.0, stroke_width=0, fill_color=GREEN, fill_opacity=1)
    legs = VGroup()
    for s in (-1, 1):
        legs.add(Ellipse(width=0.35, height=0.60, stroke_width=0, fill_color=GREEN, fill_opacity=1)
                 .rotate(s * 0.38).move_to(p(s * 0.37, -0.24)))
        legs.add(Dot(p(s * 0.22, 0.34), radius=0.11, color=INK))
        legs.add(Dot(p(s * 0.22, 0.36), radius=0.053, color=BG))
    return VGroup(body, legs).set_height(size)


class S10UnlockedToads(SpokenScene):
    def construct(self):
        pools = wetland_grid()
        self.add(pools, scope_tag())
        self.at("zeros are ambiguous")
        unknown = label("000", y=1.47, size=65, color=GOLD)
        labels = VGroup(label("Absent", y=0.44, size=32), label("Missed", y=-0.35, size=32, color=GOLD))
        self.play(FadeIn(unknown), run_time=0.55)
        self.at("absent or just", lead=0.35)
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.17) for m in labels], lag_ratio=0.7),
                  run_time=1.00)

        self.at("in 2002", lead=0.22)
        heading = field_heading("Maryland wetlands", "MacKenzie et al.  ·  2002")
        date = label("2000 surveys", y=1.18, size=32, color=TEAL)
        self.play(FadeOut(VGroup(unknown, labels)), FadeIn(heading), run_time=0.60)
        self.at("repeat maryland", lead=0.22)
        self.play(FadeIn(date), run_time=0.48)
        scans = VGroup(*[Line(p(-6.37, 1.71 - row * 0.93), p(0.93, 1.71 - row * 0.93),
                              color=TEAL, stroke_width=4).set_opacity(0.50) for row in range(5)])
        self.play(LaggedStart(*[ShowPassingFlash(line, time_width=0.7) for line in scans],
                              lag_ratio=0.26), run_time=2.72)

        self.at("american toads were", lead=0.43)
        detected = [0, 3, 7, 9, 12, 16, 19, 22, 25, 28]
        zeros = VGroup(*[T("000", 28, TEXT).move_to(pool) for i, pool in enumerate(pools) if i not in detected])
        # The symbols are schematic; detected and undetected site counts are exact.
        seen = VGroup(*[toad(0.40).move_to(pools[i]) for i in detected])
        detected_heading = label("Detected wetlands", y=1.63, size=33, color=GREEN)
        self.play(swap(date, detected_heading, 0.65),
                  LaggedStart(*[GrowFromCenter(t) for t in seen], lag_ratio=0.13),
                  run_time=1.77)
        self.at("10 of 29", lead=0.05)
        fraction = equation(f"{len(detected)} ÷ {len(pools)}", 0.92, 37)
        self.play(FadeIn(fraction), FadeIn(zeros), run_time=0.6)
        self.at("about 0", lead=0.24)
        observed = len(detected) / len(pools)
        detected_value = equation(f"{observed:.2f}", 0.92, 42, GREEN)
        first = strip(observed, x=3.50, y=0.15, width=4.60, color=GREEN)
        self.play(swap(fraction, detected_value), GrowFromEdge(first, LEFT), run_time=0.67)

        self.at("modeling detection", lead=0.28)
        estimated_heading = label("Estimated occupancy", y=-0.65, size=33, color=GOLD)
        self.play(FadeIn(estimated_heading), run_time=0.55)
        missed = [4, 13, 18, 26]
        hidden = VGroup(*[toad(0.42).move_to(pools[i]) for i in missed])
        marked_zeros = [zero for zero in zeros if any(
            np.linalg.norm(zero.get_center() - pools[i].get_center()) < 0.1 for i in missed)]
        self.at("occupancy to 0", lead=0.02)
        estimated_value = equation("0.49", -1.31, 42, GOLD)
        second = strip(0.49, x=3.50, y=-2.03, width=4.60, color=GOLD)
        self.play(FadeIn(estimated_value), GrowFromEdge(second, LEFT),
                  Succession(FadeOut(VGroup(*marked_zeros)), FadeIn(hidden)), run_time=1.25)

        self.at("repeated marks and", lead=0.4)
        for i, pool in enumerate(pools):
            pool[1].add_updater(
                lambda m, dt, phase=i * 0.27: m.set_fill(
                    interpolate_color(ManimColor(SHALLOWS), ManimColor(TEAL),
                                      0.5 + 0.5 * np.sin(self.elapsed() * 2.6 + phase))))
        rule = caption("Repeated visits reveal misses", 34, GOLD)
        self.play(FadeIn(rule), run_time=0.73)
        self.finish()


class S11End(EndCard):
    LINE = "Mark and revisit to estimate populations and separate misses from loss."
