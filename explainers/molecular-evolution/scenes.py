"""Molecular evolution: why genes keep time  (Biochemistrypedia explainer, level-up film)

COLOR MAP (one colour per concept, whole film)
  GOLD   = a DNA change: a new mutation, a substitution tick, a changed site
  BLUE   = species A: its branch, its dots, its population
  GREEN  = species B: its branch and tips
  GREY   = the common ancestor and unchanged sites
  FOSSIL = a brown stone icon (a fossil)
  RED    = a mutation removed by selection
Every number is on-screen text; dots, trees and boxes are schematic cartoons. No molecular structures.
"""
import math
import os
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

FOSSIL = "#B08457"
FOSSIL_DK = "#6E4E2E"

# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def add_motes(sc, n=34):
    """Faint drifting motes: a held frame is never a dead frame (pipeline 'ambient' idea, always on here)."""
    rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
    W, H = config.frame_width, config.frame_height
    motes = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.05, 0.1), color=rng.choice([TEAL, TEXT, GOLD])).set_opacity(rng.uniform(0.12, 0.26))
        d.move_to([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0])
        d.tg = d.get_center().copy()
        d.clock = rng.uniform(0, 2.0)

        def drift(m, dt, W=W, H=H, rng=rng):
            m.clock -= dt
            if m.clock <= 0:
                m.clock = rng.uniform(1.2, 2.4)
                m.tg = np.array([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0.0])
            c = m.get_center()
            m.move_to(c + (m.tg - c) * min(1.0, dt * 0.9))
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-10)
    sc.add(motes)


class Scn(SpokenScene):
    def setup(self):
        super().setup()
        add_motes(self)


class Jostle(VGroup):
    """A circle of dots that are replaced by new positions every period (a population, schematic)."""

    def __init__(self, center, radius, n, color=GREY, dot_r=0.1, period=1.0, seed=3, fill=0.2, stroke=5):
        super().__init__()
        self.ring = Circle(radius=radius, color=color, stroke_width=stroke, fill_color=color, fill_opacity=fill).move_to(center)
        self.dots = [Dot(radius=dot_r, color=color) for _ in range(n)]
        self.n, self.period, self.seed, self.t, self.g = n, period, seed, 0.0, 0
        self.units = self._units(0)
        for d, u in zip(self.dots, self.units):
            d.move_to(self.ring.get_center() + u * radius)
        self.add(self.ring, *self.dots)
        self.add_updater(lambda m, dt: m._upd(dt))

    def _units(self, g):
        rng = random.Random(self.seed * 100 + g)
        out = []
        while len(out) < self.n:
            p = np.array([rng.uniform(-1, 1), rng.uniform(-1, 1), 0.0])
            if np.linalg.norm(p) < 0.85 and all(np.linalg.norm(p - q) > 0.26 for q in out):
                out.append(p)
        return out

    def _upd(self, dt):
        self.t += dt
        g = int(self.t / self.period)
        if g != self.g:
            self.g = g
            self.units = self._units(g)
        c, r = self.ring.get_center(), self.ring.width / 2
        a = min(1.0, dt * 6)
        for d, u in zip(self.dots, self.units):
            p = d.get_center()
            d.move_to(p + (c + u * r - p) * a)



def wait_until(sc, t):
    r = t - sc.elapsed()
    if r > 0.02:
        sc.wait(r)


def run_events(sc, events):
    """events: [(seconds, fn)] run in time order; each fn may call sc.play."""
    for t, fn in sorted(events, key=lambda e: e[0]):
        wait_until(sc, t)
        fn()


def wobble(m, amp=0.06, sp=1.0, ph=0.0):
    m._o = m.get_center().copy()
    m._tw = ph

    def f(mm, dt):
        mm._tw += dt * sp
        mm.move_to(mm._o + np.array([math.sin(mm._tw * 2.1) * amp, math.cos(mm._tw * 1.7) * amp, 0]))
    m.add_updater(f)
    return m


