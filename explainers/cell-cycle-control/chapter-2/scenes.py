"""A Snapshot of the Cycle (chapter 2): which phase is each cell in?
COLOR MAP (chapter 1's, plus two stains): GREEN CDK activity; TEAL DNA / nuclear glow; GREY cell, nucleus,
chromosomes; RED destruction; YELLOW EdU (S phase); MAGENTA phospho-H3 (mitosis-enriched).
Dish, histogram, cytometer and records are schematic; the histogram is computed from stated area shares
(55% under the 2C peak, 25% S bridge, 20% under the 4C peak). No molecular structures are drawn.
"""
import math, random
from bp_style import *

ORANGE = "#F29E4C"
MAGENTA = "#E05CCB"
HOMA = "#7FB2FF"
HOMB = "#C792EA"
TINT = "#8FE3E8"
C = np.array([-3.25, -0.2, 0.])
NC = C + UP * .35
X0, X1 = 0.6, 6.1
CG, CT, CM = ManimColor(GREY), ManimColor(TEAL), ManimColor(MAGENTA)

# histogram geometry: fluorescence 0..2.6 (2C at 1, 4C at 2) mapped to the screen
HX0, HK, BASE, HS = -0.2, 2.55, -2.7, 1.35


def hx(fl):
    return HX0 + HK * fl


