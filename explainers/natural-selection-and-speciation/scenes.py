"""The Drought Sorts a Population.

COLOR MAP
  BLUE   shallow beaks
  YELLOW middle beaks
  GREEN  deep beaks / the higher-survival group in this drought
  WHITE  barriers, measurements, tests, and neutral evidence
  GOLD   drought / hard seeds / prediction prompt

All distributions are categorical counts computed from the token lists shown on screen. They are
labelled schematic because the three colour bins are an explanatory model, not the Grant data.
"""
from bp_parts import *


DRY = GOLD
SOFT = "#B98A58"
ISLAND = "#8EA89A"
SHALLOW, MIDDLE, DEEP = BLUE, YELLOW, GREEN
COLORS = (SHALLOW, MIDDLE, DEEP)
START_COUNTS = (4, 5, 3)
SURVIVOR_COUNTS = (1, 2, 4)
NEXT_COUNTS = (2, 3, 6)


def finch(kind=1, scale=1.0, band=None, facing=RIGHT):
    """One schematic finch; beak height is fixed by category and never changes."""
    color = COLORS[kind]
    body = Ellipse(width=0.92, height=0.64, stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.42)
    head = Circle(radius=0.25, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=0.42).move_to(body.get_center() + RIGHT * 0.42 + UP * 0.12)
    heights = (0.16, 0.25, 0.36)
    h = heights[kind]
    beak = Polygon([0, -h / 2, 0], [0, h / 2, 0], [0.46, 0, 0],
                   stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.9)
    beak.next_to(head, RIGHT, buff=-0.02)
    eye = Dot(head.get_center() + RIGHT * 0.07 + UP * 0.06, radius=0.035, color=TEXT)
    leg = Line(body.get_bottom() + RIGHT * 0.05, body.get_bottom() + DOWN * 0.23 + RIGHT * 0.05,
               color=TEXT, stroke_width=2.5)
    g = VGroup(body, head, beak, eye, leg)
    if band is not None:
        ring = Rectangle(width=0.18, height=0.11, stroke_color=TEXT, stroke_width=2,
                         fill_color=BG, fill_opacity=1).move_to(leg.get_center())
        number = T(str(band), 22, TEXT).next_to(g, DOWN, buff=0.08)
        g.add(ring, number)
        g.band = ring
    if facing is LEFT:
        g.flip(RIGHT)
    g.kind, g.beak = kind, beak
    return g.scale(scale)


def island_base(dry=True):
    """The carried Daphne Major landscape, always at the same scale and position."""
    sea = Line([-6.4, -1.75, 0], [6.4, -1.75, 0], color=BLUE, stroke_width=4)
    land = VMobject(stroke_color=ISLAND, stroke_width=4, fill_color=ISLAND, fill_opacity=0.40)
    land.set_points_smoothly([
        [-5.8, -1.72, 0], [-4.5, -0.75, 0], [-2.9, -0.35, 0], [-1.1, 0.75, 0],
        [0.5, 0.30, 0], [2.1, 1.02, 0], [3.6, 0.15, 0], [5.5, -1.72, 0],
    ])
    land.add_line_to(np.array([-5.8, -1.72, 0.0]))
    wind = VGroup(*[
        Arrow([-6.1 + i * 0.3, y, 0], [-4.8 + i * 0.3, y, 0], buff=0, color=DRY,
              stroke_width=2.5, tip_length=0.14).set_opacity(0.55)
        for i, y in enumerate((2.25, 1.75, 1.25))
    ])
    if not dry:
        wind.set_opacity(0)
    return VGroup(sea, land, wind)


FLOCK_POS = [
    (-4.6, 0.45), (-3.3, 1.45), (-2.0, 0.35), (-0.8, 1.45),
    (0.5, 0.30), (1.7, 1.55), (3.0, 0.45), (4.35, 1.35),
    (-3.7, -0.65), (-1.35, -0.70), (1.1, -0.65), (3.55, -0.60),
]
START_KINDS = [0, 1, 0, 2, 1, 0, 1, 2, 0, 1, 2, 1]


