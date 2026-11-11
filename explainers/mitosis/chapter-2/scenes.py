"""Two Motions Pull the Sisters Apart: chapter 2 of the mitosis film pair.
COLOR MAP (same as chapter 1): BLUE sisters; ORANGE kinetochores / anaphase A; TEAL cohesin;
YELLOW poles / anaphase B; GREY spindle and cell; PURPLE motors; GREEN separase / dynein; GLOW bright tubulin.
One world: a cell whose poles and sisters move by the same clock (a tracker `tm`, minutes). The same world is
drawn full size, as a thin strip above a position-versus-time plot, and zoomed on one pole.
All positions are computed from one set of example rates (anaphase A 1.0, anaphase B 1.0 um/min); schematic.
"""
from bp_style import *

ORANGE = '#F29E4C'
PURPLE = '#B58CD9'
PINK = '#E58AB0'
GLOW = '#D8FFD2'

KIN0, KINV, POLE0, POLEV = .43, 1.05, 4.2, .35   # world units; 1 um = 0.7 units
kin_x = lambda t: KIN0 + KINV * t
pole_x = lambda t: POLE0 + POLEV * t
HY, OY = 1.0, -1.0
CFG = {'full': dict(ax=0., bx=1., cx=0., ay=-.55, by=1., k=1.),
       'strip': dict(ax=0., bx=1., cx=0., ay=2.55, by=.36, k=.36),
       'zoom': dict(ax=-6.0, bx=3., cx=3., ay=-2.2, by=3., k=3.)}


def label(words, x=0, y=3.12, color=TEXT, size=34, width=12.5):
    text = fit(T(words, size, color), max_w=width).move_to([x, y, 0])
    back = Rectangle(width=text.width + .16, height=text.height + .10, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(text)
    return VGroup(back, text).set_z_index(20)


def seg(m, a, b):
    m.set_points_by_ends(np.array([a[0], a[1], 0.]), np.array([b[0], b[1], 0.]))


def rec(m):
    for s in m.family_members_with_points():
        s._fo, s._so = s.get_fill_opacity(), s.get_stroke_opacity()


def appear(m, a):
    for s in m.family_members_with_points():
        s.set_fill(opacity=a * getattr(s, '_fo', 1))
        s.set_stroke(opacity=a * getattr(s, '_so', 1))


def fade_to(m, a0, a1):
    return UpdateFromAlphaFunc(m, lambda mob, al: appear(mob, a0 + (a1 - a0) * al), suspend_mobject_updating=False)


def bracket(fa, fb, fy, color, h=.16, sw=6):
    g = VGroup(*[Line(ORIGIN, RIGHT) for _ in range(3)]).set_stroke(color, sw)

    def upd(m):
        a, b, y = fa(), fb(), fy()
        seg(m[0], [a, y], [b, y]); seg(m[1], [a, y - h], [a, y + h]); seg(m[2], [b, y - h], [b, y + h])
    g.add_updater(upd); upd(g)
    return g.set_z_index(8)


class Fib(VGroup):
    pass


class World:
    def __init__(s, sc, t=0., mode='full'):
        s.sc = sc
        s.tm = ValueTracker(t)
        s.c = {k: ValueTracker(v) for k, v in CFG[mode].items()}
        s.spread = ValueTracker(1. if mode == 'zoom' else 0.)
        s.near, s.far = VGroup(), VGroup()
        s.build()

    # mapping from world units to the screen; cx makes the zoom follow the left pole
    def v(s, k): return s.c[k].get_value()
    def K(s): return s.v('k')
    def t(s): return s.tm.get_value()
    def X(s, x): return s.v('ax') + s.v('bx') * x + s.v('cx') * pole_x(s.t())
    def Y(s, y): return s.v('ay') + s.v('by') * y
    def P(s, x, y): return np.array([s.X(x), s.Y(y), 0.])
    def pole_pos(s, side): return s.P(side * pole_x(s.t()), 0)
    def kin_pos(s, side, y): return s.P(side * kin_x(s.t()), y)

    def fibre(s, side, y, n):
        g = Fib(*[Line(ORIGIN, RIGHT, color=GREY, stroke_width=2.8) for _ in range(n)])
        g.lines = VGroup(*g.submobjects)
        g.dots = VGroup(*[Dot(radius=.045, color=TEXT) for _ in range(n)])
        g.add(g.dots)
        g._t = side * .37 + y * .1

        def upd(m, dt):
            m._t += dt
            a, b = s.pole_pos(side), s.kin_pos(side, y)
            for i, (ln, d) in enumerate(zip(m.lines, m.dots)):
                off = np.array([0, (i - (n - 1) / 2) * .12 * s.K() * s.spread.get_value(), 0])
                seg(ln, a + off, b + off)
                d.move_to(a + off + (b - a) * ((m._t * .33 + i * .25) % 1))
        g.add_updater(upd); upd(g, 0)
        return g.set_z_index(0)

    def build(s):
        sc = s.sc
        cell = Ellipse(width=12.8, height=5.65, color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.055).set_z_index(-5)

        def ucell(m):
            m.stretch_to_fit_width(12.8 * s.v('bx')); m.stretch_to_fit_height(5.65 * s.v('by')); m.move_to(s.P(0, 0))
        cell.add_updater(ucell); ucell(cell)
        s.cell = cell
        s.pol, s.rod, s.kin, s.fib = {}, {}, {}, {}
        for side in (-1, 1):
            d = Dot(radius=.19, color=YELLOW).set_z_index(2)
            d.add_updater(lambda m, side=side: (m.move_to(s.pole_pos(side)), m.set_width(2 * .19 * (.6 + .4 * s.K()))))
            s.pol[side] = d
            for who, y in (('h', HY), ('o', OY)):
                r = RoundedRectangle(width=.29, height=1.45, corner_radius=.13, color=BLUE, fill_color=BLUE, fill_opacity=.68, stroke_width=3).set_z_index(4)
                kd = Dot(radius=.115, color=ORANGE).set_z_index(5)

                def ur(m, side=side, y=y):
                    K = s.K()
                    m.stretch_to_fit_width(.29 * K ** .75); m.stretch_to_fit_height(1.45 * K)
                    m.move_to(s.kin_pos(side, y) - np.array([side * .2 * K ** .75, 0, 0]))

                def uk(m, side=side, y=y):
                    m.set_width(2 * .115 * s.K() ** .75); m.move_to(s.kin_pos(side, y))
                r.add_updater(ur); kd.add_updater(uk); ur(r); uk(kd)
                s.rod[(who, side)], s.kin[(who, side)] = r, kd
                s.fib[(who, side)] = s.fibre(side, y, 4 if who == 'h' else 1)
            d.add_updater  # (poles already have their updater)
        for side in (-1, 1):
            for m in (s.pol[side], s.rod[('h', side)], s.kin[('h', side)], s.fib[('h', side)]):
                (s.near if side == -1 else s.far).add(m)
            for who in ('o',):
                for m in (s.rod[(who, side)], s.kin[(who, side)], s.fib[(who, side)]):
                    s.far.add(m)
        s.far.add(cell)
        s.far.remove(s.pol[-1])
        s.near.add(s.pol[-1])
        every = [cell] + list(s.pol.values()) + list(s.rod.values()) + list(s.kin.values()) + list(s.fib.values())
        for m in every:
            for sub in [m]:
                pass
        for m in every:
            rec(m)
        sc.add(*every)
        s.every = every

    def hide_far(s): appear(s.far, 0)

    def y_at(s, x):
        a, b = s.pole_pos(-1), s.kin_pos(-1, HY)
        return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])

    def to(s, mode, extra=(), **kw):
        kw.setdefault('run_time', 2.0)
        s.sc.play(*[s.c[k].animate.set_value(CFG[mode][k]) for k in CFG[mode]],
                  s.spread.animate.set_value(1. if mode == 'zoom' else 0.), *extra, **kw)


