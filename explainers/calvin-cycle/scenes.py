"""The Carbon Count Pays the Bill — Calvin-cycle teaching film.

COLOR MAP
  GREEN  = RuBP / returning carbon catcher
  BLUE   = carbon arriving from CO2
  GOLD   = G3P / net carbon product
  YELLOW = ATP
  PURPLE = NADPH
  TEAL   = stroma / light-reaction input
  TEXT   = counted carbon; GREY = conveyor and supporting structure

Every molecule is represented only as a labelled carrier containing carbon counters.
No molecular structures are drawn.
"""
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CO2_BLUE = BLUE
RUBP_GREEN = GREEN
SUGAR_GOLD = GOLD


# Shared geometry: every continuing scene uses this same loop and landmarks.
LOOP_W, LOOP_H = 8.4, 4.7
LOOP_C = np.array([-0.35, 0.15, 0.0])
OUTPUT_X = 5.25


def loop_point(a, center=LOOP_C, w=LOOP_W, h=LOOP_H):
    return center + np.array([0.5 * w * np.cos(a), 0.5 * h * np.sin(a), 0.0])


def conveyor(opacity=1.0, lanes=1):
    tracks = VGroup()
    for k in range(lanes):
        e = Ellipse(width=LOOP_W - 0.34 * k, height=LOOP_H - 0.34 * k,
                    color=GREY, stroke_width=11 if k == 0 else 4,
                    fill_color=TEAL, fill_opacity=0.16 * opacity if k == 0 else 0).move_to(LOOP_C)
        e.set_stroke(opacity=0.72 * opacity)
        tracks.add(e)
    arrow = Triangle(color=GREY, fill_color=GREY, fill_opacity=0.9 * opacity,
                     stroke_width=0).scale(0.16).rotate(-PI / 2).move_to(loop_point(PI / 2))
    return VGroup(tracks, arrow)


def carbon_carrier(n, label, color, blue=0, width=None):
    width = width or max(2.0, 0.48 * n + 0.55)
    body = RoundedRectangle(corner_radius=0.18, width=width, height=1.05,
                            stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.14)
    dots = VGroup(*[Circle(radius=0.145, stroke_width=0,
                           fill_color=CO2_BLUE if i < blue else TEXT, fill_opacity=1)
                    for i in range(n)]).arrange(RIGHT, buff=0.16)
    dots.move_to(body.get_center() + UP * 0.17)
    lab = T(label, 28, color, weight=BOLD).move_to(body.get_center() + DOWN * 0.31)
    g = VGroup(body, dots, lab)
    g.body, g.dots, g.label = body, dots, lab
    return g


def compact_carrier(n, label, color, scale, blue=0, width=None):
    """Shrink the carrier geometry while preserving a readable 28 pt label."""
    g = carbon_carrier(n, label, color, blue=blue, width=width).scale(scale)
    g.label.scale(1 / scale)
    g.label.next_to(g.body, DOWN, buff=0.04)
    return g


def energy_chip(name, color):
    return chip(name, color, size=28, pad=0.18, fill_opacity=0.22)


def meter(name, value, color, x):
    box = RoundedRectangle(corner_radius=0.15, width=2.15, height=0.88,
                           stroke_color=color, fill_color=color, fill_opacity=0.12)
    lab = T(name, 28, color, weight=BOLD).move_to(box.get_center() + LEFT * 0.42)
    num = M(str(value), 34, TEXT).move_to(box.get_center() + RIGHT * 0.68)
    g = VGroup(box, lab, num).move_to([x, -3.18, 0])
    g.num = num
    return g


def output_tray():
    tray = RoundedRectangle(corner_radius=0.18, width=2.55, height=1.55,
                            stroke_color=SUGAR_GOLD, stroke_width=3,
                            fill_color=SUGAR_GOLD, fill_opacity=0.08).move_to([5.15, 0.15, 0])
    lab = T("sugar output", 28, SUGAR_GOLD, weight=BOLD).next_to(tray, UP, buff=0.12)
    return VGroup(tray, lab)


def compact_output_tray(scale=0.85, center=np.array([5.0, 0.45, 0.0])):
    """Shrink tray geometry without shrinking its required 28 pt label."""
    g = output_tray().scale(scale)
    g[1].scale(1 / scale)
    g[1].next_to(g[0], UP, buff=0.12)
    g.shift(center - g[0].get_center())
    return g


