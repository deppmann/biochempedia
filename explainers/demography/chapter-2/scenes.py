"""Demography, chapter 2: A Straight Line on a Log Axis  (Biochemistrypedia film)

COLOR MAP (same as chapter 1, one colour per concept)
  TEAL   = survivors, l_x (the survival line and points); the Hydra line
  GOLD   = births (Hydra buds)
  GREY   = a death (dot fades grey, grey bar), frames, axes
  YELLOW = highlight, the answer, the cohort being predicted
  GREEN  = growth (the Hydra body); RED = crossed-out / accident
  TEXT   = reference lines (Type I, Type III), labels

One world: a survival axis (age 0..3 across, l_x up) at the same place in every plot scene.
Type II and the Hydra line are computed from a constant chance of death; Type I, Type III and the
"cohort" line are schematic and say so.
"""
import math
import random
from bp_style import *  # noqa: F401,F403

CARD = "#171a23"

# ---------- the survival axis (same place in every plot scene) ----------
X0, XA = -5.0, 3.2          # x of age 0, width per year
Y0, YH = -2.9, 5.8          # y of the floor, height of l_x = 1
FLOOR = 0.08
LO = math.log10(FLOOR)
LX = [1.0, 0.5, 0.25, 0.125]
LXT = ["1", "0.5", "0.25", "0.125"]


def ylin(l):
    return Y0 + YH * l


def ylog(l):
    return Y0 + YH * (math.log10(max(l, 1e-4)) - LO) / (-LO)


def ypos(l, u):
    return (1 - u) * ylin(l) + u * ylog(l)


def pt(a, l, u=1.0):
    return np.array([X0 + XA * a, ypos(l, u), 0.0])


def f2(a):
    return 0.5 ** a


def f1(a):   # Type I (schematic)
    return math.exp(-(a / 2.55) ** 6 - 0.05 * a)


def f3(a):   # Type III (schematic)
    return 0.1 + 0.9 * math.exp(-3.2 * a)


def fc(a):   # a cohort (schematic): nearly level, then plunging at old ages
    return math.exp(-(a / 2.5) ** 6.5 - 0.04 * a)


def fh(a):   # Hydra: constant chance of death 0.006 per year
    return (1 - 0.006) ** a


def tmax(f):
    for t in np.linspace(0, 3, 301):
        if f(t) < 0.088:
            return float(t)
    return 3.0


def crv(f, color, w=6, u=1.0, op=1.0, dash=False):
    m = ParametricFunction(lambda t: pt(t, f(t), u), t_range=[0, tmax(f), 0.02], color=color, stroke_width=w, fill_opacity=0)
    m.set_stroke(opacity=op)
    if dash:
        m = DashedVMobject(m, num_dashes=46)
        m.set_stroke(color, w, opacity=op)
    return m


def area_of(f, color, op=0.22, u=1.0):
    ts = np.linspace(0, tmax(f), 90)
    pts = [pt(t, f(t), u) for t in ts]
    pts += [np.array([pts[-1][0], Y0, 0.0]), np.array([X0, Y0, 0.0])]
    m = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=op)
    m.set_z_index(-2)
    return m


GRID = [(1.0, "1"), (0.5, "0.5"), (0.25, "0.25"), (0.125, "0.125"), (0.1, "0.1")]


def xaxis():
    g = VGroup(Line([X0, Y0, 0], [X0 + 3 * XA + 0.45, Y0, 0], color=GREY, stroke_width=4),
               Line([X0, Y0, 0], [X0, Y0 + YH + 0.2, 0], color=GREY, stroke_width=4))
    for a in range(4):
        g.add(Line([X0 + XA * a, Y0, 0], [X0 + XA * a, Y0 - 0.1, 0], color=GREY, stroke_width=3))
        g.add(T(f"age {a}", 28, TEXT).move_to([X0 + XA * a, Y0 - 0.42, 0]))
    return g


def ytitle(txt, color=TEXT, size=30):
    t = T(txt, size, color)
    return t.move_to([-6.7 + t.width / 2, 3.42, 0])


def log_grid(op=1.0):
    g = VGroup()
    for v, txt in GRID:
        y = ylog(v)
        fa = 0.35 if v == 0.1 else 1.0
        g.add(Line([X0, y, 0], [X0 + 3 * XA + 0.45, y, 0], color=GREY, stroke_width=2, stroke_opacity=0.5 * fa * op))
        g.add(M(txt, 26, TEXT).set_opacity(fa * op).next_to([X0 - 0.3, y, 0], LEFT, buff=0.0))
    return g


def card(text, size=30, color=TEXT, x=0.0, y=0.0, fill=0.9, pad=0.16):
    t = T(text, size, color)
    r = RoundedRectangle(corner_radius=0.12, width=t.width + 2 * pad, height=t.height + 2 * pad,
                         stroke_width=0, fill_color=BG, fill_opacity=fill)
    g = VGroup(r, t)
    return g.move_to([x, y, 0])


def samples(f, n=140):
    return [pt(a, f(a))[:2] for a in np.linspace(0, tmax(f), n)]


YT_BOX = (-5.0, 3.42, 3.9, 0.6)
DATA_BOXES = [(X0 + XA * a + (0.5 if a == 0 else 0.7), ylog(f2(a)) + (-0.05 if a == 0 else 0.34), 1.5, 0.5) for a in range(4)]


