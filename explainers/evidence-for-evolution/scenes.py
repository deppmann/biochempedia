"""How Rocks Put Fossils in Order.

COLOR MAP
  GREY = sedimentary rock
  GOLD = fossils
  RED  = volcanic ash / radiometric dates
  BLUE = inherited information
  GREEN = anatomy
  TEAL = development
  TEXT = time arrows and evolutionary branches

All diagrams are schematic.  The cliff, disturbed blocks, and whale tree are
built by shared functions so carried pictures keep exactly the same geometry.
"""
from bp_parts import *


ROCK = "#78818D"
ROCK_DARK = "#59616C"
ASH = RED
FOSSIL = GOLD


def _layer_pattern(width, y, style, x=0, height=0.82):
    """One textured rock layer. Texture distinguishes matching layers."""
    fill = ROCK if style % 2 == 0 else ROCK_DARK
    rect = Rectangle(width=width, height=height, stroke_color=GREY, stroke_width=2.5,
                     fill_color=fill, fill_opacity=0.34).move_to([x, y, 0])
    marks = VGroup()
    if style == 0:
        for dx in np.linspace(-width / 2 + 0.35, width / 2 - 0.35, 7):
            marks.add(Line([x + dx - 0.13, y - 0.12, 0], [x + dx + 0.13, y + 0.12, 0],
                           color=GREY, stroke_width=1.5).set_opacity(0.45))
    elif style == 1:
        for dx in np.linspace(-width / 2 + 0.32, width / 2 - 0.32, 9):
            marks.add(Dot([x + dx, y, 0], radius=0.035, color=GREY).set_opacity(0.65))
    elif style == 2:
        for dx in np.linspace(-width / 2 + 0.4, width / 2 - 0.4, 6):
            marks.add(Line([x + dx - 0.16, y, 0], [x + dx + 0.16, y, 0],
                           color=GREY, stroke_width=2).set_opacity(0.55))
    else:
        for dx in np.linspace(-width / 2 + 0.35, width / 2 - 0.35, 7):
            marks.add(Arc(radius=0.13, start_angle=0, angle=PI, color=GREY,
                          arc_center=[x + dx, y - 0.08, 0], stroke_width=1.5).set_opacity(0.5))
    return VGroup(rect, marks)


def whale_fossil(kind="legs", scale=1.0, color=FOSSIL):
    """A simple whale fossil silhouette, not an anatomical reconstruction."""
    body = Ellipse(width=1.8, height=0.62, stroke_color=color, stroke_width=5,
                   fill_color=color, fill_opacity=0.15)
    head = Circle(radius=0.25, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=0.15).next_to(body, RIGHT, buff=-0.08)
    tail = VGroup(
        Polygon([-0.9, 0.02, 0], [-1.35, 0.35, 0], [-1.18, 0.0, 0],
                color=color, stroke_width=3, fill_color=color, fill_opacity=0.2),
        Polygon([-0.9, -0.02, 0], [-1.35, -0.35, 0], [-1.18, 0.0, 0],
                color=color, stroke_width=3, fill_color=color, fill_opacity=0.2),
    )
    g = VGroup(body, head, tail)
    if kind == "legs":
        g.add(Line([-0.28, -0.22, 0], [-0.38, -0.68, 0], color=color, stroke_width=6),
              Line([0.35, -0.22, 0], [0.42, -0.62, 0], color=color, stroke_width=6),
              Line([-0.38, -0.68, 0], [-0.65, -0.68, 0], color=color, stroke_width=5),
              Line([0.42, -0.62, 0], [0.66, -0.62, 0], color=color, stroke_width=5))
    elif kind == "small":
        g.add(Line([0.05, -0.25, 0], [0.02, -0.48, 0], color=color, stroke_width=5),
              Line([0.02, -0.48, 0], [0.19, -0.48, 0], color=color, stroke_width=4))
    return g.scale(scale)


def shell_fossil(scale=1.0, color=FOSSIL):
    arcs = VGroup(*[Arc(radius=r, start_angle=-0.25 * PI, angle=1.65 * PI,
                        color=color, stroke_width=4) for r in (0.18, 0.34, 0.5)])
    return arcs.scale(scale)


