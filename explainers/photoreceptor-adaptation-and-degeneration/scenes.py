"""Photoreceptor adaptation: delete the calcium sensors and adaptation stays  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = light (background light, the flash)
  ORANGE = calcium (dots, gauge, bath tag, the calcium-dependent mechanism)
  PURPLE = the two calcium sensors, GCAPs and recoverin (and their kinase partner chip)
  TEAL   = membrane proteins (CNG channels, the pump)
  GREEN  = cGMP, adaptation / gain control, the dark state
  PINK   = activated visual pigment
  BLUE   = control cones (curve, label, bars)
  RED    = removed / lacking / off (crossed-out sensors, knockout cones, the off T-bar, "not clamped")
  GREY   = membranes, outlines, unknowns (dashed question-mark boxes)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=22, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor(c, color, op=0.16):
    return [c[1].animate.set_stroke(color).set_fill(color, op), c[2].animate.set_color(color)]


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.05
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def cone_cell(color=GREY, s=1.0):
    """A simple cone cell: tapered outer segment on top, rounded cell body, a stub of axon."""
    outer = Polygon([-0.55, 0, 0], [0.55, 0, 0], [0.14, 1.7, 0], [-0.14, 1.7, 0], stroke_color=color, stroke_width=4,
                    fill_color=color, fill_opacity=0.18)
    body = RoundedRectangle(corner_radius=0.4, width=1.4, height=1.1, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.18).move_to([0, -0.55, 0])
    stub = Line([0, -1.1, 0], [0, -1.6, 0], color=color, stroke_width=4)
    g = VGroup(outer, body, stub).scale(s)
    g.outer, g.body = outer, body
    return g


def cross(mob, color=RED, w=6):
    r = mob.get_right()[0] - 0.12
    l = mob.get_left()[0] + 0.12
    t = mob.get_top()[1] - 0.05
    b = mob.get_bottom()[1] + 0.05
    return VGroup(Line([l, t, 0], [r, b, 0], color=color, stroke_width=w), Line([l, b, 0], [r, t, 0], color=color, stroke_width=w))


def bar(left, y, w, color, h=0.4):
    return Rectangle(width=max(w, 0.05), height=h, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([left + max(w, 0.05) / 2, y, 0])


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def make_plot(dim_axes=False):
    """Log-log plot of relative sensitivity S/Sdark against background I, computed from the lesson's fit values."""
    ax = Axes(x_range=[2, 6, 1], y_range=[-3, 0, 1], x_length=8.2, y_length=4.5,
              axis_config={"color": GREY, "stroke_width": 3, "include_ticks": True, "include_tip": False},
              ).move_to([-1.9, -0.25, 0])
    grid = VGroup(*[Line(ax.c2p(2, y), ax.c2p(6, y), color=GREY, stroke_width=1, stroke_opacity=0.25) for y in (-1, -2, -3)])
    xl = VGroup(*[T("10" + str(k).translate(SUP), 22, GREY).next_to(ax.c2p(k, -3), DOWN, buff=0.15) for k in range(2, 7)])
    yl = VGroup(*[T(s, 22, GREY).next_to(ax.c2p(2, y), LEFT, buff=0.15)
                  for y, s in ((0, "1"), (-1, "0.1"), (-2, "0.01"), (-3, "0.001"))])
    xt = T("background light (photons per µm² per s)", 22, GREY).next_to(xl, DOWN, buff=0.12)
    yt = T("relative sensitivity, S / Sdark", 22, GREY).move_to([-1.9, 2.55, 0])
    base = VGroup(grid, ax, xl, yl, xt, yt)
    return ax, base


def logS(x, I0, n):
    return -np.log10(1 + 10 ** (n * (x - np.log10(I0))))


CTRL = dict(I0=48800, n=1.0)
KO = dict(I0=12100, n=1.5)


def fit_curve(ax, p, color):
    return ax.plot(lambda x: logS(x, p["I0"], p["n"]), x_range=[2, 6, 0.02], color=color, stroke_width=6, use_smoothing=False)


