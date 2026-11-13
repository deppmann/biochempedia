"""A Race Inside the Body.

COLOR MAP
  TEAL = microbes and their computed population curves
  GOLD = antibody defense and memory cells
  RED  = disease-causing/pathogen warning
  GREY = clinics, axes, and de-emphasized comparisons

The race plot is computed from doubling until the defense day, followed by
exponential decline.  It is a deliberately schematic relative scale.
"""
from types import SimpleNamespace

import numpy as np

from bp_parts import *  # noqa: F401,F403


SKIN = "#E8B98E"


def mother_icon(color=TEXT):
    """A compact person icon, used only to compare the two clinic columns."""
    head = Circle(radius=0.105, stroke_width=0, fill_color=color, fill_opacity=1)
    body = Triangle(stroke_width=0, fill_color=color, fill_opacity=1).scale(0.22)
    body.next_to(head, DOWN, buff=0.02)
    return VGroup(head, body)


def clinic_world():
    """The carried Vienna-clinic picture used throughout s01."""
    panels = TwoPanel("First Clinic\ndoctors + students", "Second Clinic\nmidwives",
                      colors=(GREY, GREY), top=2.7, bottom=-2.0, size=28)
    panels.left_frame.layout_ok = True  # labels and icons intentionally sit within the building outline
    panels.right_frame.layout_ok = True
    first = VGroup(*[mother_icon() for _ in range(8)]).arrange_in_grid(2, 4, buff=0.27)
    second = VGroup(*[mother_icon() for _ in range(8)]).arrange_in_grid(2, 4, buff=0.27)
    first.move_to([-3.25, 0.25, 0])
    second.move_to([3.25, 0.25, 0])
    year = M("1846", 38, TEXT).move_to([0, 3.35, 0])
    return SimpleNamespace(group=VGroup(panels, first, second, year), panels=panels,
                           first=first, second=second, year=year)


def hands_pair(scale=1.0):
    palms = VGroup(
        RoundedRectangle(width=0.72, height=0.9, corner_radius=0.25,
                         stroke_color=SKIN, stroke_width=4, fill_color=SKIN,
                         fill_opacity=0.22).rotate(-0.16),
        RoundedRectangle(width=0.72, height=0.9, corner_radius=0.25,
                         stroke_color=SKIN, stroke_width=4, fill_color=SKIN,
                         fill_opacity=0.22).rotate(0.16),
    ).arrange(RIGHT, buff=0.15)
    fingers = VGroup(*[
        Line([-0.48 + i * 0.22, 0.23, 0], [-0.53 + i * 0.22, 0.72, 0],
             color=SKIN, stroke_width=6) for i in range(5)
    ])
    g = VGroup(palms, fingers).scale(scale)
    return g


def microbe(radius=0.36, antigen=True):
    """A schematic microbe dot with one recognizable surface bump."""
    core = Circle(radius=radius, stroke_color=TEAL, stroke_width=5,
                  fill_color=TEAL, fill_opacity=0.28)
    spots = VGroup(*[
        Dot(core.get_center() + radius * np.array([np.cos(a), np.sin(a), 0]) * 0.42,
            radius=radius * 0.09, color=TEAL)
        for a in (0.4, 2.4, 4.2)
    ])
    g = VGroup(core, spots)
    if antigen:
        bump = RoundedRectangle(width=radius * 0.48, height=radius * 0.34,
                                corner_radius=0.07, stroke_color=TEAL,
                                stroke_width=3, fill_color=TEAL, fill_opacity=0.8)
        bump.move_to(core.get_right() + RIGHT * radius * 0.12)
        g.add(bump)
        g.antigen = bump
    return g


def antibody(height=0.45):
    stem = Line(ORIGIN, UP * height * 0.48, color=GOLD, stroke_width=5)
    arms = VGroup(
        Line(UP * height * 0.44, UP * height + LEFT * height * 0.42,
             color=GOLD, stroke_width=5),
        Line(UP * height * 0.44, UP * height + RIGHT * height * 0.42,
             color=GOLD, stroke_width=5),
    )
    return VGroup(stem, arms)


def memory_cell(star=True):
    ring = Circle(radius=0.48, stroke_color=GOLD, stroke_width=6,
                  fill_color=GOLD, fill_opacity=0.12)
    inner = Star(n=5, outer_radius=0.20, inner_radius=0.09, color=GOLD,
                 fill_color=GOLD, fill_opacity=0.85) if star else Dot(radius=0.18, color=GOLD)
    return VGroup(ring, inner)