def moving_highlight(scene, color=TEAL, phase=0.0, center=LOOP_C, w=LOOP_W, h=LOOP_H,
                     speed=0.42, inset=0.82, radius=0.12):
    """Keep the world alive without letting the traveling marker cross its labels."""
    path_w, path_h = w - inset, h - inset
    trail = VGroup(*[Dot(radius=radius, color=color).set_opacity(0.82 - 0.07 * i)
                     for i in range(8)])
    trail.phase = phase
    for i, dot in enumerate(trail):
        dot.move_to(loop_point(phase - 0.045 * i, center, path_w, path_h))
        dot.set_z_index(-1)

    def travel(m, dt):
        m.phase = (m.phase + speed * dt) % TAU
        for i, d in enumerate(m):
            d.move_to(loop_point(m.phase - 0.045 * i, center, path_w, path_h))
    trail.add_updater(travel)

    # A slow continuous wash changes a broad area, so motion remains measurable even
    # though the marker is deliberately small enough to stay clear of all text.
    wash = Ellipse(width=max(0.4, path_w - 0.22), height=max(0.4, path_h - 0.22),
                   stroke_width=0, fill_color=color, fill_opacity=0.018).move_to(center)
    wash.t = phase
    wash.set_z_index(-4)

    def breathe(m, dt):
        m.t += dt
        m.set_fill(opacity=0.018 + 0.012 * (0.5 + 0.5 * np.sin(1.1 * m.t)))
    wash.add_updater(breathe)
    scene.add(wash)
    scene.add(trail)
    return trail


def stroma_motes(scene, n=12):
    motes = VGroup()
    for i in range(n):
        d = Dot(radius=0.025 + 0.008 * (i % 3), color=TEAL).set_opacity(0.22)
        d.move_to([-5.8 + (i * 1.07) % 11.4, -2.6 + (i * 0.73) % 5.3, 0])
        d.v = 0.07 + 0.015 * (i % 4)

        def drift(m, dt):
            m.shift(RIGHT * m.v * dt)
            if m.get_x() > 6.3:
                m.shift(LEFT * 12.4)
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-5)
    scene.add(motes)
    return motes


def question_layout():
    q = T("Can both leave?", 48, TEXT, font=TITLE_FONT)
    q.move_to([0, 2.85, 0])
    carrier = carbon_carrier(5, "RuBP · 5C", RUBP_GREEN).move_to([0, -0.65, 0])
    carrier.dots.set_opacity(0.16)
    counters = VGroup(*[Dot(radius=0.19, color=TEXT) for _ in range(6)]).arrange(RIGHT, buff=0.33)
    counters.move_to([0, 0.75, 0])
    return q, carrier, counters


class S01Hook(SpokenScene):
    def construct(self):
        shell = Ellipse(width=12.6, height=7.0, color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.035)
        loop = conveyor()
        rubp = compact_carrier(5, "RuBP · 5C", RUBP_GREEN, 0.9).move_to(loop_point(PI))
        co2 = compact_carrier(1, "CO2", CO2_BLUE, 0.9, width=1.45).move_to([-6.0, 2.15, 0])
        tray = output_tray()
        self.add(shell, loop, rubp, tray)
        stroma_motes(self)
        moving_highlight(self, phase=0.4)
        self.at("pull carbon from air")
        self.play(co2.animate.move_to([-4.65, 1.6, 0]), run_time=1.1)
        self.at("build sugar")
        q1 = T("?", 54, SUGAR_GOLD).move_to([5.15, 0.2, 0])
        self.play(FadeIn(q1, scale=0.5), tray.animate.set_opacity(1), run_time=0.7)
        self.at("carbon catching machine")
        q2 = T("?", 54, RUBP_GREEN).move_to([-3.65, -1.7, 0])
        self.play(FadeIn(q2, scale=0.5), rubp.animate.move_to(loop_point(1.25 * PI)), run_time=1.0)
        self.at("Follow the carbon count")
        bracket = BraceBetweenPoints([-4.5, -2.55, 0], [3.8, -2.55, 0], color=TEXT)
        self.play(GrowFromCenter(bracket), co2.animate.move_to([-3.95, 1.1, 0]), run_time=0.9)
        self.at("energy bill")
        atp, nad = meter("ATP", 0, YELLOW, -1.25), meter("NADPH", 0, PURPLE, 1.35)
        self.play(FadeIn(atp, shift=UP * 0.25), FadeIn(nad, shift=UP * 0.25), run_time=0.8)
        self.finish()


