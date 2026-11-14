"""How microbes multiply: a bacterium copies itself; a virus is copied by a host cell.

COLOR MAP
  GREEN  bacterial cell and food
  BLUE   bacterial chromosome
  ORANGE phage DNA and phage heads/parts
  BROWN  waste
  GOLD   time, questions, and emphasis
  GREY   phage tails, outlines, and secondary marks
"""
import numpy as np
from bp_parts import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BROWN = "#9A6745"
LIQUID = "#E8D58A"


# Every continuing picture is rebuilt through these builders, at the same scale and position.
def bacterium(center=ORIGIN, width=4.6, height=2.35, loops=1, color=GREEN):
    """Large schematic rod with one or two simple chromosome loops."""
    body = RoundedRectangle(corner_radius=height * 0.48, width=width, height=height,
                            stroke_color=color, stroke_width=5, fill_color=color,
                            fill_opacity=0.22).move_to(center)
    dna = VGroup()
    xs = [0] if loops == 1 else [-width * 0.22, width * 0.22]
    for x in xs:
        loop = Ellipse(width=min(1.45, width * 0.31), height=height * 0.48,
                       color=BLUE, stroke_width=6).move_to(body.get_center() + RIGHT * x)
        dna.add(loop)
    g = VGroup(body, dna)
    g.body, g.dna = body, dna
    return g


def phage(center=ORIGIN, scale=1.0):
    """Cartoon phage: orange hexagon head, grey tail and legs."""
    head = RegularPolygon(6, radius=0.62 * scale, color=ORANGE, stroke_width=5,
                          fill_color=ORANGE, fill_opacity=0.35)
    tail = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.75 * scale,
                color=GREY, stroke_width=6)
    foot = tail.get_end()
    legs = VGroup(
        Line(foot, foot + DL * 0.42 * scale, color=GREY, stroke_width=4),
        Line(foot, foot + DR * 0.42 * scale, color=GREY, stroke_width=4),
        Line(foot + UP * 0.15 * scale, foot + LEFT * 0.48 * scale, color=GREY, stroke_width=4),
        Line(foot + UP * 0.15 * scale, foot + RIGHT * 0.48 * scale, color=GREY, stroke_width=4),
    )
    g = VGroup(head, tail, legs).move_to(center)
    g.head, g.tail, g.legs = head, tail, legs
    return g


def flask(cloudy=False):
    """The film's one warm-flask world, with liquid and drifting schematic contents."""
    neck = VGroup(Line([-1.15, 3.0, 0], [-1.15, 1.8, 0]),
                  Line([1.15, 3.0, 0], [1.15, 1.8, 0]),
                  Line([-1.35, 3.0, 0], [1.35, 3.0, 0]))
    vessel = VMobject(stroke_color=TEXT, stroke_width=5, fill_opacity=0)
    vessel.set_points_smoothly([[-1.15, 1.8, 0], [-2.0, 0.6, 0], [-3.45, -2.5, 0],
                                [0, -3.05, 0], [3.45, -2.5, 0], [2.0, 0.6, 0], [1.15, 1.8, 0]])
    liquid = Ellipse(width=6.1, height=4.0, stroke_width=0, fill_color=LIQUID,
                     fill_opacity=0.18 if not cloudy else 0.32).move_to([0, -0.75, 0])
    liquid.set_z_index(-2)
    g = VGroup(liquid, vessel, neck)
    g.liquid = liquid
    return g


def mini_cell(center, scale=1.0):
    return bacterium(center, 1.25 * scale, 0.66 * scale, 1)


def population(n, y=0.0):
    """A deterministic grid of n rods; counts on screen always match the narration."""
    cols = {2: 2, 4: 2, 8: 4, 16: 4}.get(n, min(8, max(2, int(np.ceil(np.sqrt(n * 1.7))))))
    rows = int(np.ceil(n / cols))
    scale = {2: 2.4, 4: 2.0, 8: 1.55, 16: 1.15}.get(n, 0.8)
    cells = VGroup(*[mini_cell(ORIGIN, scale) for _ in range(n)])
    cells.arrange_in_grid(rows, cols, buff=(0.32, 0.3)).move_to([0, y, 0])
    return cells