class Film(SpokenScene):
    def move(s, w, v, until, nth=0, lead=.2, extra=()):
        d = s.t_of(until, nth) - lead - s.elapsed()
        if d > .05:
            s.play(w.tm.animate.set_value(v), *extra, run_time=d, rate_func=linear)

    def tail(s, w, v):
        d = s.narration_s - .1 - s.elapsed()
        if d > .05:
            s.play(w.tm.animate.set_value(v), run_time=d, rate_func=linear)
        s.finish()


def pulse_ring(sc, p, color=YELLOW, r=.5):
    sc.play(Flash(p, color=color, flash_radius=r, line_length=.18), run_time=.7)


def glow_fibres(w, on=True):
    col = GLOW if on else GREY
    return [w.fib[('h', -1)].lines.animate.set_color(col).set_stroke(width=4.5 if on else 2.8),
            w.fib[('h', -1)].dots.animate.set_color(col if on else TEXT)]


def drip(origin_fn, vec, n=6, speed=.5, color=GREY, r=.06):
    g = VGroup(*[Dot(radius=r, color=color) for _ in range(n)])
    g._ph = [i / n for i in range(n)]

    def upd(m, dt):
        for i, d in enumerate(m):
            m._ph[i] = (m._ph[i] + dt * speed) % 1
            u = m._ph[i]
            d.move_to(origin_fn() + vec * u + np.array([.12 * np.sin(u * 9 + i), 0, 0]))
            d.set_fill(opacity=np.sin(np.pi * u))
    g.add_updater(upd); upd(g, 0)
    return g.set_z_index(9)


def stripe_band(w, xs, w_=.7, h=2.0):
    r = Rectangle(width=w_, height=h, stroke_color=GREY, stroke_width=1.5, fill_color=BG, fill_opacity=.97).set_z_index(3)
    r.add_updater(lambda m: m.move_to([xs.get_value(), w.y_at(xs.get_value()), 0]))
    r.get_center()
    r.move_to([xs.get_value(), w.y_at(xs.get_value()), 0])
    return r


# ------------------------------------------------------------------ the kymograph (position against time)
class Kymo:
    Y0, DY = 1.3, .95

    def __init__(s, w):
        s.w = w
        tm = w.tm
        s.lines, s.tips = VGroup(), VGroup()
        s.pole_lines = VGroup()
        for side in (-1, 1):
            for fn, col in ((pole_x, YELLOW), (kin_x, ORANGE)):
                ln = Line(ORIGIN, RIGHT, color=col, stroke_width=5).set_z_index(6)
                tip = Dot(radius=.1, color=col).set_z_index(7)

                def u(m, side=side, fn=fn):
                    t = tm.get_value(); seg(m, [side * fn(0), s.Y0], [side * fn(t), s.Y0 - s.DY * t])

                def ut(m, side=side, fn=fn):
                    t = tm.get_value(); m.move_to([side * fn(t), s.Y0 - s.DY * t, 0])
                ln.add_updater(u); tip.add_updater(ut); u(ln); ut(tip)
                s.lines.add(ln); s.tips.add(tip)
                if col == YELLOW:
                    s.pole_lines.add(ln)
        s.band = Polygon(*[[0, 0, 0], [1, 0, 0], [1, -1, 0]], stroke_width=0, fill_color=BLUE, fill_opacity=.38).set_z_index(1)

        def ub(m):
            t = tm.get_value(); k0, k1 = kin_x(0), kin_x(t); y1 = s.Y0 - s.DY * t
            m.set_points_as_corners([[-k0, s.Y0, 0], [k0, s.Y0, 0], [k1, y1 - 1e-3, 0], [-k1, y1 - 1e-3, 0], [-k0, s.Y0, 0]])
        s.band.add_updater(ub); ub(s.band)
        ytop, ybot = s.Y0, s.Y0 - 4 * s.DY
        s.axes = VGroup(Line([-5.8, ytop, 0], [-5.8, ybot, 0], color=GREY, stroke_width=2))
        for t_, txt in ((0, '0'), (2, '2'), (4, '4')):
            y = s.Y0 - s.DY * t_
            s.axes.add(Line([-5.8, y, 0], [-5.68, y, 0], color=GREY, stroke_width=2), T(txt, 24, TEXT).move_to([-6.15, y, 0]))
        s.axes.add(T('time (min)', 24, TEXT).rotate(PI / 2).move_to([-6.55, (ytop + ybot) / 2, 0]))
        for um, txt in ((-8, '-8 µm'), (-4, '-4'), (0, '0'), (4, '4'), (8, '8 µm')):
            s.axes.add(T(txt, 24, TEXT).move_to([um * .7, -2.85, 0]))
        s.all = VGroup(s.band, s.lines, s.tips, s.axes)
        for m in (s.band, s.lines, s.tips, s.axes):
            rec(m)

    def add(s, sc):
        sc.add(s.band, s.lines, s.tips, s.axes)


