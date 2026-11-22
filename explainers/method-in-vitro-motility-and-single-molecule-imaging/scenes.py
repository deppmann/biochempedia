"""Motility and single-molecule imaging, timed to the supplied narration.

BLUE = glass, TEAL = fluid, GREY = structure and population average,
YELLOW = moving filaments, PURPLE = motors, ORANGE = ATP,
GREEN = fluorescence recovery, RED = loss of contact or trypsin, GOLD = names and prompts.
"""

import os

from bp_parts import *  # noqa: F401,F403
from bp_style import EndCard


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LIQUID = "#172630"
GLASS = "#355873"
TRACK_Y = -1.20
TUBE_Y = 0.72
TRACK_LENGTH = 9.4
PREDICTION = "Can one myosin II walk?"
MYOSIN_X = .10
MYOSIN_SIZE = 1.32
CONTROL_WALK_START = -3.2


def point(x, y):
    return np.array([x, y, 0.0])


def slab(width, height, x, y, color, opacity=1):
    return Rectangle(width=width, height=height, stroke_width=0,
                     fill_color=color, fill_opacity=opacity).move_to(point(x, y))


def heading(text, color=TEXT, size=34, x=0, y=2.70):
    return T(text, size, color).move_to(point(x, y))


def chamber(still=False, overhead=False):
    """The same microscope field, floor, and glass landmarks throughout."""
    pane = slab(12.95, 6.48, 0, 0.05, LIQUID)
    floor = slab(12.95, 1.54, 0, -2.42, GLASS)
    if overhead:
        floor.stretch_to_fit_height(pane.height).move_to(pane)
        floor.set_fill("#233948")
    rim = Line(point(-6.47, -1.65), point(6.47, -1.65), color=BLUE,
               stroke_width=2.5, stroke_opacity=0.50)
    if overhead:
        rim.shift(DOWN * 1.40)
    sides = VGroup(*[
        Line(point(x, -3.19), point(x, 3.28), color=BLUE, stroke_width=2.5,
             stroke_opacity=0.50)
        for x in (-6.47, 6.47)
    ])
    lower = Line(point(-6.47, -3.18), point(6.47, -3.18), color=BLUE,
                 stroke_width=3, stroke_opacity=0.55)
    bevel = slab(12.95, 0.22, 0, -2.97, BLUE, 0.13)
    glints = VGroup()
    for x, y, r, phase in [(-5.8, 1.9, .08, 0.4), (5.7, 1.6, .06, 1.7),
                            (-5.7, -0.55, .05, 2.5), (5.8, -0.25, .08, 3.8)]:
        center = point(x, y)
        speck = Dot(center, radius=r, color=TEAL).set_opacity(.38)
        if not still:
            bob(speck, amp=.19, speed=1.3, seed=phase)
        glints.add(speck)
    scope = scope_tag(size=28, color=TEXT)
    scope.move_to(point(6.38 - scope.width / 2, -3.55))
    return VGroup(pane, floor, bevel, rim, sides, lower, glints, scope)


def track(y=TRACK_Y, x=0, length=TRACK_LENGTH, tube=False, light=1.0):
    """Side view of a solid actin rod or a hollow microtubule."""
    left, right = point(x - length / 2, y), point(x + length / 2, y)
    halo = Line(left, right, color=YELLOW, stroke_width=21 if tube else 17,
                stroke_opacity=.15 * light)
    if not tube:
        core = Line(left, right, color=YELLOW, stroke_width=9,
                    stroke_opacity=.44 + .56 * light)
        return VGroup(halo, core)
    shell = slab(length, .31, x, y, YELLOW, .22 * light)
    rails = VGroup(*[Line(left + dy * UP, right + dy * UP, color=YELLOW,
                           stroke_width=3.8, stroke_opacity=.44 + .56 * light)
                     for dy in (-.145, .145)])
    opening = Ellipse(width=.25, height=.30, stroke_color=YELLOW, stroke_width=3,
                      stroke_opacity=.44 + .56 * light,
                      fill_color=LIQUID, fill_opacity=1).move_to(right)
    return VGroup(halo, shell, rails, opening)


def polarity(tube=False, x=0, y=TRACK_Y, length=TRACK_LENGTH):
    minus, plus = ("−  Minus", "Plus  +") if tube else ("−  Pointed", "Barbed  +")
    return VGroup(
        T(minus, 28, YELLOW).move_to(point(x - length / 2 + .64, y + .50)),
        T(plus, 28, YELLOW).move_to(point(x + length / 2 - .64, y + .50)),
    )


def motor(x, y=TRACK_Y, size=1.0, *, hip=0, feet=(-.57, .57),
          lifts=(0, 0), cargo=False, color=PURPLE, anchor=False):
    """Two contact pads, two legs and one body. y is the track's contact surface."""
    pivot = point(x + size * hip, y + 1.03 * size)
    base = RoundedRectangle(width=.92 * size, height=.50 * size,
                            corner_radius=.19 * size, stroke_width=0,
                            fill_color=color, fill_opacity=1).move_to(pivot)
    legs = VGroup()
    for offset, lift, sign in zip(feet, lifts, (-1, 1)):
        toe = point(x + size * offset, y + size * (.13 + lift))
        knee = (pivot + toe) / 2 + point(sign * .08 * size, .07 * size)
        limb = VMobject().set_points_smoothly([pivot, knee, toe])
        limb.set_stroke(color, 7 * size)
        pad = Ellipse(width=.38 * size, height=.21 * size, stroke_width=0,
                      fill_color=color, fill_opacity=1).move_to(toe)
        legs.add(limb, pad)
    picture = VGroup(legs, base)
    if anchor:
        picture.add(slab(.70 * size, .23 * size, pivot[0], pivot[1] + .27 * size, BLUE))
    if cargo:
        center = pivot + UP * .91 * size
        tether = Line(pivot, center - UP * .56 * size, color=PURPLE, stroke_width=5)
        vesicle = Circle(radius=.56 * size, color=TEXT, stroke_width=3.8,
                         fill_color=BLUE, fill_opacity=.52).move_to(center)
        picture.add_to_back(tether)
        picture.add(vesicle)
    return picture


