"""Overhead activity drawings and a matching schematic of the Virginia river cliff."""
from bp_parts import *
from bp_style import EndCard

# Color map: terracotta clay, ivory paper and shells, green leaves, blue water,
# gold for a clue, teal for setup and protective gear, red for a warning.
CLAY = "#BA694B"
CLAY_EDGE = "#7B402E"
CLAY_LIGHT = "#F0A67C"
PAPER = "#DDCFB8"
SHELL = "#FFE3AE"
LEAF = "#619553"
VEIN = "#D1E7A7"
WOOD = "#332926"
NEWS = "#625952"
INK = "#332725"
SAND = "#AB825A"
PLASTER = "#F4EDD8"
SKIN = "#BB835F"
WATER = "#3E8299"
QUESTION = "Which details will stay?"
QUESTION_STYLE = {"size": 38, "y": -3.35}
SINGLE = np.array([0., -0.30, 0.])
PAIR = (np.array([-3.20, -0.82, 0.]), np.array([3.20, -0.82, 0.]))
SPECIMEN_OFFSET = UP * 2.98


def xy(x, y):
    return np.array([x, y, 0.])


def panel(w, h, color, at=ORIGIN, radius=0.2, edge=None, stroke=2):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, fill_color=color, fill_opacity=1,
        stroke_color=edge or color, stroke_width=stroke,
    ).move_to(at)


def oval(w, h, color, at=ORIGIN, edge=None, stroke=2):
    return Ellipse(
        width=w, height=h, fill_color=color, fill_opacity=1,
        stroke_color=edge or color, stroke_width=stroke,
    ).move_to(at)


def path(points, color, width=4):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(
        [xy(x, y) for x, y in points]
    )


def solid(points, color, edge, width=3):
    mob = path(points + [points[0]], edge, width)
    mob.set_fill(color, opacity=1)
    return mob


def newspaper():
    sheets = VGroup()
    for x in (-3.12, 3.12):
        sheet = VGroup(panel(6.24, 5.58, NEWS, xy(x, -0.04), radius=0.09, stroke=0),
                       Line(xy(x - 3.08, 2.69), xy(x + 3.08, 2.69), color="#827367", stroke_width=3))
        for dx in (-2.04, 0, 2.04):
            for row in range(10):
                y = 2.20 - 0.485 * row
                half_width = 0.83 if row % 5 != 4 else 0.58
                sheet.add(Line(xy(x + dx - 0.86, y), xy(x + dx - 0.86 + 2 * half_width, y),
                               color="#756960", stroke_width=3))
        sheets.add(sheet)
    return sheets.set_z_index(-3)


def tabletop(with_paper=True):
    base = Rectangle(width=13.56, height=7.52, fill_color=WOOD, fill_opacity=1, stroke_width=0)
    base.set_z_index(-4)
    return VGroup(base, newspaper()) if with_paper else VGroup(base)


def shell(stamp=False, cast=False):
    outer = [(-0.30, -0.77), (-0.82, -0.47), (-1.09, 0.10), (-0.89, 0.57),
             (-0.50, 0.72), (-0.03, 0.81), (0.45, 0.74), (0.88, 0.57),
             (1.09, 0.10), (0.82, -0.47), (0.30, -0.77), (0.0, -0.86)]
    fill, shade, light = (CLAY_EDGE, "#5E2D22", CLAY_LIGHT) if stamp else (
        (PLASTER, "#AD9875", WHITE) if cast else (SHELL, "#9D693F", "#FFF2D7")
    )
    body = solid(outer, fill, shade, 4)
    ribs = VGroup()
    for x, y in [(-0.90, 0.25), (-0.62, 0.50), (-0.31, 0.62), (0, 0.66),
                 (0.31, 0.62), (0.62, 0.50), (0.90, 0.25)]:
        coords = [(x * 0.18, -0.67), (x * 0.68, -0.17), (x, y)]
        ribs.add(VGroup(path([(a + 0.036, b - 0.022) for a, b in coords], shade, 7),
                        path(coords, light, 3.4)))
    hinge = oval(0.49, 0.17, shade, xy(0, -0.71), stroke=0)
    obj = VGroup(body, ribs, hinge)
    obj.detail = ribs[3][1]
    return obj


def leaf(stamp=False):
    fill, side, veins = (CLAY_EDGE, "#5E2D22", CLAY_LIGHT) if stamp else (LEAF, "#304E33", VEIN)
    edge = [(0, -0.84), (-0.59, -0.54), (-0.72, -0.10), (-0.57, 0.37),
            (-0.26, 0.67), (0.45, 0.93), (0.69, 0.39), (0.61, -0.12), (0.39, -0.56)]
    body = solid(edge, fill, side)
    midrib = path([(-0.18, -1.01), (0, -0.58), (0.15, 0.11), (0.41, 0.79)], veins, 5.5)
    branches = VGroup(*[
        path([start, mid, end], veins, 3)
        for start, mid, end in [
            ((0, -0.58), (-0.35, -0.40), (-0.53, -0.25)),
            ((0.05, -0.33), (0.32, -0.24), (0.49, -0.07)),
            ((0.10, -0.13), (-0.21, 0.03), (-0.47, 0.27)),
            ((0.17, 0.17), (0.43, 0.27), (0.55, 0.47)),
            ((0.25, 0.38), (0.02, 0.40), (-0.18, 0.57)),
        ]
    ])
    obj = VGroup(body, midrib, branches)
    obj.detail = midrib
    return obj


def tracks():
    prints = VGroup()
    for x, y, angle in [(-0.43, -0.38, -0.24), (0.40, 0.37, 0.14)]:
        toes = VGroup(*[oval(0.15, 0.28, CLAY_EDGE, xy(dx, dy), edge=CLAY_LIGHT)
                        for dx, dy in [(-0.23, 0.17), (0, 0.30), (0.22, 0.16)]])
        pad = oval(0.47, 0.38, CLAY_EDGE, xy(0, -0.13), edge=CLAY_LIGHT)
        prints.add(VGroup(pad, toes).rotate(angle).move_to(xy(x, y)))
    prints.detail = prints[1][1][1]
    return prints


