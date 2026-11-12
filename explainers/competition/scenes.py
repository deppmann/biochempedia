"""Competition (film 1): Can it grow when rare?  Lotka-Volterra competition, invasion test.

COLOUR MAP (whole film): TEAL = species 1, ORANGE = species 2, WHITE ring = the crossing,
GREEN = passes / coexist, RED = fails / exclusion, YELLOW = bistable / highlight.
Every curve is integrated from  dN1/dt = r1 N1 (1 - (N1 + a12 N2)/K1),  dN2/dt = r2 N2 (1 - (N2 + a21 N1)/K2)
with K1 = 100, K2 = 80, r1 = 1.0, r2 = 0.5 (teal grows twice as fast), a12 = a21 = 0.5 unless a scene says otherwise.
Creatures and room bars are cartoons (schematic); plane lines and paths are computed.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

TC = TEAL
OC = "#F29E4C"
K1, K2 = 100.0, 80.0
R1, R2 = 1.0, 0.5
XMAX, YMAX = 170.0, 120.0
RING = "#FFFFFF"


# ------------------------------------------------------------------ computed dynamics
def sim(a12, a21, n1, n2, r1=R1, r2=R2, T=60.0, dt=0.02, step=5):
    pts = [(n1, n2)]
    for i in range(int(T / dt)):
        d1 = r1 * n1 * (1 - (n1 + a12 * n2) / K1)
        d2 = r2 * n2 * (1 - (n2 + a21 * n1) / K2)
        n1, n2 = max(n1 + d1 * dt, 0.0), max(n2 + d2 * dt, 0.0)
        if i % step == 0:
            pts.append((n1, n2))
    return pts


def separatrix(a12, a21):
    """Stable manifold of the saddle (bistable case), by integrating backward in time."""
    det = 1 - a12 * a21
    s1 = (K1 - a12 * K2) / det
    s2 = (K2 - a21 * K1) / det
    f = lambda x, y: np.array([R1 * x * (1 - (x + a12 * y) / K1), R2 * y * (1 - (y + a21 * x) / K2)])
    e = 1e-4
    J = np.array([(f(s1 + e, s2) - f(s1 - e, s2)) / (2 * e), (f(s1, s2 + e) - f(s1, s2 - e)) / (2 * e)]).T
    w, v = np.linalg.eig(J)
    vs = v[:, int(np.argmin(w))].real
    out = []
    for sgn in (1, -1):
        p = np.array([s1, s2]) + sgn * 0.5 * vs
        arm = [tuple(p)]
        for _ in range(60000):
            p = p - 0.01 * f(*p)
            if not (0 <= p[0] <= XMAX and 0 <= p[1] <= YMAX):
                break
            arm.append(tuple(p))
        out.append(arm)
    return out[0][::-1] + [(s1, s2)] + out[1]


def teal_pts(a):
    p1 = (0, K1 / a) if K1 / a <= YMAX else (K1 - a * YMAX, YMAX)
    return (K1, 0), p1


def orange_pts(a):
    p1 = (K2 / a, 0) if K2 / a <= XMAX else (XMAX, K2 - a * XMAX)
    return (0, K2), p1


def cross(a12, a21):
    det = 1 - a12 * a21
    return (K1 - a12 * K2) / det, (K2 - a21 * K1) / det


# ------------------------------------------------------------------ small helpers
def sym(base, sub, size=34, color=TEXT):
    b = T(base, size, color)
    s = T(sub, max(22, int(size * 0.66)), color)
    s.next_to(b, RIGHT, buff=0.03).shift(DOWN * 0.09)
    return VGroup(b, s)


def creature(color, r=0.34):
    body = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.85)
    eyes = VGroup(Dot(radius=r * 0.13, color=BG).move_to([-r * 0.33, r * 0.15, 0]),
                  Dot(radius=r * 0.13, color=BG).move_to([r * 0.33, r * 0.15, 0]))
    return VGroup(body, eyes)


def bob(m, amp=0.07, speed=3.0, phase=0.0, sway=0.0):
    m.base = m.get_center().copy()
    m.tm = phase

    def up(mm, dt):
        mm.tm += dt
        mm.move_to(mm.base + np.array([sway * np.sin(mm.tm * speed * 0.7), amp * np.sin(mm.tm * speed), 0]))
    m.add_updater(up)
    return m


def backed(text, size=28, color=TEXT):
    t = T(text, size, color)
    r = Rectangle(width=t.width + 0.3, height=t.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=0.9).move_to(t)
    return VGroup(r, t)


def arrow(a, b, color=TEXT, w=7, tip=0.22):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def pulse_arrow(a, color, direction, amp=0.12):
    a.base = a.get_center().copy()
    a.tm = 0.0
    d = np.array(direction, dtype=float)

    def up(m, dt):
        m.tm += dt
        m.move_to(m.base + d * amp * np.sin(m.tm * 3.2))
    a.add_updater(up)
    return a


def runner(pl, pts, color, period=7.0, phase=0.0, r=0.1):
    d = Dot(radius=r, color=color)
    d.tm = phase
    n = len(pts)

    def up(m, dt):
        m.tm += dt
        i = int((m.tm % period) / period * (n - 1))
        m.move_to(pl.P(*pts[i]))
    d.add_updater(up)
    up(d, 0)
    return d


class Plane:
    def __init__(self, ox=-5.3, oy=-2.65, W=11.7, H=5.4):
        self.ox, self.oy, self.W, self.H = ox, oy, W, H

    def P(self, x, y):
        return np.array([self.ox + x / XMAX * self.W, self.oy + y / YMAX * self.H, 0.0])

    def frame(self, xlab="teal numbers (N1)", ylab="orange numbers (N2)", size=28):
        ax = VGroup(Line(self.P(0, 0), self.P(XMAX, 0), color=GREY, stroke_width=4),
                    Line(self.P(0, 0), self.P(0, YMAX), color=GREY, stroke_width=4))
        xl = T(xlab, size, TC).move_to([self.ox + self.W / 2, self.oy - 0.8, 0])
        yl = T(ylab, size, OC).rotate(PI / 2).move_to([self.ox - 1.0, self.oy + self.H / 2, 0])
        return ax, xl, yl

    def seg(self, p0, p1, color, w=9):
        return Line(self.P(*p0), self.P(*p1), color=color, stroke_width=w)

    def trace(self, pts, color=TEXT, w=6, op=1.0):
        v = VMobject(color=color, stroke_width=w, stroke_opacity=op)
        v.set_points_as_corners([self.P(*p) for p in pts])
        return v

    def tick(self, x, text, color, below=True):
        t = T(text, 28, color)
        return t.next_to(self.P(x, 0), DOWN, buff=0.12) if below else t.next_to(self.P(0, x), LEFT, buff=0.12)


CLOCK = [0.0]


def _breath(op):
    return op * (1 + 0.45 * np.sin(CLOCK[0] * 2.0))


def _live(poly, op):
    poly.add_updater(lambda m: m.set_fill(opacity=_breath(op)))
    return poly


def shade_teal(pl, a12, op=0.2):
    (x0, y0), (x1, y1) = teal_pts(a12)
    pts = [(0, 0), (x0, y0), (x1, y1)] + ([(0, YMAX)] if y1 >= YMAX else [])
    return _live(Polygon(*[pl.P(*p) for p in pts], stroke_width=0, fill_color=TC, fill_opacity=_breath(op)), op)


def shade_orange(pl, a21, op=0.2):
    (x0, y0), (x1, y1) = orange_pts(a21)
    pts = [(0, 0), (x1, y1), (x0, y0)]
    if x1 >= XMAX:
        pts = [(0, 0), (XMAX, 0), (XMAX, y1), (x0, y0)]
    return _live(Polygon(*[pl.P(*p) for p in pts], stroke_width=0, fill_color=OC, fill_opacity=_breath(op)), op)


class PS(SpokenScene):
    def setup(self):
        super().setup()
        CLOCK[0] = 0.0
        c = Dot(radius=0.001, color=BG).move_to([0, -3.7, 0])
        c.add_updater(lambda m, dt: CLOCK.__setitem__(0, CLOCK[0] + dt))
        self.add(c)


class PN(NarratedScene):
    def setup(self):
        super().setup()
        CLOCK[0] = 0.0
        c = Dot(radius=0.001, color=BG).move_to([0, -3.7, 0])
        c.add_updater(lambda m, dt: CLOCK.__setitem__(0, CLOCK[0] + dt))
        self.add(c)


def ring_pulse(r):
    r.w0 = r.width
    r.tm = 0.0

    def up(m, dt):
        m.tm += dt
        m.set_width(m.w0 * (1 + 0.18 * np.sin(m.tm * 4)))
    r.add_updater(up)
    return r


def thin(pts, n=240):
    if len(pts) <= n:
        return pts
    idx = np.linspace(0, len(pts) - 1, n).astype(int)
    return [pts[i] for i in idx]


def bar_frame(y, width, h=0.7):
    return Rectangle(width=width, height=h, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([-6.0 + width / 2, y, 0])


def block_row(y, specs, h=0.6, x0=-6.0):
    g = VGroup()
    x = x0
    for w, c in specs:
        g.add(Rectangle(width=w - 0.05, height=h, stroke_width=0, fill_color=c, fill_opacity=0.95).move_to([x + w / 2, y, 0]))
        x += w
    return g


BAR_Y = -3.0
BAR2_Y = -1.6
DIAL_C = np.array([-3.6, 0.35, 0.0])
DIAL_R = 1.6


def make_dial(f_tracker, color=TC):
    arc = Arc(radius=DIAL_R, start_angle=0, angle=PI, color=GREY, stroke_width=6).move_arc_center_to(DIAL_C)
    base = Line(DIAL_C + LEFT * DIAL_R, DIAL_C + RIGHT * DIAL_R, color=GREY, stroke_width=4)
    needle = always_redraw(lambda: Line(DIAL_C, DIAL_C + DIAL_R * 0.88 * np.array([np.cos(PI * (1 - f_tracker.get_value())), np.sin(PI * (1 - f_tracker.get_value())), 0]),
                                       color=YELLOW, stroke_width=9))
    hub = Dot(DIAL_C, radius=0.1, color=YELLOW)
    lr = sym("r", "1", 30, color).move_to(DIAL_C + LEFT * DIAL_R + DOWN * 0.38)
    l0 = T("0", 30, TEXT).move_to(DIAL_C + RIGHT * DIAL_R + DOWN * 0.38)
    title = T("per-capita growth rate", 28, TEXT).move_to(DIAL_C + UP * (DIAL_R + 0.55))
    return VGroup(arc, base), needle, hub, VGroup(lr, l0), title


def creature_slots():
    return [np.array([0.9 + 1.45 * c, 0.55 + 1.5 * r, 0]) for r in range(2) for c in range(4)]


# =================================================================================================
class S00Title(TitleCard):
    LESSON = "Competition"
    TITLE = "Can It Grow When Rare?"


# -------------------------------------------------------------------------------------------------
class S01Question(PS):
    def construct(self):
        teal = VGroup(*[bob(creature(TC, 0.42).move_to([-5.2 + 1.2 * (i % 3), 0.2 + 1.25 * (i // 3), 0]), 0.07, 3, i, 0.1) for i in range(6)])
        orange = VGroup(*[bob(creature(OC, 0.42).move_to([2.2 + 1.2 * (i % 3), 0.2 + 1.25 * (i // 3), 0]), 0.07, 3, i + 1.3, 0.1) for i in range(6)])
        seeds = VGroup(*[Circle(radius=0.17, stroke_width=0, fill_color=GOLD, fill_opacity=0.95).move_to([-0.9 + 0.36 * (i % 6) + (0.18 if (i // 6) % 2 else 0), -1.6 + 0.3 * (i // 6), 0]) for i in range(18)])
        seed_l = T("one shared seed pile", 28, GOLD).move_to([0, -2.85, 0])
        self.at("two species")
        self.play(FadeIn(teal, lag_ratio=0.1), FadeIn(orange, lag_ratio=0.1), FadeIn(seeds), run_time=1.6)
        self.play(FadeIn(seed_l), run_time=0.6)
        # nibbling: creatures lean toward the pile and back
        self.at("twice as fast")
        gauge = Arc(radius=0.75, start_angle=PI, angle=-PI, color=GREY, stroke_width=6).move_to([-3.6, 2.9, 0])
        ndl = Line(gauge.get_center() + DOWN * 0.38, gauge.get_center() + DOWN * 0.38 + 0.65 * np.array([np.cos(2.4), np.sin(2.4), 0]), color=YELLOW, stroke_width=8)
        badge = VGroup(gauge, ndl)
        badge.move_to([-3.6, 2.85, 0])
        chipb = chip("growth rate ×2", TC, 28).move_to([-3.6, 3.55, 0])
        self.play(Create(gauge), run_time=0.6)
        self.play(Rotate(ndl, angle=-1.6, about_point=ndl.get_start()), FadeIn(chipb), run_time=1.0)
        self.at("must the faster")
        pod = chip("winner?", GOLD, 30).move_to([0, 1.3, 0])
        q = T("?", 110, YELLOW, weight=BOLD).move_to([0, 2.8, 0])
        self.play(FadeIn(pod, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(q, scale=1.4), run_time=0.7)
        self.at("this film builds")
        card = T("the test that decides", 34, YELLOW).move_to([0, -3.4, 0])
        self.play(FadeOut(seed_l), FadeIn(card), Indicate(q, color=YELLOW, scale_factor=1.15), run_time=1.2)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S02Room(PS):
    def construct(self):
        orange = VGroup(*[creature(OC, 0.42).move_to([2.2 + 1.2 * (i % 3), 0.2 + 1.25 * (i // 3), 0]) for i in range(6)])
        self.add(orange)
        self.wait(0.1)
        self.play(FadeOut(orange), run_time=0.7)
        # the teal creature area (left) and the curve (right)
        slots = [np.array([-5.4 + 1.3 * (i % 4), 2.4 - 1.3 * (i // 4), 0]) for i in range(8)]
        tcs = VGroup(*[bob(creature(TC, 0.4).move_to(s), 0.06, 3, i, 0.08) for i, s in enumerate(slots)])
        tr = ValueTracker(0)
        TMAX = 9.0
        ax0 = np.array([1.2, -1.1, 0])
        axes = VGroup(Line(ax0, ax0 + RIGHT * 5.2, color=GREY, stroke_width=4), Line(ax0, ax0 + UP * 4.0, color=GREY, stroke_width=4))
        xl = T("time", 28, GREY).move_to(ax0 + RIGHT * 2.6 + DOWN * 0.45)
        yl = T("teal numbers", 28, TC).rotate(PI / 2).move_to(ax0 + LEFT * 0.5 + UP * 2.0)

        def Nfun(t):
            return 1 / (1 + 9 * np.exp(-t))

        def curve():
            ts = np.linspace(0, max(tr.get_value(), 0.01), 60)
            v = VMobject(color=TC, stroke_width=7)
            v.set_points_as_corners([ax0 + np.array([t / TMAX * 5.2, Nfun(t) * 3.6, 0]) for t in ts])
            return v
        crv = always_redraw(curve)
        bar = bar_frame(BAR_Y, 12.0)
        blocks = block_row(BAR_Y, [(1.2, TC)] * 10)
        for i, b in enumerate(blocks):
            b.add_updater(lambda m, i=i: m.set_opacity(1.0 if Nfun(tr.get_value()) * 10 >= i + 0.5 else 0.0))
        for i, c in enumerate(tcs):
            c.add_updater(lambda m, i=i: m.set_opacity(1.0 if Nfun(tr.get_value()) * 8 >= i + 0.6 else 0.0))
        self.add(bar, blocks, tcs)
        self.play(Create(axes), FadeIn(xl), FadeIn(yl), FadeIn(bar), run_time=1.0)
        self.add(crv)
        self.at("its numbers rise")
        self.play(tr.animate.set_value(2.0), run_time=1.4, rate_func=linear)
        self.at("carrying capacity", nth=0)
        k_line = DashedLine(ax0 + UP * 3.6, ax0 + UP * 3.6 + RIGHT * 5.2, color=GOLD, stroke_width=4)
        self.add(k_line)
        k_lab = sym("K", "1", 34, GOLD).move_to(ax0 + UP * 3.6 + LEFT * 0.55)
        self.play(FadeIn(k_lab), tr.animate.set_value(5.5), run_time=2.2, rate_func=linear)
        self.at("settles at")
        self.play(tr.animate.set_value(TMAX), run_time=1.6, rate_func=linear)
        self.at("picture that capacity")
        lab = T("teal's room (K1)", 28, TC).move_to([-4.2, BAR_Y + 0.65, 0])
        tag = T("schematic", 22, GREY).move_to([5.2, BAR_Y + 0.62, 0])
        kk = DashedLine([6.0, BAR_Y - 0.4, 0], [6.0, BAR_Y + 0.4, 0], color=GOLD, stroke_width=5)
        self.play(FadeIn(lab), FadeIn(tag), Create(kk), run_time=0.8)
        self.play(Indicate(bar, color=GOLD, scale_factor=1.03), run_time=1.4)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S03Dial(PS):
    def construct(self):
        f = ValueTracker(0.0)
        bar = bar_frame(BAR_Y, 12.0)
        blocks = block_row(BAR_Y, [(1.2, TC)] * 10)
        for i, b in enumerate(blocks):
            b.add_updater(lambda m, i=i: m.set_opacity(float(np.clip((f.get_value() * 10 - i) * 2, 0, 1))))
        slots = creature_slots()
        tcs = VGroup(*[bob(creature(TC, 0.42).move_to(s), 0.06, 3, i, 0.08) for i, s in enumerate(slots)])
        for i, c in enumerate(tcs):
            c.add_updater(lambda m, i=i: m.set_opacity(float(np.clip(f.get_value() * 8 + 0.4 - i * 0.9 + 0.5, 0, 1))))
        lab = T("teal's room (K1)", 28, TC).move_to([-4.2, BAR_Y + 0.65, 0])
        dial_frame, needle, hub, dlabels, dtitle = make_dial(f)
        self.add(bar, blocks, lab, tcs)
        self.play(Create(dial_frame), FadeIn(needle), FadeIn(hub), FadeIn(dlabels), run_time=0.4)
        self.play(f.animate.set_value(0.45), run_time=3.5, rate_func=linear)
        self.at("per capita growth rate")
        self.play(FadeIn(dtitle), f.animate.set_value(0.7), run_time=2.3, rate_func=linear)
        self.at("reaches zero")
        self.play(f.animate.set_value(1.0), run_time=1.1, rate_func=linear)
        self.at("bar is full")
        z = Circle(radius=0.3, color=GREEN, stroke_width=6).move_to(DIAL_C + RIGHT * DIAL_R + DOWN * 0.38)
        self.play(Create(z), Indicate(bar, color=GREEN, scale_factor=1.03), run_time=1.2)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S04Alpha(PS):
    def construct(self):
        f = ValueTracker(0.6)
        bar = bar_frame(BAR_Y, 12.0)
        tblocks = block_row(BAR_Y, [(1.2, TC)] * 6)
        lab = T("teal's room (K1)", 28, TC).move_to([-4.2, BAR_Y + 0.65, 0])
        dial_frame, needle, hub, dlabels, dtitle = make_dial(f)
        o_slots = [np.array([0.9 + 1.4 * (i % 2), 0.6 + 1.5 * (i // 2), 0]) for i in range(4)]
        ocs = VGroup(*[bob(creature(OC, 0.42).move_to(s), 0.06, 3, i, 0.08) for i, s in enumerate(o_slots)])
        self.add(bar, tblocks, lab, dial_frame, needle, hub, dlabels, dtitle)
        self.at("now bring back orange")
        self.play(FadeIn(ocs, lag_ratio=0.25), run_time=1.6)
        x_next = -6.0 + 7.2
        oblocks = VGroup()
        cues = ["each orange individual", "takes some of", "teal's room", "room too"]
        for i, cue in enumerate(cues):
            self.at(cue)
            b = Rectangle(width=0.55, height=0.6, stroke_width=0, fill_color=OC, fill_opacity=0.95).move_to(o_slots[i] + DOWN * 0.1)
            oblocks.add(b)
            tgt = np.array([x_next + 0.3 + 0.6 * i, BAR_Y, 0])
            self.play(FadeIn(b, scale=0.5), run_time=0.15)
            self.play(b.animate.move_to(tgt), f.animate.set_value(0.6 + 0.05 * (i + 1)), run_time=0.5)
        self.at("a number called alpha")
        al = VGroup(sym("α", "12", 36, OC), T("= one orange block, in teal units", 28, TEXT)).arrange(RIGHT, buff=0.25)
        al.move_to([-1.0, BAR_Y + 1.45, 0])
        ptr = arrow(al.get_bottom() + DOWN * 0.05 + RIGHT * 1.0, oblocks[1].get_top() + UP * 0.05, OC, 5)
        self.play(FadeIn(al, shift=UP * 0.15), run_time=0.8)
        self.play(Create(ptr), run_time=0.7)
        self.at("counted in teal individuals")
        thin_b = Rectangle(width=0.25, height=0.55, stroke_width=0, fill_color=OC, fill_opacity=0.95).move_to([3.9, 2.35, 0])
        thick_b = Rectangle(width=1.0, height=0.55, stroke_width=0, fill_color=OC, fill_opacity=0.95).move_to([3.9, 1.35, 0])
        lt = T("small α", 28, TEXT).next_to(thin_b, RIGHT, buff=0.55)
        lk = T("large α", 28, TEXT).next_to(thick_b, RIGHT, buff=0.3)
        self.play(FadeIn(thin_b), FadeIn(lt), run_time=0.6)
        self.play(FadeIn(thick_b), FadeIn(lk), run_time=0.6)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S05Subscripts(PS):
    def construct(self):
        bar1 = bar_frame(BAR_Y, 12.0)
        b1 = VGroup(block_row(BAR_Y, [(1.2, TC)] * 6), block_row(BAR_Y, [(0.6, OC)] * 4, x0=-6.0 + 7.2))
        lab1 = T("teal's room (K1)", 28, TC).move_to([-4.2, BAR_Y + 0.65, 0])
        glow = Rectangle(width=12.4, height=3.6, stroke_width=0, fill_color=YELLOW, fill_opacity=0.08).move_to([0, 1.9, 0])
        glow.add_updater(lambda m: m.set_fill(opacity=0.08 + 0.06 * np.sin(CLOCK[0] * 2.2)))
        self.add(glow, bar1, b1, lab1)
        big = VGroup(T("α", 84, TEXT), T("1", 56, TEXT), T("2", 56, TEXT))
        big[1].next_to(big[0], RIGHT, buff=0.06).shift(DOWN * 0.2)
        big[2].next_to(big[1], RIGHT, buff=0.05)
        big.move_to([0, 2.3, 0])
        self.at("read the two numbers")
        self.play(FadeIn(big, scale=0.8), run_time=0.9)
        self.at("on then")
        on = T("ON", 30, TC).next_to(big[1], DOWN, buff=0.3).shift(LEFT * 0.55)
        self.play(big[1].animate.set_color(TC), FadeIn(on, shift=UP * 0.1), run_time=0.7)
        self.at("then from")
        fr = T("FROM", 30, OC).next_to(big[2], DOWN, buff=0.3).shift(RIGHT * 0.65)
        self.play(big[2].animate.set_color(OC), FadeIn(fr, shift=UP * 0.1), run_time=0.7)
        self.at("alpha one two")
        row1 = VGroup(creature(OC, 0.25), arrow(ORIGIN, RIGHT * 0.8, TEXT, 6, 0.18), creature(TC, 0.25),
                      VGroup(sym("α", "12", 32, TEXT), T(": ON species 1, FROM species 2", 28, TEXT)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.25)
        row1.move_to([0, 2.5, 0])
        self.play(FadeOut(on), FadeOut(fr), ReplacementTransform(big, row1), run_time=1.2)
        self.at("effect on species one")
        self.play(Indicate(row1[3], color=YELLOW, scale_factor=1.05), run_time=1.4)
        self.at("from species two")
        self.play(Indicate(row1[0], color=OC, scale_factor=1.3), run_time=1.2)
        self.at("orange has its own room bar")
        bar2 = bar_frame(BAR2_Y, 9.6)
        b2 = VGroup(block_row(BAR2_Y, [(1.2, OC)] * 5), block_row(BAR2_Y, [(0.6, TC)] * 4, x0=-6.0 + 6.0))
        lab2 = T("orange's room (K2)", 28, OC).move_to([-3.9, BAR2_Y + 0.65, 0])
        row2 = VGroup(creature(TC, 0.25), arrow(ORIGIN, RIGHT * 0.8, TEXT, 6, 0.18), creature(OC, 0.25),
                      VGroup(sym("α", "21", 32, TEXT), T(": ON species 2, FROM species 1", 28, TEXT)).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.25)
        row2.move_to([0, 1.2, 0])
        self.play(FadeIn(bar2), FadeIn(lab2), FadeIn(row2, shift=UP * 0.1), run_time=1.0)
        self.at("filled the same way")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.25) for b in b2[0]], lag_ratio=0.25), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.25) for b in b2[1]], lag_ratio=0.25), run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
def plane_base(scene, pl, with_teal=True, with_orange=False, a12=0.5, a21=0.5):
    ax, xl, yl = pl.frame()
    parts = {"ax": ax, "xl": xl, "yl": yl, "k1": pl.tick(K1, "K1", TC), "k2": pl.tick(K2, "K2", OC, below=False)}
    parts["tl"] = pl.seg(*teal_pts(a12), TC)
    parts["ol"] = pl.seg(*orange_pts(a21), OC)
    return parts


class S06Plane(PS):
    def construct(self):
        pl = Plane()
        bar1 = VGroup(bar_frame(BAR_Y, 12.0), block_row(BAR_Y, [(1.2, TC)] * 6), block_row(BAR_Y, [(0.6, OC)] * 4, x0=-6.0 + 7.2))
        bar2 = VGroup(bar_frame(BAR2_Y, 9.6), block_row(BAR2_Y, [(1.2, OC)] * 5), block_row(BAR2_Y, [(0.6, TC)] * 4, x0=0.0))
        self.add(bar1, bar2)
        self.wait(0.2)
        pr = plane_base(self, pl)
        panel = Rectangle(width=pl.W, height=pl.H, stroke_width=0, fill_color=GREY, fill_opacity=0.08).move_to(pl.P(XMAX / 2, YMAX / 2))
        panel.add_updater(lambda m: m.set_fill(opacity=0.07 + 0.05 * np.sin(CLOCK[0] * 2.0)))
        self.at("now plot both species")
        self.add(panel)
        self.play(bar1.animate.shift(DOWN * 1.2).set_opacity(0), bar2.animate.shift(DOWN * 2.0).set_opacity(0), Create(pr["ax"]), run_time=3.0)
        self.remove(bar1, bar2)
        self.at("teal numbers run across")
        self.play(FadeIn(pr["xl"]), FadeIn(pr["k1"]), run_time=0.8)
        self.at("orange numbers run up")
        self.play(FadeIn(pr["yl"]), run_time=0.8)
        self.at("the teal line marks")
        lab = T("teal isocline: teal growth = 0", 28, TC).move_to([0, 3.3, 0])
        self.play(Create(pr["tl"]), FadeIn(lab), run_time=2.4)
        self.at("on one side")
        left = VGroup(*[pulse_arrow(arrow(pl.P(x, y) + LEFT * 0.35, pl.P(x, y) + RIGHT * 0.35, TC, 7), TC, RIGHT) for x, y in [(12, 20), (12, 55), (12, 95), (40, 20)]])
        sh = shade_teal(pl, 0.5, 0.22)
        self.play(FadeIn(sh), FadeIn(left, lag_ratio=0.2), run_time=1.2)
        self.at("on the other")
        right = VGroup(*[pulse_arrow(arrow(pl.P(x, y) + RIGHT * 0.35, pl.P(x, y) + LEFT * 0.35, TC, 7), TC, LEFT) for x, y in [(125, 20), (125, 60), (70, 100), (150, 95)]])
        (a0, a1) = teal_pts(0.5)
        sh2 = Polygon(*[pl.P(*p) for p in [a0, (XMAX, 0), (XMAX, YMAX), a1]], stroke_width=0, fill_color=GREY, fill_opacity=0.18)
        self.play(FadeIn(sh2), FadeIn(right, lag_ratio=0.2), run_time=1.2)
        self.at("it shrinks")
        self.play(Indicate(right, color=YELLOW, scale_factor=1.1), run_time=1.2)
        self.finish()


class S07Orange(PS):
    def construct(self):
        pl = Plane()
        pr = plane_base(self, pl)
        lab = T("teal isocline: teal growth = 0", 28, TC).move_to([0, 3.3, 0])
        left = VGroup(*[pulse_arrow(arrow(pl.P(x, y) + LEFT * 0.35, pl.P(x, y) + RIGHT * 0.35, TC, 7), TC, RIGHT) for x, y in [(12, 20), (12, 55), (12, 95), (40, 20)]]).set_opacity(0.5)
        right = VGroup(*[pulse_arrow(arrow(pl.P(x, y) + RIGHT * 0.35, pl.P(x, y) + LEFT * 0.35, TC, 7), TC, LEFT) for x, y in [(125, 20), (125, 60), (70, 100), (150, 95)]]).set_opacity(0.5)
        self.add(shade_teal(pl, 0.5, 0.22), pr["ax"], pr["xl"], pr["yl"], pr["k1"], pr["tl"], lab, left, right)
        self.at("that line is teal's isocline")
        self.play(Indicate(pr["tl"], color=YELLOW, scale_factor=1.0), run_time=1.6)
        self.at("zero growth line")
        self.play(FadeOut(lab), FadeIn(pr["k2"]), run_time=0.8)
        self.at("orange gets one")
        lab2 = T("orange isocline: orange growth = 0", 28, OC).move_to([0, 3.3, 0])
        self.play(Create(pr["ol"]), FadeIn(lab2), FadeIn(shade_orange(pl, 0.5, 0.2)), run_time=2.0)
        ups = VGroup(*[pulse_arrow(arrow(pl.P(x, y) + DOWN * 0.3, pl.P(x, y) + UP * 0.3, OC, 7), OC, UP) for x, y in [(30, 10), (125, 6)]])
        downs = VGroup(*[pulse_arrow(arrow(pl.P(x, y) + UP * 0.3, pl.P(x, y) + DOWN * 0.3, OC, 7), OC, DOWN) for x, y in [(30, 105), (130, 75)]])
        self.play(FadeIn(ups), FadeIn(downs), run_time=1.0)
        self.at("where the two isoclines cross")
        cx, cy = cross(0.5, 0.5)
        ring = ring_pulse(Circle(radius=0.28, color=RING, stroke_width=6).move_to(pl.P(cx, cy)))
        self.play(FadeOut(left), FadeOut(right), FadeOut(lab2), Create(ring), run_time=1.2)
        self.at("neither species changes")
        nl = backed("neither changes", 28, RING).move_to(pl.P(cx, cy) + RIGHT * 0.9 + UP * 1.7)
        self.play(FadeIn(nl), run_time=0.6)
        self.at("is that crossing where they end up")
        q = T("?", 80, YELLOW, weight=BOLD).move_to(pl.P(cx, cy) + RIGHT * 0.9 + UP * 0.75)
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.play(Indicate(ring, color=YELLOW, scale_factor=1.6), run_time=1.0)
        self.finish()


# -------------------------------------------------------------------------------------------------
def banner(text, color=TEXT, size=30, y=3.3):
    return T(text, size, color).move_to([0, y, 0])


class S08Test(PS):
    def construct(self):
        pl = Plane()
        pr = plane_base(self, pl)
        cx, cy = cross(0.5, 0.5)
        ring = Circle(radius=0.28, color=RING, stroke_width=6, stroke_opacity=0.6).move_to(pl.P(cx, cy))
        self.add(shade_teal(pl, 0.5, 0.2), shade_orange(pl, 0.5, 0.2), pr["ax"], pr["xl"], pr["yl"], pr["k1"], pr["k2"], pr["tl"], pr["ol"], ring)
        self.at("here is the test")
        c1 = banner("the invasion test", YELLOW, 34)
        self.play(FadeIn(c1), run_time=0.8)
        self.at("shrink teal")
        d = Dot(pl.P(80, 40), radius=0.22, color=TC)
        self.play(FadeIn(d, scale=2), run_time=0.6)
        self.play(d.animate.move_to(pl.P(12, 80)), run_time=1.4)
        t1 = backed("teal rare", 28, TC).move_to(pl.P(12, 80) + DOWN * 0.7).align_to(pl.P(0, 0) + RIGHT * 0.35, LEFT)
        self.play(FadeIn(t1), run_time=0.4)
        self.at("orange sit at its own carrying capacity")
        o = backed("orange at K2", 28, OC).move_to(pl.P(12, 80) + DOWN * 1.25).align_to(pl.P(0, 0) + RIGHT * 0.35, LEFT)
        self.play(FadeIn(o), Indicate(pr["k2"], color=OC), run_time=0.8)
        self.at("can teal grow")
        d.base = d.get_center().copy()
        d.tm = 0.0
        d.add_updater(lambda m, dt: (setattr(m, "tm", m.tm + dt), m.move_to(m.base + RIGHT * 0.18 * (1 + np.sin(m.tm * 3)))))
        spot = Circle(radius=0.45, color=YELLOW, stroke_width=6).move_to(pl.P(12, 80))
        self.play(Create(spot), run_time=0.8)
        self.play(spot.animate.scale(1.5).set_stroke(opacity=0.3), run_time=1.2)
        self.at("this is the invasion test")
        card = VGroup(backed("can a rare species grow when its", 28, TEXT), backed("competitor is at carrying capacity?", 28, TEXT)).arrange(DOWN, buff=0.04).move_to([0, 2.95, 0])
        self.play(FadeOut(c1), FadeIn(card), run_time=0.8)
        self.play(spot.animate.scale(0.7).set_stroke(opacity=1.0), run_time=1.0)
        self.finish()


class S09Pass(PS):
    def construct(self):
        pl = Plane()
        pr = plane_base(self, pl)
        cx, cy = cross(0.5, 0.5)
        ring = ring_pulse(Circle(radius=0.28, color=RING, stroke_width=6).move_to(pl.P(cx, cy)))
        self.add(shade_teal(pl, 0.5, 0.2), shade_orange(pl, 0.5, 0.2), pr["ax"], pr["xl"], pr["yl"], pr["k1"], pr["k2"], pr["tl"], pr["ol"], ring)
        d1 = Dot(pl.P(12, 80), radius=0.16, color=TC)
        spot = Circle(radius=0.45, color=YELLOW, stroke_width=6).move_to(pl.P(12, 80))
        self.add(d1, spot)
        self.at("here teal's arrow points away from zero")
        a1 = arrow(pl.P(12, 80) + RIGHT * 0.35, pl.P(12, 80) + RIGHT * 1.7, TC, 9)
        self.play(GrowArrow(a1), run_time=1.2)
        self.at("so rare teal grows")
        tp = backed("teal passes", 30, GREEN).move_to(pl.P(12, 80) + RIGHT * 3.0 + UP * 0.35)
        self.play(FadeIn(tp), Indicate(a1, color=GREEN), run_time=1.2)
        self.at("swap")
        d2 = Dot(pl.P(100, 3), radius=0.16, color=OC)
        self.play(FadeOut(spot), FadeIn(d2, scale=2), run_time=0.8)
        a2 = arrow(pl.P(100, 3) + UP * 0.3, pl.P(100, 3) + UP * 1.5, OC, 9)
        self.at("rare orange grows too")
        self.play(GrowArrow(a2), run_time=1.0)
        op = backed("orange passes", 30, GREEN).move_to(pl.P(100, 3) + UP * 2.0 + RIGHT * 1.5)
        self.play(FadeIn(op), run_time=0.6)
        self.at("both pass")
        st = banner("both pass → stable coexistence", GREEN, 34)
        self.play(FadeIn(st), Indicate(ring, color=GREEN, scale_factor=1.8), run_time=1.2)
        self.at("every path that starts")
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(tp), FadeOut(op), run_time=0.6)
        starts = [(10, 100), (15, 12), (150, 15), (135, 100), (70, 112), (120, 50)]
        paths = [sim(0.5, 0.5, *s) for s in starts]
        traces = [pl.trace(p, TEXT, 4) for p in paths]
        for p in paths:
            assert np.hypot(p[-1][0] - cx, p[-1][1] - cy) < 1.5
        self.play(*[Create(t) for t in traces], run_time=2.6, rate_func=linear)
        self.at("flows into the crossing")
        runs = [runner(pl, thin(p, 120), YELLOW, 4.0, i * 0.5) for i, p in enumerate(paths)]
        for r in runs:
            self.add(r)
        self.play(Indicate(ring, color=YELLOW, scale_factor=1.8), run_time=1.0)
        self.at("they coexist stably")
        ax_p = pl.trace([(20, 0), (K1, 0)], GREY, 5, 0.8)
        zl = T("zero stays zero", 24, GREY).move_to(pl.P(60, 0) + UP * 0.3)
        self.play(Create(ax_p), FadeIn(zl), run_time=1.4)
        self.finish()


class S10Fail(PS):
    def construct(self):
        pl = Plane()
        pr = plane_base(self, pl)
        a21 = ValueTracker(0.5)
        cx, cy = cross(0.5, 0.5)
        ring = ring_pulse(Circle(radius=0.28, color=RING, stroke_width=6).move_to(pl.P(cx, cy)))
        oline = always_redraw(lambda: pl.seg(*orange_pts(a21.get_value()), OC))
        self.add(shade_teal(pl, 0.5, 0.2), always_redraw(lambda: shade_orange(pl, a21.get_value(), 0.2)), pr["ax"], pr["xl"], pr["yl"], pr["k1"], pr["k2"], pr["tl"], oline, ring)
        self.at("now make teal hurt orange more")
        hurt = VGroup(sym("α", "21", 34, OC), T("up", 34, OC)).arrange(RIGHT, buff=0.2).move_to([0, 3.3, 0])
        self.play(FadeIn(hurt), run_time=0.8)
        self.at("orange's line tilts")
        self.play(a21.animate.set_value(1.5), FadeOut(ring), run_time=2.6)
        pr["k2"]  # K2 intercept stays put
        self.at("rare orange among a full teal population")
        d2 = Dot(pl.P(100, 3), radius=0.16, color=OC)
        a2 = arrow(pl.P(100, 3) + UP * 0.25, pl.P(100, 3) + DOWN * 0.0 + UP * 0.25, OC)
        a2 = arrow(pl.P(100, 3) + UP * 1.3, pl.P(100, 3) + UP * 0.2, OC, 9)
        self.play(FadeIn(d2, scale=2), run_time=0.6)
        self.play(GrowArrow(a2), run_time=1.0)
        self.at("now shrinks")
        of = backed("orange fails", 30, RED).move_to(pl.P(100, 3) + UP * 1.75 + RIGHT * 0.3)
        self.play(FadeIn(of), run_time=0.6)
        self.at("teal passes orange fails")
        starts = [(10, 100), (15, 12), (130, 100), (60, 110), (110, 50), (20, 60)]
        paths = [sim(0.5, 1.5, *s) for s in starts]
        traces = [pl.trace(p, TEXT, 4) for p in paths]
        inset = Rectangle(width=2.9, height=1.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([5.1, 1.6, 0])
        tcs = VGroup(*[bob(creature(TC, 0.24).move_to([4.2 + 0.7 * i, 1.35 + 0.0, 0]), 0.05, 3, i) for i in range(3)])
        ocs = VGroup(*[bob(creature(OC, 0.24).move_to([4.2 + 0.7 * i, 1.95, 0]), 0.05, 3, i + 1) for i in range(3)])
        self.play(FadeOut(a2), FadeOut(of), run_time=0.5)
        self.play(FadeOut(hurt), FadeIn(inset), FadeIn(tcs), FadeIn(ocs), *[Create(t) for t in traces], run_time=1.9, rate_func=linear)
        runs = [runner(pl, thin(p, 120), YELLOW, 4.0, i * 0.5) for i, p in enumerate(paths)]
        for r in runs:
            self.add(r)
        self.at("orange slides to zero")
        self.play(FadeOut(ocs, lag_ratio=0.3), run_time=1.8)
        self.at("teal excludes it")
        st = banner("one passes → it excludes the other, here", RED, 32)
        self.play(FadeIn(st), run_time=0.8)
        self.finish()


class S11Neither(PS):
    def construct(self):
        pl = Plane()
        pr = plane_base(self, pl)
        a12 = ValueTracker(0.5)
        tline = always_redraw(lambda: pl.seg(*teal_pts(a12.get_value()), TC))
        oline = pl.seg(*orange_pts(1.5), OC)
        self.add(always_redraw(lambda: shade_teal(pl, a12.get_value(), 0.2)), shade_orange(pl, 1.5, 0.2), pr["ax"], pr["xl"], pr["yl"], pr["k1"], pr["k2"], tline, oline)
        self.at("cross the lines the other way")
        self.play(a12.animate.set_value(1.5), run_time=2.0)
        self.at("neither passes")
        d1 = Dot(pl.P(14, 80), radius=0.15, color=TC)
        a1 = arrow(pl.P(14, 80) + LEFT * 0.25, pl.P(14, 80) + LEFT * 1.1, TC, 8)
        d2 = Dot(pl.P(100, 3), radius=0.15, color=OC)
        a2 = arrow(pl.P(100, 3) + UP * 0.9, pl.P(100, 3) + UP * 0.05, OC, 8)
        self.play(FadeIn(d1), FadeIn(d2), GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        st1 = banner("neither passes → the start decides", YELLOW, 32)
        self.play(FadeIn(st1), run_time=0.6)
        self.at("each species wins from some starts")
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(d1), FadeOut(d2), run_time=0.3)
        starts = [(60, 20), (40, 10), (90, 60), (10, 40), (30, 80), (60, 80), (120, 30), (20, 100)]
        paths = [sim(1.5, 1.5, *s) for s in starts]
        ends = [("K1" if p[-1][0] > 50 else "K2") for p in paths]
        assert "K1" in ends and "K2" in ends, ends
        cols = [TC if e == "K1" else OC for e in ends]
        traces = [pl.trace(p, c, 5) for p, c in zip(paths, cols)]
        self.play(*[Create(t) for t in traces], run_time=1.8, rate_func=linear)
        runs = [runner(pl, thin(p, 120), TEXT, 4.0, i * 0.5, 0.08) for i, p in enumerate(paths)]
        for r in runs:
            self.add(r)
        self.at("so the starting numbers decide")
        sx = separatrix(1.5, 1.5)
        dash = DashedVMobject(pl.trace(sx, YELLOW, 6), num_dashes=40)
        dl = backed("dividing line (not equal numbers)", 28, YELLOW).move_to(pl.P(115, 112))
        self.play(Create(dash), FadeIn(dl), run_time=1.6)
        self.finish()


class S12Predict(PS):
    def construct(self):
        pl = Plane()
        pr = plane_base(self, pl)
        cx, cy = cross(0.5, 0.5)
        ring = ring_pulse(Circle(radius=0.28, color=RING, stroke_width=6).move_to(pl.P(cx, cy)))
        self.add(shade_teal(pl, 0.5, 0.2), shade_orange(pl, 0.5, 0.2), pr["ax"], pr["xl"], pr["yl"], pr["k1"], pr["k2"], pr["tl"], pr["ol"], ring)
        starts = [(10, 100), (15, 12), (150, 15), (135, 78), (70, 105), (120, 50)]
        sd = VGroup(*[Dot(pl.P(*s), radius=0.11, color=TEXT) for s in starts])
        self.at("back to the pair that coexist")
        self.play(FadeIn(sd, lag_ratio=0.2), Indicate(ring, color=GREEN, scale_factor=1.8), run_time=1.6)
        self.at("now double orange's growth rate")
        inset = Rectangle(width=5.2, height=1.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([4.1, 2.0, 0])
        oc = bob(creature(OC, 0.36).move_to([2.2, 2.0, 0]), 0.06, 3)
        badge = chip("orange growth ×2", OC, 28).move_to([8.0, 2.0, 0])
        self.play(FadeIn(inset), FadeIn(oc), run_time=0.6)
        self.play(badge.animate.move_to([4.9, 2.0, 0]).scale(0.85), run_time=1.6)
        self.at("change nothing else")
        for dd in sd:
            self.play(Indicate(dd, color=YELLOW, scale_factor=2.0), run_time=0.25)
        self.at("does the ending change")
        q = T("Same ending?", 38, YELLOW, weight=BOLD).move_to([-2.5, 3.3, 0])
        self.play(FadeIn(q), Indicate(ring, color=YELLOW, scale_factor=2.0), run_time=1.2)
        self.finish()


class S13Pause(PN):
    def construct(self):
        pl = Plane()
        pr = plane_base(self, pl)
        cx, cy = cross(0.5, 0.5)
        ring = ring_pulse(Circle(radius=0.28, color=RING, stroke_width=6).move_to(pl.P(cx, cy)))
        starts = [(10, 100), (15, 12), (150, 15), (135, 78), (70, 105), (120, 50)]
        sd = VGroup(*[Dot(pl.P(*s), radius=0.11, color=TEXT) for s in starts])
        grp = VGroup(shade_teal(pl, 0.5, 0.2), shade_orange(pl, 0.5, 0.2), pr["ax"], pr["xl"], pr["yl"], pr["k1"], pr["k2"], pr["tl"], pr["ol"], ring, sd).set_opacity(0.45)
        q = T("Same ending, or a new one?", 46, YELLOW, weight=BOLD).move_to([0, 3.3, 0])
        card = backed("orange growth ×2, nothing else changed", 28, OC).move_to([0, 2.55, 0])
        cd = ValueTracker(1.0)
        c0 = np.array([5.6, 3.2, 0])
        ringc = always_redraw(lambda: Arc(radius=0.35, start_angle=PI / 2, angle=-TAU * max(cd.get_value(), 0.001), color=YELLOW, stroke_width=8).move_arc_center_to(c0))
        self.add(grp, q, ringc)
        self.play(FadeIn(card), run_time=0.5)
        self.play(cd.animate.set_value(0.0), run_time=4.4, rate_func=linear)
        self.finish()


# -------------------------------------------------------------------------------------------------
class S14Reveal(PS):
    def construct(self):
        W, H = 5.6, 4.8
        pls = [Plane(-6.3, -3.1, W, H), Plane(0.7, -3.1, W, H)]
        cx, cy = cross(0.5, 0.5)
        grp = VGroup()
        for pl in pls:
            ax, _, _ = pl.frame()
            grp.add(shade_teal(pl, 0.5, 0.2), shade_orange(pl, 0.5, 0.2), ax, pl.seg(*teal_pts(0.5), TC, 6), pl.seg(*orange_pts(0.5), OC, 6),
                    Circle(radius=0.2, color=RING, stroke_width=5).move_to(pl.P(cx, cy)))
        t1 = T("original", 30, TEXT).move_to([-3.5, 2.0, 0])
        t2 = T("orange growth ×2", 30, OC).move_to([3.5, 2.0, 0])
        starts = [(10, 100), (15, 12), (150, 20)]
        P1 = [sim(0.5, 0.5, *s, r2=R2, T=40, dt=0.02, step=5) for s in starts]
        P2 = [sim(0.5, 0.5, *s, r2=2 * R2, T=40, dt=0.02, step=5) for s in starts]
        self.add(grp, t1, t2)
        sim_t = ValueTracker(0.0)
        dts = 0.1  # seconds of model time per sample (step 5 * dt 0.02)

        def mk(pl, paths, col):
            out = VGroup()
            for p in paths:
                out.add(always_redraw(lambda p=p, pl=pl: pl.trace(p[:max(2, int(sim_t.get_value() / dts))], col, 5)))
                d = Dot(radius=0.1, color=YELLOW)
                d.add_updater(lambda m, p=p, pl=pl: m.move_to(pl.P(*p[min(int(sim_t.get_value() / dts), len(p) - 1)])))
                out.add(d)
            return out
        trs = mk(pls[0], P1, TEXT)
        trs2 = mk(pls[1], P2, OC)
        starts_d = VGroup(*[Dot(pl.P(*s), radius=0.1, color=TEXT) for pl in pls for s in starts])
        self.add(starts_d)
        self.at("the ending stays put")
        ni = T("isoclines do not move", 28, TEXT).move_to([0, 3.3, 0])
        self.play(FadeIn(ni), run_time=0.8)
        self.at("orange moves faster")
        self.remove(starts_d)
        self.add(trs, trs2)
        self.play(sim_t.animate.set_value(30), run_time=3.0, rate_func=linear)
        self.at("but they still finish at the same crossing")
        for pl in pls:
            pass
        self.play(*[Indicate(grp[5 + 6 * i], color=YELLOW, scale_factor=2.0) for i in range(2)], run_time=1.0)
        self.at("here growth rate changes the route")
        lab = T("r changes speed and path, not the ending", 32, YELLOW).move_to([0, 3.3, 0])
        self.play(FadeOut(ni), FadeIn(lab), run_time=0.8)
        self.at("not the outcome")
        sim_t.set_value(0)
        self.play(sim_t.animate.set_value(30), run_time=4.4, rate_func=linear)
        self.finish()


class S15Words(PS):
    def construct(self):
        s = 0.09
        y1, y2 = 1.2, -1.2
        bar1 = Rectangle(width=K1 * s, height=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([-6.0 + K1 * s / 2, y1, 0])
        bar2 = Rectangle(width=K2 * s, height=0.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([-6.0 + K2 * s / 2, y2, 0])
        l1 = T("teal's room (K1)", 28, TC).move_to([-6.0 + 1.9, y1 + 0.75, 0])
        l2 = T("orange's room (K2)", 28, OC).move_to([-6.0 + 2.1, y2 + 0.75, 0])
        self.at("in words")
        self.play(FadeIn(bar1), FadeIn(bar2), FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.at("each species must limit itself")
        rule = T("each limits itself more than it limits the other", 30, YELLOW).move_to([0, 3.2, 0])
        self.play(FadeIn(rule, shift=DOWN * 0.1), run_time=1.0)
        self.at("limits means")
        sl_t1 = Rectangle(width=0.55, height=0.8, stroke_width=0, fill_color=TC, fill_opacity=1).move_to([-6.0 + 0.275, y1, 0])
        sl_t2 = Rectangle(width=0.275, height=0.8, stroke_width=0, fill_color=TC, fill_opacity=1).move_to([-6.0 + 0.1375, y2, 0])
        c1 = T("1/K1 of teal's room", 28, TC).move_to([-0.2, y1 - 0.8, 0]).align_to(bar1, LEFT)
        c2 = VGroup(sym("α", "21", 30, TC), T("/K2 of orange's room", 28, TC)).arrange(RIGHT, buff=0.08).move_to([0, y2 - 0.8, 0]).align_to(bar2, LEFT)
        self.play(FadeIn(sl_t1), FadeIn(c1), run_time=0.8)
        self.play(FadeIn(sl_t2), FadeIn(c2), run_time=0.8)
        self.at("one individual fills")
        cmp1 = VGroup(T("1/K1 > ", 34, TC), sym("α", "21", 34, TC), T("/K2", 34, TC)).arrange(RIGHT, buff=0.04).scale_to_fit_width(3.2).move_to([5.1, 1.2, 0])
        ok1 = T("teal passes ✓", 30, GREEN).move_to([3.4, -3.3, 0])
        self.play(FadeIn(cmp1), run_time=0.6)
        sl_o1 = Rectangle(width=0.55, height=0.8, stroke_width=0, fill_color=OC, fill_opacity=1).move_to([-6.0 + 0.275, y2, 0]).shift(RIGHT * 1.2)
        sl_o2 = Rectangle(width=0.275, height=0.8, stroke_width=0, fill_color=OC, fill_opacity=1).move_to([-6.0 + 0.1375, y1, 0]).shift(RIGHT * 1.2)
        cmp2 = VGroup(T("1/K2 > ", 34, OC), sym("α", "12", 34, OC), T("/K1", 34, OC)).arrange(RIGHT, buff=0.04).scale_to_fit_width(3.2).move_to([5.1, -1.2, 0])
        self.play(FadeIn(sl_o1), FadeIn(sl_o2), FadeIn(cmp2), FadeIn(ok1), run_time=0.8)
        ok2 = T("orange passes ✓", 30, GREEN).move_to([-2.6, -3.3, 0])
        self.play(FadeIn(ok2), run_time=0.5)
        self.finish()


class S16Close(PS):
    def construct(self):
        pl = Plane()
        pr = plane_base(self, pl)
        cx, cy = cross(0.5, 0.5)
        ring = ring_pulse(Circle(radius=0.28, color=RING, stroke_width=6).move_to(pl.P(cx, cy)))
        starts = [(10, 100), (15, 12), (150, 15), (135, 100)]
        paths = [sim(0.5, 0.5, *s) for s in starts]
        trs = VGroup(*[pl.trace(p, TEXT, 4) for p in paths])
        big = VGroup(shade_teal(pl, 0.5, 0.2), shade_orange(pl, 0.5, 0.2), pr["ax"], pr["tl"], pr["ol"], ring, trs)
        self.add(big)
        bigruns = [runner(pl, thin(p, 120), YELLOW, 4.0, i * 0.7) for i, p in enumerate(paths)]
        self.add(*bigruns)
        for m in big.family_members_with_points():
            m.clear_updaters()
        small = Plane(-6.4, -3.2, 5.6, 4.2)
        sm = VGroup(shade_teal(small, 0.5, 0.2), shade_orange(small, 0.5, 0.2), small.frame()[0], small.seg(*teal_pts(0.5), TC, 5), small.seg(*orange_pts(0.5), OC, 5),
                    Circle(radius=0.18, color=RING, stroke_width=4).move_to(small.P(cx, cy)),
                    *[small.trace(p, TEXT, 3) for p in paths])
        self.at("so the whole verdict")
        self.play(FadeOut(big), *[FadeOut(r) for r in bigruns], FadeIn(sm), run_time=1.0)
        for r in bigruns:
            r.clear_updaters()
            self.remove(r)
        sruns = [runner(small, thin(p, 120), YELLOW, 4.0, i * 0.7, 0.07) for i, p in enumerate(paths)]
        for r in sruns:
            self.add(r)
        ch1 = chip("both pass: coexist", GREEN, 30).move_to([2.9, 0.9, 0])
        ch2 = chip("one passes: exclusion here", RED, 30).move_to([2.9, -0.7, 0])
        ch3 = chip("neither: start decides", YELLOW, 30).move_to([2.9, -2.3, 0])
        self.play(FadeIn(ch1, shift=LEFT * 0.3), run_time=0.5)
        self.at("one question")
        self.play(FadeIn(ch2, shift=LEFT * 0.3), run_time=0.7)
        self.at("asked of each species")
        self.play(FadeIn(ch3, shift=LEFT * 0.3), run_time=0.7)
        self.at("can it grow when rare")
        q = T("Can it grow when rare?", 54, YELLOW, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.play(Write(q), run_time=1.6)
        self.at("beside a competitor")
        for c in (ch1, ch2, ch3):
            self.play(Indicate(c, scale_factor=1.08), run_time=0.5)
        self.finish()


class S17End(EndCard):
    LINE = "In this model, both coexist stably when each can grow when rare."
