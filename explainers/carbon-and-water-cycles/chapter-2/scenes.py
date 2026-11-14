"""One Door for Two Cycles — chapter 2 of The carbon and water cycles.

COLOR MAP (kept exactly across both chapters)
  TEAL       = air-tub level / interface cue
  GREEN      = photosynthesis and plants
  ORANGE     = respiration / heat
  BROWN      = decomposition, soil and ground
  RED        = burning / hot, dry stress
  DARK_BLUE  = ocean
  LIGHT_BLUE = water, water vapour and water-cycle arrows
  GOLD       = sugar / sunlight
  PURPLE     = carbon dioxide

The yard, tub and leaf opening each have one builder.  Continued scenes call the
same builder with the same coordinates, so their landmarks never drift.
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BROWN = "#A8825A"
DARK_BLUE = "#3973A8"
LIGHT_BLUE = "#58C4DD"


def arr(a, b, color=GREY, width=6, tip=0.22):
    return Arrow(a, b, buff=0.02, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=12)


def drop(at, radius=0.09):
    """A readable cartoon water drop, not a molecular picture."""
    c = Circle(radius=radius, stroke_color=LIGHT_BLUE, stroke_width=2,
               fill_color=LIGHT_BLUE, fill_opacity=0.85).move_to(at)
    return c


def air_tub(center=(4.8, 0.25, 0), scale=1.0, level=0.60, arrow=False,
            arrow_width=8):
    """The chapter-1 glass air tub, with a TEAL marker and ppm readout."""
    c = np.array(center, dtype=float)
    glass = RoundedRectangle(corner_radius=0.18, width=2.55, height=4.6,
                             stroke_color=GREY, stroke_width=5,
                             fill_color=GREY, fill_opacity=0.07).move_to(c)
    rim = Line(c + [-1.0, 2.28, 0], c + [1.0, 2.28, 0], color=GREY, stroke_width=7)
    y = c[1] - 1.72 + 3.45 * level
    marker = Line([c[0] - 0.92, y, 0], [c[0] + 0.92, y, 0], color=TEAL, stroke_width=9)
    lab = T("air", 30, TEXT, weight=BOLD).move_to(c + [0, -1.55, 0])
    read = M("ppm", 28, TEAL).move_to(c + [0, 1.55, 0])
    # Labels intentionally live in the transparent tub.
    lab.layout_ok = read.layout_ok = True
    g = VGroup(glass, rim, marker, lab, read)
    g.glass, g.marker = glass, marker
    if arrow:
        ph = arr(c + [-1.28, 0.65, 0], c + [-2.55, -0.7, 0], GREEN,
                 width=arrow_width, tip=0.26)
        g.add(ph)
        g.photo_arrow = ph
    g.scale(scale)
    return g


def oak_yard(dry=False, rain=False, small=False):
    """The carried Virginia yard: one oak, ground and optional weather."""
    ground_y = -2.15
    soil = Rectangle(width=12.4, height=1.25, stroke_width=0,
                     fill_color=BROWN, fill_opacity=0.34).move_to([0, -2.78, 0])
    trunk = RoundedRectangle(corner_radius=0.12, width=0.62, height=2.7,
                             stroke_color=BROWN, stroke_width=5,
                             fill_color=BROWN, fill_opacity=0.55).move_to([-1.65, -0.82, 0])
    crown = Ellipse(width=4.25, height=3.2, stroke_color=GREEN, stroke_width=5,
                    fill_color=GREEN, fill_opacity=0.26).move_to([-1.65, 1.15, 0])
    roots = VGroup(*[Line([-1.65, -2.08, 0], [-1.65 + dx, -2.9, 0],
                              color=BROWN, stroke_width=5) for dx in (-1.2, -0.55, 0.55, 1.2)])
    g = VGroup(soil, roots, trunk, crown)
    if dry:
        cracks = VGroup(*[
            VMobject(color=TEXT, stroke_width=3).set_points_as_corners([
                [x, ground_y - 0.1, 0], [x + 0.18, ground_y - 0.32, 0],
                [x - 0.05, ground_y - 0.55, 0]]) for x in (-5.2, -3.7, 0.7, 2.3)
        ])
        sun = Circle(radius=0.62, color=RED, stroke_width=6,
                     fill_color=RED, fill_opacity=0.25).move_to([-5.3, 2.8, 0])
        g.add(cracks, sun)
        g.cracks, g.sun = cracks, sun
    if rain:
        cloud = VGroup(
            Ellipse(width=2.9, height=1.0, color=GREY, stroke_width=4,
                    fill_color=GREY, fill_opacity=0.25).move_to([-4.5, 2.75, 0]),
            Circle(radius=0.72, color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=0.25).move_to([-5.0, 3.02, 0]),
            Circle(radius=0.84, color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=0.25).move_to([-4.15, 3.06, 0]))
        rain_drops = VGroup(*[drop([x, 2.1 - 0.18 * (i % 2), 0], 0.105)
                              for i, x in enumerate(np.linspace(-5.35, -3.65, 7))])
        g.add(cloud, rain_drops)
        g.cloud, g.rain = cloud, rain_drops
    if small:
        g.scale(0.72, about_point=[-1.65, -2.15, 0]).shift(LEFT * 0.5)
    g.soil, g.trunk, g.crown, g.roots = soil, trunk, crown, roots
    return g


def stoma(opening=1.15, center=(0, 0.2, 0), scale=1.0, arrows=True):
    """A schematic leaf opening: two guard-cell lips and both cycle directions."""
    c = np.array(center, dtype=float)
    leaf = Ellipse(width=8.2, height=5.4, stroke_color=GREEN, stroke_width=5,
                   fill_color=GREEN, fill_opacity=0.10).move_to(c)
    left = ArcBetweenPoints(c + [-opening / 2, -1.35, 0], c + [-opening / 2, 1.35, 0],
                            angle=-1.0, color=GREEN, stroke_width=18)
    right = ArcBetweenPoints(c + [opening / 2, 1.35, 0], c + [opening / 2, -1.35, 0],
                             angle=-1.0, color=GREEN, stroke_width=18)
    gap = T("one door", 32, TEXT, weight=BOLD).move_to(c + [0, 1.95, 0])
    g = VGroup(leaf, left, right, gap)
    g.leaf, g.left_lip, g.right_lip, g.gap_label = leaf, left, right, gap
    if arrows:
        water = arr(c + [0.18, 0.55, 0], c + [3.0, 1.65, 0], LIGHT_BLUE, 7, 0.25)
        carbon = arr(c + [3.0, -1.25, 0], c + [0.15, -0.35, 0], PURPLE, 7, 0.25)
        g.add(water, carbon)
        g.water_arrow, g.carbon_arrow = water, carbon
    g.scale(scale)
    return g


def dry_prediction_backdrop():
    """Exact final picture shared by s09 and the silent predict pause."""
    yard = oak_yard(dry=True, small=True)
    yard.shift(LEFT * 2.25)
    yard.sun.shift(RIGHT * 1.15)
    pore = stoma(opening=0.25, center=(2.75, 0.35, 0), scale=0.56, arrows=False)
    pore.remove(pore.gap_label)
    yard.layout_ok = True  # the bottom question chips deliberately sit over the ground band
    tub = air_tub(center=(5.65, 2.35, 0), scale=0.42, arrow=True, arrow_width=8)
    thin_water = arr([2.85, 0.55, 0], [4.2, 1.2, 0], LIGHT_BLUE, 2.5, 0.14)
    question = T("?", 40, GOLD, weight=BOLD).move_to([5.0, 1.95, 0])
    return VGroup(yard, pore, tub, thin_water, question)


class S00Title(TitleCard):
    LESSON = "The carbon and water cycles"
    TITLE = "One Door for Two Cycles"


class S01Hook(SpokenScene):
    def construct(self):
        yard = oak_yard(dry=True)
        tub = air_tub(center=(5.2, 0.45, 0), scale=0.82)
        self.play(FadeIn(yard.soil), GrowFromCenter(yard.sun), run_time=0.8)
        self.play(FadeIn(yard.roots), FadeIn(yard.trunk), GrowFromCenter(yard.crown), run_time=1.0)
        self.at("carbon dioxide in the air")
        self.play(FadeIn(tub), run_time=0.8)
        q = question_card("Can a dry summer change the air's carbon dioxide?",
                          y=-3.18, size=30, max_w=10.7)
        self.play(FadeIn(q), run_time=0.7)
        wilted = yard.crown.copy().stretch(0.82, 1).shift(DOWN * 0.28).set_fill(opacity=0.18)
        self.play(Transform(yard.crown, wilted), run_time=2.2, rate_func=smooth)
        self.at("follow water")
        drops = VGroup(*[drop([-2.65 + 0.45 * i, -2.62, 0], 0.1) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in drops], lag_ratio=0.15),
                  run_time=0.8)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        yard = oak_yard()
        tub = air_tub(center=(4.8, 0.25, 0), scale=0.92)
        self.play(FadeIn(tub), FadeIn(yard), run_time=0.9)
        self.at("green arrow drained")
        ph = arr([3.5, 1.0, 0], [0.15, 1.25, 0], GREEN, 11, 0.3)
        pl = T("photosynthesis", 30, GREEN, weight=BOLD).move_to([2.0, 1.75, 0])
        self.play(GrowArrow(ph), FadeIn(pl), tub.marker.animate.shift(DOWN * 0.55), run_time=1.5)
        self.at("Now follow")
        small_tub = air_tub(center=(5.65, 2.55, 0), scale=0.43)
        drops = VGroup(*[drop([-3.2 + 0.55 * i, -2.62, 0], 0.105) for i in range(6)])
        self.play(FadeOut(ph), FadeOut(pl), Transform(tub, small_tub),
                  LaggedStart(*[FadeIn(d, shift=DOWN * 0.2) for d in drops], lag_ratio=0.12),
                  run_time=1.4)
        self.finish()


class S03Ground(SpokenScene):
    def construct(self):
        yard = oak_yard(rain=True)
        tub = air_tub(center=(5.65, 2.55, 0), scale=0.43)
        self.play(FadeIn(yard.soil), FadeIn(yard.trunk), FadeIn(yard.crown), FadeIn(tub), run_time=0.8)
        self.at("Rain falls")
        self.play(FadeIn(yard.cloud), LaggedStart(*[FadeIn(d, shift=DOWN * 0.8) for d in yard.rain], lag_ratio=0.1),
                  run_time=1.4)
        precip = T("precipitation", 30, LIGHT_BLUE, weight=BOLD).move_to([-4.93, 0.3, 0])
        self.at("That is precipitation")
        self.play(FadeIn(precip), run_time=0.6)
        self.at("soaks into")
        sink = VGroup(*[arr([x, -2.05, 0], [x, -3.15, 0], LIGHT_BLUE, 5, 0.18)
                        for x in (-3.0, -2.35, -1.7)])
        self.play(LaggedStart(*[GrowArrow(a) for a in sink], lag_ratio=0.2), run_time=1.2)
        infil = T("infiltration", 30, LIGHT_BLUE, weight=BOLD).move_to([-3.9, -3.25, 0])
        self.at("which is infiltration")
        self.play(FadeOut(precip), FadeIn(infil), run_time=0.6)
        self.at("flows downhill")
        stream = RoundedRectangle(corner_radius=0.2, width=3.0, height=0.62,
                                  stroke_color=LIGHT_BLUE, stroke_width=3,
                                  fill_color=LIGHT_BLUE, fill_opacity=0.45).rotate(-0.12).move_to([3.75, -2.55, 0])
        flow = arr([1.7, -2.18, 0], [4.8, -2.6, 0], LIGHT_BLUE, 8, 0.28)
        self.play(FadeIn(stream), GrowArrow(flow), run_time=1.2)
        runoff = T("runoff", 30, LIGHT_BLUE, weight=BOLD).move_to([3.6, -1.85, 0])
        self.at("That is runoff")
        self.play(FadeOut(infil), FadeIn(runoff), run_time=0.6)
        self.finish()


class S04Up(SpokenScene):
    def construct(self):
        yard = oak_yard()
        tub = air_tub(center=(5.65, 2.55, 0), scale=0.43)
        self.play(FadeIn(yard), FadeIn(tub), run_time=0.8)
        self.at("roots take water")
        root_drops = VGroup(*[drop([-2.75 + 0.55 * i, -2.68, 0], 0.11) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(d) for d in root_drops], lag_ratio=0.12), run_time=0.8)
        self.at("moves up")
        up = arr([-1.65, -2.2, 0], [-1.65, 1.1, 0], LIGHT_BLUE, 9, 0.28)
        branches = VGroup(arr([-1.65, 0.15, 0], [-2.9, 1.35, 0], LIGHT_BLUE, 5, 0.18),
                          arr([-1.65, 0.15, 0], [-0.35, 1.35, 0], LIGHT_BLUE, 5, 0.18))
        self.play(GrowArrow(up), LaggedStart(*[GrowArrow(a) for a in branches], lag_ratio=0.2), run_time=1.6)
        self.at("leaves through tiny openings")
        vapour = VGroup(*[arr([x, 2.05, 0], [x + 0.15, 3.0, 0], LIGHT_BLUE, 5, 0.18)
                          for x in (-2.85, -1.65, -0.45)])
        travelling = VGroup(*[drop([-2.9 + 0.23 * i, 0.65 + 0.12 * (i % 3), 0], 0.13)
                              for i in range(12)])
        self.add(travelling)
        self.play(Indicate(yard.crown, color=LIGHT_BLUE, scale_factor=1.08), run_time=1.0)
        self.play(LaggedStart(*[d.animate.shift(UP * (1.7 + 0.1 * (i % 2)))
                                for i, d in enumerate(travelling)], lag_ratio=0.08),
                  LaggedStart(*[GrowArrow(a) for a in vapour], lag_ratio=0.18),
                  run_time=3.4, rate_func=linear)
        self.play(Indicate(yard.crown, color=LIGHT_BLUE, scale_factor=1.08), run_time=1.0)
        trans = T("transpiration", 34, LIGHT_BLUE, weight=BOLD).move_to([1.75, 2.3, 0])
        self.at("That is transpiration")
        self.play(FadeIn(trans), run_time=0.7)
        self.finish()


class S05Sky(SpokenScene):
    def construct(self):
        yard = oak_yard(small=True)
        pond = Ellipse(width=2.2, height=0.52, stroke_color=LIGHT_BLUE, stroke_width=3,
                       fill_color=LIGHT_BLUE, fill_opacity=0.5).move_to([-4.85, -2.14, 0])
        ocean = Rectangle(width=3.4, height=1.0, stroke_width=0, fill_color=DARK_BLUE,
                          fill_opacity=0.7).move_to([5.0, -2.65, 0])
        self.play(FadeIn(yard), FadeIn(pond), FadeIn(ocean), run_time=0.8)
        self.at("evaporates from the pond")
        pond_v = VGroup(*[arr([x, -1.9, 0], [x + 0.1, -0.35, 0], LIGHT_BLUE, 4, 0.16)
                          for x in (-5.25, -4.75)])
        self.play(LaggedStart(*[GrowArrow(a) for a in pond_v], lag_ratio=0.2), run_time=1.0)
        self.at("most of all from the ocean")
        ocean_v = VGroup(*[arr([x, -2.1, 0], [x - 0.1, 0.25, 0], LIGHT_BLUE, 7, 0.22)
                           for x in (4.15, 4.85, 5.55)])
        evap = T("evaporation", 30, LIGHT_BLUE, weight=BOLD).move_to([4.65, 0.7, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in ocean_v], lag_ratio=0.15), FadeIn(evap), run_time=1.3)
        self.at("vapor cools")
        cloud = VGroup(Circle(0.72), Circle(0.92), Circle(0.68)).arrange(RIGHT, buff=-0.4)
        cloud.set_stroke(GREY, 4).set_fill(GREY, 0.28).move_to([0.9, 2.55, 0])
        beads = VGroup(*[drop([0.15 + 0.35 * i, 2.55 + 0.15 * (i % 2), 0], 0.09) for i in range(6)])
        rising = VGroup(*[drop([-4.9 + 0.62 * i, -0.3 + 0.12 * (i % 3), 0], 0.12)
                          for i in range(14)])
        self.add(rising)
        targets = [np.array([0.1 + 0.17 * i, 2.45 + 0.17 * (i % 3), 0]) for i in range(14)]
        self.play(LaggedStart(*[d.animate.move_to(p) for d, p in zip(rising, targets)], lag_ratio=0.05),
                  FadeIn(beads), FadeIn(cloud), run_time=3.2, rate_func=linear)
        cond = T("condensation", 30, LIGHT_BLUE, weight=BOLD).move_to([-2.2, 3.25, 0])
        self.at("That is condensation")
        self.play(FadeIn(cond), run_time=0.6)
        self.at("rain falls again")
        rain = VGroup(*[arr([x, 1.95, 0], [x - 0.1, 0.55, 0], LIGHT_BLUE, 4, 0.16)
                        for x in (0.15, 0.65, 1.15, 1.65)])
        self.play(LaggedStart(*[GrowArrow(a) for a in rain], lag_ratio=0.12), run_time=1.1)
        words = VGroup(*[T(w, 28, LIGHT_BLUE) for w in
                         ("precipitation", "infiltration", "runoff", "transpiration")])
        for w, p in zip(words, ([-4.5, 1.65, 0], [-3.8, -3.25, 0], [2.4, -2.55, 0], [-2.0, 1.35, 0])):
            w.move_to(p)
        words.layout_ok = True  # process names sit around their own water-cycle picture
        self.play(FadeIn(words), run_time=0.8)
        self.finish()


class S06Share(SpokenScene):
    def construct(self):
        title = fit_text("water moving from land into the air", max_w=11.2, size=34, color=LIGHT_BLUE)
        title.move_to([0, 3.15, 0])
        frame = RoundedRectangle(corner_radius=0.22, width=11.0, height=2.1,
                                 stroke_color=GREY, stroke_width=4).move_to([0, 0.35, 0])
        plant = Rectangle(width=7.1, height=1.55, stroke_width=0,
                          fill_color=GREEN, fill_opacity=0.72).align_to(frame, LEFT).shift(RIGHT * 0.25)
        plant.move_to([-1.7, 0.35, 0], aligned_edge=LEFT)
        rest = Rectangle(width=3.35, height=1.55, stroke_width=0,
                         fill_color=LIGHT_BLUE, fill_opacity=0.35).next_to(plant, RIGHT, buff=0)
        self.play(FadeIn(title), Create(frame), run_time=1.0)
        self.at("Plants move")
        self.play(GrowFromEdge(plant, LEFT), run_time=1.3)
        self.at("one study estimated")
        self.play(GrowFromEdge(rest, LEFT), run_time=0.8)
        plab = fit_text("through plants — nearly two thirds", max_w=7.0, size=30,
                        color=TEXT, max_lines=1).move_to([-1.5, 0.35, 0])
        plab.layout_ok = True
        self.play(FadeIn(plab), run_time=0.7)
        bracket = BraceBetweenPoints([-4.7, -1.15, 0], [2.25, -1.15, 0], DOWN, color=GOLD)
        estimate = T("one study's estimate", 28, GOLD).next_to(bracket, DOWN, buff=0.15)
        self.at("goes through plants")
        self.play(GrowFromCenter(bracket), FadeIn(estimate), run_time=0.9)
        self.at("wide range")
        wide = DoubleArrow([-4.9, -2.55, 0], [3.6, -2.55, 0], color=GREY,
                           stroke_width=5, tip_length=0.2)
        wlab = T("wide range", 28, TEXT).next_to(wide, DOWN, buff=0.12)
        self.play(GrowFromCenter(wide), FadeIn(wlab), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S07Door(SpokenScene):
    def construct(self):
        leaf = Ellipse(width=8.8, height=5.6, stroke_color=GREEN, stroke_width=5,
                       fill_color=GREEN, fill_opacity=0.15).move_to([-0.7, 0.1, 0])
        leaf.layout_ok = True  # labels sit just inside the leaf silhouette
        self.play(GrowFromCenter(leaf), run_time=1.2)
        self.at("zoom into one leaf")
        pore = stoma(opening=1.15, center=(-0.7, 0.1, 0), scale=1.0, arrows=False)
        pore.leaf.layout_ok = True
        self.play(FadeOut(leaf), FadeIn(pore.leaf), Create(pore.left_lip), Create(pore.right_lip), run_time=1.3)
        tiny = T("tiny opening — schematic", 28, GREY).move_to([-0.7, -2.85, 0])
        self.play(FadeIn(tiny), run_time=0.5)
        self.at("Carbon dioxide comes in")
        carbon = arr([4.35, -1.0, 0], [-0.25, -0.25, 0], PURPLE, 9, 0.3)
        clab = T("carbon dioxide in", 30, PURPLE, weight=BOLD).move_to([3.15, -1.75, 0])
        self.play(GrowArrow(carbon), FadeIn(clab), run_time=1.2)
        self.at("water vapor goes out")
        water = arr([-0.3, 0.45, 0], [4.25, 1.55, 0], LIGHT_BLUE, 9, 0.3)
        wlab = T("water vapor out", 30, LIGHT_BLUE, weight=BOLD).move_to([3.15, 2.15, 0])
        self.play(GrowArrow(water), FadeIn(wlab), run_time=1.2)
        self.at("One door")
        self.play(FadeIn(pore.gap_label), Indicate(VGroup(pore.left_lip, pore.right_lip),
                                                   color=GOLD, scale_factor=1.06), run_time=0.9)
        self.finish()


class S08Sugar(SpokenScene):
    def construct(self):
        leaf = Ellipse(width=11.2, height=6.2, stroke_color=GREEN, stroke_width=5,
                       fill_color=GREEN, fill_opacity=0.10).move_to([0, 0.1, 0])
        leaf.layout_ok = True  # path labels are intentionally inside this leaf cutaway
        box = chip("photosynthesis", GREEN, size=32).move_to([0, 0.15, 0])
        self.play(FadeIn(leaf), FadeIn(box), run_time=0.9)
        self.at("uses water")
        wa = arr([-4.9, -2.4, 0], [-1.25, -0.2, 0], LIGHT_BLUE, 9, 0.28)
        wl = T("from the roots", 28, LIGHT_BLUE).move_to([-3.65, -2.65, 0])
        self.play(GrowArrow(wa), FadeIn(wl), run_time=1.2)
        self.at("carbon dioxide together")
        ca = arr([4.9, 2.35, 0], [1.25, 0.45, 0], PURPLE, 9, 0.28)
        cl = T("through the door", 28, PURPLE).move_to([3.65, 2.65, 0])
        self.play(GrowArrow(ca), FadeIn(cl), run_time=1.2)
        self.at("make sugar")
        cubes = VGroup(*[Square(0.48, color=GOLD, stroke_width=4,
                                fill_color=GOLD, fill_opacity=0.25) for _ in range(9)])
        cubes.arrange_in_grid(3, 3, buff=0.18).move_to([0, -1.35, 0])
        sugar = T("sugar", 32, GOLD, weight=BOLD).move_to([0, -2.55, 0])
        for c in cubes:
            c.save_state()
            c.scale(0.05).move_to(box)
        self.add(cubes)
        self.play(LaggedStart(*[Restore(c) for c in cubes], lag_ratio=0.1), FadeIn(sugar),
                  run_time=3.0, rate_func=linear)
        self.at("water came up")
        self.play(Indicate(VGroup(wa, cubes), color=LIGHT_BLUE, scale_factor=1.10), run_time=1.0)
        self.at("carbon dioxide came in")
        self.play(Indicate(VGroup(ca, cubes), color=PURPLE, scale_factor=1.10), run_time=1.0)
        self.finish()


class S09Predict(SpokenScene):
    def construct(self):
        wet = oak_yard(small=True)
        wet.shift(LEFT * 2.25)
        wet.layout_ok = True  # transformed yard later shares its ground band with prediction chips
        pore_open = stoma(opening=1.05, center=(2.75, 0.35, 0), scale=0.56, arrows=False)
        pore_open.remove(pore_open.gap_label)
        tub = air_tub(center=(5.65, 2.35, 0), scale=0.42, arrow=True, arrow_width=8)
        self.play(FadeIn(wet), FadeIn(pore_open), FadeIn(tub), run_time=0.9)
        self.at("hot dry summer")
        dry = oak_yard(dry=True, small=True)
        dry.shift(LEFT * 2.25)
        dry.sun.shift(RIGHT * 1.15)
        dry.layout_ok = True  # question chips later share the ground band
        self.play(Transform(wet, dry), run_time=1.1)
        self.at("soil dries out")
        roots = VGroup(*[drop([-4.4 + 0.35 * i, -2.72, 0], 0.08) for i in range(4)])
        self.play(FadeIn(roots), FadeOut(roots, shift=DOWN * 0.25), run_time=1.0)
        self.at("closes its tiny openings")
        pore_closed = stoma(opening=0.25, center=(2.75, 0.35, 0), scale=0.56, arrows=False)
        pore_closed.remove(pore_closed.gap_label)
        self.play(Transform(pore_open, pore_closed), run_time=1.4)
        thin_water = arr([2.85, 0.55, 0], [4.2, 1.2, 0], LIGHT_BLUE, 2.5, 0.14)
        question = T("?", 40, GOLD, weight=BOLD).move_to([5.0, 1.95, 0])
        self.play(GrowArrow(thin_water), FadeIn(question), run_time=0.7)
        self.at("What happens")
        q = question_card("Green arrow: thicker, thinner or the same?",
                          ["thicker", "thinner", "the same"], y=-3.55, size=29, chips_at=[4.0, -2.15, 0], left=-6.3, max_w=9.0)
        q.chips[0].shift(RIGHT * 0.98)
        self.play(FadeIn(q.chips), FadeIn(q.question), run_time=0.9)
        self.at("Pause and predict")
        self.play(Indicate(tub, color=GOLD, scale_factor=1.08), run_time=0.8)
        self.finish()


class S10Pause(PredictPause):
    QUESTION = "Green arrow: thicker, thinner or the same?"
    OPTIONS = ["thicker", "thinner", "the same"]
    CARD = {"y": -3.55, "size": 29, "chips_at": [4.0, -2.15, 0], "left": -6.3, "max_w": 9.0}
    RING_AT = (5.65, -2.85, 0)

    def backdrop(self):
        return dry_prediction_backdrop()

    def construct(self):
        bd = self.backdrop()
        self.add(bd)
        q = question_card(self.QUESTION, self.OPTIONS, **self.CARD)
        q.chips[0].shift(RIGHT * 0.98)
        self.add(q)
        progress = ValueTracker(1.0)
        center = np.array(self.RING_AT, dtype=float)
        rim = Circle(radius=0.68, color=GREY, stroke_width=5).move_to(center)
        arc = always_redraw(lambda: Arc(radius=0.68, start_angle=PI / 2,
                                        angle=max(progress.get_value(), 0.001) * TAU,
                                        color=GOLD, stroke_width=12, arc_center=center))
        numeral = always_redraw(lambda: M(str(max(1, int(np.ceil(progress.get_value() * 5)))),
                                           32, GOLD).move_to(center))
        self.add(rim, arc, numeral)
        pulse = Succession(*[AnimationGroup(Indicate(bd[4], color=GOLD, scale_factor=1.5),
                                            Indicate(bd[3], color=LIGHT_BLUE, scale_factor=1.12),
                                            Indicate(bd[2], color=GOLD, scale_factor=1.06))
                             for _ in range(4)])
        self.play(progress.animate.set_value(0), pulse, run_time=5.0, rate_func=linear)


class S11Reveal(SpokenScene):
    def construct(self):
        backdrop = dry_prediction_backdrop()
        self.add(backdrop)
        answer = T("THINNER", 46, GOLD, weight=BOLD).move_to([-4.6, 2.75, 0])
        self.at("It gets thinner")
        tub = backdrop[2]
        thin = air_tub(center=(5.65, 2.35, 0), scale=0.42, arrow=True, arrow_width=3)
        self.play(FadeIn(answer, scale=0.8), FadeOut(backdrop[4]),
                  Transform(tub, thin), run_time=1.4)
        self.at("less carbon dioxide gets in")
        pore = backdrop[1]
        self.play(FadeOut(backdrop[0]), pore.animate.scale(1.28).shift(LEFT * 0.45), run_time=1.0)
        carbon = arr([4.2, -0.15, 0], [2.85, 0.15, 0], PURPLE, 2.5, 0.14)
        particles = VGroup(*[Dot([4.05 + 0.12 * i, -0.12, 0], radius=0.12, color=PURPLE)
                             for i in range(5)])
        self.play(GrowArrow(carbon), run_time=0.8)
        self.add(particles)
        self.play(LaggedStart(*[p.animate.move_to([2.9, 0.15 + 0.08 * (i % 2), 0])
                                for i, p in enumerate(particles)], lag_ratio=0.18),
                  run_time=2.8, rate_func=linear)
        self.at("takes less carbon")
        self.play(pore.animate.scale(0.88).shift(RIGHT * 0.25),
                  Indicate(tub.photo_arrow, color=GREEN, scale_factor=1.18), run_time=1.0)
        rule = fit_text("less water out  •  less carbon in", max_w=9.2, size=34,
                        color=TEXT, max_lines=1).move_to([0, -3.25, 0])
        self.play(FadeIn(rule), run_time=0.8)
        self.finish()


class S12Europe(SpokenScene):
    def construct(self):
        # A deliberately simple, schematic geographic silhouette.
        europe = Polygon([-5.5, 1.7, 0], [-4.55, 2.8, 0], [-3.45, 2.45, 0],
                         [-2.65, 1.35, 0], [-3.25, 0.45, 0], [-2.75, -0.65, 0],
                         [-3.75, -1.7, 0], [-5.2, -1.15, 0], [-5.7, 0.2, 0],
                         stroke_color=ORANGE, stroke_width=5,
                         fill_color=ORANGE, fill_opacity=0.34)
        self.play(GrowFromCenter(europe), run_time=1.1)
        self.at("real forests")
        year = fit_text("2003: very hot, dry summer", max_w=5.4, size=30,
                        color=ORANGE, weight=BOLD, max_lines=1).move_to([-3.9, -2.3, 0])
        self.at("Europe had")
        rays = VGroup(*[Line([0, 0.85, 0], [0, 1.35, 0], color=RED, stroke_width=7)
                        .rotate(i * TAU / 12, about_point=ORIGIN) for i in range(12)])
        sun = VGroup(Circle(0.62, color=RED, stroke_width=7,
                            fill_color=RED, fill_opacity=0.28), rays).move_to([-1.05, 2.35, 0])
        self.play(FadeIn(year), FadeIn(sun), run_time=0.8)
        self.play(Rotate(rays, angle=PI, about_point=sun[0].get_center()), run_time=3.2, rate_func=linear)
        usual = Rectangle(width=1.55, height=4.2, stroke_color=GREEN, stroke_width=4,
                          fill_color=GREEN, fill_opacity=0.55).move_to([1.45, -0.25, 0])
        less = Rectangle(width=1.55, height=2.94, stroke_color=GREEN, stroke_width=4,
                         fill_color=GREEN, fill_opacity=0.32).move_to([4.25, -0.88, 0])
        ul = T("usual", 30, TEXT).next_to(usual, DOWN, buff=0.2)
        ll = T("hot, dry summer", 28, TEXT).next_to(less, DOWN, buff=0.2)
        self.at("One study estimated")
        self.play(GrowFromEdge(usual, DOWN), FadeIn(ul), run_time=1.0)
        self.at("about 30")
        self.play(GrowFromEdge(less, DOWN), FadeIn(ll), run_time=1.0)
        down = T("about 30% less", 34, GOLD, weight=BOLD).move_to([4.25, 1.35, 0])
        note = T("one study's estimate", 28, GREY).move_to([2.85, 2.65, 0])
        self.play(FadeIn(down), FadeIn(note), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S13Energy(SpokenScene):
    def construct(self):
        oak = oak_yard(small=True)
        oak.shift(DOWN * 0.05)
        carbon_loop = Circle(radius=1.55, color=GREEN, stroke_width=8).move_to([-4.2, 0.8, 0])
        water_loop = Circle(radius=1.55, color=LIGHT_BLUE, stroke_width=8).move_to([4.2, 0.8, 0])
        carbon_markers = VGroup(*[Dot([-4.2 + 1.55 * np.cos(a), 0.8 + 1.55 * np.sin(a), 0],
                                      radius=0.16, color=GOLD) for a in np.linspace(0, TAU, 8, endpoint=False)])
        water_markers = VGroup(*[Dot([4.2 + 1.55 * np.cos(a), 0.8 + 1.55 * np.sin(a), 0],
                                     radius=0.16, color=TEXT) for a in np.linspace(0, TAU, 8, endpoint=False)])
        self.play(FadeIn(oak), Create(carbon_loop), Create(water_loop),
                  FadeIn(carbon_markers), FadeIn(water_markers), run_time=1.3)
        self.at("does not cycle")
        cl = T("carbon", 30, GREEN, weight=BOLD).move_to([-4.34, 0.8, 0])
        wl = T("water", 30, LIGHT_BLUE, weight=BOLD).move_to([4.2, 0.8, 0])
        self.at("Carbon and water")
        self.play(FadeIn(cl), FadeIn(wl), Rotate(carbon_markers, TAU), Rotate(water_markers, -TAU),
                  run_time=4.0, rate_func=linear)
        self.at("Energy does not")
        sun = arr([-6.2, 2.8, 0], [-2.3, 1.35, 0], GOLD, 10, 0.32)
        sl = T("sunlight", 30, GOLD, weight=BOLD).move_to([-4.46, 2.9, 0])
        self.play(GrowArrow(sun), FadeIn(sl), run_time=1.1)
        self.at("leaves as heat")
        heat = arr([0.15, 1.2, 0], [5.9, 2.7, 0], ORANGE, 10, 0.32)
        hl = T("heat", 30, ORANGE, weight=BOLD).move_to([4.75, 2.7, 0])
        self.play(GrowArrow(heat), FadeIn(hl), run_time=1.1)
        self.at("new sunlight every day")
        rule = caption("matter cycles; energy flows through", size=34, color=TEXT)
        self.play(FadeIn(rule), Indicate(sun, color=GOLD), run_time=1.0)
        self.finish()


class S14Recap(SpokenScene):
    def construct(self):
        pore = stoma(opening=1.15, center=(0, 0.25, 0), scale=0.82, arrows=True)
        self.play(FadeIn(pore.leaf), Create(pore.left_lip), Create(pore.right_lip), run_time=1.0)
        self.at("linked at the leaf")
        self.play(FadeIn(pore.gap_label), run_time=0.7)
        self.at("Water going out")
        self.play(GrowArrow(pore.water_arrow), run_time=0.9)
        wlab = T("water out", 30, LIGHT_BLUE, weight=BOLD).move_to([4.45, 1.85, 0])
        self.play(FadeIn(wlab), run_time=0.5)
        self.at("carbon dioxide coming in")
        self.play(GrowArrow(pore.carbon_arrow), run_time=0.9)
        clab = T("carbon dioxide in", 30, PURPLE, weight=BOLD).move_to([4.35, -1.75, 0])
        self.play(FadeIn(clab), run_time=0.5)
        self.at("same tiny openings")
        glow = Circle(radius=0.78, color=GOLD, stroke_width=10).move_to([0, 0.25, 0])
        self.play(Create(glow), run_time=0.8)
        self.at("change in one cycle")
        rule = caption("Change one cycle, and the other can change.", size=34, color=TEXT)
        self.play(FadeIn(rule), Indicate(glow, color=GOLD, scale_factor=1.12), run_time=1.0)
        self.finish()


class S15End(EndCard):
    LINE = "Water out and carbon in use the same door."