def plate(at=SINGLE, scale=1, clay=True):
    rim = oval(5.30, 4.46, PAPER, edge="#AD9A7E", stroke=5)
    inner = oval(4.73, 3.88, "#F3E6CD", edge="#C0AB8B", stroke=4)
    group = VGroup(rim, inner)
    if clay:
        group.add(oval(3.78, 3.23, CLAY_EDGE, xy(0, -0.07), edge=CLAY_EDGE, stroke=4),
                  oval(3.78, 3.10, CLAY, xy(0, 0.07), edge=CLAY_LIGHT, stroke=3))
    return group.scale(scale).move_to(at)


def impression(factory, at, scale=1):
    return factory(stamp=True).scale(scale).move_to(at + UP * 0.06)


def pair_world(with_prints=False):
    plates = VGroup(*(plate(at, 0.87) for at in PAIR))
    objects = VGroup(shell().scale(0.89).move_to(PAIR[0] + SPECIMEN_OFFSET),
                     leaf().scale(0.89).move_to(PAIR[1] + SPECIMEN_OFFSET))
    marks = VGroup(impression(shell, PAIR[0], 0.89), impression(leaf, PAIR[1], 0.89))
    world = VGroup(tabletop(), plates, objects)
    if with_prints:
        world.add(marks)
    return world, objects, marks


def gloss(mob, width=6):
    return mob.copy().set_stroke(GOLD, width=width, opacity=1).set_fill(opacity=0).set_z_index(4)


def cue_text(value, color=TEXT, y=-3.28, size=34):
    return caption(value, size=size, color=color, y=y).set_x(0).set_z_index(8)


def hand(color=SKIN):
    palm = oval(0.79, 0.95, color, xy(0, -0.06), edge=INK)
    fingers = VGroup(*[panel(0.16, h, color, xy(x, 0.36), radius=0.075, edge=INK, stroke=1)
                       for x, h in [(-0.25, 0.46), (-0.07, 0.62), (0.11, 0.58), (0.28, 0.44)]])
    thumb = oval(0.23, 0.51, color, xy(-0.40, -0.03), edge=INK, stroke=1).rotate(0.43)
    return VGroup(thumb, fingers, palm)


def person(adult=True, protected=False):
    shirt = TEAL if adult else "#B59A76"
    hair_color = "#8A5E48"
    shoulders = solid([(-1.06, -1.05), (-1.04, -0.42), (-0.68, -0.13), (0.65, -0.13),
                       (1.04, -0.42), (1.06, -1.05), (0, -1.21)], shirt, INK)
    neck = panel(0.37, 0.52, SKIN, xy(0, -0.04), radius=0.13, edge=INK)
    hair = oval(1.24, 1.36, hair_color, xy(0, 0.81), edge=INK)
    face = oval(1.06, 1.21, SKIN, xy(0, 0.68), edge=INK)
    fringe = path([(-0.47, 0.99), (-0.07, 1.15), (0.43, 0.99)], hair_color, 13)
    eyes = VGroup(*(Dot(xy(x, 0.78), radius=0.045, color=INK) for x in (-0.19, 0.19)))
    obj = VGroup(shoulders, neck, hair, face, fringe, eyes)
    if protected:
        obj.add(mask(), glasses())
    return obj


def mask():
    return VGroup(Line(xy(-0.51, 0.62), xy(0.51, 0.62), color=PLASTER, stroke_width=5),
                  solid([(-0.36, 0.68), (0, 0.58), (0.36, 0.68), (0.26, 0.34),
                         (0, 0.22), (-0.26, 0.34)], PLASTER, "#6DA1A6"))


def glasses():
    return VGroup(Line(xy(-0.51, 0.80), xy(0.51, 0.80), color=TEAL, stroke_width=5),
                  *[RoundedRectangle(width=0.43, height=0.25, corner_radius=0.09,
                                      stroke_color="#C2F4F4", stroke_width=3).move_to(xy(x, 0.80))
                    for x in (-0.24, 0.24)])


def pinecone():
    cone = oval(1.10, 1.53, "#684232", edge="#C28B62")
    scales = VGroup(*[
        path([(x - 0.14, y + 0.07), (x, y - 0.07), (x + 0.14, y + 0.07)], "#D19B71", 4)
        for y, centers in [(0.46, [0]), (0.21, [-0.18, 0.18]), (-0.07, [-0.27, 0, 0.27]),
                           (-0.34, [-0.14, 0.14]), (-0.55, [0])]
        for x in centers
    ])
    return VGroup(cone, scales)


def toy(color="#8BA274"):
    legs = VGroup(*[panel(0.22, h, color, xy(x, -0.30), radius=0.08, edge=INK)
                    for x, h in [(-0.42, 0.53), (-0.16, 0.43), (0.38, 0.43), (0.62, 0.54)]])
    tail = solid([(-0.42, 0.18), (-1.15, 0.38), (-0.78, 0.08), (-0.40, -0.12)], color, INK)
    body = oval(1.40, 0.60, color, edge=INK, stroke=3)
    head = oval(0.62, 0.45, color, xy(0.70, 0.36), edge=INK, stroke=3)
    return VGroup(legs, tail, body, head, Dot(xy(0.83, 0.40), radius=0.04, color=INK))


def prohibition(mob, radius=0.82):
    center = mob.get_center()
    return VGroup(Circle(radius=radius, color=RED, stroke_width=7).move_to(center),
                  Line(center + xy(-0.58, 0.58) * radius / 0.82,
                       center + xy(0.58, -0.58) * radius / 0.82, color=RED, stroke_width=7))


def rolling_pin():
    axle = panel(0.23, 4.08, "#BA8A59", radius=0.10, edge=INK)
    barrel = panel(0.66, 2.96, "#D5A773", radius=0.19, edge="#8B6140", stroke=4)
    grain = path([(-0.12, -1.29), (-0.07, -0.2), (-0.13, 1.29)], "#F3CEA1", 5)
    return VGroup(axle, barrel, grain)