class S02Title(TitleCard):
    LESSON = "The Calvin cycle"
    TITLE = "The Carbon Count Pays the Bill"

    def construct(self):
        loop = conveyor(opacity=0.38)
        co2 = compact_carrier(1, "CO2", CO2_BLUE, 0.78, width=1.45).move_to([-4.8, 1.45, 0])
        q = VGroup(T("?", 50, SUGAR_GOLD), T("?", 50, RUBP_GREEN)).arrange(RIGHT, buff=2.6)
        q.move_to([0, 0.25, 0])
        title = T(self.TITLE, 48, TEXT, font=TITLE_FONT)
        fit(title, 11.6, 1.1)
        rule = Line(LEFT * 1.55, RIGHT * 1.55, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.3)
        self.add(loop, co2, q)
        moving_highlight(self, phase=0.8, speed=0.35)
        self.play(ReplacementTransform(q, title), GrowFromCenter(rule), co2.animate.shift(RIGHT * 0.5), run_time=0.65)
        self.wait(0.65)
        self.play(FadeOut(title), FadeOut(rule), co2.animate.shift(RIGHT * 0.45), run_time=0.55)
        self.finish()


class S03World(SpokenScene):
    def construct(self):
        shell = Ellipse(width=12.6, height=7.0, color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.03)
        loop = conveyor()
        carrier = compact_carrier(5, "RuBP · 5C", RUBP_GREEN, 0.9).move_to(loop_point(PI))
        co2 = compact_carrier(1, "CO2", CO2_BLUE, 0.8, width=1.45).move_to([-4.55, 1.45, 0])
        thyl = VGroup(*[RoundedRectangle(corner_radius=0.13, width=0.55, height=1.1,
                                        color=TEAL, fill_color=TEAL, fill_opacity=0.18)
                        for _ in range(3)]).arrange(DOWN, buff=0.1).move_to([-5.95, 0, 0])
        self.add(loop, carrier, co2)
        moving_highlight(self, phase=0.2)
        self.at("runs in")
        self.play(Create(shell), FadeIn(thyl), run_time=0.8)
        self.at("chloroplastroma")
        stroma = T("stroma", 34, TEAL, weight=BOLD).move_to([0, 3.05, 0])
        self.play(shell.animate.set_fill(TEAL, 0.09), FadeIn(stroma), carrier.animate.move_to(loop_point(1.18 * PI)), run_time=0.8)
        self.at("using")
        atp = energy_chip("ATP", YELLOW).move_to([-3.65, 2.55, 0])
        self.play(FadeIn(atp), thyl.animate.set_fill(TEAL, 0.32), run_time=0.55)
        self.at("NADPH")
        nad = energy_chip("NADPH", PURPLE).move_to([-3.65, -2.45, 0])
        self.play(FadeIn(nad), run_time=0.55)
        self.at("light reactions")
        self.play(atp.animate.move_to([-2.75, 1.15, 0]), nad.animate.move_to([-2.7, -1.2, 0]),
                  carrier.animate.move_to(loop_point(1.45 * PI)), run_time=0.9)
        self.finish()


class S04Fixation(SpokenScene):
    def construct(self):
        arc = Arc(radius=3.25, start_angle=0.15, angle=PI * 1.35, color=GREY, stroke_width=10).move_to([0, 0.1, 0])
        rubp = carbon_carrier(5, "RuBP · 5C", RUBP_GREEN).move_to([-2.6, 0.45, 0])
        co2 = carbon_carrier(1, "CO2 · 1C", CO2_BLUE, width=1.7).move_to([3.9, 1.75, 0])
        clamp = VGroup(Arc(radius=1.32, start_angle=-1.12, angle=2.24, color=TEAL, stroke_width=12),
                       Arc(radius=1.32, start_angle=PI-1.12, angle=2.24, color=TEAL, stroke_width=12))
        clamp.move_to([-0.2, 0.45, 0])
        rubisco = T("Rubisco", 32, TEAL, weight=BOLD).next_to(clamp, UP, buff=0.18)
        atp, nad = meter("ATP", 0, YELLOW, -1.25), meter("NADPH", 0, PURPLE, 1.35)
        self.add(arc, rubp, co2, atp, nad)
        moving_highlight(self, phase=3.7, center=np.array([0, 0.1, 0]), w=6.5, h=6.5)
        self.at("joins one carbon dioxide")
        self.play(FadeIn(clamp), FadeIn(rubisco), co2.animate.move_to([-0.2, 1.12, 0]),
                  rubp.animate.move_to([-0.2, -0.18, 0]), run_time=1.25)
        self.at("5 carbon acceptor")
        self.play(clamp.animate.scale(0.82), run_time=0.6)
        six = carbon_carrier(6, "6C · brief", TEXT, blue=1, width=3.75).move_to([-0.2, 0.25, 0])
        self.at("brief 6 carbon")
        self.play(FadeOut(clamp), FadeOut(rubisco), ReplacementTransform(VGroup(rubp, co2), six), run_time=0.8)
        left = carbon_carrier(3, "3-PGA · 3C", BLUE, blue=1).move_to([-2.4, -0.15, 0])
        right = carbon_carrier(3, "3-PGA · 3C", BLUE).move_to([2.1, -0.15, 0])
        self.at("immediately splits")
        self.play(ReplacementTransform(six, VGroup(left, right)), run_time=1.1)
        self.at("3 phosphoglycerate")
        self.play(left.animate.shift(LEFT * 0.55 + DOWN * 0.55), right.animate.shift(RIGHT * 0.55 + DOWN * 0.55), run_time=0.8)
        stamp = chip("ATP 0 · NADPH 0", GREEN, size=32, fill_opacity=0.24).move_to([0, 2.65, 0])
        self.at("Fixation itself")
        self.play(FadeIn(stamp, scale=1.18), Indicate(atp), Indicate(nad), run_time=0.8)
        self.at("no ATP")
        self.play(left.animate.shift(RIGHT * 0.2), right.animate.shift(LEFT * 0.2), run_time=0.6)
        self.finish()


