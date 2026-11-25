"""Beak Buffet parent guide, staged as a schematic kitchen tabletop."""

from bp_parts import *
from bp_style import EndCard

# COLOR MAP. Gold cereal and wood pin, blue water and spoon, cyan straw,
# copper beans, coral pasta, lavender dough and yarn, sage tongs, silver tweezers.
TABLE = "#212F36"
RIM = "#B0CBC6"
WATER = "#28637E"
RIPPLE = "#70B9D3"
CER = "#F4BE62"
WOOD = "#DBA161"
SPOON = "#8CC6DE"
STRAW = "#54DFCD"
BEAN = "#B66C51"
PASTA = "#F19F84"
DOUGH = "#9B81C0"
YARN = "#E2B7EE"
TONGS = "#9ED1AF"
STEEL = "#C7D3DD"
SKIN = "#CC9C83"
PAPER = "#233C48"
INK = "#14232B"
NAMES = ("Clothespin", "Slotted spoon", "Straw", "Tongs", "Tweezers")
COLORS = (WOOD, SPOON, STRAW, TONGS, STEEL)
QUESTION = "Which picks up more?"


def p(x, y):
    return np.array([x, y, 0.0])


def panel(w, h, color, edge=None, radius=0.2):
    return RoundedRectangle(width=w, height=h, corner_radius=radius,
                            fill_color=color, fill_opacity=1,
                            stroke_color=edge or color, stroke_width=3 if edge else 0)


def oval(w, h, color, x=0, y=0, angle=0):
    return Ellipse(width=w, height=h, fill_color=color, fill_opacity=1,
                   stroke_width=0).rotate(angle).move_to(p(x, y))


def shape(points, color):
    return Polygon(*(p(x, y) for x, y in points), fill_color=color,
                   fill_opacity=1, stroke_width=0)


def ring(x=0, y=0, radius=0.21):
    return Circle(radius=radius, stroke_color=CER, stroke_width=6).move_to(p(x, y))


def table():
    return panel(13.38, 7.32, TABLE, "#374C53", radius=0.44)


def heading(words, color=TEXT):
    return T(words, 34, color, weight=BOLD).move_to(p(0, 3.05))


def food_fish(color=PASTA):
    return VGroup(oval(1.15, 0.56, color, 0.05),
                  shape([(-0.36, 0), (-0.86, 0.34), (-0.86, -0.34)], color),
                  Dot(p(0.38, 0.07), radius=0.045, color=INK))


def bean():
    return VGroup(oval(0.7, 0.43, BEAN, angle=0.35),
                  oval(0.27, 0.08, "#F1BB92", 0.07, -0.04, 0.35))


def pond():
    bowl = VGroup(oval(4.75, 4.75, INK, 0, -0.13), oval(4.65, 4.65, RIM), oval(4.26, 4.26, WATER))
    for x, y, w in [(-0.95, 1.26, 1.02), (0.9, 0.98, 0.84), (-1.31, -0.68, 0.51),
                    (0.55, -1.49, 1.22), (0.31, 0.39, 1.08)]:
        bowl.add(Arc(radius=w, start_angle=4.15, angle=0.85,
                     stroke_width=2.2, stroke_color=RIPPLE).move_to(p(x, y)))
    loops = VGroup(*(ring(x, y, r) for x, y, r in [
        (-1.3, 0.8, 0.24), (-0.46, 1.45, 0.19), (0.53, 1.02, 0.23),
        (1.43, 0.52, 0.19), (-0.73, 0.19, 0.24), (0.25, -0.09, 0.22),
        (1.1, -0.61, 0.22), (-1.08, -0.79, 0.2), (-0.24, -1.39, 0.23)]))
    return VGroup(bowl, loops)


def drift_loops(bowl):
    for i, loop in enumerate(bowl[1]):
        bob(loop, amp=0.14, speed=1.45, seed=i)
    return bowl


def dish():
    plate = VGroup(oval(5.05, 4.42, RIM), oval(4.65, 4.02, "#42625D"))
    for i, (x, y) in enumerate([(-1.45, .3), (-.83, 1.13), (.06, .77), (.92, 1.17),
                                (1.56, .21), (-.56, -.05), (.52, -.23), (-1.25, -.87),
                                (-.36, -1.18), (.91, -1.07)]):
        plate.add(bean().rotate(i * 1.32).move_to(p(x, y)))
    return plate


def fish_pan():
    pan = VGroup(panel(5.55, 4.35, RIM, radius=0.48), panel(5.14, 3.94, WATER, radius=0.38))
    pan.add(*(food_fish().rotate(a).move_to(p(x, y))
              for x, y, a in [(-1.2, .97, .22), (1.19, .56, 2.9), (-.93, -.72, -.2), (1.05, -1.05, .43)]))
    return pan


def worm_station():
    clay = VGroup(oval(5.0, 3.55, "#665786", 0, -0.15), oval(5.0, 3.55, DOUGH))
    for x, y in [(-1.3, 0), (-0.3, -0.64), (0.6, 0.35), (1.35, -0.45)]:
        clay.add(CubicBezier(p(x, y), p(x + .65, y + .35), p(x - .68, y + .88),
                            p(x + .34, y + 1.03), stroke_width=10, color=YARN))
    return clay


def bottle():
    outline = [(-.78, -1.65), (.78, -1.65), (.9, -1.45), (.9, .63),
               (.42, 1.1), (.35, 1.67), (-.35, 1.67), (-.42, 1.1),
               (-.9, .63), (-.9, -1.45)]
    water = shape([(-.79, -1.51), (.79, -1.51), (.79, .55), (-.79, .55)], WATER)
    body = Polygon(*(p(x, y) for x, y in outline), color=RIM, stroke_width=4,
                   fill_color="#365767", fill_opacity=1)
    return VGroup(body, water, oval(.78, .22, INK, 0, 1.67),
                  Line(p(-.65, .55), p(.65, .55), color=RIPPLE, stroke_width=3))


