"""Extinction and survival — one carried forest, changed across the film.

COLOR MAP: living chestnuts GREEN; inherited resistance BLUE; blight/cankers RED;
seeds and offspring YELLOW; dead or non-reproducing tissue GREY.
"""
from bp_parts import *
import bp_style as _style

# The accuracy-gated end-card sentence is long. A condensed member of the house
# font family keeps the exact wording above the 22 pt floor on one line.
_style.TITLE_FONT = "Avenir Next Condensed"


GROUND_Y = -2.15
TREE_XS = (-5.25, -3.75, -2.25, -0.75, 0.75, 2.25, 3.75, 5.25)
RESISTANCE = (0.38, 1.05, 0.62, 1.52, 0.48, 1.25, 0.78, 1.68)
TAKE_HOME = "When environments change, populations survive only if some members survive and reproduce."


def tree(x, scale=1.0, resistance=0.7, alive=True, sway=True):
    """The carried chestnut picture. All forest scenes call this builder."""
    col = GREEN if alive else GREY
    trunk = RoundedRectangle(corner_radius=0.10, width=0.48 * scale, height=2.45 * scale,
                             stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.35)
    trunk.move_to([x, GROUND_Y + 1.22 * scale, 0])
    crown = VGroup(
        Circle(radius=0.66 * scale, color=col, fill_color=col, fill_opacity=0.30, stroke_width=4),
        Circle(radius=0.54 * scale, color=col, fill_color=col, fill_opacity=0.28, stroke_width=4).shift(LEFT * 0.48 * scale + DOWN * 0.12),
        Circle(radius=0.54 * scale, color=col, fill_color=col, fill_opacity=0.28, stroke_width=4).shift(RIGHT * 0.48 * scale + DOWN * 0.12),
    ).move_to([x, GROUND_Y + 2.72 * scale, 0])
    bar = RoundedRectangle(corner_radius=0.04, width=0.22 * scale, height=resistance * scale,
                           stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.85)
    bar.move_to([x, GROUND_Y + 0.18 * scale + resistance * scale / 2, 0])
    roots = VGroup(*[
        Line([x, GROUND_Y, 0], [x + dx * scale, GROUND_Y - 0.40 * scale, 0], color=col, stroke_width=4)
        for dx in (-0.45, 0.45)
    ])
    g = VGroup(roots, trunk, crown, bar)
    g.trunk, g.crown, g.bar, g.roots = trunk, crown, bar, roots
    if sway:
        crown._wind_t = x * 0.17
        base = crown.get_center().copy()
        def breeze(mob, dt, base=base):
            mob._wind_t += dt
            mob.move_to(base + RIGHT * 0.075 * np.sin(1.35 * mob._wind_t))
        crown.add_updater(breeze)
    return g


def forest(indices=range(8), resistances=RESISTANCE, alive=None, scale=1.0, ground=True):
    alive = set(indices if alive is None else alive)
    trees = VGroup(*[tree(TREE_XS[i], scale, resistances[i], i in alive) for i in indices])
    g = VGroup()
    if ground:
        g.add(Line([-6.35, GROUND_Y, 0], [6.35, GROUND_Y, 0], color=GREY, stroke_width=4))
    g.add(trees)
    g.trees = trees
    return g


def seed(x, y=-1.25, scale=1.0):
    return Ellipse(width=0.22 * scale, height=0.38 * scale, color=YELLOW,
                   fill_color=YELLOW, fill_opacity=0.9, stroke_width=2).move_to([x, y, 0]).rotate(-0.3)


