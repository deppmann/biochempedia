from bp_parts import *


# COLOR MAP (shared with chapter 1)
# GREY = old strands/backbones; GOLD = new strands; RED = A; BLUE = T;
# GREEN = C; PURPLE = G; WHITE/TEXT = labels; ORANGE = polymerase.
PURPLE = "#B58CD9"
ORANGE = "#FF9F43"
DARK_PANEL = "#29364D"
BASE_COLOURS = {"A": RED, "T": BLUE, "C": GREEN, "G": PURPLE}
PAIR = {"A": "T", "T": "A", "C": "G", "G": "C"}

FORK_Y = 0.35
UPPER_Y = 2.35
LOWER_Y = -1.65
LEFT_X = -5.75
RIGHT_X = 5.75


class ActiveSpokenScene(SpokenScene):
    """Spoken fork-world scene with a continuous, quiet copying scan behind the diagram."""

    def setup(self):
        super().setup()
        bands = VGroup()
        for x, opacity, speed in ((-5.8, 0.12, 1.65), (1.0, 0.08, 1.25)):
            band = Polygon(
                [-1.2, -3.5, 0],
                [0.7, -3.5, 0],
                [1.9, 3.5, 0],
                [0.0, 3.5, 0],
                stroke_width=0,
                fill_color=TEAL,
                fill_opacity=opacity,
            ).move_to([x, 0, 0]).set_z_index(-20)
            band.layout_ok = True
            band._scan_speed = speed

            def scan(m, dt):
                m.shift(RIGHT * m._scan_speed * dt)
                if m.get_left()[0] > 7.4:
                    m.shift(LEFT * 17.0)

            band.add_updater(scan)
            bands.add(band)
        self.add(bands)


def base_block(letter, at, scale=1.0, opacity=1.0):
    """A labelled rectangular base block, never a molecular structure."""
    col = BASE_COLOURS[letter]
    box = RoundedRectangle(
        corner_radius=0.09,
        width=0.54 * scale,
        height=0.48 * scale,
        stroke_color=col,
        stroke_width=3,
        fill_color=col,
        fill_opacity=0.25,
    )
    label = T(letter, max(24, int(28 * scale)), col, weight=BOLD).move_to(box)
    return VGroup(box, label).move_to(at).set_opacity(opacity)


def backbone(start, end, color=GREY, width=7):
    """A strand backbone whose arrowhead is at end."""
    return Arrow(
        start,
        end,
        buff=0,
        color=color,
        stroke_width=width,
        max_tip_length_to_length_ratio=0.055,
        max_stroke_width_to_length_ratio=8,
    )


def closed_ladder(x0=-5.6, x1=5.6, y=0.2, scale=1.0, old=True):
    """The carried grey ladder used for the rewind and the title."""
    dy = 0.66 * scale
    col = GREY if old else GOLD
    top = backbone([x1, y + dy, 0], [x0, y + dy, 0], col, 7)
    bottom = backbone([x0, y - dy, 0], [x1, y - dy, 0], col, 7)
    letters = ["A", "C", "T", "G", "A", "G", "C"]
    xs = np.linspace(x0 + 0.7, x1 - 0.7, len(letters))
    rungs = VGroup()
    for x, letter in zip(xs, letters):
        other = PAIR[letter]
        a = base_block(letter, [x, y + 0.31 * scale, 0], 0.72 * scale)
        b = base_block(other, [x, y - 0.31 * scale, 0], 0.72 * scale)
        rungs.add(a, b)
    field = RoundedRectangle(
        corner_radius=0.3,
        width=x1 - x0 + 0.45,
        height=1.75 * scale,
        stroke_width=0,
        fill_color=DARK_PANEL,
        fill_opacity=1,
    ).move_to([(x0 + x1) / 2, y, 0]).set_z_index(-3)
    return VGroup(top, bottom, rungs, field)


