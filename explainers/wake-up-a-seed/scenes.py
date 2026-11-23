"""A kitchen-counter experiment in two bags."""

from bp_parts import *
from bp_style import EndCard

# Color map: ochre beans, slate pebble, blue water/air, ivory roots and paper,
# green shoots, red safety marks. The earlier film uses the shared house palette.
BEAN = "#BF7952"
BEAN_EDGE = "#F2B183"
STONE = "#8797A8"
PAPER = "#EFE1C7"
DAMP = "#A9D5D7"
COUNTER = "#604638"
WALL = "#252E3C"
PLASTIC = "#426078"
ROOT = "#FFF4D7"
INK = "#334759"
SKIN = "#DCA47D"
LEFT_BAG, RIGHT_BAG = -3.18, 3.18
BEAN_SPOTS = [(-1.2, 0.30), (0, 0.36), (1.2, 0.30), (-0.64, -0.72), (0.64, -0.72)]


def xy(x, y):
    return np.array([x, y, 0.0])


def panel(w, h, fill, edge=None, radius=0.17, opacity=1):
    return RoundedRectangle(
        width=w, height=h, corner_radius=radius, stroke_color=edge or fill,
        stroke_width=2 if edge else 0, fill_color=fill, fill_opacity=opacity,
    )


def curve(start, segments, color, width=5, fill=None):
    path = VMobject(stroke_color=color, stroke_width=width)
    path.start_new_path(xy(*start))
    for a, b, c in segments:
        path.add_cubic_bezier_curve_to(xy(*a), xy(*b), xy(*c))
    if fill:
        path.close_path().set_fill(fill, opacity=1)
    return path


def counter_scene():
    """The same wall, worktop and front edge behind each camera view."""
    wall = Rectangle(width=14.22, height=8, stroke_width=0, fill_color=WALL, fill_opacity=1)
    worktop = Rectangle(width=14.22, height=2.9, stroke_width=0,
                        fill_color=COUNTER, fill_opacity=1).move_to(xy(0, -2.55))
    rim = Rectangle(width=14.22, height=0.24, stroke_width=0,
                    fill_color="#47342D", fill_opacity=1).move_to(xy(0, -3.49))
    return VGroup(wall, worktop, rim).set_z_index(-5)


def seed(x=0, y=0, scale=1, color=BEAN, swell=1):
    shell = curve((-0.99, -0.10), [
        ((-1.03, 0.55), (-0.33, 0.79), (0.34, 0.62)),
        ((1.03, 0.47), (1.13, -0.04), (0.80, -0.38)),
        ((0.55, -0.65), (0.14, -0.51), (-0.09, -0.34)),
        ((-0.28, -0.20), (-0.48, -0.63), (-0.78, -0.45)),
        ((-0.93, -0.36), (-0.98, -0.26), (-0.99, -0.10)),
    ], BEAN_EDGE, 3, fill=color)
    highlight = curve((-0.79, 0.19), [
        ((-0.57, 0.54), (0.00, 0.59), (0.49, 0.42)),
    ], BEAN_EDGE, 3).set_stroke(opacity=0.65)
    scar = Ellipse(width=0.31, height=0.105, color=ROOT, fill_opacity=1, stroke_width=0)
    scar.rotate(-0.33).move_to(xy(0.04, -0.30))
    return VGroup(shell, highlight, scar).scale(scale * swell, about_point=ORIGIN).shift(xy(x, y))


def growth(x, y, size=1, shoot=False, short=False, color=None, swell=1.13):
    """Illustrative paths of the root and shoot from beside the bean scar."""
    if shoot:
        path = curve((0.14, -0.36), [
            ((0.62, -0.50), (1.05, 0.17), (0.89, 0.91)),
            ((0.76, 1.53), (0.30, 1.62), (0.19, 1.15)),
        ], color or GREEN, max(3, 15 * size))
    elif short:
        path = curve((0.12, -0.34), [
            ((0.38, -0.56), (0.27, -0.78), (0.40, -0.96)),
        ], color or ROOT, max(3, 13 * size))
    else:
        path = curve((0.12, -0.34), [
            ((0.40, -0.55), (0.24, -0.87), (0.42, -1.13)),
            ((0.60, -1.40), (0.27, -1.62), (0.42, -1.98)),
        ], color or ROOT, max(3, 13 * size))
    return path.scale(size * swell, about_point=ORIGIN).shift(xy(x, y))


def pebble(x, y, scale=1):
    rock = curve((-0.97, -0.17), [
        ((-0.84, 0.25), (-0.27, 0.58), (0.13, 0.53)),
        ((0.52, 0.58), (0.96, 0.32), (1.02, -0.08)),
        ((1.12, -0.42), (0.56, -0.44), (-0.01, -0.47)),
        ((-0.52, -0.49), (-1.02, -0.45), (-0.97, -0.17)),
    ], "#A9B7C6", 3, fill=STONE)
    glint = curve((-0.72, 0.05), [((-0.44, 0.28), (-0.16, 0.39), (0.17, 0.38))],
                  "#BFCAD6", 3)
    return VGroup(rock, glint).scale(scale).move_to(xy(x, y))


def opening(scale=1):
    stone = pebble(-2.85, -0.70, 1.18 * scale)
    bean = seed(1.56, 0.06, 1.99 * scale)
    return stone, bean


def towel(w=4.05, h=2.35, damp=False):
    base = panel(w, h, DAMP if damp else PAPER)
    folds = VGroup(*[
        Line(xy(-w * 0.40, -h * f), xy(w * 0.40, -h * f),
             color="#729DA3" if damp else "#BAA98C", stroke_opacity=0.6, stroke_width=2)
        for f in (0.36, 0.29)
    ])
    edge = Line(xy(w * 0.42, -h * 0.32), xy(w * 0.42, h * 0.34),
                color="#8AB6BD" if damp else "#BDAE96", stroke_width=2)
    return VGroup(base, folds, edge)


def zipper(x, y, gap):
    return VGroup(*[
        Line(xy(x - 2.02, y + dy), xy(x + end, y + dy), color=BLUE, stroke_width=3)
        for dy, end in [(0.04, 2.02 - gap), (-0.06, 2.02 - gap)]
    ], Dot(xy(x + 2.02 - gap, y + 0.01), radius=0.09, color=BLUE))