def dust():
    motes = VGroup()
    for i in range(13):
        mote = Dot(xy(-5.8 + 11.6 * (i % 7) / 6, -2.36 + 4.7 * (i * 7 % 13) / 12),
                   radius=0.029 + 0.012 * (i % 3), color=PAPER).set_opacity(0.26)
        bob(mote, amp=0.16, speed=0.65 + i * 0.05, seed=i)
        motes.add(mote)
    return motes


class S01Hook(TitleCard, SpokenScene):
    TITLE = "Parent Guide: Make a Fossil Print"
    LESSON = "Make a Fossil Print"

    def construct(self):
        dish = plate()
        specimen = shell().scale(1.18).move_to(SINGLE + UP * 0.32)
        mark = impression(shell, SINGLE, 1.04)
        title = fit_text(self.TITLE, max_w=12, size=42, font=TITLE_FONT).move_to(xy(-0.12, 3.25))
        self.add(tabletop(), dish, dust(), title, specimen)
        self.at("dent in clay")
        self.play(specimen.animate.scale(0.88).move_to(mark.get_center()), run_time=0.65)
        self.add(mark)
        specimen.set_z_index(2)
        self.play(specimen.animate.scale(1.13).shift(UP * 0.26), FadeOut(title), run_time=0.57)
        self.play(specimen.animate.shift(RIGHT * 4.1 + UP * 0.55), run_time=1.32)
        self.at("in about 30")
        label = cue_text("Hollow print = mold", color=GOLD)
        self.play(FadeIn(label), Create(gloss(mark.detail)),
                  specimen.animate.shift(LEFT * 0.45 + UP * 0.63), run_time=1.65)
        self.at("make fossil prints")
        self.play(Rotate(specimen, angle=-0.36), run_time=1.85)
        self.at("turn those prints")
        self.play(Create(gloss(specimen.detail)), run_time=1.55)
        self.finish()


class S02Payoff(SpokenScene):
    def construct(self):
        pos = [xy(-4.24, -0.1), xy(0, -0.1), xy(4.24, -0.1)]
        marks = [impression(shell, pos[0], 0.87), impression(leaf, pos[1], 0.87),
                 tracks().scale(0.93).move_to(pos[2])]
        original = VGroup(plate(), impression(shell, SINGLE, 1.04))
        side_plates = [plate(p, 0.73) for p in pos]
        self.add(tabletop(), original)
        self.at("hands")
        self.play(Transform(original, VGroup(side_plates[0], marks[0])),
                  FadeIn(side_plates[1], shift=UP * 0.3), FadeIn(side_plates[2], shift=UP * 0.3),
                  FadeIn(marks[1]), FadeIn(marks[2]), run_time=0.95)
        self.remove(original)
        self.add(side_plates[0], marks[0])
        ring = Circle(radius=0.93, stroke_width=13, color=SHELL, fill_color="#1F2428", fill_opacity=0.30)
        handle = Line(xy(0.64, -0.67), xy(1.27, -1.30), color=SHELL, stroke_width=22)
        lens = VGroup(ring, handle).shift(pos[0] + LEFT * 0.20)
        self.at("looking closely")
        label = cue_text("Look closely")
        self.play(FadeIn(label), FadeIn(lens, shift=LEFT * 0.5), run_time=1.15)
        self.play(lens.animate.shift(RIGHT * 0.45 + UP * 0.51), run_time=1.65)
        self.at("match ridges")
        self.play(lens.animate.shift(RIGHT * 0.38 + DOWN * 0.54), run_time=0.73)
        self.at("leaf veins")
        self.play(lens.animate.shift(RIGHT * 3.65), run_time=0.78)
        self.at("and footprints")
        self.play(lens.animate.shift(RIGHT * 4.12), run_time=1.50)
        self.at("making a guess")
        second_label = cue_text("Guess and check", GOLD)
        self.play(swap(label, second_label), lens.animate.shift(UP * 0.43), run_time=0.85)
        self.play(lens.animate.shift(LEFT * 3.75 + UP * 0.10), run_time=2.7)
        self.at("practice patience")
        self.play(FadeOut(lens), FadeOut(second_label), run_time=0.55)
        cast = shell(cast=True).scale(0.9).move_to(xy(-4.24, 2.38))
        self.play(FadeIn(cast, shift=DOWN * 0.45), run_time=0.64)
        self.play(cast.animate.rotate(0.24).shift(RIGHT * 0.75), run_time=1.40)
        self.finish()


