"""Speciation film 2: Isolation Follows Ecology. Colour map and Stage/gate helpers copied from film 1 (../scenes.py).
OLIVE = benthic stickleback, SBLUE = limnetic, PINK/FRED flowers, GOLD dots = gene flow, GREY gates = barriers."""
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



# ------------------------------------------------------------------ chapter 2 helpers
OLIVE = "#8A9A3B"
SBLUE = "#9CC4E4"
ANC = "#C9C3A8"
NECT = "#9ADBE8"
WATER = "#1B3A55"
SAND = "#6B6A3A"


def fish(color, deep=False, s=1.0):
    """Cartoon stickleback facing right. Benthic: deep-bodied. Limnetic: slender. Schematic."""
    h = 0.62 if deep else 0.34
    body = Ellipse(width=1.3, height=h, stroke_width=2, stroke_color=TEXT, fill_color=color, fill_opacity=.95)
    tail = Polygon([-.55, 0, 0], [-.95, h * .6, 0], [-.95, -h * .6, 0], stroke_width=2, stroke_color=TEXT,
                   fill_color=color, fill_opacity=.95)
    fin = Polygon([-.15, h / 2 - .02, 0], [.15, h / 2 - .02, 0], [0, h / 2 + .2, 0], stroke_width=2,
                  stroke_color=TEXT, fill_color=color, fill_opacity=.95)
    eye = Dot([.42, .05, 0], radius=.05, color=BG)
    g = VGroup(tail, fin, body, eye)
    return g.scale(s)


def face_left(f):
    f.flip(UP)
    return f


def wig(m, ax=.12, ay=.08, f=.5, ph=0.0):
    """Incremental drift (composes with other moves)."""
    m.tt = ph
    m.cur = np.zeros(3)

    def up(mm, dt):
        mm.tt += dt
        new = np.array([ax * np.sin(mm.tt * f * TAU), ay * np.sin(mm.tt * f * TAU * 1.3 + 1), 0])
        mm.shift(new - mm.cur)
        mm.cur = new
    m.add_updater(up)
    return m


def lake(cx, cy, w, h, sand=True):
    box = RoundedRectangle(corner_radius=.25, width=w, height=h, stroke_color=TEAL, stroke_width=3,
                           fill_color=WATER, fill_opacity=.45).move_to([cx, cy, 0])
    g = VGroup(box)
    if sand:
        g.add(Rectangle(width=w - .3, height=.4, stroke_width=0, fill_color=SAND, fill_opacity=.55)
              .move_to([cx, cy - h / 2 + .3, 0]))
    return g


def hgate(cx, y, w=2.6, gap=.5, color=GREY):
    seg = (w - gap) / 2
    a = Rectangle(width=seg, height=.26, stroke_width=1.5, stroke_color=TEXT, fill_color=color, fill_opacity=.95)
    b = a.copy()
    a.move_to([cx - gap / 2 - seg / 2, y, 0])
    b.move_to([cx + gap / 2 + seg / 2, y, 0])
    return VGroup(a, b).set_z_index(3)


def tag(text, mob, color=TEXT, size=28, d=UP, buff=.18):
    t = T(text, size, color)
    t.add_updater(lambda m: m.next_to(mob, d, buff=buff))
    t.update(0)
    return t


def gold_stream(sc, y_top, y_bot, x, n=12, thin=None, spread=1.0):
    """Gold dots shuttling between two groups; their opacity follows `thin` (a ValueTracker)."""
    ds = VGroup()
    for k in range(n):
        d = Dot(radius=.1, color=GOLD)
        d.ph = k / n
        d.xo = x + np.sin(k * 2.3) * spread
        d.tt = 0.0

        def up(m, dt):
            m.tt += dt
            p = (m.tt * .22 + m.ph) % 1
            m.move_to([m.xo, y_top + (y_bot - y_top) * p, 0])
            m.set_opacity(min(1, p * 5, (1 - p) * 5) * thin.get_value())
        d.add_updater(up)
        d.update(0)
        ds.add(d)
    sc.add(ds)
    return ds


def ring_timer(tr):
    return always_redraw(lambda: Arc(radius=.4, start_angle=PI / 2, angle=-TAU * (1 - tr.get_value()),
                                     color=YELLOW, stroke_width=8).move_to([6.1, 3.2, 0]))


# ---- the 2 x 2 grid of the mating trials (shared by scenes 7, 8, 9, 10, 11) ----
GCX = [-2.9, 0.1]       # columns: same lake, different lakes
GRY = [0.5, -1.3]       # rows: same form, different form
GW, GH = 2.9, 1.65
TANK_C = (4.55, -0.1)