def cup():
    body = shape([(-.98, .61), (.98, .61), (.71, -.86), (-.71, -.86)], "#B1D5D0")
    return VGroup(body, oval(1.96, .63, RIM, 0, .61), oval(1.65, .43, INK, 0, .62))


def hand():
    return VGroup(oval(1.58, 1.9, SKIN, 0, -.16, -.24),
                  oval(.45, .99, SKIN, .62, .27, -.51),
                  *(oval(.32, .83, SKIN, x, y, -.13)
                    for x, y in [(-.51, .66), (-.18, .87), (.15, .94), (.45, .82)]))


def tool(kind, opening=0.20):
    """Upright tool, with its working end at the bottom."""
    if kind == 0:
        left = panel(.36, 3.5, WOOD, radius=.09).rotate(-opening / 2).shift(LEFT * .18)
        right = panel(.36, 3.5, "#F7C98D", radius=.09).rotate(opening / 2).shift(RIGHT * .18)
        return VGroup(left, right, Circle(radius=.20, color=STEEL, stroke_width=5))
    if kind == 1:
        return VGroup(panel(.29, 2.65, SPOON, radius=.11).shift(UP * .75),
                      oval(1.46, 1.79, SPOON, 0, -1.13),
                      *(panel(.12, .83 - abs(x), TABLE, radius=.06).move_to(p(x, -1.1))
                        for x in [-.36, -.12, .12, .36]))
    if kind == 2:
        return VGroup(panel(.25, 3.8, STRAW, radius=.10),
                      panel(.055, 3.55, "#AFF6E3", radius=.022).shift(LEFT * .05))
    color = COLORS[kind]
    angle = opening / 2
    half_width = .095
    # Keep the arm pivots fixed and make the bend tangent to both arms.
    radius = .22 / np.cos(angle)
    bend_center = p(0, 1.60 - radius * np.sin(angle))
    sweep = PI - 2 * angle
    outer = Arc(radius=radius + half_width, start_angle=angle, angle=sweep,
                arc_center=bend_center)
    inner = Arc(radius=radius - half_width, start_angle=PI - angle, angle=-sweep,
                arc_center=bend_center)
    arm_length = 3.20
    left_arm = p(-np.sin(angle), -np.cos(angle))
    right_arm = p(np.sin(angle), -np.cos(angle))
    left_tip = p(-.22, 1.60) + arm_length * left_arm
    right_tip = p(.22, 1.60) + arm_length * right_arm
    left_cap = Arc(radius=half_width, start_angle=PI - angle, angle=PI, arc_center=left_tip)
    right_cap = Arc(radius=half_width, start_angle=PI + angle, angle=PI, arc_center=right_tip)

    outline = VMobject(fill_color=color, fill_opacity=1, stroke_width=0)
    outline.set_points(outer.get_points())
    for arc in (left_cap, inner, right_cap):
        outline.add_line_to(arc.get_start())
        outline.append_points(arc.get_points())
    outline.close_path()
    arms = VGroup(outline)
    if kind == 3:
        arms.add(oval(.39, .68, color, angle=-angle).move_to(left_tip - .17 * left_arm),
                 oval(.39, .68, color, angle=angle).move_to(right_tip - .17 * right_arm))
    return arms


def tool_row(scale=.93, y=.22):
    return VGroup(*(tool(i).scale(scale).move_to(p(x, y))
                    for i, x in enumerate([-4.65, -2.35, 0, 2.35, 4.65])))


def pond_tools():
    return (pond().move_to(p(0, .2)),
            tool(0).rotate(-.4).move_to(p(-3.95, .37)),
            tool(1).rotate(.4).move_to(p(3.95, .37)))


def nectar_station():
    return bottle().scale(1.22).move_to(p(-2.55, -.48)), cup().scale(1.22).move_to(p(2.55, -.92))


def flower():
    petals = VGroup(*(oval(1.18, .66, PASTA, .63 * np.cos(a), .63 * np.sin(a), a)
                      for a in np.arange(5) * TAU / 5))
    return VGroup(Line(p(.21, -.3), p(.41, -1.8), color=TONGS, stroke_width=12),
                  petals, oval(.63, .63, CER))


def bird(kind, depth=1):
    """Profile looking right, with bill and feeding parts available for animation."""
    body_colors = ("#D65253", "#8E7764", "#728EA5", "#5CAC91", "#B68B62")
    heads = ("#E76A61", "#43A48F", "#A9BDCE", "#74CDA9", "#C49A70")
    wings = ("#AB3C4B", "#B79B79", "#526D86", "#33776C", "#886148")
    bills = (CER, "#E3BA60", "#E1B66B", "#CFDBD9", "#D9B58F")
    length = (.83, 1.24, 1.76, 1.48, .90)[kind]
    thickness = (.69, .34, .35, .14, .23)[kind] * depth
    head_x, head_y = .52, .68
    if kind == 2:
        head_x, head_y = .55, 1.38
    tail = shape([(-.7, -.37), (-2, -.54), (-1.7, .23), (-.5, .17)], wings[kind])
    if kind == 4:
        tail.rotate(-.55, about_point=p(-.62, -.06))
    body = oval(2.5, 1.38, body_colors[kind], -.44, -.23, .17)
    wing = oval(1.49, .75, wings[kind], -.62, -.19, .30)
    if kind == 3:
        wing = oval(1.8, .51, wings[kind], -.72, .22, -.71)
    neck = oval(1.02, 2.17 if kind == 2 else 1.22, heads[kind], .25, head_y - .46, -.29)
    head = oval(1.21, 1.03 if kind != 3 else .76, heads[kind], head_x, head_y)
    root, y = head_x + .36, head_y - .05
    tip = root + length
    bill = shape([(root, y + thickness / 2), (tip - (.16 if kind == 1 else 0), y + (.10 if kind == 1 else 0)),
                  (tip, y - .04), (root, y - thickness / 2)], bills[kind])
    if kind == 1:
        bill.add(Line(p(root + .17, y - .07), p(tip - .14, y - .07), color=INK, stroke_width=2))
    if kind == 0:
        head.add(shape([(.03, .94), (.37, 1.59), (.78, .99)], heads[kind]))
        head.add(oval(.43, .54, "#803742", .83, .58, .24))
    if kind == 2:
        head.add(shape([(.6, 1.67), (-.26, 1.82), (.43, 1.99)], wings[kind]))
    if kind == 3:
        neck.add(oval(.61, .48, "#D85465", .57, .27, -.37))
    if kind == 4:
        head.add(oval(.52, .10, "#F6E8CE", .69, .96, .12))
    eye = VGroup(Dot(p(head_x + .24, head_y + .18), radius=.087, color=INK),
                 Dot(p(head_x + .266, head_y + .208), radius=.023, color=WHITE))
    legs = VGroup()
    if kind == 2:
        legs.add(*(VMobject(color="#C2AD88", stroke_width=6).set_points_as_corners(
            [p(x, -.54), p(x + .09, -1.42), p(x + .44, -1.49)]) for x in [-.67, -.17]))
    scene_bird = VGroup(legs, tail, body, neck, wing, head, bill, eye)
    scene_bird.bill, scene_bird.wing = bill, wing
    return scene_bird