def calendar_icon():
    box = RoundedRectangle(width=1.2, height=1.0, corner_radius=0.12,
                           stroke_color=GREY, stroke_width=3)
    top = Line(box.get_left() + UP * 0.22, box.get_right() + UP * 0.22,
               color=GREY, stroke_width=3)
    pages = VGroup(*[Line([-0.35, y, 0], [0.35, y, 0], color=GREY, stroke_width=2)
                     for y in (-0.05, -0.25)]).move_to(box)
    return VGroup(box, top, pages)


def race_value(t, start=1.0, defense_day=7.0):
    """Computed model: daily doubling, then exponential fall after defense arrives."""
    t = float(t)
    peak = start * (2.0 ** defense_day)
    return start * (2.0 ** t) if t <= defense_day else peak * np.exp(-1.25 * (t - defense_day))


def defense_fraction(day, defense_day=7.0, baseline=0.0):
    return baseline + (1.0 - baseline) * np.clip((day - (defense_day - 2.0)) / 2.0, 0.0, 1.0)


def race_world(day=0.0, start=1.0, defense_day=7.0, baseline=0.0,
               curve="live", ghost_first=False):
    """Build the same race world at the same scale and position in every race scene."""
    field = RoundedRectangle(width=8.65, height=5.25, corner_radius=0.20,
                             stroke_width=0, fill_color=TEAL, fill_opacity=0.46)
    field.move_to([-1.85, 0.20, 0]).set_z_index(-2)
    field.layout_ok = True
    P = Plot(box=(-5.85, 2.15, -1.85, 2.35), xr=(0, 9), yr=(0, 145),
             xticks=[0, 3, 7, 9], yticks=[], xlabel="days",
             ylabel="microbes (relative, schematic scale)", label_size=26)
    tracker = ValueTracker(day)
    mote_points = [(-5.2, 1.5, 0), (-4.8, 0.25, 0), (-4.2, -0.7, 0),
                   (-3.7, 1.25, 0), (-3.0, 0.8, 0), (-2.6, -0.85, 0),
                   (-1.9, 1.55, 0), (-1.7, -1.0, 0), (-1.0, 0.35, 0),
                   (-0.5, 1.6, 0), (0.0, -1.05, 0), (0.8, -0.4, 0),
                   (1.2, 1.55, 0), (1.55, 0.9, 0)]
    motes = VGroup(*[Dot(radius=0.12, color=TEAL).set_opacity(0.58).move_to(p)
                     for p in mote_points])
    for i, mote in enumerate(motes):
        bob(mote, amp=0.38, speed=1.35 + 0.13 * i, seed=i)
    motes.set_z_index(-1)
    pieces = VGroup(field, motes, P)
    if ghost_first:
        pieces.add(P.curve(lambda x: race_value(x, 1.0, 7.0), color=GREY,
                           width=4, opacity=0.45))
    fn = lambda x: race_value(x, start, defense_day)
    if curve == "live":
        crv = P.live_curve(fn, tracker, color=TEAL, width=7)
        dot = P.dot(lambda: tracker.get_value(), lambda: fn(tracker.get_value()),
                    color=TEAL, ring=TEXT, radius=0.11)
    elif curve:
        crv = P.curve(fn, color=TEAL, width=7)
        dot = Dot(P.pt(day, fn(day)), radius=0.11, color=TEAL,
                  stroke_color=TEXT, stroke_width=3)
    else:
        crv, dot = VGroup(), VGroup()
    pieces.add(crv, dot)

    frame = RoundedRectangle(width=2.0, height=4.25, corner_radius=0.18,
                             stroke_color=GOLD, stroke_width=3).move_to([4.65, 0.25, 0])
    label = T("defense\n(antibody)", 26, GOLD, line_spacing=0.8).move_to([4.65, 2.8, 0])
    day_box = RoundedRectangle(width=2.05, height=0.55, corner_radius=0.14,
                               stroke_color=GREY, stroke_width=2).move_to([5.05, 3.5, 0])
    day_text = counter("day {:.0f}", tracker, at=[5.05, 3.5, 0], size=28, color=TEXT)
    bottom = frame.get_bottom()[1] + 0.16

    def make_bar():
        frac = defense_fraction(tracker.get_value(), defense_day, baseline)
        h = 0.16 + 3.75 * frac
        bar = Rectangle(width=1.45, height=h, stroke_width=0,
                        fill_color=GOLD, fill_opacity=0.78)
        bar.move_to([4.65, bottom + h / 2, 0])
        bar.layout_ok = True
        return bar

    bar = always_redraw(make_bar)
    frame.layout_ok = True
    day_box.layout_ok = True
    pieces.add(frame, bar, label, day_box, day_text)
    tag = scope_tag("schematic")
    pieces.add(tag)
    return SimpleNamespace(group=pieces, plot=P, tracker=tracker, curve=crv,
                           dot=dot, frame=frame, bar=bar, day_box=day_box,
                           day_text=day_text, label=label, tag=tag)


