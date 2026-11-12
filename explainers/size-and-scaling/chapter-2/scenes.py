"""Does Every Gram Cost the Same? (chapter 2 of the size-and-scaling pair; chapter 1 is ../scenes.py).

COLOUR MAP (carried from chapter 1): skin/surface GOLD; oxygen BLUE; pumped fluid RED; animals = light outlines.
New in this chapter: heat/energy burned ORANGE; exponent lines b = 1 GREY dashed, b = 3/4 TEAL, b = 2/3 PURPLE.
Every curve is computed from 70 kg -> 1,690 kcal/day on b = 3/4 (a = 69.8 kcal/day per kg^0.75); dogs are a
same-shape model. Anything not computed is labelled schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

HEAT = "#F28C28"
PURPLE = "#B084F0"
PALE = "#CFD8E8"
A_COEF = 69.8
LA = float(np.log10(A_COEF))


def mix(c, k, base=None):
    return interpolate_color(ManimColor(base or BG), ManimColor(c), float(min(max(k, 0), 1)))


# ------------------------------------------------------------------ motion helpers (as in chapter 1)
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


def breathe(m, period=2.6, amp=0.03, seed=0.0):
    m._bt = seed
    m._bs = 1.0

    def f(mob, dt):
        mob._bt += dt
        s = 1 + amp * np.sin(2 * np.pi * mob._bt / period)
        mob.stretch(s / mob._bs, 1, about_point=mob.get_bottom())
        mob._bs = s
    m.add_updater(f)
    return m


def flicker(m, amp=0.12, seed=0.0):
    m._ft = seed
    m._fs = 1.0

    def f(mob, dt):
        mob._ft += dt
        s = 1 + amp * np.sin(7 * mob._ft) * np.sin(3.1 * mob._ft + 1)
        mob.stretch(s / mob._fs, 1, about_point=mob.get_bottom())
        mob._fs = s
    m.add_updater(f)
    return m


def dots(n, color=BLUE, r=0.1):
    return VGroup(*[Dot(radius=r, color=color) for _ in range(n)])


def wisps(x, y0, n=3, h=1.1, spread=0.35, seed=0, color=HEAT, period=2.6, r=0.08):
    g = VGroup()
    rng = np.random.default_rng(seed)
    for i in range(n):
        dx = (i - (n - 1) / 2) * spread
        d = Dot(radius=r, color=color)
        sweep(d, [x + dx, y0, 0], [x + dx + rng.normal() * 0.1, y0 + h, 0], period, off=(i / n + 0.13 * seed) % 1)
        d.move_to([x + dx, y0, 0])
        g.add(d)
    return g


def stream(p0, p1, n, color=HEAT, r=0.14, period=3.2):
    g = VGroup()
    for i in range(n):
        d = Dot(radius=r, color=color)
        sweep(d, p0, p1, period, off=i / n, fade=0.08)
        d.move_to(p0)
        g.add(d)
    return g


def gauge(center, r, tr, color=BLUE, ring_color=TEXT):
    center = np.array(center, float)
    ring = Circle(r, stroke_color=ring_color, stroke_width=4).move_to(center)
    knob = Rectangle(width=0.3, height=0.16, stroke_width=0, fill_color=ring_color, fill_opacity=1).move_to(center + UP * (r + 0.1))

    def sec():
        v = tr.get_value()
        return Sector(radius=r * 0.9, angle=-2 * PI * max(v, 0.003), start_angle=PI / 2, arc_center=center,
                      fill_color=color, fill_opacity=0.7, stroke_width=0)
    return VGroup(ring, knob, always_redraw(sec))


def heart_shape(size, center, color=RED):
    f = lambda t: np.array([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0])
    h = ParametricFunction(f, t_range=[0, 2 * PI], stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=1)
    h.set_height(size)
    h.move_to(center)
    return h


def mouse(center=ORIGIN, s=1.0, color=TEXT):
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


# ------------------------------------------------------------------ new objects
def flame(h=0.6, color=HEAT):
    pts = [(0, -0.5), (0.32, -0.2), (0.28, 0.12), (0.08, 0.4), (0.12, 0.62), (-0.12, 0.3), (-0.3, 0.05), (-0.28, -0.22)]
    pts = [np.array([x, y, 0]) for x, y in pts]
    outer = VMobject(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.85)
    outer.set_points_smoothly(pts + [pts[0]])
    inner = outer.copy().set_fill(YELLOW, 0.9).set_stroke(YELLOW, 0).scale(0.5, about_point=outer.get_bottom())
    g = VGroup(outer, inner)
    g.set_height(h)
    return g


def human(height=2.2, color=TEXT):
    head = Circle(0.3).move_to([0, 1.55, 0])
    torso = RoundedRectangle(corner_radius=0.25, width=0.7, height=1.1).move_to([0, 0.8, 0])
    arms = [Rectangle(width=0.16, height=0.85).move_to([s * 0.5, 0.82, 0]) for s in (-1, 1)]
    legs = [Rectangle(width=0.24, height=0.95).move_to([s * 0.17, -0.05, 0]) for s in (-1, 1)]
    sil = Union(head, torso, *arms, *legs).set_stroke(color, 4).set_fill(color, 0.07)
    sil.set_height(height)
    return sil


def dog(w, cx, base, color=TEXT):
    body = Ellipse(width=1.7, height=0.85).move_to([0, 0.15, 0])
    head = Circle(0.36).move_to([1.0, 0.62, 0])
    snout = Ellipse(width=0.6, height=0.3).move_to([1.42, 0.52, 0])
    ear = Ellipse(width=0.24, height=0.5).move_to([0.82, 0.92, 0])
    legs = [Rectangle(width=0.2, height=0.7).move_to([x, -0.4, 0]) for x in (-0.55, -0.3, 0.45, 0.7)]
    sil = Union(body, head, snout, ear, *legs).set_stroke(color, 4).set_fill(color, 0.22)
    tail = ArcBetweenPoints(np.array([-0.82, 0.35, 0]), np.array([-1.3, 0.95, 0]), angle=-0.9).set_stroke(color, 4)
    eye = Dot([1.1, 0.7, 0], radius=0.05, color=color)
    g = VGroup(sil, tail, eye)
    g.set_width(w)
    g.move_to([cx, 0, 0])
    g.shift(DOWN * (g.get_bottom()[1] - base))
    return g


def hbar(cx, h, base=-0.1, w=0.75, color=HEAT):
    return Rectangle(width=w, height=max(h, 0.01), stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=0.55).move_to([cx, base + max(h, 0.01) / 2, 0])


def vbracket(x, y0, y1, color=GOLD):
    return VGroup(Line([x, y0, 0], [x, y1, 0]), Line([x - 0.12, y0, 0], [x + 0.12, y0, 0]),
                  Line([x - 0.12, y1, 0], [x + 0.12, y1, 0])).set_stroke(color, 4)


# dogs: same-shape model, masses M, 3M, 10M, 30M; width ~ mass^(1/3)
MASSES = [1, 3, 10, 30]
WID = [1.3 * m ** (1 / 3) for m in MASSES]
BASE = -2.55
U = 0.22   # bar height per unit of heat (model: heat = M^0.75)


def _centers():
    left, cs = -5.9, []
    for w in WID:
        cs.append(left + w / 2)
        left += w + 0.55
    return cs


CS = _centers()


def dog_row(idx=(0, 1, 2, 3)):
    return [dog(WID[i], CS[i], BASE) for i in idx]


def dog_wisps(d, seed=0):
    return wisps(d.get_center()[0], d.get_top()[1] + 0.15, 5, 2.3, 0.3, seed, r=0.11, period=3.0)


# ------------------------------------------------------------------ log-log plot (one world for s09-s16)
def PX(x, y):
    return np.array([-4.9 + (x + 2) * 1.2, -2.9 + y * 1.2, 0])


def axes_group():
    ax = VGroup(Line(PX(-2, 0), PX(3, 0)), Line(PX(-2, 0), PX(-2, 4.4))).set_stroke(TEXT, 3)
    xl = T("log mass", 28, TEXT).move_to([-1.9, -3.4, 0])
    yl = T("log metabolic rate", 28, TEXT).rotate(PI / 2).move_to([-5.65, -0.3, 0])
    return ax, xl, yl


SPECIES = [("rat", 0.3, 0.03), ("cat", 3, -0.04), ("dog", 12, 0.03), ("sheep", 50, -0.03), ("human", 70, 0.02), ("steer", 600, 0.0)]


def sp_pt(i):
    n, m, e = SPECIES[i]
    x = np.log10(m)
    return x, LA + 0.75 * x + e


def fit_line(color=TEAL, x0=-0.8, x1=2.9, w=8):
    return Line(PX(x0, LA + 0.75 * x0), PX(x1, LA + 0.75 * x1)).set_stroke(color, w)


PIV = (0.7, 2.1)


def pline(b, color, x0=-1.4, x1=2.8, dashed=False, w=8):
    p, q = PX(x0, PIV[1] + b * (x0 - PIV[0])), PX(x1, PIV[1] + b * (x1 - PIV[0]))
    if dashed:
        return DashedLine(p, q, dash_length=0.2).set_stroke(color, w)
    return Line(p, q).set_stroke(color, w)


def legend_row(y, color, text, dashed=False, x0=2.2):
    ln = DashedLine([x0, y, 0], [x0 + 0.9, y, 0], dash_length=0.15) if dashed else Line([x0, y, 0], [x0 + 0.9, y, 0])
    ln.set_stroke(color, 6)
    tx = M(text, 34, color)
    tx.move_to([x0 + 1.1 + tx.width / 2, y, 0])
    return VGroup(ln, tx)


def kdot(p, color=HEAT, r=0.17):
    return Dot(p, radius=r, color=color)


def line_stream(b, n=10, x0=-1.4, x1=2.8, pv=None, color=HEAT, period=3.4):
    if pv is None:
        a = lambda x: PIV[1] + b * (x - PIV[0])
    else:
        a = lambda x: LA + b * x
    return stream(PX(x0, a(x0)), PX(x1, a(x1)), n, color, 0.14, period)


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Size, Scale and Surface"
    TITLE = "Does Every Gram Cost the Same?"


class S01Hook(SpokenScene):
    def construct(self):
        P0 = np.array([0, 1.4, 0])
        L, HANG = 4.0, 3.0
        tilt = ValueTracker(0)

        def ends():
            t = tilt.get_value()
            return P0 + L * np.array([-np.cos(t), np.sin(t), 0]), P0 + L * np.array([np.cos(t), -np.sin(t), 0])

        beam = always_redraw(lambda: Line(*ends()).set_stroke(TEXT, 10))

        def pan(side):
            def f():
                e = ends()[side]
                bot = e + DOWN * HANG
                a = Line(e, bot + LEFT * 1.0).set_stroke(TEXT, 3)
                b = Line(e, bot + RIGHT * 1.0).set_stroke(TEXT, 3)
                c = Line(bot + LEFT * 1.1, bot + RIGHT * 1.1).set_stroke(TEXT, 8)
                return VGroup(a, b, c)
            return always_redraw(f)

        post = Polygon([0, 1.4, 0], [-0.7, -3.3, 0], [0.7, -3.3, 0], stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12)
        pivot = Dot(P0, radius=0.14, color=TEXT)
        mo, _ = mouse(ORIGIN, 0.2)
        hu = human(2.2)

        def follow(item, side):
            def f(mob, dt):
                bot = ends()[side] + DOWN * HANG
                mob.move_to([bot[0], bot[1] + 0.06 + mob.height / 2, 0])
            item.add_updater(f)
            f(item, 0)
        follow(mo, 0)
        follow(hu, 1)
        self.add(post, beam, pivot, pan(0), pan(1))
        sway = Mobject()

        def swayf(mob, dt):
            if self.elapsed() > 2.8:
                tilt.set_value(0.2 + 0.018 * np.sin(2.2 * (self.elapsed() - 2.8)))
        sway.add_updater(swayf)
        self.play(FadeIn(post), FadeIn(pivot), FadeIn(mo), FadeIn(hu), run_time=0.9)
        self.at("heavier", lead=0.3)
        self.play(tilt.animate.set_value(0.2), run_time=1.0, rate_func=rush_into)
        self.add(sway)
        mass = M("mass × 2,333", 44, YELLOW).move_to([0, 3.15, 0])
        self.at("than a mouse")
        self.play(FadeIn(mass, shift=DOWN * 0.2), run_time=0.6)
        fm = flame(0.8).move_to([-5.75, -0.45, 0])
        fh = flame(1.9).move_to([5.75, -1.3, 0])
        flicker(fm, 0.22, 0.0)
        flicker(fh, 0.2, 1.3)
        self.at("Does the human")
        self.play(FadeIn(fm, scale=0.6), FadeIn(fh, scale=0.6), run_time=0.8)
        q = T("?", 110, YELLOW, font=TITLE_FONT).move_to([5.75, 0.75, 0])
        pulse(q, 1.0, 0.15)
        self.at("times as much")
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.at("every day")
        tg = T("per day", 30, HEAT).move_to([5.75, -2.9, 0])
        self.play(FadeIn(tg), run_time=0.5)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        m, mp = mouse([0.0, -0.1, 0], 1.12)
        hpos = mp(-1.75, -0.35)
        ht = heart_shape(0.8, hpos)
        beat(ht, 0.9)
        self.play(FadeIn(m), run_time=0.7)
        self.play(FadeIn(ht), run_time=0.4)
        chs = channels(mp, hpos)
        self.at("pumps blood", lead=0.4)
        self.play(LaggedStart(*[Create(c) for c in chs], lag_ratio=0.1), run_time=1.6)
        blue = dots(14, BLUE, 0.1)
        for i, d in enumerate(blue):
            on_path(d, chs[i % len(chs)], 2.6 + 0.2 * (i % 3), off=(i * 0.31) % 1)
        self.add(blue)
        lg = lungs(mp, 1.12)
        trach = CubicBezier(mp(-4.8, 0.0), mp(-4.0, 0.9), mp(-3.0, 1.0), mp(-1.77, 0.9)).set_stroke(RED, 4)
        self.at("and air")
        self.play(FadeIn(lg), Create(trach), run_time=0.9)
        air = dots(4, RED, 0.08)
        for i, a in enumerate(air):
            on_path(a, trach, 1.6, off=i / 4)
        self.add(air)
        f1 = flame(0.62).move_to(mp(0.9, -0.05))
        f2 = flame(0.62).move_to(mp(2.9, -0.2))
        flicker(f1, 0.12, 0.2)
        flicker(f2, 0.12, 1.1)
        self.at("That flow")
        self.play(FadeIn(f1, scale=0.5), FadeIn(f2, scale=0.5), run_time=0.8)
        lab = T("supply must match use", 36, TEXT).move_to([0, -3.3, 0])
        self.at("deliver")
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.6)
        hm = T("how much?", 44, YELLOW).move_to([0, 3.2, 0])
        self.at("how much")
        self.play(FadeIn(hm, scale=1.2), run_time=0.5)
        self.finish()


class S03Rubner(SpokenScene):
    def construct(self):
        cap = T("Max Rubner, 1883", 42, TEXT).move_to([0, 3.2, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.15), run_time=0.8)
        ds = dog_row()
        for i, d in enumerate(ds):
            breathe(d, 2.6, 0.03, seed=i * 0.7)
        self.at("asked")
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.3) for d in ds], lag_ratio=0.25), run_time=1.8)
        ws = VGroup(*[dog_wisps(d, i) for i, d in enumerate(ds)])
        self.add(ws)
        q = T("cost per gram: the same?", 40, YELLOW).move_to([0, 3.2, 0])
        self.at("Does every")
        self.play(ReplacementTransform(cap, q), run_time=0.8)
        lab = T("resting dogs", 34, TEXT).move_to([0, -3.3, 0])
        self.at("resting")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.6)
        self.at("many sizes", lead=0.1)
        self.play(LaggedStart(*[Indicate(d, scale_factor=1.08, color=TEXT) for d in ds], lag_ratio=0.3), run_time=1.6)
        self.finish()


class S04Dogs(SpokenScene):
    def construct(self):
        ds = dog_row()
        for i, d in enumerate(ds):
            breathe(d, 2.6, 0.03, seed=i * 0.7)
        ws = VGroup(*[dog_wisps(d, i) for i, d in enumerate(ds)])
        self.add(*ds, ws)
        one = T("one species: dogs", 40, TEXT).move_to([0, 3.2, 0])
        self.at("One species")
        self.play(FadeIn(one, shift=DOWN * 0.15), run_time=0.6)
        ax = Arrow([-6.2, -2.95, 0], [6.4, -2.95, 0], buff=0, color=TEXT, stroke_width=4, max_tip_length_to_length_ratio=0.04)
        ticks = VGroup(*[Dot([c, -2.95, 0], radius=0.07, color=TEXT) for c in CS])
        bm = T("body mass", 28, TEXT).move_to([5.3, -3.4, 0])
        self.at("wide range")
        self.play(Create(ax), FadeIn(ticks), run_time=1.4)
        self.play(FadeIn(bm), run_time=0.4)
        self.at("size can change")
        self.play(LaggedStart(*[Indicate(d, scale_factor=1.1, color=TEXT) for d in ds], lag_ratio=0.3), run_time=1.8)
        md = T("same-shape model, not the actual dogs", 28, GOLD).move_to([-1.9, -3.5, 0])
        self.at("without changing")
        self.play(FadeIn(md, shift=UP * 0.1), run_time=0.6)
        self.finish()


def predict_world(scene, card=True, timer=False):
    d0, d2 = dog_row((0, 2))
    breathe(d0, 2.6, 0.03)
    breathe(d2, 2.6, 0.03, seed=1.0)
    l0 = M("M", 36, TEXT).move_to([CS[0], -3.0, 0])
    l2 = M("10 M", 36, TEXT).move_to([CS[2], -3.0, 0])
    b0 = hbar(CS[0], U)
    hl = T("heat", 32, HEAT).move_to([CS[0], -0.6, 0])
    dash = DashedVMobject(Rectangle(width=0.75, height=10 * U, stroke_color=HEAT, stroke_width=3).move_to([CS[2], -0.1 + 5 * U, 0]), num_dashes=40)
    x10 = M("10 ×", 36, HEAT).move_to([CS[2] + 1.35, -0.1 + 10 * U, 0])
    cardm = None
    if card:
        t = T("10 × the heat?", 40, YELLOW)
        bx = RoundedRectangle(corner_radius=0.15, width=t.width + 0.7, height=t.height + 0.5, stroke_color=YELLOW, stroke_width=3)
        cardm = VGroup(bx, t).move_to([0, 3.25, 0])
        pulse(t, 1.2, 0.08)
    return dict(d0=d0, d2=d2, l0=l0, l2=l2, b0=b0, hl=hl, dash=dash, x10=x10, card=cardm)


class S05Predict(SpokenScene):
    def construct(self):
        ds = dog_row()
        for i, d in enumerate(ds):
            breathe(d, 2.6, 0.03, seed=i * 0.7)
        ws = VGroup(*[dog_wisps(d, i) for i, d in enumerate(ds)])
        self.add(*ds, ws)
        w = predict_world(self)
        self.play(FadeOut(ds[1]), FadeOut(ds[3]), FadeOut(ws[1]), FadeOut(ws[3]), run_time=0.9)
        self.at("one dog")
        self.play(FadeIn(w["l0"]), ds[0].animate.set_stroke(TEXT, 7), run_time=0.5)
        self.at("ten times", lead=0.3)
        self.play(FadeIn(w["l2"]), ds[2].animate.set_stroke(TEXT, 7), run_time=0.5)
        self.at("every gram", lead=0.3)
        self.play(FadeOut(ws[0]), FadeOut(ws[2]), GrowFromEdge(w["b0"], DOWN), FadeIn(w["hl"]), run_time=0.9)
        self.at("ten times the heat", lead=0.0)
        self.play(Create(w["dash"]), FadeIn(w["x10"]), run_time=1.6)
        self.at("Does it")
        self.play(FadeIn(w["card"], scale=1.1), run_time=0.6)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        w = predict_world(self)
        d0, d2 = w["d0"], w["d2"]
        d0.set_stroke(TEXT, 7)
        d2.set_stroke(TEXT, 7)
        self.add(d0, d2, w["l0"], w["l2"], w["b0"], w["hl"], w["dash"], w["x10"], w["card"])
        ws = VGroup(wisps(CS[0], -0.1 + U, 3, 1.4, 0.3, 4, r=0.11), wisps(CS[2], -0.1, 5, 1.9, 0.3, 5, r=0.11))
        self.add(ws)
        tr = ValueTracker(1)
        ring = gauge([6.0, -3.0, 0], 0.5, tr, YELLOW)
        self.add(ring)
        self.play(tr.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        w = predict_world(self)
        d0, d2 = w["d0"], w["d2"]
        d0.set_stroke(TEXT, 7)
        d2.set_stroke(TEXT, 7)
        self.add(d0, d2, w["l0"], w["l2"], w["b0"], w["hl"], w["dash"], w["x10"], w["card"])
        self.play(FadeOut(w["card"]), run_time=0.6)
        b2 = hbar(CS[2], 10 ** 0.75 * U)
        self.at("total heat", lead=0.3)
        self.play(GrowFromEdge(b2, DOWN), w["x10"].animate.set_opacity(0.55), run_time=1.6)
        x56 = M("≈ 5.6 ×", 36, HEAT).move_to([CS[2] - 1.7, -0.1 + 10 ** 0.75 * U * 0.6, 0])
        self.at("much less steeply")
        self.play(FadeIn(x56, scale=1.2), run_time=0.6)
        ws = VGroup(wisps(CS[2], -0.1 + 10 ** 0.75 * U, 4, 1.0, 0.3, 6, r=0.11), wisps(CS[0], -0.1 + U, 3, 1.0, 0.3, 7, r=0.11))
        self.add(ws)
        # per-kilogram panel
        pt = T("heat per kg", 32, HEAT).move_to([4.4, 2.55, 0])
        h0, h2 = 2.2, 2.2 * 10 ** -0.25
        pb0 = hbar(3.5, h0, w=0.9)
        pb2 = hbar(5.3, h2, w=0.9)
        pl0 = M("M", 30, TEXT).move_to([3.5, -0.5, 0])
        pl2 = M("10 M", 30, TEXT).move_to([5.3, -0.5, 0])
        self.at("Each kilogram")
        self.play(FadeIn(pt), FadeIn(pl0), FadeIn(pl2), GrowFromEdge(pb0, DOWN), GrowFromEdge(pb2, DOWN), run_time=1.6)
        self.at("small dog")
        self.play(Indicate(pb0, color=HEAT, scale_factor=1.06), run_time=1.0)
        self.at("big one", lead=0.3)
        self.play(Indicate(pb2, color=HEAT, scale_factor=1.06), run_time=1.0)
        self.finish()


class S08Skin(SpokenScene):
    def construct(self):
        ds = dog_row()
        for i, d in enumerate(ds):
            breathe(d, 2.6, 0.03, seed=i * 0.7)
        k = ValueTracker(0)
        tot = [U * m ** 0.75 for m in MASSES]
        per = [1.9 * (m / 30) ** (1 / 12) for m in MASSES]
        bars = VGroup(*[always_redraw(lambda i=i: hbar(CS[i], tot[i] + (per[i] - tot[i]) * k.get_value())) for i in range(4)])
        cap1 = T("total heat", 36, HEAT).move_to([0, 3.25, 0])
        self.add(*ds)
        self.play(FadeIn(bars), FadeIn(cap1), run_time=0.7)
        self.at("body surface", lead=0.6)
        gl = ValueTracker(0)

        def glow(d):
            def f(mob, dt):
                gl.set_value(gl.get_value() + dt)
                mob.set_stroke(GOLD, 6 + 2.5 * np.sin(3 * gl.get_value()))
            d[0].add_updater(f)
        self.play(*[d[0].animate.set_stroke(GOLD, 7) for d in ds], run_time=0.8)
        for d in ds:
            d[1].set_stroke(GOLD, 6)
        glow(ds[0])
        sl = T("estimated body surface", 34, GOLD).move_to([0, -3.4, 0])
        self.play(FadeIn(sl), run_time=0.5)
        cap2 = T("heat per surface: roughly constant", 36, HEAT).move_to([0, 3.25, 0])
        self.at("values", lead=0.4)
        self.play(k.animate.set_value(1.0), ReplacementTransform(cap1, cap2), run_time=2.2)
        nt = T("a pattern, not proof of cause", 30, TEXT).move_to([0, -3.4, 0])
        self.at("Heat tracked", lead=0.3)
        self.play(ReplacementTransform(sl, nt), run_time=0.7)
        self.play(*[Indicate(d, scale_factor=1.06, color=GOLD) for d in ds[::1]], run_time=1.4)
        self.finish()


def pts_group(n=len(SPECIES)):
    return VGroup(*[kdot(PX(*sp_pt(i))) for i in range(n)])


class S09Kleiber(SpokenScene):
    def construct(self):
        cap = T("Max Kleiber, 1932", 38, TEXT).move_to([4.3, 2.5, 0])
        sub = T("resting rate vs body mass", 30, TEXT).move_to([4.3, 1.7, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.15), run_time=0.8)
        ax, xl, yl = axes_group()
        self.at("gathered", lead=0.4)
        self.play(Create(ax), FadeIn(sub), run_time=1.2)
        pts = VGroup(*[kdot(PX(*sp_pt(i))) for i in range(len(SPECIES))])
        targets = [p.get_center().copy() for p in pts]
        for p in pts:
            p.shift(UP * 3.2).set_opacity(0)
        for p in pts:
            beat(p, 1.6, 0.5)
        self.add(pts)
        self.at("rats")
        self.play(LaggedStart(*[p.animate.move_to(t).set_opacity(1) for p, t in zip(pts, targets)], lag_ratio=0.22), run_time=3.0)
        rl = T("rat", 28, TEXT).move_to(PX(*sp_pt(0)) + np.array([-0.45, 0.5, 0]))
        sl = T("steer", 28, TEXT).move_to(PX(*sp_pt(5)) + np.array([-0.7, 0.35, 0]))
        self.play(FadeIn(rl), FadeIn(sl), run_time=0.5)
        sc = T("schematic points", 26, TEXT).move_to([4.3, -3.3, 0])
        self.at("logarithmic")
        self.play(FadeIn(xl), FadeIn(yl), FadeIn(sc), run_time=0.9)
        pw = T("a power law becomes\na straight line", 32, TEXT).move_to([4.3, 0.2, 0])
        self.at("power law")
        self.play(FadeIn(pw, shift=UP * 0.1), run_time=0.6)
        ln = fit_line()
        self.at("straight line", lead=0.9)
        self.play(Create(ln), run_time=1.4)
        self.add(line_stream(0.75, 10, -0.8, 2.9, pv=1))
        self.finish()


class S10Law(SpokenScene):
    def construct(self):
        ax, xl, yl = axes_group()
        pts = pts_group()
        ln = fit_line()
        sc = T("schematic points", 26, TEXT).move_to([4.3, -3.3, 0])
        self.add(ax, xl, yl, pts, ln, sc, line_stream(0.75, 10, -0.8, 2.9, pv=1))
        l1 = M("metabolic rate", 32, TEXT).move_to([4.3, 2.3, 0])
        Mm = M("M", 44, TEXT).move_to([5.0, 1.3, 0])
        A = M("= a ×", 44, TEXT)
        A.next_to(Mm, LEFT, buff=0.15)
        bb = M("b", 30, TEXT).next_to(Mm, UR, buff=0.02).shift(DOWN * 0.12)
        self.play(Write(l1), run_time=1.0)
        self.at("equals", lead=0.1)
        self.play(Write(A), run_time=0.9)
        self.at("called a", lead=0.0)
        self.play(Indicate(A[2], color=YELLOW, scale_factor=1.4), run_time=0.9)
        self.at("body mass", lead=0.1)
        self.play(Write(Mm), run_time=0.7)
        self.at("raised to")
        self.play(FadeIn(bb, shift=UP * 0.1), run_time=0.6)
        self.at("called b", lead=0.0)
        self.play(Indicate(bb, color=YELLOW, scale_factor=1.6), run_time=0.9)
        p1, p2, p3 = PX(1, LA + 0.75), PX(2, LA + 0.75), PX(2, LA + 1.5)
        tri = Polygon(p1, p2, p3, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.15)
        sl = T("slope = b", 34, YELLOW).move_to([1.35, PX(2, LA + 1.1)[1], 0])
        self.at("these axes")
        self.play(Create(tri), run_time=1.0)
        self.at("slope of the line", lead=0.2)
        self.play(FadeIn(sl, shift=LEFT * 0.1), run_time=0.6)
        self.finish()


class S11Lines(SpokenScene):
    def construct(self):
        ax, xl, yl = axes_group()
        pts = pts_group()
        ln0 = fit_line()
        self.add(ax, xl, yl, pts, ln0)
        pvd = Dot(PX(*PIV), radius=0.14, color=YELLOW)
        self.play(FadeOut(pts), FadeOut(ln0), FadeIn(pvd), run_time=0.8)
        l1 = pline(1.0, GREY, dashed=True)
        r1 = legend_row(2.1, GREY, "b = 1", dashed=True)
        n1 = T("every kg costs the same", 26, TEXT).move_to([4.4, 1.55, 0])
        n1.align_to([2.2, 0, 0], LEFT)
        self.at("If B were")
        self.play(Create(l1), FadeIn(r1), run_time=1.3)
        self.add(line_stream(1.0, 8, color=GREY))
        self.at("every kilogram", lead=0.1)
        self.play(FadeIn(n1), run_time=0.5)
        l2 = pline(0.75, TEAL)
        r2 = legend_row(0.7, TEAL, "b = 3/4")
        n2 = T("Kleiber's line", 26, TEXT).move_to([3.4, 0.15, 0])
        n2.align_to([2.2, 0, 0], LEFT)
        self.at("line had", lead=0.5)
        self.play(Create(l2), FadeIn(r2), run_time=1.3)
        self.add(line_stream(0.75, 8, color=TEAL))
        self.play(FadeIn(n2), run_time=0.4)
        l3 = pline(2 / 3, PURPLE)
        r3 = legend_row(-0.5, PURPLE, "b = 2/3")
        n3 = T("Rubner's surface rule", 26, TEXT).move_to([4.2, -1.05, 0])
        n3.align_to([2.2, 0, 0], LEFT)
        self.at("surface rule", lead=0.6)
        self.play(Create(l3), FadeIn(r3), run_time=1.3)
        self.add(line_stream(2 / 3, 8, color=PURPLE))
        self.play(FadeIn(n3), run_time=0.4)
        sm = T("same a;\nslopes compared only", 28, YELLOW).move_to([4.3, -2.6, 0])
        self.play(FadeIn(sm), run_time=0.6)
        self.finish()


class S12Mousehuman(SpokenScene):
    def construct(self):
        ax, xl, yl = axes_group()
        ln = fit_line(x0=-1.8, x1=2.8)
        self.add(ax, xl, yl, ln, line_stream(0.75, 10, -1.8, 2.8, pv=1, color=YELLOW))
        tl = legend_row(2.0, TEAL, "b = 3/4", x0=2.2)
        self.play(FadeIn(tl), run_time=0.6)
        mx, my = np.log10(0.03), LA + 0.75 * np.log10(0.03)
        hx, hy = np.log10(70), LA + 0.75 * np.log10(70)
        mk = kdot(PX(mx, my), HEAT, 0.16)
        hk = kdot(PX(hx, hy), HEAT, 0.16)
        ml1 = T("mouse, 30 g", 26, TEXT).move_to([-2.2, -2.27, 0])
        ml2 = T("≈ 5 kcal per day", 26, HEAT).move_to([-2.2, -2.57, 0])
        hl1 = T("human, 70 kg", 28, TEXT).move_to([-2.2, 1.65, 0])
        hl2 = T("≈ 1,690 kcal per day", 28, HEAT).move_to([-2.2, 1.25, 0])
        self.at("a mouse")
        self.play(FadeIn(mk, scale=2.5), run_time=0.6)
        self.play(FadeIn(ml1), FadeIn(ml2), run_time=0.5)
        self.at("a human")
        self.play(FadeIn(hk, scale=2.5), run_time=0.6)
        self.play(FadeIn(hl1), FadeIn(hl2), run_time=0.5)
        g1 = DashedLine([-1.0, PX(mx, my)[1], 0], [1.75, PX(mx, my)[1], 0], dash_length=0.15).set_stroke(HEAT, 3)
        g2 = DashedLine(PX(hx, hy), [1.75, PX(hx, hy)[1], 0], dash_length=0.15).set_stroke(HEAT, 3)
        br = vbracket(1.75, PX(mx, my)[1], PX(hx, hy)[1], YELLOW)
        self.at("far more")
        self.play(Create(g1), Create(g2), run_time=1.0)
        self.play(Create(br), run_time=0.6)
        tt = M("total × ≈ 336", 34, YELLOW).move_to([4.35, (PX(mx, my)[1] + PX(hx, hy)[1]) / 2, 0])
        self.at("few hundred", lead=0.5)
        self.play(FadeIn(tt, shift=LEFT * 0.15), run_time=0.7)
        self.finish()


class S13Perkg(SpokenScene):
    def construct(self):
        ax, xl, yl = axes_group()
        ln = fit_line(x0=-1.8, x1=2.8)
        mx, my = np.log10(0.03), LA + 0.75 * np.log10(0.03)
        hx, hy = np.log10(70), LA + 0.75 * np.log10(70)
        mk, hk = kdot(PX(mx, my), HEAT, 0.16), kdot(PX(hx, hy), HEAT, 0.16)
        plot = VGroup(ax, xl, yl, ln, mk, hk)
        self.add(plot)
        dv = T("÷ body mass", 38, YELLOW).move_to([-2.0, 3.25, 0])
        self.play(plot.animate.set_opacity(0.3), FadeIn(dv), run_time=0.9)
        hm, hh = 4.4, 4.4 * (1690 / 70) / (5.03 / 0.03)
        base = -2.6
        title = T("kcal per kg per day", 28, TEXT).move_to([4.4, 3.3, 0])
        bm = Rectangle(width=1.1, height=hm, stroke_color=HEAT, stroke_width=3, fill_color=HEAT, fill_opacity=0.55).move_to([3.0, base + hm / 2, 0])
        bh = Rectangle(width=1.1, height=hh, stroke_color=HEAT, stroke_width=3, fill_color=HEAT, fill_opacity=0.55).move_to([5.6, base + hh / 2, 0])
        nm = T("mouse", 28, TEXT).move_to([3.0, -3.1, 0])
        nh = T("human", 28, TEXT).move_to([5.6, -3.1, 0])
        self.at("Each kilogram", lead=0.1)
        self.play(FadeIn(title), GrowFromEdge(bm, DOWN), GrowFromEdge(bh, DOWN), FadeIn(nm), FadeIn(nh), run_time=1.6)
        self.add(wisps(3.0, base + hm + 0.75, 5, 0.45, 0.16, 11, r=0.1, period=1.8), wisps(5.6, base + hh + 0.75, 1, 0.9, 0.14, 12, r=0.1, period=2.4))
        vm = M("≈ 168", 34, HEAT).move_to([3.0, base + hm + 0.4, 0])
        self.at("of mouse")
        self.play(FadeIn(vm, shift=UP * 0.1), run_time=0.5)
        x7 = M("about 7 ×", 34, YELLOW).move_to([5.1, 0.2, 0])
        self.at("about seven", lead=0.0)
        self.play(FadeIn(x7, scale=1.2), run_time=0.6)
        vh = M("≈ 24", 34, HEAT).move_to([5.6, base + hh + 0.4, 0])
        self.at("of human")
        self.play(FadeIn(vh, shift=UP * 0.1), Indicate(bh, color=HEAT, scale_factor=1.1), run_time=0.8)
        fp = T("a fitted prediction, not a measurement", 30, TEXT).move_to([-2.4, 3.25, 0])
        self.at("fitted prediction", lead=0.4)
        self.play(ReplacementTransform(dv, fp), run_time=0.7)
        self.play(Indicate(x7, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.finish()


def inset_curve(b, color):
    f = lambda x: np.array([2.5 + (x + 1.5) * (3.9 / 4.5), -2.3 + (A_COEF * 10 ** (x * (b - 1))) / 230 * 3.0, 0])
    return ParametricFunction(f, t_range=[-1.5, 3], stroke_color=color, stroke_width=6)


class S14Below1(SpokenScene):
    def construct(self):
        ax, xl, yl = axes_group()
        l1, l2, l3 = pline(1.0, GREY, dashed=True), pline(0.75, TEAL), pline(2 / 3, PURPLE)
        pvd = Dot(PX(*PIV), radius=0.14, color=YELLOW)
        r1 = legend_row(-0.9, GREY, "b = 1", dashed=True, x0=-1.5)
        r2 = legend_row(-1.6, TEAL, "b = 3/4", x0=-1.5)
        r3 = legend_row(-2.3, PURPLE, "b = 2/3", x0=-1.5)
        for r in (r1, r2, r3):
            r[0].set_stroke(width=5)
            r[1].scale(0.82, about_point=r[1].get_left())
        self.add(ax, xl, yl, l1, l2, l3, pvd, r1, r2, r3)
        self.add(line_stream(0.75, 8, color=TEAL), line_stream(2 / 3, 8, color=PURPLE, period=3.8))
        rng = M("0 < b < 1", 44, YELLOW).move_to([4.3, 2.4, 0])
        self.at("is positive", lead=0.3)
        self.play(FadeIn(rng, scale=1.2), run_time=0.7)
        self.at("below", lead=0.2)
        self.play(l1.animate.set_opacity(0.0), r1.animate.set_opacity(0.0), run_time=1.2)
        ixa = VGroup(Line([2.5, -2.3, 0], [6.4, -2.3, 0]), Line([2.5, -2.3, 0], [2.5, 0.7, 0])).set_stroke(TEXT, 3)
        yl2 = T("rate per kg", 26, TEXT).move_to([3.5, 1.0, 0])
        self.at("total rate rises", lead=0.2)
        self.play(Create(ixa), FadeIn(yl2), run_time=1.2)
        c2, c3 = inset_curve(0.75, TEAL), inset_curve(2 / 3, PURPLE)
        self.at("rate per kilogram", lead=0.3)
        self.play(Create(c2), Create(c3), run_time=1.6)
        cp = T("rate per kg falls\nas mass rises", 28, TEXT).move_to([4.5, -3.2, 0])
        self.play(FadeIn(cp), run_time=0.6)
        for c, col, off in ((c2, TEAL, 0), (c3, PURPLE, 0.4)):
            d = Dot(radius=0.13, color=col)
            on_path(d, c, 3.0, off=off)
            self.add(d)
        self.finish()


class S15Fit(SpokenScene):
    def construct(self):
        ax, xl, yl = axes_group()
        l2 = pline(0.75, TEAL)
        pvd = Dot(PX(*PIV), radius=0.14, color=YELLOW)
        self.add(ax, xl, yl, l2, pvd)
        self.add(line_stream(0.75, 10, color=TEAL))
        cap = T("a fit, not a law", 44, YELLOW, font=TITLE_FONT).move_to([4.3, 2.4, 0])
        self.at("fit", lead=0.5)
        self.play(FadeIn(cap, shift=DOWN * 0.15), run_time=0.8)
        l3 = pline(2 / 3, PURPLE)
        self.add(l3)
        l3.set_opacity(0)
        fans = [pline(b, TEXT, w=4).set_opacity(0.8) for b in (0.55, 0.6, 0.82, 0.9)]
        self.at("exponent changes", lead=0.4)
        self.play(l3.animate.set_opacity(1), LaggedStart(*[Create(f) for f in fans], lag_ratio=0.3), run_time=2.0)
        ex = T("examples, not bounds", 28, TEXT).move_to([4.3, -2.6, 0])
        self.play(FadeIn(ex), run_time=0.5)
        tags = [("which animals", 1.4, "animals"), ("rest or exercise", 0.6, "state"), ("which method", -0.2, "method")]
        for i, (txt, y, cue) in enumerate(tags):
            tg = T(txt, 32, TEXT).move_to([4.3, y, 0])
            glide(tg, 0.15, 0.05, 4.0, phase=i)
            self.at(cue, lead=0.5)
            self.play(FadeIn(tg, shift=LEFT * 0.3), run_time=0.6)
        db = T("cause: still debated", 34, YELLOW).move_to([4.3, -1.3, 0])
        self.at("debated", lead=0.6)
        self.play(FadeIn(db, scale=1.1), run_time=0.6)
        self.finish()


class S16Rule(SpokenScene):
    def construct(self):
        cx = (-4.5, 0.0, 4.5)
        boxes = [RoundedRectangle(corner_radius=0.2, width=4.0, height=5.0, stroke_color=GREY, stroke_width=3).move_to([x, 0.2, 0]) for x in cx]
        titles = [T(t, 30, TEXT).move_to([x, 2.2, 0]) for t, x in zip(("dogs: heat", "slope b < 1", "heat per kg"), cx)]
        base = -1.7
        # panel 1: dogs' heat
        p1 = VGroup(hbar(-5.3, 0.5, base, 0.8), hbar(-3.7, 2.8, base, 0.8),
                    M("M", 28, TEXT).move_to([-5.3, -2.05, 0]), M("10 M", 28, TEXT).move_to([-3.7, -2.05, 0]))
        # panel 2: Kleiber line (miniature of the log-log plot)
        PM = lambda x, y: np.array([-1.5 + (x + 1) * 0.75, -1.6 + (y - 0.3) * 0.78, 0])
        p2 = VGroup(Line(PM(-1, 0.3), PM(3, 0.3)).set_stroke(TEXT, 3), Line(PM(-1, 0.3), PM(-1, 4.2)).set_stroke(TEXT, 3),
                    *[kdot(PM(*sp_pt(i)), HEAT, 0.08) for i in range(len(SPECIES))],
                    Line(PM(-0.5, LA - 0.375), PM(2.9, LA + 2.175)).set_stroke(TEAL, 6))
        # panel 3: per kg
        p3 = VGroup(hbar(3.6, 2.6, base, 0.8), hbar(5.4, 0.37, base, 0.8),
                    T("mouse", 26, TEXT).move_to([3.6, -2.05, 0]), T("human", 26, TEXT).move_to([5.4, -2.05, 0]))
        panels = [VGroup(b, t, p) for b, t, p in zip(boxes, titles, (p1, p2, p3))]
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in panels], lag_ratio=0.4), run_time=2.4)
        self.at("mammals and birds", lead=0.2)
        self.play(Indicate(panels[1][1], color=YELLOW), run_time=0.8)
        tot = T("more in total", 36, YELLOW).move_to([-2.25, -3.1, 0])
        brk = Line([-6.2, -2.55, 0], [1.7, -2.55, 0]).set_stroke(YELLOW, 4)
        self.at("bigger animals", lead=0.3)
        self.play(boxes[0].animate.set_stroke(YELLOW, 6), boxes[1].animate.set_stroke(YELLOW, 6), Create(brk), FadeIn(tot), run_time=1.0)
        self.at("in total", lead=0.0)
        self.play(Indicate(p1[1], color=HEAT, scale_factor=1.1), run_time=1.0)
        less = T("less per kg", 36, YELLOW).move_to([4.5, -3.1, 0])
        brk2 = Line([2.8, -2.55, 0], [6.2, -2.55, 0]).set_stroke(YELLOW, 4)
        self.at("But they burn", lead=0.3)
        self.play(boxes[2].animate.set_stroke(YELLOW, 6), Create(brk2), FadeIn(less), run_time=1.0)
        self.at("per kilogram", lead=0.0)
        self.play(Indicate(p3[1], color=HEAT, scale_factor=1.1), run_time=1.0)
        self.finish()


class S17End(EndCard):
    LINE = "Bigger animals usually burn more in total, but less per kilogram."