class S03Materials(SpokenScene):
    def construct(self):
        adult = person().scale(1.13).move_to(xy(-3.62, 1.26))
        child = person(adult=False).scale(0.81).move_to(xy(-1.85, -1.55))
        lid = panel(2.85, 0.48, TEAL, xy(3.15, 2.50), edge="#81D6D6", stroke=4)
        tub = panel(2.59, 1.22, "#357780", xy(3.15, 1.07), edge=TEAL, stroke=4)
        little_shell = shell().scale(0.39).move_to(xy(3.15, 1.70))
        parent_hand = hand().scale(0.75).move_to(xy(1.41, 2.45))
        self.add(tabletop(False), adult, child)
        self.at("stay with your")
        self.play(adult.animate.shift(DOWN * 0.19), child.animate.shift(UP * 0.13), run_time=1.8)
        self.at("keep all small")
        self.play(FadeIn(tub), FadeIn(lid), FadeIn(little_shell), FadeIn(parent_hand), run_time=0.6)
        self.play(little_shell.animate.shift(DOWN * 0.70), run_time=0.57)
        little_shell.set_z_index(-1)
        self.play(lid.animate.shift(DOWN * 0.90), parent_hand.animate.shift(DOWN * 0.85), run_time=1.08)
        safe_box = VGroup(tub, lid, little_shell)
        self.play(safe_box.animate.shift(UP * 0.48 + RIGHT * 1.62), FadeOut(parent_hand), run_time=1.02)
        self.at("cover the table")
        paper = newspaper()
        self.play(FadeOut(safe_box), FadeOut(child), FadeIn(paper, shift=DOWN * 0.57),
                  adult.animate.scale(0.86).move_to(xy(-4.9, 1.39)), run_time=1.8)
        self.at("store bought modeling")
        tray = plate(xy(0, -0.10), 0.92, clay=False)
        clay = oval(2.15, 1.57, CLAY, xy(0, 0.05), edge=CLAY_LIGHT, stroke=5)
        self.play(FadeIn(tray, shift=UP * 0.32), run_time=0.6)
        self.play(FadeIn(clay, scale=0.55, shift=UP * 0.46), run_time=1.22)
        self.play(clay.animate.stretch(1.13, 0).stretch(0.93, 1), run_time=0.74)
        self.at("skip homemade")
        dough = oval(1.20, 0.91, PAPER, xy(4.55, 0.21), edge="#9E8262")
        no_dough = prohibition(dough, 0.77)
        self.play(FadeIn(dough, shift=UP * 0.33), Create(no_dough), run_time=0.9)
        self.play(FadeOut(dough, shift=RIGHT * 0.55), FadeOut(no_dough, shift=RIGHT * 0.55), run_time=0.65)
        self.at("gather empty clean")
        clean = shell().scale(0.71).move_to(xy(3.84, 1.13))
        cone = pinecone().scale(0.84).move_to(xy(4.90, -1.18))
        model = toy().scale(0.72).move_to(xy(2.95, -1.47))
        self.play(FadeIn(clean, shift=UP * 0.33), run_time=1.70)
        self.at("pinecone and toy")
        self.play(FadeIn(cone, shift=LEFT * 0.32), run_time=0.60)
        self.play(FadeIn(model, shift=UP * 0.35), run_time=1.08)
        self.at("discard cracked shells")
        crack = path([(-0.15, 0.66), (0.02, 0.27), (-0.22, 0.21), (-0.17, -0.48)], INK, 5)
        broken = VGroup(shell(), crack).scale(0.57).move_to(xy(-4.65, -0.66))
        self.play(FadeIn(broken), run_time=0.55)
        self.play(FadeOut(broken, shift=LEFT * 1.35), run_time=1.05)
        self.at("choose leaves from")
        known = leaf().scale(0.70).move_to(xy(-3.72, -1.28))
        ivy = VGroup(*[leaf().scale(0.40).rotate(angle).move_to(xy(x, y))
                       for x, y, angle in [(0, 0.30, 0), (-0.46, -0.1, 0.76), (0.46, -0.1, -0.76)]])
        ivy.move_to(xy(-5.12, -1.48))
        no_ivy = prohibition(ivy, 0.81)
        self.play(FadeIn(known, shift=RIGHT * 0.50), run_time=1.57)
        self.at("avoid poison ivy")
        self.play(FadeIn(ivy), Create(no_ivy), run_time=0.62)
        self.play(FadeOut(ivy), FadeOut(no_ivy), run_time=0.57)
        self.at("never taste plants")
        self.play(FadeIn(cue_text("Never taste plants or clay", RED)), adult.animate.shift(RIGHT * 0.31), run_time=1.42)
        self.finish()


class S04PressMold(SpokenScene):
    def construct(self):
        ball = oval(2.15, 1.57, CLAY, SINGLE + UP * 0.15, edge=CLAY_LIGHT, stroke=5)
        dish = plate(clay=False)
        hands = VGroup(hand().rotate(-PI / 2).move_to(xy(-1.60, -0.07)),
                       hand().flip(UP).rotate(PI / 2).move_to(xy(1.60, -0.07)))
        self.add(tabletop(), dish, ball)
        self.at("your child need")
        self.play(FadeIn(hands, scale=1.14), run_time=0.45)
        self.play(ball.animate.stretch(0.82, 0).stretch(1.15, 1),
                  hands[0].animate.shift(RIGHT * 0.35), hands[1].animate.shift(LEFT * 0.35),
                  rate_func=there_and_back, run_time=1.51)
        self.play(ball.animate.stretch(1.16, 0).stretch(0.83, 1),
                  hands.animate.shift(DOWN * 0.25), run_time=1.5)
        self.at("use a rolling pin")
        pin = rolling_pin().move_to(xy(-2.0, -0.3))
        self.play(FadeOut(hands), FadeIn(pin, shift=RIGHT * 0.61), run_time=0.85)
        self.play(pin.animate.shift(RIGHT * 1.20), run_time=1.9)
        self.at("flatten the clay")
        flat = plate()
        self.play(pin.animate.shift(RIGHT * 3.08), Transform(ball, flat[3].copy()), run_time=1.78)
        self.add(flat[2])
        self.bring_to_front(ball, pin)
        self.play(FadeOut(pin, shift=RIGHT * 0.48), run_time=0.5)
        self.at("about 2 cm")
        zoom = VGroup(oval(1.95, 0.68, CLAY_EDGE, xy(4.27, -0.24), edge=CLAY_LIGHT),
                      oval(1.95, 0.49, CLAY, xy(4.27, 0.03), edge=CLAY_LIGHT))
        brace = VGroup(Line(xy(5.51, -0.47), xy(5.51, 0.20), color=GOLD, stroke_width=4),
                       Line(xy(5.39, -0.47), xy(5.62, -0.47), color=GOLD, stroke_width=4),
                       Line(xy(5.39, 0.20), xy(5.62, 0.20), color=GOLD, stroke_width=4))
        height = T("≈ 2 cm", 31, GOLD).move_to(xy(4.67, 0.97))
        spec = shell().scale(1.17).move_to(SINGLE + UP * 0.32)
        self.play(FadeIn(zoom), Create(brace), FadeIn(height), run_time=0.68)
        self.play(FadeIn(spec, scale=1.14), run_time=0.80)
        self.at("press the shell")
        mark = impression(shell, SINGLE, 1.04)
        self.play(FadeOut(zoom), FadeOut(brace), FadeOut(height),
                  spec.animate.scale(0.89).move_to(mark.get_center()), run_time=0.99)
        self.add(mark)
        spec.set_z_index(2)
        self.at("lift it straight")
        self.play(spec.animate.scale(1.13).shift(UP * 0.27), run_time=0.71)
        self.play(spec.animate.shift(RIGHT * 4.1 + UP * 0.55), run_time=1.15)
        self.at("hollow print is")
        arrow = Arrow(xy(-3.12, -2.15), xy(-0.58, -0.74), buff=0.06, color=GOLD, stroke_width=4)
        self.play(Create(arrow), FadeIn(cue_text("Mold", GOLD)), run_time=0.89)
        self.finish()