def cell_tank(ci, ri, turned=False):
    """A mini tank icon with two fish. Same-form rows: two olive; different-form: olive + silver."""
    cx, cy = GCX[ci], GRY[ri]
    box = Rectangle(width=2.4, height=1.15, stroke_color=TEAL, stroke_width=2, fill_color=WATER, fill_opacity=.5).move_to([cx, cy, 0])
    a = fish(OLIVE, True, .42).move_to([cx - .55, cy - .05, 0])
    b = face_left(fish(OLIVE if ri == 0 else SBLUE, ri == 0, .42)).move_to([cx + .55, cy - .05, 0])
    if turned:
        a.flip(UP).shift(LEFT * .25)
        b.flip(UP).shift(RIGHT * .25)
    return VGroup(box, a, b)


def grid_frame(labels=True):
    g = VGroup()
    for ci in range(2):
        for ri in range(2):
            g.add(Rectangle(width=GW, height=GH, stroke_color=TEXT, stroke_width=3, fill_opacity=0)
                  .move_to([GCX[ci], GRY[ri], 0]))
    out = [g]
    if labels:
        rl = [T("same\nform", 28, TEXT, line_spacing=.6).move_to([-5.5, GRY[0], 0]),
              T("different\nform", 28, TEXT, line_spacing=.6).move_to([-5.5, GRY[1], 0])]
        cl = [T("same\nlake", 28, TEXT, line_spacing=.6).move_to([GCX[0], 2.05, 0]),
              T("different\nlakes", 28, TEXT, line_spacing=.6).move_to([GCX[1], 2.05, 0])]
        out += rl + cl
    return VGroup(*out)


def big_tank(cx=TANK_C[0], cy=TANK_C[1], w=4.6, h=3.4):
    return lake(cx, cy, w, h, sand=False)


class Grid:
    """Builds the grid with tank icons; state 'lit' = result of the trials."""
    def __init__(self, sc, icons=True, lit=False, anim=False):
        self.frame = grid_frame()
        self.tanks = {}
        sc.add(self.frame)
        if icons:
            for ci in range(2):
                for ri in range(2):
                    t = cell_tank(ci, ri, turned=lit and ri == 1)
                    self.tanks[(ci, ri)] = t
                    sc.add(t)
        self.glow = {}
        if lit:
            for ci in range(2):
                for ri in range(2):
                    r = Rectangle(width=GW, height=GH, stroke_width=0, fill_color=GREEN if ri == 0 else BG,
                                  fill_opacity=.32 if ri == 0 else .55).move_to([GCX[ci], GRY[ri], 0])
                    r.set_z_index(0.5)
                    self.glow[(ci, ri)] = r
                    sc.add(r)
            for k, t in self.tanks.items():
                t.set_z_index(1 if k[1] == 0 else 0.6)
        for t in self.tanks.values():
            for f in t[1:]:
                wig(f, .05, .04, .6, np.random.rand() * 6)


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Speciation"
    TITLE = "Isolation Follows Ecology"


class S01Hook(SpokenScene):
    def construct(self):
        tank = lake(0, -.2, 11.6, 5.6)
        self.add(tank)
        a = fish(OLIVE, True, 1.5).move_to([-4.5, -1.2, 0])
        b = face_left(fish(OLIVE, True, 1.5)).move_to([4.5, -1.2, 0])
        wig(a, .1, .1, .5, 0)
        wig(b, .1, .1, .5, 2)
        la = tag("lake A", a, TEXT, 30)
        lb = tag("lake B", b, TEXT, 30)
        self.add(a, b)
        self.play(a.animate.shift(RIGHT * .5), b.animate.shift(LEFT * .5), FadeIn(la), FadeIn(lb), run_time=1.2)
        self.at("isolation should follow")
        t1 = T("same habitat: the bottom", 34, OLIVE).move_to([0, 3.3, 0])
        self.play(FadeIn(t1), a.animate.shift(RIGHT * 1.2), b.animate.shift(LEFT * 1.2), run_time=4.0, rate_func=linear)
        self.at("So what happens")
        q = T("?", 150, TEAL, weight=BOLD).move_to([0, .6, 0])
        self.play(FadeIn(q, scale=.5), a.animate.shift(RIGHT * 1.0), b.animate.shift(LEFT * 1.0), run_time=3.0, rate_func=linear)
        self.at("meet")
        self.play(Indicate(q, color=YELLOW), run_time=1.5)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        st = Stage(self, active=(0, 1, 2), labels=(), pol=True, gspec=GATES)
        self.wait(.5)
        self.at("habitat and pollinators")
        st.lab[0] = st.label(0, TEAL)
        st.lab[1] = st.label(1, TEAL)
        self.play(FadeIn(st.lab[0]), FadeIn(st.lab[1]),
                  Indicate(st.gm[0], color=YELLOW, scale_factor=1.15), Indicate(st.gm[1], color=YELLOW, scale_factor=1.15), run_time=1.6)
        q1 = T("?", 64, YELLOW, weight=BOLD).move_to([-3.9, 3.35, 0])
        q2 = T("?", 64, YELLOW, weight=BOLD).move_to([-2.4, -3.3, 0])
        self.at("Were those gates built")
        self.play(FadeIn(q1, scale=.5), FadeIn(q2, scale=.5), run_time=.8)
        for q in (q1, q2):
            q.base = q.get_center().copy()
            wig(q, 0, .08, .8, 0)
        self.at("Or did they come free")
        self.play(Indicate(st.gm[0], color=YELLOW), Indicate(st.gm[1], color=YELLOW), run_time=1.6)
        self.finish()