def dens(f):
    g = lambda m, sd: math.exp(-.5 * ((f - m) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
    bridge = .5 * (math.erf((f - 1.1) / .04) - math.erf((f - 1.9) / .04)) / .8
    return .55 * g(1, .06) + .20 * g(2, .065) + .25 * bridge


def lab(s, p, color=TEXT, size=30, w=12.4):
    return fit(T(s, size=size, color=color), max_w=w).move_to(p)


def clamp(x, a=0., b=1.):
    return max(a, min(b, x))


# ---------------------------------------------------------------- the dish of frozen cells
class Dish:
    RC, NR = .115, .55

    def __init__(self, scene, cx, cy, s, run=0, advance=2.9, **st):
        self.t = 0.0
        V = ValueTracker
        self.cx, self.cy, self.s = V(cx), V(cy), V(s)
        v = dict(run=run, vis=1, glow=0, haze=0, edu=0, click=0, ph=0, cls=0, dp=0)
        v.update(st)
        for k, x in v.items():
            setattr(self, k, V(x))
        rng = random.Random(7)
        a = .27
        pts = []
        for r in range(-5, 6):
            for c in range(-5, 6):
                x, y = (c + (.5 if r % 2 else 0)) * a, r * a * .866
                if math.hypot(x, y) <= .9:
                    pts.append((x + rng.uniform(-.015, .015), y + rng.uniform(-.015, .015)))
        n = len(pts)
        cats = [(0, .5)] * round(n * .5) + [(.5, .77)] * round(n * .27) + [(.77, .88)] * round(n * .12)
        cats += [(.88, 1)] * (n - len(cats))
        rng.shuffle(cats)
        self.cells = []
        self.rim = Circle(radius=1, color=GREY, stroke_width=4)
        mobs = [self.rim]
        for (x, y), (lo, hi) in zip(pts, cats):
            u = rng.uniform(lo, hi)
            sp = rng.uniform(.6, 1.4)
            c = dict(x=x, y=y, u=u, a=u + advance * .07 * sp, sp=sp, ph=rng.uniform(0, 6.28),
                     body=Circle(radius=1, stroke_width=2.5), nuc=Circle(radius=1, stroke_width=1.5),
                     dot=Dot(radius=.05, color=TEXT), speck=Dot(radius=.05, color=YELLOW),
                     halo=Dot(radius=.05, color=YELLOW), ring=Circle(radius=1, stroke_width=3))
            self.cells.append(c)
            mobs += [c["body"], c["nuc"], c["halo"], c["speck"], c["ring"], c["dot"]]
        self.g = VGroup(*mobs)
        self.g.add_updater(self.update)
        scene.add(self.s, self.vis, self.g)
        self.update(self.g, 0)

    @staticmethod
    def amt(u):
        return 2 if u < .5 else (2 + 2 * (u - .5) / .27 if u < .77 else 4)

    def pos(self, i):
        c = self.cells[i]
        return np.array([self.cx.get_value() + self.s.get_value() * c["x"], self.cy.get_value() + self.s.get_value() * c["y"], 0.])

    def nearest(self, x, y):
        return min(range(len(self.cells)), key=lambda i: (self.cells[i]["x"] - x) ** 2 + (self.cells[i]["y"] - y) ** 2)

    def pick(self, lo, hi, k=0):
        return [i for i, c in enumerate(self.cells) if lo <= c["u"] < hi][k]

    def update(self, m, dt):
        self.t += dt
        t = self.t
        cx, cy, s = self.cx.get_value(), self.cy.get_value(), self.s.get_value()
        vis, run, glow, haze = self.vis.get_value(), self.run.get_value(), self.glow.get_value(), self.haze.get_value()
        edu, click, ph, cls, dp = self.edu.get_value(), self.click.get_value(), self.ph.get_value(), self.cls.get_value(), self.dp.get_value()
        self.rim.set_width(2 * s).move_to([cx, cy, 0])
        self.rim.set_stroke(GREY, 4, opacity=.9 * vis).set_fill(GREY, opacity=.04 * vis)
        for c in self.cells:
            u = c["u"]
            k = 1 + .035 * math.sin(.9 * t + c["ph"])
            px = cx + s * c["x"] + s * .012 * math.sin(.5 * t + 2 * c["ph"])
            py = cy + s * c["y"] + s * .012 * math.cos(.4 * t + c["ph"])
            R = self.RC * s * k
            b = c["body"]
            b.set_width(2 * R).move_to([px, py, 0])
            b.set_stroke(GREY, 2.5, opacity=.9 * vis)
            b.set_fill(interpolate_color(CG, CT, haze), opacity=vis * (.07 + .22 * haze))
            n = c["nuc"]
            n.set_width(2 * R * self.NR).move_to([px, py, 0])
            a = self.amt(u)
            pv = ph if u >= .86 else 0
            n.set_stroke(interpolate_color(CG, CM, pv), 1.5 + 3 * pv, opacity=.85 * vis)
            n.set_fill(TEAL, opacity=vis * (.05 + glow * (.15 + .55 * (a - 2) / 2)))
            c["a"] += dt * run * .07 * c["sp"]
            ang = 2 * math.pi * c["a"]
            d = c["dot"]
            d.set_width(max(.09, .05 * s) * (1 + .9 * dp)).move_to([px + R * math.cos(ang), py + R * math.sin(ang), 0])
            d.set_fill(TEXT, opacity=vis).set_stroke(width=0)
            inS = .5 <= u < .77
            sp_, ha = c["speck"], c["halo"]
            sp_.set_width(.3 * R).move_to([px + .1 * R, py - .05 * R, 0]).set_fill(YELLOW, opacity=vis * edu * .95 * inS).set_stroke(width=0)
            ha.set_width(1.0 * R).move_to([px + .1 * R, py - .05 * R, 0]).set_fill(YELLOW, opacity=vis * click * .45 * inS).set_stroke(width=0)
            col = TEXT if u < .5 else (YELLOW if u < .77 else (TEAL if u < .88 else MAGENTA))
            r_ = c["ring"]
            r_.set_width(2.7 * R).move_to([px, py, 0]).set_stroke(col, 3, opacity=.95 * vis * cls).set_fill(opacity=0)


# ---------------------------------------------------------------- histogram pieces
class Bars:
    def __init__(self):
        self.rects, self.cat, self.c = [], [], []
        for i in range(49):
            c = .075 + .05 * i
            h = dens(c) * HS
            if h < .015:
                continue
            r = Rectangle(width=.05 * HK * .92, height=h, stroke_width=1).move_to([hx(c), BASE + h / 2, 0])
            self.rects.append(r)
            self.c.append(c)
            self.cat.append("L" if c < 1.2 else ("R" if c > 1.8 else "M"))
        self.g = VGroup(*self.rects)
        self.paint()

    def paint(self, L=TEAL, R=TEAL, M=TEAL, lo=.55, ro=.55, mo=.5):
        for r, k in zip(self.rects, self.cat):
            col, op = {"L": (L, lo), "R": (R, ro), "M": (M, mo)}[k]
            r.set_fill(col, opacity=op).set_stroke(col, 2, opacity=1)

    def sel(self, lo, hi):
        return [r for r, c in zip(self.rects, self.c) if lo <= c <= hi]

    def at(self, fl):
        return min(zip(self.rects, self.c), key=lambda z: abs(z[1] - fl))[0]


def hist_axes(ticks=True, yaxis=False):
    g = VGroup(Line([-.4, BASE, 0], [6.4, BASE, 0], color=GREY, stroke_width=3))
    if yaxis:
        g.add(Line([-.4, BASE, 0], [-.4, 2.7, 0], color=GREY, stroke_width=3))
    if ticks:
        g.add(lab("2C", [hx(1), BASE - .35, 0], TEAL, 28), lab("4C", [hx(2), BASE - .35, 0], TEAL, 28))
    return g


def quantiles(n):
    grid = np.linspace(.03, 2.6, 800)
    cdf = np.cumsum([dens(x) for x in grid])
    cdf /= cdf[-1]
    return [float(grid[np.searchsorted(cdf, (i + .5) / n)]) for i in range(n)]


def wavy(cx, cy, half, ph=0., color=TEAL, w=4):
    xs = np.linspace(-half, half, 24)
    m = VMobject(color=color, stroke_width=w)
    m.set_points_smoothly([[cx + x, cy + .05 * math.sin(6 * x + ph), 0] for x in xs])
    return m


def xshape(c, size=.5, color=GREY, w=8):
    c = np.array(c, dtype=float)
    return VGroup(Line(c + [-.18 * size, .5 * size, 0], c + [.18 * size, -.5 * size, 0], color=color, stroke_width=w),
                  Line(c + [.18 * size, .5 * size, 0], c + [-.18 * size, -.5 * size, 0], color=color, stroke_width=w))


# ---------------------------------------------------------------- scenes with the dish at left and a histogram at right
LC = np.array([-4.2, -0.1, 0.])


class HScene(SpokenScene):
    def dish_left(self, **st):
        self.d = Dish(self, -4.35, -.2, 2.4, **st)
        return self.d

    def hist(self, tint=True, axes=True, yaxis=False, ill=True, xlab=None, ylab=False, add=True):
        self.bars = Bars()
        if tint:
            self.bars.paint(L=TINT, R=TINT, M=TEAL, lo=.9, ro=.9, mo=.65)
        self.ax = hist_axes(True, yaxis)
        self.illus = lab("illustrative numbers", [5.0, 3.45, 0], GREY, 28)
        parts = [self.bars.g]
        if axes:
            parts.append(self.ax)
        if ill:
            parts.append(self.illus)
        self.xl = lab(xlab, [3.0, -3.55, 0], TEXT, 28) if xlab else None
        self.yl = lab("number of cells", [-1.0, -.1, 0], TEXT, 28).rotate(PI / 2) if ylab else None
        for p in parts + [self.xl, self.yl]:
            if p is not None and add:
                self.add(p)

    def lifted(self, panel=True, chrom=False):
        body = Circle(radius=2.2, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.06).move_to(LC)
        nuc = Circle(radius=1.05, color=GREY, stroke_width=3, fill_color=TEAL, fill_opacity=.5).move_to(LC)
        g = VGroup(body, nuc)
        self.cbody, self.cnuc = body, nuc
        self.panel = RoundedRectangle(width=2.3, height=2.3, corner_radius=.3, stroke_color=TEXT, stroke_width=2,
                                      stroke_opacity=.4, fill_color="#8A94A8", fill_opacity=.55).move_to(LC)
        self.chrom = VGroup(*[xshape(LC + [dx * .42, dy * .42, 0], 1.0) for dx in (-1, 1) for dy in (-1, 1)])
        self.chrom.set_stroke(opacity=0 if not chrom else 1)
        g.add(self.chrom)
        if panel:
            g.add(self.panel)
        return g

    def breathe(self, mob, amp=.025):
        w = mob.width
        t = ValueTracker(0)
        t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t)
        mob.add_updater(lambda m: m.set_width(w * (1 + amp * math.sin(t.get_value() * .9))))

    def channel(self):
        ch = RoundedRectangle(width=.6, height=3.3, corner_radius=.2, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.12).move_to([5.95, 1.25, 0])
        beam = Line([5.45, 1.1, 0], [6.45, 1.1, 0], color=TEXT, stroke_width=3)
        return VGroup(ch, beam, lab("flow cytometer", [5.2, -.8, 0], TEXT, 28))

    def send(self, d, i, fl, op, rt=1.6):
        start = d.pos(i)
        B = np.array([5.95, 1.1, 0.])
        trav = VGroup(Circle(radius=.28, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.1),
                      Circle(radius=.15, stroke_width=0, fill_color=TEAL, fill_opacity=op)).move_to(start)
        path = VMobject().set_points_as_corners([start, [5.95, 3.05, 0], B])
        flash = Circle(radius=.3, stroke_width=0, fill_color=TEXT, fill_opacity=.9 if op > .5 else .6).move_to(B)
        dot = Dot([5.95, 1.1, 0], radius=.1, color=TEAL).set_opacity(1)
        tgt = np.array([hx(fl), BASE + .12, 0.])
        return Succession(FadeIn(trav, run_time=.15),
                          MoveAlongPath(trav, path, run_time=rt, rate_func=linear),
                          FadeIn(flash, run_time=.1), FadeOut(flash, run_time=.25),
                          FadeIn(dot, run_time=.05),
                          AnimationGroup(MoveAlongPath(trav, Line(B, B + DOWN * 1.2)), FadeOut(trav),
                                         MoveAlongPath(dot, Line(B, tgt)), run_time=.9))


# ---------------------------------------------------------------- the chapter-1 world (cell + record)
GB, TB, MB = (1.55, 2.25), (0., .95), (-1.5, -.8)
GREEN_CYCLE = [(0, .02), (.67, .02), (.69, .9), (.88, .9), (.89, .02), (1, .02)]
TEAL_CYCLE = [(0, .5), (.25, .5), (.5, 1), (.88, 1), (.89, .5), (1, .5)]


def level(u):
    return .5 if u < .25 else (.5 + .5 * (u - .25) / .25 if u < .5 else (1 if u < .885 else .5))


def band(points, y0, y1):
    return [[X0 + (X1 - X0) * x, y0 + (y1 - y0) * v, 0] for x, v in points]


class WorldScene(SpokenScene):
    def world(self, bands=True):
        self.pos = ValueTracker(0)
        self.hi = ValueTracker(0)
        self.hi.add_updater(lambda m, dt: m.set_value(max(m.get_value(), self.pos.get_value())))
        self.add(self.pos, self.hi)
        self.cell = Circle(radius=2.55, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.055).move_to(C)
        self.nuc = Circle(radius=1.15, color=GREY, stroke_width=3, fill_opacity=.04).move_to(NC)
        self.A = VGroup(*[wavy(NC[0], NC[1] + y, .65, j) for j, y in enumerate([-.5, -.25, 0])])
        self.B = VGroup(*[wavy(NC[0], NC[1] + y, .65, j + 2) for j, y in enumerate([.25, .5, .75])])
        self.halo = Arc(radius=2.55, start_angle=.3, angle=1.1, color=TEXT, stroke_width=7).move_arc_center_to(C)
        self.halo.add_updater(lambda m, dt: m.rotate(dt * .16, about_point=C))
        self.sy = [-1.8, 1.7]
        self.scrub = always_redraw(lambda: Line([X0 + self.pos.get_value() * (X1 - X0), self.sy[0], 0],
                                                [X0 + self.pos.get_value() * (X1 - X0), self.sy[1], 0], color=TEXT, stroke_width=2))
        self.add(self.cell, self.nuc, self.A, self.halo)

    def axes(self, banded):
        if banded:
            return VGroup(Line([X0, -1.6, 0], [X1 + .15, -1.6, 0], color=GREY), Line([X0, -1.6, 0], [X0, 2.4, 0], color=GREY),
                          lab("time →", [5.25, -2.0, 0]), lab("schematic", [1.7, -2.0, 0], GREY, 28))
        return VGroup(Line([X0, -1.8, 0], [X1 + .15, -1.8, 0], color=GREY), Line([X0, -1.8, 0], [X0, 1.7, 0], color=GREY),
                      lab("time →", [5.25, -2.2, 0]), lab("schematic", [1.7, 2.12, 0], GREY, 28))

    def prog(self, points, color, y0, y1, w=6, src="hi"):
        m = VMobject(color=color, stroke_width=w)
        trk = self.hi if src == "hi" else self.pos

        def up(mob):
            u = trk.get_value()
            pts = []
            for a, b in zip(points, points[1:]):
                if a[0] <= u:
                    pts.append(a)
                if a[0] <= u < b[0]:
                    f = (u - a[0]) / (b[0] - a[0])
                    pts.append((u, a[1] + f * (b[1] - a[1])))
                    break
            if u >= points[-1][0]:
                pts.append(points[-1])
            if len(pts) < 2:
                pts = [points[0], (points[0][0] + .001, points[0][1])]
            mob.set_points_as_corners(band(pts, y0, y1))
        m.add_updater(up)
        up(m)
        return m

    def b_tie(self):
        self.B.add_updater(lambda m: m.set_stroke(opacity=clamp((level(min(self.pos.get_value(), .885)) - .5) * 2) if self.pos.get_value() < .89 else 0))

    def to_world(self, d, k, tgt_nuc=True):
        """One dish cell enlarges into the chapter-1 world in the same place."""
        hero = VGroup(Circle(radius=d.RC * d.s.get_value(), color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.06),
                      Circle(radius=d.RC * d.s.get_value() * .55, color=GREY, stroke_width=2, fill_color=TEAL, fill_opacity=.4)).move_to(d.pos(k))
        self.add(hero)
        target = VGroup(self.cell, self.nuc)
        return hero, target


# ================================================================= scenes
class S00Link(SpokenScene):
    def construct(self):
        d = Dish(self, 0, -.45, 3.1, run=1, advance=0)
        d.s.add_updater(lambda m, dt: m.increment_value(dt * .0185))
        q = lab("Which phase is each cell in?", [0, 3.4, 0], TEXT, 44)
        self.play(FadeIn(q), run_time=.4)
        self.at("freeze")
        d.run.set_value(0)
        fl = Circle(radius=3.4, stroke_width=0, fill_color=TEXT, fill_opacity=.4).move_to([0, -.45, 0])
        self.add(fl)
        self.play(fl.animate.set_fill(opacity=0).scale(1.08), run_time=.8)
        self.remove(fl)
        self.at("carries")
        self.play(d.dp.animate.set_value(1), run_time=.6)
        self.play(d.dp.animate.set_value(0), run_time=.8)
        self.finish()


class S01Question(WorldScene):
    def construct(self):
        d = Dish(self, 0, -.45, 3.25, run=0, advance=2.9)
        self.world()
        self.remove(self.cell, self.nuc, self.A, self.halo)
        k = d.nearest(-.55, 0)
        hero, target = self.to_world(d, k)
        axf = self.axes(False)
        self.at("chapter")
        self.play(d.vis.animate.set_value(0), Transform(hero, target), run_time=1.1)
        self.remove(d.g, hero)
        self.add(self.cell, self.nuc, self.halo)
        self.play(FadeIn(self.A), Create(axf), run_time=.4)
        g = self.prog(GREEN_CYCLE, GREEN, -1.8, 1.7)
        self.add(g, self.scrub)
        gl = lab("CDK activity", [4.3, 2.65, 0], GREEN)
        self.at("kinase")
        self.play(self.pos.animate.set_value(1), run_time=1.9, rate_func=linear)
        self.play(FadeIn(gl), run_time=.5)
        cnt = lab("copies this cycle: 1", [-3.25, -3.3, 0], TEAL)
        self.at("copied")
        self.play(FadeIn(self.B), FadeIn(cnt), run_time=.8)
        # DNA per cell joins the record: make room, then draw it under the green trace
        self.at("doubles")
        g.clear_updaters()
        gs = VMobject(color=GREEN, stroke_width=6).set_points_as_corners(band(GREEN_CYCLE, *GB))
        axb = self.axes(True)
        tl = lab("DNA per cell", [1.95, 1.9, 0], TEAL)
        ticks = VGroup(lab("2C", [.22, TB[1] * .5, 0], TEAL, 28), lab("4C", [.22, TB[1], 0], TEAL, 28))
        self.pos.set_value(0)
        self.hi.set_value(0)
        self.sy = [-1.6, 2.4]
        tr = self.prog(TEAL_CYCLE, TEAL, *TB)
        self.add(tr)
        self.play(Transform(g, gs), Transform(axf, axb), FadeIn(tl), FadeIn(ticks), run_time=.8)
        self.b_tie()
        self.play(self.pos.animate.set_value(.885), run_time=1.6, rate_func=linear)
        self.pos.set_value(.89)
        # division: the right daughter slides off-frame, the left remains
        self.at("then halves")
        self.halo.clear_updaters()
        self.B.clear_updaters()
        self.remove(self.halo)
        for m in (self.B[0], self.B[1], self.B[2]):
            m.set_stroke(opacity=1)
        left = Ellipse(width=2.4, height=4.5, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.055).move_to(C + LEFT * 1.2)
        right = Ellipse(width=2.4, height=4.5, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.055).move_to(C + RIGHT * 1.2)
        self.play(FadeOut(cnt), Transform(self.cell, VGroup(left, right)), self.nuc.animate.scale(.6).shift(LEFT * 1.2),
                  self.A.animate.scale(.6).shift(LEFT * 1.2), self.B.animate.scale(.6).shift(RIGHT * 1.2), run_time=.9)
        self.play(VGroup(self.B, right).animate.shift(DOWN * 5).set_opacity(0),
                  Transform(self.cell, Circle(radius=2.55, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.055).move_to(C)),
                  self.nuc.animate.scale(1 / .6).shift(RIGHT * 1.2), self.A.animate.scale(1 / .6).shift(RIGHT * 1.2),
                  run_time=1.1)
        self.finish()


class S02Title(TitleCard):
    TITLE = "A Snapshot of the Cycle"
    LESSON = "Cyclin-CDK Control of the Cell Cycle"

    def construct(self):
        d = Dish(self, 0, -.45, 3.25, run=0, advance=2.9)
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), size=22, color=TEXT)
        title = fit(T(self.TITLE, size=54, font=TITLE_FONT), max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=.32)
        self.play(d.vis.animate.set_value(.12), FadeIn(g), run_time=.9)
        self.wait(.7)
        self.play(FadeOut(g), run_time=.4)
        self.finish()


