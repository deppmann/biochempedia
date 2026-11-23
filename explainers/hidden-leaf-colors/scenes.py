"""A tabletop field notebook for the Hidden Leaf Colors parent guide."""

from bp_parts import *

# COLOR MAP (shared palette): GREEN = fresh leaf/chlorophyll, YELLOW = hidden
# yellow pigment, RED = fall red pigment, BLUE = water, GOLD = sugar.
INK = "#30271F"
PAPER = "#FFFCF1"
PAPER_EDGE = "#C3AE8C"
COVER = "#3E5550"
METAL = "#B7C6CC"
SKIN = "#BC7955"
FIBER = "#E7DCC5"
LEAF_EDGE = {GREEN: "#3D6533", YELLOW: "#93721D", RED: "#903C32"}
LEAF_VEIN = {GREEN: "#E1EBA6", YELLOW: "#FFF1AD", RED: "#FFD2A3"}

PREDICT = "Was red also hidden under green all summer?"
PREDICT_CARD = dict(y=-2.85, color=INK, size=40, max_w=11.6)


def point(x, y):
    return np.array([x, y, 0.0])


def shape(vertices, fill, edge, width=2):
    return Polygon(*[point(*p) for p in vertices], color=edge, stroke_width=width,
                   fill_color=fill, fill_opacity=1)


def line(a, b, color=INK, width=2):
    return Line(point(*a), point(*b), color=color, stroke_width=width)


def tabletop():
    """Warm overhead light on the same tabletop in each activity scene."""
    y, x = np.mgrid[-1:1:200j, -1:1:356j]
    light = 31 * np.exp(-1.5 * ((x + 0.40) ** 2 + (y + 0.55) ** 2))
    grain = 2 * np.sin(36 * y + 0.9 * np.sin(3 * x)) + np.sin(120 * y + x)
    seams = sum(np.exp(-((y - p) / 0.009) ** 2) for p in (-0.61, 0.18, 0.82))
    base = np.array([204, 166, 120])
    pixels = np.clip(base + (light + grain - 15 * seams)[..., None], 0, 255).astype(np.uint8)
    return ImageMobject(pixels).stretch_to_fit_width(config.frame_width).stretch_to_fit_height(8).set_z_index(-20)


def paper_label(text):
    backing = paper_face(text.width + .55, text.height + .32).move_to(text)
    return VGroup(backing, text)


def backed_question(words, **layout):
    return paper_label(question_card(words, **layout))


def leaf(color, at=ORIGIN, height=4.3, angle=0, maple=False, print_ink=False):
    """A paper leaf with a stem and ribs. Prints use the matching leaf silhouette."""
    edge, vein = LEAF_EDGE[color], LEAF_VEIN[color]
    if maple:
        right = [(0.23, 1.00), (0.49, 1.12), (0.38, 0.23), (0.75, 0.43), (0.88, 0.87),
                 (1.02, 0.64), (1.56, 0.72), (1.39, 0.14), (1.59, 0.00), (0.93, -0.40),
                 (1.01, -0.65), (0.33, -0.84)]
        verts = [(0, 1.56), *right, (0, -0.79), *[(-x, y) for x, y in reversed(right)]]
        blade = shape(verts, color, edge, 2.7)
        ribs = [((0, -0.52), (0.88 * side, 0.66)) for side in (-1, 1)]
        ribs += [((0, -0.61), (1.24 * side, 0.17)) for side in (-1, 1)]
    else:
        blade = VMobject(fill_color=color, fill_opacity=1, stroke_color=edge, stroke_width=2.7)
        blade.start_new_path(point(0, -1.15))
        blade.add_cubic_bezier_curve_to(point(-1.39, -0.83), point(-1.41, 0.52), point(0.11, 1.53))
        blade.add_cubic_bezier_curve_to(point(1.37, 0.59), point(1.34, -0.84), point(0, -1.15))
        blade.close_path()
        ribs = []
        for i, y in enumerate((-0.86, -0.49, -0.10, 0.31, 0.66)):
            tip = (0.47, 0.76, 0.77, 0.61, 0.40)[i]
            ribs.extend(((0.02, y), (tip * side, y + 0.42)) for side in (-1, 1))
    stem = line((0.03, -1.58), (0, -0.76), edge, 5)
    midrib = line((0, -1.13 if not maple else -0.78), (0.07, 1.39), vein, 2.8)
    veins = VGroup(*[line(a, b, vein, 1.6) for a, b in ribs])
    freckles = VGroup()
    if not maple:
        for i, (x, y) in enumerate([(-.32, -.56), (.38, -.40), (-.54, -.04), (.47, .10),
                                     (-.38, .34), (.29, .51), (-.19, .73), (.15, .92)]):
            freckles.add(Dot(point(x, y), radius=0.028 + 0.008 * (i % 3), color=edge, fill_opacity=0.6))
    if print_ink:
        blade.set_fill(color, 0.70).set_stroke(edge, 1.2, 0.38)
        veins.set_opacity(0.7)
        stem.set_stroke(edge, 2, 0.48)
        g = VGroup(stem, blade, midrib, veins, freckles)
    else:
        shadow = blade.copy().set_fill(INK, 0.15).set_stroke(width=0).shift(point(.09, -.10))
        g = VGroup(shadow, stem, blade, midrib, veins, freckles)
    return g.set_height(height).rotate(angle).move_to(at)


