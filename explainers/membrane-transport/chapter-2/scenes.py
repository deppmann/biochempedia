"""Read the Traffic: membrane transport, chapter 2.

Same look and colour map as chapter 1 (Two Pushes, One Hill).

COLOR MAP
  ORANGE  potassium (ions through a pore)
  GREY    sodium, membrane
  YELLOW  glucose / substrate (carrier cargo)
  TEAL    voltage and measurement (detector trace, tags)
  GREEN   open time / equilibrium
  BLUE    transport proteins (channels, carriers)

Every plotted curve is computed: the carrier curve is v = 60 S / (1 + S), the pore curve
is v = 2.5 S (the lesson's teaching functions); the single-channel traces come from
explicit opening schedules.
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
SODIUM = "#B9C1CC"

# --------------------------------------------------------------------------- small helpers


def mk_dot(color, r=0.17, op=0.95):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op)


def jit(d, amp=0.12, seed=0):
    """Gentle ambient wobble around the object's current position."""
    d.clear_updaters()
    d.anchor = d.get_center().copy()
    d.ph = 1.9 * seed

    def f(m, dt):
        m.ph += dt
        m.move_to(m.anchor + np.array([amp * math.sin(1.7 * m.ph + seed),
                                       amp * math.cos(1.3 * m.ph + 0.9 * seed), 0]))
    d.add_updater(f)
    return d


def dots_at(points, color, r=0.17, amp=0.12):
    g = VGroup()
    for i, p in enumerate(points):
        g.add(jit(mk_dot(color, r).move_to([p[0], p[1], 0]), amp, i + 1))
    return g


def fields(x0, x1, y=0.0, h=0.78, top=3.8, bottom=-3.8):
    cx, w = (x0 + x1) / 2, x1 - x0
    ytop, ybot = y + h / 2, y - h / 2
    out = Rectangle(width=w, height=top - ytop, stroke_width=0, fill_color=BLUE, fill_opacity=0.12)
    out.move_to([cx, (top + ytop) / 2, 0])
    ins = Rectangle(width=w, height=ybot - bottom, stroke_width=0, fill_color=GOLD, fill_opacity=0.12)
    ins.move_to([cx, (ybot + bottom) / 2, 0])
    return VGroup(out, ins).set_z_index(-5)


def membrane_segs(y, h, x0, x1, gaps):
    segs = VGroup()
    start = x0
    for cx, half in sorted(gaps):
        if cx - half - start > 0.15:
            segs.add(RoundedRectangle(corner_radius=0.1, width=cx - half - start, height=h, color=GREY,
                                      stroke_width=2.5, fill_color=GREY, fill_opacity=0.42
                                      ).move_to([(start + cx - half) / 2, y, 0]))
        start = cx + half
    if x1 - start > 0.15:
        segs.add(RoundedRectangle(corner_radius=0.1, width=x1 - start, height=h, color=GREY,
                                  stroke_width=2.5, fill_color=GREY, fill_opacity=0.42
                                  ).move_to([(start + x1) / 2, y, 0]))
    return segs


class Chan(VGroup):
    """A channel: two blue walls round a pore, a gate block, and ions that stream when open."""

    def __init__(self, cx, cy=0.0, mem_h=0.78, pw=0.6, ww=0.34, yspan=1.7, nflow=3, speed=0.45, rf=0.14):
        super().__init__()
        self.cx, self.cy, self.pw, self.ww, self.yspan, self.speed = cx, cy, pw, ww, yspan, speed
        self.half = pw / 2 + ww
        wh = mem_h + 0.34
        self.l = RoundedRectangle(corner_radius=0.08, width=ww, height=wh, color=BLUE, stroke_width=3,
                                  fill_color=BLUE, fill_opacity=0.7).move_to([cx - pw / 2 - ww / 2, cy, 0])
        self.r = self.l.copy().move_to([cx + pw / 2 + ww / 2, cy, 0])
        self.pore = Rectangle(width=pw, height=mem_h, stroke_width=0, fill_color=BLUE, fill_opacity=0.34).move_to([cx, cy, 0])
        self.gate = RoundedRectangle(corner_radius=0.08, width=pw, height=mem_h * 0.62, color=BLUE, stroke_width=3,
                                     fill_color=BLUE, fill_opacity=0.95).move_to([cx, cy, 0])
        self.flow = VGroup(*[mk_dot(ORANGE, rf) for _ in range(nflow)])
        self.o = ValueTracker(1.0)
        self.drive = None
        self.phase = 0.0
        self.add(self.pore, self.flow, self.gate, self.l, self.r)

    def _upd(self, m, dt):
        if self.drive is not None:
            self.o.set_value(self.drive())
        o = self.o.get_value()
        self.gate.set_fill(BLUE, opacity=0.95 * (1 - o))
        self.gate.set_stroke(BLUE, width=3, opacity=1 - o)
        self.pore.set_fill(BLUE, opacity=0.14 + 0.2 * o)
        self.phase += dt * self.speed * o
        n = len(self.flow)
        for i, d in enumerate(self.flow):
            u = (self.phase + i / n) % 1.0
            d.move_to([self.cx, self.cy + self.yspan - 2 * self.yspan * u, 0])
            d.set_fill(ORANGE, opacity=min(1.0, o * 3) * min(1.0, u * 6, (1 - u) * 6))

    def activate(self):
        self.add_updater(self._upd)
        return self


def carrier_pts(cx, cy, p, s=1.0, W=1.05, H=0.95, w=0.4, D=1.25):
    dt, db = D * max(0.0, -p), D * max(0.0, p)
    wt, wb = w * min(1.0, 3 * max(0.0, -p)), w * min(1.0, 3 * max(0.0, p))
    P = [(-W, H), (-W, -H), (-wb, -H), (-wb, -H + db), (wb, -H + db), (wb, -H), (W, -H), (W, H),
         (wt, H), (wt, H - dt), (-wt, H - dt), (-wt, H), (-W, H)]
    return [[cx + s * x, cy + s * y, 0] for x, y in P]


class Carrier(VMobject):
    """Blue cup: p = -1 opens above, 0 is closed, +1 opens below. It never turns over or moves."""

    def __init__(self, cx, cy=0.0, s=1.0):
        super().__init__()
        self.cx, self.cy, self.s = cx, cy, s
        self.p = ValueTracker(-1.0)
        self.period, self.lo, self.hi, self.t = None, -1.0, 1.0, 0.0
        self.set_stroke(BLUE, 3).set_fill(BLUE, opacity=0.7)
        self.refresh()

    def refresh(self):
        self.set_points_as_corners(carrier_pts(self.cx, self.cy, self.p.get_value(), self.s))

    def _upd(self, m, dt):
        if self.period:
            self.t += dt
            mid, amp = (self.lo + self.hi) / 2, (self.hi - self.lo) / 2
            self.p.set_value(mid - amp * math.cos(2 * math.pi * self.t / self.period))
        self.refresh()

    def activate(self, period=None, lo=-1.0, hi=1.0):
        self.period, self.lo, self.hi = period, lo, hi
        self.add_updater(self._upd)
        return self


def vbrace(x, y0, y1, color=TEXT, tick=0.13):
    return VGroup(Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=5),
                  Line([x - tick, y0, 0], [x + tick, y0, 0], color=color, stroke_width=5),
                  Line([x - tick, y1, 0], [x + tick, y1, 0], color=color, stroke_width=5))


def tl(scene, mob, fn):
    """Drive a mobject's opacity from scene time: fn(t) -> 0..1."""
    mob.add_updater(lambda m: m.set_opacity(fn(scene.elapsed())))
    scene.add(mob)
    return mob


def ramp_in(t0, dur=0.5):
    return lambda t: min(1.0, max(0.0, (t - t0) / dur))


# --------------------------------------------------------------------------- single-channel traces

