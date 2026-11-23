"""Camouflage Hunt. The same yarn pieces move between the tray and both surfaces."""

from bp_parts import *
from bp_style import EndCard

# Color map: the four yarn colors stay fixed on grass, dirt, and in the tally.
WORMS = ("#83C167", "#B38257", "#FC6255", "#F5D547")
COLOR_NAMES = ("Green", "Brown", "Red", "Yellow")
GRASS = "#568747"
DIRT = "#946842"
PAPER = "#2D3C3C"
CREAM = "#FFF1CA"
INK = "#25302C"
SKY = "#91D7E5"
PATCH = np.array([-2.0, 0.0, 0.0])
SIDE = 4.42
TRAY_AT = np.array([SIDE, 0.02, 0.0])
LAWN_ROUNDS = ((1, 2, 5, 4), (2, 1, 4, 5), (1, 1, 5, 4))
LAWN_TOTALS = tuple(map(sum, zip(*LAWN_ROUNDS)))
DIRT_COUNTS = (4, 1, 5, 4)
QUESTION = "Which color hides best here?"


def xy(x, y):
    return np.array([x, y, 0.0])


def panel(w, h, color=PAPER, border=None):
    return RoundedRectangle(
        width=w, height=h, corner_radius=0.21, fill_color=color, fill_opacity=1,
        stroke_color=border or color, stroke_width=2 if border else 0,
    )


def shape(points, color):
    return Polygon(*[xy(x, y) for x, y in points], fill_color=color, fill_opacity=1, stroke_width=0)


def line(a, b, color=CREAM, width=4):
    return Line(xy(*a), xy(*b), stroke_color=color, stroke_width=width)


def label(text, x, y, size=32, color=TEXT):
    return T(text, size=size, color=color, weight=BOLD).move_to(xy(x, y))


def shoe():
    sole = panel(.36, .67, "#D7A86D")
    upper = panel(.29, .50, "#563F33").shift(UP * .04)
    laces = VGroup(*[line((-.075, y), (.075, y), CREAM, 2) for y in (.015, .09, .165)])
    return VGroup(sole, upper, laces).rotate(-.40)


def corners():
    return VGroup(*[
        shoe().move_to(PATCH + xy(x, y))
        for x, y in ((-3.91, -2.43), (-3.91, 2.43), (3.91, -2.43), (3.91, 2.43))
    ])


def field(ground="grass", breeze=False):
    """Overhead ground tile. Identical bounds and yarn coordinates in both hunts."""
    rng = np.random.default_rng(163)
    base = panel(8.78, 5.80, GRASS if ground == "grass" else DIRT)
    texture = VGroup()
    for y in np.linspace(-2.40, 2.20, 7):
        for x in np.linspace(-3.92, 3.92, 11):
            loc = xy(x + rng.uniform(-.10, .10), y + rng.uniform(-.13, .13))
            if ground == "grass":
                h = rng.uniform(.21, .51)
                tuft = VGroup(
                    shape([(0, 0), (-.18, h * .81), (-.052, h * .49), (.05, 0)], "#6C9C4C"),
                    shape([(-.03, 0), (.045, h), (.115, h * .64), (.065, 0)], "#86AC55"),
                    shape([(.03, 0), (.22, h * .55), (.16, h * .27), (.06, 0)], "#467444"),
                ).shift(loc)
                if breeze:
                    phase = rng.uniform(-.85, .85)
                    tuft.phase_time = 0.0
                    tuft.lean = 0.0

                    def sway(m, dt, anchor=loc + PATCH, phase=phase):
                        m.phase_time += dt
                        angle = .46 * (np.sin(1.95 * m.phase_time + phase) - np.sin(phase))
                        m.rotate(angle - m.lean, about_point=anchor)
                        m.lean = angle

                    tuft.add_updater(sway)
                texture.add(tuft)
            else:
                color = rng.choice(["#A4794E", "#805A3E", "#BE9264"])
                grain = Ellipse(width=rng.uniform(.07, .29), height=rng.uniform(.04, .105),
                                color=color, fill_opacity=1, stroke_width=0)
                texture.add(grain.rotate(rng.uniform(-1, 1)).move_to(loc))
    return VGroup(base, texture).shift(PATCH)


def dust():
    """Dust passes across the ground while the view and scattered yarn stay fixed."""
    rng = np.random.default_rng(64)
    cloud = VGroup()
    for _ in range(41):
        x, y = rng.uniform(-3.85, 3.85), rng.uniform(-2.2, 2.2)
        speed = rng.uniform(.38, .94)
        grain = Ellipse(width=rng.uniform(.13, .33), height=rng.uniform(.06, .15),
                        fill_color="#F5D3A4", fill_opacity=rng.uniform(.34, .60), stroke_width=0)
        grain.move_to(PATCH + xy(x, y))
        grain.age = 0

        def drift(m, dt, start=x, height=y, v=speed):
            m.age += dt
            offset = (start + 3.89 + v * m.age) % 7.78 - 3.89
            m.move_to(PATCH + xy(offset, height + .09 * np.sin(offset * 2 + height)))

        grain.add_updater(drift)
        cloud.add(grain)
    return cloud


