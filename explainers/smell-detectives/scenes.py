"""Smell Detectives, staged around a single schematic kitchen table."""
from bp_parts import *

# Color map: BLUE aroma and water, YELLOW taste and juice, GREEN checks,
# RED safety, GREY foil and faint aromas. Warm neutrals describe the kitchen.
WOOD = "#503B38"
WOOD_EDGE = "#846358"
PAPER = "#F0DEC2"
INK = "#342E3A"
FOIL = "#AAB9CA"
ADULT = "#367580"
CHILD = "#A85853"
SKIN = "#DFA27E"
HAIR = "#49313C"
COFFEE = "#74504B"
ORANGE_PEEL = "#F2A452"
CINNAMON = "#A96B4C"

TABLE_Y = -2.65
CUP_ROW = (-3.9, -1.3, 1.3, 3.9)
JUICE_ROW = (-3.65, -1.35)
PREDICTION = "Can they tell which juice?"


def p(x, y):
    return np.array([x, y, 0.0])


def oval(x, y, width, height, color, opacity=1):
    return Ellipse(width=width, height=height, stroke_width=0,
                   fill_color=color, fill_opacity=opacity).move_to(p(x, y))


def path(*points, color=TEXT, width=4, smooth=True):
    line = VMobject(stroke_color=color, stroke_width=width)
    vertices = [p(*point) for point in points]
    if smooth:
        line.set_points_smoothly(vertices)
    else:
        line.set_points_as_corners(vertices)
    line.set_cap_style(CapStyleType.ROUND)
    return line


def aroma_tip(curve, length, width):
    tip = ArrowTriangleFilledTip(length=length, width=width, color=BLUE,
                                 fill_opacity=1, stroke_width=0)
    tangent = curve.get_end() - curve.points[-2]
    tip.rotate(angle_of_vector(tangent) - tip.tip_angle)
    return tip.shift(curve.get_end() - tip.tip_point)


def table():
    top = Polygon(p(-6.6, -2.80), p(-5.6, -1.25), p(5.6, -1.25), p(6.6, -2.80),
                  fill_color=WOOD, fill_opacity=1, stroke_width=0)
    front = Polygon(p(-6.6, -2.80), p(6.6, -2.80), p(6.6, -3.65), p(-6.6, -3.65),
                    fill_color=WOOD, fill_opacity=1, stroke_width=0)
    rim = path((-6.6, -2.80), (6.6, -2.80), color=WOOD_EDGE, width=3, smooth=False)
    return VGroup(top, front, rim)


def head(x, y, scale=1, *, adult=False, closed=False, stuffy=False):
    hair = oval(0, 0.15, 2.68, 2.52, HAIR)
    ears = VGroup(oval(-1.03, -0.11, 0.44, 0.51, SKIN), oval(1.03, -0.11, 0.44, 0.51, SKIN))
    skin = oval(0, -0.06, 2.17, 2.25, SKIN)
    fringe = oval(-0.25, 0.87, 1.81, 0.62, HAIR).rotate(0.17)
    bun = oval(0.96, 1.02, 0.74, 0.79, HAIR) if adult else VGroup()
    eyes = VGroup(*[
        path((dx - 0.13, 0.16), (dx, 0.10), (dx + 0.13, 0.16), color=INK, width=4)
        if closed else oval(dx, 0.18, 0.135, 0.19, INK)
        for dx in (-0.4, 0.4)
    ])
    nose = oval(0, -0.14, 0.29, 0.19, RED if stuffy else "#BD775C")
    mouth = path((-0.19, -0.42), (0, -0.49), (0.19, -0.42), color=INK, width=3)
    return VGroup(bun, hair, ears, skin, fringe, eyes, nose, mouth).scale(
        scale, about_point=ORIGIN).shift(p(x, y))


def person(x, y, scale=1, *, adult=False, closed=False, stuffy=False):
    shirt = oval(0, -1.48, 3.10, 2.09, ADULT if adult else CHILD)
    neck = oval(0, -0.94, 0.69, 0.90, SKIN)
    body = VGroup(shirt, neck, head(0, 0, adult=adult, closed=closed, stuffy=stuffy))
    return body.scale(scale, about_point=ORIGIN).shift(p(x, y))


def hand(x, y, scale=1, angle=0, fingers=4):
    palm = oval(0, -0.10, 0.66, 0.73, SKIN)
    digits = VGroup(*[oval(dx, 0.23, 0.15, 0.83 - abs(dx), SKIN)
                      for dx in (-0.22, -0.055, 0.11, 0.275)[:fingers]])
    thumb = oval(-0.32, -0.08, 0.22, 0.48, SKIN).rotate(0.52)
    return VGroup(palm, digits, thumb).scale(scale).rotate(angle).move_to(p(x, y))


def pinching_hand(x, y, scale=1):
    """Thumb and forefinger meet across the nose, with the palm to the side."""
    edge = "#915D54"
    palm = oval(0.58, -0.14, 0.66, 0.95, SKIN).rotate(0.67)
    palm.set_stroke(edge, width=2.6)
    fingers = VGroup(
        path((0.66, 0.13), (0.38, 0.36), (0.06, 0.11), color=edge, width=13),
        path((0.62, -0.39), (0.31, -0.35), (-0.06, -0.12), color=edge, width=13),
        path((0.66, 0.13), (0.38, 0.36), (0.06, 0.11), color=SKIN, width=8),
        path((0.62, -0.39), (0.31, -0.35), (-0.06, -0.12), color=SKIN, width=8),
    )
    return VGroup(palm, fingers).scale(scale, about_point=ORIGIN).shift(p(x, y))


def tissue():
    return Polygon(p(2.54, 0.23), p(3.55, 0.35), p(3.91, -0.25), p(3.43, -0.54),
                   p(2.81, -0.43), fill_color=PAPER, fill_opacity=1, stroke_width=0)