def trial_sheet(x=-3.35, y=0):
    page = panel(5.05, 4.85, PAPER, "#647E85", radius=.22).move_to(p(x, y))
    ledger = Ledger([(NAMES[0], "1", WOOD), (NAMES[1], "3", SPOON)],
                    top_left=(x - 2.07, y + .9), row_h=1.15, key_w=3.25, width=4.2, size=32)
    return page, ledger


class TableScene(SpokenScene):
    def start(self, *objects):
        self.add(table(), *objects)

    def replace_picture(self, old, new, run_time=.75):
        self.play(FadeOut(old, shift=LEFT * .22), FadeIn(new, shift=LEFT * .22),
                  run_time=run_time)


class S01Hook(TableScene):
    def construct(self):
        bowl, pin, spoon = pond_tools()
        self.start(drift_loops(bowl), pin)
        self.at("How well")
        self.play(pin.animate.shift(RIGHT * .94 + DOWN * .52).rotate(-.36), run_time=2.45)
        self.at("Give your child")
        self.play(pin.animate.shift(RIGHT * .77 + DOWN * .31).rotate(.16), run_time=1.55)
        self.play(pin.animate.shift(LEFT * .58 + UP * .68), run_time=.85)
        self.at("Then see what")
        self.play(FadeIn(spoon, shift=RIGHT * 1.75), run_time=1.60)
        self.play(spoon.animate.shift(LEFT * .46 + DOWN * .32), run_time=1.04)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Beak Buffet: Parent Guide"
    LESSON = "Beak Buffet"

    def construct(self):
        bowl = pond().scale(.86).move_to(p(0, .22))
        self.add(table(), bowl)
        row = tool_row(.35, -2.30)
        title = T(self.LESSON, 60, font=TITLE_FONT, weight=BOLD).move_to(p(0, 2.86))
        self.play(FadeIn(title, shift=UP * .12), FadeIn(row, shift=UP * .20),
                  bowl.animate.scale(.72 / .86), run_time=.53)
        self.wait(.73)
        self.play(FadeOut(title), run_time=.49)


class S03Payoff(TableScene):
    def construct(self):
        tools = tool_row(.35, -2.30)
        full_tools = tool_row(.72, -.50)
        bowl = pond().scale(.72).move_to(p(0, .22))
        time = ValueTracker(0)
        clock = dial(time, p(-4.65, 1.72), radius=1.03, color=GOLD,
                     fmt="{:.0f} min", scale=35, size=28)
        self.start(drift_loops(bowl), tools)
        self.at("In about")
        self.add(clock)
        self.play(time.animate.set_value(1), run_time=.65)
        self.at("your child tests")
        self.play(FadeOut(bowl), LaggedStart(*(Transform(t, full) for t, full in zip(tools, full_tools)),
                                             lag_ratio=.21), run_time=2.35)
        bubble = VGroup(oval(1.22, .76, GOLD, .77, 1.66),
                        shape([(.5, 1.42), (.33, 1.21), (.81, 1.35)], GOLD),
                        T("?", 35, INK, weight=BOLD).move_to(p(.77, 1.66)))
        marks = VGroup(*(Line(p(x, 1.35), p(x, 2.04), color=GOLD, stroke_width=6)
                         for x in [.13, .38, .63, .88]),
                       Line(p(.03, 1.44), p(1.03, 1.88), color=GOLD, stroke_width=6))
        gu = T("Guess first", 31, GOLD).move_to(p(2.76, 1.72))
        count = T("Count fairly", 31, GOLD).move_to(gu)
        match = T("Match real birds", 31, GOLD).move_to(gu).shift(RIGHT * .67)
        self.at("guessing first", lead=.65)
        self.play(FadeIn(bubble, shift=UP * .23), FadeIn(gu), run_time=.35)
        self.at("counting fairly", lead=.35)
        self.play(Succession(FadeOut(bubble, run_time=.30), FadeIn(marks, run_time=.43)),
                  swap(gu, count), run_time=.73)
        self.at("comparing results")
        self.play(tools[0].animate.shift(UP * .2), tools[1].animate.shift(UP * .33), run_time=1.56)
        hummer = bird(3).scale(.63).move_to(p(0, 1.90))
        self.at("They also connect")
        self.play(FadeOut(marks), FadeOut(count), FadeIn(hummer, shift=RIGHT * .43), run_time=1.29)
        self.at("real birds outside", lead=.56)
        self.play(FadeIn(match), hummer.animate.shift(UP * .19), run_time=1.12)
        self.finish()