T_REC = 10.0
A_SCHED = [(0.5, 1.1), (2.1, 2.6), (3.7, 4.3), (5.4, 5.9), (7.0, 7.5)]


def make_drug(sched, k=2.0, T=T_REC):
    out, t = [], sched[0][0]
    for i, (a, b) in enumerate(sched):
        if t >= T:
            break
        out.append((t, min(T, t + (b - a) * k)))
        if i + 1 < len(sched):
            t = t + (b - a) * k + (sched[i + 1][0] - b)
    return out


DRUG_SCHED = make_drug(A_SCHED)
FRAC_A = sum(b - a for a, b in A_SCHED) / T_REC
FRAC_B = sum(b - a for a, b in DRUG_SCHED) / T_REC


def is_open(sched, t):
    return any(a <= t < b for a, b in sched)


def trace_mob(scheds, T, t, x0, x1, yb, yl, color=TEAL, width=6):
    X = lambda tt: x0 + tt / T * (x1 - x0)
    ts = sorted({0.0, float(T)} | {x for s in scheds for ab in s for x in ab if 0 < x < T})
    pts, prev = [], None
    for t0, t1 in zip(ts[:-1], ts[1:]):
        if t0 >= t:
            break
        lv = sum(is_open(s, (t0 + t1) / 2) for s in scheds)
        e = min(t1, t)
        y = yb + lv * yl
        if prev is None:
            pts.append([X(t0), y, 0])
        else:
            pts += [[X(t0), yb + prev * yl, 0], [X(t0), y, 0]]
        pts.append([X(e), y, 0])
        prev = lv
    if len(pts) < 2:
        pts = [[x0, yb, 0], [x0 + 0.02, yb, 0]]
    m = VMobject()
    m.set_points_as_corners(pts)
    m.set_stroke(color, width).set_fill(opacity=0)
    return m


def make_clock(T, rate):
    c = ValueTracker(0.0)
    c.on, c.rate = False, rate

    def f(m, dt):
        if m.on:
            m.set_value(min(T, m.get_value() + dt * m.rate))
    c.add_updater(f)
    return c


DX0, DX1 = -1.7, 3.7
SCR_CX, SCR_W = 1.0, 5.8
YA0, YA1, YA_B, STEP = 0.0, 3.5, 0.45, 2.25      # screen A: bottom, top, baseline
YB0, YB1, YB_B = -3.6, -0.2, -3.15               # screen B


def screen(y0, y1, cx=SCR_CX, w=SCR_W):
    return RoundedRectangle(corner_radius=0.12, width=w, height=y1 - y0, stroke_color=TEAL, stroke_width=3,
                            fill_color=BG, fill_opacity=0.92).move_to([cx, (y0 + y1) / 2, 0])


def baseline(yb, x0=DX0, x1=DX1):
    return DashedLine([x0, yb, 0], [x1, yb, 0], color=GREY, stroke_width=2, dash_length=0.12).set_opacity(0.7)


LP_CX = -4.55                                    # the left panel's channel
LP_OUT = [(-6.2, 1.5), (-3.2, 2.7), (-5.3, 2.95)]
LP_IN = [(-6.3, -1.2), (-5.4, -2.6), (-3.3, -1.5), (-4.2, -3.0), (-2.8, -2.6)]


def left_panel():
    f = fields(-6.8, -2.3)
    ch = Chan(LP_CX, 0.0, 0.78, 0.7, 0.34, 1.6)
    segs = membrane_segs(0.0, 0.78, -6.8, -2.3, [(LP_CX, ch.half)])
    outs, ins = dots_at(LP_OUT, ORANGE, 0.16), dots_at(LP_IN, ORANGE, 0.16)
    return VGroup(f, segs, outs, ins), ch


# --------------------------------------------------------------------------- the plot of S06 and S07

PX0, PY0 = 0.7, -2.6
PSX, PSY = 5.7 / 20.0, 5.4 / 60.0
S_PTS = (1, 4, 8, 12, 16, 20)
carrier_v = lambda S: 60.0 * S / (1.0 + S)
pore_v = lambda S: 2.5 * S
pxy = lambda S, v: np.array([PX0 + S * PSX, PY0 + v * PSY, 0.0])


def curve_mob(f, smax, color):
    if smax < 0.05:
        pts = [pxy(0, 0), pxy(0.02, f(0.02))]
    else:
        n = max(4, int(70 * smax / 20))
        pts = [pxy(s, f(s)) for s in np.linspace(0, smax, n)]
    m = VMobject()
    m.set_points_as_corners(pts)
    m.set_stroke(color, 7).set_fill(opacity=0)
    return m


def pts_mob(f, smax, color):
    return VGroup(*[mk_dot(color, 0.12, 1.0).move_to(pxy(s, f(s))) for s in S_PTS if s <= smax + 1e-6])


def plot_axes():
    xa = Line(pxy(0, 0), pxy(20, 0) + RIGHT * 0.15, color=GREY, stroke_width=4)
    ya = Line(pxy(0, 0), pxy(0, 60) + UP * 0.1, color=GREY, stroke_width=4)
    ticks = VGroup(*[M(str(s), 22, GREY).move_to(pxy(s, 0) + DOWN * 0.3) for s in (10, 20)],
                   *[M(str(v), 22, GREY).move_to(pxy(0, v) + LEFT * 0.35) for v in (30, 60)],
                   *[Line(pxy(s, 0) + DOWN * 0.08, pxy(s, 0) + UP * 0.08, color=GREY, stroke_width=3) for s in (10, 20)])
    lx = T("substrate (mM)", 28, TEXT).move_to([3.6, -3.5, 0])
    ly = T("initial rate", 28, TEXT).move_to([1.55, 3.5, 0])
    return VGroup(xa, ya, ticks, lx, ly)


# --------------------------------------------------------------------------- S00


def block(cx, cy, label="unknown", w=1.9, h=1.3):
    b = RoundedRectangle(corner_radius=0.16, width=w, height=h, color=BLUE, stroke_width=3,
                         fill_color=BLUE, fill_opacity=0.55).move_to([cx, cy, 0])
    t = T(label, 28, TEXT, weight=BOLD).move_to(b)
    return VGroup(b, t)


H0_X1 = 6.8
BLK1, BLK2 = -4.6, -1.5


def hook_world():
    f = fields(-6.8, H0_X1)
    segs = membrane_segs(0.0, 0.78, -6.8, H0_X1, [(BLK1, 0.95), (BLK2, 0.95)])
    b1, b2 = block(BLK1, 0), block(BLK2, 0)
    yel_out = dots_at([(-5.9, 2.5), (-3.2, 1.9), (-0.4, 2.7), (-2.2, 3.3)], YELLOW, 0.17, 0.14)
    yel_in = dots_at([(-5.6, -2.5), (-3.0, -2.0), (-0.5, -2.7), (-2.4, -3.2)], YELLOW, 0.17, 0.14)
    sod = dots_at([(-4.0, 3.2), (0.8, 2.2), (-6.1, -1.3), (1.0, -1.8)], SODIUM, 0.15, 0.12)
    return VGroup(f, segs, sod, yel_out, yel_in, b1, b2), (b1, b2), (yel_out, yel_in)


