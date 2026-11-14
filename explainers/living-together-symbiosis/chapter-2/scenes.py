"""Does the Fungus Help? — chapter 2.

COLOR MAP (carried from chapter 1's requested series palette)
  BLUE   fungus threads
  GOLD   marigolds / plant tissue
  YELLOW plant-made food
  TEAL   minerals
  RED    harm / warning
  GREY   unaffected / structure
  WATER  water
  TEXT   help badges and general evidence
"""
from bp_parts import *  # noqa: F401,F403

PLANT = GOLD
FUNGUS = BLUE
FOOD = YELLOW
MINERAL = TEAL
WATER = "#9ADCF0"

MASS_PAIRS = [(5.29, 4.44), (4.12, 3.28), (3.06, 2.89), (2.62, 2.01)]
WATER_LEVELS = ["100%", "75%", "50%", "25%"]


def greenhouse_light():
    """A broad moving greenhouse reflection: the film's continuous carried background."""
    band = Polygon([-1.8, -4.2, 0], [1.0, -4.2, 0], [2.2, 4.2, 0], [-.6, 4.2, 0],
                   stroke_width=0, fill_color=WATER, fill_opacity=.11).move_to([-5.8, 0, 0])
    band.set_z_index(-20)

    def sweep(mob, dt):
        mob.shift(RIGHT * 1.15 * dt)
        if mob.get_left()[0] > 7.2:
            mob.shift(LEFT * 17.0)
    band.add_updater(sweep)
    panes = VGroup(*[Line([x, -3.7, 0], [x, 3.7, 0], color=GREY, stroke_width=1.5, stroke_opacity=.22)
                     for x in (-4.5, 0, 4.5)])
    panes.set_z_index(-21)
    return VGroup(panes, band)


class FilmScene(SpokenScene):
    def setup(self):
        super().setup()
        self.add(greenhouse_light())


def plus_badge(at, scale=1.0):
    ring = Circle(radius=0.34 * scale, color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=0.9).move_to(at)
    plus = T("+", 34 * scale, TEXT, weight=BOLD).move_to(ring)
    plus.layout_ok = True
    return VGroup(ring, plus)


def marigold(at=ORIGIN, scale=1.0, height=2.5):
    """The carried marigold drawing; every scene rebuilds this exact picture."""
    base = np.array(at, dtype=float)
    stem = Line(base, base + UP * height, color=PLANT, stroke_width=8 * scale)
    leaf1 = Ellipse(width=0.72 * scale, height=0.32 * scale, color=PLANT,
                    fill_color=PLANT, fill_opacity=0.55).rotate(0.38).move_to(base + UP * height * 0.46 + LEFT * 0.28 * scale)
    leaf2 = Ellipse(width=0.72 * scale, height=0.32 * scale, color=PLANT,
                    fill_color=PLANT, fill_opacity=0.55).rotate(-0.38).move_to(base + UP * height * 0.66 + RIGHT * 0.28 * scale)
    petals = VGroup(*[
        Circle(radius=0.25 * scale, color=PLANT, fill_color=PLANT, fill_opacity=0.9)
        .move_to(base + UP * height + 0.25 * scale * np.array([np.cos(a), np.sin(a), 0]))
        for a in np.linspace(0, TAU, 8, endpoint=False)
    ])
    centre = Dot(base + UP * height, radius=0.14 * scale, color=FOOD)
    return VGroup(stem, leaf1, leaf2, petals, centre)


