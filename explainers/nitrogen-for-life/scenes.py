"""Nitrogen for Life — one carried schematic world, built from pipeline parts."""
from bp_parts import *


SOIL = "#8A684B"
SOIL_DARK = "#493927"
WATER = "#58A6C7"
LEAF = "#83C167"
ORANGE = "#F29E4C"
N2 = GREY
USABLE = GREEN


def gas_pair(at=ORIGIN, scale=1.0, open_clasp=False):
    """The film's nitrogen-gas glyph: a grey pair held by one gold clasp."""
    a = Dot(LEFT * 0.18, radius=0.13, color=N2)
    b = Dot(RIGHT * 0.18, radius=0.13, color=N2)
    bar = Line(a.get_center(), b.get_center(), color=N2, stroke_width=5)
    if open_clasp:
        clasp = Arc(radius=0.11, start_angle=0.2, angle=PI * 0.8, color=GOLD,
                    stroke_width=5).move_to(UP * 0.12)
    else:
        clasp = RoundedRectangle(width=0.15, height=0.18, corner_radius=0.04,
                                 stroke_color=GOLD, stroke_width=4).move_to(ORIGIN)
    return VGroup(bar, a, b, clasp).scale(scale).move_to(at)


def gas_field(points, scale=0.75):
    return VGroup(*[gas_pair(p, scale) for p in points])


def leaf_shape(at, width=0.9, angle=0.0, opacity=0.48):
    return Ellipse(width=width, height=width * 0.34, stroke_color=LEAF,
                   stroke_width=3, fill_color=LEAF, fill_opacity=opacity).rotate(angle).move_to(at)


def corn_plant(x, ground_y=-0.7, height=2.7, roots_on=True):
    stem = Line([x, ground_y, 0], [x, ground_y + height, 0], color=LEAF, stroke_width=8)
    leaves = VGroup()
    for i, f in enumerate((0.30, 0.48, 0.66, 0.83)):
        side = -1 if i % 2 else 1
        leaves.add(leaf_shape([x + side * 0.48, ground_y + height * f, 0],
                              1.15, side * 0.43))
    tassel = VGroup(*[Line([x, ground_y + height, 0],
                           [x + dx, ground_y + height + 0.32, 0], color=GOLD, stroke_width=3)
                      for dx in (-0.24, 0, 0.24)])
    roots = VGroup()
    if roots_on:
        for dx in (-0.8, -0.42, 0, 0.42, 0.8):
            roots.add(CubicBezier([x, ground_y, 0], [x + dx * .25, ground_y - .35, 0],
                                  [x + dx * .7, ground_y - .75, 0],
                                  [x + dx, ground_y - 1.2, 0]).set_stroke(SOIL, 4))
    return VGroup(stem, leaves, tassel, roots)


def soy_plant(x, ground_y=-0.7, height=2.25, nodules=True):
    stem = Line([x, ground_y, 0], [x, ground_y + height, 0], color=LEAF, stroke_width=8)
    branches = VGroup()
    leaves = VGroup()
    for i, f in enumerate((0.40, 0.63, 0.84)):
        y = ground_y + height * f
        for side in (-1, 1):
            branches.add(Line([x, y, 0], [x + side * .55, y + .22, 0], color=LEAF, stroke_width=5))
            leaves.add(leaf_shape([x + side * .72, y + .28, 0], .8, side * .28))
    leaves.add(leaf_shape([x, ground_y + height + .18, 0], .8, PI / 2))
    roots = VGroup()
    ends = []
    for dx in (-.9, -.55, 0, .55, .9):
        end = np.array([x + dx, ground_y - 1.35 + .18 * abs(dx), 0])
        ends.append(end)
        roots.add(CubicBezier([x, ground_y, 0], [x + dx * .18, ground_y - .38, 0],
                              [x + dx * .72, ground_y - .85, 0], end).set_stroke(SOIL, 4))
    bumps = VGroup()
    if nodules:
        for p in (ends[0], ends[1], ends[3], ends[4]):
            bumps.add(Circle(radius=.13, stroke_color=ORANGE, stroke_width=3,
                             fill_color=ORANGE, fill_opacity=.55).move_to(p + UP * .13))
    return VGroup(stem, branches, leaves, roots, bumps)


def deer(at=(0, 0, 0), scale=.6):
    body = Ellipse(width=1.2, height=.55, color="#C39A6B", fill_opacity=.35)
    head = Circle(radius=.24, color="#C39A6B", fill_opacity=.35).move_to([.72, .28, 0])
    legs = VGroup(*[Line([x, -.22, 0], [x, -.72, 0], color="#C39A6B", stroke_width=4)
                    for x in (-.4, .35)])
    return VGroup(body, head, legs).scale(scale).move_to(at)