def seedling(x, resistance=0.55, scale=1.0):
    stem = Line([x, GROUND_Y, 0], [x, GROUND_Y + 0.72 * scale, 0], color=YELLOW, stroke_width=5)
    leaves = VGroup(
        Ellipse(width=0.38 * scale, height=0.19 * scale, color=YELLOW, fill_color=YELLOW, fill_opacity=0.65).rotate(0.35),
        Ellipse(width=0.38 * scale, height=0.19 * scale, color=YELLOW, fill_color=YELLOW, fill_opacity=0.65).rotate(-0.35),
    ).arrange(RIGHT, buff=-0.05).move_to([x, GROUND_Y + 0.66 * scale, 0])
    bar = Rectangle(width=0.12 * scale, height=resistance * 0.38 * scale, color=BLUE,
                    fill_color=BLUE, fill_opacity=0.8).move_to([x, GROUND_Y + 0.16 * scale, 0])
    return VGroup(stem, leaves, bar)


def blight_specks(x0=-6.4, count=12, y0=-0.2):
    return VGroup(*[
        Dot([x0 - 0.18 * (i % 3), y0 + 0.33 * (i % 6), 0], radius=0.07 + 0.01 * (i % 2), color=RED)
        for i in range(count)
    ])


def canker(t):
    return RoundedRectangle(corner_radius=0.05, width=t.trunk.width + 0.10, height=0.34,
                            color=RED, fill_color=RED, fill_opacity=0.7, stroke_width=3).move_to(t.trunk.get_center())


def bird(at=(-6.2, 1.7, 0), color=TEXT):
    a = Arc(radius=0.28, start_angle=0.05, angle=2.7, color=color, stroke_width=5)
    b = Arc(radius=0.28, start_angle=0.40, angle=2.7, color=color, stroke_width=5).flip(RIGHT)
    return VGroup(a, b).arrange(RIGHT, buff=-0.12).move_to(at)


def panel_forest(center_x, varied=True):
    xs = [center_x - 2.25 + 0.9 * i for i in range(6)]
    hs = (0.36, 0.36, 0.36, 0.36, 0.36, 0.36) if not varied else (0.30, 0.62, 0.90, 0.42, 1.18, 0.76)
    trees = VGroup(*[tree(x, 0.50, h, sway=True) for x, h in zip(xs, hs)])
    front = Rectangle(width=5.15, height=0.20, stroke_color=RED, fill_color=RED,
                      fill_opacity=0.55, stroke_width=2).move_to([center_x, -2.42, 0])
    pulse(front, base=2.5, amp=1.2, speed=2.4)
    return VGroup(trees, front)


def predict_world():
    panels = TwoPanel("narrow variation", "wide variation", colors=(BLUE, BLUE), top=2.75, bottom=-2.55, size=28)
    left = panel_forest(-3.3, varied=False)
    right = panel_forest(3.3, varied=True)
    return VGroup(panels, left, right)


class S00Hook(SpokenScene):
    def construct(self):
        world = forest()
        specks = blight_specks()
        self.add(world, specks)
        self.at("red blight moves")
        self.play(specks.animate.shift(RIGHT * 11.8), run_time=3.1, rate_func=linear)
        qmark = T("?", 78, TEXT, font=TITLE_FONT).move_to([0, 2.95, 0])
        self.at("What decides whether")
        self.play(GrowFromCenter(qmark), run_time=0.8)
        self.play(qmark.animate.scale(1.10), rate_func=there_and_back, run_time=1.2)
        self.at("Watch the trees")
        self.play(LaggedStart(*[Indicate(t.bar, color=BLUE, scale_factor=1.15) for t in world.trees], lag_ratio=0.08), run_time=1.7)
        seeds = VGroup(*[seed(x, -1.72) for x in (-4.55, -1.55, 1.45, 4.45)])
        self.at("yellow seeds")
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in seeds], lag_ratio=0.15), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Extinction and Survival"
    TITLE = "Who Makes It Through the Change?"