def animal(kind, color):
    body = Ellipse(width=2.0, height=1.2, stroke_width=0, fill_color=color, fill_opacity=0.95)
    head = Circle(radius=0.5, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([0.95, 0.55, 0])
    eye = Dot([1.12, 0.65, 0], radius=0.07, color=BG)
    legs = VGroup(*[Line([x, -0.45, 0], [x, -0.95, 0], color=color, stroke_width=9) for x in (-0.6, -0.2, 0.3, 0.7)])
    if kind == "A":
        ears = VGroup(Ellipse(width=0.22, height=0.85, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([0.8, 1.2, 0]).rotate(0.15),
                      Ellipse(width=0.22, height=0.85, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([1.1, 1.2, 0]).rotate(-0.2))
        tail = Circle(radius=0.2, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([-1.05, 0.2, 0])
    else:
        ears = VGroup(Circle(radius=0.17, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([0.7, 1.0, 0]),
                      Circle(radius=0.17, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([1.2, 1.0, 0]))
        tail = Line([-1.0, 0.3, 0], [-1.7, 0.9, 0], color=color, stroke_width=9)
    g = VGroup(legs, tail, body, head, ears, eye)
    return g.scale(1.25)


def gene_bar(n=12, side=0.42, gap=0.05):
    sq = VGroup(*[Square(side, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.28) for _ in range(n)])
    sq.arrange(RIGHT, buff=gap)
    return sq


def light(sq):
    sq.set_fill(GOLD, 0.95).set_stroke(GOLD, 3)


def fossil_stone(r=0.42):
    st = Ellipse(width=2 * r, height=1.65 * r, stroke_color=FOSSIL_DK, stroke_width=3, fill_color=FOSSIL, fill_opacity=1)
    sp = VGroup(*[Arc(radius=r * k, start_angle=0.3, angle=4.2, stroke_color=FOSSIL_DK, stroke_width=3) for k in (0.25, 0.5)])
    return VGroup(st, sp.move_to(st))


# ---- the big tree (s02 - s04, s14): one world, rebuilt in the same place ----
FORK = np.array([-2.1, -1.5, 0.0])
TIP_L = np.array([-4.8, 2.7, 0.0])
TIP_R = np.array([0.6, 2.7, 0.0])
ROOT_C = np.array([-2.1, -3.0, 0.0])


def _tip(side):
    return TIP_L if side < 0 else TIP_R


def bpt(side, f):
    return FORK + (_tip(side) - FORK) * f


def tick_mark(side, f, L=0.4, w=10):
    p = bpt(side, f)
    d = _tip(side) - FORK
    d = d / np.linalg.norm(d)
    perp = np.array([-d[1], d[0], 0.0])
    return Line(p - perp * L, p + perp * L, color=GOLD, stroke_width=w)


def root_ring():
    return Jostle(ROOT_C, 0.62, 7, GREY, 0.07, 1.0, 11, 0.25, 5)


def make_tree(bt=(), gt=(), root=True):
    parts = {}
    parts["root"] = root_ring() if root else VGroup()
    parts["stem"] = Line(ROOT_C + UP * 0.62, FORK, color=GREY, stroke_width=12)
    parts["bl"] = Line(FORK, TIP_L, color=BLUE, stroke_width=12)
    parts["gr"] = Line(FORK, TIP_R, color=GREEN, stroke_width=12)
    parts["node"] = Dot(FORK, radius=0.24, color=GREY)
    parts["tl"] = Dot(TIP_L, radius=0.24, color=BLUE)
    parts["tr"] = Dot(TIP_R, radius=0.24, color=GREEN)
    bticks = [tick_mark(-1, f) for f in bt]
    gticks = [tick_mark(1, f) for f in gt]
    g = VGroup(parts["root"], parts["stem"], parts["bl"], parts["gr"], parts["node"], parts["tl"], parts["tr"], *bticks, *gticks)
    g.p = parts
    g.bticks, g.gticks = bticks, gticks
    return g


def mini_tree(cx, base_y, h, w, n_ticks, fork_frac=0.3):
    """A small Y tree for the rate/time scenes. Returns (group, parts) with ticks separate."""
    fork = np.array([cx, base_y + fork_frac * h, 0.0])
    tl = np.array([cx - w, base_y + h, 0.0])
    tr = np.array([cx + w, base_y + h, 0.0])
    stem = Line([cx, base_y, 0], fork, color=GREY, stroke_width=11)
    bl = Line(fork, tl, color=BLUE, stroke_width=11)
    gr = Line(fork, tr, color=GREEN, stroke_width=11)
    node = Dot(fork, radius=0.22, color=GREY)
    dl, dr = Dot(tl, radius=0.22, color=BLUE), Dot(tr, radius=0.22, color=GREEN)
    ticks = []
    for tip, side in ((tl, -1), (tr, 1)):
        d = tip - fork
        d = d / np.linalg.norm(d)
        perp = np.array([-d[1], d[0], 0.0])
        for i in range(n_ticks):
            f = (i + 0.6) / (n_ticks + 0.2)
            p = fork + (tip - fork) * f
            ticks.append(Line(p - perp * 0.32, p + perp * 0.32, color=GOLD, stroke_width=9))
    body = VGroup(stem, bl, gr, node, dl, dr)
    body.fork, body.tl, body.tr = fork, tl, tr
    return body, VGroup(*ticks)


# ---- populations: dots that are replaced by offspring every generation ----
class Pop(VGroup):
    def __init__(self, box, n, seed, period=1.0, gold_fn=None, offset=0.0, on_fix=None, animate=True, static_gold=0, color=BLUE):
        super().__init__()
        x0, x1, y0, y1 = box
        self.box, self.n, self.seed, self.period = box, n, seed, period
        self.gold_fn, self.offset, self.on_fix, self.color = gold_fn, offset, on_fix, color
        self.rect = RoundedRectangle(corner_radius=0.2, width=x1 - x0, height=y1 - y0, stroke_color=color, stroke_width=6,
                                     fill_color=color, fill_opacity=0.22).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        w, h = x1 - x0 - 0.7, y1 - y0 - 0.7
        cols = max(1, math.ceil(math.sqrt(n * w / h)))
        rows = math.ceil(n / cols)
        self.cells = [np.array([x0 + 0.35 + w * (c + 0.5) / cols, y0 + 0.35 + h * (r + 0.5) / rows, 0.0])
                      for r in range(rows) for c in range(cols)]
        self.cell = (w / cols, h / rows)
        self.dots = [Dot(radius=0.16, color=color) for _ in range(n)]
        self.gold = [False] * n
        self.t = 0.0
        self.g = 0
        self.targets = [None] * n
        self._place(0)
        for d, tg in zip(self.dots, self.targets):
            d.move_to(tg)
        self.add(self.rect, *self.dots)
        if static_gold:
            rng = random.Random(self.seed + 7)
            for i in rng.sample(range(n), min(static_gold, n)):
                self._set_gold(i, True)
        if animate:
            self.add_updater(lambda m, dt: m._upd(dt))

    def _set_gold(self, i, want):
        d = self.dots[i]
        if want and not self.gold[i]:
            d.set_color(GOLD)
            d.scale(1.45)
        elif not want and self.gold[i]:
            d.set_color(self.color)
            d.scale(1 / 1.45)
        self.gold[i] = want

    def _place(self, g):
        rng = random.Random(self.seed * 1000 + g)
        cells = self.cells[:]
        rng.shuffle(cells)
        cw, ch = self.cell
        for i in range(self.n):
            self.targets[i] = cells[i] + np.array([rng.uniform(-0.28, 0.28) * cw, rng.uniform(-0.28, 0.28) * ch, 0.0])
        return rng

    def restart(self):
        self.t, self.g = 0.0, 0

    def _upd(self, dt):
        self.t += dt
        g = int(self.t / self.period)
        if g != self.g:
            self.g = g
            rng = self._place(g)
            k = int(self.gold_fn(self.offset + self.t)) if self.gold_fn else 0
            gs = set(rng.sample(range(self.n), min(k, self.n)))
            for i in range(self.n):
                self._set_gold(i, i in gs)
            if self.gold_fn and k >= self.n and self.on_fix:
                self.on_fix(self)
        a = min(1.0, dt * 7)
        for d, tg in zip(self.dots, self.targets):
            c = d.get_center()
            d.move_to(c + (tg - c) * a)


class GenCounter(VGroup):
    def __init__(self, pop, center, base=0):
        super().__init__()
        self.pop, self.base, self.center, self.last = pop, base, np.array(center, dtype=float), None
        cap = T("generation", 30)
        self.cap = cap.move_to(self.center + UP * 0.5)
        self.num = M(str(base), 56, GOLD).move_to(self.center + DOWN * 0.25)
        self.add(self.cap, self.num)
        self.add_updater(lambda m, dt: m._upd())

    def _upd(self):
        g = self.pop.g + self.base
        if g != self.last:
            self.last = g
            self.num.become(M(str(g), 56, GOLD).move_to(self.center + DOWN * 0.25))


class Track(VGroup):
    """A timeline with a moving cursor; fire() lands a gold substitution tick at the cursor."""

    def __init__(self, x0, x1, y, tspan, t0=0.0, pre=(), cursor=True):
        super().__init__()
        self.x0, self.x1, self.y, self.tspan, self.t = x0, x1, y, tspan, t0
        self.line = Line([x0, y, 0], [x1, y, 0], color=TEXT, stroke_width=6).set_opacity(0.85)
        self.cursor = Line([x0, y - 0.35, 0], [x0, y + 0.35, 0], color=TEXT, stroke_width=5)
        self.add(self.line)
        self.count = 0
        for tt in pre:
            self._tick(tt, pulse=False)
        if cursor:
            self.add(self.cursor)
            self.add_updater(lambda m, dt: m._upd(dt))
            self.cursor.move_to([self._x(t0), y, 0])

    def _x(self, t):
        return self.x0 + (self.x1 - self.x0) * min(max(t / self.tspan, 0.0), 1.0)

    def _upd(self, dt):
        self.t += dt
        self.cursor.move_to([self._x(self.t), self.y, 0])

    def _tick(self, t, pulse=True):
        x = self._x(t)
        tk = Line([x, self.y - 0.35, 0], [x, self.y + 0.35, 0], color=GOLD, stroke_width=10)
        tk.p = 1.0 if pulse else 0.0

        def f(m, dt):
            m.p = max(0.0, m.p - dt * 1.8)
            m.set_stroke(width=10 + 14 * m.p)
        tk.add_updater(f)
        self.add(tk)
        self.count += 1

    def fire(self):
        self._tick(self.t)


class Sched(Mobject):
    """Invisible clock that calls fns at scene times (for scripted ticks)."""

    def __init__(self, events, t0=0.0):
        super().__init__()
        self.ev = sorted(events, key=lambda e: e[0])
        self.t = t0
        self.add_updater(lambda m, dt: m._upd(dt))

    def _upd(self, dt):
        self.t += dt
        while self.ev and self.ev[0][0] <= self.t:
            self.ev.pop(0)[1]()


# box geometry shared by s05 - s09
SM = (-5.7, -2.3, -2.4, 0.4)
LG = (0.6, 6.6, -2.4, 2.0)
GAP = (-0.85, -0.75, 0.0)
SM_LABEL = np.array([-4.0, 0.8, 0.0])
LG_LABEL = np.array([3.6, 2.45, 0.0])
S08_LEN = 18.125   # s08 narration + tail
S09_LEN = 13.775
TSPAN = S08_LEN + S09_LEN


def blue_circle():
    return Jostle([0, 0, 0], 3.3, 16, BLUE, 0.2, 1.0, 4, 0.2, 6)


def pops_pair(seed=1, period=1.0, small_fn=None, large_fn=None, offset=0.0, on_fix=(None, None), animate=True, sg=(0, 0), nl=24):
    small = Pop(SM, 6, seed, period, small_fn, offset, on_fix[0], animate, sg[0])
    large = Pop(LG, nl, seed + 1, period, large_fn, offset, on_fix[1], animate, sg[1])
    return small, large


# =============================================================================================
# s00 title
# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Molecular evolution"
    TITLE = "Why Genes Keep Time"


# =============================================================================================
# s01 question
# =============================================================================================
class S01Question(Scn):
    def construct(self):
        a = animal("A", BLUE).scale(1.2).move_to([-4.0, 1.7, 0])
        b = animal("B", GREEN).scale(1.2).flip(UP).move_to([4.0, 1.7, 0])
        wobble(a, 0.08, 1.1)
        wobble(b, 0.08, 0.9, 1.0)
        self.play(FadeIn(a, shift=UP * 0.3), FadeIn(b, shift=UP * 0.3), run_time=1.0)
        q = T("?", 230, TEXT, weight=BOLD).move_to([0, 1.7, 0])
        barA = gene_bar(10, 0.5, 0.05).move_to([-3.7, -1.2, 0])
        barB = gene_bar(10, 0.5, 0.05).move_to([3.7, -1.2, 0])
        sites = [2, 5, 7]
        label = T("same gene, two species", 40, TEXT).move_to([0, -3.2, 0])

        def show_q():
            self.play(GrowFromCenter(q), run_time=0.7)

        def show_bars():
            self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in barA], lag_ratio=0.06),
                      LaggedStart(*[FadeIn(s, scale=0.6) for s in barB], lag_ratio=0.06), run_time=1.6)

        def align():
            self.play(barA.animate.scale(1.45).move_to([0, -1.1, 0]), barB.animate.scale(1.45).move_to([0, -2.15, 0]),
                      run_time=1.5)

        def lab():
            self.play(FadeIn(label, shift=UP * 0.15), run_time=0.7)

        def diff():
            self.play(*[s.animate.set_fill(GOLD, 0.95).set_stroke(GOLD, 3) for i in sites for s in (barA[i], barB[i])], run_time=0.8)
            self.play(*[Indicate(s, color=GOLD, scale_factor=1.25) for i in sites for s in (barA[i], barB[i])], run_time=0.9)

        run_events(self, [
            (self.t_of("can their genes") - 0.2, show_q),
            (self.t_of("still tell you") - 0.2, show_bars),
            (self.t_of("line up the same") - 0.2, align),
            (self.t_of("from both") - 0.4, lab),
            (self.t_of("some sites differ") - 0.4, diff),
        ])
        self.finish()


# =============================================================================================
# s02 split
# =============================================================================================
def wf_rows(N=6):
    for s in range(1, 6000):
        r = random.Random(s)
        gold = [i == 0 for i in range(N)]
        rows = [(gold[:], None)]
        decl = False
        for _ in range(12):
            parents = [r.randrange(N) for _ in range(N)]
            new = [gold[p] for p in parents]
            if sum(new) < sum(gold):
                decl = True
            rows.append((new, parents))
            gold = new
            if all(gold) or not any(gold):
                break
        if all(gold) and 7 <= len(rows) <= 8 and decl:
            return rows
    raise RuntimeError("no WF path")


PANEL_X = (2.1, 6.6)
PANEL_CX = 4.35


class S02Split(Scn):
    def construct(self):
        jr = Jostle([-2.1, 0.0, 0], 2.1, 14, GREY, 0.14, 1.0, 5, 0.22, 6)
        self.play(FadeIn(jr), run_time=0.9)
        lab = VGroup(T("ancestral", 40, TEXT), T("population", 40, TEXT)).arrange(DOWN, buff=0.1).move_to([3.0, 0.0, 0])
        stem = Line(ROOT_C + UP * 0.62, FORK, color=GREY, stroke_width=12)
        bl = Line(FORK, TIP_L, color=BLUE, stroke_width=12)
        gr = Line(FORK, TIP_R, color=GREEN, stroke_width=12)
        node = Dot(FORK, radius=0.24, color=GREY)
        tl, tr = Dot(TIP_L, radius=0.24, color=BLUE), Dot(TIP_R, radius=0.24, color=GREEN)
        rows = wf_rows()
        G = len(rows)
        panel = RoundedRectangle(corner_radius=0.2, width=PANEL_X[1] - PANEL_X[0], height=5.05, stroke_color=BLUE, stroke_width=4,
                                 fill_color=BLUE, fill_opacity=0.18).move_to([PANEL_CX, 0.02, 0])
        plab = T("one lineage", 34, BLUE).move_to([PANEL_CX, 3.2, 0])
        ys = [-2.05 + i * 0.58 for i in range(G)]
        xs = [PANEL_CX + (j - 2.5) * 0.68 for j in range(6)]
        rowg = []
        for i, (gl, par) in enumerate(rows):
            dots = [Dot([xs[j], ys[i], 0], radius=0.19, color=GOLD if gl[j] else BLUE) for j in range(6)]
            lines = []
            if par:
                for j in range(6):
                    lines.append(Line([xs[par[j]], ys[i - 1], 0], [xs[j], ys[i], 0], color=GOLD if gl[j] else BLUE, stroke_width=3.5).set_opacity(0.85))
            rowg.append(VGroup(*lines, *dots))
        tick = tick_mark(-1, 0.45)
        slabel = T("substitution", 36, GOLD).move_to([-5.0, 0.55, 0])
        spark_pts = [(-1, 0.25), (1, 0.3), (-1, 0.62), (1, 0.55), (-1, 0.82), (1, 0.8)]
        sparks = [Dot(bpt(s, f) + np.array([0.22 * s, 0.05, 0]), radius=0.16, color=GOLD) for s, f in spark_pts]
        flyer = Dot(radius=0.24, color=GOLD)

        def lbl():
            self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.6)

        def split():
            self.play(FadeOut(lab), jr.animate.scale(0.3).move_to(ROOT_C), run_time=0.9)
            self.play(Create(stem), run_time=0.4)
            self.play(Create(bl), Create(gr), FadeIn(node), run_time=1.2)
            self.play(FadeIn(tl), FadeIn(tr), run_time=0.4)

        def mut():
            self.play(LaggedStart(*[FadeIn(s, scale=0.3) for s in sparks], lag_ratio=0.25), run_time=1.4)
            self.play(FadeOut(VGroup(*sparks)), run_time=0.4)

        def panel_in():
            self.play(FadeIn(panel), FadeIn(plab), FadeIn(rowg[0]), run_time=0.8)

        def make_row(i):
            def f():
                anims = [FadeIn(rowg[i])]
                if i >= 2:
                    anims.append(rowg[i - 2].animate.set_opacity(0.3))
                self.play(*anims, run_time=min(0.45, 2.9 / (G - 1) * 0.8))
            return f

        t0, t1 = self.t_of("some spread") - 0.2, self.t_of("carries them") - 0.1
        events = [(self.t_of("ancestral population") - 0.4, lbl), (self.t_of("splits into") - 0.4, split),
                  (self.t_of("keeps gaining") - 0.2, mut), (self.t_of("keeps gaining") + 1.9, panel_in)]
        for i in range(1, G):
            events.append((t0 + (t1 - t0) * (i - 1) / (G - 1), make_row(i)))

        def fly():
            top = VGroup(*[m for m in rowg[-1] if isinstance(m, Dot)])
            self.play(Indicate(top, color=GOLD, scale_factor=1.15), run_time=0.7)
            flyer.move_to([PANEL_CX, ys[-1], 0])
            self.add(flyer)
            path = ArcBetweenPoints(np.array([PANEL_CX, ys[-1], 0]), bpt(-1, 0.45), angle=0.9)
            self.play(MoveAlongPath(flyer, path), run_time=1.6)

        def stamp():
            self.remove(flyer)
            self.play(GrowFromCenter(tick), FadeIn(slabel, shift=RIGHT * 0.1), run_time=0.7)

        events += [(self.t_of("a mutation that") - 0.2, fly), (self.t_of("a substitution") - 0.2, stamp)]
        run_events(self, events)
        self.finish()


# =============================================================================================
# s03 both branches
# =============================================================================================
B_TICKS = [0.2, 0.45, 0.78]
G_TICKS = [0.3, 0.55, 0.85]


class S03Both(Scn):
    def construct(self):
        tree = make_tree([0.45], [])
        self.add(tree)
        new = [(0.4, -1, 0.2), (1.2, 1, 0.3), (2.0, -1, 0.78), (2.9, 1, 0.55), (4.6, 1, 0.85)]
        mk = {-1: [], 1: []}

        def tickfn(side, f):
            def fn():
                tk = tick_mark(side, f)
                mk[side].append(tk)
                self.play(GrowFromCenter(tk), run_time=0.5)
            return fn
        events = [(t, tickfn(s, f)) for t, s, f in new]

        def pulse():
            self.play(Indicate(tree.p["node"], color=TEXT, scale_factor=2.4), run_time=1.0)

        barL, barR = gene_bar(8, 0.27, 0.04), gene_bar(8, 0.27, 0.04)
        barL.move_to(TIP_L + UP * 0.75)
        barR.move_to(TIP_R + UP * 0.75)
        sitesL, sitesR = [1, 4, 6], [2, 5, 7]
        l1 = T("differences", 38, TEXT)
        l2 = T("= 3 blue ticks", 34, BLUE)
        l3 = T("+ 3 green ticks", 34, GREEN)
        d_eq = M("D = 2rt", 56, GOLD)
        n1, n2 = T("same rate r", 34, TEXT), T("on both branches", 34, TEXT)
        for m, y in ((l1, 2.7), (l2, 1.85), (l3, 1.05), (d_eq, -0.7), (n1, -1.7), (n2, -2.3)):
            m.move_to([2.5, y, 0], aligned_edge=LEFT)

        def bars():
            self.play(FadeIn(barL), FadeIn(barR), run_time=0.8)
            self.play(*[barL[i].animate.set_fill(GOLD, 0.95).set_stroke(GOLD, 3) for i in sitesL],
                      *[barR[i].animate.set_fill(GOLD, 0.95).set_stroke(GOLD, 3) for i in sitesR], run_time=0.8)

        def f_diff():
            self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.6)

        def f_blue():
            self.play(FadeIn(l2, shift=RIGHT * 0.1), *[Indicate(t, color=TEXT, scale_factor=1.6) for t in mk[-1] + [tick_mark(-1, 0.45)]][:0], run_time=0.8)

        def f_green():
            self.play(FadeIn(l3, shift=RIGHT * 0.1), run_time=0.8)

        def f_eq():
            self.play(FadeIn(d_eq, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(n1), FadeIn(n2), run_time=0.6)

        events += [(self.t_of("common ancestor") - 0.9, pulse), (self.t_of("so the differences") - 0.2, bars),
                   (self.t_of("between two species") - 0.2, f_diff), (self.t_of("both branches added") - 0.3, f_blue),
                   (self.t_of("added together") - 0.2, f_green), (self.t_of("added together") + 1.0, f_eq)]
        run_events(self, events)
        self.finish()


# =============================================================================================
# s04 why steady
# =============================================================================================
class S04Why(Scn):
    def construct(self):
        tree = make_tree(B_TICKS, G_TICKS)
        self.add(tree)
        self.play(tree.animate.scale(0.55).move_to([-4.9, 1.9, 0]), run_time=1.0)
        trk = Line([-6.2, -2.5, 0], [6.2, -2.5, 0], color=TEXT, stroke_width=6).set_opacity(0.85)
        self.play(Create(trk), run_time=0.5)
        ticks = [Line([-5.2 + i * 1.15, -3.0, 0], [-5.2 + i * 1.15, -2.0, 0], color=GOLD, stroke_width=11) for i in range(10)]
        events = [(1.0 + 0.72 * i, (lambda tk=tk: self.play(GrowFromEdge(tk, DOWN), run_time=0.3))) for i, tk in enumerate(ticks)]
        cnt = T("count = time", 40, GOLD).move_to([0.5, -3.45, 0])
        q = T("?", 260, TEXT, weight=BOLD).move_to([2.0, 0.4, 0])
        circ = blue_circle()
        circ.scale(0.05).move_to(tree.p["tl"].get_center())

        def f_cnt():
            self.play(FadeIn(cnt, shift=UP * 0.1), run_time=0.6)

        def f_q():
            self.play(GrowFromCenter(q), run_time=0.7)

        def zoom():
            self.add(circ)
            self.play(FadeOut(q), FadeOut(cnt), FadeOut(trk), FadeOut(VGroup(*ticks)), FadeOut(tree),
                      circ.animate.scale(20).move_to([0, 0, 0]), run_time=1.6)

        events += [(self.t_of("their count") - 0.2, f_cnt), (self.t_of("but why should") - 0.2, f_q), (self.t_of("the answer lies") - 0.4, zoom)]
        run_events(self, events)
        self.finish()


# =============================================================================================
# s05 two populations
# =============================================================================================
class S05Pops(Scn):
    def construct(self):
        circ = blue_circle()
        self.add(circ)
        small, large = pops_pair(1, 1.0)
        lab_s, lab_l = T("SMALL", 40, BLUE).move_to(SM_LABEL), T("LARGE", 40, BLUE).move_to(LG_LABEL)
        note = T("more individuals (schematic, not to scale)", 28, TEXT).move_to([0, -3.3, 0])
        neutral = T("neutral: no effect on survival or reproduction", 30, GOLD).move_to([0, -3.3, 0])
        counter = GenCounter(large, GAP, 0)
        small.restart()
        large.restart()

        def boxes():
            self.play(FadeOut(circ), FadeIn(small), FadeIn(large), run_time=1.2)

        def labs():
            self.play(FadeIn(lab_s, shift=UP * 0.1), run_time=0.5)

        def labl():
            self.play(FadeIn(lab_l, shift=UP * 0.1), FadeIn(note, shift=UP * 0.1), run_time=0.5)

        def gens():
            large.restart()
            small.restart()
            self.play(FadeIn(counter), run_time=0.5)

        def foc():
            self.play(Circumscribe(small.rect, color=GOLD, time_width=1.0), Circumscribe(large.rect, color=GOLD, time_width=1.0), run_time=1.4)

        def tag():
            self.play(FadeOut(note), FadeIn(neutral, shift=UP * 0.1), run_time=0.7)

        run_events(self, [(0.3, boxes), (self.t_of("one small") - 0.2, labs), (self.t_of("one large") - 0.2, labl),
                          (self.t_of("every generation") - 0.2, gens), (self.t_of("follow only") - 0.2, foc), (self.t_of("they make no") - 0.2, tag)])
        self.finish()


# =============================================================================================
# s06 predict
# =============================================================================================
class S06Predict(Scn):
    def construct(self):
        spark_s = lambda t: 1 if t >= 4.8 else 0
        spark_l = lambda t: 10 if t >= 4.8 else 0
        small, large = pops_pair(1, 1.0, spark_s, spark_l)
        lab_s, lab_l = T("SMALL", 40, BLUE).move_to(SM_LABEL), T("LARGE", 40, BLUE).move_to(LG_LABEL)
        lab_l2 = T("10× more individuals", 40, BLUE).move_to(LG_LABEL)
        counter = GenCounter(large, GAP, 11)
        large.t = 0.0
        self.add(small, large, lab_s, lab_l, counter)
        mut = T("10× more new mutations", 36, GOLD).move_to([0, -3.3, 0])
        q = T("substitutions 10× faster?", 40, TEXT).move_to([-0.2, 3.3, 0])
        yes, no = chip("yes", GREEN, 36), chip("no", RED, 36)
        yes.move_to([-0.85, 0.85, 0])
        no.move_to([-0.85, -0.45, 0])

        def big():
            self.play(ReplacementTransform(lab_l, lab_l2), run_time=0.8)

        def newm():
            self.play(FadeOut(counter), FadeIn(mut, shift=UP * 0.1), run_time=0.6)

        def ask():
            self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.7)

        def btn():
            self.play(FadeIn(yes, scale=0.8), FadeIn(no, scale=0.8), run_time=0.6)

        run_events(self, [(self.t_of("ten times bigger") - 0.5, big), (self.t_of("makes ten times") - 0.1, newm),
                          (self.t_of("does it pile") - 0.2, ask), (self.t_of("ten times faster") - 0.2, btn)])
        self.finish()


# =============================================================================================
# s07 pause: the question, still, with a countdown
# =============================================================================================
class S07Pause(NarratedScene):
    def construct(self):
        add_motes(self)
        small, large = pops_pair(1, 1.0, lambda t: 1, lambda t: 10)
        lab_s = T("SMALL", 40, BLUE).move_to(SM_LABEL)
        lab_l = T("10× more individuals", 40, BLUE).move_to(LG_LABEL)
        mut = T("10× more new mutations", 30, GOLD).move_to([0, -2.8, 0])
        q = T("substitutions 10× faster?", 40, TEXT).move_to([-0.2, 3.3, 0])
        yes, no = chip("yes", GREEN, 36), chip("no", RED, 36)
        yes.move_to([-0.85, 0.85, 0])
        no.move_to([-0.85, -0.45, 0])
        cap = T("Predict: faster, or the same?", 34, GOLD).move_to([0, -3.5, 0])
        self.add(small, large, lab_s, lab_l, mut, q, yes, no, cap)
        ring = Circle(radius=0.5, color=TEXT, stroke_width=5).move_to([-0.85, -1.6, 0])
        arc = Arc(radius=0.5, start_angle=PI / 2, angle=-TAU, color=GOLD, stroke_width=10).move_to([-0.85, -1.6, 0])
        arc.t = 0.0
        num = M("5", 34, GOLD).move_to([-0.85, -1.6, 0])
        num.k = 5

        def f(m, dt):
            m.t += dt
            frac = max(0.02, 1 - m.t / 5.0)
            m.become(Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * frac, color=GOLD, stroke_width=10).move_to([-0.85, -1.6, 0]))
        arc.add_updater(f)

        def g(m, dt):
            k = max(1, math.ceil(5 - arc.t))
            if k != m.k:
                m.k = k
                m.become(M(str(k), 34, GOLD).move_to([-0.85, -1.6, 0]))
        num.add_updater(g)
        self.add(ring, arc, num)
        self.finish()