def cliff_stack(x=-1.0, width=8.4, bottom=-2.45, layer_h=0.86, fossils=True):
    layers = VGroup(*[_layer_pattern(width, bottom + layer_h * (i + 0.5), i, x, layer_h)
                      for i in range(6)])
    fs = VGroup()
    if fossils:
        older = whale_fossil("legs", 0.58).move_to([x - 1.6, bottom + layer_h * 1.5, 0])
        later = whale_fossil("small", 0.58).move_to([x + 1.45, bottom + layer_h * 4.5, 0])
        fs.add(older, later)
    return VGroup(layers, fs)


def wave_group():
    waves = VGroup(*[ArcBetweenPoints([-6.65 + i * 1.35, -3.05, 0],
                                      [-5.75 + i * 1.35, -3.05, 0], angle=-0.45,
                                      color=BLUE, stroke_width=4) for i in range(10)])
    pulse(waves, base=4, amp=1.2, speed=2.2)
    return waves


def sediment_drift(n=18, xspan=(-5.4, 3.4), yspan=(-2.4, 2.65), seed=3):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(n):
        d = Dot([rng.uniform(*xspan), rng.uniform(*yspan), 0], radius=0.025,
                color=GREY).set_opacity(0.42)
        d.speed = rng.uniform(0.025, 0.07)
        lo, hi = yspan
        def fall(m, dt, lo=lo, hi=hi):
            m.shift(DOWN * m.speed * dt)
            if m.get_y() < lo:
                m.shift(UP * (hi - lo))
        d.add_updater(fall)
        dots.add(d)
    return dots


def time_arrow(x=4.45, y0=-2.35, y1=2.45, labels=True):
    ar = Arrow([x, y0, 0], [x, y1, 0], buff=0, color=TEXT, stroke_width=7,
               tip_length=0.28)
    g = VGroup(ar)
    if labels:
        g.add(T("older", 30, FOSSIL).next_to([x, y0, 0], RIGHT, buff=0.25),
              T("younger", 30, TEXT).next_to([x, y1, 0], RIGHT, buff=0.25))
    return g


def moving_time_marker(x=-5.35, y0=-2.2, y1=2.35, period=7.0):
    """A visible time cursor for long holds on an ordered sequence."""
    d = Dot([x, y0, 0], radius=0.11, color=FOSSIL, stroke_color=TEXT, stroke_width=2)
    d.clock = 0.0
    def travel(m, dt):
        m.clock += dt
        phase = (m.clock % period) / period
        m.move_to([x, y0 + (y1 - y0) * phase, 0])
    return d.add_updater(travel)


def disturbed_cliff(question=True):
    """Three fault-bounded blocks made from matching textured layers."""
    blocks = VGroup()
    for bx in (-3.55, -0.55, 2.45):
        layers = VGroup(*[_layer_pattern(2.72, -1.65 + 0.78 * (i + 0.5), i, bx, 0.78)
                          for i in range(5)])
        fossil = shell_fossil(0.62).move_to([bx, -1.65 + 0.78 * 1.5, 0])
        block = VGroup(layers, fossil)
        blocks.add(block)
    blocks[0].rotate(9 * DEGREES)
    blocks[1].rotate(26 * DEGREES)
    blocks[2].rotate(154 * DEGREES)
    q = T("?", 82, FOSSIL, weight=BOLD).move_to([5.35, 0.15, 0]) if question else VGroup()
    return VGroup(blocks, q)


def record_book():
    pages = VGroup()
    for i in range(4):
        page = RoundedRectangle(corner_radius=0.15, width=8.1, height=4.9,
                                stroke_color=GREY, stroke_width=3,
                                fill_color=ROCK, fill_opacity=0.10)
        page.shift(RIGHT * 0.22 * i + UP * 0.12 * i)
        pages.add(page)
    spine = Line([-4.25, -2.45, 0], [-4.25, 2.45, 0], color=GREY, stroke_width=6)
    fossils = VGroup(whale_fossil("legs", 0.63).move_to([-2.0, -1.35, 0]),
                     whale_fossil("small", 0.63).move_to([0.0, 0.0, 0]),
                     whale_fossil("none", 0.63).move_to([2.0, 1.35, 0]))
    return VGroup(pages, spine, fossils).move_to([-0.25, 0.15, 0])