class S02Fates(SpokenScene):
    def construct(self):
        world = forest()
        self.add(world)
        self.at("some members")
        self.play(world.trees[1].trunk.animate.set_fill(GREY, 0.55).set_stroke(GREY),
                  world.trees[1].crown.animate.set_opacity(0.12), run_time=1.4)
        self.at("Living members may reproduce")
        seeds = VGroup(seed(1.9), seed(2.55))
        kids = VGroup(seedling(1.9), seedling(2.55, 0.7))
        self.play(LaggedStart(*[FadeIn(s) for s in seeds], lag_ratio=0.2), run_time=0.8)
        self.play(LaggedStart(*[Transform(s, k) for s, k in zip(seeds, kids)], lag_ratio=0.2), run_time=1.2)
        self.at("Some migrate")
        b = bird()
        self.add(b)
        distant = VGroup(*[tree(4.8 + 0.7 * i, 0.35, 0.5 + 0.2 * i) for i in range(2)])
        self.play(b.animate.move_to([4.9, 2.3, 0]), FadeIn(distant), run_time=2.0)
        self.at("A species is extinct")
        local = forest(indices=range(4), alive=[], scale=0.72)
        remote = forest(indices=range(4, 8), alive=range(4, 8), scale=0.72)
        local.shift(LEFT * 0.5); remote.shift(RIGHT * 0.5)
        self.play(FadeOut(VGroup(world, seeds, b, distant)), FadeIn(local), FadeIn(remote), run_time=1.3)
        anywhere = T("living elsewhere", 30, GREEN).move_to([3.55, 2.35, 0])
        self.at("no living members remain anywhere")
        self.play(FadeIn(anywhere), Indicate(remote, color=GREEN), run_time=1.3)
        rule = caption("local loss is not extinction", 34, TEXT)
        self.at("Losing a species")
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.play(Indicate(rule, color=YELLOW), run_time=1.0)
        self.finish()


class S03Variation(SpokenScene):
    def construct(self):
        idx = (1, 2, 4, 6)
        close = forest(indices=idx, scale=1.0)
        self.play(FadeIn(close), run_time=1.0)
        self.at("blue bar represents")
        lab = T("inherited resistance", 32, BLUE).move_to([0, 3.15, 0])
        self.play(LaggedStart(*[GrowFromEdge(t.bar, DOWN) for t in close.trees], lag_ratio=0.12), FadeIn(lab), run_time=1.5)
        self.at("Different bar heights")
        self.play(LaggedStart(*[Indicate(t.bar, color=BLUE, scale_factor=1.12) for t in close.trees], lag_ratio=0.15), run_time=1.6)
        wave = Rectangle(width=0.65, height=5.4, fill_color=RED, fill_opacity=0.22, stroke_width=0).move_to([-6.2, 0.2, 0])
        self.at("cannot raise its bar")
        short = close.trees[0].bar
        self.play(FadeIn(wave), wave.animate.shift(RIGHT * 4.3), short.animate.stretch(2.3, 1, about_edge=DOWN), run_time=1.0)
        self.play(short.animate.stretch(1 / 2.3, 1, about_edge=DOWN), run_time=0.7, rate_func=there_and_back_with_pause)
        thought = VGroup(T("need does not", 27), T("change traits", 27)).arrange(DOWN, buff=0.06).move_to([-3.4, 2.4, 0])
        xout = Cross(thought, stroke_color=RED, stroke_width=5)
        xout.layout_ok = True  # deliberate cross-out: the narration rejects this idea
        self.play(FadeIn(thought), Create(xout), run_time=0.8)
        self.at("inherited from its parents")
        self.play(FadeOut(thought), FadeOut(xout), FadeOut(wave), run_time=0.5)
        parents = VGroup(*[tree(-4.25 + 1.1 * i, 0.50, 0.45 + 0.18 * i, alive=True, sway=False).set_opacity(0.30) for i in range(2)])
        lines = VGroup(*[Line(p.get_bottom(), close.trees[0].get_top(), color=GREY, stroke_width=2) for p in parents])
        self.play(FadeIn(parents), Create(lines), run_time=1.3)
        self.finish()


