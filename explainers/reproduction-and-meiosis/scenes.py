"""Copies, Halves, and Pairs.

COLOR MAP
  BLUE   first member of every chromosome pair
  GOLD   second member of every chromosome pair
  GREEN  sex cells and the strawberry runner
  WHITE  fertilized cell and restored pairs
  RED    the doubling problem / the incorrect cutting idea
  GREY   soil, cell outlines, and neutral structure
"""
from bp_parts import *  # noqa: F401,F403


LONG, SHORT, BAR_W = 2.05, 1.35, 0.32
QUESTION = "Keep every pair together, or carry only half?"
OPTIONS = ["pairs stay together", "one from each pair"]


def cell_outline(center=ORIGIN, width=5.2, height=4.5, color=GREY, fill=0.20):
    return Ellipse(width=width, height=height, color=color, stroke_width=5,
                   fill_color=color, fill_opacity=fill).move_to(center)


def chromosome(height, color, center=ORIGIN, width=BAR_W):
    return RoundedRectangle(corner_radius=width / 2, width=width, height=height,
                            stroke_width=0, fill_color=color, fill_opacity=1).move_to(center)


def pair_bars(center=ORIGIN, scale=1.0, gap=0.62):
    """One long and one short chromosome pair, always at the same relative positions."""
    x, y, _ = center
    bars = VGroup(
        chromosome(LONG * scale, BLUE, [x - 1.15 * gap, y + 0.22, 0], BAR_W * scale),
        chromosome(LONG * scale, GOLD, [x - 0.15 * gap, y + 0.22, 0], BAR_W * scale),
        chromosome(SHORT * scale, BLUE, [x + 0.75 * gap, y - 0.13, 0], BAR_W * scale),
        chromosome(SHORT * scale, GOLD, [x + 1.75 * gap, y - 0.13, 0], BAR_W * scale),
    )
    return bars


def body_cell(center=ORIGIN, width=6.0, height=5.0, scale=1.0):
    outline = cell_outline(center, width, height)
    bars = pair_bars(center, scale=scale, gap=0.8 * scale)
    return VGroup(outline, bars)


def half_cell(center, colors=(BLUE, GOLD), label=None, width=3.35, height=3.25):
    x, y, _ = center
    outline = cell_outline(center, width, height, GREEN, 0.20)
    bars = VGroup(
        chromosome(LONG * 0.78, colors[0], [x - 0.45, y + 0.08, 0], BAR_W * 0.82),
        chromosome(SHORT * 0.78, colors[1], [x + 0.45, y - 0.08, 0], BAR_W * 0.82),
    )
    g = VGroup(outline, bars)
    if label:
        lab = T(label, 28, GREEN).next_to(outline, UP, buff=0.18)
        g.add(lab)
    return g


def fertilized_cell(center=ORIGIN, width=5.0, height=4.2):
    return VGroup(cell_outline(center, width, height, TEXT, 0.20), pair_bars(center, scale=0.88, gap=0.72))


def plant(x, y=-0.55, scale=1.0, changed=False):
    """The carried strawberry plant: leaves, crown, roots, and optional rare spot."""
    stem = Line([x, y - 0.5 * scale, 0], [x, y + 0.55 * scale, 0], color=GREEN,
                stroke_width=10 * scale)
    leaves = VGroup()
    for dx, dy, ang in [(-0.62, 0.40, -0.45), (0.62, 0.40, 0.45),
                        (-0.48, 0.85, -0.25), (0.48, 0.85, 0.25), (0, 1.05, 0)]:
        leaf = Ellipse(width=0.95 * scale, height=0.45 * scale, color=GREEN,
                       fill_color=GREEN, fill_opacity=0.85, stroke_width=2)
        leaf.rotate(ang).move_to([x + dx * scale, y + dy * scale, 0])
        leaves.add(leaf)
    crown = Dot([x, y - 0.42 * scale, 0], radius=0.18 * scale, color=GREEN)
    roots = VGroup(*[
        Line([x, y - 0.48 * scale, 0], [x + dx * scale, y - 1.08 * scale, 0],
             color=GOLD, stroke_width=4) for dx in (-0.58, 0, 0.58)
    ])
    g = VGroup(stem, leaves, crown, roots)
    g.leaves = leaves
    if changed:
        g.add(Dot(leaves[3].get_center(), radius=0.09 * scale, color=RED))
    return g


