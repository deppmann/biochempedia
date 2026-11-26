"""Which Similarities Reveal Relatives? Schematic illustrations for Building a Tree of Life.

Color map: BLUE whale, GREEN hippo, GREY tuna and resemblance by function,
TEAL inherited evidence, GOLD ancestral branch points.
"""

from bp_parts import *
from bp_style import EndCard


WATER = "#28495C"
RIVER = "#273F3B"
ROCK = "#564439"
PAPER = "#253541"
QUESTION = "Which trail would you follow?"
RULE = "Trace shared derived traits to branch points to find the closest relatives."


def pt(x, y):
    return np.array([x, y, 0.0])


def silhouette(start, segments, color, opacity=0.50):
    form = VMobject(stroke_color=color, stroke_width=3.5, fill_color=color, fill_opacity=opacity)
    form.start_new_path(pt(*start))
    for handle_a, handle_b, end in segments:
        form.add_cubic_bezier_curve_to(pt(*handle_a), pt(*handle_b), pt(*end))
    form.close_path()
    return form


def path(points, color=TEAL, width=5, opacity=1):
    line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    line.set_points_as_corners(points)
    return line


def plate(width, height, center, color, opacity=1):
    return RoundedRectangle(
        width=width, height=height, corner_radius=min(0.22, width / 2, height / 2),
        stroke_width=0, fill_color=color, fill_opacity=opacity,
    ).move_to(center)


def whale():
    body = silhouette((-2.05, 0.08), [
        ((-2.02, 0.70), (-0.95, 0.83), (-0.28, 0.67)),
        ((0.55, 0.64), (1.36, 0.33), (1.85, 0.20)),
        ((2.14, 0.42), (2.48, 0.57), (2.75, 0.52)),
        ((2.64, 0.29), (2.45, 0.17), (2.26, 0.08)),
        ((2.51, -0.02), (2.65, -0.16), (2.77, -0.34)),
        ((2.36, -0.43), (2.05, -0.29), (1.85, -0.05)),
        ((0.96, -0.18), (0.51, -0.68), (-0.64, -0.63)),
        ((-1.52, -0.61), (-2.10, -0.37), (-2.05, 0.08)),
    ], BLUE, 0.64)
    flipper = silhouette((-0.64, -0.23), [
        ((-0.35, -0.19), (0.22, -0.59), (0.46, -1.0)),
        ((0.06, -1.02), (-0.61, -0.75), (-0.64, -0.23)),
    ], BLUE, 0.78)
    mouth = ArcBetweenPoints(pt(-2.01, -0.08), pt(-1.08, -0.24), angle=0.23,
                             stroke_width=2.5, color=BG)
    return VGroup(body, flipper, mouth, Dot(pt(-1.23, 0.19), radius=0.064, color=BG))


def tuna():
    body = silhouette((-1.97, 0.00), [
        ((-1.50, 0.52), (-0.74, 0.75), (-0.42, 0.58)),
        ((-0.29, 0.77), (-0.05, 1.03), (0.18, 0.97)),
        ((0.12, 0.76), (0.32, 0.61), (0.44, 0.49)),
        ((1.06, 0.40), (1.59, 0.15), (1.82, 0.11)),
        ((2.07, 0.38), (2.32, 0.69), (2.67, 0.84)),
        ((2.53, 0.54), (2.41, 0.24), (2.33, 0.03)),
        ((2.44, -0.23), (2.55, -0.53), (2.68, -0.78)),
        ((2.35, -0.62), (2.07, -0.36), (1.82, -0.10)),
        ((0.97, -0.27), (0.48, -0.68), (-0.23, -0.61)),
        ((-1.05, -0.63), (-1.65, -0.37), (-1.97, 0.00)),
    ], GREY, 0.74)
    fin = silhouette((-0.91, -0.10), [
        ((-0.51, -0.03), (-0.08, -0.25), (0.36, -0.55)),
        ((-0.09, -0.59), (-0.68, -0.48), (-0.91, -0.10)),
    ], GREY, 0.81)
    return VGroup(body, fin, Dot(pt(-1.39, 0.12), radius=0.065, color=BG))


def hippo():
    legs = VGroup(*[
        plate(0.32, 1.08, pt(x, -0.65), GREEN, opacity)
        for x, opacity in [(-0.83, 0.44), (-0.48, 0.78), (0.66, 0.44), (1.0, 0.78)]
    ])
    body = silhouette((-1.87, -0.17), [
        ((-2.02, 0.20), (-1.80, 0.43), (-1.47, 0.45)),
        ((-1.46, 0.82), (-1.04, 0.95), (-0.82, 0.63)),
        ((-0.22, 1.04), (1.08, 1.11), (1.43, 0.47)),
        ((1.80, -0.13), (1.49, -0.69), (0.94, -0.69)),
        ((0.05, -0.86), (-0.59, -0.52), (-0.95, -0.35)),
        ((-1.28, -0.45), (-1.79, -0.42), (-1.87, -0.17)),
    ], GREEN, 0.70)
    ear = Circle(radius=0.156, stroke_width=2, color=GREEN, fill_color=GREEN, fill_opacity=0.7).move_to(pt(-0.94, 0.68))
    eye = Dot(pt(-1.25, 0.48), radius=0.06, color=BG)
    mouth = ArcBetweenPoints(pt(-1.85, -0.09), pt(-1.25, -0.18), angle=0.22,
                             stroke_width=2.5, color=BG)
    return VGroup(legs, body, ear, eye, mouth)


def opening_world():
    sea = plate(7.45, 5.58, pt(-2.25, 0.02), WATER)
    river = plate(4.18, 5.58, pt(3.72, 0.02), RIVER)
    waterline = VGroup(
        Line(pt(-5.67, 2.47), pt(1.16, 2.47), color=BLUE, stroke_width=2, stroke_opacity=0.48),
        Line(pt(1.91, -1.47), pt(5.53, -1.47), color=GREEN, stroke_width=2, stroke_opacity=0.48),
    )
    backdrop = VGroup(sea, river, waterline)
    animals = VGroup(
        whale().scale(1.02).move_to(pt(-1.78, 1.12)),
        tuna().scale(0.97).move_to(pt(-1.80, -1.16)),
        hippo().scale(0.89).move_to(pt(3.70, -0.03)),
    )
    labels = VGroup(*[
        T(name, 31, color).move_to(pt(*at))
        for (name, color), at in zip(
            [("whale", BLUE), ("tuna", TEXT), ("hippo", GREEN)],
            [(-5.15, 0.83), (-5.15, -1.16), (3.69, -2.08)],
        )
    ])
    return backdrop, animals, labels, scope_tag(size=28)


