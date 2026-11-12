"""Eight Females from Texas (conservation, film 2: genetic rescue)

COLOUR MAP (same as film 1, plus ancestry colours)
  BLUE   = population runs (log numbers vs years)      RED  = the floor (10 animals)
  GOLD   = the trend arrow                             TEXT = labels
  YELLOW = gauges and the question
  TEAL   = Florida ancestry   PURPLE = Texas ancestry   TEAL with PURPLE stripes = admixed
The chart is film 1's chart, same place and size, zoomed on the y axis (10 to 100 animals).
The blue run is a random walk on log numbers (seed 950, row chosen once, swings 0.05 a year) with
the trend set by phase; it is a schematic of the story, not panther data. Pumas and maps are schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#A97BE0"
FLOOR = float(np.log(10))
YLO, YHI = 1.8, 5.0
Z = np.random.default_rng(950).standard_normal((200, 1000))


def _path():
    t = np.arange(100)
    mu = np.where(t < 50, -0.01, np.where(t < 75, 0.04, np.where(t < 87, 0.0, -0.025)))
    for r in range(200):
        x = np.log(25) + np.concatenate([[0], np.cumsum(mu + 0.05 * Z[r, :100])])
        if x[:51].min() > FLOOR + 0.25 and 2.55 < x[50] < 2.9 and x[75] - x[50] > 0.8 and x[75] < 3.9 \
                and x[100] < x[87] - 0.2 and x.max() < 4.2:
            return x
    return np.log(25) + np.concatenate([[0], np.cumsum(mu)])


PATH = _path()


class ZP:
    """Film 1's main chart panel (same box), y axis zoomed to 1.8..5.0 in ln numbers."""

    def __init__(s, x0=-5.1, y0=-3.0, w=8.7, h=5.3, yticks=True, xlabel=True):
        s.x0, s.y0, s.w, s.h, s.yticks, s.xlabel = x0, y0, w, h, yticks, xlabel

    def X(s, t):
        return s.x0 + s.w * min(t, 100) / 100.0

    def Y(s, l):
        return s.y0 + s.h * (min(max(l, YLO), YHI) - YLO) / (YHI - YLO)

    def floor_line(s):
        return DashedLine([s.x0, s.Y(FLOOR), 0], [s.x0 + s.w, s.Y(FLOOR), 0], color=RED, stroke_width=4, dash_length=0.18)

    def base(s):
        g = VGroup(Rectangle(width=s.w, height=s.h, stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                             fill_opacity=0.07).move_to([s.x0 + s.w / 2, s.y0 + s.h / 2, 0]))
        ry = s.y0 - 0.32
        for t in (0, 100):
            g.add(M(str(t), 24).move_to([s.X(t), ry, 0]))
        if s.xlabel:
            g.add(T("years", 24).move_to([s.x0 + s.w / 2, ry, 0]))
        if s.yticks:
            for n in (10, 30, 100):
                lab = M(str(n), 24).move_to([0, s.Y(np.log(n)), 0])
                lab.set_x(s.x0 - 0.15 - lab.width / 2)
                g.add(lab)
            g.add(T("numbers (log scale)", 24).rotate(PI / 2).move_to([s.x0 - 1.3, s.y0 + s.h / 2, 0]))
        return g


class Run(VMobject):
    def __init__(s, P, k, color=BLUE, width=6):
        super().__init__()
        s.P, s.k, s.col, s.wd = P, k, color, width
        s.add_updater(lambda m: m._upd())
        s._upd()

    def _upd(s):
        kv = min(max(s.k.get_value(), 0), 100)
        i = int(kv)
        f = kv - i
        pts = [[s.P.X(t), s.P.Y(PATH[t]), 0] for t in range(i + 1)]
        if f > 1e-6 and i < 100:
            pts.append([s.P.X(i + f), s.P.Y(PATH[i] + f * (PATH[i + 1] - PATH[i])), 0])
        if len(pts) < 2:
            pts = [pts[0], pts[0]]
        s.set_points_as_corners(np.array(pts, float))
        s.set_stroke(s.col, s.wd, 1 if kv > 0 else 0)
        s.set_fill(opacity=0)


def tarrow(P, slope, t_c=45, y_c=3.0, half=24, color=GOLD):
    def build():
        sl = slope.get_value()
        a = np.array([P.X(t_c - half), P.Y(y_c - sl * half), 0])
        b = np.array([P.X(t_c + half), P.Y(y_c + sl * half), 0])
        return Arrow(a, b, buff=0, color=color, stroke_width=8, max_tip_length_to_length_ratio=0.18,
                     max_stroke_width_to_length_ratio=12).set_z_index(5)
    a = build()
    a.add_updater(lambda m: m.become(build()))
    return a


class World:
    """Film 1's chart with the run, the floor and the gold arrow: built once, carried scene to scene."""

    def __init__(s, k=50, slope=-0.02, P=None, flab=True):
        s.P = P or ZP()
        s.k, s.sl = ValueTracker(k), ValueTracker(slope)
        s.base, s.floor = s.P.base(), s.P.floor_line()
        s.run = Run(s.P, s.k)
        s.arrow = tarrow(s.P, s.sl)
        s.flab = T("floor", 34, RED, weight=BOLD).move_to([5.1, s.P.Y(FLOOR) + 0.35, 0]) if flab else VGroup()


