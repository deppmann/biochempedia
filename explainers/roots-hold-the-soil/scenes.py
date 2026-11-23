"""Roots Hold the Soil, a schematic parent guide."""

from bp_parts import *
from bp_style import EndCard

# Color map: BLUE water, GREEN grass, GOLD roots and teaching cues, RED safety.
# Soil and sediment share warm browns, cartons and cups use neutral GREY/TEAL.
SOIL = "#946141"
EARTH = "#70452F"
SILT = "#C39260"
MUD = "#97654C"
GRASS = "#527E50"
BANK = "#385D4C"
SKY = "#1B2D39"
GLASS = "#A9D7DB"
CARTON = "#648C93"
WOOD = "#483B37"
PAPER = "#F3DDAB"
SKIN = "#D99C78"
LEFT_TRAY, RIGHT_TRAY = -3.32, 3.32
TRAY_TILT = -.16
QUESTION = "What do you predict the cups will look like?"


def point(x, y):
    return np.array([x, y, 0.0])


def shape(vertices, color, edge=None, width=2):
    return Polygon(*(point(*xy) for xy in vertices),
                   fill_color=color, fill_opacity=1,
                   stroke_color=edge or color, stroke_width=width if edge else 0)


def block(w, h, xy, color, radius=0.0):
    cls = RoundedRectangle if radius else Rectangle
    corners = {"corner_radius": radius} if radius else {}
    return cls(width=w, height=h, fill_color=color, fill_opacity=1,
               stroke_width=0, **corners).move_to(point(*xy))


def stroke(vertices, color, width=3, smooth=False):
    line = VMobject().set_stroke(color, width)
    pins = [point(*xy) for xy in vertices]
    return line.set_points_smoothly(pins) if smooth else line.set_points_as_corners(pins)


def heading(words, color=TEXT):
    return T(words, 36, color, weight=BOLD).move_to(point(0, 2.97))


def texture(cx, cy, w, h, count, seed, colors):
    rng = np.random.default_rng(seed)
    return VGroup(*(Ellipse(width=rng.uniform(.04, .14), height=rng.uniform(.025, .055),
                            fill_color=colors[i % len(colors)], fill_opacity=.75, stroke_width=0)
                    .rotate(rng.uniform(-.6, .6)).move_to(point(
                        cx + rng.uniform(-w / 2, w / 2), cy + rng.uniform(-h / 2, h / 2)))
                    for i in range(count)))


def sky_band():
    return block(13.2, 7.2, (0, -.03), SKY, .28)


def ground_profile():
    return [(-6.6, -.46), (-5.65, .05), (-4.9, .78), (-3.97, 1.1),
            (-3.1, 1.04), (-2.22, .63), (-.95, .16), (.45, -.2), (1.55, -.25),
            (2.35, .08), (3.6, .55), (4.45, .68), (5.55, .56), (6.6, .23)]


def landscape():
    """The same hill, patch, path and channel for the hook, title and walk."""
    profile = ground_profile()
    hills = shape([(-6.6, -.3), (-6.6, .65), (-4.9, 1.65), (-3.64, 1.85),
                   (-2.3, 1.18), (-.85, 1.28), (.65, .76), (1.95, 1.26),
                   (3.55, 1.75), (4.9, 1.61), (6.6, .91), (6.6, -.3)], BANK)
    ground = shape(profile + [(6.6, -2.64), (-6.6, -2.64)], GRASS)
    patch = shape([(1.35, -.29), (2.35, .08), (3.6, .55), (4.45, .68),
                   (5.55, .56), (6.6, .23), (6.6, -1.15), (5.5, -.91),
                   (3.84, -1.25), (2.04, -.85)], SOIL)
    channel = shape([(-6.6, -1.86), (-4.6, -2.02), (-3, -1.85), (-.6, -1.31),
                     (1.15, -1.39), (2.8, -1.85), (4.4, -1.75), (6.6, -1.15),
                     (6.6, -2.45), (4.62, -2.7), (2.61, -2.74), (.73, -2.35),
                     (-.77, -2.26), (-3.2, -2.7), (-6.6, -2.86)], MUD)
    path = stroke([(-6.1, -.48), (-5.05, -.36), (-4.1, -.57), (-3.1, -.73),
                   (-1.8, -.67), (-.38, -.61), (.87, -.63), (1.55, -.49)], PAPER, 12, True)
    flecks = texture(4.6, -.32, 3.3, .61, 26, 42, [SILT, EARTH])
    return VGroup(sky_band(), hills, ground, patch, flecks, path, channel)


def current():
    ripples = VGroup()
    for i in range(26):
        phase = i / 26
        y = -.12 + (i % 5) * .14
        ripple = stroke([(-.40, -.02), (-.18, .07), (.16, .07), (.42, -.025)],
                        SILT if i % 3 else PAPER, 6.4 if i % 3 else 4.6, True)
        def drift(m, dt, y=y, phase=phase):
            m.phase = (getattr(m, "phase", phase) + dt * .092) % 1
            x = -6.2 + 12.4 * m.phase
            m.move_to(point(x, -2.21 + .31 * np.cos((x + .2) * .65) + y))
            m.set_stroke(opacity=.75 * min(1, m.phase * 18, (1 - m.phase) * 18))
        ripple.add_updater(drift, call_updater=True)
        ripples.add(ripple)
    return ripples


def rain(x, width, top, bottom, speed=1.8, count=16, color=BLUE):
    """Soft, staggered streaks that end at the surface being watered."""
    streaks = VGroup()
    for i in range(count):
        phase = ((i + .5) * .61803399) % 1
        dx = width * ((i + .5) / count - .5)
        drop = Line(ORIGIN, point(-.075, -.26), color=color, stroke_width=3.3)
        def fall(m, dt, phase=phase, dx=dx):
            m.phase = (getattr(m, "phase", phase) + dt * speed / (top - bottom)) % 1
            m.move_to(point(x + dx - .1 * m.phase, top - (top - bottom) * m.phase))
            m.set_stroke(opacity=.82 * min(1, m.phase * 9, (1 - m.phase) * 10))
        drop.add_updater(fall, call_updater=True)
        streaks.add(drop)
    return streaks


def bench():
    """Shared table edge leaves both notches hanging over the catch cups."""
    return VGroup(sky_band(),
                  block(13.05, .65, (0, -1.56), WOOD, .12),
                  block(13.05, .075, (0, -1.265), "#9D7461"),
                  block(13.05, 1.03, (0, -2.03), "#29272B", .10))