def comparison_leaves(y=0.33):
    return (leaf(GREEN, point(-4.30, y), 4.55, 0.21),
            leaf(YELLOW, point(4.27, y), 4.55, -0.23))


def paper_face(w, h, color=PAPER):
    return RoundedRectangle(width=w, height=h, corner_radius=.08, fill_color=color,
                            fill_opacity=1, stroke_color=PAPER_EDGE, stroke_width=1.2)


def sheet(at, w=4.8, h=5.15):
    page = paper_face(w, h)
    shadow = page.copy().set_fill(INK, .16).set_stroke(width=0).shift(point(.10, -.10))
    return VGroup(shadow, page).move_to(at)


def notebook():
    at = point(3.4, 0.20)
    cover = paper_face(5.18, 5.82, COVER).set_stroke("#223E3A", 2)
    pages = paper_face(4.92, 5.57).shift(UP * .04)
    spine = line((-.02, -1.25), (-.02, 1.39), FIBER, 2)
    return VGroup(cover, pages, spine).move_to(at)


def guess_page():
    heading = T("My guess", 34, INK, weight=BOLD).move_to(point(3.39, 2.12))
    swatch = VGroup(
        Line(point(2.51, .95), point(3.2, 1.10), color=LEAF_EDGE[GREEN], stroke_width=6),
        Line(point(2.56, .79), point(3.38, .91), color=LEAF_EDGE[GREEN], stroke_width=6),
        Line(point(2.68, .63), point(3.47, .78), color=LEAF_EDGE[GREEN], stroke_width=5),
    )
    return heading, swatch


def pencil():
    wood = shape([(-.85, -.11), (.65, -.11), (1.04, 0), (.65, .11), (-.85, .11)], "#D89A36", INK)
    tip = shape([(.65, -.11), (1.04, 0), (.65, .11)], "#F1C989", INK, 1.2)
    graphite = shape([(.90, -.04), (1.04, 0), (.90, .04)], INK, INK, 1)
    return VGroup(wood, tip, graphite).rotate(2.3)


def spoon(at, length=4.45, angle=0.22):
    handle = RoundedRectangle(width=.30, height=2.7, corner_radius=.14,
                              fill_opacity=1, fill_color=METAL, color="#536973", stroke_width=2.7)
    handle.shift(UP * .72)
    bowl = Ellipse(width=1.02, height=1.67, fill_color=METAL, fill_opacity=1,
                   stroke_color="#536973", stroke_width=2.7).shift(DOWN * 1.07)
    shine = ArcBetweenPoints(point(-.29, -1.54), point(-.27, -.67), angle=-.70).set_stroke(PAPER, 4)
    return VGroup(handle, bowl, shine).set_height(length).rotate(angle).move_to(at)


def strip(at=point(0, .38), height=5.05, horizontal=False, bands=True):
    page = sheet(ORIGIN, 1.87, 5.05)
    wash = []
    for i in range(7):
        x = -.72 + i * .24
        wash.append(line((x, -2.10), (x + .09, 2.11), FIBER, 1).set_opacity(.43))
    green = shape([(-.80, -.64), (-.47, -.57), (.05, -.61), (.45, -.57), (.79, -.66),
                   (.80, .22), (.44, .27), (-.02, .20), (-.43, .26), (-.79, .16)], GREEN, GREEN, 0)
    yellow = shape([(-.80, 1.14), (-.38, 1.19), (.08, 1.17), (.43, 1.20), (.79, 1.15),
                    (.79, 1.39), (.38, 1.44), (-.10, 1.40), (-.44, 1.43), (-.80, 1.37)], YELLOW, YELLOW, 0)
    g = VGroup(page, VGroup(*wash), green, yellow)
    g.set_height(height).rotate(PI / 2 if horizontal else 0).move_to(at)
    if not bands:
        green.set_opacity(0)
        yellow.set_opacity(0)
    return g, green, yellow


def hook_world():
    fresh, fall = comparison_leaves()
    sample, _, _ = strip(point(0, -2.68), horizontal=True, bands=False)
    return VGroup(fresh, fall, sample)