def whale_tree():
    trunk = Line([-4.6, -2.25, 0], [-4.6, 2.45, 0], color=TEXT, stroke_width=5)
    branches = VGroup()
    whales = VGroup()
    specs = [(-1.25, "legs"), (0.15, "small"), (1.6, "none")]
    for i, (y, kind) in enumerate(specs):
        tip = [-1.2 + i * 0.52, y + 0.34, 0]
        branches.add(Line([-4.6, y, 0], tip, color=TEXT, stroke_width=4))
        whales.add(whale_fossil(kind, 0.62).move_to([tip[0] + 1.0, tip[1], 0]))
    arrow = Arrow([-5.35, -2.25, 0], [-5.35, 2.55, 0], buff=0, color=TEXT,
                  stroke_width=6, tip_length=0.25)
    return VGroup(trunk, branches, whales, arrow)


def evidence_lanes(x0=1.5, x1=5.8):
    return VGroup(Line([x0, 1.15, 0], [x1, 1.15, 0], color=BLUE, stroke_width=8),
                  Line([x0, 0.0, 0], [x1, 0.0, 0], color=GREEN, stroke_width=8),
                  Line([x0, -1.15, 0], [x1, -1.15, 0], color=TEAL, stroke_width=8))


class S00Hook(SpokenScene):
    def construct(self):
        waves = wave_group()
        self.add(waves)
        self.at("How can a whale")
        stack = cliff_stack(x=-0.7, width=9.4)
        layers, fossils = stack
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.18) for l in layers], lag_ratio=0.12),
                  run_time=3.0)
        self.at("whale with legs")
        self.play(FadeIn(fossils[0], scale=0.7), run_time=1.1)
        self.at("whale built for open water")
        self.play(FadeIn(fossils[1], scale=0.7), run_time=1.1)
        self.at("Imagine a cliff")
        self.play(stack.animate.scale(1.06), run_time=1.6)
        self.at("read its layers")
        self.play(LaggedStart(*[Indicate(l[0], color=TEXT, scale_factor=1.01) for l in layers],
                              lag_ratio=0.12), run_time=2.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Evidence for evolution"
    TITLE = "How Rocks Put Fossils in Order"


class S02Fossil(SpokenScene):
    def construct(self):
        fossil = shell_fossil(2.1).move_to([0, -1.45, 0])
        self.at("A fossil is")
        self.play(FadeIn(fossil, scale=0.7), run_time=1.0)
        examples = VGroup(T("bone", 30, FOSSIL), T("shell", 30, FOSSIL),
                          T("tooth", 30, FOSSIL), T("footprint", 30, FOSSIL)).arrange(RIGHT, buff=0.65).to_edge(UP, buff=0.48)
        self.at("such as a bone")
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.12) for x in examples], lag_ratio=0.18),
                  run_time=2.2)
        self.at("Watch sediment bury")
        first = _layer_pattern(11.1, -1.3, 0, 0, 1.05)
        self.play(FadeOut(examples), FadeIn(first, shift=RIGHT * 1.6), run_time=2.0)
        self.at("settle then bury another")
        second_f = whale_fossil("legs", 0.68).move_to([2.25, -0.35, 0])
        self.play(FadeIn(second_f, scale=0.8), run_time=0.8)
        second = _layer_pattern(11.1, -0.28, 1, 0, 1.0)
        third = _layer_pattern(11.1, 0.72, 2, 0, 1.0)
        self.play(FadeIn(second, shift=RIGHT * 1.3), run_time=1.6)
        self.play(FadeIn(third, shift=LEFT * 1.3), run_time=1.4)
        self.at("The lower layer")
        self.play(Indicate(first[0], color=FOSSIL, scale_factor=1.01), run_time=1.1)
        self.at("layer above it")
        self.play(Indicate(third[0], color=TEXT, scale_factor=1.01), FadeIn(scope_tag("schematic")), run_time=1.0)
        self.finish()


