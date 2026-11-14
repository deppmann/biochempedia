"""Build the Classification Path — chapter two of Domains and Kingdoms.

COLOR MAP (shared with the chapter-one script)
  GOLD  = Eukarya, its organisms, and the Eukarya decision path
  BLUE  = Bacteria
  TEAL  = Archaea
  TEXT  = trait evidence and questions
  RED   = limits and stop markers
  GREY  = neutral outlines and inactive paths
"""
from bp_parts import *  # noqa: F401,F403


# --------------------------------------------------------------------------------------
# Carried world and lesson-specific cartoons. Every continued picture is rebuilt here.

def stage_panel():
    """The shared decision field: a quiet, full-frame diagram surface, not evidence."""
    panel = RoundedRectangle(width=12.9, height=6.45, corner_radius=0.28, stroke_color=GOLD,
                             stroke_width=0, stroke_opacity=0,
                             fill_color=GOLD, fill_opacity=0.12)
    ribbon = Polygon([-6.45, -2.8, 0], [-6.45, -1.4, 0], [6.45, 1.4, 0], [6.45, 2.8, 0],
                     stroke_width=0, fill_color=GOLD, fill_opacity=0.16).set_z_index(-4)
    return VGroup(panel.set_z_index(-5), ribbon)


class PathScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(stage_panel())

def path_line(points, color=GOLD, width=18, opacity=1):
    line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    line.set_points_as_corners([np.array([x, y, 0.0]) for x, y in points])
    return pulse(line, base=width, amp=min(5, width * 0.16), speed=1.35)


def pond_drop():
    drop = Ellipse(width=6.4, height=6.3, stroke_color=TEXT, stroke_width=4,
                   fill_color=BLUE, fill_opacity=0.08).move_to([-1.7, -0.15, 0])
    cells = VGroup(
        Circle(0.55, color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.25).move_to([-3.1, 1.15, 0]),
        RoundedRectangle(width=1.15, height=0.7, corner_radius=0.32, color=TEAL, stroke_width=5,
                         fill_color=TEAL, fill_opacity=0.25).move_to([-0.35, 0.75, 0]),
        Circle(0.72, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.22).move_to([-1.9, -1.35, 0]),
    )
    nucleus = Circle(0.25, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.45)
    nucleus.move_to(cells[2])
    return VGroup(drop, cells, nucleus)


def gold_route(y=0):
    return path_line([(-6.4, y), (6.4, y)], GOLD, 56, 0.38)


def nucleus_badge(at=ORIGIN, scale=1):
    outer = Circle(0.55 * scale, color=GOLD, stroke_width=4,
                   fill_color=GOLD, fill_opacity=0.12).move_to(at)
    inner = Circle(0.22 * scale, color=GOLD, stroke_width=4,
                   fill_color=GOLD, fill_opacity=0.45).move_to(at)
    return VGroup(outer, inner)


def plant_cartoon(at=ORIGIN, scale=1.0):
    stem = Line(DOWN * 1.15, UP * 0.95, color=GOLD, stroke_width=10)
    crown = VGroup(
        Ellipse(width=1.4, height=0.75, color=GOLD, fill_color=GOLD, fill_opacity=0.32).rotate(0.35).shift(LEFT * 0.48 + UP * 0.45),
        Ellipse(width=1.4, height=0.75, color=GOLD, fill_color=GOLD, fill_opacity=0.32).rotate(-0.35).shift(RIGHT * 0.48 + UP * 0.45),
        Ellipse(width=1.2, height=0.8, color=GOLD, fill_color=GOLD, fill_opacity=0.32).shift(UP * 0.95),
    )
    roots = VGroup(Line(DOWN * 1.1, DOWN * 1.45 + LEFT * 0.45, color=GOLD, stroke_width=7),
                   Line(DOWN * 1.1, DOWN * 1.45 + RIGHT * 0.45, color=GOLD, stroke_width=7))
    return VGroup(stem, crown, roots).scale(scale).move_to(at)


def mushroom_cartoon(at=ORIGIN, scale=1.0):
    stalk = RoundedRectangle(width=0.75, height=1.8, corner_radius=0.3, color=GOLD,
                             fill_color=GOLD, fill_opacity=0.22).shift(DOWN * 0.35)
    cap = ArcBetweenPoints(LEFT * 1.25, RIGHT * 1.25, angle=-PI).set_stroke(GOLD, 7)
    brim = Line(LEFT * 1.25, RIGHT * 1.25, color=GOLD, stroke_width=7)
    capg = VGroup(cap, brim).shift(UP * 0.62)
    return VGroup(stalk, capg).scale(scale).move_to(at)


