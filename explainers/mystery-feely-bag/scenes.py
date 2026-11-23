"""Word-synced illustrations for The Mystery Feely Bag."""
from bp_parts import *

# COLOR MAP — reference template: teal for the activity, gold for setup,
# green for observations, red for safety. Orange peel is orange, metal is
# silver-blue, wood is amber, and the pillowcase is unbleached cotton.
WOOD = "#A7603C"
WOOD_LIGHT = "#C98956"
TABLE = "#754632"
TABLE_EDGE = "#4A2B25"
CLOTH = "#D9B999"
CLOTH_LIGHT = "#F3D7B4"
SEAM = "#9D7058"
OPENING = "#403136"
SKIN = "#EAA47F"
SKIN_EDGE = "#A95E54"
PEEL = "#F59A38"
PEEL_DARK = "#C86228"
METAL = "#AED0DE"
WARMTH = "#FFCB6D"
PAPER = "#FFF0D7"
BAG_X = -2.75
BAG_MOUTH = np.array([BAG_X, 0.56, 0])
ORANGE_AT = np.array([BAG_X, -0.86, 0])
SPOON_X = (-3.64, -1.86)
QUESTION = "Which will feel colder?"
QUESTION_STYLE = dict(y=2.48, size=45, color=WARMTH)
CARD_X = (-4.95, -2.48, 0, 2.48, 4.95)


def pt(x, y):
    return np.array([x, y, 0])


def shape(start, segments, fill, edge=None, width=2.5):
    path = VMobject()
    path.start_new_path(pt(*start))
    for segment in segments:
        if len(segment) == 2:
            path.add_line_to(pt(*segment))
        else:
            path.add_cubic_bezier_curve_to(*(pt(*segment[i:i + 2]) for i in (0, 2, 4)))
    path.close_path()
    return path.set_fill(fill, 1).set_stroke(edge or fill, width)


def pill(w, h, color, x=0, y=0, edge=None, radius=0.12):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            fill_color=color, fill_opacity=1,
                            stroke_color=edge or color, stroke_width=2).move_to(pt(x, y))


def oval(w, h, color, x=0, y=0, edge=None):
    return Ellipse(width=w, height=h, fill_color=color, fill_opacity=1,
                   stroke_color=edge or color, stroke_width=2).move_to(pt(x, y))


def stroke(points, color, width=3):
    return VMobject().set_points_as_corners([pt(*p) for p in points]).set_stroke(color, width)


def table():
    top = shape((-6.72, -2.45), [(-5.74, 1.8), (5.74, 1.8), (6.72, -2.45)], TABLE, WOOD_LIGHT)
    apron = pill(13.44, 1.21, TABLE_EDGE, 0, -3.03, radius=0.12)
    lip = Line(pt(-6.65, -2.46), pt(6.65, -2.46), color=WOOD_LIGHT, stroke_width=10)
    grain = VGroup(*(Line(pt(-5.1 + inset, y), pt(5.1 - inset, y),
                           stroke_width=0.7, color="#986046")
                     for inset, y in [(0.7, 1.45), (0.3, 0.45), (0, -0.55), (-0.4, -1.55)]))
    inlay = Line(pt(-6.40, -3.38), pt(6.40, -3.38), color="#815039", stroke_width=1.8)
    return VGroup(apron, inlay, top, grain, lip)


def bag(open_view=False):
    """The same pillowcase silhouette and mouth in both views."""
    shadow = oval(5.52, 0.54, OPENING, BAG_X, -2.10)
    cloth = shape((-1.76, 0.58), [
        (-2.35, 0.29, -2.22, -0.14, -2.55, -0.46),
        (-2.98, -0.97, -2.68, -1.85, -2.09, -2.00),
        (-1.23, -2.34, 1.48, -2.31, 2.19, -1.91),
        (2.85, -1.63, 2.75, -0.69, 2.34, -0.28),
        (2.11, -0.04, 2.25, 0.41, 1.75, 0.60),
        (0.76, 0.90, -0.92, 0.85, -1.76, 0.58)
    ], SEAM if open_view else CLOTH, CLOTH_LIGHT).shift(RIGHT * BAG_X)
    bottom_seam = shape((-2.34, -1.7), [
        (-1.45, -2.01, 1.62, -2.02, 2.39, -1.62),
        (2.16, -2.41, -1.95, -2.36, -2.34, -1.7)
    ], "#A47760" if open_view else "#BF9879", width=0).shift(RIGHT * BAG_X)
    cutaway = oval(4.52, 2.12, "#704E48", BAG_X, -0.83, "#B3826A")
    lump = shape((-2.31, -1.34), [
        (-1.85, -0.47, -1.53, -0.29, -1.06, -0.54),
        (-0.50, -0.91, -0.62, -0.86, -0.13, -0.55),
        (0.41, -0.21, 1.28, -0.22, 1.71, -0.76),
        (1.91, -0.98, 2.14, -1.03, 2.36, -1.42),
        (1.05, -1.66, -1.02, -1.77, -2.31, -1.34)
    ], "#EACAA8", width=0).shift(RIGHT * BAG_X)
    rim = oval(3.68, 0.63, CLOTH_LIGHT, BAG_X, 0.57, SEAM)
    slit = oval(3.29, 0.37, OPENING, BAG_X, 0.60)
    folds = VGroup(*(stroke([a, b, c], SEAM, 1.6).shift(RIGHT * BAG_X)
                     for a, b, c in [((-1.78, 0.22), (-2.01, -0.04), (-2.15, -0.41)),
                                     ((1.80, 0.23), (2.00, -0.06), (2.11, -0.45))]))
    return VGroup(shadow, cloth, bottom_seam, cutaway if open_view else lump, folds, rim, slit)