def place(c, pref, curves=(), boxes=(), extra_pts=(), pad=0.14, ymin=Y0 + 0.1):
    """Move card c to the free spot nearest `pref` that touches no curve, data point or earlier box."""
    w, h = c.width, c.height
    pts = [p for f in curves for p in samples(f)] + [tuple(e) for e in extra_pts]
    best = None
    for pd in (pad, 0.06, 0.0):
        bd = 1e9
        for x in np.arange(-6.6 + w / 2, 6.7 - w / 2 + 1e-6, 0.1):
            for y in np.arange(ymin + h / 2, 3.75 - h / 2 + 1e-6, 0.1):
                if x - w / 2 < X0 - 0.05 and y < 3.15:
                    continue
                if any(abs(px - x) < w / 2 + pd and abs(py - y) < h / 2 + pd for px, py in pts):
                    continue
                if any(abs(bx - x) < (bw + w) / 2 + pd and abs(by - y) < (bh + h) / 2 + pd for bx, by, bw, bh in boxes):
                    continue
                d = (x - pref[0]) ** 2 + (y - pref[1]) ** 2
                if d < bd:
                    best, bd = (x, y), d
        if best:
            break
    if best is None:
        print("PLACE FAILED", w, h, pref, flush=True)
        best = pref
    c.move_to([best[0], best[1], 0])
    return (best[0], best[1], w, h)


def motes(scene, seed=3):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(14):
        d = Dot(radius=rng.uniform(0.03, 0.06), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.12, 0.28))
        d.move_to([rng.uniform(-6.6, 6.6), rng.uniform(-3.6, 3.6), 0])
        d.v = (rng.uniform(-0.1, 0.1), rng.uniform(0.08, 0.22))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 3.9:
                m.shift(DOWN * 7.8)
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-10)
    scene.add(g)


# ---------- the cohort of dots (scenes 1-3) ----------
NCOL, NROW = 20, 8
SPD = 0.39
DY0 = 0.28
_rng = random.Random(11)
ORDER = list(range(160))
_rng.shuffle(ORDER)
DEATHS = [ORDER[0:80], ORDER[80:120], ORDER[120:140]]


