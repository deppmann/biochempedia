"""Temperature-sensitive mutants, timed to the supplied Kokoro transcript.

Colour map: GREY for structure, BLUE for cool apparatus, ORANGE for applied heat,
TEAL for yeast and completed divisions, PURPLE for protein, RED for a block,
YELLOW for the cell being followed, GREEN for an open gate, and GOLD for dates.
"""
from bp_parts import *

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
FIELD = "#263B4C"
CELL = "#204652"
TRACK = "#3A586C"
CENTER = np.array([-1.48, 0.20, 0])
GAUGE_X = 5.10
SWITCH_X = 4.11
SWITCH_WIDTH = 1.00
EXECUTION = 0.22
ARREST = 0.71
QUESTION = "Stop now, or finish this lap?"
CARD = {"y": -3.05, "size": 36}
LOCATIONS = [(-4.75, 0.25), (-3.45, 1.84), (-1.45, 0.32),
             (0.28, 1.70), (1.62, 0.15), (-3.14, -1.18), (-0.39, -1.30)]


def p(x, y):
    return np.array([x, y, 0.0])


def label(words, x, y, color=TEXT, size=30):
    return T(words, size, color).move_to(p(x, y))


def panel(width, height, at, color=FIELD, border=TRACK):
    return RoundedRectangle(width=width, height=height, corner_radius=0.23,
                            color=border, stroke_width=2.5, fill_color=color,
                            fill_opacity=1).move_to(at)


def yeast(at, radius=0.50, stage=0.0, color=TEAL):
    """One mother and a resizable bud, with the mother centre fixed."""
    mother = Ellipse(width=2 * radius, height=1.78 * radius, color=color,
                     stroke_width=3, fill_color=CELL, fill_opacity=1).move_to(ORIGIN)
    inner = Arc(radius=radius * 0.68, start_angle=2.0, angle=1.3, color=color,
                stroke_width=1.7).shift(LEFT * radius * 0.055)
    inner.set_stroke(opacity=0.65)
    bud = Circle(radius=0.01, color=color, stroke_width=2.7,
                 fill_color=CELL, fill_opacity=1)
    cell = VGroup(bud, mother, inner).shift(at)
    cell.radius = radius
    set_bud(cell, stage)
    return cell


def set_bud(cell, stage):
    bud, mother, _ = cell
    size = cell.radius * 0.68 * stage
    bud.set_width(max(0.018, 2 * size))
    bud.move_to(mother.get_center() + np.array([cell.radius * 0.73 + size * 0.54,
                                               cell.radius * 0.42 + size * 0.23, 0]))
    bud.set_fill(opacity=min(1, stage * 12))
    bud.set_stroke(opacity=min(1, stage * 12))


def field():
    rim = Ellipse(width=9.95, height=5.43, color=GREY, stroke_width=3,
                  fill_color=FIELD, fill_opacity=1).move_to(CENTER)
    edge = Ellipse(width=9.64, height=5.12, color=TRACK, stroke_width=2).move_to(CENTER)
    return VGroup(rim, edge)


def culture(stages=None):
    stages = stages if stages is not None else [0.68, 0.24, 0.7, 0.92, 0.34, 0.52, 0.18]
    cells = VGroup(*[yeast(p(x, y), 0.73 if i == 2 else 0.56 + 0.06 * (i % 3), stage)
                     for i, ((x, y), stage) in enumerate(zip(LOCATIONS, stages))])
    return cells


def drift_cells(cells, budding=False, lock=None):
    """Let the field drift. A growing cell sheds its bud at the lap boundary."""
    for i, cell in enumerate(cells):
        bob(cell, amp=0.13 + 0.035 * (i % 3), speed=1.0 + 0.17 * (i % 3), seed=i)
        if budding:
            def grow(mob, dt, phase=i * 0.137, speed=0.14 + 0.018 * (i % 3)):
                if lock is not None:
                    final = lock.get_value()
                    if final >= 0.999:
                        set_bud(mob, 1)
                        return
                else:
                    final = 0
                cycle = (phase + mob._bob_t * speed) % 1
                bud = np.clip((cycle - 0.18) / 0.74, 0, 1)
                set_bud(mob, interpolate(bud, 1, final))
            cell.add_updater(grow)
    return cells


def temperature(value, mode=None, x=GAUGE_X):
    """Vertical schematic gauge, or a 25–37 °C scale for the sec1 scene."""
    bottom, top = -1.46, 1.70
    tube = RoundedRectangle(width=0.57, height=4.07, corner_radius=0.28,
                            color=BLUE, stroke_width=3, fill_color=FIELD,
                            fill_opacity=1).move_to(p(x, 0.18))
    bulb = Circle(radius=0.36, color=BLUE, stroke_width=3, fill_color=FIELD,
                  fill_opacity=1).move_to(p(x, -1.95))
    level = ValueTracker(value)
    liquid = Rectangle(width=0.23, height=1, stroke_width=0, fill_opacity=1)
    core = Dot(p(x, -1.95), radius=0.235)

    def fill(mob):
        f = np.clip(level.get_value(), 0, 1)
        y = interpolate(bottom, top, f)
        color = interpolate_color(ManimColor(BLUE), ManimColor(ORANGE), f)
        mob.stretch_to_fit_height(y + 1.95).move_to(p(x, (y - 1.95) / 2)).set_fill(color)
        core.set_fill(color)
    liquid.add_updater(fill, call_updater=True)
    heading = label("Temperature", x, 2.46, BLUE)
    ticks = VGroup(*(Line(p(x + 0.38, y), p(x + 0.57, y), color=GREY, stroke_width=2)
                     for y in np.linspace(bottom, top, 5)))
    gauge = VGroup(tube, bulb, liquid, core, ticks, heading)
    if mode == "sec":
        for words, y, color in [("25 °C", bottom, BLUE), ("37 °C", top, ORANGE)]:
            mark = T(words, 28, color)
            mark.next_to(p(x + 0.67, y), RIGHT, buff=0.07)
            gauge.add(mark)
    return gauge, level