def shape_bracket(color=GREY):
    return DashedVMobject(
        path([pt(0.79, 1.09), pt(1.13, 1.09), pt(1.13, -1.10), pt(0.79, -1.10)], color, 4),
        num_dashes=14, dashed_ratio=0.61,
    )


def streamlines():
    return VGroup(*[
        ArcBetweenPoints(pt(-4.18, y), pt(0.55, y + dy), angle=ang, stroke_width=3, color=color)
        for y, dy, ang, color in [(2.19, 0.03, -0.16, BLUE), (0.12, -0.11, 0.14, BLUE),
                                  (-0.21, 0.03, -0.13, GREY), (-2.39, 0.09, 0.12, GREY)]
    ])


class S00Hook(SpokenScene):
    def construct(self):
        backdrop, animals, labels, tag = opening_world()
        self.add(backdrop, tag)
        self.at("a whale")
        self.play(FadeIn(animals[0], shift=LEFT * 0.58), run_time=0.95)
        self.at("like a tuna")
        self.play(FadeIn(animals[1], shift=LEFT * 0.57), run_time=0.58)
        self.at("than a hippo")
        self.play(FadeIn(animals[2], shift=LEFT * 0.62), run_time=0.86)
        self.play(LaggedStart(*[FadeIn(label) for label in labels], lag_ratio=0.32), run_time=0.72)
        question = T("?", 74, GOLD, weight=BOLD).move_to(pt(1.58, 1.87))
        self.at("so why does")
        self.play(GrowFromCenter(question), backdrop[1].animate.set_fill("#405945"), run_time=1.05)
        self.at("pair whale with hippo")
        link = DashedLine(pt(0.50, 1.87), pt(2.63, 1.87), color=GOLD, stroke_width=4)
        left_link = DashedLine(link.get_start(), pt(1.20, 1.87), color=GOLD, stroke_width=4, dash_length=0.12)
        right_link = DashedLine(pt(1.96, 1.87), link.get_end(), color=GOLD, stroke_width=4, dash_length=0.12)
        self.play(Create(left_link), Create(right_link),
                  animals[2][1].animate.set_fill(GREEN, opacity=0.93), run_time=1.20)
        self.at("shape offers")
        bracket = shape_bracket()
        self.play(Create(bracket), backdrop[0].animate.set_fill("#3e6070"),
                  backdrop[1].animate.set_fill(RIVER), run_time=1.25)
        self.at("but ancestry")
        self.play(bracket.animate.set_opacity(0.34), backdrop[0].animate.set_fill(WATER),
                  backdrop[1].animate.set_fill("#39544b"), run_time=1.29)
        kin = path([pt(-1.01, 1.94), pt(0.80, 2.64), pt(2.36, 2.64), pt(3.60, 1.39)], GOLD, 19, 0.65)
        self.play(Create(kin), run_time=1.62)
        self.at("which features travel")
        branch = path([pt(-0.83, -3.13), pt(0.22, -3.13), pt(0.91, -2.78)], GOLD, 5)
        self.play(
            Create(branch),
            FadeOut(question), FadeOut(left_link), FadeOut(right_link), FadeOut(bracket), FadeOut(kin),
            backdrop[1].animate.set_fill(RIVER),
            run_time=1.66,
        )
        self.finish()


class S01Title(TitleCard):
    TITLE = "Which Similarities Reveal Relatives?"
    LESSON = "Building a Tree of Life"

    def construct(self):
        backdrop, animals, labels, tag = opening_world()
        self.add(backdrop.set_opacity(0.19), animals.set_opacity(0.16), labels.set_opacity(0.11), tag.set_opacity(0.16))
        title = T("Which Similarities\nReveal Relatives?", 61, TEXT, font=TITLE_FONT,
                  line_spacing=0.85).move_to(pt(0, 0.55))
        lesson = T(self.LESSON, 30, TEAL).move_to(pt(0, -1.26))
        rule = Line(pt(-1.0, -1.82), pt(0.30, -1.82), color=GOLD, stroke_width=5)
        self.play(FadeIn(title), FadeIn(lesson), GrowFromCenter(rule), run_time=0.65)
        self.wait(0.62)
        self.play(
            ReplacementTransform(rule, path([pt(-1.0, -1.82), pt(0.30, -1.82), pt(1.12, -1.42)], GOLD, 5)),
            FadeOut(title), FadeOut(lesson), run_time=0.63,
        )
        self.wait(0.1)


class S02SameJob(SpokenScene):
    def construct(self):
        backdrop, animals, labels, tag = opening_world()
        self.add(backdrop, animals, labels, tag)
        flow = streamlines()
        self.at("both move through water")
        self.play(Create(flow),
                  animals[0].animate.shift(LEFT * 0.36), animals[1].animate.shift(LEFT * 0.36),
                  run_time=2.21)
        self.at("a smooth body")
        self.play(
            LaggedStart(*[ShowPassingFlash(m.copy().set_stroke(width=15), time_width=0.45) for m in flow],
                        lag_ratio=0.27),
            animals[0].animate.shift(RIGHT * 0.36), animals[1].animate.shift(RIGHT * 0.36),
            run_time=2.48,
        )
        bracket = shape_bracket()
        shape = T("swimming shape", 33, TEXT).move_to(pt(-2.33, -3.12))
        self.play(Create(bracket), FadeIn(shape), run_time=1.23)
        self.at("similar conditions")
        same = boxed_label("same job", GREY, size=30, pad=0.14).move_to(pt(-2.33, -3.28))
        self.play(swap(shape, same), FadeOut(flow), backdrop[0].animate.set_fill("#3e6070"), run_time=1.50)
        self.at("not close relatives")
        self.play(bracket.animate.set_opacity(0.33), backdrop[0].animate.set_fill("#243948"),
                  backdrop[1].animate.set_fill("#334d3f"), run_time=1.68)
        self.at("scientists therefore")
        # Scan the interiors while comparing what the outer outlines can and cannot tell us.
        scans = VGroup(*[
            plate(0.54, 1.24, pt(-3.54, y), TEAL, 0.78)
            for y in (1.13, -1.13)
        ])
        self.play(FadeIn(scans), backdrop[0].animate.set_fill(WATER), run_time=0.4)
        self.play(scans.animate.shift(RIGHT * 3.0), run_time=1.7, rate_func=linear)
        self.at("which similarities were inherited")
        query = T("inherited together?", 35, TEAL).move_to(pt(-2.33, -3.12))
        self.play(swap(same, query), FadeOut(scans), FadeOut(bracket),
                  backdrop[1].animate.set_fill(RIVER), run_time=1.34)
        self.finish()