def count_readout(value, label="cells", at=(4.35, 2.55, 0), widest=2097152):
    return Readout([(label, lambda: value.get_value(), "{:,.0f}", TEXT)],
                   at=at, widest=[widest], title="counter", size=28)


def clock_face(center=(-4.9, 2.2, 0), radius=0.8, label="1 hour"):
    c = np.array(center, dtype=float)
    ring = Circle(radius=radius, color=GOLD, stroke_width=5).move_to(c)
    ticks = VGroup(*[Line(c + radius * 0.78 * np.array([np.cos(a), np.sin(a), 0]),
                              c + radius * 0.95 * np.array([np.cos(a), np.sin(a), 0]),
                              color=GOLD, stroke_width=3) for a in np.linspace(0, TAU, 12, endpoint=False)])
    hand = Line(c, c + UP * radius * 0.68, color=TEXT, stroke_width=5)
    lab = T(label, 28, GOLD).next_to(ring, DOWN, buff=0.18)
    g = VGroup(ring, ticks, hand, lab)
    g.hand, g.center_point = hand, c
    return g


def liquid_field():
    """A full, gently layered liquid field for the lone-phage continuation."""
    waves = VGroup()
    for y in np.linspace(-2.5, 2.15, 8):
        line = VMobject(color=LIQUID, stroke_width=4, stroke_opacity=0.6)
        xs = np.linspace(-6.1, 6.1, 40)
        line.set_points_smoothly([[x, y + 0.07 * np.sin(1.2 * x + y), 0] for x in xs])
        line.layout_ok = True  # Background water may pass behind foreground labels.
        waves.add(line)
    return waves