def supply_world():
    white = sheet(point(-3.5, .03), 4.85, 5.7)
    utensil = spoon(point(-1.98, .70), 3.73)
    fresh = leaf(GREEN, point(-4.50, .93), 3.43, .30)
    yellow = leaf(YELLOW, point(-4.49, -1.67), 1.68, 1.12)
    red = leaf(RED, point(-2.42, -1.74), 1.55, -.29, maple=True)
    return white, utensil, fresh, yellow, red


def walker(at, scale, color):
    head = Dot(point(0, .61), radius=.16, color=SKIN)
    body = shape([(-.20, .40), (.17, .42), (.27, -.07), (-.20, -.07)], color, INK, 1.8)
    legs = VGroup(line((-.12, -.09), (-.19, -.53), INK, 5), line((.14, -.09), (.29, -.48), INK, 5))
    arms = VGroup(line((-.15, .36), (-.40, .02), color, 6), line((.14, .37), (.44, .10), color, 6))
    return VGroup(legs, body, arms, head).scale(scale).move_to(at)


def outdoor_sketch():
    ground = ArcBetweenPoints(point(1.26, -.80), point(5.42, -.39), angle=.34).set_stroke(LEAF_EDGE[GREEN], 3)
    people = VGroup(walker(point(2.17, .04), 1.35, COVER),
                    walker(point(3.18, -.23), .94, LEAF_EDGE[RED]))
    road = shape([(4.95, -1.36), (5.52, -1.34), (5.58, .83), (5.36, .76)], "#7A817C", "#555B58", 1)
    dash = VGroup(*[line((5.28 + i * .07, -1.18 + i * .51), (5.31 + i * .07, -.93 + i * .51), PAPER, 2)
                    for i in range(4)])
    fallen = leaf(YELLOW, point(3.75, -.82), .73, -1.05)
    return ground, people, VGroup(road, dash), fallen


def safety_label(words):
    return T(words, 30, INK, weight=BOLD).move_to(point(3.42, -2.04))


def po_ivy():
    leaves = VGroup(*(leaf(GREEN, point(x, y), 1.45, angle) for x, y, angle in
                      [(3.45, 1.59, .03), (2.53, .54, .86), (4.37, .54, -.86)]))
    stems = VGroup(line((3.45, -.78), (3.45, .95)), line((3.45, -.29), (2.74, .30)),
                   line((3.45, -.29), (4.17, .30)))
    slash = line((2.26, -.36), (4.61, 1.92), LEAF_EDGE[RED], 8)
    circle = Circle(radius=1.53, color=LEAF_EDGE[RED], stroke_width=5).move_to(point(3.43, .75))
    return VGroup(stems, leaves), VGroup(circle, slash)


