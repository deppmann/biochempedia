"""Speciation film: Leaks That Multiply.

COLOUR MAP (whole film): PINK = M. lewisii (bumblebee, YELLOW), FRED = M. cardinalis (hummingbird, GREEN),
GOLD dots = gene flow, GREY gates = barriers, YELLOW dashed line = the zygote, TEAL = labels/concept.
"""
import types
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#F29CC3"
FRED = "#D7263D"
BEE = "#F5D547"
HUM = "#83C167"
LANE = 1.6
X0, X1, V = -5.0, 5.0, 1.7
GATES = [(-3.9, .45), (-2.4, .35), (-0.9, .5), (2.0, .6), (3.7, .6)]
LABS = [("habitat", 1, -3.9), ("pollinator", -1, -2.4), ("pollen &\nfertilization", 1, -1.3),
        ("hybrid seed\n& survival", -1, 2.0), ("hybrid\nfertility", 1, 3.7)]
ZX = 0.4


def bchip(text, color=BLUE, size=28, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def flower(color, r=.5):
    petals = [Circle(radius=0.5 * r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.8)
              .move_to([0.62 * r * np.cos(a), 0.62 * r * np.sin(a), 0]) for a in np.arange(5) * TAU / 5 + PI / 2]
    mid = Circle(radius=0.3 * r, stroke_width=0, fill_color=GOLD, fill_opacity=1)
    return VGroup(*petals, mid)


def tube(color=FRED):
    body = Polygon([-.5, .32, 0], [.5, .1, 0], [.5, -.1, 0], [-.5, -.32, 0], color=color, fill_opacity=.85, stroke_width=2.5)
    lip = Ellipse(width=.2, height=.64, color=color, fill_opacity=.95).move_to([-.5, 0, 0])
    return VGroup(body, lip)


def bee():
    body = Ellipse(width=.6, height=.36, color=BEE, fill_opacity=.9)
    wings = VGroup(*[Ellipse(width=.3, height=.4, color=TEXT, fill_opacity=.3).move_to([x, .22, 0]) for x in (-.12, .12)])
    stripes = VGroup(*[Line([x, -.14, 0], [x, .14, 0], color=BG, stroke_width=4) for x in (-.1, .08)])
    return VGroup(wings, body, stripes).scale(1.7)


def bird():
    body = Ellipse(width=.65, height=.3, color=HUM, fill_opacity=.85)
    wing = Polygon([0, .02, 0], [-.3, .65, 0], [.2, .1, 0], color=HUM, fill_opacity=.6)
    beak = Line([-.3, 0, 0], [-.85, .0, 0], color=HUM, stroke_width=3)
    return VGroup(body, wing, beak).scale(1.5)


def sway(m, amp=.06, f=1.1, ph=0.0):
    m.tt = ph
    m.cur = 0.0

    def up(mm, dt):
        mm.tt += dt
        a = amp * np.sin(mm.tt * f * TAU / 2)
        mm.rotate(a - mm.cur)
        mm.cur = a
    m.add_updater(up)


def bob(m, amp=.1, f=.6, ph=0.0):
    m.base = m.get_center().copy()
    m.tt = ph

    def up(mm, dt):
        mm.tt += dt
        mm.move_to(mm.base + UP * amp * np.sin(mm.tt * f * TAU))
    m.add_updater(up)


def gate_mob(x, p, color=GREY):
    half = p * LANE
    top = Rectangle(width=.32, height=1.95 - half, stroke_width=1.5, stroke_color=TEXT, fill_color=color, fill_opacity=.9)
    top.move_to([x, (1.95 + half) / 2, 0])
    bot = top.copy().move_to([x, -(1.95 + half) / 2, 0])
    return VGroup(top, bot)


class Flow:
    def __init__(self, seed=3, mode="fade"):
        self.gates, self.seed, self.mode = [], seed, mode
        self.P = (X1 - X0) / V + 0.4

    def add(self, k, x, p, active=True):
        g = types.SimpleNamespace(k=k, x=x, p=p, active=active)
        self.gates.append(g)
        return g


def step(d, dt):
    fl = d.flow
    d.t += dt
    P = fl.P
    c = int(d.t // P)
    tau = d.t - c * P
    if c != d.cyc:
        rng = np.random.RandomState((fl.seed * 1000 + d.k * 37 + c) % (2 ** 31))
        d.ys = rng.uniform(-LANE, LANE, 12)
        d.state, d.cyc, d.stopt = {}, c, None
    xr = X0 + V * tau
    gs = sorted(fl.gates, key=lambda g: g.x)
    stop = None
    for g in gs:
        if g.k not in d.state and xr >= g.x - .17:
            if g.active and abs(d.ys[g.k + 1]) >= g.p * LANE:
                d.state[g.k] = "stop"
                d.stopt = tau
            else:
                d.state[g.k] = "pass"
        if d.state.get(g.k) == "stop" and stop is None:
            stop = g
    kx = [X0] + [g.x for g in gs] + [X1]
    ky = [d.ys[0]] + [d.ys[g.k + 1] for g in gs] + [d.ys[11]]
    if stop is not None:
        x = stop.x - .17
        age = tau - d.stopt
        if fl.mode == "grey":
            col, op = GREY, .45
        else:
            col, op = GOLD, max(0.0, 1 - age / .9)
    else:
        x = xr
        col, op = GOLD, 1.0
    op *= min(1, tau / .4) * min(1, max(0, (P - tau) / .4))
    y = float(np.interp(x, kx, ky))
    d.move_to([x, y, 0])
    d.set_color(col)
    d.set_opacity(op)


class Stage:
    def __init__(self, sc, active=(), draw=None, labels=(), pol=False, nd=90, mode="fade", gspec=None,
                 dots=True, seed=3, plants=True):
        self.sc = sc
        self.gspec = gspec or GATES
        draw = active if draw is None else draw
        self.flow = Flow(seed, mode)
        self.gm, self.lab = {}, {}
        for i, (x, p) in enumerate(self.gspec):
            self.flow.add(i, x, p, i in active)
        for i in draw:
            self.gm[i] = gate_mob(*self.gspec[i])
            self.gm[i].set_z_index(1)
            sc.add(self.gm[i])
        for i in labels:
            self.lab[i] = self.label(i)
            sc.add(self.lab[i])
        self.pink = self.red = self.bee = self.bird = None
        if plants:
            self.pink = VGroup(*[flower(PINK, .6).move_to([-5.95, y, 0]) for y in (-1.35, 0, 1.35)])
            self.red = VGroup(*[tube().scale(1.5).move_to([5.85, y, 0]) for y in (-1.35, 0, 1.35)])
            for j, m in enumerate(list(self.pink) + list(self.red)):
                sway(m, ph=j * 1.3)
            sc.add(self.pink, self.red)
        if pol:
            self.add_pol(sc)
        self.dots = VGroup()
        if dots:
            for k in range(nd):
                d = Dot(radius=.115, color=GOLD)
                d.flow, d.k, d.t, d.cyc = self.flow, k, k * self.flow.P / nd, -1
                d.set_z_index(2)
                d.add_updater(step)
                d.update(0)
                self.dots.add(d)
            sc.add(self.dots)

    def label(self, i, color=TEXT):
        txt, sgn, x = LABS[i]
        return T(txt, 28, color).move_to([x, 2.65 * sgn, 0]).set_z_index(3)

    def add_pol(self, sc):
        self.bee = bee().move_to([-5.9, 3.0, 0])
        self.bird = bird().move_to([5.7, 3.0, 0])
        bob(self.bee, ph=0)
        bob(self.bird, ph=.5)
        sc.add(self.bee, self.bird)

    def on(self, i):
        self.flow.gates[i].active = True


def zyg_line():
    return DashedLine([ZX, -2.0, 0], [ZX, 3.15, 0], color=YELLOW, stroke_width=4, dash_length=.15)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Speciation"
    TITLE = "Leaks That Multiply"


class S01Hook(SpokenScene):
    def construct(self):
        st = Stage(self, active=(0, 1, 2), draw=(), dots=False, gspec=[(-2.5, .3), (0, .25), (2.5, .3)])
        brush = VGroup(Line([0, 0, 0], [.8, .8, 0], color=TEXT, stroke_width=7),
                       Ellipse(width=.35, height=.5, color=GOLD, fill_opacity=1).move_to([-.05, -.08, 0]))
        path = ArcBetweenPoints([-4.6, 1.2, 0], [4.6, 1.2, 0], angle=-.6)
        brush.move_to(path.get_start())
        by = T("crossed by hand", 34, TEXT).move_to([0, 2.85, 0])
        self.wait(.4)
        self.at("crossed by hand")
        self.add(brush)
        self.play(FadeIn(by), MoveAlongPath(brush, path), run_time=2.4, rate_func=linear)
        seed = Ellipse(width=.4, height=.6, color="#B5835A", fill_opacity=.95).move_to([0, 1.0, 0])
        lab = T("hybrid seed", 36, TEXT).move_to([0, -1.5, 0])
        self.at("hybrid seed")
        self.play(seed.animate.move_to([0, -.5, 0]), FadeIn(lab), run_time=1.0)
        self.at("So why do")
        self.play(FadeOut(brush), FadeOut(seed), FadeOut(lab), FadeOut(by), run_time=.6)
        self.add(st.dots)
        q = T("?", 150, TEAL, weight=BOLD).move_to([0, 2.4, 0])
        self.at("almost no genes")
        self.play(FadeIn(q, scale=.6), run_time=.8)
        self.finish()


class S02Flow(SpokenScene):
    def construct(self):
        st = Stage(self, gspec=[(-2.5, .3), (0, .25), (2.5, .3)])
        self.wait(.3)
        lab = T("gene flow (schematic)", 34, GOLD).move_to([0, 2.7, 0])
        self.at("Gene flow")
        self.play(FadeIn(lab), run_time=.7)
        arr = Arrow([-4.2, 2.05, 0], [4.2, 2.05, 0], color=GOLD, buff=0, stroke_width=7)
        self.at("movement of genes")
        self.play(GrowArrow(arr), run_time=1.8)
        cnt = VGroup(M("1,000", 46, GOLD), T("dots", 34, TEXT)).arrange(RIGHT, buff=.25).move_to([-3.7, -2.7, 0])
        self.at("Picture it as")
        self.play(FadeIn(cnt, shift=UP * .2), run_time=.8)
        ring = Circle(radius=.24, color=YELLOW, stroke_width=5)
        d5 = st.dots[7]
        ring.add_updater(lambda r: (r.move_to(d5.get_center()), r.set_stroke(opacity=float(d5.get_fill_opacity()))))
        self.add(ring)
        note = T("one dot = one chance to cross", 32, TEXT).move_to([2.6, -2.7, 0])
        self.at("Each gold dot")
        self.play(FadeIn(note), run_time=.8)
        self.finish()


class S03Barrier(SpokenScene):
    def construct(self):
        st = Stage(self, gspec=GATES)
        lab = T("reproductive barrier", 36, TEXT).move_to([0, 2.8, 0])
        self.at("A reproductive barrier")
        self.play(FadeIn(lab), run_time=.8)
        wall = Rectangle(width=.36, height=3.8, stroke_color=TEXT, stroke_width=3, fill_color="#2A2D38", fill_opacity=1).move_to([ZX, 0, 0])
        wall.set_z_index(1)
        wg = st.flow.add(7, ZX, 0.0, active=False)
        wl = T("one complete wall?", 34, TEXT).move_to([0, -2.8, 0])
        self.at("You might expect one wall")
        self.play(FadeOut(lab), FadeIn(wall, shift=DOWN * .3), FadeIn(wl), run_time=.9)
        wg.active = True
        cross = VGroup(Line([-.5, 1.3, 0], [.5, -1.3, 0]), Line([-.5, -1.3, 0], [.5, 1.3, 0])).set_stroke(RED, 9).move_to([ZX, 0, 0]).set_z_index(4)
        self.at("These monkey flowers have no such wall")
        self.play(Create(cross), run_time=1.0)
        self.wait(.6)
        wg.active = False
        self.play(FadeOut(wall), FadeOut(cross), FadeOut(wl), run_time=1.0)
        self.at("Each of their barriers")
        for i in (0, 1, 2):
            st.gm[i] = gate_mob(*st.gspec[i]).set_z_index(1)
            self.play(FadeIn(st.gm[i], shift=DOWN * .2), run_time=.7)
            st.on(i)
        self.finish()


class S04Gates(SpokenScene):
    def construct(self):
        st = Stage(self, active=(0, 1, 2))
        self.at("as gates")
        self.play(*[Indicate(st.gm[i], color=YELLOW, scale_factor=1.15) for i in (0, 1, 2)], run_time=1.2)
        self.at("where the plants grow")
        st.lab[0] = st.label(0, TEAL)
        self.play(FadeIn(st.lab[0]), Indicate(st.gm[0], color=YELLOW), run_time=.9)
        self.at("which pollinator")
        st.lab[1] = st.label(1, TEAL)
        st.add_pol(self)
        self.play(FadeIn(st.lab[1]), FadeIn(st.bee), FadeIn(st.bird), Indicate(st.gm[1], color=YELLOW), run_time=1.0)
        self.at("whether the other")
        st.lab[2] = st.label(2, TEAL)
        self.play(FadeIn(st.lab[2]), Indicate(st.gm[2], color=YELLOW), run_time=1.0)
        self.finish()


class S05Zygote(SpokenScene):
    def construct(self):
        st = Stage(self, active=(0, 1, 2), labels=(0, 1, 2), pol=True)
        for i in (0, 1, 2):
            st.lab[i].set_color(TEAL)
        z = zyg_line()
        zl = T("zygote", 32, YELLOW).move_to([ZX, 3.5, 0])
        self.at("Fertilization makes")
        self.play(Create(z), FadeIn(zl), run_time=1.6)
        bl = Line([-4.6, -3.2, 0], [.1, -3.2, 0], color=TEAL, stroke_width=5)
        pl = T("prezygotic", 30, TEAL).move_to([-2.25, -3.55, 0])
        self.at("Gates before it")
        self.play(Create(bl), FadeIn(pl), run_time=1.0)
        for i in (3, 4):
            st.gm[i] = gate_mob(*st.gspec[i]).set_z_index(1)
        self.at("Gates after it")
        self.play(FadeIn(st.gm[3], shift=DOWN * .2), run_time=.7)
        st.on(3)
        st.lab[3] = st.label(3)
        self.at("hybrids that fail")
        self.play(FadeIn(st.lab[3]), run_time=.7)
        self.at("or are sterile")
        self.play(FadeIn(st.gm[4], shift=DOWN * .2), run_time=.7)
        st.on(4)
        st.lab[4] = st.label(4)
        self.play(FadeIn(st.lab[4]), run_time=.6)
        br = Line([.8, -3.2, 0], [4.6, -3.2, 0], color=RED, stroke_width=5)
        po = T("postzygotic", 30, RED).move_to([2.7, -3.55, 0])
        self.at("are post zygotic")
        self.play(Create(br), FadeIn(po), run_time=1.0)
        self.finish()


class S06Sequence(SpokenScene):
    def construct(self):
        st = Stage(self, active=(0, 1, 2, 3, 4), labels=(0, 1, 2), pol=True)
        for i in (0, 1, 2):
            st.lab[i].set_color(TEAL)
        self.at("Here is the key")
        self.play(Indicate(st.gm[0], color=YELLOW), Indicate(st.gm[1], color=YELLOW), run_time=1.2)
        st.flow.mode = "grey"
        self.at("When gates act")
        self.play(LaggedStart(*[Indicate(st.gm[i], color=YELLOW, scale_factor=1.1) for i in (0, 1, 2, 3, 4)], lag_ratio=.35), run_time=2.2)
        box = SurroundingRectangle(st.gm[1], color=YELLOW, buff=.15, stroke_width=5)
        self.at("each acts only on what")
        self.play(Create(box), run_time=.8)
        self.at("let through")
        self.wait(.5)
        self.play(FadeOut(box), run_time=.4)
        st.bee.clear_updaters()
        self.at("A pollinator cannot carry")
        self.play(st.bee.animate.move_to([-4.6, 1.1, 0]), run_time=1.3)
        self.play(st.bee.animate.move_to([-5.9, 3.0, 0]), run_time=1.2)
        bob(st.bee)
        far = DashedLine([-4.7, 3.3, 0], [4.7, 3.3, 0], color=TEXT, stroke_width=4)
        x = VGroup(Line([-.3, .3, 0], [.3, -.3, 0]), Line([-.3, -.3, 0], [.3, .3, 0])).set_stroke(RED, 8).move_to([0, 3.3, 0])
        self.at("never grow near")
        self.play(Create(far), run_time=1.2)
        self.play(Create(x), run_time=.5)
        self.finish()


def cards():
    return [bchip("70%?", TEAL, 30).move_to([-4.3, -3.2, 0]),
            bchip("210%?", TEAL, 30).move_to([-1.0, -3.2, 0]),
            bchip("something else?", TEAL, 30).move_to([3.3, -3.2, 0])]


class S07Predict(SpokenScene):
    def construct(self):
        st = Stage(self, active=(), draw=(), gspec=[(-2.6, .3), (0, .3), (2.6, .3)], nd=90, seed=5)
        self.at("Try three")
        for i in (0, 1, 2):
            st.gm[i] = gate_mob(*st.gspec[i]).set_z_index(1)
        cnt = M("1,000", 44, GOLD).move_to([-3.9, -2.3, 0])
        self.play(*[FadeIn(st.gm[i], shift=DOWN * .2) for i in (0, 1, 2)], FadeIn(cnt), run_time=1.0)
        for i in (0, 1, 2):
            st.on(i)
        pl = VGroup(*[M("70%", 40, TEXT).move_to([x, 2.5, 0]) for x in (-2.6, 0, 2.6)])
        self.at("each stopping 70")
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * .2) for p in pl], lag_ratio=.4), run_time=1.5)
        cs = cards()
        self.at("Together, do they stop")
        self.play(FadeIn(cs[0], shift=UP * .2), run_time=.8)
        self.at("More than a hundred")
        self.play(FadeIn(cs[1], shift=UP * .2), run_time=.8)
        self.at("Something else")
        self.play(FadeIn(cs[2], shift=UP * .2), run_time=.8)
        self.finish()


