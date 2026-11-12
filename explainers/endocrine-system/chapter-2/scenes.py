"""How Fast a Level Follows (chapter 2, endocrine system). Same colour map as chapter 1.

COLOUR MAP (one colour per concept, whole film)
  ORANGE = secretion (the gland tap, hormone dots)
  TEAL   = hormone level (water line in the plasma tank)
  GREY   = clearance (the drain: all removal and breakdown)
  RED    = negative feedback (dashed arrow from the level back to the tap)
  animals = charcoal-grey silhouettes
Everything that moves is computed: the tank obeys dL/dt = r (a - k L); the feedback loop uses
a = base / (1 + (L/K)^3) (a schematic Hill-type brake); the daily trace is the tank's own response.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F28C28"
BIRDC = "#7C8591"
COMBC = "#B9C2CC"
VESS = "#B0524A"
CELLC = "#6EA8FE"
NERVEC = GOLD
LESSON_TITLE = "Hormones and the Endocrine System"


def v3(p):
    p = np.array(p, float)
    return np.array([p[0], p[1], 0.0])


def clip(x, a, b):
    return max(a, min(b, x))


def gate(L, K=0.55):
    return 1.0 / (1.0 + (L / K) ** 3)


def P3(x, y, z=0.0):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ moving dots along a path
class Flow(VGroup):
    """Dots streaming along a polyline; .amount sets how many/how big (0 = off)."""

    def __init__(self, pts, color=ORANGE, spacing=0.42, speed=1.5, r=0.11):
        super().__init__()
        self.pts = [v3(p) for p in pts]
        self.color, self.sp, self.speed, self.r = color, spacing, speed, r
        self.amount, self.phase = 0.0, 0.0
        self.add_updater(lambda m, dt: m._step(dt))

    def _step(self, dt):
        self.phase += dt * self.speed
        P = self.pts
        seg = [float(np.linalg.norm(P[i + 1] - P[i])) for i in range(len(P) - 1)]
        tot = sum(seg)
        if self.amount < 0.03 or tot < 0.05:
            self.submobjects = []
            return
        n = int(tot / self.sp) + 1
        rad = 0.04 + (self.r - 0.04) * clip(self.amount, 0, 1.3)
        dots = []
        for i in range(n):
            s = (self.phase + i * self.sp) % (n * self.sp)
            if s > tot:
                continue
            acc = 0.0
            p = P[-1]
            for j, l in enumerate(seg):
                if s <= acc + l:
                    p = P[j] + (P[j + 1] - P[j]) * ((s - acc) / max(l, 1e-6))
                    break
                acc += l
            dots.append(Dot(p, radius=rad, color=self.color))
        self.submobjects = dots


def polyline(pts, color, width, opacity=1.0):
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    m.set_points_as_corners([v3(p) for p in pts])
    return m


def dpath(pts, color=RED, width=6, tee=True):
    """Dashed polyline with an inhibition bar at the end."""
    g = VGroup()
    for a, b in zip(pts[:-1], pts[1:]):
        g.add(DashedLine(P3(*a), P3(*b), dash_length=0.2, dashed_ratio=0.55, stroke_width=width, color=color))
    if tee:
        a, b = v3(pts[-2])[:2], v3(pts[-1])[:2]
        d = (b - a) / np.linalg.norm(b - a)
        perp = np.array([-d[1], d[0]])
        g.add(Line(P3(*(b + perp * 0.3)), P3(*(b - perp * 0.3)), stroke_width=width + 2, color=color))
    return g


# ------------------------------------------------------------------ the plasma tank
class Tank:
    """Blood as a tank. dL/dt = r (a - k L) + inj; a = adr * base * (1 - f + f gate(L)).
    All the pictures (water, stream thickness, arrow lengths, tap handle) read these numbers."""

    def __init__(s, sc, cx=0.5, cy=-0.2, w=3.2, h=4.0, pipe=None, arrows=True, handle=True,
                 L=0.0, base=0.0, f=0.0, adr=1.0, k=1.0, r=0.3, gapw=0.27):
        s.sc, s.cx, s.cy, s.w, s.h, s.r = sc, cx, cy, w, h, r
        s.top, s.bot, s.l, s.rt = cy + h / 2, cy - h / 2, cx - w / 2, cx + w / 2
        s.Lt, s.base, s.f, s.adr, s.k, s.inj = (ValueTracker(v) for v in (L, base, f, adr, k, 0.0))
        s.run, s.t, s.a, s.D = True, 0.0, 0.0, 0.0
        s.dashed, s.show_in, s.show_out, s.handle_on = False, False, False, handle
        s.nx, s.ny = cx - 0.6, s.top + 0.35
        s.pipe = pipe or [(cx - 3.4, s.ny), (s.nx, s.ny)]
        gap = gapw
        s.drain_ov = None
        fr = VMobject(stroke_color=TEXT, stroke_width=6, fill_opacity=0)
        fr.set_points_as_corners([P3(s.l, s.top), P3(s.l, s.bot), P3(cx - gap, s.bot)])
        fr.start_new_path(P3(cx + gap, s.bot))
        fr.add_points_as_corners([P3(s.rt, s.bot), P3(s.rt, s.top)])
        s.frame = fr
        s.stub = VGroup(Line(P3(cx - gap, s.bot), P3(cx - gap, s.bot - 0.4), stroke_width=6, color=GREY),
                        Line(P3(cx + gap, s.bot), P3(cx + gap, s.bot - 0.4), stroke_width=6, color=GREY))
        body = polyline(list(s.pipe) + [(s.nx, s.ny - 0.28)], ORANGE, 16, 0.45)
        s.tap = VGroup(body)
        s.water = Polygon(P3(0, 0), P3(1, 0), P3(1, 1), color=TEAL, fill_color=TEAL, fill_opacity=0.5, stroke_width=0)
        s.surf = VMobject(stroke_color=TEAL, stroke_width=7, fill_opacity=0)
        s.arr = VGroup()
        s.lever = VGroup()
        s.live = VGroup(s.water, s.surf, s.arr, s.lever)
        s.tapflow = Flow(list(s.pipe) + [(s.nx, s.bot + 1)], ORANGE)
        s.drainflow = Flow([(cx, s.bot - 0.4), (cx, s.bot - 0.95)], GREY, spacing=0.34)
        s.live.add_updater(lambda m, dt: s.step(dt))
        s.step(0.0)

    def parts(s):
        return [s.live, s.tapflow, s.drainflow]

    def surf_y(s):
        return s.bot + 0.06 + clip(s.Lt.get_value(), 0, 1) * (s.h - 0.12)

    def step(s, dt):
        L, k = s.Lt.get_value(), s.k.get_value()
        base, f = s.base.get_value(), s.f.get_value()
        s.D = base * (1 - f + f * gate(L))
        s.a = s.adr.get_value() * s.D
        if s.run and dt > 0:
            L = clip(L + (s.r * (s.a - k * L) + s.inj.get_value()) * dt, 0, 1)
            s.Lt.set_value(L)
        s.t += dt
        sy = s.surf_y()
        H = sy - (s.bot + 0.06)
        x0, x1 = s.l + 0.06, s.rt - 0.06
        if H > 0.02:
            s.water.set_points_as_corners([P3(x0, s.bot + 0.06), P3(x1, s.bot + 0.06), P3(x1, sy), P3(x0, sy), P3(x0, s.bot + 0.06)])
            xs = np.linspace(x0, x1, 26)
            wave = [P3(x, sy + 0.035 * math.sin(3.2 * x + 2.5 * s.t)) for x in xs]
            s.water.set_fill(TEAL, 0.5)
            s.surf.clear_points()
            if s.dashed:
                for i in range(0, 25, 2):
                    s.surf.start_new_path(wave[i])
                    s.surf.add_points_as_corners(wave[i + 1:i + 2])
            else:
                s.surf.set_points_as_corners(wave)
        else:
            s.water.set_fill(TEAL, 0)
            s.surf.clear_points()
        s.tapflow.pts = [v3(p) for p in list(s.pipe) + [(s.nx, max(sy, s.bot + 0.1))]]
        s.tapflow.amount = s.a / 0.9
        s.drainflow.amount = (k * L / 0.9) if s.drain_ov is None else s.drain_ov
        # arrows (in / out) and the tap handle
        s.arr.submobjects = []
        if s.show_in and s.a * 2.6 > 0.12:
            s.arr.add(Arrow(P3(s.rt + 0.15 + 2.6 * s.a, s.cy + 0.9), P3(s.rt + 0.15, s.cy + 0.9), buff=0, color=ORANGE, stroke_width=9, tip_length=0.3))
        if s.show_out and k * L * 2.6 > 0.12:
            s.arr.add(Arrow(P3(s.rt + 0.15, s.cy - 0.9), P3(s.rt + 0.15 + 2.6 * k * L, s.cy - 0.9), buff=0, color=GREY, stroke_width=9, tip_length=0.3))
        s.lever.submobjects = []
        if s.handle_on:
            op = clip(s.a / 0.9, 0, 1)
            th = (math.pi / 2) * (1 - op)
            px, py = s.cx - 1.9, s.ny
            s.lever.add(Line(P3(px, py), P3(px + 0.7 * math.cos(th), py + 0.7 * math.sin(th)), stroke_width=11, color=TEXT),
                        Dot(P3(px, py), radius=0.14, color=TEXT))



# ================================================================== chapter 2 helpers
TEAL_L = "#8FE3E8"      # same concept (hormone level), lighter stroke for a second curve
LESSON_TITLE_2 = LESSON_TITLE


class Pn:
    """Maps data coordinates (x in 0..xmax, y in 0..ymax) onto a screen rectangle."""

    def __init__(s, x0, x1, y0, y1, xmax, ymax):
        s.x0, s.x1, s.y0, s.y1, s.xmax, s.ymax = x0, x1, y0, y1, xmax, ymax

    def pt(s, x, y):
        return P3(s.x0 + (s.x1 - s.x0) * x / s.xmax, s.y0 + (s.y1 - s.y0) * y / s.ymax)


def clock(sc, knots, tr=None):
    """A ValueTracker that follows scene time through (time, value) knots, linearly."""
    xs = [k[0] for k in knots]
    ys = [k[1] for k in knots]
    tr = tr or ValueTracker(ys[0])
    d = Mobject()
    d.add_updater(lambda m: tr.set_value(float(np.interp(sc.renderer.time, xs, ys))))
    sc.add(d)
    return tr


def driver(sc, fn):
    d = Mobject()
    d.add_updater(lambda m: fn(sc.renderer.time))
    sc.add(d)
    return d


def trace_pts(pn, pts, tr, color=TEAL, w=7, opacity=1.0, fill=None):
    """A curve drawn from computed data points up to the tracker's x (live)."""
    xs = np.array([p[0] for p in pts])
    ys = np.array([p[1] for p in pts])
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=opacity, fill_opacity=0)

    def upd(mm):
        x = float(tr.get_value())
        i = int(np.searchsorted(xs, x, side="right"))
        if i < 1:
            mm.clear_points()
            return
        px = list(xs[:i])
        py = list(ys[:i])
        if i < len(xs) and xs[i] > xs[i - 1] + 1e-9 and x > xs[i - 1]:
            f = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            px.append(x)
            py.append(ys[i - 1] + f * (ys[i] - ys[i - 1]))
        if len(px) < 2:
            mm.clear_points()
            return
        mm.set_points_as_corners([pn.pt(a, b) for a, b in zip(px, py)])
    m.add_updater(upd)
    upd(m)
    return m


