"""Four Ways to Hold Steady — chapter 2.

COLOR MAP (fixed for the whole film)
  GOLD   = condition being protected
  RED    = disturbance
  BLUE   = sensing / active-transport particles
  YELLOW = control centre / advance command
  TEAL   = response
  WHITE  = current state / water vapour / passive particles
  GREY   = carbon dioxide / context

Every recurring world is made by one builder below.  Builders accept a centre and scale so a
world can expand from, and return to, precisely the same panel position.
"""
from bp_parts import *  # noqa: F401,F403


PANEL_CENTRES = {
    "heart": np.array([-3.25, 1.05, 0.0]),
    "leaf": np.array([3.25, 1.05, 0.0]),
    "root": np.array([-3.25, -1.65, 0.0]),
    "cell": np.array([3.25, -1.65, 0.0]),
}


def arrow(a, b, color=GREY, width=5, tip=0.2):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=10)


def protected_badge(text, at, scale=1.0):
    return chip(text, GOLD, size=max(24, int(28 * scale)), pad=0.18).scale(min(1.0, scale)).move_to(at)


def panel_frame(name, centre, color=GREY):
    frame = RoundedRectangle(corner_radius=0.2, width=6.0, height=2.35, color=color,
                             stroke_width=2.5, fill_color=color, fill_opacity=0.10).move_to(centre)
    label = T(name, 28, color).move_to(frame.get_corner(UL) + RIGHT * 0.65 + DOWN * 0.3)
    return VGroup(frame, label)


def heart_shape(color=RED):
    # A familiar organ silhouette, not anatomical detail.
    left = Circle(radius=0.48, color=color, stroke_width=5, fill_color=color, fill_opacity=0.35).shift(LEFT * 0.38)
    right = left.copy().shift(RIGHT * 0.76)
    tip = Polygon([-0.83, 0.05, 0], [0.83, 0.05, 0], [0, -1.05, 0], color=color,
                  stroke_width=5, fill_color=color, fill_opacity=0.35)
    return VGroup(left, right, tip)


def make_heart_world(at=ORIGIN, scale=1.0, compact=False):
    g = VGroup()
    heart = heart_shape().scale(0.72 if compact else 1.15).move_to([0.2, 0.1, 0])
    brain = RoundedRectangle(corner_radius=0.18, width=1.65, height=0.72, color=YELLOW,
                             fill_color=YELLOW, fill_opacity=0.14).move_to([-2.65, 1.65, 0])
    brain_l = T("brain", 28, YELLOW).move_to(brain)
    muscle = RoundedRectangle(corner_radius=0.15, width=2.75, height=0.68, color=BLUE,
                              fill_color=BLUE, fill_opacity=0.12).move_to([-2.65, -1.45, 0])
    muscle_l = T("working muscle", 24, BLUE).move_to(muscle)
    muscle_l.layout_ok = True  # deliberate label inside its own muscle block
    vessel = Line([1.35, -1.45, 0], [3.0, -1.45, 0], color=BLUE, stroke_width=12)
    vessel_l = T("blood vessel", 24, BLUE).next_to(vessel, DOWN, buff=0.16)
    advance = arrow(brain.get_right(), heart.get_left() + UP * 0.25, YELLOW)
    feedback1 = arrow(muscle.get_top(), brain.get_bottom(), BLUE, width=4)
    feedback2 = CurvedArrow(vessel.get_left() + DOWN * 0.05, brain.get_bottom() + RIGHT * 0.5, angle=-TAU / 5, color=BLUE, stroke_width=4)
    flow = arrow(heart.get_right(), [3.05, 0.1, 0], RED, width=8, tip=0.25)
    cells = VGroup(*[Dot([1.35 + i * 0.34, 0.1, 0], radius=0.11, color=RED) for i in range(5)])
    badge = protected_badge("muscle blood flow", [2.25, 1.6, 0])
    g.add(brain, brain_l, muscle, muscle_l, vessel, vessel_l, heart, advance, feedback1, feedback2, flow, cells, badge)
    g.brain, g.heart, g.muscle, g.vessel = brain, heart, muscle, vessel
    g.advance, g.feedback1, g.feedback2, g.flow, g.cells, g.badge = advance, feedback1, feedback2, flow, cells, badge
    g.scale(scale).move_to(at)
    return g