def tag(l1, l2, color, x, y, size=28):
    g = VGroup(T(l1, size, color), T(l2, size, color)).arrange(DOWN, buff=.08)
    back = Rectangle(width=g.width + .3, height=g.height + .2, stroke_width=0, fill_color=BG, fill_opacity=.96)
    return VGroup(back, g).move_to([x, y, 0]).set_z_index(20)


def eq_text(x, y):
    parts = VGroup(T('=', 34), T('2', 34), T('A', 34, ORANGE), T('+', 34), T('B', 34, YELLOW)).arrange(RIGHT, buff=.2)
    return parts.move_to([x, y, 0])


def stack_arrows(w, color, ymode):
    pass


# ------------------------------------------------------------------ scenes
class S00Hook(Film):
    def construct(s):
        w = World(s, 0.)
        rings = VGroup()
        for y in (HY, OY):
            for dy in (-.14, .14):
                rings.add(Ellipse(width=.86, height=.28, color=TEAL, stroke_width=4).move_to(w.P(0, y) + UP * dy))
        rings.set_z_index(6)
        s.add(rings)
        sep = VGroup(Ellipse(width=1.15, height=.72, color=GREEN, fill_color=GREEN, fill_opacity=.55, stroke_width=3),
                     T('separase', 28, GREEN).shift(UP * .75)).move_to([-2.0, 1.55, 0]).set_z_index(10)
        s.at('separés')
        s.play(FadeIn(sep), run_time=.6)
        s.at('cut the')
        s.play(sep.animate.move_to([.55, w.P(0, HY)[1] + .4, 0]), run_time=.5)
        s.play(Flash(w.P(0, HY), color=GREEN, flash_radius=.5), run_time=.5)
        s.at('links')
        frags = VGroup()
        vecs = []
        for i, rg in enumerate(rings):
            c = rg.get_center()
            for j in range(3):
                frags.add(Arc(radius=.16, start_angle=j * 2.1, angle=1.3, color=TEAL, stroke_width=4).move_to(c + RIGHT * (j - 1) * .22).set_z_index(6))
                vecs.append(np.array([(j - 1) * .9 + (.4 if i % 2 else -.4), (.7 if i < 2 else -.7) * (1 if (i + j) % 2 else -1), 0]))
        s.remove(rings); s.add(frags)
        s.play(*[f.animate.shift(v).set_opacity(0) for f, v in zip(frags, vecs)], FadeOut(sep), w.tm.animate.set_value(.35), run_time=1.7)
        s.move(w, .7, 'but what carries')
        q = label('What carries them apart?', 0, 3.12, TEXT, 40)
        s.at('but what carries')
        s.play(FadeIn(q, shift=DOWN * .1), run_time=.5)
        s.move(w, 1.0, 'two things move')
        s.at('two things move')
        arrs = VGroup()
        for side in (-1, 1):
            ao = Arrow(ORIGIN, RIGHT * .9, buff=0, color=ORANGE, stroke_width=7, tip_length=.2)
            ao.add_updater(lambda m, side=side: m.move_to(w.kin_pos(side, HY) + np.array([side * .75, 1.0, 0])).set_z_index(9)
                           if True else None)
            ay = Arrow(ORIGIN, RIGHT * .9, buff=0, color=YELLOW, stroke_width=7, tip_length=.2)
            ay.add_updater(lambda m, side=side: m.move_to(w.pole_pos(side) + np.array([side * .85, 0, 0])).set_z_index(9))
            if side == -1:
                ao.rotate(PI); ay.rotate(PI)
            arrs.add(ao, ay)
        s.play(FadeIn(arrs), run_time=.5)
        s.tail(w, 1.7)


class S01Title(TitleCard):
    TITLE = 'Two Motions Pull the Sisters Apart'
    LESSON = 'Mitosis and Chromosome Segregation'

    def construct(s):
        w = World(s, 1.7)
        title = label(s.TITLE, 0, 3.12, TEXT, 40, 12)
        s.add(title)
        s.play(w.tm.animate.set_value(1.95), run_time=max(.1, s.narration_s - .07), rate_func=linear)


