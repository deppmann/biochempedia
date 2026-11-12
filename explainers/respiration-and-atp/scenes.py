"""Spending ATP, Rebuilding ATP (high school Biology explainer, film 1 of 2)

COLOR MAP (one color per concept, whole film and the second film)
  SAND   = glucose (block of six segments; halves have three)
  GOLD   = ATP (round token, three beads), ADP (same token, two beads), loose phosphate (one bead)
  AQUA   = water drops
  BLUE   = oxygen dots
  GREY   = carbon dioxide puffs, outlines
  OLIVE  = mitochondrion
  RED    = heat shimmer, "no" marks
  SALMON = muscle
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
PURPLE = "#B58CD9"

FIB_Y = 1.9
SLOT_ATP = [(-3.8, -0.7), (-2.6, -0.7), (-3.8, -1.7), (-2.6, -1.7)]
SLOT_ADP = [(2.0, -0.7), (3.2, -0.7), (4.4, -0.7), (2.0, -1.7), (3.2, -1.7), (4.4, -1.7)]
CELL_C = np.array([0.0, -0.2, 0.0])
MITO_C = np.array([2.6, 0.2, 0.0])
HALF_A = np.array([-3.6, 0.45, 0.0])
HALF_B = np.array([-3.6, -0.45, 0.0])
TOK_L = [(-3.6, -2.0), (-2.6, -2.0)]


# ---------------------------------------------------------------- helpers
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


def bead(r=.14):
    return Dot(radius=r, color=BEAD)


def glucose(s=1.0):
    def row():
        return VGroup(*[Square(side_length=.34 * s, stroke_color=SAND_EDGE, stroke_width=2,
                               fill_color=SAND, fill_opacity=.95) for _ in range(3)]).arrange(RIGHT, buff=0)
    top, bot = row(), row()
    return VGroup(top, bot).arrange(DOWN, buff=0)


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


def sandwich():
    bread = lambda: RoundedRectangle(corner_radius=.25, width=2.4, height=.5, stroke_color="#B07F3E",
                                     stroke_width=3, fill_color="#D9A760", fill_opacity=1)
    top, bot = bread(), bread()
    lettuce = RoundedRectangle(corner_radius=.1, width=2.6, height=.18, stroke_width=0, fill_color="#7DBE6A", fill_opacity=1)
    ham = RoundedRectangle(corner_radius=.1, width=2.3, height=.22, stroke_width=0, fill_color="#E9A0A0", fill_opacity=1)
    return VGroup(bot, ham, lettuce, top).arrange(UP, buff=-.02)


def heat(n=4, w=.9, color=RED):
    g = VGroup()
    for i in range(n):
        ln = ParametricFunction(lambda t: np.array([i * .35 + .13 * np.sin(4 * t), t, 0]), t_range=[0, 1.1, .05],
                                stroke_color=color, stroke_width=4).set_opacity(.8)
        ln.ph = i * 1.3
        g.add(ln)
    g.t = 0.0

    def u(m, dt):
        m.t += dt
        for i, ln in enumerate(m):
            ln.set_opacity(.35 + .45 * (.5 + .5 * np.sin(2.4 * m.t + ln.ph)))
            ln.shift(UP * .15 * np.sin(2.4 * m.t + ln.ph) * dt * 3)
    g.add_updater(u)
    return g.center()


def mito_mob(pos, w=4.4, h=2.8):
    body = Ellipse(width=w, height=h, stroke_color=OLIVE, stroke_width=5, fill_color=OLIVE, fill_opacity=.3)
    fold = ParametricFunction(lambda t: np.array([t, .45 * np.sin(2.6 * t) * np.cos(.8 * t) , 0]),
                              t_range=[-w * .36, w * .36, .05], stroke_color="#C6D86A", stroke_width=4)
    return VGroup(body, fold).move_to(pos)


def cell_mob():
    return Ellipse(width=10.5, height=6.2, stroke_color=GREY, stroke_width=5,
                   fill_color=TEAL, fill_opacity=.16).move_to(CELL_C)


def world(c, n_atp, n_adp, atp_slots=None, adp_slots=None):
    """The carried picture for the four scenes about the muscle: fibre on top, ATP tray left, ADP tray right."""
    fib = fibre(c, 0, FIB_Y + .1, 11.5, 1.4)
    tray1 = RoundedRectangle(corner_radius=.2, width=3.2, height=2.6, stroke_color=GOLD, stroke_width=3,
                             fill_color=GOLD, fill_opacity=.16).move_to([-3.2, -1.2, 0])
    tray2 = RoundedRectangle(corner_radius=.2, width=4.0, height=2.6, stroke_color=GOLD, stroke_width=3,
                             fill_color=GOLD, fill_opacity=.16).move_to([3.2, -1.2, 0])
    lab1 = VGroup(T("a small supply of ATP", 28, TEXT), T("(schematic)", 28, TEXT)).arrange(DOWN, buff=.05).move_to([-3.2, 0.55, 0])
    lab2 = T("ADP", 28, TEXT).move_to([3.2, 0.55, 0])
    atps = [tok(3, .42).move_to([*SLOT_ATP[i], 0]) for i in (atp_slots if atp_slots is not None else range(n_atp))]
    adps = [tok(2, .42).move_to([*SLOT_ADP[i], 0]) for i in (adp_slots if adp_slots is not None else range(n_adp))]
    return fib, tray1, tray2, lab1, lab2, atps, adps


def stage(scene):
    p = RoundedRectangle(corner_radius=.35, width=12.6, height=7.2, stroke_width=0, fill_color=GREY, fill_opacity=.16).move_to([0, .1, 0]).set_z_index(-5)
    scene.add(p)
    return p


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "Respiration and ATP"
    TITLE = "Spending ATP, Rebuilding ATP"


class S01Question(SpokenScene):
    def construct(self):
        motes(self)
        c = ValueTracker(0)
        sw = sandwich().scale(1.4).move_to([-3.6, 0.8, 0])
        leg = leg_mob([4.2, 2.6], .12, .25, 2.0, 2.0)
        self.at("you just ate")
        self.play(FadeIn(sw, shift=UP * .3), run_time=1.0)
        self.play(sw.animate.shift(UP * .15), run_time=.6)
        self.at("leg muscles")
        self.play(FadeIn(leg), run_time=.7)
        blocks = VGroup(*[glucose(.55).move_to(sw.get_center() + [(i - 2) * .5, 0, 0]) for i in range(5)])
        self.play(ReplacementTransform(sw, blocks), run_time=.9)
        self.play(*[b.animate.move_to([4.6 + (i % 2) * .5 - .25, 1.0 + (i // 2) * .5 - .3, 0]) for i, b in enumerate(blocks)],
                  run_time=1.3)
        self.at("so why can't")
        fib = fibre(c, 0, .2, 11.0, 2.6)
        grid = VGroup(*[glucose(.55).move_to([-3.0 + 1.2 * i, .5 - .7 * j, 0]) for i in range(6) for j in range(2)])
        self.play(FadeOut(leg), FadeOut(blocks), FadeIn(fib), run_time=.6)
        self.play(LaggedStart(*[FadeIn(g, scale=.6) for g in grid], lag_ratio=.05), run_time=1.0)
        self.at("burn that sugar")
        q = T("?", 110, YELLOW, weight=BOLD).move_to([0, .1, 0])
        lab = T("burn the sugar directly?", 32, YELLOW).move_to([0, 2.5, 0])
        self.play(c.animate.set_value(.7), FadeIn(q, scale=.5), FadeIn(lab), run_time=.9)
        self.play(c.animate.set_value(.0), Wiggle(q), run_time=.9)
        self.at("small molecule")
        t = tok(3, .6).move_to([-6.2, -2.6, 0])
        self.play(FadeOut(q), FadeOut(lab), run_time=.2)
        self.play(t.animate.move_to([-0.6, -2.6, 0]).rotate(-TAU), run_time=.8, rate_func=smooth)
        self.at("called")
        a = T("ATP", 44, GOLD, weight=BOLD).next_to(t, RIGHT, buff=.4)
        self.play(FadeIn(a, shift=LEFT * .2), c.animate.set_value(.5), run_time=.8)
        self.play(c.animate.set_value(0), run_time=.8)
        self.finish()


class S02Spend(SpokenScene):
    def construct(self):
        motes(self)
        # 0: a cell spending tokens
        cell = Circle(radius=2.0, stroke_color=GREY, stroke_width=5, fill_color=TEAL, fill_opacity=.08).move_to([0, .3, 0])
        self.play(FadeIn(cell, scale=.7), run_time=.8)
        for i in range(2):
            t = tok(3, .4).move_to(cell.get_center())
            self.play(t.animate.move_to([3.6, .3 + i * .6 - .3, 0]), FadeOut(t, rate_func=lambda x: smooth(max(0, x * 1.4 - .4))), run_time=1.1)
        px = [-4.35, 0.0, 4.35]
        panels = [RoundedRectangle(corner_radius=.25, width=3.9, height=4.2, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=.2).move_to([x, .3, 0]) for x in px]
        c1, c2 = ValueTracker(0), ValueTracker(0)
        self.at("a muscle cell")
        f1 = fibre(c1, -4.35, .5, 3.3, 1.3)
        self.play(FadeOut(cell), FadeIn(panels[0], shift=RIGHT * .5), FadeIn(f1), run_time=.6)
        feed = tok(3, .3).move_to([-4.35, 3.3, 0])
        self.play(feed.animate.move_to([-4.35, 1.4, 0]), c1.animate.set_value(1), run_time=.8)
        self.play(FadeOut(feed), run_time=.15)
        self.play(c1.animate.set_value(0), run_time=.6)
        loop(self, ValueTracker(0), 1.6)
        loop(self, c1, 1.7)
        self.at("a nerve cell")
        ncell = Circle(radius=1.05, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=.1).move_to([0, .5, 0])
        self.play(FadeIn(panels[1], shift=DOWN * .5), FadeIn(ncell), run_time=.6)
        feed = tok(3, .3).move_to([0, 3.3, 0])
        self.play(feed.animate.move_to([0, 1.8, 0]), run_time=.6)
        self.play(FadeOut(feed), run_time=.15)
        for k in range(2):
            pl = T("+", 36, YELLOW, weight=BOLD).move_to([-.3 + k * .3, .5 - .3 * k, 0])
            self.play(FadeIn(pl, run_time=.2))
            self.play(pl.animate.move_to([1.0 + k * .08, .5 + (k - 1) * .6, 0]).scale(1.1), run_time=1.0)
        self.at("almost every cell")
        self.play(FadeIn(panels[2], shift=LEFT * .5), run_time=.6)
        feed = tok(3, .3).move_to([4.35, 3.3, 0])
        self.play(feed.animate.move_to([4.35, 1.5, 0]), run_time=.6)
        self.play(FadeOut(feed), run_time=.15)
        chain = VGroup()
        for k in range(5):
            d = Dot(radius=.17, color=PURPLE).move_to([3.0 + k * .5 + .1, .8 + .12 * (-1) ** k, 0])
            chain.add(d)
            self.play(FadeIn(d, scale=.3), run_time=.3)
        pl3 = T("protein", 28, PURPLE).move_to([4.35, -.2, 0])
        self.play(FadeIn(pl3), run_time=.3)
        self.at("none of these")
        for i, x in enumerate(px):
            g = glucose(.6).move_to([x, -2.9, 0])
            self.play(FadeIn(g), run_time=.15)
            self.play(g.animate.move_to([x, -1.9, 0]), run_time=.4)
            xm = T("X", 40, RED, weight=BOLD).move_to([x + .75, -1.9, 0])
            self.play(g.animate.move_to([x, -2.9, 0]), FadeIn(xm), run_time=.4)
            self.play(FadeOut(g), FadeOut(xm), run_time=.15)
        self.at("they run on")
        lab = T("jobs run on ATP", 34, GOLD, weight=BOLD).move_to([0, -2.8, 0])
        self.play(FadeIn(lab, shift=UP * .2), run_time=.5)
        toks = [tok(3, .3).move_to([x, 3.3, 0]) for x in px]
        self.play(*[tk.animate.move_to([x, 1.8, 0]) for tk, x in zip(toks, px)], run_time=1.0)
        self.play(*[FadeOut(tk) for tk in toks], run_time=.3)
        self.at("a molecule that carries")
        t = tok(3, .6).move_to([-4.4, -2.8, 0])
        tag = T("a molecule that carries energy", 28, TEXT)
        tag.move_to([2.2, -2.8, 0])
        self.play(FadeOut(lab), run_time=.3)
        self.play(FadeIn(t, scale=.5), FadeIn(tag), run_time=.7)
        self.play(Indicate(t, scale_factor=1.2), run_time=.9)
        self.finish()


class S03AtpToAdp(SpokenScene):
    def construct(self):
        motes(self)
        c = ValueTracker(0)
        loop(self, ValueTracker(0), 1.7)
        P = np.array([-3.7, .9, 0])
        t = tok(3, 1.1).move_to(P)
        fib = fibre(c, 3.6, .9, 5.4, 1.8)
        atp = T("ATP", 36, GOLD, weight=BOLD).move_to([-3.7, 2.5, 0])
        self.play(FadeIn(t, scale=.6), FadeIn(fib), FadeIn(atp), run_time=1.0)
        self.at("has three phosphate")
        br = Brace(t[1], DOWN, color=BEAD)
        pg = T("phosphate groups", 28, BEAD).move_to([-3.7, -.6, 0])
        self.play(GrowFromCenter(br), FadeIn(pg), run_time=.9)
        self.play(Indicate(t[1], color=BEAD), run_time=.9)
        self.at("when it reacts")
        w = VGroup(drop(.18), T("water", 28, AQUA)).arrange(RIGHT, buff=.15).move_to([-.3, 3.0, 0])
        self.play(FadeOut(br), FadeOut(pg), FadeIn(w, shift=DOWN * .3), run_time=.7)
        self.play(w.animate.move_to([-1.2, .3, 0]), run_time=1.1)
        self.at("the end phosphate")
        new = tok(2, 1.1).move_to(P)
        loose = t[1][2].copy()
        self.play(Transform(t, new), loose.animate.move_to([-.9, 2.3, 0]).scale(1.6), FadeOut(w), run_time=1.2)
        self.play(loose.animate.move_to([-.9, 2.5, 0]), run_time=.5)
        self.at("what is left")
        adp = T("ADP", 36, GOLD, weight=BOLD).move_to([-3.7, 2.5, 0])
        self.play(Transform(atp, adp), run_time=.8)
        self.at("with only two")
        self.play(Indicate(t[1], color=BEAD), run_time=.9)
        self.at("that reaction releases")
        eq = T("ATP + water → ADP + phosphate + energy for work", 28, TEXT).move_to([0, -2.6, 0])
        self.play(Write(eq), run_time=2.4)
        self.at("the muscle uses")
        spark = VMobject(stroke_color=GOLD, stroke_width=6).set_points_as_corners(
            [[-2.4, .9, 0], [-1.6, 1.3, 0], [-1.1, .5, 0], [-.4, 1.1, 0], [.4, .9, 0]])
        self.play(Create(spark), run_time=.4)
        self.play(c.animate.set_value(1), FadeOut(spark), run_time=1.0)
        self.play(c.animate.set_value(0), run_time=.8)
        self.finish()


class S04Pool(SpokenScene):
    def construct(self):
        motes(self)
        c = ValueTracker(0)
        fib, tray1, tray2, lab1, lab2, atps, adps = world(c, 4, 0)
        self.play(FadeIn(fib), run_time=.6)
        self.play(c.animate.set_value(1), run_time=.8)
        self.play(c.animate.set_value(0), run_time=.8)
        self.at("a cell keeps")
        self.play(FadeIn(tray1), LaggedStart(*[FadeIn(a, scale=.5) for a in atps], lag_ratio=.15), run_time=1.0)
        self.at("small supply")
        self.play(FadeIn(lab1, shift=UP * .1), run_time=.6)
        self.at("watch that supply")
        self.play(FadeIn(tray2), FadeIn(lab2), run_time=.5)
        for i in range(3):
            tk = atps[i]
            self.play(c.animate.set_value(1), tk.animate.move_to([0, -.7, 0]), run_time=.5)
            new = tok(2, .42).move_to(tk.get_center())
            self.play(Transform(tk, new), FadeOut(tk[1][2].copy().shift(UP * .5)), run_time=.2)
            self.play(c.animate.set_value(0), tk.animate.move_to([*SLOT_ADP[i], 0]), run_time=.5)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        motes(self)
        c = ValueTracker(.55)
        fib, tray1, tray2, lab1, lab2, atps, adps = world(c, 0, 0, atp_slots=[3], adp_slots=[0, 1, 2])
        self.add(fib, tray1, tray2, lab1, lab2, *atps, *adps)
        icon = VGroup(Circle(radius=.4, stroke_color=TEXT, stroke_width=4),
                      Rectangle(width=.1, height=.35, fill_color=TEXT, fill_opacity=1, stroke_width=0).shift(LEFT * .09),
                      Rectangle(width=.1, height=.35, fill_color=TEXT, fill_opacity=1, stroke_width=0).shift(RIGHT * .09)).move_to([6.0, 3.2, 0])
        self.play(FadeIn(icon), run_time=.4)
        for _ in range(2):
            self.play(icon.animate.scale(1.25), run_time=.45, rate_func=there_and_back)
            self.play(icon.animate.scale(1.25), run_time=.45, rate_func=there_and_back)
        self.at("what would happen")
        veil = Rectangle(width=14.3, height=8, stroke_width=0, fill_color=BG, fill_opacity=.72)
        card = VGroup(RoundedRectangle(corner_radius=.25, width=10, height=2.6, stroke_color=YELLOW, stroke_width=4,
                                       fill_color=BG, fill_opacity=1),
                      VGroup(T("If nothing rebuilds ATP...", 36, TEXT), T("the supply?   the pulling?", 36, YELLOW)).arrange(DOWN, buff=.3)
                      ).move_to([0, .2, 0])
        card[1].move_to(card[0])
        self.play(FadeIn(veil), FadeIn(card, scale=.9), run_time=.8)
        for _ in range(2):
            self.play(icon.animate.scale(1.25), run_time=.45, rate_func=there_and_back)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        motes(self)
        c = ValueTracker(.55)
        fib, tray1, tray2, lab1, lab2, atps, adps = world(c, 0, 0, atp_slots=[3], adp_slots=[0, 1, 2])
        self.add(fib, tray1, tray2, lab1, lab2, *atps, *adps)
        veil = Rectangle(width=14.3, height=8, stroke_width=0, fill_color=BG, fill_opacity=.72)
        card = VGroup(RoundedRectangle(corner_radius=.25, width=10, height=2.6, stroke_color=YELLOW, stroke_width=4,
                                       fill_color=BG, fill_opacity=1),
                      VGroup(T("If nothing rebuilds ATP...", 36, TEXT), T("the supply?   the pulling?", 36, YELLOW)).arrange(DOWN, buff=.3)
                      ).move_to([0, .2, 0])
        card[1].move_to(card[0])
        self.add(veil, card)
        tr = ValueTracker(1)
        bar = always_redraw(lambda: Rectangle(width=max(.02, 12 * tr.get_value()), height=.18, stroke_width=0,
                                              fill_color=YELLOW, fill_opacity=.9).move_to([-6 + 6 * tr.get_value(), -3.4, 0]))
        icon = VGroup(Circle(radius=.4, stroke_color=TEXT, stroke_width=4),
                      Rectangle(width=.1, height=.35, fill_color=TEXT, fill_opacity=1, stroke_width=0).shift(LEFT * .09),
                      Rectangle(width=.1, height=.35, fill_color=TEXT, fill_opacity=1, stroke_width=0).shift(RIGHT * .09)).move_to([6.0, 3.2, 0])
        self.add(bar, icon)
        self.play(tr.animate.set_value(0), run_time=self.narration_s - .1, rate_func=linear)
        self.finish()


class S07Reveal(SpokenScene):
    def construct(self):
        motes(self)
        c = ValueTracker(.55)
        fib, tray1, tray2, lab1, lab2, atps, adps = world(c, 0, 0, atp_slots=[3], adp_slots=[0, 1, 2])
        self.add(fib, tray1, tray2, lab1, lab2, *atps, *adps)
        self.at("the supply would")
        last = atps[0]
        self.play(c.animate.set_value(.8), last.animate.move_to([0, -.7, 0]), run_time=.8)
        new = tok(2, .42).move_to(last.get_center())
        self.play(Transform(last, new), run_time=.25)
        self.play(last.animate.move_to([*SLOT_ADP[3], 0]), c.animate.set_value(.6), run_time=.7)
        self.at("pulling would stop")
        nolab = T("no ATP: pulling stops (schematic)", 28, RED).move_to([0, 3.3, 0])
        self.play(FadeIn(nolab), run_time=.5)
        self.at("working cell rebuilds")
        blur = Rectangle(width=14.3, height=8, stroke_width=0, fill_color=TEXT, fill_opacity=.0)
        self.play(blur.animate.set_fill(opacity=.3), run_time=.15)
        self.play(blur.animate.set_fill(opacity=0), FadeOut(nolab), c.animate.set_value(0), run_time=.25)
        adps_all = adps + [last]
        a0, a1 = np.array([1.5, -.6, 0]), np.array([-1.5, -.6, 0])
        path = ArcBetweenPoints(a0, a1, angle=PI / 3)
        arrow = path.copy().add_tip(tip_length=.3).set_color(TEXT).set_stroke(width=5)
        self.play(Create(arrow), run_time=.5)
        atp_tokens = []
        for j in range(4):
            tk = adps_all[j]
            self.play(tk.animate.move_to(a0), run_time=.15)
            self.play(MoveAlongPath(tk, path), run_time=.4, rate_func=linear)
            nt = tok(3, .42).move_to(tk.get_center())
            self.play(Transform(tk, nt), Flash(tk, color=BEAD, flash_radius=.5, line_length=.15), run_time=.3)
            self.play(tk.animate.move_to([*SLOT_ATP[j], 0]), run_time=.2)
        self.at("putting the phosphate")
        self.play(Indicate(arrow, color=BEAD, scale_factor=1.15), run_time=.8)
        self.at("that energy comes")
        g = glucose(.9).move_to([0, -1.6, 0])
        gl = T("energy from taking glucose apart", 28, TEXT).move_to([0, -3.2, 0])
        self.play(FadeIn(g, shift=UP * .3), FadeIn(gl), run_time=.8)
        self.at("taking glucose apart")
        v = ValueTracker(0)
        cnt = counter(v)
        self.play(FadeIn(cnt), g.animate.shift(UP * .15), run_time=.6)
        self.play(g.animate.shift(DOWN * .15), run_time=.6)
        self.finish()


class S08Cytoplasm(SpokenScene):
    def construct(self):
        motes(self)
        v = ValueTracker(0)
        cnt = counter(v)
        self.add(cnt)
        cell = cell_mob()
        self.play(FadeIn(cell, scale=1.5), run_time=1.4)
        g = glucose(1.0).move_to([-6.2, .5, 0])
        self.play(g.animate.move_to([-1.5, .5, 0]), run_time=3.0, rate_func=smooth)
        self.at("taking it apart")
        glow = cell.copy().set_fill(TEAL, .22).set_stroke(TEAL, 6)
        self.play(Transform(cell, glow), run_time=.9)
        self.at("cytoplasm")
        lab = T("cytoplasm", 34, TEAL, weight=BOLD).move_to([0, 2.3, 0])
        self.play(FadeIn(lab, shift=DOWN * .2), run_time=.6)
        self.play(g.animate.move_to([-3.6, 0, 0]), run_time=2.0)
        adps = [tok(2, .38).move_to([*p, 0]) for p in TOK_L]
        self.play(FadeIn(adps[0], scale=.6), FadeIn(adps[1], scale=.6), run_time=.6)
        self.at("split glucose")
        top, bot = g[0], g[1]
        self.play(top.animate.move_to(HALF_A), bot.animate.move_to(HALF_B), run_time=1.2)
        self.at("rebuild a little")
        newt = [tok(3, .38).move_to([*p, 0]) for p in TOK_L]
        self.play(*[Transform(a, n) for a, n in zip(adps, newt)], v.animate.set_value(2), run_time=1.4)
        self.play(Flash(adps[0], color=BEAD, flash_radius=.55, line_length=.15), Flash(adps[1], color=BEAD, flash_radius=.55, line_length=.15), run_time=.6)
        self.finish()


class S09Mito(SpokenScene):
    def construct(self):
        motes(self)
        v = ValueTracker(2)
        cnt = counter(v)
        self.add(cnt)
        cell = cell_mob().set_fill(TEAL, .2)
        halves = VGroup(*[r.copy() for r in glucose(1.0)])
        halves[0].move_to(HALF_A)
        halves[1].move_to(HALF_B)
        atps = [tok(3, .38).move_to([*p, 0]) for p in TOK_L]
        self.add(cell, halves, *atps)
        mito = mito_mob(MITO_C)
        # oxygen stream
        ox = VGroup(*[o2dot() for _ in range(6)])
        for i, d in enumerate(ox):
            d.move_to([-6.0 + i * 1.1, -1.5 + .12 * (-1) ** i, 0])

        def flow(m, dt):
            for d in m:
                d.shift(RIGHT * 1.0 * dt + UP * .18 * dt)
                if d.get_x() > 1.0:
                    d.move_to([-6.0, -1.7, 0])
        ox.add_updater(flow)
        self.at("with oxygen")
        self.add(ox)
        self.play(FadeIn(mito, scale=.8), run_time=1.2)
        self.at("two halves")
        self.play(halves[0].animate.move_to(MITO_C + [-.5, .45, 0]), halves[1].animate.move_to(MITO_C + [-.5, -.1, 0]), run_time=1.2)
        self.at("mitochondrion")
        ml = T("mitochondrion", 32, OLIVE, weight=BOLD).move_to([2.55, -1.6, 0])
        self.play(FadeIn(ml), run_time=.5)
        self.at("this organelle")
        pieces = VGroup(*halves[0], *halves[1])
        spots = [(-0.3, .6), (.7, .3), (-.4, -.3), (1.6, .5), (1.0, -.5), (2.3, -.2)]
        self.play(*[p.animate.scale(.7).move_to(MITO_C + [x, y - .2, 0]) for p, (x, y) in zip(pieces, spots)], run_time=1.6)
        self.at("carbon dioxide")
        outs, kinds = [], []
        for i, p in enumerate(pieces):
            if i < 3:
                o = puff(.22).move_to(p.get_center())
            else:
                o = drop(.16).move_to(p.get_center())
            outs.append(o)
        co2 = T("carbon dioxide", 28, GREY).move_to([-1.6, 2.3, 0])
        self.play(*[ReplacementTransform(p, o) for p, o in zip(pieces, outs)], run_time=.6)
        self.play(*[o.animate.move_to([-2.1 + .55 * i, 1.6 + .1 * i, 0]) for i, o in enumerate(outs[:3])], FadeIn(co2), run_time=1.2)
        self.at("water")
        wl = T("water", 28, AQUA).move_to([2.6, -2.5, 0])
        self.play(*[o.animate.move_to([1.8 + .7 * (i - 3), -1.9, 0]) for i, o in enumerate(outs[3:], 3)] if False else
                  [outs[3 + k].animate.move_to([1.9 + .7 * k, -1.85, 0]) for k in range(3)], FadeIn(wl), run_time=1.2)
        self.play(FadeOut(VGroup(*outs)), FadeOut(co2), FadeOut(wl), FadeOut(ml), run_time=.6)
        self.at("most of the")
        adps = [tok(2, .38).move_to([-.5, y, 0]) for y in (1.1, .2, -.7)]
        self.play(LaggedStart(*[FadeIn(a, scale=.6) for a in adps], lag_ratio=.2), run_time=.7)
        for k, a in enumerate(adps):
            n = tok(3, .38).move_to(a.get_center())
            self.play(Transform(a, n), v.animate.set_value(2 + 4 * (k + 1)), Flash(a, color=BEAD, flash_radius=.5, line_length=.15), run_time=.55)
        self.finish()


class S10Count(SpokenScene):
    def construct(self):
        motes(self)
        v = ValueTracker(14)
        abt = ValueTracker(0)
        cnt = counter(v, abt)
        cell = cell_mob().set_fill(TEAL, .2)
        mito = mito_mob(MITO_C)
        atps = [tok(3, .38).move_to([*p, 0]) for p in TOK_L] + [tok(3, .38).move_to([-.5, y, 0]) for y in (1.1, .2, -.7)]
        self.add(cell, mito, *atps, cnt)
        self.at("count what one")
        outs = VGroup()
        for k in range(5):
            tk = tok(3, .3).move_to(MITO_C + [0, 0, 0])
            outs.add(tk)
        def fly(k):
            def f(m, a):
                m.move_to(MITO_C + [(k - 2) * .9 * a, 2.0 * a, 0])
                m.set_opacity(np.sin(np.pi * a))
            return UpdateFromAlphaFunc(outs[k], f, run_time=1.6)
        self.add(outs)
        self.play(v.animate.set_value(30), LaggedStart(*[fly(k) for k in range(5)], lag_ratio=.45), run_time=4.6, rate_func=linear)
        self.at("about thirty")
        abt.set_value(1)
        self.wait(.8)
        self.at("some energy")
        h1 = heat(4).move_to([2.6, 1.85, 0])
        h2 = heat(3).move_to([-3.5, 1.9, 0])
        self.play(FadeIn(h1), FadeIn(h2), run_time=.8)
        self.at("heat")
        hl = T("heat", 34, RED, weight=BOLD).move_to([5.95, 1.6, 0])
        self.play(FadeIn(hl), run_time=.5)
        self.at("that is one reason")
        inset = VGroup(RoundedRectangle(corner_radius=.2, width=2.8, height=2.4, stroke_color=GREY, stroke_width=3, fill_color=BG, fill_opacity=1))
        face = VGroup(Circle(radius=.6, stroke_color=SKIN, stroke_width=4, fill_color=SKIN, fill_opacity=.5),
                      Dot([-.2, .12, 0], radius=.06, color=TEXT), Dot([.2, .12, 0], radius=.06, color=TEXT),
                      Arc(radius=.25, start_angle=PI + .5, angle=PI - 1.0, stroke_color=TEXT, stroke_width=3).shift(UP * .05),
                      Circle(radius=.17, stroke_width=0, fill_color="#F08A9A", fill_opacity=.3).shift([-.38, -.08, 0]),
                      Circle(radius=.17, stroke_width=0, fill_color="#F08A9A", fill_opacity=.3).shift([.38, -.08, 0]))
        group = VGroup(inset, face.move_to(inset).shift(UP * .3)).move_to([5.1, -2.2, 0])
        wl2 = T("warm", 28, RED).move_to([5.1, -3.1, 0])
        self.play(FadeIn(group), FadeIn(wl2), run_time=.7)
        self.at("warm up")
        for p in face[4:]:
            self.play(p.animate.set_fill(opacity=.9), run_time=.9)
        self.finish()


class S11Cycle(SpokenScene):
    def construct(self):
        motes(self)
        stage(self)
        c = ValueTracker(0)
        L, R = np.array([-3.6, .2, 0]), np.array([3.6, .2, 0])
        tl = tok(3, .65).move_to(L)
        tr_ = tok(2, .65).move_to(R)
        la = T("ATP", 32, GOLD, weight=BOLD).move_to([-3.6, -.9, 0])
        lb = T("ADP", 32, GOLD, weight=BOLD).move_to([3.6, -.9, 0])
        fib = fibre(c, 0, .2, 4.4, 1.5)
        self.play(FadeIn(tl, scale=.6), FadeIn(tr_, scale=.6), FadeIn(la), FadeIn(lb), FadeIn(fib), run_time=1.2)
        top = ArcBetweenPoints(L + RIGHT * .8, R + LEFT * .8, angle=-PI * .7)
        bot = ArcBetweenPoints(R + LEFT * .8, L + RIGHT * .8, angle=-PI * .7)
        topv = top.copy().add_tip(tip_length=.3).set_color(TEXT).set_stroke(width=6)
        botv = bot.copy().add_tip(tip_length=.3).set_color(TEXT).set_stroke(width=6)
        self.at("work turns")
        t1 = T("cell work (muscle pulls)", 30, TEXT).move_to([0, 3.0, 0])
        self.play(Create(topv), FadeIn(t1), run_time=1.0)
        m = tok(3, .32)
        self.play(FadeIn(m.move_to(top.point_from_proportion(0))), run_time=.2)
        self.play(MoveAlongPath(m, top), c.animate.set_value(1), run_time=1.6, rate_func=linear)
        self.play(Transform(m, tok(2, .32).move_to(m.get_center())), c.animate.set_value(0), run_time=.5)
        self.at("respiration turns")
        t2 = T("respiration (glucose taken apart)", 30, TEXT).move_to([0, -2.9, 0])
        self.play(Create(botv), FadeIn(t2), FadeOut(m), run_time=1.0)
        m2 = tok(2, .32).move_to(bot.point_from_proportion(0))
        self.play(FadeIn(m2), run_time=.2)
        self.play(MoveAlongPath(m2, bot), run_time=1.6, rate_func=linear)
        self.play(Transform(m2, tok(3, .32).move_to(m2.get_center())), run_time=.5)
        self.at("round and round")
        self.remove(m2)
        a = tok(3, .32).move_to(top.point_from_proportion(0))
        b = tok(2, .32).move_to(bot.point_from_proportion(0))
        self.add(a, b)
        for _ in range(2):
            self.play(MoveAlongPath(a, top), MoveAlongPath(b, bot), c.animate.set_value(1), run_time=1.3, rate_func=linear)
            a.move_to(top.point_from_proportion(0))
            b.move_to(bot.point_from_proportion(0))
            self.play(c.animate.set_value(0), run_time=.3)
        self.finish()


class S12Equation(SpokenScene):
    def construct(self):
        motes(self)
        stage(self)
        Y1, Y2 = 1.5, -.7
        gl = glucose(1.3).move_to([-5.0, Y1, 0])
        p1 = T("+", 40).move_to([-4.2, Y1, 0])
        o2 = VGroup(*[o2dot(.18) for _ in range(3)]).arrange(RIGHT, buff=.25).move_to([-3.4, Y1, 0])
        arr = Arrow([-2.7, Y1, 0], [-.3, Y1, 0], color=TEXT, stroke_width=14, buff=0, max_tip_length_to_length_ratio=.4)
        co2 = VGroup(*[puff(.26) for _ in range(3)]).arrange(RIGHT, buff=.1).move_to([.9, Y1, 0])
        p2 = T("+", 40).move_to([2.0, Y1, 0])
        wt = VGroup(*[drop(.2) for _ in range(3)]).arrange(RIGHT, buff=.15).move_to([3.0, Y1, 0])
        row = [(gl, gl.get_center()), (p1, p1.get_center()), (o2, o2.get_center()), (arr, arr.get_center()),
               (co2, co2.get_center()), (p2, p2.get_center()), (wt, wt.get_center())]
        rng = np.random.default_rng(3)
        for mo, _ in row:
            mo.shift([rng.uniform(-1, 1), rng.uniform(-2.2, -1.2), 0])
            mo.set_opacity(0)
        self.play(*[mo.animate.move_to(pos).set_opacity(1) for mo, pos in row], run_time=1.4)
        self.at("cellular respiration")
        title = T("cellular respiration", 40, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.add(title)
        self.play(Write(title), run_time=1.2)
        q1 = T("glucose + oxygen", 28, TEXT)
        q2 = T("→ carbon dioxide + water", 28, TEXT)
        q3 = T("+ energy", 28, TEXT)
        line = VGroup(q1, q2, q3).arrange(RIGHT, buff=.18).move_to([0, -2.5, 0])
        q4 = T("(much of it captured in ATP)", 28, GOLD).move_to([0, -3.15, 0])
        self.at("glucose and oxygen")
        self.play(FadeIn(q1, shift=UP * .1), Indicate(gl), Indicate(o2), run_time=1.2)
        self.at("carbon dioxide")
        self.play(FadeIn(q2, shift=UP * .1), Indicate(co2), Indicate(wt), run_time=1.2)
        self.at("with energy")
        el = T("released energy", 28, TEXT).move_to([-1.5, 2.3, 0])
        self.play(FadeIn(q3, shift=UP * .1), FadeIn(el), Indicate(arr, color=BEAD, scale_factor=1.1), run_time=1.0)
        self.at("much of it")
        down = CurvedArrow([-1.5, 1.0, 0], [-2.3, -.1, 0], color=TEXT, stroke_width=6, angle=-PI / 4)
        adp = tok(2, .45).move_to([-5.2, Y2, 0])
        p3 = T("+", 40).move_to([-4.4, Y2, 0])
        lb = bead(.14).move_to([-3.7, Y2, 0])
        arr2 = Arrow([-3.1, Y2, 0], [-1.6, Y2, 0], color=TEXT, stroke_width=9, buff=0)
        self.play(Create(down), FadeIn(adp), FadeIn(p3), FadeIn(lb), GrowArrow(arr2), run_time=1.0)
        self.at("captured in")
        atp = tok(3, .45).move_to([-.7, Y2, 0])
        self.play(FadeIn(atp, scale=.6), FadeIn(q4), run_time=.9)
        self.play(lb.animate.move_to(adp.get_center() + [.3, 0, 0]), run_time=.8)
        hr = Arrow([-.8, .75, 0], [3.8, .75, 0], color=RED, stroke_width=6, buff=0)
        hs = heat(4).move_to([5.0, .9, 0])
        hl = T("heat", 28, RED).move_to([5.2, 1.9, 0])
        self.play(GrowArrow(hr), FadeIn(hs), FadeIn(hl), run_time=1.0)
        self.at("not energy itself")
        self.play(Indicate(atp, scale_factor=1.25), run_time=1.0)
        self.at("it is a molecule")
        tag = VGroup(T("a molecule that", 28, GOLD), T("carries energy", 28, GOLD)).arrange(DOWN, buff=.08).move_to([2.2, Y2, 0])
        self.play(FadeIn(tag, shift=LEFT * .2), run_time=.8)
        self.at("carries it")
        self.play(Indicate(tag, color=GOLD, scale_factor=1.1), run_time=.9)
        self.finish()


class S13Tease(SpokenScene):
    def construct(self):
        motes(self)
        loopt = ValueTracker(0)
        loopt.t = 0.0
        loopt.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))
        self.add(loopt)
        pl = RoundedRectangle(corner_radius=.25, width=6.0, height=5.0, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.2).move_to([-3.4, -.2, 0])
        pr = RoundedRectangle(corner_radius=.25, width=6.0, height=5.0, stroke_color=GREY, stroke_width=3,
                              fill_color=GREY, fill_opacity=.2).move_to([3.4, -.2, 0])

        def leg_build():
            tt = loopt.get_value()
            a = .55 + .55 * np.sin(5.0 * tt)
            b = .6 + .6 * np.sin(5.0 * tt + 1.4)
            return leg_mob([-5.2, 1.7], a, max(b, 0), 1.5, 1.5)
        leg = always_redraw(leg_build)
        self.at("sprinting leg")
        self.play(FadeIn(pl), FadeIn(leg), run_time=.8)
        lv = ValueTracker(.9)
        frame = Rectangle(width=.75, height=3.4, stroke_color=GOLD, stroke_width=4).move_to([-1.1, -.4, 0])
        fill = always_redraw(lambda: Rectangle(width=.75, height=max(.02, 3.4 * lv.get_value()), stroke_width=0,
                                               fill_color=GOLD, fill_opacity=.7).move_to([-1.1, -2.1 + 1.7 * lv.get_value(), 0]))
        ml = T("ATP", 28, GOLD).move_to([-1.1, -2.5, 0])
        self.play(FadeIn(frame), FadeIn(fill), FadeIn(ml), run_time=.6)
        self.play(lv.animate.set_value(.2), run_time=3.4, rate_func=linear)
        self.at("yeast sealed")
        dough = Ellipse(width=3.4, height=2.6, stroke_color="#B9935A", stroke_width=4, fill_color="#E8D3A8", fill_opacity=.5).move_to([3.4, -.5, 0])
        wrap = Ellipse(width=3.9, height=3.1, stroke_color=TEXT, stroke_width=3).move_to([3.4, -.5, 0]).set_opacity(.9)
        wrap = DashedVMobject(wrap, num_dashes=24)
        yeast = VGroup(*[Ellipse(width=.4, height=.3, stroke_color="#8A6A35", stroke_width=2, fill_color="#B9935A", fill_opacity=1).move_to(
            [3.4 + x, -.5 + y, 0]) for x, y in [(-.8, .3), (.2, .6), (.7, -.2), (-.3, -.5), (.9, .5)]])
        yeast.t = 0.0

        def wob(m, dt):
            m.t += dt
            for i, y in enumerate(m):
                y.shift([.12 * np.sin(2 * m.t + i) * dt * 2, .12 * np.cos(2.3 * m.t + i) * dt * 2, 0])
        yeast.add_updater(wob)
        self.play(FadeIn(pr), FadeIn(dough), FadeIn(yeast), run_time=.8)
        self.play(Create(wrap), run_time=.8)
        self.at("almost no oxygen")
        ox = VGroup(*[o2dot(.1).move_to([2.0 + .9 * i, 1.9 - .2 * (i % 2), 0]) for i in range(4)])
        self.play(FadeIn(ox), run_time=.4)
        self.play(*[d.animate.shift(DOWN * .55) for d in ox], run_time=.6)
        self.play(*[d.animate.shift(UP * .45 + RIGHT * (.3 if i % 2 else -.3)) for i, d in enumerate(ox)], run_time=.6)
        self.play(*[d.animate.shift(DOWN * .4) for d in ox], run_time=.5)
        self.play(FadeOut(ox), run_time=.3)
        self.at("what happens then")
        q = T("What happens then?", 42, YELLOW, weight=BOLD).move_to([0, -3.3, 0])
        self.play(FadeIn(q, shift=UP * .2), run_time=.6)
        self.at("switch the oxygen")
        self.play(FadeOut(q), run_time=.3)
        pipe = RoundedRectangle(corner_radius=.1, width=2.6, height=.4, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=.3).move_to([0, 3.1, 0])
        handle = VGroup(Line([-.2, 3.3, 0], [.2, 3.3, 0], stroke_color=BLUE, stroke_width=6), Line([0, 3.3, 0], [0, 3.7, 0], stroke_color=BLUE, stroke_width=6))
        qm = T("?", 56, YELLOW, weight=BOLD).move_to([2.0, 3.1, 0])
        self.play(FadeIn(pipe), FadeIn(handle), FadeIn(qm), run_time=.7)
        self.play(Rotate(handle, angle=-PI / 4, about_point=np.array([0, 3.3, 0])), run_time=.8)
        self.at("in the simulation")
        btn = chip("oxygen: off?", BLUE, 30).move_to([0, -3.2, 0])
        self.play(FadeIn(btn, scale=.8), run_time=.6)
        self.at("find out")
        for _ in range(3):
            self.play(btn.animate.set_opacity(.35), run_time=.4)
            self.play(btn.animate.set_opacity(1), run_time=.4)
        self.finish()


class S14End(EndCard):
    LINE = "Cells spend ATP, then rebuild it by taking glucose apart."