def blades(x, y, width, n=23):
    tuft = VGroup()
    rng = np.random.default_rng(8)
    for i in range(n):
        dx = (i / (n - 1) - .5) * width
        h = rng.uniform(.22, .66)
        lean = rng.uniform(-.24, .24)
        tuft.add(stroke([(x + dx, y), (x + dx + lean * .3, y + h * .53),
                         (x + dx + lean, y + h)], GREEN if i % 3 else "#C4DD80", 3.7, True))
    return tuft


def roots(x, y, width, depth=1):
    threads = VGroup()
    for i in range(12):
        base = x + width * (i / 11 - .5)
        lean = .18 * np.sin(i * 2.6)
        tip = y - depth * (.65 + .3 * (i % 4) / 3)
        threads.add(stroke([(base, y), (base + lean, y - depth * .43),
                            (base - lean * .66, tip)], PAPER, 2.2, True))
        threads.add(stroke([(base + lean, y - depth * .43),
                            (base + lean * 2 + .08, tip + .09)], SILT, 1.5))
    return threads


def tray_hinge(cx):
    return point(cx + 1.73, -.90)


def tray(cx, grass=False, soil=True, tilted=True, notched=True):
    """Make both cartons from the same profile. The low outlet is on the right."""
    rim = [(cx - 2.48, .16), (cx - 2.22, .49), (cx + 1.62, .49),
           (cx + 1.93, .16), (cx + 1.69, -.76), (cx - 2.3, -.76)]
    shell = shape(rim, CARTON, GLASS)
    inner = shape([(cx - 2.3, .19), (cx - 2.08, .36), (cx + 1.52, .36),
                   (cx + 1.74, .17), (cx + 1.55, -.53), (cx - 2.16, -.53)], "#355563")
    bed = shape([(cx - 2.22, .05), (cx - 1.98, .28), (cx + 1.42, .28),
                 (cx + 1.71, .05), (cx + 1.55, -.47), (cx - 2.08, -.47)], SOIL)
    grains = texture(cx - .2, -.105, 3.45, .54, 25, 78, [SILT, EARTH])
    lawn = blades(cx - .25, .13, 3.42)
    stripe = stroke([(cx - 2.22, -.64), (cx + 1.60, -.64)], GLASS, 2.6)
    outlet = shape([(cx + 1.55, -.09), (cx + 1.89, -.09), (cx + 1.75, -.49)],
                   "#293A46", None)
    g = VGroup(shell, inner, bed, grains, stripe, lawn, outlet).shift(DOWN * .34)
    g.soil_bed = VGroup(bed, grains)
    g.lawn = lawn
    g.outlet = outlet
    if tilted:
        g.rotate(TRAY_TILT, about_point=tray_hinge(cx))
    if not soil:
        g.remove(bed, grains)
    if not grass:
        g.remove(lawn)
    if not notched:
        outlet.set_fill(opacity=0)
    return g


def books(cx):
    x = cx - 1.52
    return VGroup(block(1.55, .31, (x, -1.10), "#856EAA", .045),
                  block(1.38, .35, (x - .07, -.765), "#C47B59", .045),
                  block(1.14, .052, (x - .05, -1.09), PAPER),
                  block(1.00, .047, (x - .12, -.82), PAPER))


def cup_x(cx):
    return cx + 1.76


def cup_outline(cx, y=-1.91, scale=1):
    x = cup_x(cx)
    shell = shape([(x - .56, y + .53), (x + .56, y + .53), (x + .40, y - .56),
                   (x - .40, y - .56)], "#294351", GLASS, 2.5)
    rim = Ellipse(width=1.12, height=.155, color=GLASS, stroke_width=2.2).move_to(point(x, y + .53))
    glint = stroke([(x - .43, y + .38), (x - .34, y - .29)], GLASS, 2)
    return VGroup(shell, rim, glint).scale(scale, about_point=point(x, y))


def liquid(cx, height, cloudy, sediment=0):
    if height <= .005:
        return VGroup()
    x, floor = cup_x(cx), -2.43
    top = floor + height
    width = .38 + height * .14
    hue = MUD if cloudy else "#508E9C"
    fill = shape([(x - .38, floor), (x + .38, floor), (x + width, top),
                  (x - width, top)], hue)
    surface = Ellipse(width=2 * width, height=.082, fill_color=SILT if cloudy else BLUE,
                      fill_opacity=1, stroke_width=0).move_to(point(x, top))
    layer_top = floor + sediment
    layer = shape([(x - .37, floor + .01), (x + .37, floor + .01),
                   (x + .40, layer_top), (x - .40, layer_top)], EARTH)
    return VGroup(fill, surface, *([layer] if sediment else []))


def experiment(cups=True, grass=True):
    return VGroup(bench(), books(LEFT_TRAY), books(RIGHT_TRAY),
                  tray(LEFT_TRAY), tray(RIGHT_TRAY, grass=grass),
                  *([cup_outline(LEFT_TRAY), cup_outline(RIGHT_TRAY)] if cups else []))


def can(cx):
    x, y = cx - .48, 1.88
    handle = Ellipse(width=.78, height=.91, color=GLASS, stroke_width=7).move_to(point(x + .67, y + .1))
    body = block(1.38, .93, (x, y), "#478F93", .20)
    spout = shape([(x - .53, y - .33), (x - 1.67, y - .38), (x - 1.83, y - .16),
                   (x - .63, y + .12)], CARTON, GLASS, 2)
    rose = block(.37, .28, (x - 1.74, y - .31), GLASS, .065).rotate(.24)
    rim = Ellipse(width=.67, height=.14, fill_color="#27565E", fill_opacity=1,
                  stroke_color=GLASS, stroke_width=2).move_to(point(x, y + .45))
    return VGroup(handle, spout, body, rose, rim)


def guess_sheet(x=0, y=1.7):
    paper = block(2.48, 1.61, (x, y), PAPER, .10)
    corner = shape([(x + .83, y + .80), (x + 1.23, y + .40),
                    (x + .83, y + .40)], SILT)
    lines = VGroup(*(stroke([(x - .91, y + dy), (x + .67, y + dy)], SOIL, 1.6)
                     for dy in (.32, -.07, -.46)))
    return VGroup(paper, corner, lines)


def writing(x=0, y=1.7):
    return stroke([(x - .86, y + .37), (x - .61, y + .43), (x - .41, y + .36),
                   (x - .19, y + .42), (x + .13, y + .37), (x + .45, y + .42)], EARTH, 3, True)


def pencil(x, y):
    return VGroup(block(.21, 1.0, (x, y + .58), GOLD, .045),
                  shape([(x - .105, y + .10), (x + .105, y + .10), (x, y)], PAPER)
                  ).rotate(-.42, about_point=point(x, y))