def copied_molecule(y, x0=-5.45, x1=5.45, scale=0.65):
    """One daughter molecule: one old GREY backbone and one new GOLD backbone."""
    old = backbone([x1, y + 0.34, 0], [x0, y + 0.34, 0], GREY, 6)
    new = backbone([x0, y - 0.34, 0], [x1, y - 0.34, 0], GOLD, 6)
    rungs = VGroup()
    for x, letter in zip(np.linspace(x0 + 0.8, x1 - 0.8, 6), ["A", "C", "T", "G", "A", "G"]):
        rungs.add(
            base_block(letter, [x, y + 0.17, 0], scale),
            base_block(PAIR[letter], [x, y - 0.17, 0], scale),
        )
    return VGroup(old, new, rungs)


def fork_world(fork_x=0.8, show_bases=True, upper_new=0.0, lower_segments=()):
    """The single carried fork world. Every fork scene rebuilds this exact geometry."""
    vertex = np.array([fork_x, FORK_Y, 0])
    upper = backbone(vertex, [LEFT_X, UPPER_Y, 0], GREY, 8)
    lower = backbone([LEFT_X, LOWER_Y, 0], vertex, GREY, 8)
    closed_top = Line(vertex, [RIGHT_X, FORK_Y + 0.43, 0], color=GREY, stroke_width=8)
    closed_bottom = Line(vertex, [RIGHT_X, FORK_Y - 0.43, 0], color=GREY, stroke_width=8)
    g = VGroup(upper, lower, closed_top, closed_bottom)
    open_field = Polygon(
        [LEFT_X - 0.15, UPPER_Y + 0.28, 0],
        vertex + UP * 0.62,
        vertex + DOWN * 0.62,
        [LEFT_X - 0.15, LOWER_Y - 0.28, 0],
        stroke_width=0,
        fill_color=DARK_PANEL,
        fill_opacity=1,
    ).set_z_index(-3)
    closed_field = Rectangle(
        width=max(0.2, RIGHT_X - fork_x),
        height=1.25,
        stroke_width=0,
        fill_color=DARK_PANEL,
        fill_opacity=1,
    ).move_to([(fork_x + RIGHT_X) / 2, FORK_Y, 0]).set_z_index(-3)
    g.add(open_field, closed_field)

    if show_bases:
        bases = VGroup()
        # A few large blocks make the templates readable without turning the frame into clutter.
        for frac, letter in zip((0.14, 0.30, 0.46, 0.62), ("A", "C", "T", "G")):
            p_u = interpolate(np.array([LEFT_X, UPPER_Y, 0]), vertex, frac)
            p_l = interpolate(np.array([LEFT_X, LOWER_Y, 0]), vertex, frac)
            bases.add(base_block(letter, p_u + DOWN * 0.28, 0.64))
            bases.add(base_block(PAIR[letter], p_l + UP * 0.28, 0.64))
        for x, letter in zip(np.linspace(fork_x + 0.8, RIGHT_X - 0.55, 4), ("C", "A", "G", "T")):
            bases.add(base_block(letter, [x, FORK_Y + 0.22, 0], 0.58))
            bases.add(base_block(PAIR[letter], [x, FORK_Y - 0.22, 0], 0.58))
        g.add(bases)

    if upper_new > 0:
        end = interpolate(np.array([LEFT_X + 0.35, UPPER_Y - 0.36, 0]), vertex + DOWN * 0.32, upper_new)
        g.add(backbone([LEFT_X + 0.35, UPPER_Y - 0.36, 0], end, GOLD, 8))

    if lower_segments:
        for xa, xb in lower_segments:
            ya = LOWER_Y + (FORK_Y - LOWER_Y) * ((xa - LEFT_X) / (fork_x - LEFT_X)) + 0.34
            yb = LOWER_Y + (FORK_Y - LOWER_Y) * ((xb - LEFT_X) / (fork_x - LEFT_X)) + 0.34
            g.add(backbone([xb, yb, 0], [xa, ya, 0], GOLD, 8))
    return g


