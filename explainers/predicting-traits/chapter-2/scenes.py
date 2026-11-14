"""Why Real Counts Wander — chapter 2 of Predicting Traits with Punnett Squares.

COLOR MAP (copied exactly from chapter 1)
  PURPLE = the P allele, purple flowers, purple offspring
  WHITE  = the p allele, white flowers, white offspring
  YELLOW = vocabulary words (allele, genotype, phenotype, ratio, probability, Punnett square)
  BLUE   = the Punnett grid, sex cells, gene copies
  GREEN  = chances and predictions (1 in 4, 50 percent, 3 : 1 line)
  GOLD   = Mendel's counted seeds
  RED    = question marks
  GREY   = structure and neutral labels
  TEXT   = plain labels
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B07CFF"
WHITE = "#FFFFFF"

# Fixed, precomputed outcomes: 1 means white and 0 means purple.  The first eight
# lean purple; item nine is the reveal.  Every running-share curve below is
# calculated from these same values.
OUTCOMES = np.array([
    0, 0, 0, 0, 1, 0, 0, 0, 1, 0,
    1, 0, 0, 0, 1, 0, 0, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0,
    1, 0, 0, 0, 1, 0, 0, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0,
    1, 0, 0, 1, 0, 0, 0, 1, 0, 0,
    1, 0, 0, 0, 1, 0, 0, 1, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 0,
], dtype=int)
RUNNING_WHITE = np.cumsum(OUTCOMES) / np.arange(1, len(OUTCOMES) + 1)

MENDEL = [
    ("seed shape", 5474 / 1850),
    ("seed color", 6022 / 2001),
    ("flower color", 705 / 224),
    ("pod shape", 882 / 299),
    ("pod color", 428 / 152),
    ("flower position", 651 / 207),
    ("stem length", 787 / 277),
]


def stage_panel(color=BLUE):
    """The shared chapter landscape: a full, quiet field behind every teaching picture."""
    panel = RoundedRectangle(corner_radius=0.32, width=12.4, height=6.4,
                             stroke_color=color, stroke_width=2,
                             fill_color=color, fill_opacity=0.12).set_z_index(-20)
    # Text is intentionally drawn over this decorative background field.
    panel.layout_ok = True
    return panel


class FilmScene(SpokenScene):
    """Spoken scene with the same full-frame landscape used throughout this chapter."""
    def setup(self):
        super().setup()
        self.add(stage_panel())


def geno(s, size=38):
    return T(s, size, WHITE, weight=BOLD, t2c={"P": PURPLE})


def flower_dot(kind, radius=0.22):
    """The same schematic flower disc used in chapter 1, reduced for a count row."""
    color = WHITE if kind == "white" else PURPLE
    return Circle(radius=radius, stroke_color=color, stroke_width=4,
                  fill_color=color, fill_opacity=0.88)


def grid_at(cx=-3.75, cy=0.35, s=1.25, labels=True, inside_size=34):
    """Chapter 1's Punnett square geometry, rebuilt at one fixed chapter-2 position."""
    cols = [cx - s / 2, cx + s / 2]
    rows = [cy + s / 2, cy - s / 2]
    lines = VGroup(
        Rectangle(width=2 * s, height=2 * s, stroke_color=BLUE, stroke_width=5).move_to([cx, cy, 0]),
        Line([cx, cy + s, 0], [cx, cy - s, 0], color=BLUE, stroke_width=5),
        Line([cx - s, cy, 0], [cx + s, cy, 0], color=BLUE, stroke_width=5),
    )
    cells = [np.array([cols[0], rows[0], 0]), np.array([cols[1], rows[0], 0]),
             np.array([cols[0], rows[1], 0]), np.array([cols[1], rows[1], 0])]
    if not labels:
        return lines, cells
    top = VGroup(geno("P").move_to([cols[0], cy + s + 0.42, 0]),
                 geno("p").move_to([cols[1], cy + s + 0.42, 0]))
    side = VGroup(geno("P").move_to([cx - s - 0.42, rows[0], 0]),
                  geno("p").move_to([cx - s - 0.42, rows[1], 0]))
    inside = VGroup(*[geno(g, inside_size).move_to(c)
                      for g, c in zip(("PP", "Pp", "Pp", "pp"), cells)])
    return VGroup(lines, top, side, inside), cells