def hand(size=2.0, color=SKIN):
    """Side-on hand with fingers reaching down and the thumb curled in."""
    h = shape((-0.53, 1.22), [
        (0.54, 1.22), (0.52, 0.49, 0.62, 0.31, 0.93, 0.21),
        (1.22, 0.10, 1.23, -0.28, 0.98, -0.34),
        (0.75, -0.40, 0.62, -0.20, 0.43, -0.15),
        (0.36, -0.58, 0.31, -0.99, 0.12, -1.04),
        (-0.06, -1.17, -0.16, -0.99, -0.12, -0.80),
        (-0.21, -1.20, -0.47, -1.14, -0.48, -0.91),
        (-0.56, -1.06, -0.78, -1.00, -0.75, -0.78),
        (-0.96, -0.86, -1.02, -0.69, -0.95, -0.47),
        (-0.86, 0.08, -0.54, 0.28, -0.53, 1.22)
    ], color, SKIN_EDGE, 3)
    crease = ArcBetweenPoints(pt(-0.58, -0.22), pt(0.21, 0.08), angle=-0.65)
    crease.set_stroke(SKIN_EDGE, 2.3)
    return VGroup(h, crease).set_height(size)


def orange(size=1.4):
    fruit = Circle(radius=0.70, fill_color=PEEL, fill_opacity=1, stroke_color=PEEL_DARK, stroke_width=3)
    light = oval(0.70, 0.27, "#FFB653", -0.19, 0.31).rotate(0.45)
    pores = VGroup(*(Dot(pt(r * np.cos(a), r * np.sin(a)), radius=0.024, color=PEEL_DARK)
                    for r, a in [(0.42, 0.33), (0.49, 1.22), (0.22, 1.1), (0.46, 2.45),
                                 (0.53, 3.28), (0.37, 4.02), (0.54, 4.71),
                                 (0.49, 5.60), (0.28, 5.06), (0.21, 0.12)]))
    navel = oval(0.16, 0.09, "#805934", -0.04, 0.61)
    return VGroup(fruit, light, pores, navel).set_height(size)


def pinecone():
    core = oval(1.38, 1.91, "#814A32", edge="#553637")
    scales = VGroup(*(oval(0.47, 0.26, WOOD_LIGHT, x, y, "#633A2B").rotate(tilt)
                     for y, row in [(-0.65, [-0.20, 0.20]), (-0.36, [-0.39, 0, 0.39]),
                                    (-0.08, [-0.43, 0, 0.43]), (0.20, [-0.35, 0, 0.35]),
                                    (0.47, [-0.22, 0.22]), (0.71, [0])]
                     for x in row for tilt in [x * -1.1]))
    return VGroup(core, scales)


def stone():
    body = shape((-1, -0.34), [(-1.14, 0.34, -0.47, 0.69, 0.03, 0.61),
                               (0.65, 0.56, 1.15, 0.34, 1.03, -0.21),
                               (0.76, -0.62, -0.69, -0.65, -1, -0.34)], "#89959F", METAL)
    gleam = oval(0.91, 0.14, "#B2BCC2", -0.25, 0.32).rotate(0.18)
    return VGroup(body, gleam)


def sponge():
    body = pill(1.95, 1.10, "#E5B849", edge="#FFF0A1", radius=0.18)
    pores = VGroup(*(Dot(pt(x, y), radius=r, color="#AB762D")
                    for x, y, r in [(-0.64, 0.24, 0.07), (-0.26, 0.10, 0.042), (0.31, 0.23, 0.075),
                                    (0.69, 0.06, 0.045), (-0.68, -0.17, 0.04), (0, -0.24, 0.07),
                                    (0.44, -0.26, 0.05)]))
    return VGroup(body, pores)


def mitten():
    cuff = pill(0.90, 0.44, "#844D66", 0.1, -0.83, edge="#EFADC1")
    body = shape((-0.35, -0.73), [(-0.57, -0.32, -0.99, -0.03, -0.87, 0.30),
                                  (-0.75, 0.59, -0.48, 0.39, -0.35, 0.20),
                                  (-0.38, 0.68, -0.22, 1.00, 0.15, 0.98),
                                  (0.58, 0.98, 0.67, 0.68, 0.64, 0.17),
                                  (0.62, -0.18, 0.60, -0.46, 0.53, -0.73)], "#BA7188", "#EFADC1")
    knit = VGroup(*(stroke([(x - 0.07, y + 0.06), (x, y), (x + 0.07, y + 0.06)], "#E69BB0", 2)
                    for x in [-0.15, 0.15, 0.40] for y in [-0.43, -0.16, 0.12, 0.37, 0.60]))
    return VGroup(cuff, body, knit)


def block():
    face = pill(1.42, 1.02, WOOD_LIGHT, edge="#E6AA6C")
    top = Polygon(pt(-0.71, 0.48), pt(-0.42, 0.76), pt(0.93, 0.76), pt(0.71, 0.48),
                  fill_color="#E6AA6C", fill_opacity=1, stroke_width=0)
    side = Polygon(pt(0.70, 0.49), pt(0.93, 0.76), pt(0.93, -0.23), pt(0.70, -0.51),
                   fill_color=WOOD, fill_opacity=1, stroke_width=0)
    return VGroup(face, top, side)


def spoon(wood=False, height=2.15):
    color, edge = (WOOD_LIGHT, "#77462E") if wood else (METAL, "#658097")
    shaft = pill(0.22, 1.66, color, 0, -0.26, edge, 0.09)
    bowl = oval(0.70, 0.94, color, 0, 0.61, edge)
    sheen = ArcBetweenPoints(pt(-0.10, 0.90), pt(-0.19, 0.46), angle=0.65)
    sheen.set_stroke("#EAC390" if wood else "#E8F8FF", 3)
    return VGroup(shaft, bowl, sheen).set_height(height)


def spoon_pair():
    return VGroup(spoon(height=1.83).move_to(pt(SPOON_X[0], -0.71)),
                  spoon(wood=True, height=1.83).move_to(pt(SPOON_X[1], -0.71)))


def eye(closed=False):
    if closed:
        lid = ArcBetweenPoints(pt(-0.53, 0.10), pt(0.53, 0.10), angle=1.05)
        lashes = VGroup(*(Line(pt(x, -0.06), pt(x + 0.08, -0.24), stroke_width=3)
                           for x in [-0.32, -0.04, 0.25]))
        return VGroup(lid, lashes).set_color(TEAL).set_stroke(width=4)
    white = shape((-0.64, 0), [( -0.27, 0.50, 0.27, 0.50, 0.64, 0),
                              (0.27, -0.50, -0.27, -0.50, -0.64, 0)], PAPER, TEAL)
    return VGroup(white, Dot(radius=0.23, color=TEAL), Dot(radius=0.11, color=OPENING),
                  Dot(pt(-0.06, 0.08), radius=0.046, color=WHITE))


