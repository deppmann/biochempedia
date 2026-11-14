"""Reading the Warblers' Tree Map — chapter 2 of Habitat and Niche.

COLOR MAP (shared with chapter 1)
  GOLD   habitat / comparison guides
  YELLOW insects / food
  TEAL   Cape May warbler
  ORANGE Blackburnian warbler
  GREEN  black-throated green warbler
  PURPLE bay-breasted warbler
  RED    myrtle (yellow-rumped) warbler
  GREY   observation apparatus and neutral structure

All tree and bird motion is schematic. Percentages are the lesson's table values.
"""
from bp_parts import *  # noqa: F401,F403


CAPE = TEAL
BLACKBURNIAN = ORANGE
BT_GREEN = GREEN
BAY = PURPLE
MYRTLE = RED
BIRD_COLORS = [CAPE, BLACKBURNIAN, BT_GREEN, BAY, MYRTLE]
BIRD_NAMES = ["Cape May", "Blackburnian", "Black-throated green", "Bay-breasted", "Myrtle"]

# Computed directly from the lesson table: top, middle, lower, lowest (% recorded time).
DATA = np.array([
    [92.0, 4.5, 0.0, 3.5],
    [74.6, 25.4, 0.0, 0.0],
    [44.6, 52.8, 2.6, 0.0],
    [27.2, 70.2, 2.6, 0.0],
    [25.0, 30.8, 16.5, 27.7],
])


def spruce_tree(center=(-2.4, -0.15, 0), scale=1.0, grid=False):
    """The carried tree: every continuing scene rebuilds this exact geometry."""
    cx, cy, _ = center
    trunk = Line([cx, cy - 2.55 * scale, 0], [cx, cy + 2.65 * scale, 0],
                 color=GOLD, stroke_width=9)
    branches = VGroup()
    needles = VGroup()
    for i, (y, half) in enumerate([(2.20, .65), (1.65, 1.05), (1.10, 1.45),
                                    (.50, 1.85), (-.15, 2.25), (-.85, 2.55), (-1.55, 2.85)]):
        yy = cy + y * scale
        for side in (-1, 1):
            end = np.array([cx + side * half * scale, yy - .28 * scale, 0])
            branches.add(Line([cx, yy, 0], end, color=GOLD, stroke_width=5))
            for j in range(1, 5):
                p = interpolate(np.array([cx, yy, 0]), end, j / 5)
                needles.add(Line(p + UP * .14 * scale, p + DOWN * .14 * scale,
                                 color=GOLD, stroke_width=2.5).rotate(side * .35, about_point=p))
    crown = Polygon([cx, cy + 2.9 * scale, 0], [cx - 3.05 * scale, cy - 1.95 * scale, 0],
                    [cx + 3.05 * scale, cy - 1.95 * scale, 0], stroke_color=GOLD,
                    stroke_width=3, fill_color=GOLD, fill_opacity=.20)
    world = VGroup(crown, trunk, branches, needles)
    world.trunk, world.branches, world.needles = trunk, branches, needles
    if grid:
        lines = VGroup(*[
            DashedLine([cx - w * scale, cy + y * scale, 0], [cx + w * scale, cy + y * scale, 0],
                       color=TEXT, stroke_width=2, stroke_opacity=.55, dash_length=.12)
            for y, w in [(1.55, 1.12), (.25, 1.98), (-1.05, 2.62)]
        ])
        world.add(lines)
        world.grid = lines
    return world


def sway_tree(tree, amp=.022, speed=1.35):
    """Sustained breeze through the carried spruce, pivoted at its trunk."""
    about = tree.trunk.get_bottom()
    for i, part in enumerate((tree.branches, tree.needles)):
        part._sway_t = i * .7
        part._sway_last = 0.0

        def move(mob, dt, phase=i * .7):
            mob._sway_t += dt
            angle = amp * np.sin(speed * mob._sway_t + phase)
            mob.rotate(angle - mob._sway_last, about_point=about)
            mob._sway_last = angle
        part.add_updater(move)
    tree[0]._crown_t = 0.0
    tree[0]._crown_last = 0.0
    def crown_move(mob, dt):
        mob._crown_t += dt
        angle = amp * .65 * np.sin(speed * mob._crown_t)
        mob.rotate(angle - mob._crown_last, about_point=about)
        mob._crown_last = angle
    tree[0].add_updater(crown_move)
    return tree


