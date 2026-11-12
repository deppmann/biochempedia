"""Molecular evolution, chapter 2: Reading Selection in Genes (Biochemistrypedia explainer, level-up film 2)

COLOUR MAP (the same in both chapters)
  GOLD   = a DNA change: a new mutation, a tick mark, a changed site
  BLUE   = species A: its branch and dots;  GREEN = species B
  GREY   = the common ancestor and unchanged sites
  brown stone = a fossil
  CORAL  = amino-acid (nonsynonymous / replacement) changes and the dN counter
  TEAL   = synonymous changes and the dS counter
  RED    = a change removed by selection
Every number is on-screen text; trees, codon blocks, beads and dots are schematic cartoons.
No molecular structures. Chapter 1's tree is rebuilt at the same place and scale.
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
def add_motes(sc, n=60):
    """Faint drifting motes: a held frame is never a dead frame (pipeline 'ambient' idea, always on here)."""
    rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
    W, H = config.frame_width, config.frame_height
    motes = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.06, 0.13), color=rng.choice([TEAL, TEXT, GOLD])).set_opacity(rng.uniform(0.2, 0.38))
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



CORAL = "#FF9A76"
B_TICKS = [0.2, 0.45, 0.78]
G_TICKS = [0.3, 0.55, 0.85]
AA = ["#B58CE6", "#6FD3B5", "#E39BCB", "#A9B7D0", "#B7D36A", "#8E9CF0"]


def band(x0, x1, y0, y1, color, op=0.13):
    r = RoundedRectangle(corner_radius=0.2, width=x1 - x0, height=y1 - y0, stroke_width=0, fill_color=color, fill_opacity=op)
    r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0]).set_z_index(-5)
    return r


def cue(sc, phrase, lead=0.2, nth=0):
    return sc.t_of(phrase, nth) - lead


def swap(sc, old, new, rt=0.35):
    """Fade the old label out and the new one in; returns the new label."""
    anims = []
    if old is not None:
        anims.append(FadeOut(old))
    anims.append(FadeIn(new, shift=UP * 0.08))
    sc.play(*anims, run_time=rt)
    return new


# ---- a track of ticks with a moving cursor (the "same pace" picture) ----
class TTrack(VGroup):
    def __init__(self, x0, x1, y, color, times, t0, tspan, th=0.8, num_x=None, label=None, stroke=12):
        super().__init__()
        self.x0, self.x1, self.y, self.color = x0, x1, y, color
        self.t0, self.tspan, self.th = t0, tspan, th
        self.times = sorted(times)
        self.i, self.t, self.count = 0, 0.0, 0
        self.line = Line([x0, y, 0], [x1, y, 0], color=TEXT, stroke_width=stroke).set_opacity(0.85)
        self.cursor = Line([x0, y - th / 2 - 0.1, 0], [x0, y + th / 2 + 0.1, 0], color=TEXT, stroke_width=5).set_opacity(0)
        self.add(self.line, self.cursor)
        self.num = None
        if num_x is not None:
            self.num = M("0", 64, color).move_to([num_x, y, 0])
            self.add(self.num)
        self.add_updater(lambda m, dt: m._upd(dt))

    def _x(self, t):
        return self.x0 + (self.x1 - self.x0) * min(max((t - self.t0) / self.tspan, 0.0), 1.0)

    def _upd(self, dt):
        self.t += dt
        if self.t >= self.t0:
            self.cursor.set_opacity(1)
        self.cursor.move_to([self._x(self.t), self.y, 0])
        while self.i < len(self.times) and self.times[self.i] <= self.t:
            x = self._x(self.times[self.i])
            tk = Line([x, self.y - self.th / 2, 0], [x, self.y + self.th / 2, 0], color=self.color, stroke_width=13)
            tk.p = 1.0

            def f(m, dt):
                m.p = max(0.0, m.p - dt * 1.8)
                m.set_stroke(width=13 + 14 * m.p)
            tk.add_updater(f)
            self.add(tk)
            self.i += 1
            self.count += 1
            if self.num is not None:
                self.num.become(M(str(self.count), 64, self.color).move_to([self.x1 + 0.95, self.y, 0]))


# ---- the dN / dS counters and the omega dial (s05, s06) ----
DC = np.array([0.0, -2.3, 0.0])


class Rig:
    def __init__(self):
        self.branch = VGroup(Line([-5.9, 3.3, 0], [5.9, 3.3, 0], color=BLUE, stroke_width=10),
                             Dot([-5.9, 3.3, 0], radius=0.2, color=GREY), Dot([5.9, 3.3, 0], radius=0.2, color=BLUE))
        self.ticks = VGroup()
        self.n = self.s = self.idx = 0
        self.nx, self.sx = -2.9, 3.4
        self.numN = M("0", 84, CORAL).move_to([self.nx, 1.55, 0])
        self.numS = M("0", 84, TEAL).move_to([self.sx, 1.55, 0])
        self.labN = T("dN", 50, CORAL).move_to([-4.7, 1.55, 0])
        self.labS = T("dS", 50, TEAL).move_to([1.9, 1.65, 0])
        self.per = VGroup(T("per site", 28, TEXT).move_to([self.nx, 0.7, 0]), T("per site", 28, TEXT).move_to([self.sx, 0.7, 0]))
        self.arc = Arc(radius=2.1, start_angle=0, angle=PI, color=GREY, stroke_width=12).move_to(DC + UP * 2.1 * 0.6366)
        self.arc = Arc(radius=2.1, start_angle=0, angle=PI, color=GREY, stroke_width=12, arc_center=DC)
        marks = VGroup()
        for ang, txt, off in ((PI, "0", 0.45), (PI / 2, "1", 0.4), (0, "2+", 0.5)):
            u = np.array([math.cos(ang), math.sin(ang), 0])
            marks.add(Line(DC + u * 1.92, DC + u * 2.3, color=GOLD if txt == "1" else TEXT, stroke_width=7))
            marks.add(T(txt, 38, GOLD if txt == "1" else TEXT).move_to(DC + u * (2.3 + off)))
        self.marks = marks
        zones = VGroup()
        for a0, a1, col in ((PI, 0.6 * PI, RED), (0.6 * PI, 0.4 * PI, TEXT), (0.4 * PI, 0, CORAL)):
            zones.add(AnnularSector(inner_radius=0.35, outer_radius=2.0, angle=a0 - a1, start_angle=a1, color=col, fill_opacity=0.22, stroke_width=0).move_to(DC, aligned_edge=ORIGIN) if False else
                      AnnularSector(inner_radius=0.35, outer_radius=2.0, angle=a0 - a1, start_angle=a1, color=col, fill_opacity=0.22, stroke_width=0, arc_center=DC))
        self.zones = zones
        self.needle = Line(DC, DC + UP * 1.9, color=TEXT, stroke_width=12)
        self.hub = Dot(DC, radius=0.17, color=TEXT)
        self.ang = PI / 2
        self.needle.add_updater(lambda m, dt: self._needle(dt))
        self.eq = T("omega = dN / dS", 32, GOLD).move_to([-4.2, -3.4, 0])
        self.dial = VGroup(self.zones, self.arc, self.marks, self.needle, self.hub)

    def ratio(self):
        return (self.n + 2.0) / (self.s + 2.0)

    def _needle(self, dt):
        tgt = PI * (1 - min(self.ratio(), 2.0) / 2.0)
        self.ang += (tgt - self.ang) * min(1.0, dt * 2.2)
        end = DC + 1.9 * np.array([math.cos(self.ang), math.sin(self.ang), 0])
        self.needle.put_start_and_end_on(DC, end)

    def _tick(self, color):
        x = -5.5 + 0.42 * self.idx
        self.idx += 1
        tk = Line([x, 3.3 - 0.38, 0], [x, 3.3 + 0.38, 0], color=color, stroke_width=9)
        tk.p = 1.0

        def f(m, dt):
            m.p = max(0.0, m.p - dt * 1.8)
            m.set_stroke(width=9 + 12 * m.p)
        tk.add_updater(f)
        self.ticks.add(tk)

    def tickN(self):
        self.n += 1
        self._tick(CORAL)
        self.numN.become(M(str(self.n), 84, CORAL).move_to([self.nx, 1.55, 0]))

    def tickS(self):
        self.s += 1
        self._tick(TEAL)
        self.numS.become(M(str(self.s), 84, TEAL).move_to([self.sx, 1.55, 0]))

    def reset(self):
        self.ticks.submobjects = []
        self.n = self.s = self.idx = 0
        self.numN.become(M("0", 84, CORAL).move_to([self.nx, 1.55, 0]))
        self.numS.become(M("0", 84, TEAL).move_to([self.sx, 1.55, 0]))


# ---- codon world (s03, s04): same place and size in both scenes ----
BW = 0.55
BX = [-4.97 + 1.988 * i for i in range(6)]
BLK_Y, BEAD_Y = 1.8, -1.0


def codon_squares():
    blocks = []
    for i in range(6):
        sq = VGroup(*[Square(BW, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.5) for _ in range(3)])
        sq.arrange(RIGHT, buff=0.06).move_to([BX[i], BLK_Y, 0])
        blocks.append(sq)
    return blocks


def beads_and_lines():
    beads = [Circle(radius=0.52, stroke_color=TEXT, stroke_width=3, fill_color=AA[i], fill_opacity=1).move_to([BX[i], BEAD_Y, 0]) for i in range(6)]
    lines = [Line([BX[i], BLK_Y - 0.36, 0], [BX[i], BEAD_Y + 0.52, 0], color=GREY, stroke_width=5) for i in range(6)]
    return beads, lines


def gold_sq(sq):
    sq.set_fill(GOLD, 0.95).set_stroke(GOLD, 3)


# ---- the 2 x 2 table (s08 - s14): same place in every scene ----
XS = [-6.6, -2.9, 0.9, 4.7]
YS = [3.6, 2.4, 0.15, -2.1]
CX = [-1.0, 2.8]
CY = [1.275, -0.975]
TCX = (XS[0] + XS[3]) / 2


class Table:
    def __init__(self):
        cx, cy = (XS[0] + XS[3]) / 2, (YS[0] + YS[3]) / 2
        self.outer = Rectangle(width=XS[3] - XS[0], height=YS[0] - YS[3], stroke_color=GREY, stroke_width=5).move_to([cx, cy, 0])
        self.lines = VGroup(Line([XS[0], YS[1], 0], [XS[3], YS[1], 0]), Line([XS[0], YS[2], 0], [XS[3], YS[2], 0]),
                            Line([XS[1], YS[3], 0], [XS[1], YS[0], 0]), Line([XS[2], YS[3], 0], [XS[2], YS[0], 0]))
        self.lines.set_stroke(GREY, 4)
        self.grid = VGroup(self.outer, self.lines)
        self.fillC = Rectangle(width=3.8, height=1.2, stroke_width=0, fill_color=CORAL, fill_opacity=0.35).move_to([CX[0], 3.0, 0])
        self.fillS = Rectangle(width=3.8, height=1.2, stroke_width=0, fill_color=TEAL, fill_opacity=0.35).move_to([CX[1], 3.0, 0])
        self.tints = VGroup(*[Rectangle(width=3.8, height=2.25, stroke_width=0, fill_color=(CORAL, TEAL)[c], fill_opacity=0.12).move_to([CX[c], CY[r], 0]) for r in range(2) for c in range(2)])
        self.txtC = T("replacement", 34, CORAL).move_to([CX[0], 3.0, 0])
        self.txtS = T("synonymous", 34, TEAL).move_to([CX[1], 3.0, 0])
        self.hdrC = VGroup(self.fillC, self.txtC)
        self.hdrS = VGroup(self.fillS, self.txtS)
        self.r1 = VGroup(T("varies within", 30, TEXT), T("a species", 30, TEXT)).arrange(DOWN, buff=0.1).move_to([-4.75, CY[0], 0])
        self.r2 = VGroup(T("fixed between", 30, TEXT), T("species", 30, TEXT)).arrange(DOWN, buff=0.1).move_to([-4.75, CY[1], 0])

    def all(self):
        return VGroup(self.tints, self.grid, self.hdrC, self.hdrS, self.r1, self.r2)


def num_at(n, color, r, c, size=96):
    return M(str(n), size, color).move_to([CX[c], CY[r], 0])


def count_to(sc, r, c, N, color, run, size=96):
    pos = np.array([CX[c], CY[r], 0.0])
    m = M("0", size, color).move_to(pos)
    sc.add(m)

    def f(mob, a):
        mob.become(M(str(int(round(a * N))), size, color).move_to(pos))
    sc.play(UpdateFromAlphaFunc(m, f), run_time=run, rate_func=linear)
    return m


def row_frame(r, color=GOLD, w=6):
    rect = Rectangle(width=XS[3] - XS[1] - 0.12, height=2.15, stroke_color=color, stroke_width=w, fill_opacity=0).move_to([(XS[1] + XS[3]) / 2, CY[r], 0])
    return rect


def cell_frame(r, c, color=CORAL, w=7):
    rect = Rectangle(width=3.6, height=2.15, stroke_color=color, stroke_width=w, fill_opacity=0).move_to([CX[c], CY[r], 0])
    return rect


def glow(m, base=6, amp=4, sp=5.0):
    m.gt = 0.0

    def f(mm, dt):
        mm.gt += dt
        mm.set_stroke(width=base + amp * math.sin(mm.gt * sp))
    m.add_updater(f)
    return m


def fly(color, s=1.0):
    abd = Ellipse(width=0.95, height=0.62, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([-0.72, 0, 0])
    thor = Ellipse(width=0.85, height=0.62, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([0.05, 0.05, 0])
    head = Circle(radius=0.33, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([0.72, 0.1, 0])
    eye = Dot([0.84, 0.2, 0], radius=0.13, color=RED)
    stripes = VGroup(*[Line([x, -0.26, 0], [x, 0.26, 0], color=BG, stroke_width=4) for x in (-0.95, -0.72, -0.49)])
    legs = VGroup(*[Line([x, -0.25, 0], [x + dx, -0.7, 0], color=color, stroke_width=6) for x, dx in ((-0.25, -0.18), (0.05, 0.0), (0.35, 0.2))])
    wing = Ellipse(width=1.5, height=0.5, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.28).rotate(0.35).move_to([-0.55, 0.55, 0])
    wing.ph = 0.0

    def flap(m, dt):
        m.ph += dt
        m.rotate(0.012 * math.cos(m.ph * 9), about_point=np.array([-0.1, 0.3, 0]) * s + wing.get_center() * 0)
    g = VGroup(legs, abd, thor, stripes, wing, head, eye)
    return g.scale(s)


def stone_icon():
    return fossil_stone(0.38)


def clock_icon():
    c = Circle(radius=0.36, stroke_color=TEXT, stroke_width=5)
    h1 = Line(c.get_center(), c.get_center() + UP * 0.24, color=TEXT, stroke_width=5)
    h2 = Line(c.get_center(), c.get_center() + RIGHT * 0.18, color=TEXT, stroke_width=5)
    return VGroup(c, h1, h2)


def cross(mob, color=RED):
    cx, cy = mob.get_center()[:2]
    r = max(mob.width, mob.height) * 0.62
    return VGroup(Line([cx - r, cy - r, 0], [cx + r, cy + r, 0], color=color, stroke_width=9),
                  Line([cx - r, cy + r, 0], [cx + r, cy - r, 0], color=color, stroke_width=9))


def qmarks():
    q = VGroup(M("?", 130, GOLD).move_to([CX[0], CY[1], 0]), M("?", 130, GOLD).move_to([CX[1], CY[1], 0]))
    q.qt = 0.0

    def qpulse(m, dt):
        m.qt += dt
        m.set_opacity(0.55 + 0.45 * (0.5 + 0.5 * math.sin(m.qt * 4)))
    q.add_updater(qpulse)
    return q


def full_table_with_counts(scene, glow_cell=False):
    tb = Table()
    scene.add(tb.all())
    nums = [num_at(2, CORAL, 0, 0), num_at(42, TEAL, 0, 1), num_at(7, CORAL, 1, 0), num_at(17, TEAL, 1, 1)]
    scene.add(*nums)
    return tb, nums


# =============================================================================================
# s00 title
# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Molecular evolution"
    TITLE = "Reading Selection in Genes"


# =============================================================================================
# s01 link: the Y tree and two ways a count can depart from neutral
# =============================================================================================
class S01Link(Scn):
    def construct(self):
        tree = make_tree(B_TICKS, G_TICKS)
        PY, QY = 2.0, 0.2
        pline = Line([2.0, PY, 0], [6.4, PY, 0], color=TEXT, stroke_width=12)
        qline = Line([2.0, QY, 0], [6.4, QY, 0], color=TEXT, stroke_width=12)
        self.add(band(1.6, 6.8, 1.0, 3.4, RED, 0.1), band(1.6, 6.8, -1.2, 1.0, CORAL, 0.1))
        self.play(FadeIn(tree), Create(pline), Create(qline), run_time=1.2)
        xs = [2.4, 2.9, 3.4, 3.9, 4.4]
        mk = lambda x, y, c: Line([x, y - 0.38, 0], [x, y + 0.38, 0], color=c, stroke_width=10)
        pt = [mk(x, PY, GOLD) for x in xs]
        qt = [mk(x, QY, GOLD) for x in xs]
        qx = [mk(x, QY, CORAL) for x in (4.9, 5.4, 5.9)]
        dash1 = DashedLine([4.65, PY - 0.55, 0], [4.65, PY + 0.55, 0], color=GOLD, stroke_width=5)
        dash2 = DashedLine([4.65, QY - 0.55, 0], [4.65, QY + 0.55, 0], color=GOLD, stroke_width=5)
        lab_n = T("neutral count", 30, GOLD).move_to([4.2, -0.65, 0])
        lab_t = T("neutral count", 30, GOLD).move_to([-4.4, -2.3, 0])
        lab_p = T("purifying: lags", 32, RED).move_to([2.0, PY + 0.8, 0], aligned_edge=LEFT)
        lab_q = T("positive: runs ahead", 32, CORAL).move_to([2.0, QY + 0.8, 0], aligned_edge=LEFT)
        clue = T("possible clues, not proof", 30, TEXT).move_to([4.2, -1.55, 0])
        mag = VGroup(Circle(radius=0.55, stroke_color=TEXT, stroke_width=8), Line([0.39, -0.39, 0], [0.95, -0.95, 0], color=TEXT, stroke_width=11),
                     T("?", 44, GOLD).move_to([0, 0, 0])).move_to([2.6, -2.65, 0])
        wobble(mag, 0.1, 1.2)
        sel = T("selection?", 38, GOLD).move_to([5.0, -2.65, 0])
        crossed = [cross(pt[1]).scale(0.4), cross(pt[3]).scale(0.4)]

        def f_neutral():
            self.play(FadeIn(lab_t, shift=UP * 0.1), FadeIn(dash1), FadeIn(dash2), FadeIn(lab_n), run_time=0.9)

        def f_pur():
            self.play(FadeIn(lab_p), run_time=0.4)
            self.play(LaggedStart(*[GrowFromCenter(t) for t in pt], lag_ratio=0.35), run_time=1.5)

        def f_lag():
            self.play(*[t.animate.set_stroke(opacity=0.3) for t in (pt[1], pt[3])], *[Create(c) for c in crossed], run_time=0.8)

        def f_pos():
            self.play(FadeIn(lab_q), run_time=0.4)
            self.play(LaggedStart(*[GrowFromCenter(t) for t in qt], lag_ratio=0.3), run_time=1.3)

        def f_ahead():
            self.play(LaggedStart(*[GrowFromCenter(t) for t in qx], lag_ratio=0.35), run_time=1.3)

        def f_clue():
            self.play(FadeIn(clue, shift=UP * 0.1), run_time=0.7)

        def f_mag():
            self.play(FadeIn(mag, shift=UP * 0.2), run_time=0.7)

        def f_sel():
            self.play(FadeIn(sel, shift=LEFT * 0.1), run_time=0.7)

        run_events(self, [(cue(self, "neutral count"), f_neutral), (cue(self, "Purifying selection"), f_pur),
                          (cue(self, "lag", 0.1), f_lag), (cue(self, "Positive selection"), f_pos),
                          (cue(self, "run ahead", 0.4), f_ahead), (cue(self, "ahead", -0.6), f_clue),
                          (cue(self, "So how could", 0.2), f_mag), (cue(self, "real gene", 0.1), f_sel)])
        self.finish()


# =============================================================================================
# s02 idea: two kinds of change run at the same pace, then part ways
# =============================================================================================
class S02Idea(Scn):
    def construct(self):
        T_S = [3.9, 4.9, 5.9, 6.9, 7.9, 8.6, 9.3, 10.0, 10.7, 11.4, 12.1]
        T_C = [4.2, 5.1, 6.2, 7.1, 8.2, 10.9]
        tc = TTrack(-4.0, 4.6, 1.0, CORAL, T_C, 3.4, 9.4, th=1.7, num_x=5.55)
        ts = TTrack(-4.0, 4.6, -1.3, TEAL, T_S, 3.4, 9.4, th=1.7, num_x=5.55)
        lc = T("kind 1", 36, CORAL).move_to([-5.3, 1.0, 0])
        ls = T("kind 2", 36, TEAL).move_to([-5.3, -1.3, 0])
        top = T("neutral: same average pace", 42, TEXT).move_to([0, 3.0, 0])
        bot = T("departure beyond chance = clue to selection", 40, GOLD).move_to([0, -3.1, 0])
        # the counts move with the ticks: patch the readout position (x1 + 0.95)
        self.add(band(-6.3, 6.5, 0.1, 1.9, CORAL), band(-6.3, 6.5, -2.2, -0.4, TEAL), tc, ts)
        self.wait(0.5)

        def f_kinds():
            self.play(FadeIn(lc, shift=RIGHT * 0.1), FadeIn(ls, shift=RIGHT * 0.1), run_time=0.8)

        def f_same():
            self.play(FadeIn(top, shift=UP * 0.1), run_time=0.8)

        def f_part():
            self.play(FadeOut(top), run_time=0.5)

        def f_dep():
            self.play(FadeIn(bot, shift=UP * 0.1), run_time=0.9)

        run_events(self, [(cue(self, "two kinds"), f_kinds), (cue(self, "neutrality says"), f_same),
                          (cue(self, "part ways", 0.1), f_part), (cue(self, "selection may be", 0.2), f_dep)])
        self.finish()


# =============================================================================================
# s03 codons: synonymous change
# =============================================================================================
class S03Codons(Scn):
    def construct(self):
        self.add(band(-6.3, 6.3, 1.2, 2.4, GREY, 0.14), band(-6.3, 6.3, -1.8, -0.2, AA[0], 0.1))
        blocks = codon_squares()
        flat = VGroup(*[sq for b in blocks for sq in b])
        targets = [sq.get_center().copy() for sq in flat]
        for i, sq in enumerate(flat):
            sq.move_to([-5.9 + 0.65 * i, BLK_Y, 0])
        self.play(LaggedStart(*[FadeIn(sq) for sq in flat], lag_ratio=0.04), run_time=1.3)
        hl = Rectangle(width=1.95, height=0.9, stroke_color=TEXT, stroke_width=6, fill_opacity=0)
        beads, lines = beads_and_lines()
        alt = VGroup(*[codon_alt(BX[2] + dx) for dx in (-0.8, 0.8)])
        alt_lines = VGroup(*[Line([BX[2] + dx * 0.6, -2.3 + 0.2, 0], [BX[2] + dx * 0.25, BEAD_Y - 0.52, 0], color=GREY, stroke_width=4) for dx in (-0.8, 0.8)])
        lab = T("synonymous: same amino acid", 40, TEAL).move_to([0, -3.2, 0])

        def f_group():
            self.play(*[sq.animate.move_to(t) for sq, t in zip(flat, targets)], run_time=1.0)
            hl.move_to([BX[0], BLK_Y, 0])
            self.play(FadeIn(hl), run_time=0.3)
            for i in range(1, 6):
                self.play(hl.animate.move_to([BX[i], BLK_Y, 0]), run_time=0.4)
            self.play(FadeOut(hl), run_time=0.3)

        def f_code():
            self.play(LaggedStart(*[AnimationGroup(Create(l), FadeIn(b, scale=0.6)) for l, b in zip(lines, beads)], lag_ratio=0.25), run_time=1.8)

        def f_several():
            self.play(FadeIn(alt, shift=UP * 0.15), FadeIn(alt_lines), run_time=0.9)

        def f_keep():
            self.play(FadeOut(alt), FadeOut(alt_lines), run_time=0.5)
            self.play(blocks[2][2].animate.set_fill(GOLD, 0.95).set_stroke(GOLD, 3), run_time=0.7)
            self.play(Indicate(beads[2], color=TEXT, scale_factor=1.25), run_time=0.9)

        def f_syn():
            self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.8)

        run_events(self, [(cue(self, "three letters", 0.3), f_group), (cue(self, "The genetic code"), f_code),
                          (cue(self, "several codons", 0.1), f_several), (cue(self, "so some changes", 0.2), f_keep),
                          (cue(self, "These are synonymous", 0.2), f_syn)])
        self.finish()


def codon_alt(x):
    sq = VGroup(*[Square(0.34, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.28) for _ in range(3)])
    sq.arrange(RIGHT, buff=0.04).move_to([x, -2.3, 0])
    return sq


# =============================================================================================
# s04 nonsynonymous change, and the control
# =============================================================================================
class S04Nonsyn(Scn):
    def construct(self):
        self.add(band(-6.3, 6.3, 1.2, 2.4, GREY, 0.14), band(-6.3, 6.3, -1.8, -0.2, AA[0], 0.1))
        blocks = codon_squares()
        beads, lines = beads_and_lines()
        gold_sq(blocks[2][2])
        self.add(*blocks, *lines, *beads)
        lab_s = T("synonymous", 32, TEAL).move_to([BX[2], -2.0, 0])
        lab_n = T("nonsynonymous (replacement): new amino acid", 36, CORAL).move_to([0, -3.1, 0])
        brk = VGroup(Line([BX[2] - 0.9, 2.6, 0], [BX[2] + 0.9, 2.6, 0]), Line([BX[2] - 0.9, 2.6, 0], [BX[2] - 0.9, 2.35, 0]),
                     Line([BX[2] + 0.9, 2.6, 0], [BX[2] + 0.9, 2.35, 0])).set_stroke(TEAL, 6)
        ctl = T("control", 40, TEAL).move_to([BX[2], 3.1, 0])

        def f_flip():
            self.play(blocks[4][1].animate.set_fill(GOLD, 0.95).set_stroke(GOLD, 3), run_time=0.8)
            self.play(beads[4].animate.set_fill(CORAL, 1).scale(1.15), run_time=0.9)
            self.play(Indicate(beads[4], color=TEXT, scale_factor=1.2), run_time=0.7)

        def f_lab():
            self.play(FadeIn(lab_n, shift=UP * 0.1), run_time=0.9)

        def f_syn():
            self.play(Indicate(blocks[2][2], color=TEXT, scale_factor=1.5), FadeIn(lab_s), run_time=1.0)

        def f_ctl():
            self.play(Create(brk), FadeIn(ctl, shift=DOWN * 0.1), run_time=0.9)

        run_events(self, [(0.5, f_flip), (cue(self, "These are non"), f_lab), (cue(self, "synonymous changes are neutral", 0.3), f_syn),
                          (cue(self, "built in control", 0.5), f_ctl)])
        self.finish()


# =============================================================================================
# s05 the counters and omega
# =============================================================================================
class S05Counters(Scn):
    def construct(self):
        rig = Rig()
        self.add(rig.branch, rig.ticks)
        self.play(FadeIn(rig.numN), FadeIn(rig.numS), run_time=0.8)
        S_T = [0.9, 1.5, 2.1, 2.7, 3.3, 3.9, 4.5]
        N_T = [1.2, 2.4, 3.6, 4.8, 6.0]
        ev = [(t, rig.tickS) for t in S_T] + [(t, rig.tickN) for t in N_T]
        self.add(Sched(ev, t0=self.elapsed()))

        def f_per():
            self.play(FadeIn(rig.per, shift=UP * 0.1), run_time=0.7)

        def f_n():
            self.play(FadeIn(rig.labN, shift=RIGHT * 0.1), run_time=0.6)

        def f_s():
            self.play(FadeIn(rig.labS, shift=RIGHT * 0.1), run_time=0.6)

        def f_skel():
            self.play(FadeIn(rig.zones), FadeIn(rig.arc), FadeIn(rig.marks), run_time=1.0)

        def f_dial():
            self.play(FadeIn(rig.hub), FadeIn(rig.needle), run_time=0.8)

        def f_eq():
            self.play(FadeIn(rig.eq, shift=RIGHT * 0.1), run_time=0.7)

        run_events(self, [(cue(self, "per site"), f_per), (3.4, f_skel), (cue(self, "dN"), f_n), (cue(self, "dS"), f_s),
                          (cue(self, "Their ratio", 0.5), f_dial), (cue(self, "omega", 0.4), f_eq)])
        self.finish()


# =============================================================================================
# s06 three runs of the dial
# =============================================================================================
class S06Dial(Scn):
    def construct(self):
        rig = Rig()
        self.add(rig.branch, rig.ticks, rig.numN, rig.numS, rig.labN, rig.labS, rig.per, rig.dial, rig.eq)
        # run 1: replacements lag; run 2: keep pace; run 3: replacements race ahead
        r1s = [0.4 + 0.6 * i for i in range(13)]
        r1n = [2.3, 5.2]
        r2 = [(9.9 + 0.5 * i, rig.tickN if i % 2 else rig.tickS) for i in range(12)]
        r3n = [13.2 + 0.25 * i for i in range(10)]
        r3s = [13.6, 14.4, 15.2]
        ev = [(t, rig.tickS) for t in r1s] + [(t, rig.tickN) for t in r1n] + r2 + [(t, rig.tickN) for t in r3n] + [(t, rig.tickS) for t in r3s]
        ev += [(9.35, rig.reset), (12.95, rig.reset)]
        self.add(Sched(ev, t0=self.elapsed()))
        v = [None]

        def verdict(txt, col):
            def fn():
                new = T(txt, 36, col).move_to([2.0, -3.4, 0])
                v[0] = swap(self, v[0], new)
            return fn

        run_events(self, [(cue(self, "That suggests", 0.1), verdict("purifying selection suggested", RED)),
                          (cue(self, "consistent with", 0.6), verdict("consistent with neutrality", TEXT)),
                          (cue(self, "positive selection", 0.1, nth=0), verdict("positive selection suggested", CORAL))])
        self.finish()


# =============================================================================================
# s07 McDonald & Kreitman
# =============================================================================================
class S07Mk(Scn):
    def construct(self):
        pop = Pop((-4.0, 4.0, -2.7, 2.5), 18, 5, 0.9, lambda T: 3, 0.0, None, True, 0, BLUE)
        lab = T("variation inside a species", 38, TEXT).move_to([0, 3.15, 0])
        self.play(FadeIn(pop), run_time=0.8)
        card = chip("McDonald & Kreitman, Nature, 1991", GOLD, 34).move_to([0, 3.2, 0])
        big = fly(BLUE, 1.6).move_to([-4.3, 0.7, 0])
        bar = gene_bar(14, 0.44, 0.05).move_to([1.9, 0.7, 0])
        bar_lab = T("Adh", 36, GOLD).move_to([1.9, 1.65, 0])
        bar_full = T("Adh (alcohol dehydrogenase)", 36, GOLD).move_to([1.9, 1.65, 0])
        f1, f2, f3 = fly(BLUE, 0.85).move_to([-3.8, -1.8, 0]), fly(GREEN, 0.85).move_to([0, -1.8, 0]), fly("#B58CE6", 0.85).move_to([3.8, -1.8, 0])
        flab = T("three Drosophila species", 36, TEXT).move_to([0, -3.2, 0])
        for f, ph in ((big, 0), (f1, 1), (f2, 2), (f3, 3)):
            wobble(f, 0.05, 1.0, ph)

        def f_var():
            self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.8)

        def f_1991():
            self.play(FadeOut(pop), FadeOut(lab), run_time=0.6)
            self.play(FadeIn(card, shift=DOWN * 0.1), FadeIn(big, shift=UP * 0.2), run_time=0.9)

        def f_adh():
            self.play(FadeIn(bar), FadeIn(bar_lab), run_time=0.8)

        def f_flies():
            self.play(LaggedStart(FadeIn(f1, shift=UP * 0.2), FadeIn(f2, shift=UP * 0.2), FadeIn(f3, shift=UP * 0.2), lag_ratio=0.3), run_time=1.2)
            self.play(FadeIn(flab, shift=UP * 0.1), run_time=0.7)

        def f_full():
            self.play(Transform(bar_lab, bar_full), run_time=0.8)

        run_events(self, [(cue(self, "variation inside"), f_var), (cue(self, "1991", 0.3), f_1991), (cue(self, "ADH", 0.2), f_adh),
                          (cue(self, "fruit flies", 0.2), f_flies), (cue(self, "alcohol dehydrogenase", 0.2), f_full)])
        self.finish()


# =============================================================================================
# s08 the table
# =============================================================================================
class S08Table(Scn):
    def construct(self):
        tb = Table()
        self.play(Create(tb.outer), run_time=1.0)
        self.play(Create(tb.lines), run_time=1.2)

        def f_cols():
            self.play(FadeIn(tb.fillC), FadeIn(tb.fillS), FadeIn(tb.tints), run_time=0.8)

        def f_c():
            self.play(FadeIn(tb.txtC, shift=DOWN * 0.1), run_time=0.7)

        def f_s():
            self.play(FadeIn(tb.txtS, shift=DOWN * 0.1), run_time=0.7)

        def row(r, lab):
            def fn():
                fr = row_frame(r)
                self.play(Create(fr), run_time=0.7)
                self.play(FadeIn(lab, shift=RIGHT * 0.1), run_time=0.7)
                self.play(FadeOut(fr), run_time=0.5)
            return fn

        run_events(self, [(cue(self, "The columns"), f_cols), (cue(self, "replacement", 0.1), f_c), (cue(self, "synonymous", 0.1), f_s),
                          (cue(self, "One row holds", 0.2), row(0, tb.r1)), (cue(self, "The other holds", 0.2), row(1, tb.r2))])
        self.finish()


# =============================================================================================
# s09 the neutral logic
# =============================================================================================
class S09Logic(Scn):
    def construct(self):
        ks1 = [0, 1, 1, 2, 3, 5, 8, 12, 16]
        ks2 = [2, 1, 1, 0]

        def g1(T):
            if T < 1.7:
                return 0
            return ks1[min(len(ks1) - 1, 1 + int((T - 1.7) / 0.45))]

        pop1 = Pop((-3.2, 3.2, -2.5, 2.3), 16, 3, 0.45, g1, 0.0, None, True, 0, BLUE)
        self.play(FadeIn(pop1), run_time=0.6)
        lab = [None]

        def say(txt, col):
            def fn():
                lab[0] = swap(self, lab[0], T(txt, 40, col).move_to([0, 3.2, 0]))
            return fn

        def loss():
            pop2 = Pop((-3.2, 3.2, -2.5, 2.3), 16, 9, 0.45, lambda T: ks2[min(3, int(T / 0.45))], 0.0, None, True, 0, BLUE)
            self.play(FadeOut(pop1), FadeIn(pop2), run_time=0.4)
            self.pop2 = pop2
            lab[0] = swap(self, lab[0], T("or lost", 40, GREY if False else TEXT).move_to([0, 3.2, 0]))

        tb = Table()
        tags = VGroup(T("ratio", 34, TEXT).move_to([5.8, CY[0], 0]), T("ratio", 34, TEXT).move_to([5.8, CY[1], 0]))
        eq = M("=", 90, GOLD).move_to([5.8, 0.15, 0])
        arrow = Arrow([-4.75, 0.7, 0], [-4.75, -0.4, 0], color=GOLD, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.35)
        exp = T("neutral expectation: same ratio", 38, GOLD).move_to([TCX, -2.9, 0])

        def to_table():
            self.play(FadeOut(self.pop2), FadeOut(lab[0]), run_time=0.5)
            self.play(FadeIn(tb.all()), run_time=0.9)

        def f_arrow():
            self.play(GrowArrow(arrow), run_time=0.8)

        def f_ratio():
            self.play(FadeIn(tags), FadeIn(eq, scale=0.7), run_time=0.9)

        def f_exp():
            self.play(FadeIn(exp, shift=UP * 0.1), run_time=0.9)

        run_events(self, [(0.3, say("a species", BLUE)), (cue(self, "variant within"), say("a new variant", GOLD)),
                          (cue(self, "passing stage"), say("a passing stage", TEXT)), (cue(self, "fixation", 0.3), say("fixed", GOLD)),
                          (cue(self, "loss", 0.3), loss), (cue(self, "So both rows", 0.1), to_table), (cue(self, "both rows", -0.5), f_arrow),
                          (cue(self, "same ratio", 0.1), f_ratio), (cue(self, "of replacement", 0.1), f_exp)])
        self.finish()


# =============================================================================================
# s10 predict: the variants row fills first
# =============================================================================================
class S10Predict(Scn):
    def construct(self):
        tb = Table()
        self.add(tb.all())
        q = qmarks()
        fr = row_frame(0)
        fr2 = glow(row_frame(1))

        def f_row():
            self.play(Create(fr), run_time=0.6)
            count_to(self, 0, 0, 2, CORAL, 1.0)

        def f_syn():
            count_to(self, 0, 1, 42, TEAL, 1.6)

        def f_q():
            self.play(FadeOut(fr), FadeIn(q, scale=0.6), run_time=0.8)

        def f_look():
            self.play(Create(fr2), run_time=0.7)

        run_events(self, [(0.4, f_row), (cue(self, "mostly synonymous", 0.3), f_syn), (cue(self, "If replacements", 0.1), f_q),
                          (cue(self, "what should", 0.1), f_look)])
        self.finish()


# =============================================================================================
# s11 the pause
# =============================================================================================
class S11Pause(Scn):
    def construct(self):
        tb = Table()
        self.add(tb.all(), num_at(2, CORAL, 0, 0), num_at(42, TEAL, 0, 1))
        q = qmarks()
        fr2 = glow(row_frame(1))
        cap = T("Predict: what ratio in the fixed row?", 40, GOLD).move_to([TCX, -2.9, 0])
        cx = np.array([5.8, 0.7, 0.0])
        ring = Circle(radius=0.6, color=TEXT, stroke_width=5).move_to(cx)
        arc = Arc(radius=0.6, start_angle=PI / 2, angle=-TAU, color=GOLD, stroke_width=11, arc_center=cx)
        arc.t = 0.0
        num = M("5", 40, GOLD).move_to(cx)
        num.k = 5

        def f(m, dt):
            m.t += dt
            frac = max(0.02, 1 - m.t / 5.0)
            m.become(Arc(radius=0.6, start_angle=PI / 2, angle=-TAU * frac, color=GOLD, stroke_width=11, arc_center=cx))
        arc.add_updater(f)

        def g(m, dt):
            k = max(1, math.ceil(5 - arc.t))
            if k != m.k:
                m.k = k
                m.become(M(str(k), 40, GOLD).move_to(cx))
        num.add_updater(g)
        self.add(q, fr2, cap, ring, arc, num)
        self.finish()


# =============================================================================================
# s12 reveal
# =============================================================================================
class S12Reveal(Scn):
    def construct(self):
        tb = Table()
        self.add(tb.all(), num_at(2, CORAL, 0, 0), num_at(42, TEAL, 0, 1))
        ghost = VGroup(M("≈1", 84, CORAL), M("≈23", 84, TEAL))
        ghost[0].move_to([CX[0], CY[1], 0])
        ghost[1].move_to([CX[1], CY[1], 0])
        ghost.set_opacity(0.45)
        tag = T("if neutral", 30, TEXT).move_to([5.8, CY[1], 0])
        tag2 = T("observed", 30, GOLD).move_to([5.8, CY[1], 0])
        cmp_ = M("7/17 against 2/42", 44, TEXT).move_to([TCX, -2.65, 0])
        exc = T("excess fixed replacements", 34, CORAL).move_to([TCX, -3.35, 0])
        adapt = T("suggested: adaptive fixation", 42, GOLD).move_to([TCX, -2.9, 0])
        cf = glow(cell_frame(1, 0, CORAL, 7))
        real = []

        def f_ghost():
            self.play(FadeIn(ghost, shift=UP * 0.1), FadeIn(tag), run_time=0.9)

        def f_real():
            self.play(FadeOut(ghost), FadeOut(tag), FadeIn(tag2), run_time=0.5)
            real.append(count_to(self, 1, 0, 7, CORAL, 1.1))
            real.append(count_to(self, 1, 1, 17, TEAL, 1.3))

        def f_more():
            self.play(Create(cf), run_time=0.6)
            self.play(FadeIn(cmp_, shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(exc, shift=UP * 0.1), run_time=0.8)

        def f_adapt():
            self.play(FadeOut(cmp_), FadeOut(exc), run_time=0.5)
            self.play(FadeIn(adapt, shift=UP * 0.1), run_time=0.9)

        run_events(self, [(cue(self, "same ratio", 0.1), f_ghost), (cue(self, "Instead"), f_real), (cue(self, "more replacements", 0.3), f_more),
                          (cue(self, "suggested this", 0.4), f_adapt)])
        self.finish()


# =============================================================================================
# s13 each is the other's control
# =============================================================================================
class S13Control(Scn):
    def construct(self):
        tb, nums = full_table_with_counts(self)
        a1 = Arrow([-0.9, -2.28, 0], [2.7, -2.28, 0], color=TEXT, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow([2.7, -2.48, 0], [-0.9, -2.48, 0], color=TEXT, stroke_width=6, buff=0, max_tip_length_to_length_ratio=0.3)
        lab = T("each is the other's control", 34, TEAL).move_to([TCX, -2.86, 0])
        clk = VGroup(clock_icon().scale(0.55), T("clock", 26, TEXT)).arrange(RIGHT, buff=0.25).move_to([TCX - 2.2, -3.55, 0])
        stn = VGroup(stone_icon().scale(0.55), T("dated split", 26, TEXT)).arrange(RIGHT, buff=0.25).move_to([TCX + 2.2, -3.55, 0])
        x1, x2 = cross(clk[0]), cross(stn[0])

        def f_a1():
            self.play(GrowArrow(a1), run_time=0.6)

        def f_a2():
            self.play(GrowArrow(a2), run_time=0.6)

        def f_lab():
            self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.8)

        def f_clock():
            self.play(FadeIn(clk, shift=UP * 0.1), run_time=0.5)
            self.play(Create(x1), run_time=0.5)

        def f_stone():
            self.play(FadeIn(stn, shift=UP * 0.1), run_time=0.5)
            self.play(Create(x2), run_time=0.5)

        run_events(self, [(cue(self, "each kind", 0.1), f_a1), (cue(self, "of change is", 0.2), f_a2), (cue(self, "the control", 0.5), f_lab),
                          (cue(self, "no clock", 0.3), f_clock), (cue(self, "no dated split", 0.3), f_stone)])
        self.finish()


# =============================================================================================
# s14 hedge
# =============================================================================================
class S14Hedge(Scn):
    def construct(self):
        tb, nums = full_table_with_counts(self)
        cf = glow(cell_frame(1, 0, CORAL, 7))
        self.add(cf)
        l1 = T("model inference", 42, TEXT).move_to([TCX - 1.9, -2.9, 0])
        l2 = T("can fail", 42, RED).move_to([TCX + 1.6, -2.9, 0])
        stamp = VGroup(RoundedRectangle(corner_radius=0.15, width=6.3, height=1.3, stroke_color=GOLD, stroke_width=9),
                       T("statistical signal", 46, GOLD)).rotate(0.12).move_to([-1.0, 0.6, 0])
        head = T("further checks", 42, GOLD).move_to([0.7, 3.2, 0], aligned_edge=LEFT)
        items = ["alignment", "orthology", "mutation model", "synonymous sites neutral?", "function test"]
        rows = VGroup()
        for i, it in enumerate(items):
            box = Square(0.42, stroke_color=TEXT, stroke_width=4, fill_opacity=0)
            tx = T(it, 32, TEXT)
            r = VGroup(box, tx).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN)
            r.move_to([0, 2.2 - 1.15 * i, 0])
            r.shift(RIGHT * (0.7 - r.get_left()[0]))
            rows.add(r)

        def f_l1():
            self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.7)

        def f_l2():
            self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.7)

        def f_stamp():
            stamp.scale(1.8)
            self.play(FadeOut(l1), FadeOut(l2), FadeIn(stamp), VGroup(tb.all(), *nums, cf).animate.set_opacity(0.15), run_time=0.1)
            self.play(stamp.animate.scale(1 / 1.8), run_time=0.45, rate_func=rush_into)
            self.play(Indicate(stamp, color=TEXT, scale_factor=1.06), run_time=0.5)

        def f_check():
            self.play(FadeOut(VGroup(tb.all(), *nums, cf)), stamp.animate.move_to([-3.4, 0.0, 0]), run_time=1.0)
            self.play(FadeIn(head, shift=LEFT * 0.1), run_time=0.5)

        def item(i):
            def fn():
                self.play(FadeIn(rows[i], shift=LEFT * 0.2), run_time=0.5)
            return fn

        evs = [(cue(self, "model inferences", 0.3), f_l1), (cue(self, "can fail", 0.3), f_l2), (cue(self, "A signal", 0.1), f_stamp),
               (cue(self, "further checks", 0.5), f_check)]
        for i, t in enumerate((0.0, 0.7, 1.4, 2.1, 2.8)):
            evs.append((cue(self, "further checks", 0.5) + 1.7 + t, item(i)))
        run_events(self, evs)
        self.finish()


# =============================================================================================
# s15 close: the tree and the two tracks
# =============================================================================================
class S15Close(Scn):
    def construct(self):
        tree = make_tree(B_TICKS, G_TICKS)
        T_S = [1.4 + 0.85 * i for i in range(11)]
        T_C = [1.6, 2.5, 3.4, 4.3, 5.2]
        tc = TTrack(1.9, 5.0, 1.9, CORAL, T_C, 1.0, 9.6, th=1.1, num_x=5.95)
        ts = TTrack(1.9, 5.0, -0.5, TEAL, T_S, 1.0, 9.6, th=1.1, num_x=5.95)
        lc = T("kind 1", 34, CORAL).move_to([3.5, 2.95, 0])
        ls = T("kind 2", 34, TEAL).move_to([3.5, 0.55, 0])
        q1 = T("keep pace with", 38, TEXT).move_to([3.6, -1.9, 0])
        q2 = T("the neutral count?", 38, TEXT).move_to([3.6, -2.5, 0])
        clue = T("clue to selection, not proof", 34, GOLD).move_to([3.3, -3.3, 0])
        self.add(band(1.5, 6.9, 1.2, 2.6, CORAL), band(1.5, 6.9, -1.2, 0.2, TEAL), tc, ts)
        self.play(FadeIn(tree), run_time=1.0)

        def f_k():
            self.play(FadeIn(lc), FadeIn(ls), run_time=0.7)

        def f_q():
            self.play(FadeIn(q1, shift=UP * 0.1), FadeIn(q2, shift=UP * 0.1), run_time=0.9)

        def f_clue():
            self.play(FadeOut(q1), FadeOut(q2), run_time=0.4)
            self.play(FadeIn(clue, shift=UP * 0.1), run_time=0.9)

        run_events(self, [(cue(self, "same question"), f_k), (cue(self, "keep pace", 0.3), f_q), (cue(self, "A departure", 0.2), f_clue)])
        self.finish()


# =============================================================================================
# s16 end card
# =============================================================================================
class S16End(EndCard):
    LINE = "A departure from the neutral count is a clue to selection."
