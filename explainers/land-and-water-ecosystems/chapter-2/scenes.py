"""Following Salt Down the James — chapter 2.

COLOR MAP (continued exactly from chapter 1)
  GREEN  living things and living interactions
  GOLD   nonliving conditions and measured salinity
  BLUE   fresh water
  PURPLE salty water and salt
  TEAL   mixed estuary water
  ORANGE oysters and oyster habitat
  RED    danger / unsuitable prolonged low salinity
  TEXT   labels

The James-to-ocean picture is rebuilt through ``james_world`` so its landmarks never drift.
All station heights use the eight means printed in the lesson table.
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
STATIONS = ["TF5.5", "RET5.2", "LE5.1", "LE5.2", "LE5.3", "LE5.4", "CB8.1", "CB7.4"]
SALINITY = [0.09, 1.32, 4.53, 11.54, 15.39, 20.67, 23.06, 25.78]
XS = np.linspace(-5.45, 5.45, 8)


def oyster(center=(0, 0, 0), scale=1.0, color=ORANGE, opacity=1.0):
    """A labelled-cartoon oyster shell, not an anatomical drawing."""
    c = np.array(center, dtype=float)
    shell = Arc(radius=0.46 * scale, start_angle=0.05, angle=PI - 0.1,
                color=color, stroke_width=7).move_arc_center_to(c)
    base = ArcBetweenPoints(c + LEFT * 0.46 * scale, c + RIGHT * 0.46 * scale,
                            angle=-0.55, color=color, stroke_width=7)
    ribs = VGroup(*[Line(c + DOWN * 0.08 * scale,
                         c + scale * np.array([dx, 0.35 - 0.25 * abs(dx), 0]),
                         color=color, stroke_width=3)
                    for dx in (-0.34, -0.17, 0, 0.17, 0.34)])
    g = VGroup(shell, base, ribs).set_opacity(opacity)
    return g


def boat(x=-5.35, y=-0.25, scale=1.0):
    hull = Polygon([-0.52, 0.05, 0], [0.48, 0.05, 0], [0.3, -0.25, 0],
                   [-0.36, -0.25, 0], color=TEXT, stroke_width=3,
                   fill_color=TEXT, fill_opacity=0.16)
    mast = Line([0, 0.05, 0], [0, 0.54, 0], color=TEXT, stroke_width=3)
    flag = Polygon([0.02, 0.5, 0], [0.35, 0.38, 0], [0.02, 0.29, 0],
                   color=GOLD, fill_color=GOLD, fill_opacity=0.85, stroke_width=2)
    return VGroup(hull, mast, flag).scale(scale).move_to([x, y, 0])


def reef(center=(2.9, -1.25, 0), scale=1.0):
    x, y, _ = center
    return VGroup(*[oyster([x + dx * scale, y + dy * scale, 0], 0.45 * scale)
                    for dx, dy in ((-0.7, 0), (-0.25, 0.28), (0.25, 0.2), (0.7, -0.02))])


def flow_motes(y=-0.55, seed=7):
    """Continuously moving water markers; wrapping preserves the fixed river geometry."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(22):
        x = rng.uniform(-5.7, 5.7)
        yy = y + rng.uniform(-0.55, 0.55)
        col = BLUE if x < -1 else (TEAL if x < 3.2 else PURPLE)
        d = Line([x - 0.13, yy, 0], [x + 0.13, yy, 0], color=col,
                 stroke_width=4).set_opacity(0.75)
        d.speed = 0.24 + 0.05 * (i % 4)

        def drift(m, dt):
            m.shift(RIGHT * m.speed * dt)
            if m.get_x() > 5.75:
                m.shift(LEFT * 11.5)
        d.add_updater(drift)
        g.add(d)
    return g


