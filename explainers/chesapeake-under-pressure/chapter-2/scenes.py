"""Design a Fix That Can Be Tested — Chesapeake Under Pressure, chapter 2.

COLOR MAP (continued exactly from chapter 1)
  ORANGE = nutrients / nitrogen pressure
  GREEN  = living plants, forest buffer, cover crops
  BLUE   = dissolved oxygen
  TEAL   = fresh surface water and underwater grass
  NAVY   = salty bottom water
  GOLD   = habitat and the limited budget
  GREY   = land, structures, constraints
  TEXT   = animals and evidence
"""
from bp_parts import *  # noqa: F401,F403

ORANGE = "#F29E4C"
NAVY = "#173A5E"
NUT, OXY, FRESH, HAB = ORANGE, BLUE, TEAL, GOLD


def arrow(a, b, color=GREY, width=6, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def watershed_world(*, compact=False, labels=True, motion=True):
    """The carried Chesapeake picture, rebuilt at one scale and position in every scene."""
    y0 = -0.35 if compact else -0.15
    land = Polygon([-6.25, y0 + 1.65, 0], [-2.75, y0 + 1.0, 0], [-2.15, y0 + 0.25, 0],
                   [-2.15, y0 - 2.15, 0], [-6.25, y0 - 2.15, 0],
                   stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.32)
    river = Polygon([-5.75, y0 + 0.3, 0], [-2.2, y0 - 0.25, 0], [0.0, y0 + 0.25, 0],
                    [0.0, y0 - 0.45, 0], [-2.2, y0 - 0.75, 0], [-5.75, y0 - 0.15, 0],
                    stroke_color=FRESH, stroke_width=4, fill_color=FRESH, fill_opacity=0.38)
    surface = Rectangle(width=6.15, height=1.5, stroke_color=FRESH, stroke_width=3,
                        fill_color=FRESH, fill_opacity=0.28).move_to([3.05, y0 + 0.25, 0])
    bottom = Rectangle(width=6.15, height=1.45, stroke_color=NAVY, stroke_width=3,
                       fill_color=NAVY, fill_opacity=0.68).move_to([3.05, y0 - 1.22, 0])
    field = VGroup(*[Line([-5.85, y0 + 1.25 - i * 0.35, 0], [-3.15, y0 + 0.72 - i * 0.28, 0],
                          color=GREY, stroke_width=3) for i in range(4)])
    g = VGroup(land, river, surface, bottom, field)
    g.land, g.river, g.surface, g.bottom, g.field = land, river, surface, bottom, field
    if labels:
        labs = VGroup(T("field", 28, GREY).move_to([-4.75, y0 + 1.65, 0]),
                      T("river", 28, FRESH).move_to([-1.45, y0 + 0.92, 0]),
                      T("Bay", 30, TEXT, weight=BOLD).move_to([3.1, y0 + 1.35, 0]))
        g.add(labs)
        g.labels = labs
    flow = VGroup(*[Dot([-5.35 + i * 0.72, y0 + 0.08 - 0.05 * i, 0], radius=0.09, color=FRESH)
                    for i in range(6)])
    if motion:
        for d in flow:
            d._base_x = d.get_x()
            d._t = 0.0
            def drift(m, dt):
                m._t += dt
                x = m._base_x + 0.34 * m._t
                if x > -0.75:
                    m._t = 0.0
                    x = m._base_x
                m.set_x(x)
            d.add_updater(drift)
    g.add(flow)
    g.flow = flow
    if motion:
        pulse(river, base=4.0, amp=1.2, speed=2.2)
        pulse(surface, base=3.0, amp=0.9, speed=1.7)
        pulse(bottom, base=3.0, amp=0.7, speed=1.4)
        ripples = VGroup(
            Line([0.45, y0 + 0.55, 0], [2.65, y0 + 0.55, 0], color=FRESH, stroke_width=5),
            Line([3.25, y0 + 0.05, 0], [5.55, y0 + 0.05, 0], color=FRESH, stroke_width=5),
            Line([0.7, y0 - 1.05, 0], [3.15, y0 - 1.05, 0], color=BLUE, stroke_width=4),
            Line([3.65, y0 - 1.65, 0], [5.8, y0 - 1.65, 0], color=BLUE, stroke_width=4),
        ).set_opacity(0.30)
        g.add(ripples)
        g.ripples = ripples
        bob(ripples, amp=0.11, speed=1.7)
    return g


def budget_bar(y=3.0):
    """The same limited budget bar wherever the plan is shown."""
    box = RoundedRectangle(corner_radius=0.14, width=7.0, height=0.66,
                           stroke_color=HAB, stroke_width=3, fill_color=HAB, fill_opacity=0.10)
    box.move_to([1.9, y, 0])
    fill = Rectangle(width=5.15, height=0.42, stroke_width=0, fill_color=HAB,
                     fill_opacity=0.75).align_to(box, LEFT).shift(RIGHT * 0.12).move_to(
                         [box.get_left()[0] + 0.12 + 5.15 / 2, y, 0])
    lab = T("limited cleanup budget", 28, HAB, weight=BOLD).next_to(box, LEFT, buff=0.25)
    g = VGroup(box, fill, lab)
    g.box, g.fill = box, fill
    return g


def nutrient_markers(n=8, start=(-5.6, 0.5, 0)):
    return VGroup(*[Dot(np.array(start) + [0.2 * (i % 4), -0.22 * (i // 4), 0],
                        radius=0.11, color=NUT) for i in range(n)])


def grass_bed(center=(4.8, -2.0, 0), n=9, color=HAB):
    x, y, _ = center
    blades = VGroup(*[Line([x - 0.8 + i * 0.2, y - 0.45, 0],
                           [x - 0.72 + i * 0.2, y + 0.25 + 0.12 * (i % 3), 0],
                           color=color, stroke_width=6) for i in range(n)])
    return blades


def oyster_reef(center=(2.6, -2.0, 0)):
    x, y, _ = center
    shells = VGroup(*[Arc(radius=0.28, start_angle=0, angle=PI, color=HAB, stroke_width=6)
                      .move_to([x + dx, y + dy, 0])
                      for dx, dy in [(-0.6, 0), (0, 0), (0.6, 0), (-0.3, 0.35), (0.3, 0.35)]])
    return shells


def moving_markers(path, color, n=8, speed=0.6):
    """Dots flowing along an evidence link, so the link stays active while it is discussed."""
    start, end = path.get_start(), path.get_end()
    marks = VGroup(*[Dot(interpolate(start, end, i / n), radius=0.085, color=color)
                     for i in range(n)])
    for i, mark in enumerate(marks):
        mark._p = i / n
        def travel(m, dt, a=start, b=end):
            m._p = (m._p + speed * dt) % 1.0
            m.move_to(interpolate(a, b, m._p))
        mark.add_updater(travel)
    return marks


def outcome_cards():
    panels = TwoPanel("less nutrient pressure", "fully regrown grass bed",
                      colors=(NUT, HAB), top=2.85, bottom=-1.65, width=12.4)
    small = arrow([-5.3, 0.2, 0], [-2.0, 0.2, 0], NUT, width=9)
    bed = grass_bed((3.2, 0.2, 0), n=11)
    panels.put(small, "left")
    panels.put(bed, "right")
    q = question_card("Which appears first?", y=-3.05, size=34)
    return VGroup(panels, small, bed, q)


class S00Hook(SpokenScene):
    def construct(self):
        world = watershed_world()
        self.play(FadeIn(world), run_time=0.9)
        nutrients = nutrient_markers(9)
        self.at("nutrients from land")
        self.add(nutrients)
        targets = [[-1.4 + 0.55 * i, 0.25 - 0.12 * (i % 3), 0] for i in range(9)]
        self.play(*[d.animate.move_to(p) for d, p in zip(nutrients, targets)], run_time=2.0)
        oxygen = VGroup(*[Dot([1.2 + 0.55 * i, -1.25, 0], radius=0.11, color=OXY) for i in range(8)])
        self.at("low oxygen")
        self.play(FadeIn(oxygen), FadeOut(oxygen[::2]), world.bottom.animate.set_fill(NAVY, 0.75), run_time=1.2)
        budget = budget_bar()
        self.at("limited cleanup budget")
        self.play(FadeIn(budget, shift=DOWN * 0.15), run_time=0.8)
        cause = arrow([-5.4, 2.15, 0], [-2.65, 1.65, 0], NUT, width=8)
        habitat = grass_bed((4.7, -1.95, 0), n=8)
        self.at("cuts the cause first")
        self.play(GrowArrow(cause), nutrients.animate.set_opacity(0.35), run_time=0.9)
        self.at("rebuilds habitat")
        self.play(LaggedStart(*[Create(b) for b in habitat], lag_ratio=0.08), run_time=1.0)
        self.at("real limits")
        self.play(budget.fill.animate.set_width(3.7).align_to(budget.box, LEFT).shift(RIGHT * 0.12), run_time=0.8)
        self.finish()


class S01Title(TitleCard):
    LESSON = "The Chesapeake Under Pressure"
    TITLE = "Design a Fix That Can Be Tested"


class S02Design(SpokenScene):
    def construct(self):
        panels = TwoPanel("criteria", "constraints", colors=(HAB, GREY), top=2.8, bottom=-2.35)
        self.at("returning a damaged ecosystem")
        self.play(FadeIn(panels), run_time=0.9)
        bob(panels, amp=0.12, speed=1.7)
        health = T("toward health", 34, GREEN, weight=BOLD).move_to([-3.25, 1.1, 0])
        self.play(FadeIn(health, shift=UP * 0.15), run_time=0.8)
        long_arrow = arrow([-5.5, -0.2, 0], [-1.2, -0.2, 0], NUT, width=10)
        short_arrow = arrow([-5.5, -0.2, 0], [-3.4, -0.2, 0], NUT, width=10)
        bed = grass_bed((-3.25, -1.35, 0), n=9)
        self.at("Criteria say")
        self.play(FadeIn(long_arrow), run_time=0.6)
        bob(long_arrow, amp=0.10, speed=1.6)
        self.at("lowering nitrogen")
        self.play(Transform(long_arrow, short_arrow), run_time=0.9)
        self.at("adding habitat")
        self.play(LaggedStart(*[Create(x) for x in bed], lag_ratio=0.08), run_time=1.0)
        bob(bed, amp=0.10, speed=1.8)
        bar = RoundedRectangle(corner_radius=0.12, width=4.7, height=0.62, color=HAB).move_to([3.25, 0.65, 0])
        divs = VGroup(Line([2.5, 0.34, 0], [2.5, 0.96, 0], color=HAB),
                      Line([3.7, 0.34, 0], [3.7, 0.96, 0], color=HAB))
        self.at("Constraints are limits")
        self.play(Create(bar), run_time=0.7)
        bob(bar, amp=0.10, speed=1.5)
        names = VGroup(T("money", 28, TEXT), T("land", 28, TEXT), T("time", 28, TEXT))
        for t, x in zip(names, (1.72, 3.1, 4.65)):
            t.move_to([x, 0.65, 0])
        self.at("money")
        self.play(Create(divs[0]), FadeIn(names[0]), run_time=0.45)
        self.at("land")
        self.play(Create(divs[1]), FadeIn(names[1]), run_time=0.45)
        self.at("time")
        self.play(FadeIn(names[2]), run_time=0.45)
        trade = VGroup(arrow([2.0, -1.0, 0], [4.5, -1.0, 0], GREY),
                       arrow([4.5, -1.65, 0], [2.0, -1.65, 0], GREY),
                       T("trade-off", 32, HAB, weight=BOLD).move_to([3.25, -1.33, 0]))
        self.at("every choice")
        self.play(FadeIn(trade), run_time=1.0)
        self.finish()


class S03Land(SpokenScene):
    def construct(self):
        world = watershed_world()
        self.add(world)
        self.at("Start upstream")
        self.play(Indicate(world.land, color=GREEN, scale_factor=1.02), run_time=0.7)
        buffer = Rectangle(width=0.75, height=3.35, stroke_color=GREEN, stroke_width=3,
                           fill_color=GREEN, fill_opacity=0.28).move_to([-2.55, -0.55, 0])
        trees = VGroup(*[Triangle(color=GREEN, fill_color=GREEN, fill_opacity=0.8, stroke_width=0)
                         .scale(0.18).move_to([-2.55, 0.75 - i * 0.48, 0]) for i in range(6)])
        self.at("forest buffer")
        self.play(FadeIn(buffer), LaggedStart(*[GrowFromCenter(t) for t in trees], lag_ratio=0.1), run_time=1.2)
        label = T("forest buffer", 30, GREEN, weight=BOLD).move_to([-3.45, 2.05, 0])
        self.at("beside a stream")
        self.play(FadeIn(label), run_time=0.6)
        nuts = nutrient_markers(8, (-5.5, 0.55, 0))
        self.add(nuts)
        self.at("slows runoff")
        self.play(*[d.animate.move_to([-2.95, 0.55 - 0.25 * i, 0]) for i, d in enumerate(nuts)], run_time=1.2)
        self.at("traps soil")
        self.play(*[d.animate.set_opacity(0.18) for d in nuts[2:6]], run_time=0.7)
        roots = VGroup(*[Line([-2.55, -0.6 - i * 0.22, 0], [-2.85 + 0.12 * (i % 2), -1.0 - i * 0.22, 0],
                                  color=GREEN, stroke_width=4) for i in range(5)])
        self.at("remove nitrate")
        self.play(Create(roots), nuts[6:].animate.set_opacity(0.12), run_time=1.0)
        crops = VGroup(*[Line([-5.8 + i * 0.32, -1.65, 0], [-5.72 + i * 0.32, -1.15, 0],
                                  color=GREEN, stroke_width=5) for i in range(9)])
        crop_lab = T("winter cover crop", 28, GREEN).move_to([-4.3, -2.95, 0])
        self.at("Winter cover crops")
        self.play(LaggedStart(*[Create(c) for c in crops], lag_ratio=0.06), FadeIn(crop_lab), run_time=1.1)
        self.at("take up leftover nitrogen")
        self.play(*[d.animate.move_to(crops[i % len(crops)].get_top()).set_opacity(0.15)
                    for i, d in enumerate(nuts[:4])], run_time=1.1)
        varies = T("effect varies with place", 28, GREY).move_to([-0.1, 2.35, 0])
        self.at("before nutrients reach")
        self.play(FadeIn(varies), Indicate(VGroup(buffer, crops), color=GREEN), run_time=1.0)
        self.finish()


class S04OtherTools(SpokenScene):
    def construct(self):
        world = watershed_world()
        self.add(world)
        plant = chip("treatment plant", GREY, size=28).move_to([-1.4, 1.8, 0])
        inlet = arrow([-4.0, 1.75, 0], [-3.08, 1.8, 0], NUT)  # ends at the chip edge
        loop = CurvedArrow(plant.get_right(), plant.get_bottom(), angle=-PI * 0.8, color=NUT, stroke_width=6)
        outlet = arrow([0.25, 1.5, 0], [0.8, 1.0, 0], FRESH)
        self.at("Wastewater upgrades")
        self.play(FadeIn(plant), GrowArrow(inlet), run_time=0.9)
        self.at("remove more nitrogen")
        self.play(Create(loop), GrowArrow(outlet), run_time=1.0)
        reef = oyster_reef()
        self.at("Oyster reefs")
        self.play(LaggedStart(*[Create(s) for s in reef], lag_ratio=0.1), run_time=1.1)
        particles = VGroup(*[Dot([1.6 + 0.35 * i, -0.7, 0], radius=0.08, color=GREY) for i in range(5)])
        self.at("filter particles")
        self.play(FadeIn(particles), *[p.animate.move_to(reef[i].get_center()).set_opacity(0.15)
                                      for i, p in enumerate(particles)], run_time=1.1)
        animals = VGroup(chip("crab", TEXT, 24).move_to([1.4, -2.4, 0]),
                         chip("fish", TEXT, 24).move_to([3.6, -2.4, 0]))
        self.at("shelters other animals")
        self.play(FadeIn(animals), run_time=0.8)
        source = arrow([-5.8, 1.1, 0], [-3.2, 0.65, 0], NUT, width=9)
        self.at("do not replace cutting nutrients")
        self.play(GrowArrow(source), Indicate(reef, color=HAB), run_time=1.0)
        grass = grass_bed((5.0, -2.0, 0), n=9, color=HAB).set_opacity(0.18)
        self.at("underwater grass")
        self.play(FadeIn(grass), run_time=0.7)
        readout = T("readout — not a tool", 30, HAB, weight=BOLD).move_to([4.55, 2.1, 0])
        self.at("readout not a tool")
        self.play(FadeIn(readout), run_time=0.7)
        self.at("Cleaner water")
        self.play(world.surface.animate.set_fill(FRESH, 0.06), run_time=0.8)
        self.at("let it return")
        self.play(grass.animate.set_opacity(1.0), run_time=1.2)
        self.finish()


class S05MapTools(SpokenScene):
    def construct(self):
        world = watershed_world(labels=False)
        budget = budget_bar()
        self.add(world, budget)
        bob(budget, amp=0.12, speed=1.6)
        tools = VGroup(chip("buffer", GREEN, 24).move_to([-5.15, 1.55, 0]),
                       chip("cover crop", GREEN, 24).move_to([-3.3, 0.8, 0]),
                       chip("plant", GREY, 24).move_to([-0.55, 2.05, 0]),
                       chip("reef", HAB, 24).move_to([1.8, -2.05, 0]))
        # This chip is deliberately pinned to the field polygon: it names the map location.
        tools[1][1].layout_ok = True
        self.at("Place each tool")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tools], lag_ratio=0.12), run_time=1.2)
        pressure = arrow([-5.7, 2.25, 0], [0.2, 1.0, 0], NUT, width=10)
        self.at("reduce orange nutrient flow")
        self.play(GrowArrow(pressure), run_time=1.4)
        small = arrow([-1.0, 0.8, 0], [0.5, 0.5, 0], NUT, width=6)
        self.play(Transform(pressure, small), run_time=0.8)
        reef_patch = oyster_reef((3.25, -1.65, 0))
        habitat_path = arrow([2.5, -0.7, 0], [5.4, -0.7, 0], HAB, width=9)
        self.at("add habitat directly")
        self.play(GrowArrow(habitat_path), FadeIn(reef_patch), run_time=1.0)
        bed = grass_bed((5.0, -1.9, 0), n=8)
        dotted = DashedLine([0.7, 0.3, 0], [4.7, -1.15, 0], color=HAB, stroke_width=5)
        self.at("cleaner water")
        self.play(Create(dotted), run_time=0.8)
        self.at("grass return")
        self.play(LaggedStart(*[Create(b) for b in bed], lag_ratio=0.07), run_time=0.9)
        rule = caption("Cut nutrients first; then add habitat within criteria and budget.", color=TEXT)
        self.at("cuts nutrients first")
        self.play(FadeIn(rule), Indicate(small, color=NUT), run_time=0.9)
        self.at("then adds habitat")
        self.play(Indicate(VGroup(reef_patch, bed), color=HAB), run_time=0.9)
        self.at("budget allow")
        self.play(budget.fill.animate.set_width(3.5).align_to(budget.box, LEFT).shift(RIGHT * 0.12), run_time=0.8)
        self.finish()