def split_world(sc, thin, shown=0, arrows=True, labels=True, gate=0):
    """Side-view lake: groups of fish heading to the bottom and to open water. shown: 0 = one ancestral group, 1 = split."""
    lk = lake(0, 0, 12.2, 7.0)
    sc.add(lk)
    top = [fish(SBLUE, False, 1.05).move_to([x, y, 0]) for x, y in [(-3.2, 1.6), (-1.7, 2.3), (-.2, 1.4), (-2.4, .6)]]
    bot = [fish(OLIVE, True, 1.05).move_to([x, y, 0]) for x, y in [(-3.0, -1.9), (-1.5, -2.4), (.2, -1.7), (-2.3, -1.1)]]
    for i, f in enumerate(top + bot):
        wig(f, .12, .08, .4, i * 1.1)
    sc.add(*top, *bot)
    extras = VGroup()
    if labels:
        extras.add(T("open water", 30, SBLUE).move_to([-4.6, 2.6, 0]), T("bottom", 30, OLIVE).move_to([-4.6, -2.65, 0]))
    sc.add(extras)
    return lk, top, bot, extras


class S03Selection(SpokenScene):
    def construct(self):
        thin = ValueTracker(1.0)
        lk = lake(0, 0, 12.2, 7.0)
        self.add(lk)
        pos = [(-2.2, .6), (-.8, -.2), (.6, .5), (-1.5, -1.0), (0, -.9), (-.3, 1.2)]
        anc = [fish(ANC, False, 1.05).move_to([x, y, 0]) for x, y in pos]
        for i, f in enumerate(anc):
            wig(f, .12, .08, .4, i * 1.1)
        self.add(*anc)
        pl = T("one population", 32, TEXT).move_to([-1.1, -2.6, 0])
        self.play(FadeIn(pl), run_time=.8)
        self.at("One answer")
        dsel = T("divergent selection", 34, TEAL)
        dsel.move_to([3.6, 2.9, 0])
        sel_note = T("favours different\ntraits in different\nplaces", 24, TEXT, line_spacing=.7).move_to([2.6, -1.7, 0])
        self.play(FadeIn(dsel), FadeOut(pl), run_time=1.0)
        self.at("Two populations adapt")
        up = Arrow([4.2, .5, 0], [4.2, 2.4, 0], color=TEAL, buff=0, stroke_width=8)
        dn = Arrow([4.2, -.5, 0], [4.2, -2.4, 0], color=TEAL, buff=0, stroke_width=8)
        ow = T("open water", 30, SBLUE).move_to([-4.6, 2.6, 0])
        bt = T("bottom", 30, OLIVE).move_to([-4.6, -2.65, 0])
        tops = [fish(SBLUE, False, 1.05).move_to([x, y, 0]) for x, y in [(-3.2, 1.7), (-1.7, 2.3), (-.2, 1.5)]]
        bots = [fish(OLIVE, True, 1.05).move_to([x, y, 0]) for x, y in [(-3.0, -1.9), (-1.5, -2.4), (.2, -1.7)]]
        for i, f in enumerate(tops + bots):
            wig(f, .12, .08, .4, i * 1.1)
        self.play(*[ReplacementTransform(anc[i], tops[i]) for i in range(3)],
                  *[ReplacementTransform(anc[3 + i], bots[i]) for i in range(3)],
                  GrowArrow(up), GrowArrow(dn), FadeIn(ow), FadeIn(bt), run_time=2.8)
        self.at("mating between them falls")
        gs = gold_stream(self, 1.2, -1.2, -1.6, n=14, thin=thin, spread=1.6)
        self.add(gs)
        gl = T("gene flow", 30, GOLD).move_to([2.2, 0, 0])
        self.play(FadeIn(gl), run_time=.6)
        self.play(thin.animate.set_value(.12), run_time=2.6, rate_func=linear)
        self.at("side effect")
        self.play(FadeIn(sel_note), run_time=.8)
        self.wait(1.0)
        self.finish()