class S05Reduction(SpokenScene):
    def construct(self):
        lanes = VGroup(Line([-5.6, 1.25, 0], [4.3, 1.25, 0], color=GREY, stroke_width=7),
                       Line([-5.6, -1.1, 0], [4.3, -1.1, 0], color=GREY, stroke_width=7))
        pga1 = carbon_carrier(3, "3-PGA · 3C", BLUE, blue=1).move_to([-4.35, 1.25, 0])
        pga2 = carbon_carrier(3, "3-PGA · 3C", BLUE).move_to([-4.35, -1.1, 0])
        atpm, nadm = meter("ATP", 2, YELLOW, -1.25), meter("NADPH", 2, PURPLE, 1.35)
        self.add(lanes, pga1, pga2, atpm, nadm)
        self.at("become the triose sugar")
        self.play(pga1.animate.move_to([-2.25, 1.25, 0]), pga2.animate.move_to([-2.25, -1.1, 0]), run_time=1.0)
        a1, a2 = energy_chip("ATP", YELLOW), energy_chip("ATP", YELLOW)
        a1.move_to([0.1, 1.85, 0]); a2.move_to([0.1, -0.5, 0])
        self.at("Each conversion")
        self.play(FadeIn(a1, shift=DOWN * 0.2), FadeIn(a2, shift=DOWN * 0.2), run_time=0.6)
        self.at("1 ATP")
        self.remove(a1, a2)
        self.play(Transform(atpm.num, M("0", 34, TEXT).move_to(atpm.num)), run_time=0.75)
        n1, n2 = energy_chip("NADPH", PURPLE), energy_chip("NADPH", PURPLE)
        n1.move_to([1.5, 1.85, 0]); n2.move_to([1.5, -0.5, 0])
        self.at("1 NADPH")
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.55)
        g1 = carbon_carrier(3, "G3P · 3C", SUGAR_GOLD, blue=1).move_to([2.7, 1.25, 0])
        g2 = carbon_carrier(3, "G3P · 3C", SUGAR_GOLD).move_to([2.7, -1.1, 0])
        self.at("reduce it")
        self.remove(n1, n2)
        self.play(ReplacementTransform(pga1, g1), ReplacementTransform(pga2, g2),
                  Transform(nadm.num, M("0", 34, TEXT).move_to(nadm.num)), run_time=1.0)
        ledger = VGroup(T("1 CO2 so far", 30, CO2_BLUE),
                        T("2 ATP + 2 NADPH", 36, TEXT, weight=BOLD)).arrange(DOWN, buff=0.18)
        ledger.move_to([0, 2.85, 0])
        self.at("So far")
        self.play(FadeIn(ledger, shift=UP * 0.15), g1.animate.shift(RIGHT * 0.35), g2.animate.shift(RIGHT * 0.35), run_time=0.8)
        self.at("2 ATP")
        self.play(Indicate(ledger[1], color=YELLOW), run_time=0.65)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        loop = conveyor(opacity=0.58)
        tray = output_tray()
        g1 = compact_carrier(3, "G3P · 3C", SUGAR_GOLD, 0.86, blue=1).move_to([2.8, 0.9, 0])
        g2 = compact_carrier(3, "G3P · 3C", SUGAR_GOLD, 0.86).move_to([2.8, -0.85, 0])
        self.add(loop, tray, g1, g2)
        moving_highlight(self, phase=2.5, speed=0.32)
        self.at("can both new trioses leave")
        self.play(g1.animate.move_to([2.9, 0.8, 0]), g2.animate.move_to([2.9, -0.8, 0]), run_time=1.0)
        q, carrier, counters = question_layout()
        self.at("conveyor keeps turning")
        self.play(FadeIn(q), run_time=0.65)
        self.at("Count the carbons")
        self.remove(g1, g2, tray)
        self.play(FadeIn(carrier),
                  LaggedStart(*[FadeIn(d, scale=0.5) for d in counters], lag_ratio=0.08), run_time=0.9)
        self.at("rebuild each")
        self.play(LaggedStart(*[d.animate.shift(UP * 0.16) for d in counters], lag_ratio=0.08,
                              rate_func=there_and_back, run_time=0.9))
        self.finish()


