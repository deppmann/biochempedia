"""Tight Ends, Loose Ends — one carried schematic world.

COLOR MAP
  GOLD   fresh ATP/GTP-bearing subunits
  BLUE   old ADP/GDP-bearing subunits
  GREEN  a tight end / low critical concentration
  RED    a loose end / high critical concentration
  TEAL   the free-subunit gauge
  TEXT   labels and neutral structure

All curves in this film are schematic and explicitly labelled as such.  Molecular
subunits are represented only as blocks or dots, never as molecular structures.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

GOLD_FRESH = GOLD


# Shared geometry: carried scenes rebuild these landmarks exactly.
FY = -0.35
BX = 0.56
BH = 0.90
BW = 0.50
DOOR_X = 1.15
GAUGE_X = 5.35


def until(scene, phrase, margin=0.25, floor=0.35, nth=0):
    """Time available for an animation before a spoken cue."""
    return max(floor, scene.t_of(phrase, nth) - 0.2 - scene.elapsed() - margin)


def label(text, color=TEXT, size=30, weight=NORMAL):
    return T(text, size=size, color=color, weight=weight)


def subunit(x, y=FY, color=BLUE, w=BW, h=BH):
    return RoundedRectangle(
        corner_radius=0.07, width=w, height=h,
        stroke_color=color, stroke_width=2.4,
        fill_color=color, fill_opacity=0.42,
    ).move_to([x, y, 0])


def filament(xs, colors, y=FY):
    return VGroup(*[subunit(x, y, c) for x, c in zip(xs, colors)])


def tube_columns(x0, count, fresh=0, y=0.05, rows=5, dx=0.56, dy=0.48):
    cols = VGroup()
    for i in range(count):
        c = GOLD_FRESH if i >= count - fresh else BLUE
        col = VGroup(*[subunit(x0 + i * dx, y + (r - (rows - 1) / 2) * dy,
                                     c, w=0.47, h=0.39) for r in range(rows)])
        cols.add(col)
    return cols


def drifting_field(seed=1, n=34, opacity=0.55, speed=1.0):
    """Gold free subunits with slow, deterministic wraparound drift."""
    rng = np.random.RandomState(seed)
    dots = VGroup()
    # A dense field is part of the puzzle: free building blocks remain abundant.
    n = int(round(n * 1.2))
    for _ in range(n):
        d = Dot([rng.uniform(-6.55, 6.55), rng.uniform(-3.55, 3.55), 0],
                radius=rng.uniform(0.065, 0.115), color=GOLD_FRESH)
        d.set_opacity(opacity)
        d.v = np.array([rng.uniform(-0.16, 0.18), rng.uniform(0.10, 0.24), 0]) * speed

        def drift(m, dt):
            m.shift(m.v * dt)
            if m.get_y() > 3.72:
                m.shift(DOWN * 7.35)
            if m.get_x() > 6.92:
                m.shift(LEFT * 13.75)
            elif m.get_x() < -6.92:
                m.shift(RIGHT * 13.75)

        d.add_updater(drift)
        dots.add(d)
    dots.set_z_index(-8)
    return dots


def doorway(x=DOOR_X, y=FY):
    posts = VGroup(
        Line([x, y - 0.72, 0], [x, y + 0.72, 0], color=TEXT, stroke_width=7),
        Line([x, y + 0.72, 0], [x + 0.42, y + 0.72, 0], color=TEXT, stroke_width=7),
        Line([x, y - 0.72, 0], [x + 0.42, y - 0.72, 0], color=TEXT, stroke_width=7),
    )
    return posts


def gauge(pointer_y=0.0, low_y=-1.25, high_y=1.25, show_ticks=False):
    x = GAUGE_X
    body = RoundedRectangle(corner_radius=0.12, width=1.15, height=5.0,
                            stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.08).move_to([x, 0, 0])
    fill = Rectangle(width=0.72, height=max(0.18, pointer_y + 2.25),
                     stroke_width=0, fill_color=TEAL, fill_opacity=0.38)
    fill.move_to([x, -2.25 + fill.height / 2, 0])
    pointer = Triangle(color=TEAL, fill_color=TEAL, fill_opacity=1).scale(0.12).rotate(-PI / 2)
    pointer.move_to([x - 0.72, pointer_y, 0])
    title = label("free subunits", TEAL, 28, BOLD).next_to(body, UP, buff=0.18)
    schematic = label("schematic", TEXT, 22).set_opacity(0.72).next_to(body, DOWN, buff=0.14)
    g = VGroup(body, fill, pointer, title, schematic)
    g.pointer, g.fill, g.body = pointer, fill, body
    if show_ticks:
        lo = Line([x - 0.58, low_y, 0], [x + 0.58, low_y, 0], color=GREEN, stroke_width=6)
        hi = Line([x - 0.58, high_y, 0], [x + 0.58, high_y, 0], color=RED, stroke_width=6)
        g.add(lo, hi)
        g.low, g.high = lo, hi
    return g


def tick_pair_labels():
    lo = label("tight Cc", GREEN, 28, BOLD).move_to([3.92, -1.25, 0])
    hi = label("loose Cc", RED, 28, BOLD).move_to([3.90, 1.25, 0])
    return lo, hi


def arrow_with_label(start, end, text, color):
    a = Arrow(start, end, buff=0.05, color=color, stroke_width=7, tip_length=0.28)
    t = label(text, color, 30, BOLD).next_to(a, UP, buff=0.12)
    return VGroup(a, t)


class S00Hook(SpokenScene):
    def construct(self):
        dots = drifting_field(2, 42, 0.62, 1.25)
        seed = RoundedRectangle(corner_radius=0.12, width=0.75, height=2.0,
                                stroke_color=GREY, fill_color=GREY, fill_opacity=0.42).move_to([-5.9, -0.25, 0])
        cols = tube_columns(-5.35, 16, fresh=3, y=-0.25, rows=3, dx=0.55, dy=0.52)
        cols.scale(1.35, about_point=np.array([-5.35, -0.25, 0]))
        tube_lab = label("microtubule, schematic", TEXT, 28).move_to([-2.35, -1.65, 0])
        q = label("?", TEXT, 94, BOLD).move_to([-1.4, 2.45, 0])
        clock_box = RoundedRectangle(corner_radius=0.12, width=1.75, height=0.82,
                                     stroke_color=TEXT, stroke_width=2).move_to([5.55, 2.86, 0])
        clock = M("0:00", 30, TEXT).move_to(clock_box)
        clock_note = label("schematic", TEXT, 22).set_opacity(0.75).next_to(clock_box, DOWN, buff=0.1)
        self.add(dots, seed, VGroup(*cols[:5]), tube_lab, q)

        self.at("Watch one microtubule")
        self.play(FadeIn(clock_box), FadeIn(clock), FadeIn(clock_note), run_time=0.55)
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.22) for c in cols[5:12]],
                              lag_ratio=0.45),
                  Transform(clock, M("2:20", 30, TEXT).move_to(clock_box)),
                  run_time=until(self, "It lengthens slowly", floor=2.2), rate_func=linear)
        self.at("It lengthens slowly")
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.18) for c in cols[12:]], lag_ratio=0.65),
                  Transform(clock, M("3:00", 30, TEXT).move_to(clock_box)),
                  run_time=until(self, "then collapses", floor=1.5), rate_func=linear)

        self.at("then collapses")
        peel = VGroup(*[c.copy() for c in cols[6:]])
        self.add(peel)
        self.remove(*cols[6:])
        anims = []
        for i, col in enumerate(reversed(peel)):
            for j, block in enumerate(col):
                sgn = j - 1
                anims.append(block.animate.shift(RIGHT * 0.65 + UP * sgn * (0.35 + 0.06 * i)).rotate(-0.12 * sgn).set_opacity(0))
        self.play(LaggedStart(*anims, lag_ratio=0.025), run_time=1.85)

        self.at("A crystal")
        cube = Square(1.05, color=GOLD_FRESH, fill_color=GOLD_FRESH, fill_opacity=0.28, stroke_width=4).move_to([5.45, -1.15, 0])
        crystal_lab = label("crystal: settles", GOLD_FRESH, 28, BOLD).next_to(cube, DOWN, buff=0.16)
        self.play(FadeIn(cube, shift=LEFT * 0.6), FadeIn(crystal_lab), run_time=0.75)
        regrow = tube_columns(-0.895, 4, fresh=2, y=-0.25, rows=3, dx=0.55, dy=0.52)
        regrow.scale(1.35, about_point=np.array([-0.895, -0.25, 0]))
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in regrow], lag_ratio=0.6),
                  run_time=until(self, "does not do this", floor=1.2), rate_func=linear)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Cytoskeletal Polymers and Dynamics"
    TITLE = "Tight Ends, Loose Ends"

    def construct(self):
        dots = drifting_field(3, 38, 0.28, 0.9)
        self.add(dots)
        super().construct()


class S02Doorway(SpokenScene):
    def construct(self):
        dots = drifting_field(4, 28, 0.44, 1.0)
        xs = np.arange(-5.7, 0.75, BX)
        fil = filament(xs, [BLUE] * (len(xs) - 3) + [GOLD_FRESH] * 3)
        end_glow = SurroundingRectangle(VGroup(*fil[-3:]), color=GOLD_FRESH, buff=0.12, stroke_width=2)
        g = gauge(-0.55)
        self.add(dots, fil, end_glow, g)

        self.at("treat it as a doorway")
        door = doorway()
        self.play(Create(door), run_time=0.7)
        arrive = arrow_with_label([3.0, 0.85, 0], [1.48, 0.85, 0], "arrive  0", GOLD_FRESH)
        leave = arrow_with_label([1.48, -1.3, 0], [3.0, -1.3, 0], "leave  0", BLUE)

        self.at("Subunits arrive")
        arriving = VGroup(*[Dot([3.0 + 0.35 * i, 0.25 + 0.22 * (-1) ** i, 0], radius=0.09, color=GOLD_FRESH) for i in range(4)])
        self.play(GrowArrow(arrive[0]), FadeIn(arrive[1]), FadeIn(arriving), run_time=0.55)
        dock = subunit(0.97, FY, GOLD_FRESH)
        self.play(arriving.animate.move_to([1.05, 0.05, 0]).set_opacity(0), FadeIn(dock, shift=RIGHT * 0.25),
                  Transform(arrive[1], label("arrive  1", GOLD_FRESH, 30, BOLD).move_to(arrive[1])), run_time=0.9)

        self.at("how many are free")
        high = gauge(1.25)
        high.move_to(g)
        self.play(Transform(g, high), arrive[0].animate.set_stroke(width=13),
                  dots.animate.set_opacity(0.72), run_time=1.0)
        for num in (2, 3):
            b = subunit(0.97 + (num - 1) * BX, FY, GOLD_FRESH)
            self.play(FadeIn(b, shift=RIGHT * 0.25),
                      Transform(arrive[1], label(f"arrive  {num}", GOLD_FRESH, 30, BOLD).move_to(arrive[1])), run_time=0.42)

        self.at("They leave")
        self.play(GrowArrow(leave[0]), FadeIn(leave[1]), run_time=0.5)
        loose = fil[-1].copy()
        self.add(loose)
        self.play(loose.animate.shift(RIGHT * 1.55).set_opacity(0),
                  Transform(leave[1], label("leave  1", BLUE, 30, BOLD).move_to(leave[1])), run_time=0.8)

        self.at("does not depend")
        low = gauge(-1.45)
        low.move_to(g)
        self.play(Transform(g, low), dots.animate.set_opacity(0.3), run_time=0.65)
        high2 = gauge(1.1)
        high2.move_to(g)
        self.play(Transform(g, high2), dots.animate.set_opacity(0.68), run_time=0.65)
        self.play(Indicate(leave[0], color=BLUE, scale_factor=1.0),
                  Transform(leave[1], label("leave  2", BLUE, 30, BOLD).move_to(leave[1])), run_time=0.55)

        self.at("the two balance")
        mid = gauge(0.0)
        mid.move_to(g)
        self.play(Transform(g, mid), arrive[0].animate.set_stroke(width=7),
                  Transform(arrive[1], label("arrive  4", GOLD_FRESH, 30, BOLD).move_to(arrive[1])),
                  Transform(leave[1], label("leave  4", BLUE, 30, BOLD).move_to(leave[1])), run_time=0.9)

        self.at("critical concentration")
        cc = Line([GAUGE_X - 0.58, 0, 0], [GAUGE_X + 0.58, 0, 0], color=TEAL, stroke_width=7)
        ccl = label("Cc", TEAL, 32, BOLD).next_to(cc, LEFT, buff=0.15)
        self.play(Create(cc), FadeIn(ccl), run_time=0.6)
        self.finish()


class S03Settle(SpokenScene):
    def construct(self):
        dots = drifting_field(5, 31, 0.5, 1.0)
        xs = np.arange(-5.7, 0.75, BX)
        fil = filament(xs, [BLUE] * (len(xs) - 3) + [GOLD_FRESH] * 3)
        door = doorway()
        g = gauge(0.0)
        cc = Line([GAUGE_X - 0.58, 0, 0], [GAUGE_X + 0.58, 0, 0], color=TEAL, stroke_width=7)
        ccl = label("Cc", TEAL, 32, BOLD).next_to(cc, LEFT, buff=0.15)
        self.add(dots, fil, door, g, cc, ccl)

        self.at("Above it")
        high = gauge(1.25); high.move_to(g)
        grows = arrow_with_label([0.0, 1.7, 0], [2.2, 1.7, 0], "grows", GREEN)
        extra = VGroup(*[subunit(0.97 + i * BX, FY, GOLD_FRESH) for i in range(3)])
        self.play(Transform(g, high), GrowArrow(grows[0]), FadeIn(grows[1]),
                  LaggedStart(*[FadeIn(b, shift=LEFT * 0.2) for b in extra], lag_ratio=0.5), run_time=1.0)

        self.at("Below it")
        low = gauge(-1.25); low.move_to(g)
        shrinks = arrow_with_label([2.2, 1.7, 0], [0.0, 1.7, 0], "shrinks", RED)
        self.play(Transform(g, low), ReplacementTransform(grows, shrinks),
                  LaggedStart(*[FadeOut(b, shift=RIGHT * 0.4) for b in reversed(extra)], lag_ratio=0.35), run_time=1.0)

        self.at("If subunits never use")
        neutral = filament(np.arange(-5.7, 2.25, BX), [TEXT] * len(np.arange(-5.7, 2.25, BX)))
        left_door = doorway(-6.0, FY).rotate(PI)
        self.play(FadeOut(shrinks), FadeOut(door), FadeOut(fil), FadeIn(neutral), Create(left_door),
                  Create(doorway(2.52, FY)), run_time=1.0)

        self.at("share one critical concentration")
        lcc = chip("Cc", TEAL, 28).move_to([-5.75, 1.45, 0])
        rcc = chip("Cc", TEAL, 28).move_to([2.52, 1.45, 0])
        lcc[0].set_fill(BG, opacity=1.0)
        rcc[0].set_fill(BG, opacity=1.0)
        self.play(FadeIn(lcc), FadeIn(rcc), Indicate(cc, color=TEAL), run_time=0.75)

        self.at("would grow until")
        high2 = gauge(1.55); high2.move_to(g)
        ext_l = VGroup(*[subunit(-5.98 - i * BX, FY, TEXT) for i in range(2)])
        ext_r = VGroup(*[subunit(2.52 + i * BX, FY, TEXT) for i in range(2)])
        self.play(Transform(g, high2), dots.animate.set_opacity(0.68),
                  LaggedStart(*[FadeIn(b) for b in [*ext_l, *ext_r]], lag_ratio=0.35), run_time=1.25)
        mid = gauge(0.0); mid.move_to(g)
        self.play(Transform(g, mid), dots.animate.set_opacity(0.34), run_time=1.1)

        self.at("simply settle")
        full = VGroup(ext_l, neutral, ext_r)
        br = Brace(full, UP, color=TEXT, buff=0.2)
        settled = label("settled", TEXT, 32, BOLD).next_to(br, UP, buff=0.12)
        self.play(GrowFromCenter(br), FadeIn(settled), FadeOut(lcc), FadeOut(rcc), run_time=0.7)
        self.play(Indicate(full, color=TEXT, scale_factor=1.01), run_time=0.8)
        self.finish()


class S04Fresh(SpokenScene):
    def construct(self):
        dots = drifting_field(6, 34, 0.48, 1.1)
        xs = np.arange(-5.9, 3.0, BX)
        neutral = filament(xs, [TEXT] * len(xs))
        br = Brace(neutral, UP, color=TEXT, buff=0.2)
        settled = label("settled", TEXT, 32, BOLD).next_to(br, UP, buff=0.12)
        self.add(dots, neutral, br, settled)

        self.at("actin and tubulin differ")
        old = filament(xs[:-4], [BLUE] * (len(xs) - 4))
        fresh = filament(xs[-4:], [GOLD_FRESH] * 4)
        self.play(FadeOut(br), FadeOut(settled), ReplacementTransform(neutral, VGroup(old, fresh)), run_time=0.9)

        self.at("arrives carrying fresh")
        fresh_chip = chip("fresh: ATP or GTP", GOLD_FRESH, 28).move_to([-3.9, 2.55, 0])
        dots.set_color(GOLD_FRESH)
        new = VGroup(*[subunit(3.0 + i * BX, FY, GOLD_FRESH) for i in range(3)])
        self.play(FadeIn(fresh_chip), LaggedStart(*[FadeIn(b, shift=LEFT * 0.25) for b in new], lag_ratio=0.5), run_time=1.2)

        self.at("after joining")
        old_chip = chip("old: ADP or GDP", BLUE, 28).move_to([-3.9, 1.75, 0])
        wave = VGroup(fresh, new)
        blocks = [b for grp in [fresh, new] for b in grp]
        self.play(FadeIn(old_chip), LaggedStart(*[b.animate.set_color(BLUE) for b in blocks[:4]], lag_ratio=0.55), run_time=1.45)

        self.at("releases the phosphate")
        phosphate = chip("phosphate leaves", TEXT, 28).move_to([3.9, 2.35, 0])
        self.play(FadeIn(phosphate, shift=UP * 0.25),
                  LaggedStart(*[b.animate.set_color(BLUE) for b in blocks[4:6]], lag_ratio=0.5), run_time=0.9)
        self.play(FadeOut(phosphate, shift=UP * 0.3), blocks[-1].animate.set_color(BLUE), run_time=0.65)

        self.at("hold on less tightly")
        old_all = VGroup(old, wave)
        self.play(old_all.animate.shift(UP * 0.08), run_time=0.28, rate_func=there_and_back)
        self.play(old_all.animate.shift(DOWN * 0.08), run_time=0.28, rate_func=there_and_back)
        self.play(Indicate(old_chip, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.finish()


class S05Idea(SpokenScene):
    def construct(self):
        dots = drifting_field(7, 34, 0.48, 1.0)
        xs = np.arange(-5.8, 2.6, BX)
        fil = filament(xs, [BLUE] * (len(xs) - 4) + [GOLD_FRESH] * 4)
        g0 = gauge(0.0)
        self.add(dots, fil, g0)

        self.at("Hydrolysis")
        wave = SurroundingRectangle(VGroup(*fil[-5:-3]), color=TEXT, buff=0.08, stroke_width=3)
        self.play(Create(wave), fil[-5].animate.set_color(BLUE), run_time=0.65)
        self.play(Transform(wave, SurroundingRectangle(VGroup(*fil[-4:-2]), color=TEXT, buff=0.08, stroke_width=3)),
                  fil[-4].animate.set_color(BLUE), run_time=0.65)

        self.at("two kinds of end")
        g = gauge(0.0, show_ticks=True)
        g.move_to(g0)
        self.play(FadeOut(wave), Transform(g0, g), run_time=0.85)

        self.at("A tight end")
        tight = chip("tight", GREEN, 30).move_to([2.05, 1.15, 0])
        lo, hi = tick_pair_labels()
        link_r = VMobject(color=GREEN, stroke_width=3).set_points_as_corners(
            [tight.get_right(), [2.8, -1.95, 0], [4.3, -1.95, 0], [4.55, -1.25, 0]])
        self.play(FadeIn(tight), Create(link_r), FadeIn(lo), run_time=0.8)
        incoming = VGroup(*[subunit(2.6 + i * BX, FY, GOLD_FRESH) for i in range(2)])
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.22) for b in incoming], lag_ratio=0.5), run_time=0.8)

        self.at("A loose end")
        loose = chip("loose", RED, 30).move_to([-5.15, 1.15, 0])
        link_l = VMobject(color=RED, stroke_width=3).set_points_as_corners(
            [loose.get_right(), [-4.25, 2.05, 0], [4.3, 2.05, 0], [4.55, 1.25, 0]])
        self.play(FadeIn(loose), Create(link_l), FadeIn(hi), run_time=0.8)
        self.play(fil[0].animate.shift(LEFT * 0.2).rotate(0.1), run_time=0.3, rate_func=there_and_back)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        dots = drifting_field(8, 34, 0.48, 1.0)
        xs = np.arange(-5.8, 2.6, BX)
        fil = filament(xs, [BLUE] * (len(xs) - 4) + [GOLD_FRESH] * 4)
        g = gauge(0.0, show_ticks=True)
        lo, hi = tick_pair_labels()
        tight = chip("tight", GREEN, 28).move_to([2.05, 0.85, 0])
        loose = chip("loose", RED, 28).move_to([-5.15, 0.85, 0])
        self.add(dots, fil, g, lo, hi, tight, loose)

        self.at("between the two levels")
        band = Rectangle(width=0.78, height=2.5, stroke_width=0,
                         fill_color=TEAL, fill_opacity=0.24).move_to([GAUGE_X, 0, 0])
        pointer = Triangle(color=TEAL, fill_color=TEAL, fill_opacity=1).scale(0.14).rotate(-PI / 2).move_to([GAUGE_X - 0.72, 0, 0])
        self.play(FadeIn(band), FadeIn(pointer), run_time=0.65)
        self.at("above the tight ends")
        self.play(Indicate(g.low, color=GREEN, scale_factor=1.15), pointer.animate.shift(UP * 0.35), run_time=0.55)
        self.at("below the loose ends")
        self.play(Indicate(g.high, color=RED, scale_factor=1.15), pointer.animate.shift(DOWN * 0.35), run_time=0.55)
        self.at("What can the polymer do")
        q = label("Between the levels: what happens?", TEXT, 36, BOLD).move_to([-0.6, -2.75, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.65)
        self.finish()


class S07Think(Scene):
    def construct(self):
        config.background_color = BG
        dots = drifting_field(8, 34, 0.48, 1.0)
        xs = np.arange(-5.8, 2.6, BX)
        fil = filament(xs, [BLUE] * (len(xs) - 4) + [GOLD_FRESH] * 4)
        g = gauge(0.0, show_ticks=True)
        lo, hi = tick_pair_labels()
        band = Rectangle(width=0.78, height=2.5, stroke_width=0,
                         fill_color=TEAL, fill_opacity=0.24).move_to([GAUGE_X, 0, 0])
        pointer = Triangle(color=TEAL, fill_color=TEAL, fill_opacity=1).scale(0.14).rotate(-PI / 2).move_to([GAUGE_X - 0.72, 0, 0])
        q = label("Between the levels: what happens?", TEXT, 36, BOLD).move_to([-0.6, -2.75, 0])
        tight = chip("tight", GREEN, 28).move_to([2.05, 0.85, 0])
        loose = chip("loose", RED, 28).move_to([-5.15, 0.85, 0])
        self.add(dots, fil, g, lo, hi, band, pointer, q, tight, loose)
        self.play(pointer.animate.shift(UP * 0.32), run_time=1.1, rate_func=there_and_back)
        self.play(pointer.animate.shift(DOWN * 0.32), run_time=1.1, rate_func=there_and_back)
        self.wait(2.3)


class S08Actin(SpokenScene):
    def construct(self):
        dots = drifting_field(9, 34, 0.44, 1.05)
        xs = np.arange(-5.6, 3.4, BX)
        colors = [BLUE] * (len(xs) - 4) + [GOLD_FRESH] * 4
        fil = filament(xs, colors)
        q = label("Between the levels: what happens?", TEXT, 36, BOLD).move_to([-0.6, -2.75, 0])
        self.add(dots, fil, q)

        self.at("cannot come to rest")
        self.play(FadeOut(q), fil[0].animate.shift(LEFT * 0.22).rotate(0.12),
                  fil[-1].animate.shift(RIGHT * 0.22), run_time=0.7, rate_func=there_and_back)
        self.at("answers in space")
        head = label("actin filament", TEXT, 36, BOLD).move_to([0, 2.55, 0])
        barbed = VGroup(label("barbed", TEXT, 28), chip("tight", GREEN, 28)).arrange(DOWN, buff=0.08).move_to([3.25, 1.25, 0])
        pointed = VGroup(label("pointed", TEXT, 28), chip("loose", RED, 28)).arrange(DOWN, buff=0.08).move_to([-5.2, 1.25, 0])
        self.play(FadeIn(head), FadeIn(barbed), FadeIn(pointed), run_time=0.75)

        self.at("adds subunits fast")
        added = VGroup(*[subunit(3.4 + i * BX, FY, GOLD_FRESH) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.25) for b in added], lag_ratio=0.35), run_time=1.2)
        self.at("tight end that grows")
        grow_a = Arrow([2.35, -1.35, 0], [4.45, -1.35, 0], color=GREEN, stroke_width=7, tip_length=0.28)
        self.play(GrowArrow(grow_a), run_time=0.55)

        self.at("loose end that shrinks")
        leaving = VGroup(*[fil[i].copy() for i in range(4)])
        self.add(leaving)
        self.play(LaggedStart(*[b.animate.shift(LEFT * 0.9 + DOWN * (0.15 + i * 0.06)).set_opacity(0)
                                for i, b in enumerate(leaving)], lag_ratio=0.3), run_time=1.0)

        self.at("gain and loss match")
        all_fil = VGroup(fil, added)
        br = Brace(all_fil, UP, color=TEXT, buff=0.22)
        same = label("same length", TEXT, 30, BOLD).next_to(br, UP, buff=0.1)
        tracked = fil[-3].copy().set_stroke(TEXT, width=5).set_fill(opacity=0.15)
        self.play(FadeOut(grow_a), GrowFromCenter(br), FadeIn(same), FadeIn(tracked), run_time=0.75)
        # A fixed-length window advances right while a marked subunit stays in the world.
        self.play(all_fil.animate.shift(RIGHT * 0.95), barbed.animate.shift(RIGHT * 0.45),
                  pointed.animate.shift(RIGHT * 0.95), br.animate.shift(RIGHT * 0.95), same.animate.shift(RIGHT * 0.95),
                  run_time=1.6, rate_func=linear)

        self.at("subunits flow through")
        self.play(tracked.animate.set_color(BLUE).shift(LEFT * 2.0), run_time=1.0)
        self.play(tracked.animate.shift(LEFT * 1.0 + DOWN * 0.5).set_opacity(0), run_time=0.6)
        self.at("That is treadmilling")
        word = label("treadmilling", TEXT, 42, BOLD).move_to([0, -2.55, 0])
        self.play(FadeIn(word, shift=UP * 0.2), run_time=0.65)
        self.finish()


class S09Cap(SpokenScene):
    def construct(self):
        dots = drifting_field(10, 36, 0.46, 1.05)
        # Start as the carried single actin row, in the same band.
        xs = np.arange(-5.6, 3.4, BX)
        actin = filament(xs, [BLUE] * (len(xs) - 4) + [GOLD_FRESH] * 4)
        self.add(dots, actin)

        self.at("A microtubule")
        tube = tube_columns(-5.8, 16, fresh=3, y=0.0, rows=5, dx=0.56, dy=0.50)
        tubel = label("microtubule, schematic", TEXT, 30, BOLD).move_to([-1.2, -1.75, 0])
        clock = VGroup(RoundedRectangle(corner_radius=0.1, width=1.5, height=0.7, color=TEXT),
                       M("0:00", 27, TEXT)).move_to([5.65, 2.9, 0])
        self.play(ReplacementTransform(actin, tube), FadeIn(tubel), FadeIn(clock), run_time=0.95)

        self.at("wears a cap")
        cap = VGroup(*tube[-3:])
        br = Brace(cap, UP, color=GOLD_FRESH, buff=0.15)
        capl = label("GTP cap", GOLD_FRESH, 30, BOLD).next_to(br, UP, buff=0.1)
        tight = chip("tight", GREEN, 28).move_to([4.3, 1.9, 0])
        new = tube_columns(3.16, 3, fresh=3, y=0.0, rows=5, dx=0.56, dy=0.50)
        self.play(GrowFromCenter(br), FadeIn(capl), FadeIn(tight),
                  LaggedStart(*[FadeIn(c, shift=LEFT * 0.25) for c in new], lag_ratio=0.45),
                  Transform(clock[1], M("1:40", 27, TEXT).move_to(clock[0])), run_time=1.5)

        self.at("Behind the cap")
        lattice = label("GDP lattice", BLUE, 30, BOLD).move_to([-2.2, 2.45, 0])
        self.play(FadeIn(lattice), tube[-3].animate.set_color(BLUE), new[0].animate.set_color(BLUE), run_time=0.75)

        self.at("held straight only")
        ties = VGroup()
        ghosts = VGroup()
        for c in tube[3:10:2]:
            ties.add(Line(c[1].get_center(), c[3].get_center(), color=TEXT, stroke_width=2).set_opacity(0.65))
            ghost = Arc(radius=0.7, start_angle=-PI / 2, angle=PI / 2, color=BLUE, stroke_width=3).move_to(c.get_center() + RIGHT * 0.22)
            ghost.set_opacity(0.24); ghosts.add(ghost)
        self.play(Create(ties), FadeIn(ghosts), run_time=0.75)
        self.play(ties.animate.set_stroke(width=5), run_time=0.35, rate_func=there_and_back)
        self.finish()


class S10Catastrophe(SpokenScene):
    def construct(self):
        dots = drifting_field(11, 36, 0.48, 1.05)
        tube = tube_columns(-5.8, 18, fresh=3, y=0.65, rows=5, dx=0.56, dy=0.46)
        cap = VGroup(*tube[-3:])
        br = Brace(cap, UP, color=GOLD_FRESH, buff=0.12)
        capl = label("GTP cap", GOLD_FRESH, 28, BOLD).next_to(br, UP, buff=0.08)
        tight = chip("tight", GREEN, 28).move_to([4.5, 2.25, 0])
        self.add(dots, tube, br, capl, tight)

        self.at("lost by chance")
        self.play(cap.animate.set_opacity(0.28), br.animate.set_opacity(0.28), capl.animate.set_opacity(0.28), run_time=0.4)
        self.play(cap.animate.set_opacity(1), br.animate.set_opacity(1), capl.animate.set_opacity(1), run_time=0.4)

        self.at("growth slows")
        self.play(dots.animate.set_opacity(0.28), cap[-1].animate.set_color(BLUE), run_time=0.65)
        self.play(cap[-2].animate.set_color(BLUE), cap[-3].animate.set_color(BLUE), FadeOut(br), FadeOut(capl), run_time=0.85)

        self.at("turns loose")
        loose = chip("loose", RED, 28).move_to(tight)
        self.play(ReplacementTransform(tight, loose), run_time=0.55)

        self.at("peel outward")
        peeling = VGroup(*[c.copy() for c in tube[-6:]])
        self.add(peeling); self.remove(*tube[-6:])
        anims = []
        for ci, col in enumerate(reversed(peeling)):
            for ri, b in enumerate(col):
                sgn = ri - 2
                anims.append(b.animate.shift(RIGHT * (0.45 + 0.08 * ci) + UP * sgn * 0.42)
                             .rotate(-0.16 * sgn).set_opacity(0.05))
        self.play(LaggedStart(*anims, lag_ratio=0.02), run_time=1.2)

        # Bottom strip is schematic length versus time, computed from explicit piecewise rates.
        origin = np.array([-5.4, -3.0, 0])
        xaxis = Line(origin, origin + RIGHT * 10.5, color=TEXT, stroke_width=2)
        yaxis = Line(origin, origin + UP * 1.25, color=TEXT, stroke_width=2)
        note = label("length vs time — schematic", TEXT, 24).move_to([-2.7, -3.34, 0])
        times = np.array([0.0, 7.0, 8.4, 11.0])
        lengths = np.array([0.15, 0.95, 0.22, 0.58])
        pts = [origin + RIGHT * (t / 11.0 * 10.2) + UP * (l * 1.15) for t, l in zip(times, lengths)]
        rise1 = Line(pts[0], pts[1], color=GREEN, stroke_width=6)
        drop = Line(pts[1], pts[2], color=RED, stroke_width=6)
        rise2 = Line(pts[2], pts[3], color=GREEN, stroke_width=6)

        self.at("shortens many times faster")
        self.play(Create(xaxis), Create(yaxis), FadeIn(note), Create(rise1), run_time=0.65)
        self.play(Create(drop), LaggedStart(*[FadeOut(c, shift=LEFT * 0.15) for c in reversed(tube[8:12])], lag_ratio=0.18), run_time=0.7)

        self.at("switch is a catastrophe")
        catdot = Dot(pts[1], radius=0.12, color=RED)
        cat = label("catastrophe", RED, 28, BOLD).next_to(catdot, UP, buff=0.1)
        self.play(FadeIn(catdot), FadeIn(cat), run_time=0.55)

        self.at("starting again is a rescue")
        rescue_dot = Dot(pts[2], radius=0.12, color=GREEN)
        rescue = label("rescue", GREEN, 28, BOLD).next_to(rescue_dot, DOWN, buff=0.1)
        newcap = tube_columns(0.92, 2, fresh=2, y=0.65, rows=5, dx=0.56, dy=0.46)
        tight2 = chip("tight", GREEN, 28).move_to(loose)
        self.play(Create(rise2), FadeIn(rescue_dot), FadeIn(rescue), ReplacementTransform(loose, tight2),
                  LaggedStart(*[FadeIn(c, shift=LEFT * 0.25) for c in newcap], lag_ratio=0.45), run_time=0.9)
        self.finish()


class S11Return(SpokenScene):
    def construct(self):
        dots = drifting_field(12, 32, 0.38, 1.0)
        tube = tube_columns(-5.7, 15, fresh=0, y=0.0, rows=5, dx=0.55, dy=0.46)
        fray = VGroup(*[c.copy() for c in tube[-3:]])
        self.add(dots, tube)

        self.at("commits an end")
        q = chip("?  debated", RED, 30).move_to([3.2, 2.45, 0])
        self.play(FadeIn(q), fray.animate.shift(RIGHT * 0.35), run_time=0.7)

        self.at("other proteins")
        proteins = VGroup(*[chip("accessory protein", TEXT, 24) for _ in range(3)]).arrange(DOWN, buff=0.12).move_to([4.65, 0.15, 0])
        clocks = VGroup(M("rate  ×2", 26, GREEN), M("rate  ×0.5", 26, RED)).arrange(DOWN, buff=0.16).move_to([4.7, -1.6, 0])
        self.play(FadeIn(proteins, shift=LEFT * 0.25), FadeIn(clocks), run_time=0.8)
        self.play(Indicate(clocks[0], color=GREEN), Indicate(clocks[1], color=RED), run_time=0.65)

        self.at("Hydrolysis gives tight")
        self.play(FadeOut(VGroup(tube, q, proteins, clocks)), run_time=0.5)
        divider = Line([0, -2.8, 0], [0, 2.8, 0], color=TEXT, stroke_width=2).set_opacity(0.5)
        cube = Square(1.25, color=GOLD_FRESH, fill_color=GOLD_FRESH, fill_opacity=0.28, stroke_width=4).move_to([-3.8, 0.1, 0])
        settles = label("crystal settles", GOLD_FRESH, 30, BOLD).move_to([-3.8, -1.15, 0])
        mt = tube_columns(0.65, 10, fresh=2, y=1.25, rows=3, dx=0.47, dy=0.42)
        act = filament(np.arange(0.7, 5.55, 0.47), [BLUE] * 7 + [GOLD_FRESH] * 4, y=-1.15)
        tags = VGroup(chip("tight", GREEN, 24).move_to([5.5, 2.15, 0]),
                      chip("loose", RED, 24).move_to([0.75, -2.05, 0]))
        self.play(Create(divider), FadeIn(cube), FadeIn(settles), FadeIn(mt), FadeIn(act), FadeIn(tags), run_time=0.9)

        self.at("cannot simply settle")
        self.play(mt[-1].animate.shift(RIGHT * 0.4).set_opacity(0),
                  act[0].animate.shift(LEFT * 0.5).set_opacity(0),
                  Indicate(tags, color=TEXT, scale_factor=1.04), run_time=0.8)

        self.at("search their interior")
        self.play(FadeOut(VGroup(divider, cube, settles, mt, act, tags)), run_time=0.45)
        cell = Ellipse(width=11.8, height=6.3, color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.025)
        center = RoundedRectangle(corner_radius=0.12, width=1.15, height=0.85,
                                  color=GREY, fill_color=GREY, fill_opacity=0.35)
        target = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.8,
                                  color=GOLD_FRESH, fill_color=GOLD_FRESH, fill_opacity=0.35).move_to([5.0, 1.5, 0])
        angles = np.linspace(-2.3, 2.3, 9)
        rays = VGroup(*[Line(center.get_center(), 1.0 * np.array([np.cos(a), np.sin(a), 0]),
                            color=BLUE, stroke_width=6) for a in angles])
        self.play(Create(cell), FadeIn(center), FadeIn(target), Create(rays), run_time=0.8)
        ends = [4.8, 4.2, 5.0, 3.8, 5.0, 4.0, 4.7, 4.1, 4.9]
        long_rays = VGroup(*[Line(ORIGIN, r * np.array([np.cos(a), np.sin(a), 0]), color=BLUE, stroke_width=6)
                             for a, r in zip(angles, ends)])
        self.play(Transform(rays, long_rays), run_time=1.5, rate_func=linear)
        hit = Line(ORIGIN, target.get_center(), color=GREEN, stroke_width=7)
        self.play(Transform(rays[6], hit), Indicate(target, color=GREEN, scale_factor=1.2),
                  rays[1].animate.scale(0.55, about_point=ORIGIN), rays[3].animate.scale(0.65, about_point=ORIGIN), run_time=0.8)
        self.at("and rebuild")
        self.play(rays[0].animate.scale(0.65, about_point=ORIGIN),
                  rays[5].animate.scale(1.18, about_point=ORIGIN), run_time=0.75)
        self.finish()


class S12End(EndCard):
    LINE = "Hydrolysis gives tight and loose ends, so the polymer cannot simply settle."

    def construct(self):
        dots = drifting_field(13, 28, 0.20, 0.8)
        self.add(dots)
        super().construct()
