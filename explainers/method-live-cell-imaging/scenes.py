"""Live-cell time-lapse imaging: filming what one cell does next  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREEN  = the fluorescent label, and a green (S, G2, M) nucleus
  RED    = a red (G0, G1) nucleus
  BLUE   = excitation light and the microscope
  YELLOW = tracks, rings and the quantity read from a track (distance, rate)
  GREY   = cells, frames, structure, de-emphasised text
  ORANGE = damage from light
  TEAL   = a control, and the open question marks' answers
  PURPLE = Rab5       PINK = Rab7
  GOLD   = dates, source tags and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E86FA5"
DIM_G = "#2F5A3A"      # a dim, faded green nucleus
SCREEN = "#05080C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), buff=0.0, color=color, stroke_width=w,
                 tip_length=tip, max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def cellg(x, y, r=0.34, nuc=GREEN, nr=0.5, op=1.0):
    """A cell: grey outline with a nucleus (colour = reporter state)."""
    body = Circle(radius=r, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.12).move_to([x, y, 0])
    if nuc is None:
        return VGroup(body)
    n = Circle(radius=r * nr, stroke_width=0, fill_color=nuc, fill_opacity=op).move_to([x, y, 0])
    return VGroup(body, n)


def screen(cx, cy, w, h, color=GREY):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=SCREEN,
                     fill_opacity=1.0).move_to([cx, cy, 0])


def sine(x0, x1, y, period, amp, color, w=5):
    xs = np.linspace(x0, x1, 160)
    return poly([[x, y + amp * np.sin(2 * np.pi * (x - x0) / period)] for x in xs], color, w)


def gold_tag(text, size=24):
    return T(text, size, GOLD)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Filming What One Cell Does Next"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a fixed picture cannot say who moved, what came first or who divided; film can."""

    def construct(self):
        # --- one fixed picture
        px, py, pw, ph = -2.2, 0.55, 8.2, 4.7
        panel = screen(px, py, pw, ph)
        pos = [(-5.0, 1.6), (-3.7, -0.2), (-2.2, 1.9), (-1.2, 0.2), (-3.0, -1.4), (-0.4, 1.6), (-1.8, -1.2), (-4.9, -0.8)]
        cells = VGroup(*[cellg(x, y + 0.2, 0.42, GREEN) for x, y in pos])
        cap = lab("one fixed, stained picture", 26, GREY).move_to([px, py - ph / 2 - 0.35, 0])
        dead = lab("a fixed cell is dead", 26, TEXT).move_to([px, py - ph / 2 - 0.9, 0])
        self.at("A fixed")
        self.play(FadeIn(panel), LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.1), run_time=1.2)
        self.play(FadeIn(cap), FadeIn(dead))

        q1 = chip("which cell moved?", YELLOW, 28).move_to([4.7, 2.5, 0])
        q2 = chip("which came first?", YELLOW, 28).move_to([4.7, 0.6, 0])
        q3 = chip("did it divide?", YELLOW, 28).move_to([4.7, -1.3, 0])
        ring = Circle(radius=0.58, stroke_color=YELLOW, stroke_width=4).move_to(cells[3].get_center())
        self.at("which cell moved")
        self.play(FadeIn(q1, shift=LEFT * 0.2), run_time=0.5)
        self.at("which event came first")
        self.play(FadeIn(q2, shift=LEFT * 0.2), run_time=0.5)
        self.at("whether a green cell")
        self.play(FadeIn(q3, shift=LEFT * 0.2), Create(ring), run_time=0.6)

        # --- film
        self.at("Film answers")
        self.play(FadeOut(VGroup(panel, cells, cap, dead, q1, q2, q3, ring)), run_time=0.5)
        fw, fh, gap = 2.85, 3.0, 0.27
        xs = [-6.3 + fw / 2 + i * (fw + gap) for i in range(4)]
        fy = 0.8
        frames = [screen(x, fy, fw, fh) for x in xs]
        # local positions per frame: A drifts right, B stays, C moves and divides in frame 4
        A = [(-0.85, 0.7), (-0.6, 0.75), (-0.35, 0.8), (-0.1, 0.85)]
        B = [(0.8, 1.0), (0.8, 1.0), (0.8, 1.0), (0.8, 1.0)]
        C = [(-0.7, -0.5), (-0.4, -0.45), (-0.1, -0.5), None]
        g = VGroup()
        for i, x in enumerate(xs):
            g.add(cellg(x + A[i][0], fy + A[i][1], 0.36, GREEN))
            g.add(cellg(x + B[i][0], fy + B[i][1] - 0.3, 0.36, GREEN))
            if C[i]:
                g.add(cellg(x + C[i][0], fy + C[i][1], 0.36, GREEN))
            else:
                g.add(cellg(x - 0.05, fy - 0.45, 0.26, GREEN), cellg(x + 0.55, fy - 0.45, 0.26, GREEN))
        tarrow = arr([-6.0, -1.1], [6.0, -1.1], GREY, 4)
        tl = lab("time", 24, GREY).next_to(tarrow, DOWN, buff=0.12).align_to(tarrow, RIGHT)
        self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.25),
                  LaggedStart(*[FadeIn(g[k]) for k in range(len(g))], lag_ratio=0.02), run_time=0.9)
        self.play(GrowArrow(tarrow), FadeIn(tl), run_time=0.3)
        c1 = chip("in what order", GREEN, 26).move_to([-4.3, -2.7, 0])
        c2 = chip("how fast", GREEN, 26).move_to([-0.9, -2.7, 0])
        c3 = chip("what did this cell do next", GREEN, 26).move_to([3.7, -2.7, 0])
        self.at("in what order")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.4)
        self.at("how fast")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.4)
        self.at("what did this particular")
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Label(SpokenScene):
    """the cell makes its own label; the microscope sees only the label."""

    def construct(self):
        # --- phase A: tag a protein
        cell = Circle(radius=2.3, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.10).move_to([0, -0.5, 0])
        nuc = Circle(radius=0.8, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.12).move_to([-0.3, -0.7, 0])
        self.at("cell makes")
        self.play(FadeIn(cell), FadeIn(nuc), run_time=0.8)
        prot = chip("protein of interest", GREY, 30).move_to([-3.0, 2.9, 0])
        tagc = chip("fluorescent protein tag", GREEN, 30).move_to([3.0, 2.9, 0])
        self.at("A protein of interest")
        self.play(FadeIn(prot, shift=DOWN * 0.15), run_time=0.5)
        self.at("tagged with a genetically")
        self.play(FadeIn(tagc, shift=DOWN * 0.15), run_time=0.5)
        pair = VGroup(prot, tagc)
        self.play(tagc.animate.next_to(prot, RIGHT, buff=0.0), run_time=0.4)
        rng = np.random.RandomState(4)
        dots = VGroup()
        for _ in range(9):
            a = rng.rand() * 2 * np.pi
            r = 0.8 + rng.rand() * 1.1
            dots.add(Dot([r * np.cos(a), -0.5 + r * np.sin(a) * 0.9, 0], radius=0.11, color=GREEN))
        made = lab("the cell makes the label itself", 26, GREEN).move_to([0, -3.35, 0])
        self.at("encoded fluorescent protein")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.1), FadeIn(made), run_time=1.0)
        date = gold_tag("GFP fluorescence shown in E. coli and C. elegans, 1994", 26).move_to([0, -3.35, 0])
        self.at("green fluorescent protein")
        self.play(FadeOut(made, run_time=0.2))
        self.play(FadeIn(date), run_time=0.4)

        # --- phase B: seeing only the label
        self.at("A fluorescence microscope")
        self.play(FadeOut(pair), FadeOut(date), FadeOut(nuc), run_time=0.2)
        small = VGroup(cell, dots)
        self.play(small.animate.scale(0.62).move_to([-3.4, 0.2, 0]), run_time=0.4)
        blue = sine(-6.2, -4.7, 0.2, 0.34, 0.32, BLUE, 5)
        green = sine(-1.6, 0.1, 0.2, 0.85, 0.32, GREEN, 5)
        bl = lab("excitation\nlight", 24, BLUE).move_to([-5.6, 1.2, 0])
        gl = lab("longer-wavelength\nlight", 24, GREEN).move_to([-1.0, -1.6, 0])
        filt = Rectangle(width=0.22, height=4.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3).move_to([0.9, 0.2, 0])
        fl = lab("filter", 24, BLUE).move_to([0.9, -2.6, 0])
        scr = screen(4.6, 0.2, 3.4, 4.4)
        spots = VGroup(*[Dot([4.6 + dx, 0.2 + dy, 0], radius=0.09, color=GREEN) for dx, dy in
                         [(-0.9, 1.4), (0.3, 1.7), (0.9, 0.6), (-0.4, -0.2), (0.7, -1.0), (-1.0, -1.5), (0.0, 0.5)]])
        sl = lab("the tagged protein stands out", 24, TEXT).move_to([4.6, -2.7, 0])
        self.play(Create(blue, run_time=0.3, rate_func=linear), FadeIn(bl))
        self.at("separates the excitation")
        self.play(FadeIn(filt), FadeIn(fl), run_time=0.5)
        self.at("longer wavelength light")
        self.play(Create(green, run_time=0.8, rate_func=linear), FadeIn(gl))
        self.at("stands out")
        self.play(FadeIn(scr), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in spots], lag_ratio=0.1), FadeIn(sl), run_time=0.8)
        self.at("dark background")
        self.wait(0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Film(SpokenScene):
    """living cells on a stage, imaged again and again at a chosen interval."""

    def construct(self):
        # --- stage with dish
        lens = Polygon([-4.6, 3.45, 0], [-1.8, 3.45, 0], [-2.6, 2.35, 0], [-3.8, 2.35, 0], stroke_color=BLUE, stroke_width=4,
                       fill_color=BLUE, fill_opacity=0.18)
        lens_l = lab("lens", 22, BLUE).move_to([-5.3, 2.9, 0])
        dish = RoundedRectangle(corner_radius=0.2, width=4.4, height=1.1, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([-3.2, 1.45, 0])
        dc = VGroup(*[cellg(-4.7 + i * 0.75, 1.45, 0.3, GREEN) for i in range(5)])
        stage = Rectangle(width=5.2, height=0.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to([-3.2, 0.75, 0])
        stl = lab("microscope stage, kept alive", 22, GREY).move_to([-3.2, 0.3, 0])
        self.at("living cells")
        self.play(FadeIn(lens), FadeIn(lens_l), FadeIn(dish), FadeIn(dc), FadeIn(stage), FadeIn(stl), run_time=1.0)
        names = ["cells in a dish", "brain slices", "a transparent larva", "an anaesthetised animal"]
        chips = VGroup(*[chip(n, GREY, 24) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 2.0, 0])
        self.at("cells in a dish")
        self.play(FadeIn(chips[0], shift=LEFT * 0.2), run_time=0.4)
        self.at("brain slices")
        self.play(FadeIn(chips[1], shift=LEFT * 0.2), run_time=0.4)
        self.at("a transparent larva")
        self.play(FadeIn(chips[2], shift=LEFT * 0.2), run_time=0.4)
        self.at("animal")
        self.play(FadeIn(chips[3], shift=LEFT * 0.2), run_time=0.4)

        # --- same field, again and again
        self.at("The same field")
        self.play(FadeOut(chips), run_time=0.4)
        fr = VGroup()
        for i in range(5):
            f = screen(-0.1 + i * 1.5, 2.0, 1.3, 1.3)
            c = cellg(-0.1 + i * 1.5 - 0.3 + 0.12 * i, 2.0 + 0.1, 0.22, GREEN)
            c2 = cellg(-0.1 + i * 1.5 + 0.3, 1.75, 0.22, GREEN)
            fr.add(VGroup(f, c, c2))
        flash = []
        for i in range(5):
            flash.append(AnimationGroup(Flash(lens.get_bottom(), color=BLUE, flash_radius=0.4, line_length=0.2),
                                        FadeIn(fr[i], shift=DOWN * 0.1), run_time=0.45))
        self.play(Succession(*flash))
        # --- the interval
        rows = [("human cell chromosomes", "every 30 s", 0.3, -0.75),
                ("Arabidopsis ovules", "every 5 min", 1.6, -1.85),
                ("brain slices and cultures", "every few min", 0.9, -2.95)]
        tick_x0, tick_x1 = -0.6, 6.2
        groups = []
        for name, iv, sp, y in rows:
            a = lab(name, 26, TEXT).move_to([-6.2, y + 0.2, 0], aligned_edge=LEFT) if False else lab(name, 26, TEXT)
            a.move_to([-6.2 + a.width / 2, y + 0.18, 0])
            b = M(iv, 24, YELLOW)
            b.move_to([-6.2 + b.width / 2, y - 0.2, 0])
            base = Line([tick_x0, y, 0], [tick_x1, y, 0], color=GREY, stroke_width=2.5)
            ticks = VGroup(*[Line([x, y - 0.22, 0], [x, y + 0.22, 0], color=YELLOW, stroke_width=3)
                             for x in np.arange(tick_x0 + 0.1, tick_x1, sp)])
            groups.append((a, b, base, ticks))
        ex = lab("example intervals, idealised ticks", 22, GREY).move_to([3.1, -3.55, 0])
        self.at("Chromosomes in human")
        self.play(FadeIn(groups[0][0]), FadeIn(groups[0][1]), Create(groups[0][2]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t) for t in groups[0][3]], lag_ratio=0.05), run_time=1.0)
        self.at("Arabidopsis ovules")
        self.play(FadeIn(groups[1][0]), FadeIn(groups[1][1]), Create(groups[1][2]), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t) for t in groups[1][3]], lag_ratio=0.15), run_time=0.8)
        self.at("Brain slices and cultures")
        self.play(FadeIn(groups[2][0]), FadeIn(groups[2][1]), Create(groups[2][2]), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t) for t in groups[2][3]], lag_ratio=0.1), FadeIn(ex), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Track(SpokenScene):
    """follow one cell frame to frame; colour, shape and division read as one history; the cycle reporters."""

    def construct(self):
        fw, fh, gap = 2.3, 3.6, 0.25
        xs = [-6.3 + fw / 2 + i * (fw + gap) for i in range(5)]
        fy = 1.2
        frames = [screen(x, fy, fw, fh) for x in xs]
        # tracked cell local positions, nucleus states
        tr = [(-0.55, 0.1), (-0.25, 0.25), (0.05, 0.3), (0.3, 0.2)]
        other = [(0.55, -0.7), (0.5, -0.6), (0.45, -0.55), (0.4, -0.65), (0.4, -0.6)]
        cs = [RED, RED, GREEN, GREEN]
        objs = VGroup()
        tracked = []
        for i in range(4):
            c = cellg(xs[i] + tr[i][0], fy + tr[i][1], 0.4 if i < 3 else 0.46, cs[i])
            if i == 3:
                c[0].set_stroke(GREY, 3)  # rounded, about to divide
            tracked.append(c)
        d1 = cellg(xs[4] - 0.35, fy + 0.45, 0.28, GREEN, op=0.35)
        d2 = cellg(xs[4] + 0.15, fy + 0.0, 0.28, GREEN, op=0.35)
        tracked.append(VGroup(d1, d2))
        others = [cellg(xs[i] + other[i][0] - 0.1 * (1 if i else 0), fy + other[i][1], 0.3, GREY if False else RED, op=0.5) for i in range(5)]
        self.at("Then each cell")
        self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(o) for o in others], lag_ratio=0.1), run_time=0.6)
        rings = [Circle(radius=0.5, stroke_color=YELLOW, stroke_width=4).move_to(tracked[i][0].get_center()) for i in range(4)]
        rings.append(VGroup(*[Circle(radius=0.38, stroke_color=YELLOW, stroke_width=4).move_to(d[0].get_center()) for d in (d1, d2)]))
        self.at("followed from frame")
        for i in range(5):
            self.play(FadeIn(tracked[i]), Create(rings[i]), run_time=0.3)
        pts = [t[0].get_center() for t in tracked[:4]]
        pts.append((d1[0].get_center() + d2[0].get_center()) / 2)
        track = poly([[p[0], p[1]] for p in pts], YELLOW, 4)
        tk = chip("tracking", YELLOW, 30).move_to([0, 3.55, 0])
        self.at("This is tracking")
        self.play(FadeIn(tk, shift=DOWN * 0.1), Create(track), run_time=0.7)

        # one history bracket
        brace = Brace(VGroup(frames[0], frames[4]), DOWN, color=YELLOW, buff=0.1)
        hist = lab("colour, shape changes, division: one history", 28, YELLOW).next_to(brace, DOWN, buff=0.12)
        self.at("shape changes")
        self.play(GrowFromCenter(brace), FadeIn(hist), run_time=0.8)

        # legend
        leg_r = chip("red nucleus: G0 or G1", RED, 28).move_to([-3.1, -2.95, 0])
        leg_g = chip("green nucleus: S, G2 or M", GREEN, 28).move_to([3.1, -2.95, 0])
        self.at("A red nucleus")
        self.play(FadeOut(hist), FadeOut(brace), run_time=0.3)
        self.play(FadeIn(leg_r, shift=UP * 0.15), Indicate(VGroup(tracked[0][1], tracked[1][1]), color=RED), run_time=0.7)
        self.at("A green nucleus")
        self.play(FadeIn(leg_g, shift=UP * 0.15), Indicate(VGroup(tracked[2][1], tracked[3][1]), color=GREEN), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Read(SpokenScene):
    """read a track: position per frame to rate or order; the colour sequence of one cell cycle."""

    def construct(self):
        ex = lab("example data, idealised", 24, GREY).move_to([0, 3.5, 0])
        # --- distance versus time plot (left)
        ax_o = np.array([-5.9, -0.6])
        axx = arr(ax_o, [-0.5, -0.6], GREY, 4)
        axy = arr(ax_o, [-5.9, 2.9], GREY, 4)
        tl = lab("time", 22, GREY).move_to([-3.2, -1.0, 0])
        dl = lab("distance", 22, GREY).move_to([-5.0, 3.1, 0])
        pts_x = np.linspace(-5.9, -1.0, 8)
        pts_y = -0.6 + 0.4 * np.arange(8) + np.array([0, 0.1, -0.1, 0.15, -0.05, 0.1, 0, 0.05])
        dots = VGroup(*[Dot([x, y, 0], radius=0.1, color=YELLOW) for x, y in zip(pts_x, pts_y)])
        fitl = poly([[pts_x[0], pts_y[0]], [pts_x[-1], pts_y[-1] - 0.02]], YELLOW, 3)
        # rise/run triangle
        tri_a, tri_b = np.array([-4.5, 0.2]), np.array([-2.6, 0.2])
        slope = (pts_y[-1] - pts_y[0]) / (pts_x[-1] - pts_x[0])
        tri_c = np.array([-2.6, 0.2 + slope * 1.9])
        run = poly([tri_a[:2], tri_b[:2]], GREY, 3)
        rise = poly([tri_b[:2], tri_c[:2]], GREY, 3)
        rate = lab("distance over time = rate", 26, YELLOW).move_to([-3.0, -1.8, 0])
        self.at("A movie is read")
        self.play(FadeIn(ex), GrowArrow(axx), GrowArrow(axy), FadeIn(tl), FadeIn(dl), run_time=0.8)
        self.at("Take the position")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.2), run_time=1.6)
        self.at("then measure a rate")
        self.play(Create(fitl), Create(run), Create(rise), FadeIn(rate), run_time=1.0)

        # --- order of events (right)
        ox0 = 0.7
        evx = arr([ox0, -0.6], [6.2, -0.6], GREY, 4)
        evl = lab("time", 22, GREY).move_to([5.7, -1.0, 0])
        b1 = Rectangle(width=2.0, height=0.5, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.35).move_to([1.9, 1.7, 0])
        b2 = Rectangle(width=2.0, height=0.5, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35).move_to([4.2, 0.6, 0])
        t1 = lab("event 1", 24, TEXT).next_to(b1, UP, buff=0.1)
        t2 = lab("event 2", 24, TEXT).next_to(b2, UP, buff=0.1)
        order = lab("or an order of events", 26, TEXT).move_to([3.5, -1.8, 0])
        self.at("or an order")
        self.play(GrowArrow(evx), FadeIn(evl), FadeIn(b1), FadeIn(t1), run_time=0.6)
        self.play(FadeIn(b2), FadeIn(t2), FadeIn(order), run_time=0.6)

        # --- cell-cycle movie
        self.at("On a cell cycle")
        self.play(FadeOut(VGroup(ex, axx, axy, tl, dl, dots, fitl, run, rise, rate, evx, evl, b1, b2, t1, t2, order)), run_time=0.5)
        ex2 = lab("example, idealised", 24, GREY).move_to([5.0, 3.5, 0])
        xs = [-5.0, -1.7, 1.6, 4.5]
        y = 0.7
        c_red = cellg(xs[0], y, 1.0, RED)
        c_grn = cellg(xs[1], y, 1.0, GREEN)
        c_rnd = cellg(xs[2], y, 1.15, GREEN, nr=0.65)
        c_rnd[0].set_stroke(GREY, 4)
        d_a = cellg(xs[3] - 0.6, y + 0.55, 0.65, GREEN, op=0.35)
        d_b = cellg(xs[3] + 0.6, y - 0.55, 0.65, GREEN, op=0.35)
        d_both = VGroup(d_a, d_b)
        lbls = [lab("red", 28, RED).next_to(c_red, DOWN, buff=0.3),
                lab("then green", 28, GREEN).next_to(c_grn, DOWN, buff=0.3),
                lab("dividing", 28, TEXT).next_to(c_rnd, DOWN, buff=0.3),
                lab("two dim daughters", 28, GREEN).move_to([xs[3], y - 1.6, 0])]
        arrs = [arr([xs[i] + 1.15, y], [xs[i + 1] - 1.25, y], GREY, 4) for i in range(3)]
        self.play(FadeIn(ex2), run_time=0.3)
        self.at("red")
        self.play(FadeIn(c_red, scale=0.7), FadeIn(lbls[0]), run_time=0.5)
        self.at("then green")
        self.play(GrowArrow(arrs[0]), FadeIn(c_grn, scale=0.7), FadeIn(lbls[1]), run_time=0.6)
        self.at("then a rounded")
        self.play(GrowArrow(arrs[1]), FadeIn(c_rnd, scale=0.7), FadeIn(lbls[2]), run_time=0.6)
        self.at("then two dim")
        self.play(GrowArrow(arrs[2]), FadeIn(d_both, scale=0.7), FadeIn(lbls[3]), run_time=0.6)
        br = Brace(VGroup(c_red, d_both), DOWN, color=GOLD, buff=1.1)
        one = lab("one completed cycle", 30, GOLD).next_to(br, DOWN, buff=0.1)
        self.at("marks one completed")
        self.play(GrowFromCenter(br), FadeIn(one), run_time=0.7)
        self.at("A green cell alone")
        ring = Circle(radius=1.3, stroke_color=YELLOW, stroke_width=5).move_to(c_grn.get_center())
        only = lab("green alone: not a completed cycle", 28, YELLOW).move_to([-1.7, -2.9, 0])
        self.play(FadeOut(br), FadeOut(one), Create(ring), FadeIn(only), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """light damages the cell (and it may look fine) -> limit light, test; one frame can mislead about fate."""

    def construct(self):
        # --- left panel: phototoxicity
        lx = -3.3
        lens = Polygon([lx - 1.2, 3.45, 0], [lx + 1.2, 3.45, 0], [lx + 0.5, 2.7, 0], [lx - 0.5, 2.7, 0], stroke_color=BLUE,
                       stroke_width=4, fill_color=BLUE, fill_opacity=0.18)
        cone = Polygon([lx - 0.5, 2.7, 0], [lx + 0.5, 2.7, 0], [lx + 2.2, -0.9, 0], [lx - 2.2, -0.9, 0], stroke_width=0,
                       fill_color=BLUE, fill_opacity=0.18)
        cell = Circle(radius=1.15, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([lx, 0.55, 0])
        nuc = Circle(radius=0.38, stroke_width=0, fill_color=GREEN, fill_opacity=0.8).move_to([lx, 0.55, 0])
        self.at("Imaging itself")
        self.play(FadeIn(lens), FadeIn(cell), FadeIn(nuc), run_time=0.6)
        self.play(FadeIn(cone), run_time=0.4)
        gl = lab("illumination damages\ncellular molecules", 26, ORANGE).move_to([lx, -1.9, 0])
        self.at("Illumination damages")
        self.play(FadeIn(gl), cone.animate.set_opacity(0.34), run_time=0.5)
        self.play(cone.animate.set_opacity(0.18), run_time=0.3)
        self.at("impair physiology")
        self.play(cell.animate.set_stroke(ORANGE, 4), run_time=0.5)
        self.at("or kill the sample")
        self.play(cell.animate.set_stroke(GREY, 4), run_time=0.3)
        looks = lab("damage is not always\nvisible in its shape", 26, TEXT).move_to([lx, -3.1, 0])
        self.at("not always visible")
        self.play(FadeIn(looks), run_time=0.4)

        # controls
        thin = Polygon([lx - 0.5, 2.7, 0], [lx + 0.5, 2.7, 0], [lx + 0.12, 0.65, 0], [lx - 0.12, 0.65, 0], stroke_width=0,
                       fill_color=BLUE, fill_opacity=0.18)
        band = Rectangle(width=2.6, height=0.12, stroke_width=0, fill_color=BLUE, fill_opacity=0.75).move_to([lx, 0.55, 0])
        c1 = chip("limit light to the focal plane", TEAL, 24).move_to([lx, -2.5, 0])
        c2 = chip("test for phototoxicity effects", TEAL, 24).move_to([lx, -3.3, 0])
        self.at("Limit illumination")
        self.play(FadeOut(cone), FadeOut(looks), FadeOut(gl), run_time=0.4)
        self.play(FadeIn(band), FadeIn(thin), FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.at("test for")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)

        # --- right panel: one frame can mislead about fate
        rx = 3.4
        divider = Line([0.1, -3.6, 0], [0.1, 3.5, 0], color=GREY, stroke_width=2)
        ex = lab("example, idealised", 22, GREY).move_to([rx, 3.45, 0])
        f1 = screen(rx - 1.5, 1.7, 2.7, 2.9)
        f2 = screen(rx + 1.5, 1.7, 2.7, 2.9)

        def mass(x, y):
            return RoundedRectangle(corner_radius=0.08, width=1.2, height=0.2, stroke_width=0, fill_color=GREEN, fill_opacity=0.8).move_to([x, y, 0])

        def nucleus(x, y):
            return Circle(radius=0.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.2).move_to([x, y, 0])
        top = mass(rx - 1.5, 2.55)
        bot = mass(rx - 1.5, 0.85)
        lag = Dot([rx - 1.5, 1.7, 0], radius=0.1, color=GREEN)
        q = lab("?", 40, YELLOW, weight=BOLD).move_to([rx - 1.5 + 0.8, 1.7, 0])
        f1l = lab("one frame", 24, GREY).move_to([rx - 1.5, 0.1, 0])
        self.at("A single frame")
        self.play(FadeIn(divider), FadeIn(ex), FadeIn(f1), FadeIn(f1l), run_time=0.5)
        self.play(FadeIn(top), FadeIn(bot), FadeIn(lag), run_time=0.5)
        laglab = chip("a lagging chromosome", YELLOW, 24).move_to([rx, -0.8, 0])
        self.at("A lagging chromosome")
        self.play(Create(Circle(radius=0.2, stroke_color=YELLOW, stroke_width=4).move_to(lag.get_center())),
                  FadeIn(laglab), FadeIn(q), run_time=0.6)
        nolab = lab("does not give the final count", 24, TEXT).move_to([rx, -1.6, 0])
        self.at("does not give")
        self.play(FadeIn(nolab), run_time=0.4)
        # later frame: it ends up inside one daughter nucleus (no numbers drawn)
        n1 = nucleus(rx + 1.5, 2.3)
        n2 = nucleus(rx + 1.5, 1.0)
        lag2 = Dot([rx + 1.5, 2.3, 0], radius=0.1, color=GREEN)
        f2l = lab("later frame", 24, TEAL).move_to([rx + 1.5, 0.1, 0])
        self.at("Follow it")
        self.play(FadeOut(q), FadeIn(f2), run_time=0.4)
        self.play(FadeIn(n1), FadeIn(n2), FadeIn(lag2), FadeIn(f2l), run_time=0.6)
        fol = chip("follow it until its fate is clear", TEAL, 26).move_to([rx, -2.6, 0])
        self.at("until its fate")
        self.play(FadeIn(fol, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Found(SpokenScene):
    """Noctor 2001: radial glia generate neurons; Rink 2005: Rab5 gives way to Rab7 on one endosome."""

    def construct(self):
        divider = Line([0.0, -3.6, 0], [0.0, 3.5, 0], color=GREY, stroke_width=2)
        # --- left: radial glia (Noctor 2001)
        gx = -3.2
        fibre = Line([gx, -0.7, 0], [gx, 3.1, 0], color=GREEN, stroke_width=7)
        body = Ellipse(width=2.0, height=1.5, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.35).move_to([gx, -1.3, 0])
        pial = Line([gx - 1.6, 3.15, 0], [gx + 1.6, 3.15, 0], color=GREY, stroke_width=3)
        t1 = lab("2001", 30, GOLD).move_to([-5.7, 3.35, 0])
        gl = lab("labelled\nradial glia", 28, GREEN).move_to([gx - 2.1, -1.3, 0])
        self.at("In 2001")
        self.play(FadeIn(divider), FadeIn(t1), FadeIn(fibre), FadeIn(body), FadeIn(pial), run_time=0.8)
        retro = chip("few cells labelled: retrovirus + fluorescent protein", GREEN, 22).move_to([-3.2, -3.1, 0])
        self.at("a few cells")
        self.play(FadeIn(gl), run_time=0.5)
        self.at("lapse images showed")
        self.play(FadeOut(gl), run_time=0.2)
        neuron = Circle(radius=0.45, stroke_color=TEXT, stroke_width=3, fill_color=GREEN, fill_opacity=0.9).move_to([gx + 0.6, -0.8, 0])
        bud = lab("neuron", 28, TEXT)
        self.play(FadeIn(neuron, scale=0.4), run_time=0.3)
        self.play(neuron.animate.move_to([gx + 0.5, 1.4, 0]), run_time=1.0)
        bud.next_to(neuron, RIGHT, buff=0.15)
        glia = lab("radial glia", 28, GREEN).move_to([gx - 2.1, -1.3, 0])
        self.at("proliferative radial glia generate")
        self.play(FadeIn(bud), FadeIn(glia), run_time=0.5)
        who = lab("who gave birth to whom?", 28, YELLOW).move_to([-3.2, -2.55, 0])
        src1 = gold_tag("Noctor et al., 2001 (schematic)", 24).move_to([-3.2, -3.2, 0])
        self.at("A fixed section")
        self.play(FadeIn(who), FadeIn(src1), run_time=0.5)

        # --- right: Rab conversion (Rink 2005)
        ex_ = 3.4
        t2 = lab("2005", 30, GOLD).move_to([0.9, 3.35, 0])
        endo = Circle(radius=1.7, stroke_color=PURPLE, stroke_width=8, fill_color=GREY, fill_opacity=0.08).move_to([ex_, 0.55, 0])
        cargo = Dot([ex_ + 0.05, 0.55, 0], radius=0.2, color=TEXT)
        cargo_l = lab("cargo", 24, TEXT).next_to(cargo, DOWN, buff=0.12)
        r5 = chip("Rab5", PURPLE, 28).move_to([ex_ - 1.2, 2.75, 0])
        r7 = chip("Rab7", PINK, 28).move_to([ex_ + 1.2, 2.75, 0])
        self.at("In 2005")
        self.play(FadeIn(t2), FadeIn(endo), FadeIn(cargo), FadeIn(cargo_l), FadeIn(r5), run_time=0.8)
        self.at("filmed single endosomes")
        self.play(Indicate(endo, color=TEXT, scale_factor=1.05), run_time=0.7)
        self.at("was replaced by")
        self.play(endo.animate.set_stroke(PINK, 8), r5.animate.set_opacity(0.3), FadeIn(r7), run_time=1.6)
        same = lab("cargo stays in the same endosome", 26, TEXT).move_to([ex_, -1.6, 0])
        self.at("while the cargo stayed")
        self.play(FadeIn(same), Indicate(cargo, color=TEXT, scale_factor=1.6), run_time=0.8)
        mat = chip("supports maturation", TEAL, 28).move_to([ex_, -2.35, 0])
        src2 = gold_tag("Rink et al., 2005", 24).move_to([ex_, -2.95, 0])
        a431 = lab("A431 cells, LDL cargo", 22, GREY).move_to([ex_, -3.4, 0])
        self.at("That supports maturation")
        self.play(FadeIn(mat, shift=UP * 0.1), FadeIn(src2), FadeIn(a431), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Rule(SpokenScene):
    """Hines 2015: most wrapping attempts vanish within 90 min; the rule to keep."""

    def construct(self):
        t = lab("2015", 30, GOLD).move_to([-5.9, 3.3, 0])
        axon = RoundedRectangle(corner_radius=0.15, width=11.6, height=0.5, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.25).move_to([0, 0.9, 0])
        axl = lab("Schematic: 6 of 8 attempts gone by 90 min = about 75%", 24, GREY).move_to([-2.0, 2.35, 0])
        wx = [-4.5, -3.2, -1.9, -0.6, 0.7, 2.0, 3.3, 4.6]
        wraps = VGroup(*[RoundedRectangle(corner_radius=0.15, width=0.8, height=1.8, stroke_color=PINK, stroke_width=4,
                                          fill_color=PINK, fill_opacity=0.22).move_to([x, 0.9, 0]) for x in wx])
        tline = Line([-5.8, -0.9, 0], [5.8, -0.9, 0], color=GREY, stroke_width=3)
        t0 = M("0", 24, GREY).move_to([-5.8, -1.4, 0])
        t90 = M("90 min", 24, YELLOW).move_to([4.6, -1.4, 0])
        m90 = Line([4.6, -0.7, 0], [4.6, -1.1, 0], color=YELLOW, stroke_width=4)
        m0 = Line([-5.8, -0.7, 0], [-5.8, -1.1, 0], color=GREY, stroke_width=4)
        self.at("In 2015")
        self.play(FadeIn(t), FadeIn(axon), FadeIn(axl), FadeIn(tline), FadeIn(m0), FadeIn(t0), run_time=0.8)
        self.at("colleagues filmed")
        self.play(LaggedStart(*[FadeIn(w, scale=0.6) for w in wraps], lag_ratio=0.12), run_time=1.2)
        gone = [wraps[i] for i in (0, 1, 3, 4, 6, 7)]
        keep = [wraps[i] for i in (2, 5)]
        self.at("About 75")
        self.play(FadeIn(m90), FadeIn(t90), run_time=0.4)
        self.play(*[FadeOut(w) for w in gone], run_time=1.2)
        pc = lab("about 75% of wrapping attempts gone within 90 min", 28, YELLOW).move_to([0, -2.3, 0])
        self.play(FadeIn(pc), run_time=0.5)
        sil = lab("wraps already formed on silenced axons retracted more often", 28, TEXT).move_to([0, -3.1, 0])
        self.at("retracted more often")
        self.play(FadeIn(sil), run_time=0.5)
        src = gold_tag("Hines et al., 2015", 24).move_to([4.4, 3.3, 0])
        self.play(FadeIn(src), run_time=0.3)
        self.at("Retraction is only seen")
        self.play(Indicate(pc, color=YELLOW, scale_factor=1.04), run_time=0.7)

        # the rule
        self.at("Keep one rule")
        self.play(FadeOut(VGroup(t, axon, axl, tline, m0, t0, m90, t90, pc, sil, src, *keep)), run_time=0.5)
        r1 = T("A movie shows what those cells did,", 46, TEXT, font=TITLE_FONT).move_to([0, 0.7, 0])
        r2 = T("not what all cells do.", 46, GOLD, font=TITLE_FONT).move_to([0, -0.5, 0])
        self.at("A movie shows what")
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.8)
        self.at("not what all cells")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A movie shows what those cells did, not what all cells do."