def predict_backdrop():
    world = race_world(day=0, defense_day=3, baseline=0.08, curve=False,
                       ghost_first=True)
    pathogen = microbe(0.34).move_to(world.plot.pt(0.35, 20))
    cells = VGroup(memory_cell().scale(0.62), memory_cell().scale(0.62)).arrange(DOWN, buff=0.25)
    cells.move_to([3.25, -0.35, 0])
    return VGroup(world.group, pathogen, cells)


def drifters(scene, n=22, seed=3):
    """Visible slow drifting motes behind the picture, so a held frame keeps moving."""
    import random
    rng = random.Random(seed)
    grp = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.07, 0.14), color=rng.choice([TEAL, GOLD, GREY])).set_opacity(rng.uniform(0.3, 0.5))
        d.move_to([rng.uniform(-6.5, 6.5), rng.uniform(-3.4, 3.4), 0])
        d.v = (rng.uniform(-0.35, 0.35), rng.uniform(0.2, 0.5))
        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 3.9:
                m.shift(DOWN * 7.8)
            if abs(m.get_x()) > 6.9:
                m.shift(LEFT * 13.8 * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        grp.add(d)
    grp.set_z_index(-5)
    scene.add(grp)
    return grp


class S00Title(TitleCard):
    LESSON = "Germs, Vaccines and Antibiotics"
    TITLE = "A Race Inside the Body"


class S01Question(SpokenScene):
    def construct(self):
        drifters(self, seed=1)
        w = clinic_world()
        self.at("In 1846")
        self.play(FadeIn(w.year), FadeIn(w.panels), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in VGroup(w.first, w.second)],
                              lag_ratio=0.18), run_time=1.0)
        first_grey = VGroup(*[mother_icon(GREY) for _ in range(4)]).arrange_in_grid(2, 2, buff=0.27)
        first_grey.move_to(VGroup(*w.first[:4]))
        second_grey = mother_icon(GREY).move_to(w.second[0])
        self.at("died about four times")
        self.play(Transform(VGroup(*w.first[:4]), first_grey),
                  Transform(w.second[0], second_grey), run_time=1.1)
        ratio = T("about 4 times as often", 30, RED).move_to([0, -2.62, 0])
        self.play(FadeIn(ratio), run_time=0.45)

        qmark = T("?", 92, GOLD, weight=BOLD).move_to([0, 3.15, 0])
        self.at("What could the doctors")
        self.play(FadeOut(w.year), FadeIn(qmark, scale=0.55), run_time=0.6)
        self.play(Indicate(qmark, color=GOLD, scale_factor=1.12), run_time=0.65)
        self.play(qmark.animate.shift(RIGHT * 1.25), rate_func=there_and_back, run_time=3.6)
        bob(qmark, amp=0.07, speed=3.0)
        ratio._t = 0.0
        def _breathe(m, dt):
            m._t += dt
            m.set_opacity(0.7 + 0.3 * np.sin(2.6 * m._t))
        ratio.add_updater(_breathe)
        for _g in (VGroup(*w.first[:4]), VGroup(*w.second[:1])):
            _g._t = 0.0
            _g._base = _g.get_center().copy()
            def _sway(m, dt):
                m._t += dt
                m.move_to(m._base + RIGHT * 0.06 * np.sin(2.2 * m._t))
            _g.add_updater(_sway)
        door = RoundedRectangle(width=1.55, height=1.45, corner_radius=0.12,
                                stroke_color=GREY, stroke_width=4).move_to([-4.75, -0.85, 0])
        door.layout_ok = True  # its label is intentionally written on the door
        door_lab = T("autopsy\nroom", 28, GREY, line_spacing=0.8).move_to([-4.75, -1.2, 0])
        hands = hands_pair(0.72).move_to([-3.45, -0.25, 0])
        hands.set_z_index(3)
        self.at("handled bodies in autopsies")
        ratio.clear_updaters()
        self.play(FadeOut(ratio), FadeIn(door), FadeIn(door_lab),
                  FadeIn(hands, shift=UP * 0.15), run_time=0.9)
        self.at("Then they examined")
        self.play(hands.animate.move_to([-2.75, -0.2, 0]), run_time=1.0)
        self.finish()


