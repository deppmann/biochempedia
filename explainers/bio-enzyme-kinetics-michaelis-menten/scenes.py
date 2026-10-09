"""Leonor Michaelis & Maud Menten: scientist profile  (Biochemistrypedia, enzyme-kinetics lesson)

The portrait (Chris's AI-generated engraving-style illustration from The Molecule Hunters) is the anchor:
it opens the video, then stays as a framed inset on the left while the right side animates the story as
the voice reaches each beat. Every cue is timed to the real narration (self.at -> audio/words.json).
Nothing on screen adds a fact beyond the lesson's scientists[] entry (name, dates, contribution, story, quotes).

COLOR MAP (one color per concept, whole video)
  BLUE   = Leonor Michaelis (his name, his work, his title)
  GREEN  = Maud Menten (her name, her credentials, her move, her life)
  YELLOW = light / the optical signal (polarimeter beam, dial needle, the measured progress curve)
  PURPLE = sugar (the thing being broken apart)
  RED    = whatever masks the true rate (too-late looks, byproducts, optical drift) and what was denied
  GOLD   = initial velocity, the 1913 equation (and the portrait frame)
  TEAL   = the buffered pH
  ORANGE = stains
  (Menten's hat is GREEN: her life)
  GREY   = axes, structure, de-emphasized
No molecular structure is drawn anywhere (schematic dial, tube, chips, plots from real equations only).
"""
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#E8913A"
HERE = Path(__file__).resolve().parent

IMG_AR = 1408 / 770.0
PW = 5.0                           # inset portrait width
PH = PW / IMG_AR
PC = np.array([-3.8, 1.25, 0.0])   # inset portrait center
BIG_C = np.array([0.0, 0.7, 0.0])  # title-card portrait center
BIG_W = 6.4


class Plate:
    """The portrait inset: image, gold frame, dimmers for focus, names + dates, AI-disclosure caption."""

    def __init__(self, width=PW, center=PC, focus="both"):
        h = width / IMG_AR
        self.img = ImageMobject(str(HERE / "portrait.png")).set_width(width).move_to(center)
        self.img.set_z_index(0)
        self.border = Rectangle(width=width, height=h, stroke_color=GOLD, stroke_width=2.5,
                                fill_opacity=0).move_to(center).set_z_index(3)
        self.dimL = Rectangle(width=width / 2, height=h, stroke_width=0, fill_color=BG,
                              fill_opacity=0.62 if focus == "right" else 0).move_to(center + LEFT * width / 4).set_z_index(2)
        self.dimR = Rectangle(width=width / 2, height=h, stroke_width=0, fill_color=BG,
                              fill_opacity=0.62 if focus == "left" else 0).move_to(center + RIGHT * width / 4).set_z_index(2)
        self.nameL = VGroup(T("Leonor Michaelis", 22, BLUE, weight=BOLD), M("1875–1949", 22, GREY)).arrange(DOWN, buff=0.1)
        self.nameR = VGroup(T("Maud Menten", 22, GREEN, weight=BOLD), M("1879–1960", 22, GREY)).arrange(DOWN, buff=0.1)
        y = center[1] - h / 2 - 0.6
        self.nameL.move_to([center[0] - width / 4, y, 0])
        self.nameR.move_to([center[0] + width / 4, y, 0])
        self.nameL.set_opacity(0.4 if focus == "right" else 1)
        self.nameR.set_opacity(0.4 if focus == "left" else 1)
        self.caption = T("illustration · AI-generated", 22, GREY).move_to([center[0], y - 0.85, 0])

    def parts(self):
        return [self.img, self.border, self.dimL, self.dimR, self.nameL, self.nameR, self.caption]

    def add_to(self, scene):
        scene.add(*self.parts())

    def focus(self, which):
        """Animations that shift the highlight: 'left' (Michaelis), 'right' (Menten) or 'both'."""
        return [self.dimL.animate.set_fill(BG, opacity=0.62 if which == "right" else 0),
                self.dimR.animate.set_fill(BG, opacity=0.62 if which == "left" else 0),
                self.nameL.animate.set_opacity(0.4 if which == "right" else 1),
                self.nameR.animate.set_opacity(0.4 if which == "left" else 1)]