def cell_row(cx, kind):
    """A cell (G1, S or G2) at x=cx with schematic teal DNA in its nucleus."""
    body = Circle(radius=1.55, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.06).move_to([cx, .75, 0])
    nuc = Circle(radius=.95, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.05).move_to([cx, .75, 0])
    ys = {"G1": [-.12, .12], "S": [-.24, 0, .24], "G2": [-.36, -.12, .12, .36]}[kind]
    half = .58
    dna = VGroup(*[wavy(cx, .75 + y, half * (.5 if (kind == "S" and j == 2) else 1), j) for j, y in enumerate(ys)])
    return VGroup(body, nuc), dna


def bar(cx, y, trk):
    track = Rectangle(width=3.0, height=.45, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, y, 0])
    fill = always_redraw(lambda: Rectangle(width=max(.001, 3 * trk.get_value() / 4), height=.45, stroke_width=0,
                                           fill_color=TEAL, fill_opacity=.85).move_to([cx - 1.5 + 1.5 * trk.get_value() / 4, y, 0]))
    return track, fill


BY = -1.8


class S03Stain(HScene):
    def construct(self):
        d = Dish(self, 0, -.45, 3.25, run=0, advance=2.9)
        cells = {k: cell_row(x, k) for k, x in (("G1", -4.4), ("S", 0), ("G2", 4.4))}
        tags = VGroup(*[lab(k, [x, 2.95, 0], TEXT, 36) for k, x in (("G1", -4.4), ("S", 0), ("G2", 4.4))])
        self.play(d.vis.animate.set_value(0), *[FadeIn(c[0], scale=.3) for c in cells.values()], FadeIn(tags), run_time=1.2)
        self.remove(d.g)
        self.play(*[Create(c[1]) for c in cells.values()], run_time=1.8)
        v = {k: ValueTracker(0) for k in cells}
        bars = {k: bar(x, BY, v[k]) for k, x in (("G1", -4.4), ("S", 0), ("G2", 4.4))}
        v["S"].set_value(2.1)
        self.play(*[Create(b[0]) for b in bars.values()], run_time=.8)
        self.add(*[b[1] for b in bars.values()])
        tick = Line([-5.15, BY - .22, 0], [-5.15, BY - .62, 0], color=TEAL, stroke_width=4)
        note = lab("1C = one haploid genome", [-4.1, -2.75, 0], TEAL, 28)
        self.at("1c")
        self.play(Create(tick), FadeIn(note), v["S"].animate.set_value(2.5), run_time=1.0)
        self.play(v["S"].animate.set_value(2.9), run_time=2.2, rate_func=linear)
        self.at("diploid")
        self.play(FadeOut(tick), FadeOut(note), v["G1"].animate.set_value(2), run_time=.9)
        m2 = lab("2C", [-4.4, -1.3, 0], TEAL, 32)
        self.play(FadeIn(m2), run_time=.3)
        self.at("4c")
        self.play(v["G2"].animate.set_value(4), v["S"].animate.set_value(3.3), run_time=1.0)
        m4 = lab("4C", [4.4 + 1.5, -1.3, 0], TEAL, 32)
        self.play(FadeIn(m4), run_time=.3)
        self.at("mitosis")
        self.play(FadeIn(lab("still diploid", [4.4, -2.75, 0], GREY, 30)), v["S"].animate.set_value(3.6), run_time=1.2)
        self.play(v["S"].animate.set_value(3.9), run_time=1.0)
        self.finish()


