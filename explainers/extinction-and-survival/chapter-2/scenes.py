"""From Sprouts to Seed-Making Trees — chapter 2.

COLOR MAP (continued exactly from chapter 1)
  GREEN  = living chestnut tissue
  BLUE   = inherited resistance
  RED    = blight and cankers
  YELLOW = seeds and offspring
  GREY   = dead or nonreproducing tissue
"""
from bp_parts import *  # noqa: F401,F403


# ---------------------------------------------------------------------------
# One carried forest world. Every continuing scene calls these builders so the
# root, ground, sprout and canopy opening keep the same scale and coordinates.

GROUND_Y = -0.35
ROOT_Y = -2.25


def leaf(at, angle=0, color=GREEN, scale=1.0):
    m = Ellipse(width=0.72 * scale, height=0.34 * scale, stroke_color=color,
                stroke_width=3, fill_color=color, fill_opacity=0.55)
    m.rotate(angle).move_to(at)
    return m


def sprout(x=0.0, top=2.05, color=GREEN):
    stem = Line([x, ROOT_Y + 0.15, 0], [x, top, 0], color=color, stroke_width=13)
    l1 = leaf([x - 0.42, top - 0.43, 0], 0.38, color)
    l2 = leaf([x + 0.42, top - 0.08, 0], -0.38, color)
    tip = Dot([x, top + 0.12, 0], radius=0.10, color=color)
    g = VGroup(stem, l1, l2, tip)
    g.stem, g.leaves, g.tip = stem, VGroup(l1, l2), tip
    return g


def chestnut_root():
    root = CubicBezier([-5.9, -2.45, 0], [-3.5, -1.45, 0], [2.9, -3.0, 0],
                       [5.9, -2.1, 0], color=GREEN, stroke_width=34)
    branches = VGroup(
        CubicBezier([-3.7, -2.12, 0], [-4.4, -2.6, 0], [-4.7, -3.0, 0], [-5.5, -3.25, 0]),
        CubicBezier([2.8, -2.38, 0], [3.6, -2.75, 0], [4.3, -3.0, 0], [5.2, -3.35, 0]),
    ).set_stroke(GREEN, 17)
    return VGroup(root, branches)


def empty_canopy():
    silhouettes = VGroup()
    for x, h in [(-5.35, 2.4), (-3.95, 1.9), (4.0, 1.8), (5.4, 2.45)]:
        trunk = Rectangle(width=0.24, height=h + 0.4, stroke_width=0,
                          fill_color=GREY, fill_opacity=0.20).move_to([x, GROUND_Y + (h + 0.4) / 2, 0])
        crown = Circle(radius=0.72, stroke_color=GREY, stroke_width=2,
                       fill_color=GREY, fill_opacity=0.10).move_to([x, GROUND_Y + h + 0.28, 0])
        silhouettes.add(VGroup(trunk, crown))
    return silhouettes


def root_world(sprout_x=0.0, sprout_color=GREEN, include_sprout=True, canopy=True):
    soil_band = Rectangle(width=12.7, height=3.15, stroke_width=0, fill_color=GREEN,
                          fill_opacity=0.14).move_to([0, -1.95, 0])
    ground = Line([-6.35, GROUND_Y, 0], [6.35, GROUND_Y, 0], color=GREY, stroke_width=3)
    root = chestnut_root()
    g = VGroup(soil_band, ground, root)
    if canopy:
        g.add(empty_canopy())
    s = sprout(sprout_x, color=sprout_color)
    if include_sprout:
        g.add(s)
    g.ground, g.root, g.sprout = ground, root, s
    return g


def seed_tray(x=4.55, y=-1.18, empty=True):
    tray = VGroup(
        Line([x - 1.0, y + 0.38, 0], [x - 0.78, y - 0.38, 0], color=YELLOW, stroke_width=5),
        Line([x + 1.0, y + 0.38, 0], [x + 0.78, y - 0.38, 0], color=YELLOW, stroke_width=5),
        Line([x - 0.78, y - 0.38, 0], [x + 0.78, y - 0.38, 0], color=YELLOW, stroke_width=5),
    )
    seeds = VGroup(*[Ellipse(width=0.30, height=0.18, color=YELLOW, fill_color=YELLOW,
                            fill_opacity=0.85).move_to([x - 0.45 + 0.45 * i, y - 0.10, 0]) for i in range(3)])
    label = T("seeds", 28, YELLOW).move_to([x, y - 0.82, 0])
    g = VGroup(tray, label)
    if not empty:
        g.add(seeds)
    g.tray, g.seeds = tray, seeds
    return g