class S05TradeGuess(SpokenScene):
    def construct(self):
        world, specimens, marks = pair_world(True)
        dishes = world[1]
        left = VGroup(dishes[0], marks[0])
        right = VGroup(dishes[1], marks[1])
        left_start, right_start = PAIR
        self.add(world[0], left, right)
        self.at("make some prints")
        cover = oval(2.35, 1.77, CLAY, left_start + UP * 0.06, stroke=0)
        self.add(cover)
        self.play(FadeOut(cover), run_time=1.50)
        self.at("swap plates")
        self.play(left.animate(path_arc=-0.59).shift(right_start - left_start),
                  right.animate(path_arc=-0.59).shift(left_start - right_start), run_time=1.02)
        question = cue_text("What made this print?", GOLD)
        self.at("what made this")
        self.play(FadeIn(question), run_time=0.47)
        next_question = cue_text("What clue helped you guess?", GOLD)
        self.at("what clue helped")
        self.play(swap(question, next_question), run_time=0.66)
        self.at("match the prints")
        specimens[0].shift(RIGHT * 6.4)
        specimens[1].shift(LEFT * 6.4)
        self.play(FadeOut(next_question), FadeIn(specimens, shift=DOWN * 0.46), run_time=1.02)
        shell_trace = gloss(specimens[0].detail, width=9)
        self.play(Create(shell_trace), Create(gloss(marks[0].detail, width=9)), run_time=0.94)
        self.at("ridged scallop shell")
        sea = cue_text("Sea", "#9BD9EB").shift(RIGHT * 3.20)
        self.play(FadeIn(sea),
                  VGroup(specimens[0], shell_trace).animate.shift(RIGHT * 0.53 + UP * 0.14), run_time=0.73)
        leaf_trace = gloss(specimens[1].detail, width=9)
        self.play(Create(leaf_trace), Create(gloss(marks[1].detail, width=9)), run_time=1.52)
        self.at("leaf points to")
        land = cue_text("Land with plants", "#C7ECB0").shift(LEFT * 3.20)
        self.play(FadeIn(land), VGroup(specimens[1], leaf_trace).animate.shift(LEFT * 0.52 + UP * 0.18), run_time=1.65)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world, objects, _ = pair_world()
        self.add(*world[:2])
        self.at("quick prediction")
        self.play(FadeIn(objects[0], shift=DOWN * 0.47, scale=0.86), run_time=2.44)
        self.at("ridged shell")
        highlight = gloss(objects[0].detail)
        self.play(Create(highlight), run_time=0.66)
        self.at("a leaf with")
        self.play(FadeIn(objects[1], shift=DOWN * 0.45, scale=0.87), run_time=0.66)
        vein = gloss(objects[1].detail)
        self.play(Create(vein), run_time=1.04)
        self.at("which details")
        q = question_card(QUESTION, **QUESTION_STYLE)
        self.play(FadeIn(q), run_time=0.68)
        self.at("after you lift")
        self.play(FadeOut(highlight), FadeOut(vein), run_time=0.40)
        self.play(objects.animate(rate_func=there_and_back).shift(UP * 0.66), run_time=2.64)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_STYLE
    SECONDS = 4.5
    RING_AT = (5.96, -3.06, 0)

    def backdrop(self):
        return pair_world()[0]

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, run = countdown(self.SECONDS, center=self.RING_AT, radius=0.61)
        self.add(ring)
        self.play(run)


def river_cliff():
    layers = VGroup(
        Polygon(xy(-5.7, 0.95), xy(1.73, 0.95), xy(2.97, 0.30), xy(3.35, -2.53), xy(-5.7, -2.53),
                stroke_width=0, fill_color="#9A6B48", fill_opacity=1),
        Polygon(xy(-5.7, 0.89), xy(1.82, 0.89), xy(2.92, 0.34), xy(3.06, -0.22),
                xy(-5.7, -0.31), stroke_width=0, fill_color="#CAA576", fill_opacity=1),
        Polygon(xy(-5.7, -1.19), xy(3.12, -1.07), xy(3.35, -2.53), xy(-5.7, -2.53),
                stroke_width=0, fill_color="#BD9064", fill_opacity=1),
        Line(xy(-5.7, 0.96), xy(1.82, 0.96), color="#8CAA6B", stroke_width=11),
        Line(xy(-5.65, -1.23), xy(3.1, -1.12), color="#E3BA83", stroke_width=3),
    )
    river = solid([(3.0, -1.16), (4.5, -1.09), (5.91, -1.17), (5.91, -2.47),
                   (4.45, -2.53), (3.33, -2.51)], WATER, "#76B9C4")
    fossils = VGroup(*[shell(cast=True).scale(s).rotate(a).move_to(xy(x, y))
                       for x, y, s, a in [(-4.1, 0.32, 0.31, -0.32), (-2.41, 0.31, 0.43, 0.18),
                                          (-0.62, 0.39, 0.31, 0.08), (1.08, 0.32, 0.28, -0.45),
                                          (-3.29, -1.79, 0.34, 0.34), (0.44, -1.75, 0.40, -0.21)]])
    return VGroup(layers, river), fossils