def reading_guide(color=GOLD):
    """A continuously moving guide for reading the four recorded-time columns."""
    line = DashedLine([-3.25, -2.55, 0], [-3.25, 2.45, 0], color=color,
                      stroke_width=4, stroke_opacity=.7, dash_length=.14)
    line._guide_t = 0.0
    line._guide_x = -3.25
    def scan(mob, dt):
        mob._guide_t += dt
        x = -.05 + 3.2 * np.sin(.55 * mob._guide_t)
        mob.shift(RIGHT * (x - mob._guide_x))
        mob._guide_x = x
    line.add_updater(scan)
    return line


def bird(color, at=(0, 0, 0), scale=.9):
    """A simple labelled-color bird glyph; schematic, not a species illustration."""
    body = Ellipse(width=.48, height=.31, color=color, fill_color=color, fill_opacity=.9, stroke_width=2)
    head = Circle(radius=.13, color=color, fill_color=color, fill_opacity=.9).move_to(body.get_right() + LEFT * .03 + UP * .08)
    beak = Triangle(color=YELLOW, fill_color=YELLOW, fill_opacity=.9, stroke_width=0).scale(.075).rotate(-PI / 2)
    beak.next_to(head, RIGHT, buff=-.015)
    wing = Arc(radius=.14, start_angle=.2, angle=2.6, color=BG, stroke_width=2).move_to(body)
    g = VGroup(body, head, beak, wing).scale(scale).move_to(at)
    return g


def stopwatch(at=(4.6, 1.0, 0), scale=1.0, color=TEXT):
    ring = Circle(radius=.7 * scale, color=color, stroke_width=5).move_to(at)
    hand = Line(ring.get_center(), ring.get_center() + UP * .48 * scale, color=TEAL, stroke_width=5)
    crown = RoundedRectangle(width=.32 * scale, height=.18 * scale, corner_radius=.05,
                             color=color, fill_color=color, fill_opacity=.25).next_to(ring, UP, buff=.06)
    return VGroup(ring, hand, crown)


def clipboard(at=(4.6, -1.0, 0), scale=1.0):
    board = RoundedRectangle(width=1.65 * scale, height=2.0 * scale, corner_radius=.12,
                             color=GREY, fill_color=GREY, fill_opacity=.1, stroke_width=3).move_to(at)
    clip = RoundedRectangle(width=.65 * scale, height=.22 * scale, corner_radius=.06,
                            color=TEXT, fill_color=TEXT, fill_opacity=.2).next_to(board.get_top(), DOWN, buff=.08)
    rules = VGroup(*[Line(board.get_left() + RIGHT * .3 * scale + DOWN * d * scale,
                          board.get_right() + LEFT * .3 * scale + DOWN * d * scale,
                          color=GREY, stroke_width=2) for d in (.45, .8, 1.15)])
    return VGroup(board, clip, rules)


def model_paths():
    paths = VGroup()
    for color, y, bend in zip(BIRD_COLORS, [1.9, 1.05, .25, -.55, -1.35], [.3, -.2, .25, -.25, .18]):
        p = VMobject(stroke_color=color, stroke_width=7, stroke_opacity=.85)
        p.set_points_smoothly([[-4.7, y, 0], [-3.3, y + bend, 0], [-1.6, y - bend, 0], [.1, y, 0]])
        paths.add(p)
    return paths