def sunlight():
    """A soft moving patch of light, kept within the bounds of the ground tile."""
    beam = VGroup(*[
        Ellipse(width=w, height=h, fill_color="#F7DCA2", fill_opacity=alpha, stroke_width=0)
        for w, h, alpha in ((3.42, 5.14, .07), (3.14, 4.86, .07), (2.83, 4.54, .08), (2.48, 4.18, .10))
    ]).rotate(-.26)
    beam.age = 0.0

    def move(m, dt):
        m.age += dt
        m.move_to(PATCH + xy(2.31 * np.sin(.82 * m.age - 1.26), 0))

    move(beam, 0)
    beam.add_updater(move)
    return beam


def yarn(color, center=ORIGIN, span=.53, angle=0, broad=False):
    # The twist is schematic, with the same silhouette and outline on both backgrounds.
    path = VMobject()
    path.set_points_smoothly([xy(x, y) for x, y in [
        (-.27, -.01), (-.17, .075), (-.05, .054), (.055, -.052),
        (.153, -.064), (.27, .015),
    ]])
    rim = path.copy().set_stroke("#3B3323", width=9 if broad else 6, opacity=.38)
    path.set_stroke(color, width=7 if broad else 4.5)
    stitches = VGroup(*[
        line((x - .025, y - .025), (x + .024, y + .034), "#FFF2CA", 1.2).set_opacity(.38)
        for x, y in [(-.18, .063), (-.08, .065), (.02, -.015), (.115, -.068), (.217, -.026)]
    ])
    return VGroup(rim, path, stitches).scale(span / .54).rotate(angle).move_to(center)