def schematic():
    return scope_tag(size=28, color=TEXT)


def protein(at, failed=False, width=1.45):
    if failed:
        a = Polygon(p(-.73, -.52), p(-.73, .52), p(-.06, .52), p(-.22, .13),
                    p(-.02, -.05), p(-.32, -.52), color=PURPLE, stroke_width=3,
                    fill_color=PURPLE, fill_opacity=.33)
        b = Polygon(p(.12, -.52), p(.39, -.05), p(.19, .13), p(.36, .52),
                    p(.79, .52), p(.79, -.52), color=PURPLE, stroke_width=3,
                    fill_color=PURPLE, fill_opacity=.33)
        return VGroup(a, b).scale_to_fit_width(width).move_to(at)
    body = panel(width, 1.04, at, color="#593D72", border=PURPLE)
    core = RoundedRectangle(width=width * .38, height=.33, corner_radius=.10,
                            stroke_width=0, fill_color=PURPLE, fill_opacity=.9).move_to(at)
    return VGroup(body, core)


def switch_icon():
    at = p(SWITCH_X, .02)
    case = panel(SWITCH_WIDTH, .57, at, color="#593D72", border=PURPLE)
    knob = Dot(at + LEFT * .24, radius=.17, color=PURPLE)
    return VGroup(case, knob)


def gear(at):
    gear_shape = Star(n=9, outer_radius=.38, inner_radius=.27,
                      color=PURPLE, fill_color=PURPLE, fill_opacity=1).move_to(at)
    hole = Dot(at, radius=.105, color=CELL)
    return VGroup(gear_shape, hole)


def phase_point(phase, margin=0):
    angle = TAU * phase - PI / 2
    return CENTER + p((3.95 + margin) * np.cos(angle), (2.25 + margin) * np.sin(angle))


def phase_arc(lo, hi, margin=0, color=TEXT, width=5):
    points = [phase_point(v, margin) for v in np.linspace(lo, hi, 120)]
    return VMobject(color=color, stroke_width=width).set_points_as_corners(points)


def track_section(lo, hi, color):
    phases = np.linspace(lo, hi, 80)
    outside = [phase_point(v, .335) for v in phases]
    inside = [phase_point(v, -.335) for v in phases[::-1]]
    return Polygon(*outside, *inside, stroke_width=0,
                   fill_color=color, fill_opacity=.78)


def phase_arrow(lo, hi, offset, color):
    path = phase_arc(lo, hi, offset, color=color, width=3.5)
    dashes = DashedVMobject(path, num_dashes=max(4, int(30 * (hi - lo))))
    head = Arrow(phase_point(hi - .025, offset), phase_point(hi, offset),
                 color=color, buff=0, tip_length=.17, stroke_width=3.4)
    return VGroup(dashes, head)


def cycle_deck():
    outer = Ellipse(width=8.78, height=5.25, color=GREY, stroke_width=2.5,
                    fill_color=TRACK, fill_opacity=1).move_to(CENTER)
    inner = Ellipse(width=7.02, height=3.74, color=TRACK, stroke_width=2.5,
                    fill_color=FIELD, fill_opacity=1).move_to(CENTER)
    centerline = DashedVMobject(phase_arc(0, 1, color=GREY, width=1.8), num_dashes=38)
    arrows = VGroup(*[Arrow(phase_point(v-.026), phase_point(v), color=GREY, buff=0,
                            stroke_width=2.6, tip_length=.18) for v in [.08, .46, .64, .88]])
    return VGroup(outer, inner, centerline, arrows)


def stage_key():
    items = VGroup()
    for x, name, bud in [(-3.52, "G1", 0), (-1.65, "S", .46), (.08, "Mitosis", 1)]:
        items.add(yeast(p(x, .76), .37, bud), label(name, x + .10, .03, TEXT, 28))
    return items


def station(closed=False):
    at = phase_point(EXECUTION)
    a, b = at + p(-.34, -.08), at + p(.36, .08)
    posts = VGroup(Dot(a, radius=.10, color=GREY), Dot(b, radius=.10, color=GREY))
    lever = Line(a, b if closed else a + p(.06, .70),
                 color=RED if closed else GREEN, stroke_width=8)
    return VGroup(lever, posts)


def arrest_zone():
    return phase_arc(.675, .748, color=RED, width=13)


def cycle_labels(include_arrest=True):
    station_name = label("Execution point", -.28, -.80, PURPLE, 28)
    if include_arrest:
        return VGroup(station_name, label("Arrest point", -3.04, -.80, RED, 28))
    return VGroup(station_name)


