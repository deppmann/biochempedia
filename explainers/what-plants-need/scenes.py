"""A windowsill experiment, drawn as one continuous set of paper-cup diagrams."""
from bp_parts import *
from bp_style import EndCard

# Light: yellow; water: blue; green seedlings: green; dark-grown seedlings: pale.
# Mix: brown; room and tools: slate; prediction: orange; comparison: gold.
# Stored food and sugar: pink; safety: red; condition labels: white.
PALE = "#CDD6A0"
SOIL = "#8B6B4B"
DAMP = "#4E382B"
ORANGE = "#F29E4C"
PINK = "#E49BC1"
PAPER = "#CCB99E"
INK = "#28333C"
SKY = "#335368"
SKY_LIGHT = "#456A7D"
WOOD = "#555260"
DOOR = "#3C3948"
SKIN = "#C68E75"
TAPE = "#3D3D46"

XS = (-4.65, -1.55, 1.55, 4.65)
TEST_XS = (-5.02, -2.18, 2.18, 5.02)
NAMES = ("light +\nwater", "light,\nno water", "dark +\nwater", "dark,\nno water")
RIM = -0.53
PREDICTION = "Shorter, same, or taller?"
CARD = {"size": 38, "y": -3.16, "color": ORANGE}


def pt(x, y):
    return np.array([x, y, 0.0])


def shape(points, color, edge=None, stroke=2):
    return Polygon(*(pt(x, y) for x, y in points), fill_color=color, fill_opacity=1,
                   stroke_color=edge or color, stroke_width=stroke if edge else 0)


def block(x, y, w, h, color, edge=None, radius=0):
    kind = RoundedRectangle if radius else Rectangle
    options = {"corner_radius": radius} if radius else {}
    return kind(width=w, height=h, fill_color=color, fill_opacity=1,
                stroke_color=edge or color, stroke_width=2 if edge else 0,
                **options).move_to(pt(x, y))


def disk(x, y, r, color):
    return Dot(pt(x, y), radius=r, color=color, stroke_width=0)


def oval(x, y, w, h, color, angle=0):
    return Ellipse(width=w, height=h, fill_color=color, fill_opacity=1,
                   stroke_width=0).rotate(angle).move_to(pt(x, y))


def label(text, x=0, y=3.16, size=38, color=TEXT):
    return T(text, size, color, weight=BOLD).move_to(pt(x, y))


def sun(x, y, r=0.36):
    rays = VGroup(*[Line(RIGHT * r * 1.42, RIGHT * r * 1.86, color=YELLOW,
                         stroke_width=4).rotate(a, about_point=ORIGIN)
                    for a in np.linspace(0, TAU, 8, endpoint=False)])
    return VGroup(disk(0, 0, r, YELLOW), rays).move_to(pt(x, y))


def daylight(x=0, width=12.7, open_window=False):
    """The same slate-blue sash and deep sill throughout the film."""
    left, right = x - width / 2, x + width / 2
    return VGroup(
        block(x, 0.18, width, 4.92, INK),
        block(x, 0.18, width - 0.25, 4.66, SKY),
        shape([(left + .15, -.27), (right - .15, 1.37), (right - .15, 2.16),
               (left + .15, .52)], SKY_LIGHT),
        block(x, .18, .13, 4.68, INK),
        block(x, .47, width, .11, INK),
        *([] if open_window else [sun(left + 1.1, 1.64)]),
        shape([(left + .15, -2.13), (right - .15, -2.13), (right + .13, -2.53),
               (left - .13, -2.53)], "#666778"),
        block(x, -2.62, width + .26, .18, INK),
        *([shape([(left + .17, -2.11), (left + 1.7, -1.44), (left + 1.7, 2.04),
                  (left + .17, 2.5)], "#202E3C", GREY)] if open_window else []),
    )


def cupboard():
    base = VGroup(block(3.6, .18, 6.02, 4.94, WOOD, radius=.12),
                  block(3.6, .15, 5.64, 4.50, "#1E232F"),
                  block(3.6, -2.27, 5.66, .24, "#71707E"),
                  block(3.6, -2.54, 6.02, .34, DOOR))
    door = block(3.6, .18, 5.82, 4.72, DOOR, radius=.09)
    inset = block(3.6, .18, 5.39, 4.26, "#5A5567", radius=.08)
    handle = block(1.04, .18, .12, .56, PAPER, radius=.05)
    return base, VGroup(door, inset, handle).set_z_index(5)


def door_ajar():
    return VGroup(shape([(5.53, -2.07), (6.54, -2.18), (6.54, 2.53),
                         (5.53, 2.05)], DOOR, GREY),
                  block(5.72, .18, .07, .37, PAPER, radius=.03)).set_z_index(5)


def tray():
    return VGroup(
        shape([(-6.14, -2.06), (6.14, -2.06), (6.42, -2.47), (-6.42, -2.47)], "#486D76"),
        block(0, -2.51, 12.84, .11, "#324C5D", radius=.045),
    )


# height, stem width, leaf span, colour, amount of lean
PLANTS = {
    "young": (.92, 8, .47, GREEN, .02),
    "strong": (1.27, 10, .64, GREEN, .02),
    "tall": (2.70, 8, .53, GREEN, .04),
    "thin": (2.70, 4, .43, GREEN, .08),
    "pale": (2.70, 4, .43, PALE, .13),
    "lean": (2.82, 4, .43, PALE, .43),
    "weak": (2.67, 4, .38, PALE, .76),
    "dry": (1.17, 7, .48, GREEN, .96),
}