class S03Ploidy(HScene):
    def construct(self):
        (b1, n1), dna1 = cell_row(-4.4, "G1")[0], cell_row(-4.4, "G1")[1]
        (b2, n2), dna2 = cell_row(4.4, "G2")[0], cell_row(4.4, "G2")[1]
        c1 = VGroup(b1, n1)
        c2 = VGroup(b2, n2)
        v1, v2 = ValueTracker(2), ValueTracker(4)
        t1, f1 = bar(-4.4, BY, v1)
        t2, f2 = bar(4.4, BY, v2)
        m2 = lab("2C", [-4.4, -1.3, 0], TEAL, 32)
        m4 = lab("4C", [5.9, -1.3, 0], TEAL, 32)
        self.add(c1, c2, dna1, dna2, t1, t2, f1, f2, m2, m4,
                 lab("G1", [-4.4, 2.95, 0], TEXT, 36), lab("G2", [4.4, 2.95, 0], TEXT, 36))
        self.breathe(c1)
        self.breathe(c2)
        dip = lab("diploid", [0, .75, 0], TEXT, 40)
        self.at("tetraploid")
        self.play(FadeIn(dip), run_time=.6)

        def rods(cx, sisters):
            if not sisters:
                return VGroup(Line([cx - .22, .35, 0], [cx - .22, 1.15, 0], color=HOMA, stroke_width=10),
                              Line([cx + .22, .35, 0], [cx + .22, 1.15, 0], color=HOMB, stroke_width=10))
            return VGroup(*[Line([cx + dx, .35, 0], [cx + dx, 1.15, 0], color=col, stroke_width=10)
                            for dx, col in ((-.42, HOMA), (-.2, HOMA), (.2, HOMB), (.42, HOMB))])
        for r in (rods(-4.4, False), rods(4.4, False)):
            r.set_stroke(opacity=0)
        r1, r2 = rods(-4.4, False), rods(4.4, False)
        self.at("still has")
        self.play(ReplacementTransform(dna1, r1), ReplacementTransform(dna2, r2), run_time=1.4)
        r2s = rods(4.4, True)
        self.at("chromatids")
        sl = lab("sister chromatids", [4.4, 2.7, 0], TEXT, 30)
        self.play(ReplacementTransform(r2, r2s), run_time=1.2)
        r1s = rods(-4.4, True)
        self.at("doubling")
        self.play(ReplacementTransform(r1, r1s), v1.animate.set_value(4), run_time=1.6)
        self.at("amount")
        c1_ = lab("DNA amount: doubled", [0, -1.5, 0], TEAL, 36)
        c2_ = lab("ploidy: unchanged", [0, -2.4, 0], TEXT, 36)
        self.play(FadeOut(VGroup(t1, t2, f1, f2, m2, m4)), FadeIn(c1_), run_time=.7)
        self.play(FadeIn(c2_), run_time=.7)
        for _ in range(3):
            self.play(Indicate(VGroup(r1s, r2s), scale_factor=1.06), run_time=1.5)
        self.finish()


