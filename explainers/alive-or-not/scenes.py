"""The Alive or Not? parent guide, staged on a single illustrated tabletop."""
import os

from bp_parts import *
from bp_style import EndCard

WOOD = "#523126"
GRAIN = "#634032"
PAPER = "#F0D8AB"
CREAM = "#FFDF9C"
RUST = "#D99560"
LEAF = "#BA7849"
DEEP = "#25202A"
LIVING = "#265C53"
FORMER = "#794928"
NONLIVING = "#344A65"
CAR_AT = [-3.55, -0.30, 0]
BEAN_AT = [3.55, -0.25, 0]
LEAF_AT = [0, 0.2, 0]
BASKET_AT = [-2.65, -0.15, 0]
ROCK_AT = [-3.85, -1.0, 0]
LIST_AT = [3.1, 0, 0]
PREDICT = "Living or Nonliving?"


def p(x, y):
    return np.array([x, y, 0.])


def solid(shape, color, edge=None, stroke=3):
    return shape.set_fill(color, 1).set_stroke(edge or color, stroke)


def disc(x, y, r, color):
    return Dot(p(x, y), radius=r, color=color)


def oval(w, h, color, edge=None):
    return solid(Ellipse(width=w, height=h), color, edge)


def block(w, h, color, edge=None, corner=.15):
    return solid(RoundedRectangle(width=w, height=h, corner_radius=corner), color, edge)


def line(a, b, color, width=4):
    return Line(p(*a), p(*b), stroke_color=color, stroke_width=width)


def polygon(points, color, edge=None):
    return solid(Polygon(*(p(*q) for q in points)), color, edge)


def silhouette(start, segments, color, edge=None):
    outline = VMobject().start_new_path(p(*start))
    for handle1, handle2, end in segments:
        outline.add_cubic_bezier_curve_to(p(*handle1), p(*handle2), p(*end))
    return solid(outline, color, edge)


def table():
    top = Rectangle(width=config.frame_width, height=config.frame_height,
                    stroke_width=0, fill_color=WOOD, fill_opacity=1)
    grain = VGroup()
    for x, y, w in [(-5.8, 2.6, 1.2), (0.1, 3.72, 3.9),
                    (-5.75, -3.21, 1.85), (-2, -3.57, 2.4),
                    (3.3, -3.66, 2.2), (5.8, -3.43, 1.3)]:
        grain.add(oval(w, .027, GRAIN).move_to(p(x, y)))
    return VGroup(top, grain).set_z_index(-10)


def mat(label, color, center, width=5.85, height=5.0):
    edge = {LIVING: GREEN, FORMER: RUST, NONLIVING: BLUE}[color]
    rim = oval(width, height, color, edge).move_to(center)
    inset = Ellipse(width=width - .27, height=height - .27, color=edge,
                    stroke_width=1.3, stroke_opacity=.55).move_to(center)
    name = T(label, 35, TEXT, weight=BOLD).move_to(center + UP * (height / 2 - (1.34 if width < 4 else .86)))
    return VGroup(rim, inset, name)


def mats(labels=("Alive", "Not alive")):
    return VGroup(mat(labels[0], LIVING, p(-3.22, -.28)),
                  mat(labels[1], NONLIVING, p(3.22, -.28)))


def three_mats():
    return VGroup(mat("Alive now", LIVING, p(-4.32, -.28), 3.72),
                  mat("Once alive", FORMER, p(0, -.28), 3.72),
                  mat("Nonliving", NONLIVING, p(4.32, -.28), 3.72))


def car():
    wheels = VGroup(disc(-.72, -.32, .28, DEEP), disc(.73, -.32, .28, DEEP),
                    disc(-.72, -.32, .11, GREY), disc(.73, -.32, .11, GREY))
    roof = polygon([(-.93, .09), (-.48, .64), (.42, .64), (.88, .09)], RED, "#FF9D7F")
    glass = polygon([(-.65, .16), (-.33, .52), (.31, .52), (.59, .16)], "#B5D8DE")
    body = block(2.42, .48, "#DD443D", RED).move_to(p(0, -.065))
    lamp = block(.19, .12, CREAM, corner=.035).move_to(p(1.04, -.04))
    return VGroup(roof, glass, line((-.02, .18), (-.02, .53), RED, 5), body, lamp, wheels)


def bean():
    skin = silhouette((-.99, -.07), [
        ((-1.14, .54), (-.38, .76), (.25, .62)),
        ((.96, .49), (1.11, .01), (.91, -.40)),
        ((.64, -.90), (.05, -.78), (-.13, -.41)),
        ((-.34, -.17), (-.83, -.49), (-.99, -.07)),
    ], CREAM, "#C48E56")
    crease = ArcBetweenPoints(p(-.42, -.24), p(.11, -.47), angle=-.8,
                              color="#A36D47", stroke_width=5)
    return VGroup(skin, crease, oval(.59, .10, "#FFF0C5").rotate(-.18).move_to(p(-.35, .36)))