def crab_cartoon(at=ORIGIN, scale=1.0):
    body = Ellipse(width=2.3, height=1.25, color=GOLD, stroke_width=6,
                   fill_color=GOLD, fill_opacity=0.24)
    eyes = VGroup(Dot([-0.45, 0.35, 0], radius=0.09, color=TEXT),
                  Dot([0.45, 0.35, 0], radius=0.09, color=TEXT))
    legs = VGroup(*[Line([sx * 0.7, sy * 0.25, 0], [sx * (1.55 + 0.15 * i), sy * (0.7 + 0.15 * i), 0],
                               color=GOLD, stroke_width=6)
                    for i, sy in enumerate((-1, 1)) for sx in (-1, 1)])
    claws = VGroup(Arc(radius=0.35, start_angle=0, angle=PI, color=GOLD, stroke_width=6).move_to([-1.65, 0.8, 0]),
                   Arc(radius=0.35, start_angle=0, angle=PI, color=GOLD, stroke_width=6).move_to([1.65, 0.8, 0]))
    return VGroup(legs, claws, body, eyes).scale(scale).move_to(at)


def paramecium(at=ORIGIN, scale=1.0, color=GOLD):
    body = Ellipse(width=2.6, height=1.35, color=color, stroke_width=6,
                   fill_color=color, fill_opacity=0.2).rotate(0.2)
    nucleus = Circle(0.28, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.4)
    hairs = VGroup(*[Line([1.15 * np.cos(a), 0.58 * np.sin(a), 0],
                              [1.35 * np.cos(a), 0.73 * np.sin(a), 0], color=TEXT, stroke_width=2)
                     for a in np.linspace(0, TAU, 18, endpoint=False)])
    return VGroup(hairs, body, nucleus).scale(scale).move_to(at)


def kelp_cartoon(at=ORIGIN, scale=1.0):
    stems = VGroup(*[CubicBezier([x, -1.5, 0], [x - 0.2, -0.4, 0], [x + 0.35, 0.4, 0], [x, 1.5, 0])
                     .set_stroke(GOLD, 9) for x in (-0.55, 0, 0.55)])
    blades = VGroup(*[Ellipse(width=0.65, height=1.2, color=GOLD, fill_color=GOLD, fill_opacity=0.25)
                      .rotate(a).move_to([x, y, 0])
                      for x, y, a in [(-0.8, 0.4, 0.5), (0.75, 0.65, -0.5), (-0.55, 1.2, 0.4), (0.5, 1.35, -0.4)]])
    return VGroup(stems, blades).scale(scale).move_to(at)


def trait_gate(label, at, color=TEXT, width=2.35):
    frame = RoundedRectangle(width=width, height=1.0, corner_radius=0.16, color=color,
                             stroke_width=4, fill_color=color, fill_opacity=0.11).move_to(at)
    lab = fit_text(label, max_w=width - 0.25, size=29, color=color, min_size=24, max_lines=1).move_to(frame)
    lab.layout_ok = True  # Intentional text inside its gate.
    return VGroup(frame, lab)


def predict_world():
    route = gold_route(-0.15)
    mushroom = mushroom_cartoon([-3.6, 1.3, 0], 0.9)
    plant = plant_cartoon([3.6, 1.25, 0], 0.9)
    gates = VGroup(trait_gate("movement", [-3.7, -1.2, 0]),
                   trait_gate("wall material", [0, -1.2, 0], width=2.8),
                   trait_gate("feeding", [3.7, -1.2, 0]))
    return VGroup(route, mushroom, plant, gates)


def fork_key_world():
    root = np.array([-5.8, 0.0, 0])
    joints = [np.array([-3.4, 0, 0]), np.array([-0.9, 0, 0]), np.array([1.6, 0, 0])]
    ends = [np.array([-3.4, 2.2, 0]), np.array([-0.9, 2.2, 0]), np.array([1.6, 2.2, 0]), np.array([3.35, 1.55, 0]), np.array([3.35, -1.55, 0])]
    lines = VGroup(Line(root, joints[0], color=GOLD, stroke_width=12),
                   Line(joints[0], ends[0], color=GOLD, stroke_width=10),
                   Line(joints[0], joints[1], color=GOLD, stroke_width=10),
                   Line(joints[1], ends[1], color=GOLD, stroke_width=10),
                   Line(joints[1], joints[2], color=GOLD, stroke_width=10),
                   Line(joints[2], ends[2], color=GOLD, stroke_width=10),
                   Line(joints[2], ends[3], color=GOLD, stroke_width=10),
                   Line(joints[2], ends[4], color=GOLD, stroke_width=10))
    qs = VGroup(*[Circle(0.23, color=TEXT, fill_color=TEXT, fill_opacity=1).move_to(p) for p in joints])
    return VGroup(lines, qs)