def seedling(state, x, y, scale=1, direction=1, phase=0):
    h, thick, leaf, color, lean = PLANTS[state]
    tip = pt(direction * (.77 * h * lean + phase), h * (1 - .51 * lean))
    stem = CubicBezier(ORIGIN, pt(-.06 * direction, h * .49),
                       pt(direction * .35 * h * lean, h * 1.07), tip,
                       stroke_color=color, stroke_width=thick)
    leaves = VGroup()
    for side in (-1, 1):
        angle = PI / 2 + side * (-1.02 - .9 * lean)
        reach = pt(np.cos(angle), np.sin(angle)) * leaf * .5
        center = tip + reach
        leaves.add(oval(center[0], center[1], leaf, leaf * .48, color, angle))
    return VGroup(stem, leaves).scale(scale, about_point=ORIGIN).shift(pt(x, y))


def sprouts(x, state, rim=RIM, scale=1, phase=0):
    return VGroup(*[seedling(state, x + dx * scale, rim + dy * scale,
                             scale * k, direction if state != "weak" else 1, phase)
                    for dx, dy, k, direction in ((-.48, .02, .7, -1),
                                                  (-.08, .08, 1, 1),
                                                  (.40, .01, .83, 1))]).set_z_index(1)


def cup(x, mix=DAMP, rim=RIM, scale=1):
    artwork = VGroup(
        shape([(-1.02, .015), (1.02, .015), (.78, -1.69), (-.78, -1.69)], PAPER),
        shape([(.59, .015), (1.02, .015), (.78, -1.69), (.48, -1.69)], "#A88E76"),
        oval(0, -.014, 2.04, .36, "#E8D6BA"),
        oval(0, .035, 1.79, .22, mix),
    )
    if mix != INK:
        artwork.add(*[disk(dx, .04 + dy, .024, SOIL if mix == DAMP else DAMP)
                      for dx, dy in ((-.67, 0), (-.48, .035), (-.21, -.018),
                                     (.12, .04), (.31, -.023), (.57, .015))])
    return artwork.scale(scale, about_point=ORIGIN).shift(pt(x, rim))


def condition(i, x, rim=RIM):
    color = BLUE if i in (0, 2) else PAPER
    tag = boxed_label(NAMES[i], color=color, size=28, min_size=28, pad=.12, stroke=0)
    tag.box.set_fill(TAPE, opacity=1)
    return tag.move_to(pt(x, rim - .84)).set_z_index(3)


def droplet(x, y, k=1):
    return VGroup(disk(0, -.04, .139, BLUE),
                  shape([(-.125, -.007), (.125, -.007), (0, .248)], BLUE)
                  ).scale(k).move_to(pt(x, y))


def spoon(x, y):
    return VGroup(block(.52, 0, 1.13, .12, PAPER, radius=.055),
                  oval(-.23, 0, .65, .34, GREY),
                  oval(-.24, .025, .50, .20, BLUE)).move_to(pt(x, y))


def pour(scene, xs, seconds, rim=RIM, doses=2):
    """Each tilt delivers one visibly separate spoonful to each selected cup."""
    rigs = [spoon(x + .36, rim + 1.11).set_z_index(4) for x in xs]
    scene.play(*[FadeIn(s, shift=DOWN * .12) for s in rigs], run_time=seconds * .17)
    for _ in range(doses):
        drops = [droplet(x, rim + .79).set_z_index(4) for x in xs]
        scene.add(*drops)
        scene.play(*[Rotate(s, PI / 8, about_point=s.get_center()) for s in rigs],
                   *[d.animate.shift(DOWN * .68) for d in drops], run_time=seconds * .49 / doses)
        scene.remove(*drops)
        scene.play(*[Rotate(s, -PI / 8, about_point=s.get_center()) for s in rigs],
                   run_time=seconds * .18 / doses)
    scene.play(*[FadeOut(s, shift=UP * .18) for s in rigs], run_time=seconds * .16)


def bag(x, y, wet=False):
    return VGroup(
        shape([(-1.17, -1.06), (1.17, -1.06), (.91, 1.02), (-.91, 1.02)], PAPER),
        shape([(-1.06, -.95), (1.05, -.95), (.94, -.16), (-.95, -.16)], DAMP if wet else SOIL),
        oval(0, .96, 1.70, .24, DAMP if wet else SOIL),
        *[disk(a, b, .09, GREEN) for a, b in ((-.22, .29), (.16, .41), (.34, .17))],
    ).move_to(pt(x, y))


def packet(x, y):
    radish = VGroup(disk(0, -.27, .28, "#C75676"),
                    oval(-.09, .0, .16, .34, GREEN, .53),
                    oval(.1, .03, .18, .34, GREEN, -.57),
                    Line(pt(0, -.46), pt(-.08, -.64), color="#C75676", stroke_width=3))
    return VGroup(block(0, 0, 1.56, 1.95, "#C9C5A6", radius=.08),
                  block(0, .69, 1.56, .38, "#7B4862"),
                  radish).move_to(pt(x, y))


def seeds(x, y, k=1):
    return VGroup(*[oval(x + a * k, y + b * k, .21 * k, .14 * k, color, a * 2)
                    for (a, b), color in zip(((-.48, -.04), (-.26, .09), (-.04, -.07),
                                              (.19, .06), (.42, -.03)),
                                             (SOIL, PAPER, SOIL, PAPER, SOIL))])


def pencil(x, y):
    return VGroup(block(0, 0, 1.24, .15, ORANGE, radius=.05),
                  shape([(-.81, 0), (-.59, -.075), (-.59, .075)], PAPER),
                  shape([(-.81, 0), (-.72, -.03), (-.72, .03)], INK),
                  block(.58, 0, .18, .15, PINK, radius=.04)).rotate(.24).move_to(pt(x, y))


def sheet(x, y, marked=False, scale=1, predictions=True):
    page = block(0, 0, 3.35, 1.70, "#D5CAB1", radius=.10)
    card = VGroup(page, block(0, .57, 3.08, .11, ORANGE))
    for j in range(4):
        px = -1.15 + j * .76
        card.add(block(px, -.31, .52, .66, "#B7A690", radius=.06))
        if marked:
            if predictions:
                card.add(ArcBetweenPoints(pt(px - .12, -.12), pt(px + .12, -.25), angle=-PI,
                                           color="#AC582E", stroke_width=3),
                         disk(px, -.43, .043, "#AC582E"))
            else:
                card.add(seedling(("strong", "dry", "lean", "dry")[j], px, -.52, .27))
    return card.scale(scale).move_to(pt(x, y))