def tree(x, ground=GROUND_Y, scale=1.0, color=GREEN, bar_h=None):
    trunk = Rectangle(width=0.34 * scale, height=1.75 * scale, stroke_width=0,
                      fill_color=color, fill_opacity=0.70).move_to([x, ground + 0.875 * scale, 0])
    canopy = VGroup(*[
        Circle(radius=0.62 * scale, stroke_color=color, stroke_width=3,
               fill_color=color, fill_opacity=0.28).move_to([x + dx * scale, ground + dy * scale, 0])
        for dx, dy in [(-0.45, 1.8), (0.38, 1.85), (0, 2.3)]
    ])
    g = VGroup(trunk, canopy)
    g.trunk, g.canopy = trunk, canopy
    if bar_h is not None:
        bar = Rectangle(width=0.28 * scale, height=bar_h * scale, stroke_color=BLUE,
                        stroke_width=2.5, fill_color=BLUE, fill_opacity=0.65)
        bar.move_to([x, ground + 0.18 + bar.height / 2, 0])
        g.add(bar)
        g.bar = bar
    return g


def canker(x, y, width=0.42):
    return RoundedRectangle(corner_radius=0.12, width=width, height=0.42,
                            stroke_color=RED, stroke_width=3, fill_color=RED,
                            fill_opacity=0.70).move_to([x, y, 0])


def resistance_bar(x, base, height, width=0.34):
    return Rectangle(width=width, height=height, stroke_color=BLUE, stroke_width=2.5,
                     fill_color=BLUE, fill_opacity=0.65).move_to([x, base + height / 2, 0])


def seedling(x, y=-1.65, scale=1.0, bar_h=0.7):
    stem = Line([x, y, 0], [x, y + 1.25 * scale, 0], color=GREEN, stroke_width=8)
    leaves = VGroup(leaf([x - 0.25 * scale, y + 0.82 * scale, 0], 0.35, scale=0.62 * scale),
                    leaf([x + 0.25 * scale, y + 1.07 * scale, 0], -0.35, scale=0.62 * scale))
    bar = resistance_bar(x, y, bar_h * scale, 0.25 * scale)
    g = VGroup(stem, leaves, bar)
    g.stem, g.leaves, g.bar = stem, leaves, bar
    return g


def question_backdrop():
    w = root_world(sprout_x=-1.0)
    q = question_card("Can sprouts alone rebuild the population?", y=3.25, max_w=11.5, size=34)
    tray = seed_tray(4.5, -1.15, empty=True)
    waiting = canker(-1.42, 0.35, 0.22).set_opacity(0.65)
    return VGroup(w, tray, waiting, q)


def generation_arrow(start=(-3.5, -2.95, 0), end=(3.2, -2.95, 0), color=GREY):
    return Arrow(start, end, buff=0, color=color, stroke_width=7, max_tip_length_to_length_ratio=0.08)


def breeder_parents():
    american = tree(-3.4, ground=-1.55, scale=1.35, bar_h=0.55)
    chinese = tree(3.4, ground=-1.55, scale=1.35, bar_h=1.25)
    labels = VGroup(T("American chestnut", 28, TEXT).move_to([-3.4, 2.7, 0]),
                    T("Chinese chestnut", 28, TEXT).move_to([3.4, 2.7, 0]))
    note = scope_tag("examples, not every tree")
    return VGroup(american, chinese, labels, note)


def add_living_motion(world):
    """Visible, slow ambient motion while narration lands."""
    pulse(world.root, base=30, amp=3.0, speed=1.7)
    if hasattr(world, "sprout"):
        bob(world.sprout.leaves, amp=0.055, speed=1.5, seed=3)
    return world


class TimedTitleCard(TitleCard):
    """A hook scene that remains a TitleCard subclass but uses word cues."""
    _words = SpokenScene._words
    t_of = SpokenScene.t_of
    at = SpokenScene.at


# ---------------------------------------------------------------------------
# Film scenes