# --------------------------------------------------------------------------------------
class S00Hook(PathScene):
    def construct(self):
        world = pond_drop()
        blue = path_line([(-0.3, 0.75), (5.9, 2.15)], BLUE, 16, 0.75)
        teal = path_line([(-0.3, 0.75), (5.9, 0.35)], TEAL, 16, 0.75)
        gold = path_line([(-1.7, -1.35), (5.9, -1.65)], GOLD, 18, 0.8)
        self.at("first film")
        self.play(FadeIn(world), Create(VGroup(blue, teal, gold)), run_time=1.0)
        bob(world[1][0], amp=0.07, speed=1.2)
        bob(world[1][1], amp=0.06, speed=1.0, seed=2)
        bob(world[1][2], amp=0.08, speed=1.1, seed=4)
        self.at("Which traits")
        question = fit_text("Which traits finish the Eukarya path?", 5.8, 38, TEXT).move_to([2.8, 2.95, 0])
        self.play(FadeIn(question, shift=DOWN * 0.15), run_time=0.7)
        self.at("Follow the gold")
        self.play(FadeOut(blue, shift=UP * 0.4), FadeOut(teal, shift=UP * 0.2),
                  gold.animate.set_stroke(width=30).shift(UP * 0.7), run_time=1.0)
        self.at("cells have nuclei")
        badge = nucleus_badge([2.4, -0.95, 0], 1.3)
        label = T("nucleus", 30, GOLD).next_to(badge, RIGHT, buff=0.3).shift(DOWN * 0.24)
        self.play(GrowFromCenter(badge), FadeIn(label), run_time=0.8)
        self.at("does not reveal")
        unknown = T("kingdom  ?", 38, TEXT, weight=BOLD).move_to([4.35, 0.25, 0])
        self.play(FadeIn(unknown, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Domains and Kingdoms"
    TITLE = "Build the Classification Path"

    def construct(self):
        route = gold_route(-1.65).set_opacity(0.35)
        glow = Dot([-6.2, -1.65, 0], radius=0.18, color=GOLD)
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = fit_text(self.TITLE, 11.5, 54, TEXT, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        words = VGroup(lesson, title, rule).arrange(DOWN, buff=0.34)
        self.add(route)
        self.play(FadeIn(words), glow.animate.shift(RIGHT * 12.4), run_time=1.3, rate_func=linear)
        self.play(FadeOut(words), FadeOut(route), FadeOut(glow), run_time=0.45)
        self.finish()


class S02Questions(PathScene):
    def construct(self):
        route = gold_route(0)
        travelers = VGroup(plant_cartoon([-4.9, 1.4, 0], 0.45), mushroom_cartoon([-4.0, 1.35, 0], 0.45),
                           crab_cartoon([-3.0, 1.35, 0], 0.38), paramecium([-1.9, 1.35, 0], 0.4))
        self.at("kingdom is")
        self.play(Create(route), FadeIn(travelers, shift=RIGHT * 0.2), run_time=0.9)
        rank = T("DOMAIN  →  KINGDOM", 36, GOLD, weight=BOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(rank), run_time=0.6)
        self.at("Eukarya holds")
        names = T("protists   fungi   plants   animals", 32, GOLD).move_to([0, 2.35, 0])
        self.play(FadeIn(names), travelers.animate.shift(RIGHT * 2.2), run_time=0.8)
        for phrase, label in [("cell number", "cells"), ("wall material", "wall"), ("tissues", "tissues"), ("feeding", "feeding")]:
            self.at(phrase)
            gate = trait_gate(label, [4.8, 0, 0], width=2.5)
            self.play(FadeIn(gate, shift=RIGHT * 0.2), travelers.animate.shift(RIGHT * 0.45), run_time=0.55)
            self.play(FadeOut(gate, shift=LEFT * 0.15), run_time=0.25)
        self.at("Answers work together")
        brace = SurroundingRectangle(travelers, color=TEXT, buff=0.25, corner_radius=0.15)
        together = T("use the pattern", 30, TEXT).move_to([0, -2.65, 0])
        self.play(FadeOut(names), Create(brace), FadeIn(together), run_time=0.7)
        self.at("appearances can mislead")
        self.play(Indicate(brace, color=RED, scale_factor=1.03), run_time=0.8)
        self.finish()


class S03PlantsFungi(PathScene):
    def construct(self):
        nucleus = nucleus_badge([0, 2.6, 0], 1.0)
        plant = plant_cartoon([-3.5, 0.25, 0], 1.05)
        fungus = mushroom_cartoon([3.5, 0.25, 0], 1.05)
        branches = VGroup(Line([0, 2.05, 0], [-3.5, 1.55, 0], color=GOLD, stroke_width=10),
                          Line([0, 2.05, 0], [3.5, 1.55, 0], color=GOLD, stroke_width=10))
        self.at("Begin with plants")
        self.play(GrowFromCenter(nucleus), Create(branches[0]), GrowFromCenter(plant), run_time=0.9)
        bob(plant, amp=0.035, speed=1.0)
        self.at("many cells")
        wall_p = SurroundingRectangle(plant, color=TEXT, buff=0.22, corner_radius=0.18)
        self.play(Create(wall_p), run_time=0.5)
        self.at("cellulose walls")
        cellulose = chip("cellulose", TEXT, 28).move_to([-3.5, -2.15, 0])
        self.play(FadeIn(cellulose), run_time=0.5)
        self.at("Most photosynthesize")
        sun = Dot([-5.8, 2.15, 0], radius=0.34, color=GOLD)
        light = Arrow(sun, plant.get_top(), color=TEXT, stroke_width=5, buff=0.15)
        self.play(FadeIn(sun), GrowArrow(light), run_time=0.7)
        self.at("Fungi can also")
        self.play(Create(branches[1]), GrowFromCenter(fungus), run_time=0.8)
        bob(fungus, amp=0.035, speed=1.1, seed=3)
        self.at("walls contain chitin")
        wall_f = SurroundingRectangle(fungus, color=TEXT, buff=0.22, corner_radius=0.18)
        chitin = chip("chitin", TEXT, 28).move_to([3.5, -2.15, 0])
        self.play(Create(wall_f), FadeIn(chitin), run_time=0.7)
        self.at("digest food outside")
        food = VGroup(*[Dot([5.6, y, 0], radius=0.13, color=TEXT) for y in (-0.6, 0, 0.6)])
        inward = Arrow([5.2, 0, 0], fungus.get_right(), color=TEXT, stroke_width=5, buff=0.1)
        self.play(FadeIn(food), GrowArrow(inward), food.animate.shift(LEFT * 1.3), run_time=0.9)
        self.finish()


class S04Predict(PathScene):
    def construct(self):
        world = predict_world()
        self.at("oyster mushroom")
        self.play(FadeIn(world[0]), GrowFromCenter(world[1]), GrowFromCenter(world[2]), run_time=0.9)
        bob(world[1], amp=0.04, speed=1.1)
        bob(world[2], amp=0.05, speed=1.0, seed=3)
        self.at("Both have nuclei")
        shared = T("nuclei  •  many cells  •  walls", 30, GOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(shared), run_time=0.6)
        self.at("which traits")
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.15) for g in world[3]], lag_ratio=0.2), run_time=1.0)
        self.at("Choose before")
        q = question_card("Which traits separate their paths?", y=-3.12, size=30)
        self.play(FadeIn(q), run_time=0.6)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which traits separate their paths?"
    SECONDS = 4.5

    def backdrop(self):
        shared = T("nuclei  •  many cells  •  walls", 30, GOLD).move_to([0, 3.0, 0])
        return VGroup(stage_panel(), predict_world(), shared)