class S00LinkHook(SpokenScene):
    def construct(self):
        world, (b1, b2), (yo, yi) = hook_world()
        for b in (b1, b2):
            b.set_z_index(3)
        for d in list(yo) + list(yi):
            d.set_z_index(1)
        scr = RoundedRectangle(corner_radius=0.12, width=4.4, height=4.2, stroke_color=TEAL, stroke_width=3,
                               fill_color=BG, fill_opacity=0.95).move_to([4.5, 0.1, 0])
        base = baseline(-1.0, 2.5, 6.5)
        self.add(world, scr, base)
        self.at("which way")
        movers = [yo[0], yo[1], yo[2], yo[3]]
        targets = [(BLK1, -2.4), (BLK2, -2.4), (BLK1 + 0.6, -3.1), (BLK2 - 0.6, -3.1)]
        for m in movers:
            m.clear_updaters()
        self.play(*[m.animate.move_to([m.get_x() * 0.3 + tx * 0.7, 0, 0]) for m, (tx, ty) in zip(movers, targets)],
                  run_time=1.3)
        self.play(*[m.animate.move_to([tx, ty, 0]) for m, (tx, ty) in zip(movers, targets)], run_time=1.2)
        for m in movers:
            jit(m, 0.12, 3)
        self.at("so how can")
        ups = [yi[0], yi[1]]
        for m in ups:
            m.clear_updaters()
        self.play(ups[0].animate.move_to([BLK1, 0.0, 0]), ups[1].animate.move_to([BLK2, 0.0, 0]), run_time=1.1)
        self.play(ups[0].animate.move_to([BLK1 - 0.3, 2.0, 0]), ups[1].animate.move_to([BLK2 + 0.3, 2.0, 0]), run_time=1.1)
        for m in ups:
            jit(m, 0.12, 5)
        self.at("channel or a carrier")
        q = T("?", 110, TEXT, weight=BOLD).move_to([(BLK1 + BLK2) / 2, 1.6, 0])
        self.play(GrowFromCenter(q), run_time=1.0)
        self.at("watch the traffic")
        self.play(scr.animate(rate_func=there_and_back).set_stroke(TEAL, 10), run_time=0.8)
        tt = make_clock(10, 10 / 3.0)
        self.add(tt)
        tr = always_redraw(lambda: trace_mob([A_SCHED], 10, tt.get_value(), 2.5, 6.5, -1.0, 2.4, TEAL, 7))
        self.add(tr)
        tt.on = True
        self.at("not the protein's name")
        self.play(Indicate(q, color=TEAL, scale_factor=1.15), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Transport Across Membranes"
    TITLE = "Read the Traffic"


# --------------------------------------------------------------------------- S02


class S02TwoRoutes(SpokenScene):
    def construct(self):
        MH = 1.9
        f = fields(-6.8, 6.8, 0.0, MH)
        ch = Chan(0.0, 0.0, MH, 1.0, 0.55, 2.0, nflow=4, speed=0.4, rf=0.17)
        segs = membrane_segs(0.0, MH, -6.8, 6.8, [(0.0, ch.half)])
        # start closed: one blue block (the two halves touch), pore hidden
        ch.l.shift(RIGHT * 0.5)
        ch.r.shift(LEFT * 0.5)
        ch.pore.set_fill(opacity=0)
        ch.gate.set_fill(opacity=0).set_stroke(opacity=0)
        ch.flow.set_opacity(0)
        sod = dots_at([(-4.8, 2.7), (3.9, 2.8), (-5.5, -2.7), (5.0, -2.6)], SODIUM, 0.16, 0.12)
        yel = dots_at([(-3.2, 2.9), (3.0, 1.9), (-3.4, -2.9), (4.2, -1.9), (-5.9, 1.6), (5.9, -2.7)], YELLOW, 0.2, 0.12)
        k_out = dots_at([(-2.2, 1.7), (2.2, 2.9), (-5.6, -1.5)], ORANGE, 0.17, 0.12)
        sch = T("schematic", 26, GREY).move_to([5.7, -3.5, 0])
        self.add(f, segs, ch, sod, yel, k_out, sch)
        self.at("continuous")
        self.play(ch.l.animate.shift(LEFT * 0.5), ch.r.animate.shift(RIGHT * 0.5),
                  ch.pore.animate.set_fill(BLUE, opacity=0.34), run_time=1.5)
        lab1 = T("continuous pore", 30, BLUE, weight=BOLD).move_to([3.9, 0.0, 0])
        self.play(FadeIn(lab1), run_time=0.6)
        self.at("ions stream through")
        ch.activate()
        self.at("channel can switch")
        ch.o.set_value(1.0)
        ch.drive = None
        self.play(ch.o.animate.set_value(0.0), run_time=0.7)
        self.at("open and closed")
        self.play(ch.o.animate.set_value(1.0), run_time=0.6)
        self.wait(0.4)
        self.play(ch.o.animate.set_value(0.0), run_time=0.6)
        self.at("a carrier must finish")
        car = Carrier(0.0, 0.0, 1.0)
        car.activate()
        ch.clear_updaters()
        self.play(FadeOut(lab1), FadeTransform(ch, car), run_time=1.4)
        self.at("alternating access")
        lab2 = T("alternating access", 30, BLUE, weight=BOLD).move_to([3.9, 0.0, 0])
        self.play(FadeIn(lab2), run_time=0.6)
        self.at("opens to one side")
        cargo = yel[1]
        cargo.clear_updaters()
        cargo.set_z_index(4)
        self.play(cargo.animate.move_to([0.0, 1.6, 0]), run_time=0.8)
        self.play(cargo.animate.move_to([0.0, -0.05, 0]), run_time=0.8)
        self.at("closes around")
        self.play(car.p.animate.set_value(0.0), run_time=1.1)
        self.at("then opens to the other")
        self.play(car.p.animate.set_value(1.0), run_time=1.2)
        self.play(cargo.animate.move_to([0.0, -2.4, 0]), run_time=0.9)
        jit(cargo, 0.12, 2)
        self.at("that shape change")
        self.play(car.p.animate.set_value(-1.0), run_time=1.3)
        self.play(Indicate(car, color=BLUE, scale_factor=1.06), run_time=0.9)
        self.play(car.p.animate.set_value(0.0), run_time=0.7)
        self.finish()


# --------------------------------------------------------------------------- S03


class S03ChannelTrace(SpokenScene):
    def construct(self):
        panel, ch = left_panel()
        scr = screen(YA0, YA1)
        tt = make_clock(T_REC, T_REC / 22.4)
        ch.drive = lambda: float(is_open(A_SCHED, tt.get_value()))
        self.add(panel, ch, tt)
        ch.activate()
        self.play(FadeIn(scr, scale=0.92), run_time=1.0)
        base = baseline(YA_B)
        tr = always_redraw(lambda: trace_mob([A_SCHED], T_REC, tt.get_value(), DX0, DX1, YA_B, STEP))
        self.add(base, tr)
        tt.on = True
        self.at("millions of ions")
        self.play(Indicate(VGroup(ch.l, ch.r), color=TEAL, scale_factor=1.1), run_time=1.2)
        self.at("each jump marks")
        self.play(scr.animate(rate_func=there_and_back).set_stroke(TEAL, 10), run_time=1.0)
        self.at("the step height")
        br = vbrace(4.05, YA_B, YA_B + STEP)
        self.play(Create(br), run_time=0.8)
        self.at("unitary current")
        lab = T("unitary\ncurrent", 28, TEXT, line_spacing=0.8).move_to([5.45, YA_B + STEP / 2, 0])
        self.play(FadeIn(lab, shift=LEFT * 0.15), run_time=0.7)
        self.at("the fraction of recording")
        bar = Rectangle(width=DX1 - DX0, height=0.5, stroke_color=GREY, stroke_width=3,
                        fill_opacity=0).move_to([(DX0 + DX1) / 2, -0.95, 0])
        fill = always_redraw(lambda: VGroup(*[
            Rectangle(width=max(0.001, (min(b, tt.get_value()) - a) / T_REC * (DX1 - DX0)), height=0.5, stroke_width=0,
                      fill_color=GREEN, fill_opacity=0.85).move_to(
                [DX0 + (a + (min(b, tt.get_value()) - a) / 2) / T_REC * (DX1 - DX0), -0.95, 0])
            for a, b in A_SCHED if tt.get_value() > a]))
        self.play(FadeIn(bar), run_time=0.6)
        self.add(fill)
        self.at("open probability")
        frac = VGroup(T("open time", 30, GREEN, weight=BOLD), Line(LEFT * 1.2, RIGHT * 1.2, color=TEXT, stroke_width=4),
                      T("total time", 30, TEXT, weight=BOLD)).arrange(DOWN, buff=0.14).move_to([(DX0 + DX1) / 2, -2.45, 0])
        self.play(FadeIn(frac, shift=UP * 0.15), run_time=0.8)
        self.at("those are different")
        self.play(Indicate(br, color=YELLOW), Indicate(frac, color=GREEN), run_time=1.2)
        self.finish()


# --------------------------------------------------------------------------- S04 / S05 shared pieces


def stack_screens():
    return screen(YA0, YA1), screen(YB0, YB1)


HALO = "#0d1117"


def halo(m):
    m.set_z_index(30)
    m.set_stroke(color=HALO, width=9, opacity=1.0, background=True)
    return m


def trace_labels():
    return (halo(T("before", 28, TEXT, weight=BOLD).move_to([DX0 + 0.6, 3.22, 0])),
            halo(T("drug", 28, TEXT, weight=BOLD).move_to([DX0 + 0.45, -0.48, 0])))


class S04Predict(SpokenScene):
    def construct(self):
        panel, ch = left_panel()
        scrA, scrB = stack_screens()
        la, lb = trace_labels()
        trA = trace_mob([A_SCHED], T_REC, T_REC, DX0, DX1, YA_B, STEP)
        tt = make_clock(T_REC, T_REC / 10.4)
        ch.drive = lambda: float(is_open(DRUG_SCHED, tt.get_value()))
        self.add(panel, ch, scrA, baseline(YA_B), trA, la, tt)
        ch.activate()
        self.play(FadeIn(scrB, scale=0.92), FadeIn(lb), run_time=0.8)
        trB = always_redraw(lambda: trace_mob([DRUG_SCHED], T_REC, tt.get_value(), DX0, DX1, YB_B, STEP))
        self.add(baseline(YB_B), trB)
        tt.on = True
        self.at("keeps the same height")
        brA, brB = vbrace(4.05, YA_B, YA_B + STEP), vbrace(4.05, YB_B, YB_B + STEP)
        self.play(Create(brA), Create(brB), run_time=0.9)
        self.at("what changed")
        q = T("?", 90, TEXT, weight=BOLD).move_to([5.5, 2.5, 0])
        self.play(GrowFromCenter(q), run_time=0.7)
        q.add_updater(lambda m: m.set_opacity(0.75 + 0.25 * math.sin(3.0 * self.elapsed())))
        self.at("current through one open channel")
        c1 = chip("step height?", TEAL, 28).move_to([5.5, 0.9, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.6)
        self.at("open probability")
        c2 = chip("time open?", GREEN, 28).move_to([5.5, -0.5, 0])
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.6)
        self.at("decide from the trace")
        self.play(scrA.animate(rate_func=there_and_back).set_stroke(TEAL, 10), scrB.animate(rate_func=there_and_back).set_stroke(TEAL, 10), run_time=1.2)
        self.finish()


class S05Think(NarratedScene):
    """The question held still: both traces, both braces, the two answer chips, a pulsing question mark."""

    def construct(self):
        panel, ch = left_panel()
        scrA, scrB = stack_screens()
        la, lb = trace_labels()
        trA = trace_mob([A_SCHED], T_REC, T_REC, DX0, DX1, YA_B, STEP)
        trB = trace_mob([DRUG_SCHED], T_REC, T_REC, DX0, DX1, YB_B, STEP)
        brA, brB = vbrace(4.05, YA_B, YA_B + STEP), vbrace(4.05, YB_B, YB_B + STEP)
        q = T("?", 90, TEXT, weight=BOLD).move_to([5.5, 2.5, 0])
        c1 = chip("step height?", TEAL, 28).move_to([5.5, 0.9, 0])
        c2 = chip("time open?", GREEN, 28).move_to([5.5, -0.5, 0])
        tt = make_clock(T_REC, T_REC / 4.4)
        ch.drive = lambda: float(is_open(DRUG_SCHED, tt.get_value()))
        cur = always_redraw(lambda: VGroup(*[
            Line([DX0 + tt.get_value() / T_REC * (DX1 - DX0), y0 + 0.1, 0], [DX0 + tt.get_value() / T_REC * (DX1 - DX0), y1 - 0.1, 0],
                 color=TEXT, stroke_width=3) for y0, y1 in ((YA0, YA1), (YB0, YB1))]))
        self.add(panel, ch, scrA, scrB, baseline(YA_B), baseline(YB_B), trA, trB, la, lb, brA, brB, q, c1, c2, tt, cur)
        ch.activate()
        q.add_updater(lambda m: m.set_opacity(0.75 + 0.25 * math.sin(3.0 * self.elapsed())))
        tt.on = True
        self.finish()


# --------------------------------------------------------------------------- S06

MX_Y, MX_H = 1.9, 1.0
MX_CX = [-5.9, -4.5, -3.1, -1.7, -0.3]


def rand_sched(seed, T=T_REC, p_gap=(0.8, 2.4)):
    rng = random.Random(seed)
    out, t = [], rng.uniform(0, 1.5)
    while t < T:
        d = rng.uniform(0.4, 1.3)
        out.append((t, min(T, t + d)))
        t = t + d + rng.uniform(*p_gap)
    return out


MX_SCHEDS = [rand_sched(11 + i) for i in range(5)]


def multi_world(tw=None):
    f = fields(-6.8, 0.3, MX_Y, MX_H, bottom=0.0)
    chans = [Chan(c, MX_Y, MX_H, 0.4, 0.25, 1.3, nflow=3, speed=0.5, rf=0.12) for c in MX_CX]
    segs = membrane_segs(MX_Y, MX_H, -6.8, 0.3, [(c, chans[0].half) for c in MX_CX])
    if tw is not None:
        for ch, s in zip(chans, MX_SCHEDS):
            ch.drive = (lambda s=s: float(is_open(s, tw.get_value())))
    return f, segs, chans


class S06TraceAnswer(SpokenScene):
    def construct(self):
        panel, ch = left_panel()
        scrA, scrB = stack_screens()
        la, lb = trace_labels()
        trA = trace_mob([A_SCHED], T_REC, T_REC, DX0, DX1, YA_B, STEP)
        trB = trace_mob([DRUG_SCHED], T_REC, T_REC, DX0, DX1, YB_B, STEP)
        brA, brB = vbrace(4.05, YA_B, YA_B + STEP), vbrace(4.05, YB_B, YB_B + STEP)
        q = T("?", 90, TEXT, weight=BOLD).move_to([5.5, 2.5, 0])
        c1 = chip("step height?", TEAL, 28).move_to([5.5, 0.9, 0])
        c2 = chip("time open?", GREEN, 28).move_to([5.5, -0.5, 0])
        tt = make_clock(T_REC, T_REC / 9.0)
        ch.drive = lambda: float(is_open(DRUG_SCHED, tt.get_value()))
        cur = always_redraw(lambda: VGroup(*[
            Line([DX0 + tt.get_value() / T_REC * (DX1 - DX0), y0 + 0.1, 0], [DX0 + tt.get_value() / T_REC * (DX1 - DX0), y1 - 0.1, 0],
                 color=TEXT, stroke_width=3) for y0, y1 in ((YA0, YA1), (YB0, YB1))]))
        old = VGroup(panel, scrA, scrB, baseline(YA_B), baseline(YB_B), trA, trB, la, lb, brA, brB)
        self.add(old, ch, q, c1, c2, tt, cur)
        ch.activate()
        tt.on = True
        # --- part 1: the time-open bar
        self.play(FadeOut(q), c2[0].animate.set_fill(GREEN, opacity=0.55), run_time=0.6)
        bar = Rectangle(width=2.4, height=0.55, stroke_color=GREEN, stroke_width=3, fill_opacity=0).move_to([5.5, -0.5, 0])
        fv = ValueTracker(FRAC_A)
        fill = always_redraw(lambda: Rectangle(width=max(0.001, 2.4 * fv.get_value()), height=0.55, stroke_width=0,
                                               fill_color=GREEN, fill_opacity=0.85).move_to(
            [5.5 - 1.2 + 1.2 * fv.get_value(), -0.5, 0]))
        lab = T("time open", 28, GREEN, weight=BOLD).move_to([5.5, 0.1, 0])
        self.play(ReplacementTransform(c2, VGroup(bar, lab)), run_time=0.9)
        self.add(fill)
        self.at("the channel spent more")
        self.play(fv.animate.set_value(FRAC_B), run_time=1.6)
        self.at("unchanged step height")
        self.play(Indicate(brA, color=YELLOW, scale_factor=1.3), Indicate(brB, color=YELLOW, scale_factor=1.3), run_time=1.3)
        self.at("unitary current")
        self.play(FadeOut(c1), run_time=0.6)
        self.wait(0.3)
        # --- part 2: pull back to many channels
        self.at("whole cell current")
        tt.clear_updaters()
        ch.clear_updaters()
        cur.clear_updaters()
        self.remove(cur)
        tw = make_clock(T_REC, T_REC / 12.0)
        f, segs, chans = multi_world(tw)
        scrW = screen(0.3, 3.6, cx=3.95, w=5.3)
        sch = T("schematic", 26, GREY).move_to([-5.7, 0.3, 0])
        gone = VGroup(old, ch, fill, bar, lab)
        self.play(FadeOut(gone), FadeIn(VGroup(f, segs, *chans, scrW, sch)), run_time=1.2)
        self.add(tw)
        for c in chans:
            c.activate()
        wtr = always_redraw(lambda: trace_mob(MX_SCHEDS, T_REC, tw.get_value(), 1.5, 6.4, 0.6, 0.5, TEAL, 6))
        self.add(baseline(0.6, 1.5, 6.4), wtr)
        wl = T("whole-cell current", 28, TEAL, weight=BOLD).move_to([3.95, 0.0, 0])
        self.add(wl)
        tw.on = True

        def slider(y, name, color, v):
            nm = T(name, 28, color, weight=BOLD)
            nm.move_to([-6.6 + nm.width / 2, y, 0])
            tr = Line([-4.3, y, 0], [0.7, y, 0], color=GREY, stroke_width=5)
            kn = Circle(radius=0.19, stroke_width=0, fill_color=color, fill_opacity=1).move_to([-4.3 + 5.0 * v, y, 0])
            return VGroup(nm, tr), kn

        s1, k1 = slider(-0.95, "number", BLUE, 0.5)
        s2, k2 = slider(-1.95, "step", TEAL, 0.5)
        s3, k3 = slider(-2.95, "time open", GREEN, 0.5)
        self.at("channel number")
        self.play(FadeIn(VGroup(s1, k1)), Indicate(VGroup(*chans), color=BLUE, scale_factor=1.04), run_time=0.8)
        self.at("unitary current", nth=1)
        self.play(FadeIn(VGroup(s2, k2)), run_time=0.7)
        self.at("open probability", nth=1)
        self.play(FadeIn(VGroup(s3, k3)), run_time=0.7)
        self.at("it cannot separate")
        gbox = Rectangle(width=3.6, height=0.55, stroke_color=TEAL, stroke_width=3, fill_opacity=0).move_to([4.5, -1.95, 0])
        gfill = Rectangle(width=2.0, height=0.55, stroke_width=0, fill_color=TEAL, fill_opacity=0.85).move_to([4.5 - 1.8 + 1.0, -1.95, 0])
        glab = T("mean current", 28, TEAL, weight=BOLD).move_to([4.5, -1.2, 0])
        self.play(FadeIn(VGroup(gbox, gfill, glab)), run_time=0.6)
        self.play(k1.animate.shift(RIGHT * 1.5), k2.animate.shift(LEFT * 1.1), k3.animate.shift(LEFT * 0.7), run_time=1.5)
        self.finish()


# --------------------------------------------------------------------------- S07 / S08 vesicles

V1C, V2C, VRAD = (-4.0, 1.9), (-4.0, -1.9), 1.3


def ring_positions(c, flip):
    pts = []
    for i in range(16):
        a = i * 360 / 16 + 11
        if 65 <= a <= 115:
            continue
        x = c[0] + 1.8 * math.cos(math.radians(a))
        y = c[1] + 1.65 * math.sin(math.radians(a))
        pts.append((x, y))
    rng = random.Random(5)
    rng.shuffle(pts)
    return pts


def nvis(S):
    return int(round(2 + 12 * (S - 1) / 19.0))


class S07Saturation(SpokenScene):
    def construct(self):
        # the many channels of the last scene, rebuilt in the same place
        tw = make_clock(T_REC, 0.0)
        f, segs, chans = multi_world(tw)
        old = VGroup(f, segs, *chans)
        self.add(old, tw)
        for c in chans:
            c.activate()
        # two matched vesicles
        v1 = Circle(radius=VRAD, stroke_color=GREY, stroke_width=8, fill_color=GOLD, fill_opacity=0.2).move_to([*V1C, 0])
        v2 = Circle(radius=VRAD, stroke_color=GREY, stroke_width=8, fill_color=GOLD, fill_opacity=0.2).move_to([*V2C, 0])
        car = Carrier(V1C[0], V1C[1] + VRAD, 0.45)
        pore = Chan(V2C[0], V2C[1] + VRAD, 0.5, 0.3, 0.2, 0.8, nflow=2, speed=0.5, rf=0.09)
        t1 = T("carrier", 28, YELLOW, weight=BOLD).move_to([*V1C, 0])
        t2 = T("pore", 28, ORANGE, weight=BOLD).move_to([*V2C, 0])
        new = VGroup(v1, v2, car, pore, t1, t2)
        self.play(FadeTransform(old, new), run_time=1.6)
        for c in chans:
            c.clear_updaters()
        car.activate(2.6)
        pore.activate()
        S = ValueTracker(1.0)
        S.free = False
        S.t = 0.0

        def sfree(m, dt):
            if m.free:
                m.t += dt
                m.set_value(1 + 19 * (0.5 - 0.5 * math.cos(2 * math.pi * m.t / 9.0)))
        S.add_updater(sfree)
        self.add(S)
        cargo = mk_dot(YELLOW, 0.11).move_to([car.cx, car.cy, 0]).set_z_index(5)
        cargo.add_updater(lambda m: m.move_to([car.cx, car.cy + 0.04 * car.p.get_value(), 0]).set_fill(YELLOW, opacity=min(1.0, (S.get_value() - 1) / 5.0)))
        self.add(cargo)
        subs = []
        for idx, (c, flip) in enumerate(((V1C, False), (V2C, True))):
            pos = ring_positions(c, flip)
            g = VGroup()
            for i, p in enumerate(pos[:14]):
                d = jit(mk_dot(YELLOW, 0.16).move_to([p[0], p[1], 0]), 0.1, i + 1 + 7 * idx)
                d.idx = i
                d.add_updater(lambda m: m.set_fill(YELLOW, opacity=0.95 if m.idx < nvis(S.get_value()) else 0.0), call_updater=True)
                g.add(d)
            subs.append(g)
        self.add(*subs)
        self.at("a different signature")
        ax = plot_axes()
        self.play(Create(ax), run_time=1.8)
        self.at("substrate concentration")
        Sc = ValueTracker(0.0)
        cc = always_redraw(lambda: curve_mob(carrier_v, Sc.get_value(), YELLOW))
        cp = always_redraw(lambda: pts_mob(carrier_v, Sc.get_value(), YELLOW))
        self.add(cc, cp)
        self.play(S.animate.set_value(20), Sc.animate.set_value(20), run_time=5.6, rate_func=linear)
        self.at("the rate bends toward")
        vline = DashedLine(pxy(0, 60), pxy(20, 60), color=YELLOW, stroke_width=3, dash_length=0.15)
        vlab = T("Vmax", 30, YELLOW, weight=BOLD).move_to([5.75, 3.15, 0])
        self.play(Create(vline), FadeIn(vlab), run_time=1.0)
        self.at("or simple diffusion")
        Sp = ValueTracker(0.0)
        pc = always_redraw(lambda: curve_mob(pore_v, Sp.get_value(), ORANGE))
        pp = always_redraw(lambda: pts_mob(pore_v, Sp.get_value(), ORANGE))
        td = halo(T("teaching data", 28, TEXT).move_to([4.8, -2.15, 0]))
        self.add(pc, pp)
        self.play(Sp.animate.set_value(20), FadeIn(td), run_time=3.8, rate_func=linear)
        S.free, S.t = True, 4.5
        probe = always_redraw(lambda: VGroup(
            DashedLine(pxy(S.get_value(), 0), pxy(S.get_value(), carrier_v(S.get_value())), color=TEXT, stroke_width=2, dash_length=0.1).set_opacity(0.6),
            mk_dot(YELLOW, 0.16, 1.0).move_to(pxy(S.get_value(), carrier_v(S.get_value()))),
            mk_dot(ORANGE, 0.16, 1.0).move_to(pxy(S.get_value(), pore_v(S.get_value()))),
        ))
        self.add(probe)
        self.at("channels can saturate")
        hi = halo(T("saturate at much\nhigher S", 28, ORANGE, line_spacing=0.8).move_to([5.0, -1.3, 0]))
        self.play(FadeIn(hi), run_time=1.0)
        self.at("saturation points toward")
        self.play(FadeOut(hi), run_time=0.6)
        self.at("evidence not proof")
        ev = halo(T("evidence,\nnot proof", 28, TEXT, line_spacing=0.8).move_to([3.2, 1.0, 0]))
        self.play(FadeIn(ev), run_time=0.7)
        self.finish()


# --------------------------------------------------------------------------- S08 / S09 the tracer vesicle

VC, VR = (-2.2, 0.1), 2.6
IN_DOTS = [(-4.3, 3.3), (-0.2, 3.3), (-3.3, 3.55), (-1.1, 3.55), (-5.1, 2.2)]           # outside, near the top carrier
OUT_EXTRA = [(-5.9, -0.2), (0.7, -0.8), (0.5, 2.5)]
OUT_DOTS = [(-3.1, -1.3), (-1.3, -1.3), (-2.2, -0.7), (-3.6, -0.1), (-0.9, -0.1)]       # inside, near the bottom carrier
IN_EXTRA = [(-3.2, 0.9), (-1.2, 0.9), (-2.2, 0.25)]
IN_TARGET = [(-3.0, 1.7), (-1.4, 1.7), (-2.2, 1.45), (-3.7, 1.3), (-0.7, 1.3)]
OUT_TARGET = [(-4.1, -3.35), (-0.3, -3.35), (-3.2, -3.55), (-1.2, -3.55), (-5.0, -2.6)]


def tdot(p, tagged=False):
    body = mk_dot(YELLOW, 0.17)
    badge = Circle(radius=0.085, stroke_color=BG, stroke_width=2, fill_color=TEAL, fill_opacity=1).move_to(body.get_center() + np.array([0.14, 0.14, 0]))
    g = VGroup(body, badge).move_to([p[0], p[1], 0])
    g.body, g.badge = body, badge
    badge.set_opacity(1 if tagged else 0)
    g.set_z_index(5)
    return g


def ves_core():
    ring = Circle(radius=VR, stroke_color=GREY, stroke_width=8, fill_color=GOLD, fill_opacity=0.2).move_to([*VC, 0])
    top = Carrier(VC[0], VC[1] + VR, 0.5)
    bot = Carrier(VC[0], VC[1] - VR, 0.5)
    return ring, top, bot


def gauge(x, color, label, frac, y0=-2.5, y1=1.8, w=0.9):
    box = Rectangle(width=w, height=y1 - y0, stroke_color=color, stroke_width=3, fill_opacity=0).move_to([x, (y0 + y1) / 2, 0])
    lab = T(label, 28, color, weight=BOLD, line_spacing=0.8).move_to([x, y0 - 0.65, 0])
    fill = always_redraw(lambda: Rectangle(width=w, height=max(0.001, (y1 - y0) * frac.get_value()), stroke_width=0,
                                           fill_color=color, fill_opacity=0.85).move_to(
        [x, y0 + (y1 - y0) * frac.get_value() / 2, 0]))
    return VGroup(box, lab), fill


def run_trip(scene, top, bot, d_in, d_out, in_t, out_t, hook=None):
    """One exchange trip: one dot in through the top carrier, one dot out through the bottom one (3.3 s)."""
    top.period = bot.period = None
    d_in.clear_updaters()
    d_out.clear_updaters()
    scene.play(d_in.animate.move_to([top.cx, top.cy - 0.05, 0]), d_out.animate.move_to([bot.cx, bot.cy - 0.05, 0]),
               top.p.animate.set_value(-1), bot.p.animate.set_value(-1), run_time=0.8)
    scene.play(top.p.animate.set_value(1), bot.p.animate.set_value(1), run_time=1.1)
    scene.play(d_in.animate.move_to([in_t[0], in_t[1], 0]), d_out.animate.move_to([out_t[0], out_t[1], 0]), run_time=0.8)
    if hook:
        hook()
    jit(d_in, 0.12, 4)
    jit(d_out, 0.12, 6)
    scene.play(top.p.animate.set_value(-1), bot.p.animate.set_value(-1), run_time=0.6)


class S08Tracer(SpokenScene):
    def construct(self):
        # the plot of the last scene, rebuilt, turns into the vesicle
        ax = plot_axes()
        cc = curve_mob(carrier_v, 20, YELLOW)
        pc = curve_mob(pore_v, 20, ORANGE)
        old = VGroup(ax, cc, pc, pts_mob(carrier_v, 20, YELLOW), pts_mob(pore_v, 20, ORANGE))
        self.add(old)
        ring, top, bot = ves_core()
        outs = [tdot(p) for p in IN_DOTS + OUT_EXTRA]
        ins = [tdot(p) for p in OUT_DOTS + IN_EXTRA]
        for i, d in enumerate(outs + ins):
            jit(d, 0.12, i + 1)
        new = VGroup(ring, top, bot, *outs, *ins)
        self.play(FadeTransform(old, new), run_time=1.6)
        top.activate(4.0, -1.0, -0.5)
        bot.activate(4.0, -1.0, -0.5)
        # one dot gains a tag badge (the example), then loses it again before the experiment
        ex = outs[5]
        tl(self, ex.badge, lambda t: ramp_in(1.9)(t) * (1.0 if t < 6.3 else max(0.0, 1.0 - (t - 6.3) / 0.5)))
        for i in (6, 7):
            tl(self, outs[i].badge, lambda t: ramp_in(17.6)(t))
        for i in (2, 3, 4):
            tl(self, outs[i].badge, lambda t: ramp_in(17.6)(t))
        taglab = T("tagged", 28, TEAL, weight=BOLD).move_to([-5.9, 0.4, 0])
        tl(self, taglab, lambda t: ramp_in(2.0)(t) * (1.0 if t < 6.3 else max(0.0, 1.0 - (t - 6.3) / 0.5)))
        self.at("some substrate molecules")
        self.at("the counter sees")
        tagf = ValueTracker(0.0)
        totf = ValueTracker(0.5)
        g1, f1 = gauge(3.9, TEAL, "tag\ncount", tagf)
        g2, f2 = gauge(5.7, TEXT, "total\ninside", totf)
        self.play(FadeIn(g1), run_time=0.7)
        self.add(f1)
        self.at("the total amount inside")
        self.play(FadeIn(g2), run_time=0.7)
        self.add(f2)
        eq = T("equal inside\nand outside", 28, TEXT, line_spacing=0.8).move_to([4.8, 2.9, 0])
        tl(self, eq, ramp_in(13.4))
        self.at("take carrier vesicles")
        # untagged exchange first: one in, one out, again and again
        def bump():
            tagf.set_value(min(1.0, tagf.get_value() + 0.2))
        run_trip(self, top, bot, outs[0], ins[0], IN_TARGET[0], OUT_TARGET[0])
        run_trip(self, top, bot, outs[1], ins[1], IN_TARGET[1], OUT_TARGET[1])
        run_trip(self, top, bot, outs[2], ins[2], IN_TARGET[2], OUT_TARGET[2], bump)
        run_trip(self, top, bot, outs[3], ins[3], IN_TARGET[3], OUT_TARGET[3], bump)
        run_trip(self, top, bot, outs[4], ins[4], IN_TARGET[4], OUT_TARGET[4], bump)
        top.activate(4.0, -1.0, -0.5)
        bot.activate(4.0, -1.0, -0.5)
        self.at("supplies what the tracer")
        self.play(Indicate(g2, color=TEXT, scale_factor=1.06), run_time=1.4)
        self.play(Indicate(g1, color=TEAL, scale_factor=1.06), run_time=1.4)
        self.finish()


# --------------------------------------------------------------------------- S09


def seesaw(cx, cy):
    beam = Line([cx - 1.5, cy, 0], [cx + 1.5, cy, 0], color=TEXT, stroke_width=6)
    dl, dr = tdot((cx - 1.2, cy + 0.3), True), tdot((cx + 1.2, cy + 0.3), False)
    g = VGroup(beam, dl, dr)
    g.ang = 0.0

    def f(m, dt):
        new = 0.05 * math.sin(2.2 * m.t_)
        m.t_ += dt
        m.rotate(new - m.ang, about_point=np.array([cx, cy, 0]))
        m.ang = new
    g.t_ = 0.0
    g.add_updater(f)
    fulcrum = Triangle(stroke_width=0, fill_color=GREY, fill_opacity=0.9).scale(0.24).move_to([cx, cy - 0.28, 0])
    return VGroup(g, fulcrum)


def tile_frame(cx, cy, label, color, w=2.4, h=2.5):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=BG, fill_opacity=0.95).move_to([cx, cy, 0])
    lab = T(label, 28, color, weight=BOLD).move_to([cx, cy + h / 2 - 0.42, 0])
    return VGroup(box, lab)


