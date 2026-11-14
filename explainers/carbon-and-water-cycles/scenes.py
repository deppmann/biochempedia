"""The Air Is a Tub — carbon-and-water-cycles explainer.

COLOR MAP
  TEAL       = the carbon-dioxide level in air
  GREEN      = photosynthesis / carbon flowing out of air
  ORANGE     = respiration / carbon flowing into air
  BROWN      = decomposition / carbon flowing into air
  RED        = fossil-fuel burning / carbon flowing into air
  OCEAN_BLUE = ocean exchange
  WATER_BLUE = water
  GREY       = structures and neutral annotations
"""
from bp_parts import *


ORANGE = "#F29E4C"
BROWN = "#A8825A"
OCEAN_BLUE = "#356C9A"
WATER_BLUE = "#65C7E8"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MLO_2025 = np.array([426.65, 427.09, 428.15, 429.64, 430.51, 429.61,
                     427.87, 425.48, 424.37, 424.87, 426.46, 427.49])


def flow_arrow(a, b, color, width=8):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=width, tip_length=0.28,
                 max_tip_length_to_length_ratio=0.22, max_stroke_width_to_length_ratio=12)


def volcano_station():
    """The hook picture, rebuilt as one object."""
    sea = Rectangle(width=12.6, height=1.1, stroke_width=0, fill_color=OCEAN_BLUE,
                    fill_opacity=0.55).move_to([0, -2.85, 0])
    mountain = Polygon([-5.7, -2.3, 0], [-1.6, -2.3, 0], [-3.65, 1.65, 0],
                       stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.20)
    cap = Polygon([-4.15, 0.7, 0], [-3.65, 1.65, 0], [-3.12, 0.64, 0],
                  stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.18)
    hut = VGroup(Rectangle(width=0.62, height=0.38, stroke_color=TEXT, stroke_width=3,
                           fill_color=TEXT, fill_opacity=0.15),
                 Line([-0.31, 0.19, 0], [0, 0.45, 0], color=TEXT, stroke_width=3),
                 Line([0, 0.45, 0], [0.31, 0.19, 0], color=TEXT, stroke_width=3)).move_to([-3.2, 0.55, 0])
    label = T("Mauna Loa, Hawaii", 30, TEXT, weight=BOLD).move_to([-3.65, -2.55, 0])
    station = T("station", 28, TEXT).next_to(hut, RIGHT, buff=0.22)
    return VGroup(sea, mountain, cap, hut, label, station)


def seasonal_wave(x0=-0.8, x1=6.0, y0=-1.3, y1=1.7, cycles=3.0):
    """A schematic seasonal wave for the hook; explicitly not a data curve."""
    pts = []
    for u in np.linspace(0, 1, 240):
        x = x0 + u * (x1 - x0)
        y = (y0 + y1) / 2 + 0.82 * np.sin(TAU * cycles * u + 0.55)
        pts.append([x, y, 0])
    line = VMobject(stroke_color=TEAL, stroke_width=7).set_points_as_corners(pts)
    return line


def ppm_grid():
    """One million pixels, of which exactly 400 are teal."""
    rng = np.random.default_rng(7)
    rgb = np.zeros((1000, 1000, 3), dtype=np.uint8)
    rgb[:] = np.array([83, 88, 96], dtype=np.uint8)
    picks = rng.choice(1_000_000, size=400, replace=False)
    rgb.reshape(-1, 3)[picks] = np.array([63, 184, 192], dtype=np.uint8)
    return ImageMobject(rgb).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"]).set_height(5.55)


def oak(cx=0.0, leafy=True):
    trunk = Polygon([cx - 0.35, -2.35, 0], [cx + 0.36, -2.35, 0],
                    [cx + 0.22, -0.45, 0], [cx - 0.18, -0.45, 0],
                    stroke_color=BROWN, stroke_width=4, fill_color=BROWN, fill_opacity=0.55)
    branches = VGroup(Line([cx, -0.65, 0], [cx - 0.8, 0.4, 0], color=BROWN, stroke_width=6),
                      Line([cx, -0.5, 0], [cx + 0.8, 0.5, 0], color=BROWN, stroke_width=6))
    crowns = VGroup(*[Ellipse(width=1.75, height=1.35, stroke_color=GREEN, stroke_width=3,
                             fill_color=GREEN, fill_opacity=0.30).move_to([cx + dx, 0.55 + dy, 0])
                      for dx, dy in [(-0.75, 0), (0, 0.45), (0.78, 0), (0, -0.12)]])
    if not leafy:
        crowns.set_opacity(0.12)
    return VGroup(trunk, branches, crowns)


