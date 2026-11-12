"""Two Bodies, One Wheel: plant life cycles (Biochemistrypedia explainer, chapter 1).

COLOUR MAP: haploid n = GOLD, diploid 2n = TEAL, triploid 3n = CORAL, mitosis = GREY copy arrow,
meiosis and fusion = white round gates.  The wheel is a schematic ring drawn clockwise.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

CORAL = "#F2735F"
WATER = "#4DA3E8"
SOIL = "#7A5A3C"
RING = "#A9B1BF"
LEAF = "#5FAE63"
DARK = "#10131A"
BROWN = "#B9824F"

C0 = np.array([0.0, 0.1, 0.0])     # the big wheel
RA, RB = 4.8, 2.7
M = 20.0                           # meiosis gate angle
F = -200.0                         # fusion gate angle (unwrapped; = 160 degrees)


# ---------------------------------------------------------------- geometry helpers
def P(c, ra, rb, deg):
    a = np.radians(deg)
    return np.array([c[0] + ra * np.cos(a), c[1] + rb * np.sin(a), 0.0])


def arc(c, ra, rb, a, b, color=RING, w=8):
    return ParametricFunction(lambda s: P(c, ra, rb, a + (b - a) * s), t_range=[0, 1, 0.01],
                              color=color, stroke_width=w)


def tips(c, ra, rb, degs, color=RING, size=0.2):
    g = VGroup()
    for a in degs:
        d = np.array([ra * np.sin(np.radians(a)), -rb * np.cos(np.radians(a)), 0])
        t = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(size)
        t.rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(P(c, ra, rb, a))
        g.add(t)
    return g


def legend():
    def item(col, s, live=True):
        d = Dot(radius=0.17, color=col).set_opacity(1 if live else 0.35)
        t = T(s, 24, TEXT if live else GREY)
        return VGroup(d, t).arrange(RIGHT, buff=0.15)
    a = item(GOLD, "n  haploid")
    b = item(TEAL, "2n  diploid")
    c = item(CORAL, "3n  later", False)
    row = VGroup(a, b, c).arrange(RIGHT, buff=0.8).move_to([-1.2, -3.5, 0])
    sch = T("schematic", 22, GREY).move_to([5.7, -3.5, 0])
    g = VGroup(row, sch)
    g.coral = c
    return g


def gate_m(pos, r=0.62, size=22):
    c = Circle(radius=r, stroke_color=WHITE, stroke_width=5, fill_color=BG, fill_opacity=1)
    t = T("2n → n", size, TEXT)
    g = VGroup(c, t).move_to(pos)
    g.set_z_index(20)
    return g


def gate_f(pos, r=0.55):
    c = Circle(radius=r, stroke_color=WHITE, stroke_width=5, fill_color=BG, fill_opacity=1)
    t = T("+", 48, TEXT, weight=BOLD)
    g = VGroup(c, t).move_to(pos)
    g.set_z_index(20)
    return g


def gate_small(pos, r=0.2):
    return Circle(radius=r, stroke_color=WHITE, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(pos)


def copy_arrow(pos, r=0.4, color=GREY, w=6):
    a = Arc(radius=r, start_angle=0.7, angle=4.6, stroke_color=color, stroke_width=w)
    a.add_tip(tip_length=0.2, tip_width=0.2)
    return a.move_to(pos)


def dotc(color, r=0.25, pos=ORIGIN):
    return Circle(radius=r, stroke_color=WHITE, stroke_width=2, fill_color=color, fill_opacity=1).move_to(pos)


def token(kind, pos=ORIGIN):
    col = TEAL if kind == "2n" else GOLD
    c = Circle(radius=0.34, stroke_color=WHITE, stroke_width=3, fill_color=col, fill_opacity=1)
    t = T(kind, 24, DARK, weight=BOLD)
    return VGroup(c, t).move_to(pos)


def egg(pos, r=0.32, color=GOLD):
    return dotc(color, r, pos)


def sperm(pos, color=GOLD):
    head = Dot(radius=0.15, color=color)
    tail = ParametricFunction(lambda s: np.array([-s * 0.5, 0.07 * np.sin(s * 14), 0]), t_range=[0, 1, 0.02],
                              color=color, stroke_width=4)
    return VGroup(head, tail).move_to(pos)


def body_box(txt, color, size=28, pos=ORIGIN, dim=False):
    lab = T(txt, size, TEXT)
    bg = RoundedRectangle(corner_radius=0.18, width=lab.width + 0.5, height=lab.height + 0.4, stroke_width=0,
                          fill_color=BG, fill_opacity=1)
    r = RoundedRectangle(corner_radius=0.18, width=lab.width + 0.5, height=lab.height + 0.4, stroke_color=color,
                         stroke_width=4, fill_color=color, fill_opacity=0.3)
    g = VGroup(bg, r, lab).move_to(pos)
    if dim:
        r.set_fill(opacity=0.0).set_stroke(opacity=0.4)
        lab.set_opacity(0.4)
    return g


def bob(m, amp=0.06, per=2.5, phase=0.0):
    m.bt = phase
    m.bprev = 0.0

    def up(x, dt):
        x.bt += dt
        y = amp * np.sin(2 * np.pi * x.bt / per)
        x.shift(UP * (y - x.bprev))
        x.bprev = y
    m.add_updater(up)
    return m


def breathe(m, amp=0.03, per=3.0, phase=0.0):
    m.brt = phase
    m.brprev = 1.0

    def up(x, dt):
        x.brt += dt
        s = 1 + amp * np.sin(2 * np.pi * x.brt / per)
        x.scale(s / x.brprev)
        x.brprev = s
    m.add_updater(up)
    return m


def add_sway(shoots, amp=0.03, per=4.0):
    for i, s in enumerate(shoots):
        s.sw_t = i * 1.3
        s.sw_cur = 0.0
        s.sw_base = s.get_bottom()

        def up(m, dt):
            m.sw_t += dt
            a = amp * np.sin(2 * np.pi * m.sw_t / per)
            m.rotate(a - m.sw_cur, about_point=m.sw_base)
            m.sw_cur = a
        s.add_updater(up)


def pls(m, k=1.2):
    return ScaleInPlace(m, k, rate_func=there_and_back)


def panel(c, ra, rb):
    e = Ellipse(width=2 * ra, height=2 * rb, stroke_width=0, fill_color="#252F46", fill_opacity=1).move_to(c)
    e.set_z_index(-3)
    return e


def ring_world():
    ring = arc(C0, RA, RB, 90, -270, RING, 8)
    return ring, tips(C0, RA, RB, [60, -60, -120, 120])


def rider(c, ra, rb, m, f, th, off=0.0, r=0.24):
    """A dot that circles an arc-coloured wheel; gold on the gold arc, teal on the teal arc."""
    d = Circle(radius=r, stroke_color=WHITE, stroke_width=2, fill_color=GOLD, fill_opacity=1)

    def up(x):
        a = th.get_value() + off
        x.move_to(P(c, ra, rb, a))
        ff = f.get_value() if hasattr(f, "get_value") else f
        u = (m - a) % 360
        x.set_fill(GOLD if u < (m - ff) else TEAL, 1)
    d.add_updater(up)
    up(d)
    return d


def spin(scene, th, period=14.0):
    th.add_updater(lambda t, dt: t.increment_value(-dt * 360.0 / period))
    scene.add(th)


def mini(center, f, ra=1.7, rb=0.95, gw=8, tw=8, go=1.0, to=1.0):
    gold = arc(center, ra, rb, M, f, GOLD, gw).set_stroke(opacity=go)
    teal = arc(center, ra, rb, f, M - 360, TEAL, tw).set_stroke(opacity=to)
    return VGroup(gold, teal, gate_small(P(center, ra, rb, M)), gate_small(P(center, ra, rb, f)))


MINI_C = np.array([-4.9, 2.5, 0.0])
F_MOSS = -235.0
F_FERN = -65.0
F_HUMAN = -25.0
F_ALGA = -305.0


# ---------------------------------------------------------------- plant drawings
def leaf(pos, ang, length, color, op=0.45):
    e = Ellipse(width=length, height=length * 0.34, stroke_color=color, stroke_width=2, fill_color=color,
                fill_opacity=op)
    e.rotate(ang).move_to(pos)
    return e


def shoot(x, top, base=-2.9, color=GOLD):
    stem = Line([x, base, 0], [x, top, 0], stroke_color=color, stroke_width=6)
    g = VGroup(stem)
    n = int((top - base) / 0.3)
    for i in range(n):
        y = base + 0.25 + i * 0.3
        side = 1 if i % 2 == 0 else -1
        g.add(leaf([x + side * 0.3, y + 0.1, 0], side * 0.6, 0.62, color))
    g.add(Dot([x, top, 0], radius=0.09, color=color))
    return g


MOSS_X = [(-0.6, 0.5), (1.9, 1.0), (4.3, 0.4)]


def moss_shoots():
    g = VGroup(*[shoot(x, t) for x, t in MOSS_X])
    return g


def film_path(dx=0.0):
    pts = [(-1.4, .55), (-0.6, .72), (0.6, .8), (1.9, 1.22), (3.1, .8), (4.3, .62), (5.2, .5)]
    m = VMobject()
    m.set_points_smoothly([np.array([x + dx, y, 0]) for x, y in pts])
    return m


def film():
    m = film_path().set_stroke(WATER, 9, opacity=0.85)
    return m


def stalk_capsule(color=TEAL):
    st = Line([1.9, 1.05, 0], [1.9, 2.65, 0], stroke_color=color, stroke_width=6)
    cap = Ellipse(width=0.55, height=0.8, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9)
    cap.move_to([1.9, 3.05, 0])
    return VGroup(st, cap)


def fern_curve(t):
    p0, p1, p2, p3 = (np.array(v, float) for v in [(1.2, -3.0), (1.0, -0.5), (2.2, 1.0), (1.6, 3.2)])
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


def fern(color=TEAL):
    pts = [fern_curve(t) for t in np.linspace(0, 1, 30)]
    rach = VMobject().set_points_smoothly([np.array([p[0], p[1], 0]) for p in pts])
    rach.set_stroke(color, 6)
    g = VGroup(rach)
    cases = VGroup()
    lows = []
    for i, t in enumerate(np.linspace(0.12, 0.96, 12)):
        p = fern_curve(t)
        d = fern_curve(min(1, t + 0.02)) - fern_curve(max(0, t - 0.02))
        tang = np.arctan2(d[1], d[0])
        L = 2.0 * (1 - t) + 0.45
        for side in (1, -1):
            ang = tang + side * (PI / 2 - 0.45)
            ctr = np.array([p[0], p[1], 0]) + np.array([np.cos(ang), np.sin(ang), 0]) * L / 2
            g.add(leaf(ctr, ang, L, color, 0.6))
            if side == -1 and i < 7:
                lows.append(ctr + np.array([0.0, -0.17, 0]))
    for q in lows[:6]:
        cases.add(Dot(q, radius=0.09, color=BROWN))
    return g, cases


def stone_wall(c, w, h):
    g = VGroup()
    base = Rectangle(width=w, height=h, stroke_color="#767D8C", stroke_width=3, fill_color="#4B5160", fill_opacity=1)
    base.move_to(c)
    g.add(base)
    rows = 3
    for r in range(rows + 1):
        y = c[1] - h / 2 + r * h / rows
        g.add(Line([c[0] - w / 2, y, 0], [c[0] + w / 2, y, 0], stroke_color="#767D8C", stroke_width=3))
    for r in range(rows):
        y0 = c[1] - h / 2 + r * h / rows
        off = 0.0 if r % 2 == 0 else 0.9
        x = c[0] - w / 2 + 1.8 + off
        while x < c[0] + w / 2 - 0.2:
            g.add(Line([x, y0, 0], [x, y0 + h / rows, 0], stroke_color="#767D8C", stroke_width=3))
            x += 1.8
    return g


def pine(cx, base):
    trunk = Rectangle(width=0.4, height=1.8, stroke_width=0, fill_color="#8A6240", fill_opacity=1)
    trunk.move_to([cx, base + 0.9, 0])
    g = VGroup(trunk)
    for k, (w, h, yy) in enumerate([(3.6, 1.6, 0.9), (3.0, 1.5, 1.9), (2.4, 1.4, 2.8), (1.7, 1.3, 3.6)]):
        t = Polygon([cx - w / 2, base + yy, 0], [cx + w / 2, base + yy, 0], [cx, base + yy + h, 0],
                    stroke_color=TEAL, stroke_width=3, fill_color="#2E9AA2", fill_opacity=1)
        g.add(t)
    cone = Ellipse(width=0.4, height=0.65, stroke_color=BROWN, stroke_width=3, fill_color=BROWN, fill_opacity=1)
    cone.move_to([cx + 1.55, base + 1.15, 0])
    g.add(cone)
    g.scale(1.25, about_point=np.array([cx, base, 0.0]))
    g.cone = cone
    return g


def heart(width=2.8, color=GOLD, op=0.9):
    s = width / 32.0
    f = ParametricFunction(lambda t: np.array([16 * np.sin(t) ** 3 * s,
                                              (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) * s, 0]),
                           t_range=[0, TAU, 0.05], color=color, stroke_width=4)
    f.set_fill(color, op)
    return f


def pill(txt, color, size=28, pos=ORIGIN):
    lab = T(txt, size, color, weight=BOLD)
    r = RoundedRectangle(corner_radius=0.15, width=lab.width + 0.45, height=lab.height + 0.35, stroke_color=color,
                         stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(r, lab).move_to(pos)


# =================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Plants on Land"
    TITLE = "Two Bodies, One Wheel"


class S01Question(SpokenScene):
    def construct(self):
        wall = stone_wall([-3.4, -2.6, 0], 7.2, 1.9)
        dome = Ellipse(width=6.2, height=2.8, stroke_color=LEAF, stroke_width=4, fill_color=LEAF, fill_opacity=0.4)
        dome.move_to([-3.4, -0.4, 0])
        rng = np.random.RandomState(3)
        shoots = VGroup()
        for i in range(24):
            x = -3.4 - 2.7 + i * 5.4 / 23
            ytop = -0.4 + 1.4 * np.sqrt(max(0.0, 1 - ((x + 3.4) / 3.1) ** 2)) + 0.45 + rng.uniform(0, 0.25)
            ybase = ytop - 0.9
            s = VGroup(Line([x, ybase, 0], [x, ytop, 0], stroke_color=LEAF, stroke_width=5),
                       Dot([x, ytop, 0], radius=0.08, color=LEAF))
            shoots.add(s)
        add_sway(shoots, 0.05, 3.5)
        cush = VGroup(wall, dome, shoots)
        self.play(FadeIn(cush, shift=UP * 0.15), run_time=0.9)
        # zoom on one leafy shoot
        spot = Circle(radius=0.3, stroke_color=WHITE, stroke_width=4).move_to([-2.4, 0.95, 0])
        self.at("moss")
        self.play(Create(spot), run_time=0.5)
        lens = Circle(radius=1.5, stroke_color=WHITE, stroke_width=5, fill_color=BG, fill_opacity=1).move_to([3.9, 1.5, 0])
        lf = leaf([3.9, 1.5, 0], 1.2, 2.2, LEAF, 0.35)
        cell = Circle(radius=0.62, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.9).move_to([3.9, 1.5, 0])
        self.at("haploid")
        self.play(ReplacementTransform(spot, lens), run_time=0.6)
        self.play(FadeIn(lf), FadeIn(cell, scale=0.5), run_time=0.5)
        glow = Circle(radius=0.85, stroke_color=GOLD, stroke_width=3).move_to(cell)
        lab_n = T("n: one set", 32, GOLD, weight=BOLD).move_to([3.9, -0.45, 0])
        self.play(Create(glow), FadeIn(lab_n, shift=UP * 0.1), run_time=0.4)
        breathe(glow, 0.08, 2.0)
        self.at("human egg")
        eg = Circle(radius=0.62, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.9).move_to([2.6, -2.1, 0])
        zona = Circle(radius=0.85, stroke_color=GOLD, stroke_width=3).move_to(eg)
        eg_l = T("human egg: n", 30, GOLD).move_to([5.0, -2.1, 0])
        self.play(FadeIn(eg, scale=0.5), Create(zona), run_time=0.7)
        self.play(FadeIn(eg_l, shift=LEFT * 0.1), run_time=0.4)
        breathe(zona, 0.06, 2.4, 1.0)
        self.at("so where is")
        q = T("?", 110, YELLOW, weight=BOLD).move_to([-3.4, 2.75, 0])
        ql = T("where is 2n?", 38, TEAL, weight=BOLD).move_to([-3.4, -2.6, 0])
        self.play(FadeIn(q, scale=1.6), run_time=0.6)
        self.play(FadeIn(ql, shift=UP * 0.1), run_time=0.5)
        bob(q, 0.08, 1.6)
        self.finish()


class S02Terms(SpokenScene):
    def construct(self):
        def bar(x, y):
            return RoundedRectangle(corner_radius=0.1, width=0.24, height=1.2, stroke_width=0, fill_color=WHITE,
                                    fill_opacity=0.95).move_to([x, y, 0])
        d1 = Circle(radius=1.6, stroke_color=WHITE, stroke_width=5, fill_opacity=0).move_to([-3.4, 0.7, 0])
        d2 = Circle(radius=1.6, stroke_color=WHITE, stroke_width=5, fill_opacity=0).move_to([3.4, 0.7, 0])
        self.at("a haploid cell")
        self.play(Create(d1), run_time=0.8)
        b1 = bar(-3.4, 0.7)
        self.at("one set")
        self.play(GrowFromCenter(b1), run_time=0.7)
        l1 = T("haploid = n", 38, TEXT, weight=BOLD).move_to([-3.4, -1.6, 0])
        self.at("we write that as")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.5)
        self.at("gold")
        self.play(d1.animate.set_fill(GOLD, 0.85).set_stroke(GOLD), l1.animate.set_color(GOLD), run_time=0.8)
        breathe(d1, 0.025, 3.0)
        self.at("a diploid cell")
        self.play(Create(d2), run_time=0.8)
        b2a, b2b = bar(3.1, 0.7), bar(3.7, 0.7)
        self.at("two sets")
        self.play(GrowFromCenter(b2a), run_time=0.5)
        self.play(GrowFromCenter(b2b), run_time=0.5)
        l2 = T("diploid = 2n", 38, TEXT, weight=BOLD).move_to([3.4, -1.6, 0])
        self.at("written 2n")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.5)
        self.at("teal")
        self.play(d2.animate.set_fill(TEAL, 0.85).set_stroke(TEAL), l2.animate.set_color(TEAL), run_time=0.8)
        breathe(d2, 0.025, 3.0, 1.5)
        lg = legend()
        self.play(FadeIn(lg, shift=UP * 0.3), run_time=0.7)
        self.finish()


class S03Gates(SpokenScene):
    def construct(self):
        self.add(legend())
        Y = 0.7
        # opening: a count that changes
        d = VGroup(dotc(GOLD, 0.9), T("n", 48, DARK, weight=BOLD)).move_to([0, Y, 0])
        self.play(FadeIn(d, scale=0.6), run_time=0.6)
        bob(d, 0.1, 2.0)
        self.at("only two kinds")
        d2 = VGroup(dotc(TEAL, 0.9), T("2n", 48, DARK, weight=BOLD)).move_to(d)
        self.play(Transform(d, d2), run_time=0.7)
        self.at("change that count")
        d3 = VGroup(dotc(GOLD, 0.9), T("n", 48, DARK, weight=BOLD)).move_to(d)
        self.play(Transform(d, d3), run_time=0.7)
        d.clear_updaters()
        self.at("meiosis halves it", lead=1.2)
        gm = gate_m([-4.7, Y, 0], r=1.1, size=30)
        gm[1].set_color(TEXT)
        t0 = dotc(TEAL, 0.4, [-6.3, Y, 0])
        self.play(FadeOut(d, scale=0.5), FadeIn(gm, shift=DOWN * 0.4), FadeIn(t0, scale=0.5), run_time=0.7)
        self.at("meiosis")
        self.play(t0.animate.move_to([-4.7, Y, 0]), run_time=0.7)
        outs = VGroup(*[dotc(GOLD, 0.26, [-4.7, Y, 0]) for _ in range(4)])
        self.remove(t0)
        self.add(outs)
        tg = [[-3.1, Y + 0.4, 0], [-2.5, Y + 0.4, 0], [-3.1, Y - 0.4, 0], [-2.5, Y - 0.4, 0]]
        l1 = T("meiosis halves", 34, TEXT, weight=BOLD).move_to([-4.2, -1.1, 0])
        self.play(*[o.animate.move_to(p) for o, p in zip(outs, tg)], FadeIn(l1, shift=UP * 0.1), run_time=0.8)
        bob(outs, 0.04, 2.0)
        # fusion gate
        gf = gate_f([0.2, Y, 0], r=1.1)
        gf[1].scale(1.3)
        self.at("every fusion", lead=1.0)
        self.play(FadeIn(gf, shift=DOWN * 0.4), run_time=0.5)
        g1 = dotc(GOLD, 0.3, [-1.9, Y + 0.9, 0])
        g2 = dotc(GOLD, 0.3, [-1.9, Y - 0.9, 0])
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.3)
        self.at("adds the sets")
        self.play(g1.animate.move_to([0.2, Y, 0]), g2.animate.move_to([0.2, Y, 0]), run_time=0.8)
        z = dotc(TEAL, 0.45, [0.2, Y, 0])
        self.remove(g1, g2)
        self.add(z)
        l2 = T("fusion adds", 34, TEXT, weight=BOLD).move_to([0.2, -1.1, 0])
        self.play(z.animate.move_to([2.0, Y, 0]), FadeIn(l2, shift=UP * 0.1), run_time=0.7)
        bob(z, 0.05, 2.0)
        # mitosis copy arrow
        self.at("mitosis which", lead=1.0)
        ca = copy_arrow([4.8, Y, 0], r=0.9, w=8)
        self.play(FadeIn(ca, scale=0.7), run_time=0.5)
        gd = dotc(GOLD, 0.3, [3.9, Y, 0])
        self.play(FadeIn(gd), run_time=0.3)
        self.at("copies a cell")
        lp = Arc(radius=0.9, start_angle=PI, angle=-2 * PI).move_to([4.8, Y, 0])
        self.play(MoveAlongPath(gd, lp), run_time=1.6)
        gd2 = dotc(GOLD, 0.3, gd.get_center())
        self.add(gd2)
        self.play(gd.animate.move_to([6.1, Y + 0.45, 0]), gd2.animate.move_to([6.1, Y - 0.45, 0]), run_time=0.6)
        l3 = T("mitosis copies", 34, TEXT, weight=BOLD).move_to([4.7, -1.1, 0])
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=0.4)
        bob(gd, 0.05, 2.0)
        bob(gd2, 0.05, 2.0, 1.0)
        self.finish()


def base_wheel(top="dim", gm=True, gf=False, tipsOn=True):
    ring, tp = ring_world()
    g = VGroup(ring)
    if tipsOn:
        g.add(tp)
    top_box = body_box("sporophyte (spore plant)", TEAL, 28, P(C0, RA, RB, 90), dim=(top == "dim"))
    if top is not None:
        g.add(top_box)
    gmm = gate_m(P(C0, RA, RB, M)) if gm else None
    if gm:
        g.add(gmm)
    gff = gate_f(P(C0, RA, RB, F)) if gf else None
    if gf:
        g.add(gff)
    return g, ring, top_box, gmm, gff


class S04Wheel(SpokenScene):
    def construct(self):
        self.add(legend())
        ring, tp = ring_world()
        pn = panel(C0, RA, RB)
        self.at("now draw a land plant's life as a wheel")
        self.play(Create(ring), FadeIn(tp), FadeIn(pn), run_time=3.0, rate_func=linear)
        self.at("a diploid body")
        top_box = body_box("sporophyte (spore plant)", TEAL, 28, P(C0, RA, RB, 90))
        self.play(FadeIn(top_box, scale=0.9), run_time=0.8)
        tok = token("2n", P(C0, RA, RB, 90))
        self.at("makes spores", lead=0.9)
        gate = gate_m(P(C0, RA, RB, M))
        self.play(FadeIn(tok, scale=0.6), FadeIn(gate, scale=0.7), run_time=0.5)
        self.play(MoveAlongPath(tok, arc(C0, RA, RB, 90, M, RING, 1)), run_time=1.2, rate_func=linear)
        self.at("meiosis")
        tg = token("n", gate.get_center())
        self.play(Transform(tok, tg), run_time=0.4)
        dots = VGroup(*[dotc(GOLD, 0.2, gate.get_center()) for _ in range(3)])
        self.add(dots)
        self.play(*[d.animate.move_to(P(C0, RA, RB, a)) for d, a in zip(dots, [4, -10, -24])], run_time=1.0)
        self.play(tok.animate.move_to(P(C0, RA, RB, -38)), run_time=0.8)
        self.at("each spore")
        lab = T("spores, single cells", 30, GOLD, weight=BOLD).move_to([2.4, -0.55, 0])
        self.play(FadeIn(lab, shift=LEFT * 0.2), run_time=0.5)
        for i, d in enumerate(dots):
            bob(d, 0.05, 2.2, i * 0.7)
        bob(tok, 0.05, 2.2, 2.0)
        self.finish()


class S05Gametophyte(SpokenScene):
    def construct(self):
        self.add(legend())
        g, ring, top_box, gmm, _ = base_wheel("dim")
        self.add(panel(C0, RA, RB), g)
        sp = VGroup(*[dotc(GOLD, 0.2, P(C0, RA, RB, a)) for a in [4, -10, -24]])
        self.add(sp)
        tok = token("n", P(C0, RA, RB, -38))
        self.add(tok)
        self.at("a spore divides")
        self.play(MoveAlongPath(tok, arc(C0, RA, RB, -38, -90, RING, 1)), run_time=1.6, rate_func=linear)
        sp.add_updater(lambda m: None)
        self.at("mitosis")
        ca = copy_arrow([0, -1.45, 0], r=0.38)
        twin = dotc(GOLD, 0.34, tok.get_center())
        self.add(twin)
        self.play(FadeIn(ca, scale=0.6), tok.animate.shift(LEFT * 0.5), twin.animate.shift(RIGHT * 0.5), run_time=0.6)
        self.at("a second body", lead=0.4)
        box = RoundedRectangle(corner_radius=0.18, width=5.6, height=0.8, stroke_color=GOLD, stroke_width=4,
                               fill_color=GOLD, fill_opacity=0.3).move_to(P(C0, RA, RB, -90))
        bg = RoundedRectangle(corner_radius=0.18, width=5.6, height=0.8, stroke_width=0, fill_color=BG,
                              fill_opacity=1).move_to(box)
        self.play(FadeIn(bg), GrowFromCenter(box), FadeOut(twin), FadeOut(tok), run_time=0.9)
        self.at("the gametophyte")
        lab = T("gametophyte (gamete plant)", 28, TEXT).move_to(box)
        self.play(FadeIn(lab), run_time=0.5)
        tok2 = token("n", P(C0, RA, RB, -125))
        self.at("it is already haploid")
        self.play(FadeIn(tok2, scale=0.5), run_time=0.3)
        self.play(MoveAlongPath(tok2, arc(C0, RA, RB, -125, -150, RING, 1)), run_time=1.3, rate_func=linear)
        self.at("so it makes eggs")
        eg = egg([2.0, -1.4, 0])
        self.play(FadeIn(eg, scale=0.4, shift=UP * 0.5), run_time=0.6)
        el = T("egg", 28, GOLD, weight=BOLD).next_to(eg, UP, buff=0.15)
        self.play(FadeIn(el), run_time=0.3)
        self.at("sperm", lead=0.3)
        sp1 = sperm([-2.0, -1.4, 0])
        self.play(FadeIn(sp1, scale=0.4, shift=UP * 0.5), run_time=0.6)
        sl = T("sperm", 28, GOLD, weight=BOLD).next_to(sp1, UP, buff=0.15)
        self.play(FadeIn(sl), run_time=0.3)
        self.at("by mitosis", nth=1)
        ml = T("by mitosis", 30, TEXT, weight=BOLD).move_to([0, -0.7, 0])
        self.play(FadeIn(ml, shift=DOWN * 0.1), Indicate(ca, color=WHITE, scale_factor=1.25), run_time=0.8)
        bob(eg, 0.05, 2.0)
        bob(sp1, 0.05, 2.0, 1.0)
        self.finish()


class S06Fusion(SpokenScene):
    def construct(self):
        self.add(legend())
        g, ring, top_box, gmm, gff = base_wheel("dim", gf=True)
        self.add(panel(C0, RA, RB), g)
        box = body_box("gametophyte (gamete plant)", GOLD, 28, P(C0, RA, RB, -90))
        box[1].set_fill(GOLD, 0.3)
        self.add(box)
        eg = egg([2.0, -1.4, 0])
        sp1 = sperm([-2.0, -1.4, 0])
        self.add(eg, sp1)
        tok = token("n", P(C0, RA, RB, -150))
        self.add(tok)
        gp = gff.get_center()
        self.at("then sperm and egg fuse")
        self.play(eg.animate.move_to(gp), sp1.animate.move_to(gp), MoveAlongPath(tok, arc(C0, RA, RB, -150, -200, RING, 1)),
                  run_time=2.2)
        zy = dotc(TEAL, 0.38, gp)
        self.remove(eg, sp1)
        self.add(zy)
        tz = token("2n", gp)
        self.play(Transform(tok, tz), zy.animate.move_to([-2.6, 1.5, 0]), run_time=0.7)
        self.at("the zygote")
        zl = T("zygote: 2n", 32, TEAL, weight=BOLD).move_to([-0.4, 1.5, 0])
        self.play(FadeIn(zl, shift=LEFT * 0.2), run_time=0.5)
        bob(zy, 0.06, 2.0)
        self.at("two sets again")
        self.play(Indicate(zy, color=TEAL, scale_factor=1.3), run_time=0.8)
        self.at("it divides by mitosis")
        ca1 = copy_arrow(P(C0, RA, RB, 148), r=0.28, w=5)
        ca2 = copy_arrow(P(C0, RA, RB, 130), r=0.28, w=5)
        for ca in (ca1, ca2):
            ca.add_to_back(Circle(radius=0.36, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(ca))
        self.play(FadeOut(zy), FadeOut(zl), FadeIn(ca1), FadeIn(ca2), run_time=0.5)
        self.play(MoveAlongPath(tok, arc(C0, RA, RB, 160, 92, RING, 1)), run_time=1.6, rate_func=linear)
        self.at("a new sporophyte")
        self.play(top_box[1].animate.set_fill(TEAL, 0.3).set_stroke(opacity=1), top_box[2].animate.set_opacity(1),
                  Indicate(top_box, color=TEAL, scale_factor=1.06), run_time=1.0)
        bob(tok, 0.05, 2.0)
        self.finish()


class S07Arcs(SpokenScene):
    def construct(self):
        lg = legend()
        self.add(lg)
        ring, tp = ring_world()
        gm = gate_m(P(C0, RA, RB, M))
        gf = gate_f(P(C0, RA, RB, F))
        self.add(panel(C0, RA, RB), ring, tp, gm, gf)
        th = ValueTracker(90.0)
        tk_g, tk_t = token("n"), token("2n")
        tok = VGroup(tk_g, tk_t)

        def up(x):
            a = th.get_value()
            x.move_to(P(C0, RA, RB, a))
            u = (M - a) % 360
            gold = u < (M - F)
            tk_g.set_opacity(1 if gold else 0)
            tk_t.set_opacity(0 if gold else 1)
            for m in tk_g:
                m.set_opacity(1 if gold else 0)
            for m in tk_t:
                m.set_opacity(0 if gold else 1)
        tok.add_updater(up)
        up(tok)
        self.add(tok)
        self.play(th.animate.set_value(M), pls(gm, 1.2), run_time=0.8, rate_func=linear)
        self.at("two arcs")
        self.play(pls(gf, 1.2), run_time=0.8)
        self.at("from meiosis to fertilization")
        ga = arc(C0, RA, RB, M, F, GOLD, 10)
        fl = T("fertilization", 28, TEXT, weight=BOLD).move_to([-2.9, -0.3, 0])
        self.play(Create(ga), th.animate.set_value(F), FadeIn(fl), run_time=2.0, rate_func=linear)
        self.at("gold")
        gn = T("n", 64, GOLD, weight=BOLD).move_to([0, -1.2, 0])
        self.play(FadeIn(gn, scale=1.5), run_time=0.6)
        self.at("from fertilization to the next meiosis")
        ta = arc(C0, RA, RB, F + 360, M, TEAL, 10)
        self.play(Create(ta), th.animate.set_value(M - 360), run_time=2.0, rate_func=linear)
        self.at("teal")
        tn = T("2n", 64, TEAL, weight=BOLD).move_to([0, 1.4, 0])
        self.play(FadeIn(tn, scale=1.5), run_time=0.6)
        th.set_value(M)
        spin(self, th, 12.0)
        self.at("other fusions")
        self.play(Indicate(lg.coral, color=CORAL, scale_factor=1.3), run_time=1.0)
        self.at("as the next film")
        self.play(pls(gm, 1.2), pls(gf, 1.2), run_time=1.0)
        self.finish()


def full_wheel():
    ga = arc(C0, RA, RB, M, F, GOLD, 10)
    ta = arc(C0, RA, RB, F + 360, M, TEAL, 10)
    gm = gate_m(P(C0, RA, RB, M))
    gf = gate_f(P(C0, RA, RB, F))
    return VGroup(ga, ta, gm[0], gf[0]), VGroup(gm[1], gf[1])


S_INSET = 0.38


def start_inset(scene, f):
    """Full wheel at the s07 state shrinks to the corner, carried into the later scenes."""
    body, labs = full_wheel()
    scene.add(body, labs)
    return body, labs


class S08Moss(SpokenScene):
    def construct(self):
        self.add(legend())
        pn = panel(C0, RA, RB)
        self.add(pn)
        body, labs = start_inset(self, F)
        th = ValueTracker(M)
        rd = rider(C0, RA, RB, M, F, th, r=0.3)
        spin(self, th, 10.0)
        self.add(rd)
        shoots = moss_shoots()
        self.at("the gold arc swells")
        self.remove(rd)
        self.play(FadeOut(labs), FadeOut(pn), body.animate.scale(S_INSET).move_to(MINI_C),
                  LaggedStart(*[GrowFromPoint(s, s.get_bottom()) for s in shoots], lag_ratio=0.3), run_time=2.4)
        self.remove(body)
        inset = mini(MINI_C, F, RA * S_INSET, RB * S_INSET)
        self.add(inset)
        add_sway(shoots, 0.03, 4.0)
        self.at("so that shoot is the gametophyte")
        lab = T("gametophyte, n", 34, GOLD, weight=BOLD).move_to([-4.6, -0.9, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        egg_ = egg([1.9, 1.25, 0], 0.26)
        self.play(FadeIn(egg_, scale=0.4), run_time=0.5)
        breathe(egg_, 0.12, 1.6)
        # rain
        rain = VGroup()
        rng = np.random.RandomState(7)
        for i in range(10):
            ln = Line([0, 0, 0], [-0.05, -0.35, 0], stroke_color=WATER, stroke_width=4)
            ln.move_to([rng.uniform(-1.5, 5.2), rng.uniform(1.6, 3.7), 0])
            ln.v = rng.uniform(1.6, 2.6)

            def fall(m, dt):
                m.shift(DOWN * m.v * dt)
                if m.get_y() < 1.5:
                    m.shift(UP * 2.3)
            ln.add_updater(fall)
            rain.add(ln)
        self.at("a sperm swims", lead=0.9)
        self.play(FadeIn(rain), run_time=0.4)
        fm = film()
        self.play(Create(fm), run_time=1.0)
        sp = sperm([-1.4, 0.75, 0])
        self.add(sp)
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in [(-1.4, .78, 0), (-0.6, .95, 0), (0.6, 1.05, 0), (1.55, 1.3, 0)]])
        self.at("film of rain", lead=0.5)
        self.play(MoveAlongPath(sp, path), run_time=2.6, rate_func=linear)
        self.play(pls(egg_, 1.6), run_time=0.6)
        self.finish()


def moss_state(scene, with_rain=False):
    inset = mini(MINI_C, F, RA * S_INSET, RB * S_INSET)
    shoots = moss_shoots()
    fm = film()
    return inset, shoots, fm


class S09Answer(SpokenScene):
    def construct(self):
        self.add(legend())
        inset, shoots, fm = moss_state(self)
        egg_ = egg([1.9, 1.25, 0], 0.26)
        lab = T("gametophyte, n", 34, GOLD, weight=BOLD).move_to([-4.6, -0.9, 0])
        sp = sperm([1.65, 1.3, 0])
        self.add(inset, shoots, fm, egg_, lab, sp)
        add_sway(shoots, 0.03, 4.0)
        breathe(egg_, 0.12, 1.6)
        self.wait(0.2)
        # + gate fires at the shoot tip
        pg = gate_m([1.9, 1.45, 0], r=0.5)
        pg.become(gate_f([1.9, 1.45, 0], r=0.5))
        self.at("the teal arc")
        self.play(FadeIn(pg, scale=0.5), FadeOut(sp), FadeOut(fm), run_time=0.3)
        self.play(FadeOut(pg, scale=1.5), egg_.animate.set_fill(TEAL, 1).set_stroke(TEAL), FadeOut(lab),
                  inset[1].animate.set_stroke(width=12), inset[0].animate.set_stroke(width=4, opacity=0.5), run_time=0.4)
        self.at("shrinks to a thin stalk")
        sc = stalk_capsule()
        self.remove(egg_)
        self.play(Create(sc[0]), run_time=1.2, rate_func=linear)
        self.at("capsule")
        self.play(GrowFromCenter(sc[1]), run_time=0.7)
        l1 = T("sporophyte, 2n", 34, TEAL, weight=BOLD).move_to([4.7, 2.0, 0])
        self.play(FadeIn(l1, shift=LEFT * 0.2), run_time=0.5)
        self.at("that is the diploid moss")
        q = T("?", 100, YELLOW, weight=BOLD).move_to([4.0, 0.2, 0])
        l2 = T("the diploid moss", 32, TEXT).next_to(l1, DOWN, buff=0.15)
        self.play(FadeIn(l2), FadeIn(q, scale=1.4), run_time=0.5)
        self.play(q.animate.move_to([2.7, 2.95, 0]).scale(0.7), run_time=0.8)
        tick = VMobject(stroke_color="#6BD49A", stroke_width=10)
        tick.set_points_as_corners([[2.45, 2.95, 0], [2.65, 2.7, 0], [3.05, 3.25, 0]])
        self.play(ReplacementTransform(q, tick), run_time=0.5)
        self.at("myosis in the capsule")
        gm = gate_m([0.6, 2.95, 0], r=0.72)
        self.play(FadeIn(gm, scale=0.6), run_time=0.5)
        spores = VGroup(*[dotc(GOLD, 0.14, [1.5, 2.95, 0]) for _ in range(5)])
        self.add(spores)
        self.play(*[s.animate.move_to([-0.6 - i * 0.55, 2.7 + 0.35 * np.sin(i * 1.7), 0]) for i, s in enumerate(spores)],
                  run_time=1.6)
        for i, s in enumerate(spores):
            bob(s, 0.06, 2.0, i * 0.5)
        self.finish()


class S10Fern(SpokenScene):
    def construct(self):
        self.add(legend())
        inset = mini(MINI_C, F, RA * S_INSET, RB * S_INSET, 4, 12, 0.5, 1)
        shoots = moss_shoots()
        sc = stalk_capsule()
        old = VGroup(shoots, sc)
        self.add(inset, old)
        add_sway(shoots, 0.03, 4.0)
        fr, cases = fern()
        self.at("now a fern", lead=0.0)
        self.play(old.animate.shift(LEFT * 9).set_opacity(0), Create(fr[0]), run_time=1.0)
        self.remove(old)
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in fr[1:]], lag_ratio=0.05), run_time=1.3)
        self.at("here the arcs swap sizes")
        new = mini(MINI_C, F_FERN, RA * S_INSET, RB * S_INSET, 12, 12, 1, 1)
        self.play(Transform(inset, new), run_time=1.5)
        self.at("the big frond is the sporophyte")
        lab = VGroup(T("frond =", 34, TEXT), T("sporophyte, 2n", 34, TEAL, weight=BOLD)).arrange(DOWN, buff=0.1)
        lab.move_to([-4.3, -0.2, 0])
        self.play(FadeIn(lab, shift=RIGHT * 0.2), run_time=0.6)
        self.play(Indicate(fr[1:], color=TEAL, scale_factor=1.03), run_time=0.9)
        self.at("spore cases under it")
        cl = T("spore cases", 30, BROWN, weight=BOLD).move_to([5.0, -2.2, 0])
        self.play(FadeIn(cases, scale=1.8), FadeIn(cl), run_time=0.6)
        self.at("make spores by")
        gate = gate_m([5.0, -0.3, 0], r=0.72)
        self.play(FadeIn(gate, scale=0.6), run_time=0.5)
        sp = VGroup(*[dotc(GOLD, 0.15, cases[i].get_center()) for i in range(3)])
        self.add(sp)
        self.play(*[s.animate.move_to(gate.get_center()) for s in sp], run_time=0.9)
        self.at("meiosis")
        self.play(*[s.animate.move_to([5.2 + 0.25 * i, 0.9 + 0.5 * i, 0]) for i, s in enumerate(sp)], run_time=1.0)
        for i, s in enumerate(sp):
            bob(s, 0.07, 2.0, i * 0.6)
        self.finish()


def predict_world(show_labels=True):
    soil = Rectangle(width=14.2, height=1.6, stroke_width=0, fill_color=SOIL, fill_opacity=0.85).move_to([0, -2.2, 0])
    soil.set_z_index(-1)
    sp = Circle(radius=0.75, stroke_color=WHITE, stroke_width=5, fill_opacity=0).move_to([-2.9, -0.6, 0])
    pl = Ellipse(width=3.2, height=1.2, stroke_color=WHITE, stroke_width=5, fill_opacity=0).move_to([2.4, -0.8, 0])
    return soil, sp, pl


class S11Predict(SpokenScene):
    def construct(self):
        self.add(legend())
        soil, sp, pl = predict_world()
        self.add(soil)
        fr, cases = fern()
        mini_fern = VGroup(fr, cases).scale(0.34).move_to([-2.9, 2.75, 0])
        self.add(mini_fern)
        spore = sp.copy().scale(0.3).move_to([-2.9, 2.2, 0])
        self.add(spore)
        self.play(spore.animate.scale(1 / 0.3).move_to(sp.get_center()), run_time=1.1)
        small = Ellipse(width=0.7, height=0.3, stroke_color=WHITE, stroke_width=5, fill_opacity=0).move_to([-0.6, -1.2, 0])
        self.add(small)
        self.at("into a small plant")
        self.play(Transform(small, pl), run_time=1.6)
        bs = RoundedRectangle(corner_radius=0.15, width=3.0, height=0.8, stroke_color=YELLOW, stroke_width=4, fill_opacity=0)
        bl = RoundedRectangle(corner_radius=0.15, width=3.8, height=0.8, stroke_color=YELLOW, stroke_width=4, fill_opacity=0)
        ts = T("spore ?", 32, YELLOW, weight=BOLD)
        tl = T("little plant ?", 32, YELLOW, weight=BOLD)
        b1 = VGroup(bs, ts).move_to([-2.9, 1.45, 0])
        b2 = VGroup(bl, tl).move_to([2.4, 1.45, 0])
        self.at("gold or teal")
        q = T("gold or teal?", 42, TEXT, weight=BOLD).move_to([0, 3.4, 0])
        sg = dotc(GOLD, 0.36, [-0.9, 2.6, 0])
        st = dotc(TEAL, 0.36, [0.9, 2.6, 0])
        self.play(FadeIn(q, shift=DOWN * 0.1), FadeIn(sg, scale=0.5), FadeIn(st, scale=0.5), FadeOut(mini_fern), run_time=0.6)
        bob(sg, 0.07, 1.8)
        bob(st, 0.07, 1.8, 0.9)
        self.at("the spore")
        self.play(FadeIn(b1), run_time=0.4)
        self.at("that little plant")
        self.play(FadeIn(b2), run_time=0.4)
        breathe(b1, 0.03, 1.8)
        breathe(b2, 0.03, 1.8, 0.9)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        self.add(legend())
        soil, sp, pl = predict_world()
        self.add(soil, sp, pl)
        bs = RoundedRectangle(corner_radius=0.15, width=3.0, height=0.8, stroke_color=YELLOW, stroke_width=4, fill_opacity=0)
        bl = RoundedRectangle(corner_radius=0.15, width=3.8, height=0.8, stroke_color=YELLOW, stroke_width=4, fill_opacity=0)
        b1 = VGroup(bs, T("spore ?", 32, YELLOW, weight=BOLD)).move_to([-2.9, 1.65, 0])
        b2 = VGroup(bl, T("little plant ?", 32, YELLOW, weight=BOLD)).move_to([2.4, 1.65, 0])
        q = T("gold or teal?", 42, TEXT, weight=BOLD).move_to([0, 3.4, 0])
        sg = dotc(GOLD, 0.36, [-0.9, 2.6, 0])
        st = dotc(TEAL, 0.36, [0.9, 2.6, 0])
        self.add(b1, b2, q, sg, st)
        bob(sg, 0.07, 1.8)
        bob(st, 0.07, 1.8, 0.9)
        breathe(b1, 0.03, 1.8)
        breathe(b2, 0.03, 1.8, 0.9)
        tr = ValueTracker(1.0)
        bar = Rectangle(width=10, height=0.12, stroke_width=0, fill_color=GREY, fill_opacity=0.9)
        bar.add_updater(lambda b: b.become(Rectangle(width=max(0.01, 10 * tr.get_value()), height=0.12, stroke_width=0,
                                                     fill_color=GREY, fill_opacity=0.9).move_to([-5 + 5 * tr.get_value(), -3.0, 0])))
        self.add(bar)
        self.play(tr.animate.set_value(0.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        self.add(legend())
        soil, sp, pl = predict_world()
        self.add(soil, sp, pl)
        b1 = VGroup(RoundedRectangle(corner_radius=0.15, width=3.0, height=0.8, stroke_color=YELLOW, stroke_width=4,
                                     fill_opacity=0), T("spore ?", 32, YELLOW, weight=BOLD)).move_to([-2.9, 1.65, 0])
        b2 = VGroup(RoundedRectangle(corner_radius=0.15, width=3.8, height=0.8, stroke_color=YELLOW, stroke_width=4,
                                     fill_opacity=0), T("little plant ?", 32, YELLOW, weight=BOLD)).move_to([2.4, 1.65, 0])
        self.add(b1, b2)
        self.wait(0.1)
        self.at("both gold")
        n1 = pill("spore: n", GOLD, 32, [-2.9, 1.65, 0])
        n2 = pill("little plant: n", GOLD, 32, [2.4, 1.65, 0])
        self.play(sp.animate.set_fill(GOLD, 0.9).set_stroke(GOLD), pl.animate.set_fill(GOLD, 0.9).set_stroke(GOLD),
                  ReplacementTransform(b1, n1), ReplacementTransform(b2, n2), run_time=1.0)
        # the small wheel flashes with both on the gold arc
        c = np.array([5.2, 3.0, 0])
        w = mini(c, F, 1.3, 0.7, 5, 5, 1, 0.5)
        self.at("they come after the meiosis gate")
        self.play(FadeIn(w), run_time=0.5)
        d1, d2 = dotc(GOLD, 0.12, P(c, 1.3, 0.7, -35)), dotc(GOLD, 0.12, P(c, 1.3, 0.7, -85))
        self.play(FadeIn(d1), FadeIn(d2), w[0].animate.set_stroke(width=12), pls(w[2], 1.6),
                  run_time=0.9)
        self.at("and no fusion has happened yet")
        self.play(pls(w[3], 1.6), w[0].animate.set_stroke(width=14), run_time=0.9)
        self.play(w[0].animate.set_stroke(width=8), run_time=0.5)
        self.at("the little plant is")
        hh = heart(2.3, GOLD, 0.9).move_to([2.4, -0.3, 0])
        self.at("a flat")
        self.play(Transform(pl, hh), run_time=1.4)
        self.at("heart shaped", lead=0.3)
        n3 = pill("prothallus = gametophyte, n", GOLD, 30, [2.4, 1.65, 0])
        self.play(ReplacementTransform(n2, n3), run_time=0.6)
        self.at("it lives on its own", lead=1.0)
        fm = ParametricFunction(lambda s: np.array([-0.6 + 6.0 * s, -1.2 + 0.07 * np.sin(s * 18), 0]), t_range=[0, 1, 0.01],
                                color=WATER, stroke_width=9)
        fm.set_stroke(opacity=0.85)
        self.play(Create(fm), run_time=0.8)
        eg = egg([2.4, 0.3, 0], 0.22)
        self.add(eg)
        s = sperm([-0.3, -0.95, 0])
        self.add(s)
        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in [(-0.3, -1.0, 0), (0.8, -0.95, 0), (1.7, -0.5, 0), (2.2, 0.1, 0)]])
        self.play(MoveAlongPath(s, path), run_time=2.2, rate_func=linear)
        self.finish()


def silhouette(color=TEAL):
    head = Circle(radius=0.5, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.6).move_to([0, 1.3, 0])
    body = RoundedRectangle(corner_radius=0.5, width=1.5, height=2.2, stroke_color=color, stroke_width=4, fill_color=color,
                            fill_opacity=0.6).move_to([0, -0.3, 0])
    return VGroup(head, body)


HC = np.array([0.9, 0.1, 0.0])
HRA, HRB = 4.0, 2.7


class S14Contrast(SpokenScene):
    def construct(self):
        self.add(legend())
        ftr = ValueTracker(F)
        gold = always_redraw(lambda: arc(HC, HRA, HRB, M, ftr.get_value(), GOLD, 10))
        teal = always_redraw(lambda: arc(HC, HRA, HRB, ftr.get_value(), M - 360, TEAL, 10))
        gm = always_redraw(lambda: gate_m(P(HC, HRA, HRB, M), r=0.62, size=22))
        gf = always_redraw(lambda: gate_f(P(HC, HRA, HRB, ftr.get_value()), r=0.5))
        hum = silhouette().move_to([-5.1, 0.3, 0])
        pn = panel(HC, HRA, HRB)
        self.add(pn)
        self.at("now compare")
        self.play(FadeIn(hum, shift=RIGHT * 0.3), Create(gold), Create(teal), FadeIn(gm), FadeIn(gf), run_time=1.6)
        th = ValueTracker(90.0)
        rd = rider(HC, HRA, HRB, M, ftr, th)
        spin(self, th, 12.0)
        self.add(rd)
        fern_inset = mini([5.6, 2.9, 0], F_FERN, 1.0, 0.6, 5, 5)
        fl = T("fern", 24, TEXT).move_to([5.6, 2.0, 0])
        self.at("in humans")
        hl = VGroup(T("human:", 32, TEXT, weight=BOLD), T("no haploid body", 30, TEAL, weight=BOLD)).arrange(DOWN, buff=0.1)
        hl.move_to([-4.9, -2.3, 0])
        self.play(FadeIn(hl, shift=UP * 0.1), run_time=0.5)
        self.at("meiosis makes eggs")
        self.play(pls(gm, 1.2), run_time=0.9)
        self.at("directly")
        self.play(FadeIn(fern_inset), FadeIn(fl), run_time=0.7)
        self.at("the gold arc shrinks")
        self.play(ftr.animate.set_value(F_HUMAN), run_time=1.6)
        e1 = egg(P(HC, HRA, HRB, 6), 0.2)
        s1 = sperm(P(HC, HRA, HRB, -6))
        self.at("alone")
        self.play(FadeIn(e1, scale=0.4), FadeIn(s1, scale=0.4), run_time=0.6)
        self.at("there is no haploid body")
        self.play(Indicate(hum, color=TEAL, scale_factor=1.06), run_time=1.0)
        self.finish()


class S15Algae(SpokenScene):
    def construct(self):
        self.add(legend())
        ftr = ValueTracker(F_HUMAN)
        gold = always_redraw(lambda: arc(HC, HRA, HRB, M, ftr.get_value(), GOLD, 10))
        teal = always_redraw(lambda: arc(HC, HRA, HRB, ftr.get_value(), M - 360, TEAL, 10))
        gm = always_redraw(lambda: gate_m(P(HC, HRA, HRB, M), r=0.62, size=22))
        gf = always_redraw(lambda: gate_f(P(HC, HRA, HRB, ftr.get_value()), r=0.5))
        hum = silhouette().move_to([-5.1, 0.3, 0])
        self.add(panel(HC, HRA, HRB), gold, teal, gm, gf, hum)
        th = ValueTracker(90.0)
        rd = rider(HC, HRA, HRB, M, ftr, th)
        spin(self, th, 12.0)
        self.add(rd)
        alga = VGroup(Circle(radius=1.3, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.6),
                      Ellipse(width=1.2, height=0.6, stroke_color=LEAF, stroke_width=3, fill_color=LEAF, fill_opacity=0.6)
                      ).move_to([-5.1, 0.3, 0])
        al = T("green alga", 30, GOLD, weight=BOLD).move_to([-5.0, -2.2, 0])
        self.at("in the green algae")
        self.play(FadeOut(hum), FadeIn(alga, scale=0.7), FadeIn(al), run_time=0.9)
        self.at("the teal arc shrinks instead")
        self.play(ftr.animate.set_value(F_ALGA), run_time=2.6)
        self.at("the zygote is")
        zl = VGroup(T("zygote:", 32, TEAL, weight=BOLD), T("the only 2n cell", 30, TEAL)).arrange(DOWN, buff=0.1)
        zl.move_to([0.4, 0.9, 0])
        self.play(FadeIn(zl, shift=RIGHT * 0.2), run_time=1.0)
        self.at("it undergoes meiosis")
        zd = dotc(TEAL, 0.24, P(HC, HRA, HRB, 40))
        self.add(zd)
        self.play(zd.animate.move_to(P(HC, HRA, HRB, M)), run_time=1.0)
        self.play(zd.animate.set_fill(GOLD, 1).set_stroke(GOLD), pls(gm, 1.2), run_time=0.7)
        self.finish()


ROW = [(-4.95, "moss", F_MOSS), (-1.65, "fern", F_FERN), (1.65, "human", F_HUMAN), (4.95, "alga", F_ALGA)]
RRA, RRB = 1.42, 1.9
RY = 0.45


def ring_row():
    out = []
    for x, name, f in ROW:
        c = np.array([x, RY, 0.0])
        g = arc(c, RRA, RRB, M, f, GOLD, 10)
        t = arc(c, RRA, RRB, f, M - 360, TEAL, 10)
        gm = gate_small(P(c, RRA, RRB, M), 0.22)
        gf = gate_small(P(c, RRA, RRB, f), 0.22)
        lab = T(name, 32, TEXT, weight=BOLD).move_to([x, RY - RRB - 0.45, 0])
        out.append((c, f, g, t, gm, gf, lab, panel(c, RRA, RRB)))
    return out


class S16Rule(SpokenScene):
    def construct(self):
        self.add(legend())
        rows = ring_row()
        th = ValueTracker(90.0)
        spin(self, th, 12.0)
        for i, (c, f, g, t, gm, gf, lab, pn) in enumerate(rows):
            self.add(pn, g, t, gm, gf, lab)
            self.add(rider(c, RRA, RRB, M, f, th, off=40 * i, r=0.2))
        self.wait(0.3)
        big = [(r[2] if r[1] in (F_MOSS, F_ALGA) else r[3]) for r in rows]
        self.at("so size tells you nothing")
        self.play(*[pls(b, 1.06) for b in big], run_time=1.2)
        self.at("the big body can be")
        self.play(*[pls(b, 1.06) for b in big], run_time=1.2)
        self.at("find meiosis and fusion first")
        self.play(*[r[2].animate.set_stroke(RING, 10) for r in rows], *[r[3].animate.set_stroke(RING, 10) for r in rows],
                  *[pls(r[4], 1.6) for r in rows], *[pls(r[5], 1.6) for r in rows], run_time=1.4)
        rule = T("find meiosis and fusion; the labels follow", 34, TEXT, weight=BOLD).move_to([0, -2.85, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.5)
        self.at("every label follows")
        self.play(*[r[2].animate.set_stroke(GOLD, 10) for r in rows], *[r[3].animate.set_stroke(TEAL, 10) for r in rows],
                  run_time=1.4)
        self.finish()


class S17Water(SpokenScene):
    def construct(self):
        self.add(legend())
        shoots = moss_shoots()
        fm = film()
        mo = VGroup(shoots, fm).scale(0.78).move_to([-3.4, -0.5, 0])
        hh = heart(3.0, GOLD, 0.9).move_to([3.4, -0.2, 0])
        fm2 = ParametricFunction(lambda t: np.array([1.8 + 3.2 * t, -1.75 + 0.06 * np.sin(t * 18), 0]), t_range=[0, 1, 0.01],
                                 color=WATER, stroke_width=9)
        fm2.set_stroke(opacity=0.85)
        ml = T("moss", 34, GOLD, weight=BOLD).move_to([-3.4, 1.7, 0])
        fl = T("fern", 34, TEAL, weight=BOLD).move_to([3.4, 1.7, 0])
        self.play(FadeIn(mo, shift=UP * 0.2), FadeIn(hh, shift=UP * 0.2), FadeIn(fm2), FadeIn(ml), FadeIn(fl), run_time=1.2)
        add_sway(shoots, 0.03, 4.0)
        self.at("in both the moss")
        self.play(fm.animate.set_stroke(WATER, 14, opacity=1.0), fm2.animate.set_stroke(WATER, 14, opacity=1.0), run_time=0.8)
        self.at("sperm swim")
        s1 = sperm([-5.4, -0.3, 0])
        s2 = sperm([2.0, -1.55, 0])
        self.add(s1, s2)
        self.play(s1.animate.shift(RIGHT * 2.9 + UP * 0.3), s2.animate.shift(RIGHT * 1.8 + UP * 0.4), run_time=2.4,
                  rate_func=linear)
        self.at("what can a plant do", lead=0.9)
        old = VGroup(mo, hh, fm2, ml, fl, s1, s2)
        ridge = Polygon([-7, -2.8, 0], [-4, -2.3, 0], [-1, -2.55, 0], [3, -2.2, 0], [7, -2.7, 0], [7, -3.1, 0], [-7, -3.1, 0],
                        stroke_color="#8A6A4A", stroke_width=3, fill_color="#6B5238", fill_opacity=1)
        tree = pine(-1.2, -2.3)
        sun = Circle(radius=0.7, stroke_color="#FFC83D", stroke_width=4, fill_color="#FFC83D", fill_opacity=1)
        rays = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * 0.95, np.array([np.cos(a), np.sin(a), 0]) * 1.4,
                             stroke_color="#FFC83D", stroke_width=5) for a in np.linspace(0, TAU, 11)[:-1]])
        sunner = VGroup(sun, rays).move_to([5.4, 2.7, 0])
        q = T("?", 100, TEXT, weight=BOLD).move_to([2.2, 0.0, 0])
        newg = VGroup(ridge, tree, sunner, q).shift(DOWN * 8)
        self.add(newg)
        self.play(old.animate.shift(UP * 8), newg.animate.shift(UP * 8), run_time=1.4)
        rays.add_updater(lambda m, dt: m.rotate(0.3 * dt, about_point=sun.get_center()))
        bob(q, 0.1, 1.6)
        bob(tree.cone, 0.04, 2.0)
        self.finish()


class S18End(EndCard):
    LINE = "Find meiosis and fusion; the labels follow, whichever body is big."
