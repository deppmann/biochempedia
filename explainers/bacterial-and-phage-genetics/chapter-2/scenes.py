"""When Genes Share a Phage — chapter 2.

COLOR MAP (shared with chapter 1's script and used throughout this film)
  GOLD       donor DNA and donor markers
  LIGHT_GREY recipient bacteria
  TEAL       donor bacteria
  PURPLE     phage coats and fixed-width sampling windows
  ORANGE     F factor (retained for continuity; not introduced in this chapter)
  WHITE      recipient/host chromosome
  BLUE       cell-blocking filter and the scored second marker
  RED        DNase

Chromosomes are schematic tracks, never molecular structures.  Every sampling window and
qualitative bar is explicitly marked schematic; the film makes no numerical claim.
"""
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
LIGHT_GREY = "#B9BEC8"
WHITE = TEXT


def heading(text, color=TEXT):
    return fit_text(text, max_w=11.8, size=38, color=color, font=TITLE_FONT).move_to([0, 3.28, 0])


def float_y(mob, amp=0.11, speed=1.5, seed=0.0):
    """Shift a carried subject gently without fighting its horizontal teaching animations."""
    mob._float_t = seed
    mob._float_last = amp * np.sin(speed * seed)

    def update(m, dt):
        m._float_t += dt
        now = amp * np.sin(speed * m._float_t)
        m.shift(UP * (now - m._float_last))
        m._float_last = now
    return mob.add_updater(update)


def float_x(mob, amp=0.11, speed=1.5, seed=0.0):
    """Horizontal counterpart for a qualitative bar that must not imply a height change."""
    mob._float_x_t = seed
    mob._float_x_last = amp * np.sin(speed * seed)

    def update(m, dt):
        m._float_x_t += dt
        now = amp * np.sin(speed * m._float_x_t)
        m.shift(RIGHT * (now - m._float_x_last))
        m._float_x_last = now
    return mob.add_updater(update)


def bacterium(center, color=LIGHT_GREY, width=2.55, height=1.55):
    """The cell silhouette used everywhere in this chapter."""
    return RoundedRectangle(corner_radius=0.7, width=width, height=height,
                            stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.28).move_to(center)


def phage(center, scale=1.0, cargo=True):
    """A labelled-cartoon phage coat; not a molecular drawing."""
    x, y = center[:2]
    head = RegularPolygon(6, radius=0.52 * scale, color=PURPLE, stroke_width=4,
                          fill_color=PURPLE, fill_opacity=0.14).move_to([x, y + 0.35 * scale, 0])
    tail = Line([x, y - 0.1 * scale, 0], [x, y - 0.78 * scale, 0], color=PURPLE, stroke_width=5)
    feet = VGroup(Line([x, y - 0.76 * scale, 0], [x - 0.35 * scale, y - 1.02 * scale, 0], color=PURPLE, stroke_width=4),
                  Line([x, y - 0.76 * scale, 0], [x + 0.35 * scale, y - 1.02 * scale, 0], color=PURPLE, stroke_width=4))
    g = VGroup(head, tail, feet)
    if cargo:
        g.add(Line([x - 0.27 * scale, y + 0.35 * scale, 0], [x + 0.27 * scale, y + 0.35 * scale, 0],
                   color=GOLD, stroke_width=8 * scale))
    return g


def circle_map(center=(0, -0.15, 0), radius=2.35, markers=(-0.55, 0.25, 1.2)):
    """The carried white chromosome map from the opening and map comparison."""
    ring = Circle(radius=radius, color=WHITE, stroke_width=7).move_to(center)
    dots = VGroup()
    for a in markers:
        p = ring.point_at_angle(a)
        dots.add(RoundedRectangle(width=0.42, height=0.18, corner_radius=0.05,
                                  color=GOLD, fill_color=GOLD, fill_opacity=1).move_to(p))
    return VGroup(ring, dots)


