"""Growing One Cell into a Colony.

Glass and outlines are grey, culture fluid teal, neurons blue, melanocytes dark
purple, undifferentiated crest cells gold, and transformed cells orange.
Green marks persistence or support, red marks loss or a blocked result.
"""
import numpy as np
from bp_parts import *
from bp_style import EndCard

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
INK = "#30263F"
FLUID = "#254753"
GLASS = "#7597A9"
LEFT_DISH = (-2.85, -0.12)
CENTER_DISH = (0, -0.28)
RIGHT_EMBRYO = (3.55, -0.15)
QUESTION = "Would it make both in the embryo?"
QUESTION_CARD = {"y": 3.02, "size": 36}
MIX = "npnnppn"
CROWD = [
    (-1.22, 1.15), (-0.4, 1.83), (0.85, 1.55), (1.59, 0.65),
    (-1.9, 0.15), (-0.83, 0.64), (0.45, 0.38), (1.8, -0.54),
    (-1.4, -0.9), (-0.4, -0.65), (0.85, -0.76), (-0.68, -1.76),
    (0.7, -1.71),
]
ROSETTE = [(0, 0), (0.69, 0.05), (0.38, 0.62), (-0.36, 0.62),
           (-0.7, -0.05), (-0.36, -0.65), (0.37, -0.63),
           (1.17, 0.55), (-1.2, 0.45), (0.09, -1.18),
           (-0.02, 1.19), (1.24, -0.42), (-1.23, -0.44)]


def p(x, y):
    return np.array([x, y, 0.0])


def at_offset(center, x=0, y=0):
    return p(*center) + p(x, y)


def label(text, x=3.75, y=1.9, color=TEXT, size=33, width=5.0):
    return fit_text(text, max_w=width, size=size, min_size=28,
                    color=color, weight=SEMIBOLD).move_to(p(x, y))


def path(points, color, width=3, fill=None):
    shape = VMobject()
    shape.set_points_smoothly([p(*xy) for xy in points])
    shape.set_stroke(color, width)
    if fill:
        shape.set_fill(fill, opacity=1)
    return shape


def vessel_outline(radius, color, width, fill, profile=None):
    """Match points by angle so the dish keeps its outline as it tilts."""
    angles = np.linspace(0, TAU, 128, endpoint=False)
    rays = np.column_stack((np.cos(angles), np.sin(angles)))
    if profile is None:
        outline = rays * radius
    else:
        starts = np.array(profile)
        edges = np.roll(starts, -1, axis=0) - starts
        # Distance along each ray to the edge of the convex side profile.
        normal = np.column_stack((edges[:, 1], -edges[:, 0]))
        numerator = (starts * normal).sum(axis=1)
        denominator = rays @ normal.T
        distance = np.divide(numerator, denominator, out=np.full_like(denominator, np.inf),
                             where=denominator > 1e-8)
        outline = rays * distance.min(axis=1, keepdims=True)
    return Polygon(*(p(x, y) for x, y in outline), stroke_color=color,
                   stroke_width=width, fill_color=fill, fill_opacity=1)


def petri(center=LEFT_DISH, side=False, tint=FLUID):
    """The same culture vessel viewed from above or in cross-section."""
    if side:
        shell = [(2.68, 2.42), (-2.68, 2.42), (-2.51, -1.79), (-2.37, -2.18),
                 (-2.08, -2.46), (-1.65, -2.55), (0, -2.65), (1.65, -2.55),
                 (2.08, -2.46), (2.37, -2.18), (2.51, -1.79)]
        well = [(2.38, 2.1), (-2.38, 2.1), (-2.21, -1.75), (-2, -2.03),
                (-1.42, -2.17), (0, -2.27), (1.42, -2.17), (2, -2.03),
                (2.21, -1.75)]
        rim = Line(p(2.68, 2.42), p(-2.68, 2.42), color="#ACD0DD", stroke_width=3)
        floor = path([(-2.1, -2.05), (0, -2.28), (2.1, -2.05)], GLASS, 2.6)
    else:
        shell = well = None
        rim = Arc(radius=2.69, start_angle=0.65, angle=1.84,
                  color="#ACD0DD", stroke_width=3)
        floor = Arc(radius=2.61, start_angle=3.33, angle=2.5,
                    color="#547E8E", stroke_width=2.6)
    base = vessel_outline(2.72, GLASS, 4, "#1D3342", shell)
    inner = vessel_outline(2.51, "#517786", 2.4, tint, well)
    return VGroup(base, inner, rim, floor).shift(p(*center))


def dish_light(dish, base=FLUID, highlight="#3C6170"):
    """Slow reflected light on the dish floor during live microscopy views."""
    fluid = dish[1]
    clock = ValueTracker(0)
    low, high = ManimColor(base), ManimColor(highlight)
    def reflect(surface, dt):
        clock.increment_value(dt)
        amount = 0.5 - 0.5 * np.cos(1.53 * clock.get_value())
        surface.set_fill(interpolate_color(low, high, amount))

    fluid.add_updater(reflect)
    return fluid


def stop_dish_light(fluid, tint=FLUID):
    fluid.clear_updaters()
    fluid.set_fill(tint)


