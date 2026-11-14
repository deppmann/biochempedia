"""What controls respiration's speed?  Chapter 2 of Releasing energy from food.

Every narrated change is tied to audio/words.json.  The pea-cell pathway and the
temperature experiment are rebuilt by shared builders so carried pictures do not drift.

COLOR MAP (shared exactly with chapter 1's script)
  GOLD   = glucose and stored food energy
  BLUE   = oxygen
  GREY   = carbon dioxide and neutral structure
  CYAN   = water
  GREEN  = energy for cell work / active respiration
  ORANGE = thermal energy / warmth
  PURPLE = mitochondria
  CREAM  = cells
  RED    = damage / stopped respiration
"""
from types import SimpleNamespace

import numpy as np
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CYAN = "#4FC3C9"
CREAM = "#F2E5C4"
GLUCOSE, OXYGEN, CO2, WATER, WORK, HEAT = GOLD, BLUE, GREY, CYAN, GREEN, ORANGE


def arrow(a, b, color=GREY, width=5, tip=0.2):
    """Short, high-contrast diagram arrow."""
    m = Arrow(a, b, buff=0.08, color=color, stroke_width=width, tip_length=tip,
              max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)
    return m


def moving_stream(points, color, speed, shapes="dots", size=0.11):
    """Particles cycling along a polyline, driven by a shared rate tracker."""
    pts = [np.array(p, dtype=float) for p in points]
    seg = [np.linalg.norm(b - a) for a, b in zip(pts, pts[1:])]
    total = sum(seg)
    phase = [i / 8 for i in range(8)]
    if shapes == "blocks":
        g = VGroup(*[Square(2 * size, stroke_width=0, fill_color=color, fill_opacity=0.95) for _ in phase])
    else:
        g = VGroup(*[Dot(radius=size, color=color) for _ in phase])
    clock = [0.0]

    def point_at(u):
        d = (u % 1.0) * total
        for a, b, length in zip(pts, pts[1:], seg):
            if d <= length:
                return a + (b - a) * (d / max(length, 1e-6))
            d -= length
        return pts[-1]

    def move(mob, dt):
        # Fast enough to read as material moving between steps at draft frame rate.
        clock[0] += dt * 1.6 * max(0.0, speed.get_value())
        for p, ph in zip(mob, phase):
            p.move_to(point_at(ph + clock[0]))

    g.add_updater(move)
    g.layout_ok = True  # particles intentionally travel through the labelled pathway
    return g


def pea_pathway(scale=1.0, center=ORIGIN, rate=0.32, show_labels=True):
    """The carried pea-cell world used by every scene about the same pathway."""
    c = np.array(center, dtype=float)
    speed = ValueTracker(rate)
    cell = Ellipse(width=8.4, height=5.05, stroke_color=CREAM, stroke_width=6,
                   fill_color=CREAM, fill_opacity=0.13).move_to(c)
    mito = Ellipse(width=4.55, height=2.85, stroke_color=PURPLE, stroke_width=5,
                   fill_color=PURPLE, fill_opacity=0.21).move_to(c + RIGHT * 0.65)
    folds = VGroup(*[
        ArcBetweenPoints(c + np.array([x, -0.72, 0]), c + np.array([x + 0.55, 0.72, 0]),
                         angle=(-1) ** i * 0.8, color=PURPLE, stroke_width=3)
        for i, x in enumerate([-0.85, 0.0, 0.85, 1.7])
    ])
    stones = VGroup(*[
        RoundedRectangle(corner_radius=0.09, width=0.62, height=0.42,
                         stroke_color=WORK, stroke_width=4, fill_color=WORK, fill_opacity=0.25)
        .move_to(c + np.array([-3.05 + 0.78 * i, 0.0, 0])) for i in range(8)
    ])
    wave_clock = [0.0]

    def step_wave(mob, dt):
        wave_clock[0] += dt * max(0.0, speed.get_value()) * 12.0
        for i, step in enumerate(mob):
            glow = 0.10 + 0.88 * (0.5 + 0.5 * np.sin(wave_clock[0] - i * 0.9))
            step.set_fill(WORK, opacity=glow).set_stroke(WORK, width=2 + 7 * glow)

    stones.add_updater(step_wave)
    resp = T("respiration", 30, WORK, weight=BOLD).move_to(c + DOWN * 1.78)
    mito_lab = T("mitochondrion", 28, PURPLE).move_to(c + UP * 1.02 + RIGHT * 0.65)
    base = VGroup(cell, mito, folds, stones)
    if show_labels:
        base.add(resp, mito_lab)
    in_flow = moving_stream([c + LEFT * 3.72, c + LEFT * 2.65, c + RIGHT * 2.65], OXYGEN, speed, size=0.14)
    out_flow = moving_stream([c + RIGHT * 2.65 + DOWN * 0.48, c + RIGHT * 3.75 + DOWN * 0.48],
                             CO2, speed, shapes="blocks", size=0.14)
    world = VGroup(base, in_flow, out_flow).scale(scale).move_to(c)
    # Scaling about the centre above also scales the requested offset; correct only if needed.
    if np.linalg.norm(world.get_center()[:2] - c[:2]) > 0.01:
        world.shift(c - world.get_center())
    return SimpleNamespace(group=world, cell=cell, mito=mito, stones=stones,
                           oxygen=in_flow, carbon=out_flow, speed=speed)