class S02Two(Film):
    def construct(s):
        w = World(s, 1.95)
        s.play(w.tm.animate.set_value(0.), run_time=1.5)
        oy = 1.75
        ob = VGroup(*[bracket(lambda sd=sd: w.X(sd * pole_x(w.t())), lambda sd=sd: w.X(sd * kin_x(w.t())), lambda: oy, ORANGE) for sd in (-1, 1)])
        lab = VGroup(label('anaphase A', -2.6, 2.12, ORANGE, 30), label('anaphase A', 2.6, 2.12, ORANGE, 30))
        s.at('in anaphase a')
        s.play(FadeIn(ob), FadeIn(lab), run_time=.5)
        s.move(w, 2.0, 'in anaphase b')
        s.at('in anaphase b')
        yb = bracket(lambda: w.X(-pole_x(w.t())), lambda: w.X(pole_x(w.t())), lambda: 2.6, YELLOW)
        drops = VGroup(*[DashedLine([0, -.55, 0], [0, 2.6, 0], color=YELLOW, stroke_width=3, dash_length=.15).set_opacity(.55) for _ in (0, 1)])
        for sd, d in zip((-1, 1), drops):
            d.add_updater(lambda m, sd=sd: m.become(DashedLine([w.X(sd * pole_x(w.t())), w.Y(0), 0], [w.X(sd * pole_x(w.t())), 2.6, 0],
                                                               color=YELLOW, stroke_width=3, dash_length=.15).set_opacity(.55)))
        ylab = label('anaphase B', 0, 3.12, YELLOW, 32)
        s.play(FadeIn(yb), FadeIn(drops.update()), FadeIn(ylab), run_time=.5)
        s.move(w, 3.4, 'the first changes')
        s.at('the first changes')
        s.play(Indicate(VGroup(*[l[1] for l in lab]), color=ORANGE, scale_factor=1.12), run_time=.8)
        s.move(w, 3.7, 'the second changes')
        s.at('the second changes')
        s.play(Indicate(ylab[1], color=YELLOW, scale_factor=1.12), run_time=.8)
        s.tail(w, 4.0)


class S03Fibre(Film):
    def construct(s):
        w = World(s, 3.6)
        s.play(*[w.c[k].animate.set_value(CFG['zoom'][k]) for k in CFG['zoom']], w.spread.animate.set_value(1.),
               w.tm.animate.set_value(.3), fade_to(w.far, 1, 0), run_time=2.0)
        w.hide_far()
        kf = label('k-fibre', -3.6, .5, TEXT, 34)
        s.at('k fiber')
        s.play(FadeIn(kf), run_time=.4)
        s.move(w, .45, 'bundle from a kinetochore')
        s.at('bundle from a kinetochore')
        s.play(Flash(w.kin_pos(-1, HY), color=ORANGE, flash_radius=.7), run_time=.7)
        s.move(w, .55, 'gets shorter')
        s.at('gets shorter')
        s.move(w, 1.4, 'a k fiber contains', lead=.3)
        s.at('a k fiber contains')
        s.play(w.spread.animate.set_value(1.8), run_time=1.0)
        s.move(w, 1.8, 'but where does it lose')
        qs = VGroup(T('?', 60, TEXT), T('?', 60, TEXT))
        qs[0].add_updater(lambda m: m.move_to(w.kin_pos(-1, HY) + np.array([-.7, 1.6, 0])))
        qs[1].add_updater(lambda m: m.move_to(w.pole_pos(-1) + np.array([.3, 1.3, 0])))
        for q in qs:
            q.set_z_index(12)
        s.at('but where does it lose')
        s.play(FadeIn(qs), w.spread.animate.set_value(1.0), run_time=.6)
        s.tail(w, 2.0)


def zoom_world(s, t):
    w = World(s, t, 'zoom')
    w.hide_far()
    return w


class S04Stripe(Film):
    def construct(s):
        w = zoom_world(s, 2.0)
        s.move(w, 2.15, 'made the fibers glow')
        s.at('made the fibers glow')
        tub = label('fluorescent tubulin', -3.6, 1.3, GLOW, 32)
        s.play(*glow_fibres(w), FadeIn(tub), run_time=.9)
        s.move(w, 2.3, 'in cultured mammalian cells')
        s.at('in cultured mammalian cells')
        cap = label('cultured mammalian cells, 1988', 0, -3.3, TEXT, 30)
        s.play(FadeIn(cap), run_time=.5)
        s.move(w, 2.4, 'then they bleached')
        s.play(FadeOut(tub), run_time=.3)
        s.at('then they bleached')
        a, b = w.pole_pos(-1), w.kin_pos(-1, HY)
        xs = ValueTracker((a[0] + b[0]) / 2)
        laser = Line([xs.get_value(), 3.0, 0], [xs.get_value(), -2.6, 0], color=TEXT, stroke_width=5).set_z_index(12)
        s.play(Create(laser), run_time=1.2, rate_func=linear)
        band = stripe_band(w, xs)
        s.add(band)
        s.play(Flash(band.get_center(), color=TEXT, flash_radius=.6), FadeOut(laser), run_time=.6)
        s.at('dark stripe')
        sl = label('bleached stripe', xs.get_value(), 1.4, TEXT, 32)
        s.play(FadeIn(sl), run_time=.4)
        s.move(w, 2.55, 'they tracked poles')
        s.at('they tracked poles')
        s.play(Flash(w.pole_pos(-1), color=YELLOW, flash_radius=.7), run_time=.7)
        s.move(w, 2.6, 'chromosomes')
        s.at('chromosomes')
        s.play(Flash(w.rod[('h', -1)].get_center(), color=BLUE, flash_radius=1.6), run_time=.7)
        s.move(w, 2.65, 'and the stripe')
        s.at('and the stripe')
        s.play(Flash(band.get_center(), color=TEXT, flash_radius=.9), run_time=.7)
        s.tail(w, 2.7)


def stripe_world(s, t, glow=True):
    """The experiment as left at the end of s04: carried to s05..s08 at the same place."""
    w = zoom_world(s, t)
    appear(w.fib[('h', -1)], 1)
    if glow:
        w.fib[('h', -1)].lines.set_color(GLOW).set_stroke(width=4.5)
        w.fib[('h', -1)].dots.set_color(GLOW)
    a, b = w.pole_pos(-1), w.kin_pos(-1, 1.0)
    xs_ = -6.0 + 3 * (pole_x(2.4) - kin_x(2.4)) / 2   # stripe x set at the bleach time (tm = 2.4)
    xs = ValueTracker(xs_)
    band = stripe_band(w, xs)
    s.add(band)
    return w, xs, band


