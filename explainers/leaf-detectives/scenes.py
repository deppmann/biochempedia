"""Leaf Detectives. Word cues follow the supplied Kokoro alignment."""

from bp_parts import *
from bp_style import EndCard


# COLOR MAP: cream tabletop, tan work mat, teal string, walnut tools,
# green foliage, warm fall foliage and crimson safety marks.
CREAM = "#FFF5E1"
MAT = "#E5CBA1"
INK = "#32291E"
WOOD = "#8B5935"
TEAL_INK = "#165B59"
MOSS = "#47774B"
FERN = "#6D9050"
DARK_GREEN = "#325D46"
FALL_RED = "#BE4938"
FALL_ORANGE = "#C87432"
FALL_YELLOW = "#D8A93A"
STOP = "#9D292A"
PAPER = "#FFF9EB"
SKIN = "#BD805C"
WAX = "#745774"

# Outlines and vein paths are schematic, in a common tip-up orientation.
MAPLE = [(0, 1.83), (.26, 1.17), (.52, 1.32), (.42, .67), (.81, .5),
         (1.38, .91), (1.25, .44), (1.57, .27), (1.14, -.11), (1.22, -.31),
         (.66, -.51), (.73, -.81), (.13, -.66), (0, -.8), (-.13, -.66),
         (-.73, -.81), (-.66, -.51), (-1.22, -.31), (-1.14, -.11),
         (-1.57, .27), (-1.25, .44), (-1.38, .91), (-.81, .5), (-.42, .67),
         (-.52, 1.32), (-.26, 1.17)]
OAK = [(0, 1.65), (.4, 1.52), (.52, 1.19), (.30, .98), (.69, .98),
       (.87, .69), (.77, .44), (.44, .36), (.79, .20), (.86, -.11),
       (.70, -.36), (.41, -.4), (.59, -.59), (.46, -.84), (0, -1.02),
       (-.42, -.83), (-.57, -.58), (-.35, -.39), (-.71, -.31), (-.79, -.03),
       (-.63, .19), (-.38, .31), (-.75, .45), (-.81, .73), (-.61, .96),
       (-.31, .96), (-.46, 1.23), (-.35, 1.52)]
OVAL = [(0, 1.6), (.57, 1.06), (.80, .4), (.75, -.15), (.48, -.69),
        (0, -.99), (-.47, -.69), (-.73, -.15), (-.77, .4), (-.55, 1.06)]
HOLLY = [(0, 1.67), (.18, 1.24), (.71, 1.11), (.53, .78), (.94, .46),
         (.66, .25), (.89, -.22), (.54, -.30), (.60, -.72), (.23, -.67),
         (0, -1.07), (-.23, -.67), (-.60, -.72), (-.54, -.30), (-.89, -.22),
         (-.66, .25), (-.94, .46), (-.53, .78), (-.71, 1.11), (-.18, 1.24)]
TOOTH = [(0, 1.64), (.31, 1.33), (.25, 1.21), (.55, 1.04), (.43, .93),
         (.72, .68), (.56, .63), (.80, .35), (.64, .29), (.80, .04),
         (.63, -.01), (.69, -.32), (.51, -.33), (.49, -.59), (.30, -.58),
         (.25, -.82), (0, -.99), (-.25, -.82), (-.30, -.58), (-.49, -.59),
         (-.51, -.33), (-.69, -.32), (-.63, -.01), (-.80, .04), (-.64, .29),
         (-.80, .35), (-.56, .63), (-.72, .68), (-.43, .93), (-.55, 1.04),
         (-.25, 1.21), (-.31, 1.33)]


def p(x, y):
    return np.array([x, y, 0.0])


def path(points, color, width=3, smooth=False):
    line = VMobject(stroke_color=color, stroke_width=width)
    vertices = [p(x, y) for x, y in points]
    if smooth:
        line.set_points_smoothly(vertices)
    else:
        line.set_points_as_corners(vertices)
    return line


def leaf(kind, color, center=ORIGIN, size=2.3, angle=0, rubbing=False):
    if kind == "needle":
        needles = VGroup(*[
            path([(0, -1.15), (x * .42, .26), (x, y)], shade, width, True)
            for x, y, shade, width in [(-.95, 1.64, DARK_GREEN, 7),
                                        (-.19, 1.85, MOSS, 8),
                                        (.62, 1.71, FERN, 7)]
        ])
        needles.add(path([(-.01, -1.41), (0, -1.04)], WOOD, 9))
        return needles.set_height(size).rotate(angle).move_to(center)

    outline = {"maple": MAPLE, "oak": OAK, "oval": OVAL,
               "toothed": TOOTH, "holly": HOLLY}[kind]
    edge = interpolate_color(ManimColor(color), ManimColor(INK), .49)
    vein_ink = interpolate_color(ManimColor(color), ManimColor(PAPER), .48)
    if rubbing:
        edge = WAX
        vein_ink = WAX
    blade = path(outline + [outline[0]], edge, 3, kind in ("oak", "oval"))
    blade.close_path()
    blade.set_fill(color, .25 if rubbing else 1)
    midrib = path([(0, -1.48), (0, -.72), (.035, .39), (0, 1.48)],
                  vein_ink, 2.9, True)
    if kind == "maple":
        forks = [[(0, -.72), (.65, -.27), (1.31, .22)],
                 [(0, -.72), (-.64, -.26), (-1.31, .22)],
                 [(0, -.44), (.35, .04), (.85, .46)],
                 [(0, -.44), (-.35, .04), (-.85, .46)],
                 [(0, .25), (.21, .57), (.37, .93)],
                 [(0, .25), (-.21, .57), (-.37, .93)]]
    else:
        forks = [[(0, y), (sign * x * .57, y + .19), (sign * x, y + .40)]
                 for y, x in [(-.64, .38), (-.28, .56), (.12, .61), (.5, .43)]
                 for sign in [-1, 1]]
    veins = VGroup(midrib, *[path(points, vein_ink, 1.7, True) for points in forks])
    sample = VGroup(blade, veins).set_height(size).rotate(angle).move_to(center)
    sample.blade, sample.veins = blade, veins
    return sample


