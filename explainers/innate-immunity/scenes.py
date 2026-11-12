"""Winning the First Hours (innate immunity, the race against doubling).

COLOUR MAP: bacteria GOLD dots; removal dial and k TEAL; barrier wall BROWN; macrophages and
monocytes PURPLE; neutrophils BLUE; receptor glow WHITE-YELLOW; question card TEXT.
One world: the wound box (left), counter under it, clock top right, k slider across the top,
and a log-axis plot (right) computed from count = 100 x (2 (1-k))^(doubling times).
"""
import numpy as np
from types import SimpleNamespace
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CE0"
NEUT = "#4F7DF3"
BROWN = "#B5835A"
HI = "#FFF3A0"
BAC = GOLD

BX0, BX1, BY0, BY1 = -6.6, -1.2, -2.5, 2.3
BCX, BCY = (BX0 + BX1) / 2, (BY0 + BY1) / 2
PX0, PX1, PY0, PY1 = 1.1, 6.4, -2.4, 2.2
NMAX = 110


# ---------- model ----------
def count_at(T, k, delay=0.0, N0=100.0):
    f = 2 * (1 - k)
    d = int(np.floor(T * 3 + 1e-6))
    N = N0
    for s in range(d):
        N *= 2 if s / 3.0 < delay - 1e-9 else f
    return N


def logn_at(T, k, delay=0.0, N0=100.0):
    a, b = min(T, delay), max(T - delay, 0.0)
    return np.log10(N0) + 3 * (a * np.log10(2) + b * np.log10(max(2 * (1 - k), 1e-9)))


def fmt(N):
    if N >= 1000:
        return f"{int(round(N)):,}"
    if N >= 100:
        return f"{int(round(N))}"
    if N >= 10:
        return f"{N:.0f}" if abs(N - round(N)) < 1e-6 else f"{N:.1f}"
    if N >= 1:
        return f"{N:.1f}"
    return f"{N:.3f}"


def px(t):
    return PX0 + (PX1 - PX0) * t / 4.0


def py(l):
    return PY0 + (np.clip(l, -2, 6) + 2) * (PY1 - PY0) / 8.0


def pow10(n, size=28, color=TEXT):
    b = T("10", size, color)
    e = T(str(n), 20, color).next_to(b, UR, buff=0.02).shift(DOWN * 0.1)
    return VGroup(b, e)


# ---------- pieces ----------
class Swarm(VGroup):
    """Gold bacteria that jitter inside a box; the count shown is set by n_func (splitting and removal animate)."""

    def __init__(self, n_func, seed=1, bounds=(BX0 + .15, BX1 - .15, BY0 + .15, BY1 - .15), color=BAC, nmax=NMAX,
                 r=0.115, start_n=0, keep_out=None):
        super().__init__()
        rng = np.random.RandomState(seed)
        self.n_func, self.bounds, self.color, self.nmax, self.keep_out = n_func, bounds, color, nmax, keep_out
        x0, x1, y0, y1 = bounds
        self.pos = np.stack([rng.uniform(x0, x1, nmax), rng.uniform(y0, y1, nmax)], 1)
        self.vel = rng.normal(0, 0.35, (nmax, 2))
        self.alpha = np.array([1.0 if j < start_n else 0.0 for j in range(nmax)])
        self.prev_n = start_n
        self.rng = rng
        self.dots = [Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0) for _ in range(nmax)]
        for d in self.dots:
            self.add(d)
        self.add_updater(self._step)
        self._step(self, 0.0)

    def _step(self, m, dt):
        n = int(self.n_func())
        n = max(0, min(self.nmax, n))
        if n > self.prev_n and self.prev_n > 0:
            for j in range(self.prev_n, n):
                if self.alpha[j] == 0:
                    p = (j - self.prev_n) % self.prev_n
                    self.pos[j] = self.pos[p] + self.rng.normal(0, 0.12, 2)
        self.prev_n = n
        x0, x1, y0, y1 = self.bounds
        self.vel += self.rng.normal(0, 1.6, self.vel.shape) * dt
        sp = np.linalg.norm(self.vel, axis=1, keepdims=True)
        self.vel = np.where(sp > 0.7, self.vel * 0.7 / np.maximum(sp, 1e-6), self.vel)
        self.pos += self.vel * dt
        for ax, lo, hi in ((0, x0, x1), (1, y0, y1)):
            low = self.pos[:, ax] < lo
            high = self.pos[:, ax] > hi
            self.pos[low, ax] = lo
            self.pos[high, ax] = hi
            self.vel[low | high, ax] *= -1
        for j, d in enumerate(self.dots):
            tgt = 1.0 if j < n else 0.0
            a = self.alpha[j]
            a = min(tgt, a + 3 * dt) if tgt > a else max(tgt, a - 2.2 * dt)
            self.alpha[j] = a
            d.set_fill(TEAL if (tgt < a) else self.color, opacity=a)
            d.move_to([self.pos[j, 0], self.pos[j, 1], 0])