def left_at(mob, x):
    mob.shift(RIGHT * (x - mob.get_left()[0]))
    return mob


def dial(center, r, a):
    """A schematic polarimeter dial: ring + needle whose angle follows ValueTracker a (radians)."""
    ring = Circle(radius=r, stroke_color=GREY, stroke_width=3).move_to(center)
    hub = Dot(center, radius=0.06, color=YELLOW)

    def needle():
        d = np.array([np.cos(a.get_value()), np.sin(a.get_value()), 0.0])
        return Line(center - 0.85 * r * d, center + 0.85 * r * d, color=YELLOW, stroke_width=6)

    return VGroup(ring, hub), always_redraw(needle)


def strike(mob, color=RED):
    return Line(mob.get_corner(DL) + UR * 0.05, mob.get_corner(UR) + DL * 0.05, color=color, stroke_width=6)


# ---- the progress-curve plot shared by scenes 2 and 3 --------------------------------------------
AX_O = (-0.1, -2.7)
KP = 0.45   # rate constant of the schematic progress curve: P(t) = 1 - exp(-KP t)


def prog(t):
    return 1 - np.exp(-KP * t)


def make_axes(x_max, y_max, w, h, origin, tick=2):
    ax = Axes(x_range=[0, x_max, tick], y_range=[0, y_max, 0.2], x_length=w, y_length=h,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY,
                           "stroke_width": 3, "tip_width": 0.16, "tip_height": 0.16}, tips=True)
    ax.shift(np.array([origin[0], origin[1], 0]) - ax.c2p(0, 0))
    return ax


def axis_labels(ax, xtext, ytext, size=26, x_dy=0.5, y_dx=0.55):
    o = ax.c2p(0, 0)
    xl = T(xtext, size).move_to([o[0] + ax.x_length / 2, o[1] - x_dy, 0])
    yl = T(ytext, size).rotate(PI / 2).move_to([o[0] - y_dx, o[1] + ax.y_length / 2, 0])
    return xl, yl


def prog_plot():
    ax = make_axes(10, 1.4, 6.0, 3.9, AX_O)
    xl, yl = axis_labels(ax, "time", "product formed")
    curve = ax.plot(prog, x_range=[0, 10], color=YELLOW, stroke_width=6)
    return ax, xl, yl, curve


def late_overlay(ax):
    """Too-late marker + the tangle of byproducts (RED)."""
    p8 = ax.c2p(8, prog(8))
    arrow = Arrow(p8 + UP * 1.05, p8 + UP * 0.12, buff=0, color=RED, stroke_width=6, max_tip_length_to_length_ratio=0.35)
    lab1 = T("looked here: too late", 26, RED).next_to(arrow, UP, buff=0.12)
    lab1.set_x(min(lab1.get_x(), 6.3 - lab1.width / 2))

    # byproducts: small red specks piling up in the late part of the run, under the flattened curve
    rng = np.random.default_rng(7)
    pts = [(rng.uniform(6.6, 9.7), rng.uniform(0.12, 0.72)) for _ in range(14)]
    scr = VGroup(*[Dot(ax.c2p(t, y), radius=0.075, color=RED).set_opacity(0.9) for t, y in pts])
    lab2 = T("byproducts", 26, RED).move_to(ax.c2p(4.2, 0.42))
    return arrow, lab1, scr, lab2


class Bio(SpokenScene):
    def put_plate(self, focus="both"):
        self.plate = Plate(focus=focus)
        self.plate.add_to(self)
        return self.plate