def static_pts(pn, pts, color=TEAL, w=7, opacity=1.0):
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=opacity, fill_opacity=0)
    m.set_points_as_corners([pn.pt(a, b) for a, b in pts])
    return m


def curve_pts(fn, x0, x1, n=160):
    return [(float(x), float(fn(x))) for x in np.linspace(x0, x1, n)]


def tag(text, pos, color=TEXT, size=30, **kw):
    return T(text, size, color, **kw).move_to(P3(*pos))


def power_label(prefix, base, exp, suffix, size=28, color=TEAL):
    """'prefix 2^(exp) suffix' with a raised, smaller exponent (never a caret)."""
    a = T(prefix + base, size, color)
    e = T(exp, int(size * 0.62), color)
    b = T(suffix, size, color)
    e.next_to(a, RIGHT, buff=0.04).shift(UP * a.height * 0.45)
    b.next_to(e, RIGHT, buff=0.04).align_to(a, DOWN)
    return VGroup(a, e, b)


# ---- the half-life world (scenes 3 to 6): level 0..1 against time in half-lives, tank on the left
PN = Pn(-3.0, 6.4, -2.5, 2.5, 4.0, 1.0)


def hl_axes(pn=PN):
    return VGroup(Line(pn.pt(0, 0), pn.pt(4, 0), stroke_width=5, color=TEXT),
                  Line(pn.pt(0, 0), pn.pt(0, 1.04), stroke_width=5, color=TEXT))


def hl_bars(pn=PN, text="one half-life", with_text=True):
    bars, labs = VGroup(), VGroup()
    for i in range(4):
        a, b = pn.pt(i, 0)[0], pn.pt(i + 1, 0)[0]
        r = Rectangle(width=b - a - 0.08, height=0.5, stroke_color=GREY, stroke_width=3,
                      fill_color=GREY, fill_opacity=0.15).move_to(P3((a + b) / 2, pn.y0 - 0.35, 0))
        bars.add(r)
        if with_text:
            t = T(text, 26, TEXT)
            fit(t, max_w=2.2)
            labs.add(t.move_to(r))
    return bars, labs


def mini_tank(sc, L=0.85, base=0.85):
    t = Tank(sc, cx=-5.0, cy=0.0, w=2.0, h=3.4, pipe=[(-6.5, 2.05), (-5.6, 2.05)], arrows=False,
             handle=False, L=L, base=base, k=1.0, gapw=0.2)
    t.run = False
    return t


def add_tank(sc, t):
    sc.add(*t.parts(), t.frame, t.stub, t.tap)


def y_label(pn, y, text, size=26):
    return T(text, size, TEXT).move_to(pn.pt(0, y) + LEFT * 0.42)


# ---- the burst world (scenes 7 to 13): the same short bursts into a fast and a slow drain
PER, TMAX = 60.0, 240.0
HL_FAST, HL_SLOW = 5.0, 75.0
YMAX = 2.6          # in units of one burst's jump J
BURSTS = [0.0, 60.0, 120.0, 180.0]


def burst_series(h, dt=0.5):
    q = 2 ** (-PER / h)
    peak = 1.0 / (1 - q)
    pts = []
    for b in BURSTS:
        pts.append((b, peak * q))
        n = int(PER / dt)
        for i in range(n + 1):
            x = b + i * dt
            pts.append((x, peak * 2 ** (-(i * dt) / h)))
            if i == 0:
                pass
    # the vertical jump: pts[0] is the trough, the next point is the peak at the same x
    out = []
    for p in pts:
        out.append(p)
    return out


