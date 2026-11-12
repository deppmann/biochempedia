"""Stopping Partway (high school Biology explainer, film 2 of 2: fermentation)

Same world and COLOUR MAP as film 1 (../scenes.py), so the two read as one film.
  SAND   = glucose (block of six segments; halves have three)
  GOLD   = ATP (round token, three beads), ADP (same token, two beads)
  AQUA   = water drops
  BLUE   = oxygen dots
  GREY   = carbon dioxide puffs, outlines
  OLIVE  = mitochondrion
  RED    = "no" marks, warnings
  SALMON = muscle
  ORANGE = lactate and ethanol (the leftovers of fermentation)
  TEXT   = vocabulary words and questions
Nothing here is a molecular structure. Anything not computed is labelled "schematic".
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

SAND = "#E3C48D"
SAND_EDGE = "#B99A5F"
AQUA = "#9EE6EE"
OLIVE = "#8FA43A"
BEAD = "#F3D77A"
MUSCLE = "#D98C7A"
SKIN = "#E0B090"
LACT = "#F29B3C"
LACT_EDGE = "#B8691C"
DOUGH = "#E8D3A8"
DOUGH_EDGE = "#B9935A"

# film 1's fixed positions
CELL_C = np.array([0.0, -0.2, 0.0])
MITO_C = np.array([2.6, 0.2, 0.0])
HALF_A = np.array([-3.6, 0.45, 0.0])
HALF_B = np.array([-3.6, -0.45, 0.0])
TOK_L = [(-3.6, -2.0), (-2.6, -2.0)]


# ---------------------------------------------------------------- helpers (shapes copied from film 1)
def motes(scene, n=26):
    rng = np.random.default_rng(sum(map(ord, scene.__class__.__name__)))
    field = VGroup()
    for _ in range(n):
        d = Dot([rng.uniform(-6.6, 6.6), rng.uniform(-3.6, 3.6), 0],
                radius=rng.uniform(.02, .045), color=rng.choice([GREY, TEAL])).set_opacity(rng.uniform(.16, .32))
        d.v = np.array([rng.uniform(-.12, .12), rng.uniform(.10, .22), 0])

        def drift(m, dt):
            m.shift(m.v * dt)
            if m.get_y() > 3.8:
                m.shift(DOWN * 7.6)
            if abs(m.get_x()) > 6.8:
                m.shift(LEFT * 13.6 * np.sign(m.get_x()))
        d.add_updater(drift)
        field.add(d)
    field.set_z_index(-20)
    scene.add(field)
    return field


def loop(scene, tr, period=1.8, lo=0.0, hi=1.0):
    tr.clear_updaters()
    tr.t = 0.0

    def u(m, dt):
        m.t += dt
        m.set_value(lo + (hi - lo) * (0.5 - 0.5 * np.cos(2 * np.pi * m.t / period)))
    tr.add_updater(u)
    scene.add(tr)


def tok(n=3, r=0.5):
    circ = Circle(radius=r, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=.25)
    bs = VGroup(*[Dot(radius=r * .17, color=BEAD) for _ in range(n)]).arrange(RIGHT, buff=r * .2)
    return VGroup(circ, bs)


def glucose(s=1.0):
    def row():
        return VGroup(*[Square(side_length=.34 * s, stroke_color=SAND_EDGE, stroke_width=2,
                               fill_color=SAND, fill_opacity=.95) for _ in range(3)]).arrange(RIGHT, buff=0)
    top, bot = row(), row()
    return VGroup(top, bot).arrange(DOWN, buff=0)


def half(s=1.0, n=3, color=SAND, edge=SAND_EDGE):
    return VGroup(*[Square(side_length=.34 * s, stroke_color=edge, stroke_width=2,
                           fill_color=color, fill_opacity=.95) for _ in range(n)]).arrange(RIGHT, buff=0)


def orange(s=1.0, n=3):
    return half(s, n, LACT, LACT_EDGE)


def to_orange(m):
    return m.animate.set_fill(LACT, opacity=.95).set_stroke(LACT_EDGE)


def drop(r=.12):
    return Circle(radius=r, stroke_color=AQUA, stroke_width=2, fill_color=AQUA, fill_opacity=.8)


def puff(r=.2):
    return Circle(radius=r, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=.6)


def o2dot(r=.1):
    return Dot(radius=r, color=BLUE)


def fibre(c, cx, cy, W, H):
    def build():
        v = c.get_value()
        w, h = W * (1 - .22 * v), H * (1 + .18 * v)
        body = RoundedRectangle(corner_radius=min(h / 2.2, .6), width=w, height=h, stroke_color=MUSCLE,
                                stroke_width=4, fill_color=MUSCLE, fill_opacity=.42).move_to([cx, cy, 0])
        stripes = VGroup(*[Line([cx + (k - 2.5) * w / 6, cy - h * .3, 0], [cx + (k - 2.5) * w / 6, cy + h * .3, 0],
                                stroke_color=MUSCLE, stroke_width=3).set_opacity(.55) for k in range(6)])
        return VGroup(body, stripes)
    return always_redraw(build)


def counter(v, abt=None):
    def build():
        s = "ATP rebuilt from this glucose: " + ("about " if abt is not None and abt.get_value() > .5 else "") + str(int(round(v.get_value())))
        t = T(s, 26, TEXT)
        t.move_to([6.7 - t.width / 2, 3.45, 0])
        return t
    return always_redraw(build)


def leg_mob(hip, a, b, L1=2.0, L2=2.0):
    hip = np.array([hip[0], hip[1], 0.0])
    knee = hip + L1 * np.array([np.sin(a), -np.cos(a), 0])
    ank = knee + L2 * np.array([np.sin(a - b), -np.cos(a - b), 0])
    foot = ank + np.array([.6, -.05, 0])
    th = Line(hip, knee, stroke_color=SKIN, stroke_width=38)
    sh = Line(knee, ank, stroke_color=SKIN, stroke_width=30)
    ft = Line(ank, foot, stroke_color=SKIN, stroke_width=20)
    for m in (th, sh, ft):
        m.set_cap_style(CapStyleType.ROUND)
    return VGroup(th, sh, ft, Dot(knee, radius=.2, color=SKIN))


def mito_mob(pos, w=4.4, h=2.8):
    body = Ellipse(width=w, height=h, stroke_color=OLIVE, stroke_width=5, fill_color=OLIVE, fill_opacity=.3)
    fold = ParametricFunction(lambda t: np.array([t, .45 * np.sin(2.6 * t) * np.cos(.8 * t), 0]),
                              t_range=[-w * .36, w * .36, .05], stroke_color="#C6D86A", stroke_width=4)
    return VGroup(body, fold).move_to(pos)


def dim(m, k=.3):
    m.set_stroke(opacity=k).set_fill(opacity=k * .35)
    return m


def cell_mob():
    return Ellipse(width=10.5, height=6.2, stroke_color=GREY, stroke_width=5,
                   fill_color=TEAL, fill_opacity=.16).move_to(CELL_C)


def tap(angle=0.0, x=-6.1, y=-1.5):
    pipe = RoundedRectangle(corner_radius=.08, width=1.5, height=.34, stroke_color=BLUE, stroke_width=4,
                            fill_color=BLUE, fill_opacity=.3).move_to([x, y, 0])
    stem = Line([x, y + .17, 0], [x, y + .5, 0], stroke_color=BLUE, stroke_width=6)
    bar = Line([x - .26, y + .5, 0], [x + .26, y + .5, 0], stroke_color=BLUE, stroke_width=7)
    bar.rotate(angle, about_point=np.array([x, y + .5, 0]))
    g = VGroup(pipe, stem, bar)
    g.bar = bar
    g.pivot = np.array([x, y + .5, 0])
    return g


def ox_stream(n=6, speed=1.0, x0=-5.3):
    ox = VGroup(*[o2dot() for _ in range(n)])
    span = 6.3
    for i, d in enumerate(ox):
        d.move_to([x0 + i * span / n, -1.5 + .12 * (-1) ** i, 0])
    keep = ValueTracker(1)

    def flow(m, dt):
        for i, d in enumerate(m):
            d.shift(RIGHT * speed * dt + UP * .18 * dt)
            if d.get_x() > 1.0:
                d.move_to([x0, -1.55, 0])
            d.set_opacity(1.0 if i % 3 == 0 else keep.get_value())
    ox.add_updater(flow)
    return ox, keep


def jiggle(m, amp=.05, w=2.0):
    m.base = m.get_center().copy()
    m.tt = float(np.random.default_rng(int(abs(m.base[0] * 7 + m.base[1] * 13)) + 1).uniform(0, 6))

    def u(mm, dt):
        mm.tt += dt
        mm.move_to(mm.base + np.array([amp * np.sin(w * mm.tt), amp * np.cos(1.3 * w * mm.tt), 0]))
    m.add_updater(u)


def pulse(m, color=GOLD):
    return Flash(m, color=color, flash_radius=max(m.width, m.height) * .5 + .15, line_length=.25, num_lines=14)


def tidy(m):
    m.clear_updaters()


def panel(w=12.6, h=5.5, c=(0, -.4)):
    return RoundedRectangle(corner_radius=.3, width=w, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=.16).move_to([c[0], c[1], 0])


def yeast_cell(w=1.0, h=.75, color=DOUGH_EDGE):
    return Ellipse(width=w, height=h, stroke_color="#8A6A35", stroke_width=3, fill_color=color, fill_opacity=1)


def wobble(m, amp=.1):
    m.base = [mm.get_center().copy() for mm in m]
    m.tt = 0.0

    def u(g, dt):
        g.tt += dt
        for i, (y, b) in enumerate(zip(g, g.base)):
            y.move_to(b + np.array([amp * np.sin(1.7 * g.tt + i * 1.3), amp * np.cos(2.1 * g.tt + i), 0]))
    m.add_updater(u)


def question_card(text, y=-3.0, size=34):
    t = T(text, size, YELLOW, weight=BOLD)
    fit(t, max_w=11.8)
    box = RoundedRectangle(corner_radius=.2, width=t.width + .7, height=t.height + .45, stroke_color=YELLOW,
                           stroke_width=3, fill_color=BG, fill_opacity=.92).move_to([0, y, 0])
    t.move_to(box)
    return VGroup(box, t)


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Respiration and ATP"
    TITLE = "Stopping Partway"


class S01Question(SpokenScene):
    def construct(self):
        motes(self)
        PL, PR = np.array([-3.4, -.45, 0]), np.array([3.4, -.45, 0])
        pl = RoundedRectangle(corner_radius=.25, width=6.2, height=5.0, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.18).move_to(PL)
        pr = RoundedRectangle(corner_radius=.25, width=6.2, height=5.0, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.18).move_to(PR)
        # sprinting leg (left), always moving
        ph = ValueTracker(0)
        ph.add_updater(lambda m, dt: m.set_value(m.get_value() + dt * 5.0))
        self.add(ph)

        def leg_build():
            tt = ph.get_value()
            a = .5 + .5 * np.sin(tt)
            b = .55 + .55 * np.sin(tt + 1.4)
            return leg_mob([-3.5, .85], a, max(b, 0), 1.35, 1.35)
        leg = always_redraw(leg_build)
        # dough ball in plastic wrap (right)
        dough = Ellipse(width=3.6, height=2.6, stroke_color=DOUGH_EDGE, stroke_width=4, fill_color=DOUGH,
                        fill_opacity=.55).move_to(PR + [0, -.9, 0])
        wrap = DashedVMobject(Ellipse(width=4.1, height=3.1, stroke_color=TEXT, stroke_width=3).move_to(PR + [0, -.9, 0]),
                              num_dashes=26)
        yeast = VGroup(*[yeast_cell(.5, .36).move_to(PR + [x, -.9 + y, 0])
                         for x, y in [(-1.0, .3), (.1, .6), (.9, -.1), (-.4, -.5), (1.1, .5), (.3, -.7)]])
        wobble(yeast, .12)
        # two slow oxygen taps
        taps = []
        for x in (-3.4, 3.4):
            t_ = tap(-PI / 3, x=x, y=1.55)
            taps.append(t_)
        lab_o = [T("oxygen", 28, BLUE).move_to([x + 1.7, 1.55, 0]) for x in (-3.4, 3.4)]
        drops = VGroup()
        for x in (-3.4, 3.4):
            for k in range(2):
                d = o2dot(.11).move_to([x + .55, 1.35 - k * .9, 0])
                d.x0 = x + .55
                drops.add(d)

        def drip(m, dt):
            for d in m:
                d.shift(DOWN * .5 * dt)
                if d.get_y() < .2 and d.get_x() < 0:
                    d.move_to([d.x0, 1.35, 0])
                if d.get_y() < -.3 and d.get_x() > 0:
                    d.move_to([d.x0, 1.35, 0])
        drops.add_updater(drip)
        q = T("ATP without enough oxygen?", 40, YELLOW, weight=BOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(pl), FadeIn(pr), FadeIn(q, shift=DOWN * .2), run_time=.8)
        self.play(FadeIn(leg), FadeIn(dough), FadeIn(wrap), FadeIn(yeast), run_time=.8)
        self.add(drops)
        self.play(*[FadeIn(t_) for t_ in taps], *[FadeIn(l) for l in lab_o], run_time=.8)
        self.at("a sprinting leg")
        self.play(Indicate(pl, color=SKIN, scale_factor=1.03), run_time=1.0)
        self.at("yeast sealed")
        self.play(Indicate(pr, color=DOUGH_EDGE, scale_factor=1.03), run_time=1.0)
        self.at("both face")
        self.play(Indicate(q, scale_factor=1.12), run_time=1.0)
        self.finish()


class S02Link(SpokenScene):
    def construct(self):
        motes(self)
        v, abt = ValueTracker(0), ValueTracker(0)
        cnt = counter(v, abt)
        cell = cell_mob().set_fill(TEAL, .2)
        rep = T("replay: first film", 28, YELLOW).move_to([-4.4, 3.45, 0])
        tp = tap(0.0)
        self.play(FadeIn(cell, scale=.9), FadeIn(cnt), FadeIn(rep), FadeIn(tp), run_time=1.0)
        g = glucose(1.0).move_to([-5.6, .5, 0])
        self.at("glucose began")
        g.set_opacity(0)
        self.play(g.animate.set_opacity(1).move_to([-3.6, 0, 0]), run_time=1.6, rate_func=smooth)
        self.at("in the cytoplasm")
        lab = T("cytoplasm", 34, TEAL, weight=BOLD).move_to([0, 2.3, 0])
        self.play(FadeIn(lab, shift=DOWN * .2), run_time=.5)
        self.play(g[0].animate.move_to(HALF_A), g[1].animate.move_to(HALF_B), run_time=1.0)
        self.at("with oxygen")
        mito = mito_mob(MITO_C)
        ox, keep = ox_stream()
        self.add(ox)
        self.play(FadeIn(mito, scale=.8), FadeOut(lab), run_time=1.0)
        self.at("the mitochondrion")
        ml = T("mitochondrion", 32, OLIVE, weight=BOLD).move_to([2.55, -1.6, 0])
        self.play(FadeIn(ml), run_time=.5)
        self.at("finished the job")
        pieces = VGroup(*g[0], *g[1])
        spots = [(-0.3, .6), (.7, .3), (-.4, -.3), (1.6, .5), (1.0, -.5), (2.3, -.2)]
        self.play(*[p.animate.scale(.7).move_to(MITO_C + [x, y - .2, 0]) for p, (x, y) in zip(pieces, spots)], run_time=.9)
        outs = []
        for i, p in enumerate(pieces):
            outs.append(puff(.22).move_to(p.get_center()) if i < 3 else drop(.16).move_to(p.get_center()))
        self.play(*[ReplacementTransform(p, o) for p, o in zip(pieces, outs)], run_time=.4)
        self.play(*[o.animate.move_to([-2.1 + .55 * i, 1.6 + .1 * i, 0]) for i, o in enumerate(outs[:3])],
                  *[outs[3 + k].animate.move_to([1.9 + .7 * k, -1.85, 0]) for k in range(3)], run_time=.8)
        self.play(FadeOut(VGroup(*outs)), FadeOut(ml), run_time=.3)
        self.at("that gave about")
        self.play(v.animate.set_value(30), run_time=2.0, rate_func=linear)
        abt.set_value(1)
        self.play(pulse(cnt, GOLD), run_time=.8)
        self.at("now we turn")
        self.play(FadeOut(rep), tp.bar.animate.rotate(-PI / 3, about_point=tp.pivot), keep.animate.set_value(0),
                  run_time=1.6)
        self.at("the same cell")
        abt.set_value(0)
        self.play(v.animate.set_value(0), run_time=1.0)
        self.finish()


def stage2():
    """The carried world at the end of film 2's link scene: thin oxygen, counter at 0."""
    v = ValueTracker(0)
    cnt = counter(v)
    cell = cell_mob().set_fill(TEAL, .2)
    mito = mito_mob(MITO_C)
    ox, keep = ox_stream()
    keep.set_value(0)
    tp = tap(-PI / 3)
    return v, cnt, cell, mito, ox, keep, tp


