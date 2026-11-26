"""Where Differences Begin. Shared builders keep landmarks fixed across cuts."""

from bp_parts import *  # noqa: F401,F403
from bp_style import EndCard

# COLOR MAP: blue inherited information, green environment and leaves,
# gold mutation, purple changed trait, red blocked routes, white neutral paths.
LEAF = "#79B85A"
PURPLE = "#B07CFF"
BARK = "#A47F56"
SLATE = "#344559"
PAPER = "#92A3B8"
DEEP_BLUE = "#193747"
DEEP_GREEN = "#283E30"
DEEP_PURPLE = "#302743"


def point(x, y):
    return np.array([x, y, 0.0])


def heading(text, color=TEXT):
    return T(text, 39, color, weight=BOLD).move_to(point(0, 3.16))


def surface(w, h, x, y, fill=SLATE, stroke=PAPER, opacity=1):
    return RoundedRectangle(
        width=w, height=h, corner_radius=0.19, stroke_color=stroke,
        stroke_width=2, fill_color=fill, fill_opacity=opacity,
    ).move_to(point(x, y))


def route(points, color=TEXT, width=8):
    curve = VMobject(stroke_width=width, color=color)
    if len(points) == 2:
        curve.set_points_as_corners([point(*p) for p in points])
    else:
        curve.set_points_smoothly([point(*p) for p in points])
    return curve


def arrowhead(path, color=TEXT, size=0.21):
    tip = path.get_end()
    tangent = tip - path.point_from_proportion(0.97)
    angle = np.arctan2(tangent[1], tangent[0])
    return Triangle(stroke_width=0, fill_color=color, fill_opacity=1).scale(size).rotate(angle - PI / 2).move_to(tip)


def flow(scene, paths, run_time, *emphasis):
    """Trace the active route in the direction its input travels."""
    scene.play(*[
        ShowPassingFlash(
            path.copy().set_stroke(interpolate_color(path.get_color(), WHITE, .32), width=18)
            .set_cap_style(CapStyleType.ROUND),
            time_width=.43, rate_func=linear,
        )
        for path in paths
    ], *emphasis, run_time=run_time)


def leaf(length, width, lobe=1.0):
    """A common rounded outline with variable lobe depth and blade proportions."""
    stations = [
        (0, 0), (.23, .08), (.31, .18), (.23, .25),
        (.43 * lobe, .32), (.50, .43), (.39, .50), (.34, .53),
        (.48, .61), (.43 * lobe, .71), (.32, .75), (.22, .78),
        (.27, .86), (.17, .96), (0, 1),
    ]
    outline = stations + [(-x, y) for x, y in stations[-2::-1]]
    blade = VMobject(stroke_color="#B7D992", stroke_width=2, fill_color=LEAF, fill_opacity=1)
    blade.set_points_smoothly([point(x * width, y * length) for x, y in outline])
    stem = Line(point(0, -.26), point(0, .05), color=BARK, stroke_width=4)
    rib = Line(point(0, .02), point(0, .88 * length), color=DEEP_GREEN, stroke_width=2)
    veins = VGroup(*[
        Line(point(0, y * length), point(side * w * width, (y + .14) * length),
             color=DEEP_GREEN, stroke_width=1.4)
        for y, w in ((.21, .29), (.40, .35), (.57, .29)) for side in (-1, 1)
    ])
    return VGroup(stem, blade, rib.set_z_index(1), veins.set_z_index(1))


LEAF_SHAPES = [
    (2.6, 1.19, .86, .03), (3.55, 1.18, 1.02, .04),
    (2.92, 1.19, .96, -.06), (4.10, 1.19, .83, .02),
    (3.35, 1.21, 1.06, -.02), (4.46, 1.22, .94, .01),
    (2.73, 1.17, .91, -.04), (3.94, 1.22, 1.03, -.01),
    (3.06, 1.15, .84, .04), (3.70, 1.20, 1.01, -.05),
]


def oak_world():
    branch = CubicBezier(point(-6.16, -1.95), point(-3.25, -2.52),
                         point(3.25, -1.69), point(6.16, -1.96),
                         stroke_color=BARK, stroke_width=15)
    leaves = VGroup(*[
        leaf(length, width, lobe).rotate(angle, about_point=ORIGIN)
        .shift(branch.point_from_proportion(u) + UP * .25)
        for u, (length, width, lobe, angle) in zip(np.linspace(.075, .925, 10), LEAF_SHAPES)
    ])
    ruler = VGroup(
        surface(11.9, .44, 0, -2.94, SLATE, PAPER),
        *[Line(point(x, -2.74), point(x, -2.94 - (i % 2 == 0) * .09),
               stroke_width=2, color=TEXT) for i, x in enumerate(np.linspace(-5.65, 5.65, 33))]
    )
    return branch, leaves, ruler


def leaf_tips(leaves):
    return VGroup(*[Dot(item[1].get_top() + UP * .12, radius=.072, color=PURPLE) for item in leaves])


def oak_crown(x, y, size):
    trunk = Line(point(x, y-size*.79), point(x, y), color=BARK, stroke_width=9)
    canopy = VGroup(*[
        Circle(radius=r*size, stroke_color="#9CC976", stroke_width=2,
               fill_color="#416B40", fill_opacity=1).move_to(point(x+dx*size, y+dy*size))
        for dx, dy, r in ((-.41, -.02, .51), (.41, .03, .49), (0, .33, .62))
    ])
    return VGroup(trunk, canopy)