def walk_pose(progress, start, y=TRACK_Y, size=1.0):
    """One pad remains fixed as the other swings to the next landing site."""
    index = int(progress)
    fraction = progress - index
    stride = .85
    planted = index * stride
    lifted = interpolate(planted - stride, planted + stride, smooth(fraction))
    arch = .43 * np.sin(np.pi * fraction)
    feet = (lifted, planted) if index % 2 == 0 else (planted, lifted)
    lifts = (arch, 0) if index % 2 == 0 else (0, arch)
    return motor(start, y, size, hip=planted + stride * (fraction - .5),
                 feet=feet, lifts=lifts)


def atp(x, y):
    return VGroup(Dot(point(x, y), radius=.22, color=ORANGE).set_opacity(.20),
                  Dot(point(x, y), radius=.115, color=ORANGE))


def direction(x, y, color=PURPLE):
    glow = Ellipse(width=2.14, height=.52, stroke_width=0, fill_color=color,
                   fill_opacity=.42).move_to(point(x, y))
    arrow = Arrow(point(x + .93, y), point(x - .93, y), buff=0, stroke_width=13,
                  color=color, tip_length=.44, max_stroke_width_to_length_ratio=10)
    return VGroup(glow, arrow)


def crowded_cell():
    cell = Ellipse(width=12.7, height=6.65, stroke_color=GREY, stroke_width=3,
                   fill_color="#263E4B", fill_opacity=1)
    filaments = VGroup()
    rng = np.random.default_rng(11)
    for index in range(27):
        a = index * 2.39996
        r = np.sqrt((index + .5) / 28)
        x, y = 5.3 * r * np.cos(a), 1.90 * r * np.sin(a)
        length = rng.uniform(.88, 1.65)
        rod = track(y, x, length, light=.72)
        walker = motor(x, y, .38, color=PURPLE)
        piece = VGroup(rod, walker).rotate(rng.uniform(-.50, .50), about_point=point(x, y))
        center = piece.get_center().copy()

        def drift(mob, dt, center=center, phase=a, speed=rng.uniform(1.9, 3.4)):
            mob.phase += dt * speed
            mob.move_to(center + point(.27 * np.sin(mob.phase), .12 * np.cos(mob.phase + phase)))

        piece.phase = a
        piece.add_updater(drift)
        filaments.add(piece)
    return cell, filaments


class S01Hook(SpokenScene, TitleCard):
    LESSON = "In Vitro Motility and Single-Molecule Imaging"
    TITLE = "Watching Single Motors and Filaments Move"

    def construct(self):
        cell, crowd = crowded_cell()
        question = question_card("Watch one motor?", y=2.70, size=37).shift(RIGHT * .5)
        backing = slab(question.width + .36, question.height + .16, 0, 2.70, "#16252F")
        self.add(cell, crowd)
        self.at("watch one motor")
        self.play(FadeIn(backing), run_time=.18)
        self.play(FadeIn(question), run_time=.32)

        self.at("inside a cell")
        self.play(FadeOut(question), FadeOut(backing), run_time=.30)
        self.at("blur into one average")
        crowd.clear_updaters()
        average = slab(10.6, .72, 0, 0, GREY, .92)
        self.play(FadeOut(crowd, scale=.86), GrowFromCenter(average), run_time=.65)
        average_label = heading("One average", GREY, y=.83)
        self.play(FadeIn(average_label), run_time=.33)

        glass, filament, walker = chamber(), track(), motor(-.65, size=.86, lifts=(0, .26))
        title = fit_text(self.TITLE, max_w=11.7, size=43, min_size=34, font=TITLE_FONT)
        title.move_to(point(0, 2.64))
        self.at("pull purified parts")
        self.play(FadeOut(average_label), FadeOut(average), FadeOut(cell), run_time=.45)
        self.play(FadeIn(glass), GrowFromCenter(filament), FadeIn(walker), run_time=.82)
        self.play(FadeIn(title), run_time=.55)
        self.wait(.50)
        self.play(FadeOut(title), run_time=.38)
        self.finish()