def tabletop(scene):
    scene.camera.background_color = CREAM
    config.background_color = CREAM
    shadow = RoundedRectangle(width=12.85, height=5.74, corner_radius=.38,
                              fill_color="#F4E2C1", fill_opacity=1, stroke_width=0)
    shadow.move_to(p(.05, .01))
    mat = RoundedRectangle(width=12.72, height=5.64, corner_radius=.34,
                           fill_color=MAT, fill_opacity=1, stroke_width=0)
    mat.move_to(p(0, .09))
    scene.add(VGroup(shadow, mat).set_z_index(-5))


def hoop(center, width=4.3, height=4.36):
    return Ellipse(width=width, height=height, stroke_color=TEAL_INK,
                   stroke_width=6, fill_color="#F7E4BD", fill_opacity=.62).move_to(center)


LEFT_HOOP, RIGHT_HOOP = p(-3.13, .25), p(3.13, .25)
HOOP_LABELS = p(-3.13, -2.39), p(3.13, -2.39)
LEAF_TYPES = [("oak", MOSS), ("oval", FALL_YELLOW), ("maple", FALL_RED),
              ("toothed", FERN), ("oak", FALL_ORANGE), ("oval", DARK_GREEN),
              ("maple", MOSS), ("holly", DARK_GREEN)]


def collection(center=ORIGIN, size=1.75):
    spots = [(-3.9, .92, -.45), (-1.28, 1.18, .3), (1.28, 1.08, -.28),
             (3.9, .93, .32), (-3.7, -.9, .35), (-1.22, -.96, -.42),
             (1.22, -.92, .56), (3.78, -.94, -.34)]
    return VGroup(*[leaf(kind, color, center + p(x, y) * size / 1.75, size, angle)
                    for (kind, color), (x, y, angle) in zip(LEAF_TYPES, spots)])


def sort_hoops():
    return VGroup(hoop(LEFT_HOOP), hoop(RIGHT_HOOP))


def sorted_leaves():
    checked = collection(size=1.16)
    centers = [LEFT_HOOP + p(-.80, .75), RIGHT_HOOP + p(-.68, .75),
               LEFT_HOOP + p(.65, .67), RIGHT_HOOP + p(.69, .72),
               LEFT_HOOP + p(-.83, -.62), RIGHT_HOOP + p(0, -.70),
               LEFT_HOOP + p(.69, -.67)]
    for sample, center in zip(checked, centers):
        sample.move_to(center)
    return VGroup(*checked[:7])


def label(text, center, size=33, color=INK):
    return T(text, size, color, weight=MEDIUM).move_to(center)


def prompt(text):
    return question_card(text, color=INK, y=-3.18, size=36)


def crossout(center, size):
    return VGroup(
        Circle(radius=size / 2, color=STOP, stroke_width=8).move_to(center),
        Line(center + p(-.35, .35) * size, center + p(.35, -.35) * size,
             color=STOP, stroke_width=8),
    )


def magnifier(center):
    rim = Circle(radius=.83, stroke_color=TEAL_INK, stroke_width=8)
    lens = Arc(radius=.66, start_angle=1.63, angle=1.0, color=PAPER, stroke_width=4)
    handle = Line(p(.58, -.58), p(1.43, -1.45), color=TEAL_INK, stroke_width=14)
    return VGroup(handle, rim, lens).shift(center)


def sun(center, radius=.53):
    rays = VGroup(*[Line(radius * 1.32 * u, radius * 1.69 * u,
                         color=WOOD, stroke_width=3)
                    for u in [p(np.cos(a), np.sin(a)) for a in np.arange(8) * TAU / 8]])
    disk = Circle(radius=radius, fill_color=FALL_YELLOW, fill_opacity=1,
                  stroke_color=WOOD, stroke_width=3)
    return VGroup(rays, disk).shift(center)


def paper(center, width=4.2, height=4.9):
    return RoundedRectangle(width=width, height=height, corner_radius=.08,
                            fill_color=PAPER, fill_opacity=1, stroke_color=WOOD,
                            stroke_width=2).move_to(center)