def filter_bar(x=0.0):
    bar = RoundedRectangle(width=0.42, height=5.1, corner_radius=0.16,
                           color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.15).move_to([x, 0, 0])
    pores = VGroup(*[Dot([x, y, 0], radius=0.055, color=BLUE) for y in np.linspace(-2, 2, 7)])
    return VGroup(bar, pores)


def sampling_track(pair=(-1.0, 0.0), window_x=-0.5, bar_height=None, labels=True):
    """The single generalized-transduction world, rebuilt without positional drift."""
    bed = RoundedRectangle(width=8.85, height=1.8, corner_radius=0.32, stroke_width=0,
                           fill_color=WHITE, fill_opacity=0.16).move_to([-1.275, 0.25, 0])
    track = Line([-5.7, 0.25, 0], [3.15, 0.25, 0], color=WHITE, stroke_width=8)
    ends = VGroup(*[Line([x, 0.08, 0], [x, 0.42, 0], color=WHITE, stroke_width=5) for x in (-5.7, 3.15)])
    genes = VGroup(*[RoundedRectangle(width=0.42, height=0.48, corner_radius=0.07,
                                      stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                                      fill_opacity=0.9).move_to([x, 0.25, 0]) for x in pair])
    window = RoundedRectangle(width=2.45, height=1.25, corner_radius=0.2,
                              color=PURPLE, stroke_width=5, fill_color=PURPLE,
                              fill_opacity=0.25).move_to([window_x, 0.25, 0])
    g = VGroup(bed, track, ends, genes, window)
    g.track, g.genes, g.window = track, genes, window
    if labels:
        lab = T("host fragment window", 28, PURPLE).move_to([-1.3, 1.7, 0])
        g.add(lab)
        g.label = lab
    if bar_height is not None:
        base_y, max_h = -2.4, 3.7
        frame = RoundedRectangle(width=1.65, height=max_h, corner_radius=0.15,
                                 color=GREY, stroke_width=2).move_to([5.0, base_y + max_h / 2, 0])
        bar = Rectangle(width=0.9, height=bar_height, stroke_width=0,
                        fill_color=GOLD, fill_opacity=0.9).move_to([5.0, base_y + bar_height / 2, 0])
        bl = T("shared\ncarriage", 26, GOLD, line_spacing=0.8).move_to([5.0, -2.95, 0])
        g.add(frame, bar, bl)
        g.bar = bar
    return g