class S02Hands(SpokenScene):
    def construct(self):
        name = T("Ignaz Semmelweis", 42, TEXT, font=TITLE_FONT).move_to([0, 3.25, 0])
        hands = hands_pair(1.45).move_to([0, 1.1, 0])
        basin = Arc(radius=2.0, start_angle=PI, angle=PI, color=GOLD,
                    stroke_width=9).move_to([0, -0.45, 0])
        water = Line([-1.85, -0.45, 0], [1.85, -0.45, 0], color=GOLD, stroke_width=5)
        basin_lab = T("chlorine, 1847", 32, GOLD).move_to([0, -1.65, 0])
        self.at("suspected the examiner's hands")
        self.play(FadeIn(name), FadeIn(hands, shift=UP * 0.2), run_time=0.8)
        self.at("wash in chlorine")
        self.play(Create(basin), Create(water), FadeIn(basin_lab),
                  hands.animate.move_to([0, -0.15, 0]), run_time=1.0)
        self.play(hands.animate.shift(UP * 0.18), rate_func=there_and_back, run_time=0.8)

        clip = RoundedRectangle(width=3.7, height=2.25, corner_radius=0.15,
                                stroke_color=GREY, stroke_width=4, fill_color=BG,
                                fill_opacity=1).move_to([-5.0, 0.25, 0])
        clip_label = T("his records", 32, GREY).move_to(clip)
        self.at("test his records")
        self.play(FadeOut(basin_lab),
                  VGroup(clip, clip_label).animate.move_to([4.75, 0.25, 0]), run_time=1.5)
        lesson = T("you check them in the lesson", 28, TEXT).move_to([3.8, -1.35, 0])
        self.play(FadeIn(lesson), run_time=0.45)

        bubble = VGroup(Circle(radius=1.05, stroke_color=GOLD, stroke_width=4),
                        T("???", 50, GOLD, weight=BOLD)).move_to([0, 1.05, 0])
        unknown = chip("cause unknown", GOLD, size=28).move_to([0, -2.35, 0])
        self.at("what he did not know")
        self.play(FadeOut(VGroup(clip, clip_label, lesson)), FadeOut(name),
                  FadeIn(bubble, scale=0.65), run_time=0.8)
        self.at("could not name")
        self.play(FadeIn(unknown), Indicate(bubble, color=GOLD), run_time=0.8)
        bob(bubble, amp=0.05, speed=1.8)
        self.finish()