def senses(which):
    if which == "Eyes":
        return eye()
    if which == "Skin":
        return hand(0.92).rotate(-0.43)
    if which == "Ears":
        curves = VGroup(ArcBetweenPoints(pt(-0.33, 0.17), pt(0.10, -0.41), angle=-4.2),
                        ArcBetweenPoints(pt(-0.12, 0.18), pt(0.15, -0.13), angle=-3.1))
        return curves.set_stroke(SKIN, 6)
    if which == "Nose":
        return stroke([(-0.18, 0.42), (-0.25, -0.08), (-0.41, -0.20),
                       (-0.2, -0.33), (0.21, -0.33), (0.40, -0.13), (0.16, -0.08)], SKIN, 6)
    mouth = oval(0.97, 0.59, OPENING, edge=SKIN)
    tongue = oval(0.50, 0.52, "#EA8090", 0, -0.17)
    return VGroup(mouth, tongue, Line(pt(0, -0.09), pt(0, -0.29), color=SKIN_EDGE))


def contrast_chip(word, color, size):
    label = chip(word, color, size)
    label[0].set_fill(TABLE_EDGE, 1)
    label[1].set_color(PAPER)
    return label


def stage_word(word, x, y, color=TEXT, size=34):
    return T(word, size, color, weight=BOLD).move_to(pt(x, y))


def compare_column(kind):
    is_hand = kind == "Skin"
    x = 1.25 if is_hand else 4.45
    color = GOLD if is_hand else TEAL
    icon = senses(kind).move_to(pt(x, 1.15))
    return VGroup(icon, contrast_chip(kind, color, 30).move_to(pt(x, 0.13)))


def observation(kind, text, y=-0.87):
    return stage_word(text, 1.25 if kind == "Skin" else 4.45, y,
                      GOLD if kind == "Skin" else TEAL, 31)


def word_note(text, y):
    return stage_word(text, 3.13, y, "#543528", 33)


def notes():
    page = pill(4.18, 3.58, PAPER, 3.13, -0.08, edge="#CE9D71")
    binding = VGroup(*(oval(0.19, 0.09, WOOD, x, 1.54)
                       for x in [1.55, 2.08, 2.61, 3.14, 3.67, 4.2, 4.73]))
    return VGroup(page, binding)


def pencil():
    shaft = pill(0.16, 0.93, GOLD, edge="#926239", radius=0.04)
    tip = Polygon(pt(-0.08, -0.45), pt(0.08, -0.45), pt(0, -0.68),
                  fill_color=OPENING, fill_opacity=1, stroke_width=0)
    return VGroup(shaft, tip).rotate(-0.44)


def thermometer():
    rail = pill(0.34, 2.22, PAPER, 2.92, 0.37, edge=METAL, radius=0.16)
    fluid = pill(0.12, 1.25, TEAL, 2.92, -0.01, radius=0.05)
    bulb = Dot(pt(2.92, -0.68), color=TEAL, radius=0.23)
    ticks = VGroup(*(Line(pt(3.19, y), pt(3.42, y), color=METAL, stroke_width=2)
                     for y in [-0.45, -0.03, 0.39, 0.81, 1.23]))
    return VGroup(rail, fluid, bulb, ticks)


def prediction_world():
    return VGroup(table(), bag(True), spoon_pair())


def temperature_tag():
    return VGroup(stage_word("Same room temperature", 2.99, -1.66, TEXT, 30),
                  scope_tag(size=24, color=TEXT).move_to(pt(3.0, -2.98)))


def fridge():
    housing = pill(0.84, 1.15, METAL, edge="#638799")
    rule = Line(pt(-0.41, 0.13), pt(0.41, 0.13), color="#638799", stroke_width=2)
    handles = VGroup(*(Line(pt(-0.26, y), pt(-0.26, y - 0.16), color="#466276", stroke_width=3)
                       for y in [0.43, -0.02]))
    return VGroup(housing, rule, handles)


def cross(size=0.5):
    return VGroup(Line(UL, DR), Line(DL, UR)).set_stroke(RED, 8).set_height(size)


def tube():
    sleeve = pill(2.42, 1.45, "#C19371", 3.02, -0.51, edge="#F2C29C", radius=0.26)
    opening = oval(0.53, 1.43, OPENING, 1.82, -0.51, "#E3B086")
    fiber = Line(pt(2.23, -0.97), pt(3.78, -0.97), color="#E3B086", stroke_width=2)
    return VGroup(sleeve, opening, fiber)


def marble():
    return VGroup(Dot(radius=0.22, color=TEAL), Dot(pt(-0.07, 0.08), radius=0.06, color=PAPER))


def people():
    def person(height, color):
        face = Dot(pt(0, 0.63), radius=0.39, color=SKIN)
        shirt = pill(1.10, 1.05, color, 0, -0.29, radius=0.24)
        fringe = Arc(radius=0.35, start_angle=0.47, angle=2.16, arc_center=face.get_center())
        fringe.set_stroke(TABLE_EDGE, 10)
        return VGroup(shirt, face, fringe).set_height(height)

    grown = person(2.22, TEAL)
    child = person(1.62, WOOD_LIGHT)
    return VGroup(grown, child).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)


def towel(w=2.84, h=1.72):
    cloth = pill(w, h, PAPER, edge="#D0B394")
    hems = VGroup(*(Line(pt(x, -h / 2 + 0.17), pt(x, h / 2 - 0.17), color="#BA9675", stroke_width=2)
                    for x in [-w / 2 + 0.20, w / 2 - 0.20]))
    return VGroup(cloth, hems)


def heat_arrow(x, y, length):
    return Arrow(pt(x, y), pt(x, y - length), buff=0, color=WARMTH, stroke_width=6,
                 max_tip_length_to_length_ratio=0.27)


def feather():
    vane = shape((0, -0.68), [(-0.48, -0.31, -0.59, 0.48, 0.13, 1.04),
                               (0.53, 0.55, 0.51, 0.08, 0.09, -0.51), (0, -0.68)], "#68BAB4", "#B3E9DE")
    shaft = stroke([(-0.14, -1.05), (0, -0.47), (0.15, 0.85)], PAPER)
    barbs = VGroup(*(stroke([(-0.33 + 0.07 * i, y + 0.19), (0.01 + 0.028 * i, y - 0.04),
                             (0.33 - 0.015 * i, y + 0.26)], "#C5E8DC", 1.8)
                    for i, y in enumerate([-0.37, -0.16, 0.05, 0.26, 0.45])))
    return VGroup(vane, barbs, shaft)