def people(x, y, scale=1, walking=False):
    group = VGroup()
    for offset, h, color in [(-.45, 1.8, TEAL), (.45, 1.27, GOLD)]:
        p = x + offset * scale
        top = y + h * scale
        torso = block(.47 * scale, .56 * h * scale, (p, y + .57 * h * scale), color, .11 * scale)
        head = Dot(point(p, top), radius=.205 * scale, color=SKIN)
        stride = .18 if walking else .10
        leg_a = stroke([(p - .09 * scale, y + .33 * h * scale), (p - stride * scale, y)], GLASS, 5 * scale)
        leg_b = stroke([(p + .09 * scale, y + .33 * h * scale), (p + stride * scale, y)], CARTON, 5 * scale)
        arm = stroke([(p, y + .73 * h * scale), (p + .37 * scale, y + .52 * h * scale)], SKIN, 6 * scale)
        group.add(VGroup(leg_a, leg_b, torso, arm, head))
    return group


def measure_mark(x, bottom, top):
    return VGroup(stroke([(x, bottom), (x, top)], GOLD, 2.5),
                  stroke([(x - .095, bottom), (x + .095, bottom)], GOLD, 2.5),
                  stroke([(x - .095, top), (x + .095, top)], GOLD, 2.5))


def soil_bag(x, y):
    sack = shape([(x - .78, y - .79), (x + .73, y - .79), (x + .82, y - .51),
                  (x + .63, y + .76), (x + .49, y + .93), (x - .64, y + .83),
                  (x - .81, y + .44)], PAPER)
    opening = Ellipse(width=1.19, height=.27, fill_color=EARTH, fill_opacity=1,
                      stroke_color=SILT, stroke_width=3).move_to(point(x - .03, y + .76))
    mark = shape([(x - .5, y - .22), (x - .09, y + .25), (x + .17, y - .02),
                  (x + .39, y + .08), (x + .55, y - .27), (x - .5, y - .27)], SOIL)
    return VGroup(sack, opening, mark)


def seed_packet(x, y):
    return VGroup(block(1.13, 1.38, (x, y), PAPER, .085),
                  block(.95, .24, (x, y + .45), CARTON, .025),
                  blades(x, y - .35, .64, 6).scale(.71, about_point=point(x, y - .35)))


def sun(x, y):
    return VGroup(Dot(point(x, y), radius=.29, color=GOLD),
                  *(Line(point(x, y) + .39 * v, point(x, y) + .51 * v, color=GOLD, stroke_width=3)
                    for t in np.arange(8) * TAU / 8 for v in [point(np.cos(t), np.sin(t))]))


def calendar(x, y):
    page = block(2.07, 1.35, (x, y), PAPER, .10)
    header = block(2.07, .26, (x, y + .56), CARTON, .055)
    days = VGroup(*(block(.13, .12, (x + dx, y + dy), SOIL, .015)
                    for dy in (.23, -.05, -.32) for dx in np.linspace(-.78, .78, 7)))
    return VGroup(page, header, days)


def cutter(x, y):
    """Open scissors held by an adult hand."""
    hand = block(.72, .45, (x + .77, y + .08), SKIN, .17)
    handle = VGroup(*(Circle(radius=.155, color=RED, stroke_width=5)
                      .move_to(point(x + .43, y + dy)) for dy in (-.15, .18)))
    shears = VGroup(stroke([(x + .30, y - .12), (x, y), (x - .52, y + .29)], TEXT, 4),
                    stroke([(x + .30, y + .13), (x, y), (x - .52, y - .25)], GLASS, 4))
    return VGroup(hand, handle, shears)


class S01Hook(SpokenScene):
    def construct(self):
        self.add(landscape(), current())
        self.at("after a storm")
        storm = rain(0, 12.4, 3.37, -.45, count=39)
        self.add(storm)
        self.at("where does that mud")
        self.play(FadeOut(storm), run_time=.33)
        self.play(FadeIn(question_card("Where does the mud come from?", y=2.61, size=42)), run_time=.44)
        self.at("two trays of soil")
        feeder = stroke([(5.48, -.03), (5.09, -.34), (5.24, -.67), (4.87, -.95),
                         (4.30, -1.11), (4.11, -1.49), (3.49, -1.92)], SILT, 13, True)
        self.play(Create(feeder), run_time=1.34, rate_func=linear)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Roots Hold the Soil"
    TITLE = "Roots Hold the Soil: Parent Guide"

    def construct(self):
        self.add(landscape(), current())
        title = T(self.LESSON, 51, font=TITLE_FONT).move_to(point(0, 2.76))
        title.align_to(point(-5.96, 0), LEFT)
        guide = T("Parent Guide", 29, GLASS).next_to(title, DOWN, aligned_edge=LEFT, buff=.14)
        self.play(FadeIn(title), FadeIn(guide), run_time=.4)
        self.wait(1.53)


class S03Payoff(SpokenScene):
    def construct(self):
        land = VGroup(landscape(), current())
        self.add(land)
        self.at("once the trays")
        world = VGroup(bench(), tray(LEFT_TRAY, tilted=False), tray(RIGHT_TRAY, True, tilted=False),
                       cup_outline(LEFT_TRAY), cup_outline(RIGHT_TRAY))
        self.play(FadeOut(land, shift=UP * .3), FadeIn(world, shift=UP * .25), run_time=.9)
        self.at("about 35 minutes")
        message = heading("About 35 minutes", GOLD)
        self.play(FadeIn(message), run_time=.42)
        self.at("makes a guess")
        next_message = heading("Make a guess", GOLD)
        sheet = guess_sheet(0, 1.63)
        self.play(swap(message, next_message), FadeIn(sheet, shift=UP * .3), run_time=.68)
        pen_ink = writing(0, 1.63)
        self.play(Create(pen_ink), run_time=.65)
        self.at("giving both trays")
        matched = heading("Same rain on both", BLUE)
        shower = VGroup(rain(LEFT_TRAY - .75, 2.55, 1.96, .06, count=13),
                        rain(RIGHT_TRAY - .75, 2.55, 1.96, .49, count=13))
        self.play(swap(next_message, matched), FadeOut(sheet), FadeOut(pen_ink), run_time=.60)
        self.add(shower)
        self.at("they practice explaining")
        cups = heading("Cups check it", GOLD)
        self.play(FadeOut(shower), swap(matched, cups), run_time=.58)
        outline = VGroup(*(Arc(radius=.71, start_angle=PI * 1.10, angle=PI * .8,
                                color=GOLD, stroke_width=4).move_arc_center_to(point(cup_x(cx), -1.99))
                           for cx in (LEFT_TRAY, RIGHT_TRAY)))
        self.play(Create(outline), run_time=1.15)
        self.finish()