class S03FirstSteps(SpokenScene):
    def construct(self):
        motes(self)
        v, cnt, cell, mito, ox, keep, tp = stage2()
        self.add(cell, mito, ox, tp, cnt)
        g = glucose(1.0).move_to([-6.0, 0, 0])
        self.add(g)
        self.play(g.animate.move_to([-4.9, 0, 0]), run_time=1.5, rate_func=linear)
        self.at("cytoplasm")
        lab = T("cytoplasm", 34, TEAL, weight=BOLD).move_to([0, 2.3, 0])
        self.play(FadeIn(lab, shift=DOWN * .2), g.animate.move_to([-4.5, 0, 0]), run_time=1.6, rate_func=linear)
        self.at("they need no")
        nl = T("no oxygen needed", 30, BLUE).move_to([-2.3, 1.2, 0])
        self.play(FadeIn(nl, shift=DOWN * .15), g.animate.move_to([-4.2, 0, 0]), run_time=1.6, rate_func=linear)
        self.at("and they are")
        nl2 = T("same first steps,", 30, TEXT).move_to([-2.3, 1.65, 0])
        self.play(FadeIn(nl2, shift=DOWN * .15), g.animate.move_to([-3.9, 0, 0]), run_time=1.5, rate_func=linear)
        adps = [tok(2, .38).move_to([*p, 0]) for p in TOK_L]
        self.play(FadeIn(adps[0], scale=.6), FadeIn(adps[1], scale=.6), g.animate.move_to([-3.6, 0, 0]), run_time=1.2,
                  rate_func=linear)
        self.at("glucose splits")
        self.play(g[0].animate.move_to(HALF_A), g[1].animate.move_to(HALF_B), run_time=1.2)
        self.at("the counter reaches")
        newt = [tok(3, .38).move_to([*p, 0]) for p in TOK_L]
        self.play(*[Transform(a, n) for a, n in zip(adps, newt)], v.animate.set_value(2), run_time=1.2)
        self.play(Flash(adps[0], color=BEAD, flash_radius=.55, line_length=.15),
                  Flash(adps[1], color=BEAD, flash_radius=.55, line_length=.15), run_time=.6)
        box = always_redraw(lambda: SurroundingRectangle(cnt, color=YELLOW, buff=.12))
        self.play(FadeIn(box), run_time=.4)
        self.finish()


