"""From One Day to One Year.

COLOR MAP (fixed across the film)
  BLUE  = light and day length
  RED   = temperature
  GOLD  = inner timing
  GREEN = biological response
  GREY  = structure and neutral context

The nested dial is the film's one carried world.  Every scene that uses it calls
``nested_dial`` so its circles and landmarks stay at exactly the same scale and place.
"""
from bp_parts import *


NIGHT = "#17264A"
PINK = "#F3A7C5"


def arrow(a, b, color=GREY, width=5, tip=0.22):
    return Arrow(a, b, buff=0, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def slow_turn(mob, center, speed=0.055):
    """Keep a narrated timing band visibly turning between spoken beats."""
    c = np.array(center, dtype=float)
    return mob.add_updater(lambda m, dt: m.rotate(speed * dt, about_point=c))


def monarch(height=0.9):
    """A schematic butterfly, used only as the narrated organism marker."""
    left = VGroup(
        Ellipse(width=0.75, height=0.52, color=GREEN, stroke_width=3,
                fill_color=GREEN, fill_opacity=0.30).rotate(0.45).shift(LEFT * 0.38 + UP * 0.18),
        Ellipse(width=0.58, height=0.40, color=GREEN, stroke_width=3,
                fill_color=GREEN, fill_opacity=0.20).rotate(-0.35).shift(LEFT * 0.31 + DOWN * 0.20),
    )
    right = left.copy().flip(RIGHT)
    body = RoundedRectangle(width=0.11, height=0.85, corner_radius=0.05,
                            stroke_width=0, fill_color=GREEN, fill_opacity=1)
    g = VGroup(left, right, body)
    g.set_height(height)
    return g


def twig(height=1.25, open_bud=True):
    stem = Line(DOWN * 0.55 + LEFT * 0.35, UP * 0.48 + RIGHT * 0.28,
                color=GREEN, stroke_width=7)
    bud = Circle(radius=0.25, color=GREEN, stroke_width=4,
                 fill_color=GREEN, fill_opacity=0.28).move_to(stem.get_end() + UP * 0.18)
    if open_bud:
        petals = VGroup(*[
            Circle(radius=0.13, stroke_color=PINK, stroke_width=3,
                   fill_color=PINK, fill_opacity=0.55).move_to(bud.get_center() +
                   0.20 * np.array([np.cos(a), np.sin(a), 0]))
            for a in np.linspace(0, TAU, 6)[:-1]
        ])
        bud = VGroup(bud, petals)
    g = VGroup(stem, bud).set_height(height)
    g.bud = bud
    return g


def groundhog(height=1.0):
    body = Ellipse(width=1.10, height=0.70, color=GREEN, stroke_width=4,
                   fill_color=GREEN, fill_opacity=0.20)
    head = Circle(radius=0.30, color=GREEN, stroke_width=4,
                  fill_color=GREEN, fill_opacity=0.30).move_to(body.get_right() + LEFT * 0.10 + UP * 0.25)
    ears = VGroup(*[Circle(radius=0.09, color=GREEN, stroke_width=3,
                           fill_color=GREEN, fill_opacity=0.35).move_to(head.get_top() + d)
                    for d in (LEFT * 0.16, RIGHT * 0.14)])
    eye = Dot(head.get_center() + RIGHT * 0.09 + UP * 0.04, radius=0.035, color=TEXT)
    g = VGroup(body, head, ears, eye).set_height(height)
    return g


def owl(height=1.0):
    body = Ellipse(width=0.85, height=1.05, color=GREEN, stroke_width=4,
                   fill_color=GREEN, fill_opacity=0.20)
    eyes = VGroup(*[Circle(radius=0.16, color=TEXT, stroke_width=3).add(
        Dot(radius=0.045, color=TEXT)) for _ in range(2)]).arrange(RIGHT, buff=0.08)
    eyes.move_to(body.get_center() + UP * 0.18)
    g = VGroup(body, eyes).set_height(height)
    return g


def squirrel(height=1.0):
    body = Ellipse(width=0.80, height=0.50, color=GREEN, stroke_width=4,
                   fill_color=GREEN, fill_opacity=0.20)
    head = Circle(radius=0.22, color=GREEN, stroke_width=4,
                  fill_color=GREEN, fill_opacity=0.22).next_to(body, RIGHT, buff=-0.08).shift(UP * 0.13)
    tail = Arc(radius=0.43, start_angle=-0.4, angle=4.5, color=GREEN,
               stroke_width=9).next_to(body, LEFT, buff=-0.25).shift(UP * 0.18)
    g = VGroup(body, head, tail).set_height(height)
    return g


def nested_dial(center=ORIGIN, outer_r=3.0, inner_r=1.62,
                light=True, temperature=True, inner_gold=True):
    """The single carried world: one year ring containing one day ring."""
    c = np.array(center, dtype=float)
    outer = Circle(radius=outer_r, color=GREY, stroke_width=5,
                   fill_color=GREY, fill_opacity=0.18).move_to(c)
    seasons = VGroup(
        T("SPRING", 24, GREY).move_to(c + UP * outer_r * 1.08),
        T("SUMMER", 24, GREY).move_to(c + RIGHT * outer_r * 1.27),
        T("FALL", 24, GREY).move_to(c + DOWN * outer_r * 1.08),
        T("WINTER", 24, GREY).move_to(c + LEFT * outer_r * 1.27),
    )
    day_outline = Circle(radius=inner_r, color=GREY, stroke_width=4,
                         fill_color=NIGHT, fill_opacity=0.24).move_to(c)
    night = AnnularSector(inner_radius=inner_r - 0.25, outer_radius=inner_r,
                          angle=PI, start_angle=PI / 2, fill_color=NIGHT,
                          fill_opacity=0.95, stroke_width=0).move_to(c)
    day = AnnularSector(inner_radius=inner_r - 0.25, outer_radius=inner_r,
                        angle=PI, start_angle=-PI / 2, fill_color=BLUE,
                        fill_opacity=0.75, stroke_width=0).move_to(c)
    daynight = VGroup(night, day) if light else VGroup(
        AnnularSector(inner_radius=inner_r - 0.25, outer_radius=inner_r,
                      angle=TAU - 0.002, start_angle=0, fill_color=NIGHT,
                      fill_opacity=0.95, stroke_width=0).move_to(c))
    gold = Arc(radius=inner_r - 0.48, start_angle=0.15, angle=TAU - 0.3,
               arc_center=c, color=GOLD, stroke_width=10) if inner_gold else VGroup()
    temp = Arc(radius=outer_r - 0.18, start_angle=-PI * 0.05, angle=PI * 0.92,
               arc_center=c, color=RED, stroke_width=12) if temperature else VGroup()
    g = VGroup(outer, seasons, day_outline, daynight, gold, temp)
    g.outer, g.seasons, g.day_outline, g.daynight, g.gold, g.temp = (
        outer, seasons, day_outline, daynight, gold, temp)
    return g


def full_dial_with_life():
    """Stable opening/pull-back composition shared by s01, s08 and s12."""
    d = nested_dial(center=[0, 0.15, 0], outer_r=2.85, inner_r=1.47)
    t = twig(1.15).move_to([-4.65, 1.85, 0])
    m = monarch(1.0).move_to([4.75, 1.75, 0])
    g = groundhog(1.0).move_to([3.0, -2.85, 0])
    return VGroup(d, t, m, g)


def dark_prediction_backdrop():
    d = nested_dial(center=[-1.6, 0.35, 0], outer_r=2.65, inner_r=2.05,
                    light=False, temperature=False)
    # The question occupies the right and bottom bands.
    d.seasons.set_opacity(0)
    d.outer.set_stroke(opacity=0.35).set_fill(opacity=0.18)
    return d


class S01Hook(SpokenScene):
    def construct(self):
        world = full_dial_with_life()
        dial, tree, butterfly, hog = world
        self.play(FadeIn(dial.outer), FadeIn(dial.day_outline), run_time=0.7)
        self.play(FadeIn(tree), FadeIn(butterfly), run_time=0.7)
        self.at("Watch one dial")
        self.play(FadeIn(dial.seasons), FadeIn(dial.daynight), run_time=0.8)
        slow_turn(dial.daynight, dial.get_center(), 0.045)
        self.play(Rotate(dial.daynight, angle=PI / 2, about_point=dial.get_center()), run_time=1.6, rate_func=linear)
        self.at("blue light band turns")
        self.play(Rotate(dial.daynight, angle=PI, about_point=dial.get_center()), run_time=2.1, rate_func=linear)
        self.at("red temperature band")
        self.play(Create(dial.temp), run_time=1.4)
        self.play(Rotate(dial.temp, angle=0.35, about_point=dial.get_center()), run_time=1.1, rate_func=there_and_back)
        self.at("living things change")
        self.play(FadeIn(hog), butterfly.animate.shift(DOWN * 0.35),
                  tree.animate.scale(1.08), run_time=1.5)
        bob(butterfly, amp=0.06, speed=2.2)
        bob(hog, amp=0.035, speed=1.5, seed=2)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Daily and seasonal rhythms"
    TITLE = "From One Day to One Year"

    def construct(self):
        d = nested_dial(center=[0, -0.05, 0], outer_r=3.25, inner_r=1.70)
        d.set_opacity(0.38)
        d.seasons.set_opacity(0)
        title = T(self.TITLE, 54, TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON.upper(), 24, TEAL)
        plate = RoundedRectangle(width=9.7, height=1.75, corner_radius=0.2,
                                 stroke_width=0, fill_color=BG, fill_opacity=0.88)
        words = VGroup(lesson, title).arrange(DOWN, buff=0.25).move_to(plate)
        self.add(d)
        self.play(Rotate(d.daynight, PI / 2, about_point=d.get_center()), FadeIn(plate),
                  FadeIn(words), run_time=1.0, rate_func=linear)
        self.play(Rotate(d.daynight, PI / 2, about_point=d.get_center()), run_time=1.0, rate_func=linear)
        self.finish()


class S03Daily(SpokenScene):
    def construct(self):
        d = nested_dial(center=[0, 0.15, 0], outer_r=3.15, inner_r=2.62,
                        temperature=False)
        d.seasons.set_opacity(0)
        d.outer.set_stroke(opacity=0.25).set_fill(opacity=0.18)
        self.play(FadeIn(d.day_outline), FadeIn(d.daynight), run_time=0.8)
        slow_turn(d.daynight, d.get_center(), 0.16)
        self.at("circadian rhythm")
        self.play(Create(d.gold), run_time=1.7)
        circ = T("CIRCADIAN RHYTHM", 32, GOLD).move_to([0, 0.15, 0])
        circ.layout_ok = True  # Deliberately labels the open centre of its own rhythm ring.
        hours = M("24 h", 32, TEXT).next_to(circ, DOWN, buff=0.20)
        self.play(FadeIn(circ), FadeIn(hours), run_time=0.6)
        self.at("Light and darkness")
        light_lab = T("LIGHT AND DARK", 29, BLUE).move_to([0, 3.43, 0])
        self.play(FadeIn(light_lab), Rotate(d.daynight, PI / 2, about_point=d.get_center()), run_time=1.5)
        self.at("Many owls")
        ow = owl(1.15).move_to([-4.65, 0.8, 0])
        self.play(FadeIn(ow), Rotate(d.daynight, PI / 3, about_point=d.get_center()), run_time=1.2)
        self.at("Tree squirrels")
        sq = squirrel(1.15).move_to([4.65, 0.8, 0])
        self.play(FadeIn(sq), Rotate(d.daynight, PI / 3, about_point=d.get_center()), run_time=1.2)
        self.at("Yet the rhythm")
        inner_lab = T("INNER RHYTHM", 29, GOLD).move_to([0, -3.30, 0])
        self.play(FadeIn(inner_lab), Rotate(d.gold, PI / 2, about_point=d.get_center()),
                  run_time=2.0, rate_func=linear)
        bob(ow, amp=0.04, speed=1.7)
        bob(sq, amp=0.04, speed=1.9, seed=2)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        d = nested_dial(center=[-1.6, 0.35, 0], outer_r=2.65, inner_r=2.05,
                        temperature=False)
        d.seasons.set_opacity(0)
        d.outer.set_stroke(opacity=0.35).set_fill(opacity=0.18)
        self.add(d.day_outline, d.daynight, d.gold, d.outer)
        slow_turn(d.gold, d.get_center(), 0.040)
        self.at("blue light band disappears")
        dark = dark_prediction_backdrop()
        self.play(Transform(d.daynight, dark.daynight), run_time=1.4)
        self.at("Will the gold")
        q = question_card("VANISH OR CONTINUE?", ["VANISH", "CONTINUE"],
                          chips_at=[4.45, -0.15, 0], y=-3.15, size=36, chip_size=30)
        self.play(FadeIn(q.question), run_time=0.6)
        self.play(FadeIn(q.chips), run_time=0.6)
        self.at("Watch the gold marker")
        marker = Dot(d.gold.point_from_proportion(0.12), radius=0.22, color=GOLD)
        self.play(FadeIn(marker), run_time=0.4)
        sweep = Arc(radius=2.35, start_angle=0.5, angle=1.7, arc_center=d.get_center(),
                    color=GOLD, stroke_width=18, stroke_opacity=0.45)
        slow_turn(sweep, d.get_center(), 1.3)
        self.add(sweep)
        slow_turn(marker, d.get_center(), 1.3)
        self.play(marker.animate.scale(1.5), run_time=0.7, rate_func=there_and_back)
        self.at("Choose before")
        self.play(Indicate(q.question, color=GOLD, scale_factor=1.03), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "VANISH OR CONTINUE?"
    OPTIONS = ["VANISH", "CONTINUE"]
    CHIPS_AT = [4.45, -0.15, 0]
    CARD = {"y": -3.15, "size": 36, "chip_size": 30}
    RING_AT = [5.95, -3.15, 0]
    SECONDS = 4.5

    def backdrop(self):
        d = dark_prediction_backdrop()
        marker = Dot(d.gold.point_from_proportion(0.12), radius=0.22, color=GOLD)
        pulse(d.gold, base=9.0, amp=2.0, speed=2.0)
        slow_turn(marker, d.get_center(), 1.3)
        sweep = Arc(radius=2.35, start_angle=0.5, angle=1.7, arc_center=d.get_center(),
                    color=GOLD, stroke_width=18, stroke_opacity=0.45)
        slow_turn(sweep, d.get_center(), 1.3)
        return VGroup(d, marker, sweep)


class S06Reveal(SpokenScene):
    def construct(self):
        d = dark_prediction_backdrop()
        marker = Dot(d.gold.point_from_proportion(0.10), radius=0.17, color=GOLD)
        self.add(d, marker)
        slow_turn(marker, d.get_center(), 0.24)
        pulse(d.gold, base=10.0, amp=1.8, speed=1.7)
        self.at("keeps circling")
        self.play(MoveAlongPath(marker, d.gold.copy()), Rotate(d.gold, TAU,
                  about_point=d.get_center()), run_time=3.2, rate_func=linear)
        inside = T("TIMING FROM INSIDE", 31, GOLD).move_to([3.9, 1.75, 0])
        self.at("inside the body")
        self.play(FadeIn(inside), run_time=0.7)
        self.at("Outside light")
        lit = nested_dial(center=[-1.6, 0.35, 0], outer_r=2.65, inner_r=2.05,
                          temperature=False)
        lit.seasons.set_opacity(0)
        lit.outer.set_opacity(0.35)
        self.play(Transform(d.daynight, lit.daynight), run_time=1.2)
        self.at("lined up with the day")
        step = T("KEPT IN STEP", 34, BLUE).move_to([3.9, 0.65, 0])
        self.play(Rotate(d.gold, 0.65, about_point=d.get_center()), FadeIn(step), run_time=1.8)
        self.at("work together")
        link = VGroup(arrow([3.0, 0.15, 0], [4.75, 0.15, 0], BLUE),
                      T("TOGETHER", 30, GREEN).move_to([3.9, -0.35, 0]))
        self.play(FadeIn(link), Rotate(d.daynight, PI / 3, about_point=d.get_center()), run_time=1.5)
        self.finish()


def bean_shoot(curve=0.0):
    """Computed centreline and paired cell blocks for the narrated tropism schematic."""
    n, seg = 6, 0.78
    k = max(curve, 0.0001)
    radius = 1 / k
    parts = VGroup()
    for i in range(n):
        s0, s1 = i * seg, (i + 1) * seg
        def p(s, side):
            a = k * s
            centre = np.array([radius * (1 - np.cos(a)), -2.65 + radius * np.sin(a), 0])
            normal = np.array([-np.cos(a), np.sin(a), 0])
            return centre + side * 0.48 * normal
        mid0, mid1 = p(s0, 0), p(s1, 0)
        parts.add(Polygon(p(s0, 1), p(s1, 1), mid1, mid0,
                          color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.34))
        parts.add(Polygon(mid0, mid1, p(s1, -1), p(s0, -1),
                          color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.14))
    return parts


class S07Tropism(SpokenScene):
    def construct(self):
        seed = nested_dial(center=[0, 0.15, 0], outer_r=2.8, inner_r=2.2,
                           temperature=False)
        seed.seasons.set_opacity(0)
        shoot = bean_shoot(0.0001)
        self.play(ReplacementTransform(seed.day_outline, shoot), run_time=1.0)
        pulse(shoot, base=3.5, amp=1.0, speed=1.5)
        bob(shoot, amp=0.11, speed=1.7)
        self.at("A tropism")
        name = T("TROPISM", 36, GREEN).move_to([0, 3.35, 0])
        self.play(FadeIn(name), run_time=0.5)
        self.at("Light moves")
        lamp = VGroup(Circle(radius=0.38, color=BLUE, stroke_width=5,
                             fill_color=BLUE, fill_opacity=0.25),
                      VGroup(*[Line(ORIGIN, LEFT * 0.45, color=BLUE, stroke_width=4)
                               .rotate(a, about_point=ORIGIN) for a in (-0.45, 0, 0.45)])
                      .shift(LEFT * 0.45)).move_to([5.3, 0.8, 0])
        beam = Polygon([-4.2, 2.8, 0], [-4.2, -2.1, 0], [4.7, 0.8, 0],
                       stroke_width=0, fill_color=BLUE, fill_opacity=0.10)
        beam.set_z_index(-1)
        self.play(FadeIn(beam), FadeIn(lamp), lamp.animate.move_to([-4.8, 0.8, 0]), run_time=1.8)
        self.at("Cells lengthen")
        shaded = T("SHADED SIDE", 29, GREEN).move_to([3.8, 1.85, 0])
        lit = T("LIT SIDE", 29, BLUE).move_to([3.8, 1.25, 0])
        self.play(FadeIn(shaded), run_time=0.5)
        self.play(FadeIn(lit), run_time=0.5)
        bent = bean_shoot(-0.17)
        self.at("bends toward light")
        shoot.clear_updaters()
        self.play(Transform(shoot, bent), run_time=2.5, rate_func=smooth)
        bob(shoot, amp=0.09, speed=1.6)
        self.at("Roots can also")
        root = arrow([0.0, -2.65, 0], [-2.0, -3.25, 0], BLUE, width=5)
        wet = T("WETTER", 28, BLUE).move_to([-3.1, -3.25, 0])
        self.play(GrowArrow(root), FadeIn(wet), run_time=1.2)
        self.add(scope_tag("schematic"))
        self.finish()


class S08Seasons(SpokenScene):
    def construct(self):
        world = full_dial_with_life()
        d, bud, mon, hog = world
        self.play(FadeIn(d), FadeIn(bud), FadeIn(mon), FadeIn(hog), run_time=1.0)
        slow_turn(d.daynight, d.get_center(), 0.17)
        bob(bud, amp=0.07, speed=1.5)
        bob(hog, amp=0.07, speed=1.7, seed=2)
        self.at("Shorter days")
        short = Arc(radius=1.47, start_angle=-PI / 2, angle=PI * 0.55,
                    arc_center=d.get_center(), color=BLUE, stroke_width=15)
        self.play(Transform(d.daynight[1], short), Rotate(d.temp, -0.75,
                  about_point=d.get_center()), run_time=2.2)
        self.at("Monarchs migrate")
        south = arrow([4.75, 1.2, 0], [4.75, -1.0, 0], GREEN, width=6)
        self.play(GrowArrow(south), mon.animate.shift(DOWN * 1.9), run_time=1.5)
        self.at("Tree buds")
        closed = twig(1.15, open_bud=False).move_to(bud)
        self.play(Transform(bud, closed), run_time=1.0)
        self.at("Groundhogs hibernate")
        temp = ValueTracker(0.78)
        gauge = dial(temp, center=[-4.55, -1.55, 0], radius=0.85,
                     label="BODY TEMPERATURE", color=RED, fmt="{:.0f}%", size=30)
        self.play(FadeIn(gauge), run_time=0.6)
        self.play(temp.animate.set_value(0.25), hog.animate.shift(DOWN * 0.18), run_time=2.0)
        self.at("Deciduous trees")
        leaves = VGroup(*[Dot(radius=0.10, color=GREEN).move_to([-4.7 + 0.18*i, 1.6 + 0.12*(i%2), 0])
                          for i in range(5)])
        self.play(FadeIn(leaves), leaves.animate.shift(DOWN * 1.2), run_time=1.6)
        self.finish()


def winter_response_world():
    sector = AnnularSector(inner_radius=2.25, outer_radius=3.05, angle=PI * 0.88,
                           start_angle=PI * 0.56, fill_color=BLUE, fill_opacity=0.20,
                           stroke_color=BLUE, stroke_width=4)
    mon = monarch(0.85).move_to([-4.35, 1.6, 0])
    bud = twig(1.05, open_bud=False).move_to([0, 1.55, 0])
    hog = groundhog(0.90).move_to([4.25, 1.55, 0])
    return VGroup(sector, mon, bud, hog)


class S09Survival(SpokenScene):
    def construct(self):
        w = winter_response_world()
        sector, mon, bud, hog = w
        self.play(FadeIn(sector), FadeIn(mon), FadeIn(bud), FadeIn(hog), run_time=0.9)
        bob(bud, amp=0.10, speed=1.6)
        bob(hog, amp=0.10, speed=1.8, seed=2)
        self.at("Migration changes place")
        move = T("MOVE", 32, GREEN).move_to([-5.55, -0.15, 0])
        path = arrow([-4.3, 1.0, 0], [-4.3, -2.0, 0], GREEN, width=6)
        self.play(GrowArrow(path), mon.animate.move_to([-4.3, -1.55, 0]), FadeIn(move), run_time=2.0)
        self.at("Dormancy slows")
        pause_lab = T("PAUSE GROWTH", 30, GREEN).move_to([0, -0.15, 0])
        life = Circle(radius=0.18, color=GREEN, stroke_width=6).move_to([0, 0.65, 0])
        self.play(FadeIn(pause_lab), FadeIn(life), run_time=0.8)
        pulse(sector, base=4.0, amp=1.4, speed=1.4)
        self.play(life.animate.scale(1.45), run_time=1.0, rate_func=there_and_back)
        self.at("Hibernation is")
        cool = T("COOL AND REWARM", 29, GREEN).move_to([4.15, -0.15, 0])
        bt = ValueTracker(0.65)
        bar_bg = RoundedRectangle(width=2.1, height=0.34, corner_radius=0.12,
                                  color=GREY, stroke_width=3).move_to([4.15, 0.65, 0])
        bar = always_redraw(lambda: RoundedRectangle(width=max(0.18, 2.1 * bt.get_value()), height=0.30,
                            corner_radius=0.10, stroke_width=0, fill_color=RED, fill_opacity=0.9)
                            .align_to(bar_bg, LEFT).move_to([bar_bg.get_left()[0] + max(0.18, 2.1*bt.get_value())/2,
                                                           bar_bg.get_y(), 0]))
        self.play(FadeIn(bar_bg), FadeIn(bar), FadeIn(cool), run_time=0.8)
        self.play(bt.animate.set_value(0.18), run_time=1.4)
        self.at("briefly warm")
        self.play(bt.animate.set_value(0.72), run_time=1.0)
        self.at("then cool again")
        self.play(bt.animate.set_value(0.20), run_time=1.2)
        self.at("Each response")
        cap = caption("Different responses meet the same hard season.", color=TEXT)
        cap.layout_ok = True  # Bottom-band summary is intentionally below the winter sector.
        self.play(FadeIn(cap), run_time=0.8)
        self.finish()


class S10Clocks(SpokenScene):
    def construct(self):
        d = nested_dial(center=[-2.0, 0.2, 0], outer_r=2.85, inner_r=1.65,
                        temperature=False, inner_gold=False)
        self.play(FadeIn(d.outer), FadeIn(d.daynight), run_time=0.8)
        slow_turn(d.daynight, d.get_center(), 0.18)
        self.at("inner yearly timing")
        yearly = Arc(radius=2.28, start_angle=0.08, angle=TAU - 0.16,
                     arc_center=d.get_center(), color=GOLD, stroke_width=11)
        self.play(Create(yearly), run_time=2.0)
        slow_turn(yearly, d.get_center(), 0.050)
        yl = T("INNER YEARLY TIMING", 30, GOLD).move_to([3.85, 2.55, 0])
        self.play(FadeIn(yl), run_time=0.6)
        self.at("day length held steady")
        steady = T("DAY LENGTH HELD STEADY", 27, BLUE).move_to([3.85, 1.85, 0])
        self.play(FadeIn(steady), Rotate(yearly, PI / 2, about_point=d.get_center()), run_time=1.5)
        self.at("cycles kept repeating")
        cyc = T("EATING + WEIGHT CYCLES", 28, GREEN).move_to([3.85, 1.15, 0])
        self.play(FadeIn(cyc), Rotate(yearly, PI, about_point=d.get_center()), run_time=2.0)
        self.at("monarch can fly")
        young = monarch(0.9).move_to([3.2, 0.15, 0])
        south = arrow([3.2, -0.35, 0], [3.2, -2.1, 0], GREEN, width=6)
        self.play(FadeIn(young), GrowArrow(south), young.animate.shift(DOWN * 1.4), run_time=1.7)
        self.at("some animals do learn")
        birds = VGroup(*[Arc(radius=0.20, start_angle=0.2, angle=1.1, color=GREEN, stroke_width=4)
                         .rotate(i * 0.25) for i in range(2)]).arrange(RIGHT, buff=0.3).move_to([5.0, -1.1, 0])
        learned = T("SOME ROUTES ARE LEARNED", 25, GREEN).move_to([3.9, -2.65, 0])
        self.play(FadeIn(birds), FadeIn(learned), birds.animate.shift(LEFT * 0.45), run_time=1.3)
        self.finish()


class S11Refine(SpokenScene):
    def construct(self):
        dial = Circle(radius=2.7, color=GREY, stroke_width=5,
                      fill_color=GREY, fill_opacity=0.14).move_to([-1.2, 0.15, 0])
        cold = Arc(radius=2.7, start_angle=PI * 0.65, angle=PI * 0.55,
                   arc_center=dial.get_center(), color=BLUE, stroke_width=14)
        warm = Arc(radius=2.7, start_angle=PI * 0.15, angle=PI * 0.38,
                   arc_center=dial.get_center(), color=RED, stroke_width=14)
        bud = twig(1.2, open_bud=False).move_to(dial.get_center() + RIGHT * 2.7)
        self.play(FadeIn(dial), FadeIn(bud), run_time=0.8)
        pulse(dial, base=5.0, amp=1.2, speed=1.3)
        self.at("winter cold")
        self.play(Create(cold), MoveAlongPath(bud, cold.copy()), run_time=2.0)
        cold_lab = T("COLD", 30, BLUE).move_to([-3.25, 2.8, 0])
        self.play(FadeIn(cold_lab), run_time=0.5)
        self.at("later warmth")
        self.play(Create(warm), MoveAlongPath(bud, warm.copy()), run_time=2.0)
        warm_lab = T("WARM", 30, RED).move_to([0.7, 3.0, 0])
        opened = twig(1.25, open_bud=True).move_to(bud)
        self.play(FadeIn(warm_lab), Transform(bud, opened), run_time=1.0)
        self.at("order of cues")
        order = T("COLD  →  WARM  →  OPEN", 27, TEXT).move_to([4.20, 1.55, 0])
        self.play(FadeIn(order), run_time=0.7)
        self.at("one warm day")
        other = twig(1.1, open_bud=False).move_to([3.45, -0.2, 0])
        question = T("?", 54, GOLD).next_to(other, RIGHT, buff=0.3)
        warm_day = T("WARM DAY", 29, RED).move_to([3.45, -1.15, 0])
        self.play(FadeIn(other), FadeIn(warm_day), FadeIn(question), run_time=1.0)
        self.at("timing system")
        system = T("THE ORGANISM'S TIMING SYSTEM", 28, GREEN).move_to([3.45, -2.25, 0])
        self.play(FadeIn(system), question.animate.scale(1.2), run_time=1.0, rate_func=there_and_back)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        d = nested_dial(center=[0, 0.15, 0], outer_r=3.0, inner_r=1.55)
        d.seasons.set_opacity(0)
        self.play(FadeIn(d), run_time=1.0)
        slow_turn(d.daynight, d.get_center(), 0.045)
        slow_turn(d.gold, d.get_center(), -0.040)
        self.at("Gold inner rhythms")
        self.play(Rotate(d.gold, PI, about_point=d.get_center()), run_time=2.0, rate_func=linear)
        self.at("Blue and red cues")
        self.play(Rotate(d.daynight, PI / 2, about_point=d.get_center()),
                  Rotate(d.temp, 0.55, about_point=d.get_center()), run_time=2.0, rate_func=linear)
        self.at("line up responses")
        marks = VGroup(*[Dot(d.outer.point_at_angle(a), radius=0.16, color=GREEN)
                         for a in (0.2, 2.15, 4.35)])
        arrows = VGroup(*[arrow(d.get_center() + 1.8 * np.array([np.cos(a), np.sin(a), 0]),
                                d.get_center() + 2.65 * np.array([np.cos(a), np.sin(a), 0]),
                                color=GREEN, width=4, tip=0.16)
                         for a in (0.2, 2.15, 4.35)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.18),
                  FadeIn(marks), run_time=1.7)
        self.at("No single cue")
        many = T("NO SINGLE CUE FITS EVERY ORGANISM", 30, TEXT).move_to([0, -3.35, 0])
        self.play(FadeIn(many), Rotate(d.daynight, PI / 3, about_point=d.get_center()), run_time=1.6)
        self.at("useful response")
        rule = T("A USEFUL RESPONSE AT A USEFUL TIME", 32, GREEN).move_to([0, 3.48, 0])
        self.play(FadeIn(rule), Rotate(d.gold, PI / 2, about_point=d.get_center()), run_time=1.6)
        self.finish()


class S13End(EndCard):
    LINE = "Inner rhythms and environmental cues time responses;\nlong-term changes can shift them."