# =====================================================================================================
class S00Title(NarratedScene):
    """Portrait first: slow push-in, then the name and dates."""

    def construct(self):
        img = ImageMobject(str(HERE / "portrait.png")).set_width(BIG_W).move_to(BIG_C)
        frame = Rectangle(width=BIG_W, height=BIG_W / IMG_AR, stroke_color=GOLD, stroke_width=2.5).move_to(BIG_C)
        pic = Group(img, frame)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9).move_to([0, 3.5, 0])
        lesson = T("SCIENTIST PROFILE", size=22, color=GREY).move_to([0, 3.05, 0])
        cap = T("illustration · AI-generated", 22, GREY).move_to([0, BIG_C[1] - BIG_W / IMG_AR / 2 - 0.4, 0])
        title = T("Leonor Michaelis & Maud Menten", size=44, font=TITLE_FONT)
        title.move_to([0, -2.2, 0])
        dates = M("1875–1949  ·  1879–1960", 26, GREY).move_to([0, -2.8, 0])
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4).move_to([0, -3.2, 0])
        # slow push-in for the whole card
        pic.add_updater(lambda m, dt: m.scale(1 + 0.03 * dt, about_point=BIG_C))
        self.add(pic)
        self.play(FadeIn(pic), run_time=self.beat(0.18))
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.15))
        self.play(FadeIn(cap), Write(title), run_time=self.beat(0.3))
        self.play(FadeIn(dates, shift=UP * 0.1), GrowFromCenter(rule), run_time=self.beat(0.15))
        self.wait(self.beat(0.1))
        self.play(*[FadeOut(m) for m in (brand, lesson, cap, title, dates, rule)], run_time=self.beat(0.12))
        self.finish()