def person(x, y, k=1, child=False, away=False):
    shirt = TEAL if child else "#897FBA"
    hair = "#523C49"
    g = VGroup(
        RoundedRectangle(width=1.42, height=1.33, corner_radius=.3, fill_color=shirt,
                         fill_opacity=1, stroke_width=0).move_to(pt(0, -.96)),
        block(0, -.30, .29, .34, SKIN, radius=.08),
        oval(0, .24, 1.08, 1.22, hair),
        oval(.045, .15, .89, .92, SKIN),
        oval(-.18, .51, .69, .30, hair, .23),
        disk(-.10 if away else .24, .20, .041, INK),
        shape([(-.36, .17), (-.51, .055), (-.34, .002)] if away else
              [(.42, .17), (.57, .055), (.41, .002)], SKIN),
    )
    return g.scale(k, about_point=ORIGIN).shift(pt(x, y))


def hand(x, y, k=1, angle=0):
    return VGroup(oval(.13, 0, .84, .53, SKIN),
                  block(-.37, .13, .91, .18, SKIN, radius=.085),
                  oval(-.10, -.20, .47, .20, SKIN, -.35),
                  block(.70, 0, .53, .33, "#897FBA", radius=.08)
                  ).rotate(angle).scale(k).move_to(pt(x, y))


def scissors(x, y):
    halves = VGroup()
    for side in (-1, 1):
        halves.add(VGroup(
            Circle(radius=.16, color=ORANGE, stroke_width=5).move_to(pt(.42, side * .20)),
            shape([(.29, side * .13), (-.72, -side * .20), (-.43, .021)], PAPER),
        ))
    return VGroup(halves, disk(-.12, 0, .049, INK)).move_to(pt(x, y))


def result_scene(states, positions=TEST_XS, choose=(0, 1, 2, 3)):
    bodies = [cup(positions[i], SOIL if states[i] == "dry" else DAMP) for i in choose]
    plants = [sprouts(positions[i], states[i]) for i in choose]
    tags = [condition(i, positions[i]) for i in choose]
    return bodies, plants, tags


def test_room():
    cabinet, door = cupboard()
    return VGroup(daylight(-3.6, 5.98), cabinet).set_z_index(-2), door


def compare_picture(state=None):
    """The watered pair keeps the scale and positions of the four-cup experiment."""
    room, _ = test_room()
    plants = sprouts(TEST_XS[0], "strong")
    dark = (sprouts(TEST_XS[2], state) if state else
            VGroup(oval(TEST_XS[2], 1.12, 1.67, 2.30, "#343445"),
                   label("?", TEST_XS[2], 1.12, 94, ORANGE)))
    return VGroup(room, cup(TEST_XS[0]), cup(TEST_XS[2]), plants, dark,
                  condition(0, TEST_XS[0]), condition(2, TEST_XS[2])), plants, dark


def hook_picture():
    cabinet, _ = cupboard()
    return VGroup(daylight(-3.6, 5.98), cabinet, door_ajar(),
                  cup(-3.63, rim=-.01, scale=1.26),
                  sprouts(-3.63, "strong", rim=-.01, scale=1.26))


def breeze(plant, x, state, rim=RIM, scale=1, seed=0):
    """Bend the stems from their bases so the leaves move and the cups stay put."""
    elapsed = 0.0

    def sway(mob, dt):
        nonlocal elapsed
        elapsed += dt
        angle = (np.sin(1.86 * elapsed + seed) - np.sin(seed)) * .23
        mob.become(sprouts(x, state, rim, scale, angle))

    plant.add_updater(sway)


class S01Hook(SpokenScene):
    def construct(self):
        picture = hook_picture()
        self.add(picture)
        breeze(picture[-1], -3.63, "strong", rim=-.01, scale=1.26)
        self.at("need sunlight")
        question = question_card("Water, but no light?", size=44, y=-3.16, color=ORANGE)
        self.play(FadeIn(question, shift=UP * .15), run_time=.65)
        self.at("Four cups")
        extras = VGroup(*[VGroup(cup(x, rim=-1.39, scale=.46),
                                 sprouts(x, "strong", rim=-1.39, scale=.46))
                          for x in (-5.65, -2.25, -1.27)])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .33) for c in extras], lag_ratio=.24),
                  run_time=1.04)
        self.at("dark cupboard")
        self.play(Rotate(picture[2], .045, about_point=picture[2].get_bottom(),
                         rate_func=there_and_back), run_time=1.35)
        self.finish()


class S02Title(TitleCard):
    LESSON = "What Do Plants Need?"
    TITLE = "What Do Plants Need? A Parent Guide"

    def construct(self):
        self.add(hook_picture())
        headline = T(self.LESSON, size=48, font=TITLE_FONT).move_to(pt(0, 3.16))
        self.play(FadeIn(headline, shift=UP * .10), run_time=.45)
        self.wait(self.narration_s - self.elapsed())


