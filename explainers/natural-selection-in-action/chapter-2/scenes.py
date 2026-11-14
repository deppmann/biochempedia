"""Who Selects the Breeders? — chapter 2 of Natural selection in action.

COLOR MAP (copied exactly from chapter 1)
  CREAM  = a pale moth / the less-wanted inherited plant form
  DUSK   = a dark moth / the strongly wanted inherited plant form
  SOOT   = sooty (dark) bark;  LICHEN = clean, pale bark
  BLUE   = the bird, and the ring that means "the bird spots this moth"
  RED    = eaten / paths that do not contribute offspring
  GREEN  = survivors, young, "more common"
  TEAL   = a science word being defined / deliberate human choice
  GREY   = outlines, plain labels

The population world is rebuilt by builder functions so rows, gates and landmarks
stay at exactly the same coordinates from scene to scene.
"""
from bp_parts import *  # noqa: F401,F403

CREAM = "#E8DDB5"
DUSK = "#4A3F5C"
DUSK_LINE = "#9B8DB5"
SOOT = "#2A2524"
LICHEN = "#B4AE98"
BOARD = "#27303A"

ROW_X = np.linspace(-4.5, 4.5, 6)
PARENT_Y = 1.45
OFFSPRING_Y = -0.75
GATE_Y = 0.30
START_KINDS = ["less", "strong", "less", "strong", "less", "strong"]
NEXT_KINDS = ["strong", "strong", "less", "strong", "strong", "less"]


def moth(kind, scale=1.0):
    """Chapter-one moth, unchanged in colour and geometry."""
    fill, line = (CREAM, "#FFF4D0") if kind == "pale" else (DUSK, DUSK_LINE)
    wl = Ellipse(width=0.52, height=0.30, fill_color=fill, fill_opacity=1,
                 stroke_color=line, stroke_width=2).rotate(0.5).shift(LEFT * 0.22 + UP * 0.04)
    wr = Ellipse(width=0.52, height=0.30, fill_color=fill, fill_opacity=1,
                 stroke_color=line, stroke_width=2).rotate(-0.5).shift(RIGHT * 0.22 + UP * 0.04)
    body = Ellipse(width=0.14, height=0.44, fill_color=fill, fill_opacity=1,
                   stroke_color=line, stroke_width=2).shift(DOWN * 0.02)
    return VGroup(wl, wr, body).scale(scale * 1.5)


def bird(scale=1.0):
    body = Ellipse(width=1.1, height=0.7, fill_color=BLUE, fill_opacity=0.9,
                   stroke_color=BLUE, stroke_width=2)
    head = Circle(radius=0.24, fill_color=BLUE, fill_opacity=0.9,
                  stroke_color=BLUE, stroke_width=2).shift(LEFT * 0.55 + UP * 0.2)
    beak = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI / 2)
    beak.shift(LEFT * 0.86 + UP * 0.2)
    tail = Triangle(fill_color=BLUE, fill_opacity=0.9, stroke_width=0).scale(0.2).rotate(-PI / 2)
    tail.shift(RIGHT * 0.62 + DOWN * 0.04)
    eye = Dot(head.get_center() + [-0.05, 0.05, 0], radius=0.04, color=BG)
    return VGroup(body, head, beak, tail, eye).scale(scale)


def plant(kind, scale=1.0):
    """A schematic plant whose blossom carries the inherited form."""
    fill, line = (CREAM, "#FFF4D0") if kind == "less" else (DUSK, DUSK_LINE)
    stem = Line(DOWN * 0.42, UP * 0.32, color=GREY, stroke_width=7)
    leaf_l = Ellipse(width=0.42, height=0.20, fill_color=GREY, fill_opacity=0.7,
                     stroke_color=GREY, stroke_width=2).rotate(0.45).move_to([-0.18, -0.10, 0])
    leaf_r = leaf_l.copy().rotate(-0.9).move_to([0.18, 0.08, 0])
    blossom = Circle(radius=0.24, fill_color=fill, fill_opacity=1,
                     stroke_color=line, stroke_width=3).move_to([0, 0.46, 0])
    return VGroup(stem, leaf_l, leaf_r, blossom).scale(scale)


def seed(kind, scale=1.0):
    fill, line = (CREAM, "#FFF4D0") if kind == "less" else (DUSK, DUSK_LINE)
    return Ellipse(width=0.24, height=0.38, fill_color=fill, fill_opacity=1,
                   stroke_color=line, stroke_width=2).rotate(-0.35).scale(scale)