def touch_site(site):
    if site in ("Fingertip", "Back of hand"):
        return hand(2.72).rotate(0.41 if site == "Fingertip" else -0.62)
    if site == "Elbow":
        return shape((-1.24, 1.09), [
            (-1.25, 1.51, -0.57, 1.70, -0.36, 1.32),
            (0.05, 0.18), (1.17, 0.55), (1.54, 0.66, 1.70, -0.02, 1.37, -0.15),
            (0.08, -0.82), (-0.31, -0.98, -0.61, -0.79, -0.76, -0.41)
        ], SKIN, SKIN_EDGE, 3)
    foot = oval(1.12, 2.11, SKIN, edge=SKIN_EDGE).rotate(-0.28)
    toes = VGroup(*(Dot(pt(x, y), radius=r, color=SKIN)
                    for x, y, r in [(-0.52, 0.80, 0.20), (-0.25, 0.97, 0.16),
                                    (-0.01, 1.05, 0.14), (0.20, 1.07, 0.12), (0.38, 1.03, 0.10)]))
    return VGroup(foot, toes)


def sense_tile(name, x):
    icon = senses(name).move_to(pt(x, 0.77))
    label = boxed_label(name, TEAL, size=29, pad=0.19, box=(1.90, 0.63), min_size=28)
    label.box.set_fill(TABLE_EDGE, 1)
    label.label.set_color(PAPER)
    label.move_to(pt(x, -0.18))
    return VGroup(icon, label)


def safety_icon(icon, label, x, color=TEXT):
    icon.move_to(pt(x, 0.60))
    return VGroup(icon, stage_word(label, x, -1.29, color, 31))


class S01Hook(SpokenScene):
    def construct(self):
        pouch = bag()
        reach = hand(2.55).move_to(pt(BAG_X, 2.25))
        self.add(table(), pouch)
        self.at("can you tell")
        self.play(FadeIn(reach), run_time=0.36)
        # Keep the near lip in front as the fingers pass behind it.
        front = shape((-1.68, 0.58), [
            (-1.68, 0.34, -0.82, 0.37, 0, 0.39),
            (0.82, 0.37, 1.68, 0.34, 1.68, 0.58),
            (1.43, -0.33), (-1.43, -0.33)
        ], CLOTH, width=0).shift(RIGHT * BAG_X)
        near_lip = ArcBetweenPoints(pt(BAG_X - 1.68, 0.59), pt(BAG_X + 1.68, 0.59), angle=0.53)
        near_lip.set_stroke(CLOTH_LIGHT, 6)
        front_lip = VGroup(front, near_lip)
        self.add(front_lip)
        mystery = T("What is it?", 60, PAPER, font=TITLE_FONT).move_to(pt(2.71, 2.39))
        self.play(reach.animate.shift(DOWN * 0.64), FadeIn(mystery), run_time=1.32)
        self.at("a pillowcase")
        self.play(reach.animate.shift(DOWN * 0.58).rotate(-0.11), run_time=1.7)
        self.at("let your child")
        self.play(reach.animate.shift(UP * 0.14).rotate(0.15), run_time=1.62, rate_func=there_and_back)
        self.play(FadeOut(reach), FadeOut(front_lip), FadeOut(mystery), run_time=0.55)
        self.finish()


class S02Title(TitleCard):
    TITLE = "The Mystery Feely Bag: Parent Guide"
    LESSON = "The Mystery Feely Bag"

    def construct(self):
        pouch = bag()
        title = fit_text(self.TITLE, max_w=12.15, size=49, min_size=35,
                         font=TITLE_FONT, color=PAPER).move_to(pt(-0.37, 2.66))
        self.add(table(), bob(pouch[3], amp=0.08, speed=3.6), pouch)
        self.play(FadeIn(title, shift=UP * 0.12), run_time=0.54)
        self.wait(max(0.05, self.narration_s - self.elapsed() - 0.35))
        self.play(FadeOut(title), run_time=0.35)


class S03Payoff(SpokenScene):
    def construct(self):
        pouch = bag()
        closed = eye(True).scale(1.26).move_to(pt(2.99, 0.71))
        self.add(table(), pouch)
        self.at("the bag takes sight away")
        self.play(FadeIn(closed), run_time=0.65)
        self.at("so touch")
        reaching = hand(1.83).move_to(pt(BAG_X, 1.69))
        self.play(FadeOut(closed), FadeIn(reaching, shift=UP * 0.21), run_time=0.65)
        self.play(reaching.animate.shift(DOWN * 0.22), run_time=1.45)
        bob(reaching, amp=0.10, speed=3.5)
        for cue, word, y, color in [
            ("describing what they feel", "Describe", 1.06, GOLD),
            ("making a guess", "Guess", 0.06, PAPER),
            ("checking it", "Check", -0.94, TEAL),
        ]:
            self.at(cue)
            self.play(FadeIn(contrast_chip(word, color, 35).move_to(pt(2.95, y)), shift=LEFT * 0.25), run_time=0.55)
        self.at("it takes about")
        clock = Circle(radius=0.30, color=GOLD, stroke_width=4).move_to(pt(1.72, -2.91))
        hands = stroke([(1.72, -2.72), (1.72, -2.91), (1.84, -2.96)], GOLD, 4)
        self.play(Create(clock), Create(hands), FadeIn(stage_word("25 minutes", 3.25, -2.91, PAPER, 31)), run_time=0.66)
        self.finish()


