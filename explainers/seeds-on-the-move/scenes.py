"""Illustrated parent guide. The yard, work surface and drop rig are shared across scenes."""

from bp_parts import *


# Color map: GREEN/fern = growing plants, GOLD = wings and seed coats,
# BLUE/TEAL = water and sock wool, RED = safety, warm paper = collected specimens.
FERN = "#315d44"
LEAF = "#5f995c"
MEADOW = "#24483e"
HILL = "#1d393b"
PATH = "#96765a"
PATH_EDGE = "#5f4c43"
TABLE = "#706151"
PAPER = "#f4e6c9"
SKY = "#182936"
WOOL = "#287580"
WOOL_LIGHT = "#88d0cb"
INK = "#263547"
SKIN = "#dca17d"
CLAY = "#ba7356"
BERRY = "#bc5974"
LINE = "#a8bdc9"


def pt(x, y):
    return np.array([x, y, 0.0])


def outline(start, *segments, fill, edge=None, width=2):
    shape = VMobject()
    shape.start_new_path(pt(*start))
    for segment in segments:
        if len(segment) == 2:
            shape.add_line_to(pt(*segment))
        else:
            shape.add_cubic_bezier_curve_to(*(pt(*p) for p in segment))
    shape.close_path()
    return shape.set_fill(fill, 1).set_stroke(edge or fill, width)


def panel(w, h, x, y, color, edge=None, radius=.25):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, fill_color=color, fill_opacity=1,
        stroke_color=edge or color, stroke_width=2 if edge else 0,
    ).move_to(pt(x, y))


def disk(x, y, r, color, edge=None):
    return Circle(radius=r, color=edge or color, fill_color=color, fill_opacity=1,
                  stroke_width=2 if edge else 0).move_to(pt(x, y))


def stroke(a, b, color=LINE, width=3):
    return Line(pt(*a), pt(*b), color=color, stroke_width=width)


def label(s, x, y, size=34, color=TEXT):
    return T(s, size, color, weight=BOLD).move_to(pt(x, y))


def tag(s, x, y, color=TEAL):
    return boxed_label(s, color=color, size=30, pad=.22).move_to(pt(x, y))


def sway(mob, pivot, speed=2.0, amplitude=.11, phase=0):
    """Rock a drawing around its own planted base."""
    clock = 0.0
    last = 0.0

    def rock(obj, dt):
        nonlocal clock, last
        clock += dt
        angle = amplitude * (np.sin(speed * clock + phase) - np.sin(phase))
        obj.rotate(angle - last, about_point=pivot)
        last = angle

    mob.add_updater(rock)
    return mob


def meadow_stem(x, y, height, phase, motion):
    stalk = VMobject().set_points_as_corners([pt(0, 0), pt(.03, .37), pt(.11, .75), pt(.22, 1.02)])
    stalk.set_stroke(LEAF, 5)
    leaves = VGroup(
        outline((.03, .29), ((-.31, .32), (-.47, .52), (-.44, .64)),
                ((-.16, .62), (-.04, .44), (.03, .29)), fill=FERN, edge=LEAF),
        outline((.08, .51), ((.3, .75), (.53, .74), (.57, .77)),
                ((.54, .57), (.3, .52), (.08, .51)), fill=FERN, edge=LEAF),
    )
    head = VGroup()
    for level in range(5):
        for side in [-1, 1]:
            head.add(Ellipse(width=.18, height=.34 - .027 * level, fill_color=GOLD if level > 1 else PATH,
                             fill_opacity=1, stroke_width=0).rotate(-side * .56)
                     .move_to(pt(.19 + .035 * level + side * (.09 - .012 * level), 1.02 + level * .12)))
    stem = VGroup(stalk, leaves, head).scale(height / 1.65, about_point=ORIGIN).shift(pt(x, y))
    return sway(stem, pt(x, y), 1.6 + .15 * phase, .105, phase) if motion else stem


def yard(motion=True):
    """A sunny verge with open sky reserved for cues and an unobstructed path."""
    backdrop = VGroup(
        panel(13.55, 7.52, 0, 0, SKY, radius=.32),
        disk(-5.42, 2.53, .57, "#826e47"),
        disk(-5.42, 2.53, .39, "#eed28c"),
        outline((-6.68, -1.5), (-6.68, -.48), ((-3.7, 1.54), (-1.9, .27), (.5, .22)),
                ((2.55, .21), (4.15, 1.32), (6.68, .27)), (6.68, -1.5), fill=HILL, width=0),
        outline((-6.68, -3.64), (-6.68, -1.38),
                ((-3.7, -.8), (.8, -.94), (3.52, -.52)), ((4.65, -.34), (5.86, -.59), (6.68, -.79)),
                (6.68, -3.64), fill=MEADOW, width=0),
        outline((-6.67, -3.6), (-6.67, -2.83),
                ((-3.4, -1.95), (2.0, -3), (6.67, -1.84)), (6.67, -3.6), fill=PATH_EDGE, width=0),
        outline((-6.64, -3.55), (-6.64, -3.04),
                ((-3.0, -2.2), (2.5, -3.21), (6.64, -2.12)), (6.64, -3.55), fill=PATH, width=0),
    )
    for i, (x, y, h) in enumerate([(1.5, -2.37, 1.2), (2.35, -2.45, 3.4), (3.2, -2.33, 2.6),
                                    (4.06, -2.31, 4.28), (4.89, -2.13, 3.62), (5.28, -2.01, 3.8),
                                    (5.83, -1.87, 2.16)]):
        backdrop.add(meadow_stem(x, y, h, i * .66, motion))
    return backdrop


def maple(wing=True):
    coat = Ellipse(width=.53, height=.39, color=PATH_EDGE, stroke_width=2,
                   fill_color=GOLD, fill_opacity=1).rotate(.29)
    if not wing:
        return VGroup(coat)
    blade = outline((.03, .03), ((.35, .66), (.91, .94), (1.51, .92)),
                    ((1.43, .34), (.81, -.13), (.12, -.14)), fill="#d7b45a", edge=PATH_EDGE)
    veins = VGroup(stroke((.16, -.02), (1.32, .72), "#9a7341", 2),
                   stroke((.56, .24), (1.15, .31), "#9a7341", 1.5),
                   stroke((.48, .2), (.66, .54), "#9a7341", 1.5))
    return VGroup(blade, veins, coat)