def person(x, base, height, fill=SLATE, color=PAPER):
    """Filled silhouette, with coordinates measured from the common ground line."""
    body = [
        (-.13, .72), (-.29, .69), (-.35, .44), (-.25, .41), (-.17, .58),
        (-.17, .35), (-.23, .07), (-.25, .02), (-.07, .02), (0, .35),
        (.07, .02), (.25, .02), (.23, .07), (.17, .35), (.17, .58),
        (.25, .41), (.35, .44), (.29, .69), (.13, .72),
    ]
    torso = Polygon(*[point(x + u*height*.82, base + v*height) for u, v in body],
                    color=color, stroke_width=2, fill_color=fill, fill_opacity=1)
    head = Circle(radius=.117*height, color=color, stroke_width=2,
                  fill_color=fill, fill_opacity=1).move_to(point(x, base + .881*height))
    return VGroup(torso, head)


def allele_card(letter, x, y, changed=False):
    box = boxed_label(letter, BLUE, size=37, min_size=28,
                      box=(1.14, 1.35), pad=.17, fill_opacity=1)
    box.box.set_fill(DEEP_BLUE, 1)
    box.label.set_z_index(2)
    box.move_to(point(x, y))
    if changed:
        corner = Polygon(point(x+.20, y+.65), point(x+.49, y+.65), point(x+.54, y+.61),
                         point(x+.54, y+.31), stroke_width=0, fill_color=GOLD, fill_opacity=1)
        box.add(corner)
    return box


def food_icon():
    bottom = ArcBetweenPoints(point(-.42, .04), point(.42, .04), angle=2.25,
                              stroke_width=3, color=GREEN, fill_color=GREEN, fill_opacity=.8)
    rim = Ellipse(width=.84, height=.24, color=GREEN, stroke_width=3,
                  fill_color=DEEP_GREEN, fill_opacity=1).move_to(point(0, .04))
    grain = Dot(point(.04, .08), radius=.083, color=GREEN)
    return VGroup(bottom, rim, grain)


def health_icon():
    outline = RoundedRectangle(width=.66, height=.66, corner_radius=.15, color=GREEN,
                               stroke_width=2, fill_color=DEEP_GREEN, fill_opacity=1)
    cross = VGroup(Line(LEFT*.18, RIGHT*.18), Line(DOWN*.18, UP*.18)).set_stroke(GREEN, 6)
    return VGroup(outline, cross)


def sun_icon(color=GREEN):
    return VGroup(Circle(radius=.202, color=color, fill_color=color, fill_opacity=.86),
                  *[Line(.30*p, .46*p, color=color, stroke_width=3)
                    for p in [rotate_vector(RIGHT, i*TAU/8) for i in range(8)]])


def water_icon():
    drop = VMobject(stroke_color=GREEN, stroke_width=2, fill_color=GREEN, fill_opacity=.8)
    drop.set_points_smoothly([point(0,.42), point(.27,.01), point(.20,-.26),
                              point(0,-.33), point(-.20,-.26), point(-.27,.01), point(0,.42)])
    return drop


class S00Hook(SpokenScene):
    def construct(self):
        branch, leaves, ruler = oak_world()
        self.add(branch, leaves[0], leaves[1])
        self.at("ten leaves")
        self.play(LaggedStart(*[GrowFromPoint(item, item[0].get_start()) for item in leaves[2:]],
                              lag_ratio=.17), run_time=2.65)
        self.at("why do they")
        question = question_card("Why do these leaves differ?", y=3.19, color=TEXT, size=38).shift(RIGHT*.5)
        self.play(FadeIn(question), run_time=.55)
        self.at("rounded lobes")
        blades = [leaves[i][1] for i in (1, 4, 7)]
        self.play(LaggedStart(*[b.animate.set_fill("#ADD981").set_stroke(TEXT, 3)
                               for b in blades], lag_ratio=.32), run_time=1.7)
        self.at("differ in size")
        tips = leaf_tips(leaves)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in tips], lag_ratio=.14),
                  run_time=1.92)
        self.at("their story")
        self.play(LaggedStart(*[b.animate.set_fill(LEAF).set_stroke("#B7D992", 2) for b in blades],
                              lag_ratio=.28), run_time=1.05)
        self.at("with variation")
        self.play(swap(question, heading("Variation", PURPLE), run_time=1.05))
        self.at("look closely")
        self.play(FadeIn(ruler, shift=LEFT*.68), run_time=1.5)
        self.at("beside the ruler", lead=.65)
        self.play(FadeOut(tips), run_time=.85)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Mutations and Variation"
    TITLE = "Where Differences Begin"

    def construct(self):
        branch, leaves, ruler = oak_world()
        lesson = T(self.LESSON, 28, TEXT).move_to(point(0, -2.47))
        title = T(self.TITLE, 54, TEXT, font=TITLE_FONT).move_to(point(0, 3.24))
        card = VGroup(lesson, title)
        self.add(branch, leaves, ruler)
        self.play(FadeIn(card), run_time=.48)
        self.wait(.92)
        self.play(FadeOut(card), run_time=.60)