def pot(at=ORIGIN, scale=1.0, fungus=True, plant_height=2.35):
    """Transparent pot, roots, and optional fungus at a fixed shared scale."""
    c = np.array(at, dtype=float)
    body = Polygon(c + [-1.0, 0.45, 0], c + [1.0, 0.45, 0], c + [0.78, -1.35, 0], c + [-0.78, -1.35, 0],
                   color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.10).scale(scale, about_point=c)
    soil = Line(c + LEFT * 0.88 * scale, c + RIGHT * 0.88 * scale, color=GREY, stroke_width=7).shift(UP * 0.10 * scale)
    roots = VGroup(
        CubicBezier(c + [0, 0.25, 0], c + [-0.05, -0.25, 0], c + [-0.28, -0.65, 0], c + [-0.42, -1.08, 0]),
        CubicBezier(c + [0, 0.15, 0], c + [0.12, -0.25, 0], c + [0.36, -0.60, 0], c + [0.48, -1.05, 0]),
    ).set_stroke(PLANT, width=6 * scale)
    threads = VGroup()
    if fungus:
        for dx in (-0.75, -0.35, 0.35, 0.75):
            threads.add(CubicBezier(c + [dx * scale, -1.12 * scale, 0], c + [dx * .7 * scale, -.75 * scale, 0],
                                    c + [dx * .35 * scale, -.55 * scale, 0], c + [dx * .18 * scale, -.25 * scale, 0]))
        threads.set_stroke(FUNGUS, width=4 * scale)
    plant = marigold(c + UP * 0.32 * scale, scale=scale, height=plant_height * scale)
    return VGroup(body, soil, roots, threads, plant)


def greenhouse_bench():
    bench = RoundedRectangle(corner_radius=0.16, width=12.1, height=0.34, color=GREY,
                             fill_color=GREY, fill_opacity=0.25).move_to([0, -2.15, 0])
    p = pot([-2.4, -0.8, 0], 1.05, True, 2.45)
    meter = RoundedRectangle(corner_radius=0.18, width=2.5, height=3.2, color=GREY, stroke_width=3).move_to([3.5, 0.15, 0])
    baseline = Line([2.75, -0.95, 0], [4.25, -0.95, 0], color=GREY, stroke_width=4)
    q = T("?", 72, TEXT, weight=BOLD).move_to([3.5, 0.25, 0])
    tag = scope_tag("schematic")
    return VGroup(bench, p, meter, baseline, q, tag)


def outcome_board():
    title = T("partner outcomes", 40, TEXT, font=TITLE_FONT).move_to([0, 3.05, 0])
    cols = VGroup()
    for x, name, a, b in [(-4.2, "mutualism", "+", "+"), (0, "commensalism", "+", "0"), (4.2, "parasitism", "+", "−")]:
        frame = RoundedRectangle(corner_radius=.2, width=3.7, height=4.2, color=GREY, stroke_width=2.5).move_to([x, 0.15, 0])
        head = T(name, 28, TEXT).move_to([x, 1.75, 0])
        aa = T(a, 54, TEXT if a == "+" else GREY, weight=BOLD).move_to([x, .55, 0])
        bb = T(b, 54, RED if b == "−" else (TEXT if b == "+" else GREY), weight=BOLD).move_to([x, -.75, 0])
        cols.add(VGroup(frame, head, aa, bb))
    return VGroup(title, cols)


def trade_world():
    p = pot([0, -0.25, 0], 1.65, True, 2.0)
    ml = T("minerals", 28, MINERAL).move_to([-4.85, -.2, 0])
    fl = T("plant-made food", 28, FOOD).move_to([4.55, -.2, 0])
    mins = VGroup(*[Dot([-4.8 + .36*i, -1.25 + .12*(i%2), 0], radius=.11, color=MINERAL) for i in range(5)])
    food = VGroup(*[Dot([3.55 + .34*i, .55 - .12*(i%2), 0], radius=.11, color=FOOD) for i in range(5)])
    return VGroup(p, ml, fl, mins, food)


def paired_pots(level="100%", heights=(2.35, 2.15)):
    left = pot([-2.8, -.45, 0], .9, True, heights[0])
    right = pot([2.8, -.45, 0], .9, False, heights[1])
    lf = T("with fungus", 28, FUNGUS).move_to([-2.8, 2.75, 0])
    rf = T("without fungus", 28, GREY).move_to([2.8, 2.75, 0])
    gauge = chip(level, WATER, size=30).move_to([0, 2.75, 0])
    return VGroup(left, right, lf, rf, gauge)


def four_conditions():
    heights = [2.35, 1.9, 1.45, 1.05]
    lanes = VGroup()
    for i, (lab, h) in enumerate(zip(WATER_LEVELS, heights)):
        x = -4.8 + i * 3.2
        pair = VGroup(pot([x-.55, -.55, 0], .43, True, h), pot([x+.55, -.55, 0], .43, False, h*.9))
        drop = T("●", 25, WATER).move_to([x, 2.65, 0])
        level = T(lab, 25, WATER).next_to(drop, DOWN, buff=.06)
        lanes.add(VGroup(pair, drop, level))
    return lanes