def crayon(center, length=2.9, angle=0):
    body = Polygon(p(-1.05, -.23), p(.97, -.23), p(1.43, -.08),
                   p(1.43, .09), p(.97, .23), p(-1.05, .23),
                   fill_color=WAX, fill_opacity=1, stroke_color=INK, stroke_width=2)
    shine = Line(p(-.88, .13), p(.94, .13), color="#B19AB6", stroke_width=3)
    return VGroup(body, shine).set_width(length).rotate(angle).move_to(center)


def basket(center):
    body = Polygon(p(-1.84, .1), p(1.84, .1), p(1.35, -1.37),
                   p(-1.35, -1.37), fill_color="#BE8754", fill_opacity=1,
                   stroke_color=WOOD, stroke_width=4)
    handle = Arc(radius=1.42, start_angle=0, angle=PI, color=WOOD, stroke_width=14)
    handle.shift(UP * .08)
    wicker = VGroup(*[
        Line(p(-1.72 + .16 * i, -.28 - .39 * i),
             p(1.72 - .16 * i, -.28 - .39 * i), color="#F2CD98", stroke_width=4)
        for i in range(3)
    ], *[Line(p(x, .03), p(.77 * x, -1.32), color=WOOD, stroke_width=3)
         for x in np.linspace(-1.68, 1.68, 10)])
    rim = Line(p(-1.88, .1), p(1.88, .1), color=WOOD, stroke_width=13)
    return VGroup(handle, body, wicker, rim).move_to(center)


def hand(center, angle=0, size=2.3, point=False):
    contour = [(-.70, -1.55), (-.73, -.70), (-1.04, -.27), (-1.02, .10),
               (-.78, .20), (-.53, -.10), (-.48, .85), (-.36, 1.11),
               (-.14, 1.08), (-.05, .78), (.06, 1.21), (.26, 1.29),
               (.40, 1.11), (.45, .63), (.64, .81), (.81, .73),
               (.87, .43), (1.00, .49), (1.14, .34), (1.12, -.38),
               (.84, -.94), (.79, -1.55)]
    if point:
        contour = [(-.70, -1.55), (-.73, -.75), (-.94, -.43), (-1.01, -.16),
                   (-.87, .05), (-.68, .03), (-.48, -.18),
                   (-.39, .29), (-.39, 1.32), (-.34, 1.54), (-.19, 1.63),
                   (-.02, 1.57), (.05, 1.37), (.07, .48),
                   (.23, .61), (.40, .56), (.51, .37),
                   (.65, .42), (.79, .32), (.86, .15),
                   (.99, .17), (1.10, .05), (1.12, -.18),
                   (.97, -.64), (.79, -1.00), (.79, -1.55)]
    shape = path(contour + [contour[0]], WOOD, 3, True)
    shape.close_path()
    shape.set_fill(SKIN, 1)
    cuff = RoundedRectangle(width=1.6, height=.60, corner_radius=.08,
                            fill_color=TEAL_INK, fill_opacity=1, stroke_width=0)
    cuff.move_to(p(.04, -1.4))
    return VGroup(shape, cuff).set_height(size).rotate(angle).move_to(center)


def compound(center):
    stalk = path([(0, -1.58), (0, -.03), (0, 1.36)], DARK_GREEN, 5)
    middle = leaf("oval", MOSS, p(0, 1.05), 1.83)
    left = leaf("oval", FERN, p(-.9, -.06), 1.83, .83)
    right = leaf("oval", MOSS, p(.9, -.06), 1.83, -.83)
    junction = p(0, -.98)
    petioles = VGroup(*[Line(junction, side.veins[0].point_from_proportion(.27),
                             color=DARK_GREEN, stroke_width=4)
                        for side in (left, right)])
    return VGroup(stalk, petioles, middle, left, right).move_to(center)


def person(center, size, color):
    head = Circle(radius=.24, fill_color=SKIN, fill_opacity=1, stroke_width=0).shift(UP * .91)
    coat = path([(-.28, .51), (-.49, -.02), (-.29, -.18), (-.19, .04),
                 (-.21, -.41), (.22, -.41), (.20, .02), (.32, -.17),
                 (.50, -.02), (.29, .51), (-.28, .51)], color, 0)
    coat.close_path()
    coat.set_fill(color, 1)
    legs = VGroup(Line(p(-.11, -.37), p(-.21, -.98)),
                  Line(p(.11, -.37), p(.26, -.98))).set_stroke(INK, 8)
    return VGroup(head, legs, coat).set_height(size).move_to(center)


def final_sort():
    maple = leaf("maple", FALL_RED, LEFT_HOOP, 3.45, .07)
    toothed = leaf("toothed", FERN, RIGHT_HOOP + p(.31, -.18), 2.73, -.25)
    labels = VGroup(label("Lobes", HOOP_LABELS[0]), label("No lobes", HOOP_LABELS[1]))
    question = prompt("Which hoop will hold more?")
    return maple, toothed, labels, question


def predict_picture():
    red = leaf("maple", FALL_RED, p(-2.48, .30), 4.43, .06)
    ring = hoop(p(3.02, .28), 4.5, 4.1)
    mark = T("?", 105, TEAL_INK, font=TITLE_FONT).move_to(ring)
    return red, ring, mark


