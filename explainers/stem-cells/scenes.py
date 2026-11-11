"""Stem-cell pools: stable positions, changing clones.

COLOR MAP
  BLUE   stem cells before lineage marking
  GREY   crypt, epithelium, differentiated daughters
  GREEN  permanent lineage mark / one Confetti clone
  YELLOW tamoxifen pulse / one Confetti clone
  RED    loss, short-lived outcome / one Confetti clone
  TEAL   niche-supported pool / cyan Confetti clone
  GOLD   questions and the chance spinner

All crypt scenes use the same geometry.  The picture is a simplified schematic;
no curve or quantitative readout is invented.
"""
from bp_style import *  # noqa: F401,F403


CX = -2.35
CRYPT_R = 2.15
CRYPT_CC = -1.0
CRYPT_TOP = 3.15
BASE_ANGLES = (200, 235, 270, 305, 340)
CONFETTI = [GREEN, YELLOW, RED, TEAL, GREEN]


def cell(color=BLUE, radius=0.38, opacity=0.68, stroke=3.5):
    return Circle(radius=radius, color=color, stroke_width=stroke,
                  fill_color=color, fill_opacity=opacity)


def base_positions():
    return [np.array([CX + 1.48 * np.cos(a * DEGREES),
                      CRYPT_CC + 1.48 * np.sin(a * DEGREES), 0])
            for a in BASE_ANGLES]


def crypt_shape():
    """Large, high-ink U-shaped pocket, open at the top."""
    back = VGroup(
        Rectangle(width=2 * CRYPT_R, height=CRYPT_TOP - CRYPT_CC,
                  stroke_width=0, fill_color=GREY, fill_opacity=0.20)
        .move_to([CX, (CRYPT_TOP + CRYPT_CC) / 2, 0]),
        Circle(radius=CRYPT_R, stroke_width=0, fill_color=GREY, fill_opacity=0.20)
        .move_to([CX, CRYPT_CC, 0]),
    ).set_z_index(-5)
    walls = VGroup(
        Line([CX - CRYPT_R, CRYPT_TOP, 0], [CX - CRYPT_R, CRYPT_CC, 0],
             color=GREY, stroke_width=6),
        Arc(radius=CRYPT_R, start_angle=PI, angle=PI,
            arc_center=[CX, CRYPT_CC, 0], color=GREY, stroke_width=6),
        Line([CX + CRYPT_R, CRYPT_CC, 0], [CX + CRYPT_R, CRYPT_TOP, 0],
             color=GREY, stroke_width=6),
    )
    return VGroup(back, walls)


def moving_stream(color=GREY, green_patch=False, speed=0.34):
    """A continuously renewing stream; the wrap makes every spoken hold alive."""
    xs = (-1.18, -0.38, 0.40, 1.15, -0.78, 0.05, 0.82)
    ys = (-0.20, 0.35, 0.86, 1.35, 1.82, 2.32, 2.78)
    dots = VGroup()
    for i, (dx, y) in enumerate(zip(xs, ys)):
        c = GREEN if green_patch and i in (1, 3, 5) else color
        d = cell(c, 0.29 if i % 2 else 0.32, 0.48, 2.8).move_to([CX + dx, y, 0])
        d.vy = speed * (0.82 + 0.08 * (i % 4))

        def rise(m, dt):
            m.shift(UP * m.vy * dt)
            if m.get_y() > CRYPT_TOP + 0.42:
                m.move_to([m.get_x(), -0.25, 0])

        d.add_updater(rise)
        dots.add(d)
    return dots


def simplified_label(text="simplified schematic"):
    return T(text, 28, TEXT, weight=BOLD).move_to([3.65, -3.42, 0])


def pool_bracket(label=True):
    y = -3.16
    line = VGroup(
        Line([CX - 1.92, y, 0], [CX + 1.92, y, 0], color=TEAL, stroke_width=6),
        Line([CX - 1.92, y, 0], [CX - 1.92, y + 0.24, 0], color=TEAL, stroke_width=6),
        Line([CX + 1.92, y, 0], [CX + 1.92, y + 0.24, 0], color=TEAL, stroke_width=6),
    )
    if label:
        line.add(T("stem-cell pool", 28, TEAL, weight=BOLD).next_to(line, DOWN, buff=0.08))
    return line