def deer(cx=2.55):
    body = Ellipse(width=1.25, height=0.62, stroke_color=GOLD, stroke_width=3,
                   fill_color=GOLD, fill_opacity=0.22).move_to([cx, -1.76, 0])
    neck = Line([cx + 0.42, -1.58, 0], [cx + 0.62, -0.92, 0], color=GOLD, stroke_width=7)
    head = Ellipse(width=0.55, height=0.38, stroke_color=GOLD, stroke_width=3,
                   fill_color=GOLD, fill_opacity=0.22).move_to([cx + 0.72, -0.78, 0])
    legs = VGroup(*[Line([cx + dx, -1.96, 0], [cx + dx - 0.08, -2.38, 0], color=GOLD, stroke_width=4)
                    for dx in (-0.37, 0.33)])
    return VGroup(body, neck, head, legs)


def rotting_log(cx=4.55):
    log = RoundedRectangle(width=1.35, height=0.55, corner_radius=0.2, stroke_color=BROWN,
                           stroke_width=4, fill_color=BROWN, fill_opacity=0.35).move_to([cx, -2.08, 0])
    fungi = VGroup(*[Dot([cx + dx, -1.73 + dy, 0], radius=0.08, color=BROWN)
                     for dx, dy in [(-0.38, 0.04), (-0.05, 0.12), (0.31, 0.03)]])
    return VGroup(log, fungi)


def air_tub(ppm, cx=-4.65, width=2.65, height=4.8):
    """The carried air tub. ppm is a ValueTracker used by fill, marker and readout."""
    bottom, top = -2.25, 2.55
    left, right = cx - width / 2, cx + width / 2
    glass = RoundedRectangle(width=width, height=height, corner_radius=0.22,
                             stroke_color=TEXT, stroke_width=5, fill_color=GREY,
                             fill_opacity=0.06).move_to([cx, (bottom + top) / 2, 0])
    label = T("air", 32, TEXT, weight=BOLD).move_to([cx, (bottom + top) / 2 + height / 2 + 0.35, 0])
    label.layout_ok = True

    def level_y():
        return bottom + 0.55 + np.clip((ppm.get_value() - 423.0) / 9.0, 0, 1) * (height - 1.05)

    fill = always_redraw(lambda: Rectangle(width=width - 0.18, height=max(0.08, level_y() - bottom - 0.08),
                                            stroke_width=0, fill_color=TEAL, fill_opacity=0.13)
                         .move_to([cx, (bottom + 0.08 + level_y()) / 2, 0]))
    # The film is about moving, mixed air. These drifting carbon motes keep that subject alive
    # during spoken holds without changing the measured ppm value.
    rng = np.random.default_rng(19)
    motes = VGroup()
    for _ in range(36):
        d = Dot([rng.uniform(left + 0.18, right - 0.18), rng.uniform(bottom + 0.55, top - 0.2), 0],
                radius=0.09, color=TEAL).set_opacity(0.55)
        d.air_v = np.array([rng.uniform(-0.55, 0.55), rng.uniform(1.2, 1.8), 0])

        def drift(m, dt, glass=glass):
            m.shift(m.air_v * dt)
            gl, gr = glass.get_left()[0] + 0.12, glass.get_right()[0] - 0.12
            gb, gt = glass.get_bottom()[1] + 0.12, glass.get_top()[1] - 0.12
            if m.get_y() > gt:
                m.move_to([m.get_x(), gb, 0])
            if m.get_x() > gr:
                m.move_to([gl, m.get_y(), 0])
            elif m.get_x() < gl:
                m.move_to([gr, m.get_y(), 0])
        d.add_updater(drift)
        motes.add(d)
    marker = always_redraw(lambda: Line([left + 0.12, level_y(), 0], [right - 0.12, level_y(), 0],
                                        color=TEAL, stroke_width=8))
    read = counter("{:.1f} ppm", ppm, at=[cx, bottom + 0.28, 0], size=28, color=TEAL)
    read.layout_ok = True
    return VGroup(fill, motes, glass, marker, label, read), marker


def yard_world(ppm, leafy=True):
    """The one carried world, at identical scale and landmarks in every yard scene."""
    ground = Rectangle(width=7.65, height=0.55, stroke_width=0, fill_color=BROWN,
                       fill_opacity=0.25).move_to([2.55, -2.52, 0])
    tub, marker = air_tub(ppm)
    tree = oak(0.0, leafy=leafy)
    bob(tree[2], amp=0.12, speed=3.4)
    animal = deer(2.35)
    log = rotting_log(4.65)
    world = VGroup(tub, ground, tree, animal, log)
    return {"group": world, "tub": tub, "marker": marker, "tree": tree,
            "deer": animal, "log": log, "ground": ground}