def leaf(blade=LEAF, vein="#F6BF7D", *, petiole=True):
    base = (-1.09, -.57)
    outline = silhouette(base, [
        ((-1.14, .55), (-.02, .87), (1.10, .56)),
        ((.91, -.33), (.02, -.86), (-1.09, -.57)),
    ], blade, vein)
    ribs = VGroup(line((-1.29, -.71) if petiole else base, (.83, .50), vein, 3),
                  line((-.64, -.34), (-.57, .28), vein, 2),
                  line((-.35, -.16), (.16, -.45), vein, 2),
                  line((.06, .07), (.11, .52), vein, 2),
                  line((.31, .22), (.67, .03), vein, 2))
    return VGroup(outline, ribs)


def plant():
    leaves = VGroup(leaf("#76B875", "#A7DB87", petiole=False).scale(.45).rotate(1.07).move_to(p(-.02, 1.28)),
                    leaf("#478662", "#9BCC7B", petiole=False).scale(.46).rotate(2.65).move_to(p(-.75, .44)),
                    leaf("#559957", "#A7DB87", petiole=False).scale(.48).move_to(p(.76, .58)))
    top, left, right = (blade[0].get_start() for blade in leaves)
    stem = Line(p(0, -.52), top, color=GREEN, stroke_width=7)
    stems = VGroup(stem,
                   Line(stem.point_from_proportion(.23), left, color=GREEN, stroke_width=6),
                   Line(stem.point_from_proportion(.42), right, color=GREEN, stroke_width=6))
    pot = polygon([(-.73, -.50), (.73, -.50), (.56, -1.49), (-.56, -1.49)],
                  "#BF6748", "#E79062")
    lip = block(1.62, .26, "#E79062", corner=.08).move_to(p(0, -.49))
    return VGroup(VGroup(stems, leaves), pot, lip)


def rock():
    body = polygon([(-1.05, -.39), (-.91, .17), (-.43, .59), (.31, .72),
                    (.86, .31), (1.02, -.26), (.64, -.56), (-.63, -.65)],
                   "#8795A2", "#C1C8CD")
    face = polygon([(-1.02, -.36), (-.46, -.20), (.09, .15), (.85, .31),
                    (1.0, -.24), (.63, -.53), (-.63, -.62)], "#596878")
    return VGroup(body, face)


def apple():
    body = silhouette((0, .52), [
        ((.65, .91), (.99, .32), (.78, -.26)),
        ((.60, -.90), (.16, -.90), (0, -.66)),
        ((-.39, -.98), (-.75, -.58), (-.83, -.10)),
        ((-.96, .46), (-.43, .84), (0, .52)),
    ], "#BD4843", "#EC7B65")
    return VGroup(line((0, .48), (-.075, .84), RUST, 5), body,
                  leaf("#679B55", GREEN).scale(.28).move_to(p(.31, .79)))


def stick():
    return VGroup(line((-.98, -.59), (1.03, .51), "#C48553", 14),
                  line((-.10, -.11), (-.38, .66), "#C48553", 9),
                  line((.46, .18), (.76, -.34), "#C48553", 7),
                  line((-.85, -.55), (.94, .45), "#E1A96F", 2))


def shell():
    shape = silhouette((0, -.65), [
        ((-.36, -.72), (-1.18, .00), (-.79, .51)),
        ((-.38, 1.00), (.42, 1.00), (.82, .52)),
        ((1.18, -.02), (.45, -.63), (0, -.65)),
    ], "#E1B791", CREAM)
    flutes = VGroup(*(line((0, -.49), (x, y), "#A17561", 3)
                      for x, y in [(-.68, .25), (-.40, .59), (0, .67), (.40, .59), (.68, .25)]))
    return VGroup(shape, flutes)


def spoon():
    handle = block(.22, 1.50, "#A9BEC6", corner=.10).move_to(p(0, -.36))
    bowl = oval(.78, 1.0, "#DBE7E7", "#F3F8F6").move_to(p(0, .60))
    return VGroup(handle, bowl, oval(.49, .70, "#AFCCD2").move_to(p(.04, .65))).rotate(-.64)


def picture(builder, height, where):
    return builder().set_height(height).move_to(where)


def basket():
    outer = oval(6.3, 5.16, "#A76B42", "#E0A16D")
    inner = oval(5.82, 4.70, "#744632", "#EDBB85")
    weave = VGroup()
    for side in (-1, 1):
        for x in (.35, .92, 1.49, 2.06, 2.57):
            y = side * 2.47 * np.sqrt(1 - (x / 3.03) ** 2)
            for dx in (-x, x):
                weave.add(oval(.29, .073, "#F0BC82").move_to(p(dx, y)))
    return VGroup(outer, inner, weave).move_to(BASKET_AT)


SUPPLIES = ((plant, 1.95, (-1.1, .71)), (apple, .83, (.23, .71)),
            (leaf, .78, (1.44, .82)), (stick, .80, (1.91, -.24)),
            (shell, .68, (-2.00, -.30)), (rock, .67, (-1.19, -.88)),
            (spoon, .83, (-.09, -.57)), (car, .64, (.94, -.99)),
            (bean, .46, (.07, -1.68)), (bean, .43, (.80, -1.76)))