class S05Predict(Film):
    def construct(s):
        w, xs, band = stripe_world(s, 2.6)
        winch = VGroup(Circle(radius=.3, color=TEXT, stroke_width=4),
                       *[Line(ORIGIN, .3 * np.array([np.cos(a), np.sin(a), 0]), color=TEXT, stroke_width=4) for a in (0, 2.1, 4.2)])
        winch.move_to([-5.9, -3.3, 0])
        winch._t = 0
        winch.add_updater(lambda m, dt: m.rotate(-.8 * dt))
        wl = label('reeled in at pole?', -3.4, -3.3, TEXT, 30)
        s.move(w, 2.7, 'pole reeled', lead=.1)
        s.at('pole reeled')
        s.play(FadeIn(winch), FadeIn(wl), run_time=.6)
        gx = ValueTracker(xs.get_value())
        ghost = Rectangle(width=.7, height=2.0, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.18).set_z_index(5)
        ghost.add_updater(lambda m: m.move_to([gx.get_value(), w.y_at(gx.get_value()), 0]))
        s.move(w, 2.8, 'the stripe would ride')
        s.at('the stripe would ride')
        s.add(ghost)
        s.play(gx.animate.set_value(-5.0), w.tm.animate.set_value(3.05), run_time=2.4, rate_func=linear)
        s.at('with the chromosome')
        s.play(Indicate(ghost, color=TEXT, scale_factor=1.15), run_time=.7)
        s.move(w, 3.1, 'so which way', lead=.7)
        s.play(FadeOut(ghost), FadeOut(winch), FadeOut(wl), run_time=.5)
        s.at('so which way')
        q = label('Which way does the stripe go?', -2.5, 3.4, TEXT, 40)
        s.play(FadeIn(q, shift=DOWN * .1), run_time=.5)
        s.tail(w, 3.15)


class S06Hold(NarratedScene):
    def construct(s):
        w, xs, band = stripe_world(s, 3.15)
        q = label('Which way does the stripe go?', -2.5, 3.4, TEXT, 40)
        q._t = 0
        q.add_updater(lambda m, dt: (setattr(m, '_t', m._t + dt), m.set_opacity(.8 + .2 * np.sin(m._t * 2.5))))
        icon = VGroup(Rectangle(width=.14, height=.5, stroke_width=0, fill_color=TEXT, fill_opacity=1).shift(LEFT * .14),
                      Rectangle(width=.14, height=.5, stroke_width=0, fill_color=TEXT, fill_opacity=1).shift(RIGHT * .14)).move_to([6.1, 3.4, 0])
        s.add(q, icon)
        s.wait(max(.1, s.narration_s - .07))


class S07Answer(Film):
    def construct(s):
        w, xs, band = stripe_world(s, 3.15)
        q = label('Which way does the stripe go?', -2.5, 3.4, TEXT, 40)
        icon = VGroup(Rectangle(width=.14, height=.5, stroke_width=0, fill_color=TEXT, fill_opacity=1).shift(LEFT * .14),
                      Rectangle(width=.14, height=.5, stroke_width=0, fill_color=TEXT, fill_opacity=1).shift(RIGHT * .14)).move_to([6.1, 3.4, 0])
        s.add(q, icon)
        s.play(FadeOut(q), FadeOut(icon), run_time=.5)
        yb = -3.0
        grey = bracket(lambda: w.pole_pos(-1)[0], lambda: xs.get_value(), lambda: yb, GREY, sw=5)
        same = label('same length', -4.6, -3.5, TEXT, 30)
        s.at('did not move')
        s.play(FadeIn(grey), FadeIn(same), run_time=.5)
        s.move(w, 3.2, 'the chromosome moved')
        s.at('the chromosome moved')
        ob = bracket(lambda: xs.get_value(), lambda: w.kin_pos(-1, HY)[0], lambda: yb, ORANGE, sw=6)
        short = label('shorter', -2.2, -3.5, ORANGE, 30)
        s.play(FadeIn(ob), FadeIn(short), run_time=.5)
        s.move(w, 3.62, 'so these fibers lost')
        s.at('so these fibers lost')
        dr = drip(lambda: w.kin_pos(-1, HY) + np.array([-.1, -.1, 0]), np.array([-.8, -2.6, 0]), n=7, speed=.45, color=ORANGE)
        s.add(dr)
        s.at('mainly at the kinetochore')
        lk = label('lost at kinetochore', 2.6, -1.3, ORANGE, 32)
        s.play(FadeIn(lk), run_time=.5)
        s.tail(w, 3.7)


class S08Flux(Film):
    def construct(s):
        w, xs, band = stripe_world(s, 3.6)
        pole_dr = drip(lambda: w.pole_pos(-1) + np.array([0, -.2, 0]), np.array([.1, -1.1, 0]), n=3, speed=.28)
        small = label('small loss not excluded', -3.2, -3.4, TEXT, 30)
        s.at('a small loss')
        s.add(pole_dr)
        s.play(FadeIn(small), run_time=.5)
        s.move(w, 3.62, 'poleward flux', lead=.3)
        s.at('poleward flux')
        s.play(FadeOut(small), run_time=.3)
        fl = label('poleward lattice flux', -4.4, 3.4, YELLOW, 32)
        s.play(FadeIn(fl), run_time=.5)
        s.at('lattice itself moves')
        more = drip(lambda: w.pole_pos(-1) + np.array([.3, -.2, 0]), np.array([-.1, -1.2, 0]), n=5, speed=.5)
        s.add(more)
        s.play(xs.animate.set_value(-5.1), run_time=3.2, rate_func=linear)
        s.at('in fruit fly embryos')
        cap = label('fruit-fly embryo / frog egg extract (schematic)', 0, -3.3, TEXT, 30)
        s.play(FadeIn(cap), run_time=.5)
        s.at('flux can contribute')
        s.play(Indicate(fl[1], color=YELLOW, scale_factor=1.12), run_time=.8)
        s.play(xs.animate.set_value(-5.15), run_time=max(.1, s.narration_s - .1 - s.elapsed()), rate_func=linear)
        s.finish()