def flock(kinds=START_KINDS, scale=0.72, bands=False):
    birds = VGroup()
    for i, kind in enumerate(kinds):
        b = finch(kind, scale=scale, band=(i + 21 if bands else None))
        b.move_to([*FLOCK_POS[i % len(FLOCK_POS)], 0])
        birds.add(b)
    return birds


def distribution(counts, center=(0, -2.55, 0), width=7.2, height=1.35, title="beak depth"):
    """A computed three-bin count display; bar heights derive only from counts."""
    c = np.array(center, dtype=float)
    x0 = c[0] - width / 2
    y0 = c[1] - height / 2 + 0.12
    axis = Line([x0, y0, 0], [x0 + width, y0, 0], color=TEXT, stroke_width=2.5)
    max_n = max(counts)
    bars = VGroup()
    xs = np.linspace(x0 + 1.05, x0 + width - 1.05, 3)
    for n, x, color in zip(counts, xs, COLORS):
        h = 0.22 + (height - 0.48) * n / max_n
        bar = RoundedRectangle(corner_radius=0.06, width=1.05, height=h, stroke_color=color,
                               stroke_width=2.5, fill_color=color, fill_opacity=0.55)
        bar.move_to([x, y0 + h / 2, 0])
        bars.add(bar)
    labels = VGroup(T("shallow", 24, SHALLOW), T("middle", 24, MIDDLE), T("deep", 24, DEEP))
    for lab, x in zip(labels, xs):
        lab.next_to([x, y0, 0], DOWN, buff=0.12)
    # The three category labels identify the x variable. A separate heading here would sit on the
    # carried island shoreline, so the scene narration supplies before/survivor/young context.
    g = VGroup(axis, bars, labels)
    g.bars = bars
    return g


def caliper(at=(0, 0, 0), scale=1.0):
    rail = Line(LEFT * 0.55, RIGHT * 0.55, color=TEXT, stroke_width=5)
    jaws = VGroup(Line(rail.get_left(), rail.get_left() + UP * 0.48, color=TEXT, stroke_width=4),
                  Line(rail.get_right(), rail.get_right() + UP * 0.48, color=TEXT, stroke_width=4))
    return VGroup(rail, jaws).scale(scale).move_to(at)


def seed(size="hard", at=ORIGIN):
    if size == "soft":
        return Ellipse(width=0.32, height=0.22, color=SOFT, stroke_width=2.5,
                       fill_color=SOFT, fill_opacity=0.7).move_to(at).rotate(0.35)
    return RoundedRectangle(corner_radius=0.22, width=0.65, height=0.58, color=DRY, stroke_width=3,
                            fill_color=DRY, fill_opacity=0.35).move_to(at).rotate(0.25)


def seed_world(question=False):
    base = island_base(True)
    kinds = [0, 1, 2, 0, 1, 2]
    birds = flock(kinds, scale=0.76)
    hard = VGroup(*[seed("hard", [x, y, 0]) for x, y in ((-4.8, -0.8), (-1.8, -0.8), (1.6, -0.75), (4.5, -0.8))])
    pic = VGroup(base, birds, hard)
    if question:
        q = question_card("Which birds contribute more young to the next generation?", y=-3.12,
                          size=28, max_w=10.4)
        pic.add(q)
    return pic


def gene_block(letter, color):
    box = RoundedRectangle(corner_radius=0.12, width=1.15, height=0.72, stroke_color=color,
                           stroke_width=3, fill_color=color, fill_opacity=0.18)
    label = T(letter, 28, color).move_to(box)
    return VGroup(box, label)


class S00Title(TitleCard):
    LESSON = "Natural Selection and New Species"
    TITLE = "The Drought Sorts a Population"