def supplies():
    return [picture(draw, height, BASKET_AT + p(*offset)) for draw, height, offset in SUPPLIES]


def pencil():
    tip = polygon([(-.18, -.64), (.18, -.64), (0, -.99)], "#D69B6B")
    point = polygon([(-.067, -.86), (.067, -.86), (0, -.99)], DEEP)
    return VGroup(block(.36, 1.52, YELLOW, corner=.06), tip, point,
                  block(.36, .25, "#E88686", corner=.055).move_to(p(0, .81))).rotate(-.59)


def pad(where, heading=None):
    paper = block(3.42, 2.62, "#322B2B", "#C3986E")
    ruling = VGroup(*(line((-1.38, y), (1.38, y), "#856C5B", 2) for y in (-.12, -.50, -.88)))
    obj = VGroup(paper, ruling).move_to(where)
    if heading:
        obj.add(T(heading, 31, TEXT, weight=BOLD).move_to(where + UP * .55))
    return obj


def mark(positive, color=None):
    if positive:
        return VGroup(line((-.16, .0), (-.03, -.14), color or GREEN, 6),
                      line((-.03, -.14), (.20, .15), color or GREEN, 6))
    return VGroup(line((-.14, -.14), (.14, .14), color or RED, 6),
                  line((-.14, .14), (.14, -.14), color or RED, 6))


def droplet():
    start = (0, .5)
    return silhouette(start, [
        ((.13, .23), (.40, -.03), (.35, -.24)),
        ((.32, -.63), (-.32, -.63), (-.35, -.24)),
        ((-.40, -.03), (-.13, .23), start),
    ], BLUE)


def sun():
    rays = VGroup(*(Line(p(.49, 0), p(.70, 0), color=YELLOW, stroke_width=5)
                    .rotate(k * TAU / 8, about_point=ORIGIN) for k in range(8)))
    return VGroup(disc(0, 0, .34, YELLOW), rays)


def sprout():
    return VGroup(bean().scale(.39).move_to(p(0, -.5)),
                  line((0, -.48), (0, .47), GREEN, 6),
                  leaf("#539556", GREEN).scale(.29).move_to(p(.32, .39)),
                  leaf("#549A60", GREEN).scale(.26).rotate(2.65).move_to(p(-.28, .17)))


def clue_icons():
    reaction = VGroup(line((-.24, -.1), (-.06, .19), YELLOW, 5),
                      line((-.06, .19), (.02, -.15), YELLOW, 5),
                      line((.02, -.15), (.24, .13), YELLOW, 5))
    more = VGroup(disc(-.16, -.08, .13, GREEN), disc(.16, -.08, .13, GREEN),
                  disc(0, .15, .12, GREEN))
    return [sprout().set_height(.52), droplet().set_height(.47), reaction, more]


def checklist():
    panel = block(5.44, 5.18, "#25383D", "#8CAEA1").move_to(LIST_AT)
    header = T("Four clues", 38, TEXT, weight=BOLD).move_to(LIST_AT + UP * 1.93)
    keys = ("Grows", "Water air food", "Reacts", "Makes more")
    ledger = Ledger([(key, "", TEXT) for key in keys], top_left=(1.76, 1.03),
                    row_h=.94, key_w=3.25, width=4.12, size=33)
    for index, (row, icon) in enumerate(zip(ledger.rows, clue_icons())):
        row.add(icon.move_to(p(1.16, 1.03 - .94 * index)))
    return VGroup(panel, header), ledger


def gumdrop_packet():
    packet = block(1.40, 1.87, "#31574A", GREEN)
    front = leaf("#588C57", GREEN).set_height(.53).move_to(p(0, -.31))
    return VGroup(packet, T("Seeds", 30, TEXT).move_to(p(0, .59)), front)


def hook_world():
    return (mats(), picture(car, 1.85, CAR_AT), picture(bean, 2.18, BEAN_AT),
            T("?", 72, CREAM, weight=BOLD).move_to(p(0, 1.66)))


class S01Hook(SpokenScene, TitleCard):
    TITLE = "Alive or Not? — Parent Guide"
    LESSON = "Alive or Not?"

    def construct(self):
        sorting, toy, seed, question = hook_world()
        toy.shift(LEFT * 1.34)
        seed.shift(RIGHT * 1.12)
        self.add(table(), sorting, toy, seed)
        self.at("toy car moves", lead=.5)
        self.play(toy.animate.move_to(CAR_AT), run_time=1.75)
        self.at("a dry bean", lead=.4)
        self.play(MoveAlongPath(seed, ArcBetweenPoints(seed.get_center(), BEAN_AT,
                                                      angle=.80)), run_time=1.25)
        self.at("which one")
        self.play(FadeIn(question, scale=.83), run_time=.48)
        bob(question, amp=.16, speed=2.0)
        self.at("use this")
        self.play(toy.animate.shift(RIGHT * .31), run_time=1.8, rate_func=there_and_back)
        self.at("they make a rule")
        self.play(toy.animate.shift(LEFT * .26), run_time=1.8, rate_func=there_and_back)
        self.finish()