class S04Sorting(SpokenScene):
    def construct(self):
        idx = (1, 2, 4, 6)
        world = forest(indices=idx)
        self.add(world, scope_tag("schematic"))
        bands = VGroup(*[canker(t) for t in world.trees])
        self.at("Red cankers spread")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in bands], lag_ratio=0.12), run_time=1.5)
        self.at("shorter blue bars")
        self.play(world.trees[0].crown.animate.set_opacity(0.08), world.trees[0].trunk.animate.set_color(GREY),
                  world.trees[1].crown.animate.set_opacity(0.08), world.trees[1].trunk.animate.set_color(GREY), run_time=1.4)
        self.at("taller bar does not promise")
        tall = world.trees[3]
        self.play(tall.animate.set_opacity(0.25), run_time=0.6)
        self.play(tall.animate.set_opacity(1.0), run_time=0.7)
        chance = T("changes the chance", 32, TEXT).move_to([0, 3.15, 0])
        self.at("changes the chance")
        self.play(FadeIn(chance), Indicate(VGroup(world.trees[2], tall), color=GREEN), run_time=1.0)
        self.at("yellow seeds")
        seeds = VGroup(seed(world.trees[2].get_x()), seed(tall.get_x()))
        self.play(FadeIn(seeds), seeds.animate.shift(DOWN * 0.55), run_time=1.1)
        kids = VGroup(seedling(world.trees[2].get_x() - 0.7, 0.45), seedling(tall.get_x() + 0.65, 0.72))
        self.at("next generation")
        self.play(LaggedStart(*[GrowFromPoint(k, [k.get_x(), GROUND_Y, 0]) for k in kids], lag_ratio=0.25), run_time=1.3)
        self.finish()


class S05Predict(SpokenScene):
    QUESTION = "Which forest is more likely to leave seed-making survivors?"
    def construct(self):
        world = predict_world()
        self.play(FadeIn(world[0]), run_time=0.8)
        self.at("Every tree in the narrow")
        self.play(FadeIn(world[1]), run_time=1.3)
        self.at("varied forest includes")
        self.play(FadeIn(world[2]), run_time=1.3)
        self.play(LaggedStart(*[Indicate(t.bar, color=BLUE) for t in world[2][0]], lag_ratio=0.1), run_time=1.3)
        q = question_card(self.QUESTION, y=3.35, size=29, max_w=11.5)
        self.at("Which forest is more likely")
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = S05Predict.QUESTION
    SECONDS = 4.5
    CARD = {"y": 3.35, "size": 29, "max_w": 11.5}
    RING_AT = (6.0, 3.25, 0)
    def backdrop(self):
        return predict_world()


class S07Reveal(SpokenScene):
    def construct(self):
        world = predict_world()
        self.add(world, scope_tag("schematic"))
        left, right = world[1][0], world[2][0]
        fronts = VGroup(world[1][1], world[2][1])
        self.at("better chance")
        self.play(fronts.animate.shift(UP * 4.3), run_time=1.7)
        self.play(*[t.animate.set_opacity(0.18) for t in left],
                  *[right[i].animate.set_opacity(0.18) for i in (0, 1, 3, 5)], run_time=1.2)
        seeds = VGroup(seed(right[2].get_x(), -1.45, 0.75), seed(right[4].get_x(), -1.45, 0.75))
        self.play(FadeIn(seeds), run_time=0.7)
        self.at("could still lose every tree")
        ghost = right.copy().set_opacity(0.16)
        self.play(Transform(right, ghost), run_time=0.9)
        self.play(Transform(right, panel_forest(3.3, varied=True)[0]), run_time=0.7)
        self.at("Variation in leaf shape")
        shapes = VGroup(*[RegularPolygon(n=3 + i % 4, radius=0.24, color=BLUE, fill_color=BLUE, fill_opacity=0.5).move_to(t.crown) for i, t in enumerate(right)])
        self.play(FadeOut(VGroup(*[t.bar for t in right])), FadeIn(shapes), run_time=0.8)
        red_marks = VGroup(*[Dot(s.get_center(), radius=0.10, color=RED) for s in shapes])
        self.play(FadeIn(red_marks), run_time=0.7)
        self.at("difference must help")
        self.play(FadeOut(VGroup(shapes, red_marks)), FadeIn(VGroup(*[t.bar for t in right])), run_time=0.8)
        self.at("appear later or arrive")
        clock = Circle(radius=0.48, color=TEXT, stroke_width=4).move_to([0, 2.1, 0])
        hand = Line(clock.get_center(), clock.get_center() + UP * 0.38, color=YELLOW, stroke_width=4)
        late = Rectangle(width=0.18, height=0.9, color=BLUE, fill_color=BLUE, fill_opacity=0.35).move_to([6.7, 0.5, 0])
        self.play(Create(clock), GrowFromCenter(hand), FadeIn(late), run_time=0.6)
        self.play(Rotate(hand, TAU * 2.5, about_point=clock.get_center()), late.animate.shift(LEFT * 0.5), run_time=2.2, rate_func=linear)
        self.finish()