def james_world(labels=True, boat_x=None, station_ticks=False, mix_center=1.0):
    """The one carried Virginia landscape, always at the same scale and place."""
    land = VGroup(
        Polygon([-6.1, 0.2, 0], [-5.4, 2.35, 0], [-4.7, 0.2, 0],
                color=GREY, fill_color=GREY, fill_opacity=0.26, stroke_width=3),
        Polygon([-5.4, 0.2, 0], [-4.7, 1.72, 0], [-3.9, 0.2, 0],
                color=GREY, fill_color=GREY, fill_opacity=0.2, stroke_width=3),
    )
    trees = VGroup(*[VGroup(Line([x, 0.2, 0], [x, 0.7, 0], color=GREY, stroke_width=4),
                              Circle(0.28, color=GREEN, fill_color=GREEN, fill_opacity=0.45).move_to([x, 0.86, 0]))
                     for x in (-5.9, -5.1, -4.25)])
    water = VGroup()
    n = 48
    for i in range(n):
        x0 = -5.8 + i * 11.6 / n
        t = i / (n - 1)
        # A movable fresh/mixed boundary, used in the seasonal-shift scene.
        mix_t = np.clip((x0 - (mix_center - 2.4)) / 5.0, 0, 1)
        col = interpolate_color(ManimColor(BLUE), ManimColor(TEAL), min(1, mix_t * 1.35))
        if t > 0.72:
            col = interpolate_color(ManimColor(TEAL), ManimColor(PURPLE), (t - 0.72) / 0.28)
        band = Rectangle(width=11.6 / n + 0.012, height=1.55, stroke_width=0,
                         fill_color=col, fill_opacity=0.62).move_to([x0 + 5.8 / n, -0.55, 0])
        band.shimmer_t = i * 0.15

        def shimmer(m, dt):
            m.shimmer_t += dt
            m.set_fill(opacity=0.56 + 0.12 * np.sin(1.7 * m.shimmer_t))
        band.add_updater(shimmer)
        water.add(band)
    edge = Rectangle(width=11.6, height=1.55, color=GREY, stroke_width=3).move_to([0, -0.55, 0])
    shore = Line([-6.1, -1.45, 0], [6.1, -1.45, 0], color=GREY, stroke_width=4)
    g = VGroup(land, trees, water, edge, shore, flow_motes())
    if labels:
        labs = VGroup(T("upper James", 28, BLUE).move_to([-4.15, -1.95, 0]),
                      T("Chesapeake estuary", 28, TEAL).move_to([0.75, -1.95, 0]),
                      T("ocean", 28, PURPLE).move_to([5.05, -1.95, 0]))
        g.add(labs)
    if station_ticks:
        ticks = VGroup(*[Line([x, -1.3, 0], [x, -1.05, 0], color=GOLD, stroke_width=3) for x in XS])
        g.add(ticks)
        g.ticks = ticks
    if boat_x is not None:
        b = bob(boat(boat_x, 0.28, 0.9), amp=0.035, speed=2.2)
        g.add(b)
        g.boat = b
    return g


def station_plot(bottom=-0.55, top=2.6, include_world=True):
    """Large exact data strip: point heights are computed from SALINITY."""
    p = Plot(box=(-5.45, 5.45, bottom, top), xr=(0, 7), yr=(0, 28),
             xticks=[], yticks=[(0, "0"), (10, "10"), (20, "20"), (28, "28")],
             ylabel="mean salinity (PSU)", color=GREY, size=22, label_size=28)
    area_pts = [p.pt(0, 0), *[p.pt(i, v) for i, v in enumerate(SALINITY)], p.pt(7, 0)]
    wash = Polygon(*area_pts, stroke_width=0, fill_color=GOLD, fill_opacity=0.09).set_z_index(-2)
    wash.shimmer_t = 0.0

    def wash_shimmer(m, dt):
        m.shimmer_t += dt
        m.set_fill(opacity=0.05 + 0.12 * (1 + np.sin(4.0 * m.shimmer_t)))
    wash.add_updater(wash_shimmer)
    p.add(wash)
    pts = VGroup(*[Dot(p.pt(i, v), radius=0.11, color=GOLD) for i, v in enumerate(SALINITY)])
    line = pulse(VMobject(color=GOLD, stroke_width=5).set_points_as_corners(
        [p.pt(i, v) for i, v in enumerate(SALINITY)]), base=5, amp=1.3, speed=2.4)
    codes = VGroup(*[T(code, 22, TEXT).rotate(PI / 4).next_to(p.pt(i, 0), DOWN, buff=0.14)
                     for i, code in enumerate(STATIONS)])
    values = VGroup(*[M(f"{v:.2f}", 22, GOLD).next_to(p.pt(i, v), UP if i == 0 else UL, buff=0.1 if i else 0.32)
                      for i, v in enumerate(SALINITY)])
    return p, line, pts, codes, values