class S03Relative(SpokenScene):
    def construct(self):
        stack = cliff_stack(x=-1.35, width=8.0)
        dust = sediment_drift(15, (-5.25, 2.55), (-2.35, 2.55), 5)
        self.add(stack, dust)
        self.at("That order")
        tag = chip("relative dating", FOSSIL, 34).move_to([4.35, 0.2, 0])
        self.play(FadeIn(tag, shift=LEFT * 0.2), run_time=1.0)
        self.at("which layer is older")
        self.play(Indicate(stack[0][1][0], color=FOSSIL), run_time=1.2)
        self.at("without giving an age")
        no_age = T("order ≠ age in years", 31, TEXT).move_to([4.35, -1.0, 0])
        self.play(FadeIn(no_age), run_time=1.0)
        self.at("In an undisturbed stack")
        self.play(LaggedStart(*[Indicate(l[0], color=GREY, scale_factor=1.01) for l in stack[0]],
                              lag_ratio=0.12), run_time=2.2)
        self.at("lower layers formed first")
        ar = time_arrow(3.95)
        self.play(FadeOut(tag), FadeOut(no_age), GrowArrow(ar[0]), FadeIn(ar[1]), run_time=1.5)
        self.at("points upward")
        self.play(FadeIn(ar[2]), ar[0].animate.set_stroke(width=10), run_time=1.2)
        self.at("younger rock")
        self.play(Indicate(ar[2], color=TEXT), run_time=1.0)
        self.finish()


class S04Record(SpokenScene):
    def construct(self):
        cliff = cliff_stack(x=-0.4, width=8.0)
        self.add(cliff)
        self.at("The fossil record")
        book = record_book()
        self.play(ReplacementTransform(cliff, book), run_time=2.0)
        self.at("every fossil found")
        self.play(LaggedStart(*[Indicate(f, color=FOSSIL, scale_factor=1.08) for f in book[2]],
                              lag_ratio=0.22), run_time=2.0)
        self.at("arranged by age")
        ar = time_arrow(4.55, -2.1, 2.35)
        self.play(GrowArrow(ar[0]), FadeIn(ar[1]), FadeIn(ar[2]), run_time=1.5)
        self.at("appearing changing")
        self.play(Transform(book[2][0], whale_fossil("small", 0.63).move_to(book[2][0])),
                  book[2][1].animate.scale(1.12), run_time=1.5)
        self.at("often going extinct")
        self.play(FadeOut(book[2][2], shift=UP * 0.2), run_time=1.1)
        self.at("One cliff holds")
        one = T("one cliff = one page", 34, FOSSIL).move_to([0, -3.05, 0])
        self.play(FadeIn(one), book.animate.scale(0.94), run_time=1.2)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        straight = cliff_stack(x=-0.5, width=8.3)
        self.add(straight)
        self.at("Now the cliff tilts")
        self.play(straight.animate.rotate(10 * DEGREES), run_time=2.0)
        self.at("one block turns")
        moved = disturbed_cliff(True)
        self.play(ReplacementTransform(straight, moved), run_time=2.4)
        self.at("Which fossil is older")
        q = question_card("Which fossil is older after the rocks move?", y=-3.22,
                          size=31, max_w=10.8)
        self.play(FadeIn(q.question), run_time=1.1)
        self.at("Follow the matching layers")
        self.play(LaggedStart(*[Indicate(b[0][1][0], color=FOSSIL, scale_factor=1.02)
                                for b in moved[0]], lag_ratio=0.2), run_time=2.0)
        self.at("not simply the bottom")
        self.play(Indicate(moved[1], color=FOSSIL), run_time=1.0)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Which fossil is older after the rocks move?"
    SECONDS = 4.5
    CARD = {"y": -3.22, "size": 31, "max_w": 10.8}

    def backdrop(self):
        d = disturbed_cliff(True)
        pulse(d[0][0][0][1], base=2.5, amp=1.5, speed=1.8)
        pulse(d[0][2][0][1], base=2.5, amp=1.5, speed=1.8)
        return VGroup(d, sediment_drift(16, (-5.4, 4.0), (-2.2, 2.4), 8))