class S00Title(TitleCard):
    LESSON = "Photoreceptors across a billion-fold range, and when they fail"
    TITLE = "Delete the sensors, adaptation stays"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """a cone, a background-light bar and a sensitivity meter; the two sensors are crossed out and the meter still falls."""

    def construct(self):
        cone = cone_cell(BLUE, 1.5).move_to([-4.6, -0.2, 0])
        cone_lbl = T("mouse cone", 26, BLUE).next_to(cone, DOWN, buff=0.15)
        self.at("A mouse cone")
        self.play(FadeIn(cone, shift=UP * 0.1), FadeIn(cone_lbl), run_time=0.7)

        L = 0.9
        lt_lbl = T("background light", 26, YELLOW).move_to([3.0, 2.55, 0])
        se_lbl = T("sensitivity", 26, BLUE).move_to([3.0, 0.75, 0])
        lt = bar(L, 1.95, 0.6, YELLOW)
        se = bar(L, 0.15, 4.4, BLUE)
        self.at("Its sensitivity resets")
        self.play(FadeIn(lt_lbl), FadeIn(se_lbl), FadeIn(lt), FadeIn(se), run_time=0.7)
        self.at("brightens")
        self.play(Transform(lt, bar(L, 1.95, 4.4, YELLOW)), Transform(se, bar(L, 0.15, 1.0, BLUE)), run_time=0.9)
        ad = T("adaptation", 30, GREEN, weight=BOLD).move_to([3.0, -0.65, 0])
        self.at("That reset is called")
        self.play(FadeIn(ad, shift=UP * 0.1), run_time=0.5)

        self.at("two calcium sensors")
        c1 = bchip("GCAPs", PURPLE, 26).move_to([-1.8, 1.3, 0])
        c2 = bchip("recoverin", PURPLE, 26).move_to([-1.8, 0.2, 0])
        l1 = Line(cone.get_right() + LEFT * 0.3 + UP * 0.9, c1.get_left(), color=PURPLE, stroke_width=3)
        l2 = Line(cone.get_right() + LEFT * 0.2 + DOWN * 0.1, c2.get_left(), color=PURPLE, stroke_width=3)
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(c2, shift=LEFT * 0.2), Create(l1), Create(l2), run_time=0.9)
        self.at("Delete both")
        x1, x2 = cross(c1), cross(c2)
        self.play(Create(x1), Create(x2), run_time=0.7)
        self.at("still adapts")
        self.play(Transform(lt, bar(L, 1.95, 0.6, YELLOW)), Transform(se, bar(L, 0.15, 4.4, BLUE)), run_time=0.4)
        self.play(Transform(lt, bar(L, 1.95, 4.4, YELLOW)), Transform(se, bar(L, 0.15, 1.0, BLUE)), run_time=1.1)
        self.play(Indicate(ad, color=GREEN, scale_factor=1.15), run_time=0.5)

        q = RoundedRectangle(corner_radius=0.2, width=5.4, height=1.5, stroke_color=GREY, stroke_width=4, fill_opacity=0)
        q = DashedVMobject(q, num_dashes=40).move_to([3.0, -2.15, 0])
        qm = T("?", 64, TEXT, weight=BOLD).move_to([3.0, -2.15, 0])
        self.at("doing the work")
        self.play(Create(q), FadeIn(qm, scale=1.4), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Loop(SpokenScene):
    """outer-segment membrane: light closes CNG channels, calcium entry stops, pump removes calcium, GCAPs and recoverin act."""

    def construct(self):
        cap = RoundedRectangle(corner_radius=0.6, width=8.4, height=4.0, stroke_color=GREY, stroke_width=4,
                               fill_color=GREY, fill_opacity=0.08).move_to([-2.3, -0.4, 0])
        cx = [-5.0, -3.2, -1.4]
        chans = [bchip("CNG", TEAL, 22).move_to([x, 1.6, 0]) for x in cx]
        ol = T("outer segment", 22, GREY).move_to([-5.2, -1.95, 0])
        pump = VGroup(RoundedRectangle(corner_radius=0.12, width=0.7, height=0.5, stroke_color=TEAL, stroke_width=2.5,
                                       fill_color=BG, fill_opacity=1).move_to([-3.2, -2.4, 0]),
                      RoundedRectangle(corner_radius=0.12, width=0.7, height=0.5, stroke_color=TEAL, stroke_width=2.5,
                                       fill_color=TEAL, fill_opacity=0.16).move_to([-3.2, -2.4, 0]))
        pump_lbl = T("NCKX pump", 22, TEAL).move_to([-1.9, -1.95, 0])
        out_dots = [Dot([x, 2.1, 0], radius=0.1, color=ORANGE) for x in cx]
        in_dots = [Dot([x, 1.0, 0], radius=0.1, color=ORANGE) for x in cx]
        g_lbl = T("calcium in\nouter segment", 22, ORANGE, line_spacing=0.8).move_to([4.6, 2.3, 0])
        sk2 = T("sketch, not to scale", 22, GREY).move_to([4.6, -3.0, 0])
        g_box = Rectangle(width=0.9, height=3.6, stroke_color=GREY, stroke_width=3).move_to([4.6, -0.5, 0])

        def gfill(h):
            return Rectangle(width=0.9, height=h, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8).move_to([4.6, -2.3 + h / 2, 0])
        gf = gfill(3.0)
        base = VGroup(sk2, cap, *chans, ol, pump, pump_lbl, *out_dots, *in_dots, g_lbl, g_box, gf)
        self.add(base)

        # light closes the channels
        arrows = [arr([x, 3.4, 0], [x, 1.2, 0], YELLOW, 6) for x in (-4.1, -2.3, -0.5)]
        lt = T("light", 28, YELLOW).move_to([-6.2, 3.0, 0])
        self.at("Light closes channels")
        self.play(*[GrowArrow(a) for a in arrows], FadeIn(lt), run_time=0.5)
        self.play(*[x for c in chans for x in recolor(c, GREY, 0.05)], *[d.animate.set_opacity(0) for d in in_dots], run_time=0.5)
        self.at("stops entering")
        self.play(*[FadeOut(d) for d in out_dots], run_time=0.8)

        # the pump keeps removing calcium
        exit_dots = [Dot([-3.2, -2.0, 0], radius=0.1, color=ORANGE) for _ in range(2)]
        self.at("pump keeps removing")
        self.play(*[FadeIn(d) for d in exit_dots], Indicate(pump_lbl, color=TEAL), run_time=0.5)
        self.play(exit_dots[0].animate.move_to([-3.2, -3.1, 0]), exit_dots[1].animate.move_to([-3.2, -2.55, 0]), run_time=0.8)
        self.at("calcium falls")
        self.play(Transform(gf, gfill(0.8)), FadeOut(VGroup(*exit_dots)), run_time=1.3)

        # GCAPs speed cGMP synthesis, channels reopen
        gcap = bchip("GCAPs", PURPLE, 22).move_to([-5.0, 0.45, 0])
        lowca = T("low", 22, ORANGE).next_to(g_box, RIGHT, buff=0.1)
        self.at("At low calcium")
        self.play(FadeIn(gcap, shift=DOWN * 0.1), FadeIn(lowca), run_time=0.6)
        cg = bchip("cGMP", GREEN, 22).move_to([-3.2, 0.45, 0])
        a_g = arr(gcap.get_right(), cg.get_left(), PURPLE)
        self.at("speed")
        self.play(GrowArrow(a_g), FadeIn(cg), run_time=0.7)
        ups = [arr([-3.5, 0.8, 0], [-4.9, 1.25, 0], GREEN, 4, 0.16), arr([-3.2, 0.8, 0], [-3.2, 1.25, 0], GREEN, 4, 0.16), arr([-2.9, 0.8, 0], [-1.5, 1.25, 0], GREEN, 4, 0.16)]
        self.at("reopens channels")
        self.play(*[GrowArrow(u) for u in ups], *[x for c in chans for x in recolor(c, TEAL)], run_time=0.8)

        # recoverin lets go of GRK1; GRK1 switches off activated pigment
        rec = bchip("recoverin", PURPLE, 22).move_to([-5.0, -0.75, 0])
        grk = bchip("GRK1", PURPLE, 22).next_to(rec, RIGHT, buff=0.0)
        self.at("Recoverin lets go")
        self.play(FadeIn(rec), FadeIn(grk), run_time=0.5)
        self.play(grk.animate.move_to([-2.6, -0.75, 0]), run_time=0.8)
        pig = bchip("activated pigment", PINK, 22).move_to([0.0, -0.75, 0])
        tb = inhib([-2.0, -0.75, 0], [pig.get_left()[0] - 0.05, -0.75, 0], RED)
        self.at("switches off activated pigment")
        self.play(FadeIn(pig), Create(tb), run_time=0.6)
        self.play(*recolor(pig, GREY, 0.05), run_time=0.5)

        back = bchip("back toward the dark state", GREEN, 22).move_to([-0.7, -3.15, 0])
        self.at("push the cell back")
        self.play(FadeIn(back, shift=UP * 0.1), run_time=0.6)
        gc = T("gain control", 34, GREEN, weight=BOLD).move_to([4.6, -3.0, 0])
        self.play(FadeOut(sk2), run_time=0.2)
        self.at("gain control")
        self.play(Write(gc), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cut(SpokenScene):
    """two cones in isolated mouse retina: control with three sensors, knockout with all three crossed; both still adapt."""

    def construct(self):
        y1, y2 = 0.75, -1.45
        cone1 = cone_cell(BLUE, 0.55).move_to([-5.9, y1 - 0.05, 0])
        names = ["GCAP1", "GCAP2", "recoverin"]
        xs = [-4.1, -2.5, -0.8]

        def row(y):
            return [bchip(n, PURPLE, 22).move_to([x, y, 0]) for n, x in zip(names, xs)]
        r1 = row(y1)
        L = 2.1
        W = 3.6
        se1 = bar(L, y1, W, BLUE)
        sl = T("flash sensitivity", 22, BLUE).move_to([L + 1.35, y1 + 0.5, 0])
        sk = T("qualitative sketch: bar lengths are not data", 22, GREY).move_to([0.0, -3.2, 0])
        self.add(cone1, *r1, sk)
        self.at("To test a loop")
        self.play(FadeIn(se1), FadeIn(sl), run_time=0.5)

        cone2 = cone_cell(RED, 0.55).move_to([-5.9, y2 - 0.05, 0])
        r2 = row(y2)
        se2 = bar(L, y2, W, RED)
        self.at("cut it")
        self.play(FadeIn(cone2), *[FadeIn(c) for c in r2], FadeIn(se2), run_time=0.5)
        xr = [cross(c) for c in r2]
        self.play(*[Create(x) for x in xr], run_time=0.7)

        tag1 = bchip("isolated mouse retina", GREY, 22).move_to([-2.4, 3.1, 0])
        self.at("isolated mouse retina")
        self.play(FadeIn(tag1, shift=DOWN * 0.1), run_time=0.5)
        tag2 = bchip("signal from cones only", GREY, 22).move_to([2.2, 3.1, 0])
        self.at("signal came from cones")
        self.play(FadeIn(tag2, shift=DOWN * 0.1), run_time=0.5)

        lb1 = T("control cone", 24, BLUE).move_to([-4.1, y1 + 0.62, 0]).align_to([-4.9, 0, 0], LEFT)
        lb2 = T("knockout cone", 24, RED).move_to([-4.1, y2 + 0.62, 0]).align_to([-4.9, 0, 0], LEFT)
        self.at("compared control cones")
        self.play(FadeIn(lb1), FadeIn(lb2), run_time=0.5)

        bg = T("background light", 22, YELLOW).move_to([L + 1.35, 2.35, 0])
        lt = bar(L, 1.95, 0.5, YELLOW, 0.22)
        self.at("still adapted")
        self.play(FadeIn(bg), FadeIn(lt), run_time=0.4)
        self.play(Transform(lt, bar(L, 1.95, W, YELLOW, 0.22)), Transform(se1, bar(L, y1, 0.5 * W, BLUE)),
                  Transform(se2, bar(L, y2, 0.11 * W, RED)), run_time=0.9)

        b1 = bchip("bath calcium 1.2 mM", ORANGE, 22).move_to([L + 1.9, -2.55, 0])
        self.at("bath calcium")
        self.play(FadeIn(b1, shift=UP * 0.1), run_time=0.5)
        self.at("nanomolar")
        b2 = bchip("bath calcium ≈ 30 nM", ORANGE, 22).move_to(b1)
        self.play(FadeOut(b1), run_time=0.2)
        self.play(FadeIn(b2), Indicate(se2, color=RED, scale_factor=1.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Curve(SpokenScene):
    """log-log plot of S/Sdark against background, drawn from the fit values; I0 and slope marked."""

    def construct(self):
        ax, base = make_plot()
        ctrl = fit_curve(ax, CTRL, BLUE)
        ko = fit_curve(ax, KO, RED)
        form = M("S / Sdark = 1 / (1 + (I / I0)^n)", 22, TEXT).move_to([-1.9, 3.2, 0])
        self.at("Sensitivity is response")
        self.play(FadeIn(base), FadeIn(form), run_time=0.8)

        self.at("It falls")
        self.play(Create(ctrl), run_time=1.6)

        # I0 on the control curve
        x0 = np.log10(CTRL["I0"])
        pt = Dot(ax.c2p(x0, np.log10(0.5)), radius=0.12, color=BLUE)
        hl = DashedLine(ax.c2p(2, np.log10(0.5)), ax.c2p(x0, np.log10(0.5)), color=BLUE, stroke_width=3)
        vl = DashedLine(ax.c2p(x0, np.log10(0.5)), ax.c2p(x0, -3), color=BLUE, stroke_width=3)
        half = T("0.5", 22, BLUE).next_to(ax.c2p(2, np.log10(0.5)), RIGHT, buff=0.12).shift(UP * 0.25)
        i0 = T("I0", 26, BLUE, weight=BOLD).next_to(ax.c2p(x0, -3), UP, buff=0.12).shift(RIGHT * 0.3)
        self.at("is the background that halves")
        self.play(Create(hl), Create(vl), FadeIn(pt, scale=1.5), FadeIn(half), FadeIn(i0), run_time=1.0)

        asy = DashedLine(ax.c2p(4.9, -n_asym(4.9, CTRL)), ax.c2p(6, -n_asym(6, CTRL)), color=BLUE, stroke_width=3)
        sl = T("slope −n", 24, BLUE).move_to(ax.c2p(5.5, -0.35))
        self.at("n is the slope")
        self.play(Create(asy), FadeIn(sl), run_time=0.9)

        # legend
        lg1 = VGroup(T("control cones", 26, BLUE, weight=BOLD), M("I0 = 48,800", 24, BLUE), M("n = 1", 24, BLUE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 1.5, 0]).align_to([3.1, 0, 0], LEFT)
        self.at("Control cones had")
        self.play(FadeIn(lg1, shift=LEFT * 0.1), run_time=0.6)
        self.at("photons per square")
        self.play(Indicate(base[4], color=GREY, scale_factor=1.06), run_time=0.8)

        x1 = np.log10(KO["I0"])
        pt2 = Dot(ax.c2p(x1, np.log10(0.5)), radius=0.12, color=RED)
        vl2 = DashedLine(ax.c2p(x1, np.log10(0.5)), ax.c2p(x1, -3), color=RED, stroke_width=3)
        lg2 = VGroup(T("without the sensors", 26, RED, weight=BOLD), M("I0 = 12,100", 24, RED), M("n = 1.5", 24, RED)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -1.4, 0]).align_to([3.1, 0, 0], LEFT)
        self.at("Cones lacking the sensors")
        self.play(Create(ko), run_time=1.5)
        self.play(Create(vl2), FadeIn(pt2, scale=1.5), FadeIn(lg2, shift=LEFT * 0.1), run_time=0.8)
        asy2 = DashedLine(ax.c2p(5.0, -n_asym(5.0, KO)), ax.c2p(6, -n_asym(6, KO)), color=RED, stroke_width=3)
        sl2 = T("slope −n", 24, RED).move_to(ax.c2p(5.4, -2.85))
        self.at("n of", nth=1)
        self.play(Create(asy2), FadeIn(sl2), run_time=0.7)
        self.finish()


def n_asym(x, p):
    return p["n"] * (x - np.log10(p["I0"]))


# ---------------------------------------------------------------------------------------------
class S05Gap(SpokenScene):
    """the same plot; a vertical line at 48,800 reads 0.500 and 0.110; the knockout needs a 4.55 times stronger flash."""

    def construct(self):
        ax, base = make_plot()
        ctrl = fit_curve(ax, CTRL, BLUE)
        ko = fit_curve(ax, KO, RED)
        x0 = np.log10(CTRL["I0"])
        x1 = np.log10(KO["I0"])
        p1 = ax.c2p(x0, np.log10(0.5))
        pt = Dot(p1, radius=0.12, color=BLUE)
        pt2 = Dot(ax.c2p(x1, np.log10(0.5)), radius=0.12, color=RED)
        vl2 = DashedLine(ax.c2p(x1, np.log10(0.5)), ax.c2p(x1, -3), color=RED, stroke_width=3)
        prep = T("mouse cones, ex vivo, central fit values", 22, GREY).move_to([-1.9, 3.2, 0])
        self.add(base, ctrl, ko, pt, pt2, vl2)

        vline = DashedLine(ax.c2p(x0, 0), ax.c2p(x0, -3), color=YELLOW, stroke_width=4)
        bgl = M("48,800", 24, YELLOW).next_to(ax.c2p(x0, -3), UP, buff=0.1).shift(RIGHT * 0.5)
        head = T("at 48,800\nphotons per µm² per s", 24, YELLOW, line_spacing=0.8).move_to([4.7, 2.7, 0]).align_to([3.1, 0, 0], LEFT)
        self.at("At a background of")
        self.play(Create(vline), FadeIn(bgl), FadeIn(head), run_time=0.9)
        self.at("control cones keep half")
        v1 = VGroup(T("control", 26, BLUE), M("0.500", 28, BLUE, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to([4.7, 1.75, 0]).align_to([3.1, 0, 0], LEFT)
        self.play(Indicate(pt, color=BLUE, scale_factor=1.8), FadeIn(v1), run_time=0.8)

        sK = 0.110
        p2 = ax.c2p(x0, np.log10(sK))
        pk = Dot(p2, radius=0.12, color=RED)
        v2 = VGroup(T("knockout", 26, RED), M("0.110", 28, RED, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to([4.7, 1.2, 0]).align_to([3.1, 0, 0], LEFT)
        self.at("keep about")
        self.play(FadeIn(pk, scale=1.8), FadeIn(v2), run_time=0.8)
        own = T("each against its own\ndark sensitivity", 22, GREY, line_spacing=0.8).move_to([4.7, 0.45, 0]).align_to([3.1, 0, 0], LEFT)
        self.at("measured against its own")
        self.play(FadeIn(own), run_time=0.5)

        gap = VGroup(M("0.500 / 0.110", 24, YELLOW), M("= 4.55 times", 28, YELLOW, weight=BOLD), T("stronger flash needed", 24, YELLOW), T("for the same response size", 22, YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        gap.move_to([4.7, -1.2, 0]).align_to([3.0, 0, 0], LEFT)
        self.at("same size")
        self.play(FadeIn(gap, shift=UP * 0.1), Indicate(pk, color=YELLOW, scale_factor=1.8), run_time=0.9)
        self.at("central fit values")
        self.play(FadeIn(prep), run_time=0.5)
        self.at("So the sensors matter")
        self.play(Indicate(ko, color=RED), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """adaptation has three inputs; the low-calcium bath is not a clamp; the rule."""

    def construct(self):
        ad = bchip("adaptation", GREEN, 30).move_to([5.1, 0.0, 0])
        ci = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=5.2, height=1.6, stroke_color=GREY, stroke_width=4, fill_opacity=0), num_dashes=40).move_to([0.4, 2.0, 0])
        ci_q = T("?", 56, TEXT, weight=BOLD).move_to([-1.3, 2.0, 0])
        ci_t = T("calcium-independent\ncomponent, not named", 22, TEXT, line_spacing=0.8).move_to([1.2, 2.0, 0])
        cd = bchip("a further calcium-dependent mechanism", ORANGE, 22).move_to([0.4, 0.0, 0])
        sn = bchip("GCAPs and recoverin", PURPLE, 24).move_to([0.4, -2.0, 0])
        a1 = DashedLine([3.0, 1.9, 0], [4.4, 0.4, 0], color=GREY, stroke_width=5, dash_length=0.15).add_tip(tip_length=0.2)
        a2 = arr([3.2, 0.0, 0], [3.9, 0.0, 0], ORANGE)
        a3 = arr([2.3, -2.0, 0], [4.4, -0.4, 0], PURPLE)

        self.at("The authors read this")
        self.play(FadeIn(ad), Create(ci), FadeIn(ci_q), FadeIn(ci_t), Create(a1), run_time=1.0)
        self.at("also reported")
        self.play(FadeIn(cd, shift=LEFT * 0.1), GrowArrow(a2), run_time=0.8)

        # the bath
        bath = RoundedRectangle(corner_radius=0.3, width=3.7, height=6.4, stroke_color=ORANGE, stroke_width=3,
                                fill_color=ORANGE, fill_opacity=0.08).move_to([-4.7, 0.0, 0])
        bl = T("low-calcium bath", 22, ORANGE).move_to([-4.7, 2.75, 0])
        cone = cone_cell(GREY, 1.0).move_to([-5.4, 0.25, 0])
        gbox = Rectangle(width=0.6, height=2.2, stroke_color=GREY, stroke_width=3).move_to([-3.55, -0.1, 0])
        gq = T("?", 44, TEXT, weight=BOLD).move_to(gbox)
        self.at("changes the solution")
        self.play(FadeIn(bath), FadeIn(bl), FadeIn(cone), run_time=0.7)
        ginfo = T("calcium inside:", 22, GREY).move_to([-4.7, -2.3, 0])
        nc = T("not held fixed", 22, RED).move_to([-4.7, -2.75, 0])
        self.at("does not clamp")
        self.play(FadeIn(gbox), FadeIn(gq), FadeIn(ginfo), FadeIn(nc), run_time=0.8)
        self.at("no molecule")
        self.play(Indicate(ci_q, color=TEXT, scale_factor=1.3), run_time=0.8)

        self.at("keep this rule")
        self.play(FadeOut(bath), FadeOut(bl), FadeOut(cone), FadeOut(gbox), FadeOut(gq), FadeOut(ginfo), FadeOut(nc), run_time=0.5)
        self.at("contribute")
        self.play(FadeIn(sn, shift=LEFT * 0.1), GrowArrow(a3), run_time=0.8)
        self.play(Indicate(sn, color=PURPLE, scale_factor=1.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "GCAPs and recoverin contribute, and do not account for all of the adaptation."