def garden(show_runner=True, rooted=True, question=False, changed=False):
    """The one garden world, rebuilt identically in s00, s01, s08, and s09."""
    ground = Rectangle(width=12.8, height=2.15, stroke_width=0, fill_color=GOLD,
                       fill_opacity=0.18).move_to([0, -2.77, 0])
    soil = Line([-6.4, -1.72, 0], [6.4, -1.72, 0], color=GOLD, stroke_width=7)
    parent = plant(-4.25, scale=1.2)
    child = plant(1.2, scale=1.2, changed=changed)
    child.set_opacity(1 if rooted else 0)
    runner = CubicBezier([-4.0, -1.15, 0], [-2.4, -0.72, 0], [-0.2, -1.52, 0], [1.0, -1.12, 0])
    runner.set_stroke(GREEN, width=10)
    if not show_runner:
        runner.set_opacity(0)
    sky = VGroup(*[Dot([x, 2.6 + 0.18 * np.sin(x), 0], radius=0.055, color=GREY).set_opacity(0.4)
                   for x in np.linspace(-6, 6, 18)])
    g = VGroup(ground, sky, soil, parent, runner, child)
    g.parent, g.runner, g.child = parent, runner, child
    if question:
        q = fit_text("Copy or different?", max_w=5.0, size=44, color=TEXT).move_to([3.7, 2.25, 0])
        g.add(q)
        g.question = q
    return g


def sway(mob, amp=0.055, speed=1.4, phase=0.0):
    """Gentle continuous motion around a fixed base; no cumulative drift."""
    base = mob.get_center().copy()
    mob._sway_t = phase

    def update(m, dt):
        m._sway_t += dt
        m.move_to(base + UP * amp * np.sin(speed * m._sway_t))
    mob.add_updater(update)
    return mob


def breathe_fill(mob, base=0.20, amp=0.10, speed=5.0, color=GREY):
    """Animate a large cell interior enough to remain alive during a long explanation."""
    mob._breath_t = 0.0

    def update(m, dt):
        m._breath_t += dt
        m.set_fill(color, opacity=base + amp * np.sin(speed * m._breath_t))
    mob.add_updater(update)
    return mob


def moving_garden(g):
    sway(g.parent.leaves, 0.16, 1.3)
    sway(g.child.leaves, 0.16, 1.5, 1.2)
    return g


def choice_backdrop():
    c = body_cell([0, 0.35, 0], width=5.3, height=4.25, scale=0.82)
    top = VGroup(*[b.copy() for b in c[1]]).scale(0.62).move_to([-3.75, 1.5, 0])
    together = Arrow([-3.75, 0.78, 0], [-3.75, -0.25, 0], color=GREY, stroke_width=5)
    split = VGroup(c[1][0].copy(), c[1][3].copy()).scale(0.62).move_to([3.75, 1.5, 0])
    apart = VGroup(Arrow([3.55, 0.78, 0], [3.0, -0.25, 0], color=GREY, stroke_width=5),
                   Arrow([3.95, 0.78, 0], [4.5, -0.25, 0], color=GREY, stroke_width=5))
    return VGroup(c, top, together, split, apart)


class S00Question(SpokenScene):
    def construct(self):
        g = garden(show_runner=False, rooted=False, question=True)
        g.child.set_opacity(0)
        moving_garden(g)
        self.play(FadeIn(g.parent), FadeIn(g[0]), Create(g[2]), FadeIn(g.question), run_time=1.25)
        self.at("Watch one garden")
        self.play(FadeIn(g[1]), run_time=0.8)
        self.at("A runner stretches")
        g.runner.set_opacity(1)
        self.play(Create(g.runner), run_time=2.0, rate_func=linear)
        self.at("roots nearby")
        g.child.set_opacity(1)
        self.play(FadeIn(g.child[3]), FadeIn(g.child[:3]), run_time=1.25)
        self.at("one parent")
        one = T("one parent", 32, GREEN).move_to([-1.55, -2.55, 0])
        ar = Arrow([-3.45, -1.95, 0], [0.35, -1.95, 0], color=GREEN, stroke_width=5)
        self.play(GrowArrow(ar), FadeIn(one), run_time=1.0)
        self.at("asexual reproduction")
        name = T("asexual reproduction", 34, GREEN, weight=BOLD).move_to([0, 3.1, 0])
        self.play(swap(g.question, name), run_time=1.0)
        self.at("same genetic information")
        same = caption("The new plant usually carries the same genetic information.", color=GREEN)
        self.play(FadeIn(same), Indicate(VGroup(g.parent, g.child), color=GREEN), run_time=1.3)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Reproduction and meiosis"
    TITLE = "Copies, Halves, and Pairs"

    def construct(self):
        g = garden(show_runner=True, rooted=True)
        moving_garden(g)
        # Deliberate moving picture behind the translucent title overlay.
        g.layout_ok = True
        veil = Rectangle(width=14.2, height=8, fill_color=BG, fill_opacity=0.66, stroke_width=0)
        title = T(self.TITLE, 52, TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON.upper(), 24, TEAL)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.28)
        self.add(g)
        self.play(FadeIn(veil), FadeIn(card, shift=UP * 0.15), run_time=0.65)
        self.play(FadeOut(VGroup(veil, card)), run_time=0.65)
        self.finish()


