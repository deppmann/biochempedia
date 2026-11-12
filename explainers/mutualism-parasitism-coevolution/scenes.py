"""The Net Decides the Sign: mutualism, parasitism and coevolution (chapter 1).

COLOUR MAP (same in both films)
  GREEN  = plant / host          PURPLE = fungus / parasite / partner
  GOLD   = rhizobia              TEAL   = benefit (and nitrogen, phosphorus)
  RED    = cost (and carbon)     GREY   = net bars and structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B07CE0"
PALEP = "#E7D6FF"
DULL = "#7d6f45"
SOIL = "#2a2118"
PINK = "#F28DB2"
SEED = "#D9B77A"
LIGHTG = "#B8C0CE"

# world layout shared by scenes 3 to 10 (plant panel left, balance centre, gauge right)
PBX, PBY, PS = -4.35, -0.5, 1.15
BCX, BPY = 1.3, 1.5
GX, GMID, GHH = 5.7, 0.5, 1.8


# ---------------------------------------------------------------- small helpers
def clip(v, a, b):
    return max(a, min(b, v))


def ambient_clock(sc):
    clk = ValueTracker(0)
    clk.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(clk)
    return clk


def pulse(m, amp=0.06, per=1.6):
    m._f = 1.0
    m._tt = 0.0

    def up(mm, dt):
        mm._tt += dt
        f = 1 + amp * np.sin(2 * np.pi * mm._tt / per)
        mm.scale(f / mm._f)
        mm._f = f
    m.add_updater(up)
    return m


def make_plant(bx, by, s=1.0, fungus=True, nodules=False):
    soil = Rectangle(width=3.8 * s, height=1.9 * s, stroke_width=0, fill_color=SOIL,
                     fill_opacity=0.75).move_to([bx, by - 0.95 * s, 0])
    ground = Line([bx - 1.9 * s, by, 0], [bx + 1.9 * s, by, 0], color=GREY, stroke_width=3)
    stem = Line([bx, by, 0], [bx, by + 2.0 * s, 0], color=GREEN, stroke_width=8)
    leaves = VGroup(*[
        Ellipse(width=1.0 * s, height=0.42 * s, fill_color=GREEN, fill_opacity=0.75,
                stroke_color=GREEN, stroke_width=3).rotate(a).move_to(p)
        for a, p in [(0.5, [bx - 0.5 * s, by + 1.75 * s, 0]), (-0.5, [bx + 0.5 * s, by + 1.45 * s, 0]),
                     (PI / 2, [bx, by + 2.3 * s, 0])]])
    roots = VGroup()
    base = np.array([bx, by, 0])
    for dx, dy in [(-1.45, -0.95), (-0.75, -1.65), (0.05, -1.75), (0.8, -1.55), (1.5, -0.9)]:
        e = base + np.array([dx * s, dy * s, 0])
        roots.add(CubicBezier(base, base + np.array([dx * 0.25 * s, -0.6 * s, 0]),
                              e + np.array([-0.3 * dx * s, 0.5 * s, 0]), e).set_stroke(GREEN, 5, opacity=0.95))
    threads = VGroup()
    if fungus:
        for k, rt in enumerate(roots):
            pts = []
            for u in np.linspace(0.1, 1.0, 36):
                p = rt.point_from_proportion(u)
                q = rt.point_from_proportion(min(1.0, u + 0.02)) - rt.point_from_proportion(max(0.0, u - 0.02))
                nrm = np.array([-q[1], q[0], 0.0]) / (np.linalg.norm(q) + 1e-6)
                pts.append(p + nrm * 0.1 * s * np.sin(9 * u + k))
            tip = pts[-1]
            d = pts[-1] - pts[-4]
            d = d / (np.linalg.norm(d) + 1e-6)
            for j in range(1, 7):
                pts.append(tip + d * 0.1 * s * j + np.array([0, 0.05 * s * np.sin(2.5 * j + k), 0]))
            threads.add(VMobject().set_points_smoothly(pts).set_stroke(PURPLE, 3.5))
    nods = VGroup()
    if nodules:
        for i in (0, 2, 4):
            nods.add(Circle(radius=0.2 * s, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                            fill_opacity=0.55).move_to(roots[i].point_from_proportion(0.62)))
    g = VGroup(soil, ground, stem, roots, threads, leaves, nods)
    g.soil, g.ground, g.stem, g.roots, g.threads, g.leaves, g.nods = soil, ground, stem, roots, threads, leaves, nods
    return g


def start_sway(pl, amp=0.05, per=3.2, ph=0.0):
    lv = pl.leaves
    lv._a = 0.0
    lv._tt = 0.0

    def up(m, dt):
        m._tt += dt
        a = amp * np.sin(2 * np.pi * m._tt / per + ph)
        m.rotate(a - m._a, about_point=pl.stem.get_end())
        m._a = a
    lv.add_updater(up)


def stream(path, color, n=4, speed=0.2, r=0.07, rev=False, ph=0.0):
    dots = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    for i, d in enumerate(dots):
        d._u = (i / n + ph) % 1.0

    def up(g, dt):
        for d in g:
            d._u = (d._u + (-1 if rev else 1) * speed * dt) % 1.0
            d.move_to(path.point_from_proportion(d._u))
    dots.add_updater(up)
    up(dots, 0)
    return dots


def pdots(bx, by, s, p, n=30, seed=3, spread=1.0):
    rng = np.random.RandomState(seed)
    g = VGroup(*[Dot(radius=0.075, color=TEAL) for _ in range(n)])
    for i, d in enumerate(g):
        d._h = np.array([bx + rng.uniform(-1.75, 1.75) * s * spread, by - rng.uniform(0.25, 1.8) * s, 0])
        d._ph = rng.uniform(0, 6.3)
        d._i = i
    g._tt = 0.0

    def up(m, dt):
        m._tt += dt
        for d in m:
            o = clip(p.get_value() * n - d._i, 0, 1)
            d.set_opacity(0.95 * o)
            d.move_to(d._h + 0.07 * np.array([np.sin(1.3 * m._tt + d._ph), np.cos(1.1 * m._tt + d._ph), 0]))
    g.add_updater(up)
    up(g, 0)
    return g


def counter(tr, nmax, pos, size=40, color=TEXT):
    g = VGroup(*[M(str(i), size, color).move_to(pos) for i in range(nmax + 1)])

    def up(m, dt=0):
        v = int(round(tr.get_value()))
        for i, t in enumerate(m):
            t.set_opacity(1 if i == v else 0)
    g.add_updater(up)
    up(g)
    return g


def heart(h=0.5, color=PINK):
    f = ParametricFunction(lambda t: np.array([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t)
                                               - 2 * np.cos(3 * t) - np.cos(4 * t), 0]),
                           t_range=[0, 2 * PI, 0.05])
    f.set_stroke(color, 3).set_fill(color, 0.9)
    f.set_height(h)
    return f


# ---------------------------------------------------------------- the balance
class Bal:
    def __init__(s, cx, py, L=2.3, h=1.35, tw=0.8, mx=1.0, mn=0.2, col=TEXT):
        s.cx, s.py, s.L, s.h, s.tw, s.mx, s.mn, s.col = cx, py, L, h, tw, mx, mn, col
        s.zb, s.zc, s.wb, s.wc, s.db, s.dc, s.th = [ValueTracker(0) for _ in range(7)]
        s.clock = ValueTracker(0)
        s.clock.add_updater(lambda m, dt: m.increment_value(dt))
        s.beam_m = always_redraw(s.beam)
        s.bk = [always_redraw(lambda i=i: s.block(i)) for i in (0, 1)]
        s.pivot = Dot([cx, py, 0], radius=0.13, color=GOLD)
        s.post = VGroup(Line([cx, py, 0], [cx, py - 3.0, 0], color=GREY, stroke_width=6),
                        Line([cx - 0.7, py - 3.0, 0], [cx + 0.7, py - 3.0, 0], color=GREY, stroke_width=8))
        s.labs = []

    def ang(s):
        base = clip((s.wb.get_value() - s.wc.get_value()) * 0.42, -0.34, 0.34)
        return base + s.th.get_value() + 0.014 * np.sin(1.8 * s.clock.get_value() + s.cx)

    def ends(s):
        a = s.ang()
        c, n = np.cos(a), np.sin(a)
        return (np.array([s.cx - s.L * c, s.py - s.L * n, 0.0]), np.array([s.cx + s.L * c, s.py + s.L * n, 0.0]))

    def tray(s, i):
        return s.ends()[i] + np.array([0, -s.h, 0.0])

    def beam(s):
        l, r = s.ends()
        g = VGroup(Line(l, r, color=s.col, stroke_width=8))
        for e in (l, r):
            t = e + np.array([0, -s.h, 0.0])
            a = t + np.array([-s.tw, 0, 0.0])
            b = t + np.array([s.tw, 0, 0.0])
            g.add(Line(e, a, color=s.col, stroke_width=3), Line(e, b, color=s.col, stroke_width=3),
                  Line(a, b, color=s.col, stroke_width=8))
        return g

    def block(s, i):
        z = (s.zb, s.zc)[i].get_value()
        d = (s.db, s.dc)[i].get_value()
        side = s.mn + z * (s.mx - s.mn)
        col = (TEAL, RED)[i]
        sq = Square(side, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.6)
        sq.move_to(s.tray(i) + np.array([0, side / 2 + 0.05 + d, 0]))
        return sq

    def label(s, i, text, size=30, color=None):
        col = color or (TEAL, RED)[i]
        t = T(text, size, col)
        t.add_updater(lambda m: m.move_to(s.tray(i) + np.array([0, -0.45, 0])))
        t.move_to(s.tray(i) + np.array([0, -0.45, 0]))
        return t

    def static(s):
        return VGroup(s.post, s.pivot)

    def net(s):
        return s.wb.get_value() - s.wc.get_value()

    def load(s, sc, b, c, labels=True, blocks=True):
        for tr, v in ((s.zb, b), (s.wb, b), (s.zc, c), (s.wc, c)):
            tr.set_value(v)
        sc.add(s.clock, s.post, s.pivot, s.beam_m)
        if blocks:
            sc.add(*s.bk)
        if labels:
            s.labs = [s.label(0, "benefit"), s.label(1, "cost")]
            sc.add(*s.labs)

    def drop_anim(s, sc, i, v, fall=0.7):
        z, d, w = (s.zb, s.zc)[i], (s.db, s.dc)[i], (s.wb, s.wc)[i]
        z.set_value(v)
        d.set_value(2.8)
        sc.add(s.bk[i])
        return Succession(d.animate(rate_func=rush_into, run_time=fall).set_value(0),
                          w.animate(rate_func=smooth, run_time=0.9).set_value(v))


class Gauge:
    def __init__(s, x, ymid, hh, getv, w=0.55, color=GREY, labels=True):
        s.x, s.ymid, s.hh, s.getv, s.w, s.color = x, ymid, hh, getv, w, color
        fr = VGroup(Rectangle(width=w, height=2 * hh, stroke_color=color, stroke_width=3, fill_opacity=0).move_to([x, ymid, 0]),
                    Line([x - w / 2 - 0.08, ymid, 0], [x + w / 2 + 0.08, ymid, 0], color=TEXT, stroke_width=3))
        if labels:
            for txt, yy in (("+", ymid + hh - 0.2), ("0", ymid), ("−", ymid - hh + 0.2)):
                fr.add(T(txt, 28, TEXT).move_to([x + w / 2 + 0.38, yy, 0]))
        s.frame = fr
        s.bar = always_redraw(s.mk)

    def mk(s):
        v = clip(s.getv(), -1, 1)
        h = max(abs(v) * s.hh, 0.004)
        r = Rectangle(width=s.w - 0.1, height=h, stroke_width=0, fill_color=s.color, fill_opacity=0.95)
        r.move_to([s.x, s.ymid + np.sign(v if v else 1) * h / 2, 0])
        return r

    def group(s):
        return VGroup(s.frame, s.bar)


class Slider:
    def __init__(s, x0, x1, y, p, rx):
        s.x0, s.x1, s.y, s.p = x0, x1, y, p
        s.line = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=6)
        s.knob = always_redraw(lambda: Dot([x0 + (x1 - x0) * p.get_value(), y, 0], radius=0.21, color=TEAL))
        s.reads = VGroup(*[T("soil phosphorus: " + w, 30, TEAL).move_to([rx, y + 0.6, 0]) for w in ("low", "medium", "high")])

        def up(m, dt=0):
            v = p.get_value()
            k = 0 if v < 0.34 else (1 if v < 0.67 else 2)
            for i, t in enumerate(m):
                t.set_opacity(1 if i == k else 0)
        s.reads.add_updater(up)
        up(s.reads)

    def group(s):
        return VGroup(s.line, s.knob, s.reads)


class World:
    """Plant panel + balance + gauge + slider, rebuilt in the same place each scene."""
    pass


def build_world(sc, b, c, p=None, plant=True, gauge=True, slider=False, labels=True, flows=False, sway=True):
    w = World()
    w.panel = panel()
    sc.add(w.panel)
    w.p = ValueTracker(0.1 if p is None else p)
    w.plant = make_plant(PBX, PBY, PS)
    w.bal = Bal(BCX, BPY)
    w.bal.load(sc, b, c, labels)
    if plant:
        sc.add(w.plant)
        if sway:
            start_sway(w.plant)
    w.gauge = Gauge(GX, GMID, GHH, w.bal.net)
    if gauge:
        sc.add(w.gauge.group())
    w.slider = Slider(0.3, 5.4, -3.2, w.p, 2.85)
    w.dots = pdots(PBX, PBY, PS, w.p)
    if slider:
        sc.add(w.slider.group(), w.dots)
    if flows:
        w.flows = VGroup(*[stream(r, PALEP, 2, 0.12, 0.05, ph=i * 0.17) for i, r in enumerate(w.plant.threads)])
        sc.add(w.flows)
    return w


def net_label(bal, x=4.4, y=3.3, size=34):
    pos = T("plant net: +", size, TEAL)
    neg = T("plant net: −", size, RED)
    g = VGroup(pos, neg).move_to([x, y, 0])
    pos.move_to([x, y, 0])
    neg.move_to([x, y, 0])

    def up(m, dt=0):
        v = bal.net()
        pos.set_opacity(1 if v >= 0 else 0)
        neg.set_opacity(0 if v >= 0 else 1)
    g.add_updater(up)
    up(g)
    return g


def panel(x=2.35, w=8.5, y=0.0, h=7.4):
    r = Rectangle(width=w, height=h, stroke_width=0, fill_color="#171d2a", fill_opacity=1).move_to([x, y, 0])
    r.set_z_index(-5)
    return r


def qmark(x, y):
    c = Circle(radius=0.75, stroke_color=YELLOW, stroke_width=4, fill_color=BG, fill_opacity=0.92)
    return VGroup(c, T("?", 100, YELLOW, weight=BOLD)).move_to([x, y, 0])


def schematic_tag():
    return T("schematic", 24, GREY).move_to([-5.6, 3.45, 0])


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "Mutualism, Parasitism and Coevolution"
    TITLE = "The Net Decides the Sign"


class S01Question(SpokenScene):
    def construct(self):
        p = make_plant(-3.0, -0.4, 1.4)
        self.play(FadeIn(p.soil), FadeIn(p.ground), Create(p.stem), FadeIn(p.leaves, scale=0.6), Create(p.roots),
                  run_time=1.0)
        start_sway(p)
        self.play(Create(p.threads), run_time=1.5)
        fl = VGroup(*[stream(t, PALEP, 3, 0.1, 0.05, ph=i * 0.2) for i, t in enumerate(p.threads)])
        self.add(fl)
        self.at("Is it a friend")
        q = T("?", 170, YELLOW, weight=BOLD).move_to([3.9, 0.7, 0])
        pulse(q)
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.at("friend")
        friend = T("friend?", 48, TEAL).move_to([3.9, 2.5, 0])
        self.play(FadeIn(friend, shift=DOWN * 0.2), q.animate.move_to([3.9, -1.5, 0]).scale(0.7), run_time=0.8)
        self.at("freeloader")
        free = T("freeloader?", 48, RED).move_to([3.9, 1.2, 0])
        self.play(FadeIn(free, shift=DOWN * 0.2), run_time=0.7)
        self.at("You cannot tell")
        self.play(ShowPassingFlash(p.threads.copy().set_stroke(YELLOW, 7), time_width=0.6), run_time=2.2)
        self.at("So how would you")
        self.play(q.animate.scale(1.5).move_to([3.9, -0.4, 0]), friend.animate.set_opacity(0.45),
                  free.animate.set_opacity(0.45), run_time=1.2)
        self.finish()


class S02Fitness(SpokenScene):
    def construct(self):
        big = make_plant(-3.0, -0.4, 1.4)
        self.add(big)
        start_sway(big)
        fl = VGroup(*[stream(t, PALEP, 3, 0.1, 0.05, ph=i * 0.2) for i, t in enumerate(big.threads)])
        self.add(fl)
        Lp = make_plant(-3.5, -0.5, 1.05)
        self.remove(fl)
        self.play(ReplacementTransform(big, Lp), run_time=1.1)
        start_sway(Lp)
        trL = ValueTracker(0)
        trR = ValueTracker(0)

        def stats(cx, tr, top):
            h = heart(0.5)
            pulse(h, 0.1, 1.0)
            r1 = VGroup(h, T("survival", 30, TEXT)).arrange(RIGHT, buff=0.25).move_to([cx, -2.9, 0])
            sd = Ellipse(width=0.36, height=0.22, fill_color=SEED, fill_opacity=1, stroke_color=SEED)
            cnt = counter(tr, top, [0, 0, 0], 40, YELLOW)
            lab = T("seeds", 30, TEXT)
            r2 = VGroup(sd, cnt, lab).arrange(RIGHT, buff=0.25)
            r2.move_to([cx, -3.5, 0])
            return VGroup(r1, r2), r1, r2

        sL, r1L, r2L = stats(-3.5, trL, 14)
        self.at("its survival")
        self.play(FadeIn(r1L, shift=UP * 0.2), run_time=0.7)
        self.at("reproduction")
        self.play(FadeIn(r2L), trL.animate(rate_func=linear).set_value(14), run_time=2.0)
        self.at("Then compare it")
        Rp = make_plant(-3.5, -0.5, 1.05, fungus=False)
        self.add(Rp)
        start_sway(Rp, ph=1.5)
        self.add(Rp)
        self.play(Rp.animate.shift(RIGHT * 7.0), run_time=1.6)
        sR, r1R, r2R = stats(3.5, trR, 14)
        self.at("same organism")
        lab = T("without the partner", 32, TEXT).move_to([3.5, 2.7, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.2), FadeIn(r1R), run_time=0.8)
        self.at("without the partner")
        self.play(FadeIn(r2R), trR.animate(rate_func=linear).set_value(9), run_time=1.8)
        self.at("The difference")
        br = VGroup(Line([-3.5, 3.3, 0], [-1.6, 3.3, 0], color=YELLOW, stroke_width=5),
                    Line([1.6, 3.3, 0], [3.5, 3.3, 0], color=YELLOW, stroke_width=5),
                    Line([-3.5, 3.3, 0], [-3.5, 3.05, 0], color=YELLOW, stroke_width=5),
                    Line([3.5, 3.3, 0], [3.5, 3.05, 0], color=YELLOW, stroke_width=5))
        self.play(Create(br), run_time=1.0)
        self.at("net effect")
        ne = T("net effect", 40, YELLOW).move_to([0, 3.3, 0])
        self.play(FadeIn(ne, shift=DOWN * 0.2), run_time=0.7)
        self.play(Indicate(r2L, color=YELLOW), Indicate(r2R, color=YELLOW), run_time=1.4)
        self.finish()


class S03Balance(SpokenScene):
    def construct(self):
        pl = make_plant(-3.5, -0.5, 1.05)
        self.add(pl)
        start_sway(pl)
        bal = Bal(BCX, BPY)
        self.add(bal.clock)
        pn = panel()
        self.play(pl.animate.scale(PS / 1.05).move_to(make_plant(PBX, PBY, PS).get_center()), FadeIn(pn), run_time=0.9)
        self.play(FadeIn(bal.post), FadeIn(bal.pivot), FadeIn(bal.beam_m, shift=DOWN * 0.8), run_time=1.2)
        self.at("the benefit")
        self.play(bal.drop_anim(self, 0, 0.8), run_time=1.6)
        lb = bal.label(0, "benefit")
        self.add(lb)
        self.play(FadeIn(lb), run_time=0.5)
        self.at("cost")
        self.play(bal.drop_anim(self, 1, 0.45), run_time=1.6)
        lc = bal.label(1, "cost")
        self.add(lc)
        self.play(FadeIn(lc), run_time=0.5)
        self.at("Benefit minus cost")
        g = Gauge(GX, GMID, GHH, bal.net)
        eq = T("net = benefit − cost", 40, TEXT).move_to([BCX, -3.0, 0])
        self.play(FadeIn(g.group()), Write(eq), run_time=1.4)
        self.play(Indicate(g.bar, color=YELLOW), run_time=1.2)
        self.finish()


class S04Signs(SpokenScene):
    def construct(self):
        w = build_world(self, 0.8, 0.45)
        eqt = T("net = benefit − cost", 40, TEXT).move_to([BCX, -3.0, 0])
        self.add(eqt)
        self.at("net names")
        self.play(Indicate(w.gauge.bar, color=YELLOW), run_time=1.2)
        self.at("interaction")
        self.wait(0.5)
        everything = Group(w.plant, w.bal.beam_m, *w.bal.bk, *w.bal.labs, w.bal.post, w.bal.pivot, w.gauge.group(), eqt,
                           w.panel)
        self.play(FadeOut(everything), run_time=0.9)

        def row(sign, name, y):
            ta, tb = ValueTracker(0), ValueTracker(0)
            ga = Gauge(-4.2, y, 1.0, ta.get_value, w=0.7, labels=False)
            gb = Gauge(-3.0, y, 1.0, tb.get_value, w=0.7, labels=False)
            sg = M(sign, 46, YELLOW).move_to([-1.8, y, 0], aligned_edge=LEFT)
            nm = T(name, 56, TEXT).move_to([0.8, y, 0], aligned_edge=LEFT)
            return ga, gb, sg, nm, ta, tb

        r1, r2, r3 = row("+, +", "mutualism", 2.3), row("+, 0", "commensalism", 0.0), row("+, −", "parasitism", -2.3)
        self.at("Both partners gain")
        self.play(FadeIn(r1[0].frame), FadeIn(r1[1].frame), FadeIn(r1[2]), run_time=0.3)
        self.add(r1[0].bar, r1[1].bar)
        self.play(r1[4].animate.set_value(0.7), r1[5].animate.set_value(0.7), run_time=0.8)
        self.at("mutualism")
        self.play(FadeIn(r1[3], shift=RIGHT * 0.3), run_time=0.6)
        self.play(Indicate(r1[3], color=YELLOW), run_time=0.9)
        self.at("One gains,")
        self.play(FadeIn(r2[0].frame), FadeIn(r2[1].frame), FadeIn(r2[2]), run_time=0.3)
        self.add(r2[0].bar, r2[1].bar)
        self.play(r2[4].animate.set_value(0.7), run_time=0.8)
        self.at("no net change")
        self.play(Indicate(r2[1].frame, color=YELLOW), run_time=0.9)
        self.at("commensalism")
        self.play(FadeIn(r2[3], shift=RIGHT * 0.3), run_time=0.6)
        self.play(Indicate(r2[3], color=YELLOW), run_time=0.8)
        self.at("One gains,", nth=1)
        self.play(FadeIn(r3[0].frame), FadeIn(r3[1].frame), FadeIn(r3[2]), run_time=0.3)
        self.add(r3[0].bar, r3[1].bar)
        self.play(r3[4].animate.set_value(0.7), run_time=0.5)
        self.at("loses")
        self.play(r3[5].animate.set_value(-0.7), run_time=0.9)
        self.at("parasitism")
        self.play(FadeIn(r3[3], shift=RIGHT * 0.3), run_time=0.6)
        self.play(Indicate(r3[3], color=YELLOW), run_time=1.0)
        self.finish()


class S05Fungus(SpokenScene):
    def construct(self):
        pl = make_plant(PBX, PBY, PS)
        pn = panel()
        bal = Bal(BCX, BPY)
        bal.load(self, 0, 0, labels=False, blocks=False)
        g = Gauge(GX, GMID, GHH, bal.net)
        self.add(pn, pl, g.group())
        start_sway(pl)
        flow = VGroup(*[stream(t, PALEP, 2, 0.12, 0.05, ph=i * 0.17) for i, t in enumerate(pl.threads)])
        self.add(flow)
        self.at("root fungus")
        self.play(ShowPassingFlash(pl.threads.copy().set_stroke(YELLOW, 7), time_width=0.6), run_time=1.4)
        self.at("takes carbon")
        cflow = VGroup(*[stream(r, RED, 3, 0.2, 0.09, ph=i * 0.11) for i, r in enumerate(pl.roots)])
        self.add(cflow)
        self.at("carbon")
        lc = T("carbon", 28, RED).move_to([PBX - 1.6, -3.15, 0])
        self.play(FadeIn(lc, shift=UP * 0.2), run_time=0.6)
        self.at("That is the cost")
        self.play(bal.drop_anim(self, 1, 0.3), run_time=1.6)
        cl = bal.label(1, "cost")
        self.add(cl)
        self.play(FadeIn(cl), run_time=0.5)
        self.at("soil nutrients")
        P = ValueTracker(0.55)
        d = pdots(PBX, PBY, PS, P, n=30, seed=5)
        self.play(FadeIn(d), run_time=0.9)
        self.at("phosphorus")
        lp = T("phosphorus", 28, TEAL).move_to([PBX + 1.0, -3.15, 0])
        pflow = VGroup(*[stream(t, TEAL, 3, 0.18, 0.09, ph=i * 0.13) for i, t in enumerate(pl.threads)])
        self.add(pflow)
        self.play(FadeIn(lp, shift=UP * 0.2), run_time=0.7)
        self.play(Indicate(lp, color=YELLOW), run_time=1.0)
        self.at("That is the benefit")
        self.play(bal.drop_anim(self, 0, 0.9), run_time=1.6)
        bl = bal.label(0, "benefit")
        self.add(bl)
        self.play(FadeIn(bl), run_time=0.5)
        self.finish()


class S06Poor(SpokenScene):
    def construct(self):
        w = build_world(self, 0.9, 0.3, p=0.1, slider=True, flows=True)
        tg = schematic_tag()
        self.add(tg)
        self.play(FadeIn(w.slider.group()), run_time=0.8)
        self.at("phosphorus starts scarce")
        self.play(Indicate(w.slider.reads, color=YELLOW), run_time=1.2)
        self.at("delivery")
        pf = VGroup(*[stream(t, TEAL, 3, 0.18, 0.09, ph=i * 0.13) for i, t in enumerate(w.plant.threads)])
        self.add(pf)
        self.play(Indicate(w.bal.bk[0], color=YELLOW, scale_factor=1.15), run_time=1.4)
        self.at("The benefit outweighs")
        self.play(Indicate(w.bal.bk[0], color=YELLOW, scale_factor=1.12), run_time=0.8)
        self.at("cost")
        self.play(Indicate(w.bal.bk[1], color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.at("plant's net")
        nl = net_label(w.bal)
        self.play(FadeIn(nl), Indicate(w.gauge.bar, color=YELLOW), run_time=1.4)
        self.finish()


def question_ring(cx, cy, tr):
    return always_redraw(lambda: Arc(radius=0.92, start_angle=PI / 2, angle=-2 * PI * max(tr.get_value(), 0.001),
                                     color=YELLOW, stroke_width=8).move_to([cx, cy, 0]))


def fixed_tag(bal):
    tag = VGroup(T("assumed fixed", 26, RED), T("(sketch)", 26, RED)).arrange(DOWN, buff=0.08)
    tag.add_updater(lambda m: m.move_to(bal.tray(1) + np.array([0, -1.2, 0])))
    tag.move_to(bal.tray(1) + np.array([0, -1.2, 0]))
    return tag


class S07Predict(SpokenScene):
    def construct(self):
        w = build_world(self, 0.9, 0.3, p=0.1, slider=True, flows=True)
        tg = schematic_tag()
        nl = net_label(w.bal)
        self.add(tg, nl)
        self.play(w.p.animate(rate_func=smooth).set_value(0.95), run_time=2.6)
        self.at("Suppose the carbon cost")
        tag = fixed_tag(w.bal)
        self.play(FadeIn(tag), Indicate(w.bal.bk[1], color=YELLOW, scale_factor=1.2), run_time=1.4)
        self.at("Where does")
        q = T("Where does the plant's net go?", 38, YELLOW).move_to([0.6, 3.3, 0])
        qm = qmark(GX + 0.05, GMID)
        self.play(FadeOut(nl), FadeIn(q, shift=DOWN * 0.2), FadeIn(qm, scale=0.6), run_time=1.0)
        pulse(qm, 0.05)
        self.play(Indicate(w.gauge.frame, color=YELLOW), run_time=1.0)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        w = build_world(self, 0.9, 0.3, p=0.95, slider=True, flows=True)
        self.add(schematic_tag(), fixed_tag(w.bal))
        q = T("Where does the plant's net go?", 38, YELLOW).move_to([0.6, 3.3, 0])
        qm = qmark(GX + 0.05, GMID)
        pulse(qm, 0.05)
        self.add(q, qm)
        tr = ValueTracker(0)
        ring = question_ring(GX + 0.05, GMID, tr)
        self.add(ring)
        self.play(tr.animate(rate_func=linear).set_value(1), run_time=self.beat(0.92))
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        w = build_world(self, 0.9, 0.3, p=0.95, slider=True, flows=True)
        self.add(schematic_tag(), fixed_tag(w.bal))
        q = T("Where does the plant's net go?", 38, YELLOW).move_to([0.6, 3.3, 0])
        qm = qmark(GX + 0.05, GMID)
        self.add(q, qm)
        nl = net_label(w.bal)
        nl.set_opacity(0)
        self.play(FadeOut(q), FadeOut(qm), run_time=0.3)
        self.add(nl)
        self.play(FadeIn(nl), run_time=0.2)
        b = w.bal
        self.play(b.zb.animate(rate_func=smooth).set_value(0.5), b.wb.animate(rate_func=smooth).set_value(0.5), run_time=1.0)
        self.at("because phosphorus")
        self.play(Indicate(w.dots, color=YELLOW, scale_factor=1.05), run_time=1.6)
        self.at("net slides")
        self.play(b.zb.animate(rate_func=smooth).set_value(0.1), b.wb.animate(rate_func=smooth).set_value(0.1), run_time=2.4)
        self.at("same fungus")
        self.play(Indicate(b.bk[1], color=YELLOW, scale_factor=1.25), Indicate(nl, color=RED), run_time=1.4)
        self.finish()


class S10Continuum(SpokenScene):
    def construct(self):
        w = build_world(self, 0.1, 0.3, p=0.95, slider=True, flows=True)
        tg = schematic_tag()
        nlb = net_label(w.bal)
        self.add(tg, nlb)
        self.at("fungus")
        fg = Gauge(4.75, GMID, GHH, lambda: 0.6, w=0.4, color=PURPLE, labels=False)
        cap = T("fungus still gains", 30, PURPLE).move_to([4.75, -1.65, 0])
        self.play(FadeIn(fg.group()), FadeIn(cap), run_time=0.8)
        self.play(Indicate(fg.bar, color=PURPLE), run_time=0.8)
        self.at("pair has moved")
        stuff = Group(w.plant, w.bal.beam_m, *w.bal.bk, *w.bal.labs, w.bal.post, w.bal.pivot, w.gauge.group(), fg.group(),
                      cap, w.dots, w.flows, nlb, tg, w.panel)
        self.play(FadeOut(stuff), w.p.animate(rate_func=smooth).set_value(0.05), run_time=1.0)
        X0, X1, BY = -4.6, 4.6, 0.9
        band = VGroup(*[Rectangle(width=(X1 - X0 + 0.8) / 3, height=0.6, stroke_width=0, fill_color=c, fill_opacity=0.6)
                        for c in (TEAL, GREY, RED)]).arrange(RIGHT, buff=0).move_to([0, BY, 0])
        ml = T("mutualism (+, +)", 34, TEAL).move_to([-3.6, BY + 0.9, 0])
        pl_ = T("parasitism (+, −)", 34, RED).move_to([3.6, BY + 0.9, 0])
        mk = VGroup(Circle(radius=0.4, stroke_color=GREEN, stroke_width=7, fill_opacity=0), Dot(radius=0.22, color=PURPLE))
        mk.add_updater(lambda m: m.move_to([X0 + (X1 - X0) * w.p.get_value(), BY, 0]))
        mk.move_to([X0 + (X1 - X0) * w.p.get_value(), BY, 0])
        mlab = T("the pair", 30, TEXT)
        mlab.add_updater(lambda m: m.move_to([clip(X0 + (X1 - X0) * w.p.get_value(), -5.4, 5.4), BY - 0.9, 0]))
        self.at("mutualism")
        self.play(FadeIn(band), FadeIn(ml, shift=DOWN * 0.2), FadeIn(mk), FadeIn(mlab), run_time=0.9)
        self.at("parasitism")
        self.play(FadeIn(pl_, shift=DOWN * 0.2), w.p.animate(rate_func=smooth).set_value(0.95), run_time=2.0)
        self.at("Ecologists call")
        title = T("mutualism−parasitism continuum", 42, YELLOW).move_to([0, 2.95, 0])
        self.play(Write(title), run_time=2.0)
        self.play(w.p.animate(rate_func=smooth).set_value(0.55), run_time=2.0)
        self.at("Where a pair sits")
        self.play(w.p.animate(rate_func=smooth).set_value(0.15), run_time=1.1)
        self.play(w.p.animate(rate_func=smooth).set_value(0.9), run_time=1.1)
        self.finish()


class S11Zero(SpokenScene):
    def construct(self):
        kw = dict(L=1.55, h=1.7, tw=0.75, mx=1.0, mn=0.2)
        L = Bal(-3.1, 2.1, **kw)
        R = Bal(3.1, 2.1, **kw)
        pls = Group(panel(-3.1, 6.3, 0.0, 6.6), panel(3.1, 6.3, 0.0, 6.6))
        self.add(pls)
        for bl in (L, R):
            bl.load(self, 0.05, 0.05, labels=True)
        gl = Gauge(-6.25, 0.8, 1.3, L.net, w=0.45, labels=False)
        gr = Gauge(6.25, 0.8, 1.3, R.net, w=0.45, labels=False)
        nl = T("net 0", 28, TEXT).move_to([-6.1, -1.0, 0])
        nr = T("net 0", 28, TEXT).move_to([6.1, -1.0, 0])
        self.add(gl.group(), gr.group(), nl, nr)
        self.at("A net of zero")
        self.play(Indicate(gl.frame, color=YELLOW), Indicate(gr.frame, color=YELLOW), run_time=1.4)
        self.at("A large benefit")
        self.play(R.zb.animate.set_value(1.0), R.wb.animate.set_value(1.0), run_time=1.0)
        self.at("large cost")
        self.play(R.zc.animate.set_value(1.0), R.wc.animate.set_value(1.0), run_time=0.8)
        self.at("can cancel")
        self.play(Indicate(gr.frame, color=YELLOW), run_time=1.2)
        self.at("A level balance")
        self.play(Indicate(L.bk[0], color=YELLOW), Indicate(L.bk[1], color=YELLOW), run_time=0.9)
        self.play(Indicate(R.bk[0], color=YELLOW, scale_factor=1.1), Indicate(R.bk[1], color=YELLOW, scale_factor=1.1),
                  run_time=1.0)
        lab = T("zero can hide large terms", 36, YELLOW).move_to([3.1, -3.2, 0])
        self.at("heavy loads")
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.8)
        self.finish()


# ---- rhizobia pictures
def rod_field(cx, cy, r, N, cnt, dull, size=0.46):
    g = VGroup()
    for i in range(N):
        ang = i * 2.39996
        rad = r * 0.8 * np.sqrt((i + 3) / (N + 3))
        rod = RoundedRectangle(corner_radius=0.07, width=size, height=size * 0.4, fill_color=GOLD, fill_opacity=0.85,
                               stroke_color=GOLD, stroke_width=2)
        rod._home = np.array([cx + rad * np.cos(ang), cy + rad * np.sin(ang), 0])
        rod._ph = i * 1.3
        rod._a = 0.0
        rod.move_to(rod._home)
        g.add(rod)
    g._tt = 0.0

    def up(m, dt):
        m._tt += dt
        t = m._tt
        col = interpolate_color(ManimColor(GOLD), ManimColor(DULL), dull.get_value())
        for i, rd in enumerate(m):
            rd.move_to(rd._home + 0.07 * np.array([np.cos(1.1 * t + rd._ph), np.sin(1.3 * t + rd._ph), 0]))
            a = 0.9 * i + 0.4 * np.sin(0.8 * t + rd._ph)
            rd.rotate(a - rd._a)
            rd._a = a
            o = clip(cnt.get_value() - i, 0, 1)
            rd.set_fill(col, opacity=0.85 * o)
            rd.set_stroke(col, opacity=o)
    g.add_updater(up)
    up(g, 0)
    return g


def nodule(cx, cy, r):
    return Circle(radius=r, stroke_color=GREEN, stroke_width=6, fill_color=GREEN, fill_opacity=0.22).move_to([cx, cy, 0])


A_C, A_R = (2.5, 1.3), 1.25
B_C, B_R = (2.6, -1.9), 1.15
LBX, LBY, LS = -4.4, 0.1, 1.15


def legume():
    return make_plant(LBX, LBY, LS, fungus=False, nodules=True)


def arrows_nc():
    nit = Arrow([1.05, 1.85, 0], [-3.1, 1.85, 0], color=TEAL, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.2)
    nlab = T("nitrogen", 34, TEAL).move_to([-1.0, 2.3, 0])
    car = Arrow([-4.0, 0.7, 0], [1.3, 0.7, 0], color=RED, stroke_width=8, buff=0, max_tip_length_to_length_ratio=0.2)
    clab = T("carbon", 34, RED).move_to([-0.8, 0.25, 0])
    return nit, nlab, car, clab


class S12Rhizobia(SpokenScene):
    def construct(self):
        pl = legume()
        self.play(FadeIn(pl.soil), FadeIn(pl.ground), Create(pl.stem), FadeIn(pl.leaves, scale=0.6), Create(pl.roots),
                  run_time=1.6)
        start_sway(pl)
        self.play(FadeIn(pl.nods, scale=0.4), run_time=0.9)
        self.at("Rhizobia are bacteria")
        cntA, dullA = ValueTracker(7), ValueTracker(0)
        cntB = ValueTracker(7)
        A = nodule(*A_C, A_R)
        rodsA = rod_field(*A_C, A_R, 18, cntA, dullA)
        self.play(TransformFromCopy(pl.nods[2], A), run_time=1.2)
        self.add(rodsA)
        lr = T("rhizobia", 38, GOLD).move_to([A_C[0], A_C[1] + A_R + 0.5, 0])
        self.play(FadeIn(rodsA), FadeIn(lr, shift=DOWN * 0.2), run_time=0.6)
        self.at("root nodules")
        B = nodule(*B_C, B_R)
        rodsB = rod_field(*B_C, B_R, 18, cntB, ValueTracker(0))
        ln = T("nodule", 36, GREEN).move_to([B_C[0], B_C[1] - B_R - 0.4, 0])
        self.play(FadeIn(B, scale=0.7), FadeIn(rodsB), FadeIn(ln, shift=UP * 0.2), run_time=0.9)
        self.at("small swellings")
        ln2 = T("nodule: swelling on the root", 32, GREEN).move_to([-2.4, -3.0, 0])
        self.play(Indicate(pl.nods, color=YELLOW, scale_factor=1.5), FadeIn(ln2, shift=UP * 0.2), run_time=1.6)
        self.at("They fix nitrogen")
        air = T("air", 34, GREY).move_to([A_C[0], 3.45, 0])
        ndots = VGroup(*[Dot(radius=0.08, color=TEAL) for _ in range(5)])
        for i, d in enumerate(ndots):
            d._u = i / 5
        top, bot = np.array([A_C[0], 3.15, 0]), np.array([A_C[0], A_C[1] + A_R * 0.6, 0])

        def upd(g, dt):
            for k, d in enumerate(g):
                d._u = (d._u + 0.25 * dt) % 1.0
                d.move_to(top + (bot - top) * d._u + np.array([0.25 * np.sin(6 * d._u + k), 0, 0]))
        ndots.add_updater(upd)
        self.add(ndots)
        self.play(FadeIn(air), FadeOut(lr), run_time=0.7)
        nit, nlab, car, clab = arrows_nc()
        self.at("nitrogen")
        self.play(GrowArrow(nit), FadeIn(nlab), run_time=1.0)
        self.at("take carbon")
        self.play(FadeOut(ln2), GrowArrow(car), FadeIn(clab), run_time=1.0)
        cd = stream(car, RED, 3, 0.2, 0.08)
        self.add(cd)
        self.finish()


class S13Cheat(SpokenScene):
    def construct(self):
        pl = legume()
        self.add(pl)
        start_sway(pl)
        cntA, dullA, cntB = ValueTracker(7), ValueTracker(0), ValueTracker(7)
        A = nodule(*A_C, A_R)
        rodsA = rod_field(*A_C, A_R, 18, cntA, dullA)
        B = nodule(*B_C, B_R)
        rodsB = rod_field(*B_C, B_R, 18, cntB, ValueTracker(0))
        nit, nlab, car, clab = arrows_nc()
        self.add(A, rodsA, B, rodsB, nit, nlab, car, clab, stream(car, RED, 3, 0.2, 0.08))
        self.at("takes carbon")
        self.play(Indicate(car, color=YELLOW), Indicate(clab, color=YELLOW), run_time=1.3)
        self.at("skips the fixing")
        tag = VGroup(T("N", 44, TEAL), Line([-0.35, -0.35, 0], [0.35, 0.35, 0], color=RED, stroke_width=7)).move_to(
            [A_C[0] + 1.55, A_C[1] + 0.9, 0])
        nf = T("non-fixer", 34, GOLD).move_to([A_C[0], A_C[1] - A_R - 0.4, 0])
        self.play(dullA.animate.set_value(1.0), FadeIn(tag), FadeIn(nf), nit.animate.set_opacity(0.0),
                  nlab.animate.set_opacity(0.0), run_time=1.6)
        self.at("more offspring")
        self.play(cntA.animate(rate_func=linear).set_value(14), cntB.animate(rate_func=linear).set_value(9), run_time=2.0)
        hon = T("honest", 34, GOLD).move_to([B_C[0], B_C[1] - B_R - 0.4, 0])
        self.at("and spread")
        self.play(FadeIn(hon), cntA.animate(rate_func=linear).set_value(18), run_time=1.4)
        self.at("What stops it")
        q = T("?", 150, YELLOW, weight=BOLD).move_to([5.6, 1.3, 0])
        pulse(q)
        self.play(FadeIn(q, scale=0.5), run_time=0.8)
        self.finish()


class S14Sanction(SpokenScene):
    def construct(self):
        cntA, dullA, cntB = ValueTracker(18), ValueTracker(1.0), ValueTracker(10)
        AC, BC, R_ = (-4.6, 1.2), (-4.6, -1.9), 1.1
        A = nodule(*AC, R_)
        B = nodule(*BC, R_)
        rodsA = rod_field(*AC, R_, 18, cntA, dullA, size=0.4)
        rodsB = rod_field(*BC, R_, 18, cntB, ValueTracker(0), size=0.4)
        tag = VGroup(T("N", 36, TEAL), Line([-0.3, -0.3, 0], [0.3, 0.3, 0], color=RED, stroke_width=6)).move_to(
            [AC[0] + 1.5, AC[1] + 0.75, 0])
        nf = T("non-fixer", 32, GOLD).move_to([AC[0], AC[1] + R_ + 0.4, 0])
        hon = T("honest", 32, GOLD).move_to([BC[0], BC[1] - R_ - 0.4, 0])
        self.add(A, B, rodsA, rodsB, tag, nf, hon)
        pn = panel()
        bal = Bal(BCX, BPY)
        bal.load(self, 0.0, 0.0, labels=False, blocks=False)
        self.remove(bal.beam_m, bal.post, bal.pivot)
        g = Gauge(GX, GMID, GHH, bal.net)
        self.add(pn)
        self.play(cntB.animate(rate_func=linear).set_value(12), Indicate(nf, color=YELLOW), run_time=1.3)
        self.at("sanction")
        self.add(bal.post, bal.pivot)
        self.play(FadeIn(bal.beam_m), FadeIn(g.group()), run_time=0.5)
        self.play(bal.drop_anim(self, 0, 0.7), run_time=1.1)
        bl = bal.label(0, "benefit")
        self.add(bl)
        self.at("reproduction")
        sl = bal.label(1, "host sanction", 30, RED)
        self.add(sl)
        self.play(bal.drop_anim(self, 1, 0.9), FadeIn(sl),
                  cntA.animate(rate_func=smooth).set_value(5), cntB.animate(rate_func=linear).set_value(16), run_time=3.2)
        self.at("That puts a new weight")
        self.play(Indicate(bal.bk[1], color=YELLOW, scale_factor=1.2), Indicate(g.bar, color=YELLOW), run_time=1.6)
        self.at("cheater's cost side")
        self.play(cntB.animate(rate_func=linear).set_value(18), Indicate(sl, color=YELLOW), run_time=1.8)
        self.finish()


class S15Coevo(SpokenScene):
    def construct(self):
        kw = dict(L=1.8, h=1.4, tw=0.8, mx=0.9, mn=0.2)
        H = Bal(-3.3, 1.0, col=GREEN, **kw)
        P = Bal(3.3, 1.0, col=PURPLE, **kw)
        self.add(panel(0, 13.2, 0.0, 7.4))
        H.load(self, 0.45, 0.45, labels=False)
        P.load(self, 0.45, 0.45, labels=False)
        rod = always_redraw(lambda: Line(H.ends()[1], P.ends()[0], color=GOLD, stroke_width=9))
        lh = T("host", 44, GREEN).move_to([-3.3, 3.2, 0])
        lp = T("partner", 44, PURPLE).move_to([3.3, 3.2, 0])
        self.at("partners")
        self.play(FadeIn(rod), FadeIn(lh), FadeIn(lp), run_time=1.0)
        self.at("A change in one")
        self.play(P.zb.animate.set_value(0.9), P.wb.animate.set_value(0.9), run_time=1.5)
        self.at("shifts")
        self.play(H.th.animate(rate_func=smooth).set_value(-0.2), run_time=1.4)
        self.at("selection")
        sel = T("selection changes", 34, YELLOW).move_to([-3.3, -2.7, 0])
        self.play(FadeIn(sel, shift=UP * 0.2), Indicate(H.bk[0], color=YELLOW), run_time=1.3)
        self.at("If the other then evolves")
        self.play(H.zb.animate.set_value(0.9), H.wb.animate.set_value(0.9), H.th.animate.set_value(0.0), run_time=1.6)
        self.play(P.th.animate(rate_func=smooth).set_value(-0.14), FadeOut(sel), run_time=1.2)
        self.at("coevolution")
        co = T("reciprocal change = coevolution", 40, YELLOW).move_to([0, -3.3, 0])
        self.play(FadeIn(co, shift=UP * 0.2), run_time=0.9)
        self.play(P.th.animate(rate_func=smooth).set_value(0.0), H.th.animate(rate_func=smooth).set_value(-0.1), run_time=1.4)
        self.finish()


def moth_shape(color=TEAL, tongue=1.8):
    wings = VGroup(*[Ellipse(width=1.3, height=1.8, color=color, fill_opacity=0.25, stroke_width=4)
                     .rotate(a).move_to([x, 0.7, 0]) for a, x in [(-0.5, -0.7), (0.5, 0.7)]])
    body = Ellipse(width=0.4, height=1.5, color=color, fill_opacity=0.85)
    tg = Line([0, -0.75, 0], [0, -0.75 - tongue, 0], color=color, stroke_width=6)
    return VGroup(wings, body, tg)


def flower_shape(depth=1.6, color=BLUE):
    cup = VMobject(color=color, stroke_width=7).set_points_as_corners(
        [[-0.9, 0.9, 0], [-0.4, -depth, 0], [0.4, -depth, 0], [0.9, 0.9, 0]])
    stem = Line([0, -depth, 0], [0, -depth - 1.2, 0], color=color, stroke_width=7)
    return VGroup(cup, stem)


class S16Janzen(SpokenScene):
    def construct(self):
        nm = T("Daniel Janzen, Evolution, 1980", 40, TEXT, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.play(Write(nm), run_time=1.6)
        self.at("set the standard")
        fl = flower_shape().move_to([2.6, -1.0, 0])
        mo = moth_shape(tongue=1.6).scale(0.8).move_to([2.6, 1.05, 0])
        self.play(FadeIn(fl), FadeIn(mo, shift=DOWN * 0.5), run_time=1.2)
        mo._tt = 0.0

        def hover(m, dt):
            m._tt += dt
            m.shift(UP * 0.15 * dt * np.cos(2.2 * m._tt))
        mo.add_updater(hover)
        self.at("good fit")
        tick = VGroup(Line([-0.35, 0, 0], [-0.1, -0.3, 0], color=GREEN, stroke_width=9),
                      Line([-0.1, -0.3, 0], [0.5, 0.45, 0], color=GREEN, stroke_width=9))
        tl = T("good fit", 40, GREEN)
        fit_g = VGroup(tick, tl).arrange(RIGHT, buff=0.3).move_to([-3.4, 0.2, 0])
        self.play(FadeIn(fit_g, shift=RIGHT * 0.3), run_time=0.8)
        self.at("not the evidence")
        cross = VGroup(Line([-1, 0.55, 0], [1, -0.55, 0], color=RED, stroke_width=9),
                       Line([-1, -0.55, 0], [1, 0.55, 0], color=RED, stroke_width=9)).move_to(fit_g)
        self.play(Create(cross), run_time=0.9)
        self.play(Indicate(fit_g, color=RED), run_time=1.2)
        self.at("Change in both partners")
        self.play(FadeOut(fit_g), FadeOut(cross), run_time=0.5)
        l1 = T("change in partner 1", 32, TEAL).move_to([-4.0, 1.5, 0])
        l2 = T("response in partner 2", 32, BLUE).move_to([-3.9, -1.3, 0])
        a1 = Arrow([-1.5, 1.5, 0], [1.0, 1.5, 0], color=TEAL, stroke_width=8, buff=0.05)
        a2 = Arrow([-1.5, -1.3, 0], [1.0, -1.3, 0], color=BLUE, stroke_width=8, buff=0.05)
        self.play(FadeIn(l1), GrowArrow(a1), run_time=0.9)
        self.play(FadeIn(l2), GrowArrow(a2), run_time=0.9)
        self.play(Indicate(a1, color=YELLOW), Indicate(a2, color=YELLOW), run_time=1.4)
        self.finish()


class S17Take(SpokenScene):
    def construct(self):
        self.add(panel(0, 13.2, 0.0, 7.4))
        bal = Bal(-0.8, 1.2, L=2.5, h=1.3, tw=0.8)
        p = ValueTracker(0.1)
        bal.load(self, 0.9, 0.3, labels=True)

        def follow(m, dt=0):
            v = 0.95 - 0.9 * p.get_value()
            for tr in (bal.zb, bal.wb):
                tr.set_value(v)
        drv = ValueTracker(0)
        drv.add_updater(follow)
        self.add(drv)
        sl = Slider(0.8, 6.0, 3.25, p, -3.7)
        for t in sl.reads:
            t.move_to([-3.4, 3.25, 0])
        grp = sl.group()
        grp.set_opacity(0.35)
        self.add(grp)
        pg = Gauge(4.4, 0.3, 1.5, bal.net, w=0.5, labels=False)
        fg = Gauge(5.6, 0.3, 1.5, lambda: 0.6, w=0.5, color=PURPLE, labels=True)
        pl_l = T("plant", 28, GREEN).move_to([4.4, -1.8, 0])
        fl_l = T("fungus", 28, PURPLE).move_to([5.7, -1.8, 0])
        self.play(p.animate(rate_func=linear).set_value(0.55), run_time=4.4)
        self.at("Each partner's side")
        self.play(FadeIn(pg.group()), FadeIn(fg.group()), FadeIn(pl_l), FadeIn(fl_l), run_time=1.0)
        self.play(Indicate(pg.frame, color=YELLOW), Indicate(fg.frame, color=PURPLE), run_time=1.0)
        self.at("measured against")
        t1 = T("each partner's net = benefit − cost,", 32, YELLOW)
        t2 = T("against life without the partner", 32, YELLOW)
        tt = VGroup(t1, t2).arrange(DOWN, buff=0.15).move_to([-0.8, -3.05, 0])
        self.play(Write(tt), run_time=2.4)
        self.at("Conditions can move it")
        self.play(grp.animate.set_opacity(1.0), run_time=0.6)
        self.play(p.animate(rate_func=smooth).set_value(0.95), run_time=1.6)
        self.play(p.animate(rate_func=smooth).set_value(0.3), run_time=1.4)
        self.finish()


class S18End(EndCard):
    LINE = "Each partner's net: benefit minus cost, against life without the partner."