# =====================================================================================================
class S01Michaelis(Bio):
    def construct(self):
        # --- carry the title-card portrait into the inset
        s0 = np.exp(0.03 * 3.4)
        w0 = BIG_W * s0
        pl = Plate()
        img, border = pl.img, pl.border
        img.set_width(w0).move_to(BIG_C)
        border.become(Rectangle(width=w0, height=w0 / IMG_AR, stroke_color=GOLD, stroke_width=2.5).move_to(BIG_C))
        self.add(img, border)
        a = ValueTracker(0)

        def follow(m):
            s = smooth(a.get_value())
            w = w0 + (PW - w0) * s
            c = BIG_C + (PC - BIG_C) * s
            m.set_width(w).move_to(c)

        img.add_updater(follow)
        border.add_updater(follow)
        self.play(a.animate.set_value(1), run_time=0.7, rate_func=linear)
        img.clear_updaters()
        border.clear_updaters()
        pl.dimL.set_fill(BG, opacity=0)
        pl.dimR.set_fill(BG, opacity=0)
        pl.nameR.set_opacity(0.4)
        pl.dimR.set_fill(BG, opacity=0.62)
        self.add(pl.dimL, pl.dimR)
        self.play(FadeIn(pl.nameL), FadeIn(pl.nameR), FadeIn(pl.caption), run_time=0.3)

        # --- by day / by night
        self.at("ran routine tests")
        day = VGroup(T("BY DAY", 26, GREY, weight=BOLD), chip("routine tests\nBerlin city hospital", BLUE, 26)).arrange(RIGHT, buff=0.4)
        left_at(day, -0.5).set_y(1.6)
        self.play(FadeIn(day, shift=RIGHT * 0.3), run_time=0.5)
        self.at("by night")
        night = VGroup(T("BY NIGHT", 26, GREY, weight=BOLD),
                       chip("“a laboratory of the\nmost primitive kind”", BLUE, 26)).arrange(RIGHT, buff=0.4)
        left_at(night, -0.5).set_y(-0.6)
        self.play(FadeIn(night, shift=RIGHT * 0.3), run_time=0.5)

        # --- polarimeter schematic: light twists as sugar breaks apart
        self.at("measured how light twists", lead=0.9)
        self.play(FadeOut(day), FadeOut(night), run_time=0.5)
        beam_y = 0.5
        beam_in = Arrow([-0.4, beam_y, 0], [1.05, beam_y, 0], buff=0, color=YELLOW, stroke_width=6)
        beam_lab = T("light", 26, YELLOW).next_to(beam_in, UP, buff=0.15)
        tube = RoundedRectangle(corner_radius=0.2, width=2.6, height=1.1, stroke_color=GREY, stroke_width=3).move_to([2.4, beam_y, 0])
        sugar = VGroup(*[Square(0.26, stroke_width=0, fill_color=PURPLE, fill_opacity=0.85).move_to([1.7 + 0.5 * i, beam_y, 0])
                         for i in range(4)])
        sugar_lab = T("sugar", 26, PURPLE).next_to(tube, DOWN, buff=0.2)
        beam_out = Arrow([3.7, beam_y, 0], [4.3, beam_y, 0], buff=0, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.5)
        ang = ValueTracker(np.radians(80))
        ring, needle = dial(np.array([5.1, beam_y, 0]), 0.75, ang)
        twist_lab = T("light twists", 26, YELLOW).move_to([5.1, beam_y + 1.25, 0])
        self.play(GrowArrow(beam_in), FadeIn(beam_lab), Create(tube), FadeIn(sugar), FadeIn(sugar_lab), run_time=0.9)
        self.play(GrowArrow(beam_out), Create(ring), FadeIn(needle), run_time=0.6)
        self.at("twists")
        self.play(FadeIn(twist_lab), ang.animate.set_value(np.radians(55)), run_time=0.6, rate_func=smooth)
        self.at("as sugar breaks apart", lead=0.1)
        pairs = []
        anims = []
        for sq in sugar:
            pair = VGroup(*[Square(0.13, stroke_width=0, fill_color=PURPLE, fill_opacity=0.85).move_to(sq.get_center() + RIGHT * dx)
                            for dx in (-0.12, 0.12)])
            pairs.append(pair)
            anims.append(ReplacementTransform(sq, pair))
        self.play(LaggedStart(*anims, lag_ratio=0.25), ang.animate.set_value(np.radians(15)), run_time=2.0, rate_func=linear)

        # --- professor, but not salary / chair / funding
        self.at("held the title of professor", lead=0.9)
        self.play(*[FadeOut(m) for m in (beam_in, beam_lab, tube, sugar_lab, beam_out, ring, needle, twist_lab, *pairs)], run_time=0.5)
        prof = chip("title of professor", BLUE, 30).move_to([2.9, 1.5, 0])
        self.at("professor", lead=0.2)
        self.play(FadeIn(prof, shift=DOWN * 0.2), run_time=0.5)
        self.at("but not")
        butnot = T("but not", 26, GREY).move_to([2.9, 0.3, 0])
        self.play(FadeIn(butnot), run_time=0.3)
        chips, strikes = [], []
        for word, x, cue in (("salary", 0.5, "salary"), ("chair", 2.9, "chair"), ("funding", 5.3, "funding")):
            self.at(cue, lead=0.25)
            c = chip(word, GREY, 30).move_to([x, -1.0, 0])
            self.play(FadeIn(c, shift=UP * 0.15), run_time=0.3)
            st = strike(c)
            self.play(Create(st), run_time=0.3)
            chips.append(c)
            strikes.append(st)

        # --- precision as shelter
        self.at("precision became", lead=0.3)
        self.play(*[FadeOut(m) for m in [prof, butnot, *chips, *strikes]], run_time=0.35)
        prec = chip("precision", BLUE, 36).move_to([2.9, 0.0, 0])
        self.play(FadeIn(prec, scale=0.8), run_time=0.4)
        self.at("shelter", lead=0.9)
        walls = Rectangle(width=3.6, height=1.7, stroke_color=GREY, stroke_width=4).move_to([2.9, 0.0, 0])
        roof = Polygon([0.9, 0.85, 0], [2.9, 2.15, 0], [4.9, 0.85, 0], stroke_color=GREY, stroke_width=4)
        self.play(Create(walls), Create(roof), run_time=0.9)
        sh = T("a kind of shelter", 30, GREY).move_to([2.9, -1.55, 0])
        self.play(FadeIn(sh, shift=UP * 0.1), run_time=0.4)
        self.finish()

    def clear_stage_leftovers(self, pl):
        """Remove anything on the stage (x > -0.7) that is not part of the portrait column."""
        keep = {id(m) for m in pl.parts()}
        for m in list(self.mobjects):
            if id(m) in keep:
                continue
            try:
                if m.get_center()[0] > -0.7:
                    self.remove(m)
            except Exception:
                pass


