"""A tabletop flower dissection and a three-liner pollination model."""
from bp_parts import *

# COLOR MAP: olive outer tepals, coral petals, gold pollen, mint central part.
# Red and blue are the two pretend-pollen colors. The old setup film used the
# shared style colors for safety, materials and observation (red, teal, gold).
WOOD = "#2E211E"
GRAIN = "#3B2A25"
PAPER = "#F5EBDC"
INK = "#302827"
PINK = "#D65071"
PINK_LIGHT = "#F7839B"
PLUM = "#852741"
OLIVE = "#9D804C"
OLIVE_LIGHT = "#DAB886"
STEM = "#356250"
MINT = "#80C59F"
BEAD = "#FFF1C0"
ANTHER = "#A16B19"
LENS = "#377471"
SUGAR_RED = RED
SUGAR_BLUE = BLUE
TRAY = "#55443F"
SHEET = np.array([-2.45, 0.06, 0])
FLOWER = SHEET + UP * 0.12
CUPS = [np.array([x, 0.36, 0]) for x in (-4.2, 0, 4.2)]
BEE_QUESTION = "Why do bees visit flowers?"


def pt(x, y):
    return np.array([x, y, 0.0])


def plate(w, h, color, at=ORIGIN, radius=0.18, edge=None):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, fill_color=color,
        fill_opacity=1, stroke_width=2 if edge else 0, stroke_color=edge or color,
    ).move_to(at)


def oval(w, h, color, at=ORIGIN, edge=None):
    return Ellipse(
        width=w, height=h, fill_color=color, fill_opacity=1,
        stroke_width=2 if edge else 0, stroke_color=edge or color,
    ).move_to(at)


def line(a, b, color, width=4):
    return Line(a, b, color=color, stroke_width=width)


def shape(start, segments, fill, edge=None, width=2):
    path = VMobject(fill_color=fill, fill_opacity=1, stroke_color=edge or fill,
                    stroke_width=width if edge else 0)
    path.start_new_path(pt(*start))
    for c1, c2, end in segments:
        path.add_cubic_bezier_curve_to(pt(*c1), pt(*c2), pt(*end))
    path.close_path()
    return path


def tabletop(scene):
    scene.camera.background_color = WOOD
    scene.add(*[
        Polygon(pt(-6.78, y), pt(6.78, y + rise), pt(6.78, y + rise + width * .012),
                pt(-6.78, y + width * .012), fill_color=GRAIN, fill_opacity=1,
                stroke_width=0)
        for y, rise, width in [(-3.54, .15, 3), (-2.26, .11, 1), (-.87, -.1, 2),
                               (.59, .14, 2), (1.86, .13, 1), (3.45, -.12, 3)]
    ])


def sheet():
    shadow = plate(7.35, 6.75, "#1D1615", SHEET + pt(.08, -.09))
    paper = plate(7.35, 6.75, PAPER, SHEET)
    return VGroup(shadow, paper)


def tepal(inner):
    fill, rim, vein = (PINK, PLUM, PINK_LIGHT) if inner else (OLIVE_LIGHT, OLIVE, "#F2D1A7")
    blade = shape((0, .06), [
        ((-.17, .25), (-.75, .74), (-.63, 1.43)),
        ((-.58, 1.83), (-.22, 2.13), (.04, 2.18)),
        ((.32, 2.04), (.70, 1.68), (.64, 1.28)),
        ((.62, .73), (.18, .30), (0, .06)),
    ], fill, rim)
    rib = CubicBezier(pt(.02, .23), pt(.06, .74), pt(-.18, 1.46), pt(.04, 1.97),
                      color=vein, stroke_width=5)
    details = VGroup(rib)
    if inner:
        for x, y in [(-.26, 1.30), (.25, 1.38), (-.30, 1.57), (.27, 1.66), (-.12, 1.77)]:
            details.add(line(pt(x, y), pt(x + .05, y + .12), PLUM, 3))
    return VGroup(blade, details)


def stamen():
    filament = CubicBezier(pt(0, .14), pt(.03, .29), pt(-.07, .61), pt(.07, .80),
                           color=STEM, stroke_width=4)
    head = oval(.24, .38, GOLD, pt(.07, .90), ANTHER).rotate(-.28)
    return VGroup(filament, head)


def top_center():
    return VGroup(oval(.52, .65, STEM), oval(.25, .28, MINT, pt(.01, .09)),
                  Dot(pt(.02, .13), radius=.065, color=BEAD)).shift(FLOWER)


def tape(at, angle=0):
    return plate(.50, .18, "#CCEADE", at, .04).set_fill(opacity=.72).rotate(angle)


def radial_parts(kind, spread=False):
    builders = {"sepals": lambda: tepal(False), "petals": lambda: tepal(True), "stalks": stamen}
    angles = {"sepals": (0, 120, 240), "petals": (60, 180, 300),
              "stalks": (24, 84, 144, 204, 264, 324)}
    scale = {"sepals": .59, "petals": .45, "stalks": .64}
    offset = {"sepals": 1.53, "petals": .91, "stalks": .31}
    parts, strips = VGroup(), VGroup()
    for degrees in angles[kind]:
        a = degrees * DEGREES
        piece = builders[kind]()
        if spread:
            piece.scale(scale[kind], about_point=ORIGIN).shift(UP * offset[kind])
            strips.add(tape(FLOWER + rotate_vector(UP * (offset[kind] + .15), a), a))
        elif kind == "petals":
            piece.scale(.85, about_point=ORIGIN)
        parts.add(piece.rotate(a, about_point=ORIGIN).shift(FLOWER))
    return parts, strips