def farm_world(pairs=True, water=True, plants=True):
    """Reusable Virginia farm cutaway; every wide scene calls this exact builder."""
    sky = Rectangle(width=12.8, height=3.25, stroke_width=0, fill_color=N2,
                    fill_opacity=.09).move_to([0, 1.85, 0])
    soil = Rectangle(width=12.8, height=3.35, stroke_width=0, fill_color=SOIL_DARK,
                     fill_opacity=.72).move_to([0, -1.45, 0])
    horizon = Line([-6.4, .2, 0], [6.4, .2, 0], color=SOIL, stroke_width=4)
    stream = VMobject(stroke_color=WATER, stroke_width=16, stroke_opacity=.65)
    stream.set_points_smoothly([[4.6, .15, 0], [5.05, -.35, 0], [5.35, -1.2, 0], [6.15, -2.6, 0]])
    woods = VGroup(*[Triangle(color=LEAF, fill_color=LEAF, fill_opacity=.22,
                              stroke_width=2).scale(.48 + .07 * (i % 2)).move_to([3.1 + i * .48, .72, 0])
                     for i in range(5)])
    animal = deer([4.0, .45, 0], .48)
    crops = VGroup(soy_plant(-3.2, .2, 1.65), corn_plant(1.0, .2, 2.0)) if plants else VGroup()
    p = gas_field([[-5.2, 2.85, 0], [-3.7, 2.25, 0], [-1.9, 3.0, 0],
                   [.0, 2.35, 0], [1.8, 3.0, 0], [3.6, 2.25, 0], [5.3, 3.0, 0]], .7) if pairs else VGroup()
    pool = RoundedRectangle(width=4.3, height=.72, corner_radius=.28, stroke_color=WATER,
                            stroke_width=3, fill_color=WATER, fill_opacity=.18).move_to([.2, -2.65, 0]) if water else VGroup()
    return VGroup(sky, soil, horizon, stream, woods, animal, crops, p, pool)


def root_closeup(kind="soy", nodules=True):
    """Carried root picture for the reveal, exchange, and corn comparison."""
    soil = Rectangle(width=12.8, height=4.8, stroke_width=0, fill_color=SOIL_DARK,
                     fill_opacity=.72).move_to([0, -1.0, 0])
    plant = soy_plant(0, .75, 2.3, nodules) if kind == "soy" else corn_plant(0, .75, 2.7, True)
    return VGroup(soil, plant)


def bacteria_group(center=ORIGIN, radius=1.6, count=12):
    rods = VGroup()
    for i in range(count):
        a = TAU * i / count
        r = radius * (.28 + .52 * ((i * 7) % count) / count)
        rod = RoundedRectangle(width=.42, height=.18, corner_radius=.09,
                               stroke_color=ORANGE, stroke_width=2,
                               fill_color=ORANGE, fill_opacity=.45)
        rod.rotate(a * .7).move_to(np.array(center) + [r * np.cos(a), .72 * r * np.sin(a), 0])
        rods.add(rod)
    return rods


def predict_backdrop():
    world = farm_world(pairs=True, water=True, plants=True)
    world[-1].shift(UP * 1.7)
    # Only three usable particles remain in the depleted pool.
    dots = VGroup(Dot([.1, -.95, 0], radius=.11, color=USABLE))
    same = T("same air", 28, N2, weight=BOLD).move_to([0, 3.35, 0])
    schematic = T("schematic", 24, GREY).move_to([5.65, 3.35, 0])
    return VGroup(world, dots, same, schematic)


class S00Title(TitleCard):
    LESSON = "Nitrogen for Life"
    TITLE = "Nitrogen Everywhere, and Not a Bit to Use"


class S01Hook(SpokenScene):
    def construct(self):
        world = farm_world(pairs=True, water=False, plants=True)
        self.add(world)
        world[7].shift(DOWN * .35)
        bob(world[7], amp=.14, speed=3.0)
        self.at("air around you")
        air = T("air: about 78% nitrogen", 32, N2, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(air), run_time=.5)
        self.at("cornfield need")
        bag_label = T("nitrogen", 36, USABLE, weight=BOLD)
        bag_label.layout_ok = True  # printed on its own fertilizer bag
        bag = VGroup(Polygon([-1, -.7, 0], [1, -.7, 0], [.75, .7, 0], [-.75, .7, 0],
                             stroke_color=TEXT, fill_color=TEXT, fill_opacity=.12),
                     bag_label).scale(.72).move_to([1.9, 1.0, 0])
        grains = VGroup(*[Dot([1.35 + .18 * i, .25 - .12 * (i % 2), 0], radius=.08, color=USABLE) for i in range(7)])
        self.play(FadeIn(bag, shift=UP * .2), LaggedStart(*[FadeIn(d) for d in grains], lag_ratio=.08), run_time=.75)
        self.at("soybeans next door")
        halo = SurroundingRectangle(world[6][0], color=GOLD, buff=.18, corner_radius=.12)
        self.play(Create(halo), run_time=.5)
        self.at("often do not")
        q = question_card("Why does corn need nitrogen added, and soybeans often not?", size=30)
        self.play(FadeOut(bag), FadeOut(grains), FadeIn(q.question), run_time=.65)
        self.finish()


