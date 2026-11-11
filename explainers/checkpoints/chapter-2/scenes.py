"""Chapter 2: timing securin's destruction. Same cell, colours and track as chapter 1.
COLOR MAP (chapter 1): YELLOW DNA; ORANGE separase; RED wait/sensors; GREEN recovery (here: the fluorescent glow);
TEAL Cdc20; BLUE APC/C; PURPLE securin; PINK cyclin B; GOLD ubiquitin/questions/half-life; TEXT kinetochores; GREY cell/spindle.
The curve is computed: F(t) = 100 x exp(-k t), k = ln2 / 10 min. The data are marked made-up.
"""
from bp_style import *
import math

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58FB5'
K = math.log(2) / 10


def vv(t):
    return 100 * math.exp(-K * t)


X0, XS, Y0, YS = .75, .1933, -2.1, .036


def gx(t):
    return X0 + XS * t


def gy(v):
    return Y0 + YS * v


def pt(t, v=None):
    return np.array([gx(t), gy(vv(t) if v is None else v), 0.])


FULLC = np.array([0, .15, 0.])
SS = .42
SC = np.array([-4.25, .95, 0.])
SECSM = .65
DOCK = (1.7, 1.4)
BARREL = (2.2, -1.35)
DATA = [(0, 100), (5, 71), (10, 50), (15, 35)]


def label(s, x=0, y=3.25, c=TEXT, size=32):
    return fit(T(s, size=size, color=c), max_w=12.5).move_to([x, y, 0])


def gold_card(s, x, y, size=34):
    t = T(s, size=size, color=GOLD)
    box = RoundedRectangle(corner_radius=.14, width=t.width + .5, height=t.height + .4, stroke_color=GOLD,
                           stroke_width=3, fill_color=BG, fill_opacity=.92)
    return VGroup(box, t.move_to(box)).move_to([x, y, 0])


def spindle():
    poles = VGroup(Dot([-4.5, 0, 0], radius=.13, color=GREY), Dot([4.5, 0, 0], radius=.13, color=GREY))
    pairs = VGroup(); fibers = VGroup(); links = VGroup()
    for y in [-.8, 0, .8]:
        x = -.8
        pair = VGroup()
        for dx in [-.18, .18]:
            rod = Line([x + dx, y - .28, 0], [x + dx, y + .28, 0], color=YELLOW, stroke_width=10)
            kt = Dot([x + dx, y, 0], radius=.085, color=TEXT)
            pair.add(VGroup(rod, kt))
        pairs.add(pair)
        fibers.add(Line([-4.5, 0, 0], [x - .18, y, 0], color=GREY, stroke_width=2.5))
        fibers.add(Line([4.5, 0, 0], [x + .18, y, 0], color=GREY, stroke_width=2.5))
        links.add(Line([x - .18, y - .13, 0], [x + .18, y - .13, 0], color=GREY, stroke_width=6))
    return VGroup(fibers, poles, links, pairs)


def brake(x=.6):
    return VGroup(Line([x, -3.02, 0], [x, -2.22, 0], color=RED, stroke_width=12),
                  Line([x - .25, -2.22, 0], [x + .25, -2.22, 0], color=RED, stroke_width=12))


def track_full():
    g = VGroup(Line([-4.9, -2.85, 0], [4.9, -2.85, 0], color=GREY, stroke_width=5))
    for x, s in zip([-4.4, -2.2, 0, 2.2, 4.4], ['G1', 'S', 'G2', 'M', 'anaphase']):
        g.add(label(s, x, -3.24, size=28))
    g.add(label('schematic', 0, -3.65, size=28))
    return g


def track_small():
    g = VGroup(Line([-6.6, -2.2, 0], [-2.0, -2.2, 0], color=GREY, stroke_width=5))
    for x, s in zip([-6.4, -5.5, -4.7, -3.9, -2.75], ['G1', 'S', 'G2', 'M', 'anaphase']):
        g.add(label(s, x, -2.65, size=26 if s == 'anaphase' else 28))
    return g


def make_marker(x, y):
    m = Triangle(color=TEXT, fill_opacity=1).scale(.14).rotate(PI).move_to([x, y, 0])
    m.clock = 0

    def idle(mm, dt):
        mm.clock += dt
        mm.shift(UP * (.045 * math.sin(mm.clock * 4) - .045 * math.sin((mm.clock - dt) * 4)))
    m.add_updater(idle)
    return m


def chevron(x=-3.3, y=-2.2):
    return VGroup(Line([x - .15, y + .17, 0], [x + .05, y, 0], color=GOLD, stroke_width=7),
                  Line([x + .05, y, 0], [x - .15, y - .17, 0], color=GOLD, stroke_width=7))