def bag(x=0, *, damp=False, filled=True, contents=True, gap=0, stage=0):
    """Keep the bag film, towel, zipper and seeds in consistent registration."""
    film = panel(4.7, 4.1, PLASTIC, "#9CC2D0", radius=0.28, opacity=0.96)
    film.move_to(xy(x, -0.1))
    glint = Line(xy(x - 2.07, 1.29), xy(x - 2.07, -1.73),
                 stroke_width=3, color="#91B8CE", stroke_opacity=0.7)
    frame = VGroup(film, glint)
    zipline = zipper(x, 1.53, gap)
    cloth = towel(damp=damp).move_to(xy(x, -0.52))
    beans = VGroup()
    for i, (dx, dy) in enumerate(BEAN_SPOTS):
        sprout = i < 4 and stage > 0
        parts = [seed(x + dx, dy, 0.36, swell=1.13 if sprout else 1)]
        if sprout:
            parts.append(growth(x + dx, dy, 0.36, short=stage == 1))
            if stage == 2:
                parts.append(growth(x + dx, dy, 0.36, shoot=True))
        beans.add(VGroup(*parts))
    display = VGroup(frame, zipline)
    if contents:
        display.add(cloth)
    if filled:
        display.add(beans)
    return display, cloth, beans, zipline


def bag_label(x, text, wet=False):
    return boxed_label(text, BLUE if wet else TEXT, size=30, fill_opacity=0.24).move_to(xy(x, 2.58))


def bag_pair(left_stage=0, right_stage=0, gap=3.55, right_wet=False):
    left = bag(LEFT_BAG, damp=True, gap=gap, stage=left_stage)
    right = bag(RIGHT_BAG, damp=right_wet, gap=gap, stage=right_stage)
    labels = VGroup(bag_label(LEFT_BAG, "water", True),
                    bag_label(RIGHT_BAG, "water added" if right_wet else "no water", right_wet))
    return left, right, labels


def spoon(x=0, y=0, s=1):
    bowl = Ellipse(width=0.77, height=0.47, color=TEXT, stroke_width=2,
                   fill_color=STONE, fill_opacity=1)
    inset = Ellipse(width=0.54, height=0.29, color="#5C728B", stroke_width=0, fill_opacity=1)
    handle = panel(1.27, 0.15, STONE, TEXT, radius=0.07).move_to(RIGHT * 0.88)
    return VGroup(handle, bowl, inset).scale(s, about_point=ORIGIN).shift(xy(x, y))


def drop(x, y, s=1):
    d = curve((0, 0.22), [
        ((0.06, 0.11), (0.16, -0.02), (0.13, -0.10)),
        ((0.09, -0.23), (-0.09, -0.23), (-0.13, -0.10)),
        ((-0.16, -0.02), (-0.06, 0.11), (0, 0.22)),
    ], BLUE, 1, fill=BLUE)
    return d.scale(s).move_to(xy(x, y))


def water_spoon(scene, x, cloth=None, duration=2.1, from_y=1.63, to_y=-0.45):
    tool = spoon(x + 0.23, from_y, 0.87)
    scene.play(FadeIn(tool, shift=LEFT * 0.48), run_time=0.42)
    scene.play(Rotate(tool, 0.29, about_point=xy(x + 0.23, from_y)),
               run_time=0.32)
    drops = VGroup(*[drop(x + i * 0.21 - 0.21, from_y - 0.39 + i * 0.10, 0.7)
                     for i in range(3)])
    scene.add(drops)
    scene.play(drops.animate.shift(DOWN * (from_y - to_y - 0.39)),
               run_time=duration - 1.04, rate_func=rate_functions.ease_in_quad)
    finish = [FadeOut(drops), FadeOut(tool, shift=UP * 0.24)]
    if cloth is not None:
        finish.append(Transform(cloth, towel(damp=True).move_to(cloth)))
    scene.play(*finish, run_time=0.30)


def cup():
    glass = Polygon(xy(-0.62, 0.82), xy(0.62, 0.82), xy(0.44, -0.82), xy(-0.44, -0.82),
                    color="#A6C7D6", stroke_width=3, fill_color=PLASTIC, fill_opacity=1)
    water = Polygon(xy(-0.54, 0.27), xy(0.54, 0.27), xy(0.43, -0.74), xy(-0.43, -0.74),
                    color=BLUE, stroke_width=1, fill_color=BLUE, fill_opacity=0.75)
    return VGroup(glass, water)


def tape():
    roll = Circle(0.42, color=PAPER, stroke_width=3, fill_color=GOLD, fill_opacity=1)
    hole = Circle(0.20, color=PAPER, stroke_width=2, fill_color=WALL, fill_opacity=1)
    tab = Polygon(xy(0.25, -0.19), xy(0.82, -0.25), xy(0.84, -0.52), xy(0.32, -0.47),
                  color=GOLD, fill_opacity=1, stroke_width=2)
    return VGroup(tab, roll, hole)


def marker():
    barrel = panel(1.48, 0.30, TEAL, "#7BCAD2", radius=0.08)
    cap = panel(0.46, 0.34, INK, "#6D90A5", radius=0.07).move_to(xy(-0.56, 0))
    return VGroup(barrel, cap).rotate(-0.39)


def pencil():
    body = panel(1.33, 0.17, GOLD, radius=0.06)
    tip = Polygon(xy(-0.65, 0.085), xy(-0.65, -0.085), xy(-0.94, 0),
                  color=PAPER, fill_opacity=1, stroke_width=0)
    point = Polygon(xy(-0.84, 0.028), xy(-0.84, -0.028), xy(-0.94, 0),
                    color=INK, fill_opacity=1, stroke_width=0)
    return VGroup(body, tip, point).rotate(0.50)


def calendar(x, y, columns=7, s=1):
    page = panel(columns * 0.49 + 0.42, 0.85, "#425263", STONE)
    header = Line(page.get_left() + RIGHT * 0.17 + UP * 0.20,
                  page.get_right() + LEFT * 0.17 + UP * 0.20, color=STONE, stroke_width=2)
    cells = VGroup(*[
        panel(0.37, 0.29, "#65788B", radius=0.05).move_to(xy((i - (columns - 1) / 2) * 0.49, -0.10))
        for i in range(columns)
    ])
    return VGroup(page, header, cells).scale(s).move_to(xy(x, y)), cells