class S04Ecospec(SpokenScene):
    def construct(self):
        thin = ValueTracker(.9)
        lk = lake(0, 0, 12.2, 7.0)
        self.add(lk)
        tops = [fish(SBLUE, False, 1.05).move_to([x, y, 0]) for x, y in [(-3.2, 1.7), (-1.7, 2.3), (-.2, 1.5)]]
        bots = [fish(OLIVE, True, 1.05).move_to([x, y, 0]) for x, y in [(-3.0, -1.9), (-1.5, -2.4), (.2, -1.7)]]
        for i, f in enumerate(tops + bots):
            wig(f, .12, .08, .4, i * 1.1)
        ow = T("open water", 30, SBLUE).move_to([-4.6, 2.6, 0])
        bt = T("bottom", 30, OLIVE).move_to([-4.6, -2.65, 0])
        self.add(*tops, *bots, ow, bt)
        gs = gold_stream(self, 1.2, -1.2, -1.6, n=14, thin=thin, spread=1.6)
        self.wait(.5)
        self.at("No one designs")
        no = T("no designer", 34, TEXT).move_to([4.0, 1.7, 0])
        self.play(FadeIn(no), run_time=.8)
        self.at("Selection acts on individuals")
        self.play(FadeIn(T("selection acts on individuals", 30, TEAL).move_to([3.2, .9, 0])), run_time=.8)
        self.at("isolation appears along the way")
        pieces = [Rectangle(width=.8, height=.26, stroke_width=1.5, stroke_color=TEXT, fill_color=GREY, fill_opacity=.95).move_to([x, 0, 0])
                  for x in (-4.0, -3.2, -2.4, 1.0, 1.8, 2.6)]
        pieces += [Rectangle(width=.8, height=.26, stroke_width=1.5, stroke_color=TEXT, fill_color=GREY, fill_opacity=.95).move_to([x, 0, 0])
                   for x in (-1.6, -.8, 0.0)]
        order = [0, 5, 1, 4, 2, 3, 6, 8, 7]
        for k in order[:6]:
            pieces[k].set_z_index(3)
            self.play(FadeIn(pieces[k], shift=DOWN * .15), run_time=.45)
        self.play(thin.animate.set_value(.25), run_time=1.0)
        lab = T("ecological speciation:\nisolation as a by-product of adaptation", 26, YELLOW, line_spacing=.7).move_to([2.6, 2.75, 0])
        lab.set_z_index(5)
        back = RoundedRectangle(corner_radius=.15, width=lab.width + .5, height=lab.height + .3, stroke_width=0,
                                fill_color=BG, fill_opacity=.9).move_to(lab).set_z_index(4)
        self.at("ecological speciation")
        self.play(FadeIn(back), FadeIn(lab), run_time=1.0)
        for k in order[6:]:
            pieces[k].set_z_index(3)
            self.play(FadeIn(pieces[k], shift=DOWN * .15), run_time=.5)
        self.play(thin.animate.set_value(.1), run_time=2.0)
        self.finish()


BC = [(-3.0, 3.3), (1.2, 3.3), (2.2, 2.3), (2.6, 0.6), (3.2, -.4), (2.4, -1.5), (1.6, -3.3), (-1.0, -3.3), (-2.0, -1.9),
      (-1.2, -.6), (-2.6, .8), (-3.4, 1.6)]


class S05Lakes(SpokenScene):
    def construct(self):
        off = np.array([-3.2, 0, 0])
        bc = Polygon(*[np.array([x, y, 0]) + off for x, y in BC], stroke_color=TEAL, stroke_width=4,
                     fill_color="#24324A", fill_opacity=.6)
        self.play(Create(bc), run_time=2.2)
        lp = [(-.7, 1.9, "lake A"), (-1.6, 0.3, "lake B"), (-.2, -1.5, "lake C")]
        lks = []
        self.at("Several small lakes")
        for k, (x, y, n) in enumerate(lp):
            e = Ellipse(width=1.3, height=.85, stroke_color=SBLUE, stroke_width=4, fill_color=SBLUE, fill_opacity=.5).move_to([x + off[0], y, 0])
            t = T(n, 30, TEXT).next_to(e, RIGHT, buff=.2)
            e.tt = k * 1.2

            def pulse(m, dt):
                m.tt += dt
                m.set_fill(opacity=.45 + .25 * np.sin(m.tt * 3))
            e.add_updater(pulse)
            lks.append(e)
            self.play(FadeIn(e, scale=.4), FadeIn(t), run_time=.5)
        self.at("British Columbia")
        bl = T("British Columbia (schematic)", 28, TEXT).move_to([3.6, 3.2, 0])
        self.play(FadeIn(bl), run_time=.8)
        self.at("two forms")
        ben = fish(OLIVE, True, 1.4).move_to([3.6, 1.0, 0])
        lim = fish(SBLUE, False, 1.4).move_to([3.6, -.6, 0])
        wig(ben, .2, .1, .4, 0)
        wig(lim, .2, .1, .4, 1.3)
        sp = T("threespine stickleback", 30, TEXT).move_to([3.6, -1.9, 0])
        self.play(FadeIn(ben), FadeIn(lim), FadeIn(sp), run_time=1.2)
        self.wait(1.5)
        self.finish()