def trail_picture():
    field = plate(12.14, 5.26, pt(0, 0.35), PAPER)
    icon = whale().scale(0.39).move_to(pt(-4.98, 0.35))
    trunk = path([pt(-4.07, 0.35), pt(-3.45, 0.35)], BLUE, 9)
    routes = VGroup()
    rails = VGroup()
    covers = VGroup()
    choices = VGroup()
    for color, y, text in [(GREY, 1.72, "outside shape"), (TEAL, -1.21, "inherited features")]:
        points = [pt(-3.45, 0.35), pt(-1.48, y), pt(3.43, y)]
        rails.add(path(points, color, 38, 0.32))
        routes.add(path(points, color, 6))
        choices.add(T(text, 38, color).move_to(pt(0.65, y + 0.57)))
        cover = boxed_label("?", color, size=46, box=(2.30, 1.35), fill_opacity=0.49).move_to(pt(4.74, y))
        cover.label.set_color(TEXT)
        covers.add(cover)
    question = question_card(QUESTION, size=43, y=-3.03)
    return field, icon, trunk, rails, routes, covers, choices, question


class S03Predict(SpokenScene):
    def construct(self):
        field, icon, trunk, rails, routes, covers, choices, question = trail_picture()
        self.add(field, icon)
        self.at("could follow only")
        self.play(Create(trunk), run_time=0.65)
        self.play(Create(rails[0]), Create(routes[0]), run_time=1.45)
        self.at("the outside shape")
        self.play(FadeIn(choices[0]), run_time=0.64)
        self.at("features passed through")
        self.play(Create(rails[1]), Create(routes[1]), run_time=1.48)
        self.play(FadeIn(choices[1]), run_time=0.65)
        self.at("hold your answer")
        self.play(FadeIn(question), run_time=1.10)
        self.at("the useful trail")
        self.play(
            ShowPassingFlash(routes[0].copy().set_stroke(width=39), time_width=0.54),
            ShowPassingFlash(routes[1].copy().set_stroke(width=39), time_width=0.54),
            run_time=2.76,
        )
        self.at("not just one resemblance")
        self.play(LaggedStart(*[
            FadeIn(cover, shift=LEFT * 0.60, scale=0.49, rate_func=linear) for cover in covers
        ], lag_ratio=0.38, rate_func=linear), run_time=2.43)
        self.finish()


class S04Pause(NarratedScene):
    def construct(self):
        self.add(*trail_picture())
        self.wait(self.narration_s)


BONE_X = (-2.90, -0.43, 1.70, 4.05)
BONE_NAMES = ("upper arm", "forearm pair", "wrist", "fingers")
LIMB_NAMES = ("human hand", "bat wing", "whale flipper")
LIMB_Y = (1.22, -0.49, -2.18)


def bone_sets(variant=0):
    first = plate(1.70, 0.23, pt(BONE_X[0], 0), TEAL, 0.94)
    pair = VGroup(
        plate(1.79 + 0.11 * min(variant, 2), 0.13, pt(BONE_X[1], 0.15), TEAL, 0.95),
        plate(1.63 + 0.11 * min(variant, 2), 0.12, pt(BONE_X[1], -0.15), TEAL, 0.70),
    )
    wrist = VGroup(*[
        plate(0.19, 0.17, pt(BONE_X[2] + x, y), TEAL, 0.90)
        for x in (-0.21, 0.0, 0.21) for y in (-0.10, 0.10)
    ])
    slopes = (0.34, 0.61, 0.26, 0.58)[variant]
    lengths = ((1.21, 1.68, 1.91, 1.64, 1.24), (1.38, 2.28, 2.63, 2.45, 1.94),
               (1.73, 2.15, 2.20, 1.85, 1.51), (1.30, 2.01, 2.46, 2.13, 1.71))[variant]
    digits = VGroup(*[
        path([pt(2.12, 0.11 * (2 - i)), pt(2.75 + length * 0.4, slopes * (2 - i) * 0.32),
              pt(2.67 + length, slopes * (2 - i) * 0.52)], TEAL, 6, 0.92)
        for i, length in enumerate(lengths)
    ])
    return VGroup(first, pair, wrist, digits)


def limb_outline(variant):
    if variant == 3:
        # The hand silhouette follows the spread fingers while the bone order stays fixed.
        outline = [
            (-3.93, 0.38), (0.66, 0.32), (1.92, 0.34), (2.90, 0.64), (4.08, 0.72),
            (4.22, 0.62), (4.05, 0.44), (3.49, 0.34), (4.69, 0.44), (4.85, 0.31),
            (4.72, 0.18), (4.13, 0.14), (5.12, 0.16), (5.25, 0.00), (5.10, -0.15),
            (4.12, -0.14), (4.85, -0.21), (4.94, -0.35), (4.78, -0.47), (3.82, -0.40),
            (4.42, -0.56), (4.48, -0.69), (4.30, -0.76), (3.09, -0.57), (2.41, -0.43),
            (1.58, -0.30), (0.60, -0.34), (-3.93, -0.38),
        ]
        return Polygon(*[pt(x, y) for x, y in outline], color=TEAL, stroke_width=3.5,
                       fill_color=TEAL, fill_opacity=0.40)
    top, end_y, bottom = [(0.48, 0.16, -0.49), (0.69, -0.34, -0.58), (0.47, -0.23, -0.46)][variant]
    if variant == 1:
        return silhouette((-3.93, 0), [
            ((-3.88, 0.55), (-2.66, 0.53), (-1.90, 0.28)),
            ((-0.80, 0.37), (1.75, 0.28), (2.49, 0.64)),
            ((3.31, 0.87), (4.99, 0.79), (5.63, 0.03)),
            ((5.27, 0.03), (5.01, -0.17), (5.15, -0.41)),
            ((4.86, -0.36), (4.59, -0.60), (4.71, -0.79)),
            ((3.86, -0.61), (3.07, -0.63), (2.62, -0.39)),
            ((1.04, -0.31), (-0.62, -0.36), (-1.90, -0.32)),
            ((-2.63, -0.50), (-3.87, -0.40), (-3.93, 0)),
        ], TEAL, 0.40)
    return silhouette((-3.93, 0), [
        ((-3.88, 0.55), (-2.66, 0.53), (-1.90, 0.28)),
        ((-0.80, 0.37), (1.75, 0.28), (2.49, top)),
        ((3.19, top + 0.13), (4.72, top + 0.18), (5.66, end_y)),
        ((5.21, bottom), (3.54, bottom - 0.11), (2.61, -0.39)),
        ((1.04, -0.31), (-0.62, -0.36), (-1.90, -0.32)),
        ((-2.63, -0.50), (-3.87, -0.40), (-3.93, 0)),
    ], TEAL, 0.40)