# =============================================================================================
# s08 reveal
# =============================================================================================
def ramp_fn(ramps, spark, period=0.9):
    def fn(T):
        for st, seq in ramps:
            i = int((T - st) / period)
            if 0 <= i < len(seq):
                return seq[i]
        return spark(T)
    return fn


S_RAMPS = [(3.0, [1, 2, 3, 4, 5, 6]), (11.0, [1, 2, 3, 4, 5, 6])]
L_RAMPS = [(8.6, [1, 2, 3, 5, 8, 12, 17, 24])]
S_PRE = [8.0, 15.8]
L_PRE = [15.3]
TRK_Y = -2.9


def small_spark(T):
    return 1 if int(T * 1.1) % 3 == 0 else 0


def large_spark(T):
    if 2.0 <= T < 3.9:
        return 1
    return 3 if int(T) % 2 == 0 else 2


class S08Reveal(Scn):
    def construct(self):
        trk_s = Track(SM[0], SM[1], TRK_Y, TSPAN)
        trk_l = Track(LG[0], LG[1], TRK_Y, TSPAN)
        small, large = pops_pair(1, 0.9, ramp_fn(S_RAMPS, small_spark), ramp_fn(L_RAMPS, large_spark), 0.0,
                                 (lambda p: trk_s.fire(), lambda p: trk_l.fire()))
        lab_s, lab_l = T("SMALL", 40, BLUE).move_to(SM_LABEL), T("10× more individuals", 40, BLUE).move_to(LG_LABEL)
        counter = GenCounter(large, GAP, 23)
        corner = T("ideal neutral model, single-copy mutations", 26, TEXT).move_to([0, -3.55, 0])
        t1 = T("10× more new mutations", 36, GOLD).move_to([-6.4, 3.25, 0], aligned_edge=LEFT)
        t2 = T("each: 1/10 the expected", 34, TEXT).move_to([-6.4, 2.5, 0], aligned_edge=LEFT)
        t3 = T("fixation probability", 34, TEXT).move_to([-6.4, 1.9, 0], aligned_edge=LEFT)
        self.add(small, large, lab_s, lab_l, counter, trk_s, trk_l)

        def c():
            self.play(FadeIn(corner), run_time=0.6)

        def a1():
            self.play(FadeIn(t1, shift=RIGHT * 0.1), run_time=0.6)

        def a2():
            self.play(FadeIn(t2, shift=RIGHT * 0.1), FadeIn(t3, shift=RIGHT * 0.1), run_time=0.7)

        def p1():
            self.play(Indicate(t1, color=GOLD, scale_factor=1.08), run_time=0.9)

        def p2():
            self.play(Indicate(VGroup(t2, t3), color=GOLD, scale_factor=1.08), run_time=0.9)

        run_events(self, [(0.4, c), (self.t_of("in the large") - 0.2, a1), (self.t_of("its chance") - 0.2, a2),
                          (self.t_of("more mutations") - 0.2, p1), (self.t_of("less likely") - 0.2, p2)])
        self.finish()