def burr():
    husk = VGroup(disk(0, 0, .29, "#b58956", PATH_EDGE))
    for i in range(10):
        theta = i * TAU / 10
        hook = VMobject().set_points_as_corners([pt(.22, 0), pt(.43, 0), pt(.48, .075), pt(.42, .109)])
        hook.set_stroke("#ccaa73", 4).rotate(theta, about_point=ORIGIN)
        husk.add(hook)
    husk.add(disk(-.09, .085, .045, PAPER), disk(.09, -.08, .043, PATH_EDGE))
    return husk


def float_seed():
    shell = Ellipse(width=.74, height=.48, color=PATH_EDGE, stroke_width=2,
                    fill_color="#b78958", fill_opacity=1).rotate(-.16)
    stripe = ArcBetweenPoints(pt(-.31, .01), pt(.31, -.03), angle=.55).set_stroke(PAPER, 2.5)
    return VGroup(shell, stripe)


def berries():
    return VGroup(stroke((-.44, .38), (.22, -.06), LEAF, 5),
                  stroke((-.16, .21), (-.19, -.12), LEAF, 4),
                  disk(-.19, -.18, .22, BERRY, "#773a55"), disk(.24, -.13, .23, BERRY, "#773a55"),
                  disk(-.25, -.1, .043, "#fac6ce"), disk(.17, -.05, .043, "#fac6ce"))