def bloom():
    return VGroup(*(radial_parts(k)[0] for k in ("sepals", "petals", "stalks")), top_center())


def specimen(cut=False):
    rings = [radial_parts(kind, spread=True) for kind in ("sepals", "petals", "stalks")]
    return VGroup(*(group for ring in rings for group in ring),
                  cut_base(.49).move_to(FLOWER) if cut else top_center())


def lens(at, size=1):
    rim = Circle(radius=.83, stroke_color=LENS, stroke_width=8, fill_opacity=0)
    handle = plate(.22, .95, LENS, pt(.89, -.89), .08).rotate(PI / 4)
    glint = Arc(radius=.66, start_angle=1.75, angle=.67, color="#91CDCA", stroke_width=4)
    return VGroup(handle, rim, glint).scale(size, about_point=ORIGIN).shift(at)


def specks(color, at, n=17, spread=.65, radius=.055, seed=18):
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(n):
        angle = i * 2.399963
        r = spread * np.sqrt((i + .5) / n)
        xy = pt(r * np.cos(angle), .77 * r * np.sin(angle))
        crystal = Square(side_length=radius * rng.uniform(1.1, 2), stroke_width=0,
                         fill_color=color, fill_opacity=1)
        g.add(crystal.rotate(rng.uniform(0, PI)).move_to(at + xy))
    return g


def liner(at):
    flutes = Star(n=24, outer_radius=1.43, inner_radius=1.31, fill_color="#E1CDBA",
                  fill_opacity=1, stroke_width=0)
    lip = Circle(radius=1.19, fill_color="#FFF5E6", fill_opacity=1, stroke_width=0)
    well = Circle(radius=.94, fill_color="#FFF9ED", fill_opacity=1,
                  stroke_color="#DFCDAD", stroke_width=2)
    return VGroup(flutes, lip, well).shift(at)


def swab(at, angle=0):
    shaft = plate(2.54, .10, "#BAAFA0", radius=.04)
    ends = VGroup(oval(.45, .27, "#FFF5E6", LEFT * 1.28),
                  oval(.45, .27, "#FFF5E6", RIGHT * 1.28))
    return VGroup(shaft, ends).rotate(angle, about_point=ORIGIN).shift(at)


def tray_world(filled=True, tool=True):
    tray = VGroup(plate(12.64, 4.36, "#1E1716", pt(.05, .29), .37),
                  plate(12.64, 4.36, TRAY, pt(0, .43), .37, "#9B7461"),
                  plate(12.1, 3.88, "#695048", pt(0, .43), .25))
    cups = VGroup(*(liner(p) for p in CUPS))
    sugar = VGroup(specks(SUGAR_RED, CUPS[0], n=29),
                   specks(SUGAR_BLUE, CUPS[1], n=29, seed=39))
    tool_obj = swab(pt(.2, -1.29), angle=.02)
    return VGroup(tray, cups, sugar if filled else VGroup(), tool_obj if tool else VGroup())


def tape_roll(at):
    outer = Circle(radius=.50, color=LENS, stroke_width=4, fill_color="#9AC5B3", fill_opacity=1)
    inner = Circle(radius=.26, color=LENS, stroke_width=3, fill_color=PAPER, fill_opacity=1)
    return VGroup(outer, inner, plate(.50, .20, "#CDE7DA", pt(.58, -.21), .04)).shift(at)


def scissors(at):
    loops = VGroup(*(Ellipse(width=.44, height=.57, stroke_width=6, color=LENS).move_to(pt(x, -.48))
                     for x in (-.26, .26)))
    blades = VGroup(*(Polygon(pt(-x, -.26), pt(x, .97), pt(x * .39, .86),
                              fill_color="#CED7DB", fill_opacity=1, stroke_color="#657879", stroke_width=2)
                      for x in (-.29, .29)))
    return VGroup(blades, loops, Dot(pt(0, .42), radius=.055, color=LENS)).shift(at)


def prohibition(at, radius=1.15):
    return VGroup(Circle(radius=radius, stroke_color=RED, stroke_width=8),
                  line(pt(-.68, .68) * radius, pt(.68, -.68) * radius, RED, 8)).move_to(at)


def cat(at):
    body = oval(1.35, 1.48, "#7D5350", pt(0, -.35))
    head = oval(1.12, .83, "#7D5350", pt(-.12, .49))
    ears = VGroup(*(Polygon(pt(x - .22, .65), pt(x, 1.22), pt(x + .24, .67),
                            fill_color="#7D5350", fill_opacity=1, stroke_width=0) for x in (-.48, .22)))
    eyes = VGroup(*(Dot(pt(x, .52), radius=.052, color=BEAD) for x in (-.33, .10)))
    tail = CubicBezier(pt(.45, -.74), pt(1.38, -1.15), pt(1.35, -.18), pt(.99, .06),
                       color="#7D5350", stroke_width=12)
    return VGroup(tail, body, ears, head, eyes).shift(at)


def lily(at):
    petals = VGroup()
    for i in range(6):
        blade = shape((0, 0), [
            ((-.36, .43), (-.33, .87), (0, 1.14)),
            ((.26, .91), (.34, .48), (0, 0)),
        ], "#F9DDC6", "#C38578")
        blade.rotate(i * TAU / 6, about_point=ORIGIN)
        petals.add(blade)
    return VGroup(petals, Dot(radius=.17, color=GOLD)).shift(at)