class S04Cytometer(HScene):
    def construct(self):
        d = self.dish_left(run=0, advance=2.9)
        d.cx.set_value(-4.35)
        d.cy.set_value(-.05)
        d.s.set_value(2.4)
        pi = lab("propidium iodide", [-4.35, 2.9, 0], TEAL, 30)
        self.at("propidium")
        self.play(d.glow.animate.set_value(1), d.haze.animate.set_value(1), FadeIn(pi), run_time=1.8)
        rn = chip("RNase", ORANGE, size=30).move_to([-4.35, -3.0, 0])
        self.at("add")
        self.play(FadeIn(rn), run_time=.4)
        self.play(d.haze.animate.set_value(0), run_time=2.2)
        self.at("rna")
        self.play(FadeOut(pi), FadeOut(rn), run_time=.8)
        ch = self.channel()
        ax = VGroup(Line([-.4, BASE, 0], [6.4, BASE, 0], color=GREY, stroke_width=3), lab("DNA per cell (glow)", [3.0, -3.55, 0], TEXT, 28))
        self.at("flow cytometer")
        self.play(FadeIn(ch), FadeIn(ax), run_time=.6)
        i2, i4 = d.pick(.05, .4), d.pick(.78, .86)
        self.play(AnimationGroup(self.send(d, i2, 1.0, .38), self.send(d, i4, 2.0, .75), lag_ratio=.35))
        self.finish()


class S04Amount(HScene):
    def construct(self):
        d = self.dish_left(run=0, advance=2.9, glow=1)
        d.cx.set_value(-4.35)
        d.cy.set_value(-.05)
        d.s.set_value(2.4)
        ch = self.channel()
        ax = VGroup(Line([-.4, BASE, 0], [6.4, BASE, 0], color=GREY, stroke_width=3), lab("DNA per cell (glow)", [3.0, -3.55, 0], TEXT, 28))
        self.add(ch, ax)
        tk = VGroup(lab("0", [hx(0), BASE - .3, 0], TEXT, 28), lab("2C", [hx(1), BASE - .3, 0], TEAL, 28), lab("4C", [hx(2), BASE - .3, 0], TEAL, 28))
        self.play(LaggedStart(*[FadeIn(t) for t in tk], lag_ratio=.4), run_time=1.6)
        i2, i4 = d.pick(.05, .4, 1), d.pick(.78, .86, 1)
        self.at("fluorescence")
        self.play(self.send(d, i2, 1.0, .38, rt=1.5))
        self.at("4c cell")
        self.play(self.send(d, i4, 2.0, .75, rt=1.5))
        br = Brace(Line([hx(1), BASE + .35, 0], [hx(2), BASE + .35, 0]), direction=UP, color=TEXT)
        bl = lab("about 2× signal", [(hx(1) + hx(2)) / 2, BASE + 1.05, 0], TEXT, 30)
        self.at("signal")
        self.play(Create(br), FadeIn(bl), run_time=.8)
        self.at("comparison")
        self.play(AnimationGroup(*[self.send(d, d.pick(lo, hi, k), fl, op, rt=1.3)
                                   for (lo, hi, k, fl, op) in ((.05, .4, 2, 1.0, .38), (.78, .86, 2, 2.0, .75), (.55, .7, 0, 1.5, .55))], lag_ratio=.6))
        self.finish()


class S05Histogram(HScene):
    def construct(self):
        d = self.dish_left(run=0, advance=2.9, glow=1)
        self.hist(tint=False, add=False)
        self.add(hist_axes(True), self.illus)
        self.illus.set_opacity(0)
        qs = quantiles(60)
        cnt, dots, tg = {}, VGroup(), []
        for f in qs:
            b = round(f / .05)
            k = cnt.get(b, 0)
            cnt[b] = k + 1
            dots.add(Dot([hx(f), 3.3, 0], radius=.05, color=TEAL))
            tg.append([hx(f), BASE + .07 + k * .1, 0])
        self.add(dots)
        self.play(LaggedStart(*[dd.animate.move_to(t) for dd, t in zip(dots, tg)], lag_ratio=.02), run_time=1.5)
        self.at("histogram")
        self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in self.bars.rects], lag_ratio=.02), FadeOut(dots), self.illus.animate.set_opacity(1), run_time=1.5)
        l1 = lab("2C: G0 + G1", [hx(1), 2.7, 0], TINT, 30)
        l2 = lab("4C: G2 + M", [hx(2), -.55, 0], TINT, 30)
        l3 = lab("S", [3.6, -1.6, 0], TINT, 36)
        self.at("peak at 2c")
        self.play(*[r.animate.set_fill(TINT, opacity=.75) for r in self.bars.sel(0, 1.2)], FadeIn(l1), run_time=.8)
        self.at("another")
        self.play(*[r.animate.set_fill(TINT, opacity=.75) for r in self.bars.sel(1.8, 2.6)], FadeIn(l2), run_time=.8)
        self.at("cells in s")
        self.play(*[r.animate.set_fill(TEAL, opacity=.55) for r in self.bars.sel(1.2, 1.8)], FadeIn(l3), run_time=.8)
        self.play(Indicate(VGroup(*self.bars.sel(1.2, 1.8)), color=TEAL, scale_factor=1.05), run_time=1.6)
        self.finish()


class S05Axes(HScene):
    def construct(self):
        d = self.dish_left(run=0, advance=2.9, glow=1)
        self.hist(tint=True)
        self.bars.paint(L=TINT, R=TINT, M=TEAL, lo=.92, ro=.92, mo=.7)
        xl = lab("DNA per cell (fluorescence)", [3.0, -3.55, 0], TEXT, 28)
        self.at("before")
        self.play(FadeIn(xl), run_time=.8)
        cur = Line([hx(1), BASE, 0], [hx(1), 2.5, 0], color=TEXT, stroke_width=3)
        self.at("horizontal")
        self.play(Create(cur), run_time=.6)
        self.at("fluorescence")
        self.play(cur.animate.move_to([hx(2), (BASE + 2.5) / 2, 0]), run_time=3.2)
        self.play(FadeOut(cur), run_time=.5)
        yl = lab("number of cells", [-1.0, -.1, 0], TEXT, 28).rotate(PI / 2)
        yax = Line([-.4, BASE, 0], [-.4, 2.7, 0], color=GREY, stroke_width=3)
        self.at("bar", lead=1.4)
        self.play(Create(yax), FadeIn(yl), run_time=.9)
        self.play(Indicate(VGroup(*self.bars.sel(.9, 1.1)), color=TEAL, scale_factor=1.04), run_time=1.0)
        self.at("this plot")
        xs = [.95, 1.0, 1.05, 1.5, 1.8, 1.95, 2.0, 2.05]
        ds = VGroup(*[Dot([hx(f), 3.0, 0], radius=.07, color=TEXT) for f in xs])
        tgs = [[hx(f), BASE + self.bars.at(f).height, 0] for f in xs]
        self.add(ds)
        self.play(LaggedStart(*[dd.animate.move_to(t) for dd, t in zip(ds, tgs)], lag_ratio=.08), run_time=1.4)
        self.play(FadeOut(ds), run_time=.5)
        self.at("not one")
        self.play(FadeIn(lab("one snapshot", [0.8, 3.35, 0], TEXT, 36)), run_time=.6)
        self.play(Indicate(self.bars.g, color=TEAL, scale_factor=1.02), run_time=1.6)
        self.finish()