class S02Title(TitleCard):
    TITLE = S01Hook.TITLE
    LESSON = S01Hook.LESSON

    def construct(self):
        sorting, toy, seed, _ = hook_world()
        world = VGroup(sorting, toy, seed)
        title = boxed_label(self.TITLE, CREAM, size=52, pad=.29).move_to(p(0, 2.85))
        title.box.set_fill(DEEP, 1)
        self.add(table(), world)
        self.play(world.animate.shift(DOWN * .46), FadeIn(title, shift=DOWN * .19),
                  run_time=.83)
        self.play(toy.animate.shift(RIGHT * .15), seed.animate.shift(UP * .09),
                  run_time=1.08, rate_func=there_and_back)


class S03Gather(SpokenScene):
    def construct(self):
        container = basket()
        objects = supplies()
        self.add(table())
        self.at("fill a basket")
        self.play(FadeIn(container, shift=RIGHT * .68), run_time=1.0)
        cues = ("houseplant", "apple", "dry leaf", "stick", "shell", "rock", "spoon", "toy car")
        for index, phrase in enumerate(cues):
            self.at(phrase, lead=.22)
            self.play(FadeIn(objects[index], shift=LEFT * .66), run_time=.42)
        notes = pad(p(3.45, -.55))
        pen = picture(pencil, 1.70, p(5.93, -.36))
        self.at("set out paper")
        self.play(FadeIn(notes, shift=LEFT * .8), run_time=.48)
        self.at("pencil")
        self.play(FadeIn(pen, shift=LEFT * .5), run_time=.55)
        self.play(pen.animate.rotate(.24), run_time=.75, rate_func=there_and_back)
        self.at("large dry kitchen beans", lead=.72)
        for index, item in enumerate(objects[8:]):
            seed = picture(bean, .91, p(.92 + .64 * index, -.91 - .71 * index))
            self.play(FadeIn(seed, shift=LEFT * .48), run_time=.34)
            self.play(Transform(seed, item), run_time=.61)
        packet = gumdrop_packet().move_to(p(3.45, 2.15))
        crossed = mark(False).scale(1.65).move_to(packet.get_center())
        self.at("skip garden shop")
        self.play(FadeIn(packet, shift=LEFT * .3), run_time=.45)
        self.play(Create(crossed), run_time=.37)
        self.wait(.46)
        self.play(FadeOut(packet), FadeOut(crossed), run_time=.36)
        self.finish()


class S04FirstGuess(SpokenScene):
    def construct(self):
        container, items = basket(), supplies()
        sorting = mats()
        toy = picture(car, 1.70, p(-4.30, -.39))
        seed = picture(bean, 1.28, BEAN_AT + LEFT * .59)
        flora = picture(plant, 1.85, p(-1.60, -.23))
        stone = picture(rock, 1.08, p(4.76, -.08))
        self.add(table(), container, *items)
        self.at("sort everything")
        pile = VGroup(container, *items)
        self.play(pile.animate.rotate(-.13).move_to(p(0, .36)).scale(.80), run_time=.76)
        self.play(FadeOut(pile, shift=UP * .6), run_time=.37)
        self.play(FadeIn(sorting), run_time=.36)
        small = VGroup(picture(apple, .72, p(-2.90, -1.79)),
                       picture(leaf, .58, p(1.66, -.97)),
                       picture(stick, .62, p(2.08, -1.62)),
                       picture(shell, .51, p(4.26, -1.69)),
                       picture(spoon, .79, p(5.13, -1.06)),
                       picture(bean, .43, p(3.55, -1.75)))
        self.play(FadeIn(flora, shift=LEFT * .7), FadeIn(stone, shift=RIGHT * .61),
                  run_time=.65)
        self.at("alive and not alive", lead=-.55)
        self.play(FadeIn(toy, shift=LEFT * .56), FadeIn(seed, shift=RIGHT * .70), run_time=.80)
        self.play(LaggedStart(*(FadeIn(item, shift=RIGHT * (.5 if i else -.5))
                                for i, item in enumerate(small)), lag_ratio=.12), run_time=.68)
        self.at("hold back")
        self.play(toy.animate.shift(RIGHT * .51), run_time=2.40, rate_func=there_and_back)
        self.at("instead ask")
        question = caption("How did you decide?", size=35, color=CREAM)
        self.play(FadeIn(question), run_time=.42)
        self.at("write down their rule")
        pad_at = p(3.04, -1.42)
        notes = pad(pad_at).scale(.62)
        pen = picture(pencil, 1.13, p(4.67, -1.48))
        label = T("My rule", 34, TEXT, weight=BOLD).move_to(pad_at + UP * .34)
        self.play(FadeOut(small), seed.animate.scale(.65).move_to(p(2.60, .02)),
                  run_time=.38)
        self.play(FadeIn(notes, shift=UP * .28), run_time=.48)
        self.add(pen)
        self.play(Write(label), pen.animate.shift(RIGHT * .15).rotate(.12), run_time=1.22)
        self.at("listening first")
        self.play(FadeOut(question), pen.animate.shift(DOWN * .12), run_time=.58)
        self.finish()