class S03aSafetyBeforeSetup(TableScene):
    def construct(self):
        items = VGroup(dish().scale(.57), pond().scale(.61), bottle().scale(.74)).arrange(RIGHT, buff=.64)
        items.move_to(p(0, .16))
        adult = hand().scale(.65).rotate(-.44).move_to(p(-2.16, -2))
        child = hand().scale(.44).rotate(.31).move_to(p(2.02, -2.25))
        self.start(items, adult, child)
        self.at("Stay with your child")
        self.play(adult.animate.shift(RIGHT * .72 + UP * .36), child.animate.shift(UP * .30), run_time=2.30)
        self.at("Keep small pieces")
        self.play(items.animate.shift(UP * 1.40).scale(.87), child.animate.shift(DOWN * .33), run_time=2.44)
        under = caption("Keep away from children under 4", color=GOLD, size=33)
        self.at("away from children")
        self.play(FadeIn(under), run_time=.53)
        self.at("Small pieces can")
        sample = VGroup(bean(), ring(), food_fish().scale(.47)).arrange(RIGHT, buff=.22).scale(1.57).move_to(p(0, -.54))
        self.play(FadeOut(adult), FadeOut(child), FadeIn(sample, shift=DOWN * .31), run_time=.74)
        choking = boxed_label("Choking? Call 911", color="#FFD0B1", size=42, pad=.35).move_to(p(0, -1.15))
        self.at("Call 911", lead=.68)
        self.play(FadeOut(sample), FadeOut(under), run_time=.29)
        self.play(FadeIn(choking, shift=UP * .22), run_time=.40)
        allergy = boxed_label("Check food allergies", color=GOLD, size=36, pad=.25).move_to(choking)
        self.at("Check food allergies")
        self.play(swap(choking, allergy), run_time=.85)
        kidney = caption("Skip red kidney beans", color=GOLD, size=32)
        red_bean = Difference(oval(1.42, .92, "#BD5151", angle=.52),
                              oval(.82, .54, TABLE, .48, .36, .52),
                              fill_color="#BD5151", fill_opacity=1, stroke_width=0)
        red_bean.move_to(p(0, -.72))
        no_bean = VGroup(Circle(radius=.88, color="#FFB5A6", stroke_width=5).move_to(red_bean),
                         Line(p(-.61, .61), p(.61, -.61), color="#FFB5A6", stroke_width=5).shift(red_bean.get_center()))
        self.at("Skip red kidney beans", lead=.50)
        self.play(FadeOut(allergy), run_time=.22)
        self.play(FadeIn(kidney), FadeIn(red_bean), Create(no_bean), run_time=.36)
        mouth = caption("Keep station items out of mouths", color=GOLD, size=32)
        self.at("Keep all station items")
        self.play(swap(kidney, mouth), FadeOut(VGroup(red_bean, no_bean)),
                  items.animate.shift(DOWN * .41), run_time=1.75)
        self.finish()


class S04SetupStations(TableScene):
    def construct(self):
        stations = VGroup(dish(), pond(), fish_pan(), worm_station(), bottle())
        stations[0].scale(.45).move_to(p(-4.1, 1.25))
        stations[1].scale(.46).move_to(p(0, 1.25))
        stations[2].scale(.44).move_to(p(4.15, 1.25))
        stations[3].scale(.47).move_to(p(-2.1, -1.45))
        stations[4].scale(.68).move_to(p(2.17, -1.44))
        self.start()
        self.at("Set five stations")
        self.play(LaggedStart(*(FadeIn(item, shift=UP * .31) for item in stations), lag_ratio=.19), run_time=2.76)
        plate = dish().move_to(p(-.3, .18))
        self.at("Put dry lima")
        self.replace_picture(stations, plate)
        self.play(LaggedStart(*(seed.animate.rotate(.24).shift(.18 * (seed.get_center() - plate.get_center()))
                                for seed in plate[2:]), lag_ratio=.11), run_time=2.35)
        bowl = pond().move_to(p(0, .2))
        self.at("Float cereal loops")
        self.replace_picture(plate, bowl)
        drift_loops(bowl)
        pan = fish_pan().move_to(p(-1.0, .22))
        self.at("Put pasta fish")
        self.replace_picture(bowl, pan)
        depth = boxed_label("3 cm of water", color=SPOON, size=31).move_to(p(3.68, -.05))
        self.at("three centimeters")
        self.play(FadeIn(depth), *(f.animate.shift(RIGHT * .17) for f in pan[2:]), run_time=1.35)
        sponge = panel(2.67, 1.67, CER, radius=.17).move_to(p(.37, -.49))
        glove = hand().rotate(-.8).move_to(p(-2.63, .17))
        scissors = VGroup(Circle(radius=.25, color=STEEL, stroke_width=8).move_to(p(-.23, .77)),
                          Circle(radius=.25, color=STEEL, stroke_width=8).move_to(p(.31, .77)),
                          shape([(-.21, .57), (.54, -.65), (.15, .47)], STEEL),
                          shape([(.30, .56), (-.42, -.61), (-.04, .46)], STEEL)).move_to(p(.32, .93))
        cutting = VGroup(sponge, glove, scissors)
        self.at("Cut any sponge")
        self.replace_picture(VGroup(pan, depth), cutting, run_time=.45)
        self.play(scissors.animate.shift(DOWN * .62), glove.animate.shift(RIGHT * 1.05), run_time=1.38)
        worms = worm_station().move_to(p(-1.3, .30))
        nectar = bottle().scale(.84).move_to(p(3.48, .10))
        self.at("Press yarn halfway")
        self.replace_picture(cutting, VGroup(worms, nectar), run_time=.51)
        self.play(worms[-1].animate.shift(DOWN * .22).stretch(.76, 1), run_time=1.36)
        self.finish()