def balance(at, height=.9):
    c = np.array(at, dtype=float)
    base = Line(c + LEFT*.8, c + RIGHT*.8, color=GREY, stroke_width=5)
    post = Line(c, c + UP*1.0, color=GREY, stroke_width=5)
    tray = RoundedRectangle(corner_radius=.08, width=1.35, height=.18, color=GREY).move_to(c + UP*1.05)
    bar = Rectangle(width=.75, height=height, color=PLANT, fill_color=PLANT, fill_opacity=.75).next_to(tray, UP, buff=.08)
    return VGroup(base, post, tray, bar)


def predict_backdrop():
    bars = VGroup(*[Rectangle(width=1.2, height=2.2, color=c, stroke_width=4).move_to([x, .75, 0])
                    for x, c in [(-.75, FUNGUS), (.75, GREY)]])
    labels = VGroup()
    q = question_card("Which pattern supports a plant benefit?", ["with fungus higher", "equal", "with fungus lower"],
                      y=3.05, chips_at=[0, -2.25, 0], size=34, chip_size=28)
    return VGroup(bars, labels, q)


def mass_plot(pair=(5.29, 4.44), level="100%"):
    P = Plot(box=(-3.8, 3.0, -2.0, 2.55), xr=(0, 2), yr=(0, 6), xticks=[],
             yticks=[(0, "0"), (2, "2"), (4, "4"), (6, "6")], ylabel="mean shoot dry mass (g)")
    bw = .9
    bars = VGroup()
    for x, v, col in [(.65, pair[0], FUNGUS), (1.35, pair[1], GREY)]:
        bottom = P.pt(x, 0); top = P.pt(x, v)
        bars.add(Rectangle(width=bw, height=top[1]-bottom[1], color=col, fill_color=col, fill_opacity=.72)
                 .move_to([(top[0]+bottom[0])/2, (top[1]+bottom[1])/2, 0]))
    labs = VGroup(T("with", 26, FUNGUS).move_to(P.pt(.65,0)+DOWN*.4),
                  T("without", 26, GREY).move_to(P.pt(1.35,0)+DOWN*.4))
    vals = M(f"{pair[0]:.2f} / {pair[1]:.2f}" + (" g" if level == "25%" else ""), 32, TEXT).move_to([4.65, .35, 0])
    lev = chip(level, WATER, size=30).move_to([4.65, 1.55, 0])
    return VGroup(P, bars, labs, vals, lev)


def evidence_cards():
    outer = RoundedRectangle(corner_radius=.22, width=12.4, height=5.7, color=GOLD, stroke_width=3).move_to([0, -.1, 0])
    scope = T("these marigolds, this greenhouse", 28, GOLD).move_to([0, 2.35, 0])
    rows = VGroup(
        chip("plant growth: supported here", PLANT, size=30),
        chip("survival: not measured", GREY, size=30),
        chip("fungus gain: not measured here", GREY, size=30),
    ).arrange(DOWN, buff=.55).move_to([0, -.15, 0])
    return VGroup(outer, scope, rows)


class S01Link(FilmScene):
    def construct(self):
        board = outcome_board()
        self.at("first film sorted")
        self.play(FadeIn(board), run_time=.8)
        pulse(board[1], base=2.5, amp=.6, speed=1.5)
        self.at("how can we tell")
        world = greenhouse_bench()
        self.play(FadeOut(board), FadeIn(world), run_time=1.0)
        bob(world[1][4], amp=.035, speed=1.4)
        self.at("root fungus really helps")
        self.play(Indicate(world[1][3], color=FUNGUS), Indicate(world[4], color=TEXT), run_time=.9)
        self.at("fair comparison")
        fair = chip("fair comparison", TEXT, size=34).move_to([0, 3.15, 0])
        self.play(FadeIn(fair, shift=DOWN*.15), run_time=.7)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Living together: symbiosis"
    TITLE = "Does the Fungus Help?"