class S05Checklist(SpokenScene):
    def construct(self):
        flora = picture(plant, 4.45, p(-2.82, .43))
        foliage, _, lip = flora
        pivot = lip.get_center()
        sway_time = 0.0

        def sway(leaves_and_stems, dt):
            nonlocal sway_time
            before = np.sin(1.9 * sway_time)
            sway_time += dt
            angle = .044 * (np.sin(1.9 * sway_time) - before)
            leaves_and_stems.rotate(angle, about_point=pivot)

        stone = picture(rock, 1.16, ROCK_AT + LEFT * 1.06 + DOWN * 1.01)
        panel, list_rows = checklist()
        self.add(table())
        self.at("compare the rock")
        self.play(FadeIn(stone, shift=RIGHT * .56), run_time=.52)
        self.play(FadeIn(flora, shift=LEFT * .47), run_time=.77)
        foliage.add_updater(sway)
        self.at("what does it do")
        self.play(stone.animate.shift(RIGHT * .52), run_time=1.65, rate_func=there_and_back)
        self.at("write four clues")
        self.play(FadeIn(panel, shift=LEFT * .48), run_time=.70)
        for index, phrase in enumerate(("grows", "needs water", "reacts", "makes more")):
            self.at(phrase)
            self.play(list_rows.reveal(index), run_time=.40)
        light = picture(sun, 1.22, p(-.99, 2.13))
        self.at("plants use light")
        self.play(FadeIn(light, scale=.76), run_time=.51)
        foliage.remove_updater(sway)
        self.play(Rotate(foliage, -.13, about_point=pivot), run_time=1.1)
        self.at("check all four")
        self.play(panel[0].animate.set_stroke(CREAM, width=4), run_time=.72)
        self.finish()


class S06Tricky(SpokenScene):
    def construct(self):
        stone = picture(rock, 2.38, p(-3.24, -.32))
        panel, ledger = checklist()
        mistakes = [mark(False).move_to(p(5.27, 1.03 - .94 * i)) for i in range(4)]
        self.add(table(), panel, *ledger.rows, stone)
        self.at("try the checklist")
        self.play(LaggedStart(*(Create(m) for m in mistakes), lag_ratio=.44), run_time=2.16)
        self.at("then let your child")
        self.play(stone.animate.shift(LEFT * .65), run_time=2.2, rate_func=there_and_back)
        self.at("with the car", lead=.75)
        toy = picture(car, 2.20, p(-3.24, -.32))
        self.play(FadeOut(stone), *(FadeOut(m) for m in mistakes), run_time=.30)
        self.play(FadeIn(toy, shift=RIGHT * .85), run_time=.44)
        self.play(toy.animate.shift(RIGHT * 1.05), run_time=1.32, rate_func=there_and_back)
        car_marks = [mistakes[i].copy() for i in (0, 3)]
        self.at("does it grow", lead=.03)
        self.play(Create(car_marks[0]), run_time=.30)
        self.at("make a baby car", lead=.03)
        self.play(Create(car_marks[1]), run_time=.30)
        self.at("a dry seed", lead=.55)
        seed = picture(bean, 2.13, p(-4.37, -1.46))
        self.play(FadeOut(toy), *(FadeOut(m) for m in car_marks), FadeIn(seed, shift=UP * .35),
                  run_time=.69)
        thought = oval(4.89, 2.60, "#3B4242", "#B0C6B2").move_to(p(-2.67, 1.20))
        trail = VGroup(disc(-4.19, -.26, .115, "#B0C6B2"), disc(-4.52, -.51, .065, "#B0C6B2"))
        self.play(FadeIn(thought), FadeIn(trail), run_time=.60)
        self.at("water and warmth", lead=.32)
        self.play(FadeIn(picture(droplet, .76, p(-4.11, 1.20))),
                  FadeIn(picture(sun, .92, p(-2.83, 1.20))), run_time=.35)
        self.at("let it sprout", lead=.58)
        self.play(GrowFromCenter(picture(sprout, 1.55, p(-1.36, 1.20))), run_time=.45)
        self.finish()


def predict_world():
    sorting = mats(("Living", "Nonliving"))
    dry = picture(leaf, 2.35, LEAF_AT)
    q = question_card(PREDICT, y=2.97, size=42, color=CREAM)
    q.shift(RIGHT * .5)
    return sorting, dry, q