class S08Reveal(SpokenScene):
    def construct(self):
        world, objects, marks = pair_world()
        self.add(world)
        self.at("press and lift")
        self.play(*(obj.animate.scale(0.86).move_to(mark) for obj, mark in zip(objects, marks)), run_time=0.66)
        self.add(marks)
        objects.set_z_index(2)
        self.play(*(obj.animate.scale(1 / 0.86).move_to(at + SPECIMEN_OFFSET)
                    for obj, at in zip(objects, PAIR)), run_time=1.04)
        self.at("compare the shell")
        traces = VGroup(*(gloss(m.detail) for m in (objects[0], marks[0], objects[1], marks[1])))
        self.play(Create(traces[0]), Create(traces[1]), run_time=0.59)
        shell_and_ridge = VGroup(objects[0], traces[0])
        self.play(shell_and_ridge.animate.shift(LEFT * 0.44 + UP * 0.20), run_time=0.85)
        self.at("leaf veins")
        self.play(Create(traces[2]), Create(traces[3]), run_time=0.57)
        self.at("their hollow prints")
        self.play(FadeOut(traces), run_time=0.40)
        self.play(objects[1].animate.shift(RIGHT * 0.47 + UP * 0.25), run_time=0.90)
        self.at("in Virginia")
        cliff, fossils = river_cliff()
        anchor = objects[0].copy().set_z_index(3)
        self.add(anchor)
        self.play(FadeOut(world), FadeOut(marks), FadeIn(cliff, shift=UP * 0.22),
                  Transform(anchor, fossils[1].copy().set_z_index(3)), run_time=1.05)
        self.remove(anchor)
        self.add(fossils[1])
        self.at("fossil scallops")
        other_fossils = VGroup(fossils[0], *fossils[2:])
        heading = cue_text("Virginia river cliffs", y=2.87, size=38)
        schematic = scope_tag(size=25).move_to(xy(5.55, -3.28))
        self.play(FadeIn(heading), FadeIn(schematic), FadeIn(other_fossils, lag_ratio=0.16), run_time=1.15)
        self.at("a shallow sea")
        # Restore the continuous seabed across the modern river cut before adding water.
        seabed = Polygon(xy(1.72, 0.95), xy(5.91, 0.95), xy(5.91, -2.53), xy(3.34, -2.53),
                          xy(2.96, 0.30), fill_color="#9A6B48", fill_opacity=1, stroke_width=0)
        sea = Polygon(xy(-5.7, 0.95), xy(5.91, 0.95), xy(5.91, 2.18), xy(-5.7, 2.18),
                      fill_color=WATER, fill_opacity=1, stroke_color="#7DC6D4", stroke_width=3)
        sea_label = cue_text("Shallow sea", "#AEE3EC", y=2.87, size=38)
        self.play(FadeOut(cliff[1]), FadeIn(seabed), run_time=0.47)
        self.play(swap(heading, sea_label), GrowFromEdge(sea, DOWN), run_time=1.00)
        swimmers = VGroup(*[shell().scale(0.36).rotate(angle).move_to(xy(x, 1.35))
                            for x, angle in [(-3.9, 0.2), (-1.2, 0.06), (2.3, -0.14)]])
        self.at("the scallops lived")
        self.play(FadeIn(swimmers, shift=UP * 0.2, lag_ratio=0.21), run_time=1.45)
        self.finish()


def outdoor():
    sky = Rectangle(width=13.56, height=7.52, fill_color="#31494C", fill_opacity=1, stroke_width=0)
    hills = solid([(-6.71, -0.42), (-4.68, 0.51), (-2.1, 0.29), (0.0, 0.88), (2.0, 0.35),
                   (4.10, 0.81), (6.70, 0.07), (6.70, -3.68), (-6.70, -3.68)], "#49624F", "#49624F")
    # Keep foreground silhouettes fully inside the safe rectangle.
    hills.stretch_to_fit_width(13.30).stretch_to_fit_height(3.88).move_to(xy(0, -0.91))
    bench = panel(9.56, 5.26, WOOD, xy(-0.54, -0.15), radius=0.17, edge="#967058", stroke=0)
    front = Line(xy(-5.22, -2.79), xy(4.17, -2.79), color="#967058", stroke_width=5)
    return VGroup(sky, hills, bench, front).set_z_index(-4)


def plaster_bag():
    return VGroup(panel(1.35, 1.63, PAPER, radius=0.16, edge="#957E61", stroke=4),
                  panel(1.15, 0.48, "#EAB788", xy(0, 0.10), radius=0.10, stroke=0),
                  Line(xy(-0.53, 0.62), xy(0.53, 0.62), color="#957E61", stroke_width=4))


def safety_world(protected=True):
    adult = person(protected=protected).scale(0.82).shift(xy(-3.69, 1.64))
    mark = impression(shell, SINGLE, 1.04)
    dish = plate()
    bag = plaster_bag().scale(0.88).move_to(xy(3.53, -0.55))
    return outdoor(), adult, dish, mark, bag


def heat_waves(at):
    return VGroup(*[path([(x, -0.28), (x + 0.11, 0.02), (x - 0.11, 0.31), (x, 0.59)],
                         "#FFC088", 5) for x in (-0.36, 0, 0.36)]).move_to(at)