class S00Hook(TimedTitleCard):
    LESSON = "Extinction and Survival"
    TITLE = "From Sprouts to Seed-Making Trees"

    def construct(self):
        w = root_world(include_sprout=False)
        add_living_motion(w)
        self.at("population needs survivors")
        self.play(FadeIn(w[0]), Create(w.ground), FadeIn(w.root), FadeIn(w[-1]), run_time=1.4)
        self.at("roots still send up")
        self.play(GrowFromPoint(w.sprout, [0, ROOT_Y, 0]), run_time=1.7)
        self.add(w.sprout)
        bob(w.sprout.leaves, amp=0.06, speed=1.5)
        self.at("Why has that population")
        q = fit_text("Why has the population not recovered?", max_w=10.5, size=40,
                     color=TEXT).move_to([0, 3.05, 0])
        self.play(Write(q), run_time=1.0)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        w = add_living_motion(root_world())
        self.add(w)
        title = fit_text("From Sprouts to Seed-Making Trees", max_w=8.4, size=48,
                         color=TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(FadeIn(title, shift=UP * 0.12), w.animate.shift(DOWN * 0.08), run_time=0.75)
        self.wait(0.45)
        self.play(FadeOut(title), w.animate.shift(UP * 0.08), run_time=0.75)
        self.finish()


class S02Colors(SpokenScene):
    def construct(self):
        w = add_living_motion(root_world(include_sprout=False))
        self.add(w)
        key = VGroup(
            chip("living tissue", GREEN, 28), chip("blight", RED, 28),
            chip("inherited resistance", BLUE, 28), chip("seeds", YELLOW, 28),
        ).arrange(RIGHT, buff=0.25).move_to([0, 3.15, 0])
        self.at("Keep the same colors")
        self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.1) for k in key], lag_ratio=0.12), run_time=1.4)
        self.at("Green marks living")
        self.play(Indicate(w.root, color=GREEN), run_time=0.7)
        self.at("red marks blight")
        red_icon = canker(-5.65, 1.65).scale(0.8)
        self.play(FadeIn(red_icon), Indicate(key[1], color=RED), run_time=0.7)
        self.at("blue marks inherited")
        bar = resistance_bar(0, GROUND_Y, 1.35, 0.35)
        self.play(GrowFromEdge(bar, DOWN), Indicate(key[2], color=BLUE), run_time=0.8)
        self.at("yellow marks seeds")
        seeds = seed_tray(4.75, 1.25, empty=False)
        self.play(FadeIn(seeds, shift=DOWN * 0.15), Indicate(key[3], color=YELLOW), run_time=0.8)
        self.at("A green root remains")
        self.play(FadeOut(red_icon), FadeOut(seeds), Indicate(w.root, color=GREEN), run_time=0.7)
        self.at("It sends a leafy")
        self.play(GrowFromPoint(w.sprout, [0, ROOT_Y, 0]), run_time=1.7)
        self.add(w.sprout)
        bob(w.sprout.leaves, amp=0.06, speed=1.5)
        self.finish()


class S03Canker(SpokenScene):
    def construct(self):
        w = add_living_motion(root_world())
        self.add(w)
        fungus = chip("fungus", RED, 28).move_to([-5.0, 2.65, 0])
        self.add(fungus)
        self.play(fungus.animate.move_to([-3.0, 2.65, 0]), run_time=2.2)
        spores = VGroup(*[Dot([-2.4 - 0.35 * i, 0.55 + 0.22 * (i % 2), 0], radius=0.07, color=RED) for i in range(5)])
        self.add(spores)
        self.play(spores.animate.shift(RIGHT * 0.9), FadeOut(fungus), run_time=0.6)
        self.at("crack in the bark")
        crack = VGroup(Line([-0.12, 0.72, 0], [0.10, 0.52, 0], color=TEXT, stroke_width=3),
                       Line([0.10, 0.52, 0], [-0.08, 0.32, 0], color=TEXT, stroke_width=3))
        self.play(Create(crack), run_time=0.7)
        self.play(*[d.animate.move_to([0, 0.5, 0]) for d in spores], run_time=1.0)
        self.at("A canker widens")
        band = canker(0, 0.45, 0.35)
        label = T("canker", 30, RED).move_to([1.25, 0.45, 0])
        self.play(FadeOut(spores), FadeIn(band, scale=0.4), run_time=0.5)
        self.play(band.animate.stretch_to_fit_width(0.92), FadeIn(label), run_time=1.0)
        self.at("trunk above it fades")
        dead = VGroup(w.sprout.stem.copy(), w.sprout.leaves.copy(), w.sprout.tip.copy()).set_color(GREY)
        dead.set_opacity(0.72)
        self.play(FadeIn(dead), w.sprout.animate.set_opacity(0.15), run_time=1.4)
        self.at("protected root stays green")
        self.play(Indicate(w.root, color=GREEN), run_time=0.9)
        self.at("root sends up another")
        new = sprout(2.2, top=1.85)
        self.play(dead.animate.rotate(-0.28, about_point=[0, GROUND_Y, 0]).shift(RIGHT * 0.45),
                  FadeOut(label), run_time=0.8)
        self.play(GrowFromPoint(new, [2.2, ROOT_Y, 0]), run_time=1.5)
        bob(new.leaves, amp=0.05, speed=1.6)
        self.finish()