def person(at, adult=False):
    shirt = LENS if adult else PINK
    body = plate(2.08, 1.46, shirt, pt(0, -.65), .55)
    head = oval(1.23, 1.32, "#E9AB83", pt(0, .53), "#A36853")
    hair = Arc(radius=.59, start_angle=.18, angle=2.95, color="#583831", stroke_width=16)
    hair.shift(pt(0, .63))
    face = VGroup(*(Dot(pt(x, .56), radius=.048, color=INK) for x in (-.20, .20)),
                  Arc(radius=.21, start_angle=3.75, angle=1.92, color="#934A43", stroke_width=3).shift(pt(0, .40)))
    g = VGroup(body, head, hair, face)
    if not adult:
        g.scale(.77, about_point=ORIGIN)
    return g.shift(at)


def hand(at, angle=0):
    skin = "#E9AB83"
    palm = oval(.74, .61, skin, edge="#A36853")
    fingers = VGroup(*(plate(.28, .50 - .04 * i, skin, pt(-.27 + .17 * i, .28), .11)
                       for i in range(4)))
    thumb = oval(.27, .45, skin, pt(.36, .04)).rotate(-.58)
    return VGroup(palm, fingers, thumb).rotate(angle, about_point=ORIGIN).shift(at)


def sun(at):
    center = Dot(at, radius=.34, color=YELLOW)
    rays = VGroup(*(line(at + rotate_vector(UP * .47, a), at + rotate_vector(UP * .69, a), GOLD)
                    for a in np.linspace(0, TAU, 8, endpoint=False)))
    return VGroup(center, rays)


def center_side(at):
    body = shape((0, -1.12), [
        ((-.68, -1.07), (-.70, -.29), (-.22, -.10)),
        ((-.03, .07), (-.12, .68), (-.09, 1.11)),
        ((-.42, 1.23), (-.31, 1.49), (0, 1.35)),
        ((.26, 1.48), (.38, 1.23), (.11, 1.11)),
        ((.12, .63), (.05, .08), (.24, -.11)),
        ((.68, -.31), (.66, -1.06), (0, -1.12)),
    ], MINT, STEM, 4)
    vein = CubicBezier(pt(.05, -.90), pt(.30, -.55), pt(.06, -.37), pt(.03, -.18),
                       color=STEM, stroke_width=3)
    return VGroup(body, vein).shift(at)


def cut_base(scale=1):
    at = ORIGIN
    shell = oval(2.0, 1.78, STEM, at)
    flesh = oval(1.80, 1.58, MINT, at)
    chambers = VGroup()
    beads = VGroup()
    for a in (0, TAU / 3, 2 * TAU / 3):
        chambers.add(oval(.52, .74, "#447961", UP * .39).rotate(a, about_point=ORIGIN))
        for x, y in [(-.07, .28), (.10, .43), (-.07, .56)]:
            beads.add(oval(.18, .23, BEAD, pt(x, y), "#D5BB72").rotate(a, about_point=ORIGIN))
    return VGroup(shell, flesh, chambers, beads).scale(scale)


def bee(at):
    gold, dark = "#EDAF46", "#4C3129"
    wing1 = oval(.66, 1.00, "#B9DDDD", pt(-.31, .53), LENS).rotate(.44)
    wing2 = oval(.64, 1.03, "#E3F4EA", pt(.06, .53), LENS).rotate(-.40)
    abdomen = oval(1.53, .94, gold, pt(-.14, 0), dark)
    stripes = VGroup(*(oval(.16, h, dark, pt(x, 0)).rotate(.10)
                       for x, h in [(-.71, .51), (-.44, .78), (-.14, .91)]))
    head = oval(.61, .62, dark, pt(.58, .01))
    eye = Dot(pt(.72, .10), color=PAPER, radius=.077)
    feeler = CubicBezier(pt(.62, .24), pt(.69, .55), pt(.80, .54), pt(.89, .45),
                         color=gold, stroke_width=4)
    hairs = VGroup(*(line(pt(x, y), pt(x + dx, y + dy), gold, 3) for x, y, dx, dy in [
        (-.86, .15, -.11, .07), (-.77, -.24, -.08, -.09), (-.62, -.32, -.06, -.12),
        (-.35, -.41, -.03, -.13), (-.04, -.43, .03, -.13), (.20, -.39, .05, -.11)]))
    g = VGroup(wing1, wing2, abdomen, stripes, head, eye, feeler, hairs).shift(at)
    g.wings = VGroup(wing1, wing2)
    return g


def flutter(insect):
    wings = insect.wings
    base = wings.copy()
    phase = ValueTracker(0)

    def flap(mob, dt):
        phase.increment_value(dt)
        hub = insect.get_center() + pt(-.02, .26)
        target = base.copy().move_to(hub + UP * .19)
        target.stretch(.76 + .24 * np.cos(17 * phase.get_value()), 1, about_point=hub)
        mob.become(target)

    # The wings are also children of the bee so the whole silhouette flies together.
    def update_wings(mob, dt):
        flap(wings, dt)

    insect.add_updater(update_wings)


def side_flower(at):
    stem = CubicBezier(pt(0, -2.6), pt(-.42, -1.87), pt(.35, -1.03), pt(0, -.10),
                      color=MINT, stroke_width=13)
    leaf = shape((-.07, -1.83), [
        ((-.39, -1.80), (-1.54, -1.62), (-1.62, -.86)),
        ((-.95, -.93), (-.33, -1.12), (-.07, -1.83)),
    ], STEM, MINT)
    cup = shape((-1.18, .57), [
        ((-1.02, -.21), (-.50, -.55), (0, -.56)),
        ((.65, -.51), (1.05, -.20), (1.18, .57)),
        ((.65, .22), (-.68, .22), (-1.18, .57)),
    ], PINK, PINK_LIGHT)
    back = oval(2.03, .47, PLUM, pt(0, .37), PINK_LIGHT)
    tip = VGroup(line(pt(0, .03), pt(0, .57), STEM, 6), oval(.24, .15, MINT, pt(0, .59)))
    gold = specks(YELLOW, pt(-.44, .39), n=8, spread=.28, radius=.043)
    return VGroup(stem, leaf, back, cup, tip, gold).shift(at)