# =====================================================================================================
class S02Menten(Bio):
    def construct(self):
        pl = self.put_plate("left")
        self.play(*pl.focus("right"), run_time=0.6)
        # credentials
        self.at("Canadian")
        c1 = chip("Canadian", GREEN, 30).move_to([2.9, 2.75, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.2), run_time=0.4)
        self.at("already earned")
        a1 = Arrow([2.9, 2.38, 0], [2.9, 1.95, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.5)
        c2 = chip("M.D. · already earned", GREEN, 30).move_to([2.9, 1.55, 0])
        self.play(GrowArrow(a1), FadeIn(c2, shift=DOWN * 0.2), run_time=0.5)
        self.at("would earn")
        a2 = Arrow([2.9, 1.18, 0], [2.9, 0.75, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.5)
        c3 = chip("Ph.D. · would earn", GREEN, 30).move_to([2.9, 0.35, 0])
        self.play(GrowArrow(a2), FadeIn(c3, shift=DOWN * 0.2), run_time=0.5)
        self.at("most universities")
        bar = Rectangle(width=0.1, height=1.0, stroke_width=0, fill_color=RED, fill_opacity=1).move_to([-0.2, -1.4, 0])
        red1 = T("most universities still refused\nwomen advanced degrees", 28, RED, line_spacing=0.8)
        left_at(red1, 0.05).set_y(-1.4)
        self.play(FadeIn(bar), FadeIn(red1, shift=RIGHT * 0.2), run_time=0.6)
        self.play(Indicate(c3, color=GREEN, scale_factor=1.06), run_time=0.8)

        # he saw why earlier experiments failed
        self.at("he saw why", lead=0.7)
        self.play(*[FadeOut(m) for m in (c1, a1, c2, a2, c3, bar, red1)], *pl.focus("both"), run_time=0.6)
        ax, xl, yl, curve = prog_plot()
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.7)
        self.at("experiments")
        self.play(Create(curve), run_time=1.3, rate_func=linear)
        self.at("They looked too late")
        arrow, lab1, scr, lab2 = late_overlay(ax)
        self.play(GrowArrow(arrow), FadeIn(lab1), run_time=0.6)
        self.at("after byproducts")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in scr], lag_ratio=0.12), FadeIn(lab2), run_time=1.3)
        self.play(*[d.animate.shift(0.12 * np.array([np.cos(2.1 * k), np.sin(3.3 * k), 0])) for k, d in enumerate(scr)],
                  run_time=0.8, rate_func=there_and_back)
        self.finish()