class Live(VGroup):
    def __init__(s, fn, size=30, color=TEXT, mono=False, anchor=ORIGIN, left=False):
        super().__init__()
        s.fn, s.size, s.color, s.mono, s.anchor, s.left, s._cache = fn, size, color, mono, np.array(anchor, float), left, {}
        s.add_updater(lambda m: m._upd())
        s._upd()

    def _upd(s):
        t = s.fn()
        if t not in s._cache:
            m = (M if s.mono else T)(t, s.size, s.color)
            m.move_to(s.anchor + (RIGHT * m.width / 2 if s.left else ORIGIN))
            s._cache[t] = m
            s.add(m)
        for k, m in s._cache.items():
            m.set_opacity(1 if k == t else 0)


def idle(m, amp=0.05, per=3.0, ph=0.0):
    st = {"t": ph}

    def f(mm, dt):
        st["t"] += dt
        mm.shift(UP * amp * np.sin(2 * np.pi * st["t"] / per) * dt * 2 * np.pi / per)
    m.add_updater(f)
    return m


def check(size=0.5, color=GREEN):
    c = VGroup(Line([-0.5, 0, 0], [-0.15, -0.35, 0]), Line([-0.15, -0.35, 0], [0.5, 0.45, 0])).set_stroke(color, 7)
    return c.scale(size)


# ---- pumas and maps (schematic cartoons) ---------------------------------------------------------
def puma(color=TEAL, scale=1.0, stripes=False, kink=False):
    body = Ellipse(width=1.5, height=0.62, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)
    head = Circle(radius=0.26, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5).move_to([0.85, 0.25, 0])
    ears = VGroup(Polygon([0.68, 0.43, 0], [0.76, 0.74, 0], [0.9, 0.5, 0]), Polygon([0.88, 0.5, 0], [1.02, 0.74, 0], [1.1, 0.4, 0]))
    ears.set_stroke(color, 3).set_fill(color, 0.5)
    legs = VGroup(*[Line([x, -0.26, 0], [x, -0.72, 0]) for x in (-0.5, -0.22, 0.3, 0.58)]).set_stroke(color, 6)
    tp = [[-0.72, 0.08, 0], [-1.0, 0.15, 0], [-1.0, 0.5, 0], [-1.3, 0.5, 0], [-1.3, 0.95, 0]] if kink else \
         [[-0.72, 0.08, 0], [-1.0, 0.2, 0], [-1.2, 0.5, 0], [-1.3, 0.95, 0]]
    tail = VMobject().set_points_as_corners(np.array(tp, float)).set_stroke(color, 6)
    g = VGroup(tail, legs, body, head, ears)
    if stripes:
        g.add(VGroup(*[Line([x, -0.27, 0], [x, 0.27, 0]) for x in (-0.4, 0.0, 0.4)]).set_stroke(PURPLE, 7))
        head.set_stroke(PURPLE, 3)
    return g.scale(scale)


FL_PTS = [(-1.0, 1.5), (0.9, 1.5), (1.0, 0.9), (0.8, 0.3), (1.0, -0.4), (0.8, -1.1), (0.45, -1.6), (0.15, -1.0),
          (-0.15, -0.45), (-0.8, -0.15), (-1.0, 0.5)]
TX_PTS = [(-1.0, 0.9), (0.0, 0.9), (0.0, 1.5), (0.6, 1.5), (0.9, 0.9), (1.0, 0.0), (0.6, -0.7), (0.0, -1.4),
          (-0.3, -0.9), (-0.7, -0.5), (-0.9, 0.2)]


def outline(pts, sc, c, color=GREY):
    p = Polygon(*[np.array([x * sc + c[0], y * sc + c[1], 0]) for x, y in pts], color=color, stroke_width=3,
                fill_color=color, fill_opacity=0.10)
    return p.round_corners(0.25 * sc)


def patch(sc, c, color=TEAL, op=0.55):
    return Ellipse(width=0.8 * sc, height=1.0 * sc, stroke_color=color, stroke_width=3, fill_color=color,
                   fill_opacity=op).move_to([c[0] + 0.15 * sc, c[1] - 0.55 * sc, 0])


def vortex_loop(cx, cy, r, trav=True):
    cols = [RED, TEAL, YELLOW, GOLD]
    angs = [180, 90, 0, -90]
    dots = VGroup(*[Dot(radius=0.17, color=cols[i]).move_to([cx + r * np.cos(np.radians(a)), cy + r * np.sin(np.radians(a)), 0])
                    for i, a in enumerate(angs)])
    arcs = VGroup()
    for a in angs:
        arc = Arc(radius=r, start_angle=np.radians(a - 22), angle=-np.radians(46), arc_center=[cx, cy, 0], color=TEXT, stroke_width=5)
        arc.add_tip(tip_length=0.2, tip_width=0.2)
        arcs.add(arc)
    g = VGroup(arcs, dots)
    if trav:
        d = Dot(radius=0.12, color=TEXT).set_z_index(6)
        st = {"t": 0.0}

        def mv(m, dt):
            st["t"] += dt
            a = np.radians(180 - 360 * st["t"] / 6.0)
            m.move_to([cx + r * np.cos(a), cy + r * np.sin(a), 0])
        d.add_updater(mv)
        g.add(d)
    return g