def orbit_selector(cells, side=0.6, speed=1.3):
    """A teal selector that loops over all four still-available boxes."""
    sel = RoundedRectangle(corner_radius=0.12, width=side, height=side,
                           stroke_color=TEAL, stroke_width=7,
                           fill_color=TEAL, fill_opacity=0.26).move_to(cells[0])
    # It deliberately encloses (but never obscures) the genotype it selects.
    sel.layout_ok = True
    sel._orbit_t = 0.0

    def move(mob, dt):
        mob._orbit_t += dt * speed
        u = mob._orbit_t % 4
        i = int(u)
        a, b = cells[i], cells[(i + 1) % 4]
        mob.move_to(interpolate(a, b, smooth(u - i)))

    return sel.add_updater(move)


def ratio_scanner(left, right, y=0.0, height=5.5):
    """A moving reading window; the measured ratio dots themselves never move."""
    band = RoundedRectangle(corner_radius=0.18, width=0.62, height=height,
                            stroke_width=0, fill_color=GOLD, fill_opacity=0.16)
    band.set_z_index(-2).move_to([left, y, 0])
    band.layout_ok = True
    band._scan_t = -PI / 2

    def scan(mob, dt):
        mob._scan_t += dt * 1.0
        f = (np.sin(mob._scan_t) + 1) / 2
        mob.move_to([interpolate(left, right, f), y, 0])

    return band.add_updater(scan)


def slot_row(n=8, filled=0, y=-1.65, x0=0.35, gap=0.72, pulse_empty=False):
    """A carried row of outcome slots, identical from the small run through the reveal."""
    slots = VGroup()
    for i in range(n):
        x = x0 + i * gap
        if i < filled:
            slots.add(flower_dot("white" if OUTCOMES[i] else "purple").move_to([x, y, 0]))
        else:
            slots.add(Circle(radius=0.25, stroke_color=GREY, stroke_width=3,
                             fill_opacity=0).move_to([x, y, 0]))
    if pulse_empty:
        for i, m in enumerate(slots[filled:]):
            pulse(m, base=3, amp=1.2, speed=2.0)
            bob(m, amp=0.085, speed=3.0, seed=i)
    return slots


def chance_world(empty=True):
    """The opening picture, rebuilt at exactly the same scale and place."""
    grid, cells = grid_at(inside_size=28)
    row = slot_row(8, 0 if empty else 8, pulse_empty=empty)
    target = VGroup(T("prediction", 28, GOLD, weight=BOLD),
                    M("3 purple : 1 white", 30, GOLD)).arrange(DOWN, buff=0.1)
    target.move_to([3.1, 1.15, 0])
    return grid, cells, row, target


def small_run_world(include_next=True, orbit=True):
    """The carried short-run picture for s04, s05 and s06."""
    grid, cells = grid_at(cx=-4.25, cy=0.55, s=1.15, inside_size=28)
    selector = orbit_selector(cells, side=0.55, speed=1.25) if orbit else RoundedRectangle(
        corner_radius=0.12, width=0.55, height=0.55, stroke_color=TEAL, stroke_width=6).move_to(cells[0])
    row = slot_row(9 if include_next else 8, 8, y=-1.8, x0=-0.65, gap=0.7)
    if include_next:
        row[-1].set_stroke(GOLD, width=5)
    return grid, cells, selector, row


def observed_rail(share, y=-2.75):
    """A compact white-share rail with a fixed 25% target and a movable observation."""
    x0, x1 = 1.1, 5.9
    base = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=4)
    target_x = interpolate(x0, x1, 0.25)
    target = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1, stroke_width=0).scale(0.13)
    target.rotate(PI).move_to([target_x, y + 0.28, 0])
    observed_x = interpolate(x0, x1, share)
    observed = Dot([observed_x, y, 0], radius=0.14, color=WHITE, stroke_color=TEAL, stroke_width=3)
    labels = VGroup(T("observed", 24, WHITE).next_to(observed, DOWN, buff=0.06),
                    T("target", 24, GOLD).next_to(target, LEFT, buff=0.12))
    return VGroup(base, target, observed, labels)