def tile_counter(cx, cy):
    g = tile_frame(cx, cy, "rate", TEAL)
    box = Rectangle(width=0.8, height=1.5, stroke_color=TEAL, stroke_width=3, fill_opacity=0).move_to([cx, cy - 0.35, 0])
    fill = Rectangle(width=0.8, height=0.2, stroke_width=0, fill_color=TEAL, fill_opacity=0.85)
    fill.t_ = 0.0

    def f(m, dt):
        m.t_ += dt
        h = 1.5 * ((m.t_ % 2.2) / 2.2) + 0.05
        m.stretch_to_fit_height(h)
        m.move_to([cx, cy - 1.1 + h / 2, 0])
    fill.add_updater(f)
    g.add(box, fill)
    return g


def tile_exchange(cx, cy):
    g = tile_frame(cx, cy, "exchange", YELLOW)
    up = Arrow([cx - 0.5, cy - 0.95, 0], [cx - 0.5, cy + 0.55, 0], buff=0, color=YELLOW, stroke_width=7, tip_length=0.25)
    dn = Arrow([cx + 0.5, cy + 0.55, 0], [cx + 0.5, cy - 0.95, 0], buff=0, color=TEAL, stroke_width=7, tip_length=0.25)
    d1, d2 = mk_dot(YELLOW, 0.11, 1.0), mk_dot(TEAL, 0.11, 1.0)
    d1.t_ = d2.t_ = 0.0

    def mv(sign, x):
        def f(m, dt):
            m.t_ += dt
            u = (m.t_ / 1.8) % 1.0
            y = cy - 0.95 + 1.5 * u if sign > 0 else cy + 0.55 - 1.5 * u
            m.move_to([x, y, 0])
        return f
    d1.add_updater(mv(1, cx - 0.5))
    d2.add_updater(mv(-1, cx + 0.5))
    g.add(up, dn, d1, d2)
    return g


