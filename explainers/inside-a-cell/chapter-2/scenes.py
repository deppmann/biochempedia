"""Counting Dots to Measure a Cell (Biochemistrypedia, Life Science grade 7, film 2 of 2).

COLOUR MAP (same as film 1): cell membrane BLUE; cytoplasm PALE BLUE; nucleus PURPLE; ER GREEN;
mitochondria GOLD; fat drop CREAM; muscle fibres PINK. Grid dots start HOLLOW GREY, turn GOLD on
mitochondria (CREAM on fat). Every picture is a schematic cartoon.
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CREAM = "#F1E6C4"
CYTO = "#8FC1E3"
FIBER = "#E58FB5"
RIBO = "#F5EBD0"
PICFILL = "#3B4048"
DOTC = "#B8BFCC"

CX, CY, CW, CH = 0.0, -0.5, 9.6, 5.2
PIC_C = np.array([0.0, -0.55, 0.0])
PW, PH = 8.8, 4.4
SP = 0.76
BAR_X0, BAR_W, BAR_Y = -5.8, 11.6, -2.85


def top(text, color=TEXT, size=30, y=3.1, **kw):
    t = T(text, size, color, **kw).move_to([0, y, 0])
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


def make_motes(n=10, seed=1, xr=(-4.3, 4.3), yr=(-2.8, 1.7), speed=0.5, col="#CFE8F7"):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=0.07, color=col).set_opacity(0.55)
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


# ------------------------------------------------------------- cartoons and floor plans (as film 1)
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


ORDER = ["nuc", "er", "m1", "m2", "m3", "vac", "fib"]
ROOMCOL = dict(nuc=PURPLE, er=GREEN, m1=GOLD, m2=GOLD, m3=GOLD, vac=CREAM, fib=FIBER)
NONE = (0.5, 0.5, 0.5, 0.5)
HEART2 = dict(fib=(.50, .06, .96, .60), nuc=(.55, .68, .70, .92), er=(.74, .70, .96, .78), vac=(.82, .84, .88, .90),
              m1=(.03, .06, .28, .94), m2=(.31, .06, .40, .94), m3=(.43, .06, .47, .30))
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


def stripes(spec, c, w, h, n=10):
    x0, y0, x1, y1 = spec["fib"]
    g = VGroup()
    for i in range(n):
        x = c[0] - w / 2 + (x0 + (i + 1) / (n + 1) * (x1 - x0)) * w
        ya, yb = c[1] - h / 2 + (y0 + 0.03) * h, c[1] - h / 2 + (y1 - 0.03) * h
        g.add(Line([x, ya, 0], [x, yb, 0], color=RIBO, stroke_width=3).set_opacity(0.35))
    return g


def plan(spec, c, w, h, seed=3):
    """A whole floor plan as one VGroup: base, rooms, stripes (heart only), drifting motes."""
    base, rooms = floor(spec, c, w, h)
    g = VGroup(base, rooms)
    if spec["fib"] != NONE:
        g.add(stripes(spec, c, w, h))
    g.add(make_motes(7, seed, (c[0] - w / 2 + 0.2, c[0] + w / 2 - 0.2), (c[1] - h / 2 + 0.2, c[1] + h / 2 - 0.2), 0.35))
    g.base, g.rooms = base, rooms
    return g


# ------------------------------------------------------------- the slice picture (one world)
def stadium_hit(p, c, ang, w, h):
    """Is point p inside the bean (stadium) of centre c, angle ang (deg), length w, width h?"""
    a = ang * DEGREES
    d = np.array(p[:2]) - np.array(c[:2])
    u = d[0] * math.cos(a) + d[1] * math.sin(a)
    v = -d[0] * math.sin(a) + d[1] * math.cos(a)
    half = max(w - h, 0) / 2
    u = max(-half, min(half, u))
    return (d[0] * math.cos(a) + d[1] * math.sin(a) - u) ** 2 + v ** 2 <= (h / 2) ** 2


LATT = [(i, j) for j in range(5) for i in range(11)]
LPOS = lambda i, j: np.array([(i - 5) * SP, (j - 2) * SP, 0.0]) + PIC_C   # lattice, relative to PIC_C


def gen_heart_mitos(seed=11):
    rng = random.Random(seed)
    out = []
    tries = 0
    while len(out) < 14 and tries < 5000:
        tries += 1
        c = (rng.uniform(-3.7, 3.7), rng.uniform(-1.6, 1.6))
        ang = rng.uniform(-60, 60)
        if all(math.hypot(c[0] - o[0][0], c[1] - o[0][1]) > 1.45 for o in out):
            out.append((c, ang))
    return out


HEART_MITOS = gen_heart_mitos()
MW, MH = 1.35, 0.68


def pic_frame(c=PIC_C, w=PW, h=PH):
    return Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=4, fill_color=PICFILL, fill_opacity=1).move_to(np.array(c)[:3])


def heart_pic():
    """Frame + gold-outlined mitochondria. Returns VGroup with .mitos."""
    fr = pic_frame()
    ms = VGroup(*[bean((PIC_C[0] + c[0], PIC_C[1] + c[1]), a, MW, MH, sw=3, op=0.2) for c, a in HEART_MITOS])
    g = VGroup(fr, ms)
    g.frame, g.mitos = fr, ms
    return g


def heart_hits():
    return {(i, j): any(stadium_hit(LPOS(i, j) - PIC_C, c, a, MW, MH) for c, a in HEART_MITOS) for i, j in LATT}


def make_dots(positions, r=0.1):
    return VGroup(*[Circle(radius=r, stroke_color=DOTC, stroke_width=3, fill_color=DOTC, fill_opacity=0).move_to(p) for p in positions])


def heart_dots():
    return make_dots([LPOS(i, j) for i, j in LATT])


def goldify(d, col=GOLD):
    return d.animate.set_fill(col, 1).set_stroke(col)


def sweep(frame, period=6.0):
    """A faint light band that crosses a picture forever, so a held picture is never a dead frame."""
    b = Rectangle(width=0.14, height=frame.height - 0.1, stroke_width=0, fill_color=WHITE, fill_opacity=0.09)
    b._t = 0.0
    x0, x1 = frame.get_left()[0] + 0.1, frame.get_right()[0] - 0.1
    b.move_to([x0, frame.get_center()[1], 0])

    def f(m, dt):
        m._t += dt
        m.move_to([x0 + (x1 - x0) * ((m._t % period) / period), frame.get_center()[1], 0])
    b.add_updater(f)
    return b


def fat_pic():
    fr = pic_frame()
    cell = RoundedRectangle(corner_radius=1.6, width=8.5, height=4.2, stroke_color=BLUE, stroke_width=4,
                            fill_color=CYTO, fill_opacity=0.25).move_to(PIC_C)
    drop = RoundedRectangle(corner_radius=1.3, width=7.8, height=3.5, stroke_color=CREAM, stroke_width=3,
                            fill_color=CREAM, fill_opacity=0.5).move_to(PIC_C + np.array([0.15, 0, 0]))
    nuc = Ellipse(width=0.45, height=1.7, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.55).move_to(PIC_C + np.array([-4.05, 0.55, 0]))
    ms = VGroup(bean((PIC_C[0] - 3.92, PIC_C[1] - 0.76), 90, 0.62, 0.34, sw=2, op=0.35),
                bean((PIC_C[0] + 1.0, PIC_C[1] - 1.93), 0, 0.55, 0.2, sw=2, op=0.35),
                bean((PIC_C[0] + 3.2, PIC_C[1] + 1.93), 0, 0.55, 0.2, sw=2, op=0.35))
    g = VGroup(fr, cell, drop, nuc, ms)
    g.frame, g.drop, g.nuc, g.mitos = fr, drop, nuc, ms
    return g


def fat_class(i, j):
    p = LPOS(i, j)
    specs = [(PIC_C[0] - 3.92, PIC_C[1] - 0.76, 90, 0.62, 0.34), (PIC_C[0] + 1.0, PIC_C[1] - 1.93, 0, 0.55, 0.2),
             (PIC_C[0] + 3.2, PIC_C[1] + 1.93, 0, 0.55, 0.2)]
    if any(stadium_hit(p, (x, y), a, w, h) for x, y, a, w, h in specs):
        return "gold"
    d = np.array(p[:2]) - np.array(PIC_C[:2]) - np.array([0.15, 0])
    hw, hh, r = 3.9, 1.75, 1.3
    q = np.abs(d) - np.array([hw - r, hh - r])
    dist = math.hypot(max(q[0], 0), max(q[1], 0)) + min(max(q[0], q[1]), 0) - r
    return "cream" if dist <= 0 else "hollow"


FAT_MITO_REF = list(fat_pic().mitos)


def card(seed, w=2.3, h=1.5, k=1.0):
    rng = random.Random(seed)
    fr = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_color=PICFILL, fill_opacity=1)
    ms = VGroup(*[bean((rng.uniform(-0.8, 0.8), rng.uniform(-0.45, 0.45)), rng.uniform(-50, 50), 0.5, 0.25, sw=2, op=0.2) for _ in range(5)])
    ds = VGroup(*[Dot(radius=0.04, color=DOTC).move_to([(i - 2.5) * 0.36, (j - 1) * 0.36, 0]) for i in range(6) for j in range(3)])
    return VGroup(fr, ms, ds).scale(k)


def mammal(s=1.0):
    body = Ellipse(width=0.8, height=0.42, stroke_color=TEXT, stroke_width=2, fill_color=GREY, fill_opacity=0.55)
    head = Circle(radius=0.17, stroke_color=TEXT, stroke_width=2, fill_color=GREY, fill_opacity=0.55).move_to([0.45, 0.16, 0])
    ear = Triangle(stroke_color=TEXT, stroke_width=2, fill_color=GREY, fill_opacity=0.55).scale(0.07).move_to([0.5, 0.33, 0])
    legs = VGroup(*[Line([x, -0.18, 0], [x, -0.42, 0], color=TEXT, stroke_width=3) for x in (-0.28, -0.12, 0.12, 0.28)])
    tail = Line([-0.4, 0.05, 0], [-0.65, 0.22, 0], color=TEXT, stroke_width=3)
    return VGroup(legs, tail, body, head, ear).scale(s)


def bar_x(pct):
    return BAR_X0 + BAR_W * pct / 100.0


def scale_bar():
    fr = Rectangle(width=BAR_W, height=0.26, stroke_color=TEXT, stroke_width=2).move_to([BAR_X0 + BAR_W / 2, BAR_Y, 0])
    ticks = VGroup(*[T(f"{p}%", 22, TEXT).move_to([bar_x(p), BAR_Y - 0.4, 0]) for p in (0, 50, 100)])
    return VGroup(fr, ticks)


def band(lo, hi, op=0.0):
    return Rectangle(width=bar_x(hi) - bar_x(lo), height=0.26, stroke_color=GOLD, stroke_width=3,
                     fill_color=GOLD, fill_opacity=op).move_to([(bar_x(lo) + bar_x(hi)) / 2, BAR_Y, 0])


def make_toy():
    """Toy picture (left), 5 x 4 grid with exactly 6 dots on mitochondria."""
    C = np.array([-2.9, 0.5, 0.0])
    fr = Rectangle(width=5.6, height=4.0, stroke_color=GREY, stroke_width=4, fill_color=PICFILL, fill_opacity=1).move_to(C)
    pos = {(i, j): C + np.array([(i - 2) * 1.0, (j - 1.5) * 1.0, 0]) for i in range(5) for j in range(4)}
    onm = [(0, 1), (1, 3), (2, 0), (3, 2), (4, 3), (4, 0)]
    offs = {(0, 1): (0.1, 0.05, 15), (1, 3): (-0.1, 0.0, -10), (2, 0): (0.05, 0.08, 5), (3, 2): (0.12, -0.05, 20), (4, 3): (-0.08, 0.1, 0), (4, 0): (0.05, -0.05, -15)}
    ms = VGroup(*[bean((pos[k][0] + offs[k][0], pos[k][1] + offs[k][1]), offs[k][2], 1.1, 0.56, sw=3, op=0.2) for k in onm])
    hits = [any(stadium_hit(pos[(i, j)] - np.array([offs[k][0], offs[k][1], 0]) - pos[k], (0, 0), offs[k][2], 1.1, 0.56) for k in onm) for i, j in pos]
    n = sum(any(stadium_hit(pos[(i, j)], (pos[k][0] + offs[k][0], pos[k][1] + offs[k][1]), offs[k][2], 1.1, 0.56) for k in onm) for i, j in pos)
    assert n == 6, n
    dots = VGroup(*[Circle(radius=0.11, stroke_color=DOTC, stroke_width=3, fill_color=DOTC, fill_opacity=0).move_to(pos[(i, j)]) for j in range(4) for i in range(5)])
    gold_idx = [j * 5 + i for j in range(4) for i in range(5) if any(stadium_hit(pos[(i, j)], (pos[k][0] + offs[k][0], pos[k][1] + offs[k][1]), offs[k][2], 1.1, 0.56) for k in onm)]
    return fr, ms, dots, gold_idx


def counter(label, col, y):
    return T(label, 28, col).move_to([2.3, y, 0], aligned_edge=LEFT)


# ================================================================= scenes
class S00Title(TitleCard):
    LESSON = "Inside a cell"
    TITLE = "Counting Dots to Measure a Cell"


class S01Link(SpokenScene):
    def construct(self):
        base, rooms = floor(HEART2)
        pl = VGroup(base, rooms, stripes(HEART2, (CX, CY), CW, CH))
        self.play(FadeIn(pl), run_time=1.0)
        # ambient motion: motes drifting through the plan
        mo = make_motes(8, 5, (-4.4, 4.4), (-2.9, 1.9), 0.4)
        self.add(mo)
        self.at("but how much of a cell")
        self.play(FadeOut(mo), pl.animate.scale(0.3).move_to([-5.0, 2.85, 0]), run_time=1.4)
        # cup
        cup = VGroup(Polygon([-1.1, 1.6, 0], [1.1, 1.6, 0], [0.85, -1.5, 0], [-0.85, -1.5, 0], stroke_color=TEXT, stroke_width=4,
                             fill_color=TEAL, fill_opacity=0.12),
                     *[Line([-0.95 + 0.02 * k, y, 0], [-0.55 + 0.02 * k, y, 0], color=TEXT, stroke_width=3) for k, y in enumerate((0.9, 0.2, -0.5))]).scale(1.15).move_to([3.2, -1.1, 0])
        cell = heart_cartoon((-2.6, -0.2)).scale(0.65)
        self.at("you can't pour a cell")
        self.play(FadeIn(cup, shift=UP * 0.3), FadeIn(cell), run_time=1.2)
        pulse(cell[2], 1.0, 0.05)
        self.at("into a measuring cup")
        cell[2].clear_updaters()
        self.play(cell.animate.move_to([3.2, 2.0, 0]).rotate(-0.5), run_time=1.5)
        self.play(cell.animate.shift(DOWN * 0.1), run_time=0.2)
        self.play(cell.animate.shift(UP * 0.25), run_time=0.4)
        self.play(Wiggle(cell, scale_value=1.04, rotation_angle=0.05), run_time=0.6)
        self.at("so how do scientists")
        self.play(cell.animate.rotate(0.5).move_to([-2.6, -0.2, 0]), run_time=1.4)
        q = T("?", 150, YELLOW, weight=BOLD).move_to([3.2, 1.9, 0])
        lab = bottom("how much is mitochondria?", TEXT, 32, t2c={"mitochondria": GOLD}).move_to([0.4, -3.3, 0])
        self.at("how much of a cell is mitochondria")
        self.play(FadeIn(q, scale=0.4), FadeIn(lab), run_time=0.8)
        pulse(q, 1.1, 0.12)
        self.at("mitochondria")
        self.play(*[Indicate(b, color=YELLOW, scale_factor=1.3) for b in cell[2]], run_time=1.5)
        self.finish()


class S02Slice(SpokenScene):
    def construct(self):
        cell = heart_cartoon((0, 0.1)).scale(0.9)
        self.at("first")
        self.play(FadeIn(cell), run_time=1.0)
        pulse(cell[2], 0.9, 0.05)
        self.at("they preserve the cell")
        cell[2].clear_updaters()
        stamp = T("preserved", 34, YELLOW, weight=BOLD).rotate(0.18)
        sb = RoundedRectangle(corner_radius=0.1, width=stamp.width + 0.4, height=stamp.height + 0.3, stroke_color=YELLOW, stroke_width=4).rotate(0.18)
        st = VGroup(sb, stamp).move_to([3.7, 2.2, 0])
        self.play(FadeIn(st, scale=1.5), cell.animate.set_opacity(0.85), run_time=0.9)
        self.at("cut a very thin slice")
        blade = Rectangle(width=5.6, height=0.07, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to([0, 2.4, 0])
        self.play(FadeIn(blade), run_time=0.3)
        self.play(blade.animate.move_to([0, 0.1, 0]), run_time=1.0)
        slc = Rectangle(width=4.5, height=0.2, stroke_color=TEXT, stroke_width=3, fill_color=CYTO, fill_opacity=0.6).move_to([0, 0.1, 0])
        self.add(slc)
        self.play(FadeOut(blade), slc.animate.shift(UP * 2.0), run_time=0.9)
        # microscope
        self.at("a transmission electron microscope")
        gun = Rectangle(width=1.8, height=0.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([-3.6, 2.3, 0])
        tube1 = Rectangle(width=0.9, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([-3.6, 1.35, 0])
        tube2 = Rectangle(width=0.9, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([-3.6, -0.9, 0])
        det = Rectangle(width=2.4, height=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([-3.6, -1.9, 0])
        micro = VGroup(gun, tube1, tube2, det)
        lab = top("transmission electron microscope", TEXT, 32, y=3.35)
        self.play(FadeOut(cell), FadeOut(st), FadeIn(micro), FadeIn(lab), slc.animate.scale(0.52).move_to([-3.6, 0.2, 0]), run_time=2.0)
        beam = VGroup(*[Dot(radius=0.07, color=TEAL) for _ in range(8)])
        for k, d in enumerate(beam):
            d._ph = k / 8.0

            def f(m, dt, k=k):
                m._ph = (m._ph + dt * 0.45) % 1.0
                y = 2.0 - 3.9 * m._ph
                spread = 0.12 * (k - 3.5) * (0.5 if y > 0.2 else 1.0)
                m.move_to([-3.6 + spread, y, 0])
            d.add_updater(f)
        self.at("sends a beam of electrons")
        el = T("electrons", 28, TEAL).move_to([-1.5, 1.4, 0])
        self.add(beam)
        self.play(FadeIn(el), run_time=0.6)
        self.at("it shows small organelles")
        pic = heart_pic().scale(0.62).move_to([2.6, -0.1, 0])
        sw = sweep(pic.frame, 5.0)
        self.play(FadeIn(pic), run_time=1.2)
        self.add(sw)
        self.at("that a school microscope cannot")
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.25) for m in list(pic.mitos)[:6]], run_time=1.6)
        self.at("because the cell was preserved")
        sw.clear_updaters()
        self.remove(sw)
        for d in beam:
            d.clear_updaters()
        self.play(FadeOut(micro), FadeOut(slc), FadeOut(el), FadeOut(beam), FadeOut(lab), run_time=0.6)
        self.play(pic.animate.scale(1 / 0.62).move_to(PIC_C), run_time=1.0)
        sw2 = sweep(pic.frame)
        self.add(sw2)
        l2 = bottom("a preserved slice, not a living cell", TEXT, 32)
        self.at("each picture is a still view")
        self.play(FadeIn(l2), run_time=0.6)
        self.finish()


class S03Grid(SpokenScene):
    def construct(self):
        pic = heart_pic()
        sw = sweep(pic.frame)
        self.add(pic, sw)
        self.at("point counting")
        l1 = top("point counting", YELLOW, 40, weight=BOLD)
        self.play(FadeIn(l1), run_time=0.6)
        dots = heart_dots()
        hits = heart_hits()
        self.at("lay an even grid of dots over the picture")
        for d in dots:
            d.shift(UP * 2.5).set_opacity(0)
        self.play(LaggedStart(*[d.animate.shift(DOWN * 2.5).set_opacity(1) for d in dots], lag_ratio=0.03), run_time=2.2)
        self.at("then look at where each dot lands")
        on = next(k for k, (i, j) in enumerate(LATT) if hits[(i, j)] and 2 <= i <= 8)
        i0, j0 = LATT[on]
        off = next(k for k, (i, j) in enumerate(LATT) if not hits[(i, j)] and 2 <= i <= 8 and j >= 1)
        lens = Circle(radius=0.5, stroke_color=YELLOW, stroke_width=6).move_to(dots[off].get_center())
        handle = Line(lens.get_bottom() + RIGHT * 0.35, lens.get_bottom() + RIGHT * 0.9 + DOWN * 0.5, color=YELLOW, stroke_width=8)
        mg = VGroup(lens, handle)
        t_off = T("on the fluid", 28, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(mg), FadeIn(t_off), run_time=0.8)
        self.wait(0.6)
        t_on = T("on a mitochondrion", 28, GOLD).move_to([0, -3.4, 0])
        self.play(FadeOut(t_off), run_time=0.4)
        self.play(mg.animate.move_to(mg.get_center() + (dots[on].get_center() - dots[off].get_center())), FadeIn(t_on), run_time=1.2)
        self.finish()


class S04Gold(SpokenScene):
    def construct(self):
        pic = heart_pic()
        dots = heart_dots()
        hits = heart_hits()
        sw = sweep(pic.frame)
        self.add(pic, dots, sw)
        self.at("that land on mitochondria")
        goldn = [d for d, (i, j) in zip(dots, LATT) if hits[(i, j)]]
        self.play(LaggedStart(*[goldify(d) for d in goldn], lag_ratio=0.2), run_time=3.2)
        t1 = bottom("one slice: a rough guess", TEXT, 32)
        self.at("one slice gives only a rough guess")
        self.play(FadeIn(t1), run_time=0.5)
        self.at("over many fairly chosen pictures")
        fans = VGroup(*[pic.frame.copy().set_fill(PICFILL, 1).rotate(a * DEGREES).shift(np.array([dx, dy, 0])) for a, dx, dy in ((-4, -0.3, 0.1), (5, 0.35, 0.15), (9, 0.6, -0.1))])
        for f in fans:
            f.set_z_index(-1)
        self.add(fans)
        self.bring_to_back(fans)
        self.play(FadeOut(t1), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(f) for f in fans], lag_ratio=0.3), run_time=1.6)
        f1 = T("gold dots ÷ all dots", 40, GOLD, weight=BOLD).move_to([0, 3.35, 0])
        f2 = T("≈ share of the cell's volume that is mitochondria", 28, TEXT).move_to([0, 2.7, 0])
        fit(f2, max_w=12.4)
        f3 = T("(over many fairly chosen pictures)", 24, TEXT).move_to([0, 2.2, 0])
        self.at("the share of gold dots")
        self.play(FadeIn(f1), run_time=0.6)
        self.at("estimates the share of the cell's volume")
        self.play(FadeIn(f2), run_time=0.6)
        self.play(FadeIn(f3), run_time=0.5)
        self.play(*[Indicate(d, color=YELLOW, scale_factor=1.5) for d in goldn[:8]], run_time=1.2)
        self.finish()


class S05Toy(SpokenScene):
    def construct(self):
        pic = heart_pic()
        dots = heart_dots()
        hits = heart_hits()
        for d, (i, j) in zip(dots, LATT):
            if hits[(i, j)]:
                d.set_fill(GOLD, 1).set_stroke(GOLD)
        self.add(pic, dots)
        fr, ms, tdots, gold_idx = make_toy()
        sw = sweep(fr)
        lab = top("toy grid, schematic", TEXT, 30, y=3.25).move_to([-2.9, 3.25, 0])
        self.at("try it on a small grid")
        for d in tdots:
            d.shift(UP * 1.5).set_opacity(0)
        self.play(FadeOut(pic), FadeOut(dots), FadeIn(fr), FadeIn(ms), FadeIn(lab), run_time=1.0)
        self.play(LaggedStart(*[d.animate.shift(DOWN * 1.5).set_opacity(1) for d in tdots], lag_ratio=0.05), run_time=1.2)
        self.add(sw)
        cg, ca, cr = ValueTracker(0), ValueTracker(0), None
        n_g = always_redraw(lambda: T(str(int(round(cg.get_value()))), 46, GOLD, weight=BOLD).move_to([5.9, 1.9, 0]))
        n_a = always_redraw(lambda: T(str(int(round(ca.get_value()))), 46, TEXT, weight=BOLD).move_to([5.9, 0.9, 0]))
        lg, la = counter("gold dots", GOLD, 1.9), counter("all dots", TEXT, 0.9)
        self.at("count the gold dots")
        self.add(n_g)
        self.play(FadeIn(lg), run_time=0.2)
        self.play(LaggedStart(*[AnimationGroup(goldify(tdots[k]), cg.animate.set_value(n + 1)) for n, k in enumerate(gold_idx)], lag_ratio=0.2), run_time=1.5)
        self.at("then count all the dots")
        self.add(n_a)
        self.play(FadeIn(la), run_time=0.3)
        self.play(ca.animate.set_value(20).set_rate_func(linear),
                  LaggedStart(*[Indicate(d, color=WHITE, scale_factor=1.6) for d in tdots], lag_ratio=0.05), run_time=2.0)
        self.at("the share appears on the screen")
        r1 = T("6 of 20 dots", 36, TEXT).move_to([4.1, -0.3, 0])
        r2 = T("= 30%", 48, YELLOW, weight=BOLD).move_to([4.1, -1.0, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(r2, scale=1.3), run_time=0.7)
        self.at("this toy grid")
        bar = scale_bar()
        bd = band(22, 37)
        bl = T("heart muscle, 10 kinds of mammals: 22% to 37%", 26, GOLD).move_to([0, -1.95, 0])
        self.play(FadeIn(bar), FadeIn(bd), FadeIn(bl), run_time=0.9)
        mk = Triangle(stroke_width=0, fill_color=YELLOW, fill_opacity=1).scale(0.14).rotate(PI).move_to([bar_x(30), BAR_Y + 0.7, 0])
        self.at("lands inside the real range")
        self.play(FadeIn(mk), run_time=0.3)
        self.play(mk.animate.move_to([bar_x(30), BAR_Y + 0.28, 0]), run_time=0.9, rate_func=rush_into)
        self.play(Indicate(bd, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


class S06Heart(SpokenScene):
    def construct(self):
        bar = scale_bar()
        bd = band(22, 37)
        self.add(bar, bd)
        cards = VGroup(*[card(k, k=1.12) for k in range(5)])
        for c in cards:
            c.move_to([0, 1.45, 0])
        mo = make_motes(6, 9, (-5.5, 5.5), (-1.2, 0.2), 0.3, col=GREY)
        self.at("many pictures")
        t1 = top("many pictures, many more dots", TEXT, 32)
        self.play(FadeIn(t1), FadeIn(cards), run_time=0.6)
        xs = [-5.0, -2.5, 0, 2.5, 5.0]
        rots = [4, -3, 2, -4, 3]
        self.play(LaggedStart(*[c.animate.move_to([x, 1.45, 0]).rotate(r * DEGREES) for c, x, r in zip(cards, xs, rots)], lag_ratio=0.15), run_time=2.0)
        self.add(mo)
        t2 = top("heart muscle cells", TEXT, 32)
        self.at("look at heart muscle cells")
        self.play(FadeOut(t1), FadeIn(t2), run_time=0.5)
        herd = VGroup(*[mammal(1.0 + 0.04 * (k % 4)) for k in range(10)])
        for k, m in enumerate(herd):
            m.move_to([-5.4 + 1.2 * k, -0.35, 0])
        ml = T("ten kinds of mammals (schematic)", 28, TEXT).move_to([0, -1.2, 0])
        self.at("from ten kinds of mammals")
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in herd], lag_ratio=0.15), FadeIn(ml), run_time=2.2)
        self.at("mitochondria filled about a fifth")
        fillb = band(22, 37, 0.85)
        fillb.save_state()
        fillb.stretch_to_fit_width(0.02, about_edge=LEFT)
        pct = T("22% to 37%", 40, GOLD, weight=BOLD).move_to([(bar_x(22) + bar_x(37)) / 2, -2.2, 0])
        self.add(fillb)
        self.play(FadeOut(mo), Restore(fillb), FadeIn(pct), run_time=2.0)
        self.at("depending on the kind of mammal")
        self.play(LaggedStart(*[Indicate(m, color=GOLD, scale_factor=1.15) for m in herd], lag_ratio=0.1), run_time=2.0)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        hp = heart_pic()
        dots = heart_dots()
        hits = heart_hits()
        for d, (i, j) in zip(dots, LATT):
            if hits[(i, j)]:
                d.set_fill(GOLD, 1).set_stroke(GOLD)
        self.add(hp, dots)
        fp = fat_pic()
        self.at("drop the same grid")
        self.play(dots.animate.shift(UP * 0.5), run_time=0.4)
        self.play(FadeOut(hp), FadeIn(fp), *[d.animate.set_fill(DOTC, 0).set_stroke(DOTC) for d in dots], run_time=1.0)
        self.play(dots.animate.shift(DOWN * 0.5), run_time=0.5)
        sw = sweep(fp.frame)
        self.add(sw)
        t1 = top("a white fat cell", CREAM, 36, weight=BOLD)
        self.at("white fat cell")
        self.play(FadeIn(t1), run_time=0.5)
        self.at("before the dots turn gold")
        self.play(LaggedStart(*[Indicate(d, color=WHITE, scale_factor=1.4) for d in dots], lag_ratio=0.02), run_time=1.4)
        box = RoundedRectangle(corner_radius=0.2, width=11.0, height=1.5, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=0.96)
        l1 = T("PAUSE AND PREDICT", 28, YELLOW, weight=BOLD)
        l2 = T("bigger or smaller than the heart cell's share?", 34)
        pc = VGroup(box, VGroup(l1, l2).arrange(DOWN, buff=0.12).move_to(box)).move_to([0, 3.0, 0])
        self.at("predict")
        self.play(FadeOut(t1), FadeIn(pc, shift=DOWN * 0.2), run_time=0.7)
        b1 = chip("bigger", TEXT, 30).move_to([-1.6, -3.4, 0])
        b2 = chip("smaller", TEXT, 30).move_to([1.6, -3.4, 0])
        self.at("bigger or smaller")
        self.play(FadeIn(b1), run_time=0.4)
        self.play(FadeIn(b2), run_time=0.4)
        self.finish()


def pred_world(scene):
    fp = fat_pic()
    dots = heart_dots()
    for d in dots:
        d.set_fill(DOTC, 0)
    scene.add(fp, dots)
    box = RoundedRectangle(corner_radius=0.2, width=11.0, height=1.5, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=0.96)
    l1 = T("PAUSE AND PREDICT", 28, YELLOW, weight=BOLD)
    l2 = T("bigger or smaller than the heart cell's share?", 34)
    pc = VGroup(box, VGroup(l1, l2).arrange(DOWN, buff=0.12).move_to(box)).move_to([0, 3.0, 0])
    b1 = chip("bigger", TEXT, 30).move_to([-1.6, -3.4, 0])
    b2 = chip("smaller", TEXT, 30).move_to([1.6, -3.4, 0])
    scene.add(pc, b1, b2)
    return fp, dots, pc


class S08Pause(NarratedScene):
    def construct(self):
        fp, dots, pc = pred_world(self)
        self.add(sweep(fp.frame))
        tr = ValueTracker(1.0)
        ring0 = Circle(radius=0.45, stroke_color=GREY, stroke_width=4).move_to([6.1, -3.2, 0])
        ring = always_redraw(lambda: Arc(radius=0.45, start_angle=PI / 2, angle=TAU * max(tr.get_value(), 0.001), stroke_color=YELLOW, stroke_width=8).move_to([6.1, -3.2, 0]))
        self.add(ring0, ring)
        self.play(tr.animate.set_value(0.0), run_time=4.6, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        fp = fat_pic()
        dots = heart_dots()
        for d in dots:
            d.set_fill(DOTC, 0)
        sw = sweep(fp.frame)
        self.add(fp, dots, sw)
        t0 = top("much smaller", YELLOW, 40, weight=BOLD)
        self.at("much smaller")
        self.play(FadeIn(t0, scale=1.2), run_time=0.6)
        cls = {k: fat_class(*k) for k in LATT}
        cdots = [d for d, k in zip(dots, LATT) if cls[k] == "cream"]
        gdots = [d for d, k in zip(dots, LATT) if cls[k] == "gold"]
        self.at("almost every dot lands on fat")
        self.play(LaggedStart(*[goldify(d, CREAM) for d in cdots], lag_ratio=0.06), run_time=2.6)
        self.play(LaggedStart(*[goldify(d, GOLD) for d in gdots], lag_ratio=0.3), run_time=0.8)
        self.remove(sw)
        sw = sweep(fp.frame)
        self.add(sw)
        t682 = T("grid of 682 points", 40, TEAL, weight=BOLD).move_to([0, 3.2, 0])
        self.at("a grid of 682 points")
        self.play(FadeOut(t0), FadeIn(t682, scale=1.2), run_time=0.7)
        self.play(Indicate(dots, color=WHITE, scale_factor=1.06), run_time=1.0)
        lb = bottom("white fat cells, chicken embryos", TEXT, 30)
        self.at("white fat cells from chicken embryos")
        fans = VGroup(*[fp.frame.copy().set_fill(PICFILL, 1).rotate(a * DEGREES).shift(np.array([dx, dy, 0])) for a, dx, dy in ((-4, -0.3, 0.1), (5, 0.35, 0.15))])
        for f in fans:
            f.set_z_index(-1)
        self.add(fans)
        self.bring_to_back(fans)
        self.play(FadeIn(lb), LaggedStart(*[FadeIn(f) for f in fans], lag_ratio=0.4), run_time=2.0)
        self.wait(0.5)
        # shrink the picture left, show the scale bar and numbers
        grp = VGroup(fp, dots)
        bar = scale_bar()
        hb = band(22, 37, 0.85)
        hl = T("heart muscle", 28, GOLD).move_to([(bar_x(22) + bar_x(37)) / 2, -2.2, 0])
        f1 = T("fat droplets together", 28, CREAM).move_to([3.6, 2.3, 0])
        f2 = T("about 90.9%", 48, CREAM, weight=BOLD).move_to([3.6, 1.6, 0])
        self.at("fat droplets filled about nine tenths")
        self.play(FadeOut(t682), FadeOut(lb), FadeOut(fans), FadeOut(sw), grp.animate.scale(0.68).move_to([-3.3, 0.65, 0]),
                  FadeIn(bar), FadeIn(hb), FadeIn(hl), run_time=1.5)
        self.play(FadeIn(f1), FadeIn(f2, scale=1.2), run_time=0.8)
        g1 = T("mitochondria", 28, GOLD).move_to([3.6, 0.45, 0])
        g2 = T("about 0.7%", 48, GOLD, weight=BOLD).move_to([3.6, -0.25, 0])
        sl = Rectangle(width=0.09, height=0.26, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([bar_x(0.7) + 0.05, BAR_Y, 0])
        fl = T("fat cell", 28, GOLD).move_to([-5.0, -2.2, 0])
        self.at("mitochondria filled less than one percent")
        self.play(FadeIn(g1), FadeIn(g2, scale=1.2), FadeIn(sl, scale=3), FadeIn(fl), run_time=1.0)
        self.play(*[Indicate(d, color=YELLOW, scale_factor=2.0) for d in gdots], Indicate(sl, color=YELLOW, scale_factor=2.0), run_time=1.2)
        self.finish()


class S10Rim(SpokenScene):
    def construct(self):
        fp = fat_pic()
        dots = heart_dots()
        cls = {k: fat_class(*k) for k in LATT}
        for d, k in zip(dots, LATT):
            c = {"cream": CREAM, "gold": GOLD, "hollow": None}[cls[k]]
            if c:
                d.set_fill(c, 1).set_stroke(c)
            else:
                d.set_fill(DOTC, 0)
        self.add(fp, dots)
        pl = plan(FAT, (CX, CY), CW, CH, seed=7)
        self.at("the fat takes most of the floor")
        self.play(FadeOut(fp), FadeOut(dots), FadeIn(pl), run_time=2.0)
        lab = T("fat", 36, BG, weight=BOLD).move_to(pl.rooms[5])
        self.play(FadeIn(lab), run_time=0.5)
        rim = Rectangle(width=CW + 0.15, height=CH + 0.15, stroke_color=YELLOW, stroke_width=8).move_to([CX, CY, 0])
        self.at("everything else")
        self.play(LaggedStart(*[Indicate(pl.rooms[k], color=WHITE, scale_factor=1.3) for k in (0, 1, 2, 3, 4)], lag_ratio=0.25), run_time=2.2)
        self.at("sits in a thin rim around it")
        self.play(ShowPassingFlash(rim, time_width=0.7), run_time=1.8)
        # zoom inset on the strip
        box = Rectangle(width=4.2, height=3.6, stroke_color=YELLOW, stroke_width=5, fill_color=BG, fill_opacity=0.97).move_to([2.6, -0.5, 0])
        cap = T("the rim, zoomed", 26, YELLOW).move_to([2.6, 1.0, 0])
        ib = [bean((1.4, -0.2), 20, 1.0, 0.46), bean((2.6, -0.8), -10, 1.0, 0.46), bean((3.7, -0.15), 5, 1.0, 0.46), bean((2.0, -1.5), 0, 1.0, 0.46)]
        inset = VGroup(box, cap, *ib)
        hi = Rectangle(width=0.9, height=CH * 0.2, stroke_color=YELLOW, stroke_width=5).move_to(pl.rooms[3])
        q = T("?", 110, YELLOW, weight=BOLD).move_to([2.6, 0.2, 0])
        self.at("is that rim short of mitochondria")
        self.play(Create(hi), FadeIn(inset), run_time=1.2)
        self.play(FadeIn(q, scale=0.4), run_time=0.6)
        pulse(q, 1.0, 0.1)
        self.at("the lesson lets you work it out")
        self.play(*[Indicate(b, color=YELLOW, scale_factor=1.25) for b in ib], run_time=1.6)
        self.finish()


def two_plans(scene, seed=7):
    hp = plan(HEART2, (-3.3, 0.35), 5.6, 3.3, seed=2)
    fp = plan(FAT, (3.3, 0.35), 5.6, 3.3, seed=3)
    return hp, fp


class S11Pattern(SpokenScene):
    def construct(self):
        fp0 = plan(FAT, (CX, CY), CW, CH, seed=7)
        self.add(fp0)
        hp, fp = two_plans(self)
        self.at("so")
        self.play(ReplacementTransform(fp0, fp), run_time=0.6)
        self.at("in the heart cell")
        t1 = T("heart cell", 32, TEXT).move_to([-3.3, 2.5, 0])
        self.play(FadeIn(hp), FadeIn(t1), run_time=0.7)
        j1 = T("job: work without a break", 28, TEXT).move_to([-3.3, -1.75, 0])
        self.at("mitochondria fill a large share")
        self.play(LaggedStart(*[Indicate(hp.rooms[k], color=WHITE, scale_factor=1.06) for k in (2, 3, 4)], lag_ratio=0.2), FadeIn(j1), run_time=1.8)
        t2 = T("fat cell", 32, TEXT).move_to([3.3, 2.5, 0])
        self.at("in the fat cell")
        self.play(FadeIn(t2), Indicate(fp.rooms[5], color=WHITE, scale_factor=1.05), run_time=1.0)
        j2 = T("job: store fat", 28, TEXT).move_to([3.3, -1.75, 0])
        self.at("stored fat fills most of the space")
        self.play(FadeIn(j2), Indicate(fp.rooms[5], color=WHITE, scale_factor=1.08), run_time=1.5)
        nt = bottom("drawn the same size, not to real scale", TEXT, 28)
        self.at("many of the same parts")
        self.play(FadeIn(nt), run_time=0.5)
        self.play(*[Indicate(hp.rooms[k], color=WHITE, scale_factor=1.1) for k in (0, 1)], *[Indicate(fp.rooms[k], color=WHITE, scale_factor=1.2) for k in (0, 1)], run_time=1.4)
        self.at("different floor plans")
        self.play(Indicate(hp.base, color=YELLOW, scale_factor=1.04), Indicate(fp.base, color=YELLOW, scale_factor=1.04), run_time=1.2)
        self.finish()


class S12Limits(SpokenScene):
    def construct(self):
        hp, fp = two_plans(self)
        t1 = T("heart cell", 32, TEXT).move_to([-3.3, 2.5, 0])
        t2 = T("fat cell", 32, TEXT).move_to([3.3, 2.5, 0])
        j1 = T("job: work without a break", 28, TEXT).move_to([-3.3, -1.75, 0])
        j2 = T("job: store fat", 28, TEXT).move_to([3.3, -1.75, 0])
        self.add(hp, fp, t1, t2, j1, j2)
        warn = VGroup(Triangle(stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.2).scale(0.34),
                      T("!", 32, YELLOW, weight=BOLD).move_to([0, -0.04, 0])).move_to([0, 3.15, 0])
        self.at("one caution")
        self.play(FadeIn(warn, scale=1.4), run_time=0.6)
        pulse(warn, 1.0, 0.1)
        c1 = chip("heart: ten kinds of mammals", TEXT, 28)
        c2 = chip("fat: chicken embryos", TEXT, 28)
        c1.move_to([-3.3, -2.65, 0])
        c2.move_to([3.3, -2.65, 0])
        self.at("these cells came from different animals")
        self.play(FadeOut(j1), FadeOut(j2), FadeIn(c1, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.8)
        self.at("different studies")
        self.play(Indicate(c1, color=YELLOW), Indicate(c2, color=YELLOW), run_time=1.4)
        p1 = T("pattern", 44, GREEN, weight=BOLD)
        p2 = T(", not proof", 44, "#FF8A80", weight=BOLD)
        sign = VGroup(p1, p2).arrange(RIGHT, buff=0.05).move_to([1.0, 3.3, 0])
        self.at("they show a pattern")
        self.play(FadeOut(warn), p1.animate.move_to([-0.5, 3.3, 0]).set_opacity(1) if False else FadeIn(p1, shift=DOWN * 0.15), run_time=0.8)
        sign.move_to([0, 3.3, 0])
        self.play(Indicate(p1, color=GREEN), run_time=1.2)
        self.at("they do not prove what causes it")
        self.play(FadeIn(p2, shift=LEFT * 0.2), run_time=0.8)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        stack = VGroup(*[card(10 + k, k=2.3) for k in range(5)]).move_to([-3.2, 0.9, 0])
        for k, c in enumerate(stack):
            c.shift(RIGHT * 0.12 * k + UP * 0.08 * k)
        hbar = Rectangle(width=4.6, height=0.4, stroke_color=TEXT, stroke_width=2).move_to([-3.3, -2.6, 0])
        fbar = Rectangle(width=4.6, height=0.4, stroke_color=TEXT, stroke_width=2).move_to([3.3, -2.6, 0])
        self.at("still")
        self.play(FadeIn(stack), FadeIn(hbar), FadeIn(fbar), run_time=1.0)
        pic_fan = []
        self.at("repeated over many pictures")
        flyers = VGroup()
        for k in range(5):
            top_c = stack[-1 - k]
            fly = VGroup(*[Dot(radius=0.12, color=GOLD) for _ in range(4)]).arrange(RIGHT, buff=0.15).move_to(top_c.get_center())
            flyers.add(fly)
        anims = []
        for k, (c, fly) in enumerate(zip(reversed(list(stack)), flyers)):
            anims.append(Succession(c.animate.shift(RIGHT * 4.0 + UP * 0.3).rotate(-0.2).set_opacity(0), run_time=0.5))
        for k in range(5):
            c = stack[-1 - k]
            self.add(flyers[k])
            tgt = hbar.get_left() + RIGHT * (0.3 + 0.55 * k) if k % 2 == 0 else fbar.get_left() + RIGHT * (0.3 + 0.55 * k)
            self.play(c.animate.shift(RIGHT * 3.0).set_opacity(0), flyers[k].animate.move_to(tgt).scale(0.5), run_time=0.35)
        self.play(FadeOut(flyers), run_time=0.3)
        self.at("turned images into numbers")
        tals = []
        for spec, c in ((HEART2, (-3.3, -2.6)), (FAT, (3.3, -2.6))):
            vals_g = sum((spec[m][2] - spec[m][0]) * (spec[m][3] - spec[m][1]) for m in ("m1", "m2", "m3"))
            vals_c = (spec["vac"][2] - spec["vac"][0]) * (spec["vac"][3] - spec["vac"][1])
            x0 = c[0] - 2.3
            tals.append(VGroup(Rectangle(width=4.6 * vals_g, height=0.4, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([x0 + 4.6 * vals_g / 2, c[1], 0]),
                               Rectangle(width=4.6 * vals_c, height=0.4, stroke_width=0, fill_color=CREAM, fill_opacity=0.9).move_to([x0 + 4.6 * vals_g + 4.6 * vals_c / 2, c[1], 0])))
        self.play(*[GrowFromEdge(t[0], LEFT) for t in tals], run_time=0.8)
        self.play(*[GrowFromEdge(t[1], LEFT) for t in tals], run_time=0.6)
        hp, fp = two_plans(self)
        t1 = T("heart cell", 32, TEXT).move_to([-3.3, 2.5, 0])
        t2 = T("fat cell", 32, TEXT).move_to([3.3, 2.5, 0])
        hp.shift(UP * 0.0)
        self.at("those numbers show a pattern")
        self.play(FadeIn(hp), FadeIn(fp), FadeIn(t1), FadeIn(t2), run_time=1.6)
        self.at("cells with different jobs")
        self.play(Indicate(hp.base, color=YELLOW, scale_factor=1.03), Indicate(fp.base, color=YELLOW, scale_factor=1.03), run_time=1.5)
        self.finish()


class S14End(EndCard):
    LINE = "Counting dots over many slices estimates how much space each part fills."