class S07PredictPause(Scene):
    def construct(self):
        config.background_color = BG
        loop = conveyor(opacity=0.35)
        q, carrier, counters = question_layout()
        self.add(loop, q, carrier, counters)
        moving_highlight(self, phase=2.8, speed=0.34)
        self.play(LaggedStart(*[d.animate.shift(UP * 0.18) for d in counters], lag_ratio=0.16,
                              rate_func=there_and_back, run_time=2.0))
        self.play(LaggedStart(*[d.animate.shift(DOWN * 0.15) for d in counters], lag_ratio=0.16,
                              rate_func=there_and_back, run_time=2.0))
        self.wait(0.5)


class S08ThreeTurns(SpokenScene):
    def construct(self):
        loop = conveyor(lanes=3)
        self.add(loop)
        moving_highlight(self, phase=2.9, speed=0.42, inset=1.7, radius=0.27)
        self.at("Scale up to three turns")
        self.play(loop.animate.scale(1.02), run_time=0.7)
        rubps = VGroup(*[compact_carrier(5, "RuBP · 5C", RUBP_GREEN, 0.58)
                         .move_to([-3.75, 1.55 - i * 1.55, 0]) for i in range(3)])
        co2s = VGroup(*[compact_carrier(1, "CO2 · 1C", CO2_BLUE, 0.58, width=1.55)
                        .move_to([-5.85, 1.55 - i * 1.55, 0]) for i in range(3)])
        self.at("Three RuBP")
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in rubps], lag_ratio=0.12), run_time=0.7)
        self.at("three carbon dioxides")
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in co2s], lag_ratio=0.12), run_time=0.7)
        counter = VGroup(T("carbon count", 28, GREY), M("15", 52, TEXT)).arrange(DOWN, buff=0.08).move_to([4.95, 2.55, 0])
        self.play(FadeIn(counter), run_time=0.4)
        gs = VGroup()
        positions = [loop_point(a) for a in np.linspace(0, TAU, 6, endpoint=False)]
        for i, p in enumerate(positions):
            gs.add(compact_carrier(3, "G3P", SUGAR_GOLD, 0.56, blue=0).move_to(p))
        self.at("make six trioses")
        self.remove(rubps, co2s, *rubps, *co2s)
        self.play(LaggedStart(*[FadeIn(g, scale=0.6) for g in gs], lag_ratio=0.08),
                  Transform(counter[1], M("18", 52, TEXT).move_to(counter[1])), run_time=1.0)
        self.at("Only three carbons")
        self.play(*[gs[i].dots[i % 3].animate.set_color(CO2_BLUE) for i in range(3)], run_time=0.75)
        tray = output_tray()
        self.at("only one triose")
        self.play(FadeIn(tray), gs[0].animate.move_to([5.15, 0.1, 0]).scale(1.25),
                  *[gs[i].animate.rotate(0.12, about_point=LOOP_C) for i in range(1, 6)], run_time=1.0)
        self.finish()