def data_plot(include_curve=True, include_dots=True):
    """The 2025 Mauna Loa monthly panel, computed from lesson data."""
    P = Plot(box=(-0.45, 6.15, -1.70, 2.15), xr=(1, 12), yr=(423.5, 431.2),
             xticks=[(i, MONTHS[i - 1][0]) for i in range(1, 13)],
             yticks=[(424, "424"), (427, "427"), (430, "430")],
             xlabel="month (2025)", ylabel="CO₂ (ppm)", size=22, label_size=26)
    interp = lambda x: float(np.interp(x, np.arange(1, 13), MLO_2025))
    curve = P.curve(interp, color=TEAL, width=6, n=220) if include_curve else VGroup()
    dots = VGroup(*[Dot(P.pt(i, v), radius=0.09, color=TEAL) for i, v in enumerate(MLO_2025, 1)]) if include_dots else VGroup()
    source = T("data: NOAA + Scripps, Mauna Loa", 24, TEXT).move_to([3.15, 2.9, 0])
    frame = RoundedRectangle(width=7.6, height=6.0, corner_radius=0.18, stroke_color=GREY,
                             stroke_width=2.5).move_to([2.65, 0.15, 0])
    return P, curve, dots, source, frame, interp


def graph_and_tub(ppm_value=430.51):
    ppm = ValueTracker(ppm_value)
    tub, marker = air_tub(ppm)
    P, curve, dots, source, frame, interp = data_plot()
    divider = Line([-0.75, -2.9, 0], [-0.75, 3.15, 0], color=GREY, stroke_width=2)
    tag = T("model (schematic)", 24, TEXT).move_to([-4.65, -2.82, 0])
    return {"ppm": ppm, "tub": tub, "marker": marker, "plot": P, "curve": curve,
            "dots": dots, "source": source, "frame": frame, "divider": divider,
            "tag": tag, "interp": interp}


def prediction_backdrop():
    g = graph_and_tub(425.48)
    seg = g["plot"].curve(g["interp"], 7, 8, color=GOLD, width=11, n=30)
    lab = T("largest drop: −2.39 ppm", 28, GOLD, weight=BOLD).move_to([4.15, 2.42, 0])
    return VGroup(g["tub"], g["frame"], g["plot"], g["curve"], g["dots"],
                  g["source"], g["divider"], g["tag"], seg, lab)


def balance_icon(in_heavy=True, at=(4.8, 1.65, 0)):
    cx, cy, _ = at
    tilt = -0.22 if in_heavy else 0.22
    beam = Line([cx - 1.0, cy - tilt, 0], [cx + 1.0, cy + tilt, 0], color=TEXT, stroke_width=5)
    stem = Line([cx, cy - 0.05, 0], [cx, cy - 0.75, 0], color=TEXT, stroke_width=4)
    base = Line([cx - 0.45, cy - 0.75, 0], [cx + 0.45, cy - 0.75, 0], color=TEXT, stroke_width=4)
    out = T("out", 28, GREEN).move_to([cx - 0.86, cy - tilt + 0.35, 0])
    inn = T("in", 28, ORANGE).move_to([cx + 0.86, cy + tilt + 0.35, 0])
    return VGroup(beam, stem, base, out, inn)


class S00Title(TitleCard):
    LESSON = "Carbon and water cycles"
    TITLE = "The Air Is a Tub"


class S01Hook(SpokenScene):
    def construct(self):
        volcano = volcano_station()
        wave = seasonal_wave()
        station_dot = Dot([-3.2, 0.78, 0], radius=0.11, color=TEAL)
        question = question_card("down in summer… back up?", y=-3.2, size=34)
        measured = T("measured since 1958", 28, TEAL).move_to([2.75, 2.52, 0])
        schematic = T("seasonal pattern (schematic)", 24, TEXT).move_to([2.75, -2.1, 0])
        self.play(FadeIn(volcano), run_time=0.7)
        self.at("pulls the carbon dioxide")
        self.play(FadeIn(question.question, shift=UP * 0.1), run_time=0.6)
        self.at("pushes it back up")
        self.play(GrowFromCenter(station_dot), Create(wave), FadeIn(schematic), run_time=2.1)
        pulse(wave, base=7, amp=1.5, speed=2.5)
        bob(wave, amp=0.16, speed=4.0)
        self.at("Scientists on a Hawaiian volcano")
        self.play(Indicate(volcano, color=TEXT, scale_factor=1.02), run_time=0.7)
        self.at("every year since")
        self.play(FadeIn(measured), run_time=0.6)
        self.finish()