class S02Chamber(SpokenScene):
    def construct(self):
        glass = chamber()
        actin = track()
        walker = motor(-.65, size=.86, lifts=(0, .26))
        self.add(glass, actin, walker)

        self.at("in vitro")
        title = heading("In vitro", BLUE, 39)
        self.play(FadeIn(title), run_time=.55)
        focus = slab(12.95, 3.1, 0, -.03, BLUE, .12).set_z_index(.5)
        actin.set_z_index(1)
        title.set_z_index(1)
        walker.set_z_index(1)
        self.play(FadeIn(focus, shift=UP * .55), run_time=1.3)
        self.play(FadeOut(focus, shift=UP * .55), run_time=1.25)

        self.at("add purified polar tracks")
        tube = track(TUBE_Y, tube=True, light=.17)
        self.play(FadeOut(title), FadeOut(walker), FadeIn(tube, shift=LEFT * .85),
                  actin.animate.become(track(light=.17)), run_time=1.05)
        self.at("actin or microtubules")
        names = VGroup(heading("Actin", YELLOW, 29, y=-.54),
                       heading("Microtubule", YELLOW, 29, y=1.41))
        self.play(FadeIn(names), run_time=.54)
        self.at("two distinct ends")
        ends = VGroup(polarity(), polarity(tube=True, y=TUBE_Y))
        end_marks = VGroup()
        for y in (TRACK_Y, TUBE_Y):
            end_marks.add(Circle(radius=.25, color=YELLOW, stroke_width=5.3,
                                 fill_color=LIQUID, fill_opacity=1).move_to(point(-TRACK_LENGTH / 2, y)))
            end_marks.add(Dot(point(TRACK_LENGTH / 2, y), radius=.25, color=YELLOW))
        end_marks.set_z_index(2)
        self.play(LaggedStart(*[GrowFromCenter(mark) for mark in end_marks], lag_ratio=.20),
                  run_time=.68)
        self.play(FadeIn(ends), run_time=.43)

        self.at("use fluorescence")
        method = heading("Fluorescence or dark-field", TEXT, 31)
        sweep = VGroup(
            slab(.72, 2.38, -5.35, -.24, TEXT, .12),
            slab(.19, 2.38, -5.35, -.24, TEXT, .20),
        )
        self.play(FadeIn(method), FadeIn(sweep), run_time=.48)
        self.play(sweep.animate.shift(RIGHT * 10.7), actin.animate.become(track()),
                  tube.animate.become(track(TUBE_Y, tube=True)), run_time=2.65,
                  rate_func=linear)
        self.play(FadeOut(sweep), run_time=.40)

        self.at("add a tp")
        self.play(FadeOut(method), FadeOut(names), FadeOut(ends), FadeOut(end_marks), run_time=.35)
        fuel = VGroup(atp(5.7, 1.11), atp(5.5, -.24), atp(5.8, -.78))
        fuel_name = heading("ATP", ORANGE, 33, x=4.15, y=2.30)
        self.play(FadeIn(fuel), FadeIn(fuel_name), run_time=.40)
        self.at("watch motion begin")
        step = ValueTracker(0)
        mover = always_redraw(lambda: walk_pose(step.get_value(), -3.55, size=.86))
        self.play(FadeIn(mover), run_time=.30)
        self.play(fuel.animate.shift(LEFT * 3.0), step.animate.set_value(1),
                  run_time=1.28, rate_func=linear)
        self.finish()


class S03Cycle(SpokenScene):
    def construct(self):
        glass, rail = chamber(), track()
        tube = track(TUBE_Y, tube=True)
        fuel = VGroup(atp(2.7, 1.11), atp(2.5, -.24), atp(2.8, -.78))
        fuel_name = heading("ATP", ORANGE, 33, x=4.15, y=2.30)
        walker = walk_pose(1, -3.55, size=.86)
        self.add(glass, rail, tube, fuel, fuel_name, walker)
        self.at("on its track")
        anchor, scale = -1.45, 1.62
        self.play(FadeOut(tube), FadeOut(fuel), FadeOut(fuel_name),
                  Transform(walker, motor(anchor, size=scale, lifts=(.35, 0))),
                  run_time=.90)

        self.at("foot grips")
        cue = heading("Grip", PURPLE, 36)
        self.play(Transform(walker, motor(anchor, size=scale)), FadeIn(cue), run_time=.64)
        self.at("swings while gripping")
        new_cue = heading("Swing", PURPLE, 36)
        self.play(Transform(walker, motor(anchor, size=scale, hip=.45)),
                  swap(cue, new_cue), run_time=.80)
        self.at("lets go")
        cue = heading("Release", PURPLE, 36)
        self.play(Transform(walker, motor(anchor, size=scale, hip=.45, lifts=(.35, 0))),
                  swap(new_cue, cue), run_time=.53)
        self.at("and recocks")
        new_cue = heading("Re-cock", PURPLE, 36)
        fuel = atp(-2.7, 1.52)
        self.play(Transform(walker, motor(anchor, size=scale, hip=.5,
                                        feet=(.28, .57), lifts=(.48, 0))),
                  swap(cue, new_cue), FadeIn(fuel), run_time=.85)
        self.play(FadeOut(fuel, scale=1.65), run_time=.40)

        self.at("one step's work")
        self.play(FadeOut(new_cue), run_time=.38)
        low, high, width = 80, 100, 7.4
        left = -width / 2
        energy = ValueTracker(0)
        meter = slab(width, .50, 0, 1.68, "#334A57")
        ceiling = slab(width * (high - low) / high, .50,
                       left + width * (low + high) / (2 * high), 1.68, ORANGE, .60)

        def filled_meter():
            length = max(.001, width * energy.get_value() / high)
            return slab(length, .38, left + length / 2, 1.68, GREEN)

        fill = always_redraw(filled_meter)
        limit = heading("Energy from one ATP", ORANGE, 32)
        self.play(FadeIn(meter), FadeIn(ceiling), FadeIn(limit), run_time=.7)
        self.add(fill)
        self.at("energy of 1 atp")
        self.play(energy.animate.set_value(37), run_time=2.72, rate_func=linear)

        self.at("force time step")
        formula = heading("Force × step", TEXT, 37)
        self.play(swap(limit, formula), energy.animate.set_value(53), run_time=1.05)
        self.at("about 80 to 100")
        bound = heading("Force × step ≤ about 80–100 pN·nm", TEXT, 37)
        self.play(swap(formula, bound), energy.animate.set_value(low),
                  rate_func=linear, run_time=.60)

        self.at("watching purified parts")
        fill.clear_updaters()
        self.play(FadeOut(bound), FadeOut(fill), FadeOut(meter), FadeOut(ceiling),
                  run_time=.6)
        step = ValueTracker(0)
        walker_target = always_redraw(lambda: walk_pose(step.get_value(), -2.6, size=1.42))
        self.play(ReplacementTransform(walker, walker_target), run_time=.45)
        self.play(step.animate.set_value(3), rate_func=linear, run_time=4.3)
        self.finish()