class S09Regeneration(SpokenScene):
    def construct(self):
        loop = conveyor(lanes=3, opacity=0.52)
        tray = output_tray()
        net = compact_carrier(3, "G3P · net", SUGAR_GOLD, 0.72, blue=1).move_to([5.15, 0.1, 0])
        five = VGroup(*[compact_carrier(3, "G3P", SUGAR_GOLD, 0.52)
                        .move_to([-4.8 + i * 1.35, 1.7, 0]) for i in range(5)])
        self.add(loop, tray, net, five)
        moving_highlight(self, phase=3.0, speed=0.38)
        drum = RoundedRectangle(corner_radius=0.5, width=6.2, height=3.15, color=TEAL,
                                fill_color=TEAL, fill_opacity=0.1).move_to([-0.4, -0.2, 0])
        drum_lab = T("15-carbon shuffle", 32, TEAL, weight=BOLD).next_to(drum, UP, buff=0.12)
        self.at("hold 15 carbons")
        self.play(FadeIn(drum), FadeIn(drum_lab),
                  *[five[i].animate.move_to([-2.7 + 1.15 * i, 0.1, 0]) for i in range(5)], run_time=1.0)
        dots = VGroup(*[Dot(radius=0.14, color=TEXT).move_to([-2.6 + 0.37 * (i % 8),
                                                               -0.65 + 0.5 * (i // 8), 0]) for i in range(15)])
        self.at("exactly enough")
        self.remove(five, *five)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03), run_time=0.7)
        self.at("counters are reshuffled")
        self.play(LaggedStart(*[d.animate.shift(UP * (0.25 if i % 2 else -0.1) + RIGHT * (0.12 if i % 3 else -0.15))
                                for i, d in enumerate(dots)], lag_ratio=0.025, rate_func=there_and_back, run_time=1.2))
        rebuilt = VGroup(*[compact_carrier(5, "5C sugar", RUBP_GREEN, 0.66)
                            .move_to([-2.65 + i * 2.25, -0.15, 0]) for i in range(3)])
        self.at("not discarded")
        self.remove(dots, *dots, drum, drum_lab)
        self.play(LaggedStart(*[FadeIn(r, scale=0.7) for r in rebuilt], lag_ratio=0.1), run_time=0.9)
        atps = VGroup(*[energy_chip("ATP", YELLOW).next_to(r, UP, buff=0.15) for r in rebuilt])
        self.at("spends three more ATP")
        self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.2) for a in atps], lag_ratio=0.12), run_time=0.7)
        final = VGroup(*[compact_carrier(5, "RuBP · 5C", RUBP_GREEN, 0.54).move_to(r) for r in rebuilt])
        self.at("remake RuBP")
        self.play(FadeOut(atps), ReplacementTransform(rebuilt, final), run_time=0.8)
        self.at("close all three loops")
        targets = [loop_point(PI + x) for x in (-0.55, 0, 0.55)]
        self.play(*[final[i].animate.move_to(targets[i]) for i in range(3)], run_time=1.0)
        self.finish()