def soup(x=-2.55):
    surface = oval(x, -1.18, 3.36, 0.88, PAPER)
    broth = oval(x, -1.13, 2.98, 0.62, ORANGE_PEEL)
    bowl = VMobject(stroke_width=0, fill_color="#62959B", fill_opacity=1)
    bowl.set_points_smoothly([p(x - 1.68, -1.23), p(x - 1.12, -2.14), p(x, -2.47),
                              p(x + 1.12, -2.14), p(x + 1.68, -1.23)])
    bowl.add_line_to(p(x - 1.68, -1.23))
    bowl.close_path()
    lip = path((x - 1.63, -1.24), (x, -1.50), (x + 1.63, -1.24), color=PAPER, width=4)
    return VGroup(bowl, surface, broth, lip)


def ribbon(x, y, dx, dy, color=BLUE, opacity=0.9, seed=0):
    """A moving waft in the diagram, with spatial separation from the lettering."""
    strands = VGroup()
    for i in range(3):
        off = (i - 1) * 0.26
        strand = path((x + off, y - off * 0.2), (x + dx * 0.25 + off + 0.18, y + dy * 0.29),
                      (x + dx * 0.63 + off - 0.13, y + dy * 0.65),
                      (x + dx + off, y + dy), color=color, width=5)
        strand.set_stroke(opacity=opacity)
        strands.add(bob(strand, amp=0.16, speed=2.15, seed=seed + i))
        pulse(strand, base=5.4, amp=2.0, speed=2.6)
    return strands


def cold_world():
    child = person(3.22, 0.70, 1.12, stuffy=True)
    cloud = VGroup(oval(1.96, 0.71, 0.70, 0.45, GREY, 0.48),
                   oval(1.53, 0.85, 0.66, 0.46, GREY, 0.33),
                   oval(1.21, 0.69, 0.43, 0.31, GREY, 0.23))
    return VGroup(child, table(), soup(), tissue(), bob(cloud, amp=0.12),
                  ribbon(-2.65, -0.57, 1.15, 2.35, GREY, 0.62))


def cotton(x, y, scale=1):
    return VGroup(oval(-0.22, -0.02, 0.51, 0.49, TEXT),
                  oval(0.00, 0.12, 0.52, 0.60, TEXT),
                  oval(0.23, -0.01, 0.52, 0.50, TEXT)).scale(scale).move_to(p(x, y))


def aroma_food(kind):
    if kind == "orange":
        return path((-0.53, -0.16), (-0.18, 0.24), (0.25, 0.31), (0.55, 0.12),
                    color=ORANGE_PEEL, width=19)
    if kind == "coffee":
        return VGroup(*[oval(x, y, 0.28, 0.39, COFFEE).rotate(a)
                        for x, y, a in [(-0.32, 0.12, 0.5), (0, 0.24, -0.3),
                                        (0.29, 0.09, 0.6), (0, -0.13, 1.0)]])
    if kind == "cinnamon":
        return VGroup(*[oval(x, 0, 0.24, 0.96, CINNAMON).rotate(1.0)
                        for x in [-0.16, 0.12]])
    if kind == "vanilla":
        return drop(0, 0, 0.9, CINNAMON)
    leaf = oval(0, 0, 0.66, 0.98, GREEN).rotate(-0.65)
    vein = path((-0.30, -0.37), (0, 0), (0.29, 0.34), color=ADULT, width=2, smooth=False)
    return VGroup(leaf, vein)


def drop(x, y, scale, color):
    bead = VMobject(stroke_width=0, fill_color=color, fill_opacity=1)
    bead.set_points_smoothly([p(0, 0.34), p(-0.17, -0.02), p(0, -0.23),
                              p(0.17, -0.02), p(0, 0.34)])
    return bead.scale(scale).move_to(p(x, y))


def cup(x, y=TABLE_Y, scale=1, *, cover=False, holes=False, label="",
        liquid=None, wide=False, clear=False):
    """An opaque paper cup, or a clear cup with a visible liquid surface."""
    half = 1.06 if wide else 0.82
    height = 2.07
    transparent = clear or liquid is not None
    body_color = "#57707C" if transparent else PAPER
    body = Polygon(p(-half, height), p(half, height), p(half * 0.73, 0),
                   p(-half * 0.73, 0), fill_color=body_color, fill_opacity=1,
                   stroke_color=TEXT, stroke_width=2)
    lip = oval(0, height, half * 2.01, 0.43, FOIL if transparent else PAPER)
    opening = oval(0, height + 0.015, half * 1.73, 0.29, INK)
    contents = VGroup()
    if liquid is not None:
        level = 1.47
        surface_half = half * 0.87
        contents = VGroup(
            Polygon(p(-surface_half, level), p(surface_half, level), p(half * 0.70, 0.09),
                    p(-half * 0.70, 0.09), fill_color=liquid, fill_opacity=1, stroke_width=0),
            oval(0, level, surface_half * 2, 0.30, "#FFE6A0" if liquid == YELLOW else "#ACE6F3"),
        )
    lid = VGroup(
        Polygon(p(-half * 1.02, height + 0.02), p(half * 1.02, height + 0.02),
                p(half * 0.93, height - 0.31), p(-half * 0.94, height - 0.31),
                fill_color=FOIL, fill_opacity=1, stroke_width=0),
        oval(0, height + 0.03, half * 2.06, 0.48, FOIL),
    )
    band = oval(0, height - 0.26, half * 1.89, 0.12, ADULT)
    dots = VGroup(*[oval(dx, height + dy, 0.093, 0.06, INK)
                    for dx, dy in [(-0.36, 0.03), (-0.17, 0.12), (0, 0.01), (0.19, 0.10), (0.36, 0.01)]])
    base = VGroup(body, contents, lip, opening).scale(scale, about_point=ORIGIN).shift(p(x, y))
    for part in (lid, band, dots):
        part.scale(scale, about_point=ORIGIN).shift(p(x, y))
    letter = M(label, size=34, color=INK).move_to(p(x, y + 0.87 * scale)) if label else VGroup()
    g = VGroup(base, *( [lid, band] if cover else []), *([dots] if holes else []), letter)
    g.lid, g.band, g.holes, g.letter = lid, band, dots, letter
    return g