class S02Words(SpokenScene):
    def construct(self):
        branch, leaves, ruler = oak_world()
        self.add(branch, leaves, ruler)
        self.at("a trait")
        self.play(ShowPassingFlash(leaves[5][1].copy().set_stroke(TEXT, 5), time_width=.65),
                  run_time=1.05)
        trait = heading("Trait", TEXT)
        self.play(FadeIn(trait), run_time=.55)
        self.at("like leaf shape")
        self.play(ShowPassingFlash(leaves[3][1].copy().set_stroke(TEXT, 5), time_width=.7),
                  run_time=1.25)

        self.at("a population", lead=.8)
        trees = VGroup(*[oak_crown(x,y,s) for x,y,s in
                         ((-4.05,.30,1.18),(-2.05,1.19,1.10),(0,.37,1.42),
                          (2.14,1.11,1.03),(4.06,.47,1.30),(-2.25,-.87,.81),(2.31,-.82,.96))])
        boundary = Ellipse(width=12, height=5.15, color=PAPER, stroke_width=2,
                           fill_color=DEEP_GREEN, fill_opacity=.58).shift(DOWN*.14)
        self.play(FadeOut(branch, shift=DOWN*.2), FadeOut(leaves, shift=DOWN*.2),
                  FadeOut(ruler), FadeOut(trait), FadeIn(boundary), run_time=.63)
        self.play(LaggedStart(*[GrowFromPoint(t, t.get_bottom()) for t in trees], lag_ratio=.21),
                  run_time=2.40)
        population = heading("Population", GREEN)
        self.play(FadeIn(population), run_time=.55)
        self.at("one area")
        self.play(ShowPassingFlash(boundary.copy().set_fill(opacity=0).set_stroke(TEXT, 6),
                                   time_width=.46), run_time=1.5)

        self.at("variation means")
        self.play(FadeOut(trees), FadeOut(boundary), FadeOut(population), run_time=.5)
        branch, leaves, _ = oak_world()
        self.play(FadeIn(branch), LaggedStart(*[FadeIn(l, shift=UP*.3) for l in leaves],
                                            lag_ratio=.10), run_time=1.75)
        self.play(FadeIn(heading("Variation = differences", PURPLE)), run_time=.55)
        self.at("shared traits")
        self.play(LaggedStart(*[ShowPassingFlash(leaves[i][1].copy().set_stroke(TEXT, 5),
                                                time_width=.47) for i in (0, 3, 6, 9)],
                              lag_ratio=.29), run_time=1.48)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in leaf_tips(leaves)], lag_ratio=.16),
                  run_time=1.4)
        self.finish()


def input_sources():
    parent_a = person(-5.25, .46, 1.58, DEEP_BLUE, BLUE)
    parent_b = person(-3.95, .46, 1.58, DEEP_BLUE, BLUE)
    blue_label = T("Inherited information", 30, BLUE, weight=BOLD).move_to(point(-4.29, 2.72))
    green_label = T("Environmental conditions", 30, GREEN, weight=BOLD).move_to(point(-4.03, -2.98))
    icons = VGroup(food_icon(), health_icon(), sun_icon(), water_icon())
    for i, icon in enumerate(icons):
        icon.move_to(point(-5.58 + .9*i, -1.82))
    return VGroup(parent_a, parent_b), blue_label, icons, green_label


class S03Inputs(SpokenScene):
    def construct(self):
        parents, blue_label, icons, green_label = input_sources()
        child = person(2.13, -1.96, 4.13)
        oak = leaf(3.9, 1.65, .94).shift(point(4.78, -1.77))
        blue = route([(-3.01, 1.25), (-1.25, 1.20), (.75, .61)], BLUE)
        green = route([(-2.12, -1.8), (-.66, -1.69), (.72, -1.21)], GREEN)
        blue_leaf = route([(-1.76, 1.21), (-.48, 2.48), (2.83, 3.05), (4.57, 2.75)], BLUE, 6)
        green_leaf = route([(-1.59,-1.77), (-.28, -2.46), (3.25,-2.49), (4.39,-1.72)], GREEN, 6)
        tag = scope_tag(size=28, color=TEXT)

        self.at("shape many traits", lead=.78)
        self.add(child, oak)
        self.play(Create(blue), Create(green), run_time=1.58)
        self.play(FadeIn(arrowhead(blue, BLUE)), FadeIn(arrowhead(green, GREEN)), FadeIn(tag), run_time=.5)
        self.at("blue inherited")
        self.play(FadeIn(parents), run_time=.67)
        self.play(FadeIn(blue_label), run_time=.45)
        self.at("comes from parents", lead=.65)
        blocks = VGroup(*[RoundedRectangle(width=.27, height=.33, corner_radius=.05,
                                           stroke_width=1, color=BLUE, fill_color=BLUE, fill_opacity=1)
                           for _ in range(2)]).arrange(RIGHT, buff=.15)
        self.play(MoveAlongPath(blocks, blue, rate_func=linear), run_time=1.43)
        self.play(FadeOut(blocks), run_time=.3)

        self.at("green environmental")
        self.play(FadeIn(green_label), run_time=.62)
        self.at("include food")
        self.play(GrowFromCenter(icons[0]), run_time=.65)
        self.at("health")
        self.play(GrowFromCenter(icons[1]), run_time=.65)
        self.at("sunlight")
        self.play(GrowFromCenter(icons[2]), run_time=.42)
        self.at("and water", lead=0)
        self.play(GrowFromCenter(icons[3]), run_time=.61)
        self.at("often act together")
        self.play(Create(blue_leaf), Create(green_leaf), run_time=1.50)
        self.play(FadeIn(arrowhead(blue_leaf, BLUE, .15)),
                  FadeIn(arrowhead(green_leaf, GREEN, .15)), run_time=.28)
        self.at("for many traits")
        self.play(child.animate.stretch(1.10, 1, about_edge=DOWN),
                  oak.animate.stretch(1.11, 1, about_edge=DOWN), run_time=1.72)
        self.finish()


