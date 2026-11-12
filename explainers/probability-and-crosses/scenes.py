"""A Ratio Predicts a Spread (Probability, crosses and the chi-square test).

COLOUR MAP (identical to chapter 2)
  GOLD   = round yellow seeds       GREEN = round green seeds
  ORANGE = wrinkled yellow seeds    TEAL  = wrinkled green seeds
  WHITE  = expected counts, branch probabilities, and Mendel's observed marks
  GREY   = anything made by chance in a simulation
  BLUE   = chromosomes

The expected counts and every simulated cross are computed from n=556 and p=(9,3,3,1)/16.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F28C38"
CLS = [GOLD, GREEN, ORANGE, TEAL]
PALEGREY = "#9AA3B2"
REDGREY = "#B5605E"

COLS = [-4.5, -1.5, 1.5, 4.5]
BASE = -2.45
SC = 0.0135
BARW = 1.7
MENDEL = np.array([315, 108, 101, 32])
PROBS = np.array([9, 3, 3, 1], dtype=float) / 16
EXPECT = 556 * PROBS
RUNS = np.random.default_rng(21).multinomial(556, PROBS, size=40)


def seed(i, r=0.28, opacity=1.0):
    """Phenotype icon: circles are round; wavy outlines are wrinkled."""
    if i < 2:
        m = Circle(radius=r)
    else:
        pts = [
            [r * (1 + 0.18 * math.sin(7 * t)) * math.cos(t),
             r * (1 + 0.18 * math.sin(7 * t)) * math.sin(t), 0]
            for t in np.linspace(0, TAU, 64, endpoint=False)
        ]
        m = VMobject().set_points_smoothly(pts + [pts[0]])
    return m.set_fill(CLS[i], 0.92 * opacity).set_stroke(CLS[i], 3, opacity=opacity)


def class_labels(y=-3.36, size=26, stacked=True):
    names = ["round\nyellow", "round\ngreen", "wrinkled\nyellow", "wrinkled\ngreen"]
    if not stacked:
        names = [n.replace("\n", " ") for n in names]
    out = VGroup()
    for i, (x, name) in enumerate(zip(COLS, names)):
        icon = seed(i, 0.22)
        label = T(name, size, CLS[i], line_spacing=0.85)
        g = VGroup(icon, label).arrange(RIGHT, buff=0.16).move_to([x, y, 0])
        out.add(g)
    return out


def mkbar(i, value, opacity=0.62, color=None):
    h = max(float(value) * SC, 0.02)
    c = color or CLS[i]
    r = Rectangle(width=BARW, height=h, stroke_color=c, stroke_width=4,
                  fill_color=c, fill_opacity=opacity)
    return r.move_to([COLS[i], BASE + h / 2, 0])


def bars(values, opacity=0.62, color=None):
    return VGroup(*[mkbar(i, v, opacity, color) for i, v in enumerate(values)])


def set_bars(group, values):
    for i, (r, v) in enumerate(zip(group, values)):
        h = max(float(v) * SC, 0.02)
        r.stretch_to_fit_height(h).move_to([COLS[i], BASE + h / 2, 0])


def ghosts(width=0.98):
    return VGroup(*[
        DashedLine([x - width, BASE + e * SC, 0], [x + width, BASE + e * SC, 0],
                   color=TEXT, stroke_width=4)
        for x, e in zip(COLS, EXPECT)
    ])


def expected_labels():
    return VGroup(*[
        M(s, 28, TEXT).move_to([x, BASE + e * SC + 0.34, 0])
        for x, e, s in zip(COLS, EXPECT, ["312.75", "104.25", "104.25", "34.75"])
    ])


def count_labels(values, color=TEXT, y=-2.7):
    return VGroup(*[M(str(int(v)), 30, color).move_to([x, y, 0]) for x, v in zip(COLS, values)])


def run_ticks(lo=0, hi=12, opacity=0.42):
    out = VGroup()
    for row in RUNS[lo:hi]:
        for i, v in enumerate(row):
            y = BASE + v * SC
            out.add(Line([COLS[i] - 0.72, y, 0], [COLS[i] + 0.72, y, 0],
                         color=PALEGREY, stroke_width=3).set_opacity(opacity))
    return out


def mendel_ticks():
    return VGroup(*[
        Line([x - 0.82, BASE + v * SC, 0], [x + 0.82, BASE + v * SC, 0],
             color=TEXT, stroke_width=8)
        for x, v in zip(COLS, MENDEL)
    ])


def tree_base():
    """The shape fork, placed identically in scenes 3--6."""
    root = np.array([-5.5, 0.4, 0])
    joint = np.array([-3.9, 0.4, 0])
    top = np.array([-1.6, 2.05, 0])
    bot = np.array([-1.6, -1.25, 0])
    lines = VGroup(Line(root, joint, color=TEXT, stroke_width=5),
                   Line(joint, top, color=TEXT, stroke_width=5),
                   Line(joint, bot, color=TEXT, stroke_width=5))
    labs = VGroup(T("round  3/4", 32, TEXT).move_to([-2.45, 2.42, 0]),
                  T("wrinkled  1/4", 32, TEXT).move_to([-2.25, -1.62, 0]))
    return lines, labs


def full_tree(dim=False):
    """Two unlinked 3/4 : 1/4 forks and their four computed tips."""
    first, shape_labs = tree_base()
    starts = [np.array([-1.6, 2.05, 0]), np.array([-1.6, -1.25, 0])]
    ends = [np.array([2.35, 2.9, 0]), np.array([2.35, 1.18, 0]),
            np.array([2.35, -0.38, 0]), np.array([2.35, -2.12, 0])]
    second = VGroup()
    for j, s in enumerate(starts):
        elbow = s + RIGHT * 1.25
        second.add(Line(s, elbow, color=TEXT, stroke_width=5),
                   Line(elbow, ends[2*j], color=TEXT, stroke_width=5),
                   Line(elbow, ends[2*j+1], color=TEXT, stroke_width=5))
    tips = VGroup()
    names = ["round yellow", "round green", "wrinkled yellow", "wrinkled green"]
    fracs = ["9/16", "3/16", "3/16", "1/16"]
    for i, (p, name, frac) in enumerate(zip(ends, names, fracs)):
        icon = seed(i, 0.24)
        lab = VGroup(T(name, 28, CLS[i]), M(frac, 30, CLS[i])).arrange(DOWN, buff=0.08)
        tips.add(VGroup(icon, lab).arrange(RIGHT, buff=0.18).move_to(p + RIGHT * 1.75))
    g = VGroup(first, shape_labs, second, tips)
    if dim:
        g.set_opacity(0.22)
    return g, second, tips


def timer_ring(center=(6.15, -1.5, 0)):
    tr = ValueTracker(0)
    bg = Circle(radius=0.38, color=PALEGREY, stroke_width=4).set_opacity(0.45).move_to(center)
    ring = always_redraw(lambda: Arc(radius=0.38, start_angle=PI / 2,
                                     angle=-TAU * max(tr.get_value(), 0.001),
                                     color=TEXT, stroke_width=7).move_to(center))
    return tr, bg, ring


def stage_backdrop():
    """The shared dark teaching stage used behind every narrated diagram."""
    return RoundedRectangle(corner_radius=0.25, width=12.8, height=4.0,
                            stroke_width=0, fill_color="#29303F", fill_opacity=1).set_z_index(-20)


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()


class S00Title(TitleCard):
    LESSON = "Probability, Crosses and the Chi-Square Test"
    TITLE = "A Ratio Predicts a Spread"

    def construct(self):
        silhouettes = VGroup(*[seed(i, 0.72, 0.18).move_to([-4.7 + 3.15*i, (-1)**i * 1.45, 0])
                               for i in range(4)])
        silhouettes.t = 0.0
        origins = [m.get_center().copy() for m in silhouettes]

        def drift(m, dt):
            m.t += dt
            for i, s in enumerate(m):
                s.move_to(origins[i] + UP * 0.16 * math.sin(m.t * 0.8 + i))
        silhouettes.add_updater(drift)
        brand = T("BIOCHEMISTRYPEDIA", 20, TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = T(self.TITLE, 52, TEXT, font=TITLE_FONT)
        fit(title, 11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        card = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.3)
        self.add(silhouettes)
        self.play(FadeIn(brand), FadeIn(lesson), run_time=0.45)
        self.play(Write(title), GrowFromCenter(rule), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(card), FadeOut(silhouettes), run_time=0.45)
        self.finish()


class S01Hook(FilmScene):
    def construct(self):
        tr = ValueTracker(0)
        bb = bars(np.ones(4), 0.62)
        bb.add_updater(lambda m: set_bars(m, MENDEL * tr.get_value()))
        labs = class_labels()
        nums = count_labels(MENDEL)
        counter = M("0 seeds", 38, TEXT).move_to([5.9, 3.3, 0], aligned_edge=RIGHT)
        counter.add_updater(lambda m: m.become(M(f"{int(556*tr.get_value()):d} seeds", 38, TEXT)
                                               .move_to([5.9, 3.3, 0], aligned_edge=RIGHT)))
        falling = VGroup(*[seed(i % 4, 0.12).move_to([COLS[i % 4], 3.6 + 0.3*(i//4), 0])
                           for i in range(24)])
        self.add(bb, falling, counter)
        self.play(tr.animate.set_value(1),
                  LaggedStart(*[f.animate.move_to([COLS[i % 4], BASE + 0.25 + 0.13*(i//4), 0])
                                for i, f in enumerate(falling)], lag_ratio=0.025),
                  run_time=2.3, rate_func=smooth)
        bb.clear_updaters(); counter.clear_updaters()
        self.remove(falling)
        self.add(labs)
        self.at("He crossed peas")
        cross = VGroup(seed(0, 0.45), T("×", 48, TEXT), seed(3, 0.45)).arrange(RIGHT, buff=0.35).move_to([0, 3.1, 0])
        self.play(FadeIn(cross, shift=DOWN * 0.15), run_time=0.8)
        self.at("Then he counted")
        self.play(FadeOut(cross), FadeIn(nums, shift=UP * 0.15), run_time=0.8)
        self.play(LaggedStart(*[Indicate(n, color=CLS[i], scale_factor=1.18) for i, n in enumerate(nums)],
                              lag_ratio=0.2), run_time=1.4)
        self.finish()


class S02Piles(FilmScene):
    def construct(self):
        bb = bars(MENDEL)
        labs = class_labels()
        nums = count_labels(MENDEL)
        self.add(bb, labs, nums)
        ratio = VGroup(*[M(x, 54, TEXT) for x in ["9", ":", "3", ":", "3", ":", "1"]])
        ratio.arrange(RIGHT, buff=0.28).move_to([0, 3.15, 0])
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in ratio], lag_ratio=0.16), run_time=3.2)
        self.at("Not one")
        gl, el = ghosts(), expected_labels()
        self.play(LaggedStart(*[Create(g) for g in gl], lag_ratio=0.18),
                  LaggedStart(*[FadeIn(e, shift=DOWN * 0.12) for e in el], lag_ratio=0.18), run_time=1.5)
        gaps = VGroup(*[Line([x, BASE + o*SC, 0], [x, BASE + e*SC, 0], color=CLS[i], stroke_width=9)
                        for i, (x, o, e) in enumerate(zip(COLS, MENDEL, EXPECT))])
        self.play(LaggedStart(*[ShowPassingFlash(g.copy().set_stroke(width=13), time_width=0.55)
                                for g in gaps], lag_ratio=0.2), run_time=1.4)
        self.at("Was the ratio wrong")
        q = T("?", 112, TEXT, weight=BOLD).move_to([0, 1.5, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.play(Indicate(q, color=TEXT, scale_factor=1.18), run_time=0.8)
        self.finish()


class S03Draw(FilmScene):
    def construct(self):
        single = seed(0, 1.05).move_to([0, 0.45, 0])
        self.play(FadeIn(single, scale=0.4), run_time=0.8)
        self.at("It began as")
        egg = Circle(radius=0.75, color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.08).move_to([-3.0, 0.5, 0])
        pollen = Circle(radius=0.58, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.12).move_to([3.0, 0.5, 0])
        el = T("egg", 30, TEXT).next_to(egg, DOWN, buff=0.25)
        pl = T("pollen", 30, GOLD).next_to(pollen, DOWN, buff=0.25)
        self.play(ReplacementTransform(single.copy(), egg), ReplacementTransform(single, pollen),
                  FadeIn(el), FadeIn(pl), run_time=1.1)
        self.at("Each carried")
        tags = VGroup(chip("R or r", BLUE, 30), chip("Y or y", BLUE, 30),
                      chip("R or r", BLUE, 30), chip("Y or y", BLUE, 30))
        tags[0].move_to([-3.95, 2.0, 0]); tags[1].move_to([-2.05, 2.0, 0])
        tags[2].move_to([2.05, 2.0, 0]); tags[3].move_to([3.95, 2.0, 0])
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in tags], lag_ratio=0.15), run_time=1.2)
        self.at("picked by chance")
        self.play(*[Rotate(t, angle=TAU, axis=UP) for t in tags], run_time=1.2)
        self.at("So every seed")
        copies = VGroup(*[seed(i % 4, 0.3).move_to([-4.2 + 1.2*i, -2.55, 0]) for i in range(8)])
        self.play(FadeOut(VGroup(egg, pollen, el, pl, tags)),
                  LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in copies], lag_ratio=0.1), run_time=1.5)
        self.at("For seed shape alone")
        self.play(FadeOut(copies), run_time=0.4)
        lines, tl = tree_base()
        self.play(Create(lines), run_time=1.2)
        self.at("round comes up")
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in tl], lag_ratio=0.35), run_time=1.0)
        self.finish()


class S04Tree(FilmScene):
    def construct(self):
        first, shape_labs = tree_base()
        self.add(first, shape_labs)
        whole, second, tips = full_tree()
        self.at("add seed color")
        self.play(LaggedStart(*[Create(x) for x in second], lag_ratio=0.12), run_time=1.4)
        self.at("round and yellow")
        gold_path = VGroup(first[0].copy(), first[1].copy(), second[0].copy(), second[1].copy()).set_color(GOLD).set_stroke(width=9)
        self.play(Create(gold_path), run_time=1.0)
        self.at("take both branches")
        self.play(FadeIn(tips[0], shift=LEFT * 0.15), run_time=0.8)
        equation = M("3/4 × 3/4 = 9/16", 38, GOLD).move_to([-1.1, 3.25, 0])
        self.at("multiply the chances")
        self.play(FadeIn(equation, shift=DOWN * 0.12), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(tips[i], shift=LEFT * 0.12) for i in range(1, 4)], lag_ratio=0.22), run_time=1.4)
        note = T("schematic: two unlinked genes", 28, GREY).move_to([0, -3.45, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


class S05Add(FilmScene):
    def construct(self):
        whole, second, tips = full_tree()
        self.add(whole)
        focus = SurroundingRectangle(tips[1], buff=0.3, color=GREEN, stroke_width=5,
                                     fill_color=GREEN, fill_opacity=0.10)
        self.play(whole[3][0].animate.set_opacity(0.22), whole[3][3].animate.set_opacity(0.22),
                  Create(focus), run_time=2.5)
        self.at("exactly one recessive trait")
        self.play(Indicate(tips[1], color=GREEN, scale_factor=1.12), run_time=1.6)
        self.at("or wrinkled and yellow")
        focus2 = SurroundingRectangle(tips[2], buff=0.3, color=ORANGE, stroke_width=5,
                                      fill_color=ORANGE, fill_opacity=0.10)
        self.play(FadeOut(focus), FadeIn(focus2), Indicate(tips[2], color=ORANGE, scale_factor=1.12), run_time=1.8)
        focus = focus2
        self.at("No seed can be both")
        sep = T("OR", 42, TEXT, weight=BOLD).move_to([0.2, 0.38, 0])
        self.play(FadeIn(sep, scale=0.7), focus.animate.set_opacity(0.35), run_time=1.3)
        self.at("add those paths")
        bracket = BraceBetweenPoints([6.2, 1.65, 0], [6.2, -0.85, 0], direction=RIGHT, color=TEXT)
        total = M("3/16 + 3/16 = 6/16", 38, TEXT).move_to([0.2, -3.25, 0])
        self.play(GrowFromCenter(bracket), FadeIn(total, shift=UP * 0.12), FadeOut(focus), run_time=1.5)
        self.play(Indicate(tips[1], color=GREEN, scale_factor=1.08), Indicate(tips[2], color=ORANGE, scale_factor=1.08), run_time=2.0)
        self.finish()


class S06Rule(FilmScene):
    def construct(self):
        whole, second, tips = full_tree()
        self.add(whole)
        and_rule = chip("AND: multiply along a path", GOLD, 32).move_to([-3.25, -3.25, 0])
        or_rule = chip("OR: add the paths", TEAL, 32).move_to([3.35, -3.25, 0])
        self.at("and means")
        self.play(FadeIn(and_rule, shift=UP * 0.15), run_time=0.8)
        self.at("or means")
        self.play(FadeIn(or_rule, shift=UP * 0.15), run_time=0.8)
        self.at("Those two rules")
        ratio = M("9 : 3 : 3 : 1", 72, TEXT).move_to([0, 0.25, 0])
        self.play(FadeOut(whole), FadeIn(ratio, scale=0.75), run_time=1.6)
        self.play(Indicate(ratio, color=TEXT, scale_factor=1.1), run_time=0.9)
        self.finish()


class S07Count(FilmScene):
    def construct(self):
        bb = bars(MENDEL)
        gl = ghosts()
        labs = class_labels()
        self.add(bb, gl, labs)
        self.at("Apply it")
        equation = M("556 × 9/16 = 312.75", 48, TEXT).move_to([0, 3.2, 0])
        self.play(FadeIn(equation, shift=DOWN * 0.12), run_time=0.9)
        self.at("part of a seed")
        full = seed(0, 0.78).move_to([0, 0.25, 0])
        quarter = Sector(radius=0.78, angle=PI/2, start_angle=0,
                         fill_color=BG, fill_opacity=1, stroke_color=GOLD, stroke_width=4).move_to(full)
        self.play(FadeIn(full, scale=0.6), FadeIn(quarter), run_time=0.8)
        full.t = 0.0
        full_origin = full.get_center().copy()
        quarter.t = 0.0
        quarter_origin = quarter.get_center().copy()
        def float_seed(m, dt):
            m.t += dt
            m.move_to(full_origin + 0.13 * np.array([math.sin(1.4*m.t), math.sin(2.1*m.t), 0]))
        def float_quarter(m, dt):
            m.t += dt
            m.move_to(quarter_origin + 0.13 * np.array([math.sin(1.4*m.t), math.sin(2.1*m.t), 0]))
        full.add_updater(float_seed)
        quarter.add_updater(float_quarter)
        self.at("three quarters")
        self.play(FadeOut(quarter, shift=RIGHT * 0.2), run_time=0.8)
        self.at("a ratio cannot")
        tag = chip("chances, not a count", TEXT, 34).move_to([3.5, 0.25, 0])
        self.play(FadeIn(tag, shift=LEFT * 0.15), run_time=0.8)
        self.play(Indicate(gl[0], color=TEXT, scale_factor=1.08), run_time=1.0)
        self.finish()


class S08Predict(FilmScene):
    def construct(self):
        outline = bars(MENDEL, opacity=0.0)
        gl = ghosts()
        labs = class_labels()
        self.add(outline, gl, labs)
        simlab = T("simulation: 9:3:3:1 true, 556 seeds", 30, TEXT).move_to([-6.3, 3.45, 0], aligned_edge=LEFT)
        self.play(FadeIn(simlab, shift=DOWN * 0.1), run_time=0.7)
        self.at("A computer replays")
        tr = ValueTracker(0)
        sim = bars(RUNS[0], opacity=0.55, color=PALEGREY)
        for r, c in zip(sim, CLS): r.set_stroke(c, width=4)
        sim.add_updater(lambda m: set_bars(m, RUNS[0] * tr.get_value()))
        self.add(sim)
        self.play(tr.animate.set_value(1), run_time=1.8, rate_func=smooth)
        sim.clear_updaters()
        self.play(*[sim[i].animate.set_fill(CLS[i], 0.55) for i in range(4)], run_time=0.8)
        self.at("How far from")
        card = RoundedRectangle(corner_radius=0.2, width=9.6, height=1.7, color=TEXT, stroke_width=3,
                                fill_color=BG, fill_opacity=0.96).move_to([0, 0.7, 0])
        qt = T("How far from the lines will the runs land?", 32, TEXT).move_to(card)
        self.play(FadeIn(VGroup(card, qt), scale=0.9), run_time=0.8)
        self.play(Indicate(gl, color=TEXT, scale_factor=1.05), run_time=0.9)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        sim = bars(RUNS[0], opacity=0.55)
        gl = ghosts(); labs = class_labels()
        simlab = T("simulation: 9:3:3:1 true, 556 seeds", 30, TEXT).move_to([-6.3, 3.45, 0], aligned_edge=LEFT)
        card = RoundedRectangle(corner_radius=0.2, width=9.6, height=1.7, color=TEXT, stroke_width=3,
                                fill_color=BG, fill_opacity=0.96).move_to([0, 0.7, 0])
        qt = T("How far from the lines will the runs land?", 32, TEXT).move_to(card)
        tr, bg, ring = timer_ring()
        self.camera.background_color = BG
        self.add(sim, gl, labs, simlab, card, qt, bg, ring)
        self.play(tr.animate.set_value(1), run_time=5.0, rate_func=linear)


class S10Reveal(FilmScene):
    def construct(self):
        gl = ghosts(); labs = class_labels()
        sim = bars(RUNS[0], opacity=0.48, color=PALEGREY)
        for r, c in zip(sim, CLS): r.set_stroke(c, width=4)
        simlab = T("simulation: 9:3:3:1 true, 556 seeds", 30, TEXT).move_to([-6.3, 3.45, 0], aligned_edge=LEFT)
        card = RoundedRectangle(corner_radius=0.2, width=9.6, height=1.7, color=TEXT, stroke_width=3,
                                fill_color=BG, fill_opacity=0.96).move_to([0, 0.7, 0])
        qt = T("How far from the lines will the runs land?", 32, TEXT).move_to(card)
        self.add(sim, gl, labs, simlab, card, qt)
        self.play(FadeOut(VGroup(card, qt)), run_time=0.5)
        self.at("fractions of a seed")
        frac = M("312.75   104.25   104.25   34.75", 32, TEXT).move_to([0, 2.85, 0])
        self.play(FadeIn(frac), run_time=0.6)
        self.at("Each run lands")
        cloud = VGroup()
        for k in range(12):
            nxt = bars(RUNS[k], opacity=0.45, color=PALEGREY)
            for r, c in zip(nxt, CLS): r.set_stroke(c, width=4)
            marks = VGroup(*[Line([COLS[i]-0.72, BASE+RUNS[k][i]*SC, 0],
                                      [COLS[i]+0.72, BASE+RUNS[k][i]*SC, 0],
                                      color=PALEGREY, stroke_width=3).set_opacity(0.45) for i in range(4)])
            self.play(Transform(sim, nxt), run_time=0.32, rate_func=smooth)
            self.add(marks); cloud.add(marks)
        sim.t = 0.0
        def keep_replaying(m, dt):
            m.t += dt
            u = m.t / 1.15
            k = 12 + int(u) % 8
            f = smooth(u - int(u))
            set_bars(m, (1-f) * RUNS[k] + f * RUNS[k+1])
        sim.add_updater(keep_replaying)
        self.at("Now drop in Mendel's")
        mt = mendel_ticks()
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.4) for t in mt], lag_ratio=0.18), run_time=1.2)
        self.at("They sit among")
        self.play(LaggedStart(*[Indicate(mt[i], color=CLS[i], scale_factor=1.12) for i in range(4)],
                              lag_ratio=0.2), run_time=1.5)
        self.at("well within")
        self.play(Indicate(cloud, color=PALEGREY, scale_factor=1.03), run_time=1.2)
        self.finish()


def mini_tree(center, good=True):
    c = np.array([center[0], center[1], 0.0])
    a = Line(c + LEFT*0.85, c, color=TEXT, stroke_width=4)
    b = Line(c, c + RIGHT*0.85 + UP*0.55, color=TEXT, stroke_width=4)
    d = Line(c, c + RIGHT*0.85 + DOWN*0.55, color=TEXT, stroke_width=4)
    g = VGroup(a, b, d)
    if not good:
        x = VGroup(Line(c+LEFT*0.35+UP*0.65, c+RIGHT*0.35+DOWN*0.65, color=REDGREY, stroke_width=8),
                   Line(c+LEFT*0.35+DOWN*0.65, c+RIGHT*0.35+UP*0.65, color=REDGREY, stroke_width=8))
        g.add(x)
    return g


def chromosome(x, gene_ys, label=None):
    rod = RoundedRectangle(corner_radius=0.18, width=0.42, height=3.0,
                           color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.25).move_to([x, 0.45, 0])
    tags = VGroup(*[VGroup(Dot([x, y, 0], radius=0.1, color=TEXT), T(t, 28, TEXT).move_to([x+0.42, y, 0]))
                    for y, t in gene_ys])
    return VGroup(rod, tags)


class S11Scope(FilmScene):
    def construct(self):
        divs = VGroup(Line([-1.9, -3.25, 0], [-1.9, 3.25, 0], color=GREY, stroke_width=2),
                      Line([2.2, -3.25, 0], [2.2, 3.25, 0], color=GREY, stroke_width=2))
        self.add(divs)
        self.at("different chromosomes")
        left = VGroup(chromosome(-5.2, [(1.0, "A")], "different"),
                      chromosome(-4.3, [(-0.1, "B")], "chromosomes"), mini_tree((-3.05, 0.5), True))
        ll = T("unlinked: multiply", 28, TEXT).move_to([-4.4, -2.45, 0])
        self.play(FadeIn(left, shift=UP*0.15), FadeIn(ll), run_time=1.8)
        self.play(Indicate(left, color=BLUE, scale_factor=1.04), run_time=1.8)
        self.at("far apart")
        mid = VGroup(chromosome(-0.65, [(1.35, "A"), (-0.45, "B")], "far apart"),
                     mini_tree((1.0, 0.5), True))
        cross = T("×", 38, TEXT).move_to([-0.65, 0.45, 0])
        ml = T("almost unlinked", 28, TEXT).move_to([0, -2.45, 0])
        self.play(FadeIn(mid, shift=UP*0.15), FadeIn(cross), FadeIn(ml), run_time=1.8)
        self.play(Indicate(mid, color=BLUE, scale_factor=1.04), run_time=1.8)
        self.at("close together")
        right = VGroup(chromosome(3.65, [(0.8, "A"), (0.35, "B")], "close together"),
                       mini_tree((5.35, 0.5), False))
        bracket = BraceBetweenPoints([3.25, 0.8, 0], [3.25, 0.35, 0], direction=LEFT, color=TEXT)
        rl = T("linked: do not multiply", 28, REDGREY).move_to([4.4, -2.45, 0])
        self.play(FadeIn(right, shift=UP*0.15), GrowFromCenter(bracket), FadeIn(rl), run_time=1.8)
        self.at("inherited together")
        together = T("inherited together", 28, TEXT).move_to([4.65, 2.65, 0])
        self.play(FadeIn(together), Indicate(bracket, color=TEXT, scale_factor=1.2), run_time=1.0)
        self.at("cannot simply multiply")
        self.play(Indicate(right[1], color=REDGREY, scale_factor=1.15), run_time=3.2)
        self.finish()


class S12Idea(FilmScene):
    def construct(self):
        gl = ghosts(); cloud = run_ticks(0, 12); labs = class_labels()
        for g, x in zip(labs, COLS):
            g.arrange(DOWN, buff=0.1).move_to([x, -3.0, 0])
        self.add(gl, cloud, labs)
        # The bars/world stay on the right while the guiding rules build on the left.
        world = VGroup(gl, cloud)
        self.play(world.animate.scale(0.66, about_point=ORIGIN).shift(RIGHT * 2.7 + DOWN * 0.5),
                  *[g.animate.move_to([2.7 + x * 0.66, -2.75, 0]) for g, x in zip(labs, COLS)], run_time=0.8)
        l1 = T("A cross predicts probabilities.", 32, TEXT).move_to([-6.0, 1.6, 0], aligned_edge=LEFT)
        l2 = T("Multiply along a path;\nadd the paths.", 32, TEXT, line_spacing=1.0).move_to([-6.0, 0.2, 0], aligned_edge=LEFT)
        l3 = T("A probability predicts\na spread of counts.", 32, TEXT, line_spacing=1.0).move_to([-6.0, -1.5, 0], aligned_edge=LEFT)
        self.at("A cross predicts")
        self.play(FadeIn(l1, shift=RIGHT*0.2), run_time=0.8)
        self.at("Multiply along")
        self.play(FadeIn(l2, shift=RIGHT*0.2), run_time=0.8)
        self.at("a probability predicts")
        self.play(FadeIn(l3, shift=RIGHT*0.2), run_time=0.8)
        self.play(LaggedStart(*[Indicate(c, color=CLS[i], scale_factor=1.06)
                                for i, c in enumerate([VGroup(*cloud[0::4]), VGroup(*cloud[1::4]),
                                                       VGroup(*cloud[2::4]), VGroup(*cloud[3::4])])],
                              lag_ratio=0.18), run_time=1.8)
        self.finish()


class S13Handoff(FilmScene):
    def construct(self):
        # Same bar landmarks, enlarged around the GOLD cloud without changing its x-position.
        x = COLS[0]
        center = BASE + EXPECT[0]*SC
        ticks = VGroup(*[Line([x-1.8, BASE+v*SC, 0], [x+1.8, BASE+v*SC, 0],
                              color=PALEGREY, stroke_width=5).set_opacity(0.55) for v in RUNS[:20, 0]])
        ghost = DashedLine([x-2.1, center, 0], [x+2.1, center, 0], color=TEXT, stroke_width=5)
        self.add(ticks, ghost)
        self.at("how far a count")
        outer = max(BASE + v*SC for v in RUNS[:20, 0])
        q = T("?", 100, TEXT, weight=BOLD).move_to([x, min(3.0, outer+0.8), 0])
        self.play(FadeIn(q, shift=DOWN*0.25), run_time=0.8)
        q.t = 0.0
        q_origin = q.get_center().copy()
        def bob_question(m, dt):
            m.t += dt
            m.move_to(q_origin + UP * 0.16 * math.sin(2.0*m.t))
        q.add_updater(bob_question)
        self.at("chance becomes")
        lab = T("how far is too far?", 42, TEXT).move_to([1.5, 0.8, 0])
        arrow = Arrow([-0.5, 1.35, 0], [x+0.45, q.get_y(), 0], buff=0.15, color=TEXT, stroke_width=6)
        self.play(FadeIn(lab, shift=LEFT*0.15), GrowArrow(arrow), run_time=1.0)
        self.at("chapter two")
        self.play(Indicate(VGroup(q, lab), color=TEXT, scale_factor=1.08), run_time=1.0)
        self.finish()


class S14End(EndCard):
    LINE = "A ratio predicts a spread of counts, not one count."