class S03Payoff(SpokenScene):
    def construct(self):
        self.add(daylight(), tray())
        cups = VGroup(*[cup(x, INK) for x in XS])
        clock = VGroup(Circle(radius=.48, color=GOLD, stroke_width=4),
                       Line(ORIGIN, UP * .29, color=GOLD, stroke_width=4),
                       Line(ORIGIN, RIGHT * .26, color=GOLD, stroke_width=4)).move_to(pt(.72, 1.59))
        setup = label("About 30 minutes", -.30, 3.16, 36, GOLD)
        self.at("Set up takes")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * .33) for c in cups], lag_ratio=.2),
                  run_time=1.05)
        self.play(FadeIn(setup), Create(clock), run_time=.82)
        self.at("quick checks")
        cal = block(.72, 1.59, 2.36, 1.42, INK, radius=.10)
        ticks = VGroup(*[disk(-.14 + .29 * i, 1.83 - .39 * row, .066, TEAL)
                         for row in range(2) for i in range(7)])
        self.play(FadeOut(clock), run_time=.24)
        timing = label("About two weeks", -.30, 3.16, 36, GOLD)
        self.play(swap(setup, timing, .56), FadeIn(cal), run_time=.56)
        self.play(LaggedStart(*[GrowFromCenter(t) for t in ticks], lag_ratio=.16),
                  run_time=2.5)
        self.at("child practices")
        self.play(FadeOut(cal), FadeOut(ticks), FadeOut(timing), run_time=.48)
        guess = pencil(0, 1.37).scale(1.45)
        bob(guess, amp=.13, speed=2.2)
        self.play(FadeIn(guess, shift=RIGHT * .9), run_time=.85)
        first = label("Guess, then check", -4.24, 3.16, 32, ORANGE)
        self.play(FadeIn(first), run_time=.38)
        self.at("change one thing")
        halo = mark(XS[1])
        second = label("Change one thing", 0, 3.16, 32, GOLD)
        self.play(FadeOut(guess), Create(halo), run_time=.32)
        self.play(FadeIn(second), run_time=.23)
        self.at("check the result")
        third = label("Watch over time", 4.10, 3.16, 32, TEAL)
        self.play(FadeOut(halo), FadeIn(cal),
                  LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=.1), run_time=.67)
        self.play(FadeIn(third), run_time=.35)
        self.finish()


def mark(x):
    return RoundedRectangle(width=2.51, height=2.03, corner_radius=.20, color=GOLD,
                            stroke_width=4).move_to(pt(x, -1.32)).set_z_index(4)


class S04Gather(SpokenScene):
    def construct(self):
        rack = tray()
        cups = VGroup(*[cup(x, INK) for x in XS])
        self.add(daylight(), rack, cups)
        self.at("four small cups")
        bottom = VGroup(oval(-1.55, .93, 1.73, .73, PAPER),
                        oval(-1.55, .94, 1.47, .51, "#BCA185")).set_z_index(2)
        self.play(TransformFromCopy(cups[1], bottom), run_time=.80)
        poke = hand(-.60, 1.65, .90, angle=.45).set_z_index(4)
        point = Line(pt(-1.37, 1.38), pt(-1.56, 1.10), color=GREY, stroke_width=6).set_z_index(3)
        self.at("holes and adult")
        grip = VGroup(point, poke)
        self.play(FadeIn(grip, shift=DOWN * .35), run_time=.54)
        holes = VGroup(*[disk(x, .93, .05, INK) for x in (-1.56, -1.82, -1.30)]).set_z_index(3)
        self.play(grip.animate.shift(DOWN * .17), run_time=.38)
        self.play(grip.animate.shift(UP * .17),
                  LaggedStart(*[FadeIn(dot, scale=.3) for dot in holes], lag_ratio=.5),
                  run_time=.64)
        self.play(FadeOut(grip), FadeOut(holes), FadeOut(bottom), run_time=.45)
        self.at("Add a tray")
        self.play(rack.animate.shift(DOWN * .09), rate_func=there_and_back, run_time=.52)
        self.at("potting mix")
        mix = bag(-3.52, 1.05)
        self.play(FadeIn(mix, shift=DOWN * .28), run_time=.54)
        self.at("radish seeds")
        pkt = packet(-1.36, 1.13)
        self.play(FadeIn(pkt, shift=DOWN * .27), run_time=.71)
        self.at("Bring water")
        glass = VGroup(shape([(-.47, .12), (.47, .12), (.34, 1.45), (-.34, 1.45)], GREY),
                       shape([(-.39, .20), (.39, .20), (.36, 1.14), (-.36, 1.14)], BLUE)
                       ).rotate(PI).move_to(pt(.0, .97))
        self.play(FadeIn(glass, shift=DOWN * .25), run_time=.55)
        self.at("a tablespoon")
        self.play(FadeIn(spoon(.50, 1.84).rotate(.44), shift=LEFT * .35), run_time=.62)
        self.at("labels and")
        roll = VGroup(disk(1.92, 1.06, .37, PAPER), disk(1.92, 1.06, .19, INK),
                      pencil(2.36, 1.68).rotate(-.64))
        self.play(FadeIn(roll, shift=DOWN * .3), run_time=.62)
        self.at("cupboard or")
        box = VGroup(shape([(3.62, .39), (5.72, .39), (5.72, 1.84), (3.62, 1.84)], SOIL),
                     shape([(5.72, .39), (6.19, .69), (6.19, 2.08), (5.72, 1.84)], DAMP),
                     shape([(3.62, 1.84), (5.72, 1.84), (6.19, 2.08), (4.09, 2.08)], PAPER))
        self.play(FadeIn(box, shift=DOWN * .38), run_time=1.3)
        self.finish()