class S(SpokenScene):
    def to(self, phrase, lead=0.3, nth=0, mn=0.3):
        return max(mn, self.t_of(phrase, nth) - lead - self.elapsed())

    def rest(self, pad=0.3, mn=0.3):
        return max(mn, self.narration_s - self.elapsed() - pad)


class S00Title(TitleCard):
    LESSON = "Conservation and Restoration"
    TITLE = "Eight Females from Texas"


class S01Link(S):
    def construct(self):
        W = World(k=0, slope=0.0)
        tag = T("survival held fixed?", 34, YELLOW, weight=BOLD).move_to([-0.8, 3.3, 0])
        strike = Line(tag.get_left() + LEFT * 0.1, tag.get_right() + RIGHT * 0.1, color=RED, stroke_width=7)
        loop = vortex_loop(5.35, 1.0, 0.95)
        vl = T("extinction\nvortex", 28, RED, weight=BOLD).move_to([5.35, -0.8, 0])
        self.play(FadeIn(W.base), Create(W.floor), FadeIn(W.flab), run_time=1.4)
        self.add(W.run)
        self.play(W.k.animate.set_value(50), run_time=self.to("survival fixed" if False else "can miss"), rate_func=linear)
        self.play(FadeIn(tag), run_time=0.6)
        self.at("can miss")
        self.play(Create(strike), run_time=0.6)
        self.at("If inbreeding keeps")
        self.play(FadeIn(loop), FadeIn(vl), run_time=0.8)
        self.at("the trend tilts down")
        self.add(W.arrow)
        self.play(W.sl.animate.set_value(-0.02), run_time=1.6, rate_func=smooth)
        self.at("Can adding new genes")
        ng = chip("new genes?", PURPLE, 30).move_to([5.2, -2.7, 0])
        self.play(FadeIn(ng, shift=UP * 0.3), run_time=0.8)
        self.play(Indicate(ng, color=PURPLE, scale_factor=1.12), run_time=1.2)
        self.finish()


class S02Panthers(S):
    def construct(self):
        mp = outline(FL_PTS, 1.6, (-4.0, -0.5))
        pt = patch(1.6, (-4.0, -0.5))
        lab = T("Florida panthers:\nsmall, isolated", 28, TEAL, weight=BOLD).move_to([-4.0, 3.0, 0])
        self.play(Create(mp), run_time=1.5)
        self.at("small")
        self.play(FadeIn(pt, scale=0.5), run_time=0.8)
        self.add(idle(pt, 0.04, 2.5))
        self.play(FadeIn(lab), run_time=0.8)
        pn = puma(TEAL, 1.6, kink=True).move_to([3.2, -0.1, 0])
        self.at("Its animals showed")
        self.play(FadeIn(pn, shift=LEFT * 0.4), run_time=1.2)
        idle(pn, 0.05, 3.0)
        t1 = chip("kinked tail", YELLOW, 28).move_to([0.0, 2.3, 0])
        l1 = Line([0.8, 1.95, 0], [1.1, 1.5, 0], color=YELLOW, stroke_width=4)
        t2 = chip("heart defects", YELLOW, 28).move_to([4.3, 2.55, 0])
        l2 = Line([3.9, 2.18, 0], [3.85, 0.4, 0], color=YELLOW, stroke_width=4)
        t3 = chip("poor sperm", YELLOW, 28).move_to([4.0, -2.55, 0])
        l3 = Line([3.3, -2.17, 0], [3.3, -0.4, 0], color=YELLOW, stroke_width=4)
        self.at("kink")
        self.play(FadeIn(t1), Create(l1), run_time=0.7)
        self.at("heart defects")
        self.play(FadeIn(t2), Create(l2), run_time=0.7)
        self.at("poor sperm")
        self.play(FadeIn(t3), Create(l3), run_time=0.7)
        self.play(Indicate(pn, color=YELLOW, scale_factor=1.04), run_time=1.2)
        self.finish()