class S02TwoPaths(SpokenScene):
    def construct(self):
        left = body_cell([-3.7, 0.15, 0], width=4.8, height=4.5, scale=0.72)
        right = body_cell([3.7, 0.15, 0], width=4.8, height=4.5, scale=0.72)
        pulse(left[0], base=5.0, amp=0.7, speed=1.3)
        pulse(right[0], base=5.0, amp=0.7, speed=1.5)
        self.play(FadeIn(left), FadeIn(right), run_time=1.2)
        self.at("Two sex cells join")
        target = Dot([0, 0.15, 0], radius=0.17, color=TEXT)
        self.play(left.animate.shift(RIGHT * 1.0), right.animate.shift(LEFT * 1.0), FadeIn(target), run_time=1.5)
        sway(left[1], 0.13, 1.25)
        sway(right[1], 0.13, 1.45, 0.9)
        self.at("one from each")
        p1 = T("parent 1", 28, BLUE).move_to([-3.7, 3.15, 0])
        p2 = T("parent 2", 28, GOLD).move_to([3.7, 3.15, 0])
        self.play(FadeIn(p1), FadeIn(p2), run_time=0.8)
        self.at("sperm and egg")
        self.play(swap(p1, T("sperm", 30, GREEN).move_to(p1)),
                  swap(p2, T("egg", 30, GREEN).move_to(p2)), run_time=0.9)
        self.at("a problem must be solved")
        stop = T("?", 72, RED, weight=BOLD).move_to([0, 2.65, 0])
        self.play(FadeIn(stop, scale=0.5), run_time=0.8)
        self.at("chromosomes in pairs")
        self.play(Indicate(left[1], color=TEXT), Indicate(right[1], color=TEXT), run_time=1.3)
        self.at("would double")
        doubled = VGroup(M("4 + 4", 42, RED), T("would double", 32, RED)).arrange(DOWN, buff=0.14).move_to([0, -2.75, 0])
        self.play(FadeIn(doubled), Indicate(VGroup(left[1], right[1]), color=RED), run_time=1.3)
        self.finish()