def choice_arrows():
    """The two prediction choices, rebuilt identically across s04–s06."""
    force = VGroup(T("force a balance?", 28, RED, weight=BOLD).move_to([2.7, 2.1, 0]),
                   Arrow([1.35, 1.55, 0], [4.05, 1.55, 0],
                         color=RED, stroke_width=4, tip_length=0.2))
    same = VGroup(T("same chance map?", 28, TEAL, weight=BOLD).move_to([2.7, 0.72, 0]),
                  Arrow([1.35, 0.15, 0], [4.05, 0.15, 0],
                        color=TEAL, stroke_width=4, tip_length=0.2))
    return force, same


def predict_question():
    """The carried prediction card, with its right chip clear of the outcome row."""
    q = question_card("What controls the next flower?",
                      ["earlier results", "same chance map"], y=-3.2, size=30)
    q.chips[1].shift(DOWN * 0.14)
    return q


def running_plot():
    """Large plot whose curve is calculated from OUTCOMES, never sketched."""
    p = Plot(box=(-5.75, 5.5, -2.2, 1.75), xr=(1, 80), yr=(0, 0.62),
             xticks=[(1, "1"), (20, "20"), (40, "40"), (60, "60"), (80, "80")],
             yticks=[(0, "0"), (0.25, "25%"), (0.5, "50%")],
             xlabel="offspring counted", ylabel="white share", label_size=28)
    line = DashedLine(p.pt(1, 0.25), p.pt(80, 0.25), color=GOLD,
                      stroke_width=3, dash_length=0.14)
    label = T("25% target", 26, GOLD).move_to([4.45, 1.25, 0])
    target = VGroup(line, label)
    return p, target


def running_curve(p, upto=80):
    pts = [p.pt(i, RUNNING_WHITE[i - 1]) for i in range(1, int(upto) + 1)]
    curve = VMobject(stroke_color=WHITE, stroke_width=6, fill_opacity=0)
    if len(pts) > 1:
        curve.set_points_as_corners(pts)
    return curve


def mendel_panel(left=-6.1, right=2.0):
    """Mendel's seven computed ratios on one shared scale; only 3 : 1 is marked."""
    top, bottom = 2.35, -2.45
    axis_y = 2.75
    x_of = lambda ratio: interpolate(left + 2.7, right - 0.2, (ratio - 2.75) / (3.2 - 2.75))
    base = Line([left + 2.7, axis_y, 0], [right - 0.2, axis_y, 0], color=GREY, stroke_width=4)
    tx = x_of(3.0)
    tick = Line([tx, axis_y - 0.16, 0], [tx, axis_y + 0.16, 0], color=GOLD, stroke_width=5)
    mark = M("3 : 1", 28, GOLD).next_to(tick, UP, buff=0.12)
    title = T("Mendel's counts", 32, GOLD, weight=BOLD).move_to([left + 1.2, 3.55, 0])
    rows, dots = VGroup(), VGroup()
    ys = np.linspace(top, bottom, len(MENDEL))
    for (name, ratio), y in zip(MENDEL, ys):
        lab = T(name, 26, TEXT).move_to([left, y, 0], aligned_edge=LEFT)
        guide = Line([left + 2.7, y, 0], [right - 0.2, y, 0], color=GREY,
                     stroke_width=1.5, stroke_opacity=0.35)
        dot = Dot([x_of(ratio), y, 0], radius=0.11, color=GOLD,
                  stroke_color=TEXT, stroke_width=2)
        rows.add(VGroup(lab, guide))
        dots.add(dot)
    return VGroup(title, base, tick, mark), rows, dots