class S03Axes(S):
    def construct(self):
        W = World(k=50, slope=0.0)
        loop = vortex_loop(5.35, 1.0, 0.95)
        mb = chip("more\ninbreeding", TEAL, 28).move_to([5.35, 2.95, 0])
        tag = chip("Florida panthers", TEAL, 28).move_to([-2.4, 3.3, 0])
        self.add(W.base, W.floor, W.flab, W.run)
        self.play(FadeIn(tag), run_time=0.8)
        self.at("Numbers sit close")
        gx = W.P.X(50)
        gap = DoubleArrow([gx, W.P.Y(PATH[50]) - 0.08, 0], [gx, W.P.Y(FLOOR) + 0.08, 0], color=TEXT, stroke_width=4, buff=0,
                          tip_length=0.15)
        dot = Dot([gx, W.P.Y(PATH[50]), 0], radius=0.13, color=YELLOW).set_z_index(6)
        self.play(FadeIn(dot), GrowFromCenter(gap), run_time=1.2)
        self.play(Indicate(W.floor, color=RED), run_time=1.2)
        self.at("Inbreeding can lower")
        self.play(FadeIn(loop), FadeIn(mb), run_time=0.8)
        self.at("the gold arrow tilts down")
        self.add(W.arrow)
        self.play(W.sl.animate.set_value(-0.02), run_time=1.6, rate_func=smooth)
        self.at("The vortex is turning")
        self.play(Indicate(mb, color=TEAL, scale_factor=1.12), run_time=1.4)
        self.finish()


