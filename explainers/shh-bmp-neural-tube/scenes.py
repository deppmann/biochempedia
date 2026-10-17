"""Sonic hedgehog and BMP in the neural tube: a slope becomes stripes  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = Sonic hedgehog and the signaling it causes (dots, curves, gauge)
  TEAL   = notochord and floor plate (the source tissue)
  BLUE   = class I factors / Pax6 / Pax7 side, and the motor neuron domain (pMN)
  ORANGE = class II factors / Nkx2.2 side, and the p3 domain
  RED    = repression (the T-bars) and nothing else
  PURPLE = Patched1 (the feedback receptor)
  GREY   = tube wall, neutral cells, axes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def mix(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), float(np.clip(t, 0, 1)))


def sig(x):
    return 1 / (1 + np.exp(-x))


def cell(x, y, color=GREY, o=0.25, w=0.62, h=0.38):
    return RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=o).move_to([x, y, 0])


def curve_pts(f, y0, y1, x0, scale, n=60):
    ys = np.linspace(y0, y1, n)
    return [np.array([x0 + scale * f(y), y, 0]) for y in ys]


def line_through(pts, color, w=6, o=1):
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=o)
    m.set_points_smoothly(pts)
    return m


def area_under(pts, x0, color, o=0.22):
    poly = Polygon(*([np.array([x0, pts[0][1], 0])] + pts + [np.array([x0, pts[-1][1], 0])]),
                   stroke_width=0, fill_color=color, fill_opacity=o)
    return poly


def dots_rising(xs, y0, dist, color=YELLOW, r=0.08):
    dots = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x, y0, 0]) for x in xs])
    return dots


# one wall of the tube as a column of cells, bottom first
COL_X = -4.2
COL_Y0, COL_Y1, COL_N = -1.9, 3.1, 12
COL_YS = np.linspace(COL_Y0, COL_Y1, COL_N)
FP_Y = -2.45
BASE_X = -3.2                      # baseline of the plots beside the column


def shh_amount(y):
    return np.exp(-(y - FP_Y) / 2.3)


def build_column(colors=None):
    cs = VGroup()
    for i, y in enumerate(COL_YS):
        c = cell(COL_X, y, GREY, 0.2)
        if colors:
            c.set_stroke(colors[i]).set_fill(colors[i], 0.55)
        cs.add(c)
    return cs


def shh_colors():
    return [YELLOW for _ in COL_YS]


def shade_by_shh(cells):
    anims = []
    for c, y in zip(cells, COL_YS):
        a = shh_amount(y)
        anims.append(c.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.1 + 0.7 * a))
    return anims


def floor_block():
    return RoundedRectangle(corner_radius=0.08, width=0.9, height=0.4, stroke_color=TEAL, stroke_width=3,
                            fill_color=TEAL, fill_opacity=0.5).move_to([COL_X, FP_Y, 0])


def noto_circle(x=COL_X, y=-3.1, r=0.3):
    return Circle(radius=r, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Sonic hedgehog and BMP in the neural tube"
    TITLE = "A slope becomes stripes"


# ---------------------------------------------------------------------------------------------
class S01Graft(SpokenScene):
    def construct(self):
        cx = -1.5
        tube = RoundedRectangle(corner_radius=1.5, width=3.0, height=4.8, stroke_color=GREY, stroke_width=6,
                                fill_color=GREY, fill_opacity=0.08).move_to([cx, 0.6, 0])
        fp = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.26, stroke_color=TEAL, stroke_width=3,
                              fill_color=TEAL, fill_opacity=0.6).move_to([cx, -1.68, 0])
        noto = Circle(radius=0.42, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35).move_to([cx, -2.7, 0])
        l_tube = T("neural tube", 24, GREY).move_to([cx, 3.3, 0])
        l_fp = T("floor plate", 24, TEAL).move_to([-4.6, -1.68, 0])
        l_fp_line = Line([-3.75, -1.68, 0], [cx - 0.85, -1.68, 0], color=TEAL, stroke_width=2)
        l_noto = T("notochord", 24, TEAL).next_to(noto, RIGHT, buff=0.3)
        self.play(FadeIn(tube), FadeIn(fp), FadeIn(noto), FadeIn(l_tube), FadeIn(l_fp), Create(l_fp_line), FadeIn(l_noto), run_time=0.7)

        # graft arrives beside the right wall
        g = Circle(radius=0.42, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35).move_to([5.6, 0.6, 0])
        gl = T("grafted notochord", 24, TEAL).move_to([5.6, 1.3, 0])
        self.at("against the side")
        gx = cx + 1.5 + 0.55
        self.play(g.animate.move_to([gx, 0.6, 0]), run_time=0.9)
        self.play(FadeIn(gl.move_to([gx + 2.1, 0.6, 0])), run_time=0.3)
        patch = RoundedRectangle(corner_radius=0.1, width=0.26, height=1.5, stroke_color=TEAL, stroke_width=3,
                                 fill_color=TEAL, fill_opacity=0.6).move_to([cx + 1.5, 0.6, 0])
        self.at("start to behave")
        self.play(GrowFromCenter(patch), run_time=0.8)
        l2 = T("second floor plate", 24, TEAL).move_to([gx + 2.1 + 0.15, -0.2, 0])
        l2.align_to(gl, LEFT)
        self.at("second bottom")
        self.play(FadeIn(l2, shift=UP * 0.1), Indicate(patch, color=TEAL, scale_factor=1.15), run_time=0.8)

        # the question
        qs = VGroup(*[T("?", 40, TEXT, weight=BOLD).move_to([cx - 2.1, y, 0]) for y in (-0.4, 0.8, 2.0)])
        meas = DoubleArrow([cx - 1.85, -1.5, 0], [cx - 1.85, 2.9, 0], color=GREY, stroke_width=4, tip_length=0.2, buff=0)
        self.at("how does a cell")
        main = VGroup(tube, fp, noto, l_tube, l_fp, l_fp_line, l_noto, meas, qs)
        self.play(FadeOut(VGroup(g, gl, patch, l2)), run_time=0.4)
        self.add(meas, qs)
        meas.set_opacity(0), qs.set_opacity(0)
        self.play(VGroup(tube, fp, noto, l_tube, l_fp, l_fp_line, l_noto, meas, qs).animate.shift(RIGHT * 1.5), run_time=0.6)
        self.play(meas.animate.set_opacity(1), LaggedStart(*[q.animate.set_opacity(1) for q in qs], lag_ratio=0.25), run_time=1.0)

        # the answer rises
        self.at("Sonic hedgehog")
        chipy = chip("Sonic hedgehog", YELLOW, 28).move_to([4.3, 0.6, 0])
        cx = cx + 1.5
        dxs = (-0.9, -0.5, -0.15, 0.2, 0.55, 0.9, -0.7, 0.35, -0.3, 0.7)
        dots = VGroup(*[Circle(radius=0.1, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([cx + dx, -1.35, 0])
                        for dx in dxs])
        self.play(FadeIn(chipy), FadeIn(dots), run_time=0.4)
        self.play(LaggedStart(*[d.animate.shift(UP * (1.6 + 0.3 * i)).set_opacity(0.25) for i, d in enumerate(dots)], lag_ratio=0.12),
                  run_time=2.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Slope(SpokenScene):
    def construct(self):
        cells = build_column()
        fp, noto = floor_block(), noto_circle()
        l_fp = T("floor plate", 24, TEAL).move_to([-5.75, FP_Y, 0])
        l_n = T("notochord", 24, TEAL).move_to([-5.45, -3.1, 0])
        self.play(FadeIn(cells), FadeIn(fp), FadeIn(noto), FadeIn(l_fp), FadeIn(l_n), run_time=0.6)

        # source makes the signal
        self.at("both make")
        chipy = chip("Sonic hedgehog", YELLOW, 26).move_to([-0.2, -2.9, 0])
        self.play(Indicate(fp, color=TEAL), Indicate(noto, color=TEAL), FadeIn(chipy, shift=UP * 0.15), run_time=0.8)
        dots = dots_rising([COL_X - 0.2, COL_X, COL_X + 0.2, COL_X - 0.1, COL_X + 0.1, COL_X - 0.25, COL_X + 0.25, COL_X], FP_Y + 0.35, 4)
        self.add(dots)
        self.at("spreads up")
        self.play(LaggedStart(*[d.animate.shift(UP * (1.2 + 0.55 * i)) for i, d in enumerate(dots)], lag_ratio=0.1), run_time=1.6)

        # the curve
        f = shh_amount
        pts = curve_pts(f, COL_Y0 - 0.1, COL_Y1 + 0.1, BASE_X, 5.0)
        base = Line([BASE_X, FP_Y, 0], [BASE_X, COL_Y1 + 0.3, 0], color=GREY, stroke_width=3)
        crv = line_through(pts, YELLOW, 6)
        shade = area_under(pts, BASE_X, YELLOW, 0.2)
        self.at("falls off")
        self.play(FadeOut(dots), Create(base), run_time=0.3)
        self.play(Create(crv), FadeIn(shade), *shade_by_shh(cells), run_time=1.6)
        lbl = T("amount of Sonic hedgehog", 24, YELLOW).move_to([2.35, 3.15, 0])
        self.play(FadeIn(lbl), run_time=0.4)

        mg = chip("morphogen", YELLOW, 32).move_to([3.9, 1.1, 0])
        self.at("is called")
        self.play(FadeIn(mg, scale=0.8), run_time=0.6)

        # a lot / little
        lot = T("a lot", 30, YELLOW).move_to([pts[2][0] + 0.9, -1.55, 0])
        lit = T("little", 30, YELLOW).move_to([pts[-3][0] + 1.3, 2.85, 0])
        self.at("receive a lot")
        self.play(FadeIn(lot), Indicate(VGroup(*cells[:3]), color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.at("receive little")
        self.play(FadeIn(lit), Indicate(VGroup(*cells[-3:]), color=YELLOW, scale_factor=1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
PAX_Y, NKX_Y = 0.9, -1.0


def pax7(y):
    return sig((y - PAX_Y) / 0.25)


def nkx22(y):
    return 1 - sig((y - NKX_Y) / 0.2)


def factor_colors():
    out = []
    for y in COL_YS:
        if pax7(y) > 0.5:
            out.append(BLUE)
        elif nkx22(y) > 0.5:
            out.append(ORANGE)
        else:
            out.append(GREY)
    return out


class S03Read(SpokenScene):
    def construct(self):
        cells = build_column()
        fp, noto = floor_block(), noto_circle()
        for c, y in zip(cells, COL_YS):
            a = shh_amount(y)
            c.set_stroke(YELLOW).set_fill(YELLOW, 0.1 + 0.7 * a)
        pts = curve_pts(shh_amount, COL_Y0 - 0.1, COL_Y1 + 0.1, BASE_X, 5.0)
        base = Line([BASE_X, FP_Y, 0], [BASE_X, COL_Y1 + 0.3, 0], color=GREY, stroke_width=3)
        crv = line_through(pts, YELLOW, 6, 1)
        self.add(cells, fp, noto, base, crv)
        # more signal arrow on the left
        ar = arr([-5.5, 2.7, 0], [-5.5, -1.7, 0], YELLOW, 6)
        al = T("more signal", 24, YELLOW).rotate(PI / 2).move_to([-5.95, 0.5, 0])
        self.play(crv.animate.set_stroke(opacity=0.35), FadeIn(ar), FadeIn(al), run_time=0.7)

        self.at("transcription factors")
        for_cap = T("factor present", 24, GREY).move_to([-0.6, 3.15, 0])
        self.play(FadeIn(for_cap), run_time=0.4)

        # class I
        p_pts = curve_pts(pax7, COL_Y0 - 0.1, COL_Y1 + 0.1, BASE_X, 5.0)
        p_crv = line_through(p_pts, BLUE, 7)
        chip1 = chip("class I: Pax7", BLUE, 26).move_to([3.9, 2.4, 0])
        self.at("factors are repressed")
        self.play(Create(p_crv), FadeIn(chip1, shift=LEFT * 0.2), run_time=1.2)
        self.at("lost where")
        self.play(Indicate(VGroup(*cells[:4]), color=BLUE, scale_factor=1.1), run_time=0.8)

        # class II
        n_pts = curve_pts(nkx22, COL_Y0 - 0.1, COL_Y1 + 0.1, BASE_X, 5.0)
        n_crv = line_through(n_pts, ORANGE, 7)
        chip2 = chip("class II: Nkx2.2", ORANGE, 26).move_to([3.9, -1.0, 0])
        self.at("factors need the signal")
        self.play(Create(n_crv), FadeIn(chip2, shift=LEFT * 0.2), run_time=1.2)

        # cells take the colour of the factor they carry
        cols = factor_colors()
        self.at("switched off by low")
        self.play(*[c.animate.set_stroke(col).set_fill(col, 0.55) for c, col in zip(cells, cols) if col == BLUE],
                  Indicate(chip1, color=BLUE), run_time=1.0)
        dors = T("dorsal half", 26, BLUE).move_to([3.9, 1.35, 0])
        self.play(FadeIn(dors), run_time=0.4)
        self.at("needs high levels")
        self.play(*[c.animate.set_stroke(col).set_fill(col, 0.55) for c, col in zip(cells, cols) if col == ORANGE],
                  Indicate(chip2, color=ORANGE), run_time=1.0)
        nxt = T("next to the floor plate", 26, ORANGE).move_to([3.9, -1.7, 0])
        self.play(FadeIn(nxt), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def gauge_y(t):
    return -2.2 + 4.4 * t


class S04Time(SpokenScene):
    def construct(self):
        # feedback loop on one cell (built large and centred, then moved left when the plot arrives)
        shh = chip("Sonic hedgehog", YELLOW, 24).move_to([-4.3, 3.0, 0])
        body = Circle(radius=0.9, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([-4.3, 1.0, 0])
        sg = T("signaling", 24, YELLOW).move_to(body)
        a1 = arr([-4.3, 2.65, 0], [-4.3, 1.95, 0], YELLOW)
        pt = chip("Patched1", PURPLE, 26).move_to([-4.3, -1.6, 0])
        a2 = arr([-4.75, 0.2, 0], [-4.75, -1.15, 0], YELLOW)
        ih = inhib([-3.85, -1.15, 0], [-3.85, 0.22, 0], RED)
        less = T("less sensitive", 24, RED).move_to([-4.3, -2.55, 0])
        diag = VGroup(shh, body, sg, a1, pt, a2, ih, less)
        diag.save_state()
        diag.scale(1.1).move_to([0, 0.25, 0])
        self.at("read more")
        self.play(FadeIn(shh), GrowArrow(a1), FadeIn(body), FadeIn(sg), run_time=0.8)
        self.at("its own receptor")
        self.play(GrowArrow(a2), FadeIn(pt, shift=UP * 0.2), run_time=0.7)
        self.at("less sensitive")
        self.play(Create(ih), FadeIn(less), run_time=0.7)
        self.play(Restore(diag), run_time=0.8)

        # plot of signaling over time
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.1, 0.5], x_length=6.4, y_length=4.7, tips=False,
                  axis_config={"color": GREY, "stroke_width": 3, "include_ticks": False}).move_to([1.6, -0.35, 0])
        xl = T("time", 24, GREY).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
        yl = T("signaling in the cell", 24, YELLOW).move_to([1.1, 2.75, 0])
        yl.align_to(ax.y_axis, LEFT)
        f_hi = lambda t: 1.0 * (1 - np.exp(-t / 0.4)) * np.exp(-t / 5.0)
        f_lo = lambda t: 0.5 * (1 - np.exp(-t / 0.4)) * np.exp(-t / 1.6)
        g_lo = ax.plot(f_lo, x_range=[0, 10], color=YELLOW, stroke_width=4).set_stroke(opacity=0.6)
        g_hi = ax.plot(f_hi, x_range=[0, 10], color=YELLOW, stroke_width=7)
        self.at("signaling fades")
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.5)
        self.play(Create(g_lo), run_time=0.8)

        lab_lo = T("lower dose", 24, YELLOW).set_opacity(0.8).move_to(ax.c2p(4.6, 0.2))
        lab_hi = T("higher dose", 24, YELLOW).move_to(ax.c2p(6.9, 0.62))
        self.at("higher dose")
        self.play(Create(g_hi), FadeIn(lab_lo), run_time=1.3)
        self.play(FadeIn(lab_hi), run_time=0.4)

        # fixed dose, longer exposure
        tr = ValueTracker(0.001)
        area = always_redraw(lambda: ax.get_area(g_hi, x_range=(0, max(tr.get_value(), 0.01)), color=YELLOW, opacity=0.3))
        line_t = always_redraw(lambda: DashedLine(ax.c2p(tr.get_value(), 0), ax.c2p(tr.get_value(), f_hi(tr.get_value())),
                                                   color=TEXT, stroke_width=3))
        ga = arr([5.85, gauge_y(0), 0], [5.85, gauge_y(1) + 0.1, 0], GREY, 5)
        gl = T("model:\nmore\nventral", 24, GREY, line_spacing=0.8).move_to([5.85, 2.95, 0])
        mark = always_redraw(lambda: Dot([5.85, gauge_y(tr.get_value() / 10), 0], radius=0.14, color=YELLOW))
        self.at("At a fixed dose")
        self.play(FadeOut(VGroup(g_lo, lab_lo)), g_hi.animate.set_stroke(width=7), FadeOut(lab_hi),
                  FadeIn(ga), FadeIn(gl), run_time=0.7)
        self.add(area, line_t, mark)
        self.at("longer exposure")
        self.play(tr.animate.set_value(8.5), run_time=3.2, rate_func=linear)
        tot = T("total signaling", 26, TEXT).move_to(ax.c2p(3.0, 0.22))
        self.at("total signaling")
        self.play(FadeIn(tot), Indicate(area, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
BX = -3.3
B_YS = np.linspace(-2.6, 2.9, 12)
B_BORDER = 6            # index of the border cell; cells 0..5 are the lower (Nkx2.2) block


def bcell(i, color=GREY, o=0.5):
    return cell(BX, B_YS[i], color, o, w=0.8, h=0.42)


class S05Switch(SpokenScene):
    def construct(self):
        # smooth blur: blend from orange (bottom) to blue (top)
        cells = VGroup(*[bcell(i, mix(ORANGE, BLUE, i / 11), 0.55) for i in range(12)])
        slope = arr([-5.5, 2.8, 0], [-5.5, -2.5, 0], YELLOW, 6)
        sl = T("slope", 24, YELLOW).rotate(PI / 2).move_to([-5.95, 0.2, 0])
        # mark the column as a close-up of one border in the ventral wall
        mt = RoundedRectangle(corner_radius=0.35, width=0.8, height=1.3, stroke_color=GREY, stroke_width=3).move_to([1.0, 2.35, 0])
        mfp = RoundedRectangle(corner_radius=0.05, width=0.36, height=0.12, stroke_color=TEAL, stroke_width=2,
                               fill_color=TEAL, fill_opacity=0.5).move_to([1.0, 1.72, 0])
        zb = Rectangle(width=0.22, height=0.3, stroke_color=TEXT, stroke_width=2.5).move_to([0.6, 2.05, 0])
        zf = Rectangle(width=1.5, height=5.95, stroke_color=TEXT, stroke_width=2.5).move_to([BX, 0.17, 0])
        zl = VGroup(DashedLine(zb.get_corner(UL), zf.get_corner(UR), color=GREY, stroke_width=2),
                    DashedLine(zb.get_corner(DL), zf.get_corner(DR), color=GREY, stroke_width=2))
        zt = T("close-up", 24, TEXT).move_to([BX, -3.2, 0])
        self.at("smooth slope")
        self.play(FadeIn(mt), FadeIn(mfp), FadeIn(zb), run_time=0.4)
        self.play(FadeIn(cells), FadeIn(slope), FadeIn(sl), Create(zl), FadeIn(zf), FadeIn(zt), run_time=0.8)
        blur = T("a blur?", 32, GREY).move_to([1.6, -0.4, 0])
        self.at("a blur")
        self.play(FadeIn(blur), run_time=0.5)

        # sharp borders (except the border cell)
        self.at("borders are sharp")
        anims = []
        for i, c in enumerate(cells):
            if i == B_BORDER:
                continue
            col = ORANGE if i < B_BORDER else BLUE
            anims.append(c.animate.set_stroke(col).set_fill(col, 0.55))
        bline = DashedLine([BX - 0.7, (B_YS[B_BORDER - 1] + B_YS[B_BORDER]) / 2, 0], [BX + 0.7, (B_YS[B_BORDER - 1] + B_YS[B_BORDER]) / 2, 0],
                           color=TEXT, stroke_width=3)
        self.play(*anims, FadeOut(blur), run_time=0.8)

        # factors repress each other
        pax = chip("Pax6", BLUE, 30).move_to([0.9, 1.7, 0])
        nkx = chip("Nkx2.2", ORANGE, 30).move_to([0.9, -0.9, 0])
        i1 = inhib([0.55, 1.25, 0], [0.55, -0.45, 0], RED)
        i2 = inhib([1.25, -0.45, 0], [1.25, 1.25, 0], RED)
        self.at("repress each other")
        self.play(FadeOut(VGroup(mt, mfp, zb, zl)), run_time=0.3)
        self.play(FadeIn(pax), FadeIn(nkx), run_time=0.4)
        self.play(Create(i1), Create(i2), run_time=0.8)

        l_mn = T("motor neuron\ndomain", 24, BLUE, line_spacing=0.8).move_to([BX + 2.15, 1.3, 0])
        l_p3 = T("domain\nbelow", 24, ORANGE, line_spacing=0.8).move_to([BX + 2.15, -1.3, 0])
        self.at("motor neuron domain")
        self.play(FadeIn(l_mn), FadeIn(l_p3), FadeIn(bline), run_time=0.7)

        # two-well switch
        wx0, wy0 = 4.3, 0.2
        well = lambda x: (x ** 2 - 1) ** 2
        wl = ParametricFunction(lambda x: np.array([wx0 + 1.45 * x, wy0 - 1.3 + 2.0 * well(x), 0]), t_range=[-1.5, 1.5],
                                color=GREY, stroke_width=6)
        bl = Dot([wx0 - 1.45, wy0 - 1.3, 0], radius=0.01, fill_opacity=0)
        wlab = T("two stable states", 26, GREY).move_to([wx0, wy0 - 2.6, 0])
        lab_l = T("Pax6", 24, BLUE).move_to([wx0 - 1.45, wy0 - 1.85, 0])
        lab_r = T("Nkx2.2", 24, ORANGE).move_to([wx0 + 1.45, wy0 - 1.85, 0])
        ball = Dot([wx0, wy0 + 0.7 + 0.12, 0], radius=0.17, color=TEXT)
        self.at("switch with two stable states")
        self.play(Create(wl), FadeIn(ball), run_time=1.0)
        self.play(FadeIn(wlab), FadeIn(lab_l), FadeIn(lab_r), run_time=0.5)

        # the border cell falls to one side
        self.at("falls to one side")
        path_x = lambda s: wx0 - 1.0 * s
        self.play(ball.animate.move_to([wx0 - 1.45 * 0.97, wy0 - 1.3 + 0.17 + 0.05, 0]), run_time=1.1, rate_func=smooth)
        self.play(cells[B_BORDER].animate.set_stroke(BLUE).set_fill(BLUE, 0.55), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Stripes(SpokenScene):
    def construct(self):
        # the slope on the left, as a smooth yellow bar
        sx, sw = -5.4, 0.55
        n = 40
        top, bot = 2.95, -2.15
        h = (top - bot) / n
        bar = VGroup(*[Rectangle(width=sw, height=h + 0.01, stroke_width=0, fill_color=YELLOW,
                                 fill_opacity=0.18 + 0.75 * np.exp(-(n - 1 - i) / (n / 2.2))).move_to([sx, top - (i + 0.5) * h, 0])
                       for i in range(n)])
        fp = RoundedRectangle(corner_radius=0.08, width=2.9, height=0.5, stroke_color=TEAL, stroke_width=3,
                              fill_color=TEAL, fill_opacity=0.5).move_to([-1.2, -2.4, 0])
        fpl = T("floor plate", 24, TEXT).move_to([-1.2, -2.4, 0])
        sl = T("slope", 24, YELLOW).move_to([sx, 3.3, 0])
        self.play(FadeIn(bar), FadeIn(sl), run_time=0.6)

        names = ["p0", "p1", "p2", "pMN", "p3"]
        cols = [GREY, GREY, GREY, BLUE, ORANGE]
        ops = [0.2, 0.34, 0.2, 0.55, 0.55]
        outs = ["V0 interneurons", "V1 interneurons", "V2 interneurons", "motor neurons", "V3 neurons"]
        sh = 0.5
        ys = [0.35 - sh * (i + 0.5) for i in range(5)]
        dors = Rectangle(width=2.9, height=2.45, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([-1.2, 1.7, 0])
        dl = T("dorsal domains", 26, GREY).move_to(dors)
        stripes = VGroup(*[Rectangle(width=2.9, height=sh - 0.06, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=o)
                           .move_to([-1.2, y, 0]) for c, o, y in zip(cols, ops, ys)])
        lbls = VGroup(*[T(nm, 26, c if c != GREY else TEXT, weight=BOLD).move_to([-3.35 + 0.0, y, 0]) for nm, c, y in zip(names, cols, ys)])
        for l in lbls:
            l.set_x(-3.3)
        self.at("ventral stripes")
        self.play(FadeIn(fp), FadeIn(fpl), run_time=0.5)
        self.play(FadeIn(dors), FadeIn(dl), LaggedStart(*[FadeIn(s, scale=0.92) for s in stripes], lag_ratio=0.15), run_time=1.3)
        for nm, l in zip(["p0", "p1", "p2", "pmn", "p3"], lbls):
            self.at(nm)
            self.play(FadeIn(l, shift=RIGHT * 0.15), run_time=0.4)

        arrows = VGroup(*[arr([0.4, y, 0], [1.0, y, 0], GREY, 4, 0.16) for y in ys])
        olbls = VGroup(*[T(o, 26, c if c != GREY else TEXT).move_to([1.1, y, 0]).align_to([1.15, 0, 0], LEFT)
                         for o, c, y in zip(outs, cols, ys)])
        for cue, a_, o_ in zip(["V0", "V1", "V2", "motor neurons", "V3"], arrows, olbls):
            self.at(cue)
            self.play(FadeIn(a_), FadeIn(o_, shift=RIGHT * 0.15), run_time=0.4)

        self.at("Keep this rule")
        self.play(FadeOut(arrows), FadeOut(olbls), run_time=0.5)
        r1 = chip("1  a source makes a slope", YELLOW, 26)
        r2 = chip("2  cells read level and duration", YELLOW, 26)
        r3 = chip("3  cross-repression sharpens it", RED, 26)
        for r, y in zip((r1, r2, r3), (1.6, 0.2, -1.2)):
            r.move_to([0, y, 0]).align_to([1.0, 0, 0], LEFT)
        self.at("makes a slope")
        self.play(FadeIn(r1, shift=RIGHT * 0.2), run_time=0.6)
        self.at("level and its duration")
        self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=0.6)
        self.at("sharpens it")
        self.play(FadeIn(r3, shift=RIGHT * 0.2), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A source makes a slope; cross-repression sharpens it into domains."
