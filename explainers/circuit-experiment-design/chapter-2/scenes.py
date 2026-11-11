"""How Much Evidence Is Enough? (chapter 2 of Designing a Causal Circuit Experiment)

COLOR MAP (one color per concept, same as chapter 1)
  YELLOW = light            GOLD = opsin-linked manipulation / remainder / pilot estimates
  TEAL   = fluorophore or no opsin (here also: new people)      BLUE = measured outcome
  RED    = unresolved alternative (here also: the wrong unit, too small a group)
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

LIGHT, OPSIN, FLUOR, OUT, ALT = YELLOW, GOLD, TEAL, BLUE, RED
K, N = 8, 40          # animals, trials per animal


def lab(text, color=TEXT, size=28, **kw):
    return T(text, size=size, color=color, weight=BOLD, **kw)


def make_mouse(L=1.3, color=TEXT):
    body = Ellipse(width=0.58 * L, height=0.95 * L)
    head = Ellipse(width=0.42 * L, height=0.46 * L).move_to(UP * 0.56 * L)
    ears = VGroup(*[Circle(radius=0.11 * L).move_to([s * 0.2 * L, 0.72 * L, 0]) for s in (-1, 1)])
    for m in (body, head, ears):
        m.set_stroke(color, 3).set_fill(color, 0.22)
    tail = ArcBetweenPoints(np.array([0, -0.47 * L, 0]), np.array([0.18 * L, -1.05 * L, 0]), angle=0.9).set_stroke(color, 3)
    nose = Dot(np.array([0, 0.79 * L, 0]), radius=0.04 * L + 0.01, color=color)
    return VGroup(tail, body, ears, head, nose)


def idle(m, phase=0.0, amp=0.15, w=1.2):
    st = {"t": phase, "a": amp * np.sin(w * phase)}

    def u(mm, dt):
        st["t"] += dt
        a = amp * np.sin(w * st["t"])
        mm.rotate(a - st["a"])
        st["a"] = a
    m.add_updater(u)
    return m


def meter(x, ybot, h, w, val, color=OUT, outline=TEXT):
    frame = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=outline, stroke_width=3,
                             fill_opacity=0).move_to([x, ybot + h / 2, 0])
    fill = Rectangle(width=w - 0.1, height=0.05, stroke_width=0, fill_color=color, fill_opacity=0.9)

    def upd(m):
        hh = max(float(val()) * (h - 0.1), 0.03)
        m.stretch_to_fit_height(hh)
        m.move_to([x, ybot + 0.05 + hh / 2, 0])
    fill.add_updater(upd)
    upd(fill)
    return VGroup(frame, fill)


def bob(m, phase=0.0, amp=0.06, w=1.6):
    st = {"t": phase, "y": 0.0}

    def u(mm, dt):
        st["t"] += dt
        y = amp * np.sin(w * st["t"])
        mm.shift(UP * (y - st["y"]))
        st["y"] = y
    m.add_updater(u)
    return m


def person(color=TEXT, s=0.65, op=0.25):
    head = Circle(radius=0.2, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=op).move_to([0, 0.32, 0])
    body = RoundedRectangle(corner_radius=0.24, width=0.66, height=0.62, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([0, -0.2, 0])
    return VGroup(body, head).scale(s)


class W(SpokenScene):
    def setup(self):
        super().setup()
        self.clk = ValueTracker(0)
        self.clk.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.clk)


# ------------------------------------------------------------------------------------------
# Hook board: the chapter-one two-by-two board (rows: construct, columns: light)
class S00Hook(W):
    def construct(self):
        clk = self.clk
        CX = [-4.05, -0.25]
        RY = [1.5, -1.45]
        CW, RH = 3.7, 2.8
        vals = {(0, 0): 0.30, (0, 1): 0.85, (1, 0): 0.30, (1, 1): 0.60}
        cells, mice, meters, tags = VGroup(), VGroup(), VGroup(), VGroup()
        for r in (0, 1):
            for c in (0, 1):
                fill, op = (LIGHT, 0.12) if c else ("#05060a", 0.6)
                cells.add(Rectangle(width=CW, height=RH, stroke_color=GREY, stroke_width=2.5, fill_color=fill,
                                    fill_opacity=op).move_to([CX[c], RY[r], 0]))
                col = OPSIN if r == 0 else FLUOR
                mice.add(idle(make_mouse(0.85, col).move_to([CX[c] - 0.85, RY[r] - 0.25, 0]), phase=r * 1.7 + c * 0.9))
                v = (lambda r=r, c=c: float(np.clip(vals[(r, c)] + 0.08 * np.sin(1.1 * clk.get_value() + r * 1.7 + c * 0.9), 0.03, 1)))
                meters.add(meter(CX[c] + 1.2, RY[r] - 1.2, 2.0, 0.5, v))
                tags.add(lab("OPSIN" if r == 0 else "FLUOROPHORE", col, 26).move_to([CX[c], RY[r] + RH / 2 - 0.3, 0]))
        heads = VGroup(lab("LIGHT OFF", TEXT, 30).move_to([CX[0], 3.4, 0]), lab("LIGHT ON", LIGHT, 30).move_to([CX[1], 3.4, 0]))
        rem, wa = ValueTracker(0.0), ValueTracker(0.0)
        g = meter(4.0, -2.85, 5.7, 1.0, lambda: rem.get_value() + wa.get_value() * np.sin(5.5 * clk.get_value()), color=OPSIN)
        self.play(FadeIn(cells), FadeIn(heads), FadeIn(tags), FadeIn(mice), FadeIn(meters), FadeIn(g), run_time=1.4)
        self.at("matched controls")
        self.play(*[cells[i].animate.set_stroke(OPSIN if i < 2 else FLUOR, 5) for i in range(4)], run_time=1.0)

        eff = lab("EFFECT", OPSIN, 32).move_to([4.0, 3.4, 0])
        self.at("identify")
        self.play(FadeIn(eff), rem.animate.set_value(0.30), run_time=1.6)
        self.at("looks large")
        self.play(rem.animate.set_value(0.88), run_time=1.1)

        def halo():
            s = (np.sin(3.2 * clk.get_value()) + 1) / 2
            top = -2.85 + 0.05 + (rem.get_value() + 0.0) * 5.6
            return Ellipse(width=1.8 + 0.6 * s, height=0.8 + 0.35 * s, stroke_color=ALT, stroke_width=6,
                           stroke_opacity=min(1.0, wa.get_value() * 12) * (0.95 - 0.5 * s), fill_opacity=0).move_to([4.0, top, 0])
        hal = always_redraw(halo)
        self.add(hal)
        q = T("How much evidence is enough?", size=40, color=TEXT).move_to([-2.15, 3.4, 0])
        self.at("how much evidence")
        self.play(wa.animate.set_value(0.08), FadeOut(heads), FadeOut(tags), FadeIn(q, shift=UP * 0.2), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Designing a Causal Circuit Experiment"
    TITLE = "How Much Evidence Is Enough?"


# ------------------------------------------------------------------------------------------
# Animals and their trials
class Pens:
    """Eight mouse pens. Trials are blue dots that wander but stay inside their own pen."""
    BASE = -0.14

    def __init__(self, clk):
        rng = np.random.default_rng(11)
        self.clk = clk
        m = rng.normal(0, 0.09, K).clip(-0.17, 0.17)
        self.m = m - m.mean()
        self.v = self.BASE + self.m[:, None] + rng.normal(0, 0.05, (K, N)).clip(-0.11, 0.11)
        self.u = rng.normal(0, 0.16, (K, N)).clip(-0.33, 0.33)
        self.ph = rng.uniform(0, 6.28, (K, N, 2))
        self.vis, self.dim = ValueTracker(0), ValueTracker(1)
        self.rects = [Rectangle(width=3.2, height=2.55, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.06)
                      for _ in range(K)]
        self.mice = [make_mouse(0.55, TEXT) for _ in range(K)]
        self.dots = [[Dot(radius=0.055, color=OUT) for _ in range(N)] for _ in range(K)]
        for row in self.dots:
            for d in row:
                d.set_fill(OUT, opacity=0)
        self.rect_g, self.mice_g = VGroup(*self.rects), VGroup(*self.mice)
        self.layer = VGroup(*[d for row in self.dots for d in row])
        self.grid()
        self.layer.add_updater(self._upd)
        self.mice_g.add_updater(self._mupd)

    def grid(self):
        xs, ys = [-5.1, -1.7, 1.7, 5.1], [1.55, -1.25]
        for i, r in enumerate(self.rects):
            r.stretch_to_fit_width(3.2).stretch_to_fit_height(2.55).move_to([xs[i % 4], ys[i // 4], 0])

    def row_pos(self, i):
        return [-5.775 + 1.65 * i, 0.55, 0]

    def row(self):
        for i, r in enumerate(self.rects):
            r.stretch_to_fit_width(1.45).stretch_to_fit_height(3.6).move_to(self.row_pos(i))

    def to_row_anims(self):
        return [r.animate.stretch_to_fit_width(1.45).stretch_to_fit_height(3.6).move_to(self.row_pos(i)) for i, r in enumerate(self.rects)]

    def mean_pos(self, i):
        r = self.rects[i]
        c = r.get_center()
        return np.array([c[0], c[1] + (self.BASE + self.m[i]) * r.height, 0])

    def _mupd(self, g):
        for i, mo in enumerate(self.mice):
            r = self.rects[i]
            mo.move_to(r.get_center() + UP * 0.28 * r.height)

    def _upd(self, g):
        t = self.clk.get_value()
        nv, dim = self.vis.get_value() * N, self.dim.get_value()
        for i in range(K):
            r = self.rects[i]
            c, w, h = r.get_center(), r.width, r.height
            for j, d in enumerate(self.dots[i]):
                x = c[0] + (self.u[i, j] + 0.04 * np.sin(1.3 * t + self.ph[i, j, 0])) * w
                y = c[1] + (self.v[i, j] + 0.025 * np.cos(1.1 * t + self.ph[i, j, 1])) * h
                d.move_to([x, y, 0])
                d.set_fill(OUT, opacity=float(np.clip(nv - j, 0, 1)) * dim)


def counter(name, fn, color, x, y=3.4):
    l = lab(name, color, 30).move_to([x, y, 0])
    v = always_redraw(lambda: M(str(int(round(fn()))), 34, color).next_to(l, RIGHT, buff=0.3))
    return VGroup(l, v)


def gates(ca=TEXT, cb=TEXT):
    return (chip("8 ANIMALS", ca, size=36).move_to([-3.4, -2.7, 0]), chip("320 TRIALS", cb, size=36).move_to([3.4, -2.7, 0]))


def bracket(y=2.95, x0=-6.45, x1=6.45):
    return VGroup(Line([x0, y - 0.25, 0], [x0, y, 0]), Line([x0, y, 0], [x1, y, 0]), Line([x1, y, 0], [x1, y - 0.25, 0])).set_stroke(GOLD, 7)


class S02DataHaveLevels(W):
    def construct(self):
        P = Pens(self.clk)
        self.add(P.layer)
        self.play(FadeIn(P.rect_g), FadeIn(P.mice_g), run_time=1.2)
        self.at("hundreds of responses")
        tc = counter("TRIALS", lambda: P.vis.get_value() * N * K, OUT, -4.4)
        self.play(FadeIn(tc), run_time=0.4)
        self.play(P.vis.animate.set_value(1), run_time=3.0, rate_func=linear)
        self.at("independent units")
        ac = counter("ANIMALS", lambda: 8, OPSIN, 1.4)
        self.play(FadeIn(ac, shift=DOWN * 0.2), run_time=0.6)
        self.play(Indicate(ac, color=OPSIN, scale_factor=1.12), run_time=1.2)
        self.at("share each animal's")
        self.play(P.rect_g.animate.set_stroke(OPSIN, 5), run_time=0.6)
        c1 = lab("EXPRESSION", OPSIN, 32).move_to([0, -3.3, 0])
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
        self.at("fiber placement")
        c2 = lab("FIBER PLACEMENT", OPSIN, 32).move_to([0, -3.3, 0])
        self.play(ReplacementTransform(c1, c2), run_time=0.6)
        self.at("and state")
        c3 = lab("STATE", OPSIN, 32).move_to([0, -3.3, 0])
        self.play(ReplacementTransform(c2, c3), run_time=0.6)
        self.at("More trials")
        self.play(FadeOut(c3), P.rect_g.animate.set_stroke(TEXT, 3), run_time=0.6)
        self.at("sharpen")
        rings = VGroup(*[Circle(radius=0.2, stroke_color=TEXT, stroke_width=4).move_to(P.mean_pos(i) + DOWN * 0.0) for i in range(K)])
        self.play(LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.12), run_time=1.0)
        lm = lab("EACH ANIMAL'S MEAN", TEXT, 28).move_to([0, -3.3, 0])
        self.at("that animal's mean")
        self.play(FadeIn(lm, shift=UP * 0.15), run_time=0.5)
        self.at("do not create")
        self.play(FadeOut(lm), FadeOut(rings), Indicate(ac, color=OPSIN, scale_factor=1.15), run_time=1.4)
        self.finish()


class S03Predict(W):
    def construct(self):
        P = Pens(self.clk)
        P.vis.set_value(1)
        tc = counter("TRIALS", lambda: 320, OUT, -4.4)
        ac = counter("ANIMALS", lambda: 8, OPSIN, 1.4)
        self.add(P.rect_g, P.mice_g, P.layer, tc, ac)
        self.play(FadeOut(tc), FadeOut(ac), *P.to_row_anims(), run_time=1.6)
        br = bracket()
        g1, g2 = gates()
        self.at("Does the study")
        self.play(Create(br), run_time=1.0)
        self.at("eight independent units")
        self.play(FadeIn(g1, shift=UP * 0.25), run_time=0.7)
        self.at("or 320")
        self.play(FadeIn(g2, shift=UP * 0.25), run_time=0.7)
        self.finish()


class S04Pause(W):
    def construct(self):
        P = Pens(self.clk)
        P.vis.set_value(1)
        P.row()
        g1, g2 = gates()
        br = bracket()
        self.add(P.rect_g, P.mice_g, P.layer, g1, g2, br)
        self.wait(1.4)
        self.play(Indicate(br, color=OPSIN, scale_factor=1.04), run_time=1.6)
        self.finish()


def summary_world(P):
    """Row of pens with one blue summary point per animal, the faint trial cloud behind, and the honest band."""
    S = VGroup(*[Dot(radius=0.17, color=OUT).set_stroke(TEXT, 3) for _ in range(K)])
    for i, s in enumerate(S):
        s.move_to(P.mean_pos(i))
        s.set_z_index(5)
    h = P.rects[0].height
    gm = P.rects[0].get_center()[1] + P.BASE * h
    allv = P.v.flatten()
    naive = 1.96 * allv.std(ddof=1) / math.sqrt(K * N) * h
    honest = 2.365 * P.m.std(ddof=1) / math.sqrt(K) * h
    return S, gm, naive, honest


def band(gm, half, color, op=0.45):
    return Rectangle(width=12.9, height=max(2 * half, 0.07), stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to([0, gm, 0])


class S05Reveal(W):
    def construct(self):
        P = Pens(self.clk)
        P.vis.set_value(1)
        P.row()
        g1, g2 = gates()
        br = bracket()
        self.add(P.rect_g, P.mice_g, P.layer, g1, g2, br)
        S, gm, naive, honest = summary_world(P)
        self.at("independent unit is")
        self.play(g1.animate.set_color(OPSIN), Indicate(br, color=OPSIN, scale_factor=1.03), run_time=1.2)
        self.play(g2.animate.set_color(ALT), run_time=0.6)
        self.play(g2.animate.scale(0.05).set_opacity(0), run_time=0.8)
        self.at("Keep its trials")
        self.play(P.rect_g.animate.set_stroke(OPSIN, 5), P.dim.animate.set_value(0.35), P.mice_g.animate.set_opacity(0),
                  FadeIn(S, scale=1.8), run_time=1.6)
        self.at("Treating every trial")
        self.play(P.rect_g.animate.set_stroke(opacity=0.15), run_time=1.5)
        bnd = band(gm, naive, ALT, 0.7)
        tag = chip("TOO NARROW", ALT, size=32).move_to([3.4, -2.7, 0])
        self.at("erases shared variation")
        self.play(GrowFromCenter(bnd), FadeIn(tag), run_time=1.4)
        sch = T("SCHEMATIC", size=24, color=TEXT).move_to([5.6, -3.5, 0])
        self.play(FadeIn(sch), run_time=0.5)
        self.at("more precise")
        self.play(Indicate(tag, color=ALT, scale_factor=1.1), run_time=0.9)
        self.at("than the experiment")
        bnd2 = band(gm, honest, OUT, 0.4)
        tag2 = chip("HONEST", OUT, size=32).move_to([3.4, -2.7, 0])
        self.play(Transform(bnd, bnd2), ReplacementTransform(tag, tag2), P.rect_g.animate.set_stroke(OPSIN, 5), run_time=1.6)
        self.finish()


# ------------------------------------------------------------------------------------------
# Effect size
GAP, BASEY = 1.8, -2.2
MA, MB = -2.2, -0.4


def bell(mean, sdt, grow, color=OUT):
    def build():
        sd, g = sdt.get_value(), grow.get_value()
        xs = np.linspace(mean - 2.3 * sd, mean + 2.3 * sd, 70)
        ys = g * 2.9 * (0.8 / sd) * np.exp(-0.5 * ((xs - mean) / sd) ** 2)
        pts = [np.array([x, BASEY + y, 0]) for x, y in zip(xs, ys)]
        return Polygon(*pts, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    return always_redraw(build)


def gauge_d(sdt, x=5.7):
    return meter(x, -2.9, 5.0, 0.8, lambda: (GAP / sdt.get_value()) / 2.5, color=OUT)


class S06EffectSize(W):
    def construct(self):
        clk = self.clk
        P = Pens(clk)
        P.vis.set_value(1)
        P.dim.set_value(0.35)
        P.row()
        P.rect_g.set_stroke(OPSIN, 5).set_stroke(opacity=0.15)
        P.rect_g.set_fill(opacity=0.03)
        P.mice_g.set_opacity(0)
        S, gm, naive, honest = summary_world(P)
        bnd = band(gm, honest, OUT, 0.4)
        self.add(P.rect_g, P.mice_g, P.layer, bnd, S)
        sdt, grow = ValueTracker(1.2), ValueTracker(0.0)
        base = Line([-6.5, BASEY, 0], [4.6, BASEY, 0]).set_stroke(TEXT, 3)
        bA, bB = bell(MA, sdt, grow), bell(MB, sdt, grow)
        zs = [-1.3, -0.45, 0.45, 1.3]
        targets = [np.array([MA + 0.8 * z, BASEY + 0.45, 0]) for z in zs] + [np.array([MB + 0.8 * z, BASEY + 0.45, 0]) for z in zs]
        self.add(base, bA, bB)
        self.play(FadeOut(bnd), P.dim.animate.set_value(0), P.rect_g.animate.set_stroke(opacity=0).set_fill(opacity=0),
                  *[s.animate.move_to(t) for s, t in zip(S, targets)], run_time=1.0)
        self.play(grow.animate.set_value(1), FadeOut(S, scale=0.3), run_time=1.0)
        la = lab("GROUP A", OUT, 30).move_to([-4.9, 1.0, 0])
        lb = lab("GROUP B", OUT, 30).move_to([2.4, 1.0, 0])
        sch = T("SCHEMATIC", size=24, color=TEXT).move_to([-5.4, -3.5, 0])
        self.play(FadeIn(la), FadeIn(lb), FadeIn(sch), run_time=0.4)
        self.at("standardized effect")
        gg = gauge_d(sdt)
        gl = lab("EFFECT\nSIZE", TEXT, 28).move_to([5.7, 3.0, 0])
        gd = always_redraw(lambda: M(f"d = {GAP / sdt.get_value():.1f}", 28, OUT).move_to([5.7, -3.4, 0]))
        self.play(FadeIn(gg), FadeIn(gl), FadeIn(gd), run_time=1.0)
        self.at("difference between the means")
        guides = VGroup(DashedLine([MA, BASEY, 0], [MA, 2.3, 0]), DashedLine([MB, BASEY, 0], [MB, 2.3, 0])).set_stroke(GREY, 3)
        arr = DoubleArrow([MA, 2.3, 0], [MB, 2.3, 0], buff=0, color=OPSIN, stroke_width=8, tip_length=0.22)
        gl2 = lab("MEAN GAP", OPSIN, 30).move_to([(MA + MB) / 2, 2.9, 0])
        self.play(Create(guides), run_time=0.6)
        self.play(GrowFromCenter(arr), FadeIn(gl2), run_time=0.8)
        self.at("pooled spread")
        sp = always_redraw(lambda: DoubleArrow([MB, -2.75, 0], [MB + sdt.get_value(), -2.75, 0], buff=0, color=TEXT,
                                               stroke_width=6, tip_length=0.18))
        spl = always_redraw(lambda: lab("SPREAD", TEXT, 28).move_to([MB + sdt.get_value() / 2, -3.25, 0]))
        self.play(FadeIn(sp), FadeIn(spl), run_time=0.8)
        self.at("looks larger")
        self.play(sdt.animate.set_value(0.8), run_time=2.2)
        self.at("looks smaller")
        self.play(sdt.animate.set_value(1.8), run_time=3.2)
        self.finish()


# ------------------------------------------------------------------------------------------
# Sample-size curve
PX0, PX1, PY0, PY1 = -5.4, 4.6, -2.5, 2.8


def Xd(d):
    return PX0 + (d - 0.3) / 1.2 * (PX1 - PX0)


def Yn(n):
    return PY0 + n / 180 * (PY1 - PY0)


def nd(d):
    return 2 * 2.80 ** 2 / d ** 2


def axes_world():
    xa = Line([PX0 - 0.2, PY0, 0], [PX1 + 0.4, PY0, 0]).set_stroke(TEXT, 4)
    ya = Line([PX0, PY0 - 0.1, 0], [PX0, 3.0, 0]).set_stroke(TEXT, 4)
    ticks = VGroup(*[M(s, 24, TEXT).move_to([Xd(float(s)), -2.85, 0]) for s in ("0.5", "1.0", "1.5")],
                   *[M(str(n), 24, TEXT).move_to([PX0 - 0.45, Yn(n), 0]) for n in (50, 100, 150)])
    xt = lab("EFFECT SIZE d", TEXT, 28).move_to([0.4, -3.45, 0])
    yt = lab("GROUP SIZE n", TEXT, 28).rotate(PI / 2).move_to([-6.5, 0.1, 0])
    return VGroup(xa, ya, ticks, xt, yt)


def curve_mob():
    ds = np.linspace(0.3, 1.5, 121)
    c = VMobject(stroke_color=OUT, stroke_width=7)
    c.set_points_as_corners([np.array([Xd(d), Yn(nd(d)), 0]) for d in ds])
    return c


def mark(d, label, lx, ly):
    n = nd(d)
    dot = Dot([Xd(d), Yn(n), 0], radius=0.13, color=TEXT)
    dl = DashedLine([Xd(d), PY0, 0], [Xd(d), Yn(n), 0]).set_stroke(GREY, 3)
    tx = M(label, 28, TEXT)
    tx.move_to([lx + tx.width / 2, ly, 0])
    return VGroup(dl, dot, tx)


class S07PowerCurve(W):
    def construct(self):
        clk = self.clk
        sdt, grow = ValueTracker(1.8), ValueTracker(1.0)
        bA, bB = bell(MA, sdt, grow), bell(MB, sdt, grow)
        base = Line([-6.5, BASEY, 0], [4.6, BASEY, 0]).set_stroke(TEXT, 3)
        old = VGroup(base, bA, bB)
        arr = DoubleArrow([MA, 2.3, 0], [MB, 2.3, 0], buff=0, color=OPSIN, stroke_width=8, tip_length=0.22)
        gg = gauge_d(sdt)
        self.add(old, arr, gg)
        ax = axes_world()
        self.play(FadeOut(old), FadeOut(arr), FadeOut(gg), FadeIn(ax), run_time=1.4)
        self.at("worth detecting")
        wl = Line([Xd(0.5), PY0, 0], [Xd(0.5), 3.0, 0]).set_stroke(OUT, 6)
        wt = lab("WORTH DETECTING", OUT, 28)
        wt.move_to([Xd(0.5) + 0.25 + wt.width / 2, 1.5, 0])
        self.play(Create(wl), FadeIn(wt), run_time=1.0)
        self.at("small pilot")
        px = lambda: Xd(1.2 + 0.2 * np.sin(0.9 * clk.get_value()))
        pil = always_redraw(lambda: VGroup(Dot([px(), 3.0, 0], radius=0.15, color=OPSIN),
                                           DashedLine([px(), 2.55, 0], [px(), 2.85, 0]).set_stroke(OPSIN, 3, opacity=0.5),
                                           lab("PILOT", OPSIN, 28).move_to([px(), 3.45, 0])))
        self.play(FadeIn(pil), run_time=0.7)
        self.at("sample size curve")
        cv = curve_mob()
        self.play(Create(cv), run_time=1.9, rate_func=linear)
        self.at("smaller target effects")
        m1 = mark(1.0, f"d = 1.0, n = {math.ceil(nd(1.0))}", Xd(1.0) + 0.3, -1.55)
        self.play(FadeIn(m1), run_time=0.8)
        m2 = mark(0.5, f"d = 0.5, n = {math.ceil(nd(0.5))}", Xd(0.5) + 0.25, -0.05)
        self.play(FadeIn(m2), run_time=0.8)
        self.at("rises sharply")
        seg = VMobject(stroke_color=OPSIN, stroke_width=10)
        seg.set_points_as_corners([np.array([Xd(d), Yn(nd(d)), 0]) for d in np.linspace(0.3, 0.6, 30)])
        self.play(ShowPassingFlash(seg, time_width=0.6), run_time=1.8)
        self.at("noisy overlap")
        sd = ValueTracker(1.0)

        def ov(m):
            xs = np.linspace(m - 2.2, m + 2.2, 50)
            pts = [np.array([3.9 + 0.6 * (x), 0.1 + 1.7 * math.exp(-0.5 * (x - m) ** 2), 0]) for x in xs]
            poly = Polygon(*pts, stroke_color=OUT, stroke_width=4, fill_color=OUT, fill_opacity=0.25)
            return poly
        ovg = VGroup(ov(-0.45), ov(0.45))
        ovl = lab("OVERLAP", OUT, 28).move_to([3.9, 2.2, 0])
        self.play(FadeIn(ovg), FadeIn(ovl), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------------------------------
class S08SelectedPilots(W):
    def construct(self):
        clk = self.clk
        ax = axes_world()
        wl = Line([Xd(0.5), PY0, 0], [Xd(0.5), 3.0, 0]).set_stroke(OUT, 6)
        wt = lab("WORTH DETECTING", OUT, 28)
        wt.move_to([Xd(0.5) + 0.25 + wt.width / 2, 1.5, 0])
        cv = curve_mob()
        self.add(ax, wl, wt, cv)
        zs = [-0.6, -0.45, -0.3, -0.18, -0.08, 0.0, 0.1, 0.22, 0.35, 0.5, 0.65, 0.85, 1.1, 1.5]
        dh = [0.5 + 0.33 * z for z in zs]
        est = VGroup(*[Dot([Xd(d), 3.3, 0], radius=0.12, color=OPSIN) for d in dh])
        for i, e in enumerate(est):
            bob(e, phase=i * 0.9, amp=0.1, w=2.0)
        self.at("Small pilots")
        tl = lab("TRUE EFFECT", OUT, 28).move_to(wt.get_center())
        self.play(LaggedStart(*[GrowFromCenter(e) for e in est], lag_ratio=0.12), ReplacementTransform(wt, tl), run_time=2.2)
        pl = lab("PILOT ESTIMATES", OPSIN, 28).move_to([3.4, 2.3, 0])
        self.play(FadeIn(pl), run_time=0.6)
        self.at("overshoot")
        top = est[-1]
        ring = Circle(radius=0.3, stroke_color=TEXT, stroke_width=5).move_to(top.get_center())
        ring.add_updater(lambda m: m.move_to(top.get_center()))
        self.play(Create(ring), *[e.animate.set_fill(OPSIN, opacity=0.3) for e in est[:-1]], run_time=1.0)
        self.at("planning copies")
        dtop = dh[-1]
        land = np.array([Xd(dtop), Yn(nd(dtop)), 0])
        top.clear_updaters()
        self.play(top.animate.move_to(land), run_time=1.5)
        self.at("lucky estimate")
        dl = DashedLine(land, [Xd(dtop), PY0, 0]).set_stroke(ALT, 4)
        self.play(Create(dl), run_time=0.8)
        self.at("too small")
        tray = RoundedRectangle(corner_radius=0.15, width=3.4, height=1.3, stroke_color=ALT, stroke_width=5, fill_color=ALT, fill_opacity=0.15).move_to([3.2, -0.6, 0])
        nn = math.ceil(nd(dtop))
        dots = VGroup(*[Dot(radius=0.11, color=ALT).move_to([3.2 - 1.4 + 0.37 * (k % 8), -0.6 + 0.3 * (0.5 - k // 8) * 1.8 - 0.0, 0]) for k in range(nn)])
        tt = lab("TOO SMALL", ALT, 32).move_to([3.2, 0.3, 0])
        self.play(GrowFromCenter(tray), FadeIn(tt), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.05), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------------------------
# Human imaging
PY, PS = -2.75, 0.85


def sig(p, u, t):
    shared = 0.8 * np.sin(2 * np.pi * (1.1 * u - 0.15 * t))
    noise = 0.55 * np.sin(2 * np.pi * (2.9 * u + 0.23 * t) + 1.9 * p) + 0.35 * np.sin(2 * np.pi * (4.7 * u - 0.31 * t) + 2.7 * p)
    return shared + noise


def wave(p, x0, y0, width, clk, color=OUT, amp=0.22):
    w = VMobject(stroke_color=color, stroke_width=4)

    def upd(m):
        t = clk.get_value()
        us = np.linspace(0, 1, 36)
        m.set_points_as_corners([np.array([x0 - width / 2 + width * u, y0 + amp * sig(p, u, t), 0]) for u in us])
    w.add_updater(upd)
    upd(w)
    return w


def avg_wave(P, x0, y0, width, clk):
    w = VMobject(stroke_color=OUT, stroke_width=8)

    def upd(m):
        t = clk.get_value()
        us = np.linspace(0, 1, 90)
        m.set_points_as_corners([np.array([x0 - width / 2 + width * u, y0 + 0.6 * np.mean([sig(p, u, t) for p in range(P)]), 0]) for u in us])
    w.add_updater(upd)
    upd(w)
    return w


def card(letter, color=OUT):
    r = RoundedRectangle(corner_radius=0.1, width=0.9, height=0.55, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.2)
    return VGroup(r, lab(letter, TEXT, 28).move_to(r))


def scanner(x, y):
    ring = Circle(radius=0.9, stroke_color=TEXT, stroke_width=6).move_to([x, y, 0])
    inner = Circle(radius=0.5, stroke_color=GREY, stroke_width=4).move_to([x, y, 0])
    tbl = Rectangle(width=2.0, height=0.2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.2).move_to([x, y, 0])
    return VGroup(ring, inner, tbl)


class S09HumanScale(W):
    def construct(self):
        clk = self.clk
        xs = [-4.95 + 1.1 * i for i in range(10)]
        ppl = VGroup(*[bob(person(TEXT, 0.85).move_to([x, PY, 0]), phase=i * 0.7) for i, x in enumerate(xs)])
        self.play(LaggedStart(*[GrowFromCenter(p) for p in ppl], lag_ratio=0.1), run_time=2.0)
        self.at("human imaging")
        sc = scanner(-5.2, 2.75)
        sch = T("SCHEMATIC", size=24, color=TEXT).move_to([0, -3.55, 0])
        self.play(FadeIn(sc), FadeIn(sch), run_time=0.9)
        self.at("brain wide associations")
        waves = VGroup(*[wave(i, x, -1.2, 0.9, clk, amp=0.32) for i, x in enumerate(xs)])
        self.play(LaggedStart(*[Create(w) for w in waves], lag_ratio=0.1), run_time=1.8)
        self.at("among people")
        av = avg_wave(10, 0.0, 0.7, 10.4, clk)
        self.play(Create(av), run_time=1.6)
        self.at("blood oxygenation signal")
        bl = lab("BOLD", OUT, 36).move_to([-2.9, 2.75, 0])
        self.play(FadeIn(bl, shift=RIGHT * 0.2), run_time=0.7)
        self.at("spike count")
        bl2 = lab("BOLD, not spikes", OUT, 36).move_to([-1.85, 2.75, 0])
        self.play(ReplacementTransform(bl, bl2), run_time=0.8)
        self.at("group average")
        agl = lab("GROUP AVERAGE", OUT, 28).move_to([3.9, 1.75, 0])
        self.play(FadeIn(agl), Indicate(av, color=OUT, scale_factor=1.02), run_time=1.4)
        self.at("stable rankings")
        cards = [card(l).move_to([1.7 + 1.1 * k, 2.75, 0]) for k, l in enumerate("ABCDE")]
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in cards], lag_ratio=0.12), run_time=1.2)
        p = [c.get_center() for c in cards]
        self.play(cards[0].animate.move_to(p[1]), cards[1].animate.move_to(p[0]), run_time=0.9)
        self.play(cards[2].animate.move_to(p[4]), cards[4].animate.move_to(p[2]), run_time=0.9)
        self.finish()


class S10Precision(W):
    def construct(self):
        clk = self.clk
        NP = 24
        fx = [-5.75 + 0.5 * i for i in range(NP)]
        old_idx = list(range(7, 17))
        start_x = [-4.95 + 1.1 * k for k in range(10)]
        ppl = []
        for i in range(NP):
            if i in old_idx:
                p = person(TEXT, 0.85).move_to([start_x[old_idx.index(i)], PY, 0])
            else:
                p = person(TEAL, 0.55).move_to([-8.5 if i < 7 else 8.5, PY, 0])
            bob(p, phase=i * 0.6)
            ppl.append(p)
        pg = VGroup(*ppl)
        self.add(pg)
        rng = np.random.default_rng(5)
        xd = rng.uniform(-1, 1, NP)
        yd = 0.35 * xd + 0.55 * rng.normal(0, 1, NP)
        SX0, SX1, SY0, SY1 = -6.0, -0.7, -1.0, 2.8
        sx = lambda x: (SX0 + SX1) / 2 + 2.45 * x
        sy = lambda y: 0.9 + 1.25 * y
        nt = ValueTracker(10)
        frame = VGroup(Line([SX0, SY0, 0], [SX0, SY1, 0]), Line([SX0, SY0, 0], [SX1, SY0, 0])).set_stroke(TEXT, 4)
        pts = VGroup(*[Dot(radius=0.1, color=OUT) for i in range(NP)])

        def pts_upd(g):
            n = nt.get_value()
            t = clk.get_value()
            for i, d in enumerate(pts):
                d.move_to([sx(xd[i]) + 0.04 * np.sin(1.4 * t + i), float(np.clip(sy(yd[i]), SY0 + 0.1, SY1 - 0.1)) + 0.04 * np.cos(1.2 * t + 2 * i), 0])
                d.set_fill(OUT if i < 10 else TEAL, opacity=float(np.clip(n - i, 0, 1)))
        pts.add_updater(pts_upd)

        def band_build():
            n = max(int(round(nt.get_value())), 4)
            x, y = xd[:n], np.clip(yd[:n], -0.9, 1.6)
            b, a = np.polyfit(x, y, 1)
            res = y - (a + b * x)
            s = math.sqrt((res ** 2).sum() / (n - 2))
            tcrit = 1.96 + 2.5 / n + 5.0 / n ** 2
            gx = np.linspace(-1, 1, 30)
            hw = tcrit * s * np.sqrt(1 / n + (gx - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum()) * 0.55
            up = [np.array([sx(g), float(np.clip(sy(a + b * g + h), SY0, SY1)), 0]) for g, h in zip(gx, hw)]
            lo = [np.array([sx(g), float(np.clip(sy(a + b * g - h), SY0, SY1)), 0]) for g, h in zip(gx, hw)]
            poly = Polygon(*(up + lo[::-1]), stroke_width=0, fill_color=OUT, fill_opacity=0.35)
            line = Line([sx(-1), sy(a - b), 0], [sx(1), sy(a + b), 0]).set_stroke(TEXT, 5)
            return VGroup(poly, line)
        bnd = always_redraw(band_build)
        self.add(frame, bnd, pts)
        col1 = [card(l).move_to([2.2, 2.1 - 0.65 * k, 0]) for k, l in enumerate("ABCDE")]
        v1 = lab("VISIT ONE", TEXT, 28).move_to([2.2, 2.85, 0])
        t1 = lab("PRECISION", TEXT, 34).move_to([-3.35, 3.45, 0])
        t2 = lab("RELIABILITY", TEXT, 34).move_to([3.8, 3.45, 0])
        self.at("different checks")
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(v1), LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in col1], lag_ratio=0.1), run_time=1.4)
        self.at("larger sample")
        moves = []
        for i, p in enumerate(ppl):
            if i in old_idx:
                moves.append(p.animate.scale(0.65 / 0.85).move_to([fx[i], PY, 0]))
            else:
                moves.append(p.animate.scale(0.65 / 0.55).move_to([fx[i], PY, 0]))
        self.play(*moves, nt.animate.set_value(NP), run_time=4.4, rate_func=smooth)
        self.at("Repeating the measurement")
        perm = [1, 0, 2, 4, 3]
        v2 = lab("VISIT TWO", TEXT, 28).move_to([5.3, 2.85, 0])
        col2 = [c.copy() for c in col1]
        self.add(*col2)
        self.play(FadeIn(v2), *[col2[k].animate.move_to([5.3, 2.1 - 0.65 * perm[k], 0]) for k in range(5)], run_time=2.0)
        lines = VGroup(*[Line(col1[k].get_right(), col2[k].get_left()).set_stroke(TEXT, 3, opacity=0.7) for k in range(5)])
        for k, ln in enumerate(lines):
            ln.add_updater(lambda m, a=col1[k], b=col2[k]: m.put_start_and_end_on(a.get_right(), b.get_left()))
        self.at("relative scores")
        self.play(Create(lines), run_time=0.8)
        self.at("strong group average")
        badge = chip("GROUP AVERAGE", OUT, size=36).move_to([0, -1.75, 0])
        self.play(FadeIn(badge, shift=UP * 0.2), run_time=0.7)
        self.play(Indicate(badge, color=OUT, scale_factor=1.08), run_time=0.8)
        sw = lambda a, b: [col2[a].animate.move_to(col2[b].get_center()), col2[b].animate.move_to(col2[a].get_center())]
        self.play(*sw(2, 4), run_time=1.0)
        self.at("either check")
        self.play(Indicate(frame, color=OUT, scale_factor=1.03), Indicate(lines, color=TEXT, scale_factor=1.03), run_time=1.2)
        self.at("individual biomarker")
        self.play(*sw(0, 1), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------------------------------
LY = [2.5, 0.0, -2.5]
LH = 1.8


def lane_rects(colors=(OUT, FLUOR, OPSIN)):
    rs, ls = VGroup(), VGroup()
    for i, (name, col) in enumerate(zip(("ASSOCIATION", "PREDICTION", "CAUSATION"), colors)):
        rs.add(Rectangle(width=12.8, height=LH, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.07).move_to([0, LY[i], 0]))
        ls.add(lab(name, col, 30).move_to([-4.85, LY[i], 0]))
    return rs, ls


class S11ClaimLadder(W):
    def construct(self):
        clk = self.clk
        rs, ls = lane_rects()
        self.at("Keep three claims")
        self.play(LaggedStart(*[FadeIn(r) for r in rs], lag_ratio=0.3), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in ls], lag_ratio=0.3), run_time=1.0)
        # lane 1: two gauges that move together
        self.at("Association says")
        g1 = meter(-0.8, LY[0] - 0.75, 1.5, 0.5, lambda: 0.5 + 0.3 * np.sin(1.1 * clk.get_value()), color=OUT)
        g2 = meter(1.4, LY[0] - 0.75, 1.5, 0.5, lambda: 0.48 + 0.28 * np.sin(1.1 * clk.get_value() + 0.25), color=OUT)
        sc1 = VGroup(*[Dot([3.2 + 0.4 * k, LY[0] - 0.55 + 0.17 * k + 0.12 * ((k * 7) % 5 - 2), 0], radius=0.1, color=OUT) for k in range(7)])
        for k, d in enumerate(sc1):
            bob(d, phase=k, amp=0.05, w=1.3)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(sc1), run_time=0.9)
        # lane 2: a fitted arrow crossing a gold divider
        self.at("Held out prediction")
        rng = np.random.default_rng(2)
        xs = np.linspace(-2.9, -0.4, 7)
        dots = VGroup(*[Dot([x, LY[1] - 0.45 + 0.3 * (x + 2.9) + 0.18 * rng.normal(), 0], radius=0.09, color=OUT) for x in xs])
        fit = Line([-3.0, LY[1] - 0.55, 0], [-0.3, LY[1] + 0.3, 0]).set_stroke(TEXT, 5)
        self.play(FadeIn(dots), Create(fit), run_time=0.9)
        div = DashedLine([1.5, LY[1] - 0.9, 0], [1.5, LY[1] + 0.9, 0], color=OPSIN, stroke_width=7)
        new = VGroup(*[bob(person(TEAL, 0.6).move_to([3.0 + 1.2 * k, LY[1] + 0.05, 0]), phase=k) for k in range(3)])
        self.at("travels to new people")
        arrw = Arrow([-0.2, LY[1] - 0.1, 0], [2.6, LY[1] + 0.05, 0], buff=0, color=TEXT, stroke_width=7)
        self.play(Create(div), run_time=0.5)
        self.play(GrowArrow(arrw), FadeIn(new), run_time=1.2)
        nl = lab("NEW PEOPLE", TEAL, 24).move_to([4.2, LY[1] - 0.68, 0])
        self.play(FadeIn(nl), run_time=0.4)
        # lane 3: a switch changes an outcome
        self.at("Causation asks")
        sw = ValueTracker(0)
        track = RoundedRectangle(corner_radius=0.27, width=1.2, height=0.54, stroke_color=OPSIN, stroke_width=4, fill_color=OPSIN, fill_opacity=0.2).move_to([-1.0, LY[2], 0])
        knob = always_redraw(lambda: Circle(radius=0.2, stroke_width=0, fill_color=OPSIN, fill_opacity=1).move_to([-1.0 - 0.33 + 0.66 * sw.get_value(), LY[2], 0]))
        cl = lab("CAUSE", OPSIN, 28).move_to([-2.5, LY[2], 0])
        gout = meter(2.0, LY[2] - 0.75, 1.5, 0.5, lambda: 0.2 + 0.6 * sw.get_value(), color=OUT)
        ol = lab("OUTCOME", OUT, 28).move_to([4.0, LY[2], 0])
        ar3 = Arrow([-0.2, LY[2], 0], [1.6, LY[2], 0], buff=0, color=OPSIN, stroke_width=6)
        self.play(FadeIn(cl), FadeIn(track), FadeIn(knob), FadeIn(gout), FadeIn(ol), GrowArrow(ar3), run_time=1.0)
        self.at("what changes")
        self.play(sw.animate.set_value(1), run_time=0.9)
        self.at("proposed cause is changed")
        self.play(sw.animate.set_value(0), run_time=0.7)
        self.play(sw.animate.set_value(1), run_time=0.7)
        self.at("Prediction alone")
        bridge = Arrow([-0.5, LY[1] - LH / 2, 0], [-0.5, LY[2] + LH / 2, 0], buff=0, color=ALT, stroke_width=10, max_tip_length_to_length_ratio=0.5)
        self.play(GrowArrow(bridge), run_time=1.0)
        self.play(sw.animate.set_value(0), run_time=0.8)
        self.at("that intervention")
        self.play(ShrinkToCenter(bridge), run_time=0.9)
        self.finish()


class S12Scope(W):
    def construct(self):
        clk = self.clk
        rs, ls = lane_rects()
        self.add(rs, ls)
        card_r = Rectangle(width=12.2, height=6.1, stroke_color=GREY, stroke_width=3, fill_color=TEXT, fill_opacity=0.06).move_to([0, 0.2, 0])
        self.play(FadeOut(ls), ReplacementTransform(rs, card_r), run_time=0.6)
        # base: the gold sample-size curve
        self.at("size the study")
        bx0, bx1, by0, by1 = -5.4, 5.4, -2.7, -0.95
        base = Line([bx0 - 0.3, by0, 0], [bx1 + 0.3, by0, 0]).set_stroke(TEXT, 4)
        ds = np.linspace(0.3, 1.5, 100)
        cv = VMobject(stroke_color=OPSIN, stroke_width=9)
        cv.set_points_as_corners([np.array([bx0 + (d - 0.3) / 1.2 * (bx1 - bx0), by0 + 0.05 + (by1 - by0) * min(nd(d), 175) / 175, 0]) for d in ds])
        self.play(Create(base), Create(cv), run_time=2.0)
        # middle: eight mouse units lock in
        self.at("keep observations")
        rng = np.random.default_rng(11)
        mm = rng.normal(0, 0.09, K).clip(-0.17, 0.17)
        mm = mm - mm.mean()
        units = VGroup()
        for i in range(K):
            x = -4.9 + 1.4 * i - 0.0
            x = -4.9 + 1.4 * i
            r = Rectangle(width=1.2, height=2.1, stroke_color=OPSIN, stroke_width=5, fill_color=TEXT, fill_opacity=0.06).move_to([x, 0.5, 0])
            mo = make_mouse(0.45, TEXT).move_to([x, 1.0, 0])
            sp = Dot(radius=0.13, color=OUT).move_to([x, 0.1 + 2.1 * mm[i], 0])
            units.add(VGroup(r, mo, sp))
        for u in units:
            u.shift(UP * 3.0)
        self.add(units)
        self.play(LaggedStart(*[u.animate.shift(DOWN * 3.0) for u in units], lag_ratio=0.12), run_time=2.2)
        self.at("report uncertainty")
        ib = Rectangle(width=11.2, height=0.5, stroke_color=OUT, stroke_width=3, fill_color=OUT, fill_opacity=0.4).move_to([0, 0.1, 0])
        self.play(GrowFromCenter(ib), run_time=1.2)
        # top: the three verbs click into slots
        self.at("match the final verb")
        slots = VGroup(*[Rectangle(width=3.6, height=1.0, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([x, 2.4, 0]) for x in (-4.0, 0, 4.0)])
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.25), run_time=1.5)
        verbs = [("ASSOCIATES", OUT), ("PREDICTS", FLUOR), ("CAUSES", OPSIN)]
        fills = []

        def click(i):
            t, c = verbs[i]
            f = VGroup(Rectangle(width=3.6, height=1.0, stroke_color=c, stroke_width=5, fill_color=c, fill_opacity=0.25).move_to(slots[i]),
                       lab(t, c, 34).move_to(slots[i]))
            fills.append(f)
            return f
        self.at("precise association")
        f0 = click(0)
        self.play(FadeIn(f0, scale=1.25), run_time=0.6)
        self.at("still an association")
        self.play(Indicate(f0, color=OUT, scale_factor=1.08), run_time=0.9)
        self.wait(0.4)
        f1 = click(1)
        self.play(FadeIn(f1, scale=1.25), run_time=0.6)
        self.at("causal claim")
        f2 = click(2)
        self.play(FadeIn(f2, scale=1.25), run_time=0.6)
        self.at("tested scope")
        scope = Rectangle(width=13.1, height=7.1, stroke_color=OUT, stroke_width=7).move_to([0, 0.1, 0])
        sl = lab("TESTED SCOPE", OUT, 30)
        sb = Rectangle(width=sl.width + 0.4, height=0.5, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0, -3.45, 0])
        sl.move_to(sb)
        sb.set_z_index(10)
        sl.set_z_index(11)
        self.play(Create(scope), run_time=1.3)
        self.play(FadeIn(sb), FadeIn(sl), run_time=0.5)
        self.at("Match the claim")
        self.play(Indicate(VGroup(card_r, scope), color=OPSIN, scale_factor=1.015), run_time=1.6)
        self.finish()


class S13End(EndCard):
    LINE = "Match the claim to the contrast and the sample."