def cell(kind="c", here=ORIGIN, scale=1):
    """Cell silhouettes and nuclei distinguish types without molecular imagery."""
    colors = {"c": GOLD, "n": BLUE, "b": BLUE, "p": PURPLE, "f": GREY,
              "o": ORANGE, "g": GREEN, "s": TEAL, "d": RED}
    color = colors[kind]
    fill = INK if kind == "p" else color
    if kind in "nb":
        arms = VGroup(
            path([(-0.03, 0.09), (-0.18, 0.25), (-0.34, 0.31)], color, 3.1),
            path([(-0.18, 0.25), (-0.22, 0.40)], color, 2.3),
            path([(0.03, 0.08), (0.18, 0.24), (0.33, 0.24)], color, 3.2),
            path([(0.01, -0.03), (0.12, -0.27), (0.34, -0.37)], color, 3.2),
            path([(0.14, -0.27), (0.15, -0.43)], color, 2.2),
        )
        if kind == "b":
            arms.rotate(0.95).stretch(1.2, 0)
        body = Ellipse(width=0.34, height=0.28, stroke_color=color, stroke_width=2,
                       fill_color=fill, fill_opacity=0.85)
    elif kind in "fs":
        boundary = ([(-0.57, -0.10), (-0.19, 0.13), (0.16, 0.10),
                     (0.57, 0.14), (0.24, -0.08), (-0.13, -0.13), (-0.57, -0.10)]
                    if kind == "f" else
                    [(0, 0.53), (0.13, 0.15), (0.48, 0.22), (0.21, -0.06),
                     (0.33, -0.44), (0, -0.24), (-0.34, -0.43), (-0.22, -0.05),
                     (-0.46, 0.22), (-0.11, 0.14), (0, 0.53)])
        body = Polygon(*[p(*pt) for pt in boundary], color=color, stroke_width=2.4,
                       fill_color=fill, fill_opacity=0.62)
        arms = VGroup()
    else:
        body = Ellipse(width=0.5, height=0.43, color=color, stroke_width=2.4,
                       fill_color=fill, fill_opacity=0.78)
        arms = VGroup()
    nucleus = Ellipse(width=0.14, height=0.115, stroke_width=0,
                      fill_color=PURPLE if kind == "p" else BG, fill_opacity=0.74)
    membrane = VGroup(arms, body, nucleus).scale(scale, about_point=ORIGIN)
    return membrane.shift(here)


def cells(kinds, locations, center=LEFT_DISH, scale=1):
    return VGroup(*(cell(kind, at_offset(center, *xy), scale) for kind, xy in zip(kinds, locations)))


def crowded(center=LEFT_DISH):
    return cells("npnppnnpnpnpp", CROWD, center, 1.15)


def cluster(kinds, here, spread=1, scale=1):
    return cells(kinds, [(x * spread, y * spread) for x, y in ROSETTE], here[:2], scale)


def halo(here, radius=0.46, color=YELLOW):
    return Circle(radius=radius, color=color, stroke_width=3).move_to(here)


def drift(group, amp=0.13, speed=1.45):
    for index, individual in enumerate(group):
        bob(individual, amp=amp, speed=speed + 0.13 * (index % 3), seed=index)
    return group


def settle(group):
    for individual in group:
        individual.clear_updaters()
    return group


def dish_side(gel=False):
    return petri(side=True, tint="#2E596B" if gel else "#213A45")


def gel_surface():
    return path([(-2.34, 1.75), (-1.2, 1.69), (-0.15, 1.77), (1.15, 1.70),
                 (2.34, 1.75)], BLUE, 1.9).shift(p(*LEFT_DISH))


def prediction():
    return petri(CENTER_DISH), cluster(MIX, p(*CENTER_DISH), 1.64, 1.34)


def embryo(center=RIGHT_EMBRYO):
    rim = path([(-0.16, 2.62), (1.05, 2.32), (1.49, 1.4), (1.06, 0.29),
                (0.05, -0.52), (-0.24, -1.36), (0.44, -1.73), (1.05, -1.38),
                (0.95, -2.07), (0.19, -2.51), (-0.79, -2.26), (-1.37, -1.53),
                (-1.34, -0.46), (-1.85, 0.45), (-1.81, 1.6), (-1.23, 2.35),
                (-0.16, 2.62)], GLASS, 4, "#273646")
    fold = path([(-0.62, 1.79), (0.24, 1.69), (0.65, 1.06), (0.28, 0.27),
                 (-0.54, -0.38), (-0.78, -1.08), (-0.48, -1.77)], "#536C83", 2.5)
    return VGroup(rim, fold).shift(p(*center))


def drop(here, color, size=1):
    return path([(0, 0.46), (0.23, 0.04), (0.22, -0.23), (0, -0.35),
                 (-0.22, -0.23), (-0.23, 0.04), (0, 0.46)], color, 2.4, color
                ).scale(size, about_point=ORIGIN).shift(here)


def branch(a, b, color=GLASS):
    return Line(a, b, buff=0.32, color=color, stroke_width=2.7)


def growth(existing, target, seconds):
    """Copy a visible parent into each new daughter position."""
    settle(existing)
    parents = list(existing)
    animations = []
    for index, daughter in enumerate(target):
        if index < len(parents):
            animations.append(Transform(parents[index], daughter, run_time=seconds))
        else:
            source = min(parents, key=lambda item: np.linalg.norm(item.get_center() - daughter.get_center()))
            animations.append(TransformFromCopy(source, daughter, run_time=seconds))
    return animations, VGroup(*parents, *target[len(parents):])


def grow(scene, existing, target, seconds):
    animations, colony = growth(existing, target, seconds)
    scene.play(*animations)
    return colony


