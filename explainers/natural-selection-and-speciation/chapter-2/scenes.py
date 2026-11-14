"""When One Population Becomes Two — chapter 2.

COLOR MAP (shared with chapter 1 and fixed throughout this film)
  BLUE   = shallow-beaked finches
  YELLOW = middle-beaked finches
  GREEN  = deep-beaked finches
  TEXT   = barriers, breeding tests, and gene-flow arrows
  GREY   = habitat and neutral structure
  GOLD   = prediction and take-home rule

The island, birds, river, and gauge positions are rebuilt only through the builders below so the
carried world cannot drift between scenes. Bird tokens are schematic body blocks with beak bars.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


SHALLOW, MIDDLE, DEEP = BLUE, YELLOW, GREEN
BIRD_COLORS = [SHALLOW, MIDDLE, DEEP, MIDDLE, SHALLOW, DEEP,
               MIDDLE, DEEP, SHALLOW, MIDDLE, DEEP, SHALLOW]
BIRD_POS = [(-4.7, 1.45), (-2.9, 1.35), (-1.25, 1.55), (1.25, 1.45), (2.95, 1.3), (4.75, 1.5),
            (-4.45, -0.45), (-2.65, -0.65), (-1.15, -0.35), (1.15, -0.5), (2.8, -0.35), (4.55, -0.6)]


def finch(color=MIDDLE, scale=1.0):
    """Chapter-1 token geometry; colour carries the schematic beak category."""
    body = RoundedRectangle(corner_radius=0.18, width=0.82, height=0.58,
                            stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.24)
    depth = {SHALLOW: 0.14, MIDDLE: 0.24, DEEP: 0.34}[color]
    beak = Rectangle(width=0.28, height=depth, stroke_width=0,
                     fill_color=color, fill_opacity=1).next_to(body, RIGHT, buff=0)
    eye = Dot(body.get_center() + [0.17, 0.11, 0], radius=0.045, color=TEXT)
    g = VGroup(body, beak, eye).scale(scale)
    g.body, g.beak = body, beak
    return g


def gene_block(color, text="gene version"):
    return chip(text, color=color, size=24, pad=0.16, fill_opacity=0.25)


def island_world(divided=False, left_colors=None, right_colors=None, animate=True):
    """The one carried world: same island, landmarks, birds, and river in every scene."""
    land = RoundedRectangle(corner_radius=1.0, width=12.0, height=5.15,
                            stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.16).move_to([0, 0.15, 0])
    ridge = ArcBetweenPoints([-5.4, -1.6, 0], [5.3, -1.45, 0], angle=-0.2,
                             color=GREY, stroke_width=2).set_opacity(0.45)
    colors = list(BIRD_COLORS)
    if left_colors:
        colors[:6] = left_colors
    if right_colors:
        colors[6:] = right_colors
    birds = VGroup(*[finch(c, 1.08).move_to([x, y, 0])
                     for c, (x, y) in zip(colors, BIRD_POS)])
    if animate:
        for i, b in enumerate(birds):
            bob(b, amp=0.055, speed=1.3 + 0.08 * (i % 4), seed=i)
    g = VGroup(land, ridge, birds)
    g.land, g.birds = land, birds
    if divided:
        river = Rectangle(width=1.05, height=5.12, stroke_color=TEXT, stroke_width=4,
                          fill_color=BLUE, fill_opacity=0.22).move_to([0, 0.15, 0])
        flow = DashedLine([0, 2.55, 0], [0, -2.25, 0], color=TEXT,
                          stroke_width=4, dash_length=0.25).set_opacity(0.75)
        pulse(flow, base=3.5, amp=1.2, speed=2.0)
        g.add(river, flow)
        g.river, g.flow = river, flow
    return g


def exchange_arrows(opacity=1.0):
    arrs = VGroup(
        DoubleArrow([-3.65, 0.55, 0], [-1.7, 0.55, 0], buff=0.22, color=TEXT, stroke_width=4, tip_length=0.18),
        DoubleArrow([1.55, 0.45, 0], [3.55, 0.45, 0], buff=0.22, color=TEXT, stroke_width=4, tip_length=0.18),
        DoubleArrow([-1.1, -1.25, 0], [1.1, -1.25, 0], buff=0.15, color=TEXT, stroke_width=4, tip_length=0.18),
    ).set_opacity(opacity)
    for a in arrs:
        pulse(a, base=4, amp=1.1, speed=1.7)
    return arrs


def prediction_card():
    return question_card("Has the river made two species — or only started a split?",
                         y=-3.15, size=30, max_w=11.0)


def divided_prediction_backdrop():
    return VGroup(island_world(divided=True), exchange_arrows(0.28))


def gauges(distance=0.82, tested=False):
    d = ValueTracker(distance)
    t = ValueTracker(0.05)
    dg = dial(d, center=[-3.4, 0.45, 0], radius=1.55, label="distance", color=TEXT, fmt="far", scale=0)
    tg = dial(t, center=[3.4, 0.45, 0], radius=1.55, label="interbreeding test", color=TEXT,
              fmt="tested" if tested else "not tested", scale=0, size=30)
    return VGroup(dg, tg), d, t


def generation_strip():
    line = Line([-5.5, 2.85, 0], [5.5, 2.85, 0], color=GREY, stroke_width=4)
    knob = Dot([-5.5, 2.85, 0], radius=0.15, color=TEXT)
    label = T("generations", 28, TEXT).next_to(line, UP, buff=0.12)
    return VGroup(line, knob, label), knob


class S00Title(TitleCard):
    LESSON = "Natural selection and new species"
    TITLE = "When One Population Becomes Two"


class S01Link(SpokenScene):
    def construct(self):
        world = island_world()
        self.play(FadeIn(world.land), LaggedStart(*[FadeIn(b, scale=0.7) for b in world.birds], lag_ratio=0.04),
                  run_time=1.5)
        self.at("beak differences spreading")
        self.play(LaggedStart(*[Indicate(b.beak, color=b.beak.get_fill_color(), scale_factor=1.35)
                                for b in world.birds], lag_ratio=0.04), run_time=2.4)
        self.at("When does one")
        q = T("When does one population become two species?", 36, GOLD, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
        self.at("Start with one")
        bracket = Brace(world.land, UP, color=TEXT)
        one = T("one connected population", 30, TEXT).next_to(bracket, UP, buff=0.1)
        self.play(FadeOut(q), GrowFromCenter(bracket), FadeIn(one), run_time=0.8)
        self.at("meet breed and exchange")
        arrows = exchange_arrows()
        blocks = VGroup(gene_block(BLUE, "gene version"), gene_block(GREEN, "gene version"))
        blocks[0].move_to([-2.6, 2.15, 0]); blocks[1].move_to([2.55, 2.15, 0])
        self.play(GrowFromCenter(arrows), FadeIn(blocks), run_time=1.2)
        self.play(blocks[0].animate.shift(RIGHT * 1.2), blocks[1].animate.shift(LEFT * 1.2), run_time=2.0,
                  rate_func=there_and_back)
        self.finish()


class S02Species(SpokenScene):
    def construct(self):
        world = island_world()
        pairs = VGroup(*world.birds[:4]).scale(1.25).arrange(RIGHT, buff=1.0).move_to([0, 0.85, 0])
        self.add(world.land)
        self.play(FadeIn(pairs), run_time=0.9)
        self.at("interbreeding as the test")
        bridge = RoundedRectangle(corner_radius=0.18, width=6.8, height=0.48,
                                  stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.08).move_to([0, -0.15, 0])
        head = T("biological species concept", 36, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        self.play(Create(bridge), FadeIn(head), run_time=0.9)
        self.at("produce fertile offspring")
        young = VGroup(finch(BLUE, 0.72), finch(YELLOW, 0.72), finch(GREEN, 0.72)).arrange(RIGHT, buff=0.7)
        young.move_to([0, -1.25, 0])
        self.play(LaggedStart(*[FadeIn(y, shift=DOWN * 0.2) for y in young], lag_ratio=0.2), run_time=1.4)
        self.play(young.animate.shift(RIGHT * 1.4), run_time=1.4, rate_func=there_and_back)
        self.at("rarely breed with")
        outside = finch(MIDDLE, 1.15).move_to([5.2, -1.1, 0]).set_opacity(0.55)
        rare = DashedLine([3.1, -0.6, 0], [4.6, -1.0, 0], color=GREY, dash_length=0.15)
        self.play(FadeIn(outside), Create(rare), run_time=0.8)
        self.at("applies to sexual organisms")
        sexual = T("sexual organisms", 30, TEXT).move_to([0, -2.75, 0])
        fuzzy = T("edges can be fuzzy", 28, GREY).next_to(sexual, DOWN, buff=0.22)
        self.play(FadeIn(sexual), run_time=0.6)
        self.at("edges can be fuzzy")
        self.play(FadeIn(fuzzy), rare.animate.set_opacity(0.25), run_time=1.0)
        self.finish()


class S03Barrier(SpokenScene):
    def construct(self):
        world = island_world()
        arrows = exchange_arrows()
        self.add(world, arrows)
        self.at("river divides the habitat")
        river_world = island_world(divided=True)
        self.play(FadeIn(river_world.river, scale=0.2), FadeIn(river_world.flow), run_time=1.4)
        self.at("meet less often")
        self.play(arrows[2].animate.set_opacity(0.25).set_stroke(width=2), run_time=1.8)
        self.at("geographic isolation")
        geo = T("geographic isolation", 34, TEXT, weight=BOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(geo), run_time=0.7)
        self.at("Has the river already")
        q = prediction_card()
        self.play(FadeOut(geo), FadeIn(q.question, shift=UP * 0.12), run_time=0.9)
        self.at("Make your prediction")
        self.play(Indicate(q.question, color=GOLD, scale_factor=1.03), run_time=1.2)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Has the river made two species — or only started a split?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 30, "max_w": 11.0}

    def backdrop(self):
        return divided_prediction_backdrop()


class S05NotYet(SpokenScene):
    def construct(self):
        world = island_world(divided=True)
        self.add(world)
        self.at("Separation alone")
        rule = T("separation ≠ speciation", 40, GOLD, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(rule), run_time=0.8)
        self.at("birds may still breed")
        pair = VGroup(finch(BLUE, 1.25), finch(GREEN, 1.25)).arrange(RIGHT, buff=1.3).move_to([0, -0.4, 0])
        bridge = Line([-0.8, -1.05, 0], [0.8, -1.05, 0], color=TEXT, stroke_width=7)
        self.play(FadeOut(world.birds), FadeIn(pair), Create(bridge), run_time=1.0)
        self.play(pair[0].animate.shift(RIGHT * 0.4), pair[1].animate.shift(LEFT * 0.4), run_time=1.2)
        self.at("Distance describes")
        self.play(FadeOut(VGroup(world, pair, bridge, rule)), run_time=0.6)
        gs, d, t = gauges()
        self.play(FadeIn(gs), run_time=0.9)
        self.play(d.animate.set_value(0.95), run_time=1.2)
        self.at("species test asks")
        self.play(Indicate(gs[1], color=TEXT, scale_factor=1.04), run_time=1.4)
        self.finish()


class S06Diverge(SpokenScene):
    def construct(self):
        left = [BLUE, BLUE, YELLOW, BLUE, YELLOW, GREEN]
        right = [GREEN, GREEN, YELLOW, GREEN, YELLOW, BLUE]
        world = island_world(divided=True)
        strip, knob = generation_strip()
        self.add(world, strip)
        self.at("many generations")
        self.play(knob.animate.move_to([-1.8, 2.85, 0]), run_time=1.3, rate_func=linear)
        self.at("different mutations")
        muts = VGroup(gene_block(BLUE, "mutation"), gene_block(GREEN, "mutation"))
        muts[0].move_to([-3.7, 2.05, 0]); muts[1].move_to([3.7, 2.05, 0])
        for label in (muts[0][1], muts[1][1]):
            label.layout_ok = True  # deliberate label inside its mutation chip
        self.play(FadeIn(muts, scale=0.7), run_time=0.8)
        self.at("Different conditions")
        new = island_world(divided=True, left_colors=left, right_colors=right)
        self.play(Transform(world.birds, new.birds), knob.animate.move_to([5.5, 2.85, 0]),
                  run_time=2.4, rate_func=linear)
        self.at("Chance can shift")
        spinner = Arc(radius=0.45, start_angle=0, angle=1.7 * PI, color=TEXT, stroke_width=5).move_to([0, 1.75, 0])
        tip = Arrow([0, 1.75, 0], [0.34, 2.0, 0], buff=0, color=TEXT, tip_length=0.16)
        self.play(Create(spinner), Rotate(tip, angle=1.5 * PI, about_point=[0, 1.75, 0]), run_time=1.2)
        self.at("distributions may move apart")
        tags = VGroup(scope_tag("schematic"), T("bluer", 28, BLUE).move_to([-3.7, -2.05, 0]),
                      T("greener", 28, GREEN).move_to([3.7, -2.05, 0]))
        self.play(FadeIn(tags), run_time=0.8)
        self.finish()


class S07GeneFlow(SpokenScene):
    def construct(self):
        world = island_world()
        arrows = exchange_arrows()
        self.add(world)
        self.at("moves gene versions")
        blocks = VGroup(gene_block(BLUE), gene_block(GREEN))
        blocks[0].move_to([-3.2, 2.15, 0]); blocks[1].move_to([3.0, 2.15, 0])
        self.play(FadeIn(arrows), FadeIn(blocks), run_time=0.8)
        self.play(blocks[0].animate.shift(RIGHT * 5.8), blocks[1].animate.shift(LEFT * 5.6), run_time=3.2)
        self.at("sex cells such as pollen")
        pollen = gene_block(YELLOW, "pollen").move_to([-4.5, 2.1, 0])
        pollen[1].layout_ok = True  # deliberate label inside a moving pollen chip
        self.play(FadeIn(pollen), pollen.animate.move_to([4.4, 0.35, 0]), run_time=2.2, path_arc=-0.45)
        self.at("Before the river")
        connected = T("mixing keeps groups connected", 32, TEXT).move_to([0, 3.2, 0])
        self.play(FadeIn(connected), run_time=0.7)
        self.at("After isolation")
        divided = island_world(divided=True)
        self.play(FadeOut(connected), FadeIn(divided.river), FadeIn(divided.flow),
                  arrows[2].animate.set_opacity(0.22).set_stroke(width=2), run_time=1.4)
        reduced = T("reduced gene flow", 34, TEXT, weight=BOLD).move_to([0, 3.2, 0])
        not_tested = chip("interbreeding: not yet tested", TEXT, 26).move_to([3.25, -2.0, 0])
        not_tested[1].layout_ok = True  # deliberate status label inside its gauge chip
        self.play(FadeIn(reduced), FadeIn(not_tested), run_time=0.8)
        self.at("does not prove")
        allow = caption("allows divergence  ≠  proves speciation", color=GOLD)
        self.play(FadeIn(allow), run_time=0.9)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        world = island_world(divided=True, left_colors=[BLUE, BLUE, YELLOW, BLUE, YELLOW, GREEN],
                             right_colors=[GREEN, GREEN, YELLOW, GREEN, YELLOW, BLUE])
        self.add(world)
        self.at("same selection rule")
        rule = caption("Inherited traits spread when carriers leave more reproducing offspring.",
                       size=30, color=GOLD, y=3.25)
        self.play(FadeIn(rule), run_time=0.8)
        self.at("leave more reproducing offspring")
        young_l = VGroup(*[finch(BLUE, 0.58) for _ in range(3)]).arrange(RIGHT, buff=0.18).move_to([-3.4, -1.6, 0])
        young_r = VGroup(*[finch(GREEN, 0.58) for _ in range(3)]).arrange(RIGHT, buff=0.18).move_to([3.4, -1.6, 0])
        al = Arrow([-3.4, 0.0, 0], [-3.4, -1.0, 0], color=BLUE, buff=0.05)
        ar = Arrow([3.4, 0.0, 0], [3.4, -1.0, 0], color=GREEN, buff=0.05)
        self.play(GrowArrow(al), GrowArrow(ar), FadeIn(young_l), FadeIn(young_r), run_time=1.5)
        self.at("different traits helpful")
        self.play(Indicate(world.birds[:6], color=BLUE), Indicate(world.birds[6:], color=GREEN), run_time=1.3)
        self.at("selection does not define")
        self.play(FadeOut(VGroup(world, young_l, young_r, al, ar)), rule.animate.move_to([0, 2.75, 0]), run_time=0.7)
        gs, d, t = gauges()
        self.play(FadeIn(gs), run_time=0.8)
        self.play(Indicate(gs[1], color=TEXT, scale_factor=1.04), run_time=1.4)
        self.finish()


class S09Test(SpokenScene):
    def construct(self):
        world = island_world(divided=True, left_colors=[BLUE, BLUE, YELLOW, BLUE, YELLOW, GREEN],
                             right_colors=[GREEN, GREEN, YELLOW, GREEN, YELLOW, BLUE])
        self.add(world)
        self.at("barrier disappears")
        self.play(FadeOut(VGroup(world.river, world.flow)), run_time=1.2)
        paths = VGroup(DashedLine([-3.2, 0.8, 0], [3.0, 0.7, 0], color=TEXT, dash_length=0.18),
                       DashedLine([3.1, -0.8, 0], [-3.0, -0.7, 0], color=TEXT, dash_length=0.18))
        self.play(Create(paths), run_time=1.5)
        self.at("If the groups interbreed")
        self.play(FadeOut(VGroup(world, paths)), run_time=0.5)
        panels = TwoPanel("interbreed regularly", "no interbreeding, or only rare hybrids", colors=(TEXT, TEXT))
        panels.left_frame.set_fill(GREY, 0.08); panels.right_frame.set_fill(GREY, 0.08)
        self.play(FadeIn(panels), run_time=0.8)
        connected = VGroup(finch(BLUE), DoubleArrow(LEFT * 0.8, RIGHT * 0.8, color=TEXT, buff=0.1), finch(GREEN)).arrange(RIGHT, buff=0.25)
        panels.put(connected, "left")
        bob(connected, amp=0.05, speed=1.4)
        self.play(FadeIn(connected), run_time=0.8)
        self.at("split is incomplete")
        left_result = T("split incomplete", 34, GOLD, weight=BOLD).move_to(panels.area("left")[0] + DOWN * 1.3)
        self.play(FadeIn(left_result), run_time=0.7)
        self.at("barriers prevent interbreeding")
        rare = VGroup(finch(BLUE), DashedLine(LEFT * 0.7, RIGHT * 0.7, color=GREY, dash_length=0.15), finch(GREEN)).arrange(RIGHT, buff=0.25)
        panels.put(rare, "right")
        bob(rare, amp=0.05, speed=1.6, seed=2)
        self.play(FadeIn(rare), run_time=0.8)
        self.at("separate species")
        right_result = T("separate species", 34, GOLD, weight=BOLD).move_to(panels.area("right")[0] + DOWN * 1.3)
        self.play(FadeIn(right_result), run_time=0.7)
        self.at("reproductive isolation")
        cap = caption("reproductive isolation", size=38, color=TEXT)
        self.play(FadeIn(cap), run_time=0.8)
        self.finish()


class S10Limits(SpokenScene):
    def construct(self):
        panels = TwoPanel("interbreed regularly", "rare hybrids", colors=(TEXT, TEXT))
        panels.left_frame.set_fill(GREY, 0.08); panels.right_frame.set_fill(GREY, 0.08)
        self.play(FadeIn(panels), run_time=0.7)
        self.at("boundaries can remain fuzzy")
        boundary = DashedLine([0, -2.2, 0], [0, 2.7, 0], color=GREY, dash_length=0.25).set_opacity(0.5)
        self.play(Create(boundary), run_time=1.2)
        self.at("hybridise occasionally")
        dot = finch(YELLOW, 0.85).move_to([-2.5, 0.2, 0])
        path = DashedLine([-2.2, 0.2, 0], [2.3, 0.2, 0], color=TEXT, dash_length=0.16)
        occ = T("occasionally", 30, TEXT).move_to([0, 0.75, 0])
        occ.layout_ok = True  # intentionally labels the dotted crossing within the route panels
        self.play(FadeIn(dot), Create(path), FadeIn(occ), run_time=0.8)
        self.play(dot.animate.move_to([2.5, 0.2, 0]), run_time=1.8)
        self.at("organisms reproducing without sex")
        limit = caption("This concept does not fit reproduction without sex.", color=GOLD)
        self.play(FadeIn(limit), run_time=0.8)
        self.at("Speciation can also begin")
        self.play(FadeOut(VGroup(panels, boundary, dot, path, occ, limit)), run_time=0.6)
        cards = VGroup(*[RoundedRectangle(corner_radius=0.2, width=3.7, height=4.5, stroke_color=GREY,
                                          stroke_width=3, fill_color=GREY, fill_opacity=0.06) for _ in range(3)]).arrange(RIGHT, buff=0.5)
        river = Rectangle(width=0.38, height=2.5, stroke_color=TEXT, stroke_width=3,
                          fill_color=BLUE, fill_opacity=0.2).move_to(cards[0])
        labels = VGroup(T("river model", 28, TEXT).next_to(cards[0], UP, buff=0.18),
                        T("other route", 28, GREY).next_to(cards[1], UP, buff=0.18),
                        T("other route", 28, GREY).next_to(cards[2], UP, buff=0.18))
        self.play(FadeIn(cards), FadeIn(river), FadeIn(labels), run_time=1.0)
        self.at("one useful model")
        self.play(Indicate(cards[0], color=TEXT), run_time=1.2)
        self.finish()


class S11Answer(SpokenScene):
    def construct(self):
        steps = VGroup(chip("reduced gene flow", TEXT, 30), chip("may diverge", GOLD, 30),
                       chip("interbreeding test", TEXT, 30)).arrange(RIGHT, buff=0.75).move_to([0, 0.3, 0])
        arrows = VGroup(Arrow(steps[0].get_right(), steps[1].get_left(), buff=0.14, color=TEXT),
                        Arrow(steps[1].get_right(), steps[2].get_left(), buff=0.14, color=TEXT))
        barrier = Rectangle(width=0.45, height=2.2, stroke_color=TEXT, stroke_width=4,
                            fill_color=BLUE, fill_opacity=0.2).move_to([-6.25, 0.3, 0])
        self.at("barrier can start")
        self.play(FadeIn(barrier), FadeIn(steps[0]), GrowArrow(arrows[0]), run_time=1.1)
        self.at("Mutation selection and chance")
        causes = VGroup(chip("mutation", BLUE, 26), chip("selection", YELLOW, 26), chip("chance", GREEN, 26)).arrange(RIGHT, buff=0.25)
        causes.next_to(steps[1], UP, buff=0.65)
        self.play(FadeIn(causes), FadeIn(steps[1]), run_time=1.0)
        self.play(steps[1].animate.shift(UP * 0.12), run_time=1.2, rate_func=there_and_back)
        self.at("Interbreeding tests")
        self.play(GrowArrow(arrows[1]), FadeIn(steps[2]), run_time=0.9)
        self.at("split is complete")
        self.play(Indicate(steps[2], color=TEXT, scale_factor=1.05), run_time=1.1)
        self.at("same mechanism that changes")
        rule = caption("Population change can help separate populations across generations.", color=GOLD)
        self.play(FadeIn(rule), run_time=0.9)
        self.play(barrier.animate.shift(RIGHT * 0.55), steps.animate.shift(RIGHT * 0.12), run_time=1.8,
                  rate_func=there_and_back)
        self.finish()


class S12End(EndCard):
    LINE = "A barrier can start a split; interbreeding tests whether it is complete."