def key_branch(answer=True):
    chips = VGroup(*[
        boxed_label(text, color=TEAL_INK, size=36, pad=.23, fill_opacity=.08).move_to(p(x, -1.47))
        for text, x in [("Needle?", -3.55), ("Yes", 0), ("Pine", 3.55)]
    ])
    arrows = VGroup(*[Arrow(a.get_right() + RIGHT * .21, b.get_left() + LEFT * .21,
                            buff=0, color=TEAL_INK, stroke_width=5,
                            max_tip_length_to_length_ratio=.22)
                      for a, b in zip(chips, chips[1:])])
    return VGroup(chips, arrows) if answer else (chips, arrows)


class S00Hook(SpokenScene):
    def construct(self):
        tabletop(self)
        samples = VGroup(leaf("oak", MOSS, p(-4.64, -.42), 3.62, .86),
                         leaf("oval", FALL_YELLOW, p(-4.30, .8), 3.66, .45),
                         leaf("toothed", FERN, p(-2.95, .73), 3.84, -.43),
                         leaf("maple", FALL_RED, p(-1.85, -.12), 3.62, -.54))
        sorting_ring = hoop(p(3.13, .27), 5.08, 4.88)
        self.add(sorting_ring, samples)
        self.at("which leaf clues")
        self.play(samples[-1].animate.move_to(p(3.13, .29)).rotate(.46),
                  run_time=2.05)
        self.at("in 30 minutes")
        self.play(samples[0].animate.shift(LEFT * .31 + DOWN * .25).rotate(.11),
                  samples[1].animate.shift(LEFT * .18 + UP * .22).rotate(.14),
                  samples[2].animate.shift(RIGHT * .41 + UP * .06).rotate(-.17),
                  run_time=2.25)
        self.at("test which clues")
        self.play(Create(samples[-1].blade.copy().set_fill(opacity=0)
                         .set_stroke(PAPER, 4)), run_time=1.55)
        self.finish()


class S01Title(TitleCard):
    TITLE = "Leaf Detectives: Parent Guide"
    LESSON = "Leaf Detectives"

    def construct(self):
        tabletop(self)
        title = T(self.TITLE, 50, INK, font=TITLE_FONT).move_to(p(0, .07))
        rule = Line(p(-1.26, -.7), p(1.26, -.7), color=WOOD, stroke_width=4)
        upper = leaf("maple", FALL_ORANGE, p(-4.78, 1.63), 1.67, .68)
        lower = leaf("oak", MOSS, p(4.72, -1.58), 1.68, -1.05)
        for sample in (upper, lower):
            sample.set_opacity(.41)
            bob(sample, amp=.075, speed=3)
        self.add(upper, lower)
        self.play(FadeIn(title), GrowFromCenter(rule), run_time=.5)
        self.wait(max(.1, self.narration_s - self.elapsed()))


class S02Payoff(SpokenScene):
    def construct(self):
        tabletop(self)
        close = leaf("oak", MOSS, p(-4.01, -.82), 2.95, .15)
        sort = leaf("oval", FALL_YELLOW, p(-.10, -.98), 2.65, -.22)
        season = leaf("maple", FALL_RED, p(3.98, -.78), 2.77)
        glass = magnifier(p(-4.34, 1.1))
        loops = VGroup(hoop(p(-.89, 1.25), 1.40, 1.34), hoop(p(.88, 1.25), 1.40, 1.34))
        loops.set_z_index(-1)
        sky = sun(p(2.88, 1.42), .60)
        self.add(close, sort, season)
        self.at("looking closely")
        self.play(FadeIn(glass, shift=DOWN * .25), run_time=.55)
        self.play(glass.animate.shift(DOWN * .82 + RIGHT * .19), run_time=.97)
        self.at("sorting by one rule")
        self.play(Create(loops), run_time=.7)
        self.play(sort.animate.scale(.53).move_to(p(-.89, 1.25)), run_time=1.58)
        self.at("asking a question")
        q = T("?", 64, TEAL_INK, font=TITLE_FONT).move_to(p(.88, 1.26))
        self.play(FadeIn(q), glass.animate.shift(DOWN * .51), run_time=.9)
        self.at("checking it")
        self.play(FadeOut(q), run_time=.24)
        self.play(sort.animate.move_to(p(.88, 1.25)),
                  close.animate.scale(1.24).shift(p(-.34, .45)),
                  glass.animate.shift(p(-.34, .45)), run_time=1.51)
        self.at("instead of memorizing")
        self.play(FadeIn(sky), run_time=.62)
        self.play(sky.animate.shift(RIGHT * 1.47).rotate(PI / 3), run_time=1.43)
        self.at("they discover which")
        self.play(Transform(season, leaf("maple", MOSS, p(3.98, -.78), 2.77)),
                  sky.animate.shift(LEFT * .39 + UP * .18).rotate(PI / 2), run_time=2.52)
        self.finish()


