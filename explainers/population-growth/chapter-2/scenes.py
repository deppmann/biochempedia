"""Population growth: Catching the Brake (film 2 of 2).

COLOUR MAP (same as film 1)
  WHITE  = N, population size and density (hare bars)
  TEAL   = per-capita rate or measure (fraction dying is per-capita)
  GOLD   = K, and the 'both' treatment outline
  ORANGE = total growth dN/dt (not used here)
Reef and forest cartoons are schematic; every line on a plot here is labelled schematic except film 1's
falling per-capita line, which is computed from r = 0.2 per day, K = 1000.
"""
import os, zlib
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
R, K, N0 = 0.2, 1000.0, 100.0
SAND, CORAL1, CORAL2, CORAL3, LEAF = "#C9B27C", "#E07A8A", "#9B72C9", "#F29E4C", "#2F7D4F"

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


def add_motes(scene, seed):
    rng = np.random.RandomState(zlib.crc32(seed.encode()) % 100000)
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
    scene.add(motes)


class Base(SpokenScene):
    def setup(self):
        super().setup()
        add_motes(self, os.environ.get("KX_SCENE_ID", "x"))

    def until(self, phrase, lead=0.25, lo=0.3, nth=0):
        return max(lo, self.t_of(phrase, nth) - lead - self.elapsed())


def bob(m, amp=0.05, speed=2.0, seed=0):
    rng = np.random.RandomState(seed)
    m.base = m.get_center().copy()
    m.ph = rng.uniform(0, 6.28)
    m.tt = 0.0

    def f(mm, dt):
        mm.tt += dt
        mm.move_to(mm.base + np.array([0.03 * np.sin(0.7 * speed * mm.tt + mm.ph), amp * np.sin(speed * mm.tt + mm.ph), 0]))
    m.add_updater(f)
    return m


def fish(color=BLUE, s=1.0, seed=0):
    body = Ellipse(width=0.5 * s, height=0.28 * s, fill_color=color, fill_opacity=1, stroke_width=0)
    tail = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.12 * s).rotate(-PI / 2).move_to(body.get_center() + LEFT * 0.3 * s)
    eye = Dot(radius=0.025 * s, color=BG).move_to(body.get_center() + RIGHT * 0.12 * s + UP * 0.03 * s)
    g = VGroup(body, tail, eye)
    return g


def hare(s=1.0):
    g = VGroup(Dot(radius=0.2 * s, color=WHITE),
               Ellipse(width=0.1 * s, height=0.34 * s, fill_color=WHITE, fill_opacity=1, stroke_width=0).shift(np.array([-0.1 * s, 0.3 * s, 0])),
               Ellipse(width=0.1 * s, height=0.34 * s, fill_color=WHITE, fill_opacity=1, stroke_width=0).shift(np.array([0.1 * s, 0.3 * s, 0])))
    return g


def cat(color, s=1.0):
    return VGroup(Dot(radius=0.2 * s, color=color),
                  Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.09 * s).shift(np.array([-0.13 * s, 0.22 * s, 0])),
                  Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.09 * s).shift(np.array([0.13 * s, 0.22 * s, 0])))


def pin(c, label, size=28):
    p = VGroup(Circle(radius=0.17, color=RED, fill_color=RED, fill_opacity=1, stroke_width=0).shift(UP * 0.3),
               Triangle(fill_color=RED, fill_opacity=1, stroke_width=0).scale(0.1).rotate(PI).shift(UP * 0.12))
    t = T(label, size, TEXT, weight=BOLD).next_to(p, RIGHT, buff=0.2)
    return VGroup(p, t).move_to(c)


def trees(center, w, h, n, seed=0):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        p = np.array([center[0] + rng.uniform(-w / 2 + .2, w / 2 - .2), center[1] + rng.uniform(-h / 2 + .25, h / 2 - .2), 0])
        g.add(Triangle(fill_color=LEAF, fill_opacity=0.85, stroke_width=0).scale(0.16).move_to(p))
    return g


def forest_block(center, w, h, n, seed=0, color=GREY):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=3, fill_color=LEAF, fill_opacity=0.12).move_to(center)
    return VGroup(box, trees(center, w, h, n, seed))


def reef(center, w, h, seed=0):
    rng = np.random.RandomState(seed)
    g = VGroup(Ellipse(width=w, height=h, fill_color=SAND, fill_opacity=0.3, stroke_color=SAND, stroke_width=2, stroke_opacity=0.5).move_to(center))
    for i, col in enumerate([CORAL1, CORAL2, CORAL3, CORAL1, CORAL2]):
        p = np.array([center[0] + rng.uniform(-w * 0.28, w * 0.28), center[1] + rng.uniform(-h * 0.12, h * 0.2), 0])
        g.add(Circle(radius=rng.uniform(0.12, 0.2) * min(w, 2.4) / 2.4 + 0.05, fill_color=col, fill_opacity=0.9, stroke_width=0).move_to(p))
    return g


def shoal(center, n, spread, seed=0, color=BLUE, s=1.0):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for i in range(n):
        p = np.array([center[0] + rng.uniform(-spread[0], spread[0]), center[1] + rng.uniform(-spread[1], spread[1]), 0])
        g.add(bob(fish(color, s).move_to(p), seed=seed * 50 + i))
    return g


def xmark(c, r=0.15, w=6):
    return VGroup(Line(c + np.array([-r, -r, 0]), c + np.array([r, r, 0])), Line(c + np.array([-r, r, 0]), c + np.array([r, -r, 0]))).set_stroke(RED, w)


def magnifier(c):
    g = VGroup(Circle(radius=0.6, color=WHITE, stroke_width=7, fill_color=WHITE, fill_opacity=0.08),
               Line([0.42, -0.42, 0], [1.0, -1.0, 0], color=WHITE, stroke_width=9))
    return g.move_to(c)