class S01Hook(SpokenScene):
    def construct(self):
        dish, population = petri(), crowded()
        self.add(dish, drift(population, 0.16))
        self.at("can one cell")
        focus = halo(population[5].get_center(), 0.55)
        self.play(Create(focus), run_time=0.8)
        pulse(focus, base=3.5, amp=1.2)
        question = question_card("One ancestor?", y=1.25, size=39).move_to(p(3.6, 1.6))
        self.play(FadeIn(question), run_time=0.55)
        self.at("crowded dish")
        self.play(focus.animate.set_stroke(opacity=0.45), run_time=0.6)
        self.at("neurons and pigment")
        samples = VGroup(cell("n", p(2.4, 0.22), 1.35), cell("p", p(4.8, 0.22), 1.35))
        self.play(FadeIn(samples, shift=UP * 0.18), run_time=0.7)
        self.at("you cannot tell")
        self.play(FadeOut(question), FadeOut(samples), run_time=0.45)
        self.at("one ancestor made both")
        a, b, c = p(2.1, 1.45), p(4.9, 1.98), p(4.9, 0.92)
        first = VGroup(cell("c", a, 1.1), branch(a, b), branch(a, c),
                       cell("n", b, 1.2), cell("p", c, 1.2))
        self.play(FadeIn(first, shift=RIGHT * 0.25), run_time=0.95)
        self.at("separate specialists")
        a, b, c, d = p(2.1, -0.65), p(2.1, -1.8), p(4.9, -0.65), p(4.9, -1.8)
        second = VGroup(cell("n", a, 1.08), cell("p", b, 1.08),
                        branch(a, c), branch(b, d), cell("n", c, 1.2), cell("p", d, 1.2))
        self.play(FadeIn(second, shift=RIGHT * 0.25), run_time=0.92)
        self.finish()


class S02Title(TitleCard):
    TITLE = "Growing One Cell into a Colony"
    LESSON = "Clonal and colony assays"

    def construct(self):
        center = (0, -0.95)
        dish = petri(center).scale(0.78, about_point=p(*center)).fade(0.63)
        glow = pulse(halo(p(*center), 0.68 * 0.78), base=3.2, amp=1.5, speed=2.8)
        founder = cell("c", p(*center), 1.5 * 0.78)
        title = T(self.TITLE.replace(" into", "\ninto"), 55, font=TITLE_FONT,
                  line_spacing=0.82).move_to(p(0, 2.3))
        lesson = T(self.LESSON, 29, color=GOLD).move_to(p(0, -3.43))
        self.add(dish, glow, founder)
        self.play(FadeIn(title), FadeIn(lesson), run_time=0.35)
        self.wait(1.65)


class S03Isolate(SpokenScene):
    def construct(self):
        dish, population = petri(), crowded()
        sites = [(-0.45, 0.15), (1.56, 1.15), (-1.68, -1.24)]
        sparse = cells("ccc", sites, scale=1.22)
        self.add(dish, population)
        dish_light(dish)
        self.at("plate cells sparsely")
        self.play(ReplacementTransform(population, sparse), run_time=1.48)
        founder = sparse[0]
        focus = pulse(halo(founder.get_center(), 0.48), base=3.5, amp=0.8)
        single = label("Single cell", y=0.9, color=GOLD)
        self.play(Create(focus), FadeIn(single), run_time=0.5)
        self.at("over days")
        day = ValueTracker(0)
        days = counter("Day {:.0f}", day, p(3.75, -0.3), size=31, color=TEXT)
        schematic = label("Schematic", y=-0.98, color=GREY, size=28)
        self.play(FadeOut(focus), FadeIn(days), FadeIn(schematic), run_time=0.55)
        self.at("divides into a clone")
        center = at_offset(LEFT_DISH, *sites[0])
        self.add(day)
        self.play(day.animate.set_value(1), run_time=0.6)
        clone = grow(self, VGroup(founder), cluster("cc", center, 0.9, 1.18), 0.75)
        name = label("Clone", y=0.9, color=GOLD)
        self.play(swap(single, name, 0.55), day.animate.set_value(2), run_time=0.6)
        clone = grow(self, clone, cluster("cccc", center, 0.93, 1.15), 0.92)
        self.play(day.animate.set_value(3), run_time=0.52)
        self.at("one division proves little")
        clone = grow(self, clone, cluster("ccccccc", center, 0.91, 1.12), 1.4)
        self.at("short lived progenitors")
        progenitor = sparse[1]
        group = grow(self, VGroup(progenitor),
                     cells("cc", [(1.3, 1.45), (1.79, 0.96)], scale=1.02), 1.05)
        brief = label("Short-lived progenitor", y=0.9, color=GREY)
        self.play(swap(name, brief), FadeOut(days), FadeOut(schematic), run_time=0.64)
        self.at("before differentiating")
        different = cells("ff", [(1.34, 1.41), (1.81, 0.85)], scale=0.68)
        self.play(*(Transform(a, b) for a, b in zip(group, different)), run_time=0.95)
        self.at("repeated growth and replating")
        fresh = petri((3.55, -0.28)).scale(0.79)
        test = label("Self-renewal test", y=2.65, color=GREEN)
        self.play(FadeOut(brief), run_time=0.35)
        self.play(FadeIn(fresh), run_time=0.52)
        moved = cell("c", p(3.55, -0.28), 1.17)
        self.play(TransformFromCopy(founder, moved, path_arc=-0.36), run_time=1.15)
        renewed = grow(self, VGroup(moved), cluster("cccc", p(3.55, -0.28), 1.02, 1.1), 1.15)
        self.play(FadeIn(test), run_time=0.45)
        drift(renewed, 0.09)
        self.finish()