def niche_glow():
    return Ellipse(width=4.05, height=1.65, color=TEAL, stroke_width=3,
                   fill_color=TEAL, fill_opacity=0.12).move_to([CX, -2.25, 0]).set_z_index(-2)


def crypt_world(colors=None, stream_color=GREY, green_patch=False,
                show_simple=True, bracket=False, niche=False):
    colors = colors or [BLUE] * 5
    cr = crypt_shape()
    cells = VGroup(*[cell(c).move_to(p) for c, p in zip(colors, base_positions())])
    flow = moving_stream(stream_color, green_patch)
    items = [cr]
    if niche:
        items.append(niche_glow())
    items.extend([flow, cells])
    if bracket:
        items.append(pool_bracket())
    if show_simple:
        items.append(simplified_label())
    return VGroup(*items), cells, flow


def question_text():
    return T("What happens to green\nafter its descendants\nleave the lining?",
             34, GOLD, weight=BOLD, line_spacing=0.9).move_to([3.35, 1.85, 0])


def time_arrow():
    a = Arrow([1.0, -0.55, 0], [5.75, -0.55, 0], buff=0,
              color=TEXT, stroke_width=5, tip_length=0.22)
    return VGroup(a, T("now", 28).next_to(a.get_start(), DOWN, buff=0.16),
                  T("later", 28).next_to(a.get_end(), DOWN, buff=0.16))


def ghost_patch():
    return VGroup(*[
        cell(GREEN, 0.30, 0.20, 2.2).move_to([CX + dx, y, 0])
        for dx, y in ((-0.65, 0.55), (0.20, 1.05), (-0.32, 1.62), (0.52, 2.18))
    ])


def green_ribbon():
    return RoundedRectangle(width=2.25, height=5.95, corner_radius=0.5,
                            stroke_color=GREEN, stroke_width=3,
                            fill_color=GREEN, fill_opacity=0.20).move_to([CX, 0.03, 0]).set_z_index(-3)


def chance_spinner(center=(3.8, 1.8, 0), size=0.58):
    ring = Circle(radius=size, color=GOLD, stroke_width=4).move_to(center)
    hand = Arrow(ring.get_center(), ring.get_center() + UP * size * 0.72,
                 buff=0, color=GOLD, stroke_width=4, tip_length=0.16)
    g = VGroup(ring, hand, T("chance", 28, GOLD, weight=BOLD).next_to(ring, DOWN, buff=0.18))
    hand.spin_t = 0.0

    def spin(m, dt):
        m.rotate(-0.75 * dt, about_point=ring.get_center())

    hand.add_updater(spin)
    return g


def outcome_strip(colors, y):
    box = RoundedRectangle(width=4.25, height=0.92, corner_radius=0.18,
                           color=GREY, stroke_width=3).move_to([3.65, y, 0])
    dots = VGroup(*[cell(c, 0.23, 0.72, 2.5).move_to([2.18 + i * 0.72, y, 0])
                    for i, c in enumerate(colors)])
    bracket = Line([1.95, y - 0.34, 0], [5.35, y - 0.34, 0], color=TEAL, stroke_width=4)
    return VGroup(box, dots, bracket)