class S02Need(SpokenScene):
    def construct(self):
        leaf = leaf_shape([0, 0, 0], 7.6, .10, .25)
        veins = VGroup(Line([-3.1, -.3, 0], [3.1, .3, 0], color=LEAF, stroke_width=5),
                       *[Line([x, .1*x, 0], [x + .55, .7 + .1*x, 0], color=LEAF, stroke_width=2)
                         for x in (-2.2, -1.2, -.2, .8, 1.8)])
        self.play(GrowFromCenter(leaf), Create(veins), run_time=.8)
        self.at("plant need nitrogen")
        cell = Circle(radius=2.2, stroke_color=WATER, stroke_width=5, fill_color=WATER,
                      fill_opacity=.09)
        self.play(ReplacementTransform(VGroup(leaf, veins), cell), run_time=.75)
        membrane = DashedVMobject(Circle(radius=2.35, color=WATER, stroke_width=5), num_dashes=28)
        membrane.add_updater(lambda m, dt: m.rotate(.65 * dt))
        self.add(membrane)
        self.at("A protein")
        protein = chip("protein", BLUE, 36).move_to([-1.15, .35, 0])
        self.play(FadeIn(protein, scale=.8), run_time=.5)
        self.at("builds cells")
        work = T("builds cells • does work", 28, BLUE).next_to(cell, UP, buff=.35)
        self.play(FadeIn(work), run_time=.5)
        self.at("Proteins contain nitrogen")
        tags1 = VGroup(*[Dot(protein.get_center() + [dx, -.45, 0], radius=.11, color=USABLE) for dx in (-.45, 0, .45)])
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * .2) for d in tags1], lag_ratio=.16), run_time=.7)
        self.at("DNA")
        dna = chip("DNA", "#B58CD9", 36).move_to([1.35, -.45, 0])
        self.play(FadeIn(dna, scale=.8), run_time=.5)
        self.at("carries the plant's instructions")
        inst = T("instructions", 28, "#B58CD9").next_to(cell, DOWN, buff=.35)
        self.play(FadeIn(inst), run_time=.5)
        self.at("contains nitrogen too")
        tags2 = VGroup(*[Dot(dna.get_center() + [dx, -.45, 0], radius=.11, color=USABLE) for dx in (-.32, .32)])
        bud = VGroup(leaf_shape([2.7, 1.9, 0], 1.0, .5), leaf_shape([3.4, 1.8, 0], 1.0, -.5))
        self.play(LaggedStart(*[FadeIn(d) for d in tags2], lag_ratio=.2), GrowFromCenter(bud), run_time=.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Nogrow(SpokenScene):
    def construct(self):
        cell = Circle(radius=2.2, stroke_color=WATER, stroke_width=5, fill_color=WATER, fill_opacity=.09)
        protein = chip("protein", BLUE, 36).move_to([-1.15, .35, 0])
        dna = chip("DNA", "#B58CD9", 36).move_to([1.35, -.45, 0])
        self.add(cell, protein, dna, scope_tag("schematic"))
        pulse(cell, base=5, amp=2.0, speed=3.2)
        incoming = VGroup(*[Dot([-4.5 + i * .65, 2.3, 0], radius=.12, color=USABLE) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(d) for d in incoming], lag_ratio=.08), run_time=.45)
        self.at("without nitrogen")
        self.play(*[d.animate.set_color(GREY).set_opacity(.2) for d in incoming], run_time=.45)
        self.at("cannot build new proteins")
        ghost = chip("new protein", BLUE, 32).move_to([0, 1.35, 0]).set_opacity(.18)
        cross = Cross(ghost, stroke_color=RED, stroke_width=6)
        self.play(FadeIn(ghost), Create(cross), run_time=.55)
        self.at("grow new leaves")
        bud = VGroup(leaf_shape([3.35, .45, 0], 1.1, .45, .10),
                     leaf_shape([4.0, .35, 0], 1.1, -.45, .10))
        bud.set_color("#B9A45F")
        cap = caption("no nitrogen, no new leaves", 32, RED)
        self.play(FadeIn(bud), FadeIn(cap), run_time=.55)
        self.finish()


