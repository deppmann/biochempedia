"""Why the Pea Didn't Starve (plant-nutrition film 2).

COLOUR MAP (same as film 1, plus the two this film needs): phosphate BLUE dots; nitrate and ammonium GREEN dots;
nitrogen gas PALE GREY paired dots 'N2'; phloem GOLD arrow; carbon payment ORANGE tokens; soil tan, roots cream,
bacteria purple, nodules salmon. All schematic.
"""
import importlib.util, math, os, random
from pathlib import Path
import numpy as np
from bp_style import *  # noqa: F401,F403

_here = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent
_spec = importlib.util.spec_from_file_location("film1_scenes", str(_here.parent / "scenes.py"))
F1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F1)
L, lines, mk_dot, send, path_dot, pulse, ring_timer = F1.L, F1.lines, F1.mk_dot, F1.send, F1.path_dot, F1.pulse, F1.ring_timer
stream_dot, _dot_u = F1.stream_dot, F1._dot_u
SOIL, TAN, ROOTC, LEAF, YEL, PURP, PINK, SKY = F1.SOIL, F1.TAN, F1.ROOTC, F1.LEAF, F1.YEL, F1.PURP, F1.PINK, F1.SKY

N2C = "#C4CAD0"
ORANGE = "#EE9B3C"
SALM = "#E39A86"
BROWN = "#8B5E3C"
POTC = "#B5714F"
OATC = "#9CBF5A"
BACT2 = "#9A62CC"


class Sc(SpokenScene):
    def drift_until(self, phrase, mob, k=1.05, lead=0.2):
        rest = self.t_of(phrase) - lead - self.elapsed()
        if rest > 0.1:
            self.play(mob.animate.scale(k), run_time=rest, rate_func=linear)

    def wait_until(self, phrase, lead=0.2):
        rest = self.t_of(phrase) - lead - self.elapsed()
        if rest > 0.05:
            self.wait(rest)


# ---------------------------------------------------------------- helpers
def mk_thing(m, pos, seed=0, amp=0.1):
    m.move_to([pos[0], pos[1], 0])
    m._b = np.array([pos[0], pos[1], 0.0])
    m._t = 0.0
    m._ph = (seed * 1.7, seed * 2.3)
    m._amp = amp
    m._go = None
    m.add_updater(_dot_u)
    return m


def n2pair(pos, seed=0, amp=0.12, r=0.08):
    p = VGroup(Dot(radius=r, color=N2C), Dot(radius=r, color=N2C).shift(RIGHT * 2.2 * r))
    return mk_thing(p, pos, seed, amp)


def field(n, seed, x0, x1, y0, y1, gap=0.7):
    rng = random.Random(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 4000:
        tries += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if all(math.hypot(x - a, y - b) > gap for a, b in pts):
            pts.append((x, y))
    return pts


def bouncer(x0, top, H, speed, ph):
    p = VGroup(Dot(radius=0.09, color=N2C), Dot(radius=0.09, color=N2C).shift(RIGHT * 0.2))
    p._t = 0.0

    def u(m, dt):
        m._t += dt
        y = top + 0.2 + H * abs(math.sin(speed * m._t + ph))
        m.move_to([x0 + 0.3 * math.sin(0.6 * m._t + ph), y, 0])
    p.add_updater(u)
    u(p, 0)
    return p


class Sprout:
    """A growing plant drawn from two trackers: v (0..1 height) and sick (0 green .. 1 yellow and drooping)."""

    def __init__(self, cx, base, hmax, kind="pea", v0=0.0, lw=1.0, nlev=4, thick=10):
        self.vt = ValueTracker(v0)
        self.sk = ValueTracker(0.0)
        c0 = LEAF if kind == "pea" else OATC

        def build():
            v, s = self.vt.get_value(), self.sk.get_value()
            h = hmax * v
            parts = [Line([cx, base, 0], [cx, base + max(h, 0.05), 0], color="#3E7A45",
                          stroke_width=thick * (0.5 + 0.5 * min(v, 1)))]
            col = interpolate_color(ManimColor(c0), ManimColor(YEL), s)
            for i in range(nlev):
                f = 0.3 + 0.65 * i / max(nlev - 1, 1)
                grow = min(1.0, max(0.0, (v - f * 0.75) / 0.2))
                if grow < 0.05:
                    continue
                for side in (-1, 1):
                    w = (0.95 if kind == "pea" else 1.6) * lw * grow
                    hh = (0.5 if kind == "pea" else 0.2) * lw * grow
                    ang = math.radians(24 + 5 * i) - s * math.radians(55)
                    d = np.array([side * math.cos(ang), math.sin(ang), 0])
                    e = Ellipse(width=w, height=hh, fill_color=col, fill_opacity=0.88, stroke_color=col, stroke_width=2)
                    e.rotate(math.atan2(d[1], d[0]))
                    e.move_to(np.array([cx, base + h * f, 0]) + d * w / 2)
                    parts.append(e)
            bud = Ellipse(width=0.3 * lw, height=0.6 * lw, fill_color=col, fill_opacity=0.88, stroke_color=col, stroke_width=2)
            bud.move_to([cx, base + h + 0.25 * lw, 0])
            parts.append(bud)
            return VGroup(*parts)
        self.g = build()
        self.g.add_updater(lambda m: m.become(build()))


def pot(cx, top, w=1.7, h=1.1, cut=False):
    body = Polygon([cx - w / 2, top, 0], [cx + w / 2, top, 0], [cx + w * 0.4, top - h, 0], [cx - w * 0.4, top - h, 0],
                   fill_color="#5E4A36" if cut else POTC, fill_opacity=0.92, stroke_color="#C98B6B", stroke_width=3)
    rim = Rectangle(width=w + 0.24, height=0.17, fill_color="#C98B6B", fill_opacity=1, stroke_width=0).move_to([cx, top + 0.02, 0])
    parts = [body, rim]
    if not cut:
        parts.append(Rectangle(width=w - 0.1, height=0.12, fill_color="#E6D5A8", fill_opacity=1, stroke_width=0).move_to([cx, top - 0.08, 0]))
    return VGroup(*parts).set_z_index(2)


def roots_mob(cx, top, w, h, nod=False):
    segs = VGroup()
    segs.add(Line([cx, top, 0], [cx, top - h * 0.9, 0], color=ROOTC, stroke_width=7))
    tips = []
    for k, (f, s) in enumerate([(0.25, -1), (0.35, 1), (0.55, -1), (0.65, 1)]):
        y = top - h * f
        ex, ey = cx + s * w * (0.34 - 0.04 * k), y - h * 0.22
        segs.add(Line([cx, y, 0], [ex, ey, 0], color=ROOTC, stroke_width=5))
        tips.append((ex, ey))
    nods = VGroup()
    if nod:
        for (ex, ey) in tips:
            nods.add(Circle(radius=0.17, fill_color=SALM, fill_opacity=1, stroke_color="#F2C1B2", stroke_width=2).move_to([ex, ey, 0]))
        nods.add(Circle(radius=0.14, fill_color=SALM, fill_opacity=1, stroke_color="#F2C1B2", stroke_width=2).move_to([cx + 0.1, top - h * 0.75, 0]))
    segs.set_z_index(3)
    nods.set_z_index(4)
    return segs, nods


def flame(pos):
    a = Ellipse(width=0.5, height=0.9, fill_color=ORANGE, fill_opacity=0.95, stroke_width=0)
    b = Ellipse(width=0.26, height=0.5, fill_color=YELLOW, fill_opacity=1, stroke_width=0).shift(DOWN * 0.12)
    g = VGroup(a, b).move_to(pos)
    g._t = 0.0
    g._p = np.array(pos, dtype=float)

    def u(m, dt):
        m._t += dt
        m.stretch_to_fit_height(0.9 * (1 + 0.18 * math.sin(11 * m._t)), about_edge=DOWN) if False else None
        m.move_to(m._p + np.array([0.03 * math.sin(9 * m._t), 0.04 * math.sin(13 * m._t), 0]))
    g.add_updater(u)
    return g


def flask(pos, liquid=True):
    body = Circle(radius=0.62, stroke_color=TEXT, stroke_width=4, fill_color=BROWN if liquid else BG, fill_opacity=0.8)
    neck = Rectangle(width=0.34, height=0.7, stroke_color=TEXT, stroke_width=4, fill_color=BROWN, fill_opacity=0.5).move_to([0, 0.8, 0])
    return VGroup(neck, body).move_to(pos)


def card(rows, pos, size=32, col=GOLD):
    t = lines(rows, size, TEXT)
    box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.6, height=t.height + 0.6, stroke_color=col, stroke_width=3,
                           fill_color=BG, fill_opacity=0.95)
    g = VGroup(box, t.move_to(box)).move_to(pos)
    return g, t