def tile_curve(cx, cy):
    g = tile_frame(cx, cy, "saturation", YELLOW)
    x0, y0, w, h = cx - 0.85, cy - 0.95, 1.7, 1.35
    pts = [[x0 + w * s / 20.0, y0 + h * carrier_v(s) / 60.0, 0] for s in np.linspace(0, 20, 40)]
    c = VMobject()
    c.set_points_as_corners(pts)
    c.set_stroke(YELLOW, 6).set_fill(opacity=0)
    ax = VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=GREY, stroke_width=3), Line([x0, y0, 0], [x0, y0 + h, 0], color=GREY, stroke_width=3))
    d = mk_dot(TEXT, 0.1, 1.0)
    d.t_ = 0.0

    def f(m, dt):
        m.t_ += dt
        s = 20 * (0.5 - 0.5 * math.cos(2 * math.pi * m.t_ / 5.0))
        m.move_to([x0 + w * s / 20.0, y0 + h * carrier_v(s) / 60.0, 0])
    d.add_updater(f)
    g.add(ax, c, d)
    return g


def tile_steps(cx, cy):
    g = tile_frame(cx, cy, "steps", TEAL)
    x0, x1, yb = cx - 0.95, cx + 0.95, cy - 0.95
    tr = trace_mob([A_SCHED], T_REC, T_REC, x0, x1, yb, 1.1, TEAL, 5)
    cur = Line([x0, yb - 0.1, 0], [x0, yb + 1.25, 0], color=TEXT, stroke_width=3)
    cur.t_ = 0.0

    def f(m, dt):
        m.t_ += dt
        x = x0 + (x1 - x0) * ((m.t_ / 5.0) % 1.0)
        m.put_start_and_end_on([x, yb - 0.1, 0], [x, yb + 1.25, 0])
    cur.add_updater(f)
    g.add(tr, cur)
    return g