def weather():
    rays = VGroup(*[Line(point(2.20, 1.76) + .39 * rotate_vector(RIGHT, a),
                         point(2.20, 1.76) + .54 * rotate_vector(RIGHT, a), color="#AA7927", stroke_width=3)
                    for a in np.linspace(0, TAU, 8, endpoint=False)])
    sun = VGroup(Dot(point(2.20, 1.76), radius=.29, color=YELLOW), rays)
    shirt = shape([(2.35, .62), (2.74, .94), (2.95, .98), (3.12, .72), (3.29, .98), (3.52, .94),
                   (3.91, .62), (3.68, .22), (3.53, .32), (3.53, -.58), (2.72, -.58), (2.72, .32),
                   (2.57, .22)], TEAL, COVER, 2)
    lens = Circle(radius=.54, color=COVER, stroke_width=6, fill_color=PAPER, fill_opacity=1).move_to(point(4.55, .99))
    legs = VGroup(*[line((4.55, 1.08 - .10 * i), (4.55 + s * (.28 + .02 * i), 1.23 - .18 * i))
                    for i in range(4) for s in (-1, 1)])
    tick = VGroup(line((4.93, .59), (5.32, .12), COVER, 9), lens, legs,
                  Ellipse(width=.28, height=.40, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(point(4.55, .99)))
    return VGroup(sun, shirt), tick


def soap_and_water():
    spout = VMobject().set_stroke("#59717A", 17)
    spout.set_points_as_corners([point(-4.85, .22), point(-4.85, 1.76), point(-2.47, 1.76), point(-2.47, 1.17)])
    knob = VGroup(line((-5.24, 2.03), (-4.46, 2.03), "#59717A", 11),
                  line((-4.85, 2.03), (-4.85, 1.76), "#59717A", 10))
    soap = RoundedRectangle(width=1.83, height=.88, corner_radius=.30, fill_color=TEAL,
                            fill_opacity=1, color=COVER, stroke_width=3).rotate(.22).move_to(point(-4.34, -1.14))
    water = VGroup(*[Line(point(-2.72 + .15 * i, .95), point(-2.79 + .21 * i, -1.30),
                          color=BLUE, stroke_width=3.8 + 1.3 * (i % 2)) for i in range(4)])
    bubbles = VGroup(*[Circle(radius=r, color="#447A83", stroke_width=2, fill_color=PAPER,
                              fill_opacity=.5).move_to(point(x, y)) for x, y, r in
                       [(-3.63, -.49, .19), (-3.97, -.33, .13), (-4.27, -.58, .17)]])
    return VGroup(spout, knob, soap), water, bubbles


def fold_world():
    # The marked crease is x = -3.55. The right flap folds onto the left half.
    base = sheet(point(-4.93, -.03), 2.81, 4.70)
    specimen = leaf(GREEN, point(-4.97, .03), 3.52, .10)
    flap = paper_face(2.80, 4.68).move_to(point(-2.12, .02))
    return base, specimen, flap


def folded_flap():
    return paper_face(2.81, 4.68, "#F6EFDF").move_to(point(-4.93, .02))


def fold_edge():
    return paper_face(.035, 4.68).move_to(point(-3.53, .02))


def rubbing_hand():
    handle = spoon(point(-4.91, .33), 3.42, -.69)
    palm = VMobject(fill_color=SKIN, fill_opacity=1, stroke_color="#75452F", stroke_width=2.5)
    palm.start_new_path(point(-2.83, 1.95))
    palm.add_cubic_bezier_curve_to(point(-3.02, 1.83), point(-3.61, 1.57), point(-3.82, 1.41))
    palm.add_cubic_bezier_curve_to(point(-4.04, 1.25), point(-3.89, 1.06), point(-3.72, 1.13))
    palm.add_cubic_bezier_curve_to(point(-3.63, 1.19), point(-3.55, 1.22), point(-3.47, 1.19))
    palm.add_cubic_bezier_curve_to(point(-3.64, .94), point(-3.42, .81), point(-3.24, .85))
    palm.add_cubic_bezier_curve_to(point(-3.01, .90), point(-2.88, 1.18), point(-2.72, 1.31))
    palm.add_cubic_bezier_curve_to(point(-2.59, 1.40), point(-2.49, 1.50), point(-2.42, 1.56))
    palm.close_path()
    return VGroup(handle, palm)


def print_pair(color, x, maple=False):
    source = leaf(color, point(x, 1.58), 2.3, .22, maple=maple)
    card = sheet(point(x, -1.16), 2.69, 2.68)
    ink = leaf(color, point(x, -1.16), 2.11, .20, maple=maple, print_ink=True)
    return VGroup(source, card, ink)


def sorting_leaves():
    ys = VGroup(leaf(YELLOW, point(-5.07, 1.65), 1.65, .48),
                leaf(YELLOW, point(-2.57, .43), 1.55, -.68),
                leaf(YELLOW, point(.02, -1.79), 1.42, .40))
    rs = VGroup(leaf(RED, point(-2.84, 1.68), 1.67, .31, maple=True),
                leaf(RED, point(-5.03, -.87), 1.50, -.21, maple=True),
                leaf(RED, point(.01, .98), 1.56, -.42, maple=True))
    return ys, rs


def predict_picture():
    fresh, fall = comparison_leaves(y=.45)
    fresh.scale(.79).move_to(point(-4.87, .51))
    fall.scale(.75).move_to(point(1.76, .52))
    plate = VGroup(
        Ellipse(width=3.65, height=5.02, fill_color=PAPER, fill_opacity=1, color=PAPER_EDGE, stroke_width=2.5),
        Ellipse(width=3.24, height=4.59, color=FIBER, stroke_width=2)).move_to(point(-1.47, .50))
    sample, _, band = strip(point(-1.46, .51), height=4.27)
    red = leaf(RED, point(4.76, .78), 3.27, .14, maple=True)
    plate.set_z_index(-1)
    return fresh, fall, plate, sample, red, band


def link_yellows(band, fall):
    start = band.get_right() + RIGHT * .07
    end = fall.get_left() + LEFT * .10 + UP * .28
    return CubicBezier(start, start + RIGHT * .55, end + UL * .40, end).set_stroke("#91670F", 4)


class S01Hook(SpokenScene):
    def construct(self):
        fresh, fall, sample = hook_world()
        self.add(tabletop())
        self.at("where does the yellow")
        fresh.rotate(-.13).shift(LEFT * .27)
        fall.rotate(.14).shift(RIGHT * .27)
        self.add(fresh, fall)
        question = backed_question("Where does the yellow in a fall leaf come from?",
                                   y=3.17, color=INK, size=41, max_w=11.8).shift(RIGHT * .50)
        self.play(FadeIn(question, shift=UP * .11), run_time=.65)
        self.at("start with a fresh")
        self.play(fresh.animate.shift(RIGHT * .27).rotate(.13),
                  fall.animate.shift(LEFT * .27).rotate(-.14), run_time=2.35)
        self.at("a sample coffee filter strip")
        self.play(FadeIn(sample, shift=LEFT * 1.65), run_time=2.45)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Hidden Leaf Colors: Parent Guide"
    LESSON = "Hidden Leaf Colors"

    def construct(self):
        world = hook_world()
        shade = Rectangle(width=config.frame_width - .66, height=7.47, stroke_width=0,
                          fill_color=BG, fill_opacity=.92)
        title = T(self.LESSON, 62, PAPER, font=TITLE_FONT)
        guide = T(self.TITLE.split(": ", 1)[1].capitalize(), 33, PAPER)
        card = VGroup(title, guide).arrange(DOWN, buff=.37)
        self.add(tabletop(), world)
        self.play(FadeIn(shade), run_time=.47)
        self.play(FadeIn(card, shift=UP * .13), run_time=.47)
        self.wait(1.06)


class S03Payoff(SpokenScene):
    def construct(self):
        book = notebook()
        heading, swatch = guess_page()
        page, _, open_flap = fold_world()
        folded = folded_flap()
        mark = leaf(GREEN, point(-4.91, .03), 3.63, .12, print_ink=True)
        yellow = leaf(YELLOW, point(-.52, 1.36), 1.57, -.52)
        red = leaf(RED, point(-.07, -.81), 1.65, .19, maple=True)
        sample, _, _ = strip(point(4.60, -.20), height=3.55)
        closed_cover = paper_face(2.56, 5.82, COVER).move_to(point(3.40, .20))
        self.add(tabletop(), page, folded, closed_cover)
        self.at("make a guess")
        self.play(FadeOut(closed_cover), GrowFromCenter(book), run_time=.62)
        self.add(heading)
        self.at("look closely at leaf prints")
        self.play(Transform(folded, fold_edge()), run_time=.46)
        self.add(mark)
        self.play(Transform(folded, open_flap), run_time=.91)
        self.at("sort leaves by color")
        yellow_mate = leaf(YELLOW, point(-.14, 1.96), 1.04, .25)
        red_mate = leaf(RED, point(-.62, -1.42), 1.03, -.29, maple=True)
        yellows = VGroup(yellow, yellow_mate)
        self.play(FadeIn(yellows, shift=DOWN * .95),
                  FadeIn(VGroup(red, red_mate), shift=UP * .95), Create(swatch), run_time=1.80)
        self.at("use the sample strip")
        self.play(FadeIn(sample, shift=LEFT * 1.06), run_time=2.60)
        self.at("a color you")
        self.play(sample.animate.rotate(-.09), yellows.animate.shift(UR * .52).rotate(-.16),
                  run_time=1.20)
        self.finish()


class S04Materials(SpokenScene):
    def construct(self):
        book = notebook()
        white, utensil, fresh, yellow, red = supply_world()
        ground, people, road, fallen = outdoor_sketch()
        self.add(tabletop(), book, white)
        self.at("this activity uses")
        label = backed_question("No alcohol", size=35, color=INK, y=-3.32).shift(LEFT * 2.99)
        self.play(FadeIn(label), white.animate.rotate(-.045), run_time=1.65)
        self.at("gather white paper")
        self.play(FadeOut(label), white.animate.rotate(.045), run_time=.80)
        self.at("a spoon")
        self.play(FadeIn(utensil, shift=UP * .55), run_time=.59)
        self.at("fresh green leaf")
        self.play(FadeIn(fresh, shift=RIGHT * .56), run_time=.76)
        self.at("leaves in different colors")
        self.play(FadeIn(yellow, shift=UP * .48), FadeIn(red, shift=UP * .70), run_time=1.66)
        self.at("if you go outside")
        self.play(Create(ground), run_time=.90)
        self.at("go with your child")
        self.play(FadeIn(people, shift=RIGHT * .56), run_time=1.58)
        self.at("where you have permission")
        permission = safety_label("Ask permission")
        self.play(FadeIn(permission), run_time=.90)
        self.at("away from roads")
        self.play(FadeIn(road), run_time=1.05)
        self.at("take leaves only")
        self.play(swap(permission, safety_label("Leaves you know")), FadeIn(fallen, shift=DOWN * .21), run_time=1.60)
        self.finish()


class S05Safety(SpokenScene):
    def construct(self):
        book = notebook()
        white, utensil, fresh, yellow, red = supply_world()
        ivy, prohibit = po_ivy()
        clothing, tick = weather()
        scraps = VGroup(*[leaf(c, point(x, y), h, a, maple=c == RED) for c, x, y, h, a in
                          [(RED, -4.85, .12, .44, .30), (YELLOW, -3.35, -.64, .40, -.53),
                           (GREEN, -4.24, -.72, .52, .31)]])
        basin, water, bubbles = soap_and_water()
        self.add(tabletop(), book, white, utensil, fresh, yellow, red)
        self.at("avoid poison ivy")
        self.play(FadeIn(ivy), run_time=.60)
        ivy_label = safety_label("Avoid poison ivy")
        self.play(Create(prohibit), FadeIn(ivy_label), run_time=1.30)
        self.at("dress for the sun")
        self.play(FadeOut(ivy), FadeOut(prohibit), FadeOut(ivy_label), run_time=.35)
        self.play(FadeIn(clothing, shift=UP * .33), run_time=1.10)
        self.at("check for ticks")
        self.play(FadeIn(tick, shift=LEFT * .42), run_time=1.62)
        self.at("small leaf pieces")
        self.play(FadeOut(VGroup(utensil, fresh, yellow, red)), FadeOut(clothing),
                  FadeOut(tick), FadeIn(scraps), run_time=.68)
        under_four = safety_label("Keep away from\nchildren under 4")
        self.play(FadeIn(under_four), scraps.animate.shift(UP * 1.70 + LEFT * .75).rotate(.30), run_time=2.20)
        self.at("call 911 if choking")
        emergency = safety_label("911 if choking")
        self.play(swap(under_four, emergency), run_time=1.25)
        self.at("never taste the leaves")
        never = safety_label("Never taste leaves")
        self.play(swap(emergency, never), FadeOut(scraps, shift=UP * .52), run_time=1.20)
        self.at("wash hands with soap")
        self.play(FadeIn(basin), Create(water), FadeIn(bubbles, shift=UP * .43),
                  swap(never, safety_label("Wash with soap")), run_time=1.40)
        self.play(bubbles.animate.shift(UP * .43 + RIGHT * .28), run_time=.65)
        self.finish()


class S06MakePrints(SpokenScene):
    def construct(self):
        book = notebook()
        heading, swatch = guess_page()
        fresh = leaf(GREEN, point(-4.92, .44), 4.62, .19)
        fall = leaf(YELLOW, point(-1.61, .37), 4.35, -.20)
        base, specimen, flap = fold_world()
        tool = pencil()
        tool.shift(swatch[0].get_start() - tool[2].get_vertices()[1])
        self.add(tabletop(), book, fresh, fall)
        fresh.shift(LEFT * .24).rotate(.09)
        fall.shift(RIGHT * .24).rotate(-.10)
        self.at("show the green and yellow")
        self.play(fresh.animate.shift(RIGHT * .24).rotate(-.09),
                  fall.animate.shift(LEFT * .24).rotate(.10), run_time=2.11)
        self.at("which colors do you think")
        question = backed_question("Which colors will rub off?", color=INK, size=38, y=-3.24).shift(RIGHT * .5)
        self.play(FadeIn(question), run_time=.54)
        self.play(fresh.animate.rotate(-.09), fall.animate.rotate(.12), run_time=1.65)
        self.at("have them draw")
        self.play(FadeOut(question), FadeIn(heading), FadeIn(tool, shift=UL * .65), run_time=.63)
        for index, (stroke, draw_time) in enumerate(zip(swatch, (.40, .46, .54))):
            if index:
                self.play(tool.animate.shift(stroke.get_start() - swatch[index - 1].get_end()),
                          run_time=.12)
            self.play(Create(stroke), tool.animate.shift(stroke.get_end() - stroke.get_start()),
                      run_time=draw_time, rate_func=linear)
        self.at("then fold a sheet")
        base.set_z_index(-1)
        self.play(FadeOut(fall), FadeOut(tool), FadeIn(base), run_time=.55)
        self.play(Transform(fresh, specimen), FadeIn(flap), run_time=.62)
        self.play(Transform(flap, fold_edge()), run_time=.63)
        self.play(Transform(flap, folded_flap()), run_time=.79)
        self.finish()


class S07ComparePrints(SpokenScene):
    def construct(self):
        book = notebook()
        heading, swatch = guess_page()
        base, specimen, open_flap = fold_world()
        folded = folded_flap()
        green = leaf(GREEN, point(-4.91, .03), 3.63, .12, print_ink=True)
        tool = rubbing_hand().set_z_index(10)
        self.add(tabletop(), base, specimen, folded, book, heading, swatch)
        self.at("rub the folded paper")
        self.play(FadeIn(tool, shift=UL * .42), run_time=.73)
        for offset in (DOWN * .82, UP * .82, DOWN * .64):
            self.play(tool.animate.shift(offset), run_time=.92, rate_func=smooth)
        self.at("keep rubbing until")
        self.add(green)
        green.set_opacity(0)
        self.play(tool.animate.shift(UP * .78), green.animate.set_opacity(.42), run_time=1.29)
        self.play(FadeOut(tool, shift=UR * .55), FadeOut(specimen), run_time=.45)
        self.play(Transform(folded, fold_edge()), run_time=.48)
        self.play(Transform(folded, open_flap), green.animate.set_opacity(.82), run_time=.65)
        g = print_pair(GREEN, -4.99)
        y = print_pair(YELLOW, -.98)
        r = print_pair(RED, 3.04, maple=True)
        self.at("repeat with a yellow")
        self.play(FadeOut(VGroup(base, folded, green, book, heading, swatch)),
                  FadeIn(g, shift=DOWN * .27), run_time=.55)
        self.play(FadeIn(y, shift=UP * .63), run_time=.75)
        self.at("a red leaf")
        self.play(FadeIn(r, shift=UP * .63), run_time=1.27)
        self.at("which colors came off")
        for pair in (g, y, r):
            self.play(pair[2].animate.rotate(.13), run_time=.53)
        self.at("compare the prints")
        note = VGroup(sheet(point(5.02, .0), 2.65, 2.05),
                      T("My guess", 30, INK, weight=BOLD).move_to(point(5.02, .47)),
                      swatch.copy().move_to(point(5.02, -.24)))
        self.play(g.animate.shift(LEFT * .18), y.animate.shift(LEFT * .66),
                  r.animate.shift(LEFT * 1.14), FadeIn(note, shift=UP * .47), run_time=1.65)
        self.finish()


class S08Sort(SpokenScene):
    def construct(self):
        book = notebook()
        fresh = leaf(GREEN, point(2.11, .36), 3.04, .28)
        sample_yellow = leaf(YELLOW, point(4.65, .39), 3.04, -.25)
        yellow, red = sorting_leaves()
        self.add(tabletop(), book)
        self.at("put the fallen leaves")
        self.play(LaggedStart(*(FadeIn(m, shift=UP * .48) for m in [*yellow, *red]), lag_ratio=.23),
                  run_time=2.47)
        self.at("sort them into piles")
        self.play(LaggedStart(*(m.animate.move_to(point(-4.89 + i * 1.68, 1.35))
                                for i, m in enumerate(yellow)), lag_ratio=.23), run_time=1.23)
        self.play(LaggedStart(*(m.animate.move_to(point(-4.89 + i * 1.68, -1.13))
                                for i, m in enumerate(red)), lag_ratio=.23), run_time=1.30)
        self.at("count the leaves")
        tallies = [line((-4.89 + i * 1.68, y - .19), (-4.89 + i * 1.68, y + .20), INK, 5)
                   for y in (.11, -2.39) for i in range(3)]
        self.play(LaggedStart(*(Create(t) for t in tallies), lag_ratio=.44), run_time=2.38)
        self.at("keep the green leaf")
        self.play(FadeIn(fresh, shift=UP * .38), run_time=1.15)
        self.at("a yellow leaf nearby")
        self.play(FadeIn(sample_yellow, shift=UP * .49), run_time=1.22)
        self.at("for the comparison")
        next_fresh, next_yellow = comparison_leaves()
        self.play(FadeOut(VGroup(book, yellow, red, *tallies)), run_time=.43)
        self.play(Transform(fresh, next_fresh), Transform(sample_yellow, next_yellow), run_time=1.16)
        self.finish()


def example_label(sample):
    return paper_label(place_label(T("Example strip", 32, INK, weight=BOLD), sample, dirs=(DOWN,), buff=.42))


class S09Sample(SpokenScene):
    def construct(self):
        fresh, fall = comparison_leaves()
        sample, green, yellow = strip(bands=False)
        self.add(tabletop(), fresh, fall)
        self.at("look at this drawing")
        self.play(FadeIn(sample, shift=LEFT * 1.80), run_time=2.25)
        label = example_label(sample)
        self.at("filter strip")
        self.play(FadeIn(label), run_time=.53)
        self.at("fresh green spinach")
        self.play(green.animate.set_opacity(1), fresh.animate.rotate(-.17), run_time=2.34)
        self.at("a thin yellow one")
        self.play(yellow.animate.set_opacity(1), fresh.animate.rotate(.17), run_time=1.60)
        self.at("where do you see yellow")
        connection = link_yellows(yellow, fall)
        ring = SurroundingRectangle(yellow, buff=.12, color="#91670F", stroke_width=3, corner_radius=.12)
        self.play(Create(connection), Create(ring), run_time=1.35)
        self.play(FadeOut(ring), Indicate(fall, scale_factor=1.065, color=YELLOW), run_time=1.27)
        self.finish()


class S10PredictQ(SpokenScene):
    def construct(self):
        fresh, fall = comparison_leaves()
        sample, _, yellow = strip()
        next_fresh, next_fall, plate, plated_strip, red, next_band = predict_picture()
        # Reuse the band's own coordinates so the connection leads to the exact same marks.
        connection = link_yellows(yellow, fall)
        label = example_label(sample)
        self.add(tabletop(), fresh, fall, sample, connection, label)
        self.at("the yellow was already")
        self.play(FadeIn(plate, shift=UP * .17), Transform(fresh, next_fresh), Transform(fall, next_fall),
                  Transform(sample, plated_strip), Transform(connection, link_yellows(next_band, next_fall)),
                  FadeOut(label), run_time=2.63)
        self.at("here is a follow")
        self.play(FadeOut(connection), run_time=.56)
        self.at("before your child")
        self.play(FadeIn(red, shift=DOWN * .86), run_time=1.75)
        self.at("was a red fall leaf")
        self.play(FadeIn(backed_question(PREDICT, **PREDICT_CARD)), run_time=.72)
        self.play(Rotate(red, angle=-.23, rate_func=there_and_back), run_time=3.74)
        self.finish()


class S11PredictPause(PredictPause):
    QUESTION = PREDICT
    CARD = PREDICT_CARD
    SECONDS = 4.5

    def backdrop(self):
        fresh, fall, plate, sample, red, _ = predict_picture()
        return VGroup(fresh, fall, plate, sample, red)

    def construct(self):
        self.add(tabletop(), self.backdrop(), backed_question(self.QUESTION, **self.CARD))
        track = line((-3.55, -3.50), (3.55, -3.50), PAPER, 11)
        progress = track.copy().set_stroke(COVER, 11)
        self.add(track)
        self.play(Create(progress), run_time=self.SECONDS, rate_func=linear)


class S12RevealClose(SpokenScene):
    def construct(self):
        fresh, fall, plate, sample, red, _ = predict_picture()
        question = backed_question(PREDICT, **PREDICT_CARD)
        self.add(tabletop(), fresh, fall, plate, sample, red, question)
        left = point(-4.04, .31)
        right = point(4.09, .31)
        hidden = leaf(YELLOW, left, 4.82, .18)
        chlorophyll = leaf(GREEN, left, 4.82, .18)
        base = leaf(RED, right, 4.65, -.12, maple=True)
        base[1].set_color("#686F57")
        base[2].set_fill("#A1AC88").set_stroke("#686F57", 2.7)
        base[3].set_color("#D4DBB4")
        base[4].set_color("#D4DBB4")
        newly_red = leaf(RED, right, 4.65, -.12, maple=True)
        keep_strip, _, _ = strip(point(0, .34), height=4.51)
        yellow_label = paper_label(caption("Yellow was hidden\nall summer", size=34, color=INK)).move_to(point(-4.04, -3.02))
        red_label = paper_label(caption("Most red is made\nin fall", size=34, color=INK)).move_to(point(4.08, -3.02))
        self.at("usually no")
        answer = backed_question("Usually, no.", **PREDICT_CARD)
        self.play(swap(question, answer), red.animate.rotate(-.15), run_time=.95)
        self.at("makes a great follow")
        self.play(FadeOut(plate), FadeOut(fall), Transform(sample, keep_strip),
                  Transform(fresh, chlorophyll), Transform(red, base), run_time=1.98)
        self.at("yellow pigments sit")
        self.play(FadeOut(answer), fresh.animate.shift(UP * .35 + LEFT * .43), run_time=.72)
        self.add(hidden)
        self.bring_to_front(fresh)
        self.play(fresh.animate.shift(DOWN * .35 + RIGHT * .43), run_time=1.75)
        self.at("green chlorophyll fades")
        self.play(FadeOut(fresh), run_time=1.69)
        self.play(FadeIn(yellow_label), run_time=.50)
        self.at("most reds are made new")
        sugars = VGroup(*[Dot(point(4.10 + x, .52 + y), radius=.09 + .012 * (i % 3),
                              color=GOLD, stroke_width=1.8, stroke_color=INK)
                          for i, (x, y) in enumerate([(-.27, .45), (.39, .16), (-.65, -.12),
                                                       (.07, -.21), (.64, -.37), (-.36, -.63)])])
        self.play(LaggedStart(*(GrowFromCenter(d) for d in sugars), lag_ratio=.17), run_time=1.73)
        self.at("from trapped sugars")
        self.play(Transform(red, newly_red), sugars.animate.set_color(RED).scale(.74), run_time=1.47)
        self.at("two ways fall colors appear")
        self.play(FadeOut(sugars), FadeIn(red_label), run_time=.88)
        self.finish()


class S13End(EndCard):
    LINE = "Green leaves hide yellow all summer; fall just uncovers it."