class S02Ppm(SpokenScene):
    def construct(self):
        grid = ppm_grid().move_to([-2.6, 0.15, 0])
        frame = Square(side_length=5.7, stroke_color=GREY, stroke_width=4).move_to(grid)
        ppm = M("400 ppm", 46, TEAL).move_to([3.7, 1.25, 0])
        meaning = fit_text("400 in every 1,000,000\nmolecules of air", max_w=4.6,
                           size=34, color=TEXT).move_to([3.7, -0.1, 0])
        tiny = T("a tiny part of the air", 30, TEAL, weight=BOLD).move_to([3.7, -1.65, 0])
        self.play(FadeIn(grid), Create(frame), run_time=1.2)
        bob(grid, amp=0.14, speed=4.2)
        self.at("parts per million")
        self.play(FadeIn(ppm), run_time=0.6)
        self.at("400 parts per million means")
        self.play(FadeIn(meaning, shift=LEFT * 0.15), run_time=0.8)
        self.at("million molecules of air")
        self.play(Indicate(grid, color=TEAL, scale_factor=1.01), run_time=1.1)
        self.at("only a tiny part")
        self.play(FadeIn(tiny), grid.animate.set_opacity(0.75), run_time=0.8)
        self.finish()


class S03Tub(SpokenScene):
    def construct(self):
        ppm = ValueTracker(426.0)
        world = yard_world(ppm)
        grid = ppm_grid().set_height(3.0).move_to([2.2, 0.5, 0])
        self.play(FadeIn(grid), run_time=0.7)
        self.at("way to think about it")
        self.play(grid.animate.set_height(0.55).move_to([-4.65, 1.0, 0]).set_opacity(0.15),
                  FadeIn(world["ground"]), run_time=1.0)
        self.at("air as a tub")
        self.play(FadeOut(grid), FadeIn(world["tub"]), run_time=0.8)
        self.at("holds carbon")
        self.play(FadeIn(world["tree"]), FadeIn(world["deer"]), FadeIn(world["log"]), run_time=1.0)
        self.at("marker on the side")
        pulse(world["marker"], base=8, amp=1.3, speed=2.5)
        self.play(ppm.animate.set_value(428.0), run_time=1.3)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Out(SpokenScene):
    def construct(self):
        ppm = ValueTracker(428.0)
        w = yard_world(ppm)
        self.add(w["group"], scope_tag("schematic"))
        drain = flow_arrow([-3.35, 0.65, 0], [-1.05, 0.75, 0], GREEN, 10)
        label = T("photosynthesis", 30, GREEN, weight=BOLD).move_to([-1.7, 2.25, 0])
        sugars = VGroup(*[Square(side_length=0.26, color=GOLD, fill_color=GOLD, fill_opacity=0.55)
                          for _ in range(5)]).arrange(RIGHT, buff=0.12).move_to([0, 0.5, 0])
        self.at("process drains the tub")
        self.play(GrowArrow(drain), run_time=0.8)
        self.at("Photosynthesis takes")
        self.play(FadeIn(label), run_time=0.5)
        self.at("out of the air")
        self.play(ppm.animate.set_value(426.5), run_time=1.4)
        self.at("oak in a Virginia yard")
        self.play(Indicate(w["tree"], color=GREEN, scale_factor=1.03), run_time=0.8)
        self.at("carbon into sugar")
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sugars], lag_ratio=0.18), run_time=1.1)
        bob(sugars, amp=0.035, speed=2.2)
        self.finish()