def cup_row(*, covered=False, labels=False, positions=CUP_ROW, scale=1):
    return VGroup(*[cup(x, scale=scale, cover=covered, holes=covered,
                        label=chr(65 + i) if labels else "") for i, x in enumerate(positions)])


def bottle(x, y, color=CINNAMON, *, capped=True):
    base = RoundedRectangle(width=0.85, height=1.13, corner_radius=0.17,
                            fill_color=color, fill_opacity=1, stroke_width=0).move_to(p(x, y - 0.25))
    neck = oval(x, y + 0.35, 0.40, 0.53, color)
    cap = oval(x, y + 0.57, 0.52, 0.27, INK)
    label = oval(x, y - 0.28, 0.45, 0.52, PAPER)
    opening = oval(x, y + 0.57, 0.29, 0.10, INK)
    g = VGroup(base, neck, label, cap if capped else opening)
    g.cap, g.opening = cap, opening
    return g


def blocked(obj):
    center = obj.get_center()
    ring = Circle(radius=1.08, color=RED, stroke_width=8).move_to(center)
    slash = Line(center + UL * 0.73, center + DR * 0.73, color=RED, stroke_width=8)
    return VGroup(ring, slash)


def juice_pair(numbered=True):
    return VGroup(*[cup(x, scale=1, liquid=YELLOW, label=str(i + 1) if numbered else "")
                    for i, x in enumerate(JUICE_ROW)])


def seated_base(*, closed=False):
    return VGroup(person(5.11, 0.99, 0.98, adult=True),
                  person(2.48, 0.42, 0.97, closed=closed), table())


def pinch():
    return pinching_hand(2.49, 0.27, 1.02)


def predict_backdrop():
    return VGroup(seated_base(closed=True), juice_pair(), pinch())


def prediction_card():
    return question_card(PREDICTION, y=2.87, size=42, max_w=10.7)


def talk_line(text, x, y, *, color=GOLD, size=34, max_w=7):
    return fit_text(text, size=size, color=color, min_size=28, max_w=max_w).move_to(p(x, y))


class S01Hook(SpokenScene):
    def construct(self):
        world = cold_world()
        self.add(world)
        self.at("taste so dull")
        question = talk_line("Why does food taste dull with a cold?", -0.45, 2.96, size=43, max_w=12.1)
        self.play(FadeIn(question), run_time=0.61)
        self.at("few covered cups")
        cups = VGroup(cup(0.46, scale=0.57, cover=True, holes=True),
                      cup(1.63, scale=0.57, cover=True, holes=True))
        self.play(FadeIn(cups, shift=UP * 0.35), run_time=1.15)
        self.at("pinched nose")
        gesture = pinching_hand(3.23, 0.55, 1.05)
        self.play(FadeOut(world[3]), FadeIn(gesture, shift=UP * 0.3), run_time=0.95)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Smell Detectives: Parent Guide"
    LESSON = "Smell Detectives"

    def construct(self):
        self.add(cold_world())
        title = talk_line(self.TITLE, -0.42, 2.96, color=TEXT, size=53, max_w=12)
        self.play(FadeIn(title, shift=UP * 0.13), run_time=0.45)
        self.wait(max(0.05, self.narration_s - self.elapsed() - 1 / config.frame_rate))


class S03Payoff(SpokenScene):
    def construct(self):
        world = cold_world()
        self.add(world)
        self.at("takes about 30")
        row = cup_row()
        self.play(FadeOut(world[0], world[2], world[3], world[4], world[5], shift=LEFT * 0.5),
                  LaggedStart(*[FadeIn(c, shift=UP * 0.45) for c in row], lag_ratio=0.19),
                  run_time=1.35)
        timing = boxed_label("About 30 minutes", color=TEXT, size=36).move_to(p(-0.2, 2.62))
        self.play(FadeIn(timing), run_time=0.55)
        first = boxed_label("Describe in words", color=BLUE, size=30).move_to(p(-4.10, 1.62))
        second = boxed_label("Match by smell", color=GREEN, size=30).move_to(p(0.0, 1.62))
        third = boxed_label("Predict and check", color=GOLD, size=30).move_to(p(4.10, 1.62))
        self.at("practices describing smells")
        self.play(FadeOut(timing), run_time=0.24)
        self.play(FadeIn(first), run_time=0.38)
        self.at("matching by smell")
        self.play(FadeIn(second), row[0].animate.shift(RIGHT * 0.43),
                  row[1].animate.shift(LEFT * 0.43), run_time=1.63)
        self.at("checking a prediction")
        self.play(FadeIn(third), run_time=0.62)
        self.at("how much of flavor")
        steam = ribbon(-0.12, -0.22, 0.0, 1.12)
        self.play(FadeIn(steam), run_time=1.35)
        self.finish()