class S04Tank(SpokenScene):
    def construct(self):
        field = Rectangle(width=4.0, height=.65, stroke_color=SOIL, fill_color=SOIL_DARK,
                          fill_opacity=.7).move_to([0, -2.8, 0])
        field_lab = T("1 hectare", 30, TEXT).move_to(field)
        self.play(FadeIn(field), FadeIn(field_lab), run_time=.5)
        self.at("sky above one field")
        sky = RoundedRectangle(width=5.0, height=5.3, corner_radius=.2, stroke_color=N2,
                               stroke_width=4, fill_color=N2, fill_opacity=.10).move_to([-2.1, .15, 0])
        self.play(GrowFromEdge(sky, DOWN), run_time=.75)
        self.at("huge amount")
        pairs = gas_field([[-3.5, y, 0] for y in (-1.6, -.7, .2, 1.1, 2.0)] +
                          [[-2.1, y, 0] for y in (-1.2, -.3, .6, 1.5, 2.4)] +
                          [[-.7, y, 0] for y in (-1.6, -.7, .2, 1.1, 2.0)], .7)
        n = ValueTracker(0)
        count = counter("about {:,.0f}", n, at=[4.0, 3.0, 0], size=32, color=N2)
        units = T("tonnes of nitrogen", 28, N2).move_to([4.0, 2.55, 0])
        self.add(count, units)
        self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=.03), n.animate.set_value(78000), run_time=1.05)
        pulse(sky, base=4, amp=1.5, speed=3.0)
        self.at("soybeans growing there")
        soy = soy_plant(2.8, -2.45, 2.0)
        self.play(FadeIn(soy, shift=UP * .2), run_time=.55)
        self.at("tiny bit")
        tiny = Rectangle(width=.28, height=.05, stroke_color=USABLE, fill_color=USABLE,
                         fill_opacity=.8).move_to([4.8, -2.72, 0])
        lab = VGroup(T("soybeans above ground", 28, USABLE, weight=BOLD),
                     T("about 0.19 tonnes", 28, USABLE),
                     T("one Michigan study", 24, GREY)).arrange(DOWN, buff=.12).move_to([4.15, .85, 0])
        self.play(GrowFromEdge(tiny, DOWN), FadeIn(lab), run_time=.7)
        self.finish()


class S05Locked(SpokenScene):
    def construct(self):
        soil = Rectangle(width=12.8, height=4.15, stroke_width=0, fill_color=SOIL_DARK,
                         fill_opacity=.72).move_to([0, -1.25, 0])
        corn = corn_plant(0, .82, 3.0, True)
        self.play(FadeIn(soil), FadeIn(corn), run_time=.65)
        bob(corn, amp=.13, speed=3.0)
        self.at("cannot use nitrogen gas")
        pair = gas_pair([-3.8, 2.5, 0], 1.35)
        self.play(FadeIn(pair), run_time=.45)
        blocked = T("corn cannot use", 30, RED, weight=BOLD).move_to([-3.75, 1.75, 0])
        self.play(FadeIn(blocked), run_time=.4)
        self.at("deer or you")
        d = deer([3.85, 2.2, 0], .75)
        person = VGroup(Circle(radius=.18, color=TEXT), Line(DOWN*.18, DOWN*1.0, color=TEXT, stroke_width=4),
                        Line(DOWN*.5, LEFT*.38+DOWN*.9, color=TEXT, stroke_width=4),
                        Line(DOWN*.5, RIGHT*.38+DOWN*.9, color=TEXT, stroke_width=4)).move_to([5.0, 2.2, 0])
        self.play(FadeIn(d), FadeIn(person), run_time=.55)
        self.at("Gray pairs drift down")
        falling = gas_field([[-2.5, 2.8, 0], [-1.1, 2.4, 0], [1.3, 2.65, 0], [2.6, 2.25, 0]], 1.0)
        self.play(LaggedStart(*[p.animate.shift(DOWN * (4.5 + .25 * i)) for i, p in enumerate(falling)], lag_ratio=.12), run_time=1.7)
        self.at("right past the corn's roots")
        self.play(*[p.animate.shift(DOWN * .8) for p in falling], run_time=.6)
        self.at("stays clasped shut")
        lock = T("🔒", 38, GOLD).next_to(falling[-1], RIGHT, buff=.2)
        self.play(FadeIn(lock), Indicate(falling[-1][-1], color=GOLD), run_time=.55)
        self.at("gate is locked")
        cap = caption("nitrogen gas: locked shut", 34, GOLD)
        self.play(FadeOut(falling), FadeOut(lock), FadeIn(cap), run_time=.45)
        self.finish()