class S03Pairs(SpokenScene):
    def construct(self):
        c = body_cell([-1.2, 0.1, 0], width=8.1, height=5.8, scale=1.05)
        bars = c[1]
        breathe_fill(c[0])
        self.play(FadeIn(c[0]), LaggedStart(*[FadeIn(b, scale=0.5) for b in bars], lag_ratio=0.15), run_time=1.4)
        # The entrance animation adds the bars individually, so each visible bar owns its motion.
        for i, bar in enumerate(bars):
            sway(bar, 0.11, 1.25, i * 0.18)
        self.at("Each color marks")
        blue = T("blue member", 29, BLUE).move_to([-4.9, 2.65, 0])
        gold = T("gold member", 29, GOLD).move_to([2.55, 2.65, 0])
        self.play(FadeIn(blue), FadeIn(gold), Indicate(VGroup(bars[0], bars[2]), color=BLUE),
                  Indicate(VGroup(bars[1], bars[3]), color=GOLD), run_time=1.2)
        self.at("same kinds of genes")
        ticks = VGroup()
        for i, b in enumerate(bars):
            for frac in ((0.22, 0.68) if i < 2 else (0.32, 0.7)):
                y = b.get_bottom()[1] + frac * b.height
                ticks.add(Line([b.get_x() - 0.23, y, 0], [b.get_x() + 0.23, y, 0], color=TEXT, stroke_width=5))
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.08), run_time=1.5)
        self.at("came from the mother")
        mother = T("from mother", 28, BLUE).move_to([-4.85, -2.45, 0])
        father = T("from father", 28, GOLD).move_to([2.55, -2.45, 0])
        self.play(FadeIn(mother), Indicate(VGroup(bars[0], bars[2]), color=BLUE), run_time=0.9)
        self.at("one from the father")
        self.play(FadeIn(father), Indicate(VGroup(bars[1], bars[3]), color=GOLD), run_time=0.9)
        self.at("body cell keeps")
        panel = VGroup(T("human example", 26, GREY), M("46", 52, TEXT), T("23 pairs", 30, TEXT)).arrange(DOWN, buff=0.12).move_to([5.15, 0, 0])
        self.play(FadeIn(panel), run_time=1.0)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        back = choice_backdrop()
        back[1:].set_opacity(0)
        sway(back[0][1], 0.13, 1.3)
        self.add(back[0])
        self.at("Watch the bars")
        back[1:].set_opacity(1)
        self.play(FadeIn(back[1:]), run_time=1.2)
        self.at("Should every pair")
        stay = T("stay together", 28, BLUE).move_to([-3.75, -0.75, 0])
        half = T("carry half", 28, GOLD).move_to([3.75, -0.75, 0])
        self.play(FadeIn(stay), FadeIn(half), run_time=1.0)
        self.at("Make your prediction")
        q = question_card(QUESTION, OPTIONS, y=-3.15)
        self.play(FadeIn(q), run_time=0.8)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = QUESTION
    OPTIONS = OPTIONS
    CHIPS_AT = None
    CARD = {"y": -3.15}
    SECONDS = 4.5

    def backdrop(self):
        back = choice_backdrop()
        pulse(back[2], base=4.5, amp=1.2, speed=2.0)
        pulse(back[4][0], base=4.5, amp=1.2, speed=1.8)
        return back


class S06Meiosis(SpokenScene):
    def construct(self):
        parent = body_cell([0, 0.55, 0], width=6.0, height=4.8, scale=0.9)
        self.add(parent)
        self.play(Indicate(parent[1], color=TEXT), run_time=1.0)
        self.at("members of each pair separate")
        left = half_cell([-4.05, 0.25, 0], (BLUE, GOLD), "sex cell")
        right = half_cell([4.05, 0.25, 0], (GOLD, BLUE), "sex cell")
        targets = [left[1][0], right[1][0], right[1][1], left[1][1]]
        self.play(FadeOut(parent[0]), FadeIn(left[0]), FadeIn(right[0]),
                  *[ReplacementTransform(b, t) for b, t in zip(parent[1], targets)], run_time=2.1)
        self.play(FadeIn(left[2]), FadeIn(right[2]), run_time=0.6)
        sway(left[1], 0.13, 1.25)
        sway(right[1], 0.13, 1.45, 0.8)
        self.at("one chromosome from every pair")
        self.play(Indicate(left[1], color=TEXT), Indicate(right[1], color=TEXT), run_time=1.3)
        self.at("number is half")
        n = ValueTracker(46)
        count = counter("human example: {:.0f}", n, at=[0, 2.95, 0], size=34, color=TEXT)
        self.add(count)
        self.play(n.animate.set_value(23), run_time=1.7)
        self.at("Here is the rule")
        rule = caption("Meiosis halves chromosome number; fertilization restores pairs.", size=30, color=TEXT)
        self.play(FadeIn(rule), run_time=0.9)
        self.at("makes mixes")
        self.play(Indicate(VGroup(left[1], right[1]), color=GREEN), run_time=1.0)
        self.at("Fertilization restores")
        self.play(Indicate(VGroup(left, right), color=TEXT), run_time=1.0)
        self.finish()