class S01Puzzle(SpokenScene):
    def construct(self):
        world = island_base(True)
        birds = flock()
        bob(birds[1], amp=0.05, speed=1.7)
        bob(birds[6], amp=0.04, speed=1.9, seed=2)
        self.add(world, birds)
        q = fit_text("Reshaped birds — or changed who remained?", max_w=10.5, size=38,
                     color=GOLD).move_to([0, 3.15, 0])
        self.at("Did the drought")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)

        place = T("Daphne Major", 34, TEXT).move_to([0, 3.15, 0])
        self.at("On Daphne Major")
        self.play(swap(q, place), run_time=0.7)
        doomed = VGroup(*[birds[i] for i in (0, 2, 4, 5, 8, 9, 11)])
        self.at("most medium ground")
        self.play(doomed.animate.set_opacity(0.12).shift(DOWN * 0.18), run_time=1.25)

        cal = caliper([4.9, 2.2, 0], 1.25)
        measured = T("measured before", 28, TEXT).move_to([4.9, 3.0, 0])
        self.at("Researchers had measured")
        self.play(FadeIn(cal), FadeIn(measured), birds.animate.shift(LEFT * 0.24), run_time=0.75)
        self.play(cal.animate.shift(LEFT * 8.6), run_time=1.15, rate_func=linear)

        before = distribution(START_COUNTS, center=(-3.3, -2.45, 0), width=5.4, height=1.35, title="before")
        after = distribution(SURVIVOR_COUNTS, center=(3.25, -2.45, 0), width=5.4, height=1.35, title="survivors")
        tags = VGroup(T("schematic", 24, GREY).move_to([5.7, 3.35, 0]))
        self.at("The survivors")
        self.play(FadeOut(doomed), FadeOut(cal), FadeOut(measured), FadeIn(before), FadeIn(after), FadeIn(tags),
                  run_time=1.1)
        arrow = Arrow([-0.35, -2.25, 0], [0.35, -2.25, 0], color=TEXT, buff=0, tip_length=0.2)
        self.play(GrowArrow(arrow), after.bars[2].animate.set_fill(GREEN, opacity=0.9), run_time=0.75)

        watch = caption("The population changed; no adult changed its beak.", size=32, color=TEXT, y=2.75)
        self.at("Watch the population")
        self.play(swap(place, watch), run_time=0.7)
        self.finish()