def polymerase(at, size=1.0, label=True):
    body = RoundedRectangle(
        corner_radius=0.32,
        width=2.45 * size,
        height=1.25 * size,
        stroke_color=ORANGE,
        stroke_width=5,
        fill_color=ORANGE,
        fill_opacity=0.12,
    ).move_to(at)
    if not label:
        return VGroup(body)
    text = T("DNA polymerase", max(24, int(29 * size)), ORANGE, weight=BOLD).move_to(body)
    text.layout_ok = True  # deliberate label inside the polymerase shape
    return VGroup(body, text)


def bond_flash(at):
    return Flash(at, color=TEXT, line_length=0.25, flash_radius=0.48, num_lines=10)


def orbit(mob, amp_x=0.35, amp_y=0.22, speed=1.5, phase=0.0):
    """Visible ambient movement for a free nucleotide or a spotlight."""
    mob._orbit_t = phase
    base = mob.get_center().copy()

    def update(m, dt):
        m._orbit_t += dt
        m.move_to(base + RIGHT * amp_x * np.sin(speed * m._orbit_t) + UP * amp_y * np.cos(0.73 * speed * m._orbit_t))

    return mob.add_updater(update)


def arrow_rule_picture():
    """The exact close-up used whenever the direction rule is revisited."""
    old = backbone([5.45, 1.15, 0], [-5.35, 1.15, 0], GREY, 9)
    new = backbone([-4.8, -0.65, 0], [2.65, -0.65, 0], GOLD, 10)
    poly = polymerase([2.3, -0.65, 0], 0.88)
    old_lane = RoundedRectangle(corner_radius=0.25, width=11.2, height=1.05, stroke_width=0, fill_color=DARK_PANEL, fill_opacity=1).move_to([0, 1.15, 0]).set_z_index(-3)
    new_lane = RoundedRectangle(corner_radius=0.25, width=11.2, height=1.05, stroke_width=0, fill_color=DARK_PANEL, fill_opacity=1).move_to([0, -0.65, 0]).set_z_index(-3)
    return VGroup(old, new, poly, old_lane, new_lane)


QUESTION = "If polymerase only adds at the arrowhead, how can it copy this strand?"


def lower_question_backdrop():
    world = fork_world(1.15, show_bases=False, upper_new=0.92)
    ghost = backbone([0.65, -0.03, 0], [-4.75, -1.48, 0], GOLD, 8).set_opacity(0.34)
    ghost = DashedVMobject(ghost, num_dashes=18)
    mark = T("?", 76, GOLD, weight=BOLD).move_to([-1.55, -0.45, 0])
    mark.layout_ok = True  # deliberately sits on the lower arm named by the question
    halo = Ellipse(width=7.0, height=2.65, color=GOLD, stroke_width=4).move_to([-1.75, -0.6, 0]).set_opacity(0.24)
    return VGroup(world, halo, ghost, mark)


def accuracy_closeup(wrong="A", correct="G"):
    """Large, non-molecular base-pair check inside a polymerase outline."""
    shell = RoundedRectangle(
        corner_radius=0.38,
        width=7.0,
        height=4.5,
        stroke_color=ORANGE,
        stroke_width=5,
        fill_color=ORANGE,
        fill_opacity=0.24,
    ).move_to([-2.65, 0.15, 0])
    lab = T("DNA polymerase", 30, ORANGE, weight=BOLD).next_to(shell, UP, buff=0.16)
    template = base_block("C", [-3.75, 0.45, 0], 1.65)
    wrong_b = base_block(wrong, [-1.55, 0.45, 0], 1.65)
    correct_b = base_block(correct, [-1.55, 0.45, 0], 1.65)
    return shell, lab, template, wrong_b, correct_b


def inspection_beam():
    beam = RoundedRectangle(
        corner_radius=0.35,
        width=1.8,
        height=4.0,
        stroke_width=0,
        fill_color=BLUE,
        fill_opacity=0.22,
    ).move_to([-2.65, 0.15, 0]).set_z_index(-1)
    beam.layout_ok = True  # a translucent scan passes behind the labelled base blocks
    orbit(beam, 2.15, 0.0, 1.05, 0.0)
    return beam


