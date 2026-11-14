"""What Let the Eagles Return? — animated explainer.

COLOR MAP
  GOLD   eagles, nests, eggs, and measured eagle counts
  RED    harms: DDT/DDE, thin shells, habitat loss, new dangers
  TEAL   protective actions and barriers
  GREEN  forest habitat and ecological recovery
  BLUE   water
  GREY   survey boundaries, timelines, and cautions
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403


SURVEY = [(1977, 33), (2003, 435), (2004, 428), (2005, 453),
          (2007, 560), (2008, 584), (2010, 684), (2011, 726), (2016, 1070)]


def nest_marker(scale=1.0):
    """A simple map pin/nest symbol, not a literal eagle drawing."""
    bowl = Arc(radius=0.18, start_angle=PI, angle=PI, color=GOLD, stroke_width=5)
    egg = Ellipse(width=0.13, height=0.19, color=GOLD, stroke_width=3,
                  fill_color=GOLD, fill_opacity=0.45).shift(UP * 0.08)
    return VGroup(bowl, egg).scale(scale)


def eagle_icon(scale=1.0):
    """A readable gold bird silhouette made from two wings and a body."""
    wings = VGroup(
        ArcBetweenPoints(LEFT * 0.7, ORIGIN, angle=-0.8, color=GOLD, stroke_width=7),
        ArcBetweenPoints(ORIGIN, RIGHT * 0.7, angle=-0.8, color=GOLD, stroke_width=7),
    )
    body = Line(ORIGIN + UP * 0.06, DOWN * 0.38, color=GOLD, stroke_width=7)
    return VGroup(wings, body).scale(scale)


def shoreline_world(nests=4, wide_search=False, forest=1.0):
    """The carried world. Every shoreline scene calls this exact builder."""
    water = Polygon([-6.2, -2.55, 0], [6.2, -2.55, 0], [6.2, 0.85, 0],
                    [4.7, 0.55, 0], [3.5, 1.15, 0], [2.0, 0.45, 0],
                    [0.5, 1.0, 0], [-1.0, 0.35, 0], [-2.6, 0.9, 0],
                    [-4.1, 0.35, 0], [-6.2, 0.75, 0],
                    stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18)
    forest_band = Polygon([-6.2, 0.75, 0], [-4.1, 0.35, 0], [-2.6, 0.9, 0],
                          [-1.0, 0.35, 0], [0.5, 1.0, 0], [2.0, 0.45, 0],
                          [3.5, 1.15, 0], [4.7, 0.55, 0], [6.2, 0.85, 0],
                          [6.2, 2.5, 0], [-6.2, 2.5, 0],
                          stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                          fill_opacity=0.10 * forest)
    tree_x = np.linspace(-5.7, 5.7, max(3, int(13 * forest)))
    trees = VGroup(*[
        VGroup(Line([x, 1.05 + 0.12 * np.sin(x), 0], [x, 1.48 + 0.12 * np.sin(x), 0],
                    color=GREEN, stroke_width=4),
               Circle(radius=0.20, color=GREEN, fill_color=GREEN, fill_opacity=0.35)
               .move_to([x, 1.62 + 0.12 * np.sin(x), 0]))
        for x in tree_x
    ])
    small = [(-4.7, 1.95), (-1.8, 1.6), (2.0, 1.8), (4.5, 1.75)]
    many = [(-5.4, 1.55), (-4.7, 2.05), (-3.9, 1.45), (-3.0, 2.1), (-2.0, 1.5),
            (-0.9, 2.05), (0.2, 1.55), (1.3, 2.15), (2.3, 1.55), (3.3, 2.1),
            (4.4, 1.55), (5.3, 2.0)]
    pts = many[:nests] if nests > 4 else small[:nests]
    marks = VGroup(*[nest_marker(0.9).move_to([x, y, 0]) for x, y in pts])
    boundary = RoundedRectangle(corner_radius=0.25, width=11.8 if wide_search else 4.8,
                                height=4.45, color=GREY, stroke_width=3)
    boundary.set_stroke(opacity=0.75).move_to([0 if wide_search else -3.4, 0.05, 0])
    boundary = DashedVMobject(boundary, num_dashes=42 if wide_search else 22)
    world = VGroup(water, forest_band, trees, marks, boundary)
    world.water, world.forest, world.trees, world.nests, world.boundary = water, forest_band, trees, marks, boundary
    return world


def moving_water(world, speed=1.0):
    """A visible but gentle shimmer across the carried blue water."""
    wave = VMobject(color=BLUE, stroke_width=5)
    wave.phase = 0.0
    def update(m, dt):
        m.phase += dt * speed
        pts = [[x, -1.15 + 0.09 * np.sin(1.7 * x + m.phase), 0] for x in np.linspace(-5.7, 5.7, 70)]
        m.set_points_smoothly(pts)
    wave.add_updater(update)
    return wave


def timeline(cursor=None):
    line = Line([-5.5, -2.75, 0], [5.5, -2.75, 0], color=GREY, stroke_width=5)
    ticks = VGroup(*[Line([x, -2.9, 0], [x, -2.6, 0], color=GREY, stroke_width=3)
                     for x in np.linspace(-5.0, 5.0, 7)])
    g = VGroup(line, ticks)
    if cursor is not None:
        dot = always_redraw(lambda: Dot([cursor.get_value(), -2.75, 0], radius=0.14, color=TEAL))
        g.add(dot)
    return g


def allow_component_internals(mob):
    """Approve deliberate crossings inside a standard component (dial/chip)."""
    for part in mob.family_members_with_points():
        part.layout_ok = True
    return mob


def protection_world():
    world = shoreline_world(nests=1, wide_search=True, forest=1.0)
    barrier = RoundedRectangle(corner_radius=0.25, width=12.25, height=4.75,
                               color=TEAL, stroke_width=7).move_to([0, 0.05, 0])
    return VGroup(world, barrier)


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Restoring Ecosystems"
    TITLE = "What Let the Eagles Return?"

    def construct(self):
        title = T(self.TITLE, 48, font=TITLE_FONT).move_to([0, 3.25, 0])
        world = shoreline_world(nests=3, wide_search=False)
        wave = moving_water(world)
        self.play(Write(title), FadeIn(world.water), run_time=0.9)
        self.add(wave)
        self.at("one survey map")
        self.play(FadeIn(world.forest), FadeIn(world.trees), Create(world.boundary),
                  FadeIn(world.nests, lag_ratio=0.18), run_time=1.8)
        early = M("1977: 33 pairs", 32, GOLD).move_to([-3.7, -1.8, 0])
        self.play(FadeIn(early), run_time=0.5)
        later_world = shoreline_world(nests=12, wide_search=True)
        self.at("a later larger search")
        self.play(Transform(world.boundary, later_world.boundary),
                  Transform(world.nests, later_world.nests), run_time=2.4)
        later = M("2016: 1,070 pairs", 34, GOLD).move_to([3.2, -1.7, 0])
        larger = T("larger search", 28, GREY).move_to([3.2, -0.55, 0])
        self.play(FadeIn(later), FadeIn(larger), run_time=0.7)
        self.at("not identical")
        caution = caption("The searches were not identical.", 30, GREY)
        self.play(FadeOut(early), FadeOut(later), FadeOut(larger), FadeIn(caution), run_time=0.7)
        self.add(scope_tag("schematic map"))
        self.at("what changed")
        self.play(Indicate(world.nests, color=GOLD, scale_factor=1.08), run_time=1.2)
        self.finish()


class S02Harm(SpokenScene):
    def construct(self):
        world = shoreline_world(nests=1, wide_search=True)
        world.scale(0.42).move_to([-4.6, 2.5, 0])
        pressure_ring = DashedVMobject(Circle(radius=1.65, color=RED, stroke_width=8), num_dashes=18)
        pressure_ring.move_to([3.2, 0.0, 0])
        pressure_ring.add_updater(lambda m, dt: m.rotate(0.75 * dt))
        self.add(world, pressure_ring, scope_tag("schematic"))
        intro_egg = Ellipse(width=2.4, height=3.2, color=GOLD, stroke_width=16,
                            fill_color=GOLD, fill_opacity=0.08).move_to([3.2, 0.0, 0])
        self.play(FadeIn(intro_egg, scale=0.82), run_time=1.1)
        ddt = chip("DDT", RED, 36).move_to([-4.7, 0.65, 0])
        self.at("DDT was")
        self.play(FadeIn(ddt, shift=RIGHT * 0.2), run_time=0.7)
        dde = chip("DDE", RED, 36).move_to([-1.8, 0.65, 0])
        arrow = Arrow(ddt.get_right(), dde.get_left(), buff=0.15, color=RED, stroke_width=6)
        self.at("breaks down")
        self.play(GrowArrow(arrow), TransformFromCopy(ddt, dde), run_time=1.0)
        egg = intro_egg
        self.at("bird egg shells")
        self.play(Indicate(egg, color=GOLD, scale_factor=1.04),
                  dde.animate.move_to([0.3, 0.65, 0]), run_time=1.0)
        thin = egg.copy().set_stroke(width=4)
        self.at("shells thin")
        self.play(Transform(egg, thin), run_time=1.4)
        crack = VMobject(color=RED, stroke_width=7).set_points_as_corners(
            [[2.35, 0.65, 0], [2.85, 0.15, 0], [2.6, -0.25, 0], [3.25, -0.75, 0]])
        self.at("often broke")
        self.play(Create(crack), egg.animate.shift(DOWN * 0.12), run_time=0.9)
        chicks = VGroup(*[eagle_icon(0.55).move_to([x, -2.55, 0]) for x in (-1.2, 0.2, 1.6, 3.0, 4.4)])
        self.at("other eggs failed")
        self.play(FadeIn(chicks), run_time=0.7)
        bob(chicks, amp=0.12, speed=1.7)
        self.at("fewer chicks")
        self.play(*[FadeOut(chicks[i]) for i in (1, 2, 4)], chicks[0].animate.shift(RIGHT * 1.1),
                  chicks[3].animate.shift(LEFT * 1.1), run_time=1.1)
        self.finish()


class S03MoreHarm(SpokenScene):
    def construct(self):
        world = shoreline_world(nests=4, wide_search=True)
        wave = moving_water(world)
        self.add(world, wave, scope_tag("schematic"))
        dde = chip("DDE", RED, 30).move_to([-5.1, 3.05, 0])
        self.at("not the only problem")
        self.play(FadeIn(dde), run_time=0.5)
        forest_loss = T("nesting habitat lost", 30, RED).move_to([0, 3.1, 0])
        self.at("destroyed nesting habitat")
        self.play(FadeIn(forest_loss), world.trees.animate.set_opacity(0.3), run_time=1.2)
        illegal = T("illegal shooting", 30, RED).move_to([4.7, 3.05, 0])
        self.at("shot eagles illegally")
        self.play(FadeIn(illegal), run_time=0.6)
        arrows = VGroup(*[Arrow([x, 2.75, 0], [x * 0.7, 1.45, 0], buff=0.12,
                                     color=RED, stroke_width=5) for x in (-4.8, 0, 4.8)])
        self.at("pushed the same population downward")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.22), run_time=1.4)
        gauge_value = ValueTracker(0.82)
        gauge = allow_component_internals(dial(gauge_value, center=[0, -0.55, 0], radius=1.3,
                                               label="occupied nests", color=GOLD))
        self.play(FadeIn(gauge), run_time=0.5)
        self.at("fewer young survived")
        self.play(gauge_value.animate.set_value(0.26), FadeOut(world.nests[1]), run_time=2.0)
        self.at("several pressures")
        self.play(Indicate(arrows, color=RED, scale_factor=1.03), run_time=1.0)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = shoreline_world(nests=4, wide_search=True, forest=0.45)
        wave = moving_water(world)
        harms = VGroup(chip("DDT / DDE", RED, 28).move_to([-4.7, 2.95, 0]),
                       T("habitat loss", 28, RED).move_to([4.6, 2.95, 0]))
        self.add(world, wave, harms, scope_tag("schematic"))
        barrier = RoundedRectangle(corner_radius=0.25, width=12.25, height=4.75,
                                   color=TEAL, stroke_width=7).move_to([0, 0.05, 0])
        restored = shoreline_world(nests=4, wide_search=True, forest=1.0)
        self.at("remove the pesticide pressure")
        self.play(FadeOut(harms[0], shift=UP * 0.3), Create(barrier), run_time=1.1)
        self.at("protect nesting forest")
        self.play(Transform(world.forest, restored.forest), Transform(world.trees, restored.trees),
                  FadeOut(harms[1]), run_time=1.4)
        q = question_card("Jump now—or rise over time?", y=-2.95, size=34, color=GOLD)
        self.at("what should happen next")
        self.play(FadeIn(q.question), run_time=0.7)
        self.at("jump immediately")
        jump = Arrow([-2.8, -1.95, 0], [-2.8, 0.2, 0], color=GOLD, stroke_width=6)
        rise = Arrow([1.0, -1.9, 0], [3.5, -0.2, 0], color=TEAL, stroke_width=6)
        self.play(GrowArrow(jump), GrowArrow(rise), run_time=1.1)
        for m in world.nests:
            bob(m, amp=0.045, speed=1.5)
        self.at("hold your answer")
        self.play(FadeOut(jump), FadeOut(rise), run_time=0.5)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Jump now—or rise over time?"
    SECONDS = 4.5
    CARD = {"y": -2.95, "size": 34, "color": GOLD}

    def backdrop(self):
        world = shoreline_world(nests=4, wide_search=True)
        for m in world.nests:
            bob(m, amp=0.045, speed=1.5)
        world.add(moving_water(world), RoundedRectangle(corner_radius=0.25, width=12.25, height=4.75,
                                                        color=TEAL, stroke_width=7).move_to([0, 0.05, 0]))
        return world


class S06Actions(SpokenScene):
    def construct(self):
        world = shoreline_world(nests=1, wide_search=True)
        wave = moving_water(world)
        cursor = ValueTracker(-5.0)
        self.add(world, wave, timeline(cursor), scope_tag("schematic"))
        answer = T("RISE OVER TIME", 38, TEAL, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(answer), run_time=0.6)
        ddt = chip("DDT", RED, 32).move_to([-4.6, 0.0, 0])
        self.add(ddt)
        ban = chip("1972: U.S. bans most DDT uses", TEAL, 28).move_to([0, 3.1, 0])
        self.at("United States banned")
        self.play(FadeOut(answer), FadeOut(ddt, shift=DOWN * 0.3), run_time=0.4)
        self.play(FadeIn(ban), run_time=0.6)
        ring = Circle(radius=0.75, color=TEAL, stroke_width=7).move_to(world.nests[0])
        self.at("laws protected eagles")
        self.play(Create(ring), run_time=0.8)
        lock = VGroup(RoundedRectangle(corner_radius=0.12, width=1.1, height=0.85,
                                      color=TEAL, stroke_width=6),
                      Arc(radius=0.32, start_angle=0, angle=PI, color=TEAL, stroke_width=6)
                      .shift(UP * 0.43)).move_to([4.7, 1.7, 0])
        self.at("protected nesting places")
        self.play(FadeIn(lock), world.trees.animate.set_color(GREEN), run_time=0.9)
        self.at("instead of creating")
        self.play(Indicate(world.nests[0], color=GOLD), run_time=0.8)
        conditions = caption("Protection changed conditions for survival.", 30, TEAL)
        self.at("protection changed")
        self.play(FadeOut(ban), FadeIn(conditions), run_time=0.7)
        self.finish()


class S07Delay(SpokenScene):
    def construct(self):
        world = shoreline_world(nests=1, wide_search=True)
        world.set_opacity(0.28)
        cursor = ValueTracker(-5.0)
        tl = timeline(cursor)
        self.add(world, moving_water(world), tl, scope_tag("schematic"))
        pair = VGroup(eagle_icon(0.75), eagle_icon(0.75)).arrange(RIGHT, buff=0.15).move_to([-4.6, 0.8, 0])
        nest = nest_marker(2.0).move_to([-2.7, 0.75, 0])
        self.at("a pair may raise young")
        self.play(FadeIn(pair), FadeIn(nest), cursor.animate.set_value(-3.5), run_time=1.3)
        chick = eagle_icon(0.5).move_to([-0.8, 0.75, 0])
        self.play(TransformFromCopy(nest, chick), cursor.animate.set_value(-2.0), run_time=1.0)
        young = eagle_icon(0.8).move_to([1.2, 0.75, 0])
        self.at("several years before breeding")
        self.play(Transform(chick, young), cursor.animate.set_value(1.0), run_time=2.0)
        dangers = T("death and new dangers", 28, RED).move_to([0, 2.75, 0])
        self.at("die or meet new dangers")
        ghost = young.copy().shift(UP * 0.9)
        self.play(FadeIn(dangers), FadeOut(ghost), cursor.animate.set_value(2.0), run_time=1.0)
        new_pair = VGroup(eagle_icon(0.75), eagle_icon(0.75)).arrange(RIGHT, buff=0.15).move_to([4.4, 0.75, 0])
        loop = CurvedArrow([1.9, 0.55, 0], [3.5, 0.55, 0], angle=-0.6, color=GOLD, stroke_width=6)
        self.at("each loop from nest")
        self.play(Create(loop), TransformFromCopy(young, new_pair), cursor.animate.set_value(4.8), run_time=2.0)
        self.at("delay shapes")
        self.play(Indicate(tl, color=TEAL, scale_factor=1.02), run_time=0.9)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        world = shoreline_world(nests=1, wide_search=True)
        wave = moving_water(world)
        protections = RoundedRectangle(corner_radius=0.25, width=12.25, height=4.75,
                                       color=TEAL, stroke_width=7).move_to([0, 0.05, 0])
        harm_arrows = VGroup(*[Arrow([x, 3.0, 0], [x * 0.7, 1.65, 0], color=RED, stroke_width=5)
                               for x in (-4.4, 0, 4.4)])
        self.add(world, wave, protections, harm_arrows, scope_tag("schematic"))
        rule = fit_text("Remove harm • Protect what remains • Recover over time", 11.2, 35, TEAL)
        rule.move_to([0, 3.2, 0])
        self.at("here is the rule")
        self.play(FadeIn(rule), run_time=0.7)
        self.at("remove the harm")
        self.play(harm_arrows.animate.set_stroke(opacity=0.18), run_time=1.0)
        self.at("protect what remains")
        self.play(Indicate(protections, color=TEAL, scale_factor=1.02), run_time=0.9)
        gauge_value = ValueTracker(0.18)
        gauge = allow_component_internals(dial(gauge_value, center=[4.4, -0.2, 0], radius=1.15,
                                               label="occupied nests", color=GOLD))
        self.play(FadeOut(rule), FadeIn(gauge), run_time=0.6)
        loop = VGroup(eagle_icon(0.7), nest_marker(1.5), eagle_icon(0.45), eagle_icon(0.7))
        loop.arrange(RIGHT, buff=0.65).move_to([-2.0, 0.0, 0])
        arrows = VGroup(*[Arrow(loop[i].get_right(), loop[i+1].get_left(), buff=0.12,
                                  color=GOLD, stroke_width=5) for i in range(3)])
        self.at("many rounds of reproduction")
        self.play(LaggedStart(*[FadeIn(m) for m in loop], *[GrowArrow(a) for a in arrows], lag_ratio=0.13),
                  gauge_value.animate.set_value(0.58), run_time=2.5)
        self.at("across many seasons")
        self.play(gauge_value.animate.set_value(0.92),
                  Indicate(loop, color=GOLD, scale_factor=1.04), run_time=2.0)
        self.finish()


class S09Evidence(SpokenScene):
    def construct(self):
        P = Plot(box=(-5.8, 5.0, -2.25, 2.35), xr=(1977, 2016), yr=(0, 1150),
                 xticks=[(1977, "1977"), (2004, "2004"), (2016, "2016")],
                 yticks=[(0, "0"), (500, "500"), (1000, "1,000")],
                 xlabel="breeding year", ylabel="eagle pairs", color=GREY, label_size=28)
        years = np.array([p[0] for p in SURVEY], dtype=float)
        counts = np.array([p[1] for p in SURVEY], dtype=float)
        survey_fn = lambda year: float(np.interp(year, years, counts))
        year = ValueTracker(1977)
        live = P.live_curve(survey_fn, year, color=GOLD, width=7)
        dot = P.dot(lambda: year.get_value(), lambda: survey_fn(year.get_value()), color=GOLD)
        title = T("selected survey years", 32, GREY).move_to([0, 3.25, 0])
        self.play(FadeIn(title), Create(P), run_time=1.0)
        self.add(live, dot)
        self.at("rose over decades")
        self.play(year.animate.set_value(2003), run_time=2.0, rate_func=linear)
        self.at("small dip")
        self.play(year.animate.set_value(2004), run_time=0.8, rate_func=linear)
        dip = T("small dip", 28, RED).next_to(P.pt(2004, 428), DOWN, buff=0.25)
        self.play(FadeIn(dip), year.animate.set_value(2016), run_time=2.4, rate_func=linear)
        self.at("does not prove")
        caution = caption("Evidence ≠ a complete cause map", 32, GOLD)
        self.play(FadeOut(P.xlabel), FadeIn(caution), run_time=0.7)
        factors = VGroup(*[chip(x, c, 24) for x, c in
                           [("coverage", GREY), ("weather", BLUE), ("habitat", GREEN), ("protections", TEAL)]])
        allow_component_internals(factors)
        factors.arrange(RIGHT, buff=0.25).move_to([-1.0, 1.5, 0])
        self.at("search coverage")
        self.play(FadeOut(dip), LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in factors], lag_ratio=0.18),
                  run_time=1.5)
        self.at("scientists interpret counts")
        outline = DashedVMobject(RoundedRectangle(corner_radius=0.18, width=6.9, height=0.95,
                                                   color=GREY, stroke_width=3), num_dashes=28)
        outline.move_to(factors)
        self.play(Create(outline), run_time=0.8)
        self.finish()


class S10Handoff(SpokenScene):
    def construct(self):
        world = shoreline_world(nests=8, wide_search=True)
        wave = moving_water(world)
        self.add(world, wave, scope_tag("schematic"))
        self.at("population responding")
        self.play(Indicate(world.nests, color=GOLD, scale_factor=1.05), run_time=1.0)
        bay = Polygon([-6.2, -2.6, 0], [6.2, -2.6, 0], [6.2, 2.4, 0], [-6.2, 2.4, 0],
                      color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18)
        floor = Rectangle(width=12.4, height=0.45, color=GREY, stroke_width=3,
                          fill_color=GREY, fill_opacity=0.35).move_to([0, -2.35, 0])
        self.at("entire habitat")
        self.play(FadeOut(world, shift=LEFT * 2), FadeIn(bay, shift=RIGHT * 2),
                  FadeIn(floor, shift=RIGHT * 2), run_time=2.2)
        missing = T("starter organisms missing", 34, RED).move_to([0, 0.1, 0])
        self.at("organisms needed to restart")
        self.play(FadeIn(missing), run_time=0.8)
        restoration = chip("RESTORATION", TEAL, 34).move_to([0, 2.7, 0])
        self.at("restoration enters")
        self.play(FadeIn(restoration, shift=DOWN * 0.2), FadeOut(missing), run_time=0.9)
        eagle = eagle_icon(1.0).move_to([-5.5, 1.4, 0])
        self.at("next film")
        self.play(eagle.animate.move_to([5.5, 1.4, 0]), run_time=2.0, rate_func=linear)
        self.finish()


class S11End(EndCard):
    LINE = "Remove the harm, protect what remains, and help ecosystems recover over time."