class S05MixSafety(SpokenScene):
    def construct(self):
        self.add(daylight(open_window=True), tray())
        adult = person(-3.74, -.03, 1.36)
        kid = person(4.91, -.88, .82, child=True, away=True)
        mix_y = -1.03
        mix = bag(0, mix_y)
        snips = scissors(.79, mix_y + 1.35)
        opening = label("Open window", 0, 3.16, 36, TEAL)
        self.add(adult, mix)
        self.at("adult open")
        self.play(FadeIn(snips, shift=LEFT * .82), adult.animate.shift(RIGHT * .65),
                  run_time=.73)
        for _ in range(2):
            joint = snips[1].get_center()
            self.play(Rotate(snips[0][0], .27, about_point=joint),
                      Rotate(snips[0][1], -.27, about_point=joint),
                      rate_func=there_and_back, run_time=.68)
        opening_mix = oval(0, mix_y + .97, 1.96, .42, DAMP)
        self.play(snips.animate.shift(LEFT * .75), GrowFromCenter(opening_mix), run_time=.82)
        self.at("open window")
        self.play(FadeIn(opening), FadeOut(snips), run_time=.58)
        self.at("Keep your child")
        self.play(FadeIn(kid, shift=RIGHT * .44), FadeOut(opening), run_time=.72)
        self.at("turn your face")
        profile = person(-3.09, -.03, 1.36, away=True)
        self.play(Transform(adult, profile), kid.animate.shift(RIGHT * .25), run_time=1.26)
        self.at("Dampen the mix")
        drops = VGroup(*[droplet(x, 1.14 + .46 * n, .64)
                         for n, x in enumerate((-.56, .0, .51))])
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * .49) for d in drops], lag_ratio=.18),
                  run_time=.62)
        self.play(Transform(mix, bag(0, mix_y, wet=True)), FadeOut(opening_mix),
                  LaggedStart(*[FadeOut(d, shift=DOWN * (1.12 + .46 * i))
                                for i, d in enumerate(drops)], lag_ratio=.15), run_time=.95)
        scoop = spoon(.56, mix_y + .67)
        self.play(FadeIn(scoop, shift=LEFT * .3), run_time=.36)
        self.play(FadeOut(scoop, shift=UP * .32), run_time=.40)
        self.at("Read the seed packet")
        pkt = packet(2.69, -1.10)
        self.play(FadeIn(pkt, shift=UP * .43), run_time=.66)
        untreated = boxed_label("Untreated", ORANGE, size=30).move_to(pt(2.69, .48))
        self.at("choose untreated")
        self.play(FadeIn(untreated, shift=UP * .16), run_time=.62)
        self.finish()


class S06Plant(SpokenScene):
    def construct(self):
        self.add(daylight(), tray())
        cups = [cup(x, INK) for x in XS]
        self.add(*cups)
        self.at("Fill the four cups")
        dusting = [VGroup(*cup(x)[4:]) for x in XS]
        self.play(LaggedStart(*[AnimationGroup(c[3].animate.set_fill(DAMP),
                                                FadeIn(grains, shift=DOWN * .13))
                                for c, grains in zip(cups, dusting)], lag_ratio=.23),
                  run_time=1.49)
        tags = [condition(i, x) for i, x in enumerate(XS)]
        for cue, index in (("Light plus water", 0), ("dark plus water", 2),
                           ("light no water", 1), ("dark no water", 3)):
            self.at(cue)
            self.play(FadeIn(tags[index], shift=DOWN * .12), run_time=.54)
        self.at("child presses")
        kernels = [seeds(x, .33) for x in XS]
        self.play(LaggedStart(*[FadeIn(k, shift=DOWN * .31) for k in kernels], lag_ratio=.18),
                  run_time=.84)
        finger = hand(-.91, .85, .70, angle=-.40)
        self.play(FadeIn(finger, shift=DOWN * .31), run_time=.32)
        self.play(*[k.animate.shift(DOWN * .71) for k in kernels],
                  finger.animate.shift(DOWN * .27), run_time=1.05)
        self.at("and covers them")
        self.play(*[FadeOut(k, shift=DOWN * .14) for k in kernels],
                  FadeOut(finger, shift=UP * .39), run_time=.57)
        self.at("Give each cup two")
        pour(self, XS, 2.21)
        self.finish()


class S07Grow(SpokenScene):
    def construct(self):
        window = daylight()
        self.add(window, tray(), *[cup(x) for x in XS],
                 *[condition(i, x) for i, x in enumerate(XS)])
        self.at("sunny window sill")
        light = shape([(-5.92, 1.41), (-4.98, 1.28), (1.90, -2.01), (-1.09, -2.01)],
                      YELLOW).set_fill(opacity=.29)
        light.set_z_index(-1)
        window.set_z_index(-2)
        self.play(FadeIn(light, shift=RIGHT * .4), run_time=.91)
        self.play(FadeOut(light, shift=RIGHT * .34), run_time=1.38)
        self.at("water each cup")
        pour(self, XS, 2.47, doses=1)
        self.at("Sprouts usually appear")
        plants = [sprouts(x, "young") for x in XS]
        self.play(LaggedStart(*[GrowFromPoint(p, pt(x, RIM))
                                for p, x in zip(plants, XS)], lag_ratio=.22), run_time=2.8)
        for i, p in enumerate(plants):
            breeze(p, XS[i], "young", seed=i)
        self.at("about two centimeters")
        marker = BraceBetweenPoints(pt(-3.37, RIM), pt(-3.37, .58), RIGHT,
                                    color=GOLD, buff=0)
        height = place_label(T("About 2 cm", 30, GOLD), marker, dirs=(UP,), buff=.34)
        self.play(GrowFromCenter(marker), FadeIn(height), run_time=.55)
        self.at("child predict")
        guess = sheet(.0, 1.53)
        self.play(FadeOut(marker), FadeOut(height), run_time=.27)
        self.play(FadeIn(guess, shift=DOWN * .36), run_time=.64)
        self.at("Write or draw")
        pen = pencil(1.42, 1.42)
        self.play(FadeIn(pen, shift=LEFT * .46), run_time=.34)
        self.play(Transform(guess, sheet(0, 1.53, marked=True)),
                  pen.animate.shift(LEFT * 2.0 + DOWN * .21), run_time=.93)
        self.play(FadeOut(pen, shift=RIGHT * .42), run_time=.31)
        self.finish()


