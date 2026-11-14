"""From DNA Route to Gene Order.

COLOR MAP (one colour per concept, whole film)
  GOLD    donor DNA and chromosomal markers
  GREY    recipient bacterium and neutral outlines
  TEAL    donor bacterium
  PURPLE  phage
  ORANGE  F factor and origin
  TEXT    recipient chromosome
  BLUE    filter
  RED     DNase

All drawings are schematic paths and labelled cartoons, never molecular structures.
"""
from bp_parts import *


PURPLE = "#A98BEA"
ORANGE = "#F29E4C"
LIGHT_GREY = "#C7CED8"


def bacterium(center, color, width=4.0, height=3.3, opacity=0.20):
    """The carried cell shape used throughout the film."""
    return RoundedRectangle(
        corner_radius=height * 0.33,
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=5,
        fill_color=color,
        fill_opacity=opacity,
    ).move_to(center)


def cell_pair(scale=1.0, y=0.0):
    """The one donor/recipient world, rebuilt at identical coordinates."""
    left = np.array([-3.15, y, 0.0])
    right = np.array([3.15, y, 0.0])
    donor = bacterium(left, TEAL, 4.0 * scale, 3.4 * scale)
    recipient = bacterium(right, LIGHT_GREY, 4.0 * scale, 3.4 * scale)
    bridge = Line(
        donor.get_right(), recipient.get_left(), color=GREY,
        stroke_width=8 * scale,
    )
    labels = VGroup(
        T("donor", 28, TEAL).next_to(donor, UP, buff=0.34),
        T("recipient", 28, LIGHT_GREY).next_to(recipient, UP, buff=0.34),
    )
    return VGroup(donor, recipient, bridge, labels)


def chromosome(center, radius=1.05, color=TEXT, width=6):
    """A schematic chromosome path."""
    return Circle(radius=radius, color=color, stroke_width=width).move_to(center)


def phage(center, scale=1.0, cargo=True):
    """A labelled carrier cartoon; the internal bar is donor DNA."""
    c = np.array(center, dtype=float)
    coat = RoundedRectangle(
        width=1.35 * scale, height=1.0 * scale, corner_radius=0.24 * scale,
        stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.12,
    ).move_to(c + UP * 0.35 * scale)
    tail = Line(c + DOWN * 0.15 * scale, c + DOWN * 0.9 * scale, color=PURPLE, stroke_width=5)
    feet = VGroup(
        Line(c + DOWN * 0.9 * scale, c + np.array([-0.35, -1.15, 0]) * scale, color=PURPLE, stroke_width=4),
        Line(c + DOWN * 0.9 * scale, c + np.array([0.35, -1.15, 0]) * scale, color=PURPLE, stroke_width=4),
    )
    g = VGroup(coat, tail, feet)
    if cargo:
        g.add(Line(c + np.array([-0.38, 0.35, 0]) * scale,
                   c + np.array([0.38, 0.35, 0]) * scale,
                   color=GOLD, stroke_width=9))
    return g


def filter_bar(x=0.85, height=5.7):
    """A porous filter shown as one tall blue object."""
    rail = RoundedRectangle(
        width=0.46, height=height, corner_radius=0.12,
        stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.18,
    ).move_to([x, 0, 0])
    pores = VGroup(*[
        Circle(radius=0.075, color=BLUE, fill_color=BG, fill_opacity=1, stroke_width=2)
        .move_to([x, yy, 0]) for yy in np.linspace(-2.25, 2.25, 7)
    ])
    return VGroup(rail, pores)