class S05In(SpokenScene):
    def construct(self):
        ppm = ValueTracker(426.5)
        w = yard_world(ppm)
        self.add(w["group"], scope_tag("schematic"))
        r1 = flow_arrow([0.15, 1.12, 0], [-1.8, 2.15, 0], ORANGE, 8)
        r2 = flow_arrow([2.55, -0.65, 0], [1.55, 1.55, 0], ORANGE, 8)
        respiration = T("respiration", 28, ORANGE, weight=BOLD).move_to([0.45, 2.55, 0])
        day = Circle(radius=0.24, color=YELLOW, fill_color=YELLOW, fill_opacity=0.55).move_to([4.95, 2.3, 0])
        night = Arc(radius=0.27, start_angle=-PI / 2, angle=PI, color=WATER_BLUE,
                    stroke_width=7).move_to([4.95, 2.3, 0])
        decomp = flow_arrow([4.65, -1.65, 0], [3.85, 0.45, 0], BROWN, 8)
        dl = T("decomposition", 28, BROWN, weight=BOLD).move_to([3.55, 0.8, 0])
        stack = VGroup(Rectangle(width=0.7, height=1.0, color=RED, fill_color=RED, fill_opacity=0.16),
                       Rectangle(width=0.23, height=0.9, color=RED, fill_color=RED, fill_opacity=0.22)
                       .shift(UP * 0.75 + RIGHT * 0.16)).move_to([5.65, -1.4, 0])
        burn = flow_arrow([5.65, -0.55, 0], [5.65, 1.25, 0], RED, 10)
        bl = T("burning", 28, RED, weight=BOLD).move_to([5.35, 1.65, 0])
        sea = Rectangle(width=2.0, height=0.5, stroke_width=0, fill_color=OCEAN_BLUE,
                        fill_opacity=0.65).move_to([3.6, -2.72, 0])
        ocean_a = DoubleArrow([2.8, -2.62, 0], [2.8, -1.3, 0], color=OCEAN_BLUE,
                              stroke_width=7, tip_length=0.22)
        ocean_l = T("ocean", 28, OCEAN_BLUE, weight=BOLD).move_to([3.75, -2.72, 0])
        self.at("Other processes fill it")
        self.play(ppm.animate.set_value(427.0), run_time=0.8)
        self.at("oak and the deer")
        self.play(GrowArrow(r1), GrowArrow(r2), FadeIn(respiration), run_time=0.9)
        self.at("day and night")
        self.play(FadeIn(day), run_time=0.35)
        self.play(ReplacementTransform(day, night), run_time=0.55)
        self.at("rotting log")
        self.play(GrowArrow(decomp), FadeIn(dl), run_time=0.8)
        self.at("Burning fuel")
        self.play(FadeIn(stack), GrowArrow(burn), FadeIn(bl), run_time=0.8)
        self.at("ocean takes some in")
        self.play(FadeIn(sea), GrowFromCenter(ocean_a), FadeIn(ocean_l), run_time=0.9)
        self.at("gives some back")
        self.play(Indicate(ocean_a, color=OCEAN_BLUE, scale_factor=1.08),
                  ppm.animate.set_value(428.0), run_time=1.0)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        ppm = ValueTracker(426.0)
        tub, marker = air_tub(ppm, cx=0, width=3.5, height=4.8)
        incoming = flow_arrow([-5.4, 0.6, 0], [-2.0, 0.6, 0], ORANGE, 14)
        outgoing = flow_arrow([2.0, -0.8, 0], [5.4, -0.8, 0], GREEN, 6)
        in_lab = T("in", 34, ORANGE, weight=BOLD).next_to(incoming, UP, buff=0.2)
        out_lab = T("out", 34, GREEN, weight=BOLD).next_to(outgoing, DOWN, buff=0.2)
        rise = T("in > out: level rises", 38, TEAL, weight=BOLD).move_to([0, 3.5, 0])
        fall = T("out > in: level falls", 38, TEAL, weight=BOLD).move_to([0, 3.5, 0])
        self.play(FadeIn(tub), run_time=0.6)
        self.at("Now the rule")
        self.play(GrowArrow(incoming), GrowArrow(outgoing), FadeIn(in_lab), FadeIn(out_lab), run_time=0.8)
        self.at("more flows in")
        self.play(FadeIn(rise), ppm.animate.set_value(430.0), run_time=1.6)
        incoming2 = flow_arrow([-5.4, 0.6, 0], [-2.0, 0.6, 0], ORANGE, 6)
        outgoing2 = flow_arrow([2.0, -0.8, 0], [5.4, -0.8, 0], GREEN, 14)
        self.at("goes down only")
        self.play(Transform(incoming, incoming2), Transform(outgoing, outgoing2), swap(rise, fall), run_time=1.0)
        self.at("more flows out")
        self.play(ppm.animate.set_value(424.8), run_time=1.8)
        pulse(marker, base=8, amp=1.4, speed=2.3)
        self.finish()


class S07Summer(SpokenScene):
    def construct(self):
        ppm = ValueTracker(430.0)
        w = yard_world(ppm, leafy=False)
        self.add(w["group"], scope_tag("model (schematic)"))
        months = VGroup(*[T(m, 28, TEXT) for m in ["Apr", "May", "Jun", "Jul", "Aug"]]).arrange(RIGHT, buff=0.48)
        months.move_to([0.8, -3.18, 0])
        cursor = Underline(months[0], color=TEAL, stroke_width=6)
        photo = flow_arrow([-3.35, 0.6, 0], [-1.2, 0.8, 0], GREEN, 5)
        pl = T("photosynthesis", 28, GREEN, weight=BOLD).move_to([-1.7, 2.3, 0])
        resp = flow_arrow([0.3, 1.1, 0], [-1.55, 2.0, 0], ORANGE, 6)
        decomp = flow_arrow([4.55, -1.65, 0], [3.95, 0.1, 0], BROWN, 5)
        balance = balance_icon(False)
        self.play(FadeIn(months), run_time=0.5)
        self.at("spring the oak's leaves open")
        self.play(w["tree"][2].animate.set_opacity(1), GrowFromCenter(cursor), run_time=1.0)
        self.at("photosynthesis speeds up")
        photo2 = flow_arrow([-3.35, 0.6, 0], [-1.2, 0.8, 0], GREEN, 14)
        self.play(GrowArrow(photo), FadeIn(pl), Transform(photo, photo2), run_time=1.0)
        self.at("oak still respires")
        self.play(GrowArrow(resp), run_time=0.7)
        self.at("log still rots")
        self.play(GrowArrow(decomp), run_time=0.7)
        self.at("out beats in")
        self.play(FadeIn(balance), run_time=0.6)
        self.at("level falls")
        self.play(ppm.animate.set_value(424.9), cursor.animate.become(Underline(months[-1], color=TEAL, stroke_width=6)),
                  run_time=2.2, rate_func=linear)
        self.finish()