class S04Gather(SpokenScene):
    def construct(self):
        pouch = bag()
        self.add(table(), pouch)
        self.at("eight to ten objects")
        count = stage_word("8–10 objects", 2.97, 2.53, PAPER, 39)
        self.play(FadeIn(count), run_time=0.6)
        bob(pouch[3], amp=0.12, speed=3.3)
        objects = [
            ("a pinecone", pinecone().move_to(pt(0.72, 0.98))),
            ("large smooth stone", stone().scale(0.79).move_to(pt(2.67, 0.99))),
            ("new sponge", sponge().scale(0.82).move_to(pt(4.77, 0.99))),
            ("wool mitten", mitten().scale(0.74).move_to(pt(0.70, -1.14))),
            ("an orange", orange(1.33).move_to(pt(2.67, -1.14))),
        ]
        for cue, obj in objects:
            self.at(cue)
            self.play(FadeIn(obj, shift=UP * 0.24), run_time=0.50)
        wood_block = block().scale(0.79).move_to(pt(4.76, -1.16))
        self.play(FadeIn(wood_block, shift=UP * 0.19), run_time=0.44)
        self.at("keep a metal spoon")
        self.play(FadeOut(VGroup(count, *(obj for _, obj in objects), wood_block)), run_time=0.38)
        metal = spoon().move_to(pt(0.85, 0.04))
        wooden = spoon(wood=True).move_to(pt(2.58, 0.04))
        chilled = spoon().move_to(pt(4.34, 0.04))
        self.play(FadeIn(metal, shift=LEFT * 0.61), run_time=0.55)
        self.at("a wooden spoon")
        self.play(FadeIn(wooden, shift=LEFT * 0.61), run_time=0.57)
        self.at("a spoon from the fridge")
        self.play(FadeIn(chilled, shift=LEFT * 0.61), FadeIn(fridge().move_to(pt(5.55, -0.32))), run_time=0.73)
        self.finish()


class S05TubeCheck(SpokenScene):
    def construct(self):
        pouch = bag()
        grown_child = people().move_to(pt(3.05, 0.14))
        self.add(table(), pouch, grown_child)
        self.at("stay with your child")
        self.play(grown_child.animate.shift(LEFT * 0.22), run_time=1.55)
        self.at("pack and check")
        tester = tube()
        sponge_check = sponge().rotate(PI / 2).move_to(pt(0.58, -0.52))
        helper = hand(1.54).move_to(pt(0.57, 0.86))
        self.play(FadeOut(grown_child), FadeIn(tester), FadeIn(sponge_check), FadeIn(helper), run_time=0.63)
        self.at("even when squeezed")
        self.play(sponge_check.animate.stretch(0.82, 1).shift(RIGHT * 0.50),
                  helper.animate.shift(RIGHT * 0.48 + DOWN * 0.27), run_time=1.12)
        wool = mitten().move_to(pt(0.57, -0.55))
        self.play(FadeOut(sponge_check), FadeIn(wool, shift=RIGHT * 0.14), run_time=0.44)
        self.at("too big for")
        self.play(wool.animate.stretch(0.84, 1).shift(RIGHT * 0.37),
                  helper.animate.shift(DOWN * 0.15), run_time=0.85)
        marble_check = marble().move_to(pt(0.85, -0.50))
        self.play(FadeOut(wool), FadeOut(helper), FadeIn(marble_check), run_time=0.28)
        self.play(marble_check.animate.move_to(pt(1.82, -0.51)), run_time=0.37)
        self.remove(marble_check)
        marble_check.move_to(pt(4.39, -0.56))
        reject = cross(0.76).move_to(pt(4.45, -0.61))
        self.play(FadeIn(marble_check, shift=RIGHT * 0.12), FadeIn(reject), run_time=0.42)
        self.at("skip anything sharp")
        cone = pinecone().scale(1.16).move_to(pt(2.94, -0.30))
        checker = hand(2.02).rotate(0.54).move_to(pt(4.38, 0.87))
        self.play(FadeOut(VGroup(tester, marble_check, reject)), FadeIn(cone), FadeIn(checker), run_time=0.61)
        self.play(checker.animate.shift(LEFT * 0.54 + DOWN * 0.33).rotate(-0.16), run_time=2.65)
        self.at("loose parts")
        self.play(checker.animate.shift(DOWN * 0.40).rotate(0.20), run_time=1.39)
        self.at("keep all bag objects")
        self.play(cone.animate.move_to(BAG_MOUTH + UP * 0.44),
                  checker.animate.shift(LEFT * 4.58 + UP * 0.83), run_time=0.96)
        mouths = stage_word("Keep objects out of mouths", 2.80, 2.48, PAPER, 34)
        self.play(FadeOut(cone, shift=DOWN * 0.43), FadeOut(checker, shift=UP * 0.25),
                  FadeIn(mouths), run_time=0.61)
        self.finish()


class S06Describe(SpokenScene):
    def construct(self):
        pouch = bag(True)
        fruit = orange().move_to(ORANGE_AT)
        reach = hand(2.65).rotate(-0.26).move_to(pt(BAG_X - 0.42, 0.92))
        self.add(table(), pouch, fruit)
        self.at("your child puts one hand")
        self.play(FadeIn(reach, shift=UP * 0.22), run_time=0.53)
        self.play(reach.animate.shift(DOWN * 0.54 + RIGHT * 0.21).rotate(0.18), run_time=1.68)
        self.at("holds one object")
        self.play(reach.animate.shift(DOWN * 0.25).rotate(-0.11), run_time=1.11)
        self.at("don't tell me")
        page = notes()
        self.play(FadeIn(page, shift=LEFT * 0.34), run_time=1.03)
        self.at("tell me what it feels")
        self.play(reach.animate.rotate(0.17, about_point=ORANGE_AT),
                  fruit.animate.rotate(0.21), rate_func=there_and_back, run_time=1.39)
        words = [("bumpy", 0.82), ("hard", 0.03), ("light", -0.75)]
        cards = []
        for word, y in words:
            self.at(word)
            card = chip(word, GOLD, 30, pad=0.15).move_to(pt(3.13, y))
            card[0].set_fill(TABLE_EDGE, 1)
            cards.append(card)
            self.play(FadeIn(card, shift=LEFT * 0.16), run_time=0.28)
        self.at("write them down")
        pen = pencil().move_to(pt(4.66, 0.86))
        for i, ((word, y), card) in enumerate(zip(words, cards)):
            pen_at = pt(4.48, y + 0.35)
            movement = FadeIn(pen.move_to(pen_at)) if i == 0 else pen.animate.move_to(pen_at)
            self.play(swap(card, word_note(word, y), run_time=0.34), movement, run_time=0.34)
        self.play(FadeOut(pen), run_time=0.22)
        self.finish()