def plant_row(kinds, y, scale=1.0):
    return VGroup(*[plant(k, scale).move_to([x, y, 0]) for x, k in zip(ROW_X, kinds)])


def moth_row(kinds, y, scale=0.8):
    return VGroup(*[moth(k, scale).move_to([x, y, 0]) for x, k in zip(ROW_X, kinds)])


def row_rail(y, color=GREY):
    return Line([-5.15, y - 0.62, 0], [5.15, y - 0.62, 0], color=color,
                stroke_width=3).set_opacity(0.7)


def population_world(kinds=START_KINDS, offspring=None, ringed=False, rows=1):
    """The carried plant world used from s02 through s07."""
    parents = plant_row(kinds, PARENT_Y)
    p_label = T("parents", 30, GREY, weight=BOLD).move_to([-5.75, PARENT_Y, 0])
    p_rail = row_rail(PARENT_Y)
    lower = VGroup()
    for r in range(rows):
        y = OFFSPRING_Y - r * 0.62
        lower.add(row_rail(y), T("offspring" if r == 0 else "next", 28, GREY).move_to([-5.75, y, 0]))
    if offspring is not None:
        lower.add(plant_row(offspring, OFFSPRING_Y, 0.88))
    board = RoundedRectangle(width=12.25, height=5.75, corner_radius=0.24,
                             stroke_width=0,
                             fill_color=BOARD, fill_opacity=1).move_to([0, 0.15, 0])
    g = VGroup(board, p_rail, parents, p_label, lower)
    g.parents = parents
    g.lower = lower
    if ringed:
        rings = VGroup(*[Circle(radius=0.58, color=TEAL, stroke_width=5).move_to(parents[i])
                         for i, k in enumerate(kinds) if k == "strong"])
        g.add(rings)
        g.rings = rings
    return g


def choice_gate():
    gate = RoundedRectangle(width=3.1, height=0.52, corner_radius=0.14,
                            stroke_color=TEAL, stroke_width=4, fill_color=TEAL,
                            fill_opacity=0.12).move_to([0, GATE_Y, 0])
    label = T("people choose", 28, TEAL, weight=BOLD).move_to(gate)
    gate.layout_ok = True  # Label intentionally sits inside its own gate.
    return VGroup(gate, label)


def filter_card(kind, center, scale=1.0, title=True):
    """A compact carried filter: inherited variation enters, unequal reproduction leaves."""
    cx, cy = center[:2]
    col = BLUE if kind == "natural" else TEAL
    box = RoundedRectangle(width=5.6, height=4.5, corner_radius=0.22, stroke_color=col,
                           stroke_width=3, fill_color=BOARD, fill_opacity=1).move_to([cx, cy, 0])
    head_text = "natural selection" if kind == "natural" else "artificial selection"
    head = T(head_text, 34, col, weight=BOLD).move_to([cx, cy + 1.78, 0])
    incoming = VGroup(moth("pale", 0.48), moth("dark", 0.48)).arrange(RIGHT, buff=0.35)
    incoming.move_to([cx - 1.55, cy + 0.55, 0])
    arr1 = Arrow([cx - 0.6, cy + 0.55, 0], [cx + 0.25, cy + 0.55, 0], buff=0.05,
                 color=GREY, stroke_width=4, tip_length=0.18)
    if kind == "natural":
        selector = bird(0.58).move_to([cx + 1.45, cy + 0.65, 0])
        cause = T("conditions", 34, BLUE).move_to([cx + 1.45, cy - 0.05, 0])
    else:
        selector = VGroup(RoundedRectangle(width=1.55, height=0.62, corner_radius=0.14,
                                           stroke_color=TEAL, stroke_width=4),
                          Dot(radius=0.13, color=TEAL)).move_to([cx + 1.35, cy + 0.62, 0])
        cause = T("people's choices", 34, TEAL).move_to([cx + 1.35, cy - 0.05, 0])
    output = VGroup(moth("dark", 0.48), moth("dark", 0.48), moth("pale", 0.48)).arrange(RIGHT, buff=0.18)
    output.move_to([cx, cy - 1.18, 0])
    down = Arrow([cx, cy + 0.12, 0], [cx, cy - 0.75, 0], buff=0.04,
                 color=GREEN, stroke_width=5, tip_length=0.18)
    g = VGroup(box, incoming, arr1, selector, cause, down, output)
    if title:
        g.add(head)
    g.box, g.head, g.output, g.cause = box, head, output, cause
    return g.scale(scale, about_point=np.array([cx, cy, 0]))