def route_world(unknown=False):
    """The opening/reveal world: one fixed recipient and three incoming paths."""
    recipient = bacterium([4.45, 0, 0], LIGHT_GREY, 3.6, 5.5)
    rec_label = T("recipient", 28, LIGHT_GREY).move_to([4.45, 3.28, 0])
    paths = VGroup(*[
        Line([-5.9, y, 0], [2.35, y, 0], color=GREY, stroke_width=4, stroke_opacity=0.55)
        for y in (1.75, 0.0, -1.75)
    ])
    if unknown:
        marks = VGroup(*[T("?", 54, GOLD).move_to([-1.65, y + 0.42, 0]) for y in (1.75, 0, -1.75)])
        return VGroup(recipient, rec_label, paths, marks)

    bare = VGroup(
        Line([-4.95, 1.75, 0], [-3.65, 1.75, 0], color=GOLD, stroke_width=10),
        T("transformation", 28, GOLD).move_to([-4.25, 2.45, 0]),
    )
    donor = bacterium([-4.3, 0, 0], TEAL, 2.3, 1.35)
    contact = Line(donor.get_right(), [2.35, 0, 0], color=TEAL, stroke_width=7)
    middle = VGroup(donor, contact, T("conjugation", 28, TEAL).move_to([-4.3, 1.08, 0]))
    virus = phage([-4.3, -1.35, 0], scale=0.68)
    lower = VGroup(virus, T("transduction", 28, PURPLE).move_to([-4.3, -2.75, 0]))
    return VGroup(recipient, rec_label, paths, bare, middle, lower)


def evidence_board():
    """The exact carried frame for the predict scene and its silent pause."""
    question = fit_text("Which carrier fits both clues?", max_w=11.6, size=42, color=GOLD).move_to([0, 3.34, 0])

    left_box = RoundedRectangle(width=5.2, height=2.0, corner_radius=0.18,
                                color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.07).move_to([-2.8, 1.55, 0])
    right_box = RoundedRectangle(width=5.2, height=2.0, corner_radius=0.18,
                                 color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.07).move_to([2.8, 1.55, 0])
    left = VGroup(left_box, T("survives DNase", 30, RED).move_to([-2.8, 2.12, 0]),
                  Line([-3.45, 1.15, 0], [-2.15, 1.15, 0], color=GOLD, stroke_width=10))
    mini_filter = filter_bar(3.05, 1.1).scale(0.75)
    blocked = Arrow([1.55, 1.1, 0], [2.55, 1.1, 0], buff=0, color=TEAL, stroke_width=6, tip_length=0.2)
    right = VGroup(right_box, T("stops at filter", 30, BLUE).move_to([2.8, 2.12, 0]), mini_filter, blocked)

    icons = VGroup(
        VGroup(Line([-0.55, 0, 0], [0.55, 0, 0], color=GOLD, stroke_width=9), T("transformation", 26, GREY).next_to([0, -0.15, 0], DOWN, buff=0.22)),
        VGroup(bacterium([-0.5, 0, 0], TEAL, 0.85, 0.65), bacterium([0.5, 0, 0], LIGHT_GREY, 0.85, 0.65),
               Line([-0.08, 0, 0], [0.08, 0, 0], color=TEAL, stroke_width=5), T("conjugation", 26, GREY).move_to([0, -0.7, 0])),
        VGroup(phage([0, 0.25, 0], 0.52), T("transduction", 26, GREY).move_to([0, -0.7, 0])),
    )
    for icon, x in zip(icons, (-4.25, 0, 4.25)):
        icon.move_to([x, -1.25, 0])
    return VGroup(question, left, right, icons)