class S03Trade(FilmScene):
    def construct(self):
        w = trade_world(); self.add(w[0])
        self.at("proposed trade")
        self.play(FadeIn(w[1]), FadeIn(w[2]), run_time=.7)
        self.at("minerals from soil")
        self.play(FadeIn(w[3]), w[3].animate.move_to([-1.0, -.65, 0]), run_time=2.0)
        self.at("plant passes food")
        self.play(FadeIn(w[4]), w[4].animate.move_to([1.0, -.65, 0]), run_time=2.0)
        self.at("suggests mutualism")
        badges = VGroup(plus_badge([-2.8, 1.75, 0]), plus_badge([2.8, -1.55, 0]))
        self.play(FadeIn(badges, scale=.75), run_time=.8)
        self.at("not a measurement")
        qs = VGroup(T("?", 54, TEXT).move_to(badges[0]), T("?", 54, TEXT).move_to(badges[1]))
        self.play(ReplacementTransform(badges, qs), run_time=.8)
        bob(qs, amp=.04, speed=1.6)
        self.finish()


class S04Comparison(FilmScene):
    def construct(self):
        one = pot([0, -.45, 0], 1.05, True, 2.35); self.add(one)
        self.at("with living root fungus")
        pair = paired_pots()
        self.play(ReplacementTransform(one, pair), run_time=1.0)
        self.at("same water level")
        levels = VGroup()
        for i, lab in enumerate(WATER_LEVELS):
            new = chip(lab, WATER, size=30).move_to(pair[4])
            if i == 0:
                self.play(Indicate(pair[4], color=WATER), run_time=.6)
            else:
                self.play(Transform(pair[4], new), run_time=.45)
            icon = Dot([-2.1+i*1.4, -3.05, 0], radius=.13, color=WATER)
            levels.add(icon); self.play(FadeIn(icon), run_time=.18)
        self.at("planned difference")
        lock = T("same light • pot • soil • water", 28, TEXT).move_to([0, -2.55, 0])
        self.play(FadeIn(lock), Indicate(pair[0][3], color=FUNGUS), run_time=.8)
        self.at("compared fairly")
        self.play(Circumscribe(VGroup(pair[0], pair[1]), color=TEXT), run_time=1.0)
        bob(pair[0][4], amp=.025, speed=1.2); bob(pair[1][4], amp=.025, speed=1.25)
        self.finish()


class S04Conditions(FilmScene):
    def construct(self):
        lanes = four_conditions()
        self.at("tested drought")
        for lane in lanes:
            self.play(FadeIn(lane), run_time=.45)
        self.at("reduced growth")
        self.play(*[Indicate(l[0], color=PLANT, scale_factor=1.04) for l in lanes], run_time=1.2)
        self.at("fungus benefit appears")
        bracket = Brace(lanes, DOWN, color=TEXT)
        label = T("same comparison under each water level", 28, TEXT).next_to(bracket, DOWN, buff=.12)
        self.play(GrowFromCenter(bracket), FadeIn(label), run_time=.9)
        for i, lane in enumerate(lanes): bob(lane[0], amp=.02, speed=1.1+i*.08)
        self.finish()


class S05Measure(FilmScene):
    def construct(self):
        shoots = VGroup(marigold([-3.7, -.9, 0], .75, 2.6), marigold([-1.8, -.9, 0], .62, 2.6))
        cabinet = RoundedRectangle(corner_radius=.18, width=2.7, height=4.0, color=GREY, fill_color=GREY, fill_opacity=.08).move_to([.4, .1, 0])
        dry = T("dry", 34, TEXT).move_to([.4, 1.55, 0]); dry.layout_ok = True
        self.add(shoots)
        self.at("cut and dried")
        self.play(shoots.animate.move_to(cabinet.get_center()+DOWN*.3), FadeIn(cabinet), FadeIn(dry), run_time=1.2)
        drops = VGroup(*[Dot([-.45+.42*i, -.25+.18*(i%2), 0], radius=.11, color=WATER) for i in range(5)])
        self.play(FadeIn(drops), drops.animate.shift(RIGHT*2.0+DOWN*.7), FadeOut(drops), run_time=1.6)
        self.at("each shoot was weighed")
        bals = VGroup(balance([3.0, -1.65, 0], .85), balance([5.1, -1.65, 0], .65))
        self.play(FadeOut(cabinet), FadeOut(dry), shoots.animate.scale(.55).move_to([4.05, 1.65, 0]), FadeIn(bals), run_time=1.0)
        self.at("water in the shoots")
        lab = caption("mean shoot dry mass", size=34, color=PLANT)
        self.play(FadeIn(lab), Indicate(bals, color=PLANT), run_time=.9)
        pulse(bals[0][3], base=3, amp=.8, speed=1.3); pulse(bals[1][3], base=3, amp=.8, speed=1.45)
        self.finish()


