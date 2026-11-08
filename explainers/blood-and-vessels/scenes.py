"""Blood slows in capillaries: velocity = volume flow / cross-sectional area (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  PINK   = blood (cells moving in a vessel)
  BLUE   = volume flow
  YELLOW = velocity (how fast)
  GREEN  = cross-sectional area
  ORANGE = blood (hydrostatic) pressure pushing fluid out
  TEAL   = plasma proteins pulling water in
  GREY   = vessel walls, structure, labels
  RED    = "not the reason" (crossed out)
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#D77AB8"
ORANGE = "#F29E4C"
PLASMA = TEAL


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def tube(x0, x1, cy, h, color=GREY):
    return RoundedRectangle(corner_radius=min(0.25, h / 2.5), width=x1 - x0, height=h, stroke_color=color,
                            stroke_width=4, fill_color=color, fill_opacity=0.12).move_to([(x0 + x1) / 2, cy, 0])


def bed(x0, x1, cy, total_h, n=7, bar_h=0.16):
    """many thin capillary bars side by side (a drawn stand-in, not a count)."""
    ys = np.linspace(cy + total_h / 2 - bar_h / 2, cy - total_h / 2 + bar_h / 2, n)
    bars = VGroup(*[tube(x0, x1, y, bar_h) for y in ys])
    return bars, ys


def cells(x0, x1, ys, speed, per=3, seed=1, r=0.07, jitter=0.0):
    """pink blood dots that drift left to right at `speed` units per second, wrapping at the end."""
    rnd = random.Random(seed)
    g = VGroup()
    L = x1 - x0
    for y in ys:
        for k in range(per):
            d = Dot(radius=r, color=PINK).move_to([x0 + (k + rnd.random() * 0.6) * L / per, y + rnd.uniform(-jitter, jitter), 0])
            d.set_opacity(0.95)

            def up(m, dt, s=speed):
                m.shift(RIGHT * s * dt)
                if m.get_center()[0] > x1 - 0.1:
                    m.shift(LEFT * (L - 0.2))
            d.add_updater(up)
            g.add(d)
    return g


def stop(g):
    for d in g:
        d.clear_updaters()


def lbl(text, size=24, color=GREY):
    return T(text, size, color)


class S00Title(TitleCard):
    LESSON = "Blood vessels, blood and lymph"
    TITLE = "Why blood slows in capillaries"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        names = ["heart", "arteries", "arterioles", "capillaries", "veins"]
        chips = VGroup(*[chip(n, GREY, size=24, pad=0.16) for n in names]).arrange(RIGHT, buff=0.5)
        arrows = VGroup(*[arr(chips[i].get_right(), chips[i + 1].get_left(), GREY, 4, 0.18) for i in range(4)])
        row = VGroup(chips, arrows)
        fit(row, max_w=12.2)
        row.move_to([0, 3.0, 0])
        tag = lbl("adult human at rest", 22).move_to([0, 2.3, 0])

        aor = tube(-6.2, -1.7, -0.5, 1.9)
        bars, ys = bed(1.7, 6.2, -0.5, 2.5)
        aor_l = lbl("aorta", 28).move_to([-3.95, -1.95, 0])
        bed_l = lbl("capillaries", 28).move_to([3.95, -2.05, 0])
        c_a = cells(-6.1, -1.8, [-0.2, -0.5, -0.8], 4.2, per=2, seed=3, r=0.1)
        c_b = cells(1.8, 6.1, list(ys), 0.5, per=2, seed=5, r=0.06)

        self.at("leaves the heart")
        self.play(FadeIn(chips[0]), run_time=0.3)
        for i in range(4):
            self.play(GrowArrow(arrows[i]), FadeIn(chips[i + 1]), run_time=0.45)
        self.play(FadeIn(tag), run_time=0.3)
        self.at("fastest")
        self.play(Create(aor), FadeIn(aor_l), run_time=0.6)
        self.add(c_a)
        fa = arr([-6.0, -3.0, 0], [-2.0, -3.0, 0], YELLOW, 8, 0.3)
        fl = lbl("fast", 30, YELLOW).next_to(fa, UP, buff=0.05)
        self.play(GrowArrow(fa), FadeIn(fl), run_time=0.5)
        self.at("slowest in the capillaries")
        self.play(Create(bars), FadeIn(bed_l), run_time=0.7)
        self.add(c_b)
        sa = arr([2.0, -3.0, 0], [3.0, -3.0, 0], YELLOW, 8, 0.3)
        sl = lbl("slow", 30, YELLOW).next_to(sa, UP, buff=0.05)
        self.play(GrowArrow(sa), FadeIn(sl), run_time=0.5)
        self.at("sounds backward")
        q = T("?", 96, GOLD, weight=BOLD).move_to([0, -0.5, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("why is blood slowest")
        self.play(Indicate(q, color=GOLD, scale_factor=1.25), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Flow(SpokenScene):
    def construct(self):
        c1 = VGroup(chip("volume flow", BLUE, size=30), lbl("how much blood passes a point", 24)).arrange(DOWN, buff=0.2)
        c2 = VGroup(chip("velocity", YELLOW, size=30), lbl("how fast the blood moves", 24)).arrange(DOWN, buff=0.2)
        c1.move_to([-3.4, 2.7, 0])
        c2.move_to([3.4, 2.7, 0])

        aor = tube(-6.2, -2.3, -0.6, 1.9)
        bars, ys = bed(2.3, 6.2, -0.6, 2.5)
        aor_l = lbl("aorta", 28).move_to([-4.25, -2.1, 0])
        bed_l = lbl("all the capillaries together", 26).move_to([3.7, -2.35, 0])
        eq = T("=", 64, TEXT, weight=BOLD).move_to([0, -0.6, 0])
        c_a = cells(-6.1, -2.4, [-0.3, -0.6, -0.9], 3.0, per=2, seed=3, r=0.1)
        c_b = cells(2.4, 6.1, list(ys), 0.4, per=2, seed=5, r=0.06)
        fa = chip("volume flow", BLUE, size=24).move_to([-4.25, -3.0, 0])
        fb = chip("volume flow", BLUE, size=24).move_to([4.25, -3.2, 0])

        self.at("Volume flow is")
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.6)
        self.at("Velocity is")
        self.play(FadeIn(c2, shift=DOWN * 0.2), run_time=0.6)
        self.at("steady state")
        self.play(Create(aor), FadeIn(aor_l), run_time=0.5)
        self.add(c_a)
        self.at("that")
        self.play(FadeIn(fa), run_time=0.4)
        self.at("passes through the capillaries")
        self.play(Create(bars), FadeIn(bed_l), run_time=0.7)
        self.add(c_b)
        self.at("volume flow through all")
        self.play(FadeIn(fb, shift=UP * 0.2), FadeIn(eq, scale=0.6), run_time=0.6)
        self.at("equals the flow")
        self.play(Indicate(fa, color=BLUE), Indicate(fb, color=BLUE), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Area(SpokenScene):
    def construct(self):
        v = T("velocity", 40, YELLOW, weight=BOLD)
        eqs = T("=", 40, TEXT)
        f = T("volume flow", 40, BLUE, weight=BOLD)
        d = T("÷", 40, TEXT)
        a = T("cross-sectional area", 40, GREEN, weight=BOLD)
        formula = VGroup(v, eqs, f, d, a).arrange(RIGHT, buff=0.3).move_to([0, 3.0, 0])
        fit(formula, max_w=12.2)

        small = Square(side_length=0.9, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.35).move_to([-5.3, -0.3, 0])
        sm_l = lbl("aorta", 26).next_to(small, DOWN, buff=0.3)
        cols, rows, s = 20, 8, 0.34
        grid = VGroup(*[Square(side_length=s, stroke_color=GREEN, stroke_width=1.5, fill_color=GREEN, fill_opacity=0.3)
                        for _ in range(cols * rows)]).arrange_in_grid(rows, cols, buff=0.04)
        grid.move_to([2.3, -0.3, 0])
        gr_l = lbl("all the capillaries together", 26).next_to(grid, DOWN, buff=0.3)
        note = lbl("cross-sections, not to scale", 22).move_to([0, -3.5, 0])
        lower = chip("lower velocity", YELLOW, size=26).move_to([2.3, 1.95, 0])

        self.at("Velocity equals")
        self.play(FadeIn(v), FadeIn(eqs), run_time=0.4)
        self.play(FadeIn(f, shift=RIGHT * 0.2), FadeIn(d), run_time=0.5)
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.5)
        self.at("flow is the same")
        self.play(Indicate(f, color=BLUE, scale_factor=1.06), run_time=0.8)
        self.at("larger area")
        self.play(FadeIn(small, scale=0.8), FadeIn(sm_l), run_time=0.5)
        self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(gr_l), FadeIn(note), run_time=1.0)
        self.at("lower velocity")
        self.play(FadeIn(lower, shift=DOWN * 0.15), run_time=0.5)
        self.at("Each capillary is tiny")
        one = grid[0].copy()
        self.play(grid[0].animate.set_fill(YELLOW, 0.9).set_stroke(YELLOW, 3), run_time=0.5)
        self.at("so many side by side")
        self.play(Indicate(grid, color=GREEN, scale_factor=1.03), run_time=0.8)
        self.at("far exceeds")
        self.play(grid[0].animate.set_fill(GREEN, 0.3).set_stroke(GREEN, 1.5), Indicate(small, color=GREEN, scale_factor=1.3), run_time=0.8)
        self.at("tubes in parallel")
        self.play(Indicate(grid, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Numbers(SpokenScene):
    def construct(self):
        head = lbl("made-up round numbers, adult human at rest", 26).move_to([-1.9, 3.2, 0])

        def line(label, math, col):
            return VGroup(T(label, 26, col), M(math, 28, TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        l1 = line("volume flow", "5 L/min ≈ 83 cm³/s", BLUE)
        l2 = line("aorta, 4 cm²", "83 ÷ 4 ≈ 21 cm/s", YELLOW)
        l3 = line("capillaries, 3,000 cm²", "83 ÷ 3,000 ≈ 0.03 cm/s", YELLOW)
        col = VGroup(l1, l2, l3).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([-3.0, -0.2, 0])

        base_y, x_a, x_c, unit = -2.6, 3.3, 5.1, 0.17
        axis = Line([2.3, base_y, 0], [6.6, base_y, 0], color=GREY, stroke_width=3)
        bar_a = Rectangle(width=1.1, height=21 * unit, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.5, stroke_width=3)
        bar_a.move_to([x_a, base_y + 21 * unit / 2, 0])
        bar_c = Rectangle(width=1.1, height=max(0.03 * unit, 0.03), stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.9, stroke_width=3)
        bar_c.move_to([x_c, base_y + bar_c.height / 2, 0])
        la = lbl("aorta", 24).next_to(axis, DOWN, buff=0.15).set_x(x_a)
        lc = lbl("capillaries", 24).next_to(axis, DOWN, buff=0.15).set_x(x_c)
        ua = M("21", 26, YELLOW).next_to(bar_a, UP, buff=0.12)
        uc = VGroup(M("0.03 cm/s", 24, YELLOW), T("too small to see", 22, GREY), T("on this scale", 22, GREY)).arrange(DOWN, buff=0.06).move_to([x_c + 0.25, base_y + 0.95, 0])
        ax_t = lbl("velocity, cm/s (linear)", 22).move_to([4.5, 3.2, 0])

        self.at("round numbers")
        self.play(FadeIn(head), run_time=0.5)
        self.at("liters per minute")
        self.play(FadeIn(l1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("Through")
        self.play(FadeIn(l2, shift=RIGHT * 0.2), FadeIn(ax_t), Create(axis), FadeIn(la), run_time=0.7)
        self.play(GrowFromEdge(bar_a, DOWN), FadeIn(ua), run_time=0.8)
        self.at("Spread over")
        self.play(FadeIn(l3, shift=RIGHT * 0.2), FadeIn(lc), run_time=0.7)
        self.play(GrowFromEdge(bar_c, DOWN), FadeIn(uc), run_time=0.6)
        self.at("it is about")
        self.play(Indicate(bar_c, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Exchange(SpokenScene):
    def construct(self):
        cy, x0, x1 = 0.6, -5.8, 5.8
        wall_t = Line([x0, cy + 1.0, 0], [x1, cy + 1.0, 0], color=GREY, stroke_width=8)
        wall_b = Line([x0, cy - 1.0, 0], [x1, cy - 1.0, 0], color=GREY, stroke_width=8)
        lumen = Rectangle(width=x1 - x0, height=2.0, stroke_width=0, fill_color=PINK, fill_opacity=0.10).move_to([0, cy, 0])
        cap = VGroup(lumen, wall_t, wall_b)
        c_in = cells(x0 + 0.1, x1 - 0.1, [cy + 0.4, cy - 0.4], 0.5, per=6, seed=7, r=0.1)
        wall_l = lbl("wall: one layer of endothelial cells", 24).move_to([1.5, cy + 1.45, 0])
        fl_l = lbl("tissue fluid", 24).move_to([-4.8, -3.3, 0])
        flow = arr([-5.5, cy, 0], [-3.9, cy, 0], PINK, 5, 0.22)
        flow_l = chip("slow blood", PINK, size=24, pad=0.12).move_to([-4.6, cy + 1.5, 0])

        # step 1: one arrow out, one in
        out1 = arr([-2.4, cy - 1.05, 0], [-2.4, cy - 2.0, 0], ORANGE, 8, 0.3)
        in1 = arr([3.0, cy - 2.0, 0], [3.0, cy - 1.05, 0], PLASMA, 8, 0.3)
        out1_l = lbl("blood pressure pushes fluid out", 24, ORANGE).move_to([-2.4, -2.3, 0])
        in1_l = lbl("plasma proteins pull water in", 24, PLASMA).move_to([3.0, -2.3, 0])
        # classic: out at the arterial end, in at the venous end
        ca = arr([-4.3, cy - 1.05, 0], [-4.3, cy - 2.85, 0], ORANGE, 9, 0.32)
        cv = arr([4.3, cy - 1.9, 0], [4.3, cy - 1.05, 0], PLASMA, 9, 0.32)
        art = lbl("arterial end", 24).move_to([-4.3, cy + 1.45, 0])
        ven = lbl("venous end", 24).move_to([4.3, cy + 1.45, 0])
        classic = chip("classic textbook model", GREY, size=26, pad=0.14).move_to([0, 3.4, 0])
        # reviews: filtration along the length, lymph takes it
        rev = chip("reviews: steady return at the venous end\nlacks reproducible support as a general account", ORANGE, size=24, pad=0.14).move_to([0, 3.2, 0])
        outs = VGroup(*[arr([x, cy - 1.05, 0], [x, cy - 1.95, 0], ORANGE, 6, 0.22) for x in (-4.0, -1.3, 1.4, 4.1)])
        lym = chip("lymph", GREEN, size=26).move_to([3.7, -2.9, 0])
        lym_a = arr([-0.6, -2.9, 0], [2.8, -2.9, 0], GREEN, 6, 0.25)

        self.at("exchange")
        self.play(Create(cap), FadeIn(fl_l), run_time=0.8)
        self.add(c_in)
        self.play(GrowArrow(flow), FadeIn(flow_l), run_time=0.4)
        self.at("single layer")
        self.play(FadeIn(wall_l), run_time=0.5)
        self.play(Indicate(wall_l, color=TEXT, scale_factor=1.04), run_time=0.5)
        self.at("pushes fluid out")
        self.play(GrowArrow(out1), FadeIn(out1_l), run_time=0.6)
        self.at("pull water")
        self.play(GrowArrow(in1), FadeIn(in1_l), run_time=0.6)
        self.at("classic textbook model")
        self.play(FadeOut(VGroup(out1, in1, out1_l, in1_l, wall_l, flow_l)), FadeIn(classic), FadeIn(art), FadeIn(ven), run_time=0.5)
        self.at("leaving at the arterial")
        self.play(GrowArrow(ca), run_time=0.5)
        self.at("returning at the venous")
        self.play(GrowArrow(cv), run_time=0.5)
        self.at("Reviews conclude")
        self.play(FadeOut(VGroup(classic, ca, cv, art, ven)), FadeIn(rev), run_time=0.5)
        self.at("most tissues filter slowly")
        self.play(LaggedStart(*[GrowArrow(o) for o in outs], lag_ratio=0.2), run_time=1.0)
        self.at("lymph returns")
        self.play(FadeIn(lym), GrowArrow(lym_a), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        v = T("velocity", 36, YELLOW, weight=BOLD)
        eqs = T("=", 36, TEXT)
        f = T("volume flow", 36, BLUE, weight=BOLD)
        d = T("÷", 36, TEXT)
        a = T("cross-sectional area", 36, GREEN, weight=BOLD)
        formula = VGroup(v, eqs, f, d, a).arrange(RIGHT, buff=0.3).move_to([0, 3.35, 0])
        fit(formula, max_w=12.2)

        aor = tube(-6.2, -2.0, 0.6, 2.4)
        bars, ys = bed(2.0, 6.2, 0.6, 3.0)
        aor_l = lbl("aorta", 28).move_to([-4.1, -1.0, 0])
        brace = Brace(bars, DOWN, color=GREEN, buff=0.15)
        tot = lbl("together: largest cross-section", 26, GREEN).next_to(brace, DOWN, buff=0.15).set_x(3.6)
        nar = chip("each one narrow", RED, size=26).move_to([0, 2.3, 0])
        x1 = Line(nar.get_corner(UL), nar.get_corner(DR), color=RED, stroke_width=6)
        x2 = Line(nar.get_corner(UR), nar.get_corner(DL), color=RED, stroke_width=6)
        slow = chip("wide channel, slow blood", YELLOW, size=28).move_to([0, -3.1, 0])
        c_a = cells(-6.1, -2.1, [0.9, 0.6, 0.3], 3.0, per=2, seed=3, r=0.1)
        c_b = cells(2.1, 6.1, list(ys), 0.4, per=2, seed=5, r=0.06)

        self.at("Keep one rule")
        self.play(FadeIn(formula, shift=DOWN * 0.15), run_time=0.7)
        self.play(Create(aor), FadeIn(aor_l), Create(bars), run_time=0.8)
        self.add(c_a, c_b)
        self.at("together they have")
        self.play(GrowFromCenter(brace), FadeIn(tot), Indicate(a, color=GREEN, scale_factor=1.06), run_time=0.8)
        self.at("Each one being narrow")
        self.play(FadeIn(nar), run_time=0.4)
        self.play(Create(x1), Create(x2), run_time=0.5)
        self.at("Many tiny tubes")
        self.play(FadeOut(VGroup(nar, x1, x2)), run_time=0.4)
        self.play(FadeIn(slow, scale=0.9), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Blood is slowest where the combined cross-section is largest."
