"""History of life: Births Minus Deaths (Biochemistrypedia explainer)

COLOR MAP, one colour per concept for the whole film
  GREEN = speciation (new branches, births)     RED  = extinction (endings, deaths)
  BLUE  = surviving lineages                     GREY = extinct lineages (with a cross)
  GOLD  = iridium band, brackets, surface mat    TEAL = fossil-floor flags
  YELLOW = labels to notice
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
LESSON_TITLE = "History of Life: Transitions, Extinctions and Radiations"


# ------------------------------------------------------------------ helpers
def Ln(a, b, col=TEXT, w=6):
    return Line([a[0], a[1], 0], [b[0], b[1], 0], color=col, stroke_width=w)


def live(f):
    return always_redraw(f)


def tick(sc):
    """A do-nothing time-based updater: makes every wait() run frame by frame, so always_redraw mobjects stay live."""
    d = Dot(radius=0.001, color=BG)
    d.add_updater(lambda m, dt: None)
    sc.add(d)


def until(sc, t):
    r = t - sc.elapsed()
    if r > 0.02:
        sc.wait(r)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sm(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def two(a, b, size=24, ca=TEXT, cb=YELLOW):
    return VGroup(T(a, size, ca), T(b, size, cb)).arrange(DOWN, buff=0.08)


# ------------------------------------------------------------------ the lineage tree (computed from a birth-death simulation)
def _sim(seed, lam=1.5, mu=0.6, TT=3.0, dt=0.01):
    rng = random.Random(seed)
    root = dict(t0=0.0, t1=None, kids=[], ext=False, par=None)
    nodes, alive, t = [root], [root], 0.0
    while t < TT:
        t += dt
        for n in list(alive):
            r = rng.random()
            if r < lam * dt:
                n["t1"] = t
                alive.remove(n)
                for _ in range(2):
                    k = dict(t0=t, t1=None, kids=[], ext=False, par=n)
                    n["kids"].append(k)
                    nodes.append(k)
                    alive.append(k)
            elif r < (lam + mu) * dt:
                n["t1"] = t
                n["ext"] = True
                alive.remove(n)
        if not alive:
            return None
    for n in alive:
        n["t1"] = TT
    for n in nodes:
        n["t0"] /= TT
        n["t1"] /= TT
    return nodes


def _layout(nodes):
    cnt = [0]

    def rec(n):
        if not n["kids"]:
            n["y"] = cnt[0]
            cnt[0] += 1
        else:
            for k in n["kids"]:
                rec(k)
            n["y"] = sum(k["y"] for k in n["kids"]) / len(n["kids"])
    rec(nodes[0])
    for n in nodes:
        n["y"] = n["y"] / max(1, cnt[0] - 1)
    return nodes


def count_at(nodes, cut):
    cut = min(cut, 0.9999)
    return sum(1 for n in nodes if n["t0"] <= cut < n["t1"])


def _find_tree():
    for seed in range(5000):
        nodes = _sim(seed)
        if not nodes:
            continue
        alive = sum(1 for n in nodes if not n["kids"] and not n["ext"])
        ext = sum(1 for n in nodes if n["ext"])
        if 10 <= alive <= 13 and ext >= 5 and len(nodes) <= 44 and nodes[0]["t1"] < 0.16 and count_at(nodes, 0.4) >= 4:
            return _layout(nodes)
    raise RuntimeError("no tree")


NODES = _find_tree()
XL, XR = -5.0, 5.6


def tree_mobs(nodes, cut, xl, xr, yl, yh, line=BLUE, conn=GREEN, w=6):
    g = VGroup()
    X = lambda t: xl + (xr - xl) * t
    Y = lambda v: yl + (yh - yl) * v
    g.add(Dot([X(0), Y(nodes[0]["y"]), 0], radius=0.07, color=line))
    for n in nodes:
        if cut <= n["t0"]:
            continue
        e = min(cut, n["t1"])
        dead = n["ext"] and cut >= n["t1"]
        g.add(Ln([X(n["t0"]), Y(n["y"])], [X(e), Y(n["y"])], GREY if dead else line, w))
        if n["par"] is not None:
            g.add(Ln([X(n["t0"]), Y(n["par"]["y"])], [X(n["t0"]), Y(n["y"])], conn, w))
        if dead:
            cx, cy = X(n["t1"]), Y(n["y"])
            g.add(Ln([cx - .13, cy - .13], [cx + .13, cy + .13], RED, 5))
            g.add(Ln([cx - .13, cy + .13], [cx + .13, cy - .13], RED, 5))
    return g


class TreeView:
    def __init__(self, sc, cutf, nodes=NODES, yl=-2.2, yh=2.1, xl=XL, xr=XR, **kw):
        self.xr, self.yl, self.yh = ValueTracker(xr), ValueTracker(yl), ValueTracker(yh)
        self.cutf, self.nodes, self.xl, self.kw = cutf, nodes, xl, kw
        self.mob = live(lambda: tree_mobs(self.nodes, self.cutf(), self.xl, self.xr.get_value(),
                                                   self.yl.get_value(), self.yh.get_value(), **self.kw))


# ------------------------------------------------------------------ diversity curve (schematic, computed from a simple model)
AGES = np.arange(540, -0.01, -1.0)


def _div():
    drops = {445: .45, 372: .8, 365: .75, 359: .85, 252: .2, 201: .55, 66: .4}
    v, out = .15, []
    for a in AGES:
        K = .5 + .5 * (540 - a) / 540
        v += 0.025 * v * (1 - v / K)
        for d, f in drops.items():
            if abs(a - d) < 0.5:
                v *= f
        out.append(v)
    out = np.array(out)
    return out / out.max()


VN = _div()
XA = lambda a: -6 + 12 * (540 - a) / 540
YA = lambda v: -1.9 + 3.8 * v
DROPS = [("end-Ordovician", 445, -2.95), ("Devonian", 372, -3.45), ("Late Permian", 252, -2.95),
         ("Late Triassic", 201, -3.45), ("end-Cretaceous", 66, -2.95)]


def curve_mob(n, col=BLUE, w=9):
    n = int(clamp(n, 2, len(AGES)))
    m = VMobject(color=col, stroke_width=w)
    m.set_points_as_corners([[XA(AGES[i]), YA(VN[i]), 0] for i in range(n)])
    return m


# ------------------------------------------------------------------ the timeline (s04, s05)
TX0, TX1, AXY = -5.6, 6.0, -0.4
TXF = lambda age_ga: TX0 + (TX1 - TX0) * (3.48 - age_ga) / 3.48
FLAGS = [("microbial life", "3.48 Ga", TXF(3.48), 1.2, 1), ("red alga", "about 1.05 Ga", TXF(1.05), 1.0, 1),
         ("animals", "about 558 Ma", TXF(.558), 2.0, 1), ("land plants", "about 473-471 Ma", TXF(.472), -1.6, -1)]


def flag_mob(name, date, x, h, d):
    pole = Ln([x, AXY], [x, AXY + (h if d > 0 else h + 0.4 * 0) if d > 0 else h], TEXT, 4)
    ty = h if d > 0 else h
    tri = Polygon([x, ty, 0], [x + .5, ty - .22 * d, 0], [x, ty - .44 * d, 0], color=TEAL, fill_color=TEAL, fill_opacity=.9, stroke_width=2)
    lab = two(name, date, 28)
    cx = clamp(x, -5.2, 5.0)
    if d > 0:
        lab.move_to([cx, h + 0.15 + lab.height / 2, 0])
    else:
        lab.move_to([clamp(x, -5.2, 4.7), h - 0.15 - lab.height / 2 - .45, 0])
    return VGroup(pole, tri, lab)


def timeline_parts(sc):
    axis = Arrow([TX0 - .2, AXY, 0], [TX1, AXY, 0], buff=0, color=GREY, stroke_width=5, tip_length=.25)
    ends = VGroup(T("3.48 Ga", 26, GREY).move_to([-5.2, -1.15, 0]), T("Today", 26, GREY).move_to([5.6, -1.15, 0]))
    shade = Rectangle(width=(TXF(.558) - TX0) + 0.2, height=1.9, stroke_width=0, fill_color=TEAL, fill_opacity=.13)
    shade.move_to([(TX0 + TXF(.558)) / 2 - .1, AXY, 0])
    rng = random.Random(3)
    microbes = VGroup()
    for i in range(11):
        c = Ellipse(width=.5, height=.3, color=TEAL, fill_color=TEAL, fill_opacity=.6, stroke_width=2)
        c.b = np.array([-5.0 + i * 0.85 + rng.uniform(-.2, .2), AXY + rng.uniform(-.7, .7), 0])
        c.ph = rng.uniform(0, 6)
        c.add_updater(lambda m: m.move_to(m.b + [0.18 * math.sin(.9 * sc.elapsed() + m.ph), 0.07 * math.cos(1.3 * sc.elapsed() + m.ph), 0]))
        microbes.add(c)
    flags = [flag_mob(*f) for f in FLAGS]
    cur = Dot(radius=.13, color=YELLOW)
    cur.add_updater(lambda m: m.move_to([TX0 + (sc.elapsed() * 1.6) % (TX1 - TX0), AXY, 0]))
    return axis, ends, shade, microbes, flags, cur


# ------------------------------------------------------------------ flasks (s11-s15)
PUR, TEL = PURPLE, TEAL


class Ref:
    def __init__(self, o):
        self.o = o

    def __deepcopy__(self, memo):
        return self


class Flask:
    def __init__(self, sc, cx, shaken=False, n=14, seed=1, gradient=False):
        self.sc, self.cx, self.off, self.shaken = sc, cx, np.zeros(3), shaken
        pts = [(-.5, 2.4), (-.5, 1.5), (-1.5, .9), (-1.5, -2.4), (1.5, -2.4), (1.5, .9), (.5, 1.5), (.5, 2.4)]
        self.outline = VMobject(color=TEXT, stroke_width=8)
        self.outline.set_points_as_corners([[cx + x, y, 0] for x, y in pts])
        h = 2.9 / 8
        self.strips = VGroup(*[Rectangle(width=3.0, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=.3)
                               .move_to([cx, -2.4 + h * (i + .5), 0]) for i in range(8)])
        self.static = VGroup(self.strips, self.outline)
        if gradient:
            for i, s in enumerate(self.strips):
                s.set_fill(BLUE, opacity=.08 + .5 * (i / 7))
        rng = random.Random(seed)
        self.cells = VGroup()
        for i in range(n):
            c = Circle(radius=.15, color=BLUE, fill_color=BLUE, fill_opacity=.95, stroke_width=2)
            c.b = np.array([cx + rng.uniform(-1.25, 1.25), rng.uniform(-2.05, .25), 0])
            c.ph, c.fl = rng.uniform(0, 6), Ref(self)
            c.amp = .22 if shaken else .07
            c.add_updater(self._cu)
            c.move_to(c.b)
            self.cells.add(c)
        self.group = VGroup(self.static, self.cells)

    @staticmethod
    def _cu(m):
        fo = m.fl.o
        t = fo.sc.renderer.time
        m.move_to(m.b + fo.off + [m.amp * math.sin(1.3 * t + m.ph), m.amp * math.cos(1.7 * t + m.ph * 1.3), 0])

    def sway(self, amp=.14, f=2.2):
        def upd(m):
            off = np.array([amp * math.sin(f * self.sc.renderer.time), 0, 0])
            m.shift(off - self.off)
            self.off = off
        self.static.add_updater(upd)

    def settle_now(self):
        """cells in their final zones (for s15)."""
        self.assign()
        for i, c in enumerate(self.cells):
            c.b = self.zone[i][0]
            c.set_color(self.zone[i][1])
            c.set_fill(self.zone[i][1], opacity=.95)

    def assign(self):
        cx = self.cx
        rng = random.Random(9)
        self.zone = []
        for i in range(len(self.cells)):
            if i < 4:       # stay smooth
                self.zone.append((np.array([cx + rng.uniform(-1.1, 1.1), rng.uniform(-.5, -.1), 0]), BLUE))
            elif i < 7:     # middle zone
                self.zone.append((np.array([cx + rng.uniform(-1.1, 1.1), rng.uniform(-1.3, -.7), 0]), TEL))
            elif i < 10:    # bottom zone
                self.zone.append((np.array([cx + rng.uniform(-1.1, 1.1), rng.uniform(-2.0, -1.6), 0]), PUR))
            elif i < 13:    # surface mat
                self.zone.append((np.array([cx - .9 + (i - 10) * .9, .52, 0]), GOLD))
            else:
                self.zone.append((np.array([cx + rng.uniform(-1.1, 1.1), rng.uniform(-.5, -.1), 0]), BLUE))


def mat_mob(cx):
    return RoundedRectangle(corner_radius=.08, width=2.9, height=.22, stroke_width=0, fill_color=GOLD, fill_opacity=.9).move_to([cx, .5, 0])


def jitter_cells_to(sc, cells, targets, run):
    anims = []
    for c, tg in zip(cells, targets):
        s = c.b.copy()
        anims.append(UpdateFromAlphaFunc(c, lambda m, a, s=s, tg=tg: setattr(m, "b", s * (1 - sm(a)) + tg * sm(a))))
    sc.play(*anims, run_time=run, rate_func=linear)


LX, RX = -3.3, 3.3


def flask_labels():
    return T("unshaken", 30, TEXT).move_to([LX, -3.15, 0]), T("shaken", 30, TEXT).move_to([RX, -3.15, 0])


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    TITLE = "Births Minus Deaths"
    LESSON = LESSON_TITLE


class S01Question(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        planet = VGroup(Circle(radius=.62, color=BLUE, fill_color=BLUE, fill_opacity=.18, stroke_width=4))
        for dx, dy in [(-.25, .2), (.2, .3), (.1, -.25), (-.3, -.2), (.3, -.05)]:
            planet.add(Dot([dx, dy, 0], radius=.06, color=TEAL))
        planet.move_to([-5.75, -0.1, 0])
        tv = TreeView(self, lambda: min(.999, now() / 9.0), xl=-5.0)
        counter = live(lambda: T(f"kinds: {count_at(NODES, tv.cutf())}", 40, YELLOW).move_to([4.5, 3.3, 0]))
        self.play(FadeIn(planet), run_time=.6)
        self.add(tv.mob, counter)
        self.at("microbes")
        lab = T("microbes", 28, TEAL).move_to([-5.45, 0.95, 0])
        self.play(FadeIn(lab), run_time=.5)
        self.at("so many kinds")
        q = T("?", 64, YELLOW).move_to([6.2, 3.3, 0])
        q.add_updater(lambda m: m.move_to([6.2, 3.3 + .1 * math.sin(3 * now()), 0]))
        self.play(FadeIn(q), run_time=.4)
        self.finish()


class S02Two(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        SP = 0.97
        xs = -6.0
        tb = self.t_of("new lineage")
        te = self.t_of("or a lineage") + .5
        xb = xs + SP * tb
        xe = xs + SP * te
        tip = lambda t0=0.0: xs + SP * max(0.0, now() - t0)
        A = live(lambda: Ln([xs, 2.0], [max(xs + .02, min(tip(), 5.4)), 2.0], BLUE, 9))
        B = live(lambda: Ln([xs, .3], [max(xs + .02, min(tip(), 5.4)), .3], BLUE, 6))

        def bud():
            if now() < tb:
                return Dot([xb, .3, 0], radius=.001)
            v = clamp((now() - tb) / .7)
            g = VGroup(Ln([xb, .3], [xb, .3 + .85 * v], GREEN, 6))
            if v >= 1:
                g.add(Ln([xb, 1.15], [min(5.4, xb + SP * (now() - tb - .7)), 1.15], GREEN, 6))
            return g

        def cc():
            dead = now() >= te
            x = min(tip(), xe)
            g = VGroup(Ln([xs, -1.5], [max(xs + .02, x), -1.5], GREY if dead else BLUE, 6))
            if dead:
                g.add(Ln([xe - .2, -1.7], [xe + .2, -1.3], RED, 6), Ln([xe - .2, -1.3], [xe + .2, -1.7], RED, 6))
            return g
        self.add(A, B, live(bud), live(cc))
        self.at("lineages")
        l1 = T("between events, lineages persist", 28, TEXT).move_to([-0.8, 2.6, 0])
        self.play(FadeIn(l1), run_time=.5)
        until(self, tb)
        ring = Circle(radius=.15, color=GREEN, stroke_width=6).move_to([xb, .3, 0])
        self.play(ring.animate.scale(4).set_stroke(opacity=0), run_time=.7)
        self.at("speciation")
        l2 = T("speciation (λ): adds a lineage", 30, GREEN).move_to([-1.2, -.55, 0])
        self.play(FadeIn(l2), run_time=.5)
        until(self, te)
        ring2 = Circle(radius=.15, color=RED, stroke_width=6).move_to([xe, -1.5, 0])
        self.play(ring2.animate.scale(4).set_stroke(opacity=0), run_time=.7)
        self.at("extinction")
        l3 = T("extinction (μ): removes a lineage", 30, RED).move_to([0.4, -2.45, 0])
        self.play(FadeIn(l3), run_time=.5)
        self.finish()


class S03Balance(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        tv = TreeView(self, lambda: min(.999, now() / 12.5))
        self.add(tv.mob)
        # count chart (log axis), tied to the same cut as the tree
        CY0, CY1 = -3.45, -1.7
        maxc = max(count_at(NODES, c / 200) for c in range(200))

        def cline():
            cut = tv.cutf()
            n = max(2, int(cut * 120))
            pts = [[XL + (XR - XL) * (i / 120), CY0 + (CY1 - CY0) * math.log(max(1, count_at(NODES, i / 120))) / math.log(maxc), 0] for i in range(n)]
            m = VMobject(color=YELLOW, stroke_width=6)
            m.set_points_as_corners(pts)
            return m
        axes = VGroup(Ln([XL, CY0], [XR, CY0], GREY, 3), Ln([XL, CY0], [XL, CY1], GREY, 3))
        clab = T("lineages, log scale", 22, GREY).move_to([-3.2, -3.72, 0])
        sch = T("schematic", 22, GREY).move_to([4.9, -3.72, 0])
        self.at("births")
        w1 = VGroup(T("births", 52, GREEN), T("−", 52), T("deaths", 52, RED)).arrange(RIGHT, buff=.3).move_to([0, 3.1, 0])
        self.play(FadeIn(w1), run_time=.5)
        self.at("net rate")
        r_, e_, l_, m_, u_ = T("r", 54), T("=", 54), T("λ", 54, GREEN), T("−", 54), T("μ", 54, RED)
        eq = VGroup(r_, e_, l_, m_, u_).arrange(RIGHT, buff=.3).move_to([0, 3.1, 0])
        self.play(ReplacementTransform(w1, eq), tv.yl.animate.set_value(-0.9), tv.yh.animate.set_value(2.4),
                  FadeIn(axes), FadeIn(clab), FadeIn(sch), run_time=1.0)
        self.add(live(cline))
        self.at("rates", nth=0)
        self.play(Indicate(l_, color=GREEN), Indicate(u_, color=RED), run_time=1.2)
        self.at("lineages turn over")
        self.play(Indicate(l_, color=GREEN), Indicate(u_, color=RED), run_time=1.2)
        self.at("a slow total")
        cap = T("same slow total, different rates", 36, YELLOW).move_to([0, 3.1, 0])
        base = -0.75

        def pair(cx, hg, hr):
            g = Rectangle(width=.7, height=hg, stroke_width=0, fill_color=GREEN, fill_opacity=.95).move_to([cx - .9, base + hg / 2, 0])
            r = Rectangle(width=.7, height=hr, stroke_width=0, fill_color=RED, fill_opacity=.95).move_to([cx, base + hr / 2, 0])
            s = Rectangle(width=.7, height=.2, stroke_width=0, fill_color=BLUE, fill_opacity=.95).move_to([cx + .9, base + .1, 0])
            rl = T("r", 28, BLUE).move_to([cx + .9, base + .5, 0])
            return VGroup(g, r, s, rl)
        p1, p2 = pair(-2.6, 2.2, 2.0), pair(2.6, .75, .55)
        lab1 = T("if both high", 28, TEXT).move_to([-2.6, -1.25, 0])
        lab2 = T("if both low", 28, TEXT).move_to([2.6, -1.25, 0])
        self.remove(tv.mob)
        self.play(FadeOut(eq), FadeIn(cap), run_time=.6)
        self.play(GrowFromEdge(p1, DOWN), GrowFromEdge(p2, DOWN), FadeIn(lab1), FadeIn(lab2), run_time=1.2)
        self.finish()


class S04Timeline(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        axis, ends, shade, microbes, flags, cur = timeline_parts(self)
        tv = TreeView(self, lambda: .999)
        self.add(tv.mob)
        self.wait(.4)
        self.play(tv.xr.animate.set_value(-4.7), tv.yl.animate.set_value(-.7), tv.yh.animate.set_value(-.1),
                  Create(axis), run_time=2.2)
        self.add(cur)
        self.remove(tv.mob)
        self.play(FadeIn(ends), run_time=.5)
        self.at("traces")
        self.play(FadeIn(flags[0], shift=DOWN * .3), run_time=.6)
        self.at("for most of that time")
        self.play(GrowFromEdge(shade, LEFT), run_time=1.5)
        self.at("microbial")
        self.play(FadeIn(microbes), run_time=1.0)
        self.at("new kinds")
        self.play(FadeIn(flags[1], shift=DOWN * .4), run_time=.6)
        self.wait(.3)
        self.play(FadeIn(flags[2], shift=DOWN * .4), run_time=.6)
        self.at("flags")
        self.play(FadeIn(flags[3], shift=DOWN * .4), run_time=.6)
        self.finish()


class S05Floors(SpokenScene):
    def construct(self):
        tick(self)
        axis, ends, shade, microbes, flags, cur = timeline_parts(self)
        self.add(axis, ends, shade, microbes, *flags, cur)
        self.at("early fossil record")
        self.play(*[Indicate(f[1], color=YELLOW) for f in flags], run_time=1.2)
        self.at("by this time")
        arrows = VGroup()
        for (nm, dt, x, h, d), f in zip(FLAGS[:3], flags):
            y0 = min(h - .45, .9) if d > 0 else -.9
            a = Arrow([x - .25, y0, 0], [x - .25, AXY + (.1 if d > 0 else -.1), 0], buff=0, color=YELLOW, stroke_width=5, tip_length=.2) if d > 0 else Arrow([x - .25, -.9, 0], [x - .25, AXY - .08, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=.2)
            arrows.add(a)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.3), run_time=1.3)
        lab = T("by this time, at the latest", 28, YELLOW).move_to([-2.4, 2.9, 0])
        self.play(FadeIn(lab), run_time=.5)
        self.at("oxygen in the air")
        x1, x2 = TXF(2.46), TXF(2.426)
        band = Rectangle(width=max(.1, x2 - x1), height=1.9, stroke_width=0, fill_color=GOLD, fill_opacity=.55).move_to([(x1 + x2) / 2, AXY, 0])
        self.play(FadeIn(band), FadeOut(arrows[0]), run_time=.6)
        self.at("dated from both sides")
        bl = VMobject(color=GOLD, stroke_width=6)
        bl.set_points_as_corners([[x1 - .0, AXY + 1.0, 0], [x1 - .3, AXY + 1.0, 0], [x1 - .3, AXY - 1.0, 0], [x1, AXY - 1.0, 0]])
        br = VMobject(color=GOLD, stroke_width=6)
        br.set_points_as_corners([[x2, AXY + 1.0, 0], [x2 + .3, AXY + 1.0, 0], [x2 + .3, AXY - 1.0, 0], [x2, AXY - 1.0, 0]])
        goe = two("Great Oxidation Event", "onset about 2,460-2,426 Ma", 26, TEXT, GOLD).move_to([(x1 + x2) / 2 + .6, -2.15, 0])
        self.play(Create(bl), Create(br), FadeIn(goe), run_time=1.2)
        self.finish()


class S06Cliffs(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        axis = VGroup(Ln([-6.2, -2.05], [6.2, -2.05], GREY, 4))
        ends = VGroup(T("540 Ma", 24, GREY).move_to([-5.6, -2.45, 0]), T("Today", 24, GREY).move_to([5.7, -2.45, 0]))
        sch = T("schematic", 22, GREY).move_to([5.6, -3.65, 0])
        self.play(Create(axis), FadeIn(ends), FadeIn(sch), run_time=.9)
        t0 = now()
        n_of = lambda: (now() - t0) / 4.4 * 540
        self.add(live(lambda: curve_mob(n_of())))
        labels = []
        for (nm, age, ly) in DROPS:
            x = XA(age)
            labels.append(VGroup(Ln([x, -2.05], [x, -1.85], RED, 5), Ln([x, -2.05], [x, ly + .25], RED, 2), T(nm, 24, RED).move_to([x, ly, 0])))
        for i, lb in enumerate(labels):
            until(self, t0 + 4.4 * (540 - DROPS[i][1]) / 540 + .1)
            self.add(lb)
        self.at("benchmark")
        bm = VGroup(T("benchmark: more than 3/4 of species lost", 28, TEXT), T("in a geologically short interval", 28, TEXT)).arrange(DOWN, buff=.1).move_to([0, 3.25, 0])
        self.play(FadeIn(bm), run_time=.6)
        dot = Dot(radius=.14, color=YELLOW)
        dot.add_updater(lambda m: m.move_to([XA(AGES[min(540, int(((now() - t0 - 4.4) % 6.0) / 6.0 * 540) % 541)]),
                                              YA(VN[min(540, int(((now() - t0 - 4.4) % 6.0) / 6.0 * 540) % 541)]), 0]))
        self.add(dot)
        self.at("each lost most")
        for (nm, age, ly) in DROPS:
            i = 540 - int(age) + 2
            ring = Circle(radius=.12, color=RED, stroke_width=6).move_to([XA(age), YA(VN[i]), 0])
            self.play(ring.animate.scale(5).set_stroke(opacity=0), run_time=.5)
        self.at("how sharply")
        deb = T("how sharply each stands out: debated", 32, YELLOW).move_to([0, 3.25, 0])
        self.play(FadeOut(bm), FadeIn(deb), run_time=.6)
        self.finish()


class S07Kt(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        i0, i1 = 410, 530
        win = VN[i0:i1 + 1]
        lo, hi = win.min(), win.max()
        X2 = lambda i: -5.8 + 11.6 * (i - i0) / (i1 - i0)
        Y2 = lambda v: -2.0 + 4.2 * (v - lo) / (hi - lo)
        t0 = now()

        def zc():
            n = int(clamp((now() - t0) / 2.6) * (i1 - i0)) + 2
            m = VMobject(color=BLUE, stroke_width=7)
            m.set_points_as_corners([[X2(i0 + k), Y2(VN[i0 + k]), 0] for k in range(min(n, i1 - i0 + 1))])
            return m
        title = T("end-Cretaceous", 38, TEXT).move_to([0, 3.3, 0])
        self.add(live(zc))
        self.play(FadeIn(title), run_time=.6)
        xd = X2(474)
        vl = DashedLine([xd, -2.0, 0], [xd, 2.4, 0], color=YELLOW, stroke_width=4)
        lab66 = T("66 Ma", 38, YELLOW).move_to([xd + 1.0, -2.7, 0])
        self.at("end of the cretaceous")
        self.play(Create(vl), FadeIn(lab66), run_time=.9)
        self.at("what tipped")
        q = T("?", 80, YELLOW)
        q.add_updater(lambda m: m.move_to([xd + 1.6, 0.8 + .15 * math.sin(3 * now()), 0]))
        self.play(FadeIn(q), run_time=.4)
        until(self, self.t_of("alvarez") - .6)
        self.clear()
        # world map outline
        k = .0255
        mx = lambda lon: lon * k
        my = lambda lat: 3.05 - (70 - lat) * k
        land = {
            "na": [(-168, 66), (-140, 70), (-95, 72), (-62, 60), (-55, 48), (-80, 25), (-97, 17), (-82, 8), (-105, 20), (-125, 40), (-125, 50)],
            "sa": [(-80, 8), (-60, 10), (-35, -6), (-40, -23), (-58, -40), (-68, -45), (-72, -20), (-80, -3)],
            "eu": [(-10, 36), (-10, 55), (5, 62), (30, 70), (100, 75), (180, 68), (160, 55), (140, 40), (122, 30), (110, 10), (100, 15), (80, 8), (60, 25), (35, 30), (25, 38), (10, 44)],
            "af": [(-17, 15), (-5, 36), (32, 31), (43, 12), (51, 11), (40, -15), (25, -34), (15, -28), (10, -5), (-8, 4)],
            "au": [(114, -22), (130, -12), (145, -12), (153, -27), (145, -38), (130, -32), (115, -34)],
            "nz": [(172, -35), (178, -38), (173, -46), (167, -45)],
        }
        world = VGroup(*[Polygon(*[[mx(a), my(b), 0] for a, b in p], color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=.22) for p in land.values()])
        card = T("Alvarez, Alvarez, Asaro and Michel, 1980", 28, TEXT).move_to([0, 3.55, 0])
        self.play(FadeIn(world), FadeIn(card), run_time=.9)
        cols_x = [-4.6, -1.6, 1.4]
        names = ["Denmark", "Italy", "New Zealand"]
        pins_xy = [(mx(10), my(56)), (mx(12), my(43)), (mx(174), my(-41))]
        cols, bands = VGroup(), VGroup()
        for cx in cols_x:
            body = Rectangle(width=1.5, height=2.75, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.25).move_to([cx, -1.725, 0])
            lines = VGroup(*[Ln([cx - .75, y], [cx + .75, y], GREY, 1.5) for y in (-.9, -2.4, -2.8)])
            band = Rectangle(width=1.5, height=.26, stroke_width=0, fill_color=GOLD, fill_opacity=.95).move_to([cx, -1.7, 0])
            cols.add(VGroup(body, lines))
            bands.add(band)
        self.at("extra iridium")
        self.play(GrowFromEdge(cols, DOWN), run_time=1.0)
        self.play(FadeIn(bands), run_time=.7)
        self.add(bands)
        bands.add_updater(lambda m: m.set_opacity(.65 + .3 * math.sin(3 * now())))
        self.at("three distant sites")
        for nm, cx, (px, py) in zip(names, cols_x, pins_xy):
            pin = Dot([px, py, 0], radius=.11, color=YELLOW)
            lead = DashedLine([px, py, 0], [cx, -.35, 0], color=YELLOW, stroke_width=2)
            nl = T(nm, 26, TEXT).move_to([cx, -3.45, 0])
            self.play(FadeIn(pin), Create(lead), FadeIn(nl), run_time=.7)
            self.wait(.15)
        self.at("iridium", nth=1)
        it = T("iridium", 30, GOLD).move_to([3.9, -.55, 0])
        self.play(FadeIn(it), run_time=.4)
        self.at("scarce")
        b1 = Rectangle(width=.7, height=.14, stroke_width=0, fill_color=GOLD, fill_opacity=.95).move_to([4.2, -3.0 + .07, 0])
        l1 = T("crust", 24, TEXT).move_to([4.2, -3.45, 0])
        self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), run_time=.6)
        self.at("richer")
        b2 = Rectangle(width=.7, height=1.5, stroke_width=0, fill_color=GOLD, fill_opacity=.95).move_to([5.8, -3.0 + .75, 0])
        l2 = T("meteorites", 24, TEXT).move_to([5.8, -3.45, 0])
        met = VGroup(Circle(radius=.28, color=GREY, fill_color=GREY, fill_opacity=.6, stroke_width=3), Ln([-.9, .5], [-.25, .1], GOLD, 5)).move_to([5.8, -1.0, 0])
        self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), FadeIn(met), run_time=.9)
        self.finish()


class S08Crater(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        panL = DashedVMobject(Rectangle(width=6.0, height=3.8, color=GREY, stroke_width=4).move_to([-3.5, 1.4, 0]), num_dashes=50)
        solidL = Rectangle(width=6.0, height=3.8, color=GREY, stroke_width=4).move_to([-3.5, 1.4, 0])
        panR = Rectangle(width=6.0, height=3.8, color=GREY, stroke_width=4).move_to([3.5, 1.4, 0])
        # lower strip: the end-Cretaceous marker carried from before
        tl = Arrow([-5.8, -2.2, 0], [5.8, -2.2, 0], buff=0, color=GREY, stroke_width=4, tip_length=.2)
        sep = ValueTracker(3.0)
        ext = live(lambda: Dot([sep.get_value(), -2.2, 0], radius=.16, color=RED))
        extl = live(lambda: T("extinction", 28, RED).move_to([sep.get_value(), -2.85, 0]))
        self.play(Create(panL), Create(tl), FadeIn(ext), FadeIn(extl), run_time=.9)
        hyp = T("hypothesis", 28, YELLOW).move_to([-3.5, 3.0, 0])
        self.at("hypothesis")
        self.play(FadeIn(hyp), run_time=.5)
        ground = Ln([-6.4, .0], [-.6, .0], GREY, 4)
        plant = VGroup(Ln([-1.6, 0], [-1.6, .9], GREEN, 6), Ellipse(width=.6, height=.28, color=GREEN, fill_color=GREEN, fill_opacity=.8).move_to([-1.9, .75, 0]).rotate(.5),
                       Ellipse(width=.6, height=.28, color=GREEN, fill_color=GREEN, fill_opacity=.8).move_to([-1.3, .6, 0]).rotate(-.5))
        self.play(FadeIn(ground), FadeIn(plant), run_time=.6)
        self.at("an asteroid")
        ast = VGroup(Circle(radius=.3, color=TEXT, fill_color=GREY, fill_opacity=.9, stroke_width=3), Ln([-.9, .5], [-.3, .15], RED, 6)).move_to([-6.0, 2.5, 0])
        self.add(ast)
        self.play(ast.animate.move_to([-4.0, .35, 0]), run_time=1.5, rate_func=rush_into)
        puffs = VGroup(*[Circle(radius=.35, color=GREY, fill_color=GREY, fill_opacity=.45, stroke_width=0).move_to([-4.0 + dx, .5 + dy, 0])
                         for dx, dy in [(0, 0), (-.4, .2), (.4, .15), (0, .5), (-.7, .45), (.7, .5)]])
        self.remove(ast)
        self.play(GrowFromCenter(puffs), plant.animate.set_opacity(.3), run_time=1.6)
        self.play(puffs.animate.scale(1.5).shift(RIGHT * .6 + UP * .25).set_opacity(.3), run_time=1.0)
        self.at("crater of the right age")
        land = Polygon(*[[a, b, 0] for a, b in [(.5, -.35), (.5, 3.1), (3.4, 3.1), (3.9, 2.9), (4.6, 2.8), (5.3, 2.3), (5.2, 1.8), (4.5, 2.0), (4.1, 1.6), (3.3, .8), (2.7, -.35)]],
                        color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=.2)
        ring_d = DashedVMobject(Circle(radius=.85, color=YELLOW, stroke_width=5).move_to([4.2, 2.35, 0]), num_dashes=24)
        self.play(Create(panR), FadeIn(land), run_time=.8)
        self.play(Create(ring_d), run_time=1.0)
        self.at("buried crater")
        ring_s = Circle(radius=.85, color=YELLOW, stroke_width=7).move_to([4.2, 2.35, 0])
        ring_s2 = Circle(radius=.5, color=YELLOW, stroke_width=3).move_to([4.2, 2.35, 0])
        self.play(ReplacementTransform(ring_d, ring_s), FadeIn(ring_s2), ReplacementTransform(panL, solidL), run_time=1.0)
        self.at("chicxulub")
        cl = T("Chicxulub", 30, YELLOW).move_to([4.6, .15, 0])
        self.play(FadeIn(cl), run_time=.5)
        self.at("mexico")
        mx = T("Mexico", 26, TEXT).move_to([1.7, 2.3, 0])
        self.play(FadeIn(mx), run_time=.5)
        imp = live(lambda: Dot([-sep.get_value() if sep.get_value() < 3 else -3.0, -2.2, 0], radius=.16, color=YELLOW) if False else Dot([-(sep.get_value()), -2.2, 0], radius=.16, color=YELLOW))
        impl = live(lambda: T("impact", 28, YELLOW).move_to([-sep.get_value(), -1.6, 0]))
        self.at("dating")
        self.play(FadeIn(imp), FadeIn(impl), run_time=.6)
        self.wait(.3)
        self.play(sep.animate.set_value(.3), run_time=1.6)
        self.at("closely")
        br = VMobject(color=GOLD, stroke_width=6)
        br.set_points_as_corners([[-.5, -3.2, 0], [-.5, -3.4, 0], [.5, -3.4, 0], [.5, -3.2, 0]])
        self.play(Create(br), run_time=.7)
        self.finish()


class S09Trigger(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        P = np.array([0, 1.2, 0])
        key = [(0, 0), (1.6, 0), (2.6, .22), (4.2, .22), (5.2, .02), (7.9, .02), (10.5, .18), (12, .18)]
        kt, kv = zip(*key)

        def phi():
            t = now()
            b = float(np.interp(t, kt, kv))
            if t > 7.9:
                b += .12 * math.exp(-(t - 7.9) / 2.2) * math.sin(4.2 * (t - 7.9))
            return b
        ends = lambda: (np.array([-3.6 * math.cos(phi()), 1.2 - 3.6 * math.sin(phi()), 0]), np.array([3.6 * math.cos(phi()), 1.2 + 3.6 * math.sin(phi()), 0]))
        stand = VGroup(Ln([0, 1.2], [0, -1.9], GREY, 8), Rectangle(width=2.2, height=.2, stroke_width=0, fill_color=GREY, fill_opacity=.8).move_to([0, -2.0, 0]))
        beam = live(lambda: Ln(ends()[0], ends()[1], TEXT, 8))

        def pan(side):
            e = ends()[0 if side < 0 else 1]
            c = e + np.array([0, -1.4, 0])
            return VGroup(Ln(e, c + [-1.1, 0, 0], GREY, 3), Ln(e, c + [1.1, 0, 0], GREY, 3),
                          Rectangle(width=2.4, height=.16, stroke_width=0, fill_color=TEXT, fill_opacity=.9).move_to(c))
        pl, pr = live(lambda: pan(-1)), live(lambda: pan(1))
        self.play(FadeIn(stand), FadeIn(beam), FadeIn(pl), FadeIn(pr), run_time=.8)
        self.at("evidence points")
        ban = T("evidence points to the impact as trigger", 34, YELLOW).move_to([0, 3.3, 0])
        self.play(FadeIn(ban), run_time=.6)
        self.at("impact")
        crater = live(lambda: VGroup(Circle(radius=.6, color=YELLOW, stroke_width=8), Circle(radius=.3, color=YELLOW, stroke_width=3)).move_to(ends()[0] + [0, -1.4 + .75, 0]))
        cl = T("Chicxulub impact", 28, YELLOW).move_to([-3.3, -2.9, 0])
        self.play(FadeIn(crater, shift=DOWN * .5), FadeIn(cl), run_time=.8)
        self.at("volcanic")
        volc = live(lambda: VGroup(Polygon([-.7, 0, 0], [.7, 0, 0], [.15, 1.0, 0], [-.15, 1.0, 0], color=GREY, fill_color=GREY, fill_opacity=.6, stroke_width=3),
                                            Polygon([-.15, 1.0, 0], [.15, 1.0, 0], [.0, 1.4, 0], color=RED, fill_color=RED, fill_opacity=.9, stroke_width=2)).move_to(ends()[1] + [0, -1.4 + .62, 0]))
        self.play(FadeIn(volc, shift=DOWN * .5), run_time=.8)
        self.at("deccan")
        vl = two("Deccan flood basalts", "India", 28, RED, TEXT).move_to([3.5, -2.9, 0])
        self.play(FadeIn(vl), run_time=.5)
        self.finish()


class S10Mammals(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        # fan of lineages after the drop (hand-built, balanced, schematic)
        def mk(t0, t1, depth):
            n = dict(t0=t0, t1=t1, kids=[], ext=False, par=None)
            if depth > 0:
                step = (1.0 - t1) / depth if False else 0
                span = (1.0 - t1) / depth
                for _ in range(2):
                    k = mk(t1, t1 + span, depth - 1)
                    k["par"] = n
                    n["kids"].append(k)
            return n

        def flat(n):
            return [n] + [x for k in n["kids"] for x in flat(k)]
        root = mk(0.0, 0.25, 3)
        fan = _layout(flat(root))
        cx0 = -3.2
        tv = TreeView(self, lambda: clamp((now() - 1.9) / 5.2), nodes=fan, xl=cx0, xr=4.8, yl=-1.0, yh=2.8, line=GREEN, conn=GREEN)
        ys = fan[0]["y"] * 3.8 - 1.0
        # before the drop: three lineages, two end
        pre = VGroup(Ln([-6.2, 1.9], [cx0, 1.9], BLUE, 3), Ln([-6.2, ys], [cx0, ys], BLUE, 5), Ln([-6.2, -0.3], [cx0, -0.3], BLUE, 3))
        cliff = DashedLine([cx0, -2.2, 0], [cx0, 3.0, 0], color=RED, stroke_width=4)
        l66 = T("66 Ma", 32, YELLOW).move_to([cx0, -2.6, 0])
        self.play(Create(pre), run_time=.9)
        self.play(Create(cliff), FadeIn(l66), run_time=.6)
        ad = T("already diverse", 28, BLUE).move_to([-4.7, 2.7, 0])
        crosses = VGroup()
        for y in (1.9, -0.3):
            crosses.add(Ln([cx0 - .13, y - .13], [cx0 + .13, y + .13], RED, 5), Ln([cx0 - .13, y + .13], [cx0 + .13, y - .13], RED, 5))
        self.play(FadeIn(crosses), FadeIn(ad), run_time=.6)
        self.at("survivors")
        self.add(tv.mob)
        self.at("niches")
        nl = T("emptied niches", 30, GREEN).move_to([0.6, 3.4, 0])
        self.play(FadeIn(nl), run_time=.5)
        self.at("placental")
        leaves = [n for n in fan if not n["kids"]]
        sil = VGroup()
        for n in leaves:
            y = n["y"] * 3.8 - 1.0
            body = Ellipse(width=.5, height=.28, color=GREEN, fill_color=GREEN, fill_opacity=.9, stroke_width=1)
            head = Circle(radius=.13, color=GREEN, fill_color=GREEN, fill_opacity=.9, stroke_width=1).move_to([.3, .1, 0])
            ear = Circle(radius=.06, color=GREEN, fill_color=GREEN, fill_opacity=.9, stroke_width=1).move_to([.34, .25, 0])
            tail = Ln([-.25, 0], [-.45, .1], GREEN, 3)
            sil.add(VGroup(body, head, ear, tail).move_to([5.3, y, 0]))
        self.play(LaggedStart(*[FadeIn(s) for s in sil], lag_ratio=.25), run_time=2.2)
        self.at("timing alone")
        q = T("?", 70, YELLOW)
        q.add_updater(lambda m: m.move_to([5.9, 3.3 + .1 * math.sin(3 * now()), 0]))
        why = T("release from competitors? climate?", 30, YELLOW).move_to([0.4, -3.1, 0])
        self.play(FadeIn(q), FadeIn(why), run_time=.6)
        self.finish()


class S11Flask(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        t0 = now()
        # a long timeline strip with the five drops (carried idea), then it rolls away
        strip = VGroup(Ln([-6.2, -1.2], [6.2, -1.2], GREY, 4))
        cv = VMobject(color=BLUE, stroke_width=7)
        cv.set_points_as_corners([[XA(a), -1.0 + 2.4 * v, 0] for a, v in zip(AGES, VN)])
        grow = lambda: curve_mob(0)
        part = live(lambda: (lambda n: (lambda m: (m.set_points_as_corners([[XA(AGES[i]), -1.0 + 2.4 * VN[i], 0] for i in range(n)]), m)[1])(VMobject(color=BLUE, stroke_width=7)))(int(clamp((now() - t0) / 2.4) * 539) + 2))
        ttl = T("the fossil record", 36, TEXT).move_to([0, 2.7, 0])
        self.play(Create(strip), FadeIn(ttl), run_time=.6)
        self.add(part)
        self.at("rerun")
        arc = Arc(radius=1.1, start_angle=.6, angle=4.8, color=TEXT, stroke_width=9).add_tip(tip_length=.3)
        cross = VGroup(Ln([-.7, -.7], [.7, .7], RED, 10), Ln([-.7, .7], [.7, -.7], RED, 10))
        grp = VGroup(arc, cross).move_to([0, .3, 0])
        self.play(Create(arc), part.animate.set_opacity(.35), run_time=.9)
        self.play(Create(cross), run_time=.5)
        self.at("bacteria")
        self.play(FadeOut(VGroup(strip, ttl, grp, part), shift=LEFT * 3), run_time=.9)
        self.remove(part)
        fl, fr = Flask(self, LX, seed=1), Flask(self, RX, seed=2)
        self.play(FadeIn(fl.static, shift=UP * .4), FadeIn(fr.static, shift=UP * .4), run_time=.9)
        self.add(fl.cells, fr.cells)
        self.play(FadeIn(fl.cells), FadeIn(fr.cells), run_time=.7)
        self.at("rainy")
        card = T("Rainey and Travisano, 1998", 30, TEXT).move_to([0, 3.4, 0])
        self.play(FadeIn(card), run_time=.5)
        self.at("one genotype")
        tube = chip("one genotype", BLUE, 28).move_to([0, 1.3, 0])
        a1 = Arrow([-.8, 1.0, 0], [LX + .5, .55, 0], buff=0, color=BLUE, stroke_width=5, tip_length=.2)
        a2 = Arrow([.8, 1.0, 0], [RX - .5, .55, 0], buff=0, color=BLUE, stroke_width=5, tip_length=.2)
        self.play(FadeIn(tube), run_time=.5)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=.7)
        self.at("two kinds")
        self.play(Indicate(fl.outline, color=YELLOW), Indicate(fr.outline, color=YELLOW), run_time=1.0)
        self.finish()


def flask_scene_base(sc, state="uniform"):
    """Rebuild the two flasks exactly as at the end of s11/s12."""
    fl = Flask(sc, LX, seed=1, gradient=(state != "uniform"))
    fr = Flask(sc, RX, shaken=(state != "uniform"), seed=2)
    return fl, fr


class S12Predict(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        fl, fr = Flask(self, LX, seed=1), Flask(self, RX, seed=2)
        self.add(fl.static, fr.static, fl.cells, fr.cells)
        ul, sl = flask_labels()
        self.at("one flasks")
        self.play(FadeIn(ul), run_time=.4)
        self.at("changes from")
        self.play(*[s.animate.set_fill(BLUE, opacity=.08 + .5 * (i / 7)) for i, s in enumerate(fl.strips)], run_time=1.6)
        self.at("the other")
        self.play(FadeIn(sl), run_time=.4)
        fr.shaken = True
        for c in fr.cells:
            c.amp = .25
        fr.sway(.16, 2.4)
        self.at("which will grow")
        qs = VGroup(T("?", 64, YELLOW).move_to([LX, 3.0, 0]), T("?", 64, YELLOW).move_to([RX, 3.0, 0]))
        qs.add_updater(lambda m: m.shift(UP * (.1 * math.cos(3 * now()) * 0.02)))
        self.play(FadeIn(qs), run_time=.5)
        self.finish()


class S13Pause(Scene):
    def construct(self):
        tick(self)
        self.camera.background_color = BG
        now = lambda: self.renderer.time
        fl = Flask(self, LX, seed=1, gradient=True)
        fr = Flask(self, RX, shaken=True, seed=2)
        for c in fr.cells:
            c.amp = .25
        fr.sway(.16, 2.4)
        ul, sl = flask_labels()
        cap = T("Predict: which flask diversifies?", 36, YELLOW).move_to([0, 3.3, 0])
        cd = live(lambda: T(str(max(1, 5 - int(now()))), 90, TEXT).move_to([0, 0.2, 0]))
        self.add(fl.static, fr.static, fl.cells, fr.cells, ul, sl, cap, cd)
        self.wait(5.0)


class S14Reveal(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        fl = Flask(self, LX, seed=1, gradient=True)
        fr = Flask(self, RX, shaken=True, seed=2)
        for c in fr.cells:
            c.amp = .25
        fr.sway(.16, 2.4)
        fl.assign()
        ul, sl = flask_labels()
        self.add(fl.static, fr.static, fl.cells, fr.cells, ul, sl)
        self.at("only the still flask")
        self.play(Indicate(fl.outline, color=YELLOW), run_time=1.2)
        self.at("new heritable")
        pops = []
        for i, c in enumerate(fl.cells):
            col = fl.zone[i][1]
            if col != BLUE:
                pops.append(c.animate.set_color(col).set_fill(col, opacity=.95).scale(1.3))
        self.play(LaggedStart(*pops, lag_ratio=.12), run_time=2.0)
        self.at("settled into")
        move = [c for i, c in enumerate(fl.cells) if fl.zone[i][1] in (TEL, PUR)]
        tg = [fl.zone[i][0] for i, c in enumerate(fl.cells) if fl.zone[i][1] in (TEL, PUR)]
        for c in move:
            c.amp = .05
        jitter_cells_to(self, move, tg, 2.4)
        self.at("wrinkly")
        gold = [c for i, c in enumerate(fl.cells) if fl.zone[i][1] == GOLD]
        gt = [fl.zone[i][0] for i, c in enumerate(fl.cells) if fl.zone[i][1] == GOLD]
        jitter_cells_to(self, gold, gt, 1.0)
        mat = mat_mob(LX)
        wl = T("wrinkly spreader", 30, GOLD).move_to([LX, 3.3, 0])
        lead = Ln([LX, 2.95], [LX, .8], GOLD, 3)
        self.play(FadeIn(mat), FadeIn(wl), Create(lead), run_time=.8)
        self.at("the shaken flask")
        sl2 = T("smooth ancestral type", 28, BLUE).move_to([RX, 3.3, 0])
        sch = T("schematic", 22, GREY).move_to([0, -3.5, 0])
        self.play(FadeIn(sl2), FadeIn(sch), Indicate(fr.outline, color=YELLOW), run_time=.9)
        self.finish()


class S15Logic(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        fl = Flask(self, LX, seed=1, gradient=True)
        fl.settle_now()
        for c in fl.cells:
            c.amp = .06
        mat = mat_mob(LX)
        self.add(fl.static, fl.cells, mat)
        ul, _ = flask_labels()
        self.add(ul)
        l1 = T("open niches", 40, TEAL)
        l2 = T("+ heritable variation", 40, PURPLE)
        l3 = T("= repeatable", 40, GREEN)
        l4 = T("diversification", 40, GREEN)
        ban = VGroup(l1, l2, l3, l4).arrange(DOWN, aligned_edge=LEFT, buff=.28).move_to([3.0, 1.0, 0])
        self.at("open niches")
        self.play(FadeIn(l1, shift=RIGHT * .3), run_time=.7)
        self.at("heritable")
        self.play(FadeIn(l2, shift=RIGHT * .3), run_time=.7)
        self.at("repeatable")
        self.play(FadeIn(l3, shift=RIGHT * .3), FadeIn(l4, shift=RIGHT * .3), run_time=.9)
        self.at("these were new types")
        tag = VGroup(T("morphs of one bacterium,", 30, YELLOW), T("not new species", 30, YELLOW)).arrange(DOWN, buff=.12).move_to([3.0, -2.2, 0])
        self.play(FadeIn(tag), run_time=.7)
        self.finish()


class S16Rule(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        axis = Ln([-6.2, -2.05], [6.2, -2.05], GREY, 4)
        ends = VGroup(T("540 Ma", 24, GREY).move_to([-5.6, -2.45, 0]), T("Today", 24, GREY).move_to([5.7, -2.45, 0]))
        sch = T("schematic", 24, GREY).move_to([0, -2.45, 0])
        curve = curve_mob(541)
        # gauge: births and deaths at the cursor
        ag = AGES
        lam = .3 + sum(.7 * np.exp(-np.clip(ag - 0, 0, None) * 0) * 0 for _ in [0]) + np.zeros_like(ag)
        mu = .25 + np.zeros_like(ag)
        for d in (445, 372, 252, 201, 66):
            mu = mu + 1.0 * np.exp(-((ag - d) / 7.0) ** 2)
            lam = lam + .6 * np.where(ag < d, np.exp(-(d - ag) / 35.0), 0)
        lam, mu = lam / lam.max(), mu / mu.max()
        D = 12.6
        t0 = now()
        idx = lambda: int(clamp((now() - .5) / D) * 540)
        box = Rectangle(width=2.8, height=2.4, color=GREY, stroke_width=3).move_to([-4.9, 2.4, 0])
        gl = T("births", 22, GREEN).move_to([-5.45, 1.0, 0])
        gr = T("deaths", 22, RED).move_to([-4.35, 1.0, 0])

        def gauge():
            i = idx()
            return VGroup(Rectangle(width=.8, height=2.0 * lam[i] + .02, stroke_width=0, fill_color=GREEN, fill_opacity=.95).move_to([-5.45, 1.25 + (2.0 * lam[i] + .02) / 2, 0]),
                          Rectangle(width=.8, height=2.0 * mu[i] + .02, stroke_width=0, fill_color=RED, fill_opacity=.95).move_to([-4.35, 1.25 + (2.0 * mu[i] + .02) / 2, 0]))
        dot = Dot(radius=.15, color=YELLOW)
        dot.add_updater(lambda m: m.move_to([XA(AGES[idx()]), YA(VN[idx()]), 0]))
        self.add(axis, ends, sch, curve, box, gl, gr, live(gauge), dot)
        self.at("diversity changes")
        ban = T("diversity changes by births minus deaths", 36, YELLOW).move_to([0, -3.3, 0])
        self.play(FadeIn(ban), run_time=.7)
        self.at("mass extinctions")
        self.play(Indicate(gr, color=RED), run_time=1.0)
        self.at("outrun")
        self.play(Indicate(gr, color=RED), run_time=1.0)
        self.at("survivors")
        self.play(Indicate(gl, color=GREEN), run_time=1.0)
        self.finish()


class S17End(EndCard):
    LINE = "Diversity changes by births minus deaths of lineages."