def scattered():
    rng = np.random.default_rng(25)
    slots = rng.permutation(20)
    return [
        [yarn(color, PATCH + xy(-3.20 + (k % 5) * 1.59 + rng.uniform(-.19, .19),
                               1.89 - (k // 5) * 1.24 + rng.uniform(-.18, .18)),
              span=.56, angle=rng.uniform(-1.25, 1.25), broad=True)
         for k in slots[c * 5:c * 5 + 5]]
        for c, color in enumerate(WORMS)
    ]


def tray():
    outer = panel(3.74, 3.32, "#A87751", "#DBB07B")
    lining = panel(3.46, 3.05, "#3F3028")
    slots = VGroup(*[panel(3.12, .47, "#544033").shift(UP * (.99 - i * .66)) for i in range(4)])
    return VGroup(outer, lining, slots).move_to(TRAY_AT)


def sorted_yarn():
    return [
        [yarn(c, TRAY_AT + xy((j - 2) * .59, .99 - i * .66), span=.42) for j in range(5)]
        for i, c in enumerate(WORMS)
    ]


def flat(rows):
    return [piece for row in rows for piece in row]


def bird():
    tail = shape([(-.50, -.07), (-1.17, .18), (-.93, -.21), (-.48, -.29)], "#775B43")
    body = Ellipse(width=1.60, height=.67, color="#543E30", fill_opacity=1, stroke_width=0)
    belly = Ellipse(width=1.02, height=.42, color="#B67D51", fill_opacity=1, stroke_width=0).shift(RIGHT * .21 + DOWN * .098)
    head = Circle(radius=.35, color="#543E30", fill_opacity=1, stroke_width=0).move_to(xy(.62, .25))
    beak = shape([(.82, .29), (1.18, .18), (.87, .09)], "#E9BA66")
    eye = Dot(xy(.72, .32), radius=.052, color=CREAM)
    wing = shape([(.34, .00), (-.11, .48), (-.83, .38), (-.52, -.16), (-.18, -.20)], "#8E6344")
    return VGroup(tail, body, belly, head, beak, eye, wing)


def glide(mob, start, end, duration):
    wing = mob[-1]
    wing0 = wing.copy()
    wing_at = wing.get_center() - mob[1].get_center()
    delta = end - start

    def update(m, a):
        m.move_to(start + delta * a + UP * .18 * np.sin(PI * a))
        anchor = m[1].get_center()
        wing.become(wing0.copy().move_to(anchor + wing_at).rotate(
            .32 * np.sin(TAU * 2.5 * a), about_point=anchor))

    return UpdateFromAlphaFunc(mob, update, run_time=duration, rate_func=linear)


def cup():
    foot = shape([(-.70, .43), (.70, .43), (.48, -.90), (-.48, -.90)], "#5DAEBB")
    light = shape([(-.54, .35), (-.29, .35), (-.16, -.74), (-.38, -.74)], "#83C7CD")
    top = Ellipse(width=1.46, height=.46, fill_color="#183C45", fill_opacity=1,
                  stroke_color=SKY, stroke_width=4).shift(UP * .44)
    return VGroup(foot, light, top)


def timer_at():
    clock = ValueTracker(30)
    clock_face = panel(2.50, 1.06, "#29484B", "#60A7AD").move_to(xy(SIDE, 1.85))
    digits = counter("{:02.0f} s", clock, at=xy(SIDE, 1.85), size=37, color=CREAM)
    return clock, VGroup(clock_face, digits)


def notebook():
    page = panel(2.70, 1.53, "#E7CFA6").move_to(xy(SIDE, 2.55))
    lines = VGroup(*[line((SIDE - .92, y), (SIDE + .86, y), "#BA9E7B", 1.6)
                     for y in (2.15, 2.48, 2.81)])
    return VGroup(page, lines)


def write_guess(scene, duration=.95):
    mark = VMobject(stroke_color=INK, stroke_width=4)
    mark.set_points_smoothly([xy(SIDE + x, 2.62 + y) for x, y in [
        (-.85, -.12), (-.65, .12), (-.54, -.02), (-.40, .09), (-.26, -.09), (.01, .02), (.42, .07),
    ]])
    pencil = shape([(0, 0), (.11, .05), (.48, .53), (.39, .58)], "#E1AB58")
    scene.add(pencil)

    def write(m, a):
        m.move_to(mark.point_from_proportion(a), aligned_edge=DL)

    scene.play(Create(mark), UpdateFromAlphaFunc(pencil, write), run_time=duration)
    scene.play(FadeOut(pencil), run_time=.18)
    return mark


def rug():
    base = panel(2.75, 1.17, "#734F61", "#D6A996")
    diamonds = VGroup(*[
        shape([(x - .22, 0), (x, .36), (x + .22, 0), (x, -.36)], color)
        for x, color in zip((-.92, -.46, 0, .46, .92), ("#D27D65", "#DAAF76", SKY, "#DAAF76", "#D27D65"))
    ])
    return VGroup(base, diamonds).move_to(xy(SIDE, 2.45))


def prediction_world(ground, breeze=False):
    return field(ground, breeze), tray(), sorted_yarn()


def prediction_card():
    return question_card(QUESTION, y=-3.39, size=34)


def example_caption(text):
    return caption(text, size=32, y=-3.40)


class S01Hook(SpokenScene, TitleCard):
    TITLE = "The Camouflage Hunt: Parent Guide"
    LESSON = "The Camouflage Hunt"

    def construct(self):
        lawn = field(breeze=True)
        green = yarn(WORMS[0], PATCH + xy(-1.22, .14), span=.9, angle=.62, broad=True)
        red = yarn(WORMS[2], PATCH + xy(1.45, -.33), span=.9, angle=-.35, broad=True)
        hunter = bird().flip(UP).scale(.94).move_to(xy(4.42, 1.82))
        self.add(lawn, green, red, hunter)
        self.at("why are so many")
        self.play(glide(hunter, xy(4.42, 1.82), xy(1.82, 2.35), 2.59))
        self.at("others stand out")
        self.play(glide(hunter, xy(1.82, 2.35), xy(-.95, 2.45), 2.25))
        self.at("plays a bird")
        self.play(glide(hunter, xy(-.95, 2.45), xy(-4.72, 1.70), 2.7))
        self.at("you can see")
        self.play(glide(hunter, xy(-4.72, 1.70), xy(-5.41, .77), 2.5))
        self.at("change the background")
        self.play(FadeOut(hunter, shift=UP * .2), run_time=.75)
        self.finish()


class S02Title(TitleCard):
    TITLE = S01Hook.TITLE
    LESSON = S01Hook.LESSON

    def construct(self):
        title = T(self.TITLE, size=40, color=CREAM, font=TITLE_FONT).move_to(xy(-.55, 3.36))
        self.add(field(breeze=True))
        shoes = corners()
        self.play(FadeIn(shoes), run_time=.45)
        self.play(FadeIn(title, shift=UP * .1), run_time=.43)
        self.wait(max(.1, self.narration_s - self.elapsed()))


def payoff_icons():
    bubble = VGroup(panel(.87, .64, "#485D48"), label("?", 0, 0, 37, CREAM))
    lens = VGroup(Circle(radius=.24, stroke_color=SKY, stroke_width=6), line((.17, -.17), (.40, -.40), SKY, 7))
    bars = VGroup(*[panel(.13, h, color).move_to(xy((i - 1.5) * .21, h / 2))
                    for i, (h, color) in enumerate(zip((.22, .32, .60, .51), WORMS))])
    flip = VGroup(panel(.38, .42, GRASS).shift(LEFT * .39), panel(.38, .42, DIRT).shift(RIGHT * .39),
                  Arrow(LEFT * .18, RIGHT * .19, buff=0, color=CREAM, stroke_width=3, max_tip_length_to_length_ratio=.32))
    return (bubble, lens, bars, flip)


class S03Payoff(SpokenScene):
    def construct(self):
        self.add(field(breeze=True), corners())
        worms = scattered()
        for row in worms:
            self.add(row[0])
        self.at("what does your child")
        for cue, icon, text, y in zip(
            ("practice making", "look closely", "sort their finds", "check what changes"),
            payoff_icons(), ("Predict", "Look closely", "Sort and count", "Test a change"),
            (1.85, .63, -.63, -1.85),
        ):
            icon.move_to(xy(3.05, y))
            name = label(text, 3.79, y, 30).align_to(xy(3.79, y), LEFT)
            self.at(cue)
            self.play(FadeIn(icon, shift=RIGHT * .14), run_time=.28)
            self.play(FadeIn(name), run_time=.22)
        self.finish()


def scissors():
    holes = VGroup(*[Circle(radius=.20, color="#D67558", stroke_width=9).move_to(xy(-.42, y)) for y in (-.25, .25)])
    blades = VGroup(
        shape([(-.35, .19), (.04, .03), (.83, -.28), (.68, -.34), (-.10, -.09)], "#BDD8D4"),
        shape([(-.35, -.19), (.04, -.03), (.83, .28), (.68, .34), (-.10, .09)], "#E0E9D9"),
    )
    rivet = Dot(radius=.06, color="#485958")
    return VGroup(holes, blades, rivet)


def workbench():
    board = panel(7.60, 4.93, "#674D3D", "#C49364").move_to(PATCH)
    rows = [[yarn(c, PATCH + xy(-2.45 + j * 1.20, 1.21 - i * .88), span=.82, broad=True)
             for j in range(5)] for i, c in enumerate(WORMS)]
    return board, rows


class S04Prep(SpokenScene):
    def construct(self):
        lawn = field(breeze=True)
        shoes = corners()
        board, rows = workbench()
        shears = scissors().scale(1.1).move_to(xy(SIDE, .31))
        strands = []
        for i, color in enumerate(WORMS):
            strand = VMobject(stroke_width=8, stroke_color=color)
            strand.set_points_smoothly([
                PATCH + xy(x, 1.21 - i * .88 + .12 * np.sin(3 * x))
                for x in np.linspace(-3, 3, 40)
            ])
            strands.append(strand)
        self.add(lawn, board, *strands, shears)
        self.at("cut the yarn")
        self.play(shears.animate.move_to(PATCH + xy(-.42, 1.45)), run_time=.80)
        self.play(shears[-2][0].animate.rotate(.40, about_point=shears[-1].get_center()),
                  shears[-2][1].animate.rotate(-.40, about_point=shears[-1].get_center()),
                  rate_func=there_and_back, run_time=.65)
        self.play(FadeOut(strands[0]), LaggedStart(*[FadeIn(p) for p in rows[0]], lag_ratio=.16),
                  shears.animate.move_to(xy(SIDE, .31)), run_time=.85)
        self.at("each about five")
        length = boxed_label("5 cm", size=32, color=CREAM).move_to(xy(SIDE, -.96))
        self.play(FadeIn(length), run_time=.38)
        for i, cue in enumerate(("five brown", "five red", "five yellow"), start=1):
            self.at(cue)
            self.play(shears.animate.move_to(PATCH + xy(-.41, 1.49 - i * .88)), run_time=.19)
            pivot = shears[-1].get_center()
            self.play(shears[-2][0].animate.rotate(.42, about_point=pivot),
                      shears[-2][1].animate.rotate(-.42, about_point=pivot),
                      rate_func=there_and_back, run_time=.19)
            self.play(FadeOut(strands[i]), LaggedStart(*[FadeIn(p) for p in rows[i]], lag_ratio=.15),
                      run_time=.27)
        self.at("mark out a lawn")
        self.play(FadeOut(VGroup(board, *flat(rows), shears, length)), run_time=.61)
        start = VGroup(*[shoe().scale(.86).move_to(PATCH + xy(x, y))
                         for x, y in ((-.6, -.54), (-.6, .54), (.6, -.54), (.6, .54))])
        self.play(Transform(start, shoes), run_time=.85)
        self.at("meters on each")
        measure = DoubleArrow(xy(-5.86, -3.09), xy(1.86, -3.09), buff=0, color=CREAM,
                              max_tip_length_to_length_ratio=.04)
        dimension = label("2 m × 2 m", SIDE, -.91, 34, CREAM)
        side_measure = DoubleArrow(xy(-6.66, -2.44), xy(-6.66, 2.44), buff=0, color=CREAM,
                                   max_tip_length_to_length_ratio=.052)
        self.play(GrowFromCenter(measure), GrowFromCenter(side_measure), run_time=.44)
        self.play(FadeIn(dimension), run_time=.36)
        self.at("use four shoes")
        self.play(LaggedStart(*[Indicate(s, color=CREAM, scale_factor=1.18) for s in start],
                              lag_ratio=.18), run_time=.88)
        self.finish()


def fence():
    rails = VGroup(*[line((2.53, -2.68), (2.53, 2.62), "#CDA275", 8),
                     line((2.73, -2.68), (2.73, 2.62), "#A97856", 5)])
    pegs = VGroup(*[panel(.32, .21, "#E6CBA0").move_to(xy(2.61, y)) for y in np.linspace(-2.55, 2.54, 9)])
    return VGroup(rails, pegs)


def person(color):
    head = Circle(radius=.22, fill_opacity=1, color="#E9B489", stroke_width=0).shift(UP * .67)
    hair = shape([(-.22, .69), (-.19, .85), (.01, .92), (.18, .80), (.21, .66), (-.04, .76)], "#563E32")
    top = panel(.60, .57, color).shift(UP * .17)
    legs = VGroup(line((-.12, -.06), (-.18, -.52), "#435561", 11),
                  line((.12, -.06), (.20, -.52), "#435561", 11))
    arm = line((.23, .26), (.48, .04), "#E9B489", 10)
    return VGroup(legs, top, head, hair, arm)


def indoor_pet():
    house = VGroup(panel(2.82, 1.82, "#AD7258"), shape([(-1.58, .9), (0, 1.80), (1.58, .9)], "#D9A779"),
                   panel(1.68, 1.26, "#463A41").shift(DOWN * .04))
    pet = VGroup(shape([(-.43, .05), (-.44, .55), (-.08, .30), (.14, .31), (.42, .55), (.45, .02)], "#E2BB88"),
                 Ellipse(width=.91, height=.57, fill_opacity=1, color="#E2BB88", stroke_width=0),
                 Dot(xy(-.19, .11), radius=.038, color=INK), Dot(xy(.19, .11), radius=.038, color=INK),
                 Dot(xy(0, -.043), radius=.047, color="#A56E61"))
    return VGroup(house, pet.shift(DOWN * .18)).scale(.68).move_to(xy(SIDE, 1.35))


def wash():
    basin = panel(3.00, 2.70, "#426367", "#80B8B1").move_to(xy(SIDE, .38))
    faucet = VGroup(ArcBetweenPoints(xy(SIDE + .52, 1.28), xy(SIDE, 1.27), angle=PI,
                                     stroke_color="#C7DCD0", stroke_width=12),
                    line((SIDE + .52, 1.28), (SIDE + .52, .99), "#C7DCD0", 11))
    hands = VGroup(*[panel(.43, 1.19, "#E7AE84").rotate(a).move_to(xy(SIDE + x, .27))
                     for x, a in ((-.36, -.88), (.30, .88))])
    drops = VGroup(*[Dot(xy(SIDE + x, y), radius=.055, color=SKY)
                     for x, y in ((0, 1.00), (-.08, .78), (.08, .56), (-.12, .39))])
    return VGroup(basin, faucet, hands, drops).move_to(xy(4.65, .38))


class S05Safety(SpokenScene):
    def construct(self):
        path = panel(1.37, 5.79, "#555960").move_to(xy(5.77, 0))
        stripe = DashedLine(xy(5.77, -2.56), xy(5.77, 2.56), dash_length=.23, stroke_color="#D1BA86")
        grownup = person("#E2AD62").flip(UP).scale(1.15).move_to(xy(.32, .63))
        child = person("#77BBC7").flip(UP).scale(.72).move_to(xy(1.39, .35))
        hazard = shape([(-.24, -.12), (.29, -.14), (.13, .24)], "#C8E1CF").move_to(xy(1.92, -.80))
        self.add(field(breeze=True), corners(), fence(), path, stripe, hazard, child, grownup)
        self.at("check the patch")
        self.play(grownup.animate.shift(DOWN * .34), run_time=1.24)
        self.at("choose a spot")
        clear_spot = grownup.copy().shift(LEFT * 2.62 + UP * .17)
        arm = clear_spot[-1]
        arm.rotate(-1.03, about_point=arm.get_start())
        self.play(Transform(grownup, clear_spot), child.animate.shift(LEFT * 2.58), run_time=1.28)
        self.at("hunt in shoes")
        road = VGroup(path, stripe)
        self.play(FadeOut(road), run_time=.33)
        footwear = VGroup(shoe(), shoe()).arrange(RIGHT, buff=.22).scale(1.65).move_to(xy(SIDE, 1.90))
        soft = yarn(WORMS[1], xy(SIDE, .40), span=1.98, broad=True)
        self.play(FadeIn(footwear), run_time=.45)
        self.at("use only soft yarn")
        self.play(Create(soft), run_time=.68)
        self.at("keep it away")
        warning = boxed_label("Under 4: choking hazard", size=32, color=CREAM, pad=.12).move_to(xy(-.5, -3.34))
        self.play(FadeIn(warning), run_time=.43)
        self.at("call 911 if choking")
        emergency = boxed_label("Call 911 if choking.", size=32, color=CREAM, pad=.12).move_to(warning)
        self.play(swap(warning, emergency), run_time=.52)
        self.at("keep pets indoors")
        house = indoor_pet()
        self.play(FadeOut(VGroup(emergency, footwear, soft)), FadeIn(house), run_time=.50)
        self.at("find all 20 pieces")
        box = tray().scale(.69).move_to(xy(SIDE, -1.07))
        pieces = VGroup(*flat(sorted_yarn())).scale(.69).move_to(box)
        self.play(FadeIn(box), LaggedStart(*[FadeIn(p, shift=DOWN * .13) for p in pieces], lag_ratio=.019), run_time=.83)
        self.at("wash hands afterward")
        sink = wash()
        self.play(FadeOut(VGroup(house, box, pieces)), FadeIn(sink), run_time=.37)
        self.play(sink[-2].animate.shift(RIGHT * .14), sink[-1].animate.shift(DOWN * .24),
                  rate_func=there_and_back, run_time=1.02)
        self.finish()


class S06PredictAndHunt(SpokenScene):
    def construct(self):
        lawn, box, rows = prediction_world("grass", breeze=True)
        shoes = corners()
        samples = VGroup(*[row[2] for row in rows])
        self.add(lawn, shoes, box, samples)
        self.at("one worm of each")
        self.play(LaggedStart(*[p.animate.scale(1.65) for p in samples], lag_ratio=.18), run_time=1.13)
        self.at("if you were a bird")
        hunter = bird().move_to(PATCH + xy(.19, .83))
        self.play(FadeIn(hunter, shift=LEFT * .44), run_time=.58)
        q = question_card("Which color would you find first?", y=-3.36, size=34)
        self.play(FadeIn(q), run_time=.43)
        self.at("write down their guess")
        page = notebook()
        self.play(FadeOut(q), FadeIn(page), run_time=.27)
        mark = write_guess(self, duration=.75)
        self.at("turn away")
        turn = hunter.copy().flip(UP).shift(LEFT * 2)
        self.play(Transform(hunter, turn), FadeOut(VGroup(page, mark)), run_time=.52)
        self.at("scatter all 20")
        self.remove(samples, *samples)
        full = flat(sorted_yarn())
        self.add(*full)
        targets = flat(scattered())
        self.play(LaggedStart(*[Transform(a, b) for a, b in zip(full, targets)], lag_ratio=.045),
                  FadeOut(hunter, shift=LEFT * .3), box.animate.move_to(TRAY_AT), run_time=1.89)
        self.finish()


def take_piece(piece, vessel):
    rim = vessel[-1].get_center()
    path = ArcBetweenPoints(piece.get_center(), rim, angle=-.27)
    return Succession(MoveAlongPath(piece, path, run_time=.81),
                      FadeOut(piece, shift=DOWN * .18, scale=.62, run_time=.19))


def sort_from_field(scene, pieces, targets, caught, duration, show_caught=True):
    moves = []
    for i, (row, slots) in enumerate(zip(pieces, targets)):
        for j, (piece, slot) in enumerate(zip(row, slots)):
            if j < caught[i]:
                if show_caught:
                    moves.append(FadeIn(slot, shift=DOWN * .13))
            else:
                moves.append(ReplacementTransform(piece, slot))
    scene.play(LaggedStart(*moves, lag_ratio=.045), run_time=duration)


def round_table():
    board = panel(12.30, 5.80, PAPER, "#547371")
    xs = (-1.87, .45, 2.78, 5.03)
    headings = VGroup(*[label(t, x, 1.57, 31, CREAM)
                        for t, x in zip(("Round 1", "Round 2", "Round 3", "Total"), xs)])
    title = label("Example · Grass", 0, 2.50, 36, CREAM)
    keys = [label(name, -5.40, .73 - i * .90, 32, c).align_to(xy(-5.40, 0), LEFT)
            for i, (name, c) in enumerate(zip(COLOR_NAMES, WORMS))]
    columns = [
        [label(str(value), x, .73 - i * .90, 36) for i, value in enumerate(counts)]
        for x, counts in zip(xs, (*LAWN_ROUNDS, LAWN_TOTALS))
    ]
    return board, title, headings, keys, columns


class S07CountAndRepeat(SpokenScene):
    def construct(self):
        lawn = field(breeze=True)
        shoes = corners()
        pieces = scattered()
        vessel = cup().scale(1.16).move_to(xy(SIDE, -.20))
        clock, face = timer_at()
        self.add(lawn, shoes, *flat(pieces), vessel, face)
        self.at("give your child")
        self.play(vessel.animate.shift(UP * .09), run_time=.60)
        self.at("put worms in")
        caught = [pieces[c][i] for i in range(5) for c in (2, 3, 1, 0)
                  if i < LAWN_ROUNDS[0][c]]
        first_duration = self.t_of("red and yellow usually") - .2 - self.elapsed()
        last_duration = len(caught[6:]) * .48
        remaining = 30 * last_duration / (first_duration + last_duration)
        self.play(Succession(*[take_piece(p, vessel) for p in caught[:6]]),
                  UpdateFromAlphaFunc(clock, lambda m, a: m.set_value(np.ceil(interpolate(30, remaining, a))),
                                      rate_func=linear),
                  run_time=first_duration)
        self.at("red and yellow usually")
        self.play(Succession(*[take_piece(p, vessel) for p in caught[6:]]),
                  UpdateFromAlphaFunc(clock, lambda m, a: m.set_value(np.ceil(remaining * (1 - a))),
                                      rate_func=linear),
                  run_time=last_duration)
        self.at("green and brown")
        left = [p for i in (0, 1) for p in pieces[i][LAWN_ROUNDS[0][i]:]]
        self.play(LaggedStart(*[Indicate(p, scale_factor=1.40, color=p[1].get_stroke_color()) for p in left],
                              lag_ratio=.15), run_time=1.36)
        self.at("record the count")
        tray_scale = .85
        tray_center = xy(4.05, TRAY_AT[1])
        box = tray().scale(tray_scale).move_to(tray_center)
        targets = sorted_yarn()
        for piece in flat(targets):
            piece.scale(tray_scale).move_to(tray_center + (piece.get_center() - TRAY_AT) * tray_scale)
        self.play(FadeOut(VGroup(face, vessel)), run_time=.30)
        self.play(FadeIn(box), run_time=.32)
        round_one = label("Round 1 · Example", SIDE, 2.47, 30, CREAM)
        found = label("Found", 6.17, 1.94, 28, CREAM)
        count_labels = VGroup(*[label(str(n), found.get_x(), row[0].get_y(), 28)
                                for n, row in zip(LAWN_ROUNDS[0], targets)])
        caught_in_tray = [p for row, n in zip(targets, LAWN_ROUNDS[0]) for p in row[:n]]
        self.play(FadeIn(round_one), FadeIn(found), FadeIn(count_labels),
                  LaggedStart(*[FadeIn(p) for p in caught_in_tray], lag_ratio=.03), run_time=.48)
        self.at("recover every piece")
        self.play(FadeOut(VGroup(round_one, found, count_labels)), run_time=.26)
        sort_from_field(self, pieces, targets, LAWN_ROUNDS[0], 1.55, show_caught=False)
        self.at("play three rounds")
        board, title, heads, keys, columns = round_table()
        self.play(FadeIn(board), run_time=.19)
        self.remove(lawn, shoes, box, *flat(targets))
        self.play(FadeIn(title), FadeIn(heads), *[FadeIn(k) for k in keys],
                  *[FadeIn(v) for v in columns[0]], run_time=.19)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * .09) for v in columns[1]], lag_ratio=.12), run_time=.26)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * .09) for v in columns[2]], lag_ratio=.12), run_time=.27)
        self.at("then total the counts")
        gold_column = panel(1.08, 3.61, "#666044").move_to(xy(5.03, -.62))
        self.play(FadeIn(gold_column), run_time=.23)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * .13) for v in columns[3]], lag_ratio=.12), run_time=.52)
        self.finish()