def three_lakes(sc, titles=True):
    cs = [-4.4, 0, 4.4]
    out = []
    for i, cx in enumerate(cs):
        lk = lake(cx, -.15, 4.0, 4.9)
        sc.add(lk)
        ben = fish(OLIVE, True, .95).move_to([cx + .5, -1.65, 0])
        lim = fish(SBLUE, False, .95).move_to([cx - .55, -.5, 0])
        wig(ben, .18, .06, .4, i)
        wig(lim, .18, .08, .5, i + 1)
        sc.add(ben, lim)
        if titles:
            sc.add(T(["lake A", "lake B", "lake C"][i], 30, TEXT).move_to([cx, 2.65, 0]))
        out.append((cx, lk, ben, lim))
    return out


class S06Forms(SpokenScene):
    def construct(self):
        cs = [-4.4, 0, 4.4]
        lks = []
        for i, cx in enumerate(cs):
            lk = lake(cx, -.15, 4.0, 4.9)
            self.add(lk)
            self.add(T(["lake A", "lake B", "lake C"][i], 30, TEXT).move_to([cx, 2.65, 0]))
            lks.append(lk)
        self.wait(.4)
        self.at("The benthic form")
        bens = []
        for i, cx in enumerate(cs):
            b = fish(OLIVE, True, .95).move_to([cx + .6, -1.75, 0])
            wig(b, .18, .06, .4, i)
            bens.append(b)
        bl = [tag("benthic", b, OLIVE, 28, UP, .12) for b in bens]
        self.play(*[FadeIn(b) for b in bens], *[FadeIn(t) for t in bl], run_time=1.2)
        self.at("The limnetic form")
        lims = []
        for i, cx in enumerate(cs):
            l = fish(SBLUE, False, .95).move_to([cx - .9, .2, 0])
            wig(l, .18, .08, .5, i + 1)
            lims.append(l)
        ll = [tag("limnetic", l, SBLUE, 28, UP, .12) for l in lims]
        self.play(*[FadeIn(l) for l in lims], *[FadeIn(t) for t in ll], run_time=1.2)
        self.at("arisen on its own")
        anc = []
        arrs = []
        for i, cx in enumerate(cs):
            a = fish(ANC, False, .6).move_to([cx + 1.1, 1.5, 0])
            wig(a, .06, .04, .5, i)
            anc.append(a)
            arrs.append(VGroup(Arrow([cx + .9, 1.25, 0], [cx - .1, .2, 0], color=TEXT, buff=0, stroke_width=4, max_tip_length_to_length_ratio=.25),
                               Arrow([cx + 1.45, 1.2, 0], [cx + 1.5, -.85, 0], color=TEXT, buff=0, stroke_width=4, max_tip_length_to_length_ratio=.25)))
        self.play(*[FadeIn(a) for a in anc], *[Create(r) for r in arrs], run_time=1.6)
        three = T("three separate splits", 32, TEAL).move_to([0, -3.35, 0])
        self.play(FadeIn(three), run_time=.8)
        self.finish()


def trials_scene_base(sc, icons=True, lit=False):
    return Grid(sc, icons=icons, lit=lit)


class S07Trials(SpokenScene):
    def construct(self):
        cap = T("Rundle, Nagel, Boughman & Schluter, 2000", 28, TEXT).move_to([0, 3.4, 0])
        gr = Grid(self, icons=False)
        self.play(FadeIn(cap), run_time=.8)
        tr = ValueTracker(0)
        num = always_redraw(lambda: M(f"{int(tr.get_value())}+", 64, TEAL).move_to([4.55, 1.2, 0]))
        tx = T("lab mating trials", 30, TEXT).move_to([4.55, .2, 0])
        self.add(num)
        tank = big_tank(4.55, -1.8, 3.8, 2.4)
        f1 = fish(OLIVE, True, .85).move_to([3.75, -1.8, 0])
        f2 = face_left(fish(SBLUE, False, .85)).move_to([5.2, -1.6, 0])
        wig(f1, .2, .12, .5, 0)
        wig(f2, .2, .12, .5, 1)
        self.at("hundreds of laboratory")
        self.play(FadeIn(tx), FadeIn(tank), FadeIn(f1), FadeIn(f2), tr.animate.set_value(750), run_time=4.0, rate_func=linear)
        self.at("They paired fish")
        tks = {}
        for ri in (0, 1):
            for ci in (0, 1):
                tks[(ci, ri)] = cell_tank(ci, ri)
        self.play(FadeIn(tks[(0, 0)]), FadeIn(tks[(1, 0)]), run_time=1.0)
        self.at("same and different forms")
        self.play(FadeIn(tks[(0, 1)]), FadeIn(tks[(1, 1)]), run_time=1.0)
        self.at("from the same and different lakes")
        self.play(Indicate(gr.frame[1:][2], color=YELLOW), Indicate(gr.frame[1:][3], color=YELLOW), run_time=2.0)
        self.finish()


def right_tank(sc, move=True):
    tank = big_tank(4.45, -.4, 4.2, 3.6)
    a = fish(OLIVE, True, 1.0).move_to([3.5, -.4, 0])
    b = face_left(fish(OLIVE, True, 1.0)).move_to([5.4, -.4, 0])
    wig(a, .15, .1, .5, 0)
    wig(b, .15, .1, .5, 2)
    sc.add(tank, a, b)
    return tank, a, b