class S06Reveal(PathScene):
    def construct(self):
        world = predict_world()
        self.add(world)
        bob(world[1], amp=0.035, speed=1.0)
        bob(world[2], amp=0.04, speed=1.1, seed=2)
        self.at("Movement is unreliable")
        movement = world[3][0]
        weak = T("unreliable", 28, GREY).move_to(movement).shift(LEFT * 1.15)
        weak.layout_ok = True
        self.play(FadeOut(movement), FadeIn(weak), run_time=0.8)
        self.at("mushroom follows")
        left_track = path_line([(-3.6, -0.1), (-3.6, -1.85), (-5.0, -1.85)], GOLD, 14)
        fungus = chip("FUNGI", GOLD, 30).move_to([-5.45, -2.75, 0])
        self.play(FadeOut(world[3][1]), Create(left_track), FadeIn(fungus), run_time=0.8)
        self.at("chitin and absorption")
        evidence_l = VGroup(chip("chitin", TEXT, 26), chip("absorption", TEXT, 26)).arrange(RIGHT, buff=0.2).move_to([-2.55, -2.75, 0])
        self.play(FadeIn(evidence_l), run_time=0.7)
        self.at("plant follows")
        right_track = path_line([(3.6, -0.1), (3.6, -1.85), (4.25, -1.85)], GOLD, 14)
        plants = chip("PLANTS", GOLD, 30).move_to([5.35, -2.11, 0])
        self.play(FadeOut(world[3][2]), Create(right_track), FadeIn(plants), run_time=0.8)
        self.at("cellulose")
        evidence_r = VGroup(T("cellulose  •  tissues", 28, TEXT), T("photosynthesis", 28, TEXT))
        evidence_r.arrange(DOWN, buff=0.08).move_to([2.55, -2.7, 0])
        self.play(FadeIn(evidence_r), run_time=0.8)
        self.at("familiar trait fails")
        world[3][2].set_z_index(3)
        self.add(world[3][1], world[3][2])
        self.play(FadeOut(weak), world[3][1][0].animate.set_stroke(color=TEXT, width=7),
                  world[3][2][0].animate.set_stroke(color=TEXT, width=7).set_fill(BG, opacity=1),
                  run_time=0.7)
        self.at("Wall material and feeding")
        settle = T("wall + feeding settle the split", 34, TEXT, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(settle), run_time=0.7)
        self.finish()