class S08StartTest(SpokenScene):
    def construct(self):
        room, door = test_room()
        shelf = daylight().set_z_index(-3)
        rack = tray().set_z_index(-1)
        self.add(shelf, rack)
        bodies, plants, tags = result_scene(("young",) * 4, positions=XS)
        units = [VGroup(*pieces) for pieces in zip(bodies, plants, tags)]
        self.add(*units)
        brought = sheet(0, 1.53, marked=True)
        self.add(brought)
        self.at("Use a cupboard")
        self.play(FadeOut(brought, shift=UP * .45), run_time=.56)
        empty_cabinet = room[1].copy().scale(.36).move_to(pt(3.56, 1.61))
        self.play(FadeIn(empty_cabinet, shift=LEFT * .52), run_time=.90)
        self.at("Move both dark cups")
        paths = [CubicBezier(u.get_center(), u.get_center() + pt(-.66, 1.65),
                             u.get_center() + pt(.15, 1.56),
                             u.get_center() + pt(TEST_XS[i] - XS[i], 0))
                 for i, u in enumerate(units) if i >= 2]
        self.play(Transform(shelf, room[0]), Transform(empty_cabinet, room[1]), FadeOut(rack),
                  *[units[i].animate.shift(LEFT * .37) for i in (0, 1)],
                  *[MoveAlongPath(unit, path) for unit, path in zip(units[2:], paths)],
                  run_time=1.49)
        self.at("shut the door")
        grip = hand(2.15, .18, .75).set_z_index(6)
        self.play(FadeIn(grip, shift=LEFT * .45), run_time=.31)
        self.play(*[FadeOut(unit) for unit in units[2:]], run_time=.24)
        self.play(FadeIn(door, shift=LEFT * .26),
                  grip.animate.shift(LEFT * .65), run_time=.44)
        self.play(FadeOut(grip, shift=DOWN * .32), run_time=.26)
        self.at("Give each water cup")
        self.play(FadeOut(door, shift=RIGHT * .28), run_time=.29)
        self.play(*[FadeIn(u) for u in units[2:]], run_time=.28)
        for i, plant in enumerate(plants):
            breeze(plant, TEST_XS[i], "young", seed=i)
        pour(self, (TEST_XS[0], TEST_XS[2]), 3.55)
        self.at("Stop watering")
        self.play(*[bodies[i][3].animate.set_fill(SOIL) for i in (1, 3)], run_time=.97)
        self.at("Compare cups that")
        gold = [mark(x) for x in TEST_XS]
        compare = label("Change just the light", 0, 3.16, 36, GOLD)
        self.play(Create(gold[0]), Create(gold[2]), FadeIn(compare), run_time=.61)
        self.at("or only in water")
        self.play(FadeOut(gold[2]), Create(gold[1]),
                  swap(compare, label("Change just the water", 0, 3.16, 36, GOLD), .70),
                  run_time=.70)
        self.finish()


class S09PredictQuestion(SpokenScene):
    def construct(self):
        picture, green, mystery = compare_picture()
        self.add(*picture[:-4], green, *picture[-2:])
        breeze(green, TEST_XS[0], "strong")
        self.at("Picture the two cups")
        cover, mark_text = mystery
        both = [droplet(x, -.48, 1.48) for x in (TEST_XS[0], TEST_XS[2])]
        self.play(*[FadeIn(d, shift=DOWN * 1.48) for d in both], run_time=.70)
        self.play(*[FadeOut(d, shift=DOWN * .52) for d in both], run_time=.78)
        self.at("After about a week")
        self.play(FadeIn(cover, shift=UP * .54), FadeIn(mark_text, shift=UP * .54),
                  run_time=.91)
        self.at("compare with the windowsill")
        x = TEST_XS[0]
        guides = Line(pt(x - .91, 1.20), pt(x + .59, 1.20), color=GOLD, stroke_width=5)
        self.play(Create(guides), Indicate(mystery[0], color="#535169", scale_factor=1.08),
                  run_time=1.10)
        self.play(FadeOut(guides), run_time=.35)
        self.at("Shorter the same height")
        self.play(FadeIn(question_card(PREDICTION, **CARD), shift=UP * .10), run_time=.65)
        self.finish()


class S10PredictPause(PredictPause):
    QUESTION = PREDICTION
    SECONDS = 4.5
    CARD = CARD

    def backdrop(self):
        picture, green, _ = compare_picture()
        breeze(green, TEST_XS[0], "strong")
        return picture

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        center = pt(5.05, .71)
        ring, animation = countdown(self.SECONDS, center=center, radius=.87, color=ORANGE)
        remaining = animation.mobject
        face = always_redraw(lambda: Sector(
            radius=.76, start_angle=PI / 2,
            angle=TAU * max(.001, remaining.get_value()),
            fill_color=ORANGE, fill_opacity=.75, stroke_width=0, arc_center=center))
        self.add(face, ring)
        self.play(animation)


class S11Reveal(SpokenScene):
    def construct(self):
        picture, green, mystery = compare_picture()
        self.add(picture)
        question = question_card(PREDICTION, **CARD)
        self.add(question)
        breeze(green, TEST_XS[0], "strong")
        x = TEST_XS[2]
        plant = sprouts(x, "young")
        self.at("The dark seedlings")
        self.play(FadeOut(mystery, shift=UP * .37), FadeOut(question), FadeIn(plant), run_time=.69)
        self.at("often taller")
        self.play(Transform(plant, sprouts(x, "tall")), run_time=.76)
        self.at("thinner")
        self.play(Transform(plant, sprouts(x, "thin")), run_time=.47)
        self.at("and paler")
        self.play(Transform(plant, sprouts(x, "pale")),
                  FadeIn(label("What you may see", 0, 3.16, 37, GOLD)), run_time=.87)
        self.at("may lean")
        self.play(Transform(plant, sprouts(x, "lean")), run_time=2.02)
        self.at("on stored food")
        breeze(plant, x, "lean", seed=1.1)
        self.at("what do you notice")
        self.play(FadeIn(question_card("What else do you notice?", **CARD)), run_time=.70)
        self.finish()