class S08PredictQuestion(SpokenScene):
    def construct(self):
        lawn, box, rows = prediction_world("grass")
        self.add(lawn, box, *flat(rows))
        self.at("choose bare dirt")
        dirt = field("dirt")
        self.play(FadeIn(dirt), run_time=1.12)
        self.remove(lawn)
        air = VGroup(sunlight(), dust())
        self.add(air)
        option = rug()
        self.at("patterned rug")
        self.play(FadeIn(option, shift=UP * .12), run_time=.48)
        self.at("before you scatter")
        self.play(LaggedStart(*[Indicate(VGroup(*row), color=WORMS[i], scale_factor=1.14)
                                for i, row in enumerate(rows)], lag_ratio=.44), run_time=2.5)
        self.at("will hide best here")
        q = prediction_card()
        self.play(FadeIn(q), run_time=.47)
        self.at("write down their guess")
        page = notebook()
        self.play(FadeOut(option), run_time=.25)
        self.play(FadeIn(page), run_time=.25)
        mark = write_guess(self, duration=1.0)
        self.at("make your own prediction")
        self.play(FadeOut(VGroup(page, mark)), run_time=.52)
        self.wait(max(.06, self.narration_s - self.elapsed() - .07))
        self.play(FadeOut(air), run_time=.38)
        self.finish()