def underground():
    return Rectangle(width=14.3, height=2.9, stroke_width=0, fill_color=SOIL, fill_opacity=0.22).move_to([0, -2.35, 0]).set_z_index(-5)


def tilecard(sym, col, w=0.85, size=26):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=0.62, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.95)
    return VGroup(box, T(sym, size=size, color=BG, weight=BOLD).move_to(box)).set_z_index(10)


def bar_mob(x, base, w, vt, col):
    def mk():
        h = max(0.02, vt.get_value())
        return Rectangle(width=w, height=h, fill_color=col, fill_opacity=0.92, stroke_color=col, stroke_width=2).move_to([x, base + h / 2, 0])
    b = mk()
    b.add_updater(lambda m: m.become(mk()))
    return b


def bacteroid_blobs(pts, size=0.55):
    return VGroup(*[RoundedRectangle(corner_radius=size * 0.4, width=size, height=size * 0.85, fill_color=BACT2, fill_opacity=0.95,
                                     stroke_color=PURP, stroke_width=2).move_to([x, y, 0]) for x, y in pts])


def rod(pos, seed, amp=0.08):
    r = RoundedRectangle(corner_radius=0.09, width=0.46, height=0.19, fill_color=PURP, fill_opacity=0.95, stroke_color=PURP, stroke_width=1)
    return mk_thing(r, pos, seed, amp)


# =========================================================== scenes
class S00Title(TitleCard):
    LESSON = "Soil, Nutrients and Partners"
    TITLE = "Why the Pea Didn't Starve"


class S01Hook(Sc):
    def construct(self):
        band = F1.soil_band()
        pairs = [n2pair(p, i, 0.14) for i, p in enumerate(field(18, 4, -6.5, 6.5, -2.4, 3.0, 0.9))]
        lab = L("nitrogen gas, N2", 36, N2C).move_to([0, 3.35, 0])
        self.add(band)
        self.play(FadeIn(*pairs), FadeIn(lab), run_time=1.0)
        self.at("around every")
        pea = Sprout(-3.1, -3.0, 5.0, "pea", lw=1.6, nlev=5, thick=14)
        oat = Sprout(3.1, -3.0, 5.0, "oat", lw=1.2, nlev=5, thick=12)
        self.add(pea.g, oat.g)
        self.play(pea.vt.animate.set_value(1), oat.vt.animate.set_value(1), run_time=1.6)
        self.at("why")
        q = pulse(Text("?", font=FONT, font_size=120, color=YELLOW, weight=BOLD).move_to([0, 0.3, 0]), 0.12, 4)
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.at("pea")
        lp = L("pea", 40, LEAF).move_to([-3.1, 3.4, 0]).set_z_index(30)
        self.play(FadeIn(lp), run_time=0.3)
        self.at("oat")
        lo = L("oat", 40, OATC).move_to([3.1, 3.4, 0]).set_z_index(30)
        self.play(FadeIn(lo), run_time=0.3)
        self.at("starves")
        self.play(oat.sk.animate.set_value(1), run_time=1.1)
        self.finish()