class S04SafetySetup(SpokenScene):
    def construct(self):
        adult, child = person(-3.74, 0.44, 1.10, adult=True), person(-0.87, 0.29, 0.88)
        self.add(adult, child, table())
        bob(adult, amp=0.11, speed=1.55)
        bob(child, amp=0.12, speed=1.8, seed=2)
        self.at("stay with your")
        food = VGroup(aroma_food("orange").scale(1.65).move_to(p(2.45, -1.18)),
                      aroma_food("mint").scale(1.52).move_to(p(4.05, -1.34)))
        self.at("use kitchen foods")
        self.play(FadeIn(food, shift=DOWN * 0.35), run_time=0.80)
        kitchen = talk_line("Kitchen foods only", 3.14, 1.54, color=GREEN)
        self.play(FadeIn(kitchen), run_time=0.5)
        self.at("skip essential oils")
        oil = bottle(3.20, -0.33, TEAL)
        self.play(FadeOut(food, kitchen), FadeIn(oil, shift=LEFT * 0.50), run_time=0.61)
        no_oil = blocked(oil)
        self.play(Create(no_oil), run_time=0.73)
        props = VGroup(oil, no_oil)
        self.remove(oil, no_oil)
        self.add(bob(props, amp=0.12, speed=1.85))
        self.at("check food allergies")
        check = talk_line("Check food allergies", 3.20, 1.52)
        self.play(FadeOut(props), FadeIn(food), run_time=0.65)
        self.play(FadeIn(check), run_time=0.61)
        self.at("skip nuts")
        bag = Polygon(p(2.47, -1.23), p(3.95, -1.23), p(3.82, 0.69), p(2.60, 0.69),
                      fill_color=CINNAMON, fill_opacity=1, stroke_width=0)
        nuts = VGroup(bag, oval(3.05, -0.31, 0.39, 0.73, PAPER).rotate(-0.35),
                      oval(3.43, -0.25, 0.36, 0.70, PAPER).rotate(0.34))
        self.play(FadeOut(food, check), FadeIn(nuts), run_time=0.53)
        crossed = blocked(nuts)
        self.play(Create(crossed), run_time=0.72)
        self.at("bands if anyone")
        self.play(FadeOut(nuts, crossed), run_time=0.40)
        package = boxed_label("Latex-free", color=BLUE, size=35).move_to(p(3.2, 0.35))
        bands = VGroup(*[Ellipse(width=1.35, height=0.39, color=GOLD, stroke_width=7)
                         .move_to(p(3.2 + i * 0.11, -0.95 + i * 0.21)) for i in range(3)])
        reach = hand(1.43, 0.2, 0.78, angle=-1.13)
        self.play(FadeIn(package), FadeIn(bands), FadeIn(reach, shift=RIGHT * 0.5),
                  run_time=0.93)
        bob(reach, amp=0.12)
        self.finish()


class S04Cups(SpokenScene):
    def construct(self):
        row = cup_row()
        self.add(table(), row)
        self.at("cotton ball")
        balls = VGroup(*[cotton(x, 1.53) for x in CUP_ROW])
        self.play(LaggedStart(*[FadeIn(ball, shift=DOWN * 0.45) for ball in balls], lag_ratio=0.13),
                  run_time=0.77)
        self.bring_to_front(row)
        self.play(LaggedStart(*[FadeOut(b, shift=DOWN * 2.27) for b in balls], lag_ratio=0.13),
                  run_time=2.18)
        self.remove(*balls)
        self.at("add one kitchen")
        self.play(row[0].animate.shift(RIGHT * 0.37), row[1].animate.shift(LEFT * 0.37),
                  row[2].animate.shift(RIGHT * 0.37), row[3].animate.shift(LEFT * 0.37),
                  run_time=1.05)
        active = row
        for cue, kind, x, run in [
            ("try orange peel", "orange", -2.60, 0.95),
            ("coffee", "coffee", 2.60, 0.60),
            ("cinnamon stick", "cinnamon", -2.60, 0.76),
            ("vanilla", "vanilla", 2.60, 0.71),
            ("crushed mint leaf", "mint", -2.60, 0.92),
        ]:
            self.at(cue)
            pair = VGroup(cup(x - 0.93), cup(x + 0.93))
            ingredient = aroma_food(kind).scale(1.53).move_to(p(x, 1.17))
            portions = [aroma_food(kind).scale(0.71).move_to(ingredient) for _ in pair]
            self.play(FadeOut(active), FadeIn(pair), FadeIn(ingredient, shift=DOWN * 0.17),
                      run_time=0.25)
            self.add(*portions)
            self.bring_to_front(pair)
            self.play(FadeOut(ingredient), *[FadeOut(piece, shift=p(c.get_x() - x, -1.97))
                       for piece, c in zip(portions, pair)], run_time=run - 0.25)
            active = pair
        self.play(FadeOut(active), FadeIn(cup_row()), run_time=0.39)
        self.finish()


class S05Cover(SpokenScene):
    def construct(self):
        row = cup_row()
        self.add(table(), row)
        self.at("you cover each")
        fingers = hand(row[0].get_x() - 0.10, 0.55, angle=PI)
        self.play(FadeIn(fingers, shift=DOWN * 0.29), run_time=0.53)
        self.play(LaggedStart(*[FadeIn(c.lid, shift=DOWN * 0.25) for c in row], lag_ratio=0.20),
                  fingers.animate.shift(RIGHT * 2.6), run_time=1.15)
        self.at("rubber band")
        self.play(LaggedStart(*[FadeIn(c.band, shift=DOWN * 0.09) for c in row], lag_ratio=0.15),
                  FadeOut(fingers, shift=UP * 0.4), run_time=0.85)
        self.at("poke four")
        pencil = Polygon(p(-0.10, 0), p(0.10, 0), p(0.10, -1.86), p(0, -2.18), p(-0.10, -1.86),
                         fill_color=GOLD, fill_opacity=1, stroke_width=0).rotate(-0.20)
        pencil.set_z_index(4).move_to(p(CUP_ROW[0] + 0.19, 1.15))
        grip = hand(CUP_ROW[0] + 0.22, 1.72, angle=-0.88).set_z_index(5)
        tool = VGroup(pencil, grip)
        self.play(FadeIn(tool, shift=DOWN * 0.35), run_time=0.42)
        for i, c in enumerate(row):
            if i:
                self.play(tool.animate.shift(RIGHT * 2.60), run_time=0.39)
            self.play(tool.animate.shift(DOWN * 0.75), run_time=0.22)
            self.add(c.holes)
            self.play(tool.animate.shift(UP * 0.75), run_time=0.29)
        self.play(FadeOut(tool, shift=UP * 0.46), run_time=0.48)
        self.at("label the cups")
        letters = [cup(x, label=chr(65 + i)).letter for i, x in enumerate(CUP_ROW)]
        self.play(LaggedStart(*[FadeIn(letter) for letter in letters], lag_ratio=0.19), run_time=0.96)
        self.at("keep a secret")
        cover = Polygon(p(1.95, 0.81), p(4.38, 0.81), p(4.61, 1.37), p(2.18, 1.37),
                        fill_color=ADULT, fill_opacity=1, stroke_width=0)
        pages = Polygon(p(1.99, 0.80), p(4.34, 0.80), p(4.34, 0.63), p(1.99, 0.63),
                        fill_color=PAPER, fill_opacity=1, stroke_width=0)
        spine = path((2.18, 1.36), (1.94, 0.81), (1.94, 0.64), (4.36, 0.64),
                     color=ADULT, width=5, smooth=False)
        book = VGroup(cover, pages, spine).set_z_index(1)
        key = boxed_label("Secret key", color=GOLD, size=29).move_to(p(0.21, 1.02))
        self.play(FadeIn(book, key), run_time=0.30)
        self.wait(0.80)
        self.play(FadeOut(key.label, shift=RIGHT * 0.32),
                  key.box.animate.shift(RIGHT * 0.32), run_time=0.35)
        self.play(FadeOut(key.box, shift=RIGHT * 2.53), run_time=0.35)
        self.finish()