HEIGHT_GROUND = -2.39
QUESTION = "Must their heights match?"
QUESTION_STYLE = {"y": 3.15, "size": 40}


def height_world():
    """Inputs, silhouettes, and height landmarks for the example and its return."""
    panels = TwoPanel("Child 1", "Child 2", colors=(PAPER, PAPER),
                      top=2.67, bottom=-2.69, width=12.5, gap=.37, size=29)
    panels.left_frame.set_fill("#202C3B", 1)
    panels.right_frame.set_fill("#202C3B", 1)
    people, blue, green, genes, icons, bars, masks = (VGroup() for _ in range(7))
    tips = VGroup()
    for x, h, more_food in ((-3.20, 3.64, True), (3.20, 2.72, False)):
        kids_x = x+.40
        people.add(person(kids_x, HEIGHT_GROUND, 2.75))
        b = route([(x-1.42, .94), (x-.71, .76), (x-.17, .26)], BLUE, 7)
        g = route([(x-1.21,-.80), (x-.81,-.83), (x-.52,-.67)], GREEN, 7)
        blue.add(b)
        green.add(g)
        tips.add(arrowhead(b, BLUE, .15), arrowhead(g, GREEN, .15))
        stack = VGroup(*[
            RoundedRectangle(width=.26, height=.39, corner_radius=.05, stroke_width=1.5,
                             color=BLUE, fill_color=BLUE, fill_opacity=.78) for _ in range(3)
        ]).arrange(RIGHT, buff=.085).move_to(point(x-1.91,.99))
        genes.add(stack)
        food = food_icon().scale(.71)
        health = health_icon().scale(.71)
        food_extra = food_icon().scale(.71)
        if more_food:
            tokens = VGroup(food, food_extra, health).arrange_in_grid(rows=2, cols=2, buff=.09)
        else:
            health[0].set_fill("#1E2D30", 1)
            health[1].set_stroke(GREEN, 3)
            tokens = VGroup(food, health).arrange(DOWN, buff=.11)
        tokens.move_to(point(x-1.92, -.92))
        backing = surface(1.38, 1.45, x-1.92, -.92, "#4D6841", GREEN)
        icons.add(VGroup(backing, tokens))

        bar_x = x + 1.87
        bars.add(surface(.71, h, bar_x, HEIGHT_GROUND+h/2, PURPLE, PURPLE))
        masks.add(boxed_label("?", GOLD, size=45, box=(.86, 2.49), pad=.10,
                              fill_opacity=.82).move_to(point(bar_x, HEIGHT_GROUND+1.245)))
        masks[-1].box.set_fill("#665030", 1)
    bases = VGroup(*[
        Line(point(x-2.50, HEIGHT_GROUND), point(x+2.50, HEIGHT_GROUND),
             color=PAPER, stroke_width=2) for x in (-3.20, 3.20)
    ])
    return panels, people, blue, green, genes, icons, tips, bases, bars, masks


def show_height_bars(scene, bars, run_time=2.35):
    scene.play(*[GrowFromEdge(bar, DOWN) for bar in bars], run_time=run_time)


class S04Height(SpokenScene):
    def construct(self):
        panels, people, blue, green, genes, icons, tips, bases, bars, _ = height_world()
        self.add(panels, people, bases, scope_tag(size=28, color=TEXT))
        self.at("height shows")
        self.play(Create(blue[0]), Create(blue[1]), Create(green[0]), Create(green[1]),
                  run_time=1.41)
        self.play(FadeIn(tips), run_time=.43)
        self.at("many genes")
        self.play(LaggedStart(*[GrowFromCenter(block) for column in zip(*genes) for block in column],
                              lag_ratio=.14), run_time=1.46)
        flow(self, blue, 1.15)
        self.at("food and health")
        self.play(*[FadeIn(row[0]) for row in icons], run_time=.65)
        self.play(LaggedStart(*[GrowFromCenter(token) for row in icons for token in row[1]],
                              lag_ratio=.18), run_time=1.12)
        flow(self, green, 1.20)
        self.at("similar inherited information")
        flow(self, blue, 1.18)
        for bar in bars:
            bar.set_fill("#774CA8", 1)
        show_height_bars(self, bars, 2.96)
        self.at("a height bar")
        caps = VGroup(*[
            Line(bar.get_top()+LEFT*.63, bar.get_top()+RIGHT*.63, color=PURPLE, stroke_width=9)
            for bar in bars
        ])
        self.play(LaggedStart(*[GrowFromCenter(line) for line in caps], lag_ratio=.42),
                  FadeIn(caption("Illustrative heights", 31, PURPLE)),
                  *[bar.animate.set_fill(PURPLE, 1) for bar in bars], run_time=1.22)
        self.finish()