def limb_row(i, variant=0):
    y = LIMB_Y[i]
    return limb_outline(variant).shift(UP * y), bone_sets(variant).shift(UP * y)


class S05BodyParts(SpokenScene):
    def construct(self):
        rows = [limb_row(i) for i in range(3)]
        shells = VGroup(*[row[0] for row in rows])
        parts = VGroup(*[row[1] for row in rows])
        labels = VGroup(*[
            T(name, 28, TEAL).move_to(pt(x, 2.5)) for x, name in zip(BONE_X, BONE_NAMES)
        ])
        species = VGroup(*[
            T(name, 29, TEXT).move_to(pt(-5.0, y)).align_to(pt(-4.29, 0), RIGHT)
            for name, y in zip(LIMB_NAMES, LIMB_Y)
        ])
        tag = scope_tag(size=28)
        field, icon, trunk, rails, routes, covers, choices, _ = trail_picture()
        open_route = VGroup(icon, trunk, rails[1], routes[1], covers[1], choices[1])
        self.add(field, open_route)
        intro = limb_outline(0).stretch(1.67, 1)
        intro_bones = bone_sets(0).stretch(1.67, 1)
        self.at("start inside the front")
        self.play(FadeOut(open_route), run_time=0.32)
        self.play(FadeIn(intro), FadeIn(tag), run_time=0.36)
        self.play(LaggedStart(*[FadeIn(piece, shift=RIGHT * 0.25) for piece in intro_bones],
                             lag_ratio=0.37), run_time=1.75)
        self.at("human hand")
        hand, hand_bones = limb_row(0, 3)
        self.play(FadeOut(field), ReplacementTransform(intro, hand),
                  ReplacementTransform(intro_bones, hand_bones), run_time=0.59)
        self.play(FadeIn(species[0]), run_time=0.31)
        shells = VGroup(hand, *shells[1:])
        parts = VGroup(hand_bones, *parts[1:])
        self.at("bat wing")
        self.play(FadeIn(shells[1]), TransformFromCopy(parts[0], parts[1]), run_time=0.65)
        self.play(FadeIn(species[1]), run_time=0.30)
        self.at("whale flipper")
        self.play(FadeIn(shells[2]), TransformFromCopy(parts[0], parts[2]), run_time=0.80)
        self.play(FadeIn(species[2]), run_time=0.38)
        self.at("yet each keeps")
        columns = VGroup(*[
            plate(w, 4.57, pt(x, -0.47), TEAL, 0.22)
            for x, w in zip(BONE_X, (1.97, 2.01, 0.83, 2.40))
        ])
        self.play(LaggedStart(*[
            AnimationGroup(FadeIn(col), FadeIn(label)) for col, label in zip(columns, labels)
        ], lag_ratio=0.41), run_time=2.27)
        self.at("matching parts shift")
        self.play(FadeOut(columns), run_time=0.39)
        for i in (1, 2):
            shell, bones = limb_row(i, i)
            self.play(Transform(shells[i], shell), Transform(parts[i], bones), run_time=1.58)
        self.at("a homologous structure")
        term = caption("Homologous structure", size=36, color=TEAL, y=-3.14)
        self.play(FadeIn(term), *[shell.animate.set_fill(TEAL, opacity=0.56) for shell in shells], run_time=1.25)
        self.at("a common ancestor")
        node = Dot(pt(-4.09, -0.49), radius=0.085, color=GOLD)
        routes = [
            path([pt(-3.93, y), pt(-4.09, y), pt(-4.09, -0.49)], GOLD, 8)
            for y in (LIMB_Y[0], LIMB_Y[2])
        ]
        self.play(LaggedStart(*[Create(route) for route in routes], lag_ratio=0.26),
                  GrowFromCenter(node),
                  *[shell.animate.set_fill(TEAL, opacity=0.38) for shell in shells], run_time=1.45)
        self.finish()


def embryo_form(variant=0, later=False):
    outlines = [
        [((0.41, 1.44), (1.03, 0.88), (0.78, 0.12)), ((0.28, -0.22), (0.34, -0.81), (1.03, -1.17))],
        [((0.43, 1.69), (1.14, 1.16), (0.86, 0.32)), ((0.28, -0.39), (0.24, -0.65), (0.66, -0.93))],
        [((0.54, 1.62), (1.19, 0.91), (0.82, 0.25)), ((0.52, -0.13), (0.21, -0.59), (0.48, -0.77))],
    ]
    cap, curl = outlines[variant if later else 0]
    body = silhouette((-0.67, 0.17), [
        ((-1.24, 0.99), (-0.70, 1.43), (-0.22, 1.42)),
        cap, curl,
        ((0.50, -1.24), (-0.28, -1.17), (-0.55, -0.66)),
        ((-0.88, -0.36), (-0.76, -0.11), (-0.67, 0.17)),
    ], GREY, 0.39)
    tail_start, tail_end = [
        ((-0.08, -0.88), (0.87, -1.10)),
        ((-0.16, -0.66), (0.35, -0.88)),
        ((-0.16, -0.52), (0.21, -0.73)),
    ][variant if later else 0]
    tail = ArcBetweenPoints(pt(*tail_start), pt(*tail_end), angle=0.60, color=TEAL, stroke_width=8)
    arches = VGroup(*[
        ArcBetweenPoints(pt(-0.50 + 0.19 * i, 0.56), pt(-0.40 + 0.19 * i, 0.17),
                         angle=-0.85, color=TEAL, stroke_width=6)
        for i in range(3)
    ])
    return VGroup(body, tail, arches)


def embryo_cards(later=False):
    cards, forms = VGroup(), VGroup()
    for i, x in enumerate((-4.03, 0, 4.03)):
        cards.add(plate(3.54, 4.22, pt(x, 0.2), PAPER))
        forms.add(embryo_form(i, later).scale(1.22).move_to(pt(x, 0.18)))
    return cards, forms