def tick_cells(scene, cells, duration):
    scene.play(LaggedStart(*[cell.animate.set_fill(GOLD) for cell in cells], lag_ratio=0.62),
               run_time=duration)


def eye():
    outline = curve((-0.65, 0), [
        ((-0.27, 0.49), (0.27, 0.49), (0.65, 0)),
        ((0.27, -0.47), (-0.27, -0.47), (-0.65, 0)),
    ], TEXT, 3)
    return VGroup(outline, Circle(0.18, color=BLUE, fill_opacity=1, stroke_width=1))


def cross(mob, radius=0.70):
    return Cross(mob, stroke_color=RED, stroke_width=8, scale_factor=1).scale_to_fit_width(2 * radius)


def hand(x=0, y=0, scale=1, flip=False):
    palm = curve((-0.98, -0.29), [
        ((-0.60, -0.31), (-0.42, -0.33), (-0.28, -0.39)),
        ((0.04, -0.54), (0.49, -0.42), (0.78, -0.12)),
        ((1.02, 0.12), (1.01, 0.37), (0.81, 0.29)),
        ((0.64, 0.22), (0.41, 0.00), (0.18, 0.03)),
        ((0.34, 0.18), (0.39, 0.35), (0.21, 0.39)),
        ((-0.07, 0.43), (-0.23, 0.13), (-0.47, 0.11)),
        ((-0.60, 0.08), (-0.81, 0.14), (-0.98, 0.16)),
    ], "#F0BE9D", 2, fill=SKIN)
    cuff = panel(0.40, 0.57, TEAL, radius=0.08).move_to(xy(-0.91, -0.07))
    obj = VGroup(palm, cuff)
    if flip:
        obj.flip(UP)
    return obj.scale(scale).move_to(xy(x, y))


def person(x, y, scale, shirt):
    torso = panel(1.9, 1.65, shirt, radius=0.48).move_to(xy(0, -0.48))
    head = Circle(0.57, fill_color=SKIN, fill_opacity=1, stroke_width=0).move_to(xy(0, 0.72))
    hair = Arc(radius=0.51, start_angle=0.27, angle=2.56, arc_center=xy(0, 0.77),
              color="#593D32", stroke_width=11)
    eyes = VGroup(Dot(xy(-0.18, 0.71), radius=0.035, color=WALL), Dot(xy(0.18, 0.71), radius=0.035, color=WALL))
    smile = Arc(radius=0.18, start_angle=3.74, angle=1.94, arc_center=xy(0, 0.61),
                color=INK, stroke_width=2)
    return VGroup(torso, head, hair, eyes, smile).scale(scale).move_to(xy(x, y))


def note_page(x, y, show_guess=True, s=1):
    page = panel(2.95, 2.62, PAPER, "#F8EACC", radius=0.11)
    # Pencil drawing of a bean and the child's predicted downward root.
    sketch = VGroup(
        curve((-0.76, 0.32), [
            ((-0.74, 0.76), (0.18, 0.87), (0.59, 0.50)),
            ((0.93, 0.13), (0.49, -0.15), (0.06, 0.02)),
            ((-0.21, -0.28), (-0.84, -0.12), (-0.76, 0.32)),
        ], INK, 4),
        growth(-0.05, 0.37, 0.54, color=INK, swell=1),
    )
    group = VGroup(page, sketch) if show_guess else VGroup(page)
    group.scale(s, about_point=ORIGIN).shift(xy(x, y))
    if not show_guess:
        sketch.scale(s, about_point=ORIGIN).shift(xy(x, y))
    return group, sketch


def folder():
    tab = panel(1.34, 0.47, GOLD, radius=0.12).move_to(xy(-0.88, 0.78))
    back = panel(3.36, 1.76, GOLD)
    front = panel(3.36, 1.36, "#A87830", GOLD).move_to(xy(0, -0.22))
    return VGroup(tab, back, front)


def bin_parts(x, y, s=1):
    base = Polygon(xy(-0.85, 0.5), xy(0.85, 0.5), xy(0.65, -1.1), xy(-0.65, -1.1),
                   color=STONE, fill_color=PLASTIC, fill_opacity=1, stroke_width=3)
    stripes = VGroup(*[Line(xy(a, 0.22), xy(a * 0.80, -0.83), color=STONE, stroke_width=2)
                       for a in (-0.40, 0, 0.40)])
    lid = VGroup(panel(1.95, 0.22, STONE, radius=0.09),
                 panel(0.55, 0.17, STONE, radius=0.06).shift(UP * 0.16)).move_to(xy(0, 0.65))
    return (VGroup(base, stripes).scale(s, about_point=ORIGIN).shift(xy(x, y)),
            lid.scale(s, about_point=ORIGIN).shift(xy(x, y)))


def top_label(text, color=TEXT, size=34, x=0, y=3.10):
    return fit_text(text, max_w=11.1, color=color, size=size, min_size=28).move_to(xy(x, y))


def question(text, x=0, y=2.88, w=10, size=42):
    return question_card(text, y=y, size=size, max_w=w).move_to(xy(x, y))


class S01Hook(SpokenScene, TitleCard):
    TITLE = "Wake Up a Seed: Parent Guide"
    LESSON = "Wake Up a Seed"

    def construct(self):
        stone, bean = opening(0.67)
        pair = VGroup(stone, bean)
        self.add(counter_scene(), pair)
        self.at("a dry bean")
        closer_stone, closer_bean = opening(0.85)
        self.play(Transform(stone, closer_stone), Transform(bean, closer_bean),
                  rate_func=linear, run_time=2.85)
        self.at("a little pebble")
        final_stone, final_bean = opening()
        self.play(Transform(stone, final_stone), Transform(bean, final_bean),
                  rate_func=linear, run_time=4.32)
        self.at("so is it alive", lead=0)
        q = question("Is this bean alive?", size=54)
        self.play(FadeIn(q, shift=UP * 0.12), run_time=0.52)
        self.at("two bags")
        left = bag(-1.00, damp=True, filled=False)[0]
        right = bag(1.00, filled=False)[0]
        kit = VGroup(left, right).arrange(RIGHT, buff=0.32).scale(0.37).move_to(xy(4.63, -1.92))
        self.play(FadeIn(kit, shift=UP * 0.36), run_time=1.35)
        self.play(FadeOut(kit), FadeOut(q), run_time=0.55)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Wake Up a Seed: Parent Guide"
    LESSON = "Wake Up a Seed"

    def construct(self):
        title = T(self.LESSON, 62, font=TITLE_FONT).move_to(xy(0, 2.33))
        self.add(counter_scene(), *opening())
        self.play(FadeIn(title, shift=UP * 0.15), run_time=0.42)
        self.wait(1.58)