class S03Gather(SpokenScene):
    def construct(self):
        tabletop(self)
        carrier = basket(p(-4.35, .29))
        loops = VGroup(hoop(p(-1.72, -.42), 1.38, 2.18), hoop(p(-.98, .26), 1.38, 2.18))
        sheets = VGroup(paper(p(1.02, .35), 2.1, 2.8).rotate(.20),
                        paper(p(1.24, .39), 2.1, 2.8).rotate(.08))
        wax = crayon(p(4.42, .25), 2.95, -.64)
        self.at("grab a bag")
        self.play(FadeIn(carrier, shift=RIGHT * .54), run_time=1.54)
        self.at("two hoops")
        self.play(GrowFromCenter(loops), run_time=1.25)
        self.at("thin paper")
        self.play(FadeIn(sheets, shift=RIGHT * .49), run_time=.63)
        self.at("peeled crayon")
        self.play(FadeIn(wax, shift=RIGHT * .62), run_time=.53)
        self.play(wax.animate.rotate(.49).shift(UP * .15 + RIGHT * .14), run_time=1.34)
        self.at("take a 10")
        self.play(FadeOut(VGroup(loops, sheets, wax), shift=LEFT * .55),
                  carrier.animate.scale(.73).move_to(p(-4.68, .12)), run_time=1.37)
        samples = collection(p(1.83, -.05), size=1.50)
        self.at("collect 8 to 12")
        self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * .86) for m in samples],
                              lag_ratio=.18), run_time=2.77)
        self.at("printed leaf photos")
        cards = VGroup(*[VGroup(paper(p(x, .06), 2.72, 3.38),
                               leaf(kind, color, p(x, .14), 2.46, angle))
                         for x, kind, color, angle in [(0, "oak", MOSS, .12),
                                                       (3.02, "maple", FALL_RED, -.21)]])
        self.play(FadeOut(samples, shift=UP * .25), run_time=.40)
        self.play(FadeIn(cards, shift=RIGHT * .52), run_time=1.65)
        self.finish()


class S04Safety(SpokenScene):
    def construct(self):
        tabletop(self)
        trail = path([(-5.25, -1.95), (-3.39, -.70), (-1.36, 1.12), (.10, 2.37)],
                     "#C19867", 112, True)
        trail_edge = trail.copy().set_stroke(PAPER, 2)
        adult = person(p(-4.33, .45), 3.34, TEAL_INK)
        child = person(p(-2.20, .14), 2.43, WAX)
        fallen = leaf("oak", FALL_ORANGE, p(2.43, .34), 2.93, -.36)
        self.add(trail, trail_edge, adult, child, fallen)
        self.at("stay with your child")
        self.play(adult.animate.shift(p(.35, .29)), child.animate.shift(p(.46, .39)),
                  run_time=2.4)
        self.at("within arms reach")
        self.play(child.animate.shift(p(-.63, .12)), adult.animate.shift(p(.24, .18)),
                  run_time=2.44)
        self.at("collect only fallen")
        self.play(FadeOut(VGroup(trail, trail_edge, adult, child)), run_time=.48)
        self.play(fallen.animate.move_to(p(-2.60, .28)).scale(1.18), run_time=1.14)
        checked = label("Fallen leaves only", p(-.52, -3.17), color=TEAL_INK)
        self.play(FadeIn(checked), run_time=.55)

        unfamiliar = leaf("toothed", FERN, p(-2.70, .42), 3.32, .40)
        pointing = hand(p(-4.49, -.66), -.64, 2.66, point=True)
        ivy = compound(p(2.62, .26)).scale(1.12)
        self.at("leave unfamiliar leaves")
        self.play(FadeOut(checked), Transform(fallen, unfamiliar), run_time=.48)
        self.play(FadeIn(pointing, shift=p(.44, .22)), run_time=.81)
        self.at("three leaflets")
        self.play(FadeIn(ivy, shift=UP * .23), FadeOut(pointing, shift=DOWN * .38),
                  run_time=.78)
        ban = crossout(p(2.62, .26), 4.66)
        self.play(Create(ban), run_time=1.35)
        self.at("dead or fallen poison ivy")
        warning = label("Leave it on the ground", p(-.52, -3.17), color=STOP)
        self.play(FadeIn(warning), fallen.animate.shift(LEFT * .38), run_time=.85)
        self.play(ivy.animate.set_opacity(.67), run_time=2.0)

        fungus = VGroup(
            RoundedRectangle(width=.72, height=1.45, corner_radius=.2,
                             fill_color=PAPER, fill_opacity=1, stroke_color=WOOD,
                             stroke_width=3).shift(DOWN * .33),
            AnnularSector(inner_radius=0, outer_radius=1.2, angle=PI,
                          start_angle=0, fill_color="#A9714C", fill_opacity=1,
                          stroke_color=WOOD, stroke_width=3).shift(UP * .23),
        ).move_to(p(2.62, .26))
        self.at("never taste any")
        food_bans = VGroup(crossout(fallen.get_center(), 4.02),
                           crossout(fungus.get_center(), 3.48))
        self.play(FadeOut(VGroup(warning, ivy, ban)), FadeIn(fungus),
                  run_time=.49)
        self.play(Create(food_bans), run_time=.83)
        tasting = label("Never taste", p(-.52, -3.17), color=STOP)
        self.play(FadeIn(tasting), run_time=.44)

        palms = VGroup(hand(p(-.99, -.03), -.57, 3.38),
                       hand(p(.99, -.03), .58, 3.38))
        bubbles = VGroup(*[
            Circle(radius=r, stroke_color=TEAL_INK, stroke_width=2,
                   fill_color=PAPER, fill_opacity=.89).move_to(p(x, y))
            for x, y, r in [(-.75, .64, .31), (-.23, .82, .36), (.43, .72, .37),
                            (.77, 1.12, .22), (0, 1.43, .24), (-.60, 1.58, .13)]
        ])
        self.at("wash hands")
        self.play(FadeOut(VGroup(fallen, food_bans, fungus, tasting)),
                  FadeIn(palms), run_time=.48)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in bubbles], lag_ratio=.13),
                  palms.animate.shift(UP * .28), run_time=1.25)

        fragments = VGroup(crayon(p(-1.91, .5), .93, -.3),
                           crayon(p(-.88, -.18), .49, .5),
                           leaf("oval", MOSS, p(.74, .85), .94, -.38),
                           leaf("oak", FALL_ORANGE, p(1.7, -.08), 1.14, .14))
        tray = paper(p(.03, .35), 5.2, 3.2)
        moving_hand = hand(p(-2.86, -1.0), -.7, 2.28, point=True)
        self.at("keep crayon pieces")
        self.play(FadeOut(VGroup(palms, bubbles)), FadeIn(tray), run_time=.43)
        self.add(fragments, moving_hand)
        supplies = VGroup(tray, fragments, moving_hand)
        self.at("away from children")
        self.play(supplies.animate.shift(p(2.69, 1.03)), run_time=1.61)
        self.play(FadeIn(label("Keep out of reach", p(-.52, -3.17), size=31,
                               color=STOP)), run_time=.42)
        self.finish()