class S04Agar(SpokenScene):
    def construct(self):
        dish = petri()
        center = at_offset(LEFT_DISH, -0.9, -2.14)
        fibro = cell("f", at_offset(LEFT_DISH, -0.9, -0.1), 1.4)
        self.add(dish)
        self.at("changing the dish")
        self.play(Transform(dish, dish_side()), run_time=1.75)
        fluid = dish_light(dish, "#213A45", "#365763")
        self.at("normal fibroblast")
        self.play(FadeIn(fibro, shift=DOWN * 0.2), run_time=0.5)
        self.play(fibro.animate.move_to(center), run_time=1.2)
        self.at("divides only when anchored")
        anchored = label("Anchored", color=GREY, y=0.9)
        pair = grow(self, VGroup(fibro), cells("ff", [(-1.48, -2.08), (-0.27, -2.14)],
                                               scale=1.05), 1.1)
        self.play(FadeIn(anchored), run_time=0.55)
        self.at("in soft agar")
        stop_dish_light(fluid, "#213A45")
        surface = gel_surface()
        normal = cell("f", at_offset(LEFT_DISH, -1.2, -0.05), 1.4)
        self.play(FadeOut(pair), FadeOut(anchored), Transform(dish, dish_side(True)),
                  Create(surface), run_time=1.22)
        self.play(FadeIn(normal, shift=UP * 0.44), run_time=0.75)
        bob(normal, amp=0.23, speed=1.55)
        dish_light(dish, "#2E596B", "#447282")
        agar = label("Soft agar, schematic", y=0.9, color=BLUE)
        self.play(FadeIn(agar), run_time=0.48)
        self.at("normal fibroblasts stop")
        stop = label("Fibroblast stays single", y=-0.06, color=GREY)
        self.play(FadeIn(stop), run_time=0.6)
        self.at("a transformed cell")
        t_center = at_offset(LEFT_DISH, 0.86, -0.57)
        transformed = cell("o", t_center, 1.35)
        self.play(FadeIn(transformed, shift=DOWN * 0.25), run_time=0.7)
        self.at("needs no anchor")
        colony = grow(self, VGroup(transformed), cluster("ooo", t_center, 0.8, 1.13), 0.93)
        self.at("forms a colony")
        division, colony = growth(colony, cluster("ooooooo", t_center, 0.89, 1.12), 0.85)
        name = label("Transformed colony", y=-1.07, color=ORANGE)
        self.play(*division, FadeIn(name, run_time=0.4))
        drift(colony, 0.09)
        self.finish()


class S05PredictQ(SpokenScene):
    def construct(self):
        dish, surface = dish_side(True), gel_surface()
        previous = VGroup(cell("f", at_offset(LEFT_DISH, -1.2, -0.05), 1.4),
                          cluster("ooooooo", at_offset(LEFT_DISH, 0.86, -0.57), 0.89, 1.12))
        plate, mixed = prediction()
        founder = cell("c", p(*CENTER_DISH), 1.45)
        self.add(dish, surface, previous)
        self.at("now take one neural crest")
        self.play(Transform(dish, plate), FadeOut(surface), FadeOut(previous), run_time=1.15)
        fluid = dish_light(dish)
        self.play(FadeIn(founder, shift=RIGHT * 0.42), run_time=0.6)
        ring = pulse(halo(p(*CENTER_DISH), 0.54), base=3.3, amp=1.3)
        self.play(Create(ring), run_time=0.68)
        self.at("alone in a dish")
        self.play(FadeOut(ring), founder.animate.scale(1.12), run_time=1.1)
        self.at("it grows a colony")
        colony = grow(self, VGroup(founder), cluster("cc", p(*CENTER_DISH), 1.02, 1.29), 0.65)
        colony = grow(self, colony, cluster("cccc", p(*CENTER_DISH), 1.02, 1.29), 0.58)
        self.at("neurons and pigment cells")
        colony = grow(self, colony, mixed, 1.48)
        self.at("does that show")
        fluid.clear_updaters()
        self.play(FadeIn(question_card(QUESTION, **QUESTION_CARD)),
                  fluid.animate.set_fill(FLUID), run_time=0.65)
        pivot = p(*CENTER_DISH)
        self.play(colony.animate.scale(1.24, about_point=pivot), run_time=1.5)
        remaining = max(0.5, self.narration_s + 0.4 - self.elapsed() - 0.04)
        self.play(colony.animate.scale(1 / 1.24, about_point=pivot),
                  run_time=remaining, rate_func=linear)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = QUESTION_CARD
    SECONDS = 4.5
    RING_AT = (5.85, -2.83, 0)

    def backdrop(self):
        return VGroup(*prediction())

    def construct(self):
        self.add(self.backdrop(), question_card(self.QUESTION, **self.CARD))
        center = np.array(self.RING_AT)
        guide = Circle(radius=0.56, color=GLASS, stroke_width=3.5).move_to(center)
        arc = Arc(radius=0.56, start_angle=PI / 2, angle=-TAU, arc_center=center,
                  color=GOLD, stroke_width=6.5)
        self.add(guide)
        self.play(Create(arc, rate_func=linear), run_time=self.SECONDS)