class S08Fall(SpokenScene):
    def construct(self):
        ppm = ValueTracker(424.8)
        w = yard_world(ppm, leafy=True)
        self.add(w["group"], scope_tag("model (schematic)"))
        months = VGroup(*[T(m, 28, TEXT) for m in ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]]).arrange(RIGHT, buff=0.28)
        months.move_to([0.65, -3.18, 0])
        cursor = Underline(months[0], color=TEAL, stroke_width=6)
        photo = flow_arrow([-3.35, 0.6, 0], [-1.2, 0.8, 0], GREEN, 12)
        resp = flow_arrow([0.25, 1.05, 0], [-1.55, 2.0, 0], ORANGE, 6)
        decomp = flow_arrow([4.55, -1.65, 0], [3.95, 0.1, 0], BROWN, 6)
        leaves = VGroup(*[Ellipse(width=0.18, height=0.32, color=GREEN, fill_color=GREEN, fill_opacity=0.8)
                          .move_to([x, y, 0]) for x, y in [(-0.7, 0.7), (0.1, 0.9), (0.65, 0.5), (-0.2, 0.2)]])
        balance = balance_icon(True)
        self.add(months, cursor, photo)
        self.at("photosynthesis slows")
        photo2 = flow_arrow([-3.35, 0.6, 0], [-1.2, 0.8, 0], GREEN, 3)
        self.play(Transform(photo, photo2), run_time=0.8)
        self.at("oak drops its leaves")
        self.play(w["tree"][2].animate.set_opacity(0.12),
                  *[leaf.animate.shift(DOWN * 2.0 + RIGHT * (i - 1.5) * 0.12).set_color(BROWN)
                    for i, leaf in enumerate(leaves)], run_time=1.3)
        self.at("Respiration and decomposition")
        self.play(GrowArrow(resp), GrowArrow(decomp), run_time=0.9)
        self.at("one beats out")
        self.play(FadeIn(balance), run_time=0.6)
        self.at("level rises")
        self.play(ppm.animate.set_value(429.7), cursor.animate.become(Underline(months[-1], color=TEAL, stroke_width=6)),
                  run_time=2.2, rate_func=linear)
        self.finish()


class S09Record(SpokenScene):
    def construct(self):
        g = graph_and_tub(430.51)
        t = ValueTracker(1.0)
        live = g["plot"].live_curve(g["interp"], t, color=TEAL, width=6, x0=1)
        dot = g["plot"].dot(lambda: t.get_value(), lambda: g["interp"](t.get_value()), color=TEXT, ring=TEAL)
        guide = always_redraw(lambda: Line(g["plot"].pt(t.get_value(), 423.5),
                                           g["plot"].pt(t.get_value(), 431.2),
                                           color=TEAL, stroke_width=10).set_opacity(0.28))
        note = T("measures the air — not each flow", 26, TEXT).move_to([3.05, -3.25, 0])
        may_ring = Circle(radius=0.19, color=GOLD, stroke_width=6).move_to(g["plot"].pt(5, MLO_2025[4]))
        may = T("May: 430.51 ppm", 28, GOLD, weight=BOLD).move_to([3.2, 2.42, 0])
        self.play(FadeIn(g["tub"]), FadeIn(g["tag"]), Create(g["divider"]), run_time=0.7)
        self.at("Real air shows")
        panel = VGroup(g["frame"], g["plot"], g["source"])
        self.play(FadeIn(panel, shift=LEFT * 0.35), run_time=1.2)
        self.at("record from Mauna Loa")
        self.add(live, guide, dot)
        self.play(t.animate.set_value(12), run_time=4.2, rate_func=linear)
        self.at("measures the air itself")
        self.play(FadeIn(note), run_time=0.7)
        self.at("highest month is May")
        self.play(FadeIn(may_ring), FadeIn(may), run_time=0.7)
        self.at("falls all summer")
        self.play(t.animate.set_value(9), g["ppm"].animate.set_value(424.37), run_time=1.7, rate_func=linear)
        self.finish()


class S10Predict(SpokenScene):
    def construct(self):
        back = prediction_backdrop()
        self.add(back)
        q = question_card("Is August the lowest month?", y=-3.16, size=34)
        seg = back[-2]
        pulse(seg, base=11, amp=2.0, speed=2.4)
        self.at("July to August")
        self.play(Indicate(seg, color=GOLD, scale_factor=1.02), run_time=0.8)
        self.at("dropped the most")
        self.play(FadeIn(back[-1]), run_time=0.6)
        self.at("is August the lowest month")
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.8)
        self.at("Pause and decide")
        self.play(Indicate(q.question, color=GOLD, scale_factor=1.04), run_time=0.7)
        self.finish()


