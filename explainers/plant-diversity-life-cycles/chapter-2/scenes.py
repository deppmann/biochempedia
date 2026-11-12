"""The Gametophyte Moves Inside: seed plants (Biochemistrypedia explainer, chapter 2).

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



# ---------------------------------------------------------------- film 1 drawings reused
def leaf(pos, ang, length, color, op=0.45):
    e = Ellipse(width=length, height=length * 0.34, stroke_color=color, stroke_width=2, fill_color=color,
                fill_opacity=op)
    e.rotate(ang).move_to(pos)
    return e



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



def pill(txt, color, size=28, pos=ORIGIN):
    lab = T(txt, size, color, weight=BOLD)
    r = RoundedRectangle(corner_radius=0.15, width=lab.width + 0.45, height=lab.height + 0.35, stroke_color=color,
                         stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(r, lab).move_to(pos)





# =================================================================== chapter 2 world
S_INSET = 0.38
MINI_RA, MINI_RB = RA * S_INSET, RB * S_INSET
LENS_C = np.array([4.25, 0.4, 0.0])
LENS_R = 2.45
SLOT = np.array([4.25, -2.6, 0.0])         # the one label slot under the lens
PX, PBASE = -1.2, -2.3                     # the pine (as film 1 ended)
SMALL_CONE = np.array([-2.6, -0.85, 0.0])
BIG_CONE = np.array([0.2, -0.85, 0.0])
GATE_L = np.array([3.1, 0.4, 0.0])        # meiosis gate inside the lens
SPORE_X = [3.9, 4.4, 4.9, 5.4]


def legend2(coral_live=False):
    def item(col, s, live=True):
        d = Dot(radius=0.17, color=col).set_opacity(1 if live else 0.35)
        t = T(s, 24, TEXT if live else GREY)
        return VGroup(d, t).arrange(RIGHT, buff=0.15)
    a = item(GOLD, "n  haploid")
    b = item(TEAL, "2n  diploid")
    c = item(CORAL, "3n  triploid" if coral_live else "3n  later", coral_live)
    row = VGroup(a, b, c).arrange(RIGHT, buff=0.8).move_to([-1.2, -3.5, 0])
    sch = T("schematic", 22, GREY).move_to([5.7, -3.5, 0])
    g = VGroup(row, sch)
    g.coral = c
    return g


def backed(m, buff=0.12):
    r = RoundedRectangle(corner_radius=0.12, width=m.width + 2 * buff, height=m.height + 2 * buff, stroke_width=0,
                         fill_color=BG, fill_opacity=0.93).move_to(m)
    return VGroup(r, m)


def lab(txt, color=TEXT, pos=SLOT, size=28, weight=BOLD, bk=True):
    t = T(txt, size, color, weight=weight).move_to(pos)
    return backed(t) if bk else t


def lab2(l1, l2, color=TEXT, pos=SLOT, size=28):
    g = VGroup(T(l1, size, color, weight=BOLD), T(l2, size, color, weight=BOLD)).arrange(DOWN, buff=0.08).move_to(pos)
    return backed(g)


def lane(c, ra, rb, k, color=GOLD, w=8, s0=0.0, s1=1.0):
    c0, c1 = P(c, ra, rb, M), P(c, ra, rb, F)

    def f(s):
        a = P(c, ra, rb, M + (F - M) * s)
        ch = c0 + (c1 - c0) * s
        return ch + (a - ch) * k
    return ParametricFunction(f, t_range=[s0, s1, 0.01], color=color, stroke_width=w)


def lane_pt(c, ra, rb, k, s):
    c0, c1 = P(c, ra, rb, M), P(c, ra, rb, F)
    a = P(c, ra, rb, M + (F - M) * s)
    ch = c0 + (c1 - c0) * s
    return ch + (a - ch) * k


def ovule_rect(c, ra, rb, w=4):
    sc = rb / RB
    r = RoundedRectangle(corner_radius=0.5 * sc, width=0.958 * ra, height=0.56 * rb, stroke_color=TEAL,
                         stroke_width=w, fill_color=TEAL, fill_opacity=0.14)
    return r.move_to([c[0], c[1] - 0.85 * rb, 0])


def corner(male=False, ovule=False, grain=False, arrow=False, c=MINI_C, ra=MINI_RA, rb=MINI_RB, w=8, grain_s=0.5):
    gold = arc(c, ra, rb, M, F, GOLD, w)
    teal = arc(c, ra, rb, F, M - 360, TEAL, w)
    gm_ = gate_small(P(c, ra, rb, M), 0.2 * ra / MINI_RA)
    gf_ = gate_small(P(c, ra, rb, F), 0.2 * ra / MINI_RA)
    g = VGroup(gold, teal, gm_, gf_)
    g.fem, g.teal, g.gm, g.gf = gold, teal, gm_, gf_
    g.male = g.ov = g.grain = g.arrow = None
    if male:
        g.male = lane(c, ra, rb, 0.4, GOLD, w)
        g.add(g.male)
    if ovule:
        g.ov = ovule_rect(c, ra, rb, 4 if ra < 3 else 6)
        g.add(g.ov)
    if grain:
        gp = lane_pt(c, ra, rb, 0.4, grain_s)
        g.grain = Circle(radius=max(0.09, 0.067 * ra), stroke_color=WHITE, stroke_width=2, fill_color=GOLD,
                         fill_opacity=1).move_to(gp)
        g.add(g.grain)
    if arrow:
        gp = lane_pt(c, ra, rb, 0.4, 0.5)
        top = gp + DOWN * max(0.12, 0.067 * ra)
        bot = np.array([c[0], c[1] - 0.57 * rb, 0.0])
        g.arrow = Arrow(top, bot, buff=0, stroke_width=4 if ra < 3 else 7, tip_length=0.12 if ra < 3 else 0.3,
                        color=WHITE, max_tip_length_to_length_ratio=0.9)
        g.add(g.arrow)
    return g


def corner_tags():
    m = T("male", 26, GOLD, weight=BOLD).move_to([MINI_C[0], MINI_C[1] + 0.62, 0])
    f = T("female", 26, GOLD, weight=BOLD).move_to([MINI_C[0], MINI_C[1] - 1.45, 0])
    return VGroup(m, f)


def ridge():
    return Polygon([-7, -2.8, 0], [-4, -2.3, 0], [-1, -2.55, 0], [3, -2.2, 0], [7, -2.7, 0], [7, -3.1, 0], [-7, -3.1, 0],
                   stroke_color="#8A6A4A", stroke_width=3, fill_color="#6B5238", fill_opacity=1)


def sunner():
    sun = Circle(radius=0.7, stroke_color="#FFC83D", stroke_width=4, fill_color="#FFC83D", fill_opacity=1)
    rays = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * 0.95, np.array([np.cos(a), np.sin(a), 0]) * 1.4,
                         stroke_color="#FFC83D", stroke_width=5) for a in np.linspace(0, TAU, 11)[:-1]])
    g = VGroup(sun, rays).move_to([5.4, 2.7, 0])
    g.sun, g.rays = sun, rays
    return g


def cone_m(pos, w, h):
    e = Ellipse(width=w, height=h, stroke_color="#8A5A2B", stroke_width=3, fill_color=BROWN, fill_opacity=1).move_to(pos)
    ln = VGroup(*[Line(pos + np.array([-w * 0.4, y, 0]), pos + np.array([w * 0.4, y, 0]), stroke_color="#8A5A2B",
                       stroke_width=2) for y in (-h * 0.2, 0.0, h * 0.2)])
    return VGroup(e, ln)


def pine_world(with_cones=True):
    tr = pine(PX, PBASE)
    tr.remove(tr.cone)
    g = VGroup(ridge(), tr)
    sc = cone_m(SMALL_CONE, 0.36, 0.56)
    bc = cone_m(BIG_CONE, 0.6, 0.95)
    g.tree, g.small, g.big = tr, sc, bc
    if with_cones:
        g.add(sc, bc)
    return g


def lens_obj():
    c = Circle(radius=LENS_R, stroke_color=WHITE, stroke_width=5, fill_color=BG, fill_opacity=1).move_to(LENS_C)
    c.set_z_index(1)
    return c


def zlist(mobs, z):
    for m in mobs:
        m.set_z_index(z)
    return mobs


def ovule_obj(w=3.8, h=3.0):
    return Ellipse(width=w, height=h, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.3).move_to(LENS_C)


def micro_dot(pos, r=0.22, color=GOLD):
    return dotc(color, r, pos)


def grain_obj(pos, r=0.42, nuclei=3):
    body = Circle(radius=r, stroke_color=WHITE, stroke_width=3, fill_color=GOLD, fill_opacity=0.35).move_to(pos)
    g = VGroup(body)
    offs = [(-0.16, 0.1), (0.15, 0.12), (0.0, -0.17)][:nuclei]
    for ox, oy in offs:
        g.add(Dot(pos + np.array([ox, oy, 0]), radius=0.09, color=GOLD))
    return g


def droplet(pos, s=1.0):
    c = Circle(radius=0.2 * s, stroke_color=WATER, stroke_width=2, fill_color=WATER, fill_opacity=1).move_to(pos + DOWN * 0.08 * s)
    t = Triangle(stroke_width=0, fill_color=WATER, fill_opacity=1).scale(0.2 * s).move_to(pos + UP * 0.2 * s)
    return VGroup(c, t)


def cross(pos, s=0.35, color=WHITE, w=6):
    return VGroup(Line(pos + np.array([-s, -s, 0]), pos + np.array([s, s, 0]), stroke_color=color, stroke_width=w),
                  Line(pos + np.array([-s, s, 0]), pos + np.array([s, -s, 0]), stroke_color=color, stroke_width=w))


def static_state(scene, sun=False, lens=False, wheel_kw=None, tags=True, legend_obj=None):
    wk = dict(male=True)
    wk.update(wheel_kw or {})
    pw = pine_world()
    cw = corner(**wk)
    lg = legend_obj or legend2()
    objs = [pw, cw, lg]
    scene.add(pw, cw, lg)
    tg = None
    if tags:
        tg = corner_tags()
        scene.add(tg)
    s_ = None
    if sun:
        s_ = sunner()
        scene.add(s_)
    ln = None
    if lens:
        ln = lens_obj()
        scene.add(ln)
    return pw, cw, lg, tg, s_, ln


def spin_rider(scene, c=MINI_C, ra=MINI_RA, rb=MINI_RB, period=9.0, r=0.1):
    th = ValueTracker(M)
    rd = rider(c, ra, rb, M, F, th, r=r)
    spin(scene, th, period)
    scene.add(rd)
    return rd, th


# =================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Plants on Land"
    TITLE = "The Gametophyte Moves Inside"

    def construct(self):
        pn = panel(C0, RA, RB)
        ga = arc(C0, RA, RB, M, F, GOLD, 10).set_stroke(opacity=0.45)
        ta = arc(C0, RA, RB, F, M - 360, TEAL, 10).set_stroke(opacity=0.45)
        th = ValueTracker(M)
        rd = rider(C0, RA, RB, M, F, th, r=0.3)
        self.add(pn, ga, ta, rd)
        spin(self, th, 6.0)
        super().construct()


class S01Question(SpokenScene):
    def construct(self):
        lg = legend2()
        self.add(lg)
        pn = panel(C0, RA, RB)
        ga = arc(C0, RA, RB, M, F, GOLD, 10)
        ta = arc(C0, RA, RB, F + 360, M, TEAL, 10)
        gm = gate_m(P(C0, RA, RB, M))
        gf = gate_f(P(C0, RA, RB, F))
        body = VGroup(ga, ta, gm[0], gf[0])
        labs = VGroup(gm[1], gf[1])
        th = ValueTracker(M)
        rd = rider(C0, RA, RB, M, F, th, r=0.3)
        self.add(pn)
        self.play(Create(ga), Create(ta), FadeIn(gm), FadeIn(gf), run_time=1.6)
        self.add(rd)
        spin(self, th, 9.0)
        self.at("gold after meiosis", lead=0.0)
        self.play(ga.animate.set_stroke(width=18), pls(gm, 1.2), run_time=0.9)
        self.play(ga.animate.set_stroke(width=10), run_time=0.4)
        self.at("teal after fusion", lead=0.0)
        self.play(ta.animate.set_stroke(width=18), pls(gf, 1.2), run_time=0.9)
        self.play(ta.animate.set_stroke(width=10), run_time=0.4)
        # the wheel shrinks into the corner while the dry ridge and the pine rise
        pw = pine_world(with_cones=False)
        sn = sunner()
        rise = VGroup(pw, sn).shift(DOWN * 8)
        self.add(rise)
        self.at("now at the top", lead=0.3)
        self.remove(rd)
        self.play(FadeOut(labs), FadeOut(pn), body.animate.scale(S_INSET).move_to(MINI_C),
                  rise.animate.shift(UP * 8), run_time=1.6)
        self.remove(body)
        cw = corner(male=False)
        self.add(cw)
        sn.rays.add_updater(lambda m, dt: m.rotate(0.3 * dt, about_point=sn.sun.get_center()))
        # no water film
        film = ParametricFunction(lambda t: np.array([2.4 + 3.8 * t, -1.9 + 0.06 * np.sin(t * 16), 0]), t_range=[0, 1, 0.01],
                                  color=WATER, stroke_width=9)
        self.at("there is no water", lead=0.4)
        self.play(Create(film), run_time=0.8)
        nw = T("no water film", 36, TEXT, weight=BOLD).move_to([4.2, -1.1, 0])
        self.at("water film", lead=0.1)
        self.play(FadeIn(nw, shift=UP * 0.1), run_time=0.5)
        xx = cross(np.array([4.3, -1.9, 0]), 0.45, WHITE, 8)
        self.play(Create(xx), run_time=0.5)
        # the two cones and the question
        sc, bc = cone_m(SMALL_CONE, 0.36, 0.56), cone_m(BIG_CONE, 0.6, 0.95)
        self.at("so how does a sperm", lead=0.3)
        self.play(FadeIn(sc, scale=0.4), FadeIn(bc, scale=0.4), run_time=0.7)
        q = T("?", 90, YELLOW, weight=BOLD).move_to([-1.2, -0.8, 0])
        self.play(FadeIn(q, scale=1.6), run_time=0.5)
        bob(q, 0.08, 1.6)
        bob(sc, 0.04, 2.0)
        bob(bc, 0.04, 2.0, 1.0)
        self.finish()


class S02Tree(SpokenScene):
    def construct(self):
        pw = pine_world(with_cones=True)
        cw = corner(male=False)
        lg = legend2()
        sn = sunner()
        self.add(pw, cw, lg, sn)
        sn.rays.add_updater(lambda m, dt: m.rotate(0.3 * dt, about_point=sn.sun.get_center()))
        bob(pw.small, 0.04, 2.0)
        bob(pw.big, 0.04, 2.0, 1.0)
        spin_rider(self)
        self.at("the pine tree is", lead=0.0)
        self.play(Indicate(pw.tree, color=WHITE, scale_factor=1.03), run_time=1.0)
        sl = T("sporophyte, 2n", 34, TEAL, weight=BOLD).move_to([-4.8, -0.4, 0])
        self.at("sporophyte", lead=0.3)
        self.play(FadeIn(sl, shift=RIGHT * 0.2), run_time=0.5)
        self.at("so it is teal", lead=0.2)
        fills = [m for m in pw.tree if isinstance(m, Polygon) and not isinstance(m, Rectangle)]
        self.play(*[m.animate.set_fill(TEAL, 1).set_stroke(TEAL) for m in fills], sl.animate.set_color(TEAL), run_time=1.0)
        self.at("its cones make two kinds", lead=0.3)
        self.play(pls(pw.small, 1.5), pls(pw.big, 1.5), run_time=1.2)
        self.at("so the gold arc splits", lead=0.6)
        male = lane(MINI_C, MINI_RA, MINI_RB, 0.4, GOLD, 8)
        self.play(TransformFromCopy(cw.fem, male), run_time=1.6)
        cw.male = male
        cw.add(male)
        mt = T("male", 26, GOLD, weight=BOLD).move_to([MINI_C[0], MINI_C[1] + 0.62, 0])
        ft = T("female", 26, GOLD, weight=BOLD).move_to([MINI_C[0], MINI_C[1] - 1.45, 0])
        self.at("in two", lead=0.3)
        self.play(FadeIn(mt, shift=DOWN * 0.1), FadeIn(ft, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S03Pollen(SpokenScene):
    def construct(self):
        pw, cw, lg, tg, _, _ = static_state(self)
        spin_rider(self)
        bob(pw.small, 0.04, 2.0)
        bob(pw.big, 0.04, 2.0, 1.0)
        # open the lens on the small cone
        ring_ = Circle(radius=0.45, stroke_color=WHITE, stroke_width=4).move_to(SMALL_CONE)
        ln = lens_obj()
        cluster = VGroup(*[cone_m(LENS_C + np.array(p, float), 0.7, 1.1) for p in [(-0.9, 0.2, 0), (0.0, -0.3, 0), (0.9, 0.2, 0)]])
        cluster.set_z_index(2)
        self.play(Create(ring_), GrowFromPoint(ln, SMALL_CONE), run_time=0.9)
        self.play(FadeIn(cluster, scale=0.6), run_time=0.5)
        for i, c in enumerate(cluster):
            bob(c, 0.05, 2.2, i * 0.7)
        # meiosis makes microspores
        self.at("meiosis makes", lead=0.3)
        gm = gate_m(GATE_L, r=0.62, size=22)
        tok = dotc(TEAL, 0.3, GATE_L)
        zlist([gm, tok], 3)
        self.play(FadeOut(cluster), FadeIn(gm, scale=0.7), FadeIn(tok, scale=0.5), run_time=0.5)
        pos4 = [LENS_C + np.array(p, float) for p in [(0.05, 0.5, 0), (1.05, 0.5, 0), (0.05, -0.5, 0), (1.05, -0.5, 0)]]
        outs = VGroup(*[micro_dot(GATE_L, 0.2) for _ in range(4)])
        zlist(outs, 2)
        self.remove(tok)
        self.add(outs)
        self.play(*[o.animate.move_to(p) for o, p in zip(outs, pos4)], Indicate(cw.male, color=WHITE, scale_factor=1.0), run_time=0.9)
        ml = lab("microspores", GOLD, LENS_C + np.array([0.05, -1.4, 0]), 30, bk=False)
        ml.set_z_index(3)
        self.at("microspores", lead=0.2)
        self.play(FadeIn(ml, shift=UP * 0.1), run_time=0.4)
        for i, o in enumerate(outs):
            bob(o, 0.05, 2.0, i * 0.5)
        # each swells into a pollen grain
        self.at("each one becomes", lead=0.2)
        grains = VGroup(*[grain_obj(p, 0.42, 3) for p in pos4])
        zlist(grains, 3)
        self.play(*[ReplacementTransform(o, g) for o, g in zip(outs, grains)], run_time=1.2)
        gl = lab("pollen grains", GOLD, LENS_C + np.array([0.05, -1.4, 0]), 30, bk=False)
        gl.set_z_index(3)
        self.play(FadeOut(ml), FadeIn(gl), FadeOut(gm), run_time=0.5)
        for i, g in enumerate(grains):
            bob(g, 0.05, 2.0, i * 0.5)
        # not a sperm
        self.at("is not a sperm", lead=0.8)
        sp = T("sperm", 36, TEXT, weight=BOLD).move_to(LENS_C + np.array([0.05, 1.75, 0]))
        xx = Line(sp.get_left() + LEFT * 0.1, sp.get_right() + RIGHT * 0.1, stroke_color=CORAL, stroke_width=8)
        VGroup(sp, xx).set_z_index(3)
        self.play(FadeIn(sp, scale=1.3), run_time=0.4)
        self.play(Create(xx), run_time=0.4)
        # a male gametophyte of a few cells
        self.at("male gametophyte", lead=0.6)
        self.play(FadeOut(sp), FadeOut(xx), FadeOut(gl), run_time=0.4)
        gt = lab2("male gametophyte:", "a few cells", GOLD)
        self.play(FadeIn(gt, shift=UP * 0.1), Indicate(grains[0], color=GOLD, scale_factor=1.35), run_time=0.8)
        self.finish()


class S04Ovule(SpokenScene):
    def construct(self):
        pw, cw, lg, tg, _, _ = static_state(self)
        spin_rider(self)
        bob(pw.small, 0.04, 2.0)
        bob(pw.big, 0.04, 2.0, 1.0)
        ring_ = Circle(radius=0.6, stroke_color=WHITE, stroke_width=4).move_to(BIG_CONE)
        ln = lens_obj()
        ov = ovule_obj()
        ov.set_z_index(2)
        self.play(Create(ring_), GrowFromPoint(ln, BIG_CONE), run_time=0.9)
        self.play(FadeIn(ov, scale=0.6), run_time=0.6)
        breathe(ov, 0.015, 3.0)
        ol = lab("ovule", TEAL, LENS_C + np.array([0.0, -1.9, 0]), 28, bk=False)
        ol.set_z_index(3)
        self.at("meiosis inside an ovule", lead=0.3)
        gm = gate_m(GATE_L, r=0.55, size=20)
        tok = dotc(TEAL, 0.28, GATE_L + LEFT * 0.0)
        zlist([gm, tok], 3)
        self.play(FadeIn(ol), FadeIn(gm, scale=0.7), Indicate(cw.fem, color=WHITE, scale_factor=1.0), run_time=0.8)
        self.at("gives four", lead=0.8)
        outs = VGroup(*[micro_dot(GATE_L, 0.22) for _ in range(4)])
        zlist(outs, 2)
        self.add(outs)
        self.play(*[o.animate.move_to(np.array([x, LENS_C[1], 0])) for o, x in zip(outs, SPORE_X)], run_time=1.2)
        ml = lab("megaspores", GOLD, LENS_C + np.array([0.0, 0.75, 0]), 26, bk=False)
        ml.set_z_index(3)
        self.at("megaspores", lead=0.3)
        self.play(FadeIn(ml, shift=DOWN * 0.1), run_time=0.4)
        for i, o in enumerate(outs):
            bob(o, 0.05, 2.0, i * 0.5)
        # only one survives
        self.at("only one survives", lead=0.6)
        self.play(*[o.animate.set_fill(GREY, 0.8).set_stroke(GREY) for o in outs[:3]], FadeOut(gm), run_time=0.8)
        self.play(*[FadeOut(o, scale=0.4) for o in outs[:3]], run_time=0.8)
        # it grows into the female gametophyte
        self.at("it grows into the female", lead=0.4)
        surv = outs[3]
        mass = Ellipse(width=2.7, height=1.8, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.5).move_to(LENS_C + np.array([0.45, 0.0, 0]))
        mass.set_z_index(3)
        self.play(ReplacementTransform(surv, mass), FadeOut(ml), run_time=1.6)
        gl = lab("female gametophyte, n", GOLD)
        self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.5)
        # forms eggs
        self.at("forms eggs", lead=0.8)
        e1 = dotc(GOLD, 0.26, LENS_C + np.array([-0.35, 0.4, 0]))
        e2 = dotc(GOLD, 0.26, LENS_C + np.array([-0.35, -0.4, 0]))
        zlist([e1, e2], 4)
        self.play(FadeIn(e1, scale=0.4), FadeIn(e2, scale=0.4), run_time=0.7)
        pl = pill("egg", GOLD, 28, LENS_C + np.array([1.1, 0.0, 0]))
        pl.set_z_index(4)
        self.play(FadeIn(pl), run_time=0.4)
        bob(e1, 0.04, 1.8)
        bob(e2, 0.04, 1.8, 0.9)
        breathe(mass, 0.02, 2.5)
        self.finish()


def ovule_state(scene, tube=False, grain=True):
    """The lens with the ovule and the female gametophyte, exactly as s04 ends."""
    ln = lens_obj()
    ov = ovule_obj()
    mass = Ellipse(width=2.7, height=1.8, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.5).move_to(LENS_C + np.array([0.45, 0.0, 0]))
    e1 = dotc(GOLD, 0.26, LENS_C + np.array([-0.35, 0.4, 0]))
    e2 = dotc(GOLD, 0.26, LENS_C + np.array([-0.35, -0.4, 0]))
    pl = pill("egg", GOLD, 28, LENS_C + np.array([1.1, 0.0, 0]))
    ol = lab("ovule", TEAL, LENS_C + np.array([0.0, -1.9, 0]), 28, bk=False)
    st = VGroup(ln, ov, mass, e1, e2, pl, ol)
    zlist([ov, mass, ol], 2)
    zlist([e1, e2, pl], 4)
    st.ov, st.mass, st.e1, st.e2, st.pl, st.ol = ov, mass, e1, e2, pl, ol
    scene.add(st)
    return st


class S05Tube(SpokenScene):
    def construct(self):
        pw, cw, lg, tg, _, _ = static_state(self)
        spin_rider(self)
        st = ovule_state(self)
        gl = lab("female gametophyte, n", GOLD)
        self.add(gl)
        bob(pw.small, 0.04, 2.0)
        bob(pw.big, 0.04, 2.0, 1.0)
        # wind carries pollen
        rng = np.random.RandomState(5)
        winds = VGroup()
        for i in range(5):
            y = LENS_C[1] + 1.3 + 0.28 * i - 0.2
            ln = ParametricFunction(lambda t, y=y: np.array([0, 0.07 * np.sin(t * 9), 0]) + np.array([t * 0.9, 0, 0]), t_range=[0, 1, 0.05],
                                    color=WHITE, stroke_width=3)
            ln.set_stroke(opacity=0.8).move_to([2.7 + rng.uniform(-0.3, 0.3), y + 0.4, 0])
            ln.v = rng.uniform(0.9, 1.5)

            def drift(m, dt):
                m.shift(RIGHT * m.v * dt)
                if m.get_x() > 3.9:
                    m.shift(LEFT * 2.4)
            ln.add_updater(drift)
            ln.set_z_index(5)
            winds.add(ln)
        grains = VGroup(*[Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_color=GOLD, fill_opacity=1).move_to([2.15 + 0.2 * i, 2.2 - 0.45 * i, 0]) for i in range(3)])
        zlist(grains, 5)
        self.at("wind carries pollen", lead=0.2)
        self.play(FadeIn(winds), FadeIn(grains), run_time=0.6)
        landing = np.array([2.3, 0.8, 0])
        self.play(grains[0].animate.move_to(landing), grains[1].animate.move_to([2.4, 2.0, 0]), grains[2].animate.move_to([2.9, 1.85, 0]), run_time=1.6)
        self.play(FadeOut(grains[1]), FadeOut(grains[2]), FadeOut(winds), run_time=0.5)
        # a pollen tube grows to the egg
        self.at("a pollen tube grows", lead=0.2)
        tube = Line([2.4, 0.8, 0], [3.65, 0.8, 0], stroke_color=GOLD, stroke_width=10)
        tube.set_z_index(4)
        self.play(Create(tube), run_time=1.3)
        sp = sperm([2.55, 0.8, 0])
        sp.set_z_index(5)
        self.at("delivers sperm", lead=0.3)
        self.add(sp)
        self.play(sp.animate.move_to([3.65, 0.8, 0]), run_time=1.3, rate_func=linear)
        self.play(pls(st.e1, 1.5), run_time=0.6)
        # no outside water
        self.at("with no outside water", lead=0.2)
        self.play(FadeOut(gl), run_time=0.3)
        nw = lab("no outside water", TEXT, SLOT + np.array([0.6, 0, 0]), 28)
        dr = droplet(SLOT + np.array([-1.6, 0, 0]), 1.2)
        xx = cross(SLOT + np.array([-1.6, 0, 0]), 0.3, WHITE, 6)
        self.play(FadeIn(nw), FadeIn(dr), run_time=0.4)
        self.play(Create(xx), run_time=0.4)
        # both gametophytes still here, just shrunk
        self.at("both gametophytes", lead=0.2)
        self.play(FadeOut(nw), FadeOut(dr), FadeOut(xx), run_time=0.4)
        self.play(cw.fem.animate.set_stroke(width=15), cw.male.animate.set_stroke(width=15), run_time=0.8)
        self.at("just shrunk", lead=0.2)
        self.play(cw.fem.animate.set_stroke(width=8), cw.male.animate.set_stroke(width=8), run_time=0.6)
        # the female one stays inside the ovule
        self.at("the female one stays", lead=0.2)
        ovr = ovule_rect(MINI_C, MINI_RA, MINI_RB, 4)
        cw.ov = ovr
        cw.add(ovr)
        self.play(Create(ovr), Indicate(st.mass, color=GOLD, scale_factor=1.08), run_time=1.2)
        fl = lab("female stays inside", GOLD, SLOT, 28)
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.4)
        # the male one travels as pollen
        self.at("the male one travels", lead=0.2)
        self.play(FadeOut(fl), run_time=0.3)
        gr = Circle(radius=0.1, stroke_color=WHITE, stroke_width=2, fill_color=GOLD, fill_opacity=1).move_to(lane_pt(MINI_C, MINI_RA, MINI_RB, 0.4, 0.2))
        cw.grain = gr
        self.add(gr)
        sub = lane(MINI_C, MINI_RA, MINI_RB, 0.4, GOLD, 1, 0.2, 0.5)
        ml = lab("male travels as pollen", GOLD, SLOT, 28)
        self.play(MoveAlongPath(gr, sub), FadeIn(ml, shift=UP * 0.1), run_time=2.0, rate_func=linear)
        arr = Arrow(lane_pt(MINI_C, MINI_RA, MINI_RB, 0.4, 0.5) + DOWN * 0.1, np.array([MINI_C[0], MINI_C[1] - 0.57 * MINI_RB, 0]), buff=0,
                    stroke_width=4, tip_length=0.12, color=WHITE, max_tip_length_to_length_ratio=0.9)
        cw.arrow = arr
        self.play(Create(arr), grains[0].animate.shift(LEFT * 0.0), run_time=0.6)
        self.finish()


def seed_layers(c=LENS_C):
    coat = Ellipse(width=3.7, height=2.9, stroke_color=WHITE, stroke_width=4, fill_opacity=0).move_to(c)
    food = Ellipse(width=3.0, height=2.2, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.08).move_to(c)
    emb = Ellipse(width=1.0, height=0.6, stroke_color=WHITE, stroke_width=4, fill_opacity=0).move_to(c + np.array([-0.3, 0.1, 0]))
    zlist([coat, food, emb], 3)
    return coat, food, emb


class S06Predict(SpokenScene):
    def construct(self):
        pw, cw, lg, tg, _, _ = static_state(self, wheel_kw=dict(male=True, ovule=True, grain=True, arrow=True))
        spin_rider(self)
        st = ovule_state(self)
        tube = Line([2.4, 0.8, 0], [3.65, 0.8, 0], stroke_color=GOLD, stroke_width=10)
        tube.set_z_index(4)
        self.add(tube)
        bob(pw.small, 0.04, 2.0)
        bob(pw.big, 0.04, 2.0, 1.0)
        pnts = LENS_C + np.array([-0.35, 0.4, 0])
        # the egg is fertilized
        self.at("the egg is fertilized", lead=0.0)
        gf_ = gate_f(pnts, r=0.4)
        gf_.set_z_index(8)
        sp = sperm([3.0, 0.8, 0])
        sp.set_z_index(9)
        self.add(sp)
        self.play(FadeIn(gf_, scale=0.6), sp.animate.move_to(pnts), run_time=1.0)
        self.play(pls(gf_, 1.3), run_time=0.5)
        zy = dotc(TEAL, 0.28, pnts)
        zy.set_z_index(6)
        self.remove(sp)
        self.add(zy)
        self.play(FadeOut(gf_), FadeOut(tube), run_time=0.5)
        # a seed forms
        self.at("and a seed forms", lead=0.3)
        coat, food, emb = seed_layers()
        self.play(FadeOut(st.ov), FadeOut(st.mass), FadeOut(st.e1), FadeOut(st.e2), FadeOut(st.pl), FadeOut(st.ol), FadeOut(zy), Create(coat), run_time=1.0)
        self.play(Create(food), run_time=0.8)
        self.play(Create(emb), run_time=0.7)
        self.at("food store", lead=0.2)
        fl = lab("food store: ?", YELLOW, SLOT + np.array([-1.0, 0, 0]), 32)
        fl.set_z_index(3)
        tr = ValueTracker(0.0)
        food.add_updater(lambda m: m.set_fill(WHITE, 0.08 + 0.12 * (0.5 + 0.5 * np.sin(tr.get_value()))))
        self.add(tr)
        tr.add_updater(lambda t, dt: t.increment_value(dt * 4.0))
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.5)
        self.at("gold or teal", lead=0.6)
        sg = dotc(GOLD, 0.28, SLOT + np.array([1.5, 0, 0]))
        st_ = dotc(TEAL, 0.28, SLOT + np.array([2.2, 0, 0]))
        self.play(FadeIn(sg, scale=0.5), FadeIn(st_, scale=0.5), run_time=0.5)
        bob(sg, 0.07, 1.8)
        bob(st_, 0.07, 1.8, 0.9)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        pw, cw, lg, tg, _, _ = static_state(self, wheel_kw=dict(male=True, ovule=True, grain=True, arrow=True))
        spin_rider(self)
        self.add(lens_obj())
        coat, food, emb = seed_layers()
        self.add(coat, food, emb)
        fl = lab("food store: ?", YELLOW, SLOT + np.array([-1.0, 0, 0]), 32)
        fl.set_z_index(3)
        sg = dotc(GOLD, 0.28, SLOT + np.array([1.5, 0, 0]))
        st_ = dotc(TEAL, 0.28, SLOT + np.array([2.2, 0, 0]))
        self.add(fl, sg, st_)
        bob(sg, 0.07, 1.8)
        bob(st_, 0.07, 1.8, 0.9)
        tr = ValueTracker(0.0)
        food.add_updater(lambda m: m.set_fill(WHITE, 0.08 + 0.12 * (0.5 + 0.5 * np.sin(tr.get_value()))))
        tr.add_updater(lambda t, dt: t.increment_value(dt * 4.0))
        self.add(tr)
        bar = Rectangle(width=10, height=0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.9)
        tm = ValueTracker(1.0)
        bar.add_updater(lambda b: b.become(Rectangle(width=max(0.01, 10 * tm.get_value()), height=0.1, stroke_width=0,
                                                    fill_color=GREY, fill_opacity=0.9).move_to([-5 + 5 * tm.get_value(), -3.1, 0])))
        self.add(bar)
        self.play(tm.animate.set_value(0.0), run_time=self.narration_s - 0.1, rate_func=linear)
        self.finish()


class S08Reveal(SpokenScene):
    def construct(self):
        pw, cw, lg, tg, _, _ = static_state(self, wheel_kw=dict(male=True, ovule=True, grain=True, arrow=True))
        spin_rider(self)
        self.add(lens_obj())
        coat, food, emb = seed_layers()
        self.add(coat, food, emb)
        fl = lab("food store: ?", YELLOW, SLOT + np.array([-1.0, 0, 0]), 32)
        sg = dotc(GOLD, 0.28, SLOT + np.array([1.5, 0, 0]))
        st_ = dotc(TEAL, 0.28, SLOT + np.array([2.2, 0, 0]))
        zlist([fl, sg, st_], 3)
        self.add(fl, sg, st_)
        tr = ValueTracker(0.0)
        food.add_updater(lambda m: m.set_fill(WHITE, 0.08 + 0.12 * (0.5 + 0.5 * np.sin(tr.get_value()))))
        tr.add_updater(lambda t, dt: t.increment_value(dt * 4.0))
        self.add(tr)
        self.at("gold", lead=0.0)
        food.clear_updaters()
        self.remove(tr)
        self.play(pw.animate.set_opacity(0.3), food.animate.set_fill(GOLD, 0.8).set_stroke(GOLD), FadeOut(st_), sg.animate.move_to(SLOT + np.array([2.0, 0, 0])), run_time=0.8)
        self.play(FadeOut(sg), run_time=0.3)
        # the arrows trace back to the corner wheel: gold lane, teal arc, teal arc
        def trace(start, end, color, ang):
            a = CurvedArrow(start, end, angle=ang, color=color, stroke_width=5, tip_length=0.2)
            a.set_z_index(9)
            return a
        # food store = female gametophyte
        self.at("the food store is", lead=0.2)
        l1 = lab("female gametophyte, n", GOLD)
        self.play(FadeOut(fl), FadeIn(l1), run_time=0.5)
        fl = l1
        a1 = trace(LENS_C + np.array([-1.4, -1.5, 0]), np.array([-4.2, 1.45, 0]), GOLD, -0.5)
        self.play(Create(a1), Indicate(cw.fem, color=GOLD, scale_factor=1.0), run_time=1.2)
        self.at("so it is haploid", lead=0.0)
        self.play(pls(food, 1.05), run_time=0.8)
        # coat = parent sporophyte, teal
        self.at("the seed coat comes", lead=0.3)
        self.play(FadeOut(a1), run_time=0.3)
        l2 = lab("parent sporophyte, 2n", TEAL)
        self.play(FadeOut(fl), FadeIn(l2), coat.animate.set_fill(TEAL, 0.9).set_stroke(TEAL), run_time=1.0)
        fl = l2
        a2 = trace(LENS_C + np.array([-1.2, 1.7, 0]), np.array([-4.9, 3.6, 0]), TEAL, 0.5)
        self.play(Create(a2), run_time=1.0)
        # embryo = new sporophyte
        self.at("the embryo is the new", lead=0.3)
        self.play(FadeOut(a2), run_time=0.3)
        l3 = lab("new sporophyte, 2n", TEAL)
        self.play(FadeOut(fl), FadeIn(l3), emb.animate.set_fill(TEAL, 0.95).set_stroke(TEAL), run_time=1.0)
        fl = l3
        a3 = trace(LENS_C + np.array([-0.9, 0.1, 0]), np.array([-6.5, 2.8, 0]), TEAL, -0.6)
        self.play(Create(a3), Indicate(cw.gf, color=WHITE, scale_factor=1.6), run_time=1.0)
        # one seed, three generations
        self.at("one seed holds three", lead=0.3)
        self.play(FadeOut(a3), FadeOut(fl), run_time=0.3)
        fin = lab2("one seed,", "three generations", TEXT, SLOT, 28)
        self.play(FadeIn(fin, shift=UP * 0.1), run_time=0.5)
        for m in (coat, food, emb):
            self.play(Indicate(m, scale_factor=1.06), run_time=0.7)
        self.finish()


def plant_obj():
    base = np.array([-0.8, -2.45, 0.0])
    stem = ParametricFunction(lambda t: base + np.array([0.12 * np.sin(t * 3.0), 5.4 * t, 0]), t_range=[0, 1, 0.01],
                              color=TEAL, stroke_width=7)
    g = VGroup()
    flowers = []
    # rosette
    for ang in (0.25, 0.7, 2.45, 2.9):
        e = Ellipse(width=1.3, height=0.36, stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.8)
        e.rotate(ang).move_to(base + np.array([np.cos(ang) * 0.6, 0.15 + np.sin(ang) * 0.3, 0]))
        g.add(e)
    g.add(stem)
    # branches
    spec = [((-0.8, 0.4), (-2.2, 1.0)), ((-0.78, 0.9), (0.6, 1.6)), ((-0.7, 1.7), (-2.0, 2.4)), ((-0.65, 2.1), (0.5, 2.8))]
    tips = []
    for (a, b) in spec:
        ln = Line([a[0], a[1], 0], [b[0], b[1], 0], stroke_color=TEAL, stroke_width=5)
        g.add(ln)
        tips.append(np.array([b[0], b[1], 0]))
    tips.append(base + np.array([0.12 * np.sin(3.0), 5.4, 0]))
    for tp in tips:
        f = VGroup(*[Ellipse(width=0.42, height=0.22, stroke_color=WHITE, stroke_width=1, fill_color=WHITE, fill_opacity=1)
                     .rotate(a).move_to(tp + np.array([np.cos(a) * 0.2, np.sin(a) * 0.2, 0])) for a in (0, PI / 2, PI, 3 * PI / 2)])
        f.add(Dot(tp, radius=0.07, color=LEAF))
        g.add(f)
        flowers.append(f)
    g.flowers = flowers
    g.tips = tips
    g.stem = stem
    return g


def flower_big(c=LENS_C):
    g = VGroup()
    for a in (0, PI / 2, PI, 3 * PI / 2):
        g.add(Ellipse(width=1.5, height=0.8, stroke_color=WHITE, stroke_width=2, fill_color=WHITE, fill_opacity=0.9)
              .rotate(a).move_to(c + np.array([np.cos(a) * 0.95, np.sin(a) * 0.95, 0])))
    pist = Ellipse(width=0.5, height=0.9, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=1).move_to(c)
    g.add(pist)
    anth = VGroup()
    for a in (PI / 4, 3 * PI / 4, 5 * PI / 4, 7 * PI / 4):
        d = np.array([np.cos(a), np.sin(a), 0])
        g.add(Line(c + d * 0.3, c + d * 0.62, stroke_color=LEAF, stroke_width=3))
        anth.add(Dot(c + d * 0.7, radius=0.13, color=GOLD))
    g.anth = anth
    g.add(anth)
    return g


class S09Flower(SpokenScene):
    def construct(self):
        cw = corner(male=True, ovule=True, grain=True, arrow=True)
        lg = legend2()
        rg = ridge()
        self.add(cw, lg, rg)
        spin_rider(self)
        pl = plant_obj()
        self.play(FadeIn(pl, shift=UP * 0.4), run_time=1.2)
        for i, f in enumerate(pl.flowers):
            bob(f, 0.04, 2.2, i * 0.6)
        # zoom into a flower
        ring_ = Circle(radius=0.5, stroke_color=WHITE, stroke_width=4).move_to(pl.tips[-1])
        ln = lens_obj()
        fb = flower_big()
        fb.set_z_index(2)
        self.at("shrink the female", lead=0.8)
        self.play(Create(ring_), run_time=0.4)
        self.play(GrowFromPoint(ln, pl.tips[-1]), run_time=1.0)
        self.play(FadeIn(fb, scale=0.7), run_time=0.7)
        breathe(fb, 0.015, 3.0)
        # pollen grain is the male gametophyte
        self.at("the pollen grain is", lead=0.3)
        self.play(Indicate(fb.anth, color=GOLD, scale_factor=1.8), run_time=0.9)
        gt = lab2("pollen grain =", "male gametophyte", GOLD)
        self.at("male gametophyte", lead=0.3)
        self.play(FadeIn(gt, shift=UP * 0.1), run_time=0.5)
        # Arabidopsis
        self.at("in arabidopsis", lead=0.0)
        al = VGroup(T("Arabidopsis", 34, TEAL, weight=BOLD), T("sporophyte", 34, TEAL, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([-4.9, -0.5, 0])
        self.play(FadeIn(al, shift=RIGHT * 0.2), run_time=0.6)
        # embryo sac inside the ovule
        self.at("embryo sac", lead=0.5)
        ov = ovule_obj()
        ov.set_z_index(2)
        self.play(FadeOut(gt), FadeOut(fb), FadeOut(ring_), run_time=0.4)
        dsac = DashedVMobject(Ellipse(width=2.4, height=1.8).move_to(LENS_C + np.array([0.5, 0, 0])), num_dashes=24).set_stroke(GOLD, 4)
        dsac.set_z_index(3)
        ol = lab("ovule", TEAL, LENS_C + np.array([0.0, 2.2, 0]), 28, bk=False)
        ol.set_z_index(3)
        sl = lab("embryo sac", GOLD, SLOT, 30)
        self.play(FadeIn(ov, scale=0.6), run_time=0.7)
        self.play(Create(dsac), FadeIn(sl, shift=UP * 0.1), run_time=0.8)
        self.at("inside the ovule", lead=0.1)
        self.play(FadeIn(ol, shift=DOWN * 0.1), run_time=0.4)
        # four megaspores
        self.at("gives four", lead=0.8)
        gm = gate_m(GATE_L, r=0.55, size=20)
        gm.set_z_index(8)
        self.play(FadeIn(gm, scale=0.7), run_time=0.5)
        outs = VGroup(*[micro_dot(GATE_L, 0.22) for _ in range(4)])
        zlist(outs, 4)
        self.add(outs)
        self.play(*[o.animate.move_to(np.array([x, LENS_C[1], 0])) for o, x in zip(outs, SPORE_X)], run_time=1.2)
        ml = lab("megaspores", GOLD, SLOT, 30)
        self.play(FadeOut(sl), FadeIn(ml), run_time=0.4)
        sl = ml
        for i, o in enumerate(outs):
            bob(o, 0.05, 2.0, i * 0.5)
        self.at("three degenerate", lead=0.3)
        self.play(*[o.animate.set_fill(GREY, 0.8).set_stroke(GREY) for o in outs[:3]], FadeOut(gm), run_time=0.7)
        self.play(*[FadeOut(o, scale=0.4) for o in outs[:3]], FadeOut(sl), FadeIn(lab("megaspore", GOLD, SLOT, 30)), run_time=0.8)
        self.finish()


# ---- the embryo sac frame (s10 to s13), in film coordinates
SA = np.array([5.4, -0.55, 0.0])
SK = 1.6


def fmap(p):
    p = np.array([p[0], p[1], 0.0])
    return SA + SK * (p - SA)


ST1 = {"E": (4.9, -0.55), "a": (4.0, -0.15), "b": (4.0, -0.95), "P1": (3.2, -0.55),
       "E2": (-4.1, -0.55), "a2": (-3.2, -0.15), "b2": (-3.2, -0.95), "P2": (-2.4, -0.55)}


def sac_oval(final):
    e = Ellipse(width=10.0, height=2.2, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.16).move_to([0.4, -0.55, 0])
    if final:
        e.scale(SK, about_point=SA)
    e.set_z_index(0)
    return e


def sac_final_world(polar=True, egg_wall=True, cell_wall=True, dim=True):
    """Final frame: only the egg end and the central cell are in view."""
    oval = sac_oval(True)
    egg_ = dotc(GOLD, 0.32, fmap(ST1["E"]))
    a = dotc(GOLD, 0.32, fmap(ST1["a"]))
    b = dotc(GOLD, 0.32, fmap(ST1["b"]))
    if dim:
        a.set_opacity(0.5)
        b.set_opacity(0.5)
    p1 = dotc(GOLD, 0.32, fmap((0.9, -0.55)))
    p2 = dotc(GOLD, 0.32, fmap((-0.1, -0.55)))
    for m in (egg_, a, b, p1, p2):
        m.set_z_index(4)
    ew = Circle(radius=0.62, stroke_color=WHITE, stroke_width=3, fill_opacity=0).move_to(fmap(ST1["E"]))
    cw_ = Ellipse(width=5.0, height=2.5, stroke_color=WHITE, stroke_width=3, fill_opacity=0).move_to([-2.6, -0.55, 0])
    ew.set_z_index(3)
    cw_.set_z_index(3)
    g = VGroup(oval, egg_, a, b, p1, p2, ew, cw_)
    g.oval, g.egg, g.a, g.b, g.p1, g.p2, g.ew, g.cw = oval, egg_, a, b, p1, p2, ew, cw_
    return g


class S10Nuclei(SpokenScene):
    def construct(self):
        cw = corner(male=True, ovule=True, grain=True, arrow=True)
        lg = legend2()
        self.add(cw, lg)
        spin_rider(self)
        oval = sac_oval(False)
        n0 = dotc(GOLD, 0.2, [0.4, -0.55, 0])
        n0.set_z_index(4)
        cnt = T("1 nucleus", 44, GOLD, weight=BOLD).move_to([1.6, 2.4, 0])
        self.play(FadeIn(oval, scale=0.8), FadeIn(n0, scale=0.5), FadeIn(cnt), run_time=0.8)
        bob(n0, 0.04, 2.0)

        def count(txt):
            return T(txt, 44, GOLD, weight=BOLD).move_to([1.6, 2.4, 0])
        # 1 -> 2
        self.at("divides", lead=0.2)
        n1 = dotc(GOLD, 0.2, n0.get_center())
        n1.set_z_index(4)
        self.add(n1)
        n0.clear_updaters()
        self.play(n0.animate.move_to([-3.6, -0.55, 0]), n1.animate.move_to([4.4, -0.55, 0]), Transform(cnt, count("2 nuclei")), run_time=1.0)
        # 2 -> 4
        self.at("times", lead=0.1)
        dots = [n0, n1]
        new = []
        for d in dots:
            c2 = dotc(GOLD, 0.2, d.get_center())
            c2.set_z_index(4)
            self.add(c2)
            new.append(c2)
        self.play(n0.animate.move_to([-3.6, -0.15, 0]), new[0].animate.move_to([-3.6, -0.95, 0]),
                  n1.animate.move_to([4.4, -0.15, 0]), new[1].animate.move_to([4.4, -0.95, 0]), Transform(cnt, count("4 nuclei")), run_time=1.0)
        # 4 -> 8
        self.at("making new cells", lead=0.2)
        four = [n0, new[0], n1, new[1]]
        tgt = [((-4.1, -0.55), (-3.2, -0.15)), ((-3.2, -0.95), (-2.4, -0.55)), ((4.9, -0.55), (4.0, -0.15)), ((4.0, -0.95), (3.2, -0.55))]
        twins = []
        for d in four:
            c2 = dotc(GOLD, 0.2, d.get_center())
            c2.set_z_index(4)
            self.add(c2)
            twins.append(c2)
        acts = []
        for d, t2, (p, q) in zip(four, twins, tgt):
            acts += [d.animate.move_to([p[0], p[1], 0]), t2.animate.move_to([q[0], q[1], 0])]
        self.play(*acts, Transform(cnt, count("8 nuclei")), run_time=1.0)
        allnuc = VGroup(*four, *twins)
        for i, d in enumerate(allnuc):
            bob(d, 0.04, 2.0, i * 0.3)
        # walls form: camera shows the egg end and the central cell
        self.at("then walls form", lead=0.2)
        # the two polar nuclei migrate to the middle
        polar_r, polar_l = twins[3], twins[1]        # at (3.2,-0.55) and (-2.4,-0.55)
        for d in (polar_r, polar_l):
            d.clear_updaters()
        self.play(polar_r.animate.move_to([0.9, -0.55, 0]), polar_l.animate.move_to([-0.1, -0.55, 0]), FadeOut(cnt), run_time=1.0)
        grp = VGroup(oval, *allnuc)
        for d in allnuc:
            d.clear_updaters()
        self.play(grp.animate.scale(SK, about_point=SA), run_time=1.6)
        fin = sac_final_world()
        # replace the scaled copies by the clean final objects (identical positions)
        self.remove(oval, *allnuc)
        self.add(fin.oval, fin.egg, fin.a, fin.b, fin.p1, fin.p2)
        cwall = fin.cw
        ewall = fin.ew
        self.play(Create(ewall), Create(cwall), run_time=1.4)
        self.at("the egg and", lead=0.1)
        gl = Circle(radius=0.85, stroke_color=GOLD, stroke_width=4).move_to(fmap(ST1["E"]))
        el = lab("egg", GOLD, [4.6, -2.1, 0], 30)
        self.play(Create(gl), FadeIn(el, shift=UP * 0.1), run_time=0.6)
        breathe(gl, 0.06, 1.8)
        self.at("a large central cell", lead=0.2)
        cl = lab("central cell", GOLD, [-2.6, -2.75, 0], 30)
        cg = Ellipse(width=5.4, height=2.9, stroke_color=GOLD, stroke_width=4).move_to([-2.6, -0.55, 0])
        self.play(Create(cg), FadeIn(cl, shift=UP * 0.1), run_time=0.7)
        breathe(cg, 0.015, 2.2)
        self.at("holding two nuclei", lead=0.1)
        self.play(Indicate(fin.p1, color=WHITE, scale_factor=1.5), Indicate(fin.p2, color=WHITE, scale_factor=1.5), run_time=1.0)
        bob(fin.p1, 0.04, 1.8)
        bob(fin.p2, 0.04, 1.8, 0.9)
        self.finish()


def sac_state(scene, labels=("egg", "central cell"), glow=False):
    fin = sac_final_world()
    cw = corner(male=True, ovule=True, grain=True, arrow=True)
    lg = legend2()
    scene.add(fin, cw, lg)
    out = [fin, cw, lg]
    if "egg" in labels:
        out.append(lab("egg", GOLD, [4.6, -2.1, 0], 30))
        scene.add(out[-1])
    if "central cell" in labels:
        out.append(lab("central cell", GOLD, [-2.6, -2.75, 0], 30))
        scene.add(out[-1])
    return fin, cw, lg, out


class S11Polar(SpokenScene):
    def construct(self):
        fin, cw, lg, out = sac_state(self)
        spin_rider(self)
        bob(fin.p1, 0.04, 1.8)
        bob(fin.p2, 0.04, 1.8, 0.9)
        # those two are the polar nuclei, both gold
        self.at("those two are", lead=0.2)
        pn = lab("polar nuclei", GOLD, [-1.6, 1.7, 0], 30)
        self.play(FadeIn(pn, shift=DOWN * 0.1), Indicate(fin.p1, color=WHITE, scale_factor=1.5), Indicate(fin.p2, color=WHITE, scale_factor=1.5), run_time=1.0)
        self.at("both are gold", lead=0.0)
        self.play(Indicate(fin.p1, color=GOLD, scale_factor=1.4), Indicate(fin.p2, color=GOLD, scale_factor=1.4), run_time=0.8)
        # they fuse before fertilization
        self.at("they fuse before", lead=0.4)
        fin.p1.clear_updaters()
        fin.p2.clear_updaters()
        gate = gate_f([-2.6, -0.55, 0], r=0.42)
        gate.set_z_index(8)
        self.play(FadeIn(gate, scale=0.6), run_time=0.5)
        self.play(fin.p1.animate.move_to([-2.6, -0.55, 0]), fin.p2.animate.move_to([-2.6, -0.55, 0]), run_time=1.4)
        nuc = dotc(TEAL, 0.32, [-2.6, -0.55, 0])
        nuc.set_z_index(6)
        self.remove(fin.p1, fin.p2)
        self.add(nuc)
        self.play(FadeOut(gate), FadeOut(pn), run_time=0.5)
        # fusion adds
        self.at("fusion adds", lead=0.3)
        eq = VGroup(T("n", 44, GOLD, weight=BOLD), T("+", 44, TEXT, weight=BOLD), T("n", 44, GOLD, weight=BOLD), T("=", 44, TEXT, weight=BOLD),
                    T("2n", 44, TEAL, weight=BOLD)).arrange(RIGHT, buff=0.28).move_to([0.4, 2.55, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.7)
        self.at("so the central cell is", lead=0.3)
        self.play(fin.cw.animate.set_stroke(TEAL, 6), pls(nuc, 1.4), run_time=1.0)
        bob(nuc, 0.04, 1.8)
        self.finish()


def sac_with_teal(scene, tube=False):
    fin, cw, lg, out = sac_state(scene, labels=())
    fin.remove(fin.p1, fin.p2)
    scene.remove(fin.p1, fin.p2)
    nuc = dotc(TEAL, 0.32, [-2.6, -0.55, 0])
    nuc.set_z_index(6)
    fin.cw.set_stroke(TEAL, 6)
    scene.add(nuc)
    return fin, cw, lg, nuc


class S12Double(SpokenScene):
    def construct(self):
        fin, cw, lg, nuc = sac_with_teal(self)
        spin_rider(self)
        bob(nuc, 0.04, 1.8)
        # a pollen tube brings two sperm
        tube_path = VMobject()
        tube_path.set_points_smoothly([np.array(p, float) for p in [(6.6, 3.4, 0), (5.7, 2.2, 0), (5.0, 1.0, 0), (4.7, 0.3, 0)]])
        tube_path.set_stroke(GOLD, 14)
        tube_path.set_z_index(5)
        self.at("a pollen tube", lead=0.0)
        self.play(Create(tube_path), run_time=1.3)
        s1 = sperm([4.75, 0.45, 0])
        s2 = sperm([5.0, 0.7, 0])
        zlist([s1, s2], 7)
        self.at("two sperm", lead=0.2)
        self.add(s1, s2)
        self.play(s1.animate.shift(DOWN * 0.15), s2.animate.shift(DOWN * 0.25), run_time=0.8)
        # one fuses with the egg
        self.at("one fuses with", lead=0.2)
        g1 = gate_f(fmap(ST1["E"]), r=0.42)
        g1.set_z_index(8)
        self.play(FadeIn(g1, scale=0.6), s1.animate.move_to(fmap(ST1["E"])), run_time=1.2)
        self.at("giving a teal", lead=0.2)
        zy = dotc(TEAL, 0.32, fmap(ST1["E"]))
        zy.set_z_index(6)
        self.remove(s1, fin.egg)
        self.add(zy)
        self.play(FadeOut(g1), run_time=0.4)
        zl = lab("zygote, 2n", TEAL, [4.6, -2.1, 0], 30)
        self.play(FadeIn(zl, shift=UP * 0.1), Indicate(zy, color=TEAL, scale_factor=1.4), run_time=0.8)
        # the other fuses with the central cell
        self.at("the other fuses", lead=0.3)
        path2 = VMobject()
        path2.set_points_smoothly([np.array(p, float) for p in [(5.0, 0.55, 0), (3.8, 0.7, 0), (1.5, 0.7, 0), (0.2, 0.3, 0), (-0.15, -0.55, 0)]])
        g2 = gate_f([-0.9, -0.55, 0], r=0.4)
        g2.set_z_index(8)
        self.play(FadeIn(g2, scale=0.6), nuc.animate.move_to([-1.8, -0.55, 0]), run_time=0.7)
        self.play(MoveAlongPath(s2, path2), run_time=2.8, rate_func=linear)
        self.play(pls(g2, 1.25), run_time=0.5)
        bob(zy, 0.04, 1.8)
        self.finish()


def sac_s13_start(scene):
    fin, cw, lg, nuc = sac_with_teal(scene)
    nuc.move_to([-1.8, -0.55, 0])
    zy = dotc(TEAL, 0.32, fmap(ST1["E"]))
    zy.set_z_index(6)
    scene.remove(fin.egg)
    scene.add(zy)
    g2 = gate_f([-0.9, -0.55, 0], r=0.4)
    g2.set_z_index(8)
    s2 = sperm([-0.15, -0.55, 0])
    s2.set_z_index(7)
    scene.add(g2, s2)
    return fin, cw, lg, nuc, zy, g2, s2


class S13Endosperm(SpokenScene):
    def construct(self):
        fin, cw, lg, nuc, zy, g2, s2 = sac_s13_start(self)
        spin_rider(self)
        bob(zy, 0.04, 1.8)
        self.at("fusion adds again", lead=0.1)
        nuc.clear_updaters()
        eq = VGroup(T("2n", 44, TEAL, weight=BOLD), T("+", 44, TEXT, weight=BOLD), T("n", 44, GOLD, weight=BOLD), T("=", 44, TEXT, weight=BOLD),
                    T("3n", 44, CORAL, weight=BOLD)).arrange(RIGHT, buff=0.28).move_to([0.4, 2.55, 0])
        self.play(nuc.animate.move_to([-0.9, -0.55, 0]), s2.animate.move_to([-0.9, -0.55, 0]), FadeIn(eq, shift=DOWN * 0.1), run_time=1.0)
        cn = dotc(CORAL, 0.34, [-0.9, -0.55, 0])
        cn.set_z_index(6)
        self.remove(nuc, s2)
        self.add(cn)
        self.play(FadeOut(g2), cn.animate.move_to([-2.6, -0.55, 0]), fin.cw.animate.set_stroke(CORAL, 6), run_time=1.0)
        self.at("the result is endosperm", lead=0.2)
        self.play(Transform(lg.coral, legend2(True).coral), run_time=0.7)
        self.at("a food tissue", lead=0.2)
        cells = VGroup()
        cpos = [(-4.3, 0.1), (-3.1, 0.1), (-1.9, 0.1), (-0.7, 0.1), (-3.7, -1.1), (-2.5, -1.1), (-1.3, -1.1)]
        for p in cpos:
            c = Circle(radius=0.55, stroke_color=WHITE, stroke_width=2, fill_color=CORAL, fill_opacity=0.5).move_to([p[0], p[1], 0])
            c.add(Dot(np.array([p[0], p[1], 0]), radius=0.14, color=CORAL))
            cells.add(c)
        zlist(cells, 5)
        self.play(FadeOut(fin.cw), LaggedStart(*[GrowFromPoint(c, np.array([-2.6, -0.55, 0])) for c in cells], lag_ratio=0.15), FadeOut(cn), run_time=1.6)
        el = lab("endosperm, 3n: a food tissue", CORAL, [-2.6, -2.75, 0], 30)
        self.play(FadeIn(el, shift=UP * 0.1), run_time=0.5)
        for i, c in enumerate(cells):
            bob(c, 0.03, 2.0, i * 0.4)
        self.at("three sets", lead=0.2)
        self.play(Indicate(eq[4], color=CORAL, scale_factor=1.4), run_time=0.8)
        self.at("that holds in", lead=0.2)
        self.play(FadeOut(eq), run_time=0.4)
        fn = VGroup(T("Arabidopsis and most", 28, TEXT), T("flowering plants, not all", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([3.3, 2.5, 0])
        self.play(FadeIn(fn, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


def icon_moss():
    g = VGroup()
    for x, h in [(-0.35, 0.7), (0.0, 1.0), (0.35, 0.6)]:
        g.add(Line([x, -0.5, 0], [x, -0.5 + h, 0], stroke_color=GOLD, stroke_width=5))
        g.add(Dot([x, -0.5 + h, 0], radius=0.09, color=GOLD))
        for i in range(2):
            g.add(leaf([x + 0.14, -0.4 + i * 0.3, 0], 0.5, 0.35, GOLD, 0.5))
    return g


def icon_fern():
    g = VGroup()
    pts = [np.array([-0.2 + 0.4 * t * t, -0.6 + 1.3 * t, 0]) for t in np.linspace(0, 1, 12)]
    vm = VMobject().set_points_smoothly(pts).set_stroke(TEAL, 4)
    g.add(vm)
    for t in np.linspace(0.15, 0.95, 6):
        p = np.array([-0.2 + 0.4 * t * t, -0.6 + 1.3 * t, 0])
        L = 0.7 * (1 - t) + 0.2
        for s in (1, -1):
            g.add(leaf(p + np.array([s * L / 2, 0.05, 0]), s * 0.35, L, TEAL, 0.7))
    return g


def icon_pine():
    g = VGroup()
    g.add(Rectangle(width=0.14, height=0.5, stroke_width=0, fill_color="#8A6240", fill_opacity=1).move_to([0, -0.65, 0]))
    for w, y in [(1.0, -0.35), (0.8, 0.0), (0.55, 0.35)]:
        g.add(Polygon([-w / 2, y, 0], [w / 2, y, 0], [0, y + 0.55, 0], stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=1))
    return g


def icon_flower():
    g = VGroup(Line([0, -0.75, 0], [0, 0, 0], stroke_color=TEAL, stroke_width=5))
    for a in (0, PI / 2, PI, 3 * PI / 2):
        g.add(Ellipse(width=0.5, height=0.28, stroke_color=WHITE, stroke_width=1, fill_color=WHITE, fill_opacity=1)
              .rotate(a).move_to([np.cos(a) * 0.28, np.sin(a) * 0.28, 0]))
    g.add(Dot([0, 0, 0], radius=0.09, color=LEAF))
    return g.shift(UP * 0.2)


class S14Rule(SpokenScene):
    def construct(self):
        small = corner(male=True, ovule=True, grain=True, arrow=True)
        lg = legend2(True)
        self.add(small, lg)
        rd, th = spin_rider(self)
        pn = panel(C0, RA, RB)
        big = corner(male=True, ovule=True, grain=True, arrow=True, c=C0, ra=RA, rb=RB, w=10)
        # the wheel pulls back to full size
        self.at("every label came", lead=0.0)
        self.remove(rd)
        self.play(FadeIn(pn), Transform(small, big), run_time=1.5)
        self.remove(small)
        self.add(big)
        rd2 = rider(C0, RA, RB, M, F, th, r=0.3)
        self.add(rd2)
        gm = gate_m(P(C0, RA, RB, M))
        gf = gate_f(P(C0, RA, RB, F))
        # lanes' circles from `big` are plain gates; put the labelled gates on top
        for m in (big.gm, big.gf):
            m.set_opacity(0)
        self.play(FadeIn(gm, scale=0.7), FadeIn(gf, scale=0.7), run_time=0.4)
        self.at("same two gates", lead=0.3)
        self.play(pls(gm, 1.25), pls(gf, 1.25), run_time=1.0)
        sp = body_box("sporophyte", TEAL, 28, P(C0, RA, RB, 90))
        self.play(FadeIn(sp, scale=0.9), run_time=0.5)
        # meiosis halves, fusion adds
        self.at("meiosis halves the sets", lead=0.3)
        self.play(pls(gm, 1.3), gm[0].animate.set_stroke(YELLOW, 8), run_time=1.0)
        self.at("and fusion adds them", lead=0.3)
        self.play(gm[0].animate.set_stroke(WHITE, 5), pls(gf, 1.3), gf[0].animate.set_stroke(YELLOW, 8), run_time=1.0)
        self.play(gf[0].animate.set_stroke(WHITE, 5), run_time=0.4)
        # size and place changed: the four icons
        self.at("size and place changed", lead=0.3)
        specs = [(icon_moss(), "moss", GOLD, (-5.9, 2.5), 145), (icon_flower(), "flower", TEXT, (5.9, 2.5), 35),
                 (icon_fern(), "fern", TEAL, (-5.9, -0.8), -155), (icon_pine(), "pine", TEAL, (5.9, 0.0), -30)]
        icons = VGroup()
        for ic, nm, col, pos, ang in specs:
            ic.scale(1.15).move_to([pos[0], pos[1], 0])
            tx = T(nm, 28, col, weight=BOLD).next_to(ic, DOWN, buff=0.12)
            link = DashedLine(ic.get_center() + (RIGHT if pos[0] < 0 else LEFT) * 0.7, P(C0, RA, RB, ang),
                              stroke_color=RING, stroke_width=3, dash_length=0.12)
            icons.add(VGroup(ic, tx, link))
        self.play(LaggedStart(*[FadeIn(g, scale=0.8) for g in icons], lag_ratio=0.45), run_time=2.2)
        # meiosis starts each gametophyte, fertilization each sporophyte
        self.at("meiosis still starts", lead=0.3)
        self.play(Indicate(gm[0], color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.at("and fertilization each", lead=0.2)
        self.play(Indicate(gf[0], color=YELLOW, scale_factor=1.2), run_time=1.0)
        # extra fusions add the endosperm
        self.at("extra fusions add", lead=0.3)
        gp = lane_pt(C0, RA, RB, 1.0, 0.4)
        gate_c = gate_f(gp, r=0.32)
        gate_c[1].scale(0.6)
        br = VMobject()
        br.set_points_smoothly([gp + np.array([0.25, -0.05, 0]), np.array([2.5, -2.75, 0]), np.array([3.1, -2.75, 0])])
        br.set_stroke(CORAL, 8)
        cdot = dotc(CORAL, 0.24, [3.1, -2.75, 0])
        self.play(FadeIn(gate_c, scale=0.6), run_time=0.5)
        self.play(Create(br), FadeIn(cdot, scale=0.5), run_time=1.0)
        cl = T("endosperm 3n", 28, CORAL, weight=BOLD).move_to([5.15, -2.75, 0])
        self.play(FadeIn(cl, shift=LEFT * 0.1), run_time=0.5)
        # the female gametophyte now stays inside the ovule
        self.at("the female gametophyte now", lead=0.3)
        fgl = VGroup(T("female", 26, GOLD, weight=BOLD), T("gametophyte", 26, GOLD, weight=BOLD)).arrange(DOWN, buff=0.05).move_to([-0.7, -1.9, 0])
        self.play(big.ov.animate.set_stroke(WHITE, 8), FadeIn(fgl, shift=UP * 0.1), run_time=1.0)
        self.at("inside the ovule", lead=0.3)
        ovl = T("ovule", 28, TEAL, weight=BOLD).move_to([1.5, -1.8, 0])
        self.play(big.ov.animate.set_stroke(TEAL, 8), FadeIn(ovl, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


class S15End(EndCard):
    LINE = "Same two gates; the female gametophyte now stays inside the ovule."