class S02Link(Sc):
    def construct(self):
        tag = L("Film 1 take-home", 30, GOLD).move_to([0, 1.6, 0])
        line = lines(["How far a nutrient moves", "shapes how a plant must reach it."], 40, TEXT).move_to([0, 0.1, 0])
        rule = Line(LEFT * 3.5, RIGHT * 3.5, color=GOLD, stroke_width=4).move_to([0, -1.2, 0])
        g = VGroup(tag, line, rule)
        self.play(FadeIn(tag), Write(line), GrowFromCenter(rule), run_time=2.4)
        self.drift_until("form matters", g, 1.06)
        self.play(FadeOut(g, shift=UP * 0.4), run_time=0.4)
        big = L("Form matters, too.", 66, GOLD).move_to([0, 0.5, 0])
        self.play(Write(big), run_time=1.0)
        self.drift_until("nitrogen gas", big, 1.05)
        self.play(FadeOut(big), run_time=0.4)
        leaf = Ellipse(width=9, height=1.6, fill_color=LEAF, fill_opacity=0.9, stroke_color=LEAF, stroke_width=3).move_to([0, -1.5, 0])
        vein = Line([-4.2, -1.5, 0], [4.2, -1.5, 0], color="#2F6B34", stroke_width=5)
        bs = [bouncer(-4.8 + 1.6 * i, -0.7, 1.3 + 0.5 * (i % 3), 1.4 + 0.15 * i, i * 0.9) for i in range(7)]
        n2 = L("N2", 44, N2C).move_to([-5.6, 2.6, 0])
        self.play(FadeIn(leaf), FadeIn(vein), FadeIn(*bs), FadeIn(n2), run_time=0.9)
        self.at("no plant enzyme")
        t = L("no plant enzyme can use it", 36, TEXT).move_to([0, -2.9, 0])
        self.play(FadeIn(t), run_time=0.5)
        self.finish()


POTX6 = [-5.5, -3.3, -1.1, 1.1, 3.3, 5.5]


class S03Pots(Sc):
    def construct(self):
        pots = [pot(x, -1.6, 1.9, 1.5) for x in POTX6]
        self.play(LaggedStart(*[GrowFromEdge(p, DOWN) for p in pots], lag_ratio=0.12), run_time=1.2)
        self.at("bernburg")
        cap = L("Bernburg, 1888", 40, GOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.2), run_time=0.5)
        self.at("hermann")
        names = L("Hellriegel and Wilfarth", 38, TEXT).move_to([0, 2.55, 0])
        self.play(Write(names), run_time=1.3)
        self.at("pots")
        self.play(*[Indicate(p, scale_factor=1.06, color=YELLOW) for p in pots], run_time=1.0)
        self.at("peas")
        seeds = [Sprout(x, -1.6, 3.4, "pea" if i < 3 else "oat", 0.0, lw=0.8) for i, x in enumerate(POTX6)]
        for s in seeds[:3]:
            self.add(s.g)
        lp = L("peas", 36, LEAF).move_to([-3.3, -3.4, 0])
        self.play(*[s.vt.animate.set_value(0.3) for s in seeds[:3]], FadeIn(lp), run_time=0.8)
        self.at("oats")
        for s in seeds[3:]:
            self.add(s.g)
        lo = L("oats", 36, OATC).move_to([3.3, -3.4, 0])
        self.play(*[s.vt.animate.set_value(0.3) for s in seeds[3:]], FadeIn(lo), run_time=0.8)
        self.at("washed")
        t = L("washed, sterilised sand", 34, TAN).move_to([0, 0.7, 0])
        a = Arrow([0.9, 0.25, 0], [1.7, -1.4, 0], buff=0, color=TAN, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(t), GrowArrow(a), run_time=0.7)
        self.finish()


class S04Solution(Sc):
    def construct(self):
        pots = [pot(x, -1.6, 1.9, 1.5) for x in POTX6]
        seeds = [Sprout(x, -1.6, 3.4, "pea" if i < 3 else "oat", 0.3, lw=0.8) for i, x in enumerate(POTX6)]
        self.add(*pots, *[s.g for s in seeds])
        can = VGroup(Rectangle(width=1.0, height=0.8, fill_color="#8A94A0", fill_opacity=1, stroke_color=TEXT, stroke_width=3).move_to([0.5, 0.6, 0]),
                     Line([0.0, 0.5, 0], [-0.7, 0.2, 0], color=TEXT, stroke_width=6),
                     Arc(radius=0.4, start_angle=0, angle=PI, color=TEXT, stroke_width=4).move_to([0.5, 1.15, 0]))
        can.shift(RIGHT * (POTX6[0] + 0.7))
        self.play(FadeIn(can), run_time=0.4)
        syms = ["P", "K", "Ca", "Mg", "S", "Fe"]
        tx = [None]
        for i, x in enumerate(POTX6):
            if i == 0:
                pass
            else:
                self.play(can.animate.shift(RIGHT * (x - POTX6[i - 1])), run_time=0.2)
            tl = tilecard(syms[i], TAN, 0.8 if len(syms[i]) == 1 else 1.0).move_to([x - 0.7, 0.1, 0])
            self.add(tl)
            self.play(tl.animate.move_to([x, -1.5, 0]).set_opacity(0.0), run_time=0.32)
            if i == 1:
                lab = lines(["base solution:", "every mineral except nitrogen"], 32, TEXT).move_to([0, 3.0, 0])
                self.add(lab)
        self.at("no nitrogen")
        ntile = tilecard("N", GREEN, 0.95, 32).move_to([5.3, 2.7, 0])
        cross = VGroup(Line([4.8, 2.35, 0], [5.8, 3.05, 0], color=RED, stroke_width=8), Line([4.8, 3.05, 0], [5.8, 2.35, 0], color=RED, stroke_width=8)).set_z_index(12)
        self.play(FadeOut(can), FadeIn(ntile), Create(cross), run_time=0.6)
        self.at("extra nitrogen")
        ex = L("extra nitrogen: from where?", 38, GREEN).move_to([0, 1.3, 0])
        self.play(FadeIn(ex), run_time=0.5)
        self.at("what they")
        w = L("from what they added", 34, GREEN).move_to([-3.6, 0.1, 0])
        rng = random.Random(8)
        ds = [mk_dot(GREEN, (-3.6 + rng.uniform(-1.6, 1.6), -0.3 + rng.uniform(-0.2, 0.2)), r=0.1, seed=i, amp=0.08) for i in range(8)]
        self.play(FadeIn(w), FadeIn(*ds), run_time=0.5)
        for i, d in enumerate(ds):
            send(d, (-1.1 + (i % 3) * 0.1 if i % 2 else -3.3, -1.5), 1.4)
        self.at("from the air")
        a = L("from the air", 34, N2C).move_to([3.7, 0.1, 0])
        ps = [n2pair(p, i, 0.12) for i, p in enumerate(field(8, 3, 1.5, 6.0, 0.6, 2.4, 0.9))]
        self.play(FadeIn(a), FadeIn(*ps), run_time=0.6)
        self.finish()