class S03Germ(SpokenScene):
    def construct(self):
        bubble = VGroup(Circle(radius=1.05, stroke_color=GOLD, stroke_width=4),
                        T("???", 50, GOLD, weight=BOLD)).move_to([0, 0.6, 0])
        self.add(bubble)
        lens = Circle(radius=2.35, stroke_color=TEXT, stroke_width=8).move_to([0, 0.45, 0])
        handle = Line([1.65, -1.2, 0], [3.35, -2.65, 0], color=TEXT, stroke_width=12)
        self.at("Germ theory later")
        self.play(Transform(bubble[0], lens), FadeOut(bubble[1]), Create(handle), run_time=1.0)
        microbes = VGroup(*[microbe(0.26, antigen=False) for _ in range(6)]).arrange_in_grid(2, 3, buff=0.45)
        microbes.move_to([0, 0.45, 0])
        microbes_lab = T("microbes", 36, TEAL).move_to([0, 3.25, 0])
        self.at("caused by microbes")
        self.play(LaggedStart(*[FadeIn(m, scale=0.45) for m in microbes], lag_ratio=0.12),
                  FadeIn(microbes_lab), run_time=1.1)
        self.at("too small to see")
        self.play(Indicate(lens, color=TEXT, scale_factor=1.04), run_time=0.8)

        chosen = microbe(0.55).move_to([-2.55, 0.45, 0])
        tag = chip("pathogen: causes disease", RED, size=30).move_to([2.1, 0.45, 0])
        arrow = Arrow(chosen.get_right(), tag.get_left(), buff=0.15, color=RED,
                      stroke_width=5, tip_length=0.22)
        self.at("causes disease is called")
        self.play(FadeOut(microbes), FadeIn(chosen, scale=0.6), GrowArrow(arrow),
                  FadeIn(tag), run_time=1.0)

        skin_l = Line([-6.1, -1.65, 0], [-0.7, -1.65, 0], color=SKIN, stroke_width=18)
        skin_r = Line([0.7, -1.65, 0], [6.1, -1.65, 0], color=SKIN, stroke_width=18)
        body_lab = T("into the body", 32, SKIN).move_to([0, -3.12, 0])
        self.at("multiply once they get")
        self.play(FadeOut(VGroup(tag, arrow)), Create(skin_l), Create(skin_r),
                  FadeIn(body_lab), chosen.animate.move_to([0, -2.05, 0]), run_time=1.2)
        self.finish()


class S04Race(SpokenScene):
    def construct(self):
        w = race_world(day=0, defense_day=7, curve="live")
        self.play(Create(w.plot), FadeIn(VGroup(w.frame, w.label, w.day_box, w.day_text, w.tag)),
                  run_time=0.75)
        self.add(w.curve, w.dot, w.bar)
        self.at("One becomes two")
        self.play(w.tracker.animate.set_value(1), run_time=1.0, rate_func=linear)
        self.at("two become four")
        self.play(w.tracker.animate.set_value(2), run_time=0.9, rate_func=linear)
        self.at("doubling keeps going")
        self.play(w.tracker.animate.set_value(3.8), run_time=1.3, rate_func=linear)
        self.at("body builds a defense")
        self.play(w.tracker.animate.set_value(4.8), run_time=1.15, rate_func=linear)

        big = microbe(0.72).move_to([-1.0, 0.1, 0])
        antigen_lab = T("one small part: antigen", 28, TEAL).move_to([-0.65, 3.15, 0])
        ab = antibody(0.62).rotate(-PI / 2).move_to(big.get_right() + RIGHT * 0.42)
        ab_lab = T("antibody", 30, GOLD).move_to([1.35, 1.25, 0])
        demo = VGroup(big, antigen_lab, ab, ab_lab)
        demo.set_z_index(5)
        self.at("Antibodies are proteins")
        self.play(FadeIn(big, scale=0.65), FadeIn(ab_lab), run_time=0.75)
        self.at("stick to one small part")
        self.play(FadeIn(antigen_lab), FadeIn(ab, shift=RIGHT * 0.3), run_time=0.9)
        self.at("block a microbe")
        self.play(Indicate(VGroup(big, ab), color=GOLD, scale_factor=1.05),
                  w.tracker.animate.set_value(5.4), run_time=1.0)
        self.at("takes a week or more")
        self.play(FadeOut(demo), w.tracker.animate.set_value(6.0),
                  run_time=1.2, rate_func=linear)
        self.finish()