def safety_label(text, position, color=TEXT, size=33):
    return boxed_label(text, color=color, size=size, pad=.21).move_to(position)


def ring_question(text, y=-2.90):
    return question_card(text, y=y, size=33)


def question_world():
    insect = bee(ORIGIN).scale(.73, about_point=ORIGIN).shift(pt(2.10, 1.52))
    flower = side_flower(ORIGIN).scale(.38, about_point=ORIGIN).shift(pt(-2.08, 1.61))
    return VGroup(tray_world(), insect, flower)


def bee_question_card():
    return question_card(BEE_QUESTION, y=-2.68, size=38).set_x(0)


def reply_prompt():
    return T("How would you reply?", 30, TEXT).move_to(pt(0, -3.30))


def comparison_bloom(at):
    # Different flower silhouette for the gathering shot: a fused petunia trumpet.
    lobes = VGroup(*(oval(1.45, 1.56, "#AB73B1", rotate_vector(UP * .69, i * TAU / 5), "#784E83")
                     for i in range(5)))
    throat = VGroup(oval(1.2, 1.2, "#6C4779"), oval(.40, .40, "#F2D3E4"))
    return VGroup(lobes, throat).shift(at)


class S01Hook(SpokenScene):
    def construct(self):
        tabletop(self)
        page, flower = sheet(), bloom()
        flower.scale(1.26, about_point=FLOWER)
        glass = lens(pt(4.28, -.70), 1.18)
        question = VGroup(Dot(radius=.39, color=INK),
                          T("?", 43, PAPER, weight=BOLD)).move_to(FLOWER)
        self.add(page, flower)
        self.at("where do seeds")
        self.play(FadeIn(question), flower.animate.scale(1.04, about_point=FLOWER), run_time=1.15)
        self.play(flower.animate.scale(1 / 1.04, about_point=FLOWER), run_time=1.25)
        self.at("take one apart")
        self.play(flower.animate.scale(1 / 1.26, about_point=FLOWER),
                  FadeOut(question, scale=.80), FadeIn(glass, shift=RIGHT * .60), run_time=2.35)
        self.at("where seeds start")
        self.play(glass.animate.shift(pt(-2.12, .99)),
                  flower.animate.rotate(.18, about_point=FLOWER), run_time=1.30)
        self.play(glass.animate.shift(pt(2.12, -.99)),
                  flower.animate.rotate(-.18, about_point=FLOWER), run_time=1.63)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Take a Flower Apart: Parent Guide"
    LESSON = "Take a Flower Apart"

    def construct(self):
        tabletop(self)
        flower = bloom()
        self.add(sheet(), flower, lens(pt(4.28, -.70), 1.18))
        title = T(self.TITLE.split(": ")[0], 37, PAPER, font=TITLE_FONT).move_to(pt(3.96, 1.68))
        sub = T(self.TITLE.split(": ")[1], 32, GOLD).move_to(pt(3.96, 1.05))
        self.play(FadeIn(title), FadeIn(sub), flower.animate.rotate(.025, about_point=FLOWER), run_time=.55)
        self.play(flower.animate.rotate(-.025, about_point=FLOWER), run_time=.9)
        self.play(FadeOut(title), FadeOut(sub), run_time=.45)


class S03Payoff(SpokenScene):
    def construct(self):
        tabletop(self)
        flower = bloom()
        glass = lens(pt(4.28, -.70), 1.18)
        self.add(sheet(), flower, glass)
        self.at("looking closely")
        self.play(glass.animate.move_to(pt(-2.58, 1.18)), run_time=1.40)
        self.at("sorting pieces")
        rings = VGroup(*(DashedVMobject(Circle(radius=r, color="#A38C76", stroke_width=2).move_to(FLOWER),
                                        num_dashes=36, dashed_ratio=.32)
                         for r in (2.94, 2.28, 1.28)))
        self.play(FadeIn(rings), glass.animate.shift(pt(-.13, -1.60)), run_time=2.50)
        self.at("making a guess")
        self.play(glass.animate.shift(pt(.98, -.56)), run_time=2.45)
        self.at("peel one flower")
        self.play(glass.animate.move_to(pt(4.75, 2.09)).scale(.75), run_time=1.58)
        self.at("then play")
        mini = tray_world(tool=False).scale(.39).move_to(pt(3.81, -.60))
        self.play(FadeIn(mini, shift=RIGHT * .70), run_time=1.55)
        self.finish()