def burst_level(h, t):
    q = 2 ** (-PER / h)
    peak = 1.0 / (1 - q)
    t = t % TMAX
    k = int(t // PER)
    return peak * 2 ** (-(t - k * PER) / h)


def burst_on(tm):
    return any(b <= tm % TMAX < b + 8.0 for b in BURSTS)


FAST_PTS = burst_series(HL_FAST)
SLOW_PTS = burst_series(HL_SLOW)
PN_O = Pn(-3.0, 6.4, -2.3, 2.4, TMAX, YMAX)             # overlay panel (scenes 10, 12)
PN_L = Pn(-6.3, -0.8, -1.1, 2.3, TMAX, YMAX)            # split panels (scenes 11, 13)
PN_R = Pn(0.8, 6.3, -1.1, 2.3, TMAX, YMAX)


def p_axes(pn, ticks=True, size=24):
    g = VGroup(Line(pn.pt(0, 0), pn.pt(TMAX, 0), stroke_width=5, color=TEXT),
               Line(pn.pt(0, 0), pn.pt(0, YMAX), stroke_width=5, color=TEXT))
    if ticks:
        for m in (0, 60, 120, 180, 240):
            g.add(T(str(m), size, TEXT).move_to(pn.pt(m, 0) + DOWN * 0.62))
    return g


def burst_marks(pn, tr=None):
    """Orange tabs under the axis at each burst; they light up as the clock passes them."""
    g = VGroup()
    for b in BURSTS:
        r = Rectangle(width=max(0.18, pn.pt(8, 0)[0] - pn.pt(0, 0)[0]), height=0.26, stroke_width=0,
                      fill_color=ORANGE, fill_opacity=1).move_to(pn.pt(b + 4, 0) + DOWN * 0.2)
        if tr is not None:
            r.add_updater(lambda m, b=b: m.set_fill(ORANGE, 1.0 if tr.get_value() >= b else 0.25))
        g.add(r)
    return g


def pair_tanks(sc, cx=(-2.6, 2.6), cy=0.6, w=2.6, h=2.8):
    pipe_y = cy + h / 2 + 0.35
    out = []
    for c, gp in zip(cx, (0.55, 0.13)):
        t = Tank(sc, cx=c, cy=cy, w=w, h=h, pipe=[(0.0, 3.2), (0.0, pipe_y), (c - 0.6, pipe_y)], arrows=False,
                 handle=False, L=0.0, base=0.0, k=1.0, gapw=gp)
        t.run = False
        out.append(t)
    return out


def side_tanks(sc, with_text=True):
    """Two small tanks in the left column, one per drain (fast on top)."""
    ts = []
    for cy, gp in ((1.55, 0.1), (-1.45, 0.3)):
        t = Tank(sc, cx=-5.2, cy=cy, w=1.4, h=1.9, pipe=[(-6.5, cy + 0.95 + 0.35), (-5.8, cy + 0.95 + 0.35)],
                 arrows=False, handle=False, L=0.0, base=0.0, k=1.0, gapw=gp)
        t.run = False
        ts.append(t)
    return ts


def run_side_tanks(sc, ts, rate=14.1, t0=0.6, loop=False):
    def fn(tm):
        m = (tm - t0) * rate
        if loop:
            m = m % TMAX
        m = max(0.0, min(TMAX - 1e-3, m))
        for t, h in zip(ts, (HL_SLOW, HL_FAST)):
            L = burst_level(h, m) / YMAX
            t.Lt.set_value(max(0.0, min(1.0, L)))
            t.base.set_value(0.9 if burst_on(m) else 0.0)
            t.drain_ov = min(1.3, 2.5 * L * (6.0 if h < 10 else 1.0)) if L > 0.01 else 0.0
    driver(sc, fn)


def add_side(sc, ts):
    for t in ts:
        add_tank(sc, t)


# ================================================================== scenes
class S00Title(TitleCard):
    TITLE = "How Fast a Level Follows"
    LESSON = LESSON_TITLE


class S01Hook(SpokenScene):
    def construct(self):
        ah = T("adult human", 32, TEXT).move_to(P3(-5.2, 3.45, 0))
        self.add(ah)
        c1 = chip("cortisol", ORANGE, 36)
        c2 = chip("liver", TEXT, 36)
        c3 = chip("makes more glucose", TEXT, 34)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=1.15).move_to(P3(0, 0.4, 0))
        a1 = Arrow(c1.get_right(), c2.get_left(), buff=0.12, color=TEXT, stroke_width=7)
        a2 = Arrow(c2.get_right(), c3.get_left(), buff=0.12, color=TEXT, stroke_width=7)
        self.play(FadeIn(c1, scale=0.8), run_time=0.7)
        self.at("liver")
        self.play(Create(a1), FadeIn(c2, shift=RIGHT * 0.2), run_time=0.8)
        self.at("glucose")
        self.play(Create(a2), FadeIn(c3, shift=RIGHT * 0.2), run_time=0.8)
        self.at("adrenal")
        self.play(FadeOut(VGroup(row, a1, a2)), run_time=0.6)
        # strip 1: the adrenal tap in bursts, on a time axis (0..360 min)
        X0, X1 = -4.0, 6.4
        pn1 = Pn(X0, X1, 0.5, 2.1, 360.0, 1.0)
        pn2 = Pn(X0, X1, -3.0, -0.2, 360.0, 1.0)
        ax1 = Line(pn1.pt(0, 0), pn1.pt(360, 0), stroke_width=5, color=TEXT)
        ax2 = VGroup(Line(pn2.pt(0, 0), pn2.pt(360, 0), stroke_width=5, color=TEXT),
                     DashedLine(pn2.pt(0, 0.45), pn2.pt(360, 0.45), dash_length=0.18, stroke_width=4, color=TEAL).set_opacity(0.0))
        lt = T("adrenal\ntap", 32, ORANGE, line_spacing=0.8).move_to(P3(-5.0, 0.7, 0))
        pipe = polyline([(-6.5, 1.75), (-5.9, 1.75), (-5.9, 1.25)], ORANGE, 16, 0.5)
        lever = Line(P3(-6.5, 1.75), P3(-6.1, 2.15), stroke_width=9, color=TEXT)
        self.play(Create(ax1), FadeIn(lt), FadeIn(pipe), FadeIn(lever), run_time=0.9)
        # the sweep (min of the clock) starts when the pulses are named
        tr = clock(self, [(0, 0), (5.2, 0), (12.2, 360)])
        burst_t = [20, 95, 170, 245, 320]
        blocks = VGroup()
        for b in burst_t:
            r = Rectangle(width=pn1.pt(12, 0)[0] - pn1.pt(0, 0)[0], height=1.5, stroke_width=0,
                          fill_color=ORANGE, fill_opacity=0.9)
            r.b = b

            def upd(m, b=b):
                h = 1.5 * max(0.001, min(1.0, (tr.get_value() - b) / 4.0)) if tr.get_value() >= b else 0.001
                m.stretch_to_fit_height(h)
                m.move_to(pn1.pt(b + 6, 0) + UP * h / 2)
                m.set_fill(ORANGE, 0.9 if tr.get_value() >= b else 0.0)
            r.add_updater(upd)
            upd(r)
            blocks.add(r)
        cur = DashedLine(P3(0, -3.1, 0), P3(0, 2.4, 0), dash_length=0.15, stroke_width=4, color=TEXT)
        cur.add_updater(lambda m: m.move_to(P3(pn1.pt(tr.get_value(), 0)[0], -0.35, 0)))
        cur.set_opacity(0.0)

        def lev(tm):
            on = any(b <= tr.get_value() < b + 12 for b in burst_t)
            ang = 0.15 if on else 1.15
            lever.put_start_and_end_on(P3(-6.5, 1.75, 0), P3(-6.5 + 0.6 * math.cos(ang), 1.75 + 0.6 * math.sin(ang), 0))
        driver(self, lev)
        self.add(blocks, cur)
        self.at("pulses")
        cur.set_opacity(0.7)
        self.at("sixty")
        br = VGroup(Line(P3(pn1.pt(20, 0)[0], 2.45, 0), P3(pn1.pt(95, 0)[0], 2.45, 0), stroke_width=5, color=TEXT),
                    Line(P3(pn1.pt(20, 0)[0], 2.3, 0), P3(pn1.pt(20, 0)[0], 2.6, 0), stroke_width=5, color=TEXT),
                    Line(P3(pn1.pt(95, 0)[0], 2.3, 0), P3(pn1.pt(95, 0)[0], 2.6, 0), stroke_width=5, color=TEXT))
        bl = T("60 to 90 min", 30, TEXT).move_to(P3((pn1.pt(20, 0)[0] + pn1.pt(95, 0)[0]) / 2, 2.95, 0))
        self.play(Create(br), FadeIn(bl), run_time=0.9)
        self.play(FadeIn(ax2[0]), run_time=0.6)
        self.at("its level")
        ll = T("level\nin blood", 32, TEAL, line_spacing=0.8).move_to(P3(-5.35, -1.6, 0))
        q = T("?", 140, TEAL, weight=BOLD).move_to(P3(1.2, -1.6, 0))
        q.t = 0.0
        q.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_opacity(0.55 + 0.45 * math.sin(3.2 * m.t)))[0])
        self.play(FadeIn(ll), run_time=0.6)
        self.add(q)
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        t = Tank(self, cx=0.5, cy=-0.2, w=3.2, h=4.0, L=0.0, base=0.0, k=0.0)
        self.add(*t.parts())
        self.at("tank")
        self.play(Create(t.frame), run_time=1.0)
        self.at("tap")
        tl = T("tap", 34, ORANGE).move_to(P3(-4.3, 2.15, 0))
        self.play(FadeIn(t.tap), FadeIn(tl), run_time=0.7)
        t.base.set_value(0.0)
        self.play(t.base.animate.set_value(0.65), run_time=1.0)
        self.at("drain")
        dl = T("drain: clearance", 32, GREY).move_to(P3(4.4, -2.55, 0))
        self.play(FadeIn(t.stub), t.k.animate.set_value(1.0), FadeIn(dl), run_time=1.0)
        self.at("level")
        ll = T("level", 34, TEAL).move_to(P3(-2.2, t.surf_y(), 0))
        ll.add_updater(lambda m, dt: m.move_to(P3(-2.2, t.surf_y(), 0)))
        self.play(FadeIn(ll), run_time=0.6)
        self.at("match")
        ie = T("in = out", 40, TEXT).move_to(P3(5.0, 0.4, 0))
        ring = Circle(radius=0.25, color=TEAL, stroke_width=6).move_to(P3(t.rt + 0.35, 0.0, 0))
        fb = dpath([(t.rt + 0.6, 0.0), (3.3, 0.0), (3.3, 3.4), (t.cx - 1.9, 3.4), (t.cx - 1.9, 3.05)])
        self.play(FadeIn(ie), FadeIn(ring), Create(fb), run_time=1.4)
        self.play(fb.animate.set_opacity(0.3), ring.animate.set_opacity(0.3), run_time=1.0)
        self.at("time the drain")
        sw = VGroup(Circle(radius=0.5, color=TEXT, stroke_width=6), Line(P3(0, 0.5, 0), P3(0, 0.72, 0), stroke_width=8, color=TEXT),
                    Line(P3(0, 0, 0), P3(0.28, 0.2, 0), stroke_width=6, color=GREY)).move_to(P3(t.cx + 1.6, t.bot - 0.8, 0))
        self.play(FadeIn(sw, scale=0.6), run_time=0.6)
        self.play(Rotate(sw[2], -2 * PI, about_point=sw[0].get_center()), run_time=1.6)
        self.finish()