class S07PredictQ(SpokenScene):
    def construct(self):
        sorting, dry, question = predict_world()
        background, ledger = checklist()
        old = VGroup(background, *ledger.rows).set_opacity(.40)
        self.add(table(), old)
        dry.shift(LEFT * 2.35)
        self.at("picture the dry leaf")
        self.play(FadeIn(dry, shift=UP * .65), run_time=.85)
        self.at("using just two piles")
        self.play(FadeOut(old), run_time=.34)
        self.play(FadeIn(sorting), dry.animate.move_to(LEAF_AT), run_time=.56)
        self.bring_to_front(dry)
        self.play(dry.animate.rotate(-.17), run_time=2.05, rate_func=there_and_back)
        self.at("pause and decide")
        self.play(FadeIn(question, shift=DOWN * .18), run_time=.55)
        self.play(dry.animate.shift(RIGHT * .29), run_time=1.67, rate_func=there_and_back)
        self.at("which pile")
        self.play(dry.animate.shift(LEFT * .27), run_time=2.3, rate_func=there_and_back)
        self.finish()


class S08PredictPause(Scene):
    def construct(self):
        self.add(table(), *predict_world())
        track = line((-2.83, -3.30), (2.83, -3.30), "#8F6650", 9)
        progress = line((-2.83, -3.30), (2.83, -3.30), CREAM, 9)
        self.add(track)
        bead = disc(-2.83, -3.30, .095, CREAM)
        self.add(bead)
        self.play(Create(progress, rate_func=linear),
                  bead.animate(rate_func=linear).move_to(p(2.83, -3.30)),
                  run_time=float(os.environ["KX_DURATION"]))


def branch():
    twigs = VGroup(line((-1.65, -1.94), (-3.95, .80), "#AA865C", 10),
                   line((-2.48, -.93), (-3.92, -.51), "#AA865C", 6),
                   line((-3.28, .00), (-2.92, .76), "#AA865C", 5))
    return twigs.set_opacity(.67)


def sorted_objects():
    positions = (
        (plant, 2.21, p(-4.69, -.49)),
        (bean, .72, p(-3.32, -1.37)),
        (leaf, 1.23, p(-.06, -.38)),
        (stick, .84, p(.33, -1.53)),
        (rock, 1.02, p(4.69, -.94)),
    )
    return [picture(draw, height, point) for draw, height, point in positions]


class S09PredictReveal(SpokenScene):
    def construct(self):
        sorting, dry, question = predict_world()
        self.add(table(), sorting, dry, question)
        self.at("for this sort")
        rule = caption("Virginia’s kindergarten sort", size=31, color=CREAM)
        self.play(FadeOut(question), FadeIn(rule), run_time=.48)
        self.play(dry.animate.shift(LEFT * .64), run_time=1.35, rate_func=there_and_back)
        self.at("the dry leaf goes")
        self.play(dry.animate.scale(.73).rotate(.18).move_to(p(-3.50, -.49)), run_time=1.75)
        self.at("it was part")
        origin = branch()
        self.play(Create(origin), run_time=1.68)
        self.bring_to_front(dry)
        self.at("a rock goes")
        flora, seed, former_leaf, twig, stone = sorted_objects()
        self.play(FadeIn(stone, shift=LEFT * .82), run_time=.75)
        self.at("for ages 8 to 10")
        ages = caption("Ages 8–10", size=32, color=CREAM)
        self.play(swap(rule, ages), run_time=.65)
        self.at("split the living pile")
        revised = three_mats()
        self.play(FadeOut(sorting[0][2]), FadeOut(sorting[1][2]), FadeOut(origin),
                  run_time=.31)
        self.play(Transform(sorting[0][0], revised[0][0]), Transform(sorting[0][1], revised[0][1]),
                  Transform(sorting[1][0], revised[2][0]), Transform(sorting[1][1], revised[2][1]),
                  FadeIn(VGroup(*revised[1][:2])), Transform(dry, former_leaf), run_time=.74)
        self.bring_to_front(dry, stone)
        self.play(*(FadeIn(mat_group[2]) for mat_group in revised), run_time=.31)
        self.at("alive now", lead=.02)
        self.play(FadeIn(flora, shift=RIGHT * .39), FadeIn(seed, shift=UP * .35),
                  run_time=.66)
        self.at("once alive", lead=.10)
        self.play(FadeIn(twig, shift=UP * .43), run_time=.76)
        self.finish()


def jar():
    glass = block(3.38, 4.02, "#35575B", "#9ED6CD", corner=.46)
    lip = block(2.86, .40, "#4D7470", "#A5D6CA").move_to(p(0, 1.78))
    shine = line((-1.31, -.86), (-1.31, 1.26), "#6A9C92", 7)
    floor = oval(2.35, .19, "#497772").move_to(p(0, -1.63))
    lid = block(3.07, .47, "#B9C5CC", "#ECF2E9").move_to(p(0, 2.37))
    ribs = VGroup(*(line((x, 2.25), (x, 2.49), "#8799A4", 2)
                     for x in np.linspace(-1.26, 1.26, 9)))
    return VGroup(glass, lip, shine, floor), VGroup(lid, ribs)