class S06Usable(SpokenScene):
    def construct(self):
        world = farm_world(pairs=True, water=True, plants=False)
        corn = corn_plant(1.0, .2, 2.4, True)
        self.play(FadeIn(world), FadeIn(corn), run_time=.7)
        bob(world[7], amp=.14, speed=3.0)
        bob(corn, amp=.10, speed=2.7)
        self.at("only usable nitrogen")
        dots = VGroup(*[Dot([-.9 + .42*i, -2.65 + .12*(i%2), 0], radius=.12, color=USABLE) for i in range(6)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=.08), run_time=.6)
        label = T("usable nitrogen", 32, USABLE, weight=BOLD).move_to([-3.9, -2.65, 0])
        self.play(FadeIn(label), run_time=.35)
        self.at("changed out of the gas")
        pair = gas_pair([-2.8, -1.2, 0], 1.05)
        opening = gas_pair([-2.8, -1.2, 0], 1.05, True)
        newdots = VGroup(Dot([-3.05, -1.2, 0], radius=.13, color=USABLE), Dot([-2.55, -1.2, 0], radius=.13, color=USABLE))
        self.play(FadeIn(pair), run_time=.35)
        self.play(ReplacementTransform(pair, opening), ReplacementTransform(opening.copy(), newdots), run_time=.65)
        self.at("Roots take most")
        self.play(*[d.animate.move_to([.65 + .13*i, -.55 + .26*i, 0]) for i, d in enumerate(dots[:4])], run_time=1.0)
        self.at("soil water")
        self.play(Indicate(world[-1], color=WATER, scale_factor=1.02), run_time=.5)
        self.at("green pool is small")
        frame = SurroundingRectangle(world[0], color=N2, buff=.02)
        self.play(Create(frame), world[-1].animate.scale(.75), run_time=.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S07Changers(SpokenScene):
    def construct(self):
        soil = Rectangle(width=12.8, height=2.2, stroke_width=0, fill_color=SOIL_DARK,
                         fill_opacity=.72).move_to([0, -2.35, 0])
        incoming = gas_field([[-5.2, 2.5, 0], [-4.2, 2.1, 0], [3.8, 2.45, 0], [4.8, 2.0, 0]], 1.0)
        self.add(soil, incoming)
        bob(incoming, amp=.14, speed=3.0)
        self.at("who opens the gate")
        q = T("Who opens the clasp?", 38, GOLD, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(q), run_time=.45)
        self.at("Lightning opens")
        bolt = Polygon([-.35, 2.45, 0], [.2, 1.4, 0], [-.15, 1.4, 0], [.25, .2, 0],
                       [-.55, 1.25, 0], [-.2, 1.25, 0], stroke_color=YELLOW,
                       fill_color=YELLOW, fill_opacity=.7).move_to([-3.6, .2, 0])
        self.play(FadeIn(bolt, scale=.6), run_time=.25)
        opened = gas_pair([-4.7, -.6, 0], 1.0, True)
        greenfew = VGroup(Dot([-4.95, -1.2, 0], radius=.13, color=USABLE), Dot([-4.45, -1.2, 0], radius=.13, color=USABLE))
        self.play(ReplacementTransform(incoming[0], opened), FadeIn(greenfew, shift=DOWN*.3), run_time=.55)
        little = T("lightning: a little", 28, YELLOW, weight=BOLD).move_to([-3.8, -3.15, 0])
        self.play(FadeIn(little), run_time=.4)
        self.at("Factories that make fertilizer")
        factory_body = Rectangle(width=2.5, height=1.55, stroke_color=TEXT,
                                 fill_color=TEXT, fill_opacity=.12).move_to([3.8, .15, 0])
        factory_stack = Rectangle(width=.42, height=1.25, stroke_color=TEXT,
                                  fill_color=TEXT, fill_opacity=.12).move_to([4.5, 1.55, 0])
        factory = VGroup(factory_body, factory_stack,
                         T("factory", 30, TEXT, weight=BOLD).move_to(factory_body))
        self.play(FadeIn(factory, shift=UP*.2), incoming[2:].animate.move_to([3.0, 1.0, 0]), run_time=.65)
        self.at("open it wide")
        bag = chip("fertilizer", USABLE, 32).move_to([3.8, -1.15, 0])
        many = VGroup(*[Dot([2.3 + .4*(i%8), -2.2 - .25*(i//8), 0], radius=.11, color=USABLE) for i in range(16)])
        self.play(FadeIn(bag), LaggedStart(*[FadeIn(d, shift=DOWN*.2) for d in many], lag_ratio=.03), run_time=.8)
        a_lot = T("fertilizer factory: a lot", 28, USABLE, weight=BOLD).move_to([3.8, -3.15, 0])
        self.play(FadeIn(a_lot), run_time=.35)
        self.at("material farmers add")
        self.play(Indicate(bag, color=USABLE), run_time=.45)
        self.at("supply nutrients")
        self.play(many.animate.shift(UP*.35), run_time=.55)
        self.finish()


class S08Bacteria(SpokenScene):
    def construct(self):
        soil = Rectangle(width=12.8, height=7.0, stroke_width=0, fill_color=SOIL_DARK,
                         fill_opacity=.72)
        rods = bacteria_group([0, .25, 0], 2.3, 14)
        self.add(soil)
        self.at("bacteria open the gate")
        pair = gas_pair([-4.7, .3, 0], 1.35)
        seed_rod = rods[0]
        self.play(FadeIn(seed_rod, scale=.6), FadeIn(pair), pair.animate.move_to([-1.55, .3, 0]), run_time=.65)
        self.at("tiny living things")
        self.play(LaggedStart(*[FadeIn(r, scale=.6) for r in rods[1:]], lag_ratio=.04), run_time=.6)
        ring = SurroundingRectangle(rods, color=ORANGE, buff=.2, corner_radius=.25)
        label = T("bacteria", 34, ORANGE, weight=BOLD).move_to([0, 3.1, 0])
        self.play(Create(ring), FadeIn(label), run_time=.5)
        pulse(ring, base=4, amp=1.8, speed=3.2)
        self.at("each made of one cell")
        one = T("one cell each", 30, ORANGE).move_to([0, 2.55, 0])
        self.play(FadeIn(one), Indicate(rods[3], color=ORANGE), run_time=.55)
        self.at("live free in the soil")
        self.play(rods.animate.shift(DOWN*.55), run_time=.55)
        self.at("turns gray pairs")
        opened = gas_pair([-1.55, -.25, 0], 1.35, True)
        out = VGroup(Dot([3.6, .4, 0], radius=.18, color=USABLE), Dot([4.15, .4, 0], radius=.18, color=USABLE))
        self.play(ReplacementTransform(pair, opened), run_time=.45)
        self.at("into green dots")
        arrow = Arrow([1.4, .4, 0], [3.15, .4, 0], color=USABLE, buff=0, stroke_width=6)
        self.play(GrowArrow(arrow), FadeIn(out), run_time=.6)
        summary = VGroup(T("lightning", 26, YELLOW), T("factory", 26, TEXT), T("bacterium", 26, ORANGE)).arrange(RIGHT, buff=.9).move_to([0, -2.75, 0])
        self.play(FadeOut(ring), FadeIn(summary), run_time=.5)
        self.add(scope_tag("schematic"))
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        self.play(FadeIn(back), run_time=.65)
        self.at("almost no usable nitrogen")
        self.play(Indicate(back[1], color=USABLE, scale_factor=1.4), run_time=.55)
        self.at("Corn and soybeans")
        self.play(Indicate(back[0][6], color=GOLD, scale_factor=1.03), run_time=.55)
        self.at("same air")
        self.play(Indicate(back[2], color=N2), run_time=.4)
        self.at("Which one could still grow well")
        q = question_card("Almost no usable nitrogen in the soil. Which could still grow well?",
                          ["corn", "soybean"], size=29, chip_size=28)
        self.play(FadeIn(q.chips), run_time=.4)
        self.play(FadeIn(q.question), run_time=.5)
        self.at("Pause and decide")
        self.play(Indicate(q.question, color=GOLD), run_time=.45)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Almost no usable nitrogen in the soil. Which could still grow well?"
    OPTIONS = ["corn", "soybean"]
    CARD = {"size": 29, "chip_size": 28}

    def backdrop(self):
        return predict_backdrop()


class S11Reveal(SpokenScene):
    def construct(self):
        soil = Rectangle(width=12.8, height=4.0, stroke_width=0, fill_color=SOIL_DARK,
                         fill_opacity=.72).move_to([0, -1.6, 0])
        soy = soy_plant(0, -.05, 2.4, True)
        self.add(soil)
        self.at("The soybean")
        answer = T("soybean", 42, USABLE, weight=BOLD).move_to([-4.65, 3.1, 0])
        self.play(FadeIn(answer), FadeIn(soy), run_time=.65)
        self.at("Dig it up")
        hand = VGroup(RoundedRectangle(width=1.4, height=.55, corner_radius=.22,
                                       stroke_color=TEXT, fill_color=TEXT, fill_opacity=.14),
                      Line([.65, 0, 0], [1.4, .45, 0], color=TEXT, stroke_width=8)).move_to([2.3, .2, 0])
        self.play(FadeIn(hand), soy.animate.shift(UP*.65), run_time=.65)
        bob(soy, amp=.12, speed=3.0)
        self.at("shake off the soil")
        crumbs = VGroup(*[Dot([-.9 + .3*i, -1.0 - .12*(i%3), 0], radius=.08, color=SOIL) for i in range(7)])
        self.play(LaggedStart(*[d.animate.shift(DOWN*1.2).set_opacity(0) for d in crumbs], lag_ratio=.06), run_time=.75)
        self.at("small round bumps")
        bumps = soy[-1]
        self.play(LaggedStart(*[Indicate(b, color=ORANGE, scale_factor=1.35) for b in bumps], lag_ratio=.12), run_time=.7)
        self.at("root nodule")
        label = T("root nodule", 32, ORANGE, weight=BOLD).move_to([-3.9, -2.7, 0])
        self.play(FadeIn(label), run_time=.45)
        self.at("packed with bacteria")
        nodule = Circle(radius=1.55, stroke_color=ORANGE, stroke_width=5,
                        fill_color=ORANGE, fill_opacity=.10).move_to([3.75, -.7, 0])
        rods = bacteria_group(nodule.get_center(), 1.3, 12)
        self.play(FadeIn(nodule, scale=.6), LaggedStart(*[FadeIn(r) for r in rods], lag_ratio=.04), run_time=.85)
        self.add(scope_tag("schematic"))
        self.finish()


class S12Nodule(SpokenScene):
    def construct(self):
        world = root_closeup("soy", True)
        nodule = Circle(radius=1.5, stroke_color=ORANGE, stroke_width=5,
                        fill_color=ORANGE, fill_opacity=.10).move_to([3.7, -.8, 0])
        rods = bacteria_group(nodule.get_center(), 1.25, 11)
        self.add(world, nodule, rods, scope_tag("schematic"))
        pulse(nodule, base=5, amp=2.0, speed=3.2)
        bob(rods, amp=.10, speed=2.8)
        self.at("bacteria take in nitrogen gas")
        pairs = gas_field([[5.8, .5, 0], [5.4, -.35, 0], [5.8, -1.25, 0]], .9)
        self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=.1), run_time=.55)
        self.play(*[p.animate.move_to(nodule.get_center() + [.3*(i-1), .15*(i-1), 0]) for i,p in enumerate(pairs)], run_time=.75)
        self.at("pass usable nitrogen")
        dots = VGroup(*[Dot(nodule.get_center()+[.3*(i-2), -.2, 0], radius=.13, color=USABLE) for i in range(5)])
        self.play(FadeOut(pairs), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=.08), run_time=.55)
        self.at("to the plant")
        up = Arrow([3.1, -.35, 0], [.65, 1.25, 0], color=USABLE, stroke_width=8, buff=0)
        self.play(GrowArrow(up), *[d.animate.shift(LEFT*(2.3+.12*i)+UP*(1.0+.12*i)) for i,d in enumerate(dots)], run_time=.9)
        self.at("carries its own gate opener")
        cap = caption("a private gate opener", 34, GOLD)
        self.play(FadeIn(cap), run_time=.45)
        self.at("right on its roots")
        self.play(Indicate(world[1][-1], color=ORANGE, scale_factor=1.2), run_time=.55)
        self.finish()


class S13Sugar(SpokenScene):
    def construct(self):
        world = root_closeup("soy", True)
        nodule = Circle(radius=1.5, stroke_color=ORANGE, stroke_width=5,
                        fill_color=ORANGE, fill_opacity=.10).move_to([3.7, -.8, 0])
        rods = bacteria_group(nodule.get_center(), 1.25, 11)
        green = Arrow([3.1, -.35, 0], [.65, 1.25, 0], color=USABLE, stroke_width=8, buff=0)
        self.add(world, nodule, rods, green, scope_tag("schematic"))
        pulse(nodule, base=5, amp=2.0, speed=3.2)
        bob(rods, amp=.10, speed=2.8)
        self.at("sends sugar from its leaves")
        sugar = Arrow([-.65, 2.7, 0], [2.7, -.35, 0], color=ORANGE, stroke_width=8, buff=0)
        self.play(GrowArrow(sugar), run_time=.8)
        sugar_lab = T("sugar", 32, ORANGE, weight=BOLD).move_to([-3.7, 2.7, 0])
        self.play(FadeIn(sugar_lab), run_time=.35)
        self.at("down to the nodules")
        self.play(Indicate(nodule, color=ORANGE), run_time=.5)
        self.at("Root cells there change the sugar")
        crumbs = VGroup(*[Dot(nodule.get_center()+[.32*np.cos(i), .32*np.sin(i), 0], radius=.10, color=ORANGE) for i in range(7)])
        self.play(LaggedStart(*[FadeIn(c, scale=.5) for c in crumbs], lag_ratio=.08), run_time=.6)
        self.at("food the bacteria can use")
        food = T("food for bacteria", 30, ORANGE, weight=BOLD).move_to([3.7, -2.65, 0])
        partners = T("partners", 34, TEXT, weight=BOLD).move_to([0, -3.15, 0])
        self.play(FadeIn(food), FadeIn(partners), run_time=.55)
        self.play(Indicate(green, color=USABLE), Indicate(sugar, color=ORANGE), run_time=.6)
        self.finish()


class S14Corn(SpokenScene):
    def construct(self):
        soil = Rectangle(width=12.8, height=4.8, stroke_width=0, fill_color=SOIL_DARK,
                         fill_opacity=.72).move_to([0, -1.0, 0])
        corn = corn_plant(0, .75, 2.7, True)
        self.play(FadeIn(soil), FadeIn(corn), run_time=.65)
        bob(corn, amp=.13, speed=3.0)
        self.at("no root nodules")
        smooth = T("smooth roots — no nodules", 32, RED, weight=BOLD).move_to([3.7, -1.5, 0])
        self.play(FadeIn(smooth), run_time=.5)
        self.at("green dots already in the soil")
        pool = RoundedRectangle(width=4.0, height=.75, corner_radius=.25, stroke_color=WATER,
                                fill_color=WATER, fill_opacity=.18).move_to([0, -2.85, 0])
        dots = VGroup(*[Dot([-1.2+.48*i, -2.85, 0], radius=.12, color=USABLE) for i in range(6)])
        self.play(FadeIn(pool), FadeIn(dots), run_time=.55)
        self.play(*[d.animate.move_to([-.45+.18*i, -.5+.25*i, 0]) for i,d in enumerate(dots[:4])], run_time=.85)
        self.at("corn farmers usually add nitrogen")
        bag = chip("fertilizer", USABLE, 34).move_to([4.6, 1.5, 0])
        refill = VGroup(*[Dot([3.6+.35*(i%5), .7-.22*(i//5), 0], radius=.11, color=USABLE) for i in range(10)])
        self.play(FadeIn(bag), LaggedStart(*[d.animate.move_to([-.9+.4*(i%5), -2.75-.2*(i//5), 0]) for i,d in enumerate(refill)], lag_ratio=.04), run_time=.9)
        self.at("to their fields")
        self.play(Indicate(pool, color=USABLE, scale_factor=1.03), run_time=.5)
        self.add(scope_tag("schematic"))
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        world = farm_world(pairs=True, water=True, plants=True)
        self.add(world)
        bob(world[7], amp=.14, speed=3.0)
        self.at("air's nitrogen is not the problem")
        sky_box = SurroundingRectangle(world[0], color=N2, buff=.02)
        self.play(Create(sky_box), run_time=.55)
        self.at("The gate is")
        clasp = gas_pair([0, 1.65, 0], 2.2)[-1]
        self.play(FadeIn(clasp, scale=.4), run_time=.55)
        self.at("Plants need usable nitrogen")
        self.play(FadeOut(sky_box), run_time=.25)
        dots = VGroup(*[Dot([-1.1+.4*i, -2.65, 0], radius=.13, color=USABLE) for i in range(7)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=.08), run_time=.6)
        rule = T("plants need usable nitrogen", 34, USABLE, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(rule), run_time=.4)
        self.at("not the nitrogen gas")
        self.play(world[7].animate.set_opacity(.25), run_time=.45)
        self.at("Where nitrogen runs short")
        tag = T("where nitrogen runs short", 30, GOLD).move_to([-3.5, -3.25, 0])
        self.play(FadeIn(tag), run_time=.4)
        self.at("usable nitrogen sets")
        level = ValueTracker(.25)
        gauge = always_redraw(lambda: Rectangle(width=.55, height=2.6*level.get_value(),
                                                 stroke_color=USABLE, fill_color=USABLE, fill_opacity=.55)
                              .move_to([5.8, -2.8+1.3*level.get_value(), 0]))
        self.add(gauge)
        self.play(level.animate.set_value(1.0), run_time=.85)
        self.at("how much a field can grow")
        taller = VGroup(soy_plant(-3.2, .2, 2.6), corn_plant(1.0, .2, 3.0))
        self.play(FadeOut(rule), FadeOut(tag), ReplacementTransform(world[6], taller),
                  dots.animate.shift(UP*.7), run_time=1.0)
        self.finish()


class S16Tease(SpokenScene):
    def construct(self):
        panels = TwoPanel("soybean with nodules", "soybean without nodules", colors=(ORANGE, GREY),
                          top=3.1, bottom=-2.5, gap=1.2, width=11.5)
        left = soy_plant(-3.2, -.75, 1.95, True)
        right = soy_plant(3.2, -.75, 1.95, False)
        self.play(FadeIn(panels), FadeIn(left), FadeIn(right), run_time=.7)
        bob(left, amp=.10, speed=2.8)
        bob(right, amp=.10, speed=3.1, seed=2)
        self.at("bumps really add nitrogen")
        qmark = T("?", 90, GOLD, weight=BOLD).move_to([0, -.1, 0])
        self.play(FadeIn(qmark, scale=.5), run_time=.55)
        q = caption("Do the bumps really add nitrogen?", 34, GOLD)
        self.play(FadeIn(q), run_time=.45)
        self.at("lesson tests that")
        self.play(Indicate(left[-1], color=ORANGE, scale_factor=1.25), run_time=.5)
        self.at("real field data")
        data = T("real field data", 34, TEXT, weight=BOLD).move_to([0, -3.1, 0])
        self.play(swap(q, data), run_time=.55)
        self.finish()


class S17End(EndCard):
    LINE = "Plants need usable nitrogen, not the nitrogen gas in air."