class S09PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        dirt, box, rows = prediction_world("dirt")
        self.add(dirt, box, *flat(rows), prediction_card())
        self.wait(4.5)


def comparison_ledgers():
    lawn = Ledger([(name, str(value), c) for name, value, c in zip(COLOR_NAMES, LAWN_TOTALS, WORMS)],
                  top_left=(2.67, 1.83), title="Grass · 3 rounds", row_h=.51, key_w=2.17, width=3.58, size=28)
    dirt = Ledger([(name, str(value), c) for name, value, c in zip(COLOR_NAMES, DIRT_COUNTS, WORMS)],
                  top_left=(2.67, -.91), title="Dirt · 1 round", row_h=.51, key_w=2.17, width=3.58, size=28)
    for ledger in (lawn, dirt):
        ledger[0].set_color(CREAM)
    return lawn, dirt


class S10Reveal(SpokenScene):
    def construct(self):
        ground, box, rows = prediction_world("dirt")
        self.add(ground, sunlight(), dust(), box, *flat(rows))
        self.at("scatter the same worms")
        targets = scattered()
        self.play(LaggedStart(*[Transform(p, target) for p, target in zip(flat(rows), flat(targets))],
                              lag_ratio=.038), run_time=1.75)
        self.at("run another")
        clock, face = timer_at()
        vessel = cup().scale(.87).move_to(xy(SIDE, -.52))
        self.play(FadeOut(box), run_time=.24)
        self.play(FadeIn(face), FadeIn(vessel), run_time=.25)
        caught = [rows[c][i] for i in range(5) for c in (2, 0, 3, 1) if i < DIRT_COUNTS[c]]
        paths = [ArcBetweenPoints(p.get_center(), vessel[-1].get_center(), angle=-.24) for p in caught]
        transfers = [Succession(MoveAlongPath(p, path, run_time=.30), FadeOut(p, run_time=.10))
                     for p, path in zip(caught, paths)]
        self.play(clock.animate(run_time=2.12, rate_func=linear).set_value(0),
                  LaggedStart(*transfers, lag_ratio=.31), run_time=2.12)
        self.at("count by color")
        self.play(FadeOut(VGroup(face, vessel)), run_time=.26)
        self.play(FadeIn(box), run_time=.25)
        self.at("find every leftover")
        slots = sorted_yarn()
        sort_from_field(self, rows, slots, DIRT_COUNTS, 1.95)
        self.at("check your guesses")
        lawn, dirt = comparison_ledgers()
        group = VGroup(box, *flat(slots))
        self.play(FadeOut(group), run_time=.31)
        paper = panel(3.90, 6.39, PAPER, "#547371").move_to(xy(4.52, -.23))
        example = label("Example", SIDE, 2.53, 33, CREAM)
        self.play(FadeIn(paper), FadeIn(example), run_time=.32)
        self.play(FadeIn(lawn), FadeIn(dirt), run_time=.32)
        self.play(LaggedStart(*[table.reveal(i) for i in range(4) for table in (lawn, dirt)],
                              lag_ratio=.13), run_time=1.0)
        self.at("found least often")
        self.play(*[table.mark(i) for table, counts in ((lawn, LAWN_TOTALS), (dirt, DIRT_COUNTS))
                    for i, value in enumerate(counts) if value == min(counts)], run_time=.64)
        self.at("brown often hides")
        match_x, match_y = -2.92, .40
        red = yarn(WORMS[2], xy(match_x + 1.70, match_y), span=1.30, angle=.13, broad=True)
        brown = yarn(WORMS[1], xy(match_x, match_y), span=1.30, angle=-.32, broad=True)
        self.play(FadeIn(brown), run_time=.35)
        focus = Circle(radius=.91, stroke_color=CREAM, stroke_width=5, fill_color="#FFF1CA",
                       fill_opacity=.09).move_to(brown)
        self.play(Create(focus), run_time=.42)
        self.play(FadeIn(red), run_time=.52)
        self.at("harder to spot")
        self.play(FadeOut(focus), run_time=.45)
        self.finish()