def zone_strip(name, color, values, y):
    """A data strip whose four cell opacities are computed from recorded percentages."""
    label = fit_text(name, max_w=3.0, size=24, color=color, max_lines=1).move_to([-4.95, y, 0])
    cells = VGroup()
    for j, value in enumerate(values):
        # opacity is a monotonic map of the printed table value, never an invented value
        op = .27 + .68 * float(value) / 100.0
        cell = RoundedRectangle(width=1.6, height=.72, corner_radius=.08, stroke_color=color,
                                stroke_width=2.5, fill_color=color, fill_opacity=op)
        cell.move_to([-2.45 + 1.72 * j, y, 0])
        cells.add(cell)
    return VGroup(label, cells)


def five_strips():
    heads = VGroup(*[T(x, 22, GREY).move_to([-2.45 + 1.72 * i, 2.75, 0])
                     for i, x in enumerate(["top", "middle", "lower", "lowest"])])
    strips = VGroup(*[zone_strip(n, c, vals, 1.85 - i * .92)
                      for i, (n, c, vals) in enumerate(zip(BIRD_NAMES, BIRD_COLORS, DATA))])
    title = T("RECORDED TIME", 30, TEXT, weight=BOLD).move_to([.55, 3.35, 0])
    return VGroup(title, heads, strips)


def shared_cells(question=True):
    """The predict/reveal picture, rebuilt identically for s06–s08."""
    head = T("outer tips · top 3 m", 31, GOLD, weight=BOLD).move_to([0, 2.65, 0])
    names = VGroup(T("Cape May", 28, CAPE), T("Blackburnian", 28, BLACKBURNIAN)).arrange(DOWN, buff=.7, aligned_edge=RIGHT)
    names.move_to([-3.0, .75, 0])
    vals = VGroup(M("49.9%", 42, CAPE), M("34.8%", 42, BLACKBURNIAN)).arrange(DOWN, buff=.45)
    vals.move_to([1.2, .75, 0])
    boxes = VGroup(*[RoundedRectangle(width=3.0, height=1.0, corner_radius=.14, stroke_color=c,
                                      stroke_width=5, fill_color=c, fill_opacity=.30).move_to(v)
                     for c, v in zip((CAPE, BLACKBURNIAN), vals)])
    answers = VGroup(chip("SEPARATION", GREY, 28), chip("OVERLAP", GREY, 28)).arrange(RIGHT, buff=.7).move_to([0, -1.25, 0])
    q = question_card("What do two nonzero values show?", y=-3.15, size=30) if question else VGroup()
    return VGroup(head, names, boxes, vals, answers, q)


def evidence_card(text, color=TEXT):
    lab = fit_text(text, max_w=3.25, size=29, color=color, max_lines=2, weight=BOLD)
    box = RoundedRectangle(width=3.65, height=1.25, corner_radius=.15, stroke_color=color,
                           stroke_width=3, fill_color=color, fill_opacity=.22)
    lab.move_to(box)
    return VGroup(box, lab)


class S01Hook(SpokenScene):
    def construct(self):
        tree = spruce_tree(grid=False)
        sway_tree(tree)
        paths = model_paths()
        years = T("1956–1957", 28, GREY).move_to([4.6, -2.65, 0])
        self.play(FadeIn(tree), Create(paths), run_time=1.4)
        self.at("Did real warblers")
        q = fit_text("Did real warblers use the tree this way?", max_w=5.0, size=36, color=TEXT, max_lines=3)
        q.move_to([4.0, 1.2, 0])
        self.play(Write(q), run_time=1.2)
        self.at("keep the same tree")
        grid_tree = spruce_tree(grid=True)
        watch = stopwatch([4.5, .9, 0], .75)
        clip = clipboard([4.5, -1.0, 0], .75)
        self.play(FadeOut(q), FadeOut(paths), Transform(tree, grid_tree), FadeIn(watch), FadeIn(clip), run_time=1.4)
        self.at("recorded observations")
        self.play(FadeIn(years), Rotate(watch[1], angle=-1.2, about_point=watch[0].get_center()), run_time=.9)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Habitat and niche"
    TITLE = "Reading the Warblers' Tree Map"

    def construct(self):
        tree = spruce_tree(center=(-3.8, -.2, 0), scale=.72, grid=True)
        sway_tree(tree)
        title = fit_text(self.TITLE, max_w=7.2, size=47, font=TITLE_FONT, max_lines=2).move_to([2.6, .55, 0])
        lesson = T(self.LESSON.upper(), 22, GREY).move_to([2.6, 2.15, 0])
        rule = Line([-.2, -.65, 0], [5.4, -.65, 0], color=GOLD, stroke_width=5)
        bob(tree.branches, amp=.025, speed=1.5)
        self.add(tree)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=.9)
        self.wait(.7)
        self.play(FadeOut(VGroup(lesson, title)), rule.animate.move_to([-3.8, 1.1, 0]).scale(.55), run_time=.35)
        self.finish()