def myosin_question():
    """The exact prediction frame, used before, during and after the pause."""
    rail = track()
    myosin = motor(MYOSIN_X, size=MYOSIN_SIZE, cargo=True)
    identity = heading("Myosin II", PURPLE, 35, x=-3.44, y=1.05)
    question = question_card(PREDICTION, y=2.70, size=39).shift(RIGHT * .5)
    return rail, myosin, identity, question


class S04Predict(SpokenScene):
    def construct(self):
        glass, rail = chamber(still=True), track()
        step = ValueTracker(0)
        walker = always_redraw(lambda: walk_pose(step.get_value(), -3.85, size=1.28))
        self.add(glass, rail, walker)

        self.at("one foot always grips")
        self.play(step.animate.set_value(1.05), rate_func=linear, run_time=1.58)
        self.at("kites in one")
        walker_name = heading("Kinesin-1 / Myosin V", PURPLE, 35)
        self.play(FadeIn(walker_name), step.animate.set_value(1.62), run_time=.72)
        self.at("walks alone")
        self.play(step.animate.set_value(3.24), rate_func=linear, run_time=1.95)

        self.at("muscle myosin two")
        walker.clear_updaters()
        self.play(FadeOut(walker), FadeOut(walker_name), run_time=.50)
        _, myosin, identity, question = myosin_question()
        tether, legs, body, vesicle = myosin
        # The body and heads arrive before the cargo is shown.
        self.play(FadeIn(legs), FadeIn(body), run_time=.72)
        self.play(FadeIn(identity), run_time=.50)
        braced = motor(MYOSIN_X, size=MYOSIN_SIZE, hip=.62)
        self.play(Transform(VGroup(legs, body), braced), run_time=2.35,
                  rate_func=there_and_back)

        self.at("could one myosin")
        self.play(FadeIn(question), run_time=.68)
        self.at("carry a vesicle")
        target_center = vesicle.get_center()
        pivot = tether.get_start()
        radius = vesicle.width / 2
        vesicle.shift(RIGHT * 2.35 + DOWN * .20)

        def reach_rim(line):
            center = vesicle.get_center()
            line.put_start_and_end_on(pivot, center + radius * normalize(pivot - center))

        reach_rim(tether)
        self.play(FadeIn(tether), FadeIn(vesicle), run_time=.52)
        tether.add_updater(reach_rim)
        self.play(vesicle.animate.move_to(target_center),
                  run_time=self.narration_s + .36 - self.elapsed(), rate_func=rush_into)
        tether.clear_updaters()
        self.finish()


class S05Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.add(chamber(still=True), *myosin_question())
        self.wait(float(os.environ["KX_DURATION"]))


class S06Reveal(SpokenScene):
    def construct(self):
        rail, myosin, identity, question = myosin_question()
        self.add(chamber(still=True), rail, myosin, identity, question)
        self.at("no myosin 2")
        answer = heading("Both feet can lift", RED, 34, x=-3.42, y=2.72)
        self.play(FadeOut(question), run_time=.27)
        lifted = motor(MYOSIN_X, size=MYOSIN_SIZE, cargo=True, lifts=(.39, .45))
        self.play(FadeIn(answer), Transform(myosin, lifted), run_time=.43)
        self.at("a lone molecule")
        self.play(myosin.animate.shift(RIGHT * 1.64 + UP * .52),
                  run_time=1.82, rate_func=linear)
        self.at("works in a crowd")
        self.play(FadeOut(myosin), FadeOut(answer), FadeOut(identity), run_time=.36)
        crowd = VGroup()
        for x in (-2.7, -1.35, 0, 1.35, 2.7):
            anchored = motor(x, size=.56, lifts=(.36, 0), anchor=True).rotate(PI)
            anchored.shift(UP * (TRACK_Y - .085 - anchored.get_top()[1]))
            crowd.add(anchored)
        ensemble = heading("Myosin II ensemble", PURPLE, 35)
        self.play(FadeIn(crowd, shift=UP * .24), FadeIn(ensemble), run_time=.67)
        self.play(rail.animate.shift(RIGHT * 1.05), run_time=1.36, rate_func=linear)
        self.at("catch direction exceptions")
        self.play(FadeOut(crowd), FadeOut(ensemble), run_time=.35)
        tube = track(TUBE_Y, tube=True)
        minus = VGroup(
            heading("−  Pointed", YELLOW, 29, x=-4.05, y=-.69),
            heading("−  Minus", YELLOW, 29, x=-4.05, y=1.25),
        )
        self.play(rail.animate.shift(LEFT * 1.05), FadeIn(tube, shift=LEFT * .6),
                  run_time=.72)
        self.play(FadeIn(minus), run_time=.43)

        self.at("purified myosin 6")
        myosin_vi = heading("Myosin VI", PURPLE, 32, y=-.03)
        actin_arrow = direction(3.78, -.77)
        self.play(FadeIn(myosin_vi), FadeIn(actin_arrow), run_time=.55)
        self.play(actin_arrow.animate.shift(LEFT * 5.25),
                  Indicate(rail[1], color=YELLOW, scale_factor=1.06),
                  run_time=2.38, rate_func=linear)
        self.at("fruit fly kinesin")
        ncd = heading("Fruit-fly kinesin ncd", PURPLE, 32, y=2.36)
        tube_arrow = direction(3.78, 1.21)
        self.play(FadeIn(ncd), FadeIn(tube_arrow), run_time=.51)
        self.play(tube_arrow.animate.shift(LEFT * 5.81),
                  tube[1].animate.set_fill(YELLOW, .43),
                  run_time=4.65, rate_func=linear)
        self.finish()