def pulse_q(m):
    m.base = m.get_center().copy()
    m.tt = 0.0
    m.add_updater(lambda mm, dt: (setattr(mm, "tt", mm.tt + dt), mm.move_to(mm.base + UP * 0.12 * np.sin(3 * mm.tt)))[0])
    return m


def pframe(P):
    return P


def draw_line(P, fn, x0, x1, color=TEAL, w=6, n=60, op=1.0):
    m = VMobject(stroke_color=color, stroke_width=w, stroke_opacity=op, fill_opacity=0)
    m.set_points_as_corners([P.pt(x, fn(x)) for x in np.linspace(x0, x1, n)])
    return m


def fall(N):
    return R * (1 - N / K)


def f_both(x):
    return 0.08 + 0.80 * x ** 0.85


def f_flat1(x):
    return 0.30 + 0.01 * x


def f_flat2(x):
    return 0.22 + 0.012 * x


# ---- shared layouts -------------------------------------------------------------------------
GX = {0: -2.7, 1: 1.9}
GY = {0: 1.25, 1: -1.55}
GW, GH = 4.4, 2.0
SQ = {"control": (0, 0), "food": (1, 0), "fence": (0, 1), "both": (1, 1)}


def sq_c(k):
    a, b = SQ[k]
    return np.array([GX[a], GY[b], 0.0])


def sq_label(k, text, color=TEXT, size=24):
    c = sq_c(k)
    return fit(T(text, size, color), max_w=GW - 0.1).move_to(c + UP * (GH / 2 + 0.28))


def forest_grid():
    sqs = {k: forest_block(sq_c(k), GW, GH, 7, seed=i + 3) for i, k in enumerate(SQ)}
    return sqs


# reef 2x2 grid for the predator crossing
def reef_sq(k):
    return reef(sq_c(k), GW - 0.3, GH - 0.1, seed=hash(k) % 7 if False else list(SQ).index(k) + 2)


# chapter-2 big plot (starting density vs fraction died)
CB = (-5.2, 2.6, -2.45, 2.25)


def dens_plot():
    return Plot(CB, (0, 1), (0, 1), [(0.05, "low"), (0.95, "high")], [(0, "0"), (0.5, "0.5"), (1, "1")],
                "starting density of young chromis", "fraction that died")


