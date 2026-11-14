"""Extra Nutrients, Less Deep Oxygen.

COLOR MAP: nutrients GOLD, algae/plants GREEN, oxygen BLUE, decomposers GREY,
animals TEXT.  Every Bay scene is rebuilt by ``bay_world`` so the geography and
all carried objects remain at exactly the same scale and position.
"""
from types import SimpleNamespace

from bp_parts import *


NUT = GOLD
ALG = GREEN
OXY = BLUE
DECOMP = GREY
ANIMAL = TEXT
WATER = "#17324A"
DEEP = "#10263C"
LAND = "#705A38"


def _wave(y, color=BLUE, opacity=0.35, phase=0.0):
    """A broad, slowly moving current line used as honest ambient motion."""
    line = VMobject(stroke_color=color, stroke_width=2.5, stroke_opacity=opacity)
    line.phase = phase

    def redraw(mob, dt):
        mob.phase += 0.45 * dt
        xs = np.linspace(-2.7, 6.25, 70)
        pts = [np.array([x, y + 0.045 * np.sin(1.25 * x + mob.phase), 0]) for x in xs]
        mob.set_points_smoothly(pts)

    redraw(line, 0)
    line.add_updater(redraw)
    return line


def _nutrient(x, y, r=0.085):
    return Dot([x, y, 0], radius=r, color=NUT)


def _alga(x, y, color=ALG, scale=1.0):
    return Ellipse(width=0.22 * scale, height=0.12 * scale, color=color,
                   fill_color=color, fill_opacity=0.75, stroke_width=2).move_to([x, y, 0])


def _oxygen(x, y):
    return Dot([x, y, 0], radius=0.075, color=OXY, stroke_color=TEXT, stroke_width=1)


def _bacterium(x, y, scale=1.0):
    body = RoundedRectangle(corner_radius=0.09, width=0.35 * scale, height=0.17 * scale,
                            color=DECOMP, fill_color=DECOMP, fill_opacity=0.65, stroke_width=2)
    return body.rotate(0.25).move_to([x, y, 0])


def _fish(at=(3.6, -1.35, 0), scale=1.0):
    body = Ellipse(width=0.72 * scale, height=0.34 * scale, color=ANIMAL,
                   fill_color=ANIMAL, fill_opacity=0.15, stroke_width=3)
    tail = Polygon([-0.34, 0, 0], [-0.62, 0.22, 0], [-0.62, -0.22, 0], color=ANIMAL,
                   fill_color=ANIMAL, fill_opacity=0.12, stroke_width=3).scale(scale)
    eye = Dot([0.22 * scale, 0.06 * scale, 0], radius=0.025 * scale, color=ANIMAL)
    return VGroup(tail, body, eye).move_to(at)


def _crab(at=(1.8, -2.05, 0), scale=1.0):
    shell = Arc(radius=0.27 * scale, start_angle=0, angle=PI, color=ANIMAL, stroke_width=3)
    legs = VGroup(*[Line([dx, 0, 0], [dx + np.sign(dx) * 0.13, -0.18, 0], color=ANIMAL,
                              stroke_width=2.5) for dx in (-0.22, -0.08, 0.08, 0.22)])
    return VGroup(shell, legs).move_to(at)


def _oyster(at=(4.9, -2.08, 0), scale=1.0):
    shell = Arc(radius=0.27 * scale, start_angle=0, angle=PI, color=ANIMAL, stroke_width=4)
    base = Line(LEFT * 0.29 * scale, RIGHT * 0.29 * scale, color=ANIMAL, stroke_width=4)
    return VGroup(shell, base).move_to(at)


