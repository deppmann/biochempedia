"""Rot Detectives, illustrated as a forest floor and a shelf of sealed tubs."""

from bp_parts import *


# COLOR MAP: teal for looking and clear plastic, gold for questions and guesses,
# green for living growth, red for safety, warm browns for leaf litter and soil.
GLASS = "#344C59"
RIM = "#8CBCC6"
WOOD = "#975F43"
SOIL = "#563827"
DIRT = "#B27953"
LEAVES = ("#E49B48", "#C86A40", "#AA5434", "#F1BD63")
APPLE = "#F4CC8A"
CRUST = "#BB7541"
MOLD = "#9CB797"
TAPE = "#B3DECE"
SKIN = "#E4AB86"
PAPER = "#E5CCA2"
SLOTS = (-5.04, -2.52, 0, 2.52, 5.04)
ITEMS = ("apple", "leaf", "bread", "cap", "apple")

FILM_TITLE = "Rot Detectives: Parent Guide"
LESSON_TITLE = "Rot Detectives"
PREDICTION = "Which will change?\nWhich will not?"
PREDICTION_LAYOUT = dict(left=-6.12, y=2.81, size=34, max_w=6.5)


def xy(x, y):
    return np.array([x, y, 0.0])


def block(w, h, x, y, color, edge=None, radius=0.14, opacity=1):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, stroke_width=2 if edge else 0,
        stroke_color=edge or color, fill_color=color, fill_opacity=opacity,
    ).move_to(xy(x, y))


def shape(points, fill, edge=None, width=2):
    return Polygon(
        *(xy(*p) for p in points), fill_color=fill, fill_opacity=1,
        stroke_color=edge or fill, stroke_width=width if edge else 0,
    )


def line(x1, y1, x2, y2, color, width=3):
    return Line(xy(x1, y1), xy(x2, y2), color=color, stroke_width=width)


def disc(x, y, radius, color):
    return Dot(xy(x, y), radius=radius, color=color)


def leaf(color=LEAVES[0]):
    left, right = xy(-0.62, 0), xy(0.62, 0)
    blade = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    blade.start_new_path(left)
    blade.add_cubic_bezier_curve_to(xy(-0.28, 0.56), xy(0.28, 0.44), right)
    blade.add_cubic_bezier_curve_to(xy(0.12, -0.47), xy(-0.32, -0.43), left)
    blade.close_path()
    vein = VGroup(line(-0.69, -0.04, 0.43, 0.015, SOIL, 2.2))
    for x in (-0.32, -0.06, 0.18):
        vein.add(line(x, 0, x + 0.16, 0.14, SOIL, 1.2),
                 line(x, 0, x + 0.16, -0.12, SOIL, 1.2))
    return VGroup(blade, vein)


def apple(rotted=False):
    rind = shape([(-0.78, 0.27), (-0.37, 0.60), (0.12, 0.69), (0.62, 0.49),
                  (0.81, 0.15), (0.67, -0.27), (0.43, -0.54), (-0.48, -0.54)], "#B85239")
    flesh = shape([(-0.66, 0.26), (-0.33, 0.49), (0.11, 0.58), (0.54, 0.39),
                   (0.69, 0.13), (0.55, -0.24), (0.36, -0.46), (-0.43, -0.46)],
                  "#B07C53" if rotted else APPLE)
    seeds = VGroup(disc(-0.17, -0.11, 0.064, SOIL), disc(0.02, -0.08, 0.052, SOIL))
    spots = VGroup(*[disc(x, y, r, c) for x, y, r, c in
                     [(-0.37, 0.24, 0.13, SOIL), (0.41, 0.13, 0.17, "#69493B"),
                      (0.24, -0.22, 0.09, SOIL), (-0.22, 0.33, 0.06, "#D8A672")]])
    return VGroup(rind, flesh, seeds, spots) if rotted else VGroup(rind, flesh, seeds)


def fuzz(x, y, size):
    patch = VGroup(disc(0, 0, 0.35, "#546A5A"))
    for k in range(18):
        angle = k * TAU / 18
        radius = 0.29 + 0.06 * np.sin(k * 9)
        patch.add(disc(radius * np.cos(angle), radius * np.sin(angle), 0.086,
                       (MOLD, "#7C927D", "#647B6C")[k % 3]))
    patch.add(disc(-0.07, 0.04, 0.15, "#BCC7A3"), disc(0.12, -0.07, 0.10, "#A4AE8D"))
    return patch.scale(size).move_to(xy(x, y))


def bread():
    outer = block(1.30, 0.91, 0, -0.11, CRUST, radius=0.15)
    top = Ellipse(width=1.52, height=0.68, fill_color=CRUST, fill_opacity=1,
                  stroke_width=0).move_to(UP * 0.33)
    crumb = block(1.10, 0.76, 0, -0.085, "#F3DBA9", radius=0.10)
    crown = Ellipse(width=1.28, height=0.50, fill_color="#F3DBA9", fill_opacity=1,
                    stroke_width=0).move_to(UP * 0.30)
    pores = VGroup(*[disc(x, y, r, "#C99E71") for x, y, r in
                     [(-0.4, 0.14, 0.038), (-0.28, -0.19, 0.045), (0.17, 0.31, 0.035),
                      (0.28, -0.08, 0.045), (0.42, 0.18, 0.036), (-0.05, 0.05, 0.041)]])
    return VGroup(outer, top, crumb, crown, pores)


def cap():
    side = block(1.26, 0.47, 0, -0.07, "#27768E", radius=0.12)
    ribs = VGroup(*[line(x, -0.13, x, -0.24, BLUE, 2) for x in np.linspace(-0.49, 0.49, 9)])
    top = Ellipse(width=1.26, height=0.43, fill_color=BLUE, fill_opacity=1,
                  stroke_color=RIM, stroke_width=2).move_to(UP * 0.13)
    seal = Ellipse(width=0.90, height=0.26, stroke_color="#27768E", stroke_width=2).move_to(top)
    return VGroup(side, ribs, top, seal)