class S07GuessLook(SpokenScene):
    def construct(self):
        pouch = bag(True)
        fruit = orange().move_to(ORANGE_AT)
        reach = hand(2.65).rotate(-0.19).move_to(pt(BAG_X - 0.21, 0.13))
        page = VGroup(notes(), *(word_note(word, y) for word, y in
                                 [("bumpy", 0.82), ("hard", 0.03), ("light", -0.75)]))
        self.add(table(), pouch, fruit, reach, page)
        self.at("have your child guess")
        self.play(reach.animate.rotate(0.08), run_time=1.08, rate_func=there_and_back)
        self.at("then pull out")
        self.play(fruit.animate.move_to(pt(BAG_X, 1.89)).scale(1.21),
                  reach.animate.shift(UP * 2.03), run_time=1.30)
        self.play(FadeOut(reach), Transform(pouch, bag()), run_time=0.58)
        self.at("compare what they felt")
        self.play(FadeOut(page), fruit.animate.move_to(pt(BAG_X, 0.98)).scale(1.20), run_time=0.71)
        skin = compare_column("Skin")
        eyes = compare_column("Eyes")
        self.play(FadeIn(skin[0]), run_time=0.48)
        self.play(FadeIn(eyes[0]), run_time=0.48)
        self.at("their hand could feel")
        self.play(FadeIn(skin[1]), run_time=0.52)
        self.at("the shape and bumps")
        self.play(fruit.animate.rotate(0.31), FadeIn(observation("Skin", "shape")),
                  FadeIn(observation("Skin", "bumpy", -1.49)), run_time=0.92)
        self.at("their eyes can see")
        self.play(FadeIn(eyes[1]), FadeIn(observation("Eyes", "color")), run_time=0.38)
        self.finish()


class S08Spoons(SpokenScene):
    def construct(self):
        pouch = bag()
        self.add(table(), pouch)
        left, right = spoon_pair()
        left_start = pt(SPOON_X[0], 1.86)
        right_start = pt(SPOON_X[1], 1.86)
        self.at("put the metal spoon")
        shown_left = left.copy().move_to(left_start)
        self.play(FadeIn(shown_left), run_time=0.55)
        self.at("the wooden spoon")
        shown_right = right.copy().move_to(right_start)
        self.play(FadeIn(shown_right), run_time=0.48)
        self.at("in the bag")
        self.play(Transform(pouch, bag(True)), shown_left.animate.move_to(left),
                  shown_right.animate.move_to(right), run_time=1.12)
        self.at("they have been")
        self.play(FadeIn(thermometer(), shift=UP * 0.47), run_time=0.69)
        self.at("the same room")
        self.play(FadeIn(temperature_tag()), run_time=0.55)
        self.play(shown_left.animate.shift(LEFT * 0.32), shown_right.animate.shift(RIGHT * 0.32),
                  rate_func=there_and_back, run_time=1.02)
        self.finish()


class S09PredictQ(SpokenScene):
    def construct(self):
        meter = VGroup(thermometer(), temperature_tag())
        world = prediction_world()
        self.add(world, meter)
        self.at("both spoons are")
        self.play(Indicate(meter[0][2], color=METAL, scale_factor=1.16), run_time=1.55)
        self.at("what do you predict")
        self.play(FadeOut(meter), run_time=0.48)
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.play(FadeIn(question), run_time=0.60)
        self.at("your child feels both")
        # Both handles move by the same amount, so neither spoon is favored.
        self.play(world[2].animate.shift(UP * 0.53), rate_func=there_and_back, run_time=1.65)
        self.at("will one feel colder")
        self.play(world[2][0].animate.shift(LEFT * 0.40), world[2][1].animate.shift(RIGHT * 0.40),
                  rate_func=there_and_back, run_time=1.73)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE

    def construct(self):
        # The locked audio gives this hold 4.5 seconds. Preserve the final question frame.
        world = prediction_world()
        bob(world[1], amp=0.19, speed=2 * TAU / self.narration_s)
        self.add(world, question_card(self.QUESTION, **self.CARD))
        self.wait(self.narration_s)