def predict_backdrop(with_question=False):
    w = james_world(labels=False, boat_x=-0.78, station_ticks=True)
    # Exact points compressed over the fixed river, so the river remains the base layer.
    base, span = 0.9, 1.65
    pts = VGroup(*[Dot([x, base + span * v / 28, 0], radius=0.09, color=GOLD) for x, v in zip(XS, SALINITY)])
    line = VMobject(color=GOLD, stroke_width=4).set_points_as_corners([p.get_center() for p in pts])
    ghost = oyster([-0.2, -0.15, 0], 0.85, ORANGE, 0.28)
    ghost.phase = 0.0

    def drift(m, dt):
        m.phase += dt
        m.move_to([-0.2 + 2.0 * np.sin(0.35 * m.phase), -0.15, 0])
    ghost.add_updater(drift)
    g = VGroup(w, line, pts, ghost)
    if with_question:
        g.add(question_card("Where does an oyster first fit?", y=-3.13, size=32, color=ORANGE))
    return g


class S01Link(SpokenScene):
    def construct(self):
        world = james_world(labels=True, boat_x=0.4)
        living = Circle(1.05, color=GREEN, stroke_width=7).move_to([-1.15, 1.9, 0])
        nonliving = Circle(1.05, color=GOLD, stroke_width=7).move_to([1.15, 1.9, 0])
        living_l = T("living", 28, GREEN).move_to(living)
        non_l = T("nonliving", 28, GOLD).move_to(nonliving)
        self.play(FadeIn(world), run_time=1.0)
        self.at("first film separated")
        self.play(Create(living), Create(nonliving), FadeIn(living_l), FadeIn(non_l), run_time=1.6)
        self.at("one non living condition")
        self.play(FadeOut(living), FadeOut(living_l), nonliving.animate.scale(1.35).move_to([0, 1.85, 0]),
                  non_l.animate.move_to([0, 1.85, 0]), run_time=1.2)
        oq = oyster([0.4, 0.65, 0], 0.8)
        q = T("?", 48, RED, weight=BOLD).next_to(oq, UP, buff=0.05)
        self.at("predict where oysters")
        self.play(FadeOut(nonliving), FadeOut(non_l), FadeIn(oq, scale=0.7), FadeIn(q), run_time=0.8)
        self.at("same Virginia landscape")
        self.play(Indicate(world[0], color=TEXT), run_time=1.1)
        salt = VGroup(*[Dot([x, -0.55, 0], radius=0.055, color=GOLD) for x in np.linspace(-4.8, 5.25, 13)])
        self.at("Follow salt")
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.18) for d in salt], lag_ratio=0.08),
                  world.boat.animate.move_to([5.0, 0.28, 0]), run_time=3.0)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Land and water ecosystems"
    TITLE = "Following Salt Down the James"


