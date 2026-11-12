"""What Was Dated? (human-evolution film, chapter 1)

COLOUR MAP: TEAL = Homo sapiens; GOLD = dated things (flints, date tags, pins' dates); ASH = volcanic ash;
RED = heat/fire; GREY = ground, outlines. Maps and cut-aways are schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ASH = "#CDBF9F"
LBL = "#C9D1DE"
SOIL, SED, BAND, DEEP = "#4D4234", "#5F5242", "#7A6648", "#41382D"

AFR = [(-4.6, 2.0), (-3.4, 3.0), (-1.2, 3.2), (0.6, 3.0), (1.4, 2.4), (1.8, 1.2), (2.4, 0.2), (3.2, -0.4),
       (2.2, -0.9), (1.6, -2.0), (0.6, -3.4), (-0.4, -3.5), (-1.0, -2.2), (-1.4, -0.6), (-2.6, -0.6),
       (-3.8, 0.2), (-4.8, 0.8)]
ASIA = [(1.9, 2.8), (3.0, 3.4), (5.5, 3.3), (6.5, 2.0), (5.4, 0.6), (4.3, -0.5), (3.6, 0.3), (2.9, 1.4), (2.3, 2.1)]
PIN_I, PIN_O, PIN_M = (-3.7, 2.3), (1.3, 0.0), (2.4, 2.5)


class Atlas:
    def __init__(self, s=0.95, cx=0.0, cy=-0.1):
        self.s, self.cx, self.cy = s, cx, cy

    def P(self, x, y):
        return np.array([self.cx + (x - 0.85) * self.s, self.cy + (y + 0.05) * self.s, 0.0])

    def land(self):
        a = Polygon(*[self.P(*p) for p in AFR], stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        b = Polygon(*[self.P(*p) for p in ASIA], stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        return VGroup(a, b)


def pin(col=TEXT):
    tri = Polygon([0, 0, 0], [-0.17, 0.4, 0], [0.17, 0.4, 0], stroke_width=0, fill_color=col, fill_opacity=1)
    head = Circle(radius=0.2, stroke_width=0, fill_color=col, fill_opacity=1).move_to([0, 0.52, 0])
    dot = Dot(radius=0.07, color=BG).move_to([0, 0.52, 0])
    return VGroup(tri, head, dot)


def pin_at(p, col=TEXT):
    g = pin(col)
    g.move_to(p + UP * g.height / 2)
    return g


def motes(seed, n=18, col=(GOLD, TEAL, GREY)):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.07, 0.13), color=col[rng.randint(len(col))])
        d.set_opacity(rng.uniform(0.35, 0.7))
        d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
        d.v = (rng.uniform(-0.15, 0.15), rng.uniform(0.1, 0.3))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 4.0:
                m.shift(DOWN * 8.0)
            if abs(m.get_x()) > 7.1:
                m.shift(LEFT * 14.2 * np.sign(m.get_x()))
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-5)
    return g


def pulse(m, lo=0.45, rate=2.4):
    m.pt = 0.0

    def up(x, dt):
        x.pt += dt
        x.set_opacity(lo + (1 - lo) * abs(np.sin(rate * x.pt)))
    m.add_updater(up)
    return m


def pulse_chip(c, rate=2.4, phase=0.0):
    c.pt = phase

    def up(x, dt):
        x.pt += dt
        a = 0.35 + 0.65 * abs(np.sin(rate * x.pt))
        x[0].set_stroke(opacity=a)
        x[1].set_opacity(a)
    c.add_updater(up)
    return c


def breathe(m, a=0.55, b=1.0, rate=2.0):
    m.bt = 0.0

    def up(x, dt):
        x.bt += dt
        x.set_fill(opacity=a + (b - a) * (0.5 + 0.5 * np.sin(rate * x.bt)))
    m.add_updater(up)
    return m


def skull(scale=1.0, col=TEAL):
    cran = Ellipse(width=2.2, height=1.9).move_to([0, 0.35, 0])
    face = Polygon([0.45, 0.65, 0], [1.0, 0.35, 0], [1.12, -0.35, 0], [0.7, -0.8, 0], [-0.1, -0.8, 0],
                   [-0.45, -0.2, 0]).round_corners(0.12)
    jaw = Polygon([-0.25, -0.75, 0], [0.75, -0.8, 0], [0.8, -1.2, 0], [0.1, -1.45, 0], [-0.5, -1.1, 0]).round_corners(0.1)
    teeth = VGroup(*[Rectangle(width=0.12, height=0.17, stroke_width=0, fill_color=TEXT, fill_opacity=1)
                     .move_to([0.02 + 0.15 * i, -0.84, 0]) for i in range(5)])
    eye = Circle(radius=0.13, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([0.5, 0.32, 0])
    for p in (cran, face, jaw):
        p.set_stroke(col, 4).set_fill(col, 0.35)
    g = VGroup(cran, face, jaw, teeth, eye)
    g.cran, g.face, g.jaw, g.teeth = cran, face, jaw, teeth
    g.scale(scale)
    return g


def bone(x, y, ang=0.3, w=0.8):
    return RoundedRectangle(corner_radius=0.07, width=w, height=0.15, stroke_color=TEAL, stroke_width=2,
                            fill_color=TEAL, fill_opacity=0.6).rotate(ang).move_to([x, y, 0])


def flint(x, y, s=1.0, op=0.55):
    pts = [(-0.22, 0.05), (-0.05, 0.2), (0.2, 0.12), (0.26, -0.08), (0.05, -0.2), (-0.18, -0.14)]
    return Polygon(*[[px * s + x, py * s + y, 0] for px, py in pts], stroke_color=GOLD, stroke_width=2.5,
                   fill_color=GOLD, fill_opacity=op).round_corners(0.04 * s)


def flame(h=0.8):
    outer = Polygon([0, 0.5, 0], [0.2, 0.1, 0], [0.15, -0.2, 0], [0, -0.3, 0], [-0.15, -0.2, 0], [-0.2, 0.1, 0],
                    stroke_width=0, fill_color=RED, fill_opacity=0.95).round_corners(0.1)
    inner = Polygon([0, 0.2, 0], [0.09, -0.02, 0], [0, -0.2, 0], [-0.09, -0.02, 0],
                    stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).round_corners(0.05)
    g = VGroup(outer, inner).set_height(h)
    g.ft = 0.0

    def fl(m, dt):
        m.ft += dt
        m.stretch_to_fit_height(h * (1 + 0.12 * np.sin(9 * m.ft)), about_edge=DOWN) if False else None
        m.set_opacity(0.75 + 0.25 * np.sin(11 * m.ft))
    g.add_updater(fl)
    return g


def tag(text, size=28, col=GOLD):
    return chip(text, color=col, size=size, pad=0.16, fill_opacity=0.22)


# ---------- cut-away ground (shared by the Jebel Irhoud and Omo scenes) ----------
GX0, GX1 = -5.2, 5.2


def rect(top, bot, color, op=1.0):
    return Rectangle(width=GX1 - GX0, height=top - bot, stroke_width=0, fill_color=color, fill_opacity=op
                     ).move_to([(GX0 + GX1) / 2, (top + bot) / 2, 0])


def ground(ash=False):
    A = rect(1.0, 0.6, ASH if ash else SOIL, 0.9 if ash else 1)
    B = rect(0.6, -0.6, SED)
    C = rect(-0.6, -1.8, BAND)
    D = rect(-1.8, -3.6, DEEP)
    lines = VGroup(*[Line([GX0, y, 0], [GX1, y, 0], color=GREY, stroke_width=1.5).set_opacity(0.6)
                     for y in (0.6, -0.6, -1.8)])
    frame = Rectangle(width=GX1 - GX0, height=4.6, stroke_color=GREY, stroke_width=3).move_to([0, -1.3, 0])
    g = VGroup(A, B, C, D, lines, frame)
    g.A, g.B, g.C, g.D = A, B, C, D
    return g


def irhoud_finds(full=True):
    sk = skull(0.3).move_to([-1.5, -1.2, 0])
    bones = VGroup(bone(-2.7, -1.35, 0.3), bone(-0.5, -1.4, -0.4, 0.6))
    fl = VGroup(*[flint(x, y, 1.1) for x, y in [(0.9, -1.15), (1.7, -1.35), (2.5, -1.1), (3.3, -1.3)]])
    return sk, bones, fl


def ring_pin_label(P, text):
    p = pin_at(P)
    t = T(text, 28, TEXT).next_to(p, RIGHT, buff=0.15)
    return p, t


def gauge(center, w=0.9, h=3.2, col=GOLD):
    box = Rectangle(width=w, height=h, stroke_color=col, stroke_width=3).move_to(center)
    tr = ValueTracker(0.0)
    fill = always_redraw(lambda: Rectangle(width=w - 0.12, height=max(0.001, (h - 0.12) * tr.get_value()),
                                           stroke_width=0, fill_color=col, fill_opacity=0.85
                                           ).move_to(box.get_bottom() + UP * 0.06, aligned_edge=DOWN))
    return box, fill, tr


def stream(starts, tgt, n, col, rate=0.3):
    g = VGroup()
    for i in range(n):
        s = np.array(starts[i % len(starts)], dtype=float)
        d = Dot(radius=0.07, color=col).move_to(s)
        d.s, d.tgt, d.ph = s, np.array(tgt, dtype=float) + np.array([np.sin(i * 2.1) * 0.6, np.cos(i * 1.7) * 0.4, 0]), i / n

        def up(m, dt):
            m.ph = (m.ph + dt * rate) % 1
            m.move_to(m.s + (m.tgt - m.s) * m.ph)
            m.set_opacity(np.sin(np.pi * m.ph))
        d.add_updater(up)
        g.add(d)
    return g


def checklist(scale=1.0):
    a = T("What was dated?", 34, GOLD, weight=BOLD)
    b = T("Where did it lie?", 34, TEAL, weight=BOLD)
    t = VGroup(a, b).arrange(DOWN, buff=0.18)
    box = RoundedRectangle(corner_radius=0.18, width=t.width + 1.7, height=t.height + 0.9, stroke_color=TEXT,
                           stroke_width=3, fill_color=BG, fill_opacity=0.92)
    g = VGroup(box, t)
    g.a, g.b = a, b
    return g.scale(scale)


def schem():
    return T("schematic", 22, LBL).move_to([6.1, -3.55, 0])


# ===========================================================================================
class S00Title(TitleCard):
    LESSON = "Human Evolutionary History: An African Origin and Archaic Ancestry"
    TITLE = "What Was Dated?"


class S01Question(SpokenScene):
    def construct(self):
        at = Atlas()
        self.add(motes(1))
        land = at.land()
        head = T("One place? One date?", 38, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.at("Did our species")
        self.play(Create(land), Write(head), run_time=2.6)
        self.at("A skull from")
        p, t = ring_pin_label(at.P(*PIN_I), "Jebel Irhoud")
        pos = p.get_center().copy()
        p.shift(UP * 1.2).set_opacity(0)
        self.play(p.animate.move_to(pos).set_opacity(1), run_time=0.8)
        self.at("Morocco")
        self.play(Write(t), run_time=0.8)
        self.at("seems to answer yes")
        sk = skull(0.15).move_to(p.get_top())
        self.add(sk)
        self.play(sk.animate.scale(4.5).move_to([-6.1, -0.2, 0]), run_time=1.8)
        self.at("It comes with a date")
        tg = VGroup(T("~315,000", 30, GOLD, weight=BOLD), T("years?", 30, GOLD, weight=BOLD)).arrange(DOWN, buff=0.1)
        tg.next_to(sk, DOWN, buff=0.3).shift(RIGHT * 0.75)
        self.play(FadeIn(tg, shift=UP * 0.2), run_time=0.8)
        pulse(tg[1])
        self.at("looks precise")
        self.play(Indicate(tg[0], color=GOLD, scale_factor=1.15), run_time=1.0)
        self.finish()


class S02Mosaic(SpokenScene):
    def construct(self):
        self.add(motes(2))
        sk = skull(1.3).move_to([0, -0.2, 0])
        self.add(sk)
        self.at("It has a face")
        self.play(Rotate(sk, angle=0.12, rate_func=there_and_back), run_time=1.2)
        for p in (sk.face, sk.jaw):
            self.play(p.animate.set_fill(TEAL, 0.7).set_stroke(TEAL, 7), run_time=0.8)
        l1 = VGroup(T("face, jaw, teeth:", 30, TEAL), T("modern", 30, TEAL, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([4.5, -0.9, 0])
        ln1 = Line(sk.face.get_right() + DOWN * 0.2, l1.get_left() + LEFT * 0.1, color=TEAL, stroke_width=3)
        self.play(FadeIn(l1), Create(ln1), run_time=0.9)
        self.at("Its brain case")
        old = sk.cran
        new = Ellipse(width=3.0, height=1.4).move_to([-0.35, 0.2, 0]).set_stroke(LBL, 4).set_fill(GREY, 0.5)
        new.scale(1.3)
        new.move_to(old.get_center() + LEFT * 0.4 + DOWN * 0.25)
        self.play(Transform(old, new), run_time=2.0)
        l2 = VGroup(T("braincase:", 30, LBL), T("more primitive", 30, LBL, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([-4.3, 2.3, 0])
        ln2 = Line(l2.get_right() + RIGHT * 0.1, old.get_left() + RIGHT * 0.8, color=LBL, stroke_width=3)
        self.play(FadeIn(l2), Create(ln2), run_time=0.9)
        self.at("It is a mosaic")
        ban = T("mosaic", 52, GOLD, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.play(Write(ban), run_time=1.2)
        self.play(Rotate(sk, angle=-0.1, rate_func=there_and_back), run_time=1.6)
        self.finish()


class S03What(SpokenScene):
    def construct(self):
        self.add(motes(3))
        self.at("Now ask the question")
        p, t = ring_pin_label(np.array([-4.2, 1.0, 0]), "Jebel Irhoud")
        g = ground()
        self.add(p)
        self.play(GrowFromEdge(g, UP), Write(t), run_time=2.2)
        sk, bones, fl = irhoud_finds()
        self.play(FadeIn(sk), FadeIn(bones), run_time=1.0)
        self.at("What was actually dated")
        q = T("What was actually dated?", 40, TEXT, font=TITLE_FONT).move_to([0, 2.65, 0])
        self.play(Write(q), run_time=1.5)
        tg = tag("~315,000").move_to([-0.2, 1.75, 0])
        stem = Line(tg.get_bottom(), sk.get_top(), color=GOLD, stroke_width=2.5)
        self.play(FadeIn(tg, shift=DOWN * 0.2), Create(stem), run_time=0.8)
        self.at("Not the skull itself")
        self.play(Wiggle(tg, scale_value=1.1), sk.animate.set_opacity(0.45), run_time=1.5)
        self.at("Flints lay beside")
        self.play(LaggedStart(*[GrowFromCenter(f) for f in fl], lag_ratio=0.2), run_time=1.0)
        lb = VGroup(T("bones", 28, TEAL).move_to([-1.8, -2.4, 0]), T("flints", 28, GOLD).move_to([2.1, -2.4, 0]))
        self.play(FadeIn(lb), run_time=0.3)
        st2 = Line(tg.get_bottom(), [1.9, -0.9, 0], color=GOLD, stroke_width=2.5)
        self.play(tg.animate.move_to([1.9, 1.75, 0]), Transform(stem, st2), run_time=0.7)
        self.at("and a fire had heated them")
        fs = VGroup(*[flame(0.6).move_to(f.get_center() + UP * 0.45) for f in fl[::2]])
        self.play(FadeIn(fs), run_time=0.5)
        self.finish()


class S04Tl(SpokenScene):
    def construct(self):
        self.add(motes(4))
        fx = np.array([-3.8, -0.5, 0])
        fl = flint(0, 0, 6.0, 0.35).move_to(fx)
        box, fill, tr = gauge([-0.9, -0.5, 0], h=3.4)
        tr.set_value(0.6)
        gl = T("dose stored", 28, GOLD).next_to(box, UP, buff=0.2)
        self.add(fl, box, fill)
        self.play(FadeIn(gl), run_time=0.6)
        self.at("Enough heat resets")
        fm = flame(1.5).move_to(fx + UP * 1.5)
        self.play(FadeIn(fm), run_time=0.4)
        self.play(tr.animate.set_value(0.0), run_time=1.8)
        self.at("Afterward")
        self.play(FadeOut(fm), run_time=0.6)
        self.at("radiation from the flint")
        inner = VGroup(*[Dot(radius=0.09, color=GOLD).move_to(fx + np.array([dx, dy, 0]))
                         for dx, dy in [(-0.7, 0.2), (0.3, -0.4), (0.8, 0.3), (-0.2, 0.5)]])
        for d in inner:
            pulse(d, 0.3, 3.0)
        self.play(FadeIn(inner), tr.animate.set_value(0.25), run_time=1.2)
        self.at("its surroundings")
        sed = Rectangle(width=6.2, height=0.7, stroke_color=ASH, stroke_width=2, fill_color=ASH, fill_opacity=0.35
                        ).move_to([-3.4, -3.4, 0])
        sl = T("sediment", 26, ASH).move_to(sed)
        self.play(FadeIn(sed), FadeIn(sl), run_time=0.4)
        st = stream([[x, -3.05, 0] for x in np.linspace(-5.8, -1.6, 7)], fx + DOWN * 0.8, 10, GOLD, 0.3)
        self.add(st)
        self.play(tr.animate.set_value(0.55), run_time=0.5)
        self.at("builds it back")
        cr = Arrow([-3.8, 3.2, 0], [-3.8, 1.2, 0], color=LBL, stroke_width=4, buff=0)
        cl = T("cosmic rays", 26, LBL).next_to(cr, RIGHT, buff=0.15)
        self.play(GrowArrow(cr), FadeIn(cl), tr.animate.set_value(0.85), run_time=1.6)
        self.at("The stored dose")
        e1 = T("dose stored / yearly dose", 32, TEXT).move_to([3.9, 1.7, 0])
        e2 = T("= time since heating", 32, TEXT).move_to([3.9, 1.0, 0])
        self.play(Write(e1), run_time=1.2)
        self.play(Write(e2), run_time=1.0)
        self.at("gives the time since heating")
        r1 = T("315,000 +/- 34,000 years", 32, GOLD, weight=BOLD).move_to([3.9, -0.6, 0])
        r2 = T("(Richter et al., 2017)", 26, LBL).move_to([3.9, -1.3, 0])
        self.play(Write(r1), FadeIn(r2), run_time=1.5)
        self.finish()


def cut_irhoud(scene, tag_x=1.9, with_tag=True):
    g = ground()
    p, t = ring_pin_label(np.array([-4.2, 1.0, 0]), "Jebel Irhoud")
    sk, bones, fl = irhoud_finds()
    items = [g, p, t, sk, bones, fl]
    tg = None
    if with_tag:
        tg = tag("~315,000").move_to([tag_x, 1.75, 0])
        items += [tg]
    scene.add(*items)
    return g, sk, fl, tg


class S05Beside(SpokenScene):
    def construct(self):
        self.add(motes(5))
        g, sk, fl, tg = cut_irhoud(self)
        self.at("this date belongs")
        a1 = Arrow([3.8, 0.0, 0], [3.0, -0.95, 0], color=GOLD, stroke_width=5, buff=0)
        l1 = T("dated", 30, GOLD, weight=BOLD).next_to(a1, UP, buff=0.1)
        self.play(GrowArrow(a1), FadeIn(l1), Indicate(fl, color=GOLD), run_time=1.6)
        self.at("not to the bones themselves")
        a2 = Arrow([-3.6, 0.0, 0], [-1.9, -0.95, 0], color=TEAL, stroke_width=5, buff=0)
        l2 = T("fossil", 30, TEAL, weight=BOLD).next_to(a2, UP, buff=0.1)
        self.play(GrowArrow(a2), FadeIn(l2), Indicate(sk, color=TEAL), run_time=1.6)
        self.at("Every date in the story")
        c = checklist(0.85).move_to([0, -2.7, 0])
        self.play(FadeIn(c, shift=UP * 0.3), run_time=1.0)
        self.play(Indicate(c.a, color=GOLD), run_time=0.9)
        self.play(Indicate(c.b, color=TEAL), run_time=0.9)
        self.finish()


def omo_layers(ash=True):
    g = ground(ash)
    sk = skull(0.3).move_to([0.6, -1.2, 0])
    return g, sk


def volcano():
    v = Polygon([3.5, 1.0, 0], [4.15, 2.4, 0], [4.8, 1.0, 0], stroke_color=GREY, stroke_width=3,
                fill_color=GREY, fill_opacity=0.4)
    return v


def puffs(n=8, seed=0):
    rng = np.random.RandomState(seed)
    g = VGroup()
    for i in range(n):
        d = Dot(radius=rng.uniform(0.08, 0.14), color=ASH)
        d.s = np.array([4.15, 2.4, 0.0])
        d.tgt = np.array([rng.uniform(-3.5, 4.5), 0.8, 0.0])
        d.ph = i / n

        def up(m, dt):
            m.ph = (m.ph + dt * 0.35) % 1
            f = m.ph
            m.move_to(m.s + (m.tgt - m.s) * f + UP * 1.0 * np.sin(np.pi * f))
            m.set_opacity(0.9 * np.sin(np.pi * f))
        d.add_updater(up)
        g.add(d)
    return g


class S06Omo(SpokenScene):
    def construct(self):
        at = Atlas()
        self.add(motes(6))
        land = at.land()
        pi = pin_at(at.P(*PIN_I))
        pi_l = T("Jebel Irhoud", 28, TEXT).next_to(pi, RIGHT, buff=0.15)
        self.add(land, pi, pi_l)
        self.at("Travel east")
        po = pin_at(at.P(*PIN_O))
        pos = po.get_center().copy()
        po.shift(UP * 1.2).set_opacity(0)
        trav = DashedLine(at.P(*PIN_I) + DOWN * 0.1, at.P(*PIN_O) + UP * 0.1, color=LBL, stroke_width=3)
        self.play(Create(trav), run_time=1.4)
        self.at("to Omo")
        ol = T("Omo I", 28, TEXT).next_to(po, LEFT, buff=0.15)
        self.play(po.animate.move_to(pos).set_opacity(1), FadeIn(ol), run_time=1.0)
        self.play(Indicate(po, color=TEXT), run_time=1.0)
        self.at("Here a fossil lies")
        self.play(FadeOut(VGroup(land, pi, pi_l, po, ol, trav)), run_time=0.5)
        g, sk = omo_layers(ash=False)
        p, t = ring_pin_label(np.array([-4.2, 1.0, 0]), "Omo I")
        self.add(p)
        self.play(GrowFromEdge(g, UP), Write(t), run_time=1.5)
        self.play(FadeIn(sk, shift=DOWN * 0.3), run_time=0.8)
        self.at("and a band of volcanic ash")
        sch = schem()
        self.play(g.A.animate.set_fill(ASH, 0.9), FadeIn(sch), run_time=1.5)
        self.play(Indicate(g.A, color=ASH), run_time=1.3)
        self.at("The eruption that laid the ash")
        v = volcano()
        pf = puffs()
        self.play(FadeIn(v, shift=UP * 0.3), run_time=0.8)
        self.add(pf)
        self.at("has been dated")
        tg = tag("~233,000 years (eruption)").move_to([0.6, 1.75, 0])
        tg.shift(UP * 0.8).set_opacity(0)
        self.play(tg.animate.shift(DOWN * 0.8).set_opacity(1), run_time=0.9)
        self.finish()


def omo_still(scene, ash_tag=True):
    g, sk = omo_layers(True)
    p, t = ring_pin_label(np.array([-4.2, 1.0, 0]), "Omo I")
    v = volcano()
    tg = tag("~233,000 years (eruption)").move_to([0.6, 1.75, 0])
    scene.add(g, p, t, sk, v, schem(), tg)
    return g, sk, tg


class S07Predict(SpokenScene):
    def construct(self):
        self.add(motes(7))
        g, sk, tg = omo_still(self)
        pf = puffs()
        self.add(pf)
        self.at("The ash lies above the bone")
        self.play(Indicate(g.A, color=ASH), run_time=1.5)
        self.at("and the date belongs to the ash")
        self.play(Indicate(tg, color=GOLD), run_time=1.2)
        ar = Arrow(tg.get_bottom(), sk.get_top() + UP * 0.1, color=GOLD, stroke_width=5, buff=0.05)
        self.play(GrowArrow(ar), run_time=1.3)
        breathe(sk.cran, 0.2, 0.7, 3.0)
        self.at("So is the bone older or younger")
        c1 = chip("older?", TEAL, 32).move_to([-2.0, 0.0, 0])
        c2 = chip("younger?", GOLD, 32).move_to([3.2, 0.0, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.7)
        pulse_chip(c1, 2.4, 0.0)
        pulse_chip(c2, 2.4, 0.65)
        breathe(g.A)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        self.add(motes(8))
        g, sk, tg = omo_still(self)
        ar = Arrow(tg.get_bottom(), sk.get_top() + UP * 0.1, color=GOLD, stroke_width=5, buff=0.05)
        c1 = chip("older?", TEAL, 32).move_to([-2.0, 0.0, 0])
        c2 = chip("younger?", GOLD, 32).move_to([3.2, 0.0, 0])
        self.add(ar, c1, c2, puffs())
        pulse_chip(c1, 2.4, 0.0)
        pulse_chip(c2, 2.4, 0.65)
        breathe(g.A)
        bt = ValueTracker(0)
        bar = always_redraw(lambda: Rectangle(width=max(0.01, 13.6 * bt.get_value()), height=0.2, stroke_width=0, fill_color=TEXT, fill_opacity=0.8).move_to([-6.8, -3.7, 0], aligned_edge=LEFT))
        self.add(bar)
        tr = ValueTracker(0)
        ring = always_redraw(lambda: Arc(radius=0.4, start_angle=PI / 2, angle=-TAU * max(0.001, tr.get_value()),
                                         color=TEXT, stroke_width=6).move_to([4.2, 2.6, 0]))
        back = Circle(radius=0.4, color=GREY, stroke_width=3).move_to([4.2, 2.6, 0])
        self.add(back, ring)
        self.play(tr.animate.set_value(1), bt.animate.set_value(1), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S09Reveal(SpokenScene):
    def construct(self):
        self.add(motes(9))
        g, sk, tg = omo_still(self)
        ar = Arrow(tg.get_bottom(), sk.get_top() + UP * 0.1, color=GOLD, stroke_width=5, buff=0.05)
        c1 = chip("older?", TEAL, 32).move_to([-2.0, 0.0, 0])
        c2 = chip("younger?", GOLD, 32).move_to([3.2, 0.0, 0])
        self.add(ar, c1, c2)
        self.at("At least as old")
        tick = T("OK", 32, TEAL, weight=BOLD)
        c1n = chip("older? yes", TEAL, 32).move_to(c1)
        self.play(Transform(c1, c1n), FadeOut(c2), FadeOut(ar), run_time=1.2)
        self.at("The ash fell after")
        self.remove(tick)
        self.play(g.A.animate.shift(UP * 1.4).set_opacity(0), g.B.animate.shift(UP * 1.4).set_opacity(0),
                  FadeOut(tg), FadeOut(c1), run_time=1.0)
        self.at("the bone was buried")
        sh = g.B.copy().shift(UP * 1.4).set_opacity(0)
        self.play(g.B.animate.shift(DOWN * 1.4).set_opacity(1), run_time=1.0)
        pf = puffs()
        self.add(pf)
        self.play(g.A.animate.shift(DOWN * 1.4).set_opacity(0.9), run_time=1.0)
        self.at("So its date is a minimum")
        nt = VGroup(T("at least ~233,000 years", 28, GOLD, weight=BOLD), T("(minimum)", 28, GOLD)).arrange(DOWN, buff=0.08)
        nt.move_to([-2.4, -1.2, 0])
        self.play(FadeIn(nt, shift=LEFT * 0.3), run_time=1.0)
        self.at("not dated directly")
        self.play(Indicate(nt, color=GOLD), run_time=1.2)
        self.finish()


def mapworld(scene, labels=True, pins=("I", "O")):
    at = Atlas()
    land = at.land()
    items = [land]
    pp = {}
    for k, P, nm, side in (("I", PIN_I, "Jebel Irhoud", RIGHT), ("O", PIN_O, "Omo I", LEFT), ("M", PIN_M, "Misliya Cave", RIGHT)):
        if k in pins:
            p = pin_at(at.P(*P))
            pp[k] = p
            items.append(p)
            if labels:
                items.append(T(nm, 28, TEXT).next_to(p, side, buff=0.15))
    scene.add(*items)
    return at, land, pp


class S10Misliya(SpokenScene):
    def construct(self):
        self.add(motes(10))
        at, land, pp = mapworld(self)
        self.at("Now cross into Western Asia")
        dot = Dot(radius=0.12, color=TEAL).move_to(at.P(*PIN_O))
        path = ArcBetweenPoints(at.P(*PIN_O), at.P(*PIN_M), angle=-0.8)
        self.play(MoveAlongPath(dot, path), Create(path.copy().set_stroke(TEAL, 3)), run_time=2.6)
        self.at("Cave in Israel")
        pm = pin_at(at.P(*PIN_M))
        pos = pm.get_center().copy()
        pm.shift(UP * 1.2).set_opacity(0)
        ml = T("Misliya Cave", 28, TEXT).next_to(pos + DOWN * 0.1 + RIGHT * 0.1, RIGHT, buff=0.15)
        self.play(pm.animate.move_to(pos).set_opacity(1), FadeOut(dot), run_time=0.9)
        self.play(FadeIn(ml), run_time=0.6)
        self.at("a jaw with teeth")
        jaw = skull(0.5)
        j = VGroup(jaw.jaw, jaw.teeth).move_to([5.5, -1.0, 0]).scale(3.0)
        j[0].set_fill(TEAL, 0.5)
        ln = Line(pm.get_center() + RIGHT * 1.4 + DOWN * 0.65, j.get_top() + UP * 0.05, color=TEAL, stroke_width=3)
        self.play(GrowFromCenter(j), Create(ln), run_time=1.3)
        sh = Dot(radius=0.1, color=TEAL)
        sh.ph = 0.0
        sh.add_updater(lambda m, dt: (setattr(m, 'ph', (m.ph + dt * 0.25) % 1), m.move_to(path.point_from_proportion(m.ph))))
        self.add(sh)
        breathe(j[0], 0.25, 0.75, 3.0)
        self.at("It was dated far earlier")
        pa = VGroup(T("177,000-194,000 years ago", 28, GOLD, weight=BOLD)).move_to([-2.8, -3.0, 0])
        bg = RoundedRectangle(corner_radius=0.12, width=6.2, height=1.2, stroke_width=0, fill_color=BG, fill_opacity=0.9).move_to([-3.0, -3.1, 0])
        pa.move_to(bg.get_center() + UP * 0.25)
        self.play(FadeIn(bg), Write(pa), run_time=1.5)
        self.at("than the dispersal")
        pb = VGroup(T("textbook dispersal", 28, LBL), T("~60,000 years ago", 28, LBL)).arrange(DOWN, buff=0.1).move_to([3.6, -3.0, 0])
        bg2 = RoundedRectangle(corner_radius=0.12, width=5.4, height=1.2, stroke_width=0, fill_color=BG, fill_opacity=0.9).move_to(pb)
        self.play(FadeIn(bg2), FadeIn(pb), run_time=1.0)
        self.play(Create(Line(pb.get_left() + LEFT * 0.1, pb.get_right() + RIGHT * 0.1, color=LBL, stroke_width=3)), run_time=1.0)
        self.at("Part of that dating")
        ch = T("(part of the dating challenged)", 28, GOLD).move_to(bg.get_center() + DOWN * 0.25)
        self.play(Write(ch), Wiggle(j), run_time=1.5)
        self.finish()


class S11Presence(SpokenScene):
    def construct(self):
        self.add(motes(11))
        at, land, pp = mapworld(self, labels=False, pins=("I", "O", "M"))
        origin = at.P(-0.2, 0.8)
        og = Dot(radius=0.14, color=TEAL).move_to(origin)
        ol = T("Africa", 30, TEAL, weight=BOLD).next_to(og, DOWN, buff=0.15)
        self.add(og, ol)
        self.at("Does that mean")
        thin = ArcBetweenPoints(origin, at.P(*PIN_M) + DOWN * 0.1, angle=-0.5).set_stroke(TEAL, 3)
        q = T("descendants?", 32, TEAL).move_to([5.0, -1.2, 0])
        self.play(Create(thin), run_time=2.2)
        self.play(FadeIn(q), run_time=0.8)
        self.at("Not by itself")
        self.play(FadeOut(thin), FadeOut(q), run_time=1.0)
        self.at("A fossil shows presence")
        card = T("presence is not ancestry", 36, GOLD, weight=BOLD).move_to([0, -3.1, 0])
        bg = RoundedRectangle(corner_radius=0.15, width=card.width + 0.6, height=0.9, stroke_color=GOLD, stroke_width=2,
                              fill_color=BG, fill_opacity=0.92).move_to(card)
        self.play(FadeIn(bg), Write(card), run_time=1.6)
        self.play(Indicate(pp["M"], color=TEXT), run_time=1.0)
        self.at("Genomes of living")
        thick = ArcBetweenPoints(origin + RIGHT * 0.3, at.P(5.6, 1.8), angle=-0.9).set_stroke(TEAL, 9)
        self.play(Create(thick), run_time=2.6)
        self.at("a later dispersal")
        ll = T("later dispersal (genomes)", 30, TEAL).move_to([3.6, 3.45, 0])
        self.play(Write(ll), run_time=1.2)
        self.finish()


class S12Timebar(SpokenScene):
    def construct(self):
        self.add(motes(12))
        at, land, pp = mapworld(self, labels=False, pins=("I", "O", "M"))
        og = Dot(radius=0.14, color=TEAL).move_to(at.P(-0.2, 0.8))
        self.add(og)
        small = Atlas(0.5, -3.4, 1.55)
        world = VGroup(land, *pp.values(), og)
        tgt = small.land()
        self.at("So the dates do not mark")
        self.play(Transform(land, tgt),
                  *[pp[k].animate.move_to(small.P(*P) + UP * 0.2).scale(0.55) for k, P in (("I", PIN_I), ("O", PIN_O), ("M", PIN_M))],
                  og.animate.move_to(small.P(-0.2, 0.8)).scale(0.7), run_time=1.2)
        X = lambda t: 5.6 - 11.2 * t / 400000
        by = -3.0
        bar = Line([-5.6, by, 0], [5.6, by, 0], color=LBL, stroke_width=4)
        ticks = VGroup(*[VGroup(Line([X(t), by - 0.1, 0], [X(t), by + 0.1, 0], color=LBL, stroke_width=3),
                                T(f"{t:,}" if t else "now", 22, LBL).move_to([X(t), by - 0.4, 0])) for t in (400000, 300000, 200000, 100000, 0)])
        self.play(Create(bar), FadeIn(ticks), run_time=0.7)
        specs = [(315000, -4.3, "heated flints,", "beside", GOLD), (233000, -1.2, "ash, above:", "minimum", ASH),
                 (185000, 2.3, "jaw, partly", "challenged", GOLD)]
        marks = []
        for t, lx, a, b, col in specs:
            lab = VGroup(T(a, 28, col), T(b, 28, col)).arrange(DOWN, buff=0.06).move_to([lx, -1.85, 0])
            mk = Dot(radius=0.13, color=col).move_to([X(t), by, 0])
            ld = Line(lab.get_bottom() + DOWN * 0.05, mk.get_center(), color=col, stroke_width=2.5)
            self.play(FadeIn(lab, shift=DOWN * 0.15), Create(ld), GrowFromCenter(mk), run_time=0.4)
            marks.append(mk)
        self.at("People with partly modern")
        self.play(Indicate(marks[0], color=GOLD, scale_factor=2), Indicate(pp["I"], color=TEXT), run_time=1.3)
        self.at("North Africa")
        s1 = VGroup(T("north Africa:", 32, TEAL, weight=BOLD), T("~300,000 years ago", 32, TEAL)).arrange(DOWN, buff=0.1).move_to([3.4, 2.4, 0])
        self.play(Write(s1), run_time=1.6)
        self.at("They lived in East Africa")
        self.play(Indicate(marks[1], color=ASH, scale_factor=2), Indicate(pp["O"], color=TEXT), run_time=1.3)
        s2 = VGroup(T("east Africa:", 32, TEAL, weight=BOLD), T("by at least ~233,000 years ago", 32, TEAL)).arrange(DOWN, buff=0.1).move_to([3.4, 0.7, 0])
        self.play(Write(s2), run_time=1.6)
        self.finish()


def braid(at):
    xs = [-4.1, -2.6, -1.1, 0.4, 1.6]
    edges = [((0, 0.0), (1, 0.9)), ((0, 0.0), (1, -0.9)), ((1, 0.9), (2, 1.6)), ((1, 0.9), (2, 0.2)),
             ((1, -0.9), (2, -0.2)), ((1, -0.9), (2, -1.6)), ((2, 1.6), (3, 1.0)), ((2, 0.2), (3, 1.0)),
             ((2, -0.2), (3, -1.0)), ((2, -1.6), (3, -1.0)), ((3, 1.0), (4, 0.6)), ((3, -1.0), (4, -0.4)),
             ((3, 1.0), (4, -0.4))]
    out = VGroup()
    for (i, y0), (j, y1) in edges:
        a, b = at.P(xs[i], y0 * 1.3 + 0.4), at.P(xs[j], y1 * 1.3 + 0.4)
        c = CubicBezier(a, a + RIGHT * 0.6, b + LEFT * 0.6, b).set_stroke(TEAL, 6)
        out.add(c)
    return out


class S13Braid(SpokenScene):
    def construct(self):
        self.add(motes(13))
        at, land, pp = mapworld(self, labels=False, pins=())
        self.at("Genomes of living people")
        afr = land[0]
        pops = VGroup(*[Dot(radius=0.12, color=TEAL).move_to(at.P(-2.0 + 0.9 * (i % 4) - 0.3 * (i // 4), 1.8 - 0.8 * (i // 4) + 0.2 * (i % 2))) for i in range(10)])
        for i, d in enumerate(pops):
            d.pt = i * 0.7

            def up(m, dt):
                m.pt += dt
                m.shift([0.25 * np.cos(m.pt) * dt, 0.25 * np.sin(1.3 * m.pt) * dt, 0])
            d.add_updater(up)
        self.play(afr.animate.set_fill(TEAL, 0.3).set_stroke(TEAL, 4), LaggedStart(*[GrowFromCenter(d) for d in pops], lag_ratio=0.15), run_time=3.0)
        self.at("ancestry traces to Africa")
        self.play(Indicate(afr, color=TEAL), run_time=1.5)
        self.at("But the history is not one tree")
        self.play(FadeOut(pops), run_time=0.5)
        trunk = Line(at.P(-1.3, -2.6), at.P(-1.3, 0.2), color=TEXT, stroke_width=8)
        br = VGroup(*[Line(at.P(-1.3, y), at.P(-1.3 + dx, y + 1.0), color=TEXT, stroke_width=5)
                      for y, dx in [(-0.8, -1.2), (-0.8, 1.2), (0.2, -1.5), (0.2, 1.5), (0.2, 0.0)]])
        tree = VGroup(trunk, br)
        self.play(Create(tree), run_time=1.6)
        self.at("with one root")
        rl = T("one place, one date", 30, TEXT).move_to([4.2, -3.2, 0])
        self.play(Write(rl), run_time=1.2)
        self.at("It is connected populations")
        b = braid(at)
        self.play(FadeOut(tree), FadeOut(rl), run_time=0.5)
        self.play(Create(b), run_time=1.4)
        flows = VGroup()
        for i, c in enumerate(b):
            d = Dot(radius=0.09, color=TEXT)
            d.c, d.ph = c, (i * 0.17) % 1

            def up(m, dt):
                m.ph = (m.ph + dt * 0.3) % 1
                m.move_to(m.c.point_from_proportion(m.ph))
            d.add_updater(up)
            flows.add(d)
        self.add(flows)
        self.at("split")
        self.play(Indicate(b[0:2], color=TEXT), run_time=1.2)
        self.at("merged again")
        self.play(Indicate(b[10:13], color=TEXT), run_time=1.2)
        self.add(schem())
        self.finish()


class S14Close(SpokenScene):
    def construct(self):
        self.add(motes(14))
        row = VGroup()
        for nm, x in (("Jebel Irhoud", -4.0), ("Omo I", 0.0), ("Misliya Cave", 4.0)):
            p = pin_at(np.array([x, -2.9, 0]))
            t = T(nm, 28, TEXT).next_to(p, UP, buff=0.12)
            row.add(VGroup(p, t))
        self.at("So whenever you meet")
        self.play(FadeIn(row, lag_ratio=0.3), run_time=1.0)
        for r in row:
            self.play(Indicate(r[0], color=GOLD, scale_factor=1.5), run_time=0.7)
        self.at("ask two plain questions")
        c = checklist(1.4).move_to([0, 0.4, 0])
        self.play(FadeIn(c, shift=UP * 0.3), run_time=1.2)
        self.at("What was dated")
        self.play(Indicate(c.a, color=GOLD, scale_factor=1.2), run_time=1.3)
        self.at("And where did it lie")
        self.play(Indicate(c.b, color=TEAL, scale_factor=1.2), run_time=1.3)
        self.finish()


class S15End(EndCard):
    LINE = "Ask what was dated, and where it lay."