class S04Cycle(SpokenScene):
    def construct(self):
        w = add_living_motion(root_world(sprout_x=-1.1, canopy=False))
        self.add(w)
        tag = T("schematic", 24, GREY).move_to([-5.05, 3.3, 0])
        loop = CurvedArrow([-3.0, 1.9, 0], [2.7, 1.85, 0], angle=-1.4, color=GREY,
                           stroke_width=5)
        self.at("cycle repeats")
        self.play(FadeIn(tag), Create(loop), run_time=0.9)
        band = canker(-1.1, 0.25, 0.55)
        self.play(FadeIn(band), run_time=0.7)
        self.play(w.sprout.animate.set_color(GREY).set_opacity(0.55), run_time=0.8)
        new = sprout(1.8, top=1.9)
        self.play(GrowFromPoint(new, [1.8, ROOT_Y, 0]), run_time=1.2)
        self.at("forest contains living")
        clock = VGroup(Circle(radius=0.48, color=GREY, stroke_width=3),
                       Line(ORIGIN, UP * 0.31, color=TEXT, stroke_width=4),
                       Line(ORIGIN, RIGHT * 0.25, color=TEXT, stroke_width=4)).move_to([-4.9, 1.9, 0])
        self.play(FadeIn(clock), Rotate(clock[1], angle=1.2, about_point=clock.get_center()),
                  new.animate.shift(UP * 0.28), run_time=1.4)
        self.at("rarely become seed")
        dim_seeds = seed_tray(4.75, 0.15, empty=True).set_opacity(0.38)
        opening = DashedVMobject(Ellipse(width=4.5, height=1.45, color=GREY), num_dashes=28).move_to([0.5, 2.6, 0])
        self.play(FadeIn(dim_seeds), Create(opening), new.animate.shift(DOWN * 0.28), run_time=1.0)
        self.play(Rotate(clock[1], angle=1.5, about_point=clock.get_center()), run_time=1.4)
        self.at("Living stems alone")
        rule = fit_text("Living stems alone ≠ recovery", max_w=7.6, size=32,
                        color=TEXT).move_to([0.8, 3.3, 0])
        self.play(FadeOut(opening), FadeIn(rule, shift=UP * 0.12), run_time=0.9)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        w = add_living_motion(root_world(sprout_x=-1.0))
        self.add(w)
        self.at("Freeze the cycle")
        stop = VGroup(Line([-2.0, 2.45, 0], [-2.0, 3.0, 0], color=RED, stroke_width=8),
                      Line([-1.68, 2.45, 0], [-1.68, 3.0, 0], color=RED, stroke_width=8))
        self.play(FadeIn(stop), w.sprout.animate.rotate(-0.07, about_point=[-1.0, ROOT_Y, 0]), run_time=0.8)
        self.at("No yellow seeds")
        tray = seed_tray(4.5, -1.15, empty=True).shift(RIGHT * 1.5)
        self.add(tray)
        self.play(tray.animate.shift(LEFT * 1.5), run_time=1.2)
        self.at("every sprout dies")
        waiting = canker(-1.42, 0.35, 0.22).set_opacity(0.65)
        self.play(FadeIn(waiting), w.sprout.animate.rotate(0.07, about_point=[-1.0, ROOT_Y, 0]), run_time=0.9)
        self.at("can these sprouts rebuild")
        q = question_card("Can sprouts alone rebuild the population?", y=3.25,
                          max_w=11.5, size=34)
        self.play(FadeOut(stop), FadeIn(q.question, shift=DOWN * 0.1), run_time=1.0)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        config.background_color = BG
        g = question_backdrop()
        self.add(g)
        pulse(g[0].root, base=30, amp=3.0, speed=1.7)
        bob(g[0].sprout.leaves, amp=0.055, speed=1.5, seed=3)
        self.wait(4.5)


class S07Reveal(SpokenScene):
    def construct(self):
        w = add_living_motion(root_world(sprout_x=-2.7, canopy=False))
        self.add(w)
        self.play(w.sprout.animate.rotate(0.045, about_point=[-2.7, ROOT_Y, 0]), run_time=0.8)
        self.play(w.sprout.animate.rotate(-0.045, about_point=[-2.7, ROOT_Y, 0]), run_time=0.8)
        self.at("each green sprout proves")
        check = T("✓  living tissue remains", 32, GREEN).move_to([-2.6, 2.75, 0])
        self.play(FadeIn(check, shift=RIGHT * 0.15), run_time=0.9)
        self.at("species is not extinct")
        alive = chip("not extinct", GREEN, 30).move_to([3.9, 2.75, 0])
        self.play(FadeIn(alive), run_time=0.8)
        self.at("sprouts die before making")
        band = canker(-2.7, 0.35, 0.7)
        self.play(FadeIn(band), w.sprout.animate.set_color(GREY).set_opacity(0.55), run_time=1.1)
        self.at("no new generation")
        arrow = generation_arrow((-3.8, -3.05, 0), (3.6, -3.05, 0), GREY)
        block = Line([0.6, -3.34, 0], [0.6, -2.76, 0], color=RED, stroke_width=8)
        tray = seed_tray(4.65, -1.0, empty=True)
        self.play(GrowArrow(arrow), FadeIn(block), FadeIn(tray), run_time=1.2)
        self.at("replaces the old roots")
        self.play(w.root.animate.set_opacity(0.42).set_stroke(width=21), run_time=1.6)
        self.at("few sprouts make seeds")
        self.play(tray.animate.shift(UP * 0.38), run_time=0.8)
        self.play(tray.animate.shift(DOWN * 0.38), run_time=0.8)
        self.at("Survival requires survivors")
        rule = fit_text("Survival requires survivors to reproduce, not merely remain alive.",
                        max_w=11.5, size=36, color=TEXT).move_to([0, 1.65, 0])
        self.play(FadeOut(check), FadeOut(alive), FadeOut(w.sprout), FadeOut(band),
                  FadeIn(rule, shift=UP * 0.12), run_time=1.2)
        self.play(Indicate(VGroup(arrow, block), color=RED, scale_factor=1.02), run_time=1.0)
        self.finish()