class S05Logic(Sc):
    def construct(self):
        seed = Ellipse(width=0.9, height=1.3, fill_color=TAN, fill_opacity=1, stroke_color="#E6D5A8", stroke_width=3).move_to([-5.2, 1.3, 0])
        halo = Circle(radius=0.95, color=YELLOW, fill_color=YELLOW, fill_opacity=0.15, stroke_width=0).move_to(seed)
        halo._t = 0.0
        halo.add_updater(lambda m, dt: (setattr(m, "_t", m._t + dt), m.set_opacity(0.5 + 0.5 * math.sin(3 * m._t)))[0] if False else m.set_fill(YELLOW, 0.1 + 0.12 * (1 + math.sin(3 * (m.__dict__.setdefault("_tt", 0.0) + 0.0)))))
        seedt = ValueTracker(0.0)
        halo.clear_updaters()
        halo.add_updater(lambda m: m.set_fill(YELLOW, 0.14 + 0.1 * math.sin(3 * (self.renderer.time))))
        self.play(FadeIn(seed, scale=0.5), FadeIn(halo), run_time=0.8)
        sv = ValueTracker(0.0)
        sbar = bar_mob(-5.2, -2.6, 0.9, sv, GREEN)
        sl = lines(["nitrogen", "in seed"], 30, GREEN).move_to([-5.2, -0.45, 0])
        self.add(sbar)
        self.play(sv.animate.set_value(1.2), FadeIn(sl), run_time=1.3)
        self.at("if every")
        xs = [-2.2, 0.1, 2.4, 4.7]
        pots = [pot(x, -2.7, 1.4, 0.9) for x in xs]
        vts = [ValueTracker(0.0) for _ in xs]
        bars = [bar_mob(x, -2.6, 0.8, v, GREEN) for x, v in zip(xs, vts)]
        self.add(*bars)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.3) for p in pots], lag_ratio=0.2), run_time=1.0)
        self.at("relied")
        t = L("soil nitrogen only", 36, GREEN).move_to([1.1, 1.2, 0])
        self.play(FadeIn(t), run_time=0.5)
        self.play(*[v.animate.set_value(1.2) for v in vts], run_time=1.6)
        self.at("none")
        ceil = DashedLine([-4.6, -1.4, 0], [6.4, -1.4, 0], color=GOLD, stroke_width=5, dash_length=0.2)
        self.play(Create(ceil), run_time=1.0, rate_func=linear)
        c = lines(["the most it could hold", "without another nitrogen source"], 30, GOLD).move_to([1.1, -0.6, 0])
        self.play(FadeIn(c), run_time=0.5)
        self.at("seed held")
        self.play(Indicate(sbar, color=YELLOW), Indicate(ceil, color=YELLOW), run_time=1.2)
        self.finish()


OATX = [-4.95, -1.65, 1.65, 4.95]


class S06Oats(Sc):
    def construct(self):
        pots = [pot(x, -1.7, 2.0, 1.3) for x in OATX]
        pl = [Sprout(x, -1.7, 3.6, "oat", 0.1, lw=1.1) for x in OATX]
        self.play(GrowFromEdge(pots[0], DOWN), run_time=0.7)
        self.add(pl[0].g)
        self.at("no nitrogen")
        l0 = L("none", 36, TEXT).move_to([OATX[0], -3.4, 0])
        self.play(FadeIn(l0), run_time=0.4)
        self.play(pl[0].vt.animate.set_value(0.16), run_time=1.5)
        self.at("others")
        self.play(LaggedStart(*[GrowFromEdge(p, DOWN) for p in pots[1:]], lag_ratio=0.12), run_time=0.6)
        for p in pl[1:]:
            self.add(p.g)
        names = ["low", "medium", "high"]
        self.at("measured")
        ls = [L(n, 36, TEXT).move_to([x, -3.4, 0]) for n, x in zip(names, OATX[1:])]
        self.play(LaggedStart(*[FadeIn(l) for l in ls], lag_ratio=0.15), run_time=0.5)
        self.at("nitrate")
        tn = L("nitrate", 36, GREEN).move_to([0, 3.3, 0])
        rng = random.Random(5)
        drops = []
        for x, n in zip(OATX[1:], [4, 8, 14]):
            for k in range(n):
                drops.append((mk_dot(GREEN, (x + rng.uniform(-0.5, 0.5), 2.6 + rng.uniform(0, 1.0)), r=0.1, seed=k, amp=0.04), x))
        self.play(FadeIn(tn), FadeIn(*[d for d, _ in drops]), run_time=0.4)
        for d, x in drops:
            send(d, (x + rng.uniform(-0.3, 0.3), -1.6), rng.uniform(2.2, 3.6))
        self.at("oats grew")
        self.play(pl[1].vt.animate.set_value(0.45), pl[2].vt.animate.set_value(0.75), pl[3].vt.animate.set_value(1.0), FadeOut(tn),
                  run_time=3.0)
        self.finish()