class S08Predict(SpokenScene):
    def construct(self):
        gr = Grid(self, icons=True)
        box = SurroundingRectangle(Rectangle(width=GW, height=GH).move_to([GCX[1], GRY[0], 0]), color=YELLOW, buff=0, stroke_width=7).set_z_index(5)
        self.wait(.3)
        self.at("A benthic fish")
        tank, a, b = right_tank(self)
        la = tag("lake A", a, TEXT, 28)
        self.play(Create(box), FadeIn(tank), FadeIn(a), FadeIn(b), FadeIn(la), run_time=1.5)
        self.at("another lake")
        lb = tag("lake B", b, TEXT, 28)
        self.play(FadeIn(lb), a.animate.shift(RIGHT * .2), b.animate.shift(LEFT * .2), run_time=2.0)
        self.at("Will they mate")
        q = bchip("Will they mate?", TEAL, 34).move_to([4.45, -3.1, 0])
        self.play(FadeIn(q, shift=UP * .2), run_time=.8)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        gr = Grid(self, icons=True)
        box = SurroundingRectangle(Rectangle(width=GW, height=GH).move_to([GCX[1], GRY[0], 0]), color=YELLOW, buff=0, stroke_width=7).set_z_index(5)
        tank, a, b = right_tank(self)
        a.shift(RIGHT * .2)
        b.shift(LEFT * .2)
        la = tag("lake A", a, TEXT, 28)
        lb = tag("lake B", b, TEXT, 28)
        q = bchip("Will they mate?", TEAL, 34).move_to([4.45, -3.1, 0])
        self.add(box, la, lb, q)
        tr = ValueTracker(0)
        ring = ring_timer(tr)
        ring.move_to([-6.1, 3.2, 0])
        self.add(ring)
        self.play(tr.animate.set_value(1), run_time=5, rate_func=linear)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        gr = Grid(self, icons=True)
        self.wait(.3)
        lab = T("isolation tracks\nform, not lake", 38, TEAL, line_spacing=.7).move_to([4.55, 1.2, 0])
        note = T("(brightness is schematic)", 24, TEXT).move_to([4.55, -.4, 0])
        self.at("Yes")
        g = {}
        for ci in (1, 0):
            r = Rectangle(width=GW, height=GH, stroke_width=0, fill_color=GREEN, fill_opacity=.32).move_to([GCX[ci], GRY[0], 0])
            g[(ci, 0)] = r
        self.play(FadeIn(g[(1, 0)]), run_time=1.0)
        self.play(FadeIn(g[(0, 0)]), run_time=.8)
        self.at("But benthic and limnetic")
        anims = []
        for ci in (0, 1):
            r = Rectangle(width=GW, height=GH, stroke_width=0, fill_color=BG, fill_opacity=.6).move_to([GCX[ci], GRY[1], 0])
            r.set_z_index(.6)
            g[(ci, 1)] = r
            t = gr.tanks[(ci, 1)]
            anims += [FadeIn(r), Rotate(t[1], PI, axis=UP), Rotate(t[2], PI, axis=UP), t[1].animate.shift(LEFT * .25), t[2].animate.shift(RIGHT * .25)]
        self.play(*anims, run_time=2.0)
        self.at("whichever lakes")
        self.play(FadeIn(lab), FadeIn(note), run_time=1.2)
        self.play(Indicate(lab, color=YELLOW, scale_factor=1.08), run_time=1.5)
        self.finish()


class S11Logic(SpokenScene):
    def construct(self):
        gr = Grid(self, icons=True, lit=True)
        c1 = VGroup(RoundedRectangle(corner_radius=.15, width=4.2, height=1.7, stroke_color=TEAL, stroke_width=3, fill_color=BG, fill_opacity=1),
                    T("ancestry predicts", 30, TEAL).move_to([0, .35, 0]), T("same lake mates best", 26, TEXT).move_to([0, -.3, 0])).move_to([4.5, 1.7, 0])
        c2 = VGroup(RoundedRectangle(corner_radius=.15, width=4.2, height=1.7, stroke_color=GREEN, stroke_width=3, fill_color=BG, fill_opacity=1),
                    T("ecology predicts", 30, GREEN).move_to([0, .35, 0]), T("same form mates best", 26, TEXT).move_to([0, -.3, 0])).move_to([4.5, -1.0, 0])
        col = SurroundingRectangle(VGroup(Rectangle(width=GW, height=GH).move_to([GCX[0], GRY[0], 0]),
                                          Rectangle(width=GW, height=GH).move_to([GCX[0], GRY[1], 0])), color=YELLOW, buff=0, stroke_width=7).set_z_index(5)
        row = SurroundingRectangle(VGroup(Rectangle(width=GW, height=GH).move_to([GCX[0], GRY[0], 0]),
                                          Rectangle(width=GW, height=GH).move_to([GCX[1], GRY[0], 0])), color=YELLOW, buff=0, stroke_width=7).set_z_index(5)
        self.wait(.4)
        self.at("If ancestry mattered")
        self.play(FadeIn(c1, shift=LEFT * .5), Create(col), run_time=1.5)
        self.at("If ecology mattered")
        self.play(FadeOut(col), FadeIn(c2, shift=LEFT * .5), Create(row), run_time=1.5)
        self.at("wherever they came from")
        tick = VGroup(Line([-.3, 0, 0], [-.1, -.25, 0]), Line([-.1, -.25, 0], [.35, .3, 0])).set_stroke(GREEN, 12).move_to([4.5, -2.5, 0]).scale(.8)
        self.play(Create(tick), c1.animate.set_opacity(.25), run_time=1.5)
        self.play(Indicate(c2, color=GREEN, scale_factor=1.05), run_time=1.5)
        self.finish()