class S07AnimalsProtists(PathScene):
    def construct(self):
        route = gold_route(-0.15)
        gates = VGroup(trait_gate("no wall", [-2.6, -0.15, 0]), trait_gate("ingests", [0.5, -0.15, 0]))
        crab = crab_cartoon([-5.0, 1.5, 0], 0.75)
        self.at("Animals have")
        self.play(Create(route), GrowFromCenter(crab), run_time=0.8)
        self.at("no cell walls")
        self.play(FadeIn(gates[0]), crab.animate.shift(RIGHT * 2.2), run_time=0.7)
        self.at("ingest food")
        self.play(FadeIn(gates[1]), crab.animate.shift(RIGHT * 2.7), run_time=0.7)
        self.at("usually form tissues")
        animal = chip("ANIMALS", GOLD, 30).move_to([4.9, 1.45, 0])
        self.play(crab.animate.move_to([4.9, 0.25, 0]), FadeIn(animal), run_time=0.8)
        bob(crab, amp=0.045, speed=1.2)
        self.at("Sponges are")
        special = T("tissues: special case", 28, TEXT).move_to([4.9, -0.85, 0])
        self.play(FadeIn(special), run_time=0.6)
        self.at("other eukaryotes")
        para = paramecium([-4.6, -1.65, 0], 0.58)
        kelp = kelp_cartoon([-2.2, -1.55, 0], 0.55)
        remaining = path_line([(-5.5, -2.45), (3.3, -2.45)], GOLD, 14)
        self.play(Create(remaining), FadeIn(para), FadeIn(kelp), run_time=0.9)
        self.at("go with protists")
        protists = chip("PROTISTS", GOLD, 30).move_to([4.8, -2.45, 0])
        scope = scope_tag("six-kingdom scheme", 24, GREY)
        self.play(para.animate.shift(RIGHT * 5.7), kelp.animate.shift(RIGHT * 4.1), FadeIn(protists), FadeIn(scope), run_time=1.0)
        self.at("Most are one cell")
        self.play(Indicate(para, color=TEXT), run_time=0.6)
        self.at("multicellular algae")
        self.play(Indicate(kelp, color=TEXT), run_time=0.6)
        self.finish()