class S05Rule(SpokenScene):
    def construct(self):
        drifters(self, seed=5)
        w = race_world(day=6, defense_day=7, curve="live")
        self.add(w.group)
        cap = caption("infection as a race (simple model)", size=30, color=TEXT)
        self.at("picture an infection as a race")
        self.play(FadeIn(cap), w.tracker.animate.set_value(6.6), run_time=1.0)
        self.at("defenses catch up")
        self.play(w.tracker.animate.set_value(7.0), run_time=1.1, rate_func=linear)
        self.at("microbes fall once")
        self.play(w.tracker.animate.set_value(8.6), run_time=2.0, rate_func=linear)
        peak_p = w.plot.pt(7, race_value(7))
        bracket = BraceBetweenPoints(w.plot.pt(7, 0), peak_p, direction=RIGHT, color=TEAL)
        peak_lab = T("peak", 30, TEAL).move_to(w.plot.pt(5.4, 122))
        self.at("climbed very high")
        self.play(GrowFromCenter(bracket), FadeIn(peak_lab), run_time=0.8)
        face = VGroup(Circle(radius=0.42, color=RED, stroke_width=4),
                      Dot(radius=0.04, color=RED).shift(LEFT * 0.14 + UP * 0.1),
                      Dot(radius=0.04, color=RED).shift(RIGHT * 0.14 + UP * 0.1),
                      Arc(radius=0.17, start_angle=0.15, angle=PI - 0.3,
                          color=RED, stroke_width=4).shift(DOWN * 0.18))
        face.move_to([3.0, 1.65, 0])
        sick = T("often more illness", 28, RED).move_to([3.05, 0.8, 0])
        self.at("more microbes means")
        self.play(FadeIn(face), FadeIn(sick), Indicate(bracket, color=TEAL), run_time=0.9)
        bob(face, amp=0.12, speed=3.0)
        peak_lab._t = 0.0
        def _glow(m, dt):
            m._t += dt
            m.set_opacity(0.65 + 0.35 * np.sin(3.0 * m._t))
        peak_lab.add_updater(_glow)
        sick._t = 0.0
        sick.add_updater(lambda m, dt: (setattr(m, "_t", m._t + dt), m.set_opacity(0.7 + 0.3 * np.sin(2.4 * m._t + 1)))[0])
        pulse(bracket, base=4.0, amp=2.5, speed=4.0)
        self.finish()


class S06Start(SpokenScene):
    def construct(self):
        w = race_world(day=0, start=0.22, defense_day=7, curve="live", ghost_first=True)
        self.add(w.group)
        start_dots = VGroup(*[Dot(radius=0.13, color=TEAL) for _ in range(12)]).arrange_in_grid(3, 4, buff=0.12)
        start_dots.move_to(w.plot.pt(0.55, 35))
        self.at("two ways to get ahead")
        self.play(FadeIn(start_dots, scale=0.7), run_time=0.7)
        smaller = T("smaller start", 32, TEAL).move_to([-0.5, 3.25, 0])
        self.at("start the race with fewer")
        keep = VGroup(*start_dots[:3])
        swept = VGroup(*start_dots[3:])
        self.play(FadeOut(swept, shift=LEFT * 1.0), keep.animate.shift(LEFT * 0.3),
                  FadeIn(smaller), run_time=1.0)

        tools = VGroup(chip("hand washing", TEAL, size=28), chip("clean water", TEAL, size=28),
                       chip("sterile tools", TEAL, size=28)).arrange(DOWN, buff=0.2)
        tools.move_to([4.65, 0.3, 0])
        self.at("Hand washing")
        self.play(FadeOut(VGroup(w.frame, w.bar, w.label)), FadeIn(tools[0]), run_time=0.7)
        self.at("clean water and sterile tools")
        self.play(FadeIn(tools[1]), FadeIn(tools[2]), run_time=0.8)
        self.at("keep microbes out")
        self.play(FadeOut(keep, shift=LEFT * 0.8), run_time=0.65)

        self.at("Run the race again")
        self.play(FadeOut(tools), FadeIn(VGroup(w.frame, w.bar, w.label)),
                  w.tracker.animate.set_value(4.6), run_time=1.8, rate_func=linear)
        self.at("defense still arrives")
        self.play(w.tracker.animate.set_value(7.0), run_time=1.8, rate_func=linear)
        low_peak = w.plot.pt(7, race_value(7, 0.22, 7))
        low_lab = T("lower peak", 30, TEAL).move_to(w.plot.pt(4.3, 105))
        low_lab.layout_ok = True  # deliberate label beside its computed curve
        self.at("peak is lower")
        self.play(FadeIn(low_lab), Indicate(w.curve, color=TEAL), run_time=0.8)
        self.finish()