def fall_world(sc, pn=PN, marks=True, bar_text="one half-life", level_t=4.0):
    """Rebuild the end of scene 3: axes, bars, the halving curve, marks. Returns a dict."""
    d = {}
    d["ax"] = hl_axes(pn)
    d["bars"], d["labs"] = hl_bars(pn, bar_text)
    d["curve"] = static_pts(pn, curve_pts(lambda x: 2 ** -x, 0, 4), TEAL, 8)
    d["ymarks"] = VGroup(*[y_label(pn, v, s) for v, s in ((1, "1"), (0.5, "1/2"), (0.25, "1/4"), (0.125, "1/8"))])
    d["drops"] = VGroup(*[DashedLine(pn.pt(i, 0), pn.pt(i, 2 ** -i), dash_length=0.12, stroke_width=3, color=TEXT).set_opacity(0.6)
                          for i in (1, 2, 3)])
    d["dots"] = VGroup(*[Dot(pn.pt(i, 2 ** -i), radius=0.12, color=TEAL) for i in (1, 2, 3)])
    sc.add(d["ax"], d["bars"], d["labs"], d["curve"])
    if marks:
        sc.add(d["ymarks"], d["drops"], d["dots"])
    return d


class S03Fall(SpokenScene):
    def construct(self):
        pn = PN
        ax = hl_axes()
        bars, labs = hl_bars()
        t = mini_tank(self)
        add_tank(self, t)
        tl = T("tap", 34, ORANGE).move_to(P3(-6.0, 2.65, 0))
        dl = T("drain", 32, GREY).move_to(P3(-5.0, -3.2, 0))
        y1 = y_label(pn, 1, "1")
        self.add(ax, bars, tl, dl, y1)
        self.play(FadeIn(ax), FadeIn(bars), run_time=0.01)
        tr = clock(self, [(0, 0), (0.9, 0), (9.6, 4.0)])
        pts = curve_pts(lambda x: 2 ** -x, 0, 4, 300)
        curve = trace_pts(pn, pts, tr, TEAL, 8)
        dot = Dot(radius=0.14, color=TEAL)
        dot.add_updater(lambda m: m.move_to(pn.pt(tr.get_value(), 2 ** -tr.get_value())))
        self.add(curve, dot)

        def tk(tm):
            x = tr.get_value()
            t.Lt.set_value(0.85 * 2 ** -x)
            t.base.set_value(0.85 * max(0.0, 1 - max(0.0, tm - 0.5) / 0.6))
        driver(self, tk)
        self.at("shut")
        self.wait(0.2)
        self.at("not in a straight line")
        line = DashedLine(pn.pt(0, 1), pn.pt(2, 0), dash_length=0.2, stroke_width=5, color=TEXT)
        nt = T("not this", 30, TEXT).move_to(P3(-1.45, -1.0, 0))
        self.play(Create(line), FadeIn(nt), run_time=1.0)
        self.at("constant fraction")
        self.play(FadeOut(line), FadeOut(nt), Transform(dl, T("drain: a constant\nfraction per minute", 26, GREY, line_spacing=0.8).move_to(P3(-5.0, -3.2, 0))), run_time=0.8)
        self.at("so the level halves")
        ymk = {v: y_label(pn, v, s) for v, s in ((0.5, "1/2"), (0.25, "1/4"), (0.125, "1/8"))}
        drops = [DashedLine(pn.pt(i, 0), pn.pt(i, 2 ** -i), dash_length=0.12, stroke_width=3, color=TEXT).set_opacity(0.6) for i in (1, 2, 3)]
        dots = [Dot(pn.pt(i, 2 ** -i), radius=0.13, color=TEAL) for i in (1, 2, 3)]
        self.play(FadeIn(ymk[0.5]), Create(drops[0]), FadeIn(dots[0], scale=2), run_time=0.7)
        self.at("then halves again")
        self.play(FadeIn(ymk[0.25]), Create(drops[1]), FadeIn(dots[1], scale=2), run_time=0.7)
        self.at("again in")
        self.play(FadeIn(ymk[0.125]), Create(drops[2]), FadeIn(dots[2], scale=2), run_time=0.7)
        self.at("equal steps")
        self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.2), *[b.animate.set_fill(GREY, 0.4) for b in bars], run_time=1.4)
        self.play(*[b.animate.set_fill(GREY, 0.15) for b in bars], run_time=0.5)
        self.at("wherever it starts")
        tr2 = clock(self, [(0, 0), (14.4, 0), (17.0, 4.0)])
        c2 = trace_pts(pn, curve_pts(lambda x: 0.5 * 2 ** -x, 0, 4, 300), tr2, TEAL_L, 7)
        d2 = Dot(radius=0.12, color=TEAL_L)
        d2.add_updater(lambda m: m.move_to(pn.pt(tr2.get_value(), 0.5 * 2 ** -tr2.get_value())))
        self.add(c2, d2)
        self.at("each halving")
        self.play(*[b.animate.set_fill(GREY, 0.4) for b in bars[:2]], run_time=0.6)
        self.play(*[b.animate.set_fill(GREY, 0.15) for b in bars[:2]], run_time=0.5)
        self.finish()


