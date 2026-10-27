"""Skeletal muscle: power peaks at a middle load  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the muscle (labelled blocks)
  ORANGE = load / force (load blocks, load axis, isometric force)
  YELLOW = speed of shortening (curve, bars, arrows)
  GREEN  = external power (curve, peak)
  RED    = zero / rejected (zero external work, speed zero, the straight-line viscous brake)
  TEAL   = heat (thermopile)
  PURPLE = sarcomere length
  GOLD   = the question mark and the title rule
  GREY   = axes, lever, wall, notes
  Model muscle only: F0 = 100 N, a = 0.25 F0, b = 0.100 m/s (vmax = 0.40 m/s), all made up.
  Everything is a labelled schematic block or a plot computed from Hill's equation: not to scale.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
MUSCLE, LOAD, SPEED, POWER, ZERO, HEAT, LENGTH = BLUE, ORANGE, YELLOW, GREEN, RED, TEAL, PURPLE


# ---------------------------------------------------------------------------------------------
# the model muscle (the lesson's worked problem): F0 = 100 N on the plateau, a/F0 = 0.25, vmax = 0.40 m/s
# ---------------------------------------------------------------------------------------------
BCONST = 0.100            # m/s  (vmax = b F0 / a = 0.40 m/s)
FSTAR = float(np.sqrt(0.25 ** 2 + 0.25) - 0.25)   # best load as a fraction of F0 = 0.309


def vel(F, F0=100.0):
    return BCONST * (F0 - F) / (F + 0.25 * F0)


def pw(F, F0=100.0):
    return F * vel(F, F0)


def f0_at(L):
    """model: plateau to 2.20 um, then a straight line to zero at 3.65 um."""
    return 100.0 if L <= 2.20 else 100.0 * (3.65 - L) / (3.65 - 2.20)


class Plot:
    """A labelled schematic plot: axes, ticks, labels. p(x, y) maps data to the screen."""

    def __init__(self, cx, cy, w, h, xmax, ymax, xticks, yticks, xlabel, ylabel, xmin=0.0, tick=22, lab=24):
        self.w, self.h, self.xmin, self.xmax, self.ymax = w, h, xmin, xmax, ymax
        self.o = np.array([cx - w / 2, cy - h / 2, 0.0])
        xa = Line(self.o, self.o + [w, 0, 0], color=GREY, stroke_width=3)
        ya = Line(self.o, self.o + [0, h, 0], color=GREY, stroke_width=3)
        self.xt, self.yt = {}, {}
        marks = []
        for xv, txt in xticks:
            pt = self.p(xv, 0)
            marks.append(Line(pt + DOWN * 0.08, pt + UP * 0.08, color=GREY, stroke_width=3))
            self.xt[txt] = T(txt, tick, GREY).move_to(pt + DOWN * 0.33)
        for yv, txt in yticks:
            pt = self.p(xmin, yv)
            marks.append(Line(pt + LEFT * 0.08, pt + RIGHT * 0.08, color=GREY, stroke_width=3))
            lab_ = T(txt, tick, GREY)
            lab_.move_to(pt + LEFT * (0.18 + lab_.width / 2))
            self.yt[txt] = lab_
        self.xl = T(xlabel, lab, TEXT).move_to([cx, self.o[1] - 0.85, 0])
        self.yl = T(ylabel, lab, TEXT)
        self.yl.move_to([self.o[0] - 0.2 + self.yl.width / 2, self.o[1] + h + 0.42, 0])
        self.frame = VGroup(xa, ya, *marks)
        self.ticks = VGroup(*self.xt.values(), *self.yt.values())
        self.texts = VGroup(self.ticks, self.xl, self.yl)

    def p(self, x, y):
        return self.o + np.array([(x - self.xmin) / (self.xmax - self.xmin) * self.w, y / self.ymax * self.h, 0.0])

    def curve(self, f, x0, x1, color, width=6, n=90):
        pts = [self.p(x, f(x)) for x in np.linspace(x0, x1, n)]
        m = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
        m.set_points_as_corners(pts)
        return m

    def dot(self, x, y, color, r=0.13):
        return Dot(self.p(x, y), radius=r, color=color)


def vplot(cx, cy, w, h, big=False):
    return Plot(cx, cy, w, h, 105, 0.42, [(0, "0"), (50, "50"), (100, "100")],
                [(0, "0"), (0.2, "0.2"), (0.4, "0.4")], "load F (N)", "speed v (m/s)")


def pplot(cx, cy, w, h, ylabel="power P (W)"):
    return Plot(cx, cy, w, h, 105, 4.2, [(0, "0"), (50, "50"), (100, "100")],
                [(0, "0"), (2, "2"), (4, "4")], "load F (N)", ylabel)


# small-plot geometry shared by scenes 4 to 6
LCX, RCX, PCY, PW, PH = -3.2, 3.7, 0.15, 4.8, 3.8


def bleg(text, size=24, color=GREY):
    """text with an opaque backing."""
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.12, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


class S00Title(TitleCard):
    LESSON = "Skeletal muscle: length, load and speed"
    TITLE = "Power peaks at a middle load"


# ---------------------------------------------------------------------------------------------
def hang(cx, tr, load_w=None, load_label=""):
    """A muscle block hung from a ceiling bar, its length read from tracker tr; an optional load hangs below."""
    def build():
        L = tr.get_value()
        top = 3.25
        ceil = Line([cx - 1.6, 3.3, 0], [cx + 1.6, 3.3, 0], color=GREY, stroke_width=8)
        m = RoundedRectangle(corner_radius=0.18, width=2.1, height=L, stroke_color=MUSCLE, stroke_width=4,
                             fill_color=MUSCLE, fill_opacity=0.3).move_to([cx, top - L / 2, 0])
        parts = [ceil, m, T("muscle", 30, MUSCLE).move_to(m)]
        bot = top - L
        if load_w:
            cord = Line([cx, bot, 0], [cx, bot - 0.5, 0], color=GREY, stroke_width=4)
            box = RoundedRectangle(corner_radius=0.12, width=load_w, height=1.6, stroke_color=LOAD, stroke_width=4,
                                   fill_color=LOAD, fill_opacity=0.35).move_to([cx, bot - 0.5 - 0.8, 0])
            parts += [cord, box, T(load_label, 30, LOAD).move_to(box)]
        else:
            parts += [Dot([cx, bot - 0.1, 0], radius=0.1, color=GREY)]
        return VGroup(*parts)
    return always_redraw(build)


class S01Zero(SpokenScene):
    """no load: fast, zero work; load it cannot move: zero work; where is the power? Hill's question."""

    def construct(self):
        LX, RX = -3.9, 3.9
        trL, trR = ValueTracker(2.4), ValueTracker(2.4)
        left = hang(LX, trL)
        right = hang(RX, trR, load_w=2.6, load_label="load")
        self.at("lifts nothing")
        self.play(FadeIn(left), run_time=0.7)
        cap_l = T("lifts nothing", 26, GREY).move_to([LX, -1.75, 0])
        self.play(FadeIn(cap_l), run_time=0.4)
        self.at("shortens as fast")
        arrow = Arrow([LX + 1.55, 1.3, 0], [LX + 1.55, 2.9, 0], buff=0, color=SPEED, stroke_width=8, tip_length=0.32)
        fast = T("fastest", 28, SPEED).next_to(arrow, RIGHT, buff=0.15)
        self.play(trL.animate.set_value(1.2), GrowArrow(arrow), FadeIn(fast), run_time=1.0)
        self.at("no external work")
        z1 = T("external work: zero", 28, ZERO).move_to([LX, -2.7, 0])
        self.play(FadeIn(z1, shift=UP * 0.1), run_time=0.5)
        self.at("Another muscle holds")
        self.play(FadeIn(right), run_time=0.7)
        cap_r = T("holds a load it cannot move", 24, GREY).move_to([RX, -1.75, 0])
        self.play(FadeIn(cap_r), run_time=0.5)
        self.at("also does no")
        z2 = T("external work: zero", 28, ZERO).move_to([RX, -2.7, 0])
        self.play(FadeIn(z2, shift=UP * 0.1), run_time=0.5)
        self.at("both extremes")
        self.play(Indicate(z1, color=ZERO, scale_factor=1.12), Indicate(z2, color=ZERO, scale_factor=1.12), run_time=1.0)
        self.at("So where does")
        q = T("?", 170, GOLD, font=TITLE_FONT).move_to([0, 0.8, 0])
        qt = T("where is the power?", 26, GOLD).move_to([0, -0.7, 0])
        self.play(FadeIn(q, scale=0.6), FadeIn(qt), run_time=0.7)
        self.at("Hill asked")
        who = T("A. V. Hill, 1938", 32, GOLD).move_to([0, 1.1, 0])
        ask = T("What sets how fast an activated muscle shortens?", 36, font=TITLE_FONT)
        fit(ask, max_w=11.8)
        ask.move_to([0, -0.2, 0])
        self.play(FadeOut(VGroup(left, right, cap_l, cap_r, z1, z2, q, qt, arrow, fast)), run_time=0.5)
        self.play(FadeIn(who), Write(ask), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Hill(SpokenScene):
    """frog sartorius on a lever with a series of loads; heat recorded; heavier load, slower shortening."""

    def construct(self):
        P0 = np.array([-4.6, 0.0, 0.0])
        h = ValueTracker(0.0)            # rise of the muscle's attachment on the lever
        state = {"w": 1.5, "name": "light"}
        ARM_M, ARM_L = 3.0, 6.0
        xa = P0[0] + ARM_M

        def theta():
            return float(np.arcsin(np.clip(h.get_value() / ARM_M, -0.9, 0.9)))

        def build():
            th = theta()
            d = np.array([np.cos(th), np.sin(th), 0.0])
            A, E = P0 + ARM_M * d, P0 + ARM_L * d
            ceil = Line([xa - 1.6, 3.3, 0], [xa + 1.6, 3.3, 0], color=GREY, stroke_width=8)
            ht = 3.25 - A[1]
            m = RoundedRectangle(corner_radius=0.18, width=2.1, height=ht, stroke_color=MUSCLE, stroke_width=4,
                                 fill_color=MUSCLE, fill_opacity=0.3).move_to([xa, 3.25 - ht / 2, 0])
            lever = Line(P0, E, color=GREY, stroke_width=9)
            piv = Triangle(color=GREY, fill_color=GREY, fill_opacity=0.6, stroke_width=2).scale(0.3).move_to(P0 + DOWN * 0.3)
            cord = Line(E, E + DOWN * 0.3, color=GREY, stroke_width=4)
            box = RoundedRectangle(corner_radius=0.12, width=state["w"], height=1.6, stroke_color=LOAD, stroke_width=4,
                                   fill_color=LOAD, fill_opacity=0.35).move_to(E + DOWN * (0.3 + 0.8))
            lbl = T(state["name"], 26, LOAD).move_to(box)
            return VGroup(ceil, m, T("muscle", 30, MUSCLE).move_to(m), lever, piv, cord, box, lbl)

        rig = always_redraw(build)
        head = T("schematic: isolated frog sartorius, about 0 °C", 28, GREY).move_to([-1.7, -3.2, 0])
        self.play(FadeIn(rig), FadeIn(head), run_time=0.8)
        self.at("each muscle")
        tet = T("tetanized", 26, MUSCLE).move_to([xa, 3.7, 0])
        self.play(FadeIn(tet), Indicate(rig, color=MUSCLE, scale_factor=1.02), run_time=0.8)
        self.at("let it shorten")
        self.play(h.animate.set_value(1.0), run_time=0.7, rate_func=linear)
        self.play(h.animate.set_value(0.0), run_time=0.2)
        state.update(w=2.0, name="heavier")
        self.at("series of loads")
        self.play(h.animate.set_value(0.42), run_time=0.7, rate_func=linear)
        self.play(h.animate.set_value(0.0), run_time=0.2)
        state.update(w=2.5, name="heaviest")
        self.at("on a lever")
        self.play(h.animate.set_value(0.15), run_time=0.7, rate_func=linear)
        lev = T("lever", 26, GREY).move_to([P0[0] + 0.9, -0.75, 0])
        self.play(FadeIn(lev), run_time=0.3)
        self.at("thermopile recorded")
        th_chip = chip("thermopile", HEAT, 26).move_to([-5.2, 2.5, 0])
        hline = DashedLine(th_chip.get_right(), [xa - 1.1, 2.5, 0], color=HEAT, stroke_width=4)
        heat = T("heat", 24, HEAT).next_to(hline, UP, buff=0.1)
        self.play(FadeIn(th_chip), Create(hline), FadeIn(heat), run_time=0.8)
        self.at("read the speed")
        v10, v40, v70 = vel(10.0), vel(40.0), vel(70.0)
        sc = 2.6 / v10
        rows = [("light", v10, 1.3), ("heavier", v40, 0.1), ("heaviest", v70, -1.1)]
        ph = T("speed of shortening", 28, SPEED).move_to([4.5, 2.5, 0])
        grp = [ph]
        bars = []
        for name, v, y in rows:
            lab = T(name, 24, LOAD).move_to([3.2 + 0.0, y + 0.5, 0])
            lab.align_to([3.2, 0, 0], LEFT)
            bar = Rectangle(width=max(v * sc, 0.05), height=0.4, stroke_width=0, fill_color=SPEED, fill_opacity=0.95)
            bar.move_to([3.2 + bar.width / 2, y, 0])
            grp += [lab]
            bars.append(bar)
        self.play(FadeIn(ph), *[FadeIn(g) for g in grp[1:]], run_time=0.5)
        self.play(*[GrowFromEdge(b, LEFT) for b in bars], run_time=0.9)
        self.at("not from the total")
        tot1 = T("not from the total", 24, ZERO)
        tot2 = T("distance shortened", 24, GREY)
        tot = VGroup(tot1, tot2).arrange(DOWN, buff=0.1).move_to([4.6, -2.4, 0])
        self.play(FadeIn(tot), run_time=0.5)
        self.at("Heavier loads")
        self.play(Indicate(VGroup(*bars), color=SPEED, scale_factor=1.04), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
def big_plot():
    p = Plot(0.2, 0.1, 8.6, 4.2, 105, 0.42, [(0, "0"), (50, "50"), (100, "100")],
             [(0, "0"), (0.2, "0.2"), (0.4, "0.4")], "load F (N)", "speed v (m/s)")
    p.yl.shift(UP * 0.22)
    return p


class S03Curve(SpokenScene):
    """speed against load: hyperbola, not a straight line, for the model muscle."""

    def construct(self):
        pl = big_plot()
        shown = VGroup(pl.xt["0"], pl.xt["50"], pl.yt["0"], pl.yt["0.2"])
        head = T("Model muscle: made-up values, not measured human values", 26, TEXT).move_to([0, 3.35, 0])
        fit(head, max_w=12.2)
        eq = M("v = b (F0 - F) / (F + a),   a = 25 N,  b = 0.100 m/s", 22, GREY).move_to([0.2, -3.45, 0])
        self.play(Create(pl.frame), FadeIn(pl.xl), FadeIn(pl.yl), FadeIn(shown), FadeIn(head), FadeIn(eq), run_time=1.0)
        hyper = pl.curve(vel, 0, 100, SPEED)
        legend_x = pl.p(24, 0)[0]
        lg1 = Line([legend_x, 1.75, 0], [legend_x + 0.7, 1.75, 0], color=SPEED, stroke_width=7)
        lt1 = T("rectangular hyperbola", 24, SPEED).next_to(lg1, RIGHT, buff=0.2)
        self.at("rectangular hyperbola")
        self.play(Create(hyper), FadeIn(lg1), FadeIn(lt1), run_time=1.8)
        line = DashedLine(pl.p(0, 0.4), pl.p(100, 0), color=ZERO, stroke_width=5)
        lg2 = DashedLine([legend_x, 1.2, 0], [legend_x + 0.7, 1.2, 0], color=ZERO, stroke_width=5)
        lt2 = T("straight line", 24, ZERO).next_to(lg2, RIGHT, buff=0.2)
        self.at("not along a straight")
        self.play(Create(line), FadeIn(lg2), FadeIn(lt2), run_time=1.2)
        lt2b = T("viscous brake: straight line", 24, ZERO).next_to(lg2, RIGHT, buff=0.2)
        self.at("would give a straight")
        self.play(Transform(lt2, lt2b), run_time=0.5)
        mid = pl.p(50, 0.2)
        x1 = Line(mid + UL * 0.3, mid + DR * 0.3, color=ZERO, stroke_width=8)
        x2 = Line(mid + UR * 0.3, mid + DL * 0.3, color=ZERO, stroke_width=8)
        self.at("ruled out")
        ro = T("ruled out", 26, ZERO).move_to(mid + RIGHT * 0.5 + UP * 0.65)
        self.play(Create(x1), Create(x2), FadeIn(ro), run_time=0.5)
        self.at("isometric force")
        vl = DashedLine(pl.p(100, 0), pl.p(100, 0.42), color=LOAD, stroke_width=4)
        f0l = T("F0 = 100 N", 26, LOAD).move_to(pl.p(100, 0.2) + LEFT * 1.1)
        self.play(FadeIn(pl.xt["100"]), Create(vl), FadeIn(f0l), run_time=0.8)
        self.at("no load")
        d0 = pl.dot(0, 0.4, SPEED)
        l0 = T("no load: 0.40 m/s", 26, SPEED).move_to(pl.p(0, 0.4) + UP * 0.45 + RIGHT * 1.6)
        self.play(FadeIn(pl.yt["0.4"]), FadeIn(d0, scale=1.6), FadeIn(l0), run_time=0.8)
        self.at("does not shorten")
        d1 = pl.dot(100, 0, ZERO)
        l1 = T("speed zero", 26, ZERO).move_to(pl.p(100, 0) + UP * 0.55 + RIGHT * 0.95)
        self.play(FadeIn(d1, scale=1.6), FadeIn(l1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Power(SpokenScene):
    """P = F x v: zero at no load, zero at the isometric load; external power, not ATP."""

    def construct(self):
        big = big_plot()
        bigcurve = big.curve(vel, 0, 100, SPEED)
        bigbits = VGroup(big.xl, big.yl, big.ticks)
        bigdots = VGroup(big.dot(0, 0.4, SPEED), big.dot(100, 0, ZERO))
        self.add(big.frame, bigbits, bigcurve, bigdots)
        vs = vplot(LCX, PCY, PW, PH)
        ps = pplot(RCX, PCY, PW, PH)
        vcurve = vs.curve(vel, 0, 100, SPEED)
        pcurve_full = ps.curve(pw, 0, 100, POWER)
        banner = T("power = force × speed", 32, POWER).move_to([0, 3.3, 0])
        self.at("Power is force times")
        self.play(ReplacementTransform(big.frame, vs.frame), ReplacementTransform(bigcurve, vcurve),
                  FadeOut(bigbits), FadeOut(bigdots), FadeIn(vs.texts), run_time=1.3)
        self.play(Create(ps.frame), FadeIn(ps.texts), FadeIn(banner), run_time=1.0)

        Ft = ValueTracker(0.0)
        gv = always_redraw(lambda: VGroup(
            DashedLine(vs.p(Ft.get_value(), 0), vs.p(Ft.get_value(), vel(Ft.get_value())), color=LOAD, stroke_width=3),
            vs.dot(Ft.get_value(), vel(Ft.get_value()), LOAD)))
        gp = always_redraw(lambda: VGroup(
            DashedLine(ps.p(Ft.get_value(), 0), ps.p(Ft.get_value(), pw(Ft.get_value())), color=LOAD, stroke_width=3),
            ps.dot(Ft.get_value(), pw(Ft.get_value()), LOAD)))
        trace = always_redraw(lambda: ps.curve(pw, 0, max(Ft.get_value(), 0.01), POWER, n=60))
        formula = M("no load:  0 N × 0.40 m/s = 0 W", 26, TEXT).move_to([0, -3.3, 0])
        self.at("With no load")
        self.play(FadeIn(gv), FadeIn(gp), FadeIn(formula), run_time=0.6)
        self.add(trace)
        self.at("When the load equals")
        self.play(FadeOut(formula), run_time=0.2)
        self.play(Ft.animate.set_value(100.0), run_time=3.2, rate_func=linear)
        formula = M("load = 100 N:  100 N × 0 m/s = 0 W", 26, TEXT).move_to([0, -3.3, 0])
        self.at("zero again")
        self.play(FadeIn(formula), run_time=0.5)
        self.at("external power")
        newl = T("external power P (W)", 24, TEXT)
        newl.move_to([ps.o[0] - 0.2 + newl.width / 2, ps.o[1] + ps.h + 0.42, 0])
        self.play(Transform(ps.yl, newl), run_time=0.5)
        self.at("An isometric muscle")
        iso = T("isometric: no external work, yet ATP is still split", 26, TEXT).move_to([0, -3.3, 0])
        self.play(FadeOut(formula), FadeIn(iso), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Peak(SpokenScene):
    """the peak: 0.31 F0 = 30.9 N, 0.1236 m/s, 3.82 W."""

    def construct(self):
        vs = vplot(LCX, PCY, PW, PH)
        ps = pplot(RCX, PCY, PW, PH, "external power P (W)")
        vcurve = vs.curve(vel, 0, 100, SPEED)
        pcurve = ps.curve(pw, 0, 100, POWER)
        banner = T("power = force × speed", 32, POWER).move_to([0, 3.3, 0])
        Ft = ValueTracker(100.0)
        gv = always_redraw(lambda: VGroup(
            DashedLine(vs.p(Ft.get_value(), 0), vs.p(Ft.get_value(), vel(Ft.get_value())), color=LOAD, stroke_width=3),
            vs.dot(Ft.get_value(), vel(Ft.get_value()), LOAD)))
        gp = always_redraw(lambda: VGroup(
            DashedLine(ps.p(Ft.get_value(), 0), ps.p(Ft.get_value(), pw(Ft.get_value())), color=LOAD, stroke_width=3),
            ps.dot(Ft.get_value(), pw(Ft.get_value()), LOAD)))
        self.add(vs.frame, vs.texts, ps.frame, ps.texts, vcurve, pcurve, banner, gv, gp)
        FS = 100 * FSTAR
        self.at("between power")
        self.play(Ft.animate.set_value(FS), run_time=0.8)
        ring = Circle(radius=0.28, color=POWER, stroke_width=6).move_to(ps.p(FS, pw(FS)))
        pk = T("peak power", 26, POWER).move_to(ps.p(76, 3.9))
        self.at("Power peaks")
        self.play(Create(ring), FadeIn(pk), run_time=0.7)
        quarter = M("a / F0 = 0.25  (model value)", 28, TEXT).move_to([0, 3.3, 0])
        self.at("constant")
        self.play(Transform(banner, quarter), run_time=0.6)
        near = M("peak at about 0.31 F0", 28, TEXT).move_to([0, 3.3, 0])
        self.at("peak sits near")
        self.play(Transform(banner, near), run_time=0.6)
        self.at("a load of")
        ld = T("30.9 N", 22, LOAD).move_to(ps.p(FS, 0) + DOWN * 0.33)
        self.play(FadeIn(ld), run_time=0.5)
        self.at("speed there")
        sv = T("0.1236 m/s", 24, SPEED).move_to(vs.p(FS, vel(FS)) + UP * 0.5 + RIGHT * 1.05)
        self.play(FadeIn(sv), run_time=0.5)
        self.at("peak power is")
        pv = T("3.82 W", 26, POWER).move_to(ps.p(76, 3.35))
        self.play(FadeIn(pv), run_time=0.5)
        self.at("exact fraction")
        note = T("the fraction depends on the curvature", 26, GREY).move_to([0, -3.3, 0])
        self.play(FadeIn(note), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Stretch(SpokenScene):
    """stretch to 3.00 um: F0 = 44.83 N, peak power x 0.448; limits; the rule."""

    def construct(self):
        ps = pplot(RCX, PCY, PW, PH, "external power P (W)")
        K = ValueTracker(100.0)
        pcurve = always_redraw(lambda: ps.curve(lambda F: pw(F, K.get_value()), 0, K.get_value(), POWER))
        pring = always_redraw(lambda: Circle(radius=0.26, color=POWER, stroke_width=6).move_to(
            ps.p(FSTAR * K.get_value(), pw(FSTAR * K.get_value(), K.get_value()))))
        old_lab = T("3.82 W", 24, POWER).move_to(ps.p(76, 3.55))
        self.add(ps.frame, ps.texts, pcurve, pring, old_lab)

        ls = Plot(LCX, PCY, PW, PH, 3.8, 105, [(2.2, "2.2"), (3.0, "3.0"), (3.65, "3.65")], [(0, "0"), (50, "50"), (100, "100")],
                  "sarcomere length (µm)", "isometric force (N)", xmin=2.0)
        # tick labels appear on their cues
        shown_x = {k: v for k, v in ls.xt.items()}
        base = VGroup(ls.yt["0"], ls.yt["50"], ls.yt["100"], ls.xl, ls.yl)
        self.at("Now stretch")
        self.play(Create(ls.frame), FadeIn(base), run_time=1.0)
        limb = VMobject(stroke_color=LOAD, stroke_width=6, fill_opacity=0)
        limb.set_points_as_corners([ls.p(2.05, 100), ls.p(2.2, 100), ls.p(3.65, 0)])
        self.at("straight line")
        self.play(Create(limb), run_time=1.1)
        self.at("full force at")
        d22 = ls.dot(2.2, 100, LOAD)
        self.play(FadeIn(d22, scale=1.6), FadeIn(ls.xt["2.2"]), run_time=0.5)
        self.at("zero at")
        d365 = ls.dot(3.65, 0, LOAD)
        self.play(FadeIn(d365, scale=1.6), FadeIn(ls.xt["3.65"]), run_time=0.5)
        Lt = ValueTracker(2.2)
        mark = always_redraw(lambda: Dot(ls.p(Lt.get_value(), f0_at(Lt.get_value())), radius=0.17, color=LENGTH))
        drop = always_redraw(lambda: DashedLine(ls.p(Lt.get_value(), 0), ls.p(Lt.get_value(), f0_at(Lt.get_value())),
                                                color=LENGTH, stroke_width=4))
        readout = always_redraw(lambda: M(f"F0 = {f0_at(Lt.get_value()):.2f} N" if Lt.get_value() > 2.2 else "F0 = 100 N",
                                          24, LOAD).move_to(ls.p(3.2, 93)))
        self.add(drop, mark)
        ghost = ps.curve(pw, 0, 100, POWER, width=3)
        ghost.set_stroke(opacity=0.35)
        self.at("isometric force is")
        self.add(ghost)
        self.add(readout)
        self.play(FadeIn(ls.xt["3.0"]), Lt.animate.set_value(3.0), run_time=1.8)
        self.at("peak power falls")
        n_lab = T("1.71 W", 24, POWER)
        n_lab.move_to(ps.p(f0_at(3.0) * FSTAR, pw(f0_at(3.0) * FSTAR, f0_at(3.0))) + RIGHT * 0.95 + UP * 0.35)
        self.play(K.animate.set_value(f0_at(3.0)), FadeIn(n_lab), run_time=1.0)
        fac = M("peak power × 0.448", 26, TEXT).move_to([0, -3.3, 0])
        self.at("same factor")
        self.play(FadeIn(fac), run_time=0.5)
        spd = T("speed at peak power: 0.309 of top speed, unchanged", 26, SPEED).move_to([0, -3.3, 0])
        self.at("speed at peak power")
        self.play(FadeOut(fac), FadeIn(spd), run_time=0.5)
        c1 = chip("no molecular mechanism", GREY, 24).move_to([-3.2, -3.3, 0])
        c2 = chip("frog values at about 0 °C", GREY, 24).move_to([3.7, -3.3, 0])
        self.at("Hill's rule gives")
        self.play(FadeOut(spd), FadeIn(c1), run_time=0.5)
        self.at("its constants")
        self.play(FadeIn(c2), run_time=0.5)
        self.at("External power is")
        self.play(FadeOut(VGroup(c1, c2, ghost, old_lab)), run_time=0.7)
        rule = T("external power is zero at both extremes and peaks at a middle load", 28, TEXT).move_to([0, 3.4, 0])
        fit(rule, max_w=12.2)
        self.play(FadeIn(rule), run_time=0.5)
        e0 = Dot(ps.p(0, 0), radius=0.12, color=ZERO)
        e1 = Dot(ps.p(f0_at(3.0), 0), radius=0.12, color=ZERO)
        self.at("zero at both")
        self.play(FadeIn(e0, scale=1.8), FadeIn(e1, scale=1.8), run_time=0.6)
        self.at("peaks at a middle")
        self.play(Indicate(pring, color=POWER, scale_factor=1.3), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "External power: zero at both extremes, peak at a middle load."