def lifted_hist_state(self, panel=True, card=True):
    self.hist(tint=True, axes=True, yaxis=True, xlab="DNA per cell (fluorescence)", ylab=True)
    self.bars.paint(L=TINT, R=TINT, M=TEAL, lo=.92, ro=.92, mo=.7)
    lc = self.lifted(panel=panel)
    return lc


class S06Predict(HScene):
    def construct(self):
        d = self.dish_left(run=0, advance=2.9, glow=1)
        self.hist(tint=True, axes=True, yaxis=True, xlab="DNA per cell (fluorescence)", ylab=True)
        self.bars.paint(L=TINT, R=TINT, M=TEAL, lo=.92, ro=.92, mo=.7)
        dot = Dot([hx(2), -2.0, 0], radius=.09, color=TEXT)
        self.add(dot)
        lc = self.lifted(panel=False)
        self.play(Indicate(dot, scale_factor=2.2, color=TEXT), d.vis.animate.set_value(0), run_time=1.0)
        self.remove(d.g)
        self.at("one cell")
        self.play(ReplacementTransform(dot, lc), run_time=1.6)
        self.breathe(lc)
        self.at("copied")
        self.play(FadeIn(self.panel), run_time=.9)
        card = lab("G2 or mitosis?", [0, 3.4, 0], TEXT, 44)
        self.at("is it still")
        self.play(FadeIn(card, shift=DOWN * .2), run_time=.6)
        self.play(Indicate(VGroup(*self.bars.sel(1.8, 2.6)), color=TEXT, scale_factor=1.03), run_time=1.4)
        self.finish()


class S07Think(HScene):
    def construct(self):
        self.hist(tint=True, axes=True, yaxis=True, xlab="DNA per cell (fluorescence)", ylab=True)
        self.bars.paint(L=TINT, R=TINT, M=TEAL, lo=.92, ro=.92, mo=.7)
        lc = self.lifted(panel=True)
        self.add(lc, lab("G2 or mitosis?", [0, 3.4, 0], TEXT, 44))
        self.breathe(lc)
        t = ValueTracker(0)
        t.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(t)
        for r in self.bars.sel(1.8, 2.6):
            r.add_updater(lambda m: m.set_fill(TINT, opacity=.6 + .25 * math.sin(t.get_value() * 2.2)))
        self.finish()


class S08Blind(HScene):
    def construct(self):
        self.hist(tint=True, axes=True, yaxis=True, xlab="DNA per cell (fluorescence)", ylab=True)
        self.bars.paint(L=TINT, R=TINT, M=TEAL, lo=.92, ro=.92, mo=.7)
        lc = self.lifted(panel=True)
        card = lab("G2 or mitosis?", [0, 3.4, 0], TEXT, 44)
        self.add(lc, card)
        self.breathe(lc)
        self.play(FadeOut(card), run_time=.8)
        r4 = Ellipse(width=1.7, height=2.0, color=TEXT, stroke_width=4).move_to([hx(2), -1.65, 0])
        r2 = Ellipse(width=1.7, height=5.2, color=TEXT, stroke_width=4).move_to([hx(1), -.1, 0])
        c4 = chip("G2 + M", TEXT, size=30).move_to([hx(2), -.3, 0])
        c2 = chip("G1 + G0", TEXT, size=30).move_to([4.7, 1.7, 0])
        q0 = lab("G0: quiescent", [4.7, .95, 0], TEXT, 28)
        self.at("mitotic")
        self.play(Create(r4), FadeIn(c4), run_time=1.2)
        self.at("quiescent")
        self.play(Create(r2), FadeIn(c2), run_time=1.2)
        self.at("zero cells")
        self.play(FadeIn(q0), run_time=.6)
        sent = lab("DNA narrows the phase", [-1.2, 3.4, 0], GOLD, 40)
        self.at("dna content")
        self.play(FadeIn(sent), run_time=.8)
        self.at("other markers")
        self.play(Indicate(r4, color=TEXT, scale_factor=1.12), Indicate(r2, color=TEXT, scale_factor=1.05), run_time=1.6)
        self.play(Indicate(c4, color=TEXT), Indicate(c2, color=TEXT), run_time=1.4)
        self.finish()


class S09Edu(HScene):
    def construct(self):
        d = self.dish_left(run=0, advance=2.9, glow=1)
        self.hist(tint=True, xlab="DNA per cell (fluorescence)")
        self.bars.paint(L=TINT, R=TINT, M=TEAL, lo=.92, ro=.92, mo=.7)
        lbl = chip("EdU", YELLOW, size=30).move_to([-4.4, 2.75, 0])
        self.at("edu")
        self.play(FadeIn(lbl), run_time=.6)
        self.at("during")
        lbl2 = chip("EdU pulse", YELLOW, size=30).move_to([-4.4, 2.75, 0])
        rng = random.Random(3)
        wash = VGroup(*[Dot([-7.0 + rng.uniform(0, .9), rng.uniform(-2.3, 2.0), 0], radius=.05, color=YELLOW) for _ in range(55)])
        self.add(wash)
        self.play(Transform(lbl, lbl2), LaggedStart(*[w.animate.shift(RIGHT * 5.6) for w in wash], lag_ratio=.01), run_time=1.3)
        self.play(FadeOut(wash), run_time=.3)
        self.at("cells copying")
        self.play(d.edu.animate.set_value(1), run_time=1.4)
        click = chip("click tag", YELLOW, size=30).move_to([-4.4, -3.0, 0])
        self.at("click")
        self.play(FadeIn(click), d.click.animate.set_value(1), run_time=1.2)
        self.at("marks")
        self.play(*[r.animate.set_fill(YELLOW, opacity=.8) for r in self.bars.sel(1.2, 1.8)], run_time=1.0)
        self.play(Indicate(VGroup(*self.bars.sel(1.2, 1.8)), color=YELLOW, scale_factor=1.06), run_time=1.4)
        self.finish()