class S02Variation(SpokenScene):
    def construct(self):
        birds = flock()
        base = island_base(True)
        dist = distribution(START_COUNTS, center=(0, -2.55, 0), width=7.0, height=1.35)
        self.add(base, birds)
        self.at("Before the drought")
        self.play(FadeIn(dist), run_time=0.85)

        specimen = birds[7]
        measure = DoubleArrow(specimen.beak.get_top() + RIGHT * 0.18, specimen.beak.get_bottom() + RIGHT * 0.18,
                              color=TEXT, buff=0, tip_length=0.11, stroke_width=3)
        depth = T("beak depth", 28, TEXT).move_to([5.15, 2.35, 0])
        self.at("Beak depth is")
        self.play(Create(measure), FadeIn(depth), birds.animate.shift(UP * 0.18), run_time=0.7)

        targets = []
        for kind, x in zip((0, 1, 2), (-3.5, 0, 3.5)):
            indices = [i for i, k in enumerate(START_KINDS) if k == kind]
            for j, i in enumerate(indices):
                targets.append((birds[i], [x + (j - (len(indices)-1)/2) * 0.72, 0.65 + 0.32 * (j % 2), 0]))
        self.at("Blue birds")
        self.play(*[b.animate.move_to(p) for b, p in targets if b.kind == 0], run_time=0.8)
        self.at("yellow birds")
        self.play(*[b.animate.move_to(p) for b, p in targets if b.kind == 1], run_time=0.8)
        self.at("green birds")
        self.play(*[b.animate.move_to(p) for b, p in targets if b.kind == 2], run_time=0.8)
        label = T("variation before drought", 34, TEXT).move_to([0, 2.8, 0])
        self.at("These differences existed")
        self.play(FadeOut(measure), FadeOut(depth), FadeIn(label), run_time=0.75)
        self.play(LaggedStart(*[Indicate(b.beak, color=COLORS[b.kind], scale_factor=1.18) for b in birds],
                              lag_ratio=0.08), run_time=1.4)
        rule = caption("Variation gives the environment something to sort.", size=32, color=GOLD)
        self.at("Variation gives")
        self.play(FadeOut(dist), FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S03Seeds(SpokenScene):
    def construct(self):
        base = island_base(True)
        birds = flock([0, 1, 2, 0, 1, 2], scale=0.78)
        dist = distribution(START_COUNTS, center=(0, -2.55, 0), width=6.7, height=1.2)
        soft = VGroup(*[seed("soft", [x, y, 0]) for x, y in ((-5, -0.75), (-3.7, -0.9), (-2.4, -0.65),
                                                                       (-0.6, -0.8), (1.0, -0.65), (2.5, -0.9), (4.1, -0.7))])
        hard = VGroup(*[seed("hard", [x, y, 0]) for x, y in ((-4.4, -0.65), (-1.5, -0.75), (1.8, -0.7), (4.6, -0.65))])
        self.add(base, birds, dist, soft, hard, scope_tag("schematic"))
        self.at("Then drought")
        self.play(base[2].animate.set_opacity(0.95), soft.animate.shift(RIGHT * 0.25), run_time=0.8)
        self.at("Small soft seeds")
        self.play(LaggedStart(*[FadeOut(s, scale=0.4) for s in soft], lag_ratio=0.08),
                  birds.animate.shift(LEFT * 0.24), run_time=1.2)
        self.at("while large")
        self.play(LaggedStart(*[Indicate(s, color=DRY, scale_factor=1.18) for s in hard], lag_ratio=0.12), run_time=0.9)

        greens = VGroup(*[b for b in birds if b.kind == 2])
        self.at("Deeper beaks")
        self.play(*[b.animate.shift(DOWN * 0.28) for b in greens], run_time=0.6)
        crack = VGroup(Line([-0.15, -0.18, 0], [0.08, 0.08, 0], color=TEXT, stroke_width=3),
                       Line([0.08, 0.08, 0], [0.2, -0.13, 0], color=TEXT, stroke_width=3))
        crack.move_to(hard[2])
        self.play(Create(crack), hard[2].animate.scale(1.12), run_time=0.6)

        q = question_card("Which birds contribute more young to the next generation?", y=-3.12,
                          size=28, max_w=10.4)
        self.at("Which birds do")
        self.play(FadeOut(dist), FadeIn(q), run_time=0.85)
        self.at("Follow the colors")
        self.play(birds.animate.shift(UP * 0.22), run_time=1.1)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Which birds contribute more young to the next generation?"
    SECONDS = 4.5
    CARD = {"y": -3.12, "size": 28, "max_w": 10.4}

    def backdrop(self):
        pic = seed_world(False)
        for i, b in enumerate(pic[1]):
            bob(b, amp=0.035, speed=1.4 + 0.12 * i, seed=i)
        return pic


class S05Survival(SpokenScene):
    def construct(self):
        base = island_base(True)
        kinds = [0, 1, 1, 2, 2, 2, 2]
        birds = flock(kinds, scale=0.82)
        self.add(base)
        self.at("More green birds")
        self.play(LaggedStart(*[FadeIn(b, scale=0.7) for b in birds], lag_ratio=0.10), run_time=1.25)
        colors = VGroup(T("blue remains", 28, BLUE), T("yellow remains", 28, YELLOW), T("more green", 28, GREEN))
        colors.arrange(RIGHT, buff=0.7).move_to([0, 2.75, 0])
        self.at("but some birds")
        self.play(FadeIn(colors), run_time=0.7)

        before = distribution(START_COUNTS, center=(-3.35, -2.45, 0), width=5.2, height=1.3, title="before")
        after = distribution(SURVIVOR_COUNTS, center=(3.25, -2.45, 0), width=5.2, height=1.3, title="survivors")
        self.at("The groups overlap")
        tag = T("schematic", 24, GREY).move_to([5.7, 3.35, 0])
        self.play(FadeIn(before), FadeIn(after), FadeIn(tag), run_time=0.9)
        self.play(LaggedStart(*[Indicate(after.bars[i], color=COLORS[i], scale_factor=1.08) for i in range(3)],
                              lag_ratio=0.2), run_time=0.8)

        better = T("better chance here", 34, GREEN).move_to([0, 2.82, 0])
        self.at("A deep beak")
        self.play(swap(colors, better), run_time=0.65)
        chance = ValueTracker(0.48)
        gauge = dial(chance, center=[5.1, 1.65, 0], radius=0.8, label="chance", color=GREEN, size=28)
        self.play(FadeIn(gauge), chance.animate.set_value(0.78), run_time=1.0)
        not_certain = T("not guaranteed", 32, TEXT).move_to([0, 2.82, 0])
        self.at("It does not")
        self.play(swap(better, not_certain), chance.animate.set_value(0.68), run_time=0.7)
        depends = caption("Helpful depends on the present environment.", size=32, color=GOLD)
        self.at("A helpful trait")
        self.play(FadeOut(before), FadeOut(after), FadeOut(tag), FadeIn(depends, shift=UP * 0.1),
                  base[2].animate.set_opacity(0.8), run_time=0.8)
        self.finish()


class S06Inheritance(SpokenScene):
    def construct(self):
        before = distribution(START_COUNTS, center=(-3.45, -2.45, 0), width=5.0, height=1.3, title="starting")
        after = distribution(NEXT_COUNTS, center=(3.35, -2.45, 0), width=5.0, height=1.3, title="young")
        survivors = VGroup(finch(0, 0.95), finch(1, 0.95), finch(2, 0.95), finch(2, 0.95), finch(2, 0.95))
        survivors.arrange(RIGHT, buff=0.72).move_to([0, 1.7, 0])
        bob(survivors[0], amp=0.16, speed=1.2)
        tag = T("schematic", 24, GREY).move_to([5.7, 3.35, 0])
        self.add(before, tag)
        self.at("Survival alone")
        self.play(FadeIn(survivors), run_time=0.9)
        unfinished = T("survival is not the finish", 34, TEXT).move_to([0, 3.0, 0])
        self.play(FadeIn(unfinished), run_time=0.6)

        parents = VGroup(survivors[1], survivors[2], survivors[3], survivors[4])
        pairs = VGroup(SurroundingRectangle(VGroup(parents[0], parents[1]), buff=0.18, color=TEXT, corner_radius=0.12),
                       SurroundingRectangle(VGroup(parents[2], parents[3]), buff=0.18, color=TEXT, corner_radius=0.12))
        inherited = T("young tend to resemble parents", 32, TEXT).move_to([0, 3.0, 0])
        self.at("Beak size is")
        self.play(FadeIn(pairs), swap(unfinished, inherited), run_time=0.8)
        self.at("so parents and")
        self.play(LaggedStart(*[Indicate(p, color=COLORS[p.kind], scale_factor=1.12) for p in parents], lag_ratio=0.15),
                  run_time=1.0)

        self.at("The survivors breed")
        self.play(pairs[0].animate.set_stroke(YELLOW, width=5), pairs[1].animate.set_stroke(GREEN, width=5), run_time=0.7)
        young_kinds = [1, 2, 2, 2, 1, 2]
        young = VGroup(*[finch(k, 0.58) for k in young_kinds]).arrange(RIGHT, buff=0.33).move_to([0, 0.3, 0])
        arrows = VGroup(Arrow([-2.0, 1.25, 0], [-1.25, 0.65, 0], color=TEXT, buff=0.05, tip_length=0.16),
                        Arrow([2.0, 1.25, 0], [1.25, 0.65, 0], color=TEXT, buff=0.05, tip_length=0.16))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  LaggedStart(*[FadeIn(b, scale=0.5) for b in young], lag_ratio=0.12), run_time=1.3)

        self.at("Their young form")
        self.play(FadeIn(after), run_time=0.85)
        self.at("now with deeper")
        self.play(after.bars[2].animate.set_fill(GREEN, opacity=0.9),
                  LaggedStart(*[Indicate(b, color=COLORS[b.kind], scale_factor=1.12) for b in young], lag_ratio=0.1),
                  run_time=1.1)
        across = caption("Change across generations — not within one life.", size=32, color=GOLD)
        self.at("That makes change")
        self.play(FadeOut(before), FadeOut(after), FadeOut(tag), FadeIn(across), run_time=0.75)
        self.at("not within")
        self.play(LaggedStart(*[Indicate(b.beak, color=COLORS[b.kind], scale_factor=1.1) for b in survivors],
                              lag_ratio=0.12), run_time=0.9)
        self.finish()