class S03Salinity(SpokenScene):
    def construct(self):
        world = james_world(labels=False)
        self.play(FadeIn(world), run_time=0.8)
        salt = VGroup(*[Dot([x, -0.65 + 0.38 * np.sin(i), 0], radius=0.055, color=GOLD)
                        for i, x in enumerate(np.linspace(-4.8, 5.45, 16))])
        self.at("Salinity is")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in salt], lag_ratio=0.05), run_time=1.7)
        sal_lab = T("salinity", 34, GOLD, weight=BOLD).move_to([0, 2.95, 0])
        self.play(FadeIn(sal_lab), run_time=0.5)
        ends = VGroup(T("fresh", 32, BLUE).move_to([-3.25, 1.55, 0]),
                      T("salty", 32, PURPLE).move_to([3.65, 1.55, 0]))
        self.at("upper James is fresh")
        self.play(FadeIn(ends[0]), run_time=0.6)
        self.at("ocean water is salty")
        self.play(FadeIn(ends[1]), run_time=0.6)
        arrows = VGroup(Arrow([-4.6, 0.8, 0], [-0.4, 0.8, 0], color=BLUE, stroke_width=7),
                        Arrow([4.8, 0.55, 0], [0.6, 0.55, 0], color=PURPLE, stroke_width=7))
        mix = T("mix", 36, TEAL, weight=BOLD).move_to([0.1, 0.75, 0])
        self.at("river water and ocean water")
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=1.5)
        self.at("mix")
        self.play(FadeIn(mix, scale=0.6), run_time=0.5)
        level = ValueTracker(0.04)
        gauge = dial(level, [5.05, 2.5, 0], radius=0.85, label="salinity", color=GOLD,
                     fmt="{:.0f}", scale=28, size=30)
        marker = Dot([-5.1, -0.55, 0], radius=0.12, color=GOLD)
        self.at("Salinity usually rises")
        self.play(FadeOut(arrows), FadeOut(mix), FadeIn(gauge), FadeIn(marker), run_time=0.6)
        self.play(marker.animate.move_to([5.1, -0.55, 0]), level.animate.set_value(0.92), run_time=2.3, rate_func=linear)
        self.at("mixing zone can move")
        self.play(salt.animate.shift(RIGHT * 0.45), run_time=0.65)
        self.play(salt.animate.shift(LEFT * 0.75), run_time=0.65)
        self.finish()


class S04Stations(SpokenScene):
    def construct(self):
        world = james_world(labels=False, boat_x=XS[0], station_ticks=True)
        self.add(world)
        self.at("sampling boat starts")
        self.play(FadeIn(world.boat, shift=RIGHT * 0.2), run_time=0.7)
        probe = Line(world.boat.get_bottom(), world.boat.get_bottom() + DOWN * 0.9, color=GOLD, stroke_width=4)
        depth = T("1 m", 28, GOLD).next_to(probe, RIGHT, buff=0.12)
        self.at("probe measures")
        self.play(Create(probe), FadeIn(depth), run_time=0.8)
        self.play(FadeOut(probe), FadeOut(depth), run_time=0.35)
        base, span = 0.8, 1.85
        pts, segs, labels = VGroup(), VGroup(), VGroup()
        for i, (x, value, code) in enumerate(zip(XS, SALINITY, STATIONS)):
            y = base + span * value / 28
            d = Dot([x, y, 0], radius=0.1, color=GOLD)
            lab = VGroup(T(code, 22, TEXT), M(f"{value:.2f}", 22, GOLD)).arrange(DOWN, buff=0.03)
            lab.move_to([x, 3.05, 0])
            if i:
                segs.add(Line(pts[-1].get_center(), d.get_center(), color=GOLD, stroke_width=4))
            pts.add(d); labels.add(lab)
        self.at("Each stop adds")
        for i in range(8):
            animations = [world.boat.animate.move_to([XS[i], 0.28, 0]), FadeIn(pts[i], scale=0.4), FadeIn(labels[i])]
            if i:
                animations.append(Create(segs[i - 1]))
            self.play(*animations, run_time=0.62)
        self.at("points climb")
        self.play(LaggedStart(*[Indicate(p, color=GOLD, scale_factor=1.35) for p in pts], lag_ratio=0.08),
                  run_time=1.5)
        self.at("toward the bay")
        self.play(world.boat.animate.shift(RIGHT * 0.2), run_time=0.6)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        self.add(back)
        oy = oyster([-0.78, 0.85, 0], 0.9)
        self.at("place an oyster")
        self.play(FadeIn(oy, scale=0.6), run_time=0.8)
        q = question_card("Where does an oyster first fit?", y=-3.13, size=32, color=ORANGE)
        self.at("Where along this fresh")
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.9)
        self.at("Make a prediction")
        self.play(Indicate(q.question, color=ORANGE, scale_factor=1.03), run_time=0.8)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Where does an oyster first fit?"
    SECONDS = 4.5
    CARD = {"y": -3.13, "size": 32, "color": ORANGE}

    def backdrop(self):
        return predict_backdrop()