def soft_spot(x, y, radius, color=GREEN, brightness=1.0):
    """A soft microscope image built from concentric, translucent fills."""
    return VGroup(*[
        Dot(point(x, y), radius=radius * scale, color=color).set_opacity(alpha * brightness)
        for scale, alpha in [(1.15, .07), (1, .22), (.83, .29), (.62, .38), (.36, .44)]
    ])


def cluster(x, y, size=1.0):
    offsets = [(-.61, .28), (-.30, -.40), (-.21, .18),
               (.08, .54), (.17, -.12), (.42, .26), (.53, -.38)]
    return VGroup(*[
        soft_spot(x + dx * size, y + dy * size, .30 * size)
        for dx, dy in offsets
    ])


def droplet(x, y, width, height=None):
    height = height if height is not None else width
    body = Ellipse(width=width, height=height, color=GREEN, stroke_width=2.8,
                   fill_color=GREEN, fill_opacity=.33).move_to(point(x, y))
    core = soft_spot(x, y, min(width, height) * .49, brightness=.44)
    return VGroup(body, core)


class S07Illusions(SpokenScene):
    def construct(self):
        self.add(chamber())
        self.at("still glowing spots")
        left_spot, right_spot = soft_spot(-3.25, .4, 1.3), soft_spot(3.25, .4, 1.3)
        self.play(FadeIn(left_spot, scale=.8), FadeIn(right_spot, scale=.8), run_time=1.05)
        for spot, seed in ((left_spot, 1), (right_spot, 4)):
            bob(spot, amp=.17, speed=2.2, seed=seed)
        self.at("clusters below the microscope's")
        left_spot.clear_updaters()
        dots = cluster(-3.25, .4, 1.28)
        self.play(FadeOut(left_spot), FadeIn(dots), run_time=1.05)
        cluster_name = heading("Cluster", GREEN, 33, x=-3.25)
        self.play(FadeIn(cluster_name), run_time=.40)
        self.at("like liquid droplets")
        right_spot.clear_updaters()
        drop = droplet(3.25, .4, 2.21)
        self.play(FadeOut(right_spot), FadeIn(drop), run_time=.81)
        liquid_name = heading("Liquid droplet", GREEN, 33, x=3.25)
        self.play(FadeIn(liquid_name), run_time=.40)

        self.at("drifting clusters")
        dots2, drop2 = cluster(-1.55, -.16, .91), droplet(5.05, -.16, 1.55)
        self.play(FadeIn(dots2), FadeIn(drop2), run_time=.44)
        self.play(dots.animate.shift(LEFT * .78), dots2.animate.shift(LEFT * 1.18 + UP * .16),
                  drop.animate.shift(LEFT * .65), drop2.animate.shift(LEFT * 1.25 + UP * .30),
                  run_time=1.38, rate_func=linear)
        self.at("unless they relax")
        joined = droplet(3.17, .38, 3.15, 1.76)
        self.play(ReplacementTransform(VGroup(drop, drop2), joined), run_time=.60)
        self.play(Transform(joined, droplet(3.17, .38, 2.60)), run_time=2.30, rate_func=smooth)

        self.at("bleaching fluorescence")
        self.play(FadeOut(dots), FadeOut(dots2), FadeOut(joined),
                  FadeOut(cluster_name), FadeOut(liquid_name), run_time=.42)
        full = soft_spot(0, .22, 1.65)
        self.play(FadeIn(full), run_time=.36)
        flash = Dot(point(0, .22), radius=1.63, color=TEXT).set_opacity(.74)
        dark = Circle(radius=1.64, stroke_color=GREEN, stroke_width=2.0,
                      stroke_opacity=.45, fill_color=LIQUID, fill_opacity=.96).move_to(point(0, .22))
        self.play(FadeIn(flash), run_time=.15)
        self.play(FadeOut(flash), FadeIn(dark), FadeOut(full), run_time=.28)
        self.at("watching glow return")
        recovery = soft_spot(0, .22, 1.53, brightness=.50)
        self.play(FadeIn(recovery), run_time=.9)
        self.at("called frap")
        frap = heading("FRAP", GREEN, 39)
        self.play(FadeIn(frap), run_time=.45)
        self.at("measures turnover")
        newcomers = VGroup(*[
            Dot(point(x, y), radius=.13, color=GREEN)
            for x, y in [(-3.8, .12), (3.8, -.14), (-3.6, 1.42), (3.5, 1.54)]
        ])
        self.play(FadeIn(newcomers), run_time=.34)
        destinations = [(-.76, .32), (.74, -.15), (-.35, 1.13), (.41, .87)]
        self.play(*[dot.animate.move_to(point(*xy)) for dot, xy in zip(newcomers, destinations)],
                  Transform(recovery, soft_spot(0, .22, 1.53)), run_time=1.55, rate_func=linear)
        self.at("unbinding also give")
        self.play(newcomers[0].animate.shift(LEFT * 1.86),
                  newcomers[3].animate.shift(RIGHT * 2.29 + UP * .50),
                  run_time=1.38, rate_func=linear)
        self.finish()