class S07Evidence(SpokenScene):
    def construct(self):
        panels = TwoPanel("measured before", "checked later", colors=(TEXT, TEXT), top=3.0, bottom=-2.35)
        birds = VGroup(finch(0, 1.0, 21), finch(1, 1.0, 34), finch(2, 1.0, 57))
        birds.arrange(DOWN, buff=0.30).move_to([-3.25, 0.0, 0])
        bob(birds[0], amp=0.16, speed=1.15)
        self.add(panels)
        no_guess = T("not a guess", 34, TEXT).move_to([0, 3.35, 0])
        self.at("Researchers did not")
        self.play(FadeIn(no_guess), run_time=0.6)
        self.at("Each measured bird")
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in birds], lag_ratio=0.16), run_time=1.0)
        self.play(LaggedStart(*[Indicate(b.band, color=TEXT, scale_factor=1.3) for b in birds], lag_ratio=0.2), run_time=0.9)

        checked = birds.copy()
        checked[0].set_opacity(0.12)
        checked.move_to([3.25, 0.2, 0])
        self.at("Later the team")
        self.play(TransformFromCopy(birds, checked), run_time=1.1)
        checkmarks = VGroup(T("not found", 25, TEXT).next_to(checked[0], RIGHT, buff=0.2),
                            T("found", 25, TEXT).next_to(checked[1], RIGHT, buff=0.2),
                            T("found", 25, TEXT).next_to(checked[2], RIGHT, buff=0.2))
        self.play(FadeIn(checkmarks), run_time=0.7)

        surv = T("survival evidence", 32, GREEN).move_to([0, 3.35, 0])
        self.at("Comparing the groups")
        self.play(swap(no_guess, surv), run_time=0.65)
        self.play(Indicate(VGroup(birds, checked), color=TEXT, scale_factor=1.03), run_time=0.9)
        association = caption("Association, not a promise about every bird.", size=31, color=TEXT)
        self.at("It shows an")
        self.play(FadeIn(association), run_time=0.7)

        parent = finch(2, 1.15).move_to([-1.1, 0.0, 0])
        child = finch(2, 0.8).move_to([1.2, 0.0, 0])
        arrow = Arrow(parent.get_right(), child.get_left(), color=TEXT, buff=0.12, tip_length=0.18)
        inherit = T("inheritance evidence", 32, TEXT).move_to([0, -1.35, 0])
        self.at("Parents and young")
        self.play(FadeOut(VGroup(association, panels, birds, checked, checkmarks)), FadeIn(parent),
                  GrowArrow(arrow), FadeIn(child), FadeIn(inherit), run_time=1.0)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        title = T("NATURAL SELECTION", 42, TEXT, weight=BOLD).move_to([0, 3.15, 0])
        self.at("This is natural")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        xs = (-4.2, 0, 4.2)
        variation = VGroup(finch(0, 0.8), finch(1, 0.8), finch(2, 0.8)).arrange(RIGHT, buff=0.25).move_to([xs[0], 0.8, 0])
        parents = VGroup(finch(2, 0.82), finch(2, 0.55)).arrange(DOWN, buff=0.35).move_to([xs[1], 0.8, 0])
        offspring = VGroup(finch(0, 0.55), finch(2, 0.55), finch(2, 0.55), finch(2, 0.55)).arrange_in_grid(2, 2, buff=0.28).move_to([xs[2], 0.8, 0])
        bob(offspring[0], amp=0.16, speed=1.1)
        labels = VGroup(T("variation", 30, TEXT), T("inheritance", 30, TEXT), T("unequal offspring", 30, TEXT))
        for lab, x in zip(labels, xs): lab.move_to([x, -0.55, 0])
        arrows = VGroup(Arrow([variation.get_right()[0] + 0.15, 0.8, 0], [parents.get_left()[0] - 0.2, 0.8, 0], color=TEXT, buff=0, tip_length=0.2),
                        Arrow([1.45, 0.8, 0], [2.65, 0.8, 0], color=TEXT, buff=0, tip_length=0.2))
        self.at("It needs variation")
        self.play(FadeIn(variation), FadeIn(labels[0]), run_time=0.75)
        self.at("inheritance")
        self.play(GrowArrow(arrows[0]), FadeIn(parents), FadeIn(labels[1]), run_time=0.75)
        self.at("unequal reproductive")
        self.play(GrowArrow(arrows[1]), FadeIn(offspring), FadeIn(labels[2]), run_time=0.85)

        rule = fit_text("Inherited traits spread when their carriers leave more reproducing offspring.",
                        max_w=11.8, size=38, color=GOLD, max_lines=2).move_to([0, -2.05, 0])
        self.at("Inherited traits spread")
        self.play(FadeIn(rule, shift=UP * 0.1), VGroup(variation, parents, offspring).animate.shift(UP * 0.18),
                  run_time=0.8)
        self.play(LaggedStart(*[Indicate(b, color=GREEN, scale_factor=1.12) for b in offspring[1:]], lag_ratio=0.15),
                  run_time=1.2)
        fitness = caption("Fitness = contribution to the next generation", size=32, color=TEXT)
        self.at("Fitness means")
        self.play(swap(rule, fitness), run_time=0.7)
        no = VGroup(T("strength", 28, GREY), T("health", 28, GREY), T("long life", 28, GREY)).arrange(RIGHT, buff=0.9).move_to([0, -2.0, 0])
        for label in no:
            label.layout_ok = True  # Deliberate strike-through: these are explicitly not fitness.
        crosses = VGroup(*[Cross(x, stroke_color=TEXT, stroke_width=4, scale_factor=1.1) for x in no])
        self.at("It does not")
        self.play(FadeOut(fitness), FadeIn(no), Create(crosses), run_time=0.8)
        self.finish()


