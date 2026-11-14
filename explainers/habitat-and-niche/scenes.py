"""One forest, different ways to live.

COLOR MAP
  GOLD    habitat / the shared spruce forest
  YELLOW  insects and food resources
  TEAL    Cape May warbler
  ORANGE  Blackburnian warbler
  GREEN   black-throated green warbler
  PURPLE  bay-breasted warbler
  RED     myrtle warbler; red also marks competition/overlap

All bird movement and feeding zones are explicitly marked schematic.  The spruce,
birds, paths, and landmarks are rebuilt by ``spruce_world`` at the same scale and
position in every continuing scene.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


ORANGE = "#FF9D4D"
PURPLE = "#B58CD9"
BIRD_COLORS = [TEAL, ORANGE, GREEN, PURPLE, RED]
TREE_X = -0.65


def drifting(mob, amp=0.035, speed=1.2, phase=0.0):
    """Relative idle drift which remains compatible with later animations."""
    mob._drift_t = 0.0
    mob._drift_last = np.sin(phase) * amp

    def update(m, dt):
        m._drift_t += dt
        now = np.sin(speed * m._drift_t + phase) * amp
        m.shift(UP * (now - m._drift_last))
        m._drift_last = now
    mob.add_updater(update)
    return mob


def swaying(mob, amp=0.012, speed=0.75):
    """Slow canopy motion, applied as relative rotations so transforms still work."""
    mob._sway_t = 0.0
    mob._sway_last = 0.0

    def update(m, dt):
        m._sway_t += dt
        now = amp * np.sin(speed * m._sway_t)
        m.rotate(now - m._sway_last, about_point=m.get_center())
        m._sway_last = now
    mob.add_updater(update)
    return mob


def bird(color, scale=1.0):
    """A simple side-on bird silhouette; a labelled cartoon, not a species portrait."""
    body = Ellipse(width=0.58, height=0.34, stroke_color=color, stroke_width=2.5,
                   fill_color=color, fill_opacity=0.88)
    head = Circle(radius=0.14, stroke_width=0, fill_color=color, fill_opacity=1).move_to([0.26, 0.11, 0])
    wing = Ellipse(width=0.28, height=0.17, stroke_color=BG, stroke_width=1.5,
                   fill_color=BG, fill_opacity=0.35).move_to([-0.05, 0.02, 0]).rotate(-0.25)
    bill = Triangle(stroke_width=0, fill_color=YELLOW, fill_opacity=1).scale(0.07).rotate(-PI / 2)
    bill.move_to([0.43, 0.11, 0])
    tail = Triangle(stroke_width=0, fill_color=color, fill_opacity=0.9).scale(0.12).rotate(PI / 2)
    tail.move_to([-0.36, -0.03, 0])
    eye = Dot([0.29, 0.15, 0], radius=0.022, color=BG)
    return VGroup(tail, body, wing, head, bill, eye).scale(scale)


def search_path(kind, color=None, opacity=0.62):
    """Fixed preferred-zone paths for the five colors."""
    color = color or BIRD_COLORS[kind]
    pts = [
        [[-0.7, 2.35, 0], [1.25, 1.75, 0], [1.85, 1.10, 0]],
        [[-0.8, 1.45, 0], [-2.65, 0.95, 0], [-3.35, 0.15, 0]],
        [[-0.6, 0.55, 0], [1.55, 0.05, 0], [2.65, -0.65, 0]],
        [[-0.65, -0.25, 0], [-2.35, -0.85, 0], [-3.15, -1.55, 0]],
        [[-0.55, -1.10, 0], [1.25, -1.55, 0], [2.15, -2.20, 0]],
    ][kind]
    pts = [np.array(p) + RIGHT * TREE_X for p in pts]
    return VMobject(stroke_color=color, stroke_width=7, stroke_opacity=opacity).set_points_smoothly(pts)


def all_tree_path(kind, color=None):
    color = color or BIRD_COLORS[kind]
    phase = kind * 0.23
    pts = [
        np.array([TREE_X - 2.9, -1.9 + phase, 0]),
        np.array([TREE_X + 2.6, -1.0 + phase, 0]),
        np.array([TREE_X - 2.4, 0.2 + phase, 0]),
        np.array([TREE_X + 2.0, 1.0 + phase, 0]),
        np.array([TREE_X - 0.1, 2.45, 0]),
    ]
    return VMobject(stroke_color=color, stroke_width=5, stroke_opacity=0.52).set_points_smoothly(pts)


def spruce_world(paths="zones", insects=10, drift=True, birds=True):
    """The carried world: same tree, branch landmarks, bird colors, and coordinates."""
    trunk = Polygon([TREE_X - 0.22, -2.75, 0], [TREE_X + 0.22, -2.75, 0],
                    [TREE_X + 0.10, 2.65, 0], [TREE_X - 0.10, 2.65, 0],
                    stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.18)
    branches = VGroup()
    levels = [(2.15, 1.15), (1.55, 1.75), (0.85, 2.35), (0.10, 2.85), (-0.70, 3.25), (-1.55, 3.55)]
    for y, half in levels:
        branches.add(Line([TREE_X, y + 0.22, 0], [TREE_X - half, y - 0.42, 0], color=GOLD, stroke_width=7))
        branches.add(Line([TREE_X, y + 0.22, 0], [TREE_X + half, y - 0.42, 0], color=GOLD, stroke_width=7))
        for side in (-1, 1):
            x0 = TREE_X + side * half * 0.48
            branches.add(Line([x0, y - 0.02, 0], [x0 + side * 0.34, y + 0.28, 0],
                              color=GOLD, stroke_width=3.5).set_opacity(0.82))
    outline = Polygon([TREE_X, 2.95, 0], [TREE_X - 1.15, 1.55, 0], [TREE_X - 2.15, 0.15, 0],
                      [TREE_X - 3.75, -2.25, 0], [TREE_X + 3.75, -2.25, 0],
                      [TREE_X + 2.15, 0.15, 0], [TREE_X + 1.15, 1.55, 0],
                      stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.18)
    if drift:
        swaying(branches)
    path_group = VGroup()
    if paths == "zones":
        path_group = VGroup(*[search_path(i) for i in range(5)])
    elif paths == "all":
        path_group = VGroup(*[all_tree_path(i) for i in range(5)])

    insect_spots = [(-2.45, -1.35), (1.85, -1.45), (-1.85, -0.45), (2.15, -0.30),
                    (-1.20, 0.55), (1.25, 0.70), (-0.65, 1.55), (0.60, 1.45),
                    (-0.10, 2.25), (2.75, -1.70), (-3.05, -1.75), (0.15, -0.55)]
    bugs = VGroup(*[Dot([TREE_X + x, y, 0], radius=0.085, color=YELLOW) for x, y in insect_spots[:insects]])
    if drift and len(bugs):
        drifting(bugs, amp=0.10, speed=0.82, phase=0.6)
    bird_group = VGroup()
    if birds:
        for i in range(5):
            p = (search_path(i) if paths != "all" else all_tree_path(i)).point_from_proportion(0.15 + i * 0.12)
            b = bird(BIRD_COLORS[i], 0.78).move_to(p)
            if drift:
                drifting(b, amp=0.13, speed=0.82 + 0.06 * i, phase=i)
            bird_group.add(b)
    world = VGroup(outline, trunk, branches, path_group, bugs, bird_group)
    world.outline, world.trunk, world.branches = outline, trunk, branches
    world.paths, world.bugs, world.birds = path_group, bugs, bird_group
    return world


def model_tag():
    t = scope_tag("MODEL — SCHEMATIC", size=24)
    t.layout_ok = True
    return t


def energy_bar(color, x, value=0.18):
    frame = RoundedRectangle(corner_radius=0.08, width=0.34, height=1.05, stroke_color=color, stroke_width=2)
    fill = Rectangle(width=0.25, height=max(0.08, value), stroke_width=0, fill_color=color, fill_opacity=0.85)
    fill.align_to(frame, DOWN).shift(UP * 0.06)
    return VGroup(frame, fill).move_to([x, -2.3, 0])


def predict_backdrop():
    world = spruce_world(paths="all", insects=3)
    bars = VGroup(energy_bar(GREEN, 4.65, 0.08), energy_bar(RED, 5.35, 0.08))
    return VGroup(world, bars, model_tag())


class S01Hook(SpokenScene):
    def construct(self):
        tree = spruce_world(paths=None, insects=12)
        self.play(FadeIn(VGroup(tree.outline, tree.trunk, tree.branches), scale=0.97), run_time=0.8)
        self.play(FadeIn(tree.bugs, lag_ratio=0.06), FadeIn(tree.birds, lag_ratio=0.12), run_time=1.1)
        five = T("FIVE KINDS", 34, TEXT, weight=BOLD).move_to([4.75, 2.55, 0])
        five.layout_ok = True
        self.play(FadeIn(five, shift=LEFT * 0.2), run_time=0.6)
        self.at("How can they share")
        q = fit_text("How can they share one place\nwithout running out of food?", 5.0, 36, TEXT,
                     font=TITLE_FONT).move_to([4.25, 0.75, 0])
        self.play(Write(q), run_time=1.4)
        self.at("Watch the same tree")
        self.play(LaggedStart(*[b.animate.shift(RIGHT * (0.25 if i % 2 else -0.2))
                                for i, b in enumerate(tree.birds)], lag_ratio=0.12), run_time=1.4)
        self.at("Gold outlines")
        self.play(Indicate(tree.outline, color=GOLD, scale_factor=1.015), run_time=1.0)
        self.add(model_tag())
        self.finish()


class S02Title(NarratedScene):
    def construct(self):
        tree = spruce_world(paths=None, insects=8)
        title = fit_text("One Forest, Different Ways to Live", 8.2, 48, TEXT, font=TITLE_FONT).move_to([1.9, 0.45, 0])
        rule = Line([-2.0, -0.15, 0], [5.8, -0.15, 0], color=GOLD, stroke_width=5)
        self.add(tree)
        veil = RoundedRectangle(corner_radius=0.2, width=9.0, height=1.65, stroke_width=0,
                                fill_color=BG, fill_opacity=0.93).move_to([1.9, 0.38, 0])
        self.play(FadeIn(veil), FadeIn(title, shift=UP * 0.12), GrowFromCenter(rule), run_time=0.65)
        self.wait(0.75)
        self.play(FadeOut(VGroup(title, veil)), Transform(rule, tree.outline.copy()), run_time=0.45)
        self.finish()


class S03PlaceAndWay(SpokenScene):
    def construct(self):
        world = spruce_world(paths=None, insects=9)
        self.add(world)
        self.at("spruce forest")
        self.play(Indicate(world.outline, color=GOLD, scale_factor=1.02), run_time=0.8)
        habitat = T("HABITAT: PLACE", 34, GOLD, weight=BOLD).move_to([4.75, 2.65, 0])
        self.play(FadeIn(habitat, shift=LEFT * 0.2), run_time=0.7)
        self.at("A niche is different")
        paths = VGroup(*[search_path(i) for i in range(5)])
        self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.12), run_time=1.5)
        self.at("organism's role")
        niche = T("NICHE: WAY OF LIVING", 30, TEAL, weight=BOLD).move_to([4.15, 2.65, 0])
        self.play(swap(habitat, niche), run_time=0.7)
        self.at("Food is part")
        food = chip("food", YELLOW, size=28).move_to([4.75, 1.30, 0])
        self.play(FadeIn(food, scale=0.9), run_time=0.5)
        self.at("where and when")
        when = chip("place + time", TEAL, size=28).move_to([4.75, 0.45, 0])
        self.play(FadeIn(when, scale=0.9), run_time=0.5)
        self.at("space it uses")
        space = chip("space", GREEN, size=28).move_to([4.75, -0.40, 0])
        self.play(FadeIn(space, scale=0.9), run_time=0.5)
        self.at("what eats it")
        predators = chip("predators", RED, size=28).move_to([4.75, -1.25, 0])
        self.play(FadeIn(predators, scale=0.9), run_time=0.5)
        self.at("ecosystem role")
        role = chip("ecosystem role", PURPLE, size=26).move_to([4.55, -2.10, 0])
        self.play(FadeIn(role, scale=0.9), run_time=0.6)
        self.add(model_tag())
        self.finish()


class S04Resources(SpokenScene):
    def construct(self):
        world = spruce_world(paths="zones", insects=10)
        self.add(world, model_tag())
        self.at("needs and takes")
        resource = T("RESOURCE", 34, YELLOW, weight=BOLD).move_to([4.85, 2.55, 0])
        self.play(FadeIn(resource, shift=LEFT * 0.2), Indicate(world.bugs, color=YELLOW), run_time=0.9)
        self.at("Food, water")
        icons = VGroup(chip("food", YELLOW, 27), chip("water", BLUE, 27),
                       chip("shelter", GOLD, 27), chip("space", GREEN, 27)).arrange(DOWN, buff=0.18)
        icons.move_to([4.85, 0.55, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.15) for x in icons], lag_ratio=0.22), run_time=1.5)
        self.at("Each warbler searches")
        self.play(FadeOut(icons), LaggedStart(*[Indicate(p, color=BIRD_COLORS[i], scale_factor=1.01)
                                                for i, p in enumerate(world.paths)], lag_ratio=0.12), run_time=1.5)
        food_label = T("FOOD RESOURCE", 30, YELLOW, weight=BOLD).move_to([4.75, 1.25, 0])
        self.play(swap(resource, food_label), run_time=0.6)
        self.at("Finding insects")
        targets = list(world.bugs)[:5]
        for b in world.birds:
            b.clear_updaters()
        self.play(*[b.animate.move_to(t.get_center() + UP * 0.16) for b, t in zip(world.birds, targets)],
                  FadeOut(VGroup(*targets)), run_time=1.4)
        for i, b in enumerate(world.birds):
            drifting(b, amp=0.11, speed=0.85 + 0.05 * i, phase=i)
        self.at("food helps")
        bars = VGroup(*[energy_bar(BIRD_COLORS[i], 3.55 + i * 0.62, 0.16) for i in range(5)])
        full = VGroup(*[energy_bar(BIRD_COLORS[i], 3.55 + i * 0.62, 0.82) for i in range(5)])
        self.play(FadeIn(bars), run_time=0.5)
        self.play(Transform(bars, full), run_time=1.0)
        self.finish()


class S05Overlap(SpokenScene):
    def construct(self):
        world = spruce_world(paths="zones", insects=7)
        self.add(world, model_tag())
        self.at("short supply")
        gone = VGroup(*list(world.bugs)[3:])
        self.play(FadeOut(gone, lag_ratio=0.12), run_time=1.2)
        self.at("they compete")
        comp = T("COMPETITION", 36, RED, weight=BOLD).move_to([4.75, 2.55, 0])
        self.play(FadeIn(comp, shift=LEFT * 0.2), run_time=0.7)
        cross_a = search_path(0).point_from_proportion(0.70)
        shared = Dot(cross_a, radius=0.10, color=YELLOW)
        a, b = world.birds[0], world.birds[2]
        a.clear_updaters(); b.clear_updaters()
        self.at("same branches")
        self.play(a.animate.move_to(shared.get_center() + LEFT * 0.35),
                  b.animate.move_to(shared.get_center() + RIGHT * 0.35), FadeIn(shared), run_time=1.4)
        self.at("same insect")
        self.play(a.animate.move_to(shared.get_center()), b.animate.shift(RIGHT * 0.2), FadeOut(shared), run_time=0.8)
        drifting(a, amp=0.11, speed=0.86, phase=0.2)
        drifting(b, amp=0.11, speed=0.91, phase=1.1)
        overlap = Ellipse(width=2.25, height=1.35, stroke_color=RED, stroke_width=5,
                          fill_color=RED, fill_opacity=0.16).move_to(cross_a)
        self.at("niches overlap")
        self.play(Create(overlap), run_time=0.9)
        pulse(overlap, base=5, amp=1.5, speed=2.2)
        label = T("OVERLAP", 30, RED, weight=BOLD).move_to([4.75, 1.55, 0])
        self.play(FadeIn(label), run_time=0.5)
        self.finish()


class S05Species(SpokenScene):
    def construct(self):
        world = spruce_world(paths="zones", insects=4)
        overlap = Ellipse(width=2.25, height=1.35, stroke_color=RED, stroke_width=5,
                          fill_color=RED, fill_opacity=0.14).move_to(search_path(0).point_from_proportion(0.70))
        pulse(overlap, base=5, amp=1.4, speed=2.1)
        self.add(world, overlap, model_tag())
        self.at("one kind")
        species = T("SPECIES = ONE KIND", 31, TEXT, weight=BOLD).move_to([4.25, 2.55, 0])
        self.play(FadeIn(species, shift=LEFT * 0.2), run_time=0.7)
        self.at("different species")
        lineup = VGroup(*[bird(c, 0.82) for c in BIRD_COLORS]).arrange(RIGHT, buff=0.28).move_to([4.55, 1.45, 0])
        self.play(ReplacementTransform(world.birds.copy(), lineup), run_time=1.2)
        self.at("look similar")
        self.play(LaggedStart(*[Indicate(x, color=BIRD_COLORS[i], scale_factor=1.08)
                                for i, x in enumerate(lineup)], lag_ratio=0.12), run_time=1.2)
        self.at("enough food")
        bars = VGroup(energy_bar(TEAL, 4.15, 0.12), energy_bar(GREEN, 5.05, 0.12))
        self.play(FadeOut(lineup), FadeIn(bars), run_time=0.5)
        outcome = VGroup(energy_bar(TEAL, 4.15, 0.86), energy_bar(GREEN, 5.05, 0.22))
        self.play(Transform(bars, outcome), run_time=1.2)
        labels = VGroup(T("enough", 26, TEAL), T("short", 26, RED)).arrange(RIGHT, buff=0.75).move_to([4.6, -1.45, 0])
        self.play(FadeIn(labels), run_time=0.5)
        self.at("resource is scarce")
        self.play(Indicate(overlap, color=RED, scale_factor=1.05), run_time=0.9)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        world = spruce_world(paths="zones", insects=8)
        self.add(world, model_tag())
        self.at("Now predict")
        wide = VGroup(*[all_tree_path(i) for i in range(5)])
        self.play(Transform(world.paths, wide), run_time=1.2)
        self.at("Insects become scarce")
        self.play(FadeOut(VGroup(*list(world.bugs)[3:]), lag_ratio=0.10), run_time=1.1)
        self.at("every kind searches")
        for b in world.birds:
            b.clear_updaters()
        self.play(*[b.animate.move_to(all_tree_path(i).point_from_proportion(0.62))
                    for i, b in enumerate(world.birds)], run_time=1.3)
        for i, b in enumerate(world.birds):
            drifting(b, amp=0.13, speed=0.82 + 0.06 * i, phase=i)
        q = question_card("Will more birds get enough food, or will more fall short?", size=29,
                          y=-3.18, max_w=8.8, left=-6.25)
        self.at("Will more birds")
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.8)
        bars = VGroup(energy_bar(GREEN, 4.65, 0.08), energy_bar(RED, 5.35, 0.08))
        self.play(FadeIn(bars), run_time=0.5)
        self.at("insect dots fade")
        self.play(*[bug.animate.set_opacity(0.28) for bug in list(world.bugs)[:3]], run_time=1.0)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Will more birds get enough food, or will more fall short?"
    SECONDS = 4.5
    CARD = {"size": 29, "y": -3.18, "max_w": 10.7, "left": -6.25}
    RING_AT = (6.05, -3.12, 0)

    def backdrop(self):
        return predict_backdrop()


class S08Reveal(SpokenScene):
    def construct(self):
        world = spruce_world(paths="all", insects=3)
        self.add(world, model_tag())
        low = VGroup(*[energy_bar(c, 3.65 + i * 0.60, 0.16) for i, c in enumerate(BIRD_COLORS)])
        self.add(low)
        self.at("more kinds are likely")
        result = T("MODEL RESULT", 28, RED, weight=BOLD).move_to([4.85, 2.55, 0])
        self.play(FadeIn(result), run_time=0.5)
        fallen = VGroup(*[energy_bar(c, 3.65 + i * 0.60, 0.22 if i else 0.78) for i, c in enumerate(BIRD_COLORS)])
        self.play(Transform(low, fallen), run_time=1.4)
        self.at("each color favor")
        zoned = VGroup(*[search_path(i) for i in range(5)])
        self.play(Transform(world.paths, zoned), run_time=1.6)
        for b in world.birds:
            b.clear_updaters()
        self.play(*[b.animate.move_to(search_path(i).point_from_proportion(0.52))
                    for i, b in enumerate(world.birds)], run_time=1.2)
        for i, b in enumerate(world.birds):
            drifting(b, amp=0.13, speed=0.82 + 0.06 * i, phase=i)
        self.at("fewer paths cross")
        overlap = Ellipse(width=1.15, height=0.72, stroke_color=RED, stroke_width=4,
                          fill_color=RED, fill_opacity=0.12).move_to([TREE_X + 0.15, 0.35, 0])
        pulse(overlap, base=4, amp=1.0, speed=2.0)
        self.play(FadeIn(overlap), run_time=0.6)
        self.at("insects are limited")
        refill = VGroup(*[Dot(p, radius=0.085, color=YELLOW) for p in
                          ([TREE_X - 2.2, -1.25, 0], [TREE_X + 1.8, -1.25, 0],
                           [TREE_X - 1.0, 0.65, 0], [TREE_X + 0.7, 1.45, 0], [TREE_X, 2.15, 0])])
        self.play(LaggedStart(*[FadeIn(x, scale=0.4) for x in refill], lag_ratio=0.16), run_time=1.4)
        self.at("help more kinds")
        better = VGroup(*[energy_bar(c, 3.65 + i * 0.60, 0.62 + 0.05 * (i % 2)) for i, c in enumerate(BIRD_COLORS)])
        self.play(Transform(low, better), run_time=1.4)
        rule = caption("Different niches can reduce competition.", size=30, color=TEAL)
        self.play(FadeIn(rule), run_time=0.7)
        self.finish()


class S09Refine(SpokenScene):
    def construct(self):
        world = spruce_world(paths="zones", insects=6)
        world.scale(0.82).move_to([-1.55, 0.15, 0])
        frame = RoundedRectangle(corner_radius=0.18, width=7.0, height=5.2, stroke_color=GREY,
                                 stroke_width=3).move_to([-1.55, 0.15, 0])
        tag = T("MODEL", 28, GREY, weight=BOLD).move_to([-3.95, 2.25, 0])
        overlap = Ellipse(width=0.9, height=0.55, stroke_color=RED, stroke_width=4,
                          fill_color=RED, fill_opacity=0.13).move_to([-1.25, 0.4, 0])
        pulse(overlap, base=4, amp=1.0, speed=2.0)
        self.add(world, frame, tag, overlap)
        self.at("simplifies nature")
        self.play(Indicate(frame, color=GREY, scale_factor=1.01), run_time=0.8)
        self.at("Real niches")
        real = RoundedRectangle(corner_radius=0.22, width=12.5, height=6.35, stroke_color=TEAL,
                                stroke_width=4).move_to([0, 0.05, 0])
        real_lab = T("REAL NICHE", 32, TEAL, weight=BOLD).move_to([4.2, 2.79, 0])
        self.play(Transform(frame, real), swap(tag, real_lab), run_time=1.2)
        self.at("much more than feeding")
        factors = VGroup(chip("food", YELLOW, 26), chip("time", TEAL, 26), chip("space", GREEN, 26),
                         chip("predators", RED, 26), chip("weather", BLUE, 26)).arrange(DOWN, buff=0.15)
        factors.move_to([4.75, 0.45, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=LEFT * 0.12) for x in factors], lag_ratio=0.14), run_time=1.4)
        self.at("weather changes")
        wind = Arrow([3.0, 2.0, 0], [0.8, 1.55, 0], buff=0, color=BLUE, stroke_width=5, tip_length=0.22)
        self.play(GrowArrow(wind), world.birds[0].animate.shift(DOWN * 0.75), run_time=1.2)
        self.at("does not remove")
        self.play(Indicate(overlap, color=RED, scale_factor=1.08), run_time=0.8)
        self.at("chances of meeting")
        chance = T("chance of meeting", 30, RED, weight=BOLD).move_to([4.65, -2.15, 0])
        self.play(FadeOut(factors), FadeIn(chance, shift=UP * 0.12), run_time=0.7)
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        world = spruce_world(paths="zones", insects=7)
        self.add(world, model_tag())
        self.at("opening puzzle")
        puzzle = fit_text("How can they share one forest?", 5.2, 34, TEXT, font=TITLE_FONT).move_to([4.35, 2.35, 0])
        self.play(FadeIn(puzzle, shift=LEFT * 0.15), run_time=0.7)
        self.at("Shared habitat")
        rule = fit_text("SHARED HABITAT\n≠\nIDENTICAL NICHE", 4.0, 37, TEAL, font=TITLE_FONT).move_to([4.8, 0.55, 0])
        self.play(swap(puzzle, rule), Indicate(world.outline, color=GOLD, scale_factor=1.015), run_time=1.1)
        self.at("next step is evidence")
        grid = VGroup(*[DashedLine([TREE_X - 3.2, y, 0], [TREE_X + 3.2, y, 0], color=TEXT,
                                  stroke_width=2, dash_length=0.12).set_opacity(0.34)
                        for y in (-1.1, 0.2, 1.4)])
        watch = Circle(radius=0.48, color=TEXT, stroke_width=4).move_to([4.5, -1.65, 0])
        hand = Line(watch.get_center(), watch.get_center() + UP * 0.27 + RIGHT * 0.10, color=YELLOW, stroke_width=4)
        button = Line([4.35, -1.12, 0], [4.65, -1.12, 0], color=TEXT, stroke_width=4)
        self.play(FadeIn(grid), Create(watch), GrowFromCenter(button), Create(hand), run_time=1.2)
        self.at("Watch where real warblers")
        obs = T("TEST WITH OBSERVATIONS", 27, TEAL, weight=BOLD).move_to([4.05, 2.45, 0])
        self.play(swap(rule, obs), LaggedStart(*[Indicate(b, color=BIRD_COLORS[i], scale_factor=1.08)
                                                for i, b in enumerate(world.birds)], lag_ratio=0.12), run_time=1.4)
        self.at("observations can support")
        self.play(Indicate(grid, color=TEAL, scale_factor=1.01), run_time=0.9)
        self.play(FadeOut(VGroup(obs, grid, watch, hand, button)), run_time=0.5)
        self.finish()


class S11End(EndCard):
    LINE = "Different niches can reduce competition, helping species share a habitat."