def guard_cell(side, gap=1.0):
    x = side * (0.48 + gap * 0.35)
    c = RoundedRectangle(corner_radius=0.55, width=0.8, height=3.25, color=TEAL, stroke_width=5,
                         fill_color=TEAL, fill_opacity=0.2).move_to([x, 0, 0])
    c.rotate(side * -0.13)
    return c


def make_leaf_world(at=ORIGIN, scale=1.0, narrow=False, arrows=True, particles=True):
    gap = 0.18 if narrow else 1.0
    g = VGroup()
    surface = RoundedRectangle(corner_radius=0.35, width=8.4, height=5.2, color=GREY,
                               stroke_width=3, fill_color=GREEN, fill_opacity=0.16)
    gl, gr = guard_cell(-1, gap), guard_cell(1, gap)
    dry = VGroup(*[Arc(radius=0.32 + 0.08 * i, start_angle=0, angle=PI, color=RED,
                       stroke_width=4).move_to([-2.8 + i * 1.4, 2.05, 0]) for i in range(5)])
    dry_l = T("dry air", 28, RED).move_to([-4.9, 2.05, 0])
    water = VGroup(*[Dot([(-0.4 + 0.4 * (i % 3)), -1.9 + 0.38 * i, 0], radius=0.09, color=WHITE)
                     for i in range(7)])
    co2 = VGroup(*[Dot([(0.45 - 0.45 * (i % 3)), 2.0 - 0.33 * i, 0], radius=0.09, color=GREY)
                   for i in range(7)])
    water_a = arrow([-0.55, -1.7, 0], [-0.55, 1.8, 0], WHITE, width=7, tip=0.25)
    co2_a = arrow([0.55, 1.8, 0], [0.55, -1.7, 0], GREY, width=7, tip=0.25)
    badge = protected_badge("water in leaf", [2.70, -1.98, 0])
    g.add(surface, dry, dry_l, gl, gr)
    if particles:
        g.add(water, co2)
    if arrows:
        g.add(water_a, co2_a)
    g.add(badge)
    g.surface, g.left_guard, g.right_guard = surface, gl, gr
    g.water, g.co2, g.water_arrow, g.co2_arrow, g.badge = water, co2, water_a, co2_a, badge
    g.scale(scale).move_to(at)
    return g


def make_root_world(at=ORIGIN, scale=1.0, curved=True):
    g = VGroup()
    soil = Rectangle(width=11.5, height=5.3, stroke_color=GREY, stroke_width=3,
                     fill_color="#7A5630", fill_opacity=0.38)
    wet = Rectangle(width=4.8, height=5.3, stroke_width=0, fill_color=BLUE, fill_opacity=0.30).align_to(soil, RIGHT)
    dry_l = T("drier", 28, RED).move_to([-4.3, 2.15, 0])
    wet_l = T("wetter", 28, BLUE).move_to([4.5, 2.15, 0])
    grad = arrow([-3.0, 1.55, 0], [3.1, 1.55, 0], BLUE, width=6)
    grad_l = T("water gradient", 28, BLUE).move_to([1.2, 2.05, 0])
    grad_l.layout_ok = True  # deliberately labels its adjacent gradient arrow
    if curved:
        pts = [[-1.0, 2.4, 0], [-1.0, 1.2, 0], [-0.8, 0.0, 0], [0.0, -1.15, 0], [1.8, -2.25, 0]]
    else:
        pts = [[-1.0, 2.4, 0], [-1.0, 1.1, 0], [-1.0, -0.2, 0], [-1.0, -1.5, 0], [-1.0, -2.25, 0]]
    root = VMobject(color=TEAL, stroke_width=14).set_points_smoothly(pts)
    trace = DashedVMobject(root.copy().set_stroke(GREY, width=4, opacity=0.6), num_dashes=18)
    badge = protected_badge("water supply", [4.15, -2.0, 0])
    g.add(soil, wet, dry_l, wet_l, grad, grad_l, trace, root, badge)
    g.soil, g.wet, g.root, g.trace, g.badge = soil, wet, root, trace, badge
    g.scale(scale).move_to(at)
    return g