def half_frap():
    center = point(0, .36)
    radius = 1.82
    boundary = Circle(radius=radius, color=GREEN, stroke_width=3,
                      stroke_opacity=.72).move_to(center)
    left = Sector(radius=radius, start_angle=PI / 2, angle=PI,
                  fill_color=GREEN, fill_opacity=.5, stroke_width=0).shift(center)
    right = Sector(radius=radius, start_angle=-PI / 2, angle=PI,
                   fill_color=GREEN, fill_opacity=.5, stroke_width=0).shift(center)
    particles = VGroup(*[
        Dot(center + point(x, y), radius=.12, color=GREEN)
        for x, y in [(-1.15, .40), (-.97, -.59), (-.44, .83), (-.62, -.18),
                     (-1.36, -.25), (-.35, -.88)]
    ])
    return boundary, left, right, particles


class S08Controls(SpokenScene):
    def construct(self):
        self.add(chamber())
        self.at("bleaching half a large spot")
        outline, lit, bleached, inside = half_frap()
        self.add(outline, lit, bleached)
        flash = bleached.copy().set_fill(TEXT, .74)
        self.play(FadeIn(flash), run_time=.25)
        self.play(FadeOut(flash), bleached.animate.set_fill(opacity=.035),
                  FadeIn(inside), run_time=.60)
        name = heading("Half-body FRAP", GREEN, 35)
        self.play(FadeIn(name), run_time=.45)

        self.at("molecules mix inside")
        targets = [(1.19, .59), (.67, -.69), (.58, 1.05),
                   (.85, -.04), (-.42, .08), (-.6, -.76)]
        self.play(*[dot.animate.move_to(point(x, y + .36)) for dot, (x, y) in zip(inside, targets)],
                  lit.animate.set_fill(opacity=.42), bleached.animate.set_fill(opacity=.16),
                  run_time=1.66, rate_func=linear)
        self.at("cross its edge")
        outside = VGroup(Dot(point(3.3, .82), radius=.12, color=GREEN),
                         Dot(point(-3.22, -.17), radius=.12, color=GREEN))
        self.play(FadeIn(outside), run_time=.42)
        self.play(outside[0].animate.move_to(point(2.35, .74)),
                  outside[1].animate.move_to(point(-2.69, -.10)), run_time=1.55, rate_func=linear)
        self.at("faster inside mixing")
        hedge = heading("Favours, not proof", GOLD, 33, x=-4.0, y=.88)
        self.play(FadeIn(hedge), run_time=.55)
        self.play(inside[0].animate.move_to(point(.79, .14)),
                  inside[1].animate.move_to(point(-.18, .57)),
                  inside[3].animate.move_to(point(-.69, -.16)),
                  outside[0].animate.move_to(point(1.64, .60)),
                  lit.animate.set_fill(opacity=.36), bleached.animate.set_fill(opacity=.36),
                  run_time=3.40, rate_func=linear)

        self.at("motor chambers")
        self.play(*[FadeOut(m) for m in (outline, lit, bleached, inside, outside, name, hedge)],
                  run_time=.50)
        rail = track()
        step = ValueTracker(0)
        walker = always_redraw(lambda: walk_pose(step.get_value(), CONTROL_WALK_START, size=1.42))
        self.play(FadeIn(rail), FadeIn(walker), run_time=.70)
        self.play(step.animate.set_value(1), run_time=1.42, rate_func=linear)
        self.at("motors outside the cell")
        location = heading("Outside the cell", TEXT, 35)
        self.play(FadeIn(location), step.animate.set_value(1.9), run_time=1.41, rate_func=linear)
        self.at("low load unless")
        load = heading("Outside the cell, low load", TEXT, 35)
        self.play(swap(location, load), step.animate.set_value(2.2), run_time=.50, rate_func=linear)
        self.play(step.animate.set_value(3.35), run_time=1.92, rate_func=linear)
        self.finish()


def axoneme():
    lanes = [-1.10, -.31, .48, 1.27]
    pairs = VGroup(*[
        VGroup(track(y - .11, -1.65, 6.75, light=.89),
               track(y + .11, -1.65, 6.75, light=.89))
        for y in lanes
    ])
    for pair in pairs:
        for fiber in pair:
            fiber[1].set_stroke(width=12)
    bridges = []
    for x in (-4.0, -2.9, -1.8, -.7, .4):
        bridges.append(VGroup(*[
            Line(point(x, a + .12), point(x + .13, b - .12),
                 color=GREY, stroke_width=9.2)
            for a, b in zip(lanes, lanes[1:])
        ]))
    return pairs, VGroup(*bridges)


def scissors(x, y):
    tip = point(x, y)
    handles = []
    for dx in (-.16, .16):
        handle = Circle(radius=.12, color=RED, stroke_width=3).move_to(tip + point(dx, .35))
        blade = Line(tip + point(dx, .24), tip + point(-dx * .65, -.13),
                     color=RED, stroke_width=4)
        handles.extend([blade, handle])
    return VGroup(*handles)