class S10Safety(SpokenScene):
    def construct(self):
        container = basket()
        seeds = [picture(bean, .93, p(-3.23, -.22)), picture(bean, .94, p(-1.65, -.43))]
        glass, lid = jar()
        glass.shift(RIGHT * 3.28 + DOWN * .25)
        lid.shift(RIGHT * 3.28 + UP * .78)
        self.add(table(), container)
        self.at("stay with your child")
        self.play(FadeIn(seeds[0], shift=UP * .37), run_time=.65)
        self.play(FadeIn(seeds[1], shift=UP * .37), run_time=.65)
        self.at("keep all small objects")
        self.play(FadeIn(glass, shift=LEFT * .45), FadeIn(lid, shift=LEFT * .45),
                  run_time=.95)
        self.at("under 4", lead=.72)
        under = boxed_label("Under 4: no small items", CREAM, size=32).move_to(p(-2.6, 2.96))
        under.box.set_fill(DEEP, 1)
        self.play(FadeIn(under), run_time=.55)
        self.at("keep everything in")
        no_taste = boxed_label("No tasting", TEXT, size=34).move_to(p(-2.65, -1.63))
        no_taste.box.set_fill(DEEP, 1)
        self.play(FadeIn(no_taste, shift=UP * .19), run_time=.55)
        self.at("count the beans")
        self.play(FadeOut(no_taste), run_time=.28)
        self.bring_to_front(*seeds)
        for index, seed in enumerate(seeds):
            target = p(2.56 + index * 1.44, -1.41 + index * .16)
            arc = ArcBetweenPoints(seed.get_center(), target, angle=-1.45)
            self.play(MoveAlongPath(seed, arc), run_time=.86)
        self.play(lid.animate.shift(DOWN * 1.13), run_time=.52)
        self.at("if a child is choking", lead=.38)
        urgent = boxed_label("Choking? Call 911", TEXT, size=44, pad=.32).move_to(p(-2.68, 0))
        urgent.box.set_fill("#9C302D", 1).set_stroke(RED, 4)
        self.play(FadeOut(under), FadeOut(container), run_time=.28)
        self.play(FadeIn(urgent, scale=.85), run_time=.51)
        self.at("call 911", lead=.36)
        self.play(urgent.box.animate.set_stroke(CREAM, 5), run_time=.75)
        self.finish()


def tree():
    trunk = block(.32, 2.52, "#825538", corner=.13).move_to(p(0, -.83))
    crown = VGroup(disc(-.71, .55, .77, "#377B63"),
                   disc(.66, .63, .80, "#4B8960"), disc(0, 1.37, .91, "#57995E"),
                   disc(-.06, .69, .84, "#4B9369"))
    return VGroup(trunk, crown)


def magnifier():
    ring = Circle(radius=.86, stroke_color=CREAM, stroke_width=10)
    lens = Circle(radius=.76, fill_color=BLUE, fill_opacity=.14, stroke_width=0)
    handle = block(.23, .92, "#B28D63", CREAM, corner=.11).rotate(.62).move_to(p(.78, -.91))
    return VGroup(handle, lens, ring)


def footpath():
    lawn = Rectangle(width=config.frame_width, height=config.frame_height, stroke_width=0,
                     fill_color="#284B43", fill_opacity=1).set_z_index(-9)
    track = silhouette((-7.3, -2.58), [
        ((-3.9, -3.46), (.12, -2.63), (2.9, -1.29)),
        ((4.92, -.31), (5.2, .45), (7.3, .54)),
        ((7.3, .05), (7.3, -.69), (7.3, -1.18)),
        ((5.66, -1.17), (5.46, -2.27), (3.61, -3.06)),
        ((.60, -4.29), (-4.81, -4.30), (-7.3, -4.28)),
        ((-7.3, -3.81), (-7.3, -3.0), (-7.3, -2.58)),
    ], "#C7A776").set_z_index(-8)
    tufts = VGroup()
    for x, y in [(-6.2, -.30), (-5.6, -2.03), (-2.0, -1.52), (-1.2, 1.37),
                 (1.08, -.02), (6.1, -2.65), (0.0, -1.79)]:
        tufts.add(line((x, y), (x - .13, y + .20), "#5C8763", 3),
                  line((x, y), (x + .14, y + .26), "#5C8763", 3))
    water = oval(4.13, 2.47, "#3A7480", "#80BFBA").move_to(p(4.51, 1.76))
    ripples = VGroup(oval(1.77, .045, "#7BB7B5").move_to(p(4.45, 1.57)),
                     oval(1.12, .042, "#7BB7B5").move_to(p(5.20, 2.08)))
    boundary = VMobject(stroke_color="#E4B586", stroke_width=4).start_new_path(p(2.05, 1.95))
    boundary.add_cubic_bezier_curve_to(p(2.00, .25), p(3.50, .02), p(4.50, .20))
    boundary.add_cubic_bezier_curve_to(p(5.37, .36), p(5.98, .78), p(6.73, .78))
    edge = DashedVMobject(boundary, num_dashes=17)
    return VGroup(lawn, track, tufts), VGroup(water, ripples), edge


