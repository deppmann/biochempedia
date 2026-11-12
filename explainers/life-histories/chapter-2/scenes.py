"""Life histories, film 2: Why the trade-off hides.

Same colour map as film 1 (../scenes.py): intake A = dark bar with light outline, GOLD = reproduction R,
TEAL = self S, GREY = trend lines and labels; axes: horizontal R (gold), vertical S (teal).
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

INK = "#232834"
BIRD_C = "#C9B28F"
NEST_C = "#8A6A44"

K = 0.42                      # axis units per unit of intake
O2 = np.array([-4.8, -3.3, 0.0])
AXL = 6.5


def P(x, y):
    return np.array([x, y, 0.0])


def dp(R, S, O=O2, k=K):
    return O + P(k * R, k * S)


def songbird(s=1.0, color=BIRD_C):
    body = Ellipse(width=1.1, height=0.62, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    head = Circle(radius=0.21, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8).move_to(P(0.5, 0.26))
    beak = Polygon(P(0.68, 0.30), P(0.92, 0.24), P(0.68, 0.18), stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=1)
    tail = Polygon(P(-0.45, 0.05), P(-0.95, 0.3), P(-0.95, -0.12), stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
    eye = Dot(P(0.56, 0.30), radius=0.04, color=BG)
    return VGroup(tail, body, head, beak, eye).scale(s)


def chick(x=0, y=0, r=0.12, color=GOLD):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.9).move_to(P(x, y))


def idle(m, amp=0.06, speed=1.7, phase=0.0):
    m._tt = phase
    m._off = 0.0

    def up(mob, dt):
        mob._tt += dt
        new = amp * np.sin(speed * mob._tt)
        mob.shift(UP * (new - mob._off))
        mob._off = new
    m.add_updater(up)
    return m


def axes2(xl="reproduction R", yl="self S", ysize=30):
    xa = Arrow(O2, O2 + P(AXL, 0), buff=0, color=GOLD, stroke_width=5, tip_length=0.2)
    ya = Arrow(O2, O2 + P(0, AXL), buff=0, color=TEAL, stroke_width=5, tip_length=0.2)
    xt = T(xl, 30, GOLD)
    xt.move_to(O2 + P(AXL + 0.25 + xt.width / 2, 0))
    yt = T(yl, ysize, TEAL)
    yt.move_to(P(O2[0] + yt.width / 2 - 0.2, O2[1] + AXL + 0.4))
    return VGroup(xa, ya), xt, yt


def tline2(A, color=GREY, w=5, op=1.0):
    return Line(dp(0, A), dp(A, 0), color=color, stroke_width=w, stroke_opacity=op)


def seg_bar(rh, x0, w, y, h):
    gold = Rectangle(width=max(w * rh, 0.01), height=h, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(P(x0 + w * rh / 2, y))
    teal = Rectangle(width=max(w * (1 - rh), 0.01), height=h, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to(P(x0 + w * rh + w * (1 - rh) / 2, y))
    out = Rectangle(width=w, height=h, stroke_color=TEXT, stroke_width=3).move_to(P(x0 + w / 2, y))
    return VGroup(gold, teal, out)


def intake_bar(x0, w, y, h=0.5):
    """Black intake bar (dark fill, light outline), starting at x0."""
    return Rectangle(width=w, height=h, stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=1).move_to(P(x0 + w / 2, y))


# ---- one population (computed), shared by the scenes that draw the cloud ------------------
_rng = np.random.default_rng(11)
POP_A = np.clip(_rng.normal(10, 3, 60), 4, 15.2)
POP_R = 0.5 + _rng.normal(0, 0.045, 60)
POP_RR = POP_A * POP_R             # reproduction
POP_SS = POP_A * (1 - POP_R)       # self


def pop_dots(O=O2, k=K, r=0.1, op=0.95):
    return VGroup(*[Dot(dp(a, s, O, k), radius=r, color=TEXT).set_opacity(op) for a, s in zip(POP_RR, POP_SS)])


def pop_lines(O=O2, k=K, op=0.45):
    return VGroup(*[Line(dp(0, a, O, k), dp(a, 0, O, k), color=GREY, stroke_width=2.5, stroke_opacity=op) for a in POP_A])


def trend(O=O2, k=K):
    m, b = np.polyfit(POP_RR, POP_SS, 1)
    x0, x1 = POP_RR.min() - 0.8, POP_RR.max() + 0.8
    return Line(dp(x0, m * x0 + b, O, k), dp(x1, m * x1 + b, O, k), color=GREY, stroke_width=6)


def shimmer(g, amp=0.025, speed=1.3):
    """Every dot of a group drifts a hair, so a held cloud is alive."""
    for i, d in enumerate(g):
        d._ph = 0.7 * i
        d._home = d.get_center().copy()

    def up(grp, dt):
        grp._t = getattr(grp, "_t", 0.0) + dt
        for d in grp:
            d.move_to(d._home + P(amp * np.sin(speed * grp._t + d._ph), amp * np.cos(speed * 0.8 * grp._t + 1.3 * d._ph)))
    g.add_updater(up)
    return g


def coin(r=0.22):
    return VGroup(Circle(radius=r, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.35),
                  Circle(radius=r * 0.55, stroke_color=GOLD, stroke_width=2))


def flip(c, run_time=0.9):
    return Rotate(c, angle=TAU * 2, axis=RIGHT, run_time=run_time)


def motes(scene, n=22, seed=1):
    """Faint drifting specks so a held picture is never frozen."""
    rg = np.random.default_rng(seed)
    g = VGroup(*[Dot(P(rg.uniform(-6.8, 6.8), rg.uniform(-3.8, 3.8)), radius=rg.uniform(0.03, 0.07), color=rg.choice([TEAL, GREY, GOLD])).set_opacity(rg.uniform(0.18, 0.35)) for _ in range(n)])
    for d in g:
        d.v = (rg.uniform(-0.15, 0.15), rg.uniform(0.1, 0.3))

    def up(grp, dt):
        for d in grp:
            d.shift(P(d.v[0] * dt, d.v[1] * dt))
            if d.get_y() > 3.9:
                d.shift(DOWN * 7.8)
    g.add_updater(up)
    g.set_z_index(-5)
    scene.add(g)
    return g


class SB(SpokenScene):
    def until(self, t):
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


class S00Title(TitleCard):
    LESSON = "Life histories and trade-offs"
    TITLE = "Why the Trade-off Hides"


# ----------------------------------------------------------------------------------------
class S01Question(SB):
    def construct(self):
        ax, xt, yt = axes2()
        ln = tline2(15, GREY)
        r = ValueTracker(0.5)
        dot = always_redraw(lambda: Dot(dp(15 * r.get_value(), 15 * (1 - r.get_value())), radius=0.17, color=TEXT))
        self.play(Create(ax[0]), Create(ax[1]), FadeIn(xt), FadeIn(yt), run_time=0.8)
        self.play(Create(ln), FadeIn(dot), run_time=0.8)
        tl = T("trade-off line", 30, GREY).move_to(P(0.9, 0.6))
        self.play(FadeIn(tl), r.animate.set_value(0.65), run_time=1.2)
        self.play(r.animate.set_value(0.4), run_time=0.9)
        self.at("If breeding can cost")
        self.play(r.animate.set_value(0.8), run_time=2.2, rate_func=smooth)
        self.at("why do birds")
        dots = pop_dots()
        xt2 = T("clutch size", 30, GOLD)
        xt2.move_to(O2 + P(AXL + 0.25 + xt2.width / 2, 0))
        yt2 = T("parent survival to next year", 28, TEAL)
        yt2.move_to(P(O2[0] + yt2.width / 2 - 0.2, O2[1] + AXL + 0.4))
        self.play(FadeOut(ln), FadeOut(tl), FadeOut(dot), Transform(xt, xt2), Transform(yt, yt2), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.04, run_time=2.4))
        shimmer(dots)
        self.at("At first glance")
        tr = trend()
        self.play(Create(tr), run_time=1.0)
        cap = VGroup(T("larger clutches,", 36, TEXT), T("better survival", 36, TEXT)).arrange(DOWN, buff=0.14).move_to(P(4.6, 0.8))
        sch = T("schematic", 24, GREY).move_to(P(5.7, -3.4))
        self.play(FadeIn(cap, shift=LEFT * 0.2), FadeIn(sch), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------
def right_cap(lines, y, color=TEXT, size=36, x=4.6):
    return VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, buff=0.12).move_to(P(x, y))


class S02Rich(SB):
    def construct(self):
        ax, xt, yt = axes2()
        self.add(ax, xt, yt)
        poor_l, rich_l = tline2(6, GREY), tline2(12, BIRD_C)
        pbar = intake_bar(2.7, 6 * 0.32, 2.4, 0.6)
        rbar = intake_bar(2.7, 12 * 0.32, 0.8, 0.6)
        plab = T("poor bird", 32, TEXT).next_to(pbar, UP, buff=0.12, aligned_edge=LEFT)
        rlab = T("rich bird", 32, BIRD_C).next_to(rbar, UP, buff=0.12, aligned_edge=LEFT)
        pd = Dot(dp(3, 3), radius=0.2, color=TEXT)
        rd = Dot(dp(6, 6), radius=0.2, color=BIRD_C)
        self.play(FadeIn(pbar, shift=RIGHT * 0.3), FadeIn(plab), run_time=0.9)
        self.play(Create(poor_l), run_time=1.4)
        self.at("Its intake is small")
        self.play(Indicate(pbar, color=TEXT, scale_factor=1.12), run_time=1.0)
        self.at("close to the corner")
        self.play(Indicate(poor_l, color=TEXT, scale_factor=1.0), run_time=1.2)
        self.at("A rich bird")
        self.play(GrowFromEdge(rbar, LEFT), FadeIn(rlab), run_time=1.3)
        self.at("Its line sits further")
        self.play(Create(rich_l), run_time=1.6)
        self.at("same downward slope")
        self.play(Indicate(poor_l, color=TEXT), Indicate(rich_l, color=BIRD_C), run_time=1.4)
        self.at("Same split")
        gp = VGroup(DashedLine(dp(3, 3), dp(3, 0), color=GOLD, stroke_width=3), DashedLine(dp(3, 3), dp(0, 3), color=TEAL, stroke_width=3))
        gr = VGroup(DashedLine(dp(6, 6), dp(6, 0), color=GOLD, stroke_width=3), DashedLine(dp(6, 6), dp(0, 6), color=TEAL, stroke_width=3))
        self.play(FadeIn(pd, scale=0.3), FadeIn(rd, scale=0.3), run_time=0.5)
        cap = right_cap(["same split,", "more of both"], -1.0, TEXT, 36)
        self.play(Create(gp), Create(gr), FadeIn(cap, shift=LEFT * 0.2), Indicate(rd, color=GOLD, scale_factor=1.8), run_time=1.0)
        idle(pd, 0.03), idle(rd, 0.03, phase=1.0)
        self.finish()


# ----------------------------------------------------------------------------------------
class S03Cloud(SB):
    def construct(self):
        ax, xt, yt = axes2()
        self.add(ax, xt, yt)
        lines = pop_lines()
        dots = pop_dots()
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.05, run_time=2.8))
        self.at("Each bird is a dot")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.04, run_time=1.8))
        self.at("every line slopes down")
        cap = right_cap(["every line", "slopes down"], 1.8, GREY, 38)
        self.play(FadeIn(cap, shift=LEFT * 0.2), lines.animate.set_stroke(opacity=0.6), run_time=1.0)
        self.play(lines.animate.set_stroke(opacity=0.3), run_time=1.0)
        self.at("Yet birds that take in more")
        top = sorted(range(60), key=lambda i: -POP_A[i])[:8]
        tg = VGroup(*[dots[i] for i in top])
        self.play(Indicate(tg, color=GOLD, scale_factor=1.9), run_time=1.4)
        self.at("on both axes")
        i0 = top[0]
        g = VGroup(DashedLine(dp(POP_RR[i0], POP_SS[i0]), dp(POP_RR[i0], 0), color=GOLD, stroke_width=3),
                   DashedLine(dp(POP_RR[i0], POP_SS[i0]), dp(0, POP_SS[i0]), color=TEAL, stroke_width=3))
        self.play(Create(g), run_time=1.0)
        self.at("So the cloud")
        tr = trend()
        cap2 = right_cap(["the cloud", "slopes up"], -0.6, TEXT, 38)
        self.play(FadeOut(g), lines.animate.set_stroke(opacity=0.12), Create(tr), FadeIn(cap2, shift=LEFT * 0.2), run_time=1.3)
        shimmer(dots)
        self.finish()


# ----------------------------------------------------------------------------------------
def person(x, y, c=TEXT):
    head = Circle(radius=0.2, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.9).move_to(P(x, y + 0.3))
    body = RoundedRectangle(corner_radius=0.18, width=0.6, height=0.4, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.5).move_to(P(x, y - 0.12))
    return VGroup(head, body)


def house_icon(x, y, c=GOLD, s=1.0):
    b = Square(side_length=0.36, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.6).move_to(P(x, y - 0.06))
    r = Polygon(P(x - 0.27, y + 0.12), P(x, y + 0.38), P(x + 0.27, y + 0.12), stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.9)
    return VGroup(b, r).scale(s, about_point=P(x, y))


def car_icon(x, y, c=TEAL, s=1.0):
    b = RoundedRectangle(corner_radius=0.08, width=0.7, height=0.26, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.6).move_to(P(x, y))
    t = RoundedRectangle(corner_radius=0.08, width=0.38, height=0.2, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.9).move_to(P(x, y + 0.2))
    w = VGroup(Dot(P(x - 0.2, y - 0.14), radius=0.07, color=TEXT), Dot(P(x + 0.2, y - 0.14), radius=0.07, color=TEXT))
    return VGroup(b, t, w).scale(s, about_point=P(x, y))


class S04Income(SB):
    def construct(self):
        motes(self, 18, 2)
        cap = T("van Noordwijk and de Jong, 1986", 32, TEXT).move_to(P(0, -3.35))
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=1.0)
        ys = [1.4, -0.3, -2.0]
        ws = [2.8, 4.9, 7.0]
        x0 = -4.6
        icons = [person(-5.7, y) for y in ys]
        bars = [seg_bar(0.5, x0, w, y, 0.9) for w, y in zip(ws, ys)]
        outs = [b[2] for b in bars]
        self.until(2.6)
        incl = T("income", 32, TEXT).move_to(P(-5.7, 2.4))
        self.play(FadeIn(incl), run_time=0.6)
        self.at("People with large incomes")
        for ic, o in zip(icons, outs):
            self.play(FadeIn(ic, shift=UP * 0.1), GrowFromEdge(o, LEFT), run_time=0.55)
        self.at("bigger houses")
        lh = VGroup(house_icon(0, 0), T("house", 36, GOLD)).arrange(RIGHT, buff=0.2).move_to(P(-2.2, 3.1))
        self.play(FadeIn(lh), *[GrowFromEdge(b[0], LEFT) for b in bars], run_time=1.0)
        self.at("newer cars")
        lc = VGroup(car_icon(0, 0), T("car", 36, TEAL)).arrange(RIGHT, buff=0.2).move_to(P(1.4, 3.1))
        self.play(FadeIn(lc), *[GrowFromEdge(b[1], RIGHT) for b in bars], run_time=1.0)
        self.wait(0.3)
        self.at("Yet for any one income")
        self.play(*[FadeOut(m) for m in (icons[0], icons[1], bars[0], bars[1], incl)], run_time=0.7)
        fx0, fw, fy, fh = -5.0, 10.0, 0.1, 1.4
        big = seg_bar(0.5, fx0, fw, fy, fh)
        self.play(icons[2].animate.move_to(P(-6.2, fy)), ReplacementTransform(bars[2], big), run_time=1.2)
        rh = ValueTracker(0.5)
        live = always_redraw(lambda: seg_bar(rh.get_value(), fx0, fw, fy, fh))
        hnd = always_redraw(lambda: Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1, stroke_width=1).scale(0.2).rotate(PI).move_to(P(fx0 + fw * rh.get_value(), fy - 0.8)))
        self.remove(big)
        self.add(live, hnd)
        self.at("money spent on the house")
        self.play(rh.animate.set_value(0.78), run_time=1.6, rate_func=smooth)
        self.at("for the car")
        self.play(Indicate(lc, color=TEAL, scale_factor=1.25), rh.animate.set_value(0.8), run_time=1.2)
        self.finish()


# ----------------------------------------------------------------------------------------
def cloud_world(scene, with_lines=False):
    ax, xt, yt = axes2()
    dots = pop_dots()
    tr = trend()
    scene.add(ax, xt, yt)
    if with_lines:
        scene.add(pop_lines(op=0.0))
    scene.add(dots, tr)
    return dots, tr


class S05Trap(SB):
    def construct(self):
        dots, tr = cloud_world(self)
        shimmer(dots)
        self.at("refute")
        stamp = VGroup(T("trade-off", 40, RED, weight=BOLD), T("refuted?", 40, RED, weight=BOLD)).arrange(DOWN, buff=0.1)
        box = RoundedRectangle(corner_radius=0.12, width=stamp.width + 0.5, height=stamp.height + 0.4, stroke_color=RED, stroke_width=4)
        st = VGroup(box, stamp).rotate(0.12).move_to(P(4.6, 1.8))
        self.play(FadeIn(st, scale=1.5), run_time=0.5)
        self.at("trade off")
        cross = Line(st.get_corner(DL) + P(-0.1, -0.1), st.get_corner(UR) + P(0.1, 0.1), color=RED, stroke_width=8)
        self.play(Create(cross), run_time=0.8)
        self.at("who took in more")
        lines = pop_lines(op=0.45)
        self.play(FadeIn(lines), run_time=0.8)
        top = sorted(range(60), key=lambda i: -POP_A[i])[:8]
        self.play(Indicate(VGroup(*[dots[i] for i in top]), color=GOLD, scale_factor=1.9), run_time=1.4)
        self.at("To test")
        hi = int(np.argsort(POP_A)[30])
        self.play(FadeOut(lines), FadeOut(st), FadeOut(cross), run_time=0.8)
        self.at("change breeding effort")
        d = dots[hi]
        d.clear_updaters() if False else None
        dots.clear_updaters()
        d.set_color(GOLD)
        a = POP_A[hi]
        ln = Line(dp(0, a), dp(a, 0), color=GOLD, stroke_width=4)
        cap = right_cap(["test: change", "effort at random"], 1.0, TEXT, 38)
        self.play(Create(ln), FadeIn(cap, shift=LEFT * 0.2), run_time=0.8)
        self.play(d.animate.move_to(dp(a * 0.8, a * 0.2)), run_time=1.0)
        self.play(d.animate.move_to(dp(a * 0.25, a * 0.75)), run_time=1.1)
        self.finish()


# ----------------------------------------------------------------------------------------
PAT = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1]
NX = [-5.5 + 2.2 * (i % 6) for i in range(12)]
NY = [1.1 if i < 6 else -1.7 for i in range(12)]


def nest(i):
    x, y = NX[i], NY[i]
    n = Ellipse(width=1.9, height=0.75, stroke_color=NEST_C, stroke_width=3, fill_color=NEST_C, fill_opacity=0.9).move_to(P(x, y))
    c1, c2 = chick(x - 0.28, y + 0.38, 0.16, BIRD_C), chick(x + 0.28, y + 0.38, 0.16, BIRD_C)
    return VGroup(n, c1, c2)


def extras(i):
    x, y = NX[i], NY[i]
    return VGroup(chick(x - 0.25, y + 0.85, 0.16), chick(x + 0.25, y + 0.85, 0.16))


class S06Experiment(SB):
    def construct(self):
        big = coin(0.9).move_to(P(0, 0.3))
        self.play(FadeIn(big, scale=0.5), run_time=0.5)
        self.play(flip(big, 1.5), run_time=1.5)
        self.at("Take a set of nests")
        nests = [nest(i) for i in range(12)]
        self.play(FadeOut(big), LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in nests], lag_ratio=0.1, run_time=1.8))
        self.at("At random")
        coins = [coin(0.26).move_to(P(NX[i], NY[i] + 1.3)) for i in range(12)]
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in coins], lag_ratio=0.03, run_time=0.4))
        self.play(LaggedStart(*[flip(c, 0.6) for c in coins], lag_ratio=0.04, run_time=1.0))
        self.at("add two chicks")
        ex = {i: extras(i) for i in range(12) if PAT[i]}
        anims = [FadeOut(c) for i, c in enumerate(coins) if not PAT[i]]
        anims += [FadeOut(c) for i, c in enumerate(coins) if PAT[i]]
        self.play(*anims, LaggedStart(*[FadeIn(e, shift=DOWN * 0.4) for e in ex.values()], lag_ratio=0.1), run_time=1.0)
        self.at("half of them")
        lg1 = VGroup(chick(0, 0, 0.12), T("enlarged", 36, GOLD)).arrange(RIGHT, buff=0.2).move_to(P(-3.0, 3.35))
        self.play(FadeIn(lg1), Indicate(VGroup(*ex.values()), color=GOLD, scale_factor=1.4), run_time=1.0)
        self.at("leave the other")
        ctrl = VGroup(*[nests[i] for i in range(12) if not PAT[i]])
        lg2 = VGroup(chick(0, 0, 0.12, BIRD_C), T("control", 36, BIRD_C)).arrange(RIGHT, buff=0.2).move_to(P(3.0, 3.35))
        self.play(FadeIn(lg2), Indicate(ctrl, color=BIRD_C, scale_factor=1.12), run_time=1.0)
        for e in ex.values():
            idle(e, 0.05, 2.0, phase=np.random.rand() * 3)
        self.at("Parents of enlarged")
        sch = T("schematic: parents may also forage harder", 28, GREY).move_to(P(0, -3.45))
        self.play(FadeIn(sch), run_time=0.8)
        self.at("more mouths")
        self.play(*[Indicate(e, color=GOLD, scale_factor=1.5) for e in ex.values()], run_time=1.4)
        self.finish()


# ----------------------------------------------------------------------------------------
def make_piles():
    """Random assignment of 12 parents (computed): the two groups differ a little in mean intake."""
    for sd in range(1, 400):
        rg = np.random.default_rng(sd)
        a = np.clip(rg.normal(10, 3, 12), 5, 15)
        idx = rg.permutation(12)
        g1, g2 = a[idx[:6]], a[idx[6:]]
        if abs(g1.mean() - g2.mean()) < 0.03 * a.mean() and g1.min() < 7 and g2.min() < 7 and g1.max() > 12 and g2.max() > 12:
            return g1, g2
    return a[:6], a[6:]


G1, G2 = make_piles()
PCX = (-4.1, 4.1)
CXS = [-1.8, 0.0, 1.8]
PY = [1.7, -0.3]


def pile(cx, vals, bar_color=TEXT):
    birds, bars = VGroup(), VGroup()
    for j, a in enumerate(vals):
        x, y = cx + CXS[j % 3], PY[j // 3]
        birds.add(songbird(0.62).move_to(P(x, y + 0.4)))
        bars.add(Rectangle(width=a * 0.11, height=0.3, stroke_color=TEXT, stroke_width=2, fill_color=INK, fill_opacity=1).move_to(P(x - 0.0, y - 0.35)))
    return birds, bars


class S07Random(SB):
    def construct(self):
        t1 = T("enlarged", 38, GOLD).move_to(P(PCX[0], 3.2))
        t2 = T("control", 38, BIRD_C).move_to(P(PCX[1], 3.2))
        b1, r1 = pile(PCX[0], G1)
        b2, r2 = pile(PCX[1], G2)
        c = coin(0.5).move_to(P(0, 1.6))
        self.play(FadeIn(t1), FadeIn(t2), run_time=0.5)
        self.at("a coin chose")
        self.play(FadeIn(c, scale=0.5), run_time=0.4)
        self.play(flip(c, 1.2), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in list(b1) + list(b2)], lag_ratio=0.1, run_time=1.2))
        self.play(FadeOut(c), run_time=0.15)
        for i, b in enumerate(list(b1) + list(b2)):
            idle(b, 0.04, 1.7, phase=i * 0.5)
        self.at("rich and poor parents")
        self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in list(r1) + list(r2)], lag_ratio=0.1, run_time=1.1))
        self.at("are balanced")
        m1 = Rectangle(width=G1.mean() * 0.25, height=0.4, stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=1).move_to(P(PCX[0], -1.9))
        m2 = Rectangle(width=G2.mean() * 0.25, height=0.4, stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=1).move_to(P(PCX[1], -1.9))
        ml = T("mean intake", 30, GREY).move_to(P(0, -1.9))
        self.play(GrowFromCenter(m1), GrowFromCenter(m2), FadeIn(ml), run_time=1.2)
        self.at("on average")
        cap = VGroup(T("random assignment: rich and poor", 32, TEXT), T("parents balanced on average", 32, TEXT)).arrange(DOWN, buff=0.12).move_to(P(0, -3.05))
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.8)
        self.at("A later difference")
        self.play(FadeOut(cap), FadeOut(ml), FadeOut(m1), FadeOut(m2), run_time=0.6)
        arr = DoubleArrow(P(-1.45, 0.5), P(1.45, 0.5), buff=0, color=TEXT, stroke_width=5, tip_length=0.2)
        dl = VGroup(T("difference in", 30, TEXT), T("parent survival", 30, TEXT)).arrange(DOWN, buff=0.08).move_to(P(0, 1.5))
        self.play(Create(arr), FadeIn(dl), run_time=1.0)
        self.at("extra chicks")
        ex = VGroup(chick(0, 0, 0.13), chick(0, 0, 0.13)).arrange(RIGHT, buff=0.12).move_to(P(PCX[0] + 1.6, 3.2))
        self.play(FadeIn(ex, scale=0.5), arr.animate.set_color(GOLD), run_time=0.8)
        self.at("allowing for chance")
        ch = T("allowing for chance", 32, GREY).move_to(P(0, -1.5))
        self.play(FadeIn(ch), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------
def calendar():
    page = Rectangle(width=3.2, height=1.9, stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=1)
    head = Rectangle(width=3.2, height=0.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).align_to(page, UP)
    lab = T("spring", 40, TEXT).move_to(page.get_center() + DOWN * 0.2)
    return VGroup(page, head, lab).move_to(P(0, 2.7))


def s08_world(q_op=1.0):
    cal = calendar()
    gl = VGroup(*[songbird(0.8).move_to(P(-5.9 + 1.7 * j, 0.5)) for j in range(3)])
    gr = VGroup(*[songbird(0.8).move_to(P(2.5 + 1.7 * j, 0.5)) for j in range(3)])
    tl = T("enlarged broods", 36, GOLD).move_to(P(-4.5, 1.7))
    tr = T("control", 36, BIRD_C).move_to(P(4.5, 1.7))
    ex = VGroup(*[chick(-3.15 - 0.4 * k, 1.1, 0.18) for k in range(2)])
    bl = Rectangle(width=3.6, height=1.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to(P(-4.5, -1.3))
    br = Rectangle(width=3.6, height=1.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to(P(4.5, -1.3))
    ql, qr = T("?", 50, GREY).move_to(bl), T("?", 50, GREY).move_to(br)
    q = T("?", 190, GREY, weight=BOLD).move_to(P(0, -0.2))
    chips = [chip("more", TEAL, 42).move_to(P(-3.8, -3.0)), chip("fewer", GOLD, 42).move_to(P(0, -3.0)), chip("the same", TEXT, 42).move_to(P(3.8, -3.0))]
    return dict(cal=cal, gl=gl, gr=gr, tl=tl, tr=tr, ex=ex, boxes=VGroup(bl, br, ql, qr), q=q, chips=chips)


class S08Predict(SB):
    def construct(self):
        w = s08_world()
        cal = w["cal"]
        page = VGroup(*cal)
        self.play(FadeIn(cal[0]), FadeIn(cal[1]), run_time=0.6)
        self.play(FadeIn(cal[2], scale=0.6), run_time=0.6)
        self.play(Rotate(cal[2], angle=TAU, axis=UP), run_time=1.2)
        for j, b in enumerate(list(w["gl"]) + list(w["gr"])):
            idle(b, 0.04, 1.7, phase=j * 0.6)
        self.at("Suppose extra chicks")
        self.play(FadeIn(w["gl"], shift=UP * 0.3), FadeIn(w["gr"], shift=UP * 0.3), FadeIn(w["tl"]), FadeIn(w["tr"]), run_time=1.2)
        self.at("cost parents")
        self.play(FadeIn(w["ex"], scale=0.5), run_time=0.8)
        self.play(Indicate(w["ex"], color=GOLD, scale_factor=1.5), run_time=1.2)
        self.at("What should happen")
        self.play(FadeIn(w["q"], scale=0.5), run_time=0.8)
        w["q"].add_updater(lambda m, dt: m.set_opacity(0.65 + 0.35 * np.sin(self.renderer.time * 4)))
        self.at("next spring")
        self.play(Indicate(cal, color=TEAL, scale_factor=1.12), FadeIn(w["boxes"]), run_time=1.2)
        self.at("Will more")
        self.play(FadeIn(w["chips"][0], scale=0.7), run_time=0.5)
        self.at("fewer")
        self.play(FadeIn(w["chips"][1], scale=0.7), run_time=0.5)
        self.at("the same")
        self.play(FadeIn(w["chips"][2], scale=0.7), run_time=0.5)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        w = s08_world()
        self.add(w["cal"], w["gl"], w["gr"], w["tl"], w["tr"], w["ex"], w["boxes"], *w["chips"])
        for j, b in enumerate(list(w["gl"]) + list(w["gr"])):
            idle(b, 0.04, 1.7, phase=j * 0.6)
        q = w["q"]
        self.add(q)
        t = ValueTracker(0.0)
        base = Circle(radius=1.3, color=GREY, stroke_width=3).move_to(q)
        ring = always_redraw(lambda: Arc(radius=1.3, start_angle=PI / 2, angle=-TAU * (1 - t.get_value()) + 1e-3,
                                         color=GOLD, stroke_width=8).move_to(q))
        self.add(base, ring)
        q.add_updater(lambda m, dt: m.set_opacity(0.65 + 0.35 * np.sin(self.renderer.time * 4)))
        self.play(t.animate.set_value(0.999), run_time=4.9, rate_func=linear)
        self.finish()


# ----------------------------------------------------------------------------------------
def doc_card(x, y, r=0.6):
    c = RoundedRectangle(corner_radius=0.06, width=r * 1.3, height=r * 1.7, stroke_color=TEXT, stroke_width=3, fill_color=INK, fill_opacity=1).move_to(P(x, y))
    ls = VGroup(*[Line(P(x - r * 0.4, y + dy), P(x + r * 0.4, y + dy), color=GREY, stroke_width=3) for dy in (0.25 * r, 0, -0.25 * r)])
    return VGroup(c, ls)


def breathe(m, amp=0.05, speed=2.2, phase=0.0):
    m._bt = phase
    m._bs = 1.0

    def up(mob, dt):
        mob._bt += dt
        s = 1 + amp * np.sin(speed * mob._bt)
        mob.scale(s / mob._bs)
        mob._bs = s
    m.add_updater(up)
    return m


class S10Reveal(SB):
    def construct(self):
        motes(self, 22, 5)
        rg = np.random.default_rng(3)
        cards = [doc_card(rg.uniform(-5.5, 5.5), rg.choice([-2.8, 2.8]) + rg.uniform(-0.3, 0.3)) for _ in range(6)]
        stack_pos = [P(-0.5 + 0.18 * i, 0.4 + 0.1 * i) for i in range(6)]
        self.at("A meta-analysis") if False else None
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cards], lag_ratio=0.12, run_time=1.2))
        self.at("gathered")
        self.play(LaggedStart(*[c.animate.move_to(p) for c, p in zip(cards, stack_pos)], lag_ratio=0.1, run_time=1.2))
        self.at("across 30")
        grid = VGroup(*[songbird(0.55).move_to(P(-5.6 + 1.25 * (i % 10), 1.6 - 1.5 * (i // 10))) for i in range(30)])
        head = T("30 bird species (eLife, 2025)", 40, TEXT).move_to(P(0, 3.2))
        self.play(FadeOut(VGroup(*cards)), LaggedStart(*[FadeIn(b, scale=0.4) for b in grid], lag_ratio=0.04, run_time=1.6), FadeIn(head))
        for i, b in enumerate(grid):
            idle(b, 0.03, 1.5, phase=i * 0.4)
        self.at("On average")
        # columns
        base_l = Line(P(-5.9, 0.6), P(-1.3, 0.6), color=GREY, stroke_width=3)
        base_r = Line(P(1.3, 0.6), P(5.9, 0.6), color=GREY, stroke_width=3)
        hl = VGroup(T("enlarged broods:", 36, GOLD), T("parent survival", 36, TEXT)).arrange(DOWN, buff=0.08).move_to(P(-3.4, 2.8))
        self.play(FadeOut(grid), FadeOut(head), FadeIn(hl), Create(base_l), run_time=1.0)
        self.at("survived a little less")
        down = Arrow(P(-3.4, 0.6), P(-3.4, -0.5), buff=0, color=GOLD, stroke_width=12, tip_length=0.3)
        small = T("small", 36, GOLD).move_to(P(-3.4, -1.2))
        self.play(GrowArrow(down), FadeIn(small), run_time=1.2)
        breathe(down, 0.06, 2.0)
        self.at("uncertain")
        wh = VGroup(Line(P(-3.4, 0.0), P(-3.4, -1.0), color=TEXT, stroke_width=5),
                    Line(P(-3.6, 0.0), P(-3.2, 0.0), color=TEXT, stroke_width=5),
                    Line(P(-3.6, -1.0), P(-3.2, -1.0), color=TEXT, stroke_width=5))
        sm2 = T("small, uncertain", 36, GOLD).move_to(P(-3.4, -1.5))
        self.play(FadeIn(wh), Transform(small, sm2), run_time=1.0)
        self.play(wh.animate.scale(1.35), run_time=0.8, rate_func=there_and_back)
        self.at("later breeding")
        lb = T("or on later breeding", 36, GOLD).move_to(P(-3.4, -2.4))
        self.play(FadeIn(lb, shift=UP * 0.1), run_time=0.8)
        self.play(Indicate(lb, color=GOLD, scale_factor=1.1), run_time=1.0)
        self.at("In the same data")
        hr = VGroup(T("naturally larger clutches:", 34, TEXT), T("parent survival", 34, TEXT)).arrange(DOWN, buff=0.08).move_to(P(3.6, 2.8))
        self.play(FadeIn(hr), Create(base_r), run_time=1.0)
        self.at("survived better")
        up_a = Arrow(P(3.6, 0.6), P(3.6, 1.9), buff=0, color=GREY, stroke_width=12, tip_length=0.3)
        self.play(GrowArrow(up_a), run_time=1.3)
        breathe(up_a, 0.05, 2.0)
        self.at("Two opposite signs")
        self.play(Indicate(down, color=GOLD, scale_factor=1.3), Indicate(up_a, color=TEXT, scale_factor=1.3), run_time=1.3)
        self.at("fits the cloud")
        sk = 0.13
        Oc = P(-0.95, -1.2)
        cd = VGroup(*[Dot(dp(a, s, Oc, sk), radius=0.06, color=TEXT).set_opacity(0.85) for a, s in zip(POP_RR, POP_SS)])
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in cd], lag_ratio=0.03, run_time=1.3))
        shimmer(cd, 0.03)
        self.at("though it does not prove")
        cap = T("fits the cloud; does not prove it", 36, TEXT).move_to(P(0, -3.4))
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------
class S11Rule(SB):
    def construct(self):
        motes(self, 14, 9)
        O3, k3, L3 = P(-6.4, -2.9), 0.33, 5.3
        xa = Arrow(O3, O3 + P(L3, 0), buff=0, color=GOLD, stroke_width=5, tip_length=0.2)
        ya = Arrow(O3, O3 + P(0, L3), buff=0, color=TEAL, stroke_width=5, tip_length=0.2)
        xl, yl = T("R", 34, GOLD).move_to(O3 + P(L3 + 0.35, 0)), T("S", 34, TEAL).move_to(O3 + P(0, L3 + 0.35))
        dots = pop_dots(O3, k3, 0.09)
        self.play(Create(xa), Create(ya), FadeIn(xl), FadeIn(yl), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.04, run_time=2.0))
        shimmer(dots, 0.02)
        self.at("rule")
        cap1 = T("correlation alone: ambiguous", 32, TEXT).move_to(P(-3.4, -3.5))
        tr = trend(O3, k3)
        self.play(Create(tr), FadeIn(cap1, shift=UP * 0.1), run_time=1.2)
        self.at("Birds that take in more")
        top = sorted(range(60), key=lambda i: -POP_A[i])[:8]
        self.play(Indicate(VGroup(*[dots[i] for i in top]), color=GOLD, scale_factor=2.0), run_time=1.5)
        self.play(Indicate(VGroup(*[dots[i] for i in top]), color=TEAL, scale_factor=2.0), run_time=1.5)
        self.at("Adding chicks at random")
        gl = VGroup(*[songbird(0.5).move_to(P(1.9 + 1.1 * (j % 2), 1.1 - 1.1 * (j // 2))) for j in range(4)])
        gr = VGroup(*[songbird(0.5).move_to(P(4.9 + 1.1 * (j % 2), 1.1 - 1.1 * (j // 2))) for j in range(4)])
        tl = T("enlarged", 32, GOLD).move_to(P(2.45, 2.5))
        tr2 = T("control", 32, BIRD_C).move_to(P(5.45, 2.5))
        c = coin(0.4).move_to(P(3.9, -0.8))
        self.add(c)
        for j, b in enumerate(list(gl) + list(gr)):
            idle(b, 0.04, 1.7, phase=j * 0.5)
        self.play(FadeIn(gl), FadeIn(gr), FadeIn(tl), FadeIn(tr2), flip(c, 0.9), run_time=0.9)
        self.at("tests")
        cap2 = T("random change: tests the cost", 32, TEXT).move_to(P(3.6, -3.5))
        self.play(FadeOut(c), FadeIn(cap2, shift=UP * 0.1), run_time=0.6)
        self.at("extra breeding")
        ex = VGroup(chick(3.75, 2.5, 0.15), chick(4.05, 2.5, 0.15))
        self.play(FadeIn(ex, scale=0.5), run_time=0.7)
        self.play(Indicate(ex, color=GOLD, scale_factor=1.5), run_time=1.0)
        self.at("And each bird may")
        few = [top[0], top[3], 20, 35, 50]
        lns = VGroup(*[Line(dp(0, POP_A[i], O3, k3), dp(POP_A[i], 0, O3, k3), color=GREY, stroke_width=4) for i in few])
        self.play(FadeOut(tr), LaggedStart(*[Create(l) for l in lns], lag_ratio=0.2, run_time=1.6))
        self.at("its own downward")
        self.play(Indicate(lns, color=TEXT, scale_factor=1.0), run_time=1.2)
        self.finish()


class S12End(EndCard):
    LINE = "Natural correlations can hide a trade-off; random manipulation tests the cost."