class S04Grow(SpokenScene):
    def construct(self):
        right = tray(RIGHT_TRAY, soil=False, tilted=False, notched=False)
        left = tray(LEFT_TRAY, soil=False, tilted=False, notched=False)
        adults = people(-.28, -1.26, .83)
        self.add(bench(), left, right, adults)
        self.at("stay with your child")
        bag = soil_bag(RIGHT_TRAY - 1.13, 1.62)
        self.at("use bagged soil")
        self.play(FadeOut(adults), FadeIn(bag, shift=UP * .3), run_time=.53)
        right.insert(2, right.soil_bed)
        self.play(bag.animate.rotate(-.17), FadeIn(right.soil_bed), run_time=.80)
        self.at("untreated seed")
        packet = seed_packet(2.15, 1.41)
        untreated = heading("Plain, untreated seed", GOLD)
        self.play(FadeOut(bag, shift=UP * .22), run_time=.23)
        self.play(FadeIn(packet), FadeIn(untreated), run_time=.45)
        self.at("thickly in one tray")
        sowing = rain(2.91, 3.15, 1.04, -.13, speed=1.25, count=25, color=PAPER)
        self.add(sowing)
        schedule = calendar(-3.86, 1.48)
        weeks = heading("2–3 weeks ahead", GOLD)
        self.play(swap(untreated, weeks), FadeIn(schedule), run_time=.62)
        for day in schedule[2][:14]:
            self.play(day.animate.set_fill(GRASS), run_time=.067)
        self.at("keep it moist")
        sunshine = sun(3.98, 1.65)
        wet = rain(2.82, 1.8, 1.40, .04, count=8)
        self.remove(sowing)
        self.play(FadeOut(packet), FadeIn(sunshine), run_time=.4)
        self.add(wet)
        self.play(FadeIn(right.lawn), run_time=1.35)
        self.at("or press sod")
        sod_label = heading("Or use sod that day", GOLD)
        sod_drop = DOWN * 1.30
        sod_base = block(3.45, .25, (RIGHT_TRAY - .25, -.335), EARTH, .075).shift(-sod_drop)
        sod_lawn = right.lawn.copy().shift(-sod_drop)
        self.remove(wet)
        self.play(swap(weeks, sod_label), FadeOut(schedule), FadeOut(sunshine),
                  FadeOut(right.lawn), FadeIn(sod_base), FadeIn(sod_lawn), run_time=.62)
        self.play(sod_lawn.animate.shift(sod_drop), FadeOut(sod_base, shift=sod_drop), run_time=.8)
        self.finish()


class S05Setup(SpokenScene):
    def construct(self):
        left = tray(LEFT_TRAY, soil=False, tilted=False, notched=False)
        right = tray(RIGHT_TRAY, True, tilted=False, notched=False)
        self.add(bench(), left, right)
        self.at("fill the bare tray")
        bag = soil_bag(-4.68, 1.61)
        self.play(FadeIn(bag), run_time=.45)
        left.insert(2, left.soil_bed)
        self.play(bag.animate.rotate(-.31).shift(RIGHT * .48),
                  FadeIn(left.soil_bed), run_time=1.27)
        depth = measure_mark(-5.65, -.81, -.08)
        five = T("5 cm", 33, GOLD).move_to(point(-4.55, .92))
        self.at("five centimeters deep")
        self.play(Create(depth), FadeOut(bag), FadeIn(five), run_time=.56)
        self.at("if you grew grass")
        self.play(FadeOut(depth), FadeOut(five), run_time=.32)
        matching = heading("Same bagged soil if grown from seed", GOLD)
        self.play(FadeIn(matching), run_time=.52)
        checks = VGroup(*(stroke([(x - 1.3, -.56), (x + .95, -.56)], SILT, 7)
                          for x in (LEFT_TRAY, RIGHT_TRAY)))
        self.play(Create(checks), run_time=1.10)
        self.at("you cut a small notch")
        self.play(FadeOut(matching), FadeOut(checks), run_time=.39)
        left_tool = cutter(cup_x(LEFT_TRAY) + .29, -.55)
        right_tool = cutter(cup_x(RIGHT_TRAY) + .29, -.55)
        self.play(FadeIn(left_tool), left.outlet.animate.set_fill(opacity=1), run_time=.77)
        self.play(FadeOut(left_tool), run_time=.33)
        self.play(FadeIn(right_tool), right.outlet.animate.set_fill(opacity=1), run_time=.77)
        self.at("raise the other ends")
        self.play(FadeOut(right_tool), run_time=.33)
        self.play(Rotate(left, TRAY_TILT, about_point=tray_hinge(LEFT_TRAY)),
                  Rotate(right, TRAY_TILT, about_point=tray_hinge(RIGHT_TRAY)),
                  FadeIn(books(LEFT_TRAY), shift=RIGHT * .33),
                  FadeIn(books(RIGHT_TRAY), shift=RIGHT * .33), run_time=1.2)
        self.at("set a clear plastic cup")
        self.play(*(FadeIn(cup_outline(x), shift=UP * .39)
                    for x in (LEFT_TRAY, RIGHT_TRAY)), run_time=1.1)
        self.finish()