class S08Cross(SpokenScene):
    def construct(self):
        backdrop = Rectangle(width=12.7, height=2.1, stroke_width=0, fill_color=GREEN,
                             fill_opacity=0.14).move_to([0, -2.45, 0])
        self.add(backdrop)
        self.at("How might people")
        prompt = fit_text("How might people change the path?", max_w=10, size=38).move_to([0, 3.2, 0])
        self.play(FadeIn(prompt), run_time=0.8)
        self.at("Breeders begin")
        parents = breeder_parents()
        self.play(FadeOut(prompt), LaggedStart(FadeIn(parents[0]), FadeIn(parents[1]), lag_ratio=0.25),
                  FadeIn(parents[2]), FadeIn(parents[3]), run_time=1.5)
        self.at("resist blight better")
        self.play(Indicate(VGroup(parents[0].bar, parents[1].bar), color=BLUE), run_time=0.9)
        self.at("cross the trees")
        cross_arrow = DoubleArrow([-2.1, -2.4, 0], [2.1, -2.4, 0], buff=0, color=YELLOW, stroke_width=6)
        cross_label = T("cross", 30, YELLOW).move_to([0, -2.8, 0])
        self.play(GrowArrow(cross_arrow), FadeIn(cross_label), run_time=0.9)
        self.at("expose the offspring")
        self.play(FadeOut(parents), FadeOut(cross_arrow), FadeOut(cross_label), run_time=0.5)
        kids = VGroup(*[seedling(-4.5 + 1.5 * i, -1.75, 0.9, h) for i, h in enumerate([0.5, 1.1, 0.7, 1.35, 0.65, 1.0, 0.55])])
        red = VGroup(*[canker(-4.5 + 1.5 * i, -0.85, 0.25 + 0.08 * (i % 3)) for i in range(7)])
        self.play(LaggedStart(*[GrowFromPoint(k, [k.get_x(), -1.75, 0]) for k in kids], lag_ratio=0.08), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in red], lag_ratio=0.08), run_time=1.0)
        self.finish()