class S05SetupToolsAndRules(TableScene):
    def construct(self):
        tools = tool_row()
        self.start()
        self.at("Set out a clothespin")
        self.play(FadeIn(tools[0], shift=UP * .35), run_time=.57)
        for phrase, i in [("slotted spoon", 1), ("straw tongs", 2), ("tongs and tweezers", 3), ("tweezers", 4)]:
            self.at(phrase, lead=.31)
            self.play(FadeIn(tools[i], shift=UP * .32), run_time=.32)
        self.at("Every child needs")
        label = caption("One straw per child", color=STRAW, size=34)
        self.play(tools[2].animate.shift(UP * .48), FadeIn(label), run_time=1.45)
        bot, glass = nectar_station()
        water, surface = bot[1], bot[3]
        full_height = water.get_top()[1]
        water.stretch(.10, 1, about_edge=DOWN)
        rise = UP * (full_height - water.get_top()[1])
        surface.shift(-rise)
        s = tool(2).scale(.82).rotate(-.52).move_to(p(-.14, .55))
        self.at("Fill a narrow")
        self.play(*(FadeOut(tools[i]) for i in [0, 1, 3, 4]), FadeOut(label),
                  FadeIn(bot, shift=DOWN * .80), ReplacementTransform(tools[2], s), run_time=1.14)
        self.play(water.animate.stretch(10, 1, about_edge=DOWN), surface.animate.shift(rise), run_time=1.75)
        self.at("Set an empty cup")
        self.play(FadeIn(glass, shift=RIGHT * .91), run_time=1.16)
        self.play(s.animate.rotate(.16), run_time=.59)
        self.finish()


class S05aShowTheRules(TableScene):
    def construct(self):
        glass = cup().scale(1.38).move_to(p(2.24, -.18)).set_z_index(2)
        h1 = hand().scale(1.03).rotate(.42).move_to(p(3.26, -.94))
        seed = bean().scale(.83).rotate(PI / 2 - .38 - .35).move_to(p(-2.76, -1.85)).set_z_index(3)
        pin = tool(0, .23).scale(.83).rotate(-.38).move_to(p(-2.03, .29)).set_z_index(4)
        h2 = hand().scale(.68).rotate(-.65).move_to(pin.get_top() + DOWN * .44)
        grip = VGroup(h2, pin)
        self.start(h1, glass, seed)
        self.at("Give your child")
        self.play(VGroup(h1, glass).animate.shift(UP * .26), run_time=1.98)
        self.at("and a tool")
        self.play(FadeIn(grip, shift=UP * .61), run_time=.78)
        jaw_axis = p(np.sin(.38), np.cos(.38))
        jaw_center = (pin[0].get_center() + pin[1].get_center()) / 2 - jaw_axis * 1.32
        self.play(grip.animate.shift(seed.get_center() - jaw_center), run_time=1.60)
        self.at("Move food to the cup")
        carry = glass[2].get_center() + UP * .41 - seed.get_center()
        held = VGroup(grip, seed)
        self.play(Rotate(held, angle=-1.05, about_point=seed.get_center()), run_time=.44)
        self.play(held.animate.shift(UP * carry[1]), run_time=.75)
        self.play(held.animate.shift(RIGHT * carry[0]), run_time=1.03)
        self.play(seed.animate.move_to(glass[2].get_center()).scale(.75),
                  grip.animate.shift(UP * .23), run_time=.47)
        self.at("In this game")
        label = caption("Cup = the bird’s stomach", size=34)
        self.play(FadeIn(label), FadeOut(grip, shift=UP * .28), run_time=1.09)
        self.finish()

class S06Predict(TableScene):
    def construct(self):
        bowl, pin, spoon = pond_tools()
        rest_positions = [loop.get_center() for loop in bowl[1]]
        self.start(drift_loops(bowl))
        self.at("Start with pond food")
        self.play(FadeIn(pin, shift=LEFT * .82), run_time=1.43)
        self.at("Look at the clothespin")
        self.play(FadeIn(spoon, shift=RIGHT * .92), run_time=1.24)
        self.at("Which do you think")
        self.play(FadeIn(question_card(QUESTION, size=38)), run_time=.65)
        self.at("in the same time")
        for loop in bowl[1]:
            loop.clear_updaters()
        self.play(*(loop.animate.move_to(position) for loop, position in zip(bowl[1], rest_positions)),
                  run_time=2.08, rate_func=linear)
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(table(), *pond_tools(), question_card(QUESTION, size=38))
        self.wait(float(os.environ["KX_DURATION"]))


class S08RunTrials(TableScene):
    def construct(self):
        bowl, pin, spoon = pond_tools()
        tongs = tool(3).scale(.6).rotate(-.47).move_to(p(-5.47, .42))
        self.start(drift_loops(bowl), pin, spoon)
        self.at("At each station")
        self.play(FadeIn(tongs, shift=LEFT * .63), run_time=2.23)
        q = question_card("Which beak will get the most?", size=34)
        self.at("Ask which beak")
        self.play(FadeIn(q), spoon.animate.rotate(-.37), run_time=.84)
        guess = caption("Example guess: slotted spoon", size=33, color=GOLD)
        self.at("Write down their guess")
        self.play(swap(q, guess), run_time=1.05)
        clock_value = ValueTracker(0)
        timer = dial(clock_value, p(-4.81, 1.34), radius=1.06, color=GOLD,
                     fmt="{:.0f} s", scale=30, size=30)
        glass = cup().scale(.91).move_to(p(4.96, -1.39))
        pieces = VGroup(bowl[1][3], bowl[1][6], bowl[1][5])
        self.at("Try each tool", lead=.92)
        self.play(FadeOut(pin), FadeOut(tongs), FadeOut(guess), FadeIn(timer), FadeIn(glass),
                  spoon.animate.move_to(p(.87, .92)).rotate(-.40).scale(.88), run_time=.63)
        for loop in pieces:
            loop.clear_updaters()
        scoop = spoon[1].get_center()
        self.play(*(loop.animate.move_to(scoop + p(x, y)).scale(.77)
                    for loop, (x, y) in zip(pieces, [(-.25, .23), (.22, .13), (-.05, -.20)])),
                  run_time=.28)
        self.bring_to_front(pieces)
        carry = RIGHT * (glass.get_x() - scoop[0]) + UP * .28
        self.play(clock_value.animate(run_time=.87).set_value(1),
                  spoon.animate(run_time=1.68).shift(carry), pieces.animate(run_time=1.68).shift(carry))
        self.at("Count what lands")
        self.play(pieces.animate.move_to(glass[2]).scale(.77), spoon.animate.shift(UP * .21),
                  FadeIn(caption("3 cereal loops", size=33, color=CER, y=-3.02)), run_time=.82)
        self.at("then tip it back")
        self.play(FadeOut(spoon, shift=UP * .53), run_time=.28)
        self.play(glass.animate.rotate(.95).shift(LEFT * .85 + UP * .54),
                  pieces.animate.move_to(p(1.47, -.27)), run_time=1.03)
        self.finish()