def trackers(sc, L=100., G=1., HT=1., T0=0., link=False):
    W = dict(L=ValueTracker(L), G=ValueTracker(G), H=ValueTracker(HT), T=ValueTracker(T0), GV=ValueTracker(1))
    for v in W.values():
        sc.add(v)
    import random
    rng = random.Random(os.environ.get('KX_SCENE_ID', 'x'))
    motes = VGroup()
    for _ in range(40):
        d = Dot(radius=rng.uniform(.03, .07), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(.18, .4))
        d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
        d.v = (rng.uniform(-.25, .25), rng.uniform(.1, .35))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 3.9:
                m.shift(DOWN * 7.8)
            if abs(m.get_x()) > 6.9:
                m.shift(LEFT * 13.8 * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        motes.add(d)
    motes.set_z_index(-10)
    sc.add(motes)
    if link:
        W['L'].add_updater(lambda m: m.set_value(vv(W['T'].get_value())))
        W['L'].set_value(vv(T0))
    return W


def make_sec(scale=1.0):
    halo = RoundedRectangle(corner_radius=.12, width=.66, height=.48, stroke_color=GREEN, stroke_width=6,
                            fill_color=GREEN, fill_opacity=0)
    body = RoundedRectangle(corner_radius=.09, width=.46, height=.3, stroke_color=PURPLE, stroke_width=2.5,
                            fill_color=PURPLE, fill_opacity=.85)
    g = VGroup(halo, body)
    halo.set_stroke(opacity=0)
    return g.scale(scale, scale_stroke=True)


def _slots():
    out = []
    for j, y in enumerate([1.35, 1.85, 2.35]):
        for i, x in enumerate([-1.6, -.8, 0, .8]):
            out.append((x + .06 * math.sin(3 * i + 2 * j), y + .05 * math.cos(2 * i + 3 * j)))
    out.sort(key=lambda q: (q[0] - DOCK[0]) ** 2 + (q[1] - DOCK[1]) ** 2)
    return out


SLOTS = _slots()


def amb(m, dt):
    m.clk += dt
    off = np.array([m.amp * math.sin(m.clk * 1.3 + m.ph), m.amp * math.cos(m.clk * 1.1 + m.ph * 1.7), 0])
    m.shift(off - m.off)
    m.off = off
    h = m.H.get_value()
    op = 1.0
    if m.lvl is not None:
        op = min(1, max(0, m.lvl[0].get_value() * 11 / 100 - m.lvl[1]))
    m[0].set_stroke(opacity=h * op * (.6 + .25 * math.sin(m.clk * 2.2 + m.ph)))
    m[0].set_fill(GREEN, opacity=h * .2 * op)
    m[1].set_fill(opacity=.85 * op)
    m[1].set_stroke(opacity=op)


class Cell:
    def __init__(self, sc, W, small=False, alive=12, labels=True):
        self.sc, self.W, self.small = sc, W, small
        self.s = SS if small else 1.
        self.c = SC.copy() if small else FULLC.copy()
        shell = Ellipse(width=11.7, height=5.5, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.16).shift(UP * .15)
        shell.clk = 0

        def glow(m, dt):
            m.clk += dt
            g = W['G'].get_value(); lv = W['L'].get_value() / 100
            m.set_fill(interpolate_color(ManimColor(GREY), ManimColor(GREEN), g),
                       opacity=.16 + .2 * g * lv + .02 * g * math.sin(m.clk * 4))
            m.set_stroke(interpolate_color(ManimColor(GREY), ManimColor(GREEN), .7 * g))
        shell.add_updater(glow)
        notch = Rectangle(width=.3, height=.5, color=TEAL, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([2.1, 1.4, 0])
        a = chip('APC/C', BLUE, size=30, pad=.2).move_to([3.2, 1.85, 0])
        c = chip('Cdc20', TEAL, size=30, pad=.2).move_to([3.2, .95, 0])
        barrel = RoundedRectangle(corner_radius=.15, width=2.4, height=1.0, color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=.25).move_to([BARREL[0], BARREL[1], 0])
        self.group = VGroup(shell, spindle(), notch, a[0], c[0], barrel)
        self.labels = VGroup(a[1], c[1], T('proteasome', size=26, color=TEXT).move_to(barrel).shift(DOWN * .25)) if (labels and not small) else VGroup()
        if small:
            self.group.scale(SS, about_point=FULLC, scale_stroke=True).shift(SC - FULLC)
        self.secs = {}
        sc.add(self.group)
        for p, (x, y) in enumerate(SLOTS):
            if p < 12 - alive:
                continue
            self.secs[p] = self._new_sec(p, x, y)
            sc.add(self.secs[p])
        sc.add(self.labels)

    def _new_sec(self, p, x, y):
        sec = make_sec(SECSM if self.small else 1.).move_to(self.P(x, y))
        sec.clk = p * .7; sec.ph = p * 1.3; sec.amp = .02 if self.small else .05
        sec.off = np.zeros(3); sec.H = self.W['H']; sec.lvl = None
        sec.add_updater(amb)
        return sec

    def P(self, x, y):
        return self.c + self.s * (np.array([x, y, 0.]) - FULLC)

    def level_mode(self):
        for p, sec in self.secs.items():
            sec.lvl = (self.W['L'], 11 - p)

    def shrink_anims(self):
        an = [self.group.animate.scale(SS, about_point=FULLC, scale_stroke=True).shift(SC - FULLC), FadeOut(self.labels)]
        for p, sec in self.secs.items():
            x, y = SLOTS[p]
            an.append(sec.animate.scale(SECSM, scale_stroke=True).move_to(SC + SS * (np.array([x, y, 0.]) - FULLC)))
            sec.amp = .02
        self.small, self.s, self.c = True, SS, SC.copy()
        return an

    def drain(self, n, run=1.2):
        ps = sorted(self.secs)[:n]
        pin = self.P(*BARREL)
        an = []
        for p in ps:
            sec = self.secs.pop(p)
            sec.clear_updaters()
            an.append(sec.animate.move_to(pin).scale(.3).set_opacity(0))
        return LaggedStart(*an, lag_ratio=.4, run_time=run)

    def cycle(self, sync=None, Lto=None, name=False):
        sc = self.sc; sync = sync or {}

        def wait(k):
            if k in sync:
                sc.at(sync[k])
        p = min(self.secs); sec = self.secs.pop(p); sec.clear_updaters()
        D = self.P(*DOCK)
        wait('dock')
        lab = None
        if name:
            lab = T('securin', size=26, color=PURPLE)
            lab.add_updater(lambda m: m.next_to(sec[1], DOWN, buff=.08).shift(LEFT * .8))
            sc.add(lab)
        sc.play(sec.animate.move_to(D), run_time=.6)
        wait('tag')
        tags = VGroup(*[Dot(radius=.075, color=GOLD) for _ in range(4)]).arrange(RIGHT, buff=.06).next_to(sec, UP, buff=.05)
        sc.play(LaggedStart(*[FadeIn(d, scale=.3) for d in tags], lag_ratio=.3, run_time=.7))
        grp = VGroup(sec, tags)
        wait('enter')
        if lab is not None:
            lab.clear_updaters()
            sc.play(FadeOut(lab), run_time=.2)
        sc.play(grp.animate.move_to(self.P(BARREL[0], BARREL[1] + 1.0)), run_time=.7)
        sc.play(grp.animate.move_to(self.P(BARREL[0], BARREL[1] + .3)).scale(.3).set_opacity(0), run_time=.45)
        wait('out')
        frs = VGroup(*[Square(side_length=.17, color=PURPLE, fill_opacity=1).move_to(self.P(3.5 + .12 * i, -1.35 + (i % 2) * .15 - .1)) for i in range(4)])
        sc.add(frs)
        an = [LaggedStart(*[f.animate.shift(RIGHT * .5 + DOWN * .25).set_opacity(0) for f in frs], lag_ratio=.2, run_time=.6)]
        if Lto is not None:
            an.append(self.W['L'].animate.set_value(Lto))
        sc.play(*an, run_time=.6)
        sc.remove(frs, grp)


def make_gauge(W, x, full):
    L, GV = W['L'], W['GV']
    GH, yb = 3.9, -2.0
    box = Rectangle(width=.5, height=GH, color=TEXT, stroke_width=3).move_to([x, yb + GH / 2, 0])
    bar = Rectangle(width=.44, height=.02, stroke_width=0, fill_color=GREEN, fill_opacity=.95).move_to([x, yb + .04, 0])

    def bupd(m):
        h = max(.02, (GH - .06) * L.get_value() / 100)
        m.become(Rectangle(width=.44, height=h, stroke_width=0, fill_color=GREEN,
                           fill_opacity=.95 * GV.get_value()).move_to([x, yb + .03 + h / 2, 0]))
    bar.add_updater(bupd)
    box.add_updater(lambda m: m.set_stroke(opacity=GV.get_value()))
    read = M('100%', size=26).move_to([x, yb - .4, 0]); read.v = None

    def rupd(m):
        v = int(round(L.get_value()))
        if v != m.v:
            m.become(M(f'{v}%', size=26).move_to([x, yb - .4, 0])); m.v = v
        m.set_opacity(GV.get_value())
    read.add_updater(rupd)
    name = T('glow =\nsecurin left', size=24) if full else T('glow', size=26)
    name.move_to([x - .4, 2.5, 0] if full else [x, 2.3, 0])
    name.add_updater(lambda m: m.set_opacity(GV.get_value()))
    return VGroup(box, bar, read, name)


def make_clock(W):
    clk = T('t = 0 min', size=30); clk.v = -1

    def upd(m):
        v = int(round(W['T'].get_value()))
        if v != m.v:
            m.become(T(f't = {v} min', size=30).move_to([-4.3, -3.35, 0])); m.v = v
    clk.add_updater(upd)
    return clk


def axes_group():
    g = VGroup(Line([X0, Y0, 0], [gx(30), Y0, 0], color=TEXT, stroke_width=4),
               Line([X0, Y0, 0], [X0, gy(100) + .12, 0], color=TEXT, stroke_width=4))
    for t in range(0, 31, 5):
        g.add(Line([gx(t), Y0, 0], [gx(t), Y0 - .1, 0], color=TEXT, stroke_width=3))
        g.add(T(str(t), size=22).move_to([gx(t), Y0 - .35, 0]))
    for v in (0, 25, 50, 75, 100):
        g.add(Line([X0, gy(v), 0], [X0 - .1, gy(v), 0], color=TEXT, stroke_width=3))
        g.add(T(str(v), size=22).move_to([X0 - .4, gy(v), 0]))
    xt = T('minutes after metaphase', size=24).move_to([gx(15), Y0 - .8, 0])
    yt = T('securin glow (% of metaphase)', size=22).rotate(PI / 2).move_to([-.45, -.3, 0])
    g.add(xt, yt)
    g.xt = xt
    return g


def made_up():
    return T('made-up data', size=28, color=TEXT).move_to([gx(15), 1.95, 0])


def dot_at(t, v):
    return Dot(pt(t, v), radius=.13, color=PURPLE)


def dot_lab(t, v):
    return T(f'{v}%', size=24, color=PURPLE).move_to(pt(t, v) + np.array([.55, .3, 0]))


def curve(t0, t1, dashed=False):
    c = ParametricFunction(lambda u: pt(u), t_range=[t0, t1, .1], color=PURPLE, stroke_width=6)
    return DashedVMobject(c, num_dashes=18) if dashed else c


def bracket(t0, t1, text='half-life\n= 10 min'):
    y = -1.75
    b = VGroup(Line([gx(t0), y, 0], [gx(t1), y, 0], color=GOLD, stroke_width=5),
               Line([gx(t0), y - .1, 0], [gx(t0), y + .1, 0], color=GOLD, stroke_width=5),
               Line([gx(t1), y - .1, 0], [gx(t1), y + .1, 0], color=GOLD, stroke_width=5))
    lab = T(text, size=26 if '\n' in text else 28, color=GOLD).move_to([gx((t0 + t1) / 2) - (.12 if '\n' in text else 0), -1.05 if '\n' in text else -1.3, 0])
    return b, lab


def dash10():
    return DashedLine([gx(10), gy(50), 0], [gx(10), Y0, 0], color=GOLD, stroke_width=4)


def question_state(sc):
    """s05/s06: ring at 20 minutes, dashed line, card."""
    ring = Circle(radius=.17, color=PURPLE, stroke_width=4).move_to([gx(20), Y0, 0])
    dl = DashedLine([gx(20), Y0 + .17, 0], [gx(20), .2, 0], color=PURPLE, stroke_width=4)
    card = gold_card('Glow at\n20 minutes?', 4.9, .95, size=32)
    return ring, dl, card


def left_world(sc, W, T0, alive, hdr=True):
    cell = Cell(sc, W, small=True, alive=alive)
    trk = track_small(); mk = make_marker(-3.9, -1.95)
    g = make_gauge(W, -1.3, False)
    sc.add(trk, mk, g, make_clock(W))
    if hdr:
        sc.add(label('HeLa cell (schematic)', -4.3, 2.75, size=28))
    return cell, mk


def plot_base(sc, dots=4, crv=None, dot20=False, b1=False):
    ax = axes_group(); sc.add(ax, made_up())
    ds = [dot_at(t, v) for t, v in DATA[:dots]]
    sc.add(*ds)
    out = dict(ax=ax, dots=ds)
    if crv:
        c = curve(0, crv); sc.add(c); out['curve'] = c
    if dot20:
        d = dot_at(20, 25); sc.add(d, T('25%', size=28, color=PURPLE).move_to(pt(20, 25) + np.array([.55, .42, 0]))); out['d20'] = d
    if b1:
        b, lab = bracket(0, 10); sc.add(b, lab, dash10()); out['b1'] = VGroup(b, lab)
    return out


# ---------------------------------------------------------------- scenes
class S00Link(SpokenScene):
    def construct(self):
        W = trackers(self, G=0, HT=0)
        cell = Cell(self, W)
        self.add(label('PtK1 · rat-kangaroo · schematic'), track_full(), make_marker(2.2, -2.55))
        card = gold_card('How fast?', -3.3, 1.75)
        self.at('how fast')
        self.play(FadeIn(card, shift=RIGHT * 1.5), run_time=.8)
        cell.cycle()
        self.at('the brake')
        b = brake()
        self.play(FadeIn(b), run_time=.4)
        self.at('lifting')
        self.play(b.animate.shift(UP * .9).set_opacity(0), run_time=.9)
        cell.cycle(sync=dict(dock='the apc', tag='tag securin', enter='and the proteasome', out='destroyed it'), name=True)
        cell.cycle()
        self.finish()


class S01Title(TitleCard):
    LESSON = 'Checkpoints and Irreversible Transitions'
    TITLE = "Timing Securin's Destruction"

    def construct(self):
        shell = Ellipse(width=11.7, height=5.5, color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.16).shift(UP * .15)
        sp = spindle()
        dim = VGroup(shell).set_opacity(.3)
        dim.base = dim.copy(); dim.clock = 0

        def breathe(m, dt):
            m.clock += dt
            m.become(m.base.copy().scale(1 + .02 * math.sin(m.clock * 2.2)))
        dim.add_updater(breathe)
        self.add(dim)
        super().construct()


class S02Reporter(SpokenScene):
    def construct(self):
        W = trackers(self, G=0, HT=0)
        cell = Cell(self, W)
        hdr = label('PtK1 · rat-kangaroo · schematic')
        self.add(hdr, track_full(), make_marker(2.2, -2.55))
        self.at('fluorescent')
        lab = T('securin +\nfluorescent tag', size=24, color=GREEN).move_to([-3.5, 1.5, 0])
        self.play(W['H'].animate.set_value(1), FadeIn(lab), run_time=1.4)
        self.at('and film')
        self.play(W['G'].animate.set_value(1), run_time=1.6)
        self.at('the glow tracks')
        g = make_gauge(W, 6.3, True); W['GV'].set_value(0); self.add(g)
        self.play(W['GV'].animate.set_value(1), run_time=1.2)
        self.at('is left')
        self.play(Indicate(VGroup(*cell.secs.values()), color=GREEN, scale_factor=1.08), run_time=1.0)
        self.at('in human')
        self.play(FadeOut(hdr), FadeOut(lab), run_time=.4)
        self.play(FadeIn(label('HeLa cell (schematic)', -3.9, 3.25)), run_time=.4)
        self.at('fall at metaphase')
        cell.cycle(Lto=92)
        self.finish()


class S03Data(SpokenScene):
    def construct(self):
        W = trackers(self, link=True)
        cell = Cell(self, W)
        hdr = label('HeLa cell (schematic)', -3.9, 3.25)
        ftrack, fmark, fgauge = track_full(), make_marker(2.2, -2.55), make_gauge(W, 6.3, True)
        self.add(hdr, ftrack, fmark, fgauge)
        self.at('here are')
        mk_s = make_marker(-3.9, -1.95)
        self.play(*cell.shrink_anims(), Transform(hdr, label('HeLa cell (schematic)', -4.3, 2.75, size=28)),
                  FadeOut(ftrack), FadeOut(fmark), FadeOut(fgauge), run_time=2.0)
        self.add(track_small(), mk_s, make_gauge(W, -1.3, False))
        clk = make_clock(W); self.add(clk)
        ax = axes_group()
        self.at('made up numbers')
        self.play(Create(ax[0]), Create(ax[1]), run_time=1.0)
        self.play(FadeIn(ax[2:]), FadeIn(made_up()), run_time=1.0)
        self.at('at metaphase')
        d0 = dot_at(0, 100); l0 = dot_lab(0, 100)
        self.play(FadeIn(d0, shift=DOWN * .8), FadeIn(l0), run_time=.6)
        self.wait(max(.05, 4.8 - self.elapsed()))
        # 0 -> 5 minutes: run before the narrator names it, dot lands on "71"
        self.play(W['T'].animate.set_value(5), cell.drain(4, 1.8), run_time=2.4, rate_func=linear)
        self.at('71')
        d1 = dot_at(5, 71); l1 = dot_lab(5, 71)
        self.play(FadeIn(d1, shift=DOWN * .8), FadeIn(l1), run_time=.5)
        self.wait(max(.05, 9.0 - self.elapsed()))
        self.play(W['T'].animate.set_value(10), cell.drain(2, 1.0), run_time=1.8, rate_func=linear)
        self.at('50')
        d2 = dot_at(10, 50); l2 = dot_lab(10, 50)
        self.play(FadeIn(d2, shift=DOWN * .8), FadeIn(l2), run_time=.5)
        self.wait(max(.05, 11.3 - self.elapsed()))
        self.play(W['T'].animate.set_value(15), cell.drain(2, 1.0), run_time=1.8, rate_func=linear)
        self.at('35')
        d3 = dot_at(15, 35); l3 = dot_lab(15, 35)
        self.play(FadeIn(d3, shift=DOWN * .8), FadeIn(l3), run_time=.5)
        self.finish()


class S04Halflife(SpokenScene):
    def construct(self):
        W = trackers(self, T0=15, link=True)
        cell, mk = left_world(self, W, 15, 4)
        P = plot_base(self, dots=4)
        labs = VGroup(*[dot_lab(t, v) for t, v in DATA]); self.add(labs)
        self.play(FadeOut(labs), run_time=.5)
        crv = curve(0, 15)
        self.at('exponential loss')
        self.play(Create(crv), run_time=1.6)
        self.at('no new securin')
        chp = chip('new securin', PURPLE, size=28).move_to([-5.55, -1.4, 0])
        arr = Arrow([-5.55, -1.0, 0], [-5.55, -.25, 0], buff=0, color=PURPLE, stroke_width=5)
        xx = VGroup(Line([-5.8, -.45, 0], [-5.3, -.8, 0], color=TEXT, stroke_width=7),
                    Line([-5.8, -.8, 0], [-5.3, -.45, 0], color=TEXT, stroke_width=7))
        nm = T('none made', size=28, color=TEXT).move_to([-3.3, -.85, 0])
        self.play(FadeIn(chp), GrowArrow(arr), run_time=.7)
        self.play(Create(xx), FadeIn(nm), run_time=.7)
        self.at('at 10 minutes')
        dl = dash10()
        self.play(Create(dl), run_time=.8)
        self.at('half is gone')
        self.play(Indicate(P['dots'][2], color=GOLD, scale_factor=1.8), run_time=.8)
        self.at('that time is')
        b, lab = bracket(0, 10)
        self.play(Create(b), run_time=.8)
        self.play(FadeIn(lab), run_time=.5)
        self.at('a half life removes')
        self.play(Indicate(VGroup(b, lab), color=GOLD), run_time=1.0)
        self.at('of what remains')
        self.play(Indicate(P['dots'][2], color=GOLD, scale_factor=1.8), run_time=.8)
        self.at('the loss is')
        a1 = VGroup(DashedLine([gx(0), gy(100), 0], [gx(5), gy(100), 0], color=GOLD, stroke_width=4),
                    Arrow([gx(5), gy(100), 0], [gx(5), gy(71) + .13, 0], buff=0, color=GOLD, stroke_width=5))
        l1 = T('x 0.71', size=26, color=GOLD).move_to([gx(5) + .85, 1.15, 0])
        self.play(Create(a1), FadeIn(l1), run_time=.8)
        self.at('a steady fraction')
        a2 = VGroup(DashedLine([gx(10), gy(50), 0], [gx(15), gy(50), 0], color=GOLD, stroke_width=4),
                    Arrow([gx(15), gy(50), 0], [gx(15), gy(35) + .13, 0], buff=0, color=GOLD, stroke_width=5))
        l2 = T('x 0.71', size=26, color=GOLD).move_to([gx(15) + .85, -.4, 0])
        self.play(Create(a2), FadeIn(l2), run_time=.8)
        self.at('not a steady')
        self.play(Indicate(VGroup(a1[1], a2[1]), color=GOLD), run_time=1.2)
        self.finish()


def s05_world(sc):
    W = trackers(sc, T0=15, link=True)
    cell, mk = left_world(sc, W, 15, 4)
    P = plot_base(sc, dots=4, crv=15, b1=True)
    return W, cell, P


class S05Predict(SpokenScene):
    def construct(self):
        W, cell, P = s05_world(self)
        self.at('here is a test')
        self.play(Indicate(P['b1'], color=GOLD), run_time=1.0)
        ring, dl, card = question_state(self)
        self.at('ten minutes took')
        self.play(Indicate(P['dots'][0], color=GOLD, scale_factor=1.8), run_time=.6)
        self.play(Indicate(P['dots'][2], color=GOLD, scale_factor=1.8), run_time=.6)
        self.at('what will it read')
        self.play(FadeIn(ring), Create(dl), FadeIn(card, shift=LEFT), run_time=1.2)
        self.finish()


class S06Think(NarratedScene):
    def construct(self):
        W, cell, P = s05_world(self)
        ring, dl, card = question_state(self)
        self.add(ring, dl, card)
        ring.clk = 0
        ring.add_updater(lambda m, dt: (setattr(m, 'clk', m.clk + dt), m.set_stroke(opacity=.55 + .45 * math.sin(m.clk * 3) ** 2))[0])
        dl.clk = 0
        dl.add_updater(lambda m, dt: (setattr(m, 'clk', m.clk + dt), m.set_stroke(opacity=.5 + .5 * math.sin(m.clk * 4) ** 2))[0])
        self.wait(self.narration_s)
        self.finish()


class S07Answer(SpokenScene):
    def construct(self):
        W, cell, P = s05_world(self)
        ring, dl, card = question_state(self)
        self.add(ring, dl, card)
        self.at('twenty five percent')
        c2 = curve(15, 20)
        d20 = dot_at(20, 25)
        self.play(FadeOut(card), Create(c2), W['T'].animate.set_value(20), cell.drain(1, 1.0),
                  FadeOut(ring), FadeIn(d20), run_time=1.4, rate_func=linear)
        self.add(c2)
        l25 = T('25%', size=28, color=PURPLE).move_to(pt(20, 25) + np.array([.55, .42, 0]))
        self.play(FadeIn(l25), FadeOut(dl), run_time=.4)
        self.at('not zero')
        ghost = DashedLine([gx(0), gy(100), 0], [gx(20), gy(0), 0], color=TEXT, stroke_width=4)
        gl = T('steady amount:\nzero', size=26, color=TEXT).move_to([5.0, .0, 0])
        self.play(Create(ghost), FadeIn(gl), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(ghost), FadeOut(gl), run_time=.6)
        self.at('two half lives')
        b2, bl2 = bracket(10, 20, 'half-life')
        self.play(Create(b2), FadeIn(bl2), run_time=1.0)
        self.at('the first ten minutes')
        ar1 = Arrow([5.6, gy(100), 0], [5.6, gy(50), 0], buff=0, color=GOLD, stroke_width=6)
        t1 = M('-50', size=28, color=GOLD).move_to([5.0, gy(75), 0])
        self.play(GrowArrow(ar1), FadeIn(t1), run_time=.9)
        self.at('the next ten')
        ar2 = Arrow([6.35, gy(50), 0], [6.35, gy(25), 0], buff=0, color=GOLD, stroke_width=6)
        t2 = M('-25', size=28, color=GOLD).move_to([6.35, gy(25) - .4, 0])
        self.play(GrowArrow(ar2), FadeIn(t2), run_time=.9)
        self.finish()


def eqn():
    ft = T('F(t)', size=40); eq = T('=', size=40); f0 = T('F', size=40); f0s = T('0', size=26)
    tm = T('×', size=40); e = T('e', size=40)
    ex = VGroup(T('−', size=28), T('k', size=28), T('t', size=28)).arrange(RIGHT, buff=.04)
    ft.move_to([1.0, 3.3, 0]); eq.next_to(ft, RIGHT, buff=.2); f0.next_to(eq, RIGHT, buff=.2)
    f0s.move_to(f0.get_right() + np.array([.15, -.1, 0])); tm.next_to(f0, RIGHT, buff=.4)
    e.next_to(tm, RIGHT, buff=.2); ex.move_to(e.get_right() + np.array([.5, .22, 0]))
    g = VGroup(ft, eq, f0, f0s, tm, e, ex)
    g.ft, g.f0, g.ex = ft, f0, ex
    return g


def s08_world(sc):
    W = trackers(sc, T0=20, link=True)
    cell, mk = left_world(sc, W, 20, 3)
    P = plot_base(sc, dots=4, crv=20, dot20=True, b1=True)
    return W, cell, P


class S08Formula(SpokenScene):
    def construct(self):
        W, cell, P = s08_world(self)
        f = eqn()
        self.at('formula')
        self.play(Write(f), run_time=1.7)
        self.at('f of t')
        c1 = DashedLine(f.ft.get_bottom(), P['d20'].get_center(), color=GOLD, stroke_width=4)
        self.play(Indicate(f.ft, color=GOLD), Create(c1), Indicate(P['d20'], color=GOLD, scale_factor=1.8), run_time=1.0)
        self.at('f zero')
        c2 = DashedLine(f.f0.get_bottom(), P['dots'][0].get_center(), color=GOLD, stroke_width=4)
        self.play(FadeOut(c1), Indicate(f.f0, color=GOLD), Create(c2), Indicate(P['dots'][0], color=GOLD, scale_factor=1.8), run_time=1.0)
        self.at('times e')
        self.play(FadeOut(c2), run_time=.4)
        self.at('minus k t')
        self.play(Indicate(f.ex, color=GOLD), Indicate(P['ax'].xt, color=GOLD), run_time=1.0)
        self.at('the rate constant')
        k1 = T('k =', size=34).move_to([1.6, 2.7, 0])
        self.play(Write(k1), run_time=.6)
        self.at('natural log')
        k2 = T('ln 2', size=34).next_to(k1, RIGHT, buff=.2)
        self.play(Write(k2), run_time=.6)
        self.at('divided by')
        k3 = T('/', size=34).next_to(k2, RIGHT, buff=.15)
        self.play(Write(k3), run_time=.4)
        self.at('by the half life')
        word = T('half-life', size=34, color=GOLD).next_to(k3, RIGHT, buff=.15)
        self.play(TransformFromCopy(P['b1'][1], word), run_time=1.0)
        self.at('k is about')
        line = VGroup(k1, k2, k3, word)
        fin = T('k ≈ 0.069 per minute', size=34, color=GOLD).move_to([3.7, 2.7, 0])
        self.play(Transform(line, fin), run_time=1.2)
        self.at('per minute')
        self.play(Indicate(line, color=GOLD), run_time=1.0)
        self.finish()


class S09Oneway(SpokenScene):
    def construct(self):
        W = trackers(self, T0=0, link=True)
        cell, mk = left_world(self, W, 0, 12)
        P = plot_base(self, dots=4, crv=20, dot20=True)
        # the first securin is destroyed for good
        p0 = min(cell.secs)
        slot = cell.P(*SLOTS[p0])
        self.at('each securin')
        ghost = DashedVMobject(RoundedRectangle(corner_radius=.09, width=.3, height=.195, color=PURPLE, stroke_width=2).move_to(slot))
        self.play(cell.drain(1, 1.4), FadeIn(ghost), run_time=1.4)
        frs = VGroup(*[Square(side_length=.08, color=PURPLE, fill_opacity=1).move_to(cell.P(3.5 + .1 * i, -1.35 + (i % 2) * .1)) for i in range(4)])
        self.add(frs)
        self.play(frs.animate.shift(RIGHT * .3 + DOWN * .2).set_opacity(0), run_time=.7)
        cell.level_mode()
        self.at('gone for good')
        gl = T('gone for good', size=28).move_to([-4.3, -.65, 0])
        self.play(FadeIn(gl), run_time=.5)
        self.at('while none')
        ring = Circle(radius=.2, color=GOLD, stroke_width=5)
        ring.add_updater(lambda m: m.move_to(pt(W['T'].get_value())))
        ring.move_to(pt(0))
        self.add(ring)
        self.play(FadeOut(gl), run_time=.4)
        self.play(W['T'].animate.set_value(12), run_time=4.4, rate_func=linear)
        self.at('one way')
        ch = chevron()
        self.play(W['T'].animate.set_value(20), FadeIn(ch), run_time=3.3, rate_func=linear)
        self.finish()


class S10Return(SpokenScene):
    def construct(self):
        W = trackers(self, T0=20, link=True)
        cell, mk = left_world(self, W, 20, 12)
        P = plot_base(self, dots=4, crv=20, dot20=True)
        cell.level_mode()
        ch = chevron(); self.add(ch)
        self.at('so read')
        self.play(W['T'].animate.set_value(0), run_time=1.5)
        ring = Circle(radius=.22, color=GOLD, stroke_width=5)
        ring.add_updater(lambda m: m.move_to(pt(W['T'].get_value())))
        ring.move_to(pt(0))
        self.at('every half')
        b1, bl1 = bracket(0, 10)
        self.play(FadeIn(ring), Create(b1), FadeIn(bl1), run_time=.8)
        self.add(ring)
        self.at('halves')
        self.play(W['T'].animate.set_value(10), run_time=1.3)
        self.at('what is left')
        b2, bl2 = bracket(10, 20, 'half-life')
        self.play(Create(b2), FadeIn(bl2), W['T'].animate.set_value(20), run_time=1.3)
        self.at('one number')
        self.play(Indicate(bl1, color=GOLD), run_time=.8)
        self.at('predict')
        pr = curve(20, 30, dashed=True)
        self.play(Create(pr), run_time=2.0)
        self.finish()


class S11End(EndCard):
    LINE = 'Every half-life halves what is left.'