class S12DryAndWeak(SpokenScene):
    def construct(self):
        room, door = test_room()
        bodies, plants, tags = result_scene(("strong", "young", "lean", "young"))
        self.add(room, *bodies[:2], *plants[:2], *tags[:2], door)
        breeze(plants[0], TEST_XS[0], "strong")
        grip = hand(2.1, .18, .74).set_z_index(6)
        self.at("Every day or two")
        self.play(FadeIn(grip, shift=LEFT * .4), run_time=.49)
        self.at("take a quick look")
        groups = [VGroup(bodies[i], plants[i], tags[i]) for i in (2, 3)]
        self.play(FadeOut(door, shift=RIGHT * .27), FadeOut(grip, shift=RIGHT * .31),
                  run_time=.28)
        self.play(*[FadeIn(group) for group in groups], run_time=.27)
        self.play(*[g.animate.shift(UP * .22) for g in groups], run_time=.43)
        self.at("return the dark cups")
        self.play(*[g.animate.shift(DOWN * .22) for g in groups], run_time=.53)
        self.play(*[FadeOut(g) for g in groups], run_time=.24)
        self.play(FadeIn(door, shift=LEFT * .25), run_time=.37)
        self.at("Draw each cup")
        observations = sheet(-.95, 1.60, scale=.95, predictions=False).set_z_index(6)
        pen = pencil(.22, 1.56).set_z_index(7)
        self.play(FadeIn(observations, shift=DOWN * .23), FadeIn(pen, shift=LEFT * .29),
                  run_time=.69)
        self.play(Transform(observations, sheet(-.95, 1.60, marked=True, scale=.95,
                                                 predictions=False).set_z_index(6)),
                  pen.animate.shift(LEFT * 1.69 + DOWN * .24), run_time=1.14)
        self.at("Note height color")
        metrics = label("Height • Color • Drooping", 0, 3.15, 36, GOLD)
        self.play(FadeIn(metrics), FadeOut(pen, shift=UP * .33), run_time=.59)
        self.at("The dry cups")
        self.play(FadeOut(door, shift=RIGHT * .26), FadeOut(observations, shift=UP * .22),
                  FadeOut(metrics), run_time=.39)
        self.play(*[FadeIn(g) for g in groups], run_time=.28)
        self.at("usually droop")
        timing = label("Dry cups • 2 to 5 days", 0, 3.16, 36, GOLD)
        self.play(*[Transform(plants[i], sprouts(TEST_XS[i], "dry")) for i in (1, 3)],
                  run_time=1.24)
        self.play(FadeIn(timing), run_time=.49)
        self.at("Dark seedlings weaken")
        weak_timing = label("Dark seedlings • 1 to 2 weeks", 0, 3.16, 36, GOLD)
        self.play(swap(timing, weak_timing, .77),
                  Transform(plants[2], sprouts(TEST_XS[2], "weak")), run_time=1.58)
        self.at("light and water cup")
        self.play(FadeOut(weak_timing), Create(mark(TEST_XS[0])), run_time=.62)
        self.finish()


def food_meter(level):
    """A qualitative store: the capsule empties without suggesting a measured amount."""
    x, y, width = 2.65, -.25, 2.70
    frame = block(x, y, width, .77, TAPE, edge=PINK, radius=.20)
    left = x - width / 2 + .13
    w = max(.001, (width - .26) * level.get_value())
    return VGroup(frame, block(left + w / 2, y, w, .51, PINK))


class S13Why(SpokenScene):
    def construct(self):
        picture, green, dark = compare_picture("weak")
        self.add(picture)
        self.at("A green plant")
        leaf = oval(0, .52, 3.85, 1.72, GREEN, .60)
        vein = Line(pt(-1.37, -.49), pt(1.34, 1.51), stroke_width=4, color="#467346")
        closeup = VGroup(leaf, vein)
        self.play(FadeOut(picture), TransformFromCopy(green[1][1][1], closeup), run_time=1.08)
        bob(closeup, amp=.10, speed=1.6)
        self.at("own food")
        sugar = VGroup(*[block(a, b, .38, .38, PINK, radius=.08)
                         for a, b in ((3.90, .31), (4.28, .48), (4.12, .86))])
        self.play(LaggedStart(*[FadeIn(o, scale=.6) for o in sugar], lag_ratio=.24),
                  run_time=.79)
        sweet = label("Sugar", 4.10, -.42, 34, PINK)
        self.play(FadeIn(sweet), run_time=.43)
        light = sun(-4.8, 2.33, .35)
        items = VGroup(light, droplet(-4.79, .55, 1.55),
                       VGroup(*[oval(-4.91, -.90 + i * .15, .38 + .18 * i, .066, TEAL)
                                for i in range(3)]))
        for cue, index, name, color, y in (
                ("It uses light", 0, "Light", YELLOW, 2.33),
                ("water and a gas", 1, "Water", BLUE, .55),
                ("a gas from the air", 2, "Gas from air", TEAL, -.78)):
            self.at(cue)
            ray = Arrow(pt(-3.72, y), pt(-1.67, .82 - index * .40), buff=0,
                        color=color, stroke_width=4, tip_length=.21,
                        max_tip_length_to_length_ratio=.16)
            self.play(FadeIn(items[index]), GrowArrow(ray), run_time=.37)
            self.play(FadeIn(label(name, -4.76, y - (.98 if index == 0 else .53), 30, color)),
                      run_time=.23)
        output = Arrow(pt(1.82, .64), pt(3.46, .64), buff=0, color=PINK,
                       stroke_width=4, tip_length=.21, max_tip_length_to_length_ratio=.16)
        self.play(GrowArrow(output), run_time=.48)
        self.at("In the dark")
        extras = [m for m in self.mobjects if m is not closeup]
        self.play(*[FadeOut(m) for m in extras], FadeOut(closeup), run_time=.42)
        room, _ = test_room()
        x = TEST_XS[2]
        night = VGroup(room[1], cup(x), sprouts(x, "lean"),
                       condition(2, x), block(-2.80, .18, 6.51, 4.94, "#252535", radius=.12))
        level = ValueTracker(1)
        store = always_redraw(lambda: food_meter(level).shift(LEFT * 5.48))
        self.play(FadeIn(night), run_time=.55)
        self.at("on stored food")
        self.add(store)
        self.play(FadeIn(label("Stored food", -2.83, .64, 36, PINK)),
                  level.animate.set_value(.52), run_time=1.42)
        self.at("runs out")
        self.play(level.animate.set_value(0),
                  Transform(night[2], sprouts(x, "weak")), run_time=1.75)
        self.finish()