def check_ledger(rows=3):
    data = [
        ("1", "matching check", BLUE),
        ("2", "proofreading", GOLD),
        ("3", "repair", GREEN),
    ][:rows]
    return Ledger(data, top_left=[1.15, 2.25], title="accuracy checks", row_h=0.78, key_w=0.75, width=5.2, size=28)


class S00Title(TitleCard):
    LESSON = "DNA structure and copying"
    TITLE = "Inside the Fork"

    def construct(self):
        ladder = closed_ladder(-5.9, 5.9, 0.0, 0.95).set_opacity(0.22)
        fork = fork_world(-2.4, show_bases=False).set_opacity(0.22)
        brand = T("BIOCHEMISTRYPEDIA", 20, TEAL, weight=BOLD).set_opacity(0.9)
        brand.layout_ok = True
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = T(self.TITLE, 54, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        words = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.add(ladder)
        self.play(Transform(ladder, fork), FadeIn(brand), FadeIn(lesson), run_time=0.8)
        self.play(Write(title), GrowFromCenter(rule), run_time=0.9)
        self.wait(0.55)
        self.play(FadeOut(VGroup(ladder, words)), run_time=0.7)
        self.finish()


class S01Link(ActiveSpokenScene):
    def construct(self):
        daughters = VGroup(copied_molecule(1.35), copied_molecule(-1.25))
        self.play(FadeIn(daughters, shift=LEFT * 0.15), run_time=0.8)
        self.at("each old strand")
        self.play(Indicate(daughters[0][0], color=GREY), Indicate(daughters[1][0], color=GREY), run_time=0.8)
        self.at("But how does")
        ladder = closed_ladder(-5.6, 5.6, 0.2, 1.0)
        self.play(ReplacementTransform(daughters, ladder), run_time=1.0)
        letters = VGroup(*[T(x, 34, GOLD, weight=BOLD).move_to([xv, -2.35, 0]) for x, xv in zip("ATCG", [-1.5, -0.5, 0.5, 1.5])])
        self.at("one letter at a time")
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.25) for x in letters], lag_ratio=0.18), run_time=1.2)
        self.at("does not open")
        little_fork = fork_world(-3.25, show_bases=True)
        self.play(FadeOut(VGroup(letters, ladder)), FadeIn(little_fork), run_time=1.2)
        self.finish()


class S02Fork(ActiveSpokenScene):
    def construct(self):
        world = fork_world(-3.25, show_bases=True)
        self.add(world)
        self.at("moving Y")
        fork_label = T("fork", 32, TEXT, weight=BOLD).move_to([-3.0, -0.75, 0])
        pointer = Arrow(fork_label.get_top(), [-3.18, 0.1, 0], buff=0.12, color=TEXT, stroke_width=4)
        self.play(GrowArrow(pointer), FadeIn(fork_label), run_time=0.7)
        self.at("fork moves along")
        moved = fork_world(1.2, show_bases=True)
        move_arrow = Arrow([-2.4, -2.55, 0], [2.6, -2.55, 0], buff=0, color=GOLD, stroke_width=6)
        move_label = T("fork moves", 30, GOLD, weight=BOLD).next_to(move_arrow, DOWN, buff=0.15)
        self.play(FadeOut(VGroup(pointer, fork_label)), GrowArrow(move_arrow), FadeIn(move_label), Transform(world, moved), run_time=2.2, rate_func=linear)
        self.at("Both old strands")
        self.play(Indicate(world[0], color=GREY), Indicate(world[1], color=GREY), run_time=0.9)
        self.at("opposite ways")
        self.play(Circumscribe(world[0].get_tip(), color=TEXT), Circumscribe(world[1].get_tip(), color=TEXT), run_time=0.9)
        self.finish()