class S09Edges(HScene):
    def construct(self):
        d = self.dish_left(run=0, advance=2.9, glow=1, edu=1, click=1)
        self.hist(tint=True, xlab="DNA per cell (fluorescence)")
        self.bars.paint(L=TINT, R=TINT, M=YELLOW, lo=.75, ro=.75, mo=.6)
        self.add(chip("EdU", YELLOW, size=30).move_to([-4.4, 2.75, 0]))
        early, late = self.bars.sel(1.1, 1.28), self.bars.sel(1.72, 1.9)
        e_l = lab("early S", [3.55, -1.55, 0], YELLOW, 30)
        l_l = lab("late S", [4.2, -.8, 0], YELLOW, 30)
        self.at("borders")
        self.play(Indicate(VGroup(*self.bars.sel(1.2, 1.8)), color=YELLOW, scale_factor=1.04), run_time=1.4)
        self.at("early s")
        self.play(*[r.animate.set_fill(YELLOW, opacity=1) for r in early], FadeIn(e_l), run_time=.9)
        self.play(Indicate(VGroup(*early), color=TEXT, scale_factor=1.15), run_time=1.2)
        self.at("late s")
        self.play(*[r.animate.set_fill(YELLOW, opacity=1) for r in late], FadeIn(l_l), run_time=.9)
        self.play(Indicate(VGroup(*late), color=TEXT, scale_factor=1.15), run_time=1.2)
        self.at("dna content")
        self.play(Indicate(VGroup(*self.bars.sel(.9, 1.1)), color=TINT, scale_factor=1.04),
                  Indicate(VGroup(*self.bars.sel(1.9, 2.1)), color=TINT, scale_factor=1.04), run_time=1.6)
        fin = lab("S at the edges", [4.3, .35, 0], YELLOW, 36)
        br = Brace(Line([hx(1.15), BASE + 1.0, 0], [hx(1.9), BASE + 1.0, 0]), direction=UP, color=YELLOW)
        self.at("reveals")
        self.play(ReplacementTransform(VGroup(e_l, l_l), fin), Create(br), run_time=1.0)
        self.play(Indicate(VGroup(*self.bars.sel(1.2, 1.8)), color=YELLOW, scale_factor=1.05), run_time=1.6)
        self.finish()


class S10Ph3(HScene):
    def construct(self):
        self.hist(tint=True, axes=True, yaxis=True, xlab="DNA per cell (fluorescence)", ylab=True)
        self.bars.paint(L=TINT, R=TINT, M=TEAL, lo=.92, ro=.92, mo=.7)
        lc = self.lifted(panel=True, chrom=True)
        self.add(lc)
        self.breathe(lc, .02)
        outlines = VGroup(*[xshape(x.get_center(), 1.0, MAGENTA, 15) for x in self.chrom])
        outlines.set_stroke(opacity=0)
        self.add(outlines)
        self.remove(self.chrom)
        self.chrom.set_stroke(opacity=1)
        self.add(self.chrom)
        self.bring_to_back(outlines)
        chipab = chip("antibody", MAGENTA, size=30).move_to([-4.2, 2.8, 0])
        self.at("antibody")
        self.play(FadeIn(chipab), run_time=.6)
        self.play(self.panel.animate.shift(UP * .5).set_opacity(0), run_time=1.4)
        self.at("phosphorylated")
        pl = lab("phospho-H3", [-4.2, -2.75, 0], MAGENTA, 32)
        self.play(FadeIn(pl), outlines.animate.set_stroke(opacity=.55, width=10), run_time=1.0)
        self.at("this mark")
        self.play(LaggedStart(*[o.animate.set_stroke(opacity=1, width=18) for o in outlines], lag_ratio=.4), run_time=3.0)
        rng = random.Random(5)
        pts = [[hx(2) + rng.uniform(-.35, .35), BASE + rng.uniform(.25, 1.35), 0] for _ in range(8)]
        md = VGroup(*[Dot(p, radius=.09, color=MAGENTA) for p in pts])
        me = lab("mitosis-enriched", [hx(2), -.55, 0], MAGENTA, 30)
        self.at("helps")
        self.play(LaggedStart(*[FadeIn(m_, scale=2) for m_ in md], lag_ratio=.15), FadeIn(me), run_time=1.6)
        self.at("not an exact")
        self.play(*[m_.animate.shift([rng.uniform(-.25, .25), rng.uniform(-.2, .2), 0]) for m_ in md], run_time=1.6)
        self.finish()


class S10Timing(SpokenScene):
    def construct(self):
        XL, XR, BY_, HH = -6.2, 6.2, -2.55, 2.4
        pos = ValueTracker(0)
        self.add(pos)
        prof = lambda u: (.12 + .13 * u / .25) if u < .25 else (.25 + .75 * (u - .25) / .25 if u < .5 else (1 if u < .75 else 1 - (u - .75) / .25))
        sx = lambda u: XL + (XR - XL) * u
        base = Line([XL, BY_, 0], [XR, BY_, 0], color=GREY, stroke_width=3)
        divs = VGroup(*[Line([sx(u), BY_ + .1, 0], [sx(u), BY_ - .25, 0], color=GREY, stroke_width=3) for u in (0, .25, .5, .75, 1)])
        names = VGroup(*[lab(n, [sx(u + .125), -3.2, 0], TEXT, 32) for n, u in (("late G2", 0), ("prophase", .25), ("metaphase", .5), ("anaphase", .75))])
        tag = lab("schematic", [5.3, 3.45, 0], GREY, 28)
        sig = lab("phospho-H3 signal", [-4.4, .5, 0], MAGENTA, 30)
        xs = np.linspace(0, 1, 60)
        sym = xshape([0, 2.35, 0], 2.6, GREY, 14)
        spots = VGroup(*[Dot([0, 2.35 + dy, 0], radius=.11, color=MAGENTA) for dy in (-.25, 0, .25)])
        outl = xshape([0, 2.35, 0], 2.6, MAGENTA, 24)
        self.add(base, divs, names, tag, outl, sym, spots)

        def curve(mob):
            u = pos.get_value()
            pts = [[sx(x), BY_ + HH * prof(x), 0] for x in xs if x <= u]
            if len(pts) < 2:
                pts = [[sx(0), BY_ + HH * prof(0), 0], [sx(0) + .001, BY_ + HH * prof(0), 0]]
            mob.set_points_as_corners(pts)
        line = VMobject(color=MAGENTA, stroke_width=6)
        line.add_updater(curve)
        fillm = VMobject(stroke_width=0, fill_color=MAGENTA, fill_opacity=.4)

        def fillup(mob):
            u = pos.get_value()
            pts = [[sx(x), BY_ + HH * prof(x), 0] for x in xs if x <= u]
            if len(pts) < 2:
                return
            mob.set_points_as_corners([[pts[0][0], BY_, 0]] + pts + [[pts[-1][0], BY_, 0]])
        fillm.add_updater(fillup)
        scr = always_redraw(lambda: Line([sx(pos.get_value()), BY_, 0], [sx(pos.get_value()), BY_ + HH + .3, 0], color=TEXT, stroke_width=2))
        sym.set_stroke(opacity=1)

        def symup(mob):
            I = prof(pos.get_value())
            o = clamp((I - .3) / .6)
            outl.set_stroke(opacity=o)
            spots.set_fill(MAGENTA, opacity=clamp(I * 4) * (1 - o))
        sym.add_updater(symup)
        self.add(fillm, line, scr)
        self.play(FadeIn(sig), run_time=.5)
        self.at("signal begins")
        self.play(pos.animate.set_value(.2), run_time=max(.5, self.t_of("before") - self.elapsed()), rate_func=linear)
        self.at("spreads")
        self.play(pos.animate.set_value(.5), run_time=max(.5, self.t_of("remains") - self.elapsed() - .2), rate_func=linear)
        self.at("remains")
        self.play(pos.animate.set_value(.75), run_time=max(.5, self.t_of("then") - self.elapsed() - .2), rate_func=linear)
        self.at("then fades")
        self.play(pos.animate.set_value(1), run_time=max(.5, self.t_of("so a") - self.elapsed() - .2), rate_func=linear)
        um = lab("usually mitotic", [0, .4, 0], MAGENTA, 36)
        self.at("so a positive")
        self.play(FadeIn(um), run_time=.8)
        ap = lab("approximate", [4.9, .55, 0], MAGENTA, 32)
        self.at("timing")
        self.play(FadeIn(ap), run_time=.6)
        self.play(pos.animate.set_value(.0), run_time=2.4, rate_func=linear)
        self.play(pos.animate.set_value(1), run_time=2.0, rate_func=linear)
        self.finish()