class S06Predict(FilmScene):
    def construct(self):
        bal = VGroup(balance([-1.3, -1.1, 0]), balance([1.3, -1.1, 0])); self.add(bal)
        self.at("what pattern")
        back = predict_backdrop()
        self.play(ReplacementTransform(bal, back[0]), FadeIn(back[1]), run_time=.8)
        self.at("choose before")
        self.play(FadeIn(back[2].question), run_time=.6)
        self.at("higher dry mass")
        self.play(FadeIn(back[2].chips, lag_ratio=.18), run_time=1.1)
        pulse(back[0], base=4, amp=.7, speed=1.2)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Which pattern supports a plant benefit?"
    OPTIONS = ["with fungus higher", "equal", "with fungus lower"]
    CHIPS_AT = [0, -2.25, 0]
    CARD = {"y": 3.05, "size": 34, "chip_size": 28}
    SECONDS = 4.5

    def setup(self):
        super().setup()
        self.add(greenhouse_light())

    def backdrop(self):
        b = predict_backdrop()
        return VGroup(b[0], b[1])


class S08Data(FilmScene):
    def construct(self):
        chart = mass_plot(MASS_PAIRS[0], WATER_LEVELS[0])
        self.at("tested water levels")
        self.play(FadeIn(chart[0]), FadeIn(chart[2]), run_time=.7)
        self.at("higher with fungus")
        self.play(GrowFromEdge(chart[1], DOWN), FadeIn(chart[3]), FadeIn(chart[4]), run_time=.9)
        for pair, level in zip(MASS_PAIRS[1:], WATER_LEVELS[1:]):
            nxt = mass_plot(pair, level)
            self.play(Transform(chart[1], nxt[1]), Transform(chart[3], nxt[3]), Transform(chart[4], nxt[4]), run_time=.7)
        self.at("study values")
        self.play(Indicate(chart[3], color=TEXT), run_time=.7)
        self.at("smallest gap")
        gaps = [a-b for a,b in MASS_PAIRS]
        dots = VGroup(*[Dot([-3.6+i*2.4, -.1+(g-.17)*1.6, 0], radius=.16, color=FUNGUS) for i,g in enumerate(gaps)])
        axis = Line([-4.2,-1.0,0],[4.2,-1.0,0],color=GREY,stroke_width=4)
        bracket = Brace(dots[2], RIGHT, color=TEXT)
        note = T("could be due to chance", 28, TEXT).next_to(bracket, RIGHT, buff=.18)
        cap = caption("computed from table values", size=28, color=GREY)
        self.play(FadeOut(chart), FadeIn(axis), FadeIn(dots), run_time=.8)
        self.play(GrowFromCenter(bracket), FadeIn(note), FadeIn(cap), run_time=.7)
        bob(dots, amp=.035, speed=1.3)
        self.finish()


class S08Means(FilmScene):
    def construct(self):
        bar = Rectangle(width=2.1, height=4.3, color=FUNGUS, fill_color=FUNGUS, fill_opacity=.7).move_to([0,-.1,0])
        self.add(bar)
        self.at("mean an average")
        plants = VGroup(*[marigold([-4.2+i*1.65,-1.7,0], .42, h) for i,h in enumerate([2.7,3.3,2.9,3.6,3.0,3.4])])
        self.play(ReplacementTransform(bar, plants), run_time=1.2)
        self.at("every plant")
        self.play(*[Indicate(p, color=PLANT, scale_factor=1.04) for p in plants], run_time=1.0)
        self.at("group averages")
        mean = Line([-5.0,.55,0],[5.0,.55,0],color=TEXT,stroke_width=5)
        label = T("group mean, not every plant", 32, TEXT).move_to([0, 2.65, 0])
        self.play(Create(mean), FadeIn(label), run_time=.8)
        newbar = Rectangle(width=2.1, height=4.3, color=FUNGUS, fill_color=FUNGUS, fill_opacity=.7).move_to([0,-.1,0])
        self.play(FadeOut(mean), FadeOut(label), ReplacementTransform(plants,newbar), run_time=1.0)
        pulse(newbar, base=4, amp=.8, speed=1.2)
        self.finish()