class S09Nectar(TableScene):
    def construct(self):
        bot, glass = nectar_station()
        bot.shift(DOWN * .80)
        s = tool(2).scale(.59).move_to(bot[2].get_center())
        s.shift(UP * (bot[3].get_y() + .15 - s.get_bottom()[1]))
        finger = hand().scale(.61).rotate(-1.32)
        self.start(bot, glass, s)
        self.at("Dip the straw")
        dip = bot[2].get_top()[1] + .19 - s.get_top()[1]
        self.play(s.animate.shift(UP * dip), run_time=1.40)
        water_bottom = s.get_bottom() + UP * .06
        water_height = bot[3].get_y() - water_bottom[1]
        water = panel(.085, water_height, RIPPLE, radius=.034)
        water.move_to(water_bottom + UP * water_height / 2)
        self.play(FadeIn(water), run_time=.23)
        self.at("cover the top", lead=.36)
        finger.shift(s.get_top() + p(.07, .035) - finger[4].get_right())
        self.play(FadeIn(finger, shift=LEFT * .55), run_time=.57)
        self.at("Lift it over")
        sealed = VGroup(s, water, finger)
        lift = bot[2].get_top()[1] + .12 - s.get_bottom()[1]
        self.play(sealed.animate.shift(UP * lift), run_time=.58)
        self.play(sealed.animate.shift(RIGHT * (glass.get_x() - s.get_x())), run_time=.78)
        lower = glass[1].get_top()[1] + .43 - s.get_bottom()[1]
        self.play(sealed.animate.shift(UP * lower), run_time=.23)
        self.at("uncover it", lead=.29)
        self.play(FadeOut(finger, shift=UP * .10 + LEFT * .55), run_time=.33)
        drop = oval(.13, .22, RIPPLE).move_to(s.get_bottom() + DOWN * .10)
        self.play(ReplacementTransform(water, drop), run_time=.27)
        self.play(drop.animate.move_to(glass[2]), run_time=.27)
        poured = oval(.71, .15, RIPPLE).move_to(glass[2]).shift(DOWN * .045)
        self.play(ReplacementTransform(drop, poured), run_time=.19)
        tally = ValueTracker(0)
        read = counter("Strawfuls  {:.0f}", tally, p(0, -2.85), size=34, color=STRAW, mono=False)
        self.at("Count each straw")
        self.add(read)
        self.play(tally.animate.set_value(1), s.animate.shift(UP * .40), run_time=.81)
        hummer = bird(3).scale(1.12).move_to(p(-1.2, -.05))
        bloom = flower().scale(.9).move_to(p(2.37, -.4))
        bob(hummer, amp=.14, speed=3.6)
        self.at("The straw models")
        self.play(FadeOut(VGroup(read, bot, glass, poured)), FadeIn(hummer), FadeIn(bloom),
                  s.animate.rotate(PI / 2).move_to(p(-1.50, 2.1)), run_time=.93)
        reach = caption("Straw models reach", color=STRAW, size=33)
        self.at("hummingbird's reach")
        self.play(FadeIn(reach), run_time=.60)
        self.at("A hummingbird uses")
        self.play(FadeOut(s), FadeOut(reach), run_time=.54)
        hummer.clear_updaters()
        tip = max(hummer.bill.get_vertices(), key=lambda point: point[0])
        tongue = Line(tip, bloom[-1].get_center(), color="#FFB5C4", stroke_width=6)
        self.at("its tongue")
        self.play(Create(tongue), run_time=.58)
        self.play(tongue.animate.scale(.68, about_point=tip), run_time=.29)
        self.play(tongue.animate.scale(1 / .68, about_point=tip), run_time=.39)
        self.finish()


BIRD_NAMES = ("Northern cardinal", "Mallard", "Great blue heron",
              "Ruby-throated hummingbird", "Carolina wren")


BIRD_TOOLS = (0, 1, 3, 2, 4)


def bird_match(kind):
    f = (lambda: oval(.64, .31, WOOD, angle=.36), ring, food_fish, flower, insect)[kind]()
    if kind == 3:
        f.scale(.68)
    if kind in (0, 1, 4):
        f.scale(1.38)
    b = bird(kind).scale(1.23).move_to(p(.65, -.05))
    t = tool(BIRD_TOOLS[kind]).scale(.99).move_to(p(-4.6, -.05))
    f.move_to(b.bill.get_right() + RIGHT * (f.width / 2 + .44) + DOWN * .09)
    return b, t, f


def insect():
    bark = panel(.93, 2.2, "#785641", radius=.13).shift(RIGHT * .57)
    bug = oval(.67, .32, CER, -.04, .1, .27)
    legs = VGroup(*(Line(p(x, .10), p(x + .10, y), color=CER, stroke_width=4)
                    for x in [-.21, -.01, .19] for y in [-.20, .39]))
    return VGroup(bark, legs, bug)