class S07Fertilization(SpokenScene):
    def construct(self):
        sperm = half_cell([-4.35, 0.35, 0], (BLUE, GOLD), "sperm")
        egg = half_cell([4.35, 0.35, 0], (GOLD, BLUE), "egg")
        pulse(sperm[0], base=5.0, amp=0.7, speed=1.3)
        pulse(egg[0], base=5.0, amp=0.7, speed=1.5)
        self.play(FadeIn(sperm), FadeIn(egg), run_time=1.0)
        self.play(sperm.animate.shift(RIGHT * 0.55), egg.animate.shift(LEFT * 0.55), run_time=0.8)
        self.at("Fertilization joins")
        zygote = fertilized_cell([0, 0.25, 0])
        self.play(FadeOut(VGroup(sperm[0], sperm[2], egg[0], egg[2])), FadeIn(zygote[0]),
                  ReplacementTransform(sperm[1][0], zygote[1][0]),
                  ReplacementTransform(egg[1][0], zygote[1][1]),
                  ReplacementTransform(egg[1][1], zygote[1][2]),
                  ReplacementTransform(sperm[1][1], zygote[1][3]), run_time=2.2)
        sway(zygote[1], 0.13, 1.3)
        self.at("full pairs again")
        braces = VGroup(Brace(VGroup(zygote[1][0], zygote[1][1]), DOWN, color=TEXT),
                        Brace(VGroup(zygote[1][2], zygote[1][3]), DOWN, color=TEXT))
        self.play(GrowFromCenter(braces[0]), GrowFromCenter(braces[1]), run_time=1.1)
        self.at("one chromosome from each parent")
        self.play(Indicate(VGroup(zygote[1][0], zygote[1][2]), color=BLUE),
                  Indicate(VGroup(zygote[1][1], zygote[1][3]), color=GOLD), run_time=1.3)
        self.at("chromosome number returns")
        eq = M("23 + 23 = 46", 46, TEXT, weight=BOLD).move_to([0, 3.1, 0])
        self.play(FadeIn(eq), run_time=1.0)
        self.at("instead of growing")
        stable = caption("The body-cell number is restored each generation.", color=TEXT)
        self.play(FadeIn(stable), Indicate(eq, color=GREEN), run_time=1.2)
        self.finish()


class S07bWholeChromosomes(SpokenScene):
    def construct(self):
        bars = VGroup(chromosome(3.55, BLUE, [-0.55, 0.25, 0], 0.5),
                      chromosome(3.55, GOLD, [0.55, 0.25, 0], 0.5))
        sway(bars, 0.13, 1.25)
        count = VGroup(M("2", 50, TEXT), T("whole chromosomes", 32, TEXT)).arrange(RIGHT, buff=0.25).move_to([0, 3.2, 0])
        self.play(FadeIn(bars), FadeIn(count), run_time=1.0)
        self.at("does not mean cutting")
        scissors = T("✂", 64, RED).move_to([3.4, 0.45, 0])
        not_cut = T("not cut", 32, RED, weight=BOLD).move_to([3.4, -0.65, 0])
        self.play(FadeIn(scissors), FadeIn(not_cut), run_time=0.8)
        self.play(scissors.animate.shift(RIGHT * 2.2).set_opacity(0), run_time=0.9)
        self.at("one whole chromosome")
        left = cell_outline([-3.55, 0.1, 0], 3.0, 4.05, GREEN, 0.20)
        right = cell_outline([3.55, 0.1, 0], 3.0, 4.05, GREEN, 0.20)
        self.play(FadeIn(left), FadeIn(right), bars[0].animate.move_to(left), bars[1].animate.move_to(right),
                  FadeOut(not_cut), run_time=1.8)
        self.at("When the cells join")
        white = cell_outline([0, 0.1, 0], 5.1, 4.65, TEXT, 0.20)
        self.play(FadeOut(VGroup(left, right)), FadeIn(white), bars[0].animate.move_to([-0.45, 0.1, 0]),
                  bars[1].animate.move_to([0.45, 0.1, 0]), run_time=1.8)
        self.at("form pairs again")
        brace = Brace(bars, DOWN, color=TEXT)
        self.play(GrowFromCenter(brace), run_time=0.8)
        self.at("repeat across generations")
        ring = Arc(radius=2.85, start_angle=0.2, angle=TAU * 0.88, color=GREEN, stroke_width=6)
        tip = ArrowTriangleFilledTip(color=GREEN).scale(0.18).move_to(ring.get_end()).rotate(-0.7)
        self.play(Create(ring), FadeIn(tip), run_time=2.0)
        self.finish()