class S09CastOptional(SpokenScene):
    def construct(self):
        outside, adult, dish, mark, bag = safety_world(False)
        inside = tabletop()
        self.add(inside, dish, mark)
        self.at("make a cast")
        self.play(FadeIn(adult, shift=UP * 0.55), run_time=1.12)
        label = cue_text("Adult only", TEAL)
        self.at("only an adult")
        self.play(FadeIn(bag, shift=DOWN * 0.35), FadeIn(label), run_time=1.60)
        self.at("work outdoors")
        self.play(FadeOut(inside), FadeIn(outside), run_time=1.52)
        child = person(adult=False).scale(0.56).move_to(xy(5.27, 0.76))
        pet = toy("#D7A377").scale(0.67).move_to(xy(5.28, -1.30))
        self.at("keep children and")
        self.play(FadeIn(child, shift=RIGHT * 0.38), FadeIn(pet, shift=RIGHT * 0.38), run_time=1.13)
        self.play(child.animate.shift(RIGHT * 0.53), pet.animate.shift(RIGHT * 0.47), run_time=0.95)
        self.at("wear a NIOSH")
        self.play(FadeOut(child), FadeOut(pet), FadeOut(label), run_time=0.36)
        resp = mask().scale(0.82, about_point=ORIGIN).shift(xy(-3.69, 1.64))
        goggles = glasses().scale(0.82, about_point=ORIGIN).shift(xy(-3.69, 1.64))
        face_glove = hand(TEAL).scale(0.79).rotate(-0.5).move_to(xy(-3.65, -0.46))
        safety = cue_text("NIOSH-approved dust mask", size=31)
        self.play(FadeIn(resp, shift=UP * 0.36), FadeIn(safety), run_time=0.94)
        self.at("eye protection")
        eyes = cue_text("Eye protection", size=31)
        self.play(FadeIn(goggles, shift=UP * 0.19), swap(safety, eyes), run_time=0.63)
        self.at("and gloves")
        gloves_label = cue_text("Gloves", size=31)
        self.play(FadeIn(face_glove, shift=RIGHT * 0.56), swap(eyes, gloves_label), run_time=0.74)
        self.play(face_glove.animate.shift(DOWN * 0.44 + RIGHT * 0.61), run_time=0.68)
        self.at("never put any")
        raised_hand = hand(PAPER).scale(0.97).move_to(xy(4.96, 0.68))
        no_hand = prohibition(raised_hand, 0.94)
        self.play(FadeIn(raised_hand), Create(no_hand), FadeOut(gloves_label), run_time=1.20)
        label = cue_text("Keep skin out of plaster", "#FF9A8D", size=31)
        self.play(FadeIn(label), run_time=0.51)
        self.at("it can get hot")
        cup = oval(1.11, 0.53, PLASTER, xy(4.97, -1.63), edge="#A48163", stroke=4)
        heat = heat_waves(xy(4.96, -0.87))
        self.play(FadeIn(cup), Create(heat), run_time=0.77)
        self.finish()


def cast_wall():
    return Ellipse(width=3.32, height=2.75, color=CLAY_EDGE, stroke_width=24).move_to(SINGLE + UP * 0.06)


def plaster_cup():
    body = Polygon(xy(-0.53, 0.17), xy(0.53, 0.17), xy(0.34, -0.68), xy(-0.34, -0.68),
                   color="#AA936D", stroke_width=3, fill_color=PAPER, fill_opacity=1)
    return VGroup(body, oval(1.12, 0.48, PLASTER, xy(0, 0.17), edge="#AA936D", stroke=3))


class S10Safety(SpokenScene):
    def construct(self):
        outside, adult, dish, mark, bag = safety_world()
        glove = hand(TEAL).scale(0.76).move_to(xy(-3.59, -0.87))
        self.add(outside, adult, dish, mark, bag, glove)
        self.at("build a clay wall")
        wall = cast_wall()
        self.play(Create(wall), glove.animate.move_to(xy(-2.42, -0.93)), run_time=1.76)
        wall_label = cue_text("Clay wall ≈ 2 cm", GOLD, size=31)
        self.play(FadeIn(wall_label), run_time=0.77)
        self.at("mix the plaster")
        cup = plaster_cup().move_to(xy(2.88, 1.46))
        spoon = panel(0.16, 1.06, "#99724E", xy(3.06, 1.92), radius=0.07, edge="#C4A078")
        open_bag = oval(0.87, 0.18, INK, bag.get_top() + DOWN * 0.15, edge=PAPER, stroke=3)
        self.play(FadeIn(open_bag), FadeOut(wall_label), FadeIn(cup, shift=LEFT * 0.3), run_time=0.46)
        self.play(FadeIn(spoon), run_time=0.28)
        self.play(Rotate(spoon, -0.66, about_point=xy(2.9, 1.48), rate_func=there_and_back), run_time=0.90)
        self.at("pour it into")
        self.play(FadeOut(spoon), cup.animate.rotate(0.88).shift(LEFT * 1.56), run_time=0.56)
        stream = path([(1.05, 1.56), (0.58, 0.86), (0.31, 0.02)], PLASTER, 12)
        fill = oval(2.65, 2.05, PLASTER, SINGLE + UP * 0.07, edge="#CDBB9C", stroke=3)
        self.play(Create(stream), FadeIn(fill, scale=0.2), run_time=0.94)
        self.at("keep children back")
        warm = heat_waves(xy(0.15, 1.25))
        self.play(FadeOut(stream), FadeOut(cup, shift=RIGHT * 0.62), FadeIn(warm), run_time=0.67)
        self.play(FadeOut(warm, shift=UP * 0.80), run_time=1.61)
        self.at("it hardens in")
        time_label = cue_text("Hardens in about 30–60 min", GOLD, size=31)
        self.play(FadeIn(time_label), fill.animate.set_fill("#E9DFCA"), run_time=1.40)
        self.at("leave it overnight")
        moon = Difference(Circle(radius=0.42), Circle(radius=0.36).shift(RIGHT * 0.18),
                          fill_color=PLASTER, fill_opacity=1, stroke_width=0).move_to(xy(5.2, 2.65))
        night = Rectangle(width=13.56, height=7.52, fill_color="#282E48", fill_opacity=0.62,
                          stroke_width=0).set_z_index(5)
        night_label = cue_text("Dry overnight", size=34)
        self.play(FadeIn(night), FadeIn(moon.set_z_index(6)), swap(time_label, night_label), run_time=0.92)
        self.play(FadeOut(night), FadeOut(moon, shift=UP * 0.60), FadeOut(night_label), run_time=0.83)
        self.at("then peel off")
        cast = shell(cast=True).scale(1.04).move_to(SINGLE + UP * 0.07)
        mold = VGroup(dish, mark)
        self.remove(fill)
        self.add(cast)
        cast.set_z_index(2)
        wall.set_z_index(2)
        mold.set_z_index(0)
        glove.set_z_index(3)
        self.play(wall.animate.stretch(0.36, 0).rotate(-0.27).shift(LEFT * 1.60 + UP * 0.32),
                  glove.animate.shift(UP * 0.44), cast.animate.shift(RIGHT * 0.40 + UP * 0.22),
                  FadeOut(bag), FadeOut(open_bag), run_time=0.62)
        self.play(mold.animate.shift(LEFT * 2.5), cast.animate.scale(1.22).move_to(xy(3.14, -0.20)),
                  FadeOut(glove), FadeOut(adult), FadeOut(wall, shift=UP * 0.47), run_time=0.75)
        self.at("the raised cast")
        self.play(FadeIn(cue_text("Hollow mold", GOLD).shift(LEFT * 2.5)),
                  FadeIn(cue_text("Raised cast").shift(RIGHT * 3.14)),
                  cast.animate.rotate(0.13), run_time=0.79)
        self.finish()