def car():
    body = RoundedRectangle(width=.59, height=.30, corner_radius=.07,
                            color=YELLOW, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
    roof = RoundedRectangle(width=.29, height=.19, corner_radius=.05,
                            fill_color=BG, fill_opacity=1, stroke_width=0).shift(UP * .14)
    wheels = VGroup(Dot(p(-.17, -.15), radius=.064, color=BG),
                    Dot(p(.17, -.15), radius=.064, color=BG))
    vehicle = VGroup(body, roof, wheels).scale(1.34)
    return VGroup(track_halo(YELLOW, .50), vehicle)


def track_halo(color, radius):
    return Circle(radius=radius, color=color, stroke_width=2,
                  fill_color=color, fill_opacity=.45)


def breathe_halo(halo):
    halo.age = 0.0

    def glow(mob, dt):
        mob.age += dt
        mob.set_fill(opacity=.49 + .27 * np.sin(3.7 * mob.age))

    halo.add_updater(glow)


def travelling_mark(start, tracker, color, width=14):
    """A stroke behind the moving example shows the part of the lap traversed."""
    mark = phase_arc(start, start + .001, color=color, width=width)
    mark.add_updater(lambda m: m.become(
        phase_arc(start, max(start + .001, tracker.get_value()), color=color, width=width)),
        call_updater=True)
    return mark


def on_track(mob, tracker, margin=0):
    mob.add_updater(lambda m: m.move_to(phase_point(tracker.get_value(), margin)), call_updater=True)
    return mob


def title_field():
    return field(), culture(), temperature(0.16)[0]


class S01Hook(SpokenScene):
    def construct(self):
        dish, cells, gauge = title_field()
        drift_cells(cells)
        self.add(dish, cells, gauge, schematic())
        self.at("study a gene")
        icon = gear(p(*LOCATIONS[2]))
        self.play(GrowFromCenter(icon), run_time=.7)
        self.at("Break it permanently")
        cross = Cross(icon, stroke_color=RED, stroke_width=6)
        self.play(Create(cross), run_time=.55)
        self.at("cells stop growing")
        for cell in cells:
            cell.clear_updaters()
        question = label("?", -1.48, .22, YELLOW, 120)
        self.play(FadeOut(cells), FadeOut(icon), FadeOut(cross), run_time=1.25)
        self.play(GrowFromCenter(question), run_time=.66)
        self.at("You need a switch")
        fresh = drift_cells(culture())
        switch = switch_icon()
        self.play(FadeOut(question), run_time=.30)
        self.play(FadeIn(fresh), run_time=.47)
        self.play(FadeIn(switch), run_time=.48)
        self.play(switch[1].animate.shift(RIGHT * .47), run_time=.65)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Temperature-sensitive mutants"
    TITLE = "Switching Off an Essential Gene With Heat"

    def construct(self):
        dish, cells, gauge = title_field()
        drift_cells(cells)
        scrim = panel(11.82, 2.12, p(-.52, .12), color=BG, border=TRACK)
        scrim.set_fill(opacity=.95)
        title = fit_text(self.TITLE, max_w=11.05, size=47, min_size=38, font=TITLE_FONT).move_to(p(-.52, .29))
        lesson = label(self.LESSON, -.52, -.52, GOLD, 28)
        self.add(dish, cells, gauge, scrim, title, lesson)
        self.wait(self.narration_s)


class S03Switch(SpokenScene):
    def construct(self):
        dish, cells, _ = title_field()
        gauge, temp = temperature(.16)
        lock = ValueTracker(0)
        drift_cells(cells, budding=True, lock=lock)
        switch = switch_icon()
        switch[1].shift(RIGHT * .47)
        self.add(dish, cells, gauge, switch, schematic())
        self.at("builds that switch")
        piece = protein(p(SWITCH_X, .02), width=SWITCH_WIDTH)
        self.play(ReplacementTransform(switch, piece), run_time=.85)
        self.at("into one protein")
        name = place_label(T("Protein", 28, PURPLE), piece, dirs=(DOWN,), buff=.39)
        name.shift(LEFT * .12)
        self.play(FadeIn(name), run_time=.35)
        self.at("At a low temperature")
        cool = label("Cool", GAUGE_X, -2.61, BLUE, 28)
        self.play(FadeIn(cool), run_time=.45)
        self.at("yeast divide normally")
        pulse(piece[0], base=3, amp=.9, speed=2.4)
        self.at("Each bud shows")
        examples = []
        for cue, x, stage, text in [("none in G1", -3.90, 0, "G1"),
                                     ("small in S", -1.65, .44, "S"),
                                     ("large by mitosis", .75, 1, "Mitosis")]:
            self.at(cue)
            sample = yeast(p(x, -2.96), .29, stage)
            tag = label(text, x + .10, -3.53, TEXT, 28)
            examples.extend([sample, tag])
            self.play(GrowFromCenter(sample), FadeIn(tag), run_time=.46)
        self.at("Warm cells")
        restrictive = label("Restrictive", GAUGE_X, -2.61, ORANGE, 28)
        self.play(*[FadeOut(m) for m in examples], swap(cool, restrictive),
                  temp.animate.set_value(1), run_time=1.58)
        self.at("that protein fails")
        piece[0].clear_updaters()
        self.play(ReplacementTransform(piece, protein(p(SWITCH_X, .02), failed=True, width=SWITCH_WIDTH)),
                  run_time=.86)
        self.at("Cells then stall")
        self.play(lock.animate.set_value(1), run_time=2.2, rate_func=smooth)
        self.finish()


class S04TwoTimes(SpokenScene):
    def construct(self):
        dish = field()
        cells = culture([1] * len(LOCATIONS))
        gauge, temp = temperature(1)
        restricted = label("Restrictive", GAUGE_X, -2.61, ORANGE, 28)
        broken = protein(p(SWITCH_X, .02), failed=True, width=SWITCH_WIDTH)
        piece_name = label("Protein", SWITCH_X - .12, -1.03, PURPLE, 28)
        deck, key = cycle_deck(), stage_key()
        self.add(dish, cells, gauge, restricted, broken, piece_name, schematic())
        self.at("Never assume")
        self.play(ReplacementTransform(dish, deck), FadeOut(cells), FadeOut(restricted),
                  FadeOut(broken), FadeOut(piece_name), temp.animate.set_value(.16), run_time=1.45)
        self.play(FadeIn(key), run_time=.58)
        self.at("Picture a car", lead=.44)
        position = ValueTracker(.10)
        runner = on_track(car(), position)
        gate = station()
        self.play(FadeIn(runner), FadeIn(gate), run_time=.52)
        first_lap = travelling_mark(.10, position, GREEN)
        self.add(first_lap)
        self.bring_to_front(runner, gate)
        self.play(position.animate.set_value(.29), run_time=1.20, rate_func=linear)
        self.play(position.animate.set_value(1.12), run_time=1.65, rate_func=linear)
        first_lap.clear_updaters()
        self.at("Close that station")
        shut = station(closed=True)
        self.play(FadeOut(first_lap), ReplacementTransform(gate, shut), temp.animate.set_value(1),
                  position.animate.set_value(1.18), run_time=1.0)
        self.at("stalls later that lap")
        zone = arrest_zone()
        unfuelled = travelling_mark(1.18, position, YELLOW)
        self.add(unfuelled)
        self.bring_to_front(shut, runner)
        self.play(position.animate.set_value(1 + ARREST), run_time=2.5, rate_func=linear)
        unfuelled.clear_updaters()
        runner.set_z_index(1)
        self.play(Create(zone), FadeOut(unfuelled), run_time=.39)
        self.at("The station is")
        names = cycle_labels()
        pulse(shut[0], base=8, amp=2.0, speed=2.35)
        at_station = track_section(EXECUTION - .054, EXECUTION + .054, PURPLE)
        self.play(FadeIn(names[0]), FadeIn(at_station), run_time=.78)
        self.bring_to_front(shut)
        self.at("when the gene is last needed")
        trace = ValueTracker(EXECUTION + .001)
        gap = always_redraw(lambda: track_section(EXECUTION, trace.get_value(), PURPLE))
        self.add(gap)
        self.bring_to_front(at_station, shut, zone, runner)
        self.play(trace.animate.set_value(ARREST), run_time=2.78, rate_func=linear)
        gap.clear_updaters()
        self.at("Where cells collect")
        at_stop = track_section(ARREST - .075, ARREST + .075, RED)
        self.play(FadeOut(gap), FadeOut(at_station), FadeIn(at_stop),
                  FadeIn(names[1]), run_time=1.10)
        self.bring_to_front(zone, runner)
        self.at("or arrest point")
        self.play(FadeOut(at_stop), run_time=1.15)
        self.finish()


FOCUS = .315
COHORT = (.03, .15, .43, .57, .77, .91)


def culture_on_track(phases=COHORT):
    trackers = [ValueTracker(phase) for phase in phases]
    cells = VGroup()
    for tracker in trackers:
        cell = yeast(ORIGIN, .27, .62)
        cell[0].set_fill("#388593")
        cell[1].set_fill("#388593")
        cells.add(on_track(cell, tracker))
    return cells, trackers


def focus_cell(phase=FOCUS):
    t = ValueTracker(phase)
    halo = track_halo(YELLOW, .56)
    focus = VGroup(halo, yeast(ORIGIN, .36, .72, YELLOW))
    return on_track(focus, t), t


def predict_paths():
    return VGroup(phase_arrow(FOCUS + .03, ARREST - .02, -.42, RED),
                  phase_arrow(FOCUS + .027, .992, .43, TEAL))


def prediction_view():
    gauge, _ = temperature(1)
    others, _ = culture_on_track()
    focus, _ = focus_cell()
    return VGroup(cycle_deck(), stage_key(), station(True), cycle_labels(False),
                  gauge, others, focus, predict_paths(), schematic())


class S05PredictQ(SpokenScene):
    def construct(self):
        deck, key = cycle_deck(), stage_key()
        gauge, temp = temperature(1)
        gate = station(True)
        names = cycle_labels()
        zone = arrest_zone()
        old_car = on_track(car(), ValueTracker(ARREST))
        cells, clocks = culture_on_track([a - .22 for a in COHORT])
        focus, clock = focus_cell(.10)
        self.add(deck, key, gauge, gate, names, zone, old_car, schematic())
        self.at("Picture a growing culture")
        open_gate = station()
        self.play(FadeOut(old_car), FadeOut(names[1]), FadeOut(zone), FadeIn(cells),
                  FadeIn(focus), ReplacementTransform(gate, open_gate),
                  temp.animate.set_value(.16), run_time=1.2)
        self.play(*[t.animate.set_value(a - .105) for t, a in zip(clocks, COHORT)],
                  clock.animate.set_value(.16), run_time=2.5, rate_func=linear)
        self.at("We raise the heat")
        self.play(*[t.animate.set_value(a - .02) for t, a in zip(clocks, COHORT)],
                  clock.animate.set_value(.257), run_time=1.65, rate_func=linear)
        self.at("cell passes the execution point")
        self.play(*[t.animate.set_value(a) for t, a in zip(clocks, COHORT)],
                  clock.animate.set_value(FOCUS), temp.animate.set_value(1),
                  ReplacementTransform(open_gate, station(True)), run_time=1.65)
        paths = predict_paths()
        q = question_card(QUESTION, **CARD)
        self.at("Does it stop")
        self.play(Create(paths[0]), FadeIn(q), run_time=1.0)
        self.at("or finish this division")
        self.play(Create(paths[1]), run_time=1.2)
        breathe_halo(focus[0])
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = QUESTION
    CARD = CARD
    SECONDS = 4.5

    def backdrop(self):
        return prediction_view()

    def construct(self):
        world = self.backdrop()
        breathe_halo(world[6][0])
        self.add(world, question_card(self.QUESTION, **self.CARD))
        box = RoundedRectangle(width=5.10, height=.26, corner_radius=.10,
                               color=GREY, stroke_width=2.5, fill_color=FIELD,
                               fill_opacity=1).move_to(p(-.5, -3.55))
        self.add(box)
        bar = Rectangle(width=4.90, height=.155, stroke_width=0,
                        fill_color=GOLD, fill_opacity=1).move_to(box)
        self.play(GrowFromEdge(bar, LEFT), run_time=self.SECONDS, rate_func=linear)


class S07PredictAnswer(SpokenScene):
    def construct(self):
        world = prediction_view()
        deck, key, gate, names, gauge, cohort, focus, paths, scope = world
        q = question_card(QUESTION, **CARD)
        self.add(*world, q)
        focus.clear_updaters()
        clock = ValueTracker(FOCUS)
        on_track(focus, clock)
        self.at("It finishes this lap")
        self.play(FadeOut(paths[0]), FadeOut(q), run_time=.40)
        lap = travelling_mark(FOCUS, clock, TEAL, 18)
        self.add(lap)
        self.bring_to_front(focus)
        self.play(clock.animate.set_value(1), run_time=2.92, rate_func=linear)
        lap.clear_updaters()
        daughter = yeast(phase_point(1) + RIGHT * .32, .29, 0, YELLOW)
        self.play(GrowFromCenter(daughter), FadeOut(paths[1]), run_time=.65)
        set_bud(focus[1], 0)
        self.at("Only on the next lap")
        zone = arrest_zone()
        arrest_label = cycle_labels()[1]
        next_lap = travelling_mark(1, clock, YELLOW, 18)
        self.add(next_lap)
        self.bring_to_front(focus, daughter)
        self.play(clock.animate.set_value(1 + ARREST), FadeOut(daughter), FadeOut(lap),
                  run_time=2.55, rate_func=linear)
        next_lap.clear_updaters()
        self.play(Create(zone), FadeOut(next_lap), run_time=.30)
        self.play(FadeIn(arrest_label), run_time=.37)
        self.at("Follow single cells")
        for cell in cohort:
            cell.clear_updaters()
        self.play(FadeOut(focus), FadeOut(cohort), run_time=.35)
        live, clocks = culture_on_track()
        self.play(FadeIn(live), run_time=.48)
        self.at("those past the station finish")
        eligible = [i for i, start in enumerate(COHORT) if start > EXECUTION]
        for i in eligible:
            live[i].set_stroke(TEAL, width=4.0)
            live[i][1].set_fill(TEAL, opacity=.92)
            live[i][0].set_fill(TEAL, opacity=.92)
            live[i].scale(1.32)
        self.play(*[clocks[i].animate.set_value(.94 + j * .037) for j, i in enumerate(eligible)],
                  run_time=1.67, rate_func=linear)
        self.at("those before it stall")
        earlier = [i for i, start in enumerate(COHORT) if start < EXECUTION]
        for i in earlier:
            live[i][0].set_fill(RED, opacity=.85)
            live[i][1].set_fill(RED, opacity=.85)
            live[i].scale(1.52)
        self.play(*[clocks[i].animate.set_value(ARREST + (j - .5) * .04)
                    for j, i in enumerate(earlier)], run_time=1.75, rate_func=linear)
        for i in earlier:
            live[i].set_stroke(RED, width=4)
        self.at("So the fraction that finish")
        arc = phase_arc(EXECUTION, 1, .45, color=TEAL, width=11)
        end = Arrow(phase_point(EXECUTION, .45), phase_point(EXECUTION, .19),
                    color=TEAL, buff=0, tip_length=.13, stroke_width=3)
        tag = caption("Fraction that finishes", 32, TEAL, y=-3.28)
        self.play(FadeOut(live), Create(arc), run_time=2.0)
        self.play(GrowArrow(end), FadeIn(tag), run_time=.56)
        self.at("Switch an essential protein")
        self.play(FadeOut(tag), arc.animate.set_stroke(width=18), run_time=1.17)
        self.play(arc.animate.set_stroke(width=9), run_time=1.19)
        self.at("and how cells stall")
        signal = phase_arc(ARREST - .083, ARREST + .083, color=RED, width=30)
        self.play(Create(signal), run_time=1.0)
        self.play(FadeOut(signal), FadeOut(arc), FadeOut(end), run_time=1.45)
        self.finish()


def pathway(y, block=None):
    xs = (1.82, 3.62, 5.42)
    dots = VGroup(*[Dot(p(x, y), radius=.22, color=GREY) for x in xs])
    links = VGroup(*[Arrow(p(a + .29, y), p(b - .31, y), buff=0,
                           color=TEXT, stroke_width=3.8, tip_length=.15)
                     for a, b in zip(xs, xs[1:])])
    stop = Line(p(xs[block], y - .37), p(xs[block], y + .37),
                color=RED, stroke_width=7) if block is not None else VGroup()
    if block is not None:
        dots[block].set_fill(RED)
    return VGroup(links, dots, stop)


class S08Limits(SpokenScene):
    def construct(self):
        deck, key, gate, names, zone = cycle_deck(), stage_key(), station(True), cycle_labels(), arrest_zone()
        gauge, _ = temperature(1)
        self.add(deck, key, gate, names, zone, gauge, schematic())
        self.at("Two traps can mislead")
        compact = VGroup(deck, gate, zone)
        compact_scale, compact_shift = .65, LEFT * 2.30
        self.play(FadeOut(key), FadeOut(names), FadeOut(gauge), run_time=.30)
        self.play(compact.animate.scale(compact_scale, about_point=CENTER).shift(compact_shift),
                  run_time=.75)
        small_gauge, temp = temperature(1, x=-.05)
        right = panel(5.08, 5.18, p(3.945, .15))
        self.play(FadeIn(small_gauge), FadeIn(right), run_time=.70)
        self.at("stalled cells show")
        cluster = VGroup(*[yeast(CENTER + compact_shift
                                  + (phase_point(ARREST + k * .057) - CENTER) * compact_scale,
                                  .23, .85, RED) for k in (-1, 0, 1)])
        top = label("Arrest point", 3.88, 1.70, RED, 33)
        self.play(FadeIn(cluster), FadeIn(top), run_time=.66)
        closeup = VGroup(*[yeast(p(2.44 + i * 1.37, .02), .49, .85, RED)
                           for i in range(3)])
        for cell in closeup:
            cell[0].set_fill("#783F45")
            cell[1].set_fill("#783F45")
        self.play(TransformFromCopy(cluster, closeup), run_time=1.3)
        self.play(closeup.animate.shift(DOWN * .38), run_time=1.22)
        self.at("Track single cells")
        timing = label("Track cells or pulse heat", 3.88, 1.70, ORANGE, 28)
        self.play(swap(top, timing), FadeOut(cluster), FadeOut(closeup),
                  temp.animate.set_value(.13), run_time=.63)
        heat_windows = VGroup()
        for i in range(2):
            heat = RoundedRectangle(width=1.22, height=1.10, corner_radius=.14,
                                    color=ORANGE, stroke_width=2.5, fill_color=ORANGE,
                                    fill_opacity=.75).move_to(p(2.94 + 1.78 * i, .08))
            self.play(temp.animate.set_value(1), GrowFromEdge(heat, DOWN), run_time=.56)
            self.play(temp.animate.set_value(.13), heat.animate.set_fill(opacity=.27), run_time=.52)
            heat_windows.add(heat)
        self.at("Second a screen's count")
        findings = label("Screen yield", 3.88, 1.70, TEAL, 32)
        bins = VGroup(*[panel(.83, .55, p(2.44 + .96 * i, .56),
                              color="#3F9197", border=TEAL) for i in range(4)])
        missed = VGroup(*[panel(.53, .45, p(2.02 + .62 * i, -.73),
                                color="#546875", border=GREY) for i in range(7)])
        missed.set_opacity(.73)
        not_found = label("Not found", 3.88, -1.57, TEXT, 28)
        self.play(FadeOut(heat_windows), swap(timing, findings),
                  LaggedStart(*[GrowFromEdge(b, DOWN) for b in bins], lag_ratio=.42),
                  run_time=2.03)
        self.at("not every gene needed")
        self.play(LaggedStart(*[GrowFromEdge(m, DOWN) for m in missed], lag_ratio=.36),
                  FadeIn(not_found), run_time=1.85)
        self.at("A double mutant looks")
        row1, row2 = pathway(.75, 0), pathway(-.80, 1)
        first = yeast(p(1.82, 1.45), .27, .33)
        second = yeast(p(3.62, -.10), .27, .75)
        singles = label("Single mutants", 3.88, 1.96, TEXT, 31)
        self.play(FadeOut(bins), FadeOut(missed), FadeOut(not_found), swap(findings, singles),
                  run_time=.65)
        self.play(FadeIn(row1), FadeIn(first), run_time=.47)
        self.play(FadeIn(row2), FadeIn(second), run_time=.52)
        self.at("blocks earlier")
        merged = yeast(p(1.82, .62), .31, .33, YELLOW)
        double = label("Double mutant", 3.88, 1.96, YELLOW, 31)
        ordered = pathway(-.13, 0)
        self.play(FadeOut(row2), ReplacementTransform(row1, ordered),
                  ReplacementTransform(VGroup(first, second), merged), swap(singles, double),
                  run_time=1.0)
        self.at("order steps")
        self.play(Indicate(ordered[0], color=TEAL), run_time=1.45)
        pulse(ordered[2], base=7, amp=1.4, speed=2.2)
        self.finish()


class S09UnlockedCdc(SpokenScene):
    def construct(self):
        self.at("With those guards")
        dish = field()
        gauge, temp = temperature(.16)
        lock = ValueTracker(0)
        rows = VGroup()
        stages = (0, .45, 1)
        for i, y in enumerate([1.62, .24, -1.18]):
            row = VGroup(*[yeast(p(x, y), .46, (.15 + .22 * (i + j)) % 1)
                           for j, x in enumerate([-4.01, -2.42, -.82, .78])])
            for j, cell in enumerate(row):
                bob(cell, amp=.11 + .015 * j, speed=1.7, seed=j + 3 * i)
                def grow(mob, dt, target=stages[i], start=(i * .32 + j * .237) % 1):
                    live = np.clip(((start + .18 * mob._bob_t) % 1 - .13) / .78, 0, 1)
                    set_bud(mob, interpolate(live, target, lock.get_value()))
                cell.add_updater(grow)
            rows.add(row)
        self.add(dish, gauge, schematic())
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=.35), run_time=1.55)
        self.at("In 1970")
        date = label("1970  Hartwell, Culotti & Reid", -1.48, 3.31, GOLD, 34)
        self.play(FadeIn(date), run_time=.6)
        self.at("budding yeast")
        species = label("Saccharomyces cerevisiae", -1.48, -3.13, TEXT, 31)
        self.play(FadeIn(species), run_time=.52)
        self.at("They called them")
        cdc = label("cdc  •  cell division cycle", -1.48, -3.13, TEAL, 31)
        self.play(swap(species, cdc), run_time=.75)
        self.at("At a higher temperature")
        self.play(temp.animate.set_value(1), run_time=1.0)
        self.at("stopped with one uniform shape")
        self.play(lock.animate.set_value(1), run_time=1.92)
        self.finish()