class S03Zones(SpokenScene):
    def construct(self):
        tree = spruce_tree(center=(-2.7, -.2, 0), scale=.92)
        sway_tree(tree)
        self.play(FadeIn(tree), run_time=.7)
        self.at("divided spruce trees")
        bands = VGroup(*[Rectangle(width=w, height=1.0, stroke_color=TEAL, stroke_width=2,
                                   fill_color=TEAL, fill_opacity=.08).move_to([-2.7, y, 0])
                         for y, w in [(1.65, 2.2), (.55, 3.35), (-.55, 4.55), (-1.65, 5.45)]])
        self.play(LaggedStart(*[FadeIn(b) for b in bands], lag_ratio=.18), run_time=1.1)
        self.at("Height bands ran down")
        nums = VGroup(*[M(str(i + 1), 27, TEXT).move_to([-5.75, y, 0]) for i, y in enumerate([1.65, .55, -.55, -1.65])])
        self.play(FadeIn(nums, lag_ratio=.18), run_time=.9)
        self.at("Each branch also")
        inset = Circle(radius=1.55, color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=.96).move_to([4.4, .45, 0])
        branch = Line([3.15, .45, 0], [5.65, .45, 0], color=GOLD, stroke_width=8)
        marks = VGroup(Dot([3.45, .45, 0], color=CAPE, radius=.15), Dot([4.4, .45, 0], color=BLACKBURNIAN, radius=.15),
                       Dot([5.35, .45, 0], color=GREEN, radius=.15))
        self.play(FadeIn(inset), GrowFromPoint(branch, branch.get_start()), run_time=.8)
        labels = VGroup(T("base", 24, CAPE).move_to([3.25, -1.35, 0]),
                        T("middle", 24, BLACKBURNIAN).move_to([4.4, -1.35, 0]),
                        T("outer tips", 24, GREEN).move_to([5.75, -1.35, 0]))
        self.at("a base")
        self.play(FadeIn(marks[0]), FadeIn(labels[0]), run_time=.45)
        self.at("a middle")
        self.play(FadeIn(marks[1]), FadeIn(labels[1]), run_time=.45)
        self.at("outer tips")
        self.play(FadeIn(marks[2]), FadeIn(labels[2]), run_time=.45)
        self.at("same map for every bird")
        clean = spruce_tree(center=(-2.7, -.2, 0), scale=.92, grid=True)
        self.play(FadeOut(VGroup(inset, branch, marks, labels, bands, nums)), Transform(tree, clean), run_time=1.0)
        self.finish()