class S03Payoff(SpokenScene):
    def construct(self):
        bean = opening()[1]
        self.add(counter_scene(), bean)
        cal, days = calendar(0, -2.65, columns=14, s=1.32)
        setup = top_label("Setup · about 20 minutes")
        self.at("setup takes")
        self.play(FadeIn(cal, shift=UP * 0.35), FadeIn(setup), run_time=0.75)
        self.at("then two or three")
        daily = top_label("2–3 minutes a day · 1–2 weeks")
        self.play(swap(setup, daily, 0.45), run_time=0.45)
        tick_cells(self, days, 2.8)
        self.at("making a guess")
        items = [
            VGroup(pencil().scale(0.83), T("Guess, then check", 29, GOLD)).arrange(RIGHT, buff=0.22),
            VGroup(calendar(0, 0, columns=2, s=0.75)[0], T("Wait for it", 29, GOLD)).arrange(RIGHT, buff=0.22),
            VGroup(eye().scale(0.73), T("Look closely", 29, GOLD)).arrange(RIGHT, buff=0.22),
        ]
        for item, y in zip(items, [1.23, 0.15, -0.94]):
            item.align_to(xy(-6.10, y), LEFT).set_y(y)
        self.play(FadeOut(daily), FadeIn(items[0], shift=RIGHT * 0.2), run_time=0.56)
        self.at("waiting for a slow")
        self.play(FadeIn(items[1], shift=RIGHT * 0.2), run_time=0.60)
        self.at("and checking it")
        self.play(FadeIn(items[2], shift=RIGHT * 0.2), run_time=0.60)
        self.at("and they find out")
        resting = top_label("Alive and resting", color=GOLD, size=42)
        self.play(FadeOut(VGroup(*items)), FadeIn(resting), run_time=0.53)
        self.play(bean.animate.scale(1.08), run_time=2.4, rate_func=smooth)
        self.finish()


class S04Gather(SpokenScene):
    def construct(self):
        self.add(counter_scene())
        heap = VGroup(*[
            seed((i % 5 - 2) * 0.77 + 0.16 * (i // 5), (i // 5 - 1) * 0.58,
                 0.34, color=[BEAN, "#A5694B", "#C99871"][i % 3]).rotate((i % 4 - 1) * 0.39)
            for i in range(15)
        ])
        self.at("you need")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.55) for b in heap], lag_ratio=0.12),
                  run_time=2.3)
        self.at("the grocery store")
        groceries = top_label("Grocery beans · 12–20", color=GOLD)
        self.play(FadeIn(groceries), run_time=0.5)
        self.at("like lima")
        examples = [
            (seed(-2.9, 1.51, 0.63, color="#D9B492"), T("Lima", 28)),
            (seed(0, 1.51, 0.63, color=BEAN), T("Pinto", 28)),
            (seed(2.9, 1.51, 0.63, color="#50434B"), T("Black", 28)),
        ]
        options = VGroup(*[VGroup(s, t.next_to(s, UP, buff=0.13)) for s, t in examples])
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.18) for g in options], lag_ratio=0.7),
                  run_time=2.60)
        self.at("skip red kidney")
        red = seed(3.50, -0.20, 0.72, color="#9F434A")
        packet = panel(1.1, 1.36, "#58775C", GREEN).move_to(xy(-3.64, -0.01))
        packet_mark = seed(-3.64, -0.06, 0.36, color="#C0CE8D")
        packet_group = VGroup(packet, packet_mark, cross(packet))
        warn = VGroup(T("Skip red kidney beans", 28, "#FFB4A9").move_to(xy(3.50, -1.38)),
                      T("Not garden seed packets", 28, "#FFB4A9").move_to(xy(-3.64, -1.38)))
        self.play(FadeOut(options), run_time=0.24)
        red_group = VGroup(red, cross(red))
        self.play(FadeIn(red_group), FadeIn(packet_group), FadeIn(warn), run_time=0.42)
        self.at("add two clear")
        self.play(FadeOut(VGroup(red_group, packet_group, warn, groceries)),
                  heap.animate.scale(0.49).move_to(xy(-5.3, -0.52)), run_time=0.30)
        bags = VGroup(*[bag(contents=False, filled=False)[0].scale(0.40).shift(xy(x, y))
                        for x, y in [(-3.13, -0.42), (-2.90, -0.19)]])
        self.play(FadeIn(bags, shift=RIGHT * 0.50), run_time=0.80)
        self.at("two paper towels")
        towels = VGroup(towel(1.35, 1.12).shift(xy(-0.80, -0.45)),
                        towel(1.35, 1.12).shift(xy(-0.64, -0.26)))
        self.play(FadeIn(towels, shift=RIGHT * 0.40), run_time=0.60)
        self.at("a cup of water")
        water = cup().move_to(xy(1.17, -0.37))
        self.play(FadeIn(water, shift=RIGHT * 0.45), run_time=0.43)
        self.at("a spoon")
        tool = spoon(2.05, -1.17, 0.76).rotate(0.43)
        self.play(FadeIn(tool, shift=RIGHT * 0.32), run_time=0.42)
        self.at("tape and a marker")
        self.play(FadeIn(tape().move_to(xy(3.63, -0.53)), shift=RIGHT * 0.35),
                  FadeIn(marker().move_to(xy(5.31, -0.49)), shift=RIGHT * 0.57), run_time=0.72)
        self.finish()