class S06Fair(SpokenScene):
    def construct(self):
        world = experiment()
        self.add(world)
        self.at("same slope")
        pair = heading("Same slope", GOLD)
        # Identical rise and run, with the hypotenuse parallel to each tray.
        grades = VGroup(*(shape([(cx - 2.04, 1.78), (cx + 1.36, 1.23),
                                 (cx - 2.04, 1.23)], SILT, GOLD)
                          for cx in (LEFT_TRAY, RIGHT_TRAY)))
        self.play(FadeIn(grades, shift=DOWN * .25), FadeIn(pair), run_time=.54)
        self.at("same rain")
        rain_label = heading("Same rain", BLUE)
        drops = VGroup(*(VGroup(*(shape([(cx + dx - .16, 1.36), (cx + dx - .20, 1.60),
                                        (cx + dx, 1.97), (cx + dx + .20, 1.60),
                                        (cx + dx + .16, 1.36), (cx + dx, 1.30)], BLUE)
                                  for dx in (-1.34, -.54, .26))) for cx in (LEFT_TRAY, RIGHT_TRAY)))
        self.play(swap(pair, rain_label), FadeOut(grades), FadeIn(drops), run_time=.57)
        self.play(drops.animate.shift(DOWN * .47), run_time=1.02)
        self.at("one tray is bare")
        bare = T("Bare soil", 32, PAPER).move_to(point(LEFT_TRAY - .4, 1.38))
        grass = T("Grass", 32, GREEN).move_to(point(RIGHT_TRAY - .4, 1.38))
        left_soil, right_soil = world[3][2], world[4][2]
        self.play(FadeOut(rain_label), FadeOut(drops), run_time=.28)
        self.play(FadeIn(bare), left_soil.animate.set_fill(SILT), run_time=.58)
        self.at("other has grass")
        self.play(FadeIn(grass), left_soil.animate.set_fill(SOIL),
                  right_soil.animate.set_fill(SILT), world[4].lawn.animate.set_color("#CFEB91"),
                  run_time=.82)
        self.play(right_soil.animate.set_fill(SOIL), world[4].lawn.animate.set_color(GREEN), run_time=.85)
        self.at("which cup will get")
        question = question_card("Which cup gets muddier?", size=38)
        self.play(FadeIn(question), run_time=.52)
        self.at("write the guess down")
        sheet = guess_sheet(0, 1.76)
        ink = writing(0, 1.76)
        pen = pencil(-.86, 2.15)
        self.play(FadeIn(sheet), FadeIn(pen), run_time=.38)
        self.play(Create(ink), pen.animate.shift(RIGHT * 1.38), run_time=.97)
        self.finish()


def prediction_question():
    return question_card(QUESTION, size=38)


class S07PredictQuestion(SpokenScene):
    def construct(self):
        self.add(experiment())
        self.at("for gentle rain")
        watering_can = can(LEFT_TRAY)
        self.play(FadeIn(watering_can, shift=LEFT * 1.40 + DOWN * .48),
                  run_time=2.08, rate_func=smooth)
        height = measure_mark(-5.90, .58, 1.53)
        height_text = T("About 20 cm", 32, GOLD).move_to(point(-4.44, 2.95))
        self.at("about 20 centimeters")
        self.play(GrowFromPoint(height, height.get_bottom()), FadeIn(height_text), run_time=.75)
        marker = Dot(point(-5.90, .58), radius=.096, color=GOLD)
        self.play(FadeIn(marker), run_time=.24)
        self.play(marker.animate.shift(UP * .95), run_time=1.55, rate_func=linear)
        self.at("pour two cups")
        volume = heading("2 cups over about 30 seconds", BLUE)
        self.play(FadeOut(height), FadeOut(height_text), FadeOut(marker), run_time=.32)
        self.play(FadeIn(volume), Rotate(watering_can, .22, rate_func=there_and_back), run_time=1.65)
        self.at("repeat with the same")
        same = heading("Same amount, height and speed", GOLD)
        self.play(swap(volume, same),
                  watering_can.animate.shift(RIGHT * (RIGHT_TRAY - LEFT_TRAY)), run_time=1.5)
        self.at("what do you predict")
        self.play(FadeOut(same), watering_can.animate.shift(LEFT * (RIGHT_TRAY - LEFT_TRAY)),
                  FadeIn(prediction_question()), run_time=1.12)
        self.finish()


class S08PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = {"size": 38}
    SECONDS = 4.5

    def backdrop(self):
        world = experiment()
        bob(world[4].lawn, amp=.035, speed=2.1)
        return VGroup(world, can(LEFT_TRAY))

    def finish(self):
        # This is the script's silent 4.5-second beat, with no narration tail.
        pass


def runoff(cx, color, speed=1, route=None):
    if route is None:
        route = [(cx - 1.98, .45), (cx - 1.70, .37), (cx - .78, .21),
                 (cx + .12, .06), (cx + .98, -.08), (cx + 1.71, -.33),
                 (cup_x(cx), -1.62)]
    tracks = VGroup()
    for i in range(12):
        drop = Ellipse(width=.19, height=.083, fill_color=color, fill_opacity=1, stroke_width=0)
        phase = i / 12
        def descend(m, dt, phase=phase):
            m.phase = (getattr(m, "phase", phase) + dt * .65 * speed) % 1
            t = m.phase * (len(route) - 1)
            j = int(t)
            start, end = np.array(route[j]), np.array(route[j + 1])
            p = interpolate(start, end, t - j)
            m.move_to(point(*p))
            m.set_fill(opacity=min(1, t * 1.7, (len(route) - 1 - t) * 2))
        drop.add_updater(descend, call_updater=True)
        tracks.add(drop)
    return tracks


def pour(scene, cx, watering_can, level, height, seconds, *during, storm=False):
    """Both trays share the same watering profile. Cup levels show qualitative results."""
    stream = rain(cx - 1.95, .55 if storm else .38, 1.49, .49,
                  count=19 if storm else 10, speed=3.5 if storm else 2.0)
    draining = runoff(cx, SILT if cx == LEFT_TRAY else BLUE, speed=1.45 if storm else 1)
    scene.add(stream, draining)
    scene.play(level.animate.set_value(height), Rotate(watering_can, .12, rate_func=there_and_back),
               *during, run_time=seconds, rate_func=linear)
    scene.remove(stream, draining)


def collect(scene):
    left, right = ValueTracker(0), ValueTracker(0)
    fills = VGroup(always_redraw(lambda: liquid(LEFT_TRAY, left.get_value(), True)),
                   always_redraw(lambda: liquid(RIGHT_TRAY, right.get_value(), False)))
    scene.add(fills, cup_rims())
    return left, right, fills


def cup_rims():
    return VGroup(*(cup_outline(cx)[1:] for cx in (LEFT_TRAY, RIGHT_TRAY)))


def rills():
    return VGroup(*(stroke([(LEFT_TRAY - 1.78 + dx, .41),
                            (LEFT_TRAY - .91 + dx, .19 - .05 * i),
                            (LEFT_TRAY - .45 + dx, .23 - .11 * i),
                            (LEFT_TRAY + .40, .02), (LEFT_TRAY + 1.45, -.19)],
                           EARTH, 4.5, True)
                     for i, dx in enumerate((-.17, .13, .38))))


def clock_face(x=0, y=1.40):
    origin = point(x, y)
    disc = Circle(radius=.66, fill_color="#304650", fill_opacity=1,
                  stroke_color=GLASS, stroke_width=3).move_to(origin)
    ticks = VGroup(*(Line(origin + .50 * v, origin + .59 * v, color=GLASS, stroke_width=2.4)
                     for a in np.arange(12) * TAU / 12 for v in [point(np.cos(a), np.sin(a))]))
    hand = Line(origin, origin + UP * .47, color=GOLD, stroke_width=4)
    return VGroup(disc, ticks, hand), hand, origin


