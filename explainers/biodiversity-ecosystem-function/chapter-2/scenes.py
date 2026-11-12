"""Ten Years at Cedar Creek: biodiversity and ecosystem function (chapter 2).

Same colour map as chapter 1 (dark ground): species A GOLD; B TEAL; others CORAL, SLATE, SAND;
complementarity GREEN; selection VIOLET; a plot's total = white OUTLINE; expected = DASHED grey bar.
Everything is labelled schematic unless computed.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403
from bp_style import SpokenScene, TitleCard, EndCard, NarratedScene, T, M, chip, GOLD, TEAL

CORAL = "#FF7F6B"
SLATE = "#7C8FE8"
SAND = "#E8D5A3"
VIOLET = "#B28DFF"
OUT = "#FFFFFF"
SP = [GOLD, TEAL, CORAL, SLATE, SAND]
BASE = -2.7
X5 = [-1.8, -0.05, 1.7, 3.45, 5.2]
SOIL = ["#6b4a2f", "#8a6a3f", "#4d3a28", "#a07a4a"]


def lerp(a, b, m):
    return a + (b - a) * m


# ---------------------------------------------------------------- shared pieces
def tuft(color, h=1.0, w=1.0):
    g = VGroup(*[Line(ORIGIN, [dx * w, hh * h, 0], color=color, stroke_width=5)
                 for dx, hh in [(-0.22, 0.7), (0, 1), (0.22, 0.85)]])
    base = Dot(ORIGIN, radius=0.001).set_opacity(0)
    g.add(base)
    g.base = base
    return g


def sway(g, amp=0.07, speed=1.5, phase=0.0):
    st = {"t": phase, "a": 0.0}

    def up(m, dt):
        st["t"] += dt
        a = amp * np.sin(speed * st["t"])
        m.rotate(a - st["a"], about_point=m.base.get_center())
        st["a"] = a
    g.add_updater(up)
    return g


def put(g, x, y):
    g.shift(np.array([x, y, 0]) - g.base.get_center())
    return g


def baseline(x0=-6.4, x1=6.4, y=BASE):
    strip = Rectangle(width=x1 - x0, height=y + 3.8, stroke_width=0, fill_color="#1c2e22", fill_opacity=1)
    strip.move_to([(x0 + x1) / 2, (y - 3.8) / 2, 0])
    return VGroup(strip, Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=3))


def name(text, x, color=TEXT, size=28, y=BASE - 0.45):
    return T(text, size, color).move_to([x, y, 0])


def tag(text, x=0.0, y=-3.62):
    return T(text, 22, GREY).move_to([x, y, 0])


def plot_box(cx, cy, size, n, colors, hs=None, seed=0, sw=True):
    box = Rectangle(width=size, height=size, stroke_color=GREY, stroke_width=3,
                    fill_color="#1b2a1f", fill_opacity=1).move_to([cx, cy, 0])
    rng = np.random.default_rng(seed)
    tufts = VGroup()
    sp = size / n
    for idx, c in enumerate(colors):
        i, j = divmod(idx, n)
        t = tuft(c, h=(hs[idx] if hs else 0.5 * sp + 0.15 * sp * rng.random()) , w=sp * 0.9)
        put(t, cx + (j - (n - 1) / 2) * sp, cy + ((n - 1) / 2 - i) * sp - sp * 0.4)
        if sw:
            sway(t, phase=rng.random() * 6)
        tufts.add(t)
    return box, tufts


def mix_bars(x, k, w=1.9):
    ga = Rectangle(width=w, height=300 * k, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.55)
    ga.move_to([x, BASE + 150 * k, 0])
    gb = Rectangle(width=w, height=100 * k, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.55)
    gb.move_to([x, BASE + 350 * k, 0])
    ol = Rectangle(width=w + 0.08, height=400 * k, stroke_color=OUT, stroke_width=6).move_to([x, BASE + 200 * k, 0])
    return VGroup(ga, gb, ol)


def dashed_bar(x, k, v=250, w=1.9):
    r = Rectangle(width=w, height=v * k).move_to([x, BASE + v * k / 2, 0])
    d = DashedVMobject(r, num_dashes=40).set_stroke(GREY, 4)
    fill = Rectangle(width=w, height=v * k, stroke_width=0, fill_color=GREY, fill_opacity=0.12).move_to(r)
    return VGroup(fill, d)


def brk(x, y0, y1, color=YELLOW):
    return VGroup(Line([x, y0, 0], [x, y1, 0]), Line([x - 0.15, y0, 0], [x, y0, 0]),
                  Line([x - 0.15, y1, 0], [x, y1, 0])).set_stroke(color, 5)


def die(x, y):
    sq = RoundedRectangle(corner_radius=0.12, width=0.8, height=0.8, stroke_color=TEXT, stroke_width=3,
                          fill_color=BG, fill_opacity=1)
    dots = VGroup(*[Dot([dx, dy, 0], radius=0.06, color=TEXT) for dx, dy in
                    [(-0.2, 0.2), (0.2, 0.2), (0, 0), (-0.2, -0.2), (0.2, -0.2)]])
    g = VGroup(sq, dots).move_to([x, y, 0])
    return g


def grid_plots(cx, cy, cell, cols=14, rows=12):
    sq = VGroup()
    for r in range(rows):
        for c in range(cols):
            s = Square(cell * 0.88, stroke_color=GREY, stroke_width=1.5, fill_color="#1b2a1f", fill_opacity=1)
            s.move_to([cx + (c - (cols - 1) / 2) * cell, cy + ((rows - 1) / 2 - r) * cell, 0])
            sq.add(s)
    return sq


def year_text(t, x, y, size=44, color=YELLOW):
    return always_redraw(lambda: M(str(1996 + min(int(t.get_value()), 9)), size, color).move_to([x, y, 0]))


# ---------------------------------------------------------------- split chart data (schematic)
SEL = np.array([1.0, 0.8, 0.5, 0.2, -0.2, -0.6, -1.0, -1.4, -1.8, -2.1])
COMP = np.array([0.2, 0.4, 0.7, 1.0, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3])
ZY = 0.4
U = 0.95
CX0, CXS, CBW = 0.4, 0.62, 0.26


def rect_v(x, v, color, w=CBW, u=U, zy=ZY):
    h = max(abs(v) * u, 0.001)
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.8)
    r.move_to([x, zy + np.sign(v if v != 0 else 1) * h / 2, 0])
    return r


def pair(i):
    x = CX0 + CXS * i
    return VGroup(rect_v(x - 0.15, COMP[i], GREEN), rect_v(x + 0.15, SEL[i], VIOLET))


def split_chart(ug, uv):
    def f():
        g = VGroup()
        for i in range(10):
            x = CX0 + CXS * i
            a = float(np.clip(ug.get_value() - i, 0, 1))
            b = float(np.clip(uv.get_value() - i, 0, 1))
            if a > 0.01:
                g.add(rect_v(x - 0.15, COMP[i] * a, GREEN))
            if b > 0.01:
                g.add(rect_v(x + 0.15, SEL[i] * b, VIOLET))
        if len(g) == 0:
            g.add(Dot([0, 0, 0], radius=0.001).set_opacity(0))
        return g
    return always_redraw(f)


def chart_axes():
    z = Line([-0.3, ZY, 0], [6.5, ZY, 0], color=GREY, stroke_width=3)
    zl = T("0", 26, GREY).move_to([-0.6, ZY, 0])
    y0 = T("1996", 28, TEXT).move_to([CX0, -2.3, 0])
    y1 = T("2005", 28, TEXT).move_to([CX0 + 9 * CXS, -2.3, 0])
    ar = Arrow([CX0 + 0.75, -2.3, 0], [CX0 + 9 * CXS - 0.75, -2.3, 0], color=GREY, stroke_width=3, buff=0,
               max_tip_length_to_length_ratio=0.1)
    return VGroup(z, zl, y0, y1, ar)


def legend():
    return VGroup(T("complementarity", 30, GREEN).move_to([1.0, 3.3, 0]),
                  T("selection", 30, VIOLET).move_to([4.5, 3.3, 0]))


# ---------------------------------------------------------------- species fluctuation world (s10-s15)
def _make_z(n=6):
    rng = np.random.default_rng(23)
    best = None
    for _ in range(20000):
        rows = []
        for _i in range(n):
            v = rng.standard_normal(10)
            v -= v.mean()
            for r in rows:
                v -= (v @ r) / (r @ r) * r
            rows.append(v)
        Zs = [r / np.sqrt((r @ r) / 10) for r in rows]
        m = max(abs(z).max() for z in Zs)
        if best is None or m < best[0]:
            best = (m, Zs)
        if m < 2.0:
            break
    return best[1]


Z = _make_z()
XB = [-5.4, -4.5, -3.6, -2.7, -1.8]
XSTACK, WSTACK = -2.6, 3.0
XMONO = 3.4
KS, KT = 0.04, 0.012
MEAN_S = 55.0


def zval(row, t):
    i0 = int(t) % 10
    i1 = (i0 + 1) % 10
    f = t - int(t)
    f = f * f * (3 - 2 * f)
    return Z[row][i0] * (1 - f) + Z[row][i1] * f


class World:
    def __init__(self, xs=XSTACK):
        self.xs = xs
        self.t = ValueTracker(0.0)
        self.speed = 0.0
        self.nsp = ValueTracker(0.0)
        self.merge = ValueTracker(0.0)
        self.ol = ValueTracker(0.0)
        self.mono_on = ValueTracker(0.0)
        self.mono_m = ValueTracker(0.0)   # 0: one species bar, 1: whole monoculture total

        def up(m, dt):
            m.set_value((m.get_value() + dt * self.speed) % 10)
        self.t.add_updater(up)

    def add_to(self, scene):
        scene.add(self.t, self.nsp, self.merge, self.ol, self.mono_on, self.mono_m)

    def vals(self):
        t = self.t.get_value()
        return [MEAN_S * (1 + 0.45 * zval(i, t)) for i in range(5)]

    def species(self):
        def f():
            g = VGroup()
            m = self.merge.get_value()
            n = self.nsp.get_value()
            k = lerp(KS, KT, m)
            vs = self.vals()
            run = 0.0
            for i, (v, c) in enumerate(zip(vs, SP)):
                a = float(np.clip(n - i, 0, 1))
                h = max(v * k * a, 0.001)
                x = lerp(XB[i], self.xs, m)
                w = lerp(0.7, WSTACK, m)
                bot = BASE + m * run
                r = Rectangle(width=w, height=h, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.7)
                r.move_to([x, bot + h / 2, 0])
                g.add(r)
                run += v * k * a
            if self.ol.get_value() > 0.5:
                g.add(Rectangle(width=WSTACK + 0.08, height=run, stroke_color=OUT, stroke_width=6)
                      .move_to([self.xs, BASE + run / 2, 0]))
            return g
        return always_redraw(f)

    def mono(self):
        def f():
            if self.mono_on.get_value() < 0.5:
                return VGroup(Dot([0, 0, 0], radius=0.001).set_opacity(0))
            m = self.mono_m.get_value()
            mean = lerp(MEAN_S, 275.0, m)
            k = lerp(KS, KT, m)
            w = lerp(1.2, WSTACK, m)
            v = mean * (1 + 0.30 * zval(5, self.t.get_value()))
            h = v * k
            r = Rectangle(width=w, height=h, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.7)
            r.move_to([XMONO, BASE + h / 2, 0])
            return r
        return always_redraw(f)


def means_lines():
    ls = VGroup()
    for x in XB:
        ls.add(DashedLine([x - 0.5, BASE + MEAN_S * KS, 0], [x + 0.5, BASE + MEAN_S * KS, 0], color=TEXT, stroke_width=2.5))
    return ls


# ================================================================ scenes
class S00Title(TitleCard):
    TITLE = "Ten Years at Cedar Creek"
    LESSON = "Biodiversity and Ecosystem Function"


class S01Link(SpokenScene):
    def construct(self):
        k = 0.0105
        mix = mix_bars(-4.2, k)
        self.play(GrowFromEdge(mix, DOWN), run_time=0.8)
        n1 = name("mixture", -4.2)
        bl0 = baseline(-6.4, 1.0)
        self.add(bl0)
        self.play(FadeIn(n1), run_time=0.2)
        self.at("a field as a sum")
        self.play(Indicate(mix[2], color=OUT, scale_factor=1.04), run_time=1.0)
        self.at("follow one real field")
        dsh = dashed_bar(-1.9, k)
        n2 = name("expected", -1.9)
        self.play(FadeIn(dsh), FadeIn(n2), run_time=1.2)
        self.at("how much of its extra yield")
        y0, y1 = BASE + 250 * k, BASE + 400 * k
        b = brk(-0.8, y0, y1)
        ex = T("extra yield", 32, YELLOW).move_to([0.9, (y0 + y1) / 2, 0])
        self.play(Create(b), FadeIn(ex), run_time=1.0)
        self.at("complementarity")
        ym = (y0 + y1) / 2
        bg = brk(-0.8, y0, ym, GREEN)
        bv = brk(-0.8, ym, y1, VIOLET)
        lg = T("complementarity", 32, GREEN).move_to([1.2, (y0 + ym) / 2, 0])
        self.play(FadeOut(b), FadeOut(ex), Create(bg), Create(bv), FadeIn(lg), run_time=1.0)
        self.at("how much is selection")
        lv = T("selection", 32, VIOLET).move_to([0.55, (ym + y1) / 2 + 0.15, 0])
        self.play(FadeIn(lv), run_time=0.8)
        q = T("?", 90, YELLOW).move_to([4.6, 0.4, 0])
        self.play(FadeIn(q, scale=1.6), run_time=0.8)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.at("Does the answer")
        t = ValueTracker(0.0)
        t.add_updater(lambda m, dt: m.increment_value(dt * 0.9))
        self.add(t)
        grid = grid_plots(1.5, -0.1, 0.42)
        yr = year_text(t, 4.2, 3.2, 40)
        self.play(FadeOut(VGroup(mix, n1, dsh, n2, bg, bv, lg, lv, q, bl0)), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.004, run_time=1.6), FadeIn(yr))
        self.finish()


MN = [(-97.2, 49.0), (-95.15, 49.0), (-95.15, 49.4), (-94.6, 48.7), (-93.0, 48.6), (-91.5, 48.1), (-89.6, 48.0),
      (-92.1, 46.75), (-92.3, 46.1), (-92.8, 45.6), (-92.75, 44.75), (-91.2, 43.5), (-96.45, 43.5),
      (-96.45, 45.3), (-96.6, 45.8), (-96.85, 46.6)]


def proj(lon, lat):
    return np.array([(lon + 93.9) * 0.6 - 4.4, (lat - 46.25) * 0.95, 0])


class S02Site(SpokenScene):
    def construct(self):
        mn = Polygon(*[proj(*p) for p in MN], stroke_color=GREY, stroke_width=4, fill_color="#1b2a1f", fill_opacity=1)
        self.play(Create(mn), run_time=0.6)
        self.at("Cedar Creek")
        pp = proj(-93.2, 45.4)
        pin = VGroup(Triangle(color=YELLOW, fill_opacity=1).rotate(PI).scale(0.2).move_to(pp + UP * 0.2),
                     Circle(0.2, color=YELLOW, fill_opacity=1).move_to(pp + UP * 0.55))
        lab = T("Cedar Creek", 32, YELLOW).move_to(pp + RIGHT * 1.9 + DOWN * 0.1)
        self.play(FadeIn(pin, shift=DOWN * 0.5), FadeIn(lab), run_time=0.8)
        self.at("Minnesota")
        mnl = T("Minnesota", 30, TEXT).move_to([-5.0, 2.0, 0])
        self.play(FadeIn(mnl), run_time=0.6)
        self.at("spring 1994")
        t_d = T("sown spring 1994", 28, TEXT).move_to([3.1, 3.25, 0])
        self.play(FadeIn(t_d), run_time=0.6)
        grid = grid_plots(3.1, -0.1, 0.44)
        cnt = ValueTracker(0.0)
        self.add(cnt)
        ct = always_redraw(lambda: T(f"{int(cnt.get_value())} plots", 36, YELLOW).move_to([5.0, -3.3, 0]))
        self.add(ct)
        self.at("David")
        nm = T("David Tilman and colleagues", 28, TEXT).move_to([-3.2, -3.3, 0])
        self.play(FadeIn(nm), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.02, run_time=3.6),
                  cnt.animate(run_time=3.6, rate_func=linear).set_value(168))
        self.at("Each plot was")
        hi = grid[12 * 14 // 14 * 14 - 14].copy() if False else grid[154].copy()
        hi.set_stroke(YELLOW, 5).set_fill(YELLOW, 0.25)
        each = T("each 9 m by 9 m", 28, YELLOW).move_to([1.2, -3.3, 0])
        self.play(FadeIn(hi), FadeIn(each), run_time=0.6)
        self.play(Indicate(hi, color=YELLOW, scale_factor=1.6), run_time=1.0)
        self.add(tag("schematic", x=-0.8, y=3.25))
        self.finish()


def species_hop_targets(cx, cy, size, n):
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n / cols))
    sp = size / cols
    out = []
    for idx in range(n):
        r, c = divmod(idx, cols)
        out.append((cx + (c - (cols - 1) / 2) * sp, cy + ((rows - 1) / 2 - r) * sp - sp * 0.42))
    return out, sp


class S03Draw(SpokenScene):
    def construct(self):
        PY, PS = -0.2, 1.5
        boxes = VGroup(*[Rectangle(width=PS, height=PS, stroke_color=GREY, stroke_width=3, fill_color="#1b2a1f",
                                   fill_opacity=1).move_to([x, PY, 0]) for x in X5])
        self.play(FadeIn(boxes), run_time=0.8)
        for w, x in zip(["one", "two", "four", "eight", "16"], X5):
            self.at(w + " " if False else w)
            self.play(FadeIn(T({"one": "1", "two": "2", "four": "4", "eight": "8", "16": "16"}[w], 36, YELLOW)
                             .move_to([x, PY - 1.2, 0]), scale=1.3), run_time=0.35)
        self.at("They were drawn at random")
        dd = die(-4.6, -0.9)
        dt = ValueTracker(0)
        dd.add_updater(lambda m, dt: m.rotate(dt * 5))
        self.play(FadeIn(dd), run_time=0.5)
        self.at("a pool of 18")
        tray = VGroup()
        for i in range(18):
            r, c = divmod(i, 6)
            t = tuft(SP[i % 5], h=0.55 + 0.12 * ((i * 7) % 4), w=0.7)
            put(t, -5.75 + 0.46 * c + 0.2, 1.7 - 0.5 * r)
            tray.add(t)
        tl = T("18 species", 30, TEXT).move_to([-4.6, 2.75, 0])
        self.play(FadeIn(tray, lag_ratio=0.03), FadeIn(tl), run_time=1.2)
        self.at("grassland and savannah")
        anims = []
        idx = 0
        for x, n in zip(X5, [1, 2, 4, 8, 16]):
            tg, sp = species_hop_targets(x, PY, PS * 0.9, n)
            s = {1: 0.9, 2: 0.7, 4: 0.55, 8: 0.42, 16: 0.34}[n]
            for (tx, ty) in tg:
                c = tray[idx % 18].copy()
                c.clear_updaters()
                self.add(c)
                bc = c.base.get_center()
                anims.append(c.animate.scale(s, about_point=bc).shift(np.array([tx, ty, 0]) - bc))
                idx += 1
        dd.clear_updaters()
        self.play(LaggedStart(*anims, lag_ratio=0.06, run_time=3.0), FadeOut(dd, run_time=0.5))
        self.at("Every plot got the same")
        bags = VGroup()
        for x in X5:
            bag = VGroup(RoundedRectangle(corner_radius=0.15, width=0.55, height=0.5, stroke_color=SAND, stroke_width=3,
                                          fill_color=SAND, fill_opacity=0.6),
                         Line([-0.2, 0.25, 0], [0.2, 0.25, 0], color=SAND, stroke_width=5)).move_to([x, 1.9, 0])
            bags.add(bag)
        self.play(FadeIn(bags, lag_ratio=0.1), run_time=0.8)
        self.play(LaggedStart(*[b.animate.shift(DOWN * 1.15) for b in bags], lag_ratio=0.15, run_time=1.4))
        sl = T("same seed mass in every plot", 32, SAND).move_to([1.7, -2.7, 0])
        self.play(FadeIn(sl), run_time=0.6)
        self.add(tag("schematic", x=5.5, y=-3.4))
        self.finish()


class S04Why(SpokenScene):
    def construct(self):
        rows = [1.9, 0.75, -0.4, -1.55]
        sq = VGroup()
        for x in X5:
            for y in rows:
                sq.add(Square(1.0, stroke_color=GREY, stroke_width=2.5, fill_color="#1b2a1f", fill_opacity=1).move_to([x, y, 0]))
        heads = VGroup(*[T(s, 34, YELLOW).move_to([x, 2.95, 0]) for x, s in zip(X5, ["1", "2", "4", "8", "16"])])
        dd = die(-4.5, 2.0)
        dd.add_updater(lambda m, dt: m.rotate(dt * 5))
        self.play(LaggedStart(*[FadeIn(s) for s in sq], lag_ratio=0.03, run_time=1.4), FadeIn(heads), FadeIn(dd))
        self.at("nobody chose")
        dd.clear_updaters()
        self.play(FadeOut(dd), run_time=0.3)
        big = put(tuft(GOLD, 1.5, 1.4), -5.3, -0.2)
        sway(big)
        palm = RoundedRectangle(corner_radius=0.1, width=0.7, height=0.6, stroke_color=SAND, stroke_width=3,
                                fill_color=SAND, fill_opacity=0.3)
        fing = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.14, height=0.45, stroke_color=SAND, stroke_width=2,
                                         fill_color=SAND, fill_opacity=0.3).move_to([dx, 0.45, 0]) for dx in (-0.25, -0.08, 0.09, 0.26)])
        hand = VGroup(palm, fing).move_to([-5.3, 1.5, 0])
        self.play(FadeIn(big), FadeIn(hand, shift=DOWN * 0.4), run_time=0.5)
        self.play(VGroup(hand, big).animate.shift(RIGHT * 1.6 + DOWN * 0.2), run_time=0.9)
        self.at("rich plots")
        cross = VGroup(Line([-4.5, 1.9, 0], [-2.9, -0.7, 0]), Line([-4.5, -0.7, 0], [-2.9, 1.9, 0])).set_stroke(RED, 8)
        nl = T("nobody chose strong\nspecies", 28, TEXT, line_spacing=0.8).move_to([-4.6, -2.0, 0])
        self.play(Create(cross), FadeIn(nl), run_time=0.9)
        self.at("Better soil")
        self.play(FadeOut(VGroup(hand, big, cross, nl)), run_time=0.3)
        rng = np.random.default_rng(5)
        self.play(*[s.animate.set_fill(SOIL[rng.integers(0, 4)], 1) for s in sq], run_time=0.9)
        self.at("line up with richness")
        sl = T("soil not\nsystematically\naligned with\nrichness", 30, TEXT, line_spacing=0.8).move_to([-4.9, 0.3, 0])
        self.play(FadeIn(sl, shift=RIGHT * 0.3), run_time=0.8)
        self.add(tag("schematic", x=5.5, y=-3.4))
        self.finish()


TOT = [150, 225, 290, 340, 385]
KB = 0.0135
NSEG = [1, 2, 4, 8, 16]


def seg_cols(n):
    return [SP[i % 5] for i in range(n)]


def rise_bars(t, grow):
    def f():
        g = VGroup()
        tt = t.get_value()
        gr = grow.get_value()
        for i, (x, tot, n) in enumerate(zip(X5, TOT, NSEG)):
            v = tot * (1 + 0.06 * np.sin(0.9 * tt * 1.6 + i * 1.3)) * gr
            h = v * KB
            y = BASE
            for c in seg_cols(n):
                sh = h / n
                r = Rectangle(width=1.3, height=max(sh, 0.001), stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.7)
                r.move_to([x, y + sh / 2, 0])
                g.add(r)
                y += sh
            g.add(Rectangle(width=1.38, height=max(h, 0.001), stroke_color=OUT, stroke_width=5).move_to([x, BASE + h / 2, 0]))
        return g
    return always_redraw(f)


def tools_icons():
    sh = VGroup(Line([-.3, .35, 0], [.3, -.35, 0]), Line([-.3, -.35, 0], [.3, .35, 0])).set_stroke(SAND, 5)
    sh.add(Circle(0.12, color=SAND).move_to([-.3, -.35, 0]), Circle(0.12, color=SAND).move_to([.3, -.35, 0]))
    ov = VGroup(RoundedRectangle(corner_radius=0.1, width=0.9, height=0.75, stroke_color=CORAL, stroke_width=4),
                *[Line([dx, -.15, 0], [dx, .15, 0]).set_stroke(CORAL, 4) for dx in (-.25, 0, .25)])
    pan = VGroup(Line([-.45, .2, 0], [.45, .2, 0]), Triangle().scale(0.2).move_to([0, -.15, 0]),
                 Arc(radius=.2, start_angle=PI, angle=PI).move_to([-.4, .0, 0]).rotate(PI),
                 Arc(radius=.2, start_angle=PI, angle=PI).move_to([.4, .0, 0]).rotate(PI)).set_stroke(TEAL, 4)
    return sh, ov, pan


class S05Rise(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        t.add_updater(lambda m, dt: m.set_value(min(m.get_value() + dt * 9 / 8.8, 9.0)))
        grow = ValueTracker(0.0)
        self.add(t, grow, baseline(-3.2, 6.2))
        bars = rise_bars(t, grow)
        nums = VGroup(*[T(s, 32, TEXT).move_to([x, BASE - 0.45, 0]) for x, s in zip(X5, ["1", "2", "4", "8", "16"])])
        yr = year_text(t, -5.0, 3.2)
        self.add(bars, nums, yr)
        self.play(grow.animate.set_value(1.0), run_time=1.0)
        self.at("clipped")
        sh, ov, pan = tools_icons()
        sh.move_to([-5.4, 1.6, 0])
        ov.move_to([-5.4, 0.2, 0])
        pan.move_to([-5.4, -1.2, 0])
        w1 = T("clip", 30).move_to([-4.0, 1.6, 0])
        w2 = T("dry", 30).move_to([-4.0, 0.2, 0])
        w3 = T("weigh", 30).move_to([-3.95, -1.2, 0])
        self.play(FadeIn(sh, shift=RIGHT * 0.3), FadeIn(w1), Rotate(sh, angle=0.3, rate_func=there_and_back), run_time=0.8)
        self.at("dried")
        self.play(FadeIn(ov, shift=RIGHT * 0.3), FadeIn(w2), run_time=0.7)
        self.at("weighed")
        self.play(FadeIn(pan, shift=RIGHT * 0.3), FadeIn(w3), Rotate(pan, angle=0.15, rate_func=there_and_back), run_time=0.9)
        self.at("Year after year")
        self.play(FadeOut(VGroup(sh, ov, pan, w1, w2, w3)), run_time=0.6)
        self.at("more species")
        ar = Arrow([X5[0] - 0.5, BASE + TOT[0] * KB + 0.35, 0], [X5[4] - 0.5, BASE + TOT[4] * KB + 0.35, 0],
                   color=YELLOW, stroke_width=6, buff=0)
        ms = T("more species", 30, YELLOW).move_to([-5.2, 0.9, 0])
        self.play(Create(ar), FadeIn(ms), run_time=1.2)
        self.at("above ground biomass")
        yl = T("aboveground biomass", 28, TEXT).rotate(PI / 2).move_to([-3.1, 0.0, 0])
        self.play(FadeIn(yl), run_time=0.7)
        self.add(tag("schematic, not data", x=-5.3, y=-3.4))
        self.finish()


def left_bars():
    k = 0.0105
    mix = mix_bars(-4.4, k, 1.6)
    dsh = dashed_bar(-2.3, k, 250, 1.6)
    ym = BASE + 325 * k
    g = Rectangle(width=1.6, height=75 * k, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.7)
    g.move_to([-2.3, BASE + 287.5 * k, 0])
    v = Rectangle(width=1.6, height=75 * k, stroke_color=VIOLET, stroke_width=3, fill_color=VIOLET, fill_opacity=0.7)
    v.move_to([-2.3, BASE + 362.5 * k, 0])
    return VGroup(mix, dsh, g, v), g, v


class S06Split(SpokenScene):
    def construct(self):
        nm = T("Fargione and colleagues, 2007", 30, TEXT).move_to([-3.1, 3.3, 0])
        self.add(baseline(-6.4, -0.9))
        self.play(FadeIn(nm, shift=DOWN * 0.2), run_time=0.8)
        self.at("split the extra yield")
        lb, g, v = left_bars()
        self.play(FadeIn(lb[0]), FadeIn(lb[1]), run_time=1.0)
        self.play(FadeIn(g), FadeIn(v), run_time=0.8)
        self.at("mixture")
        n1 = name("mixture", -4.4)
        self.play(FadeIn(n1), run_time=0.5)
        self.at("alone")
        n2 = name("alone (expected)", -2.3)
        n2.shift(RIGHT * 0.3)
        self.play(FadeIn(n2), run_time=0.6)
        self.play(FadeOut(nm), run_time=0.4)
        ug, uv = ValueTracker(0.0), ValueTracker(0.0)
        self.add(ug, uv)
        ax = chart_axes()
        ch = split_chart(ug, uv)
        self.play(FadeIn(ax), run_time=0.8)
        self.add(ch)
        self.at("The green bar")
        lg = T("complementarity", 30, GREEN).move_to([1.0, 3.3, 0])
        self.play(Indicate(g, color=GREEN, scale_factor=1.1), FadeIn(lg), ug.animate.set_value(10.0), run_time=3.0)
        self.at("The violet bar")
        lv = T("selection", 30, VIOLET).move_to([4.5, 3.3, 0])
        self.play(Indicate(v, color=VIOLET, scale_factor=1.1), FadeIn(lv), uv.animate.set_value(10.0), run_time=2.2)
        self.add(tag("schematic: direction of change only", x=3.0, y=-3.4))
        self.finish()


def plot16(cx, cy, size=3.2, big=5):
    cols = [SP[i % 5] for i in range(16)]
    hs = [0.55 * size / 4 + 0.1] * 16
    box, tufts = plot_box(cx, cy, size, 4, cols, hs=hs, seed=3)
    bigt = tufts[big]
    return box, tufts, bigt


class S07Early(SpokenScene):
    def construct(self):
        ug, uv = ValueTracker(0.0), ValueTracker(0.0)
        self.add(ug, uv)
        ax = chart_axes()
        ch = split_chart(ug, uv)
        lg = legend()
        self.add(ax, ch, lg)
        lab = T("early: selection positive", 30, VIOLET).move_to([3.2, -3.1, 0])
        box, tufts, bigt = plot16(-3.9, 0.0)
        rl = T("rich plot", 28, TEXT).move_to([-3.9, -2.2, 0])
        self.add(tufts)
        self.play(ug.animate.set_value(4.0), uv.animate.set_value(4.0), FadeIn(box), FadeIn(rl), run_time=2.4, rate_func=linear)
        self.play(FadeIn(lab), run_time=0.5)
        self.at("Rich plots out yielded")
        self.at("productive species")
        glow = Circle(0.55, stroke_width=0, fill_color=YELLOW, fill_opacity=0.35).move_to(bigt.get_center() + UP * 0.2)
        self.add(glow)
        bigt.scale(1.7, about_point=bigt.base.get_center())
        tm = ValueTracker(0)
        glow.add_updater(lambda m, dt: (tm.increment_value(dt), m.set_fill(YELLOW, 0.25 + 0.2 * np.sin(4 * tm.get_value()))))
        pl = T("productive species", 28, YELLOW).move_to([-3.9, 2.2, 0])
        self.play(FadeIn(pl), Indicate(bigt, color=YELLOW, scale_factor=1.2), run_time=1.2)
        self.add(tag("schematic", x=-3.9, y=-3.4))
        self.finish()


class S08Shift(SpokenScene):
    def construct(self):
        ug, uv = ValueTracker(4.0), ValueTracker(4.0)
        self.add(ug, uv)
        ax = chart_axes()
        ch = split_chart(ug, uv)
        lg = legend()
        self.add(ax, ch, lg)
        box, tufts, bigt = plot16(-3.9, 0.0)
        bigt.scale(1.7, about_point=bigt.base.get_center())
        self.add(box, tufts)
        self.play(ug.animate.set_value(6.0), uv.animate.set_value(6.0), bigt.animate.scale(0.8, about_point=bigt.base.get_center()),
                  run_time=3.7, rate_func=linear)
        self.at("Selection shrank")
        self.play(ug.animate.set_value(10.0), uv.animate.set_value(10.0), bigt.animate.scale(0.6, about_point=bigt.base.get_center()),
                  run_time=2.0, rate_func=linear)
        self.at("ended strongly negative")
        lb = T("by 2005: selection\nstrongly negative", 28, VIOLET, line_spacing=0.8).move_to([3.3, -3.05, 0])
        self.play(FadeIn(lb), run_time=0.6)
        self.at("the biggest gains")
        self.play(FadeOut(VGroup(box, tufts)), run_time=0.5)
        small = put(tuft(CORAL, 0.35, 0.8), -5.3, -0.9)
        big = put(tuft(CORAL, 1.7, 1.4), -2.9, -0.9)
        sway(big)
        arr = Arrow([-4.6, -0.6, 0], [-3.6, 0.3, 0], color=YELLOW, buff=0, stroke_width=6)
        a1 = T("alone", 28).move_to([-5.3, -1.45, 0])
        a2 = T("in mixture", 28).move_to([-2.9, -1.45, 0])
        gl = T("biggest gains:\nspecies small alone", 28, TEXT, line_spacing=0.8).move_to([-4.1, 1.9, 0])
        self.play(FadeIn(small), FadeIn(a1), FadeIn(gl), run_time=0.8)
        self.play(GrowFromPoint(big, big.base.get_center()), FadeIn(arr), FadeIn(a2), run_time=1.4)
        self.at("associated with")
        self.play(FadeOut(VGroup(small, big, arr, a1, a2, gl)), run_time=0.5)
        pl = put(tuft(GREEN, 1.4, 1.4), -4.4, -0.8)
        sway(pl)
        nn = VGroup(Circle(0.38, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.2),
                    T("N", 34, YELLOW)).move_to([-3.4, 0.4, 0])
        nl = T("associated with more\nplant nitrogen", 28, TEXT, line_spacing=0.8).move_to([-4.2, 1.9, 0])
        self.play(GrowFromPoint(pl, pl.base.get_center()), FadeIn(nn, scale=1.5), FadeIn(nl), run_time=1.2)
        self.play(Indicate(nn, color=YELLOW, scale_factor=1.3), run_time=1.0)
        self.add(tag("schematic", x=-4.2, y=-3.4))
        self.finish()


class S09Years(SpokenScene):
    def construct(self):
        ax = chart_axes()
        pairs = [pair(i) for i in range(10)]
        allp = VGroup(*pairs)
        lg = legend()
        self.add(ax, allp, lg)
        self.wait(0.5)
        self.at("depending on which years")
        e = SurroundingRectangle(pairs[0], color=YELLOW, buff=0.1, stroke_width=4)
        l = SurroundingRectangle(pairs[9], color=YELLOW, buff=0.1, stroke_width=4)
        self.play(Create(e), Create(l), run_time=1.0)
        self.at("Each year's split")
        # big snapshots
        def snap(cx, ci):
            return VGroup(rect_v(cx - 0.55, COMP[ci], GREEN, w=0.9, u=1.0), rect_v(cx + 0.55, SEL[ci], VIOLET, w=0.9, u=1.0))
        s1, s2 = snap(-3.0, 0), snap(3.4, 9)
        z1 = Line([-4.5, ZY, 0], [-1.5, ZY, 0], color=GREY, stroke_width=3)
        z2 = Line([1.9, ZY, 0], [4.9, ZY, 0], color=GREY, stroke_width=3)
        rest = VGroup(*pairs[1:9])
        self.play(FadeOut(rest), FadeOut(e), FadeOut(l), FadeOut(ax), FadeOut(lg[0]), FadeOut(lg[1]), run_time=0.6) if False else None
        self.play(FadeOut(rest), FadeOut(e), FadeOut(l), FadeOut(ax), run_time=0.4)
        self.play(ReplacementTransform(pairs[0], s1), ReplacementTransform(pairs[9], s2), FadeIn(z1), FadeIn(z2), run_time=1.1)
        n1 = T("early years", 32, TEXT).move_to([-3.0, -2.5, 0])
        n2 = T("late years", 32, TEXT).move_to([3.4, -2.5, 0])
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.4)
        self.at("snapshots changed")
        self.play(Indicate(s1[1], color=VIOLET, scale_factor=1.2), Indicate(s2[1], color=VIOLET, scale_factor=1.2), run_time=1.2)
        self.add(tag("schematic", x=0.2, y=-3.4))
        self.finish()


class S10Zoom(SpokenScene):
    def construct(self):
        W = World()
        W.speed = 1.0
        W.add_to(self)
        box, tufts, _ = plot16(-3.6, 0.0, 3.4)
        self.play(FadeIn(box), run_time=0.5)
        self.add(tufts)
        self.at("zoom")
        self.play(VGroup(box, tufts).animate.scale(1.25), run_time=1.6)
        self.at("follow their species")
        self.add(W.species(), baseline(-6.4, 0.6))
        self.play(FadeOut(VGroup(box, tufts)), W.nsp.animate.set_value(5.0), run_time=1.8)
        hd = T("16-species plot", 30, TEXT).move_to([-3.6, 2.3, 0])
        self.play(FadeIn(hd), FadeIn(means_lines()), run_time=0.6)
        self.at("proportionally more")
        lab = T("species, on average: less steady in rich plots", 30, YELLOW).move_to([0, 3.3, 0])
        self.play(FadeIn(lab), run_time=0.8)
        self.at("than species in poorer plots")
        W.mono_on.set_value(1.0)
        self.add(W.mono(), baseline(2.0, 6.4))
        h2 = T("1-species plot", 30, TEXT).move_to([XMONO, 2.3, 0])
        self.play(FadeIn(h2), run_time=0.8)
        self.add(tag("schematic", x=-1.0, y=-3.55))
        self.finish()


def static_world(W, merge=1.0, ol=1.0, mono=1.0, mono_m=1.0, t=3.0):
    W.t.set_value(t)
    W.nsp.set_value(5.0)
    W.merge.set_value(merge)
    W.ol.set_value(ol)
    W.mono_on.set_value(mono)
    W.mono_m.set_value(mono_m)


class S11Predict(SpokenScene):
    def construct(self):
        W = World()
        W.speed = 1.0
        W.t.set_value(4.0)
        W.nsp.set_value(5.0)
        W.mono_on.set_value(1.0)
        W.add_to(self)
        ml = means_lines()
        self.add(W.species(), W.mono(), baseline(-6.4, 0.6), baseline(2.0, 6.4), ml)
        hd = T("16-species plot", 30, TEXT).move_to([-3.6, 2.3, 0])
        h2 = T("1-species plot", 30, TEXT).move_to([XMONO, 2.3, 0])
        self.add(hd, h2)
        self.wait(1.0)
        self.at("Will the")
        W.speed = 0.4
        self.play(FadeOut(hd), FadeOut(h2), FadeOut(ml), W.merge.animate.set_value(1.0), W.mono_m.animate.set_value(1.0),
                  W.ol.animate.set_value(1.0), run_time=1.0)
        self.remove(*[m for m in self.mobjects if isinstance(m, Line) and not isinstance(m, DashedLine) and m.get_length() < 9
                      and abs(m.get_start()[1] - BASE) < 0.01])
        self.add(baseline(-6.4, 6.4))
        n1 = name("16-species plot total", XSTACK, TEXT)
        n2 = name("monoculture", XMONO, TEXT)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.3)
        self.at("more steady")
        c1 = chip("more steady", BLUE, 28).move_to([0.4, 0.8, 0])
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        self.at("less steady", nth=1)
        c2 = chip("less steady", RED, 28).move_to([0.4, -0.4, 0])
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        self.add(tag("schematic", x=-4.8, y=-3.55))
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        W = World()
        static_world(W)
        W.add_to(self)
        self.add(W.species(), W.mono(), baseline())
        self.add(name("16-species plot total", XSTACK, TEXT), name("monoculture", XMONO, TEXT))
        c1 = chip("more steady", BLUE, 28).move_to([0.4, 0.8, 0])
        c2 = chip("less steady", RED, 28).move_to([0.4, -0.4, 0])
        cap = T("Predict: is the total steadier?", 36, YELLOW).move_to([0, 3.25, 0])
        self.add(c1, c2, cap)
        bar = Rectangle(width=5.0, height=0.16, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([0.5, -3.6, 0])
        self.add(bar)
        self.play(bar.animate.stretch_to_fit_width(0.01).align_to([-2.0, 0, 0], LEFT), run_time=5.0, rate_func=linear)
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        W = World()
        static_world(W)
        W.speed = 1.0
        W.add_to(self)
        self.add(W.species(), W.mono(), baseline())
        self.add(name("16-species plot total", XSTACK, TEXT), name("monoculture", XMONO, TEXT))
        c1 = chip("more steady", BLUE, 28).move_to([0.4, 0.8, 0])
        self.add(c1)
        self.at("More")
        self.play(Indicate(c1, color=BLUE, scale_factor=1.25), run_time=1.2)
        self.at("Peter Reich")
        nt = T("Tilman, Reich and Knops, Nature, 2006", 30, TEXT).move_to([0, 3.3, 0])
        self.play(FadeIn(nt, shift=DOWN * 0.2), run_time=0.8)
        self.at("The total varied")
        l1 = T("total:\nsteadier", 28, BLUE, line_spacing=0.8).move_to([0.4, -0.4, 0])
        self.play(FadeOut(c1), FadeIn(l1), run_time=0.7)
        self.at("species on average")
        l2 = T("species:\nless steady", 28, YELLOW, line_spacing=0.8).move_to([0.4, -1.6, 0])
        self.play(FadeIn(l2), run_time=0.7)
        self.add(tag("schematic", x=-4.8, y=-3.55))
        self.finish()


def chip2(lines, color, w=4.6):
    tx = T(lines, 28, color, line_spacing=0.8)
    box = RoundedRectangle(corner_radius=0.14, width=w, height=tx.height + 0.4, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.14)
    tx.move_to(box)
    return VGroup(box, tx)


class S14Why(SpokenScene):
    def construct(self):
        W = World()
        static_world(W, mono=0.0)
        W.speed = 1.0
        W.add_to(self)
        self.add(W.species(), baseline(-6.4, 0.0), name("16-species plot total", XSTACK, TEXT))
        c3 = chip2("opposite swings grow\nwith richness?", RED)
        c1 = chip2("swings partly cancel\n(averaging)", YELLOW)
        c2 = chip2("higher mean biomass", YELLOW)
        c1.move_to([3.6, 2.4, 0])
        c2.move_to([3.6, 0.8, 0])
        c3.move_to([3.6, -1.0, 0])
        self.at("opposite swings")
        self.play(FadeIn(c3, shift=LEFT * 0.3), run_time=0.8)
        self.at("no evidence")
        ne = T("no evidence found", 30, TEXT).move_to([3.6, -2.2, 0])
        self.play(c3.animate.set_opacity(0.35), FadeIn(ne), run_time=0.9)
        for m in (c1, c2):
            m.save_state()
            m.set_opacity(0.3)
            self.add(m)
        self.at("Averaging")
        self.play(c1.animate.restore(), run_time=0.8)
        self.play(Indicate(c1, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("higher mean")
        self.play(c2.animate.restore(), run_time=0.8)
        self.play(Indicate(c2, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.at("only if the swings")
        self.play(FadeOut(ne), run_time=0.3)
        ol = T("only if swings grow less\nthan in proportion", 30, YELLOW, line_spacing=0.8).move_to([3.6, -2.4, 0])
        self.play(FadeIn(ol, shift=UP * 0.2), run_time=0.8)
        self.add(tag("schematic", x=-4.8, y=-3.55))
        self.finish()


class S15Rule(SpokenScene):
    def construct(self):
        t = ValueTracker(0.0)
        t.add_updater(lambda m, dt: m.set_value(min(m.get_value() + dt * 9 / 8.0, 9.0)))
        grow = ValueTracker(0.0)
        self.add(t, grow)
        XL = [-5.9, -4.8, -3.7, -2.6, -1.5]

        def f():
            g = VGroup()
            tt = t.get_value()
            gr = grow.get_value()
            for i, (x, tot, n) in enumerate(zip(XL, TOT, NSEG)):
                v = tot * (1 + 0.06 * np.sin(0.9 * tt * 1.6 + i * 1.3)) * gr
                h = v * KB
                y = BASE
                for c in seg_cols(n):
                    sh = h / n
                    r = Rectangle(width=0.85, height=max(sh, 0.001), stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.7)
                    r.move_to([x, y + sh / 2, 0])
                    g.add(r)
                    y += sh
                g.add(Rectangle(width=0.92, height=max(h, 0.001), stroke_color=OUT, stroke_width=4).move_to([x, BASE + h / 2, 0]))
            return g
        bars = always_redraw(f)
        self.add(bars, baseline(-6.4, -0.8))
        yr = year_text(t, -3.7, 3.3, 40)
        self.add(yr)
        self.play(grow.animate.set_value(1.0), run_time=1.6)
        self.at("richer plots grew more")
        ar = Arrow([XL[0], BASE + TOT[0] * KB + 0.35, 0], [XL[4], BASE + TOT[4] * KB + 0.35, 0], color=YELLOW, stroke_width=6, buff=0)
        mo = T("more", 34, YELLOW).move_to([-5.0, 1.6, 0])
        self.play(Create(ar), FadeIn(mo), run_time=1.0)
        self.at("grew steadier")
        W = World(xs=3.4)
        static_world(W, mono=0.0)
        W.speed = 1.0
        W.add_to(self)
        sp = W.species()
        self.add(baseline(0.6, 6.4))
        self.play(FadeIn(sp), run_time=0.8)
        st = T("total: steadier", 30, BLUE).move_to([3.4, 2.3, 0])
        self.play(FadeIn(st), run_time=0.6)
        self.at("Their species")
        sl = T("species: less steady", 30, YELLOW).move_to([3.4, -3.2, 0])
        self.play(FadeIn(sl), run_time=0.7)
        self.finish()


class S16End(EndCard):
    LINE = "Richer plots: more, steadier biomass, though species were less steady on average."