class S14SafetyBeans(SpokenScene):
    def construct(self):
        adult = person(-3.95, 0.25, 1.35, TEAL)
        child = person(3.66, -0.15, 1.05, "#B57654")
        kit = bag(contents=False, filled=False)[0].scale(0.45).move_to(xy(1.12, -1.63))
        beans = VGroup(*[seed(-1.65 + (i % 3) * 0.57, -1.28 - (i // 3) * 0.4, 0.25)
                         for i in range(6)])
        self.add(counter_scene(), adult, child, kit, beans)
        self.at("check for bean")
        allergy = top_label("Check allergies", color=GOLD, size=42)
        self.play(FadeIn(allergy), run_time=0.48)
        types = top_label("Bean · pea · peanut · soy", size=29, y=2.45)
        self.play(FadeIn(types, shift=UP * 0.28), run_time=0.65)
        ring = RoundedRectangle(width=2.2, height=1.40, corner_radius=0.33, color=GOLD,
                                stroke_width=3).move_to(beans)
        self.play(Create(ring), run_time=1.25)
        self.at("keep beans and bags")
        self.play(FadeOut(types), FadeOut(ring), run_time=0.24)
        away = top_label("Keep away from under 4s", color=GOLD, size=40)
        self.play(swap(allergy, away, 0.64), run_time=0.64)
        self.play(VGroup(beans, kit).animate.shift(LEFT * 0.72), run_time=1.35)
        self.at("stay with your child")
        self.play(FadeOut(away), run_time=0.27)
        reach = hand(-2.12, -0.72, 0.75)
        self.play(FadeIn(reach, shift=RIGHT * 0.28), run_time=0.59)
        self.at("count the beans out")
        count_order = (5, 2, 4, 1, 3, 0)
        self.play(LaggedStart(*[
            MoveAlongPath(bean, CubicBezier(
                bean.get_center(), xy(bean.get_x(), -2.90),
                xy(bean.get_x(), -2.96), xy(0.65 - i * 0.56, -2.96),
            ))
            for i, bean in enumerate(beans[j] for j in count_order)
        ], lag_ratio=0.38), run_time=1.9)
        self.at("if a child is choking")
        call = top_label("Choking? Call 911", RED, 54, y=3.0)
        self.play(FadeOut(reach), FadeIn(call, shift=UP * 0.12), run_time=0.56)
        self.finish()


class S15SafetyMold(SpokenScene):
    def construct(self):
        self.add(counter_scene())
        bean = seed(-2.78, 0.03, 1.8)
        lips = curve((-0.98, 0.02), [
            ((-0.53, 0.55), (-0.15, 0.51), (0.01, 0.39)),
            ((0.28, 0.52), (0.72, 0.32), (0.98, 0.02)),
            ((0.50, -0.59), (-0.54, -0.64), (-0.98, 0.02)),
        ], "#EFAB9F", 4, fill="#AE6162")
        mouth = VGroup(lips, Line(LEFT * 0.79, RIGHT * 0.79, color="#783F4A", stroke_width=5))
        mouth.scale(1.3).move_to(xy(2.5, 0.0))
        self.add(bean)
        self.at("raw beans contain")
        self.play(bean.animate.scale(1.11), run_time=2.6)
        self.at("never taste")
        crossed = VGroup(mouth, cross(mouth, 1.30))
        self.play(FadeIn(crossed, shift=LEFT * 0.19), run_time=0.59)
        self.at("if a child chews")
        phone = VGroup(top_label("Poison Control", RED, 36, y=3.24),
                       top_label("1-800-222-1222", TEXT, 48, y=2.50))
        self.play(FadeIn(phone, shift=DOWN * 0.13), run_time=0.66)
        self.at("look through the plastic")
        self.play(FadeOut(crossed), FadeOut(bean), FadeOut(phone), run_time=0.42)
        mold_bag = bag(2.61, damp=True, stage=1, gap=0.52)[0]
        fuzz = VGroup(*[
            Line(xy(0, 0), xy(0.25 * np.cos(a), 0.25 * np.sin(a)), color=ROOT, stroke_width=2.4)
            for a in np.linspace(0, TAU, 13, endpoint=False)
        ], *[Dot(xy(dx, dy), radius=0.08, color="#788A6F") for dx, dy in [(0, 0), (0.09, -0.02), (-0.03, 0.09)]])
        fuzz.move_to(xy(2.61, 0.38))
        mold_bag.add(fuzz)
        self.play(FadeIn(mold_bag, shift=UP * 0.22), run_time=1.25)
        self.at("if you see fuzz")
        focus = Circle(radius=0.48, color=GOLD, stroke_width=4).move_to(fuzz)
        self.play(mold_bag.animate.scale(1.12, about_point=xy(2.61, 0.08)), Create(focus),
                  run_time=0.70)
        mold_rule = question("Follow the guide’s\nmold rule", x=-3.15, y=1.06, w=5.5, size=38)
        self.at("follow the guide's")
        self.play(FadeIn(mold_rule), run_time=0.59)
        self.at("have an adult")
        adult = person(-3.08, -1.19, 1.03, TEAL)
        fingers = hand(1.38, 1.72, 0.73)
        self.play(FadeOut(focus), FadeIn(adult, shift=UP * 0.15), run_time=0.60)
        self.play(FadeIn(fingers, shift=RIGHT * 0.26), run_time=0.53)
        self.at("seal it")
        zipline = mold_bag[1]
        closed = zipper(2.61, 1.53, 0).scale(1.12, about_point=xy(2.61, 0.08))
        self.play(Transform(zipline, closed), fingers.animate.shift(RIGHT * 2.35), run_time=0.55)
        self.at("throw it away")
        base, lid = bin_parts(2.70, -1.85, 1.32)
        self.play(FadeIn(base), FadeOut(fingers),
                  mold_bag.animate.scale(0.37).move_to(xy(2.70, 0.41)), run_time=0.52)
        self.play(mold_bag.animate.scale(0.70).move_to(xy(2.70, -1.92)), run_time=0.44)
        self.play(FadeOut(mold_bag), FadeIn(lid), run_time=0.28)
        self.at("never open or sniff")
        self.play(FadeOut(mold_rule), run_time=0.22)
        self.play(FadeIn(top_label("Keep the bag closed", RED, 41, y=2.86)), run_time=0.46)
        self.finish()


class S05LookFirst(SpokenScene):
    def construct(self):
        palms = VGroup(hand(-2.03, -0.35, 1.67), hand(2.03, -0.35, 1.67, flip=True))
        self.add(counter_scene(), palms)
        self.at("start by handing")
        beans = VGroup(seed(-1.86, 0.58, 0.69), seed(1.86, 0.58, 0.69))
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.55) for b in beans], lag_ratio=0.55),
                  run_time=2.04)
        self.at("ask is this alive")
        prompt = question("Is this alive?\nHow could we find out?", y=2.58, w=10.4, size=40)
        self.play(FadeIn(prompt, shift=UP * 0.12), run_time=0.63)
        self.at("write down the answer")
        pad = panel(2.65, 1.08, PAPER).move_to(xy(-2.53, -2.45))
        line = curve((-3.51, -2.46), [
            ((-3.30, -2.03), (-3.24, -2.64), (-3.04, -2.35)),
            ((-2.93, -2.15), (-2.76, -2.65), (-2.57, -2.35)),
            ((-2.39, -2.11), (-2.23, -2.66), (-1.62, -2.39)),
        ], INK, 3.2)
        self.play(FadeIn(pad, shift=RIGHT * 0.4), run_time=0.48)
        self.play(Create(line), run_time=1.20)
        self.finish()


