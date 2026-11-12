"""Population growth: Watch the Per-Capita Rate (film 1 of 2).

COLOUR MAP (same in both films)
  WHITE  = N, population size
  TEAL   = per-capita rate (and its line)
  GOLD   = K, the carrying capacity
  ORANGE = total growth dN/dt (and each day's gain)
  GREEN / RED = births / deaths (schematic, s02 and s09 only)
One world: rule on top, rate panel (left), N-vs-time panel (right), growth hump (lower left).
All curves are computed from r = 0.2 per day, K = 1000, N0 = 100.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
R, K, N0 = 0.2, 1000.0, 100.0
T_J = float(np.log(12.0) / R)          # day when exp growth reaches N = 1200 (12.43)


def Nlog(t):
    return K / (1 + (K / N0 - 1) * np.exp(-R * t))


def Nexp(t):
    return N0 * np.exp(R * t)


def tof(N):
    return -np.log((K / N - 1) / (K / N0 - 1)) / R


def rate(N, s=1.0):
    return R * (1 - s * N / K)


class Plot:
    """Hand-built axes (no LaTeX). box = (x0, x1, y0, y1) in scene units; xr, yr = data ranges."""

    def __init__(self, box, xr, yr, xticks, yticks, xlabel, ylabel):
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
        xl = T(xlabel, 24, GREY).move_to([(self.x0 + self.x1) / 2, self.y0 - 0.62, 0])
        yl = T(ylabel, 24, GREY).move_to([self.x0, self.y1 + 0.35, 0])
        yl.shift(RIGHT * (yl.width / 2 - 0.3))
        self.parts.add(xl, yl)

    def pt(self, x, y):
        fx = (x - self.xr[0]) / (self.xr[1] - self.xr[0])
        fy = (y - self.yr[0]) / (self.yr[1] - self.yr[0])
        return np.array([self.x0 + fx * (self.x1 - self.x0), self.y0 + fy * (self.y1 - self.y0), 0.0])


LB = (-5.4, -0.9, 0.6, 2.6)
RB = (2.0, 6.5, -2.75, 1.2)
HB = (-5.4, -0.9, -2.75, -1.1)


def left_plot():
    return Plot(LB, (0, 1200), (-0.05, 0.25), [(0, "0"), (500, "500"), (1000, "1000")],
                [(0, "0"), (0.1, "0.1"), (0.2, "0.2")], "N", "per-capita rate (per day)")


def right_plot(xmax=20):
    return Plot(RB, (0, xmax), (0, 1200), [(v, str(v)) for v in range(0, xmax + 1, 10)],
                [(0, "0"), (500, "500"), (1000, "1000")], "time (days)", "N")


def hump_plot():
    return Plot(HB, (0, 1000), (0, 70), [(0, "0"), (500, "500"), (1000, "1000")],
                [(0, "0"), (25, "25"), (50, "50")], "N", "growth (individuals / day)")


def zero_line(P):
    return DashedLine(P.pt(0, 0), P.pt(1200, 0), color=GREY, stroke_width=2, dash_length=0.12).set_opacity(0.6)


def rate_line(P, s):
    return Line(P.pt(0, R), P.pt(1200, R * (1 - s * 1.2)), color=TEAL, stroke_width=6)


def rate_line_live(P, st):
    return always_redraw(lambda: Line(P.pt(0, R), P.pt(1200, R * (1 - st.get_value() * 1.2)), color=TEAL, stroke_width=6))


def static_curve(P, fn, x0, x1, color=WHITE, w=6, op=1.0, n=120):
    xs = np.linspace(x0, x1, n)
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op, fill_opacity=0)
    m.set_points_as_corners([P.pt(x, fn(x)) for x in xs])
    return m


def grow_curve(P, fn, tt, color=WHITE, w=6):
    def mk():
        t = tt.get_value()
        m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
        if t < 0.05:
            return m
        xs = np.linspace(0, t, max(3, int(t * 10) + 1))
        m.set_points_as_corners([P.pt(x, fn(x)) for x in xs])
        return m
    return always_redraw(mk)


def rule(size=30):
    k = size / 30.0
    g = VGroup(T("growth", size, ORANGE, weight=BOLD), T("=", size), T("per-capita rate", size, TEAL, weight=BOLD),
               T("×", size), T("N", size, WHITE, weight=BOLD)).arrange(RIGHT, buff=0.25 * k)
    return g


def rule_top():
    return rule(30).move_to([0, 3.5, 0])


def readout(nf, rf):
    """Three rows tied to the same tracker as the dot: N (white), rate (teal), growth (orange)."""
    box = RoundedRectangle(corner_radius=0.14, width=5.2, height=1.9, stroke_color=GREY, stroke_width=2.5).move_to([-3.15, -1.85, 0])

    def mk():
        n = nf()
        r = rf(n)
        rows = VGroup(M(f"N      = {n:5.0f}", 28, WHITE), M(f"rate   = {r:+5.2f} /day", 28, TEAL),
                      M(f"growth = {r * n:+5.0f} /day", 28, ORANGE)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rows.move_to(box.get_center())
        rows.align_to(box.get_left() + RIGHT * 0.3, LEFT)
        return rows
    return VGroup(box, always_redraw(mk))


def animal(r=0.14, ears=True):
    g = VGroup(Dot(radius=r, color=WHITE))
    if ears:
        g.add(Dot(radius=r * 0.5, color=WHITE).shift(np.array([-r * 0.75, r * 0.85, 0])),
              Dot(radius=r * 0.5, color=WHITE).shift(np.array([r * 0.75, r * 0.85, 0])))
    return g


def bob(m, amp=0.04, speed=2.0, seed=0):
    rng = np.random.RandomState(seed)
    m.base = m.get_center().copy()
    m.ph = rng.uniform(0, 6.28)
    m.tt = 0.0

    def f(mm, dt):
        mm.tt += dt
        mm.move_to(mm.base + np.array([0, amp * np.sin(speed * mm.tt + mm.ph), 0]))
    m.add_updater(f)
    return m


def crowd(cols, rows, dx, dy, center, seed=1, ears=True, r=0.14, jitter=0.06):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for i in range(rows):
        for j in range(cols):
            p = np.array([center[0] + (j - (cols - 1) / 2) * dx + rng.uniform(-jitter, jitter),
                          center[1] + (i - (rows - 1) / 2) * dy + rng.uniform(-jitter, jitter), 0])
            g.add(bob(animal(r, ears).move_to(p), seed=len(g) + seed * 100))
    return g


def pulse(m, base=6, amp=2.5, speed=5.0):
    m.pt_ = 0.0

    def f(mm, dt):
        mm.pt_ += dt
        mm.set_stroke(width=base + amp * np.sin(speed * mm.pt_))
    m.add_updater(f)
    return m


class Base(SpokenScene):
    def setup(self):
        super().setup()
        rng = np.random.RandomState(abs(hash(os.environ.get("KX_SCENE_ID", "x"))) % 1000)
        W, H = 14.0, 7.8
        motes = VGroup()
        for _ in range(45):
            d = Dot(radius=rng.uniform(0.04, 0.09), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.25, 0.5))
            d.move_to([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0])
            d.v = (rng.uniform(-0.3, 0.3), rng.uniform(0.2, 0.5))

            def drift(m, dt):
                m.shift([m.v[0] * dt, m.v[1] * dt, 0])
                if m.get_y() > H / 2:
                    m.shift(DOWN * H)
                if abs(m.get_x()) > W / 2:
                    m.shift(LEFT * W * (1 if m.get_x() > 0 else -1))
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)

    def until(self, phrase, lead=0.25, lo=0.3, nth=0):
        return max(lo, self.t_of(phrase, nth) - lead - self.elapsed())

    def left_dot(self, P, nf, rf):
        return always_redraw(lambda: Dot(P.pt(nf(), rf(nf())), radius=0.12, color=WHITE, stroke_color=TEAL, stroke_width=3))


class S00Title(TitleCard):
    LESSON = "Population Growth and Regulation"
    TITLE = "Watch the Per-Capita Rate"


# ---------------------------------------------------------------------------------------------
class S01Question(Base):
    def construct(self):
        ic = crowd(10, 10, 0.5, 0.5, (-3.3, -0.2))
        self.play(LaggedStart(*[FadeIn(a, scale=0.4) for a in ic], lag_ratio=0.015), run_time=2.0)
        tag = VGroup(T("N = 100", 36, WHITE, weight=BOLD), T("growth rate now:", 28, TEAL), T("about 20 per day", 28, TEAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        box = SurroundingRectangle(tag, color=TEAL, buff=0.25, corner_radius=0.14, stroke_width=3)
        tagg = VGroup(box, tag).move_to([3.4, 1.8, 0])
        self.at("rate it is growing")
        self.play(FadeIn(tagg, shift=LEFT * 0.2), run_time=0.9)
        body = RoundedRectangle(corner_radius=0.15, width=3.0, height=2.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
        band = Rectangle(width=3.0, height=0.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.6).align_to(body, UP).align_to(body, LEFT)
        day = T("today", 40, WHITE).move_to(body.get_center() + DOWN * 0.2)
        cal = VGroup(body, band, day).move_to([3.4, -1.5, 0])
        self.at("right now")
        self.play(FadeIn(cal, shift=UP * 0.2), run_time=0.8)
        q = T("?", 80, GOLD, weight=BOLD).move_to([3.4, 0.45, 0])
        q.base = q.get_center().copy()
        q.tt = 0.0
        q.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.move_to(m.base + UP * 0.12 * np.sin(3 * m.tt)))[0])
        self.at("tomorrow's")
        tom = T("tomorrow?", 38, WHITE).move_to(day)
        self.play(FadeIn(q), Transform(day, tom), run_time=0.8)
        self.at("or faster")
        self.play(Indicate(q, scale_factor=1.3, color=GOLD), run_time=0.9)
        self.finish()


class S02Percapita(Base):
    def construct(self):
        ic = crowd(10, 10, 0.5, 0.5, (-3.3, -0.2))
        self.add(ic)
        keep = ic[55]
        others = VGroup(*[a for i, a in enumerate(ic) if i != 55])
        keep.clear_updaters()
        self.play(FadeOut(others), keep.animate.scale(3.6).move_to([-3.6, 0.2, 0]), run_time=1.4)
        eyes = VGroup(Dot(radius=0.07, color=BG).move_to(keep[0].get_center() + np.array([-0.17, 0.08, 0])),
                      Dot(radius=0.07, color=BG).move_to(keep[0].get_center() + np.array([0.17, 0.08, 0])))
        self.play(FadeIn(eyes), run_time=0.4)
        self.at("it may give birth")
        baby = animal(0.1).move_to([-1.2, 1.5, 0])
        a1 = Arrow([-2.9, 0.6, 0], [-1.7, 1.35, 0], color=GREEN, buff=0, stroke_width=6)
        l1 = T("+ births", 34, GREEN).next_to(baby, RIGHT, buff=0.3)
        self.play(GrowArrow(a1), FadeIn(baby, scale=0.2), FadeIn(l1), run_time=1.0)
        self.at("and it may die")
        ghost = animal(0.1).move_to([-1.2, -1.1, 0]).set_opacity(0.4)
        a2 = Arrow([-2.9, -0.2, 0], [-1.7, -0.95, 0], color=RED, buff=0, stroke_width=6)
        l2 = T("- deaths", 34, RED).next_to(ghost, RIGHT, buff=0.3)
        self.play(GrowArrow(a2), FadeIn(ghost, scale=0.2), FadeIn(l2), run_time=1.0)
        self.at("Births minus deaths")
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(baby), FadeOut(ghost),
                  l1.animate.move_to([3.2, 0.9, 0]), l2.animate.move_to([3.2, -0.3, 0]), run_time=1.4)
        self.at("per individual")
        br = SurroundingRectangle(VGroup(l1, l2), color=GREY, buff=0.25, corner_radius=0.12, stroke_width=2.5)
        self.play(Create(br), run_time=0.8)
        self.at("per capita rate")
        badge = VGroup(T("per-capita rate", 36, TEAL, weight=BOLD), T("= births - deaths,", 28), T("per individual", 28)).arrange(DOWN, buff=0.15)
        bb = SurroundingRectangle(badge, color=TEAL, buff=0.28, corner_radius=0.14, stroke_width=3.5)
        badge = VGroup(bb, badge).move_to([3.4, 0.3, 0])
        self.play(ReplacementTransform(VGroup(l1, l2, br), badge), run_time=1.2)
        self.play(Indicate(badge, color=TEAL, scale_factor=1.06), run_time=0.9)
        self.finish()


class S03Rule(Base):
    def construct(self):
        badge = VGroup(T("per-capita rate", 36, TEAL, weight=BOLD), T("= births - deaths,", 28), T("per individual", 28)).arrange(DOWN, buff=0.15)
        bb = SurroundingRectangle(badge, color=TEAL, buff=0.28, corner_radius=0.14, stroke_width=3.5)
        badge = VGroup(bb, badge).move_to([3.4, 0.3, 0])
        big = rule(44).move_to([0, 0.9, 0])
        self.add(badge)
        self.play(ReplacementTransform(badge, big[2]), run_time=1.4)
        self.at("by the population")
        self.play(FadeIn(big[3], shift=LEFT * 0.2), run_time=0.7)
        self.at("population size")
        self.play(FadeIn(big[4], shift=LEFT * 0.2), run_time=0.7)
        self.at("n", lead=0.1)
        self.play(Indicate(big[4], scale_factor=1.4, color=WHITE), run_time=0.9)
        # the closed population
        self.at("in a closed")
        sub = T("closed population: no one moves in or out", 28, TEXT).move_to([0, 0.05, 0])
        ctr = np.array([0, -1.95, 0])
        ring = Circle(radius=1.1, color=GREY, stroke_width=4).move_to(ctr)
        dots = VGroup()
        rng = np.random.RandomState(4)
        for i in range(14):
            d = Dot(radius=0.09, color=WHITE).move_to(ctr + np.array([rng.uniform(-.7, .7), rng.uniform(-.7, .7), 0]))
            d.v = np.array([rng.uniform(-.5, .5), rng.uniform(-.5, .5), 0])

            def wander(m, dt, ctr=ctr):
                m.shift(m.v * dt)
                c = m.get_center() - ctr
                dd = np.linalg.norm(c)
                if dd > 0.95:
                    u = c / dd
                    m.v = m.v - 2 * np.dot(m.v, u) * u
                    m.shift(-u * (dd - 0.95))
            d.add_updater(wander)
            dots.add(d)
        self.play(FadeIn(sub), Create(ring), FadeIn(dots), run_time=1.2)
        self.at("with no one moving")
        def arrow_x(x0, x1):
            ar = Arrow([x0, ctr[1], 0], [x1, ctr[1], 0], color=GREY, buff=0, stroke_width=6)
            mid = (x0 + x1) / 2
            cr = VGroup(Line([mid - .25, ctr[1] - .25, 0], [mid + .25, ctr[1] + .25, 0]), Line([mid - .25, ctr[1] + .25, 0], [mid + .25, ctr[1] - .25, 0])).set_stroke(RED, 7)
            return VGroup(ar, cr)
        ax1, ax2 = arrow_x(-3.6, -1.4), arrow_x(3.6, 1.4)
        self.play(FadeIn(ax1, shift=RIGHT * 0.2), FadeIn(ax2, shift=LEFT * 0.2), run_time=1.0)
        self.at("that product")
        self.play(FadeIn(big[1]), FadeIn(big[0], shift=RIGHT * 0.2), run_time=0.9)
        self.at("growth", nth=0, lead=0.1)
        self.play(Indicate(big[0], color=ORANGE, scale_factor=1.25), run_time=0.9)
        self.at("This one rule")
        top = rule(30).move_to([0, 3.5, 0])
        self.play(FadeOut(VGroup(sub, ring, dots, ax1, ax2)), Transform(big, top), run_time=1.8)
        self.finish()


class S04Flat(Base):
    def construct(self):
        self.add(rule_top())
        LP = left_plot()
        RP = right_plot(20)
        self.play(FadeIn(LP.parts), run_time=1.4)
        nn = ValueTracker(0)
        line = rate_line(LP, 0)
        self.at("First")
        z = zero_line(LP)
        ro = readout(lambda: nn.get_value(), lambda n: R)
        dot = self.left_dot(LP, lambda: nn.get_value(), lambda n: R)
        self.add(ro, dot)
        self.play(Create(line, run_time=3.0, rate_func=linear), nn.animate(run_time=3.0, rate_func=linear).set_value(1200),
                  FadeIn(RP.parts, run_time=1.4), FadeIn(z))
        lab = T("r = 0.2 per day", 30, TEAL).move_to(LP.pt(0, 0.145)).align_to(LP.pt(60, 0), LEFT)
        self.play(FadeIn(lab), run_time=0.7)
        self.play(nn.animate(run_time=2.2, rate_func=there_and_back).set_value(300))
        self.finish()


def strip_static():
    base = Line([2.0, 2.0, 0], [6.5, 2.0, 0], color=GREY, stroke_width=3)
    lab = VGroup(T("gain per day", 24, ORANGE), T("(computed)", 22, GREY)).arrange(DOWN, buff=0.05).move_to([5.7, 2.5, 0])
    return VGroup(base, lab)


def strip_bars(tt):
    def mk():
        t = tt.get_value()
        g = VGroup()
        for d in range(int(t)):
            gain = Nexp(d + 1) - Nexp(d)
            h = max(gain / 350 * 0.95, 0.02)
            xc = 2.0 + 4.5 * (d + 0.5) / 20
            g.add(Rectangle(width=0.17, height=h, stroke_width=0, fill_color=ORANGE, fill_opacity=0.8).move_to([xc, 2.0 + h / 2, 0]))
        return g
    return always_redraw(mk)


def strip_tags(tt):
    def mk():
        t = tt.get_value()
        g = VGroup()
        for d in range(min(3, int(t))):
            gain = Nexp(d + 1) - Nexp(d)
            g.add(T(f"+{gain:.0f}", 24, ORANGE).move_to([2.35 + d * 0.6, 2.5, 0]))
        return g
    return always_redraw(mk)


class S05Compound(Base):
    def construct(self):
        self.add(rule_top())
        LP, RP = left_plot(), right_plot(20)
        tt = ValueTracker(0)
        nf = lambda: Nexp(tt.get_value())
        self.add(LP.parts, zero_line(LP), rate_line(LP, 0), RP.parts, strip_static())
        self.add(readout(nf, lambda n: R), self.left_dot(LP, nf, lambda n: R))
        curve = grow_curve(RP, Nexp, tt)
        tipd = always_redraw(lambda: Dot(RP.pt(tt.get_value(), Nexp(tt.get_value())), radius=0.1, color=WHITE))
        self.add(curve, tipd, strip_bars(tt), strip_tags(tt))
        self.play(tt.animate(run_time=9.2, rate_func=linear).set_value(10))
        self.finish()


class S06Jcurve(Base):
    def construct(self):
        self.add(rule_top())
        LP, RP = left_plot(), right_plot(20)
        tt = ValueTracker(10)
        nf = lambda: Nexp(tt.get_value())
        self.add(LP.parts, zero_line(LP), rate_line(LP, 0), RP.parts, strip_static())
        self.add(readout(nf, lambda n: R), self.left_dot(LP, nf, lambda n: R))
        curve = grow_curve(RP, Nexp, tt)
        tipd = always_redraw(lambda: Dot(RP.pt(tt.get_value(), Nexp(tt.get_value())), radius=0.1, color=WHITE))
        self.add(curve, tipd, strip_bars(tt))
        p10 = RP.pt(10, Nexp(10))
        self.at("By day 10")
        vline = DashedLine(RP.pt(10, 0), p10, color=GREY, stroke_width=3)
        lab739 = VGroup(T("739", 34, WHITE, weight=BOLD), T("(computed)", 22, GREY)).arrange(DOWN, buff=0.03).next_to(p10, RIGHT, buff=0.25)
        self.play(Create(vline), FadeIn(lab739), Indicate(tipd, scale_factor=2.2, color=WHITE), run_time=1.3)
        self.at("steady adding")
        p300 = RP.pt(10, 300)
        hl = DashedLine(RP.pt(0, 300), p300, color=GREY, stroke_width=3)
        m300 = Dot(p300, radius=0.09, color=GREY)
        l300 = VGroup(T("300 if it added", 24, GREY), T("20 a day", 24, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(p300, RIGHT, buff=0.25)
        self.play(Create(hl), FadeIn(m300), FadeIn(l300), run_time=1.3)
        self.at("This compounding")
        self.play(tt.animate(run_time=1.3, rate_func=linear).set_value(T_J))
        self.at("exponential growth", lead=0.4)
        jl = VGroup(T("J-curve:", 30, WHITE, weight=BOLD), T("exponential", 30, WHITE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([5.3, -1.7, 0])
        self.play(FadeOut(VGroup(vline, lab739, hl, m300, l300)), FadeIn(jl, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


def gold_right(P, xmax):
    ln = DashedLine(P.pt(0, K), P.pt(xmax, K), color=GOLD, stroke_width=4)
    return ln


def k_left(P):
    ln = DashedLine(P.pt(K, 0), P.pt(K, -0.05), color=GOLD, stroke_width=5)
    return ln


class S07Crowding(Base):
    def construct(self):
        self.add(rule_top())
        LP, RP = left_plot(), right_plot(20)
        self.add(LP.parts, zero_line(LP), rate_line(LP, 0), RP.parts, static_curve(RP, Nexp, 0, T_J))
        self.add(VGroup(T("J-curve:", 30, WHITE, weight=BOLD), T("exponential", 30, WHITE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([5.3, -1.7, 0]))
        # crowd box x -5.6..-0.8, y -2.4..-0.5
        rng = np.random.RandomState(7)
        pos = [np.array([rng.uniform(-5.4, -1.0), rng.uniform(-2.3, -0.6), 0]) for _ in range(110)]
        pop = VGroup(*[bob(animal(0.1, False).move_to(p), seed=i) for i, p in enumerate(pos)])
        food = VGroup(*[Square(0.14, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).move_to([rng.uniform(-5.4, -1.0), rng.uniform(-2.3, -0.6), 0]) for _ in range(24)])
        self.play(FadeIn(food), FadeIn(pop[:12]), run_time=0.8)
        self.at("As numbers rise")
        self.play(LaggedStart(*[FadeIn(p, scale=0.3) for p in pop[12:]], lag_ratio=0.03), run_time=2.2)
        self.at("less food")
        c1 = chip("food", GREEN, 26)
        c2 = chip("space", GREY, 26)
        c3 = chip("shelter", TEAL, 26)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3).move_to([-3.2, -3.1, 0])
        self.play(FadeIn(c1), food[:16].animate.set_opacity(0.15), run_time=1.0)
        self.at("space")
        self.play(FadeIn(c2), run_time=0.7)
        self.at("shelter")
        self.play(FadeIn(c3), food[16:].animate.set_opacity(0.15), run_time=0.8)
        self.at("Births fall")
        arr = Arrow(LP.pt(1000, R) + DOWN * 0.15, LP.pt(1000, R) + DOWN * 0.95, color=TEAL, buff=0, stroke_width=7)
        arr.base = arr.get_center().copy()
        arr.tt = 0.0
        arr.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.move_to(m.base + DOWN * 0.12 * np.sin(4 * m.tt)))[0])
        self.play(FadeIn(arr), run_time=0.6)
        self.finish()


class S08Tilt(Base):
    def construct(self):
        self.add(rule_top())
        LP, RP = left_plot(), right_plot(20)
        self.add(LP.parts, zero_line(LP), RP.parts, static_curve(RP, Nexp, 0, T_J))
        self.add(VGroup(T("J-curve:", 30, WHITE, weight=BOLD), T("exponential", 30, WHITE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([5.3, -1.7, 0]))
        st = ValueTracker(0)
        nn = ValueTracker(600)
        self.add(rate_line_live(LP, st))
        rf = lambda n: R * (1 - st.get_value() * n / K)
        ro = readout(lambda: nn.get_value(), rf)
        dot = self.left_dot(LP, lambda: nn.get_value(), rf)
        self.add(ro, dot)
        self.at("tilt the line")
        self.play(st.animate(run_time=2.4).set_value(1.0))
        self.at("Let the per")
        self.play(nn.animate(run_time=3.4, rate_func=linear).set_value(1200))
        self.at("The logistic model")
        lab = VGroup(T("assumed", 28, TEAL, weight=BOLD), T("straight line", 28, TEAL, weight=BOLD)).arrange(DOWN, buff=0.04).move_to(LP.pt(960, 0.185))
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.8)
        self.play(nn.animate(run_time=3.0, rate_func=linear).set_value(100))
        self.finish()


class S09K(Base):
    def construct(self):
        self.add(rule_top())
        LP, RP = left_plot(), right_plot(20)
        self.add(LP.parts, zero_line(LP), rate_line(LP, 1), RP.parts, static_curve(RP, Nexp, 0, T_J))
        self.add(VGroup(T("J-curve:", 30, WHITE, weight=BOLD), T("exponential", 30, WHITE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([5.3, -1.7, 0]))
        nn = ValueTracker(0)
        rf = lambda n: rate(n)
        dot = self.left_dot(LP, lambda: nn.get_value(), rf)
        self.add(dot)
        self.play(nn.animate(run_time=1.4, rate_func=linear).set_value(1000))
        self.at("a size called")
        kl = k_left(LP)
        kt = T("K = 1,000", 30, GOLD, weight=BOLD).move_to(LP.pt(1000, 0.14))
        kr = gold_right(RP, 20)
        kr_t = T("K", 30, GOLD, weight=BOLD).move_to(RP.pt(17.5, 780))
        self.play(Create(kl), FadeIn(kt), run_time=0.9)
        self.at("carrying capacity", lead=0.3)
        self.play(Create(kr), FadeIn(kr_t), run_time=1.0)
        self.at("There")
        # births vs deaths bars (schematic): births fixed, deaths grow with N
        base_y = -2.6
        births = Rectangle(width=0.9, height=1.6, stroke_width=0, fill_color=GREEN, fill_opacity=0.8).move_to([-4.3, base_y + 0.8, 0])
        deaths_h = lambda: max(1.6 * nn.get_value() / K, 0.02)
        deaths = always_redraw(lambda: Rectangle(width=0.9, height=deaths_h(), stroke_width=0, fill_color=RED, fill_opacity=0.8).move_to([-2.7, base_y + deaths_h() / 2, 0]))
        lb = T("births", 26, GREEN).move_to([-4.3, -3.0, 0])
        ld = T("deaths", 26, RED).move_to([-2.7, -3.0, 0])
        sch = T("per individual (schematic)", 24, GREY).move_to([-3.5, -0.65, 0])
        eq = T("=", 48, WHITE, weight=BOLD).move_to([-3.5, base_y + 0.9, 0])
        self.play(FadeIn(births), FadeIn(deaths), FadeIn(lb), FadeIn(ld), FadeIn(sch), run_time=0.9)
        self.play(FadeIn(eq, scale=1.4), run_time=0.6)
        self.play(nn.animate(run_time=1.6).set_value(600), FadeOut(eq))
        self.play(nn.animate(run_time=1.6).set_value(1000))
        self.play(FadeIn(eq, scale=1.4), run_time=0.5)
        self.finish()


def left_tilt_world(scene, with_k=True):
    LP = left_plot()
    scene.add(LP.parts, zero_line(LP), rate_line(LP, 1))
    if with_k:
        scene.add(k_left(LP), T("K = 1,000", 30, GOLD, weight=BOLD).move_to(LP.pt(1000, 0.14)))
    return LP


def right30_world(scene, s_curve=True, j_op=0.3):
    RP = right_plot(30)
    scene.add(RP.parts, gold_right(RP, 30), T("K", 30, GOLD, weight=BOLD).move_to(RP.pt(27.5, 780)),
              static_curve(RP, Nexp, 0, T_J, color=WHITE, w=3, op=j_op))
    if s_curve:
        scene.add(static_curve(RP, Nlog, 0, 30, n=200))
    return RP


class S10Scurve(Base):
    def construct(self):
        self.add(rule_top())
        LP = left_tilt_world(self)
        RP0 = right_plot(20)
        old = VGroup(RP0.parts, static_curve(RP0, Nexp, 0, T_J), gold_right(RP0, 20), T("K", 30, GOLD, weight=BOLD).move_to(RP0.pt(17.5, 780)),
                     VGroup(T("J-curve:", 30, WHITE, weight=BOLD), T("exponential", 30, WHITE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([5.3, -1.7, 0]))
        self.add(old)
        RP = right_plot(30)
        new = VGroup(RP.parts, gold_right(RP, 30), T("K", 30, GOLD, weight=BOLD).move_to(RP.pt(27.5, 780)),
                     static_curve(RP, Nexp, 0, T_J, color=WHITE, w=3, op=0.3))
        self.wait(0.4)
        self.play(FadeOut(old), FadeIn(new), run_time=1.4)
        tt = ValueTracker(0)
        nf = lambda: Nlog(tt.get_value())
        ro = readout(nf, lambda n: rate(n))
        dot = self.left_dot(LP, nf, lambda n: rate(n))
        self.add(ro, dot)
        curve = grow_curve(RP, Nlog, tt)
        tipd = always_redraw(lambda: Dot(RP.pt(tt.get_value(), Nlog(tt.get_value())), radius=0.1, color=WHITE))
        self.add(curve, tipd)
        self.at("The curve rises")
        self.play(tt.animate(run_time=5.4, rate_func=linear).set_value(30))
        self.at("That is the")
        sl = VGroup(T("S-curve:", 30, WHITE, weight=BOLD), T("logistic", 30, WHITE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([5.3, -1.7, 0])
        self.play(FadeIn(sl, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


class S11Predict(Base):
    def construct(self):
        self.add(rule_top())
        LP = left_tilt_world(self)
        RP = right30_world(self)
        s = static_curve(RP, Nlog, 0, 30, w=6, n=200)
        self.add(pulse(s, 6, 3, 4.0))
        self.at("at what size")
        chips = [chip("when N is small", WHITE, 26), chip("halfway to K", WHITE, 26), chip("right at K", WHITE, 26)]
        grp = VGroup(*chips).arrange(DOWN, buff=0.15).move_to([-3.1, -1.85, 0])
        self.play(FadeIn(chips[0], shift=RIGHT * 0.2), run_time=0.7)
        self.at("most individuals")
        self.play(FadeIn(chips[1], shift=RIGHT * 0.2), run_time=0.7)
        self.at("per day")
        self.play(FadeIn(chips[2], shift=RIGHT * 0.2), run_time=0.7)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        self.add(rule_top())
        LP = left_tilt_world(self)
        RP = right30_world(self)
        s = static_curve(RP, Nlog, 0, 30, w=6, n=200)
        self.add(s)
        chips = [chip("when N is small", WHITE, 26), chip("halfway to K", WHITE, 26), chip("right at K", WHITE, 26)]
        self.add(VGroup(*chips).arrange(DOWN, buff=0.15).move_to([-3.1, -1.85, 0]))
        cap = T("Predict: where is it adding the most per day?", 26, TEXT).move_to([-6.6, -3.5, 0]).align_to([-6.6, 0, 0], LEFT)
        self.add(cap)
        pr = ValueTracker(1.0)
        c0 = np.array([0.15, -1.75, 0])
        ring_bg = Circle(radius=0.6, color=GREY, stroke_width=4).move_to(c0).set_opacity(0.5)
        ring = always_redraw(lambda: Arc(radius=0.6, start_angle=PI / 2, angle=max(pr.get_value(), 0.001) * TAU, color=GOLD, stroke_width=8, arc_center=c0))
        self.add(ring_bg, ring)
        self.play(pr.animate(run_time=4.8, rate_func=linear).set_value(0.0))
        self.finish()


class S13Reveal(Base):
    def construct(self):
        self.add(rule_top())
        LP = left_tilt_world(self)
        RP = right30_world(self)
        self.add(static_curve(RP, Nlog, 0, 30, w=6, n=200))
        nn = ValueTracker(500)
        rf = lambda n: rate(n)
        dotL = self.left_dot(LP, lambda: nn.get_value(), rf)
        dotR = always_redraw(lambda: Dot(RP.pt(tof(nn.get_value()), nn.get_value()), radius=0.12, color=WHITE, stroke_color=ORANGE, stroke_width=3))
        half = chip("halfway to K", GOLD, 26).move_to([-2.9, -3.15, 0])
        # icon cluster and "each adds" bar, both tied to N
        def cluster():
            n = nn.get_value()
            cnt = max(1, int(n / 20))
            g = VGroup()
            for i in range(cnt):
                r_, c_ = divmod(i, 10)
                g.add(animal(0.07, False).move_to([-4.2 + c_ * 0.3, -1.05 - r_ * 0.3, 0]))
            return g
        def bar():
            h = max(1.6 * rate(nn.get_value()) / 0.2, 0.03)
            return Rectangle(width=0.7, height=h, stroke_width=0, fill_color=TEAL, fill_opacity=0.85).move_to([-5.3, -2.7 + h / 2, 0])
        barlab = T("each adds", 24, TEAL).move_to([-5.4, -3.2, 0])
        def fm():
            n = nn.get_value()
            if n < 300:
                return T("few", 30, WHITE, weight=BOLD).move_to([-2.9, -0.6, 0])
            if n > 700:
                return T("many", 30, WHITE, weight=BOLD).move_to([-2.9, -0.6, 0])
            return VGroup()
        self.add(dotL, dotR)
        self.play(FadeIn(half, shift=UP * 0.2), run_time=0.8)
        self.play(Indicate(half, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.at("When the population is small")
        self.play(nn.animate(run_time=1.4).set_value(100))
        self.add(always_redraw(cluster), always_redraw(bar), always_redraw(fm), barlab)
        self.at("each individual adds")
        self.play(Indicate(barlab, color=TEAL), run_time=0.9)
        self.at("Near K")
        self.play(nn.animate(run_time=2.6, rate_func=linear).set_value(900))
        self.at("each adding little")
        self.play(Indicate(barlab, color=TEAL), run_time=0.8)
        self.finish()




def hump_fn(n):
    return R * n * (1 - n / K)


def hump_live(HP, nn):
    def mk():
        m = VMobject(stroke_color=ORANGE, stroke_width=7, fill_opacity=0)
        n = nn.get_value()
        if n > 3:
            xs = np.linspace(0, n, max(3, int(n / 10) + 2))
            m.set_points_as_corners([HP.pt(x, hump_fn(x)) for x in xs])
        return m
    return always_redraw(mk)


class S14Hump(Base):
    def construct(self):
        self.add(rule_top())
        LP = left_tilt_world(self)
        RP = right30_world(self)
        self.add(static_curve(RP, Nlog, 0, 30, w=6, n=200))
        HP = hump_plot()
        self.play(FadeIn(HP.parts), run_time=1.0)
        nn = ValueTracker(0)
        dotL = self.left_dot(LP, lambda: nn.get_value(), lambda n: rate(n))
        hump = hump_live(HP, nn)
        tip = always_redraw(lambda: Dot(HP.pt(nn.get_value(), hump_fn(nn.get_value())), radius=0.11, color=ORANGE))
        self.add(dotL, hump, tip)
        self.play(nn.animate(run_time=4.4, rate_func=linear).set_value(1000))
        self.at("highest at half")
        pk = HP.pt(500, 50)
        pkl = VGroup(T("peak =", 26, ORANGE, weight=BOLD), T("50 per day", 26, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to(pk + DOWN * 0.6)
        self.play(FadeIn(pkl), Indicate(tip, scale_factor=1.8), run_time=1.0)
        self.at("steepest", lead=2.0)
        ps = RP.pt(tof(500), 500)
        wp = RP.pt(0, 750) + LEFT * 0.7
        link = VGroup(DashedLine(pk + RIGHT * 0.1, wp, color=ORANGE, stroke_width=3.5, dash_length=0.1), DashedLine(wp, ps, color=ORANGE, stroke_width=3.5, dash_length=0.1))
        mk = Dot(ps, radius=0.13, color=ORANGE)
        kl = T("K/2 = 500", 26, ORANGE, weight=BOLD).next_to(ps, DOWN + RIGHT, buff=0.15)
        self.play(Create(link), FadeIn(mk), run_time=1.5)
        self.play(FadeIn(kl), Indicate(mk, scale_factor=1.8, color=ORANGE), run_time=1.0)
        self.finish()


def hump_static(HP, op=1.0):
    return static_curve(HP, hump_fn, 0, 1000, color=ORANGE, w=7, op=op)


def k_hump(HP):
    return DashedLine(HP.pt(1000, 0), HP.pt(1000, 60), color=GOLD, stroke_width=4)


class S15Stop(Base):
    def construct(self):
        self.add(rule_top())
        LP = left_tilt_world(self)
        RP = right30_world(self)
        self.add(static_curve(RP, Nlog, 0, 30, w=6, n=200))
        HP = hump_plot()
        self.add(HP.parts, hump_static(HP))
        nn = ValueTracker(500)
        dotL = self.left_dot(LP, lambda: nn.get_value(), lambda n: rate(n))
        tip = always_redraw(lambda: Dot(HP.pt(nn.get_value(), hump_fn(nn.get_value())), radius=0.11, color=ORANGE))
        pkl = VGroup(T("peak =", 26, ORANGE, weight=BOLD), T("50 per day", 26, ORANGE, weight=BOLD)).arrange(DOWN, buff=0.05).move_to(HP.pt(500, 50) + DOWN * 0.6)
        self.add(dotL, tip, pkl)
        self.play(FadeOut(pkl), run_time=0.4)
        self.play(nn.animate(run_time=2.8, rate_func=linear).set_value(1000))
        kh = k_hump(HP)
        self.play(Create(kh), run_time=0.6)
        zl, zh = LP.pt(1000, 0), HP.pt(1000, 0)
        self.play(Flash(zl, color=TEAL, line_length=0.3, flash_radius=0.3), Flash(zh, color=ORANGE, line_length=0.3, flash_radius=0.3), run_time=1.0)
        self.at("per capita rate")
        r1 = Circle(radius=0.28, color=TEAL, stroke_width=5).move_to(zl)
        self.play(Create(r1), run_time=0.6)
        while self.elapsed() < self.narration_s - 2.8:
            self.play(nn.animate(run_time=1.3).set_value(550))
            self.play(nn.animate(run_time=1.3).set_value(1000))
        self.finish()


class S16Summary(Base):
    def construct(self):
        self.add(rule_top())
        st = ValueTracker(1.0)
        LP = left_plot()
        self.add(LP.parts, zero_line(LP), rate_line_live(LP, st), k_left(LP), T("K = 1,000", 30, GOLD, weight=BOLD).move_to(LP.pt(1000, 0.14)))
        RP = right_plot(30)
        self.add(RP.parts, gold_right(RP, 30), T("K", 30, GOLD, weight=BOLD).move_to(RP.pt(27.5, 780)))
        J = static_curve(RP, Nexp, 0, T_J, w=6)
        S = static_curve(RP, Nlog, 0, 30, w=6, n=200)
        HP = hump_plot()
        H = hump_static(HP)
        self.add(HP.parts, k_hump(HP), J, S, H)
        J.add_updater(lambda m: m.set_stroke(opacity=0.2 + 0.8 * (1 - st.get_value())))
        S.add_updater(lambda m: m.set_stroke(opacity=0.2 + 0.8 * st.get_value()))
        H.add_updater(lambda m: m.set_stroke(opacity=0.2 + 0.8 * st.get_value()))
        la = T("compounds", 30, WHITE, weight=BOLD).move_to([5.45, -1.9, 0])
        lb = T("stops at K", 30, GOLD, weight=BOLD).move_to([5.45, -1.9, 0])
        la.add_updater(lambda m: m.set_opacity(float(np.clip((0.5 - st.get_value()) * 4, 0, 1))))
        lb.add_updater(lambda m: m.set_opacity(float(np.clip((st.get_value() - 0.5) * 5, 0, 1))))
        self.add(la, lb)
        self.wait(0.3)
        self.at("one teal line")
        self.play(Indicate(LP.parts[0], color=TEAL, scale_factor=1.0), run_time=0.1)
        self.at("Hold it flat")
        self.play(st.animate(run_time=2.2).set_value(0.0))
        self.at("Let it fall")
        self.play(st.animate(run_time=2.4).set_value(1.0))
        while self.elapsed() < self.narration_s - 2.2:
            self.play(st.animate(run_time=1.0).set_value(0.7))
            self.play(st.animate(run_time=1.0).set_value(1.0))
        self.finish()


class S17Assumption(Base):
    def construct(self):
        self.add(rule_top())
        LP = left_tilt_world(self)
        RP = right30_world(self)
        self.add(static_curve(RP, Nlog, 0, 30, w=6, n=200))
        HP = hump_plot()
        hg = VGroup(HP.parts, hump_static(HP), k_hump(HP))
        self.add(hg)
        tl = Line(LP.pt(0, R), LP.pt(1200, R * (1 - 1.2)), color=TEAL, stroke_width=6)
        pulse(tl, 6, 2.5, 3.0)
        self.add(tl)
        self.at("assumption")
        t = T("assumption", 28, GOLD, weight=BOLD)
        st = VGroup(SurroundingRectangle(t, color=GOLD, buff=0.2, corner_radius=0.08, stroke_width=4), t).move_to([0.1, 2.75, 0])
        self.play(FadeIn(st, scale=1.6), run_time=0.5)
        self.at("Whether")
        self.play(FadeOut(hg), run_time=0.9)
        self.at("tested in the field")
        nb = VGroup(RoundedRectangle(corner_radius=0.1, width=1.5, height=2.0, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.18))
        for i in range(5):
            nb.add(Line([-0.45, 0.65 - i * 0.28, 0], [0.45, 0.65 - i * 0.28, 0], color=GREY, stroke_width=3))
        nb.move_to([-4.6, -1.8, 0])
        q = T("?", 80, GOLD, weight=BOLD).move_to([-2.6, -1.2, 0])
        q.base = q.get_center().copy()
        q.tt = 0.0
        q.add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.move_to(m.base + UP * 0.12 * np.sin(3 * m.tt)))[0])
        mi = T("measure it", 36, WHITE, weight=BOLD).move_to([-2.0, -2.55, 0])
        self.play(FadeIn(nb, shift=UP * 0.2), FadeIn(q), FadeIn(mi), run_time=1.0)
        self.finish()


class S18End(EndCard):
    LINE = "Growth stops where the per-capita rate falls to zero: at K."