class S04Gather(SpokenScene):
    def construct(self):
        tabletop(self)
        first = bloom().shift(-FLOWER).scale(1.10).move_to(pt(-2.72, .02))
        second = comparison_bloom(pt(2.91, .14))
        self.add(first)
        self.at("single flowers")
        self.play(FadeIn(second, shift=RIGHT * .60), run_time=1.0)
        self.play(Rotate(first, .14), Rotate(second, -.16), run_time=2.55)
        self.at("if a cat")
        pet = cat(pt(-3.20, .22)).scale(1.15, about_point=pt(-3.2, .22))
        forbidden = lily(pt(2.82, .32)).scale(1.18, about_point=pt(2.82, .32))
        warning = prohibition(pt(2.82, .32), 1.52)
        question = safety_label("Cat lives here or visits?", pt(-2.85, 2.60))
        no_lilies = safety_label("No lilies or daylilies", pt(2.82, -2.07), RED)
        self.play(FadeOut(first), FadeOut(second), FadeIn(pet), FadeIn(forbidden), run_time=.68)
        self.play(FadeIn(question), pet.animate.shift(RIGHT * .24), run_time=1.23)
        self.at("never bring in")
        self.play(Create(warning), FadeIn(no_lilies), run_time=1.05)
        self.at("even pollen")
        pollen = specks(YELLOW, pt(.86, .92), n=12, spread=.42, radius=.075)
        water = shape((0, .48), [
            ((-.09, .21), (-.44, -.11), (-.34, -.35)),
            ((-.24, -.66), (.26, -.64), (.36, -.32)),
            ((.42, -.11), (.13, .20), (0, .48)),
        ], BLUE).scale(1.53).shift(pt(.87, -.58))
        self.play(FadeIn(pollen, shift=DOWN * .30), run_time=.70)
        self.play(GrowFromCenter(water), run_time=.63)
        self.play(pollen.animate.shift(LEFT * 1.03), water.animate.shift(LEFT * 1.03),
                  run_time=1.06)
        self.at("add paper tape")
        writing = sheet()
        roll = tape_roll(pt(-3.83, .94))
        self.play(FadeOut(VGroup(pet, forbidden, warning, pollen, water, question, no_lilies)),
                  FadeIn(writing, shift=LEFT * .45), FadeIn(roll, shift=RIGHT * .35), run_time=.84)
        glass, snips = lens(pt(-2.21, -.79), .77), scissors(pt(-.05, .48)).rotate(.35)
        self.at("a hand lens")
        self.play(FadeIn(glass, shift=UP * .33), FadeIn(snips, shift=RIGHT * .35), run_time=1.38)
        self.at("gather 3 liners")
        mini = tray_world().scale(.40).move_to(pt(3.86, -.06))
        self.play(FadeIn(mini, shift=RIGHT * .63), run_time=2.30)
        self.finish()


class S05Safety(SpokenScene):
    def construct(self):
        tabletop(self)
        page = sheet()
        adult, child = person(pt(-4.77, 1.49), True), person(pt(-1.49, 1.20))
        self.add(page, adult, child)
        self.at("stay with your child")
        self.play(adult.animate.shift(RIGHT * .50), child.animate.shift(LEFT * .35), run_time=2.58)
        self.at("do all cutting")
        snips = scissors(pt(-4.10, -1.25)).rotate(.84)
        adult_hand = hand(snips[1].get_center() + pt(-.32, -.07), -1.05)
        glass = lens(pt(-2.42, -1.25), .63)
        self.play(FadeIn(snips, shift=LEFT * .40), FadeIn(adult_hand, shift=LEFT * .40), run_time=.96)
        self.play(FadeIn(glass, shift=UP * .48), run_time=1.26)
        self.at("keep swabs sugar")
        small = VGroup(swab(pt(3.82, 1.73), -.16),
                       specks(SUGAR_RED, pt(3.20, .52), n=14, spread=.41),
                       specks(SUGAR_BLUE, pt(4.33, .52), n=14, spread=.41),
                       tepal(True).scale(.44).rotate(.68).move_to(pt(3.76, -.49)))
        self.play(FadeIn(small, shift=RIGHT * .50), run_time=1.36)
        away = safety_label("Keep away from\nchildren under 4", pt(3.81, -1.91), size=30)
        self.at("away from children")
        self.play(FadeIn(away), run_time=.85)
        self.at("keep them out")
        self.play(small.animate.scale(.83).shift(UP * .41), child.animate.shift(LEFT * .27), run_time=2.1)
        self.at("call 911 if choking")
        call = safety_label("Call 911 if choking", pt(3.81, -1.91), RED, 31)
        self.play(swap(away, call), run_time=1.45)
        self.at("never point the lens")
        solar = sun(pt(4.68, .81))
        ban = prohibition(pt(4.68, .81), .90)
        self.play(FadeOut(small), FadeOut(call), FadeIn(solar), glass.animate.shift(LEFT * .12), run_time=.64)
        self.play(Create(ban), run_time=.96)
        self.finish()