class S06Bags(SpokenScene):
    def construct(self):
        self.add(counter_scene())
        left = bag(LEFT_BAG, contents=False, filled=False, gap=3.55)
        right = bag(RIGHT_BAG, contents=False, filled=False, gap=3.55)
        self.add(left[0], right[0])
        self.at("fold a towel")
        cloths = [left[1], right[1]]
        unfurled = [
            towel(4.05, 2.95).move_to(xy(x, -0.54))
            for x in (LEFT_BAG, RIGHT_BAG)
        ]
        self.play(*[FadeIn(m, shift=DOWN * 0.7) for m in unfurled], run_time=0.82)
        self.play(*[ReplacementTransform(m, c) for m, c in zip(unfurled, cloths)], run_time=1.45)
        self.at("wet one with a spoon")
        water_spoon(self, LEFT_BAG, cloths[0], duration=2.8, from_y=1.30)
        self.at("leave the other towel")
        target = SurroundingRectangle(cloths[1], color=GOLD, corner_radius=0.20, buff=0.14,
                                      stroke_width=7)
        self.play(FadeIn(target), run_time=0.36)
        self.play(Uncreate(target), run_time=1.0)
        self.at("lay four to six")
        self.play(LaggedStart(*[
            AnimationGroup(FadeIn(a, shift=DOWN * 0.40), FadeIn(b, shift=DOWN * 0.40))
            for a, b in zip(left[2], right[2])
        ], lag_ratio=0.42), run_time=2.67)
        self.at("label the bags")
        wet = bag_label(LEFT_BAG, "water", True)
        dry = bag_label(RIGHT_BAG, "no water")
        self.play(FadeIn(wet, shift=DOWN * 0.18), run_time=0.57)
        self.play(FadeIn(dry, shift=DOWN * 0.18), run_time=0.56)
        self.finish()


class S07ChildGuess(SpokenScene):
    def construct(self):
        left, right, labels = bag_pair()
        self.add(counter_scene(), left[0], right[0], labels)
        self.at("before you set")
        outline = SurroundingRectangle(VGroup(left[0], right[0]), buff=0.16,
                                       color=GOLD, corner_radius=0.29, stroke_width=2)
        self.play(Create(outline), run_time=1.55)
        self.at("what do you think")
        prompt = question("What will happen in each bag?", y=-3.10, size=37)
        self.play(FadeOut(outline), FadeIn(prompt), run_time=0.46)
        self.at("have your child draw")
        page, sketch = note_page(0, 0.10, show_guess=False, s=0.92)
        self.play(FadeOut(prompt), FadeIn(page, shift=UP * 0.26), run_time=0.39)
        self.play(Create(sketch), run_time=1.03)
        self.at("save it for later")
        cover = folder().move_to(xy(0, -1.93))
        cover[-1].set_z_index(2)
        self.play(FadeIn(cover), run_time=0.27)
        self.play(VGroup(page, sketch).animate.scale(0.75).shift(DOWN * 1.75),
                  run_time=0.68)
        self.finish()


def window():
    frame = panel(12.7, 6.08, "#879EAB", "#ABC5D0", radius=0.14).move_to(UP * 0.25)
    panes = VGroup(*[
        panel(5.93, 5.57, "#37546D", radius=0.10).move_to(xy(x, 0.25))
        for x in (LEFT_BAG, RIGHT_BAG)
    ])
    sill = panel(12.90, 0.21, STONE, radius=0.06).move_to(xy(0, -2.80))
    return VGroup(frame, panes, sill).set_z_index(-2)


class S08Place(SpokenScene):
    def construct(self):
        left, right, labels = bag_pair()
        self.add(counter_scene(), left[0], right[0], labels)
        self.at("leave each bag open")
        self.play(*[Transform(parts[3], zipper(x, 1.53, 0.78))
                    for parts, x in [(left, LEFT_BAG), (right, RIGHT_BAG)]], run_time=1.17)
        air = VGroup(*[
            Arrow(xy(x + 1.62, 1.89), xy(x + 1.62, 0.86), buff=0,
                  color=BLUE, stroke_width=4, max_tip_length_to_length_ratio=0.25)
            for x in (LEFT_BAG, RIGHT_BAG)
        ])
        self.at("a finger's width")
        detail = panel(4.45, 1.80, PLASTIC, STONE).move_to(xy(0, 0.96))
        detail_zip = zipper(0, 0.78, 0.78).scale(0.91, about_point=xy(0, 0.78))
        finger = panel(0.55, 0.71, SKIN, "#F0BE9D", radius=0.24).move_to(xy(1.50, 1.22))
        inset = VGroup(detail, detail_zip, finger)
        self.play(FadeIn(inset), run_time=0.37)
        self.play(finger.animate.shift(DOWN * 0.27), run_time=0.52)
        self.play(FadeOut(inset), *[GrowArrow(a) for a in air], run_time=0.44)
        self.play(FadeOut(air), run_time=0.33)
        self.at("tape both to a bright")
        win = window()
        tape_tabs = VGroup(*[
            panel(0.89, 0.24, GOLD, radius=0.05).rotate(-0.12).move_to(xy(x, 1.97))
            for x in (LEFT_BAG, RIGHT_BAG)
        ])
        self.play(FadeIn(win), run_time=0.83)
        self.play(LaggedStart(*[FadeIn(t) for t in tape_tabs], lag_ratio=0.57),
                  run_time=0.98)
        self.at("or lay them")
        self.play(FadeOut(win), FadeOut(tape_tabs), run_time=0.84)
        self.at("check both bags daily")
        cal, cells = calendar(0, -2.95, columns=5)
        self.play(FadeIn(cal, shift=UP * 0.17), run_time=0.40)
        tick_cells(self, cells, 1.65)
        self.at("add a few drops")
        self.play(left[1][0].animate.set_fill("#C5DAD5"), run_time=0.42)
        water_spoon(self, LEFT_BAG, cloth=left[1], duration=2.1, from_y=1.33)
        self.finish()