def shuffle_hands():
    return VGroup(*[
        surface(w, h, x, y, DEEP_BLUE, "#34596D").set_stroke(width=0).set_z_index(-2)
        for w, h, x, y in ((4.84, 1.92, -3.03, 1.72), (4.84, 1.92, 3.03, 1.72),
                           (3.45, 2.05, -3.97, -1.81), (3.45, 2.05, 0, -1.81),
                           (3.45, 2.05, 3.97, -1.81))
    ])


class S05Shuffle(SpokenScene):
    def construct(self):
        hands = shuffle_hands()
        parents = heading("Parents", TEXT)
        tray = surface(10.55, 1.48, 0, -.06, SLATE, PAPER).set_stroke(width=0).set_z_index(-2)
        letters = ("A", "B", "C", "a", "b", "c")
        original = (-4.43, -3.03, -1.63, 1.63, 3.03, 4.43)
        mixed = (-4.58, -.62, 4.58, -3.36, .62, 3.36)
        cards = VGroup(*[allele_card(letter,x,1.72) for letter,x in zip(letters, original)])
        self.add(hands[0], hands[1], cards, parents)
        self.at("reproduction reshuffles")
        self.play(FadeIn(tray), run_time=.46)
        self.play(*[card.animate.shift(DOWN*1.42) for card in cards[:3]], run_time=.58)
        self.play(*[cards[i].animate.move_to(point(mixed[i], -.06)) for i in range(3)],
                  run_time=.85)
        self.play(*[cards[i].animate.move_to(point(mixed[i], 1.72)) for i in range(3, 6)],
                  run_time=.62)
        self.play(*[card.animate.shift(DOWN*1.78) for card in cards[3:]], run_time=.62)
        self.at("picture blue cards")
        self.play(FadeIn(hands[2:]), FadeOut(tray), FadeOut(hands[:2]), FadeOut(parents), run_time=.43)
        self.play(LaggedStart(*[card.animate.shift(DOWN*1.75) for card in cards],
                              lag_ratio=.21), run_time=2.37)
        self.at("the combinations")
        rule = caption("New mix of existing alleles", 32, BLUE, y=-3.38).shift(RIGHT*.9)
        bracket = VGroup(Line(point(-5.53,-2.98), point(5.53,-2.98), color=BLUE, stroke_width=3),
                         Line(point(-5.53,-2.98), point(-5.53,-2.90), color=BLUE, stroke_width=3),
                         Line(point(5.53,-2.98), point(5.53,-2.90), color=BLUE, stroke_width=3))
        self.play(Create(bracket), run_time=.75)
        self.play(FadeIn(rule), run_time=.53)
        self.at("cards already existed")
        self.play(LaggedStart(*[c.box.animate.set_fill("#26526B") for c in cards],
                              lag_ratio=.14), run_time=1.80)
        self.at("siblings can receive")
        self.play(FadeIn(T("Siblings", 39, TEXT, weight=BOLD).move_to(point(0,-.17))), run_time=.85)
        self.play(LaggedStart(*[hand.animate.set_fill("#294658") for hand in hands[2:]],
                              lag_ratio=.35), run_time=1.6)
        self.finish()


def dna_block(base, x, y, changed=False):
    color = GOLD if changed else BLUE
    block = boxed_label(base, color, size=39, box=(1.05, 1.18), pad=.13, fill_opacity=1)
    block.box.set_fill("#483919" if changed else DEEP_BLUE, 1)
    return block.move_to(point(x, y))


def dna_world(changed=False):
    card = surface(10.16, 3.40, 0, 0, DEEP_BLUE, BLUE)
    row = VGroup(*[
        dna_block("T" if changed and i == 3 else base, (i-2.5)*1.29, -.37, changed and i == 3)
        for i, base in enumerate("ACGGTA")
    ])
    label = T("DNA sequence", 33, BLUE, weight=BOLD).move_to(point(0, .93))
    return card, row, label


def protein_badge(x, word, widths):
    background = surface(3.22, 1.82, x, -2.22, DEEP_PURPLE, PURPLE)
    blocks = VGroup(*[
        RoundedRectangle(width=w, height=.41, corner_radius=.12, stroke_width=0,
                         fill_color=PURPLE, fill_opacity=1) for w in widths
    ]).arrange(RIGHT, buff=.13).move_to(point(x, -1.93))
    text = T(word, 30, TEXT).move_to(point(x,-2.59))
    return VGroup(background, blocks, text)


class S06Mutation(SpokenScene):
    def construct(self):
        card, row, label = dna_world()
        self.at("mutation adds")
        self.add(card)
        self.play(LaggedStart(*[FadeIn(block, shift=UP*.16) for block in row], lag_ratio=.22),
                  run_time=2.55)
        self.at("a mutation changes")
        self.play(FadeIn(label), run_time=.58)
        replacement = dna_world(changed=True)[1][3]
        grown = row[3]
        self.play(Succession(
            grown.animate.stretch(.035, dim=0).set_opacity(0),
            FadeIn(replacement),
        ), run_time=1.42)
        self.remove(grown)
        self.at("the order of")
        self.play(Indicate(replacement.box, scale_factor=1.08, color=GOLD), run_time=1.18)

        self.at("that change can")
        original = allele_card("A", -3.55, -.03)
        other = allele_card("B", -1.85, -.03)
        new = allele_card("A", 2.30, -.03, changed=True)
        new_label = T("New allele", 35, GOLD, weight=BOLD).move_to(point(2.3, 1.38))
        self.play(FadeOut(card), FadeOut(label), FadeOut(VGroup(*[row[i] for i in (0,1,2,4,5)])),
                  FadeOut(replacement), run_time=.45)
        self.add(original, other)
        self.play(FadeIn(new, shift=RIGHT*.83), run_time=.72)
        self.play(FadeIn(new_label), run_time=.55)
        self.at("it may change")
        protein = protein_badge(-3.53, "Protein", (.36, .58))
        amount = protein_badge(0, "Amount", (.32, .32, .32))
        same = protein_badge(3.53, "Neither", (.39, .39))
        self.play(FadeIn(protein), run_time=.66)
        self.at("its amount")
        self.play(FadeIn(amount), run_time=.47)
        self.at("or neither")
        self.play(FadeIn(same), run_time=.48)
        self.finish()