class S04Timing(SpokenScene):
    def construct(self):
        tree = spruce_tree(center=(-2.4, -.15, 0), scale=.9, grid=True)
        sway_tree(tree)
        b = bird(CAPE, [-3.8, 1.65, 0], .95)
        secs = ValueTracker(0)
        ro = Readout([("visible", lambda: secs.get_value(), "{:4.1f} s", CAPE)], at=[4.5, 1.5, 0], widest=[99.9], title="stopwatch")
        watch = stopwatch([4.5, -.55, 0], .8)
        self.add(tree)
        self.at("could see a bird")
        self.play(FadeIn(b), FadeIn(watch), FadeIn(ro), run_time=.7)
        self.at("timed how long")
        self.play(b.animate.move_to([-1.6, .55, 0]), secs.animate.set_value(3.6), Rotate(watch[1], -1.6, about_point=watch[0].get_center()), run_time=2.0, rate_func=linear)
        self.at("forest was dense")
        cover = VGroup(*[Line([-.2 + i * .18, -.8, 0], [.35 + i * .12, 1.25, 0], color=GOLD, stroke_width=7) for i in range(7)])
        self.play(FadeIn(cover), b.animate.move_to([.0, .1, 0]).set_opacity(.12), run_time=.8)
        self.at("Many hours of watching")
        hour = ValueTracker(0)
        hour_counter = counter("watching {:.0f} min", hour, [4.5, -2.1, 0], 29, GREY)
        self.add(hour_counter)
        self.play(hour.animate.set_value(60), run_time=1.6, rate_func=linear)
        self.at("few useful seconds")
        self.play(Indicate(ro, color=CAPE, scale_factor=1.04), run_time=.6)
        self.at("Each colored timer")
        others = VGroup(*[bird(c, [-4.3 + i * 1.25, -1.45 + .3 * (i % 2), 0], .72) for i, c in enumerate(BIRD_COLORS)])
        self.play(FadeOut(cover), FadeOut(b), FadeIn(others, lag_ratio=.12), secs.animate.set_value(8.4), run_time=1.5)
        self.at("remains visible")
        ticks = VGroup(*[Dot([-3.8 + i * .65, -2.15, 0], color=BIRD_COLORS[i % 5], radius=.08) for i in range(10)])
        self.play(LaggedStart(*[FadeIn(t, shift=UP * .3) for t in ticks], lag_ratio=.08), run_time=1.0)
        self.finish()


class S05PercentMap(SpokenScene):
    def construct(self):
        display = five_strips()
        pulse(display[2], base=2.5, amp=1.3, speed=2.0)
        ticks = VGroup(*[Dot([-5.3 + i * .5, 3.35, 0], color=BIRD_COLORS[i % 5], radius=.075) for i in range(18)])
        self.add(ticks)
        self.at("recorded seconds became percentages")
        self.play(ReplacementTransform(ticks, display), run_time=1.5)
        guide = reading_guide()
        self.add(guide)
        self.at("Darker zones")
        centers = VGroup(*[display[2][i][1][int(np.argmax(DATA[i]))] for i in range(5)])
        self.play(LaggedStart(*[Indicate(c, color=BIRD_COLORS[i], scale_factor=1.04) for i, c in enumerate(centers)], lag_ratio=.12), run_time=1.3)
        self.at("different centers of activity")
        guides = VGroup(*[SurroundingRectangle(c, color=GOLD, buff=.05, stroke_width=3) for c in centers])
        self.play(FadeIn(guides, lag_ratio=.12), run_time=1.0)
        self.at("colored areas still overlap")
        top_cells = VGroup(*[display[2][i][1][0] for i in range(5)])
        self.play(LaggedStart(*[Indicate(c, color=GOLD, scale_factor=1.03) for c in top_cells], lag_ratio=.1), run_time=1.1)
        self.at("No bird owns")
        private = T("shared zones", 31, GOLD, weight=BOLD).move_to([4.9, -2.75, 0])
        self.play(FadeIn(private), FadeOut(guides), run_time=.7)
        self.at("centered activity high")
        arrow = Arrow([-2.45, -2.6, 0], [-2.45, 2.25, 0], color=GOLD, stroke_width=5, tip_length=.22)
        self.play(GrowArrow(arrow), run_time=.8)
        self.at("Others centered lower")
        self.play(arrow.animate.shift(RIGHT * 3.44).rotate(PI, about_point=[.99, -.15, 0]), run_time=.9)
        self.at("spread their time more widely")
        self.play(Indicate(display[2][4], color=MYRTLE, scale_factor=1.025), FadeOut(private), run_time=1.0)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        pic = shared_cells(question=True)
        pulse(pic[2], base=5, amp=1.4, speed=2.1)
        self.at("Predict how to read")
        self.play(FadeIn(pic[0]), FadeIn(pic[1]), run_time=.7)
        self.at("Both kinds clearly")
        self.play(FadeIn(pic[2]), FadeIn(pic[3]), run_time=.9)
        self.at("complete separation")
        self.play(FadeIn(pic[4][0]), run_time=.5)
        self.at("show overlap")
        self.play(FadeIn(pic[4][1]), run_time=.5)
        self.at("Hold your answer")
        self.play(FadeIn(pic[5]), Indicate(pic[2], color=GOLD, scale_factor=1.03), run_time=.8)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "What do two nonzero values show?"
    OPTIONS = ()
    SECONDS = 4.5

    def backdrop(self):
        pic = shared_cells(question=False)
        pulse(pic[2], base=5, amp=1.4, speed=2.1)
        pulse(pic[2][0], base=5, amp=1.2, speed=2.2)
        pulse(pic[2][1], base=5, amp=1.2, speed=2.2)
        return pic