def dpos(i):
    return np.array([(i % NCOL - (NCOL - 1) / 2) * SPD, DY0 + (i // NCOL) * SPD, 0])


def cohort(dead=()):
    ds = VGroup(*[Dot(dpos(i), radius=0.15, color=TEAL) for i in range(160)])
    for i in dead:
        ds[i].set_color(GREY).set_opacity(0.18)
    return ds


BAR_X = [-3.5, 0.0, 3.5]
BAR_S = 1.8 / 500
BAR_BASE = -2.95


def bar(k, n):
    h = n * BAR_S
    return Rectangle(width=2.0, height=h, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                     fill_opacity=0.75).move_to([BAR_X[k], BAR_BASE + h / 2, 0])


def bar_lab(k, n, txt=None):
    return M(txt or str(n), 28, TEXT).move_to([BAR_X[k], BAR_BASE + n * BAR_S + 0.32, 0])


def bar_axis():
    g = VGroup(Line([-6.0, BAR_BASE, 0], [6.0, BAR_BASE, 0], color=GREY, stroke_width=3))
    for k in range(3):
        g.add(T(f"year {k + 1}", 26, TEXT).move_to([BAR_X[k], BAR_BASE - 0.35, 0]))
    return g


def left_lab(txt, color=TEAL, size=34):
    t = T(txt, size, color)
    return t.move_to([-6.7 + t.width / 2, 3.42, 0])


def chance_lab():
    t = T("chance of death each year = 0.5", 30, YELLOW)
    return t.move_to([6.7 - t.width / 2, 3.42, 0])


# ---------- Hydra cartoon ----------
def hydra(h=2.0, tm=None, bud=True, color=GREEN, at=(0.0, 0.0)):
    """Bottom centre of the foot at `at`."""
    at = np.array([at[0], at[1], 0.0])
    foot = Ellipse(width=0.42 * h, height=0.09 * h, color=color, fill_opacity=0.9, stroke_width=2).move_to([0, 0.045 * h, 0])
    body = RoundedRectangle(corner_radius=0.1 * h, width=0.2 * h, height=0.62 * h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.55).move_to([0, 0.09 * h + 0.31 * h, 0])
    foot.shift(at)
    body.shift(at)
    top = at + np.array([0, 0.7 * h, 0])
    tents = VGroup()
    for k in range(5):
        dx = (k - 2) * 0.13 * h

        def make(k=k, dx=dx):
            sw = 0.05 * h * math.sin(tm.get_value() * 1.6 + k) if tm is not None else 0.0
            p0 = top + np.array([(k - 2) * 0.03 * h, 0, 0])
            p3 = top + np.array([dx * 1.4 + sw, 0.32 * h, 0])
            p1 = p0 + np.array([dx * 0.2, 0.18 * h, 0])
            p2 = p3 + np.array([-dx * 0.5 + sw, -0.14 * h, 0])
            return CubicBezier(p0, p1, p2, p3, color=color, stroke_width=max(2.5, 2.2 * h))
        tents.add(always_redraw(make) if tm is not None else make())
    g = VGroup(foot, body, tents)
    if bud:
        stub = Line(at + [0.09 * h, 0.4 * h, 0], at + [0.19 * h, 0.46 * h, 0], color=color, stroke_width=max(2.5, 2 * h))
        b = Dot(at + [0.2 * h, 0.47 * h, 0], radius=0.075 * h, color=GOLD)
        g.add(stub, b)
    return g


def timer(scene):
    tm = ValueTracker(0)
    tm.add_updater(lambda m, dt: m.increment_value(dt))
    scene.add(tm)
    return tm


# ---------- dynamic survival world (scenes 4-6) ----------
def world(scene, ug=0.0, up=0.0, op=1.0):
    ugt, upt, opt = ValueTracker(ug), ValueTracker(up), ValueTracker(op)
    scene.add(xaxis())
    items = [(1.0, "1"), (0.5, "0.5"), (0.25, "0.25"), (0.125, "0.125"), (0.1, "0.1"), (0.0, "0")]
    for v, txt in items:
        def gl(v=v):
            u = ugt.get_value()
            if v == 0.0:
                return VGroup()
            fa = u * 0.35 if v == 0.1 else 1.0
            return Line([X0, ypos(v, u), 0], [X0 + 3 * XA + 0.45, ypos(v, u), 0], color=GREY, stroke_width=2, stroke_opacity=0.5 * fa)

        def gt(v=v, txt=txt):
            u = ugt.get_value()
            fa = u if v == 0.1 else ((1 - u) if v == 0.0 else 1.0)
            return M(txt, 26, TEXT).set_opacity(fa).next_to([X0 - 0.3, ypos(v, u), 0], LEFT, buff=0.0)
        scene.add(always_redraw(gl), always_redraw(gt))
    curve = always_redraw(lambda: ParametricFunction(lambda t: pt(t, f2(t), upt.get_value()), t_range=[0, 3, 0.02],
                                                     color=TEAL, stroke_width=8, fill_opacity=0).set_stroke(opacity=opt.get_value()))
    dots_ = [always_redraw(lambda a=a: Dot(pt(a, f2(a), upt.get_value()), radius=0.16, color=TEAL).set_opacity(opt.get_value())) for a in range(4)]
    labs = [always_redraw(lambda a=a: M(LXT[a], 28, TEXT).set_opacity(opt.get_value()).move_to(pt(a, f2(a), upt.get_value()) + (np.array([0.5, -0.05, 0]) if a == 0 else np.array([0.7, 0.34, 0]))))
            for a in range(4)]
    grp = VGroup(curve, *dots_, *labs)
    scene.add(grp)
    area = always_redraw(lambda: Polygon(*([pt(t, f2(t), upt.get_value()) for t in np.linspace(0, 3, 60)] + [np.array([X0 + 3 * XA, Y0, 0.0]), np.array([X0, Y0, 0.0])]),
                                         stroke_width=0, fill_color=TEAL, fill_opacity=0.22 * opt.get_value()).set_z_index(-2))
    return ugt, upt, curve, VGroup(*dots_), VGroup(*labs), opt, area


def start_s07(scene, label=True):
    scene.add(xaxis(), log_grid(), ytitle("l_x, log axis"))
    ln = crv(f2, TEAL)
    pts = VGroup(*[Dot(pt(a, f2(a)), radius=0.16, color=TEAL) for a in range(4)])
    scene.add(area_of(f2, TEAL), ln, pts)
    return ln, pts


# =============================== scenes ===============================
class S00Title(TitleCard):
    LESSON = "Demography and Survivorship"
    TITLE = "A Straight Line on a Log Axis"


class S01Question(SpokenScene):
    def construct(self):
        motes(self)
        # a small inset of chapter 1's stacked R0 bar
        segs = VGroup(*[Rectangle(width=0.7, height=h, stroke_color=GOLD, stroke_width=3, fill_color=TEAL, fill_opacity=0.75)
                        for h in (0.8, 0.8, 0.1)]).arrange(UP, buff=0)
        r0 = M("R0", 30, YELLOW)
        inset = VGroup(segs, r0).arrange(DOWN, buff=0.15).move_to([0, 0.5, 0]).scale(1.6)
        self.play(FadeIn(inset, scale=0.8), run_time=1.0)
        self.at("now watch survival")
        ds = cohort()
        lab = left_lab("1,000 newborns")
        self.play(inset.animate.scale(0.15).move_to([-6.3, 3.4, 0]).set_opacity(0),
                  LaggedStart(*[FadeIn(d, scale=0.4) for d in ds], lag_ratio=0.011), FadeIn(lab, shift=UP * 0.1), run_time=1.8)
        self.remove(inset)
        self.at("half of this cohort")
        ch = chance_lab()
        self.play(Write(ch), run_time=1.4)
        self.play(Indicate(ch, color=YELLOW, scale_factor=1.08), run_time=0.9)
        self.at("do the same number")
        q = T("Do the same number die each year?", 44, TEXT).move_to([0, -1.3, 0])
        self.play(Write(q), run_time=1.8)
        qm = T("?", 130, YELLOW, weight=BOLD).move_to([0, -2.9 + 0.3, 0])
        self.play(FadeIn(qm, scale=0.5), run_time=0.7)
        self.play(Indicate(qm, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.finish()


class S02Year1(SpokenScene):
    def construct(self):
        motes(self)
        ds = cohort()
        lab = left_lab("1,000 newborns")
        ch = chance_lab()
        self.add(ds, lab, ch)
        self.wait(0.8)
        self.at("half of the cohort")
        anims = [ds[i].animate.set_color(GREY).set_opacity(0.18) for i in DEATHS[0]]
        new = left_lab("alive: 500")
        self.play(LaggedStart(*anims, lag_ratio=0.015), run_time=2.2)
        self.play(ReplacementTransform(lab, new), run_time=0.8)
        self.at("the gray bar")
        ax = bar_axis()
        self.play(Create(ax), run_time=1.0)
        b = bar(0, 500)
        self.play(GrowFromEdge(b, DOWN), run_time=1.6)
        bl = bar_lab(0, 500, "500 deaths")
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(bl, color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.finish()


class S03Shrink(SpokenScene):
    def construct(self):
        motes(self)
        ds = cohort(dead=DEATHS[0])
        lab = left_lab("alive: 500")
        ch = chance_lab()
        ax = bar_axis()
        b1, b1l = bar(0, 500), bar_lab(0, 500, "500 deaths")
        self.add(ds, lab, ch, ax, b1, b1l)
        self.wait(0.3)
        # year 2
        new = left_lab("alive: 250")
        self.play(LaggedStart(*[ds[i].animate.set_color(GREY).set_opacity(0.18) for i in DEATHS[1]], lag_ratio=0.02), ReplacementTransform(lab, new), run_time=2.0)
        lab = new
        b2 = bar(1, 250)
        self.play(GrowFromEdge(b2, DOWN), run_time=1.0)
        b2l = bar_lab(1, 250)
        self.play(FadeIn(b2l, shift=UP * 0.1), run_time=0.5)
        self.at("year after year")
        new = left_lab("alive: 125")
        self.play(LaggedStart(*[ds[i].animate.set_color(GREY).set_opacity(0.18) for i in DEATHS[2]], lag_ratio=0.03), ReplacementTransform(lab, new), run_time=1.6)
        b3 = bar(2, 125)
        self.play(GrowFromEdge(b3, DOWN), run_time=0.9)
        b3l = bar_lab(2, 125)
        self.play(FadeIn(b3l, shift=UP * 0.1), run_time=0.5)
        self.at("a constant chance")
        h1 = M("x 1/2", 28, YELLOW).move_to([-1.75, -1.65, 0])
        h2 = M("x 1/2", 28, YELLOW).move_to([1.75, -2.2, 0])
        self.play(FadeIn(h1, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(h2, shift=RIGHT * 0.2), run_time=0.6)
        self.at("same fraction")
        fin = T("same fraction, shrinking numbers", 34, YELLOW).move_to([0, -0.2, 0])
        self.play(Write(fin), run_time=1.6)
        self.play(Indicate(h1, color=YELLOW), Indicate(h2, color=YELLOW), run_time=1.0)
        self.finish()


class S04Linear(SpokenScene):
    def construct(self):
        motes(self)
        ugt, upt, curve, dts, labs, opt, area = world(self, 0.0, 0.0)
        objs = list(self.mobjects)[1:]
        self.remove(*objs)
        axes, grid, grp = objs[0], objs[1:13], objs[13]
        yt = ytitle("l_x")
        self.play(Create(axes), run_time=2.0)
        self.add(*grid)
        self.play(FadeIn(yt), run_time=0.8)
        self.at("on an ordinary axis")
        oa = T("ordinary axis", 32, YELLOW).move_to([-6.7 + 1.2, 3.42, 0])
        self.play(ReplacementTransform(yt, oa), run_time=0.9)
        self.remove(grp)
        area.set_opacity(0)
        self.at("the points fall")
        for a in range(4):
            self.play(FadeIn(dts[a], scale=0.4), FadeIn(labs[a], shift=UP * 0.1), run_time=0.35)
            self.wait(0.08)
        self.at("then the curve bends")
        self.play(Create(curve), run_time=2.4)
        self.add(area)
        self.play(Indicate(curve, color=YELLOW, scale_factor=1.0), run_time=1.2)
        self.finish()


class S05Log(SpokenScene):
    def construct(self):
        motes(self)
        ugt, upt, curve, dts, labs, opt, area = world(self, 0.0, 0.0)
        self.add(area)
        oa = T("ordinary axis", 32, YELLOW).move_to([-6.7 + 1.2, 3.42, 0])
        self.add(oa)
        self.play(opt.animate.set_value(0.25), run_time=0.8)
        self.play(Indicate(oa, color=TEXT, scale_factor=1.1), run_time=1.0)
        self.at("on a log axis")
        new = ytitle("l_x, log axis", YELLOW)
        self.play(ugt.animate.set_value(1.0), ReplacementTransform(oa, new), run_time=3.2)
        self.at("every halving")
        marks = VGroup()
        for i in range(3):
            y = (ylog(LX[i]) + ylog(LX[i + 1])) / 2
            marks.add(M("x 1/2", 30, YELLOW).move_to([X0 + 0.7, y, 0]))
        for m in marks:
            self.play(FadeIn(m, shift=DOWN * 0.15), run_time=0.5)
            self.wait(0.25)
        self.at("equal drops")
        sx = X0 + 2.7
        arrows = VGroup(*[Arrow([sx, ylog(LX[i]), 0], [sx, ylog(LX[i + 1]), 0], buff=0, color=YELLOW, stroke_width=6,
                                max_tip_length_to_length_ratio=0.25) for i in range(3)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=1.5)
        t = card("equal drops = equal fractions", 34, YELLOW, x=2.4, y=1.9)
        self.play(FadeIn(t, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S06Straight(SpokenScene):
    def construct(self):
        motes(self)
        ugt, upt, curve, dts, labs, opt, area = world(self, 1.0, 0.0, 0.25)
        self.add(area)
        yt = ytitle("l_x, log axis", YELLOW)
        self.add(yt)
        self.play(opt.animate.set_value(1.0), run_time=0.8)
        self.wait(0.6)
        self.at("they slide into")
        self.play(upt.animate.set_value(1.0), run_time=3.0)
        self.at("a constant chance")
        tag = card("Type II: constant chance of death", 32, TEAL)
        place(tag, (1.9, 2.6), [f2], [YT_BOX] + DATA_BOXES)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.9)
        dot = Dot(pt(0, 1.0), radius=0.14, color=YELLOW)
        path = crv(f2, TEAL)
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=3.2, rate_func=linear)
        self.remove(dot)
        self.at("type II")
        self.play(Indicate(tag, color=YELLOW, scale_factor=1.06), run_time=1.2)
        self.finish()


def t2card():
    c = card("Type II", 30, TEAL)
    place(c, (0.0, 1.75), [f2, f1, f3], [YT_BOX])
    return c


class S07Types(SpokenScene):
    def construct(self):
        motes(self)
        ln, pts = start_s07(self)
        tag = t2card()
        self.add(tag)
        self.at("two other shapes")
        self.wait(0.5)
        self.at("type 1 stays")
        t1 = crv(f1, TEXT, w=5)
        self.play(Create(t1), run_time=2.2)
        boxes = [YT_BOX, (tag.get_x(), tag.get_y(), tag.width, tag.height)]
        l1 = card("Type I (schematic)", 28, TEXT)
        boxes.append(place(l1, (-2.4, 3.4), [f1, f2, f3], boxes))
        self.play(FadeIn(l1), run_time=0.5)
        self.at("because most deaths come late")
        d1 = card("deaths late", 28, YELLOW)
        boxes.append(place(d1, (5.65, 0.35), [f1, f2, f3], boxes))
        self.play(FadeIn(d1, shift=LEFT * 0.2), run_time=0.7)
        self.at("type 3 drops")
        t3 = crv(f3, TEXT, w=5, dash=True)
        self.play(Create(t3), run_time=1.8)
        l3 = card("Type III (schematic)", 28, TEXT)
        boxes.append(place(l3, (0.4, -1.35), [f1, f2, f3], boxes))
        self.play(FadeIn(l3), run_time=0.5)
        self.at("because most deaths come early")
        d3 = card("deaths early", 28, YELLOW)
        boxes.append(place(d3, (-2.5, 0.3), [f1, f2, f3], boxes))
        self.play(FadeIn(d3, shift=UP * 0.2), run_time=0.7)
        self.finish()


def s08_state(scene, ghost=0.28):
    scene.add(xaxis(), log_grid(), ytitle("l_x, log axis"))
    g = VGroup(crv(f2, TEAL, op=ghost), crv(f1, TEXT, w=5, op=ghost), crv(f3, TEXT, w=5, op=ghost, dash=True))
    scene.add(g)
    return g


def cohort_label():
    c = card("a cohort (schematic)", 30, YELLOW)
    place(c, (-3.3, 2.35), [f2, f1, f3, fc], [YT_BOX, (1.4, 3.42, 7.4, 0.9)])
    return c


BTN = [("constant", -1.1), ("rising", 1.45), ("falling", 3.95)]


def buttons(lit=None):
    g = VGroup()
    for name, x in BTN:
        c = YELLOW if name == lit else TEXT
        ch = chip(name, c, 30)
        ch[0].set_fill(c, 0.95 if name == lit else 0.12)
        if name == lit:
            ch[1].set_color(BG)
        ch.move_to([x, 3.42, 0])
        g.add(ch)
    return g


class S08Predict(SpokenScene):
    def construct(self):
        motes(self)
        ln, pts = start_s07(self)
        tag = t2card()
        t1 = crv(f1, TEXT, w=5)
        t3 = crv(f3, TEXT, w=5, dash=True)
        self.add(tag, t1, t3)
        self.wait(0.3)
        self.at("here is another")
        self.play(*[m.animate.set_stroke(opacity=0.28) for m in (ln, t1, t3)], pts.animate.set_opacity(0.28), tag.animate.set_opacity(0.28), run_time=1.4)
        self.at("its line stays")
        c = crv(fc, YELLOW, w=7)
        cl = cohort_label()
        self.play(Create(c), run_time=3.6)
        self.play(FadeIn(cl), FadeIn(area_of(fc, YELLOW, 0.2)), run_time=0.6)
        self.at("is the chance of dying")
        b = buttons()
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in b], lag_ratio=0.5), run_time=2.4)
        self.play(Indicate(b[0]), run_time=0.7)
        self.play(Indicate(b[1]), run_time=0.7)
        self.play(Indicate(b[2]), run_time=0.7)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        motes(self)
        self.add(xaxis(), log_grid())
        g = VGroup(crv(f2, TEAL, op=0.28), crv(f1, TEXT, w=5, op=0.28), crv(f3, TEXT, w=5, op=0.28, dash=True))
        c = crv(fc, YELLOW, w=7)
        cl = cohort_label()
        b = buttons()
        pr = T("Predict", 36, YELLOW).move_to([-5.4, 3.42, 0])
        self.add(area_of(fc, YELLOW, 0.2), g, c, cl, b, pr)
        for i in range(3):
            self.play(Indicate(b[i], scale_factor=1.12), run_time=1.3)
        self.play(Indicate(pr, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        motes(self)
        self.add(xaxis(), log_grid())
        g2 = VGroup(crv(f2, TEAL, op=0.28), crv(f3, TEXT, w=5, op=0.28, dash=True))
        t1 = crv(f1, TEXT, w=5, op=0.28)
        c = crv(fc, YELLOW, w=7)
        cl = cohort_label()
        b = buttons()
        pr = T("Predict", 36, YELLOW).move_to([-5.4, 3.42, 0])
        self.add(area_of(fc, YELLOW, 0.2), g2, t1, c, cl, b, pr)
        self.wait(0.3)
        nb = buttons("rising")
        self.play(ReplacementTransform(b, nb), run_time=0.8)
        self.play(Flash(nb[1], color=YELLOW, line_length=0.25, flash_radius=0.7), run_time=1.0)
        self.at("few die young")
        allc = [f2, f1, f3, fc]
        bx = [YT_BOX, (cl.get_x(), cl.get_y(), cl.width, cl.height)]

        def hop(a0, a1, rt):
            return MoveAlongPath(dot, ParametricFunction(lambda t: pt(t, fc(t)), t_range=[a0, a1, 0.01]), run_time=rt, rate_func=linear)
        dot = Dot(pt(0.25, fc(0.25)), radius=0.2, color=WHITE)
        a = card("few die", 30, YELLOW)
        bx.append(place(a, (-1.5, 1.55), allc, bx))
        self.play(FadeIn(dot, scale=2), FadeIn(a, shift=UP * 0.1), run_time=0.7)
        self.at("the chance of dying climbs")
        b2 = card("more die", 30, YELLOW)
        bx.append(place(b2, (1.2, 0.35), allc, bx))
        b3 = card("most die", 30, YELLOW)
        bx.append(place(b3, (3.2, -1.05), allc, bx))
        self.play(hop(0.25, 1.9, 1.7))
        self.play(FadeIn(b2, shift=UP * 0.1), hop(1.9, 2.3, 0.7))
        self.at("so the line bends")
        self.play(FadeIn(b3, shift=UP * 0.1), hop(2.3, 2.85, 1.3))
        self.remove(dot)
        self.at("close to type 1")
        self.play(t1.animate.set_stroke(opacity=1.0, width=7), run_time=1.0)
        lt = card("close to Type I", 30, TEXT)
        place(lt, (-3.0, 1.0), allc, bx)
        self.play(FadeIn(lt, shift=UP * 0.1), Indicate(t1, color=YELLOW, scale_factor=1.0), run_time=1.2)
        self.finish()


def cartoon_card(x=-1.6, y=0.9):
    t = T("Mortality always\nrises with age?", 40, YELLOW, weight=BOLD, line_spacing=0.9)
    r = RoundedRectangle(corner_radius=0.18, width=t.width + 0.7, height=t.height + 0.55, stroke_color=YELLOW, stroke_width=5,
                         fill_color=CARD, fill_opacity=0.96)
    g = VGroup(r, t).move_to([x, y, 0]).rotate(0.06)
    return g


class S11HydraQuestion(SpokenScene):
    def construct(self):
        motes(self)
        self.add(xaxis(), log_grid(0.5))
        g = VGroup(crv(f2, TEAL, op=0.25), crv(f1, TEXT, w=5, op=0.25), crv(f3, TEXT, w=5, op=0.25, dash=True))
        self.add(g)
        tm = timer(self)
        self.wait(0.2)
        self.at("does every")
        cd = cartoon_card()
        self.play(FadeIn(cd, scale=1.3), run_time=0.9)
        hy = hydra(3.7, tm, at=(4.7, -2.7))
        self.at("a classic reading")
        self.play(FadeIn(hy, shift=UP * 0.3), run_time=1.2)
        self.at("for every multicellular")
        cap = card("breeds repeatedly", 34, TEXT, x=-1.6, y=-1.0)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.9)
        self.play(Indicate(cd, color=YELLOW, scale_factor=1.04), run_time=1.2)
        self.finish()


DISH_X = [-4.5, -1.5, 1.5, 4.5]
DISH_Y = [1.65, 0.1, -1.45]


def dish(x, y, bud=False):
    c = Circle(radius=0.68, stroke_color=GREY, stroke_width=3, fill_color=CARD, fill_opacity=1.0).move_to([x, y, 0])
    h = hydra(0.95, None, bud=bud)
    h.shift(np.array([x, y - 0.34, 0]) - h[0].get_bottom())
    c.set_z_index(1)
    h.set_z_index(2)
    return VGroup(c, h)


class S12HydraMethod(SpokenScene):
    def construct(self):
        motes(self)
        dishes = VGroup(*[dish(x, y) for y in DISH_Y for x in DISH_X])
        n1 = T("2,256 Hydra", 36, TEXT).move_to([-6.7 + 1.5, 3.42, 0])
        n2 = T("12 cohorts", 36, TEXT).move_to([-0.4, 3.42, 0])
        self.at("researchers kept")
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dishes], lag_ratio=0.08), run_time=2.2)
        self.at("small freshwater")
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.7)
        self.at("12 cohorts")
        self.play(FadeIn(n2, shift=UP * 0.1), LaggedStart(*[ShowPassingFlash(d[0].copy().set_fill(opacity=0).set_stroke(YELLOW, 7), time_width=1.0) for d in dishes], lag_ratio=0.1), run_time=2.0)
        self.at("they checked every")
        day = ValueTracker(1)
        cal = always_redraw(lambda: VGroup(
            RoundedRectangle(corner_radius=0.12, width=2.35, height=0.75, stroke_color=TEXT, stroke_width=3, fill_color=CARD, fill_opacity=1),
            M(f"day {int(day.get_value())}", 32, TEXT)).move_to([5.45, 3.42, 0]))
        self.add(cal)
        ck = T("checked daily: deaths and buds", 34, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(ck, shift=UP * 0.1), run_time=0.8)
        sweep = Line([-6.2, 2.5, 0], [6.2, 2.5, 0], color=YELLOW, stroke_width=5).set_opacity(0.7)
        self.add(sweep)
        self.play(day.animate.set_value(10), sweep.animate.shift(DOWN * 4.6), run_time=1.6, rate_func=linear)
        sweep.move_to([0, 2.5, 0])
        self.at("deaths")
        self.play(*[dishes[i][1].animate.set_color(GREY) for i in (1, 6, 10)], day.animate.set_value(14), sweep.animate.shift(DOWN * 4.6), run_time=1.0, rate_func=linear)
        sweep.move_to([0, 2.5, 0])
        self.at("new buds")
        buds = VGroup(*[Dot([dishes[i][0].get_center()[0] + 0.22, dishes[i][0].get_center()[1] - 0.12, 0], radius=0.075, color=GOLD).set_z_index(3) for i in (0, 2, 4, 5, 7, 9, 11)])
        self.play(day.animate.set_value(30), sweep.animate.shift(DOWN * 4.6), LaggedStart(*[FadeIn(b, scale=2.5) for b in buds], lag_ratio=0.25), run_time=2.0, rate_func=linear)
        self.finish()


class S13Censor(SpokenScene):
    def construct(self):
        motes(self)
        dsh = dish(-5.3, 2.45).scale(1.5, about_point=[-5.3, 2.45, 0])
        self.at("deaths from culture")
        self.play(FadeIn(dsh, scale=0.7), run_time=0.9)
        self.at("accidents")
        self.play(dsh.animate.rotate(-1.1, about_point=dsh[0].get_center() + np.array([0.7, -0.7, 0])).shift(DOWN * 0.1), run_time=1.0)
        tri = Triangle(color=RED, fill_color=RED, fill_opacity=0.9).scale(0.5).move_to([-3.1, 2.45, 0]).set_z_index(5)
        ex = T("!", 34, BG, weight=BOLD).move_to(tri).shift(DOWN * 0.04).set_z_index(6)
        acc = T("accident", 38, RED).move_to([-1.3, 2.45, 0])
        self.play(FadeIn(VGroup(tri, ex), scale=0.5), FadeIn(acc), run_time=0.8)
        self.at("natural deaths")
        nd = T("not a natural death", 32, TEXT).move_to([2.6, 2.45, 0])
        self.play(FadeIn(nd, shift=RIGHT * 0.2), run_time=0.8)
        self.at("those animals counted")
        rows = [1.0, 0.0, -1.0, -2.0]
        xs = -4.6
        r1 = Line([xs, rows[0], 0], [0.6, rows[0], 0], color=TEAL, stroke_width=7)
        d1 = Dot([0.6, rows[0], 0], radius=0.18, color=GREY)
        r2 = Line([xs, rows[1], 0], [5.4, rows[1], 0], color=TEAL, stroke_width=7)
        a2 = Arrow([5.2, rows[1], 0], [6.1, rows[1], 0], buff=0, color=TEAL, stroke_width=7)
        r3 = Line([xs, rows[2], 0], [2.6, rows[2], 0], color=TEAL, stroke_width=7)
        d3 = Dot([2.6, rows[2], 0], radius=0.18, color=GREY)
        r4 = Line([xs, rows[3], 0], [-0.9, rows[3], 0], color=TEAL, stroke_width=7)
        self.play(LaggedStart(Create(r1), Create(r2), Create(r3), Create(r4), lag_ratio=0.25), run_time=1.7)
        self.play(FadeIn(d1, scale=2), FadeIn(d3, scale=2), FadeIn(a2), run_time=0.6)
        nl = T("natural death", 28, TEXT).move_to([2.55, rows[0] + 0.0, 0])
        risk = T("at risk while watched", 28, TEXT).move_to([-2.75, rows[3] - 0.4, 0])
        self.play(FadeIn(nl, shift=RIGHT * 0.1), FadeIn(risk, shift=UP * 0.1), run_time=0.8)
        self.at("then left the table")
        dsh_line = DashedLine([-0.9, rows[3], 0], [3.4, rows[3], 0], color=TEAL, stroke_width=6, dash_length=0.2)
        br = VGroup(Line([3.45, rows[3] + 0.3, 0], [3.45, rows[3] - 0.3, 0]), Line([3.45, rows[3] + 0.3, 0], [3.2, rows[3] + 0.3, 0]),
                    Line([3.45, rows[3] - 0.3, 0], [3.2, rows[3] - 0.3, 0])).set_stroke(YELLOW, 6)
        self.play(Create(dsh_line), run_time=1.4)
        self.play(Create(br), run_time=0.6)
        self.at("that is called censoring")
        cen = T("censored: not a natural death", 32, YELLOW).move_to([0.2, rows[3] - 1.0 + 0.0, 0])
        self.play(Write(cen), run_time=1.4)
        self.play(Indicate(br, color=YELLOW), run_time=1.0)
        self.finish()


class S14HydraResult(SpokenScene):
    def construct(self):
        motes(self)
        self.add(xaxis(), log_grid())
        gh = crv(f2, TEAL, op=0.2)
        self.add(gh)
        self.at("ten of the")
        t1 = T("10 of 12 cohorts", 36, TEXT).move_to([-6.7 + 2.2, 3.42, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.8)
        self.at("the yearly chance")
        t2 = T("about 0.006 per year", 36, YELLOW).move_to([2.6, 3.42, 0])
        self.play(Write(t2), run_time=1.6)
        self.at("on the log axis")
        hl = crv(fh, TEAL, w=9)
        self.play(Create(hl), run_time=2.2)
        self.play(FadeIn(area_of(fh, TEAL, 0.2)), run_time=0.6)
        tag = card("Hydra (computed)", 30, TEAL)
        place(tag, (-1.6, 2.3), [f2, fh], [(-2.5, 3.42, 7.0, 0.7)])
        self.play(FadeIn(tag), run_time=0.5)
        self.at("did not systematically")
        xs = [X0 + XA * a for a in (0.35, 1.0, 1.65, 2.3)]
        hs = VGroup()
        for x in xs:
            h = hydra(1.2, None, bud=True)
            h.shift(np.array([x, -2.8, 0]) - h[0].get_bottom())
            hs.add(h)
        hb = [(h.get_x(), h.get_y(), h.width + 0.2, h.height) for h in hs]
        fl = card("fertility: no systematic fall", 34, GOLD)
        place(fl, (-1.4, -1.0), [f2, fh], hb)
        self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in hs], lag_ratio=0.3), FadeIn(fl), run_time=2.0)
        self.play(Indicate(hs, color=GOLD, scale_factor=1.05), run_time=1.2)
        self.finish()