def copy_stamp(x, y):
    sheet = surface(1.23, .90, x-.11, y-.04, SLATE, PAPER)
    stamp = surface(.98, .65, x+.11, y+.15, DEEP_BLUE, BLUE)
    ribs = VGroup(*[Line(point(x-.16, y+.20-.13*i), point(x+.38,y+.20-.13*i),
                         color=BLUE, stroke_width=2) for i in range(2)])
    return sheet, VGroup(stamp, ribs)


def bottle(x, y):
    glass = Polygon(
        *[point(x+u,y+v) for u,v in ((-.38,-.37),(.38,-.37),(.38,.11),
                                     (.17,.28),(.17,.43),(-.17,.43),(-.17,.28),(-.38,.11))],
        stroke_color=PAPER, stroke_width=3, fill_color=SLATE, fill_opacity=1,
    )
    fill = Line(point(x-.29,y-.18), point(x+.29,y-.18), color=TEXT, stroke_width=6)
    return VGroup(glass, fill)


class S07Causes(SpokenScene):
    def construct(self):
        cell = Ellipse(width=6.76, height=3.48, color=BLUE, stroke_width=2,
                       fill_color=DEEP_BLUE, fill_opacity=1).move_to(point(1.47, -.17))
        cell_label = T("Cell", 29, BLUE, weight=BOLD).move_to(point(1.47, .96))
        base = dna_block("G", 1.47, -.21)
        changed = dna_block("T", 1.47, -.21, True)
        sheet, stamp = copy_stamp(-4.47, 2.35)
        sun = sun_icon(TEXT).scale(1.20).move_to(point(.4,2.59))
        flask = bottle(4.48, 2.55)
        causes = VGroup(
            T("Copying mistakes", 30, TEXT).move_to(point(-4.47, 1.58)),
            T("Radiation", 30, TEXT).move_to(point(-1.1, 2.64)),
            T("Some chemicals", 30, TEXT).move_to(point(4.48, 1.79)),
        )
        self.add(cell, cell_label, base, sheet, stamp)
        self.at("copying mistakes")
        self.play(stamp.animate.shift(RIGHT*.26 + DOWN*.17).rotate(-.22),
                  FadeIn(causes[0]), run_time=.91)
        self.at("radiation")
        rays = VGroup(*[Line(point(.63+.21*i,1.94), point(.75+.21*i,1.55),
                             color=TEXT, stroke_width=3.5) for i in range(3)])
        self.play(FadeIn(sun), FadeIn(causes[1]), run_time=.39)
        self.play(Create(rays), run_time=.44)
        self.at("some chemicals")
        self.play(FadeIn(flask, shift=DOWN*.18), FadeIn(causes[2]), run_time=.51)
        self.at("can cause mutations")
        self.play(swap(base, changed, run_time=1.09))
        self.at("the change does")
        self.play(FadeOut(sheet), FadeOut(stamp), FadeOut(sun), FadeOut(flask),
                  FadeOut(causes), FadeOut(rays), run_time=.77)
        self.at("living thing needs")
        need = boxed_label("NEED", TEXT, size=41, box=(3.08, 1.54), pad=.25, fill_opacity=1)
        need.box.set_fill("#544252", 1)
        need.move_to(point(-4.94, -.21))
        self.play(FadeIn(need), run_time=.69)
        blocked = DashedLine(need.get_right()+RIGHT*.18, point(-2.38,-.21),
                             color=RED, stroke_width=13, dash_length=.15)
        wall = Line(point(-2.20,-1.04), point(-2.20,.63), color=RED, stroke_width=15)
        self.at("need sends no")
        self.play(Create(blocked), run_time=.62)
        self.play(GrowFromCenter(wall), cell.animate.set_stroke(BLUE, 7), run_time=.67)
        self.at("more exposure", lead=.4)
        self.play(FadeOut(need), FadeOut(blocked), FadeOut(wall), run_time=.45)
        arrows = VGroup(*[Arrow(point(x,2.62), point(x,1.56), color=TEXT, buff=0,
                                stroke_width=9, tip_length=.23) for x in (.56,1.47,2.38)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.46), run_time=1.54)
        self.play(FadeIn(caption("More exposure can raise chance", 30, GOLD)),
                  cell.animate.set_fill("#374550"), run_time=.81)
        self.finish()


def predict_question():
    return question_card(QUESTION, **QUESTION_STYLE)