def food_field():
    pts = [(-5.6 + 1.1 * (i % 11), -2.45 + 1.15 * (i // 11), 0) for i in range(33)]
    dots = VGroup(*[Dot(p, radius=0.17, color=GREEN).set_opacity(0.7) for p in pts])
    for d in dots:
        d.layout_ok = True  # Background food particles deliberately drift behind labels.
    return dots


def predict_backdrop():
    n = ValueTracker(1)
    ro = count_readout(n, at=(4.25, 2.55, 0), widest=1000000)
    card = chip("20 min per doubling  •  7 hours", GOLD, size=28).move_to([-0.9, 1.7, 0])
    one = bacterium([-4.65, 0.0, 0], 3.25, 1.75, 1)
    return VGroup(one, card, ro)


def contrast_world():
    tp = TwoPanel("BACTERIUM", "VIRUS", colors=(GREEN, ORANGE), top=3.15, bottom=-2.45)
    left = bacterium([-3.25, 0.2, 0], width=4.4, height=2.0, loops=2)
    host = bacterium([3.25, 0.2, 0], width=4.7, height=2.55, loops=1)
    parts = VGroup(*[RegularPolygon(6, radius=0.22, color=ORANGE, stroke_width=3,
                                    fill_color=ORANGE, fill_opacity=0.4)
                     for _ in range(6)]).arrange_in_grid(2, 3, buff=0.25).move_to([3.25, 0.5, 0])
    return tp, left, host, parts


class S00Title(TitleCard):
    LESSON = "How microbes multiply"
    TITLE = "Copy Yourself, or Be Copied"


class S01Hook(SpokenScene):
    def construct(self):
        world = flask()
        cell = mini_cell([-1.35, -0.65, 0], 1.45)
        vir = phage([1.45, -0.25, 0], 1.0)
        self.play(FadeIn(world), run_time=0.55)
        self.play(FadeIn(cell, shift=DOWN * 0.35), FadeIn(vir, shift=DOWN * 0.35), run_time=0.75)
        bob(cell, amp=0.08, speed=1.25); bob(vir, amp=0.11, speed=1.05, seed=2)
        self.at("warm flask")
        warm = T("warm • food-rich", 30, LIQUID).move_to([0, -2.35, 0])
        self.play(FadeIn(warm), run_time=0.45)
        self.at("An hour later")
        clk = clock_face()
        self.play(FadeIn(clk), Rotate(clk.hand, TAU, about_point=clk.center_point), run_time=1.15)
        self.at("which has made")
        q = question_card("Which makes more of itself — and how?", y=-3.2, max_w=10.7)
        self.play(FadeIn(q.question, shift=UP * 0.15), run_time=0.7)
        self.at("And how")
        self.play(Indicate(VGroup(cell, vir), color=GOLD, scale_factor=1.05), run_time=0.65)
        self.finish()


class S02Cell(SpokenScene):
    def construct(self):
        cell = bacterium([0, 0.15, 0], 8.2, 4.15, 1)
        self.play(FadeIn(cell.body), run_time=0.55)
        self.at("single cell")
        self.play(FadeIn(cell.dna, scale=0.8), run_time=0.55)
        self.at("DNA in one loop")
        self.play(Rotate(cell.dna, angle=0.35), run_time=0.9)
        cell.dna.add_updater(lambda m, dt: m.rotate(0.10 * dt))
        label = place_label(T("chromosome\n(the cell's main DNA)", 28, BLUE,
                              line_spacing=0.8), cell.dna, avoid=[cell.body], dirs=(UP,))
        label.move_to([0, 2.75, 0])
        self.play(FadeIn(label), run_time=0.55)
        self.at("There is no nucleus")
        ghost = DashedVMobject(Circle(radius=1.22, color=GREY, stroke_width=4).move_to(cell.dna), num_dashes=22)
        x = VGroup(Line([-0.7, -0.7, 0], [0.7, 0.7, 0], color=RED, stroke_width=8),
                   Line([-0.7, 0.7, 0], [0.7, -0.7, 0], color=RED, stroke_width=8)).move_to(cell.dna)
        no = T("no nucleus", 30, RED).move_to([0, -2.6, 0])
        self.play(Create(ghost), run_time=0.45)
        self.play(Create(x), FadeIn(no), run_time=0.55)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Fission(SpokenScene):
    def construct(self):
        count = ValueTracker(1)
        ro = count_readout(count)
        cell = bacterium([0, -0.15, 0], 5.3, 2.75, 1)
        self.add(cell, ro, scope_tag("schematic"))
        step = T("1  COPY", 32, BLUE, weight=BOLD).move_to([0, 2.85, 0])
        self.at("cell copies")
        two_loops = bacterium([0, -0.15, 0], 5.3, 2.75, 2)
        self.play(FadeIn(step), Transform(cell.dna, two_loops.dna), run_time=1.0)
        self.at("then it grows")
        grow_lab = T("2  GROW", 32, GREEN, weight=BOLD).move_to(step)
        long = bacterium([0, -0.15, 0], 9.0, 2.75, 2)
        self.play(swap(step, grow_lab), Transform(cell, long), run_time=1.15)
        self.at("one copy at each end")
        self.play(cell.dna[0].animate.shift(LEFT * 0.6), cell.dna[1].animate.shift(RIGHT * 0.6), run_time=0.7)
        self.at("pinches in the middle")
        split_lab = T("3  SPLIT", 32, GOLD, weight=BOLD).move_to(step)
        daughters = VGroup(bacterium([-2.4, -0.15, 0], 4.3, 2.75, 1),
                           bacterium([2.4, -0.15, 0], 4.3, 2.75, 1))
        waist = VGroup(ArcBetweenPoints([0, 1.15, 0], [0, -0.15, 0], angle=-0.7, color=GREEN, stroke_width=6),
                       ArcBetweenPoints([0, -0.15, 0], [0, -1.45, 0], angle=-0.7, color=GREEN, stroke_width=6))
        self.play(swap(grow_lab, split_lab), Create(waist), run_time=0.55)
        self.at("splits in two")
        self.play(FadeOut(waist), ReplacementTransform(cell, daughters), count.animate.set_value(2), run_time=0.95)
        self.finish()


class S04Name(SpokenScene):
    def construct(self):
        daughters = VGroup(bacterium([-2.4, -0.2, 0], 4.3, 2.65, 1),
                           bacterium([2.4, -0.2, 0], 4.3, 2.65, 1))
        self.add(daughters, scope_tag("schematic"))
        bob(daughters[0], amp=0.055, speed=1.0)
        bob(daughters[1], amp=0.055, speed=1.0, seed=3)
        self.at("binary fission")
        banner = T("BINARY FISSION", 40, GREEN, weight=BOLD).move_to([0, 2.9, 0])
        self.play(FadeIn(banner, shift=DOWN * 0.15), run_time=0.6)
        self.at("complete copy")
        self.play(Indicate(daughters[0].dna, color=BLUE), Indicate(daughters[1].dna, color=BLUE), run_time=0.8)
        self.at("two cells match")
        equal = T("=", 52, TEXT, font=MONO).move_to([0, -0.2, 0])
        self.play(FadeIn(equal), run_time=0.45)
        self.at("rare copying mistakes")
        dot = Dot(daughters[1].dna[0].get_top() + DOWN * 0.12, radius=0.1, color=RED)
        rare = T("rare copying mistake", 28, RED).move_to([2.4, -2.25, 0])
        self.play(Flash(dot, color=RED, flash_radius=0.35), FadeIn(dot), FadeIn(rare), run_time=0.75)
        self.finish()


class S05Counter(SpokenScene):
    def construct(self):
        n = ValueTracker(2)
        ro = count_readout(n)
        cells = population(2, -0.15)
        self.add(cells, ro, scope_tag("schematic"))
        bob(cells, amp=0.07, speed=1.15)
        self.at("same thing")
        self.play(LaggedStart(*[Indicate(c.body, color=GREEN, scale_factor=1.08) for c in cells], lag_ratio=0.15), run_time=0.7)
        self.at("1 becomes 2")
        label = T("one doubling per round", 28, GOLD).move_to([-3.2, 3.15, 0])
        self.play(FadeIn(label), run_time=0.45)
        self.play(cells.animate.shift(UP * 0.35), run_time=1.15, rate_func=there_and_back)
        self.at("2 become 4")
        next_cells = population(4, -0.2)
        self.play(ReplacementTransform(cells, next_cells), n.animate.set_value(4), run_time=0.7)
        cells = next_cells
        self.at("then 8")
        next_cells = population(8, -0.2)
        self.play(ReplacementTransform(cells, next_cells), n.animate.set_value(8), run_time=0.65)
        cells = next_cells
        self.at("then 16")
        next_cells = population(16, -0.25)
        self.play(ReplacementTransform(cells, next_cells), n.animate.set_value(16), run_time=0.8)
        self.at("Every round doubles")
        self.play(Indicate(ro, color=GOLD, scale_factor=1.04), run_time=0.6)
        self.finish()


class S06Time(SpokenScene):
    def construct(self):
        n = ValueTracker(1)
        ro = count_readout(n)
        clock = clock_face(center=(-4.7, 0.55, 0), radius=1.45, label="doubling time")
        one = bacterium([1.5, 0.2, 0], 4.5, 2.3, 1)
        self.add(one, ro, scope_tag("schematic"))
        self.at("one round")
        self.play(FadeIn(clock), run_time=0.55)
        self.at("doubling time")
        self.play(Rotate(clock.hand, angle=TAU / 3, about_point=clock.center_point), run_time=0.8)
        self.at("best lab conditions")
        card = chip("E. coli • best lab conditions", GREEN, size=28).move_to([0, -2.55, 0])
        self.play(FadeIn(card), run_time=0.55)
        self.at("double about every 20 minutes")
        daughters = VGroup(bacterium([0.25, 0.2, 0], 3.55, 2.3, 1),
                           bacterium([3.95, 0.2, 0], 3.55, 2.3, 1))
        twenty = T("about 20 min", 34, GOLD, weight=BOLD).move_to([-4.7, -1.65, 0])
        self.play(ReplacementTransform(one, daughters), n.animate.set_value(2), FadeIn(twenty), run_time=1.0)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        backdrop = predict_backdrop()
        self.play(FadeIn(backdrop), run_time=0.65)
        self.at("seven hours")
        self.play(Indicate(backdrop[1], color=GOLD, scale_factor=1.05), run_time=0.55)
        self.at("no cells dying")
        no_death = T("no cells dying", 28, GREEN).move_to([-4.65, -1.45, 0])
        self.play(FadeIn(no_death), run_time=0.45)
        self.at("Will one cell")
        q = question_card("After 7 hours, which is closer?", ["about 1,000?", "about 1,000,000?"], y=-3.18)
        self.play(FadeIn(q.chips), run_time=0.55)
        self.play(FadeIn(q.question), run_time=0.55)
        bob(q.chips[0], amp=0.07, speed=1.2)
        bob(q.chips[1], amp=0.07, speed=1.2, seed=3)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "After 7 hours, which is closer?"
    OPTIONS = ["about 1,000?", "about 1,000,000?"]
    CARD = {"y": -3.18}

    def backdrop(self):
        return predict_backdrop()

    def construct(self):
        self.add(self.backdrop())
        q = question_card(self.QUESTION, self.OPTIONS, y=-3.18)
        self.add(q)
        for c in q.chips:
            pulse(c[0], base=2.5, amp=1.2, speed=2.1)
        bob(q.chips[0], amp=0.07, speed=1.2)
        bob(q.chips[1], amp=0.07, speed=1.2, seed=3)
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        self.play(run)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        doublings = ValueTracker(0)
        cells_n = ValueTracker(1)
        ro = Readout([("doublings", lambda: doublings.get_value(), "{:2.0f}", GOLD),
                      ("cells", lambda: cells_n.get_value(), "{:9,.0f}", TEXT)],
                     at=[3.95, 1.3, 0], widest=[21, 2097152], title="calculated", size=28)
        clock = clock_face(center=(-3.9, 1.35, 0), radius=1.45, label="7 hours")
        clock[-1].next_to(clock[0], UP, buff=0.18)
        choice = chip("about 1,000,000?", GOLD, size=30).move_to([3.95, -1.4, 0])
        haze = VGroup(*[Dot(radius=0.09, color=GREEN) for _ in range(120)]).arrange_in_grid(10, 12, buff=0.08).move_to([-3.9, -1.85, 0])
        self.add(clock, ro, choice, scope_tag("in this model"))
        self.at("More than a million")
        self.play(choice.animate.set_fill(GOLD, opacity=0.45), Indicate(choice, color=GOLD),
                  LaggedStart(*[FadeIn(d) for d in haze], lag_ratio=0.003), run_time=0.9)
        self.at("counter reaches")
        self.play(Rotate(clock.hand, angle=7 * TAU, about_point=clock.center_point),
                  doublings.animate.set_value(21), cells_n.animate.set_value(2097152),
                  haze.animate.scale(1.2), run_time=2.6, rate_func=linear)
        self.at("about 2 million")
        self.play(Indicate(ro.rows, color=GOLD, scale_factor=1.03), run_time=0.55)
        self.at("calculated number")
        stamp = T("CALCULATED • NOT COUNTED", 27, GREEN, weight=BOLD).move_to([3.5, -2.5, 0])
        self.play(FadeIn(stamp, shift=UP * 0.15), run_time=0.55)
        self.finish()


class S10Flask(SpokenScene):
    def construct(self):
        world = flask(cloudy=True).shift(LEFT * 1.4)
        haze = VGroup(*[Dot(radius=0.07, color=GREEN) for _ in range(55)]).arrange_in_grid(7, 8, buff=0.14).move_to([-1.4, -0.75, 0])
        food = ValueTracker(1.0); waste = ValueTracker(0.08); count = ValueTracker(50)
        food_dial = dial(food, [4.75, 1.25, 0], 1.15, "food", GREEN)
        waste_dial = dial(waste, [4.75, -1.65, 0], 1.15, "waste", BROWN)
        ro = count_readout(count, at=[4.0, 2.75, 0], widest=1000000)
        self.play(FadeIn(world), FadeIn(haze), run_time=0.65)
        bob(haze, amp=0.035, speed=0.7)
        self.at("real flask is closed")
        self.play(FadeIn(food_dial), FadeIn(waste_dial), FadeIn(ro), run_time=0.65)
        self.at("cells multiply")
        self.play(count.animate.set_value(8000), run_time=1.0, rate_func=linear)
        self.at("use up the food")
        self.play(food.animate.set_value(0.18), count.animate.set_value(10500), run_time=1.25, rate_func=linear)
        self.at("wastes build up")
        self.play(waste.animate.set_value(0.9), count.animate.set_value(11200), run_time=1.35, rate_func=linear)
        self.add(scope_tag("schematic"))
        self.finish()


def level_plot():
    P = Plot(box=(-5.8, 5.2, -2.25, 2.35), xr=(0, 10), yr=(0, 1.05),
             xticks=[0, 5, 10], yticks=[(0, "low"), (1, "high")],
             xlabel="time", ylabel="cell count", size=24, label_size=28)
    return P


def logistic(t):
    return 1.0 / (1.0 + 24.0 * np.exp(-1.0 * t))


class S11Level(SpokenScene):
    def construct(self):
        P = level_plot(); t = ValueTracker(0)
        live = P.live_curve(logistic, t, color=GREEN, width=7)
        dot = P.dot(lambda: t.get_value(), lambda: logistic(t.get_value()), color=GOLD, radius=0.11)
        area = always_redraw(lambda: Polygon(P.pt(0, 0),
                                             *[P.pt(x, logistic(x)) for x in np.linspace(0, max(0.02, t.get_value()), 50)],
                                             P.pt(max(0.02, t.get_value()), 0), stroke_width=0,
                                             fill_color=GREEN, fill_opacity=0.2))
        self.play(Create(P), run_time=0.65)
        self.add(area, live, dot, scope_tag("schematic"))
        self.at("climb slows")
        self.play(t.animate.set_value(7.0), run_time=2.0, rate_func=linear)
        self.at("count levels off")
        self.play(t.animate.set_value(10.0), run_time=1.15, rate_func=linear)
        labels = VGroup(chip("food low", GREEN, size=28), chip("wastes high", BROWN, size=28)).arrange(DOWN, buff=0.25).move_to([3.65, 0.75, 0])
        self.play(FadeIn(labels), run_time=0.55)
        self.at("Doubling makes numbers huge")
        self.play(Indicate(live, color=GOLD, scale_factor=1.0), run_time=0.65)
        self.at("only while food lasts")
        rule = caption("Doubling continues only while conditions allow it.", color=GOLD, y=-3.42)
        self.play(FadeIn(rule), run_time=0.6)
        self.finish()


class S12Virus(SpokenScene):
    def construct(self):
        water = liquid_field()
        food_bg = food_field()
        vir = phage([0, -0.25, 0], 1.9)
        count = ValueTracker(1)
        ro = count_readout(count, label="phages", at=[4.65, 2.55, 0], widest=1)
        foods = VGroup(*[Dot([x, y, 0], radius=0.1, color=GREEN) for x, y in
                         [(-4.7, 1.8), (-3.7, -1.4), (3.8, 1.4), (4.5, -1.1), (-2.8, 0.1)]])
        self.play(FadeIn(water), FadeIn(food_bg), FadeIn(vir, scale=0.85), FadeIn(ro), run_time=0.65)
        bob(vir, amp=0.09, speed=1.0)
        self.at("This one is a phage")
        name = T("phage (bacteriophage)", 32, ORANGE).move_to([0, 2.65, 0])
        self.play(FadeIn(name), run_time=0.55)
        self.at("infects bacteria")
        host_icon = mini_cell([-4.8, -2.3, 0], 0.9)
        self.play(FadeIn(host_icon), run_time=0.45)
        self.at("Left alone")
        self.play(FadeIn(foods), run_time=0.55)
        for d in foods: bob(d, amp=0.08, speed=0.8, seed=int(abs(d.get_x()) * 3))
        self.at("what does it do")
        q = T("What does it do alone?", 32, GOLD).move_to([0, -3.3, 0])
        self.play(FadeIn(q), run_time=0.55)
        self.add(scope_tag("schematic"))
        self.finish()


class S13Nothing(SpokenScene):
    def construct(self):
        water = liquid_field()
        food_bg = food_field()
        vir = phage([-3.7, 0.35, 0], 1.7)
        count = ValueTracker(1)
        ro = count_readout(count, label="phages", at=[4.55, 2.55, 0], widest=1)
        clk = clock_face(center=[3.8, -0.55, 0], radius=1.2, label="time passes")
        clk[0].set_fill("#0f1117", opacity=1)
        self.add(water, food_bg, vir, ro, clk, scope_tag("schematic")); bob(vir, amp=0.08, speed=0.9)
        self.at("Nothing")
        nothing = T("NOTHING", 44, TEXT, weight=BOLD).move_to([0, 2.75, 0])
        self.play(FadeIn(nothing), run_time=0.5)
        marks = VGroup()
        for text, y in [("grow", 1.0), ("split", 0.0), ("make anything", -1.0)]:
            lab = T(text, 30, GREY).move_to([0.2, y, 0])
            lab = VGroup(Rectangle(width=lab.width + 0.3, height=lab.height + 0.3, stroke_width=0, fill_color="#0f1117", fill_opacity=1).move_to(lab), lab)
            x = VGroup(Line([-0.32, 0.32, 0], [0.32, -0.32, 0], color=RED, stroke_width=7),
                       Line([-0.32, -0.32, 0], [0.32, 0.32, 0], color=RED, stroke_width=7)).next_to(lab, RIGHT, buff=0.3)
            marks.add(VGroup(lab, x))
        self.at("does not grow")
        self.play(FadeIn(marks[0][0]), Create(marks[0][1]), Rotate(clk.hand, TAU, about_point=clk.center_point), run_time=0.75)
        self.at("does not split")
        self.play(FadeIn(marks[1][0]), Create(marks[1][1]), Rotate(clk.hand, TAU, about_point=clk.center_point), run_time=0.75)
        self.at("cannot make anything")
        self.play(FadeIn(marks[2][0]), Create(marks[2][1]), Rotate(clk.hand, TAU, about_point=clk.center_point), run_time=0.8)
        self.at("counter stays at one")
        self.play(Indicate(ro, color=GOLD, scale_factor=1.04), run_time=0.65)
        self.finish()


class S14Land(SpokenScene):
    def construct(self):
        host = bacterium([1.0, -0.15, 0], 8.4, 4.2, 1)
        vir = phage([-4.7, 0.35, 0], 1.05).rotate(-PI / 2)
        self.add(host, vir, scope_tag("schematic"))
        pulse(host.body, base=5.0, amp=0.8, speed=1.5)
        self.at("lands on a bacterium")
        self.play(vir.animate.move_to([-3.15, 0.35, 0]), run_time=0.8)
        self.at("injects its DNA")
        dna = VMobject(color=ORANGE, stroke_width=6).set_points_smoothly([
            vir.head.get_center(), [-2.2, 0.3, 0], [-0.8, 0.0, 0], [0.2, 0.45, 0]])
        self.play(Create(dna), run_time=0.85)
        self.at("phage parts start")
        heads = VGroup(*[RegularPolygon(6, radius=0.28, color=ORANGE, stroke_width=4,
                                        fill_color=ORANGE, fill_opacity=0.4) for _ in range(4)])
        tails = VGroup(*[Line(ORIGIN, DOWN * 0.55, color=GREY, stroke_width=5) for _ in range(4)])
        heads.arrange(RIGHT, buff=0.45).move_to([1.55, 0.8, 0])
        tails.arrange(RIGHT, buff=0.45).move_to([1.55, -0.65, 0])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in VGroup(*heads, *tails)], lag_ratio=0.08), run_time=1.0)
        self.at("inside the cell")
        lab = T("phage parts", 30, ORANGE).move_to([1.55, -1.75, 0])
        self.play(FadeIn(lab), run_time=0.45)
        self.finish()


