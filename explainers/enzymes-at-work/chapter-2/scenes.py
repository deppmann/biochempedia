"""Enzymes at work: Why Heat Gives a Peak (film 2 of 2, Biochemistrypedia explainer).

Same world as film 1: dark ground, BLUE enzyme blocks with a notch, ORANGE substrate, GREEN products,
GREY denatured block, BLUE counter top left, YELLOW gauge top right, PURPLE rate bar bottom right.
Added here: RED temperature dial, gelatin chains (ORANGE bead strings), WATER droplets.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
TAN = "#C9A66B"
PINE = "#E6C35C"
WATER = "#BFE3F5"

ENZ_PTS = [(-1.8, -1.0), (1.8, -1.0), (1.8, 1.0), (0.65, 1.0), (0.45, 0.2), (-0.45, 0.2), (-0.65, 1.0), (-1.8, 1.0)]
ENZ_BAD = [(-1.9, -1.1), (1.7, -0.8), (2.0, 0.7), (0.95, 0.9), (0.85, 0.55), (0.35, 0.5), (0.0, 0.95), (-1.6, 1.1)]
FIT = 0.58


def enzyme(s=1.0, color=BLUE, pts=ENZ_PTS, fill=0.35, sw=4):
    p = Polygon(*[np.array([x, y, 0.0]) for x, y in pts], stroke_color=color, stroke_width=sw,
                fill_color=color, fill_opacity=fill).round_corners(0.12)
    return p.scale(s)


def bad_enzyme(s=1.0):
    return enzyme(s, GREY, ENZ_BAD, 0.4)


def wedge(s=1.0, color=ORANGE, narrow=1.0):
    w = 0.6 * narrow
    pts = [(-w, 0.37), (w, 0.37), (0.4 * narrow, -0.37), (-0.4 * narrow, -0.37)]
    p = Polygon(*[np.array([x, y, 0.0]) for x, y in pts], stroke_color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.8).round_corners(0.06)
    return p.scale(s)


def lab(text, size=30, color=TEXT, pos=ORIGIN, **kw):
    return T(text, size=size, color=color, **kw).move_to(pos)


def jig(m, amp=0.05, tr=None, sp=1.3, ph=0.0):
    """Drifting whose speed and size follow a tracker (hotter = faster jiggle)."""
    m._tt = 0.0
    m._off = np.zeros(3)

    def u(mm, dt):
        k = tr.get_value() if tr is not None else 1.0
        mm._tt += dt * sp * k
        a = amp * k ** 0.5
        off = np.array([a * np.sin(mm._tt + ph), a * np.cos(1.3 * mm._tt + ph), 0.0])
        mm.shift(off - mm._off)
        mm._off = off
    m.add_updater(u)
    return m


def swim(m, ax=0.25, ay=0.18, sp=1.0, ph=0.0):
    m._tt = 0.0
    m._off = np.zeros(3)

    def u(mm, dt):
        mm._tt += dt
        t = mm._tt * sp + ph
        off = np.array([ax * np.sin(t), ay * np.cos(1.3 * t), 0.0])
        mm.shift(off - mm._off)
        mm._off = off
    m.add_updater(u)
    return m


class Film(SpokenScene):
    pass


# ---------------------------------------------------------------------------------------------
# the row of tubes (film 1's tube world, now five tubes from cold to hot)
# ---------------------------------------------------------------------------------------------
TX = [-5.4, -3.6, -1.8, 0.0, 1.8]
TW, TH, TCY = 1.7, 3.5, -0.95
TEMPS = [20, 32, 42, 47, 58]
SPD = [float(np.exp(0.04 * (t - 20))) for t in TEMPS]
GV = [0.2 * s for s in SPD]            # gauge value 0..1
NWORK = [8, 8, 6, 3, 0]
ORDER = [7, 2, 5, 0, 3, 6, 1, 4]
GAUGE_C = np.array([5.0, 2.3, 0.0])
GAUGE_R = 1.1
BAR_X, BAR_BASE, BAR_H, BAR_W = 6.0, -3.0, 3.0, 1.0
BS = 0.21


def dial_angle(t):
    return np.radians(150 - 120 * (t - 20) / 38.0)


def make_dial(c, r=0.34, ang=None, sw=4):
    ring = Circle(radius=r, stroke_color=RED, stroke_width=sw, fill_color=RED, fill_opacity=0.12).move_to(c)
    a = ang if ang is not None else np.radians(150)
    ptr = Line(c, c + r * 0.85 * np.array([np.cos(a), np.sin(a), 0]), color=RED, stroke_width=sw + 1)
    return ring, ptr


def counter_text(n):
    return T(f"working sites: {n} of 8", 32, BLUE).move_to([-6.5, 3.4, 0], aligned_edge=LEFT)


class Row:
    def __init__(self, sc, sel=0, nw=(8, 8, 8, 8, 8), jt=None, nt=None, st=None):
        self.sc = sc
        self.nw = list(nw)
        self.jt = jt or [ValueTracker(1.0) for _ in range(5)]
        self.tubes, self.blocks, self.wedges, self.bad = [], [], [], []
        for i, x in enumerate(TX):
            tube = RoundedRectangle(corner_radius=0.35, width=TW, height=TH, stroke_color=GREY, stroke_width=5,
                                    fill_color=GREY, fill_opacity=0.1).move_to([x, TCY, 0])
            self.tubes.append(tube)
            nb = 8 - self.nw[i]
            bl = []
            for j in range(8):
                p = [x + (-0.4 if j % 2 == 0 else 0.4), 0.35 - 0.6 * (j // 2), 0]
                if j in ORDER[:nb]:
                    b = bad_enzyme(BS).move_to(p)
                else:
                    b = enzyme(BS).move_to(p)
                jig(b, 0.03, self.jt[i], 1.4, 0.7 * j + i)
                bl.append(b)
            self.blocks.append(bl)
            self.bad.append(nb)
            wl = []
            for j in range(4):
                w = wedge(0.22).move_to([x - 0.55 + 0.37 * j, -2.15, 0])
                jig(w, 0.1, self.jt[i], 1.0, 1.7 * j + i)
                wl.append(w)
            self.wedges.append(wl)
        self.dials = []
        for i, x in enumerate(TX):
            ring, ptr = make_dial(np.array([x, 1.35, 0]), 0.34, dial_angle(TEMPS[i]))
            self.dials.append(VGroup(ring, ptr))
        self.chx = VGroup(Arrow([TX[0] + 0.7, -3.25, 0], [TX[4] - 0.7, -3.25, 0], buff=0, color=RED, stroke_width=5),
                          lab("cold", 28, RED, [TX[0] - 0.2, -3.25, 0]), lab("hot", 28, RED, [TX[4] + 0.2, -3.25, 0]))
        self.sx = ValueTracker(TX[sel])
        self.nt = nt or ValueTracker(float(self.nw[sel]))
        self.st = st or ValueTracker(GV[sel])
        self.hil = always_redraw(lambda: RoundedRectangle(corner_radius=0.3, width=TW + 0.22, height=4.75, stroke_color=TEXT,
                                                           stroke_width=5, fill_opacity=0).move_to([self.sx.get_value(), -0.55, 0]))
        self.counter = always_redraw(lambda: counter_text(int(round(self.nt.get_value()))))
        arc = Arc(radius=GAUGE_R, start_angle=0, angle=PI, stroke_color=YELLOW, stroke_width=7, arc_center=GAUGE_C)
        needle = Line(GAUGE_C, GAUGE_C + UP * GAUGE_R * 0.85, color=YELLOW, stroke_width=7)

        def un(m):
            th = PI * (1 - self.st.get_value())
            m.put_start_and_end_on(GAUGE_C, GAUGE_C + GAUGE_R * 0.85 * np.array([np.cos(th), np.sin(th), 0]))
        needle.add_updater(un)
        self.gauge = VGroup(arc, needle, Dot(GAUGE_C, radius=0.1, color=YELLOW))
        self.glabel = lab("speed per site", 28, YELLOW, GAUGE_C + DOWN * 0.55)
        self.bar = Rectangle(width=BAR_W, height=BAR_H, stroke_color=PURPLE, stroke_width=4, fill_opacity=0).move_to(
            [BAR_X, BAR_BASE + BAR_H / 2, 0])

        def fill():
            h = max(BAR_H * min(1.0, (self.nt.get_value() / 8.0) * self.st.get_value() / 0.4), 0.001)
            return Rectangle(width=BAR_W - 0.08, height=h, stroke_width=0, fill_color=PURPLE, fill_opacity=0.9).move_to(
                [BAR_X, BAR_BASE + h / 2, 0])
        self.barfill = always_redraw(fill)
        self.blab = lab("rate", 28, PURPLE, [BAR_X, -3.45, 0])

    def tube_mobs(self, idx=range(5)):
        out = []
        for i in idx:
            out += [self.tubes[i], *self.blocks[i], *self.wedges[i]]
        return out

    def add_tubes(self, idx=range(5)):
        self.sc.add(*self.tube_mobs(idx))

    def add_dials(self):
        self.sc.add(*self.dials, self.chx)

    def add_readouts(self, counter=True, gauge=True, bar=True, hil=True):
        if hil:
            self.sc.add(self.hil)
        if counter:
            self.sc.add(self.counter)
        if gauge:
            self.sc.add(self.gauge, self.glabel)
        if bar:
            self.sc.add(self.bar, self.barfill, self.blab)

    def goto(self, k, rt=1.5, nt=True, st=True):
        a = [self.sx.animate.set_value(TX[k])]
        if nt:
            a.append(self.nt.animate.set_value(float(NWORK[k])))
        if st:
            a.append(self.st.animate.set_value(GV[k]))
        return AnimationGroup(*a, run_time=rt, rate_func=smooth)

    def denature(self, i, n_bad):
        """Animations turning blocks of tube i grey until n_bad are bent."""
        anims = []
        for j in ORDER[self.bad[i]:n_bad]:
            b = self.blocks[i][j]
            anims.append(Transform(b, bad_enzyme(BS).move_to(b.get_center())))
        self.bad[i] = max(self.bad[i], n_bad)
        return anims


# ---------------------------------------------------------------------------------------------
# gelatin chains
# ---------------------------------------------------------------------------------------------
def pm(m, ph, A, cutT, q, sp=1.0):
    m._tt = 0.0
    m._off = np.zeros(3)

    def u(mm, dt):
        mm._tt += dt * sp
        c = cutT.get_value() if cutT is not None else 0.0
        p = ph + c * q * 1.9
        a = A * (1 + c * 1.5)
        off = np.array([a * np.sin(mm._tt + p), 0.7 * a * np.cos(1.3 * mm._tt + p), 0.0])
        mm.shift(off - mm._off)
        mm._off = off
    m.add_updater(u)


class Chains:
    def __init__(self, x0, x1, ys, nb=12, seed=0, npieces=3, cutT=None, amp=0.07, rad=0.12):
        rng = np.random.RandomState(seed)
        self.beads, self.pieces, self.tails = [], [], []
        per = nb // npieces
        for k, y0 in enumerate(ys):
            ph = rng.uniform(0, 6)
            xs = [x0 + (x1 - x0) * i / (nb - 1) for i in range(nb)]
            pts = [np.array([x, y0 + 0.16 * np.sin(1.1 * x + ph), 0.0]) for x in xs]
            bs = [Dot(radius=rad, color=ORANGE).move_to(p) for p in pts]
            self.beads.append(bs)
            row = []
            for q in range(npieces):
                a, b = q * per, (q + 1) * per
                poly = VMobject(stroke_color=ORANGE, stroke_width=4).set_points_as_corners(pts[a:b])
                parts = [poly] + bs[a:b]
                if q < npieces - 1:
                    tail = Line(pts[b - 1], pts[b], color=ORANGE, stroke_width=4)
                    parts.append(tail)
                    self.tails.append(tail)
                g = VGroup(*parts)
                pm(g, ph, amp, cutT, q)
                row.append(g)
            self.pieces.append(row)
        self.all = VGroup(*[g for r in self.pieces for g in r])

    def links(self, lt, idxs, rows=None):
        out = []
        for k in (rows if rows is not None else range(len(self.beads) - 1)):
            for i in idxs:
                a, b = self.beads[k][i], self.beads[k + 1][i]
                out.append(always_redraw(lambda a=a, b=b: Line(a.get_center(), b.get_center(), color=ORANGE, stroke_width=4)
                                         .set_stroke(opacity=lt.get_value())))
        return out


def droplets(pts, seed=0):
    out = []
    for i, (x, y) in enumerate(pts):
        d = Circle(radius=0.14, stroke_color=WATER, stroke_width=3, fill_color=WATER, fill_opacity=0.75).move_to([x, y, 0])
        swim(d, 0.06, 0.08, 1.3, i * 1.1 + seed)
        out.append(d)
    return out


def bowl(c, R, firm, fill=ORANGE):
    b = Sector(radius=R, start_angle=PI, angle=PI, stroke_color=GREY, stroke_width=5, fill_color=fill, fill_opacity=0.22)
    b.move_to(c, aligned_edge=UP)
    b.move_to([c[0], c[1] - R / 2 + 0.0, 0], aligned_edge=ORIGIN) if False else None
    return b


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Enzymes at Work"
    TITLE = "Why Heat Gives a Peak"


def jelly_bowl(cx, cy, R, runny, tr):
    """A cartoon bowl: half disc of jelly, wavy (runny) or flat (firm) top, pineapple pieces."""
    half = Sector(radius=R, start_angle=PI, angle=PI, stroke_color=GREY, stroke_width=6, fill_color=ORANGE, fill_opacity=0.25)
    half.move_to([cx, cy - 0.425 * R, 0])
    if runny:
        top = always_redraw(lambda: ParametricFunction(
            lambda t: np.array([cx + t, cy + 0.09 * np.sin(3.2 * t + 3.0 * tr.get_value()), 0.0]), t_range=[-R, R],
            stroke_width=6, color=WATER))
    else:
        top = Line([cx - R, cy, 0], [cx + R, cy, 0], color=WATER, stroke_width=6)
    chunks = VGroup()
    for k, (dx, dy) in enumerate([(-0.7, -0.35), (0.1, -0.7), (0.75, -0.3)]):
        c = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.42, stroke_color=PINE, stroke_width=3,
                             fill_color=PINE, fill_opacity=0.85).move_to([cx + dx * R / 1.5, cy + dy * R / 1.5, 0])
        if runny:
            swim(c, 0.18, 0.1, 1.2, k * 2.0)
        else:
            swim(c, 0.02, 0.02, 1.0, k)
        chunks.add(c)
    return half, top, chunks


class S01Question(Film):
    def construct(self):
        tm = ValueTracker(0.0)
        tm.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(tm)
        R = 1.8
        b1 = jelly_bowl(-2.9, -0.3, R, True, tm)
        b2 = jelly_bowl(1.3, -0.3, R, False, tm)
        l1 = lab("fresh pineapple", 30, PINE, [-2.9, -2.6, 0])
        l2 = lab("canned pineapple", 30, PINE, [1.3, -2.6, 0])
        self.add(tm)
        self.at("why does fresh pineapple")
        self.play(FadeIn(b1[0]), Create(b1[1]), FadeIn(b1[2]), run_time=1.0)
        self.play(FadeIn(l1), run_time=0.5)
        self.at("canned pineapple")
        self.play(FadeIn(b2[0]), Create(b2[1]), FadeIn(b2[2]), run_time=1.0)
        self.play(FadeIn(l2), run_time=0.5)
        self.at("lets it set")
        q = lab("?", 90, TEXT, [-0.8, 0.6, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        swim(q, 0.0, 0.08, 1.5)
        self.at("the first film")
        eq = VGroup(T("rate", 30, PURPLE), T("=", 30, TEXT), T("working sites", 30, BLUE), T("×", 30, TEXT),
                    T("speed per site", 30, YELLOW)).arrange(RIGHT, buff=0.2).move_to([-1.6, 2.4, 0])
        self.at("how many active sites")
        row = Row(self, nt=ValueTracker(8.0), st=ValueTracker(0.5))
        self.play(FadeIn(row.counter, shift=RIGHT * 0.2), run_time=0.8)
        self.play(Indicate(row.counter, color=BLUE, scale_factor=1.06), run_time=0.8)
        self.at("how fast each one")
        self.play(FadeIn(row.gauge), FadeIn(row.glabel), run_time=0.8)
        self.play(row.st.animate.set_value(0.65), run_time=0.7)
        self.play(row.st.animate.set_value(0.5), run_time=0.7)
        self.at("heat turns both")
        self.add(row.barfill)
        self.play(FadeIn(row.bar), FadeIn(row.blab), FadeIn(eq, shift=UP * 0.1), run_time=1.0)
        self.play(Indicate(row.counter, color=BLUE, scale_factor=1.06), Indicate(row.glabel, color=YELLOW, scale_factor=1.1),
                  run_time=1.2)
        self.finish()


class S02Gelatin(Film):
    def construct(self):
        ys = [-1.7, -0.9, -0.1, 0.7, 1.5]
        lt = ValueTracker(0.0)
        chA = Chains(-5.6, 5.6, ys, 12, seed=2)
        lk = chA.links(lt, [2, 6, 10])
        dr = droplets([(-4.0 + 4.0 * c, ys[r] + 0.4) for r in range(4) for c in range(3)])
        t1 = lab("gelatin is a protein", 34, ORANGE, [0, 2.75, 0])
        self.at("gelatin is a protein")
        self.play(FadeIn(chA.all, lag_ratio=0.05), FadeIn(t1), run_time=1.6)
        self.at("long chains")
        self.play(Transform(t1, lab("long chains", 34, ORANGE, [0, 2.75, 0])), run_time=0.6)
        self.add(*lk)
        self.at("link up")
        self.play(lt.animate.set_value(1.0), Transform(t1, lab("chains link into a net", 34, ORANGE, [0, 2.75, 0])), run_time=1.5)
        self.at("traps water")
        self.play(*[FadeIn(d) for d in dr], Transform(t1, lab("the net traps water", 34, WATER, [0, 2.75, 0])), run_time=1.2)
        self.at("turns firm")
        self.play(Transform(t1, lab("firm", 40, TEXT, [0, 2.75, 0])), run_time=0.7)
        self.wait(0.5)
        self.at("fresh pineapple contains")
        cutT = ValueTracker(0.0)
        lt2 = ValueTracker(0.0)
        chB = Chains(-5.6, 5.6, ys, 12, seed=5, cutT=cutT)
        dr2 = droplets([(-4.0 + 4.0 * c, ys[r] + 0.4) for r in range(4) for c in range(3)], 3.0)
        self.play(FadeOut(chA.all), *[FadeOut(m) for m in lk], *[FadeOut(d) for d in dr], FadeOut(t1), run_time=0.6)
        self.add(chB.all, *dr2)
        t2 = lab("fresh pineapple", 34, PINE, [0, 2.75, 0])
        self.play(FadeIn(t2), run_time=0.5)
        self.at("bromelain")
        blk = [enzyme(0.55).move_to([x, 3.0, 0]) for x in (-3.4, 3.4)]
        for b in blk:
            swim(b, 0.04, 0.04, 1.5)
        nm = lab("bromelain", 34, BLUE, [0, 2.75, 0])
        self.play(Transform(t2, nm), *[FadeIn(b, shift=DOWN * 0.3) for b in blk], run_time=1.0)
        self.at("small family")
        self.play(*[Indicate(b, color=BLUE, scale_factor=1.15) for b in blk], run_time=1.2)
        self.at("bromelain cuts")
        for b in blk:
            b.clear_updaters()
        self.play(*[b.animate.move_to([b.get_center()[0], -1.8, 0]) for b in blk], cutT.animate.set_value(1.0),
                  *[t.animate.set_stroke(opacity=0) for t in chB.tails],
                  *[g.animate.set_color(GREEN) for r in chB.pieces for g in r], run_time=2.6, rate_func=linear)
        self.at("net cannot form")
        self.play(Transform(t2, lab("no net", 36, TEXT, [0, 2.75, 0])), *[d.animate.shift(DOWN * 0.5) for d in dr2],
                  FadeOut(VGroup(*blk)), run_time=1.5)
        self.finish()


class S03Dial(Film):
    def construct(self):
        row = Row(self)
        row.add_tubes([0])
        self.at("so the question")
        self.play(*[FadeIn(m) for m in row.tube_mobs([0])], run_time=1.0)
        self.at("bromelain")
        t = lab("bromelain", 34, BLUE, [-5.4, 1.3, 0])
        self.play(FadeIn(t), Indicate(row.blocks[0][0], color=BLUE, scale_factor=1.6), run_time=0.9)
        self.at("equal tubes")
        self.play(*[FadeIn(m) for m in row.tube_mobs([1, 2, 3, 4])], FadeOut(t), run_time=1.8, lag_ratio=0.1)
        self.add(*row.tube_mobs([1, 2, 3, 4]))
        self.at("different temperatures")
        self.play(*[FadeIn(d, shift=DOWN * 0.1) for d in row.dials], FadeIn(row.chx), run_time=1.6, lag_ratio=0.15)
        self.at("same time")
        clock = VGroup(Circle(radius=0.4, stroke_color=TEXT, stroke_width=5).move_to([-5.9, 2.5, 0]))
        hand = Line([-5.9, 2.5, 0], [-5.9, 2.8, 0], color=TEXT, stroke_width=5)
        hand._a = 0.0

        def uh(m, dt):
            m.rotate(-2.2 * dt, about_point=np.array([-5.9, 2.5, 0]))
        hand.add_updater(uh)
        ct = lab("same time in every tube", 30, TEXT, [-2.7, 2.5, 0])
        self.play(Create(clock), FadeIn(hand), FadeIn(ct), run_time=0.9)
        self.wait(0.9)
        self.at("compare both dials")
        self.play(FadeOut(ct), FadeOut(clock), FadeOut(hand), run_time=0.5)
        row.add_readouts()
        self.add(row.barfill)
        self.play(FadeIn(row.hil), FadeIn(row.counter), FadeIn(row.gauge), FadeIn(row.glabel), FadeIn(row.bar),
                  FadeIn(row.blab), run_time=1.2)
        self.at("tube to tube")
        self.play(Indicate(row.counter, color=BLUE, scale_factor=1.06), Indicate(row.glabel, color=YELLOW, scale_factor=1.1),
                  run_time=1.0)
        self.finish()


IC = np.array([-0.2, 2.55, 0.0])


def curve_y(x, hh=3.2):
    sig = 1.0 / (1.0 + np.exp(-(x - 0.6) / 0.9))
    return -0.3 + (-1.6 + 0.3) * sig + hh * np.exp(-((x + 0.1) / 1.5) ** 2)


def ipt(x):
    return np.array([IC[0] + 0.47 * x, IC[1] + 0.32 * (curve_y(x) - 0.6), 0.0])


class S04Speed(Film):
    def construct(self):
        jt = [ValueTracker(1.0) for _ in range(5)]
        row = Row(self, jt=jt)
        row.add_tubes()
        row.add_dials()
        row.add_readouts()
        self.add(row.barfill)
        hill = ParametricFunction(lambda t: ipt(t), t_range=[-3.1, 3.1], stroke_width=6, color=TEXT)
        frame = RoundedRectangle(corner_radius=0.1, width=3.4, height=1.7, stroke_color=GREY, stroke_width=3).move_to(IC + DOWN * 0.1)
        nv = ValueTracker(2.0)
        rate = ValueTracker(0.12)
        balls = VGroup()
        for i in range(9):
            b = Circle(radius=0.11, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.9)
            b.p = i / 9.0
            b.i = i

            def u(m, dt):
                vis = m.i < nv.get_value()
                if vis:
                    m.p = (m.p + dt * rate.get_value()) % 1.0
                x = -3.0 + 6.0 * m.p
                m.move_to(ipt(x) + UP * (0.13 + 0.03 * abs(np.sin(7 * m.p + m.i))))
                c = GREEN if x > 1.6 else ORANGE
                a = 0.0 if not vis else min(1.0, m.p * 8, (1 - m.p) * 8)
                m.set_stroke(c, opacity=a).set_fill(c, 0.9 * a)
            b.add_updater(u)
            balls.add(b)
        self.wait(0.3)
        self.at("warmer molecules")
        self.play(row.goto(1, 1.5, nt=False), jt[1].animate.set_value(SPD[1]), run_time=1.5)
        self.at("more of them")
        self.add(balls)
        self.play(Create(frame), Create(hill), run_time=1.2)
        self.at("activation energy hill")
        self.play(nv.animate.set_value(5.0), rate.animate.set_value(0.2), run_time=1.5)
        self.at("the speed of each")
        for k in (2, 3, 4):
            self.play(row.goto(k, 1.2, nt=False), jt[k].animate.set_value(SPD[k]), nv.animate.set_value(5.0 + 1.5 * (k - 1)),
                      rate.animate.set_value(0.2 + 0.1 * k), run_time=1.2)
        self.at("up to a point")
        self.play(Indicate(row.barfill, color=PURPLE, scale_factor=1.04), run_time=1.0)
        self.at("runs faster")
        self.play(Indicate(row.gauge, color=YELLOW, scale_factor=1.06), run_time=1.0)
        self.finish()


class S05Unfold(Film):
    def construct(self):
        tm = ValueTracker(0.0)
        tm.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(tm)
        C = np.array([-1.2, 0.0, 0.0])
        blk = enzyme(1.45).move_to(C)
        fold = [np.array([C[0] - 2.0 + 0.5 * k, C[1] - 0.35 + (0.45 if k % 2 == 0 else -0.45), 0]) for k in range(9)]
        loose = [np.array([C[0] - 2.2 + 0.55 * k, C[1] - 0.35 + 0.55 * np.sin(1.9 * k + 0.4), 0]) for k in range(9)]
        a = ValueTracker(0.0)
        ro = ValueTracker(0.0)
        jam = ValueTracker(0.0)

        def pts():
            aa = a.get_value()
            j = 0.03 + 0.1 * jam.get_value()
            t = tm.get_value()
            return [(1 - aa) * fold[k] + aa * loose[k] + np.array([j * np.sin(3 * t + k), j * np.cos(2.3 * t + 1.3 * k), 0])
                    for k in range(9)]
        ribbon = always_redraw(lambda: VMobject(stroke_color=BLUE, stroke_width=8, stroke_opacity=ro.get_value())
                               .set_points_smoothly(pts()))
        pairs = [(0, 2), (2, 4), (4, 6), (6, 8), (1, 3), (3, 5)]
        vs = [ValueTracker(0.0) for _ in pairs]
        links = []
        for (i, j), v in zip(pairs, vs):
            links.append(always_redraw(lambda i=i, j=j, v=v: DashedLine(pts()[i], pts()[j], color=TEXT, stroke_width=4,
                                                                         dash_length=0.1).set_stroke(opacity=v.get_value())))
        th = ValueTracker(150.0)
        DC = np.array([4.8, 0.7, 0.0])
        ring = Circle(radius=0.9, stroke_color=RED, stroke_width=6, fill_color=RED, fill_opacity=0.12).move_to(DC)
        ptr = always_redraw(lambda: Line(DC, DC + 0.75 * np.array([np.cos(np.radians(th.get_value())),
                                                                   np.sin(np.radians(th.get_value())), 0]), color=RED, stroke_width=7))
        dl = VGroup(lab("cold", 28, RED, DC + LEFT * 1.6 + DOWN * 0.3), lab("hot", 28, RED, DC + RIGHT * 1.15 + DOWN * 1.1))
        swim(blk, 0.03, 0.03, 1.5)
        self.at("protein enzyme")
        self.play(FadeIn(blk, scale=0.9), run_time=1.0)
        self.add(ribbon, *links)
        self.at("folded chain")
        self.play(ro.animate.set_value(1.0), run_time=1.4)
        self.at("held in shape")
        self.play(*[v.animate.set_value(1.0) for v in vs], run_time=1.5)
        self.at("weak attractions")
        wl = lab("weak attractions", 32, TEXT, [C[0], -2.3, 0])
        self.play(FadeIn(wl, shift=UP * 0.1), run_time=0.6)
        self.at("too much heat")
        self.add(ring, ptr)
        self.play(FadeIn(ring), FadeIn(dl), jam.animate.set_value(0.6), th.animate.set_value(35.0), run_time=2.0)
        self.at("shakes")
        for k, v in enumerate(vs):
            self.play(v.animate.set_value(0.0), a.animate.set_value((k + 1) / 8.0), run_time=0.55)
        self.play(a.animate.set_value(0.75), FadeOut(wl), run_time=0.6)
        self.at("to denature")
        dn = lab("denatured", 40, GREY, [C[0], -2.3, 0])
        self.play(Transform(blk, bad_enzyme(1.45).move_to(C)), a.animate.set_value(1.0), FadeIn(dn), run_time=1.5)
        self.at("lose the folded shape")
        self.play(Indicate(dn, color=GREY, scale_factor=1.1), run_time=1.0)
        self.finish()


class S06Counter(Film):
    def construct(self):
        jt = [ValueTracker(SPD[i]) for i in range(5)]
        row = Row(self, sel=1, jt=jt)
        row.add_tubes()
        row.add_dials()
        row.add_readouts()
        self.add(row.barfill)
        self.at("denatured enzyme")
        self.play(*row.denature(4, 8), run_time=1.8)
        self.at("not dead")
        t = lab("not dead", 36, TEXT, [-2.5, 2.5, 0])
        self.play(FadeIn(t), run_time=0.6)
        self.at("no longer fits")
        w = row.wedges[4][2]
        w.clear_updaters()
        w.move_to([TX[4] + 0.4, -2.15, 0])
        for _ in range(2):
            self.play(w.animate.move_to([TX[4] + 0.4, -1.78, 0]), run_time=0.4, rate_func=rush_into)
            self.play(w.animate.move_to([TX[4] + 0.4, -2.3, 0]), run_time=0.4, rate_func=rush_from)
        jig(w, 0.1, jt[4], 1.0, 1.0)
        self.play(FadeOut(t), run_time=0.4)
        self.at("hotter tubes")
        self.play(*row.denature(2, 2), *row.denature(3, 5), row.goto(2, 1.4), run_time=1.4)
        self.play(row.goto(3, 1.4), run_time=1.4)
        self.at("starts to fall")
        self.play(Indicate(row.counter, color=BLUE, scale_factor=1.08), run_time=1.0)
        self.finish()


# graph world ---------------------------------------------------------------------------------
def gx(T_):
    return -5.4 + (T_ - 20) / 40.0 * 10.8


def gy(v):
    return -2.4 + v * 4.4


def spd_n(T_):
    return float(np.exp(0.04 * (T_ - 60)))


def work_n(T_):
    return float(1 / (1 + np.exp((T_ - 45) / 2.5)))


_RMAX = max(spd_n(t) * work_n(t) for t in np.linspace(20, 60, 400))


def rate_n(T_):
    return spd_n(T_) * work_n(T_) / _RMAX * 0.8


def curve(fn, t0, t1, color, sw=6):
    return ParametricFunction(lambda t: np.array([gx(t), gy(fn(t)), 0.0]), t_range=[t0, t1], stroke_width=sw, color=color)


def graph_frame():
    ya = Line([-5.6, -2.5, 0], [-5.6, 2.7, 0], color=TEXT, stroke_width=4)
    xa = Line([-5.6, -2.5, 0], [5.8, -2.5, 0], color=TEXT, stroke_width=4)
    xl = lab("temperature, cold to hot", 28, TEXT, [-1.0, -3.1, 0])
    tag = lab("schematic, one test length", 24, TEXT, [3.9, -3.1, 0])
    return VGroup(ya, xa, xl, tag)


class S07Curve(Film):
    def construct(self):
        # carried: the row as it ended, then it turns into the graph
        row = Row(self, sel=3, nw=NWORK, jt=[ValueTracker(SPD[i]) for i in range(5)])
        row.add_tubes()
        row.add_dials()
        row.add_readouts()
        self.add(row.barfill)
        self.wait(0.2)
        self.at("multiply the two dials")
        fr = graph_frame()
        ty = ValueTracker(20.0)
        yc = always_redraw(lambda: curve(spd_n, 20, max(ty.get_value(), 20.01), YELLOW))
        bc = always_redraw(lambda: curve(work_n, 20, max(ty.get_value(), 20.01), BLUE))
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        self.clear()
        self.add(fr, yc, bc)
        yl = lab("speed per site", 28, YELLOW, [3.9, 2.65, 0])
        bl = lab("working sites", 28, BLUE, [-3.9, 2.65, 0])
        self.play(FadeIn(fr), ty.animate.set_value(60.0), run_time=2.6, rate_func=linear)
        self.play(FadeIn(yl), FadeIn(bl), run_time=0.6)
        self.at("at first")
        tp = ValueTracker(20.0)
        pc = always_redraw(lambda: curve(rate_n, 20, max(tp.get_value(), 20.01), PURPLE, 9))
        sc = always_redraw(lambda: DashedLine([gx(tp.get_value()), gy(0), 0], [gx(tp.get_value()), gy(1.0), 0], color=TEXT,
                                              stroke_width=3))
        dots = always_redraw(lambda: VGroup(
            Dot([gx(tp.get_value()), gy(spd_n(tp.get_value())), 0], radius=0.1, color=YELLOW),
            Dot([gx(tp.get_value()), gy(work_n(tp.get_value())), 0], radius=0.1, color=BLUE),
            Dot([gx(tp.get_value()), gy(rate_n(tp.get_value())), 0], radius=0.12, color=PURPLE)))
        self.add(pc, sc, dots)
        self.play(tp.animate.set_value(38.0), run_time=3.2, rate_func=linear)
        self.at("then the falling counter")
        self.play(tp.animate.set_value(46.0), run_time=2.4, rate_func=linear)
        self.at("rate drops")
        pl = lab("rate", 32, PURPLE, [gx(46) + 0.7, gy(rate_n(46)) + 0.4, 0])
        self.play(FadeIn(pl), tp.animate.set_value(50.0), run_time=1.0)
        self.finish()


def graph_state(sc, upto=46.0, tag=True):
    fr = graph_frame()
    yc = curve(spd_n, 20, 60, YELLOW)
    bc = curve(work_n, 20, 60, BLUE)
    pc = curve(rate_n, 20, upto, PURPLE, 9)
    yl = lab("speed per site", 28, YELLOW, [3.9, 2.65, 0])
    bl = lab("working sites", 28, BLUE, [-3.9, 2.65, 0])
    sc.add(fr, yc, bc, pc, yl, bl)
    return fr, yc, bc, pc, yl, bl


PEAK_T = max(np.linspace(20, 60, 800), key=rate_n)


class S08Often(Film):
    def construct(self):
        tp = ValueTracker(46.0)
        fr = graph_frame()
        yc = curve(spd_n, 20, 60, YELLOW)
        bc = curve(work_n, 20, 60, BLUE)
        pc = always_redraw(lambda: curve(rate_n, 20, max(tp.get_value(), 20.01), PURPLE, 9))
        yl = lab("speed per site", 28, YELLOW, [3.9, 2.65, 0])
        bl = lab("working sites", 28, BLUE, [-3.9, 2.65, 0])
        self.add(fr, yc, bc, pc, yl, bl)
        px, py = gx(PEAK_T), gy(rate_n(PEAK_T))
        mk = Dot([px, py, 0], radius=0.16, color=TEXT)
        drop = DashedLine([px, py, 0], [px, gy(0), 0], color=TEXT, stroke_width=3)
        self.at("the optimum")
        ol = lab("optimum", 34, TEXT, [px - 1.2, py - 1.2, 0])
        self.play(FadeIn(mk, scale=2.0), Create(drop), FadeIn(ol), run_time=1.2)
        swim(mk, 0.0, 0.0)
        ring = Circle(radius=0.2, color=PURPLE, stroke_width=4).move_to(mk.get_center())
        ring._tt = 0.0

        def _ring(m, dt):
            m._tt += dt
            ph = (m._tt % 1.6) / 1.6
            m.become(Circle(radius=0.2 + 0.7 * ph, color=PURPLE, stroke_width=4, stroke_opacity=1 - ph).move_to(mk.get_center()))
            m._tt = m._tt
        ring.add_updater(_ring)
        self.add(ring)
        self.at("fastest")
        self.play(Indicate(mk, color=PURPLE, scale_factor=2.0), run_time=1.0)
        self.at("above the optimum")
        band = Rectangle(width=gx(60) - px, height=5.2, stroke_width=0, fill_color=RED, fill_opacity=0.12).move_to(
            [(px + gx(60)) / 2, 0.1, 0])
        bt = lab("losing working sites", 28, RED, [px + 2.9, 2.0 + 0.0, 0])
        self.play(FadeIn(band), FadeIn(bt), tp.animate.set_value(60.0), run_time=2.4, rate_func=linear)
        self.at("often falls")
        cap = lab("Above the optimum, the rate often falls", 30, TEXT, [0, 3.4, 0])
        ul = Line(cap.get_left() + RIGHT * 4.45, cap.get_left() + RIGHT * 5.35, color=TEXT, stroke_width=5)
        ul.shift(DOWN * 0.22)
        self.play(FadeIn(cap), run_time=0.6)
        self.play(Create(ul), run_time=0.6)
        self.at("lost faster")
        greys = VGroup()
        for k, T_ in enumerate([45, 47.5, 50, 52.5, 55]):
            g = bad_enzyme(0.12).move_to([gx(T_) + 0.1, gy(work_n(T_)) + 0.35, 0])
            swim(g, 0.03, 0.03, 1.3, k)
            greys.add(g)
        self.play(FadeIn(greys, lag_ratio=0.25), run_time=2.0)
        self.finish()


class S09Canning(Film):
    def construct(self):
        cutT = ValueTracker(0.0)
        lt = ValueTracker(0.0)
        CX, CY = -3.9, -0.1
        can = Rectangle(width=2.6, height=3.2, stroke_color=GREY, stroke_width=6, fill_color=GREY, fill_opacity=0.12).move_to([CX, CY, 0])
        blocks = []
        for j in range(8):
            b = enzyme(0.26).move_to([CX + (-0.62 if j % 2 == 0 else 0.62), CY + 0.95 - 0.62 * (j // 2), 0])
            jig(b, 0.03, None, 1.4, j)
            blocks.append(b)
        cl = lab("canned pineapple", 30, PINE, [CX, 2.0, 0])
        stove = Rectangle(width=3.2, height=0.3, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.35).move_to([CX, -1.9, 0])
        flames = VGroup()
        for k in range(4):
            f = Triangle(stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.8).scale(0.22).move_to([CX - 0.9 + 0.6 * k, -2.35, 0])
            f.ph = k
            f._t = 0.0

            def uf(m, dt):
                m._t += dt
                m.stretch_to_fit_height(0.4 + 0.12 * np.sin(9 * m._t + m.ph), about_edge=UP)
            f.add_updater(uf)
            flames.add(f)
        DC = np.array([-1.4, 0.0, 0.0])
        th = ValueTracker(150.0)
        ring = Circle(radius=0.7, stroke_color=RED, stroke_width=6, fill_color=RED, fill_opacity=0.12).move_to(DC)
        ptr = always_redraw(lambda: Line(DC, DC + 0.58 * np.array([np.cos(np.radians(th.get_value())), np.sin(np.radians(th.get_value())), 0]),
                                         color=RED, stroke_width=7))
        nt = ValueTracker(8.0)
        counter = always_redraw(lambda: counter_text(int(round(nt.get_value()))))
        ys = [-1.9, -1.0, -0.1, 0.8, 1.7]
        ch = Chains(1.6, 6.2, ys, 9, seed=7, cutT=cutT, rad=0.11)
        lk = ch.links(lt, [2, 5])
        self.at("back to the pineapple")
        self.play(FadeIn(can), *[FadeIn(b) for b in blocks], FadeIn(cl), FadeIn(counter), FadeIn(ch.all), run_time=1.4)
        self.add(counter)
        self.add(*lk)
        self.at("canning heats")
        self.add(ptr)
        self.play(FadeIn(stove), FadeIn(flames), FadeIn(ring), th.animate.set_value(35.0), run_time=1.6)
        self.at("denature")
        self.play(*[Transform(b, bad_enzyme(0.26).move_to(b.get_center())) for b in blocks[::2]], run_time=1.2)
        self.play(*[Transform(b, bad_enzyme(0.26).move_to(b.get_center())) for b in blocks[1::2]], run_time=1.2)
        self.at("the counter falls")
        self.play(nt.animate.set_value(0.0), run_time=1.4, rate_func=linear)
        self.remove(counter)
        almost = lab("working sites: almost none (schematic)", 30, BLUE, [-6.5, 3.4, 0]).set_opacity(0.7)
        almost.move_to([-6.5, 3.4, 0], aligned_edge=LEFT)
        self.add(almost)
        self.at("too little")
        t = lab("too few left to cut", 32, TEXT, [3.9, 2.8, 0])
        self.play(FadeIn(t), run_time=0.6)
        self.at("cut the gelatin chains")
        self.play(Indicate(ch.all, color=ORANGE, scale_factor=1.02), run_time=1.2)
        self.at("link up")
        self.play(lt.animate.set_value(1.0), FadeOut(t), run_time=1.6)
        self.at("gelatin sets")
        fin = lab("canned: bromelain denatured, gelatin sets", 30, TEXT, [0.0, -3.4, 0])
        self.play(FadeIn(fin, shift=UP * 0.1), run_time=0.8)
        self.finish()


BOWL_C = np.array([3.2, -0.4, 0.0])
BOWL_R = 2.4
GREY_POS = [(1.9, -1.1), (3.0, -0.5), (4.2, -1.1), (3.2, -1.7)]


def bowl_world(sc, lt=None, cut=None):
    b = Sector(radius=BOWL_R, start_angle=PI, angle=PI, stroke_color=GREY, stroke_width=6, fill_color=ORANGE, fill_opacity=0.15)
    b.move_to([BOWL_C[0], BOWL_C[1] - 0.425 * BOWL_R, 0])
    ch = Chains(1.7, 4.7, [-0.8, -1.4, -2.0], 9, seed=11, rad=0.1)
    lk = ch.links(lt if lt is not None else ValueTracker(0.0), [2, 5]) if lt is not None else []
    return b, ch, lk


class S10Predict(Film):
    def construct(self):
        tm = ValueTracker(0.0)
        tm.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(tm)
        GX, GY = -3.6, -0.4
        glass = RoundedRectangle(corner_radius=0.3, width=2.2, height=3.0, stroke_color=TEXT, stroke_width=5).move_to([GX, GY, 0])
        juice = Rectangle(width=2.0, height=2.3, stroke_width=0, fill_color=PINE, fill_opacity=0.3).move_to([GX, GY - 0.3, 0])
        blks = []
        for j in range(4):
            b = enzyme(0.26).move_to([GX + (-0.5 if j % 2 == 0 else 0.5), GY - 0.1 - 0.6 * (j // 2), 0])
            jig(b, 0.04, None, 1.4, j)
            blks.append(b)
        DC = np.array([GX, 2.25, 0])
        th = ValueTracker(150.0)
        ring = Circle(radius=0.55, stroke_color=RED, stroke_width=6, fill_color=RED, fill_opacity=0.12).move_to(DC)
        ptr = always_redraw(lambda: Line(DC, DC + 0.46 * np.array([np.cos(np.radians(th.get_value())), np.sin(np.radians(th.get_value())), 0]),
                                         color=RED, stroke_width=7))
        dl = VGroup(lab("cold", 26, RED, DC + LEFT * 1.1 + DOWN * 0.1), lab("hot", 26, RED, DC + RIGHT * 0.95 + DOWN * 0.1))
        gl = lab("fresh pineapple juice", 30, PINE, [GX, -2.55, 0])
        bw, ch, _ = bowl_world(self)
        self.at("now a harder one")
        self.play(FadeIn(glass), FadeIn(juice), *[FadeIn(b) for b in blks], FadeIn(gl), FadeIn(bw), FadeIn(ch.all), run_time=1.4)
        self.at("fresh pineapple juice")
        self.play(Indicate(juice, color=PINE, scale_factor=1.03), run_time=1.0)
        self.at("as hot as canning")
        self.add(ptr)
        self.play(FadeIn(ring), FadeIn(dl), th.animate.set_value(35.0), run_time=1.4)
        clock = Circle(radius=0.4, stroke_color=TEXT, stroke_width=5).move_to([-0.7, 1.3, 0])
        hand = Line([-0.7, 1.3, 0], [-0.7, 1.6, 0], color=TEXT, stroke_width=5)
        hand.add_updater(lambda m, dt: m.rotate(-2.2 * dt, about_point=np.array([-0.7, 1.3, 0])))
        self.play(Create(clock), FadeIn(hand), run_time=0.6)
        self.at("denature most")
        self.play(*[Transform(b, bad_enzyme(0.26).move_to(b.get_center())) for b in blks[:2]], run_time=1.2)
        self.play(*[Transform(b, bad_enzyme(0.26).move_to(b.get_center())) for b in blks[2:]], run_time=1.2)
        self.at("then cool it")
        ice = VGroup(*[Square(side_length=0.38, stroke_color=WATER, stroke_width=3, fill_color=WATER, fill_opacity=0.25)
                       .move_to([GX - 1.1 + 0.73 * k, -2.05 + 0.04 * (k % 2), 0]).rotate(0.2 * k) for k in range(4)])
        self.play(th.animate.set_value(150.0), FadeIn(ice), FadeOut(clock), FadeOut(hand), run_time=1.6)
        self.at("add it to gelatin")
        for b in blks:
            b.clear_updaters()
        self.play(*[b.animate.move_to([GREY_POS[i][0], GREY_POS[i][1], 0]).scale(0.3 / 0.26 * 0.26 / 0.26) for i, b in enumerate(blks)],
                  juice.animate.set_opacity(0.0), run_time=2.4, rate_func=smooth)
        self.play(*[FadeOut(m) for m in (glass, juice, gl, ring, dl, ice)], FadeOut(ptr), run_time=0.8)
        for i, b in enumerate(blks):
            jig(b, 0.03, None, 1.2, i)
        self.at("will the gelatin set")
        q = lab("working sites: ?", 32, BLUE, ORIGIN)
        q.move_to([-6.5, 3.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(q), run_time=0.6)
        self.play(Indicate(q, color=BLUE, scale_factor=1.1), run_time=0.9)
        self.finish()


def pause_state(sc):
    bw, ch, _ = bowl_world(sc)
    greys = []
    for i, (x, y) in enumerate(GREY_POS):
        g = bad_enzyme(0.26).move_to([x, y, 0])
        jig(g, 0.03, None, 1.2, i)
        greys.append(g)
    q = lab("working sites: ?", 32, BLUE, [-6.5, 3.4, 0])
    q.move_to([-6.5, 3.4, 0], aligned_edge=LEFT)
    sc.add(bw, ch.all, *greys, q)
    return bw, ch, greys, q


class S11Pause(NarratedScene):
    def construct(self):
        bw, ch, greys, q = pause_state(self)
        pt = lab("Predict: set or runny?", 40, TEXT, [-3.0, 0.3, 0])
        self.add(pt)
        ring_bg = Circle(radius=0.45, stroke_color=GREY, stroke_width=5).move_to([-3.0, -1.4, 0])
        tt = ValueTracker(0.0)
        ring = always_redraw(lambda: Arc(radius=0.45, start_angle=PI / 2, angle=-TAU * max(tt.get_value(), 0.001),
                                         stroke_color=TEXT, stroke_width=7, arc_center=[-3.0, -1.4, 0]))
        self.add(ring_bg, ring)
        self.play(tt.animate.set_value(1.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S12Reveal(Film):
    def construct(self):
        lt = ValueTracker(0.0)
        bw, ch, greys, q = pause_state(self)
        lk = ch.links(lt, [2, 5])
        self.add(*lk)
        DC = np.array([-0.2, 1.4, 0.0])
        ring, ptr = make_dial(DC, 0.5, np.radians(150), 6)
        dlab = lab("cold", 28, RED, DC + DOWN * 0.8)
        pan = Circle(radius=1.25, stroke_color=GREY, stroke_width=6, fill_color=GREY, fill_opacity=0.18).move_to([-3.9, -0.6, 0])
        egg = Ellipse(width=1.6, height=1.2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.08).move_to([-3.9, -0.6, 0])
        egg.set_stroke(opacity=0.5)
        swim(egg, 0.02, 0.02, 1.4)
        self.at("likely to set")
        c1 = lab("likely to set", 36, TEXT, [3.2, 1.9, 0])
        self.play(FadeIn(c1), lt.animate.set_value(1.0), run_time=1.6)
        self.at("cooling does not")
        self.play(FadeIn(ring), FadeIn(ptr), FadeIn(dlab), run_time=0.8)
        self.play(Indicate(q, color=BLUE, scale_factor=1.06), run_time=0.8)
        a2 = lab("working sites: almost none (schematic)", 30, BLUE, [-6.5, 3.4, 0]).set_opacity(0.7)
        a2.move_to([-6.5, 3.4, 0], aligned_edge=LEFT)
        self.play(FadeOut(q), FadeIn(a2), *[Indicate(g, color=GREY, scale_factor=1.2) for g in greys], run_time=1.2)
        self.at("a few proteins")
        self.play(Indicate(c1, color=TEXT, scale_factor=1.05), run_time=1.0)
        self.at("heat damage")
        self.play(FadeIn(pan), FadeIn(egg), run_time=0.8)
        self.at("often permanent")
        c2 = lab("often permanent", 36, TEXT, [3.2, 1.1, 0])
        self.play(FadeIn(c2), egg.animate.set_fill(TEXT, 0.4), run_time=1.0)
        self.at("cooked egg white")
        self.play(egg.animate.set_fill(TEXT, 0.9), run_time=1.0)
        plate = Circle(radius=1.25, stroke_color=TEXT, stroke_width=4, fill_opacity=0).move_to([-3.9, -0.6, 0])
        self.play(Transform(pan, plate), run_time=0.8)
        self.finish()


class S13Close(Film):
    def construct(self):
        fr, yc, bc, pc, yl, bl = graph_state(self, 60.0)
        px, py = gx(PEAK_T), gy(rate_n(PEAK_T))
        mk = Dot([px, py, 0], radius=0.16, color=TEXT)
        ol = lab("optimum", 34, TEXT, [px - 1.2, py - 1.2, 0])
        a1 = Arrow([gx(24) + 0.1, 0.9, 0], [px - 0.3, py + 0.05, 0], buff=0.1, color=YELLOW, stroke_width=6)
        a2 = Arrow([gx(55), 0.7, 0], [px + 0.3, py + 0.05, 0], buff=0.1, color=BLUE, stroke_width=6)
        t1 = lab("faster sites", 28, YELLOW, [gx(24) - 0.2, 1.3, 0])
        t2 = lab("working sites lost", 28, BLUE, [2.35, 1.65, 0])
        swim(mk, 0.0, 0.0)
        ring = Circle(radius=0.2, color=PURPLE, stroke_width=4).move_to(mk.get_center())
        ring._tt = 0.0

        def _ring(m, dt):
            m._tt += dt
            ph = (m._tt % 1.6) / 1.6
            m.become(Circle(radius=0.2 + 0.7 * ph, color=PURPLE, stroke_width=4, stroke_opacity=1 - ph).move_to(mk.get_center()))
            m._tt = m._tt
        ring.add_updater(_ring)
        self.add(ring)
        self.wait(0.3)
        self.at("heat speeds up each working site")
        self.play(FadeIn(t1), GrowArrow(a1), Indicate(yl, color=YELLOW, scale_factor=1.1), run_time=1.5)
        self.at("can take sites out of work")
        self.play(FadeIn(t2), GrowArrow(a2), Indicate(bl, color=BLUE, scale_factor=1.1), run_time=1.5)
        self.at("in this model")
        cap = lab("in this model", 32, TEXT, [0.0, 3.4, 0])
        self.play(FadeIn(cap), run_time=0.6)
        self.at("the rate peaks")
        self.play(FadeIn(mk, scale=2.0), FadeIn(ol), run_time=1.0)
        self.at("faster sites are offset")
        self.play(Indicate(mk, color=PURPLE, scale_factor=2.0), run_time=1.4)
        self.at("real optima")
        c2 = lab("real optima can have other causes", 32, TEXT, [0.0, 3.4, 0])
        self.play(Transform(cap, c2), run_time=0.8)
        self.at("depend on the test")
        c3 = lab("and depend on the test", 32, TEXT, [0.0, 3.4, 0])
        self.play(Transform(cap, c3), run_time=0.8)
        self.finish()


class S14End(EndCard):
    LINE = "Heat speeds each working site but can remove sites, so rate peaks."