class S08Refine(SpokenScene):
    def construct(self):
        animal = fertilized_cell([0, 0.1, 0], 4.7, 4.0)
        pulse(animal[0], base=5.0, amp=0.7, speed=1.2)
        self.play(FadeIn(animal), run_time=1.0)
        self.at("Plants take an extra step")
        self.play(animal.animate.scale(0.58).move_to([-4.6, 0.45, 0]), run_time=1.1)
        flower = plant(-4.6, -0.25, 0.72)
        spores = VGroup(*[Dot([x, 1.2 + 0.2 * np.sin(x * 3), 0], radius=0.12, color=GOLD)
                          for x in (-1.4, -0.7, 0, 0.7, 1.4)])
        self.play(ReplacementTransform(animal, flower), run_time=1.0)
        self.at("Meiosis first makes spores")
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in spores], lag_ratio=0.12), run_time=1.2)
        self.at("sex cells form later")
        sex = VGroup(half_cell([-1.15, -0.45, 0], (BLUE, GOLD), width=2.2, height=2.15),
                     half_cell([1.15, -0.45, 0], (GOLD, BLUE), width=2.2, height=2.15))
        sex.scale(0.65)
        self.play(ReplacementTransform(spores, sex), run_time=1.3)
        self.at("still carry half")
        half = T("half", 34, GREEN).move_to([0, -2.15, 0])
        self.play(FadeIn(half), Indicate(sex, color=GREEN), run_time=1.0)
        self.at("simple model also has an exception")
        self.play(FadeOut(VGroup(flower, sex, half)), run_time=0.8)
        g = garden(show_runner=True, rooted=True, changed=True)
        moving_garden(g)
        self.play(FadeIn(g), run_time=1.1)
        self.at("Rare DNA changes")
        rare = T("rare DNA change", 29, RED).move_to([3.9, 2.05, 0])
        arrow = Arrow([3.2, 1.72, 0], [1.7, 0.75, 0], color=RED, stroke_width=4)
        self.play(FadeIn(rare), GrowArrow(arrow), run_time=1.0)
        self.finish()


class S09Answer(SpokenScene):
    def construct(self):
        g = garden(show_runner=True, rooted=True)
        g.scale(0.78).shift(LEFT * 1.45 + UP * 0.15)
        moving_garden(g)
        self.play(FadeIn(g), run_time=1.0)
        self.at("runner grows from one parent")
        self.play(Indicate(VGroup(g.parent, g.runner, g.child), color=GREEN), run_time=1.3)
        self.at("parent's genetic information")
        same = T("usually a copy", 32, GREEN).move_to([-2.4, -2.55, 0])
        self.play(FadeIn(same), run_time=0.9)
        self.at("Sexual offspring begin")
        left = half_cell([3.35, 0.7, 0], (BLUE, GOLD), width=2.4, height=2.3)
        right = half_cell([5.45, 0.7, 0], (GOLD, BLUE), width=2.4, height=2.3)
        left.scale(0.78); right.scale(0.78)
        self.play(FadeIn(left), FadeIn(right), run_time=0.9)
        self.at("half sets join")
        joined = fertilized_cell([4.4, 0.45, 0], 3.5, 3.0)
        joined.scale(0.8)
        self.play(ReplacementTransform(VGroup(left, right), joined), run_time=1.4)
        self.at("prevents chromosome number")
        halves = T("meiosis: half", 29, GREEN).move_to([4.4, 2.5, 0])
        self.play(FadeIn(halves), run_time=0.8)
        self.at("Fertilization restores")
        restored = T("fertilization: pairs", 29, TEXT).move_to([4.4, -1.75, 0])
        self.play(FadeIn(restored), Indicate(joined[1], color=TEXT), run_time=1.0)
        self.at("next question")
        variants = VGroup(pair_bars([3.5, -2.7, 0], 0.35, 0.42), pair_bars([5.2, -2.7, 0], 0.35, 0.42)).set_opacity(0.35)
        q = T("Why aren't half sets all alike?", 30, GOLD).move_to([3.95, 3.2, 0])
        self.play(FadeOut(VGroup(halves, restored)), FadeIn(variants), FadeIn(q), run_time=1.1)
        sway(variants[0], 0.04, 1.2)
        sway(variants[1], 0.04, 1.45, 1.0)
        self.finish()


class S10End(EndCard):
    LINE = "Sexual reproduction: meiosis halves chromosome number\nand makes mixes; fertilization restores pairs."