class S09Engines(Film):
    def construct(s):
        w = World(s, 3.6, 'zoom')
        w.hide_far()
        appear(w.fib[('h', -1)], 1)
        s.play(*[w.c[k].animate.set_value(CFG['full'][k]) for k in CFG['full']], w.spread.animate.set_value(0.),
               w.tm.animate.set_value(3.7), fade_to(w.far, 0, 1), run_time=2.2)
        yb = bracket(lambda: w.X(-pole_x(w.t())), lambda: w.X(pole_x(w.t())), lambda: 2.6, YELLOW)
        drops = VGroup(*[DashedLine([0, 0, 0], [0, 1, 0]) for _ in (0, 1)])
        for sd, d in zip((-1, 1), drops):
            d.add_updater(lambda m, sd=sd: m.become(DashedLine([w.X(sd * pole_x(w.t())), w.Y(0), 0], [w.X(sd * pole_x(w.t())), 2.6, 0],
                                                               color=YELLOW, stroke_width=3, dash_length=.15).set_opacity(.55)))
        s.play(FadeIn(yb), FadeIn(drops.update()), run_time=.5)
        s.move(w, 3.75, 'in many animal cells')
        s.at('in many animal cells')
        mz = VGroup()
        for side in (-1, 1):
            for off in (-.25, 0, .25):
                ln = Line(ORIGIN, RIGHT, color=GREY, stroke_width=3)
                ln.add_updater(lambda m, side=side, off=off: seg(m, w.pole_pos(side), [w.X(-side * 1.1), w.Y(0) + off]))
                mz.add(ln)
        s.play(FadeIn(mz), run_time=.8)
        s.move(w, 3.82, 'motors slide')
        s.at('motors slide')
        blobs = VGroup(*[Ellipse(width=.3, height=.2, color=PURPLE, fill_color=PURPLE, fill_opacity=.85, stroke_width=1).move_to([w.X(x), w.Y(0) + o, 0]).set_z_index(9)
                         for x, o in ((-.7, .25), (-.35, 0), (0, -.25), (.35, 0), (.7, .25))])
        arr = VGroup(*[Arrow([w.X(sd * .2), w.Y(0) - .5, 0], [w.X(sd * 1.3), w.Y(0) - .5, 0], buff=0, color=PURPLE, stroke_width=7, tip_length=.2) for sd in (-1, 1)])
        pl = label('midzone motors', 0, w.Y(0) - 1.25, PURPLE, 32)
        for b_, ph in zip(blobs, range(5)):
            b_._t = ph
            b_.add_updater(lambda m, dt: (setattr(m, '_t', m._t + dt), m.shift(RIGHT * .12 * dt * np.cos(m._t * 2.0))))
        s.play(FadeIn(blobs), FadeIn(arr), FadeIn(pl), run_time=.7)
        s.move(w, 3.88, 'at the cell cortex', lead=.5)
        s.at('at the cell cortex')
        rays, duds = VGroup(), VGroup()
        for side in (-1, 1):
            for a in (0, .44, -.44, .8, -.8):
                bp = [w.X(side * 6.4 * np.cos(a)), w.Y(0) + 2.83 * np.sin(a)]
                ray = Line(ORIGIN, RIGHT, color=GREY, stroke_width=2.5)
                ray.add_updater(lambda m, side=side, bp=bp: seg(m, w.pole_pos(side), bp))
                d = Ellipse(width=.45, height=.26, color=GREEN, fill_color=GREEN, fill_opacity=.85, stroke_width=1).move_to([*bp, 0]).set_z_index(9)
                d._t = a * 3 + side
                d._o = np.array([bp[0] - w.X(0), bp[1] - w.Y(0), 0])
                d._o = d._o / np.linalg.norm(d._o)
                d.add_updater(lambda m, dt: (setattr(m, '_t', m._t + dt), m.shift(m._o * .12 * dt * np.cos(m._t * 2.0))))
                rays.add(ray); duds.add(d)
        dl = label('cortical dynein', -3.6, 3.12, GREEN, 32)
        s.play(FadeIn(rays), FadeIn(duds), FadeIn(dl), run_time=.9)
        s.move(w, 3.95, 'their balance differs', lead=.3)
        s.at('their balance differs')
        s.play(Indicate(pl[1], color=PURPLE, scale_factor=1.12), run_time=.7)
        s.play(Indicate(dl[1], color=GREEN, scale_factor=1.12), run_time=.7)
        s.tail(w, 4.0)


def strip_world(s, t):
    w = World(s, t, 'strip')
    return w


