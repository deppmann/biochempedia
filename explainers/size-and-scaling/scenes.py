"""Why a Mouse Needs Plumbing: size, surface and diffusion (Biochemistrypedia explainer, re-paced).

COLOUR MAP (whole film): surface/skin GOLD; oxygen BLUE; pumped fluid (blood, air) RED;
oxygen-starved core dark grey; animals = light outlines. Anything not computed is labelled schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

LOW = "#1E232D"      # tissue with no oxygen
CORE = "#4B505B"     # oxygen-starved core (dark grey)
PALE = "#CFD8E8"

EX = np.array([0.866, -0.5, 0.0])
EY = np.array([-0.866, -0.5, 0.0])
EZ = np.array([0.0, 1.0, 0.0])


def mix(c, k, base=None):
    return interpolate_color(ManimColor(base or BG), ManimColor(c), float(min(max(k, 0), 1)))


# ------------------------------------------------------------------ motion helpers
def brown(m, box, sigma=1.2, seed=0):
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = box

    def f(mob, dt):
        p = mob.get_center() + np.array([rng.normal(), rng.normal(), 0]) * sigma * np.sqrt(dt)
        if p[0] < x0: p[0] = 2 * x0 - p[0]
        if p[0] > x1: p[0] = 2 * x1 - p[0]
        if p[1] < y0: p[1] = 2 * y0 - p[1]
        if p[1] > y1: p[1] = 2 * y1 - p[1]
        p[0] = min(max(p[0], x0), x1); p[1] = min(max(p[1], y0), y1)
        mob.move_to(p)
    m.add_updater(f)
    return m


def sweep(m, p0, p1, period, off=0.0, fade=0.15):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    m._tt = off * period

    def f(mob, dt):
        mob._tt += dt
        fr = (mob._tt / period) % 1
        mob.move_to(p0 + (p1 - p0) * fr)
        mob.set_opacity(min(1, fr / fade, (1 - fr) / fade))
    m.add_updater(f)
    return m


def on_path(m, path, period, off=0.0):
    m._tt = off * period

    def f(mob, dt):
        mob._tt += dt
        mob.move_to(path.point_from_proportion((mob._tt / period) % 1))
    m.add_updater(f)
    return m


def glide(m, ax, ay, period, phase=0.0):
    m._g = phase

    def f(mob, dt):
        old = np.array([ax * np.sin(2 * np.pi * mob._g / period), ay * np.sin(4 * np.pi * mob._g / period), 0])
        mob._g += dt
        new = np.array([ax * np.sin(2 * np.pi * mob._g / period), ay * np.sin(4 * np.pi * mob._g / period), 0])
        mob.shift(new - old)
    m.add_updater(f)
    return m


def beat(m, period=0.9, amp=0.14):
    m._bt = 0.0
    m._bs = 1.0
    c = m.get_center()

    def f(mob, dt):
        mob._bt += dt
        s = 1 + amp * max(0, np.sin(2 * np.pi * mob._bt / period)) ** 2
        mob.scale(s / mob._bs, about_point=c)
        mob._bs = s
    m.add_updater(f)
    return m


def pulse(m, period=1.2, amp=0.18):
    return beat(m, period, amp)


def dots(n, color=BLUE, r=0.1):
    return VGroup(*[Dot(radius=r, color=color) for _ in range(n)])


# ------------------------------------------------------------------ cubes
def cell(origin, a, c=(0, 0, 0)):
    i, j, k = c
    P = lambda x, y, z: origin + a * (x * EX + y * EY + z * EZ)
    top = Polygon(P(i, j, k + 1), P(i + 1, j, k + 1), P(i + 1, j + 1, k + 1), P(i, j + 1, k + 1))
    right = Polygon(P(i + 1, j, k), P(i + 1, j + 1, k), P(i + 1, j + 1, k + 1), P(i + 1, j, k + 1))
    left = Polygon(P(i, j + 1, k), P(i + 1, j + 1, k), P(i + 1, j + 1, k + 1), P(i, j + 1, k + 1))
    for poly, k_ in ((top, 0.62), (right, 0.42), (left, 0.30)):
        poly.base = k_
        poly.set_fill(mix(GOLD, k_), 1).set_stroke(GOLD, 3)
    g = VGroup(left, right, top)
    g.set_z_index(i + j + k)
    return g


def cube_n(origin, a, n):
    cells = sorted([(i, j, k) for i in range(n) for j in range(n) for k in range(n)], key=sum)
    g = VGroup(*[cell(origin, a, c) for c in cells])
    return g


def shimmer(g, period=2.4):
    g._sh = 0.0

    def f(mob, dt):
        mob._sh += dt
        s = 0.8 + 0.2 * np.sin(2 * np.pi * mob._sh / period)
        for p in mob.family_members_with_points():
            if hasattr(p, "base"):
                p.set_fill(mix(GOLD, p.base * s), 1)
    g.add_updater(f)
    return g


def vbracket(x, y0, y1, color=GOLD):
    return VGroup(Line([x, y0, 0], [x, y1, 0]), Line([x - 0.12, y0, 0], [x + 0.12, y0, 0]),
                  Line([x - 0.12, y1, 0], [x + 0.12, y1, 0])).set_stroke(color, 4)


def bgtext(text, size=28, color=TEXT, **kw):
    t = T(text, size, color, **kw)
    r = BackgroundRectangle(t, color=BG, fill_opacity=0.85, buff=0.08)
    return VGroup(r, t)


A = 1.25
SMALL = np.array([-5.0, 0.0, 0])
BIG = np.array([-0.6, 0.0, 0])


def counter(prefix, tr, pos, color, size=36):
    return always_redraw(lambda: M(f"{prefix} \u00d7 {int(round(tr.get_value()))}", size, color).move_to(pos))


def gauge(center, r, tr, color=BLUE, wrap=False, ring_color=TEXT):
    center = np.array(center, float)
    ring = Circle(r, stroke_color=ring_color, stroke_width=4).move_to(center)
    knob = Rectangle(width=0.3, height=0.16, stroke_width=0, fill_color=ring_color, fill_opacity=1).move_to(center + UP * (r + 0.1))

    def sec():
        v = tr.get_value()
        v = (v % 1) if wrap else v
        return Sector(radius=r * 0.9, angle=-2 * PI * max(v, 0.003), start_angle=PI / 2, arc_center=center,
                      fill_color=color, fill_opacity=0.7, stroke_width=0)
    return VGroup(ring, knob, always_redraw(sec))


# ------------------------------------------------------------------ animals
def planarian(w=5.5, color=TEXT):
    body = Ellipse(width=w, height=w * 0.24, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.1)
    ears = VGroup(*[Circle(radius=w * 0.04, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.1)
                    .move_to([-w * 0.43, s * w * 0.12, 0]) for s in (1, -1)])
    eyes = VGroup(*[Dot(radius=w * 0.015, color=color).move_to([-w * 0.36, s * w * 0.04, 0]) for s in (1, -1)])
    g = VGroup(body, ears, eyes)
    g.body = body
    return g


def heart_shape(size, center, color=RED):
    f = lambda t: np.array([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0])
    h = ParametricFunction(f, t_range=[0, 2 * PI], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=1)
    h.set_height(size)
    h.move_to(center)
    return h


def mouse(center=ORIGIN, s=1.0, color=TEXT):
    """Mouse silhouette facing left. Returns (group, mp) where mp maps local (x, y) to the screen."""
    center = np.array(center, float)
    mp = lambda x, y: center + s * np.array([x - 0.7, y, 0])
    body = Ellipse(width=7.0, height=3.8).move_to([0.5, 0, 0])
    head = Ellipse(width=2.8, height=2.2).move_to([-3.6, 0.15, 0])
    nose = Circle(0.35).move_to([-4.75, -0.05, 0])
    ear = Circle(0.55).move_to([-3.3, 1.35, 0])
    l1 = Ellipse(width=1.1, height=0.8).move_to([-1.5, -1.8, 0])
    l2 = Ellipse(width=1.1, height=0.8).move_to([2.5, -1.8, 0])
    sil = Union(body, head, nose, ear, l1, l2).set_stroke(color, 4).set_fill(color, 0.07)
    tail = ArcBetweenPoints(np.array([3.9, -0.2, 0]), np.array([6.2, 1.7, 0]), angle=-1.0).set_stroke(color, 4)
    eye = Dot([-4.2, 0.45, 0], radius=0.07, color=color)
    g = VGroup(sil, tail, eye)
    g.scale(s, about_point=ORIGIN).shift(center - s * np.array([0.7, 0, 0]))
    return g, mp


def lungs(mp, s):
    lg = VGroup()
    for x in (-2.75, -0.8):
        lg.add(Ellipse(width=1.5 * s, height=1.8 * s, stroke_color=PALE, stroke_width=3, fill_color=PALE, fill_opacity=0.15).move_to(mp(x, 0.5)))
    br = VGroup()
    for x in (-2.75, -0.8):
        for dy in (0.6, 0.2, -0.2):
            br.add(Line(mp(-1.77, 0.9), mp(x + (0.3 if x < -2 else -0.3), 0.5 + dy), stroke_width=2, color=PALE))
    return VGroup(lg, br)


def channels(mp, src, seed=3):
    rng = np.random.default_rng(seed)
    targets = [(-4.2, 0.7), (-3.6, -0.9), (-0.5, 1.5), (2.2, 1.1), (0.5, -1.5), (2.6, -1.75), (-1.5, -1.75), (4.1, -0.1), (3.3, 0.5), (1.0, 0.2)]
    paths = VGroup()
    for tx, ty in targets:
        a = np.array(src, float)
        b = mp(tx, ty)
        c1 = a + (b - a) * 0.35 + np.array([rng.normal(0, 0.25), rng.normal(0, 0.25), 0])
        c2 = a + (b - a) * 0.7 + np.array([rng.normal(0, 0.25), rng.normal(0, 0.25), 0])
        paths.add(CubicBezier(a, c1, c2, b).set_stroke(RED, 4))
    return paths


# ------------------------------------------------------------------ balls
def ball(center, R, prof, core=0.0, n=30):
    g = VGroup()
    for i in range(n):
        r = R * (1 - i / n)
        g.add(Circle(radius=r, stroke_width=0, fill_color=mix(BLUE, prof(r, R), LOW), fill_opacity=1).move_to(center))
    if core > 0.02:
        g.add(Circle(radius=core, stroke_color=GREY, stroke_width=2, fill_color=CORE, fill_opacity=1).move_to(center))
    g.add(Circle(radius=R, stroke_color=GOLD, stroke_width=9, fill_opacity=0).move_to(center))
    return g


def prof_soak(r, R):
    return float(np.exp(-(R - r) / 0.95))


def prof_steady(r, R):
    return float((r / R) ** 2)


def sheet(width, thick, y=0.2, n=14):
    g = VGroup()
    for i in range(n):
        yy = (0.5 - (i + 0.5) / n) * thick
        c = 0.45 + 0.55 * (abs(yy) / (thick / 2)) ** 2
        g.add(Rectangle(width=width, height=thick / n + 0.01, stroke_width=0, fill_color=mix(BLUE, c, LOW), fill_opacity=1).move_to([0, y + yy, 0]))
    g.add(Line([-width / 2, y + thick / 2, 0], [width / 2, y + thick / 2, 0]).set_stroke(GOLD, 8))
    g.add(Line([-width / 2, y - thick / 2, 0], [width / 2, y - thick / 2, 0]).set_stroke(GOLD, 8))
    return g


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Size, Scale and Surface"
    TITLE = "Why a Mouse Needs Plumbing"


class S01Hook(SpokenScene):
    def construct(self):
        pl = planarian(5.5).move_to([-3.4, 0.2, 0])
        glide(pl, 0.35, 0.08, 7.0)
        self.play(FadeIn(pl), run_time=0.6)
        lab1 = T("no lungs, no heart", 32, TEXT).move_to([-3.4, -1.6, 0])
        self.at("no lungs")
        self.play(FadeIn(lab1, shift=UP * 0.15), run_time=0.6)
        self.at("A mouse", lead=0.1)
        m, mp = mouse([3.7, 0.0, 0], 0.5)
        lg = lungs(mp, 0.5)
        ht = heart_shape(0.5, mp(-1.75, -0.35))
        beat(ht, 0.9)
        self.play(FadeIn(m), FadeIn(lg), FadeIn(ht), run_time=0.7)
        lab2 = T("lungs and heart", 32, TEXT).move_to([3.7, -1.6, 0])
        self.at("both")
        self.play(FadeIn(lab2, shift=UP * 0.15), run_time=0.6)
        q = T("?", 110, YELLOW, font=TITLE_FONT).move_to([0.0, 0.3, 0])
        pulse(q, 1.0, 0.18)
        self.at("what changed")
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.finish()


class S02Surface(SpokenScene):
    def construct(self):
        pl = planarian(5.5).move_to([-3.4, 0.2, 0])
        m, mp = mouse([3.7, 0.0, 0], 0.5)
        lg = lungs(mp, 0.5)
        ht = heart_shape(0.5, mp(-1.75, -0.35))
        beat(ht, 0.9)
        glide(pl, 0.2, 0.06, 6.0)
        self.add(pl, m, lg, ht)
        self.play(FadeOut(VGroup(m, lg, ht)), pl.animate.scale(1.7).move_to([0, 0.2, 0]), run_time=1.4)
        self.at("takes in", lead=0.0)
        self.play(pl.body.animate.set_stroke(GOLD, 9), run_time=0.8)
        a, b = 4.7, 1.05
        rng = np.random.default_rng(5)
        ds = dots(16)
        for i, d in enumerate(ds):
            th = rng.uniform(0.25, 2 * PI - 0.25)
            if abs(np.sin(th)) < 0.25:
                th += 0.5
            sweep(d, [1.12 * a * np.cos(th), 0.2 + 2.1 * b * np.sin(th), 0], [0.6 * a * np.cos(th), 0.2 + 0.4 * b * np.sin(th), 0],
                  2.2, off=i / 16)
            d.move_to([0, 3, 0])
        self.add(ds)
        self.finish()


class S03Cube(SpokenScene):
    def construct(self):
        small = cell(BIG, A, (1, 1, 1))
        shimmer(small)
        lab = T("s = 10 \u00b5m", 32, TEXT).move_to([BIG[0], 1.9, 0])
        glide(small, 0.0, 0.1, 3.0)
        br = vbracket(BIG[0] - 1.4, BIG[1] - A * 0.5, BIG[1] + A * 0.5)
        self.play(FadeIn(small, scale=0.8), run_time=0.8)
        self.at("tiny cube")
        self.play(FadeIn(lab), Create(br), run_time=0.6)
        self.at("gold faces")
        self.play(*[p.animate.set_stroke(YELLOW, 7) for p in small.family_members_with_points() if hasattr(p, "base")],
                  run_time=0.5, rate_func=there_and_back)
        sl = T("surface", 34, GOLD).move_to([-4.0, 1.0, 0])
        sa = Arrow([-3.1, 0.9, 0], [BIG[0] - 1.1, 0.5, 0], buff=0, color=GOLD, stroke_width=4)
        self.at("surface")
        self.play(FadeIn(sl), GrowArrow(sa), run_time=0.6)
        inner = cell(BIG, A * 0.5, (1, 1, 1))
        for p in inner:
            p.set_fill(mix(PALE, p.base), 1).set_stroke(PALE, 3)
        inner.set_z_index(20)
        vl = T("volume", 34, PALE).move_to([2.6, 0.2, 0])
        va = Arrow([1.7, 0.2, 0], [BIG[0] + 0.35, 0.2, 0], buff=0, color=PALE, stroke_width=4)
        self.at("its inside")
        self.play(FadeIn(inner, scale=0.5), run_time=0.6)
        self.at("volume")
        self.play(FadeIn(vl), GrowArrow(va), run_time=0.6)
        self.at("now make", lead=0.0)
        small.clear_updaters()
        shimmer(small)
        self.play(FadeOut(VGroup(sl, sa, vl, va, inner)), small.animate.move_to(BIG), run_time=0.5)
        big_cells = []
        for c in sorted([(i, j, k) for i in range(2) for j in range(2) for k in range(2) if (i, j, k) != (1, 1, 1)], key=sum):
            big_cells.append(cell(BIG, A, c))
        for g in big_cells:
            shimmer(g)
        self.at("every")
        lab2 = T("s = 20 \u00b5m", 32, TEXT).move_to([BIG[0], 3.1, 0])
        br2 = vbracket(BIG[0] - 2.35, BIG[1] - A, BIG[1] + A)
        self.play(LaggedStart(*[ReplacementTransform(small.copy(), g) for g in big_cells], lag_ratio=0.12),
                  Transform(lab, lab2), Transform(br, br2), run_time=1.6)
        self.add(*big_cells)
        cp = cell(SMALL, A, (1, 1, 1))
        shimmer(cp)
        self.play(FadeIn(cp, shift=LEFT * 1.0), run_time=0.6)
        self.finish()


def two_cubes(sc, labels=True):
    s_ = cell(SMALL, A, (1, 1, 1))
    shimmer(s_)
    b_ = cube_n(BIG, A, 2)
    shimmer(b_)
    sc.add(s_, b_)
    out = [s_, b_]
    if labels:
        l1 = T("s = 10 \u00b5m", 32, TEXT).move_to([SMALL[0], 1.8, 0])
        l2 = T("s = 20 \u00b5m", 32, TEXT).move_to([BIG[0], 3.1, 0])
        sc.add(l1, l2)
        out += [l1, l2]
    return out


class S04Ratio(SpokenScene):
    def construct(self):
        s_, b_, l1, l2 = two_cubes(self)
        vt, st = ValueTracker(1), ValueTracker(1)
        vc = counter("volume", vt, [4.6, 2.5, 0], PALE)
        sc_ = counter("surface", st, [4.6, 1.4, 0], GOLD)
        self.add(vc, sc_)
        self.at("eight times", lead=0.3)
        self.play(vt.animate.set_value(8), Indicate(b_, color=PALE, scale_factor=1.03), run_time=1.8)
        self.at("outer surface", lead=0.3)
        self.play(st.animate.set_value(4), run_time=1.4)
        rt = ValueTracker(0.6)
        title = T("surface \u00f7 volume", 30, TEXT).move_to([4.7, -0.3, 0])
        num = always_redraw(lambda: M(f"{rt.get_value():.1f} per \u00b5m", 40, GOLD).move_to([4.7, -1.2, 0]))
        sub = M("= 6 / s", 34, TEXT).move_to([4.7, -2.1, 0])
        bar_box = Rectangle(width=3.6, height=0.4, stroke_color=TEXT, stroke_width=3).move_to([4.7, -3.0, 0])
        bar = always_redraw(lambda: Rectangle(width=3.6 * rt.get_value() / 0.6, height=0.4, stroke_width=0, fill_color=GOLD,
                                              fill_opacity=0.8).move_to([4.7 - 1.8 + 1.8 * rt.get_value() / 0.6, -3.0, 0]))
        self.at("each bit")
        self.play(FadeIn(title), FadeIn(num), FadeIn(sub), FadeIn(bar_box), FadeIn(bar), run_time=0.8)
        self.at("half as much")
        self.play(rt.animate.set_value(0.3), run_time=1.8)
        self.finish()


class S05Far(SpokenScene):
    def construct(self):
        s_, b_ = two_cubes(self, labels=False)
        vt, st = ValueTracker(8), ValueTracker(4)
        vc = counter("volume", vt, [4.6, 2.5, 0], PALE)
        sc_ = counter("surface", st, [4.6, 1.4, 0], GOLD)
        self.add(vc, sc_)
        self.play(vc.animate.set_opacity(0.4), sc_.animate.set_opacity(0.4), Indicate(s_), run_time=1.0)
        self.at("center of")
        d1, d2 = dots(1, BLUE, 0.15)[0], dots(1, BLUE, 0.15)[0]
        d1.move_to(SMALL)
        d2.move_to(BIG)
        h1, h2 = 0.5 * A, A
        ln1 = DashedLine(SMALL, SMALL + UP * h1, color=BLUE, stroke_width=4)
        ln2 = DashedLine(BIG, BIG + UP * h2, color=BLUE, stroke_width=4)
        self.play(FadeIn(d1, scale=2), FadeIn(d2, scale=2), run_time=0.6)
        self.play(Create(ln1), Create(ln2), run_time=1.0)
        t1 = bgtext("5 \u00b5m", 30, BLUE).move_to(SMALL + [1.1, 0.5, 0])
        t2 = bgtext("10 \u00b5m", 30, BLUE).move_to(BIG + [1.2, 0.9, 0])
        for o in (d1, d2, ln1, ln2, t1, t2):
            o.set_z_index(30)
        self.add(t1, t2)
        self.at("twice as far")
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.5)
        tw = T("2 \u00d7 farther", 48, BLUE).move_to([4.6, -0.3, 0])
        self.play(FadeIn(tw, shift=UP * 0.2), run_time=0.6)
        self.at("oxygen must")
        trav1 = Dot(radius=0.1, color=BLUE)
        trav2 = Dot(radius=0.1, color=BLUE)
        trav1.set_z_index(31); trav2.set_z_index(31)
        sweep(trav1, SMALL + UP * h1, SMALL, 1.6, fade=0.1)
        sweep(trav2, BIG + UP * h2, BIG, 3.2, fade=0.1)
        trav1.move_to(SMALL + UP * h1)
        trav2.move_to(BIG + UP * h2)
        self.add(trav1, trav2)
        self.finish()


class S06Walk(SpokenScene):
    def construct(self):
        s_ = cell(SMALL, A, (1, 1, 1))
        self.add(s_)
        x0, x1, y0, y1 = -6.2, 1.8, -3.0, 3.0
        block = Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=PALE, stroke_width=3, fill_color=LOW, fill_opacity=1)
        block.move_to([(x0 + x1) / 2, 0, 0])
        wall = Line([x0, y0, 0], [x0, y1, 0]).set_stroke(GOLD, 12)
        self.play(ReplacementTransform(s_, block), FadeIn(wall), run_time=1.2)
        tr = ValueTracker(0)
        sw = gauge([4.5, 1.6, 0], 1.0, tr, BLUE, wrap=True)
        swl = T("time", 30, TEXT).move_to([4.5, 0.1, 0])
        self.play(FadeIn(sw), FadeIn(swl), run_time=0.5)
        tr.add_updater(lambda m, dt: m.increment_value(dt * 0.4))
        self.add(tr)
        lead = Dot(radius=0.14, color=YELLOW).move_to([x0 + 0.1, 0.5, 0])
        brown(lead, (x0, x1, y0, y1), 1.6, 1)
        pts = [lead.get_center()]
        trail = VMobject(stroke_color=YELLOW, stroke_width=3, stroke_opacity=0.7)

        def tf(m, dt):
            pts.append(lead.get_center())
            if len(pts) > 2:
                m.set_points_as_corners(pts)
        trail.add_updater(tf)
        self.add(trail, lead)
        dl = T("diffusion", 34, BLUE).move_to([4.5, -1.6, 0])
        self.at("diffusion", lead=0.0)
        self.play(FadeIn(dl), run_time=0.5)
        self.at("as likely")
        swarm = dots(14)
        for i, d in enumerate(swarm):
            d.move_to([x0 + 0.1, np.random.default_rng(i).uniform(y0 + 0.3, y1 - 0.3), 0])
            brown(d, (x0, x1, y0, y1), 1.6, 10 + i)
        self.play(FadeIn(swarm), run_time=0.6)
        self.finish()


TOP_Y, BOT_Y = 2.25, -0.7


def tube_world(sc, top_t, bot_t, card=None, bottom=True, top_read=True, bot_read="?"):
    """Two diffusion tubes with gold ends and a stopwatch fill each. Returns a dict of the parts."""
    parts = {}
    top = Rectangle(width=4, height=1.1, stroke_color=PALE, stroke_width=3, fill_color=LOW, fill_opacity=1).move_to([-4.0, TOP_Y, 0])
    cap1 = Line([-6, TOP_Y - 0.55, 0], [-6, TOP_Y + 0.55, 0]).set_stroke(GOLD, 12)
    l1 = T("L = 5 \u00b5m", 30, TEXT).move_to([-4.0, TOP_Y - 1.05, 0])
    d1 = dots(4)
    for i, d in enumerate(d1):
        d.move_to([-5.8 + 0.1 * i, TOP_Y, 0])
        brown(d, (-5.9, -2.1, TOP_Y - 0.45, TOP_Y + 0.45), 1.4, i)
    g1 = gauge([4.6, TOP_Y, 0], 0.8, top_t, BLUE)
    r1 = M("0.0125 s", 32, TEXT).move_to([4.6, TOP_Y - 1.25, 0])
    sc.add(top, cap1, l1, d1, g1)
    parts.update(top=top, l1=l1, g1=g1, r1=r1)
    if top_read:
        sc.add(r1)
    if bottom:
        bot = Rectangle(width=8, height=1.1, stroke_color=PALE, stroke_width=3, fill_color=LOW, fill_opacity=1).move_to([-2.0, BOT_Y, 0])
        cap2 = Line([-6, BOT_Y - 0.55, 0], [-6, BOT_Y + 0.55, 0]).set_stroke(GOLD, 12)
        l2 = T("L = 10 \u00b5m", 30, TEXT).move_to([-2.0, BOT_Y - 1.05, 0])
        d2 = dots(6)
        for i, d in enumerate(d2):
            d.move_to([-5.8 + 0.1 * i, BOT_Y, 0])
            brown(d, (-5.9, 1.9, BOT_Y - 0.45, BOT_Y + 0.45), 1.4, 20 + i)
        g2 = gauge([4.6, BOT_Y, 0], 0.8, bot_t, BLUE)
        sc.add(bot, cap2, l2, d2, g2)
        parts.update(bot=bot, l2=l2, g2=g2)
        if bot_read:
            r2 = M(bot_read, 32, TEXT).move_to([4.6, BOT_Y - 1.25, 0])
            sc.add(r2)
            parts["r2"] = r2
    if card:
        c = chip(card, YELLOW, 34).move_to([0, -3.1, 0])
        sc.add(c)
        parts["card"] = c
    return parts


class S07Predict(SpokenScene):
    def construct(self):
        t1, t2 = ValueTracker(0), ValueTracker(0)
        top = Rectangle(width=4, height=1.1, stroke_color=PALE, stroke_width=3, fill_color=LOW, fill_opacity=1).move_to([-4.0, TOP_Y, 0])
        cap1 = Line([-6, TOP_Y - 0.55, 0], [-6, TOP_Y + 0.55, 0]).set_stroke(GOLD, 12)
        d1 = dots(4)
        for i, d in enumerate(d1):
            d.move_to([-5.8 + 0.1 * i, TOP_Y, 0])
            brown(d, (-5.9, -2.1, TOP_Y - 0.45, TOP_Y + 0.45), 1.4, i)
        self.add(top, cap1, d1)
        l1 = T("L = 5 \u00b5m", 30, TEXT).move_to([-4.0, TOP_Y - 1.05, 0])
        g1 = gauge([4.6, TOP_Y, 0], 0.8, t1, BLUE)
        self.at("5 micrometers", lead=0.4)
        self.play(FadeIn(l1), FadeIn(g1), run_time=0.6)
        self.at("takes about")
        self.play(t1.animate.set_value(0.25), run_time=0.9, rate_func=linear)
        r1 = M("0.0125 s", 32, TEXT).move_to([4.6, TOP_Y - 1.25, 0])
        self.at("hundredth")
        self.play(FadeIn(r1), run_time=0.5)
        bot = Rectangle(width=8, height=1.1, stroke_color=PALE, stroke_width=3, fill_color=LOW, fill_opacity=1).move_to([-2.0, BOT_Y, 0])
        cap2 = Line([-6, BOT_Y - 0.55, 0], [-6, BOT_Y + 0.55, 0]).set_stroke(GOLD, 12)
        d2 = dots(6)
        for i, d in enumerate(d2):
            d.move_to([-5.8 + 0.1 * i, BOT_Y, 0])
            brown(d, (-5.9, 1.9, BOT_Y - 0.45, BOT_Y + 0.45), 1.4, 20 + i)
        self.at("double")
        self.play(GrowFromEdge(bot, LEFT), FadeIn(cap2), run_time=1.0)
        self.add(d2)
        l2 = T("L = 10 \u00b5m", 30, TEXT).move_to([-2.0, BOT_Y - 1.05, 0])
        g2 = gauge([4.6, BOT_Y, 0], 0.8, t2, BLUE)
        self.at("10 micrometers")
        self.play(FadeIn(l2), FadeIn(g2), run_time=0.6)
        card = chip("L = 10 \u00b5m: how long?", YELLOW, 34).move_to([0, -3.1, 0])
        r2 = M("? s", 32, YELLOW).move_to([4.6, BOT_Y - 1.25, 0])
        self.at("how much longer")
        self.play(FadeIn(card, shift=UP * 0.2), FadeIn(r2), run_time=0.6)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        t1, t2 = ValueTracker(0.25), ValueTracker(0)
        parts = tube_world(self, t1, t2, card="L = 10 \u00b5m: how long?", bot_read="? s")
        parts["r2"].set_color(YELLOW)
        tr = ValueTracker(1)
        ring = gauge([6.0, -3.0, 0], 0.5, tr, YELLOW)
        self.add(ring)
        self.play(tr.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        t1, t2 = ValueTracker(0.25), ValueTracker(0)
        parts = tube_world(self, t1, t2, card="L = 10 \u00b5m: how long?", bot_read=None)
        r2 = always_redraw(lambda: M(f"{0.05 * t2.get_value():.3f} s", 32, TEXT).move_to([4.6, BOT_Y - 1.25, 0]))
        self.add(r2)
        self.play(FadeOut(parts["card"]), t2.animate.set_value(1.0), run_time=1.0, rate_func=linear)
        x4 = T("\u00d7 4", 40, YELLOW).move_to([6.2, BOT_Y, 0])
        self.at("long")
        self.play(FadeIn(x4, scale=1.3), run_time=0.5)
        form = M("t = L\u00b2 / 2D", 42, TEXT).move_to([-3.0, -2.7, 0])
        dnote = T("D = 1,000 \u00b5m\u00b2 per s", 30, TEXT).move_to([-3.0, -3.4, 0])
        self.at("diffusion time")
        self.play(Write(form), run_time=1.5)
        self.play(FadeIn(dnote), run_time=0.5)
        self.at("square of")
        self.play(Indicate(form, color=YELLOW, scale_factor=1.12), run_time=1.0)
        s1 = T("2 \u00d7 distance = 4 \u00d7 time", 30, YELLOW).move_to([3.2, -2.7, 0])
        self.at("twice as far", lead=0.0)
        self.play(FadeIn(s1, shift=UP * 0.15), run_time=0.7)
        s2 = T("10 \u00d7 distance = 100 \u00d7 time", 30, RED).move_to([3.2, -3.4, 0])
        self.at("ten times", lead=0.0)
        self.play(FadeIn(s2, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S10Cm(SpokenScene):
    def construct(self):
        x0, x1, y0, y1 = -6.2, 1.8, -3.0, 3.0
        block = Rectangle(width=x1 - x0, height=y1 - y0, stroke_color=PALE, stroke_width=3, fill_color=LOW, fill_opacity=1).move_to([-2.2, 0, 0])
        wall = Line([x0, y0, 0], [x0, y1, 0]).set_stroke(GOLD, 12)
        d = dots(8)
        for i, p in enumerate(d):
            p.move_to([-5.5 + 0.2 * i, np.sin(i) * 2, 0])
            brown(p, (x0, x1, y0, y1), 1.6, i)
        self.add(block, wall, d)
        self.wait(self.t_of("now zoom") - 0.3 - self.elapsed())
        fy = 0.1
        finger = RoundedRectangle(corner_radius=2.0, width=4.2, height=6.0, stroke_color=PALE, stroke_width=4, fill_color=PALE, fill_opacity=0.08).move_to([-2.2, -0.75, 0])
        nail = Arc(radius=1.2, start_angle=0.5, angle=PI - 1.0, color=PALE, stroke_width=3).move_to([-2.2, 1.4, 0])
        brk = VGroup(Line([-4.3, 3.45, 0], [-0.1, 3.45, 0]), Line([-4.3, 3.3, 0], [-4.3, 3.6, 0]), Line([-0.1, 3.3, 0], [-0.1, 3.6, 0])).set_stroke(GOLD, 4)
        bl = T("1 cm", 32, GOLD).move_to([-2.2, 2.85, 0])
        speck = Dot([-5.4, -2.0, 0], radius=0.06, color=GOLD)
        sl = T("a cell", 30, TEXT).move_to([-5.7, -1.4, 0])
        self.at("zoom out", lead=0.0)
        self.play(FadeOut(d), FadeOut(wall), block.animate.scale(0.01).move_to([-5.4, -2.0, 0]),
                  FadeIn(finger), FadeIn(nail), FadeIn(speck), FadeIn(sl), run_time=1.2)
        self.remove(block)
        self.at("centimeter", lead=0.0)
        self.play(Create(brk), FadeIn(bl), run_time=0.8)
        h = ValueTracker(0)
        c = np.array([4.2, 0.0, 0])
        face = Circle(2.0, stroke_color=TEXT, stroke_width=5).move_to(c)
        ticks = VGroup(*[Line(c + 1.75 * np.array([np.sin(a), np.cos(a), 0]), c + 1.95 * np.array([np.sin(a), np.cos(a), 0])).set_stroke(TEXT, 3)
                         for a in np.arange(12) * PI / 6])
        mh = always_redraw(lambda: Line(c, c + 1.7 * np.array([np.sin(2 * PI * h.get_value()), np.cos(2 * PI * h.get_value()), 0])).set_stroke(YELLOW, 5))
        hh = always_redraw(lambda: Line(c, c + 1.1 * np.array([np.sin(2 * PI * h.get_value() / 12), np.cos(2 * PI * h.get_value() / 12), 0])).set_stroke(TEXT, 8))
        self.at("about a finger", lead=0.0)
        self.play(FadeIn(face), FadeIn(ticks), FadeIn(mh), FadeIn(hh), run_time=0.6)
        self.at("the same", lead=0.0)
        self.play(h.animate.set_value(14), run_time=2.4, rate_func=linear)
        lab = T("\u2248 14 hours", 44, YELLOW).move_to([4.2, -2.8, 0])
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.5)
        self.finish()


class S11Ball(SpokenScene):
    def construct(self):
        C = np.array([-2.4, 0.0, 0])
        R = 2.9
        front = ValueTracker(0)
        b = ball(C, R, prof_soak)

        def upd(m):
            fr = front.get_value()
            m.become(ball(C, R, lambda r, RR: prof_soak(r, RR) * min(1, max(0, (fr - (RR - r)) / 0.5))))
        b.add_updater(upd)
        self.play(FadeIn(b, scale=0.7), run_time=1.2)
        self.at("gold skin", lead=0.2)
        skin = T("gold skin", 34, GOLD).move_to([4.2, 2.2, 0])
        sa = Arrow([3.0, 2.0, 0], C + np.array([np.cos(0.6), np.sin(0.6), 0]) * R, buff=0.05, color=GOLD, stroke_width=4)
        self.play(FadeIn(skin), GrowArrow(sa), run_time=0.6)
        self.at("oxygen soaks", lead=0.0)
        self.play(front.animate.set_value(4.0), run_time=2.6, rate_func=linear)
        ds = dots(12, BLUE, 0.1)
        rng = np.random.default_rng(2)
        for i, d in enumerate(ds):
            th = rng.uniform(0, 2 * PI)
            u = np.array([np.cos(th), np.sin(th), 0])
            sweep(d, C + u * (R + 0.15), C + u * (R - 1.3), 2.4, off=i / 12, fade=0.2)
        self.add(ds)
        lab = T("oxygen used", 32, BLUE).move_to([4.2, -0.3, 0])
        lab2 = T("on the way in", 32, BLUE).move_to([4.2, -0.85, 0])
        lab3 = T("(schematic)", 28, TEXT).move_to([4.2, -1.5, 0])
        self.at("burns it", lead=0.4)
        self.play(FadeIn(lab), FadeIn(lab2), FadeIn(lab3), run_time=0.6)
        self.finish()


class S12Core(SpokenScene):
    def construct(self):
        C = np.array([-2.4, 0.0, 0])
        Rt = ValueTracker(2.9)
        Rt.add_updater(lambda m, dt: m.set_value(2.9 + 0.8 * min(1, max(0, (self.elapsed() - 0.5) / 9.3))))

        def mk():
            R = Rt.get_value()
            return ball(C, R, prof_soak, core=max(0.0, 2.2 * (R - 3.4)))
        b = always_redraw(mk)
        ds = dots(12, BLUE, 0.1)
        rng = np.random.default_rng(4)
        ang = [rng.uniform(0, 2 * PI) for _ in ds]

        for i, d in enumerate(ds):
            d._tt = i * 0.2
            d.ang = ang[i]

            def f(mob, dt):
                mob._tt += dt
                fr = (mob._tt / 2.4) % 1
                R = Rt.get_value()
                u = np.array([np.cos(mob.ang), np.sin(mob.ang), 0])
                mob.move_to(C + u * (R + 0.15 - 1.45 * fr))
                mob.set_opacity(min(1, fr / 0.2, (1 - fr) / 0.2))
            d.add_updater(f)
        ring = DashedVMobject(Circle(3.4, stroke_color=TEXT, stroke_width=3).move_to(C), num_dashes=60)
        self.add(Rt, b, ds)
        self.at("tissue holds", lead=0.0)
        lim = T("schematic limit", 28, TEXT).move_to([5.0, 2.7, 0])
        la = Arrow([4.0, 2.5, 0], C + np.array([np.cos(0.5), np.sin(0.5), 0]) * 3.4, buff=0.05, color=TEXT, stroke_width=3)
        self.play(FadeIn(ring), FadeIn(lim), GrowArrow(la), run_time=0.8)
        self.wait(self.t_of("in this ideal") - 0.2 - self.elapsed())
        lab = T("ideal model;", 30, TEXT).move_to([4.3, -0.2, 0])
        lab2 = T("core size schematic", 30, TEXT).move_to([4.3, -0.75, 0])
        self.play(FadeIn(lab), FadeIn(lab2), run_time=0.6)
        cl = T("no oxygen", 34, TEXT).move_to([4.3, -2.4, 0])
        ca = Arrow([3.0, -2.2, 0], C + [0.5, 0, 0], buff=0.05, color=GREY, stroke_width=3)
        self.at("runs out")
        self.play(FadeIn(cl), GrowArrow(ca), run_time=0.6)
        self.finish()


class S13Depth(SpokenScene):
    def construct(self):
        CL = np.array([-3.2, 0.1, 0])
        CR = np.array([3.8, 0.1, 0])
        Rt = ValueTracker(1.0)
        left = always_redraw(lambda: ball(CL, Rt.get_value(), prof_steady))
        self.add(left)
        self.play(Rt.animate.set_value(2.9), run_time=3.0)
        ds = dots(8, BLUE, 0.08)
        rng = np.random.default_rng(7)
        for i, d in enumerate(ds):
            th = rng.uniform(0, 2 * PI)
            u = np.array([np.cos(th), np.sin(th), 0])
            sweep(d, CL + u * 3.0, CL + u * 1.7, 2.2, off=i / 8, fade=0.2)
        self.add(ds)
        self.at("slow tissue", lead=0.0)
        sl = T("slow tissue", 32, TEXT).move_to([-3.2, 3.5, 0])
        self.play(FadeIn(sl), run_time=0.5)
        rad = Line(CL, CL + RIGHT * 2.9).set_stroke(TEXT, 4)
        self.at("millimeter of radius", lead=0.5)
        rl = T("limiting radius \u2248 1.45 mm", 30, TEXT).move_to([-3.2, -3.35, 0])
        self.play(Create(rad), FadeIn(rl), run_time=0.8)
        Rs = 2.9 * 0.19 / 1.45
        right = ball(CR, Rs, prof_steady, n=12)
        self.at("busy tissue", lead=0.0)
        bl = T("busy tissue", 32, TEXT).move_to([3.8, 1.3, 0])
        self.play(FadeIn(right, scale=0.2), FadeIn(bl), run_time=0.8)
        rr = T("\u2248 0.19 mm", 30, TEXT).move_to([3.8, -0.6, 0])
        sc = T("same scale", 28, TEXT).move_to([3.8, -1.5, 0])
        self.at("few tenths")
        self.play(FadeIn(rr), FadeIn(sc), run_time=0.6)
        self.finish()


class S14Flat(SpokenScene):
    def construct(self):
        CL = np.array([-3.2, 0.1, 0])
        b = ball(CL, 2.9, prof_steady)
        ds = dots(8, BLUE, 0.08)
        rng = np.random.default_rng(7)
        for i, d in enumerate(ds):
            th = rng.uniform(0, 2 * PI)
            u = np.array([np.cos(th), np.sin(th), 0])
            sweep(d, CL + u * 3.0, CL + u * 1.7, 2.2, off=i / 8, fade=0.2)
        self.add(b, ds)
        self.wait(0.4)
        sh = sheet(8.4, 2.4, y=0.1)
        self.at("takes another", lead=0.2)
        self.play(FadeOut(ds), ReplacementTransform(b, sh), run_time=2.0)
        flow = dots(14, BLUE, 0.09)
        for i, d in enumerate(flow):
            x = -3.8 + 7.6 * (i % 7) / 6
            if i < 7:
                sweep(d, [x, 1.65, 0], [x, 0.7, 0], 2.4, off=(i * 0.37) % 1, fade=0.2)
            else:
                sweep(d, [x, -1.25, 0], [x, -0.3, 0], 2.4, off=(i * 0.37) % 1, fade=0.2)
        self.add(flow)
        self.at("grows long", lead=0.0)
        a1 = Arrow([-4.3, 0.2, 0], [-5.9, 0.2, 0], buff=0, color=TEXT, stroke_width=6)
        a2 = Arrow([4.3, 0.2, 0], [5.9, 0.2, 0], buff=0, color=TEXT, stroke_width=6)
        self.play(sh.animate.stretch_to_fit_width(10.6), FadeIn(a1), FadeIn(a2), run_time=1.6)
        lw = T("long and wide", 34, TEXT).move_to([0, 2.35, 0])
        self.play(FadeIn(lw), run_time=0.4)
        self.at("stays thin", lead=0.0)
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(lw), sh.animate.stretch_to_fit_height(2.7), run_time=1.0)
        br = vbracket(5.8, -0.95, 1.35, TEXT)
        th = T("stays thin", 34, TEXT).move_to([4.0, -2.0, 0])
        self.play(Create(br), FadeIn(th), run_time=0.6)
        self.at("every cell", lead=0.0)
        cl = T("every cell near the outside", 32, BLUE).move_to([0, -2.9, 0])
        self.play(FadeIn(cl), run_time=0.6)
        self.finish()


class S15Mouse(SpokenScene):
    def construct(self):
        m, mp = mouse([0.0, -0.1, 0], 1.12)
        hpos = mp(-1.75, -0.35)
        ht = heart_shape(0.8, hpos)
        beat(ht, 0.9)
        self.play(FadeIn(m), run_time=0.8)
        self.play(FadeIn(ht), run_time=0.5)
        self.at("tissue runs")
        chs = channels(mp, hpos)
        self.at("moves fluid", lead=0.0)
        self.play(LaggedStart(*[Create(c) for c in chs], lag_ratio=0.1), run_time=1.8)
        lg = lungs(mp, 1.12)
        trach = CubicBezier(mp(-4.8, 0.0), mp(-4.0, 0.9), mp(-3.0, 1.0), mp(-1.77, 0.9)).set_stroke(RED, 4)
        self.at("pumped air", lead=0.0)
        self.play(FadeIn(lg), Create(trach), run_time=1.0)
        air = dots(4, RED, 0.08)
        for i, a in enumerate(air):
            on_path(a, trach, 1.6, off=i / 4)
        self.add(air)
        blue = dots(14, BLUE, 0.1)
        for i, d in enumerate(blue):
            on_path(d, chs[i % len(chs)], 2.6 + 0.2 * (i % 3), off=(i * 0.31) % 1)
        self.at("pumped blood", lead=0.0)
        self.play(FadeIn(blue), run_time=0.6)
        al = T("air", 32, RED).move_to(mp(-4.4, 1.9))
        bl = T("blood", 32, RED).move_to([4.8, -3.1, 0])
        self.add(al, bl)
        self.at("carry")
        bo = T("oxygen rides in the flow", 32, BLUE).move_to([-1.2, -3.1, 0])
        self.play(FadeIn(bo), run_time=0.5)
        self.finish()


class S16Last(SpokenScene):
    def construct(self):
        ves = Rectangle(width=12.8, height=1.6, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.15).move_to([0, 2.0, 0])
        cells = VGroup()
        for r in range(3):
            for c in range(7):
                cells.add(RoundedRectangle(corner_radius=0.12, width=1.6, height=0.85, stroke_color=GREY, stroke_width=3,
                                           fill_color=LOW, fill_opacity=1).move_to([-5.4 + c * 1.8, 0.25 - r * 1.0, 0]))
        self.play(FadeIn(ves), FadeIn(cells), run_time=0.8)
        stream = dots(10, RED, 0.07)
        for i, d in enumerate(stream):
            sweep(d, [-6.4, 1.5 + 0.25 * (i % 4), 0], [6.4, 1.5 + 0.25 * (i % 4), 0], 3.5, off=i / 10, fade=0.02)
        self.add(stream)
        bl = T("bulk flow", 34, RED).move_to([0, 3.3, 0])
        self.play(FadeIn(bl), run_time=0.5)
        riders = dots(6, BLUE, 0.1)
        for i, d in enumerate(riders):
            sweep(d, [-6.4, 2.0, 0], [6.4, 2.0, 0], 3.5, off=i / 6 + 0.05, fade=0.02)
        self.add(riders)
        self.at("but it does not")
        outs = dots(10, BLUE, 0.1)
        for i, d in enumerate(outs):
            d.ph = 0
            d.rng = np.random.default_rng(30 + i)
            d.clock = i * 0.7
            d.x0 = -5.5 + i * 1.2
            d.move_to([d.x0, 1.9, 0])

            def f(mob, dt):
                mob.clock += dt
                t = mob.clock % 4.5
                if t < 1.0:
                    mob.move_to([mob.x0 + t * 1.2, 1.9, 0])
                    mob.set_opacity(1)
                else:
                    if t - dt < 1.0:
                        mob.pos = np.array([mob.x0 + 1.2, 1.2, 0])
                    mob.pos = mob.pos + np.array([mob.rng.normal() * 1.2 * np.sqrt(dt), -0.45 * dt + mob.rng.normal() * 0.9 * np.sqrt(dt), 0])
                    mob.pos[0] = min(max(mob.pos[0], -6.2), 6.2)
                    mob.pos[1] = min(mob.pos[1], 1.1)
                    mob.move_to(mob.pos)
                    mob.set_opacity(min(1, (4.5 - t) / 0.6))
            d.pos = np.array([d.x0, 1.2, 0])
            d.add_updater(f)
        self.add(outs)
        dl = T("last few \u00b5m: diffusion", 34, BLUE).move_to([0, -2.9, 0])
        self.at("diffusion still")
        self.play(FadeIn(dl), run_time=0.6)
        wl = T("thin walls", 30, TEXT).move_to([4.6, -2.9, 0])
        self.at("thin walls", lead=0.0)
        self.play(FadeIn(wl), run_time=0.5)
        self.finish()


class S17Rule(SpokenScene):
    def construct(self):
        s_ = cell(np.array([-5.4, 2.3, 0]), 0.55, (1, 1, 1))
        b_ = cube_n(np.array([-3.7, 2.3, 0]), 0.55, 2)
        shimmer(s_)
        shimmer(b_)
        cl = T("surface \u00d7 4, volume \u00d7 8", 28, TEXT).move_to([-4.0, 0.9, 0])
        self.play(FadeIn(s_), FadeIn(b_), FadeIn(cl), run_time=0.8)
        cap = T("same shape, fed from outside", 30, TEXT).move_to([0, 0.15, 0])
        self.at("same shape")
        self.play(FadeIn(cap), run_time=0.6)
        tr = ValueTracker(0)
        gg = gauge([1.3, 2.4, 0], 0.8, tr, BLUE)
        st = T("2 \u00d7 distance", 30, TEXT).move_to([4.5, 2.8, 0])
        st2 = T("= 4 \u00d7 time", 30, YELLOW).move_to([4.5, 2.1, 0])
        self.at("longer path", lead=0.3)
        self.play(FadeIn(gg), FadeIn(st), run_time=0.5)
        self.play(tr.animate.set_value(1.0), FadeIn(st2), run_time=1.5, rate_func=linear)
        # bottom row
        pl = planarian(3.6, GOLD)
        pl.body.set_stroke(GOLD, 5)
        pl.move_to([-4.5, -1.3, 0])
        glide(pl, 0.2, 0.05, 4.0)
        l1 = T("stay thin", 30, TEXT).move_to([-4.5, -3.1, 0])
        self.at("stay thin", lead=0.1)
        self.play(FadeIn(pl), FadeIn(l1), run_time=0.7)
        box = RoundedRectangle(corner_radius=0.15, width=3.3, height=2.1, stroke_color=TEXT, stroke_width=3).move_to([0, -1.3, 0])
        zz = VMobject(stroke_color=GOLD, stroke_width=6)
        pts = []
        for i in range(13):
            pts.append([-1.4 + i * 0.233, -1.3 + (0.8 if i % 2 == 0 else -0.8), 0])
        zz.set_points_as_corners(pts)
        l2 = T("add inner surface", 30, TEXT).move_to([0, -3.1, 0])
        fd = dots(5, BLUE, 0.07)
        for i, d in enumerate(fd):
            brown(d, (-1.4, 1.4, -2.2, -0.4), 1.2, 40 + i)
            d.move_to([-1.0 + 0.5 * i, -1.3, 0])
        self.at("add inner", lead=0.1)
        self.play(FadeIn(box), Create(zz), FadeIn(l2), run_time=0.9)
        self.add(fd)
        mm, mmp = mouse([4.4, -1.3, 0], 0.36)
        hp = mmp(-1.75, -0.35)
        ht = heart_shape(0.36, hp)
        beat(ht, 0.9)
        chs = channels(mmp, hp)
        for c in chs:
            c.set_stroke(RED, 2)
        l3 = T("pump fluid", 30, TEXT).move_to([4.5, -3.1, 0])
        self.at("pump fluid", lead=0.3)
        self.play(FadeIn(mm), FadeIn(ht), FadeIn(l3), run_time=0.6)
        self.play(LaggedStart(*[Create(c) for c in chs], lag_ratio=0.1), run_time=1.0)
        bd = dots(8, BLUE, 0.05)
        for i, d in enumerate(bd):
            on_path(d, chs[i % len(chs)], 2.2, off=(i * 0.3) % 1)
        self.add(bd)
        self.at("bulk flow", lead=0.1)
        sr = SurroundingRectangle(VGroup(mm, l3), color=RED, buff=0.15, stroke_width=4)
        self.play(Create(sr), run_time=0.6)
        self.finish()


class S18End(EndCard):
    LINE = "Same shape, bigger body, longer path: stay thin, add surface, or pump."