class S04Define(SpokenScene):
    def construct(self):
        pn = PN
        w = fall_world(self, bar_text="one half-life")
        t = mini_tank(self, L=0.85 * 2 ** -4, base=0.0)
        add_tank(self, t)
        tl = T("tap", 34, ORANGE).move_to(P3(-6.0, 2.65, 0))
        dl = T("drain", 32, GREY).move_to(P3(-5.0, -3.2, 0))
        self.add(tl, dl)
        # a slow ambient run: a marker rides the curve
        rid = clock(self, [(0, 0), (4.3, 4.0)])
        runner = Dot(radius=0.13, color=TEXT)
        runner.add_updater(lambda m: m.move_to(pn.pt(rid.get_value(), 2 ** -rid.get_value())))
        self.add(runner)
        self.at("one halving")
        self.play(Indicate(w["dots"][0], scale_factor=2.0), w["bars"][0].animate.set_fill(GREY, 0.45), run_time=1.0)
        self.at("half life")
        ar = DoubleArrow(pn.pt(0, 1.1), pn.pt(1, 1.1), buff=0, stroke_width=7, color=TEXT, tip_length=0.25)
        hl = T("half-life", 34, TEXT).move_to(pn.pt(0.5, 1.1) + UP * 0.45)
        self.play(Create(ar), FadeIn(hl), run_time=0.9)
        self.at("in this example")
        w["bars"][0].set_fill(GREY, 0.15)
        new_labs = [T("5 min", 26, TEXT).move_to(l) for l in w["labs"]]
        self.remove(*t.parts())
        self.play(FadeOut(VGroup(tl, dl)), FadeOut(t.frame), FadeOut(t.stub), FadeOut(t.tap),
                  *[Transform(a, b) for a, b in zip(w["labs"], new_labs)], FadeOut(ar), FadeOut(hl),
                  FadeOut(w["drops"]), FadeOut(w["dots"]), run_time=1.0)
        self.at("small peptide")
        pl = T("illustrative peptide:\nhalf-life 5 min", 28, TEAL, line_spacing=0.85)
        fit(pl, max_w=3.1)
        pl.move_to(P3(-5.2, 1.3, 0))
        self.play(FadeIn(pl, shift=RIGHT * 0.3), run_time=0.8)
        self.at("cortisol")
        trc = clock(self, [(0, 0), (9.9, 0), (12.8, 20.0)])
        # cortisol drawn on the same 0..20 min axis (75 min half-life shown, a mid value of 60 to 90)
        pn_m = Pn(PN.x0, PN.x1, PN.y0, PN.y1, 20.0, 1.0)
        cc = trace_pts(pn_m, curve_pts(lambda x: 2 ** (-x / 75.0), 0, 20, 120), trc, TEAL_L, 8)
        cd = Dot(radius=0.12, color=TEAL_L)
        cd.add_updater(lambda m: m.move_to(pn_m.pt(trc.get_value(), 2 ** (-trc.get_value() / 75.0))))
        self.add(cc, cd)
        self.at("textbooks")
        cl = T("cortisol:\nabout 60 to 90 min", 28, TEAL_L, line_spacing=0.85)
        fit(cl, max_w=3.1)
        cl.move_to(P3(-5.2, -0.5, 0))
        self.play(FadeIn(cl, shift=RIGHT * 0.3), run_time=0.8)
        self.at("about")
        nt = T("curve drawn with\n75 min", 24, TEXT, line_spacing=0.85)
        nt.move_to(P3(-5.2, -1.6, 0))
        self.play(FadeIn(nt), run_time=0.6)
        self.finish()


class S05Rise(SpokenScene):
    def construct(self):
        pn = PN
        ax = hl_axes()
        bars, labs = hl_bars()
        t = mini_tank(self, L=0.85 * 2 ** -4, base=0.0)
        add_tank(self, t)
        tl = T("tap", 34, ORANGE).move_to(P3(-6.0, 2.65, 0))
        dl = T("drain", 32, GREY).move_to(P3(-5.0, -3.2, 0))
        self.add(ax, bars, labs, tl, dl, y_label(pn, 0, "0"))
        tr = clock(self, [(0, 0), (0.9, 0), (8.2, 4.0)])
        curve = trace_pts(pn, curve_pts(lambda x: 1 - 2 ** -x, 0, 4, 300), tr, TEAL, 8)
        dot = Dot(radius=0.14, color=TEAL)
        dot.add_updater(lambda m: m.move_to(pn.pt(tr.get_value(), 1 - 2 ** -tr.get_value())))
        self.add(curve, dot)

        def tk(tm):
            x = tr.get_value()
            t.Lt.set_value(0.85 * (1 - 2 ** -x) + 0.85 * 2 ** -4 * 0)
            t.base.set_value(0.85 * min(1.0, max(0.0, (tm - 0.5) / 0.5)))
        driver(self, tk)
        self.at("open the tap")
        self.wait(0.3)
        self.at("new steady")
        st = DashedLine(pn.pt(0, 1), pn.pt(4, 1), dash_length=0.2, stroke_width=5, color=TEAL)
        sl = T("new steady level", 30, TEAL).move_to(P3(1.2, 2.95, 0))
        self.play(Create(st), FadeIn(sl), run_time=1.0)
        self.at("matches")
        self.wait(0.3)
        self.at("halfway")
        d1 = DashedLine(pn.pt(1, 0), pn.pt(1, 0.5), dash_length=0.12, stroke_width=3, color=TEXT).set_opacity(0.7)
        h1 = DashedLine(pn.pt(0, 0.5), pn.pt(1, 0.5), dash_length=0.12, stroke_width=3, color=TEXT).set_opacity(0.7)
        m1 = Dot(pn.pt(1, 0.5), radius=0.14, color=TEXT)
        t1 = T("50% at\n1 half-life", 26, TEXT, line_spacing=0.85).move_to(pn.pt(1, 0) + P3(1.17, 0.55, 0))
        self.play(Create(d1), Create(h1), FadeIn(m1, scale=2), FadeIn(t1), run_time=0.9)
        self.at("nearly there")
        d2 = DashedLine(pn.pt(2, 0), pn.pt(2, 0.75), dash_length=0.12, stroke_width=3, color=TEXT).set_opacity(0.7)
        m2 = Dot(pn.pt(2, 0.75), radius=0.14, color=TEXT)
        t2 = T("75% at 2", 28, TEXT).move_to(pn.pt(2, 0) + P3(1.2, 1.3, 0))
        self.play(Create(d2), FadeIn(m2, scale=2), FadeIn(t2), run_time=0.9)
        self.at("about four")
        m4 = Dot(pn.pt(4, 0.9375), radius=0.14, color=TEXT)
        t4 = T("94% at 4", 28, TEXT).move_to(pn.pt(4, 0) + P3(-1.2, 1.1, 0))
        d4 = DashedLine(pn.pt(4, 0), pn.pt(4, 0.9375), dash_length=0.12, stroke_width=3, color=TEXT).set_opacity(0.7)
        self.play(Create(d4), FadeIn(m4, scale=2), FadeIn(t4), run_time=0.9)
        self.finish()