def predict_backdrop():
    world = population_world(ringed=True, rows=3)
    gate = choice_gate()
    gate.move_to([0, GATE_Y, 0])
    for p in world.parents:
        bob(p, amp=0.09, speed=1.35, seed=int((p.get_x() + 5) * 3))
    return VGroup(world, gate)


def population_strip(y, shares, x0=-4.7, width=9.4, icon="moth"):
    """Several unlabeled generations, with form preserved within each generation."""
    groups = VGroup()
    xs = np.linspace(x0, x0 + width, len(shares))
    for x, strong in zip(xs, shares):
        kinds = (["dark"] * strong + ["pale"] * (4 - strong)) if icon == "moth" else \
                (["strong"] * strong + ["less"] * (4 - strong))
        maker = moth if icon == "moth" else plant
        mini = VGroup(*[maker(k, 0.30 if icon == "moth" else 0.40) for k in kinds]).arrange_in_grid(2, 2, buff=0.07)
        mini.move_to([x, y, 0])
        groups.add(mini)
    return groups


class S00Hook(SpokenScene):
    def construct(self):
        bark = RoundedRectangle(width=11.2, height=4.0, corner_radius=0.2, stroke_color=GREY,
                                stroke_width=3, fill_color=SOOT, fill_opacity=1).move_to([0, -0.15, 0])
        parents = moth_row(["pale", "dark", "pale", "dark", "dark", "pale"], 1.0, 0.78)
        offspring = moth_row(["dark", "dark", "pale", "dark", "dark", "dark"], -1.15, 0.68)
        br = bird(0.75).move_to([4.85, 2.55, 0])
        red_paths = VGroup(*[Arrow(br.get_bottom(), parents[i].get_top(), buff=0.12, color=RED,
                                      stroke_width=4, tip_length=0.16) for i in (0, 2)])
        survivors = VGroup(*[Circle(radius=0.50, color=GREEN, stroke_width=4).move_to(parents[i])
                             for i in (1, 3, 4)])
        world = VGroup(bark, parents, offspring, br, red_paths, survivors)
        pulse(bark, base=3, amp=0.8, speed=1.4)
        bob(br, amp=0.10, speed=1.25, seed=2)
        self.at("The first film showed")
        self.play(FadeIn(bark), LaggedStart(*[FadeIn(m) for m in parents], lag_ratio=0.10), run_time=1.0)
        self.play(FadeIn(br), LaggedStart(*[GrowArrow(a) for a in red_paths], lag_ratio=0.15),
                  LaggedStart(*[Create(r) for r in survivors], lag_ratio=0.12), run_time=1.0)
        self.at("Can people shift")
        self.play(world.animate.scale(0.62).move_to([-3.35, 0.0, 0]), run_time=0.9)
        people_box = RoundedRectangle(width=5.5, height=4.2, corner_radius=0.22,
                                      stroke_color=TEAL, stroke_width=4).move_to([3.35, 0, 0])
        q = T("?", 86, TEAL, weight=BOLD).move_to(people_box)
        self.play(Create(people_box), FadeIn(q, scale=0.6), run_time=0.8)
        self.at("Keep the parent row")
        labels = VGroup(T("parent row", 28, GREY), T("offspring row", 28, GREEN),
                        T("trait frequency", 28, TEAL)).arrange(DOWN, buff=0.34).move_to([3.35, 0, 0])
        self.play(FadeOut(q), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in labels], lag_ratio=0.18),
                  run_time=1.2)
        self.at("The population picture")
        pulse(people_box, base=4, amp=1.3, speed=2.0)
        self.play(Indicate(labels, color=TEAL, scale_factor=1.04), run_time=0.8)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Natural selection in action"
    TITLE = "Who Selects the Breeders?"

    def construct(self):
        left = filter_card("natural", [-3.4, -0.2, 0], 0.72, title=False).set_opacity(0.38)
        empty = RoundedRectangle(width=4.0, height=3.25, corner_radius=0.2,
                                 stroke_color=TEAL, stroke_width=4).move_to([3.4, -0.2, 0]).set_opacity(0.45)
        title = T(self.TITLE, 52, font=TITLE_FONT).move_to([0, 2.9, 0])
        lesson = T(self.LESSON.upper(), 22, GREY).next_to(title, DOWN, buff=0.16)
        self.play(FadeIn(left), Create(empty), FadeIn(title), FadeIn(lesson), run_time=0.7)
        gate = choice_gate().move_to([3.4, -0.2, 0])
        self.play(ReplacementTransform(title.copy(), gate), FadeOut(title), FadeOut(lesson), run_time=0.8)
        self.finish()