def ruler(cx):
    x = cup_x(cx) + .74
    strip = block(.29, 1.18, (x, -1.86), PAPER, .025)
    ticks = VGroup(*(stroke([(x - .15, -2.43 + i * .105),
                             (x - (.00 if i % 5 == 0 else .07), -2.43 + i * .105)], EARTH, 1.8)
                     for i in range(11)))
    return VGroup(strip, ticks)


def settle(scene, heights, layers, ruler_cue, fills):
    clock, hand, center = clock_face()
    tag = heading("After 10 minutes", GOLD)
    scene.play(FadeIn(clock), FadeIn(tag), run_time=.25)
    scene.play(Rotate(hand, -TAU / 6, about_point=center), run_time=.65, rate_func=linear)
    scene.at(ruler_cue)
    scene.remove(fills)
    for cx, h, layer in zip((LEFT_TRAY, RIGHT_TRAY), heights, layers):
        scene.add(liquid(cx, h, cx == LEFT_TRAY, layer))
    scene.add(cup_rims())
    gauges = VGroup(*(ruler(cx) for cx in (LEFT_TRAY, RIGHT_TRAY)))
    scene.play(FadeIn(gauges, shift=DOWN * .23), run_time=.67)
    return VGroup(clock, tag, gauges)


class S09Reveal(SpokenScene):
    def construct(self):
        self.add(experiment())
        watering_can = can(LEFT_TRAY)
        self.add(watering_can)
        self.at("tray's runoff")
        left, right, fills = collect(self)
        pour(self, LEFT_TRAY, watering_can, left, .79, 2.22)
        muddier = T("Usually cloudier", 31, PAPER).move_to(point(LEFT_TRAY - .18, -3.03))
        self.play(FadeIn(muddier), watering_can.animate.shift(RIGHT * (RIGHT_TRAY - LEFT_TRAY)), run_time=.86)
        self.at("the grass tray's cup")
        less = T("Often less water", 31, BLUE).move_to(point(RIGHT_TRAY, -3.03))
        reveal = Succession(Wait(1.05), FadeIn(less, run_time=.55), Wait(.62), rate_func=linear)
        pour(self, RIGHT_TRAY, watering_can, right, .47, 2.22, reveal)
        self.play(FadeOut(watering_can), run_time=.60)
        self.at("where did the soil")
        q = question_card("Where did the soil in this cup come from?", size=34)
        self.play(FadeOut(muddier), FadeOut(less), run_time=.33)
        self.play(FadeIn(q), run_time=.40)
        self.at("check the guess")
        sheet = VGroup(guess_sheet(), writing())
        self.play(FadeIn(sheet, shift=DOWN * .24), run_time=.70)
        self.at("after 10 minutes")
        self.play(FadeOut(q), FadeOut(sheet), run_time=.27)
        settle(self, (.79, .47), (.19, .06), "measure the settled soil", fills)
        self.finish()


def spoonful():
    x, y = 1.50, .53
    scoop = Ellipse(width=1.55, height=.39, fill_color=GLASS, fill_opacity=1,
                    stroke_width=2, color=CARTON).move_to(point(x, y - .71))
    handle = block(2.03, .17, (x + 1.36, y - .66), GLASS, .07).rotate(.18)
    sod = shape([(x - .69, y + .21), (x + .64, y + .21), (x + .49, y - .61),
                 (x - .42, y - .64)], SOIL)
    return VGroup(handle, scoop, sod, roots(x, y + .18, 1, .72), blades(x, y + .16, 1.31, 11))


class S10StormRoots(SpokenScene):
    def construct(self):
        self.add(experiment())
        self.at("empty the cups")
        liquid_pair = VGroup(liquid(LEFT_TRAY, .79, True, .19), liquid(RIGHT_TRAY, .47, False, .06))
        self.add(liquid_pair, cup_rims())
        self.play(*(Transform(mob, liquid(cx, .013, cx == LEFT_TRAY))
                    for mob, cx in zip(liquid_pair, (LEFT_TRAY, RIGHT_TRAY))), run_time=1.1)
        self.remove(liquid_pair)
        self.at("pour two fresh cups")
        left, right, fills = collect(self)
        watering_can = can(LEFT_TRAY)
        label = heading("2 fresh cups per tray", BLUE)
        self.play(FadeIn(watering_can), FadeIn(label), run_time=.36)
        pour(self, LEFT_TRAY, watering_can, left, .87, 1.7, storm=True)
        self.at("taking about five seconds")
        timing = heading("About 5 seconds per tray", BLUE).shift(UP * .18)
        self.play(swap(label, timing), watering_can.animate.shift(RIGHT * (RIGHT_TRAY - LEFT_TRAY)),
                  run_time=.69)
        pour(self, RIGHT_TRAY, watering_can, right, .58, 1.7, storm=True)
        self.at("small channels called rills")
        self.play(FadeOut(watering_can), FadeOut(timing), run_time=.32)
        channels = rills()
        self.play(Create(channels), run_time=.73)
        rill_label = T("Rills", 32, PAPER).move_to(point(-3.42, 1.29))
        self.play(FadeIn(rill_label), run_time=.35)
        self.at("after ten minutes")
        self.play(FadeOut(rill_label), run_time=.25)
        end = settle(self, (.87, .58), (.34, .105), "measure the settled soil", fills)
        self.at("lift the grass")
        self.play(FadeOut(end), run_time=.27)
        chunk = spoonful().shift(DOWN * .62 + RIGHT * 1.23)
        self.play(FadeIn(chunk), run_time=.26)
        self.play(chunk.animate.shift(UP * 1.81 + LEFT * 1.23).scale(1.13), run_time=1.03)
        self.finish()


def section_surface(cx):
    return (cx - 2.23, .74), (cx + 1.72, .09)


def section(cx, grass=False):
    (x1, y1), (x2, y2) = section_surface(cx)
    base = -1.21
    body = shape([(x1, y1), (x2, y2), (x2, base), (x1, base)], EARTH)
    color_band = shape([(x1, y1), (x2, y2), (x2, -.23), (x1, .20)], SOIL)
    grains = texture(cx - .22, -.40, 3.60, 1.06, 40, 44, [SILT, SOIL])
    rim = stroke([(x1 - .03, y1), (x1 - .03, base), (x2 + .03, base), (x2 + .03, y2)],
                 GLASS, 4)
    lawn = blades(cx - .24, y1, 3.78)
    threads = roots(cx - .23, y1, 3.65, 1.12)
    if grass:
        for lines in (lawn, threads):
            for piece in lines:
                x = piece.get_start()[0]
                piece.shift(DOWN * (.65 * (x - x1) / (x2 - x1)))
    return VGroup(body, color_band, grains, rim, *([lawn] if grass else [])), threads