class S01Hook(SpokenScene, TitleCard):
    LESSON = "Stem cells and tissue renewal"
    TITLE = "How a Stem-Cell Pool Persists While Its Clones Come and Go"

    def construct(self):
        world, cells, flow = crypt_world()
        self.play(FadeIn(world[0]), FadeIn(flow), FadeIn(cells),
                  FadeIn(world[-1]), run_time=0.5)
        self.at("replaces its intestinal")
        self.play(flow.animate.set_opacity(0.88), run_time=0.7)
        self.at("How can its")
        q = T("How can the pool last\nwhen clones vanish?", 36, GOLD,
              weight=BOLD, line_spacing=0.9).move_to([3.45, 1.15, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.at("Watch one crypt")
        label = T("intestinal crypt", 30, TEXT, weight=BOLD).move_to([3.45, -0.25, 0])
        arrow = Arrow([2.1, -0.42, 0], [0.0, -0.72, 0], color=TEXT,
                      stroke_width=4, tip_length=0.2)
        self.play(FadeIn(label), GrowArrow(arrow), run_time=0.65)
        self.at("new lining cells")
        self.play(Indicate(flow, color=TEXT, scale_factor=1.03), run_time=0.7)
        self.finish()


class S02Title(TitleCard):
    LESSON = "Stem cells and tissue renewal"
    TITLE = "How a Stem-Cell Pool Persists While Its Clones Come and Go"

    def construct(self):
        world, cells, flow = crypt_world()
        self.add(world)
        title = T("How a Stem-Cell Pool Persists\nWhile Its Clones Come and Go",
                  38, font=TITLE_FONT, weight=BOLD, line_spacing=0.92)
        title.move_to([1.55, 2.35, 0])
        panel = BackgroundRectangle(title, color=BG, fill_opacity=0.88, buff=0.22)
        # Keep every sampled title frame readable; Write() exposes partial glyphs.
        self.play(FadeIn(panel), FadeIn(title), run_time=0.45)
        corner = T("STEM-CELL POOL", 28, TEAL, weight=BOLD).move_to([3.75, 3.28, 0])
        # A text-to-text Transform leaves a briefly unreadable knot of glyphs.
        # Clear the long title before the compact carried label appears.
        self.play(FadeOut(VGroup(panel, title), shift=UP * 0.08), run_time=0.28)
        self.play(FadeIn(corner, shift=UP * 0.08), run_time=0.32)
        self.finish()


class S03Positions(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(niche=True)
        self.add(world[0], flow, world[-1])
        self.at("handful")
        self.play(LaggedStart(*[FadeIn(c, scale=0.75) for c in cells], lag_ratio=0.12),
                  run_time=1.0)
        self.at("The epithelium")
        epi = T("epithelium = intestinal lining", 30, TEXT, weight=BOLD).move_to([3.45, 1.25, 0])
        shapes = VGroup(
            RoundedRectangle(width=0.55, height=0.88, corner_radius=0.12, color=GREY,
                             fill_color=GREY, fill_opacity=0.38),
            Circle(radius=0.35, color=GREY, fill_color=GREY, fill_opacity=0.38),
            Triangle(color=GREY, fill_color=GREY, fill_opacity=0.38).scale(0.38),
        ).arrange(RIGHT, buff=0.42).move_to([3.45, 0.25, 0])
        self.play(FadeIn(epi), FadeIn(shapes, shift=UP * 0.25), run_time=0.75)
        self.play(shapes.animate.shift(UP * 0.35), run_time=0.55)
        self.at("Cells need niche")
        support = T("niche support", 32, TEAL, weight=BOLD).move_to([3.45, -1.45, 0])
        self.play(FadeIn(world[1]), FadeIn(support), run_time=0.65)
        self.at("keep a base")
        self.play(Indicate(cells, color=TEAL, scale_factor=1.04), run_time=0.75)
        self.finish()


class S04Pool(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(bracket=True)
        self.add(world)
        jobs = T("TWO JOBS", 32, TEXT, weight=BOLD).move_to([3.55, 2.72, 0])
        self.play(FadeIn(jobs), run_time=0.45)
        self.at("First")
        output = T("1  make specialized descendants", 30, TEXT, weight=BOLD).move_to([3.55, 1.45, 0])
        up = Arrow([0.35, -0.7, 0], [0.35, 2.15, 0], color=GREY, stroke_width=8, tip_length=0.28)
        self.play(GrowArrow(up), FadeIn(output), flow.animate.set_opacity(1), run_time=0.85)
        self.at("Second")
        maintain = T("2  maintain the pool", 30, TEAL, weight=BOLD).move_to([3.55, 0.35, 0])
        # The carried world already contains the pool bracket.  Reusing it avoids
        # a second bracket sweeping across the base cells during the transition.
        bracket = world[-2]
        self.play(FadeOut(up), FadeIn(maintain),
                  Indicate(bracket, color=TEAL, scale_factor=1.02), run_time=0.8)
        self.at("Neighbors can fill")
        leaving = cells[3]
        gap = leaving.get_center().copy()
        replacement = cells[2].copy()
        self.play(leaving.animate.shift(UP * 1.1).set_opacity(0), run_time=0.65)
        self.play(replacement.animate.move_to(gap), cells[2].animate.shift(RIGHT * 0.14), run_time=0.75)
        self.at("pool may persist")
        result = T("same pool  •  changing cells", 31, TEAL, weight=BOLD).move_to([3.55, -1.45, 0])
        self.play(FadeOut(VGroup(jobs, output, maintain)), FadeIn(result),
                  Indicate(world[-2], color=TEAL, scale_factor=1.02), run_time=0.8)
        self.finish()


class S04PermanentMark(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world()
        self.add(world)
        proof = T("shape or Lgr5 now", 31, TEXT, weight=BOLD).move_to([3.55, 2.35, 0])
        alone = T("cannot prove ancestry", 31, RED, weight=BOLD).next_to(proof, DOWN, buff=0.25)
        self.play(FadeIn(proof), FadeIn(alone), run_time=0.65)
        self.at("Scientists give")
        target = cells[2]
        tag = chip("Lgr5 now", BLUE, 28).move_to([3.55, 1.15, 0])
        pulse = Ellipse(width=0.7, height=5.7, color=YELLOW, stroke_width=0,
                        fill_color=YELLOW, fill_opacity=0.34).move_to([-4.7, -0.2, 0])
        self.play(FadeIn(tag), FadeIn(pulse), run_time=0.35)
        self.play(pulse.animate.shift(RIGHT * 4.7), run_time=0.75)
        self.play(FadeOut(pulse), target.animate.set_color(GREEN).set_fill(GREEN, 0.72), run_time=0.45)
        self.at("Every daughter inherits")
        d1, d2 = target.copy(), target.copy()
        self.play(target.animate.scale(0.78), run_time=0.3)
        self.play(d1.animate.move_to(base_positions()[1]),
                  d2.animate.move_to([CX + 0.35, -0.15, 0]), run_time=0.85)
        self.add(d1, d2)
        self.at("even after it stops")
        family = VGroup(d1, d2)
        self.play(FadeOut(tag, shift=UP * 0.15), d2.animate.shift(UP * 1.15), run_time=0.8)
        self.at("mark follows ancestry")
        brace = Brace(family, RIGHT, color=GREEN)
        ancestry = T("ancestry", 32, GREEN, weight=BOLD).next_to(brace, RIGHT, buff=0.18)
        self.play(FadeOut(VGroup(proof, alone)), GrowFromCenter(brace), FadeIn(ancestry), run_time=0.7)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(colors=[BLUE, GREEN, BLUE, BLUE, BLUE])
        patch = ghost_patch()
        q = question_text()
        timeline = time_arrow()
        self.add(world)
        self.at("only a short lived")
        short = T("short-lived precursor", 31, GREEN, weight=BOLD).move_to([3.4, 2.95, 0])
        self.play(FadeIn(short), FadeIn(patch, shift=UP * 0.2), run_time=0.75)
        self.at("limited output")
        self.play(patch.animate.shift(UP * 0.45).set_opacity(0.48), run_time=0.65)
        self.at("What should happen")
        self.play(FadeOut(short), FadeIn(q), FadeIn(timeline), run_time=0.75)
        self.at("descendants leave")
        self.play(patch.animate.shift(UP * 0.45).set_opacity(0.28), run_time=0.7)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        self.camera.background_color = BG
        world, cells, flow = crypt_world(colors=[BLUE, GREEN, BLUE, BLUE, BLUE])
        patch = ghost_patch().shift(UP * 0.9).set_opacity(0.24)
        self.add(world, patch, question_text(), time_arrow())
        self.wait(4.5)


class S07RibbonReveal(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(colors=[BLUE, GREEN, BLUE, BLUE, BLUE])
        patch = ghost_patch().shift(UP * 1.15).set_opacity(0.35)
        self.add(world, patch)
        self.at("fade away")
        short = T("short-lived", 31, RED, weight=BOLD).move_to([3.45, 2.75, 0])
        self.play(FadeIn(short), patch.animate.shift(UP * 1.0).set_opacity(0), run_time=0.7)
        self.at("Instead")
        ribbon = green_ribbon()
        marker = VGroup(
            Arrow([1.15, 1.75, 0], [5.65, 1.75, 0], buff=0, color=TEXT, stroke_width=5),
            T("0", 28).move_to([1.15, 1.34, 0]),
            T("60 days", 30, GREEN, weight=BOLD).move_to([5.25, 1.30, 0]),
            Dot([1.15, 1.75, 0], radius=0.13, color=GREEN),
        )
        self.play(FadeOut(short), FadeIn(ribbon), FadeIn(marker), run_time=0.65)
        self.at("persisted for 60")
        self.play(marker[-1].animate.move_to([5.65, 1.75, 0]),
                  cells[1].animate.set_color(GREEN).set_fill(GREEN, 0.72), run_time=1.1)
        self.at("contained every epithelial")
        kinds = []
        specs = [
            (RoundedRectangle(width=.48, height=.72, corner_radius=.1), "absorptive", 0.72),
            (Circle(radius=.28), "goblet", -0.05),
            (Triangle().scale(.28), "enteroendocrine", -0.82),
        ]
        for shape, name, y in specs:
            shape.set_color(GREEN).set_fill(GREEN, 0.45).move_to([2.05, y, 0])
            kinds.append(VGroup(shape, T(name, 28, GREEN, weight=BOLD).next_to(shape, RIGHT, buff=.22)))
        kinds = VGroup(*kinds)
        paneth_shape = Square(side_length=.52, color=GREEN, fill_color=GREEN,
                              fill_opacity=.45).move_to(base_positions()[0])
        paneth_label = T("Paneth", 28, GREEN, weight=BOLD).move_to([-5.35, -2.18, 0])
        paneth_arrow = Arrow(paneth_label.get_right(), paneth_shape.get_left(), buff=.12,
                             color=GREEN, stroke_width=4, tip_length=.16)
        paneth = VGroup(paneth_shape, paneth_label, paneth_arrow)
        self.remove(marker)
        self.play(LaggedStart(*[FadeIn(k, shift=RIGHT * .18) for k in kinds],
                              FadeIn(paneth), lag_ratio=.12), run_time=1.0)
        self.at("A lineage is")
        lineage = T("lineage = descendant family", 30, GREEN, weight=BOLD).move_to([3.65, 2.15, 0])
        self.play(FadeIn(lineage), run_time=0.55)
        self.at("multipotent output")
        multi = chip("multipotent output", GREEN, 30).move_to([3.65, -2.65, 0])
        schematic = T("schematic reconstruction", 28, TEXT, weight=BOLD).move_to([3.65, -3.42, 0])
        self.play(FadeOut(lineage), FadeIn(multi), ReplacementTransform(world[-1], schematic), run_time=0.75)
        self.finish()


class S08InferenceLimit(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(colors=[BLUE, GREEN, GREEN, BLUE, BLUE], green_patch=True)
        ribbon = green_ribbon()
        halo = Circle(radius=0.58, color=YELLOW, stroke_width=6).move_to(cells[2])
        start = T("starting cell", 30, YELLOW, weight=BOLD).move_to([3.6, 2.5, 0])
        brace = Brace(cells[2], RIGHT, color=YELLOW)
        self.add(ribbon, world, halo, start, brace)
        self.at("does not mean")
        replacement = cells[1].copy()
        self.play(FadeOut(halo), FadeOut(cells[2], shift=UP * .7),
                  replacement.animate.move_to(cells[2]), run_time=0.8)
        self.add(replacement)
        self.at("trace identifies")
        pop_brace = Brace(VGroup(ribbon, cells), RIGHT, color=GREEN)
        pop = T("population tested\nover time", 31, GREEN, weight=BOLD,
                line_spacing=.9).move_to([4.05, 1.25, 0])
        self.play(ReplacementTransform(brace, pop_brace), ReplacementTransform(start, pop), run_time=0.8)
        self.at("descendant output")
        self.play(flow.animate.set_color(GREEN).set_opacity(0.75), run_time=0.7)
        self.at("not a marker alone")
        card = chip("marker alone", TEXT, 30).move_to([3.9, -1.35, 0])
        x = VGroup(Line(card.get_corner(UL), card.get_corner(DR), color=RED, stroke_width=7),
                   Line(card.get_corner(DL), card.get_corner(UR), color=RED, stroke_width=7))
        self.play(FadeIn(card), Create(x), run_time=0.7)
        self.at("supplies the evidence")
        evidence = T("descendants over time", 31, GREEN, weight=BOLD).move_to([3.9, -2.55, 0])
        self.play(FadeIn(evidence), Indicate(flow, color=GREEN, scale_factor=1.03), run_time=0.7)
        self.finish()


class S09Confetti(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world()
        self.add(world)
        self.at("permanent confetti")
        new_cells = VGroup(*[cell(c).move_to(p) for c, p in zip(CONFETTI, base_positions())])
        self.play(ReplacementTransform(cells, new_cells), run_time=0.8)
        cells = new_cells
        self.at("green")
        legend = VGroup(*[VGroup(cell(c, .18), T(n, 28, c, weight=BOLD)).arrange(RIGHT, buff=.16)
                          for c, n in ((GREEN, "green"), (YELLOW, "yellow"),
                                       (RED, "red"), (TEAL, "cyan"))])
        legend.arrange(DOWN, aligned_edge=LEFT, buff=.22).move_to([3.6, 1.65, 0])
        self.play(LaggedStart(*[FadeIn(x) for x in legend], lag_ratio=.15), run_time=1.1)
        self.at("divide about once")
        clock = VGroup(Circle(radius=.58, color=TEXT, stroke_width=4),
                       Line(ORIGIN, UP*.37, color=TEXT, stroke_width=4),
                       Line(ORIGIN, RIGHT*.25, color=TEXT, stroke_width=4)).move_to([3.65, -.55, 0])
        daily = T("about once daily", 30, TEXT, weight=BOLD).next_to(clock, DOWN, buff=.18)
        self.play(FadeOut(legend), FadeIn(clock), FadeIn(daily), run_time=.55)
        self.play(Rotate(clock[1], -TAU, about_point=clock[0].get_center()), run_time=.75)
        self.at("Most divisions")
        parent = cells[0]
        twins = VGroup(parent.copy().scale(.78), parent.copy().scale(.78))
        twins.arrange(RIGHT, buff=.1).move_to(parent)
        symmetric = T("symmetric", 32, GREEN, weight=BOLD).move_to([3.65, 1.15, 0])
        self.play(ReplacementTransform(parent, twins), FadeIn(symmetric), run_time=.75)
        self.at("both daughters retain")
        self.play(twins.animate.arrange(RIGHT, buff=.35).move_to([CX - 1.0, -2.05, 0]), run_time=.7)
        self.at("or both leave")
        exiting = cells[2].copy()
        two_out = VGroup(exiting.copy(), exiting.copy()).arrange(RIGHT, buff=.18).move_to(cells[2])
        gap = cells[2].get_center().copy()
        neighbour = cells[3].copy()
        self.play(ReplacementTransform(cells[2], two_out), run_time=.35)
        self.play(two_out.animate.shift(UP * 1.35).set_opacity(0),
                  neighbour.animate.move_to(gap), FadeOut(VGroup(clock, daily, symmetric)), run_time=.8)
        self.finish()


class S10Exchange(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(colors=CONFETTI, bracket=True)
        spinner = chance_spinner()
        self.add(world)
        self.at("appear to compete")
        self.play(FadeIn(spinner), Indicate(cells, color=GOLD, scale_factor=1.04), run_time=.75)
        self.at("Green expands")
        gap = cells[2].get_center().copy()
        green_copy = cells[1].copy()
        self.play(cells[2].animate.shift(UP * 1.0).set_opacity(0), run_time=.55)
        self.play(green_copy.animate.move_to(gap), run_time=.65)
        self.add(green_copy)
        self.at("Red disappears")
        gone = T("red disappears", 30, RED, weight=BOLD).move_to([3.75, -.05, 0])
        self.play(FadeIn(gone), run_time=.5)
        self.at("cyan pushes")
        cyan_copy = cells[3].copy()
        green_target = cells[4]
        self.play(green_target.animate.shift(UP * .9).set_opacity(0),
                  cyan_copy.animate.move_to(green_target), FadeOut(gone), run_time=.75)
        self.add(cyan_copy)
        self.at("Color shares change")
        changing = T("colour shares change", 31, GOLD, weight=BOLD).move_to([3.75, -.1, 0])
        constrained = T("pool stays constrained", 31, TEAL, weight=BOLD).move_to([3.75, -1.15, 0])
        self.play(FadeIn(changing), FadeIn(constrained), run_time=.7)
        self.at("pool stays constrained")
        self.play(Indicate(world[-2], color=TEAL, scale_factor=1.02), run_time=.7)
        self.finish()


class S10Winner(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(colors=CONFETTI, bracket=True)
        spinner = chance_spinner((3.65, 2.55, 0), .48)
        self.add(world, spinner)
        yellow = cells[1]
        self.at("erase most colors")
        for i in (2, 0):
            repl = yellow.copy()
            self.play(FadeOut(cells[i], shift=UP*.65), repl.animate.move_to(cells[i]), run_time=.48)
            self.add(repl)
        self.at("one clone fills")
        targets = [c for i, c in enumerate(cells) if i not in (0, 1, 2)]
        new = [yellow.copy() for _ in targets]
        self.play(*[FadeOut(c, shift=UP*.55) for c in targets], run_time=.4)
        self.play(*[n.animate.move_to(t) for n, t in zip(new, targets)], run_time=.65)
        self.add(*new)
        self.at("Different repeats")
        strips = VGroup(outcome_strip([GREEN]*5, .65),
                        outcome_strip([RED]*5, -.55),
                        outcome_strip([TEAL]*5, -1.75))
        self.play(FadeOut(simplified_label()), FadeIn(strips, shift=RIGHT*.18), run_time=.9)
        self.at("different winners")
        self.play(LaggedStart(*[Indicate(s[1], scale_factor=1.05) for s in strips], lag_ratio=.15), run_time=.9)
        self.at("takeover by one")
        result = T("one-clone takeover", 32, YELLOW, weight=BOLD).move_to([3.65, -2.85, 0])
        self.play(FadeOut(strips), FadeIn(result), run_time=.65)
        self.at("not survival")
        lost = T("most starting clones vanish", 30, RED, weight=BOLD).move_to([3.65, -1.45, 0])
        self.play(FadeIn(lost), run_time=.65)
        self.finish()


class S11PopulationBalance(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(colors=[YELLOW]*5, bracket=True)
        strips = VGroup(outcome_strip([GREEN, GREEN, RED, GREEN, TEAL], 1.35),
                        outcome_strip([RED, YELLOW, YELLOW, TEAL, YELLOW], .15),
                        outcome_strip([TEAL, GREEN, TEAL, TEAL, RED], -1.05))
        self.add(world)
        self.at("clone identities change")
        self.play(FadeIn(strips, shift=RIGHT*.18), run_time=.85)
        # Shares change, but each teal baseline (the supported pool) is identical.
        finals = VGroup(outcome_strip([GREEN]*5, 1.35),
                        outcome_strip([YELLOW]*5, .15),
                        outcome_strip([TEAL]*5, -1.05))
        self.play(Transform(strips, finals), run_time=1.0)
        self.at("Balance belongs")
        balance = T("balance = population property", 31, TEAL, weight=BOLD).move_to([3.7, 2.55, 0])
        self.play(FadeIn(balance), run_time=.6)
        self.at("not every division")
        division = chip("every division", TEXT, 28).move_to([3.7, -2.15, 0])
        slash = Line(division.get_corner(UL), division.get_corner(DR), color=RED, stroke_width=7)
        self.play(FadeIn(division), Create(slash), run_time=.65)
        self.at("No cell is appointed")
        crown = T("no appointed winner", 30, GOLD, weight=BOLD).move_to([3.7, -2.95, 0])
        self.play(FadeOut(VGroup(division, slash)), FadeIn(crown), run_time=.6)
        self.at("neutral drift")
        neutral = chip("neutral drift", GOLD, 34).move_to([3.7, .05, 0])
        self.play(FadeOut(VGroup(strips, balance, crown)), run_time=.28)
        self.play(FadeIn(neutral), run_time=.42)
        self.at("chance competition")
        spinner = chance_spinner((3.7, -1.45, 0), .48)
        self.play(FadeIn(spinner), Indicate(neutral, color=GOLD, scale_factor=1.04), run_time=.75)
        self.finish()


class S12Takeaway(SpokenScene):
    def construct(self):
        world, cells, flow = crypt_world(colors=CONFETTI, bracket=True)
        self.add(world)
        self.at("follow descendants")
        follow = T("FOLLOW DESCENDANTS\nOVER TIME", 31, GREEN, weight=BOLD,
                   line_spacing=.9).move_to([3.55, 2.35, 0])
        self.play(FadeIn(follow), flow.animate.set_opacity(.9), run_time=.7)
        self.at("pool can make specialized")
        output = T("specialized output", 30, TEXT, weight=BOLD).move_to([3.55, 1.35, 0])
        self.play(FadeIn(output), Indicate(flow, color=TEXT, scale_factor=1.03), run_time=.75)
        self.at("most clones vanish")
        winner = cells[1]
        for i in (2, 3, 0):
            repl = winner.copy()
            self.play(FadeOut(cells[i], shift=UP*.55), repl.animate.move_to(cells[i]), run_time=.42)
            self.add(repl)
        self.at("one may take over")
        last = winner.copy()
        self.play(FadeOut(cells[4], shift=UP*.55), last.animate.move_to(cells[4]), run_time=.6)
        self.add(last)
        self.at("population persists")
        pop = T("POPULATION PERSISTS", 34, TEAL, weight=BOLD).move_to([3.55, .1, 0])
        self.remove(follow, output)
        self.play(FadeIn(pop), Indicate(world[-2], color=TEAL, scale_factor=1.02),
                  run_time=.55)
        self.at("membership changes")
        membership = T("membership changes", 32, YELLOW, weight=BOLD).move_to([3.55, -1.0, 0])
        self.play(FadeIn(membership), run_time=.65)
        self.at("stable stem cell pool")
        rule = T("A stable stem-cell pool\npersists while most of its\nclones vanish.",
                 32, TEXT, font=TITLE_FONT, weight=BOLD, line_spacing=.86).move_to([3.35, -2.05, 0])
        self.remove(pop, membership, world[-1])
        self.play(FadeIn(rule), run_time=.55)
        self.finish()


class S13End(EndCard):
    LINE = "A stable stem-cell pool persists while most of its clones vanish."

    def construct(self):
        world, cells, flow = crypt_world(colors=[YELLOW]*5, bracket=True, show_simple=False)
        self.add(world)
        line = T("A stable stem-cell pool persists\nwhile most of its clones vanish.",
                 42, TEXT, font=TITLE_FONT, weight=BOLD, line_spacing=.9).move_to([2.2, .55, 0])
        panel = BackgroundRectangle(line, color=BG, fill_opacity=.88, buff=.3)
        sub = T("biochemistrypedia.com", 28, TEAL, weight=BOLD).move_to([3.3, -1.25, 0])
        self.play(FadeIn(panel), FadeIn(line, shift=UP*.12), FadeIn(sub), run_time=.75)
        # A breathing bracket plus the continuing stream keeps the final world alive.
        bracket = world[-1]
        self.play(bracket.animate.set_opacity(.55), rate_func=there_and_back, run_time=.8)
        self.finish()