class S09Axonemes(SpokenScene):
    def construct(self):
        glass, rail = chamber(), track()
        step = ValueTracker(3.35)
        walker = always_redraw(lambda: walk_pose(step.get_value(), CONTROL_WALK_START, size=1.42))
        prior = heading("Outside the cell, low load", TEXT, 35)
        self.add(glass, rail, walker, prior)
        self.at("microscope chambers")
        walker.clear_updaters()
        pairs, bridges = axoneme()
        self.play(FadeOut(walker), FadeOut(prior), FadeOut(rail), run_time=.50)
        self.play(LaggedStart(*[FadeIn(pair, shift=RIGHT * .56) for pair in pairs],
                              lag_ratio=.35), run_time=1.18)
        self.play(LaggedStart(*[FadeIn(bridge) for bridge in bridges], lag_ratio=.20), run_time=.9)

        self.at("summers and gibbons")
        citation = heading("Summers & Gibbons", GOLD, 36)
        self.play(FadeIn(citation), run_time=.54)
        self.at("sea urchin sperm")
        bundle = heading("Sea-urchin sperm axoneme", TEXT, 30, y=1.96)
        specimen = VGroup(pairs, bridges)
        self.play(FadeIn(bundle), specimen.animate.scale(1.10, about_point=point(-1.65, .10)),
                  run_time=1.22)
        self.play(specimen.animate.scale(1 / 1.10, about_point=point(-1.65, .10)),
                  run_time=1.23)

        self.at("enzyme trypsin")
        cutter = scissors(-4.2, 1.36).scale(1.72)
        enzyme = heading("Trypsin", RED, 33, x=3.42, y=1.79)
        self.play(FadeOut(bundle), FadeIn(cutter), run_time=.40)
        self.play(FadeIn(enzyme), run_time=.50)
        self.at("disrupted what resists")
        for x, bridge in zip((-4.0, -2.9, -1.8, -.7, .4), bridges):
            self.play(cutter.animate.move_to(point(x, 1.23)),
                      FadeOut(bridge, scale=.66), run_time=.42)
        self.remove(bridges)
        self.play(FadeOut(cutter), FadeOut(enzyme), run_time=.37)

        self.at("with 0 .1")
        fuel = VGroup(*[atp(x, y).scale(1.57) for x, y in
                        [(5.4, 1.18), (5.69, .43), (5.45, -.40), (4.72, -.82)]])
        amount = heading("0.1 mM ATP", ORANGE, 31, x=3.42, y=1.79)
        self.play(FadeIn(fuel, shift=LEFT * .31), run_time=.48)
        self.at("millimolar atp")
        self.play(FadeIn(amount), fuel.animate.shift(LEFT * .70), run_time=1.20, rate_func=linear)
        self.at("darkfield microscopy")
        self.play(fuel.animate.shift(LEFT * 2.20), run_time=1.58, rate_func=linear)
        self.at("groups of microtubule")
        self.play(FadeOut(fuel), *(p.animate.shift(RIGHT * dx)
                   for p, dx in zip(pairs, (.0, 1.6, 2.05, .38))),
                  run_time=2.72, rate_func=linear)

        self.at("dynein slides microtubules")
        result = heading("Dynein slides doublets", PURPLE, 34)
        self.play(swap(citation, result), FadeOut(amount), run_time=.71)
        self.play(*(p.animate.shift(RIGHT * dx)
                   for p, dx in zip(pairs, (.0, .57, 1.56, .19))),
                  run_time=2.02, rate_func=linear)
        self.finish()


def dynamic_tube(length, peel=0.0):
    left, y = -5.28, -.28
    tip = left + length
    shell = slab(length, .74, left + length / 2, y, YELLOW, .22)
    rails = VGroup(*[
        Line(point(left, y + sign * .36), point(tip, y + sign * .36),
             color=YELLOW, stroke_width=6)
        for sign in (-1, 1)
    ])
    segments = VGroup(*[
        Line(point(x, y - .33), point(x, y + .33), color=YELLOW,
             stroke_width=2, stroke_opacity=.31)
        for x in np.arange(left + .34, tip - .12, .34)
    ])
    opening = Ellipse(width=.44, height=.74, stroke_color=YELLOW, stroke_width=4,
                      fill_color=LIQUID, fill_opacity=1).move_to(point(tip, y))
    tube = VGroup(shell, rails, segments, opening)
    # Separating schematic rails make the shortening tip legible.
    if peel > .01:
        for sign in (-1, 1):
            rail = VMobject().set_points_smoothly([
                point(tip - .1, y + sign * .36),
                point(tip + .37 * peel, y + sign * .46),
                point(tip + .69 * peel, y + sign * (.46 + .37 * peel)),
            ])
            rail.set_stroke(YELLOW, 4.4)
            tube.add(rail)
    return tube