class S09Select(SpokenScene):
    def construct(self):
        backdrop = Rectangle(width=12.7, height=2.1, stroke_width=0, fill_color=GREEN,
                             fill_opacity=0.14).move_to([0, -2.45, 0])
        hs = [0.45, 1.25, 0.7, 1.45, 0.55, 1.05, 0.6]
        xs = [-4.5 + 1.5 * i for i in range(7)]
        kids = VGroup(*[seedling(x, -1.75, 0.9, 0.5) for x in xs])
        self.add(backdrop, scope_tag("schematic"))
        self.play(LaggedStart(*[GrowFromPoint(k, [k.get_x(), -1.75, 0]) for k in kids], lag_ratio=0.06), run_time=0.55)
        self.at("bars differ")
        targets = [resistance_bar(x, -1.75, h * 0.9, 0.225) for x, h in zip(xs, hs)]
        self.play(LaggedStart(*[Transform(k.bar, target) for k, target in zip(kids, targets)], lag_ratio=0.08), run_time=1.4)
        self.at("choose the most resistant")
        chosen = VGroup(kids[1], kids[3], kids[5])
        rings = VGroup(*[Circle(radius=0.7, color=YELLOW, stroke_width=4).move_to([k.get_x(), -0.75, 0]) for k in chosen])
        hand = VGroup(Circle(radius=0.28, color=TEXT, fill_color=TEXT, fill_opacity=0.25),
                      Line([0, -0.25, 0], [0, -0.85, 0], color=TEXT, stroke_width=7)).move_to([-5.7, 2.3, 0])
        self.play(FadeIn(hand), hand.animate.move_to([kids[3].get_x(), 2.3, 0]), Create(rings), run_time=1.4)
        self.at("cross those back")
        parent = tree(4.9, ground=-1.5, scale=0.75, bar_h=0.45)
        cross_arrow = Arrow([1.9, 1.6, 0], [4.1, 1.25, 0], color=YELLOW, stroke_width=6)
        self.play(chosen.animate.shift(UP * 2.7).scale(0.7), FadeOut(hand), FadeOut(rings), FadeIn(parent), GrowArrow(cross_arrow), run_time=1.4)
        self.at("test again")
        newkids = VGroup(*[seedling(-3.9 + 1.3 * i, -2.25, 0.72, h) for i, h in enumerate([0.6, 1.0, 0.75, 1.2, 0.7, 1.1])])
        self.play(FadeOut(VGroup(*[k for k in kids if k not in chosen])), LaggedStart(*[FadeIn(k) for k in newkids], lag_ratio=0.08), run_time=1.2)
        self.at("artificial selection")
        label = chip("artificial selection", YELLOW, 32).move_to([0, 2.8, 0])
        self.play(FadeOut(chosen), FadeOut(parent), FadeOut(cross_arrow), FadeIn(label), run_time=0.9)
        self.at("People choose which trees")
        arrows = VGroup(*[Arrow([k.get_x(), -0.9, 0], [k.get_x(), 0.1, 0], color=YELLOW, stroke_width=4, buff=0.1) for k in [newkids[1], newkids[3], newkids[5]]])
        selected_new = VGroup(newkids[1], newkids[3], newkids[5])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
                  selected_new.animate.shift(UP * 0.35), run_time=1.2)
        self.at("environment alone decide")
        self.play(selected_new.animate.shift(DOWN * 0.35),
                  Indicate(VGroup(label, arrows), color=YELLOW, scale_factor=1.02), run_time=1.0)
        self.finish()


class S10Target(SpokenScene):
    def construct(self):
        backdrop = Rectangle(width=12.7, height=2.0, stroke_width=0, fill_color=GREEN,
                             fill_opacity=0.14).move_to([0, -2.75, 0])
        ground = Line([-6.2, -1.75, 0], [6.2, -1.75, 0], color=GREY, stroke_width=3)
        trees = VGroup(*[tree(-3.7 + 2.45 * i, ground=-1.75, scale=1.0, bar_h=h) for i, h in enumerate([0.65, 1.35, 1.05, 1.45])])
        self.at("not simply more differences")
        shapes = VGroup(Circle(radius=0.28, color=GREEN), Square(side_length=0.55, color=GREEN),
                        Triangle(color=GREEN).scale(0.34)).arrange(RIGHT, buff=0.35).move_to([0, 2.9, 0])
        self.play(FadeIn(backdrop), Create(ground),
                  LaggedStart(*[GrowFromPoint(t, [t.get_x(), -1.75, 0]) for t in trees], lag_ratio=0.10),
                  FadeIn(shapes), run_time=1.4)
        self.at("inherited resistance")
        self.play(FadeOut(shapes), LaggedStart(*[Indicate(t.bar, color=BLUE) for t in trees], lag_ratio=0.12),
                  trees.animate.shift(UP * 0.18), run_time=1.2)
        self.at("survive make seeds")
        cankers = VGroup(*[canker(t.get_x(), -0.6, 0.35) for t in trees])
        seeds = VGroup(*[Ellipse(width=0.28, height=0.17, color=YELLOW, fill_color=YELLOW, fill_opacity=0.9).move_to([x, 1.8, 0]) for x in [-2.8, -2.2, 0.9, 1.5, 3.7]])
        self.play(LaggedStart(*[FadeIn(c) for c in cankers], lag_ratio=0.1),
                  trees.animate.shift(DOWN * 0.18), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in seeds], lag_ratio=0.1), run_time=1.0)
        self.at("grow a next generation")
        nextgen = VGroup(*[seedling(-2.8 + 1.4 * i, -3.0, 0.48, 0.7) for i in range(5)])
        arrow = CurvedArrow([4.7, 1.7, 0], [3.3, -2.35, 0], angle=-0.6, color=YELLOW, stroke_width=5)
        self.play(Create(arrow), LaggedStart(*[GrowFromPoint(k, [k.get_x(), -3.0, 0]) for k in nextgen], lag_ratio=0.1), run_time=1.4)
        self.at("Other traits still matter")
        leaf_shapes = VGroup(leaf([-5.2, 2.7, 0], 0, scale=0.8), leaf([-4.3, 2.7, 0], 0.5, scale=0.65))
        self.play(FadeIn(leaf_shapes), run_time=0.7)
        self.at("cannot replace resistance")
        self.play(FadeOut(leaf_shapes, shift=LEFT * 0.3), Indicate(VGroup(*[t.bar for t in trees]), color=BLUE), run_time=1.0)
        self.finish()