def sink():
    basin = block(2.4, .82, "#A7C2CB", "#E0F1E9", corner=.25).move_to(p(0, -.39))
    bowl = oval(1.86, .48, "#3C7177", "#D6E0DB").move_to(p(0, -.36))
    tap = ArcBetweenPoints(p(-.77, -.19), p(.15, .33), angle=-2.83,
                           color="#D1E6E4", stroke_width=13)
    soap = block(.63, .37, "#E29A5E", CREAM, corner=.13).move_to(p(.93, .29))
    bubbles = VGroup(*(Circle(radius=r, color="#C8EFE4", stroke_width=2).move_to(p(x,y))
                        for x, y, r in [(.76, .59, .11), (1.06, .70, .13), (.91, .94, .085)]))
    return VGroup(basin, bowl, tap, soap, bubbles), bubbles


class S11Walk(SpokenScene):
    def construct(self):
        meadow, pond, boundary = footpath()
        specimens = VGroup(picture(tree, 4.15, p(-3.91, .47)),
                           picture(rock, 1.37, p(-1.01, -1.28)))
        glass = picture(magnifier, 2.30, p(-3.81, .09))
        self.add(table())
        self.at("optional 10")
        self.play(FadeIn(meadow), run_time=.82)
        self.play(FadeIn(specimens, shift=UP * .39), run_time=.71)
        self.at("find 3 living")
        self.play(FadeIn(glass, shift=RIGHT * .32), run_time=.52)
        self.play(glass.animate.move_to(p(-1.21, -1.17)), run_time=2.10)
        self.at("stay on a permitted path")
        self.play(FadeIn(pond), run_time=.83)
        self.play(Create(boundary), run_time=1.08)
        bob(pond[1], amp=.16, speed=2.15)
        self.at("within arms reach")
        close = boxed_label("Stay within arm’s reach", CREAM, size=32).move_to(p(-.62, 3.08))
        close.box.set_fill(DEEP, 1)
        self.play(FadeIn(close, shift=UP * .22), run_time=.56)
        self.at("never leave")
        water = boxed_label("Stay together near water", CREAM, size=32).move_to(p(-.62, 3.08))
        water.box.set_fill(DEEP, 1)
        self.play(swap(close, water), run_time=.63)
        self.at("look without picking")
        self.play(FadeOut(water), glass.animate.move_to(p(-3.47, .28)), run_time=1.23)
        self.at("wash hands")
        wash, bubbles = sink()
        wash.move_to(p(1.43, .49))
        label = T("Wash hands", 34, TEXT, weight=BOLD).move_to(p(-.62, 3.08))
        self.play(FadeIn(wash, shift=UP * .26), run_time=.61)
        bob(bubbles, amp=.16, speed=2.4)
        self.play(FadeIn(label), run_time=.37)
        self.at("check for ticks")
        ticks = T("Check for ticks", 32, TEXT, weight=BOLD).move_to(label)
        self.play(swap(label, ticks), run_time=.64)
        self.finish()


class S12Payoff(SpokenScene):
    def construct(self):
        sorting = three_mats()
        flora, seed, dry, twig, stone = sorted_objects()
        panel, ledger = checklist()
        pad_at = p(-2.14, -1.63)
        notes = pad(pad_at)
        first = T("My rule", 32, TEXT, weight=BOLD).move_to(pad_at + UP * .52)
        updated = T("Rule checked", 32, TEXT, weight=BOLD).move_to(first)
        self.add(table(), sorting, flora, seed, dry, twig, stone)
        self.at("looking closely")
        self.play(Indicate(seed, color=CREAM, scale_factor=1.12),
                  Indicate(dry, color=CREAM, scale_factor=1.08), run_time=1.28)
        self.at("stating a rule")
        self.play(FadeOut(sorting), FadeOut(twig), FadeOut(stone), run_time=.44)
        self.play(flora.animate.scale(1.22).move_to(p(-5.05, .55)),
                  seed.animate.move_to(p(-2.65, 1.45)),
                  dry.animate.move_to(p(-1.46, .65)), run_time=.76)
        self.play(FadeIn(notes, shift=UP * .26), run_time=.48)
        self.play(FadeIn(first), run_time=.48)
        self.at("they test that rule")
        self.play(FadeIn(panel, shift=LEFT * .38), run_time=.63)
        for i in range(4):
            self.play(ledger.reveal(i), run_time=.43)
        self.at("revise it")
        self.play(swap(first, updated), run_time=.68)
        check = mark(True).scale(1.22).move_to(p(-2.14, -2.31))
        self.play(Create(check), run_time=.55)
        self.at("one clue alone")
        self.play(Indicate(ledger.rows[0][2], color=YELLOW, scale_factor=1.46),
                  dry.animate.rotate(.26).move_to(p(-1.31, 1.42)), run_time=1.56)
        self.at("checking every sign together")
        icons = [row[2] for row in ledger.rows]
        self.play(*(Indicate(icon, color=CREAM, scale_factor=1.18) for icon in icons),
                  panel[0].animate.set_stroke(CREAM, width=4.0), run_time=1.36)
        self.finish()


class S13End(EndCard):
    LINE = "No single clue decides life; check the whole list together."