class S07Reveal(SpokenScene):
    def construct(self):
        moved = disturbed_cliff(False)
        self.add(moved)
        self.at("Tilting changes the angle")
        traces = VGroup(*[moved[0][i][0][1][0].copy().set_stroke(FOSSIL, width=7)
                          for i in range(3)])
        self.play(LaggedStart(*[Create(t) for t in traces], lag_ratio=0.2), run_time=2.2)
        self.at("not the order")
        self.play(*[Indicate(b[1], color=FOSSIL) for b in moved[0]], run_time=1.2)
        self.at("Folding flipping or faults")
        self.play(LaggedStart(*[Rotate(b, angle=(-9, -26, -154)[i] * DEGREES)
                                for i, b in enumerate(moved[0])], lag_ratio=0.12), run_time=3.0)
        self.at("move old rock above")
        self.play(LaggedStart(*[Indicate(b[0][1][0], color=FOSSIL) for b in moved[0]],
                              lag_ratio=0.15), run_time=1.5)
        self.at("reconstruct the stack")
        aligned = cliff_stack(x=-1.45, width=7.8)
        self.play(FadeOut(traces), ReplacementTransform(moved, aligned), run_time=2.0)
        self.at("lower means older")
        ar = time_arrow(3.25)
        lanes = evidence_lanes(4.15, 6.35).scale(0.65, about_point=[4.15, 0, 0])
        self.play(GrowArrow(ar[0]), FadeIn(ar[1]), FadeIn(ar[2]),
                  LaggedStart(*[Create(x) for x in lanes], lag_ratio=0.15), run_time=1.5)
        self.finish()


class S08Dating(SpokenScene):
    def construct(self):
        stack = cliff_stack(x=-3.2, width=5.5)
        self.add(stack)
        self.at("Relative order")
        contrast = T("order  ≠  age in years", 32, FOSSIL).move_to([3.15, 2.0, 0])
        self.play(FadeIn(contrast), run_time=1.6)
        self.at("Radioactive dating")
        ash = Rectangle(width=5.5, height=0.28, stroke_color=ASH, fill_color=ASH,
                        fill_opacity=0.8).move_to([-3.2, 0.35, 0])
        self.play(FadeIn(ash, shift=RIGHT * 1.2), run_time=1.6)
        self.at("certain minerals")
        mineral = chip("mineral", ASH, 30).move_to([3.2, 0.78, 0])
        self.play(FadeOut(contrast), FadeIn(mineral), run_time=1.0)
        frac = ValueTracker(1.0)
        left, y, W, H = 0.75, -0.45, 5.1, 1.0
        outline = Rectangle(width=W, height=H, stroke_color=GREY, stroke_width=3).move_to([left + W / 2, y, 0])
        start = always_redraw(lambda: Rectangle(width=max(0.01, W * frac.get_value()), height=H,
                    stroke_width=0, fill_color=ASH, fill_opacity=0.7).move_to([left + W * frac.get_value() / 2, y, 0]))
        prod = always_redraw(lambda: Rectangle(width=max(0.01, W * (1-frac.get_value())), height=H,
                    stroke_width=0, fill_color=TEXT, fill_opacity=0.65).move_to([left + W - W * (1-frac.get_value()) / 2, y, 0]))
        labs = VGroup(T("starting atoms", 28, ASH).move_to([2.0, -1.35, 0]),
                      T("product atoms", 28, TEXT).move_to([4.7, -1.35, 0]))
        self.at("Starting atoms")
        self.play(FadeIn(outline), FadeIn(start), FadeIn(labs[0]), run_time=1.0)
        self.at("change into product")
        self.add(prod)
        self.play(frac.animate.set_value(0.52), FadeIn(labs[1]), run_time=2.6, rate_func=linear)
        self.at("steady rate")
        steady = T("steady rate", 30, TEXT).move_to([3.25, -2.15, 0])
        self.play(FadeIn(steady), frac.animate.set_value(0.38), run_time=1.5, rate_func=linear)
        self.at("measured amounts")
        self.play(Indicate(VGroup(start, prod), color=FOSSIL), run_time=1.1)
        self.at("when the mineral formed")
        self.play(FadeIn(caption("amounts → estimated formation time", color=FOSSIL)),
                  frac.animate.set_value(0.3), run_time=1.5)
        self.finish()