def fossil_whale():
    legs = VGroup(*[
        path([pt(x, y), pt(x - 0.10, y - 0.34), pt(x + 0.11, y - 0.75),
              pt(x - 0.10, y - 0.75)], color, 8)
        for x, y, color in [(-0.85, -0.22, "#898174"), (-0.53, -0.33, "#D0BA9F"),
                            (0.76, -0.22, "#898174"), (1.04, -0.33, "#D0BA9F")]
    ])
    body = silhouette((-2.12, 0.20), [
        ((-1.88, 0.43), (-1.65, 0.27), (-1.46, 0.36)),
        ((-1.09, 0.92), (0.45, 0.75), (1.27, 0.30)),
        ((1.56, 0.11), (1.97, 0.19), (2.30, 0.59)),
        ((2.13, 0.06), (1.60, -0.15), (1.27, -0.07)),
        ((0.97, -0.59), (-0.30, -0.44), (-1.13, -0.28)),
        ((-1.41, -0.21), (-1.68, -0.02), (-2.12, 0.04)),
        ((-2.19, 0.08), (-2.16, 0.16), (-2.12, 0.20)),
    ], "#D0BA9F", 0.55)
    return VGroup(legs, body, Dot(pt(-1.55, 0.23), radius=0.05, color=BG))


def rock_layers():
    return VGroup(*[
        plate(11.65, 0.75, pt(0, y), color)
        for y, color in [(-1.82, ROCK), (-1.13, "#4b3e3a"), (-0.44, "#594b3f"), (0.25, "#644f3f")]
    ])


def fossil_picture():
    layers = rock_layers()
    axis = Arrow(pt(-5.55, -2.47), pt(5.56, -2.47), buff=0, color=GREY, stroke_width=4, tip_length=0.17)
    age = VGroup(T("past", 28, TEXT).move_to(pt(-5.15, -2.89)),
                 T("present", 28, TEXT).move_to(pt(5.07, -2.89)))
    forms = VGroup(fossil_whale().scale(0.83).move_to(pt(-3.12, 1.25)),
                   whale().scale(0.88).move_to(pt(3.09, 1.25)))
    names = VGroup(T("fossil whale", 31, TEXT).move_to(pt(-3.12, 2.53)),
                   T("modern whale", 31, BLUE).move_to(pt(3.09, 2.53)))
    node = Dot(pt(0, -1.44), radius=0.13, color=GOLD)
    links = VGroup(
        path([node.get_center(), pt(-1.59, -1.44), pt(-3.12, 0.34)], GOLD, 5),
        path([node.get_center(), pt(1.61, -1.44), pt(3.09, 0.43)], GOLD, 5),
    )
    return layers, axis, age, forms, names, node, links


class S06DevelopmentFossils(SpokenScene):
    def construct(self):
        cards, embryos = embryo_cards()
        _, later = embryo_cards(later=True)
        tag = scope_tag(size=28)
        header = T("Development", 36, TEXT).move_to(pt(0, 2.78))
        self.at("development and fossils")
        self.play(LaggedStart(*[FadeIn(card) for card in cards], lag_ratio=0.18),
                  FadeIn(tag), run_time=0.74)
        self.play(LaggedStart(*[FadeIn(embryo[0]) for embryo in embryos], lag_ratio=0.35),
                  FadeIn(header), run_time=2.0)
        self.at("vertebrate embryos")
        self.play(AnimationGroup(*[AnimationGroup(Create(embryo[1]), Create(embryo[2])) for embryo in embryos]),
                  *[card.animate.set_fill("#2c5156") for card in cards], run_time=1.91)
        self.at("follow different paths")
        self.play(
            Transform(embryos[1], later[1].stretch(1.24, 0)),
            Transform(embryos[2], later[2].stretch(0.76, 1)),
            cards[1].animate.set_fill("#36434d"), cards[2].animate.set_fill("#365358"), run_time=1.9,
        )
        layers, axis, age, forms, names, node, links = fossil_picture()
        self.at("fossils place past")
        self.play(FadeOut(cards), FadeOut(embryos), FadeOut(header), run_time=0.30)
        self.play(LaggedStart(*[FadeIn(layer, shift=UP * 0.29) for layer in layers],
                             lag_ratio=0.18), Create(axis), run_time=1.35)
        self.play(FadeIn(age), run_time=0.60)
        self.at("embryos begin hind limbs")
        detail = embryo_form().scale(0.64).move_to(pt(0, 1.37))
        bud = Dot(pt(0.20, 0.92), color=TEAL, radius=0.11)
        embryo_name = T("whale embryo", 29, BLUE).move_to(pt(0, 2.53))
        lens = plate(2.0, 1.82, pt(0, 1.37), PAPER)
        self.play(FadeIn(lens), FadeIn(detail), run_time=0.46)
        self.play(GrowFromCenter(bud), FadeIn(embryo_name), run_time=0.91)
        self.at("had working legs")
        self.play(FadeIn(forms[0], shift=UP * 0.43), run_time=0.56)
        self.play(FadeIn(names[0]), Indicate(forms[0][0], color=TEAL, scale_factor=1.055), run_time=0.9)
        self.at("an adult whale")
        self.play(FadeOut(detail), FadeOut(lens), FadeOut(bud), FadeOut(embryo_name),
                  FadeIn(forms[1]), run_time=0.53)
        self.play(LaggedStart(GrowFromCenter(node), Create(links), lag_ratio=0.24),
                  FadeIn(names[1]), run_time=1.40)
        self.finish()


TIP_Y = (2.23, 1.12, 0.01, -1.10, -2.21)
STRIP_X = (-2.63, 0.41, 3.31)
TIP_COLORS = (GREY, GREY, GREY, BLUE, GREEN)
TIP_NAMES = ("outgroup", "pig", "cow", "whale", "hippo")
ROOT = pt(-5.68, 0.27)
OUT_SPLIT = pt(-4.48, 0.27)
INNER_SPLIT = pt(-2.64, -0.41)
PAIR_SPLIT = pt(0.75, -1.65)
TRAIT_AT = pt(-0.61, -1.65)
TIPS = tuple(pt(2.87, y) for y in TIP_Y)


def sequence_picture():
    title = T("Matching DNA locations", 34, TEXT).move_to(pt(0, 3.08))
    strips, names, slots = VGroup(), VGroup(), VGroup()
    for name, color, y in zip(TIP_NAMES, TIP_COLORS, TIP_Y):
        strip = plate(9.9, 0.85, pt(0.92, y), color, 0.32)
        strips.add(strip)
        names.add(T(name, 29, color).next_to(strip, LEFT, buff=0.22))
        slots.add(VGroup(*[plate(0.80, 0.48, pt(x, y), BG, 0.76) for x in STRIP_X]))
    inserts = VGroup(*[
        VGroup(*[plate(0.71, 0.39, pt(x, y), TEAL) for y in TIP_Y[-2:]])
        for x in STRIP_X
    ])
    return title, strips, names, slots, inserts