class S08Reveal(SpokenScene):
    def construct(self):
        pic = shared_cells(question=False)
        self.add(pic)
        self.at("It shows overlap")
        selected = chip("OVERLAP", GOLD, 30).move_to(pic[4][1])
        self.play(Transform(pic[4][1], selected), pic[4][0].animate.set_opacity(.3), run_time=.7)
        self.at("Both kinds spent")
        self.play(Indicate(pic[2], color=GOLD, scale_factor=1.04), run_time=.8)
        self.at("percentages can still differ")
        diff = M("49.9 − 34.8 = 15.1 points", 30, TEXT).move_to([0, -2.25, 0])
        self.play(FadeIn(diff), run_time=.8)
        self.at("Read down a column")
        table = five_strips()
        pulse(table[2], base=2.5, amp=1.3, speed=2.0)
        self.play(FadeOut(pic), FadeOut(diff), FadeIn(table), run_time=1.0)
        vguide = SurroundingRectangle(VGroup(*[table[2][i][1][0] for i in range(5)]), color=GOLD, buff=.08, stroke_width=4)
        self.play(Create(vguide), run_time=.8)
        self.at("read across a row")
        hguide = SurroundingRectangle(table[2][3], color=BAY, buff=.08, stroke_width=4)
        self.play(ReplacementTransform(vguide, hguide), run_time=.8)
        self.at("large value marks")
        self.play(Indicate(table[2][3][1][1], color=GOLD, scale_factor=1.05), run_time=.8)
        self.at("Smaller values still matter")
        smalls = VGroup(table[2][0][1][1], table[2][2][1][2], table[2][4][1][2])
        self.play(LaggedStart(*[Indicate(c, color=GOLD, scale_factor=1.05) for c in smalls], lag_ratio=.2), FadeOut(hguide), run_time=1.1)
        self.finish()