class S07PredictAnswer(SpokenScene):
    def construct(self):
        dish, colony = prediction()
        question = question_card(QUESTION, **QUESTION_CARD)
        body = embryo()
        self.add(dish, colony, question)
        self.at("not necessarily")
        shift = p(*LEFT_DISH) - p(*CENTER_DISH)
        self.play(FadeOut(question), dish.animate.shift(shift), colony.animate.shift(shift),
                  run_time=1.32)
        drift(colony, 0.12)
        self.at("growing one cell")
        self.play(FadeIn(body, shift=LEFT * 0.2), run_time=1.1)
        self.at("tests potential")
        potential = label("Potential: dish", -2.85, 3.03, GOLD)
        fate = label("Fate: embryo", 3.55, 3.03, GREY)
        self.play(FadeIn(potential), FadeIn(fate), run_time=0.62)
        self.at("culture shows what")
        halos = VGroup(halo(colony[0].get_center(), 0.53, BLUE),
                       halo(colony[1].get_center(), 0.48, PURPLE))
        self.play(LaggedStart(*[Create(h) for h in halos], lag_ratio=0.42), run_time=1.1)
        self.play(FadeOut(halos), run_time=0.95)
        self.at("in the embryo")
        route = path([(-0.58, 1.43), (0.11, 1.14), (0.31, 0.56), (-0.09, 0.04),
                      (-0.66, -0.55), (-0.82, -0.95)], GOLD, 3).shift(p(*RIGHT_EMBRYO))
        migrant = cell("c", route.get_start(), 1.14)
        self.play(FadeIn(migrant), run_time=0.4)
        self.play(Create(route), MoveAlongPath(migrant, route), run_time=2.16)
        self.at("only one type")
        descendant = cell("n", route.get_end(), 1.22)
        self.play(Transform(migrant, descendant), FadeOut(route), run_time=0.94)
        self.at("label it in place")
        mark = Dot(migrant.get_center() + UP * 0.43, radius=0.091, color=YELLOW)
        self.play(GrowFromCenter(mark), run_time=0.5)
        self.at("find its descendants")
        product = VGroup(migrant.copy(), mark.copy()).shift(RIGHT * 0.17 + UP * 0.78)
        self.play(TransformFromCopy(VGroup(migrant, mark), product), run_time=1.15)
        self.finish()


class S08Controls(SpokenScene):
    def construct(self):
        dish, mixed = petri(), crowded()
        self.add(dish, drift(mixed, 0.21))
        fluid = dish_light(dish)
        self.at("two traps can mislead")
        proportions = label("Mixed proportions", y=1.6)
        self.play(FadeIn(proportions), run_time=0.58)
        self.at("can shift through faster")
        settle(mixed)
        daughters = cells("nnn", [(-0.37, 1.19), (0.55, 0.96), (-0.19, -1.26)], scale=1.02)
        self.play(*(TransformFromCopy(a, b) for a, b in zip((mixed[0], mixed[2], mixed[5]), daughters)),
                  run_time=0.94)
        self.at("or death")
        dying = VGroup(mixed[3], mixed[9], mixed[12])
        self.play(dying.animate.set_color(RED), run_time=0.45)
        self.play(FadeOut(dying, scale=0.72), run_time=0.48)
        self.at("without any fate change")
        conclusion = label("Same cell types", y=0.52, color=GREY)
        self.play(FadeIn(conclusion), run_time=0.55)
        self.at("follow clones instead")
        sparse = cells("cn", [(-1.05, 0.35), (1.03, -0.65)], scale=1.2)
        old = VGroup(*(m for m in mixed if m not in dying), daughters)
        count_label = label("Count every cell", y=1.6, color=GOLD)
        self.play(FadeOut(old), FadeOut(conclusion),
                  swap(proportions, count_label),
                  FadeIn(sparse), run_time=0.75)
        tallies = Ledger([("Start", "1 + 1", GREY), ("End", "4 + 2", GREEN)],
                         top_left=(1.55, 0.35), row_h=0.74, key_w=1.65, width=4.4, size=30)
        self.at("counting every cell")
        self.play(tallies.reveal(0), run_time=0.43)
        self.at("start and end")
        ga = cluster("cccc", at_offset(LEFT_DISH, -1.33, 0.35), 0.78, 0.9)
        gb = cluster("nn", at_offset(LEFT_DISH, 0.65, -0.66), 0.95, 0.99)
        grow_a, a = growth(VGroup(sparse[0]), ga, 0.65)
        grow_b, b = growth(VGroup(sparse[1]), gb, 0.65)
        self.play(*grow_a, *grow_b)
        self.play(tallies.reveal(1), run_time=0.5)
        self.at("dish conditions")
        fluid.clear_updaters()
        self.play(FadeOut(VGroup(a, b, tallies.everything())),
                  FadeOut(count_label),
                  Transform(dish, petri(tint="#2E5268")), run_time=0.68)
        unusual = cell("c", p(*LEFT_DISH), 2.5)
        self.play(FadeIn(unusual), run_time=0.48)
        self.at("trigger fates")
        self.play(Transform(unusual, cell("s", p(*LEFT_DISH), 2.5)), run_time=1.02)
        self.at("in living animals")
        body = embryo()
        only = label("Unusual dish fate", -2.85, 3.02, TEAL)
        self.play(FadeIn(body), FadeIn(only), run_time=0.65)
        self.at("helper cells boosting")
        helper = cells("fff", [(-1.49, -0.12), (-0.89, -1.19), (0.52, -1.55)], scale=1.1)
        seed = cell("c", at_offset(LEFT_DISH, 0.18, 0.32), 1.16)
        self.play(FadeOut(body), FadeOut(only), FadeOut(unusual, scale=0.72),
                  FadeIn(helper), FadeIn(seed), run_time=0.8)
        kit = grow(self, VGroup(seed), cluster("ccccccc", at_offset(LEFT_DISH, 0.18, 0.32),
                                              1.05, 1.12), 1.3)
        drift(kit, 0.12)
        self.at("they can help")
        self.play(FadeIn(label("Sufficiency,\nnot requirement", y=0.5, color=GREEN)), run_time=0.68)
        self.finish()