class S03Polymerase(ActiveSpokenScene):
    def construct(self):
        world = fork_world(1.2, show_bases=False, upper_new=0.58)
        self.add(world)
        poly = polymerase([-0.35, 1.35, 0], 0.92)
        self.at("enzyme that builds")
        self.play(FadeIn(poly, scale=0.85), run_time=0.8)
        free = VGroup(
            base_block("A", [3.8, 2.25, 0], 1.0),
            base_block("T", [4.65, 1.15, 0], 1.0),
            base_block("G", [3.55, -0.25, 0], 1.0),
            base_block("C", [5.15, -0.55, 0], 1.0),
        )
        orbit(free[0], 0.65, 0.32, 1.45, 0.4)
        orbit(free[1], 0.55, 0.38, 1.7, 1.2)
        orbit(free[2], 0.72, 0.28, 1.3, 2.0)
        orbit(free[3], 0.48, 0.34, 1.85, 2.7)
        self.at("At each base")
        self.play(FadeIn(free, lag_ratio=0.15), run_time=0.8)
        target = base_block("T", [0.0, 1.35, 0], 1.0)
        self.at("picks the nucleotide")
        free[1].clear_updaters()
        self.play(Transform(free[1], target), run_time=1.0)
        self.at("wrong one almost")
        self.play(free[0].animate.shift(RIGHT * 0.5), free[2].animate.shift(RIGHT * 0.45), free[3].animate.shift(RIGHT * 0.4), run_time=2.4, rate_func=there_and_back)
        self.at("Then it joins")
        self.play(FadeOut(VGroup(free[0], free[2], free[3])), bond_flash([-0.45, 1.35, 0]), run_time=2.8)
        self.finish()


class S04Rule(ActiveSpokenScene):
    def construct(self):
        picture = arrow_rule_picture()
        self.play(FadeIn(picture), run_time=0.7)
        self.at("one strict habit")
        halo = Circle(radius=0.42, color=GOLD, stroke_width=6).move_to(picture[1].get_end())
        self.play(Create(halo), run_time=0.7)
        incoming = base_block("C", [4.5, -0.65, 0], 1.05)
        self.at("adds nucleotides only")
        self.play(incoming.animate.move_to([3.0, -0.65, 0]), bond_flash([2.75, -0.65, 0]), run_time=1.0)
        tail_try = base_block("A", [-5.75, -1.75, 0], 0.95)
        cross = T("×", 50, RED, weight=BOLD).move_to([-4.85, 0.05, 0])
        self.at("arrowhead end")
        self.play(FadeIn(tail_try), tail_try.animate.move_to([-4.85, -0.65, 0]), run_time=0.65)
        self.play(FadeIn(cross), tail_try.animate.shift(DOWN * 0.8), run_time=0.55)
        banner = caption("adds only at the arrowhead", 34, GOLD)
        self.at("every new strand")
        self.play(FadeOut(VGroup(tail_try, cross)), FadeIn(banner), run_time=0.7)
        self.at("opposite way")
        self.play(Indicate(picture[0].get_tip(), color=GREY), Indicate(picture[1].get_tip(), color=GOLD), run_time=0.8)
        self.finish()


class S05Upper(ActiveSpokenScene):
    def construct(self):
        x = ValueTracker(-2.7)
        world = always_redraw(lambda: fork_world(x.get_value(), show_bases=False))
        start = LEFT_X + 0.35
        gold = always_redraw(lambda: backbone(
            [start, UPPER_Y - 0.36, 0],
            [x.get_value() - 0.35, FORK_Y + 0.18, 0],
            GOLD,
            9,
        ))
        poly = always_redraw(lambda: polymerase([x.get_value() - 0.5, FORK_Y + 0.55, 0], 0.72))
        self.add(world, gold, poly)
        self.at("arrowhead points")
        self.play(Indicate(gold, color=GOLD), run_time=0.8)
        pieces = ValueTracker(1)
        read = counter("upper strand: {:.0f} piece", pieces, at=[4.15, 2.72, 0], size=30, color=GOLD)
        self.at("polymerase simply follows")
        self.play(FadeIn(read), x.animate.set_value(0.7), run_time=2.2, rate_func=linear)
        self.at("nucleotide after nucleotide")
        self.play(x.animate.set_value(3.25), run_time=2.3, rate_func=linear)
        self.finish()