# =============================================================================================
# s09 the two effects cancel
# =============================================================================================
class S09Rule(Scn):
    def construct(self):
        t0 = S08_LEN
        trk_s = Track(SM[0], SM[1], TRK_Y, TSPAN, t0, S_PRE)
        trk_l = Track(LG[0], LG[1], TRK_Y, TSPAN, t0, L_PRE)
        evs = [(t - t0, (lambda: trk_s.fire())) for t in (21.5, 25.3, 29.8)] + [(t - t0, (lambda: trk_l.fire())) for t in (20.9, 24.0, 27.4, 30.5)]
        sched = Sched(evs, 0.0)
        small, large = pops_pair(1, 0.9, lambda T: small_spark(T), lambda T: 3 if int(T) % 2 == 0 else 2, t0)
        t1 = T("10× more new mutations", 36, GOLD).move_to([-6.4, 3.25, 0], aligned_edge=LEFT)
        t2 = T("each: 1/10 the expected", 34, TEXT).move_to([-6.4, 2.5, 0], aligned_edge=LEFT)
        t3 = T("fixation probability", 34, TEXT).move_to([-6.4, 1.9, 0], aligned_edge=LEFT)
        lab_s, lab_l = T("SMALL", 40, BLUE).move_to(SM_LABEL), T("10× more individuals", 40, BLUE).move_to(LG_LABEL)
        cs = T("ticks 2", 36, GOLD).move_to([(SM[0] + SM[1]) / 2, -3.5, 0])
        cl = T("ticks 1", 36, GOLD).move_to([(LG[0] + LG[1]) / 2, -3.5, 0])
        cs.n = cl.n = 0

        def upd(trk):
            def f(mm, dt):
                if trk.count != mm.n:
                    mm.n = trk.count
                    mm.become(T(f"ticks {trk.count}", 36, GOLD).move_to(mm.get_center()))
            return f
        cs.add_updater(upd(trk_s))
        cl.add_updater(upd(trk_l))
        samep = VGroup(T("same average", 26, TEXT), T("rate", 26, TEXT)).arrange(DOWN, buff=0.12).move_to(GAP)
        e1 = T("= same rate", 40, GOLD).move_to([-6.4, 1.1, 0], aligned_edge=LEFT)
        k1 = T("substitution rate K", 38, GOLD).move_to([-6.4, 3.25, 0], aligned_edge=LEFT)
        k2 = T("= mutation rate mu", 38, TEXT).move_to([-6.4, 2.5, 0], aligned_edge=LEFT)
        k3 = T("(neutral sites, on average)", 30, TEXT).move_to([-6.4, 1.85, 0], aligned_edge=LEFT)
        cl_trk = Line([0.9, 3.1, 0], [6.3, 3.1, 0], color=TEXT, stroke_width=6).set_opacity(0.85)
        clock_ticks = [Line([1.1 + 0.55 * i, 2.8, 0], [1.1 + 0.55 * i, 3.4, 0], color=GOLD, stroke_width=10) for i in range(10)]
        cl_lab = T("clock (on average)", 36, GOLD).move_to([3.6, 2.45, 0])
        self.add(small, large, trk_s, trk_l, t1, t2, t3, lab_s, lab_l, sched)

        def counters():
            self.play(FadeOut(lab_s), FadeOut(lab_l), FadeIn(cs), FadeIn(cl), run_time=0.5)

        def cancel():
            self.play(Indicate(VGroup(t1, t2, t3), color=GOLD, scale_factor=1.06), FadeIn(e1, shift=RIGHT * 0.1), run_time=1.0)

        def eq():
            self.play(FadeOut(VGroup(t1, t2, t3, e1)), run_time=0.4)
            self.play(FadeIn(k1, shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(k2, shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(k3, shift=RIGHT * 0.1), run_time=0.5)

        def same():
            self.play(FadeIn(samep), run_time=0.6)

        def clk():
            self.play(Create(cl_trk), run_time=0.4)
            for tk in clock_ticks[:4]:
                self.play(GrowFromEdge(tk, DOWN), run_time=0.25)
                self.wait(0.15)

        def clklab():
            self.play(FadeIn(cl_lab, shift=UP * 0.1), run_time=0.5)
            for tk in clock_ticks[4:8]:
                self.play(GrowFromEdge(tk, DOWN), run_time=0.25)
                self.wait(0.1)

        run_events(self, [(0.1, counters), (self.t_of("cancel") - 0.1, cancel), (self.t_of("on average") - 0.4, eq),
                          (self.t_of("whatever the") - 0.2, same), (self.t_of("that steady input") - 0.4, clk), (self.t_of("makes the clock") - 0.3, clklab)])
        self.finish()


# =============================================================================================
# s10 rate or time?
# =============================================================================================
class S10Ratetime(Scn):
    def construct(self):
        bar = gene_bar(8, 0.45, 0.08).move_to([1.0, -3.45, 0])
        dist = T("same distance", 36, GOLD).move_to([-3.3, -3.45, 0])
        short, sticks = mini_tree(-3.9, -2.0, 3.0, 1.5, 4)
        tall, tticks = mini_tree(3.9, -2.0, 5.2, 1.5, 4)
        l_fast = T("fast rate, short time", 34, TEXT).move_to([-3.9, -2.65, 0])
        l_slow = T("slow rate, long time", 34, TEXT).move_to([3.9, -2.65, 0])
        q = T("?", 260, TEXT, weight=BOLD).move_to([0, 0.5, 0])

        def f_bar():
            self.play(LaggedStart(*[s.animate.set_fill(GOLD, 0.95).set_stroke(GOLD, 3) for s in bar], lag_ratio=0.12), run_time=1.6)

        def f_dist():
            self.play(FadeIn(dist, shift=UP * 0.1), run_time=0.6)

        def f_short():
            self.play(Create(short), run_time=1.0)
            self.play(LaggedStart(*[GrowFromCenter(t) for t in sticks], lag_ratio=0.2), run_time=1.4)

        def f_sl():
            self.play(FadeIn(l_fast, shift=UP * 0.1), run_time=0.6)

        def f_tall():
            self.play(Create(tall), run_time=1.4)
            self.play(LaggedStart(*[GrowFromCenter(t) for t in tticks], lag_ratio=0.3), run_time=2.0)

        def f_ll():
            self.play(FadeIn(l_slow, shift=UP * 0.1), run_time=0.6)

        def f_q():
            self.play(GrowFromCenter(q), run_time=0.8)
            q.add_updater(lambda m, dt: m.rotate(math.sin(self.elapsed() * 3) * 0.02))

        self.add(bar)
        run_events(self, [(0.3, f_bar), (self.t_of("one distance") - 0.3, f_dist), (self.t_of("one distance") + 0.8, f_short),
                          (self.t_of("short time") - 0.1, f_sl), (self.t_of("slow rate") - 0.2, f_tall), (self.t_of("long time") - 0.1, f_ll),
                          (self.t_of("the sequences alone") - 0.2, f_q)])
        self.finish()


# =============================================================================================
# s11 calibrate with a fossil
# =============================================================================================
class S11Calib(Scn):
    def construct(self):
        t1, k1 = mini_tree(-3.3, -2.4, 2.6, 1.4, 3)
        t2, k2 = mini_tree(3.1, -2.4, 5.2, 1.4, 6)
        stone = fossil_stone(0.5)
        fork1 = t1.fork
        tag1 = chip("fossil date", FOSSIL, 28).move_to([-5.3, -2.55, 0])
        tag2 = chip("computed date", GOLD, 28).move_to([5.1, -2.55, 0])
        arrow = CurvedArrow(np.array([-1.7, 1.0, 0]), np.array([1.2, 1.0, 0]), angle=-0.5, color=GOLD, stroke_width=8)
        rate = T("shared rate", 40, GOLD).move_to([-0.2, 2.2, 0])
        self.add(t1, t2, k1, k2)
        out = T("a date from outside", 40, TEXT).move_to([0, 3.35, 0])

        def f_out():
            self.play(FadeIn(out, shift=UP * 0.1), run_time=0.6)

        def f_drop():
            self.play(FadeOut(out), run_time=0.3)
            stone.move_to([-3.3, 3.4, 0])
            self.add(stone)
            self.play(stone.animate.move_to(fork1 + UP * 0.02), run_time=1.0, rate_func=rush_into)
            self.play(Indicate(stone, color=FOSSIL, scale_factor=1.2), FadeIn(tag1, shift=RIGHT * 0.1), run_time=0.8)

        def f_arrow():
            self.play(Create(arrow), FadeIn(rate, shift=UP * 0.1), run_time=1.2)

        def f_comp():
            self.play(FadeIn(tag2, shift=LEFT * 0.1), Indicate(t2[3], color=GOLD, scale_factor=2.0), run_time=1.0)

        run_events(self, [(0.3, f_out), (self.t_of("the commonest") - 0.2, f_drop),
                          (self.t_of("if two splits") - 0.2, f_arrow), (self.t_of("one dated split") - 0.2, f_comp)])
        self.finish()


# =============================================================================================
# s12 a fossil gives a minimum age
# =============================================================================================
class S12Minimum(Scn):
    def construct(self):
        ax = Arrow([-2.2, -3.4, 0], [-2.2, 3.0, 0], color=TEXT, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.1)
        axl = T("time", 36, TEXT).move_to([-2.2, 3.45, 0])
        pin_y = 0.8
        stone = fossil_stone(0.6).move_to([-2.2, 3.2, 0])
        dash = DashedLine([-2.2, pin_y, 0], [6.4, pin_y, 0], color=FOSSIL, stroke_width=6)
        tag = chip("at least this old", FOSSIL, 36).move_to([2.9, pin_y + 0.75, 0])
        band = VGroup(*[Rectangle(width=8.6, height=0.7, stroke_width=0, fill_color=GOLD, fill_opacity=0.5 - 0.08 * i).move_to([2.1, pin_y - 0.35 - 0.7 * i, 0]) for i in range(5)])
        arr = Arrow([0.6, pin_y - 0.3, 0], [0.6, -3.3, 0], color=GOLD, stroke_width=12, buff=0)
        lab = VGroup(T("real split:", 40, GOLD), T("somewhere earlier", 40, GOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([1.2, -1.2, 0], aligned_edge=LEFT)
        self.play(Create(ax), FadeIn(axl), run_time=0.8)

        def f_drop():
            self.add(stone)
            self.play(stone.animate.move_to([-2.2, pin_y, 0]), run_time=1.0, rate_func=rush_into)
            self.play(Indicate(stone, color=FOSSIL, scale_factor=1.25), run_time=0.7)

        def f_then():
            self.play(Create(dash), FadeIn(tag, shift=LEFT * 0.1), run_time=1.0)

        def f_band():
            self.play(LaggedStart(*[FadeIn(r) for r in band], lag_ratio=0.25), Create(arr), run_time=1.8)

        def f_lab():
            self.play(FadeIn(lab, shift=RIGHT * 0.1), run_time=0.8)

        def f_min():
            self.play(Circumscribe(tag, color=GOLD, time_width=1.2), run_time=1.3)

        run_events(self, [(self.t_of("fossil") - 0.4, f_drop), (self.t_of("existed by") - 0.2, f_then), (self.t_of("real split") - 0.2, f_band),
                          (self.t_of("by an unknown") - 0.2, f_lab), (self.t_of("minimum age") - 0.5, f_min)])
        self.finish()


# =============================================================================================
# s13 only neutral changes count
# =============================================================================================
class S13Neutral(Scn):
    def construct(self):
        box = (-6.4, -0.8, -2.2, 2.2)
        pop = Pop(box, 20, 5, 1.0)
        pop_lab = T("population", 38, BLUE).move_to([-3.6, 2.75, 0])
        tspan = self.narration_s + 0.4
        tr1 = Track(1.0, 6.5, 1.2, tspan)
        tr2 = Track(1.0, 6.5, -1.6, tspan)
        l1 = T("neutral changes", 38, GOLD).move_to([3.75, 2.0, 0])
        l2 = VGroup(T("constrained gene:", 36, TEXT), T("slow clock", 36, TEXT)).arrange(DOWN, buff=0.1).move_to([3.75, -0.6, 0])
        ev = Sched([(3.1, tr1.fire), (4.5, tr1.fire), (5.6, tr1.fire), (10.2, tr1.fire), (11.9, tr1.fire), (12.3, tr2.fire)], 0.0)
        mut = Dot(radius=0.3, color=GOLD).move_to([-3.6, 0.0, 0])
        cross = Cross(Dot(radius=0.4), stroke_color=RED, stroke_width=10).move_to(mut)
        rem = T("removed by selection", 36, RED).move_to([-3.6, -2.85, 0])
        self.add(pop, pop_lab, tr1, ev)
        self.add(tr2)
        tr2.set_opacity(0)

        def f_l1():
            self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.6)

        def f_new():
            self.play(FadeIn(mut, scale=0.3), run_time=0.6)

        def f_rem():
            self.play(mut.animate.set_color(RED), run_time=0.4)
            self.play(Create(cross), FadeIn(rem, shift=UP * 0.1), run_time=0.6)

        def f_gone():
            self.play(FadeOut(mut), FadeOut(cross), FadeOut(rem), run_time=0.7)

        def f_tr2():
            self.play(tr2.animate.set_opacity(1), FadeIn(l2, shift=UP * 0.1), run_time=0.8)

        run_events(self, [(self.t_of("the clock") - 0.3, f_l1), (self.t_of("a mutation removed") - 0.2, f_new),
                          (self.t_of("removed by selection") - 0.2, f_rem), (self.t_of("never becomes") + 0.5, f_gone),
                          (self.t_of("so a tightly") - 0.2, f_tr2)])
        self.finish()


# =============================================================================================
# s14 close
# =============================================================================================
class S14Close(Scn):
    def construct(self):
        tree = make_tree([], [])
        self.add(tree)
        fr = [0.15, 0.32, 0.5, 0.68, 0.86]
        bt = [tick_mark(-1, f) for f in fr]
        gt = [tick_mark(1, f) for f in fr]
        events = []
        for i in range(5):
            events.append((0.2 + 0.9 * i, (lambda i=i: self.play(GrowFromCenter(bt[i]), GrowFromCenter(gt[i]), run_time=0.5))))
        count = VGroup(M("10", 96, GOLD), T("substitutions", 36, GOLD)).arrange(DOWN, buff=0.15).move_to([3.5, 1.5, 0])
        stone = fossil_stone(0.5)
        tag = T("at least", 38, "#E0BE92").move_to([-5.3, -2.6, 0])
        arr = Arrow(FORK + np.array([-0.6, -0.3, 0]), np.array([-4.3, -2.4, 0]), color="#E0BE92", stroke_width=8, buff=0.05)
        ax = Arrow([5.8, -3.2, 0], [5.8, 3.2, 0], color=TEXT, stroke_width=8, buff=0)
        axl = T("years", 36, TEXT).move_to([5.8, 3.55, 0])
        d1 = DashedLine(TIP_R + RIGHT * 0.3, [5.8, TIP_R[1], 0], color=GOLD, stroke_width=5)
        d2 = DashedLine(FORK + RIGHT * 0.3, [5.8, FORK[1], 0], color=GOLD, stroke_width=5)
        span = VGroup(T("time since", 36, GOLD), T("the split", 36, GOLD)).arrange(DOWN, buff=0.1).move_to([3.7, -0.5, 0])

        def f_count():
            self.play(FadeIn(count, shift=UP * 0.1), Indicate(VGroup(*bt, *gt), color=GOLD, scale_factor=1.3), run_time=1.0)

        def f_stone():
            stone.move_to([-2.1, 3.4, 0])
            self.add(stone)
            self.play(stone.animate.move_to(FORK), run_time=1.0, rate_func=rush_into)
            self.play(Create(arr), FadeIn(tag, shift=RIGHT * 0.1), run_time=0.8)

        def f_time():
            self.play(Create(ax), FadeIn(axl), Create(d1), Create(d2), run_time=1.0)
            self.play(FadeIn(span, shift=LEFT * 0.1), run_time=0.7)

        events += [(self.t_of("count them") - 0.2, f_count), (self.t_of("add one") - 0.2, f_stone), (self.t_of("becomes time") - 0.8, f_time)]
        run_events(self, events)
        self.finish()


# =============================================================================================
# s15 end card
# =============================================================================================
class S15End(EndCard):
    LINE = "Neutral changes tick at the mutation rate; one dated split reads time."