def shoe(wrapped=True):
    sole = outline((-1.9, -.79), (1.82, -.79), ((2.08, -.76), (2.04, -.4), (1.87, -.36)),
                   (-1.98, -.33), ((-2.14, -.47), (-2.11, -.72), (-1.9, -.79)),
                   fill=WOOL_LIGHT if wrapped else PAPER)
    upper = outline((-1.91, -.48), (-1.8, .65), (-.73, .65),
                    ((-.62, .17), (.03, -.02), (.44, -.02)),
                    ((.87, .02), (1.74, .04), (1.89, -.43)), fill=WOOL if wrapped else INK,
                    edge=WOOL_LIGHT if wrapped else LINE, width=3)
    if not wrapped:
        return VGroup(sole, upper, *[stroke((x, -.05), (x + .25, .1), PAPER, 4) for x in [-.35, -.06, .23]])
    cuff = panel(1.16, .37, -1.23, .58, WOOL_LIGHT, radius=.12)
    stitches = VGroup()
    for i in range(32):
        x = -1.69 + (i % 11) * .31
        y = -.34 + (i // 11) * .19
        if y <= -.13 or x < -.56:
            stitches.add(ArcBetweenPoints(pt(x, y), pt(x + .12, y + .025), angle=-1.45)
                         .set_stroke(WOOL_LIGHT, 2.7, opacity=.72))
    return VGroup(sole, upper, cuff, stitches)


def walking_shoe(x=-.65, y=-1.84):
    return shoe().scale(1.23).move_to(pt(x, y))


def empty_sock():
    return shoe().stretch(.85, 1).rotate(-.20)


def bag(plastic=False):
    fill = "#315763" if plastic else "#b28b58"
    edge = BLUE if plastic else "#e4bd7d"
    body = outline((-1.14, 1.33), (1.14, 1.33), (1.31, -1.14), (1.0, -1.36), (-1.1, -1.36),
                   (-1.32, -1.12), fill=fill, edge=edge, width=3)
    if plastic:
        body.set_fill(fill, .55)
    return VGroup(body, stroke((-1.09, 1.12), (1.09, 1.12), edge, 5),
                  stroke((-1.03, -.99), (.97, -.99), edge, 2))


def hand(direction=1):
    palm = outline((-1.04, -.43), (-.58, -.43),
                    ((-.18, -.48), (.08, -.39), (.48, -.24)),
                    ((.83, -.15), (.91, .06), (.71, .15)),
                    ((.63, .26), (.42, .17), (.3, .14)),
                    ((.67, .41), (.76, .59), (.58, .65)),
                    ((.4, .69), (.08, .51), (-.14, .41)),
                    ((-.28, .48), (-.56, .43), (-.65, .2)), (-1.04, .2),
                    fill=SKIN, edge="#925f52", width=2)
    sleeve = panel(.66, .75, -1.11, -.12, WOOL, WOOL_LIGHT, .09)
    g = VGroup(palm, sleeve)
    if direction < 0:
        g.flip(UP)
    return g


def desk():
    return VGroup(panel(13.52, 7.51, 0, 0, SKY, radius=.32),
                  panel(13.22, 4.43, 0, -1.35, TABLE, radius=.29),
                  stroke((-6.31, -2.98), (6.31, -2.98), "#907861", 2),
                  stroke((-6.25, -3.22), (6.25, -3.22), "#907861", 2))


def sheet(x, y, w=5.8, h=3.15):
    return panel(w, h, x, y, PAPER, "#d1bda2", .12)


def prediction_sheet(x, y):
    paper = sheet(x, y, 3.9, 3.45)
    title = label("First ideas", x, y + 1.09, 32, INK)
    rules = VGroup(*[stroke((x - 1.35, y + dy), (x + 1.36, y + dy), "#b6a587", 2)
                     for dy in [.48, -.05, -.58, -1.11]])
    return VGroup(paper, title, rules)


def marks(x, y):
    return VGroup(*[stroke((x - 1.08 + i * .37, y + dy + .09), (x - .84 + i * .37, y + dy + .12),
                           INK, 3) for dy, count in [(0, 5), (-.53, 4)] for i in range(count)])


def lens(radius=.91):
    rim = Circle(radius=radius, color=TEXT, fill_color=BLUE, fill_opacity=.11, stroke_width=6)
    grip = stroke((radius * .68, -radius * .72), (radius * 1.21, -radius * 1.28), TEAL, 15)
    glint = Arc(radius=radius * .76, start_angle=1.13, angle=.97, color=WOOL_LIGHT, stroke_width=4)
    return VGroup(grip, rim, glint)


def fiber_detail():
    yarn = VGroup()
    for y in [-.65, -.15, .35]:
        fiber = VMobject().set_points_smoothly([pt(-1.4, y), pt(-.65, y + .25), pt(.13, y - .06),
                                                pt(.76, y + .16), pt(1.38, y)])
        yarn.add(fiber.set_stroke(WOOL_LIGHT, 9))
    hooked = VMobject().set_points_smoothly([pt(-.35, 1.02), pt(.23, .71), pt(.32, .22),
                                            pt(.09, .10), pt(-.11, .32)])
    hooked.set_stroke(GOLD, 10)
    wide_lens = Circle(radius=1.85, color=TEXT, stroke_width=5, fill_color=WOOL, fill_opacity=1)
    handle = stroke((1.2, -1.39), (2.12, -2.19), TEAL, 19)
    return VGroup(handle, wide_lens, yarn, hooked, disk(-.41, 1.11, .33, "#b58956", PAPER))


def tweezers():
    return VGroup(stroke((-.13, -.72), (-.3, .55), INK, 5),
                  stroke((.08, -.72), (.3, .55), INK, 5),
                  ArcBetweenPoints(pt(-.3, .55), pt(.3, .55), angle=-PI).set_stroke(INK, 5))


def clock_face(radius=.64):
    face = disk(0, 0, radius, INK, WOOL_LIGHT)
    ticks = VGroup(*[Line(UP * radius * .75, UP * radius * .92, color=TEXT, stroke_width=2.5)
                     .rotate(i * TAU / 12, about_point=ORIGIN) for i in range(12)])
    needle = stroke((0, 0), (0, radius * .69), GOLD, 4)
    return VGroup(face, ticks, needle, disk(0, 0, .06, TEXT)), needle


def person(child=False):
    top = CLAY if child else WOOL
    legs = VGroup(stroke((-.2, -1.13), (-.31, -2.06), INK, 19),
                  stroke((.2, -1.13), (.32, -2.06), INK, 19),
                  panel(.53, .31, -.39, -2.07, PAPER), panel(.53, .31, .4, -2.07, PAPER))
    torso = panel(1.15, 1.3, 0, -.58, top, PAPER, .21)
    arm = stroke((.48, -.1), (.75, -.89), top, 19)
    other = stroke((-.48, -.09), (-.71, -.87), top, 19)
    head = VGroup(disk(0, .7, .53, SKIN), disk(-.22, 1.01, .29, INK), disk(.1, 1.09, .32, INK),
                  disk(.23, .68, .046, INK), disk(-.05, .68, .046, INK),
                  ArcBetweenPoints(pt(.03, .51), pt(.21, .51), angle=.8).set_stroke(INK, 2.2))
    return VGroup(legs, other, arm, disk(.75, -.96, .12, SKIN), disk(-.71, -.94, .12, SKIN), torso, head)


def family():
    adult = person().scale(1.05).move_to(pt(-3.98, -.3))
    child = person(True).scale(.76).move_to(pt(-1.92, -.82))
    return VGroup(adult, child)


def bird():
    return VGroup(Ellipse(width=1.4, height=.89, fill_color=CLAY, fill_opacity=1, stroke_width=0),
                  Ellipse(width=.77, height=.44, fill_color=INK, fill_opacity=1, stroke_width=0).rotate(.21),
                  disk(.55, .43, .4, CLAY), disk(.67, .5, .055, INK),
                  outline((.85, .47), (1.23, .31), (.86, .22), fill=GOLD))


def ripples(x, y, width=1.64):
    return VGroup(*[ArcBetweenPoints(pt(x - width / 2, y - i * .21), pt(x + width / 2, y - i * .21),
                                     angle=.28).set_stroke(BLUE, 4.4) for i in range(3)])


class S01Hook(SpokenScene):
    def construct(self):
        self.add(yard())
        question = question_card("How do seeds travel?", y=2.26, left=-4.06, size=49)
        boot = walking_shoe()
        self.at("so how do")
        self.play(FadeIn(question, shift=UP * .12), run_time=.55)
        self.at("an old fuzzy", lead=.9)
        self.play(FadeIn(boot, shift=LEFT * 2.2 + UP * .45), run_time=.86)
        self.at("can catch some")
        self.play(Rotate(boot, -.15, about_point=boot.get_bottom()), rate_func=there_and_back,
                  run_time=1.1)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Seeds on the Move: Parent Guide"
    LESSON = "Seeds on the Move"

    def construct(self):
        title = T(self.TITLE, size=45, font=TITLE_FONT).move_to(pt(.17, 2.63))
        self.add(yard(), walking_shoe(), title)
        self.wait(self.narration_s)


def travel_examples():
    wing = maple().rotate(.13).shift(DOWN * .14)
    wind = VGroup(*[ArcBetweenPoints(pt(-.93, y), pt(.73, y + .1), angle=-.32)
                    .set_stroke(GOLD, 4.1) for y in [-.34, -.59, -.84]])
    flier = VGroup(wind, wing)
    floater = VGroup(ripples(0, -.2), float_seed().scale(1.5).move_to(pt(0, .1)))
    eaten = VGroup(bird().shift(RIGHT * .13), berries().scale(.68).move_to(pt(1.35, .26)))
    carried = VGroup(shoe().scale(.48), burr().scale(.83).move_to(pt(.68, .22)))
    return [flier, floater, eaten, carried]


class S03Payoff(SpokenScene):
    def construct(self):
        backdrop = yard()
        self.add(backdrop, walking_shoe())
        exemplars = travel_examples()
        for example, x in zip(exemplars, [-4.65, -1.57, 1.53, 4.57]):
            example.move_to(pt(x, .35))
            backing = panel(2.70, 2.03, x, .35, "#263d49", radius=.35)
            example.add_to_back(backing)
        self.at("in about 35")
        duration = tag("About 35 minutes", -2.45, 2.63, GOLD)
        self.play(FadeIn(duration), run_time=.55)
        self.at("looking closely")
        glass = lens(.67).move_to(pt(-.18, -1.17))
        self.play(FadeIn(glass, shift=LEFT * .55), run_time=.45)
        self.at("sorting by a rule")
        trial = VGroup(maple().scale(.66).move_to(pt(-4.2, .67)),
                       float_seed().move_to(pt(-2.81, .62)), burr().move_to(pt(-1.53, .61)))
        self.play(FadeOut(glass), FadeIn(trial, shift=RIGHT * .3), run_time=.55)
        self.at("testing a guess")
        guess = question_card("Which will float?", y=1.60, left=-1.2, size=36)
        self.play(FadeIn(guess), run_time=.38)
        self.at("they notice how")
        self.play(FadeOut(trial), FadeOut(guess), FadeOut(duration), FadeOut(backdrop[10:]),
                  run_time=.38)
        self.at("seeds travel by", lead=.52)
        self.play(FadeIn(exemplars[0], shift=UP * .28), run_time=.40)
        self.at("wind", lead=.1)
        self.play(FadeIn(label("Wind", -4.65, 1.68, color=GOLD)), run_time=.23)
        self.at("water and", lead=.5)
        self.play(FadeIn(exemplars[1], shift=UP * .28), run_time=.30)
        self.play(FadeIn(label("Water", -1.57, 1.68, color=BLUE)), run_time=.23)
        self.at("animals including", lead=.34)
        self.play(FadeIn(exemplars[2], shift=UP * .25), run_time=.26)
        self.play(FadeIn(label("Animals", 1.53, 1.68)), run_time=.23)
        self.at("including people", lead=.18)
        self.play(FadeIn(exemplars[3], shift=UP * .25), run_time=.34)
        self.play(FadeIn(label("People", 4.57, 1.68, color=WOOL_LIGHT)), run_time=.27)
        for i, example in enumerate(exemplars):
            bob(example[-1], amp=.07, speed=3, seed=i)
        self.finish()


class S04Walk(SpokenScene):
    def construct(self):
        self.add(yard())
        ideas = prediction_sheet(-3.78, -.34)
        written = marks(-3.78, -.34)
        q = boxed_label("How do seeds get\nto new places?", size=39, color=GOLD,
                        pad=.29).move_to(pt(.4, 2.49))
        self.at("ask how do")
        self.play(FadeIn(q), FadeIn(ideas, shift=UP * .22), run_time=.55)
        self.at("write down their")
        self.play(LaggedStart(*[Create(mark) for mark in written], lag_ratio=.26), run_time=1.5)
        self.at("slip the sock", lead=.35)
        boot = shoe(False).scale(1.23).move_to(pt(-2.4, -1.84))
        wrap = walking_shoe(-2.4, -1.84)
        self.play(FadeOut(q), FadeOut(ideas), FadeOut(written), FadeIn(boot), run_time=.45)
        self.play(FadeIn(wrap, shift=UP * .52), run_time=.64)
        self.remove(boot)
        self.at("walk slowly along")
        self.play(wrap.animate.move_to(pt(-.15, -1.6)), run_time=1.0)
        timer, needle = clock_face()
        timer.move_to(pt(-3.4, 1.79))
        self.at("edge for three", lead=.32)
        self.play(FadeIn(timer), run_time=.32)
        timing = label("3 to 5 min", -3.4, .77, color=GOLD)
        self.play(FadeIn(timing), run_time=.28)
        self.play(wrap.animate.move_to(pt(1.18, -1.84)),
                  Rotate(needle, -TAU, about_point=timer[0].get_center()), run_time=1.3)
        self.at("collect only seeds")
        maple_key = maple().scale(.8).move_to(pt(-.56, -2.68))
        paper_bag = bag().scale(.8).move_to(pt(2.6, -.22))
        fingers = hand().scale(.77).move_to(pt(-1.36, -2.37))
        self.play(FadeOut(wrap), FadeOut(timing), FadeOut(timer),
                  FadeIn(paper_bag), FadeIn(maple_key), run_time=.46)
        self.play(FadeIn(fingers, shift=UP * .62), run_time=.48)
        self.at("like maple keys", lead=.30)
        self.play(fingers.animate.shift(pt(2.4, 2.57)), maple_key.animate.shift(pt(2.8, 2.74)),
                  run_time=.60)
        self.play(FadeOut(maple_key, shift=DOWN * .55), FadeOut(fingers, shift=UP * .30), run_time=.44)
        self.finish()


def sock_check():
    step = panel(13.1, 4.18, 0, -1.44, PATH_EDGE, radius=.19)
    paper = sheet(-.97, -.79, 8.1, 4.17).set_stroke(width=0)
    sock = empty_sock().scale(1.29).move_to(pt(-1.08, -.66))
    return step, paper, sock


class S05Check(SpokenScene):
    def construct(self):
        step, paper, sock = sock_check()
        hooked = burr().scale(.76).move_to(pt(-.39, -.77))
        second = burr().scale(.63).move_to(pt(-1.62, -.47))
        loose = VGroup(sock, hooked, second)
        outdoor = yard()
        self.add(outdoor, step, paper)
        self.at("stay outdoors to")
        self.play(FadeIn(loose, shift=UP * .45), run_time=.66)
        self.at("lay it on")
        self.play(loose.animate.shift(DOWN * .30), run_time=.76)
        tool = tweezers().scale(.88).move_to(pt(-.4, -.35))
        lifting_hand = hand().scale(.68).move_to(pt(-1.02, .20))
        self.at("pull off", lead=.45)
        self.play(FadeIn(tool, shift=DOWN * .4), FadeIn(lifting_hand, shift=DOWN * .4), run_time=.38)
        first_lift = pt(2.46, -.42)
        self.play(hooked.animate.shift(first_lift), tool.animate.shift(first_lift),
                  lifting_hand.animate.shift(first_lift), run_time=.65)
        reach_back = pt(-3.69, .72)
        self.play(tool.animate.shift(reach_back), lifting_hand.animate.shift(reach_back), run_time=.39)
        second_lift = pt(2.99, -.41)
        self.play(second.animate.shift(second_lift), tool.animate.shift(second_lift),
                  lifting_hand.animate.shift(second_lift), run_time=.63)
        self.at("looking for ticks", lead=.34)
        inspection = lens(.79).move_to(pt(-2.64, -.52))
        notice = tag("Look for ticks", 2.76, 2.2, GOLD)
        self.play(FadeOut(tool), FadeOut(lifting_hand), FadeIn(inspection), run_time=.40)
        self.play(FadeIn(notice), inspection.animate.move_to(pt(.45, -1.0)), run_time=1.52)
        self.at("then seal the")
        sack = bag(True).scale(1.10).move_to(pt(4.69, -.59))
        zip_slider = panel(.27, .22, 3.55, .66, PAPER, radius=.05)
        self.play(FadeOut(inspection), FadeOut(notice), FadeIn(sack), run_time=.42)
        self.play(sock.animate.scale(.48).move_to(pt(4.69, -.61)), run_time=.81)
        self.add(zip_slider)
        self.play(zip_slider.animate.shift(RIGHT * 2.28), run_time=.59)
        self.finish()


SORT_X = (-4.71, -1.57, 1.57, 4.71)
SORT_NAMES = ("Flies", "Floats", "Sticks", "Gets eaten")


def seeds_for_sort():
    return [maple().scale(1.23), float_seed().scale(1.57), burr().scale(1.46), berries().scale(1.42)]


class S06Sort(SpokenScene):
    def construct(self):
        self.add(desk())
        closeup = fiber_detail().scale(1.25).move_to(pt(-.52, .31))
        self.at("use a hand")
        self.play(FadeIn(closeup, scale=.82), run_time=.72)
        self.at("hooks and spines")
        self.play(closeup[3].animate.shift(pt(-.16, -.20)), closeup[4].animate.shift(pt(-.16, -.20)),
                  run_time=1.03)
        self.play(closeup[2].animate.shift(RIGHT * .16), run_time=.98)
        self.at("then make four", lead=.35)
        piles = VGroup(*[sheet(x, -1.13, 2.82, 2.78) for x in SORT_X])
        seeds = seeds_for_sort()
        for seed, x in zip(seeds, SORT_X):
            seed.move_to(pt(x, 1.36))
        self.play(FadeOut(closeup), FadeIn(piles), run_time=.45)
        for name, item, x, color in zip(SORT_NAMES, seeds, SORT_X, [GOLD, BLUE, TEAL, BERRY]):
            name_tag = label(name, x, -2.0, 31, INK)
            cue = {"Flies": "flies floats", "Floats": "floats sticks", "Sticks": "sticks gets",
                   "Gets eaten": "gets eaten"}[name]
            self.at(cue, lead=.27)
            self.play(FadeIn(item, shift=UP * .14), run_time=.20)
            self.play(item.animate.move_to(pt(x, -.77)), FadeIn(name_tag), run_time=.27)
        self.at("why does this")
        question = question_card("Why this pile?", y=2.42, size=40)
        self.play(FadeIn(question), run_time=.40)
        self.play(seeds[2].animate.scale(1.13), rate_func=there_and_back, run_time=1.05)
        self.at("seeds fit two")
        bridge_seed = seeds[0]
        smile = VGroup(disk(0, 0, .38, GOLD), disk(-.12, .10, .034, INK), disk(.12, .10, .034, INK),
                       ArcBetweenPoints(pt(-.14, -.02), pt(.14, -.02), angle=.95).set_stroke(INK, 3))
        smile.move_to(pt(-3.14, 2.05))
        self.play(FadeOut(question), run_time=.25)
        self.play(bridge_seed.animate.scale(.79).move_to(pt(-3.14, .91)), run_time=.97)
        self.play(FadeIn(smile), run_time=.35)
        bob(bridge_seed, amp=.09, speed=3)
        self.finish()


def bowl():
    body = outline((-3.22, .17), ((-2.98, -1.07), (-2.35, -1.66), (0, -1.72)),
                   ((2.35, -1.66), (2.98, -1.07), (3.22, .17)), fill="#284d62", edge=BLUE, width=4)
    top = Ellipse(width=6.45, height=1.30, fill_color="#263d51", fill_opacity=1,
                  color=BLUE, stroke_width=4).shift(UP * .18)
    water = Ellipse(width=5.14, height=.58, fill_color="#3b8aab", fill_opacity=1,
                    color=BLUE, stroke_width=2.5).shift(DOWN * .10)
    return VGroup(body, top, water)


class S07Float(SpokenScene):
    def construct(self):
        surface = desk()
        people = family().scale(.83, about_point=ORIGIN).shift(pt(-1.02, .87))
        people[0].shift(UP * .64)
        people[1].shift(UP * 1.08)
        surface[1:].set_z_index(1)
        basin = bowl().move_to(pt(1.99, -.76)).set_z_index(2)
        self.add(surface, people)
        self.at("stay with your")
        self.play(FadeIn(basin, shift=UP * .21), run_time=.74)
        loose = seeds_for_sort()
        for item, x in zip(loose, [.31, 1.47, 2.69, 3.88]):
            item.scale(.58).move_to(pt(x, 1.25)).set_z_index(3)
        self.at("shallow bowl of")
        self.play(basin[2].animate.set_fill("#529db9"), rate_func=there_and_back, run_time=1.08)
        self.at("ask which seeds")
        question = question_card("Which seeds will float?", y=2.50, left=-.9, size=39).set_z_index(4)
        self.play(FadeIn(question), LaggedStart(*[FadeIn(item, shift=UP * .32) for item in loose], lag_ratio=.28),
                  run_time=1.1)
        self.at("drop one of")
        self.play(FadeOut(question), run_time=.30)
        targets = [pt(.45, -.21), pt(1.50, -.31), pt(2.55, -.245), pt(3.55, -.18)]
        self.play(LaggedStart(*[item.animate.move_to(p) for item, p in zip(loose, targets)], lag_ratio=.30),
                  run_time=1.62)
        for i, item in enumerate(loose[:2]):
            bob(item, amp=.06, speed=2.8, seed=i)
        self.at("check again after")
        face, needle = clock_face(.62)
        face.move_to(pt(3.85, 2.39))
        self.play(FadeIn(face), run_time=.37)
        now = label("10 minutes later", 1.11, 2.39, 34, GOLD)
        self.play(Rotate(needle, -TAU, about_point=face[0].get_center()), FadeIn(now), run_time=1.28)
        self.at("empty the bowl", lead=.36)
        for item in loose:
            item.clear_updaters()
        grip = hand().scale(.67).rotate(.15).move_to(pt(-.96, -.18)).set_z_index(4)
        pouring = VGroup(basin, *loose)
        splash = outline((4.8, -.34), ((5.03, -.68), (5.65, -.71), (5.69, -1.13)),
                         (5.89, -1.43), (5.43, -1.43),
                         ((5.43, -.94), (4.96, -.98), (4.66, -.61)), fill=BLUE).set_z_index(3)
        self.play(FadeOut(face), FadeOut(now), FadeIn(grip), run_time=.44)
        self.play(Rotate(pouring, -.33), grip.animate.shift(pt(.13, .28)), FadeIn(splash), run_time=.75)
        self.play(FadeOut(splash, shift=DOWN * .64), FadeOut(basin[2]),
                  *[FadeOut(item, shift=RIGHT * .25) for item in loose], run_time=.48)
        self.finish()


DROP_Y = 1.83
FLOOR_Y = -2.45
DROP_X = (.29, 3.87)


def drop_room():
    return VGroup(panel(13.50, 7.5, 0, 0, SKY, radius=.32),
                  panel(13.12, 1.05, 0, -3.01, PATH, radius=.2),
                  stroke((-6.48, FLOOR_Y - .05), (6.48, FLOOR_Y - .05), PAPER, 4))


def drop_question():
    return question_card("Which lands\nfirst?", y=.20, left=-5.99, size=51, max_w=3.95)


def drop_marks():
    return DashedLine(pt(-.69, DROP_Y), pt(5.25, DROP_Y), dash_length=.15,
                      color=WOOL_LIGHT, stroke_width=3)


def raised_pair(wingless=True):
    left = maple().scale(1.19).rotate(-.40).move_to(pt(DROP_X[0], DROP_Y))
    right = maple(not wingless).scale(1.19).move_to(pt(DROP_X[1], DROP_Y))
    return left, right


def drop_hands():
    return (hand().scale(.98).rotate(-.42).move_to(pt(-1.45, DROP_Y + .34)),
            hand(-1).scale(.98).rotate(.42).move_to(pt(4.94, DROP_Y + .34)))


class S08PredictQuestion(SpokenScene):
    def construct(self):
        self.add(drop_room())
        left, extra = raised_pair(False)
        extra.shift(pt(DROP_X[1], DROP_Y) - extra[2].get_center())
        hand_l, hand_r = drop_hands()
        self.at("now a question")
        self.play(FadeIn(hand_l, shift=UP * .49), FadeIn(left, shift=UP * .49), run_time=.74)
        self.at("stand on the")
        self.play(left.animate.shift(UP * .28), hand_l.animate.shift(UP * .28), run_time=.92)
        self.at("hold a whole")
        self.play(left.animate.shift(DOWN * .28), hand_l.animate.shift(DOWN * .28), run_time=.82)
        self.at("snap the wing", lead=.68)
        self.play(FadeIn(hand_r, shift=LEFT * .35), FadeIn(extra, shift=LEFT * .35), run_time=.56)
        wing = VGroup(extra[0], extra[1])
        stub = extra[2]
        self.remove(extra)
        self.add(wing, stub)
        self.play(FadeOut(wing, shift=RIGHT * .54 + DOWN * .52), run_time=.56)
        self.at("hold both at")
        reference = drop_marks().shift(DOWN * .83)
        together = VGroup(hand_l, hand_r, left, stub).set_z_index(1)
        self.play(together.animate.shift(DOWN * .83), Create(reference), run_time=.75)
        self.at("which do you predict", lead=.40)
        self.play(FadeIn(drop_question(), shift=RIGHT * .12), run_time=.31)
        self.play(together.animate.shift(UP * .83), reference.animate.shift(UP * .83),
                  rate_func=linear, run_time=self.narration_s + .39 - self.elapsed())
        self.finish()


class S09PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(drop_room(), drop_marks(), *drop_hands(), *raised_pair(), drop_question())
        self.wait(float(os.environ.get("KX_DURATION", "4.5")))


def release_path(seed, x_end, seconds, *, spinning=False):
    start = seed.get_center()
    original = seed.copy()
    target = pt(x_end, FLOOR_Y + (.30 if spinning else .19))

    def travel(mob, progress):
        height_progress = progress if spinning else progress ** 1.8
        position = np.array([interpolate(start[0], target[0], progress),
                             interpolate(start[1], target[1], height_progress), 0.0])
        mob.become(original)
        if spinning:
            phase = progress * TAU * 4
            mob.stretch(.43 + .57 * abs(np.cos(phase)), 0)
            mob.rotate(.63 * np.sin(phase))
        mob.move_to(position)

    return UpdateFromAlphaFunc(seed, travel, run_time=seconds, rate_func=linear)


class S10Reveal(SpokenScene):
    def construct(self):
        left, right = raised_pair()
        hands = drop_hands()
        mark = drop_marks()
        question = drop_question()
        self.add(drop_room(), mark, *hands, left, right, question)
        self.at("the key without", lead=0)
        quick_clock, repeat_clock = clock_face(.60), clock_face(.60)
        quick_clock[0].move_to(pt(-2.96, -.39))
        repeat_clock[0].move_to(pt(-4.78, -.39))
        clocks = VGroup(repeat_clock[0], quick_clock[0],
                        maple().scale(.58).move_to(pt(-4.78, .68)),
                        maple(False).scale(.82).move_to(pt(-2.96, .68)))
        schematic = scope_tag(size=30, color=TEXT).move_to(pt(-3.87, -1.47))
        self.play(FadeOut(question), FadeOut(mark), *[FadeOut(h, shift=UP * .3) for h in hands],
                  FadeIn(clocks), FadeIn(schematic), run_time=.40)
        self.play(AnimationGroup(
            release_path(right, DROP_X[1], .91),
            release_path(left, DROP_X[0], 5.52, spinning=True),
            Rotate(quick_clock[1], -.75, about_point=quick_clock[0][0].get_center(),
                   run_time=.91, rate_func=linear),
            Rotate(repeat_clock[1], -4.55, about_point=repeat_clock[0][0].get_center(),
                   run_time=5.52, rate_func=linear),
            lag_ratio=0,
        ))
        self.at("the spinning wing", lead=.23)
        self.play(repeat_clock[0][0].animate.set_stroke(GOLD, width=5), run_time=.54)
        self.at("a breeze then", lead=.56)
        replay = raised_pair()[0]
        breeze = VGroup(*[Arrow(pt(-4.82, y), pt(-1.33, y), buff=0, color=BLUE,
                                stroke_width=5, max_tip_length_to_length_ratio=.12)
                          for y in [1.13, .64, .15]])
        self.play(FadeOut(clocks), FadeOut(schematic), FadeOut(right), FadeOut(left), FadeIn(replay), run_time=.51)
        self.play(LaggedStart(*[GrowArrow(a) for a in breeze], lag_ratio=.12), run_time=.43)
        self.play(release_path(replay, 4.24, 2.56, spinning=True), breeze.animate.shift(RIGHT * .40),
                  run_time=2.56, rate_func=linear)
        self.at("time three drops", lead=.25)
        trials = label("3 drops of each", -2.49, 2.51, 36, GOLD)
        self.play(FadeOut(breeze), FadeIn(trials), run_time=.45)
        self.finish()


def phone():
    return VGroup(panel(2.22, 3.52, 0, 0, INK, WOOL_LIGHT, .28),
                  panel(1.89, 2.67, 0, .05, "#203b49", radius=.15),
                  stroke((-.3, 1.55), (.3, 1.55), LINE, 4),
                  disk(0, -1.46, .09, WOOL_LIGHT))


def no_tasting():
    face = VGroup(disk(.26, .21, .83, SKIN), disk(.40, .44, .077, INK),
                  ArcBetweenPoints(pt(.28, -.18), pt(.76, -.1), angle=-.65).set_stroke(INK, 5))
    sprig = berries().scale(.92).move_to(pt(-.76, -.30))
    halo = Circle(radius=1.36, color=RED, stroke_width=9)
    ban = stroke((-1.02, -1.02), (1.02, 1.02), RED, 9)
    return VGroup(face, sprig), VGroup(halo, ban)


def acorn():
    nut = Ellipse(width=.76, height=.97, fill_color="#af744c", fill_opacity=1,
                  color=PATH_EDGE, stroke_width=2).shift(DOWN * .12)
    cap = outline((-.48, .21), ((-.45, .66), (.44, .66), (.48, .21)), fill=PATH_EDGE, edge=PAPER)
    return VGroup(nut, cap, stroke((0, .46), (.06, .66), PATH_EDGE, 6))


class S11Safety(SpokenScene):
    def construct(self):
        people = family()
        outside = yard()
        self.add(outside, people)
        self.at("choose a patch")
        permission = tag("Pick where allowed", -2.66, 2.53, GOLD)
        self.play(FadeIn(permission), run_time=.52)
        self.at("stay within arms")
        self.play(people[0].animate.shift(RIGHT * .38), people[1].animate.shift(LEFT * .17),
                  run_time=1.19)
        self.at("never taste any", lead=.36)
        safety_panel = panel(5.54, 5.20, 3.28, -.04, "#223745", "#597482", .3)
        face, stop = no_tasting()
        face.shift(pt(3.27, .30))
        stop.shift(pt(3.27, .30))
        self.play(FadeOut(permission), FadeOut(outside[7:]), FadeIn(safety_panel), FadeIn(face), run_time=.44)
        self.play(Create(stop[0]), Create(stop[1]), run_time=.52)
        warning = label("Never taste wild plants", 3.28, -1.67, 28, TEXT)
        self.play(FadeIn(warning), run_time=.32)
        self.at("keep acorns", lead=.38)
        self.play(FadeOut(face), FadeOut(stop), FadeOut(warning), run_time=.35)
        examples = [acorn().scale(.92).move_to(pt(1.76, .55)),
                    float_seed().scale(.96).move_to(pt(3.29, .55)),
                    burr().scale(1.07).move_to(pt(4.81, .55))]
        self.play(FadeIn(examples[0], shift=UP * .37), run_time=.52)
        self.at("small seeds and", lead=.21)
        self.play(FadeIn(examples[1], shift=UP * .37), run_time=.44)
        self.at("burrs away from", lead=.18)
        self.play(FadeIn(examples[2], shift=UP * .37), run_time=.44)
        self.at("children under four", lead=.28)
        choke = label("Under 4: choking risk", 3.27, -1.42, 32, TEXT)
        self.play(FadeIn(choke), run_time=.36)
        self.at("call 911 if", lead=.38)
        handset = phone().stretch(1.15, 0).move_to(pt(3.27, .15))
        emergency = label("Choking:\n911 first", 3.27, .30, 32, TEXT)
        self.play(*[FadeOut(item) for item in examples], FadeOut(choke), FadeIn(handset, shift=UP * .25),
                  run_time=.42)
        self.play(FadeIn(emergency), run_time=.31)
        self.play(handset[1].animate.set_fill("#377488"), rate_func=there_and_back, run_time=1.61)
        self.at("if anyone swallows", lead=.18)
        swallowed = VGroup(berries().scale(.85).move_to(pt(1.22, .15)),
                           float_seed().scale(.85).move_to(pt(5.32, .14)))
        self.play(FadeOut(emergency), FadeIn(swallowed, shift=UP * .27), run_time=.55)
        self.play(swallowed[0].animate.shift(UP * .36), swallowed[1].animate.shift(UP * .36),
                  rate_func=there_and_back, run_time=1.02)
        self.play(handset[1].animate.set_fill("#3b7b90"), rate_func=there_and_back, run_time=1.42)
        self.at("call poison help", lead=.24)
        self.play(FadeIn(label("Poison\nHelp", 3.27, .24, 34, TEXT)), run_time=.39)
        self.finish()


def protected_leg():
    boot = shoe(False).scale(.89).move_to(pt(.32, -1.74))
    sock = panel(1.56, 1.02, -.61, -.99, WOOL_LIGHT, TEAL, .16)
    pant = outline((-1.43, 2.25), (.49, 2.25), (.08, -.69), (-1.30, -.69),
                   fill="#526b85", edge=LINE, width=3)
    seam = stroke((-1.15, 2.09), (-1.04, -.48), "#8da2b0", 2.6)
    cuff = panel(1.60, .26, -.61, -.57, WOOL_LIGHT, TEAL, .085)
    return VGroup(boot, pant, seam, sock, cuff)


def wash_station():
    pipe = VMobject().set_points_as_corners([pt(2.11, 1.13), pt(2.11, 2.18), pt(.37, 2.18),
                                             pt(.37, 1.77)])
    pipe.set_stroke(LINE, 25)
    nozzle = panel(.55, .23, .36, 1.72, TEXT, radius=.07)
    sink = panel(7.34, .38, .42, -1.88, "#9bb0b8", TEXT, .12)
    sink_base = outline((-2.87, -1.92), (3.7, -1.92),
                        ((3.41, -2.63), (2.91, -2.87), (2.21, -2.87)), (-1.39, -2.87),
                        ((-2.12, -2.86), (-2.57, -2.60), (-2.87, -1.92)), fill="#4a6b77", edge=LINE)
    return VGroup(pipe, nozzle, sink_base, sink)


class S12Ticks(SpokenScene):
    def construct(self):
        people = family()
        backdrop = yard()
        self.add(backdrop, people)
        self.at("ticks live in")
        field_lens = lens(.77).move_to(pt(4.28, .08))
        self.play(FadeIn(field_lens, shift=RIGHT * .39), run_time=.53)
        self.play(field_lens.animate.shift(pt(.51, .42)), run_time=.88)
        self.at("wear", lead=.48)
        inset = panel(5.67, 5.43, 3.43, .02, "#263e4b", "#64828b", .27)
        leg = protected_leg().scale(.91).move_to(pt(3.31, -.28))
        for piece in leg[1:3]:
            piece.shift(UP * .28)
        self.play(FadeOut(field_lens), FadeIn(inset), FadeIn(leg), run_time=.50)
        shoes = label("Closed shoes", 3.43, 2.36, 30, TEXT)
        self.play(FadeIn(shoes), run_time=.34)
        self.at("tuck long pants")
        tucked = label("Pants tucked into socks", 3.43, 2.36, 29, TEXT)
        self.play(leg[1].animate.shift(DOWN * .28), leg[2].animate.shift(DOWN * .28),
                  swap(shoes, tucked), run_time=.85)
        self.at("before going inside")
        self.play(FadeOut(tucked), run_time=.23)
        self.play(FadeOut(inset), FadeOut(leg), run_time=.40)
        exam = lens(.62).move_to(pt(-1.78, -.49))
        self.at("check your child's", lead=.29)
        self.play(FadeIn(exam, shift=LEFT * .32), run_time=.42)
        self.play(exam.animate.move_to(pt(-1.88, .43)), run_time=.65)
        self.play(exam.animate.move_to(pt(-1.85, -.81)), run_time=.69)
        self.play(exam.animate.move_to(pt(-1.93, -1.53)), run_time=.60)
        self.at("wash hands with", lead=.52)
        surface = desk()
        tap = wash_station()
        palms = VGroup(hand().scale(.81).move_to(pt(-.53, -.35)),
                       hand(-1).scale(.81).rotate(.11).move_to(pt(1.08, -.56)))
        foam = VGroup(*[disk(x, y, r, TEXT, BLUE) for x, y, r in [
            (-.07, .20, .16), (.19, .43, .19), (.45, .11, .24), (.72, .28, .15),
            (.88, -.03, .13), (.19, -.14, .15), (-.19, -.09, .17)]])
        stream = VGroup(*[stroke((.23 + i * .13, 1.55), (.16 + i * .15, .5), BLUE, 4) for i in range(3)])
        self.play(FadeOut(exam), FadeOut(people), FadeOut(backdrop), FadeIn(surface), FadeIn(tap),
                  FadeIn(palms), FadeIn(stream), run_time=.52)
        self.play(FadeIn(foam, scale=.65), palms[0].animate.shift(RIGHT * .29),
                  palms[1].animate.shift(LEFT * .22), run_time=.65)
        self.play(foam.animate.shift(pt(.2, -.29)), palms[0].animate.shift(LEFT * .31),
                  palms[1].animate.shift(RIGHT * .2), run_time=.74)
        bob(foam, amp=.10, speed=4.1)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        self.add(desk())
        first = prediction_sheet(-3.78, -.34)
        written = marks(-3.78, -.34)
        ideas = VGroup(first, written)
        collected = VGroup(sheet(2.36, -.56, 5.95, 3.32),
                           burr().move_to(pt(1.31, -.30)), burr().scale(.63).move_to(pt(3.11, -.70)))
        self.at("look back at")
        self.play(FadeIn(ideas, shift=UP * .3), run_time=.60)
        self.play(FadeIn(collected, shift=LEFT * .46), run_time=.59)
        self.at("how did the seeds", lead=.55)
        q = question_card("How did the seeds get there?", y=2.7, size=38)
        detail = fiber_detail().scale(.86).move_to(pt(2.54, -.42))
        self.play(FadeOut(collected), FadeIn(detail), run_time=.47)
        self.play(FadeIn(q), run_time=.45)
        self.play(detail[3].animate.shift(pt(-.13, -.37)), detail[4].animate.shift(pt(-.13, -.37)),
                  run_time=.76)
        self.at("any seeds that stuck", lead=.32)
        self.play(FadeOut(q), FadeOut(ideas), FadeOut(detail), run_time=.36)
        self.clear()
        outdoors = yard()
        boot = walking_shoe(-2.48, -1.86)
        hitchhiker = burr().scale(.82).move_to(pt(-1.28, -1.78))
        ride = VGroup(boot, hitchhiker)
        self.add(outdoors)
        self.play(FadeIn(ride), run_time=.34)
        self.play(ride.animate.shift(pt(2.45, .31)), run_time=1.03)
        self.play(ride.animate.shift(pt(1.75, -.27)), run_time=1.04)
        self.at("if the sock stayed")
        self.play(FadeOut(hitchhiker), run_time=.29)
        self.play(boot.animate.move_to(pt(-1.84, -1.85)), run_time=.43)
        self.at("try again later")
        self.play(boot.animate.shift(pt(1.55, .22)), run_time=.61)
        self.finish()


class S14End(EndCard):
    LINE = "Seed shapes carry seeds away by wind, water and animals."