def demo_full(sc):
    st = Stage(sc, active=(0, 1, 2), gspec=[(-2.6, .3), (0, .3), (2.6, .3)], nd=90, seed=5)
    pl = VGroup(*[M("70%", 40, TEXT).move_to([x, 2.5, 0]) for x in (-2.6, 0, 2.6)])
    cs = VGroup(*cards())
    cnt = M("1,000", 44, GOLD).move_to([-3.9, -2.3, 0])
    sc.add(pl, cs, cnt)
    return st, pl, cs, cnt


class S08Pause(NarratedScene):
    def construct(self):
        st, pl, cs, cnt = demo_full(self)
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=.4, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()), color=YELLOW, stroke_width=8).move_to([6.1, 3.2, 0]))
        self.add(ring)
        self.play(tr.animate.set_value(1), run_time=5, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        st, pl, cs, cnt = demo_full(self)
        xs = [-1.3, 1.3, 3.9]
        vals = ["300", "90", "27"]
        ns = [M(v, 44, GOLD).move_to([x, -2.3, 0]) for v, x in zip(vals, xs)]
        self.at("Watch the counter")
        self.play(Indicate(cnt, color=YELLOW), run_time=1.2)
        self.at("Each gate leaves less")
        self.play(FadeIn(ns[0], shift=UP * .2), run_time=.8)
        self.at("for the next one")
        self.play(FadeIn(ns[1], shift=UP * .2), run_time=.8)
        self.at("In the end")
        self.play(FadeIn(ns[2], shift=UP * .2), run_time=.8)
        fin = bchip("stopped: 97.3%", GREEN, 30).move_to([3.3, -3.2, 0])
        self.at("about 97")
        self.play(FadeOut(cs[2]), FadeIn(fin), run_time=.8)
        bad = bchip("210% is impossible", RED, 30).move_to([-1.0, -3.2, 0])
        self.at("That stops more than")
        self.play(FadeOut(cs[0]), Transform(cs[1], bad), run_time=1.0)
        self.at("still pass")
        self.play(Indicate(ns[2], color=YELLOW, scale_factor=1.4), run_time=1.5)
        self.finish()


class S10Rule(SpokenScene):
    def construct(self):
        widths = [1, .3, .09, .027]
        ys = [1.9, 1.0, .1, -.8]
        names = ["start", "gate 1", "gate 2", "gate 3"]
        vals = ["1", "0.3", "0.09", "0.027"]
        rows = []
        for i in range(4):
            w = max(8.5 * widths[i], .03)
            b = Rectangle(width=w, height=.6, stroke_width=0, fill_color=GOLD, fill_opacity=.9).move_to([-4.9 + w / 2, ys[i], 0])
            n = T(names[i], 28, TEXT).move_to([-5.8, ys[i], 0])
            v = M(vals[i], 34, GOLD).next_to(b, RIGHT, buff=.2)
            rows.append(VGroup(n, b, v))
        self.at("That is the rule")
        self.play(FadeIn(rows[0], shift=RIGHT * .3), run_time=1.2)
        eq = M("left = 0.3 × 0.3 × 0.3 = 0.027", 40, TEXT).move_to([0, 3.05, 0])
        self.at("The fractions")
        self.play(Write(eq), run_time=1.8)
        self.at("multiply")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * .3) for r in rows[1:]], lag_ratio=.6), run_time=2.2)
        gen = M("gene flow left = (1 − RI1) × (1 − RI2) × (1 − RI3)", 28, TEAL).move_to([0, -2.8, 0])
        ri = T("RI = share of what is left that a barrier stops", 28, TEXT).move_to([0, -3.4, 0])
        self.at("Several leaky gates")
        self.play(FadeIn(gen, shift=UP * .2), run_time=1.0)
        self.at("block nearly all")
        self.play(Indicate(rows[3], color=YELLOW, scale_factor=1.2), FadeIn(ri), run_time=1.5)
        wrong = M("70% + 70% + 70% = 210%", 36, TEXT).move_to([0, -1.85, 0])
        self.at("Adding their")
        self.play(Write(wrong), run_time=1.5)
        strike = Line(wrong.get_left() + LEFT * .1, wrong.get_right() + RIGHT * .1, color=RED, stroke_width=8)
        self.at("is wrong")
        self.play(Create(strike), run_time=.8)
        self.at("the sum can pass")
        self.play(Indicate(wrong, color=RED, scale_factor=1.15), run_time=1.5)
        self.finish()