class S12Meaning(SpokenScene):
    def construct(self):
        lk = three_lakes(self)
        self.wait(.4)
        self.at("isolation followed ecology")
        gs = []
        for (cx, l, ben, lim) in lk:
            g = hgate(cx, -1.05, 3.0, .6)
            gs.append(g)
            self.play(FadeIn(g, shift=DOWN * .2), run_time=.8)
            self.wait(.2)
        self.at("Drift alone")
        t1 = T("drift alone: unlikely to repeat", 32, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(t1), run_time=.8)
        self.at("Divergent selection is")
        t2 = T("repeats with the environment", 32, TEXT).move_to([0, -3.4, 0])
        t3 = T("divergent selection (likely cause)", 34, TEAL).move_to([0, 3.4, 0])
        self.play(Transform(t1, t2), FadeIn(t3), *[Indicate(g, color=YELLOW, scale_factor=1.1) for g in gs], run_time=2.0)
        self.finish()


def hill():
    return Polygon([-6.6, -3.7, 0], [-6.6, 1.6, 0], [6.6, -2.3, 0], [6.6, -3.7, 0], stroke_color=GREEN, stroke_width=3,
                   fill_color="#26362B", fill_opacity=.9)


def slope_y(x):
    return 1.6 - (x + 6.6) * 3.9 / 13.2


class S13Back(SpokenScene):
    def construct(self):
        h = hill()
        self.add(h)
        self.wait(.4)
        self.at("The red one")
        reds = [tube().scale(1.5).move_to([x, slope_y(x) + .55, 0]) for x in (2.2, 3.4, 4.6)]
        for j, m in enumerate(reds):
            sway(m, ph=j * 1.3)
        rl = T("red: lower", 32, FRED).move_to([3.0, .75, 0]).set_z_index(5)
        self.play(*[GrowFromCenter(m) for m in reds], FadeIn(rl), run_time=1.5)
        self.at("the pink one")
        pks = [flower(PINK, .6).move_to([x, slope_y(x) + .5, 0]) for x in (-5.0, -3.8, -2.6)]
        for j, m in enumerate(pks):
            sway(m, ph=j * 1.3)
        pl = T("pink: higher", 32, PINK).move_to([-3.0, 2.5, 0])
        arr = Arrow([6.1, -2.4, 0], [6.1, 2.6, 0], color=TEXT, buff=0, stroke_width=7)
        hl = T("higher", 30, TEXT).move_to([5.3, 3.2, 0])
        self.play(*[GrowFromCenter(m) for m in pks], FadeIn(pl), GrowArrow(arr), FadeIn(hl), run_time=1.8)
        self.at("Their flowers suit")
        b = bee().move_to([-6.2, 3.1, 0])
        d = bird().move_to([6.0, 1.8, 0])
        b.clear_updaters()
        self.add(b, d)
        self.play(b.animate.move_to([-5.4, 1.9, 0]), d.animate.move_to([4.6, 1.5, 0]), run_time=2.0)
        bob(b, .12, .6, 0)
        bob(d, .12, .6, .5)
        self.wait(1.5)
        self.finish()