class S07Reveal(SpokenScene):
    def construct(self):
        world = james_world(labels=False, station_ticks=True)
        self.add(world)
        suitable = Line([XS[3], -2.0, 0], [XS[7], -2.0, 0], color=ORANGE, stroke_width=8)
        ends = VGroup(Line([XS[3], -1.78, 0], [XS[3], -2.2, 0], color=ORANGE, stroke_width=6),
                      Line([XS[7], -1.78, 0], [XS[7], -2.2, 0], color=ORANGE, stroke_width=6))
        guide = T("10–28 PSU", 32, ORANGE, weight=BOLD).next_to(suitable, DOWN, buff=0.2)
        oy = oyster([XS[3] + 0.25, -0.45, 0], 1.0)
        self.at("first fits the brackish")
        self.play(Create(suitable), Create(ends), FadeIn(guide), FadeIn(oy, scale=0.6), run_time=1.3)
        ghost = oyster([XS[0], -0.45, 0], 1.0, ORANGE, 0.22)
        cross = VGroup(Line([-0.25, -0.25, 0], [0.25, 0.25, 0], color=RED, stroke_width=6),
                       Line([-0.25, 0.25, 0], [0.25, -0.25, 0], color=RED, stroke_width=6)).move_to(ghost)
        self.at("not the fresh upper")
        self.play(FadeIn(ghost), Create(cross), run_time=0.7)
        warning = fit_text("below 5 for a long time", 4.0, 28, RED, max_lines=1).move_to([-3.65, 2.35, 0])
        self.at("die when water stays")
        self.play(FadeIn(warning, shift=DOWN * 0.12), Indicate(cross, color=RED), run_time=0.9)
        rf = reef([2.7, -0.35, 0], 1.2)
        self.at("Wild oyster reefs grow")
        self.play(LaggedStart(*[FadeIn(o, scale=0.4) for o in rf], lag_ratio=0.15), run_time=1.5)
        mixed = T("mixed water", 30, TEAL).move_to([2.75, 1.15, 0])
        self.at("water is mixed")
        self.play(FadeIn(mixed), run_time=0.6)
        self.finish()


class S08Data(SpokenScene):
    def construct(self):
        p, line, pts, codes, values = station_plot()
        self.at("measured station means")
        self.play(Create(p), run_time=1.0)
        self.play(Create(line), LaggedStart(*[FadeIn(d, scale=0.4) for d in pts], lag_ratio=0.08), run_time=1.5)
        self.at("Low values sit upstream")
        self.play(LaggedStart(*[FadeIn(c) for c in codes[:4]], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(v) for v in values[:4]], lag_ratio=0.12), run_time=1.3)
        self.at("higher values sit")
        self.play(LaggedStart(*[FadeIn(c) for c in codes[4:]], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(v) for v in values[4:]], lag_ratio=0.12), run_time=1.3)
        highlight = VGroup(*[Line(codes[i].get_corner(DL) + DOWN * 0.05,
                                      codes[i].get_corner(DR) + DOWN * 0.05,
                                      color=GOLD, stroke_width=4) for i in (0, 5)])
        self.at("difference between two stations")
        self.play(Create(highlight), run_time=0.8)
        slot = VGroup(M("20.67", 34, GOLD), M("−", 34, TEXT), M("0.09", 34, GOLD), M("= ?", 34, TEXT)).arrange(RIGHT, buff=0.22)
        slot.move_to([0, 3.35, 0])
        self.at("must be calculated")
        self.play(FadeIn(slot, shift=DOWN * 0.15), run_time=0.8)
        self.at("not guessed from spacing")
        self.play(Indicate(slot, color=GOLD), run_time=0.8)
        shade = Rectangle(width=p.x1 - p.x0, height=p.pt(0, 28)[1] - p.pt(0, 10)[1], stroke_width=0,
                          fill_color=ORANGE, fill_opacity=0.11).move_to([0, (p.pt(0, 28)[1] + p.pt(0, 10)[1]) / 2, 0])
        shade.set_z_index(-1)
        self.at("test the oyster range")
        self.play(FadeIn(shade), LaggedStart(*[Indicate(pts[i], color=ORANGE) for i in range(3, 8)], lag_ratio=0.1), run_time=1.4)
        self.finish()