class S04Release(S):
    def construct(self):
        tx_c, fl_c = (-4.3, 0.0), (4.4, -0.35)
        tx = outline(TX_PTS, 1.7, tx_c, PURPLE)
        fl = outline(FL_PTS, 1.7, fl_c)
        pt = patch(1.7, fl_c)
        lt = T("Texas", 34, PURPLE, weight=BOLD).move_to([-4.3, -2.3, 0])
        lf = T("Florida", 34, TEAL, weight=BOLD).move_to([4.4, -3.35, 0])
        yr = T("1995", 56, TEXT, weight=BOLD, font=TITLE_FONT).move_to([-3.0, 3.2, 0])
        self.add(tx, fl, pt, lt, lf)
        self.play(FadeIn(yr, shift=DOWN * 0.2), run_time=0.8)
        self.at("managers tried")
        gr = T("a genetic rescue", 40, GOLD, weight=BOLD).move_to([2.2, 3.2, 0])
        self.play(Write(gr), run_time=1.6)
        self.at("They released eight")
        pumas = VGroup(*[puma(PURPLE, 0.33).move_to([tx_c[0] - 0.6 + (i % 4) * 0.55, tx_c[1] + 0.6 - (i // 4) * 0.7, 0]) for i in range(8)])
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pumas], lag_ratio=0.12), run_time=1.4)
        self.at("from Texas")
        self.play(Indicate(lt, color=PURPLE), run_time=0.8)
        self.at("into the Florida")
        tgt = patch(1.7, fl_c).get_center()
        anims = []
        for i, p in enumerate(pumas):
            dest = tgt + np.array([(i % 4 - 1.5) * 0.28, (i // 4 - 0.5) * 0.4, 0])
            path = ArcBetweenPoints(p.get_center(), dest, angle=-0.5)
            anims.append(MoveAlongPath(p, path))
        self.play(LaggedStart(*anims, lag_ratio=0.1), run_time=max(1.5, self.t_of("population") - self.elapsed() + 1.2))
        self.play(Indicate(pt, color=PURPLE, scale_factor=1.15), run_time=1.0)
        self.finish()


class S04bSame(S):
    def construct(self):
        fp = puma(TEAL, 1.2, kink=True).move_to([-3.6, 1.6, 0])
        tp = puma(PURPLE, 1.2).move_to([3.6, 1.6, 0])
        ls = T("one species,\ntwo populations", 28, TEXT, weight=BOLD).move_to([0, 1.7, 0])
        lf = T("Florida", 28, TEAL, weight=BOLD).move_to([-3.6, 0.35, 0])
        lt = T("Texas", 28, PURPLE, weight=BOLD).move_to([3.6, 0.35, 0])
        self.play(FadeIn(fp), FadeIn(lf), run_time=0.9)
        self.play(FadeIn(tp), FadeIn(lt), run_time=0.9)
        idle(fp, 0.04, 3.0)
        idle(tp, 0.04, 3.4, 1.0)
        self.at("same species")
        self.play(FadeIn(ls), run_time=0.8)
        self.at("Adding animals")
        small = puma(PURPLE, 0.4).move_to(tp.get_center() + DOWN * 0.1)
        self.play(FadeIn(small), run_time=0.3)
        self.play(small.animate.move_to(fp.get_center() + RIGHT * 1.9 + DOWN * 0.9), run_time=2.2, rate_func=smooth)
        self.at("reinforcement")
        rl = T("reinforcement", 40, GOLD, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(rl), run_time=0.8)
        self.at("The aim was genetic")
        self.play(FadeOut(VGroup(ls, lf, lt, small)), run_time=0.6)
        pairs = []
        row = VGroup()
        for i in range(6):
            a = Square(0.55, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.65)
            b = Square(0.55, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.65)
            pr = VGroup(a, b).arrange(RIGHT, buff=0.06).move_to([-5.0 + i * 2.0, -1.45, 0])
            pairs.append(pr)
            row.add(pr)
        lab = T("identical pairs", 32, TEAL, weight=BOLD).move_to([0, -2.75, 0])
        self.play(FadeIn(row, shift=UP * 0.2), FadeIn(lab), run_time=1.0)
        self.at("to reverse inbreeding")
        self.play(Indicate(tp, color=PURPLE, scale_factor=1.1), run_time=1.0)
        self.at("new gene versions")
        newlab = T("mixed pairs", 32, PURPLE, weight=BOLD).move_to([0, -2.75, 0])
        anims = [pairs[i][1].animate.set_fill(PURPLE, 0.8).set_stroke(PURPLE) for i in (0, 2, 3, 5)]
        self.play(LaggedStart(*anims, lag_ratio=0.25), Transform(lab, newlab), run_time=2.2)
        self.finish()


# ---- generation strip used in films s05 and s10 --------------------------------------------------
GEN_X = [-5.5, -3.3, -1.1, 1.1, 3.3, 5.5]
GEN_Y = [1.0, -0.2, -1.4]
GEN_MIX = [(4, 2, 0), (3, 1, 2), (2, 0, 4), (1, 0, 5), (1, 0, 5), (0, 0, 6)]


def gen_col(k):
    teal, purple, stripe = GEN_MIX[k]
    kinds = ["T"] * teal + ["P"] * purple + ["S"] * stripe
    g = VGroup()
    for j, kd in enumerate(kinds):
        col = PURPLE if kd == "P" else TEAL
        p = puma(col, 0.46, stripes=(kd == "S"))
        p.move_to([GEN_X[k] + (-0.58 if j % 2 == 0 else 0.58), GEN_Y[j // 2], 0])
        p.striped = kd == "S"
        g.add(p)
    return g


def gen_arrow(k):
    return Arrow([GEN_X[k] + 1.0, 0.05, 0], [GEN_X[k + 1] - 1.0, 0.05, 0], buff=0, color=GREY, stroke_width=4,
                 max_tip_length_to_length_ratio=0.5, tip_length=0.15)


class S05Kittens(S):
    def construct(self):
        cols = [gen_col(k) for k in range(4)]
        self.play(FadeIn(cols[0]), run_time=1.0)
        self.at("more and more")
        self.play(FadeIn(cols[1], shift=RIGHT * 0.3), run_time=1.2)
        self.at("carried both")
        self.play(FadeIn(cols[2], shift=RIGHT * 0.3), run_time=1.2)
        self.play(FadeIn(cols[3], shift=RIGHT * 0.3), run_time=1.2)
        self.at("Biologists call")
        lab = T("admixed: both ancestries", 40, TEXT, weight=BOLD).move_to([0, -2.8, 0])
        self.play(FadeIn(lab), run_time=0.9)
        self.play(*[Indicate(p, color=PURPLE, scale_factor=1.15) for c in cols[1:] for p in c if p.striped], run_time=1.6)
        self.finish()


class S06Het(S):
    def construct(self):
        trk = {"c": ValueTracker(0.25), "h": ValueTracker(0.3)}
        bars, ros = gauge_strip(trk)
        self.at("track two things")
        self.play(FadeIn(bars[0]), run_time=0.8)
        self.play(FadeIn(bars[1]), run_time=0.8)
        self.at("the head count")
        self.play(Indicate(bars[0][0], color=YELLOW), trk["c"].animate.set_value(0.3), run_time=1.4)
        head = T("one gene position, two copies", 32, TEXT, weight=BOLD).move_to([0, 1.35, 0])
        A = VGroup(*[Square(1.4, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.65) for _ in range(2)]).arrange(RIGHT, buff=0.1).move_to([-3.2, -0.3, 0])
        B = VGroup(Square(1.4, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.65),
                   Square(1.4, stroke_color="#A8E6EA", stroke_width=4, fill_color="#A8E6EA", fill_opacity=0.65)).arrange(RIGHT, buff=0.1).move_to([3.2, -0.3, 0])
        la = T("same version twice", 30, TEAL, weight=BOLD).move_to([-3.2, -1.7, 0])
        lb = T("two versions", 30, "#A8E6EA", weight=BOLD).move_to([3.2, -1.7, 0])
        self.at("The other is heterozygosity")
        self.play(Indicate(bars[1][0], color=YELLOW), trk["h"].animate.set_value(0.35), run_time=1.2)
        self.at("the share of gene positions")
        self.play(FadeIn(head), run_time=0.8)
        self.play(FadeIn(A, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(B, shift=UP * 0.2), run_time=0.8)
        self.at("two different versions")
        self.play(FadeIn(la), run_time=0.7)
        self.play(FadeIn(lb), Indicate(B[1], color="#A8E6EA", scale_factor=1.1), run_time=1.0)
        self.finish()


def gauge_strip(trk):
    bars = VGroup()
    ros = []
    for key, y, lab, rt in (("c", 3.45, "head count", "about 3x"), ("h", 2.7, "heterozygosity", "2x")):
        l = T(lab, 28, YELLOW, weight=BOLD)
        l.move_to([-6.5 + l.width / 2, y, 0])
        box = Rectangle(width=6.6, height=0.45, stroke_color=TEXT, stroke_width=3).move_to([1.0, y, 0])

        def up(m, key=key, y=y):
            w = max(0.02, 6.6 * trk[key].get_value())
            m.become(Rectangle(width=w, height=0.45, stroke_width=0, fill_color=YELLOW, fill_opacity=0.8).move_to([-2.3 + w / 2, y, 0]))
        fill = Rectangle(width=1, height=0.45, stroke_width=0)
        fill.add_updater(up)
        up(fill)
        ro = T(rt, 30, YELLOW, weight=BOLD)
        ro.move_to([4.55 + ro.width / 2, y, 0])
        bars.add(VGroup(l, box, fill))
        ros.append(ro)
    return bars, ros


class S07Result(S):
    def construct(self):
        W = World(k=50, slope=-0.02)
        trk = {"c": ValueTracker(0.25), "h": ValueTracker(0.3)}
        bars, ros = gauge_strip(trk)
        self.add(bars, W.base, W.floor, W.flab, W.run, W.arrow)
        yr = T("1995", 28, YELLOW, weight=BOLD).move_to([W.P.X(50), W.P.y0 + W.P.h - 0.3, 0])
        mk = DashedLine([W.P.X(50), W.P.y0, 0], [W.P.X(50), W.P.y0 + W.P.h, 0], color=YELLOW, stroke_width=3, dash_length=0.12)
        cite = T("Johnson et al.,\nScience, 2010", 24, TEXT).move_to([5.2, 0.9, 0])
        self.play(Create(mk), FadeIn(yr), FadeIn(cite), run_time=1.0)
        self.at("Numbers had about tripled")
        self.play(trk["c"].animate.set_value(0.75), run_time=1.6, rate_func=smooth)
        self.play(FadeIn(ros[0]), run_time=0.4)
        self.at("Heterozygosity had doubled")
        self.play(trk["h"].animate.set_value(0.6), run_time=1.4, rate_func=smooth)
        self.play(FadeIn(ros[1]), run_time=0.4)
        self.at("Survival and fitness")
        sv = T("survival and\nfitness:\nimproved", 26, GREEN, weight=BOLD).move_to([5.2, -0.9, 0])
        self.play(FadeIn(sv), run_time=0.8)
        self.at("On the chart")
        self.play(FadeOut(mk), FadeOut(yr), run_time=0.4)
        self.play(W.k.animate.set_value(75), W.sl.animate.set_value(0.03), run_time=self.rest(0.4), rate_func=smooth)
        self.finish()


def shrink_patch(c, sc, tr):
    cen = np.array([c[0] + 0.15 * sc, c[1] - 0.55 * sc, 0])

    def mk():
        s = max(tr.get_value(), 0.05)
        return Ellipse(width=0.8 * sc * s, height=1.0 * sc * s, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.55).move_to(cen)
    p = mk()
    p.add_updater(lambda m: m.become(mk()))
    return p


def ripple(P, t=75, color=YELLOW, per=1.5):
    st = {"t": 0.0}
    c = Circle(radius=0.1, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([P.X(t), P.Y(PATH[t]), 0])

    def up(m, dt):
        st["t"] += dt
        f = (st["t"] % per) / per
        m.become(Circle(radius=0.15 + 1.7 * f, stroke_color=color, stroke_width=10, fill_opacity=0.12 * (1 - f), fill_color=color).set_stroke(opacity=1 - 0.8 * f).move_to([P.X(t), P.Y(PATH[t]), 0]))
    c.add_updater(up)
    return c


def qzone(P, zt):
    x0 = P.X(75)

    def mk():
        w = max(0.02, (P.X(100) - x0) * zt.get_value())
        g = VGroup(Rectangle(width=w, height=P.h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.16).move_to([x0 + w / 2, P.y0 + P.h / 2, 0]))
        if zt.get_value() > 0.5:
            g.add(T("?", 110, YELLOW, weight=BOLD).move_to([x0 + (P.X(100) - x0) / 2, P.y0 + P.h * 0.62, 0]))
        return g
    z = mk()
    z.add_updater(lambda m: m.become(mk()))
    return z


class S08Predict(S):
    def construct(self):
        W = World(k=75, slope=0.03, flab=False)
        fc = (5.25, 0.35)
        fl = outline(FL_PTS, 0.95, fc)
        tr = ValueTracker(1.0)
        pt = shrink_patch(fc, 0.95, tr)
        q = T("will the climb continue?", 38, YELLOW, weight=BOLD).move_to([-0.8, 3.3, 0])
        self.add(W.base, W.floor, W.run, W.arrow, fl, pt, ripple(W.P))
        self.at("habitat loss")
        hl = T("habitat loss", 30, TEAL, weight=BOLD).move_to([5.25, -1.9, 0])
        self.play(FadeIn(hl), run_time=0.6)
        self.play(tr.animate.set_value(0.65), run_time=self.to("persistent inbreeding"), rate_func=linear)
        self.at("persistent inbreeding")
        self.play(Indicate(hl, color=TEAL), tr.animate.set_value(0.5), run_time=self.to("will the climb"), rate_func=linear)
        self.at("will the climb")
        zt = ValueTracker(0.0)
        self.add(qzone(W.P, zt))
        self.play(FadeIn(q), tr.animate.set_value(0.3), zt.animate.set_value(1.0), run_time=self.rest(0.2), rate_func=linear)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        W = World(k=75, slope=0.03, flab=False)
        fc = (5.25, 0.35)
        fl = outline(FL_PTS, 0.95, fc)
        ptr = ValueTracker(0.3)
        pt = shrink_patch(fc, 0.95, ptr)
        hl = T("habitat loss", 30, TEAL, weight=BOLD).move_to([5.25, -1.9, 0])
        q = T("Predict: does the climb continue?", 38, YELLOW, weight=BOLD).move_to([-0.8, 3.3, 0])
        self.add(W.base, W.floor, W.run, W.arrow, fl, pt, hl, q, ripple(W.P))
        zt = ValueTracker(1.0)
        self.add(qzone(W.P, zt))
        tr = ValueTracker(5.0)
        cd = Live(lambda: str(max(1, int(np.ceil(tr.get_value())))), 64, YELLOW, True, [-0.8, 0.5, 0])
        self.add(cd)
        self.play(tr.animate.set_value(0.01), ptr.animate.set_value(0.1), run_time=4.4, rate_func=linear)
        self.finish()


class S10Reveal(S):
    def construct(self):
        cols = [gen_col(k) for k in range(6)]
        lab0 = T("admixed: both ancestries", 40, TEXT, weight=BOLD).move_to([0, -2.8, 0])
        self.add(*cols[:4], lab0)
        cite = T("Onorato et al., Scientific Reports, 2024", 26, TEXT).move_to([0, 3.5, 0])
        cnt = T("1,192 panthers", 38, YELLOW, weight=BOLD).move_to([0, 2.8, 0])
        self.at("In 2024")
        self.play(FadeIn(cite), run_time=0.8)
        self.at("records from")
        self.play(FadeIn(cnt, shift=UP * 0.2), run_time=1.0)
        self.play(Indicate(cnt, color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.at("The genetic benefits")
        newlab = T("benefits through five generations", 40, GOLD, weight=BOLD).move_to([0, -2.8, 0])
        self.play(FadeOut(lab0), FadeOut(cnt), run_time=0.5)
        self.play(FadeIn(cols[4], shift=RIGHT * 0.3), run_time=1.0)
        self.play(FadeIn(cols[5], shift=RIGHT * 0.3), run_time=1.0)
        self.at("five generations")
        cks = VGroup(*[check(0.5).move_to([GEN_X[k], 1.9, 0]) for k in range(1, 6)])
        self.play(FadeIn(newlab), LaggedStart(*[Create(c) for c in cks], lag_ratio=0.2), run_time=1.8)
        self.finish()


class S11Decline(S):
    def construct(self):
        W = World(k=75, slope=0.03)
        self.add(W.base, W.floor, W.flab, W.run, W.arrow)
        bx0, bx1 = W.P.X(80), W.P.X(100)
        band = Rectangle(width=bx1 - bx0, height=W.P.h, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to([(bx0 + bx1) / 2, W.P.y0 + W.P.h / 2, 0])
        bl = T("2016 to 2020:\nstabilised, then declined", 28, TEXT, weight=BOLD).move_to([-0.2, 1.45, 0])
        self.at("stabilized")
        self.play(FadeIn(band), run_time=0.8)
        self.at("then declined")
        self.play(W.k.animate.set_value(100), W.sl.animate.set_value(0.0), run_time=2.4, rate_func=linear)
        self.play(FadeIn(bl), run_time=0.8)
        self.at("The genetic benefits")
        gb = chip("genetic benefits persist", GREEN, 30).move_to([-1.8, 3.3, 0])
        ck = check(0.5).move_to(gb.get_right() + RIGHT * 0.5)
        self.play(FadeIn(gb), Create(ck), run_time=1.0)
        self.at("the climb stopped")
        self.play(Indicate(W.arrow, color=GOLD), run_time=1.0)
        self.at("A population gain")
        self.play(FadeOut(gb), FadeOut(ck), FadeOut(W.arrow), run_time=0.6)
        self.at("other causes")
        oc = chip("other causes of decline", RED, 30).move_to([-0.8, 3.3, 0])
        sc = T("schematic", 24, GREY).move_to([5.1, -2.6, 0])
        self.play(FadeIn(oc), FadeIn(sc), run_time=1.0)
        self.play(Indicate(oc, color=RED, scale_factor=1.06), run_time=1.4)
        self.finish()


class S12Method(S):
    def construct(self):
        def panel(x):
            return RoundedRectangle(corner_radius=0.2, width=6.0, height=4.4, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.07).move_to([x, -0.2, 0])
        pl, pr = panel(-3.4), panel(3.4)
        tl = T("admixed vs\nnon-admixed", 30, TEXT, weight=BOLD).move_to([-3.4, 3.15, 0])
        tr_ = T("after vs\nbefore", 30, TEXT, weight=BOLD).move_to([3.4, 3.15, 0])
        self.play(FadeIn(pl), FadeIn(pr), FadeIn(tl), FadeIn(tr_), run_time=1.0)
        ad = VGroup(*[puma(TEAL, 0.5, stripes=True).move_to([-5.2 + (i % 2) * 1.45, 0.7 - (i // 2) * 1.5, 0]) for i in range(4)])
        nt = VGroup(*[puma(TEAL, 0.5).move_to([-2.5 + (i % 2) * 1.45, 0.7 - (i // 2) * 1.5, 0]) for i in range(4)])
        self.at("They compared admixed")
        self.play(LaggedStart(*[FadeIn(p) for p in ad], lag_ratio=0.15), run_time=1.0)
        self.at("non admixed")
        self.play(LaggedStart(*[FadeIn(p) for p in nt], lag_ratio=0.15), run_time=1.0)
        self.at("and the years after")
        ty = -0.3
        bef = Rectangle(width=2.4, height=0.5, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.2).move_to([2.2, ty, 0])
        aft = Rectangle(width=2.4, height=0.5, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.75).move_to([4.6, ty, 0])
        mk = Line([3.4, ty - 0.7, 0], [3.4, ty + 0.7, 0], color=YELLOW, stroke_width=5)
        yr = T("1995", 30, YELLOW, weight=BOLD).move_to([3.4, ty - 1.15, 0])
        self.play(FadeIn(bef), FadeIn(aft), Create(mk), FadeIn(yr), run_time=0.8)
        lbl_a = T("after", 30, TEAL, weight=BOLD).move_to([4.6, ty + 0.85, 0])
        lbl_b = T("before", 30, TEAL, weight=BOLD).move_to([2.2, ty + 0.85, 0])
        self.play(FadeIn(lbl_a), run_time=0.5)
        self.at("with the years before")
        self.play(FadeIn(lbl_b), run_time=0.7)
        self.at("Both comparisons")
        one = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=13.0, height=5.3, stroke_color=YELLOW, stroke_width=4).move_to([0, -0.2, 0]), num_dashes=90)
        ol = T("one population", 30, YELLOW, weight=BOLD).move_to([0, -3.4, 0])
        self.play(Create(one), run_time=1.2)
        self.at("a single population")
        self.play(FadeIn(ol), run_time=0.7)
        self.play(Indicate(ol, color=YELLOW), run_time=1.0)
        self.finish()


class S13Rule(S):
    def construct(self):
        P = ZP(-6.2, -3.0, 7.4, 5.3, yticks=False)
        W = World(k=100, slope=0.0, P=P, flab=False)
        c1 = RoundedRectangle(corner_radius=0.2, width=4.9, height=2.0, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.08).move_to([4.3, 2.3, 0])
        t1 = T("1. Find and remove\nthe cause of decline", 24, GOLD, weight=BOLD).move_to(c1.get_center() + RIGHT * 0.6)
        c2 = RoundedRectangle(corner_radius=0.2, width=4.9, height=3.0, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.08).move_to([4.3, -1.5, 0])
        t2h = T("2. Alongside:", 26, TEXT, weight=BOLD)
        t2h.move_to([2.1 + t2h.width / 2, -0.55, 0])
        words = []
        for w_, y in (("numbers", -1.15), ("connections", -1.75), ("genes", -2.35)):
            t = T(w_, 28, TEAL, weight=BOLD)
            t.move_to([2.3 + t.width / 2, y, 0])
            words.append(t)
        self.add(W.base, W.floor, W.run, W.arrow)
        self.play(FadeIn(c1), FadeIn(t1), FadeIn(c2), FadeIn(t2h), FadeIn(VGroup(*words)), run_time=0.8)
        self.at("genetic rescue")
        gene = chip("gene", PURPLE, 28).move_to([3.0, 0.2, 0])
        self.play(FadeIn(gene), run_time=0.4)
        self.play(gene.animate.next_to(words[2], RIGHT, buff=0.5), run_time=1.2, rate_func=smooth)
        self.play(Indicate(words[2], color=PURPLE), W.sl.animate.set_value(0.015), run_time=1.4)
        self.at("But it does not")
        glow = c1.copy().set_stroke(RED, 6).set_fill(RED, 0.15)
        hp = Ellipse(width=0.9, height=1.2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.55).move_to([2.7, 2.3, 0])
        self.play(FadeIn(glow), FadeIn(hp, scale=0.5), run_time=1.0)
        self.at("habitat loss")
        self.play(hp.animate.scale(0.45), run_time=1.2)
        self.at("road deaths")
        rd = T("habitat loss, road deaths", 24, RED, weight=BOLD).move_to([4.3, 0.75, 0])
        self.play(FadeIn(rd), run_time=0.8)
        self.at("Address those")
        self.play(Indicate(c1, color=GOLD, scale_factor=1.04), run_time=1.2)
        self.at("or the gain may fade")
        self.play(W.sl.animate.set_value(-0.01), run_time=1.6, rate_func=smooth)
        self.at("Genes and habitat work together")
        self.play(W.sl.animate.set_value(0.02), Indicate(c2, color=TEAL, scale_factor=1.03), run_time=self.rest(0.4), rate_func=smooth)
        self.finish()


class S14End(EndCard):
    LINE = "Genes can lift the trend; other causes of decline must still go."