def tree_picture(outgroup="outgroup"):
    """Shared coordinates for each taxon, node, and highlighted stretch of branch."""
    lines = VGroup(
        path([ROOT, OUT_SPLIT], GREY, 8),
        path([OUT_SPLIT, pt(-3.19, TIP_Y[0]), TIPS[0]], GREY, 7),
        path([OUT_SPLIT, pt(-3.45, -0.41), INNER_SPLIT], GREY, 7),
        path([INNER_SPLIT, pt(-1.40, TIP_Y[1]), TIPS[1]], GREY, 7),
        path([INNER_SPLIT, pt(-1.78, TIP_Y[2]), TIPS[2]], GREY, 7),
        path([INNER_SPLIT, pt(-1.86, -1.65), PAIR_SPLIT], GREY, 7),
        path([PAIR_SPLIT, pt(1.58, TIP_Y[3]), TIPS[3]], BLUE, 8),
        path([PAIR_SPLIT, pt(1.58, TIP_Y[4]), TIPS[4]], GREEN, 8),
    )
    backdrop = plate(12.74, 5.60, pt(-0.12, 0.05), PAPER)
    nodes = VGroup(*[Dot(center, radius=radius, color=GOLD) for center, radius in
                     [(OUT_SPLIT, 0.10), (INNER_SPLIT, 0.10), (PAIR_SPLIT, 0.155)]]).set_z_index(10)
    tips = VGroup(*[Dot(tip, radius=0.08, color=color) for tip, color in zip(TIPS, TIP_COLORS)])
    labels = VGroup(*[
        T(name, 31, TEXT if color in (BLUE, GREEN) else color).next_to(tip, RIGHT, buff=0.33)
        for name, tip, color in zip((outgroup, *TIP_NAMES[1:]), TIPS, TIP_COLORS)
    ])
    return backdrop, lines, nodes, tips, labels


def evidence_icon(index):
    if index == 0:
        out = VGroup(*[plate(0.38, 0.10, pt(0, y), TEAL) for y in (-0.10, 0.10)])
        return out.rotate(0.38)
    if index == 1:
        body, tail, arches = embryo_form().set_height(0.44)
        return VGroup(body.set_stroke(width=1.5), tail.set_stroke(width=2), arches.set_stroke(width=2))
    if index == 2:
        return fossil_whale().set_width(0.57)
    return VGroup(*[plate(0.10, 0.31, pt(x, 0), TEAL) for x in (-0.16, 0, 0.16)])


EVIDENCE_NAME = ("body", "development", "fossils", "DNA")


def evidence_picture():
    fields = VGroup(*[
        plate(w, h, pt(x, y), "#3d6873").set_z_index(1)
        for w, h, x, y in [(2.50, 0.66, -4.93, -0.78), (3.32, 0.72, -4.54, -1.61),
                           (2.42, 0.54, -4.99, -2.39), (1.94, 0.50, -1.48, -2.39)]
    ])
    icons, labels = VGroup(), VGroup()
    for i, (name, field) in enumerate(zip(EVIDENCE_NAME, fields)):
        icon = evidence_icon(i).scale(1.07).set_z_index(2)
        label = T(name, 28, TEXT).set_z_index(2)
        VGroup(icon, label).arrange(RIGHT, buff=0.18).move_to(field)
        icons.add(icon)
        labels.add(label)

    # Route under the branches and fan into the lower edge of the convergence ring.
    connectors = VGroup(
        path([fields[0].get_right(), pt(-3.17, -0.78), pt(-2.54, -1.15),
              pt(-1.95, -1.79), pt(0.39, -1.79)], TEAL, 4),
        path([fields[1].get_right(), pt(-2.60, -1.61), pt(-2.03, -1.94),
              pt(0.49, -1.94)], TEAL, 4),
        path([fields[2].get_right(), pt(-3.00, -2.39), pt(-2.58, -2.06),
              pt(-0.27, -2.06), pt(0.65, -2.03)], TEAL, 4),
        path([fields[3].get_right(), pt(-0.14, -2.39), pt(0.51, -2.30),
              pt(0.87, -2.02)], TEAL, 4),
    )
    return icons, labels, fields, connectors


def pair_ring():
    return Circle(radius=0.39, color=TEAL, stroke_width=7).move_to(PAIR_SPLIT)


def pair_field():
    return plate(4.89, 2.12, pt(3.73, -1.65), "#35636a")


def tip_field(i, color):
    return plate(4.89, 0.91, pt(3.73, TIP_Y[i]), color)