def survivors(counts, center):
    worms = []
    for i, (color, n) in enumerate(zip(WORMS, counts)):
        row = VGroup(*[yarn(color, center + xy(-1.21 + j * .64, .98 - i * .66), span=.51, broad=True)
                       for j in range(5 - n)])
        worms.append(row)
    return worms


class S11Debrief(SpokenScene):
    def construct(self):
        comparison = TwoPanel("Grass", "Dirt", colors=("#8CB272", "#D5A16F"), top=2.90, bottom=-2.65, size=35)
        comparison.left_head.set_color(CREAM)
        comparison.right_head.set_color(CREAM)
        comparison.left_frame.set_fill(GRASS, opacity=.18)
        comparison.right_frame.set_fill(DIRT, opacity=.20)
        parents = survivors(LAWN_ROUNDS[0], comparison.area("left")[0])
        dirt_survivors = survivors(DIRT_COUNTS, comparison.area("right")[0])
        self.add(comparison)
        self.at("which worms would")
        groups = [row for table in (parents, dirt_survivors) for row in table if len(row)]
        self.play(comparison.left_frame.animate.set_fill(GRASS, opacity=.67),
                  comparison.right_frame.animate.set_fill(DIRT, opacity=.78),
                  LaggedStart(*[FadeIn(row, shift=UP * .13) for row in groups], lag_ratio=.19),
                  run_time=2.5)
        self.at("real animals can pass")
        self.play(FadeOut(VGroup(*dirt_survivors)), run_time=.25)
        grass_head = label("Grass survivors", -3.30, 2.45, 34, CREAM)
        young_head = label("Their young", 3.30, 2.45, 34, CREAM)
        self.play(swap(comparison.left_head, grass_head), swap(comparison.right_head, young_head),
                  comparison.right_frame.animate.set_fill(GRASS, opacity=.67).set_stroke("#8CB272"),
                  run_time=.52)
        inherited = [
            [yarn(color, xy(2.08 + j * .67, 1.31 - i * .66), span=.44, broad=True)
             for j in range(len(row))]
            for i, (color, row) in enumerate(zip(WORMS, parents))
        ]
        self.play(LaggedStart(*[TransformFromCopy(parent, baby)
                                for a, b in zip(parents, inherited) for parent, baby in zip(a, b)],
                              lag_ratio=.155), run_time=2.22)
        self.at("with a matching color")
        rule = example_caption("If survivors have more young")
        self.play(FadeIn(rule), run_time=.44)
        self.at("survive more often")
        extra_green = [p.copy().move_to(xy(2.08 + j * .67, .97)) for j, p in enumerate(inherited[0])]
        self.play(LaggedStart(*[TransformFromCopy(p, q) for p, q in zip(parents[0], extra_green)], lag_ratio=.30),
                  run_time=1.0)
        total_survivors = sum(map(len, parents))
        total_young = sum(map(len, inherited)) + len(extra_green)
        before = label(f"{len(parents[0])} of {total_survivors} green", -3.3, -2.16, 31, CREAM)
        after = label(f"{len(inherited[0]) + len(extra_green)} of {total_young} green", 3.3, -2.16, 31, CREAM)
        tracks = VGroup(*[panel(3.75, .41, "#233B2E").move_to(xy(x, -1.63)) for x in (-3.30, 3.30)])
        proportions = (len(parents[0]) / total_survivors, (len(inherited[0]) + len(extra_green)) / total_young)
        fills = VGroup(*[panel(3.55 * fraction, .23, WORMS[0]).move_to(track.get_left() + RIGHT * .10, aligned_edge=LEFT)
                         for track, fraction in zip(tracks, proportions)])
        self.play(FadeIn(tracks), run_time=.22)
        self.play(*[GrowFromEdge(fill, LEFT) for fill in fills], FadeIn(before), FadeIn(after), run_time=.93)
        self.finish()


class S12End(EndCard):
    LINE = "Colors that blend into the background are harder to spot."
