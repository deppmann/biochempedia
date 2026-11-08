"""Population growth: growth falls as numbers rise  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the population, N (bars, the logistic population curve's start)
  YELLOW = per capita growth rate, r (and what new individuals add)
  ORANGE = the exponential model
  GREEN  = the logistic model
  TEAL   = total growth, dN/dt
  GOLD   = K, the carrying capacity and equilibrium
  RED    = a wrong expectation / the time-lag sketch that overshoots
  GREY   = axes, structure, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
R, K, N0 = 0.2, 1000.0, 100.0


def logi(t, n0=N0):
    return K / (1 + (K / n0 - 1) * np.exp(-R * t))


def expo(t):
    return N0 * np.exp(R * t)


class Plot:
    """Hand-built axes (no LaTeX). box = (x0, x1, y0, y1) in scene units; xr, yr = data ranges."""

    def __init__(self, box, xr, yr, xticks, yticks, xlabel, ylabel, ysize=22):
        self.x0, self.x1, self.y0, self.y1 = box
        self.xr, self.yr = xr, yr
        self.parts = VGroup()
        self.parts.add(Line([self.x0, self.y0, 0], [self.x1, self.y0, 0], color=GREY, stroke_width=3))
        self.parts.add(Line([self.x0, self.y0, 0], [self.x0, self.y1, 0], color=GREY, stroke_width=3))
        for v, lab in xticks:
            p = self.pt(v, yr[0])
            self.parts.add(Line(p, p + DOWN * 0.1, color=GREY, stroke_width=3))
            self.parts.add(T(lab, 22, GREY).next_to(p, DOWN, buff=0.14))
        for v, lab in yticks:
            p = self.pt(xr[0], v)
            self.parts.add(Line(p, p + LEFT * 0.1, color=GREY, stroke_width=3))
            self.parts.add(T(lab, 22, GREY).next_to(p, LEFT, buff=0.14))
        self.xl = T(xlabel, 24, GREY).next_to(Line([self.x0, self.y0, 0], [self.x1, self.y0, 0]), DOWN, buff=0.55)
        self.yl = T(ylabel, 24, GREY)
        self.yl.move_to([self.x0, self.y1 + 0.35, 0])
        self.yl.shift(RIGHT * (self.yl.width / 2 - 0.3))
        self.parts.add(self.xl, self.yl)

    def pt(self, x, y):
        fx = (x - self.xr[0]) / (self.xr[1] - self.xr[0])
        fy = (y - self.yr[0]) / (self.yr[1] - self.yr[0])
        return np.array([self.x0 + fx * (self.x1 - self.x0), self.y0 + fy * (self.y1 - self.y0), 0.0])

    def curve(self, fn, x_from, x_to, color, n=160, ymax=None, w=6):
        xs = np.linspace(x_from, x_to, n)
        pts = []
        for x in xs:
            y = fn(x)
            if ymax is not None and y > ymax:
                y = ymax
            pts.append(self.pt(x, y))
        m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
        m.set_points_as_corners(pts)
        return m


def tag_sketch(pos=(-4.5, -3.2, 0)):
    return T("in this sketch", 24, GREY).move_to(list(pos))


class Timed(SpokenScene):
    def gap(self, phrase, lead=0.25, lo=0.4, nth=0):
        """seconds from now until just before the narrator says `phrase` (never below lo)."""
        return max(lo, self.t_of(phrase, nth) - lead - self.elapsed())


class S00Title(TitleCard):
    LESSON = "Population growth and regulation"
    TITLE = "Growth falls as numbers rise"


# ---------------------------------------------------------------------------------------------
class S01Compound(Timed):
    """100 -> expected 300 (crossed) vs 739; the part above 300 is what new individuals add."""

    def construct(self):
        base = -2.55
        sc = 4.5 / 739.0
        head = chip("invented population  ·  r = 0.2 per day", YELLOW, size=26).to_edge(UP, buff=0.35)
        axis = Line([-6.0, base, 0], [6.0, base, 0], color=GREY, stroke_width=3)
        bw = 1.9
        xs = [-3.9, 0.0, 3.9]

        def bar(x, v, color, op=0.55):
            return Rectangle(width=bw, height=max(v * sc, 0.01), stroke_color=color, stroke_width=3,
                             fill_color=color, fill_opacity=op).move_to([x, base + v * sc / 2, 0])

        self.at("invented population")
        self.play(FadeIn(head, shift=DOWN * 0.1), Create(axis), run_time=0.7)
        b0 = bar(xs[0], 100, BLUE)
        l0 = T("day 0", 26, GREY).move_to([xs[0], base - 0.4, 0])
        v0 = M("100", 30, BLUE).next_to(b0, UP, buff=0.12)
        unit = T("individuals", 24, BLUE).next_to(v0, UP, buff=0.05)
        self.at("individuals with a per")
        self.play(GrowFromEdge(b0, DOWN), FadeIn(l0), run_time=0.6)
        self.play(FadeIn(v0), FadeIn(unit), run_time=0.3)

        # ten days pass
        arrow10 = Arrow([xs[0] + 1.1, 0.6, 0], [xs[1] - 1.1, 0.6, 0], color=GREY, buff=0.05, stroke_width=5)
        t10 = T("10 days", 28, GREY).next_to(arrow10, UP, buff=0.15)
        self.at("After")
        self.play(GrowArrow(arrow10), FadeIn(t10), run_time=0.8)

        # the guess: three hundred
        gb = Rectangle(width=bw, height=300 * sc, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([xs[1], base + 300 * sc / 2, 0])
        gb = DashedVMobject(gb, num_dashes=40)
        gl = T("day 10", 26, GREY).move_to([xs[1], base - 0.4, 0])
        gt = M("300?", 30, GREY).next_to(gb, UP, buff=0.12)
        gsub = T("you might expect", 24, GREY).move_to([xs[1], base - 0.85, 0])
        self.at("might expect")
        self.play(Create(gb), FadeIn(gl), FadeIn(gt), FadeIn(gsub), run_time=0.9)

        # the real bar
        rl = T("day 10", 26, GREY).move_to([xs[2], base - 0.4, 0])
        rsub = T("if nothing stops it", 24, ORANGE).move_to([xs[2], base - 0.85, 0])
        lower = bar(xs[2], 300, BLUE)
        extra = Rectangle(width=bw, height=439 * sc, stroke_color=ORANGE, stroke_width=3,
                          fill_color=ORANGE, fill_opacity=0.55).move_to([xs[2], base + 300 * sc + 439 * sc / 2, 0])
        self.at("nothing stops it")
        self.play(FadeIn(rl), FadeIn(rsub), run_time=0.3)
        self.play(GrowFromEdge(lower, DOWN), run_time=0.9)
        # cross out the guess when the real bar passes it
        cross = VGroup(Line(gb.get_corner(UL), gb.get_corner(DR), color=RED, stroke_width=6),
                       Line(gb.get_corner(UR), gb.get_corner(DL), color=RED, stroke_width=6))
        self.play(GrowFromEdge(extra, DOWN), Create(cross), run_time=1.0)
        v2 = M("739", 34, ORANGE).next_to(extra, UP, buff=0.12)
        self.play(FadeIn(v2), run_time=0.4)

        self.at("Growth compounds")
        self.play(Indicate(extra, color=ORANGE, scale_factor=1.04), run_time=0.9)
        lab = T("more than\nstraight-line growth (300)", 24, ORANGE, line_spacing=0.9)
        lab.move_to([0.8, 1.3, 0])
        arrow = Arrow(lab.get_right() + RIGHT * 0.05, [xs[2] - bw / 2 - 0.05, 1.2, 0], color=ORANGE, buff=0.1, stroke_width=5)
        self.at("starts adding")
        self.play(FadeIn(lab), GrowArrow(arrow), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Double(Timed):
    """dN/dt = rN: exponential curve and equal doubling intervals."""

    def construct(self):
        pl = Plot((-5.3, 5.5, -2.3, 2.1), (0, 10), (0, 800), [(0, "0"), (5, "5"), (10, "10")],
                  [(0, "0"), (400, "400"), (800, "800")], "time (days)", "N (individuals)")
        self.add(pl.parts)
        sk = tag_sketch()
        n_chip = chip("N = number of individuals", BLUE, size=26)
        r_chip = chip("r = 0.2 per day", YELLOW, size=26)
        eq = chip("dN/dt = rN", ORANGE, size=28)
        top = VGroup(n_chip, r_chip).arrange(RIGHT, buff=0.5).move_to([0.7, 3.0, 0])
        self.at("number of individuals")
        self.play(FadeIn(n_chip, shift=DOWN * 0.1), Indicate(pl.yl, color=BLUE), run_time=0.7)
        self.at("per capita rate")
        self.play(FadeIn(r_chip, shift=DOWN * 0.1), run_time=0.6)
        eq.move_to(top.get_center())
        self.at("Growth each day")
        self.play(FadeOut(top), run_time=0.3)
        self.play(FadeIn(eq, scale=0.9), FadeIn(sk), run_time=0.5)
        cur = pl.curve(expo, 0, 10, ORANGE)
        self.play(Create(cur), run_time=self.gap("constant doubling time", lo=1.0) - 0.4, rate_func=linear)
        end = Dot(pl.pt(10, expo(10)), color=ORANGE, radius=0.1)
        self.play(FadeIn(end), run_time=0.2)

        # doubling marks: equal time steps
        td = np.log(2) / R
        self.at("constant doubling time")
        marks = VGroup()
        for i in range(0, 3):
            t = td * i
            p = pl.pt(t, expo(t))
            marks.add(DashedLine(pl.pt(t, 0), p, color=GREY, stroke_width=3))
            marks.add(Dot(p, color=ORANGE, radius=0.11))
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15), run_time=1.5)
        br = VGroup()
        for i in range(2):
            a, b = pl.pt(td * i, 0), pl.pt(td * (i + 1), 0)
            y = pl.y0 - 0.0
            seg = Line(a + UP * 0.35, b + UP * 0.35, color=TEAL, stroke_width=5)
            br.add(seg, Line(seg.get_start() + DOWN * 0.1, seg.get_start() + UP * 0.1, color=TEAL, stroke_width=5),
                   Line(seg.get_end() + DOWN * 0.1, seg.get_end() + UP * 0.1, color=TEAL, stroke_width=5))
        self.play(Create(br), run_time=0.8)
        self.at("Here it is about")
        lab = T("doubling time  ln 2 / r  =  3.47 days", 26, TEAL).move_to([-1.9, 1.35, 0])
        bg = Rectangle(width=lab.width + 0.3, height=lab.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(lab)
        self.play(FadeIn(bg), FadeIn(lab), run_time=0.7)
        self.at("whether the population holds")
        sub = T("at 100 or at 100,000", 26, TEAL).next_to(lab, DOWN, buff=0.25)
        sbg = Rectangle(width=sub.width + 0.3, height=sub.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(sub)
        self.play(FadeIn(sbg), FadeIn(sub), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Brake(Timed):
    """per capita rate: flat at r, then a straight line falling to zero at K."""

    def construct(self):
        pl = Plot((-5.0, 5.4, -2.2, 1.9), (0, 1000), (0, 0.2), [(0, "0"), (500, "500"), (1000, "1,000")],
                  [(0, "0"), (0.1, "0.1"), (0.2, "0.2")], "N (individuals)", "per capita rate (per day)")
        sk = tag_sketch()
        self.add(pl.parts)
        flat = pl.curve(lambda n: 0.2, 0, 1000, YELLOW, n=2)
        flat_lbl = T("exponential: r stays 0.2", 26, ORANGE).move_to([1.5, pl.pt(0, 0.2)[1] + 0.45, 0])
        self.at("Real populations meet")
        self.play(Create(flat), FadeIn(flat_lbl), FadeIn(sk), run_time=1.2)
        # crowd of dots: more individuals as N rises
        dot = Dot(pl.pt(30, 0.2), color=BLUE, radius=0.14)
        falling = pl.curve(lambda n: R * (1 - n / K), 0, 1000, YELLOW, n=2)
        self.at("less food")
        self.play(FadeIn(dot), run_time=0.3)
        self.play(FadeOut(flat_lbl), run_time=0.3)
        self.at("births fall")
        eqn = chip("(1/N) dN/dt = r (1 − N/K)", YELLOW, size=28).move_to([1.2, 2.95, 0])
        self.play(Transform(flat, falling), FadeIn(eqn, shift=DOWN * 0.1), run_time=self.gap("straight line", lead=0.6, lo=1.6))
        self.at("straight line")
        self.play(dot.animate.move_to(pl.pt(500, 0.1)), run_time=self.gap("near zero", lo=0.8), rate_func=smooth)
        self.at("near zero")
        self.play(dot.animate.move_to(pl.pt(30, R * (1 - 0.03))), run_time=0.7)
        rl = M("r", 30, YELLOW).move_to(pl.pt(30, 0.2) + RIGHT * 0.5 + DOWN * 0.4)
        self.play(FadeIn(rl), run_time=0.3)
        self.at("zero at")
        self.play(dot.animate.move_to(pl.pt(1000, 0)), run_time=self.gap("carrying capacity", lo=1.0), rate_func=smooth)
        kmark = DashedLine(pl.pt(1000, 0), pl.pt(1000, 0.2), color=GOLD, stroke_width=4)
        self.at("carrying capacity")
        klab = chip("K = carrying capacity", GOLD, size=26)
        klab.move_to([2.5, 0.9, 0])
        self.play(Create(kmark), FadeIn(klab), run_time=0.8)
        ksub = T("1,000 in the invented example", 24, GOLD).next_to(klab, DOWN, buff=0.2)
        self.play(FadeIn(ksub), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Peak(Timed):
    """total growth = per capita rate x N, peaks at K/2 (50 per day)."""

    def construct(self):
        L = Plot((-5.5, -0.9, -1.75, 1.75), (0, 1000), (0, 0.2), [(0, "0"), (500, "500"), (1000, "1,000")],
                 [(0, "0"), (0.2, "0.2")], "N", "per capita rate")
        Rp = Plot((1.4, 6.1, -1.75, 1.75), (0, 1000), (0, 55), [(0, "0"), (500, "500"), (1000, "1,000")],
                  [(0, "0"), (50, "50")], "N", "total growth (individuals per day)")
        self.add(L.parts)
        self.add(L.curve(lambda n: R * (1 - n / K), 0, 1000, YELLOW, n=2))
        sk = tag_sketch([-4.0, 2.95, 0])
        tg = chip("total growth = rate × N", TEAL, size=28).move_to([2.2, 2.95, 0])
        self.add(Rp.parts)
        nt = ValueTracker(0)

        def lp():
            n = nt.get_value()
            return L.pt(n, R * (1 - n / K))

        def rp():
            n = nt.get_value()
            return Rp.pt(n, R * n * (1 - n / K))

        ldot = always_redraw(lambda: Dot(lp(), color=BLUE, radius=0.12))
        rdot = always_redraw(lambda: Dot(rp(), color=TEAL, radius=0.12))
        link = always_redraw(lambda: DashedLine(lp(), rp(), color=GREY, stroke_width=2))
        trace = always_redraw(lambda: self._trace(Rp, nt.get_value()))
        self.at("Total growth")
        self.play(FadeIn(tg, shift=DOWN * 0.1), FadeIn(sk), FadeIn(ldot), FadeIn(rdot), FadeIn(link), run_time=0.8)
        self.add(trace)
        self.at("per capita rate")
        self.play(Indicate(L.parts[1], color=YELLOW), run_time=0.8)
        self.at("times big N")
        self.play(Indicate(tg, color=TEAL), run_time=0.8)
        self.at("At low")
        few = T("few individuals to multiply", 26, TEAL).move_to([3.5, -3.2, 0])
        self.play(nt.animate.set_value(90), FadeIn(few), run_time=self.gap("Near", lo=0.8), rate_func=smooth)
        self.at("Near")
        self.play(FadeOut(few), run_time=0.2)
        self.play(nt.animate.set_value(950), run_time=self.gap("adds almost nothing", lo=0.8), rate_func=linear)
        low = T("each adds almost nothing", 26, TEAL).move_to([3.5, -3.2, 0])
        self.at("adds almost nothing")
        self.play(FadeIn(low), run_time=0.5)
        self.at("greatest in the middle")
        self.play(FadeOut(low), nt.animate.set_value(500), run_time=min(1.6, self.gap("individuals per day", lo=0.6)), rate_func=smooth)
        pk = chip("K / 2", GOLD, size=26).move_to([5.3, 1.2, 0])
        pkd = DashedLine(Rp.pt(500, 0), Rp.pt(500, 50), color=GOLD, stroke_width=3)
        self.play(Create(pkd), FadeIn(pk), run_time=0.6)
        self.at("individuals per day")
        lab = chip("50 individuals per day", TEAL, size=26).move_to([3.5, -3.2, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), Indicate(rdot, color=TEAL, scale_factor=1.8), run_time=0.9)
        self.finish()

    @staticmethod
    def _trace(P, nmax):
        nmax = max(nmax, 1.0)
        xs = np.linspace(0, nmax, 90)
        m = VMobject(stroke_color=TEAL, stroke_width=6, fill_opacity=0)
        m.set_points_as_corners([P.pt(x, R * x * (1 - x / K)) for x in xs])
        return m


# ---------------------------------------------------------------------------------------------
class S05Part(Timed):
    """both models from 100: day-10 and day-20 values."""

    def construct(self):
        ymax = 1100.0
        pl = Plot((-5.3, 5.3, -2.3, 2.0), (0, 20), (0, ymax), [(0, "0"), (10, "10"), (20, "20")],
                  [(0, "0"), (500, "500"), (1000, "1,000")], "time (days)", "N (individuals)")
        sk = tag_sketch()
        self.add(pl.parts)
        kline = DashedLine(pl.pt(0, K), pl.pt(20, K), color=GOLD, stroke_width=3)
        klab = T("K", 26, GOLD).next_to(pl.pt(20, K), RIGHT, buff=0.12)
        self.add(kline, klab)
        start = Dot(pl.pt(0, N0), color=BLUE, radius=0.12)
        s_lbl = T("100", 24, BLUE).next_to(start, RIGHT, buff=0.12).shift(DOWN * 0.15)
        self.at("run both models")
        self.play(FadeIn(start), FadeIn(s_lbl), FadeIn(sk), run_time=0.7)

        d10 = DashedLine(pl.pt(10, 0), pl.pt(10, ymax), color=GREY, stroke_width=2)
        self.at("At day")
        d10l = T("day 10", 24, GREY).next_to(pl.pt(10, ymax), UP, buff=0.12)
        self.play(Create(d10), FadeIn(d10l), run_time=0.7)
        self.at("exponential model gives")
        ex = pl.curve(expo, 0, 10, ORANGE)
        self.play(Create(ex), run_time=self.gap("logistic model gives", lo=1.0), rate_func=linear)
        e10 = Dot(pl.pt(10, expo(10)), color=ORANGE, radius=0.12)
        e10l = M("739", 28, ORANGE).next_to(e10, LEFT, buff=0.2)
        self.play(FadeIn(e10), FadeIn(e10l), run_time=0.4)
        self.at("logistic model gives")
        lg = pl.curve(logi, 0, 10, GREEN)
        self.play(Create(lg), run_time=self.gap("agree at first", lo=1.0), rate_func=linear)
        g10 = Dot(pl.pt(10, logi(10)), color=GREEN, radius=0.12)
        g10l = M("451", 28, GREEN).next_to(g10, RIGHT, buff=0.2)
        self.play(FadeIn(g10), FadeIn(g10l), run_time=0.4)

        self.at("agree at first")
        early = Ellipse(width=1.6, height=0.7, color=TEAL, stroke_width=4).move_to(pl.pt(1.9, 150))
        agree = T("agree", 26, TEAL).next_to(early, UP, buff=0.2).shift(RIGHT * 0.3)
        self.play(FadeOut(s_lbl), Create(early), FadeIn(agree), run_time=0.7)
        self.at("then part")
        part = T("part", 26, TEAL).move_to(pl.pt(8.0, 520) + RIGHT * 0.05)
        self.play(FadeOut(early), FadeOut(agree), FadeIn(part), run_time=0.7)

        self.at("By day")
        self.play(FadeOut(part), run_time=0.3)
        y_exit = (ymax / expo(1)) if False else None
        t_exit = np.log(ymax / N0) / R
        ex2 = pl.curve(expo, 10, t_exit, ORANGE, ymax=ymax)
        lg2 = pl.curve(logi, 10, 20, GREEN)
        self.play(Create(ex2), Create(lg2), run_time=self.gap("exponential model predicts", lo=1.0, lead=-0.4), rate_func=linear)
        up = Arrow(pl.pt(t_exit, ymax) + DOWN * 0.1, pl.pt(t_exit, ymax) + UP * 0.55, color=ORANGE, buff=0, stroke_width=6)
        e20 = chip("exponential: 5,460 at day 20", ORANGE, size=26).move_to([2.7, 2.95, 0])
        self.at("exponential model predicts")
        self.play(GrowArrow(up), FadeIn(e20), run_time=0.8)
        g20 = Dot(pl.pt(20, logi(20)), color=GREEN, radius=0.12)
        g20l = chip("logistic: about 858", GREEN, size=26).move_to([3.5, -0.6, 0])
        self.at("logistic about")
        self.play(FadeIn(g20), FadeIn(g20l), run_time=0.7)
        self.at("illustrative")
        ill = T("illustrative numbers, not measured for any species", 24, GREY).move_to([1.6, -3.4, 0])
        self.play(FadeIn(ill), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def delayed_logistic(tau=10.0, tmax=60.0, dt=0.02, n_start=100.0):
    n = int(tmax / dt)
    d = int(tau / dt)
    N = np.zeros(n + 1)
    N[: d + 1] = n_start
    for i in range(d, n):
        N[i + 1] = N[i] + dt * R * N[i] * (1 - N[i - d] / K)
    return np.arange(n + 1) * dt, N


class S06Equilibrium(Timed):
    """K as an equilibrium: approached from above and below; a time lag overshoots."""

    def construct(self):
        ymax = 1500.0
        tmax = 40.0
        pl = Plot((-5.3, 5.5, -2.3, 2.0), (0, tmax), (0, ymax), [], [(0, "0"), (1000, "K")], "time", "N")
        sk = tag_sketch()
        self.add(pl.parts)
        kline = DashedLine(pl.pt(0, K), pl.pt(tmax, K), color=GOLD, stroke_width=4)
        self.at("equilibrium")
        self.play(Create(kline), FadeIn(sk), run_time=0.9)
        eq = chip("K: an equilibrium", GOLD, size=28).move_to([0.8, 2.95, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.5)
        self.at("not a ceiling")
        self.play(Indicate(kline, color=GOLD), run_time=0.8)

        self.at("starts above")
        n_hi = 1400.0
        hi = pl.curve(lambda t: logi(t, n_hi), 0, tmax, RED if False else BLUE, n=200)
        self.play(Create(hi), run_time=self.gap("starts below", lo=1.0, lead=0.8), rate_func=linear)
        hi_l = T("starts above K: declines", 26, BLUE).move_to(pl.pt(22, 1330))
        self.play(FadeIn(hi_l), run_time=0.4)
        self.at("starts below")
        lo = pl.curve(lambda t: logi(t, N0), 0, tmax, GREEN, n=200)
        self.play(Create(lo), run_time=self.gap("never overshoots", lo=1.0, lead=0.8), rate_func=linear)
        lo_l = T("starts below K: rises", 26, GREEN).move_to(pl.pt(24, 380))
        self.play(FadeIn(lo_l), run_time=0.4)
        self.at("never overshoots")
        self.play(Indicate(lo, color=GREEN), run_time=0.9)

        # reset to the lagged sketch
        self.at("Real populations")
        self.play(FadeOut(hi), FadeOut(hi_l), FadeOut(lo), FadeOut(lo_l), run_time=0.6)
        tau = 5.0
        ts, Ns = delayed_logistic(tau=tau, tmax=tmax + tau)
        keep = ts >= tau
        ts, Ns = ts[keep] - tau, Ns[keep]
        idx = np.arange(0, len(ts), 8)
        tl = VMobject(stroke_color=RED, stroke_width=6, fill_opacity=0)
        tl.set_points_as_corners([pl.pt(ts[i], min(Ns[i], ymax)) for i in idx])
        lag_l = chip("with a time lag", RED, size=26).move_to([2.8, -1.5, 0])
        self.play(Create(tl), run_time=self.gap("produce overshoot", lo=1.0, lead=0.8), rate_func=linear)
        self.play(FadeIn(lag_l), run_time=0.4)
        self.at("produce overshoot")
        self.play(Indicate(tl, color=RED, scale_factor=1.02), run_time=0.9)
        self.at("Keep the rule")
        rule = chip("per capita rate falls as N rises", YELLOW, size=28).move_to([2.3, -1.5, 0])
        self.play(FadeOut(lag_l), FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Per capita growth falls as N rises; K is an equilibrium."