class S11Limits(SpokenScene):
    def construct(self):
        backdrop = Rectangle(width=12.7, height=2.0, stroke_width=0, fill_color=GREEN,
                             fill_opacity=0.14).move_to([0, -2.65, 0])
        self.add(backdrop)
        panels = TwoPanel("site A · schematic", "site B · schematic", colors=(GREY, GREY), top=2.8, bottom=-2.4)
        self.at("Crossing does not promise")
        self.play(FadeIn(panels), run_time=0.9)
        fam_a = VGroup(*[seedling(-4.4 + 1.25 * i, -1.7, 0.72, 0.9) for i in range(4)])
        fam_b = VGroup(*[seedling(1.9 + 1.25 * i, -1.7, 0.72, 0.9) for i in range(4)])
        self.play(FadeIn(fam_a), FadeIn(fam_b), run_time=1.0)
        self.at("repeated tests")
        can_a = VGroup(*[canker(k.get_x(), -0.95, 0.55) for k in fam_a])
        can_b = VGroup(*[canker(k.get_x(), -0.95, 0.24) for k in fam_b])
        self.play(LaggedStart(*[FadeIn(c) for c in can_a], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(c) for c in can_b], lag_ratio=0.1), run_time=1.2)
        self.at("many families and sites")
        third = chip("more families · more sites", TEXT, 30).move_to([0, 3.25, 0])
        clips = VGroup(*[VGroup(Rectangle(width=0.62, height=0.8, color=TEXT, stroke_width=2),
                                Line([-0.18, 0.12, 0], [0.18, 0.12, 0], color=TEXT, stroke_width=2),
                                Line([-0.18, -0.08, 0], [0.12, -0.08, 0], color=TEXT, stroke_width=2))
                         .move_to([-4.8 + 1.9 * i, -2.95, 0]) for i in range(6)])
        self.play(FadeIn(third), LaggedStart(*[FadeIn(c) for c in clips], lag_ratio=0.1), run_time=1.2)
        self.at("how well young trees")
        self.play(fam_a.animate.set_opacity(0.55), Indicate(fam_b, color=GREEN), run_time=1.0)
        self.at("resist blight")
        self.play(Indicate(VGroup(can_a, can_b), color=RED), run_time=0.9)
        self.finish()