def predict_world(covered=True):
    """Exact shared frame for s06, s07 and the opening of s08."""
    line1 = Line([-5.8, 1.25, 0], [-1.2, 1.25, 0], color=WHITE, stroke_width=7)
    line2 = Line([-5.8, -1.0, 0], [-1.2, -1.0, 0], color=WHITE, stroke_width=7)
    close = VGroup(*[Dot([x, 1.25, 0], radius=0.15, color=GOLD) for x in (-4.0, -3.25)])
    wide = VGroup(*[Dot([x, -1.0, 0], radius=0.15, color=GOLD) for x in (-4.7, -2.5)])
    covers = VGroup(*[RoundedRectangle(width=4.85, height=1.5, corner_radius=0.15,
                                       color=GREY, fill_color=GREY, fill_opacity=0.24).move_to([-3.5, y, 0])
                      for y in (1.37, -0.88)])
    labels = VGroup(T("pair A", 28, TEXT).move_to([-3.5, 1.66, 0]),
                    T("pair B", 28, TEXT).move_to([-3.5, -0.59, 0]))
    base = -2.25
    bars = VGroup(Rectangle(width=0.9, height=3.8, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([2.35, base + 1.9, 0]),
                  Rectangle(width=0.9, height=1.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([4.45, base + 0.75, 0]))
    bar_labels = VGroup(T("A", 28, TEXT).move_to([2.35, -2.62, 0]), T("B", 28, TEXT).move_to([4.45, -2.62, 0]),
                        T("shared carriage", 28, GOLD).move_to([3.4, 2.35, 0]))
    g = VGroup(line1, line2, close, wide, bars, bar_labels)
    g.lines, g.pairs, g.bars = VGroup(line1, line2), VGroup(close, wide), bars
    if covered:
        g.add(covers, labels)
        g.covers, g.pair_labels = covers, labels
    return g


def moving_windows(y, positions, width=2.45):
    return VGroup(*[RoundedRectangle(width=width, height=0.88, corner_radius=0.14,
                                     color=PURPLE, stroke_width=3, fill_color=PURPLE,
                                     fill_opacity=0.06).move_to([x, y, 0]) for x in positions])


class S00LinkHook(SpokenScene):
    def construct(self):
        world = circle_map()
        self.play(Create(world[0]), FadeIn(world[1]), run_time=0.9)
        self.at("How can a phage")
        phages = VGroup(*[phage([-4.9, y, 0], 0.72) for y in (1.7, 0.15, -1.45)])
        recipient = bacterium([3.8, -0.15, 0], width=3.0, height=2.4)
        q = fit_text("How can a phage reveal which genes sit close together?", max_w=11.8,
                     size=34, color=GOLD).move_to([0, 3.2, 0])
        self.play(world.animate.scale(0.72).move_to([3.8, -0.15, 0]), FadeIn(recipient),
                  FadeIn(phages, shift=RIGHT * 0.2), FadeIn(q), run_time=1.1)
        self.at("Keep following gold")
        for p in phages:
            self.play(p.animate.shift(RIGHT * 1.05), run_time=0.48)
        self.at("The carrier has changed")
        readout = T("carrier changes → readout changes", 30, PURPLE).move_to([0, -2.65, 0])
        self.play(FadeIn(readout), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.play(phages.animate.shift(RIGHT * 0.55), run_time=1.2, rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Bacterial and phage genetics"
    TITLE = "When Genes Share a Phage"


class S02EvidenceAndGeneralized(SpokenScene):
    def construct(self):
        donor = bacterium([-4.7, 0, 0], TEAL, 2.7, 2.2)
        recipient = bacterium([4.7, 0, 0], LIGHT_GREY, 2.7, 2.2)
        ph = phage([-2.8, 1.3, 0], 0.75)
        filt = filter_bar(0)
        self.play(FadeIn(donor), FadeIn(recipient), FadeIn(ph), run_time=0.7)
        self.at("cross a cell blocking filter")
        self.play(FadeIn(filt), ph.animate.move_to([2.7, 1.3, 0]), run_time=1.1)
        self.play(donor.animate.shift(RIGHT * 1.3), run_time=0.7)
        self.at("protected from")
        dn = T("DNase", 30, RED).move_to([1.25, 3.05, 0])
        sweep = Line([-5.8, 2.15, 0], [5.8, 2.15, 0], color=RED, stroke_width=10)
        self.play(FadeIn(dn), Create(sweep), run_time=0.8)
        self.play(sweep.animate.shift(DOWN * 3.8), run_time=1.0)
        self.at("In generalized transduction")
        self.play(FadeOut(VGroup(donor, recipient, filt, sweep, dn, ph)), run_time=0.5)
        chromosome = Line([-5.7, 0, 0], [5.7, 0, 0], color=WHITE, stroke_width=9)
        chromosome_bed = RoundedRectangle(width=11.4, height=1.8, corner_radius=0.32,
                                           stroke_width=0, fill_color=WHITE, fill_opacity=0.16)
        window = RoundedRectangle(width=2.5, height=1.35, corner_radius=0.2, color=PURPLE,
                                  stroke_width=5, fill_color=PURPLE, fill_opacity=0.1).move_to([-4.0, 0, 0])
        float_y(window)
        self.play(FadeIn(chromosome_bed), Create(chromosome), FadeIn(window), run_time=0.8)
        self.at("sometimes packages host")
        cargo = Line([-4.85, 0, 0], [-3.15, 0, 0], color=GOLD, stroke_width=10)
        self.play(Create(cargo), run_time=0.6)
        self.play(VGroup(window, cargo).animate.move_to([0, 1.7, 0]).scale(0.75), run_time=0.8)
        self.at("Any host region")
        samples = VGroup()
        for x in (-3.6, -0.7, 2.7):
            w = window.copy().scale(0.8).move_to([x, 0, 0])
            samples.add(w)
            self.play(FadeIn(w), run_time=0.42)
        self.at("The coat reveals")
        coat = phage([4.8, 2.0, 0], 0.8)
        self.play(ReplacementTransform(VGroup(window, cargo), coat), run_time=0.8)
        self.at("The host fragment creates")
        self.play(Indicate(coat[-1], color=GOLD, scale_factor=1.25), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S03GeneralizedHosts(SpokenScene):
    def construct(self):
        world = sampling_track(pair=(-1.0, 0.0), window_x=-0.5)
        float_y(world.window)
        carrier = phage([4.7, 1.8, 0], 0.72)
        self.add(world, carrier, scope_tag("schematic"))
        salmonella = chip("Salmonella: P22", TEAL, size=30).move_to([0, 2.8, 0])
        self.play(FadeIn(salmonella), run_time=0.6)
        self.at("P1 does this")
        ecoli = chip("E. coli: P1", TEAL, size=30).move_to(salmonella)
        self.play(swap(salmonella, ecoli), world.window.animate.shift(RIGHT * 1.2), run_time=0.9)
        self.at("Each transducing particle")
        short = Line([-0.2, 0.25, 0], [1.5, 0.25, 0], color=GOLD, stroke_width=10)
        self.play(Create(short), carrier.animate.shift(LEFT * 0.5), run_time=0.8)
        self.at("only a limited")
        self.play(TransformFromCopy(short, carrier[-1]), world.window.animate.shift(LEFT * 2.2), run_time=0.9)
        self.at("a short window")
        whole = Brace(world.track, DOWN, color=WHITE)
        short_brace = Brace(world.window, UP, color=PURPLE)
        self.play(GrowFromCenter(whole), GrowFromCenter(short_brace), run_time=0.8)
        self.at("not the whole")
        self.play(Indicate(world.window, color=PURPLE), Indicate(world.track, color=WHITE), run_time=0.9)
        self.finish()


class S04Specialized(SpokenScene):
    def construct(self):
        self.play(FadeIn(heading("Specialized transduction", PURPLE)), run_time=0.6)
        track_bed = RoundedRectangle(width=11.4, height=1.45, corner_radius=0.28, stroke_width=0,
                                     fill_color=WHITE, fill_opacity=0.16)
        float_y(track_bed, amp=0.08, speed=1.3)
        track = Line([-5.7, 0, 0], [5.7, 0, 0], color=WHITE, stroke_width=9)
        blocks = VGroup(chip("distant", WHITE, 28).move_to([-4.6, 0.65, 0]),
                        chip("gal", WHITE, 30).move_to([-1.65, 0.65, 0]),
                        chip("lambda", PURPLE, 30).move_to([0, 0.65, 0]),
                        chip("bio", WHITE, 30).move_to([1.65, 0.65, 0]),
                        chip("distant", WHITE, 28).move_to([4.6, 0.65, 0]))
        for b in blocks:
            b[0].set_fill(BG, opacity=1)
        self.at("Lambda inserts")
        self.play(FadeIn(track_bed), Create(track), FadeIn(blocks[1]), FadeIn(blocks[3]), run_time=0.7)
        self.play(FadeIn(blocks[2], shift=DOWN * 0.3), run_time=0.6)
        site = T("preferred site", 28, PURPLE).next_to(blocks[2], UP, buff=0.4)
        self.play(FadeIn(site), run_time=0.5)
        self.at("Inaccurate removal")
        self.play(FadeIn(blocks[0]), FadeIn(blocks[4]), run_time=0.5)
        lifted = VGroup(blocks[2], blocks[3])
        self.play(FadeOut(site), run_time=0.25)
        self.play(lifted.animate.shift(UP * 1.65), run_time=0.75)
        float_y(lifted, amp=0.13, speed=1.35)
        self.at("only neighbouring")
        blocks[3][0].set_stroke(GOLD)
        blocks[3][1].set_color(GOLD)
        self.play(Indicate(blocks[3], color=GOLD), run_time=0.8)
        self.at("not random sampling")
        fixed = T("one fixed attachment site", 30, PURPLE).move_to([0, -1.55, 0])
        self.play(FadeIn(fixed), run_time=0.7)
        self.at("position matters")
        site_marker = Dot([0, 0, 0], radius=0.16, color=PURPLE)
        self.play(FadeIn(site_marker), lifted.animate.shift(LEFT * 0.25), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S05SharedWindow(SpokenScene):
    def construct(self):
        world = sampling_track(pair=(-1.0, -0.15), window_x=-1.8)
        float_y(world.window)
        self.play(FadeIn(world), FadeIn(heading("Generalized transduction", PURPLE)), run_time=0.7)
        self.at("Two genes can share")
        self.play(world.window.animate.move_to([-0.55, 0.25, 0]), run_time=1.0)
        self.at("only when one host fragment")
        self.play(Indicate(world.genes, color=GOLD), run_time=0.7)
        self.at("Closer markers")
        close_positions = [-1.2, -0.65, -0.1, 0.45]
        close_windows = moving_windows(0.25, close_positions)
        self.play(FadeIn(close_windows, lag_ratio=0.15), run_time=1.0)
        self.at("more possible windows")
        self.play(close_windows.animate.set_opacity(0.35), run_time=0.8)
        self.at("Move the window")
        self.play(FadeOut(close_windows), world.genes[0].animate.move_to([-2.0, 0.25, 0]),
                  world.genes[1].animate.move_to([0.8, 0.25, 0]), run_time=0.8)
        self.play(world.window.animate.move_to([-0.6, 0.25, 0]), run_time=0.8)
        self.play(world.window.animate.move_to([-1.4, 0.25, 0]), run_time=0.7)
        self.at("both markers remain")
        self.play(world.window.animate.move_to([-0.6, 0.25, 0]), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        w = predict_world(True)
        self.play(FadeIn(w.lines), FadeIn(w.covers), FadeIn(w.pair_labels), run_time=0.7)
        self.at("One bar is high")
        self.play(GrowFromEdge(w.bars[0], DOWN), run_time=0.8)
        self.at("one is low")
        self.play(GrowFromEdge(w.bars[1], DOWN), FadeIn(w[-3]), run_time=0.7)
        self.at("Which pair lies closer")
        q = question_card("Which pair is closer?", ["pair A", "pair B"], y=-3.18, max_w=7.6)
        self.play(FadeIn(q), run_time=0.8)
        self.at("Compare only the bars")
        self.play(Indicate(w.bars, color=GOLD), run_time=0.8)
        self.at("do not infer direction")
        self.play(w.covers.animate.set_stroke(PURPLE, width=3), run_time=0.8)
        self.finish()


class S07Pause(PredictPause):
    QUESTION = "Which pair is closer?"
    OPTIONS = ["pair A", "pair B"]
    SECONDS = 4.5
    CARD = {"y": -3.18, "max_w": 7.6}

    def backdrop(self):
        w = predict_world(True)
        ghost = moving_windows(0.12, [-4.6, -3.1, -1.6], width=1.5).set_opacity(0.22)
        return VGroup(ghost, w)


class S08Reveal(SpokenScene):
    def construct(self):
        covered = predict_world(True)
        ghost = RoundedRectangle(width=1.75, height=0.88, corner_radius=0.14,
                                 color=PURPLE, stroke_width=5, fill_color=PURPLE,
                                 fill_opacity=0.12).move_to([0, 0, 0])
        float_y(ghost, amp=0.13, speed=1.4)
        self.add(ghost, covered, scope_tag("schematic"))
        self.at("higher shared carriage")
        self.play(FadeOut(covered.covers), FadeOut(covered.pair_labels), run_time=0.8)
        answer = T("higher bar → closer pair", 32, GOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(answer), Indicate(covered.pairs[0], color=GOLD), run_time=0.8)
        self.at("More fragment positions")
        close_w = moving_windows(1.25, [-4.2, -3.7, -3.2], width=1.75)
        self.play(LaggedStart(*[FadeIn(x) for x in close_w], lag_ratio=0.18), run_time=1.0)
        self.at("more particles deliver")
        phages = VGroup(*[phage([x, -0.15, 0], 0.38) for x in (-0.6, 0.2, 1.0)])
        self.play(FadeIn(phages, shift=RIGHT * 0.15), run_time=0.8)
        self.at("The bar summarizes")
        self.play(Indicate(covered.bars[0], color=GOLD), phages.animate.shift(RIGHT * 0.4), run_time=0.9)
        self.at("not one specially")
        self.play(FadeOut(phages[0]), FadeOut(phages[1]), FadeOut(phages[2]),
                  close_w.animate.set_opacity(0.2), run_time=0.8)
        self.finish()


class S09Frequency(SpokenScene):
    def construct(self):
        ph = phage([-5.5, 2.1, 0], 0.55)
        cells = VGroup(*[bacterium([x, y, 0], LIGHT_GREY, 1.45, 0.85)
                         for x, y in [(-3.7, 1.5), (-1.6, 1.5), (0.5, 1.5), (2.6, 1.5),
                                      (-2.65, -0.1), (-0.55, -0.1), (1.55, -0.1), (3.65, -0.1)]])
        self.play(FadeIn(ph), FadeIn(cells, lag_ratio=0.08), run_time=0.8)
        self.at("gained one donor marker")
        first = VGroup(*[Dot(c.get_center(), radius=0.12, color=GOLD) for c in cells])
        self.play(FadeIn(first, lag_ratio=0.06), ph.animate.shift(RIGHT * 1.0), run_time=0.9)
        self.at("Then they score")
        plate = Ellipse(width=11.2, height=4.0, color=GREY, stroke_width=4,
                        fill_color=GREY, fill_opacity=0.22).move_to([0, 0.65, 0])
        self.play(FadeIn(plate), run_time=0.6)
        self.at("also gained another")
        second = VGroup(*[Circle(radius=0.21, color=BLUE, stroke_width=4).move_to(cells[i].get_center()) for i in (1, 4, 6)])
        self.play(FadeIn(second, lag_ratio=0.2), run_time=0.8)
        self.at("That fraction is")
        subset = SurroundingRectangle(VGroup(cells[1], cells[4], cells[6]), color=BLUE, buff=0.25)
        label = fit_text("cotransduction frequency", max_w=5.4, size=34, color=BLUE).move_to([0, -2.35, 0])
        self.play(Create(subset), FadeIn(label), run_time=0.9)
        self.at("Selection defines the denominator")
        denom = T("selected-marker recipients", 28, GOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(denom), Indicate(first, color=GOLD), run_time=0.9)
        self.at("before the second marker")
        self.play(Indicate(second, color=BLUE), run_time=0.8)
        self.finish()


class S10OrderLimit(SpokenScene):
    def construct(self):
        bed = RoundedRectangle(width=10.8, height=1.15, corner_radius=0.25, stroke_width=0,
                               fill_color=WHITE, fill_opacity=0.16).move_to([0, 0.4, 0])
        line = Line([-5.4, 0.4, 0], [5.4, 0.4, 0], color=WHITE, stroke_width=8)
        selected = chip("selected", GOLD, 30).move_to([0, 1.05, 0])
        selected[0].set_fill(BG, opacity=1)
        other = chip("second", BLUE, 30).move_to([-2.4, 1.05, 0])
        other[0].set_fill(BG, opacity=1)
        bar = Rectangle(width=1.0, height=2.4, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([4.5, 1.65, 0])
        float_x(bar, amp=0.13, speed=1.35)
        self.play(FadeIn(bed), Create(line), FadeIn(selected), FadeIn(other), GrowFromEdge(bar, DOWN), run_time=0.9)
        self.at("cannot place genes left or right")
        other_right = chip("second", BLUE, 30).move_to([2.4, 1.05, 0])
        other_right[0].set_fill(BG, opacity=1)
        self.play(swap(other, other_right, run_time=1.2), run_time=1.2)
        other = other_right
        self.at("Three factor classes")
        third = chip("third", PURPLE, 30).move_to([-2.4, 1.05, 0])
        third[0].set_fill(BG, opacity=1)
        self.play(FadeIn(third), run_time=0.6)
        cards = VGroup(*[chip(t, GREY, 26) for t in ("class 1", "class 2", "class 3", "class 4")]).arrange(RIGHT, buff=0.25).move_to([0, -1.65, 0])
        self.play(FadeOut(VGroup(bed, line, selected, other, third)), run_time=0.35)
        self.play(FadeIn(cards), run_time=0.65)
        self.at("The same proximity")
        q = T("Which class reveals the order?", 32, PURPLE).move_to([0, 2.8, 0])
        self.play(FadeIn(q), bar.animate.shift(LEFT * 0.15), run_time=0.8)
        self.at("either side")
        self.play(cards.animate.set_color(TEXT), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S11Recovery(SpokenScene):
    def construct(self):
        cell = bacterium([1.4, 0, 0], LIGHT_GREY, 8.5, 5.0)
        float_y(cell, amp=0.07, speed=1.3)
        chrom = Line([-1.8, -0.55, 0], [4.5, -0.55, 0], color=WHITE, stroke_width=9)
        ph = phage([-4.8, 1.6, 0], 0.72)
        float_y(ph, amp=0.16, speed=1.35)
        frag = Line([-4.0, 0.75, 0], [-2.5, 0.75, 0], color=GOLD, stroke_width=10)
        self.play(FadeIn(cell), Create(chrom), FadeIn(ph), run_time=0.8)
        self.at("must enter")
        self.play(TransformFromCopy(ph[-1], frag), run_time=0.7)
        self.play(frag.animate.shift(RIGHT * 2.2), run_time=0.8)
        entry = chip("entry", PURPLE, 28).move_to([-4.7, -3.05, 0])
        self.play(FadeIn(entry), run_time=0.5)
        self.at("be expressed")
        expression = chip("expression", BLUE, 28).move_to([0, -3.05, 0])
        glow = SurroundingRectangle(frag, color=BLUE, buff=0.18)
        self.play(FadeIn(expression), Create(glow), run_time=0.7)
        self.at("For stable inheritance")
        integration = chip("stable integration", GOLD, 28).move_to([4.4, -3.05, 0])
        self.play(FadeIn(integration), frag.animate.move_to([1.0, -0.55, 0]), FadeOut(glow), run_time=0.9)
        self.at("recombine into")
        joins = VGroup(*[Line([x - 0.18, -0.82, 0], [x + 0.18, -0.28, 0], color=GOLD, stroke_width=5) for x in (0.25, 1.75)])
        self.play(Create(joins), run_time=0.7)
        self.at("A colony combines")
        chain = VGroup(entry, expression, integration)
        arrows = VGroup(Arrow(entry.get_right(), expression.get_left(), color=GREY, buff=0.12, tip_length=0.18),
                        Arrow(expression.get_right(), integration.get_left(), color=GREY, buff=0.12, tip_length=0.18))
        self.play(FadeIn(arrows), Indicate(chain, color=GOLD), run_time=0.9)
        self.at("survival under selection")
        colony = Circle(radius=0.55, color=GREEN, fill_color=GREEN, fill_opacity=0.22).move_to([4.8, 1.8, 0])
        self.play(GrowFromCenter(colony), ph.animate.shift(UP * 0.15), run_time=0.9)
        self.finish()


class S12TwoMaps(SpokenScene):
    def construct(self):
        panels = TwoPanel("interrupted mating", "cotransduction", colors=(TEAL, PURPLE), top=3.0, bottom=-2.35)
        self.play(FadeIn(panels), run_time=0.6)
        circle = circle_map(center=(-3.25, 0.15, 0), radius=1.65)
        timeline = Arc(radius=1.85, start_angle=0.2, angle=5.6, arc_center=[-3.25, 0.15, 0], color=GOLD, stroke_width=5)
        self.at("long chromosome stretches")
        self.play(Create(circle[0]), FadeIn(circle[1]), Create(timeline), run_time=1.0)
        self.at("Catransduction resolves")
        track = Line([0.8, 0.15, 0], [5.7, 0.15, 0], color=WHITE, stroke_width=7)
        pair = VGroup(Dot([2.2, 0.15, 0], radius=0.14, color=GOLD), Dot([2.95, 0.15, 0], radius=0.14, color=GOLD))
        win = RoundedRectangle(width=1.8, height=1.1, corner_radius=0.16, color=PURPLE, stroke_width=4).move_to([2.55, 0.15, 0])
        float_y(win, amp=0.13, speed=1.4)
        bar = Rectangle(width=0.7, height=1.65, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([5.0, 0.98, 0])
        self.play(Create(track), FadeIn(pair), FadeIn(win), GrowFromEdge(bar, DOWN), run_time=1.0)
        self.at("Each root creates")
        rule = caption("route → readout → map", size=34, color=GOLD, y=-3.1)
        self.play(FadeIn(rule), timeline.animate.rotate(0.35), win.animate.shift(RIGHT * 0.65), run_time=1.0)
        self.at("Neither readout gives")
        note = VGroup(T("not base pairs", 26, GREY).move_to([-3.25, -1.98, 0]),
                      T("not base pairs", 26, GREY).move_to([3.25, -1.98, 0]))
        self.play(FadeIn(note), timeline.animate.rotate(-0.25), win.animate.shift(LEFT * 1.1), run_time=1.0)
        self.at("in this lesson")
        self.play(Indicate(rule, color=GOLD), run_time=0.8)
        self.finish()


class S13Rule(SpokenScene):
    def construct(self):
        world = sampling_track(pair=(-1.0, -0.2), window_x=-0.6, bar_height=0.2)
        float_y(world.window, amp=0.13, speed=1.4)
        float_y(world[0], amp=0.08, speed=1.25)
        title = T("generalized transduction", 32, PURPLE).move_to([0, 3.25, 0])
        self.play(FadeIn(world), FadeIn(title), run_time=0.7)
        self.at("shared carriage maps proximity")
        tall = Rectangle(width=0.9, height=3.4, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([5.0, -2.4 + 1.7, 0])
        self.play(ReplacementTransform(world.bar, tall), world.window.animate.shift(RIGHT * 0.35), run_time=1.0)
        self.at("Closer genes travel")
        self.play(Indicate(world.genes, color=GOLD), run_time=0.8)
        self.at("within the phage's limited load")
        self.play(Indicate(world.window, color=PURPLE), run_time=0.8)
        self.at("Compare markers")
        low = Rectangle(width=0.9, height=1.15, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([5.0, -2.4 + 0.575, 0])
        self.play(world.genes[0].animate.move_to([-2.1, 0.25, 0]), world.genes[1].animate.move_to([0.9, 0.25, 0]),
                  world.window.animate.shift(LEFT * 0.8), ReplacementTransform(tall, low), run_time=1.1)
        self.at("same phage")
        same = T("same phage + conditions", 30, TEAL).move_to([0, -2.55, 0])
        self.play(FadeIn(same), world.window.animate.shift(RIGHT * 0.6), run_time=0.8)
        schematic = T("schematic", 24, GREY).move_to([-5.65, -3.35, 0])
        self.add(schematic)
        self.finish()


class S14End(EndCard):
    LINE = "Shared carriage maps proximity; closer genes travel together more often."