def secretory_cell():
    return yeast(p(-1.65, .28), 2.22, .38)


def vesicle(at, radius=.14):
    outline = Circle(radius=radius, color=TEAL, stroke_width=2.5,
                     fill_color="#487C85", fill_opacity=1).move_to(at)
    cargo = Dot(at, radius=radius * .45, color=YELLOW)
    return VGroup(outline, cargo)


def secretory_traffic(temp):
    cargo = VGroup()
    for i in range(15):
        m = vesicle(ORIGIN, .22 if i % 2 == 0 else .17)
        def transport(mob, dt, j=i):
            mob.age += dt
            time = (mob.age * .30 + j * .137) % 1
            angle = TAU * ((j * .61803399) % 1)
            ray = p(np.cos(angle), .84 * np.sin(angle))
            if temp.get_value() < .96:
                r = .24 + 2.55 * time
                mob.move_to(p(-1.65, .28) + ray * r)
                mob[0].set_stroke(opacity=float(np.clip((.86 - time) * 16, 0, 1)))
                mob[0].set_fill(opacity=float(np.clip((.86 - time) * 16, 0, 1)))
                mob[1].set_opacity(float(np.clip((1 - time) * 12, 0, 1)))
            else:
                if mob.warmed_at is None:
                    mob.warmed_at = mob.age
                since_heat = mob.age - mob.warmed_at
                trapped_radius = .45 + .26 * (j % 5)
                if j < 7:
                    visible = 1.0
                    r = trapped_radius * min(1, .40 + since_heat * .60)
                else:
                    time_from_formation = since_heat - .42 * (j - 7)
                    visible = float(np.clip(time_from_formation * 4, 0, 1))
                    r = trapped_radius * np.clip(time_from_formation * .72, .09, 1)
                mob.move_to(p(-1.65, .28) + ray * r
                            + p(.08 * np.sin(2.2 * mob.age + j), .08 * np.cos(2.4 * mob.age + j)))
                mob[0].set_stroke(opacity=visible).set_fill(opacity=visible)
                mob[1].set_opacity(visible)
        m.age = i * .095
        m.warmed_at = None
        m.add_updater(transport, call_updater=True)
        cargo.add(m)
    return cargo