class S08Reproduction(SpokenScene):
    def construct(self):
        parents = VGroup(tree(-2.0, 1.15, 1.1), tree(2.0, 1.15, 1.45))
        ground = Line([-6.2, GROUND_Y, 0], [6.2, GROUND_Y, 0], color=GREY, stroke_width=4)
        self.play(Create(ground), FadeIn(parents), run_time=1.2)
        stop = Arrow([-5.4, -2.75, 0], [-0.5, -2.75, 0], color=GREY, stroke_width=5)
        self.at("never make seeds")
        self.play(GrowArrow(stop), run_time=1.2)
        blocked = T("no next generation", 30, GREY).move_to([2.6, -2.75, 0])
        self.play(FadeIn(blocked), run_time=0.8)
        self.at("yellow seeds fall")
        pollen = VGroup(*[Dot([-1.2 + 0.4 * i, 0.5 + 0.15 * np.sin(i), 0], radius=0.06, color=YELLOW) for i in range(7)])
        seeds = VGroup(seed(-1.1), seed(0), seed(1.1))
        self.play(FadeOut(blocked), FadeIn(pollen), pollen.animate.shift(RIGHT * 2.0), FadeIn(seeds), run_time=1.3)
        kids = VGroup(seedling(-1.1), seedling(0, 0.7), seedling(1.1, 0.8))
        self.play(LaggedStart(*[Transform(s, k) for s, k in zip(seeds, kids)], lag_ratio=0.15), run_time=1.3)
        arrow = Arrow([-5.4, -2.75, 0], [5.3, -2.75, 0], color=YELLOW, stroke_width=6)
        self.play(Transform(stop, arrow), run_time=0.6)
        self.at("Here is the rule")
        part1 = T("When environments change,", 33, TEXT).move_to([0, 3.28, 0])
        part2 = T("populations survive only if some members survive and reproduce.", 29, TEXT).move_to([0, 2.75, 0])
        self.play(FadeIn(part1), run_time=0.7)
        self.at("populations survive only")
        self.play(FadeIn(part2), run_time=1.0)
        self.finish()