class S11Pause(PredictPause):
    QUESTION = "Is August the lowest month?"
    CARD = {"y": -3.16, "size": 34}

    def backdrop(self):
        return prediction_backdrop()

    def construct(self):
        self.add(self.backdrop())
        self.add(question_card(self.QUESTION, y=-3.16, size=34))
        ring, run = countdown(self.SECONDS, center=(5.75, -3.0, 0), radius=0.72)
        self.add(ring)
        self.play(run)
        self.finish()


class S12Reveal(SpokenScene):
    def construct(self):
        g = graph_and_tub(425.48)
        self.add(g["tub"], g["tag"], g["divider"], g["frame"], g["plot"],
                 g["curve"], g["dots"], g["source"])
        cursor_x = ValueTracker(8)
        cursor = g["plot"].dot(lambda: cursor_x.get_value(), lambda: g["interp"](cursor_x.get_value()),
                               color=TEXT, ring=GOLD, radius=0.14)
        self.add(cursor)
        sep = T("September 2025\n424.37 ppm\nlowest", 28, GOLD, weight=BOLD,
                line_spacing=0.72).move_to([4.25, 2.25, 0])
        octo = T("October: higher again", 28, TEAL, weight=BOLD).move_to([4.1, 2.43, 0])
        rule = T("model: stops falling\nwhen out no longer beats in", 24, TEXT,
                 line_spacing=0.8).move_to([-4.65, -2.95, 0])
        self.at("monthly average kept falling")
        self.play(cursor_x.animate.set_value(9), g["ppm"].animate.set_value(424.37), run_time=1.6)
        self.at("September the lowest month")
        self.play(FadeOut(g["source"]), FadeIn(sep), run_time=0.7)
        self.at("October it was higher")
        self.play(cursor_x.animate.set_value(10), g["ppm"].animate.set_value(424.87), swap(sep, octo), run_time=1.1)
        self.at("tub keeps draining")
        self.play(g["ppm"].animate.set_value(424.15), run_time=1.0)
        self.at("as long as outbeats in")
        self.play(FadeOut(g["tag"]), FadeIn(rule), run_time=0.7)
        self.at("bottom comes after")
        self.play(g["ppm"].animate.set_value(425.2), Indicate(cursor, color=GOLD, scale_factor=1.15), run_time=1.3)
        self.finish()


class S13Climb(SpokenScene):
    def construct(self):
        ppm = ValueTracker(424.0)
        tub, marker = air_tub(ppm)
        timeline = Line([-5.7, -2.95, 0], [5.8, -2.95, 0], color=TEXT, stroke_width=5)
        y1958 = T("1958", 28, TEXT).move_to([-5.55, -3.35, 0])
        y2025 = T("2025", 28, TEXT).move_to([5.55, -3.35, 0])
        coal = RoundedRectangle(width=3.0, height=0.72, corner_radius=0.18, stroke_color=BROWN,
                                stroke_width=4, fill_color=BROWN, fill_opacity=0.28).move_to([3.4, -1.85, 0])
        coal_l = T("old carbon underground", 28, BROWN, weight=BOLD).move_to(coal)
        coal_l.layout_ok = True
        burn = flow_arrow([3.4, -1.4, 0], [3.4, 1.55, 0], RED, 6)
        burn_l = T("burning coal, oil + gas", 30, RED, weight=BOLD).move_to([3.65, 2.05, 0])
        balance = balance_icon(True, at=(3.6, 0.1, 0))
        self.play(FadeIn(tub), Create(timeline), FadeIn(y1958), FadeIn(y2025), run_time=0.8)
        self.at("step back to many years")
        self.play(ppm.animate.set_value(426.0), run_time=1.0)
        self.at("Burning coal oil and gas")
        self.play(FadeIn(coal), FadeIn(coal_l), GrowArrow(burn), FadeIn(burn_l), run_time=1.1)
        burn2 = flow_arrow([3.4, -1.4, 0], [3.4, 1.55, 0], RED, 14)
        self.at("old carbon from underground")
        self.play(Transform(burn, burn2), run_time=1.0)
        self.at("Each year a little more")
        self.play(FadeIn(balance), ppm.animate.set_value(430.5), run_time=1.8)
        self.finish()