def item(index, changed=False):
    name = ITEMS[index]
    if name == "apple":
        picture = apple(rotted=changed)
        if index == 4:
            picture.flip(UP)
    elif name == "leaf":
        picture = leaf(LEAVES[2]).rotate(-0.22).scale(1.1)
    elif name == "bread":
        picture = bread()
        if changed:
            picture.add(fuzz(-0.28, 0.22, 0.67), fuzz(0.28, -0.10, 0.57))
    else:
        picture = cap()
    return picture


def soil(x):
    bed = shape([(-1.0, -1.23), (-1.06, -0.83), (-0.73, -0.73), (-0.3, -0.76),
                 (0.1, -0.65), (0.52, -0.69), (1.06, -0.81), (1.0, -1.23)], SOIL)
    grains = VGroup(*[disc(a, b, r, DIRT) for a, b, r in
                      [(-0.83, -0.94, 0.045), (-0.61, -1.13, 0.045), (-0.46, -0.89, 0.032),
                       (-0.19, -1.00, 0.054), (0.06, -0.84, 0.037), (0.25, -1.10, 0.047),
                       (0.50, -0.92, 0.054), (0.78, -1.09, 0.039), (0.83, -0.89, 0.035)]])
    return VGroup(bed, grains).shift(RIGHT * x)


def tape_at(x):
    band = block(2.19, 0.62, x, 1.37, TAPE, edge=TAPE, radius=0.12, opacity=0.25)
    folds = VGroup(line(x - 1.01, 1.11, x - 1.01, 1.58, TAPE, 2.2),
                   line(x + 1.01, 1.11, x + 1.01, 1.58, TAPE, 2.2),
                   line(x - 0.97, 1.11, x + 0.97, 1.11, TAPE, 1.6))
    return VGroup(band, folds)


def tub(x):
    body = shape([(-1.10, 1.37), (1.10, 1.37), (1.00, -1.10), (0.86, -1.24),
                  (-0.86, -1.24), (-1.00, -1.10)], GLASS, RIM)
    glare = VGroup(line(-0.91, 0.94, -0.87, 0.19, RIM, 2),
                   line(0.87, 0.39, 0.85, 0.03, RIM, 1.5))
    lid = VGroup(block(2.28, 0.32, 0, 1.45, "#6596A5", edge=RIM, radius=0.10),
                 line(-0.96, 1.52, 0.96, 1.52, "#C0D9DC", 2))
    VGroup(body, glare, lid).shift(RIGHT * x)
    return VGroup(body, glare), lid


def shelf(contents=0, soil_count=0, sealed=False, changed=False, lids=True):
    """Build the same five stations and their independent layers in every scene."""
    scene = VGroup()
    scene.board = VGroup(block(12.92, 0.35, 0, -1.43, WOOD, radius=0.10),
                         line(-6.30, -1.29, 6.30, -1.29, "#CE8D62", 3))
    scene.bodies, scene.lids, scene.beds = VGroup(), VGroup(), VGroup()
    scene.samples, scene.tapes, scene.numbers = VGroup(), VGroup(), VGroup()
    for i, x in enumerate(SLOTS):
        body, lid = tub(x)
        scene.bodies.add(body)
        scene.lids.add(lid)
        scene.beds.add(soil(x))
        scene.samples.add(item(i, changed).move_to(xy(x, -0.63)))
        scene.tapes.add(tape_at(x))
        scene.numbers.add(T(str(i + 1), 30, color="#F2C69C", weight=BOLD).move_to(xy(x, -1.94)))
    scene.add(scene.board, scene.bodies, scene.beds[:soil_count], scene.samples[:contents])
    if lids:
        scene.add(scene.lids)
    if sealed:
        scene.add(scene.tapes)
    return scene.add(scene.numbers)


def lens(x=0, y=0.17, scale=1):
    rim = Circle(radius=0.68, stroke_color=TEAL, stroke_width=7,
                 fill_color=BLUE, fill_opacity=0.12)
    handle = line(0.51, -0.51, 1.03, -1.03, TEAL, 12)
    reflection = Arc(radius=0.50, start_angle=PI * 0.58, angle=PI * 0.32,
                     color="#C6F2EE", stroke_width=3)
    return VGroup(handle, rim, reflection).scale(scale).shift(xy(x, y))


def calendar(text):
    label = T(text, 32, color=TEXT, weight=BOLD).move_to(xy(4.12, 2.55))
    back = block(3.72, 1.24, 4.12, 2.63, "#263B46", edge=RIM, radius=0.13)
    header = block(3.72, 0.28, 4.12, 3.13, WOOD, radius=0.10)
    rings = VGroup(line(3.18, 3.12, 3.18, 3.41, PAPER, 4),
                   line(5.06, 3.12, 5.06, 3.41, PAPER, 4))
    return VGroup(back, header, rings, label)


def journal(changed=False):
    paper = VGroup()
    sketches = VGroup()
    for i, x in enumerate(SLOTS):
        card = block(2.08, 0.96, x, -2.94, PAPER, radius=0.07)
        outline = block(1.23, 0.69, x, -2.92, "#D0B587", edge=WOOD, radius=0.09)
        sample = item(i, changed).scale(0.38).move_to(xy(x, -2.98))
        paper.add(card)
        sketches.add(VGroup(outline, sample))
    star = Star(n=5, outer_radius=0.19, inner_radius=0.086,
                color=SOIL, stroke_width=0, fill_opacity=1).move_to(xy(-0.82, -2.70))
    return paper, sketches, star