class S09Sources(SpokenScene):
    def construct(self):
        mutation = VGroup(*[gene_block(x, c) for x, c in zip(("A", "B", "C"), (BLUE, YELLOW, GREEN))])
        mutation.arrange(RIGHT, buff=0.25).move_to([-3.6, 1.35, 0])
        mlabel = T("mutation", 32, TEXT).move_to([-3.6, 2.55, 0])
        self.at("Mutation supplies")
        self.play(FadeIn(mutation), FadeIn(mlabel), run_time=0.8)
        changed = gene_block("B′", GREEN).move_to(mutation[1])
        self.play(ReplacementTransform(mutation[1], changed), run_time=0.7)

        parent1 = VGroup(gene_block("A", BLUE), gene_block("B", YELLOW)).arrange(RIGHT, buff=0.15)
        parent2 = VGroup(gene_block("B", YELLOW), gene_block("C", GREEN)).arrange(RIGHT, buff=0.15)
        parent1.move_to([2.8, 1.75, 0]); parent2.move_to([4.5, 0.75, 0])
        shuffle = T("sexual reproduction", 31, TEXT).move_to([3.55, 2.55, 0])
        self.at("sexual reproduction")
        self.play(FadeIn(parent1), FadeIn(parent2), FadeIn(shuffle), run_time=0.9)
        child = VGroup(gene_block("A", BLUE), gene_block("C", GREEN)).arrange(RIGHT, buff=0.15).move_to([3.6, -0.25, 0])
        self.play(TransformFromCopy(VGroup(parent1[0], parent2[1]), child), run_time=0.9)

        adult = finch(2, 1.55).move_to([-2.8, -1.0, 0])
        lock_body = RoundedRectangle(corner_radius=0.12, width=0.65, height=0.55, color=TEXT, stroke_width=3)
        lock_arc = Arc(radius=0.22, start_angle=0, angle=PI, color=TEXT, stroke_width=3).next_to(lock_body, UP, buff=-0.08)
        lock = VGroup(lock_body, lock_arc).next_to(adult.beak, RIGHT, buff=0.25)
        self.at("Selection does not")
        self.play(FadeOut(VGroup(mutation, changed, mlabel, parent1, parent2, shuffle, child)), FadeIn(adult), FadeIn(lock), run_time=0.9)
        present = VGroup(finch(0, 0.75), finch(1, 0.75), finch(2, 0.75)).arrange(RIGHT, buff=0.45).move_to([2.4, -0.7, 0])
        bob(present[0], amp=0.16, speed=1.1)
        label = T("sorts inherited variation", 32, TEXT).move_to([2.4, 0.55, 0])
        self.at("It sorts inherited")
        self.play(FadeIn(present), FadeIn(label), run_time=0.8)
        self.play(LaggedStart(*[present[i].animate.shift(UP * (0.12 + 0.12 * i)) for i in range(3)], lag_ratio=0.15),
                  run_time=0.9)
        self.at("including mutations")
        self.play(present.animate.shift(RIGHT * 0.24), lock.animate.shift(UP * 0.12), run_time=0.75)
        fixed = caption("No finch changed its own beak.", size=34, color=GOLD)
        self.at("No finch")
        self.play(FadeIn(fixed), Indicate(lock, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.finish()


class S10Scope(SpokenScene):
    def construct(self):
        base = island_base(True)
        birds = flock([0, 1, 2, 2, 1, 2], scale=0.82)
        hard = VGroup(*[seed("hard", [x, -0.75, 0]) for x in (-4.6, -1.5, 1.5, 4.6)])
        dist = distribution(NEXT_COUNTS, center=(2.8, -2.48, 0), width=5.4, height=1.28, title="young")
        self.add(base, birds, hard)
        advantage = T("advantage is not permanent", 36, GOLD).move_to([0, 3.05, 0])
        self.at("The advantage")
        self.play(FadeIn(advantage), run_time=0.7)

        rain = VGroup(*[Line([x, 2.7, 0], [x - 0.25, 2.1, 0], color=BLUE, stroke_width=3)
                        for x in np.linspace(-5.5, 5.5, 13)])
        soft = VGroup(*[seed("soft", [x, -0.65 + 0.10 * (i % 2), 0]) for i, x in enumerate((-5.1, -3.7, -2.4, -0.5, 0.8, 2.2, 3.7, 5.0))])
        self.at("If rainfall")
        self.play(FadeOut(base[2]), FadeIn(rain), FadeIn(soft), hard.animate.set_opacity(0.35), run_time=1.1)
        direction = CurvedArrow([2.3, 2.35, 0], [-2.3, 2.35, 0], angle=0.5, color=TEXT, tip_length=0.22)
        dl = T("direction can change", 30, TEXT).next_to(direction, UP, buff=0.12)
        self.at("selection can")
        self.play(FadeOut(advantage), Create(direction), FadeIn(dl), run_time=0.75)

        arrival = finch(1, 0.82).move_to([-6.05, 0.25, 0])
        chance = T("chance", 28, TEXT).move_to([-4.8, 1.9, 0])
        self.at("Chance and arrivals")
        self.play(FadeIn(chance), FadeIn(arrival), arrival.animate.move_to([-4.6, 0.25, 0]),
                  birds.animate.shift(DOWN * 0.18), run_time=1.0)

        fixed = T("adult beaks unchanged", 31, TEXT).move_to([-3.3, -2.75, 0])
        locks = VGroup(*[Circle(radius=0.10, color=TEXT, stroke_width=2).next_to(b.beak, RIGHT, buff=0.05) for b in birds])
        self.at("The drought did")
        self.play(FadeOut(VGroup(advantage, direction, dl, chance, rain, soft, hard)), FadeIn(fixed), FadeIn(locks), run_time=0.9)
        self.at("It changed which")
        self.play(birds.animate.shift(UP * 0.22), run_time=1.0)
        self.at("The next generation")
        self.play(FadeIn(dist), FadeIn(scope_tag("schematic")), run_time=0.8)
        self.play(dist.bars[2].animate.set_fill(GREEN, opacity=0.9), run_time=0.65)
        self.finish()


class S11End(EndCard):
    LINE = "Inherited traits spread when their carriers leave more reproducing offspring."