class S09Limits(SpokenScene):
    def construct(self):
        tree = spruce_tree(center=(-4.5, -.3, 0), scale=.65, grid=True)
        sway_tree(tree, amp=.035)
        cards = VGroup(evidence_card("TIME RECORDED", TEAL), evidence_card("SOME SINGING", YELLOW),
                       evidence_card("NO COMPETITION MEASURE", RED)).arrange(DOWN, buff=.38).move_to([2.35, .35, 0])
        self.add(tree)
        self.at("separate observation from explanation")
        self.play(FadeIn(cards[0], shift=LEFT * .3), run_time=.7)
        self.at("not insects")
        food = VGroup(T("insects eaten", 28, YELLOW), Line(LEFT * 1.1, RIGHT * 1.1, color=RED, stroke_width=7)).move_to([-4.3, -2.65, 0])
        food[1].rotate(.18)
        food[1].layout_ok = True  # intentional strike-through: the narration says these were not measured
        self.play(FadeIn(food), run_time=.6)
        self.at("singing birds")
        self.play(FadeIn(cards[1], shift=LEFT * .3), run_time=.7)
        self.at("Visibility matters")
        veil = Rectangle(width=2.7, height=3.1, color=GOLD, fill_color=GOLD, fill_opacity=.22, stroke_width=0).move_to(tree)
        veil._mist_t = 0.0
        veil._mist_x = veil.get_x()
        def mist(mob, dt):
            mob._mist_t += dt
            mob.set_fill(opacity=.20 + .12 * (1 + np.sin(2.0 * mob._mist_t)) / 2)
            x = -4.5 + .45 * np.sin(1.25 * mob._mist_t)
            mob.shift(RIGHT * (x - mob._mist_x))
            mob._mist_x = x
        veil.add_updater(mist)
        self.play(FadeIn(veil), run_time=.8)
        self.at("observer could record")
        watch = stopwatch([-4.5, .0, 0], .65)
        watch[1].add_updater(lambda hand, dt: hand.rotate(-.9 * dt, about_point=watch[0].get_center()))
        self.play(FadeIn(watch), Rotate(watch[1], -1.5, about_point=watch[0].get_center()), run_time=.8)
        self.at("did not directly measure competition")
        self.play(FadeIn(cards[2], shift=LEFT * .3), FadeOut(veil), run_time=.8)
        self.at("may reduce competition")
        inference = T("may reduce competition", 29, GOLD).move_to([2.35, -2.55, 0])
        tag = scope_tag("INFERENCE", size=24, color=GOLD)
        arrow = DashedLine(cards[2].get_bottom(), inference.get_top(), color=GOLD, stroke_width=4, dash_length=.15)
        self.play(Create(arrow), FadeIn(inference), FadeIn(tag), run_time=.9)
        pulse(cards, base=3, amp=1.0, speed=1.7)
        self.at("cannot prove that cause")
        self.play(Indicate(cards[2], color=RED, scale_factor=1.04), run_time=.8)
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        obs = evidence_card("OBSERVATION", TEAL).move_to([-4.45, .45, 0])
        inf = evidence_card("INFERENCE", GOLD).move_to([0, .45, 0])
        lim = evidence_card("LIMIT", RED).move_to([4.45, .45, 0])
        tree = spruce_tree(center=(-4.45, -1.65, 0), scale=.34, grid=True)
        sway_tree(tree, amp=.045)
        arr1 = Arrow(obs.get_right(), inf.get_left(), color=GREY, stroke_width=4, tip_length=.18)
        arr2 = Arrow(inf.get_right(), lim.get_left(), color=GREY, stroke_width=4, tip_length=.18)
        self.at("careful claim")
        self.play(FadeIn(obs), GrowArrow(arr1), FadeIn(inf), GrowArrow(arr2), FadeIn(lim), run_time=1.2)
        pulse(VGroup(obs, inf, lim), base=3, amp=1.0, speed=1.6)
        self.at("shared a habitat")
        overlaps = VGroup(*[Ellipse(width=1.3, height=.65, color=c, fill_color=c, fill_opacity=.15, stroke_width=3)
                            .move_to([-4.8 + i * .2, -1.55 + (i % 2) * .25, 0]) for i, c in enumerate(BIRD_COLORS)])
        self.play(FadeIn(tree), FadeIn(overlaps, lag_ratio=.1), run_time=1.0)
        self.at("possible explanation")
        dotted = DashedLine([-.85, -1.55, 0], [.85, -1.55, 0], color=GOLD, stroke_width=5, dash_length=.15)
        may = T("may reduce competition", 27, GOLD).next_to(dotted, DOWN, buff=.18)
        self.play(Create(dotted), FadeIn(may), run_time=.9)
        pulse(dotted, base=5, amp=1.5, speed=1.8)
        self.at("evidence for the idea")
        watch = stopwatch([4.45, -1.55, 0], .55, RED)
        self.play(FadeIn(watch), run_time=.7)
        self.at("not proof")
        proof = T("NOT PROOF", 30, RED, weight=BOLD).next_to(watch, DOWN, buff=.25)
        self.play(FadeIn(proof), Indicate(lim, color=RED, scale_factor=1.04), run_time=.7)
        self.finish()


class S11End(EndCard):
    LINE = "Different niches can reduce competition, helping species share a habitat."