class S06Predict(ActiveSpokenScene):
    def construct(self):
        backdrop = lower_question_backdrop()
        orbit(backdrop[1], 1.0, 0.16, 1.25, 0.0)
        self.add(backdrop[0])
        self.at("look at the lower")
        self.play(FadeIn(backdrop[1]), run_time=0.7)
        self.at("must point the other way")
        self.play(Create(backdrop[2]), run_time=1.1)
        self.at("back away from")
        self.play(Indicate(backdrop[2], color=GOLD), run_time=0.8)
        self.at("If polymerase only")
        self.play(FadeIn(backdrop[3], scale=0.6), run_time=0.6)
        q = question_card(QUESTION, y=-3.15, size=29, max_w=10.9)
        self.at("how can it copy")
        self.play(FadeIn(q.question, shift=UP * 0.1), run_time=0.7)
        pulse(backdrop[3], base=5.5, amp=1.8, speed=3.2)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = QUESTION
    CARD = {"y": -3.15, "size": 29, "max_w": 10.9}
    RING_AT = (6.0, -3.05, 0)
    SECONDS = 5.0

    def backdrop(self):
        g = lower_question_backdrop()
        pulse(g[3], base=5.5, amp=1.8, speed=3.2)
        orbit(g[1], 1.0, 0.16, 1.25, 0.0)
        return g


class S08Reveal(ActiveSpokenScene):
    def construct(self):
        fork_x = -0.2
        world = fork_world(fork_x, show_bases=False, upper_new=0.9)
        self.add(world)
        count = ValueTracker(0)
        read = counter("lower strand pieces: {:.0f}", count, at=[4.0, 2.72, 0], size=29, color=GOLD)
        self.at("builds in short pieces")
        p1 = backbone([-0.55, 0.0, 0], [-3.45, -0.92, 0], GOLD, 9)
        self.play(
            FadeIn(read),
            count.animate.set_value(1),
            GrowArrow(p1),
            world.animate.shift(RIGHT * 0.55),
            run_time=4.8,
            rate_func=linear,
        )
        self.at("Each piece starts")
        beads = VGroup(*[
            base_block(letter, interpolate(np.array([-0.55, 0.0, 0]), np.array([-3.45, -0.92, 0]), f), 0.68)
            for letter, f in zip(("T", "G", "A", "C"), (0.18, 0.40, 0.62, 0.84))
        ])
        for bead in beads:
            bead[1].layout_ok = True  # bases intentionally sit on their new strand backbone
        self.play(
            LaggedStart(*[FadeIn(b, scale=0.75) for b in beads], lag_ratio=0.28),
            world.animate.shift(RIGHT * 0.40),
            run_time=3.2,
            rate_func=linear,
        )
        self.at("fork opens more")
        moved = fork_world(1.8, show_bases=False, upper_new=0.92)
        self.play(Transform(world, moved), run_time=1.35, rate_func=linear)
        p2 = backbone([1.45, 0.42, 0], [-0.42, -0.15, 0], GOLD, 9)
        self.at("fresh piece starts")
        self.play(count.animate.set_value(2), GrowArrow(p2), run_time=1.25)
        self.at("grows back toward")
        self.play(p2.animate.put_start_and_end_on([1.45, 0.42, 0], [-0.62, -0.21, 0]), run_time=0.8)
        p3 = backbone([2.75, 0.83, 0], [1.5, 0.45, 0], GOLD, 9)
        self.play(count.animate.set_value(3), GrowArrow(p3), run_time=0.9)
        joiner = chip("joining enzyme", GREY, 26).move_to([0.35, -1.15, 0])
        joiner[1].layout_ok = True  # labelled enzyme deliberately covers the joining point
        self.at("Another enzyme joins")
        self.play(FadeIn(joiner), joiner.animate.move_to([-0.5, -0.18, 0]), bond_flash([-0.5, -0.18, 0]), run_time=1.0)
        joined = T("lower strand: joined", 30, GOLD, weight=BOLD).move_to(read)
        self.at("into one strand")
        self.play(swap(read, joined), FadeOut(joiner), bond_flash([1.47, 0.43, 0]), run_time=0.9)
        self.finish()