def real_stage(sc, labels=(), zyg=True, pol=True, **kw):
    st = Stage(sc, active=(0, 1, 2, 3, 4), labels=labels, pol=pol, **kw)
    zl = None
    if zyg:
        zl = VGroup(zyg_line(), T("zygote", 32, YELLOW).move_to([ZX, 3.5, 0]))
        sc.add(zl)
    return st, zl


class S11Study(SpokenScene):
    def construct(self):
        st, zl = real_stage(self)
        cap = T("Ramsey, Bradshaw & Schemske, 2003", 32, TEXT).move_to([-0.3, -3.55, 0])
        self.at("Bradshaw")
        self.play(FadeIn(cap), run_time=.8)
        names = [("range\noverlap", 0, -3.9, 1), ("pollinator\nisolation", 1, -2.4, -1), ("pollen\nprecedence", 2, -1.3, 1)]
        for phrase, (txt, i, x, sgn) in zip(["measured these gates", "one stage", "at a time"], names):
            t = T(txt, 28, TEAL).move_to([x, 2.65 * sgn, 0])
            self.at(phrase)
            self.play(FadeIn(t), Indicate(st.gm[i], color=YELLOW), run_time=.8)
        f1 = T("F1 fitness:\ngermination to fertility", 28, RED).move_to([2.85, -2.7, 0])
        self.at("They worked")
        self.play(FadeIn(f1), Indicate(st.gm[3], color=YELLOW), Indicate(st.gm[4], color=YELLOW), run_time=1.2)
        self.at("Every gate")
        self.play(LaggedStart(*[Indicate(st.gm[i], color=YELLOW, scale_factor=1.2) for i in range(5)], lag_ratio=.3), run_time=2.0)
        self.finish()


