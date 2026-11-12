"""History of life, film 2: Floors and Brackets (Biochemistrypedia explainer)

COLOR MAP, same as film 1
  GREEN = speciation   RED = extinction / "no"   BLUE = surviving lineages (here: uranium, the parent atoms)
  GREY = extinct lineages (here: lead, the daughter atoms)
  GOLD = brackets between two dated layers, the oxygen band      TEAL = fossil-floor flags, zircon
  YELLOW = labels to notice
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

LESSON_TITLE = "History of Life: Transitions, Extinctions and Radiations"
ASH_C, ROCK1, ROCK2 = "#CFC9BD", "#8A6B4F", "#7A6A58"


# ------------------------------------------------------------------ helpers
def Ln(a, b, col=TEXT, w=6):
    return Line([a[0], a[1], 0], [b[0], b[1], 0], color=col, stroke_width=w)


def live(f):
    return always_redraw(f)


def tick(sc):
    d = Dot(radius=0.001, color=BG)
    d.add_updater(lambda m, dt: None)
    sc.add(d)


def until(sc, t):
    r = t - sc.elapsed()
    if r > 0.02:
        sc.wait(r)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def two(a, b, size=28, ca=TEXT, cb=YELLOW):
    return VGroup(T(a, size, ca), T(b, size, cb)).arrange(DOWN, buff=0.08)


def left_label(text, y, col=TEXT, size=30, xr=-0.55):
    t = T(text, size, col)
    t.move_to([xr - t.width / 2, y, 0])
    return t


# ------------------------------------------------------------------ the rock column (one world, same place every scene)
COLX, CW, CT, CB = 2.0, 4.6, 3.0, -3.4


class Column:
    def __init__(self, cx=COLX, w=CW, yt=CT, yb=CB):
        h = yt - yb
        e = [yt, yt - .125 * h, yt - .1875 * h, yt - .5625 * h, yt - .625 * h, yb]
        self.cx, self.w, self.e = cx, w, e
        self.ashA_y, self.ashB_y = (e[1] + e[2]) / 2, (e[3] + e[4]) / 2
        self.bed_y = (e[2] + e[3]) / 2
        specs = [(e[4], e[5], ROCK1, .55, 4), (e[3], e[4], ASH_C, .85, 0), (e[2], e[3], ROCK2, .55, 3),
                 (e[1], e[2], ASH_C, .85, 0), (e[0], e[1], ROCK1, .55, 1)]
        self.parts = []
        for y1, y0, col, op, n in [(s[0], s[1], s[2], s[3], s[4]) for s in specs]:
            y_hi, y_lo = max(y1, y0), min(y1, y0)
            r = Rectangle(width=w, height=y_hi - y_lo, stroke_width=2, stroke_color=TEXT,
                          fill_color=col, fill_opacity=op).move_to([cx, (y_hi + y_lo) / 2, 0])
            g = VGroup(r)
            for k in range(1, n + 1):
                y = y_lo + (y_hi - y_lo) * k / (n + 1)
                g.add(Ln([cx - w / 2, y], [cx + w / 2, y], BG, 2).set_stroke(opacity=.6))
            self.parts.append(g)
        self.group = VGroup(*self.parts)


def shell(x, y, s=1.0, col=TEXT, op=1.0):
    sec = Sector(radius=.3 * s, angle=PI, start_angle=0, fill_color=col, fill_opacity=op,
                 stroke_width=2 if op < .5 else 0, stroke_color=col)
    g = VGroup(sec)
    for a in (.25, .5, .75):
        ang = PI * a
        g.add(Line(ORIGIN, [.3 * s * math.cos(ang), .3 * s * math.sin(ang), 0], color=BG, stroke_width=2).set_stroke(opacity=op))
    return g.move_to([x, y, 0])


def zircon(sc, x, y, s=1.0):
    d = Square(side_length=.26 * s, color=TEXT, stroke_width=2, fill_color=TEAL, fill_opacity=.95).rotate(PI / 4)
    ring = Circle(radius=.3 * s, color=TEAL, stroke_width=4)
    ph = random.random() * 6
    ring.add_updater(lambda m: m.set_stroke(opacity=.15 + .8 * max(0, math.sin(2.2 * (sc.elapsed() if hasattr(sc, "elapsed") else sc.renderer.time) + ph)) ** 2))
    return VGroup(d, ring).move_to([x, y, 0])


SH = [(-1.6, -0.3), (-0.95, 1.25), (1.3, 1.1), (1.5, -0.1)]          # shells in the bed, relative to the column centre
GH = [(-1.6, -1.9), (-0.4, -2.5), (1.2, -2.0), (0.2, -3.0)]           # ghost shells in older layers (film's last half)


def bed_shells(cx=COLX):
    return VGroup(*[shell(cx + x, y) for x, y in SH])


def bob(sc, m, amp=.1, f=3.0):
    m.b0 = m.get_center().copy()
    m.add_updater(lambda x: x.move_to(x.b0 + [0, amp * math.sin(f * (sc.elapsed() if hasattr(sc, "elapsed") else sc.renderer.time)), 0]))
    return m


def scan(sc, y0, y1=CB + .1):
    ln = Line([COLX - CW / 2, 0, 0], [COLX + CW / 2, 0, 0], color=YELLOW, stroke_width=9)
    t0 = sc.elapsed()
    ln.add_updater(lambda m: m.move_to([COLX, y0 - (((sc.elapsed() - t0) * .35) % 1) * (y0 - y1), 0]).set_stroke(opacity=.75))
    sc.add(ln)
    return ln


def bone(x, y, ln=1.3, ang=0.0, col=TEXT, wd=16):
    c = [x, y, 0]
    d = np.array([math.cos(ang), math.sin(ang), 0])
    p = np.array(c)
    g = VGroup(Line(p - d * ln / 2, p + d * ln / 2, color=col, stroke_width=wd))
    nrm = np.array([-d[1], d[0], 0])
    for s in (-1, 1):
        for t in (-1, 1):
            g.add(Dot(p + d * s * ln / 2 + nrm * t * wd * .006, radius=wd * .0105, color=col))
    return g


def flag(x, y, h=1.0):
    pole = Ln([x, y], [x, y + h], TEXT, 5)
    tri = Polygon([x, y + h, 0], [x + .55, y + h - .22, 0], [x, y + h - .44, 0], color=TEAL, fill_color=TEAL, fill_opacity=.95, stroke_width=2)
    return VGroup(pole, tri)


def sand_glass(sc, cx, cy, H, W, level, flow=True):
    """Hourglass: two triangular bulbs. level() in [0, 1] = fraction of sand still in the top bulb."""
    outline = VGroup(Polygon([cx - W, cy + H, 0], [cx + W, cy + H, 0], [cx, cy, 0], color=TEXT, stroke_width=5),
                     Polygon([cx - W, cy - H, 0], [cx + W, cy - H, 0], [cx, cy, 0], color=TEXT, stroke_width=5))

    def sand():
        L = clamp(level())
        h = H * L
        g = VGroup()
        if h > .02:
            g.add(Polygon([cx - W * h / H, cy + h, 0], [cx + W * h / H, cy + h, 0], [cx, cy, 0], stroke_width=0, fill_color=GOLD, fill_opacity=.9))
        b = H * (1 - L)
        if b > .02:
            g.add(Polygon([cx - W, cy - H, 0], [cx + W, cy - H, 0], [cx + W * (H - b) / H, cy - H + b, 0],
                          [cx - W * (H - b) / H, cy - H + b, 0], stroke_width=0, fill_color=GOLD, fill_opacity=.9))
        if flow and 0.015 < L < .985:
            g.add(Ln([cx, cy], [cx, cy - H + b], GOLD, 3))
        return g
    return outline, live(sand)


# ------------------------------------------------------------------ the zircon grid (same place in s03 to s06)
GX, GY = -2.5, 0.0
ORDER = random.Random(5).sample(range(16), 16)


def gpos(i):
    r, c = divmod(i, 4)
    return np.array([GX + (c - 1.5) * .8, GY - (r - 1.5) * .8, 0])


def crystal_mob():
    P = [(-2.3, 1.9), (0, 2.7), (2.3, 1.9), (2.3, -1.9), (0, -2.7), (-2.3, -1.9)]
    return Polygon(*[[GX + x, GY + y, 0] for x, y in P], color=TEAL, stroke_width=6, fill_color=TEAL, fill_opacity=.12)


class Grid:
    def __init__(self, sc, grey=(), glow=False):
        self.sc, self.glow = sc, glow
        self.dots = VGroup()
        rng = random.Random(2)
        for i in range(16):
            col = GREY if i in grey else BLUE
            d = Circle(radius=.26, color=col, fill_color=col, fill_opacity=1, stroke_width=3)
            d.b, d.ph, d.col, d.cc = gpos(i), rng.uniform(0, 6), col, ManimColor(col)
            d.move_to(d.b)
            d.add_updater(lambda m, dt, g=self: g._u(m, dt))
            self.dots.add(d)

    def _u(self, m, dt):
        t = self.sc.elapsed()
        m.move_to(m.b + [.05 * math.sin(1.1 * t + m.ph), .05 * math.cos(1.4 * t + m.ph), 0])
        m.cc = interpolate_color(m.cc, ManimColor(m.col), clamp(5 * dt))
        c = m.cc
        if self.glow and m.col == BLUE:
            s = max(0, math.sin(.8 * t + m.ph * 3)) ** 14
            c = interpolate_color(c, ManimColor(YELLOW), s)
        m.set_fill(c, 1)
        m.set_stroke(c, 3)

    def flip(self, idxs, run=1.0):
        rings = []
        for i in idxs:
            self.dots[i].col = GREY
            r = Circle(radius=.26, color=YELLOW, stroke_width=6).move_to(self.dots[i].get_center())
            rings.append(r)
        self.sc.play(*[r.animate.scale(2.6).set_stroke(opacity=0) for r in rings], run_time=run)
        self.sc.remove(*rings)


def legend(text, col, size=28):
    return VGroup(Dot(radius=.17, color=col), T(text, size, TEXT)).arrange(RIGHT, buff=.25)


# clock tied to a tracker (half-lives elapsed)
CKX, CKY, CKR = 3.5, 1.55, .95


def clock_parts(hl, cx=CKX, cy=CKY, r=CKR):
    face = Circle(radius=r, color=TEXT, stroke_width=5).move_to([cx, cy, 0])
    ticks = VGroup(*[Ln([cx + .84 * r * math.cos(a * PI / 6), cy + .84 * r * math.sin(a * PI / 6)],
                        [cx + r * math.cos(a * PI / 6), cy + r * math.sin(a * PI / 6)], TEXT, 3) for a in range(12)])

    def hand():
        f = hl.get_value()
        fr = 0 if f <= 0 else f - math.floor(f - 1e-6)
        fr = max(fr, .004)
        s = Sector(radius=.9 * r, angle=2 * PI * fr, start_angle=PI / 2 - 2 * PI * fr, fill_color=GOLD, fill_opacity=.4, stroke_width=0)
        s.shift(np.array([cx, cy, 0]) - s.get_arc_center())
        a = PI / 2 - 2 * PI * fr
        return VGroup(s, Ln([cx, cy], [cx + .88 * r * math.cos(a), cy + .88 * r * math.sin(a)], GOLD, 7))
    return VGroup(face, ticks), live(hand)


# ------------------------------------------------------------------ recap timeline (film 1's flags, same colours)
TX0, TX1, AXY = -5.6, 6.0, -0.4
TXF = lambda ga: TX0 + (TX1 - TX0) * (3.48 - ga) / 3.48
FLAGS = [("microbial life", "3.48 Ga", TXF(3.48), 1.2, 1), ("red alga", "about 1.05 Ga", TXF(1.05), 1.0, 1),
         ("animals", "about 558 Ma", TXF(.558), 2.0, 1), ("land plants", "about 473-471 Ma", TXF(.472), -1.6, -1)]


def flag_parts(name, date, x, h, d):
    pole = Ln([x, AXY], [x, h], TEXT, 4)
    tri = Polygon([x, h, 0], [x + .5, h - .22 * d, 0], [x, h - .44 * d, 0], color=TEAL, fill_color=TEAL, fill_opacity=.9, stroke_width=2)
    lab = two(name, date, 28)
    cx = clamp(x, -5.2, 5.0)
    lab.move_to([cx, h + .15 + lab.height / 2, 0] if d > 0 else [clamp(x, -5.2, 4.7), h - .6 - lab.height / 2, 0])
    return VGroup(pole, tri), lab


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    TITLE = "Floors and Brackets"
    LESSON = LESSON_TITLE


class S01Link(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        axis = Arrow([TX0 - .2, AXY, 0], [TX1, AXY, 0], buff=0, color=GREY, stroke_width=5, tip_length=.25)
        ends = VGroup(T("3.48 Ga", 26, GREY).move_to([-5.2, -1.15, 0]), T("Today", 26, GREY).move_to([5.6, -1.15, 0]))
        fparts = [flag_parts(*f) for f in FLAGS]
        mark = Arrow([TXF(.066) - .05, .55, 0], [TXF(.066) - .05, AXY + .08, 0], buff=0, color=RED, stroke_width=8, tip_length=.25)
        mlab = T("66 Ma", 30, RED).move_to([5.3, .95, 0])
        cur = Dot(radius=.13, color=YELLOW)
        cur.add_updater(lambda m: m.move_to([TX0 + (now() * 1.6) % (TX1 - TX0), AXY, 0]))
        self.play(Create(axis), FadeIn(ends), run_time=1.2)
        self.add(cur)
        self.at("flags")
        self.play(LaggedStart(*[FadeIn(VGroup(p, l), shift=DOWN * .3) for p, l in fparts], lag_ratio=.3), run_time=1.5)
        self.at("last cliff")
        self.play(GrowArrow(mark), FadeIn(mlab), run_time=.8)
        self.at("But how can")
        labels = VGroup(ends, mlab, *[l for _, l in fparts])
        tl = VGroup(axis, *[p for p, _ in fparts], mark)
        self.remove(cur)
        self.play(FadeOut(labels), run_time=.5)
        self.play(tl.animate.scale(.45).move_to([-4.6, 0, 0]), run_time=1.0)
        self.play(Rotate(tl, PI / 2), run_time=1.0)
        col = Column()
        self.play(LaggedStart(*[FadeIn(p, shift=UP * .2) for p in col.parts], lag_ratio=.18), run_time=1.2)
        self.at("bone")
        b = bone(COLX + .2, col.bed_y, 1.6, .3)
        self.play(FadeIn(b, scale=1.3), run_time=.6)
        self.at("no one there")
        q = T("?", 96, YELLOW)
        q.add_updater(lambda m: m.move_to([COLX + 1.7, col.bed_y + .1 + .1 * math.sin(3 * now()), 0]))
        self.play(FadeIn(q), run_time=.4)
        self.finish()


class S02Minerals(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        col = Column()
        VX = -3.6
        mount = Polygon([VX - 2.6, -3.4, 0], [VX - .5, 0.2, 0], [VX + .5, 0.2, 0], [VX + 2.6, -3.4, 0], color=GREY, stroke_width=5,
                        fill_color=ROCK1, fill_opacity=.35)
        chamber = Ellipse(width=3.0, height=1.5, color=RED, stroke_width=4, fill_color=RED, fill_opacity=.35).move_to([VX, -2.2, 0])
        rng = random.Random(4)
        magma = VGroup()
        for i in range(10):
            d = Dot(radius=.07, color=RED)
            d.b, d.ph = np.array([VX + rng.uniform(-1.1, 1.1), -2.2 + rng.uniform(-.45, .45), 0]), rng.uniform(0, 6)
            d.add_updater(lambda m: m.move_to(m.b + [.1 * math.sin(1.3 * now() + m.ph), .12 * math.cos(1.7 * now() + m.ph), 0]))
            magma.add(d)
        self.play(LaggedStart(*[FadeIn(p) for p in col.parts], lag_ratio=.15), FadeIn(mount), FadeIn(chamber), run_time=1.6)
        self.add(magma)
        sch = T("schematic", 24, GREY).move_to([-3.6, -3.62, 0])
        self.add(sch)
        self.at("minerals")
        self.play(*[Indicate(p, color=YELLOW, scale_factor=1.03) for p in col.parts[1::2]], run_time=1.4)
        self.at("zircon")
        crys = VGroup(*[Square(side_length=.28, color=TEXT, stroke_width=2, fill_color=TEAL, fill_opacity=.95).rotate(PI / 4)
                        .move_to([VX + dx, -2.2 + dy, 0]) for dx, dy in [(-.7, .15), (0, -.3), (.6, .2), (.1, .35)]])
        zl = T("zircon", 30, TEAL).move_to([VX, -1.2, 0])
        for c in crys:
            c.b = c.get_center()
            c.add_updater(lambda m, dt: m.rotate(.6 * dt))
        self.play(FadeIn(zl), *[GrowFromCenter(c) for c in crys], run_time=1.0)
        self.at("crystallizes")
        self.play(*[c.animate.scale(1.5) for c in crys], run_time=1.6)
        self.at("eruption")
        puffs = VGroup()
        for i in range(14):
            p = Dot(radius=rng.uniform(.06, .12), color=ASH_C)
            p.move_to([VX + rng.uniform(-.2, .2), .3, 0])
            puffs.add(p)
        tgt = [[COLX + rng.uniform(-2.0, 2.0), col.ashA_y + rng.uniform(-.1, .1), 0] for _ in puffs]
        self.add(puffs)
        self.play(*[p.animate.move_to([VX + rng.uniform(-.6, .6), 2.6, 0]) for p in puffs], run_time=.8)
        self.play(*[p.animate.move_to(t) for p, t in zip(puffs, tgt)], run_time=1.2)
        self.at("volcanic ash")
        z = zircon(self, COLX + 1.0, col.ashA_y)
        al = left_label("ash", col.ashA_y, ASH_C)
        self.play(FadeIn(al), FadeIn(z), Indicate(col.parts[3], color=ASH_C), run_time=.9)
        self.finish()


class S03Zircon(SpokenScene):
    def construct(self):
        tick(self)
        cr = crystal_mob()
        g = Grid(self)
        zl = T("zircon", 32, TEAL).move_to([GX, 3.25, 0])
        self.play(GrowFromCenter(cr), FadeIn(zl), run_time=1.8)
        self.at("takes up uranium")
        self.add(g.dots)
        self.play(*[FadeIn(d, scale=.3) for d in g.dots], run_time=1.5)
        ul = legend("uranium (parent)", BLUE).move_to([3.6, 1.5, 0])
        self.play(FadeIn(ul), run_time=.5)
        self.at("almost no lead")
        greys = VGroup(*[Circle(radius=.26, color=GREY, fill_color=GREY, fill_opacity=1, stroke_width=3).move_to([-6.2, y, 0]) for y in (1.6, 0, -1.6)])
        self.add(greys)
        for gd in greys:
            gd.add_updater(lambda m, dt: None)
        self.play(*[gd.animate.move_to([-5.1, gd.get_y(), 0]) for gd in greys], run_time=.9)
        self.play(*[gd.animate.move_to([-6.3, gd.get_y(), 0]).set_opacity(.15) for gd in greys], run_time=.8)
        ll = legend("almost no lead at the start", GREY).move_to([3.1, 0.2, 0])
        self.play(FadeIn(ll), run_time=.5)
        self.at("nearly all the lead")
        self.play(Indicate(ll[0], color=GREY, scale_factor=1.8), run_time=1.0)
        self.at("later decay")
        rings = [Circle(radius=.26, color=YELLOW, stroke_width=6).move_to(g.dots[i].get_center()) for i in (1, 6, 11)]
        for r in rings:
            self.add(r)
        self.play(*[r.animate.scale(2.8).set_stroke(opacity=0) for r in rings], run_time=1.2)
        self.finish()


class S04Halflife(SpokenScene):
    def construct(self):
        tick(self)
        cr = crystal_mob()
        g = Grid(self, glow=True)
        self.add(cr, g.dots)
        hl = ValueTracker(0)
        face, hand = clock_parts(hl)
        cl = T("one half-life", 28, GOLD).move_to([CKX, .22, 0])
        ORG, W, H = np.array([1.5, -3.1, 0]), 4.8, 2.1
        axes = VGroup(Ln(ORG, ORG + [W, 0, 0], GREY, 4), Ln(ORG, ORG + [0, H, 0], GREY, 4),
                      T("parent atoms left", 22, GREY).move_to(ORG + [1.1, H + .2, 0]), T("time", 22, GREY).move_to(ORG + [W - .2, -.3, 0]))

        def curve():
            t = clamp(hl.get_value(), 0, 3)
            n = max(2, int(60 * t / 3) + 1)
            m = VMobject(color=BLUE, stroke_width=8)
            m.set_points_as_corners([[ORG[0] + W * s / 3, ORG[1] + H * 2 ** -s, 0] for s in np.linspace(0, t, n)])
            return m
        mk = live(lambda: Dot([ORG[0] + W * clamp(hl.get_value(), 0, 3) / 3, ORG[1] + H * 2 ** -clamp(hl.get_value(), 0, 3), 0], radius=.14, color=YELLOW))
        self.at("same small chance")
        l1 = T("same small chance each year", 28, YELLOW).move_to([3.5, 3.1, 0])
        self.play(FadeIn(l1), run_time=.6)
        self.at("half the parent atoms")
        self.play(FadeIn(face), FadeIn(cl), Create(axes), run_time=.9)
        self.add(hand, live(curve), mk)
        self.play(hl.animate.set_value(1), run_time=2.0, rate_func=linear)
        self.at("the half life")
        d = VGroup(T("half-life = time for half", 28, GOLD), T("the parent atoms to decay", 28, GOLD)).arrange(DOWN, buff=.06).move_to([3.5, 3.05, 0])
        self.play(FadeOut(l1), FadeIn(d), run_time=.6)
        self.at("constant")
        nl = T("not a straight line", 26, YELLOW).move_to([4.9, -1.35, 0])
        self.play(FadeIn(nl), hl.animate.set_value(2.3), run_time=2.3, rate_func=linear)
        self.finish()


class S05Halving(SpokenScene):
    def construct(self):
        tick(self)
        cr = crystal_mob()
        g = Grid(self)
        self.add(cr, g.dots)
        hl = ValueTracker(0)
        face, hand = clock_parts(hl, CKX, 1.9, 1.05)
        self.add(face, hand)
        note = T("illustrative averages: each atom decays at random", 22, GREY).move_to([GX, -3.3, 0])
        self.add(note)
        self.at("after one half life")
        self.play(hl.animate.set_value(1), run_time=1.5, rate_func=linear)
        g.flip(ORDER[:8], 1.0)
        self.at("after the next")
        self.play(hl.animate.set_value(2), run_time=1.3, rate_func=linear)
        g.flip(ORDER[8:12], 1.0)
        self.at("the crystal keeps time")
        level = ValueTracker(1)
        out, sand = sand_glass(self, CKX, -0.85, .9, .7, lambda: level.get_value())
        hlab = T("started when", 26, TEXT)
        hlab2 = T("the crystal formed", 26, TEXT)
        hg = VGroup(hlab, hlab2).arrange(DOWN, buff=.05).move_to([CKX, -2.4, 0])
        self.play(FadeIn(out), FadeIn(hg), run_time=.7)
        self.add(sand)
        self.play(level.animate.set_value(.2), run_time=2.6, rate_func=linear)
        self.finish()


class S06Ratio(SpokenScene):
    def construct(self):
        tick(self)
        cr = crystal_mob()
        g = Grid(self, grey=set(ORDER[:12]))
        self.add(cr, g.dots)
        self.at("closed")
        seal = DashedVMobject(cr.copy().scale(1.1).set_fill(opacity=0).set_stroke(GOLD, 6), num_dashes=40)
        sl = T("closed: nothing in or out", 26, GOLD).move_to([GX, -3.3, 0])
        self.play(Create(seal), FadeIn(sl), run_time=1.3)
        self.at("started with no lead")
        tag = T("no lead at the start", 28, GREY).move_to([GX, 3.25, 0])
        self.play(FadeIn(tag), run_time=.5)
        self.at("the parent left")
        box = RoundedRectangle(corner_radius=.15, width=4.4, height=1.3, color=TEXT, stroke_width=5, fill_color=TEXT, fill_opacity=.08).move_to([3.6, 2.4, 0])
        bt = VGroup(T("measure parent", 26, TEXT), T("and daughter", 26, TEXT)).arrange(DOWN, buff=.05).move_to(box)
        beam = DashedLine([1.4, 2.4, 0], [-.1, 1.2, 0], color=YELLOW, stroke_width=4)
        self.play(FadeIn(box), FadeIn(bt), Create(beam), run_time=.9)
        self.play(*[Indicate(g.dots[i], color=YELLOW, scale_factor=1.4) for i in ORDER[12:]], run_time=.9)
        self.at("lead built up")
        self.play(*[Indicate(g.dots[i], color=GREY, scale_factor=1.3) for i in ORDER[:12]], run_time=1.2)
        self.at("count the half lives")
        cl = T("half-lives passed", 28, TEXT).move_to([3.6, .5, 0])
        ticks = VGroup(*[Circle(radius=.24, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0).move_to([2.4 + i * .8, -.4, 0]) for i in range(4)])
        self.play(FadeIn(cl), FadeIn(ticks), run_time=.6)
        self.play(ticks[0].animate.set_fill(GOLD, 1), run_time=.5)
        self.play(ticks[1].animate.set_fill(GOLD, 1), run_time=.5)
        self.at("gives the age")
        ar = Arrow([3.6, -1.1, 0], [3.6, -2.1, 0], buff=0, color=YELLOW, stroke_width=7)
        age = T("age", 52, GOLD).move_to([3.6, -2.7, 0])
        self.play(GrowArrow(ar), FadeIn(age), run_time=.8)
        self.finish()


def add_shells(sc, col, which=range(4), lag=.25):
    s = bed_shells()
    return s


class S07Column(SpokenScene):
    def construct(self):
        tick(self)
        col = Column()
        self.play(LaggedStart(*[FadeIn(p, shift=UP * .3) for p in col.parts], lag_ratio=.35), run_time=3.0)
        self.at("bed of fossils")
        sh = bed_shells()
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sh], lag_ratio=.25), run_time=1.3)
        fl = left_label("fossil bed", col.bed_y + .3)
        self.play(FadeIn(fl), run_time=.5)
        self.at("two layers")
        self.play(Indicate(col.parts[1], color=YELLOW, scale_factor=1.04), Indicate(col.parts[3], color=YELLOW, scale_factor=1.04), run_time=1.2)
        a1, a2 = left_label("ash above", col.ashA_y, ASH_C), left_label("ash below", col.ashB_y, ASH_C)
        self.play(FadeIn(a1), FadeIn(a2), run_time=.6)
        self.at("dated by its zircons")
        zs = VGroup(zircon(self, COLX - 1.0, col.ashA_y), zircon(self, COLX + 1.1, col.ashA_y),
                    zircon(self, COLX - 1.1, col.ashB_y), zircon(self, COLX + 1.0, col.ashB_y))
        self.play(LaggedStart(*[GrowFromCenter(z) for z in zs], lag_ratio=.2), run_time=1.0)
        self.finish()


def stage(sc, shells=True, zircons=True):
    col = Column()
    sc.add(col.group)
    parts = [col.group]
    if shells:
        sh = bed_shells()
        sc.add(sh)
        parts.append(sh)
    if zircons:
        zs = VGroup(zircon(sc, COLX - 1.0, col.ashA_y), zircon(sc, COLX + 1.1, col.ashA_y),
                    zircon(sc, COLX - 1.1, col.ashB_y), zircon(sc, COLX + 1.0, col.ashB_y))
        sc.add(zs)
    return col


class S08Predict(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        col = stage(self)
        self.at("undisturbed")
        slab = Rectangle(width=CW, height=.35, stroke_width=2, stroke_color=TEXT, fill_color="#A98B6B", fill_opacity=.7).move_to([COLX, 3.75, 0])
        up = Arrow([-.9, -2.9, 0], [-.9, 2.9, 0], buff=0, color=YELLOW, stroke_width=6)
        self.play(FadeIn(slab), run_time=.4)
        self.at("younger ones settle")
        self.play(slab.animate.move_to([COLX, CT + .175, 0]), run_time=1.0, rate_func=rush_into)
        self.at("older ones")
        yl, ol = left_label("younger", 2.8, YELLOW, xr=-1.25), left_label("older", -2.8, YELLOW, xr=-1.25)
        self.play(GrowArrow(up), FadeIn(yl), FadeIn(ol), run_time=1.0)
        self.at("oldest lies")
        un = VGroup(T("undisturbed:", 30, TEXT), T("oldest at the bottom", 30, TEXT)).arrange(DOWN, buff=.08).move_to([-3.9, 0.2, 0])
        self.play(FadeIn(un), Indicate(col.parts[0], color=YELLOW, scale_factor=1.02), run_time=1.2)
        self.at("How old")
        q = T("?", 110, YELLOW)
        q.add_updater(lambda m: m.move_to([COLX, col.bed_y + .1 + .12 * math.sin(3 * now()), 0]))
        self.play(FadeIn(q, scale=.5), run_time=.6)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        tick(self)
        self.camera.background_color = BG
        now = lambda: self.renderer.time
        col = Column()
        self.add(col.group, bed_shells())
        self.add(zircon(self, COLX - 1.0, col.ashA_y), zircon(self, COLX + 1.1, col.ashA_y),
                 zircon(self, COLX - 1.1, col.ashB_y), zircon(self, COLX + 1.0, col.ashB_y))
        q = T("?", 110, YELLOW)
        q.add_updater(lambda m: m.move_to([COLX, col.bed_y + .1 + .12 * math.sin(3 * now()), 0]))
        cap = VGroup(T("Predict:", 32, YELLOW), T("how old is the fossil bed?", 32, YELLOW)).arrange(DOWN, buff=.1).move_to([-3.9, 1.5, 0])
        cd = live(lambda: T(str(max(1, 5 - int(now()))), 110, TEXT).move_to([-3.9, -1.2, 0]))
        self.add(q, cap, cd)
        self.wait(5.0)


class S10Reveal(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        col = stage(self)
        q = T("?", 110, YELLOW).move_to([COLX, col.bed_y + .1, 0])
        self.add(q)
        self.play(FadeOut(q), run_time=.3)
        b = left_label("younger than this", col.ashB_y, GOLD)
        self.play(FadeIn(b), Indicate(col.parts[1], color=GOLD, scale_factor=1.05), run_time=1.2)
        self.at("older than")
        a = left_label("older than this", col.ashA_y, GOLD)
        self.play(FadeIn(a), Indicate(col.parts[3], color=GOLD, scale_factor=1.05), run_time=1.2)
        self.at("The answer")
        br = VMobject(color=GOLD, stroke_width=10)
        br.set_points_as_corners([[COLX + CW / 2 + .05, col.ashA_y, 0], [COLX + CW / 2 + .5, col.ashA_y, 0],
                                  [COLX + CW / 2 + .5, col.ashB_y, 0], [COLX + CW / 2 + .05, col.ashB_y, 0]])
        self.play(Create(br), run_time=1.0)
        self.at("a bracket")
        ban = VGroup(T("a bracket,", 40, GOLD), T("not a point", 40, GOLD)).arrange(DOWN, buff=.1).move_to([-3.4, col.bed_y, 0])
        self.play(FadeIn(ban, scale=1.1), run_time=.7)
        self.finish()


class S11Floor(SpokenScene):
    def construct(self):
        tick(self)
        col = Column()
        self.add(col.group)
        self.add(zircon(self, COLX - 1.0, col.ashA_y), zircon(self, COLX + 1.1, col.ashA_y),
                 zircon(self, COLX - 1.1, col.ashB_y), zircon(self, COLX + 1.0, col.ashB_y))
        sh = bed_shells()
        self.at("oldest known")
        self.play(LaggedStart(*[GrowFromCenter(s) for s in sh], lag_ratio=.2), run_time=1.2)
        x0, y0 = COLX + SH[0][0], col.bed_y + SH[0][1]
        fl = flag(x0, y0 + .2, 1.0)
        fl.shift(UP * 1.4)
        self.play(fl.animate.shift(DOWN * 1.4), run_time=.8, rate_func=rush_into)
        lab = left_label("oldest known fossil", y0 + .95, TEAL)
        ar = Arrow([x0 - .4, y0 + 1.25, 0], [x0 - .4, y0 + .3, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=.22)
        self.play(FadeIn(lab), GrowArrow(ar), run_time=.7)
        bob(self, ar, .08, 3.0)
        self.at("by then")
        self.play(Indicate(fl, color=YELLOW), run_time=1.2)
        self.at("it does not show")
        scan(self, y0 - .3)
        self.at("when the group began")
        q = T("?", 100, YELLOW).move_to([x0 + 1.0, col.e[4] - .9, 0])
        self.play(FadeIn(q, scale=.5), run_time=.6)
        bob(self, q, .1, 3.0)
        self.finish()


class S12Floor2(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        col = Column()
        self.add(col.group)
        self.add(zircon(self, COLX - 1.0, col.ashA_y), zircon(self, COLX + 1.1, col.ashA_y),
                 zircon(self, COLX - 1.1, col.ashB_y), zircon(self, COLX + 1.0, col.ashB_y))
        self.add(bed_shells())
        x0, y0 = COLX + SH[0][0], col.bed_y + SH[0][1]
        fl = flag(x0, y0 + .2, 1.0)
        lab = left_label("oldest known fossil", y0 + .95, TEAL)
        ar = Arrow([x0 - .4, y0 + 1.25, 0], [x0 - .4, y0 + .3, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=.22)
        self.add(fl, lab, ar)
        bob(self, ar, .08, 3.0)
        scan(self, y0 - .3)
        self.at("Earlier members")
        gh = VGroup(*[shell(COLX + x, y, 1.1, TEXT, .28) for x, y in GH])
        self.play(LaggedStart(*[FadeIn(s, scale=.6) for s in gh], lag_ratio=.3), run_time=1.6)
        for i, s in enumerate(gh):
            s.b, s.ph = s.get_center(), i * 1.7
            s.add_updater(lambda m: m.move_to(m.b + [.06 * math.cos(1.2 * now() + m.ph), .14 * math.sin(1.8 * now() + m.ph), 0]))
        gl = VGroup(T("not preserved", 28, TEXT), T("or not yet found", 28, TEXT)).arrange(DOWN, buff=.06)
        gl.move_to([-0.55 - gl.width / 2, -2.2, 0])
        self.at("never have been preserved")
        self.play(FadeIn(gl), run_time=.7)
        self.at("found yet")
        self.play(Indicate(gh, color=YELLOW, scale_factor=1.15), run_time=1.5)
        self.at("a floor")
        l2 = VGroup(T("minimum age:", 28, TEAL), T("by this time, at the latest", 28, TEAL)).arrange(DOWN, buff=.06)
        l2.move_to([-0.55 - l2.width / 2, y0 + 1.0, 0])
        self.play(FadeOut(lab), FadeIn(l2), Indicate(fl, color=YELLOW), run_time=1.0)
        self.at("The group may be older")
        old = Arrow([5.3, y0 + .6, 0], [5.3, -3.2, 0], buff=0, color=YELLOW, stroke_width=7)
        ol = T("older?", 30, YELLOW).move_to([5.9, y0 + .9, 0])
        self.play(GrowArrow(old), FadeIn(ol), run_time=1.0)
        bob(self, old, .1, 3.0)
        self.finish()


class S13Goe(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        AX = -1.3
        xa = lambda age: -5.4 + 10.8 * (2500 - age) / 100
        axis = Arrow([-6.0, AX, 0], [6.3, AX, 0], buff=0, color=GREY, stroke_width=5, tip_length=.25)
        tks = VGroup(T("2,500 Ma", 24, GREY).move_to([-5.4, AX - .35, 0]), T("2,400 Ma", 24, GREY).move_to([5.4, AX - .35, 0]))
        rng = random.Random(8)
        bub = VGroup()
        for i in range(14):
            d = Circle(radius=rng.uniform(.08, .15), color=TEXT, stroke_width=3).set_stroke(opacity=.7)
            d.x0, d.sp, d.ph = rng.uniform(3.0, 6.2), rng.uniform(.25, .6), rng.uniform(0, 5)
            d.add_updater(lambda m: m.move_to([m.x0 + .15 * math.sin(2 * now() + m.ph), -.9 + ((now() * m.sp + m.ph) % 1) * 2.8, 0]))
            bub.add(d)
        self.play(Create(axis), FadeIn(tks), run_time=1.0)
        self.add(bub)
        ol = T("oxygen in the air", 30, TEXT).move_to([4.7, 2.5, 0])
        self.at("Oxygen in")
        self.play(FadeIn(ol), run_time=.6)
        self.at("start of the great")
        x1, x2 = xa(2460), xa(2426)
        band = Rectangle(width=x2 - x1, height=3.1, stroke_width=0, fill_color=GOLD, fill_opacity=.3).move_to([(x1 + x2) / 2, AX + 1.55, 0])
        ttl = T("Great Oxidation Event", 36, TEXT).move_to([-3.0, 3.25, 0])
        sub = T("onset about 2,460-2,426 Ma", 30, GOLD).move_to([-2.6, 2.6, 0])
        self.play(FadeIn(ttl), GrowFromEdge(band, LEFT), run_time=1.5)
        self.play(FadeIn(sub), run_time=.5)
        self.at("bracketed by dated")
        rocks = VGroup()
        for x in (x1, x2):
            r = Rectangle(width=1.5, height=1.0, stroke_width=3, stroke_color=TEXT, fill_color=RED, fill_opacity=.3).move_to([x, AX - 1.3, 0])
            rocks.add(r, zircon(self, x, AX - 1.3, .9))
        rl = T("dated volcanic rock", 28, TEXT).move_to([(x1 + x2) / 2, -3.4, 0])
        self.play(FadeIn(rocks), FadeIn(rl), run_time=.9)
        bl = VMobject(color=GOLD, stroke_width=8).set_points_as_corners([[x1 + .35, AX + 3.1, 0], [x1, AX + 3.1, 0], [x1, AX, 0], [x1 + .35, AX, 0]])
        br = VMobject(color=GOLD, stroke_width=8).set_points_as_corners([[x2 - .35, AX + 3.1, 0], [x2, AX + 3.1, 0], [x2, AX, 0], [x2 - .35, AX, 0]])
        self.play(Create(bl), Create(br), run_time=1.0)
        self.at("from both sides")
        a1 = Arrow([x1 - .9, AX + 1.2, 0], [x1 - .1, AX + 1.2, 0], buff=0, color=YELLOW, stroke_width=6)
        a2 = Arrow([x2 + .9, AX + 1.2, 0], [x2 + .1, AX + 1.2, 0], buff=0, color=YELLOW, stroke_width=6)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=.8)
        self.finish()


class S14C14(SpokenScene):
    def construct(self):
        tick(self)
        lc, lu = ValueTracker(1), ValueTracker(1)
        LXc, RXc, CY, H, W = -3.3, 3.3, .9, 1.5, 1.1
        oc, sc_ = sand_glass(self, LXc, CY, H, W, lambda: lc.get_value())
        ou, su = sand_glass(self, RXc, CY, H, W, lambda: lu.get_value())
        self.add(sc_, su)
        self.play(FadeIn(oc), FadeIn(ou), run_time=1.0)
        self.play(lu.animate.set_value(.97), run_time=.01)
        lu_ = VGroup(T("uranium-235", 30, BLUE), T("to lead-207", 30, BLUE)).arrange(DOWN, buff=.05).move_to([RXc, -1.4, 0])
        self.play(FadeIn(lu_), run_time=.6)
        self.at("Carbon 14")
        lcl = VGroup(T("carbon-14", 34, YELLOW), T("half-life about 5,730 years", 26, TEXT)).arrange(DOWN, buff=.06).move_to([LXc, -1.45, 0])
        self.play(FadeIn(lcl), run_time=.6)
        self.at("decays quickly")
        self.play(lc.animate.set_value(.04), lu.animate.set_value(.94), run_time=3.2, rate_func=linear)
        self.at("too little")
        tag = T("about 50,000 years: too little left", 28, RED).move_to([LXc, -2.75, 0])
        self.play(FadeIn(tag), run_time=.6)
        self.play(lu.animate.set_value(.90), run_time=2.0, rate_func=linear)
        self.finish()


def mini_col(cx, w, yt, yb):
    return Column(cx, w, yt, yb)


class S15Dino(SpokenScene):
    def construct(self):
        tick(self)
        now = self.elapsed
        YT, YB = 2.9, -2.4
        b = bone(0, .6, 3.4, .25, TEXT, 22)
        self.at("dinosaur bones")
        self.play(Create(b), run_time=.9)
        self.at("carbon dated")
        stamp = VGroup(Rectangle(width=4.6, height=1.0, color=RED, stroke_width=8), T("no carbon-14", 40, RED)).rotate(.2).move_to([0, -1.0, 0])
        self.play(FadeIn(stamp, scale=1.4), run_time=.5)
        self.at("volcanic ash")
        A = Column(-4.2, 2.5, YT, YB)
        self.play(FadeOut(stamp), b.animate.scale(.3).move_to([-4.2, A.bed_y, 0]).rotate(-.25), run_time=.8)
        self.play(LaggedStart(*[FadeIn(p) for p in A.parts], lag_ratio=.12), run_time=1.0)
        self.remove(b)
        b2 = bone(-4.2, A.bed_y, 1.0, 0, TEXT, 12)
        self.add(b2)
        zA = VGroup(zircon(self, -4.5, A.ashA_y, .8), zircon(self, -3.9, A.ashA_y, .8), zircon(self, -4.5, A.ashB_y, .8), zircon(self, -3.9, A.ashB_y, .8))
        a1 = Arrow([-5.85, A.bed_y, 0], [-5.85, A.ashA_y, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=.2)
        a2 = Arrow([-5.85, A.bed_y, 0], [-5.85, A.ashB_y, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=.2)
        wl = T("where ash occurs", 28, YELLOW).move_to([-4.2, -3.05, 0])
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(zA), FadeIn(wl), run_time=1.0)
        self.at("slower clocks")
        self.play(*[Indicate(z, color=YELLOW, scale_factor=1.6) for z in zA], run_time=1.5)
        self.at("Elsewhere")
        B = Column(0.0, 2.5, YT, YB)
        C = Column(4.2, 2.5, YT, YB)
        # B has no ash layers: draw them as plain rock
        for i in (1, 3):
            B.parts[i][0].set_fill(ROCK1, .55)
        bb = bone(0, B.bed_y, 1.0, 0, TEXT, 12)
        zC = VGroup(zircon(self, 3.9, C.ashA_y, .8), zircon(self, 4.5, C.ashA_y, .8), zircon(self, 3.9, C.ashB_y, .8), zircon(self, 4.5, C.ashB_y, .8))
        self.play(FadeIn(B.group), FadeIn(bb), FadeIn(C.group), FadeIn(zC), run_time=1.0)
        link = DashedLine([1.3, B.bed_y, 0], [2.95, C.ashB_y, 0], color=YELLOW, stroke_width=5)
        ol = T("other methods", 28, YELLOW).move_to([2.1, -3.05, 0])
        self.at("other methods")
        self.play(Create(link), FadeIn(ol), run_time=1.2)
        self.finish()


class S16Rule(SpokenScene):
    def construct(self):
        tick(self)
        YT, YB = 2.4, -2.7
        L = Column(-3.4, 3.2, YT, YB)
        R = Column(3.4, 3.2, YT, YB)
        div = Ln([0, 3.0], [0, -3.6], GREY, 3)
        shL = VGroup(*[shell(-3.4 + dx, L.bed_y + dy, .9) for dx, dy in [(-.9, -.1), (.5, .5)]])
        sR = [(-.9, -.4), (.5, .5), (.9, -.2)]
        shR = VGroup(*[shell(3.4 + dx, R.bed_y + dy, .9) for dx, dy in sR])
        ghR = VGroup(*[shell(3.4 + dx, y, 1.0, TEXT, .28) for dx, y in [(-.8, -1.5), (.4, -2.2), (.9, -1.7)]])
        zs = VGroup(zircon(self, -3.8, L.ashA_y, .8), zircon(self, -2.9, L.ashA_y, .8), zircon(self, -3.8, L.ashB_y, .8), zircon(self, -2.9, L.ashB_y, .8))
        dim = [Rectangle(width=6.8, height=7.2, stroke_width=0, fill_color=BG, fill_opacity=.62).move_to([x, -.3, 0]) for x in (-3.4, 3.4)]
        self.play(FadeIn(L.group), FadeIn(R.group), FadeIn(div), FadeIn(shL), FadeIn(shR), FadeIn(ghR), FadeIn(zs), run_time=1.2)
        self.add(*dim)
        self.at("Dated layers")
        self.play(FadeOut(dim[0]), run_time=.8)
        br = VMobject(color=GOLD, stroke_width=10)
        br.set_points_as_corners([[-1.75, L.ashA_y, 0], [-1.35, L.ashA_y, 0], [-1.35, L.ashB_y, 0], [-1.75, L.ashB_y, 0]])
        bl = T("bracket", 48, GOLD).move_to([-3.4, 3.3, 0])
        self.play(Create(br), FadeIn(bl), run_time=1.2)
        self.at("oldest known fossil")
        self.play(FadeOut(dim[1]), run_time=.8)
        x0, y0 = 3.4 - .9, R.bed_y - .4
        fl = flag(x0, y0 + .2, .9)
        ar = Arrow([x0 - .35, y0 + 1.1, 0], [x0 - .35, y0 + .25, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=.2)
        fll = T("floor", 48, TEAL).move_to([3.4, 3.3, 0])
        self.play(FadeIn(fl, shift=DOWN * .5), GrowArrow(ar), FadeIn(fll), run_time=1.0)
        self.finish()


class S17End(EndCard):
    LINE = "Dated layers give a bracket; a first fossil gives a floor."