class S06Both(SpokenScene):
    def construct(self):
        pn = PN
        ax = hl_axes()
        bars, labs = hl_bars()
        self.add(ax, bars, labs)
        self.add(y_label(pn, 0, "0"), y_label(pn, 1, "1"))
        t_fall = clock(self, [(0, 0), (0.4, 0), (3.0, 4.0)])
        t_rise = clock(self, [(0, 0), (2.4, 0), (5.0, 4.0)])
        fall = trace_pts(pn, curve_pts(lambda x: 2 ** -x, 0, 4, 240), t_fall, TEAL, 8)
        rise = trace_pts(pn, curve_pts(lambda x: 1 - 2 ** -x, 0, 4, 240), t_rise, TEAL, 8)
        self.add(fall, rise)
        self.at("both directions")
        sc_ = T("same clock\nboth ways", 32, TEAL, line_spacing=0.85).move_to(P3(-5.1, 3.0, 0))
        self.play(FadeIn(sc_, shift=RIGHT * 0.3), run_time=0.8)
        self.at("slow drain")
        t_sf = clock(self, [(0, 0), (4.4, 0), (7.0, 4.0)])
        slowf = trace_pts(pn, curve_pts(lambda x: 2 ** (-x / 2.0), 0, 4, 240), t_sf, TEAL_L, 7)
        self.add(slowf)
        sd = T("slower drain", 28, TEAL_L).move_to(P3(5.0, 0.0, 0))
        self.play(FadeIn(sd), run_time=0.6)
        self.at("slow rise")
        t_sr = clock(self, [(0, 0), (6.6, 0), (9.2, 4.0)])
        slowr = trace_pts(pn, curve_pts(lambda x: 1 - 2 ** (-x / 2.0), 0, 4, 240), t_sr, TEAL_L, 7)
        self.add(slowr)
        self.at("lags")
        tap = DashedLine(pn.pt(0, 1.0), pn.pt(4, 1.0), dash_length=0.2, stroke_width=6, color=ORANGE)
        tapl = T("tap on", 28, ORANGE).move_to(pn.pt(3.4, 1.0) + UP * 0.45)
        gap = DoubleArrow(pn.pt(0.5, 1.0), pn.pt(0.5, 1 - 2 ** -0.5), buff=0, stroke_width=6, color=ORANGE, tip_length=0.2)
        lg = T("lag", 30, TEXT).move_to(P3(-2.45, 0.8, 0))
        self.play(Create(tap), FadeIn(tapl), run_time=0.9)
        self.play(Create(gap), FadeIn(lg), run_time=0.7)
        self.at("short half life")
        a = chip("short half-life:\nminutes", TEAL, 26)
        a.move_to(P3(-5.1, 1.1, 0))
        self.play(FadeIn(a, shift=RIGHT * 0.3), run_time=0.7)
        self.at("long one")
        b = chip("long half-life:\nhours", TEAL_L, 26)
        b.move_to(P3(-5.1, -0.9, 0))
        self.play(FadeIn(b, shift=RIGHT * 0.3), run_time=0.7)
        r1 = Dot(radius=0.13, color=TEXT)
        r2 = Dot(radius=0.13, color=TEXT)

        def run(tm):
            x = max(0.0, (tm - 9.4) * 0.5) % 4.0
            r1.move_to(pn.pt(x, 2 ** -x))
            r2.move_to(pn.pt(x, 1 - 2 ** -x))
        run(0.0)
        driver(self, run)
        self.add(r1, r2)
        self.finish()


def build_pair_world(sc, pulses_from=4.2, speed=20.0):
    """Two equal tanks, one tap, the burst axis. Returns the tanks, the cursor tracker and the labels."""
    tl, tr_ = pair_tanks(sc)
    for t in (tl, tr_):
        sc.add(*t.parts())
    return tl, tr_


class S07Twotanks(SpokenScene):
    def construct(self):
        tl, tr_ = pair_tanks(self)
        self.add(*tl.parts(), *tr_.parts())
        self.at("two hormones")
        self.play(Create(tl.frame), Create(tr_.frame), run_time=1.0)
        self.at("same tap")
        tap = tag("same tap", (1.6, 3.3), ORANGE, 32)
        self.play(FadeIn(tl.tap), FadeIn(tr_.tap), FadeIn(tap), run_time=0.8)
        self.at("equal short bursts")
        PNB = Pn(-5.6, 5.6, -2.9, -2.4, TMAX, 1.0)
        axb = Line(PNB.pt(0, 0), PNB.pt(TMAX, 0), stroke_width=5, color=TEXT)
        blocks = VGroup(*[Rectangle(width=PNB.pt(10, 0)[0] - PNB.pt(0, 0)[0], height=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.35)
                          .move_to(PNB.pt(b + 5, 0) + UP * 0.25) for b in BURSTS])
        self.play(Create(axb), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.35), run_time=1.4)
        bl = T("one equal burst every 60 min, illustrative", 26, ORANGE).move_to(P3(0, -3.45, 0))
        self.play(FadeIn(bl), run_time=0.5)
        cur = clock(self, [(0, 0), (4.4, 0), (13.9, 190.0)])
        cursor = Line(P3(0, -3.0, 0), P3(0, -2.3, 0), stroke_width=6, color=TEXT)
        cursor.add_updater(lambda m: m.move_to(P3(PNB.pt(cur.get_value(), 0)[0], -2.65, 0)))
        self.add(cursor)

        def tk(tm):
            m = cur.get_value()
            on = burst_on(m) and tm > 4.4
            for t in (tl, tr_):
                t.base.set_value(0.9 if on else 0.0)
            for b, r in zip(BURSTS, blocks):
                r.set_fill(ORANGE, 0.95 if (b <= m < b + 10 and tm > 4.4) else (0.55 if m >= b + 10 and tm > 4.4 else 0.35))
        driver(self, tk)
        self.at("fast drain")
        tl.drain_ov = 1.0
        dl = tag("half-life 5 min", (-2.6, -2.0), GREY, 30)
        self.play(FadeIn(dl), run_time=0.6)
        self.at("slow drain")
        tr_.drain_ov = 0.35
        dr = tag("half-life 75 min", (2.6, -2.0), GREY, 30)
        self.play(FadeIn(dr), run_time=0.6)
        self.finish()


def backdrop_pair(sc, ghost=0.28):
    tl, tr_ = pair_tanks(sc)
    g = VGroup()
    for t in (tl, tr_):
        g.add(t.frame, t.stub, t.tap)
    g.set_opacity(ghost)
    sc.add(g)
    PNB = Pn(-5.6, 5.6, -2.9, -2.4, TMAX, 1.0)
    axb = Line(PNB.pt(0, 0), PNB.pt(TMAX, 0), stroke_width=5, color=TEXT).set_opacity(ghost)
    blocks = VGroup(*[Rectangle(width=PNB.pt(10, 0)[0] - PNB.pt(0, 0)[0], height=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.35 * 1.0)
                      .move_to(PNB.pt(b + 5, 0) + UP * 0.25) for b in BURSTS]).set_opacity(ghost)
    sc.add(axb, blocks)
    sc.add(tag("half-life 5 min", (-2.6, -2.0), GREY, 30).set_opacity(ghost), tag("half-life 75 min", (2.6, -2.0), GREY, 30).set_opacity(ghost))
    return tl, tr_


def question_card():
    q = VGroup(T("Relative to its own average,", 40, TEXT), T("which level swings more?", 44, TEXT, weight=BOLD)).arrange(DOWN, buff=0.2)
    card = RoundedRectangle(corner_radius=0.25, width=q.width + 1.0, height=q.height + 0.9, stroke_color=GOLD, stroke_width=5,
                            fill_color=BG, fill_opacity=1).move_to(P3(0, 0.3, 0))
    card.stretch_to_fit_height(3.9)
    card.move_to(P3(0, 0.3, 0))
    q.move_to(P3(0, 1.25, 0))
    c1 = chip("fast drain", GREY, 34)
    c2 = chip("slow drain", GREY, 34)
    ch = VGroup(c1, c2).arrange(RIGHT, buff=1.2).move_to(P3(0, -1.2, 0))
    return card, q, c1, c2