def make_membrane_world(at=ORIGIN, scale=1.0):
    g = VGroup()
    outside_bg = Rectangle(width=10.5, height=2.35, stroke_width=0, fill_color=BLUE,
                           fill_opacity=0.10).move_to([0, 1.55, 0])
    inside_bg = Rectangle(width=10.5, height=2.35, stroke_width=0, fill_color=GOLD,
                          fill_opacity=0.10).move_to([0, -1.55, 0])
    outside = T("outside", 28, GREY).move_to([0, 2.6, 0])
    inside = T("inside", 28, GOLD).move_to([0, -2.6, 0])
    membrane = RoundedRectangle(corner_radius=0.18, width=10.5, height=0.7, color=TEAL,
                                stroke_width=5, fill_color=TEAL, fill_opacity=0.16)
    gate = RoundedRectangle(corner_radius=0.12, width=1.25, height=1.3, color=WHITE,
                            fill_color=BG, fill_opacity=1).move_to([-2.4, 0, 0])
    pump = RoundedRectangle(corner_radius=0.18, width=1.9, height=1.55, color=TEAL,
                            fill_color=TEAL, fill_opacity=0.2).move_to([2.52, 0, 0])
    pump_l = T("pump", 26, TEAL).move_to(pump).shift(RIGHT * 0.28)
    white = VGroup(*[Dot([-3.25 + 0.5 * (i % 4), 2.0 - 0.42 * (i // 4), 0], radius=0.11, color=WHITE)
                     for i in range(12)])
    few = VGroup(*[Dot([-2.85 + 0.55 * i, -1.7, 0], radius=0.11, color=WHITE) for i in range(3)])
    blue = VGroup(*[Dot([1.45 + 0.45 * i, 1.7, 0], radius=0.11, color=BLUE) for i in range(3)])
    crowd = VGroup(*[Dot([1.2 + 0.48 * (i % 6), -1.5 - 0.35 * (i // 6), 0], radius=0.11, color=BLUE)
                      for i in range(12)])
    passive = arrow([-2.4, 1.5, 0], [-2.4, -1.3, 0], WHITE, width=6)
    active = arrow([1.85, 1.35, 0], [1.85, -1.3, 0], BLUE, width=6)
    energy = chip("energy", GREY, 24, pad=0.15).move_to([4.25, 0.8, 0])
    badge = protected_badge("inside stays different", [4.0, -2.25, 0])
    g.add(outside_bg, inside_bg, outside, inside, membrane, gate, pump, pump_l, white, few, blue, crowd,
          passive, active, energy, badge)
    g.membrane, g.gate, g.pump = membrane, gate, pump
    g.white, g.few, g.blue, g.crowd = white, few, blue, crowd
    g.passive, g.active, g.energy, g.badge = passive, active, energy, badge
    g.scale(scale).move_to(at)
    return g


def make_four_worlds(with_frames=True):
    """Four readable overview panels: icon silhouettes, never scaled-down labels."""
    groups = VGroup()
    if with_frames:
        groups.add(panel_frame("heart", PANEL_CENTRES["heart"]), panel_frame("leaf", PANEL_CENTRES["leaf"]),
                   panel_frame("root", PANEL_CENTRES["root"]), panel_frame("cell", PANEL_CENTRES["cell"]))
    # Attributes mirror the full builders so later scenes can highlight the same actions.
    hc = PANEL_CENTRES["heart"] + DOWN * 0.2
    heart_shape_m = heart_shape().scale(0.42).move_to(hc)
    advance = arrow(hc + LEFT * 1.9 + UP * 0.55, hc + LEFT * 0.55 + UP * 0.25, YELLOW, width=4)
    feedback = arrow(hc + LEFT * 0.55 + DOWN * 0.65, hc + LEFT * 1.9 + DOWN * 0.2, BLUE, width=4)
    flow = arrow(hc + RIGHT * 0.55, hc + RIGHT * 1.9, RED, width=6)
    hb = Circle(radius=0.16, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to(hc + RIGHT * 2.25 + UP * 0.65)
    heart = VGroup(heart_shape_m, advance, feedback, flow, hb)
    heart.heart, heart.advance, heart.feedback1, heart.feedback2 = heart_shape_m, advance, feedback, feedback
    heart.flow, heart.badge = flow, hb

    lc = PANEL_CENTRES["leaf"] + DOWN * 0.2
    lg, rg = guard_cell(-1, 0.18).scale(0.42), guard_cell(1, 0.18).scale(0.42)
    lg.move_to(lc + LEFT * 0.3), rg.move_to(lc + RIGHT * 0.3)
    wa = arrow(lc + DOWN * 0.8, lc + UP * 0.8, WHITE, width=4)
    ca = arrow(lc + RIGHT * 0.65 + UP * 0.8, lc + RIGHT * 0.65 + DOWN * 0.8, GREY, width=4)
    lb = Circle(radius=0.16, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to(lc + RIGHT * 2.25 + UP * 0.65)
    leaf = VGroup(lg, rg, wa, ca, lb)
    leaf.left_guard, leaf.right_guard, leaf.water_arrow, leaf.co2_arrow, leaf.badge = lg, rg, wa, ca, lb

    rc = PANEL_CENTRES["root"] + DOWN * 0.15
    root_line = VMobject(color=TEAL, stroke_width=10).set_points_smoothly(
        [rc + UP * 0.85 + LEFT * 0.6, rc + UP * 0.2 + LEFT * 0.55, rc + DOWN * 0.35, rc + DOWN * 0.8 + RIGHT * 1.1])
    water = Rectangle(width=2.4, height=1.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.18).move_to(rc + RIGHT * 1.65)
    rb = Circle(radius=0.16, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to(rc + RIGHT * 2.25 + UP * 0.65)
    root = VGroup(water, root_line, rb)
    root.root, root.badge = root_line, rb

    cc = PANEL_CENTRES["cell"] + DOWN * 0.15
    membrane = Line(cc + LEFT * 2.1, cc + RIGHT * 2.1, color=TEAL, stroke_width=12)
    gate = RoundedRectangle(corner_radius=0.1, width=0.65, height=0.85, color=WHITE, fill_color=BG, fill_opacity=1).move_to(cc + LEFT)
    pump = RoundedRectangle(corner_radius=0.12, width=0.8, height=0.95, color=TEAL, fill_color=TEAL, fill_opacity=0.2).move_to(cc + RIGHT)
    dots = VGroup(*[Dot(cc + [-1.8 + 0.45 * i, 0.65 if i < 5 else -0.65, 0], radius=0.07,
                            color=WHITE if i < 5 else BLUE) for i in range(10)])
    cb = Circle(radius=0.16, color=GOLD, fill_color=GOLD, fill_opacity=1).move_to(cc + RIGHT * 2.25 + UP * 0.65)
    cell = VGroup(membrane, gate, pump, dots, cb)
    cell.membrane, cell.gate, cell.pump, cell.white, cell.badge = membrane, gate, pump, dots, cb
    groups.add(heart, leaf, root, cell)
    groups.heart, groups.leaf, groups.root, groups.cell = heart, leaf, root, cell
    return groups


def add_soft_motion(*mobs):
    for i, mob in enumerate(mobs):
        # Large enough to survive the film linter's 320-pixel freeze detector, still visually gentle.
        bob(mob, amp=0.10 + 0.02 * (i % 3), speed=1.8 + 0.2 * i, seed=i)


def add_equal_leaf_flows(w, speed=0.34):
    """Loop both particle streams through the narrow pore at the same visible speed."""
    low = w.surface.get_bottom()[1] + 0.42
    high = w.surface.get_top()[1] - 0.42
    span = high - low
    centre_x = w.surface.get_center()[0]

    for particles, direction, lane_x in ((w.water, 1, centre_x - 0.12),
                                         (w.co2, -1, centre_x + 0.12)):
        particles.clear_updaters()  # drop any group bob: it re-centres the stream and jerks it at each wrap
        for i, dot in enumerate(particles):
            dot.move_to([lane_x, low + span * (i + 0.5) / len(particles), 0])

            def travel(mob, dt, direction=direction, low=low, high=high, span=span):
                mob.shift(UP * direction * speed * dt)
                if direction > 0 and mob.get_y() > high:
                    mob.shift(DOWN * span)
                elif direction < 0 and mob.get_y() < low:
                    mob.shift(UP * span)

            dot.add_updater(travel)


def add_flow_arrow_motion(w, amp=0.34, speed=1.0):
    """Move both long arrows along their flow directions without implying unequal rates."""
    for flow_arrow, direction in ((w.water_arrow, 1), (w.co2_arrow, -1)):
        flow_arrow._flow_t = 0.0
        base = flow_arrow.get_center().copy()

        def travel(mob, dt, direction=direction, base=base):
            mob._flow_t += dt
            mob.move_to(base + UP * direction * amp * np.sin(speed * mob._flow_t))

        flow_arrow.add_updater(travel)


def add_leaf_sway(w, amp=0.30, speed=1.7):
    """Sway the close leaf view while its two equal particle streams continue crossing."""
    w._sway_t = 0.0
    base = w.get_center().copy()

    def sway(mob, dt):
        mob._sway_t += dt
        mob.move_to(base + RIGHT * amp * np.sin(speed * mob._sway_t))

    w.add_updater(sway)


def rock_balance_bar(bar, centre):
    """Keep the tradeoff visibly unresolved instead of settling on either side."""
    bar._rock_t = 0.0
    bar._rock_angle = 0.12

    def rock(mob, dt):
        mob._rock_t += dt
        angle = 0.15 * np.sin(1.35 * mob._rock_t + 0.9)
        mob.rotate(angle - mob._rock_angle, about_point=centre)
        mob._rock_angle = angle

    bar.add_updater(rock)


class S00LinkAndQuestion(TitleCard, SpokenScene):
    LESSON = "Homeostasis in Action"
    TITLE = "Four Ways to Hold Steady"

    def construct(self):
        # It is the required opening TitleCard class, but the spoken hook carries chapter one's world forward.
        loop = VGroup(*[chip(t, c, 28) for t, c in (("warming", RED), ("sensor", BLUE),
                                                     ("control", YELLOW), ("response", TEAL))])
        loop.arrange(RIGHT, buff=0.5)
        links = VGroup(*[arrow(loop[i].get_right(), loop[i + 1].get_left(),
                                    [BLUE, YELLOW, TEAL][i], width=4) for i in range(3)])
        badge = protected_badge("body temperature", [0, -1.4, 0])
        scope = scope_tag("schematic")
        self.play(FadeIn(loop), LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.2), FadeIn(badge), run_time=2.2)
        self.at("Do hearts")
        q = fit_text("Do hearts, leaves, roots, and cells use the same loop?", max_w=11.8,
                     size=38, color=TEXT).move_to([0, 3.25, 0])
        worlds = make_four_worlds()
        worlds.scale(0.88).shift(DOWN * 0.22)
        self.play(FadeOut(loop), FadeOut(links), FadeOut(badge), FadeIn(worlds), FadeIn(q), run_time=2.6)
        add_soft_motion(worlds.heart.heart, worlds.leaf.left_guard, worlds.root.root, worlds.cell.white)
        self.at("Keep the same colors")
        self.play(Indicate(worlds.heart.advance, color=YELLOW), Indicate(worlds.leaf.left_guard, color=TEAL), run_time=1.2)
        self.at("A gold badge")
        self.play(LaggedStart(*[Indicate(w.badge, color=GOLD) for w in
                                (worlds.heart, worlds.leaf, worlds.root, worlds.cell)], lag_ratio=0.2), run_time=1.8)
        self.add(scope)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        worlds = make_four_worlds()
        worlds.scale(0.88).shift(DOWN * 0.22)
        add_soft_motion(worlds.heart.heart, worlds.leaf.left_guard, worlds.root.root, worlds.cell.white)
        title = T("Four Ways to Hold Steady", 50, font=TITLE_FONT).move_to([0, 3.25, 0])
        rule = Line([-2.0, 2.82, 0], [2.0, 2.82, 0], color=GOLD, stroke_width=4)
        self.add(worlds)
        self.play(FadeIn(title), GrowFromCenter(rule), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(title), FadeOut(rule), run_time=0.5)
        self.finish()


class S02Heart(SpokenScene):
    def construct(self):
        w = make_heart_world(DOWN * 0.1, 1.0)
        # Show the actors before naming the routes.
        hidden = VGroup(w.advance, w.feedback1, w.feedback2, w.flow, w.cells, w.badge)
        self.add(*[m for m in w if m not in hidden])
        pulse(w.heart[0], base=5, amp=1.5, speed=3)
        add_soft_motion(w.heart, w.cells)
        self.at("Commands from")
        self.play(GrowArrow(w.advance), Indicate(w.heart, color=RED), run_time=1.5)
        advance_l = T("advance command", 28, YELLOW).move_to([-1.35, 2.65, 0])
        self.play(FadeIn(advance_l), run_time=0.45)
        self.at("Sensors in")
        self.play(GrowArrow(w.feedback1), Create(w.feedback2), run_time=1.5)
        feedback_l = T("feedback", 28, BLUE).move_to([-3.9, 0.15, 0])
        self.play(FadeIn(feedback_l), run_time=0.45)
        self.at("The faster heart")
        self.play(w.heart.animate.scale(1.14), GrowArrow(w.flow), FadeIn(w.cells), FadeIn(w.badge), run_time=1.6)
        self.at("Exercise control combines")
        self.play(Indicate(w.advance, color=YELLOW), Indicate(VGroup(w.feedback1, w.feedback2), color=BLUE), run_time=1.8)
        self.finish()


class S03Leaf(SpokenScene):
    def construct(self):
        w = make_leaf_world(DOWN * 0.05, 1.0, narrow=False)
        add_soft_motion(w.left_guard, w.right_guard, w.water, w.co2)
        self.add(w.surface)
        self.at("gold range")
        self.play(FadeIn(w.badge), FadeIn(w.left_guard), FadeIn(w.right_guard), run_time=1.1)
        self.at("Dry air")
        self.play(FadeIn(w[1]), FadeIn(w[2]), FadeIn(w.water), GrowArrow(w.water_arrow), run_time=1.6)
        pores = T("stoma: a small pore", 28, TEXT).move_to([-3.9, -3.0, 0])
        pores.layout_ok = True  # label intentionally sits on the leaf surface
        self.at("leaf's small pores")
        self.play(FadeIn(pores), run_time=0.6)
        self.at("Guard cells")
        nl, nr = guard_cell(-1, 0.18).move_to(w.left_guard), guard_cell(1, 0.18).move_to(w.right_guard)
        self.play(Transform(w.left_guard, nl), Transform(w.right_guard, nr), run_time=1.4)
        self.at("But the pore")
        self.play(FadeIn(w.co2), GrowArrow(w.co2_arrow), run_time=1.3)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        w = make_leaf_world(UP * 0.2, 0.88, narrow=True)
        # Equal arrow widths are intentional for the unanswered prediction.
        add_equal_leaf_flows(w)
        add_flow_arrow_motion(w)
        add_leaf_sway(w)
        self.add(w, scope_tag("schematic"))
        self.at("Predict what happens")
        q = question_card("Narrow pore: one flow or both?", y=-3.15, size=32)
        self.play(FadeIn(q), run_time=0.8)
        self.at("Does only water")
        self.play(Indicate(w.water_arrow, color=WHITE), run_time=0.9)
        self.at("or do both")
        self.play(Indicate(w.co2_arrow, color=GREY), run_time=0.9)
        self.at("Watch the two arrows")
        self.play(Indicate(VGroup(w.water_arrow, w.co2_arrow), scale_factor=1.04), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Narrow pore: one flow or both?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 32}

    def backdrop(self):
        w = make_leaf_world(UP * 0.2, 0.88, narrow=True)
        add_soft_motion(w.water, w.co2)
        return w


class S06LeafReveal(SpokenScene):
    def construct(self):
        w = make_leaf_world(UP * 0.15, 0.84, narrow=True)
        add_soft_motion(w.left_guard, w.right_guard, w.water, w.co2)
        q = question_card("Narrow pore: one flow or both?", y=-3.15, size=32)
        self.add(w, q)
        self.at("Both movements slow")
        thin_w = w.water_arrow.copy().set_stroke(width=3)
        thin_c = w.co2_arrow.copy().set_stroke(width=3)
        trade = T("tradeoff", 40, GOLD).move_to([0, 3.25, 0])
        self.play(Transform(w.water_arrow, thin_w), Transform(w.co2_arrow, thin_c), swap(q, trade), run_time=1.3)
        add_equal_leaf_flows(w, speed=0.17)
        add_flow_arrow_motion(w, amp=0.28, speed=0.55)
        self.at("Fewer water")
        self.play(LaggedStart(*[w.water[i].animate.shift(UP * 0.65) for i in range(0, len(w.water), 3)], lag_ratio=0.25),
                  run_time=1.6)
        left = chip("slower water loss", WHITE, 27).move_to([-3.0, -2.55, 0])
        self.play(FadeIn(left), run_time=0.5)
        self.at("Fewer carbon")
        self.play(LaggedStart(*[w.co2[i].animate.shift(DOWN * 0.65) for i in range(0, len(w.co2), 3)], lag_ratio=0.25),
                  run_time=1.6)
        right = chip("less carbon dioxide", GREY, 27).move_to([3.0, -2.55, 0])
        self.play(FadeIn(right), run_time=0.5)
        self.at("One response")
        # Below the leaf panel, between the two chips. Create and Rotate are separate plays: in one play
        # Rotate started from Create's zero-length bar and the bar never showed.
        bar = Line([-0.95, -2.45, 0], [0.95, -2.45, 0], color=GOLD, stroke_width=7)
        pivot = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1).scale(0.2).move_to([0, -2.72, 0])
        self.play(Create(bar), FadeIn(pivot), run_time=0.8)
        self.play(Rotate(bar, 0.12, about_point=[0, -2.45, 0]), run_time=0.7)
        rock_balance_bar(bar, np.array([0, -2.45, 0]))
        self.finish()


class S07Root(SpokenScene):
    def construct(self):
        straight = make_root_world(DOWN * 0.1, 1.0, curved=False)
        curved = make_root_world(DOWN * 0.1, 1.0, curved=True)
        self.add(straight.soil, straight.wet)
        self.at("water is uneven")
        self.play(FadeIn(straight[2]), FadeIn(straight[3]), GrowArrow(straight[4]), FadeIn(straight[5]), run_time=1.5)
        self.at("root can curve")
        self.play(Create(straight.root), run_time=1.0)
        pulse(straight.root, base=14, amp=3.5, speed=2.4)
        self.play(Transform(straight.root, curved.root), FadeIn(curved.trace), run_time=2.0)
        self.at("This is hydrotropism")
        label = T("hydrotropism", 36, TEAL).move_to([0, -3.05, 0])
        self.play(FadeIn(label), FadeIn(curved.badge), run_time=0.8)
        self.at("It supports water")
        self.play(Indicate(curved.badge, color=GOLD), run_time=1.0)
        self.at("but biologists")
        ghosts = VGroup(chip("sensor?", BLUE, 27), chip("control centre?", YELLOW, 27)).arrange(RIGHT, buff=0.45).move_to([0, 3.1, 0])
        self.play(FadeIn(ghosts), run_time=0.7)
        response = scope_tag("response — not a complete loop", size=24, color=TEAL)
        self.at("not a complete")
        self.play(FadeOut(ghosts, shift=UP * 0.2), FadeIn(response), run_time=1.0)
        self.finish()


class S08Membrane(SpokenScene):
    def construct(self):
        w = make_membrane_world(DOWN * 0.05, 1.0)
        add_soft_motion(w.white, w.blue, w.crowd)
        self.add(w[0], w[1], w[2], w[3])
        self.at("selectively permeable")
        self.play(Create(w.membrane), FadeIn(w.gate), FadeIn(w.pump), FadeIn(w[7]), run_time=1.5)
        self.play(FadeIn(w.white), FadeIn(w.blue), run_time=0.8)
        self.at("Passive transport")
        passive_l = T("passive", 30, WHITE).move_to([-4.1, -0.95, 0])
        self.play(GrowArrow(w.passive), w.white.animate.shift(DOWN * 0.7), FadeIn(w.few), FadeIn(passive_l), run_time=2.2)
        self.at("Active transport")
        active_l = T("active", 30, TEAL).move_to([2.65, -1.05, 0])
        self.play(FadeIn(w.energy), GrowArrow(w.active), FadeIn(active_l), run_time=1.2)
        self.play(w.blue.animate.shift(DOWN * 1.0), FadeIn(w.crowd), run_time=1.5)
        self.at("Together")
        self.play(FadeIn(w.badge), Indicate(VGroup(w.gate, w.pump), color=TEAL), run_time=1.4)
        self.finish()


class S09GuidingRule(SpokenScene):
    def construct(self):
        worlds = make_four_worlds()
        worlds.scale(0.9).shift(DOWN * 0.18)
        self.add(worlds)
        add_soft_motion(worlds.heart.heart, worlds.leaf.left_guard, worlds.root.root, worlds.cell.white)
        heading = T("same goal · different routes", 42, GOLD).move_to([0, 3.35, 0])
        self.at("different route")
        self.play(FadeIn(heading), run_time=0.8)
        self.at("heart changes")
        self.play(Indicate(worlds.heart.flow, color=TEAL), run_time=0.9)
        self.at("guard cells")
        self.play(Indicate(VGroup(worlds.leaf.left_guard, worlds.leaf.right_guard), color=TEAL), run_time=0.9)
        self.at("membranes control")
        self.play(Indicate(VGroup(worlds.cell.gate, worlds.cell.pump), color=TEAL), run_time=0.9)
        self.at("Roots support")
        self.play(Indicate(worlds.root.root, color=TEAL), run_time=1.0)
        self.finish()


def temperature_loop(at=ORIGIN, scale=1.0):
    labels = [("warming", RED), ("sensor", BLUE), ("control centre", YELLOW), ("effector", TEAL)]
    nodes = VGroup(*[chip(t, c, 26) for t, c in labels]).arrange(RIGHT, buff=0.3)
    links = VGroup(*[arrow(nodes[i].get_right(), nodes[i + 1].get_left(), labels[i + 1][1], width=4)
                     for i in range(3)])
    g = VGroup(nodes, links).scale(scale).move_to(at)
    g.nodes, g.links = nodes, links
    return g


class S10Scope(SpokenScene):
    def construct(self):
        loop = temperature_loop([0, 1.15, 0], 0.95)
        add_soft_motion(*loop.nodes)
        self.add(loop)
        equality = T("=", 64, TEXT).move_to([0, -0.05, 0])
        routes = fit_text("same goal, different routes", max_w=8.5, size=40, color=GOLD).move_to([0, -0.15, 0])
        self.at("diagrams are not identical")
        self.play(FadeIn(equality), run_time=0.45)
        self.play(swap(equality, routes, run_time=0.9), run_time=0.9)
        self.at("Body temperature")
        self.play(LaggedStart(*[Indicate(n, color=c) for n, c in zip(loop.nodes[1:], [BLUE, YELLOW, TEAL])], lag_ratio=0.2), run_time=1.4)
        heart = chip("exercise: advance + feedback", YELLOW, 28).move_to([-3.65, -1.25, 0])
        root = chip("root: environmental response", TEAL, 28).move_to([3.65, -1.25, 0])
        membrane = chip("membrane: gates + energy", TEAL, 28).move_to([0, -2.45, 0])
        self.at("Exercise adds")
        self.play(FadeIn(heart), run_time=0.8)
        self.at("Hydrotropism")
        self.play(FadeIn(root), run_time=0.8)
        self.at("A membrane")
        self.play(FadeIn(membrane), run_time=0.8)
        self.finish()


def recovery_curve():
    # Schematic only: an exponential return, clearly marked as a preview rather than data.
    p = Plot(box=(0.1, 5.95, -2.05, 2.15), xr=(0, 6), yr=(0, 1.05),
             xticks=[0, 3, 6], yticks=[],
             xlabel="time", ylabel="heart rate", label_size=26)
    fn = lambda t: 0.2 + 0.8 * np.exp(-0.62 * t)
    return p, fn


class S11Handoff(SpokenScene):
    def construct(self):
        # A purpose-built stack keeps every label readable; the full overview is never miniaturised.
        names = VGroup(*[chip(n, c, 24, pad=0.14) for n, c in
                         (("heart", RED), ("leaf", TEAL), ("root", TEAL), ("cell", BLUE))])
        names.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-5.15, 0.2, 0])
        markers = VGroup(*[Circle(radius=0.13, color=GOLD, fill_color=GOLD, fill_opacity=1)
                           .next_to(n, RIGHT, buff=0.18) for n in names])
        worlds = VGroup(names, markers)
        self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.12) for n in names], lag_ratio=0.15),
                  FadeIn(markers), run_time=0.8)
        self.at("heart's two nerves")
        tags = VGroup(chip("two nerves", YELLOW, 26), chip("temperature", RED, 26), chip("growth", TEAL, 26))
        tags.arrange(DOWN, buff=0.25).move_to([-2.0, 0, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in tags], lag_ratio=0.25), run_time=1.5)
        p, fn = recovery_curve()
        p.shift(RIGHT * 0.25)
        t = ValueTracker(0)
        live = p.live_curve(fn, t, color=WHITE, width=7)
        dot = p.dot(lambda: t.get_value(), lambda: fn(t.get_value()), color=WHITE, ring=GOLD)
        band = p.hline(0.2, color=GOLD)
        self.at("Then real heart")
        self.play(Create(p), FadeIn(band), run_time=1.0)
        self.add(live, dot)
        self.play(t.animate.set_value(6), run_time=3.2, rate_func=linear)
        next_l = T("real data next", 30, GOLD).move_to([3.2, 2.8, 0])
        self.play(FadeIn(next_l), run_time=0.5)
        self.add(scope_tag("schematic preview"))
        self.finish()


class S12End(EndCard):
    LINE = "Same goal, different routes: only some are complete feedback loops."