class S09Bracket(SpokenScene):
    def construct(self):
        rock = _layer_pattern(8.4, 0, 1, -1.3, 1.25)
        fossil = whale_fossil("legs", 0.75).move_to([-1.3, 0, 0])
        self.add(rock, fossil)
        self.at("Watch two volcanic ash")
        lower = Rectangle(width=8.4, height=0.34, stroke_color=ASH, fill_color=ASH,
                          fill_opacity=0.8).move_to([-1.3, -1.2, 0])
        upper = lower.copy().move_to([-1.3, 1.2, 0])
        self.play(FadeIn(lower, shift=DOWN * 1.0), FadeIn(upper, shift=UP * 1.0), run_time=2.5)
        self.at("lower ash formed earlier")
        old = chip("older date", ASH, 30).move_to([5.3, -1.2, 0])
        self.play(FadeIn(old), Indicate(lower, color=ASH), run_time=1.5)
        self.at("upper ash formed later")
        young = chip("younger date", ASH, 30).move_to([5.3, 1.2, 0])
        self.play(FadeIn(young), Indicate(upper, color=ASH), run_time=1.5)
        self.at("dates bracket the fossil")
        brackets = VGroup(Line([3.0, -0.95, 0], [3.0, -0.35, 0], color=ASH, stroke_width=7),
                          Line([3.0, 0.95, 0], [3.0, 0.35, 0], color=ASH, stroke_width=7))
        self.play(Create(brackets), brackets.animate.shift(LEFT * 1.1), run_time=1.7)
        self.at("neither gives its exact age")
        exact = T("exact age: unknown", 32, TEXT).move_to([0, -2.55, 0])
        self.play(FadeIn(exact), run_time=1.2)
        self.finish()


class S10Match(SpokenScene):
    def construct(self):
        panels = TwoPanel("cliff nearby", "dated rocks elsewhere", colors=(GREY, ASH), top=3.0, bottom=-2.5)
        self.at("More often")
        self.play(FadeIn(panels), run_time=1.1)
        def mini_cliff(x):
            ls = VGroup(*[_layer_pattern(5.3, -1.7 + i * 0.8, i, x, 0.78) for i in range(5)])
            sh = shell_fossil(0.72).move_to([x, -0.5, 0])
            return VGroup(ls, sh)
        left, right = mini_cliff(-3.25), mini_cliff(3.25)
        self.at("no volcanic layer")
        self.play(FadeIn(left, shift=UP * 0.2), run_time=1.4)
        self.at("match a fossil layer")
        self.play(FadeIn(right, shift=UP * 0.2), run_time=1.5)
        self.at("dated rocks elsewhere")
        ash = Rectangle(width=5.3, height=0.26, stroke_color=ASH, fill_color=ASH,
                        fill_opacity=0.85).move_to([3.25, 1.35, 0])
        self.play(FadeIn(ash), run_time=1.0)
        self.at("Index fossils help")
        self.play(Indicate(left[1], color=FOSSIL), Indicate(right[1], color=FOSSIL), run_time=1.5)
        self.at("known span of time")
        match = DashedLine(left[1].get_right(), right[1].get_left(), color=FOSSIL,
                           stroke_width=5, dash_length=0.16)
        self.play(Create(match), run_time=1.6)
        self.finish()