MATCHED_ROW = (-4.10, -2.16, 1.86, 3.80)


def matched_cups():
    return VGroup(*[cup(x, cover=True, holes=True, label=letter)
                    for x, letter in zip(MATCHED_ROW, "ACBD")])


class S06Waft(SpokenScene):
    def construct(self):
        row = cup_row(covered=True, labels=True)
        face = person(3.25, 1.54, 1.11, adult=True).set_z_index(-2)
        self.add(table(), row)
        self.at("how to waft")
        self.play(FadeIn(face, shift=UP * 0.2), run_time=0.65)
        self.at("hold a cup")
        active = row[2]
        self.play(active.animate.shift(p(0.70, 0.53)), run_time=1.47)
        support = hand(2.28, -1.83, scale=0.67, angle=0.93)
        self.play(FadeIn(support), face.animate.shift(DOWN * 0.21), run_time=0.72)
        self.at("wave the air")
        waving = hand(0.82, 0.73, scale=0.88, angle=-0.69)
        air = ribbon(2.12, 0.28, 0.73, 0.93)
        self.play(FadeIn(waving), FadeIn(air), run_time=0.57)
        self.play(Rotate(waving, angle=-0.73), face.animate.shift(p(-0.18, -0.08)),
                  rate_func=there_and_back, run_time=2.12)
        bob(waving, amp=0.27, speed=2.0)
        bob(face, amp=0.19, speed=1.5)
        self.at("strong or faint")
        strong = boxed_label("Strong or faint?", color=GOLD, size=38).move_to(p(-3.27, 1.68))
        self.play(FadeIn(strong), run_time=0.52)
        self.at("pleasant or not")
        pleasant = boxed_label("Pleasant or not?", color=GOLD, size=38).move_to(strong)
        self.play(swap(strong, pleasant, run_time=0.63))
        self.at("mix up the cups")
        self.play(FadeOut(face, air, waving, support, pleasant),
                  row[2].animate.shift(UP * 1.92), run_time=0.48)
        self.play(row[2].animate.shift(LEFT * 4.16),
                  row[1].animate.shift(RIGHT * 3.16), run_time=0.60)
        self.play(row[2].animate.shift(DOWN * 2.45),
                  row[0].animate.shift(LEFT * 0.20),
                  row[3].animate.shift(LEFT * 0.10), run_time=0.68)
        self.finish()


class S07Name(SpokenScene):
    def construct(self):
        row = matched_cups()
        self.add(table(), row)
        self.at("guess what each")
        guesses = [boxed_label(text, color=GOLD, size=35).move_to(p(x, 1.90))
                   for text, x in [("Candy?", -3.13), ("Christmas?", 2.83)]]
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.18) for g in guesses], lag_ratio=0.3),
                  run_time=0.84)
        self.at("peel back the")
        mint_cup = row[0]
        foil = VGroup(mint_cup.lid, mint_cup.band, mint_cup.holes)
        mint = aroma_food("mint").move_to(p(-4.10, -0.37)).scale(0.88)
        self.play(foil.animate.rotate(-0.70, about_point=mint_cup.lid.get_left()).shift(UP * 0.36),
                  FadeIn(mint, shift=UP * 0.38), run_time=1.44)
        check = path((-3.19, 0.10), (-2.96, -0.12), (-2.55, 0.35),
                     color=GREEN, width=9, smooth=False)
        self.play(Create(check), run_time=0.40)
        self.at("common to know")
        scent = ribbon(-4.10, 0.06, 0.42, 0.94, opacity=0.60)
        self.play(FadeIn(scent), run_time=0.82)
        self.at("not find its name")
        self.play(FadeOut(*guesses), run_time=0.60)
        self.at("where have you")
        question = question_card("Where have you smelled this before?", y=2.41, size=39,
                                 max_w=11.0)
        self.play(FadeIn(question), run_time=0.61)
        self.finish()


