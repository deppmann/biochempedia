"""The Last Gas the Blood Touches (gas exchange, film 1).

COLOUR MAP (same in every scene and in film 2)
  water or air = BLUE         blood = RED
  oxygen = GOLD dots (density = PO2 within that stream only); total oxygen per litre only as a separate bar
  barrier = GREY strip        diffusion arrows = thin GOLD
Every plotted curve is computed from a linear exchanger model (equal oxygen-carrying flows of water and blood).
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

# ------------------------------------------------------------------ shared geometry
X0, X1 = -5.0, 5.0
GEO = (1.95, 3.25, 1.65, 1.95, 0.35, 1.65)      # water y0,y1 ; strip y0,y1 ; blood y0,y1  (compact lamella, top of frame)
PY0, PY1 = -3.15, -0.45                          # plot: value 0 and value 100


def px(s):
    return X0 + s * (X1 - X0)


def py(v):
    return PY0 + (PY1 - PY0) * v / 100.0


def clock(scene):
    tr = ValueTracker(0)
    tr.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(tr)
    return tr


# ------------------------------------------------------------------ exchanger models (values 0..100, s = 0..1 along the plate)
def same_model(k):
    return (lambda s: 50 + 50 * math.exp(-2 * k * s)), (lambda s: 50 - 50 * math.exp(-2 * k * s))


def counter_model(k):
    kk = k if callable(k) else (lambda: k)

    def D():
        return 100.0 / (1 + kk())
    pw = lambda s: 100 - kk() * D() * s
    pb = lambda s: 100 - kk() * D() * s - D()
    return pw, pb


# ------------------------------------------------------------------ helpers
def march(p0, p1, color=BLUE, n=5, speed=0.8, r=0.07, op=1.0):
    p0 = np.array(p0, float)
    p1 = np.array(p1, float)
    L = max(np.linalg.norm(p1 - p0), 1e-3)
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    for i, d in enumerate(g):
        d.s = i / n

    def upd(m, dt):
        for d in m:
            d.s = (d.s + dt * speed / L) % 1
            d.move_to(p0 + (p1 - p0) * d.s)
            d.set_opacity(op * min(1, d.s * 6, (1 - d.s) * 6))
    g.add_updater(upd)
    upd(g, 0)
    return g


def stream(x0, x1, ylo, yhi, fn, sp=None, n=56, speed=0.085, seed=1, r=0.08):
    rng = random.Random(seed)
    g = VGroup()
    for i in range(n):
        d = Dot(radius=r, color=GOLD)
        d.s = (i + rng.random()) / n
        d.f = ylo + (yhi - ylo) * (0.12 + 0.76 * rng.random())
        d.thr = rng.random()
        d.v = speed * (0.85 + 0.3 * rng.random())
        g.add(d)
    g.sp = sp if sp is not None else ValueTracker(1)

    def upd(m, dt):
        k = m.sp.get_value()
        for d in m:
            d.s = (d.s + dt * d.v * k) % 1
            d.move_to([x0 + d.s * (x1 - x0), d.f, 0])
            vis = d.thr < 0.07 + 0.93 * max(0.0, min(1.0, fn(d.s) / 100.0))
            d.set_fill(GOLD, opacity=1.0 if vis else 0.0)
    g.add_updater(upd)
    upd(g, 0)
    return g


def band(x0, x1, y0, y1, color, op=0.16):
    return Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0, fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def lam(pw, pb, geo=GEO, x0=X0, x1=X1, bdir=1, n=56, seed=3, wdots=None, bdots=None):
    """One lamella: BLUE water band on top, GREY strip, RED blood band below, gold dots whose density follows pw / pb."""
    wy0, wy1, sy0, sy1, by0, by1 = geo
    wb = band(x0, x1, wy0, wy1, BLUE)
    bb = band(x0, x1, by0, by1, RED)
    st = Rectangle(width=x1 - x0, height=sy1 - sy0, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([(x0 + x1) / 2, (sy0 + sy1) / 2, 0])
    L = x1 - x0
    wm, bm = (wy0 + wy1) / 2, (by0 + by1) / 2
    wa = VGroup(*[Arrow([x - 0.5, wm, 0], [x + 0.5, wm, 0], buff=0, color=BLUE, stroke_width=5, tip_length=0.22).set_opacity(0.5) for x in (x0 + 0.2 * L, x0 + 0.5 * L, x0 + 0.8 * L)])
    ba = VGroup(*[Arrow([x - 0.5 * bdir, bm, 0], [x + 0.5 * bdir, bm, 0], buff=0, color=RED, stroke_width=5, tip_length=0.22).set_opacity(0.5) for x in (x0 + 0.2 * L, x0 + 0.5 * L, x0 + 0.8 * L)])
    wsp, bsp = ValueTracker(1), ValueTracker(bdir)
    wd = stream(x0, x1, wy0, wy1, pw, sp=wsp, n=n, seed=seed)
    bd = stream(x0, x1, by0, by1, pb, sp=bsp, n=n, seed=seed + 7)
    g = VGroup(wb, bb, st, wa, ba, wd, bd)
    g.wa, g.ba, g.wd, g.bd, g.wsp, g.bsp, g.st, g.wb, g.bb = wa, ba, wd, bd, wsp, bsp, st, wb, bb
    return g


def gauge(x, y0, h, color, src, w=0.42):
    box = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3).move_to([x, y0 + h / 2, 0])
    fill = Rectangle(width=w - 0.08, height=0.01, stroke_width=0, fill_color=color, fill_opacity=0.9)

    def upd(m):
        v = max(0.004, min(1.0, src()))
        m.become(Rectangle(width=w - 0.08, height=v * h, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, y0 + v * h / 2, 0]))
    fill.add_updater(upd)
    upd(fill)
    g = VGroup(box, fill)
    g.x, g.y0, g.h = x, y0, h
    return g


def vbar(x, base, h, color=GOLD, w=0.9, op=0.55):
    return Rectangle(width=w, height=max(h, 0.05), stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to([x, base + max(h, 0.05) / 2, 0])


def dial(y, label, tr, x0=-3.6, x1=-0.4, lx=-6.6, size=28, color=TEAL):
    track = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=7)
    done = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=7)
    done.add_updater(lambda m: m.put_start_and_end_on([x0, y, 0], [x0 + (x1 - x0) * max(tr.get_value(), 0.001), y, 0]))
    knob = Dot(radius=0.2, color=color)
    knob.add_updater(lambda m: m.move_to([x0 + (x1 - x0) * tr.get_value(), y, 0]))
    lab = T(label, size)
    lab.move_to([lx + lab.width / 2, y, 0])
    return VGroup(lab, track, done, knob)


def drift_dots(center_fn, pts, clk, color=GOLD, r=0.06, op=1.0, amp=0.12, seed=0):
    rng = random.Random(seed)
    g = VGroup(*[Dot(radius=r, color=color) for _ in pts])
    for d, p in zip(g, pts):
        d.p = np.array(p, float)
        d.ph = (rng.random() * 6.28, rng.random() * 6.28)
        d.w = (0.8 + rng.random(), 0.8 + rng.random())

    def upd(m):
        t = clk.get_value()
        c = np.array(center_fn(), float)
        for d in m:
            d.move_to(c + d.p + np.array([amp * math.sin(d.w[0] * t + d.ph[0]), amp * math.cos(d.w[1] * t + d.ph[1]), 0]))
            d.set_opacity(op)
    g.add_updater(upd)
    upd(g)
    return g


def disc_pts(R, n, seed=0):
    rng = random.Random(seed)
    pts = []
    while len(pts) < n:
        x, y = rng.uniform(-R, R), rng.uniform(-R, R)
        if x * x + y * y < R * R:
            pts.append([x, y, 0])
    return pts


def curve(fn, color, p, width=7):
    c = VMobject(stroke_color=color, stroke_width=width)

    def upd(m):
        pp = max(p.get_value(), 0.004)
        pts = [[px(s), py(fn(s)), 0] for s in np.linspace(0, pp, max(3, int(90 * pp) + 2))]
        m.set_points_as_corners(pts)
    c.add_updater(upd)
    upd(c)
    return c


def axes():
    ya = Line([X0 - 0.2, PY0, 0], [X0 - 0.2, PY1 + 0.15, 0], color=GREY, stroke_width=4)
    xa = Line([X0 - 0.2, PY0, 0], [X1 + 0.1, PY0, 0], color=GREY, stroke_width=4)
    yl = T("PO2", 26, TEXT).move_to([X0 - 0.95, PY1 + 0.05, 0])
    xl = T("distance along the plate", 24, TEXT).move_to([0, PY0 - 0.36, 0])
    return VGroup(ya, xa, yl, xl)


def lab(text, x, y, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def wave_line(x0, x1, y, clk, amp=0.07, color=BLUE):
    c = VMobject(stroke_color=color, stroke_width=5)

    def upd(m):
        t = clk.get_value()
        m.set_points_as_corners([[x, y + amp * math.sin(2.2 * x + 2.0 * t), 0] for x in np.linspace(x0, x1, 60)])
    c.add_updater(upd)
    upd(c)
    return c


def fish(cx, cy, w=3.4):
    s = w / 3.4
    body = Ellipse(width=3.4 * s, height=1.8 * s, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.25).move_to([cx, cy, 0])
    tail = Polygon([cx + 1.55 * s, cy, 0], [cx + 2.35 * s, cy + 0.85 * s, 0], [cx + 2.35 * s, cy - 0.85 * s, 0], stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.25)
    eye = Dot([cx - 1.15 * s, cy + 0.3 * s, 0], radius=0.09, color=TEXT)
    gill = Arc(radius=0.78 * s, start_angle=PI / 2, angle=PI, color=TEXT, stroke_width=5).move_to([cx - 0.5 * s, cy - 0.05, 0])
    return VGroup(tail, body, eye, gill)


def chest(cx, cy, k=1.0):
    return _chest(0, 0).scale(k).move_to([cx, cy + 0.3 * k, 0])


def _chest(cx, cy):
    torso = RoundedRectangle(corner_radius=0.5, width=2.7, height=2.9, stroke_color=TEXT, stroke_width=4, fill_color=GREY, fill_opacity=0.2).move_to([cx, cy, 0])
    lungs = VGroup(*[Ellipse(width=1.0, height=1.9, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.22).move_to([cx + dx, cy - 0.15, 0]) for dx in (-0.62, 0.62)])
    tr = Line([cx, cy + 1.45, 0], [cx, cy + 2.1, 0], color=TEXT, stroke_width=8)
    return VGroup(torso, lungs, tr)


# =================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Gas Exchange and Breathing"
    TITLE = "The Last Gas the Blood Touches"


class S01Question(SpokenScene):
    def construct(self):
        ck = clock(self)
        F = fish(-4.1, 1.5, w=4.2)
        C = chest(5.0, 1.2, 1.15)
        w_in = march([-6.85, 1.5, 0], [-6.3, 1.5, 0], BLUE, n=3, speed=0.5)
        w_out = march([-4.7, 0.35, 0], [-4.7, -0.3, 0], BLUE, n=3, speed=0.5)
        a_in = march([4.8, 3.75, 0], [4.8, 2.95, 0], BLUE, n=4, speed=0.8)
        a_out = march([5.2, 2.95, 0], [5.2, 3.75, 0], BLUE, n=4, speed=0.8)
        self.play(FadeIn(F), FadeIn(C), run_time=1.0)
        self.add(w_in, w_out, a_in, a_out)
        self.at("far less")
        air = vbar(-5.5, -3.2, 2.2, w=1.1)
        wat = vbar(-4.0, -3.2, 2.2 / 30, w=1.1)
        bl = VGroup(lab("air", -5.5, -3.52, 24), lab("water", -4.0, -3.52, 24), lab("oxygen per litre", -4.75, -0.75, 24))
        self.play(GrowFromEdge(air, DOWN), GrowFromEdge(wat, DOWN), FadeIn(bl), run_time=1.3)
        note = VGroup(lab("air-saturated fresh water, 15-20 C:", 0.8, -2.0, 28), lab("about 30 times less oxygen per litre", 0.8, -2.65, 28, GOLD))
        self.at("yet")
        self.play(FadeIn(note), run_time=1.0)
        gb_t = ValueTracker(0)
        gb = gauge(-0.6, 0.6, 2.0, RED, lambda: 0.75 * gb_t.get_value())
        gw = gauge(0.55, 0.6, 2.0, BLUE, lambda: 0.35 * gb_t.get_value())
        gl = VGroup(lab("blood", -0.6, 0.28, 22, RED), lab("water", 0.55, 0.28, 22, BLUE), lab("PO2 leaving", 0.0, 2.9, 24))
        self.at("send its blood out")
        self.play(FadeIn(gb), FadeIn(gw), FadeIn(gl), run_time=0.6)
        self.play(gb_t.animate.set_value(1), run_time=2.6)
        self.at("than the water leaving")
        self.play(Indicate(gw, color=BLUE, scale_factor=1.1), run_time=1.2)
        self.at("your lung")
        gb2_t = ValueTracker(0)
        g2b = gauge(1.85, 0.6, 2.0, RED, lambda: 0.62 * gb2_t.get_value())
        g2a = gauge(2.95, 0.6, 2.0, BLUE, lambda: 0.72 * gb2_t.get_value())
        gl2 = VGroup(lab("blood", 1.85, 0.28, 22, RED), lab("air", 2.95, 0.28, 22, BLUE))
        sch = lab("gauges: schematic", 5.0, -3.6, 22, GREY)
        self.play(FadeOut(note), FadeIn(g2b), FadeIn(g2a), FadeIn(gl2), FadeIn(sch), run_time=0.6)
        self.play(gb2_t.animate.set_value(1), run_time=2.0)
        self.at("why not")
        q = chip("Why can a gill do what a lung cannot?", GOLD, size=36)
        q.move_to([1.3, -2.4, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.8)
        self.finish()


class S02Partial(SpokenScene):
    def construct(self):
        ck = clock(self)
        BX, BY = -5.2, -0.1
        grey_s = Rectangle(width=1.5, height=4.108, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.4).move_to([BX, BY - 2.6 + 2.054, 0])
        gold_s = Rectangle(width=1.5, height=1.092, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.45).move_to([BX, BY + 2.6 - 0.546, 0])
        gd = drift_dots(lambda: grey_s.get_center(), [[p[0] * 0.5 / 1.0, p[1] * 1.9 / 1.0, 0] for p in disc_pts(1.0, 16, 1)], ck, color=TEXT, op=0.7)
        od = drift_dots(lambda: gold_s.get_center(), [[-0.4, 0.2, 0], [0.3, -0.25, 0], [0.0, 0.0, 0], [0.45, 0.25, 0]], ck, color=GOLD, amp=0.1)
        bar = VGroup(grey_s, gold_s, gd, od)
        tot = VGroup(lab("total pressure", -2.3, 0.4, 28), lab("dry air, sea level:", -2.3, -0.2, 28), lab("about 760 mmHg", -2.3, -0.8, 28, GOLD))
        tot_a = T("total pressure", 28)
        self.play(Create(grey_s), Create(gold_s), run_time=1.0)
        self.add(gd, od)
        self.play(FadeIn(tot[0]), run_time=0.8)
        self.at("its share")
        share = lab("partial pressure = one gas's share of the total", 0.0, -3.4, 28)
        self.play(Write(share), run_time=2.2)
        self.at("dry air")
        self.play(FadeIn(tot[1]), FadeIn(tot[2]), run_time=1.0)
        self.at("one fifth")
        l21 = lab("21% oxygen", 2.3, 2.0, 30, GOLD)
        self.play(gold_s.animate.shift(RIGHT * 4.6), FadeIn(l21), run_time=1.3)
        self.at("oxygen")
        p160 = lab("PO2 about 160 mmHg", 2.6, 1.3, 30, GOLD)
        self.play(FadeIn(p160), run_time=1.0)
        self.at("but partial pressure")
        s2 = lab("partial pressure is not amount", 0.0, -3.4, 30, GOLD)
        self.play(Transform(share, s2), run_time=1.2)
        self.at("water left")
        gone = VGroup(grey_s, gold_s, gd, od, tot, l21, p160)
        self.play(FadeOut(gone), run_time=0.9)
        air_r = Rectangle(width=5.6, height=2.3, stroke_width=3, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.08).move_to([-3.6, 0.65, 0])
        wat_r = Rectangle(width=5.6, height=2.3, stroke_width=3, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.35).move_to([-3.6, -1.65, 0])
        surf = wave_line(-6.4, -0.8, -0.5, ck)
        lbls = VGroup(lab("air", -3.6, 1.2, 30, BLUE), lab("water", -3.6, -2.0, 30, BLUE))
        self.play(FadeIn(air_r), FadeIn(wat_r), FadeIn(lbls), run_time=1.2)
        self.add(surf)
        g_t = ValueTracker(0)
        ga = gauge(1.0, -2.3, 3.3, GOLD, lambda: 0.6 * g_t.get_value())
        gw = gauge(2.1, -2.3, 3.3, GOLD, lambda: 0.6 * g_t.get_value())
        gl = VGroup(lab("air", 1.0, -2.65, 24), lab("water", 2.1, -2.65, 24), lab("PO2", 1.55, 1.3, 28))
        self.at("same oxygen")
        self.play(FadeIn(ga), FadeIn(gw), FadeIn(gl), run_time=0.6)
        self.play(g_t.animate.set_value(1), run_time=1.8)
        sm = lab("same PO2", 1.55, 1.85, 30, GOLD)
        self.play(FadeIn(sm), run_time=0.6)
        self.at("yet each")
        ba = vbar(4.5, -2.3, 3.0, w=0.9)
        bw = vbar(5.8, -2.3, 0.1, w=0.9)
        bl = VGroup(lab("air", 4.5, -2.65, 24), lab("water", 5.8, -2.65, 24), lab("oxygen per litre", 5.15, 1.3, 24))
        self.play(GrowFromEdge(ba, DOWN), GrowFromEdge(bw, DOWN), FadeIn(bl), run_time=1.6)
        self.finish()


class S03Diffusion(SpokenScene):
    def construct(self):
        geo = (0.3, 3.0, -0.3, 0.3, -3.0, -0.3)
        L = lam(lambda s: 90, lambda s: 12, geo=geo)
        self.play(FadeIn(L), run_time=1.2)
        tag_w = lab("water", -5.9, 1.9, 28, BLUE)
        tag_b = lab("blood", -5.9, -1.9, 28, RED)
        self.play(FadeIn(tag_w), FadeIn(tag_b), run_time=0.8)
        self.at("only by")
        pump = chip("pump", TEXT, size=30)
        pump.move_to([-4.2, 0, 0])
        cross = VGroup(Line([-4.9, 0.5, 0], [-3.5, -0.5, 0], color=RED, stroke_width=5), Line([-4.9, -0.5, 0], [-3.5, 0.5, 0], color=RED, stroke_width=5))
        self.play(FadeIn(pump), Create(cross), run_time=1.0)
        self.at("molecules cross both")
        xs_dn = [-2.6, -1.3, 0.0, 1.3, 2.6, 3.9]
        dn = VGroup(*[Arrow([x, 1.0, 0], [x, -1.0, 0], buff=0, color=GOLD, stroke_width=9, tip_length=0.3) for x in xs_dn])
        up = VGroup(*[Arrow([x, -1.0, 0], [x, 1.0, 0], buff=0, color=GOLD, stroke_width=3, tip_length=0.15).set_opacity(0.5) for x in (-1.95, 3.25)])
        mv = VGroup(*[march([x, 1.0, 0], [x, -1.0, 0], GOLD, n=2, speed=1.0, r=0.07) for x in xs_dn], *[march([x, -1.0, 0], [x, 1.0, 0], GOLD, n=1, speed=1.0, r=0.07, op=0.6) for x in (-1.95, 3.25)])
        self.play(FadeIn(up), run_time=1.0)
        self.add(mv)
        self.at("but the net")
        self.play(FadeIn(dn), run_time=1.0)
        net = Arrow([6.2, 1.4, 0], [6.2, -1.4, 0], buff=0, color=GOLD, stroke_width=14, tip_length=0.4)
        nl = lab("net", 6.2, 1.8, 28, GOLD)
        self.play(GrowArrow(net), FadeIn(nl), run_time=1.0)
        self.at("higher partial")
        top = lab("net diffusion: high PO2 to low PO2", 0, 3.5, 30, GOLD)
        self.play(Write(top), run_time=1.6)
        self.at("so here")
        hi = lab("high PO2", -5.85, 1.3, 26, BLUE)
        lo = lab("low PO2", -5.85, -1.3, 26, RED)
        self.play(FadeIn(hi), FadeIn(lo), run_time=0.8)
        self.at("not more")
        bt = lab("richer = higher PO2, not more oxygen", 0, -3.55, 28, GOLD)
        self.play(FadeIn(bt), run_time=1.0)
        self.finish()


class S04Fick(SpokenScene):
    def construct(self):
        ck = clock(self)
        a, d, t = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        Af = lambda: 0.45 + 0.55 * a.get_value()
        Pw = lambda: 55 + 40 * d.get_value()
        Tk = lambda: 0.7 - 0.45 * t.get_value()
        wb = band(X0, X1, 2.35, 3.55, BLUE)
        bb = band(X0, X1, 0.3, 1.65, RED)
        st = Rectangle(width=1, height=1, stroke_width=0, fill_color=GREY, fill_opacity=0.9)

        def sup(m):
            m.become(Rectangle(width=10 * Af(), height=Tk(), stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([0, 2.0, 0]))
        st.add_updater(sup)
        sup(st)
        wd = stream(X0, X1, 2.35, 3.55, lambda s: Pw(), seed=2)
        bd = stream(X0, X1, 0.3, 1.65, lambda s: 12, seed=5)
        xs = [-4.2, -2.8, -1.4, 0, 1.4, 2.8, 4.2]
        ar = VGroup(*[Arrow([x, 2.95, 0], [x, 1.05, 0], buff=0, color=GOLD, stroke_width=3, tip_length=0.22) for x in xs])

        def aup(m):
            rate = Af() * (Pw() - 12) / 100 / Tk()
            for x, arrow in zip(xs, m):
                on = abs(x) <= 5 * Af() - 0.1
                arrow.set_stroke(GOLD, width=2 + 7 * rate, opacity=1.0 if on else 0.0)
                arrow.tip.set_fill(GOLD, opacity=1.0 if on else 0.0)
        ar.add_updater(aup)
        aup(ar)
        self.play(FadeIn(wb), FadeIn(bb), FadeIn(st), run_time=1.0)
        self.add(wd, bd, ar)
        self.wait(0.6)
        self.at("three dials")
        dA = dial(-0.9, "A, area", a, x0=-2.2, x1=1.6)
        dP = dial(-1.8, "ΔP, PO2 difference", d, x0=-2.2, x1=1.6)
        dT = dial(-2.7, "T, thickness", t, x0=-2.2, x1=1.6)
        self.play(FadeIn(dA), run_time=0.6)
        self.play(FadeIn(dP), run_time=0.6)
        self.play(FadeIn(dT), run_time=0.6)
        self.at("more area")
        self.play(a.animate.set_value(1), run_time=1.6)
        self.at("a steeper")
        self.play(d.animate.set_value(1), run_time=1.6)
        self.at("thinner")
        self.play(t.animate.set_value(1), run_time=1.4)
        self.at("all speed")
        eq = M("rate = k x A x ΔP / T", 30, GOLD).move_to([0, -3.5, 0])
        self.play(Write(eq), run_time=1.4)
        self.wait(0.5)
        self.at("that is why")
        # cut-outs: a feathery gill filament and a cluster of alveoli
        self.play(FadeOut(VGroup(wb, bb, st, wd, bd, ar, dA, dP, dT, eq)), run_time=0.8)
        stem = Line([-3.6, -2.2, 0], [-3.6, 2.4, 0], color=TEXT, stroke_width=6)
        lamel = VGroup()
        for i in range(12):
            y = -1.9 + i * 0.38
            for sgn in (-1, 1):
                ln = Line([-3.6, y, 0], [-3.6 + sgn * 1.2, y + 0.55, 0], color=RED, stroke_width=5)
                ln.base = (y, sgn, i)
                lamel.add(ln)

        def sway(m):
            tt = ck.get_value()
            for ln in m:
                y, sgn, i = ln.base
                ln.put_start_and_end_on([-3.6, y, 0], [-3.6 + sgn * (1.2 + 0.12 * math.sin(1.6 * tt + i * 0.5)), y + 0.55 + 0.08 * math.sin(1.3 * tt + i), 0])
        lamel.add_updater(sway)
        sway(lamel)
        gill = VGroup(stem, lamel)
        alv = VGroup()
        cents = [[3.0, 1.5], [4.4, 1.5], [3.7, 0.3], [2.4, 0.2], [5.0, 0.2], [3.0, -1.0], [4.4, -1.0]]
        for c in cents:
            alv.add(Circle(radius=0.62, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.15).move_to([c[0], c[1], 0]))
        alv.add(Line([3.7, 2.1, 0], [3.7, 2.9, 0], color=TEXT, stroke_width=7))

        def pulse(m):
            m.set_stroke(BLUE, width=5 + 1.5 * math.sin(2.0 * ck.get_value()))
        alv.add_updater(lambda m: [c.set_stroke(BLUE, width=5 + 1.5 * math.sin(2.0 * ck.get_value() + i)) for i, c in enumerate(m[:-1])])
        self.play(FadeIn(gill), FadeIn(alv), run_time=1.2)
        names = VGroup(lab("gill filaments", -3.6, 3.5, 28), lab("alveoli", 3.7, 3.5, 28))
        self.play(FadeIn(names), run_time=0.6)
        lt = lab("large, thin", 0.0, -1.9, 34, GOLD)
        self.play(FadeIn(lt), run_time=0.8)
        self.at("moist")
        film_g = Ellipse(width=3.2, height=5.5, stroke_color=BLUE, stroke_width=3, fill_opacity=0).move_to([-3.6, 0.1, 0])
        film_a = VGroup(*[Circle(radius=0.72, stroke_color=BLUE, stroke_width=3).move_to([c[0], c[1], 0]) for c in cents])
        self.play(Create(film_g), Create(film_a), run_time=1.5)
        mt = VGroup(lab("moist: gases dissolve", 0.0, -3.0, 30, BLUE), lab("before crossing cells", 0.0, -3.5, 30, BLUE))
        self.play(FadeIn(mt), run_time=1.0)
        self.finish()


class S05Ceiling(SpokenScene):
    def construct(self):
        geo = (1.0, 3.3, 0.65, 1.0, -2.0, 0.65)
        pw, pb = same_model(1.2)
        L = lam(pw, pb, geo=geo)
        self.play(FadeIn(L), run_time=1.0)
        sc = lab("schematic", -5.7, -3.65, 22, GREY)
        self.add(sc)
        self.at("all along")
        xs = [-3.8, -1.9, 0.0, 1.9, 3.8]
        dif = VGroup(*[march([x, 2.4, 0], [x, -0.8, 0], GOLD, n=2, speed=0.9) for x in xs])
        self.add(dif)
        tg = VGroup(*[Arrow([x, 2.2, 0], [x, -0.6, 0], buff=0, color=GOLD, stroke_width=3, tip_length=0.18) for x in xs])
        self.play(FadeIn(tg), run_time=0.8)
        self.at("the water or air stays")
        t1 = lab("medium richer than blood all along", 0, 3.55, 30, BLUE)
        self.play(Write(t1), run_time=1.8)
        self.at("diffusion brings")
        t_ = ValueTracker(0)
        gw = gauge(5.55, -2.0, 5.3, BLUE, lambda: pw(1.0) / 100, w=0.44)
        gb = gauge(6.4, -2.0, 5.3, RED, lambda: pb(1.0) / 100 * t_.get_value(), w=0.44)
        self.play(FadeIn(gw), FadeIn(gb), run_time=0.4)
        self.play(t_.animate.set_value(1), run_time=1.5)
        self.at("never past")
        top_y = -2.0 + 5.3 * pw(1.0) / 100
        dash = DashedLine([5.0, top_y, 0], [6.85, top_y, 0], color=GOLD, stroke_width=5)
        gl = VGroup(lab("water", 5.55, -2.3, 22, BLUE), lab("blood", 6.4, -2.65, 22, RED))
        self.play(Create(dash), FadeIn(gl), run_time=1.0)
        self.at("so the leaving")
        c1 = lab("ceiling = PO2 of the last water or air touched", -0.8, -2.65, 30, GOLD)
        c2 = lab("(while the medium stays richer)", -0.8, -3.2, 26, TEXT)
        self.play(Write(c1), run_time=1.8)
        self.play(FadeIn(c2), run_time=0.8)
        hc = lab("how close: Fick and the flows", -0.8, -3.7, 26, TEAL)
        self.play(FadeIn(hc), run_time=0.8)
        self.finish()


class S06Same(SpokenScene):
    def construct(self):
        k = 2.2
        pw, pb = same_model(k)
        L = lam(pw, pb)
        ax = axes()
        self.play(FadeIn(L), FadeIn(ax), run_time=1.2)
        self.wait(0.6)
        self.at("a thin gill")
        t1 = lab("lamella", 0, 3.55, 30, TEXT)
        self.play(FadeIn(t1), run_time=0.8)
        self.at("the water starts")
        hw = lab("rich", -4.4, 3.0, 28, BLUE)
        self.play(FadeIn(hw), run_time=0.6)
        self.at("starts poor")
        hb = lab("poor", -4.4, 0.65, 28, RED)
        self.play(FadeIn(hb), run_time=0.6)
        self.at("partway along")
        self.play(FadeOut(t1), FadeOut(hw), FadeOut(hb), run_time=0.5)
        p = ValueTracker(0)
        cw = curve(pw, BLUE, p)
        cb = curve(pb, RED, p)
        scan = Line([0, PY0, 0], [0, 3.25, 0], color=GOLD, stroke_width=3)
        scan.add_updater(lambda m: m.put_start_and_end_on([px(p.get_value()), PY0, 0], [px(p.get_value()), 3.25, 0]))
        gw = gauge(5.8, 0.35, 2.9, BLUE, lambda: pw(p.get_value()) / 100, w=0.42)
        gb = gauge(6.4, 0.35, 2.9, RED, lambda: pb(p.get_value()) / 100, w=0.42)
        self.add(cw, cb, scan, gw, gb)
        lw = lab("water", px(0.42), py(pw(0.42)) + 0.4, 26, BLUE)
        lb = lab("blood", px(0.42), py(pb(0.42)) - 0.4, 26, RED)
        self.play(FadeIn(lw), FadeIn(lb), run_time=0.5)
        self.at("close in")
        self.play(p.animate.set_value(1.0), run_time=3.2, rate_func=linear)
        self.at("the rest")
        sh = Rectangle(width=px(1) - px(0.55), height=py(100) - PY0, stroke_width=0, fill_color=GREY, fill_opacity=0.25).move_to([(px(0.55) + px(1)) / 2, (PY0 + py(100)) / 2, 0])
        al = lab("adds little", px(0.775), py(86), 30, TEXT)
        self.play(FadeIn(sh), FadeIn(al), run_time=1.0)
        gl = VGroup(lab("out", 5.8, 0.0, 22, BLUE), lab("out", 6.4, 0.0, 22, RED))
        self.play(FadeIn(gl), run_time=0.6)
        self.finish()


def reversing_world(scene, qtext=None):
    pw, _ = same_model(2.2)
    pbr = lambda s: 8
    L = lam(pw, pbr)
    return L


class S07Predict(SpokenScene):
    def construct(self):
        pw, pb = same_model(2.2)
        bl = ValueTracker(1)
        pbf = lambda s: 14 + (pb(s) - 14) * bl.get_value()
        L = lam(pw, pbf)
        self.add(L)
        self.wait(0.4)
        self.at("reverse")
        self.play(L.bsp.animate.set_value(-1), bl.animate.set_value(0), *[Rotate(a, angle=PI) for a in L.ba], run_time=1.8)
        self.at("where will")
        q = chip("Blood against the water:\nwhere does the leaving blood end up?", GOLD, size=40)
        q = fit(q, max_w=12.0)
        q.move_to([0, -1.4, 0])
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.9)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        pw, pb = same_model(2.2)
        poor = lambda s: 14
        L = lam(pw, poor, bdir=-1)
        self.add(L)
        q = chip("Blood against the water:\nwhere does the leaving blood end up?", GOLD, size=40)
        q = fit(q, max_w=12.0)
        q.move_to([0, -1.4, 0])
        self.add(q)
        ring = Circle(radius=0.35, color=GREY, stroke_width=6).move_to([0, -3.2, 0])
        arc = Arc(radius=0.35, start_angle=PI / 2, angle=0.01, color=GOLD, stroke_width=8, arc_center=[0, -3.2, 0])
        tr = ValueTracker(0)
        arc.add_updater(lambda m: m.become(Arc(radius=0.35, start_angle=PI / 2, angle=-TAU * max(tr.get_value(), 0.01), color=GOLD, stroke_width=8, arc_center=[0, -3.2, 0])))
        self.add(ring, arc)
        self.play(tr.animate.set_value(1), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S09Counter(SpokenScene):
    def construct(self):
        k = 4.0
        pw, pb = counter_model(k)
        L = lam(pw, pb, bdir=-1)
        ax = axes()
        self.play(FadeIn(L), FadeIn(ax), run_time=0.8)
        self.at("the blood about")
        box = RoundedRectangle(corner_radius=0.15, width=2.6, height=3.2, stroke_color=GOLD, stroke_width=5).move_to([-3.7, 1.8, 0])
        t1 = lab("blood about to leave meets water just arrived", 0.6, 3.6, 28, GOLD)
        t1 = fit(t1, max_w=11.5)
        self.play(Create(box), FadeIn(t1), run_time=1.2)
        self.at("all along")
        self.play(FadeOut(box), FadeOut(t1), run_time=0.4)
        xs = [-4.0, -2.4, -0.8, 0.8, 2.4, 4.0]
        dif = VGroup(*[march([x, 2.6, 0], [x, 1.1, 0], GOLD, n=2, speed=0.8, r=0.07) for x in xs])
        self.add(dif)
        p = ValueTracker(0)
        cw = curve(pw, BLUE, p)
        cb = curve(pb, RED, p)
        scan = Line([0, PY0, 0], [0, 3.25, 0], color=GOLD, stroke_width=3)
        scan.add_updater(lambda m: m.put_start_and_end_on([px(p.get_value()), PY0, 0], [px(p.get_value()), 3.25, 0]))
        gb = gauge(-5.9, 0.35, 2.9, RED, lambda: pb(0.0) / 100 * min(1.0, p.get_value() * 3))
        gw = gauge(5.9, 0.35, 2.9, BLUE, lambda: pw(1.0) / 100 * min(1.0, p.get_value() * 3))
        lw = lab("water", px(0.12), py(pw(0.12)) + 0.34, 26, BLUE)
        lb = lab("blood", px(0.12), py(pb(0.12)) - 0.34, 26, RED)
        self.add(cw, cb, scan)
        self.play(FadeIn(gb), FadeIn(gw), FadeIn(lw), FadeIn(lb), p.animate.set_value(1.0), run_time=1.6, rate_func=linear)
        self.at("the water stays a little")
        gap = DoubleArrow([px(0.5), py(pw(0.5)), 0], [px(0.5), py(pb(0.5)), 0], buff=0, color=GOLD, stroke_width=6, tip_length=0.2)
        gl = lab("gap", px(0.5) - 0.45, (py(pw(0.5)) + py(pb(0.5))) / 2 + 0.02, 26, GOLD)
        self.play(GrowFromCenter(gap), FadeIn(gl), run_time=1.0)
        self.at("this is countercurrent")
        cc = lab("countercurrent", 0, 3.55, 34, GOLD)
        self.play(FadeIn(cc), run_time=0.8)
        self.finish()


class S10Conditions(SpokenScene):
    def construct(self):
        a, t = ValueTracker(0), ValueTracker(0)
        kf = lambda: 2.0 * (0.25 + 0.75 * a.get_value()) / (1.0 - 0.5 * t.get_value())
        pw, pb = counter_model(kf)
        L = lam(pw, pb, bdir=-1)
        gb = gauge(-5.9, 0.35, 2.9, RED, lambda: pb(0.0) / 100)
        gw = gauge(5.9, 0.35, 2.9, BLUE, lambda: pw(1.0) / 100)
        self.add(L)
        dA = dial(-1.2, "A, area", a, x0=-3.6, x1=-0.4)
        dT = dial(-2.4, "T, thickness", t, x0=-3.6, x1=-0.4)
        self.play(FadeIn(gb), FadeIn(gw), FadeIn(dA), FadeIn(dT), run_time=0.4)
        self.play(a.animate.set_value(1), t.animate.set_value(1), run_time=2.0)
        self.at("the leaving blood")
        top = lab("countercurrent: blood can beat the water leaving", 0, 3.55, 28, GOLD)
        top = fit(top, max_w=11.5)
        self.play(FadeIn(top), run_time=0.8)
        self.at("running the same")
        # inset: same direction
        kk = lambda: 2.0 * (0.25 + 0.75 * a.get_value()) / (1.0 - 0.5 * t.get_value())
        sw = lambda s: 50 + 50 * math.exp(-2 * kk() * s)
        sb = lambda s: 50 - 50 * math.exp(-2 * kk() * s)
        g2 = (-1.0, -0.2, -1.3, -1.0, -2.1, -1.3)
        I = lam(sw, sb, geo=g2, x0=0.9, x1=4.9, n=26, seed=9)
        ig_w = gauge(5.55, -2.1, 1.9, BLUE, lambda: sw(1.0) / 100, w=0.36)
        ig_b = gauge(6.15, -2.1, 1.9, RED, lambda: sb(1.0) / 100, w=0.36)
        self.play(FadeIn(I), FadeIn(ig_w), FadeIn(ig_b), run_time=1.0)
        self.at("never")
        nv = lab("same direction: never", 3.1, -2.75, 28, TEXT)
        self.play(FadeIn(nv), run_time=0.6)
        self.finish()


def sac(cx, cy, R=2.2):
    gap = math.asin(0.4 / R)
    ring = Arc(radius=R, start_angle=PI / 2 + gap, angle=TAU - 2 * gap, arc_center=[cx, cy, 0], color=GREY, stroke_width=14)
    tube = VGroup(Line([cx - 0.4, cy + R * math.cos(gap), 0], [cx - 0.4, cy + R + 1.4, 0], color=GREY, stroke_width=14),
                  Line([cx + 0.4, cy + R * math.cos(gap), 0], [cx + 0.4, cy + R + 1.4, 0], color=GREY, stroke_width=14))
    pool = Circle(radius=R - 0.17, stroke_width=0, fill_color=BLUE, fill_opacity=0.13).move_to([cx, cy, 0])
    return ring, tube, pool


def fresh_swirl(ck, cx, cy, R, n=10, period=5.0, seed=4):
    rng = random.Random(seed)
    g = VGroup(*[Dot(radius=0.075, color=BLUE) for _ in range(n)])
    top = np.array([cx, cy + R + 1.2, 0.0])
    for d in g:
        r = R * 0.8 * math.sqrt(rng.random())
        a = rng.random() * TAU
        d.anchor = np.array([cx + r * math.cos(a), cy + r * math.sin(a), 0.0])
        d.off = rng.random() * 0.25
        d.w = 0.9 + rng.random()
        d.ph = rng.random() * TAU

    def upd(m):
        for d in m:
            ph = ((ck.get_value() / period) + d.off) % 1.0
            if ph < 0.3:
                u = ph / 0.3
                u = u * u * (3 - 2 * u)
                pos = top + (d.anchor - top) * u
                op = min(1.0, ph / 0.05)
            else:
                u = (ph - 0.3) / 0.7
                pos = d.anchor + 0.25 * np.array([math.sin(d.w * ck.get_value() + d.ph), math.cos(d.w * ck.get_value() + d.ph), 0])
                op = max(0.0, 1.0 - 0.75 * u) * min(1.0, (1 - ph) / 0.06)
            d.move_to(pos)
            d.set_opacity(op)
    g.add_updater(upd)
    upd(g)
    return g


class S11Lung(SpokenScene):
    def construct(self):
        ck = clock(self)
        cx, cy, R = 0.0, -0.6, 2.2
        strip = Line([-4.5, cy, 0], [4.5, cy, 0], color=GREY, stroke_width=14)
        ring, tube, pool = sac(cx, cy, R)
        self.play(Create(strip), run_time=0.8)
        self.at("fold")
        self.play(Transform(strip, ring), run_time=2.0)
        self.add(ring)
        self.remove(strip)
        stale = drift_dots(lambda: [cx, cy, 0], disc_pts(R - 0.45, 26, 5), ck, color=BLUE, r=0.07, op=0.35, amp=0.2)
        self.play(FadeIn(pool), Create(tube), run_time=1.0)
        self.add(stale)
        self.at("alveolus")
        al = lab("alveolus", 3.9, cy, 34, TEXT)
        self.play(FadeIn(al), run_time=0.8)
        self.at("air goes")
        a_in = march([cx - 0.2, cy + R + 1.3, 0], [cx - 0.2, cy + R - 0.3, 0], BLUE, n=4, speed=0.9, r=0.08)
        a_out = march([cx + 0.2, cy + R - 0.3, 0], [cx + 0.2, cy + R + 1.3, 0], BLUE, n=4, speed=0.9, r=0.08, op=0.5)
        self.add(a_in, a_out)
        self.play(FadeIn(VGroup(lab("in", -1.1, 3.1, 26, BLUE), lab("out", 1.15, 3.1, 26, BLUE))), run_time=0.8)
        self.at("each breath")
        fresh = fresh_swirl(ck, cx, cy, R - 0.2)
        self.add(fresh)
        pt = lab("only part of the gas is replaced", -3.7, cy, 28, BLUE)
        pt = pt.scale(1.0)
        pt = VGroup(lab("only part of", -4.1, cy + 0.3, 28, BLUE), lab("the gas is replaced", -4.1, cy - 0.25, 28, BLUE))
        self.play(FadeIn(pt), run_time=1.0)
        self.finish()


class S12Pool(SpokenScene):
    def construct(self):
        ck = clock(self)
        cx, cy, R = 0.0, -0.6, 2.2
        ring, tube, pool = sac(cx, cy, R)
        stale = drift_dots(lambda: [cx, cy, 0], disc_pts(R - 0.45, 26, 5), ck, color=BLUE, r=0.07, op=0.35, amp=0.2)
        fresh = fresh_swirl(ck, cx, cy, R - 0.2)
        self.add(ring, tube, pool, stale, fresh)
        self.wait(0.3)
        # capillaries wrap the sac
        caps = VGroup()
        Rc = R + 0.38
        gap = math.asin(0.55 / Rc)
        spans = [(PI / 2 + gap + 0.05, 0.95), (PI / 2 + gap + 1.12, 0.95), (PI / 2 + gap + 2.19, 0.95), (PI / 2 + gap + 3.26, 0.95), (PI / 2 + gap + 4.33, 0.55 + 0.0)]
        spans = [(PI / 2 + gap + 0.05 + i * 1.0, 0.9) for i in range(5)]
        for a0, da in spans:
            caps.add(Arc(radius=Rc, start_angle=a0, angle=da, arc_center=[cx, cy, 0], color=RED, stroke_width=12))
        rd = VGroup()
        for c in caps:
            g = VGroup(*[Dot(radius=0.07, color=RED) for _ in range(4)])
            for i, d in enumerate(g):
                d.s = i / 4

            def upd(m, dt, c=c):
                for d in m:
                    d.s = (d.s + dt * 0.18) % 1
                    d.move_to(c.point_from_proportion(d.s))
            g.add_updater(upd)
            upd(g, 0)
            rd.add(g)
        cross = VGroup()
        for a0, da in spans:
            am = a0 + da / 2
            u = np.array([math.cos(am), math.sin(am), 0])
            cross.add(march([cx, cy, 0] + u * (R - 0.45), [cx, cy, 0] + u * (Rc + 0.05), GOLD, n=2, speed=0.6, r=0.07))
        self.play(FadeIn(caps), run_time=1.0)
        self.add(rd, cross)
        self.wait(0.5)
        self.at("so the sac")
        ti = ValueTracker(0)
        g1 = gauge(3.5, -3.0, 3.1, BLUE, lambda: 1.0 * ti.get_value())
        g2 = gauge(4.8, -3.0, 3.1, BLUE, lambda: 0.667 * ti.get_value())
        tb_ = ValueTracker(0)
        g3 = gauge(6.1, -3.0, 3.1, RED, lambda: 0.667 * tb_.get_value())
        gls = VGroup(lab("inhaled", 3.5, -3.32, 22, BLUE), lab("alveolar", 4.8, -3.32, 22, BLUE), lab("blood", 6.1, -3.32, 22, RED))
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(gls), run_time=0.7)
        self.play(ti.animate.set_value(1), run_time=2.0)
        l1 = VGroup(lab("warmed, humidified", -4.6, 2.5, 26, BLUE), lab("inhaled air:", -4.6, 2.0, 26, BLUE), lab("about 150 mmHg", -4.6, 1.5, 28, BLUE))
        l2 = VGroup(lab("alveolar gas:", -4.6, 0.3, 26, BLUE), lab("about 100 mmHg", -4.6, -0.2, 28, BLUE), lab("(resting adult human)", -4.6, -0.7, 24, TEXT))
        self.play(FadeIn(l1), run_time=0.6)
        self.play(FadeIn(l2), run_time=0.6)
        self.at("every capillary")
        vp = lab("ventilated pool", 0, -3.65, 32, GOLD)
        hl = Circle(radius=R - 0.1, color=GOLD, stroke_width=4).move_to([cx, cy, 0])
        self.play(Create(hl), FadeIn(vp), run_time=1.2)
        self.play(FadeOut(hl), run_time=0.5)
        self.at("blood can")
        top_y = -3.0 + 3.1 * 0.667
        dash = DashedLine([3.2, top_y, 0], [6.6, top_y, 0], color=GOLD, stroke_width=5)
        self.play(FadeIn(g3), run_time=0.4)
        self.play(tb_.animate.set_value(1), Create(dash), run_time=1.3)
        self.finish()


class S13Answer(SpokenScene):
    def construct(self):
        ck = clock(self)
        geo = (0.9, 2.2, 0.6, 0.9, -0.7, 0.6)
        pw, pb = counter_model(4.0)
        L = lam(pw, pb, geo=geo, x0=-6.4, x1=-0.9, bdir=-1, n=36, seed=21)
        cx, cy, R = 3.7, -0.15, 1.75
        ring, tube, pool = sac(cx, cy, R)
        ring.set_stroke(width=10)
        tube.set_stroke(width=10)
        stale = drift_dots(lambda: [cx, cy, 0], disc_pts(R - 0.4, 18, 8), ck, color=BLUE, r=0.06, op=0.35, amp=0.15)
        Rc = R + 0.3
        caps = VGroup(*[Arc(radius=Rc, start_angle=PI / 2 + 0.3 + i * 1.0, angle=0.85, arc_center=[cx, cy, 0], color=RED, stroke_width=9) for i in range(5)])
        h1 = lab("trout gill", -3.65, 3.2, 30, TEXT)
        h2 = lab("your lung", 3.7, 3.2, 30, TEXT)
        self.play(FadeIn(L), FadeIn(ring), FadeIn(tube), FadeIn(pool), FadeIn(caps), run_time=1.2)
        self.add(stale)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.5)
        self.at("in its gill")
        box = RoundedRectangle(corner_radius=0.15, width=2.5, height=3.3, stroke_color=GOLD, stroke_width=5).move_to([-5.15, 0.8, 0])
        lt1 = VGroup(lab("last touched:", -3.65, -2.55, 28, GOLD), lab("fresh, incoming water", -3.65, -3.1, 28, BLUE))
        self.play(Create(box), FadeIn(lt1), run_time=1.4)
        self.at("in your lung")
        hl = Circle(radius=R + 0.05, color=GOLD, stroke_width=5).move_to([cx, cy, 0])
        lt2 = VGroup(lab("last touched:", 3.7, -2.55, 28, GOLD), lab("stale, mixed gas", 3.7, -3.1, 28, BLUE))
        self.play(Create(hl), FadeIn(lt2), run_time=1.4)
        self.finish()


class S14Recap(SpokenScene):
    def construct(self):
        ck = clock(self)
        pw, pb = same_model(1.2)
        geo = (1.2, 3.2, 0.85, 1.2, -1.15, 0.85)
        L = lam(pw, pb, geo=geo, x0=-6.4, x1=-0.2, n=40, seed=31)
        gw = gauge(0.5, -1.15, 4.35, BLUE, lambda: pw(1.0) / 100, w=0.4)
        gb = gauge(1.1, -1.15, 4.35, RED, lambda: pb(1.0) / 100, w=0.4)
        ceil_y = -1.15 + 4.35 * pw(1.0) / 100
        dash = DashedLine([0.2, ceil_y, 0], [1.5, ceil_y, 0], color=GOLD, stroke_width=5)
        sch = lab("schematic", -3.3, -1.6, 24, GREY)
        cards = [("Fick and the flows:", "how close (A, ΔP, T)"), ("arrangement:", "what blood last touches"), ("breathing:", "keeps it fresh")]
        cs = VGroup()
        for i, (l1, l2) in enumerate(cards):
            t1 = T(l1, 30, GOLD, weight=BOLD)
            t2 = T(l2, 30, TEXT)
            tx = VGroup(t1, t2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            bx = RoundedRectangle(corner_radius=0.16, width=5.1, height=tx.height + 0.6, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.12)
            tx.move_to(bx)
            c = VGroup(bx, tx)
            c.move_to([4.25, 2.5 - i * 2.4, 0])
            cs.add(c)
        self.play(FadeIn(L), FadeIn(gw), FadeIn(gb), FadeIn(dash), FadeIn(sch), run_time=0.6)
        self.at("fix law")
        self.play(FadeIn(cs[0], shift=LEFT * 0.3), run_time=0.8)
        self.play(Indicate(dash, color=GOLD), run_time=1.0)
        self.at("the flow")
        self.play(cs[0].animate.set_opacity(0.5), FadeIn(cs[1], shift=LEFT * 0.3), run_time=0.8)
        self.play(Rotate(L.ba, angle=PI), L.bsp.animate.set_value(-1), run_time=1.4)
        self.at("breathing")
        self.play(cs[1].animate.set_opacity(0.5), FadeIn(cs[2], shift=LEFT * 0.3), run_time=0.8)
        self.play(Indicate(L.wd, color=BLUE), run_time=1.2)
        self.finish()


class S15End(EndCard):
    LINE = "Blood gaining oxygen can at best reach the PO2 it last touched."