def tap(x, y):
    pipe = VMobject(stroke_width=23, stroke_color=GREY)
    pipe.set_points_as_corners([pt(x - .75, y - .83), pt(x - .75, y),
                                pt(x + .55, y), pt(x + .55, y - .33)])
    return VGroup(pipe, block(x - .75, y - .80, .64, .19, GREY, radius=.06),
                  block(x - .75, y + .29, .61, .13, PAPER, radius=.05))


class S14Safety(SpokenScene):
    def construct(self):
        self.add(daylight(), tray())
        adult = person(-2.55, .05, 1.40)
        kid = person(-.40, -.53, 1.08, child=True)
        plant_cup = VGroup(cup(2.1), sprouts(2.1, "young"))
        self.add(adult, kid, plant_cup)
        self.at("Stay with your child")
        self.play(adult.animate.shift(RIGHT * .32), kid.animate.shift(RIGHT * .20), run_time=.95)
        self.at("they plant and water")
        pour(self, (2.1,), 1.36, doses=1)
        self.at("Nobody tastes")
        self.play(FadeOut(adult), FadeOut(kid), FadeOut(plant_cup), run_time=.39)
        trio = VGroup(seeds(-2.61, -.17, 1.45), bag(0, -.04, wet=True),
                      cup(2.39, rim=-.06, scale=.68),
                      sprouts(2.39, "young", rim=-.06, scale=.83))
        self.play(LaggedStart(*[FadeIn(item, shift=DOWN * .38) for item in trio],
                              lag_ratio=.19), run_time=.83)
        no_taste = VGroup(
            Ellipse(width=8.04, height=2.99, color=RED, stroke_width=8).move_to(pt(0, -.12)),
            Line(pt(-3.38, .73), pt(3.38, -.97), color=RED, stroke_width=9))
        previous = label("Do not taste", 0, 3.16, 39, RED)
        self.play(Create(no_taste), FadeIn(previous), run_time=.76)
        self.at("Keep seeds and marker")
        self.play(FadeOut(trio), FadeOut(no_taste), FadeOut(previous), run_time=.46)
        high_shelf = block(-2.58, .65, 4.31, .18, WOOD, radius=.05)
        cap = block(-1.48, .97, .29, .43, GREY, edge=PAPER, radius=.07)
        small = VGroup(seeds(-3.09, .99), cap)
        child = person(2.65, -.92, .91, child=True, away=True)
        self.play(FadeIn(high_shelf), FadeIn(child), FadeIn(small, shift=UP * 1.29), run_time=.95)
        self.at("children under 4")
        risk = label("Under 4: choking risk", 0, 3.16, 38, RED)
        self.play(FadeIn(risk), run_time=.62)
        call = boxed_label("Call 911", TEXT, size=42, pad=.24).move_to(pt(0, -.39))
        call.box.set_fill("#3D2834", opacity=1).set_stroke(RED, width=3)
        self.at("call 911")
        self.play(FadeOut(small), FadeOut(high_shelf), FadeOut(child), FadeOut(risk),
                  FadeIn(call, shift=UP * .21), run_time=.76)
        self.at("Wash hands")
        faucet = tap(.10, 1.88)
        left_hand = hand(-.53, -.35, 1.05).flip(UP).rotate(.20)
        right_hand = hand(1.52, -.35, 1.05, -.20)
        bubbles = VGroup(*[Circle(radius=r, color=TEXT, stroke_width=3).move_to(pt(x, y))
                           for x, y, r in ((.17, .25, .17), (.62, .16, .13), (-.25, .04, .16),
                                           (-.01, .56, .11), (.53, .53, .095))])
        water = VGroup(*[Line(pt(x, 1.43), pt(x - .13, y), color=BLUE, stroke_width=5)
                         for x, y in ((.65, -.04), (.55, .12), (.75, .02))])
        self.play(FadeOut(call), FadeIn(faucet), FadeIn(left_hand, shift=LEFT * .37),
                  FadeIn(right_hand, shift=RIGHT * .37), run_time=.56)
        self.at("with soap and water")
        self.play(Create(water), FadeIn(bubbles, shift=UP * .22), run_time=.56)
        for n in range(3):
            self.play(left_hand.animate.shift(RIGHT * .22), right_hand.animate.shift(LEFT * .22),
                      bubbles.animate.shift(UP * .18), rate_func=there_and_back,
                      run_time=.96)
        self.finish()


class S15Debrief(SpokenScene):
    def construct(self):
        room, _ = test_room()
        bodies, plants, tags = result_scene(("strong", "dry", "weak", "dry"))
        self.add(room, *bodies, *plants, *tags)
        breeze(plants[0], TEST_XS[0], "strong")
        breeze(plants[2], TEST_XS[2], "weak", seed=1.3)
        self.at("lay the first guesses")
        paper = sheet(0, 1.57, marked=True, scale=.85)
        self.play(FadeIn(paper, shift=DOWN * .59), run_time=1.11)
        self.at("what surprised you")
        surprise = question_card("What surprised you?", **CARD)
        self.play(FadeIn(surprise, shift=UP * .13), run_time=.69)
        self.at("where does a green plant")
        food = question_card("Where does a green plant get its food?", **CARD)
        self.play(swap(surprise, food, .82))
        self.at("child point to a cup")
        pointing = hand(-3.51, .83, 1.02, .23)
        self.play(FadeIn(pointing, shift=LEFT * .27), run_time=.61)
        self.play(pointing.animate.shift(LEFT * .33 + DOWN * .09),
                  rate_func=there_and_back, run_time=1.46)
        self.finish()


class S16End(EndCard):
    LINE = "Green plants need light and water to make food."