class S05FirstSort(SpokenScene):
    def construct(self):
        tabletop(self)
        samples = collection()
        self.at("spread out the leaves")
        self.play(LaggedStart(*[FadeIn(m, shift=(m.get_center() - ORIGIN) * .31)
                                for m in samples], lag_ratio=.12), run_time=2.32)
        large = leaf("oak", MOSS, p(-1.22, .12), 4.50, -.10)
        self.at("look at their edges")
        self.play(FadeOut(samples), FadeIn(large), run_time=.42)
        pointer = Dot(large.blade.get_right(), radius=.13, color=PAPER,
                      stroke_color=TEAL_INK, stroke_width=3)
        self.add(pointer)
        edge = large.blade.copy().pointwise_become_partial(large.blade, .22, .42)
        pointer.move_to(edge.get_start())
        self.play(MoveAlongPath(pointer, edge), run_time=.69)
        self.at("veins and tips")
        midrib = large.veins[0].copy().pointwise_become_partial(large.veins[0], .38, .91)
        self.play(pointer.animate.move_to(midrib.get_start()), run_time=.21)
        self.play(MoveAlongPath(pointer, midrib), run_time=.52)
        self.play(pointer.animate.move_to(large.blade.get_top()), run_time=.59)
        self.at("keep spiny leaves")
        spiny = leaf("holly", DARK_GREEN, p(2.61, .39), 3.83, -.15)
        adult = hand(p(4.72, -1.02), .58, 2.56, point=True)
        self.play(FadeOut(pointer), FadeIn(spiny), FadeIn(adult), run_time=.58)
        self.play(spiny.animate.shift(p(2.35, .25)).scale(.68),
                  adult.animate.shift(p(1.12, .15)).scale(.78), run_time=1.76)
        self.at("let your child sort")
        rings = sort_hoops()
        scattered = VGroup(*collection(size=1.16)[:7])
        piles = sorted_leaves()
        self.play(FadeOut(VGroup(spiny, adult, large)), FadeIn(rings),
                  FadeIn(scattered), run_time=.60)
        self.play(LaggedStart(*[Transform(sample, dest)
                                for sample, dest in zip(scattered, piles)],
                              lag_ratio=.18), run_time=2.58)
        self.at("then ask")
        question = prompt("What was your rule?")
        self.play(FadeIn(question), run_time=.46)
        self.at("write down their words")
        note = paper(p(0, .17), 1.27, 1.89).rotate(-.09)
        scribble = VGroup(*[Line(p(-.38, y), p(x, y), color=WOOD, stroke_width=2)
                            for x, y in [(.36, .56), (.28, .34), (.36, .12), (.12, -.10)]])
        self.play(FadeIn(note), run_time=.31)
        self.play(Create(scribble), run_time=.85)
        self.play(FadeOut(VGroup(note, scribble, question)), run_time=.32)
        self.finish()