class S10Movie(Film):
    def construct(s):
        w = World(s, 4.0)
        s.play(*[w.c[k].animate.set_value(CFG['strip'][k]) for k in CFG['strip']], w.spread.animate.set_value(0.),
               w.tm.animate.set_value(0.), run_time=2.0)
        ky = Kymo(w)
        ky.add(s)
        appear(ky.all, 0)
        s.at('example numbers')
        s.play(fade_to(ky.axes, 0, 1), fade_to(ky.lines, 0, 1), fade_to(ky.tips, 0, 1), run_time=.6)
        illus = label('illustrative numbers', 0, -3.4, TEXT, 30)
        s.play(FadeIn(illus), run_time=.4)
        appear(ky.band, 0)
        ob = VGroup(*[bracket(lambda sd=sd: sd * pole_x(w.t()), lambda sd=sd: sd * kin_x(w.t()), lambda: ky.Y0 - ky.DY * w.t(), ORANGE, sw=6) for sd in (-1, 1)])
        yb = bracket(lambda: -pole_x(w.t()), lambda: pole_x(w.t()), lambda: ky.Y0 - ky.DY * w.t(), YELLOW, sw=6)
        otag = tag('anaphase A', '1.0 µm/min', ORANGE, -3.3, -1.5)
        ytag = tag('anaphase B', '1.0 µm/min', YELLOW, 0, -1.6)
        ytag.add_updater(lambda m: m.move_to([0, ky.Y0 - ky.DY * w.t() + .75, 0]))
        s.at('each kinetochore closes')
        s.add(ob)
        s.play(FadeIn(otag), w.tm.animate.set_value(.5), run_time=.8, rate_func=linear)
        s.move(w, 2.0, 'the poles separate')
        s.play(FadeOut(ob), FadeOut(otag), run_time=.3)
        s.at('the poles separate')
        s.add(yb)
        s.play(FadeIn(ytag), run_time=.4)
        s.move(w, 3.6, 'these are illustrative')
        s.play(FadeOut(yb), FadeOut(ytag), run_time=.3)
        s.at('these are illustrative')
        s.play(Indicate(illus[1], color=TEXT, scale_factor=1.12), w.tm.animate.set_value(4.0), run_time=2.2, rate_func=linear)
        s.finish()


def plot_world(s, t, band=True):
    w = World(s, t, 'strip')
    ky = Kymo(w)
    ky.add(s)
    return w, ky


def blocks_final():
    return chip('3.0 µm/min', BLUE, 27).move_to([-1.6, -3.55, 0]).set_z_index(10)


class S11Sum(Film):
    def construct(s):
        w, ky = plot_world(s, 4.0)
        s.play(w.tm.animate.set_value(0.), run_time=1.4)
        sl = label('sister separation', 0, -.2, BLUE, 32)
        s.at('sisters separate')
        sl.add_updater(lambda m: m.set_opacity(float(np.clip((w.t() - 2.3) / .3, 0, 1))))
        s.add(sl)
        s.play(w.tm.animate.set_value(.3), run_time=.5)
        d = s.t_of('each closes on its own pole') - .2 - s.elapsed()
        if d > .05:
            s.wait(d)
        s.at('each closes on its own pole')
        a1 = chip('A', ORANGE, 27).move_to([-6.0, -3.55, 0])
        a2 = chip('A', ORANGE, 27).move_to([-5.0, -3.55, 0])
        plus = T('+', 34).move_to([-4.2, -3.55, 0])
        b = chip('B', YELLOW, 27).move_to([-3.4, -3.55, 0])
        s.play(w.tm.animate.set_value(1.9), run_time=max(.1, s.t_of('two times one') - .2 - s.elapsed()), rate_func=linear)
        s.at('two times one')
        s.play(FadeIn(a1), FadeIn(a2), run_time=.5)
        s.play(w.tm.animate.set_value(2.4), run_time=max(.1, s.t_of('plus one') - .2 - s.elapsed()), rate_func=linear)
        s.at('plus one')
        s.play(FadeIn(plus), FadeIn(b), run_time=.5)
        s.play(w.tm.animate.set_value(3.0), run_time=max(.1, s.t_of('three micrometers') - .2 - s.elapsed()), rate_func=linear)
        s.at('three micrometers')
        grp = VGroup(a1, a2, b)
        s.play(FadeOut(plus), run_time=.25)
        s.play(a1.animate.move_to([-2.5, -3.55, 0]), a2.animate.move_to([-1.6, -3.55, 0]), b.animate.move_to([-.7, -3.55, 0]),
               w.tm.animate.set_value(3.4), run_time=.75)
        chip3 = blocks_final()
        s.play(ReplacementTransform(grp, chip3), run_time=.7)
        s.play(w.tm.animate.set_value(3.7), run_time=max(.1, s.t_of('in this symmetric movie') - .2 - s.elapsed()), rate_func=linear)
        s.at('twice a plus b')
        e = eq_text(1.5, -3.55)
        s.play(FadeIn(e), w.tm.animate.set_value(4.0), run_time=1.0)
        s.tail(w, 4.0)