class S07Dna(SpokenScene):
    def construct(self):
        layers = rock_layers()
        tag = scope_tag(size=28)
        self.add(layers, tag)
        title, strips, names, slots, inserts = sequence_picture()
        self.at("dna supplies")
        self.play(
            LaggedStart(*[ReplacementTransform(layer, strip) for layer, strip in zip(layers, strips)],
                        FadeIn(strips[-1]), lag_ratio=0.20),
            run_time=2.4,
        )
        self.play(LaggedStart(*[FadeIn(name) for name in names], lag_ratio=0.16), run_time=1.2)
        self.at("compare corresponding sequences")
        self.play(LaggedStart(*[FadeIn(row) for row in slots], lag_ratio=0.34),
                  FadeIn(title), run_time=2.75)
        self.at("look for changes")
        brackets = VGroup(*[
            DashedLine(pt(x, 2.74), pt(x, -2.74), dash_length=0.14, color=TEAL, stroke_width=3,
                       stroke_opacity=0.63)
            for x in (STRIP_X[0] - 0.53, STRIP_X[1] - 0.53, STRIP_X[2] - 0.53)
        ])
        guides = VGroup(*[plate(1.08, 5.45, pt(x, 0), TEAL, 0.37).set_z_index(-1) for x in STRIP_X])
        self.play(
            LaggedStart(*[FadeIn(guide, shift=UP * 0.26) for guide in guides], lag_ratio=0.5),
            LaggedStart(*[Create(line) for line in brackets], lag_ratio=0.5), run_time=2.16,
        )
        self.at("shared insertions")
        self.play(
            LaggedStart(*[FadeIn(pair, shift=DOWN * 0.22) for pair in inserts], lag_ratio=0.85),
            run_time=2.38,
        )
        self.at("especially useful clues")
        self.play(
            LaggedStart(*[Indicate(pair, color=TEXT, scale_factor=1.14) for pair in inserts], lag_ratio=0.5),
            strips[3].animate.set_fill(BLUE, opacity=0.58),
            strips[4].animate.set_fill(GREEN, opacity=0.58), run_time=1.68,
        )
        self.at("several such clues")
        canvas, lines, nodes, tips, labels = tree_picture()
        self.play(FadeOut(title), FadeOut(slots), FadeOut(brackets), FadeOut(names), FadeOut(guides), run_time=0.32)
        self.play(
            FadeIn(canvas), FadeOut(inserts),
            LaggedStart(*[
                ReplacementTransform(strips[i], lines[j])
                for i, j in enumerate((1, 3, 4, 6, 7))
            ], lag_ratio=0.12),
            run_time=1.29,
        )
        self.bring_to_back(canvas)
        self.play(LaggedStart(*[Create(lines[i]) for i in (0, 2, 5)], lag_ratio=0.20),
                  FadeIn(nodes), FadeIn(tips), FadeIn(labels), run_time=1.35)
        self.at("when body")
        icons, _, _, _ = evidence_picture()
        incoming = VGroup(*[
            VGroup(plate(1.22, 1.03, ORIGIN, PAPER), icon.copy().set_width(0.62).move_to(ORIGIN))
            .move_to(pt(x, y))
            for icon, (x, y) in zip(icons, [(-5.3, 2.10), (-5.30, 0.94), (-4.8, -1.40), (-3.45, -2.20)])
        ])
        self.play(LaggedStart(*[FadeIn(icon, shift=UP * 0.17) for icon in incoming], lag_ratio=0.72),
                  run_time=2.27)
        self.at("evidence agree")
        pair = pair_field().set_z_index(-1)
        canvas.set_z_index(-2)
        self.play(
            LaggedStart(*[FadeOut(icon, target_position=PAIR_SPLIT) for icon in incoming], lag_ratio=0.19),
            Create(pair_ring()), FadeIn(pair, scale=0.65), run_time=1.83,
        )
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        canvas, lines, nodes, tips, labels = tree_picture()
        icons, names, evidence_fields, connectors = evidence_picture()
        ring = pair_ring()
        pair = pair_field().set_z_index(-1)
        canvas.set_z_index(-2)
        self.add(canvas, pair, lines, nodes, tips, labels, ring, scope_tag(size=28))
        self.at("one clue")
        self.play(Uncreate(ring), FadeOut(pair), FadeIn(icons[0]),
                  FadeIn(evidence_fields[0]), run_time=1.20)
        self.at("compare independent evidence")
        self.play(Create(connectors[0]), run_time=2.18)
        self.at("body structures")
        self.play(FadeIn(names[0]), evidence_fields[0].animate.set_fill("#57858d"), run_time=0.65)
        self.at("development")
        self.play(FadeIn(evidence_fields[1]), run_time=0.27)
        self.play(FadeIn(icons[1]), FadeIn(names[1]), run_time=0.35)
        self.at("fossils")
        self.play(FadeIn(icons[2]), FadeIn(names[2]), FadeIn(evidence_fields[2]), run_time=0.63)
        self.at("the same branches")
        self.play(FadeIn(icons[3]), FadeIn(names[3]), FadeIn(evidence_fields[3]), run_time=0.47)
        self.play(LaggedStart(*[Create(line) for line in connectors[1:]], lag_ratio=0.34), run_time=2.45)
        self.at("when they agree")
        ring = pair_ring()
        self.play(Create(ring), FadeIn(pair, scale=0.65), run_time=1.23)
        self.play(FadeOut(names), FadeOut(icons), run_time=0.30)
        self.play(FadeOut(connectors), FadeOut(evidence_fields), run_time=0.52)
        self.at("are derived traits")
        marker = Square(side_length=0.44, color=TEAL, fill_color=TEAL,
                        fill_opacity=1, stroke_width=0).rotate(PI / 4).move_to(TRAIT_AT)
        trait = boxed_label("derived trait", TEAL, size=32).move_to(pt(-3.45, -2.21))
        stem = path([pt(-1.86, -1.65), PAIR_SPLIT], TEAL, 22)
        self.play(GrowFromCenter(marker), Create(stem), FadeOut(pair), run_time=1.04)
        self.play(FadeIn(trait), run_time=0.62)
        self.at("first appeared")
        meaning = boxed_label("first in one ancestor", TEAL, size=30).move_to(trait)
        self.play(swap(trait, meaning), run_time=0.88)
        self.at("and passed to")
        self.play(
            LaggedStart(*[Create(line.copy().set_stroke(TEAL, width=22)) for line in lines[6:]],
                        lag_ratio=0.35), FadeIn(pair, scale=0.71), run_time=1.91,
        )
        self.at("shared derived traits to")
        self.play(FadeOut(meaning), run_time=0.40)
        rule = caption(RULE.replace("points to", "points\nto"), size=29, color=TEXT, y=-3.28)
        self.play(FadeIn(rule), ShowPassingFlash(stem.copy().set_stroke(TEXT, width=27),
                                                time_width=0.62), run_time=1.45)
        self.at("the closest relatives")
        self.play(pair.animate.set_fill("#3a7073"), ring.animate.set_stroke(width=12), run_time=0.88)
        self.finish()


def family_result():
    canvas, lines, nodes, tips, labels = tree_picture("tuna")
    pictures = VGroup(
        tuna().set_width(1.48).move_to(pt(5.37, TIP_Y[0])),
        whale().set_width(1.48).move_to(pt(5.37, TIP_Y[3])),
        hippo().set_width(1.32).move_to(pt(5.37, TIP_Y[4])),
    )
    note = T("swimming shape", 29, GREY).move_to(pt(-4.85, 2.45))
    track = path([pt(-1.68, -1.65), PAIR_SPLIT], TEAL, 13)
    ring = Circle(radius=0.38, color=TEAL, stroke_width=7).move_to(PAIR_SPLIT)
    return canvas, lines, nodes, tips, labels, pictures, note, track, ring


def trait_labels(words):
    return VGroup(*[
        boxed_label(word, TEAL, size=29, box=(width, 0.58), pad=0.12,
                    fill_opacity=0.12).move_to(pt(x, -3.25))
        for word, x, width in zip(words, (-4.85, -2.35, 0.15), (1.70, 2.36, 2.0))
    ])