class S08Feeding(PathScene):
    def construct(self):
        cell = paramecium([0, 0.15, 0], 1.25, color=GOLD)
        route = path_line([(-5.8, -2.0), (5.8, -2.0)], GOLD, 18, 0.6)
        self.at("vary in feeding")
        self.play(Create(route), GrowFromCenter(cell), run_time=0.8)
        bob(cell, amp=0.05, speed=1.1)
        sun = Dot([-5.0, 2.35, 0], radius=0.38, color=GOLD)
        light = Arrow(sun, cell.get_left() + UP * 0.45, color=TEXT, stroke_width=6, buff=0.2)
        food = VGroup(*[Dot([4.8, y, 0], radius=0.14, color=TEXT) for y in (1.4, 1.9, 2.4)])
        ingest = Arrow(food.get_left(), cell.get_right() + UP * 0.35, color=TEXT, stroke_width=6, buff=0.2)
        self.at("Some make food")
        self.play(FadeIn(sun), GrowArrow(light), run_time=0.7)
        self.at("some take it in")
        self.play(FadeIn(food), GrowArrow(ingest), food.animate.shift(LEFT * 1.1), run_time=0.7)
        self.at("some do both")
        both = T("mixed feeding", 32, TEXT, weight=BOLD).move_to([0, 2.85, 0])
        self.play(FadeIn(both), run_time=0.6)
        self.at("green photosynthesizing cell")
        green = Circle(0.42, color=GREEN, fill_color=GREEN, fill_opacity=0.45).move_to(cell.get_center())
        plant_pull = Arrow([0, -0.8, 0], [4.6, -1.75, 0], color=GREEN, stroke_width=6)
        plant_label = T("plants?", 30, GREEN).move_to([5.2, -1.1, 0])
        self.play(FadeIn(green), GrowArrow(plant_pull), FadeIn(plant_label), run_time=0.8)
        self.at("not automatically")
        tokens = VGroup(chip("nucleus", TEXT, 25), chip("one cell", TEXT, 25), chip("mixed feeding", TEXT, 25))
        tokens.arrange(RIGHT, buff=0.2).move_to([0, -2.75, 0])
        self.play(FadeIn(tokens), FadeOut(plant_pull), FadeOut(plant_label), run_time=0.9)
        self.at("full pattern matters")
        self.play(Indicate(tokens, color=GOLD, scale_factor=1.04), run_time=0.8)
        self.finish()


def plant_stage(kind):
    base = plant_cartoon([0, 0.35, 0], 1.25)
    if kind == "moss":
        picture = VGroup(*[Line([x, -0.8, 0], [x, 0.5 + 0.2 * i, 0], color=GOLD, stroke_width=10)
                           for i, x in enumerate(np.linspace(-1.5, 1.5, 7))])
        traits = "no vascular tissue  •  no seeds"
    elif kind == "fern":
        picture = VGroup(Line([0, -1.3, 0], [0, 1.4, 0], color=TEXT, stroke_width=12),
                         *[Line([0, y, 0], [s * (1.3 - abs(y) * 0.2), y + 0.45, 0], color=GOLD, stroke_width=8)
                           for y in np.linspace(-0.8, 0.9, 5) for s in (-1, 1)])
        traits = "vascular tissue  •  no seeds"
    elif kind == "conifer":
        cone = Polygon([-0.75, 1.35, 0], [0.75, 1.35, 0], [0, -1.4, 0], color=GOLD,
                       fill_color=GOLD, fill_opacity=0.25, stroke_width=6)
        picture, traits = VGroup(cone, Line([0, -1.4, 0], [0, -1.8, 0], color=GOLD, stroke_width=10)), "seeds in cones"
    else:
        flower = VGroup(*[Circle(0.5, color=GOLD, fill_color=GOLD, fill_opacity=0.28).shift(d * 0.5)
                          for d in (UP, DOWN, LEFT, RIGHT)], Dot(ORIGIN, radius=0.22, color=TEXT))
        fruit = Circle(0.48, color=GOLD, fill_color=GOLD, fill_opacity=0.42).move_to([1.8, -0.65, 0])
        picture, traits = VGroup(flower, fruit, Line([0, -0.5, 0], [0, -1.7, 0], color=GOLD, stroke_width=9)), "seeds inside fruits"
    return VGroup(picture).move_to([0, 0.25, 0]), T(traits, 32, TEXT).move_to([0, -2.45, 0])


class S09Plants(PathScene):
    def construct(self):
        route = path_line([(-5.8, 2.55), (5.8, 2.55)], GOLD, 16, 0.65)
        title = T("plant branch", 34, GOLD, weight=BOLD).move_to([0, 3.2, 0])
        self.at("plant branch")
        self.play(Create(route), FadeIn(title), run_time=0.8)
        moss, mt = plant_stage("moss")
        self.at("Mosses lack")
        self.play(GrowFromCenter(moss), FadeIn(mt), run_time=0.8)
        fern, ft = plant_stage("fern")
        self.at("Ferns have")
        self.play(ReplacementTransform(moss, fern), swap(mt, ft), run_time=0.9)
        bob(fern, amp=0.04, speed=1.1)
        self.at("spread by spores")
        spores = VGroup(*[Dot([x, 1.7 + 0.25 * np.sin(i), 0], radius=0.1, color=TEXT)
                          for i, x in enumerate(np.linspace(-2, 2, 9))])
        self.play(FadeIn(spores), spores.animate.shift(UP * 0.5), run_time=0.8)
        conifer, ct = plant_stage("conifer")
        self.at("Conifers carry")
        self.play(ReplacementTransform(fern, conifer), swap(ft, ct), FadeOut(spores), run_time=0.9)
        flower, flt = plant_stage("flower")
        self.at("Flowering plants")
        self.play(ReplacementTransform(conifer, flower), swap(ct, flt), run_time=0.9)
        self.finish()