PREDICTION = "What comes out first?\nWhich way?"
PREDICT_CARD = {"y": 0.68, "left": -6.02, "size": 40, "max_w": 5.15}


def predict_picture(swell=1.15, direction=True):
    cloth = towel(5.65, 4.35, damp=True).move_to(xy(3.33, -0.23)).rotate(-0.07)
    damp_bean = seed(3.05, 0.14, 1.62, swell=swell)
    arrows = VGroup(
        Arrow(xy(5.21, 0.48), xy(5.21, 1.55), buff=0, color=INK, stroke_width=7),
        Arrow(xy(5.21, -0.22), xy(5.21, -1.29), buff=0, color=INK, stroke_width=7),
    )
    picture = VGroup(counter_scene(), cloth, damp_bean)
    if direction:
        picture.add(arrows)
    return picture, damp_bean, arrows


class S09PredictQuestion(SpokenScene):
    def construct(self):
        picture, bean, arrows = predict_picture(swell=0.88, direction=False)
        self.add(picture)
        self.at("here is a question")
        self.play(FadeIn(question_card(PREDICTION, **PREDICT_CARD)), run_time=0.66)
        self.at("when the damp bean")
        self.play(Transform(bean, predict_picture(direction=False)[1]),
                  run_time=3.8, rate_func=linear)
        self.at("and which way")
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.6), run_time=0.94)
        self.finish()


class S10PredictPause(PredictPause):
    QUESTION = PREDICTION
    CARD = PREDICT_CARD
    RING_AT = (-3.5, -0.79, 0)
    SECONDS = 4.5

    def backdrop(self):
        return predict_picture()[0]

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        ring, run = countdown(self.SECONDS, center=self.RING_AT, radius=0.69)
        self.add(ring)
        self.play(run)


def growth_closeup(zoom, swelling, root_length, shoot_length):
    """Draw the magnified germination sequence from one anchored seed."""
    x, y, size = -2.68, 0.39, 1.14
    swell = swelling.get_value()
    cloth = towel(5.72, 4.87, damp=True).move_to(xy(x, 0.15))
    cloth[0].set_fill("#507F85")
    bean = seed(x, y, size, swell=swell)
    picture = VGroup(cloth, bean)
    for length, is_shoot in [(root_length, False), (shoot_length, True)]:
        fraction = length.get_value()
        full = growth(x, y, size, shoot=is_shoot, swell=swell)
        sprout = full.copy().pointwise_become_partial(full, 0, max(0.001, fraction))
        sprout.set_stroke(opacity=1 if fraction > 0 else 0)
        picture.add(sprout)
    return picture.scale(zoom.get_value(), about_point=xy(x, 0.15))


class S11Root(SpokenScene):
    def construct(self):
        left, right, labels = bag_pair(gap=0.78)
        self.add(counter_scene(), left[0], right[0], labels)
        self.at("in a warm room")
        warm = top_label("Warm room", size=29, x=0, y=3.35)
        cal, cells = calendar(0, -3.10, columns=7, s=1.17)
        self.play(FadeIn(warm), FadeIn(cal, shift=UP * 0.18), run_time=0.53)
        self.at("most beans swell")
        zoom, swelling, root_length, shoot_length = [ValueTracker(v) for v in (0.82, 1, 0, 0)]
        closeup = always_redraw(lambda: growth_closeup(zoom, swelling, root_length, shoot_length))
        self.play(FadeOut(labels[0]), run_time=0.24)
        self.play(FadeOut(left[0]), run_time=0.28)
        self.add(closeup)
        self.play(zoom.animate.set_value(0.94), swelling.animate.set_value(1.16),
                  cells[0].animate.set_fill(GOLD), run_time=1.64)
        self.at("a white root")
        self.play(root_length.animate.set_value(0.84), zoom.animate.set_value(1.04),
                  tick_animation(cells[1:5]), run_time=3.82, rate_func=linear)
        self.at("the curved shoot")
        self.play(tick_animation(cells[5:]), root_length.animate.set_value(1),
                  shoot_length.animate.set_value(1), zoom.animate.set_value(0.99),
                  run_time=3.72, rate_func=linear)
        self.at("the dry beans")
        grown = bag(LEFT_BAG, damp=True, stage=2, gap=0.78)[0]
        closeup.clear_updaters()
        self.play(FadeOut(closeup), FadeIn(grown), FadeOut(warm), FadeOut(cal), run_time=0.62)
        self.play(FadeIn(labels[0]), run_time=0.32)
        self.finish()


def tick_animation(cells):
    return LaggedStart(*[c.animate.set_fill(GOLD) for c in cells], lag_ratio=0.43)