class S12Blind(Film):
    def construct(s):
        w, ky = plot_world(s, 4.0)
        sl = label('sister separation', 0, -.2, BLUE, 32)
        sl.add_updater(lambda m: m.set_opacity(float(np.clip((w.t() - 2.3) / .3, 0, 1))))
        chip3 = blocks_final()
        s.add(sl, chip3)
        # poles become dotted outlines: the solid pole lines and dots fade, dashed copies stay
        rings = VGroup()
        for sd in (-1, 1):
            r = DashedVMobject(Circle(radius=.13, color=YELLOW, stroke_width=3), num_dashes=10)
            r.add_updater(lambda m, sd=sd: m.move_to(w.pole_pos(sd)))
            rings.add(r)
        dl = VGroup()
        for sd in (-1, 1):
            dline = DashedLine([sd * POLE0, ky.Y0, 0], [sd * POLE0, ky.Y0 - .01, 0], color=YELLOW, stroke_width=3, dash_length=.12)
            dline.add_updater(lambda m, sd=sd: m.become(
                DashedLine([sd * POLE0, ky.Y0, 0], [sd * pole_x(w.t()), ky.Y0 - ky.DY * w.t(), 0], color=YELLOW, stroke_width=3, dash_length=.12)
                if w.t() > .15 else Line([sd * POLE0, ky.Y0, 0], [sd * POLE0, ky.Y0 - .01, 0], color=YELLOW, stroke_width=3).set_opacity(0)))
            dl.add(dline)
        s.at('hide the poles')
        s.add(rings, dl)
        s.play(fade_to(w.pol[-1], 1, .2), fade_to(w.pol[1], 1, .2), fade_to(ky.pole_lines, 1, 0),
               fade_to(VGroup(ky.tips[0], ky.tips[2]), 1, 0), FadeIn(rings), run_time=.9)
        s.play(w.tm.animate.set_value(0.), run_time=.9)
        s.play(w.tm.animate.set_value(1.0), run_time=max(.1, s.t_of('a movie tracking') - .2 - s.elapsed()), rate_func=linear)
        s.at('a movie tracking')
        s.play(Indicate(chip3, color=BLUE, scale_factor=1.1), run_time=.8)
        s.play(w.tm.animate.set_value(2.0), run_time=max(.1, s.t_of('but cannot tell') - .2 - s.elapsed()), rate_func=linear)
        s.at('but cannot tell')
        e1 = T('=', 34).move_to([.7, -3.55, 0])
        bl = VGroup(chip('A', ORANGE, 27).move_to([1.7, -3.55, 0]), chip('A', ORANGE, 27).move_to([2.7, -3.55, 0]), chip('B', YELLOW, 27).move_to([3.7, -3.55, 0]))
        s.play(FadeIn(e1), FadeIn(bl), w.tm.animate.set_value(2.6), run_time=.8, rate_func=linear)
        s.play(w.tm.animate.set_value(3.0), run_time=max(.1, s.t_of('without that landmark') - .2 - s.elapsed()), rate_func=linear)
        s.at('without that landmark')
        s.play(w.tm.animate.set_value(3.3), run_time=.8, rate_func=linear)
        s.at('a and b')
        q = chip('?', GREY, 27).move_to([2.7, -3.55, 0])
        ql = label('A or B?', 5.4, -3.55, TEXT, 32)
        s.play(ReplacementTransform(bl, q), FadeIn(ql), w.tm.animate.set_value(3.7), run_time=1.0)
        s.tail(w, 4.0)


class S13Return(Film):
    def construct(s):
        w, ky = plot_world(s, 4.0)
        scene_lab = label('sister separation', 0, -.2, BLUE, 32)
        s.add(scene_lab)
        s.play(FadeOut(scene_lab), fade_to(ky.band, 1, 0), fade_to(ky.axes, 1, 0), fade_to(ky.lines, 1, 0), fade_to(ky.tips, 1, 0),
               *[w.c[k].animate.set_value(CFG['full'][k]) for k in CFG['full']], w.tm.animate.set_value(0.), run_time=2.0)
        s.remove(ky.band, ky.axes, ky.lines, ky.tips)
        oy = 1.75
        ob = VGroup(*[bracket(lambda sd=sd: w.X(sd * pole_x(w.t())), lambda sd=sd: w.X(sd * kin_x(w.t())), lambda: oy, ORANGE) for sd in (-1, 1)])
        olab = VGroup(label('anaphase A', -2.6, 2.12, ORANGE, 30), label('anaphase A', 2.6, 2.12, ORANGE, 30))
        s.at('chromosomes travel along')
        s.play(FadeIn(ob), FadeIn(olab), run_time=.5)
        s.move(w, 2.0, 'the poles spread apart')
        yb = bracket(lambda: w.X(-pole_x(w.t())), lambda: w.X(pole_x(w.t())), lambda: 2.6, YELLOW)
        drops = VGroup(*[DashedLine([0, 0, 0], [0, 1, 0]) for _ in (0, 1)])
        for sd, d in zip((-1, 1), drops):
            d.add_updater(lambda m, sd=sd: m.become(DashedLine([w.X(sd * pole_x(w.t())), w.Y(0), 0], [w.X(sd * pole_x(w.t())), 2.6, 0],
                                                               color=YELLOW, stroke_width=3, dash_length=.15).set_opacity(.55)))
        ylab = label('anaphase B', 0, 3.12, YELLOW, 32)
        s.at('the poles spread apart')
        s.play(FadeIn(yb), FadeIn(drops.update()), FadeIn(ylab), run_time=.5)
        s.move(w, 2.7, 'measure each against')
        s.at('measure each against')
        s.play(Indicate(VGroup(*[l[1] for l in olab]), color=ORANGE, scale_factor=1.12), Indicate(ylab[1], color=YELLOW, scale_factor=1.12), run_time=.8)
        s.move(w, 3.0, 'its own landmark')
        s.at('its own landmark')
        s.play(Flash(w.pole_pos(-1), color=YELLOW, flash_radius=.8), Flash(w.pole_pos(1), color=YELLOW, flash_radius=.8), run_time=.8)
        s.move(w, 3.3, 'those landmarks keep')
        s.at('those landmarks keep')
        sy = w.Y(0)
        sg = bracket(lambda: w.X(-kin_x(w.t())), lambda: w.X(kin_x(w.t())), lambda: sy, BLUE)
        sgl = label('sister gap', 0, -3.0, BLUE, 32)
        s.play(FadeIn(sg), FadeIn(sgl), run_time=.5)
        s.move(w, 3.65, 'sisters part by two motions')
        s.at('sisters part by two motions')
        s.play(Indicate(sgl[1], color=BLUE, scale_factor=1.15), run_time=.8)
        s.move(w, 3.85, 'chromosomes to poles')
        s.at('chromosomes to poles')
        s.play(Indicate(VGroup(*[l[1] for l in olab]), color=ORANGE, scale_factor=1.15), run_time=.7)
        s.move(w, 3.95, 'poles apart')
        s.at('poles apart')
        s.play(Indicate(ylab[1], color=YELLOW, scale_factor=1.15), run_time=.7)
        s.tail(w, 4.0)


class S14End(EndCard):
    LINE = 'Sisters part by two motions: chromosomes to poles, poles apart.'