class S12Early(SpokenScene):
    def construct(self):
        st, zl = real_stage(self, labels=(0, 1))
        sch = T("schematic", 28, TEXT).move_to([5.7, -3.5, 0])
        self.add(sch)
        self.at("Where the plants grow")
        self.play(Indicate(st.gm[0], color=YELLOW), run_time=1.0)
        self.at("which pollinator")
        self.play(Indicate(st.gm[1], color=YELLOW), run_time=1.0)
        shade = Rectangle(width=5.0, height=3.9, stroke_width=0, fill_color=YELLOW, fill_opacity=.12).move_to([-2.1, 0, 0])
        self.at("came first")
        self.play(FadeIn(shade), run_time=1.0)
        msg = T("most isolation before any hybrid forms", 30, YELLOW).move_to([0, -3.4, 0])
        self.at("Most of the stream")
        self.play(FadeIn(msg, shift=UP * .2), run_time=1.2)
        self.at("before any hybrid")
        self.play(Indicate(zl[0], color=YELLOW), run_time=1.2)
        self.finish()


class S13Total(SpokenScene):
    def construct(self):
        st, zl = real_stage(self, zyg=False)
        l1 = T("measured barriers together:", 32, TEXT).move_to([0, 3.35, 0])
        l2 = VGroup(M("99.87%", 44, GOLD), T("of gene flow blocked", 36, TEXT)).arrange(RIGHT, buff=.3).move_to([0, 2.7, 0])
        note = T("estimate; mean of the two directions", 28, TEXT).move_to([0, -3.1, 0])
        self.at("Together")
        self.play(FadeIn(l1), run_time=.8)
        self.at("measured barriers")
        self.play(*[st.gm[i].animate.set_color(YELLOW) for i in range(5)], run_time=1.0)
        self.at("on average")
        self.play(FadeIn(note), run_time=.8)
        self.at("almost all gene flow")
        self.play(FadeIn(l2, shift=UP * .2), run_time=1.0)
        self.at("No one gate")
        self.play(*[Indicate(st.gm[i], color=YELLOW, scale_factor=1.15) for i in range(5)], run_time=1.5)
        self.finish()