def marker_timeline(y=-0.25):
    """One shared, number-free map used in the mapping scenes."""
    xs = (-4.6, -1.8, 0.5, 4.3)
    line = Arrow([-5.6, y, 0], [5.55, y, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.22)
    names = ("A", "B", "C", "D")
    marks = VGroup(*[
        VGroup(Line([x, y - 0.18, 0], [x, y + 0.18, 0], color=GOLD, stroke_width=6),
               chip(n, GOLD, 28, pad=0.13).move_to([x, y + 0.68, 0]))
        for x, n in zip(xs, names)
    ])
    gaps = VGroup(*[
        VGroup(Line([a, y - 0.55, 0], [b, y - 0.55, 0], color=GOLD, stroke_width=4),
               Line([a, y - 0.7, 0], [a, y - 0.4, 0], color=GOLD, stroke_width=4),
               Line([b, y - 0.7, 0], [b, y - 0.4, 0], color=GOLD, stroke_width=4),
               T("gap", 26, GOLD).move_to([(a + b) / 2, y - 0.95, 0]))
        for a, b in zip(xs[:-1], xs[1:])
    ])
    return VGroup(line, marks, gaps)


class S00Hook(SpokenScene):
    def construct(self):
        world = route_world(unknown=True)
        pulse(world[0], base=5.0, amp=1.4, speed=2.2)
        self.play(FadeIn(world[:3]), run_time=0.8)
        dots = VGroup(*[Dot([-5.5, y, 0], radius=0.14, color=GOLD) for y in (1.75, 0, -1.75)])
        self.add(dots, scope_tag("schematic"))
        self.at("A bacterium gained")
        self.play(*[d.animate.shift(RIGHT * 7.2) for d in dots], run_time=2.0, rate_func=linear)
        self.at("What carried it there")
        self.play(FadeIn(world[3]), *[Indicate(p, color=GOLD) for p in world[2]], run_time=1.2)
        self.at("Watch the donor DNA")
        self.play(*[d.animate.shift(LEFT * 7.2) for d in dots], run_time=1.4, rate_func=linear)
        self.play(*[d.animate.shift(RIGHT * 7.2) for d in dots], run_time=1.8, rate_func=linear)
        self.at("Bacteria do not make")
        rule = caption("Donor genes can become inherited.", color=GOLD)
        self.play(FadeIn(rule), run_time=0.7)
        self.play(*[d.animate.shift(LEFT * 4.2) for d in dots], run_time=1.6, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Bacterial and phage genetics"
    TITLE = "From DNA Route to Gene Order"


class S02ThreeRoutes(SpokenScene):
    def construct(self):
        world = route_world(False)
        pulse(world[0], base=5.0, amp=1.4, speed=2.2)
        bob(world[0], amp=0.10, speed=2.2)
        self.add(world[:3], scope_tag("schematic"))
        self.at("One path exposes")
        self.play(FadeIn(world[3]), run_time=0.7)
        self.play(world[3][0].animate.shift(RIGHT * 5.9), run_time=1.7, rate_func=linear)
        self.at("Another joins donor")
        self.play(FadeIn(world[4]), run_time=0.7)
        gold = Dot([-4.1, 0, 0], radius=0.14, color=GOLD)
        self.add(gold)
        self.play(gold.animate.move_to([2.6, 0, 0]), run_time=1.7, rate_func=linear)
        self.at("The third protects")
        self.play(FadeIn(world[5]), run_time=0.7)
        self.play(world[5][0].animate.shift(RIGHT * 6.5), run_time=1.8, rate_func=linear)
        self.at("Competent cells take up")
        self.play(world[3][0].animate.move_to([4.45, 1.75, 0]), run_time=1.2)
        self.play(Indicate(world[0], color=LIGHT_GREY, scale_factor=1.0), run_time=0.8)
        self.finish()


class S03TwoTests(SpokenScene):
    def construct(self):
        world = route_world(False)
        pulse(world[0], base=5.0, amp=1.4, speed=2.2)
        self.add(world)
        filt = filter_bar(1.1)
        filt.shift(LEFT * 2.0)
        self.at("A filter that stops")
        self.play(filt.animate.shift(RIGHT * 2.0), run_time=1.0)
        self.play(world[4][0].animate.shift(LEFT * 0.55), run_time=1.0)
        self.play(world[3][0].animate.shift(RIGHT * 5.6), world[5][0].animate.shift(RIGHT * 5.7), run_time=1.5)
        sweep = Line([-5.0, 2.75, 0], [-5.0, -2.75, 0], color=RED, stroke_width=12)
        dnase = T("DNase", 30, RED).move_to([0, 3.42, 0])
        self.at("Deoxyribonuclease destroys")
        self.play(FadeOut(world[3][1]), FadeOut(world[4][2]), FadeOut(world[5][1]), run_time=0.3)
        self.play(FadeIn(dnase), Create(sweep), run_time=0.3)
        self.play(sweep.animate.shift(RIGHT * 8.8),
                  FadeOut(world[3][0]), run_time=1.7, rate_func=linear)
        self.at("but a phage coat")
        self.play(Indicate(world[5][0], color=PURPLE), run_time=1.1)
        self.at("That two step test")
        decision = T("two tests → one decision", 30, TEXT).move_to([-3.55, 3.32, 0])
        self.play(swap(dnase, decision), run_time=0.8)
        self.play(Indicate(filt, color=BLUE), Indicate(world[5][0][-1], color=GOLD), run_time=1.2)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        board = evidence_board()
        pulse(board[1][0], base=3.0, amp=1.0, speed=2.0)
        pulse(board[2][0], base=3.0, amp=1.0, speed=2.3)
        self.at("An unknown transfer")
        self.play(FadeIn(board[1]), run_time=0.8)
        self.at("but stops when cells")
        self.play(FadeIn(board[2]), run_time=0.8)
        self.at("Which carrier fits")
        self.play(FadeIn(board[0]), run_time=0.7)
        self.at("Follow both clues")
        self.play(FadeIn(board[3]), run_time=0.8)
        for icon in board[3]:
            bob(icon, amp=0.035, speed=1.5)
        self.at("One result rules out")
        self.play(Indicate(board[1], color=RED), run_time=1.0)
        self.at("The other rules out")
        self.play(Indicate(board[2], color=BLUE), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = ""
    SECONDS = 4.5
    CARD = {"size": 24}

    def backdrop(self):
        board = evidence_board()
        for icon in board[3]:
            bob(icon, amp=0.035, speed=1.5)
        pulse(board[2][2][0], base=4.0, amp=1.0, speed=3.0)
        return board


class S06Reveal(SpokenScene):
    def construct(self):
        pair = cell_pair()
        pulse(pair[0], base=5.0, amp=1.5, speed=2.0)
        pulse(pair[1], base=5.0, amp=1.5, speed=2.3)
        pair[0].shift(LEFT * 1.0)
        pair[1].shift(RIGHT * 1.0)
        pair[2].set_opacity(0)
        self.at("Conjugation fits")
        self.play(FadeIn(pair), pair[0].animate.shift(RIGHT * 1.0), pair[1].animate.shift(LEFT * 1.0), run_time=1.1)
        pair[2].set_opacity(1)
        gold = Dot(pair[0].get_center(), radius=0.15, color=GOLD)
        self.add(gold)
        self.at("Its DNA is never exposed")
        self.play(gold.animate.move_to(pair[1].get_center()), run_time=2.0, rate_func=linear)
        sweep = Line([-5.7, 2.3, 0], [-5.7, -2.3, 0], color=RED, stroke_width=12)
        self.at("so the enzyme misses")
        self.play(FadeOut(pair[3]), run_time=0.3)
        self.play(sweep.animate.shift(RIGHT * 11.4), run_time=1.2, rate_func=linear)
        filt = filter_bar(0.0)
        filt.shift(UP * 5.7)
        self.at("Separating the cells")
        self.play(filt.animate.shift(DOWN * 5.7), pair[2].animate.set_opacity(0),
                  pair[0].animate.shift(LEFT * 0.65), pair[1].animate.shift(RIGHT * 0.65), run_time=1.4)
        self.at("Both clues point")
        rule = caption("direct contact", color=TEAL, size=36)
        self.play(FadeIn(rule), run_time=0.7)
        self.play(Indicate(pair[0], color=TEAL), Indicate(pair[1], color=LIGHT_GREY), run_time=1.2)
        self.finish()


class S07FFactor(SpokenScene):
    def construct(self):
        pair = cell_pair()
        pulse(pair[0], base=5.0, amp=1.6, speed=2.0)
        pulse(pair[1], base=5.0, amp=1.6, speed=2.4)
        bob(pair[0], amp=0.11, speed=2.0)
        bob(pair[1], amp=0.11, speed=2.3, seed=2)
        self.add(pair)
        chrom_d = chromosome(pair[0].get_center(), 1.05, TEXT, 5)
        chrom_r = chromosome(pair[1].get_center(), 1.05, TEXT, 5)
        pulse(chrom_d, base=5.0, amp=1.3, speed=2.2)
        pulse(chrom_r, base=5.0, amp=1.3, speed=2.6)
        bob(chrom_d, amp=0.11, speed=2.0)
        bob(chrom_r, amp=0.11, speed=2.3, seed=2)
        f_ring = Circle(radius=0.42, color=ORANGE, stroke_width=7).move_to(pair[0].get_center() + LEFT * 0.2)
        f_lab = T("F", 28, ORANGE).move_to(f_ring)
        self.add(chrom_d, chrom_r)
        self.at("In E coli")
        self.play(Create(f_ring), FadeIn(f_lab), run_time=1.0)
        plus = T("F+", 30, ORANGE).move_to([-3.15, -2.25, 0])
        minus = T("F−", 30, LIGHT_GREY).move_to([3.15, -2.25, 0])
        self.play(FadeIn(plus), FadeIn(minus), run_time=0.7)
        self.at("Free F transfers")
        strand = ArcBetweenPoints(f_ring.get_left(), f_ring.get_right(), angle=-PI, color=ORANGE, stroke_width=7)
        self.play(ReplacementTransform(f_ring, strand), FadeOut(f_lab), run_time=0.8)
        self.at("One strand crosses")
        self.play(strand.animate.move_to(pair[1].get_center()), run_time=1.8, rate_func=linear)
        self.at("and each cell completes")
        new_d = Circle(radius=0.42, color=ORANGE, stroke_width=7).move_to(pair[0].get_center() + LEFT * 0.2)
        new_r = Circle(radius=0.42, color=ORANGE, stroke_width=7).move_to(pair[1].get_center() + LEFT * 0.2)
        plus_r = T("F+", 30, ORANGE).move_to(minus)
        self.play(Create(new_d), ReplacementTransform(strand, new_r), swap(minus, plus_r), run_time=1.3)
        self.at("Chromosomal markers rarely")
        self.play(Indicate(VGroup(chrom_d, chrom_r), color=TEXT), run_time=1.2)
        self.finish()


class S08Hfr(SpokenScene):
    def construct(self):
        pair = cell_pair()
        pulse(pair[0], base=5.0, amp=1.6, speed=2.0)
        pulse(pair[1], base=5.0, amp=1.6, speed=2.4)
        bob(pair[0], amp=0.10, speed=2.0)
        bob(pair[1], amp=0.10, speed=2.3, seed=2)
        donor_c = pair[0].get_center()
        chrom = chromosome(donor_c, 1.12, TEXT, 6)
        f_ring = Circle(radius=0.43, color=ORANGE, stroke_width=7).move_to(donor_c + LEFT * 0.15)
        self.add(pair, chrom, f_ring)
        embedded = Arc(radius=1.12, start_angle=-0.35, angle=0.7, arc_center=donor_c, color=ORANGE, stroke_width=9)
        self.at("When F joins")
        self.play(ReplacementTransform(f_ring, embedded), run_time=1.2)
        hfr = T("Hfr", 32, ORANGE).move_to([-3.15, -2.25, 0])
        self.at("the cell is HFR")
        self.play(FadeIn(hfr), run_time=0.6)
        strip = Line([-4.15, 0, 0], [4.15, 0, 0], color=TEXT, stroke_width=7)
        origin = Dot([-3.65, 0, 0], radius=0.15, color=ORANGE)
        direction = Arrow([-3.45, 0.35, 0], [-2.5, 0.35, 0], buff=0, color=ORANGE, stroke_width=6, tip_length=0.22)
        self.at("Transfer now pulls")
        self.play(ReplacementTransform(VGroup(chrom, embedded), strip), FadeIn(origin), GrowArrow(direction), run_time=1.1)
        markers = VGroup(*[Dot([-3.0 + i * 0.72, 0, 0], radius=0.14, color=GOLD) for i in range(4)])
        self.add(markers)
        self.play(*[m.animate.shift(RIGHT * (4.5 - i * 0.25)) for i, m in enumerate(markers)], run_time=2.0, rate_func=linear)
        self.at("Because pairs usually separate")
        pair[0].clear_updaters()
        pair[1].clear_updaters()
        self.play(pair[2].animate.set_opacity(0), pair[0].animate.shift(LEFT * 0.5), pair[1].animate.shift(RIGHT * 0.5), run_time=1.1)
        self.at("recipients receive only")
        bob(pair[0], amp=0.10, speed=2.0)
        bob(pair[1], amp=0.10, speed=2.3, seed=2)
        partial = caption("only part arrives", color=GOLD)
        self.play(FadeIn(partial), run_time=0.7)
        self.at("The remaining F sequence")
        self.play(Indicate(origin, color=ORANGE), run_time=1.2)
        self.finish()


class S09Timeline(SpokenScene):
    def construct(self):
        rows = VGroup()
        for y in (2.15, 1.25, 0.35, -0.55):
            donor = bacterium([-4.9, y, 0], TEAL, 1.35, 0.65)
            rec = bacterium([-2.7, y, 0], LIGHT_GREY, 1.35, 0.65)
            bridge = Line(donor.get_right(), rec.get_left(), color=GREY, stroke_width=4)
            rows.add(VGroup(donor, rec, bridge))
        bob(rows, amp=0.045, speed=1.8)
        self.play(FadeIn(rows), run_time=0.8)
        bar = Line([-1.55, 2.7, 0], [-1.55, -1.05, 0], color=RED, stroke_width=10)
        self.at("Break different pairs")
        self.play(bar.animate.shift(RIGHT * 1.0), run_time=1.4, rate_func=linear)
        self.play(*[r[2].animate.set_opacity(0) for r in rows], run_time=0.7)
        timeline = marker_timeline(-1.75)
        pulse(timeline[0], base=5.0, amp=1.4, speed=2.1)
        for i, mark in enumerate(timeline[1]):
            bob(mark, amp=0.09, speed=1.9 + 0.12 * i, seed=i)
        self.at("then score the recipients")
        self.play(FadeOut(rows), FadeIn(timeline[0]), run_time=0.6)
        self.at("Markers nearer the origin")
        for mark in timeline[1]:
            self.play(FadeIn(mark), run_time=0.35)
        self.at("With steady transfer")
        self.play(FadeIn(timeline[2]), run_time=1.2)
        plate = Ellipse(width=2.2, height=0.9, color=GREY, stroke_width=3,
                        fill_color=GREY, fill_opacity=0.08).move_to([4.8, 1.75, 0])
        bob(plate, amp=0.10, speed=2.1)
        colonies = VGroup(*[Dot([4.35 + 0.25 * i, 1.75 + 0.12 * ((i % 2) * 2 - 1), 0], radius=0.09, color=GOLD) for i in range(5)])
        self.at("Selective plates reveal")
        self.play(FadeIn(plate), LaggedStart(*[GrowFromCenter(c) for c in colonies], lag_ratio=0.15), run_time=1.2)
        self.at("A marker's entry time")
        sweep = Line([-5.4, 2.65, 0], [-5.4, -0.55, 0], color=RED, stroke_width=7)
        self.play(sweep.animate.shift(RIGHT * 3.6), run_time=2.0, rate_func=linear)
        self.play(Indicate(timeline[1][0], color=GOLD), run_time=0.8)
        self.finish()


class S10Reverse(SpokenScene):
    def construct(self):
        c = np.array([0, 0.15, 0])
        ring = chromosome(c, 2.55, TEXT, 7)
        pulse(ring, base=7.0, amp=2.2, speed=2.0)
        bob(ring, amp=0.11, speed=2.1)
        angles = (145, 55, -25, -125)
        marks = VGroup(*[Dot(c + 2.55 * np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0]), radius=0.15, color=GOLD) for a in angles])
        origin = Dot(c + LEFT * 2.55, radius=0.18, color=ORANGE)
        arrow1 = CurvedArrow(c + np.array([-2.2, -1.25, 0]), c + np.array([-1.35, -2.1, 0]), angle=0.5, color=ORANGE, stroke_width=6)
        self.add(ring, marks, origin, arrow1)
        self.at("A different HFR origin")
        origin2 = Dot(c + RIGHT * 2.55, radius=0.18, color=ORANGE)
        arrow2 = CurvedArrow(c + np.array([2.2, 1.25, 0]), c + np.array([1.35, 2.1, 0]), angle=0.5, color=ORANGE, stroke_width=6)
        self.play(ReplacementTransform(origin, origin2), ReplacementTransform(arrow1, arrow2), run_time=1.3)
        self.play(Rotate(marks, angle=PI, about_point=c), run_time=1.5)
        self.at("Absolute arrival times change")
        clocks = VGroup(M("start", 28, GREY), M("different start", 28, GREY)).arrange(DOWN, buff=0.25).move_to([4.6, -2.4, 0])
        self.play(FadeIn(clocks), run_time=0.8)
        self.at("but matching gaps")
        arcs = VGroup(*[
            Arc(radius=2.9, start_angle=a * DEGREES, angle=-0.72, arc_center=c, color=GOLD, stroke_width=5)
            for a in (155, 65, -25)
        ])
        self.play(Create(arcs), run_time=1.2)
        self.at("The origin sets")
        self.play(Indicate(origin2, color=ORANGE), run_time=1.0)
        self.at("so absolute times cannot")
        self.play(FadeOut(clocks), Indicate(arcs, color=GOLD), run_time=1.1)
        self.finish()


class S11Readout(SpokenScene):
    def construct(self):
        plate = Ellipse(width=8.8, height=5.2, color=GREY, stroke_width=4,
                        fill_color=GREY, fill_opacity=0.16).move_to([0, -0.15, 0])
        pulse(plate, base=4.0, amp=1.3, speed=2.0)
        bob(plate, amp=0.10, speed=2.1)
        cells = VGroup(*[
            Dot([x, y, 0], radius=0.12, color=LIGHT_GREY)
            for x, y in [(-3, 1), (-2.1, -1.4), (-0.8, 0.7), (0.7, -1), (2, 1.25), (3, -0.4)]
        ])
        self.play(FadeIn(plate), FadeIn(cells), run_time=0.9)
        self.at("Selection makes rare")
        survivors = VGroup(cells[1], cells[4])
        self.play(*[FadeOut(c) for c in [cells[0], cells[2], cells[3], cells[5]]],
                  *[s.animate.scale(2.2) for s in survivors], run_time=1.2)
        chain = VGroup(
            chip("entry", GOLD, 28), chip("integration", ORANGE, 28), chip("expression", TEAL, 28)
        ).arrange(RIGHT, buff=0.65).move_to([0, 3.05, 0])
        arrows = VGroup(*[
            Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.1, color=GREY, stroke_width=4, tip_length=0.18)
            for i in range(2)
        ])
        self.at("but a colony reports")
        self.play(FadeIn(chain[0]), run_time=0.6)
        self.at("The donor piece must")
        self.play(GrowArrow(arrows[0]), FadeIn(chain[1]), run_time=0.8)
        self.play(GrowArrow(arrows[1]), FadeIn(chain[2]), run_time=0.8)
        chrom = chromosome([0, -0.55, 0], 1.2, TEXT, 6)
        donor_piece = Line([-0.5, -1.72, 0], [0.5, -1.72, 0], color=GOLD, stroke_width=9)
        self.add(chrom, donor_piece)
        self.at("Incoming linear DNA")
        self.play(donor_piece.animate.move_to([0, -1.67, 0]), run_time=1.0)
        self.at("Recombination can replace")
        integrated = Arc(radius=1.2, start_angle=-2.0, angle=0.85, arc_center=[0, -0.55, 0], color=GOLD, stroke_width=9)
        self.play(ReplacementTransform(donor_piece, integrated), Indicate(chain[1], color=ORANGE), run_time=1.3)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        pair = cell_pair()
        pulse(pair[0], base=5.0, amp=1.5, speed=2.0)
        pulse(pair[1], base=5.0, amp=1.5, speed=2.4)
        strip = Line([-3.8, 0, 0], [3.8, 0, 0], color=TEXT, stroke_width=7)
        markers = VGroup(*[Dot([-2.8 + i * 1.35, 0, 0], radius=0.15, color=GOLD) for i in range(4)])
        self.add(pair, strip, markers)
        self.at("The route created")
        self.play(*[m.animate.shift(RIGHT * 1.2) for m in markers], run_time=1.1, rate_func=linear)
        timeline = marker_timeline(-0.1)
        pulse(timeline[0], base=5.0, amp=1.5, speed=2.2)
        self.at("For HFR transfer")
        self.play(FadeOut(pair), ReplacementTransform(strip, timeline[0]),
                  ReplacementTransform(markers, timeline[1]), run_time=1.2)
        self.at("ordered arrival maps")
        self.play(Indicate(timeline[1], color=GOLD), run_time=1.0)
        self.at("If transfer is roughly")
        self.play(FadeIn(timeline[2]), run_time=1.0)
        self.at("time gaps also map")
        self.play(Indicate(timeline[2], color=GOLD), run_time=1.1)
        self.at("Keep the gaps")
        final = caption("Keep the gaps, not the starting values.", color=GOLD)
        self.play(FadeIn(final), run_time=0.7)
        self.play(Indicate(timeline[2], color=GOLD), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "Ordered arrival maps gene order; time gaps map distance."