class S00Link(FilmScene):
    def construct(self):
        grid, cells, row, target = chance_world(empty=True)
        self.play(Create(grid[0]), FadeIn(grid[1:]), run_time=1.3)
        self.at("purple flowered parents")
        self.play(FadeIn(row, lag_ratio=0.08), run_time=1.0)
        self.at("real offspring counts")
        self.play(FadeIn(target, shift=DOWN * 0.15), run_time=0.8)
        selector = orbit_selector(cells)
        self.at("each new plan")
        self.play(FadeIn(selector), run_time=0.5)
        self.at("real group records")
        held_pulse = lambda t: 1.0 if 0.38 <= t <= 0.48 else 0.0
        self.play(Indicate(VGroup(self.mobjects[0], row, target), color=TEAL, scale_factor=1.0,
                           rate_func=held_pulse), run_time=5.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Predicting traits with Punnett squares"
    TITLE = "Why Real Counts Wander"

    def construct(self):
        grid, cells, row, target = chance_world(empty=True)
        background = VGroup(grid, row, target).set_opacity(0.18)
        self.add(background)
        orbit = orbit_selector(cells, speed=0.3).set_opacity(0.35)
        self.add(orbit)
        veil = Rectangle(width=8.7, height=2.4, fill_color=BG, fill_opacity=0.88,
                         stroke_color=GOLD, stroke_width=2).move_to(ORIGIN)
        title = T(self.TITLE, 52, TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON.upper(), 22, GREY).next_to(title, UP, buff=0.28)
        self.play(FadeIn(veil), FadeIn(lesson), Write(title), run_time=0.9)
        self.wait(0.7)
        self.play(FadeOut(VGroup(veil, lesson, title)), run_time=0.4)


class S02Chance(FilmScene):
    def construct(self):
        grid, cells, row, target = chance_world(empty=True)
        self.add(grid, row, target)
        selector = orbit_selector(cells, speed=1.3)
        self.play(FadeIn(selector), run_time=0.6)
        pack = VGroup(T("packing list", 30, GREY),
                      Rectangle(width=2.4, height=0.85, stroke_color=GREY, stroke_width=3))
        pack[0].move_to(pack[1])
        pack.move_to([3.15, 2.45, 0])
        self.at("not a packing list")
        self.play(FadeIn(pack), run_time=0.6)
        slash = Line(pack.get_corner(UL), pack.get_corner(DR), color=RED, stroke_width=7)
        # The strike-through is the meaning of this crossed-out packing-list icon.
        slash.layout_ok = True
        self.play(Create(slash), run_time=0.45)
        filled = flower_dot("purple").move_to(row[0])
        self.at("one box is selected")
        selector.clear_updaters()
        self.play(selector.animate.move_to(cells[1]), run_time=1.0)
        self.play(Transform(row[0], filled), run_time=0.7)
        self.at("process starts again")
        self.play(selector.animate.move_to(cells[0]), run_time=0.8)
        selector.add_updater(orbit_selector(cells, speed=1.25).updaters[0])
        self.at("do not remove boxes")
        self.play(Indicate(grid[0], color=TEAL, scale_factor=1.02), run_time=1.0)
        reset = T("new chance each time", 34, TEAL, weight=BOLD).move_to([3.15, -0.25, 0])
        self.at("map resets")
        self.play(FadeOut(VGroup(pack, slash)), FadeIn(reset, shift=UP * 0.12), run_time=0.8)
        self.finish()


class S03SmallRun(FilmScene):
    def construct(self):
        grid, cells = grid_at(cx=-4.5, cy=0.65, s=1.05, inside_size=28)
        selector = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.5,
                                    stroke_color=TEAL, stroke_width=4,
                                    fill_color=TEAL, fill_opacity=0.24).move_to(cells[0])
        selector.layout_ok = True  # deliberately encloses the selected genotype
        title = T("computed example", 30, TEAL, weight=BOLD).move_to([-4.5, 3.55, 0])
        slots = slot_row(8, 0, y=-1.85, x0=-1.35, gap=0.68)
        base_y = -0.15
        bars = VGroup(
            Rectangle(width=0.75, height=0.001, stroke_color=PURPLE, fill_color=PURPLE,
                      fill_opacity=0.75).move_to([3.6, base_y, 0]),
            Rectangle(width=0.75, height=0.001, stroke_color=WHITE, fill_color=WHITE,
                      fill_opacity=0.75).move_to([5.0, base_y, 0]),
        )
        bar_labels = VGroup(T("purple", 26, PURPLE).move_to([3.6, -0.62, 0]),
                            T("white", 26, WHITE).move_to([5.0, -0.62, 0]))
        target = DashedLine([3.0, 1.45, 0], [5.65, 1.45, 0], color=GOLD,
                            stroke_width=4, dash_length=0.13)
        self.play(FadeIn(title), Create(grid[0]), FadeIn(grid[1:]), FadeIn(slots), run_time=1.2)
        self.at("selectors land")
        self.add(selector)
        purple_n = white_n = 0
        for i, outcome in enumerate(OUTCOMES[:8]):
            cell = cells[3] if outcome else cells[i % 3]
            color = "white" if outcome else "purple"
            self.play(selector.animate.move_to(cell), run_time=0.3)
            self.play(Transform(slots[i], flower_dot(color).move_to(slots[i])), run_time=0.24)
            white_n += int(outcome)
            purple_n += int(not outcome)
        selector._orbit_t = 0.0
        selector.add_updater(orbit_selector(cells, side=0.5, speed=1.35).updaters[0])
        self.at("uneven group")
        self.play(FadeIn(bar_labels), Create(target), run_time=0.7)
        pb = Rectangle(width=0.75, height=2.6 * purple_n / 8, stroke_color=PURPLE,
                       fill_color=PURPLE, fill_opacity=0.75).move_to([3.6, base_y + 1.3 * purple_n / 8, 0])
        wb = Rectangle(width=0.75, height=2.6 * white_n / 8, stroke_color=WHITE,
                       fill_color=WHITE, fill_opacity=0.75).move_to([5.0, base_y + 1.3 * white_n / 8, 0])
        self.play(Transform(bars[0], pb), Transform(bars[1], wb), run_time=1.0)
        self.at("does not make")
        self.play(Indicate(grid, color=BLUE, scale_factor=1.02), run_time=0.8)
        rail = observed_rail(white_n / 8, y=-2.65)
        self.at("chance to swing")
        self.play(FadeIn(rail, shift=UP * 0.1), run_time=0.9)
        self.at("lean differently")
        self.play(Indicate(slots, color=TEAL, scale_factor=1.02), run_time=1.0)
        pulse(target, base=4, amp=1.2, speed=2.0)
        self.finish()