class S15Host(SpokenScene):
    def construct(self):
        host = bacterium([0.8, -0.1, 0], 9.6, 4.4, 1)
        coat = phage([-5.25, 0.45, 0], 0.85).rotate(-PI / 2).set_opacity(0.3)
        strand = VMobject(color=ORANGE, stroke_width=6).set_points_smoothly([[-2.8, 0.6, 0], [-1.8, 0.9, 0], [-0.7, 0.55, 0]])
        bench = RoundedRectangle(corner_radius=0.18, width=2.4, height=1.35, color=GREY,
                                 stroke_width=5, fill_color=GREY, fill_opacity=0.25).move_to([0.5, 1.25, 0])
        gear = T("host machinery", 28, TEXT).move_to(bench)
        out = VGroup(*[RegularPolygon(6, radius=0.23, color=ORANGE, stroke_width=3,
                                      fill_color=ORANGE, fill_opacity=0.4) for _ in range(5)]).arrange(RIGHT, buff=0.3).move_to([3.2, 1.25, 0])
        self.add(host, coat, strand, scope_tag("schematic"))
        pulse(host.body, base=5.0, amp=0.8, speed=1.4)
        bob(coat, amp=0.05, speed=1.0)
        self.at("phage is not making")
        idle = T("doing nothing", 28, GREY).move_to([-5.1, -1.75, 0])
        self.play(FadeIn(idle), run_time=0.5)
        self.at("The cell is")
        gear.layout_ok = True  # Deliberately printed on its own machinery block.
        self.play(FadeIn(bench), FadeIn(gear), run_time=0.6)
        self.at("reads the phage genes")
        self.play(strand.animate.move_to(bench), run_time=0.8)
        self.at("as if they were its own")
        self.play(Indicate(bench, color=ORANGE, scale_factor=1.04), run_time=0.65)
        self.at("builds phage parts")
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in out], lag_ratio=0.12), run_time=0.9)
        builds = T("the host cell builds", 32, GREEN, weight=BOLD).move_to([0.5, -2.5, 0])
        self.play(FadeIn(builds), run_time=0.45)
        self.finish()