def feeder_layer():
    sites = [(x + (0.25 if row % 2 else 0), y)
             for row, y in enumerate((-1.62, -0.82, 0, 0.82, 1.62))
             for x in (-1.75, -0.84, 0.08, 1.0, 1.74)
             if (x + (0.25 if row % 2 else 0)) ** 2 + y ** 2 < 4.75]
    return cells("f" * len(sites), sites, scale=0.64).set_opacity(0.27)


def day_bar(progress):
    center = p(3.72, 0.23)
    track = RoundedRectangle(width=3.94, height=0.25, corner_radius=0.11,
                             stroke_color=GLASS, stroke_width=2)
    track.move_to(center)
    start = center + LEFT * 1.88
    fill = always_redraw(lambda: RoundedRectangle(
        width=max(0.04, 3.76 * progress.get_value()), height=0.11, corner_radius=0.02,
        stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to(start, aligned_edge=LEFT))
    legend = label("7–10 days", y=0.68, color=TEXT, size=30)
    scope = label("Schematic", y=-0.25, color=GREY, size=28)
    return VGroup(track, fill, legend, scope)


class S09UnlockedCrest(SpokenScene):
    def construct(self):
        dish = petri(tint="#2E5268")
        helpers = cells("fff", [(-1.49, -0.12), (-0.89, -1.19), (0.52, -1.55)], scale=1.1)
        seed = cluster("ccccccc", at_offset(LEFT_DISH, 0.18, 0.32), 1.05, 1.12)
        self.add(dish, helpers, seed)
        self.at("colony assays unlocked findings")
        layer = feeder_layer()
        self.play(FadeOut(seed), Transform(dish, petri()), ReplacementTransform(helpers, layer),
                  run_time=1.22)
        self.at("1988")
        source = label("Baroffio, Dupin &\nLe Douarin, 1988", y=1.85, color=GOLD, size=30)
        self.play(FadeIn(source), run_time=0.62)
        self.play(LaggedStart(*[Indicate(f, color=GREY, scale_factor=1.15) for f in layer[::4]],
                              lag_ratio=0.27), run_time=2.4)
        self.at("plated single")
        sites = [(-0.95, 0.87), (0.86, -0.86), (1.27, 0.93), (-1.2, -0.97)]
        singles = cells("cccc", sites, scale=1.14)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.32) for c in singles], lag_ratio=0.31),
                  run_time=1.36)
        self.at("they analyzed", lead=0.35)
        progress = ValueTracker(0)
        number = counter("{:.0f} clones", progress, p(3.72, -1.26), size=36, color=GOLD)
        # One progress fraction drives both the elapsed growth window and the clone total.
        bar_fraction = ValueTracker(0)
        bar_fraction.add_updater(lambda m: m.set_value(progress.get_value() / 243))
        bar = day_bar(bar_fraction)
        self.add(progress, bar_fraction)
        self.play(FadeIn(bar), FadeIn(number), run_time=0.25)
        early = [cluster("ccc", at_offset(LEFT_DISH, *xy), 0.58, 0.67) for xy in sites]
        self.play(*(Transform(a, group[0], run_time=1.83) for a, group in zip(singles, early)),
                  *(TransformFromCopy(a, b, run_time=1.83)
                    for a, group in zip(singles, early) for b in group[1:]),
                  progress.animate(run_time=0.65).set_value(243))
        self.at("some made one neuron type")
        original = VGroup(singles[0], *early[0][1:])
        one = cells("nnn", [(-1.5, 0.83), (-0.85, 1.19), (-0.9, 0.54)], scale=0.86)
        self.play(*(Transform(a, b) for a, b in zip(original, one)),
                  FadeOut(bar), run_time=0.86)
        single_type = label("One neuron type", y=0.33, color=BLUE, size=30)
        self.play(FadeIn(single_type), run_time=0.5)
        self.at("others made several")
        mixed = VGroup(singles[1], *early[1][1:])
        final_sites = [(0.35, -0.63), (1.42, -0.6), (1.0, -1.44), (0.4, -1.45), (1.15, 0.08)]
        types = cells("nbc", final_sites, scale=0.88)
        self.play(*(Transform(a, b) for a, b in zip(mixed, types)),
                  FadeOut(VGroup(singles[3], *early[3][1:])), run_time=0.9)
        middle = VGroup(singles[2], *early[2][1:])
        intermediate = cells("nnp", [(0.88, 1.05), (1.48, 1.14), (1.58, 0.62)], scale=0.74)
        self.play(*(Transform(a, b) for a, b in zip(middle, intermediate)),
                  swap(single_type, label("Several cell types", y=0.33, color=BLUE), 0.66),
                  run_time=0.72)
        self.at("neuronal cells")
        gray = cell("f", at_offset(LEFT_DISH, *final_sites[2]), 0.69)
        self.play(Transform(mixed[2], gray), run_time=0.72)
        self.at("making melanocytes")
        self.play(TransformFromCopy(mixed[0], cell("p", at_offset(LEFT_DISH, *final_sites[3]), 0.95)),
                  TransformFromCopy(mixed[1], cell("p", at_offset(LEFT_DISH, *final_sites[4]), 0.92)),
                  run_time=0.95)
        self.finish()


