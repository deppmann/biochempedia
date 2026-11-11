"""Where the Reader Works — protein-sorting explainer.

COLOR MAP
  GOLD/YELLOW = address or signal sequence
  TEAL        = SRP and SRP receptor
  BLUE        = readers that act after release (TOM, PEX5)
  INDIGO      = ER membrane, lumen, and Sec61
  ORANGE      = mitochondrion
  MAGENTA     = peroxisome
  PINK        = GTP
  RED         = cutting, blocked, or cannot enter
  GREY/WHITE  = structure, chain, and neutral labels
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

INDIGO = "#7779E8"
ORANGE = "#F29E4C"
MAGENTA = "#D96BB0"
PINK = "#F0A3C4"
GOLD = YELLOW
ER_Y = -2.15
RIBO_POS = np.array([-2.25, 0.9, 0.0])


def ambient(seed=1):
    """Visible cytosol specks with slow continuous drift."""
    rng = random.Random(seed)
    dots = VGroup()
    for _ in range(46):
        d = Dot([rng.uniform(-6.25, 6.25), rng.uniform(-3.35, 3.35), 0],
                radius=rng.uniform(0.08, 0.16), color=GREY)
        d.set_opacity(rng.uniform(0.25, 0.48))
        d.v = np.array([rng.uniform(-0.8, 0.8), rng.uniform(0.48, 0.88), 0])
        def drift(m, dt):
            m.shift(m.v * dt)
            if m.get_y() > 3.55: m.shift(DOWN * 7.0)
            if m.get_x() > 6.5: m.shift(LEFT * 13.0)
            if m.get_x() < -6.5: m.shift(RIGHT * 13.0)
        d.add_updater(drift)
        dots.add(d)
    dots.set_z_index(-20)
    return dots


def bead_chain(n=13, gold=4, r=0.14, vertical=False, gold_at_end=False):
    b = VGroup(*[Circle(radius=r, stroke_width=1.5, stroke_color=BG,
                        fill_color=TEXT, fill_opacity=1) for _ in range(n)])
    b.arrange(DOWN if vertical else RIGHT, buff=0.035)
    ids = range(n-gold, n) if gold_at_end else range(gold)
    for i in ids: b[i].set_fill(GOLD)
    return b


def ribosome(pos=RIBO_POS, scale=1.0, cutaway=False):
    big = Ellipse(width=3.15, height=2.15, stroke_color=GREY, stroke_width=4,
                  fill_color=GREY, fill_opacity=0.26)
    small = Ellipse(width=2.25, height=1.15, stroke_color=GREY, stroke_width=4,
                    fill_color=GREY, fill_opacity=0.32).shift(UP * 1.25 + LEFT * 0.25)
    tunnel = ArcBetweenPoints(np.array([-0.45, 1.2, 0]), np.array([0.72, -0.96, 0]),
                              angle=-0.55, color=BG, stroke_width=15)
    mouth = Dot([0.72, -0.96, 0], radius=0.13, color=BG)
    g = VGroup(big, small, tunnel, mouth).scale(scale).move_to(pos)
    if cutaway:
        big.set_fill(GREY, 0.12)
        tunnel.set_stroke(GOLD, width=10, opacity=0.5)
    return g


def er_world(opacity=1.0):
    lumen = Rectangle(width=13.4, height=1.55, stroke_width=0,
                      fill_color=INDIGO, fill_opacity=0.13 * opacity).move_to([0, -3.02, 0])
    membrane = VGroup(
        RoundedRectangle(width=7.0, height=.32, corner_radius=.12, stroke_color=INDIGO,
                         fill_color=INDIGO, fill_opacity=.45, stroke_width=3).move_to([-3.2, ER_Y, 0]),
        RoundedRectangle(width=4.55, height=.32, corner_radius=.12, stroke_color=INDIGO,
                         fill_color=INDIGO, fill_opacity=.45, stroke_width=3).move_to([4.02, ER_Y, 0]))
    sec = VGroup(*[RoundedRectangle(width=.35, height=.72, corner_radius=.1,
                                    stroke_color=INDIGO, fill_color=INDIGO, fill_opacity=.75,
                                    stroke_width=3).move_to([x, ER_Y, 0]) for x in (.55, 1.35)])
    lab = T("ER lumen", 28, INDIGO).move_to([-4.9, -3.05, 0])
    g = VGroup(lumen, membrane, sec, lab).set_opacity(opacity)
    return g


def mitochondrion(pos=(5.45, .15, 0), scale=1.0):
    outer = RoundedRectangle(width=3.0, height=3.55, corner_radius=.9, stroke_color=ORANGE,
                             stroke_width=4, fill_color=ORANGE, fill_opacity=.08)
    inner = RoundedRectangle(width=2.25, height=2.8, corner_radius=.65, stroke_color=ORANGE,
                             stroke_width=3, stroke_opacity=.65)
    return VGroup(outer, inner).scale(scale).move_to(pos)


def peroxisome(pos=(-5.65, 2.55, 0), scale=1.0):
    return Circle(radius=.7, stroke_color=MAGENTA, stroke_width=4,
                  fill_color=MAGENTA, fill_opacity=.1).scale(scale).move_to(pos)


def gel(scale=1.0, pos=(-4.9, 2.05, 0), labels=True):
    box = RoundedRectangle(width=3.1, height=2.35, corner_radius=.18,
                           stroke_color=GREY, stroke_width=2, fill_color=BG, fill_opacity=.9)
    lane1 = Rectangle(width=.72, height=1.52, stroke_color=GREY, stroke_width=1).move_to([-0.65, -.1, 0])
    lane2 = lane1.copy().move_to([.65, -.1, 0])
    hi = RoundedRectangle(width=.58, height=.18, corner_radius=.06, stroke_width=0,
                          fill_color=TEXT, fill_opacity=1).move_to([-.65, .28, 0])
    lo = hi.copy().move_to([.65, -.12, 0])
    bracket = BraceBetweenPoints(np.array([-.08, -.12, 0]), np.array([-.08, .28, 0]),
                                 direction=RIGHT, color=GOLD)
    q = T("?", 34, GOLD, weight=BOLD).next_to(bracket, RIGHT, buff=.06)
    parts = [box, lane1, lane2, hi, lo, bracket, q]
    if labels:
        a = T("test tube", 28, TEXT).move_to([-.65, .94, 0])
        b = T("cells", 28, TEXT).move_to([.65, .94, 0])
        parts += [a, b]
    return VGroup(*parts).scale(scale).move_to(pos)


def world(seed=2, er_opacity=1.0, labels=True):
    r = ribosome()
    e = er_world(er_opacity)
    m = mitochondrion()
    p = peroxisome()
    parts = [ambient(seed), e, m, p, r]
    if labels:
        parts += [T("exit tunnel", 28, TEXT).move_to([.45, .30, 0]),
                  T("schematic, not to scale", 22, TEXT).move_to([5.05, -3.48, 0])]
    return VGroup(*parts)


def reveal_chain(scene, chain, run_time=1.5):
    scene.play(LaggedStart(*[FadeIn(x, scale=.45) for x in chain], lag_ratio=.12), run_time=run_time)


def question_card():
    return T("Membranes added after release: does it get in?", 36, TEXT, weight=BOLD).move_to([0, 3.25, 0])


def padlock():
    shackle = Arc(radius=.22, start_angle=0, angle=PI, color=RED, stroke_width=5)
    body = RoundedRectangle(width=.52, height=.42, corner_radius=.07, stroke_color=RED,
                            fill_color=RED, fill_opacity=.25, stroke_width=4).next_to(shackle, DOWN, buff=-.04)
    return VGroup(shackle, body)


def dark_chip(text, color, size=28):
    """Readable chip that masks any compartment line behind its label."""
    c = chip(text, color, size)
    c[0].set_fill(BG, opacity=.92)
    return c




# ====================== CHAPTER 2 ADDITIONS ======================
LIME = "#9BDB3C"
CYAN = "#4FD6E6"
GLASS = "#A9BDD4"
LIQ = "#1B2638"
TCX, THW, TTOP, TBOT, LTOP = -3.1, 2.95, 3.0, -3.7, 2.3
GXC = 4.2
LANE_X = [2.6, 4.2, 5.8]
BAND_Y = 1.3
V_A = [(-5.3, -0.9, 0), (-2.4, 1.2, 0), (-0.95, -0.4, 0), (-5.2, -2.4, 0), (-1.3, -2.3, 0)]
V_B = [(-2.2, 1.5, 0), (-2.2, -1.2, 0), (-0.85, 0.1, 0)]
INSET_POS = [-5.3, 3.05, 0]


def schem():
    return T("schematic, not to scale", 22, TEXT).move_to([5.05, -3.48, 0])


def bob(m, amp=.1, w=.7, ph=0.0):
    ax, ay = amp if isinstance(amp, tuple) else (amp, amp)
    m._bt = 0.0
    m._bo = np.zeros(3)

    def up(mm, dt):
        mm._bt += dt
        o = np.array([ax * np.sin(w * mm._bt + ph), ay * np.cos(.83 * w * mm._bt + 1.7 * ph), 0.0])
        mm.shift(o - mm._bo)
        mm._bo = o
    m.add_updater(up)
    return m


def specks(x0, x1, y0, y1, n=22, seed=1, vy=.35):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot([rng.uniform(x0, x1), rng.uniform(y0, y1), 0], radius=rng.uniform(.04, .09), color=GREY)
        d.set_opacity(rng.uniform(.3, .55))
        d.v = np.array([rng.uniform(-.25, .25), rng.uniform(.15, vy), 0])

        def drift(m, dt, x0=x0, x1=x1, y0=y0, y1=y1):
            m.shift(m.v * dt)
            if m.get_y() > y1: m.shift(DOWN * (y1 - y0))
            if m.get_x() > x1: m.shift(LEFT * (x1 - x0))
            if m.get_x() < x0: m.shift(RIGHT * (x1 - x0))
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-8)
    return g


def tube_pts(top):
    r = 1.4
    L, R = TCX - THW, TCX + THW
    pts = [[L, top, 0], [L, TBOT + r, 0]]
    for a in np.linspace(PI, 1.5 * PI, 14)[1:]:
        pts.append([L + r + r * np.cos(a), TBOT + r + r * np.sin(a), 0])
    for a in np.linspace(1.5 * PI, 2 * PI, 14)[1:]:
        pts.append([R - r + r * np.cos(a), TBOT + r + r * np.sin(a), 0])
    pts.append([R, top, 0])
    return pts


def tube_group():
    liq = Polygon(*tube_pts(LTOP), fill_color=LIQ, fill_opacity=.9, stroke_width=0).set_z_index(-10)
    glass = VMobject(stroke_color=GLASS, stroke_width=5).set_points_as_corners(tube_pts(TTOP)).set_z_index(-9)
    surf = Line([TCX - THW, LTOP, 0], [TCX + THW, LTOP, 0], stroke_color=GLASS, stroke_width=2,
                stroke_opacity=.6).set_z_index(-9)
    return VGroup(liq, glass, surf)


def gel_group():
    box = RoundedRectangle(width=5.1, height=5.7, corner_radius=.18, stroke_color=GREY, stroke_width=2,
                           fill_color=BG, fill_opacity=.95).move_to([GXC, -.1, 0])
    lanes = VGroup(*[Rectangle(width=1.3, height=3.95, stroke_color=GREY, stroke_width=1.5).move_to([x, .475, 0])
                     for x in LANE_X])
    labs = VGroup(*[T(t, 22, TEXT).move_to([x, -2.15, 0]) for t, x in
                    zip(["no\nprotease", "+\nprotease", "+ protease\n+ detergent"], LANE_X)])
    return VGroup(box, lanes, labs)


def band(lane, y=BAND_Y, color=TEXT):
    return RoundedRectangle(width=1.0, height=.26, corner_radius=.07, stroke_width=0,
                            fill_color=color, fill_opacity=1).move_to([LANE_X[lane], y, 0])


def bead(r, color=TEXT):
    return Circle(radius=r, stroke_width=1.2, stroke_color=BG, fill_color=color, fill_opacity=1)


def wavy(a, b, n=8, r=.11, amp=.12, gold=0, gold_far=True, k=1.5):
    a = np.array(a, float); b = np.array(b, float)
    d = b - a; u = d / np.linalg.norm(d); p = np.array([-u[1], u[0], 0])
    g = VGroup()
    for i in range(n):
        t = i / (n - 1)
        c = bead(r)
        if gold and ((gold_far and i >= n - gold) or (not gold_far and i < gold)):
            c.set_fill(GOLD)
        g.add(c.move_to(a + d * t + p * amp * np.sin(2 * PI * k * t)))
    return g


def coil(center, n=12, r=.1, R0=.5, turns=1.8, gold=0):
    center = np.array(center, float)
    g = VGroup()
    for i in range(n):
        t = i / (n - 1)
        ang = 2 * PI * turns * t
        rad = R0 * (1 - .8 * t)
        c = bead(r)
        if i < gold: c.set_fill(GOLD)
        g.add(c.move_to(center + rad * np.array([np.cos(ang), np.sin(ang), 0])))
    return g


def feed(scene, beads, mouth, rt=1.4, lag=.16):
    slots = [b.get_center().copy() for b in beads]
    for b in beads:
        b.move_to(mouth)
        b.set_opacity(0)
    scene.add(*beads)
    order = list(zip(beads, slots))[::-1]
    scene.play(LaggedStart(*[b.animate.move_to(s).set_opacity(1) for b, s in order], lag_ratio=lag), run_time=rt)


def scatter(beads, rt=1.5):
    return LaggedStart(*[b.animate.shift(np.array([random.uniform(-.8, .8), random.uniform(-.8, .8), 0])).set_opacity(0)
                         for b in beads], lag_ratio=.1, run_time=rt)


def cutter(pos, s=1.0, ph=0.0, amp=.3):
    pos = [pos[0], pos[1], 0]
    body = Sector(radius=.3 * s, angle=TAU * .8, start_angle=.5, stroke_width=0, fill_color=LIME, fill_opacity=1)
    eye = Dot([0, .12 * s, 0], radius=.035 * s, color=BG)
    g = VGroup(body, eye).move_to(pos)
    return bob(g, amp, .9, ph)


def vesicle(pos, r=.65, sw=5, ph=0.0):
    c = Circle(radius=r, stroke_color=INDIGO, stroke_width=sw, fill_color=INDIGO, fill_opacity=.14).move_to([pos[0], pos[1], 0])
    return bob(c, .08, .6, ph)


def ves_group(pos_list):
    return VGroup(*[vesicle(p, ph=i * 1.3) for i, p in enumerate(pos_list)])


def tube_base(seed=1):
    return tube_group(), specks(-5.7, -.5, -3.2, 2.1, 24, seed)


def folded_ball(pos, r=.6):
    b = Circle(radius=r, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.88)
    f1 = Arc(radius=r * .55, start_angle=.4, angle=2.4, color=BG, stroke_width=3)
    f2 = Arc(radius=r * .4, start_angle=3.6, angle=2.2, color=BG, stroke_width=3)
    return VGroup(b, f1, f2).move_to([pos[0], pos[1], 0])


def rules_lines(size=38):
    l1 = VGroup(T("GOT IN?", size, TEXT, weight=BOLD), T("protection", size, INDIGO, weight=BOLD),
                T("test", size, TEXT, weight=BOLD)).arrange(RIGHT, buff=.18)
    l2 = VGroup(T("WHAT SENT IT?", size, TEXT, weight=BOLD), T("move and delete", size, GOLD, weight=BOLD)
                ).arrange(RIGHT, buff=.18)
    return VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=.2)


def rules_parked():
    return rules_lines().scale(.62).move_to([3.85, 3.15, 0])


def thin(g, w=1.6):
    for m in g.get_family():
        try:
            if m.get_stroke_width() > w: m.set_stroke(width=w)
        except Exception:
            pass
    return g


def inset_lite():
    tg = tube_group()
    ves = VGroup(*[Circle(radius=.65, stroke_color=INDIGO, stroke_width=5, fill_color=INDIGO,
                          fill_opacity=.14).move_to(p) for p in V_B])
    cl = coil(V_B[0], 10, .07, .35, 1.5)
    gb = gel_group()[:2]
    bands = VGroup(band(0), band(1, .95))
    g = VGroup(tg, ves, cl, gb, bands)
    g.scale(.2).move_to(INSET_POS)
    thin(g, 1.4)
    tg[0].set_stroke(width=0)
    g.ves = ves[0]
    return g


def cell_world(seed=9, ribo=False, mito=True, perox=True, perox_pos=(-5.45, .6, 0), perox_scale=1.0):
    parts = [ambient(seed)]
    er = er_world(.3)
    er.remove(er[3])
    parts.append(er)
    if mito: parts.append(bob(mitochondrion(), .08, .5))
    if perox: parts.append(bob(peroxisome(perox_pos, perox_scale), .08, .6, 1.0))
    if ribo: parts.append(ribosome())
    return VGroup(*parts)


def chrome(scene, necessary=False, sufficient=True):
    ins = inset_lite()
    rules = rules_parked()
    scene.add(ins, rules, schem())
    out = {"ins": ins, "rules": rules}
    if sufficient:
        out["suf"] = T("sufficient", 28, GOLD, weight=BOLD).move_to([2.8, 2.3, 0]); scene.add(out["suf"])
    if necessary:
        out["nec"] = T("necessary", 28, GOLD, weight=BOLD).move_to([5.2, 2.3, 0]); scene.add(out["nec"])
    return out


def animal(kind):
    st = dict(stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=.15)
    head = Circle(radius=.26, **st)
    if kind == "rabbit":
        ears = VGroup(*[Ellipse(width=.14, height=.5, **st).move_to([s * .1, .42, 0]) for s in (-1, 1)])
    elif kind == "dog":
        ears = VGroup(*[Ellipse(width=.16, height=.36, **st).rotate(s * .4).move_to([s * .3, .05, 0]) for s in (-1, 1)])
    else:
        ears = VGroup(*[Circle(radius=.12, **st).move_to([s * .2, .25, 0]) for s in (-1, 1)])
    eyes = VGroup(Dot([-.09, .03, 0], radius=.025, color=TEXT), Dot([.09, .03, 0], radius=.025, color=TEXT))
    return VGroup(ears, head, eyes)


def eraser(pos):
    return RoundedRectangle(width=.45, height=.9, corner_radius=.1, stroke_width=0, fill_color=RED,
                            fill_opacity=.9).rotate(-.4).move_to(pos)


# ---------------- scenes ----------------
class S00Link(SpokenScene):
    def construct(self):
        amb = ambient(30)
        er = er_world(1)
        mito = bob(mitochondrion(), .08, .5)
        per = bob(peroxisome((-5.45, .6, 0)), .08, .6, 1.0)
        rib = ribosome()
        sch = schem()
        self.add(amb)
        self.play(LaggedStart(FadeIn(er, shift=UP * .25), FadeIn(mito, shift=LEFT * .2), FadeIn(per, shift=DOWN * .2),
                              FadeIn(rib, scale=.9), FadeIn(sch), lag_ratio=.2), run_time=1.6)
        ch = bead_chain(9, 4, r=.15, vertical=True).move_to([-.82, -.3, 0])
        reveal_chain(self, ch, 1.4)
        self.at("address")
        addr = T("address", 32, GOLD, weight=BOLD).move_to([.7, .55, 0])
        self.play(FadeIn(addr), Indicate(VGroup(*ch[:4]), color=GOLD), run_time=.9)
        self.at("went inside")
        q1 = T("?", 64, TEXT, weight=BOLD).move_to([2.6, -2.9, 0])
        self.play(FadeOut(addr), ch.animate.shift(DOWN * 1.2), GrowFromCenter(q1), run_time=1.5)
        self.at("which stretch")
        q2 = T("?", 64, TEXT, weight=BOLD).move_to([.45, -.7, 0])
        self.play(Indicate(VGroup(*ch[:4]), color=GOLD, scale_factor=1.5), GrowFromCenter(q2), run_time=1.2)
        self.play(Indicate(VGroup(*ch[:4]), color=GOLD, scale_factor=1.5), run_time=1.0)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Protein sorting"
    TITLE = "How Do You Know It Went In?"


def s02_end_state():
    tg, sp = tube_base(2)
    ves = ves_group(V_A)
    rib = bob(ribosome(pos=(-4.2, .9, 0), scale=.34), .05, .7)
    m = rib[3].get_center()
    c1 = wavy(m + np.array([.15, -.1, 0]), m + np.array([1.7, -1.2, 0]), 9, .1, .1, gold=3).move_to([-3.1, -2.2, 0])
    c2 = wavy(m + np.array([.15, -.1, 0]), m + np.array([1.7, -1.2, 0]), 9, .1, .1, gold=3)
    for i, c in enumerate((c1, c2)): bob(c, .05, .6, i)
    cut = VGroup(*[cutter(p, .9, i, .3) for i, p in enumerate([(-4.9, 1.9), (-3.7, .3), (-1.2, 1.0), (-2.2, -1.4)])])
    return tg, sp, ves, rib, c1, c2, cut


class S02Tube(SpokenScene):
    def construct(self):
        tg, sp = tube_base(2)
        gl = gel_group()
        self.add(schem())
        self.play(Create(tg[1]), FadeIn(tg[0]), FadeIn(tg[2]), run_time=1.6)
        self.add(sp)
        self.play(FadeIn(gl), run_time=1.1)
        self.at("make the protein")
        rib = bob(ribosome(pos=(-4.2, .9, 0), scale=.34), .05, .7)
        self.play(FadeIn(rib, scale=.8), run_time=.6)
        m = rib[3].get_center()
        c1 = wavy(m + np.array([.15, -.1, 0]), m + np.array([1.7, -1.2, 0]), 9, .1, .1, gold=3)
        feed(self, c1, m, 1.3)
        self.at("also holds")
        ves = ves_group(V_A)
        self.play(LaggedStart(*[FadeIn(v, scale=.5) for v in ves], lag_ratio=.25), run_time=1.4)
        lab = T("microsomes (ER vesicles)", 28, INDIGO).move_to([TCX, 2.75, 0])
        self.play(FadeIn(lab), c1.animate.move_to([-3.1, -2.2, 0]), run_time=.8)
        bob(c1, .05, .6, 0)
        self.at("sealed vesicles")
        c2 = wavy(m + np.array([.15, -.1, 0]), m + np.array([1.7, -1.2, 0]), 9, .1, .1, gold=3)
        feed(self, c2, m, 1.3)
        bob(c2, .05, .6, 1)
        self.at("membrane", nth=0)
        self.play(FadeOut(lab), Indicate(ves, color=INDIGO), run_time=1.0)
        self.at("then add a protease")
        pip = Polygon([-.18, .55, 0], [.18, .55, 0], [.06, -.5, 0], [-.06, -.5, 0], fill_color=LIME, fill_opacity=.9,
                      stroke_color=LIME, stroke_width=2).move_to([-3.1, 3.9, 0])
        self.play(pip.animate.move_to([-3.1, 2.55, 0]), run_time=1.0)
        self.at("protease")
        spots = [(-4.9, 1.9, 0), (-3.7, .3, 0), (-1.2, 1.0, 0), (-2.2, -1.4, 0)]
        cut = VGroup(*[cutter((-3.1, 2.2), .9, i, .3) for i in range(4)])
        for c in cut: c.set_opacity(0)
        self.add(cut)
        plab = T("protease", 28, LIME).move_to([-4.6, 2.65, 0])
        self.play(*[c.animate.move_to(p).set_opacity(1) for c, p in zip(cut, spots)], FadeOut(pip, shift=UP),
                  FadeIn(plab), run_time=1.6)
        self.at("chews up")
        self.play(*[Indicate(c, scale_factor=1.3, color=LIME) for c in cut], run_time=1.2)
        self.finish()


class S03Shield(SpokenScene):
    def construct(self):
        tg, sp, ves, rib, c1, c2, cut = s02_end_state()
        old = VGroup(tg, sp, ves, rib, c1, c2, cut)
        gl = gel_group()
        self.add(old, gl, schem())
        C = np.array([-3.0, .1, 0])
        big = Circle(radius=2.4, stroke_color=INDIGO, stroke_width=6, fill_color=INDIGO, fill_opacity=.12).move_to(C)
        ins = coil(C, 16, .15, 1.2, 2.2)
        out = wavy((-4.3, -3.25, 0), (-1.7, -3.25, 0), 11, .14, .12)
        bob(ins, .05, .6); bob(out, .06, .6, 1)
        sp2 = specks(-6.4, .3, -3.6, 3.4, 16, 3)
        cs = [cutter(p, 1.6, i, .15) for i, p in enumerate([(-6.25, .1), (-5.4, 2.5), (-.4, 1.6), (-1.5, -2.8)])]
        new = VGroup(big, ins, out, sp2, *cs)
        self.play(FadeOut(old, scale=1.6), FadeIn(new, scale=.6), run_time=1.3)
        self.at("cannot cross")
        x1 = Cross(Square(.3), stroke_color=RED, stroke_width=8).move_to([-5.4, .1, 0])
        x2 = Cross(Square(.3), stroke_color=RED, stroke_width=8).move_to([-4.85, 2.05, 0])
        lab = T("cannot\ncross", 28, RED).move_to([-6.0, -2.1, 0])
        self.play(cs[0].animate.shift(RIGHT * .35), cs[1].animate.shift(RIGHT * .3 + DOWN * .3), FadeIn(x1), FadeIn(x2),
                  FadeIn(lab), run_time=.8)
        self.play(cs[0].animate.shift(LEFT * .3), cs[1].animate.shift(LEFT * .3 + UP * .3), run_time=.8)
        self.play(Indicate(big, color=INDIGO), run_time=1.0)
        self.at("a chain outside")
        self.play(Indicate(out), cs[3].animate.move_to([-3.4, -2.8, 0]), cs[2].animate.move_to([-1.3, -2.7, 0]),
                  run_time=1.6)
        self.at("chewed up")
        self.play(scatter(out, 1.6), FadeOut(x1), FadeOut(x2), FadeOut(lab))
        self.at("a chain inside")
        self.play(Indicate(ins, color=WHITE), run_time=.9)
        self.at("shielded")
        halo = Circle(radius=2.4, stroke_color=INDIGO, stroke_width=16, stroke_opacity=.5).move_to(C)
        self.play(FadeIn(halo), run_time=.7)
        self.at("band survives")
        b1 = band(0)
        self.play(FadeIn(b1), run_time=.5)
        b2 = band(1, 3.0)
        self.add(b2)
        self.play(b2.animate.move_to([LANE_X[1], BAND_Y, 0]), run_time=.9)
        self.finish()


def s03_end_gel():
    return VGroup(gel_group(), band(0), band(1))


class S04Detergent(SpokenScene):
    def construct(self):
        C = np.array([-3.0, .1, 0])
        big = Circle(radius=2.4, stroke_color=INDIGO, stroke_width=6, fill_color=INDIGO, fill_opacity=.12).move_to(C)
        ins = coil(C, 16, .15, 1.2, 2.2)
        cs = [cutter(p, 1.6, i, .15) for i, p in enumerate([(-6.25, .1), (-5.4, 2.5), (-1.3, -2.7), (-3.4, -2.8)])]
        old = VGroup(big, ins, *cs)
        gl = s03_end_gel()
        self.add(old, gl, schem())
        tg, sp = tube_base(4)
        ves = ves_group(V_A)
        cl = coil(V_A[1], 10, .06, .38, 1.5)
        cut = [cutter(p, .9, i, .3) for i, p in enumerate([(-3.9, .5), (-4.8, 1.6), (-2.0, -1.2), (-3.4, -1.6)])]
        new = VGroup(tg, sp, ves, cl, *cut)
        self.play(FadeOut(old, scale=.6), FadeIn(new, scale=1.5), run_time=1.3)
        self.at("resists")
        q = T("?", 54, TEXT, weight=BOLD).move_to([-1.15, 1.9, 0])
        self.play(GrowFromCenter(q), run_time=.6)
        self.at("a detergent")
        bubs = VGroup()
        for i in range(8):
            b = Circle(radius=random.uniform(.1, .22), stroke_color=CYAN, stroke_width=3, fill_color=CYAN,
                       fill_opacity=.15).move_to([random.uniform(-5.4, -.8), random.uniform(-3.2, 1.5), 0])
            b.vy = random.uniform(.7, 1.1)

            def rise(m, dt):
                m.shift(UP * m.vy * dt)
                if m.get_y() > 2.2: m.shift(DOWN * 5.5)
            b.add_updater(rise)
            bubs.add(b)
        dl = T("detergent", 28, CYAN, weight=BOLD).move_to([-3.1, -3.0, 0])
        self.play(FadeIn(bubs), FadeIn(dl), FadeOut(q), run_time=1.0)
        self.at("dissolves membranes")
        arcs = VGroup()
        for v in ves:
            v.clear_updaters()
            for a in (0, 2.1, 4.2):
                arcs.add(Arc(radius=.65, start_angle=a + .2, angle=1.5, stroke_color=INDIGO, stroke_width=5
                             ).move_to(v.get_center() + 0 * RIGHT).shift(0))
        # rebuild arcs around each ring centre properly
        arcs = VGroup()
        for v in ves:
            c = v.get_center()
            for a in (0, 2.1, 4.2):
                arcs.add(Arc(radius=.65, start_angle=a + .2, angle=1.5, stroke_color=INDIGO, stroke_width=5,
                             arc_center=c))
        self.play(*[v.animate.scale(1.12) for v in ves], rate_func=there_and_back, run_time=.5)
        self.remove(ves)
        self.add(arcs)
        self.play(arcs.animate.scale(1.5).set_opacity(0), FadeOut(dl), run_time=1.3)
        self.play(cut[0].animate.move_to([-3.0, 1.2, 0]), cut[1].animate.move_to([-2.0, 2.0, 0]), run_time=.9)
        self.play(scatter(cl, 1.0))
        self.at("band now vanishes")
        dash = DashedVMobject(Rectangle(width=1.0, height=.26, stroke_color=GREY, stroke_width=3), num_dashes=16
                              ).move_to([LANE_X[2], BAND_Y, 0])
        self.play(FadeIn(dash), run_time=.6)
        self.at("membrane was the shield")
        tick = T("✓ membrane was the shield", 28, GREEN, weight=BOLD).move_to([TCX, 2.65, 0])
        self.play(FadeIn(tick), run_time=.7)
        self.finish()


def s05_labels():
    r1 = T("light chain\n(secreted)", 28, TEXT).move_to([-3.75, .25, 0])
    r2 = T("globin\n(stays in cytosol)", 28, TEXT).move_to([-3.75, -2.45, 0])
    cap = T("Blobel and Dobberstein, 1975", 24, TEXT).move_to([TCX, -3.1, 0])
    return r1, r2, cap


def s05_objects():
    ra = bob(ribosome(pos=(-4.7, 1.5, 0), scale=.32), .04, .7)
    rb = bob(ribosome(pos=(-4.7, -1.2, 0), scale=.32), .04, .7, 1)
    ma, mb = ra[3].get_center(), rb[3].get_center()
    lc = wavy(ma + np.array([.1, -.05, 0]), [-3.05, .95, 0], 7, .1, .08, gold=3)
    gb = wavy(mb + np.array([.1, -.05, 0]), [-3.05, -1.5, 0], 7, .1, .08)
    bob(lc, .04, .6); bob(gb, .04, .6, 1)
    cut = VGroup(*[cutter((x, 2.62, 0), .8, i, .05) for i, x in enumerate([-5.2, -4.0, -2.8, -1.6])])
    return ra, rb, lc, gb, cut, ma, mb


class S05Predict(SpokenScene):
    def construct(self):
        tg, sp = tube_base(5)
        gl = s03_end_gel()
        cut = VGroup(*[cutter(p, .9, i, .3) for i, p in enumerate([(-3.9, .5), (-4.8, 1.6), (-2.0, -1.2), (-3.4, -1.6)])])
        dash = DashedVMobject(Rectangle(width=1.0, height=.26, stroke_color=GREY, stroke_width=3), num_dashes=16
                              ).move_to([LANE_X[2], BAND_Y, 0])
        tick = T("✓ membrane was the shield", 28, GREEN, weight=BOLD).move_to([TCX, 2.65, 0])
        self.add(tg, sp, gl, cut, dash, tick, schem())
        ves = ves_group(V_B)
        ra, rb, lc, gb, cutp, ma, mb = s05_objects()
        gel_new = gel_group()
        self.play(FadeOut(tick), FadeOut(dash), FadeOut(gl[1:]), *[c.animate.move_to(p.get_center()) for c, p in zip(cut, cutp)],
                  LaggedStart(*[FadeIn(v, scale=.5) for v in ves], lag_ratio=.2), run_time=1.3)
        self.remove(cut)
        self.add(cutp)
        self.at("1975")
        r1, r2, cap = s05_labels()
        self.play(FadeIn(cap), run_time=.8)
        self.at("blobel")
        self.play(FadeIn(ra, scale=.8), run_time=.7)
        self.at("antibody light chain")
        feed(self, lc, ma, 1.4)
        self.at("secreted protein")
        self.play(FadeIn(r1), run_time=.6)
        self.at("globin")
        self.play(FadeIn(rb, scale=.8), run_time=.7)
        feed(self, gb, mb, 1.4)
        self.play(FadeIn(r2), run_time=.6)
        self.at("made the same way")
        self.play(Indicate(lc), Indicate(gb), run_time=1.0)
        self.at("which survives")
        card = T("Which survives the protease?", 36, TEXT, weight=BOLD).move_to([0, 3.45, 0])
        self.play(FadeIn(card, shift=DOWN * .1), run_time=.7)
        self.finish()


class S06Pause(NarratedScene):
    def construct(self):
        tg, sp = tube_base(6)
        gl = gel_group()
        ves = ves_group(V_B)
        ra, rb, lc, gb, cut, ma, mb = s05_objects()
        r1, r2, cap = s05_labels()
        card = T("Which survives the protease?", 36, TEXT, weight=BOLD).move_to([0, 3.45, 0])
        self.add(tg, sp, gl, ves, ra, rb, lc, gb, cut, r1, r2, cap, card, schem())
        self.wait(4.5)


class S07Reveal(SpokenScene):
    def construct(self):
        tg, sp = tube_base(7)
        gl = gel_group()
        ves = ves_group(V_B)
        ra, rb, lc, gb, cut, ma, mb = s05_objects()
        r1, r2, cap = s05_labels()
        card = T("Which survives the protease?", 36, TEXT, weight=BOLD).move_to([0, 3.45, 0])
        self.add(tg, sp, gl, ves, ra, rb, lc, gb, cut, r1, r2, cap, card, schem())
        self.play(FadeOut(card), FadeOut(lc), FadeOut(r1), ra.animate.shift(RIGHT * .9), run_time=.9)
        ma2 = ra[3].get_center()
        cl = coil(V_B[0], 11, .07, .42, 1.6, gold=4)
        feed(self, cl, ma2, 1.6)
        gold = VGroup(*cl[:4])
        self.play(*[g.animate.shift(UP * .5 + RIGHT * .3).set_opacity(0) for g in gold], run_time=.9)
        b1 = band(0)
        b2 = band(1, .95)
        tl = T("trim", 24, TEXT).move_to([LANE_X[1], .5, 0])
        self.at("only when", lead=.8)
        spots = [(-3.6, -.8, 0), (-1.6, -2.2, 0), (-5.4, -0.2, 0), (-1.0, -1.0, 0)]
        self.play(*[c.animate.move_to(p) for c, p in zip(cut, spots)], FadeIn(b1), FadeIn(b2), FadeIn(tl), run_time=1.4)
        self.at("vesicles were there")
        panel = RoundedRectangle(width=5.1, height=5.7, corner_radius=.18, stroke_color=GREY, stroke_width=2,
                                 fill_color=BG, fill_opacity=.97).move_to([GXC, -.1, 0])
        self.play(FadeOut(VGroup(gl, b1, b2, tl)), FadeIn(panel), run_time=.6)
        row1l = T("made alone", 26, TEXT).move_to([GXC, 2.25, 0])
        row1i = wavy((3.6, 1.55, 0), (4.8, 1.55, 0), 6, .09, .06)
        self.play(FadeIn(row1l), FadeIn(row1i), run_time=.4)
        self.at("while it was being made")
        row2l = T("vesicles added", 26, INDIGO).move_to([GXC, .55, 0])
        ring = Circle(radius=.4, stroke_color=INDIGO, stroke_width=4, fill_color=INDIGO, fill_opacity=.14).move_to([5.1, -.15, 0])
        row2i = wavy((3.0, -.15, 0), (4.1, -.15, 0), 6, .09, .06)
        self.play(FadeIn(row2l), FadeIn(ring), FadeIn(row2i), run_time=.4)
        row3l = T("then protease", 26, LIME).move_to([GXC, -1.15, 0])
        row3i = wavy((3.4, -1.85, 0), (4.6, -1.85, 0), 6, .09, .06)
        rc = cutter((5.3, -1.85, 0), .8, 0, .1)
        self.play(FadeIn(row3l), FadeIn(row3i), FadeIn(rc), run_time=.4)
        self.play(rc.animate.move_to([4.2, -1.85, 0]), run_time=.4)
        tag = T("vesicles added later", 26, RED).move_to([GXC, -2.55, 0])
        self.play(scatter(row3i, .7), FadeIn(tag))
        self.at("was not protected", lead=2.0)
        self.play(FadeOut(VGroup(panel, row1l, row1i, row2l, ring, row2i, row3l, rc, tag)), FadeIn(gl), FadeIn(b1),
                  FadeIn(b2), FadeIn(tl), run_time=.7)
        self.play(cut[0].animate.move_to([-3.6, -1.6, 0]), cut[1].animate.move_to([-4.3, -1.5, 0]), run_time=.8)
        self.play(scatter(gb, 1.2), FadeOut(r2), run_time=1.2)
        nt = T("not protected", 28, RED, weight=BOLD).move_to([-3.75, -2.45, 0])
        self.play(FadeIn(nt), run_time=.5)
        self.finish()


def s08_static():
    tg, sp = tube_base(8)
    gl = VGroup(gel_group(), band(0), band(1, .95), T("trim", 24, TEXT).move_to([LANE_X[1], .5, 0]))
    rs = bob(ribosome(pos=(-4.3, -.2, 0), scale=.4), .04, .7)
    vd = vesicle((-1.9, -.6, 0))
    mr = VMobject(stroke_color=TEXT, stroke_width=4).set_points_smoothly(
        [np.array(p + (0,)) for p in [(-3.0, 1.05), (-3.3, .8), (-3.6, .95), (-3.85, .6), (-4.0, .3)]])
    return tg, sp, gl, rs, vd, mr


ICONS = [("rabbit", -5.0), ("mouse", -3.1), ("dog", -1.2)]


def s08_icons(rs, vd, mr):
    out = VGroup()
    targets = {"rabbit": rs.get_top() + DOWN * .1, "mouse": np.array([-3.3, .9, 0]), "dog": vd.get_top()}
    for k, x in ICONS:
        ic = animal(k).move_to([x, 3.05, 0])
        lb = T(k, 28, TEXT).move_to([x, 2.0, 0])
        ln = DashedLine(lb.get_bottom() + DOWN * .05, targets[k], color=TEXT, stroke_width=3, stroke_opacity=.7)
        out.add(VGroup(ic, lb, ln))
    return out


class S08Species(SpokenScene):
    def construct(self):
        tg, sp, gl, rs, vd, mr = s08_static()
        self.add(tg, sp, gl, schem())
        self.play(FadeIn(rs), FadeIn(vd), FadeIn(mr), run_time=1.3)
        icons = s08_icons(rs, vd, mr)
        for (k, x), grp, cue in zip(ICONS, icons, ["rabbit", "dog", "mouse"]):
            pass
        order = {"rabbit": 0, "mouse": 1, "dog": 2}
        self.at("rabbit")
        self.play(FadeIn(icons[0], shift=DOWN * .5), run_time=1.0)
        self.at("dog")
        self.play(FadeIn(icons[2], shift=DOWN * .5), run_time=1.0)
        self.at("mouse")
        self.play(FadeIn(icons[1], shift=DOWN * .5), run_time=1.0)
        self.at("work together")
        m = rs[3].get_center()
        ch = wavy(m + np.array([.12, -.05, 0]), [-1.9, -.6, 0], 9, .1, .08, gold=3)
        self.play(*[Indicate(g[2], color=WHITE) for g in icons], run_time=.7)
        feed(self, ch, m, 1.6)
        self.at("special secretory ribosome")
        sl = T("special ribosome", 28, TEXT).move_to([-4.3, -1.5, 0])
        self.play(FadeIn(sl), run_time=.6)
        strike = Line(sl.get_left() + LEFT * .1, sl.get_right() + RIGHT * .1, color=RED, stroke_width=7)
        self.play(Create(strike), run_time=.6)
        self.at("address in the growing")
        al = T("address: growing protein", 28, GOLD, weight=BOLD).move_to([-3.1, -2.6, 0])
        self.play(FadeIn(al), *[Indicate(b, color=GOLD, scale_factor=1.6) for b in ch[-3:]], run_time=1.2)
        self.finish()


class S09Idea(SpokenScene):
    def construct(self):
        tg, sp, gl, rs, vd, mr = s08_static()
        icons = s08_icons(rs, vd, mr)
        ch = wavy(rs[3].get_center() + np.array([.12, -.05, 0]), [-1.9, -.6, 0], 9, .1, .08, gold=3)
        world_g = VGroup(tg, sp, gl, rs, vd, mr, icons, ch)
        self.add(world_g, schem())
        self.play(world_g.animate.set_opacity(.25), run_time=1.0)
        self.at("idea")
        lines = rules_lines()
        lines.scale(1.35).move_to([0, .1, 0])
        self.at("two kinds of test")
        self.play(Write(lines[0]), run_time=1.0)
        self.play(Write(lines[1]), run_time=1.0)
        self.at("one shows")
        ins = inset_lite()
        for m in world_g.get_family(): m.clear_updaters()
        self.play(Indicate(lines[0], color=INDIGO), world_g.animate.scale(.2).move_to(INSET_POS).set_opacity(0),
                  FadeIn(ins), run_time=1.5)
        self.remove(world_g)
        self.at("the other shows")
        cw = cell_world(11, ribo=True)
        self.play(FadeIn(cw), lines.animate.scale(.62 / 1.35).move_to([3.85, 3.15, 0]), run_time=1.5)
        self.play(Indicate(lines[1], color=GOLD), run_time=1.0)
        self.finish()


class S10Move(SpokenScene):
    def construct(self):
        cw = cell_world(11, ribo=True)
        self.add(cw)
        ch = chrome(self, sufficient=False)
        rib = cw[-1]
        self.play(FadeOut(rib), run_time=.8)
        ball = folded_ball((-3.6, -.3, 0))
        blab = T("passenger (cytosolic)", 28, TEXT).move_to([-3.6, -1.3, 0])
        other = wavy((-4.1, 1.55, 0), (-2.0, 1.55, 0), 9, .12, .06, gold=3, gold_far=False)
        self.play(FadeIn(ball), FadeIn(blab), FadeIn(other), run_time=1.0)
        self.at("move a stretch")
        gold = VGroup(*other[:3])
        arrow = DashedLine([-3.6, 1.35, 0], [-3.6, .45, 0], color=GOLD, stroke_width=4)
        self.play(Create(arrow), run_time=.5)
        tg = [np.array([-2.7 + .3 * k, -.3, 0]) for k in range(3)]
        self.play(*[b.animate.move_to(p) for b, p in zip(gold, tg)], run_time=1.0)
        self.play(FadeOut(arrow), run_time=.3)
        self.at("moves too")
        box = RoundedRectangle(width=3.4, height=2.4, corner_radius=.3, stroke_color=TEXT, stroke_width=3,
                               fill_color=TEXT, fill_opacity=.04).move_to([1.0, -.4, 0])
        tl = T("target", 28, TEXT).move_to([1.0, .45, 0])
        self.play(FadeIn(box), FadeIn(tl), FadeOut(blab), run_time=.6)
        arr2 = DashedLine([-2.2, -.3, 0], [.4, -.9, 0], color=TEXT, stroke_width=3)
        self.play(Create(arr2), run_time=.3)
        self.play(VGroup(ball, gold).animate.shift(RIGHT * 3.6 + DOWN * .6), run_time=.9)
        self.at("is sufficient")
        suf = T("sufficient", 28, GOLD, weight=BOLD).move_to([2.8, 2.3, 0])
        self.play(FadeIn(suf), run_time=.6)
        self.finish()


class S11Delete(SpokenScene):
    def construct(self):
        cw = cell_world(11)
        self.add(cw)
        ch = chrome(self)
        box = RoundedRectangle(width=3.4, height=2.4, corner_radius=.3, stroke_color=TEXT, stroke_width=3,
                               fill_color=TEXT, fill_opacity=.04).move_to([1.0, -.4, 0])
        tl = T("target", 28, TEXT).move_to([1.0, .45, 0])
        ball = folded_ball((.0, -.9, 0))
        gold = VGroup(*[bead(.12, GOLD).move_to([.9 + .3 * k, -.9, 0]) for k in range(3)])
        old = VGroup(box, tl, ball, gold)
        self.add(old)
        self.play(FadeOut(old), run_time=.4)
        chn = wavy((.8, .15, 0), (3.4, .15, 0), 9, .13, .06, gold=3)
        self.play(FadeIn(chn), run_time=.3)
        self.at("delete the stretch")
        er = eraser([3.9, .15, 0])
        self.play(FadeIn(er), run_time=.3)
        self.play(er.animate.move_to([2.3, .15, 0]), *[FadeOut(b) for b in chn[-3:]], run_time=1.2)
        self.play(FadeOut(er), run_time=.3)
        rest = VGroup(*chn[:6])
        self.play(rest.animate.move_to([-1.5, .2, 0]), run_time=1.2)
        bob(rest, (.7, .4), .8)
        self.at("stranded")
        tag = T("stranded", 28, RED, weight=BOLD).move_to([-1.5, -1.2, 0])
        self.play(FadeIn(tag), run_time=.6)
        self.at("necessary")
        nec = T("necessary", 28, GOLD, weight=BOLD).move_to([5.2, 2.3, 0])
        self.play(FadeIn(nec), run_time=.6)
        self.at("mouse enzyme")
        chip_ = VGroup(chip("DHFR (mouse enzyme)", GREY, 28), bead(.13, GOLD)).arrange(LEFT, buff=.15).move_to([1.0, 1.55, 0])
        chip_[1].set_fill(GOLD)
        st = T("sufficiency test", 28, GOLD).move_to([1.0, .85, 0])
        self.play(FadeIn(chip_), FadeIn(st), run_time=.7)
        self.play(Indicate(chip_[1], color=GOLD, scale_factor=1.8), run_time=.8)
        self.finish()


class S12Examples(SpokenScene):
    def construct(self):
        cw = cell_world(12, mito=False, perox=False)
        self.add(cw)
        chrome(self, necessary=True)
        outer = RoundedRectangle(width=5.4, height=4.0, corner_radius=.9, stroke_color=ORANGE, stroke_width=5,
                                 fill_color=ORANGE, fill_opacity=.06).move_to([-3.0, -.8, 0])
        inner = RoundedRectangle(width=4.2, height=2.9, corner_radius=.65, stroke_color=ORANGE, stroke_width=3,
                                 stroke_opacity=.7).move_to([-3.0, -.85, 0])
        tom = dark_chip("TOM", BLUE, 26).move_to([-1.5, 1.2, 0])
        tim = dark_chip("TIM23", BLUE, 26).move_to([-1.45, .6, 0])
        mat = T("matrix", 28, ORANGE).move_to([-4.0, -1.2, 0])
        per = peroxisome((4.4, -.7, 0), 2.29)
        self.play(FadeIn(VGroup(outer, inner, tom, tim, mat)), FadeIn(per), run_time=1.3)
        cargo = VGroup(chip("DHFR (mouse enzyme)", GREY, 28).move_to([-1.6, 2.75, 0]),
                       *[bead(.13, GOLD).move_to([-3.0 + .32 * k, 2.0, 0]) for k in range(3)])
        cargo[0].shift(RIGHT * 0)
        self.play(FadeIn(cargo), run_time=.8)
        self.at("first 53")
        clab = T("COXIV precursor:\nfirst 53 amino acids", 26, GOLD).move_to([1.8, 1.4, 0])
        self.play(FadeIn(clab), run_time=.7)
        self.at("carried mouse")
        self.play(cargo.animate.shift(DOWN * .4), run_time=.8)
        thread = bead_chain(10, 3, r=.12, vertical=True, gold_at_end=True).move_to([-2.6, -.4, 0])
        self.play(FadeTransform(cargo, thread), FadeOut(clab), run_time=1.5)
        self.play(thread.animate.shift(DOWN * .3), run_time=1.0)
        self.at("matrix")
        tk = T("✓ sufficient", 28, GREEN, weight=BOLD).move_to([-3.0, -3.3, 0])
        self.play(FadeIn(tk), run_time=.6)
        ball = folded_ball((1.5, 1.0, 0), .5)
        bl = T("bacterial\nenzyme", 28, TEXT).move_to([1.5, .0, 0])
        self.play(FadeIn(ball), FadeIn(bl), run_time=.9)
        self.at("adding skl")
        tip = VGroup(*[VGroup(Square(.4, stroke_width=0, fill_color=GOLD, fill_opacity=1), T(c, 22, BG, weight=BOLD)
                              ).move_to([2.2 + .45 * k, 1.0, 0]) for k, c in enumerate("SKL")])
        self.play(FadeIn(tip, shift=LEFT * .3), run_time=.8)
        self.at("carboxyl end")
        pex = dark_chip("PEX5", BLUE, 26).move_to([2.65, 1.8, 0])
        self.play(FadeIn(pex), run_time=.7)
        self.at("sent it into")
        patch = Circle(radius=.5, stroke_width=0, fill_color=MAGENTA, fill_opacity=.35).move_to([2.95, -.5, 0])
        grp = VGroup(ball, tip, pex)
        self.play(FadeOut(bl), run_time=.3)
        self.play(FadeIn(patch), grp.animate.move_to([4.4, -.7, 0]), run_time=1.5)
        self.at("mammalian cell")
        cap = T("in mammalian cells", 22, TEXT).move_to([1.2, -1.1, 0])
        tk2 = T("✓ sufficient", 28, GREEN, weight=BOLD).move_to([4.4, -2.75, 0])
        self.play(FadeIn(cap), FadeIn(tk2), run_time=.8)
        self.finish()


class S13Luciferase(SpokenScene):
    def construct(self):
        cw = cell_world(13, mito=False, perox=True, perox_pos=(4.4, -.7, 0), perox_scale=2.29)
        self.add(cw)
        chrome(self, necessary=True)
        pex = dark_chip("PEX5", BLUE, 26).move_to([2.0, .6, 0])
        ball = folded_ball((-3.4, .3, 0))
        lab = T("luciferase", 28, TEXT).move_to([-3.4, -.65, 0])
        tail = VGroup(*[bead(.12, GOLD).move_to([-2.65 + .28 * k, .3, 0]) for k in range(3)])
        body = VGroup(ball, lab, tail)
        self.play(FadeIn(body), FadeIn(pex), run_time=1.0)
        self.play(body.animate.shift(RIGHT * 2.2), run_time=1.6)
        self.at("deleting")
        er = eraser([.1, .3, 0])
        self.play(FadeIn(er), run_time=.3)
        self.play(er.animate.move_to([-.5, .3, 0]), FadeOut(tail), run_time=1.2)
        self.play(FadeOut(er), run_time=.3)
        self.at("no more than 12")
        tl = T("tail signal: ≤12 amino acids", 28, GOLD).move_to([-.6, 1.6, 0])
        self.play(FadeIn(tl), run_time=.7)
        self.at("left it in the cytosol")
        self.play(body.animate.move_to([.2, -.3, 0]), run_time=1.6)
        self.play(body.animate.shift(RIGHT * 1.2 + DOWN * .1), run_time=1.0)
        tag = T("stays in cytosol", 28, RED, weight=BOLD).move_to([-3.0, -.3, 0])
        self.play(FadeIn(tag), body.animate.shift(LEFT * 1.0), run_time=.8)
        self.at("a signal in that tail")
        self.play(Indicate(tl, color=GOLD), Indicate(tail if False else tl), run_time=1.0)
        self.finish()


class S14Cautions(SpokenScene):
    def construct(self):
        cw = cell_world(14, mito=False, perox=False)
        self.add(cw)
        chrome(self, necessary=True)
        r1 = VGroup(folded_ball((-4.8, 1.5, 0), .5), *[bead(.12, GOLD).move_to([-4.0 + .28 * k, 1.5, 0]) for k in range(3)])
        self.play(FadeIn(r1), run_time=.9)
        self.at("working for one passenger")
        tk = T("✓", 54, GREEN, weight=BOLD).move_to([-2.9, 1.5, 0])
        self.play(GrowFromCenter(tk), run_time=.6)
        r2 = VGroup(RoundedRectangle(width=1.0, height=1.0, corner_radius=.15, stroke_color=GREY, stroke_width=3,
                                     fill_color=GREY, fill_opacity=.3).move_to([-4.8, 0, 0]),
                    *[bead(.12, GOLD).move_to([-4.0 + .28 * k, 0, 0]) for k in range(3)])
        self.play(FadeIn(r2), run_time=.9)
        self.at("every passenger")
        q = T("?", 54, TEXT, weight=BOLD).move_to([-2.9, 0, 0])
        lb = T("one passenger is\nnot every passenger", 28, TEXT).move_to([-3.6, -1.35, 0])
        self.play(GrowFromCenter(q), FadeIn(lb), run_time=.9)
        self.at("skl is picky")
        blocks = VGroup(*[VGroup(Square(.8, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                                 T(c, 32, BG, weight=BOLD)).move_to([3.0 + 1.1 * k, 1.2, 0]) for k, c in enumerate("SKL")])
        self.play(FadeIn(blocks), run_time=.8)
        self.at("only a few swaps")
        alt = ["T", "R", "M"]
        res = [True, False, False, True, False, False]
        dots = VGroup()
        for i, ok in enumerate(res):
            k = i % 3
            new = VGroup(Square(.8, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                         T(alt[k], 32, BG, weight=BOLD)).move_to(blocks[k])
            self.play(Transform(blocks[k], new), run_time=.15)
            d = Circle(radius=.18, stroke_width=0, fill_color=GREEN if ok else RED, fill_opacity=1
                       ).move_to([2.3 + .6 * i, -.3, 0])
            self.play(FadeIn(d, scale=.5), run_time=.15)
            dots.add(d)
            old = VGroup(Square(.8, stroke_width=0, fill_color=GOLD, fill_opacity=1),
                         T("SKL"[k], 32, BG, weight=BOLD)).move_to(blocks[k])
            self.play(Transform(blocks[k], old), run_time=.15)
        self.at("kept it working")
        fl = T("only a few swaps work", 28, TEXT, weight=BOLD).move_to([4.2, -1.2, 0])
        self.play(FadeIn(fl), run_time=.7)
        self.finish()


class S15Return(SpokenScene):
    def construct(self):
        cw = cell_world(15, perox_pos=(-5.45, .6, 0))
        chr_ = chrome(self, necessary=True)
        self.play(FadeIn(cw), run_time=1.0)
        chn = wavy((-1.9, .3, 0), (1.9, .3, 0), 14, .13, .1)
        for i in (0, 1, 2, 11, 12, 13): chn[i].set_fill(GOLD)
        self.play(FadeIn(chn), run_time=.8)
        self.at("two signals")
        self.play(Indicate(VGroup(*chn[:3]), color=GOLD, scale_factor=1.6), Indicate(VGroup(*chn[-3:]), color=GOLD, scale_factor=1.6),
                  run_time=.9)
        a1 = DashedLine([-2.1, .35, 0], [-4.6, .5, 0], color=GOLD, stroke_width=4).add_tip(tip_length=.25)
        a2 = DashedLine([2.1, .3, 0], [3.8, .2, 0], color=GOLD, stroke_width=4).add_tip(tip_length=.25)
        q1 = T("?", 54, TEXT, weight=BOLD).move_to([-3.3, 1.2, 0])
        q2 = T("?", 54, TEXT, weight=BOLD).move_to([2.95, 1.0, 0])
        self.play(Create(a1), Create(a2), FadeIn(q1), FadeIn(q2), run_time=1.0)
        self.at("only an experiment")
        tt = T("test it", 28, TEXT, weight=BOLD).move_to([0, 1.1, 0])
        self.play(FadeIn(tt), run_time=.6)
        self.at("protection shows")
        halo = Circle(radius=.17, stroke_color=INDIGO, stroke_width=6).move_to(chr_["ins"].ves.get_center())
        self.play(FadeIn(halo), Indicate(chr_["ins"], color=INDIGO), run_time=1.2)
        self.at("moving and deleting")
        self.play(Indicate(chr_["rules"][1], color=GOLD), Indicate(chr_["suf"], color=GOLD), Indicate(chr_["nec"], color=GOLD),
                  run_time=1.3)
        self.finish()


class S16End(EndCard):
    LINE = "Protection shows it got in; moving and deleting show what sent it."
