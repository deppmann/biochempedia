"""Two Rates, One Crossing  (island biogeography; Biochemistrypedia explainer)

COLOUR MAP (same in both films)
  BLUE = immigration of new species, I(S)      RED = local extinction, E(S)
  GOLD = the crossing, S*                      TEXT = labels, axes
  Species tokens are small multicoloured dots (schematic).
Curves are computed from I(S) = b(1 - S/100) and E(S) = e*S with P = 100 (b = 10, e = 0.1 unless a scene changes them).
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PAL = ["#E07BE0", "#9B7BFF", "#4ED6A4", "#FF9F43", "#B8E04A", "#F78FB3", "#C69C6D", "#DDE6F0", "#2EC4B6", "#FFB4A2"]
SEA = "#2A8C99"
RIP = "#6FD0DA"
LAND = "#2E6B45"
LANDS = "#7FBF8A"
YMAX = 11.0
ORDER = list(range(100))
random.Random(11).shuffle(ORDER)


# ---------------------------------------------------------------------------------------------
# the model (computed)
# ---------------------------------------------------------------------------------------------
def _ss(t):
    return 3 * t * t - 2 * t ** 3


def _g(t, bend):
    return (1 - bend) * t + bend * _ss(t)


def I_of(s, b, bend=0.0):
    return b * (1 - _g(s / 100.0, bend))


def E_of(s, e, bend=0.0):
    return 100.0 * e * _g(s / 100.0, bend)


def crossing(b, e, bend=0.0):
    lo, hi = 0.0, 100.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if I_of(mid, b, bend) - E_of(mid, e, bend) > 0:
            lo = mid
        else:
            hi = mid
    return lo, I_of(lo, b, bend)


def smax(e, bend):
    s = 100.0
    while s > 1 and E_of(s, e, bend) > YMAX:
        s -= 0.5
    return s


class Plot:
    def __init__(self, b=10.0, e=0.1, bend=0.0, center=(-2.9, 0.0), xl=6.2, yl=4.4, ticks=True):
        self.bt, self.et, self.bd = ValueTracker(b), ValueTracker(e), ValueTracker(bend)
        self.ax = Axes(x_range=[0, 100, 50], y_range=[0, YMAX, 5], x_length=xl, y_length=yl, tips=False,
                       axis_config={"color": TEXT, "stroke_width": 3, "include_ticks": False}).move_to([center[0], center[1], 0])
        ax = self.ax
        parts = [ax]
        if ticks:
            parts += [M("0", 24).next_to(ax.c2p(0, 0), DOWN, 0.2), M("100", 24).next_to(ax.c2p(100, 0), DOWN, 0.2),
                      M("5", 24).next_to(ax.c2p(0, 5), LEFT, 0.2), M("10", 24).next_to(ax.c2p(0, 10), LEFT, 0.2)]
        self.base = VGroup(*parts)
        self.xlab = T("species on the island, S", 26).move_to(ax.c2p(50, 0) + DOWN * 0.8)

    def p(self, s, y):
        return self.ax.c2p(s, y)

    def blue(self, upto=None, w=7):
        def f():
            hi = 100.0 if upto is None else max(0.8, min(100.0, upto.get_value()))
            return self.ax.plot(lambda s: I_of(s, self.bt.get_value(), self.bd.get_value()), x_range=[0, hi, hi / 50.0],
                                color=BLUE, stroke_width=w, use_smoothing=False)
        return always_redraw(f)

    def red(self, upto=None, w=7):
        def f():
            top = smax(self.et.get_value(), self.bd.get_value())
            hi = top if upto is None else max(0.8, min(top, upto.get_value()))
            return self.ax.plot(lambda s: E_of(s, self.et.get_value(), self.bd.get_value()), x_range=[0, hi, hi / 50.0],
                                color=RED, stroke_width=w, use_smoothing=False)
        return always_redraw(f)

    def tracer(self, which, S, color):
        def f():
            s = max(0.0, min(100.0, S.get_value()))
            y = I_of(s, self.bt.get_value(), self.bd.get_value()) if which == "I" else E_of(s, self.et.get_value(), self.bd.get_value())
            return Dot(self.p(s, min(y, YMAX)), radius=0.15, color=color)
        return always_redraw(f)

    def xs(self):
        return crossing(self.bt.get_value(), self.et.get_value(), self.bd.get_value())

    def gold(self):
        dot = always_redraw(lambda: Dot(self.p(*self.xs()), radius=0.17, color=GOLD).set_z_index(5))
        drop = always_redraw(lambda: DashedLine(self.p(self.xs()[0], 0), self.p(*self.xs()), color=GOLD, stroke_width=4))
        lab = always_redraw(lambda: M("S*", 32, GOLD).next_to(self.p(*self.xs()), UP, 0.32))
        return dot, drop, lab

    def faint_blue(self, b, bend=0.0):
        c = self.ax.plot(lambda s: I_of(s, b, bend), x_range=[0, 100, 2], color=BLUE, stroke_width=5, use_smoothing=False)
        return DashedVMobject(c, num_dashes=40).set_stroke(opacity=0.45)

    def faint_red(self, e, bend=0.0):
        c = self.ax.plot(lambda s: E_of(s, e, bend), x_range=[0, smax(e, bend), 1], color=RED, stroke_width=5, use_smoothing=False)
        return DashedVMobject(c, num_dashes=40).set_stroke(opacity=0.45)


# ---------------------------------------------------------------------------------------------
# the world: sea, mainland, island
# ---------------------------------------------------------------------------------------------
def sea(x0, x1, y0, y1, n=14, seed=1):
    rng = random.Random(seed)
    rect = Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=0, fill_color=SEA, fill_opacity=0.14).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    rip = VGroup()
    for _ in range(n):
        a = Arc(radius=0.2, start_angle=PI * 1.2, angle=PI * 0.6, stroke_color=RIP, stroke_width=3, stroke_opacity=0.55)
        a.move_to([rng.uniform(x0 + 0.3, x1 - 0.3), rng.uniform(y0 + 0.3, y1 - 0.3), 0])
        a.v = rng.uniform(0.15, 0.3)

        def u(m, dt, x0=x0, x1=x1):
            m.shift(RIGHT * m.v * dt)
            if m.get_x() > x1 - 0.15:
                m.shift(LEFT * (x1 - x0 - 0.3))
        a.add_updater(u)
        rip.add(a)
    g = VGroup(rect, rip)
    g.rect, g.rip = rect, rip
    g.set_z_index(-5)
    return g


def tok(k, r, pos):
    return Circle(radius=r, stroke_color=PAL[(k // 10) % 10], stroke_width=2, fill_color=PAL[k % 10], fill_opacity=1).move_to(pos)


def sunflower(n, a, b, c):
    out = []
    for i in range(n):
        r = np.sqrt((i + 0.5) / n)
        th = i * 2.39996
        out.append(np.array([c[0] + a * r * np.cos(th), c[1] + b * r * np.sin(th), 0.0]))
    return out


class Mainland(VGroup):
    def __init__(self, cx, cy, w, h, cols, rows, r, tokens=True):
        super().__init__()
        self.body = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=LANDS, stroke_width=4,
                                     fill_color=LAND, fill_opacity=0.9).move_to([cx, cy, 0])
        dx = (w - 0.6) / (cols - 1) if cols > 1 else 0
        dy = (h - 0.6) / (rows - 1)
        self.tokens = VGroup(*[tok(k, r, [cx + ((k % cols) - (cols - 1) / 2) * dx, cy + ((rows - 1) / 2 - k // cols) * dy, 0]) for k in range(cols * rows)])
        self.add(self.body)
        if tokens:
            self.add(self.tokens)


class Isl(VGroup):
    def __init__(self, cx, cy, w, h, r, seed=3):
        super().__init__()
        self.body = Ellipse(width=w, height=h, stroke_color=LANDS, stroke_width=4, fill_color=LAND, fill_opacity=0.9).move_to([cx, cy, 0])
        pos = sunflower(100, w * 0.43, h * 0.43, [cx, cy])
        self.slots = VGroup(*[tok(k, r, pos[k]) for k in range(100)])
        self.slots.set_opacity(0)
        self.add(self.body, self.slots)
        self.present = set()
        self.alpha = [0.0] * 100
        self.lastop = [-1.0] * 100
        self.clock = 0.0
        self.blink_rate = 0.0
        self.blink_until = [0.0] * 100
        self.follow = None
        self.rng = random.Random(seed)
        self.add_updater(lambda m, dt: m._tick(dt))

    def set_now(self, present):
        self.present = set(present)
        self.alpha = [1.0 if k in self.present else 0.0 for k in range(100)]

    def _tick(self, dt):
        self.clock += dt
        if self.follow is not None:
            n = max(0, min(100, int(round(self.follow.get_value()))))
            self.present = set(ORDER[:n])
        for k in range(100):
            tgt = 1.0 if k in self.present else 0.0
            if self.blink_rate and tgt and self.rng.random() < self.blink_rate * dt:
                self.blink_until[k] = self.clock + 0.7
            if self.blink_until[k] > self.clock:
                tgt = 0.0
            a = self.alpha[k]
            a = min(tgt, a + 6 * dt) if tgt > a else max(tgt, a - 6 * dt)
            self.alpha[k] = a
            op = a * (0.88 + 0.12 * np.sin(self.clock * 2.2 + k * 0.9))
            if abs(op - self.lastop[k]) > 0.02:
                self.lastop[k] = op
                s = self.slots[k]
                s.set_fill(opacity=op)
                s.set_stroke(opacity=op)


def counter(isl, size=40, color=TEXT, gap=0.12):
    def f():
        sz = size.get_value() if hasattr(size, "get_value") else size
        return M(f"S = {len(isl.present)}", sz, color).next_to(isl.body, UP, gap)
    return always_redraw(f)


def swatches(isl, cx, y):
    sq = VGroup(*[Square(0.13, stroke_width=0, fill_opacity=0).move_to([cx + ((i % 28) - 13.5) * 0.15, y - (i // 28) * 0.2, 0]) for i in range(56)])

    def u(m):
        sp = sorted(isl.present)
        for i, s in enumerate(m):
            if i < len(sp):
                s.set_fill(PAL[sp[i] % 10], opacity=1)
            else:
                s.set_fill(opacity=0)
    sq.add_updater(u)
    return sq


# ---------------------------------------------------------------------------------------------
# scene base with flights
# ---------------------------------------------------------------------------------------------
def tide(sc):
    r = Rectangle(width=16, height=9, stroke_width=0, fill_color="#3A9AA8", fill_opacity=0.07).set_z_index(-20)
    r.t = 0.0

    def u(m, dt):
        m.t += dt
        m.set_fill(opacity=0.07 + 0.06 * np.sin(m.t * TAU / 3.0))
    r.add_updater(u)
    sc.add(r)


class FS(SpokenScene):
    def setup(self):
        super().setup()
        tide(self)

    def span(self, phrase, lead=0.2, nth=0, minimum=0.1):
        return max(minimum, self.t_of(phrase, nth) - lead - self.elapsed())

    def ring(self, pos, color=TEXT, r=0.1):
        ring = Circle(radius=r, stroke_color=color, stroke_width=3).move_to(pos)
        ring.age = 0.0

        def u(m, dt):
            m.age += dt
            m.scale(1 + 3.0 * dt)
            m.set_stroke(opacity=max(0.0, 1 - m.age / 0.5))
        ring.add_updater(u)
        self.add(ring)

    def fly(self, main, isl, k, run=0.8, frac=1.0, arc=-0.55, trail=True, new=True):
        src = main.tokens[k].get_center()
        dst = isl.slots[k].get_center()
        path = ArcBetweenPoints(src, dst, angle=arc)
        r = max(isl.slots[k].width / 2 * 1.15, 0.06)
        dot = Circle(radius=r, stroke_width=0, fill_color=PAL[k % 10], fill_opacity=1).move_to(src).set_z_index(3)
        tr = None
        if trail:
            tr = DashedVMobject(path.copy(), num_dashes=18).set_stroke(PAL[k % 10], 3, 0.7)
            self.add(tr)
        self.add(dot)

        def upd(m, a):
            m.move_to(path.point_from_proportion(min(1.0, a) * frac))
            m.set_opacity(1.0 - max(0.0, (a - 0.55) / 0.45) if frac < 1 else 1.0)
        self.play(UpdateFromAlphaFunc(dot, upd), run_time=run, rate_func=smooth)
        self.remove(dot)
        if tr is not None:
            self.remove(tr)
        if frac >= 1:
            if new:
                isl.present.add(k)
            self.ring(dst)

    def churn(self, main, isl, until, lo=46, hi=54, run=0.55, rng=None):
        rng = rng or random.Random(5)
        while self.elapsed() < until - run - 0.1:
            n = len(isl.present)
            if n >= hi:
                mode = "out"
            elif n <= lo:
                mode = "in"
            else:
                mode = rng.choice(["swap", "swap", "out", "in"])
            if mode in ("out", "swap"):
                kk = rng.choice(sorted(isl.present))
                isl.present.discard(kk)
                self.ring(isl.slots[kk].get_center(), RED, 0.08)
            if mode in ("in", "swap"):
                ks = [k for k in range(100) if k not in isl.present]
                self.fly(main, isl, rng.choice(ks), run=run, trail=False)
            else:
                self.wait(run)


# ---------------------------------------------------------------------------------------------
# panel stage: plot on the left, mainland strip and island on the right
# ---------------------------------------------------------------------------------------------
PX, PY = 4.5, 0.4     # island centre in the panel


class Stage:
    def __init__(self, sc, S=0, b=10.0, e=0.1, bend=0.0, dx=0.0, scale=1.0, blue=False, red=False, gold=False,
                 blab=False, rlab=False, add=True, ctr_size=40):
        self.sc = sc
        self.pl = Plot(b, e, bend)
        self.sea = sea(2.25, 6.8, -1.5, 2.3, 10, 4)
        self.main = Mainland(1.9, PY, 0.7, 3.8, 4, 25, 0.045)
        self.isl = Isl(PX + dx, PY, 3.3 * scale, 2.64 * scale, 0.08 * scale)
        self.isl.set_now(ORDER[:S])
        self.csize = ValueTracker(ctr_size)
        self.ctr = counter(self.isl, self.csize)
        self.mlab = T("mainland", 24).move_to([1.9, -1.85, 0])
        self.blab = T("I(S): new species arriving per day", 26, BLUE).move_to([-2.9, 3.3, 0])
        self.rlab = T("E(S): residents lost per day", 26, RED).move_to([-2.9, 2.8, 0])
        self.curves = VGroup()
        self.blue_c = self.red_c = None
        if blue:
            self.blue_c = self.pl.blue()
        if red:
            self.red_c = self.pl.red()
        self.gold_parts = self.pl.gold() if gold else None
        if add:
            sc.add(self.sea, self.pl.base, self.pl.xlab, self.main, self.isl, self.ctr, self.mlab)
            for c in (self.blue_c, self.red_c):
                if c is not None:
                    sc.add(c)
            if gold:
                sc.add(*self.gold_parts)
            if blab:
                sc.add(self.blab)
            if rlab:
                sc.add(self.rlab)

    def arcs(self):
        isl = self.isl
        self.aw, self.ao = ValueTracker(3.0), ValueTracker(0.8)

        def f():
            lx = isl.body.get_left()[0]
            g = VGroup()
            for y in (0.95, -0.05):
                g.add(DashedVMobject(ArcBetweenPoints([2.3, y, 0], [lx + 0.18, y, 0], angle=-0.45), num_dashes=max(8, int((lx - 2.3) * 6))))
            g.set_stroke(TEXT, self.aw.get_value(), self.ao.get_value())
            return g
        return always_redraw(f)


def pulse(sc, mob, color=TEXT, w=14, t=1.2):
    c = mob.copy().set_stroke(color, w)
    return ShowPassingFlash(c, time_width=0.6, run_time=t)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Island Biogeography"
    TITLE = "Two Rates, One Crossing"


# ---------------------------------------------------------------------------------------------
class S01Question(FS):
    def construct(self):
        sz = sea(-3.2, 6.8, -3.8, 3.8, 18, 2)
        main = Mainland(-4.9, 0, 3.4, 4.2, 10, 10, 0.1, tokens=False)
        mlab = T("mainland", 28).move_to([-4.9, -2.65, 0])
        islA = Isl(-0.9, 1.0, 3.6, 2.9, 0.12)
        islB = Isl(4.7, -1.0, 2.2, 1.6, 0.08)
        nA, nB = ValueTracker(0), ValueTracker(0)
        islA.follow, islB.follow = nA, nB
        cA = always_redraw(lambda: M(str(int(round(nA.get_value()))), 44).next_to(islA.body, UP, 0.12))
        cB = always_redraw(lambda: M(str(int(round(nB.get_value()))), 44).next_to(islB.body, UP, 0.12))
        sch = T("schematic", 24).move_to([4.9, -3.3, 0])
        self.add(sz)
        self.play(FadeIn(main), FadeIn(mlab), FadeIn(islA), FadeIn(islB), FadeIn(sch), run_time=1.2)
        self.at("hold more kinds")
        self.add(cA)
        self.play(nA.animate.set_value(30), run_time=1.6, rate_func=linear)
        self.at("small remote one")
        self.add(cB)
        self.play(nB.animate.set_value(8), run_time=0.9, rate_func=linear)
        self.at("One process can give both patterns")
        q = T("?", 110, TEXT, weight=BOLD).move_to([2.25, 0.45, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        q.add_updater(lambda m, dt: m.set_opacity(0.8 + 0.2 * np.sin(self.renderer.time * 5)))
        self.at("It is a balance between")
        q.clear_updaters()
        arrB = Arrow([3.3, 0.9, 0], [1.4, 0.9, 0], color=BLUE, buff=0, stroke_width=8)
        arrR = Arrow([1.4, -0.1, 0], [3.3, -0.1, 0], color=RED, buff=0, stroke_width=8)
        self.play(ReplacementTransform(q, VGroup(arrB, arrR)), run_time=1.2)
        self.at("two rates")
        lb = T("arrivals", 28, BLUE).next_to(arrB, UP, 0.12)
        lr = T("losses", 28, RED).next_to(arrR, DOWN, 0.12)
        self.play(FadeIn(lb), FadeIn(lr), run_time=0.7)
        self.play(Indicate(arrB, color=BLUE), Indicate(arrR, color=RED), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
def wide_world(sc, tokens=True, island_present=(), labels=True):
    sz = sea(-3.2, 6.8, -3.8, 3.8, 18, 2)
    main = Mainland(-4.9, 0, 3.4, 4.2, 10, 10, 0.1, tokens=tokens)
    isl = Isl(3.6, 0.0, 5.0, 4.0, 0.12)
    isl.set_now(island_present)
    ctr = counter(isl, 44)
    return sz, main, isl, ctr


def pool_label():
    return VGroup(T("species pool", 28), M("P = 100", 28)).arrange(DOWN, buff=0.1).move_to([-4.9, -2.85, 0])


class S02Pool(FS):
    def construct(self):
        sz, main, isl, ctr = wide_world(self, tokens=False)
        mlab = T("mainland", 28).move_to([-4.9, -2.7, 0])
        self.add(sz)
        self.play(FadeIn(main), run_time=0.9)
        self.at("mainland")
        self.play(FadeIn(mlab), run_time=0.6)
        self.at("It holds a pool of species")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in main.tokens], lag_ratio=0.03, run_time=self.span("island,", 0.3)))
        self.at("island,")
        self.play(FadeIn(isl), run_time=0.8)
        self.play(pulse(self, main.body, TEXT, 10, 1.0), run_time=1.0)
        self.at("pea species")
        pl = pool_label()
        self.play(ReplacementTransform(mlab, pl), run_time=0.7)
        self.at("The number living on the island")
        slab = T("S: species living on the island", 26).move_to([3.6, -2.95, 0])
        self.play(FadeIn(ctr), FadeIn(slab), run_time=0.8)
        self.at("S")
        self.play(Indicate(ctr, color=TEXT, scale_factor=1.3), run_time=0.9)
        self.at("species richness")
        self.play(Indicate(slab, color=TEXT, scale_factor=1.12), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Arrivals(FS):
    def construct(self):
        sz, main, isl, ctr = wide_world(self, tokens=True)
        pl = pool_label()
        self.add(sz, main, isl, ctr, pl)
        seq = ORDER[:15]
        # phase A: slow, one at a time (4 flights)
        self.wait(0.4)
        i = 0
        for _ in range(4):
            self.fly(main, isl, seq[i], run=1.5)
            i += 1
        self.at("so the count climbs fast", lead=0.0)
        # phase B: fast (8 flights)
        for _ in range(8):
            self.fly(main, isl, seq[i], run=0.3, trail=False)
            i += 1
        self.at("Immigration here means")
        cap = T("immigration = arrival of a NEW species", 30, BLUE).move_to([1.5, -3.4, 0])
        self.play(FadeIn(cap), run_time=0.6)
        left = 3
        slot = max(0.8, (self.narration_s - self.elapsed() - 0.2) / left)
        for _ in range(left):
            self.fly(main, isl, seq[i], run=slot - 0.1)
            i += 1
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Slowing(FS):
    def construct(self):
        sz, main, isl, ctr = wide_world(self, tokens=True, island_present=ORDER[:15])
        pl = pool_label()
        self.add(sz, main, isl, ctr, pl)
        rng = random.Random(21)
        n = 15
        # phase 1: still filling quickly
        for _ in range(6):
            self.fly(main, isl, ORDER[n], run=0.28, trail=False)
            n += 1
        self.at("more arrivals belong to species already there")
        lab = T("species already here: no new species", 28, TEXT).move_to([1.5, -3.4, 0])
        newleft = 3
        plan = ["r", "r", "n", "r", "r", "r", "n", "r", "r", "n", "r", "r"]
        for kind in plan:
            if self.elapsed() > self.t_of("So new arrivals slow") - 0.9:
                break
            if kind == "n":
                self.fly(main, isl, ORDER[n], run=0.8, trail=False)
                n += 1
            else:
                kk = rng.choice(sorted(isl.present))
                self.fly(main, isl, kk, run=0.8, new=False, trail=False)
            if lab.get_opacity() == 0 or lab not in self.mobjects:
                if self.elapsed() > self.t_of("already there") - 0.2:
                    self.play(FadeIn(lab), run_time=0.4)
        if lab not in self.mobjects:
            self.add(lab)
        self.at("changes nothing in the count", lead=-1.0 if False else 0.2)
        self.play(Indicate(ctr, color=TEXT, scale_factor=1.25), run_time=0.9)
        # slow phase: mostly repeats
        until = self.t_of("So new arrivals slow") - 0.2
        while self.elapsed() < until - 1.0:
            kk = rng.choice(sorted(isl.present))
            self.fly(main, isl, kk, run=0.8, new=False, trail=False)
        self.at("So new arrivals slow")
        until = self.t_of("all pea species live there") - 0.3
        while self.elapsed() < until - 0.9:
            kk = rng.choice(sorted(isl.present))
            self.fly(main, isl, kk, run=0.8, new=False, trail=False)
        self.at("stop when all")
        S = ValueTracker(n)
        isl.follow = S
        self.play(S.animate.set_value(100), run_time=max(0.8, self.span("species live there", 0.0)), rate_func=linear)
        isl.follow = None
        fin = T("S = P: no new species left", 28, TEXT).move_to([1.5, -3.4, 0])
        self.play(ReplacementTransform(lab, fin), run_time=0.6)
        for _ in range(2):
            if self.elapsed() + 0.9 < self.narration_s:
                self.fly(main, isl, rng.randrange(100), run=0.7, new=False, trail=False)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Blue(FS):
    def construct(self):
        sz, main, isl, ctr = wide_world(self, tokens=True, island_present=range(100))
        pl = pool_label()
        fin = T("S = P: no new species left", 28, TEXT).move_to([1.5, -3.4, 0])
        self.add(sz.rect, sz.rip, main, isl, ctr, pl, fin)
        st = Stage(self, S=100, add=False)
        st.isl.slots.set_opacity(1)
        ST = ValueTracker(100)
        self.wait(0.3)
        self.play(FadeOut(pl), FadeOut(fin), FadeOut(ctr),
                  ReplacementTransform(main, st.main), ReplacementTransform(isl, st.isl),
                  ReplacementTransform(sz.rect, st.sea.rect), FadeOut(sz.rip), FadeIn(st.sea.rip),
                  run_time=2.0)
        self.add(st.ctr)
        self.play(FadeIn(st.mlab), run_time=0.4)
        self.at("against the number of species")
        self.play(Create(st.pl.ax), run_time=0.8)
        self.play(FadeIn(st.pl.base[1:]), FadeIn(st.pl.xlab), run_time=0.6)
        self.at("island.")
        st.isl.follow = ST
        self.play(ST.animate.set_value(0), run_time=max(0.6, self.span("The blue line", 0.0) - 0.1), rate_func=linear)
        self.at("The blue line")
        self.play(FadeIn(st.blab), run_time=0.5)
        tr = st.pl.blue(upto=ST)
        dt = st.pl.tracer("I", ST, BLUE)
        self.add(tr, dt)
        end = self.t_of("reaches P") if False else self.t_of("p.") + 0.35
        self.play(ST.animate.set_value(100), run_time=max(1.0, end - self.elapsed()), rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Losses(FS):
    def construct(self):
        st = Stage(self, S=100, blue=True, blab=True)
        isl = st.isl
        rng = random.Random(8)

        def lose():
            kk = rng.choice(sorted(isl.present))
            isl.present.discard(kk)
            self.ring(isl.slots[kk].get_center(), RED, 0.08)

        self.at("disappear", lead=1.2)
        for _ in range(3):
            lose()
            self.wait(0.7)
        self.at("local extinction")
        for _ in range(1):
            lose()
            self.wait(0.6)
        self.at("a loss from this island only")
        lost = VGroup(T("lost from", 28, RED), T("this island only", 28, RED)).arrange(DOWN, buff=0.1).move_to([PX, -2.35, 0])
        self.play(FadeIn(lost), pulse(self, st.main.body, TEXT, 10, 1.2), run_time=1.2)
        lose()
        self.wait(0.8)
        lose()
        self.at("Suppose each resident has the same")
        self.play(LaggedStart(*[Flash(isl.slots[k].get_center(), color=TEXT, flash_radius=0.22, line_length=0.08, num_lines=8) for k in sorted(isl.present)[:40]],
                              lag_ratio=0.08, run_time=max(2.0, self.span("Then more residents mean", 0.7))))
        self.at("Then more residents mean more losses")
        ST = ValueTracker(len(isl.present))
        isl.follow = ST
        self.play(ST.animate.set_value(3), FadeOut(lost), run_time=0.7)
        isl.blink_rate = 0.03
        self.play(FadeIn(st.rlab), run_time=0.4)
        tr = st.pl.red(upto=ST)
        dt = st.pl.tracer("E", ST, RED)
        self.add(tr, dt)
        self.play(ST.animate.set_value(100), run_time=max(1.5, self.narration_s - self.elapsed() - 0.5), rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Cross(FS):
    def construct(self):
        st = Stage(self, S=100, blue=True, red=True, blab=True, rlab=True)
        pl, isl = st.pl, st.isl
        self.wait(0.2)
        self.play(pulse(self, st.blue_c, WHITE, 12, 1.0), run_time=1.0)
        self.play(pulse(self, st.red_c, WHITE, 12, 1.0), run_time=1.0)
        self.at("new arrivals equal losses")
        dot, drop, lab = pl.gold()
        self.play(GrowFromCenter(dot), run_time=0.7)
        self.play(Create(drop), run_time=0.9)
        self.at("That richness is")
        ST = ValueTracker(100)
        isl.follow = ST
        self.play(FadeIn(lab), ST.animate.set_value(50), run_time=1.6)
        self.at("S")
        self.play(Indicate(dot, color=GOLD, scale_factor=1.8), run_time=1.0)
        # on-axis marker
        marker = always_redraw(lambda: Triangle(color=GOLD, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI).move_to(pl.p(ST.get_value(), 0) + UP * 0.2))
        self.at("Below it")
        self.play(FadeOut(pl.xlab), run_time=0.3)
        arrL = Arrow(pl.p(6, 0) + DOWN * 0.5, pl.p(40, 0) + DOWN * 0.5, color=BLUE, buff=0, stroke_width=8)
        labL = VGroup(T("arrivals > losses", 28), T("S rises", 28)).arrange(DOWN, buff=0.05).move_to(pl.p(23, 0) + DOWN * 1.15)
        self.add(marker)
        self.play(ST.animate.set_value(20), FadeIn(arrL), FadeIn(labL), run_time=0.8)
        self.play(ST.animate.set_value(50), run_time=max(1.2, self.span("Above it", 0.3)), rate_func=smooth)
        self.at("Above it")
        arrR = Arrow(pl.p(94, 0) + DOWN * 0.5, pl.p(60, 0) + DOWN * 0.5, color=RED, buff=0, stroke_width=8)
        labR = VGroup(T("losses > arrivals", 28), T("S falls", 28)).arrange(DOWN, buff=0.05).move_to(pl.p(77, 0) + DOWN * 1.15)
        self.play(ST.animate.set_value(85), FadeIn(arrR), FadeIn(labR), run_time=0.8)
        self.play(ST.animate.set_value(50), run_time=max(1.2, self.narration_s - self.elapsed() - 0.4), rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Turnover(FS):
    def construct(self):
        st = Stage(self, S=50, blue=True, red=True, gold=True, blab=True, rlab=True)
        pl, isl, main = st.pl, st.isl, st.main
        sch = VGroup(T("chance version,", 24), T("schematic", 24)).arrange(DOWN, buff=0.05).move_to([PX + 0.4, -2.0, 0])
        self.add(sch)
        until = self.t_of("The count settles") - 0.4
        rng = random.Random(5)
        t_turn = self.t_of("That shared rate")
        self.churn(main, isl, t_turn - 0.2, rng=rng)
        self.at("That shared rate")
        hl = always_redraw(lambda: DashedLine(pl.p(*pl.xs()), pl.p(0, pl.xs()[1]), color=GOLD, stroke_width=4))
        tl = T("turnover = I(S*) = E(S*)", 28, GOLD).move_to([-2.9, 3.3, 0])
        self.play(FadeOut(st.blab), FadeOut(st.rlab), Create(hl), FadeIn(tl), run_time=1.0)
        self.churn(main, isl, self.t_of("The count settles") - 0.3, rng=rng)
        self.at("The count settles")
        sw = swatches(isl, PX, -2.75)
        swl = T("species present", 26).move_to([PX, -3.4, 0])
        self.play(FadeIn(sw), FadeIn(swl), run_time=0.7)
        self.churn(main, isl, self.narration_s - 0.2, rng=rng)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09Predict(FS):
    def construct(self):
        st = Stage(self, S=50, blue=True, red=True, gold=True, blab=True, rlab=True)
        pl, isl = st.pl, st.isl
        arcs = st.arcs()
        self.add(arcs)
        self.at("push the island farther", lead=0.0)
        self.play(isl.animate.shift(RIGHT * 0.6), run_time=2.2)
        self.at("keeping its size the same")
        self.play(pulse(self, isl.body, LANDS, 10, 1.0), run_time=1.2)
        self.at("Which line moves")
        self.play(pulse(self, st.blue_c, WHITE, 14, 1.0), run_time=1.0)
        self.play(pulse(self, st.red_c, WHITE, 14, 1.0), run_time=1.0)
        self.at("which way does the gold point go")
        q = T("?", 90, GOLD, weight=BOLD).move_to(pl.p(50, 8.6))
        self.play(FadeIn(q, scale=0.5), Indicate(st.gold_parts[0], color=GOLD, scale_factor=1.8), run_time=1.0)
        q.add_updater(lambda m, dt: m.set_opacity(0.75 + 0.25 * np.sin(self.renderer.time * 5)))
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        tide(self)
        # same picture as the end of the previous scene, held, with a timer ring
        st = Stage(self, S=50, dx=0.6, blue=True, red=True, gold=True, blab=True, rlab=True)
        arcs = st.arcs()
        q = T("?", 90, GOLD, weight=BOLD).move_to(st.pl.p(50, 8.6))
        self.add(arcs, q)
        T_ = ValueTracker(0)
        ring0 = Circle(radius=0.32, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.4).move_to([6.3, 3.2, 0])
        ring = always_redraw(lambda: Arc(radius=0.32, start_angle=PI / 2, angle=-TAU * max(0.001, T_.get_value()), stroke_color=GOLD, stroke_width=8).move_to([6.3, 3.2, 0]).shift(
            np.array([0, 0, 0])))
        self.add(ring0, ring)
        q.add_updater(lambda m, dt: m.set_opacity(0.75 + 0.25 * np.sin(self.renderer.time * 5)))
        self.play(T_.animate.set_value(1.0), run_time=4.8, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11Far(FS):
    def construct(self):
        st = Stage(self, S=50, dx=0.6, blue=True, red=True, gold=True, blab=True, rlab=True)
        pl, isl, main = st.pl, st.isl, st.main
        arcs = st.arcs()
        self.add(arcs)
        rng = random.Random(4)
        t1 = self.t_of("So the blue line drops")
        pres = sorted(isl.present)
        # fewer arrivals reach the distant island: most fade on the way
        n = 0
        plan = [0.55, 0.5, 1.0, 0.6]
        slot = (t1 - 0.3 - self.elapsed()) / len(plan)
        for fr in plan:
            self.fly(main, isl, pres[n * 3], run=slot - 0.1, frac=fr, new=False, trail=True)
            n += 1
        self.play(st.aw.animate.set_value(1.5), st.ao.animate.set_value(0.45), run_time=0.8)
        self.at("So the blue line drops")
        fb = pl.faint_blue(10.0)
        self.add(fb)
        ST = ValueTracker(50)
        isl.follow = ST
        self.play(pl.bt.animate.set_value(5.0), run_time=2.4, rate_func=smooth)
        far = T("farther: S* 50 to 33", 28, GOLD).move_to([PX, -2.4, 0])
        self.play(FadeIn(far), ST.animate.set_value(33.3), run_time=max(1.5, self.span("The far island holds", 0.0)), rate_func=smooth)
        self.at("The far island holds")
        self.play(Indicate(st.ctr, color=TEXT, scale_factor=1.25), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12Small(FS):
    def construct(self):
        st = Stage(self, S=33, dx=0.6, b=5.0, blue=True, red=True, gold=True, blab=True, rlab=True)
        pl, isl, main = st.pl, st.isl, st.main
        fb = pl.faint_blue(10.0)
        self.add(fb)
        ST = ValueTracker(33)
        isl.follow = ST
        # reset to the original distance
        self.play(pl.bt.animate.set_value(10.0), ApplyMethod(isl.shift, LEFT * 0.6, suspend_mobject_updating=False), ST.animate.set_value(50), FadeOut(fb), run_time=1.6)
        self.at("shrink the island instead", lead=0.5)
        self.play(ApplyMethod(isl.scale, 0.62, suspend_mobject_updating=False), run_time=2.0)
        self.at("A small island loses residents faster")
        isl.blink_rate = 0.05
        fr = pl.faint_red(0.1)
        self.wait(max(0.1, self.span("The red line rises", 1.0)))
        self.add(fr)
        self.play(pl.et.animate.set_value(0.2), run_time=2.0, rate_func=smooth)
        self.at("S star moves left", lead=0.5)
        sm = T("smaller: S* 50 to 33", 28, GOLD).move_to([PX, -2.4, 0])
        self.play(FadeIn(sm), ST.animate.set_value(33.3), run_time=max(1.2, self.narration_s - self.elapsed() - 0.5), rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13Both(FS):
    def column(self, cx, b, e, ni, w, h, r, label, blink):
        pl = Plot(b, e, 0.0, center=(cx, -1.5), xl=4.6, yl=2.6, ticks=False)
        isl = Isl(cx, 1.9, w, h, r)
        sx, sy = crossing(b, e)
        isl.set_now(ORDER[:int(round(sx))])
        isl.blink_rate = blink
        bl, rd = pl.blue(w=6), pl.red(w=6)
        dot = Dot(pl.p(sx, sy), radius=0.15, color=GOLD).set_z_index(5)
        drop = DashedLine(pl.p(sx, 0), pl.p(sx, sy), color=GOLD, stroke_width=4)
        ctr = counter(isl, 40)
        lab = T(label, 30, GOLD).move_to([cx, 0.4, 0])
        return pl, isl, bl, rd, dot, drop, ctr, lab

    def construct(self):
        L = self.column(-3.4, 10.0, 0.1, 50, 3.2, 1.9, 0.085, "high S*", 0.03)
        R = self.column(3.4, 5.0, 0.2, 20, 1.6, 1.0, 0.055, "low S*", 0.03)
        divider = Line([0, -3.3, 0], [0, 3.5, 0], color=TEXT, stroke_width=2, stroke_opacity=0.3)
        self.add(divider)
        pl, isl, bl, rd, dot, drop, ctr, lab = L
        self.add(pl.ax, isl, ctr)
        self.wait(0.3)
        self.play(Create(bl), Create(rd), run_time=1.0)
        self.play(GrowFromCenter(dot), Create(drop), FadeIn(lab), run_time=0.7)
        self.play(pulse(self, isl.body, LANDS, 10, 1.0), run_time=0.6)
        self.at("far, small ones the fewest")
        pl, isl, bl, rd, dot, drop, ctr, lab = R
        self.add(pl.ax, isl, ctr)
        self.play(Create(bl), Create(rd), run_time=1.4)
        self.play(GrowFromCenter(dot), Create(drop), FadeIn(lab), run_time=0.9)
        self.play(pulse(self, isl.body, LANDS, 10, 1.0), run_time=0.8)
        self.at("One balance of two rates")
        self.play(Indicate(L[4], color=GOLD, scale_factor=1.8), Indicate(R[4], color=GOLD, scale_factor=1.8), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14Scope(FS):
    def construct(self):
        st = Stage(self, S=50, blue=True, red=True, gold=True, blab=True, rlab=True, ctr_size=40)
        pl, isl = st.pl, st.isl
        isl.blink_rate = 0.06
        self.wait(0.3)
        self.play(pulse(self, st.blue_c, WHITE, 12, 1.0), pulse(self, st.red_c, WHITE, 12, 1.0), run_time=1.0)
        self.at("This is a model")
        self.play(Indicate(st.ctr, color=TEXT, scale_factor=1.15), run_time=1.0)
        self.at("It leaves out new species forming")
        ni = VGroup(T("not included: new species", 26), T("forming on the island", 26)).arrange(DOWN, buff=0.08).move_to([PX, -2.55, 0])
        self.play(FadeIn(ni), run_time=0.8)
        self.at("Real curves need not be straight")
        rc = VGroup(T("real curves: not necessarily", 26), T("straight (schematic)", 26)).arrange(DOWN, buff=0.08).move_to([PX, -2.55, 0])
        self.play(FadeOut(ni), pl.bd.animate.set_value(1.0), run_time=1.1, rate_func=smooth)
        self.play(FadeIn(rc), run_time=1.1)
        self.at("because species differ")
        self.play(Indicate(st.blue_c, color=BLUE, scale_factor=1.03), run_time=1.2)
        self.at("And it predicts how many species")
        sw = swatches(isl, PX, -2.5)
        swl = VGroup(T("which species:", 26), T("not predicted", 26)).arrange(DOWN, buff=0.06).move_to([PX, -3.3, 0])
        self.play(FadeOut(rc), FadeIn(sw), st.csize.animate.set_value(60), run_time=1.0)
        self.at("not which ones")
        self.play(FadeIn(swl), run_time=0.8)
        self.finish()


class S15End(EndCard):
    LINE = "Species count settles where new arrivals equal local losses."