class S08Predict(SpokenScene):
    def construct(self):
        tl, tr_ = pair_tanks(self)
        self.add(*tl.parts(), *tr_.parts(), tl.frame, tr_.frame, tl.stub, tr_.stub, tl.tap, tr_.tap)
        tl.drain_ov = 1.0
        tr_.drain_ov = 0.35
        PNB = Pn(-5.6, 5.6, -2.9, -2.4, TMAX, 1.0)
        self.add(Line(PNB.pt(0, 0), PNB.pt(TMAX, 0), stroke_width=5, color=TEXT))
        blocks = VGroup(*[Rectangle(width=PNB.pt(10, 0)[0] - PNB.pt(0, 0)[0], height=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.35)
                          .move_to(PNB.pt(b + 5, 0) + UP * 0.25) for b in BURSTS])
        self.add(blocks, tag("half-life 5 min", (-2.6, -2.0), GREY, 30), tag("half-life 75 min", (2.6, -2.0), GREY, 30))
        cur = clock(self, [(0, 0), (0.0, 0), (10.2, 200.0)])
        cursor = Line(P3(0, -3.0, 0), P3(0, -2.3, 0), stroke_width=6, color=TEXT)
        cursor.add_updater(lambda m: m.move_to(P3(PNB.pt(cur.get_value(), 0)[0], -2.65, 0)))
        self.add(cursor)

        def tk(tm):
            m = cur.get_value()
            for t in (tl, tr_):
                t.base.set_value(0.9 if burst_on(m) else 0.0)
            for b, r in zip(BURSTS, blocks):
                r.set_fill(ORANGE, 0.95 if b <= m < b + 10 else (0.55 if m >= b + 10 else 0.35))
        driver(self, tk)
        self.at("compared")
        card, q, c1, c2 = question_card()
        chips = VGroup(c1, c2).arrange(RIGHT, buff=1.2).move_to(P3(0, -0.6, 0))
        self.play(FadeIn(VGroup(card, q), scale=0.92), run_time=0.8)
        self.at("which level")
        self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(c2, shift=UP * 0.2), run_time=0.7)
        self.at("swing")
        self.play(Indicate(c1, color=TEXT, scale_factor=1.1), run_time=0.9)
        self.play(Indicate(c2, color=TEXT, scale_factor=1.1), run_time=0.9)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        tl, tr_ = pair_tanks(self)
        self.add(*tl.parts(), *tr_.parts(), tl.frame, tr_.frame, tl.stub, tr_.stub, tl.tap, tr_.tap)
        tl.drain_ov = 1.0
        tr_.drain_ov = 0.35
        PNB = Pn(-5.6, 5.6, -2.9, -2.4, TMAX, 1.0)
        self.add(Line(PNB.pt(0, 0), PNB.pt(TMAX, 0), stroke_width=5, color=TEXT))
        self.add(VGroup(*[Rectangle(width=PNB.pt(10, 0)[0] - PNB.pt(0, 0)[0], height=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.35)
                          .move_to(PNB.pt(b + 5, 0) + UP * 0.25) for b in BURSTS]),
                 tag("half-life 5 min", (-2.6, -2.0), GREY, 30), tag("half-life 75 min", (2.6, -2.0), GREY, 30))
        card, q, c1, c2 = question_card()
        VGroup(c1, c2).arrange(RIGHT, buff=1.2).move_to(P3(0, -0.6, 0))
        self.add(card, q, c1, c2)
        ring_c = P3(5.9, 3.2, 0)
        tv = ValueTracker(0)
        ring = Arc(radius=0.42, start_angle=PI / 2, angle=-2 * PI, stroke_color=GOLD, stroke_width=8)
        ring.add_updater(lambda m: m.become(Arc(radius=0.42, start_angle=PI / 2, angle=-2 * PI * (1 - tv.get_value()) - 0.001, stroke_color=GOLD, stroke_width=8).move_to(ring_c)))
        self.add(ring)
        self.play(tv.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        self.finish()


def overlay_traces(sc, tr, pn=PN_O, widths=(7, 7)):
    fast = trace_pts(pn, FAST_PTS, tr, TEAL, widths[0])
    slow = trace_pts(pn, SLOW_PTS, tr, TEAL, widths[1])
    return fast, slow


def side_labels(sc):
    a = T("slow", 28, TEAL).move_to(P3(-3.95, 1.55, 0))
    b = T("fast", 28, TEAL).move_to(P3(-3.95, -1.45, 0))
    return VGroup(a, b)


class S10Reveal(SpokenScene):
    def construct(self):
        pn = PN_O
        ts = side_tanks(self)
        add_side(self, ts)
        ax = p_axes(pn)
        tr = clock(self, [(0, 0), (0.6, 0), (17.6, 240.0)])
        marks = burst_marks(pn, tr)
        self.add(ax, marks, side_labels(self))
        tank_tap = [T("tap", 28, ORANGE).move_to(P3(-6.2, 3.35 if i == 0 else 0.3, 0)) for i in (0, 1)]
        self.add(*tank_tap)
        fast, slow = overlay_traces(self, tr)
        self.add(fast, slow)
        run_side_tanks(self, ts, rate=240.0 / 17.0, t0=0.6)
        self.at("same amount")
        l1 = T("same jump per burst in both tanks", 30, TEXT).move_to(P3(0.5, 3.45, 0))
        self.play(FadeIn(l1), run_time=0.7)
        fn = T("computed, illustrative numbers; swings compared relative to each level", 22, TEXT).move_to(P3(0.2, -3.62, 0))
        self.at("fast draining")
        self.play(FadeIn(fn), run_time=0.5)
        self.at("empties")
        self.play(FadeOut(l1), run_time=0.3)
        l2 = power_label("fast: peak/trough = 2", "", "60/5", ", about 4,000-fold", 28).move_to(P3(0.5, 3.45, 0))
        self.play(FadeIn(l2), run_time=0.6)
        self.at("tiny")
        self.wait(0.1)
        self.at("never empties")
        self.wait(0.1)
        self.at("ripples")
        l3 = power_label("slow: peak/trough = 2", "", "60/75", ", about 1.7-fold", 28).move_to(P3(0.5, 2.9, 0))
        self.play(FadeIn(l3), run_time=0.6)
        self.finish()


def static_overlay(sc, pn=PN_O):
    fast = static_pts(pn, FAST_PTS, TEAL, 7)
    slow = static_pts(pn, SLOW_PTS, TEAL, 7)
    return fast, slow


class S11Meaning(SpokenScene):
    def construct(self):
        ts = side_tanks(self)
        add_side(self, ts)
        run_side_tanks(self, ts, rate=14.1, t0=0.0, loop=True)
        side_lab = side_labels(self)
        self.add(side_lab)
        ax = p_axes(PN_O)
        marks = burst_marks(PN_O)
        fast, slow = static_overlay(self)
        self.add(ax, marks, fast, slow)
        # split: each trace goes to its own panel at full height
        self.at("what matters")
        axL, axR = p_axes(PN_L, size=22), p_axes(PN_R, size=22)
        fastL = static_pts(PN_L, FAST_PTS, TEAL, 7)
        slowR = static_pts(PN_R, SLOW_PTS, TEAL, 7)
        mL, mR = burst_marks(PN_L), burst_marks(PN_R)
        self.remove(*[m for t in ts for m in t.parts()])
        self.play(FadeOut(VGroup(*[x for t in ts for x in (t.frame, t.stub, t.tap)])),
                  FadeOut(side_lab), FadeOut(ax), FadeOut(marks),
                  Transform(fast, fastL), Transform(slow, slowR), FadeIn(axL), FadeIn(axR), FadeIn(mL), FadeIn(mR), run_time=1.6)
        self.at("half life compared")
        sx = PN_L.pt(0, 0)[0]
        rx = PN_R.pt(0, 0)[0]
        unit = (PN_L.pt(TMAX, 0)[0] - sx) / TMAX
        def bar(x0, mins, y, color):
            return Rectangle(width=mins * unit, height=0.24, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(P3(x0 + mins * unit / 2, y, 0))
        hbL, hbR = bar(sx, 5, -2.55, GREY), bar(rx, 75, -2.55, GREY)
        hlL = T("half-life 5 min", 28, GREY).next_to(hbL, RIGHT, buff=0.15)
        hlR = T("half-life 75 min", 28, GREY).next_to(hbR, RIGHT, buff=0.15)
        self.play(FadeIn(hbL, scale=0.5), FadeIn(hbR, scale=0.5), FadeIn(hlL), FadeIn(hlR), run_time=0.9)
        self.at("gap between")
        gbL, gbR = bar(sx, 60, -3.05, TEXT), bar(rx, 60, -3.05, TEXT)
        glL = T("gap 60 min", 28, TEXT).next_to(gbL, RIGHT, buff=0.15)
        glR = T("gap 60 min", 28, TEXT).next_to(gbR, RIGHT, buff=0.15)
        self.play(FadeIn(gbL, scale=0.5), FadeIn(gbR, scale=0.5), FadeIn(glL), FadeIn(glR), run_time=0.9)
        self.at("much shorter")
        tL = T("half-life much shorter\nthan the gap: tracks pulses", 28, TEAL, line_spacing=0.85).move_to(P3(-3.55, 3.25, 0))
        fit(tL, max_w=5.5)
        self.play(FadeIn(tL), run_time=0.7)
        self.at("tracks each pulse")
        self.play(*[Indicate(m, color=ORANGE, scale_factor=1.4) for m in mL], run_time=1.0)
        self.at("as long as")
        tR = T("half-life about as long as\nthe gap: smooths pulses", 28, TEAL, line_spacing=0.85).move_to(P3(3.55, 3.25, 0))
        fit(tR, max_w=5.5)
        self.play(FadeIn(tR), run_time=0.7)
        self.at("smooths")
        self.play(Indicate(slow, color=TEAL_L, scale_factor=1.0), run_time=1.0)
        self.at("cortisol's")
        ct = chip("cortisol-like", TEXT, 28)
        ct.move_to(P3(3.55, -0.2, 0))
        self.play(FadeIn(ct, scale=0.8), run_time=0.7)
        self.at("ripples")
        self.play(Indicate(slow, color=TEAL_L, scale_factor=1.0), run_time=1.0)
        self.finish()


class S12Average(SpokenScene):
    def construct(self):
        pn = PN_O
        ts = side_tanks(self)
        add_side(self, ts)
        run_side_tanks(self, ts, rate=14.1, t0=0.0, loop=True)
        self.add(side_labels(self))
        ax = p_axes(pn)
        marks = burst_marks(pn)
        fast, slow = static_overlay(self)
        self.add(ax, marks, fast, slow)
        af = 1.0 / (math.log(2) * PER / HL_FAST)
        as_ = 1.0 / (math.log(2) * PER / HL_SLOW)
        self.at("on average")
        avf = DashedLine(pn.pt(0, af), pn.pt(TMAX, af), dash_length=0.18, stroke_width=5, color=TEAL_L)
        avs = DashedLine(pn.pt(0, as_), pn.pt(TMAX, as_), dash_length=0.18, stroke_width=5, color=TEAL_L)
        al = T("averages", 28, TEAL_L).move_to(P3(5.3, -0.15, 0))
        self.play(Create(avf), Create(avs), FadeIn(al), run_time=1.2)
        self.at("what the tap adds")
        eq = M("average level = average secretion / (k x V)", 26, TEXT).move_to(P3(0.5, 3.45, 0))
        self.play(FadeIn(eq), run_time=0.8)
        self.at("smaller fraction")
        self.play(Indicate(ts[0].frame, color=TEAL, scale_factor=1.06), run_time=1.0)
        self.at("fuller tank")
        self.play(Indicate(ts[0].frame, color=TEAL, scale_factor=1.06), run_time=1.0)
        self.at("sits higher")
        ar = DoubleArrow(pn.pt(TMAX * 0.5, af), pn.pt(TMAX * 0.5, as_), buff=0, stroke_width=7, color=TEXT, tip_length=0.22)
        r15 = T("75 / 5 = 15 times higher, same bursts", 28, TEAL).move_to(P3(0.5, 2.95, 0))
        self.play(Create(ar), FadeIn(r15), run_time=1.0)
        self.play(FadeOut(eq), run_time=0.3)
        sw = T("slow level: smaller swings relative to its average", 28, TEAL).move_to(P3(0.5, 3.45, 0))
        self.play(FadeIn(sw), run_time=0.6)
        self.finish()


class S13Caveat(SpokenScene):
    def construct(self):
        ts = side_tanks(self)
        add_side(self, ts)
        run_side_tanks(self, ts, rate=14.1, t0=0.0, loop=True)
        side_lab = side_labels(self)
        self.add(side_lab)
        ax = p_axes(PN_O)
        marks = burst_marks(PN_O)
        fast, slow = static_overlay(self)
        self.add(ax, marks, fast, slow)
        axL = p_axes(PN_L, size=22)
        fastL, slowL = static_pts(PN_L, FAST_PTS, TEAL, 6), static_pts(PN_L, SLOW_PTS, TEAL, 6)
        self.remove(*[m for t in ts for m in t.parts()])
        self.play(FadeOut(VGroup(*[x for t in ts for x in (t.frame, t.stub, t.tap)])),
                  FadeOut(side_lab), FadeOut(ax), FadeOut(marks), Transform(fast, fastL), Transform(slow, slowL),
                  FadeIn(axL), run_time=1.4)
        self.at("simple model")
        st = T("MODEL", 52, TEXT, weight=BOLD)
        box = SurroundingRectangle(st, buff=0.22, color=TEXT, stroke_width=6)
        stamp = VGroup(box, st).rotate(0.15).move_to(P3(-3.55, 0.45, 0))
        stamp[0].set_fill(BG, 0.6)
        self.play(FadeIn(stamp, scale=1.4), run_time=0.7)
        ml = T("invented numbers", 28, TEXT).move_to(P3(-3.55, 3.2, 0))
        self.at("invented")
        self.play(FadeIn(ml), run_time=0.6)
        self.at("real secretion")
        axO = VGroup(Line(PN_R.pt(0, 0), PN_R.pt(TMAX, 0), stroke_width=5, color=TEXT), Line(PN_R.pt(0, 0), PN_R.pt(0, YMAX), stroke_width=5, color=TEXT))
        rl = T("real secretion varies\n(schematic)", 28, ORANGE, line_spacing=0.85).move_to(P3(3.55, 3.2, 0))
        self.play(Create(axO), FadeIn(rl), run_time=0.9)
        rs = np.random.RandomState(7)
        xs = np.linspace(0, TMAX, 150)
        raw = 1.05 + 0.55 * np.sin(xs / 17.0) + 0.35 * np.sin(xs / 6.1 + 1.0) + 0.25 * rs.randn(150)
        raw = np.clip(raw, 0.25, 2.4)
        opts = [(float(a), float(b)) for a, b in zip(xs, raw)]
        trs = ValueTracker(0.0)
        oc = trace_pts(PN_R, opts, trs, ORANGE, 7)
        self.add(oc)
        self.play(trs.animate.set_value(TMAX), run_time=max(1.0, self.narration_s - self.elapsed() - 0.6), rate_func=linear)
        self.finish()


class S14End(EndCard):
    LINE = "The half-life sets how fast a hormone level can follow."