class S09Answer(SpokenScene):
    def construct(self):
        backdrop, animals, labels, tag = opening_world()
        bracket = shape_bracket()
        self.add(backdrop, animals, labels, tag)
        self.at("the first question")
        self.play(Create(bracket), backdrop[0].animate.set_fill("#3e6070"), run_time=1.55)
        self.at("the whale's swimming shape")
        function = T("function", 37, GREY).move_to(pt(-2.31, -3.15))
        self.play(Indicate(bracket, color=TEXT, scale_factor=1.03), FadeIn(function),
                  animals[0].animate.shift(LEFT * 0.29), animals[1].animate.shift(LEFT * 0.29),
                  run_time=1.52)
        self.at("by function")
        self.play(bracket.animate.set_opacity(0.37), backdrop[0].animate.set_fill(WATER), run_time=0.88)
        canvas, lines, nodes, tips, names, pictures, note, track, ring = family_result()
        first = trait_labels(("lungs", "limb bones", "embryos"))
        second = trait_labels(("milk", "fossils", "DNA"))
        self.at("its lungs")
        self.play(FadeOut(backdrop), FadeOut(labels), FadeOut(function), FadeOut(bracket),
                  run_time=0.30)
        self.play(FadeIn(canvas.set_z_index(-2)), run_time=0.30)
        self.bring_to_back(canvas)
        self.play(
            ReplacementTransform(animals[0], pictures[1]),
            ReplacementTransform(animals[1], pictures[0]),
            ReplacementTransform(animals[2], pictures[2]),
            FadeIn(first[0]), run_time=0.63,
        )
        self.at("limb bones")
        self.play(FadeIn(first[1]), run_time=0.51)
        self.at("and embryos")
        self.play(FadeIn(first[2]), run_time=0.48)
        self.play(LaggedStart(Create(lines[0]), GrowFromCenter(nodes[0]), Create(lines[1]),
                             Create(lines[2]), lag_ratio=0.42),
                  FadeIn(tips[0]), FadeIn(names[0]), run_time=2.0)
        self.at("its milk")
        self.play(swap(first[0], second[0]), run_time=0.63)
        self.at("fossils and dna", lead=0.55)
        self.play(swap(first[1], second[1]), run_time=0.65)
        self.at("and dna")
        self.play(swap(first[2], second[2]), run_time=0.63)
        self.at("link it to mammals")
        mammals = plate(4.89, 4.36, pt(3.73, -0.55), "#34545f").set_z_index(-1)
        self.play(LaggedStart(*[Create(lines[i]) for i in (3, 4, 5)], lag_ratio=0.22),
                  GrowFromCenter(nodes[1]), FadeIn(tips[1:3]), FadeIn(names[1:3]),
                  FadeIn(mammals), run_time=1.72)
        self.at("within living mammals")
        self.play(LaggedStart(GrowFromCenter(nodes[2]), Create(lines[6]), Create(lines[7]), lag_ratio=0.45),
                  run_time=1.49)
        self.play(FadeIn(tips[3:]), FadeIn(names[3:]), run_time=0.61)
        self.at("whales closest to hippos")
        pair = pair_field().set_z_index(-1)
        self.play(LaggedStart(*[FadeOut(label) for label in second], lag_ratio=0.22),
                  Create(track), Create(ring), ReplacementTransform(mammals, pair), run_time=1.58)
        self.at("the tree records ancestry")
        self.play(FadeIn(note), run_time=0.61)
        self.play(
            ShowPassingFlash(path([PAIR_SPLIT, pt(1.58, TIP_Y[3]), TIPS[3]], TEXT, 19), time_width=0.72),
            ShowPassingFlash(path([PAIR_SPLIT, pt(1.58, TIP_Y[4]), TIPS[4]], TEXT, 19), time_width=0.72),
            pair.animate.set_fill("#3a7073"), run_time=1.87,
        )
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        canvas, lines, nodes, tips, labels, pictures, note, track, ring = family_result()
        pair = pair_field().set_fill("#3a7073").set_z_index(-1)
        canvas.set_z_index(-2)
        self.add(canvas, pair, lines, nodes, tips, labels, pictures, track, ring, scope_tag(size=28))
        inset = plate(3.13, 2.04, pt(-4.14, -1.57), "#284952")
        bones = bone_sets(2).set_width(2.65).move_to(inset)
        bones[3].stretch(2.5, 1).set_stroke(width=2)
        self.at("looks still matter")
        self.play(FadeIn(inset), FadeIn(bones), run_time=1.19)
        self.at("preserve inherited parts")
        self.play(
            pair.animate.set_fill("#46818a"),
            LaggedStart(*[Indicate(part, color=TEXT, scale_factor=1.10) for part in bones], lag_ratio=0.46),
            run_time=1.85,
        )
        silhouettes = VGroup(
            whale().set_width(2.31).move_to(pt(-4.14, -1.12)),
            tuna().set_width(2.31).move_to(pt(-4.14, -2.02)),
        )
        self.at("they mislead")
        self.play(FadeOut(bones), FadeIn(silhouettes), inset.animate.set_fill(WATER), run_time=0.64)
        self.at("a shared job")
        function = T("shared function", 29, GREY).move_to(note)
        tuna_field = tip_field(0, "#3f4e57").set_z_index(-1)
        self.play(FadeIn(function), FadeIn(tuna_field), run_time=0.65)
        self.at("begin with traits", lead=0.30)
        self.play(FadeOut(function), FadeOut(tuna_field), FadeOut(silhouettes),
                  inset.animate.set_fill(PAPER), run_time=0.30)
        self.at("test them with independent")
        icons, _, _, _ = evidence_picture()
        row = icons.arrange_in_grid(2, 2, buff=(0.34, 0.44)).scale(1.39).move_to(inset)
        self.play(LaggedStart(*[FadeIn(icon) for icon in row], lag_ratio=0.49),
                  inset.animate.set_fill("#36575f"), run_time=1.63)
        self.at("follow their paths")
        tracing = path([TIPS[3], pt(1.58, TIP_Y[3]), PAIR_SPLIT], TEAL, 16)
        finger = Dot(TIPS[3], radius=0.17, color=TEXT).set_stroke(TEAL, 3)
        self.play(FadeOut(row), FadeOut(inset), FadeIn(finger), run_time=0.40)
        self.play(MoveAlongPath(finger, tracing), Create(tracing), run_time=1.87)
        self.play(FadeOut(finger), ring.animate.set_stroke(width=11), run_time=0.55)
        self.at("turns a resemblance")
        takeaway = caption("A claim you can check", size=34, color=TEAL, y=-3.17)
        self.play(FadeIn(takeaway), pair.animate.set_fill("#35636a"), run_time=0.67)
        self.at("a claim you can check")
        self.play(
            Create(path([PAIR_SPLIT, pt(1.58, TIP_Y[4]), TIPS[4]], TEAL, 22)),
            pair.animate.set_fill("#47848a"), run_time=1.16,
        )
        self.finish()


class S11End(EndCard):
    LINE = "Trace shared derived traits to branch points to find the closest relatives."