class S11Reveal(SpokenScene):
    def construct(self):
        world = prediction_world()
        question = question_card(QUESTION, **QUESTION_STYLE)
        self.add(world, question)
        self.at("the metal spoon")
        left = hand(1.80).move_to(pt(SPOON_X[0] - 0.20, 1.31))
        right = hand(1.80).move_to(pt(SPOON_X[1] + 0.20, 1.31))
        self.play(FadeOut(question), FadeIn(left), run_time=0.50)
        self.play(FadeIn(right), left.animate.shift(DOWN * 0.25), run_time=0.46)
        self.play(right.animate.shift(DOWN * 0.25), run_time=0.50)
        self.at("feels colder")
        answer = stage_word("Metal usually feels colder", 2.97, 2.48, METAL, 36)
        self.play(FadeIn(answer), run_time=0.55)
        self.at("draws heat from fingers")
        metal_heat = heat_arrow(SPOON_X[0] + 0.41, 0.35, 1.55)
        wood_heat = heat_arrow(SPOON_X[1] + 0.41, 0.35, 0.67)
        explanation = stage_word("Heat leaves fingers faster", 2.96, -0.78, WARMTH, 33)
        self.play(GrowArrow(metal_heat), GrowArrow(wood_heat), FadeIn(explanation), run_time=1.49)
        self.play(metal_heat.animate.shift(DOWN * 0.24), wood_heat.animate.shift(DOWN * 0.09),
                  rate_func=there_and_back, run_time=1.05)
        self.at("dry the fridge spoon")
        pouch, pair = world[1], world[2]
        chilled = spoon(height=2.26).rotate(-0.93).move_to(pt(3.1, 0.52))
        adult = hand(1.60).rotate(-0.73).move_to(pt(4.54, 1.27))
        wiping = towel(1.72, 1.21).move_to(pt(2.72, 0.53))
        self.play(FadeOut(VGroup(left, right, metal_heat, wood_heat, answer, explanation, pair)),
                  Transform(pouch, bag()), FadeIn(chilled), FadeIn(wiping), FadeIn(adult), run_time=0.58)
        self.play(wiping.animate.shift(LEFT * 0.65 + UP * 0.46),
                  adult.animate.shift(LEFT * 0.54), run_time=0.98)
        self.at("hand it over")
        receiver = hand(1.90).rotate(1.76).move_to(pt(0.86, -0.75))
        closed = eye(True).scale(1.20).move_to(pt(4.85, 1.15))
        self.play(FadeOut(wiping), FadeIn(receiver), run_time=0.47)
        self.play(chilled.animate.move_to(pt(2.11, -0.23)).rotate(-0.23),
                  adult.animate.shift(LEFT * 0.81 + DOWN * 0.39),
                  receiver.animate.shift(RIGHT * 0.47), FadeIn(closed), run_time=1.21)
        self.play(FadeOut(adult), run_time=0.40)
        self.at("ask whether")
        wet_question = question_card("Does it feel wet?", y=2.54, size=38, color=WARMTH).shift(RIGHT * 2.60)
        self.play(FadeIn(wet_question), receiver.animate.rotate(0.18),
                  chilled.animate.rotate(0.14), run_time=1.20)
        self.at("wipe the spoon")
        cloth = towel(3.03).move_to(pt(3.11, -0.87))
        self.play(FadeOut(closed), FadeOut(wet_question), FadeIn(cloth), run_time=0.49)
        self.play(chilled.animate.move_to(pt(3.31, -0.33)),
                  receiver.animate.shift(RIGHT * 0.99), run_time=1.23)
        self.at("check the towel")
        self.play(FadeOut(receiver), chilled.animate.move_to(pt(3.33, 0.73)), run_time=0.81)
        self.at("the towel stays dry")
        dry = stage_word("Towel stays dry", 3.13, -2.88, TEXT, 32)
        self.play(FadeIn(dry), cloth.animate.rotate(-0.11), run_time=0.65)
        self.at("the cold may explain")
        dry_note = stage_word("Cold may feel wet", 3.00, 2.44, METAL, 35)
        self.play(FadeIn(dry_note), chilled.animate.rotate(0.25), run_time=1.08)
        self.at("a damp spot")
        damp = stage_word("Towel has a damp spot", 3.13, -2.88, TEXT, 32)
        damp_note = stage_word("Possible condensation", 3.00, 2.44, METAL, 35)
        damp_cloth = VGroup(towel(3.03).move_to(pt(3.11, -0.87)),
                            oval(1.30, 0.46, "#7DAFB7", 3.01, -0.86)).rotate(0.08)
        water = VGroup(*(Dot(pt(x, y), radius=r, color=BLUE) for x, y, r in
                         [(3.35, 0.76, 0.09), (3.57, 0.94, 0.065), (3.42, 1.05, 0.051)]))
        self.play(swap(dry, damp), swap(cloth, damp_cloth), FadeOut(dry_note), FadeIn(water), run_time=0.83)
        self.at("from condensation")
        self.play(FadeIn(damp_note), water.animate.shift(DOWN * 0.22), run_time=0.83)
        self.finish()


class S12FeatherSort(SpokenScene):
    def construct(self):
        pouch = bag()
        self.add(table(), pouch)
        closed = eye(True).scale(1.25).move_to(pt(2.54, 1.08))
        self.at("close their eyes")
        self.play(FadeIn(closed), run_time=0.76)
        feather_model = feather().set_z_index(10)
        brush = feather_model.copy().rotate(1.39).move_to(pt(4.29, 0.29))
        self.at("brush a craft feather")
        self.play(FadeIn(brush, shift=UP * 0.34), run_time=0.66)
        self.play(FadeOut(closed), run_time=0.27)

        wrapped_site = None
        for cue, name, contact, angle, run in [
            ("a fingertip", "Fingertip", (2.46, -1.48), 1.95, 0.66),
            ("the back of the hand", "Back of hand", (1.65, -0.23), 2.85, 0.68),
            ("an elbow", "Elbow", (2.52, -1.20), 1.70, 0.47),
            ("a foot", "Foot", (2.97, -0.15), 1.36, 0.87),
        ]:
            self.at(cue)
            icon = touch_site(name).move_to(pt(2.58, -0.23))
            name_label = stage_word(name, 2.68, 2.49, PAPER, 35)
            new_site = VGroup(icon, name_label)
            if wrapped_site is None:
                self.play(FadeIn(new_site), run_time=0.22)
            else:
                self.play(swap(wrapped_site, new_site, run_time=0.24))
            wrapped_site = new_site
            pose = feather_model.copy().rotate(angle)
            # The end of the first vane curve is the feather tip.
            pose.shift(pt(*contact) - pose[0].get_end_anchors()[0])
            self.play(Transform(brush, pose), run_time=run)

        self.at("ask where they felt")
        best = question_card("Where did you feel it best?", y=2.48, size=37, color=WARMTH).shift(RIGHT * 3.15)
        self.play(swap(wrapped_site[1], best), brush.animate.shift(UP * 0.29 + RIGHT * 0.17), run_time=0.75)
        self.play(brush.animate.rotate(-0.38), run_time=0.67, rate_func=there_and_back)
        self.at("then label five cards")
        self.play(FadeOut(VGroup(best, wrapped_site[0], brush, pouch)), run_time=0.68)
        for cue, name, x in zip(("for eyes", "ears", "nose", "tongue", "skin"),
                                ("Eyes", "Ears", "Nose", "Tongue", "Skin"), CARD_X):
            self.at(cue)
            self.play(FadeIn(sense_tile(name, x), shift=UP * 0.12), run_time=0.29)
        self.at("sort the describing")
        for word, x, y, color in [
            ("color", CARD_X[0], -1.39, TEAL),
            ("bumpy", CARD_X[-1], -1.04, GOLD),
            ("hard", CARD_X[-1], -1.91, GOLD),
        ]:
            item = contrast_chip(word, color, 28).move_to(pt(x, y))
            self.play(FadeIn(item, shift=LEFT * 0.26), run_time=0.45)
        self.finish()