class S08Statistics(FilmScene):
    def construct(self):
        base = mass_plot(MASS_PAIRS[2], WATER_LEVELS[2]); self.add(base)
        self.at("chance variation")
        band = Rectangle(width=1.35, height=.75, color=GREY, fill_color=GREY, fill_opacity=.23).move_to(base[1][1].get_top())
        lab = T("chance variation — schematic", 28, GREY).move_to([3.9,2.7,0])
        self.play(FadeIn(band), FadeIn(lab), run_time=.8)
        self.at("smallest gap")
        unclear = chip("not clear", GREY, size=28).move_to([4.4,-.55,0])
        self.play(FadeIn(unclear), Indicate(base[1], color=GREY), run_time=.8)
        self.at("other gaps")
        clear = chip("clear in this study", FUNGUS, size=28).move_to([4.4,-1.55,0])
        tall = mass_plot(MASS_PAIRS[0], WATER_LEVELS[0])
        self.play(Transform(base[1],tall[1]), FadeIn(clear), run_time=1.0)
        pulse(band, base=3, amp=.7, speed=1.15)
        self.finish()


class S09Inference(FilmScene):
    def construct(self):
        bars = mass_plot(MASS_PAIRS[0], WATER_LEVELS[0]); self.add(bars)
        self.at("supports a benefit")
        cards = evidence_cards()
        self.play(FadeOut(bars), FadeIn(cards[0]), FadeIn(cards[1]), FadeIn(cards[2][0]), run_time=.9)
        self.at("how many plants lived")
        self.play(FadeIn(cards[2][1], shift=LEFT*.15), run_time=.7)
        self.at("fungus's gain")
        self.play(FadeIn(cards[2][2], shift=LEFT*.15), run_time=.7)
        pulse(cards[0], base=3, amp=.6, speed=1.1)
        self.finish()


class S10Classify(FilmScene):
    def construct(self):
        conditions = RoundedRectangle(corner_radius=.22, width=12.5, height=5.5, color=GOLD, stroke_width=3).move_to([0,.15,0])
        scope = T("these marigolds, this greenhouse", 28, GOLD).move_to([0,2.45,0])
        plant = marigold([-3.7,-1.45,0],.75,3.0)
        fungus = VGroup(*[CubicBezier([-5.1,-1.5,0],[-4.8,-.8,0],[-4.5,-.3,0],[-4.0,.05,0]),
                          CubicBezier([-4.8,-1.65,0],[-4.5,-1.0,0],[-4.2,-.55,0],[-3.85,-.1,0])]).set_stroke(FUNGUS,width=6)
        food = VGroup(*[Dot([-2.75+.32*i,.35-.12*(i%2),0],radius=.11,color=FOOD) for i in range(5)])
        arrow = Arrow([-2.5,.3,0],[-4.35,-.45,0],buff=.12,color=FOOD,stroke_width=5)
        evidence = chip("plant growth: supported here", PLANT, size=30).move_to([2.8,.2,0])
        self.add(conditions,scope,plant,fungus,food,arrow,evidence)
        self.at("receive plant made food")
        foodplus = plus_badge([-4.7,1.45,0]); self.play(FadeIn(foodplus), Indicate(food,color=FOOD),run_time=.8)
        self.at("plant growth result")
        plantplus = plus_badge([2.8,1.35,0]); self.play(FadeIn(plantplus),Indicate(evidence,color=PLANT),run_time=.8)
        self.at("mutualism fits")
        result = chip("mutualism fits this case", TEXT, size=36).move_to([0,-3.18,0])
        self.play(foodplus.animate.move_to([-.55,-1.7,0]),plantplus.animate.move_to([.55,-1.7,0]),FadeIn(result),run_time=1.0)
        self.at("tested and measured")
        self.play(Circumscribe(conditions,color=GOLD),run_time=1.0)
        bob(VGroup(foodplus,plantplus),amp=.035,speed=1.3)
        self.finish()