class S07Vanilla(SpokenScene):
    def construct(self):
        adult = person(-3.98, 0.64, 1.08, adult=True)
        left, right = [cup(x, wide=True) for x in [0.27, 3.84]]
        self.add(adult, table(), left, right)
        bob(adult, amp=0.12, speed=1.7)
        self.at("make two covered")
        extract = bottle(-1.10, 1.02, capped=False)
        grasp = hand(-1.50, 0.70, 0.69, angle=-0.96)
        held = VGroup(extract, grasp)
        balls = VGroup(cotton(0.27, -0.58, 0.90), cotton(3.84, -0.58, 0.90))
        self.play(FadeIn(held, shift=RIGHT * 0.35), FadeIn(balls), run_time=0.87)
        self.at("one drop to")
        tilt = -2.40
        pour_at = p(left.get_x(), 0.95)
        self.play(held.animate.rotate(tilt, about_point=extract.opening.get_center())
                  .shift(pour_at - extract.opening.get_center()), run_time=0.56)
        single = drop(left.get_x(), -0.06, 0.77, CINNAMON)
        self.play(FadeIn(single, target_position=extract.opening), run_time=0.70)
        self.play(FadeOut(single, shift=DOWN * 0.42), run_time=0.38)
        self.at("six to the other")
        self.play(held.animate.shift(RIGHT * (right.get_x() - left.get_x())), run_time=0.59)
        beads = [drop(right.get_x() + (i % 3 - 1) * 0.26, -0.05 + (i // 3) * 0.29, 0.52, CINNAMON)
                 for i in range(6)]
        self.play(LaggedStart(*[FadeIn(b, target_position=extract.opening) for b in beads], lag_ratio=0.25),
                  run_time=0.9)
        self.at("you handle the extract")
        self.play(FadeOut(*beads, balls), FadeIn(left.lid, left.band, left.holes),
                  FadeIn(right.lid, right.band, right.holes),
                  held.animate.rotate(-tilt).move_to(p(-1.18, 0.83)), run_time=1.19)
        self.at("contains alcohol")
        warning = boxed_label("Contains alcohol", color=GOLD, size=31).move_to(p(2.33, 2.06))
        self.play(FadeIn(warning), run_time=0.57)
        self.at("close it and")
        lid = extract.cap.move_to(extract.opening)
        self.play(FadeIn(lid, shift=DOWN * 0.27), run_time=0.39)
        self.play(FadeOut(held, lid, shift=UL * 0.7), FadeOut(warning), run_time=0.92)
        first = M("1 drop", size=34, color=TEXT).move_to(p(0.27, -3.13))
        second = M("6 drops", size=34, color=TEXT).move_to(p(3.84, -3.13))
        self.play(FadeIn(first, second), run_time=0.45)
        self.at("compare the smells")
        waft = ribbon(0.27, -0.12, -0.42, 1.20)
        self.play(FadeIn(waft), run_time=0.50)
        self.at("resting a minute")
        wait = boxed_label("Rest 1 minute", color=GOLD, size=33).move_to(p(2.02, 1.94))
        clock = Circle(radius=0.52, color=GOLD, stroke_width=5).move_to(p(2.02, 0.68))
        tick = Line(clock.get_center(), clock.get_center() + UP * 0.33, color=GOLD, stroke_width=5)
        self.play(FadeOut(waft), FadeIn(wait, clock, tick), run_time=0.42)
        self.play(Rotate(tick, -TAU, about_point=clock.get_center()), rate_func=linear, run_time=0.83)
        self.play(FadeIn(ribbon(3.84, -0.12, -0.31, 1.20)), run_time=0.61)
        self.finish()


class S08TasteSafety(SpokenScene):
    def construct(self):
        row = VGroup(*[cup(x, cover=True, holes=True) for x in (-3.75, -1.35)])
        stage = table()
        self.add(stage, row)
        self.at("only for smelling")
        mouth = VGroup(oval(2.68, 0.17, 1.56, 0.62, CHILD),
                       path((2.04, 0.18), (2.68, 0.03), (3.32, 0.18), color=INK, width=5))
        scent = ribbon(-2.55, -0.10, 0.35, 1.77)
        self.play(FadeIn(mouth), FadeIn(scent), run_time=0.58)
        stop = blocked(mouth)
        self.play(Create(stop), run_time=0.73)
        self.at("wash hands after")
        self.play(FadeOut(row, mouth, stop, scent), run_time=0.47)
        hands = VGroup(hand(-0.61, 0.13, 1.55, -0.66), hand(0.62, -0.32, 1.49, 0.79))
        tap = path((2.09, -0.97), (2.09, 1.89), (0.93, 2.19), (0.19, 1.69),
                   color=FOIL, width=19)
        water = VGroup(*[bob(drop(0.17 + i * 0.14, 1.24 - i * 0.34, 0.60, BLUE),
                             amp=0.16, speed=3.0, seed=i) for i in range(4)])
        self.play(Create(tap), FadeIn(hands, water), run_time=0.67)
        self.play(hands[0].animate.shift(RIGHT * 0.34), hands[1].animate.shift(LEFT * 0.34),
                  rate_func=there_and_back, run_time=1.71)
        self.at("skip tasting if")
        caution = boxed_label("Trouble swallowing?\nSkip tasting.", color=RED, size=34).move_to(p(-3.57, 0.54))
        self.play(FadeOut(tap, water, hands), run_time=0.44)
        seated = seated_base()
        self.remove(stage)
        self.add(seated)
        bob(seated[0], amp=0.10, speed=1.7)
        bob(seated[1], amp=0.11, speed=1.9, seed=3)
        self.play(FadeIn(caution), run_time=0.55)
        self.at("have them sit")
        sip = cup(-1.35, scale=0.64, liquid=YELLOW)
        instruction = talk_line("Small sips", -3.72, 1.55, size=36)
        self.play(FadeOut(caution), FadeIn(sip, shift=DOWN * 0.26), run_time=0.63)
        self.at("take small sips")
        self.play(FadeIn(instruction), run_time=0.44)
        self.at("swallow before talking")
        after = talk_line("Swallow before talking", -3.72, 1.55, size=34, max_w=5.65)
        self.play(swap(instruction, after, run_time=0.76))
        self.finish()


class S08TasteSetup(SpokenScene):
    def construct(self):
        seated = seated_base()
        self.add(seated)
        self.at("pour two juices")
        empty = VGroup(*[cup(x, clear=True) for x in JUICE_ROW])
        filled = juice_pair(numbered=False)
        carafes = VGroup(*[bottle(x - 0.25, 1.74, YELLOW, capped=False).rotate(-2.2)
                           for x in JUICE_ROW])
        self.play(FadeIn(empty, shift=DOWN * 0.34), run_time=0.75)
        self.play(FadeIn(carafes, shift=DOWN * 0.27), run_time=0.80)
        self.at("apple and white")
        names = [talk_line(text, x, 2.84, color=TEXT, size=30, max_w=3.5)
                 for x, text in [(-4.05, "Apple"), (-0.94, "White grape")]]
        for source, target, bottle_obj, name in zip(empty, filled, carafes, names):
            x = source.get_x()
            stream = path(tuple(bottle_obj.opening.get_center()[:2]), (x, 0.62),
                          (x, -0.66), color=YELLOW, width=8)
            self.play(Create(stream), FadeIn(name), run_time=0.63)
            self.play(FadeIn(target[0][1]), FadeOut(stream), run_time=0.82)
        self.play(FadeOut(carafes, *names), run_time=0.61)
        self.at("mark them one")
        self.play(LaggedStart(*[FadeIn(c.letter) for c in juice_pair()], lag_ratio=0.35), run_time=0.96)
        self.at("close their eyes")
        child = seated[1]
        leaning = seated_base(closed=True)[1].shift(p(-0.30, -0.11))
        self.play(Transform(child, leaning), seated[0].animate.shift(DOWN * 0.25),
                  run_time=0.72)
        self.at("pinch their nose")
        self.play(FadeIn(pinch(), shift=DOWN * 1.02), child.animate.shift(p(0.30, 0.11)),
                  seated[0].animate.shift(UP * 0.25), run_time=1.18)
        self.finish()


class S09PredictQuestion(SpokenScene):
    def construct(self):
        world = predict_backdrop()
        adult = world[0][0]
        self.add(world)
        self.at("make a prediction")
        q = prediction_card()
        self.play(FadeIn(q), adult.animate.shift(p(-0.12, -0.14)), run_time=0.78)
        self.at("with their nose pinched")
        # Keep both cups untouched as the adult looks between them.
        self.play(adult.animate.shift(p(-0.05, -0.15)), run_time=1.38)
        self.at("tell which juice")
        self.play(adult.animate.shift(p(0.17, 0.29)), rate_func=linear, run_time=2.24)
        self.finish()


class S10PredictPause(PredictPause):
    QUESTION = PREDICTION
    CARD = {"y": 2.87, "size": 42, "max_w": 10.7}
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop()

    def construct(self):
        # Hold the prior composition without a timer or a hint.
        self.add(self.backdrop(), prediction_card())
        self.wait(self.SECONDS)


class S11Reveal(SpokenScene):
    def construct(self):
        adult, child, stage = seated_base(closed=True)
        left, right = juice_pair()
        pinched = pinch()
        self.add(adult, child, stage, left, right, pinched)
        self.at("offer a small sip")
        serve = hand(-4.39, -1.33, 0.92, -0.82)
        self.play(FadeIn(serve, shift=RIGHT * 0.67),
                  adult.animate.shift(LEFT * 0.10), run_time=0.56)
        # The front-facing child takes a sip from the rim, with the cup lifted only for the sip.
        held_sip = cup(2.03, -1.43, scale=0.72, liquid=YELLOW)[0].rotate(-0.28)
        self.play(FadeOut(left.letter, serve), run_time=0.28)
        self.play(ReplacementTransform(left[0], held_sip, path_arc=-1.55), run_time=1.09)
        self.at("signal their guess")
        guess = hand(0.72, 0.94, 0.99, 0.05, fingers=2)
        self.play(FadeIn(guess, shift=UP * 0.68), held_sip.animate.shift(p(-0.37, -0.59)), run_time=1.02)
        self.play(guess.animate.shift(UP * 0.28), rate_func=there_and_back, run_time=1.50)
        self.at("let go of")
        self.play(FadeOut(pinched, guess, shift=DOWN * 0.64),
                  child.animate.shift(UP * 0.13), run_time=0.65)
        scent = path((2.14, -0.06), (1.98, 0.09), (2.10, 0.31), (2.37, 0.36),
                     color=BLUE, width=7)
        tip = aroma_tip(scent, length=0.23, width=0.21)
        self.at("and swallow")
        self.play(Create(scent), FadeIn(tip), child.animate.shift(DOWN * 0.13),
                  held_sip.animate.shift(DOWN * 0.27), run_time=0.92)
        pulse(scent, base=7.0, amp=2.5, speed=3.0)
        self.at("what changed when")
        question = question_card("What changed when you let go?", y=2.89, size=38)
        self.play(FadeIn(question), run_time=0.71)
        self.at("offer water")
        water = cup(-3.65, liquid=BLUE)
        self.play(FadeOut(scent, tip, held_sip, question), FadeIn(water, shift=RIGHT * 0.54),
                  run_time=0.68)
        self.at("repeat with the other")
        other_sip = cup(2.03, -1.43, scale=0.72, liquid=YELLOW)[0].rotate(-0.28)
        self.play(FadeOut(right.letter), FadeIn(pinch()), run_time=0.30)
        self.play(ReplacementTransform(right[0], other_sip), run_time=0.88)
        self.finish()


def profile():
    """Side view. The front faces left, with room inside for the airflow path."""
    outline = VMobject(stroke_color=SKIN, stroke_width=5, fill_color="#583F47", fill_opacity=1)
    outline.set_points_smoothly([p(-0.25, -2.60), p(0.26, -1.72), p(1.40, -0.45),
                                 p(1.34, 1.31), p(0.32, 2.65), p(-1.58, 2.65),
                                 p(-2.65, 1.71), p(-2.73, 0.84)])
    outline.add_points_as_corners([p(-3.43, 0.16), p(-3.24, -0.02), p(-2.81, -0.06),
                                  p(-2.82, -0.42), p(-2.41, -0.58), p(-2.83, -0.69),
                                  p(-2.77, -1.19), p(-2.20, -1.61), p(-1.99, -2.60),
                                  p(-0.25, -2.60)])
    eye = oval(-2.42, 0.85, 0.17, 0.26, TEXT)
    ear = oval(0.33, 0.40, 0.53, 0.78, SKIN, 0.68)
    tongue = oval(-2.16, -0.79, 0.85, 0.25, CHILD)
    brain = VGroup(oval(-0.96, 1.66, 1.76, 1.01, "#755C71"),
                   oval(-0.22, 1.64, 1.36, 0.99, "#755C71"),
                   oval(-0.53, 2.00, 1.31, 0.70, "#755C71"))
    return VGroup(outline, eye, ear, tongue, brain)


class S12Why(SpokenScene):
    def construct(self):
        self.add(table(), profile())
        self.at("breathe out after")
        breath = ribbon(-3.52, 0.10, -1.27, 0.54, GREY, 0.70)
        self.play(FadeIn(breath), run_time=0.67)
        self.at("aromas can travel")
        route = path((-2.05, -0.55), (-1.39, -0.52), (-1.08, -0.13), (-1.64, 0.33),
                     (-2.35, 0.32), (-2.88, 0.13), color=BLUE, width=8)
        tip = aroma_tip(route, length=0.27, width=0.24)
        self.play(Create(route), FadeOut(breath), run_time=1.53)
        self.play(FadeIn(tip), run_time=0.24)
        pulse(route, base=8, amp=2.1, speed=3.6)
        aroma = boxed_label("Food aromas", color=BLUE, size=38).move_to(p(3.95, 1.67))
        self.at("to your nose")
        self.play(FadeIn(aroma), run_time=0.56)
        self.at("your brain combines")
        taste_path = path((-2.09, -0.93), (-1.22, -1.08), (-0.53, -0.54), (-0.43, 0.24),
                          (-0.68, 1.18), color=YELLOW, width=7)
        taste = boxed_label("Taste", color=YELLOW, size=38).move_to(p(3.95, 0.48))
        smell_path = DashedVMobject(path((-2.13, 0.39), (-1.75, 0.82), (-1.27, 1.25),
                                         color=BLUE, width=6), num_dashes=7)
        self.play(Create(taste_path), Create(smell_path), run_time=0.77)
        self.play(FadeIn(taste), run_time=0.48)
        pulse(taste_path, base=7, amp=2, speed=3)
        self.at("pinching your nose")
        fingers = pinching_hand(-3.19, -0.01, 0.86).flip(UP, about_point=p(-3.19, -0.01))
        route.clear_updaters()
        self.play(FadeIn(fingers, shift=UP * 0.41), route.animate.set_stroke(opacity=0.23),
                  tip.animate.set_opacity(0.23), smell_path.animate.set_stroke(opacity=0.23),
                  run_time=1.13)
        fade = boxed_label("Flavor fades", color=GOLD, size=38).move_to(p(3.95, -0.86))
        self.at("the flavor fade")
        self.play(FadeIn(fade), run_time=0.70)
        self.finish()


class S13Safety(SpokenScene):
    def construct(self):
        adult = person(3.77, 0.69, 1.14, adult=True)
        self.add(adult, table())
        bob(adult, amp=0.11, speed=1.85)
        self.at("keep cotton balls")
        small = VGroup(cotton(-3.87, -1.32, 1.22),
                       Ellipse(width=1.31, height=0.45, color=GOLD, stroke_width=8).move_to(p(-1.93, -1.52)),
                       aroma_food("cinnamon").move_to(p(-0.42, -1.43)))
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.25) for o in small], lag_ratio=0.37),
                  run_time=1.31)
        caution = boxed_label("Choking risk under four", color=RED, size=37).move_to(p(-2.94, 1.78))
        self.at("other small pieces")
        self.play(FadeIn(caution), run_time=0.59)
        self.at("away from children")
        palm = hand(0.95, -1.23, 1.28, -0.84)
        self.play(FadeIn(palm, shift=LEFT * 0.46), run_time=0.48)
        self.play(FadeOut(palm, small, shift=UR * 1.3), run_time=1.71)
        self.at("call 911")
        emergency = boxed_label("Call 911 for choking", color=RED, size=39).move_to(caution)
        self.play(swap(caution, emergency, run_time=0.60))
        self.at("cannot cough")
        condition = talk_line("Cannot cough, cry, or talk", -2.94, 0.57, color=TEXT, size=33, max_w=6.7)
        self.play(FadeIn(condition), run_time=0.66)
        self.finish()