class S06Compare(SpokenScene):
    def construct(self):
        mini = watershed_world(compact=True, labels=False, motion=False).scale(0.55).move_to([0, -2.55, 0])
        self.add(mini)
        vals = [ValueTracker(0.72), ValueTracker(0.34), ValueTracker(0.22)]
        gauges = VGroup(dial(vals[0], [-4.25, 0.75, 0], radius=1.35, label="nitrogen load", color=NUT),
                        dial(vals[1], [0, 0.75, 0], radius=1.35, label="summer oxygen", color=OXY),
                        dial(vals[2], [4.25, 0.75, 0], radius=1.35, label="underwater grass", color=HAB))
        # The dial label deliberately sits in its own gauge's lower band.
        gauges[2][-1].layout_ok = True
        self.at("No single readout")
        self.play(LaggedStart(*[FadeIn(g) for g in gauges], lag_ratio=0.15), run_time=1.2)
        bob(gauges, amp=0.09, speed=1.6)
        links = VGroup(DashedLine([-4.25, -0.95, 0], [-2.6, -1.8, 0], color=NUT),
                       DashedLine([0, -0.95, 0], [1.2, -1.95, 0], color=OXY),
                       DashedLine([4.25, -0.95, 0], [3.6, -2.35, 0], color=HAB))
        self.at("Nitrogen load")
        self.play(Create(links[0]), vals[0].animate.set_value(0.45), run_time=1.1)
        self.add(moving_markers(links[0], NUT))
        total = fit_text("pressure entering the Bay", max_w=3.4, size=27, color=NUT,
                         max_lines=2).move_to([-4.25, 2.65, 0])
        self.at("pressure entering")
        self.play(FadeIn(total), run_time=0.7)
        self.at("Summer oxygen")
        self.play(Create(links[1]), vals[1].animate.set_value(0.58), run_time=1.1)
        self.add(moving_markers(links[1], OXY, speed=0.55))
        cond = fit_text("condition animals need", max_w=3.4, size=27, color=OXY,
                        max_lines=2).move_to([0, 2.65, 0])
        self.play(FadeIn(cond), run_time=0.6)
        self.at("Underwater grass")
        self.play(Create(links[2]), vals[2].animate.set_value(0.32), run_time=1.1)
        self.add(moving_markers(links[2], HAB, speed=0.5))
        hab = T("habitat", 28, HAB).move_to([4.25, 2.65, 0])
        self.play(FadeIn(hab), run_time=0.6)
        self.at("improve one before another")
        self.play(vals[0].animate.set_value(0.25), run_time=0.8)
        self.play(vals[1].animate.set_value(0.7), run_time=0.8)
        self.play(vals[2].animate.set_value(0.48), run_time=0.8)
        self.at("all three gauges")
        self.play(Indicate(gauges, color=TEXT, scale_factor=1.01), run_time=0.8)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        cards = outcome_cards()
        bob(cards[1], amp=0.10, speed=1.5)
        bob(cards[2], amp=0.10, speed=1.8, seed=2)
        self.at("nutrient flow drops")
        self.play(FadeIn(cards[0]), FadeIn(cards[1]), run_time=1.0)
        self.play(cards[1].animate.scale(0.72), run_time=0.9)
        self.at("Which change")
        self.play(FadeIn(cards[3]), run_time=0.8)
        self.at("Less nutrient pressure")
        self.play(Indicate(cards[1], color=NUT, scale_factor=1.03), run_time=0.7)
        self.at("fully regrown grass bed")
        self.play(Indicate(cards[2], color=HAB, scale_factor=1.03), run_time=0.7)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Which appears first?"
    SECONDS = 4.5

    def backdrop(self):
        cards = outcome_cards()
        bob(cards[1], amp=0.10, speed=1.5)
        bob(cards[2], amp=0.10, speed=1.8, seed=2)
        return VGroup(cards[0], cards[1].scale(0.72), cards[2])