# =====================================================================================================
class S03InitialVelocity(Bio):
    def construct(self):
        pl = self.put_plate("both")
        ax, xl, yl, curve = prog_plot()
        arrow, lab1, scr, lab2 = late_overlay(ax)
        self.add(ax, xl, yl, curve, arrow, lab1, scr, lab2)
        self.play(*[FadeOut(m) for m in (arrow, lab1, scr, lab2)], run_time=0.5)
        # the beginning
        self.at("at the beginning")
        band = Rectangle(width=ax.c2p(1.2, 0)[0] - ax.c2p(0, 0)[0], height=ax.y_length, stroke_width=0,
                         fill_color=GOLD, fill_opacity=0.14)
        band.move_to([(ax.c2p(1.2, 0)[0] + ax.c2p(0, 0)[0]) / 2, ax.c2p(0, 0)[1] + ax.y_length / 2, 0])
        beg = T("the beginning", 26, GOLD).move_to([ax.c2p(0, 0)[0] + 0.7, ax.c2p(0, 1.4)[1] + 0.35, 0])
        self.play(FadeIn(band), FadeIn(beg), run_time=0.5)
        # buffered pH
        self.at("buffering")
        ph = chip("buffered pH", TEAL, 28).move_to([0.9, 2.85, 0])
        self.play(FadeIn(ph, shift=DOWN * 0.2), run_time=0.5)
        # initial velocity = slope at the start
        self.at("initial velocity")
        p0, p1 = ax.c2p(0, 0), ax.c2p(2.4, KP * 2.4)
        tang = Line(p0, p1, color=GOLD, stroke_width=7)
        iv = T("initial velocity", 28, GOLD).next_to(p1, RIGHT, buff=0.2).shift(UP * 0.15)
        self.play(Create(tang), FadeIn(iv), run_time=0.9)
        # Menten's move: freeze at precise instants
        self.at("Menton's move", lead=0.4)
        self.play(*pl.focus("right"), run_time=0.5)
        self.at("freeze")
        times = [0.35, 0.8, 1.3, 1.9]
        marks = VGroup()
        for t in times:
            pt = ax.c2p(t, prog(t))
            ln = DashedLine(ax.c2p(t, 0), pt, color=GREEN, stroke_width=3, dash_length=0.1)
            marks.add(VGroup(ln, Dot(pt, radius=0.09, color=GREEN)))
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.3), run_time=1.3)
        self.at("precise")
        frz = T("reaction frozen at\nprecise instants", 26, GREEN, line_spacing=0.8).move_to(ax.c2p(6.6, 0.42))
        self.play(FadeIn(frz), run_time=0.3)
        # optical drift stops
        dd = np.array([5.7, 2.65, 0])
        a2 = ValueTracker(np.radians(80))
        ring, needle = dial(dd, 0.45, a2)
        drift_lab = T("optical drift", 26, RED).move_to([3.75, 2.65, 0])
        self.at("instance", lead=0.25)
        self.play(Create(ring), FadeIn(needle), FadeIn(drift_lab), run_time=0.4)
        self.play(a2.animate.set_value(np.radians(50)), run_time=0.8, rate_func=linear)
        self.at("stopping", lead=0.15)
        stopped = T("stopped", 24, GREEN).next_to(ring, DOWN, buff=0.1)
        self.play(FadeIn(stopped), run_time=0.3)
        self.at("masked the true rate", lead=0.6)
        self.play(Indicate(tang, color=GOLD, scale_factor=1.0), Transform(iv, T("the true rate", 28, GOLD).move_to(iv)), run_time=1.0)
        self.finish()