class S04Predict(FilmScene):
    def construct(self):
        grid, cells, selector, row = small_run_world()
        self.add(grid, selector, row)
        self.at("next slot")
        self.play(row[-1].animate.scale(1.55), run_time=0.8)
        force, same = choice_arrows()
        self.at("force the next flower")
        self.play(FadeIn(force[0]), GrowArrow(force[1]), run_time=0.9)
        self.at("same chance map")
        self.play(FadeIn(same[0]), GrowArrow(same[1]), run_time=0.9)
        q = predict_question()
        self.at("make your prediction")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S05Pause(Scene):
    def construct(self):
        grid, cells, selector, row = small_run_world()
        row[-1].scale(1.55)
        force, same = choice_arrows()
        q = predict_question()
        self.add(stage_panel(), grid, selector, row, force, same, q)
        self.wait(4.5)


class S06Reveal(FilmScene):
    def construct(self):
        grid, cells, selector, row = small_run_world()
        row[-1].scale(1.55)
        force, same = choice_arrows()
        self.add(grid, selector, row, force, same)
        self.at("same chance map applies")
        self.play(FadeOut(force), Indicate(same, color=TEAL, scale_factor=1.08), run_time=0.9)
        selector.clear_updaters()
        self.at("next result")
        self.play(selector.animate.move_to(cells[3]), run_time=1.0)
        self.play(Transform(row[-1], flower_dot("white", 0.27).move_to(row[-1])), run_time=0.8)
        separate = T("separate chance", 34, TEAL, weight=BOLD).move_to([2.7, 2.1, 0])
        self.at("separate chance")
        self.play(swap(same, separate), run_time=0.8)
        old_rail = observed_rail(RUNNING_WHITE[7], y=-2.65)
        new_rail = observed_rail(RUNNING_WHITE[8], y=-2.65)
        self.at("nearer the prediction")
        self.play(FadeIn(old_rail), run_time=0.5)
        self.play(Transform(old_rail, new_rail), run_time=1.0)
        self.at("farther away")
        self.play(Indicate(old_rail, color=TEAL, scale_factor=1.02), run_time=0.8)
        selector.add_updater(orbit_selector(cells, speed=1.2).updaters[0])
        self.finish()


