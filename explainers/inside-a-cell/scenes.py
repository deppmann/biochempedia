"""One Cell, Many Jobs, Shared Space (Biochemistrypedia, Life Science grade 7, film 1).

COLOUR MAP (whole film): cell membrane BLUE; cytoplasm PALE BLUE; nucleus PURPLE; ER GREEN;
mitochondria GOLD; vacuole / fat drop CREAM; food ORANGE; muscle fibres PINK; energy YELLOW.
All cells are flat schematic cartoons.
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CREAM = "#F1E6C4"
CYTO = "#8FC1E3"
FOOD = "#F29E4C"
FIBER = "#E58FB5"
RIBO = "#F5EBD0"

CX, CY, CW, CH = 0.0, -0.5, 9.6, 5.2
NUC_C = (-2.7, 0.6)
ER_C = (0.3, 0.85)
MITO = [((3.2, -0.7), 20), ((1.0, -2.1), -12), ((3.5, -2.3), 8)]
VAC_C = (-3.2, -1.9)


# ---------------------------------------------------------------- small helpers
def top(text, color=TEXT, size=30, **kw):
    t = T(text, size, color, **kw).move_to([0, 3.1, 0])
    return fit(t, max_w=12.4, max_h=0.8)


def bottom(text, color=TEXT, size=28, **kw):
    t = T(text, size, color, **kw).move_to([0, -3.45, 0])
    return fit(t, max_w=12.4, max_h=0.6)


def bean(pos, ang, w=1.6, h=0.75, col=GOLD, sw=4, op=0.4):
    return RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=col, stroke_width=sw,
                            fill_color=col, fill_opacity=op).rotate(ang * DEGREES).move_to([*pos, 0])


def pulse(m, period=1.0, amp=0.08):
    c = m.get_center()
    m._pt = [0.0, 1.0]

    def f(mm, dt):
        mm._pt[0] += dt
        s = 1 + amp * (0.5 - 0.5 * math.cos(2 * math.pi * mm._pt[0] / period))
        mm.scale(s / mm._pt[1], about_point=c)
        mm._pt[1] = s
    m.add_updater(f)


def heart_icon(c, h=0.7):
    f = lambda t: np.array([16 * math.sin(t) ** 3, 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t), 0])
    g = ParametricFunction(f, t_range=[0, TAU], stroke_color=RED, stroke_width=3).set_fill(RED, 0.9)
    g.set_height(h).move_to([*c, 0])
    return g


def make_motes(n=16, seed=1, xr=(-4.3, 4.3), yr=(-2.8, 1.7), speed=0.6):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=0.07, color="#CFE8F7").set_opacity(0.55)
        d.move_to([rng.uniform(*xr), rng.uniform(*yr), 0])
        a = rng.uniform(0, TAU)
        d.v = np.array([math.cos(a), math.sin(a), 0]) * speed * rng.uniform(0.5, 1.0)

        def f(m, dt, xr=xr, yr=yr):
            m.shift(m.v * dt)
            x, y = m.get_center()[:2]
            if x < xr[0] or x > xr[1]:
                m.v[0] *= -1
                m.shift(m.v * dt * 2)
            if y < yr[0] or y > yr[1]:
                m.v[1] *= -1
                m.shift(m.v * dt * 2)
        d.add_updater(f)
        g.add(d)
    return g


class ER(VGroup):
    """Folded ribbons that gently wave; ribosome dots ride on them. Trackers drive colour, wave, dots."""
    DOT_U = [0.15, 0.4, 0.65, 0.88]

    def __init__(self, center=ER_C, L=2.8, tint=1.0, dot_op=0.0, level=1.0):
        super().__init__()
        self.c = np.array(center, dtype=float)
        self.L = L
        self.t = 0.0
        self.tint = ValueTracker(tint)
        self.dotop = ValueTracker(dot_op)
        self.amp = ValueTracker(1.0)
        self.level = ValueTracker(level)
        self.ribbons = VGroup(*[VMobject() for _ in range(4)])
        self.dots = VGroup(*[Dot(radius=0.07) for _ in range(16)])
        self.add(self.ribbons, self.dots)
        self._place()
        self.add_updater(lambda m, dt: m._step(dt))

    def _y(self, k, u):
        return self.c[1] + (k - 1.5) * 0.34 + 0.1 * self.amp.get_value() * np.sin(2 * np.pi * 1.25 * u + k * 1.2 + self.t * 1.7)

    def _place(self):
        col = interpolate_color(ManimColor(GREY), ManimColor(GREEN), self.tint.get_value())
        lv = self.level.get_value()
        u = np.linspace(0, 1, 40)
        for k, r in enumerate(self.ribbons):
            x = self.c[0] - self.L / 2 + u * self.L
            y = self._y(k, u)
            r.set_points_smoothly(np.stack([x, y, np.zeros_like(x)], 1))
            r.set_stroke(col, 8, opacity=lv)
            r.set_fill(opacity=0)
        for i, d in enumerate(self.dots):
            k, ui = i % 4, self.DOT_U[i // 4]
            d.move_to([self.c[0] - self.L / 2 + ui * self.L, self._y(k, ui) + 0.08, 0])
            d.set_fill(RIBO, opacity=self.dotop.get_value() * lv)

    def _step(self, dt):
        self.t += dt
        self._place()

    def freeze(self):
        self.clear_updaters()


class World:
    """The one cell the film carries, rebuilt in the same place in every scene."""

    def __init__(self, fill=0.25, nuc=PURPLE, er=1.0, mito=GOLD, vac=CREAM, dots=0.0, motes=True, scroll=False, seed=1):
        self.body = RoundedRectangle(corner_radius=1.0, width=CW, height=CH, stroke_color=BLUE, stroke_width=7,
                                     fill_color=CYTO, fill_opacity=fill).move_to([CX, CY, 0])
        self.nuc = Circle(radius=0.95, stroke_color=nuc, stroke_width=5, fill_color=nuc, fill_opacity=0.3).move_to([*NUC_C, 0])
        sc = VGroup(Rectangle(width=0.4, height=0.55, stroke_color=TEXT, stroke_width=2, fill_color=TEXT, fill_opacity=0.2),
                    *[Line([-0.12, dy, 0], [0.12, dy, 0], color=TEXT, stroke_width=2) for dy in (0.14, 0, -0.14)])
        self.scroll = sc.move_to([*NUC_C, 0]).set_opacity(1 if scroll else 0)
        self.er = ER(tint=er, dot_op=dots)
        self.mitos = VGroup(*[bean(p, a, col=mito) for p, a in MITO])
        self.vac = Circle(radius=0.75, stroke_color=vac, stroke_width=5, fill_color=vac, fill_opacity=0.3).move_to([*VAC_C, 0])
        self.motes = make_motes(seed=seed) if motes else VGroup()

    def add_to(self, scene):
        scene.add(self.body, self.motes, self.vac, self.nuc, self.scroll, self.er, self.mitos)

    def parts(self):
        return [self.body, self.motes, self.vac, self.nuc, self.scroll, self.er, self.mitos]

    def freeze(self):
        self.er.freeze()
        for m in self.motes:
            m.clear_updaters()


def badge(n, pos):
    c = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=0.95)
    return VGroup(c, T(str(n), 30, YELLOW, weight=BOLD).move_to(c)).move_to([*pos, 0])


def lit(a, b, w=5):
    return Line([*a, 0], [*b, 0], color=YELLOW, stroke_width=w).set_opacity(0.85)


# ---------------------------------------------------------------- cartoons (opening and closing)
HC, FC = (-3.7, -0.1), (3.9, -0.1)


def heart_cartoon(c):
    rect = RoundedRectangle(corner_radius=0.9, width=5.0, height=2.9, stroke_color=BLUE, stroke_width=6, fill_color=CYTO, fill_opacity=0.25)
    nuc = Ellipse(width=0.9, height=0.7, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.4)
    rng = random.Random(4)
    beans = VGroup()
    for xi in (-1.9, -1.0, 1.0, 1.9):
        for yi in (-0.85, 0, 0.85):
            beans.add(bean((xi, yi), rng.uniform(-25, 25), 0.72, 0.32, sw=3))
    for yi in (-0.95, 0.95):
        beans.add(bean((0, yi), rng.uniform(-10, 10), 0.72, 0.32, sw=3))
    return VGroup(rect, nuc, beans).move_to([*c, 0])


def fat_cartoon(c):
    ring = Circle(radius=1.9, stroke_color=BLUE, stroke_width=6, fill_color=CYTO, fill_opacity=0.25)
    drop = Circle(radius=1.55, stroke_color=CREAM, stroke_width=4, fill_color=CREAM, fill_opacity=0.5)
    pt = lambda a, d=1.73: np.array([d * math.cos(a * DEGREES), d * math.sin(a * DEGREES), 0])
    nuc = Ellipse(width=0.7, height=0.28, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.5).rotate((140 - 90) * DEGREES).move_to(pt(140))
    beans = VGroup(bean(pt(30)[:2], 30 + 90, 0.4, 0.18, sw=2), bean(pt(250)[:2], 250 + 90, 0.4, 0.18, sw=2))
    return VGroup(ring, drop, nuc, beans).move_to([*c, 0])


# ---------------------------------------------------------------- floor plans (rooms in normalised coordinates)
ORDER = ["nuc", "er", "m1", "m2", "m3", "vac", "fib"]
ROOMCOL = dict(nuc=PURPLE, er=GREEN, m1=GOLD, m2=GOLD, m3=GOLD, vac=CREAM, fib=FIBER)
NONE = (0.5, 0.5, 0.5, 0.5)
GEN = dict(nuc=(.04, .50, .30, .95), er=(.36, .55, .66, .95), m1=(.72, .50, .96, .95), m2=(.36, .08, .62, .42),
           m3=(.70, .08, .96, .38), vac=(.04, .08, .30, .42), fib=NONE)
SPEC_A = dict(nuc=(.04, .60, .24, .95), er=(.30, .40, .96, .95), m1=(.30, .08, .50, .32), m2=(.54, .08, .72, .32),
              m3=(.76, .08, .96, .32), vac=(.04, .10, .20, .45), fib=NONE)
SPEC_B = dict(vac=(.04, .08, .58, .92), nuc=(.66, .62, .96, .92), er=(.66, .30, .96, .54), m1=(.66, .08, .78, .22),
              m2=(.82, .08, .94, .22), m3=(.78, .56, .92, .60), fib=NONE)
HEART1 = dict(fib=(.50, .06, .96, .60), nuc=(.55, .68, .70, .92), er=(.74, .70, .96, .78), vac=(.82, .84, .88, .90),
              m1=(.12, .44, .20, .56), m2=(.30, .44, .36, .56), m3=(.43, .44, .47, .52))
HEART2 = dict(HEART1, m1=(.03, .06, .28, .94), m2=(.31, .06, .40, .94), m3=(.43, .06, .47, .30))
FAT = dict(vac=(.12, .12, .88, .88), nuc=(.14, .90, .30, .97), er=(.38, .90, .60, .97), m1=(.66, .90, .78, .97),
           m2=(.02, .30, .09, .50), m3=(.91, .50, .98, .66), fib=NONE)


def floor(spec, c=(CX, CY), w=CW, h=CH):
    base = Rectangle(width=w, height=h, stroke_color=BLUE, stroke_width=7, fill_color=CYTO, fill_opacity=0.25).move_to([*c, 0])
    rooms = VGroup()
    for k in ORDER:
        x0, y0, x1, y1 = spec[k]
        r = Rectangle(width=max((x1 - x0) * w, 0.02), height=max((y1 - y0) * h, 0.02), stroke_color=ROOMCOL[k],
                      stroke_width=3, fill_color=ROOMCOL[k], fill_opacity=0.6)
        r.move_to([c[0] - w / 2 + (x0 + x1) / 2 * w, c[1] - h / 2 + (y0 + y1) / 2 * h, 0])
        if (x1 - x0) * (y1 - y0) < 0.002:
            r.set_opacity(0)
        rooms.add(r)
    return base, rooms


def stripes(spec, c=(CX, CY), w=CW, h=CH, n=10):
    x0, y0, x1, y1 = spec["fib"]
    g = VGroup()
    for i in range(n):
        x = c[0] - w / 2 + (x0 + (i + 1) / (n + 1) * (x1 - x0)) * w
        ya, yb = c[1] - h / 2 + (y0 + 0.03) * h, c[1] - h / 2 + (y1 - 0.03) * h
        g.add(Line([x, ya, 0], [x, yb, 0], color=RIBO, stroke_width=3).set_opacity(0.35))
    return g


def tally(spec, c, w, hgt=0.38):
    sh = lambda k: (spec[k][2] - spec[k][0]) * (spec[k][3] - spec[k][1]) if (spec[k][2] - spec[k][0]) * (spec[k][3] - spec[k][1]) >= 0.002 else 0.0
    vals = [sh("nuc"), sh("er"), sh("m1") + sh("m2") + sh("m3"), sh("vac"), sh("fib")]
    vals.append(max(0.0, 1 - sum(vals)))
    cols = [PURPLE, GREEN, GOLD, CREAM, FIBER, CYTO]
    g = VGroup()
    x = c[0] - w / 2
    for v, col in zip(vals, cols):
        ww = max(v * w, 0.004)
        g.add(Rectangle(width=ww, height=hgt, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([x + ww / 2, c[1], 0]))
        x += v * w
    return g


def tally_frame(c, w, hgt=0.38):
    return Rectangle(width=w, height=hgt, stroke_color=TEXT, stroke_width=2).move_to([*c, 0])


TAL_C, TAL_W = (3.1, 3.1), 3.0


# ================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Inside a cell"
    TITLE = "One Cell, Many Jobs, Shared Space"


class S01Question(SpokenScene):
    def construct(self):
        sch = T("schematic cartoons", 24, TEXT).move_to([0, -3.4, 0])
        self.add(sch)
        heart, fat = heart_cartoon(HC), fat_cartoon(FC)
        hl = T("heart muscle cell", 30).move_to([HC[0], -2.0, 0])
        fl = T("white fat cell", 30).move_to([FC[0], -2.3, 0])
        icon = heart_icon((HC[0], 2.0))
        fdrop_t = fat[1].copy()
        fat[1].scale(0.05).set_opacity(0)
        self.at("your")
        self.play(FadeIn(heart[0]), FadeIn(heart[1]), LaggedStart(*[FadeIn(b, scale=0.4) for b in heart[2]], lag_ratio=0.06),
                  FadeIn(hl), FadeIn(icon), run_time=1.5)
        pulse(icon, 0.9, 0.18)
        pulse(heart[2], 0.9, 0.04)
        self.at("white fat cell")
        self.play(FadeIn(fat[0]), FadeIn(fat[2]), FadeIn(fat[3]), FadeIn(fl), run_time=0.6)
        fat[1].set_opacity(1)
        self.play(Transform(fat[1], fdrop_t), run_time=1.2)
        self.at("same kinds of parts")
        self.play(Indicate(heart[1], color=YELLOW), Indicate(fat[2], color=YELLOW), Indicate(heart[2], color=YELLOW, scale_factor=1.05), run_time=1.4)
        q = T("?", 160, YELLOW, weight=BOLD).move_to([0.1, 0.1, 0])
        self.at("so why")
        self.play(FadeIn(q, scale=0.4), run_time=0.7)
        pulse(q, 1.1, 0.12)
        self.at("look nothing alike")
        self.play(Indicate(heart[0], color=YELLOW, scale_factor=1.03), Indicate(fat[0], color=YELLOW, scale_factor=1.03), run_time=1.4)
        self.at("let's build")
        for m in (icon, heart[2], q):
            m.clear_updaters()
        L = VGroup(heart, hl, icon)
        R = VGroup(fat, fl)
        self.play(FadeOut(q), L.animate.shift(LEFT * 8), R.animate.shift(RIGHT * 8), FadeOut(sch), run_time=1.5)
        self.finish()


class S02Outline(SpokenScene):
    def construct(self):
        body = RoundedRectangle(corner_radius=1.0, width=CW, height=CH, stroke_color=BLUE, stroke_width=7,
                                fill_color=CYTO, fill_opacity=0.0).move_to([CX, CY, 0])
        self.at("start with the outline")
        self.play(Create(body), run_time=2.3)
        l1 = top("cell membrane", BLUE, 34, weight=BOLD)
        self.at("the cell membrane")
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.5)
        self.at("thin boundary")
        self.play(body.animate.set_stroke(width=14), run_time=0.5)
        self.play(body.animate.set_stroke(width=7), run_time=0.4)
        self.at("around the cell")
        self.play(ShowPassingFlash(body.copy().set_stroke(YELLOW, 12), time_width=0.5), run_time=1.6)
        dots = VGroup(*[Dot(radius=0.17, color=TEXT).move_to(p) for p in ([-6.3, 0.4, 0], [-6.3, -1.0, 0], [3.9, 0.4, 0], [3.9, -1.0, 0])])
        A, B, C, D = dots
        l2 = top("cell membrane: controls what enters and leaves", TEXT, 30, t2c={"cell membrane": BLUE})
        self.at("it controls what enters")
        self.play(FadeOut(l1), FadeIn(l2), FadeIn(dots), run_time=0.5)
        self.play(A.animate.move_to([-3.6, 0.4, 0]), B.animate.move_to([-4.95, -1.0, 0]),
                  C.animate.move_to([6.2, 0.4, 0]), D.animate.move_to([4.65, -1.0, 0]), run_time=1.6)
        self.play(B.animate.move_to([-6.3, -1.0, 0]), D.animate.move_to([3.4, -1.0, 0]), run_time=0.9)
        self.play(FadeOut(dots), run_time=0.4)
        motes = make_motes()
        l3 = top("cytoplasm", CYTO, 34, weight=BOLD)
        self.at("inside is the cytoplasm")
        self.play(body.animate.set_fill(CYTO, 0.25), FadeOut(l2), FadeIn(l3), FadeIn(motes), run_time=1.4)
        l4 = top("cytoplasm: a jelly-like fluid", TEXT, 32, t2c={"cytoplasm": CYTO})
        self.at("jelly like fluid")
        self.play(FadeOut(l3), FadeIn(l4), run_time=0.4)
        l5 = top("cytoplasm: fluid plus the parts in it", TEXT, 32, t2c={"cytoplasm": CYTO})
        self.at("the parts in it")
        self.play(FadeOut(l4), FadeIn(l5), run_time=0.4)
        l6 = top("cytoplasm: fluid plus parts, not the nucleus", TEXT, 32, t2c={"cytoplasm": CYTO})
        self.at("except the nucleus")
        self.play(FadeOut(l5), FadeIn(l6), run_time=0.4)
        self.finish()


class S03Parts(SpokenScene):
    def construct(self):
        w = World(nuc=GREY, er=0.0, mito=GREY, vac=GREY, dots=0.0, motes=True)
        self.add(w.body, w.motes)
        ph = [w.vac, w.nuc, w.er, w.mitos]
        self.at("the parts inside")
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in ph], lag_ratio=0.3), run_time=2.0)
        self.at("organelles")
        l1 = top("organelles", YELLOW, 34, weight=BOLD)
        self.play(FadeIn(l1), run_time=0.5)
        l2 = top("organelle = a small part with a special job", TEXT, 32, t2c={"organelle": YELLOW})
        self.at("an organelle is a small part")
        self.play(FadeOut(l1), FadeIn(l2), run_time=0.4)
        self.at("special job")
        self.play(*[Indicate(p, color=YELLOW, scale_factor=1.08) for p in (w.nuc, w.vac, w.mitos)], run_time=1.2)
        l3 = top("nucleus: holds the cell's instructions", TEXT, 32, t2c={"nucleus": PURPLE})
        self.at("the nucleus holds")
        self.play(FadeOut(l2), FadeIn(l3), w.nuc.animate.set_color(PURPLE), run_time=0.7)
        self.play(w.scroll.animate.set_opacity(1), Indicate(w.nuc, color=PURPLE), run_time=1.2)
        l4 = top("endoplasmic reticulum (ER)", GREEN, 34, weight=BOLD)
        self.at("the er")
        self.play(FadeOut(l3), FadeIn(l4), w.er.tint.animate.set_value(1.0), run_time=0.8)
        l5 = top("ER: a network of folded membranes", TEXT, 32, t2c={"ER": GREEN})
        self.at("folded membranes")
        self.play(FadeOut(l4), FadeIn(l5), w.er.amp.animate.set_value(2.2), run_time=1.0)
        self.play(w.er.amp.animate.set_value(1.0), run_time=1.0)
        l6 = top("ER: helps make and move proteins and fats", TEXT, 32, t2c={"ER": GREEN})
        self.at("it helps make")
        self.play(FadeOut(l5), FadeIn(l6), w.er.dotop.animate.set_value(1.0), run_time=0.8)
        pc = chip("protein", TEXT, 26).move_to([1.2, 1.7, 0])
        fc = chip("fat", CREAM, 26).move_to([-0.6, 1.7, 0])
        self.at("proteins and fats")
        self.play(FadeIn(pc, scale=0.5), FadeIn(fc, scale=0.5), run_time=0.7)
        self.play(pc.animate.move_to([3.2, 1.3, 0]), fc.animate.move_to([3.2, 0.5, 0]).set_opacity(1), run_time=1.8)
        self.finish()


class S04More(SpokenScene):
    def construct(self):
        w = World(nuc=PURPLE, er=1.0, mito=GREY, vac=GREY, dots=1.0, scroll=True)
        w.add_to(self)
        l1 = top("mitochondria: release energy stored in food", TEXT, 32, t2c={"mitochondria": GOLD})
        self.at("mitochondria release")
        self.play(w.mitos.animate.set_color(GOLD), FadeIn(l1), run_time=0.8)
        cube = Square(0.35, stroke_color=FOOD, stroke_width=3, fill_color=FOOD, fill_opacity=0.8).move_to([-1.2, -1.0, 0])
        sl = T("sugar", 28, FOOD).next_to(cube, UP, buff=0.12)
        self.at("such as sugar")
        self.play(FadeIn(cube, scale=0.5), FadeIn(sl), run_time=0.6)
        self.at("fats")
        self.play(FadeOut(sl), cube.animate.move_to([1.0, -2.1, 0]).scale(0.3), run_time=1.2)
        spark = VGroup(Circle(radius=0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.25),
                       Dot(radius=0.14, color=YELLOW)).move_to([1.0, -2.1, 0])
        l2 = top("energy in a form the cell can use", YELLOW, 32)
        self.at("they release it in a form")
        self.play(FadeOut(cube), FadeIn(spark), FadeOut(l1), FadeIn(l2), run_time=0.5)
        self.play(spark.animate.move_to([0.3, 0.3, 0]), run_time=1.6)
        self.play(FadeOut(spark), run_time=0.3)
        l3 = top("vacuole: stores water, food and wastes", TEXT, 32, t2c={"vacuole": CREAM, "water": CYTO, "food": FOOD, "wastes": "#C49A6C"})
        self.at("a vacuole is a sac")
        self.play(FadeOut(l2), FadeIn(l3), w.vac.animate.set_color(CREAM), run_time=0.8)
        d1 = Dot(radius=0.12, color=CYTO).move_to([VAC_C[0] - 0.25, VAC_C[1] + 0.2, 0])
        d2 = Dot(radius=0.12, color=FOOD).move_to([VAC_C[0] + 0.25, VAC_C[1] + 0.1, 0])
        d3 = Dot(radius=0.12, color="#C49A6C").move_to([VAC_C[0], VAC_C[1] - 0.25, 0])
        self.at("stores water")
        self.play(FadeIn(d1, scale=0.3), run_time=0.4)
        self.at("food and wastes")
        self.play(FadeIn(d2, scale=0.3), run_time=0.4)
        self.at("wastes")
        self.play(FadeIn(d3, scale=0.3), run_time=0.4)
        self.wait(0.5)
        # inset: plant cell beside animal cell
        self.at("plant cells have one large vacuole")
        w.freeze()
        sm = VGroup(*w.parts(), d1, d2, d3)
        pl = RoundedRectangle(corner_radius=0.25, width=5.3, height=3.1, stroke_color=BLUE, stroke_width=6, fill_color=CYTO, fill_opacity=0.25).move_to([-3.4, -0.3, 0])
        big = RoundedRectangle(corner_radius=0.5, width=3.4, height=2.0, stroke_color=CREAM, stroke_width=4, fill_color=CREAM, fill_opacity=0.35).move_to([-3.4, -0.3, 0])
        pn = Circle(radius=0.28, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.35).move_to([-5.45, 1.05, 0])
        pm = bean((-4.9, -1.4), 30, 0.7, 0.3, sw=3)
        lp = T("plant cell: one large vacuole", 30, TEXT, t2c={"vacuole": CREAM}).move_to([-3.4, 1.8, 0])
        self.play(FadeOut(l3), FadeOut(w.motes), sm.animate.scale(0.55).move_to([3.5, -0.3, 0]), FadeIn(pl), FadeIn(pn), FadeIn(pm), run_time=1.0)
        self.play(GrowFromCenter(big), FadeIn(lp), run_time=1.2)
        la = T("animal cell: small sacs", 30, TEXT, t2c={"sacs": CREAM}).move_to([3.5, 1.8, 0])
        sacs = VGroup(*[Circle(radius=r, stroke_color=CREAM, stroke_width=4, fill_color=CREAM, fill_opacity=0.3) for r in (0.18, 0.14, 0.12)])
        c0 = w.vac.get_center()
        for s, off in zip(sacs, ([-0.2, 0.1], [0.2, -0.05], [0.0, -0.25])):
            s.move_to([c0[0] + off[0], c0[1] + off[1], 0])
        self.at("many animal cells")
        self.play(FadeIn(la), FadeOut(d1), FadeOut(d2), FadeOut(d3), ReplacementTransform(w.vac, sacs), run_time=1.5)
        self.finish()


class S05Job(SpokenScene):
    def construct(self):
        w = World(dots=1.0, scroll=True)
        w.add_to(self)
        lab = top("one job: replace a worn-out protein", TEXT, 32, t2c={"worn-out protein": YELLOW})
        worn = chip("worn-out protein", GREY, 26).move_to([0.1, -0.8, 0])
        self.at("give the cell one job")
        self.play(FadeIn(lab), run_time=0.6)
        self.at("worn out protein")
        self.play(FadeIn(worn, scale=0.7), run_time=0.7)
        b1 = badge(1, (-3.6, 1.5))
        self.at("the nucleus holds the instructions")
        self.play(FadeIn(b1), Indicate(w.nuc, color=YELLOW), run_time=1.0)
        l1 = lit((-1.75, 0.75), (-1.15, 0.85))
        self.at("instructions")
        self.play(Create(l1), Indicate(w.scroll, color=YELLOW, scale_factor=1.4), run_time=1.0)
        b2 = badge(2, (-1.5, 1.75))
        self.at("the er helps make")
        self.play(FadeIn(b2), Indicate(w.er.ribbons, color=YELLOW, scale_factor=1.03), run_time=0.9)
        sq = VGroup(*[Square(0.2, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to(w.er.dots[i].get_center()) for i in (1, 5, 9)])
        newp = chip("new protein", TEXT, 24).move_to([1.2, 1.72, 0])
        self.at("new protein")
        self.play(FadeIn(sq, scale=0.5), run_time=0.4)
        self.play(ReplacementTransform(sq, newp), run_time=0.7)
        self.at("move it")
        self.play(newp.animate.move_to([3.2, 1.3, 0]), worn.animate.move_to([-2.0, -1.2, 0]).set_opacity(0.0), run_time=2.0)
        b3 = badge(3, (2.3, 0.05))
        self.at("the mitochondria release")
        self.play(FadeIn(b3), *[Indicate(m, color=YELLOW) for m in w.mitos], run_time=1.0)
        sparks = VGroup(*[Dot(radius=0.13, color=YELLOW).move_to([*p, 0]) for p, _ in MITO])
        self.at("the energy that building uses")
        self.play(FadeIn(sparks), run_time=0.3)
        self.play(*[s.animate.move_to([x, 0.35, 0]) for s, x in zip(sparks, (1.3, 0.3, -0.7))], run_time=1.4)
        self.play(FadeOut(sparks), run_time=0.3)
        b4 = badge(4, (-4.8, 0.4))
        self.at("the membrane")
        self.play(FadeIn(b4), Indicate(w.body, color=YELLOW, scale_factor=1.01), run_time=0.8)
        fa = Arrow([-6.5, -0.7, 0], [-4.4, -0.7, 0], buff=0, color=FOOD, stroke_width=6, max_tip_length_to_length_ratio=0.4)
        fl = T("food", 28, FOOD).move_to([-5.5, -0.25, 0])
        cube = Square(0.32, stroke_color=FOOD, stroke_width=3, fill_color=FOOD, fill_opacity=0.8).move_to([-6.2, -0.7, 0])
        self.at("lets in food")
        self.play(GrowArrow(fa), FadeIn(fl), FadeIn(cube), run_time=0.5)
        self.play(cube.animate.move_to([-3.4, -0.7, 0]), run_time=0.9)
        oa = Arrow([-6.4, -2.9, 0], [-4.3, -2.9, 0], buff=0, color=TEXT, stroke_width=6, max_tip_length_to_length_ratio=0.4)
        ol = T("oxygen", 28, TEXT).move_to([-5.9, -2.4, 0])
        ox = VGroup(*[Circle(radius=0.12, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25).move_to([-6.0 - i * 0.4, -2.9, 0]) for i in range(2)])
        self.at("oxygen")
        p1 = Square(0.2, stroke_color=FOOD, stroke_width=3, fill_color=FOOD, fill_opacity=0.8).move_to([-3.3, -0.7, 0])
        p2 = p1.copy().move_to([-3.0, -0.45, 0])
        self.play(GrowArrow(oa), FadeIn(ol), FadeIn(ox), ReplacementTransform(cube, VGroup(p1, p2)), run_time=0.6)
        self.play(p1.animate.move_to([0.7, -2.0, 0]), p2.animate.move_to([2.8, -0.7, 0]),
                  ox[0].animate.move_to([0.5, -2.8, 0]), ox[1].animate.move_to([3.2, -2.8, 0]), run_time=2.0)
        self.finish()


class S06Team(SpokenScene):
    def construct(self):
        w = World(dots=1.0, scroll=True)
        w.add_to(self)
        t = bottom("4 parts, 1 job", YELLOW, 34, weight=BOLD)
        self.at("four parts")
        self.play(FadeIn(t), Indicate(w.nuc, color=YELLOW), Indicate(w.mitos, color=YELLOW), Indicate(w.body, color=YELLOW, scale_factor=1.01), run_time=1.4)
        pts = [(-2.7, 0.6), (0.3, 0.85), (3.2, -0.7), (1.0, -2.1), (-4.7, -1.2)]
        loop = Polygon(*[[*p, 0] for p in pts], color=YELLOW, stroke_width=5).set_fill(opacity=0)
        self.at("every life job")
        self.play(Create(loop), run_time=1.8)
        self.at("team")
        self.play(Indicate(loop, color=YELLOW), run_time=1.0)
        self.play(FadeOut(loop), run_time=0.4)
        jobs = {"growth": (-4.2, TEAL, [NUC_C, MITO[0][0], ER_C]), "repair": (0.0, YELLOW, [NUC_C, ER_C, MITO[1][0]]),
                "response": (4.2, FIBER, [ER_C, MITO[0][0], (-4.7, -1.2)])}
        lines = VGroup()
        for name, (x, col, tg) in jobs.items():
            lb = T(name, 32, col, weight=BOLD).move_to([x, 3.1, 0])
            ls = VGroup(*[Line([x, 2.8, 0], [*p, 0], color=col, stroke_width=3.5) for p in tg])
            lines.add(ls)
            self.at(name)
            self.play(FadeIn(lb), Create(ls), run_time=0.8)
        self.at("several parts working at once")
        self.play(Indicate(lines, color=WHITE, scale_factor=1.0), run_time=1.2)
        self.finish()


def dim_card_world(w, o=0.28):
    for m in (w.body, w.nuc, w.scroll, w.vac):
        m.set_opacity(o)
    w.er.level.set_value(o)


def flicker(g):
    g._ft = 0.0

    def f(m, dt):
        m._ft += dt
        o = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(m._ft * 9)) * (0.5 + 0.5 * math.sin(m._ft * 3.1 + 1))
        for s in m:
            s.set_stroke(opacity=o)
            s.set_fill(opacity=0.4 * o)
    g.add_updater(f)


def predict_card():
    box = RoundedRectangle(corner_radius=0.2, width=10.4, height=1.7, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=0.96)
    l1 = T("PAUSE AND PREDICT", 28, YELLOW, weight=BOLD)
    l2 = T("If only the mitochondria stop,", 32)
    l3 = T("do other jobs slow down too?", 32)
    txt = VGroup(l1, l2, l3).arrange(DOWN, buff=0.1).move_to(box)
    return VGroup(box, txt).move_to([0, 1.35, 0])


def predict_buttons():
    b1 = chip("only energy use", TEXT, 30).move_to([-1.95, 0.05, 0])
    b2 = chip("other jobs too", TEXT, 30).move_to([1.95, 0.05, 0])
    return VGroup(b1, b2)


class S07Predict(SpokenScene):
    def construct(self):
        w = World(dots=1.0, scroll=True, motes=False)
        w.add_to(self)
        self.at("so what if only the mitochondria stop")
        self.play(*[m.animate.set_opacity(0.28) for m in (w.body, w.nuc, w.scroll, w.vac)], w.er.level.animate.set_value(0.28), run_time=0.8)
        flicker(w.mitos)
        card, btn = predict_card(), predict_buttons()
        self.at("does only energy use slow down")
        self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.7)
        self.at("or do other jobs")
        self.play(FadeIn(btn[0]), run_time=0.4)
        self.play(FadeIn(btn[1]), run_time=0.4)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        w = World(dots=1.0, scroll=True, motes=False)
        dim_card_world(w)
        w.add_to(self)
        flicker(w.mitos)
        card, btn = predict_card(), predict_buttons()
        self.add(card, btn)
        tr = ValueTracker(1.0)
        ring0 = Circle(radius=0.5, stroke_color=GREY, stroke_width=4).move_to([5.95, 1.35, 0])
        ring = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=TAU * max(tr.get_value(), 0.001), stroke_color=YELLOW, stroke_width=8).move_to([5.95, 1.35, 0]))
        self.add(ring0, ring)
        self.play(tr.animate.set_value(0.0), run_time=4.6, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        w = World(dots=1.0, scroll=True)
        w.add_to(self)
        block = chip("protein", TEXT, 24)
        block[0].set_fill(BG, 1.0)
        block._t = 1.01

        def mv(m, dt):
            m._t += dt
            f = (m._t % 3.0) / 3.0
            m.move_to([-0.7 + 2.4 * f, 0.85, 0])
        block.add_updater(mv)
        sparks = VGroup(*[Dot(radius=0.13, color=YELLOW) for _ in MITO])
        for i, (s, (p, _)) in enumerate(zip(sparks, MITO)):
            s._t = i * 0.5
            s._p = np.array([*p, 0.0])

            def sm(m, dt):
                m._t += dt
                f = (m._t % 1.5) / 1.5
                m.move_to(m._p + (np.array([0.3, 0.35, 0]) - m._p) * f)
            s.add_updater(sm)
        self.add(block, sparks)
        trs = {k: ValueTracker(1.0) for k in ("growth", "repair", "response")}
        cols = {"growth": TEAL, "repair": YELLOW, "response": FIBER}
        xs = {"growth": -6.4, "repair": -2.2, "response": 2.0}
        bars = VGroup()
        for k in trs:
            lb = T(k, 28, cols[k], weight=BOLD).move_to([xs[k], 3.1, 0], aligned_edge=LEFT)
            fr = Rectangle(width=2.0, height=0.32, stroke_color=TEXT, stroke_width=2).move_to([xs[k] + 2.95, 3.1, 0])
            fl = always_redraw(lambda k=k, fr=fr: Rectangle(width=max(2.0 * trs[k].get_value(), 0.01), height=0.32, stroke_width=0,
                                                            fill_color=cols[k], fill_opacity=0.9).align_to(fr, LEFT).move_to([0, 3.1, 0], coor_mask=[0, 1, 0]))
            bars.add(VGroup(lb, fr, fl))
        self.at("other jobs slow down too")
        self.play(w.mitos.animate.set_color(GREY), FadeOut(sparks), run_time=1.2)
        t1 = bottom("other jobs slow too", YELLOW, 30, weight=BOLD)
        self.play(FadeIn(bars), FadeIn(t1), run_time=0.8)
        self.at("the nucleus and the er")
        ring_n = Circle(radius=1.1, stroke_color=PURPLE, stroke_width=6).move_to([*NUC_C, 0])
        ring_e = RoundedRectangle(corner_radius=0.3, width=3.3, height=1.5, stroke_color=GREEN, stroke_width=6).move_to([*ER_C, 0])
        self.play(ShowPassingFlash(ring_n, time_width=0.8), ShowPassingFlash(ring_e, time_width=0.8), run_time=1.8)
        self.at("still fine")
        self.play(Indicate(w.nuc, color=PURPLE), run_time=1.0)
        self.at("but building needs energy")
        block.clear_updaters()
        self.play(block.animate.shift(RIGHT * 0.25), run_time=1.6, rate_func=rush_from)
        self.at("the repair path slows and stalls")
        self.play(trs["repair"].animate.set_value(0.5), run_time=1.8)
        self.at("growth and response slow down with it")
        self.play(trs["growth"].animate.set_value(0.6), run_time=1.2)
        self.play(trs["response"].animate.set_value(0.45), run_time=1.2)
        t2 = bottom("no part decides anything", TEXT, 30)
        self.at("no part decides anything")
        self.play(FadeOut(t1), FadeIn(t2), Indicate(w.er.ribbons, color=GREEN, scale_factor=1.02), run_time=1.0)
        t3 = bottom("each part simply follows chemistry", TEXT, 30)
        self.at("each one simply follows chemistry")
        self.play(FadeOut(t2), FadeIn(t3), run_time=0.6)
        self.finish()


def fib_label(room):
    t = T("muscle fibres\nthat contract", 28, TEXT).move_to(room.get_center())
    bg = Rectangle(width=t.width + 0.3, height=t.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(t)
    return VGroup(bg, t)


def room_label(room, text, col=TEXT, size=26):
    return T(text, size, col).move_to(room.get_center())


class S10Space(SpokenScene):
    def construct(self):
        w = World(mito=GREY, dots=1.0, scroll=True)
        w.add_to(self)
        self.at("here is the second idea")
        self.play(w.mitos.animate.set_color(GOLD), run_time=1.0)
        l1 = top("second idea", YELLOW, 34, weight=BOLD)
        self.at("second idea")
        self.play(FadeIn(l1), run_time=0.5)
        w.freeze()
        base, rooms = floor(GEN)
        l2 = top("floor plan = shares of the cell", TEXT, 30, t2c={"floor plan": BLUE}).move_to([-3.2, 3.1, 0])
        self.at("picture the cell from above")
        self.play(ReplacementTransform(w.body, base), FadeTransform(w.nuc, rooms[0]), FadeTransform(w.er, rooms[1]),
                  FadeTransform(w.mitos[0], rooms[2]), FadeTransform(w.mitos[1], rooms[3]), FadeTransform(w.mitos[2], rooms[4]),
                  FadeTransform(w.vac, rooms[5]), FadeOut(w.scroll), FadeOut(w.motes), FadeOut(l1), FadeIn(l2), run_time=2.4)
        self.add(rooms[6])
        labs = VGroup(room_label(rooms[0], "nucleus"), room_label(rooms[1], "ER"), room_label(rooms[2], "mitochondria", size=24),
                      room_label(rooms[5], "vacuole", BG))
        self.at("each part is a room")
        self.play(LaggedStart(*[FadeIn(x, scale=0.8) for x in labs], lag_ratio=0.5), run_time=2.0)
        tal = tally(GEN, TAL_C, TAL_W)
        tf = tally_frame(TAL_C, TAL_W)
        pc = T("100%", 28, TEXT, weight=BOLD).move_to([5.8, 3.1, 0])
        self.at("together the rooms make up the whole cell")
        self.play(LaggedStart(*[Indicate(r, color=WHITE, scale_factor=1.05) for r in rooms[:6]], lag_ratio=0.15),
                  FadeIn(tf), LaggedStart(*[GrowFromEdge(s, LEFT) for s in tal], lag_ratio=0.15), FadeIn(pc), run_time=2.2)
        self.finish()


def floor_scene_base(scene, spec, label, tal_spec=None):
    base, rooms = floor(spec)
    scene.add(base, rooms)
    l = T(label, 30, TEXT, t2c={"floor plan": BLUE}).move_to([-3.2, 3.1, 0])
    tal = tally(tal_spec or spec, TAL_C, TAL_W)
    tf = tally_frame(TAL_C, TAL_W)
    pc = T("100%", 28, TEXT, weight=BOLD).move_to([5.8, 3.1, 0])
    scene.add(l, tal, tf, pc)
    return base, rooms, l, tal, tf, pc


class S11Choose(SpokenScene):
    def construct(self):
        base, rooms, l, tal, tf, pc = floor_scene_base(self, GEN, "floor plan = shares of the cell")
        note = bottom("schematic: a picture of shares; real cells also grow and shrink", TEXT, 26)
        self.play(FadeIn(note), run_time=0.5)
        _, ra = floor(SPEC_A)
        self.at("so when one room takes a big share")
        self.play(*[Transform(rooms[i], ra[i]) for i in range(7)], Transform(tal, tally(SPEC_A, TAL_C, TAL_W)), run_time=3.0)
        _, rb = floor(SPEC_B)
        l2 = T("cells with different jobs: often different amounts", 30, TEXT).move_to([-1.5, 3.1, 0])
        l2 = fit(l2, max_w=7.6)
        l2.move_to([-2.4, 3.1, 0])
        self.at("cells with different jobs")
        self.play(*[Transform(rooms[i], rb[i]) for i in range(7)], Transform(tal, tally(SPEC_B, TAL_C, TAL_W)), FadeOut(l), FadeIn(l2), run_time=2.6)
        self.finish()


class S12Heart(SpokenScene):
    def construct(self):
        base, rooms, l, tal, tf, pc = floor_scene_base(self, SPEC_B, "cells with different jobs: often different amounts")
        l.become(fit(T("cells with different jobs: often different amounts", 30, TEXT), max_w=7.6).move_to([-2.4, 3.1, 0]))
        icon = heart_icon((-6.2, 3.1), 0.6)
        _, r1 = floor(HEART1)
        st = stripes(HEART1).set_opacity(0)
        self.add(st)
        hl = T("heart muscle cell", 32, TEXT, weight=BOLD).move_to([-3.2, 3.1, 0])
        self.at("a heart muscle cell")
        self.play(*[Transform(rooms[i], r1[i]) for i in range(7)], Transform(tal, tally(HEART1, TAL_C, TAL_W)),
                  FadeOut(l), FadeIn(hl), FadeIn(icon), run_time=1.2)
        pulse(icon, 0.9, 0.18)
        job = bottom("job: work without a break", YELLOW, 30)
        self.at("works without a break")
        self.play(FadeIn(job), st.animate.set_opacity(0.6), run_time=0.9)
        fl = fib_label(rooms[6])
        self.play(FadeIn(fl), run_time=0.6)
        self.at("it releases a lot of energy")
        self.play(*[Indicate(rooms[i], color=YELLOW, scale_factor=1.15) for i in (2, 3, 4)], run_time=1.4)
        self.at("mostly from fats")
        self.play(*[Indicate(rooms[i], color=YELLOW, scale_factor=1.08) for i in (2, 3)], run_time=1.2)
        _, r2 = floor(HEART2)
        gl = T("mitochondria", 24, TEXT)
        self.at("so mitochondria fill")
        self.play(*[Transform(rooms[i], r2[i]) for i in range(7)], Transform(tal, tally(HEART2, TAL_C, TAL_W)), run_time=2.0)
        gl.move_to(rooms[2].get_center())
        self.play(FadeIn(gl), Indicate(rooms[2], color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.finish()


HP_C, HP_W, HP_H = (-3.7, -0.1), 5.0, 2.9
FP_C, FP_W, FP_H = (3.9, -0.1), 3.8, 3.8


class S13Fat(SpokenScene):
    def construct(self):
        base, rooms = floor(HEART2)
        st = stripes(HEART2).set_opacity(0.6)
        tal = tally(HEART2, TAL_C, TAL_W)
        tf = tally_frame(TAL_C, TAL_W)
        pc = T("100%", 28, TEXT, weight=BOLD).move_to([5.8, 3.1, 0])
        hl = T("heart muscle cell", 32, TEXT, weight=BOLD).move_to([-3.2, 3.1, 0])
        icon = heart_icon((-6.2, 3.1), 0.6)
        job = bottom("job: work without a break", YELLOW, 30)
        gl = T("mitochondria", 24, TEXT).move_to(rooms[2].get_center())
        fl = fib_label(rooms[6])
        self.add(base, rooms, st, tal, tf, pc, hl, icon, job, gl, fl)
        pulse(icon, 0.9, 0.18)
        # shrink the heart plan to the left half
        hb, hr = floor(HEART2, HP_C, HP_W, HP_H)
        hst = stripes(HEART2, HP_C, HP_W, HP_H).set_opacity(0.6)
        htal = tally(HEART2, (HP_C[0], 2.35), 4.2)
        htf = tally_frame((HP_C[0], 2.35), 4.2)
        hpc = T("100%", 26, TEXT, weight=BOLD).move_to([-0.95, 2.35, 0])
        hl2 = T("heart muscle cell", 32, TEXT, weight=BOLD).move_to([HP_C[0], 3.1, 0])
        hjob = T("job: work without a break", 28, YELLOW).move_to([HP_C[0], -2.4, 0])
        fb, fr = floor(GEN, FP_C, FP_W, FP_H)
        slide = VGroup(fb, fr)
        fl_ = T("white fat cell", 32, TEXT, weight=BOLD).move_to([FP_C[0], 3.1, 0])
        ftal = tally(GEN, (FP_C[0] - 0.3, 2.35), 3.2)
        ftf = tally_frame((FP_C[0] - 0.3, 2.35), 3.2)
        fpc = T("100%", 26, TEXT, weight=BOLD).move_to([FP_C[0] + 2.0, 2.35, 0])
        note = bottom("drawn the same size, not to real scale", TEXT, 26)
        slide.shift(RIGHT * 9)
        self.add(slide)
        self.play(slide.animate.shift(LEFT * 9), FadeIn(fl_), FadeIn(ftal), FadeIn(ftf), FadeIn(fpc), FadeIn(note),
                  FadeOut(gl), FadeOut(fl), FadeOut(job), ReplacementTransform(base, hb),
                  *[Transform(rooms[i], hr[i]) for i in range(7)], Transform(st, hst), Transform(tal, htal), Transform(tf, htf),
                  Transform(pc, hpc), Transform(hl, hl2), icon.animate.move_to([-6.2, 3.1, 0]), FadeIn(hjob), run_time=1.4)
        self.at("a white fat cell")
        fjob = T("job: store fat", 28, YELLOW).move_to([FP_C[0], -2.4, 0])
        self.at("stores fat")
        self.play(FadeIn(fjob), run_time=0.6)
        _, ff = floor(FAT, FP_C, FP_W, FP_H)
        fa = T("fat drop", 26, BG, weight=BOLD)
        self.at("one big fat drop")
        self.play(*[Transform(fr[i], ff[i]) for i in range(7)], Transform(ftal, tally(FAT, (FP_C[0] - 0.3, 2.35), 3.2)), run_time=2.4)
        fa.move_to(fr[5].get_center())
        self.play(FadeIn(fa), run_time=0.5)
        self.at("the other parts")
        self.play(*[Indicate(fr[i], color=YELLOW, scale_factor=1.3) for i in (0, 1, 2, 3, 4)], run_time=1.8)
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        hb, hr = floor(HEART2, HP_C, HP_W, HP_H)
        hst = stripes(HEART2, HP_C, HP_W, HP_H).set_opacity(0.6)
        htal = tally(HEART2, (HP_C[0], 2.35), 4.2)
        htf = tally_frame((HP_C[0], 2.35), 4.2)
        hpc = T("100%", 26, TEXT, weight=BOLD).move_to([-0.95, 2.35, 0])
        hl = T("heart muscle cell", 32, TEXT, weight=BOLD).move_to([HP_C[0], 3.1, 0])
        hjob = T("job: work without a break", 28, YELLOW).move_to([HP_C[0], -2.4, 0])
        fb, fr = floor(FAT, FP_C, FP_W, FP_H)
        ftal = tally(FAT, (FP_C[0] - 0.3, 2.35), 3.2)
        ftf = tally_frame((FP_C[0] - 0.3, 2.35), 3.2)
        fpc = T("100%", 26, TEXT, weight=BOLD).move_to([FP_C[0] + 2.0, 2.35, 0])
        fl = T("white fat cell", 32, TEXT, weight=BOLD).move_to([FP_C[0], 3.1, 0])
        fjob = T("job: store fat", 28, YELLOW).move_to([FP_C[0], -2.4, 0])
        fat_lab = T("fat drop", 26, BG, weight=BOLD).move_to(fr[5].get_center())
        icon = heart_icon((-6.2, 3.1), 0.6)
        self.add(hb, hr, hst, htal, htf, hpc, hl, hjob, fb, fr, ftal, ftf, fpc, fl, fjob, fat_lab, icon)
        pulse(icon, 0.9, 0.18)
        self.at("many of the same parts")
        self.play(LaggedStart(*[Indicate(r, color=WHITE, scale_factor=1.12) for r in list(hr[:6]) + list(fr[:6])], lag_ratio=0.08), run_time=2.2)
        self.at("floor plans")
        self.play(Indicate(hb, color=YELLOW, scale_factor=1.02), Indicate(fb, color=YELLOW, scale_factor=1.02), run_time=0.6)
        hc, fc = heart_cartoon(HC), fat_cartoon(FC)
        icon.clear_updaters()
        self.play(FadeOut(hr), FadeOut(hst), FadeOut(htal), FadeOut(htf), FadeOut(hpc), FadeOut(hjob), FadeOut(icon),
                  FadeOut(fr), FadeOut(ftal), FadeOut(ftf), FadeOut(fpc), FadeOut(fjob), FadeOut(fat_lab),
                  ReplacementTransform(hb, hc[0]), ReplacementTransform(fb, fc[0]),
                  FadeIn(hc[1]), FadeIn(hc[2]), FadeIn(fc[1]), FadeIn(fc[2]), FadeIn(fc[3]),
                  hl.animate.move_to([HC[0], -2.0, 0]), fl.animate.move_to([FC[0], -2.3, 0]), run_time=1.4)
        pulse(hc[2], 0.9, 0.04)
        self.at("a part size alone")
        self.play(Indicate(hc[2], color=YELLOW, scale_factor=1.06), Indicate(fc[1], color=YELLOW, scale_factor=1.05), run_time=1.4)
        jl = T("job", 40, YELLOW, weight=BOLD).move_to([0.5, -0.1, 0])
        a1 = Arrow([0.1, -0.1, 0], [-1.45, -0.1, 0], buff=0, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow([0.9, -0.1, 0], [2.45, -0.1, 0], buff=0, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        self.at("cell's job")
        self.play(FadeIn(jl), GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        self.at("but comparing parts with jobs")
        self.play(Indicate(a1, color=WHITE, scale_factor=1.1), Indicate(a2, color=WHITE, scale_factor=1.1), run_time=1.2)
        pt = bottom("a pattern, not a rule for every cell", TEXT, 28)
        self.at("a pattern")
        self.play(FadeIn(pt), run_time=0.6)
        self.finish()


class S15End(EndCard):
    LINE = "Parts work as a team; cells with different jobs hold different amounts."