class S08Predict(SpokenScene):
    def construct(self):
        panels, people, blue, green, genes, icons, tips, bases, _, masks = height_world()
        self.add(panels, people, bases, masks, scope_tag(size=28, color=TEXT))
        self.at("now predict")
        self.play(FadeIn(genes, shift=RIGHT*.18), run_time=.9)
        self.at("two children inherit")
        self.play(Create(blue[0]), Create(blue[1]), FadeIn(tips[0]), FadeIn(tips[2]), run_time=1.36)
        flow(self, blue, 1.20)
        self.at("food and health")
        self.play(FadeIn(icons), run_time=.74)
        self.play(Create(green[0]), Create(green[1]), FadeIn(tips[1]), FadeIn(tips[3]), run_time=1.33)
        self.at("must they reach")
        self.play(FadeIn(predict_question()), run_time=.70)
        self.at("hold your answer")
        self.play(*[Indicate(mask.box, color=GOLD, scale_factor=1.035) for mask in masks], run_time=1.06)
        self.at("watch both colored")
        food_highlights = [row[0].animate.set_fill("#759A5D") for row in icons]
        flow(self, (blue[0], blue[1], green[0], green[1]), 3.30,
             genes.animate.set_fill(interpolate_color(ManimColor(BLUE), WHITE, .40), opacity=1),
             *food_highlights)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        config.background_color = BG
        self.camera.background_color = BG
        panels, people, blue, green, genes, icons, tips, bases, _, masks = height_world()
        self.add(panels, people, bases, genes, icons, blue, green, tips, masks,
                 scope_tag(size=28, color=TEXT), predict_question())
        self.wait(4.5)


class S10Reveal(SpokenScene):
    def construct(self):
        panels, people, blue, green, genes, icons, tips, bases, bars, masks = height_world()
        q = predict_question()
        self.add(panels, people, bases, genes, icons, blue, green, tips, masks,
                 scope_tag(size=28, color=TEXT), q)
        self.at("now")
        self.play(FadeOut(masks, shift=UP*.60), FadeOut(q), run_time=.44)
        self.at("genes and environment")
        flow(self, (blue[0], blue[1], green[0], green[1]), 2.06,
             people.animate.set_fill("#5A6E88"))
        self.at("different conditions")
        show_height_bars(self, bars, 2.33)
        self.at("this does not prove")
        example = surface(12.84, 5.77, 0, -.01, BG, PURPLE, opacity=0).set_stroke(width=11)
        self.play(Create(example), run_time=1.63)
        self.at("shows a possibility")
        qualifier = heading("Possible outcome, not a diagnosis", PURPLE).shift(UP*.10)
        self.play(FadeIn(qualifier), run_time=.78)
        self.at("that child's history")
        self.play(*[Indicate(bar, color=PURPLE, scale_factor=1.03) for bar in bars], run_time=1.05)
        self.finish()


def cell_location(x, y):
    return Circle(radius=.72, color=PAPER, stroke_width=3, fill_color="#697E94", fill_opacity=1).move_to(point(x,y))


class S11Routes(SpokenScene):
    def construct(self):
        parent = person(-3.54, -2.78, 5.23)
        offspring = person(4.47, -2.78, 3.36)
        parent_tag = T("Parent", 33, TEXT, weight=BOLD).move_to(point(-3.54,3.13))
        kid_tag = T("Offspring", 32, TEXT, weight=BOLD).move_to(point(4.47,1.14))
        skin = cell_location(-2.41,.31).scale(.77)
        sex = cell_location(-3.54,-.56).scale(.87)
        skin_tag = boxed_label("Skin cell", TEXT, size=30, box=(2.40,.86), pad=.16)
        skin_tag.box.set_fill("#52647A", 1)
        skin_tag.move_to(point(.40,.88))
        sex_tag = boxed_label("Egg or sperm", TEXT, size=30, box=(2.83,.71), pad=.14)
        sex_tag.box.set_fill("#52647A", 1)
        sex_tag.move_to(point(-3.62,-3.27))
        skin_lead = Line(point(-1.84,.35),point(-.92,.79),color=PAPER,stroke_width=2)
        sex_lead = route([(-3.59,-1.18),(-4.80,-2.00),(-4.54,-2.78)], PAPER, 2)
        self.add(parent, parent_tag)
        self.at("eggs and sperm")
        self.play(FadeIn(sex), Create(sex_lead), FadeIn(sex_tag), run_time=1.07)
        self.at("location also matters")
        self.play(FadeIn(skin), Create(skin_lead), FadeIn(skin_tag), run_time=1.09)
        self.at("a mutation in a body")
        skin_path = route([(-2.44,.30),(-2.66,.28),(-2.92,.48),(-3.18,.41)], RED, 6)
        skin_dot = Dot(skin_path.get_start(), radius=.22, color=GOLD)
        border = Line(point(-3.55,.19),point(-3.55,.63),color=RED,stroke_width=6)
        self.play(GrowFromCenter(skin_dot), skin.animate.set_fill("#626454"), run_time=.50)
        self.play(Create(skin_path), GrowFromCenter(border), run_time=.63)
        self.at("stays in that body")
        self.play(MoveAlongPath(skin_dot, skin_path), FadeToColor(parent[0], "#4A5262"), run_time=1.46)
        self.at("a mutation in an egg")
        germ_path = route([(-3.54,-.56), (-2.3,-.98), (.32,-.94), (3.60,-.48)], TEXT, 6)
        dot_path = germ_path.copy().add_line_to(point(4.35,-.48))
        germ_dot = Dot(germ_path.get_start(), radius=.22, color=GOLD).set_z_index(2)
        self.play(GrowFromCenter(germ_dot), sex.animate.set_fill("#626454"), run_time=.50)
        self.play(Create(germ_path), FadeIn(offspring), FadeIn(kid_tag), run_time=.87)
        self.at("can reach offspring", lead=.17)
        self.play(FadeIn(arrowhead(germ_path)), MoveAlongPath(germ_dot, dot_path),
                  run_time=1.93)
        self.at("the path")
        can = T("Can reach", 33, TEXT, weight=BOLD).move_to(point(.57,-1.49))
        self.play(FadeIn(can), run_time=.62)
        self.at("decides whether")
        flow(self, (germ_path,), 1.71)
        self.finish()