class S10GuidingRule(SpokenScene):
    def construct(self):
        loop = conveyor(lanes=3).scale(0.72).move_to([0, 1.55, 0])
        self.add(loop)
        moving_highlight(self, phase=2.4, center=np.array([0, 1.55, 0]), w=LOOP_W*0.72, h=LOOP_H*0.72, speed=0.44)
        red = VGroup(T("reduction", 28, BLUE), T("6 ATP + 6 NADPH", 34, TEXT, weight=BOLD)).arrange(DOWN, buff=0.12)
        reg = VGroup(T("regeneration", 28, RUBP_GREEN), T("3 ATP", 34, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.12)
        totals = VGroup(red, reg).arrange(RIGHT, buff=1.1).move_to([0, -0.85, 0])
        self.at("three turn bill")
        self.play(LaggedStart(FadeIn(red), FadeIn(reg), lag_ratio=0.2), run_time=0.55)
        bar = Line([-4.5, -1.7, 0], [4.5, -1.7, 0], color=TEXT, stroke_width=4)
        div = M("÷ 3", 40, TEXT).next_to(bar, DOWN, buff=0.18)
        self.at("by three")
        self.play(Create(bar), FadeIn(div), run_time=0.7)
        result = chip("per CO2: 3 ATP + 2 NADPH", GOLD, size=38, fill_opacity=0.18).move_to([0, -2.5, 0])
        self.at("ordinary C3 cycle")
        self.remove(totals, red, reg, div, bar)
        self.play(FadeIn(result, shift=UP * 0.12), run_time=0.8)
        self.at("3 ATP")
        self.play(Indicate(result, color=YELLOW, scale_factor=1.04), run_time=0.7)
        self.at("2 NADPH")
        self.play(Indicate(result, color=PURPLE, scale_factor=1.04), run_time=0.7)
        icons = VGroup(energy_chip("ATP", YELLOW), energy_chip("ATP", YELLOW), energy_chip("ATP", YELLOW),
                       energy_chip("NADPH", PURPLE), energy_chip("NADPH", PURPLE)).arrange(RIGHT, buff=0.15)
        icons.move_to([0, -0.8, 0])
        self.at("One extra ATP")
        self.play(FadeIn(icons), run_time=0.6)
        return_arrow = CurvedArrow([3.0, 0.85, 0], [3.55, 1.3, 0], angle=0.55, color=RUBP_GREEN)
        self.at("rebuild the acceptor")
        self.play(icons[2].animate.move_to([3.0, 0.15, 0]), Create(return_arrow), run_time=0.8)
        bracket = SurroundingRectangle(loop, color=TEXT, buff=0.18, corner_radius=0.25)
        self.at("Count the carbons")
        self.play(Create(bracket), loop.animate.set_color(TEXT), run_time=0.8)
        self.finish()


class S11Scale(SpokenScene):
    def construct(self):
        loop = conveyor().scale(0.75).move_to([-1.0, 0.7, 0])
        tray = compact_output_tray(0.85, np.array([5.05, 0.55, 0]))
        laps = chip("3 turns", TEAL, size=34).move_to([-4.9, 2.75, 0])
        atpm, nadm = meter("ATP", 9, YELLOW, -1.25), meter("NADPH", 6, PURPLE, 1.35)
        self.add(loop, tray, laps, atpm, nadm)
        moving_highlight(self, phase=2.6, center=np.array([-1.0, 0.7, 0]),
                         w=LOOP_W*.75, h=LOOP_H*.75, speed=0.55, radius=0.27)
        self.at("spend 9 ATP")
        self.play(Indicate(atpm, color=YELLOW), run_time=0.7)
        self.at("6 NADPH")
        self.play(Indicate(nadm, color=PURPLE), run_time=0.7)
        g1 = compact_carrier(3, "G3P", SUGAR_GOLD, 0.62, blue=1).move_to([5.15, 0.55, 0])
        self.at("one net G3P")
        self.play(FadeIn(g1, shift=RIGHT * 0.25), run_time=0.75)
        laps6 = chip("6 turns", TEAL, size=34).move_to(laps)
        self.at("Six turns")
        self.play(Transform(laps, laps6), loop.animate.set_stroke(width=11), run_time=0.75)
        self.at("18 ATP")
        self.play(Transform(atpm.num, M("18", 34, TEXT).move_to(atpm.num)), run_time=0.6)
        self.at("12 NADPH")
        self.play(Transform(nadm.num, M("12", 34, TEXT).move_to(nadm.num)), run_time=0.6)
        g2 = compact_carrier(3, "G3P", SUGAR_GOLD, 0.62).move_to([5.15, -0.45, 0])
        self.at("two net trioses")
        self.play(g1.animate.move_to([5.15, 0.65, 0]), FadeIn(g2, shift=RIGHT * 0.25), run_time=0.8)
        supply_box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.8, height=2.0, color=SUGAR_GOLD))
        supply_box.move_to([4.0, 0.1, 0])
        supply_lab = T("hexose phosphate supply", 28, SUGAR_GOLD, weight=BOLD).next_to(supply_box, UP, buff=0.12)
        self.at("supply one hexose phosphate")
        self.play(FadeOut(tray), Create(supply_box), FadeIn(supply_lab),
                  g1.animate.move_to([3.25, 0.2, 0]), g2.animate.move_to([4.75, 0.2, 0]), run_time=0.9)
        no = VGroup(Line(LEFT * 0.22 + UP * 0.22, RIGHT * 0.22 + DOWN * 0.22, color=RED, stroke_width=6),
                    Line(LEFT * 0.22 + DOWN * 0.22, RIGHT * 0.22 + UP * 0.22, color=RED, stroke_width=6))
        wrong = VGroup(no, T("free glucose directly", 30, RED)).arrange(RIGHT, buff=0.2).move_to([0, -2.25, 0])
        self.at("does not directly release")
        self.play(FadeIn(wrong), run_time=0.7)
        self.finish()