class S16Contrast(SpokenScene):
    def construct(self):
        tp, left, host, parts = contrast_world()
        self.play(FadeIn(tp), run_time=0.55)
        self.at("opposite ways")
        middle = T("TWO WAYS TO MULTIPLY", 28, GOLD, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(middle), FadeIn(left), FadeIn(host), run_time=0.55)
        self.at("bacterium grows")
        self.play(Indicate(left.body, color=GREEN, scale_factor=1.03), run_time=0.55)
        daughters = VGroup(bacterium([-4.4, 0.2, 0], 2.15, 1.75, 1), bacterium([-2.1, 0.2, 0], 2.15, 1.75, 1))
        self.at("splits on its own")
        self.play(ReplacementTransform(left, daughters), run_time=0.8)
        self.at("virus never divides")
        lone = phage([3.25, 1.65, 0], 0.55)
        self.play(FadeIn(lone), Indicate(lone, color=ORANGE, scale_factor=1.0), run_time=0.65)
        self.play(lone.animate.shift(UP * 0.22), run_time=1.15, rate_func=there_and_back)
        self.at("host cell builds")
        self.play(LaggedStart(*[FadeIn(p) for p in parts], lag_ratio=0.1), run_time=0.85)
        self.at("every new virus")
        made = VGroup(*[phage(ORIGIN, 0.4) for _ in range(4)]).arrange(RIGHT, buff=0.4).move_to([3.25, -1.45, 0])
        self.play(ReplacementTransform(parts, made), run_time=0.75)
        self.finish()


class S17Takehome(SpokenScene):
    def construct(self):
        tp, left, host, parts = contrast_world()
        self.add(tp, left, host, parts)
        self.at("one rule to keep")
        heading = T("ONE RULE", 32, GOLD, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(heading), run_time=0.55)
        self.at("bacterium copies itself")
        left_rule = fit_text("copies itself", max_w=5.2, size=38, color=GREEN, weight=BOLD).move_to([-3.25, -1.72, 0])
        self.play(FadeIn(left_rule, shift=UP * 0.12), left.animate.shift(UP * 0.25), run_time=0.8)
        self.at("virus is copied")
        right_rule = fit_text("is copied by a host cell", max_w=5.3, size=34, color=ORANGE, weight=BOLD).move_to([3.25, -1.72, 0])
        self.play(FadeIn(right_rule, shift=UP * 0.12), host.animate.shift(UP * 0.2), run_time=0.8)
        self.at("never by itself")
        self.play(Indicate(right_rule, color=GOLD, scale_factor=1.04), run_time=0.7)
        self.finish()


class S18End(EndCard):
    LINE = "A bacterium copies itself; a virus is copied by a host cell."