# =====================================================================================================
class S04Equation(Bio):
    def construct(self):
        pl = self.put_plate("both")
        self.at("1913")
        yr = T("1913", 50, GOLD, font=TITLE_FONT)
        left_at(yr, -0.3).set_y(3.05)
        self.play(Write(yr), run_time=0.5)
        self.at("equation")
        eq = M("v = Vmax[S] / (Km + [S])", 32, GOLD)
        left_at(eq, -0.3).set_y(2.05)
        ax = make_axes(10, 1.2, 6.0, 3.6, (0.0, -2.8))
        xl = T("[S]", 28).move_to([ax.c2p(5, 0)[0], ax.c2p(0, 0)[1] - 0.45, 0])
        yl = T("v", 28).move_to(ax.c2p(0, 1.2) + LEFT * 0.4 + DOWN * 0.1)
        curve = ax.plot(lambda s: s / (2 + s), x_range=[0, 10], color=GOLD, stroke_width=6)
        self.play(FadeIn(eq, shift=RIGHT * 0.2), Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.7)
        self.play(Create(curve), run_time=1.3)
        self.at("descriptive science", lead=0.4)
        d = chip("descriptive\nscience", GREY, 28)
        q = chip("quantitative\nscience", GOLD, 28)
        row = VGroup(d, Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.5), q).arrange(RIGHT, buff=0.25)
        left_at(row, -0.3).set_y(1.9)
        arrow_mid = row[1]
        self.play(FadeOut(eq), FadeIn(d, shift=RIGHT * 0.2), run_time=0.5)
        self.at("quantitative", lead=0.3)
        self.play(GrowArrow(arrow_mid), FadeIn(q, shift=RIGHT * 0.2), run_time=0.5)
        self.play(Indicate(curve, color=GOLD, scale_factor=1.0), run_time=0.5)
        # a single year
        self.at("and they worked", lead=0.7)
        self.play(*[FadeOut(m) for m in (yr, row, ax, xl, yl, curve)], run_time=0.45)
        y0 = 0.5
        mb = VGroup(T("Michaelis", 26, BLUE), Dot(radius=0.3, color=BLUE)).arrange(DOWN, buff=0.2).move_to([0.4, y0, 0])
        mt = VGroup(T("Menten", 26, GREEN), Dot(radius=0.3, color=GREEN)).arrange(DOWN, buff=0.2).move_to([5.4, y0, 0])
        self.play(FadeIn(mb), FadeIn(mt), run_time=0.3)
        self.at("worked together", lead=0.1)
        self.play(mb.animate.move_to([1.7, y0, 0]), mt.animate.move_to([4.1, y0, 0]), run_time=0.5)
        link = Line(mb[1].get_center(), mt[1].get_center(), color=GOLD, stroke_width=6).set_z_index(-1)
        self.play(Create(link), run_time=0.3)
        self.at("single year", lead=0.3)
        br = Brace(link, DOWN, color=GOLD, buff=0.3)
        yl2 = T("a single year", 34, GOLD).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(yl2), run_time=0.6)
        self.finish()


# =====================================================================================================
def icon_slide():
    slide = Rectangle(width=1.1, height=0.7, stroke_color=GREY, stroke_width=3)
    s1 = Ellipse(width=0.55, height=0.32, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8).shift(LEFT * 0.12 + UP * 0.03)
    s2 = Ellipse(width=0.3, height=0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=0.5).shift(RIGHT * 0.25 + DOWN * 0.1)
    return VGroup(slide, s1, s2)


def icon_mountains():
    m1 = Polygon([-0.6, -0.4, 0], [-0.15, 0.4, 0], [0.25, -0.4, 0], stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.25)
    m2 = Polygon([0.0, -0.4, 0], [0.35, 0.1, 0], [0.65, -0.4, 0], stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.25)
    return VGroup(m1, m2)