class S06OneFeature(SpokenScene):
    def construct(self):
        tabletop(self)
        rings = sort_hoops()
        piles = sorted_leaves()
        self.add(rings, piles)
        self.at("sort by one feature")
        oak = piles[0]
        self.play(FadeOut(VGroup(*piles[1:]), shift=UP * .40),
                  Transform(oak, leaf("oak", MOSS, p(.58, .42), 2.66, -.14)),
                  run_time=1.47)
        needle = leaf("needle", MOSS, p(-.63, .59), 2.42, .11)
        self.at("try one leaf")
        self.play(FadeIn(needle, shift=LEFT * .3), run_time=.53)
        left_pos, right_pos = HOOP_LABELS
        needle_flat = VGroup(label("Needle", left_pos), label("Flat", right_pos))
        self.at("first needle")
        self.play(needle.animate(run_time=1.21).move_to(LEFT_HOOP).rotate(-.18),
                  oak.animate(run_time=1.21).move_to(RIGHT_HOOP).rotate(.14),
                  FadeIn(needle_flat, run_time=.20))

        oval = leaf("oval", MOSS, LEFT_HOOP, 2.73, .10)
        smooth_tooth = VGroup(label("Smooth", left_pos), label("Toothed", right_pos))
        self.at("smooth edge or toothed", lead=.40)
        self.play(FadeOut(needle_flat), run_time=.20)
        self.at("smooth edge or toothed")
        self.play(Succession(FadeOut(needle, run_time=.20),
                             FadeIn(oval, run_time=.27)),
                  Transform(oak, leaf("toothed", FERN, RIGHT_HOOP, 2.73, -.10),
                            run_time=.65),
                  FadeIn(smooth_tooth, run_time=.20))

        red, final_tooth, lobes, question = final_sort()
        self.at("lobes or no lobes", lead=-.25)
        self.play(FadeOut(smooth_tooth), FadeOut(oval, shift=UP * .39),
                  FadeIn(red, shift=RIGHT * .44), run_time=.69)
        self.play(FadeIn(lobes), run_time=.40)
        self.at("before each round")
        self.play(Transform(oak, final_tooth), run_time=1.21)
        self.at("which hoop do you")
        self.play(FadeIn(question), run_time=.70)
        self.finish()


class S07PredictQuestion(SpokenScene):
    def construct(self):
        tabletop(self)
        red, ring, mark = predict_picture()
        previous_rings = sort_hoops()
        previous_red, previous_tooth, labels, previous_question = final_sort()
        self.add(previous_rings, previous_red, previous_tooth, labels, previous_question)
        initial_red = red.copy().shift(p(-.78, -.39)).rotate(-.31)
        self.at("a bright red leaf")
        self.play(FadeOut(VGroup(previous_rings, previous_tooth, labels, previous_question)),
                  ReplacementTransform(previous_red, initial_red), run_time=2.2)
        self.at("imagine using that")
        self.play(GrowFromCenter(ring), run_time=1.48)
        self.play(FadeIn(mark), run_time=.86)
        self.at("leaves from the same tree")
        self.play(FadeIn(prompt("Same pile in summer?")), run_time=.46)
        self.play(ReplacementTransform(initial_red, red, rate_func=linear),
                  run_time=self.narration_s + .29 - self.elapsed())
        self.finish()


class S08PredictPause(Scene):
    def construct(self):
        tabletop(self)
        self.add(*predict_picture(), prompt("Same pile in summer?"))
        self.wait(float(os.environ["KX_DURATION"]))


class S09PredictReveal(SpokenScene):
    def construct(self):
        tabletop(self)
        red, ring, mark = predict_picture()
        question = prompt("Same pile in summer?")
        self.add(red, ring, mark, question)
        summer = label("Summer", p(-2.48, -2.42), color=TEAL_INK)
        fall = label("Possible fall colors", p(3.02, -2.42))
        self.at("a red maple leaf")
        self.play(FadeOut(ring, shift=RIGHT * .52), FadeOut(mark, shift=RIGHT * .52),
                  FadeOut(question), run_time=.75)
        self.at("can be green")
        self.play(Transform(red, leaf("maple", MOSS, p(-2.48, .30), 4.43, .06)),
                  run_time=.84)
        self.play(FadeIn(summer), run_time=.47)
        self.at("in fall it can")
        self.play(FadeIn(fall), run_time=.63)
        colors = VGroup(*[leaf("maple", color, p(x, .34), 1.97, angle)
                          for color, x, angle in [(FALL_RED, 1.21, .06),
                                                   (FALL_ORANGE, 3.26, .06),
                                                   (FALL_YELLOW, 5.31, .06)]])
        for cue, sample in zip(("can be red", "orange or yellow", "or yellow"), colors):
            self.at(cue, lead=.23)
            self.play(FadeIn(sample, shift=UP * .25), run_time=.40)
        self.at("what color was this")
        july = prompt("What color in July?")
        self.play(FadeIn(july), run_time=.49)
        self.play(colors[0].animate.shift(UP * .44).rotate(.08), run_time=1.45)
        self.at("two differently colored leaves")
        self.play(FadeOut(VGroup(colors[1], colors[2], fall, summer, july)), run_time=.48)
        target = leaf("maple", FALL_RED, p(2.48, .30), 4.43, .06)
        self.play(Transform(colors[0], target), run_time=1.57)
        self.at("compare their shapes")
        self.play(*[Create(sample.blade.copy().set_fill(opacity=0).set_stroke(PAPER, 4))
                    for sample in (red, target)], run_time=1.76)
        self.finish()