def mini_pathway(center=(-2.0, 0.25, 0), rate=0.32):
    """The same carried pathway, reduced for the temperature/curve composition."""
    return pea_pathway(scale=0.55, center=center, rate=rate, show_labels=False)


def thermometer(center=(-5.55, 0.15, 0), value=None, height=4.65):
    """Large schematic thermometer with a live level tracker from 0 to 1."""
    value = value or ValueTracker(0.25)
    c = np.array(center, dtype=float)
    tube = RoundedRectangle(corner_radius=0.13, width=0.48, height=height,
                            stroke_color=TEXT, stroke_width=4).move_to(c)
    bulb = Circle(radius=0.43, stroke_color=TEXT, stroke_width=4,
                  fill_color=HEAT, fill_opacity=0.95).move_to(c + DOWN * (height / 2 + 0.14))
    y0, span = c[1] - height / 2 + 0.15, height - 0.3
    fluid = always_redraw(lambda: Rectangle(width=0.22, height=max(0.04, span * value.get_value()),
                                             stroke_width=0, fill_color=HEAT, fill_opacity=0.95)
                          .move_to([c[0], y0 + span * value.get_value() / 2, 0]))
    ticks = VGroup(*[Line([c[0] + 0.27, y, 0], [c[0] + 0.47, y, 0], color=GREY, stroke_width=2)
                     for y in np.linspace(y0 + 0.35, y0 + span - 0.2, 6)])
    return SimpleNamespace(group=VGroup(tube, bulb, fluid, ticks), value=value)


def temp_rate(x):
    """A smooth qualitative response used only in explicitly schematic temperature plots."""
    return max(0.0, 1.0 - ((x - 0.58) / 0.52) ** 2)


def temperature_world(progress=0.62, cover=False, question=False):
    """Exact carried composition for warming, prediction, pause, and heat reveal."""
    temp = ValueTracker(progress)
    th = thermometer(value=temp)
    path = mini_pathway(rate=temp_rate(progress) * 0.46)
    P = Plot(box=(0.45, 5.95, -1.72, 2.35), xr=(0, 1), yr=(0, 1.08),
             xticks=(), yticks=(), xlabel="temperature", ylabel="respiration rate",
             color=GREY, label_size=28)
    curve = P.curve(temp_rate, color=WORK, width=7)
    suitable = Rectangle(width=2.65, height=4.07, stroke_width=0, fill_color=WORK,
                         fill_opacity=0.08).move_to([2.92, 0.315, 0])
    suitable_lab = T("suitable range", 28, WORK).move_to([2.75, -1.25, 0])
    hot = Rectangle(width=1.43, height=4.07, stroke_width=0, fill_color=RED,
                    fill_opacity=0.10).move_to([5.235, 0.315, 0])
    hot_lab = T("hotter", 28, RED).move_to([5.23, -1.25, 0])
    cover_mob = RoundedRectangle(corner_radius=0.12, width=1.75, height=3.15,
                                 stroke_color=RED, stroke_width=3, fill_color=BG,
                                 fill_opacity=1).move_to([5.08, 0.48, 0])
    qmark = T("?", 60, RED, weight=BOLD).move_to(cover_mob)
    cover_group = VGroup(cover_mob, qmark)
    tag = T("schematic", 24, GREY).move_to([5.72, 3.48, 0])
    group = VGroup(th.group, path.group, suitable, P, curve, suitable_lab, hot, hot_lab, tag)
    if cover:
        group.add(cover_group)
    if question:
        group.add(question_card("Hotter forever means faster forever?"))
    return SimpleNamespace(group=group, thermometer=th, path=path, plot=P, curve=curve,
                           suitable=VGroup(suitable, suitable_lab), hot=VGroup(hot, hot_lab),
                           cover=cover_group, temp=temp)