class S07Larger(FilmScene):
    def construct(self):
        p, target = running_plot()
        title = T("computed example", 30, TEAL, weight=BOLD).move_to([-4.4, 3.55, 0])
        n = ValueTracker(2)
        curve = always_redraw(lambda: running_curve(p, max(2, int(n.get_value()))))
        dot = always_redraw(lambda: Dot(p.pt(max(1, int(n.get_value())),
                                             RUNNING_WHITE[max(1, int(n.get_value())) - 1]),
                                        radius=0.12, color=WHITE, stroke_color=TEAL, stroke_width=3))

        def conveyor():
            upto = max(1, int(n.get_value()))
            start = max(0, upto - 18)
            dots = VGroup(*[flower_dot("white" if OUTCOMES[i] else "purple", 0.12)
                            for i in range(start, upto)])
            dots.arrange(RIGHT, buff=0.13).move_to([0.4, 2.55, 0])
            return dots

        stream = always_redraw(conveyor)

        def bars():
            upto = max(1, int(n.get_value()))
            white = int(OUTCOMES[:upto].sum())
            purple = upto - white
            total_h = 1.1
            pb = Rectangle(width=0.34, height=max(0.02, total_h * purple / upto),
                           fill_color=PURPLE, fill_opacity=0.8, stroke_color=PURPLE)
            wb = Rectangle(width=0.34, height=max(0.02, total_h * white / upto),
                           fill_color=WHITE, fill_opacity=0.8, stroke_color=WHITE)
            VGroup(pb, wb).arrange(RIGHT, buff=0.12, aligned_edge=DOWN).move_to([5.5, 2.55, 0])
            return VGroup(pb, wb)

        live_bars = always_redraw(bars)
        stream_scan = ratio_scanner(-3.4, 3.9, y=2.55, height=0.72)
        self.add(stream_scan)
        self.play(FadeIn(title), FadeIn(stream), FadeIn(live_bars), run_time=0.8)
        self.at("bars rescale")
        self.play(Create(p), FadeIn(target), run_time=1.1)
        self.add(curve, dot)
        self.at("still wiggles")
        self.play(n.animate.set_value(22), run_time=4.0, rate_func=linear)
        self.at("swings usually shrink")
        self.play(n.animate.set_value(45), run_time=4.0, rate_func=linear)
        self.at("less control")
        self.play(n.animate.set_value(65), run_time=3.0, rate_func=linear)
        self.at("approaches its target")
        self.play(n.animate.set_value(80), run_time=5.0, rate_func=linear)
        pulse(target[0], base=3, amp=1.0, speed=2.0)
        self.finish()


class S08Mendel(FilmScene):
    def construct(self):
        head, rows, dots = mendel_panel(left=-5.7, right=5.9)
        scanner = ratio_scanner(-2.95, 5.7, y=-0.05, height=5.55)
        self.add(scanner)
        self.play(FadeIn(head[0]), run_time=0.7)
        self.at("real pea plants")
        self.play(Create(head[1]), Create(head[2]), FadeIn(head[3]), run_time=0.9)
        self.at("several traits")
        self.play(LaggedStart(*[FadeIn(row, shift=RIGHT * 0.1) for row in rows], lag_ratio=0.12),
                  run_time=1.5)
        self.at("place each")
        self.play(LaggedStart(*[FadeIn(dot, scale=1.5) for dot in dots], lag_ratio=0.16),
                  run_time=2.0)
        self.at("gather near")
        for group in (VGroup(*dots[:3]), VGroup(*dots[3:])):
            self.play(Indicate(group, color=GOLD, scale_factor=1.04), run_time=0.8)
        for i, dot in enumerate(dots):
            bob(dot, amp=0.018, speed=1.5, seed=i)
        self.finish()


class S09Evidence(FilmScene):
    def construct(self):
        head, rows, dots = mendel_panel(left=-6.15, right=1.15)
        panel = VGroup(head, rows, dots)
        scanner = ratio_scanner(-3.45, 0.95, y=-0.05, height=5.55)
        self.add(scanner, panel)
        for i, dot in enumerate(dots):
            bob(dot, amp=0.015, speed=1.4, seed=i)
        brace = Brace(VGroup(*dots), RIGHT, color=GOLD)
        spread = T("spread", 28, GOLD, weight=BOLD).next_to(brace, RIGHT, buff=0.12)
        self.at("evidence to examine")
        self.play(GrowFromCenter(brace), FadeIn(spread), run_time=0.8)
        self.at("gather near it")
        self.play(Indicate(VGroup(*dots), color=GOLD, scale_factor=1.03), run_time=1.0)
        guide_title = T("read the evidence", 30, TEAL, weight=BOLD).move_to([4.25, 2.4, 0])
        guide = VGroup()
        for label in ("counts", "ratios", "group sizes"):
            box = Square(side_length=0.42, stroke_color=TEAL, stroke_width=3)
            text = T(label, 28, TEXT)
            guide.add(VGroup(box, text).arrange(RIGHT, buff=0.2))
        guide.arrange(DOWN, aligned_edge=LEFT, buff=0.48).move_to([4.25, 0.55, 0])
        self.at("no single row")
        self.play(FadeOut(VGroup(brace, spread)), FadeIn(guide_title), run_time=0.7)
        self.at("compare counts")
        self.play(FadeIn(guide[0], shift=RIGHT * 0.12), run_time=0.6)
        self.at("ratios")
        self.play(FadeIn(guide[1], shift=RIGHT * 0.12), run_time=0.6)
        self.at("group sizes")
        self.play(FadeIn(guide[2], shift=RIGHT * 0.12), run_time=0.6)
        pulse(head[1], base=4, amp=1.0, speed=2.0)
        self.finish()