class S09Limits(SpokenScene):
    def construct(self):
        p, line, pts, codes, values = station_plot(bottom=-0.35, top=1.05)
        if p.ylabel is not None:
            p.remove(p.ylabel)
        self.add(p, line, pts, codes)
        soft = RoundedRectangle(width=11.0, height=0.62, corner_radius=0.3, stroke_width=0,
                                fill_color=GREEN, fill_opacity=0.2).move_to([0, 3.25, 0])
        self.at("Range matches are not sharp")
        self.play(FadeIn(soft), run_time=0.8)
        grass = T("widgeon grass: every station", 28, GREEN).move_to(soft)
        self.at("Widgeon Grass can fit")
        self.play(FadeIn(grass), run_time=0.7)
        oyster_r = RoundedRectangle(width=6.35, height=0.5, corner_radius=0.25, stroke_width=0,
                                    fill_color=ORANGE, fill_opacity=0.28).move_to([2.28, 2.55, 0])
        oyster_l = T("oyster range", 28, ORANGE).move_to(oyster_r)
        eel = RoundedRectangle(width=4.65, height=0.5, corner_radius=0.25, stroke_width=0,
                               fill_color=GREEN, fill_opacity=0.3).move_to([3.1, 1.88, 0])
        eel_l = T("eelgrass stations", 28, GREEN).move_to(eel)
        self.at("oyster's range overlaps")
        self.play(FadeIn(oyster_r), FadeIn(oyster_l), FadeIn(eel), FadeIn(eel_l), run_time=1.2)
        measured = chip("✓  salinity fits", GOLD, size=28).move_to([-3.5, -2.25, 0])
        counted = chip("organism counted?  □", GREEN, size=28).move_to([3.15, -2.25, 0])
        self.at("crews measured water")
        self.play(FadeIn(measured), run_time=0.7)
        self.at("did not count organisms")
        self.play(FadeIn(counted), run_time=0.7)
        arrow = Arrow(measured.get_right(), counted.get_left(), color=TEXT, stroke_width=4)
        cross = Line(arrow.get_start(), arrow.get_end(), color=RED, stroke_width=7)
        self.at("Suitable salinity suggests")
        self.play(GrowArrow(arrow), run_time=0.6)
        self.at("does not prove")
        self.play(Create(cross), counted.animate.set_color(RED), run_time=0.8)
        self.finish()