class S10ResultsAndBirds(TableScene):
    def construct(self):
        page, ledger = trial_sheet()
        bowl = pond().scale(.81).move_to(p(3.36, .10))
        pin = tool(0).scale(.54).rotate(-.52).move_to(p(.95, .25))
        spoon = tool(1).scale(.54).rotate(.64).move_to(p(5.93, .25))
        label = T("Example pond counts", 32, TEXT, weight=BOLD).move_to(p(-3.35, 1.68))
        self.start(page, drift_loops(bowl), pin, spoon, label)
        self.at("Check the pond counts")
        self.play(ledger.reveal(0), run_time=.66)
        self.play(ledger.reveal(1), run_time=.69)
        winner = Circle(radius=.34, color=GOLD, stroke_width=5).move_to(ledger.rows[1][1])
        self.at("Circle the best tool")
        self.play(Create(winner), spoon.animate.shift(UP * .44).rotate(-.32), run_time=1.23)
        self.at("Different beak shapes")
        guiding = caption("Different beak shapes work well for different foods.", size=31, color=GOLD)
        self.play(FadeIn(guiding), run_time=.68)
        data = VGroup(page, *ledger.rows, label, winner, bowl, pin, spoon, guiding)
        for kind, (cue, name) in enumerate(zip(
            ["A cardinal", "A mallard", "A heron", "A hummingbird", "A wren"], BIRD_NAMES
        )):
            b, t, food = bird_match(kind)
            self.at(cue, lead=.62)
            self.play(FadeOut(data), run_time=.25)
            water = oval(4.80, 1.28, WATER, 1.90, -.96) if kind == 1 else VGroup()
            self.play(FadeIn(VGroup(water, t, b, food), shift=LEFT * .20), run_time=.24)
            title = heading(name)
            tool_kind = BIRD_TOOLS[kind]
            tool_name = T(NAMES[tool_kind], 31, COLORS[tool_kind], weight=BOLD).move_to(p(-4.6, -2.70))
            self.play(FadeIn(title), FadeIn(tool_name), run_time=.46)
            move = -.43 if kind != 3 else -.22
            self.play(food.animate.shift(RIGHT * move), b.animate.shift(RIGHT * .22),
                      run_time=.93 if kind == 0 else 1.16)
            if kind == 0:
                halves = VGroup(oval(.30, .36, BEAN, -.19, -.04, .47),
                                oval(.30, .34, BEAN, .16, .08, -.61)).scale(1.3).move_to(food)
                self.play(ReplacementTransform(food, halves), halves.animate.shift(DOWN * .24), run_time=.48)
                food = halves
            elif kind == 1:
                drops = VGroup(*(Dot(food.get_center() + p(dx, -.45), radius=.085, color=RIPPLE)
                                 for dx in [-.18, .03, .24]))
                self.play(FadeIn(drops, shift=DOWN * .60), run_time=.51)
                food = VGroup(food, drops)
            elif kind == 2:
                self.play(food.animate.rotate(.35).shift(LEFT * .17 + UP * .19), run_time=.42)
            elif kind == 4:
                self.play(VGroup(*food[1:]).animate.shift(LEFT * .36 + UP * .21), run_time=.46)
            data = VGroup(water, t, b, food, title, tool_name)
        self.finish()


def flock(depths):
    return VGroup(*(bird(0, d).scale(.42).move_to(p(x, y)) for d, (x, y) in zip(
        depths, [(-1.35, 1.0), (1.0, 1.0), (-1.35, -.89), (1.0, -.89)]
    )))


class S11OneBirdVsPopulation(TableScene):
    def construct(self):
        panels = TwoPanel("One bird", "Many generations", colors=(WOOD, SPOON), top=2.82, bottom=-2.55)
        cardinal = bird(0).scale(.97)
        panels.put(cardinal, "left")
        seed = bean().move_to(cardinal.bill.get_right() + RIGHT * .48)
        self.start(panels.left_frame, panels.left_head, cardinal, seed)
        self.at("If your child asks")
        self.play(seed.animate.shift(LEFT * .32), cardinal.animate.rotate(-.085), run_time=1.80)
        shelf = panel(4.37, .28, WOOD, radius=.09).move_to(p(3.28, 1.37))
        reach = hand().scale(1.07).move_to(p(3.25, -.93))
        self.at("Can you grow longer")
        self.play(FadeIn(shelf), FadeIn(reach, shift=DOWN * .45), run_time=.56)
        self.play(reach.animate.shift(UP * .48), run_time=.73)
        self.play(reach.animate.shift(DOWN * .29), FadeOut(seed), run_time=.71)
        self.at("A bird's bill")
        bill = cardinal.bill
        bill.save_state()
        self.play(FadeOut(shelf), FadeOut(reach), bill.animate.stretch(1.40, 0, about_edge=LEFT), run_time=1.24)
        self.play(Restore(bill), run_time=1.22)
        self.at("A change in food")
        fish = food_fish().scale(.66).move_to(seed)
        self.play(FadeIn(fish), run_time=.73)
        self.play(fish.animate.shift(RIGHT * .11 + DOWN * .43), cardinal.animate.rotate(.09), run_time=1.58)
        fixed = caption("Same kind of bill", size=32, color=WOOD)
        self.play(FadeIn(fixed), run_time=.49)
        self.at("Over many generations")
        before = panels.put(flock([.67, 1.17, .72, .69]), "right")
        after = panels.put(flock([1.17, 1.17, 1.17, .69]), "right")
        first = T("Earlier flock", 28, SPOON).move_to(p(3.30, -2.06))
        later = T("Later flock", 28, SPOON).move_to(first)
        self.play(FadeOut(fixed), FadeIn(panels.right_frame), FadeIn(panels.right_head),
                  FadeIn(before), FadeIn(first), run_time=.71)
        self.at("bill shapes can change")
        self.play(swap(first, later), FadeOut(before, shift=LEFT * .55), run_time=.60)
        self.play(FadeIn(after, shift=RIGHT * .55), run_time=.74)
        self.finish()