class S02NewPopulation(SpokenScene):
    def construct(self):
        board = RoundedRectangle(width=12.25, height=5.75, corner_radius=0.24,
                                 stroke_width=0,
                                 fill_color=BOARD, fill_opacity=1).move_to([0, 0.15, 0])
        moths = moth_row(["pale", "dark", "pale", "dark", "pale", "dark"], PARENT_Y, 0.76)
        rails = VGroup(row_rail(PARENT_Y), row_rail(OFFSPRING_Y))
        labels = VGroup(T("parents", 30, GREY, weight=BOLD).move_to([-5.75, PARENT_Y, 0]),
                        T("offspring", 28, GREY).move_to([-5.75, OFFSPRING_Y, 0]))
        self.add(board, rails, labels, moths)
        plants = plant_row(START_KINDS, PARENT_Y)
        self.at("Replace the moths")
        self.play(*[ReplacementTransform(m, p) for m, p in zip(moths, plants)], run_time=1.2)
        for i, p in enumerate(plants):
            bob(p, amp=0.10, speed=1.3, seed=i)
        self.at("Some show the wanted")
        strong = VGroup(*[plants[i] for i, k in enumerate(START_KINDS) if k == "strong"])
        self.play(LaggedStart(*[Indicate(p, color=DUSK_LINE, scale_factor=1.16) for p in strong],
                              lag_ratio=0.18), run_time=1.1)
        self.at("Others show it less")
        less = VGroup(*[plants[i] for i, k in enumerate(START_KINDS) if k == "less"])
        self.play(LaggedStart(*[Indicate(p, color=CREAM, scale_factor=1.16) for p in less],
                              lag_ratio=0.18), run_time=1.0)
        self.at("Their colors match")
        legend = VGroup(chip("wanted form", DUSK_LINE, 28), chip("less of it", CREAM, 28)).arrange(RIGHT, buff=0.5)
        legend.move_to([0, 2.85, 0])
        self.play(FadeIn(legend), run_time=0.6)
        self.at("Each plant keeps")
        inherited = caption("inherited variation", size=34, color=TEAL)
        self.play(FadeIn(inherited), Indicate(plants, color=TEAL, scale_factor=1.03), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Choice(SpokenScene):
    def construct(self):
        world = population_world()
        for i, p in enumerate(world.parents):
            bob(p, amp=0.10, speed=1.3, seed=i)
        self.add(world)
        strong_i = [i for i, k in enumerate(START_KINDS) if k == "strong"]
        rings = VGroup(*[Circle(radius=0.58, color=TEAL, stroke_width=5).move_to(world.parents[i]) for i in strong_i])
        hand = VGroup(RoundedRectangle(width=1.0, height=0.55, corner_radius=0.22,
                                       stroke_color=TEAL, stroke_width=4),
                      Line([0.45, 0, 0], [1.15, 0.45, 0], color=TEAL, stroke_width=7))
        hand.move_to([-5.6, 2.65, 0])
        self.at("A farmer marks")
        self.play(hand.animate.move_to(world.parents[1].get_center() + UP * 0.8), Create(rings[0]), run_time=0.8)
        self.play(hand.animate.move_to(world.parents[3].get_center() + UP * 0.8), Create(rings[1]), run_time=0.6)
        self.play(hand.animate.move_to(world.parents[5].get_center() + UP * 0.8), Create(rings[2]), run_time=0.6)
        seeds = VGroup(*[seed("strong").move_to(world.parents[i].get_center() + DOWN * 0.60) for i in strong_i])
        self.at("and saves seeds")
        self.play(FadeOut(hand), FadeIn(seeds), run_time=0.5)
        gate = choice_gate()
        self.at("The choice is deliberate")
        self.play(FadeIn(gate), run_time=0.6)
        targets = [[-1.2, OFFSPRING_Y, 0], [0, OFFSPRING_Y, 0], [1.2, OFFSPRING_Y, 0]]
        self.at("The choice changes")
        self.play(*[s.animate.move_to(t) for s, t in zip(seeds, targets)], run_time=1.4, rate_func=linear)
        self.at("Plants without the mark")
        stopped = VGroup(*[DashedLine(world.parents[i].get_bottom(), [world.parents[i].get_x(), GATE_Y + 0.35, 0],
                                           color=RED, stroke_width=3) for i, k in enumerate(START_KINDS) if k == "less"])
        stopbar = Line([-4.9, GATE_Y + 0.28, 0], [4.9, GATE_Y + 0.28, 0], color=RED, stroke_width=4)
        self.play(LaggedStart(*[Create(x) for x in stopped], lag_ratio=0.18), Create(stopbar), run_time=1.0)
        self.at("their seeds are not used")
        self.play(Indicate(VGroup(stopped, stopbar), color=RED, scale_factor=1.02), run_time=0.8)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        self.add(back)
        self.at("If the farmer repeats")
        self.play(Indicate(back[1], color=TEAL, scale_factor=1.06), run_time=0.8)
        q = question_card("What becomes more common?", y=-3.43, color=GOLD, size=34)
        self.at("what should happen")
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.6)
        legend = VGroup(chip("wanted", DUSK_LINE, 28), chip("less wanted", CREAM, 28)).arrange(RIGHT, buff=0.35)
        legend.move_to([3.9, 2.85, 0])
        self.play(FadeIn(legend), run_time=0.5)
        self.at("Watch the empty")
        self.play(Indicate(back[0].lower, color=GREEN, scale_factor=1.02), run_time=0.8)
        self.play(Indicate(legend, color=TEAL, scale_factor=1.06), run_time=0.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "What becomes more common?"
    SECONDS = 4.5
    CARD = {"y": -3.43, "color": GOLD, "size": 34, "max_w": 9.4}
    RING_AT = (6.0, -2.48, 0)

    def backdrop(self):
        return predict_backdrop()


class S06Reveal(SpokenScene):
    def construct(self):
        world = population_world(ringed=True)
        gate = choice_gate()
        for i, p in enumerate(world.parents):
            bob(p, amp=0.10, speed=1.3, seed=i)
        self.add(world, gate)
        seeds = VGroup(*[seed("strong").move_to(world.parents[i].get_center() + DOWN * 0.60)
                         for i, k in enumerate(START_KINDS) if k == "strong"])
        self.add(seeds)
        offspring = plant_row(NEXT_KINDS, OFFSPRING_Y, 0.88)
        self.at("The next row")
        self.play(*[s.animate.move_to(offspring[i].get_center()) for i, s in enumerate(seeds)], run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p, scale=0.55) for p in offspring], lag_ratio=0.12), FadeOut(seeds), run_time=1.1)
        for i, p in enumerate(offspring):
            bob(p, amp=0.03, speed=1.8, seed=i + 8)
        wanted = VGroup(*[offspring[i] for i, k in enumerate(NEXT_KINDS) if k == "strong"])
        self.at("The selected form came")
        self.play(Indicate(wanted, color=DUSK_LINE, scale_factor=1.10), run_time=0.9)
        self.at("No plant changed")
        links = VGroup(*[DashedLine(world.parents[i].get_bottom(), offspring[i].get_top(), color=GREY,
                                    stroke_width=2) for i in range(6)])
        self.play(FadeOut(gate), Create(links), Indicate(world.parents, color=GREY, scale_factor=1.02), run_time=1.0)
        self.at("The population changed")
        bracket = Line(offspring[0].get_left() + DOWN * 0.70, offspring[3].get_right() + DOWN * 0.70,
                       color=GREEN, stroke_width=7)
        label = T("trait frequency", 32, TEAL, weight=BOLD).next_to(bracket, DOWN, buff=0.16)
        self.play(GrowFromEdge(bracket, LEFT), FadeIn(label), run_time=1.2)
        self.at("contributed more offspring")
        self.play(Indicate(VGroup(bracket, wanted), color=GREEN, scale_factor=1.04), run_time=1.0)
        self.finish()