def splashes(cx):
    cloud = VGroup()
    for i in range(12):
        grain = Dot(radius=.064, color=SILT)
        def bounce(m, dt, i=i):
            m.phase = (getattr(m, "phase", (i * .37) % 1) + dt * 1.15) % 1
            x = cx - 1.92 + i * .256 + .41 * m.phase
            ground = .73 - (x - (cx - 2.23)) * .165
            m.move_to(point(x, ground + (.24 + (i % 3) * .08) * np.sin(m.phase * PI)))
            m.set_fill(opacity=min(1, m.phase * 10, (1 - m.phase) * 10))
        grain.add_updater(bounce, call_updater=True)
        cloud.add(grain)
    return cloud


class S11Why(SpokenScene):
    def construct(self):
        bare, _ = section(LEFT_TRAY)
        grass, root_net = section(RIGHT_TRAY, True)
        self.add(bench(), bare, grass, cup_outline(LEFT_TRAY), cup_outline(RIGHT_TRAY))
        self.at("leaves and stems")
        droplets = rain(RIGHT_TRAY - .25, 3.4, 2.40, .96, speed=1.96, count=28)
        leaf_drips = rain(RIGHT_TRAY - .25, 2.75, .92, .46, speed=.78, count=18)
        self.add(droplets, leaf_drips)
        leaf_text = T("Leaves soften drops", 34, GREEN).move_to(point(2.9, 2.95))
        self.play(FadeIn(leaf_text), run_time=.62)
        lawn = grass[-1]
        lean = lawn.copy()
        for blade, bent in zip(lawn, lean):
            bent.rotate(-.31, about_point=blade.get_start())
        resting = lawn.copy()
        self.play(Transform(lawn, lean), run_time=1.65)
        self.play(Transform(lawn, resting), run_time=1.62)
        self.at("roots grip the soil")
        root_label = T("Roots grip", 34, GOLD).move_to(point(2.9, 2.95))
        self.play(swap(leaf_text, root_label), Create(root_net), run_time=1.23)
        self.at("help water soak in")
        seep = VGroup(*(Arrow(point(x, .42), point(x + .16, -.71), buff=0,
                              color=BLUE, stroke_width=4, max_tip_length_to_length_ratio=.22)
                       for x in (1.55, 2.74, 3.96)))
        self.play(LaggedStart(*(GrowArrow(v) for v in seep), lag_ratio=.32), run_time=1.15)
        self.at("on bare soil")
        self.play(FadeOut(root_label), FadeOut(seep), run_time=.35)
        bare_drops = rain(LEFT_TRAY - .25, 3.65, 2.36, .48, speed=3.4)
        self.add(bare_drops, splashes(LEFT_TRAY))
        scatter = T("Drops knock grains loose", 33, PAPER).move_to(point(-3.0, 2.95))
        self.play(FadeIn(scatter), run_time=.60)
        self.at("water flowing downhill")
        transport = T("Runoff carries soil", 33, PAPER).move_to(point(-3.0, 2.95))
        (x1, y1), (x2, y2) = section_surface(LEFT_TRAY)
        spill_x = x2 + .20
        route = list(zip(np.linspace(x1 + .12, spill_x, 6),
                         np.linspace(y1 + .05, y2 + .08, 6)))
        route.extend([(spill_x, -.67), (spill_x, -1.62)])
        self.add(runoff(LEFT_TRAY, SILT, speed=1.6, route=route))
        level = ValueTracker(.04)
        self.add(always_redraw(lambda: liquid(LEFT_TRAY, level.get_value(), True)), cup_rims())
        self.play(swap(scatter, transport), level.animate.set_value(.71), run_time=2.65)
        self.finish()


def sink():
    basin = VGroup(block(4.92, .43, (0, -.78), CARTON, .16),
                   block(3.91, 1.37, (0, -1.60), "#385564", .16),
                   Ellipse(width=4.01, height=.47, fill_color="#213B49", fill_opacity=1,
                           color=GLASS, stroke_width=3).move_to(point(0, -.70)))
    tap = stroke([(-1.19, -.50), (-1.19, .92), (-1.02, 1.50), (-.48, 1.55),
                  (-.19, 1.11), (-.19, .91)], GLASS, 12, True)
    soap = VGroup(block(.67, .93, (1.60, .06), TEAL, .15),
                  block(.17, .30, (1.60, .64), GLASS),
                  block(.43, .10, (1.69, .77), GLASS, .035))
    hands = VGroup(block(1.38, .40, (-.32, -.15), SKIN, .17).rotate(-.31),
                   block(1.35, .37, (.26, -.30), "#E8AE86", .15).rotate(.18))
    bubbles = VGroup(*(Circle(radius=r, color=TEXT, stroke_width=2.1).move_to(point(x, y))
                       for x, y, r in [(-.5, .1, .10), (.1, .07, .13), (.38, .19, .088), (.62, -.05, .10)]))
    return VGroup(basin, tap, soap, hands, bubbles)