class S13Scope(SpokenScene):
    def construct(self):
        loop = conveyor().scale(0.76).move_to([0, 0.05, 0])
        badge = chip("simplest steady state", TEAL, size=32).move_to([0, 3.05, 0])
        self.add(loop)
        moving_highlight(self, phase=2.7, center=np.array([0, 0.05, 0]),
                         w=LOOP_W*.76, h=LOOP_H*.76, speed=0.4, radius=0.27)
        self.at("simplest steady state")
        self.play(FadeIn(badge, shift=DOWN * 0.15), run_time=0.65)
        dawn = VGroup(Rectangle(width=1.8, height=0.85, color=YELLOW),
                      Line([-0.65, -0.2, 0], [0.55, 0.2, 0], color=YELLOW, stroke_width=5))
        startup = VGroup(T("startup", 28, YELLOW, weight=BOLD), dawn).arrange(DOWN, buff=0.12).move_to([-5.0, 1.65, 0])
        photo = VGroup(T("photorespiration", 28, RED, weight=BOLD),
                       VGroup(Line(DOWN*.45, UP*.45, color=RED, stroke_width=5),
                              Line(ORIGIN, RIGHT*.65+UP*.35, color=RED, stroke_width=5),
                              Line(ORIGIN, RIGHT*.65+DOWN*.35, color=RED, stroke_width=5))).arrange(DOWN, buff=0.12).move_to([4.8, 1.55, 0])
        pump = VGroup(T("C4 / CAM", 28, CO2_BLUE, weight=BOLD),
                      Circle(radius=0.45, color=CO2_BLUE), Arrow(LEFT*.35, RIGHT*.35, color=CO2_BLUE, buff=0)).arrange(DOWN, buff=0.12).move_to([-5.0, -1.65, 0])
        self.at("Startup")
        self.play(FadeIn(startup), startup[1][1].animate.shift(UP * 0.14), run_time=0.24)
        self.at("photo respiration")
        self.play(FadeIn(photo), Rotate(photo[1], 0.18, rate_func=there_and_back), run_time=0.7)
        self.at("carbon concentrating pathways")
        self.play(FadeIn(pump), Rotate(pump[1], PI), run_time=0.7)
        deeper = VGroup(Arrow(UP * 0.35, DOWN * 0.35, color=TEXT), T("deeper below", 30, TEXT)).arrange(DOWN, buff=0.12).move_to([4.85, -2.35, 0])
        self.at("page below")
        self.play(FadeOut(startup, target_position=deeper[0]), FadeOut(photo, target_position=deeper[0]),
                  FadeOut(pump, target_position=deeper[0]), FadeIn(deeper), run_time=0.9)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        shell = Ellipse(width=12.6, height=7.0, color=TEAL, stroke_width=3,
                        fill_color=TEAL, fill_opacity=0.035)
        loop = conveyor(lanes=3)
        tray = output_tray()
        self.add(shell, loop, tray)
        stroma_motes(self)
        moving_highlight(self, phase=2.4, speed=0.5)
        six = VGroup(*[compact_carrier(3, "G3P", SUGAR_GOLD, 0.5, blue=1 if i == 0 else 0)
                       .move_to(loop_point(PI / 6 + i * TAU / 6)) for i in range(6)])
        self.add(six)
        net = six[0]
        drum = RoundedRectangle(corner_radius=0.35, width=3.6, height=2.1, color=TEAL,
                                fill_color=TEAL, fill_opacity=0.1).move_to([-0.2, -0.1, 0])
        self.at("builds carbon product")
        self.remove(*[six[i].body for i in range(1, 6)], *[six[i].label for i in range(1, 6)])
        self.play(net.animate.move_to([5.15, 0.1, 0]).scale(1.35), FadeIn(drum),
                  *[six[i].dots.animate.move_to([-1.45 + 0.65*i, -0.1, 0]) for i in range(1, 6)], run_time=1.0)
        rebuilt = VGroup(*[compact_carrier(5, "RuBP", RUBP_GREEN, 0.54)
                            .move_to(loop_point(PI + (i-1)*0.55)) for i in range(3)])
        self.at("rebuilding its carbon catcher")
        returning_dots = [six[i].dots for i in range(1, 6)]
        self.remove(*six[1:], *returning_dots,
                    *[d for group in returning_dots for d in group], drum)
        self.play(LaggedStart(*[FadeIn(r) for r in rebuilt], lag_ratio=0.1), run_time=0.9)
        one = chip("1 of 6 is net", SUGAR_GOLD, size=34).move_to([2.9, 3.05, 0])
        self.at("one trios in six")
        self.play(FadeIn(one), *[r.animate.rotate(0.14, about_point=LOOP_C) for r in rebuilt], run_time=0.75)
        atp, nad = meter("ATP", 3, YELLOW, -1.25), meter("NADPH", 2, PURPLE, 1.35)
        self.at("ATP demand")
        self.play(FadeIn(atp, shift=UP * 0.2), FadeIn(nad, shift=UP * 0.2), run_time=0.7)
        bracket = Brace(VGroup(atp, nad), UP, color=TEXT, buff=0.12)
        self.at("exceeds NADPH")
        self.play(GrowFromCenter(bracket), Indicate(atp, color=YELLOW), run_time=0.8)
        self.finish()


class S15End(EndCard):
    LINE = "Count the carbons, and the bill follows."

    def construct(self):
        loop = conveyor(opacity=0.22)
        line = T(self.LINE, 46, TEXT, font=TITLE_FONT)
        fit(line, 11.6, 1.2)
        rule = Line(LEFT * 1.55, RIGHT * 1.55, color=GOLD, stroke_width=4).next_to(line, DOWN, buff=0.32)
        self.add(loop)
        moving_highlight(self, color=GOLD, phase=PI, speed=0.42, inset=-0.18)
        self.play(FadeIn(line, shift=UP * 0.12), GrowFromCenter(rule), run_time=0.8)
        self.wait(2.8)
        self.finish()