class S07Vaccine(SpokenScene):
    def construct(self):
        heading = T("send the defense in early", 42, GOLD, font=TITLE_FONT).move_to([0, 3.25, 0])
        syringe = VGroup(
            RoundedRectangle(width=2.0, height=0.55, corner_radius=0.08,
                             stroke_color=TEXT, stroke_width=4),
            Line([1.0, 0, 0], [2.0, 0, 0], color=TEXT, stroke_width=4),
            Line([-1.25, -0.48, 0], [-1.25, 0.48, 0], color=TEXT, stroke_width=4),
            T("vaccine", 28, TEXT),
        ).move_to([-4.4, 1.25, 0])
        antigen = microbe(0.34).move_to([-1.1, 1.25, 0])
        antigen_lab = fit_text("antigen: the part the immune system recognizes", max_w=4.6,
                               size=28, color=TEAL, max_lines=2).move_to([-1.1, 0.25, 0])
        immune = VGroup(*[Circle(radius=0.42, stroke_color=GOLD, stroke_width=4,
                                 fill_color=GOLD, fill_opacity=0.08) for _ in range(4)]).arrange(DOWN, buff=0.28)
        immune.move_to([3.9, 0.65, 0])
        self.at("send the defense in early")
        self.play(FadeIn(heading), FadeIn(syringe, shift=RIGHT * 0.2), run_time=0.85)
        self.at("vaccine shows the immune system")
        self.play(FadeIn(immune), syringe.animate.shift(RIGHT * 0.55), run_time=0.9)
        self.at("an antigen")
        self.play(FadeIn(antigen, scale=0.55), FadeIn(antigen_lab), run_time=0.8)
        self.at("learns to recognize")
        self.play(antigen.animate.move_to([2.45, 1.25, 0]),
                  Indicate(immune, color=GOLD), run_time=1.1)
        no_disease = chip("without the full disease", RED, size=28).move_to([-2.6, -2.3, 0])
        slash = Line(no_disease.get_corner(UL), no_disease.get_corner(DR), color=TEXT, stroke_width=5)
        slash.layout_ok = True
        self.at("without the full disease")
        self.play(FadeIn(no_disease), Create(slash), run_time=0.85)

        memories = VGroup(memory_cell(), memory_cell(), memory_cell()).arrange(RIGHT, buff=0.45)
        memories.move_to([2.5, -1.55, 0])
        self.at("become memory cells")
        self.play(Transform(VGroup(*immune[:3]), memories), FadeOut(immune[3]),
                  FadeOut(VGroup(no_disease, slash)), run_time=1.0)
        mem_lab = T("memory cells", 32, GOLD).move_to([2.5, -2.55, 0])
        cal = calendar_icon().move_to([-0.3, -1.65, 0])
        self.at("stay in the body long after")
        self.play(FadeIn(mem_lab), FadeIn(cal),
                  Rotate(cal, angle=-0.08, rate_func=there_and_back), run_time=1.2)
        bob(memories, amp=0.04, speed=1.7)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        w = race_world(day=0, defense_day=3, baseline=0.08, curve=False, ghost_first=True)
        self.add(w.group)
        cells = VGroup(memory_cell().scale(0.62), memory_cell().scale(0.62)).arrange(DOWN, buff=0.25)
        cells.move_to([3.25, -0.35, 0])
        pathogen = microbe(0.34).move_to([-6.4, 1.15, 0])
        self.at("real pathogen arrives")
        self.play(FadeIn(cells), pathogen.animate.move_to(w.plot.pt(0.35, 20)), run_time=1.2)
        bob(cells, amp=0.055, speed=1.9)
        same = T("same antigen", 28, TEAL).move_to([-3.85, 1.95, 0])
        self.at("carrying the same antigen")
        self.play(FadeIn(same), Indicate(pathogen.antigen, color=TEAL), run_time=0.8)
        second = T("second meeting", 34, GOLD).move_to([-1.8, 3.25, 0])
        self.at("body's second meeting")
        self.play(FadeOut(same), FadeIn(second), Indicate(cells, color=GOLD), run_time=0.9)
        q = question_card("sooner or later?", options=("sooner", "later"),
                          chips_at=[3.3, 1.35, 0], size=38, color=GOLD)
        self.at("Will the gold defense")
        self.play(FadeIn(q.chips), run_time=0.55)
        self.at("sooner or later")
        self.play(FadeIn(q.question), run_time=0.65)
        self.finish()


class S09Pause(PredictPause):
    QUESTION = "sooner or later?"
    OPTIONS = ("sooner", "later")
    CHIPS_AT = [3.3, 1.35, 0]
    CARD = {"size": 38, "color": GOLD}
    RING_AT = (-6.0, -3.0, 0)

    def backdrop(self):
        return predict_backdrop()