class S06Rings(SpokenScene):
    def construct(self):
        tabletop(self)
        sepals, petals, stalks = (radial_parts(kind)[0] for kind in ("sepals", "petals", "stalks"))
        core = top_center()
        glass = lens(pt(.03, -.35), .86)
        self.add(sheet(), sepals, petals, stalks, core, glass)
        self.at("inspect one flower")
        self.play(glass.animate.shift(pt(-2.0, 1.32)), run_time=1.55)
        self.at("count its petals")
        for petal in petals:
            self.play(petal.animate.scale(1.16, about_point=FLOWER),
                      run_time=.31, rate_func=there_and_back)
        self.play(glass.animate.shift(pt(-.96, -.55)), run_time=.48)
        self.at("in the very middle")
        self.play(glass.animate.shift(pt(.50, -.30)), run_time=.64)
        self.play(FadeOut(glass), run_time=.29)
        sp, st = radial_parts("sepals", True)
        pp, tape_p = radial_parts("petals", True)
        self.at("peel the outer")
        self.play(Transform(sepals, sp, path_arc=-.17), run_time=.85)
        sep_label = T("Sepals", 36, BEAD).move_to(pt(3.74, 1.68))
        pet_label = T("Petals", 36, PINK_LIGHT).move_to(pt(3.74, .63))
        self.play(FadeIn(sep_label), run_time=.32)
        self.at("then the petals")
        self.play(Transform(petals, pp, path_arc=.17), FadeIn(pet_label), run_time=.86)
        self.at("taping each ring")
        self.play(FadeIn(st), FadeIn(tape_p), run_time=.90)
        dark_paper = plate(4.02, 2.39, "#211C23", pt(3.76, -.61), .15)
        dust = specks(YELLOW, pt(3.34, -.54), n=24, spread=.66, radius=.043)
        dab = stamen().scale(1.45).rotate(-PI / 2, about_point=ORIGIN).shift(pt(2.22, -.39))
        self.at("dab the thin stalks")
        self.play(FadeOut(sep_label), FadeOut(pet_label), run_time=.23)
        self.play(FadeIn(dark_paper), FadeIn(dab, shift=UP * .43), run_time=.47)
        self.play(dab.animate.shift(DOWN * .15), run_time=.56)
        self.at("spot powdery pollen")
        pollen_label = place_label(T("Pollen", 36, YELLOW), dark_paper, dirs=(DOWN,), buff=.25)
        self.play(FadeIn(dust), dab.animate.shift(UP * .59), run_time=.80)
        self.play(FadeIn(pollen_label), run_time=.43)
        poles, clips = radial_parts("stalks", True)
        self.at("then tape them next")
        self.play(Transform(stalks, poles, path_arc=-.13), FadeOut(dab), run_time=.79)
        self.play(FadeIn(clips), FadeOut(VGroup(dark_paper, dust, pollen_label)), run_time=.68)
        self.finish()


class S07MiddleIdea(SpokenScene):
    def construct(self):
        tabletop(self)
        show = specimen()
        self.add(sheet(), show)
        ask = question_card("Where do you think\nseeds will grow?", size=33,
                            max_w=5.0, left=1.62, y=2.60)
        center = center_side(pt(3.69, .63))
        self.at("where do you think")
        self.play(FadeIn(ask), TransformFromCopy(show[-1], center), run_time=1.46)
        self.at("slice across the base")
        hand_tool = VGroup(hand(pt(5.10, -.13), -.68),
                           scissors(pt(4.66, -.17)).scale(.61).rotate(PI / 2))
        sliced = cut_base(1.03).move_to(pt(3.65, -.37))
        self.play(FadeOut(ask), FadeIn(hand_tool, shift=RIGHT * .34), run_time=.58)
        self.play(hand_tool.animate.shift(LEFT * .39), run_time=.67)
        self.play(FadeOut(hand_tool), center.animate.move_to(pt(4.85, 2.25)).scale(.55),
                  FadeIn(sliced, shift=DOWN * .26), run_time=.75)
        tiny = cut_base(.49).move_to(FLOWER)
        self.at("tape the pieces down")
        self.play(ReplacementTransform(show[-1], tiny), FadeIn(tape(FLOWER + pt(-.26, -.39), .30)),
                  run_time=1.02)
        self.at("look for pale beads")
        crop = lens(pt(3.30, -.54), 1.57)
        bead_mark = place_label(T("Pale beads", 34, BEAD), crop, dirs=(DOWN,), buff=.16)
        self.play(FadeIn(crop, shift=RIGHT * .65),
                  sliced.animate.scale(1.28).move_to(pt(3.30, -.54)), run_time=1.0)
        self.play(FadeIn(bead_mark), run_time=.47)
        self.at("pollen lands on the tip")
        tip = center.get_top() + DOWN * .07
        pollen = Dot(tip + pt(1.05, .21), radius=.104, color=YELLOW)
        self.play(FadeIn(pollen), run_time=.27)
        self.play(pollen.animate.move_to(tip), run_time=.88)
        self.at("the beads inside")
        self.play(VGroup(crop, sliced).animate.scale(1.12, about_point=crop.get_bottom()),
                  run_time=1.78)
        self.finish()


def sugar_packet(at):
    bag = plate(1.33, 1.40, "#CC9C85", at, .13, "#F0C5AB")
    band = plate(1.11, .18, "#F4D8BD", at + UP * .49, .04)
    label = plate(.96, .64, PAPER, at + DOWN * .04, .08)
    marks = VGroup(*(line(at + pt(-.30, y), at + pt(.30, y), "#815D50", 2)
                     for y in (.12, -.02, -.16)))
    return VGroup(bag, band, label, marks)


class S08PredictQ(SpokenScene):
    def construct(self):
        tabletop(self)
        world = question_world()
        self.add(sheet())
        page = self.mobjects[-1]
        sample = specimen(cut=True)
        self.add(sample)
        self.at("use colored sugar")
        self.play(FadeOut(VGroup(page, sample), shift=LEFT * 2.35),
                  FadeIn(world, shift=RIGHT * 2.42), run_time=2.08)
        product = sugar_packet(pt(-2.45, -2.71))
        check = T("Check for allergies", 33, TEXT).move_to(pt(1.0, -2.70))
        self.at("check the label")
        self.play(FadeIn(product, shift=DOWN * .24), run_time=.67)
        self.play(FadeIn(check), product.animate.rotate(-.17), run_time=1.32)
        self.at("never taste plants")
        no_taste = T("Never taste plants or sugar", 33, TEXT).move_to(pt(1.39, -2.70))
        self.play(swap(check, no_taste), product.animate.rotate(.30).shift(LEFT * .46),
                  run_time=1.02)
        self.at("do not blow")
        no_blow = T("Do not blow on the sugar", 33, TEXT).move_to(pt(1.44, -2.70))
        self.play(swap(no_taste, no_blow),
                  product.animate.rotate(-.13).shift(RIGHT * .46).scale(1.17), run_time=.86)
        self.play(product.animate.scale(1 / 1.17), run_time=.50)
        self.at("why bees visit flowers")
        q = bee_question_card()
        self.play(FadeOut(product), swap(no_blow, q), world[1].animate.shift(pt(-.34, .13)), run_time=1.35)
        self.at("what might your child say")
        self.play(FadeIn(reply_prompt()), world[1].animate.shift(pt(.34, -.13)), run_time=1.64)
        self.finish()