class S11Refine(FilmScene):
    def construct(self):
        tag = chip("mutualism", TEXT, size=38).move_to([0,1.9,0]); self.add(tag)
        self.at("never permission")
        case = RoundedRectangle(corner_radius=.22,width=5.5,height=3.6,color=GREY,stroke_width=3).move_to([2.1,0,0])
        self.play(tag.animate.shift(LEFT*3.9),FadeIn(case), run_time=.8)
        self.at("another plant fungus")
        new = VGroup(pot([1.25,-.55,0],.8,True,1.65),chip("different water",WATER,size=28).move_to([3.2,1.25,0]))
        self.play(FadeIn(new),run_time=.8)
        self.at("different result")
        q=T("?",64,TEXT).move_to([3.8,.2,0]);self.play(tag.animate.move_to([-1.5,2.5,0]),FadeIn(q),run_time=.8)
        self.at("compare partners fairly")
        steps=VGroup(chip("compare fairly",TEXT,28),chip("measure",TEXT,28),chip("state limits",TEXT,28)).arrange(RIGHT,buff=.45).move_to([0,-2.65,0])
        arrows=VGroup(Arrow(steps[0].get_right(),steps[1].get_left(),buff=.12,color=GREY),Arrow(steps[1].get_right(),steps[2].get_left(),buff=.12,color=GREY))
        self.play(FadeIn(steps[0]),run_time=.35);self.play(GrowArrow(arrows[0]),FadeIn(steps[1]),run_time=.45);self.play(GrowArrow(arrows[1]),FadeIn(steps[2]),run_time=.45)
        bob(new[0][4],amp=.03,speed=1.2)
        self.finish()


class S12Close(FilmScene):
    def construct(self):
        bench=VGroup(Line([-6.0,.75,0],[-3.0,.75,0],color=GREY,stroke_width=7),pot([-4.5,1.15,0],.42,True,1.8))
        trade=VGroup(pot([-4.5,-1.65,0],.42,True,1.2),
                     VGroup(*[Dot([-5.8+.24*i,-1.65,0],radius=.08,color=MINERAL) for i in range(5)]),
                     Arrow([-5.2,-1.65,0],[-4.75,-1.65,0],buff=.05,color=MINERAL,stroke_width=4))
        bars=VGroup(Rectangle(width=.7,height=2.4,color=FUNGUS,fill_color=FUNGUS,fill_opacity=.7).move_to([-.5,1.0,0]),
                    Rectangle(width=.7,height=1.9,color=GREY,fill_color=GREY,fill_opacity=.7).move_to([.5,.75,0]),
                    Line([-1.3,-.2,0],[1.3,-.2,0],color=GREY,stroke_width=4))
        cards=VGroup(*[RoundedRectangle(corner_radius=.12,width=2.6,height=.75,color=c,stroke_width=3).move_to([4.4,y,0])
                       for c,y in [(PLANT,1.45),(GREY,.35),(GREY,-.75)]])
        self.add(bench,trade,bars,cards)
        self.at("ask what the evidence")
        board=outcome_board();self.play(FadeOut(VGroup(bench,trade,bars,cards)),FadeIn(board),run_time=1.0)
        pointer=Triangle(color=TEXT,fill_color=TEXT,fill_opacity=1).scale(.15).rotate(-PI/2).move_to([-4.2,-2.15,0])
        self.play(FadeIn(pointer),run_time=.3)
        self.at("each partner")
        self.play(pointer.animate.move_to([0,-2.15,0]),run_time=.7);self.play(pointer.animate.move_to([4.2,-2.15,0]),run_time=.7)
        self.at("testable scientific claim")
        self.play(pointer.animate.move_to([-4.2,2.2,0]),Circumscribe(board[1][0],color=TEXT),run_time=.9)
        bob(pointer,amp=.05,speed=1.4)
        self.finish()


class S13End(EndCard):
    LINE = "Sort symbiosis by what each partner gains or loses."