class S10RubbingsAndKey(SpokenScene):
    def construct(self):
        tabletop(self)
        sample = leaf("maple", MOSS, p(0, .12), 4.31, .06)
        sheet = paper(p(0, .14), 6.19, 4.86)
        self.add(sample)
        self.at("under thin paper")
        self.play(FadeIn(sheet.set_fill(opacity=.73), shift=LEFT * 3.42), run_time=2.28)
        wax = crayon(p(-.80, 1.85), 3.32, -.13)
        rubbing = leaf("maple", WAX, p(0, .12), 4.31, .06, rubbing=True)
        self.at("rub with the side")
        self.play(FadeIn(wax, shift=p(.37, -.40)),
                  sheet.animate.set_fill(opacity=1), run_time=.51)
        self.remove(sample)
        self.play(wax.animate.shift(p(1.65, -.61)).rotate(.17),
                  Create(VGroup(*rubbing.veins[1:3])), run_time=1.05)
        self.play(wax.animate.shift(p(-1.75, -.75)).rotate(-.10),
                  Create(VGroup(*rubbing.veins[3:])), run_time=1.06)
        self.at("the veins and edges")
        self.play(wax.animate.shift(p(1.83, -1.02)), Create(rubbing.blade),
                  Create(rubbing.veins[0]), run_time=1.55)
        self.play(wax.animate.shift(p(2.23, .12)), run_time=.66)
        self.at("for older children")
        self.play(FadeOut(VGroup(sheet, rubbing, wax)), run_time=.53)
        pine = leaf("needle", MOSS, p(0, .92), 3.34, .09)
        self.play(FadeIn(pine, shift=DOWN * .50), run_time=1.56)
        chips, arrows = key_branch(answer=False)
        self.at("ask whether the leaf")
        self.play(FadeIn(chips[0]), pine.animate.rotate(-.13), run_time=1.28)
        self.at("if it is")
        self.play(GrowArrow(arrows[0]), FadeIn(chips[1]), run_time=1.01)
        self.at("leads to pine")
        self.play(GrowArrow(arrows[1]), FadeIn(chips[2]), run_time=.98)
        self.finish()


def question_sheet():
    sheet = paper(p(2.89, 1.05), 4.4, 3.15)
    first = label("Needle?", p(2.24, 2.02), 33, TEAL_INK)
    second = label("Pointy?", p(2.24, 1.12), 33, TEAL_INK)
    revised = label("Lobes?", p(2.24, 1.12), 33, TEAL_INK)
    last = Line(p(1.46, .22), p(4.25, .22), color=WOOD, stroke_width=2)
    return sheet, first, second, revised, last


class S11Closing(SpokenScene):
    def construct(self):
        tabletop(self)
        branch = key_branch()
        pine = leaf("needle", MOSS, p(0, .92), 3.34, -.04)
        self.add(branch, pine)
        family = VGroup(leaf("oak", MOSS, p(-3.04, .78), 2.48, .39),
                        leaf("oval", FALL_ORANGE, p(-1.52, .74), 2.19, -.46))
        self.at("a key only covers")
        self.play(pine.animate.scale(.71).move_to(p(-4.54, .67)),
                  FadeIn(family, shift=LEFT * .55), run_time=2.49)
        sheet, first, second, revised, last = question_sheet()
        writing_hand = hand(p(4.06, .92), .49, 1.35, point=True)
        self.at("help your child write")
        self.play(FadeIn(sheet, shift=DOWN * .37), run_time=.58)
        self.play(FadeIn(writing_hand), Write(first), run_time=.75)
        self.play(writing_hand.animate.shift(DOWN * .45), Write(second),
                  Create(last), run_time=1.01)
        other_hand = hand(p(-4.73, -.17), -.88, 1.70, point=True)
        sample = family[0]
        self.at("give someone a leaf")
        self.play(FadeOut(writing_hand), FadeIn(other_hand), run_time=.43)
        self.play(sample.animate.move_to(p(-.64, .98)), family[1].animate.move_to(p(-2.86, .69)),
                  other_hand.animate.shift(RIGHT * 2.52), run_time=1.45)
        route = Arrow(p(.08, 1.25), p(1.12, 1.75), buff=0, color=TEAL_INK,
                      stroke_width=4, max_tip_length_to_length_ratio=.23)
        self.at("try the key")
        self.play(GrowArrow(route), FadeOut(other_hand), run_time=.86)
        self.at("rewrite any question")
        circle = SurroundingRectangle(second, color=STOP, corner_radius=.18,
                                      stroke_width=4, buff=.18)
        self.play(Create(circle), sample.animate.shift(LEFT * .74).rotate(-.20),
                  run_time=.78)
        self.play(Uncreate(circle), run_time=.45)
        self.play(swap(second, revised), run_time=.78)
        self.at("choosing clues that stay")
        self.play(FadeOut(route), FadeOut(family[1]), FadeOut(pine),
                  sample.animate.scale(1.32).move_to(p(-2.91, .85)), run_time=1.40)
        self.play(Create(sample.blade.copy().set_fill(opacity=0).set_stroke(PAPER, 5)),
                  run_time=1.1)
        self.finish()


class S12End(EndCard):
    LINE = "Sort leaves by steady shapes and edges, not seasonal color."