class S13Safety(SpokenScene):
    def construct(self):
        together = safety_icon(people(), "Stay together", -4.10)
        self.add(table())
        self.at("stay with your child")
        self.play(FadeIn(together, shift=LEFT * 0.31), run_time=0.63)
        self.play(together[0].animate.shift(RIGHT * 0.12), run_time=1.39)
        self.at("keep small things")
        items = VGroup(
            marble().scale(1.6),
            oval(0.66, 0.66, GOLD, edge="#F8D88D"),
            VGroup(pill(0.46, 0.79, METAL), pill(0.20, 0.11, METAL, 0, 0.44, radius=0.05)),
        ).arrange(RIGHT, buff=0.25).move_to(pt(0, 0.58))
        for i, cue in enumerate(["marbles", "coins", "batteries"]):
            self.at(cue)
            self.play(FadeIn(items[i], shift=UP * 0.22), run_time=0.66)
        self.at("children under four")
        danger = VGroup(*(cross(0.79).set_stroke(width=5).move_to(item) for item in items))
        warning = T("Under 4:\nchoking risk", 31, PAPER, weight=BOLD, line_spacing=0.78).move_to(pt(0, -1.29))
        self.play(Create(danger), FadeIn(warning), run_time=0.76)
        self.at("call 911")
        screen = pill(0.97, 1.60, "#1B3341", edge=METAL, radius=0.15)
        call = ArcBetweenPoints(pt(-0.21, 0.28), pt(0.25, -0.22), angle=1.1).set_stroke(METAL, 9)
        phone = VGroup(screen, call)
        emergency = safety_icon(phone, "Choking: call 911", 4.13, PAPER)
        self.play(FadeIn(emergency, shift=UP * 0.20), run_time=0.62)
        self.play(phone.animate.rotate(0.19), run_time=1.23, rate_func=there_and_back)
        self.finish()


class S14Safety2(SpokenScene):
    def construct(self):
        self.add(table())
        allergy = stage_word("Check for allergies", -4.08, 2.44, PAPER, 37)
        self.at("check for allergies")
        self.play(FadeIn(allergy), run_time=0.66)
        balloon = oval(0.88, 1.19, "#C77A94", -4.66, 0.63, "#F5B3C8")
        string = stroke([(-4.66, 0.04), (-4.84, -0.26), (-4.65, -0.57)], PAPER, 2.5)
        glove = hand(1.46, GOLD).rotate(PI - 0.25).move_to(pt(-3.41, 0.52))
        self.at("leave out balloons")
        self.play(FadeIn(VGroup(balloon, string), shift=UP * 0.25), run_time=0.64)
        self.at("rubber gloves")
        self.play(FadeIn(glove, shift=UP * 0.25), run_time=0.63)
        self.at("a latex allergy")
        latex = stage_word("Latex allergy?", -4.08, -1.42, PAPER, 32)
        self.play(FadeOut(allergy), FadeIn(latex), Create(cross(1.35).move_to(pt(-4.03, 0.56))), run_time=0.84)
        self.at("use a craft store feather")
        craft = feather().rotate(-0.40)
        tag = pill(0.65, 0.43, PAPER, 0.66, -0.46, edge=WOOD, radius=0.09)
        cord = stroke([(0.04, -0.44), (0.27, -0.62), (0.38, -0.47)], PAPER, 2)
        item = safety_icon(VGroup(craft, cord, tag), "Craft-store feather", 0.0)
        self.play(FadeIn(item, shift=UP * 0.29), run_time=0.84)
        self.at("everyone washes hands")
        hands = VGroup(hand(1.85).rotate(0.84), hand(1.63).rotate(-1.80))
        hands[0].shift(LEFT * 0.37)
        hands[1].shift(RIGHT * 0.41 + DOWN * 0.25)
        bubbles = VGroup(*(Circle(radius=r, color=METAL, stroke_width=3).move_to(pt(x, y))
                           for x, y, r in [(0.05, 0.12, 0.21), (0.44, 0.37, 0.16),
                                          (0.59, 0.03, 0.13), (-0.53, 0.37, 0.18), (0.21, 0.70, 0.16)]))
        washing = safety_icon(VGroup(hands, bubbles), "Wash hands", 4.14)
        self.play(FadeIn(washing, shift=UP * 0.18), run_time=0.53)
        self.play(hands[0].animate.shift(RIGHT * 0.23), hands[1].animate.shift(LEFT * 0.18),
                  bubbles.animate.shift(UP * 0.27), run_time=1.22, rate_func=there_and_back)
        self.finish()


class S15Return(SpokenScene):
    def construct(self):
        pouch = bag()
        fruit = orange(1.69).move_to(pt(BAG_X, 0.98))
        metal, wooden = spoon_pair()
        for item, x, tilt in [(metal, -4.09, -1.18), (wooden, -1.40, 1.07)]:
            item.rotate(tilt).move_to(pt(x, -1.53))
        skin, eyes = compare_column("Skin"), compare_column("Eyes")
        round_word = observation("Skin", "shape")
        bumps = observation("Skin", "bumpy", -1.52)
        peel_color = observation("Eyes", "color")
        self.add(table(), pouch, metal, wooden, fruit, skin, eyes, round_word, bumps, peel_color)
        self.at("what could your hand")
        prompt = hand(1.68).rotate(-0.34).move_to(pt(BAG_X - 0.96, 1.77))
        self.play(FadeIn(prompt), run_time=0.43)
        self.play(prompt.animate.shift(RIGHT * 0.42 + DOWN * 0.26),
                  fruit.animate.rotate(-0.22), run_time=1.42)
        self.at("what could only your eyes")
        self.play(FadeOut(prompt), eyes[0].animate.shift(UP * 0.34).scale(1.36),
                  fruit.animate.shift(UP * 0.26), run_time=0.66)
        self.play(eyes[0].animate.shift(DOWN * 0.34).scale(1 / 1.36),
                  fruit.animate.shift(DOWN * 0.26), run_time=0.75)
        self.at("skin found shape")
        self.play(Indicate(round_word, color=WARMTH, scale_factor=1.08),
                  fruit.animate.rotate(0.27), run_time=0.51)
        self.at("texture")
        texture = observation("Skin", "texture", -1.52)
        self.play(swap(bumps, texture, run_time=0.54), run_time=0.54)
        self.at("and cold")
        self.play(FadeIn(observation("Skin", "cold", -2.08), shift=DOWN * 0.08),
                  skin[0].animate(rate_func=there_and_back).shift(UP * 0.29).scale(1.25),
                  metal.animate.rotate(-0.29), wooden.animate.rotate(0.29), run_time=1.22)
        self.at("eyes found color")
        self.play(Indicate(peel_color, color=PAPER, scale_factor=1.07),
                  fruit.animate.rotate(0.38).shift(UP * 0.27), run_time=0.74)
        self.finish()


class S16End(EndCard):
    LINE = "Touch finds shape, texture and cold, but not color."