def sand_tub():
    back = panel(9.72, 4.31, "#46686A", xy(0, -0.19), radius=0.25, edge="#94B7B1", stroke=5)
    base = panel(9.12, 3.47, SAND, xy(0, -0.30), radius=0.22, edge="#E0BC89", stroke=3)
    upper = panel(8.94, 1.65, "#D0AB78", xy(0, 0.53), radius=0.20)
    flecks = VGroup(*[Line(xy(x, y), xy(x + 0.12, y + 0.015), color="#916848", stroke_width=2)
                      for row, y in enumerate((-1.83, -1.17, -0.31, 0.44, 1.02))
                      for x in np.linspace(-4.14, 4.04, 15) + (row % 2) * 0.08])
    return VGroup(back, base, upper, flecks)


def brush():
    stick = panel(2.33, 0.17, "#BC7650", xy(0.36, 0), radius=0.08, edge="#F0AD73")
    ferrule = panel(0.53, 0.25, "#D4BA92", xy(-0.70, 0), radius=0.07, edge=INK)
    bristles = solid([(-1.47, -0.17), (-0.93, -0.13), (-0.93, 0.13), (-1.43, 0.20)],
                     "#E8CD9B", "#8B694F")
    return VGroup(stick, ferrule, bristles)


class S11Wrap(SpokenScene):
    def construct(self):
        world, _, marks = pair_world()
        shell_plate = VGroup(world[1][0], marks[0]).shift(xy(0.77, 1.0))
        leaf_plate = VGroup(world[1][1], marks[1]).shift(xy(-0.77, 1.0))
        self.add(world[0], shell_plate, leaf_plate)
        self.at("skip the plaster")
        self.play(shell_plate.animate.move_to(PAIR[0]), run_time=1.1)
        self.at("sort prints")
        water = cue_text("Water", "#AEE3EC").shift(LEFT * 3.20)
        land = cue_text("Land", "#C7ECB0").shift(RIGHT * 3.20)
        self.play(leaf_plate.animate.move_to(PAIR[1]), FadeIn(water), FadeIn(land), run_time=1.84)
        self.at("try a sand dig")
        tub = sand_tub()
        self.play(FadeOut(shell_plate), FadeOut(leaf_plate), FadeOut(water), FadeOut(land),
                  FadeIn(tub, shift=UP * 0.38), run_time=1.38)
        self.at("lightly damp")
        adult = person().scale(0.66).move_to(xy(-5.65, 1.75))
        self.play(FadeIn(adult, shift=UP * 0.27), run_time=1.55)
        self.at("berry shells")
        buried_shell = shell().scale(0.79).move_to(xy(-2.13, -1.21))
        buried_leaf = impression(leaf, xy(1.93, 0.40), 0.69)
        self.play(FadeIn(buried_shell, shift=DOWN * 0.55), run_time=0.63)
        self.at("leaf prints")
        self.play(FadeIn(buried_leaf), run_time=0.70)
        self.play(buried_shell.animate.set_opacity(0.36), buried_leaf.animate.set_opacity(0.39), run_time=1.1)
        self.at("brush gently")
        tool = brush().rotate(0.27).move_to(xy(2.32, 1.2))
        self.play(FadeIn(tool, shift=LEFT * 0.7), run_time=0.51)
        self.play(tool.animate.shift(LEFT * 0.61 + DOWN * 0.40), buried_leaf.animate.set_opacity(1), run_time=1.0)
        self.play(tool.animate.shift(LEFT * 3.02 + DOWN * 1.23), buried_shell.animate.set_opacity(1), run_time=1.23)
        self.at("wash hands")
        stream = VGroup(*(path([(x, 0.70), (x + 0.1, -0.01), (x + 0.06, -0.71)], "#8BD8E6", 7)
                          for x in (-0.26, 0.03, 0.28)))
        soap = panel(1.92, 1.10, TEAL, xy(-3.43, -0.59), radius=0.28, edge="#A0E0D8", stroke=5)
        bubbles = VGroup(*[Circle(radius=r, stroke_width=3, color=PAPER).move_to(xy(x, y))
                           for x, y, r in [(-1.33, -0.32, 0.19), (-1.07, -0.03, 0.15),
                                           (-0.73, 0.28, 0.22), (0.51, -0.52, 0.14)]])
        hands = VGroup(hand().flip(UP).rotate(1.0).scale(1.36).move_to(xy(-0.98, -0.71)),
                       hand().rotate(-1.0).scale(1.36).move_to(xy(0.92, -0.82)))
        self.play(FadeOut(tub), FadeOut(adult), FadeOut(tool), FadeOut(buried_shell), FadeOut(buried_leaf),
                  FadeIn(soap), FadeIn(hands), run_time=0.61)
        self.play(Create(stream), FadeIn(bubbles, shift=UP * 0.29), run_time=1.52)
        self.at("your child used shapes")
        dish = plate()
        mark = impression(shell, SINGLE, 1.04)
        real = shell().scale(1.18).move_to(SINGLE + xy(4.1, 0.81))
        self.play(FadeOut(soap), FadeOut(stream), FadeOut(bubbles), FadeOut(hands),
                  FadeIn(dish), FadeIn(mark), FadeIn(real, shift=LEFT * 0.44), run_time=0.84)
        self.at("shapes as clues")
        self.play(Create(gloss(mark.detail)), Create(gloss(real.detail)), run_time=1.53)
        self.finish()


class S12End(EndCard):
    LINE = "Fossil prints save shapes that reveal past life and places."