class S04Stuck(SpokenScene):
    def construct(self):
        motes(self)
        v = ValueTracker(2)
        cnt = counter(v)
        cell = cell_mob().set_fill(TEAL, .2)
        mito = mito_mob(MITO_C)
        ox, keep = ox_stream()
        keep.set_value(0)
        tp = tap(-PI / 3)
        atps = [tok(3, .38).move_to([*p, 0]) for p in TOK_L]
        A = half().move_to(HALF_A)
        B = half().move_to(HALF_B)
        self.add(cell, mito, ox, tp, cnt, *atps, A, B)
        self.at("oxygen")
        o_l = T("too little oxygen", 30, BLUE).move_to([-4.8, -2.8, 0])
        self.play(FadeIn(o_l), Indicate(ox, color=BLUE, scale_factor=1.2), run_time=1.0)
        self.at("the mitochondrion")
        kcu = T("can't keep up", 32, RED, weight=BOLD).move_to([.3, 2.0, 0])
        self.play(FadeOut(o_l), FadeIn(kcu), Indicate(mito, color=OLIVE, scale_factor=1.06), run_time=1.0)
        path = DashedLine([-.7, .2, 0], [.9, .2, 0], color=TEXT, stroke_width=4, dash_length=.12)
        path.add_tip(tip_length=.22)
        self.play(Create(path), run_time=.6)
        WAIT = [(-3.6, 1.35), (-1.7, .95), (-1.7, .1), (-1.7, -.75)]
        new = [half().move_to([-6.2, y, 0]) for _, y in WAIT]
        self.at("keep up")
        self.play(*[n.animate.move_to([x, y, 0]) for n, (x, y) in zip(new, WAIT)], run_time=1.6)
        self.at("some halves")
        self.play(FadeOut(kcu), A.animate.move_to([-.5, .2, 0]), run_time=.8)
        self.at("can't go on")
        self.play(*[n.animate(rate_func=there_and_back).shift(RIGHT * .8) for n in new[1:]],
                  A.animate.move_to([1.3, .2, 0]).scale(.7).set_opacity(.5), run_time=2.0)
        self.remove(A)
        for n in new:
            jiggle(n, .05, 2.0)
        self.play(B.animate.move_to([-.5, .2, 0]), run_time=1.5)
        self.at("stop partway")
        sl = T("stops partway", 34, YELLOW, weight=BOLD).move_to([.3, 2.0, 0])
        self.play(FadeIn(sl, shift=DOWN * .15), B.animate.move_to([1.3, .2, 0]).scale(.7).set_opacity(.5), run_time=1.4)
        self.remove(B)
        self.at("energy stays")
        ll = T("energy locked inside", 34, GOLD, weight=BOLD).move_to([.3, 2.0, 0])
        self.play(Transform(sl, ll), LaggedStart(*[Indicate(n, color=GOLD, scale_factor=1.15) for n in new], lag_ratio=.15),
                  run_time=1.6)
        self.finish()