class S07Peas(Sc):
    def construct(self):
        x1, x2 = -2.6, 2.6
        p1 = pot(x1, -1.6, 2.4, 1.5)
        a = Sprout(x1, -1.6, 3.8, "pea", 0.12, lw=1.2)
        self.play(GrowFromEdge(p1, DOWN), run_time=0.7)
        self.add(a.g)
        self.at("nothing")
        l1 = L("no extract", 36, TEXT).move_to([x1, -3.4, 0])
        self.play(FadeIn(l1), run_time=0.4)
        self.at("stayed")
        self.play(a.vt.animate.set_value(0.25), run_time=1.5)
        self.at("but")
        p2 = pot(x2, -1.6, 2.4, 1.5)
        b = Sprout(x2, -1.6, 3.8, "pea", 0.12, lw=1.2)
        fl = flask([5.4, 0.9, 0])
        self.add(b.g)
        self.play(GrowFromEdge(p2, DOWN), FadeIn(fl, shift=LEFT * 0.6), run_time=0.9)
        self.at("little extract")
        l2 = L("live soil extract", 36, BROWN if False else "#C9915F").move_to([x2, -3.4, 0])
        self.play(FadeIn(l2), run_time=0.4)
        self.at("shaken")
        self.play(Rotate(fl, angle=1.1, about_point=fl.get_center()), run_time=0.5)
        self.play(Rotate(fl, angle=0.12, about_point=fl.get_center(), rate_func=there_and_back), run_time=0.3)
        mouth = fl.get_center() + np.array([-0.9, 0.5, 0])
        rng = random.Random(2)
        for k in range(9):
            d = mk_dot(BROWN, (mouth[0] - 0.1, mouth[1] - 0.1), r=0.1, seed=k, amp=0.0)
            self.add(d)
            send(d, (x2 + rng.uniform(-0.5, 0.5), -1.5), 2.2)
            self.wait(0.2)
        self.at("those grew")
        self.play(FadeOut(fl), b.vt.animate.set_value(1.0), run_time=1.6)
        self.finish()


class S08Nodules(Sc):
    def construct(self):
        cx = -3.6
        self.add(underground())
        p = pot(cx, -0.8, 2.6, 2.4, cut=True)
        r, nods = roots_mob(cx, -0.8, 2.6, 2.4, nod=True)
        pl = Sprout(cx, -0.8, 3.3, "pea", 1.0, lw=1.0, nlev=4)
        self.play(FadeIn(p), FadeIn(r), FadeIn(pl.g), run_time=1.0)
        self.at("nodules")
        self.play(LaggedStart(*[GrowFromCenter(n) for n in nods], lag_ratio=0.15), run_time=1.0)
        lab = L("nodules", 36, SALM).move_to([-0.3, -1.7, 0])
        ar = Arrow([-1.2, -1.8, 0], [-2.7, -2.0, 0], buff=0.05, color=SALM, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(lab), GrowArrow(ar), run_time=0.5)
        sch = L("schematic bars", 24, GREY).move_to([4.1, 3.5, 0])
        self.at("plants ended")
        v1, v2 = ValueTracker(0.0), ValueTracker(0.0)
        b1 = bar_mob(2.6, -2.6, 1.2, v1, GREEN)
        b2 = bar_mob(5.4, -2.6, 1.2, v2, GREEN)
        l1 = lines(["nitrogen", "in seed"], 28, GREEN).move_to([2.6, -3.25, 0])
        self.add(b1, b2)
        self.play(v1.animate.set_value(0.8), FadeIn(l1), FadeIn(sch), run_time=1.0)
        self.at("far more")
        l2 = lines(["nitrogen", "at harvest"], 28, GREEN).move_to([5.4, -3.25, 0])
        self.play(v2.animate.set_value(3.6), FadeIn(l2), run_time=2.2)
        self.at("held")
        self.play(Indicate(b1, color=YELLOW), run_time=0.8)
        self.at("extra nitrogen")
        seg = Rectangle(width=1.2, height=2.8, fill_color=N2C, fill_opacity=0.95, stroke_color=N2C, stroke_width=2).move_to([5.4, -2.6 + 0.8 + 1.4, 0])
        self.play(FadeIn(seg), run_time=0.6)
        self.at("came from")
        g = lines(["gained from", "the air"], 32, N2C).move_to([3.0, 0.5, 0])
        self.play(FadeIn(g), run_time=0.5)
        self.play(Indicate(seg, color=YELLOW), run_time=1.0)
        self.finish()


PX = 4.3


def heated_pot():
    p = pot(PX, -1.1, 3.0, 2.2, cut=True)
    r, _ = roots_mob(PX, -1.1, 3.0, 2.2, nod=False)
    pl = Sprout(PX, -1.1, 3.4, "pea", 0.2, lw=1.1)
    lab = L("heated extract", 30, TEXT).move_to([PX, -3.6, 0])
    return p, r, pl, lab


def q_card():
    return card(["Heated extract:", "nodules?", "nitrogen gained?"], [-3.2, 0.6, 0], 36)