def oak_inputs():
    blue = route([(-5.77,-2.38),(-3.62,-2.38),(-1.28,-2.17)], BLUE, 7)
    green = route([(5.77,-2.76),(3.66,-2.76),(1.32,-2.15)], GREEN, 7)
    return blue, green


def recap_card(x, changed=False):
    card = boxed_label("A", BLUE, size=28, box=(1.14, .64), pad=.12, fill_opacity=1)
    card.box.set_fill(DEEP_BLUE, 1)
    card.move_to(point(x, -2.91))
    if changed:
        card.add(Polygon(point(x+.20,-2.64), point(x+.49,-2.64), point(x+.49,-2.81),
                         fill_color=GOLD, fill_opacity=1, stroke_width=0))
    return card


class S12Idea(SpokenScene):
    def construct(self):
        branch, leaves, _ = oak_world()
        blue, green = oak_inputs()
        self.add(branch, *leaves[::2])
        self.at("follow the full")
        self.play(LaggedStart(*[GrowFromPoint(l,l[0].get_start()) for l in leaves[1::2]], lag_ratio=.085),
                  run_time=2.45)
        self.at("shared traits")
        tips = leaf_tips(leaves)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in tips], lag_ratio=.13), run_time=1.54)
        self.at("inherited information")
        blue_label = T("Inherited information", 28, BLUE).move_to(point(-3.70,3.22))
        green_label = T("Environment", 28, GREEN).move_to(point(3.65,3.22))
        tok = recap_card(-4.65)
        self.play(Create(blue), FadeIn(blue_label), run_time=.76)
        self.at("and environment", lead=0)
        self.play(Create(green), FadeIn(green_label), run_time=1.02)
        self.play(FadeIn(arrowhead(blue, BLUE)), FadeIn(arrowhead(green, GREEN)), run_time=.30)
        leaf_highlight = interpolate_color(ManimColor(LEAF), WHITE, .20)
        flow(self, (blue, green), 1.38,
             *[item[1].animate(rate_func=there_and_back).set_fill(leaf_highlight) for item in leaves])
        self.at("chance mutation")
        self.play(FadeIn(tok, shift=RIGHT*.34), run_time=.67)
        amber = Polygon(point(-4.45,-2.64), point(-4.16,-2.64), point(-4.16,-2.81),
                        fill_color=GOLD, fill_opacity=1, stroke_width=0)
        self.play(GrowFromCenter(amber), run_time=.67)
        self.play(VGroup(tok, amber).animate.shift(RIGHT*2.07), run_time=1.45)
        summary = heading("Sources of variation", TEXT)
        self.play(FadeOut(blue_label), FadeOut(green_label), run_time=.36)
        self.play(FadeIn(summary), run_time=.53)
        self.at("every visible difference")
        self.play(blue.animate.set_stroke(opacity=.36),
                  VGroup(tok, amber).animate.set_opacity(.66), run_time=.72)
        flow(self, (green,), 1.48)
        self.finish()


class S13Handoff(SpokenScene):
    def construct(self):
        _, leaves, _ = oak_world()
        oak = leaves[5]
        allele = recap_card(-2.58, changed=True)
        # Two schematic light settings pass behind the same fixed leaf.
        dark = surface(11.6, 6.25, 0, -.33, "#202B40", "#53647D").set_stroke(width=0).set_z_index(-3)
        light = surface(11.6, 6.25, 0, -.33, "#385148", "#6F9277").set_stroke(width=0).set_z_index(-2)
        sun = sun_icon(TEXT).scale(1.25).move_to(point(-4.68,1.56))
        self.add(dark, oak)
        self.at("a new difference")
        self.play(FadeIn(allele, shift=RIGHT*.33), run_time=.89)
        self.play(ShowPassingFlash(oak[1].copy().set_stroke(TEXT, 5), time_width=.57), run_time=1.22)
        self.at("ask whether its")
        self.play(FadeIn(light), FadeIn(sun), run_time=.70)
        self.bring_to_front(oak, allele)
        self.at("the surroundings")
        wipe = light.copy()
        wipe.stretch(.01, 0, about_edge=RIGHT)
        self.bring_to_front(light, sun, oak, allele)
        self.play(ReplacementTransform(light, wipe), FadeOut(sun), run_time=1.58)
        self.remove(wipe)
        self.at("that is the")
        prompt = T("Effect?", 42, PURPLE, weight=BOLD).move_to(point(3.57,.11))
        self.play(FadeIn(prompt, shift=UP*.14), run_time=.87)
        self.finish()


class S14End(EndCard):
    LINE = "Genes and environments shape variation;\nchance mutations add new genetic differences."