def valve(center=(-5.0, 0.3, 0), openness=None):
    """A large oxygen valve whose two plates visibly constrict the blue stream."""
    openness = openness or ValueTracker(1.0)
    c = np.array(center, dtype=float)
    pipe = VGroup(Line(c + LEFT * 1.25, c + RIGHT * 1.25, color=OXYGEN, stroke_width=12),
                  Circle(radius=0.82, color=OXYGEN, stroke_width=5).move_to(c))
    plates = always_redraw(lambda: VGroup(
        Line(c + np.array([-0.58, 0.62 * openness.get_value(), 0]),
             c + np.array([0.58, 0.12 * openness.get_value(), 0]), color=TEXT, stroke_width=8),
        Line(c + np.array([-0.58, -0.62 * openness.get_value(), 0]),
             c + np.array([0.58, -0.12 * openness.get_value(), 0]), color=TEXT, stroke_width=8)))
    return SimpleNamespace(group=VGroup(pipe, plates), openness=openness)


def hopper(center=(-5.0, 0.75, 0), fill=None):
    """A schematic glucose hopper with a live gold fill."""
    fill = fill or ValueTracker(0.12)
    c = np.array(center, dtype=float)
    outline = Polygon(c + [-1.0, 1.45, 0], c + [1.0, 1.45, 0], c + [0.42, -0.65, 0],
                      c + [0.2, -0.65, 0], c + [0.2, -1.25, 0], c + [-0.2, -1.25, 0],
                      c + [-0.2, -0.65, 0], c + [-0.42, -0.65, 0],
                      color=GLUCOSE, stroke_width=5, fill_opacity=0)
    blocks = VGroup(*[Square(0.28, stroke_width=0, fill_color=GLUCOSE, fill_opacity=0.95)
                      .move_to(c + [-0.65 + 0.43 * (i % 4), -0.35 + 0.38 * (i // 4), 0]) for i in range(16)])

    def show(mob):
        n = int(round(np.clip(fill.get_value(), 0, 1) * len(mob)))
        for i, block in enumerate(mob):
            block.set_opacity(1 if i < n else 0)

    blocks.add_updater(lambda m, dt: show(m))
    return SimpleNamespace(group=VGroup(outline, blocks), fill=fill, blocks=blocks)


class S00Link(TitleCard):
    LESSON = "Releasing energy from food"
    TITLE = "What Controls Respiration's Speed?"

    def construct(self):
        world = pea_pathway(rate=0.25)
        title = fit_text(self.TITLE, max_w=11.6, size=48, font=TITLE_FONT).move_to([0, 3.27, 0])
        lesson = T(self.LESSON.upper(), 22, GREY).move_to([0, 2.78, 0])
        q = fit_text("What makes respiration speed up or slow down?", max_w=11.5,
                     size=40, color=GOLD).move_to([0, 3.1, 0])
        tag = scope_tag("schematic")
        self.play(FadeIn(world.group, scale=0.96), run_time=self.beat(0.20))
        self.play(FadeIn(lesson), Write(title), run_time=self.beat(0.18))
        self.play(FadeOut(lesson), swap(title, q), run_time=self.beat(0.22))
        self.add(tag)
        self.play(world.speed.animate.set_value(0.45), run_time=self.beat(0.28), rate_func=smooth)
        self.finish()


class S01Rate(SpokenScene):
    def construct(self):
        world = pea_pathway(rate=0.18, center=(-1.7, 0, 0), scale=0.9)
        rate = ValueTracker(0.18)
        d = dial(rate, center=[4.35, 0.7, 0], radius=1.55, label="respiration rate",
                 color=WORK, fmt="", scale=1, size=1)
        # No numerical readout: five windows fill from the same tracker as the dial.
        windows = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.55, height=0.72,
                                            stroke_color=CO2, stroke_width=3, fill_color=CO2, fill_opacity=0.12)
                           for _ in range(5)]).arrange(RIGHT, buff=0.16).move_to([4.35, -1.65, 0])
        marker = always_redraw(lambda: VGroup(*[
            Square(0.31, stroke_width=0, fill_color=CO2, fill_opacity=0.95).move_to(windows[i])
            for i in range(max(1, min(5, int(np.ceil(rate.get_value() * 5)))))]))
        heading = T("track inputs and outputs over time", 30, TEXT).move_to([0, 3.2, 0])
        out_lab = T("carbon dioxide output", 28, CO2).move_to([4.35, -2.42, 0])
        self.play(FadeIn(world.group), run_time=0.8)
        self.at("how fast cells")
        self.play(Write(heading), run_time=0.8)
        self.at("oxygen entering")
        self.play(Indicate(world.oxygen, color=OXYGEN, scale_factor=1.25), run_time=0.8)
        self.at("carbon dioxide leaving")
        self.play(Indicate(world.carbon, color=TEXT, scale_factor=1.25), run_time=0.8)
        self.at("faster motion")
        self.play(FadeIn(d), FadeIn(windows), FadeIn(marker), FadeIn(out_lab), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.play(rate.animate.set_value(0.92), world.speed.animate.set_value(0.75),
                  run_time=3.2, rate_func=smooth)
        self.finish()


class S02Warming(SpokenScene):
    def construct(self):
        w = temperature_world(progress=0.22)
        # Start without the completed curve; grow it from the computed function.
        w.group.remove(w.curve)
        x = ValueTracker(0.06)
        live = w.plot.live_curve(temp_rate, x, color=WORK, width=7)
        title = T("temperature", 38, HEAT, weight=BOLD).move_to([-3.0, 3.2, 0])
        self.play(FadeIn(w.thermometer.group), FadeIn(w.path.group), run_time=0.9)
        self.at("temperature")
        self.play(FadeIn(title), run_time=0.5)
        self.at("suitable range")
        self.play(FadeIn(w.suitable), Create(w.plot), run_time=1.1)
        self.add(live, w.group[-1])
        self.play(w.temp.animate.set_value(0.38), x.animate.set_value(0.32),
                  w.path.speed.animate.set_value(0.38), run_time=3.2, rate_func=linear)
        self.at("move more quickly")
        self.play(w.temp.animate.set_value(0.68), x.animate.set_value(0.68),
                  w.path.speed.animate.set_value(0.62), run_time=4.2, rate_func=smooth)
        self.at("does not mean")
        self.play(FadeIn(w.hot), run_time=0.8)
        self.finish()


class S03Predict(SpokenScene):
    def construct(self):
        w = temperature_world(progress=0.76, cover=True)
        self.add(w.thermometer.group, w.path.group, w.suitable, w.plot, w.curve, w.group[-2])
        self.at("keep getting hotter")
        self.play(w.temp.animate.set_value(0.94), w.path.speed.animate.set_value(0.72),
                  FadeIn(w.hot), run_time=2.0)
        self.play(FadeIn(w.cover), run_time=0.6)
        q = question_card("Hotter forever means faster forever?")
        self.at("rising forever")
        self.play(w.path.speed.animate.set_value(0.12), run_time=1.2)
        self.at("follow the pathway")
        self.play(GrowFromCenter(q), run_time=1.1)
        self.at("make your prediction")
        self.play(Indicate(q, color=GOLD, scale_factor=1.02), run_time=0.7)
        self.finish()


class S04Pause(PredictPause):
    QUESTION = "Hotter forever means faster forever?"
    SECONDS = 4.5

    def backdrop(self):
        return temperature_world(progress=0.94, cover=True).group


class S05HeatReveal(SpokenScene):
    def construct(self):
        w = temperature_world(progress=0.94, cover=True)
        w.group.remove(w.hot[1])
        self.add(w.group)
        self.at("too much heat")
        self.play(FadeOut(w.cover), run_time=0.7)
        damage = T("cell damage", 30, RED, weight=BOLD).move_to([5.23, 2.3, 0])
        self.play(FadeIn(damage), w.path.speed.animate.set_value(0.05), run_time=2.2)
        self.at("bends downward")
        self.play(Indicate(w.curve, color=RED, scale_factor=1.02), run_time=1.1)
        self.at("boiling is")
        bubbles = VGroup(*[Circle(radius=0.11 + 0.03 * (i % 2), color=TEXT, stroke_width=3)
                           .move_to([-4.6 + 0.38 * (i % 3), 2.0 + 0.42 * (i // 3), 0]) for i in range(6)])
        boil = T("boiling", 30, RED, weight=BOLD).move_to([-3.0, 3.3, 0])
        self.play(w.temp.animate.set_value(1.0), FadeIn(bubbles, shift=UP * 0.25), FadeIn(boil), run_time=1.4)
        self.at("kills the pea")
        dead = T("dead cells: no respiration", 30, RED, weight=BOLD).move_to([0.4, -3.3, 0])
        self.play(w.path.group.animate.set_opacity(0.18), FadeIn(dead), run_time=1.4)
        self.finish()


class S06Oxygen(SpokenScene):
    def construct(self):
        world = pea_pathway(scale=0.78, center=(0.1, -0.45, 0), rate=0.62, show_labels=False)
        v = valve(center=(-5.0, 0.4, 0))
        rate = ValueTracker(0.82)
        d = dial(rate, center=[5.35, 0.95, 0], radius=1.35, label="respiration rate",
                 color=WORK, fmt="", scale=1, size=1)
        lab = T("oxygen valve", 32, OXYGEN, weight=BOLD).move_to([-5.0, 2.4, 0])
        self.play(FadeIn(world.group), FadeIn(v.group), FadeIn(d), FadeIn(lab), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.at("close the oxygen valve")
        self.play(v.openness.animate.set_value(0.38), world.speed.animate.set_value(0.30),
                  rate.animate.set_value(0.42), run_time=3.4, rate_func=smooth)
        self.at("uses oxygen slows")
        self.play(Indicate(world.mito, color=OXYGEN, scale_factor=1.05), run_time=0.9)
        self.at("seal the valve")
        shut = T("sealed", 30, RED, weight=BOLD).move_to([-5.0, -1.55, 0])
        self.play(v.openness.animate.set_value(0.0), FadeIn(shut), run_time=1.3)
        self.at("oxygen left")
        inside = VGroup(*[Dot([-2.15 + 0.46 * (i % 6), -0.12 + 0.42 * (i // 6), 0], radius=0.19,
                                    color=OXYGEN) for i in range(12)])
        self.play(FadeIn(inside), run_time=0.6)
        self.at("oxygen runs out")
        self.play(LaggedStart(*[FadeOut(p, scale=0.4) for p in inside], lag_ratio=0.18),
                  rate.animate.set_value(0.01), world.speed.animate.set_value(0.0),
                  run_time=4.2, rate_func=linear)
        self.finish()


class S07Sugar(SpokenScene):
    def construct(self):
        world = pea_pathway(scale=0.72, center=(0.1, -0.5, 0), rate=0.10, show_labels=False)
        h = hopper(center=(-5.15, 0.45, 0))
        rate = ValueTracker(0.12)
        d = dial(rate, center=[5.35, 0.95, 0], radius=1.35, label="respiration rate",
                 color=WORK, fmt="", scale=1, size=1)
        lab = T("glucose supply", 32, GLUCOSE, weight=BOLD).move_to([-5.15, 2.45, 0])
        self.play(FadeIn(world.group), FadeIn(h.group), FadeIn(d), FadeIn(lab), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.at("too little glucose")
        self.play(Indicate(h.group, color=GLUCOSE, scale_factor=1.04), run_time=0.8)
        sugar_stream = moving_stream([[-5.15, -0.65, 0], [-3.1, -0.55, 0]], GLUCOSE,
                                     ValueTracker(0.72), shapes="blocks", size=0.18)
        self.add(sugar_stream)
        self.at("add some")
        self.play(h.fill.animate.set_value(0.68), rate.animate.set_value(0.82),
                  world.speed.animate.set_value(0.62), run_time=3.2, rate_func=smooth)
        self.at("keep adding")
        limit = fit_text("another factor limits the rate", max_w=4.3, size=29,
                         color=RED).move_to([4.45, -2.25, 0])
        self.play(h.fill.animate.set_value(1.0), rate.animate.set_value(0.84), FadeIn(limit), run_time=2.5)
        self.at("in yeast")
        self.play(FadeOut(world.group), FadeOut(d), FadeOut(limit), run_time=0.7)
        yeast = RoundedRectangle(corner_radius=0.35, width=7.1, height=3.25, stroke_color=CREAM,
                                 stroke_width=4, fill_color=CREAM, fill_opacity=0.06).move_to([1.0, -0.35, 0])
        oxy = T("respiration with oxygen", 28, OXYGEN).move_to([1.0, 0.6, 0])
        ferm = T("fermentation", 34, GLUCOSE, weight=BOLD).move_to([1.0, -1.25, 0])
        branch = arrow([1.0, 0.18, 0], [1.0, -0.85, 0], GLUCOSE)
        self.play(FadeIn(yeast), FadeIn(oxy), GrowArrow(branch), FadeIn(ferm), run_time=1.2)
        ferm_flow = moving_stream([[1.0, 0.22, 0], [1.0, -1.0, 0]], GLUCOSE,
                                  ValueTracker(0.65), shapes="blocks", size=0.14)
        self.add(ferm_flow)
        self.at("respiration with oxygen falls")
        self.play(oxy.animate.set_opacity(0.35), ferm.animate.scale(1.08), run_time=1.1)
        self.finish()


class S08Balloon(SpokenScene):
    def construct(self):
        tp = TwoPanel("two carbon-dioxide sources", "what the measurement means",
                      colors=(CO2, OXYGEN), top=3.05, bottom=-2.48)
        left_c, _, _ = tp.area("left")
        resp = T("respiration with oxygen", 28, OXYGEN).move_to(left_c + UP * 2.05)
        ferm = T("fermentation", 30, GLUCOSE, weight=BOLD).move_to(left_c + UP * 1.2)
        co1 = VGroup(*[Square(0.22, stroke_width=0, fill_color=CO2, fill_opacity=0.95)
                       for _ in range(4)]).arrange(RIGHT, buff=0.12).next_to(resp, DOWN, buff=0.12)
        co2 = VGroup(*[Square(0.22, stroke_width=0, fill_color=CO2, fill_opacity=0.95)
                       for _ in range(6)]).arrange(RIGHT, buff=0.10).next_to(ferm, DOWN, buff=0.12)
        gas_rate = ValueTracker(0.72)
        gas_stream = VGroup(
            moving_stream([[-2.25, 0.3, 0], [-0.55, -0.35, 0]], CO2, gas_rate,
                          shapes="blocks", size=0.15),
            moving_stream([[-2.25, -0.6, 0], [-0.55, -0.35, 0]], CO2, gas_rate,
                          shapes="blocks", size=0.15),
        )
        neck = Line([-0.45, -1.82, 0], [-0.45, -1.25, 0], color=CO2, stroke_width=9)
        balloon = Ellipse(width=1.35, height=1.75, color=CO2, stroke_width=4,
                          fill_color=CO2, fill_opacity=0.12).move_to([-0.45, -0.45, 0])
        rough = T("rough measure", 30, CO2, weight=BOLD).move_to([4.15, 0.85, 0])
        oxy_marks = VGroup(*[Dot(radius=0.12, color=OXYGEN) for _ in range(7)]).arrange(RIGHT, buff=0.16)
        oxy_marks.move_to([3.45, -0.45, 0])
        clean = fit_text("cleaner for respiration with oxygen", max_w=4.2, size=26,
                         color=OXYGEN).move_to([3.45, -1.3, 0])
        self.play(FadeIn(tp), run_time=0.8)
        lanes = VGroup(arrow([-5.1, 0.3, 0], [-1.1, -0.25, 0], CO2),
                       arrow([-5.1, -0.6, 0], [-1.1, -0.45, 0], CO2))
        self.play(LaggedStart(*[GrowArrow(a) for a in lanes], lag_ratio=0.25), run_time=2.2)
        self.add(gas_stream)
        self.at("fermentation also")
        self.play(FadeIn(resp), FadeIn(ferm), run_time=0.8)
        self.play(FadeIn(co1, shift=RIGHT * 0.2), FadeIn(co2, shift=RIGHT * 0.2), run_time=0.8)
        self.at("even when air")
        air = VGroup(*[Dot(radius=0.09, color=OXYGEN) for _ in range(8)]).arrange_in_grid(2, 4, buff=0.22)
        air.move_to(left_c + DOWN * 1.45 + LEFT * 1.6)
        self.play(FadeIn(air), run_time=0.6)
        self.at("most gas")
        balloon.scale(0.62).set_fill(opacity=0.06)
        self.add(balloon)
        self.play(FadeIn(neck), balloon.animate.scale(2.25).set_fill(opacity=0.22), run_time=3.4)
        a1 = arrow([0.15, 0.85, 0], [2.65, 1.22, 0], CO2)
        a2 = arrow([0.15, -0.2, 0], [2.65, 0.48, 0], CO2)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(rough), run_time=1.1)
        self.at("oxygen use is cleaner")
        self.play(FadeIn(oxy_marks), FadeIn(clean), run_time=1.0)
        pulse(balloon, base=4, amp=1.2, speed=2)
        self.finish()


class S09Limits(SpokenScene):
    def construct(self):
        world = pea_pathway(scale=0.73, center=(0, -0.3, 0), rate=0.36, show_labels=False)
        tv, vo, hf = ValueTracker(0.58), ValueTracker(1.0), ValueTracker(0.65)
        th = thermometer(center=(-4.7, 0.55, 0), value=tv, height=2.45).group.scale(0.62)
        th.move_to([-4.8, 1.65, 0])
        va = valve(center=(0, 0, 0), openness=vo).group.scale(0.55).move_to([0, 1.9, 0])
        hp = hopper(center=(0, 0, 0), fill=hf).group.scale(0.52).move_to([4.75, 1.65, 0])
        controls = VGroup(th, va, hp)
        labs = VGroup(T("suitable range", 28, HEAT).move_to([-4.8, 3.45, 0]),
                      T("uses oxygen", 28, OXYGEN).move_to([0, 3.6, 0]),
                      T("only to a point", 28, GLUCOSE).move_to([4.75, 3.45, 0]))
        starts = [np.array([-1.5, 2.7, 0]), np.array([2.2, 2.6, 0]), np.array([0, -2.7, 0])]
        targets = [m.get_center().copy() for m in controls]
        for m, p in zip(controls, starts):
            m.move_to(p)
        self.play(FadeIn(world.group), FadeIn(controls), run_time=0.9)
        self.at("same pathway")
        self.play(Rotate(controls, angle=PI / 2, about_point=world.group.get_center()), run_time=2.0)
        for m, p in zip(controls, targets):
            m.generate_target(); m.target.move_to(p)
        self.play(*[MoveToTarget(m) for m in controls], run_time=1.4)
        self.at("suitable range")
        self.play(FadeIn(labs[0]), tv.animate.set_value(0.75), run_time=1.2)
        self.at("uses oxygen")
        self.play(FadeIn(labs[1]), vo.animate.set_value(0.45), run_time=1.2)
        self.at("only until")
        self.play(FadeIn(labs[2]), hf.animate.set_value(0.98), run_time=1.2)
        self.add(scope_tag("schematic"))
        self.play(world.speed.animate.set_value(0.50), run_time=2.0)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        world = pea_pathway(scale=0.72, center=(-1.3, -0.55, 0), rate=0.28, show_labels=False)
        line1 = T("Respiration releases stored food energy;", 34, TEXT, weight=BOLD)
        line2 = T("temperature, oxygen, and sugar change its rate.", 34, GOLD, weight=BOLD)
        rule = VGroup(line1, line2).arrange(DOWN, buff=0.15).move_to([0, 2.95, 0])
        rate = ValueTracker(0.35)
        d = dial(rate, center=[5.1, -0.15, 0], radius=1.25, label="respiration rate",
                 color=WORK, fmt="", scale=1, size=1)
        controls = VGroup(T("temperature", 28, HEAT), T("oxygen", 28, OXYGEN), T("sugar", 28, GLUCOSE))
        controls.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-5.5, -0.15, 0])
        self.play(FadeIn(world.group), run_time=0.8)
        self.at("stored food energy")
        self.play(Write(rule), run_time=1.4)
        self.at("temperature oxygen")
        self.play(FadeIn(controls, lag_ratio=0.25), FadeIn(d), run_time=1.1)
        self.play(rate.animate.set_value(0.78), world.speed.animate.set_value(0.58), run_time=2.2)
        self.at("picture gives")
        self.add(scope_tag("schematic"))
        self.play(rate.animate.set_value(0.48), world.speed.animate.set_value(0.36), run_time=1.3)
        self.at("real measurements")
        panel = RoundedRectangle(corner_radius=0.18, width=3.6, height=2.65,
                                 stroke_color=OXYGEN, stroke_width=4, fill_color=BG, fill_opacity=0.96)
        panel.move_to([4.95, -0.25, 0])
        panel_lab = fit_text("measure oxygen or carbon dioxide over time", max_w=3.1,
                             size=24, color=OXYGEN).move_to(panel)
        self.play(ReplacementTransform(d, panel), FadeIn(panel_lab), run_time=1.2)
        self.finish()


class S11Evidence(SpokenScene):
    def construct(self):
        frame = RoundedRectangle(corner_radius=0.22, width=11.3, height=5.87,
                                 stroke_color=OXYGEN, stroke_width=4).move_to([0, 0.09, 0])
        title = T("evidence", 40, OXYGEN, weight=BOLD).move_to([0, 3.5, 0])
        self.play(FadeIn(frame), FadeIn(title), run_time=0.8)
        self.at("real pea ranges")
        axes = VGroup(Line([-4.7, -1.65, 0], [-1.1, -1.65, 0], color=TEXT, stroke_width=4),
                      Line([-4.7, -1.65, 0], [-4.7, 1.55, 0], color=TEXT, stroke_width=4),
                      T("blank graph", 29, GREY).move_to([-2.9, 0.25, 0]))
        self.play(Create(axes), run_time=1.0)
        self.at("yeast values")
        table = VGroup(*[Line([0.0, y, 0], [4.65, y, 0], color=GREY, stroke_width=2)
                         for y in [-1.45, -0.55, 0.35, 1.25]],
                       Line([1.55, -1.45, 0], [1.55, 1.25, 0], color=GREY, stroke_width=2),
                       T("blank data table", 29, GREY).move_to([2.32, 1.72, 0]))
        self.play(Create(table), run_time=1.0)
        self.at("units or source")
        badges = VGroup(chip("units", GOLD, 28), chip("source notes", PURPLE, 28)).arrange(RIGHT, buff=0.45)
        badges.move_to([2.3, -2.20, 0])
        self.play(FadeIn(badges, lag_ratio=0.25), run_time=0.9)
        focus = SurroundingRectangle(axes, color=GOLD, buff=0.18, corner_radius=0.12, stroke_width=4)
        focus2 = SurroundingRectangle(table, color=GOLD, buff=0.32, corner_radius=0.12, stroke_width=4)
        focus3 = SurroundingRectangle(badges, color=GOLD, buff=0.18, corner_radius=0.12, stroke_width=4)
        self.play(Create(focus), run_time=0.8)
        self.play(Transform(focus, focus2), run_time=1.7)
        self.play(Transform(focus, focus3), run_time=1.7)
        self.at("compare complete data sets")
        self.play(FadeOut(focus), Indicate(frame, color=OXYGEN, scale_factor=1.01), run_time=1.0)
        gauge = Arc(radius=0.42, start_angle=PI, angle=-PI, color=GREY, stroke_width=6).move_to([-5.0, -3.15, 0])
        model = T("model, not evidence", 28, RED, weight=BOLD).next_to(gauge, RIGHT, buff=0.2)
        self.at("rather than trusting")
        self.play(FadeIn(gauge), FadeIn(model), run_time=0.8)
        self.finish()


class S12End(EndCard):
    LINE = "Respiration releases stored food energy;\ntemperature, oxygen, and sugar change its rate."
