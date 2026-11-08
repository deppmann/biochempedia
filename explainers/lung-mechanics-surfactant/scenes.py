"""Lung mechanics and surfactant: why small alveoli need surfactant  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = air / gas in the airspace (the air-filled lung, the alveolus)
  PURPLE = liquid fill (the liquid-filled lung)
  YELLOW = surface tension T and the air-liquid surface
  ORANGE = pressure P needed to hold an alveolus open
  GREEN  = surfactant (the lining, the lung-extract film) and its result
  RED    = the problem: gas moving from the small alveolus into the large one
  GREY   = outlines, structure, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
LIQ = "#B58CD9"   # liquid fill (purple)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def alveolus(radius, center, rim=YELLOW, fill=BLUE, rim_w=7):
    return Circle(radius=radius, stroke_color=rim, stroke_width=rim_w, fill_color=fill, fill_opacity=0.22).move_to(center)


def frame_axes(x0, x1, y0, y1, xlabel, ylabel, xsize=24, ysize=24):
    """Plain L-shaped axes (no LaTeX). Returns a group with .x and .y label attributes."""
    ax = Arrow([x0, y0, 0], [x1, y0, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    ay = Arrow([x0, y0, 0], [x0, y1, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
    xl = T(xlabel, xsize, GREY).next_to(ax, DOWN, buff=0.15)
    yl = T(ylabel, ysize, GREY).rotate(PI / 2).next_to(ay, LEFT, buff=0.15)
    g = VGroup(ax, ay, xl, yl)
    return g


def curve_through(pts, color, w=6):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_smoothly([np.array([x, y, 0.0]) for x, y in pts])
    return m


def sig(p, c, k):
    return 1 / (1 + np.exp(-(p - c) / k))


def norm_sig(p, c, k):
    return (sig(p, c, k) - sig(0, c, k)) / (sig(10, c, k) - sig(0, c, k))


class S00Title(TitleCard):
    LESSON = "Lung mechanics and surfactant"
    TITLE = "Why small alveoli need surfactant"


# ---------------------------------------------------------------------------------------------
class S01Air(SpokenScene):
    """air-filled vs liquid-filled lung: liquid removes the air-liquid surface; the pressure curve moves left."""

    def construct(self):
        # --- plot (sketch) ---
        X0, X1, Y0, Y1 = 0.9, 6.2, -2.6, 2.4
        axes = frame_axes(X0, X1, Y0, Y1, "Distending pressure", "Volume")
        note = T("relative units, in this sketch", 22, GREY).move_to([3.5, 2.85, 0])

        def X(p): return X0 + 5.3 * p / 10

        def Y(v): return Y0 + 4.6 * v

        ps = np.linspace(0, 10, 40)
        air = curve_through([(X(p), Y(norm_sig(p, 6.0, 1.3))) for p in ps], BLUE)
        liq = curve_through([(X(p), Y(norm_sig(p, 2.8, 1.0))) for p in ps], LIQ)
        air_l = T("air-filled", 24, BLUE).move_to([5.45, 0.55, 0])
        liq_l = T("liquid-filled", 24, LIQ).move_to([1.95, 1.55, 0])

        # --- lung block with four idealised alveoli ---
        cx, cy = -3.9, -0.1
        block = RoundedRectangle(corner_radius=0.25, width=3.4, height=3.0, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.12).move_to([cx, cy, 0])
        offs = [(-0.78, 0.65), (0.78, 0.65), (-0.78, -0.65), (0.78, -0.65)]
        bubs = VGroup(*[alveolus(0.52, [cx + dx, cy + dy, 0], rim=YELLOW, fill=BLUE, rim_w=6) for dx, dy in offs])
        blk_l = T("excised lung", 24, GREY).next_to(block, DOWN, buff=0.2)
        state = T("air-filled", 28, BLUE, weight=BOLD).next_to(blk_l, DOWN, buff=0.12)
        surf_l = T("air-liquid surface", 24, YELLOW).move_to([cx, 2.15, 0])
        surf_a = arr([cx - 0.6, 1.95, 0], [cx - 0.78, 1.25, 0], YELLOW, 4, 0.18)
        who = T("von Neergaard, 1929", 26, GREY).move_to([-3.9, 3.05, 0])
        tissue = T("same tissue both times", 24, GREY).next_to(state, DOWN, buff=0.12)

        self.at("Fill an")
        self.play(FadeIn(block), FadeIn(blk_l), FadeIn(bubs), FadeIn(state), run_time=0.9)
        self.at("pressure to inflate")
        self.play(FadeIn(axes), FadeIn(note), run_time=0.6)
        self.play(Create(air), FadeIn(air_l), run_time=1.4)
        self.at("The tissue is the same")
        self.play(FadeIn(tissue), Indicate(block, color=GREY, scale_factor=1.05), run_time=0.8)
        self.at("compared an")
        self.play(FadeIn(who), run_time=0.6)
        self.at("gum solution")
        liq_state = T("liquid-filled", 28, LIQ, weight=BOLD).move_to(state)
        self.play(ReplacementTransform(state, liq_state),
                  *[b.animate.set_fill(LIQ, 0.5) for b in bubs], Create(liq), FadeIn(liq_l), run_time=1.3)
        self.at("The liquid removes")
        self.play(FadeIn(surf_l), GrowArrow(surf_a), run_time=0.6)
        self.at("lines every")
        self.play(FadeOut(surf_l), FadeOut(surf_a), *[b.animate.set_stroke(LIQ, 3) for b in bubs], run_time=0.8)
        # gap bracket at V = 0.5
        v = 0.5
        pa = float(np.interp(v, [norm_sig(p, 6.0, 1.3) for p in ps], ps))
        pl = float(np.interp(v, [norm_sig(p, 2.8, 1.0) for p in ps], ps))
        gap = DoubleArrow([X(pl) + 0.05, Y(v), 0], [X(pa) - 0.05, Y(v), 0], buff=0, color=YELLOW,
                          stroke_width=5, tip_length=0.18)
        gap_l = T("gap: recoil from\nsurface tension", 24, YELLOW, line_spacing=0.7).move_to([4.9, -1.3, 0])
        self.at("He concluded")
        self.play(GrowFromCenter(gap), FadeIn(gap_l), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Laplace(SpokenScene):
    """one idealised alveolus; P = 2T/r filled in with the lesson's illustrative numbers."""

    def construct(self):
        cen = np.array([-3.7, 0.1, 0.0])
        circ = alveolus(2.3, cen, rim=GREY, fill=BLUE, rim_w=5)
        who = T("one alveolus", 28, BLUE).move_to([-3.7, -2.65, 0])
        nts = T("idealised sphere, not to scale", 22, GREY).move_to([-3.7, -3.15, 0])
        p_q = VGroup(T("P = ?", 34, ORANGE, weight=BOLD), T("holds it open", 22, GREY)).arrange(DOWN, buff=0.12).move_to(cen + UP * 0.8)

        eq = M("P = 2T / r", 54, ORANGE).move_to([3.3, 2.3, 0])
        t_lab = T("T: surface tension", 24, YELLOW).move_to([-3.7, 2.95, 0])
        ang = -35 * DEGREES
        rad = Line(cen, cen + 2.3 * np.array([np.cos(ang), np.sin(ang), 0]), color=TEXT, stroke_width=4)
        r_lab = T("r", 32, TEXT).move_to(cen + 1.0 * np.array([np.cos(ang), np.sin(ang), 0]) + DOWN * 0.35 + LEFT * 0.1)

        s_r = M("r = 100 µm", 34, TEXT).move_to([3.3, 1.0, 0])
        s_t = VGroup(M("T = 70 mN/m", 34, YELLOW), T("no surfactant", 24, GREY)).arrange(DOWN, buff=0.1).move_to([3.3, -0.2, 0])
        s_p = M("P = 14.3 cmH2O", 36, ORANGE).move_to([3.3, -1.55, 0])
        s_n = T("illustrative values; static", 22, GREY).move_to([3.3, -2.45, 0])
        one = T("one air-liquid surface", 24, YELLOW).move_to([3.3, 3.1, 0])

        self.at("So how hard")
        self.play(FadeIn(circ), FadeIn(who), FadeIn(nts), FadeIn(p_q), run_time=1.0)
        self.at("relation")
        self.play(circ.animate.set_stroke(YELLOW, 8), FadeIn(one), run_time=0.8)
        self.at("The pressure equals")
        self.play(Write(eq), run_time=1.4)
        self.at("surface tension")
        self.play(FadeIn(t_lab), Indicate(circ, color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.at("and r is")
        self.play(Create(rad), FadeIn(r_lab), run_time=0.8)
        self.at("Take a radius")
        self.play(FadeIn(s_r, shift=UP * 0.1), run_time=0.7)
        self.at("and a tension")
        self.play(FadeIn(s_t, shift=UP * 0.1), run_time=0.7)
        self.at("illustrative values")
        self.play(FadeIn(s_n), run_time=0.6)
        self.at("The pressure is")
        new_p = VGroup(T("P = 14.3", 34, ORANGE, weight=BOLD), T("cmH2O", 24, ORANGE)).arrange(DOWN, buff=0.1).move_to(cen + UP * 0.8)
        self.play(FadeIn(s_p, shift=UP * 0.1), ReplacementTransform(p_q, new_p), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Small(SpokenScene):
    """P = 2T/r plot; halve r doubles P; two alveoli on one airway: small empties into large."""

    def construct(self):
        T_N = 0.070

        def P_cm(r_um):
            return 2 * T_N / (r_um * 1e-6) / 98.07

        X0, X1, Y0, Y1 = -5.2, 5.3, -2.5, 2.7
        def X(r): return X0 + (r - 30) / (170 - 30) * (X1 - X0 - 0.4)
        def Y(p): return Y0 + p / 42.0 * (Y1 - Y0 - 0.3)

        axes = frame_axes(X0, X1, Y0, Y1, "radius r (µm)", "pressure P (cmH2O)", 24, 24)
        rs = np.linspace(35, 165, 40)
        cur = curve_through([(X(r), Y(P_cm(r))) for r in rs], ORANGE)
        eqlab = M("P = 2T / r", 34, ORANGE).move_to([3.0, 2.4, 0])
        tnote = T("T = 70 mN/m, same at both", 24, YELLOW).move_to([3.0, 1.6, 0])

        d100 = Dot([X(100), Y(P_cm(100)), 0], radius=0.13, color=TEXT)
        l100 = VGroup(T("r = 100 µm", 24, TEXT), M("14.3 cmH2O", 26, ORANGE)).arrange(DOWN, buff=0.08)
        l100.next_to(d100, UR, buff=0.25)
        drop100 = DashedLine([X(100), Y(P_cm(100)), 0], [X(100), Y0, 0], color=GREY, stroke_width=3)

        p50 = (X(50), Y(P_cm(50)), 0)
        d50 = Dot([X(100), Y(P_cm(100)), 0], radius=0.13, color=TEXT)
        drop50 = DashedLine([X(50), Y(P_cm(50)), 0], [X(50), Y0, 0], color=GREY, stroke_width=3)
        l50 = VGroup(T("r = 50 µm", 24, TEXT), M("28.6 cmH2O", 26, ORANGE)).arrange(DOWN, buff=0.08)
        l50.next_to(np.array(p50), RIGHT, buff=0.3).shift(UP * 0.2)
        dbl = T("halve r, double P", 30, TEXT, weight=BOLD).move_to([3.0, 0.7, 0])

        self.add(axes, cur, eqlab, d100, l100, drop100, tnote)
        self.at("the radius")

        def slide(mob, alpha):
            r = 100 + (50 - 100) * alpha
            mob.move_to([X(r), Y(P_cm(r)), 0])
        self.play(UpdateFromAlphaFunc(d50, slide), run_time=1.2)
        self.play(Create(drop50), FadeIn(l50), run_time=0.7)
        self.at("The pressure doubles")
        self.play(FadeIn(dbl, shift=UP * 0.1), run_time=0.8)

        # --- two alveoli on one airway ---
        small = alveolus(0.85, [-3.9, 0.2, 0], rim=YELLOW, fill=BLUE, rim_w=6)
        large = alveolus(1.7, [3.0, 0.2, 0], rim=YELLOW, fill=BLUE, rim_w=6)
        bar = Rectangle(width=3.05 - 0.0, height=0.36, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        bar.move_to([(-3.05 + 1.3) / 2, 0.2, 0])
        s_lab = VGroup(T("r = 50 µm", 26, TEXT), M("28.6 cmH2O", 28, ORANGE), M("T = 70 mN/m", 24, YELLOW)).arrange(DOWN, buff=0.1).move_to([-3.9, -1.9, 0])
        l_lab = VGroup(T("r = 100 µm", 26, TEXT), M("14.3 cmH2O", 28, ORANGE), M("T = 70 mN/m", 24, YELLOW)).arrange(DOWN, buff=0.1).move_to([3.0, -2.35, 0])
        air_l = T("one airway", 24, GREY).move_to([(-3.05 + 1.3) / 2, -0.55, 0])
        nts = T("idealised spheres, not to scale", 22, GREY).move_to([0, 3.15, 0])
        self.at("Join the two")
        self.play(*[FadeOut(m) for m in (axes, cur, eqlab, tnote, d100, l100, drop100, d50, drop50, l50, dbl)], run_time=0.6)
        self.play(FadeIn(small), FadeIn(large), FadeIn(bar), FadeIn(s_lab), FadeIn(l_lab), FadeIn(air_l), FadeIn(nts), run_time=1.0)
        flow = arr([-2.8, 0.85, 0], [0.9, 0.85, 0], RED, 8, 0.35)
        flow_l = T("small empties into large", 26, RED).move_to([-0.9, 1.4, 0])
        self.at("the small alveolus would empty")
        self.play(GrowArrow(flow), FadeIn(flow_l), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Film(SpokenScene):
    """surface film balance: barrier compresses the film; tension falls from about 46 to about 10 dynes per cm."""

    def construct(self):
        # --- balance schematic (left) ---
        tx0, tx1, ty0, ty1 = -6.1, -0.7, -2.5, -0.8
        trough = Rectangle(width=tx1 - tx0, height=ty1 - ty0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.15)
        trough.move_to([(tx0 + tx1) / 2, (ty0 + ty1) / 2, 0])
        t_lab = T("trough", 24, GREY).move_to([-5.2, -1.65, 0])
        surf_y = ty1 - 0.02
        film_x = ValueTracker(tx1 - 0.15)
        barrier = Rectangle(width=0.24, height=1.1, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.5)
        barrier.add_updater(lambda m: m.move_to([film_x.get_value() + 0.12, surf_y - 0.1, 0]))
        film = Line([tx0 + 0.1, surf_y, 0], [film_x.get_value(), surf_y, 0], color=GREEN, stroke_width=9)
        film.add_updater(lambda m: m.put_start_and_end_on(np.array([tx0 + 0.1, surf_y, 0]), np.array([film_x.get_value(), surf_y, 0])))
        film_l = T("film from lung extract", 26, GREEN).move_to([-2.2, 0.35, 0])
        film_p = arr([-2.7, 0.05, 0], [-3.1, surf_y + 0.1, 0], GREEN, 3, 0.15)
        bar_l = always_redraw(lambda: T("movable barrier", 24, TEXT).move_to([film_x.get_value() - 0.9, ty0 - 0.4, 0]))
        bar_p = always_redraw(lambda: arr([film_x.get_value() + 0.0, ty0 - 0.15, 0], [film_x.get_value() + 0.12, surf_y - 0.62, 0], TEXT, 3, 0.15))
        px = -4.7
        sensor = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.55, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.3).move_to([px, 1.5, 0])
        s_txt = T("sensor", 22, GREY).move_to(sensor)
        hang = Line([px, 1.22, 0], [px, surf_y - 0.2, 0], color=YELLOW, stroke_width=4)
        plate = Rectangle(width=0.5, height=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5).move_to([px, surf_y - 0.05, 0])
        plate_l = T("thin plate", 24, YELLOW).move_to([-5.55, 0.35, 0])
        plate_p = arr([-5.3, 0.1, 0], [px - 0.28, -0.6, 0], YELLOW, 3, 0.15)
        read = VGroup(T("tension", 24, YELLOW), M("about 46", 34, YELLOW), T("dynes per cm", 22, YELLOW)).arrange(DOWN, buff=0.06).move_to([px, 2.75, 0])

        # --- plot (right) ---
        X0, X1, Y0, Y1 = 1.4, 6.2, -2.4, 2.4
        axes = frame_axes(X0, X1, Y0, Y1, "film area (relative)", "tension (dynes per cm)", 24, 24)
        def X(a): return X0 + 0.5 + a * (X1 - X0 - 1.3)      # a: 0 small .. 1 large
        def Y(t): return Y0 + 0.2 + (t / 50.0) * (Y1 - Y0 - 0.7)
        axes[2].shift(DOWN * 0.35)
        tk_small = T("small", 22, GREY).move_to([X(0), Y0 - 0.3, 0])
        tk_large = T("large", 22, GREY).move_to([X(1), Y0 - 0.3, 0])
        d_big = Dot([X(1), Y(46), 0], radius=0.14, color=YELLOW)
        d_mov = Dot([X(1), Y(46), 0], radius=0.14, color=YELLOW)
        guide = DashedLine([X(1), Y(46), 0], [X(0), Y(10), 0], color=GREY, stroke_width=3)
        y46 = M("46", 26, YELLOW).move_to([X0 + 0.35, Y(46) + 0.3, 0])
        y10 = M("10", 26, YELLOW).move_to([X0 + 0.35, Y(10) + 0.3, 0])
        sketch = T("dashed line: sketch only", 22, GREY).move_to([3.8, 3.1, 0])

        self.add(axes, tk_small, tk_large, trough, t_lab)
        self.at("Surfactant changes that")
        self.wait(0.3)
        self.at("put films")
        self.add(film, barrier)
        self.play(FadeIn(film_l), GrowArrow(film_p), run_time=0.7)
        self.at("movable barrier")
        self.add(bar_l, bar_p)
        self.play(Indicate(barrier, color=TEXT, scale_factor=1.4), run_time=0.8)
        self.at("thin plate")
        self.play(FadeIn(sensor), FadeIn(s_txt), Create(hang), FadeIn(plate), FadeIn(plate_l), GrowArrow(plate_p), run_time=1.0)
        self.at("The tension depended")
        self.play(FadeIn(read), Indicate(axes[1], color=YELLOW), run_time=0.9)
        self.at("It fell from")
        self.play(FadeIn(d_big), FadeIn(y46), run_time=0.6)
        new_read = VGroup(T("tension", 24, YELLOW), M("about 10", 34, YELLOW), T("dynes per cm", 22, YELLOW)).arrange(DOWN, buff=0.06).move_to([px, 2.75, 0])
        self.at("to about")

        def slide(m, alpha):
            m.move_to([X(1 - alpha), Y(46 + (10 - 46) * alpha), 0])
        self.play(film_x.animate.set_value(-3.3), UpdateFromAlphaFunc(d_mov, slide),
                  FadeIn(guide), ReplacementTransform(read, new_read), run_time=2.6)
        self.play(FadeIn(y10), FadeIn(sketch), run_time=0.5)
        self.at("The name surfactant")
        chipg = chip("pulmonary surfactant", GREEN, size=28).move_to([-2.0, 0.35, 0])
        self.play(ReplacementTransform(film_l, chipg), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Lining(SpokenScene):
    """same two alveoli, now with a lining whose tension falls with area: 2.0 below 4.1."""

    def construct(self):
        small = alveolus(0.85, [-3.9, 0.2, 0], rim=YELLOW, fill=BLUE, rim_w=6)
        large = alveolus(1.7, [3.0, 0.2, 0], rim=YELLOW, fill=BLUE, rim_w=6)
        bar = Rectangle(width=3.05, height=0.36, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        bar.move_to([(-3.05 + 1.3) / 2, 0.2, 0])
        air_l = T("one airway", 24, GREY).move_to([(-3.05 + 1.3) / 2, -0.55, 0])
        nts = T("idealised spheres, not to scale", 22, GREY).move_to([0, 3.15, 0])

        def lab(r, p, t, color_t, color_p, x, y):
            return VGroup(T(r, 26, TEXT), M(p, 28, color_p), M(t, 24, color_t)).arrange(DOWN, buff=0.1).move_to([x, y, 0])

        s_old = lab("r = 50 µm", "28.6 cmH2O", "T = 70 mN/m", YELLOW, ORANGE, -3.9, -1.9)
        l_old = lab("r = 100 µm", "14.3 cmH2O", "T = 70 mN/m", YELLOW, ORANGE, 3.0, -2.35)
        flow = arr([-2.8, 0.85, 0], [0.9, 0.85, 0], RED, 8, 0.35)
        flow_l = T("small empties into large", 26, RED).move_to([-0.9, 1.4, 0])
        self.add(small, large, bar, air_l, nts, s_old, l_old, flow, flow_l)

        # clear the old answer and bring in the lining in one move
        s_new = lab("r = 50 µm", "P = ?", "T = ?", GREY, GREY, -3.9, -1.9)
        l_new = lab("r = 100 µm", "P = ?", "T = ?", GREY, GREY, 3.0, -2.35)
        self.at("whose tension", lead=0.6)
        self.play(FadeOut(flow), FadeOut(flow_l), FadeOut(s_old), FadeOut(l_old), run_time=0.25)
        self.play(small.animate.set_stroke(GREEN, 8), large.animate.set_stroke(GREEN, 8),
                  FadeIn(s_new), FadeIn(l_new), run_time=0.6)
        lin = T("lining: tension falls\nas area falls", 26, GREEN, line_spacing=0.7).move_to([-0.3, -1.8, 0])
        self.play(FadeIn(lin), run_time=0.6)
        self.at("illustrative")
        self.play(Indicate(lin, color=GREEN, scale_factor=1.08), run_time=0.6)
        self.at("with surfactant")
        self.play(Indicate(large, color=GREEN, scale_factor=1.05), run_time=0.7)
        self.at("tension is")
        l_t = lab("r = 100 µm", "P = ?", "T = 20 mN/m", YELLOW, GREY, 3.0, -2.35)
        self.play(Transform(l_new, l_t), run_time=0.6)
        self.at("The pressure is")
        l_p = lab("r = 100 µm", "P = 4.1 cmH2O", "T = 20 mN/m", YELLOW, ORANGE, 3.0, -2.35)
        self.play(Transform(l_new, l_p), run_time=0.6)
        self.at("tension is", nth=1)
        self.play(Indicate(small, color=GREEN, scale_factor=1.12), run_time=0.5)
        s_t = VGroup(T("r = 50 µm", 26, TEXT), M("P = ?", 28, GREY), M("T = 5 mN/m", 24, YELLOW), T("(made up)", 22, GREY)).arrange(DOWN, buff=0.08).move_to([-3.9, -2.0, 0])
        self.play(Transform(s_new, s_t), run_time=0.6)
        self.at("The pressure is", nth=1)
        s_p = VGroup(T("r = 50 µm", 26, TEXT), M("P = 2.0 cmH2O", 28, ORANGE), M("T = 5 mN/m", 24, YELLOW), T("(made up)", 22, GREY)).arrange(DOWN, buff=0.08).move_to([-3.9, -2.0, 0])
        self.play(Transform(s_new, s_p), run_time=0.6)
        cmp_ = M("2.0 < 4.1", 40, GREEN, weight=BOLD).move_to([-0.9, 1.4, 0])
        self.at("below the large")
        self.play(FadeOut(lin), FadeIn(cmp_, scale=0.9), run_time=0.7)
        self.at("no longer empties")
        res = T("the small one\nno longer empties", 28, GREEN, line_spacing=0.7).move_to([-0.3, -1.8, 0])
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """caveats (theory and in vitro; slope matters; tethered neighbours), then the rule."""

    def construct(self):
        c1 = chip("a result of theory\nand of films in vitro", GREY, size=30)
        c2 = chip("depends on how steeply\ntension changes with area", YELLOW, size=30)
        left = VGroup(c1, c2).arrange(DOWN, buff=0.8).move_to([-3.4, -0.2, 0])

        # four blocks sharing walls (schematic)
        cells = VGroup()
        s = 1.55
        ox, oy = 3.7, 0.5
        for i in range(2):
            for j in range(2):
                cells.add(Square(side_length=s, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.18)
                          .move_to([ox + (i - 0.5) * s, oy + (j - 0.5) * s, 0]))
        shared = VGroup(Line([ox, oy - s, 0], [ox, oy + s, 0], color=YELLOW, stroke_width=8),
                        Line([ox - s, oy, 0], [ox + s, oy, 0], color=YELLOW, stroke_width=8))
        g_l = T("real alveoli are tethered:\nneighbours share walls", 26, GREY, line_spacing=0.7).move_to([3.7, -1.9, 0])
        g_n = T("schematic", 22, GREY).move_to([3.7, 2.6, 0])
        rule1 = VGroup(T("Surface tension: ", 38, YELLOW, weight=BOLD), T("small alveoli are harder to hold open.", 38, TEXT)).arrange(RIGHT, buff=0.14)
        rule2 = VGroup(T("Surfactant: ", 38, GREEN, weight=BOLD), T("lowest tension when the alveolus is small.", 38, TEXT)).arrange(RIGHT, buff=0.14)
        rules = VGroup(rule1, rule2).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        fit(rules, max_w=12.2)
        rules.move_to([0, 0.0, 0])

        self.at("This emptying")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.8)
        self.at("how steeply")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.8)
        self.at("Real alveoli")
        self.play(FadeIn(cells), FadeIn(g_n), run_time=0.9)
        self.at("share walls")
        self.play(Create(shared), FadeIn(g_l), run_time=0.9)
        self.at("Keep this rule")
        self.play(*[FadeOut(m) for m in (left, cells, shared, g_l, g_n)], run_time=0.7)
        self.at("Surface tension makes")
        self.play(FadeIn(rule1, shift=UP * 0.1), run_time=0.8)
        self.at("surfactant lowers")
        self.play(FadeIn(rule2, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Surfactant lowers tension most when the alveolus is small."