def clock_mobs(T_):
    face = Circle(radius=0.4, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([6.15, 3.2, 0])

    def hand():
        a = np.pi / 2 - 2 * np.pi * T_.get_value()
        return Line(face.get_center(), face.get_center() + 0.32 * np.array([np.cos(a), np.sin(a), 0]), color=TEXT, stroke_width=5)

    def txt():
        m = int(round(T_.get_value() * 60))
        return M(f"{m // 60}:{m % 60:02d}", 30, TEXT).move_to([5.0, 3.2, 0])
    return VGroup(face, always_redraw(hand), always_redraw(txt))


def slider(K, x0=-1.2, x1=2.4, y=3.2, h=0.3, size=34, show_val=True):
    track = Rectangle(width=x1 - x0, height=h, stroke_color=TEAL, stroke_width=3, fill_opacity=0).move_to([(x0 + x1) / 2, y, 0])
    fill = always_redraw(lambda: Rectangle(width=max(1e-3, (x1 - x0) * K.get_value()), height=h, stroke_width=0,
                                          fill_color=TEAL, fill_opacity=0.85).move_to([x0 + (x1 - x0) * K.get_value() / 2, y, 0]))
    mark = Line([x0 + (x1 - x0) * .5, y - h, 0], [x0 + (x1 - x0) * .5, y + h, 0], color=TEXT, stroke_width=3)
    lab = T("k", size, TEAL, weight=BOLD).move_to([x0 - 0.45, y, 0])
    g = VGroup(track, fill, mark, lab)
    if show_val:
        g.add(always_redraw(lambda: M(f"{K.get_value():.2f}", 28, TEAL).move_to([x1 + 0.7, y, 0])))
    return g


def corner_factor(text="2 × (1 − k)"):
    return M(text, 34, TEAL).move_to([-4.5, 3.2, 0])


def plot_axes(label=True):
    xa = Line([PX0, PY0, 0], [PX1 + .1, PY0, 0], color=TEXT, stroke_width=4)
    ya = Line([PX0, PY0, 0], [PX0, PY1 + .1, 0], color=TEXT, stroke_width=4)
    panel = Rectangle(width=PX1 - PX0 + 0.1, height=PY1 - PY0 + 0.1, stroke_width=0, fill_color=TEAL, fill_opacity=0.07).move_to([(PX0 + PX1) / 2 + 0.05, (PY0 + PY1) / 2 + 0.05, 0])
    g = VGroup(panel, xa, ya)
    for t in range(5):
        g.add(Line([px(t), PY0, 0], [px(t), PY0 - .1, 0], color=TEXT, stroke_width=3))
        g.add(T(f"{t} h" if t in (0, 4) else str(t), 24, TEXT).move_to([px(t), PY0 - .38, 0]))
    for e in (0, 3, 6):
        g.add(Line([PX0, py(e), 0], [PX0 - .1, py(e), 0], color=TEXT, stroke_width=3))
        g.add(pow10(e).move_to([PX0 - .55, py(e), 0]))
    if label:
        g.add(T("bacteria, log scale", 24, TEXT).move_to([3.9, 2.62, 0]))
    return g


def curve(T_, K, delay=0.0, defense=True, dashed=False, opacity=1.0, tmax=4.0):
    """Computed log-count line: GOLD while no defense acts, TEAL once removal acts."""
    def build():
        t = min(T_.get_value(), tmax)
        k = K.get_value() if defense else 0.0
        d = delay.get_value() if hasattr(delay, "get_value") else delay
        out = VGroup()
        segs = []
        if k > 1e-6 and d > 0:
            segs = [(0, min(t, d), BAC), (d, t, TEAL)]
        elif k > 1e-6:
            segs = [(0, t, TEAL)]
        else:
            segs = [(0, t, BAC)]
        for a, b, col in segs:
            if b - a < 1e-4:
                continue
            ts = np.linspace(a, b, 40)
            pts = [[px(x), py(logn_at(x, k, d)), 0] for x in ts]
            m = VMobject().set_points_as_corners(pts).set_stroke(col, 6, opacity=opacity)
            if dashed:
                m = DashedVMobject(m, num_dashes=30)
            out.add(m)
        return out
    return always_redraw(build)


def make_world(sc, N0=100.0, k0=0.0, plot=True, clock=True, slide=True, factor=True, counter=True, n_start=None,
               delay=0.0, nmax=NMAX, box_alpha=True, swarm=True, show_val=True):
    w = SimpleNamespace()
    w.N, w.T, w.K = ValueTracker(N0), ValueTracker(0.0), ValueTracker(k0)
    w.delay = ValueTracker(delay)
    sc.add(w.N, w.T, w.K, w.delay)
    w.box = Rectangle(width=BX1 - BX0, height=BY1 - BY0, stroke_color=TEXT, stroke_width=3, fill_color=BAC, fill_opacity=0.1).move_to([BCX, BCY, 0])
    if box_alpha:
        w.box.add_updater(lambda m: m.set_fill(BAC, 0.10 + 0.22 * float(np.clip(np.log10(max(w.N.get_value(), 1)) / 5.6, 0, 1))))
    sc.add(w.box)
    w.mobs = [w.box]
    if swarm:
        ns = int(round(N0 * .3)) if n_start is None else n_start
        w.swarm = Swarm(lambda: min(nmax, int(round(w.N.get_value() * 0.3))), seed=3, nmax=nmax, start_n=min(ns, nmax))
        sc.add(w.swarm)
        w.mobs.append(w.swarm)
    if counter:
        w.counter = always_redraw(lambda: VGroup(T("bacteria", 28, TEXT), M(fmt(w.N.get_value()), 40, BAC)).arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to([BCX, -3.05, 0]))
        sc.add(w.counter)
        w.mobs.append(w.counter)
    if clock:
        w.clock = clock_mobs(w.T)
        sc.add(w.clock)
    if slide:
        w.slider = slider(w.K, show_val=show_val)
        sc.add(w.slider)
    if factor:
        w.factor = corner_factor()
        sc.add(w.factor)
    if plot:
        w.axes = plot_axes()
        sc.add(w.axes)
    return w


def drive(w, k_fixed=None, delay=0.0):
    """Make N follow T (stepped doublings) under the world's k."""
    def upd(m):
        w.N.set_value(count_at(w.T.get_value(), w.K.get_value(), w.delay.get_value() if delay is None else delay))
    w.N.add_updater(upd)
    return upd


def stop_drive(w, upd):
    w.N.remove_updater(upd)


def question_card(text="rise or fall?", center=(3.7, -0.3), size=56):
    lab = T(text, size, TEXT, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.25, width=lab.width + 0.9, height=lab.height + 0.9, stroke_color=TEXT, stroke_width=4,
                           fill_color=BG, fill_opacity=1)
    return VGroup(box, lab).move_to([center[0], center[1], 0])


def sweep(sc, rt=0.9):
    band = Rectangle(width=0.5, height=BY1 - BY0, stroke_width=0, fill_color=TEAL, fill_opacity=0.45).move_to([BX0 + 0.25, BCY, 0])
    sc.add(band)
    sc.play(band.animate.move_to([BX1 - 0.25, BCY, 0]), run_time=rt, rate_func=linear)
    sc.play(FadeOut(band), run_time=0.2)


def tick(sc, w, k, rt_each=0.9):
    """One doubling time by hand: teal sweep removes k, survivors double."""
    sweep(sc, rt_each)
    sc.play(w.N.animate.set_value(w.N.get_value() * (1 - k)), run_time=0.7)
    sc.play(w.N.animate.set_value(w.N.get_value() * (1 - k) * 2), run_time=0.7)


# ================= SCENES =================
class S00Title(TitleCard):
    LESSON = "Innate Immunity: Recognize and Respond"
    TITLE = "Winning the First Hours"


class S01Hook(SpokenScene):
    def construct(self):
        w = make_world(self, plot=False, slide=False, factor=False, clock=False)
        T_ = w.T
        clk = clock_mobs(T_)
        self.add(clk)
        x0, x1, y = 0.9, 6.3, -0.9
        bar = Line([x0, y, 0], [x1, y, 0], color=TEXT, stroke_width=6)
        ticks = VGroup(*[Line([x0 + i * (x1 - x0) / 5, y - .18, 0], [x0 + i * (x1 - x0) / 5, y + .18, 0], color=TEXT, stroke_width=4) for i in range(6)])
        cut = T("a cut lets in bacteria", 30, TEXT).move_to([BCX, 2.85, 0])
        self.add(cut)
        # one bacterium doubling, big
        def bdot(x, yy=0.9):
            return Circle(radius=0.36, stroke_color=BAC, stroke_width=4, fill_color=BAC, fill_opacity=0.9).move_to([x, yy, 0])
        d0 = bdot(3.7)
        self.at("and each one")
        self.play(FadeIn(d0, scale=0.5), run_time=0.6)
        self.at("doubles")
        d1 = d0.copy()
        mult = M("× 2", 40, TEXT).move_to([3.7, 2.0, 0])
        self.play(d0.animate.move_to([3.2, 0.9, 0]), d1.animate.move_to([4.2, 0.9, 0]), FadeIn(mult), T_.animate.set_value(1 / 6), run_time=1.0)
        self.at("every 20")
        t20 = T("every 20 minutes", 32, TEAL, weight=BOLD).move_to([3.7, -0.15, 0])
        e0, e1 = d0.copy(), d1.copy()
        self.add(e0, e1)
        self.play(FadeIn(t20), T_.animate.set_value(1 / 3), d0.animate.move_to([2.5, 0.9, 0]), e0.animate.move_to([3.45, 0.9, 0]), d1.animate.move_to([4.4, 0.9, 0]), e1.animate.move_to([5.35, 0.9, 0]), run_time=1.4)
        f0 = e1
        self.at("New antibodies")
        self.play(FadeOut(VGroup(d0, d1, e0, e1, mult, t20)), FadeOut(cut), Create(bar), FadeIn(ticks), run_time=1.0)
        flag_x = x1 - 0.6
        flag = VGroup(Line([flag_x, y, 0], [flag_x, y + 1.6, 0], color=TEXT, stroke_width=5),
                      T("new antibodies:", 30, TEXT), T("days", 40, TEXT, weight=BOLD))
        flag[1].next_to(flag[0].get_end(), LEFT, buff=0.3).shift(DOWN * 0.3)
        flag[2].next_to(flag[1], DOWN, buff=0.08, aligned_edge=RIGHT)
        flag[0].set_z_index(2)
        self.play(FadeIn(flag, shift=LEFT * 0.4), run_time=0.9)
        self.at("so what has to happen")
        brace = Brace(Line([x0, y, 0], [x0 + 0.7, y, 0]), DOWN, color=TEAL)
        q = T("first few hours?", 38, TEAL, weight=BOLD).next_to(brace, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(GrowFromCenter(brace), FadeIn(q), T_.animate.set_value(1.0), run_time=1.6)
        self.finish()


class S02Grow(SpokenScene):
    def construct(self):
        w = make_world(self, slide=False, factor=False, plot=False)
        w.axes = plot_axes()
        self.play(FadeIn(w.axes), run_time=1.0)
        g = curve(w.T, w.K, defense=False)
        self.add(g)
        drive(w)
        self.at("Every 20 minutes")
        self.play(w.T.animate.set_value(1 / 3), run_time=1.3, rate_func=smooth)
        self.at("The clock runs")
        lab = T("12 doublings", 32, TEXT).move_to([4.2, -1.0, 0])
        self.play(w.T.animate.set_value(4.0), run_time=max(1.0, self.t_of("past") - self.elapsed() + 0.5), rate_func=linear)
        self.play(FadeIn(lab), run_time=0.5)
        self.finish()


class S03Dial(SpokenScene):
    def construct(self):
        w = make_world(self, plot=False, slide=False, factor=False, clock=True, show_val=False)
        K = ValueTracker(0.0)
        self.add(K)
        x0, x1, y = 1.1, 6.2, 0.9
        track = Rectangle(width=x1 - x0, height=0.7, stroke_color=TEAL, stroke_width=4, fill_opacity=0).move_to([(x0 + x1) / 2, y, 0])
        fill = always_redraw(lambda: Rectangle(width=max(1e-3, (x1 - x0) * K.get_value()), height=0.7, stroke_width=0, fill_color=TEAL,
                                              fill_opacity=0.85).move_to([x0 + (x1 - x0) * K.get_value() / 2, y, 0]))
        self.at("defense")
        self.play(Create(track), run_time=1.0)
        self.add(fill)
        self.at("In each doubling time")
        self.play(w.T.animate.set_value(1 / 3), run_time=1.4, rate_func=smooth)
        self.at("removes a fraction")
        sweep(self, 0.9)
        self.play(w.N.animate.set_value(60), K.animate.set_value(0.4), run_time=1.3)
        self.at("Call that fraction")
        kl = T("k", 64, TEAL, weight=BOLD).move_to([(x0 + x1) / 2, y + 1.15, 0])
        cap = T("fraction removed", 30, TEAL).move_to([(x0 + x1) / 2, y - 0.85, 0])
        cap2 = T("per doubling time", 30, TEAL).next_to(cap, DOWN, buff=0.1)
        self.play(FadeIn(kl, scale=1.4), run_time=0.7)
        self.play(FadeIn(cap), FadeIn(cap2), run_time=0.7)
        self.at("The survivors then double")
        self.play(w.N.animate.set_value(120), w.T.animate.set_value(2 / 3), run_time=1.6)
        self.at("just as before")
        sweep(self, 0.7)
        self.play(w.N.animate.set_value(72), run_time=0.6)
        self.finish()


class S04Factor(SpokenScene):
    def construct(self):
        w = make_world(self, plot=False, slide=False, factor=False, clock=True, N0=100, k0=0.4)
        K = w.K
        w.slider = slider(K, show_val=False)
        self.add(w.slider)
        self.at("multiplies the count")
        pre = T("each doubling time", 30, TEXT).move_to([3.7, 1.9, 0])
        big = M("count × 2 × (1 − k)", 32, TEAL).move_to([3.7, 1.2, 0])
        self.play(FadeIn(pre), run_time=0.8)
        self.at("by 2 times")
        self.play(Write(big), run_time=2.0)
        self.at("That factor is the whole")
        fac = M("2 × (1 − k)", 34, TEAL)
        self.play(Indicate(big, color=TEAL, scale_factor=1.05), run_time=0.9)
        self.play(FadeOut(pre), ReplacementTransform(big, corner_factor()), run_time=1.3)
        # panel: factor = 1 line
        line = Line([1.0, -0.1, 0], [6.4, -0.1, 0], color=TEAL, stroke_width=5)
        ll = M("factor = 1", 30, TEAL).move_to([5.0, 0.28, 0])
        zup = Rectangle(width=5.4, height=2.2, stroke_width=0, fill_color=BAC, fill_opacity=0.15).move_to([3.7, 1.0, 0])
        zdn = Rectangle(width=5.4, height=2.2, stroke_width=0, fill_color=TEAL, fill_opacity=0.15).move_to([3.7, -1.2, 0])
        self.at("Above 1")
        self.play(Create(line), FadeIn(ll), run_time=0.8)
        up = Arrow([2.0, 0.2, 0], [2.0, 1.8, 0], color=BAC, buff=0, stroke_width=10)
        gl = T("grows", 40, BAC, weight=BOLD).move_to([3.8, 1.0, 0])
        self.play(FadeIn(zup), GrowArrow(up), FadeIn(gl), w.N.animate.set_value(200), run_time=1.4)
        self.at("Below 1")
        dn = Arrow([2.0, -0.4, 0], [2.0, -2.0, 0], color=TEAL, buff=0, stroke_width=10)
        sl = T("shrinks", 40, TEAL, weight=BOLD).move_to([3.8, -1.2, 0])
        self.play(FadeIn(zdn), GrowArrow(dn), FadeIn(sl), w.N.animate.set_value(100), run_time=1.4)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        w = make_world(self, plot=False, slide=True, factor=True, clock=True, k0=0.0)
        # bar of four quarters
        qs = VGroup(*[Rectangle(width=1.3, height=1.0, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0).move_to([1.75 + 1.35 * i, 1.0, 0]) for i in range(4)])
        self.at("every 20 minutes") if False else None
        self.at("remove")
        self.play(FadeIn(qs), run_time=0.8)
        self.at("three quarters")
        self.play(*[qs[i].animate.set_fill(TEAL, 0.8) for i in range(3)], w.K.animate.set_value(0.75), run_time=1.6)
        tq = T("3 of every 4 removed", 32, TEAL).move_to([3.7, 0.0, 0])
        self.play(FadeIn(tq), run_time=0.6)
        self.at("Does the count")
        card = question_card("rise or fall?", center=(3.7, -1.5))
        self.play(FadeIn(card, scale=0.9), run_time=0.8)
        up = Arrow([0.9, -2.3, 0], [0.9, -0.8, 0], color=BAC, buff=0, stroke_width=8)
        dn = Arrow([6.5, -0.8, 0], [6.5, -2.3, 0], color=TEAL, buff=0, stroke_width=8)
        self.play(GrowArrow(up), GrowArrow(dn), run_time=0.8)
        self.at("Decide before")
        self.play(Indicate(card, color=TEXT, scale_factor=1.06), run_time=1.2)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        w = make_world(self, plot=False, slide=True, factor=True, clock=True, k0=0.75)
        qs = VGroup(*[Rectangle(width=1.3, height=1.0, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.8 if i < 3 else 0).move_to([1.75 + 1.35 * i, 1.0, 0]) for i in range(4)])
        card = question_card("rise or fall?", center=(3.7, -1.0))
        ring_bg = Circle(radius=0.45, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.4).move_to([6.0, -2.9, 0])
        prog = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.45, start_angle=np.pi / 2, angle=-2 * np.pi * max(prog.get_value(), 1e-3), color=TEAL, stroke_width=7).move_to([6.0, -2.9, 0]))
        self.add(qs, card, ring_bg, ring)
        self.play(prog.animate.set_value(1.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        w = make_world(self, k0=0.75, plot=False, factor=False)
        w.axes = plot_axes()
        self.add(w.axes)
        gold = curve(w.T, ValueTracker(0.0), defense=False, opacity=0.55, tmax=4.0)
        gold_ref = VGroup(*[Line([0, 0, 0], [0, 0, 0])])
        # full no-defense reference line
        pts = [[px(t), py(logn_at(t, 0.0)), 0] for t in np.linspace(0, 4, 40)]
        ref = VMobject().set_points_as_corners(pts).set_stroke(BAC, 5, opacity=0.85)
        reflab = T("no defense", 28, BAC).move_to([2.3, 2.0, 0])
        w.factor = M("2 × (1 − k)", 34, TEAL).move_to([-4.5, 3.2, 0])
        self.add(w.factor)
        self.add(ref, reflab)
        tl = curve(w.T, w.K)
        self.add(tl)
        drive(w)
        self.at("It falls")
        dnl = VGroup(T("falls", 48, TEAL, weight=BOLD)).move_to([BCX, BCY, 0])
        dnl.add_to_back(BackgroundRectangle(dnl[0], color=BG, fill_opacity=0.9, buff=0.15))
        dnl.set_z_index(5)
        self.play(FadeIn(dnl, scale=1.3), run_time=0.6)
        self.at("The factor is")
        self.play(FadeOut(dnl), Transform(w.factor, M("2 × 0.25 = 0.5", 34, TEAL).move_to([-4.5, 3.2, 0])), run_time=1.0)
        self.at("so every 20 minutes")
        self.play(w.T.animate.set_value(1.0), run_time=max(1.0, self.t_of("After four") - 0.2 - self.elapsed() - 0.2), rate_func=linear)
        self.at("After four hours")
        end_t = self.t_of("one bacterium") + 0.2 - self.elapsed()
        self.play(w.T.animate.set_value(4.0), run_time=max(1.2, end_t - 0.2), rate_func=linear)
        ex = T("expected count", 28, TEXT).move_to([BCX, -3.6, 0])
        self.play(FadeIn(ex), run_time=0.5)
        self.at("The infection")
        cl = T("very likely cleared", 34, TEAL, weight=BOLD).move_to([BCX, BCY, 0]).set_z_index(5)
        self.play(FadeIn(cl, scale=1.2), run_time=1.0)
        self.finish()


class S08Threshold(SpokenScene):
    def construct(self):
        w = make_world(self, k0=0.75, plot=False, factor=False)
        w.axes = plot_axes()
        self.add(w.axes)
        pts = [[px(t), py(logn_at(t, 0.0)), 0] for t in np.linspace(0, 4, 40)]
        ref = VMobject().set_points_as_corners(pts).set_stroke(BAC, 5, opacity=0.85)
        self.add(ref)
        # teal computed line, redrawn live from k
        Tfull = ValueTracker(4.0)
        self.add(Tfull)
        tl = curve(Tfull, w.K)
        self.add(tl)
        w.factor = always_redraw(lambda: M(f"2 × {1 - w.K.get_value():.2f} = {2 * (1 - w.K.get_value()):.2f}", 34, TEAL).move_to([-4.5, 3.2, 0]))
        self.add(w.factor)
        w.N.set_value(100)
        self.at("slide the dial")
        self.play(w.K.animate.set_value(0.5), run_time=max(1.5, self.t_of("At exactly") - 0.2 - self.elapsed() + 1.2), rate_func=smooth)
        self.at("the factor is")
        lab = T("k = 0.5: factor 1, holds", 30, TEAL).move_to([3.9, -0.65, 0])
        self.play(FadeIn(lab), run_time=0.7)
        self.at("and the counter freezes")
        Tfull.set_value(4.0)
        self.play(w.T.animate.set_value(4.0), run_time=2.4, rate_func=linear)
        self.at("So in this model")
        self.play(Indicate(w.slider, color=TEAL), run_time=1.0)
        self.at("Remove more than half")
        win = T("win: k above 0.5", 38, TEAL, weight=BOLD).move_to([3.9, -1.55, 0])
        self.play(FadeIn(win, shift=UP * 0.2), run_time=0.9)
        self.play(Indicate(win, color=TEAL, scale_factor=1.08), run_time=1.2)
        self.finish()


class S09Delay(SpokenScene):
    def construct(self):
        w = make_world(self, k0=0.75, plot=False, factor=True)
        w.axes = plot_axes()
        self.add(w.axes)
        pts = [[px(t), py(logn_at(t, 0.75)), 0] for t in np.linspace(0, 4, 40)]
        early = DashedVMobject(VMobject().set_points_as_corners(pts).set_stroke(TEAL, 5, opacity=0.6), num_dashes=24)
        early_lab = T("removal from the start", 24, TEAL).move_to([4.85, 0.7, 0])
        self.play(FadeIn(early), FadeIn(early_lab), run_time=1.2)
        self.at("Keep the same strong")
        self.play(Indicate(w.slider, color=TEAL), run_time=1.0)
        self.at("wait one hour")
        w.delay.set_value(1.0)
        tl = curve(w.T, w.K, delay=w.delay)
        self.add(tl)
        drive(w, delay=None)
        br = Brace(Line([px(0), PY0 + .05, 0], [px(1), PY0 + .05, 0]), UP, color=TEXT, buff=0.05)
        brl = T("delay 1 h", 28, TEXT).next_to(br, UP, buff=0.05).shift(RIGHT * 0.5)
        self.play(GrowFromCenter(br), FadeIn(brl), w.T.animate.set_value(1.0), run_time=max(1.3, self.t_of("The pile") - self.elapsed() - 0.4), rate_func=linear)
        self.at("The pile reaches")
        pk = T("800", 34, BAC, weight=BOLD).move_to([px(1) - 0.05, py(np.log10(800)) + 0.45, 0])
        self.play(FadeIn(pk, scale=1.3), run_time=0.6)
        self.at("before it turns")
        self.play(w.T.animate.set_value(2.4), run_time=max(1.0, self.narration_s - self.elapsed() - 0.2), rate_func=linear)
        self.finish()


class S10Delay2(SpokenScene):
    def construct(self):
        w = make_world(self, k0=0.75, plot=False, factor=True, clock=False, swarm=True, N0=100)
        w.axes = plot_axes()
        self.add(w.axes)
        T1 = ValueTracker(4.0)
        self.add(T1)
        c1 = curve(T1, w.K, delay=1.0)
        self.add(c1)
        pk1 = T("800", 30, BAC, weight=BOLD).move_to([px(1) - 0.05, py(np.log10(800)) + 0.65, 0])
        self.add(pk1)
        T2 = ValueTracker(0.0)
        self.add(T2)
        c2 = curve(T2, w.K, delay=2.0)
        self.add(c2)
        cap = T("illustrative model, not a measured wound", 24, TEXT).move_to([3.0, -3.3, 0])
        self.add(cap)
        self.at("Wait two hours")
        self.play(T2.animate.set_value(2.0), run_time=1.6, rate_func=linear)
        self.at("reaches 6")
        pk2 = T("6,400", 34, BAC, weight=BOLD).move_to([px(2) + 0.7, py(np.log10(6400)) + 0.8, 0])
        self.play(FadeIn(pk2, scale=1.3), T2.animate.set_value(4.0), run_time=2.4, rate_func=linear)
        self.at("Each hour of waiting")
        ar = Arrow([px(1) + 0.2, py(np.log10(800)) + 0.15, 0], [px(2) - 0.25, py(np.log10(6400)) - 0.1, 0], color=TEXT, buff=0, stroke_width=6)
        t8 = T("× 8 per hour of delay", 28, TEXT).move_to([3.6, -1.5, 0])
        t8b = T("(3 doublings)", 28, TEXT).next_to(t8, DOWN, buff=0.1)
        self.play(GrowArrow(ar), run_time=0.8)
        self.play(FadeIn(t8), run_time=0.7)
        self.at("eightfold")
        self.play(FadeIn(t8b), run_time=0.7)
        self.at("receptors must be ready")
        rg = VGroup(Circle(radius=0.25, color=HI, stroke_width=5).move_to([px(1), py(np.log10(800)), 0]),
                    Circle(radius=0.25, color=HI, stroke_width=5).move_to([px(2), py(np.log10(6400)), 0]))
        self.play(Create(rg), run_time=0.9)
        self.play(Indicate(rg, color=HI, scale_factor=1.3), run_time=1.2)
        self.finish()


def build_wall(gap_x=-4.2, gap_w=0.7, thick=0.18):
    xs = [BX0, gap_x - gap_w / 2, gap_x + gap_w / 2, BX1]
    top_l = Rectangle(width=xs[1] - xs[0], height=thick, stroke_width=0, fill_color=BROWN, fill_opacity=1).move_to([(xs[0] + xs[1]) / 2, BY1, 0])
    top_r = Rectangle(width=xs[3] - xs[2], height=thick, stroke_width=0, fill_color=BROWN, fill_opacity=1).move_to([(xs[2] + xs[3]) / 2, BY1, 0])
    return VGroup(top_l, top_r)


def full_wall():
    return VGroup(build_wall(), Line([BX0, BY0, 0], [BX0, BY1, 0], color=BROWN, stroke_width=10), Line([BX1, BY0, 0], [BX1, BY1, 0], color=BROWN, stroke_width=10),
                  Line([BX0, BY0, 0], [BX1, BY0, 0], color=BROWN, stroke_width=10))


def lab(text, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw).set_stroke(BG, 8, background=True)


def job_cards(filled=(), y0=1.7, dy=1.7, texts=("fewer get in", "the clock starts early", "more removed\nper doubling")):
    cards = VGroup()
    for i, t in enumerate(texts):
        on = (i + 1) in filled
        box = RoundedRectangle(corner_radius=0.2, width=5.5, height=1.4, stroke_color=TEXT if on else GREY, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.14 if on else 0).move_to([3.7, y0 - i * dy, 0])
        num = T(str(i + 1), 44, TEAL, weight=BOLD).move_to([1.3, y0 - i * dy, 0])
        tx = T(t, 28, TEXT, line_spacing=0.8).move_to([4.0, y0 - i * dy, 0])
        if not on:
            tx.set_opacity(0)
            box.set_stroke(opacity=0.5)
        cards.add(VGroup(box, num, tx))
    return cards


def light_card(c):
    return [c[2].animate.set_opacity(1), c[0].animate.set_fill(TEAL, 0.14).set_stroke(TEXT, 3, 1)]


class S11Barrier(SpokenScene):
    def construct(self):
        box = Rectangle(width=BX1 - BX0, height=BY1 - BY0, stroke_color=TEXT, stroke_width=3, fill_color=BAC, fill_opacity=0.05).move_to([BCX, BCY, 0])
        cards = job_cards(filled=())
        out = Swarm(lambda: 16, seed=7, bounds=(BX0 + .15, BX1 - .15, BY1 + 0.3, BY1 + 1.35), start_n=16, nmax=16)
        inn = Swarm(lambda: 4, seed=9, bounds=(BX0 + .15, BX1 - .15, BY0 + .15, BY1 - .3), start_n=4, nmax=4)
        self.add(box, out, inn)
        wall = full_wall()
        gate_x = -4.2
        wl = lab("a bacterial wound", 28, TEXT).move_to([BCX, -2.95, 0])
        self.add(wl)
        self.at("the defenses")
        self.play(FadeIn(cards, lag_ratio=0.2), run_time=1.6)
        self.at("First")
        self.play(FadeIn(wall[0], shift=DOWN * 0.4), Create(wall[1]), Create(wall[2]), Create(wall[3]), run_time=1.6)
        self.play(*light_card(cards[0]), run_time=0.6)
        self.at("barriers")
        sl = []
        for i in range(2):
            d = Circle(radius=0.115, stroke_width=0, fill_color=BAC, fill_opacity=1).move_to([gate_x + 0.15 * i, BY1 + 0.5, 0])
            sl.append(d)
        self.add(*sl)
        self.play(*[sl[i].animate.move_to([gate_x - 0.2 + 0.6 * i, BY1 - 0.9 - 0.5 * i, 0]) for i in range(2)], run_time=1.3)
        self.at("lower the starting number")
        ln = lab("lower starting number", 28, TEXT).move_to([BCX, -2.95, 0])
        self.play(ReplacementTransform(wl, ln), run_time=0.8)
        s1 = T("jobs this model follows;", 26, TEXT).move_to([3.7, -3.0, 0])
        s2 = T("not a complete list", 26, TEXT).move_to([3.7, -3.4, 0])
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.7)
        self.finish()


class S12Sense(SpokenScene):
    def construct(self):
        box = Rectangle(width=BX1 - BX0, height=BY1 - BY0, stroke_color=TEXT, stroke_width=3, fill_color=BAC, fill_opacity=0.05).move_to([BCX, BCY, 0])
        wall = full_wall()
        cards = job_cards(filled=(1,))
        self.add(box, wall, cards)
        clk_t = ValueTracker(0.0)
        self.add(clk_t)
        clk = clock_mobs(clk_t)
        MC = np.array([BCX, -0.45, 0.0])
        mac = Circle(radius=1.15, stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.3).move_to(MC)
        mlab = T("macrophage", 24, PURPLE, weight=BOLD).move_to(MC).set_stroke(BG, 6, background=True).set_z_index(8)
        bacs = Swarm(lambda: 4, seed=11, bounds=(BX0 + .2, BX1 - .2, BY0 + .2, BY1 - .2), start_n=4, nmax=4)
        self.add(bacs)
        self.at("Second")
        self.play(*light_card(cards[1]), run_time=0.9)
        self.at("the clock starts")
        self.add(clk)
        self.play(clk_t.animate.set_value(0.05), run_time=1.2, rate_func=linear)
        self.at("A macrophage")
        self.play(GrowFromCenter(mac), run_time=1.0)
        self.play(FadeIn(mlab), run_time=0.6)
        self.at("long")
        el = lab("long-lived eating cell", 26, TEXT).move_to([BCX, -2.15, 0])
        self.play(FadeIn(el), clk_t.animate.set_value(0.12), run_time=1.2)
        self.at("carries ready")
        angs = [120, 70, 20, 200, 300]
        recs = VGroup()
        for a in angs:
            ar = np.deg2rad(a)
            u = np.array([np.cos(ar), np.sin(ar), 0])
            base = MC + 1.15 * u
            stem = Line(base, base + 0.3 * u, color=TEXT, stroke_width=4)
            blk = Square(side_length=0.3, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.3).move_to(base + 0.45 * u)
            recs.add(VGroup(stem, blk))
        self.play(FadeIn(recs, lag_ratio=0.25), FadeOut(el), clk_t.animate.set_value(0.2), run_time=2.0)
        self.at("One")
        tlr = recs[0]
        tag = lab("TLR4", 34, HI, weight=BOLD).next_to(tlr[1], LEFT, buff=0.15).set_stroke(BG, 6, background=True).set_z_index(8)
        self.play(Indicate(tlr, color=HI, scale_factor=1.5), FadeIn(tag), run_time=1.4)
        self.at("senses a molecule")
        bt = Circle(radius=0.2, stroke_width=0, fill_color=BAC, fill_opacity=1).move_to([BX1 - 1.2, 1.5, 0])
        lps = lab("lipopolysaccharide", 26, TEXT).next_to(bt, UP, buff=0.12).set_stroke(BG, 6, background=True).set_z_index(8)
        lps.add_updater(lambda m: m.next_to(bt, UP, buff=0.12))
        self.play(FadeIn(bt), FadeIn(lps), run_time=0.6)
        target = tlr[1].get_center() + np.array([0.3, 0.12, 0])
        self.at("from the outer membrane")
        self.play(bt.animate.move_to(target), clk_t.animate.set_value(0.3), run_time=1.6)
        glow = Circle(radius=0.3, stroke_color=HI, stroke_width=6, fill_color=HI, fill_opacity=0.5).move_to(tlr[1].get_center())
        self.play(FadeIn(glow, scale=0.5), tlr[1].animate.set_fill(HI, 1).set_stroke(HI, 4), run_time=0.5)
        self.play(glow.animate.scale(2.5).set_opacity(0), run_time=0.9)
        self.finish()


def bgl(m):
    g = VGroup(BackgroundRectangle(m, color=BG, fill_opacity=0.9, buff=0.08), m)
    g.set_z_index(8)
    return g


class S13Inflame(SpokenScene):
    def construct(self):
        box = Rectangle(width=BX1 - BX0, height=BY1 - BY0, stroke_color=TEXT, stroke_width=3, fill_color=BAC, fill_opacity=0.05).move_to([BCX, BCY, 0])
        wall = full_wall()
        cards = job_cards(filled=(1, 2))
        mac = Circle(radius=0.7, stroke_color=PURPLE, stroke_width=5, fill_color=PURPLE, fill_opacity=0.3).move_to([BCX, 0.9, 0])
        bacs = Swarm(lambda: 12, seed=13, bounds=(BX0 + .3, BX1 - .3, -1.0, BY1 - .3), start_n=12, nmax=12)
        K = ValueTracker(0.2)
        vw = ValueTracker(0.0)
        clk_t = ValueTracker(0.3)
        self.add(K, vw, clk_t)
        sl = slider(K, x0=-1.2, x1=2.4, show_val=False)
        clk = clock_mobs(clk_t)
        vessel = always_redraw(lambda: Rectangle(width=BX1 - BX0 - 0.1, height=0.35 + 0.5 * vw.get_value(), stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.25).move_to([BCX, BY0 + 0.05 + (0.35 + 0.5 * vw.get_value()) / 2, 0]))
        vlab = lab("blood vessel", 26, RED).move_to([BCX, -2.95, 0])
        self.add(box, wall, cards, mac, bacs, sl, clk, vessel, vlab)
        self.at("Third")
        self.play(*light_card(cards[2]), run_time=0.9)
        self.at("Sensing sets off")
        infl = lab("inflammation", 34, HI, weight=BOLD).move_to([BCX, 1.95, 0]).set_stroke(BG, 6, background=True).set_z_index(8)
        self.play(FadeIn(infl, scale=1.2), run_time=0.9)
        self.at("A nearby vessel")
        self.play(vw.animate.set_value(1.0), FadeOut(infl), run_time=2.0)
        self.at("leaks")
        gx = [BCX - 1.6, BCX, BCX + 1.6]
        gaps = VGroup(*[Rectangle(width=0.3, height=0.1, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([x, BY0 + 0.05 + 0.85, 0]) for x in gx])
        self.play(FadeIn(gaps), run_time=0.5)
        self.at("Neutrophils")
        neuts = VGroup(*[Circle(radius=0.22, stroke_color=NEUT, stroke_width=4, fill_color=NEUT, fill_opacity=0.7).move_to([x + 0.0, BY0 + 0.5, 0]) for x in gx + [BCX - 0.8, BCX + 0.8]])
        nl = bgl(lab("neutrophils", 28, NEUT, weight=BOLD).move_to([BCX + 1.4, -0.9, 0]))
        self.add(neuts)
        tgt = [[BCX - 1.9, -0.2], [BCX - 0.9, -0.5], [BCX + 0.2, -0.2], [BCX + 1.2, -0.5], [BCX + 1.9, -0.1]]
        self.play(FadeIn(nl), *[neuts[i].animate.move_to([tgt[i][0], tgt[i][1], 0]) for i in range(5)], K.animate.set_value(0.3), run_time=1.8)
        self.play(FadeOut(nl), run_time=0.3)
        self.at("then monocytes")
        monos = VGroup(*[Circle(radius=0.22, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.5).move_to([x, BY0 + 0.5, 0]) for x in gx])
        ml = bgl(lab("monocytes", 28, PURPLE, weight=BOLD).move_to([BCX, -0.5, 0]))
        self.add(monos)
        self.play(FadeIn(ml), *[monos[i].animate.move_to([BCX - 1.7 + 1.7 * i, -1.2 + 0.0, 0]) for i in range(3)], K.animate.set_value(0.38), run_time=1.6)
        self.at("which become macrophages")
        mm = bgl(lab("macrophages", 28, PURPLE, weight=BOLD).move_to([BCX, -0.6, 0]))
        self.play(FadeOut(ml), FadeIn(mm), *[monos[i].animate.scale(2.0) for i in range(3)], K.animate.set_value(0.46), run_time=1.8)
        self.finish()


class S14Steps(SpokenScene):
    def construct(self):
        labels = ["sense", "vessels change", "cells arrive", "clear and repair"]
        xs = [-5.0, -1.65, 1.7, 5.05]
        blocks = VGroup()
        for i, (lb, x) in enumerate(zip(labels, xs)):
            bx = RoundedRectangle(corner_radius=0.2, width=3.0, height=2.2, stroke_color=TEXT, stroke_width=3, fill_color=TEAL, fill_opacity=0.08).move_to([x, 1.6, 0])
            tx = T(lb.replace(" ", "\n", 1) if i in (1, 3) else lb, 32, TEXT, line_spacing=0.8).move_to([x, 1.45, 0])
            nm = T(str(i + 1), 34, TEAL, weight=BOLD).move_to([x, 2.35, 0])
            tx.set_opacity(0.35)
            blocks.add(VGroup(bx, tx, nm))
        K = ValueTracker(0.12)
        self.add(K)
        x0, x1, y = -4.4, 4.4, -0.6
        track = Rectangle(width=x1 - x0, height=0.8, stroke_color=TEAL, stroke_width=4, fill_opacity=0).move_to([0, y, 0])
        fill = always_redraw(lambda: Rectangle(width=max(1e-3, (x1 - x0) * K.get_value()), height=0.8, stroke_width=0, fill_color=TEAL, fill_opacity=0.85).move_to([x0 + (x1 - x0) * K.get_value() / 2, y, 0]))
        mark = Line([0, y - 0.65, 0], [0, y + 0.65, 0], color=TEXT, stroke_width=5)
        marklab = M("0.5", 32, TEXT).move_to([0, y - 1.0, 0])
        kl = T("k", 48, TEAL, weight=BOLD).move_to([x0 - 0.6, y, 0])
        self.at("Inflammation runs")
        self.play(FadeIn(blocks, lag_ratio=0.3), run_time=2.0)

        def light(i):
            return [blocks[i][1].animate.set_opacity(1), blocks[i][0].animate.set_fill(TEAL, 0.3)]
        self.at("scents")
        self.play(*light(0), run_time=0.5)
        self.at("vessels change")
        self.play(*light(1), run_time=0.5)
        self.at("cells arrive")
        self.play(*light(2), run_time=0.5)
        self.at("then clear and repair")
        self.play(*light(3), run_time=0.5)
        self.at("As the eating cells")
        self.play(Create(track), FadeIn(mark), FadeIn(marklab), FadeIn(kl), run_time=0.9)
        self.add(fill)
        self.at("the fraction removed")
        self.play(K.animate.set_value(0.4), run_time=max(1.2, self.narration_s - self.elapsed() - 1.6), rate_func=smooth)
        sm = T("whether it passes 0.5 depends on the infection", 28, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(sm), run_time=0.6)
        self.finish()


class S15Close(SpokenScene):
    def construct(self):
        xs = [-4.2, 0, 4.2]
        cards = VGroup()
        for x in xs:
            cards.add(RoundedRectangle(corner_radius=0.25, width=3.8, height=4.2, stroke_color=TEXT, stroke_width=3, fill_color=TEAL, fill_opacity=0.06).move_to([x, 0.6, 0]))
        wall_icon = VGroup(Rectangle(width=2.6, height=0.4, stroke_width=0, fill_color=BROWN, fill_opacity=1),
                           *[Circle(radius=0.12, stroke_width=0, fill_color=BAC, fill_opacity=1).move_to([-1.0 + 0.7 * i, 0.6 + 0.3 * (i % 2), 0]) for i in range(4)]).move_to([xs[0], 1.5, 0])
        blk = Square(side_length=0.8, stroke_color=HI, stroke_width=5, fill_color=HI, fill_opacity=0.8).move_to([xs[1], 1.5, 0])
        halo = Circle(radius=0.8, stroke_color=HI, stroke_width=4, stroke_opacity=0.6).move_to(blk)
        cells = VGroup(*[Circle(radius=0.3, stroke_color=NEUT, stroke_width=4, fill_color=NEUT, fill_opacity=0.5).move_to([xs[2] - 0.8 + 0.8 * i, 1.8 - 0.4 * (i % 2), 0]) for i in range(3)],
                       *[Circle(radius=0.38, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.4).move_to([xs[2] - 0.4 + 0.8 * i, 1.1 - 0.2 * (i % 2), 0]) for i in range(2)])
        texts = [T("keep\nthem out", 34, BROWN, weight=BOLD, line_spacing=0.8), T("see them\nat once", 34, HI, weight=BOLD, line_spacing=0.8),
                 T("remove more\nthan half", 34, TEAL, weight=BOLD, line_spacing=0.8)]
        for t_, x in zip(texts, xs):
            t_.move_to([x, -0.55, 0])
        sub = T("each doubling time", 26, TEXT).move_to([xs[2], -1.9, 0])
        self.at("Keep them out")
        self.play(FadeIn(cards[0]), FadeIn(wall_icon), run_time=0.8)
        self.play(FadeIn(texts[0]), run_time=0.5)
        self.at("see them at once")
        self.play(FadeIn(cards[1]), FadeIn(blk), FadeIn(halo), run_time=0.8)
        self.play(FadeIn(texts[1]), Indicate(halo, color=HI, scale_factor=1.3), run_time=0.7)
        self.at("and remove more")
        self.play(FadeIn(cards[2]), FadeIn(cells, lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(texts[2]), FadeIn(sub), run_time=0.7)
        self.at("This is an illustrative")
        note = T("illustrative model: one well-mixed wound, constant rates", 28, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(note), run_time=1.0)
        self.play(Indicate(note, color=TEXT, scale_factor=1.03), run_time=1.5)
        self.finish()


class S16End(EndCard):
    LINE = "Remove more than half every doubling time, and start early."