class S14Same(SpokenScene):
    def construct(self):
        P = Plot(box=(-5.5, 5.8, -2.1, 2.15), xr=(1958, 2025), yr=(310, 435),
                 xticks=[(1958, "1958"), (2025, "2025")],
                 yticks=[(317.51, "317.51"), (430.51, "430.51")],
                 xlabel="same month across years", ylabel="CO₂ (ppm)", size=24, label_size=28)
        a = Dot(P.pt(1958, 317.51), radius=0.13, color=TEAL)
        b = Dot(P.pt(2025, 430.51), radius=0.13, color=TEAL)
        rise = Line(a.get_center(), b.get_center(), color=TEAL, stroke_width=8)
        may1 = T("May 1958", 28, TEAL).next_to(a, UP, buff=0.18)
        may2 = T("May 2025", 28, TEAL).next_to(b, DOWN, buff=0.18)
        same = T("same month: the climb", 32, TEAL, weight=BOLD).move_to([-2.25, 3.1, 0])
        sep = Dot(P.pt(2025, 424.37), radius=0.12, color=GREY)
        swing = Line(P.pt(2025, 424.37), P.pt(2025, 430.51), color=GREY, stroke_width=8)
        swing_l = T("May → September: yearly swing", 28, TEXT).move_to([3.35, 3.1, 0])
        tag = scope_tag("schematic comparison")
        guide = Line(P.pt(1958, 310), P.pt(1958, 435), color=TEAL,
                     stroke_width=9).set_opacity(0.24)
        guide.scan_t = 0.0

        def scan(mob, dt):
            mob.scan_t += dt
            year = 1958 + (2025 - 1958) * (0.5 + 0.5 * np.sin(1.25 * mob.scan_t - PI / 2))
            mob.put_start_and_end_on(P.pt(year, 310), P.pt(year, 435))
        self.play(FadeIn(P), FadeIn(tag), run_time=0.7)
        self.at("whole record climbs")
        self.play(FadeIn(a), Create(rise), FadeIn(b), run_time=1.6)
        self.at("same month across the years")
        guide.add_updater(scan)
        self.play(FadeIn(may1), FadeIn(may2), FadeIn(same), FadeIn(guide), run_time=0.9)
        self.at("May with May")
        self.play(Indicate(VGroup(a, b), color=TEAL, scale_factor=1.12), run_time=0.8)
        self.at("May against September")
        self.play(FadeIn(sep), Create(swing), FadeIn(swing_l), run_time=1.0)
        self.at("yearly swing")
        self.play(Indicate(swing, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.finish()


class S15Recap(SpokenScene):
    def construct(self):
        panels = TwoPanel("yearly swing", "long climb", colors=(GREEN, RED), top=3.0, bottom=-2.5,
                          gap=2.8, width=13.5)
        left_p = Plot(box=(-6.1, -1.9, -1.55, 1.65), xr=(1, 12), yr=(423.5, 431.2),
                      xticks=[(1, "Jan"), (5, "May"), (9, "Sep"), (12, "Dec")],
                      yticks=[(424, "424"), (430, "430")], xlabel="2025", ylabel="ppm",
                      size=22, label_size=26)
        interp = lambda x: float(np.interp(x, np.arange(1, 13), MLO_2025))
        swing = left_p.curve(interp, color=TEAL, width=7)
        right_p = Plot(box=(2.3, 6.25, -1.55, 1.65), xr=(1958, 2025), yr=(310, 435),
                       xticks=[(1958, "1958"), (2025, "2025")],
                       yticks=[(318, "318"), (431, "431")], xlabel="May with May", ylabel="ppm",
                       size=22, label_size=26)
        climb_fn = lambda year: 317.51 + (430.51 - 317.51) * (year - 1958) / (2025 - 1958)
        climb = right_p.curve(climb_fn, color=RED, width=7)
        tub_ppm = ValueTracker(427.0)
        mini, _ = air_tub(tub_ppm, cx=0.0, width=2.4)
        left_rule = T("out beats in → then in beats out", 26, GREEN).move_to([-4.05, -2.9, 0])
        right_rule = T("mostly burning: a little more in", 26, RED).move_to([4.05, -2.9, 0])
        self.play(FadeIn(panels), FadeIn(mini), run_time=0.7)
        self.at("One tub two patterns")
        self.play(Indicate(mini, color=TEAL, scale_factor=1.06), run_time=0.7)
        self.at("yearly swing")
        self.play(FadeIn(left_p), Create(swing), run_time=1.1)
        self.at("plants taking out more")
        self.play(FadeIn(left_rule), tub_ppm.animate.set_value(424.5), run_time=1.2)
        self.at("then less")
        self.play(tub_ppm.animate.set_value(428.0), run_time=1.0)
        self.at("long climb")
        self.play(FadeIn(right_p), Create(climb), run_time=1.1)
        self.at("mostly from burning")
        self.play(FadeIn(right_rule), Indicate(climb, color=RED, scale_factor=1.05), run_time=0.8)
        self.finish()


class S16End(EndCard):
    LINE = "The level moves only when in and out are unequal."