class S10Reveal(SpokenScene):
    def construct(self):
        w = race_world(day=0, defense_day=3, baseline=0.08, curve="live", ghost_first=True)
        self.add(w.group)
        memories = VGroup(memory_cell().scale(0.68), memory_cell().scale(0.68)).arrange(DOWN, buff=0.2)
        memories.move_to([3.2, -0.35, 0])
        self.add(memories)
        answer = T("SOONER", 50, GOLD, weight=BOLD).move_to([-1.75, 3.25, 0])
        self.at("Sooner")
        self.play(FadeIn(answer, scale=0.55), Indicate(memories, color=GOLD), run_time=0.8)
        self.at("Memory cells recognize")
        copies = VGroup(*[memory_cell().scale(0.50) for _ in range(3)]).arrange(DOWN, buff=0.12)
        copies.move_to([3.2, -0.35, 0])
        self.play(Transform(memories, copies), run_time=0.9)

        maker = RoundedRectangle(width=1.35, height=1.55, corner_radius=0.35,
                                 stroke_color=GOLD, stroke_width=5,
                                 fill_color=GOLD, fill_opacity=0.15).move_to([2.95, -0.95, 0])
        maker_lab = T("antibody-\nmaking\ncells", 28, GOLD,
                      line_spacing=0.72).move_to(maker)
        self.at("lead to large amounts")
        self.play(Transform(memories, VGroup(maker, maker_lab)), run_time=0.9)
        ys = VGroup(*[antibody(0.24).move_to([2.35 + 0.36 * (i % 4),
                                             0.25 + 0.38 * (i // 4), 0]) for i in range(8)])
        self.at("of antibody")
        self.play(LaggedStart(*[FadeIn(y, shift=UP * 0.2) for y in ys], lag_ratio=0.08),
                  run_time=0.9)
        self.at("defense arrives days earlier")
        self.play(w.tracker.animate.set_value(3.0), run_time=1.8, rate_func=linear)
        self.at("less time to double")
        self.play(w.tracker.animate.set_value(4.6), FadeOut(ys),
                  run_time=1.5, rate_func=linear)
        early_peak = T("second meeting", 30, TEAL).move_to([-2.4, 1.55, 0])
        self.at("never climb very high")
        self.play(FadeIn(early_peak), Indicate(w.curve, color=TEAL), run_time=0.8)
        self.finish()


def mini_race(start, defense_day, panel_center):
    x = panel_center[0]
    P = Plot(box=(x - 2.5, x + 2.5, -1.65, 1.55), xr=(0, 9), yr=(0, 145),
             xticks=[], yticks=[], xlabel="days", ylabel="microbes", label_size=24)
    curve = P.curve(lambda t: race_value(t, start, defense_day), color=TEAL, width=6)
    finish = P.vline(7, "finish", color=GOLD, size=24)
    return VGroup(P, curve, finish)


class S11Both(SpokenScene):
    def construct(self):
        panels = TwoPanel("hygiene: smaller start", "vaccine: earlier defense",
                          colors=(TEAL, GOLD), top=2.8, bottom=-2.35, size=30)
        panels.left_frame.set_fill(TEAL, opacity=0.32)
        panels.right_frame.set_fill(GOLD, opacity=0.32)
        panels.left_frame.layout_ok = True
        panels.right_frame.layout_ok = True
        self.add(panels)
        left = mini_race(0.22, 7, [-3.3, 0, 0])
        right = mini_race(1.0, 3, [3.3, 0, 0])
        self.at("Hygiene shrinks the start")
        self.play(Create(left[0]), Create(left[1]), FadeIn(left[2]), run_time=1.2)
        self.at("vaccine moves the defense earlier")
        self.play(Create(right[0]), Create(right[1]), FadeIn(right[2]), run_time=1.2)
        shared = T("same race", 32, TEXT).move_to([0, 3.35, 0])
        self.at("two ways to win")
        self.play(FadeIn(shared), Indicate(VGroup(left[2], right[2]), color=GOLD), run_time=0.9)
        rule = caption("A smaller start or an earlier defense keeps the peak low.",
                       size=32, color=GOLD)
        self.at("A smaller start")
        self.play(Write(rule), run_time=1.5)
        pulse(left[1], base=6, amp=1.0, speed=2.4)
        pulse(right[1], base=6, amp=1.0, speed=2.4)
        self.finish()


class S12End(EndCard):
    LINE = "A smaller start or an earlier defense keeps the peak low."