class S12Safety(TableScene):
    def construct(self):
        glass = cup().scale(1.19).move_to(p(-3.44, -1.23))
        straw = tool(2).scale(.82).rotate(.21).move_to(p(-3.74, 1.24))
        tips = tool(4, .12).scale(1.10).move_to(p(3.26, .28))
        self.start(glass, straw)
        label = caption("Straws stay out of mouths", color=STRAW, size=32)
        drops = VGroup(*(Dot(p(x, y), color=RIPPLE, radius=.092)
                         for x, y in [(-3.43, -.2), (-3.5, .1), (-3.44, .37)]))
        self.at("Keep straws out")
        self.play(FadeIn(label), FadeIn(drops, shift=DOWN * .39), run_time=.92)
        self.play(drops.animate.shift(DOWN * .49), run_time=.52)
        self.at("tweezer tips down")
        point = caption("Tips down, away from faces", color=STEEL, size=32)
        self.play(swap(label, point), FadeIn(tips, shift=UP * .84), FadeOut(drops), run_time=1.28)
        self.at("Skip toothpicks")
        sharp = caption("Skip sharp points", color=GOLD, size=32)
        toothpick = shape([(-.11, -1.39), (.06, -1.39), (.10, .90), (0, 1.64)],
                         WOOD).rotate(-.54).move_to(p(.13, .18))
        self.play(swap(point, sharp), FadeIn(toothpick), run_time=.81)
        self.play(FadeOut(toothpick, shift=UP * .76), run_time=.52)
        puddle = oval(4.0, 2.12, WATER, .4, -.36, -.22)
        lost = VGroup(bean().move_to(p(1, -1.08)), ring(.46, -.39))
        wipe = VGroup(panel(2.23, 1.49, "#E9BE82", radius=.16), hand().scale(.75).shift(UP * .61))
        wipe.move_to(p(-3.68, -.27))
        self.at("Wipe up spills", lead=.48)
        self.replace_picture(VGroup(glass, straw, tips, sharp), VGroup(puddle, lost, wipe), .56)
        self.play(wipe.animate.shift(RIGHT * 3.84), puddle.animate.stretch(.35, 0, about_edge=RIGHT), run_time=.78)
        self.at("pick up dropped pieces")
        self.play(wipe.animate.shift(RIGHT * 1.75), FadeOut(puddle), FadeOut(lost), run_time=.92)
        bowl = pond().scale(.74).move_to(p(-2.6, .36))
        pan = fish_pan().scale(.67).move_to(p(2.56, .36))
        bowl_water, pan_water = bowl[0][2].set_z_index(1), pan[1].set_z_index(1)
        ripples = bowl[0][3:].set_z_index(2)
        loops, fish = bowl[1].set_z_index(3), pan[2:].set_z_index(3)
        left_hand = hand().scale(.67).rotate(-.86).move_to(p(-4.21, -.77)).set_z_index(4)
        right_hand = hand().scale(.67).rotate(.86).move_to(p(4.19, -.77)).set_z_index(4)
        vessels = VGroup(bowl, pan, left_hand, right_hand)
        self.at("Empty the bowls")
        self.replace_picture(wipe, vessels, .6)
        self.play(bowl.animate.rotate(.41).shift(DOWN * .49), pan.animate.rotate(-.43).shift(DOWN * .49),
                  left_hand.animate.rotate(.41).shift(DOWN * .49 + RIGHT * .21),
                  right_hand.animate.rotate(-.43).shift(DOWN * .49 + LEFT * .21), run_time=.94)
        splash = VGroup(*(Dot(p(x, y), radius=.105, color=RIPPLE)
                          for x, y in [(-2.72, -1.1), (-2.3, -1.52), (2.43, -1.1), (2.9, -1.55)]))
        self.add(splash)
        self.play(FadeOut(loops, shift=DOWN * .58), FadeOut(fish, shift=DOWN * .62),
                  bowl_water.animate.set_fill(INK), pan_water.animate.set_fill(INK), FadeOut(ripples),
                  FadeOut(splash, shift=DOWN * 1.11), run_time=.63)
        hands = VGroup(hand().rotate(-.59), hand().rotate(.72)).arrange(RIGHT, buff=-.42).scale(1.18)
        stream = VGroup(*(Line(p(x, 2.48), p(x - .13, .40), color=SPOON, stroke_width=6)
                          for x in [-.33, -.13, .07, .27]))
        suds = VGroup(*(Circle(radius=.11 + .055 * (i % 3), color=WHITE, stroke_width=3).move_to(p(x, y))
                       for i, (x, y) in enumerate([(-.65, .42), (.3, .83), (1.0, -.08), (-.2, -.3),
                                                    (.62, -.61), (.91, .51), (-1.09, .11)])))
        self.at("Wash hands with soap")
        empty_vessels = VGroup(bowl[0][:3], pan[:2], left_hand, right_hand)
        self.replace_picture(empty_vessels, VGroup(hands, stream, suds), .53)
        self.play(hands[0].animate.shift(RIGHT * .36), hands[1].animate.shift(LEFT * .26 + UP * .14),
                  suds.animate.shift(DOWN * .53), run_time=1.25)
        self.finish()


class S13Close(TableScene):
    def construct(self):
        page, ledger = trial_sheet()
        label = T("Example pond counts", 32, TEXT, weight=BOLD).move_to(p(-3.35, 1.68))
        pin = tool(0).scale(.64).rotate(-.58).move_to(p(1.43, .55))
        spoon = tool(1).scale(.69).rotate(.38).move_to(p(4.17, .38))
        self.start(page, label, *ledger.rows, pin, spoon)
        self.at("Ask what helped")
        q = question_card("What helped one tool work better?", size=34)
        self.play(FadeIn(q), spoon.animate.rotate(.29), run_time=1.27)
        self.at("use the counts")
        self.play(ledger.mark(1), pin.animate.shift(DOWN * .34), run_time=.92)
        self.at("Watch how the tools move")
        self.play(FadeOut(q), spoon.animate.rotate(-.81).shift(UP * .24), run_time=1.2)
        heron = bird(2).scale(.92).move_to(p(1.89, -.38))
        heron[3:8].rotate(-.45, about_point=p(1.52, -.36))
        marsh = oval(5.15, 1.47, WATER, 3.39, -1.60)
        fish = food_fish().scale(.46).flip().move_to(p(5.37, -1.62))
        self.at("A heron waits", lead=.61)
        self.replace_picture(VGroup(pin, spoon), VGroup(marsh, heron, fish), run_time=.51)
        self.play(fish.animate.move_to(p(heron.bill.get_right()[0] + .30, -1.42)), run_time=1.96)
        self.finish()


class S14End(EndCard):
    LINE = "Different beak shapes work well for different foods."