class S15Scope(SpokenScene):
    def construct(self):
        motes(self)
        self.add(xaxis(), log_grid())
        hl = crv(fh, TEAL, w=9)
        self.add(area_of(fh, TEAL, 0.2), hl)
        self.wait(0.4)
        self.at("laboratory cohorts")
        t1 = chip("laboratory cohorts", TEAL, 34)
        t1.move_to([-1.9, 1.7, 0])
        c1 = Line([-1.9, ypos(fh(1.0), 1) - 0.03, 0], [-1.9, t1.get_top()[1], 0], color=TEAL, stroke_width=5)
        self.play(Create(c1), FadeIn(t1, shift=UP * 0.3), run_time=0.9)
        self.at("counting rule")
        t2 = chip("accidents censored", YELLOW, 34)
        t2.move_to([3.2, 1.7, 0])
        c2 = Line([3.2, ypos(fh(1.0), 1) - 0.03, 0], [3.2, t2.get_top()[1], 0], color=YELLOW, stroke_width=5)
        self.play(Create(c2), FadeIn(t2, shift=UP * 0.3), run_time=0.9)
        self.at("it does not show")
        k1 = chip("immortal", TEXT, 44)
        k1.move_to([-1.9, -0.2, 0])
        self.play(FadeIn(k1, scale=0.8), run_time=0.8)
        x1 = VGroup(Line(k1.get_corner(UL), k1.get_corner(DR)), Line(k1.get_corner(DL), k1.get_corner(UR))).set_stroke(RED, 8)
        self.play(Create(x1), run_time=0.7)
        self.at("or that they live")
        k2 = chip("same in ponds", TEXT, 44)
        k2.move_to([2.8, -1.5, 0])
        self.play(FadeIn(k2, scale=0.8), run_time=0.8)
        x2 = VGroup(Line(k2.get_corner(UL), k2.get_corner(DR)), Line(k2.get_corner(DL), k2.get_corner(UR))).set_stroke(RED, 8)
        self.play(Create(x2), run_time=0.7)
        self.finish()