class S09Predict(Sc):
    def construct(self):
        self.add(underground())
        p, r, pl, lab = heated_pot()
        self.play(FadeIn(p), FadeIn(r), FadeIn(pl.g), run_time=0.8)
        self.at("soil extract")
        fl = flask([2.2, 0.4, 0])
        self.play(FadeIn(fl), run_time=0.5)
        self.at("heated")
        fm = flame([2.2, -1.0, 0])
        self.play(FadeIn(fm), FadeIn(lab), run_time=0.4)
        self.wait(0.2)
        self.play(FadeOut(fm), Rotate(fl, angle=-1.1, about_point=fl.get_center()), run_time=0.5)
        mouth = fl.get_center() + np.array([0.9, 0.5, 0])
        rng = random.Random(4)
        for k in range(5):
            d = mk_dot(BROWN, (mouth[0] + 0.1, mouth[1] - 0.1), r=0.1, seed=k, amp=0.0)
            self.add(d)
            send(d, (PX + rng.uniform(-0.6, 0.6), -1.0), 3.0)
            self.wait(0.1)
        self.play(FadeOut(fl), run_time=0.2)
        self.at("will")
        cd, t = q_card()
        self.play(FadeIn(cd), run_time=0.5)
        self.at("nodules")
        self.play(Indicate(t[1], color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("gain nitrogen")
        self.play(Indicate(t[2], color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        self.add(underground())
        p, r, pl, lab = heated_pot()
        cd, t = q_card()
        self.add(p, r, pl.g, lab, cd)
        tc = ring_timer([-5.9, -3.1, 0], 0.5)
        arc = Arc(radius=0.5, start_angle=PI / 2, angle=-2 * PI, color=GOLD, stroke_width=7).move_to(tc)
        self.add(tc)
        self.play(Create(arc), run_time=4.8, rate_func=linear)
        self.finish()


class S11Reveal(Sc):
    def construct(self):
        self.add(underground())
        p, r, pl, lab = heated_pot()
        self.add(p, r, pl.g, lab)
        no = L("No.", 110, RED).move_to([-2.2, 1.0, 0])
        self.play(FadeIn(no, scale=1.3), run_time=0.5)
        self.wait_until("no nodules")
        self.play(FadeOut(no), run_time=0.2)
        t1 = L("No nodules.", 52, RED).move_to([-2.2, 1.3, 0])
        self.play(Write(t1), run_time=0.8)
        self.at("no nitrogen")
        t2 = L("No nitrogen gained.", 46, RED).move_to([-2.2, 0.2, 0])
        self.play(Write(t2), run_time=0.8)
        self.at("a living")
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.3)
        xs = [-4.3, 0.0]
        pA = pot(xs[0], -1.1, 3.0, 2.2, cut=True)
        rA, _ = roots_mob(xs[0], -1.1, 3.0, 2.2)
        plA = Sprout(xs[0], -1.1, 3.4, "pea", 0.2, lw=1.1)
        pB = pot(xs[1], -1.1, 3.0, 2.2, cut=True)
        rB, nB = roots_mob(xs[1], -1.1, 3.0, 2.2, nod=True)
        plB = Sprout(xs[1], -1.1, 3.4, "pea", 0.2, lw=1.1)
        lA = L("no extract", 30, TEXT).move_to([xs[0], -3.6, 0])
        lB = L("live extract", 30, TEXT).move_to([xs[1], -3.6, 0])
        self.add(plA.g, plB.g)
        self.play(FadeIn(pA), FadeIn(rA), FadeIn(pB), FadeIn(rB), FadeIn(nB), FadeIn(lA), FadeIn(lB), plB.vt.animate.set_value(1.0), run_time=0.7)
        self.at("living agent")
        ag = L("a living agent from soil", 38, GOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(ag), run_time=0.5)
        self.at("tied")
        self.play(Indicate(nB, color=YELLOW, scale_factor=1.5), run_time=1.0)
        self.finish()


class S12Rhizobia(Sc):
    def construct(self):
        rng = random.Random(6)
        rods = [rod((-5.7 + rng.uniform(-0.6, 0.9), rng.uniform(-2.6, 1.8)), i, 0.14) for i in range(8)]
        self.play(FadeIn(*rods), run_time=0.8)
        self.at("bacteria")
        lab = L("bacteria", 36, PURP).move_to([-5.0, 2.8, 0])
        self.play(FadeIn(lab), run_time=0.4)
        self.at("rhizobia")
        lab2 = L("rhizobia", 44, PURP).move_to([-5.0, 2.8, 0])
        self.play(Transform(lab, lab2), run_time=0.6)
        self.wait_until("enter")
        band = Rectangle(width=0.7, height=7.0, fill_color=ROOTC, fill_opacity=0.9, stroke_width=0).move_to([-3.0, -0.2, 0]).set_z_index(-1)
        rl = L("root", 34, ROOTC).move_to([-3.0, 3.5, 0])
        nod = RoundedRectangle(corner_radius=0.5, width=8.9, height=6.0, stroke_color=SALM, stroke_width=4, fill_color=SALM, fill_opacity=0.12).move_to([1.7, -0.2, 0])
        cells = VGroup(*[RoundedRectangle(corner_radius=0.3, width=3.8, height=2.6, stroke_color=ROOTC, stroke_width=2.5, fill_color=ROOTC, fill_opacity=0.08).move_to([cx, cy, 0])
                         for cx, cy in [(-0.1, 1.3), (3.6, 1.3), (-0.1, -1.7), (3.6, -1.7)]])
        self.play(FadeIn(band), FadeIn(rl), FadeIn(nod), FadeIn(cells), run_time=0.8)
        cellc = [(-0.1, 1.3), (3.6, 1.3), (-0.1, -1.7), (3.6, -1.7)]
        for i, d in enumerate(rods):
            cx, cy = cellc[i % 4]
            send(d, (cx + rng.uniform(-1.2, 1.2), cy + rng.uniform(-0.6, 0.6)), 1.7, kill=False)
        extra = [rod((-5.7, rng.uniform(-2.6, 1.8)), 20 + i, 0.1) for i in range(8)]
        self.add(*extra)
        for i, d in enumerate(extra):
            cx, cy = cellc[i % 4]
            send(d, (cx + rng.uniform(-1.2, 1.2), cy + rng.uniform(-0.6, 0.6)), 1.6, kill=False)
        self.at("inside")
        nl = L("nodule cells", 34, ROOTC).move_to([1.7, 3.45, 0])
        self.play(FadeIn(nl), run_time=0.5)
        self.at("change")
        self.play(*[d.animate.stretch_to_fit_width(0.5).stretch_to_fit_height(0.5).set_fill(BACT2, 1.0) for d in rods + extra], run_time=1.3)
        bl = L("bacteroids", 40, PURP).move_to([1.7, -3.55, 0])
        self.at("bacteroids")
        self.play(FadeIn(bl), run_time=0.5)
        self.finish()


class S13Nitrogenase(Sc):
    def construct(self):
        blob = RoundedRectangle(corner_radius=1.2, width=6.0, height=4.6, stroke_color=PURP, stroke_width=4, fill_color=PURP, fill_opacity=0.12).move_to([-1.2, 0, 0])
        bl = L("bacteroid", 36, PURP).move_to([-1.2, 2.9, 0])
        self.play(FadeIn(blob), FadeIn(bl), run_time=1.0)
        blk = RoundedRectangle(corner_radius=0.2, width=3.4, height=2.2, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.18).move_to([-1.2, 0, 0])
        self.play(FadeIn(blk, scale=0.7), run_time=0.8)
        self.at("nitrogenase")
        bt = L("nitrogenase", 38, GOLD).move_to(blk)
        self.play(Write(bt), run_time=0.9)
        lanes = [-1.2, -0.4, 0.4, 1.2]
        tr = ValueTracker(0.0)

        def carrier(y, ph):
            pr = VGroup(Dot(radius=0.09, color=N2C), Dot(radius=0.09, color=N2C).shift(RIGHT * 0.2))
            am = Dot(radius=0.12, color=GREEN)
            g = VGroup(pr, am)
            g._t = 0.0

            def u(m, dt):
                m._t += dt
                f = (ph + 0.14 * m._t) % 1.0
                on = tr.get_value()
                if f < 0.42:
                    x = -6.4 + (f / 0.42) * (-2.9 + 6.4)
                    pr.move_to([x, y, 0]); am.move_to([0, 0, 0])
                    pr.set_opacity(on); am.set_opacity(0)
                elif f > 0.58:
                    x = -0.3 + ((f - 0.58) / 0.42) * (5.0 + 0.3)
                    am.move_to([x, y, 0]); pr.set_opacity(0); am.set_opacity(on)
                else:
                    pr.set_opacity(0); am.set_opacity(0)
            g.add_updater(u)
            u(g, 0)
            return g
        cs = [carrier(y, k * 0.125 + (0.5 if j % 2 else 0.0)) for j, y in enumerate(lanes) for k in range(2)]
        self.add(*cs)
        self.at("turns")
        self.play(tr.animate.set_value(1.0), run_time=0.8)
        self.at("nitrogen gas")
        n2 = L("N2", 40, N2C).move_to([-5.4, 1.9, 0])
        self.play(FadeIn(n2), run_time=0.4)
        self.at("ammonia")
        am = L("ammonia", 36, GREEN).move_to([2.9, 2.75, 0])
        self.play(FadeIn(am), run_time=0.4)
        self.at("a form")
        cell = RoundedRectangle(corner_radius=0.5, width=2.8, height=4.6, stroke_color=LEAF, stroke_width=4, fill_color=LEAF, fill_opacity=0.12).move_to([5.2, 0, 0])
        cl = L("pea cell", 34, LEAF).move_to([5.2, 2.9, 0])
        self.play(FadeIn(cell), FadeIn(cl), run_time=0.6)
        self.at("makes no")
        nn = lines(["makes no", "nitrogenase"], 32, RED).move_to([5.2, -3.2, 0])
        xx = VGroup(Line([4.5, -0.6, 0], [5.9, 0.6, 0], color=RED, stroke_width=7), Line([4.5, 0.6, 0], [5.9, -0.6, 0], color=RED, stroke_width=7))
        self.play(FadeIn(nn), Create(xx), run_time=0.7)
        self.finish()


class S14Payment(Sc):
    def construct(self):
        self.add(underground())
        pl = Sprout(-4.4, -0.9, 3.4, "pea", 1.0, lw=1.0)
        root = VMobject(color=ROOTC, stroke_width=9).set_points_as_corners([[-4.4, -0.9, 0], [-4.4, -1.8, 0], [1.0, -1.75, 0]])
        nod = Circle(radius=1.9, stroke_color=SALM, stroke_width=5, fill_color=SALM, fill_opacity=0.18).move_to([2.9, -1.7, 0])
        bts = [(2.2, -1.2), (3.6, -1.0), (2.5, -2.4), (3.9, -2.3), (3.0, -1.7)]
        bb = bacteroid_blobs(bts)
        self.play(FadeIn(pl.g), FadeIn(root), FadeIn(nod), FadeIn(bb), run_time=1.0)
        self.at("pays")
        self.play(Indicate(pl.g, color=ORANGE, scale_factor=1.04), run_time=1.0)
        self.at("sugar")
        pts = [(-3.9, 1.9), (-4.4, 1.3), (-4.4, -1.8), (0.9, -1.75)]
        toks = [path_dot(pts, 0.1, k / 5, ORANGE, 0.15, rev=False) for k in range(5)]
        sl = L("sucrose", 36, ORANGE).move_to([-2.4, 1.0, 0])
        self.play(FadeIn(sl), run_time=0.4)
        self.add(*toks)
        self.at("there")
        ml = L("malate", 36, ORANGE).move_to([2.9, 1.3, 0])
        sq = []
        rng = random.Random(9)
        for k in range(5):
            s = Square(0.3, fill_color=ORANGE, fill_opacity=1, stroke_width=0)
            mk_thing(s, (1.2, -1.7 + rng.uniform(-0.2, 0.2)), k, 0.03)
            sq.append(s)
        self.add(*sq)
        self.play(FadeIn(ml), run_time=0.4)
        for s, (x, y) in zip(sq, bts):
            send(s, (x - 0.3, y + 0.1), 0.9, kill=False)
        self.at("fuels")
        bt = L("bacteroids", 36, PURP).move_to([2.9, 0.5, 0])
        self.play(FadeIn(bt), *[Indicate(b, color=YELLOW, scale_factor=1.12) for b in bb], run_time=1.0)
        self.finish()


class S15Trade(Sc):
    def construct(self):
        nc = np.array([-3.4, -0.1, 0])
        nod = Circle(radius=1.7, stroke_color=SALM, stroke_width=5, fill_color=SALM, fill_opacity=0.18).move_to(nc)
        bb = bacteroid_blobs([(-4.0, 0.4), (-2.8, 0.3), (-3.9, -0.7), (-2.8, -0.6)], 0.55)
        tl = L("pea nodule", 34, SALM).move_to([-3.4, -2.5, 0])
        self.play(FadeIn(nod), FadeIn(bb), FadeIn(tl), run_time=0.8)
        a1 = Arrow([-6.2, 1.7, 0], [-4.7, 0.8, 0], buff=0, color=ORANGE, stroke_width=6, tip_length=0.25)
        a2 = Arrow([-2.2, -0.6, 0], [-0.5, -1.7, 0], buff=0, color=GREEN, stroke_width=6, tip_length=0.25)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        oin = [path_dot([(-6.2, 1.7), (-4.7, 0.8)], 0.3, k / 3, ORANGE, 0.14, rev=False) for k in range(3)]
        gout = [path_dot([(-2.2, -0.6), (-0.5, -1.7)], 0.3, k / 3, GREEN, 0.14, rev=False) for k in range(3)]
        self.add(*oin, *gout)
        self.at("carbon")
        lc = L("carbon", 36, ORANGE).move_to([-5.6, 2.4, 0])
        self.play(FadeIn(lc), run_time=0.4)
        self.at("nitrogen")
        ln = L("nitrogen", 36, GREEN).move_to([-0.6, -2.4, 0])
        self.play(FadeIn(ln), run_time=0.4)
        self.at("oats")
        rt = Line([3.6, 2.0, 0], [3.6, -1.4, 0], color=ROOTC, stroke_width=14)
        hairs = VGroup(*[Line([3.6, y, 0], [3.6 + s * 0.8, y - 0.25, 0], color=ROOTC, stroke_width=5) for y in (1.4, 0.4, -0.6) for s in (-1, 1)])
        ol = L("oat root", 34, ROOTC).move_to([3.6, 2.9, 0])
        self.play(FadeIn(rt), FadeIn(hairs), FadeIn(ol), run_time=0.7)
        self.at("no nodules")
        nn = L("no nodules", 32, RED).move_to([5.3, 2.2, 0])
        self.play(FadeIn(nn), run_time=0.4)
        rng = random.Random(3)
        trk = ValueTracker(0.5)
        sd = []
        for i in range(10):
            d = stream_dot((3.6, -0.4, 0.0), 2 * PI * i / 10 + 0.3, 0.6, 2.6, trk, GREEN, 0.1)
            d._on.set_value(0.0)
            sd.append(d)
        self.add(*sd)
        self.at("depend")
        for d in sd:
            d._on.set_value(1.0)
        self.at("nitrate")
        sl = L("nitrate and ammonium", 32, GREEN).move_to([3.6, -3.4, 0])
        self.play(FadeIn(sl), run_time=0.5)
        self.finish()


class S16Rule(Sc):
    def construct(self):
        self.add(underground())
        pl = Sprout(-2.4, -0.9, 3.6, "pea", 1.0, lw=1.3, nlev=4)
        ps = [n2pair(p, i, 0.14) for i, p in enumerate([q for q in field(16, 5, -6.4, 6.4, -3.4, 3.0, 1.0) if not (q[0] > 2.4 and q[1] > 1.8) and not (0.2 < q[0] < 3.6 and -0.5 < q[1] < 1.3) and not (1.0 < q[0] < 3.8 and -3.0 < q[1] < -1.6)])]
        self.play(FadeIn(pl.g), FadeIn(*ps), run_time=1.0)
        self.at("all around")
        n2 = L("N2 gas", 38, N2C).move_to([4.4, 3.3, 0])
        self.play(FadeIn(n2), run_time=0.4)
        self.at("cannot")
        nu = L("a form it cannot use", 34, TEXT).move_to([4.4, 2.6, 0])
        self.play(FadeIn(nu), run_time=0.4)
        self.at("so")
        root = VMobject(color=ROOTC, stroke_width=9).set_points_as_corners([[-2.4, -0.9, 0], [-2.4, -1.9, 0], [-1.0, -2.2, 0]])
        nod = Circle(radius=0.9, stroke_color=SALM, stroke_width=5, fill_color=SALM, fill_opacity=0.2).move_to([0.0, -2.3, 0])
        bb = bacteroid_blobs([(-0.3, -2.2), (0.3, -2.4), (0.1, -1.9)], 0.4)
        self.play(FadeIn(root), FadeIn(nod), FadeIn(bb), run_time=0.7)
        self.at("carbon")
        toks = [path_dot([(-2.0, 1.4), (-2.4, 1.0), (-2.4, -1.9), (-1.0, -2.2)], 0.12, k / 4, ORANGE, 0.13, rev=False) for k in range(4)]
        outs = [path_dot([(-0.4, -1.6), (-1.9, -1.5), (-1.9, 0.9)], 0.1, k / 3, GREEN, 0.13, rev=False) for k in range(3)]
        lc = L("carbon", 36, ORANGE).move_to([-5.5, 0.3, 0])
        self.add(*toks)
        self.play(FadeIn(lc), run_time=0.4)
        self.at("partner")
        lp = L("partner", 36, PURP).move_to([2.3, -2.3, 0])
        self.play(FadeIn(lp), run_time=0.4)
        self.at("can use")
        self.add(*outs)
        la = L("ammonia", 36, GREEN).move_to([1.8, 0.4, 0])
        self.play(FadeIn(la), run_time=0.4)
        self.finish()


class S17End(EndCard):
    LINE = "A form the plant cannot use can be bought from a partner."