class S14Hybrids(SpokenScene):
    def construct(self):
        st, zl = real_stage(self, labels=(3, 4))
        q = T("what if hybrids were fertile?", 32, TEXT).move_to([3.1, -3.5, 0])
        self.at("does not need")
        self.play(st.gm[3].animate.set_opacity(.25), st.gm[4].animate.set_opacity(.25),
                  st.lab[3].animate.set_opacity(.4), st.lab[4].animate.set_opacity(.4), FadeIn(q), run_time=1.2)
        self.at("When the early gates")
        self.play(*[Indicate(st.gm[i], color=YELLOW, scale_factor=1.15) for i in (0, 1, 2)], run_time=1.5)
        few = T("few hybrids form", 32, YELLOW).move_to([-3.0, -3.3, 0])
        self.at("few hybrids form")
        self.play(FadeIn(few), run_time=.9)
        self.finish()


class S15Takeaway(SpokenScene):
    def construct(self):
        st, zl = real_stage(self)
        wall = Rectangle(width=.36, height=3.8, stroke_color=TEXT, stroke_width=3, fill_color="#2A2D38", fill_opacity=.5).move_to([ZX, 0, 0])
        x = VGroup(Line([-.5, 1.3, 0], [.5, -1.3, 0]), Line([-.5, -1.3, 0], [.5, 1.3, 0])).set_stroke(RED, 9).move_to([ZX, 0, 0])
        self.at("So two species")
        self.play(FadeIn(wall), Create(x), run_time=1.2)
        self.at("perfect wall")
        self.wait(.5)
        self.play(FadeOut(wall), FadeOut(x), run_time=.8)
        self.at("Several leaky gates")
        self.play(LaggedStart(*[Indicate(st.gm[i], color=YELLOW, scale_factor=1.15) for i in range(5)], lag_ratio=.4), run_time=2.5)
        tr = T("a trickle", 36, GOLD).move_to([4.3, -2.6, 0])
        self.at("to a trickle")
        self.play(FadeIn(tr, shift=UP * .2), run_time=.9)
        self.finish()


class S16End(EndCard):
    LINE = "Each barrier blocks only what earlier barriers let through, so leaks multiply."