class S16Close(SpokenScene):
    def construct(self):
        motes(self)
        self.add(xaxis(), log_grid(), ytitle("l_x, log axis"))
        hl = crv(fh, TEAL, w=9)
        self.add(area_of(fh, TEAL, 0.2), hl)
        l2 = crv(f2, TEAL, w=6, op=0.9)
        l1 = crv(f1, TEXT, w=5, op=0.7)
        l3 = crv(f3, TEXT, w=5, op=0.7, dash=True)
        qtxt = T("Mortality always rises with age", 30, YELLOW)
        qm = T("?", 38, YELLOW, weight=BOLD)
        qrow = VGroup(qtxt, qm).arrange(RIGHT, buff=0.06)
        cd = VGroup(RoundedRectangle(corner_radius=0.12, width=qrow.width + 0.5, height=0.72, stroke_color=YELLOW, stroke_width=4,
                                     fill_color=CARD, fill_opacity=0.96), qrow)
        qrow.move_to(cd[0])
        cd.move_to([2.6, 3.42, 0])
        self.add(cd)
        self.wait(0.3)
        self.at("a straight line")
        self.play(Create(l1), Create(l3), Create(l2), run_time=2.0)
        self.at("constant chance of death")
        self.play(l2.animate.set_stroke(width=10), run_time=0.8)
        lab = card("same fraction each year", 32, TEAL)
        place(lab, (-1.0, -0.65), [f2, f1, f3, fh], [YT_BOX, (2.6, 3.42, cd[0].width, 0.8)])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.8)
        dot = Dot(pt(0, 1.0), radius=0.14, color=YELLOW)
        self.add(dot)
        self.play(MoveAlongPath(dot, crv(f2, TEAL)), run_time=2.2, rate_func=linear)
        self.remove(dot)
        self.at("not universal")
        strike = Cross(qm, stroke_color=RED, stroke_width=9).scale(1.15)
        self.play(Create(strike), run_time=0.8)
        self.play(Indicate(cd, color=RED, scale_factor=1.03), run_time=1.0)
        self.finish()


class S17End(EndCard):
    LINE = "Straight on a log axis means the same fraction dies each year."
