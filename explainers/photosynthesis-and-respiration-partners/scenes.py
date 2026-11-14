"""Two Jobs in One Green Cell.

COLOR MAP: photosynthesis/chloroplast/sugar GREEN; respiration/mitochondrion RED;
oxygen/water BLUE; light/usable energy/heat YELLOW; carbon dioxide/labels GREY.
All materials are schematic labelled blocks or bubbles, never molecular structures.
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


CELL_C = np.array([0.0, -0.15, 0.0])
CHL_C = np.array([-3.15, -0.05, 0.0])
MIT_C = np.array([3.15, -0.05, 0.0])


def _drift(mob, velocity):
    """Wrap a small cytoplasm particle inside the common cell outline."""
    mob.velocity = np.array(velocity, dtype=float)

    def update(dot, dt):
        dot.shift(dot.velocity * dt)
        if dot.get_x() > 5.65:
            dot.shift(LEFT * 11.3)
        if dot.get_y() > 2.45:
            dot.shift(DOWN * 5.0)
    return mob.add_updater(update)


def cell_shell(night=False, particles=True):
    """The carried green leaf cell, always rebuilt at the same scale and position."""
    fill = "#121827" if night else GREEN
    shell = RoundedRectangle(
        corner_radius=0.72, width=12.2, height=6.15,
        stroke_color=GREEN, stroke_width=6,
        fill_color=fill, fill_opacity=0.08 if not night else 0.34,
    ).move_to(CELL_C)
    inner = RoundedRectangle(
        corner_radius=0.58, width=11.75, height=5.72,
        stroke_color=GREEN, stroke_width=2,
    ).set_opacity(0.42).move_to(CELL_C)
    # These two outlines deliberately sit behind everything inside the cell.
    shell.layout_ok = True
    inner.layout_ok = True
    group = VGroup(shell, inner)
    if particles:
        # Twenty-four visible particles make the cytoplasm itself a living, continuously
        # changing subject during narration holds (not a token pulse).
        pts = [(-5.2 + (i % 8) * 1.45, -1.85 + (i // 8) * 1.78 + 0.18*(i % 2))
               for i in range(24)]
        motes = VGroup()
        for i, (x, y) in enumerate(pts):
            d = Dot([x, y, 0], radius=0.07 + 0.008 * (i % 3), color=TEXT).set_opacity(0.34)
            motes.add(_drift(d, (0.48 + 0.06 * (i % 4), 0.025 + 0.008 * (i % 2), 0)))
        group.add(motes)
        group.motes = motes
    return group


def chloroplast(center=CHL_C, labelled=False, dim=False):
    body = Ellipse(width=3.35, height=2.1, color=GREEN, stroke_width=6,
                   fill_color=GREEN, fill_opacity=0.2).move_to(center)
    bands = VGroup(*[
        Line(center + [-1.0, y, 0], center + [1.0, y, 0], color=GREEN, stroke_width=4)
        for y in (-0.45, 0, 0.45)
    ]).set_opacity(0.75)
    body.layout_ok = True
    bands.layout_ok = True
    g = VGroup(body, bands)
    if labelled:
        lab = T("chloroplast", 30, GREEN, weight=BOLD).next_to(body, DOWN, buff=0.18)
        g.add(lab)
        g.label = lab
    if dim:
        g.set_opacity(0.38)
    return g


def mitochondrion(center=MIT_C, labelled=False, dim=False):
    body = Ellipse(width=3.25, height=2.0, color=RED, stroke_width=6,
                   fill_color=RED, fill_opacity=0.2).move_to(center)
    wave = VMobject(color=RED, stroke_width=4)
    xs = np.linspace(center[0] - 1.15, center[0] + 1.15, 45)
    wave.set_points_as_corners([np.array([x, center[1] + 0.38 * np.sin((x-center[0]) * 5.2), 0]) for x in xs])
    body.layout_ok = True
    wave.layout_ok = True
    g = VGroup(body, wave)
    if labelled:
        lab = T("mitochondrion", 30, RED, weight=BOLD).next_to(body, DOWN, buff=0.18)
        g.add(lab)
        g.label = lab
    if dim:
        g.set_opacity(0.38)
    return g


def cell_world(night=False, labels=False, dim=False):
    """The common cell picture used by every intracellular scene."""
    cell = cell_shell(night=night)
    chl = chloroplast(labelled=labels, dim=dim)
    mit = mitochondrion(labelled=labels, dim=dim)
    pulse(mit[0], base=6, amp=1.2, speed=2.1)
    # The organelles are the scene subject, so their sustained living-cell motion
    # continues while each sentence lands instead of relying on a token pulse.
    bob(chl, amp=0.14, speed=2.5, seed=0)
    bob(mit, amp=0.14, speed=2.5, seed=2)
    g = VGroup(cell, chl, mit)
    g.cell, g.chl, g.mit = cell, chl, mit
    return g


def sun(at=(-5.25, 2.55, 0), scale=1.0):
    core = Circle(radius=0.38 * scale, color=YELLOW, stroke_width=5,
                  fill_color=YELLOW, fill_opacity=0.35).move_to(at)
    rays = VGroup(*[
        Line(ORIGIN + RIGHT * 0.52 * scale, ORIGIN + RIGHT * 0.78 * scale,
             color=YELLOW, stroke_width=4).rotate(a).shift(at)
        for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    g = VGroup(core, rays)
    g.layout_ok = True  # a background symbol; labels may intentionally sit across its rays
    return g


def material(text, color, at, size=26):
    g = chip(text, color=color, size=size, pad=0.18).move_to(at)
    # A dark backing keeps the route beneath a travelling badge from crossing its letters.
    g[0].set_fill(BG, opacity=0.92)
    return g


def oxygen_bubbles(at, count=3):
    x, y, _ = at
    g = VGroup(*[
        Circle(radius=0.13 + 0.025 * (i % 2), color=BLUE, stroke_width=4,
               fill_color=BLUE, fill_opacity=0.18).move_to([x + 0.28*i, y + 0.15*(i % 2), 0])
        for i in range(count)
    ])
    # Bubbles deliberately travel beside labelled material badges on the same route.
    g.layout_ok = True
    return g


def path_arrow(start, end, color, bend=0.0, width=6):
    # Arrow is deliberately used instead of a hand-added tip: it stays compatible
    # with the pinned Manim version and remains a valid MoveAlongPath path.
    return Arrow(start, end, buff=0.0, color=color, stroke_width=width,
                 tip_length=0.22, max_tip_length_to_length_ratio=0.18)


def loop_paths():
    top = path_arrow(CHL_C + [1.25, 0.55, 0], MIT_C + [-1.25, 0.55, 0], GREEN, 0.45)
    bottom = path_arrow(MIT_C + [-1.25, -0.55, 0], CHL_C + [1.25, -0.55, 0], BLUE, -0.45)
    return VGroup(top, bottom)


def working_cell_icon():
    body = RoundedRectangle(corner_radius=0.18, width=1.45, height=0.85,
                            color=YELLOW, fill_color=YELLOW, fill_opacity=0.12)
    gear = VGroup(Circle(radius=0.17, color=YELLOW, stroke_width=4),
                  *[Line(RIGHT*0.21, RIGHT*0.31, color=YELLOW, stroke_width=4).rotate(a)
                    for a in np.linspace(0, TAU, 8, endpoint=False)])
    return VGroup(body, gear).move_to([5.1, 2.05, 0])


def question_world():
    world = cell_world()
    arrows = loop_paths()
    arrows.set_opacity(0.72)
    g = VGroup(world, arrows, sun())
    g.scale(0.84).shift(UP * 0.35)
    return g


def creek_world(night=False):
    """Simple creek bank in the same flat diagram language as the cell."""
    sky = Rectangle(width=13.0, height=2.6, stroke_width=0,
                    fill_color="#11182A" if night else BLUE, fill_opacity=0.13).move_to([0, 2.1, 0])
    water = Rectangle(width=13.0, height=3.2, stroke_width=0,
                      fill_color=BLUE, fill_opacity=0.18).move_to([0, -1.2, 0])
    xs = np.linspace(-6.4, 6.4, 100)
    surface = VMobject(color=BLUE, stroke_width=5)
    surface.phase = 0.0

    def ripple(line, dt):
        line.phase += 2.2 * dt
        line.set_points_as_corners([
            np.array([x, 0.4 + 0.09*np.sin(2.2*x + line.phase), 0]) for x in xs
        ])
    ripple(surface, 0)
    surface.add_updater(ripple)
    bank = Polygon([-6.4, 0.4, 0], [-3.9, 0.4, 0], [-2.6, -0.3, 0], [-6.4, -0.3, 0],
                   color=GREEN, fill_color=GREEN, fill_opacity=0.18, stroke_width=0)
    return VGroup(sky, water, surface, bank)


class S00Hook(SpokenScene, TitleCard):
    LESSON = "Photosynthesis and respiration partners"
    TITLE = "Two Jobs in One Green Cell"

    def construct(self):
        cell = cell_shell()
        self.play(Create(cell[0]), FadeIn(cell[1:]), run_time=1.2)
        chl = chloroplast(dim=True)
        mit = mitochondrion(dim=True)
        self.at("one green leaf cell")
        self.play(FadeIn(chl, scale=0.8), FadeIn(mit, scale=0.8), run_time=1.1)
        q = T("?", 92, YELLOW, weight=BOLD).move_to([0, 1.35, 0])
        self.at("build sugar")
        self.play(GrowFromCenter(q), run_time=0.7)
        partial = loop_paths().set_opacity(0.45)
        partial[0].pointwise_become_partial(partial[0], 0, 0.62)
        partial[1].pointwise_become_partial(partial[1], 0, 0.58)
        self.at("parts begin working")
        self.play(Create(partial), chl.animate.set_opacity(1), mit.animate.set_opacity(1), run_time=1.8)
        self.at("materials connect")
        self.play(Indicate(VGroup(chl, mit, partial), color=YELLOW, scale_factor=1.02), run_time=1.2)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        world = cell_world(dim=True)
        title = T("Two Jobs in One Green Cell", 50, TEXT, font=TITLE_FONT)
        title.layout_ok = True  # deliberate title overlay on the dim living-cell background
        rule = Line(LEFT*1.4, RIGHT*1.4, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.24)
        backing = SurroundingRectangle(VGroup(title, rule), buff=0.28, corner_radius=0.16,
                                       color=GOLD, stroke_width=2, fill_color=BG, fill_opacity=0.9)
        backing.layout_ok = True
        self.add(world)
        self.play(FadeIn(backing), Write(title), GrowFromCenter(rule), run_time=0.85)
        self.wait(0.55)
        self.play(VGroup(backing, title, rule).animate.scale(0.48).move_to([-4.65, 3.3, 0]), run_time=0.6)
        self.finish()


class S02Photosynthesis(SpokenScene):
    def construct(self):
        cell = cell_shell()
        chl = chloroplast()
        self.add(cell)
        light = path_arrow([-5.9, 2.8, 0], [-4.25, 0.9, 0], YELLOW, 0.15, 8)
        self.play(GrowArrow(light), run_time=0.9)
        self.at("green chloroplast")
        self.play(GrowFromCenter(chl), run_time=1.1)
        label = T("chloroplast", 30, GREEN, weight=BOLD).next_to(chl, DOWN, buff=0.18)
        self.at("takes in light")
        self.play(FadeIn(label), Indicate(light, color=YELLOW), run_time=0.9)
        co2 = material("carbon dioxide", GREY, [-5.05, -1.8, 0])
        water = material("water", BLUE, [-2.55, -2.05, 0])
        self.at("Carbon dioxide and water")
        self.play(FadeOut(label), FadeIn(co2), FadeIn(water), run_time=0.6)
        self.play(co2.animate.move_to(CHL_C + [-0.65, -0.45, 0]),
                  water.animate.move_to(CHL_C + [0.65, 0.45, 0]), run_time=1.2)
        sugar = material("sugar", GREEN, CHL_C + [0.15, 0.15, 0])
        bubbles = oxygen_bubbles(CHL_C + [0.5, 0.05, 0])
        self.at("Sugar, called glucose")
        self.play(ReplacementTransform(VGroup(co2, water), VGroup(sugar, bubbles)), run_time=1.2)
        self.at("oxygen move out")
        self.play(sugar.animate.move_to([-0.75, 1.55, 0]),
                  bubbles.animate.move_to([-0.4, 0.65, 0]), run_time=1.4)
        self.finish()


class S03Respiration(SpokenScene):
    def construct(self):
        world = cell_world()
        sugar = material("sugar", GREEN, [-1.0, 1.55, 0])
        oxy = oxygen_bubbles([-0.75, 0.65, 0])
        self.add(world, sugar, oxy)
        self.play(sugar.animate.move_to([1.15, 1.1, 0]), run_time=1.1)
        label = T("mitochondrion", 30, RED, weight=BOLD).next_to(world.mit, DOWN, buff=0.18)
        self.at("red mitochondrion")
        self.play(FadeIn(label), Indicate(world.mit, color=RED), run_time=0.8)
        self.at("cellular respiration")
        self.play(world.mit.animate.scale(1.06), run_time=0.55, rate_func=there_and_back)
        pieces = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.45, height=0.32,
                                          color=GREEN, fill_color=GREEN, fill_opacity=0.25)
                          for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to([1.4, 0.7, 0])
        self.at("breaks down the sugar")
        self.play(ReplacementTransform(sugar, pieces), run_time=0.8)
        self.play(pieces.animate.move_to(MIT_C + [-0.3, 0.2, 0]).scale(0.65),
                  oxy.animate.move_to(MIT_C + [0.45, 0.2, 0]).scale(0.75), run_time=1.0)
        energy = path_arrow([4.15, 0.55, 0], [5.0, 1.7, 0], YELLOW, 0.1, 7)
        worker = working_cell_icon()
        self.at("usable energy comes out")
        self.play(GrowArrow(energy), FadeIn(worker), run_time=0.9)
        co2 = material("carbon dioxide", GREY, [4.25, -1.35, 0], 24)
        water = material("water", BLUE, [2.2, -1.75, 0], 24)
        self.at("Carbon dioxide and water")
        self.play(FadeOut(label), FadeIn(co2, shift=DOWN*0.25), FadeIn(water, shift=DOWN*0.25), run_time=0.8)
        self.play(co2.animate.shift(LEFT*1.0), water.animate.shift(LEFT*1.0), run_time=1.0)
        self.finish()


class S04ReactantsProducts(SpokenScene):
    def construct(self):
        world = cell_world()
        top, bottom = loop_paths()
        self.add(world)
        incoming = material("sugar + oxygen", GREEN, [-0.9, 1.25, 0], 24)
        rt = chip("reactant", GREY, 24).next_to(incoming, UP, buff=0.1)
        self.play(FadeIn(incoming), run_time=0.5)
        self.at("A reactant")
        self.play(FadeIn(rt), Create(top), run_time=0.7)
        self.play(VGroup(incoming, rt).animate.move_to([1.55, 1.15, 0]), run_time=1.1)
        outgoing = material("carbon dioxide + water", BLUE, [2.0, -1.25, 0], 22)
        pt = chip("product", GREEN, 24).next_to(outgoing, DOWN, buff=0.1)
        self.at("A product")
        self.play(ReplacementTransform(VGroup(incoming, rt), VGroup(outgoing, pt)), Create(bottom), run_time=1.0)
        self.at("product badge move")
        self.play(VGroup(outgoing, pt).animate.move_to([-0.1, -1.45, 0]), run_time=1.2)
        new_rt = chip("reactant", GREY, 24).move_to(pt)
        self.at("becomes a reactant")
        self.play(swap(pt, new_rt), run_time=0.8)
        self.play(VGroup(outgoing, new_rt).animate.move_to([-1.7, -1.15, 0]), run_time=1.0)
        moving = Dot(top.get_start(), radius=0.13, color=GREEN)
        self.at("supply reactants")
        self.add(moving)
        self.play(MoveAlongPath(moving, top), run_time=1.6, rate_func=linear)
        self.finish()


class S05PredictDark(SpokenScene):
    def construct(self):
        world = question_world()
        self.add(world)
        arc = ArcBetweenPoints([-5.25, 2.55, 0], [5.25, 2.55, 0], angle=-PI/2, color=YELLOW, stroke_width=3)
        self.at("sun moves toward the horizon")
        self.play(MoveAlongPath(world[2], arc), run_time=2.2, rate_func=linear)
        dots = VGroup(Dot(world[1][0].get_start(), radius=0.12, color=GREEN),
                      Dot(world[1][1].get_start(), radius=0.12, color=BLUE))
        self.add(dots)
        self.at("still needs usable energy")
        self.play(MoveAlongPath(dots[0], world[1][0]), MoveAlongPath(dots[1], world[1][1]), run_time=1.6)
        q = question_card("Which arrows stop in darkness?", y=-3.15, size=30)
        self.at("Which moving arrows")
        self.play(FadeIn(q), run_time=0.7)
        self.at("every material in mind")
        self.play(Indicate(world[0], color=YELLOW, scale_factor=1.01), run_time=1.2)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which arrows stop in darkness?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 30}

    def backdrop(self):
        return question_world()


class S07DarkReveal(SpokenScene):
    def construct(self):
        world = cell_world(night=True)
        light = path_arrow([-5.9, 2.8, 0], [-4.25, 0.9, 0], YELLOW, 0.15, 8)
        self.add(world, light)
        self.play(FadeOut(light), run_time=0.8)
        self.at("chloroplast stops")
        self.play(world.chl.animate.set_opacity(0.28), run_time=0.8)
        stored = material("stored sugar", GREEN, [0.3, 1.45, 0], 24)
        oxy = oxygen_bubbles([0.2, 0.65, 0])
        self.at("using stored sugar")
        self.play(FadeIn(stored), FadeIn(oxy), run_time=0.6)
        pieces = VGroup(*[Square(0.32, color=GREEN, fill_color=GREEN, fill_opacity=0.25) for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to([1.5, 0.9, 0])
        self.play(ReplacementTransform(stored, pieces), run_time=0.65)
        self.play(pieces.animate.move_to(MIT_C + [-0.3, 0.2, 0]).scale(0.7),
                  oxy.animate.move_to(MIT_C + [0.4, 0.2, 0]).scale(0.75), run_time=1.0)
        energy = path_arrow([4.1, 0.55, 0], [5.35, 1.45, 0], YELLOW, 0.1, 7)
        self.at("releasing usable energy")
        self.play(GrowArrow(energy), run_time=0.8)
        co2 = material("carbon dioxide", GREY, [4.45, -1.3, 0], 22)
        water = material("water", BLUE, [2.4, -1.6, 0], 24)
        self.at("carbon dioxide, and water")
        self.play(FadeIn(co2), FadeIn(water), run_time=0.6)
        self.play(co2.animate.move_to([5.0, -1.6, 0]), water.animate.move_to([5.15, -2.25, 0]), run_time=1.2)
        rule = caption("The plant cell is still respiring.", color=RED)
        self.at("still respiring")
        self.play(FadeIn(rule), run_time=0.7)
        self.finish()


class S08LightReturns(SpokenScene):
    def construct(self):
        world = cell_world(night=True)
        self.add(world)
        s = sun()
        light = path_arrow([-5.9, 2.8, 0], [-4.25, 0.9, 0], YELLOW, 0.15, 8)
        self.play(FadeIn(s), GrowArrow(light), world.cell[0].animate.set_fill(GREEN, 0.08), run_time=1.0)
        self.at("photosynthesis starts")
        self.play(world.chl.animate.set_opacity(1), run_time=0.8)
        paths = loop_paths()
        dots = VGroup(Dot(paths[0].get_start(), radius=0.13, color=GREEN),
                      Dot(paths[1].get_start(), radius=0.13, color=BLUE))
        self.add(paths, dots)
        self.at("Respiration continues")
        self.play(MoveAlongPath(dots[0], paths[0]), MoveAlongPath(dots[1], paths[1]), run_time=1.6, rate_func=linear)
        self.at("same time")
        self.play(world.chl.animate.scale(1.04), world.mit.animate.scale(1.04), run_time=0.55, rate_func=there_and_back)
        clab = T("photosynthesis", 28, GREEN, weight=BOLD).next_to(world.chl, DOWN, buff=0.18)
        mlab = T("respiration", 28, RED, weight=BOLD).next_to(world.mit, DOWN, buff=0.18)
        self.at("does not switch")
        self.play(FadeIn(clab), FadeIn(mlab), run_time=0.8)
        dots.move_to(ORIGIN)
        dots[0].move_to(paths[0].get_start()); dots[1].move_to(paths[1].get_start())
        self.at("while light is available")
        self.play(MoveAlongPath(dots[0], paths[0]), MoveAlongPath(dots[1], paths[1]), run_time=1.7, rate_func=linear)
        add = T("adds oxygen in light", 28, GREEN).move_to([-2.65, 2.35, 0])
        use = T("uses oxygen day and night", 28, RED).move_to([2.8, 2.35, 0])
        self.at("Photosynthesis adds oxygen")
        self.play(FadeOut(clab), FadeOut(mlab), FadeIn(add), run_time=0.7)
        self.at("Respiration uses oxygen")
        self.play(FadeIn(use), run_time=0.7)
        self.play(Indicate(VGroup(add, use), color=YELLOW, scale_factor=1.02), run_time=1.0)
        self.finish()


class S09Matter(SpokenScene):
    def construct(self):
        world = cell_world()
        paths = loop_paths()
        self.add(world, paths)
        co2 = material("carbon dioxide", GREY, paths[1].get_start(), 22)
        bpath1 = paths[1].copy().shift(DOWN * 0.62)
        water = oxygen_bubbles(bpath1.get_start(), 2)
        self.at("material badges")
        self.play(MoveAlongPath(co2, paths[1]), MoveAlongPath(water, bpath1), run_time=1.7, rate_func=linear)
        sugar = material("sugar", GREEN, paths[0].get_start(), 24)
        bpath0 = paths[0].copy().shift(DOWN * 0.62)
        oxy = oxygen_bubbles(bpath0.get_start(), 2)
        self.at("build sugar and oxygen")
        self.play(ReplacementTransform(VGroup(co2, water), VGroup(sugar, oxy)), run_time=0.9)
        self.at("feed respiration")
        self.play(MoveAlongPath(sugar, paths[0]), MoveAlongPath(oxy, bpath0), run_time=1.7, rate_func=linear)
        opening = Line([5.7, -2.7, 0], [6.35, -3.25, 0], color=GREY, stroke_width=5)
        self.at("used again")
        self.play(Create(opening), Indicate(paths, color=GREEN, scale_factor=1.01), run_time=1.0)
        energy = path_arrow([-5.7, 2.65, 0], [5.65, 2.65, 0], YELLOW, 0, 7).set_opacity(0.2)
        self.add(energy)
        self.at("different path")
        self.play(energy.animate.set_opacity(1), run_time=1.1)
        self.finish()


class S10Energy(SpokenScene):
    def construct(self):
        world = cell_world(dim=True)
        matter_paths = loop_paths().set_opacity(0.28)
        self.add(world, matter_paths)
        ribbon1 = path_arrow([-5.8, 2.55, 0], CHL_C + [-0.5, 0.65, 0], YELLOW, -0.1, 10)
        self.play(GrowArrow(ribbon1), run_time=1.0)
        sugar = material("sugar: chemical energy", GREEN, [-0.45, 1.3, 0], 24)
        self.at("Chemical energy travels")
        self.play(TransformFromCopy(ribbon1, sugar), run_time=0.9)
        self.play(sugar.animate.move_to([1.65, 0.9, 0]), run_time=1.1)
        ribbon2 = path_arrow([2.0, 0.8, 0], [5.15, 1.65, 0], YELLOW, 0.15, 9)
        useful = T("usable energy", 28, YELLOW, weight=BOLD).next_to(ribbon2, DOWN, buff=0.15)
        self.at("energy the cell can use")
        self.play(ReplacementTransform(sugar, ribbon2), FadeIn(useful), run_time=1.0)
        heat = VGroup(*[
            Arc(radius=0.34 + i*0.18, start_angle=-PI/3, angle=2*PI/3,
                color=YELLOW, stroke_width=max(2, 6-i)).move_to([5.45+i*0.18, -0.55+i*0.32, 0])
            for i in range(3)
        ])
        self.at("leaves as heat")
        self.play(Create(heat), run_time=1.1)
        loop_label = T("matter loops", 28, GREEN).move_to([-2.9, -2.45, 0])
        flow_label = T("energy flows one way", 28, YELLOW).move_to([2.4, -2.45, 0])
        self.at("matter arrows loop")
        self.play(FadeIn(loop_label), run_time=0.5)
        self.at("energy flows one way")
        self.play(FadeIn(flow_label), Indicate(VGroup(ribbon1, ribbon2), color=YELLOW), run_time=0.9)
        self.finish()


class S11OutsideLeaf(SpokenScene):
    def construct(self):
        cell = cell_world()
        self.add(cell)
        leaf = Ellipse(width=3.2, height=5.4, color=GREEN, stroke_width=7,
                       fill_color=GREEN, fill_opacity=0.2).rotate(-0.35)
        vein = Line([-0.8, -2.15, 0], [0.8, 2.15, 0], color=GREEN, stroke_width=5)
        leaf_g = VGroup(leaf, vein)
        self.play(ReplacementTransform(cell, leaf_g), run_time=1.1)
        bob(leaf_g, amp=0.08, speed=1.2)
        creek = creek_world()
        self.at("pond or creek")
        self.play(ReplacementTransform(leaf_g, creek), run_time=1.2)
        grass = VGroup(*[Line([-5+i*0.25, 0.4, 0], [-5+i*0.25+0.1, 1.15+(i%2)*0.25, 0], color=GREEN, stroke_width=5) for i in range(5)])
        algae = VGroup(*[Circle(radius=0.12, color=GREEN, fill_color=GREEN, fill_opacity=0.25).move_to([-1.5+i*0.3, -0.55+(i%2)*0.2, 0]) for i in range(5)])
        self.at("Photosynthetic organisms")
        self.play(Create(grass), FadeIn(algae), run_time=0.8)
        bubbles = oxygen_bubbles([-1.5, -0.1, 0], 4)
        self.play(bubbles.animate.shift(UP*1.2), run_time=1.1)
        animal = VGroup(Ellipse(width=1.1, height=0.55, color=RED, fill_color=RED, fill_opacity=0.18),
                        Triangle(color=RED, fill_color=RED, fill_opacity=0.18).scale(0.28).rotate(-PI/2).shift(LEFT*0.65)).move_to([2.0, -0.75, 0])
        fungus = VGroup(Arc(radius=0.42, start_angle=0, angle=PI, color=RED, stroke_width=5),
                        Line([0,0,0],[0,-0.5,0],color=RED,stroke_width=5)).move_to([4.5, 0.15, 0])
        microbes = VGroup(*[Dot([3.5+i*0.35, -1.8+(i%2)*0.25, 0], radius=0.11, color=RED) for i in range(4)])
        self.at("Plants, animals, fungi")
        self.play(FadeIn(animal), FadeIn(fungus), FadeIn(microbes), run_time=0.9)
        use_arrows = VGroup(*[Arrow(b.get_center(), target, buff=0.08, color=RED, stroke_width=4, tip_length=0.15)
                              for b, target in zip(bubbles[:3], [animal.get_center(), fungus.get_center(), microbes.get_center()])])
        self.at("use oxygen through respiration")
        self.play(Create(use_arrows), run_time=1.0)
        day = sun([-4.8, 2.55, 0], 0.8)
        night = T("night", 30, BLUE, weight=BOLD).move_to([4.8, 2.55, 0])
        bar = Arrow([-4.0, 2.55, 0], [3.9, 2.55, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        self.at("continues in darkness")
        self.play(FadeIn(day), GrowArrow(bar), FadeIn(night), Indicate(use_arrows, color=RED), run_time=1.2)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        creek = creek_world()
        self.add(creek)
        sun_obj = sun([-4.8, 2.55, 0], 0.75)
        day_bar = Line([-4.0, 2.55, 0], [0, 2.55, 0], color=YELLOW, stroke_width=12)
        night_bar = Line([0, 2.55, 0], [4.7, 2.55, 0], color=BLUE, stroke_width=12)
        self.play(FadeIn(sun_obj), Create(day_bar), Create(night_bar), run_time=0.8)
        add = Arrow([-4.4, 0.7, 0], [-0.3, 0.7, 0], color=GREEN, stroke_width=10, tip_length=0.28)
        add_lab = T("oxygen added in light", 30, GREEN).next_to(add, UP, buff=0.2)
        self.at("oxygen can be added")
        self.play(GrowArrow(add), FadeIn(add_lab), run_time=0.8)
        use = Arrow([-4.4, -1.2, 0], [4.4, -1.2, 0], color=RED, stroke_width=10, tip_length=0.28)
        use_lab = T("respiration uses oxygen day and night", 30, RED).next_to(use, DOWN, buff=0.2)
        self.at("day and night")
        self.play(GrowArrow(use), FadeIn(use_lab), run_time=1.0)
        line = T("Photosynthesis adds oxygen in light; respiration uses oxygen day and night.", 34, TEXT, font=TITLE_FONT)
        fit(line, max_w=12.0)
        self.at("Carry that pattern")
        self.play(FadeOut(VGroup(creek, sun_obj, day_bar, night_bar, add, add_lab, use, use_lab)),
                  FadeIn(line), run_time=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Photosynthesis adds oxygen in light; respiration uses oxygen day and night."
