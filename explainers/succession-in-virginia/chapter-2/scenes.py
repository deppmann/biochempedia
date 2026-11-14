"""Why Succession Stays Open — chapter 2 of Succession in Virginia.

COLOR MAP (identical to chapter 1)
  LIME   early plants and fields
  GREEN  pines
  ORANGE oaks and hickories / late hardwoods
  YELLOW sunlight
  SOIL   soil
  BLUE   defined ideas and evidence
  RED    disturbance
  PURPLE people mowing
  GREY   neutral outlines and labels

The landscape and all plant symbols are schematic.  Every continuing scene rebuilds the
same landmarks at the same coordinates through ``virginia_landscape``.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

LIME = "#B5D86A"
SOIL = "#A67C52"
ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINE = GREEN
HARD = ORANGE
GROUND_Y = -2.25
PATCH_X = (-4.75, -1.6, 1.6, 4.75)


# --------------------------------------------------------------------------- shared world
def tufts(cx, base, n=6, h=0.75, color=LIME, gap=0.24, width=4):
    g = VGroup()
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * gap
        g.add(Line([x, base, 0], [x + (0.06 if i % 2 else -0.06), base + h * (0.82 + 0.06 * (i % 4)), 0],
                   color=color, stroke_width=width))
    return g


def pine(cx, base, h=2.3, w=1.25, color=PINE):
    trunk = Line([cx, base, 0], [cx, base + 0.55 * h, 0], color=color, stroke_width=5)
    crown = Polygon([cx - w / 2, base + 0.35 * h, 0], [cx + w / 2, base + 0.35 * h, 0],
                    [cx, base + h, 0], stroke_color=color, stroke_width=3.5,
                    fill_color=color, fill_opacity=0.34)
    return VGroup(trunk, crown)


def oak(cx, base, h=1.45, r=0.62, color=HARD):
    trunk = Line([cx, base, 0], [cx, base + h, 0], color=color, stroke_width=5)
    crown = Circle(radius=r, stroke_color=color, stroke_width=3.5,
                   fill_color=color, fill_opacity=0.34).move_to([cx, base + h + 0.45 * r, 0])
    return VGroup(trunk, crown)


def soil_strip():
    return Rectangle(width=12.6, height=0.34, stroke_color=SOIL, stroke_width=2.5,
                     fill_color=SOIL, fill_opacity=0.5).move_to([0, GROUND_Y - 0.17, 0])


def patch_frame(i, color=GREY, opacity=0.34):
    return RoundedRectangle(corner_radius=0.18, width=2.85, height=4.45, stroke_color=color,
                            stroke_width=2.5, stroke_opacity=opacity).move_to([PATCH_X[i], 0.0, 0])


def patch_plants(i, stage=None):
    """Same four patches everywhere: field, pines, hardwoods, mixed hardwoods."""
    x = PATCH_X[i]
    stage = stage or ("field", "pine", "hard", "mixed")[i]
    if stage == "field":
        return tufts(x, GROUND_Y, 8, 0.85)
    if stage == "pine":
        return VGroup(pine(x - 0.62, GROUND_Y, 2.55, 1.2), pine(x + 0.62, GROUND_Y, 2.2, 1.1))
    if stage == "young":
        return VGroup(oak(x - 0.55, GROUND_Y, 0.8, 0.38), oak(x + 0.55, GROUND_Y, 0.7, 0.34))
    if stage == "maple":
        return VGroup(oak(x - 0.65, GROUND_Y, 1.35, 0.58),
                      oak(x + 0.65, GROUND_Y, 1.2, 0.52, color=RED))
    return VGroup(oak(x - 0.68, GROUND_Y, 1.55, 0.66), oak(x + 0.68, GROUND_Y, 1.38, 0.60))


def virginia_landscape(stages=None, frames=True, moving=True):
    stages = stages or ("field", "pine", "hard", "mixed")
    land = VGroup(soil_strip())
    if frames:
        land.add(VGroup(*[patch_frame(i) for i in range(4)]))
    plants = VGroup(*[patch_plants(i, stages[i]) for i in range(4)])
    if moving:
        for i, p in enumerate(plants):
            bob(p, amp=0.12, speed=3.2 + 0.25 * i, seed=i)
    land.add(plants)
    clouds = VGroup(
        Ellipse(width=3.0, height=0.72, stroke_width=0, fill_color=GREY, fill_opacity=0.15).move_to([-3.5, 2.75, 0]),
        Ellipse(width=2.6, height=0.62, stroke_width=0, fill_color=GREY, fill_opacity=0.13).move_to([2.8, 2.45, 0]),
    )
    if moving:
        bob(clouds[0], amp=0.14, speed=3.1, seed=1)
        bob(clouds[1], amp=0.13, speed=3.5, seed=3)
    land.add(clouds)
    land.plants = plants
    land.clouds = clouds
    return land


def disturbance_mark(i, symbol="storm"):
    x = PATCH_X[i]
    if symbol == "flood":
        waves = VGroup(*[Arc(radius=0.5 + 0.22 * k, start_angle=0.12, angle=PI - 0.24,
                            color=BLUE, stroke_width=5).move_to([x, -1.25, 0]) for k in range(3)])
        return waves
    if symbol == "fire":
        return VGroup(*[Triangle(stroke_color=RED, fill_color=RED, fill_opacity=0.6).scale(0.22 + 0.05 * k)
                        .move_to([x - 0.55 + 0.38 * k, -1.55, 0]) for k in range(4)])
    if symbol == "mow":
        body = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.45, color=PURPLE,
                                fill_color=PURPLE, fill_opacity=0.25)
        wheels = VGroup(Dot(radius=0.1, color=PURPLE), Dot(radius=0.1, color=PURPLE))
        wheels.arrange(RIGHT, buff=0.5).next_to(body, DOWN, buff=-0.02)
        return VGroup(body, wheels).move_to([x, -1.25, 0])
    bolt = VMobject(stroke_color=RED, stroke_width=8).set_points_as_corners([
        [x - 0.55, 2.55, 0], [x + 0.1, 1.75, 0], [x - 0.15, 1.75, 0], [x + 0.55, 0.85, 0]])
    return bolt


def roots_and_seeds(i):
    x = PATCH_X[i]
    roots = VGroup(*[ArcBetweenPoints([x + d, GROUND_Y - 0.03, 0], [x + d * 0.5, GROUND_Y - 0.28, 0],
                                     angle=0.6, color=SOIL, stroke_width=3) for d in (-0.7, -0.25, 0.3, 0.7)])
    seeds = VGroup(*[Dot([x + d, GROUND_Y - 0.08, 0], radius=0.055, color=LIME) for d in (-0.55, 0, 0.5)])
    return VGroup(roots, seeds)


def canopy_comparison(gap=False, meters=True):
    panels = TwoPanel("unbroken canopy", "storm gap", colors=(HARD, HARD), top=3.0, bottom=-2.15)
    left_ground = Rectangle(width=5.2, height=0.25, fill_color=SOIL, fill_opacity=0.5,
                            stroke_color=SOIL).move_to([-3.3, -1.72, 0])
    right_ground = left_ground.copy().move_to([3.3, -1.72, 0])
    left = VGroup(left_ground, oak(-4.35, -1.6, 2.0, 0.78), oak(-3.25, -1.6, 2.15, 0.8),
                  oak(-2.15, -1.6, 1.95, 0.76), tufts(-3.25, -1.6, 4, 0.42, HARD))
    right = VGroup(right_ground, oak(2.15, -1.6, 2.0, 0.78), oak(4.35, -1.6, 1.95, 0.76),
                   tufts(3.25, -1.6, 4, 0.42, HARD))
    if not gap:
        right.add(oak(3.25, -1.6, 2.15, 0.8))
    world = VGroup(panels, left, right)
    if meters:
        lv, rv = ValueTracker(0.18), ValueTracker(0.18)
        meters_g = VGroup(dial(lv, [-3.3, 0.0, 0], radius=0.62, label="", color=YELLOW,
                               fmt="", size=28),
                           dial(rv, [3.3, 0.0, 0], radius=0.62, label="", color=YELLOW,
                               fmt="", size=28))
        world.add(meters_g)
        world.left_meter, world.right_meter = lv, rv
        world.meters = meters_g
    world.left_trees, world.right_trees = left, right
    return world


def route_icons(center=(0, 0, 0), scale=1.0):
    x, y, _ = center
    field = tufts(x - 2.3 * scale, y - 0.45 * scale, 5, 0.8 * scale).scale(scale)
    pn = pine(x, y - 0.45 * scale, 1.55 * scale, 0.9 * scale)
    hd = oak(x + 2.3 * scale, y - 0.45 * scale, 1.0 * scale, 0.48 * scale)
    a1 = Arrow([x - 1.55 * scale, y, 0], [x - 0.65 * scale, y, 0], color=GREY, buff=0,
               stroke_width=4, tip_length=0.18)
    a2 = Arrow([x + 0.65 * scale, y, 0], [x + 1.55 * scale, y, 0], color=GREY, buff=0,
               stroke_width=4, tip_length=0.18)
    return VGroup(field, a1, pn, a2, hd)


def summary_card(at=(-3.4, 0.25, 0), width=5.6, height=4.7):
    box = RoundedRectangle(corner_radius=0.2, width=width, height=height, stroke_color=BLUE,
                           stroke_width=4, fill_color=BLUE, fill_opacity=0.07).move_to(at)
    title = T("regional summary", 32, BLUE, weight=BOLD).next_to(box.get_top(), DOWN, buff=0.3)
    route = route_icons((at[0], at[1] - 0.15, 0), 0.78)
    tag = T("schematic pattern", 28, GREY).next_to(box.get_bottom(), UP, buff=0.28)
    return VGroup(box, title, route, tag)


def permanent_plot(at=(3.5, 0.15, 0), mix=(LIME, PINE, HARD)):
    x, y, _ = at
    box = Square(3.8, stroke_color=BLUE, stroke_width=5).move_to(at)
    stakes = VGroup(*[Dot(box.get_corner(c), radius=0.11, color=BLUE) for c in (UL, UR, DL, DR)])
    plants = VGroup()
    xs = (-1.05, -0.35, 0.35, 1.05)
    for k, dx in enumerate(xs):
        col = mix[k % len(mix)]
        if col == PINE:
            plants.add(pine(x + dx, y - 1.45, 1.35 + 0.12 * (k % 2), 0.65))
        elif col == HARD:
            plants.add(oak(x + dx, y - 1.45, 0.8 + 0.1 * (k % 2), 0.34))
        else:
            plants.add(tufts(x + dx, y - 1.45, 3, 0.7, col, gap=0.13, width=3))
    return VGroup(box, stakes, plants)


# --------------------------------------------------------------------------- scenes
class S00Hook(SpokenScene):
    def construct(self):
        close_ground = Rectangle(width=12.6, height=0.38, stroke_color=SOIL, stroke_width=3,
                                 fill_color=SOIL, fill_opacity=0.55).move_to([0, -2.15, 0])
        field = VGroup(close_ground, tufts(-4.3, -1.95, 9, 1.35),
                       pine(-0.7, -1.95, 3.9, 2.1), oak(3.4, -1.95, 2.4, 1.05))
        bob(field[1], amp=0.12, speed=3.0)
        bob(field[2], amp=0.12, speed=3.3, seed=1)
        bob(field[3], amp=0.12, speed=3.6, seed=2)
        self.add(field)
        self.at("The first film")
        self.play(field.animate.scale(0.92), run_time=1.1)
        self.at("Why does a whole landscape")
        q = fit_text("Why not one final stage?", 10.8, 48, YELLOW, font=TITLE_FONT).move_to([0, 2.75, 0])
        self.play(Write(q), field.animate.scale(0.9), run_time=1.6)
        self.at("Pull back from")
        world = virginia_landscape()
        self.play(FadeOut(q), Transform(field, world), run_time=2.2)
        tag = scope_tag("schematic", size=24)
        self.play(FadeIn(tag), run_time=0.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Succession in Virginia"
    TITLE = "Why Succession Stays Open"


class S02Patchwork(SpokenScene):
    def construct(self):
        world = virginia_landscape()
        self.add(world, scope_tag("schematic"))
        self.at("Different patches")
        self.play(LaggedStart(*[Indicate(patch_frame(i), color=BLUE, scale_factor=1.02) for i in range(4)],
                              lag_ratio=0.18), run_time=1.5)
        marks = []
        for phrase, i, kind in (("A storm opens", 2, "storm"), ("Flood water covers", 1, "flood"),
                                ("Fire crosses", 3, "fire"), ("People keep mowing", 0, "mow")):
            self.at(phrase)
            m = disturbance_mark(i, kind)
            marks.append(m)
            self.play(FadeIn(m, shift=UP * 0.12), run_time=0.65)
            if kind == "mow":
                self.play(m.animate.shift(RIGHT * 0.7), run_time=0.6)
            else:
                self.play(Indicate(world.plants[i], color=RED, scale_factor=0.96), run_time=0.55)
        self.at("Each disturbance removes")
        self.play(LaggedStart(*[FadeOut(m) for m in marks], lag_ratio=0.12), run_time=0.8)
        remains = VGroup(*[roots_and_seeds(i) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.08) for r in remains], lag_ratio=0.18), run_time=1.4)
        self.at("different soil")
        labs = VGroup(T("soil", 28, SOIL), T("roots", 28, SOIL), T("seeds", 28, LIME)).arrange(RIGHT, buff=0.7)
        labs.move_to([0, 3.15, 0])
        self.play(FadeIn(labs, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        world = canopy_comparison(gap=True)
        for i, tree in enumerate(list(world.left_trees[1:4]) + list(world.right_trees[1:3])):
            bob(tree, amp=0.12, speed=3.2 + 0.2 * i, seed=i)
        self.at("Compare an unbroken")
        self.play(FadeIn(world, lag_ratio=0.08), run_time=1.4)
        self.at("Which patch")
        q = question_card("Which patch receives more light at ground level?", y=-3.15, size=30)
        qm = T("?", 64, YELLOW, weight=BOLD).move_to([0, 0.15, 0])
        self.play(FadeIn(qm), FadeIn(q.question), run_time=0.9)
        self.at("Watch the two")
        self.play(Indicate(world.meters[0], color=YELLOW), Indicate(world.meters[1], color=YELLOW), run_time=1.2)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Which patch receives more light at ground level?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 30}
    def backdrop(self):
        w = canopy_comparison(gap=True)
        for i, tree in enumerate(list(w.left_trees[1:4]) + list(w.right_trees[1:3])):
            bob(tree, amp=0.12, speed=3.2 + 0.2 * i, seed=i)
        w.add(T("?", 64, YELLOW, weight=BOLD).move_to([0, 0.15, 0]))
        return w


class S05Reveal(SpokenScene):
    def construct(self):
        world = canopy_comparison(gap=True)
        for i, tree in enumerate(list(world.left_trees[1:4]) + list(world.right_trees[1:3])):
            bob(tree, amp=0.12, speed=3.2 + 0.2 * i, seed=i)
        self.add(world)
        self.at("The gap meter")
        self.play(world.right_meter.animate.set_value(0.88), run_time=1.4)
        self.at("Saplings already")
        young = VGroup(oak(2.9, -1.6, 0.55, 0.28), oak(3.65, -1.6, 0.48, 0.25))
        self.play(FadeIn(young, shift=UP * 0.1), run_time=0.7)
        self.play(*[s.animate.scale(1.65, about_point=s.get_bottom()) for s in young], run_time=2.0)
        self.at("while older trees")
        self.play(Indicate(VGroup(world.right_trees[1], world.right_trees[2]), color=HARD), run_time=1.0)
        self.at("The forest now")
        landscape = virginia_landscape(stages=("field", "pine", "young", "mixed"))
        self.play(FadeOut(world), FadeOut(young), FadeIn(landscape), run_time=1.5)
        self.at("A disturbance can redirect")
        outline = patch_frame(2, RED, 1.0)
        self.play(Create(outline), run_time=1.0)
        self.play(Indicate(landscape.plants[2], color=RED, scale_factor=1.06), run_time=1.1)
        self.finish()


class S06Scale(SpokenScene):
    def construct(self):
        world = virginia_landscape()
        self.add(world, scope_tag("schematic"))
        self.at("Storms insects")
        ripples = VGroup(*[Circle(radius=0.25, color=RED, stroke_width=4).move_to([PATCH_X[i], 0.2 + 0.35 * (i % 2), 0])
                           for i in range(4)])
        self.play(LaggedStart(*[Create(r) for r in ripples], lag_ratio=0.25), run_time=2.4)
        self.at("Some patches change")
        quick = patch_plants(0, "young")
        self.play(Transform(world.plants[0], quick), run_time=1.3)
        self.at("Others remain")
        self.play(Indicate(world.plants[3], color=HARD, scale_factor=1.02), run_time=1.2)
        self.at("Together they form")
        loop = CurvedArrow([4.8, 2.5, 0], [-4.8, 2.5, 0], angle=-0.45, color=BLUE, stroke_width=5)
        lab = T("different histories", 32, BLUE).move_to([0, 3.2, 0])
        self.play(Create(loop), FadeIn(lab), run_time=1.4)
        self.at("not one community")
        self.play(LaggedStart(*[Indicate(patch_frame(i), color=BLUE, scale_factor=1.02) for i in range(4)],
                              lag_ratio=0.2), run_time=1.8)
        self.finish()


class S07Climax(SpokenScene):
    def construct(self):
        world = virginia_landscape()
        self.add(world)
        self.at("Older models called")
        frame = patch_frame(3, BLUE, 1.0)
        label = fit_text("climax community: model late stage", 6.0, 30, BLUE).move_to([2.8, 3.15, 0])
        self.play(Create(frame), FadeIn(label), run_time=1.2)
        self.at("For most of Virginia")
        oaklab = T("oak–hickory", 30, HARD).move_to([4.75, 2.45, 0])
        self.play(FadeIn(oaklab), Indicate(world.plants[3], color=HARD), run_time=1.2)
        self.at("useful as a prediction")
        arrow = DashedVMobject(Arrow([0.4, 1.2, 0], [3.2, 1.2, 0], color=BLUE, buff=0.1,
                                     stroke_width=5, tip_length=0.2), num_dashes=10)
        self.play(Create(arrow), run_time=1.1)
        self.at("not a claim")
        tree = world.plants[3][0]
        self.play(Rotate(tree, angle=-PI / 2.3, about_point=tree.get_bottom()), run_time=1.2)
        gapfill = tufts(4.15, GROUND_Y, 4, 0.45, HARD)
        loop = CurvedArrow([3.3, -0.2, 0], [5.3, -0.2, 0], angle=-1.2, color=YELLOW, stroke_width=4)
        notfinish = T("not a finish line", 28, YELLOW).move_to([4.2, -3.0, 0])
        self.play(FadeIn(gapfill, shift=UP * 0.1), Create(loop), FadeIn(notfinish), run_time=1.3)
        self.finish()


class S08Path(SpokenScene):
    def construct(self):
        title = T("possible routes", 38, BLUE, font=TITLE_FONT).move_to([0, 3.2, 0])
        stem = Arrow([0, 2.65, 0], [0, 1.65, 0], color=BLUE, buff=0, stroke_width=5)
        branches = VGroup(Arrow([0, 1.65, 0], [-3.2, 0.75, 0], color=BLUE, buff=0.05, stroke_width=5),
                          Arrow([0, 1.65, 0], [3.2, 0.75, 0], color=BLUE, buff=0.05, stroke_width=5))
        self.play(FadeIn(title), GrowArrow(stem), run_time=0.8)
        self.at("Without fire")
        self.play(GrowArrow(branches[0]), run_time=0.8)
        shade = Rectangle(width=5.4, height=3.2, stroke_color=GREY, fill_color=GREY,
                          fill_opacity=0.12).move_to([-3.25, -0.75, 0])
        mix = VGroup(oak(-4.2, -2.1, 1.55, 0.65), oak(-3.0, -2.1, 1.35, 0.58, RED),
                     oak(-1.95, -2.1, 1.45, 0.61))
        can = chip("can: red maple mixes in", RED, 28).move_to([-3.2, -2.95, 0])
        self.play(FadeIn(shade), FadeIn(mix, lag_ratio=0.15), FadeIn(can), run_time=1.5)
        bob(mix[1], amp=0.08, speed=1.0)
        self.at("Elsewhere disturbance")
        self.play(GrowArrow(branches[1]), run_time=0.7)
        mark = disturbance_mark(3, "fire").move_to([3.2, 0.2, 0])
        other = VGroup(pine(2.25, -2.1, 1.7, 0.8), oak(3.25, -2.1, 1.3, 0.55),
                       tufts(4.2, -2.1, 5, 0.8))
        may = chip("may: a different mix", RED, 28).move_to([3.2, -2.95, 0])
        self.play(FadeIn(mark), FadeIn(other, lag_ratio=0.12), FadeIn(may), run_time=1.5)
        bob(other[1], amp=0.08, speed=1.15)
        self.at("The result depends")
        deps = VGroup(T("disturbance", 28, RED), T("nearby organisms", 28, TEXT),
                      T("conditions left", 28, SOIL)).arrange(RIGHT, buff=1.0).move_to([0, 2.6, 0])
        self.play(FadeOut(title), FadeOut(stem), FadeOut(branches), FadeOut(mark), FadeIn(deps), run_time=1.2)
        bob(deps, amp=0.10, speed=3.0)
        self.finish()


class S09Evidence(SpokenScene):
    def construct(self):
        self.at("How can ecologists")
        q = T("How common is this path?", 46, YELLOW, font=TITLE_FONT).move_to([0, 2.9, 0])
        self.play(Write(q), run_time=1.2)
        cards = VGroup(*[RoundedRectangle(corner_radius=0.12, width=3.2, height=2.1, stroke_color=BLUE,
                                         stroke_width=2.5, fill_color=BLUE, fill_opacity=0.05)
                         .move_to([-2.2 + i * 1.1, -0.25 - i * 0.25, 0]) for i in range(4)])
        for i, c in enumerate(cards):
            c.set_opacity(0.22 + 0.12 * i)
        self.at("One source presents")
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.12), run_time=1.0)
        big = summary_card((0, -0.2, 0), 8.2, 5.0)
        pulse(big[0], base=4.0, amp=1.2, speed=1.6)
        self.play(TransformFromCopy(cards[-1], big), FadeOut(q), run_time=1.3)
        self.at("usual Piedmont")
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.05) for m in big[2][::2]], lag_ratio=0.25), run_time=1.5)
        self.at("pattern not")
        pat = T("pattern — not one field’s dated history", 30, YELLOW).move_to([0, -3.05, 0])
        self.play(FadeIn(pat), cards.animate.set_opacity(0.12), run_time=0.9)
        self.finish()


class S10Plot(SpokenScene):
    def construct(self):
        summary = summary_card((-3.65, 0.25, 0), 5.7, 5.4).scale(0.88)
        pulse(summary[0], base=4.0, amp=1.2, speed=1.5)
        self.add(summary)
        self.at("Another source marks")
        plot = permanent_plot((3.55, 0.2, 0), (LIME, LIME, PINE))
        pulse(plot[0], base=5.0, amp=1.3, speed=1.7)
        for i, p in enumerate(plot[2]):
            bob(p, amp=0.12, speed=3.2 + 0.2 * i, seed=i)
        label = T("same place, repeated record", 28, BLUE).move_to([3.55, 2.75, 0])
        self.play(Create(plot[0]), FadeIn(plot[1]), FadeIn(label), run_time=1.3)
        self.play(FadeIn(plot[2], lag_ratio=0.12), run_time=1.0)
        self.at("At Glacier Bay")
        gb = T("Glacier Bay", 30, TEXT).move_to([3.55, -2.25, 0])
        self.play(FadeIn(gb), run_time=0.5)
        self.at("resurveys found")
        later = permanent_plot((3.55, 0.2, 0), (PINE, HARD, LIME))
        self.play(Transform(plot[2], later[2]), run_time=1.5)
        self.at("Early arrivals")
        self.play(Indicate(plot[2][0], color=YELLOW), Indicate(plot[2][1], color=YELLOW), run_time=1.2)
        self.at("One plot gives")
        mini = VGroup(*[permanent_plot((-1.1 + 2.25 * i, -2.65, 0), mix).scale(0.34)
                        for i, mix in enumerate(((LIME, PINE), (PINE, HARD), (HARD, LIME, PINE)))])
        varied = T("timing varied", 30, YELLOW).move_to([3.55, 3.15, 0])
        self.play(FadeOut(label), FadeOut(gb), FadeIn(varied),
                  LaggedStart(*[FadeIn(p) for p in mini], lag_ratio=0.2), run_time=1.4)
        self.finish()


class S11Compare(SpokenScene):
    def construct(self):
        summary = summary_card((-3.6, 0.45, 0), 5.4, 4.7).scale(0.8)
        plot = permanent_plot((3.6, 0.45, 0), (LIME, PINE, HARD)).scale(0.72)
        pulse(summary[0], base=4.0, amp=1.2, speed=1.5)
        pulse(plot[0], base=5.0, amp=1.3, speed=1.7)
        for i, p in enumerate(plot[2]):
            bob(p, amp=0.12, speed=3.2 + 0.2 * i, seed=i)
        self.at("Use each source")
        self.play(FadeIn(summary), FadeIn(plot), run_time=1.2)
        self.at("A regional summary")
        broad = T("broad tendency", 30, BLUE).move_to([-3.6, -2.05, 0])
        self.play(FadeIn(broad), Indicate(summary, color=BLUE), run_time=1.0)
        self.at("A dated plot")
        detail = T("one place in detail", 30, BLUE).move_to([3.6, -2.05, 0])
        self.play(FadeIn(detail), Indicate(plot, color=BLUE), run_time=1.0)
        model = RoundedRectangle(corner_radius=0.18, width=4.0, height=1.0, stroke_color=YELLOW,
                                 stroke_width=4).move_to([0, -3.05, 0])
        mlab = T("model scope", 30, YELLOW).move_to(model)
        arrows = VGroup(Arrow([-3.0, -2.35, 0], [-1.7, -2.8, 0], color=BLUE, buff=0.1),
                        Arrow([3.0, -2.35, 0], [1.7, -2.8, 0], color=BLUE, buff=0.1))
        self.at("Agreement can")
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), Create(model), FadeIn(mlab), run_time=1.2)
        self.play(model.animate.stretch_to_fit_width(5.1), run_time=0.8)
        self.at("Differences reveal")
        self.play(model.animate.stretch_to_fit_width(3.2), run_time=1.2)
        self.finish()


class S12Biodiversity(SpokenScene):
    def construct(self):
        world = virginia_landscape()
        self.add(world)
        self.at("Succession also changes")
        label = T("biodiversity = variety of living things", 36, BLUE).move_to([0, 3.2, 0])
        self.play(FadeIn(label), run_time=1.0)
        quadrat = Square(2.35, stroke_color=BLUE, stroke_width=5).move_to([PATCH_X[0], -0.65, 0])
        qlab = T("sampled patch", 28, BLUE).next_to(quadrat, UP, buff=0.12)
        tally = VGroup(T("species count", 30, YELLOW),
                       VGroup(*[Dot(radius=0.12, color=c) for c in (LIME, PINE, HARD, RED)]).arrange(RIGHT, buff=0.18))
        tally.arrange(DOWN, buff=0.18).move_to([4.65, 2.55, 0])
        self.play(Create(quadrat), FadeIn(qlab), run_time=0.8)
        self.at("A species count")
        self.play(FadeIn(tally[0]), FadeIn(VGroup(*tally[1][:2])), run_time=0.8)
        self.play(quadrat.animate.move_to([PATCH_X[1], -0.65, 0]), qlab.animate.move_to([PATCH_X[1], 0.72, 0]),
                  FadeIn(VGroup(*tally[1][2:])), run_time=1.4)
        self.play(quadrat.animate.move_to([PATCH_X[2], -0.65, 0]), qlab.animate.move_to([PATCH_X[2], 0.72, 0]),
                  FadeOut(tally[1][-1]), run_time=1.3)
        self.at("Scientists must name")
        self.play(Indicate(tally[0], color=YELLOW), Indicate(qlab, color=BLUE), run_time=1.4)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        world = virginia_landscape()
        self.add(world, scope_tag("schematic"))
        old = T("What stage comes next?", 42, GREY, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.at("Do not ask only")
        self.play(FadeIn(old), run_time=0.8)
        self.play(FadeOut(old), run_time=0.6)
        prompts = [T("What changed?", 34, RED).move_to([-4.5, 2.95, 0]),
                   T("What remained?", 34, SOIL).move_to([0, 2.95, 0]),
                   T("What evidence?", 34, BLUE).move_to([4.45, 2.95, 0])]
        targets = [world.plants[0], world.plants[2], world.plants[3]]
        arrows = [Arrow(p.get_bottom(), t.get_top(), color=c, buff=0.12, stroke_width=4)
                  for p, t, c in zip(prompts, targets, (RED, SOIL, BLUE))]
        for phrase, p, a in zip(("Ask what changed", "what remained", "what evidence"), prompts, arrows):
            self.at(phrase)
            self.play(FadeIn(p), GrowArrow(a), run_time=0.75)
        self.at("This connects succession")
        routes = VGroup(*[CurvedArrow([PATCH_X[i], -0.9, 0], [PATCH_X[i + 1], -0.9, 0],
                                      angle=(-0.35 if i % 2 else 0.35), color=YELLOW, stroke_width=4)
                          for i in range(3)])
        self.play(LaggedStart(*[Create(a) for a in routes], lag_ratio=0.25), run_time=1.7)
        self.finish()


class S14End(EndCard):
    LINE = "Disturbance can redirect succession, leaving a patchwork of stages."