def pause_bar():
    start, end = pt(-1.43, -3.60), pt(1.43, -3.60)
    track = line(start, end, "#8B6B5C", 4)
    fill = line(start, end, GOLD, 4)
    return track, fill


class S09PredictPause(PredictPause):
    SECONDS = 4.5

    def backdrop(self):
        return question_world()

    def construct(self):
        tabletop(self)
        world = self.backdrop()
        track, fill = pause_bar()
        self.add(world, bee_question_card(), reply_prompt(), track)
        insect = world[1]
        anchor = insect.get_center().copy()

        def figure_eight(mob, alpha):
            a = TAU * alpha
            lift = .34 * (1 - np.cos(a))
            mob.move_to(anchor + pt(.18 * np.sin(a), lift + .15 * np.sin(2 * a)))

        self.play(UpdateFromAlphaFunc(insect, figure_eight), Create(fill),
                  run_time=self.SECONDS, rate_func=linear)


class S10PredictReveal(SpokenScene):
    def construct(self):
        tabletop(self)
        world = question_world()
        q = bee_question_card()
        reply = reply_prompt()
        bar = VGroup(*pause_bar())
        self.add(world, q, reply, bar)
        left, right = pt(-3.86, -.18), pt(3.70, -.18)
        first, second = side_flower(left), side_flower(right)
        second[-1].set_opacity(0)
        insect = world[1]
        insect_target = bee(pt(-4.99, 1.14)).scale(1.26)
        self.at("your child might say")
        self.play(FadeOut(VGroup(q, reply, bar)), run_time=.42)
        self.play(FadeOut(VGroup(world[0], world[2])),
                  FadeIn(first, shift=UP * .20), FadeIn(second, shift=UP * .20),
                  Transform(insect, insect_target, path_arc=.18), run_time=2.12)
        self.bring_to_front(insect)
        self.at("bees visit for food")
        food = T("Bees come for food", 38, BEAD).move_to(pt(.0, 2.94))
        self.play(insect.animate.shift(pt(.45, -.36)), run_time=.72)
        self.play(FadeIn(food), run_time=.53)
        self.at("they collect nectar")
        head = insect[4]
        mouth = head.get_center() + pt(.32 * head.width, -.37 * head.height)
        sip = line(mouth, mouth + DOWN * .30, GOLD, 4)
        nectar = oval(.16, .11, BLUE, sip.get_end())
        self.play(Create(sip), run_time=.33)
        self.play(FadeIn(nectar), run_time=.24)
        self.wait(.52)
        self.play(nectar.animate.move_to(mouth), run_time=.51)
        self.play(FadeOut(nectar), FadeOut(sip), run_time=.35)
        self.at("as a bee visits flowers")
        flutter(insect)
        self.play(insect.animate.shift(pt(.41, -.46)), run_time=1.09)
        self.at("pollen sticks")
        hair_dust = specks(YELLOW, insect.get_center() + pt(-.33, -.34),
                           n=10, spread=.49, radius=.060)
        placed = hair_dust.copy()
        placed.move_to(left + pt(-.43, .39))
        self.play(TransformFromCopy(first[-1], placed), run_time=.25)
        self.play(Transform(placed, hair_dust), run_time=.37)
        self.bring_to_front(placed)
        flight = VGroup(insect, placed)
        target = flight.get_center() + pt(6.67, -.06)
        self.play(flight.animate(path_arc=-.33).move_to(target), run_time=1.10)
        self.at("rubs off on the next flower")
        grains = specks(YELLOW, right + pt(0, .59), n=6, spread=.19, radius=.038)
        self.play(TransformFromCopy(placed, grains, path_arc=-.17), run_time=.69)
        self.play(flight.animate.shift(pt(.56, .94)), run_time=.70)
        self.finish()


def game_result(magnification=1):
    result = VGroup(specks(SUGAR_RED, CUPS[2] + pt(-.20, .09), n=9, spread=.38, radius=.082),
                  specks(SUGAR_BLUE, CUPS[2] + pt(.19, -.08), n=9, spread=.37, radius=.082, seed=39))
    return result.scale(magnification, about_point=CUPS[2])


def game_lens():
    return lens(CUPS[2], 1.42)


def wand_at(contact, angle=-.31):
    return swab(contact - rotate_vector(RIGHT * 1.28, angle), angle)