def bay_world(*, nutrients=False, bloom=False, sinking=False, low_oxygen=False,
              layered=False, bacteria=False, animals=True, questions=False):
    """Build the single carried Bay world at invariant scale and coordinates."""
    sky = Rectangle(width=12.8, height=1.55, stroke_width=0, fill_color="#17202B",
                    fill_opacity=1).move_to([0, 2.3, 0])
    land = Polygon([-6.4, 1.55, 0], [-3.25, 1.55, 0], [-2.55, 0.85, 0],
                   [-2.55, -2.35, 0], [-6.4, -2.35, 0], color=LAND,
                   fill_color=LAND, fill_opacity=0.48, stroke_width=2)
    upper = Polygon([-2.72, 1.38, 0], [6.35, 1.38, 0], [6.35, -0.25, 0],
                    [-2.55, -0.25, 0], color=OXY, fill_color=OXY,
                    fill_opacity=0.16 if not layered else 0.22, stroke_width=2)
    lower = Polygon([-2.55, -0.25, 0], [6.35, -0.25, 0], [6.35, -2.35, 0],
                    [-2.55, -2.35, 0], color=OXY, fill_color=DEEP,
                    fill_opacity=0.58 if layered else 0.42, stroke_width=2)
    bottom = VMobject(color=LAND, stroke_width=7).set_points_smoothly([
        [-2.55, -1.55, 0], [-0.8, -1.82, 0], [1.2, -2.18, 0], [3.4, -2.3, 0], [6.35, -2.27, 0]
    ])
    river = VMobject(color=OXY, stroke_width=12).set_points_smoothly([
        [-6.1, 0.7, 0], [-5.1, 0.4, 0], [-4.2, 0.65, 0], [-3.3, 0.75, 0], [-2.58, 0.8, 0]
    ])
    currents = VGroup(_wave(0.85, phase=0.0), _wave(0.35, phase=1.4),
                      _wave(-0.85, opacity=0.22, phase=2.2), _wave(-1.65, opacity=0.18, phase=3.0))
    root = VGroup(sky, land, upper, lower, currents, bottom, river)

    # Rain and fertilizer are always available in the field; scenes decide visibility.
    field_nutrients = VGroup(*[_nutrient(-5.75 + 0.32 * (i % 4), 1.18 - 0.23 * (i // 4)) for i in range(8)])
    rain = VGroup(*[Line([x, 3.0, 0], [x - 0.22, 2.45, 0], color=OXY, stroke_width=3)
                    for x in (-6.0, -5.45, -4.9, -4.35, -3.8)])
    sun = VGroup(Circle(radius=0.36, color=YELLOW, fill_color=YELLOW, fill_opacity=0.18,
                        stroke_width=3).move_to([5.55, 2.65, 0]),
                 *[Line([5.55, 2.65, 0] + 0.48 * np.array([np.cos(a), np.sin(a), 0]),
                        [5.55, 2.65, 0] + 0.68 * np.array([np.cos(a), np.sin(a), 0]),
                        color=YELLOW, stroke_width=2) for a in np.linspace(0, TAU, 8, endpoint=False)])
    root.add(sun)

    surface_oxygen = VGroup(*[_oxygen(x, y) for x, y in
                              [(-1.9, 1.0), (-0.7, 0.6), (0.7, 1.08), (2.0, 0.5),
                               (3.25, 1.02), (4.55, 0.58), (5.7, 1.05)]])
    deep_positions = [(-1.7, -0.72), (-0.45, -1.3), (0.85, -0.72), (2.1, -1.42),
                      (3.35, -0.8), (4.55, -1.55), (5.65, -0.9)]
    deep_oxygen = VGroup(*[_oxygen(x, y) for x, y in deep_positions])
    if low_oxygen:
        deep_oxygen = VGroup(*[_oxygen(*deep_positions[i]) for i in (0, 2)])
    root.add(surface_oxygen, deep_oxygen)
    bob(surface_oxygen, amp=0.035, speed=1.1)
    bob(deep_oxygen, amp=0.025, speed=0.9, seed=2)

    grass = VGroup(*[Line([x, -1.75, 0], [x + 0.04, -1.25, 0], color=ALG,
                               stroke_width=5) for x in (-2.25, -2.0, -1.75)])
    root.add(grass)
    algae_positions = [(-1.8, 0.92), (-1.05, 0.55), (-0.25, 1.02), (0.55, 0.62),
                       (1.35, 1.0), (2.15, 0.58), (2.95, 0.98), (3.8, 0.58),
                       (4.65, 1.0), (5.45, 0.65)]
    algae = VGroup(*[_alga(x, y) for x, y in algae_positions[:3 if not bloom else 10]])
    if bloom:
        root.add(algae)
        bob(algae, amp=0.035, speed=1.3, seed=1)
    dead_positions = [(-0.9, -0.55), (0.15, -1.15), (1.25, -1.72), (2.35, -0.95),
                      (3.35, -1.75), (4.45, -1.15)]
    dead = VGroup(*[_alga(x, y, DECOMP, 0.9) for x, y in dead_positions])
    if sinking:
        root.add(dead)
        bob(dead, amp=0.055, speed=0.8, seed=3)
    bugs = VGroup(*[_bacterium(x, y) for x, y in
                    [(-0.55, -1.9), (0.35, -1.72), (1.35, -2.02), (2.35, -1.8),
                     (3.4, -2.03), (4.35, -1.78)]])
    if bacteria:
        root.add(bugs)
        pulse(bugs, base=2.2, amp=0.7, speed=2.0)
    fish, crab, oyster = _fish(), _crab(), _oyster()
    animal_group = VGroup(fish, crab, oyster)
    if animals:
        root.add(animal_group)
        bob(fish, amp=0.045, speed=1.4)
    if nutrients:
        root.add(field_nutrients, rain)
        bob(field_nutrients, amp=0.035, speed=2.0)
    if layered:
        boundary = _wave(-0.25, color=TEXT, opacity=0.5, phase=0.5).set_stroke(width=5)
        root.add(boundary)
    else:
        boundary = VGroup()
    return SimpleNamespace(root=root, sky=sky, land=land, upper=upper, lower=lower,
                           river=river, rain=rain, field_nutrients=field_nutrients,
                           surface_oxygen=surface_oxygen, deep_oxygen=deep_oxygen,
                           grass=grass, algae=algae, dead=dead, bacteria=bugs,
                           fish=fish, crab=crab, oyster=oyster, animals=animal_group,
                           boundary=boundary, sun=sun)


def path_nodes():
    """Five compact nodes placed on the geography, not as a separate list."""
    return VGroup(
        Dot([-4.65, 0.55, 0], radius=0.16, color=NUT),
        Dot([0.15, 0.88, 0], radius=0.16, color=ALG),
        Dot([1.6, -1.82, 0], radius=0.16, color=DECOMP),
        Dot([3.2, -1.0, 0], radius=0.16, color=OXY),
        Dot([4.65, -1.86, 0], radius=0.16, color=ANIMAL),
    )


def path_arrows(nodes):
    return VGroup(*[Arrow(nodes[i].get_center(), nodes[i + 1].get_center(), buff=0.2,
                          color=GREY, stroke_width=3, max_tip_length_to_length_ratio=0.08)
                    for i in range(4)])


class S00Hook(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True)
        self.at("How can fertilizer")
        self.play(FadeIn(w.root), run_time=1.2)
        q = fit_text("How can fertilizer leave deep animals without oxygen?", max_w=8.6,
                     size=30, color=TEXT).move_to([0.0, 3.08, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.8)
        # Keep the opening question alive while its first sentence lands.
        self.play(w.rain.animate.shift(DOWN * 0.32),
                  w.upper.animate.set_fill(OXY, 0.27), run_time=2.2,
                  rate_func=there_and_back)
        self.at("Watch one Chesapeake")
        tag = scope_tag("schematic")
        river_flash = w.river.copy().set_stroke(OXY, width=18, opacity=0.9)
        self.play(ShowPassingFlash(river_flash, time_width=0.7), FadeIn(tag),
                  w.lower.animate.set_fill(DEEP, 0.62), run_time=1.7,
                  rate_func=there_and_back)
        self.at("answer begins")
        land_ring = SurroundingRectangle(w.field_nutrients, color=NUT, buff=0.16,
                                         corner_radius=0.12, stroke_width=4)
        self.play(Create(land_ring), Indicate(w.field_nutrients, color=NUT, scale_factor=1.25),
                  run_time=1.4)
        self.play(FadeOut(land_ring), run_time=0.45)
        self.at("surface may look")
        self.play(w.upper.animate.set_fill(ALG, 0.27), run_time=1.2)
        self.play(w.upper.animate.set_fill(OXY, 0.16), run_time=0.75)
        self.at("animals below")
        self.play(Indicate(w.animals, color=ANIMAL, scale_factor=1.15),
                  w.lower.animate.set_fill(DEEP, 0.62), run_time=1.7)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Big Changes: Dead Zones, Storms and Climate"
    TITLE = "Extra Nutrients, Less Deep Oxygen"

    def construct(self):
        w = bay_world(nutrients=True)
        self.add(w.root, scope_tag("schematic"))
        title = fit_text(self.TITLE, max_w=8.8, size=48, color=TEXT,
                         font=TITLE_FONT).move_to([0.7, 2.7, 0])
        backing = BackgroundRectangle(title, color=BG, fill_opacity=0.88, buff=0.22)
        self.play(FadeIn(backing), Write(title), run_time=0.75)
        self.wait(0.55)
        self.play(FadeOut(VGroup(backing, title), shift=RIGHT * 0.35), run_time=0.7)
        self.finish()


class S02Nutrients(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True)
        self.add(w.root, scope_tag("schematic"))
        self.at("Rain carries")
        self.play(w.rain.animate.shift(DOWN * 0.35), run_time=1.0)
        self.at("into a creek")
        moving = w.field_nutrients.copy()
        self.add(moving)
        self.play(moving.animate.move_to([-4.25, 0.55, 0]).scale(0.8), run_time=1.25)
        self.play(moving.animate.move_to([-1.35, 0.75, 0]), run_time=1.2)
        self.at("Fertilizer and manure")
        labels = VGroup(chip("fertilizer", NUT, 28), chip("manure", NUT, 28)).arrange(DOWN, buff=0.18)
        labels.move_to([-4.85, -0.75, 0])
        self.play(FadeIn(labels, shift=RIGHT * 0.15), run_time=0.7)
        self.at("nutrients that")
        nutrient = chip("nutrients", NUT, 32).move_to([0.7, 2.65, 0])
        self.play(ReplacementTransform(labels.copy(), nutrient), run_time=0.9)
        self.finish()


class S03Sources(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True)
        self.add(w.root, scope_tag("schematic"))
        self.at("Wastewater")
        waste = chip("wastewater", NUT, 28).move_to([-4.65, -0.55, 0])
        self.play(FadeIn(waste), run_time=0.6)
        self.at("air pollution")
        air = chip("some air pollution", NUT, 28).move_to([-1.1, 2.65, 0])
        self.play(FadeIn(air, shift=DOWN * 0.15), run_time=0.7)
        self.at("add nutrients too")
        streams = VGroup(Arrow(waste.get_right(), [-2.7, 0.58, 0], buff=0.15, color=NUT),
                         Arrow(air.get_bottom(), [-0.15, 0.85, 0], buff=0.15, color=NUT))
        self.play(LaggedStart(*[GrowArrow(a) for a in streams], lag_ratio=0.25), run_time=1.0)
        self.at("Nutrients help growth")
        self.play(Indicate(w.grass, color=ALG, scale_factor=1.15), run_time=1.0)
        self.at("where they go")
        self.play(FadeOut(VGroup(waste, air, streams)), Indicate(w.river, color=NUT), run_time=1.1)
        self.at("how much arrives")
        self.play(w.field_nutrients.animate.scale(1.25), rate_func=there_and_back, run_time=1.0)
        self.finish()


class S04Green(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True)
        self.add(w.root, scope_tag("schematic"))
        self.at("Pond water")
        window = VGroup(Rectangle(width=2.2, height=2.15, color=TEXT, stroke_width=4),
                        Line(UP * 1.07, DOWN * 1.07, color=TEXT, stroke_width=2),
                        Line(LEFT * 1.1, RIGHT * 1.1, color=TEXT, stroke_width=2)).move_to([-0.4, 0.4, 0])
        jar = RoundedRectangle(corner_radius=0.2, width=0.95, height=1.25, color=TEXT,
                               fill_color=OXY, fill_opacity=0.22).move_to([-0.4, 0.15, 0])
        inset = VGroup(window, jar)
        self.play(FadeIn(inset), run_time=0.75)
        self.at("turn green")
        self.play(jar.animate.set_fill(ALG, 0.58), run_time=1.2)
        self.at("In the bay")
        self.play(FadeOut(inset, scale=1.5), run_time=0.65)
        self.at("extra nitrogen")
        np_label = chip("nitrogen + phosphorus", NUT, 28).move_to([0.8, 2.65, 0])
        self.play(FadeIn(np_label), run_time=0.65)
        self.at("feed fast growth")
        algae = VGroup(*[_alga(x, y) for x, y in
                         [(-1.8, .92), (-1.05, .55), (-.25, 1.02), (.55, .62),
                          (1.35, 1.0), (2.15, .58), (2.95, .98), (3.8, .58), (4.65, 1.0)]])
        self.play(LaggedStart(*[GrowFromCenter(a) for a in algae], lag_ratio=0.09),
                  run_time=2.0)
        self.finish()


class S05Bloom(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True, bloom=True)
        self.add(w.root, scope_tag("schematic"))
        self.at("A thick growth")
        self.play(w.upper.animate.set_fill(ALG, 0.34), run_time=1.1)
        self.at("algae bloom")
        label = chip("algae bloom", ALG, 32).move_to([1.4, 2.65, 0])
        self.play(GrowFromCenter(label), run_time=0.7)
        self.at("More nutrients")
        self.play(w.field_nutrients.animate.shift(RIGHT * 1.3), run_time=1.2)
        self.at("conditions still matter")
        maybe = T("conditions still matter", 28, TEXT).move_to([-3.9, 2.05, 0])
        self.play(FadeIn(maybe), run_time=0.6)
        self.at("block sunlight")
        shadow = Polygon([-1.3, 0.25, 0], [0.35, 0.25, 0], [-1.35, -1.72, 0], [-2.35, -1.72, 0],
                         stroke_width=0, fill_color=BG, fill_opacity=0.62)
        self.play(FadeIn(shadow), w.grass.animate.set_opacity(0.3), run_time=1.4)
        self.at("grasses below")
        self.play(Indicate(w.grass, color=ALG), run_time=0.8)
        self.finish()


def predict_backdrop():
    w = bay_world(bloom=True, sinking=True)
    return w.root


class S06Sinking(SpokenScene):
    def construct(self):
        w = bay_world(bloom=True)
        self.add(w.root, scope_tag("schematic"))
        self.at("Later")
        self.play(w.algae.animate.set_color(DECOMP), run_time=0.7)
        self.at("die and sink")
        targets = [[-0.9, -0.55, 0], [0.15, -1.15, 0], [1.25, -1.72, 0],
                   [2.35, -0.95, 0], [3.35, -1.75, 0], [4.45, -1.15, 0]]
        self.play(*[w.algae[i].animate.move_to(targets[i]) for i in range(6)],
                  *[FadeOut(w.algae[i]) for i in range(6, len(w.algae))], run_time=2.0)
        self.at("next part")
        self.play(Indicate(VGroup(*w.algae[:6]), color=DECOMP), run_time=0.9)
        self.at("Now predict")
        q = question_card("Where will oxygen run low?", ["near the surface", "in deep water"],
                          chips_at=[-4.75, 2.45, 0], y=-3.22, max_w=9.4)
        self.play(FadeIn(q.chips), run_time=0.65)
        self.at("near the surface")
        self.play(FadeIn(q.question), run_time=0.65)
        self.finish()


class S07PredictPause(PredictPause):
    QUESTION = "Where will oxygen run low?"
    OPTIONS = ["near the surface", "in deep water"]
    CHIPS_AT = [-4.75, 2.45, 0]
    CARD = {"y": -3.22, "max_w": 9.4}
    SECONDS = 4.5

    def backdrop(self):
        return predict_backdrop()


class S08Decomposers(SpokenScene):
    def construct(self):
        w = bay_world(sinking=True)
        self.add(w.root, scope_tag("schematic"))
        self.at("Deep water")
        deep = T("deep water", 30, OXY).move_to([-1.0, -2.85, 0])
        self.play(FadeIn(deep), run_time=0.6)
        self.at("runs low")
        self.play(*[FadeOut(d) for d in w.deep_oxygen[2:]], run_time=1.2)
        self.at("Bacteria gather")
        bugs = VGroup(*[_bacterium(x, y) for x, y in
                        [(-.55, -1.9), (.35, -1.72), (1.35, -2.02), (2.35, -1.8), (3.4, -2.03)]])
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in bugs], lag_ratio=0.12), run_time=1.1)
        self.at("These decomposers")
        label = chip("decomposers", DECOMP, 30).move_to([2.8, 2.65, 0])
        self.play(FadeIn(label), run_time=0.6)
        self.at("use dissolved oxygen")
        survivors = list(w.deep_oxygen[:2])
        self.play(*[d.animate.move_to(bugs[i].get_center()) for i, d in enumerate(survivors)], run_time=1.2)
        self.play(*[FadeOut(d) for d in survivors], run_time=0.5)
        self.at("algae are food")
        self.play(Indicate(w.dead, color=DECOMP), Indicate(bugs, color=DECOMP), run_time=1.0)
        self.at("not direct")
        direct = T("not direct oxygen thieves", 30, TEXT).move_to([0.7, 2.6, 0])
        self.play(swap(label, direct), run_time=0.8)
        pulse(bugs, base=2.2, amp=0.7, speed=2.0)
        self.finish()


class S09Rule(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True, bloom=True, sinking=True, low_oxygen=True, bacteria=True)
        self.add(w.root, scope_tag("schematic"))
        nodes = path_nodes()
        arrows = path_arrows(nodes)
        self.at("Change one ecosystem")
        rule = fit_text("Change one part; effects can spread through the system.", max_w=8.4,
                        size=34, color=TEXT).move_to([-0.1, 2.8, 0])
        self.play(FadeIn(rule), run_time=0.8)
        self.at("Here")
        self.play(FadeIn(nodes[0]), run_time=0.4)
        self.at("nutrients change algae")
        self.play(GrowArrow(arrows[0]), FadeIn(nodes[1]), run_time=0.9)
        self.at("decomposition")
        self.play(GrowArrow(arrows[1]), FadeIn(nodes[2]), run_time=0.9)
        self.at("oxygen")
        self.play(GrowArrow(arrows[2]), FadeIn(nodes[3]), run_time=0.9)
        self.at("animal habitat")
        self.play(GrowArrow(arrows[3]), FadeIn(nodes[4]), run_time=0.9)
        self.at("Each step")
        self.play(LaggedStart(*[Indicate(n, scale_factor=1.8) for n in nodes], lag_ratio=0.22), run_time=2.8)
        self.finish()


class S10Layers(SpokenScene):
    def construct(self):
        w = bay_world(bloom=True, sinking=True, low_oxygen=True, layered=True, bacteria=True)
        self.add(w.root, scope_tag("schematic"))
        self.at("Summer makes")
        self.play(Indicate(w.sun, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.at("Fresher river water")
        fresh = T("fresher", 30, OXY).move_to([0.2, 0.8, 0])
        fresh.layout_ok = True  # Deliberately labels the upper water layer.
        self.play(FadeIn(fresh), run_time=0.7)
        self.at("saltier bay water")
        salty = T("saltier", 30, OXY).move_to([0.2, -1.05, 0])
        salty.layout_ok = True  # Deliberately labels the lower water layer.
        self.play(FadeIn(salty), run_time=0.7)
        self.at("layers mix poorly")
        self.play(Indicate(w.boundary, color=TEXT), run_time=1.2)
        mix = chip("mix poorly", TEXT, 28).move_to([-1.0, 2.65, 0])
        self.play(FadeIn(mix), run_time=0.55)
        self.at("Warm water")
        self.play(w.upper.animate.set_fill(YELLOW, 0.12), run_time=1.1)
        self.at("holds less oxygen")
        self.play(*[FadeOut(d) for d in w.surface_oxygen[::2]], run_time=1.1)
        self.at("Algae fed")
        self.play(Indicate(w.algae, color=ALG), run_time=1.0)
        self.at("sinking and decaying")
        self.play(w.dead.animate.shift(DOWN * 0.18), Indicate(w.bacteria, color=DECOMP), run_time=1.6)
        self.finish()


class S11Animals(SpokenScene):
    def construct(self):
        w = bay_world(sinking=True, low_oxygen=True, layered=True, bacteria=True)
        self.add(w.root, scope_tag("schematic"))
        self.at("Fish and crabs")
        self.play(Indicate(VGroup(w.fish, w.crab), color=ANIMAL), run_time=0.8)
        self.at("move away")
        self.play(w.fish.animate.move_to([1.0, 0.55, 0]),
                  w.crab.animate.move_to([-1.55, -1.35, 0]), run_time=2.0)
        self.at("Adult oysters")
        oyster_label = T("fixed in place", 30, ANIMAL).move_to([3.4, -2.9, 0])
        self.play(FadeIn(oyster_label), Indicate(w.oyster, color=ANIMAL), run_time=0.8)
        self.at("cannot leave")
        self.play(w.oyster.animate.set_opacity(0.5), run_time=1.1)
        self.at("sick or die")
        risk = T("may become sick or die", 30, RED).move_to([1.4, 2.65, 0])
        self.play(FadeIn(risk), run_time=0.7)
        self.at("Bacteria still")
        self.play(Indicate(w.bacteria, color=DECOMP), run_time=1.0)
        self.at("Low oxygen shrinks")
        habitat = Polygon([-2.45, -0.38, 0], [6.18, -0.38, 0], [6.18, -2.22, 0],
                          [-2.45, -1.55, 0], color=RED, fill_color=RED, fill_opacity=0.10,
                          stroke_width=4)
        self.play(Create(habitat), run_time=1.2)
        self.at("deep habitat")
        self.play(habitat.animate.scale(0.78, about_point=[6.18, -1.3, 0]), run_time=1.3)
        self.finish()


class S12Eutrophication(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True, bloom=True, sinking=True, low_oxygen=True, bacteria=True)
        self.add(w.root, scope_tag("schematic"))
        nodes = path_nodes()
        arrows = path_arrows(nodes)
        self.add(nodes, arrows)
        self.at("This process")
        title = T("eutrophication", 44, NUT, font=TITLE_FONT, weight=BOLD).move_to([0.8, 2.82, 0])
        self.play(FadeIn(title), run_time=0.7)
        self.at("Extra nutrients")
        self.play(Indicate(nodes[0], color=NUT, scale_factor=1.8), run_time=0.7)
        self.at("too much algae")
        self.play(Indicate(nodes[1], color=ALG, scale_factor=1.8), run_time=0.7)
        self.at("lead to low oxygen")
        self.play(Indicate(nodes[2], color=DECOMP, scale_factor=1.8),
                  Indicate(nodes[3], color=OXY, scale_factor=1.8), run_time=1.2)
        bracket = Brace(arrows, DOWN, color=NUT)
        meaning = T("can lead to low oxygen", 30, OXY).next_to(bracket, DOWN, buff=0.28)
        self.play(GrowFromCenter(bracket), FadeIn(meaning), run_time=0.9)
        self.at("Fertilizer does not")
        no_direct = Cross(Arrow(nodes[0].get_center(), nodes[3].get_center(), buff=0.2,
                                color=RED), stroke_color=RED, stroke_width=5)
        self.play(Create(no_direct), run_time=1.0)
        self.finish()


class S13Connections(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True, bloom=True, sinking=True, low_oxygen=True, bacteria=True)
        self.add(w.root, scope_tag("schematic"))
        nodes = path_nodes()
        arrows = path_arrows(nodes)
        self.add(nodes, arrows)
        self.at("effects travel")
        self.play(LaggedStart(*[Indicate(n, scale_factor=1.8) for n in nodes], lag_ratio=0.25), run_time=2.2)
        self.at("living connections")
        self.play(Indicate(arrows, color=NUT), run_time=1.0)
        self.at("word names")
        bracket = Brace(arrows, DOWN, color=NUT)
        label = T("eutrophication", 34, NUT).next_to(bracket, DOWN, buff=0.28)
        self.play(GrowFromCenter(bracket), FadeIn(label), run_time=0.8)
        self.at("not every patch")
        unrelated = VGroup(*[_alga(-5.75 + .28 * i, 2.45, ALG) for i in range(4)])
        self.play(FadeIn(unrelated), run_time=0.5)
        self.play(unrelated.animate.set_opacity(0.18), run_time=0.7)
        self.finish()


class S14Model(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True, bloom=True, sinking=True, low_oxygen=True, bacteria=True)
        self.add(w.root, scope_tag("schematic"))
        nodes = path_nodes()
        arrows = path_arrows(nodes)
        self.add(nodes, arrows)
        self.at("A useful model")
        self.play(LaggedStart(*[Indicate(a, color=NUT) for a in arrows], lag_ratio=0.18), run_time=1.8)
        self.at("starting point")
        self.play(Indicate(nodes[0], color=NUT, scale_factor=1.9), run_time=0.8)
        self.at("each connected part")
        self.play(LaggedStart(*[Indicate(n, scale_factor=1.6) for n in nodes[1:]], lag_ratio=0.16), run_time=1.6)
        self.at("what could weaken")
        qs = VGroup(*[T("?", 42, YELLOW, weight=BOLD).move_to(p) for p in
                      [(-3.7, 0.95, 0), (0.8, -0.25, 0), (5.3, -1.35, 0)]])
        for q in qs:
            q.layout_ok = True  # Each question mark intentionally sits on the link it questions.
        self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in qs], lag_ratio=0.25), run_time=1.2)
        self.at("interrupt the path")
        self.play(LaggedStart(*[Indicate(q, color=YELLOW) for q in qs], lag_ratio=0.25), run_time=1.2)
        self.finish()


class S15Evidence(SpokenScene):
    def construct(self):
        w = bay_world(nutrients=True, bloom=True, sinking=True, low_oxygen=True, bacteria=True)
        self.add(w.root, scope_tag("schematic"))
        nodes = path_nodes()
        arrows = path_arrows(nodes)
        self.add(nodes, arrows)
        self.at("makes the model")
        heading = T("test each connection", 34, TEXT).move_to([0.8, 2.75, 0])
        self.play(FadeIn(heading), run_time=0.7)
        self.at("useful for evidence")
        checks = VGroup()
        for a in arrows:
            check = T("✓", 31, NUT).move_to(a.get_center() + UP * 0.22)
            check.layout_ok = True  # Evidence mark intentionally belongs to its tested connection.
            checks.add(check)
            self.play(Indicate(a, color=NUT), FadeIn(check), run_time=0.65)
        self.at("not just memorizing")
        self.play(arrows.animate.set_opacity(0.45), checks.animate.set_opacity(0.8), run_time=0.8)
        self.at("Evidence can test")
        self.play(LaggedStart(*[Indicate(a, color=NUT) for a in arrows], lag_ratio=0.2), run_time=1.5)
        self.at("first and last")
        q = T("?", 44, YELLOW, weight=BOLD).move_to([5.35, -1.35, 0])
        self.play(FadeIn(q), run_time=0.6)
        self.finish()


class S16End(EndCard):
    LINE = "Change one ecosystem part, and effects can spread through the system."