class S09Check(ActiveSpokenScene):
    def construct(self):
        shell, lab, template, wrong, correct = accuracy_closeup()
        beam = inspection_beam()
        self.play(FadeIn(shell), FadeIn(lab), FadeIn(beam), run_time=0.7)
        self.at("zoom in on one step")
        self.play(FadeIn(template), run_time=0.7)
        ledger = check_ledger(1)
        self.at("Polymerase tests")
        self.play(FadeIn(ledger), ledger.reveal(0), FadeIn(wrong, shift=LEFT * 0.2), run_time=1.0)
        clash = VGroup(Line([-2.75, 0.9, 0], [-2.35, 0.0, 0], color=RED, stroke_width=7), Line([-2.75, 0.0, 0], [-2.35, 0.9, 0], color=RED, stroke_width=7))
        self.at("does not pair")
        self.play(Create(clash), wrong.animate.shift(RIGHT * 1.35), run_time=0.8)
        self.at("turned away")
        self.play(FadeOut(VGroup(wrong, clash)), FadeIn(correct, shift=LEFT * 0.25), bond_flash([-2.65, 0.45, 0]), run_time=0.9)
        self.finish()


class S10Proofread(ActiveSpokenScene):
    def construct(self):
        shell, lab, template, wrong, correct = accuracy_closeup()
        ledger = check_ledger(3)
        beam = inspection_beam()
        self.add(shell, beam, lab, template, wrong, ledger)
        self.add(ledger.rows[0])
        self.at("wrong base slips")
        self.play(bond_flash([-2.65, 0.45, 0]), run_time=0.7)
        self.at("Polymerase checks")
        self.play(Indicate(wrong, color=RED), run_time=0.7)
        self.at("removes most wrong")
        self.play(wrong.animate.shift(RIGHT * 1.4), FadeIn(correct, shift=LEFT * 0.25), run_time=0.9)
        self.at("called proofreading")
        self.play(ledger.reveal(1), bond_flash([-2.65, 0.45, 0]), run_time=0.8)
        finished = VGroup(
            backbone([-5.45, -2.4, 0], [-1.35, -2.4, 0], GREY, 7),
            backbone([-1.35, -3.05, 0], [-5.45, -3.05, 0], GOLD, 7),
            base_block("C", [-3.3, -2.55, 0], 0.9),
            base_block("A", [-3.3, -2.9, 0], 0.9),
        )
        repair = chip("repair enzyme", GREEN, 25).move_to([-0.25, -2.72, 0])
        repair[1].layout_ok = True  # labelled enzyme deliberately covers the mismatch it repairs
        self.at("Repair enzymes")
        self.play(FadeIn(finished), FadeIn(repair), run_time=0.8)
        fixed = base_block("G", [-3.3, -2.9, 0], 0.9)
        self.at("catch many of")
        self.play(repair.animate.move_to([-3.3, -2.72, 0]), Transform(finished[3], fixed), bond_flash([-3.3, -2.72, 0]), ledger.reveal(2), run_time=1.0)
        self.finish()