class S07Repeat(SpokenScene):
    def construct(self):
        gate = choice_gate().move_to([0, 1.95, 0])
        rows = VGroup(
            plant_row(["less", "strong", "less", "strong", "less", "strong"], 0.85, 0.62),
            plant_row(["strong", "strong", "less", "strong", "less", "strong"], -0.25, 0.62),
            plant_row(["strong", "strong", "strong", "strong", "less", "strong"], -1.35, 0.62),
        )
        for j, row in enumerate(rows):
            for i, p in enumerate(row):
                bob(p, amp=0.09, speed=1.3, seed=i + 4 * j)
        board = RoundedRectangle(width=12.25, height=6.0, corner_radius=0.24,
                                 stroke_width=0, fill_color=BOARD, fill_opacity=1).move_to([0, 0.0, 0])
        self.add(board)
        self.at("Repeat the cycle")
        self.play(FadeIn(gate), FadeIn(rows[0]), run_time=0.7)
        steps = VGroup(T("inherited variation", 30, TEAL), T("chosen breeders", 30, TEAL),
                       T("offspring", 30, GREEN)).arrange(RIGHT, buff=0.75).move_to([0, 3.10, 0])
        self.at("inherited variation")
        self.play(FadeIn(steps[0]), run_time=0.35)
        self.at("chosen breeders")
        self.play(FadeIn(steps[1]), Indicate(gate, color=TEAL), run_time=0.45)
        self.at("then offspring")
        self.play(FadeIn(steps[2]), FadeIn(rows[1]), run_time=0.6)
        self.at("Across generations")
        self.play(rows.animate.shift(UP * 0.55), FadeIn(rows[2]), run_time=1.2)
        self.at("The trait shifts")
        self.play(Indicate(rows[2], color=GREEN, scale_factor=1.05), run_time=0.9)
        self.at("This is artificial selection")
        loop = CurvedArrow([-4.6, -2.45, 0], [4.6, -2.45, 0], angle=-0.45,
                           color=TEAL, stroke_width=5)
        loop_label = T("artificial selection", 36, TEAL, weight=BOLD).move_to([0, -2.75, 0])
        self.play(Create(loop), FadeIn(loop_label), run_time=0.9)
        self.at("plants or animals")
        animal = VGroup(Circle(radius=0.27, color=GREY),
                        Triangle(color=GREY, fill_color=GREY, fill_opacity=1).scale(0.11).move_to([-0.16, 0.26, 0]),
                        Triangle(color=GREY, fill_color=GREY, fill_opacity=1).scale(0.11).move_to([0.16, 0.26, 0]))
        icons = VGroup(plant("strong", 0.55), animal).arrange(RIGHT, buff=0.45).move_to([4.9, -2.75, 0])
        self.play(FadeIn(icons), run_time=0.6)
        self.finish()