def grove(thin=False):
    """The same tree and section of forest floor at the opening and return."""
    ground = shape([(-6.40, -1.94), (-4.50, -1.78), (-2.35, -1.99), (-0.20, -1.82),
                    (2.03, -2.03), (4.45, -1.92), (6.40, -2.02), (6.40, -3.36),
                    (-6.40, -3.36)], SOIL)
    grains = VGroup()
    rng = np.random.default_rng(19)
    for _ in range(44):
        x, y = rng.uniform(-6.25, 6.25), rng.uniform(-3.24, -2.11)
        grains.add(disc(x, y, rng.uniform(0.018, 0.05), DIRT))
    branches = shape([(-4.57, -1.90), (-4.03, -1.59), (-3.93, 0.63), (-4.95, 1.70),
                      (-4.81, 1.87), (-3.75, 1.14), (-3.57, 2.40), (-3.36, 2.38),
                      (-3.46, 0.86), (-2.36, 1.75), (-2.15, 1.67), (-3.40, 0.17),
                      (-3.40, -1.55), (-2.76, -1.91)], WOOD)
    crown = VGroup()
    for x, y, w, h, c in [(-5.13, 1.53, 2.38, 1.68, "#A95436"),
                           (-4.37, 2.28, 2.72, 1.89, "#B6633B"),
                           (-3.34, 2.54, 2.64, 1.90, "#C47740"),
                           (-2.21, 2.16, 2.62, 1.76, "#B9663A"),
                           (-2.10, 1.52, 2.40, 1.50, "#A95537"),
                           (-3.60, 1.78, 2.78, 1.41, "#D99049")]:
        crown.add(Ellipse(width=w, height=h, fill_color=c, fill_opacity=1,
                          stroke_width=0).move_to(xy(x, y)))
    for _ in range(24):
        accent = leaf(LEAVES[rng.integers(0, 4)]).scale(rng.uniform(0.18, 0.41))
        accent.rotate(rng.uniform(-1.2, 1.2)).move_to(xy(rng.uniform(-5.65, -1.1), rng.uniform(1.40, 2.78)))
        crown.add(accent)
    tree = VGroup(branches, crown)
    pile = VGroup()
    for i in range(38):
        x = -5.38 + (i % 14) * 0.42 + rng.uniform(-0.15, 0.15)
        y = -1.72 + (i // 14) * 0.39 + rng.uniform(-0.09, 0.09)
        if thin and i % 3:
            continue
        if thin:
            y = -1.85 + rng.uniform(-0.08, 0.08)
        litter = leaf(LEAVES[i % 4]).rotate(rng.uniform(-0.43, 0.43))
        litter.scale(rng.uniform(0.32, 0.73) if not thin else 0.34).move_to(xy(x, y))
        pile.add(litter)
    return VGroup(ground, grains, tree), pile


def falling_leaf(x, y, color):
    return leaf(color).scale(0.52).rotate(-0.45).move_to(xy(x, y))


def hand():
    fingers = VGroup(*[block(0.24, length, -0.42 + i * 0.24, -0.02 + length / 2,
                             SKIN, radius=0.11) for i, length in enumerate((0.53, 0.74, 0.65, 0.46))])
    palm = block(0.94, 0.68, -0.05, -0.23, SKIN, radius=0.27)
    thumb = block(0.26, 0.57, 0.42, -0.18, SKIN, radius=0.12).rotate(-0.50)
    wrist = block(0.48, 0.33, -0.06, -0.56, SKIN, radius=0.09)
    return VGroup(wrist, palm, fingers, thumb)


def pencil():
    tip = shape([(0, 0), (-0.105, 0.35), (0.105, 0.35)], "#C9A472")
    lead = shape([(0, 0), (-0.04, 0.13), (0.04, 0.13)], GLASS)
    shaft = block(0.21, 1.18, 0, 0.88, GOLD, radius=0.035)
    eraser = block(0.21, 0.27, 0, 1.57, "#D78868", radius=0.056)
    # Pivot at the tip so the pencil stays below the tub numbers as it draws.
    return VGroup(shaft, eraser, tip, lead).scale(0.65, about_point=ORIGIN).rotate(-1.76, about_point=ORIGIN)


def spoon():
    bowl = Ellipse(width=0.86, height=0.42, fill_color=RIM,
                   fill_opacity=1, stroke_width=0).move_to(LEFT * 0.40)
    dirt = Ellipse(width=0.65, height=0.27, fill_color=DIRT,
                   fill_opacity=1, stroke_width=0).move_to(xy(-0.43, 0.06))
    grip = hand().scale(0.52).rotate(PI / 2).shift(xy(1.02, 0))
    return VGroup(line(-0.16, 0, 0.95, 0, RIM, 8), bowl, dirt, grip)


def highlight(x):
    return block(2.37, 3.00, x, 0.17, TEAL, edge=TEAL, radius=0.18, opacity=0).set_stroke(width=4)


def no_mark(icon):
    ring = Circle(radius=0.82, stroke_color=RED, stroke_width=6)
    return VGroup(icon, ring, line(-0.57, 0.57, 0.57, -0.57, RED, 6))


def safety_badge(icon, text, x):
    picture = icon.scale(0.62).move_to(xy(x, 2.88))
    label = T(text, 30, weight=BOLD).move_to(xy(x, 2.07))
    return VGroup(picture, label)


def lock():
    bow = Arc(radius=0.33, start_angle=0, angle=PI, color=TAPE, stroke_width=8).shift(UP * 0.04)
    box = block(0.95, 0.63, 0, -0.17, TAPE, radius=0.12)
    return VGroup(bow, box, disc(0, -0.15, 0.085, GLASS), line(0, -0.16, 0, -0.30, GLASS, 4))


def sniff():
    nose = shape([(-0.19, 0.48), (0.08, 0.43), (0.10, 0.19), (0.43, -0.10),
                  (0.33, -0.23), (-0.05, -0.23), (-0.15, -0.36), (-0.35, -0.24)], SKIN)
    air = VGroup(line(0.48, -0.36, 0.65, -0.43, TEXT, 2),
                 line(0.43, -0.50, 0.54, -0.59, TEXT, 2))
    return no_mark(VGroup(nose, air))


def soap():
    hands = VGroup(hand().scale(0.76).rotate(-0.65).shift(xy(-0.39, -0.12)),
                   hand().scale(0.76).rotate(0.76).shift(xy(0.37, -0.27)))
    bubbles = VGroup(*[Circle(radius=r, stroke_color=BLUE, stroke_width=3).move_to(xy(x, y))
                       for x, y, r in [(-0.40, 0.38, 0.16), (0.03, 0.55, 0.25),
                                       (0.56, 0.37, 0.14), (-0.09, 0.14, 0.11)]])
    return VGroup(hands, bubbles)


class S01Hook(SpokenScene, TitleCard):
    TITLE = FILM_TITLE
    LESSON = LESSON_TITLE

    def construct(self):
        landscape, pile = grove()
        _, thin = grove(thin=True)
        self.add(landscape, pile)
        self.at("trees drop", lead=0.7)
        drops = VGroup(*[falling_leaf(-2.36 + i * 0.64, 1.16 - i * 0.21, LEAVES[i % 4])
                         for i in range(4)])
        self.add(drops)
        self.play(LaggedStart(*(d.animate.shift(xy(0.46, -2.22 + i * 0.19)).rotate(0.91)
                                for i, d in enumerate(drops)), lag_ratio=0.20), run_time=2.65)
        self.at("a year later", lead=0.38)
        old = calendar("Autumn")
        new = calendar("One year later")
        self.play(FadeIn(old), run_time=0.35)
        self.play(swap(old, new, 0.65),
                  FadeOut(drops, shift=DOWN * 0.52), FadeOut(pile, shift=DOWN * 0.28),
                  FadeIn(thin), run_time=2.0)
        self.at("where did they go")
        q = question_card("Where did the\nleaves go?", y=0.32, left=1.45, size=43, max_w=4.9)
        self.play(FadeIn(q, shift=UP * 0.16), run_time=0.46)
        self.at("5 sealed containers")
        small_world = shelf(sealed=True)
        small_world.remove(small_world.numbers)
        small_world.scale(0.34).move_to(xy(3.78, -1.40))
        self.play(FadeIn(small_world, shift=UP * 0.26), run_time=1.9)
        self.finish()


class S02Title(TitleCard):
    TITLE = FILM_TITLE
    LESSON = LESSON_TITLE

    def construct(self):
        landscape, litter = grove(thin=True)
        title = T(self.LESSON, 55, font=TITLE_FONT).move_to(xy(2.79, 0.75))
        subtitle = T(self.TITLE.split(": ", 1)[1], 30, color="#F2C69C").move_to(xy(2.79, 0.04))
        rule = line(1.77, -0.36, 3.81, -0.36, GOLD, 3)
        drift = falling_leaf(-0.58, 2.28, LEAVES[0])
        self.add(landscape, litter, drift)
        self.play(FadeIn(VGroup(title, subtitle, rule), run_time=0.44),
                  drift.animate(run_time=1.94, rate_func=linear).shift(xy(0.58, -1.45)).rotate(0.84))


class S03Payoff(SpokenScene):
    def construct(self):
        world = shelf()
        prep = calendar("About 25 min")
        self.at("set aside")
        self.add(world.board, world.bodies)
        stations = [VGroup(lid, number) for lid, number in zip(world.lids, world.numbers)]
        self.play(LaggedStart(*(FadeIn(station, shift=DOWN * 0.28) for station in stations),
                              lag_ratio=0.24), FadeIn(prep), run_time=2.6)
        self.at("then check")
        weeks = calendar("3–4 weeks")
        cadence = caption("Check twice a week", size=35)
        self.play(swap(prep, weeks, 0.9), FadeIn(cadence), run_time=1.15)
        glass = lens(SLOTS[0])
        self.play(FadeIn(glass), run_time=0.45)
        self.play(glass.animate.shift(RIGHT * 4.92), run_time=2.75)
        self.at("looking closely")
        look = caption("Look closely", size=35)
        self.play(swap(cadence, look, 0.5), glass.animate.shift(RIGHT * 1.45), run_time=0.92)
        self.at("recording changes")
        record = caption("Record changes", size=35)
        self.play(swap(look, record, 0.52), glass.animate.shift(RIGHT * 1.48), run_time=0.85)
        self.at("checking their guesses")
        wait = caption("Wait and check", size=35)
        self.play(swap(record, wait, 0.53), glass.animate.shift(RIGHT * 1.70), run_time=1.16)
        self.play(FadeOut(glass), FadeOut(weeks), FadeOut(wait), run_time=0.45)
        self.finish()


class S04Setup(SpokenScene):
    def construct(self):
        world = shelf(lids=False)
        self.add(world, world.lids)
        self.at("number 5")
        self.play(LaggedStart(*(Indicate(n, color=TEXT, scale_factor=1.16) for n in world.numbers),
                              lag_ratio=0.27), run_time=2.6)
        self.at("put 2", lead=0.67)
        scoop = spoon().move_to(xy(-4.55, 2.25))
        self.play(FadeOut(world.lids[:4], shift=UP * 0.31), FadeIn(scoop), run_time=0.53)
        for i in range(4):
            x = SLOTS[i]
            self.play(scoop.animate.move_to(xy(x + 0.48, 1.80)).rotate(0.52),
                      GrowFromEdge(world.beds[i], DOWN), run_time=0.49)
            if i < 3:
                self.play(scoop.animate.move_to(xy(x + 2.98, 2.16)).rotate(-0.52), run_time=0.52)
        self.play(FadeOut(scoop, shift=UP * 0.31), run_time=0.36)
        self.at("use 1 item")
        guide = caption("One item per tub", size=35)
        self.play(FadeIn(guide), run_time=0.58)
        self.wait(0.70)
        self.play(FadeOut(guide), run_time=0.36)
        active = None
        cues = ("half an apple", "a dry leaf", "bread", "bottle cap")
        names = ("Half an apple slice", "Dry leaf", "Bread", "Bottle cap")
        for index, (cue, name) in enumerate(zip(cues, names)):
            self.at(cue, lead=0.56)
            sample = world.samples[index]
            self.play(FadeIn(sample, shift=DOWN * 2.07), run_time=0.40)
            label = caption(name, size=34)
            if active is None:
                self.play(FadeIn(label), run_time=0.21)
            else:
                self.play(swap(active, label, 0.24))
            active = label
        self.wait(1.15)
        self.play(FadeOut(active), run_time=0.41)
        self.finish()


class S05Seal(SpokenScene):
    def construct(self):
        world = shelf(contents=4, soil_count=4, lids=False)
        self.add(world, world.lids[4])
        self.at("the fifth container")
        self.play(FadeOut(world.lids[4], shift=UP * 0.38), run_time=0.66)
        self.at("the other half", lead=0.3)
        self.play(FadeIn(world.samples[4], shift=DOWN * 2.44), run_time=1.08)
        self.at("no soil")
        note = T("No soil", 32, color=GOLD).move_to(xy(SLOTS[4], -2.82))
        self.play(FadeIn(note), run_time=0.38)
        self.at("tape every lid", lead=0.38)
        self.play(FadeOut(note), FadeIn(world.lids, shift=DOWN * 0.30), run_time=0.44)
        for tape in world.tapes:
            self.play(GrowFromEdge(tape, LEFT), run_time=0.52)
        self.at("these lids stay shut")
        closed = caption("The lids stay shut", size=35)
        self.play(FadeIn(closed), run_time=0.52)
        shine = block(1.37, 0.15, SLOTS[0], 1.47, TEXT, radius=0.07, opacity=0.58)
        self.play(FadeIn(shine), run_time=0.21)
        self.play(shine.animate.shift(RIGHT * 10.08), run_time=1.29)
        self.play(FadeOut(shine), run_time=0.22)
        self.at("we are detectives")
        glass = lens(-1.52, 0.18)
        through = question_card("We look through the sides.", y=-2.88, left=-4.85, size=35, color=TEAL)
        self.play(swap(closed, through, 0.76), FadeIn(glass), run_time=0.78)
        self.play(glass.animate.shift(RIGHT * 1.36 + DOWN * 0.31), run_time=1.78)
        self.finish()


class S06PredictChild(SpokenScene):
    def construct(self):
        world = shelf(5, 4, sealed=True)
        paper, sketches, star = journal()
        self.add(world)
        self.at("before the first check")
        self.play(FadeIn(paper, shift=UP * 0.45), run_time=1.36)
        self.at("which one do you")
        q = question_card("Which will change first?", y=2.76, left=-6.1, size=36)
        self.play(FadeIn(q, shift=UP * 0.12), run_time=0.62)
        self.at("write down")
        pen = pencil().shift(xy(-0.82, -2.64))
        self.play(FadeIn(pen, shift=DOWN * 0.34), DrawBorderThenFill(star), run_time=0.82)
        self.play(pen.animate.shift(LEFT * 4.14 + UP * 0.34), run_time=1.13)
        self.at("have your child draw")
        for i, sketch in enumerate(sketches):
            start = xy(SLOTS[i] - 0.55, -2.97)
            self.play(pen.animate.shift(start - pen[-1].get_bottom()), run_time=0.20)
            self.play(DrawBorderThenFill(sketch), pen.animate.shift(RIGHT * 1.10), run_time=0.40)
        self.play(FadeOut(pen, shift=UP * 0.42), run_time=0.35)
        self.finish()


class S07PredictQuestion(SpokenScene):
    def construct(self):
        world = shelf(5, 4, sealed=True)
        start = calendar("Day 1")
        question = question_card(PREDICTION, **PREDICTION_LAYOUT)
        self.add(world)
        self.at("now a question")
        self.play(FadeIn(start, shift=UP * 0.32), run_time=1.6)
        self.at("after 2 weeks")
        self.play(swap(start, calendar("Week 2"), 1.52))
        self.at("which containers")
        self.play(FadeIn(question, shift=UP * 0.12), run_time=0.56)
        self.at("do you predict")
        marks = [T("?", 52, color="#FFF1BB").move_to(xy(x, 0.59)) for x in SLOTS]
        inspection = lens(-5.12, -0.30, scale=0.61)
        walls = [body[0] for body in world.bodies]
        lit = "#547A87"
        self.play(FadeIn(inspection), FadeIn(marks[0]), walls[0].animate.set_fill(lit), run_time=0.45)
        for index in (1, 2):
            self.play(FadeIn(marks[index]), inspection.animate.shift(RIGHT * 2.52),
                      walls[index - 1].animate.set_fill(GLASS), walls[index].animate.set_fill(lit),
                      run_time=0.92)
        self.at("and which one")
        for index in (3, 4):
            self.play(FadeIn(marks[index]), inspection.animate.shift(RIGHT * 2.52),
                      walls[index - 1].animate.set_fill(GLASS), walls[index].animate.set_fill(lit),
                      run_time=0.87)
        self.play(*(FadeOut(mark) for mark in marks), FadeOut(inspection),
                  walls[4].animate.set_fill(GLASS), run_time=self.narration_s + 0.40 - self.elapsed(),
                  rate_func=lambda t: t ** 3)
        self.finish()


class S08PredictPause(PredictPause):
    QUESTION = PREDICTION
    CARD = PREDICTION_LAYOUT

    def backdrop(self):
        return VGroup(shelf(5, 4, sealed=True), calendar("Week 2"))

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        self.wait(self.narration_s)


class S09Reveal(SpokenScene):
    def construct(self):
        world = shelf(5, 4, sealed=True)
        week = calendar("Week 2")
        self.add(world, week)
        self.at("bread often")
        later = shelf(5, 4, sealed=True, changed=True)
        patches = later.samples[2][-2:]
        focus = highlight(SLOTS[2]).set_fill(TEAL, opacity=0.13)
        self.play(FadeIn(focus), run_time=0.48)
        self.play(LaggedStart(*(GrowFromCenter(patch) for patch in patches), lag_ratio=0.36),
                  run_time=1.69)
        fast = place_label(T("Fast", 34, color=GREEN, weight=BOLD), world.numbers[2], dirs=(DOWN,), buff=0.36)
        self.play(FadeIn(fast), run_time=0.42)
        self.at("both apples usually")
        self.play(focus.animate.shift(LEFT * 5.04).set_fill(TEAL, opacity=0), run_time=0.53)
        self.play(Transform(world.samples[0], later.samples[0]), run_time=1.24)
        self.at("even the 1")
        other = highlight(SLOTS[4]).set_fill(TEAL, opacity=0.13)
        self.play(FadeOut(focus), FadeIn(other), run_time=0.49)
        self.play(Transform(world.samples[4], later.samples[4]), run_time=1.52)
        self.at("mold spores")
        spores = VGroup(*[disc(4.53 + (i % 4) * 0.33, 0.04 + (i // 4) * 0.28, 0.05, MOLD)
                          for i in range(11)])
        tag = scope_tag(size=28, color=TEXT)
        self.play(FadeOut(fast), FadeOut(other), FadeIn(spores), FadeIn(tag), run_time=0.40)
        self.play(LaggedStart(*(dot.animate.shift(xy(0.17 * (-1) ** i, -0.36 - 0.07 * (i % 3)))
                                for i, dot in enumerate(spores)), lag_ratio=0.08),
                  run_time=2.13, rate_func=linear)
        self.at("the leaf may")
        slow = place_label(T("Slow", 34, color=GOLD, weight=BOLD), world.numbers[1], dirs=(DOWN,), buff=0.36)
        selected = highlight(SLOTS[1])
        self.play(FadeOut(spores), FadeOut(tag), Create(selected), run_time=0.45)
        self.play(FadeIn(slow), swap(week, calendar("About a month"), 1.05), run_time=1.13)
        self.finish()


class S10Cap(SpokenScene):
    def construct(self):
        world = shelf(5, 4, sealed=True, changed=True)
        date = calendar("About a month")
        self.add(world, date)
        self.at("the bottle cap")
        selected = highlight(SLOTS[3])
        self.play(Create(selected), run_time=0.73)
        unchanged = caption("No change", size=35)
        self.play(FadeIn(unchanged), run_time=0.46)
        glass = lens(1.95, 0.20, scale=0.88)
        self.play(FadeIn(glass), run_time=0.42)
        self.play(glass.animate.shift(RIGHT * 0.55 + DOWN * 0.43), run_time=1.27)
        self.at("most decomposers")
        rule = caption("Most decomposers can’t use plastic as food", size=32)
        self.play(swap(unchanged, rule, 0.75), glass.animate.shift(RIGHT * 0.37), run_time=1.18)
        self.play(FadeOut(glass), FadeOut(selected), FadeOut(date), run_time=1.08)
        self.at("break down dead things")
        view_center = xy(SLOTS[2], 1.93)
        view = Circle(radius=1.10, fill_color="#233943", fill_opacity=1,
                      stroke_color=TEAL, stroke_width=5).move_to(view_center)
        mold_patches = world.samples[2][-2:]
        leaders = VGroup(*[
            Line(patch.get_center(), view.point_at_angle(angle), color=TEAL, stroke_width=3)
            for patch, angle in zip(mold_patches, (4 * PI / 3, 5 * PI / 3))
        ])
        self.play(FadeOut(rule), Create(leaders), FadeIn(view, scale=0.40), run_time=0.78)
        threads = VGroup()
        for x, y, length in [(-0.57, -0.39, 0.75), (-0.23, -0.18, 0.77), (0.08, -0.55, 1.17)]:
            threads.add(line(x, y, x + 0.12, y + length, MOLD, 5),
                        line(x + 0.04, y + length * 0.38, x - 0.19, y + length * 0.67, MOLD, 4),
                        disc(x + 0.12, y + length, 0.095, MOLD))
        threads.shift(view_center)
        self.play(LaggedStart(*(Create(t) for t in threads), lag_ratio=0.17), run_time=1.83)
        self.at("here the main")
        dots = VGroup(*[block(0.24, 0.10, x, y, YELLOW, radius=0.045).rotate(angle)
                        for x, y, angle in [(0.50, 0.29, 0.63), (0.77, -0.03, -0.45),
                                            (0.39, -0.10, 0.22), (0.61, -0.40, 0.58),
                                            (0.32, -0.67, -0.54)]]).shift(view_center)
        decomposers = T("Decomposers", 34, color=GREEN, weight=BOLD).next_to(view, UP, buff=0.17)
        self.play(FadeIn(decomposers), LaggedStart(*(GrowFromCenter(d) for d in dots), lag_ratio=0.25),
                  run_time=1.6)
        self.at("bacteria and mold")
        key = caption("Bacteria and mold", size=35)
        self.play(FadeIn(key), FadeIn(scope_tag(size=28, color=TEXT)),
                  dots.animate.shift(UP * 0.12), run_time=1.10)
        self.finish()


class S11Ask(SpokenScene):
    def construct(self):
        world = shelf(5, 4, sealed=True, changed=True)
        previous, sketches, star = journal()
        self.add(world)
        self.at("each time you look")
        glass = lens(-3.77, 0.34, scale=0.8)
        self.play(FadeIn(glass), run_time=0.51)
        q = question_card("What is different since last time?", left=-6.1, y=2.72, size=36)
        self.at("what is different")
        self.play(FadeIn(q), glass.animate.shift(RIGHT * 3.78), run_time=1.63)
        self.at("compare the apple")
        apple_frames = VGroup(highlight(SLOTS[0]), highlight(SLOTS[4]))
        left = T("With soil", 32, color=TEAL).move_to(xy(SLOTS[0], 2.75))
        right = T("On its own", 32, color=TEAL).move_to(xy(SLOTS[4], 2.75))
        self.play(FadeOut(q), FadeOut(glass), Create(apple_frames[0]), run_time=0.65)
        self.play(FadeIn(left), run_time=0.37)
        self.at("with the apple")
        self.play(Create(apple_frames[1]), run_time=0.63)
        self.play(FadeIn(right), run_time=0.39)
        self.at("at the end")
        day = T("Day 1", 30, color="#F2C69C").move_to(xy(-5.53, -2.54))
        latest = T("Later", 30, color="#F2C69C").move_to(xy(-5.53, -3.27))
        later_cards, later_sketches, _ = journal(changed=True)
        day_one, later = [], []
        for i in range(5):
            x = -3.56 + i * 1.84
            day_one.append(VGroup(previous[i], sketches[i]).scale(0.63).move_to(xy(x, -2.54)))
            later.append(VGroup(later_cards[i], later_sketches[i]).scale(0.63).move_to(xy(x, -3.27)))
        star.scale(0.64).move_to(xy(0.59, -2.39))
        self.play(FadeOut(left), FadeOut(right), FadeOut(apple_frames), FadeIn(day),
                  LaggedStart(*(FadeIn(card, shift=UP * 0.12) for card in day_one), lag_ratio=0.18),
                  FadeIn(star), run_time=0.97)
        self.play(LaggedStart(*(FadeIn(card, shift=UP * 0.12) for card in later), lag_ratio=0.25),
                  FadeIn(latest), run_time=1.26)
        self.at("check the starting guess")
        self.play(Indicate(star, scale_factor=1.24, color=SOIL), run_time=0.55)
        self.at("sort fast", lead=0.32)
        self.play(FadeOut(latest), FadeOut(world.numbers), run_time=0.26)
        fast = T("Fast", 31, color=GREEN, weight=BOLD).move_to(xy(-2.79, 3.07))
        slow = T("Slow", 31, color=GOLD, weight=BOLD).move_to(xy(0.93, 3.07))
        same = T("No change", 31, color=BLUE, weight=BOLD).move_to(xy(4.36, 3.07))
        self.play(FadeIn(fast), later[0].animate.move_to(xy(-4.26, 2.39)),
                  later[2].animate.move_to(xy(-2.81, 2.39)),
                  later[4].animate.move_to(xy(-1.36, 2.39)), run_time=0.74)
        self.at("slow", lead=0.12)
        self.play(FadeIn(slow), later[1].animate.move_to(xy(0.93, 2.39)), run_time=0.57)
        self.at("unchanged")
        self.play(FadeIn(same), later[3].animate.move_to(xy(4.36, 2.39)), run_time=0.72)
        self.finish()


class S12Safety(SpokenScene):
    def construct(self):
        world = shelf(5, 4, sealed=True, changed=True)
        self.add(world)
        self.at("you set up")
        adult = safety_badge(hand().rotate(-0.55), "Adult seals", -4.72)
        self.play(FadeIn(adult[0], shift=DOWN * 0.26), run_time=0.63)
        self.play(FadeIn(adult[1]), run_time=0.46)
        shine = block(1.14, 0.15, SLOTS[0], 1.47, TEXT, radius=0.07, opacity=0.61)
        self.play(FadeIn(shine), run_time=0.24)
        self.play(shine.animate.shift(RIGHT * 10.08), run_time=1.30)
        self.play(FadeOut(shine), run_time=0.27)
        self.at("keep the tubs")
        shade = caption("Keep out of direct sun", size=35)
        self.play(FadeIn(shade), run_time=0.56)
        self.play(world.board[1].animate.set_stroke(color="#C1B099", width=4), run_time=1.98)
        self.at("stay with your child")
        glass = lens(-3.7, 0.12, scale=0.84)
        through = caption("Look through the sides", size=35)
        self.play(swap(shade, through, 0.74), FadeIn(glass), run_time=0.84)
        self.play(glass.animate.shift(RIGHT * 5.37), run_time=2.31)
        self.at("nobody opens")
        locked = safety_badge(lock(), "Never open", -1.56)
        nose = safety_badge(sniff(), "No sniffing", 1.56)
        self.play(FadeOut(glass), FadeOut(through), FadeIn(locked), run_time=0.64)
        self.at("sniffs")
        self.play(FadeIn(nose), run_time=0.50)
        self.at("or shakes")
        shake = caption("Do not shake", size=34, color=RED)
        self.play(FadeIn(shake), run_time=0.50)
        self.at("mold spores")
        allergy = caption("Mold spores can trigger asthma or allergies", size=32)
        self.play(swap(shake, allergy, 0.80), run_time=0.80)
        focus = highlight(SLOTS[2])
        self.play(Create(focus), run_time=1.53)
        self.at("anyone with asthma")
        keep_clear = caption("Asthma or mold allergy: leave tubs alone", size=32)
        self.play(swap(allergy, keep_clear, 0.78), run_time=0.78)
        self.play(focus.animate.set_stroke(opacity=0.65), run_time=1.45)
        self.at("a weakened immune system")
        immune = caption("Weakened immune system: leave tubs alone", size=32)
        self.play(swap(keep_clear, immune, 0.90), run_time=0.90)
        self.play(focus.animate.set_stroke(opacity=1), run_time=0.89)
        self.at("leave the containers alone")
        self.play(FadeOut(focus), run_time=0.69)
        self.at("wash hands")
        washed = safety_badge(soap(), "Wash hands", 4.72)
        self.play(FadeOut(immune), FadeIn(washed[0], shift=UP * 0.18), run_time=0.66)
        self.play(FadeIn(washed[1]), run_time=0.50)
        self.finish()


def face():
    head = Circle(radius=0.94, fill_color=SKIN, fill_opacity=1, stroke_width=0)
    hair = Arc(radius=0.76, start_angle=0.26, angle=2.60, color=SOIL, stroke_width=13).shift(UP * 0.10)
    features = VGroup(disc(-0.30, 0.09, 0.064, SOIL), disc(0.30, 0.09, 0.064, SOIL),
                      Circle(radius=0.16, stroke_color=SOIL, stroke_width=4).shift(DOWN * 0.35))
    return VGroup(head, hair, features)


def trash_can():
    body = shape([(2.73, 0.19), (5.98, 0.19), (5.60, -2.80), (3.11, -2.80)],
                 "#355E65", RIM)
    ribs = VGroup(*[line(x, -0.12, x + (4.36 - x) * 0.16, -2.49, "#68939A", 4)
                    for x in (3.28, 3.82, 4.35, 4.88, 5.42)])
    cover = VGroup(block(3.52, 0.29, 4.35, 0.22, RIM, radius=0.10),
                   block(0.79, 0.25, 4.35, 0.46, RIM, radius=0.09))
    return VGroup(body, ribs), cover


def bag(tied=False):
    body = shape([(-0.74, 1.48), (0.78, 1.48), (0.46, 1.04), (1.34, 0.17),
                  (1.18, -1.15), (0.64, -1.44), (-0.73, -1.44), (-1.27, -0.86),
                  (-1.18, 0.22), (-0.41, 1.05)],
                 "#34525C" if tied else "#384953", RIM)
    creases = VGroup(line(-0.30, 0.88, -0.58, 0.26, RIM, 2),
                     line(0.29, 0.88, 0.70, 0.28, RIM, 2))
    if tied:
        creases.add(block(0.88, 0.20, 0.02, 1.0, TAPE, radius=0.08))
    return VGroup(body, creases)


class S13Safety2(SpokenScene):
    def construct(self):
        world = shelf(5, 4, sealed=True, changed=True)
        self.add(world)
        self.at("bottle cap")
        hazard = no_mark(cap()).scale(1.12).move_to(xy(-3.70, 2.72))
        child = face().scale(0.93).move_to(xy(3.49, 2.65))
        self.play(FadeIn(hazard, shift=UP * 0.23), run_time=0.88)
        self.play(FadeIn(child, shift=LEFT * 0.32), run_time=0.89)
        self.at("choking risk")
        warning = caption("Under 4: choking risk", 35, RED)
        self.play(FadeIn(warning), run_time=0.57)
        self.play(hazard.animate.shift(LEFT * 1.94), run_time=2.03)
        self.at("keep small pieces")
        out = caption("Keep small pieces out of reach", 34)
        self.play(swap(warning, out, 0.75), hazard.animate.shift(LEFT * 0.15), run_time=1.05)
        self.at("call 911")
        emergency = caption("Choking? Call 911", 38, RED)
        self.play(swap(out, emergency, 0.70), FadeOut(hazard), run_time=0.87)
        self.play(Indicate(child[2][-1], color=RED, scale_factor=1.45), run_time=1.15)
        self.at("never taste")
        no_taste = caption("Never taste the samples", 35, RED)
        food = no_mark(apple()).scale(0.91).move_to(xy(-2.31, 2.63))
        self.play(swap(emergency, no_taste, 0.71), FadeOut(child), FadeIn(food), run_time=0.87)
        self.play(food.animate.shift(RIGHT * 2.28), run_time=1.55)
        self.at("at the end")
        self.play(FadeOut(food), FadeOut(no_taste), run_time=0.49)
        self.at("bag the sealed tubs", lead=0.67)
        container, lid = trash_can()
        container.set_z_index(1)
        lid.set_z_index(2)
        sack = bag().move_to(xy(-0.77, -0.38))
        hands = VGroup(hand().rotate(-0.9).shift(xy(-3.2, 0.43)),
                       hand().rotate(0.8).shift(xy(0.98, 0.52)))
        tubs = VGroup(*[VGroup(world.bodies[i].copy(), world.lids[i].copy(), world.tapes[i].copy(),
                              world.samples[i].copy()) for i in range(5)])
        tubs.scale(0.29).move_to(xy(-1.07, 2.15))
        outdoors, _ = grove(thin=True)
        self.remove(world)
        self.add(outdoors, container, lid, sack)
        self.play(FadeIn(hands), FadeIn(tubs, shift=DOWN * 0.25), run_time=0.61)
        self.play(tubs.animate.shift(DOWN * 1.65), run_time=0.60)
        tied = bag(tied=True).move_to(sack)
        knot = tied[1][-1]
        grip = VGroup(
            hand().scale(0.65).rotate(-PI / 2).next_to(knot, LEFT, buff=-0.08),
            hand().scale(0.65).rotate(PI / 2).next_to(knot, RIGHT, buff=-0.08),
        )
        self.play(Transform(sack, tied), Transform(hands, grip),
                  FadeOut(tubs, shift=DOWN * 0.43), run_time=0.37)
        self.at("put them in", lead=0.15)
        done = caption("Sealed tubs go in outdoor trash", size=34).set_z_index(3)
        hinge = lid[0].get_right()
        lid_angle = 1.43
        self.play(Rotate(lid, -lid_angle, about_point=hinge), FadeIn(done), run_time=0.34)
        above_can = xy(4.35, 1.79)
        travel = above_can - sack.get_center()
        self.play(sack.animate.scale(0.78).move_to(above_can),
                  hands.animate.scale(0.78, about_point=sack.get_center()).shift(travel), run_time=0.64)
        self.play(sack.animate.shift(DOWN * 2.85), FadeOut(hands, shift=UP * 0.31), run_time=0.52)
        self.remove(sack)
        self.play(Rotate(lid, lid_angle, about_point=hinge), run_time=0.30)
        self.finish()


def seedling():
    stem = line(0, -0.15, 0.05, 1.99, GREEN, 6)
    left = leaf(GREEN).rotate(-0.49).move_to(xy(-0.52, 1.30))
    right = leaf("#A9CB63").rotate(0.55).move_to(xy(0.62, 1.72))
    return VGroup(stem, left, right).shift(xy(2.45, -1.90))


class S14Return(SpokenScene):
    def construct(self):
        landscape, litter = grove(thin=True)
        self.add(landscape, litter)
        self.at("so where did")
        question = question_card("Where did the\nleaves go?", y=0.32, left=1.45, size=43, max_w=4.9)
        drops = VGroup(falling_leaf(-1.1, 1.61, LEAVES[1]), falling_leaf(-0.70, 2.38, LEAVES[0]))
        self.play(FadeIn(question), FadeIn(drops), run_time=0.59)
        self.play(LaggedStart(*(d.animate.rotate(0.87).move_to(xy(d.get_x() + 0.36, -1.85)) for d in drops),
                              lag_ratio=0.28), run_time=2.54)
        self.at("tiny living things")
        bits = VGroup(*[disc(x, -2.00, 0.077, LEAVES[i % 4])
                        for i, x in enumerate((-4.70, -3.42, -2.14, -0.87, 0.16))])
        self.play(FadeOut(question), FadeOut(litter, shift=DOWN * 0.33), FadeOut(drops, shift=DOWN * 0.33),
                  FadeIn(bits, shift=DOWN * 0.22), run_time=1.47)
        self.at("returned the bits")
        arrows = VGroup(*[Arrow(xy(x + 0.18, -2.10), xy(x + 0.18, -3.03),
                                color=PAPER, buff=0.04, stroke_width=3, max_tip_length_to_length_ratio=0.20)
                          for x in (-4.70, -3.42, -2.14, -0.87, 0.16)])
        self.play(LaggedStart(*(GrowArrow(a) for a in arrows), lag_ratio=0.14),
                  bits.animate.shift(DOWN * 0.76), run_time=1.62)
        self.at("new plants")
        plant = seedling()
        self.play(GrowFromEdge(plant, DOWN), FadeOut(arrows), run_time=1.70)
        self.finish()


class S15End(EndCard):
    LINE = "Tiny living things make some materials rot faster than others."