class S09Lag(SpokenScene):
    def construct(self):
        timeline = arrow([-5.8, -2.45, 0], [5.8, -2.45, 0], GREY, width=5)
        ticks = VGroup(*[Line([x, -2.65, 0], [x, -2.25, 0], color=GREY, stroke_width=3)
                         for x in (-4.5, -1.5, 1.5, 4.5)])
        pulse(timeline, base=5.0, amp=1.2, speed=1.6)
        bob(timeline, amp=0.11, speed=1.5)
        self.add(timeline, ticks, scope_tag("schematic"))
        pressure = arrow([-5.2, 1.85, 0], [-2.4, 1.85, 0], NUT, width=9)
        pmark = Dot([-3.7, -2.45, 0], radius=0.16, color=NUT)
        self.at("Less nutrient pressure")
        self.play(GrowArrow(pressure), FadeIn(pmark), run_time=1.0)
        soil_box = RoundedRectangle(corner_radius=0.16, width=3.2, height=1.45, color=GREY,
                                    fill_color=GREY, fill_opacity=0.25).move_to([-3.9, 0.2, 0])
        store = VGroup(*[Dot([-4.9 + 0.38 * (i % 6), 0.45 - 0.4 * (i // 6), 0], radius=0.09, color=NUT)
                         for i in range(12)])
        soil_lab = T("stored nitrogen in soil", 28, NUT).next_to(soil_box, UP, buff=0.18)
        self.at("Grass recovery often lags")
        self.play(FadeIn(soil_box), FadeIn(store), FadeIn(soil_lab), run_time=1.0)
        water = Rectangle(width=4.5, height=1.45, color=FRESH, fill_color=NAVY,
                          fill_opacity=0.65).move_to([2.9, 0.25, 0])
        grass = grass_bed((3.0, -0.1, 0), n=10).set_opacity(0.15)
        pulse(water, base=4.0, amp=1.1, speed=1.8)
        bob(grass, amp=0.10, speed=1.7)
        self.add(water, grass)
        self.at("water must clear")
        self.play(water.animate.set_fill(FRESH, 0.16), run_time=1.2)
        self.at("time to spread back")
        self.play(grass.animate.set_opacity(1.0), run_time=1.4)
        gmark = Dot([2.6, -2.45, 0], radius=0.16, color=HAB)
        self.play(FadeIn(gmark), run_time=0.5)
        leaks = VGroup(*[arrow([-3.0 + 0.18 * i, 0.1, 0], [-1.8 + 0.18 * i, -0.35, 0], NUT, width=3, tip=0.12)
                         for i in range(3)])
        self.at("leaking from soil")
        self.play(Create(leaks), *[d.animate.set_opacity(0.18) for d in store[:5]], run_time=1.2)
        self.at("for years")
        self.play(pmark.animate.move_to([-2.1, -2.45, 0]), run_time=1.0)
        years = T("several years", 30, GREY).move_to([0, -3.05, 0])
        self.play(FadeIn(years), run_time=0.5)
        self.at("Track each criterion")
        self.play(Indicate(VGroup(pmark, gmark), color=TEXT, scale_factor=1.5), run_time=0.9)
        self.at("instead of judging one sample")
        samples = VGroup(*[Dot([x, -2.45, 0], radius=0.1, color=TEXT) for x in (-4.5, -1.5, 1.5, 4.5)])
        self.play(FadeIn(samples), run_time=0.9)
        self.finish()


class S10Evidence(SpokenScene):
    def construct(self):
        vals = [ValueTracker(0.4), ValueTracker(0.55), ValueTracker(0.3)]
        gauges = VGroup(dial(vals[0], [-4.65, 1.15, 0], radius=0.9, label="pressure", color=NUT, size=30),
                        dial(vals[1], [-2.2, 1.15, 0], radius=0.9, label="condition", color=OXY, size=30),
                        dial(vals[2], [0.25, 1.15, 0], radius=0.9, label="habitat", color=HAB, size=30))
        clip = RoundedRectangle(corner_radius=0.16, width=4.3, height=5.4, color=TEXT,
                                fill_color=BG, fill_opacity=0.92).move_to([4.05, 0.15, 0])
        title = T("evidence plan", 34, TEXT, weight=BOLD).move_to([4.05, 2.35, 0])
        self.at("states what evidence")
        self.play(FadeIn(clip), FadeIn(title), run_time=0.9)
        bob(clip, amp=0.09, speed=1.4)
        rows = VGroup(*[T(s, 28, c).move_to([2.85, 1.55 - i * 0.72, 0], aligned_edge=LEFT)
                        for i, (s, c) in enumerate([("pressure", NUT), ("condition", OXY),
                                                   ("habitat", HAB), ("several years", TEXT),
                                                   ("fair comparison", TEXT)])])
        self.at("Measure the pressure")
        self.play(FadeIn(gauges[0]), FadeIn(rows[0]), run_time=0.7)
        self.at("the condition")
        self.play(FadeIn(gauges[1]), FadeIn(rows[1]), run_time=0.7)
        self.at("habitat response")
        self.play(FadeIn(gauges[2]), FadeIn(rows[2]), run_time=0.7)
        self.at("several years")
        year_dots = VGroup(*[Dot([-4.8 + i * 1.05, -1.1, 0], radius=0.13, color=TEXT) for i in range(6)])
        year_line = Line([-4.8, -1.1, 0], [0.45, -1.1, 0], color=GREY, stroke_width=4)
        self.play(Create(year_line), LaggedStart(*[FadeIn(d) for d in year_dots], lag_ratio=0.1), FadeIn(rows[3]), run_time=1.1)
        self.at("comparison fair")
        balance = VGroup(Line([-3.9, -2.2, 0], [-0.6, -2.2, 0], color=TEXT, stroke_width=5),
                         Line([-2.25, -2.2, 0], [-2.25, -2.9, 0], color=TEXT, stroke_width=5),
                         T("fix", 28, GREEN).move_to([-3.5, -2.65, 0]),
                         T("no fix", 28, GREY).move_to([-1.0, -2.65, 0]))
        self.play(FadeIn(balance), FadeIn(rows[4]), run_time=0.9)
        checks = VGroup(*[T("✓", 32, GREEN).move_to([2.48, 1.55 - i * 0.72, 0]) for i in range(4)])
        self.at("report when")
        self.play(LaggedStart(*[FadeIn(c) for c in checks], lag_ratio=0.1), run_time=0.8)
        partial = Rectangle(width=2.9, height=0.42, color=HAB).move_to([4.05, -1.72, 0])
        fill = Rectangle(width=1.55, height=0.3, stroke_width=0, fill_color=HAB, fill_opacity=0.8)
        fill.align_to(partial, LEFT).shift(RIGHT * 0.06).move_to([partial.get_left()[0] + 0.06 + 0.775, -1.72, 0])
        partlab = T("part supported", 28, HAB).move_to([4.05, -2.18, 0])
        self.at("only part")
        self.play(FadeIn(partial), FadeIn(fill), FadeIn(partlab), run_time=0.9)
        self.finish()


class S11Test(SpokenScene):
    def construct(self):
        panels = TwoPanel("fix", "comparison: no fix", colors=(GREEN, GREY), top=2.8, bottom=-2.0)
        # motion=False: the drift/bob updaters pin absolute positions and break once scaled
        left = watershed_world(labels=False, motion=False).scale(0.43)
        right = watershed_world(labels=False, motion=False).scale(0.43)
        panels.put(left, "left")
        panels.put(right, "right")
        self.at("Build the plan")
        self.play(FadeIn(panels), FadeIn(left), run_time=0.9)
        bob(panels, amp=0.12, speed=1.7)
        self.at("measure the results")
        measure = T("measure", 32, OXY, weight=BOLD).move_to([-2.9, -2.65, 0])
        self.play(FadeIn(measure), run_time=0.7)
        self.at("compare them")
        self.play(FadeIn(right), run_time=0.8)
        compare = arrow([-1.4, -2.65, 0], [1.4, -2.65, 0], TEXT)
        self.play(GrowArrow(compare), run_time=0.7)
        loop_words = VGroup(T("build", 28, GREEN).move_to([-4.6, 3.35, 0]),
                            T("measure", 28, OXY).move_to([-1.5, 3.35, 0]),
                            T("compare", 28, TEXT).move_to([1.6, 3.35, 0]),
                            T("refine", 28, HAB).move_to([4.65, 3.35, 0]))
        self.at("results are unclear")
        self.play(FadeIn(loop_words[:3]), run_time=0.8)
        self.at("refine the design")
        self.play(FadeIn(loop_words[3]), run_time=0.7)
        loop = arrow([4.75, 2.92, 0], [-4.75, 2.92, 0], HAB, width=5)
        self.at("test again")
        self.play(Create(loop), run_time=0.9)
        final = watershed_world(labels=True, motion=True)
        self.at("causal chain")
        self.play(FadeOut(VGroup(panels, left, right, measure, compare, loop_words, loop)), FadeIn(final), run_time=1.0)
        small = arrow([-5.5, 2.15, 0], [-3.0, 1.7, 0], NUT, width=7)
        oxygen = ValueTracker(0.42)
        gauge = dial(oxygen, [1.6, 2.35, 0], radius=0.78, label="", color=OXY, size=28)
        gauge_lab = T("oxygen", 28, OXY).move_to([1.6, 3.25, 0])
        bed = grass_bed((4.8, -1.95, 0), n=9)
        goals = T("possible goals", 28, GREY).move_to([4.7, 2.65, 0])
        self.at("where to act")
        self.play(GrowArrow(small), run_time=0.7)
        self.at("Measured criteria")
        self.play(FadeIn(gauge), FadeIn(gauge_lab), oxygen.animate.set_value(0.68), run_time=0.8)
        self.at("whether the plan works")
        self.play(LaggedStart(*[Create(b) for b in bed], lag_ratio=0.06), FadeIn(goals), run_time=0.9)
        self.finish()


class S12End(EndCard):
    LINE = "Effective fixes cut nutrients first, rebuild habitat, and track recovery over time."