class S05Muscle(SpokenScene):
    def construct(self):
        motes(self)
        v = ValueTracker(2)
        cnt = counter(v)
        self.add(cnt)
        pn = panel()
        c = ValueTracker(0)
        fib = fibre(c, -1.0, -.65, 9.4, 3.0)
        lab = T("working muscle cell", 30, TEXT).move_to([-3.6, 1.85, 0])
        loop(self, c, 2.0, 0, .6)
        SLOT = lambda k: np.array([-1.5 + 1.1 * (k % 3), -.05 - .42 * (k // 3), 0])
        slot_n = [0]

        def cycle(rt=1.1):
            g = glucose(.95).move_to([-4.6, -.65, 0]).set_opacity(0)
            self.play(g.animate.set_opacity(1).move_to([-3.4, -.65, 0]), run_time=rt * .3)
            self.play(g[0].animate.shift(UP * .22), g[1].animate.shift(DOWN * .22), run_time=rt * .2)
            k = slot_n[0]
            self.play(to_orange(g[0]), to_orange(g[1]), run_time=rt * .15)
            self.play(g[0].animate.move_to(SLOT(k)), g[1].animate.move_to(SLOT(k + 1)), run_time=rt * .35)
            slot_n[0] += 2
        # first glucose arrives and settles before the word "halves"
        g0 = glucose(.95).move_to([-5.2, -.65, 0]).set_opacity(0)
        self.play(FadeIn(pn), FadeIn(fib), FadeIn(lab), g0.animate.set_opacity(1).move_to([-3.4, -.65, 0]), run_time=1.0)
        self.at("the halves")
        self.play(g0[0].animate.shift(UP * .22), g0[1].animate.shift(DOWN * .22), run_time=.6)
        self.at("become")
        ll = T("lactate", 34, LACT, weight=BOLD).move_to([.9, 1.75, 0])
        self.play(g0[0].animate.set_fill(LACT, opacity=.95).set_stroke(LACT_EDGE).move_to(SLOT(0)),
                  g0[1].animate.set_fill(LACT, opacity=.95).set_stroke(LACT_EDGE).move_to(SLOT(1)),
                  FadeIn(ll, shift=DOWN * .15), run_time=.9)
        slot_n[0] = 2
        self.at("lactate builds")
        cycle()
        cycle()
        self.at("than it can")
        ar = Arrow([4.0, -.65, 0], [5.9, -.65, 0], color=GREY, stroke_width=5, buff=0)
        ul = T("used slowly", 28, TEXT).move_to([4.95, -1.25, 0])
        tr = orange(.5).move_to([4.0, -.65, 0])
        tr.tt = 0.0

        def trick(m, dt):
            m.tt += dt
            a = (m.tt % 5.0) / 5.0
            m.move_to([4.0 + 1.6 * a, -.65, 0])
            m.set_opacity(min(1, 4 * a, 4 * (1 - a)))
        tr.add_updater(trick)
        self.play(GrowArrow(ar), FadeIn(ul), FadeIn(tr), run_time=.6)
        cycle()
        cycle()
        self.at("your leg")
        sp = T("hard sprint", 32, YELLOW, weight=BOLD).move_to([4.2, 1.85, 0])
        self.play(FadeIn(sp, shift=DOWN * .15), run_time=.5)
        loop(self, c, .9, 0, 1.0)
        cycle(1.2)
        self.finish()


class S06Yeast(SpokenScene):
    def construct(self):
        motes(self)
        v = ValueTracker(2)
        cnt = counter(v)
        self.add(cnt)
        pn = panel()
        DC = np.array([0, -.4, 0])
        dough = Ellipse(width=9.6, height=3.9, stroke_color=DOUGH_EDGE, stroke_width=4, fill_color=DOUGH,
                        fill_opacity=.5).move_to(DC)
        wrap = DashedVMobject(Ellipse(width=10.0, height=4.3, stroke_color=TEXT, stroke_width=3).move_to(DC), num_dashes=40)
        dg = VGroup(dough, wrap)
        YC = np.array([-3.3, -.6, 0])
        ycell = yeast_cell(2.0, 1.4).move_to(YC)
        small = VGroup(*[yeast_cell(.5, .36).move_to(p) for p in
                         [(1.8, -1.5, 0), (3.4, -.6, 0), (.9, -1.7, 0), (2.4, .3, 0)]])
        wobble(small, .1)
        yl = T("yeast", 30, TEXT).move_to([-3.3, .45, 0])
        hv = [half().move_to(YC + [0, .2, 0]), half().move_to(YC + [0, -.2, 0])]
        self.play(FadeIn(pn), FadeIn(dg), FadeIn(ycell), FadeIn(small), FadeIn(yl), *[FadeIn(h_) for h_ in hv], run_time=.7)
        self.at("the halves")
        # halves become ethanol pieces plus carbon dioxide puffs
        eth = [orange(1.0, 2).move_to([-.9, -.95, 0]), orange(1.0, 2).move_to([-.9, -1.4, 0])]
        puffs = [puff(.22).move_to([-1.6 + .45 * i, .1 + .15 * i, 0]) for i in range(3)]
        self.play(ReplacementTransform(hv[0], eth[0]), ReplacementTransform(hv[1], eth[1]),
                  *[FadeIn(p_, scale=.4) for p_ in puffs], run_time=.8)
        self.at("ethanol")
        el = T("ethanol", 32, LACT, weight=BOLD).move_to([-.9, -2.0, 0])
        self.play(FadeIn(el, shift=UP * .1), Indicate(eth[0], color=LACT), Indicate(eth[1], color=LACT), run_time=.8)
        self.at("carbon")
        cl = T("carbon dioxide", 32, GREY, weight=BOLD).move_to([0.0, 1.1, 0])
        self.play(FadeIn(cl, shift=DOWN * .1), *[Indicate(p_) for p_ in puffs], run_time=.8)
        self.at("the carbon dioxide")
        bubbles = VGroup(*[Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.25).move_to(p)
                           for r, p in [(.42, (1.0, .6, 0)), (.3, (2.2, -.2, 0)), (.5, (3.2, .7, 0)), (.28, (1.4, -1.0, 0)),
                                        (.36, (3.5, -1.2, 0)), (.24, (.4, .9, 0))]])
        bubbles.tt = 0.0
        bubbles.base = [b.get_center().copy() for b in bubbles]

        def bob(m, dt):
            m.tt += dt
            for i, (b, p) in enumerate(zip(m, m.base)):
                b.move_to(p + np.array([.06 * np.sin(1.4 * m.tt + i), .12 * np.sin(1.1 * m.tt + 2 * i), 0]))
        self.play(FadeOut(cl),
                  *[p_.animate.move_to(b.get_center()) for p_, b in zip(puffs, [bubbles[0], bubbles[5], bubbles[3]])],
                  LaggedStart(*[GrowFromCenter(b) for b in bubbles], lag_ratio=.15), run_time=1.6)
        bubbles.add_updater(bob)
        self.add(bubbles)
        self.at("bubbles")
        self.play(FadeOut(VGroup(*puffs)), run_time=.4)
        self.at("make bread")
        sw = T("dough swells", 32, TEXT).move_to([-4.7, 1.95, 0])
        self.play(FadeIn(sw), dg.animate.scale(1.12), run_time=1.6)
        self.play(dg.animate.scale(1.03), run_time=1.0)
        self.finish()


def mini_panel(kind, cx, cy=-.55, w=6.2, h=4.6):
    """Miniature of one panel for the 'fermentation' banner scene. Returns a dict of parts."""
    P = np.array([cx, cy, 0])
    parts = {}
    parts["panel"] = RoundedRectangle(corner_radius=.25, width=w, height=h, stroke_color=GREY, stroke_width=3,
                                      fill_color=GREY, fill_opacity=.16).move_to(P)
    if kind == "muscle":
        parts["body"] = VGroup(
            RoundedRectangle(corner_radius=.6, width=w - .6, height=1.9, stroke_color=MUSCLE, stroke_width=4,
                             fill_color=MUSCLE, fill_opacity=.42).move_to(P + [0, .25, 0]),
            *[Line(P + [(k - 2.5) * (w - .6) / 6, .35 - .6, 0], P + [(k - 2.5) * (w - .6) / 6, .35 + .6, 0],
                   stroke_color=MUSCLE, stroke_width=3).set_opacity(.5) for k in range(6)])
        leftover = "lactate"
    else:
        parts["body"] = VGroup(Ellipse(width=w - .5, height=2.5, stroke_color=DOUGH_EDGE, stroke_width=4,
                                       fill_color=DOUGH, fill_opacity=.5).move_to(P + [0, .35, 0]),
                               yeast_cell(.8, .6).move_to(P + [-2.2, -.2, 0]))
        leftover = "ethanol"
    parts["glu"] = glucose(.7).move_to(P + [-2.0, .35, 0])
    parts["hal"] = VGroup(half(.7).move_to(P + [-.2, .6, 0]), half(.7).move_to(P + [-.2, .1, 0]))
    n = 3 if kind == "muscle" else 2
    parts["left"] = VGroup(orange(.7, n).move_to(P + [1.7, .6, 0]), orange(.7, n).move_to(P + [1.7, .1, 0]))
    parts["mito"] = dim(mito_mob(P + [0, -1.45, 0], 2.2, 1.0), .35)
    parts["leftlab"] = T(leftover, 30, LACT, weight=BOLD).move_to(P + [1.7, 1.78, 0])
    r1 = DashedLine(P + [-1.5, .35, 0], P + [-.8, .35, 0], color=TEXT, stroke_width=4, dash_length=.1).add_tip(tip_length=.2)
    r2 = DashedLine(P + [.4, .35, 0], P + [1.0, .35, 0], color=TEXT, stroke_width=4, dash_length=.1).add_tip(tip_length=.2)
    parts["route1"], parts["route2"] = r1, r2
    if kind == "yeast":
        parts["puffs"] = VGroup(puff(.16).move_to(P + [.9, 1.15, 0]), puff(.12).move_to(P + [1.25, 1.0, 0]))
    return parts


class S07Name(SpokenScene):
    def construct(self):
        motes(self)
        v = ValueTracker(2)
        cnt = counter(v)
        self.add(cnt)
        # last frame of the yeast scene, rebuilt, which then shrinks into the right-hand panel
        big = VGroup(panel(), Ellipse(width=11.2, height=4.8, stroke_color=DOUGH_EDGE, stroke_width=4, fill_color=DOUGH,
                                      fill_opacity=.5).move_to([0, -.4, 0]))
        self.add(big)
        mu = mini_panel("muscle", -3.2)
        ye = mini_panel("yeast", 3.2)
        base = ("panel", "body", "glu", "mito")
        self.play(FadeTransform(big, VGroup(*[ye[k] for k in base])),
                  FadeIn(VGroup(*[mu[k] for k in base]), shift=RIGHT * .6), run_time=1.6)
        self.at("biologists call")
        ban = T("fermentation", 48, YELLOW, weight=BOLD).move_to([-3.6, 3.3, 0])
        self.play(Write(ban), run_time=1.4)
        self.at("it runs in")
        self.play(*[Create(d["route1"]) for d in (mu, ye)], *[FadeIn(d["hal"]) for d in (mu, ye)], run_time=1.0)
        self.play(*[Create(d["route2"]) for d in (mu, ye)], run_time=.8)
        self.at("never uses")
        nl = [T("mitochondrion: not used", 28, OLIVE).move_to([x, -3.3, 0]) for x in (-3.2, 3.2)]
        self.play(*[FadeIn(n_) for n_ in nl], *[Indicate(d["mito"], color=OLIVE, scale_factor=1.1) for d in (mu, ye)], run_time=1.0)
        self.at("watch the counter")
        box = always_redraw(lambda: SurroundingRectangle(cnt, color=YELLOW, buff=.12))
        self.play(FadeIn(box), pulse(cnt, YELLOW), run_time=1.0)
        self.at("turning the")
        self.play(*[ReplacementTransform(d["hal"], d["left"]) for d in (mu, ye)],
                  *[FadeIn(d["leftlab"]) for d in (mu, ye)], FadeIn(ye["puffs"]), run_time=1.4)
        self.at("adds nothing")
        zero = T("+0", 48, RED, weight=BOLD).move_to([.5, 3.45, 0])
        self.play(FadeIn(zero, scale=1.4), run_time=.5)
        self.play(zero.animate.shift(DOWN * .12), pulse(cnt, RED), run_time=1.0)
        self.at("both")
        self.play(*[Indicate(d["route1"], color=GOLD, scale_factor=1.4) for d in (mu, ye)],
                  *[Indicate(d["glu"], color=GOLD, scale_factor=1.15) for d in (mu, ye)], run_time=1.2)
        self.play(FadeOut(zero), run_time=.5)
        self.finish()


class S08Energy(SpokenScene):
    def construct(self):
        motes(self)
        v = ValueTracker(2)
        cnt = counter(v)
        self.add(cnt)
        Y0, H, BW = -2.6, 3.9, 1.3
        cols = [-4.4, .3, 4.2]
        bars = [Rectangle(width=BW, height=H, stroke_color=GREY, stroke_width=3).move_to([cx + .9, Y0 + H / 2, 0]) for cx in cols]
        trk = [ValueTracker(0) for _ in cols]
        fills = []
        for i, cx in enumerate(cols):
            def mk(i=i, cx=cx):
                f = trk[i].get_value()
                if i == 0:
                    return Rectangle(width=BW, height=max(.01, H * f), stroke_width=0, fill_color=SAND, fill_opacity=.9) \
                        .move_to([cx + .9, Y0 + H * f / 2, 0])
                top = min(.93, f) * H
                gold_h = max(0, H * f - .93 * H)
                body = Rectangle(width=BW, height=max(.01, top), stroke_width=0, fill_color=LACT, fill_opacity=.9) \
                    .move_to([cx + .9, Y0 + top / 2, 0])
                if gold_h <= 0.01:
                    return body
                cap = Rectangle(width=BW, height=gold_h, stroke_width=0, fill_color=GOLD, fill_opacity=1) \
                    .move_to([cx + .9, Y0 + top + gold_h / 2, 0])
                return VGroup(body, cap)
            fills.append(always_redraw(mk))
        gl = glucose(1.2).move_to([cols[0] - 1.1, Y0 + H * .5, 0])
        self.at("why only")
        l0 = T("energy in one glucose", 28, TEXT).move_to([cols[0] + .2, 2.45, 0])
        self.play(FadeIn(gl), FadeIn(bars[0]), FadeIn(fills[0]), FadeIn(l0), run_time=.8)
        self.play(trk[0].animate.set_value(1), run_time=1.4, rate_func=smooth)
        self.at("look at")
        lac = VGroup(orange(1.0).move_to([0, .17, 0]), orange(1.0).move_to([0, -.17, 0])).move_to([cols[1] - 1.1, Y0 + H * .5, 0])
        eth = VGroup(orange(1.0, 2).move_to([0, .17, 0]), orange(1.0, 2).move_to([0, -.17, 0])).move_to([cols[2] - 1.1, Y0 + H * .5, 0])
        l1 = T("lactate leftovers", 28, LACT).move_to([cols[1] + .6, 2.45, 0])
        l2 = T("ethanol leftovers", 28, LACT).move_to([cols[2] + .5, 2.45, 0])
        self.play(FadeIn(lac), FadeIn(eth), FadeIn(bars[1]), FadeIn(bars[2]), FadeIn(fills[1]), FadeIn(fills[2]),
                  FadeIn(l1), FadeIn(l2), run_time=.8)
        self.play(trk[1].animate.set_value(.93), trk[2].animate.set_value(.93), run_time=1.4)
        self.at("lactate and ethanol")
        ny = Y0 + .9 * H
        dl = DashedLine([cols[1] + .2, ny, 0], [6.1, ny, 0], color=TEXT, stroke_width=3, dash_length=.15)
        nl = T("nine-tenths", 28, TEXT).move_to([3.15, ny - .35, 0])
        self.play(Create(dl), run_time=1.2)
        self.at("9 tenths")
        self.play(FadeIn(nl), run_time=.5)
        self.at("that was in")
        cap = T("over 90 % left in the leftovers (schematic)", 28, TEXT).move_to([0, -3.35, 0])
        self.play(FadeIn(cap), Indicate(fills[1], color=LACT, scale_factor=1.03), Indicate(fills[2], color=LACT, scale_factor=1.03),
                  run_time=1.4)
        self.at("fermentation frees")
        self.play(trk[1].animate.set_value(1.0), trk[2].animate.set_value(1.0), run_time=.9)
        fl = T("freed: small part", 28, GOLD, weight=BOLD).move_to([3.15, 1.85, 0])
        self.play(FadeIn(fl, shift=DOWN * .1), run_time=.6)
        self.play(Indicate(fills[1], color=GOLD, scale_factor=1.04), Indicate(fills[2], color=GOLD, scale_factor=1.04),
                  run_time=1.0)
        self.finish()


def two_cells(with_mito=True):
    L, R = np.array([-3.4, -.3, 0]), np.array([3.4, -.3, 0])
    cl = Ellipse(width=5.8, height=3.8, stroke_color=GREY, stroke_width=5, fill_color=TEAL, fill_opacity=.2).move_to(L)
    cr = Ellipse(width=5.8, height=3.8, stroke_color=GREY, stroke_width=5, fill_color=TEAL, fill_opacity=.2).move_to(R)
    ml = mito_mob(L + [1.1, .8, 0], 2.4, 1.4)
    mr = dim(mito_mob(R + [1.3, .7, 0], 1.9, 1.1), .35)
    hl = T("with oxygen", 32, BLUE, weight=BOLD).move_to([-3.4, 2.05, 0])
    hr = T("fermentation", 32, LACT, weight=BOLD).move_to([3.4, 2.05, 0])
    return cl, cr, ml, mr, hl, hr


def cell_motes(cx, cy, n=7, seed=1):
    rng = np.random.default_rng(seed)
    g = VGroup(*[Dot([cx + rng.uniform(-2.2, 2.2), cy + rng.uniform(-1.0, 1.0), 0], radius=.045, color=TEAL).set_opacity(.5)
                 for _ in range(n)])
    g.base = [m.get_center().copy() for m in g]
    g.tt = 0.0

    def u(m, dt):
        m.tt += dt
        for i, (d, b) in enumerate(zip(m, m.base)):
            d.move_to(b + np.array([.25 * np.sin(.9 * m.tt + i * 2.1), .18 * np.cos(1.1 * m.tt + i), 0]))
    g.add_updater(u)
    return g


class S09Predict(SpokenScene):
    def construct(self):
        motes(self)
        cl, cr, ml, mr, hl, hr = two_cells()
        mt1, mt2 = cell_motes(-3.4, -.3, 7, 1), cell_motes(3.4, -.3, 7, 2)
        self.play(FadeIn(cl), FadeIn(cr), FadeIn(ml), FadeIn(mr), FadeIn(hl), FadeIn(hr), FadeIn(mt1), FadeIn(mt2), run_time=.5)
        ox, keep = ox_stream(5)
        ox.shift(RIGHT * 0)
        # oxygen dots flow in the left cell only
        for i, d in enumerate(ox):
            d.move_to([-6.2 + i * .75, -1.1 + .1 * (-1) ** i, 0])

        def flow(m, dt):
            for d in m:
                d.shift(RIGHT * .9 * dt)
                if d.get_x() > -.9:
                    d.move_to([-6.2, -1.1, 0])
        ox.clear_updaters()
        ox.add_updater(flow)
        self.add(ox)
        self.at("so suppose")
        badge = T("ATP needed: 30", 40, GOLD, weight=BOLD)
        bb = SurroundingRectangle(badge, color=GOLD, buff=.2, corner_radius=.15)
        bg = VGroup(bb, badge).move_to([0, 3.2, 0])
        self.play(FadeIn(bg, scale=.8), run_time=.8)
        self.at("no oxygen")
        self.play(Indicate(cr, color=LACT, scale_factor=1.03), run_time=1.0)
        self.at("how many")
        qc = question_card("How many glucose for 30 ATP by fermentation?")
        self.play(FadeIn(qc, shift=UP * .2), run_time=.8)
        self.finish()


class S10Pause(NarratedScene):
    def construct(self):
        motes(self)
        cl, cr, ml, mr, hl, hr = two_cells()
        mt1, mt2 = cell_motes(-3.4, -.3, 7, 1), cell_motes(3.4, -.3, 7, 2)
        badge = T("ATP needed: 30", 40, GOLD, weight=BOLD)
        bg = VGroup(SurroundingRectangle(badge, color=GOLD, buff=.2, corner_radius=.15), badge).move_to([0, 3.2, 0])
        qc = question_card("How many glucose for 30 ATP by fermentation?")
        ox = VGroup(*[o2dot() for _ in range(5)])
        for i, d in enumerate(ox):
            d.move_to([-6.2 + i * .75, -1.1 + .1 * (-1) ** i, 0])

        def flow(m, dt):
            for d in m:
                d.shift(RIGHT * .9 * dt)
                if d.get_x() > -.9:
                    d.move_to([-6.2, -1.1, 0])
        ox.add_updater(flow)
        self.add(cl, cr, ml, mr, hl, hr, mt1, mt2, ox, bg, qc)
        tr = ValueTracker(1)
        bar = always_redraw(lambda: Rectangle(width=max(.02, 12 * tr.get_value()), height=.18, stroke_width=0,
                                              fill_color=YELLOW, fill_opacity=.9).move_to([-6 + 6 * tr.get_value(), -3.62, 0]))
        self.add(bar)
        self.play(tr.animate.set_value(0), run_time=self.narration_s - .1, rate_func=linear)
        self.finish()


class S11Reveal(SpokenScene):
    def construct(self):
        motes(self)
        cl, cr, ml, mr, hl, hr = two_cells()
        mt1, mt2 = cell_motes(-3.4, -.3, 5, 1), cell_motes(3.4, -.3, 5, 2)
        badge = T("ATP needed: 30", 40, GOLD, weight=BOLD)
        bg = VGroup(SurroundingRectangle(badge, color=GOLD, buff=.2, corner_radius=.15), badge).move_to([0, 3.2, 0])
        n_atp_l, n_atp_r, n_glu_r = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        tl = always_redraw(lambda: T(f"1 glucose · {int(round(n_atp_l.get_value()))} ATP", 32, GOLD, weight=BOLD).move_to([-3.4, -2.7, 0]))
        trr = always_redraw(lambda: T(f"{int(round(n_glu_r.get_value()))} glucose · {int(round(n_atp_r.get_value()))} ATP", 32, GOLD,
                                      weight=BOLD).move_to([3.4, -2.7, 0]))
        eq = T("30 ATP ÷ 2 ATP per glucose = 15 glucose", 30, TEXT).move_to([0, -3.4, 0])
        self.add(cl, cr, ml, mr, hl, hr, mt1, mt2, bg, tl, trr)
        # the answer comes first, then it is shown
        self.play(FadeIn(eq, shift=UP * .15), Indicate(eq, color=YELLOW, scale_factor=1.08), run_time=1.2)
        self.at("with oxygen")
        # left cell: one glucose, all the way down
        g = glucose(.9).move_to([-4.7, 1.0, 0])
        self.play(FadeIn(g, shift=DOWN * .3), run_time=.4)
        self.play(g.animate.move_to([-4.7, -.1, 0]), run_time=.5)
        self.play(g[0].animate.move_to([-3.0, .6, 0]), g[1].animate.move_to([-3.0, 0, 0]), run_time=.4)
        self.play(g[0].animate.move_to([-2.4, .75, 0]).scale(.6), g[1].animate.move_to([-2.4, .45, 0]).scale(.6),
                  run_time=.4)
        outs = VGroup(*[tok(3, .26) for _ in range(5)]).arrange(RIGHT, buff=.1).move_to([-3.4, -1.15, 0])
        self.play(FadeOut(g), n_atp_l.animate.set_value(30), LaggedStart(*[FadeIn(o, scale=.4) for o in outs], lag_ratio=.15),
                  run_time=1.3, rate_func=linear)
        self.at("without it")
        pile = []

        def slot(k):
            return np.array([2.15 + .62 * (k % 5), -.55 - .38 * (k // 5), 0])
        for k in range(15):
            gk = glucose(.6).move_to([2.2, 1.0, 0])
            gk.set_opacity(0)
            self.play(gk.animate.set_opacity(1).move_to([2.2, .1, 0]), run_time=.12)
            self.play(gk.animate.move_to(slot(k)).scale(.85).set_fill(LACT, opacity=.95).set_stroke(LACT_EDGE),
                      n_glu_r.animate.set_value(k + 1), n_atp_r.animate.set_value(2 * (k + 1)), run_time=.28)
            pile.append(gk)
        self.at("that is about")
        self.play(pulse(trr, GOLD), Indicate(eq, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.at("times as much")
        self.play(Indicate(VGroup(*pile), color=LACT, scale_factor=1.1), run_time=1.0)
        self.at("for the same")
        self.play(pulse(tl, GOLD), pulse(trr, GOLD),
                  Indicate(bg, color=GOLD, scale_factor=1.1), run_time=1.2)
        self.finish()


class S12Speed(SpokenScene):
    def construct(self):
        motes(self)
        sp = ValueTracker(2.2)
        ph = ValueTracker(0)
        ph.add_updater(lambda m, dt: m.set_value(m.get_value() + dt * sp.get_value()))
        self.add(ph)

        def leg_build():
            tt = ph.get_value()
            a = .35 + .4 * np.sin(tt)
            b = .55 + .55 * np.sin(tt + 1.4)
            return leg_mob([4.5, 2.6], a, max(b, 0), 1.7, 1.7)
        leg = always_redraw(leg_build)
        mito = mito_mob([-4.3, 1.25, 0], 3.2, 1.9)
        blob = Ellipse(width=2.6, height=1.5, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=.2).move_to([-4.3, -1.5, 0])
        bl = T("cytoplasm", 28, TEAL).move_to(blob)
        thick = Line([-2.6, 1.25, 0], [3.7, 1.55, 0], stroke_color=GOLD, stroke_width=16).set_opacity(.55)
        thin = Line([-2.9, -1.5, 0], [3.9, -.1, 0], stroke_color=GOLD, stroke_width=6).set_opacity(.25)
        on_thin = ValueTracker(0)
        # gold tokens running along both lines
        dots = VGroup()
        for i in range(6):
            d = tok(3, .17)
            d.lane, d.f = 0, i / 6
            dots.add(d)
        for i in range(4):
            d = tok(3, .13)
            d.lane, d.f = 1, i / 4
            dots.add(d)

        def run(m, dt):
            for d in m:
                if d.lane == 0:
                    d.f = (d.f + dt * .22) % 1.0
                    d.move_to(thick.point_from_proportion(d.f))
                    d.set_opacity(1)
                else:
                    d.f = (d.f + dt * (.45 if on_thin.get_value() > .5 else .0)) % 1.0
                    d.move_to(thin.point_from_proportion(d.f))
                    d.set_opacity(1 if on_thin.get_value() > .5 else 0)
        dots.add_updater(run)
        l1 = T("with oxygen", 32, GOLD, weight=BOLD).move_to([.2, 2.2, 0])
        l2 = T("fermentation", 32, LACT, weight=BOLD).move_to([.2, -1.75, 0])
        ar_l = Rectangle(width=0, height=0)
        self.play(FadeIn(leg), FadeIn(mito), FadeIn(thick), FadeIn(l1), run_time=1.0)
        self.add(dots)
        self.at("fermentation does")
        self.play(FadeIn(blob), FadeIn(bl), FadeIn(thin), FadeIn(l2), run_time=1.0)
        self.at("it needs no")
        nol = T("no oxygen needed", 28, BLUE).move_to([-4.3, -2.7, 0])
        self.play(FadeIn(nol), run_time=.6)
        self.at("quickly")
        on_thin.set_value(1)
        self.play(thin.animate.set_opacity(1), run_time=.6)
        self.wait(.8)
        on_thin.set_value(0)
        self.play(thin.animate.set_opacity(.25), FadeOut(nol), run_time=.5)
        self.at("so a hard")
        self.play(sp.animate.set_value(6.0), run_time=1.2)
        on_thin.set_value(1)
        self.play(thin.animate.set_opacity(1), Indicate(l2, color=LACT), run_time=.8)
        self.at("the mitochondria")
        self.play(Indicate(mito, color=OLIVE, scale_factor=1.06), Indicate(thick, color=GOLD), run_time=1.2)
        self.at("yeast and")
        dough = Ellipse(width=2.6, height=1.5, stroke_color=DOUGH_EDGE, stroke_width=4, fill_color=DOUGH, fill_opacity=.55).move_to([4.7, -2.85, 0])
        wrap = DashedVMobject(Ellipse(width=3.0, height=1.9, stroke_color=TEXT, stroke_width=3).move_to([4.7, -2.85, 0]), num_dashes=22)
        yy = VGroup(*[yeast_cell(.4, .3).move_to([4.7 + x, -2.85 + y, 0]) for x, y in [(-.6, .1), (.1, .3), (.6, -.2), (-.2, -.35)]])
        wobble(yy, .08)
        dl = T("no other route", 28, LACT).move_to([1.6, -2.85, 0])
        self.play(FadeIn(dough), FadeIn(wrap), FadeIn(yy), run_time=.8)
        self.at("has no other")
        self.play(FadeIn(dl), run_time=.6)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        motes(self)
        Y1, Y2 = 1.45, -1.65
        X = [-5.3, -3.2]
        g1 = glucose(1.1).move_to([X[0], Y1, 0])
        g2 = glucose(1.1).move_to([X[0], Y2, 0])
        h1 = VGroup(half(1.1).move_to([X[1], Y1 + .33, 0]), half(1.1).move_to([X[1], Y1 - .33, 0]))
        h2 = VGroup(half(1.1).move_to([X[1], Y2 + .33, 0]), half(1.1).move_to([X[1], Y2 - .33, 0]))
        a1 = Arrow([-4.55, Y1, 0], [-4.0, Y1, 0], color=TEXT, buff=0, stroke_width=5)
        a2 = Arrow([-4.55, Y2, 0], [-4.0, Y2, 0], color=TEXT, buff=0, stroke_width=5)
        mito = mito_mob([-.4, Y1, 0], 3.2, 1.9)
        ar_m = Arrow([-2.4, Y1, 0], [-2.0, Y1, 0], color=TEXT, buff=0, stroke_width=5)
        ar_m2 = Arrow([1.3, Y1, 0], [1.8, Y1, 0], color=TEXT, buff=0, stroke_width=5)
        co2 = VGroup(*[puff(.23) for _ in range(3)]).arrange(RIGHT, buff=.08).move_to([2.9, Y1 + .35, 0])
        wt = VGroup(*[drop(.16) for _ in range(3)]).arrange(RIGHT, buff=.1).move_to([2.9, Y1 - .35, 0])
        ctop = VGroup(T("about 30", 38, GOLD, weight=BOLD), T("ATP", 38, GOLD, weight=BOLD)).arrange(DOWN, buff=.08).move_to([5.55, Y1, 0])
        ar_f = Arrow([-2.4, Y2, 0], [-.3, Y2, 0], color=TEXT, buff=0, stroke_width=5)
        left = VGroup(orange(1.1).move_to([.9, Y2 + .33, 0]), orange(1.1).move_to([.9, Y2 - .33, 0]))
        ll = T("lactate or ethanol", 28, LACT).move_to([.9, Y2 - 1.2, 0])
        barf = Rectangle(width=.8, height=2.4, stroke_color=GREY, stroke_width=3).move_to([3.3, Y2, 0])
        ev = ValueTracker(0)
        barfill = always_redraw(lambda: Rectangle(width=.8, height=max(.01, 2.4 * ev.get_value()), stroke_width=0,
                                                  fill_color=LACT, fill_opacity=.9).move_to([3.3, Y2 - 1.2 + 1.2 * ev.get_value(), 0]))
        el = T("energy left", 28, GOLD).move_to([3.3, Y2 + 1.6, 0])
        cbot = VGroup(T("2", 38, GOLD, weight=BOLD), T("ATP", 38, GOLD, weight=BOLD)).arrange(DOWN, buff=.08).move_to([5.55, Y2, 0])
        self.play(FadeIn(g1, scale=.8), run_time=.8)
        self.at("all the way")
        self.play(FadeIn(a1), FadeIn(h1), run_time=.8)
        self.play(FadeIn(mito), FadeIn(ar_m), run_time=.8)
        self.play(FadeIn(ar_m2), FadeIn(co2), FadeIn(wt), run_time=.7)
        self.at("rebuilds about")
        self.play(FadeIn(ctop, scale=.8), run_time=.6)
        self.play(Indicate(ctop, color=GOLD), run_time=.6)
        self.at("stop at")
        self.play(FadeIn(g2, scale=.8), FadeIn(a2), FadeIn(h2), run_time=.7)
        self.play(FadeIn(ar_f), FadeIn(left), run_time=.7)
        self.at("it rebuilds")
        self.play(FadeIn(cbot, scale=.8), run_time=.6)
        self.play(Indicate(cbot, color=GOLD), run_time=.8)
        self.at("most of the")
        self.play(FadeIn(barf), FadeIn(barfill), FadeIn(ll), FadeIn(el), run_time=.5)
        self.play(ev.animate.set_value(.93), run_time=1.6)
        self.play(Indicate(barfill, color=LACT, scale_factor=1.05), Indicate(left, color=LACT, scale_factor=1.1), run_time=1.0)
        self.at("same glucose")
        brk = SurroundingRectangle(VGroup(g1, g2, h1, h2), color=YELLOW, buff=.2, corner_radius=.2)
        self.play(Create(brk), run_time=1.0)
        self.at("very different")
        self.play(Indicate(ctop, color=GOLD, scale_factor=1.15), Indicate(cbot, color=GOLD, scale_factor=1.15), run_time=1.2)
        self.finish()


class S14End(EndCard):
    LINE = "How far each glucose is taken apart sets how much ATP returns."