class S08Compare(SpokenScene):
    def construct(self):
        tp = TwoPanel("natural selection", "artificial selection", colors=(BLUE, TEAL), size=32)
        left = filter_card("natural", [-3.3, 0.1, 0], 0.90, title=False)
        right = filter_card("artificial", [3.3, 0.1, 0], 0.90, title=False)
        tp.put(left, "left")
        tp.put(right, "right")
        pulse(left.box, base=3, amp=0.8, speed=1.4)
        pulse(right.box, base=3, amp=0.8, speed=1.7)
        bob(left.output, amp=0.10, speed=1.25, seed=2)
        bob(right.output, amp=0.10, speed=1.35, seed=5)
        self.at("Bring back the moth filter")
        self.play(FadeIn(tp), FadeIn(left), run_time=0.9)
        self.at("In natural selection")
        # Let the condition filter visibly sort across the full explanatory sentence.
        self.play(left.animate.shift(RIGHT * 0.18), run_time=1.5)
        self.play(left.animate.shift(LEFT * 0.36), run_time=1.5)
        self.play(left.animate.shift(RIGHT * 0.36), run_time=1.5)
        self.play(left.animate.shift(LEFT * 0.18), run_time=1.5)
        self.at("In artificial selection")
        self.play(FadeIn(right), Indicate(right.cause, color=TEAL, scale_factor=1.10), run_time=0.9)
        shared = caption("inherited variation  →  shifted population", size=32, color=GREEN)
        self.at("Both can shift")
        self.play(FadeIn(shared), Indicate(VGroup(left.output, right.output), color=GREEN, scale_factor=1.06), run_time=1.0)
        self.at("Neither process changes")
        no_change = T("no organism changes during life", 30, TEXT, weight=BOLD).move_to([0, -3.17, 0])
        self.play(FadeOut(shared), FadeIn(no_change), run_time=0.7)
        self.play(Indicate(no_change, color=TEXT, scale_factor=1.04), run_time=0.7)
        self.finish()