class S12OtherPath(SpokenScene):
    def construct(self):
        backdrop = Rectangle(width=12.7, height=2.0, stroke_width=0, fill_color=GREEN,
                             fill_opacity=0.14).move_to([0, -2.65, 0])
        self.add(backdrop)
        panels = TwoPanel("breeding path", "one-gene path", colors=(YELLOW, BLUE), top=2.9, bottom=-1.7)
        self.play(FadeIn(panels), run_time=0.7)
        left = VGroup(tree(-3.3, ground=-1.3, scale=0.75, bar_h=0.85),
                      DoubleArrow([-4.9, 0.0, 0], [-1.7, 0.0, 0], color=YELLOW, stroke_width=5))
        self.play(FadeIn(left), run_time=0.8)
        self.at("one gene from wheat")
        gene = chip("wheat gene", BLUE, 30).move_to([3.3, 1.45, 0])
        cell = RoundedRectangle(corner_radius=0.35, width=2.2, height=1.5, color=GREY, stroke_width=3).move_to([3.3, -0.15, 0])
        self.play(FadeIn(gene), Create(cell), run_time=0.8)
        self.play(gene.animate.move_to(cell), run_time=1.0)
        self.at("helped American chestnuts resist")
        altered = tree(3.3, ground=-1.35, scale=0.75, bar_h=1.1)
        self.play(FadeOut(gene), Transform(cell, altered), run_time=1.1)
        self.at("still being checked")
        check = chip("still being checked", GREY, 28).move_to([3.3, -1.35, 0])
        self.play(FadeIn(check), run_time=0.8)
        self.at("Both paths ask")
        self.play(FadeOut(panels), FadeOut(check), left.animate.scale(0.75).move_to([-3.2, 0.5, 0]),
                  cell.animate.scale(0.75).move_to([3.2, 0.5, 0]), run_time=1.0)
        forest = VGroup(*[tree(-1.1 + 1.1 * i, ground=-2.45, scale=0.48, bar_h=0.7) for i in range(3)])
        arrows = VGroup(Arrow([-2.7, -0.7, 0], [-1.0, -1.65, 0], color=YELLOW, stroke_width=5),
                        Arrow([2.7, -0.7, 0], [1.0, -1.65, 0], color=BLUE, stroke_width=5))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(forest), run_time=1.0)
        self.at("Will enough trees survive")
        q = fit_text("Will enough trees survive, reproduce, and keep reproducing?", max_w=11.5,
                     size=34, color=TEXT).move_to([0, 3.15, 0])
        gen = generation_arrow((-3.9, -3.15, 0), (3.9, -3.15, 0), YELLOW)
        self.play(FadeIn(q), GrowArrow(gen), run_time=1.2)
        self.play(Indicate(forest, color=GREEN), run_time=0.9)
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        ground = Line([-6.3, GROUND_Y, 0], [6.3, GROUND_Y, 0], color=GREY, stroke_width=3)
        root = chestnut_root()
        self.at("underground route")
        self.play(Create(ground), FadeIn(root), run_time=1.0)
        pulse(root, base=30, amp=3, speed=1.7)
        self.at("sprout alone keeps")
        lone = sprout(-3.7, top=1.55)
        band = canker(-3.7, 0.15, 0.55)
        self.play(GrowFromPoint(lone, [-3.7, ROOT_Y, 0]), FadeIn(band), run_time=1.2)
        loop = CurvedArrow([-4.8, 1.8, 0], [-2.7, 1.8, 0], angle=-1.5, color=GREY, stroke_width=4)
        self.play(Create(loop), lone.animate.set_color(GREY).set_opacity(0.6), run_time=1.0)
        self.at("Seed making trees")
        pair = VGroup(tree(2.0, ground=GROUND_Y, scale=1.0, bar_h=1.15),
                      tree(4.4, ground=GROUND_Y, scale=1.0, bar_h=1.25))
        self.play(LaggedStart(*[GrowFromPoint(t, [t.get_x(), GROUND_Y, 0]) for t in pair], lag_ratio=0.2), run_time=1.4)
        self.at("begin the future")
        pollen = VGroup(*[Dot([2.7 + 0.25 * i, 1.55 + 0.15 * np.sin(i), 0], radius=0.055, color=YELLOW) for i in range(6)])
        self.play(LaggedStart(*[FadeIn(p) for p in pollen], lag_ratio=0.1), run_time=0.6)
        self.play(pollen.animate.shift(RIGHT * 1.0), run_time=1.0)
        self.at("living through blight")
        red = VGroup(canker(2.0, 0.2, 0.35), canker(4.4, 0.2, 0.35))
        self.play(FadeIn(red), Indicate(VGroup(pair[0].bar, pair[1].bar), color=BLUE), run_time=1.0)
        self.at("producing the next generation")
        seeds = VGroup(*[Ellipse(width=0.25, height=0.15, color=YELLOW, fill_color=YELLOW, fill_opacity=0.9).move_to([2.8 + 0.38 * i, -0.05, 0]) for i in range(4)])
        kids = VGroup(*[seedling(2.7 + 0.65 * i, -2.9, 0.42, 0.75) for i in range(4)])
        arrow = generation_arrow((0.6, -3.25, 0), (5.7, -3.25, 0), YELLOW)
        self.play(FadeIn(seeds), GrowArrow(arrow), LaggedStart(*[GrowFromPoint(k, [k.get_x(), -2.9, 0]) for k in kids], lag_ratio=0.1), run_time=1.5)
        self.finish()


class S14Rule(SpokenScene):
    def construct(self):
        panels = TwoPanel("alive, not recovering", "survive and reproduce", colors=(GREEN, YELLOW), top=2.8, bottom=-2.15)
        left = VGroup(chestnut_root().scale(0.42), sprout(-3.25, top=0.8).scale(0.65), canker(-3.25, -0.05, 0.45))
        left.move_to([-3.25, 0.0, 0])
        right = VGroup(tree(2.15, ground=-1.5, scale=0.72, bar_h=1.0),
                       tree(4.25, ground=-1.5, scale=0.72, bar_h=1.1),
                       *[seedling(2.4 + 0.55 * i, -2.0, 0.38, 0.7) for i in range(4)])
        self.at("chestnut can remain alive")
        self.play(FadeIn(panels), FadeIn(left), run_time=1.0)
        self.at("fail to recover")
        self.play(left.animate.set_opacity(0.45), run_time=1.1)
        self.at("rule for this film")
        self.play(FadeIn(right), run_time=1.1)
        arrow = generation_arrow((-1.5, -2.8, 0), (1.5, -2.8, 0), YELLOW)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.at("Survival requires survivors")
        rule = fit_text("Survival requires survivors to reproduce, not merely remain alive.",
                        max_w=11.7, size=36, color=TEXT).move_to([0, 3.3, 0])
        self.play(FadeIn(rule, shift=DOWN * 0.12), right.animate.set_opacity(1.0), run_time=1.2)
        self.play(Indicate(right, color=YELLOW, scale_factor=1.02), run_time=1.0)
        self.finish()


class S15End(EndCard):
    LINE = "Survival requires survivors to reproduce, not merely remain alive."