TGF_CENTER = at_offset(LEFT_DISH, 0, -0.77)
TGF_SOURCE = "Roberts & Sporn\n1981 & 1983"


def mouse_organ():
    tissue = path([(-1.06, -0.31), (-1.02, 0.33), (-0.58, 0.69), (0.15, 0.74),
                   (0.98, 0.44), (0.82, 0.02), (0.38, -0.09), (0.16, -0.49),
                   (-0.47, -0.62), (-1.06, -0.31)], GREY, 3, "#596275")
    fold = path([(-0.76, -0.26), (-0.3, 0.03), (0.21, 0.21), (0.58, 0.25)], "#9DA6B3", 2.6)
    return VGroup(tissue, fold).move_to(p(3.75, -0.27))


class S10UnlockedTgfb(SpokenScene):
    def construct(self):
        dish = petri()
        self.add(dish)
        self.at("soft agar")
        surface = gel_surface()
        self.play(Transform(dish, dish_side(True)), Create(surface), run_time=1.5)
        fibro = cell("f", TGF_CENTER, 1.28)
        self.play(FadeIn(fibro, shift=DOWN * 0.33), run_time=0.64)
        bob(fibro, amp=0.18, speed=1.45)
        self.at("transforming growth factor")
        source = label(TGF_SOURCE, y=1.89, color=GOLD, size=30)
        reagent = drop(at_offset(LEFT_DISH, -0.8, 1.1), ORANGE, 0.85)
        self.play(FadeIn(source), FadeIn(reagent, shift=DOWN * 0.35), run_time=0.77)
        self.at("was thought to come")
        thought = label("Thought: cancer-cell\nproduct", y=0.1, color=GREY, size=30)
        self.play(FadeIn(thought), reagent.animate.shift(DOWN * 0.62), run_time=1.5)
        self.at("1981")
        year = label("1981", y=0.68, color=GOLD, size=33)
        self.play(FadeOut(reagent), swap(thought, year), run_time=0.66)
        organ = mouse_organ()
        self.play(FadeIn(organ, shift=LEFT * 0.25),
                  dish[1].animate.set_fill("#426A7C"), run_time=1.12)
        self.at("found such activity")
        extract = VGroup(drop(at_offset(LEFT_DISH, -0.9, 0.85), ORANGE, 0.84),
                         drop(at_offset(LEFT_DISH, -0.25, 0.53), ORANGE, 0.57))
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 1.7 + UP * 0.32) for d in extract],
                              lag_ratio=0.38),
                  dish[1].animate.set_fill("#2E596B"), run_time=1.38)
        self.at("healthy mouse organs")
        self.play(extract.animate.shift(DOWN * 0.56), run_time=0.62)
        population = grow(self, VGroup(fibro), cluster("fff", TGF_CENTER, 0.92, 0.72), 0.82)
        drift(population, 0.09)
        self.finish()


class S10bUnlockedTgfbTwo(SpokenScene):
    def construct(self):
        dish, surface = dish_side(True), gel_surface()
        extract = VGroup(drop(at_offset(LEFT_DISH, -0.9, 0.29), ORANGE, 0.84),
                         drop(at_offset(LEFT_DISH, -0.25, -0.03), ORANGE, 0.57))
        population = cluster("fff", TGF_CENTER, 0.92, 0.72)
        source = label(TGF_SOURCE, y=1.89, color=GOLD, size=30)
        organ, old_year = mouse_organ(), label("1981", y=0.68, color=GOLD, size=33)
        self.add(dish, surface, extract, population, source, organ, old_year)
        self.at("1983")
        year = label("1983", y=0.68, color=GOLD, size=33)
        self.play(FadeOut(organ), swap(old_year, year), run_time=0.85)
        drift(population, 0.10)
        self.at("two proteins")
        alpha_at, beta_at = at_offset(LEFT_DISH, -1.26, 0.96), at_offset(LEFT_DISH, 1.24, 0.96)
        alpha, beta = drop(alpha_at, ORANGE, 1.02), drop(beta_at, PURPLE, 1.02)
        self.play(ReplacementTransform(extract[0], alpha), ReplacementTransform(extract[1], beta),
                  run_time=1.33)
        a_name = chip("TGF-α", ORANGE, 29).move_to(p(2.4, -0.39))
        b_name = chip("TGF-β", PURPLE, 29).move_to(p(5.05, -0.39))
        self.play(FadeIn(a_name), FadeIn(b_name), run_time=0.56)
        self.at("TGFβ raised")
        fibro = cell("f", TGF_CENTER, 1.3)
        alone = label("TGF-β alone", y=-1.4, color=PURPLE, size=30)
        self.play(FadeOut(alpha), FadeOut(a_name), FadeOut(settle(population)),
                  FadeIn(fibro), FadeIn(alone),
                  beta.animate.move_to(at_offset(LEFT_DISH, 0, 0.64)), run_time=0.68)
        bob(fibro, amp=0.14, speed=1.45)
        self.at("only alongside")
        partner = drop(alpha_at, ORANGE, 0.91)
        paired = label("TGF-α or EGF", y=-1.4, color=ORANGE, size=31)
        self.play(swap(alone, paired), FadeIn(partner, shift=DOWN * 0.48), run_time=0.69)
        self.play(partner.animate.shift(RIGHT * 0.59 + DOWN * 0.69), run_time=0.72)
        target = cluster("fffffffffffff", TGF_CENTER + DOWN * 0.15, 0.9, 0.72)
        colony = grow(self, VGroup(fibro), VGroup(*target[:6]), 0.86)
        colony = grow(self, colony, target, 1.08)
        drift(colony, 0.08)
        self.finish()