class S15Return(SpokenScene):
    def construct(self):
        world = cold_world()
        self.add(world)
        self.at("food taste dull")
        question = talk_line("Why does food taste dull with a cold?", -0.45, 2.96, size=43, max_w=12.1)
        self.play(FadeIn(question), run_time=0.57)
        self.at("stuffy nose makes")
        haze = ribbon(0.1, 0.07, 1.45, 0.57, GREY, 0.52)
        self.play(FadeIn(haze), world[0].animate.shift(p(-0.20, -0.14)),
                  world[3].animate.shift(p(-0.20, -0.14)), run_time=1.23)
        self.play(world[0].animate.shift(p(0.20, 0.14)),
                  world[3].animate.shift(p(0.20, 0.14)), run_time=1.57)
        self.at("compare what your")
        drinks = VGroup(cup(-0.15, scale=0.66, liquid=YELLOW, label="1"),
                        cup(1.19, scale=0.66, liquid=YELLOW, label="2"))
        adult = person(-4.35, 0.69, 1.12, adult=True).set_z_index(-1)
        self.play(FadeOut(question), FadeIn(adult, shift=RIGHT * 0.28),
                  FadeIn(drinks, shift=DOWN * 0.30), run_time=0.92)
        bob(adult, amp=0.10, speed=1.88)
        self.finish()


class S16End(EndCard):
    LINE = "Much of flavor comes from aromas that reach your nose."