class S10Dynamic(SpokenScene):
    def construct(self):
        self.add(chamber())
        self.at("second in 1984")
        population = VGroup(*[
            track(y, x, length, tube=True, light=.25)
            for y, x, length in [(-1.07, .22, 8.2), (-.63, .08, 9.2),
                                 (.18, -.12, 8.0), (.65, -.43, 6.8),
                                 (1.16, .15, 8.7), (1.58, -.61, 6.5)]
        ])
        length, curl = ValueTracker(7.7), ValueTracker(0)
        specimen = always_redraw(lambda: dynamic_tube(length.get_value(), curl.get_value()))
        self.play(LaggedStart(*[FadeIn(rod, shift=RIGHT * .58) for rod in population],
                              lag_ratio=.18), run_time=1.54)
        self.at("mitchison and kirchner")
        credit = heading("Mitchison & Kirschner, 1984", GOLD, 35)
        self.play(FadeIn(credit), run_time=.60)
        self.play(LaggedStart(*[Indicate(rod, color=YELLOW, scale_factor=1.015) for rod in population],
                              lag_ratio=.23), run_time=2.65)
        self.at("microtubule populations")
        self.play(FadeOut(population), FadeIn(specimen), run_time=1.03)

        self.at("their ends switched")
        title = heading("Dynamic instability", TEXT, 38)
        self.play(swap(credit, title), run_time=.76)
        self.at("steady growth")
        growing = heading("Steady growth", YELLOW, 32, y=1.62)
        self.play(FadeIn(growing), length.animate.set_value(8.53), run_time=.40, rate_func=linear)
        self.play(length.animate.set_value(9.92), run_time=.67, rate_func=linear)
        self.at("rapid shortening")
        shortening = heading("Rapid shortening", YELLOW, 32, y=1.62)
        self.play(swap(growing, shortening), length.animate.set_value(7.81),
                  curl.animate.set_value(.48), run_time=.40, rate_func=linear)
        self.play(length.animate.set_value(5.55), curl.animate.set_value(1),
                  run_time=.43, rate_func=linear)
        self.play(curl.animate.set_value(0), run_time=.40)

        self.at("single purified ends")
        self.play(swap(shortening, growing), length.animate.set_value(6.14),
                  run_time=.40, rate_func=linear)
        self.play(length.animate.set_value(8.9), run_time=1.88, rate_func=linear)
        self.at("those switches directly")
        self.play(swap(growing, shortening), length.animate.set_value(7.22),
                  curl.animate.set_value(.59), run_time=.40, rate_func=linear)
        self.play(length.animate.set_value(6.05), curl.animate.set_value(1),
                  run_time=.28, rate_func=linear)
        self.play(FadeOut(shortening), curl.animate.set_value(0),
                  length.animate.set_value(6.65), run_time=.78, rate_func=linear)
        self.finish()


ROTOR_CENTER = point(-.76, -.13)
ROTATION_STEP = TAU / 3


def needle(angle, color=YELLOW, faded=False):
    start = ROTOR_CENTER - .55 * point(np.cos(angle), np.sin(angle))
    end = ROTOR_CENTER + 2.40 * point(np.cos(angle), np.sin(angle))
    halo = Line(start, end, color=color, stroke_width=29, stroke_opacity=.12 if faded else .25)
    core = Line(start, end, color=color, stroke_width=13, stroke_opacity=.24 if faded else 1)
    return VGroup(halo, core)


class S11Rotary(SpokenScene):
    def construct(self):
        self.add(chamber(overhead=True))
        self.at("third noji and")
        credit = heading("Noji & Yoshida", GOLD, 36)
        base = VGroup(
            Circle(radius=.79, color=BLUE, stroke_width=4,
                   fill_color=BLUE, fill_opacity=.28).move_to(ROTOR_CENTER),
            Dot(ROTOR_CENTER, radius=.55, color=PURPLE),
        )
        landing = ROTOR_CENTER + LEFT * 1.04 + UP * .31
        base.move_to(landing)
        self.play(FadeIn(base), run_time=.67)
        self.play(FadeIn(credit), run_time=.50)
        self.at("fixed a t p")
        synthase = heading("ATP synthase", PURPLE, 33, x=3.71, y=-1.12)
        self.play(base.animate.move_to(ROTOR_CENTER), run_time=1.54)
        self.play(FadeIn(synthase), run_time=.51)
        self.at("fluorescent actin filament")
        rotation = ValueTracker(0)
        active = always_redraw(lambda: needle(rotation.get_value()))
        initial_rod = needle(0)
        self.play(GrowFromPoint(initial_rod, ROTOR_CENTER), run_time=1.61)
        self.remove(initial_rod)
        self.add(active)

        def turn(index, trace=False):
            if trace:
                self.add(needle((index - 1) * ROTATION_STEP, faded=True))
                self.bring_to_front(active)
            fuel = atp(3.76, .80)
            self.play(FadeIn(fuel), run_time=.15)
            self.play(rotation.animate.set_value(index * ROTATION_STEP),
                      FadeOut(fuel, scale=1.7), run_time=.27, rate_func=linear)

        self.at("the heads spun")
        orbit = Circle(radius=2.40, color=BLUE, stroke_width=3.4, stroke_opacity=.57).move_to(ROTOR_CENTER)
        self.play(Create(orbit), run_time=.75)
        turn(1, trace=True)
        self.at("120 degree steps")
        steps = heading("120° steps", YELLOW, 37)
        self.play(swap(credit, steps), run_time=.48)

        one_per = heading("1 ATP per step", ORANGE, 32, x=3.76, y=1.41)
        self.at("one per a t")
        self.play(FadeIn(one_per), run_time=.26)
        for index in (2, 3):
            turn(index, trace=True)
            self.wait(.23)

        self.at("isolated on glass")
        echoes = VGroup(*[
            motor(x, y, .41, color=GREY).set_opacity(.14)
            for x, y in [(-5.34, 1.13), (-4.38, -.84), (-5.24, -.34), (5.16, -.34), (4.96, .38)]
        ])
        self.play(FadeIn(echoes), run_time=.55)
        for index in (4, 5, 6):
            turn(index)
            self.wait(.40)
        self.at("the crowd's average")
        self.play(FadeOut(echoes), run_time=.65)
        self.finish()


class S12End(EndCard):
    LINE = "Watch purified parts under a microscope to see what averages hide."