class S10Key(PathScene):
    def construct(self):
        world = fork_key_world()
        self.at("paired choices")
        self.play(Create(world[0]), FadeIn(world[1]), run_time=1.0)
        title = T("DICHOTOMOUS KEY", 36, GOLD, weight=BOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(title), run_time=0.5)
        self.at("Each answer leads")
        tips = VGroup(*[chip(x, GOLD, 26).move_to(p) for x, p in zip(
            ("plants", "fungi", "animals", "protists", "next question"),
            ((-3.4, 2.72, 0), (-0.9, 2.72, 0), (1.6, 2.72, 0), (5.0, 1.55, 0), (5.0, -1.55, 0)))])
        self.play(FadeOut(title), LaggedStart(*[FadeIn(t) for t in tips], lag_ratio=0.15), run_time=1.0)
        self.at("works only")
        boundary = SurroundingRectangle(VGroup(world, tips), color=TEXT, buff=0.25, corner_radius=0.15)
        limit = T("built-in organisms + traits", 29, TEXT).move_to([0, -3.15, 0])
        self.play(Create(boundary), FadeIn(limit), run_time=0.8)
        self.at("evidence is missing")
        missing = tips[4]
        blank = trait_gate("evidence missing", [5.15, -1.55, 0], RED, 2.9)
        self.play(FadeOut(missing), FadeIn(blank), run_time=0.7)
        self.at("stop rather")
        stop = RegularPolygon(n=8, radius=0.62, color=RED, fill_color=RED, fill_opacity=0.28, stroke_width=6).move_to([3.15, -1.55, 0])
        stop_word = T("STOP", 26, RED, weight=BOLD).move_to(stop)
        stop_word.layout_ok = True
        self.play(GrowFromCenter(stop), FadeIn(stop_word), run_time=0.7)
        self.finish()


class S11Names(PathScene):
    def construct(self):
        ranks = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
        blocks = VGroup(*[RoundedRectangle(width=11.5 - i * 1.25, height=0.58, corner_radius=0.1,
                                           color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.12)
                          for i in range(len(ranks))]).arrange(DOWN, buff=0.06).move_to([0, 0.35, 0])
        labels = VGroup(*[T(r, 26, GOLD if i in (0, 5, 6) else TEXT).move_to(b) for i, (r, b) in enumerate(zip(ranks, blocks))])
        for lab in labels:
            lab.layout_ok = True
        self.at("Classification continues")
        self.play(FadeIn(VGroup(blocks[0], labels[0]), shift=DOWN * 0.08), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(VGroup(b, l), shift=DOWN * 0.08) for b, l in zip(blocks[1:], labels[1:])], lag_ratio=0.15), run_time=5.5)
        self.at("species name")
        self.play(FadeOut(VGroup(*blocks[:5], *labels[:5])),
                  VGroup(blocks[5], blocks[6], labels[5], labels[6]).animate.shift(UP * 1.8), run_time=0.8)
        genus = T("Callinectes", 58, TEXT, font=TITLE_FONT, slant=ITALIC)
        epithet = T("sapidus", 58, TEXT, font=TITLE_FONT, slant=ITALIC)
        name = VGroup(genus, epithet).arrange(RIGHT, buff=0.45).move_to([0, -0.5, 0])
        self.at("capitalized genus")
        self.play(Write(genus), genus.animate.shift(UP * 0.07), run_time=0.8)
        gl = T("capitalized genus", 28, GOLD).next_to(genus, DOWN, buff=0.65)
        self.play(FadeIn(gl), run_time=0.4)
        self.at("lowercase")
        self.play(Write(epithet), epithet.animate.shift(DOWN * 0.1), run_time=0.8)
        el = T("lower-case epithet", 28, GOLD).next_to(epithet, DOWN, buff=0.65)
        self.play(FadeIn(el), run_time=0.4)
        self.at("appear in italics")
        self.play(Indicate(VGroup(genus, epithet), color=GOLD, scale_factor=1.04), run_time=0.7)
        self.at("Naming records")
        record = trait_gate("recorded result", [0, -2.75, 0], TEXT, 3.2)
        self.play(FadeIn(record), run_time=0.6)
        self.at("does not supply")
        evidence = T("evidence comes first", 30, RED).next_to(record, RIGHT, buff=0.5)
        self.play(FadeIn(evidence), run_time=0.6)
        self.finish()