class S09Challenges(SpokenScene):
    def construct(self):
        world = forest(indices=(1, 3, 5, 7), scale=0.9)
        kids = VGroup(seedling(-1.0), seedling(0.2), seedling(1.4))
        gen = Arrow([-5.8, -2.8, 0], [5.5, -2.8, 0], color=YELLOW, stroke_width=5)
        self.add(world, kids, gen)
        self.at("bird can leave")
        b = bird()
        self.play(FadeIn(b), b.animate.move_to([6.0, 2.1, 0]), run_time=1.7)
        self.at("rooted chestnut cannot")
        self.play(LaggedStart(*[Indicate(t.roots, color=GREEN) for t in world.trees], lag_ratio=0.15), run_time=1.3)
        self.at("seeds may spread")
        seeds = VGroup(seed(-0.4), seed(0.1), seed(0.6))
        self.play(FadeIn(seeds), seeds.animate.shift(RIGHT * 1.0 + DOWN * 0.5), run_time=1.3)
        cloud = RoundedRectangle(corner_radius=0.25, width=3.5, height=1.0, color=RED,
                                 fill_color=RED, fill_opacity=0.16).move_to([0, 2.65, 0])
        label = T("habitat loss", 30, RED).move_to(cloud)
        self.at("Habitat loss")
        self.play(FadeIn(cloud), FadeIn(label), run_time=0.7)
        for phrase, text in (("pollution", "pollution"), ("climate change", "climate change"), ("invasive species", "invasive species")):
            self.at(phrase)
            new = T(text, 30, RED).move_to(cloud)
            self.play(swap(label, new, 0.55))
            label = new
        self.at("same test remains")
        q = caption("Can any members survive and reproduce?", 34, TEXT)
        self.play(FadeOut(VGroup(cloud, label)), FadeIn(q), run_time=0.9)
        self.play(Indicate(VGroup(world, kids), color=YELLOW), run_time=1.0)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        world = forest()
        self.play(FadeIn(world), run_time=1.0)
        specks = blight_specks()
        self.at("Red blight arrives")
        self.add(specks)
        self.play(specks.animate.shift(RIGHT * 11.8), run_time=1.5, rate_func=linear)
        self.at("Blue resistance differs")
        self.play(LaggedStart(*[Indicate(t.bar, color=BLUE) for t in world.trees], lag_ratio=0.07), run_time=1.3)
        self.at("Some trees remain")
        lost = (0, 1, 3, 4, 6)
        self.play(*[world.trees[i].animate.set_opacity(0.15) for i in lost], run_time=1.2)
        self.at("yellow seeds start")
        seeds = VGroup(*[seed(x) for x in (-2.4, 0.3, 2.9)])
        kids = VGroup(*[seedling(x, 0.5 + 0.15 * i) for i, x in enumerate((-2.4, 0.3, 2.9))])
        self.play(FadeIn(seeds), seeds.animate.shift(DOWN * 0.5), run_time=0.8)
        self.play(LaggedStart(*[Transform(s, k) for s, k in zip(seeds, kids)], lag_ratio=0.15), run_time=1.2)
        self.at("population continues only")
        arrow = CurvedArrow([-5.5, 2.7, 0], [5.4, -1.1, 0], angle=-0.35, color=YELLOW, stroke_width=7)
        self.play(Create(arrow), run_time=1.4)
        self.finish()


class S11Handoff(SpokenScene):
    def construct(self):
        world = forest(indices=(1, 3, 5, 7), scale=0.82)
        model = T("model", 32, BLUE).move_to([0, 3.15, 0])
        self.play(FadeIn(world), FadeIn(model), run_time=1.0)
        self.at("requirement not a guarantee")
        req = caption("requirement, not guarantee", 34, TEXT)
        self.play(FadeIn(req), run_time=0.8)
        self.at("model forest is not")
        for t in world.trees:
            t.crown.clear_updaters()  # breeze updater would pull crowns off trunks during the slide
        self.play(FadeOut(req), world.animate.scale(0.5).move_to([-3.5, 0.3, 0]), model.animate.move_to([-3.5, 1.9, 0]), run_time=1.1)
        table = RoundedRectangle(corner_radius=0.16, width=5.4, height=4.5, color=GREY, stroke_width=3).move_to([3.4, 0.15, 0])
        real = T("real data", 34, YELLOW).next_to(table, UP, buff=0.2)
        self.play(Create(table), FadeIn(real), run_time=1.0)
        self.at("test the rule")
        self.play(Indicate(world, color=BLUE), run_time=0.8)
        self.at("real American Chestnut data")
        down = Arrow([3.4, -2.25, 0], [3.4, -3.35, 0], color=TEXT, stroke_width=6)
        self.play(Indicate(table, color=YELLOW), GrowArrow(down), run_time=1.1)
        self.finish()


class S12End(EndCard):
    LINE = TAKE_HOME