class S11Gaps(SpokenScene):
    def construct(self):
        book = record_book()
        self.at("The cliff is not")
        self.play(FadeIn(book), run_time=1.3)
        self.at("Most remains rot")
        gone = book[2][0].copy()
        self.play(gone.animate.set_opacity(0.08).scale(0.7), run_time=1.6)
        self.at("never get buried quickly")
        gap1 = Rectangle(width=8.4, height=0.52, stroke_width=0, fill_color=BG,
                         fill_opacity=1).move_to([0, -0.72, 0])
        self.play(FadeIn(gap1), run_time=1.3)
        self.at("Water and sediment")
        panels = TwoPanel("forest", "seafloor", colors=(GREEN, BLUE), top=2.8, bottom=-2.35)
        forest = VGroup(*[Line([-4.5+i*0.55,-1.4,0],[-4.5+i*0.55,0.8,0], color=GREEN, stroke_width=7)
                          for i in range(5)])
        sea = VGroup(shell_fossil(1.15).move_to([3.25, -0.8, 0]),
                     _layer_pattern(4.8, -1.25, 2, 3.25, 0.65))
        self.play(FadeOut(book), FadeOut(gone), FadeOut(gap1), FadeIn(panels),
                  FadeIn(forest), FadeIn(sea), run_time=2.1)
        self.at("favor some environments")
        self.play(forest.animate.set_opacity(0.15),
                  FadeIn(_layer_pattern(4.8, -0.62, 1, 3.25, 0.65), shift=DOWN * 0.3), run_time=1.8)
        self.at("book with many missing pages")
        book2 = record_book()
        gaps = VGroup(*[Rectangle(width=8.5, height=0.38, stroke_width=0, fill_color=BG,
                                  fill_opacity=1).move_to([0, y, 0]) for y in (-1.15, 0.25, 1.2)])
        self.play(FadeOut(VGroup(panels, forest, sea)), FadeIn(book2),
                  LaggedStart(*[FadeIn(g) for g in gaps], lag_ratio=0.2), run_time=2.1)
        self.finish()