class S12WetDry(SpokenScene):
    def construct(self):
        left, right, labels = bag_pair(left_stage=2, gap=0.78)
        self.add(counter_scene(), left[0], right[0], labels)
        self.at("after about a week")
        cal, cells = calendar(0, -2.99, columns=7)
        self.play(FadeIn(cal), run_time=0.49)
        self.at("have your child predict")
        page, _ = note_page(-0.18, -0.37, s=0.78)
        self.play(FadeIn(page, shift=RIGHT * 0.42), run_time=0.75)
        self.play(tick_animation(cells[:3]), run_time=1.99)
        self.at("dampen that towel")
        self.play(FadeOut(page), run_time=0.24)
        water_spoon(self, RIGHT_BAG, cloth=right[1], duration=1.43, from_y=1.30)
        updated = bag_label(RIGHT_BAG, "water added", True)
        self.play(swap(labels[1], updated, 0.44), run_time=0.44)
        self.play(tick_animation(cells[3:]), run_time=0.82)
        self.at("most of those beans")
        new_beans = bag(RIGHT_BAG, damp=True, stage=1, gap=0.78)[2]
        self.play(LaggedStart(*[
            AnimationGroup(Transform(before[0], after[0]), Create(after[1]))
            for before, after in zip(right[2][:4], new_beans[:4])
        ], lag_ratio=0.37), run_time=1.95)
        # Let the viewer inspect the roots on the bag that has just received water.
        sprouted = VGroup(right[0], *[b[1] for b in new_beans[:4]])
        self.play(sprouted.animate.scale(1.18, about_point=xy(RIGHT_BAG, 0.28)),
                  updated.animate.shift(UP * 0.28),
                  cal.animate.shift(LEFT * 0.42 + DOWN * 0.24),
                  run_time=1.49, rate_func=linear)
        self.finish()


class S13Debrief(SpokenScene):
    def construct(self):
        left, right, labels = bag_pair(left_stage=2, right_stage=1, gap=0.78, right_wet=True)
        page, sketch = note_page(2.93, -0.11, s=1.27)
        self.add(counter_scene(), left[0], labels[0])
        self.at("compare the first drawing")
        self.play(FadeIn(page, shift=LEFT * 1.13), run_time=1.58)
        self.at("have your child point")
        pointer = hand(4.95, -0.62, 0.86, flip=True).rotate(0.22)
        self.play(FadeIn(pointer, shift=LEFT * 0.34), run_time=0.66)
        ring = Ellipse(width=0.83, height=1.37, color=GOLD, stroke_width=5)
        ring.move_to(sketch[1]).shift(UP * 0.13)
        self.play(Create(ring), run_time=1.10)
        self.at("at the end")
        adult_hand = hand(-4.15, -2.57, 0.72)
        self.play(FadeOut(VGroup(page, pointer, ring)), FadeIn(adult_hand),
                  FadeIn(right[0]), FadeIn(labels[1]), run_time=0.57)
        self.at("count the beans back")
        intake = VGroup(*[seed(-2.52 + i * 0.56, -2.57, 0.25) for i in range(10)])
        in_bags = [*left[2], *right[2]]
        self.play(LaggedStart(*[
            AnimationGroup(FadeOut(original, shift=DOWN * 0.21), FadeIn(counted, shift=UP * 0.36))
            for original, counted in zip(in_bags, intake)
        ], lag_ratio=0.48), run_time=1.74)
        left[0].remove(left[2])
        right[0].remove(right[2])
        self.at("throw the beans and towels")
        base, lid = bin_parts(3.17, -0.75, 1.25)
        used = VGroup(left[1].copy(), right[1].copy()).set_z_index(1)
        self.add(used)
        self.play(FadeIn(base), FadeOut(VGroup(left[0], right[0], labels, adult_hand)),
                  used.animate.scale(0.31).move_to(xy(3.17, 0.49)),
                  intake.animate.scale(0.54).move_to(xy(3.17, 0.99)), run_time=0.69)
        self.play(FadeOut(VGroup(used, intake), shift=DOWN * 0.63), FadeIn(lid), run_time=0.49)
        self.at("then wash hands")
        wash = VGroup(hand(-0.97, -0.22, 1.52), hand(0.92, -0.58, 1.52, flip=True))
        soap = VGroup(
            panel(0.86, 1.18, TEAL, TEXT).move_to(xy(-3.23, 0.03)),
            panel(0.28, 0.25, STONE).move_to(xy(-3.23, 0.72)),
            panel(0.65, 0.13, TEXT, radius=0.05).move_to(xy(-3.08, 0.88)),
            panel(0.53, 0.35, PAPER, radius=0.06).move_to(xy(-3.23, 0.08)),
        )
        flow = VGroup(*[drop(x, 0.89 + 0.24 * (i % 3), 0.75)
                        for i, x in enumerate([-0.34, -0.17, 0, 0.17, 0.34])])
        suds = VGroup(*[
            Circle(r, color=ROOT, stroke_width=2, fill_color=PAPER, fill_opacity=0.18).move_to(xy(x, y))
            for x, y, r in [(-0.48, 0.12, 0.14), (0.07, -0.05, 0.19), (0.35, 0.22, 0.12)]
        ])
        self.play(FadeOut(VGroup(base, lid)), FadeIn(wash), FadeIn(flow), FadeIn(soap), run_time=0.43)
        self.play(flow.animate.shift(DOWN * 0.57), FadeIn(suds),
                  wash[1].animate.shift(UP * 0.13 + LEFT * 0.19), run_time=0.83)
        self.finish()


class S16Return(SpokenScene):
    def construct(self):
        stone, _ = opening()
        bean = seed(1.56, 0.06, 1.99, swell=1.03)
        root = growth(1.56, -0.07, 1.38)
        shoot = growth(1.56, -0.07, 1.38, shoot=True)
        sprout = VGroup(bean, root, shoot)
        glow = Ellipse(width=4.8, height=5.4, stroke_width=0,
                       fill_color=GOLD, fill_opacity=0.08).move_to(xy(1.85, -0.32))
        self.add(counter_scene(), stone, glow, sprout)
        self.at("that pebble")
        self.play(glow.animate.set_fill(GOLD, opacity=0.20).scale(1.12),
                  sprout.animate.scale(1.07, about_point=xy(1.56, -0.01)),
                  run_time=2.71, rate_func=linear)
        self.at("it was alive")
        self.play(Rotate(shoot, angle=-0.12, about_point=shoot.get_start(),
                         rate_func=there_and_back),
                  glow.animate.set_fill(GOLD, opacity=0.11), run_time=2.90)
        self.at("water is what")
        self.play(FadeIn(drop(4.65, -0.45, 1.70), shift=DOWN * 0.58),
                  glow.animate.set_fill(GOLD, opacity=0.20), run_time=1.35)
        self.finish()


class S17End(EndCard):
    LINE = "A dry seed is alive but resting; water wakes it."