class S10Change(SpokenScene):
    def construct(self):
        world = james_world(labels=False, station_ticks=True)
        self.add(world)
        boundary = DashedLine([-0.8, 1.2, 0], [-0.8, -1.35, 0], color=TEAL, stroke_width=6)
        tag = scope_tag("schematic seasonal shift", size=24)
        self.at("shifts with rain")
        self.play(Create(boundary), FadeIn(tag), run_time=0.7)
        clouds = VGroup(*[Circle(0.28, color=GREY, fill_color=GREY, fill_opacity=0.7).move_to([-4.8 + i * 0.4, 2.35, 0]) for i in range(4)])
        drops = VGroup(*[Line([-5.2 + 0.35 * (i % 5), 1.95 - 0.28 * (i // 5), 0],
                                  [-5.3 + 0.35 * (i % 5), 1.65 - 0.28 * (i // 5), 0], color=BLUE, stroke_width=4)
                           for i in range(15)])
        self.play(FadeIn(clouds), LaggedStart(*[Create(d) for d in drops], lag_ratio=0.04), run_time=1.4)
        self.at("boundary slides")
        self.play(boundary.animate.shift(RIGHT * 2.0), run_time=1.5)
        gauges = VGroup()
        levels = []
        for x, v in zip(XS, SALINITY):
            bg = Rectangle(width=0.18, height=0.8, color=GREY, stroke_width=2).move_to([x, 1.45, 0])
            fill = Rectangle(width=0.14, height=max(0.06, 0.72 * v / 28), stroke_width=0,
                             fill_color=GOLD, fill_opacity=0.9).align_to(bg, DOWN).shift(UP * 0.04)
            gauges.add(VGroup(bg, fill)); levels.append(fill)
        self.at("station's value can change")
        self.play(FadeIn(gauges), *[f.animate.stretch(0.62, 1, about_edge=DOWN) for f in levels], run_time=1.4)
        self.at("river and bay remain")
        self.play(Indicate(world[3], color=TEXT, scale_factor=1.01), run_time=0.8)
        self.at("summer sample is a snapshot")
        self.play(FadeOut(drops), FadeOut(clouds), boundary.animate.shift(LEFT * 1.35),
                  *[f.animate.stretch(1.35, 1, about_edge=DOWN) for f in levels], run_time=1.5)
        snap = T("one sample ≠ permanent border", 32, TEXT).move_to([0, 2.85, 0])
        self.at("not a permanent border")
        self.play(FadeIn(snap), run_time=0.7)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        world = james_world(labels=False)
        oy = oyster([1.25, -0.45, 0], 1.25)
        self.add(world, oy)
        salt = chip("salt", GOLD, size=28).move_to([-4.65, 2.25, 0])
        self.at("Salinity is powerful evidence")
        salt_arrow = Arrow(salt.get_bottom(), oy.get_corner(UL), color=GOLD)
        self.play(FadeIn(salt), GrowArrow(salt_arrow), run_time=0.9)
        self.at("only one condition")
        self.play(salt.animate.shift(LEFT * 0.25), run_time=0.55)
        abiotic = [("light", -2.7, 2.5), ("temperature", 0, 2.7), ("water movement", 3.2, 2.55)]
        living = [("predators", -2.7, -2.45), ("food", 3.2, -2.45)]
        made = VGroup()
        self.at("Light")
        for name, x, y in abiotic:
            c = chip(name, GOLD, size=26).move_to([x, y, 0])
            a = Arrow(c.get_center() + DOWN * 0.25, oy.get_center(), color=GOLD, stroke_width=4, tip_length=0.16)
            made.add(c, a)
            self.play(FadeIn(c), GrowArrow(a), run_time=0.48)
        self.at("predators")
        for name, x, y in living:
            c = chip(name, GREEN, size=28).move_to([x, y, 0])
            a = Arrow(c.get_center() + UP * 0.25, oy.get_center(), color=GREEN, stroke_width=4, tip_length=0.16)
            made.add(c, a)
            self.play(FadeIn(c), GrowArrow(a), run_time=0.55)
        self.at("Living interactions and non living")
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.04) for m in made[::2]], lag_ratio=0.08), run_time=0.8)
        self.at("strongest explanation connects")
        self.play(LaggedStart(*[Indicate(m, scale_factor=1.04) for m in made[::2]], lag_ratio=0.08), run_time=1.4)
        rule = fit_text("Living interactions + nonliving conditions", 10.5, 36, TEXT, max_lines=1).move_to([0, 3.25, 0])
        self.at("both sides of the ecosystem")
        self.play(FadeOut(made), FadeOut(salt), FadeOut(salt_arrow), FadeIn(rule), run_time=0.9)
        self.at("Use the station data")
        self.play(FadeOut(rule), run_time=1.0)
        limit = T("test the rule — with limits", 34, GOLD).move_to([0, 2.45, 0])
        self.at("test that rule with limits")
        self.play(FadeIn(limit), run_time=0.7)
        self.play(FadeOut(limit), FadeOut(oy), run_time=0.5)
        self.finish()


class S12End(EndCard):
    LINE = "Living interactions and nonliving conditions help decide what can live where."