class S10Scope(FilmScene):
    def construct(self):
        frame = RoundedRectangle(corner_radius=0.2, width=5.7, height=5.6,
                                 stroke_color=BLUE, stroke_width=4).move_to([-3.2, 0.1, 0])
        grid, cells = grid_at(cx=-3.25, cy=0.2, s=1.35)
        selector = orbit_selector(cells, side=1.08, speed=1.2)
        inside = T("one-gene model", 32, BLUE, weight=BOLD).move_to([-3.25, 3.48, 0])
        self.play(Create(frame), FadeIn(grid), FadeIn(selector), run_time=1.0)
        self.at("one gene model")
        self.play(FadeIn(inside), run_time=0.6)
        outside_title = T("outside this model", 30, GREY, weight=BOLD).move_to([3.45, 2.9, 0])
        weather = VGroup(Circle(radius=0.3, color=GREY),
                         *[Line(0.45 * d, 0.72 * d, color=GREY, stroke_width=4)
                           for d in (UP, DOWN, LEFT, RIGHT, UR, UL, DR, DL)])
        weather.move_to([2.0, 1.75, 0])
        soil = VGroup(Rectangle(width=1.0, height=0.55, stroke_color=GREY, fill_color=GREY,
                                fill_opacity=0.2), T("soil", 26, GREY)).arrange(DOWN, buff=0.08)
        soil.move_to([3.55, 1.65, 0])
        seed = flower_dot("white", 0.18)
        lost = VGroup(seed, Line(seed.get_corner(UL) + UL * 0.12, seed.get_corner(DR) + DR * 0.12,
                                 color=GREY, stroke_width=5), T("lost seed", 24, GREY)).arrange(DOWN, buff=0.08)
        lost.move_to([5.1, 1.65, 0])
        self.at("weather soil")
        self.play(FadeIn(outside_title), FadeIn(weather), FadeIn(soil), run_time=0.9)
        self.at("lost seeds")
        self.play(FadeIn(lost), run_time=0.6)
        self.at("within its scope")
        target = DashedLine([1.25, -0.35, 0], [5.85, -0.35, 0], color=GOLD,
                            stroke_width=5, dash_length=0.15)
        target_lab = T("target", 28, GOLD).next_to(target, UP, buff=0.12)
        self.play(Create(target), FadeIn(target_lab), run_time=0.7)
        small = Dot([2.0, -0.35, 0], radius=0.16, color=WHITE)
        large = Dot([4.9, -0.35, 0], radius=0.16, color=WHITE)
        labels = VGroup(T("small group", 26, TEXT).move_to([2.0, -1.45, 0]),
                        T("large group", 26, TEXT).move_to([4.9, -1.45, 0]))
        tags = VGroup(T("schematic", 24, GREY).next_to(labels[0], DOWN, buff=0.08),
                      T("schematic", 24, GREY).next_to(labels[1], DOWN, buff=0.08))
        self.at("larger groups")
        self.play(FadeIn(VGroup(small, large, labels, tags)), run_time=0.7)
        small_base, large_base = small.get_center().copy(), large.get_center().copy()
        small._t = large._t = 0.0
        small.add_updater(lambda m, dt: (setattr(m, "_t", m._t + dt),
                                         m.move_to(small_base + UP * 0.72 * np.sin(2.3 * m._t)))[1])
        large.add_updater(lambda m, dt: (setattr(m, "_t", m._t + dt),
                                         m.move_to(large_base + UP * 0.2 * np.sin(2.0 * m._t)))[1])
        pulse(target, base=5, amp=1.2, speed=2.0)
        self.finish()


class S11End(EndCard):
    LINE = "Larger groups usually come closer to a Punnett square’s predicted ratio."