class S11Tally(ActiveSpokenScene):
    def construct(self):
        stage = VGroup(
            RoundedRectangle(corner_radius=0.3, width=5.7, height=5.45, stroke_width=0, fill_color=DARK_PANEL, fill_opacity=1).move_to([-3.15, 0.15, 0]),
            RoundedRectangle(corner_radius=0.3, width=5.7, height=5.45, stroke_width=0, fill_color=DARK_PANEL, fill_opacity=1).move_to([3.15, 0.15, 0]),
        ).set_z_index(-3)
        self.add(stage)
        ledger = check_ledger(3)
        self.play(FadeIn(ledger), run_time=0.6)
        self.at("matching check")
        self.play(ledger.reveal(0), run_time=0.55)
        self.at("proofreading")
        self.play(ledger.reveal(1), run_time=0.55)
        self.at("then repair")
        self.play(ledger.reveal(2), run_time=0.55)
        segments = VGroup(
            Rectangle(width=3.2, height=0.85, color=BLUE, fill_color=BLUE, fill_opacity=0.7),
            Rectangle(width=3.2, height=0.85, color=GOLD, fill_color=GOLD, fill_opacity=0.7),
            Rectangle(width=3.2, height=0.85, color=GREEN, fill_color=GREEN, fill_opacity=0.7),
        ).arrange(RIGHT, buff=0.08).move_to([0, 0.35, 0])
        labels = VGroup(T("match", 26, BG, weight=BOLD), T("proofread", 26, BG, weight=BOLD), T("repair", 26, BG, weight=BOLD))
        for label, box in zip(labels, segments):
            label.move_to(box)
            label.layout_ok = True  # deliberate text inside its coloured check segment
        bar = VGroup(segments, labels)
        self.at("Each later check")
        self.play(FadeOut(ledger.everything()), FadeIn(bar, shift=DOWN * 0.2), run_time=1.0)
        self.play(LaggedStart(*[Indicate(s, scale_factor=1.04) for s in segments], lag_ratio=0.35), run_time=1.3)
        estimate = VGroup(
            T("textbook estimate", 28, GREY),
            T("about 1 uncorrected mistake", 38, TEXT, weight=BOLD),
            M("per 1,000,000,000 bases copied", 34, GOLD),
        ).arrange(DOWN, buff=0.25).move_to([0, -1.75, 0])
        self.at("textbook estimate")
        self.play(bar.animate.shift(UP * 1.5), FadeIn(estimate, shift=UP * 0.2), run_time=1.0)
        self.finish()


class S12TwoJobs(ActiveSpokenScene):
    def construct(self):
        panels = TwoPanel("PAIRING → POSSIBLE", "CHECKING → ACCURATE", colors=(GOLD, GREEN), top=3.15, bottom=-2.35)
        panels.left_frame.set_fill(DARK_PANEL, opacity=1)
        panels.right_frame.set_fill(DARK_PANEL, opacity=1)
        self.play(FadeIn(panels), run_time=0.7)
        pairs = VGroup(
            VGroup(base_block("A", ORIGIN, 1.25), T("with", 28, TEXT), base_block("T", ORIGIN, 1.25)).arrange(RIGHT, buff=0.35),
            VGroup(base_block("C", ORIGIN, 1.25), T("with", 28, TEXT), base_block("G", ORIGIN, 1.25)).arrange(RIGHT, buff=0.35),
        ).arrange(DOWN, buff=0.55)
        panels.put(pairs, "left")
        checks = VGroup(
            chip("matching", BLUE, 28),
            Arrow(ORIGIN, DOWN * 0.38, buff=0, color=GREY),
            chip("proofreading", GOLD, 28),
            Arrow(ORIGIN, DOWN * 0.38, buff=0, color=GREY),
            chip("repair", GREEN, 28),
        ).arrange(DOWN, buff=0.1)
        panels.put(checks, "right")
        checks.shift(DOWN * 0.08)
        self.at("Pairing makes")
        self.play(FadeIn(pairs, lag_ratio=0.18), run_time=1.0)
        self.at("which base goes where")
        self.play(Indicate(pairs, color=GOLD), run_time=0.8)
        self.at("Checking makes")
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.08) for x in checks], lag_ratio=0.12), run_time=1.1)
        self.at("removes almost every")
        self.play(Indicate(checks, color=GREEN), run_time=0.8)
        fork = fork_world(3.4, show_bases=False, upper_new=0.96, lower_segments=((-4.9, -2.4), (-2.25, 0.1), (0.25, 2.75))).scale(0.7).move_to([0, 0.2, 0])
        self.play(FadeOut(VGroup(panels, pairs, checks)), FadeIn(fork, scale=0.92), run_time=1.0)
        self.play(fork.animate.shift(RIGHT * 0.7), run_time=1.0, rate_func=linear)
        self.play(FadeOut(fork), run_time=0.5)
        self.finish()


class S13End(EndCard):
    LINE = "Pairing makes the copy possible; checking makes it accurate."