class S12Safety(SpokenScene):
    def construct(self):
        self.add(bench())
        adult_child = people(-3.65, -1.26, 1.47)
        carton = tray(2.25, tilted=False, notched=False)
        together = heading("Stay with your child", TEAL)
        self.add(adult_child, carton, together)
        self.at("you do the cutting")
        cut_label = heading("Adults cut and lift", GOLD)
        tool = cutter(4.20, -.55)
        self.play(swap(together, cut_label), FadeIn(tool),
                  carton.outlet.animate.set_fill(opacity=1), run_time=.75)
        tape = block(.28, .49, (4.01, -.58), GOLD, .055).rotate(-.15)
        self.play(FadeOut(tool), FadeIn(tape), run_time=.37)
        held = VGroup(carton, tape)
        hands = VGroup(*(block(.56, .32, (x, -1.06), SKIN, .14)
                         for x in (.26, 3.72))).set_z_index(10)
        self.play(FadeIn(hands), run_time=.20)
        self.play(held.animate.shift(UP * .60), hands.animate.shift(UP * .60), run_time=.75)
        self.at("keep small pieces")
        risk = heading("Under 4: choking risk", GOLD)
        shelf = block(3.49, .20, (2.13, .95), CARTON, .055)
        packet = seed_packet(2.04, 1.71)
        pieces = texture(3.08, 1.10, .62, .12, 12, 52, [PAPER, SILT])
        self.play(FadeOut(held), FadeOut(hands), swap(cut_label, risk), FadeIn(shelf), run_time=.61)
        self.play(FadeIn(packet, shift=UP * .65), FadeIn(pieces), run_time=1.12)
        self.at("call 911 if choking")
        emergency = heading("Call 911 if choking", RED)
        self.play(swap(risk, emergency), run_time=.53)
        self.at("never taste plants")
        warning = heading("Never taste plants, soil or seed", RED)
        self.play(swap(emergency, warning), run_time=.52)
        self.play(packet.animate.shift(LEFT * .46), run_time=.76)
        self.at("wash hands with soap")
        washing = sink()
        wash_label = heading("Wash with soap and water", BLUE)
        self.play(FadeOut(adult_child), FadeOut(shelf), FadeOut(packet), FadeOut(pieces),
                  swap(warning, wash_label), FadeIn(washing), run_time=.64)
        self.add(rain(-.22, .27, .82, -.45, speed=2.4, count=10))
        bob(washing[3], amp=.075, speed=5)
        bob(washing[4], amp=.11, speed=3.7)
        self.finish()


def cloud(x, y, color):
    return VGroup(block(1.71, .63, (x, y - .09), color, .28),
                  *(Dot(point(x + dx, y + dy), radius=r, color=color)
                    for dx, dy, r in [(-.49, .16, .31), (-.05, .28, .45), (.48, .12, .32)]))


def plan():
    board = block(4.52, 1.62, (3.78, 2.13), "#273D46", .13)
    grass = blades(2.42, 2.08, .67, 7).scale(.53, about_point=point(2.42, 2.08))
    mulch = texture(3.80, 2.22, .79, .39, 24, 19, [SOIL, SILT, PAPER])
    leaves = VGroup(*(Ellipse(width=.43, height=.18, fill_color=c, fill_opacity=1, stroke_width=0)
                      .rotate(a).move_to(point(5.15 + dx, 2.24 + dy))
                      for dx, dy, a, c in [(-.19, .04, .61, GOLD), (.17, .06, -.55, GREEN), (0, -.17, .17, SILT)]))
    names = VGroup(*(T(name, 28, TEXT).move_to(point(x, 1.75))
                     for name, x in [("Grass", 2.42), ("Mulch", 3.80), ("Leaves", 5.15)]))
    return board, (grass, mulch, leaves), names


class S13Return(SpokenScene):
    def construct(self):
        world = landscape()
        self.add(world, current())
        self.at("for an optional walk")
        clouds = cloud(-3.55, 2.54, "#667B88")
        light = sun(-4.59, 2.70)
        self.play(FadeIn(light), FadeIn(clouds, shift=RIGHT * .34), run_time=.90)
        self.at("check the weather")
        notice = T("Check the weather", 34, TEXT).move_to(point(1.02, 2.79))
        self.play(FadeIn(notice), clouds.animate.shift(LEFT * .07), run_time=.58)
        self.at("choose shade")
        shade = T("Choose shade or sun protection", 33, TEXT).move_to(notice)
        self.play(swap(notice, shade), light.animate.shift(LEFT * .48), run_time=.78)
        self.at("wait until rain stops")
        shower = rain(-2.0, 4.6, 2.04, -.20, count=23)
        self.add(shower)
        self.play(FadeOut(shade), clouds.animate.shift(LEFT * .33), run_time=.76)
        self.play(FadeOut(shower), FadeOut(clouds), run_time=.75)
        self.at("at least 30 minutes")
        face, hand, center = clock_face(-2.25, 2.45)
        wait = T("At least 30 min after thunder", 32, GOLD).move_to(point(1.58, 2.78))
        self.play(FadeIn(face), FadeIn(wait), run_time=.42)
        self.play(Rotate(hand, -PI, about_point=center), run_time=1.31, rate_func=linear)
        self.at("stay together on")
        walkers = people(-5.45, -.43, .74, walking=True)
        self.play(FadeOut(face), FadeOut(wait), FadeIn(walkers), run_time=.55)
        self.play(walkers.animate.shift(RIGHT * 1.76 + DOWN * .24), run_time=2.35, rate_func=linear)
        self.at("stay away from roads")
        danger = T("Stay back from water and drains", 33, GOLD).move_to(point(.1, 2.83))
        self.play(FadeIn(danger), walkers.animate.shift(RIGHT * 1.35), run_time=1.65)
        self.play(walkers.animate.shift(RIGHT * 1.35 + UP * .09), run_time=1.55, rate_func=linear)
        self.at("bodies of water")
        bank_edge = stroke([(-.55, -1.23), (.68, -1.28), (1.58, -1.44), (2.78, -1.74)], GOLD, 7, True)
        self.play(Create(bank_edge), run_time=1.04)
        self.at("never walk through floodwater")
        hazard = T("Never cross floodwater", 35, RED).move_to(danger)
        self.play(swap(danger, hazard), FadeOut(bank_edge), run_time=.61)
        self.play(walkers.animate.shift(RIGHT * 1.25), run_time=1.62)
        self.at("patch ask how")
        q = T("How could we fix it?", 39, GOLD).move_to(point(-2.74, 2.72))
        board, sketches, names = plan()
        self.play(FadeOut(hazard), FadeOut(light), FadeIn(q), FadeIn(board), run_time=.52)
        for picture, label in zip(sketches, names):
            self.play(FadeIn(picture, shift=UP * .14), FadeIn(label), run_time=.55)
        self.at("check for ticks")
        ticks = T("Check for ticks afterward", 32, TEXT).move_to(point(-3.09, 2.72))
        self.play(swap(q, ticks), run_time=.65)
        self.at("wash hands with soap")
        mini_sink = sink().scale(.55).move_to(point(-3.57, 1.15))
        wash = T("Wash with soap and water", 30, BLUE).move_to(point(-3.57, 3.00))
        inset = block(3.8, 2.45, (-3.57, 1.25), "#273D46", .13)
        self.play(swap(ticks, wash), FadeIn(inset), FadeIn(mini_sink), run_time=.67)
        tap_x, tap_y = mini_sink[1].get_end()[:2]
        self.add(rain(tap_x, .18, tap_y - .07, tap_y - .85, speed=1.9, count=8))
        bob(mini_sink[3], amp=.041, speed=4)
        self.finish()


class S14End(EndCard):
    LINE = "Roots and leaves hold soil in place when rain falls."