def density_tube():
    center = p(-3.70, .20)
    outline = RoundedRectangle(width=1.90, height=3.30, corner_radius=.35,
                               color=GREY, stroke_width=3.5,
                               fill_color=CELL, fill_opacity=1).move_to(center)
    layers = VGroup(*[RoundedRectangle(width=1.57, height=.44, corner_radius=.10,
                                       stroke_width=0, fill_color=TEAL, fill_opacity=.10 + i * .085)
                       .move_to(center + p(0, .94 - i * .55)) for i in range(5)])
    particles = VGroup(*[Dot(center + p(.60 * np.sin(2.4 * i), 1.09 - (i % 12) * .19),
                             radius=.047, color=YELLOW) for i in range(32)])
    return VGroup(outline, layers, particles)


def groups_grid():
    return VGroup(*[panel(.42, .35, p(-1.12 + (i % 6) * .53, 1.22 - (i // 6) * .58),
                          color=CELL, border=TEAL) for i in range(23)])


class S10UnlockedSec(SpokenScene):
    def construct(self):
        self.at("In 1979")
        dish, cell = field(), secretory_cell()
        gauge, temp = temperature(0, "sec")
        date = label("1979  Novick & Schekman", -1.48, 3.30, GOLD, 33)
        self.add(dish, cell, gauge, schematic())
        self.play(FadeIn(date), run_time=.68)
        self.at("reported Sec1")
        sec = label("sec1", -1.48, -3.12, PURPLE, 34)
        self.play(FadeIn(sec), run_time=.50)
        self.at("yeast mutant growing")
        traffic = secretory_traffic(temp)
        self.add(traffic)
        self.at("At 37 degrees")
        self.play(temp.animate.set_value(1), run_time=1.48)
        self.at("keeps making secretory enzymes")
        blocked = label("Enzymes trapped", -1.48, -3.12, RED, 33)
        self.play(swap(sec, blocked), run_time=.65)
        self.at("In 1980")
        next_date = label("1980  Novick, Field & Schekman", -1.48, 3.30, GOLD, 33)
        tube = density_tube()
        for m in traffic:
            m.clear_updaters()
        self.play(ReplacementTransform(cell, tube[0]), FadeOut(traffic),
                  FadeOut(blocked), swap(date, next_date), run_time=1.1)
        self.play(FadeIn(tube[1]), FadeIn(tube[2]), run_time=.77)
        self.at("188 clones")
        clones = label("188 clones", -3.70, -3.12, TEXT, 32)
        self.play(FadeIn(clones), run_time=.60)
        self.play(tube[2].animate.shift(DOWN * .31), run_time=1.4)
        self.at("23 complementation groups")
        bins = groups_grid()
        groups = label("23 complementation groups", -.08, -1.04, TEAL, 28)
        screen = label("Screen yield", -.02, 1.89, TEXT, 30)
        arrow = Arrow(p(-2.55, .40), p(-1.47, .40), buff=0, tip_length=.20,
                      color=GREY, stroke_width=3.2)
        self.play(GrowArrow(arrow), run_time=.45)
        self.play(LaggedStart(*[FadeIn(b) for b in bins], lag_ratio=.06),
                  FadeIn(groups), FadeIn(screen), run_time=1.60)
        self.at("roughly one gene")
        gene = label("About one gene per group", .20, -3.12, TEXT, 28)
        self.play(FadeIn(gene), run_time=.55)
        self.at("mutants ordered")
        ordered_title = label("1981  Double mutants", -1.48, 3.30, GOLD, 34)
        chain = pathway(.25)
        chain.shift(LEFT * 5.1)
        self.play(FadeOut(clones), FadeOut(tube), FadeOut(groups), FadeOut(gene),
                  FadeOut(screen), FadeOut(arrow), swap(next_date, ordered_title), run_time=.70)
        self.play(ReplacementTransform(bins, chain), run_time=1.10)
        self.finish()


def pupa():
    base = Ellipse(width=5.85, height=2.40, color=GREY, stroke_width=3.9,
                   fill_color=CELL, fill_opacity=1).move_to(p(-1.48, .84))
    cap = Arc(radius=1.18, start_angle=-.78, angle=1.56,
              color=TEAL, stroke_width=3.4).stretch(.40, dim=0).move_to(p(-3.62, .84))
    segments = VGroup(*[Arc(radius=.88, start_angle=-.90, angle=1.8,
                            color=TEAL, stroke_width=2.8).stretch(.42, dim=0)
                        .stretch(1.39 - .12 * i, dim=1).move_to(p(-2.65 + i * .70, .84))
                        for i in range(5)])
    tips = VGroup(*[Line(p(-4.15, y), p(-4.56, y + sign * .17),
                         color=GREY, stroke_width=3) for y, sign in [(1.2, 1), (.47, -1)]])
    return VGroup(base, cap, segments, tips)


def pupal_timeline():
    y = -1.35
    x0, x1 = -4.55, 1.60
    axis = Line(p(x0, y), p(x1, y), color=GREY, stroke_width=3)
    ticks = VGroup(*[Line(p(x, y-.10), p(x, y+.10), color=GREY, stroke_width=3)
                     for x in [x0, x1]])
    ends = VGroup(label("0", x0, -.92, TEXT, 28), label("14 hours", x1, -.92, TEXT, 28))
    t = ValueTracker(0)
    cursor = Dot(radius=.093, color=BLUE)
    cursor.add_updater(lambda m: m.move_to(p(interpolate(x0, x1, t.get_value()), y)),
                       call_updater=True)
    return VGroup(axis, ticks, ends, cursor), t


def skin_patch():
    cells = VGroup()
    for j in range(3):
        for i in range(7):
            at = p(-4.35 + .89 * i + .20 * (j % 2), 1.59 - .98 * j)
            cells.add(RegularPolygon(n=6, radius=.40, color=GREY, stroke_width=2.5,
                                     fill_color=CELL, fill_opacity=1).move_to(at))
    return cells


class S11UnlockedNotch(SpokenScene):
    def construct(self):
        self.at("Heat switches work")
        dish, fly = field(), pupa()
        gauge, temp = temperature(.14)
        self.add(dish, gauge, schematic())
        self.play(DrawBorderThenFill(fly), run_time=1.92)
        bob(fly, amp=.21, speed=1.75)
        self.at("In 1990")
        date = label("1990  Hartenstein & Posakony", -1.48, 3.31, GOLD, 33)
        self.play(FadeIn(date), run_time=.55)
        self.at("fly pupae carrying")
        fly_name = label("Fly pupa", -1.48, -3.13, TEXT, 29)
        self.play(FadeIn(fly_name), run_time=.54)
        self.at("version of notch")
        notch = label("Temperature-sensitive Notch", -1.48, -3.13, PURPLE, 31)
        self.play(swap(fly_name, notch), run_time=.80)
        self.at("Pulses between")
        axis, time = pupal_timeline()
        self.play(FadeOut(notch), FadeIn(axis), run_time=.62)
        self.play(time.animate.set_value(.19), run_time=.85, rate_func=linear)
        timeline = axis[0]
        for lo, hi in [(.19, .31), (.56, .71)]:
            self.play(time.animate.set_value(lo), run_time=.39, rate_func=linear)
            window = Line(timeline.point_from_proportion(lo), timeline.point_from_proportion(hi),
                          color=ORANGE, stroke_width=8).shift(UP * .18)
            self.play(Create(window), temp.animate.set_value(1), time.animate.set_value(hi),
                      run_time=.89, rate_func=linear)
            self.play(temp.animate.set_value(.14), run_time=.36)
        self.at("for chosen windows")
        self.play(time.animate.set_value(1), run_time=1.16, rate_func=linear)
        self.at("Extra bristle precursors")
        fly.clear_updaters()
        skin = skin_patch()
        self.play(FadeOut(axis), *[FadeOut(m) for m in self.mobjects
                                  if isinstance(m, Line) and m.get_color() == ManimColor(ORANGE)],
                  ReplacementTransform(fly, skin), run_time=.88)
        dots = VGroup()
        bristles = VGroup()
        for i in [2, 5, 9, 12, 16, 19]:
            spot = skin[i].get_center()
            dots.add(Dot(spot, color=YELLOW, radius=.143))
            bristles.add(ArcBetweenPoints(spot, spot + p(.31, .63), angle=-.7,
                                          color=YELLOW, stroke_width=4.4))
        precursor = label("Extra bristle precursors", -1.48, -3.13, YELLOW, 31)
        affected = [skin[i] for i in [2, 5, 9, 12, 16, 19]]
        mark_fates = [AnimationGroup(GrowFromCenter(dot), cell.animate.set_fill("#776044"))
                      for dot, cell in zip(dots, affected)]
        self.play(LaggedStart(*mark_fates, lag_ratio=.35), FadeIn(precursor), run_time=2.47)
        self.at("So heat timing reveals")
        self.play(LaggedStart(*[Create(b) for b in bristles], lag_ratio=.43), run_time=2.34)
        for i, bristle in enumerate(bristles):
            pulse(bristle, base=4.4, amp=1.2, speed=1.8 + .19 * i)
        self.finish()


class S12End(EndCard):
    LINE = "Switch an essential protein off with heat; read when it acts."