class S09ExchangeRead(SpokenScene):
    def construct(self):
        ring, top, bot = ves_core()
        outs = [tdot(p, True) for p in IN_DOTS[:3] + OUT_EXTRA]
        ins = [tdot(p) for p in OUT_DOTS[:4] + IN_EXTRA[:2]] + [tdot(p, True) for p in IN_TARGET[:3]]
        for i, d in enumerate(outs + ins):
            jit(d, 0.12, i + 1)
        tagf, totf = ValueTracker(0.6), ValueTracker(0.5)
        g1, f1 = gauge(3.9, TEAL, "tag\ncount", tagf)
        g2, f2 = gauge(5.7, TEXT, "total\ninside", totf)
        self.add(ring, top, bot, *outs, *ins, g1, f1, g2, f2)
        top.activate()
        bot.activate()
        ss = seesaw(4.8, 2.55)
        sl = T("one in / one out", 28, TEXT, weight=BOLD).move_to([4.8, 3.45, 0])
        self.play(FadeIn(ss), run_time=0.9)
        self.at("not net uptake")
        self.play(FadeIn(sl), run_time=0.6)
        self.at("label has its own")
        self.play(Indicate(VGroup(*outs), color=TEAL, scale_factor=1.15), run_time=1.0)

        def bump():
            tagf.set_value(min(1.0, tagf.get_value() + 0.2))
        run_trip(self, top, bot, outs[0], ins[0], IN_TARGET[3], OUT_TARGET[0], bump)
        self.at("total substrate stays level")
        self.play(Indicate(g2, color=TEXT, scale_factor=1.06), run_time=1.0)
        warn = VGroup(Triangle(stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.9).scale(0.34),
                      T("!", 28, RED, weight=BOLD)).move_to([2.8, 1.2, 0])
        warn[1].set_color(BG).move_to(warn[0].get_center() + DOWN * 0.04)
        warn[0].set_fill(RED, opacity=0.9)
        tl(self, warn, ramp_in(self.t_of("never proves") - 0.2))
        self.at("a rising count alone")
        run_trip(self, top, bot, outs[1], ins[1], IN_TARGET[4], OUT_TARGET[1], bump)
        # four evidence tiles
        self.at("so measure the total")
        self.play(Indicate(g2, color=TEXT, scale_factor=1.06), run_time=1.0)
        self.at("combine exchange")
        self.remove(f1, f2)
        self.play(FadeOut(VGroup(g1, g2, ss, sl)), run_time=0.6)
        for m in (top, bot):
            m.clear_updaters()
        tx = tile_exchange(2.7, -1.45)
        self.play(FadeIn(tx, scale=0.9), run_time=0.7)
        tc = tile_counter(2.7, 1.45)
        self.play(FadeIn(tc, scale=0.9), warn.animate.move_to([0.9, 1.45, 0]), run_time=0.8)
        self.at("saturation")
        tr = tile_curve(5.3, 1.45)
        self.play(FadeIn(tr, scale=0.9), run_time=0.7)
        self.at("single channel steps")
        ts = tile_steps(5.3, -1.45)
        self.play(FadeIn(ts, scale=0.9), run_time=0.7)
        self.at("instead of trusting")
        outline = RoundedRectangle(corner_radius=0.2, width=5.5, height=5.9, stroke_color=BLUE, stroke_width=6,
                                   fill_opacity=0).move_to([4.0, 0.0, 0])
        ml = T("mechanism", 34, BLUE, weight=BOLD).move_to([4.0, 3.45, 0])
        self.play(Create(outline), FadeIn(ml), run_time=1.2)
        self.finish()