class S11G0(HScene):
    def construct(self):
        d = self.dish_left(run=0, advance=2.9, glow=1, edu=1, click=1, ph=1)
        self.hist(tint=True, xlab="DNA per cell (fluorescence)")
        self.bars.paint(L=TINT, R=TINT, M=YELLOW, lo=.92, ro=.92, mo=.7)
        nc = lab("no clean G0 marker", [4.6, 1.9, 0], TEXT, 30)
        self.at("no single")
        self.play(FadeIn(nc), run_time=.6)
        self.at("together")
        self.play(d.cls.animate.set_value(1), run_time=1.0)
        cS = chip("S", YELLOW, size=32).move_to([3.6, -1.75, 0])
        self.at("classify")
        self.play(FadeIn(cS), run_time=.6)
        c0 = chip("G0 or G1?", TEXT, size=30).move_to([1.5, 2.7, 0])
        self.at("g0 versus")
        self.play(FadeIn(c0), run_time=.7)
        c2 = chip("G2 or late M?", TEAL, size=30).move_to([hx(2), -.55, 0])
        c3 = chip("late G2 or M", MAGENTA, size=30).move_to([hx(2), .6, 0])
        self.at("boundary")
        self.play(FadeIn(c2), FadeIn(c3), run_time=.8)
        self.play(Indicate(VGroup(c0, c2, c3), scale_factor=1.05), run_time=1.6)
        self.finish()


class S12Return(WorldScene):
    def construct(self):
        d = Dish(self, -4.35, -.2, 2.4, run=0, advance=2.9, glow=1, edu=1, click=1, ph=1, cls=1)
        bars = Bars()
        bars.paint(L=TINT, R=TINT, M=YELLOW, lo=.92, ro=.92, mo=.7)
        ax = hist_axes(True, True)
        self.add(bars.g, ax)
        q = lab("Which phase is each cell in?", [0, 3.4, 0], TEXT, 38)
        self.add(q)
        self.world()
        self.remove(self.cell, self.nuc, self.A, self.halo)
        k = d.nearest(-.1, 0)
        hero, target = self.to_world(d, k)
        self.play(d.vis.animate.set_value(0), Transform(hero, target), FadeOut(bars.g), FadeOut(ax), run_time=1.5)
        self.remove(d.g, hero)
        self.add(self.cell, self.nuc, self.halo, self.A, self.B)
        self.B.set_stroke(opacity=0)
        axb = self.axes(True)
        self.sy = [-1.6, 2.4]
        cnt = lab("copies this cycle: 1", [-3.25, -3.3, 0], TEAL)
        gl = lab("CDK activity", [4.3, 2.65, 0], GREEN)
        tl = lab("DNA per cell", [1.95, 1.9, 0], TEAL)
        ticks = VGroup(lab("2C", [.22, TB[1] * .5, 0], TEAL, 28), lab("4C", [.22, TB[1], 0], TEAL, 28))
        self.play(Create(axb), FadeIn(cnt), FadeIn(gl), run_time=.8)
        g = self.prog(GREEN_CYCLE, GREEN, *GB)
        tr = self.prog(TEAL_CYCLE, TEAL, *TB)
        self.add(g, tr, self.scrub)
        self.b_tie()
        ph = lab("G1", [-5.6, 2.08, 0], GREEN)
        self.add(ph)

        def phase_up(m):
            u = self.pos.get_value()
            s = "G1" if u < .25 else ("S" if u < .5 else ("G2" if u < .69 else ("M" if u < .89 else "G1")))
            if getattr(m, "cur", None) != s:
                m.cur = s
                m.become(lab(s, [-5.6, 2.08, 0], GREEN))
                m.cur = s
        ph.add_updater(phase_up)
        self.at("dna amount")
        self.play(FadeIn(tl), FadeIn(ticks), self.pos.animate.set_value(.67), run_time=2.4, rate_func=linear)
        # EdU: yellow over the S ramp
        yel = self.prog([(.25, .5), (.5, 1)], YELLOW, *TB, w=11, src="pos")
        yl = lab("EdU", [2.9, .2, 0], YELLOW, 30)
        self.at("edu")
        self.play(self.pos.animate.set_value(.2), run_time=.2)
        self.add(yel, yl)
        yl.set_opacity(0)
        self.play(self.pos.animate.set_value(.5), yl.animate.set_opacity(1), run_time=.5, rate_func=linear)
        # phospho-H3: magenta starts late in G2, fades in anaphase
        mp = [(.62, 0), (.7, .45), (.75, 1), (.88, 1), (.95, 0), (1, 0)]
        mag = self.prog(mp, MAGENTA, *MB, w=7, src="pos")
        ml = lab("phospho-H3", [2.2, -.55, 0], MAGENTA, 30)
        self.at("phosphoh3")
        self.pos.set_value(.6)
        self.add(mag, ml)
        self.play(self.pos.animate.set_value(.8), FadeIn(ml), run_time=1.3, rate_func=linear)
        self.at("sharpen")
        self.play(self.pos.animate.set_value(.97), Transform(q, lab("Markers sharpen the answer", [0, 3.4, 0], GOLD, 38)), run_time=1.5, rate_func=linear)
        self.at("g0 remains")
        self.play(self.pos.animate.set_value(.2), run_time=2.0, rate_func=linear)
        sw = VGroup(Circle(radius=.5, color=TEXT, stroke_width=5), Line([0, .5, 0], [0, .68, 0], color=TEXT, stroke_width=6),
                    lab("?", [0, -.02, 0], GOLD, 32)).move_to([6.1, 3.2, 0])
        hand = Line([6.1, 3.2, 0], [6.1, 3.6, 0], color=GOLD, stroke_width=4)
        hand.add_updater(lambda m, dt: m.rotate(dt * 1.2, about_point=np.array([6.1, 3.2, 0.])))
        self.at("how long")
        self.play(FadeIn(sw), FadeIn(hand), self.pos.animate.set_value(.0), run_time=1.0)
        self.play(self.pos.animate.set_value(.3), run_time=3.0, rate_func=linear)
        self.finish()


class S13End(EndCard):
    LINE = "DNA amount narrows the phase; markers sharpen the answer."