def icon_car():
    body = RoundedRectangle(corner_radius=0.06, width=1.0, height=0.28, stroke_color=GREEN, stroke_width=3).shift(DOWN * 0.1)
    cab = RoundedRectangle(corner_radius=0.05, width=0.45, height=0.3, stroke_color=GREEN, stroke_width=3).shift(LEFT * 0.12 + UP * 0.14)
    w1 = Circle(0.12, stroke_color=GREEN, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([-0.3, -0.26, 0])
    w2 = Circle(0.12, stroke_color=GREEN, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([0.3, -0.26, 0])
    return VGroup(body, cab, w1, w2)


def icon_hat():
    brim = Ellipse(width=0.62, height=0.1, stroke_width=0, fill_color=GREEN, fill_opacity=0.95)
    crown = RoundedRectangle(corner_radius=0.1, width=0.3, height=0.2, stroke_width=0, fill_color=GREEN, fill_opacity=0.95).next_to(brim, UP, buff=-0.04)
    return VGroup(crown, brim)


class S05MentenAfter(Bio):
    def construct(self):
        pl = self.put_plate("both")
        self.play(*pl.focus("right"), run_time=0.5)
        ys = [2.5, 0.9, -0.7, -2.3]
        icx, tx = 0.15, 1.15

        def label(txt, y):
            t = T(txt, 26, TEXT, line_spacing=0.8)
            left_at(t, tx).set_y(y)
            return t

        # row 1: azo-dye stains
        self.at("develop")
        i1 = icon_slide().move_to([icx, ys[0], 0])
        l1 = label("azo-dye stains still used\nin pathology today", ys[0])
        self.play(FadeIn(i1, scale=0.8), FadeIn(l1, shift=RIGHT * 0.2), run_time=0.6)
        # row 2: wilderness
        self.at("climbed")
        i2 = icon_mountains().move_to([icx, ys[1], 0])
        l2 = label("climbed in the\nCanadian wilderness", ys[1])
        self.play(Create(i2), FadeIn(l2, shift=RIGHT * 0.2), run_time=0.7)
        # row 3: Model T and hats
        self.at("drove")
        car = icon_car().move_to([icx - 1.4, ys[2], 0])
        l3 = label("drove a Model T through\nPittsburgh in Paris hats", ys[2])
        self.play(FadeIn(l3, shift=RIGHT * 0.2), car.animate.move_to([icx, ys[2], 0]), run_time=1.0, rate_func=smooth)
        self.at("Paris hats", lead=0.0)
        hat = icon_hat().move_to(car[1].get_top() + UP * 0.12 + LEFT * 0.0)
        self.play(FadeIn(hat, shift=DOWN * 0.25), run_time=0.5)
        # row 4: passed over
        self.at("passed over", lead=0.3)
        l4 = label("passed over for advancement,\nher whole career", ys[3])
        steps = VGroup(*[Rectangle(width=0.3, height=0.18 + 0.2 * i, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15)
                         for i in range(4)]).arrange(RIGHT, buff=0, aligned_edge=DOWN)
        steps.move_to([icx, ys[3] - 0.15, 0])
        tops = [s.get_top() + UP * 0.14 for s in steps]
        me = Dot(tops[0], radius=0.12, color=GREEN)
        others = [Dot(tops[0], radius=0.11, color=GREY) for _ in range(3)]
        self.play(Create(steps), FadeIn(l4, shift=RIGHT * 0.2), FadeIn(me), *[FadeIn(o) for o in others], run_time=0.7)
        self.play(*[o.animate.move_to(tops[k + 1]) for k, o in enumerate(others)], run_time=1.1)
        self.finish()


# =====================================================================================================
class S06Quote(Bio):
    def construct(self):
        pl = self.put_plate("both")
        lines = ["“If this assumption is correct, the rate",
                 "of inversion must be proportional to the",
                 "prevailing concentration of the",
                 "sucrose-enzyme complex.”"]
        txts = [T(s, 30, TEXT, font=TITLE_FONT) for s in lines]
        block = VGroup(*txts).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        left_at(block, -0.3).set_y(0.45)
        fit(block, max_w=6.7, max_h=4.0)
        left_at(block, -0.3)
        attr = T("— Leonor Michaelis & Maud Menten", 26, GREY)
        left_at(attr, -0.3).set_y(block.get_bottom()[1] - 0.6)
        bar = Rectangle(width=0.07, height=block.height, stroke_width=0, fill_color=GOLD, fill_opacity=1)
        bar.next_to(block, LEFT, buff=0.2)
        self.wait(0.4)
        self.play(FadeIn(bar), run_time=0.4)
        for t in txts:
            self.play(FadeIn(t, shift=RIGHT * 0.15), run_time=0.7)
        self.wait(0.3)
        self.play(FadeIn(attr), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Buffered pH + initial velocity: a reproducible v = Vmax[S]/(Km + [S])"