class S11BeeGame(SpokenScene):
    def construct(self):
        tabletop(self)
        full = tray_world(tool=False)
        base, cups, sugar, _ = full
        self.add(base)
        self.at("put the liners")
        self.play(FadeIn(cups, shift=UP * .37), run_time=1.64)
        self.at("a small spoonful")
        self.play(FadeIn(sugar[0], shift=DOWN * .59), run_time=1.06)
        self.play(FadeIn(sugar[1], shift=DOWN * .59), run_time=1.16)
        self.at("leave the third empty")
        rim = Circle(radius=1.62, color=GOLD, stroke_width=4).move_to(CUPS[2])
        self.play(cups[2].animate.scale(1.13).shift(UP * .24), run_time=.57,
                  rate_func=there_and_back)
        self.play(Create(rim), run_time=1.02)
        self.at("what will the empty flower")
        guess = ring_question("What will the empty flower look like?")
        self.play(FadeIn(guess), run_time=.70)
        wand = wand_at(CUPS[0] + pt(.30, 1.32), -.70)
        self.play(FadeIn(wand, shift=UP * .36), run_time=1.12)
        self.at("child dab each liner")
        red_position = CUPS[0] + pt(.68, .21)
        blue_position = CUPS[1] + pt(.04, .13)
        last_position = CUPS[2] + pt(-.16, .15)
        self.play(FadeOut(guess), FadeOut(rim),
                  Transform(wand, wand_at(red_position)), run_time=.36)
        load = specks(SUGAR_RED, red_position, n=6, spread=.11, radius=.050)
        self.add(load)
        self.play(Transform(wand, wand_at(blue_position), path_arc=-.8),
                  load.animate(path_arc=-.8).move_to(blue_position), run_time=.70)
        red_drop = specks(SUGAR_RED, CUPS[1] + pt(.31, .30), n=6, spread=.26)
        loaded = VGroup(load, specks(SUGAR_BLUE, blue_position + pt(.08, .07), n=6,
                                     spread=.12, radius=.05, seed=39))
        self.add(red_drop, loaded[1])
        self.play(Transform(wand, wand_at(last_position), path_arc=-.8),
                  loaded.animate(path_arc=-.8).shift(last_position - blue_position), run_time=.76)
        result = game_result(.70)
        self.play(FadeOut(wand, shift=UP * .51), FadeOut(loaded, shift=UP * .44),
                  FadeIn(result), run_time=.48)
        self.play(FadeIn(game_lens(), shift=RIGHT * .45),
                  result.animate.scale(1 / .70, about_point=CUPS[2]), run_time=.63)
        self.finish()


def washing(at):
    drop = shape((0, .45), [
        ((-.13, .15), (-.35, -.08), (-.31, -.24)),
        ((-.24, -.61), (.25, -.61), (.31, -.24)),
        ((.36, -.06), (.14, .22), (0, .45)),
    ], BLUE)
    drops = VGroup(*(drop.copy().scale(s).move_to(pt(x, y))
                     for s, x, y in [(.95, -.51, .64), (.65, .23, .82), (.52, .73, .46)]))
    palms = VGroup(hand(pt(-.44, -.38), .55), hand(pt(.51, -.39), -.61))
    return VGroup(palms, drops).shift(at)


def ring_highlight(radius, color):
    return DashedVMobject(Circle(radius=radius, color=color, stroke_width=4).move_to(FLOWER),
                          num_dashes=38, dashed_ratio=.44)


class S12Wrap(SpokenScene):
    def construct(self):
        tabletop(self)
        world = tray_world(tool=False)
        world[2].add(specks(SUGAR_RED, CUPS[1] + pt(.31, .30), n=6, spread=.26))
        result = game_result()
        glass = game_lens()
        self.add(world, result, glass)
        self.at("look for both colors")
        self.play(glass.animate.shift(pt(-.26, .13)), run_time=1.91)
        self.at("toss the sugar")
        page = sheet()
        done = specimen(cut=True)
        done.add(tape(FLOWER + pt(-.26, -.39), .30))
        self.play(FadeOut(VGroup(world, result, glass), shift=RIGHT * 1.86),
                  FadeIn(VGroup(page, done), shift=LEFT * .63), run_time=.80)
        self.at("wash hands together")
        wash = washing(pt(3.78, .53)).scale(1.70)
        self.play(FadeIn(wash), run_time=.56)
        self.play(wash[0][0].animate.shift(RIGHT * .25), wash[0][1].animate.shift(LEFT * .23),
                  wash[1].animate.shift(DOWN * .34), run_time=1.25)
        self.at("point to where seeds begin")
        pointer = hand(pt(-.96, -.64), 1.35).scale(1.22)
        sample = cut_base(1.30).move_to(pt(3.70, .37))
        self.play(FadeOut(wash), FadeIn(pointer, shift=RIGHT * .60),
                  TransformFromCopy(done[-2], sample), run_time=1.12)
        self.at("petals can attract animals")
        petal_ring = ring_highlight(1.99, PINK)
        petal_label = T("Petals", 38, PINK_LIGHT).move_to(pt(3.67, 1.64))
        pollinator = bee(pt(4.89, -.15)).rotate(PI, axis=UP, about_point=pt(4.89, -.15))
        self.play(FadeOut(VGroup(pointer, sample)), Create(petal_ring), run_time=.63)
        self.play(FadeIn(petal_label), FadeIn(pollinator, shift=RIGHT * .38), run_time=.60)
        self.play(pollinator.animate.shift(pt(-1.0, .07)), run_time=.83)
        self.at("make the pollen")
        stalk_ring = ring_highlight(1.13, ANTHER)
        stalk_label = T("Pollen stalks", 38, YELLOW).move_to(pt(3.67, 1.64))
        enlarged = stamen().scale(2.02).rotate(-.63).move_to(pt(4.51, -.09))
        self.play(FadeOut(petal_ring), Create(stalk_ring), swap(petal_label, stalk_label),
                  FadeIn(enlarged), pollinator.animate.shift(LEFT * .74), run_time=.77)
        dust = specks(YELLOW, pt(4.02, .35), n=9, spread=.29)
        self.play(FadeIn(dust), run_time=.47)
        self.play(dust.animate.shift(pt(-1.12, -.60)), run_time=.76)
        self.finish()


class S13End(EndCard):
    LINE = "Flowers make seeds, and pollen must travel for seeds to grow."
