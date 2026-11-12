"""A Region Outlasts Its Ponds (Levins metapopulation model)

COLOUR MAP: occupied pond TEAL, empty pond GREY, colonization / gains GOLD, extinction / losses RED,
white dot = equilibrium p*, symbols p, c, e. All curves computed from  gains = c p (1-p), losses = e p.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

C0, E0 = 0.4, 0.1
BROWN = "#C49A6C"
FROG = "#9BD16B"
WHITE = "#FFFFFF"
RANK = np.random.RandomState(2).permutation(20)
_R = np.random.RandomState(5)
POS = []
for _j in range(4):
    for _i in range(5):
        POS.append((-4.4 + 2.2 * _i + _R.uniform(-0.4, 0.4), -1.75 + 1.17 * _j + _R.uniform(-0.14, 0.14)))

BIG = (1.0, (0.0, -0.5))
MID = (0.7, (-2.4, -0.3))
MINI = (0.36, (-4.3, 2.0))
LX = -4.3   # left panel x


class Pond(VGroup):
    def __init__(self, pos, occ, phase):
        self.body = Ellipse(width=1.2, height=0.84, stroke_width=3)
        self.rip = Ellipse(width=1.2, height=0.84, stroke_width=2)
        super().__init__(self.rip, self.body)
        self.occ = occ
        self.ph = phase
        self.t = 0.0
        self.move_to([pos[0], pos[1], 0])
        self.set_z_index(2)
        self.add_updater(lambda m, dt: m.paint(dt))
        self.paint(0)

    def paint(self, dt=0.0):
        self.t += dt
        o = float(self.occ)
        col = interpolate_color(ManimColor(GREY), ManimColor(TEAL), o)
        self.body.set_stroke(color=col, width=3, opacity=1)
        self.body.set_fill(col, opacity=0.12 + 0.5 * o + 0.06 * o * math.sin(self.t * 1.6 + self.ph * 6))
        ph = (self.t * 0.3 + self.ph) % 1.0
        w, h = self.body.width, self.body.height
        self.rip.stretch_to_fit_width(w * (1 + 0.5 * ph))
        self.rip.stretch_to_fit_height(h * (1 + 0.5 * ph))
        self.rip.move_to(self.body.get_center())
        self.rip.set_stroke(color=TEAL, width=2, opacity=o * 0.55 * (1 - ph))
        self.rip.set_fill(opacity=0)


class MapW(VGroup):
    def __init__(self, n_occ=15, field_color=GREY, field_op=0.20):
        self.field = RoundedRectangle(corner_radius=0.3, width=12.6, height=5.9, stroke_width=0,
                                      fill_color=field_color, fill_opacity=field_op)
        self.field.set_z_index(0)
        self.ponds = [Pond(POS[i], 1.0 if RANK[i] < n_occ else 0.0, i * 0.137) for i in range(20)]
        super().__init__(self.field, *self.ponds)


def place(mp, scale, center):
    mp.scale(scale).move_to([center[0], center[1], 0])
    return mp


def new_map(layout=BIG, n_occ=15, **kw):
    mp = MapW(n_occ, **kw)
    return place(mp, *layout)


class Occ(Animation):
    def __init__(self, pond, target, **kw):
        kw.setdefault("suspend_mobject_updating", False)
        super().__init__(pond, **kw)
        self.tg = target

    def begin(self):
        self.s0 = self.mobject.occ
        super().begin()

    def interpolate_mobject(self, alpha):
        self.mobject.occ = self.s0 + (self.tg - self.s0) * alpha


def drive(mp, tr):
    def f(m):
        n = 20 * tr.get_value()
        for i, p in enumerate(m.ponds):
            p.occ = float(np.clip(n - RANK[i], 0, 1))
    mp.add_updater(f)
    f(mp)


def manual(mp):
    mp.clear_updaters()


def xmark(pos, s):
    return VGroup(Line(pos + s * np.array([-1, -1, 0]), pos + s * np.array([1, 1, 0])),
                  Line(pos + s * np.array([-1, 1, 0]), pos + s * np.array([1, -1, 0]))).set_stroke(RED, 5).set_z_index(5)


def make_ticks(mp):
    g = VGroup()
    g.vis = ValueTracker(0)
    for i, p in enumerate(mp.ponds):
        t = xmark(ORIGIN, p.body.width * 0.12)
        t.idx = i
        g.add(t)

    def f(m):
        for t in m:
            p = mp.ponds[t.idx]
            t.move_to(p.body.get_center() + UP * p.body.height * 0.05)
            on = (RANK[t.idx] % 2 == 0)
            t.set_stroke(opacity=(p.occ if on else 0) * m.vis.get_value())
    g.add_updater(f)
    f(g)
    return g


def frog(pos, s=1.0, ph=0.0):
    b = Ellipse(width=0.34 * s, height=0.22 * s, fill_color=FROG, fill_opacity=1, stroke_width=0)
    e1 = Dot(radius=0.05 * s, color=TEXT).shift(LEFT * 0.08 * s + UP * 0.1 * s)
    e2 = Dot(radius=0.05 * s, color=TEXT).shift(RIGHT * 0.08 * s + UP * 0.1 * s)
    g = VGroup(b, e1, e2).move_to(pos)
    g.t = ph
    g.off = 0.0

    def hop(m, dt):
        m.t += dt
        o = 0.09 * s * abs(math.sin(m.t * 3.0 + ph * 5))
        m.shift(UP * (o - m.off))
        m.off = o
    g.add_updater(hop)
    return g


def clock(center, r, tr):
    face = Circle(radius=r, color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(center)
    hand = Line(center, center + UP * r * 0.8, color=YELLOW, stroke_width=5)
    hub = Dot(center, radius=0.05, color=TEXT)

    def f(m):
        a = -tr.get_value() * 2 * PI
        m.put_start_and_end_on(center, center + r * 0.8 * np.array([math.sin(a), math.cos(a), 0]))
    hand.add_updater(f)
    return VGroup(face, hand, hub)


def lab(text, size=30, color=TEXT, **kw):
    return T(text, size=size, color=color, **kw)


def left(text, y, color=TEXT, size=28, mono=False):
    m = (M if mono else T)(text, size=size, color=color)
    return m.move_to([LX, y, 0])


# ------------------------------------------------------------------ graph
class Graph:
    def __init__(self, c=C0, e=E0, dg=1.0, dr=1.0, p=0.75, dashed_gold=False):
        self.c, self.e, self.dg, self.dr, self.p = [ValueTracker(v) for v in (c, e, dg, dr, p)]
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 0.12, 0.04], x_length=7.0, y_length=5.3,
                  axis_config={"color": GREY, "include_tip": False, "include_ticks": False, "stroke_width": 3})
        ax.move_to([2.55, -0.1, 0])
        self.ax = ax
        labs = VGroup()
        for v, s in ((0, "0"), (0.5, "0.5"), (1, "1")):
            labs.add(M(s, 24, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.3))
        for v, s in ((0.05, "0.05"), (0.1, "0.10")):
            labs.add(M(s, 24, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.12))
        labs.add(T("p, fraction occupied", 28, TEXT).move_to([2.55, -3.55, 0]))
        labs.add(T("fraction of ponds per year", 26, TEXT).move_to([ax.c2p(0, 0.12)[0] + 2.2, 2.98, 0]))
        self.labels = labs
        YM = 0.103

        def gold():
            d = self.dg.get_value()
            if d < 0.02:
                return VMobject()
            c = self.c.get_value()
            return ax.plot(lambda x: c * x * (1 - x), x_range=[0, d, 0.01], color=GOLD, stroke_width=7)

        def red():
            d = self.dr.get_value()
            e = max(self.e.get_value(), 1e-3)
            xm = min(d, YM / e)
            if xm < 0.02:
                return VMobject()
            return ax.plot(lambda x: e * x, x_range=[0, xm, 0.01], color=RED, stroke_width=7)

        if dashed_gold:
            self.gold = DashedVMobject(ax.plot(lambda x: c * x * (1 - x), x_range=[0, 1, 0.01], color=GOLD, stroke_width=7), num_dashes=40)
        else:
            self.gold = always_redraw(gold)
        self.red = always_redraw(red)
        self.pdot = always_redraw(lambda: Dot(ax.c2p(self.p.get_value(), 0), radius=0.15, color=TEAL).set_z_index(6))

        def cross():
            c, e = self.c.get_value(), self.e.get_value()
            ps = max(0.0, 1 - e / c)
            d = Dot(ax.c2p(ps, e * ps), radius=0.16, color=WHITE).set_z_index(7)
            d.set_opacity(min(1.0, ps / 0.05))
            return d
        self.cross = always_redraw(cross)
        self.loss_lab = T("losses = e p", 28, RED).move_to([5.6, 2.15, 0])
        self.gain_lab = M("gains = c p (1 − p)", 26, GOLD).move_to([2.0, 2.3, 0])
        self.panel = RoundedRectangle(corner_radius=0.25, width=8.6, height=7.0, stroke_width=0, fill_color=GREY, fill_opacity=0.2).move_to([2.45, -0.3, 0]).set_z_index(-5)
        self.rate_lab = None

    def pc(self, p, y=None):
        return self.ax.c2p(p, y if y is not None else 0)

    def add_base(self, sc, gold=True, red=True, loss_lab=True, gain_lab=False):
        sc.add(self.panel, self.ax, self.labels)
        if gold:
            sc.add(self.gold)
        if red:
            sc.add(self.red)
        if loss_lab:
            sc.add(self.loss_lab)
        if gain_lab:
            sc.add(self.gain_lab)


def sweep(sc, gr, a, b, rt, draw_gold=False, draw_red=False):
    anims = [gr.p.animate(rate_func=linear).set_value(b)]
    if draw_gold:
        anims.append(gr.dg.animate(rate_func=linear).set_value(b))
    if draw_red:
        anims.append(gr.dr.animate(rate_func=linear).set_value(b))
    sc.play(*anims, run_time=rt)


# ------------------------------------------------------------------ colonize / wink
def arrow(a, b, s):
    return Arrow(a, b, color=GOLD, buff=0.32 * s, stroke_width=5, max_tip_length_to_length_ratio=0.3).set_z_index(5)


def step(sc, mp, out, inn, src, rt, mask=None):
    s = mp.ponds[0].body.width / 1.2
    ticks = [xmark(mp.ponds[i].get_center(), 0.15 * s + 0.06) for i in out]
    arrows = [arrow(mp.ponds[a].get_center(), mp.ponds[b].get_center(), s) for a, b in zip(src, inn)]
    A = [Occ(mp.ponds[i], 0.0) for i in out] + [FadeIn(t) for t in ticks] + [GrowArrow(a) for a in arrows]
    if A:
        sc.play(*A, run_time=rt * 0.55)
    B = [Occ(mp.ponds[j], 1.0) for j in inn] + [FadeOut(x) for x in ticks + arrows]
    if B:
        sc.play(*B, run_time=rt * 0.45)
    if mask is not None:
        for i in out:
            mask[i] = 0
        for j in inn:
            mask[j] = 1


def wink(sc, mp, mask, rng, k=1, rt=1.0):
    occ = [i for i in range(20) if mask[i]]
    emp = [i for i in range(20) if not mask[i]]
    k = min(k, len(occ) - 1, len(emp))
    out = [int(x) for x in rng.choice(occ, k, replace=False)]
    inn = [int(x) for x in rng.choice(emp, k, replace=False)]
    keep = [o for o in occ if o not in out]
    src = [int(rng.choice(keep)) for _ in inn]
    step(sc, mp, out, inn, src, rt, mask)


def mask_of(n=15):
    return [1 if RANK[i] < n else 0 for i in range(20)]


def find_sim():
    for seed in range(5000):
        r = np.random.RandomState(seed)
        mask = mask_of(15)
        log, cnt = [], [15]
        ok = True
        for y in range(16):
            p = sum(mask) / 20
            out = [i for i in range(20) if mask[i] and r.rand() < 0.1]
            inn = [i for i in range(20) if not mask[i] and r.rand() < 0.4 * p]
            keep = [i for i in range(20) if mask[i] and i not in out]
            if not keep:
                ok = False
                break
            src = [int(r.choice(keep)) for _ in inn]
            for i in out:
                mask[i] = 0
            for j in inn:
                mask[j] = 1
            n = sum(mask)
            if n < 12 or n > 18 or (y < 12 and not (out or inn)):
                ok = False
                break
            log.append((out, inn, src))
            cnt.append(n)
        if ok and any(l[0] for l in log[:6]) and sum(1 for l in log if l[0]) >= 9 and 14 <= cnt[12] <= 16:
            return log, cnt
    raise RuntimeError("no sim")


SIM, CNT = find_sim()


def add_motes(sc, seed):
    import random
    rng = random.Random(seed)
    W, H = config.frame_width, config.frame_height
    g = VGroup()
    for _ in range(34):
        d = Dot(radius=rng.uniform(0.05, 0.11), color=rng.choice([TEAL, GOLD, TEXT])).set_opacity(rng.uniform(0.30, 0.55))
        d.move_to([rng.uniform(-W / 2, W / 2), rng.uniform(-H / 2, H / 2), 0])
        d.v = (rng.uniform(-0.45, 0.45), rng.uniform(-0.35, 0.35))

        def drift(m, dt, W=W, H=H):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if abs(m.get_x()) > W / 2 + 0.1:
                m.shift(LEFT * (W + 0.2) * (1 if m.get_x() > 0 else -1))
            if abs(m.get_y()) > H / 2 + 0.1:
                m.shift(DOWN * (H + 0.2) * (1 if m.get_y() > 0 else -1))
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-1)
    sc.add(g)


class Sc(SpokenScene):
    def setup(self):
        super().setup()
        add_motes(self, type(self).__name__)


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Movement and Spatial Populations"
    TITLE = "A Region Outlasts Its Ponds"

    def construct(self):
        mp = new_map(BIG)
        veil = Rectangle(width=14.3, height=8.1, stroke_width=0, fill_color=BG, fill_opacity=0.62).set_z_index(10)
        self.add(mp, veil)
        super().construct()


class S01Question(Sc):
    def construct(self):
        mp = new_map(BIG)
        self.play(FadeIn(mp, scale=1.05), run_time=1.2)
        hi = next(i for i in (7, 8, 6, 12, 11, 13) if RANK[i] < 15)
        pond = mp.ponds[hi]
        c = pond.get_center()
        self.at("each pond's")
        self.play(Circumscribe(pond, color=WHITE, run_time=1.0))
        tr = ValueTracker(0)
        ck = clock(c + UP * 0.95, 0.38, tr)
        self.at("frogs last")
        self.play(FadeIn(ck), run_time=0.4)
        self.play(tr.animate(rate_func=linear).set_value(1.0), run_time=max(1.0, self.t_of("decade") - self.elapsed() + 0.1))
        yrs = lab("~10 years", 32, TEXT).next_to(ck, RIGHT, buff=0.2)
        bg = SurroundingRectangle(yrs, color=BG, fill_color=BG, fill_opacity=0.9, stroke_width=0, buff=0.08)
        tick = xmark(c, 0.2)
        self.play(FadeIn(bg), FadeIn(yrs), Occ(pond, 0.0), FadeIn(tick), run_time=0.9)
        tr2 = ValueTracker(0)
        big = clock(np.array([-1.7, 3.1, 0]), 0.6, tr2)
        y100 = lab("100 years", 40, TEXT).next_to(big, RIGHT, buff=0.3)
        self.at("so why can")
        self.play(FadeOut(VGroup(ck, yrs, bg)), FadeIn(big), FadeIn(y100), FadeOut(tick), run_time=0.9)
        self.play(tr2.animate(rate_func=linear).set_value(2.0), run_time=max(1.0, self.t_of("later") - self.elapsed()))
        q = lab("?", 90, YELLOW, weight=BOLD).move_to([3.4, 3.1, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.5)
        self.play(tr2.animate(rate_func=linear).set_value(3.5), run_time=3.0)
        self.finish()


class S02Meta(Sc):
    def construct(self):
        mp = new_map(BIG)
        self.add(mp)
        hi = next(i for i in (7, 8, 6, 12, 11, 13) if RANK[i] < 15)
        pond = mp.ponds[hi]
        pc = pond.get_center()
        mp.save_state()
        self.play(mp.animate.scale(3.2, about_point=pc).shift(-pc), run_time=1.3)
        title = lab("local population", 36, TEAL).move_to([0, 3.2, 0])
        self.at("local population")
        self.play(FadeIn(title), run_time=0.5)
        fr = VGroup(*[frog(pond.get_center() + np.array(o), 2.2, i) for i, o in enumerate([(-0.9, 0.1, 0), (0.7, 0.25, 0), (0.0, -0.3, 0), (0.95, -0.2, 0)])])
        self.at("the frogs that live")
        self.play(FadeIn(fr, lag_ratio=0.2), run_time=1.0)
        self.at("pond holds") if False else None
        self.wait(max(0.1, self.t_of("the fields") - 0.8 - self.elapsed()))
        self.play(FadeOut(title), FadeOut(fr), Restore(mp), run_time=1.1)
        allfr = VGroup()
        for i, p in enumerate(mp.ponds):
            if RANK[i] < 15 and i != hi:
                allfr.add(frog(p.get_center() + np.array([-0.2, 0.0, 0]), 0.9, i), frog(p.get_center() + np.array([0.2, -0.05, 0]), 0.9, i + 3))
        own = VGroup(*[frog(pond.get_center() + np.array(o), 0.9, k) for k, o in enumerate([(-0.2, 0, 0), (0.2, -0.05, 0)])])
        self.play(FadeIn(allfr), FadeIn(own), run_time=0.7)
        self.at("the fields between")
        hl = lab("hostile ground", 36, BROWN).move_to([0, 3.2, 0])
        self.play(mp.field.animate.set_fill(BROWN, 0.32), FadeIn(hl), run_time=1.0)
        self.at("linked by dispersal")
        pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (7, 8), (8, 9), (10, 11), (12, 13), (13, 14), (2, 7), (6, 11)]
        pairs = [(a, b) for a, b in pairs if RANK[a] < 15 and RANK[b] < 15] or [(0, 1)]
        lines = VGroup(*[DashedLine(mp.ponds[a].get_center(), mp.ponds[b].get_center(), color=GOLD, stroke_width=4).set_z_index(1) for a, b in pairs])
        dots = VGroup()
        for k, (a, b) in enumerate(pairs):
            d = Dot(radius=0.09, color=GOLD).set_z_index(6)
            d.a, d.b, d.u = mp.ponds[a].get_center(), mp.ponds[b].get_center(), k * 0.17

            def mv(m, dt):
                m.u = (m.u + dt * 0.45) % 1.0
                m.move_to(m.a + (m.b - m.a) * m.u)
            d.add_updater(mv)
            dots.add(d)
        self.play(FadeOut(hl), Create(lines), FadeIn(dots), run_time=1.0)
        self.at("a metapopulation")
        box = RoundedRectangle(corner_radius=0.3, width=12.9, height=6.2, color=WHITE, stroke_width=4).move_to(mp.field.get_center()).set_z_index(8)
        mlab = lab("metapopulation", 40, WHITE, weight=BOLD).move_to([0, 3.2, 0])
        self.play(FadeOut(lines), FadeOut(dots), Create(box), FadeIn(mlab), run_time=1.0)
        self.finish()


class S03Levins(Sc):
    def construct(self):
        mp = new_map(BIG)
        mp.field.set_fill(BROWN, 0.32)
        frs = VGroup()
        for i, p in enumerate(mp.ponds):
            if RANK[i] < 15:
                frs.add(frog(p.get_center() + np.array([-0.2, 0.0, 0]), 0.9, i), frog(p.get_center() + np.array([0.2, -0.05, 0]), 0.9, i + 3))
        self.add(mp, frs)
        card = lab("Richard Levins, 1969", 42, TEXT).move_to([0, 3.2, 0])
        self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.8)
        self.at("forget how many frogs")
        self.play(FadeOut(card), FadeOut(frs), mp.field.animate.set_fill(GREY, 0.20), run_time=1.2)
        self.at("each pond is either")
        occ_i = next(i for i in range(20) if RANK[i] < 15)
        emp_i = next(i for i in range(20) if RANK[i] >= 15)
        po, pe = mp.ponds[occ_i], mp.ponds[emp_i]
        l1 = lab("occupied", 36, TEAL).move_to([-3.0, 3.2, 0])
        l2 = lab("empty", 36, GREY).move_to([3.0, 3.2, 0])
        self.at("occupied or")
        self.play(FadeIn(l1), Circumscribe(po, color=TEAL), run_time=1.0)
        self.at("empty")
        self.play(FadeIn(l2), Circumscribe(pe, color=GREY), run_time=1.0)
        self.at("follow one number")
        pl = M("p", 70, TEAL, weight=BOLD).move_to([-5.2, 3.15, 0])
        self.play(FadeOut(l1), FadeOut(l2), FadeIn(pl), run_time=0.8)
        self.at("fraction of ponds")
        txt = M("p = fraction occupied = 15/20 = 0.75", 36, TEAL).move_to([0, 3.2, 0])
        self.play(Transform(pl, txt), run_time=1.0)
        # count the teal ponds one by one
        teal = [p for i, p in enumerate(mp.ponds) if RANK[i] < 15]
        self.play(LaggedStart(*[Indicate(p, color=WHITE, scale_factor=1.15) for p in teal], lag_ratio=0.1), run_time=2.2)
        self.finish()


class S04Wink(Sc):
    def construct(self):
        mp = new_map(BIG)
        self.add(mp)
        self.play(mp.animate.scale(MID[0] / BIG[0]).move_to([MID[1][0], MID[1][1], 0]), run_time=1.2)
        manual(mp)
        ax = Axes(x_range=[0, 14, 7], y_range=[0, 1, 0.5], x_length=3.4, y_length=3.4,
                  axis_config={"color": GREY, "include_tip": False, "include_ticks": False, "stroke_width": 3}).move_to([4.9, -0.5, 0])
        tl = VGroup(M("0", 22, GREY).next_to(ax.c2p(0, 0), DOWN, buff=0.12), M("14", 22, GREY).next_to(ax.c2p(14, 0), DOWN, buff=0.12),
                    M("0.5", 22, GREY).next_to(ax.c2p(0, 0.5), LEFT, buff=0.1), M("1", 22, GREY).next_to(ax.c2p(0, 1), LEFT, buff=0.1),
                    T("years", 26, TEXT).move_to([4.9, -2.95, 0]), M("p", 30, TEAL).move_to([3.15, 1.5, 0]))
        rates = VGroup(T("c = 0.4 per year", 28, GOLD), T("e = 0.1 per year", 28, RED)).arrange(DOWN, buff=0.15).move_to([4.9, 2.9, 0])
        yr = ValueTracker(0)
        trace = VMobject(color=TEAL, stroke_width=6)

        def tu(m):
            y = yr.get_value()
            k = int(y)
            pts = [ax.c2p(j, CNT[j] / 20) for j in range(k + 1)]
            if k < len(CNT) - 1:
                f = y - k
                pts.append(ax.c2p(y, CNT[k] / 20 + (CNT[k + 1] - CNT[k]) / 20 * f))
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
        trace.add_updater(tu)
        counter = always_redraw(lambda: M(f"p = {CNT[min(int(yr.get_value() + 0.5), 16)]}/20 = {CNT[min(int(yr.get_value() + 0.5), 16)] / 20:.2f}", 38, TEAL).move_to([MID[1][0], 2.75, 0]))
        yl = always_redraw(lambda: M(f"year {int(yr.get_value())}", 28, TEXT).move_to([4.9, 1.95, 0]))
        self.play(Create(ax), FadeIn(tl), FadeIn(rates), FadeIn(counter), run_time=1.0)
        self.add(trace, yl)
        mask = mask_of(15)
        dashed_done = False
        k = 0
        t_h = self.t_of("hovers near")
        end = self.narration_s - 0.4
        while k < 15 and self.elapsed() + 1.0 < end:
            if not dashed_done and self.elapsed() >= t_h - 1.0:
                dl = DashedLine(ax.c2p(0, 0.75), ax.c2p(14, 0.75), color=WHITE, stroke_width=3)
                dlab = M("0.75", 24, WHITE).next_to(ax.c2p(14, 0.75), UP, buff=0.05).shift(LEFT * 0.4)
                self.play(Create(dl), FadeIn(dlab), run_time=0.5)
                dashed_done = True
            out, inn, src = SIM[k]
            self.play(yr.animate(rate_func=linear).set_value(k + 1), *self._step_anims(mp, out, inn, src), run_time=1.0)
            self._cleanup()
            k += 1
        self.finish()

    def _step_anims(self, mp, out, inn, src):
        s = mp.ponds[0].body.width / 1.2
        self._ex = [xmark(mp.ponds[i].get_center(), 0.15 * s + 0.04) for i in out]
        self._ar = [arrow(mp.ponds[a].get_center(), mp.ponds[b].get_center(), s) for a, b in zip(src, inn)]
        return ([Occ(mp.ponds[i], 0.0) for i in out] + [Occ(mp.ponds[j], 1.0) for j in inn] +
                [FadeIn(t) for t in self._ex] + [GrowArrow(a) for a in self._ar])

    def _cleanup(self):
        if self._ex or self._ar:
            self.play(*[FadeOut(x) for x in self._ex + self._ar], run_time=0.2)


class S05Loss(Sc):
    def construct(self):
        mp = new_map(BIG)
        gr = Graph(dg=0, dr=0, p=0.75)
        self.add(mp)
        drive(mp, gr.p)
        self.play(mp.animate.scale(MINI[0] / BIG[0]).move_to([MINI[1][0], MINI[1][1], 0]), run_time=1.5)
        drive(mp, gr.p)
        self.play(FadeIn(gr.panel), Create(gr.ax), FadeIn(gr.labels), run_time=1.5)
        self.add(gr.red)
        ticks = make_ticks(mp)
        self.add(ticks)
        self.at("each occupied pond")
        self.play(ticks.vis.animate.set_value(1.0), run_time=0.8)
        self.at("loses its population")
        self.play(LaggedStart(*[Indicate(t, color=RED, scale_factor=1.8) for t in ticks], lag_ratio=0.04), run_time=1.5)
        el = left("e = 0.1 per year", -0.5, RED, 32)
        self.at("extinction rate")
        self.play(FadeIn(el), run_time=0.6)
        self.play(LaggedStart(*[Indicate(t, color=RED, scale_factor=1.8) for t in ticks], lag_ratio=0.04), run_time=1.3)
        self.at("so total losses")
        self.play(gr.p.animate.set_value(0.0), run_time=1.0)
        self.add(gr.pdot)
        rt = max(1.8, self.t_of("with the fraction") + 0.9 - self.elapsed())
        sweep(self, gr, 0, 1, rt, draw_red=True)
        self.play(FadeIn(gr.loss_lab), run_time=0.5)
        self.finish()


class S06Gain(Sc):
    def construct(self):
        mp = new_map(MINI, n_occ=20)
        gr = Graph(dg=0, dr=1, p=1.0)
        self.add(mp)
        drive(mp, gr.p)
        gr.add_base(self, gold=False)
        self.add(gr.pdot)
        el = left("e = 0.1 per year", -0.5, RED, 32)
        self.add(el)
        self.play(gr.p.animate.set_value(0.5), run_time=1.3)
        manual(mp)
        occ = [i for i in range(20) if RANK[i] < 10]
        emp = [i for i in range(20) if RANK[i] >= 10]
        pairs = sorted([(float(np.linalg.norm(mp.ponds[a].get_center() - mp.ponds[b].get_center())), a, b) for a in occ for b in emp])
        _, a1, b1 = pairs[0]
        a2, b2 = next((a, b) for _, a, b in pairs if a != a1 and b != b1 and a != b1 and b != a1)
        s = mp.ponds[0].body.width / 1.2
        ar1 = arrow(mp.ponds[a1].get_center(), mp.ponds[b1].get_center(), s)
        self.at("colonists must come")
        self.play(GrowArrow(ar1), Indicate(mp.ponds[a1], color=WHITE), run_time=1.2)
        l1 = left("from occupied: p", -1.4, TEAL, 30)
        self.at("an occupied pond")
        self.play(FadeIn(l1), Circumscribe(mp.ponds[a1], color=TEAL), run_time=1.0)
        self.at("found a population")
        self.play(Occ(mp.ponds[b1], 1.0), run_time=1.0)
        l2 = left("to empty: 1 − p", -2.2, GREY, 30)
        self.at("empty one")
        ar2 = arrow(mp.ponds[a2].get_center(), mp.ponds[b2].get_center(), s)
        self.play(FadeIn(l2), FadeOut(ar1), GrowArrow(ar2), run_time=1.0)
        self.play(Occ(mp.ponds[b2], 1.0), run_time=0.8)
        self.at("so gains need")
        self.play(FadeOut(ar2), FadeIn(gr.gain_lab), Indicate(l1), Indicate(l2), run_time=1.2)
        self.finish()


class S07Hump(Sc):
    def construct(self):
        mp = new_map(MINI, n_occ=10)
        gr = Graph(dg=0, dr=1, p=0.5)
        self.add(mp)
        drive(mp, gr.p)
        gr.add_base(self, gold=True, gain_lab=True)
        self.add(gr.pdot)
        self.add(left("e = 0.1 per year", -0.5, RED, 32))
        self.play(gr.p.animate.set_value(0.0), run_time=1.0)
        self.at("no colonists")
        self.play(Indicate(gr.pdot, color=WHITE, scale_factor=2.0), run_time=1.0)
        self.at("with every pond")
        self.play(gr.p.animate.set_value(1.0), run_time=1.5)
        manual(mp)
        self.at("nowhere to land")
        s = mp.ponds[0].body.width / 1.2
        ars = []
        for a, b in ((6, 7), (11, 12)):
            ars.append(arrow(mp.ponds[a].get_center(), mp.ponds[b].get_center(), s))
        self.play(*[GrowArrow(a) for a in ars], run_time=0.7)
        self.play(*[FadeOut(a, shift=LEFT * 0.15) for a in ars], run_time=0.5)
        ars = [arrow(mp.ponds[a].get_center(), mp.ponds[b].get_center(), s) for a, b in ((14, 13), (3, 2))]
        self.play(*[GrowArrow(a) for a in ars], run_time=0.7)
        self.play(*[FadeOut(a, shift=RIGHT * 0.15) for a in ars], run_time=0.5)
        self.at("between those two")
        drive(mp, gr.p)
        self.play(gr.p.animate.set_value(0.0), run_time=1.0)
        self.at("gains rise")
        rt = max(1.8, self.t_of("hump") + 0.6 - self.elapsed())
        sweep(self, gr, 0, 1, rt, draw_gold=True)
        self.finish()


class S08Cross(Sc):
    def construct(self):
        mp = new_map(MINI, n_occ=20)
        gr = Graph(p=1.0)
        self.add(mp)
        drive(mp, gr.p)
        gr.add_base(self, gain_lab=True)
        self.add(gr.pdot)
        self.add(left("c = 0.4", -0.5, GOLD, 30).shift(LEFT * 0.9), left("e = 0.1", -0.5, RED, 30).shift(RIGHT * 1.0))
        self.at("gold hump meets")
        self.add(gr.cross)
        self.play(Flash(gr.pc(0.75, 0.075), color=WHITE, flash_radius=0.5), run_time=1.0)
        pst = M("p*", 34, WHITE).move_to(gr.pc(0.75, 0.075) + DOWN * 1.3 + LEFT * 0.7)
        self.play(FadeIn(pst), run_time=0.5)
        self.at("gains equal losses")
        vl = DashedLine(gr.pc(0.75, 0.075), gr.pc(0.75, 0), color=WHITE, stroke_width=3)
        self.play(Create(vl), Indicate(gr.cross, color=WHITE, scale_factor=1.6), run_time=1.2)
        self.at("settles there")
        up = Arrow(gr.pc(0.97, -0.0), gr.pc(0.8, 0), color=RED, buff=0, stroke_width=6).shift(UP * 0.35)
        self.play(GrowArrow(up), gr.p.animate.set_value(0.75), run_time=1.4)
        dn = Arrow(gr.pc(0.3, 0), gr.pc(0.7, 0), color=GOLD, buff=0, stroke_width=6).shift(UP * 0.35)
        self.play(GrowArrow(dn), gr.p.animate.set_value(0.4), run_time=0.9)
        self.play(gr.p.animate.set_value(0.75), run_time=1.1)
        self.at("that level is")
        e1 = left("p* = 1 − e/c", -1.5, WHITE, 32, mono=True)
        self.play(FadeIn(e1), run_time=0.6)
        self.at("extinction to colonization")
        e2 = left("= 1 − 0.1/0.4", -2.3, WHITE, 32, mono=True)
        self.play(FadeIn(e2), run_time=0.6)
        self.at("with these rates")
        e3 = left("= 0.75", -3.0, WHITE, 36, mono=True)
        self.play(FadeIn(e3), Indicate(gr.cross, color=WHITE, scale_factor=1.8), run_time=1.0)
        self.finish()


def graph_state_s09(sc, gr_kwargs=None):
    mp = new_map(MINI, n_occ=15)
    gr = Graph(p=0.75, dashed_gold=True)
    sc.add(mp)
    drive(mp, gr.p)
    gr.add_base(sc, gain_lab=True)
    sc.add(gr.pdot, gr.cross)
    return mp, gr


class S09Predict(Sc):
    def construct(self):
        mp, gr = graph_state_s09(self)
        pst = M("p* = 0.75", 32, WHITE).move_to([3.4, -1.3, 0])
        self.add(pst)
        self.wait(0.4)
        self.at("colonization rate")
        cl = left("c: 0.4 → 0.2", -0.5, GOLD, 32)
        self.play(FadeIn(cl), Indicate(gr.gain_lab, color=GOLD), run_time=1.0)
        self.at("keep extinction")
        el = left("e stays 0.1", -1.2, RED, 32)
        self.play(FadeIn(el), Indicate(gr.loss_lab, color=RED), run_time=1.0)
        self.at("does the occupied")
        q1 = left("Does the occupied", -2.1, TEXT, 30)
        q2 = left("fraction halve too?", -2.65, TEXT, 30)
        qm = lab("?", 60, YELLOW, weight=BOLD).move_to(gr.pc(0.75, 0.075) + UP * 0.5 + RIGHT * 0.4)
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(qm), Indicate(gr.cross, color=WHITE, scale_factor=2.0), run_time=1.2)
        self.at("make your guess")
        self.play(Indicate(qm, color=YELLOW, scale_factor=1.4), run_time=1.0)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        add_motes(self, 'S10')
        mp, gr = graph_state_s09(self)
        self.add(M("p* = 0.75", 32, WHITE).move_to([3.4, -1.3, 0]))
        self.add(left("c: 0.4 → 0.2", -0.5, GOLD, 32), left("e stays 0.1", -1.2, RED, 32),
                 left("Does the occupied", -2.1, TEXT, 30), left("fraction halve too?", -2.65, TEXT, 30),
                 lab("?", 60, YELLOW, weight=BOLD).move_to(gr.pc(0.75, 0.075) + UP * 0.5 + RIGHT * 0.4))
        cur = None
        for n in (5, 4, 3, 2, 1):
            new = M(str(n), 56, YELLOW).move_to([LX, -3.3, 0])
            if cur is None:
                self.play(FadeIn(new), run_time=0.2)
            else:
                self.play(FadeOut(cur), FadeIn(new), run_time=0.2)
            cur = new
            self.wait(0.8)
        self.finish()


class S11Reveal(Sc):
    def construct(self):
        mp = new_map(MINI, n_occ=15)
        gr = Graph(p=0.75)
        ghost = DashedVMobject(gr.ax.plot(lambda x: C0 * x * (1 - x), x_range=[0, 1, 0.01], color=GOLD, stroke_width=5), num_dashes=40).set_opacity(0.6)
        self.add(mp)
        drive(mp, gr.p)
        gr.add_base(self, gain_lab=False)
        self.add(ghost, gr.pdot, gr.cross)
        gl = M("gains = c p (1 − p)", 26, GOLD).move_to([2.0, 2.3, 0])
        self.add(gl)
        cl = left("c: 0.4 → 0.2", -0.5, GOLD, 32)
        el = left("e stays 0.1", -1.2, RED, 32)
        self.add(cl, el)
        self.at("the hump shrinks")
        self.play(gr.c.animate.set_value(0.2), run_time=1.8)
        self.at("the crossing slides")
        e3 = VGroup(left("p* = 1 − 0.1/0.2", -1.9, WHITE, 30, mono=True), left("= 0.50", -2.5, WHITE, 32, mono=True))
        self.play(gr.p.animate.set_value(0.5), FadeIn(e3), run_time=2.0)
        self.play(Indicate(gr.cross, color=WHITE, scale_factor=1.8), run_time=1.0)
        self.at("what matters")
        e4 = left("it depends on e/c", -3.2, WHITE, 30)
        self.play(FadeIn(e4), Indicate(e3, color=WHITE), run_time=1.5)
        self.at("ratio of the two")
        self.play(Indicate(e4, color=YELLOW), Indicate(gr.cross, color=WHITE, scale_factor=1.6), run_time=1.5)
        self.finish()


class S12Threshold(Sc):
    def construct(self):
        mp = new_map(MINI, n_occ=15)
        gr = Graph(p=0.75)
        self.add(mp)
        drive(mp, gr.p)
        gr.add_base(self, gain_lab=True)
        self.add(gr.pdot, gr.cross)
        self.add(left("c = 0.4", -0.5, GOLD, 30))
        # slider for e (0 .. 0.4)
        x0, x1, ys = -6.0, -2.6, -1.6
        track = Line([x0, ys, 0], [x1, ys, 0], color=GREY, stroke_width=5)
        knob = always_redraw(lambda: Dot([x0 + (x1 - x0) * gr.e.get_value() / 0.4, ys, 0], radius=0.18, color=RED).set_z_index(5))
        ro = always_redraw(lambda: M(f"e = {gr.e.get_value():.2f}", 32, RED).move_to([LX, -2.4, 0]))
        sl = lab("e", 36, RED).move_to([x0 - 0.0, ys + 0.5, 0])
        self.at("push extinction up")
        self.play(Create(track), FadeIn(sl), run_time=0.8)
        self.add(knob, ro)
        # p tracks the crossing
        gr.p.add_updater(lambda m: m.set_value(max(0.0, 1 - gr.e.get_value() / gr.c.get_value())))
        self.at("the red line steepens")
        self.play(gr.e.animate(rate_func=linear).set_value(0.32), run_time=max(2.0, self.t_of("when extinction equals") - 0.4 - self.elapsed()))
        self.at("when extinction equals")
        self.play(gr.e.animate(rate_func=linear).set_value(0.4), run_time=max(1.5, self.t_of("the line only touches") - self.elapsed()))
        gr.p.clear_updaters()
        self.at("the line only touches")
        self.play(Indicate(track, color=WHITE), Flash(gr.pc(0, 0), color=WHITE, flash_radius=0.6), run_time=1.2)
        txt = left("e = c → p* = 0", -3.1, WHITE, 32, mono=True)
        self.at("at zero")
        self.play(FadeIn(txt), run_time=0.6)
        self.at("no crossing")
        self.play(Flash(gr.pc(0, 0), color=WHITE, flash_radius=0.8), Indicate(txt, color=WHITE), run_time=1.2)
        self.finish()


class S13Rule(Sc):
    def construct(self):
        mp = new_map(MINI, n_occ=15)
        gr = Graph(p=0.75)
        self.add(mp)
        manual(mp)
        gr.add_base(self, gain_lab=True)
        self.add(gr.pdot, gr.cross)
        lp = VGroup(left("c = 0.4", -0.5, GOLD, 30).shift(LEFT * 0.9), left("e = 0.1", -0.5, RED, 30).shift(RIGHT * 1.0))
        self.add(lp)
        rng = np.random.RandomState(9)
        mask = mask_of(15)
        grp = VGroup(gr.ax, gr.labels, gr.gold, gr.red, gr.pdot, gr.cross, gr.loss_lab, gr.gain_lab)
        wink(self, mp, mask, rng, 1, 1.0)
        self.at("colonization beats")
        ce = VGroup(M("c", 80, GOLD, weight=BOLD), M(">", 80, TEXT), M("e", 80, RED, weight=BOLD)).arrange(RIGHT, buff=0.3).move_to([LX, -2.0, 0])
        self.play(FadeIn(ce, scale=0.8), run_time=0.8)
        wink(self, mp, mask, rng, 1, 1.0)
        self.at("no single pond")
        wink(self, mp, mask, rng, 1, 1.0)
        self.play(FadeOut(grp), FadeOut(lp), run_time=0.7)
        self.play(mp.animate.scale(BIG[0] / MINI[0]).move_to([BIG[1][0], BIG[1][1], 0]), ce.animate.move_to([0, 3.2, 0]).scale(0.7), run_time=1.4)
        self.at("refounding balances")
        while self.elapsed() < self.narration_s - 1.4:
            wink(self, mp, mask, rng, 2, 1.1)
        self.finish()


def icon_identical():
    return VGroup(*[Ellipse(width=0.55, height=0.4, color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.55) for _ in range(4)]).arrange(RIGHT, buff=0.2)


def icon_reach():
    pts = [LEFT * 0.7 + DOWN * 0.3, RIGHT * 0.7 + DOWN * 0.3, UP * 0.5]
    g = VGroup(*[Dot(p, radius=0.14, color=TEAL) for p in pts])
    for a, b in ((0, 1), (1, 2), (0, 2)):
        g.add(DoubleArrow(pts[a], pts[b], color=GOLD, buff=0.2, stroke_width=3, tip_length=0.15))
    return g


def icon_flat():
    return VGroup(Line(LEFT * 0.9, RIGHT * 0.9, color=GREY, stroke_width=3).shift(DOWN * 0.4), Line(LEFT * 0.9, RIGHT * 0.9, color=RED, stroke_width=6))


class S14Scope(Sc):
    def construct(self):
        mp = new_map(BIG, n_occ=15)
        self.add(mp)
        manual(mp)
        self.play(mp.animate.scale(0.62).move_to([2.9, -0.3, 0]), run_time=1.3)
        hd = lab("model assumptions", 32, TEXT, weight=BOLD).move_to([-4.2, 3.2, 0])
        self.play(FadeIn(hd), run_time=0.5)
        items = []
        for ic, txt, y in ((icon_identical(), "identical ponds", 2.0), (icon_reach(), "all equally reachable", 0.2), (icon_flat(), "rates never change", -1.6)):
            ic.move_to([-4.2, y, 0])
            t = lab(txt, 28, TEXT).next_to(ic, DOWN, buff=0.15)
            items.append(VGroup(ic, t))
        self.at("its ponds are identical")
        self.play(FadeIn(items[0], shift=RIGHT * 0.3), run_time=0.8)
        self.at("all equally reachable")
        self.play(FadeIn(items[1], shift=RIGHT * 0.3), run_time=0.8)
        self.at("rates that never")
        self.play(FadeIn(items[2], shift=RIGHT * 0.3), run_time=0.8)
        rng = np.random.RandomState(4)
        mask = mask_of(15)
        mp2 = mp
        self.wait(max(0.1, self.t_of("real networks have") - 1.8 - self.elapsed()))
        self.play(FadeOut(VGroup(hd, *items)), mp.animate.scale(1.0 / 0.62).move_to([BIG[1][0], BIG[1][1], 0]), run_time=1.2)
        rl = lab("real networks: schematic", 34, TEXT).move_to([0, 3.2, 0])
        self.at("real networks have")
        self.play(FadeIn(rl), run_time=0.5)
        anims = []
        for i, p in enumerate(mp.ponds):
            sx, sy = rng.uniform(0.5, 1.7), rng.uniform(0.5, 1.7)
            sh = np.array([rng.uniform(-0.6, 0.6), rng.uniform(-0.3, 0.3), 0])
            anims.append(p.body.animate.stretch_to_fit_width(1.2 * sx).stretch_to_fit_height(0.84 * sy).shift(sh))
            p.rip.shift(sh)
        self.at("big and small")
        self.play(*anims, run_time=2.0)
        self.at("near and far")
        a, b, c2 = mp.ponds[7].body.get_center(), mp.ponds[8].body.get_center(), mp.ponds[19].body.get_center()
        near = DashedLine(a, b, color=GOLD, stroke_width=5).set_z_index(1)
        far = DashedLine(mp.ponds[0].body.get_center(), c2, color=GOLD, stroke_width=5).set_z_index(1)
        self.play(Create(near), Create(far), run_time=1.0)
        self.at("a small network")
        sm = VGroup(*[Ellipse(width=1.8, height=1.2, stroke_width=3) for _ in range(5)])
        pos = [(-4.0, 0.9), (-1.8, -1.2), (0.3, 1.2), (2.6, -0.6), (4.3, 1.0)]
        sps = []
        for (x, y) in pos:
            pd = Pond((x, y), 1.0, len(sps) * 0.2)
            pd.scale(1.5)
            sps.append(pd)
        small_field = RoundedRectangle(corner_radius=0.3, width=12.6, height=5.9, stroke_width=0, fill_color=GREY, fill_opacity=0.20).move_to([0, -0.5, 0])
        sl = lab("small network: chance loss", 34, TEXT).move_to([0, 3.2, 0])
        self.play(FadeOut(mp), FadeOut(near), FadeOut(far), FadeOut(rl), FadeIn(small_field), FadeIn(VGroup(*sps)), FadeIn(sl), run_time=1.0)
        self.at("can lose every pond")
        for pd in sps:
            tk = xmark(pd.body.get_center(), 0.22)
            self.play(Occ(pd, 0.0), FadeIn(tk), run_time=0.6)
            self.wait(0.15)
        self.at("even when colonization")
        s2 = lab("even with c > e", 34, GOLD).move_to([0, 2.72, 0])
        self.play(FadeIn(s2), run_time=0.6)
        self.finish()


class S15End(EndCard):
    LINE = "A region keeps a species only while colonization beats extinction."