IPS_SITES = [(-1.31, 0.98), (0.28, 1.5), (1.17, 0.55),
             (-1.20, -0.72), (0.25, -0.31), (1.14, -1.22)]


def genes_badge(value, wording):
    return counter(wording, value, p(3.74, 0.22), size=35, color=GOLD)


class S11UnlockedIps(SpokenScene):
    def construct(self):
        dish, surface = dish_side(True), gel_surface()
        old = cluster("fffffffffffff", TGF_CENTER + DOWN * 0.15, 0.9, 0.72)
        fibro = cells("ffffff", IPS_SITES, scale=1.14)
        self.add(dish, surface, old)
        self.at("colonies also guided")
        self.play(Transform(dish, petri()), FadeOut(surface), FadeOut(old),
                  FadeIn(fibro), run_time=1.45)
        drift(fibro, 0.1)
        self.at("2006")
        source = label("Takahashi & Yamanaka\n2006", y=1.9, color=GOLD, size=30)
        self.play(FadeIn(source), run_time=0.59)
        self.at("delivered 24")
        number = ValueTracker(24)
        genes = genes_badge(number, "{:.0f} genes")
        badge = chip("24 genes", GOLD, 29).move_to(p(3.74, 0.22))
        self.play(FadeIn(badge), run_time=0.5)
        entries = cells("cccccc", IPS_SITES, scale=0.30)
        self.play(LaggedStart(*(FadeIn(m, shift=RIGHT * 0.74 + UP * 0.48) for m in entries),
                              lag_ratio=0.18), run_time=1.55)
        self.play(FadeOut(entries, scale=0.55), run_time=0.66)
        self.at("linked a stem cell gene")
        linked = label("Linked to drug resistance", y=-1.05, color=TEXT, size=30)
        self.play(FadeIn(linked), run_time=0.57)
        self.at("drug resistance")
        wash = petri(tint="#496571")
        self.play(Transform(dish, wash), run_time=1.04)
        self.at("only cells activating")
        settle(fibro)
        survivors = VGroup(fibro[0], fibro[4], fibro[5])
        discarded = VGroup(fibro[1], fibro[2], fibro[3])
        self.play(FadeOut(discarded, scale=0.72),
                  *(Transform(f, cell("g", f.get_center(), 1.02)) for f in survivors),
                  run_time=1.06)
        self.at("formed colonies")
        centers = [at_offset(LEFT_DISH, *IPS_SITES[i]) for i in (0, 4, 5)]
        colonies = []
        for parent, center in zip(survivors, centers):
            colonies.append(grow(self, VGroup(parent), cluster("ggggg", center, 0.73, 0.8), 0.47))
        self.at("leaving out one factor")
        self.play(FadeOut(badge), FadeOut(linked), run_time=0.31)
        self.add(genes)
        self.play(number.animate.set_value(4), run_time=1.5, rate_func=linear)
        genes.clear_updaters()
        self.play(swap(genes, chip("4 factors", GOLD, 30).move_to(p(3.74, 0.22)), 0.44))
        self.at("induced pluripotent stem cells")
        for group in colonies:
            drift(group, 0.11)
        self.play(FadeIn(label("iPS cell colonies", y=-1.05, color=GREEN, size=32)), run_time=0.6)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        dish = petri(tint="#496571")
        previous = VGroup(*[cluster("ggggg", at_offset(LEFT_DISH, *IPS_SITES[i]),
                                     0.73, 0.8) for i in (0, 4, 5)])
        self.add(dish, previous)
        self.at("every colony reveals")
        founder = cell("c", p(*LEFT_DISH), 1.32)
        self.play(Transform(dish, petri()), FadeOut(previous), FadeIn(founder), run_time=0.7)
        first = grow(self, VGroup(founder), cluster("cc", p(*LEFT_DISH), 1.15, 1.26), 0.86)
        self.at("one isolated cell")
        first = grow(self, first, cluster("cccc", p(*LEFT_DISH), 1.15, 1.26), 0.62)
        final = grow(self, first, cluster(MIX, p(*LEFT_DISH), 1.53, 1.3), 0.81)
        potential = label("Potential", -2.85, 3.03, GOLD)
        self.play(FadeIn(potential), run_time=0.46)
        drift(final, 0.12)
        self.at("to learn what")
        body = embryo()
        trace = cell("n", at_offset(RIGHT_EMBRYO, -0.82, -0.62), 1.05)
        self.play(FadeIn(body, shift=LEFT * 0.23), run_time=0.83)
        self.play(FadeIn(trace), run_time=0.55)
        self.at("inside the living body")
        tissue = label("Living tissue", 3.55, 3.03, GREY)
        self.play(FadeIn(tissue), run_time=0.46)
        self.play(VGroup(dish, settle(final), body, trace, potential, tissue).animate.fade(0.52),
                  run_time=0.84)
        self.finish()


class S13End(EndCard):
    LINE = "Growing one cell into a colony tests potential, not fate."