def badge():
    t = VGroup(T("per-capita measure:", 26, TEAL, weight=BOLD), T("fraction dying over", 24, TEAL), T("the study interval", 24, TEAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    return VGroup(SurroundingRectangle(t, color=TEAL, buff=0.22, corner_radius=0.12, stroke_width=3), t).move_to([4.65, 0.3, 0])


# mini plots for predict / reveal
MB = (1.3, 6.3, -2.0, 1.6)


def mini_plot():
    return Plot(MB, (0, 1), (0, 1), [(0.05, "low"), (0.95, "high")], [(0, "0"), (1, "1")], "starting density", "fraction died")


MSQ = {"none": (-5.2, 1.45), "res": (-2.4, 1.45), "tra": (-5.2, -0.65), "both": (-2.4, -0.65)}
MW, MH = 2.5, 1.5


def mini_sq(k, label, on=True, gold=False):
    c = np.array([MSQ[k][0], MSQ[k][1], 0.0])
    r = RoundedRectangle(corner_radius=0.1, width=MW, height=MH, stroke_color=GOLD if gold else GREY, stroke_width=4 if gold else 3,
                         fill_color=SAND, fill_opacity=0.2)
    r.move_to(c)
    cor = reef(c + DOWN * 0.1, MW - 0.4, MH - 0.5, seed=3)
    lab = T(label, 22, TEXT).move_to(c + UP * (MH / 2 + 0.25))
    return VGroup(r, cor, lab)


def predict_frame():
    sq = {"none": mini_sq("none", "no predators"), "res": mini_sq("res", "residents only"), "tra": mini_sq("tra", "transients only"),
          "both": mini_sq("both", "both", gold=True)}
    P = mini_plot()
    return sq, P


class S00Title(TitleCard):
    LESSON = "Population Growth and Regulation"
    TITLE = "Catching the Brake"


class S01Link(Base):
    def construct(self):
        P = Plot((-4.6, 4.2, -2.4, 2.3), (0, 1200), (-0.05, 0.25), [(0, "0"), (500, "500"), (1000, "1000")],
                 [(0, "0"), (0.1, "0.1"), (0.2, "0.2")], "N", "per-capita rate (per day)")
        self.play(FadeIn(P.parts), run_time=0.5)
        kl = DashedLine(P.pt(1000, -0.05), P.pt(1000, 0.25), color=GOLD, stroke_width=5)
        kt = T("K", 32, GOLD, weight=BOLD).next_to(P.pt(1000, 0.25), UP, buff=0.1)
        self.play(Create(kl), FadeIn(kt), run_time=0.4)
        self.at("tilted")
        line = Line(P.pt(0, R), P.pt(1200, fall(1200)), color=TEAL, stroke_width=6)
        glass = magnifier(P.pt(0, R) + UP * 0.1)
        self.play(Create(line, rate_func=linear), run_time=1.8)
        self.at("assumption")
        self.play(FadeIn(glass), run_time=0.4)
        self.play(glass.animate.move_to(P.pt(1000, fall(1000)) + UP * 0.1), run_time=self.until("real forest", lo=0.5), rate_func=smooth)
        forest = forest_block([-3.4, 0.2, 0], 6.6, 4.6, 26, seed=8)
        fl = T("forest", 34, WHITE, weight=BOLD).move_to([-3.4, -2.75, 0])
        self.play(FadeOut(VGroup(P.parts, kl, kt, line)), FadeIn(forest), FadeIn(fl), glass.animate.move_to([-3.4, 0.4, 0]), run_time=1.4)
        self.at("real reef")
        rf = reef([3.5, 0.2, 0], 6.2, 4.4, seed=11)
        rl = T("reef", 34, WHITE, weight=BOLD).move_to([3.5, -2.75, 0])
        fsh = shoal([3.5, 0.5, 0], 6, (2.2, 1.0), seed=5)
        self.play(FadeIn(rf), FadeIn(rl), FadeIn(fsh), run_time=1.2)
        self.at("how would you")
        self.play(glass.animate.move_to([3.5, 0.5, 0]), run_time=self.until("tilting", lo=1.0), rate_func=smooth)
        q = pulse_q(T("?", 90, GOLD, weight=BOLD).move_to([0, 0.3, 0]))
        self.at("tilting")
        self.play(FadeIn(q), run_time=0.6)
        self.finish()


class S02Kluane(Base):
    def construct(self):
        ctr = np.array([0.6, -0.3, 0])
        forest = forest_block([-3.6, 0.3, 0], 5.4, 4.6, 20, seed=12)
        self.play(FadeIn(forest), run_time=0.5)
        self.at("Yukon")
        pn = pin([-3.6, 2.95, 0], "Kluane Lake, Yukon")
        self.play(FadeIn(pn, shift=DOWN * 0.2), run_time=0.9)
        self.at("snowshoe")
        # schematic cycle: a wave of hare density over about a decade
        wave = FunctionGraph(lambda x: 0.95 * np.sin(1.5 * x) ** 2 * np.exp(-0.0 * x), x_range=[0, 6.8], color=WHITE, stroke_width=6)
        wave.move_to([3.3, -0.8, 0])
        base = Line(wave.get_start() + DOWN * 0.1 + LEFT * 0.0, wave.get_end() + DOWN * 0.1, color=GREY, stroke_width=3)
        base.move_to(wave.get_bottom() + DOWN * 0.05)
        h = hare(1.6)
        h.move_to([-3.6, 0.3, 0])
        self.play(FadeIn(h, scale=0.4), Create(base), run_time=0.8)
        tr = ValueTracker(0)
        self.play(Create(wave, rate_func=linear), run_time=1.8)
        dot = always_redraw(lambda: Dot(wave.point_from_proportion(tr.get_value() % 1.0), radius=0.14, color=ORANGE))
        self.add(dot)
        self.play(tr.animate(run_time=1.0, rate_func=linear).set_value(0.5))
        self.at("decade")
        lab = VGroup(T("cycle of roughly a decade", 30, WHITE, weight=BOLD), T("(schematic)", 24, GREY)).arrange(DOWN, buff=0.1).move_to([3.3, 2.2, 0])
        self.play(FadeIn(lab), tr.animate(run_time=2.0, rate_func=linear).set_value(1.5), run_time=2.0)
        self.finish()


class S03Design(Base):
    def construct(self):
        sqs = forest_grid()
        self.play(LaggedStart(*[FadeIn(sqs[k]) for k in SQ], lag_ratio=0.2), run_time=1.6)
        self.at("blocks of forest")
        note = VGroup(T("blocks about", 28, TEXT), T("1 km²", 34, WHITE, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([5.5, 1.1, 0])
        self.play(FadeIn(note), run_time=0.7)
        lc = sq_label("control", "control")
        self.at("added food", lead=0.4)
        lf = sq_label("food", "food added")
        feed = VGroup(*[Dot(radius=0.07, color="#E0C050").move_to(sq_c("food") + np.array([-1.8 + 0.55 * i, -0.75 + 0.2 * (i % 2), 0])) for i in range(7)])
        self.play(FadeIn(lf), FadeIn(feed), run_time=0.7)
        self.at("fenced")
        fence = DashedLine(sq_c("fence") + np.array([-GW / 2, -GH / 2, 0]), sq_c("fence") + np.array([-GW / 2, GH / 2, 0]), color=WHITE, stroke_width=6)
        fence = VGroup(*[DashedVMobject(Rectangle(width=GW + 0.15, height=GH + 0.15, color=WHITE, stroke_width=6).move_to(sq_c("fence")), num_dashes=40)])
        lfn = sq_label("fence", "predators fenced out")
        lynx = VGroup(cat(ORANGE, 1.2), T("lynx", 24, ORANGE)).arrange(DOWN, buff=0.1).move_to([-5.8, -1.0, 0])
        coy = VGroup(cat(GREY, 1.2), T("coyote", 24, GREY)).arrange(DOWN, buff=0.1).move_to([-5.8, -2.55, 0])
        self.play(FadeIn(lfn), Create(fence), FadeIn(lynx), FadeIn(coy), run_time=1.0)
        self.at("did both")
        lb = sq_label("both", "both", GOLD)
        fence2 = DashedVMobject(Rectangle(width=GW + 0.15, height=GH + 0.15, color=WHITE, stroke_width=6).move_to(sq_c("both")), num_dashes=40)
        feed2 = VGroup(*[Dot(radius=0.07, color="#E0C050").move_to(sq_c("both") + np.array([-1.8 + 0.55 * i, -0.75 + 0.2 * (i % 2), 0])) for i in range(7)])
        gold = RoundedRectangle(corner_radius=0.1, width=GW, height=GH, stroke_color=GOLD, stroke_width=6).move_to(sq_c("both"))
        self.play(FadeIn(lb), Create(fence2), FadeIn(feed2), Create(gold), run_time=0.7)
        self.at("did neither")
        self.play(FadeIn(lc), Indicate(sqs["control"], color=WHITE, scale_factor=1.04), run_time=1.0)
        ey = T("eight years", 34, WHITE, weight=BOLD).move_to([5.7, -0.3, 0])
        self.play(FadeIn(ey, shift=UP * 0.1), run_time=0.8)
        self.finish()


def build_grid(scene, labels=True, predators=True):
    """The Kluane grid exactly as in S03; returns a dict of the pieces."""
    sqs = forest_grid()
    d = {"sqs": sqs}
    allm = VGroup(*sqs.values())
    labs = VGroup(sq_label("control", "control"), sq_label("food", "food added"), sq_label("fence", "predators fenced out"), sq_label("both", "both", GOLD))
    feed = VGroup(*[Dot(radius=0.07, color="#E0C050").move_to(sq_c(k) + np.array([-1.8 + 0.55 * i, -0.75 + 0.2 * (i % 2), 0])) for k in ("food", "both") for i in range(7)])
    fences = VGroup(*[DashedVMobject(Rectangle(width=GW + 0.15, height=GH + 0.15, color=WHITE, stroke_width=6).move_to(sq_c(k)), num_dashes=40) for k in ("fence", "both")])
    gold = RoundedRectangle(corner_radius=0.1, width=GW, height=GH, stroke_color=GOLD, stroke_width=6).move_to(sq_c("both"))
    scene.add(allm, labs, feed, fences, gold)
    d.update(labs=labs, feed=feed, fences=fences, gold=gold)
    if predators:
        lynx = VGroup(cat(ORANGE, 1.2), T("lynx", 24, ORANGE)).arrange(DOWN, buff=0.1).move_to([-5.8, -1.0, 0])
        coy = VGroup(cat(GREY, 1.2), T("coyote", 24, GREY)).arrange(DOWN, buff=0.1).move_to([-5.8, -2.55, 0])
        scene.add(lynx, coy)
        d.update(lynx=lynx, coy=coy)
    return d


class S04Bars(Base):
    def construct(self):
        g = build_grid(self)
        self.play(FadeOut(g["feed"]), run_time=0.5)
        unit = 0.16
        vals = {"control": 1, "fence": 2, "food": 3, "both": 11}
        txt = {"control": "= 1", "fence": "about 2x", "food": "about 3x", "both": "about 11x"}
        bars = {}
        for k, v in vals.items():
            c = sq_c(k)
            b = Rectangle(width=0.55, height=unit * v, stroke_width=0, fill_color=WHITE, fill_opacity=0.95)
            b.move_to([c[0] + 1.7, c[1] - GH / 2 + 0.1 + unit * v / 2, 0])
            bars[k] = b
        lab = {k: T(txt[k], 28, WHITE, weight=BOLD).move_to(sq_c(k) + np.array([-0.5, 0.1, 0])).set_stroke("#0B1A14", width=8, background=True).set_z_index(5) for k in vals}
        ctrl_grow = bars["control"]
        self.play(FadeIn(bars["control"]), FadeIn(lab["control"]), run_time=0.8)
        self.at("fencing out")
        self.play(GrowFromEdge(bars["fence"], DOWN), FadeIn(lab["fence"]), run_time=1.4)
        self.at("so did food")
        self.play(GrowFromEdge(bars["food"], DOWN), FadeIn(lab["food"]), run_time=1.4)
        self.at("doing both")
        self.play(GrowFromEdge(bars["both"], DOWN), FadeIn(lab["both"]), run_time=2.2)
        cite = VGroup(T("Krebs et al.,", 26, TEXT), T("Science, 1995", 26, TEXT)).arrange(DOWN, buff=0.08).move_to([5.5, 0.0, 0])
        self.play(FadeIn(cite), run_time=0.8)
        self.finish()


class S05Limits(Base):
    def construct(self):
        g = build_grid(self, predators=False)
        unit = 0.16
        vals = {"control": 1, "fence": 2, "food": 3, "both": 11}
        txt = {"control": "= 1", "fence": "about 2x", "food": "about 3x", "both": "about 11x"}
        for k, v in vals.items():
            c = sq_c(k)
            b = Rectangle(width=0.55, height=unit * v, stroke_width=0, fill_color=WHITE, fill_opacity=0.95)
            b.move_to([c[0] + 1.7, c[1] - GH / 2 + 0.1 + unit * v / 2, 0])
            self.add(b, T(txt[k], 28, WHITE, weight=BOLD).move_to(c + np.array([-0.5, 0.1, 0])).set_stroke("#0B1A14", width=8, background=True).set_z_index(5))
        self.remove(g["feed"])
        self.at("both limited")
        self.play(Indicate(g["gold"], color=GOLD, scale_factor=1.04), run_time=1.0)
        self.at("but were individuals")
        P = Plot((5.1, 6.7, -1.3, 1.5), (0, 1), (0, 1), [], [], "density", "per-capita")
        P.parts[-2].set_color(GREY)
        ql = draw_line(P, lambda x: 0.8 - 0.4 * x if False else 0.5, 0, 1, TEAL, 6, op=0.4)
        q = pulse_q(T("?", 90, GOLD, weight=BOLD).move_to(P.pt(0.5, 0.78)))
        self.play(FadeIn(P.parts), Create(DashedVMobject(ql, num_dashes=14)), FadeIn(q), run_time=1.4)
        cap = T("more hares, but are individuals doing worse at high density?", 28, WHITE)
        cap2 = T("These counts cannot say.", 30, GOLD, weight=BOLD)
        cg = VGroup(cap, cap2).arrange(DOWN, buff=0.12).move_to([-0.3, -3.2, 0])
        fit(cg, max_w=11.8)
        self.play(Write(cap), run_time=2.6)
        self.at("counts of")
        self.play(Write(cap2), run_time=1.2)
        self.finish()


class S06Reef(Base):
    def construct(self):
        rfs = [reef([-4.1 + 4.1 * i, 0.2 - 0.25 * (i % 2), 0], 3.8, 2.6, seed=20 + i) for i in range(3)]
        shoals = [shoal([-4.1 + 4.1 * i, 0.4 - 0.25 * (i % 2), 0], 4, (1.0, 0.5), seed=30 + i) for i in range(3)]
        self.play(LaggedStart(*[FadeIn(r) for r in rfs], lag_ratio=0.2), run_time=1.0)
        self.add(*shoals)
        self.at("per capita rate")
        t = VGroup(T("per-capita rate", 38, TEAL, weight=BOLD), T("at several densities", 30, TEXT)).arrange(DOWN, buff=0.1).move_to([0, 2.8, 0])
        self.play(FadeIn(t, shift=DOWN * 0.15), run_time=0.9)
        self.at("Hickson")
        nc = VGroup(T("Hixon and Carr", 32, WHITE, weight=BOLD), T("Science, 1997", 28, TEXT)).arrange(DOWN, buff=0.08).move_to([0, -2.4, 0])
        self.play(FadeOut(t), FadeIn(nc), run_time=1.0)
        self.at("Bahamas")
        pn = pin([0, -3.4, 0], "Lee Stocking Island, Bahamas", 28)
        self.play(FadeIn(pn, shift=UP * 0.15), run_time=0.9)
        self.finish()


class S07Percap(Base):
    def construct(self):
        c = np.array([-2.4, 0.1, 0])
        rf = reef(c, 6.4, 4.2, seed=40)
        pos = [c + np.array([-2.0 + 1.0 * (i % 5), 0.7 - 1.1 * (i // 5) + 0.15 * (i % 2), 0]) for i in range(10)]
        fs = VGroup(*[bob(fish(BLUE, 1.5).move_to(p), seed=70 + i, amp=0.07) for i, p in enumerate(pos)])
        self.play(FadeIn(rf), LaggedStart(*[FadeIn(f, scale=0.5) for f in fs], lag_ratio=0.1), run_time=2.0)
        self.at("outcomes")
        self.play(Indicate(fs, color=BLUE, scale_factor=1.05), run_time=1.0)
        self.at("not heads")
        heads = M("10 fish", 34, GREY).move_to([4.3, -1.7, 0])
        self.play(FadeIn(heads), run_time=0.8)
        self.at("fraction")
        dead = [2, 5, 8]
        for i in dead:
            fs[i].clear_updaters()
        xs = VGroup(*[xmark(fs[i].get_center()) for i in dead])
        frac = VGroup(T("3 of 10 died", 36, TEAL, weight=BOLD), M("= 0.3", 38, TEAL)).arrange(DOWN, buff=0.15).move_to([4.3, 0.9, 0])
        sch = T("(schematic numbers)", 22, GREY).move_to([4.3, -2.5, 0])
        self.play(*[fs[i].animate.set_opacity(0.3) for i in dead], FadeIn(xs), FadeIn(frac), FadeIn(sch), run_time=1.6)
        self.at("on each reef")
        self.play(Indicate(frac, color=TEAL, scale_factor=1.08), run_time=1.0)
        self.finish()


class S08Stock(Base):
    def construct(self):
        cs = [-4.4, 0.0, 4.4]
        rfs = [reef([x, -0.2, 0], 3.9, 3.2, seed=20 + i) for i, x in enumerate(cs)]
        self.play(LaggedStart(*[FadeIn(r) for r in rfs], lag_ratio=0.15), run_time=0.5)
        self.at("stocked")
        counts = [3, 8, 16]
        shs = [shoal([x, -0.1, 0], n, (1.3, 0.8), seed=90 + i, s=1.4) for i, (x, n) in enumerate(zip(cs, counts))]
        self.play(FadeIn(shs[0], scale=0.6), run_time=1.0)
        self.add(shs[1], shs[2])
        shs[1].set_opacity(0)
        shs[2].set_opacity(0)
        self.at("different densities")
        labs = [T(w, 38, WHITE, weight=BOLD).move_to([x, -2.6, 0]) for w, x in zip(["low", "medium", "high"], cs)]
        sub = T("starting density", 30, TEAL).move_to([0, 3.0, 0])
        self.play(FadeIn(sub), run_time=0.7)
        self.at("few")
        self.play(FadeIn(labs[0]), run_time=0.6)
        self.play(shs[1].animate.set_opacity(1), FadeIn(labs[1]), run_time=1.0)
        self.at("some got many")
        self.play(shs[2].animate.set_opacity(1), FadeIn(labs[2]), run_time=1.2)
        self.finish()


class S09Predators(Base):
    def construct(self):
        names = {"control": "no predators", "food": "residents only", "fence": "transients only", "both": "both"}
        rs = {k: reef_sq(k) for k in SQ}
        labs = {k: sq_label(k, names[k], GOLD if k == "both" else TEXT) for k in SQ}
        self.play(LaggedStart(*[FadeIn(rs[k]) for k in SQ], lag_ratio=0.15), run_time=1.4)
        self.at("two kinds of predator")
        self.play(FadeIn(labs["control"]), run_time=0.6)
        gold = RoundedRectangle(corner_radius=0.1, width=GW, height=GH, stroke_color=GOLD, stroke_width=6).move_to(sq_c("both"))
        self.at("Residents")
        res_c = lambda k, dx=0.0: sq_c(k) + np.array([dx, -0.1, 0])
        pr = fish(RED, 1.8).move_to(res_c("food"))
        crev = Arc(radius=0.6, start_angle=0, angle=PI, color=GREY, stroke_width=6).move_to(res_c("food") + DOWN * 0.12)
        pr2 = fish(RED, 1.8).move_to(res_c("both", -0.8))
        self.play(FadeIn(labs["food"]), FadeIn(pr), Create(crev), run_time=1.0)
        self.play(FadeIn(pr2, scale=0.5), run_time=0.7)
        self.at("Tranients")
        pt = fish(RED, 1.8).move_to(sq_c("fence") + np.array([-2.6, 0.1, 0]))
        pt2 = fish(RED, 1.8).move_to(sq_c("both") + np.array([-2.6, 0.1, 0]))
        ar = Arrow(pt.get_right(), sq_c("fence") + np.array([-0.2, 0.1, 0]), color=RED, buff=0.1, stroke_width=6)
        self.play(FadeIn(labs["fence"]), FadeIn(pt), GrowArrow(ar), run_time=1.0)
        self.play(pt.animate.move_to(sq_c("fence") + np.array([0.9, 0.2, 0])), run_time=1.6, rate_func=smooth)
        self.at("move between")
        self.play(pt.animate.move_to(sq_c("fence") + np.array([1.6, -0.3, 0])), FadeIn(pt2), FadeIn(labs["both"]), Create(gold), run_time=0.8)
        self.play(pt2.animate.move_to(sq_c("both") + np.array([0.7, 0.3, 0])), run_time=1.4)
        self.finish()


class S10Axes(Base):
    def construct(self):
        P = dens_plot()
        self.play(FadeIn(P.parts), run_time=1.4)
        self.at("fraction of young")
        fl = T("fraction of young fish that died", 30, WHITE).move_to([4.6, 2.2, 0])
        fl.set_width(min(fl.width, 3.9))
        fl = VGroup(T("fraction of", 30, WHITE), T("young fish", 30, WHITE), T("that died", 30, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.9, 1.9, 0])
        self.play(FadeIn(fl, shift=LEFT * 0.2), run_time=0.9)
        self.at("starting density")
        sf = shoal([P.pt(0.5, 0.0)[0], -3.4, 0], 0, (0, 0), seed=1)
        xl = SurroundingRectangle(P.parts[-2], color=WHITE, buff=0.12, corner_radius=0.1, stroke_width=3)
        self.play(Create(xl), run_time=0.8)
        self.at("per capita measure")
        b = badge().move_to([4.9, -0.7, 0])
        self.play(FadeOut(xl), FadeIn(b), run_time=1.0)
        self.at("teal")
        self.play(Indicate(b, color=TEAL, scale_factor=1.06), run_time=1.0)
        self.finish()


def plot_with_axes(scene):
    P = dens_plot()
    scene.add(P.parts)
    return P


class S11Both(Base):
    def construct(self):
        P = plot_with_axes(self)
        lab = VGroup(T("both predator", 30, TEAL, weight=BOLD), T("groups: rising", 30, TEAL, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.0, 1.2, 0])
        sch = T("(schematic, not the paper's data)", 22, GREY).move_to([4.7, -1.9, 0])
        sch.set_width(3.9)
        self.add(badge().move_to([4.9, -0.7, 0]).scale(0.0001)) if False else None
        self.play(FadeIn(lab), FadeIn(sch), run_time=1.2)
        tr = ValueTracker(0)
        self.at("line rose")
        line = always_redraw(lambda: draw_line(P, f_both, 0, max(tr.get_value(), 0.001), TEAL, 7, n=40))
        dot = always_redraw(lambda: Dot(P.pt(tr.get_value(), f_both(tr.get_value())), radius=0.13, color=WHITE, stroke_color=TEAL, stroke_width=3))
        self.add(line, dot)
        self.play(tr.animate(run_time=1.9, rate_func=linear).set_value(1.0))
        self.at("the more young fish")
        self.play(tr.animate(run_time=1.6, rate_func=smooth).set_value(0.1))
        self.play(tr.animate(run_time=self.until("larger the share", lo=0.5), rate_func=linear).set_value(0.7))
        self.at("larger the share")
        self.play(tr.animate(run_time=1.4, rate_func=smooth).set_value(1.0))
        mk = VGroup(T("more fish", 28, WHITE), T("larger share died", 28, TEAL)).arrange(DOWN, buff=0.1).move_to([0.2, -0.9, 0])
        self.play(FadeIn(mk), run_time=0.8)
        self.finish()


class S12Dd(Base):
    def construct(self):
        P = plot_with_axes(self)
        line = draw_line(P, f_both, 0, 1, TEAL, 7)
        dot = Dot(P.pt(1, f_both(1)), radius=0.13, color=WHITE, stroke_color=TEAL, stroke_width=3)
        sch = T("(schematic, not the paper's data)", 22, GREY).move_to([4.7, -1.9, 0])
        sch.set_width(3.9)
        self.add(line, dot, sch)
        lab = VGroup(T("both predator", 30, TEAL, weight=BOLD), T("groups: rising", 30, TEAL, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.0, 1.2, 0])
        self.add(lab)
        tr = ValueTracker(0.2)
        sl = always_redraw(lambda: Dot(P.pt(tr.get_value(), f_both(tr.get_value())), radius=0.13, color=WHITE, stroke_color=TEAL, stroke_width=3))
        self.add(sl)
        self.play(tr.animate(run_time=2.0, rate_func=linear).set_value(1.0))
        self.at("density")
        st = T("density-dependent mortality", 28, WHITE, weight=BOLD)
        stamp = VGroup(SurroundingRectangle(st, color=TEAL, buff=0.2, corner_radius=0.1, stroke_width=5), st).rotate(0.06).move_to([-1.45, 1.6, 0])
        self.play(FadeIn(stamp, scale=1.5), tr.animate(run_time=1.2, rate_func=smooth).set_value(0.4), run_time=0.7)
        self.play(tr.animate(run_time=1.6, rate_func=linear).set_value(1.0))
        self.at("Predators")
        r1 = fish(RED, 1.8)
        r2 = fish(RED, 1.8)
        row = VGroup(T("resident", 26, TEXT), r1, T("+", 40, WHITE), r2, T("transient", 26, TEXT)).arrange(RIGHT, buff=0.25).move_to([0.5, -1.45, 0])
        self.play(FadeIn(row, shift=UP * 0.15), run_time=1.0)
        self.at("together")
        self.play(Indicate(row[2], color=WHITE, scale_factor=1.6), tr.animate(run_time=2.0, rate_func=linear).set_value(0.3), run_time=2.0)
        self.finish()


class S13Predict(Base):
    def construct(self):
        sq, P = predict_frame()
        self.add(P.parts)
        for k in ("none", "res", "tra", "both"):
            self.add(sq[k])
        self.at("take away")
        self.play(sq["both"].animate.set_opacity(0.3), run_time=1.0)
        self.at("either one")
        glow = [SurroundingRectangle(sq[k][0], color=TEAL, buff=0.06, corner_radius=0.1, stroke_width=6) for k in ("res", "tra")]
        self.play(*[Create(g) for g in glow], run_time=1.0)
        q = pulse_q(T("?", 110, TEAL, weight=BOLD).move_to(P.pt(0.5, 0.55)))
        self.at("does the teal")
        self.play(FadeIn(q), run_time=0.8)
        self.at("still rise")
        self.play(Indicate(q, color=TEAL, scale_factor=1.3), run_time=1.2)
        self.finish()


class S14Pause(NarratedScene):
    def setup(self):
        super().setup()
        add_motes(self, "s14")

    def construct(self):
        sq, P = predict_frame()
        self.add(P.parts)
        for k in ("none", "res", "tra", "both"):
            self.add(sq[k])
        sq["both"].set_opacity(0.3)
        for k in ("res", "tra"):
            self.add(SurroundingRectangle(sq[k][0], color=TEAL, buff=0.06, corner_radius=0.1, stroke_width=6))
        q = pulse_q(T("?", 110, TEAL, weight=BOLD).move_to(P.pt(0.5, 0.55)))
        self.add(q)
        cap = T("Predict: with one predator group, does the line still rise?", 30, GOLD, weight=BOLD)
        fit(cap, max_w=12.2)
        cap.move_to([0, -3.15, 0])
        c0 = np.array([5.9, 3.2, 0])
        pr = ValueTracker(1.0)
        ring = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=max(pr.get_value(), 0.001) * TAU, color=GOLD, stroke_width=8, arc_center=c0))
        self.add(cap, ring)
        self.play(pr.animate(run_time=4.6, rate_func=linear).set_value(0.0))
        self.finish()


class S15Reveal(Base):
    def construct(self):
        sq, P = predict_frame()
        self.add(P.parts)
        for k in ("none", "res", "tra", "both"):
            self.add(sq[k])
        sq["both"].set_opacity(0.3)
        for k in ("res", "tra"):
            self.add(SurroundingRectangle(sq[k][0], color=TEAL, buff=0.06, corner_radius=0.1, stroke_width=6))
        self.at("no rise")
        l1 = draw_line(P, f_flat1, 0, 1, TEAL, 7)
        l2 = draw_line(P, f_flat2, 0, 1, TEAL, 7)
        self.play(Create(l1, rate_func=linear), Create(l2, rate_func=linear), run_time=2.0)
        self.at("low statistical power")
        top = [P.pt(x, f_flat1(x) + 0.18) for x in np.linspace(0, 1, 20)]
        bot = [P.pt(x, f_flat1(x) - 0.16) for x in np.linspace(1, 0, 20)]
        band = Polygon(*(top + bot), stroke_width=0, fill_color=GREY, fill_opacity=0.35)
        tag = T("low power", 30, WHITE, weight=BOLD)
        tg = VGroup(SurroundingRectangle(tag, color=GREY, buff=0.15, corner_radius=0.1, stroke_width=3), tag).move_to(P.pt(0.5, 0.78))
        self.play(FadeIn(band), FadeIn(tg), run_time=1.2)
        self.at("too little data")
        self.play(Indicate(band, color=WHITE, scale_factor=1.05), run_time=1.2)
        self.at("not detected")
        cap = T("not detected is not absent", 40, GOLD, weight=BOLD).move_to([0, -3.15, 0])
        self.play(Write(cap), run_time=2.0)
        self.play(Indicate(cap, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.finish()


class S16Fraction(Base):
    def construct(self):
        cl, cr = np.array([-3.4, 0.0, 0]), np.array([3.4, 0.0, 0])
        rl, rr = reef(cl, 5.2, 4.0, seed=50), reef(cr, 5.2, 4.0, seed=51)
        fl = VGroup(*[bob(fish(BLUE, 1.5).move_to(cl + np.array([-1.1 + 1.1 * (i % 3), 0.5 - 1.0 * (i // 3) + 0.4, 0])), seed=200 + i) for i in range(5)])
        pr = [(-1.8 + 0.9 * (i % 5), 1.0 - 0.9 * (i // 5)) for i in range(15)][:15]
        fr = VGroup(*[bob(fish(BLUE, 1.2).move_to(cr + np.array([-1.8 + 0.9 * (i % 5), 1.1 - 0.9 * (i // 5), 0])), seed=300 + i) for i in range(15)])
        sch = T("(schematic numbers)", 22, GREY).move_to([0, 3.4, 0])
        self.play(FadeIn(rl), FadeIn(rr), FadeIn(fl), FadeIn(fr), FadeIn(sch), run_time=1.2)
        self.at("not more deaths")
        # left: 1 of 4 died
        fl[1].clear_updaters()
        x1 = xmark(fl[1].get_center())
        t1 = M("1 of 5 died", 30, TEAL).move_to([-3.4, -2.55, 0])
        for i in (2, 7, 12):
            fr[i].clear_updaters()
        xs = VGroup(*[xmark(fr[i].get_center()) for i in (2, 7, 12)])
        t2 = M("3 of 15 died", 30, TEAL).move_to([3.4, -2.55, 0])
        self.play(fl[1].animate.set_opacity(0.3), FadeIn(x1), FadeIn(t1), run_time=0.6)
        self.play(*[fr[i].animate.set_opacity(0.3) for i in (2, 7, 12)], FadeIn(xs), FadeIn(t2), run_time=0.8)
        same = T("more deaths, same fraction: no tilt", 30, WHITE, weight=BOLD).move_to([0, -3.3, 0])
        self.play(FadeIn(same), run_time=0.5)
        self.at("larger fraction")
        extra = (0, 4, 9, 14)
        for i in extra:
            fr[i].clear_updaters()
        xs2 = VGroup(*[xmark(fr[i].get_center()) for i in extra])
        t3 = M("7 of 15 died", 30, TEAL).move_to([3.4, -2.55, 0])
        same2 = T("larger fraction: a tilt", 34, GOLD, weight=BOLD).move_to([0, -3.3, 0])
        self.play(*[fr[i].animate.set_opacity(0.3) for i in extra], FadeIn(xs2), Transform(t2, t3), Transform(same, same2), run_time=2.2)
        self.finish()


class S17Two(Base):
    def construct(self):
        # left: white Kluane bars
        x0, y0 = -5.9, -2.0
        base = Line([x0, y0, 0], [-0.9, y0, 0], color=GREY, stroke_width=3)
        unit = 0.26
        vals = [("control", 1), ("fenced", 2), ("food", 3), ("both", 11)]
        bars = VGroup(*[Rectangle(width=0.8, height=unit * v, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([x0 + 0.8 + 1.15 * i, y0 + unit * v / 2, 0]) for i, (n, v) in enumerate(vals)])
        vl = VGroup(*[T(f"{v}x" if v > 1 else "1", 28, WHITE).next_to(bars[i], UP, buff=0.1) for i, (n, v) in enumerate(vals)])
        self.at("hares")
        self.play(FadeIn(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(vl), run_time=0.8)
        # right: rising teal line
        P = Plot((1.7, 6.3, -2.0, 1.4), (0, 1), (0, 1), [], [], "starting density", "fraction died")
        P.parts[-2].set_color(GREY)
        self.at("the chromis")
        line = draw_line(P, f_both, 0, 1, TEAL, 7)
        self.play(FadeIn(P.parts), Create(line, rate_func=linear), run_time=1.4)
        sc = T("(schematic)", 22, GREY).move_to([5.3, -1.2, 0])
        self.add(sc)
        self.at("two different questions")
        self.play(Indicate(bars, color=WHITE, scale_factor=1.03), Indicate(line, color=TEAL, scale_factor=1.03), run_time=0.9)
        self.at("showed what limited")
        ll = VGroup(T("treatments vs control:", 28, WHITE, weight=BOLD), T("what limits", 32, WHITE, weight=BOLD)).arrange(DOWN, buff=0.08).move_to([-3.4, 1.9, 0])
        self.play(FadeIn(ll, shift=DOWN * 0.15), run_time=1.0)
        self.at("density dependence")
        rl = VGroup(T("per-capita deaths:", 28, TEAL, weight=BOLD), T("density dependence", 30, TEAL, weight=BOLD), T("one generation, across reefs", 24, TEAL)).arrange(DOWN, buff=0.08).move_to([4.0, 2.5, 0])
        rl.move_to([4.0, 2.75, 0])
        self.play(FadeIn(rl, shift=DOWN * 0.15), run_time=1.0)
        self.finish()


class S18Rule(Base):
    def construct(self):
        LP = Plot((-6.0, -1.3, -2.1, 1.8), (0, 1200), (-0.05, 0.25), [(0, "0"), (500, "500"), (1000, "1000")], [(0, "0"), (0.2, "0.2")], "N", "net per-capita growth")
        RP = Plot((1.7, 6.3, -2.1, 1.8), (0, 1), (0, 1), [], [], "starting density", "fraction died")
        RP.parts[-2].set_color(GREY)
        rline = draw_line(RP, f_both, 0, 1, TEAL, 7)
        self.add(RP.parts, rline, T("(schematic)", 22, GREY).move_to(RP.pt(0.25, 0.9)))
        self.at("negative density")
        kl = DashedLine(LP.pt(1000, -0.05), LP.pt(1000, 0.25), color=GOLD, stroke_width=5)
        fline = Line(LP.pt(0, R), LP.pt(1200, fall(1200)), color=TEAL, stroke_width=7)
        self.play(FadeIn(LP.parts), Create(kl), run_time=0.9)
        self.play(Create(fline, rate_func=linear), run_time=1.6)
        y = 2.55
        x0, x1 = LP.pt(0, 0)[0], LP.pt(1200, 0)[0]
        br = VGroup(Line([x0, y, 0], [x1, y, 0]), Line([x0, y, 0], [x0, y - 0.2, 0]), Line([x1, y, 0], [x1, y - 0.2, 0])).set_stroke(GOLD, 6)
        bl = VGroup(T("negative density dependence:", 28, GOLD, weight=BOLD), T("a brake", 34, GOLD, weight=BOLD)).arrange(DOWN, buff=0.08).move_to([(x0 + x1) / 2, 3.25, 0])
        self.play(Create(br), FadeIn(bl), run_time=1.0)
        self.at("deaths rise")
        dl = T("death part of the net rate", 26, TEAL, weight=BOLD).move_to([4.0, 2.65, 0])
        tr = ValueTracker(0)
        dd = always_redraw(lambda: Dot(RP.pt(tr.get_value(), f_both(tr.get_value())), radius=0.13, color=WHITE, stroke_color=TEAL, stroke_width=3))
        self.add(dd)
        self.play(FadeIn(dl), tr.animate(run_time=2.0, rate_func=linear).set_value(1.0))
        self.at("net per capita growth")
        t2 = ValueTracker(0)
        d2 = always_redraw(lambda: Dot(LP.pt(t2.get_value() * 1200, fall(t2.get_value() * 1200)), radius=0.13, color=WHITE, stroke_color=TEAL, stroke_width=3))
        self.add(d2)
        self.play(t2.animate(run_time=2.2, rate_func=linear).set_value(1.0))
        self.at("measuring")
        cap = T("per-capita, changing with density", 28, TEAL, weight=BOLD)
        cap2 = cap.copy()
        fit(cap, max_w=5.0)
        fit(cap2, max_w=5.0)
        cap.move_to([-3.65, -3.4, 0])
        cap2.move_to([4.0, -3.4, 0])
        self.play(FadeIn(cap), FadeIn(cap2), run_time=1.0)
        self.play(tr.animate(run_time=1.5, rate_func=linear).set_value(0.0), t2.animate(run_time=1.5, rate_func=linear).set_value(0.0))
        self.play(tr.animate(run_time=1.5, rate_func=linear).set_value(1.0), t2.animate(run_time=1.5, rate_func=linear).set_value(1.0))
        self.finish()


class S19End(EndCard):
    LINE = "A brake makes net per-capita growth fall as density rises."