class S14Flowers(SpokenScene):
    def construct(self):
        divider = DashedLine([0, -3.5, 0], [0, 3.5, 0], color=GREY, stroke_width=3)
        self.add(divider)
        self.wait(.3)
        self.at("The pink flower is wide")
        pf = flower(PINK, 1.7).move_to([-3.4, .3, 0])
        sway(pf, .03, .8)
        self.play(GrowFromCenter(pf), run_time=1.4)
        self.at("small nectar reward")
        nd = Circle(radius=.12, stroke_width=0, fill_color=NECT, fill_opacity=1).move_to([-3.4, .3, 0]).set_z_index(5)
        nl = T("small reward", 30, NECT).move_to([-3.4, -2.5, 0])
        self.play(FadeIn(nd, scale=.3), FadeIn(nl), run_time=1.0)
        self.at("bumblebees visit")
        b = bee().scale(1.4).move_to([-5.8, 2.9, 0])
        b.clear_updaters()
        self.add(b)
        self.play(b.animate.move_to([-3.4, 2.1, 0]), run_time=1.6)
        bob(b, .1, .8, 0)
        self.at("The red flower has a narrow tube")
        rf = tube().scale(3.0).move_to([3.6, .3, 0])
        sway(rf, .03, .8)
        self.play(GrowFromCenter(rf), run_time=1.4)
        self.at("large reward")
        nd2 = Circle(radius=.38, stroke_width=0, fill_color=NECT, fill_opacity=1).move_to([3.9, .3, 0]).set_z_index(5)
        nl2 = T("large reward", 30, NECT).move_to([3.6, -2.5, 0])
        self.play(FadeIn(nd2, scale=.3), FadeIn(nl2), run_time=1.0)
        self.at("hummingbirds visit")
        d = bird().scale(1.3).move_to([6.2, 2.9, 0])
        d.clear_updaters()
        self.add(d)
        self.play(d.animate.move_to([2.4, 1.6, 0]), run_time=1.6)
        bob(d, .1, .8, .4)
        self.wait(.8)
        self.finish()


class S15Gates(SpokenScene):
    def construct(self):
        st = Stage(self, active=(), draw=(), pol=True, gspec=GATES)
        self.wait(.4)
        self.at("Those adaptations")
        arr = Arrow([-3.9, -1.6, 0], [-3.9, 1.6, 0], color=TEXT, buff=0, stroke_width=8).set_z_index(4)
        el = T("higher", 30, TEXT).move_to([-3.9, 2.15, 0]).set_z_index(4)
        pf = flower(PINK, .55).move_to([-2.4, .95, 0]).set_z_index(4)
        rf = tube().scale(1.2).move_to([-2.4, -.95, 0]).set_z_index(4)
        sb = bee().scale(.6).move_to([-1.6, .95, 0]).set_z_index(4)
        sbd = bird().scale(.6).move_to([-1.55, -.95, 0]).set_z_index(4)
        for m in (sb, sbd):
            m.clear_updaters()
        pairs = VGroup(pf, rf, sb, sbd)
        self.play(GrowArrow(arr), FadeIn(el), FadeIn(pairs), run_time=1.6)
        self.at("Plants adapted to different elevations")
        st.gm[0] = gate_mob(*GATES[0]).set_z_index(1)
        st.lab[0] = st.label(0, TEAL)
        st.on(0)
        self.play(Transform(arr, st.gm[0]), FadeOut(el), FadeIn(st.lab[0]), run_time=2.0)
        self.at("A pollinator that")
        self.wait(.3)
        st.gm[1] = gate_mob(*GATES[1]).set_z_index(1)
        st.lab[1] = st.label(1, TEAL)
        st.on(1)
        self.at("carries little pollen")
        self.play(Transform(pairs, st.gm[1]), FadeIn(st.lab[1]), run_time=2.0)
        self.wait(2.5)
        self.finish()


class S16Takeaway(SpokenScene):
    def construct(self):
        div = Line([0, -3.7, 0], [0, 3.7, 0], color=GREY, stroke_width=3)
        lk = lake(-3.4, 0, 6.2, 6.4)
        self.add(div, lk)
        self.wait(.3)
        self.at("Fish or flowers")
        hl = hill().scale(.46).move_to([3.4, -1.6, 0])
        ben = fish(OLIVE, True, 1.1).move_to([-3.4, -.5, 0])
        lim = fish(SBLUE, False, 1.1).move_to([-3.4, .5, 0])
        pf = flower(PINK, .6).move_to([2.2, -.1, 0])
        rf = tube().scale(1.4).move_to([3.9, -1.2, 0])
        for j, m in enumerate((ben, lim)):
            wig(m, .15, .07, .4, j)
        for j, m in enumerate((pf, rf)):
            sway(m, ph=j * 1.3)
        self.play(FadeIn(hl), FadeIn(ben), FadeIn(lim), FadeIn(pf), FadeIn(rf), run_time=1.5)
        self.at("Adapt to different places")
        self.play(ben.animate.move_to([-4.3, -1.8, 0]), lim.animate.move_to([-2.5, 1.9, 0]),
                  pf.animate.move_to([1.3, .1, 0]), rf.animate.move_to([5.0, -1.5, 0]), run_time=3.0)
        self.at("isolation often grows")
        g1 = hgate(-3.4, 0, 3.4, .6)
        g2 = gate_mob(3.4, .3)
        g2.scale(.6).move_to([3.15, -.5, 0])
        self.play(FadeIn(g1, shift=DOWN * .2), FadeIn(g2, shift=DOWN * .2), run_time=1.2)
        self.at("side effect")
        self.play(Indicate(g1, color=YELLOW), Indicate(g2, color=YELLOW), run_time=1.5)
        self.wait(1.0)
        self.finish()


class S17End(EndCard):
    LINE = "Adapt to different habitats, and isolation often follows as a side effect."