# --------------------------------------------------------------------------- S10


class S10Return(SpokenScene):
    def construct(self):
        CY = 0.4
        f = fields(-6.8, 6.8, CY, 0.78)
        PXC, CXC = -3.3, 2.6
        pore = Chan(PXC, CY, 0.78, 0.7, 0.4, 1.4, nflow=3)
        car = Carrier(CXC, CY, 0.7)
        segs = membrane_segs(CY, 0.78, -6.8, 6.8, [(PXC, pore.half), (CXC, 0.75)])
        k_dots = dots_at([(-5.5, 2.0), (-1.6, 2.0), (-4.6, -1.6), (-1.9, -2.0)], ORANGE, 0.16, 0.12)
        y_dots = dots_at([(0.6, 1.9), (4.9, 2.0), (0.9, -0.8), (5.6, -1.0)], YELLOW, 0.17, 0.12)
        pore.o.set_value(1.0)
        pore.l.set_fill(opacity=0.7)
        lp = halo(T("unknown", 28, TEXT, weight=BOLD).move_to([PXC, CY + 1.0, 0]))
        lc = halo(T("unknown", 28, TEXT, weight=BOLD).move_to([CXC, CY + 1.0, 0]))
        q = T("?", 100, TEXT, weight=BOLD).move_to([-0.35, 2.0, 0])
        # the cargo that rides the carrier
        cargo = mk_dot(YELLOW, 0.14, 1.0).set_z_index(5)
        cargo.t_ = 0.0

        def cg(m, dt):
            m.t_ += dt
            u = (m.t_ / 3.2) % 1.0
            car.p.set_value(-math.cos(2 * math.pi * u))
            if u < 0.2:
                y, o = CY + 1.0 * (1 - u / 0.2), min(1.0, u * 12)
            elif u < 0.5:
                y, o = CY, 1.0
            elif u < 0.75:
                y, o = CY - 1.0 * (u - 0.5) / 0.25, 1.0
            else:
                y, o = CY - 1.0, max(0.0, 1 - (u - 0.75) * 10)
            m.move_to([CXC, y - 0.03, 0]).set_fill(YELLOW, opacity=o)
        cargo.add_updater(cg)
        self.add(f, segs, k_dots, y_dots, pore, car, lp, lc, q, cargo)
        pore.activate()
        car.activate()
        # the energy hill from chapter 1
        hill = Line([-2.0, 3.35, 0], [2.0, 2.65, 0], color=TEXT, stroke_width=9)
        hl = VGroup(T("OUT", 24, GREY).next_to(hill.get_start(), LEFT, buff=0.2), T("IN", 24, GREY).next_to(hill.get_end(), RIGHT, buff=0.2))
        ball = mk_dot(ORANGE, 0.2, 1.0).move_to(hill.point_from_proportion(0.04) + UP * 0.28)
        hg = VGroup(hill, hl, ball)
        self.at("hill from chapter 1")
        self.play(Create(hill), FadeIn(hl), FadeIn(ball), run_time=1.0)
        self.at("which way traffic")
        self.play(ball.animate.move_to(hill.point_from_proportion(0.94) + UP * 0.28), run_time=1.8)
        self.at("the pattern of that traffic")
        hdr = T("energy hill", 28, TEXT).move_to([-3.3, 3.45, 0])
        self.play(hg.animate.scale(0.5).move_to([0, 3.45, 0]), FadeOut(hl), FadeIn(hdr), run_time=1.2)
        self.at("reveals the route")
        self.play(Indicate(q, color=TEAL, scale_factor=1.15), run_time=1.0)
        self.at("square steps")
        tsq = tile_steps(PXC, -2.15)
        l1 = Line([PXC, -0.95, 0], [PXC, CY - 0.4, 0], color=TEAL, stroke_width=4)
        self.play(FadeIn(tsq, shift=UP * 0.2), Create(l1), run_time=1.0)
        self.at("pore", nth=0)
        newp = halo(T("pore", 30, BLUE, weight=BOLD).move_to(lp))
        self.play(Transform(lp, newp), run_time=0.7)
        self.at("saturation and exchange")
        tsa = tile_curve(0.9, -2.15)
        l2 = Line([0.9, -0.95, 0], [CXC - 0.2, CY - 0.4, 0], color=TEAL, stroke_width=4)
        self.play(FadeIn(tsa, shift=UP * 0.2), Create(l2), run_time=0.9)
        tex = tile_exchange(4.3, -2.15)
        l3 = Line([4.3, -0.95, 0], [CXC + 0.2, CY - 0.4, 0], color=TEAL, stroke_width=4)
        self.play(FadeIn(tex, shift=UP * 0.2), Create(l3), run_time=0.9)
        self.at("toward a carrier")
        newc = halo(T("carrier", 30, BLUE, weight=BOLD).move_to(lc))
        self.play(Transform(lc, newc), run_time=0.7)
        self.at("mechanism lives in")
        ck = VGroup(Line([-0.75, 1.9, 0], [-0.45, 1.5, 0], color=TEAL, stroke_width=14),
                    Line([-0.45, 1.5, 0], [0.2, 2.5, 0], color=TEAL, stroke_width=14)).move_to([-0.35, 2.0, 0])
        self.play(ReplacementTransform(q, ck), run_time=1.0)
        self.at("not the family name")
        self.play(Indicate(ck, color=TEAL, scale_factor=1.2), run_time=1.0)
        self.finish()


class S11End(EndCard):
    LINE = "Read the traffic pattern, not the protein's label."