class S09Time(SpokenScene):
    def construct(self):
        board = RoundedRectangle(width=12.25, height=6.0, corner_radius=0.24,
                                 stroke_width=0, fill_color=BOARD, fill_opacity=1)
        self.add(board)
        top = population_strip(1.25, [1, 2, 3, 3], x0=-3.9, width=8.3, icon="moth")
        low = population_strip(-1.0, [1, 2, 2, 3], x0=-3.9, width=8.3, icon="plant")
        heads = VGroup(T("natural", 30, BLUE, weight=BOLD).move_to([-5.6, 1.25, 0]),
                       T("artificial", 30, TEAL, weight=BOLD).move_to([-5.6, -1.0, 0]))
        for i, g in enumerate(VGroup(*top, *low)):
            bob(g, amp=0.09, speed=1.2, seed=i)
        arrows = VGroup(Arrow([-4.8, 2.35, 0], [4.9, 2.35, 0], buff=0, color=GREEN, stroke_width=5),
                        Arrow([-4.8, -2.05, 0], [4.9, -2.05, 0], buff=0, color=GREEN, stroke_width=5))
        self.at("Both processes can shift")
        self.play(FadeIn(heads), FadeIn(top[0]), FadeIn(low[0]), GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.15) for g in top[1:]], lag_ratio=0.22),
                  LaggedStart(*[FadeIn(g, shift=RIGHT * 0.15) for g in low[1:]], lag_ratio=0.22), run_time=1.8)
        self.at("while big changes")
        many = T("many generations", 32, GREEN, weight=BOLD).move_to([0, 3.08, 0])
        self.play(FadeIn(many), arrows.animate.set_stroke(width=7), run_time=0.7)
        self.at("Inherited variation must")
        sparkle = VGroup(*[Line(ORIGIN, d * 0.28, color=YELLOW, stroke_width=4) for d in (UP, DOWN, LEFT, RIGHT, UR, UL, DR, DL)])
        sparkle.move_to([-5.0, 0.05, 0])
        variant = moth("dark", 0.40).move_to([-4.35, 0.05, 0])
        self.play(Create(sparkle), FadeIn(variant, scale=0.4), run_time=0.8)
        first = T("variation first", 32, YELLOW, weight=BOLD).move_to([-2.5, -3.05, 0])
        sort = T("selection sorts it", 32, TEAL, weight=BOLD).move_to([2.5, -3.05, 0])
        self.at("before selection can sort")
        self.play(FadeIn(first), GrowArrow(Arrow(first.get_right(), sort.get_left(), buff=0.18,
                                                color=GREY, stroke_width=4)), FadeIn(sort), run_time=1.0)
        pulse(sparkle, base=4, amp=1.4, speed=2.0)
        self.finish()


class S10Adaptation(SpokenScene):
    def construct(self):
        bark = RoundedRectangle(width=10.6, height=4.5, corner_radius=0.22, stroke_color=GREY,
                                stroke_width=3, fill_color=SOOT, fill_opacity=1).move_to([0, -0.25, 0])
        dark = moth("dark", 2.4).move_to([0, -0.15, 0])
        pulse(bark, base=3, amp=0.8, speed=1.4)
        bob(dark, amp=0.11, speed=1.25, seed=3)
        self.at("Natural selection also")
        self.play(FadeIn(bark), FadeIn(dark, scale=0.6), run_time=0.9)
        outline = Circle(radius=1.35, color=GREEN, stroke_width=7).move_to(dark)
        self.play(Create(outline), run_time=0.6)
        labels = VGroup(T("structure", 30, TEAL), T("function", 30, TEAL), T("behaviour", 30, TEAL))
        labels[0].move_to([-3.5, 1.5, 0]); labels[1].move_to([3.5, 1.5, 0]); labels[2].move_to([0, -2.25, 0])
        self.at("An adaptation is")
        self.play(FadeIn(labels[0]), run_time=0.4)
        self.at("function")
        self.play(FadeIn(labels[1]), run_time=0.4)
        self.at("behavior shaped")
        self.play(FadeIn(labels[2]), run_time=0.4)
        shaped = T("adaptation shaped by natural selection", 34, GREEN, weight=BOLD).move_to([0, 3.05, 0])
        self.at("helps survival")
        self.play(FadeIn(shaped), Indicate(outline, color=GREEN, scale_factor=1.05), run_time=0.8)
        self.at("Its value depends")
        pale_bark = bark.copy().set_fill(LICHEN, 1)
        self.play(Transform(bark, pale_bark), FadeOut(outline), run_time=1.0)
        environment = T("value depends on environment", 34, TEXT, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeOut(labels), FadeIn(environment), run_time=0.7)
        self.finish()