def evidence_table():
    rows = [
        ("archaeon", "Archaea", TEAL), ("bacterium", "Bacteria", BLUE), ("paramecium", "Protists", GOLD),
        ("mushroom", "Fungi", GOLD), ("pine + dogwood", "Plants", GOLD), ("crab", "Animals", GOLD),
    ]
    table = Ledger(rows, top_left=(-5.9, 2.45), title="evidence path (schematic)", row_h=0.7,
                   key_w=3.6, width=11.6, size=28)
    panel = RoundedRectangle(width=12.35, height=5.35, corner_radius=0.2, color=GOLD, stroke_width=3,
                             fill_color=GOLD, fill_opacity=0.06).move_to([0, 0.15, 0])
    table.add_to_back(panel)
    return table


class S12Apply(PathScene):
    def construct(self):
        table = evidence_table()
        self.at("path can sort")
        self.play(FadeIn(table), run_time=0.6)
        tracer = Dot([-5.65, 2.12, 0], radius=0.11, color=TEXT)
        self.add(tracer)
        self.play(tracer.animate.shift(RIGHT * 11.0), run_time=3.1, rate_func=linear)
        self.remove(tracer)
        self.add(scope_tag("schematic"))
        phrases = ["archaeon", "bacterium", "paramecium", "mushroom", "plants", "crab"]
        for i, phrase in enumerate(phrases):
            self.at(phrase)
            self.play(table.reveal(i), run_time=0.45)
        self.at("plants still match")
        pair = VGroup(plant_cartoon([2.6, 0.9, 0], 0.38), plant_cartoon([4.6, 0.9, 0], 0.38))
        same = T("same main traits", 26, TEXT).move_to([3.6, 2.0, 0])
        self.play(FadeIn(pair), FadeIn(same), run_time=0.7)
        self.at("division evidence")
        cone = chip("cone", TEXT, 26).move_to([2.6, -0.35, 0])
        fruit = chip("flower + fruit", TEXT, 26).move_to([4.6, -0.35, 0])
        self.play(pair[0].animate.move_to([2.6, 0.9, 0]), pair[1].animate.move_to([4.6, 0.9, 0]),
                  FadeIn(cone), FadeIn(fruit), run_time=0.9)
        self.finish()


class S13Limit(PathScene):
    def construct(self):
        table = evidence_table()
        for i in range(6):
            table.add(table.rows[i])
        self.at("scheme is simplified")
        self.play(FadeIn(table), run_time=0.7)
        self.at("deepest branches")
        paths = VGroup(path_line([(-5.8, 0.7), (5.8, 2.1)], BLUE, 22),
                       path_line([(-5.8, 0.2), (5.8, 0.2)], TEAL, 22),
                       path_line([(-5.8, -0.3), (5.8, -1.75)], GOLD, 22))
        self.play(FadeOut(table), Create(paths), run_time=0.8)
        self.at("strength is the method")
        method = T("ask  →  observe  →  follow", 34, TEXT, weight=BOLD).move_to([2.8, 3.1, 0])
        self.play(FadeIn(method), run_time=0.6)
        self.at("follow the evidence")
        dots = VGroup(Dot([5.8, 2.1, 0], radius=0.18, color=BLUE), Dot([5.8, 0.2, 0], radius=0.18, color=TEAL),
                      Dot([5.8, -1.75, 0], radius=0.18, color=GOLD))
        self.play(FadeIn(dots), dots.animate.shift(LEFT * 5.5), run_time=1.0)
        self.at("Ask traits in order")
        rule = caption("Ask traits in order; stop where your evidence runs out.", 32, TEXT, -3.15)
        self.play(FadeIn(rule), run_time=0.7)
        self.at("evidence runs out")
        stop = RegularPolygon(n=8, radius=0.55, color=RED, fill_color=RED, fill_opacity=0.3, stroke_width=5).move_to([2.9, -1.75, 0])
        self.play(GrowFromCenter(stop), run_time=0.6)
        self.finish()


class S14End(EndCard):
    LINE = "Ask traits in order; stop where your evidence runs out."