class S12Sequence(SpokenScene):
    def construct(self):
        tree = whale_tree()
        self.add(sediment_drift(14, (-6.0, 5.8), (-2.45, 2.65), 12))
        self.at("Even with gaps")
        self.play(Create(tree[0]), GrowArrow(tree[3]), run_time=1.5)
        self.add(moving_time_marker())
        self.at("ordered sequence")
        self.play(LaggedStart(*[Create(b) for b in tree[1]], lag_ratio=0.25), run_time=2.1)
        self.at("Older whale fossils")
        self.play(FadeIn(tree[2][0], scale=0.7), run_time=1.3)
        legs = T("legs and feet", 30, FOSSIL).move_to([3.9, -1.55, 0])
        self.play(FadeIn(legs), run_time=0.9)
        self.at("Later forms")
        self.play(FadeIn(tree[2][1], scale=0.7), run_time=1.2)
        small = T("smaller hind limbs", 30, FOSSIL).move_to([4.0, -0.05, 0])
        self.play(FadeIn(small), run_time=1.0)
        self.at("The sequence shows change")
        self.play(FadeIn(tree[2][2], scale=0.7),
                  LaggedStart(*[Indicate(w, color=FOSSIL, scale_factor=1.05) for w in tree[2]],
                              lag_ratio=0.2), run_time=2.2)
        self.at("Not that one named fossil")
        note = caption("branch tips ≠ a parent-to-child chain", color=TEXT)
        self.play(FadeOut(legs), FadeOut(small), FadeIn(note), run_time=1.4)
        self.at("direct ancestor")
        self.play(Indicate(tree[1], color=TEXT, scale_factor=1.01), run_time=1.2)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        tree = whale_tree().scale(0.88).move_to([-0.7, 0, 0])
        self.add(tree, moving_time_marker(x=-4.75, y0=-2.0, y1=2.15),
                 sediment_drift(14, (-6.0, 5.8), (-2.5, 2.65), 13))
        pulse(tree[0], base=5, amp=2.5, speed=2.5)
        self.at("One line of evidence")
        tilted = VGroup(*[_layer_pattern(1.5, -0.25 + i * 0.38, i, -5.45, 0.36)
                          for i in range(3)]).rotate(18 * DEGREES)
        bob(tilted, amp=0.4, speed=1.6, seed=1)
        self.play(FadeIn(tilted), run_time=1.1)
        self.at("Rocks may be disturbed")
        self.play(Rotate(tilted, angle=18 * DEGREES), run_time=1.2)
        self.at("dates may only bracket")
        br = VGroup(Line([-6.0, -0.85, 0], [-5.0, -0.85, 0], color=ASH, stroke_width=6),
                    Line([-6.0, -1.35, 0], [-5.0, -1.35, 0], color=ASH, stroke_width=6))
        bob(br, amp=0.35, speed=1.7, seed=3)
        self.play(FadeIn(br), run_time=1.1)
        self.at("fossils may be missing")
        page = RoundedRectangle(corner_radius=0.1, width=1.2, height=0.85,
                                color=GREY, stroke_width=3).move_to([-5.5, -2.25, 0])
        gap = Rectangle(width=0.55, height=0.9, fill_color=BG, fill_opacity=1,
                        stroke_width=0).move_to(page)
        missing = VGroup(page, gap)
        bob(missing, amp=0.35, speed=1.5, seed=5)
        self.play(FadeIn(missing), run_time=1.2)
        self.at("A different method")
        lane = Line([2.0, 1.8, 0], [5.9, 1.8, 0], color=BLUE, stroke_width=9)
        self.play(Create(lane), run_time=1.8)
        self.at("check the same history")
        checks = VGroup(*[T("✓", 32, c).move_to([6.25, y, 0])
                          for y, c in ((1.8, BLUE), (0.75, GREEN), (-0.3, TEAL))])
        lanes = VGroup(Line([2.0, 0.75, 0], [5.9, 0.75, 0], color=GREEN, stroke_width=9),
                       Line([2.0, -0.3, 0], [5.9, -0.3, 0], color=TEAL, stroke_width=9))
        self.play(LaggedStart(*[Create(l) for l in lanes], lag_ratio=0.2), FadeIn(checks), run_time=1.8)
        self.at("Independent evidence that agrees")
        for _ln in (lane, *lanes):
            pulse(_ln, base=8, amp=2.5, speed=2.2)
        rule = caption("Agreement among independent evidence strengthens the explanation.",
                       color=FOSSIL, size=32)
        self.play(FadeOut(VGroup(tilted, br, missing)), FadeIn(rule),
                  LaggedStart(*[Indicate(x, color=x.get_color(), scale_factor=1.01)
                                for x in VGroup(lane, *lanes)], lag_ratio=0.15), run_time=2.2)
        self.at("common descent")
        self.play(Indicate(tree, color=TEXT, scale_factor=1.02), run_time=1.3)
        self.finish()


class S14Handoff(SpokenScene):
    def construct(self):
        cliff = cliff_stack(x=-3.8, width=4.5)
        tree = whale_tree().scale(0.74).move_to([-0.2, 0, 0])
        self.add(cliff, tree)
        self.at("This film built")
        timeline = VGroup(Line([-5.75, -2.15, 0], [-5.75, 2.3, 0], color=GREY, stroke_width=12),
                          Arrow([-5.75, -2.15, 0], [-5.75, 2.5, 0], buff=0,
                                color=TEXT, stroke_width=5, tip_length=0.22))
        self.play(ReplacementTransform(cliff, timeline), run_time=2.0)
        self.at("Bodies and inherited information")
        lanes = evidence_lanes(3.0, 6.6)
        labels = VGroup(T("DNA", 30, BLUE), T("anatomy", 30, GREEN),
                        T("development", 30, TEAL))
        for lab, ln in zip(labels, lanes):
            lab.next_to(ln, UP, buff=0.12, aligned_edge=LEFT)
        self.play(LaggedStart(*[Create(l) for l in lanes], lag_ratio=0.18),
                  LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.18), run_time=2.5)
        self.at("same branching history")
        pulse(tree[0], base=5, amp=1.5, speed=2)
        self.play(Indicate(tree, color=TEXT, scale_factor=1.02), run_time=1.4)
        self.finish()


class S15End(EndCard):
    LINE = "Independent evidence that agrees strengthens an explanation of common descent."