class S11Evolution(SpokenScene):
    def construct(self):
        board = RoundedRectangle(width=12.25, height=6.0, corner_radius=0.24,
                                 stroke_width=0, fill_color=BOARD, fill_opacity=1)
        self.add(board)
        natural = population_strip(1.15, [1, 2, 3, 4], x0=-3.9, width=8.3, icon="moth")
        artificial = population_strip(-1.15, [1, 2, 3, 4], x0=-3.9, width=8.3, icon="plant")
        labels = VGroup(T("natural selection", 28, BLUE, weight=BOLD).move_to([-3.25, 3.05, 0]),
                        T("artificial selection", 28, TEAL, weight=BOLD).move_to([3.25, 3.05, 0]))
        for i, g in enumerate(VGroup(*natural, *artificial)):
            bob(g, amp=0.09, speed=1.2, seed=i)
        timeline = Arrow([-5.4, -2.45, 0], [6.15, -2.45, 0], buff=0, color=GREY,
                         stroke_width=4, tip_length=0.25)
        generations = T("generations", 30, GREY).next_to(timeline, DOWN, buff=0.15)
        self.add(labels, natural[0], artificial[0])
        self.at("Evolution is change")
        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.12) for g in natural[1:]], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(g, shift=RIGHT * 0.12) for g in artificial[1:]], lag_ratio=0.15), run_time=1.8)
        brace = BraceBetweenPoints([-4.9, 2.35, 0], [4.9, 2.35, 0], direction=UP, color=GREEN)
        evo = T("evolution", 38, GREEN, weight=BOLD).next_to(brace, UP, buff=0.12)
        self.play(Create(brace), FadeIn(evo), GrowArrow(timeline), FadeIn(generations), run_time=0.9)
        self.at("Natural selection is")
        highlight = SurroundingRectangle(natural, color=BLUE, buff=0.18, stroke_width=5)
        self.play(Create(highlight), run_time=0.6)
        self.at("produces adaptations")
        adapt = chip("adaptations", GREEN, 30).move_to([5.3, -0.05, 0])
        link = Arrow(highlight.get_corner(DR) + LEFT * 0.9, adapt.get_top(), buff=0.12, color=GREEN, stroke_width=5)
        self.play(GrowArrow(link), FadeIn(adapt), run_time=0.8)
        self.at("Big changes usually")
        self.play(timeline.animate.shift(RIGHT * 0.45), natural.animate.shift(LEFT * 0.2),
                  artificial.animate.shift(LEFT * 0.2), run_time=1.2)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        left = filter_card("natural", [-3.3, 0.5, 0], 0.92)
        right = filter_card("artificial", [3.3, 0.5, 0], 0.92)
        left.remove(left.cause)
        right.remove(right.cause)
        pulse(left.box, base=3, amp=0.8, speed=1.5)
        pulse(right.box, base=3, amp=0.8, speed=1.8)
        bob(left.output, amp=0.10, speed=1.25, seed=2)
        bob(right.output, amp=0.10, speed=1.35, seed=5)
        self.at("The shared pattern")
        self.play(FadeIn(left), FadeIn(right), run_time=0.9)
        shared = RoundedRectangle(width=12.4, height=0.75, corner_radius=0.18, stroke_color=GREEN,
                                  stroke_width=4, fill_color=GREEN, fill_opacity=0.10).move_to([0, -2.72, 0])
        shared_text = T("unequal reproduction  →  inherited population change", 31, GREEN, weight=BOLD).move_to(shared)
        shared.layout_ok = True  # Summary text intentionally sits inside its own path box.
        self.play(Create(shared), FadeIn(shared_text), run_time=0.8)
        self.at("The important difference")
        causes = VGroup(T("environmental conditions", 30, BLUE, weight=BOLD).move_to([-3.3, 3.15, 0]),
                        T("people's choices", 30, TEAL, weight=BOLD).move_to([3.3, 3.15, 0]))
        self.play(FadeIn(causes), run_time=0.7)
        self.at("In artificial selection")
        self.play(Indicate(right, color=TEAL, scale_factor=1.03), run_time=0.8)
        self.at("People shift inherited")
        selected = VGroup(plant("strong", 0.70), plant("strong", 0.70), plant("less", 0.70)).arrange(RIGHT, buff=0.45)
        selected.move_to([3.3, -0.6, 0])
        path = Arrow([3.3, 0.35, 0], selected.get_top(), buff=0.1, color=TEAL, stroke_width=6)
        self.play(GrowArrow(path), FadeIn(selected, shift=DOWN * 0.2), run_time=1.0)
        self.at("choosing which organisms reproduce")
        self.play(Indicate(selected, color=TEAL, scale_factor=1.08), run_time=0.9)
        self.finish()


class S13End(EndCard):
    LINE = "People shift inherited traits by choosing which organisms reproduce."
