"""Move It, Mutate It, Block It — nuclear transport chapter 2 (same look and colour map as chapter 1).

COLOR MAP
  YELLOW  soluble protein cargo
  BLUE    importin alpha/beta and NLS
  PURPLE  CRM1 export receptor
  ORANGE  NES
  GREEN   RanGTP
  GREY    RanGDP, small particles, and nuclear envelope
  TEAL    FG repeats, RCC1, RanGAP, and RanBP1

The same large left/right cutaway is rebuilt at identical coordinates in every
scene.  All molecular actors are deliberately schematic labelled cartoons.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
CYT_TINT = BG
NUC_TINT = "#24503B"


def label(text, pos, color=TEXT, size=28, weight=NORMAL):
    return T(text, size=size, color=color, weight=weight).move_to(pos)


def add_bob(mob, scene, amp=0.08, speed=1.0, phase=0.0, axis=UP):
    """Gentle ambient motion around a fixed centre; safe during narrated holds."""
    state = {"last": 0.0}

    def bob(m, dt):
        del dt
        now = amp * math.sin(speed * scene.renderer.time + phase)
        m.shift(axis * (now - state["last"]))
        state["last"] = now
    mob.add_updater(bob)
    return mob


def world(scene, question=None):
    """The film's carried world: left cytoplasm, right nucleus, one large pore."""
    left = Rectangle(width=6.75, height=7.0, stroke_width=0,
                     fill_color=CYT_TINT, fill_opacity=0.96).move_to([-3.38, 0, 0])
    right = Rectangle(width=6.75, height=7.0, stroke_width=0,
                      fill_color=NUC_TINT, fill_opacity=0.90).move_to([3.38, 0, 0])
    membranes = VGroup()
    for x in (-0.52, 0.52):
        for y in (-2.75, 2.75):
            membranes.add(RoundedRectangle(corner_radius=0.07, width=0.18, height=1.55,
                                            stroke_color=GREY, stroke_width=2,
                                            fill_color=GREY, fill_opacity=0.65).move_to([x, y, 0]))
    rims = VGroup(
        RoundedRectangle(corner_radius=0.20, width=1.65, height=0.30, stroke_color=GREY,
                         stroke_width=3, fill_color=GREY, fill_opacity=0.34).move_to([0, 2.0, 0]),
        RoundedRectangle(corner_radius=0.20, width=1.65, height=0.30, stroke_color=GREY,
                         stroke_width=3, fill_color=GREY, fill_opacity=0.34).move_to([0, -2.0, 0]),
    )
    chains = VGroup()
    for i, y in enumerate(np.linspace(-1.58, 1.58, 11)):
        side = -1 if i % 2 == 0 else 1
        chain = CubicBezier([side * 0.72, y, 0], [side * 0.25, y + 0.28, 0],
                            [-side * 0.12, y - 0.24, 0], [-side * 0.42, y, 0],
                            color=TEAL, stroke_width=7)
        phase = i * 0.72

        def make_wave(y0, side0, phase0):
            def wave(m, dt):
                del dt
                wiggle = 0.28 * math.sin(scene.renderer.time * 2.2 + phase0)
                m.become(CubicBezier([side0 * 0.72, y0, 0],
                                     [side0 * (0.32 + wiggle), y0 + 0.28, 0],
                                     [-side0 * (0.12 - wiggle), y0 - 0.24, 0],
                                     [-side0 * 0.42, y0, 0], color=TEAL, stroke_width=7))
            return wave
        chain.add_updater(make_wave(y, side, phase))
        chains.add(chain)
    places = VGroup(label("CYTOPLASM", [-4.8, -3.22, 0], TEXT, 28, BOLD),
                    label("NUCLEUS", [4.8, -3.22, 0], TEXT, 28, BOLD))
    schematic = chip("SCHEMATIC", TEAL, size=22, pad=0.15, fill_opacity=0.13).move_to([5.55, 3.28, 0])
    g = VGroup(left, right, membranes, rims, chains, places, schematic)
    g.chains, g.rims = chains, rims
    if question:
        q = label(question, [-3.4, 3.18, 0], YELLOW, 34, BOLD)
        fit(q, max_w=9.7)
        q_bg = RoundedRectangle(corner_radius=0.12, width=q.width + 0.48,
                                height=q.height + 0.24, stroke_width=0,
                                fill_color=BG, fill_opacity=0.96).move_to(q)
        q_bg.set_z_index(20)
        q.set_z_index(21)
        g.add(q_bg, q)
        g.question = q
    return g


def cargo(pos, tag=None, tag_color=BLUE, scale=1.0):
    body = RoundedRectangle(corner_radius=0.20, width=1.12, height=0.88,
                            stroke_color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.86).move_to(pos)
    gloss = Line(body.get_corner(UL) + [0.16, -0.12, 0], body.get_top() + [0.22, -0.12, 0],
                 color=TEXT, stroke_width=2).set_opacity(0.55)
    g = VGroup(body, gloss)
    if tag:
        # Compensate for the final actor scale so every teaching tag remains 28 pt.
        txt = T(tag, size=28 / scale, color=BG, weight=BOLD)
        tab = RoundedRectangle(corner_radius=0.06, width=max(0.80, txt.width + 0.18),
                               height=max(0.42, txt.height + 0.12),
                               stroke_width=0, fill_color=tag_color, fill_opacity=1)
        txt.move_to(tab)
        badge = VGroup(tab, txt).move_to(body.get_top() + UP * 0.12)
        g.add(badge)
        g.tag = badge
    g.body = body
    return g.scale(scale)


def receptor(text, pos, color=BLUE, side=LEFT, scale=1.0):
    """A readable cup rather than an inert name chip."""
    s = -1 if np.allclose(side, LEFT) else 1
    cup = VGroup(
        Line([s * 0.62, 0.58, 0], [s * 0.62, -0.58, 0], color=color, stroke_width=8),
        Line([s * 0.62, 0.58, 0], [-s * 0.05, 0.58, 0], color=color, stroke_width=8),
        Line([s * 0.62, -0.58, 0], [-s * 0.05, -0.58, 0], color=color, stroke_width=8),
    )
    cup.scale(scale)
    txt = T(text, size=28, color=color, weight=BOLD)
    txt_bg = RoundedRectangle(corner_radius=0.06, width=txt.width + 0.18,
                              height=txt.height + 0.10, stroke_width=0,
                              fill_color=BG, fill_opacity=0.94)
    name = VGroup(txt_bg, txt.move_to(txt_bg)).next_to(cup, DOWN, buff=0.16)
    return VGroup(cup, name).move_to(pos)


def ran(pos, gtp=True, scale=1.0, text=True):
    col = GREEN if gtp else GREY
    radius = 0.38 / scale if text else 0.27
    dot = Circle(radius=radius, stroke_color=col, stroke_width=3,
                 fill_color=col, fill_opacity=0.82)
    pos = [pos[0], pos[1], 0] if len(pos) == 2 else pos
    if text:
        txt = T("GTP" if gtp else "GDP", size=28 / scale, color=BG, weight=BOLD).move_to(dot)
        return VGroup(dot, txt).scale(scale).move_to(pos)
    return dot.scale(scale).move_to(pos)


def ran_field(scene, equal=False, labelled=True):
    """Fixed density map used without lateral drift in every gradient scene."""
    nuc_pts = [(2.0, 2.25), (3.15, 1.50), (4.45, 2.28), (5.55, 1.20),
               (2.25, -1.30), (3.75, -2.20), (5.25, -1.35)]
    cyt_green = [(-5.4, 1.65), (-4.0, 2.35), (-2.75, 1.30),
                 (-5.15, -1.30), (-3.65, -2.15), (-2.25, -1.35)]
    cyt_grey = [(-5.35, 1.75), (-4.05, 2.30), (-2.65, 1.25),
                (-5.15, -1.35), (-3.65, -2.15), (-2.30, -1.35)]
    ng = VGroup(*[ran(p, True, 0.78, text=False) for p in nuc_pts])
    cg = VGroup(*[ran(p, equal, 0.78, text=False) for p in (cyt_green if equal else cyt_grey)])
    for i, d in enumerate([*ng, *cg]):
        add_bob(d, scene, amp=0.08, speed=0.75 + (i % 3) * 0.1, phase=i * 0.8,
                axis=RIGHT if i % 2 else UP)
    g = VGroup(ng, cg)
    g.nuclear, g.cytoplasmic = ng, cg
    if labelled:
        l1 = label("RanGTP high", [4.55, 2.95, 0], GREEN, 28, BOLD)
        l2 = label("RanGTP equal" if equal else "RanGDP high", [-4.35, 2.95, 0],
                   GREEN if equal else GREY, 28, BOLD)
        g.add(l1, l2)
    return g


def drift_dots(scene, points, color=GREY, radius=0.11):
    dots = VGroup(*[Dot(p, radius=radius, color=color) for p in points])
    for i, d in enumerate(dots):
        add_bob(d, scene, amp=0.10, speed=0.8 + i * 0.08, phase=i, axis=UP if i % 2 else RIGHT)
    return dots


import random as _random

LESSON_TITLE = "The Nuclear Envelope and Nuclear Transport"
RED_STOP = "#E5534B"


# ---------------------------------------------------------------- helpers (chapter 2)
def pent(pos, r=0.4, tails=0):
    """Pentamer cartoon: yellow pentagon core with `tails` blue tails."""
    body = RegularPolygon(5, radius=r, start_angle=PI / 2, stroke_color=YELLOW, stroke_width=3,
                          fill_color=YELLOW, fill_opacity=0.9)
    tl = VGroup()
    for k in range(tails):
        ang = PI / 2 + k * TAU / 5
        d = np.array([math.cos(ang), math.sin(ang), 0])
        a = d * r * 0.95
        b = d * (r * 0.95 + 0.42)
        tl.add(VGroup(Line(a, b, color=BLUE, stroke_width=7), Dot(b, radius=0.09, color=BLUE)))
    g = VGroup(body, tl)
    g.body, g.tails = body, tl
    return g.move_to(pos)


def needle(tip, direction, length=2.3):
    d = np.array([direction[0], direction[1], 0.0], dtype=float)
    d = d / np.linalg.norm(d)
    tip = np.array([tip[0], tip[1], 0.0])
    return VGroup(Line(tip, tip + d * 0.7, color=TEXT, stroke_width=3),
                  Line(tip + d * 0.7, tip + d * length, color=GREY, stroke_width=12))


def scissors(pos):
    a = Line(LEFT * 0.4 + DOWN * 0.18, RIGHT * 0.4 + UP * 0.18, color=TEXT, stroke_width=6)
    b = Line(LEFT * 0.4 + UP * 0.18, RIGHT * 0.4 + DOWN * 0.18, color=TEXT, stroke_width=6)
    h1 = Circle(radius=0.13, color=GREY, stroke_width=4).move_to(RIGHT * 0.52 + UP * 0.2)
    h2 = Circle(radius=0.13, color=GREY, stroke_width=4).move_to(RIGHT * 0.52 + DOWN * 0.2)
    g = VGroup(a, b, h1, h2)
    g.blade = a
    return g.move_to(pos)


def stop_sign(pos, r=0.3, solid=False):
    s = RegularPolygon(8, radius=r, start_angle=PI / 8, stroke_color=RED_STOP, stroke_width=5,
                       fill_color=RED_STOP, fill_opacity=0.95 if solid else 0.0)
    return s.move_to(pos)


def icon_row(solid_block=False):
    """MOVE / MUTATE / BLOCK icons, built the same way in every scene."""
    banner = Rectangle(width=10.4, height=0.8, stroke_width=0, fill_color=BG, fill_opacity=1.0).move_to([-0.8, 3.12, 0])
    banner.set_z_index(8)
    mv = VGroup(Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=BLUE, stroke_width=7, tip_length=0.2),
                label("MOVE", ORIGIN, BLUE, 28, BOLD)).arrange(RIGHT, buff=0.22).move_to([-4.3, 3.12, 0])
    k = VGroup(T("K", size=28, color=BLUE, weight=BOLD),
               Arrow(LEFT * 0.12, RIGHT * 0.12, buff=0, color=TEXT, stroke_width=4, tip_length=0.12),
               T("T", size=28, color=GREY, weight=BOLD)).arrange(RIGHT, buff=0.12)
    mu = VGroup(k, label("MUTATE", ORIGIN, TEXT, 28, BOLD)).arrange(RIGHT, buff=0.4).move_to([-0.7, 3.12, 0])
    st = stop_sign(ORIGIN, 0.27, solid_block)
    bl = VGroup(st, label("BLOCK", ORIGIN, RED_STOP, 28, BOLD)).arrange(RIGHT, buff=0.22).move_to([2.8, 3.12, 0])
    for m_ in (mv, mu, bl):
        m_.set_z_index(9)
    g = VGroup(banner, mv, mu, bl)
    g.banner, g.move, g.mutate, g.block, g.sign = banner, mv, mu, bl, st
    g.items = VGroup(mv, mu, bl)
    return g


def micro_look(scene, seed=3):
    """Grainy black-and-white electron-micrograph look laid over the carried cutaway."""
    veil = Rectangle(width=13.6, height=7.0, stroke_width=0, fill_color="#0B0E12", fill_opacity=0.50)
    rng = _random.Random(seed)
    grains = VGroup(*[Dot([rng.uniform(-6.7, 6.7), rng.uniform(-3.4, 3.4), 0], radius=0.025,
                          color=TEXT).set_opacity(0.28) for _ in range(90)])

    def jitter(m, dt):
        del dt
        for d in m:
            d.move_to([rng.uniform(-6.7, 6.7), rng.uniform(-3.4, 3.4), 0])
    grains.add_updater(jitter)
    g = VGroup(veil, grains)
    return g


def gold(pos, r=0.16, coat=YELLOW, tab=False, gap=False):
    halo_r = r + 0.13
    if gap:
        halo = Arc(radius=halo_r, start_angle=0.9, angle=4.6, color=coat, stroke_width=5)
    else:
        halo = Circle(radius=halo_r, stroke_color=coat, stroke_width=4, fill_color=coat, fill_opacity=0.22)
    g = VGroup(halo, Dot(radius=r, color=GOLD))
    if tab:
        g.add(Dot(RIGHT * halo_r * 0.75 + UP * halo_r * 0.75, radius=0.07, color=BLUE))
    return g.move_to([pos[0], pos[1], 0])


def drift(scene, mob, amp=0.14, speed=0.9, phase=0.0):
    """Slow two-axis wander around where the object was placed."""
    state = {"x": 0.0, "y": 0.0}

    def f(m, dt):
        del dt
        t = scene.renderer.time
        nx, ny = amp * math.sin(speed * t + phase), amp * math.cos(speed * 0.8 * t + phase * 1.3)
        m.shift([nx - state["x"], ny - state["y"], 0])
        state["x"], state["y"] = nx, ny
    mob.add_updater(f)
    return mob


def walk(scene, mob, pts, total, rate=linear):
    """Move mob through waypoints in `total` seconds."""
    seg = total / len(pts)
    for p in pts:
        scene.play(mob.animate.move_to([p[0], p[1], 0]), run_time=seg, rate_func=rate)


def stuck_at_pore_left(scene, mobs):
    for i, m in enumerate(mobs):
        drift(scene, m, 0.07, 1.1 + 0.15 * i, i)


GREY_POS = [(-4.6, 1.5), (-3.8, 0.6), (-4.4, -0.2), (-2.9, 1.3), (-3.2, 0.1), (-2.2, 0.8)]


def grey_grains(scene):
    gg = VGroup(*[gold(p, 0.14, GREY) for p in GREY_POS])
    for i, m in enumerate(gg):
        drift(scene, m, 0.1, 0.8 + 0.1 * i, i)
    return gg


def lmb_plug(pos, scale=1.0):
    c = Circle(radius=0.34 * scale, stroke_color=RED_STOP, stroke_width=6, fill_color=BG, fill_opacity=0.9)
    s = Line(c.point_at_angle(PI * 0.75), c.point_at_angle(-PI * 0.25), color=RED_STOP, stroke_width=6)
    return VGroup(c, s).move_to(pos)


def gc_chip():
    c = chip("GRADIENT COLLAPSED", RED_STOP, size=28)
    back = RoundedRectangle(corner_radius=0.14, width=c.width, height=c.height, stroke_width=0,
                            fill_color=BG, fill_opacity=0.97).move_to(c)
    g = VGroup(back, c).move_to([3.1, -2.35, 0])
    g.set_z_index(30)
    return g


def x_mark(pos, r=0.26):
    return VGroup(Line([-r, -r, 0], [r, r, 0], color=RED_STOP, stroke_width=8),
                  Line([-r, r, 0], [r, -r, 0], color=RED_STOP, stroke_width=8)).move_to(pos)


# ---------------------------------------------------------------- scenes
class S00Link(SpokenScene):
    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        self.add(w, field)
        c = add_bob(cargo([-2.2, 0.85, 0], "NLS", BLUE, 1.0), self, 0.08, 0.9)
        self.play(FadeIn(c, scale=0.8), run_time=0.8)
        mag_ring = Circle(radius=0.55, color=TEXT, stroke_width=7)
        mag_handle = Line(mag_ring.point_at_angle(-PI / 4), mag_ring.point_at_angle(-PI / 4) + [0.55, -0.55, 0],
                          color=TEXT, stroke_width=9)
        mag = VGroup(mag_ring, mag_handle).move_to([-2.2, 1.35, 0])
        qm = label("?", [-1.05, 1.9, 0], YELLOW, 80, BOLD)
        self.play(FadeIn(mag, shift=DOWN * 0.3), run_time=0.8)
        self.play(FadeIn(qm, scale=0.6), run_time=0.6)
        add_bob(mag, self, 0.09, 1.2, axis=RIGHT)
        self.at("Chapter 1")
        imp = VGroup(cargo([-5.3, -0.55, 0], "NLS", BLUE, 0.8),
                     receptor("importin", [-4.2, -0.6, 0], BLUE, side=LEFT, scale=0.7))
        exp = VGroup(cargo([5.0, -0.55, 0], "NES", ORANGE, 0.8),
                     receptor("CRM1", [3.95, -0.6, 0], PURPLE, side=RIGHT, scale=0.75))
        self.play(FadeOut(mag), FadeOut(qm), FadeIn(imp), FadeIn(exp), run_time=0.5)
        self.play(imp.animate.shift(RIGHT * 2.0), exp.animate.shift(LEFT * 2.3), run_time=2.0, rate_func=smooth)
        self.at("with Ran controlling")
        self.play(Indicate(field.nuclear, color=GREEN, scale_factor=1.12), run_time=1.3)
        self.play(Indicate(field.cytoplasmic, color=GREY, scale_factor=1.12), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = LESSON_TITLE
    TITLE = "Move It, Mutate It, Block It"

    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        veil = Rectangle(width=13.5, height=7.1, stroke_width=0, fill_color=BG, fill_opacity=0.52)
        title = T(self.TITLE.upper(), size=48, color=TEXT, font=TITLE_FONT, weight=BOLD)
        fit(title, max_w=11.2)
        rule = Line(LEFT * 2.0, RIGHT * 2.0, color=GOLD, stroke_width=4).next_to(title, DOWN, 0.28)
        panel = RoundedRectangle(corner_radius=0.18, width=title.width + 0.75,
                                 height=title.height + rule.height + 0.82,
                                 stroke_width=0, fill_color=BG, fill_opacity=0.92)
        panel.move_to(VGroup(title, rule))
        self.add(w, field)
        self.play(FadeIn(veil), FadeIn(panel), FadeIn(title, shift=UP * 0.15),
                  GrowFromCenter(rule), run_time=0.45)
        self.wait(0.7)
        self.play(FadeOut(VGroup(veil, panel, title, rule)), run_time=0.35)


class S02Tails(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        oo = chip("FROG OOCYTE", TEAL, size=28).move_to([-4.5, 3.18, 0])
        p0 = pent([-4.1, 0.6, 0], 0.55, tails=5)
        drift(self, p0, 0.1, 0.8)
        self.at("Start with")
        self.play(FadeIn(oo), GrowFromCenter(p0), run_time=0.5)
        nm = label("NUCLEOPLASMIN", [-4.1, 1.95, 0], YELLOW, 28, BOLD)
        self.at("nucleoplasmin")
        self.play(FadeIn(nm), run_time=0.6)
        self.at("each with a tail")
        tag = label("TAIL", [-2.55, 1.35, 0], BLUE, 28, BOLD)
        self.play(FadeIn(tag), Indicate(p0.tails, color=BLUE, scale_factor=1.15), run_time=1.1)
        self.wait(0.3)
        self.play(FadeOut(tag), FadeOut(nm), run_time=0.4)
        sc = scissors([-5.8, 2.6, 0])
        self.at("In 1982")
        self.play(FadeIn(sc), sc.animate.move_to(p0.get_center() + [-1.4, 1.0, 0]), run_time=1.0)
        self.at("clipped the tails")
        for t in list(p0.tails):
            tgt = t.get_center()
            self.play(sc.animate.move_to(tgt + [0.55, 0.15, 0]), run_time=0.2)
            self.play(Rotate(sc.blade, angle=0.5, rate_func=there_and_back), FadeOut(t, shift=OUT), run_time=0.22)
        self.play(FadeOut(sc, shift=UP), run_time=0.3)
        self.remove(p0)
        p0 = p0.body
        self.add(p0)
        n1 = needle([-4.5, 1.5], [-1, 0.45], 2.4)
        c2, c3 = pent([-4.5, 1.5, 0], 0.35), pent([-4.5, 1.5, 0], 0.35)
        self.at("Bare cores injected")
        nl = label("NO TAILS: OUT", [-3.3, 2.2, 0], TEXT, 28, BOLD)
        self.play(FadeIn(n1, shift=DOWN * 0.4), run_time=0.35)
        self.add(c2, c3)
        self.play(c2.animate.move_to([-3.6, -0.5, 0]), c3.animate.move_to([-4.7, -0.4, 0]),
                  p0.animate.move_to([-4.0, 0.9, 0]), FadeOut(n1), run_time=0.7)
        self.play(p0.animate.move_to([-1.55, 0.95, 0]), c2.animate.move_to([-1.5, -0.1, 0]),
                  c3.animate.move_to([-1.6, -1.05, 0]), run_time=1.1, rate_func=smooth)
        stuck_at_pore_left(self, [p0, c2, c3])
        self.at("stayed out")
        self.play(FadeIn(nl), run_time=0.5)
        n2 = needle([-4.4, -1.4], [-1, -1], 2.4)
        big = pent([-4.4, -1.4, 0], 0.7, tails=1)
        self.at("A larger pentamer")
        self.play(FadeIn(n2, shift=UP * 0.4), run_time=0.3)
        self.add(big)
        self.play(FadeOut(n2), run_time=0.3)
        yl = label("ONE TAIL: IN", [3.9, 2.6, 0], TEXT, 28, BOLD)
        walk(self, big, [(-2.4, -1.5), (-0.9, -0.9), (0.9, -0.4), (2.6, -0.2), (3.6, -0.3)], 1.9, smooth)
        drift(self, big, 0.08, 0.9)
        self.at("went in")
        self.play(FadeIn(yl), run_time=0.4)
        self.finish()


class S02bTailNumber(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        one = pent([-4.4, 0.9, 0], 0.7, tails=1)
        five = pent([-4.4, -0.9, 0], 0.7, tails=5)
        self.at("One attached")
        l1 = label("ONE TAIL: SUFFICIENT", [-3.2, 2.65, 0], TEXT, 28, BOLD)
        self.play(FadeIn(one, shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeIn(l1), run_time=0.5)
        self.play(one.animate.move_to([-2.0, 0.9, 0]), run_time=2.0, rate_func=linear)
        self.at("More tails")
        l2 = label("MORE TAILS: FASTER", [3.2, 2.65, 0], TEXT, 28, BOLD)
        self.play(FadeIn(five), FadeIn(l2), one.animate.move_to([-1.0, 0.9, 0]), run_time=0.8, rate_func=linear)
        self.play(five.animate.move_to([3.6, -0.9, 0]), one.animate.move_to([3.6, 0.9, 0]),
                  run_time=3.4, rate_func=linear) if False else None
        self.play(AnimationGroup(five.animate(rate_func=smooth, run_time=2.8).move_to([3.6, -0.9, 0]),
                                 one.animate(rate_func=linear, run_time=4.9).move_to([3.6, 0.9, 0])))
        drift(self, one, 0.1, 1.0)
        drift(self, five, 0.1, 1.2, 1)
        self.finish()


class S03ThirdInjection(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        r1 = VGroup(label("NO TAILS: OUT", [-4.3, 1.9, 0], TEXT, 28, BOLD), pent([-2.0, 1.9, 0], 0.32),
                    label("ONE TAIL: IN", [-4.3, -1.9, 0], TEXT, 28, BOLD), pent([-2.0, -1.9, 0], 0.5, tails=1))
        r1.set_opacity(0.5)
        self.add(r1)
        nd = needle([3.0, 0.3], [1, 0], 2.6)
        nd.shift(RIGHT * 4.0)
        cores = [pent([3.0, 0.3, 0], 0.5), pent([3.0, 0.3, 0], 0.5), pent([3.0, 0.3, 0], 0.5)]
        self.at("One more injection")
        self.play(nd.animate.shift(LEFT * 4.0), run_time=2.0, rate_func=smooth)
        self.at("straight into")
        self.add(*cores)
        self.play(cores[0].animate.move_to([2.4, 1.3, 0]), cores[1].animate.move_to([3.4, -1.0, 0]),
                  cores[2].animate.move_to([4.2, 1.2, 0]), run_time=1.4, rate_func=smooth)
        for i, c in enumerate(cores):
            drift(self, c, 0.22, 0.9 + 0.2 * i, i * 2)
        self.at("They remained there")
        self.play(Indicate(VGroup(*cores), color=YELLOW, scale_factor=1.1), run_time=1.4)
        ring = DashedVMobject(Circle(radius=1.25, color=YELLOW, stroke_width=5), num_dashes=24).move_to(nd.get_center())
        qm = label("?", [4.1, 2.1, 0], YELLOW, 80, BOLD)
        ring.add_updater(lambda m, dt: m.rotate(0.6 * dt))
        self.at("Why that injection")
        self.play(FadeIn(ring), FadeIn(qm, scale=0.5), run_time=0.8)
        self.finish()


class S04Gold(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        qm = label("?", [0, 0, 0], YELLOW, 112, BOLD)
        self.at("Which route")
        self.play(FadeIn(qm, scale=0.6), run_time=0.8)
        m = micro_look(self)
        self.add(m)
        self.play(FadeIn(m[0]), Indicate(w.chains, color=TEAL, scale_factor=1.05), run_time=1.6)
        self.at("In 1984")
        nd = needle([-4.6, 1.2], [-1, 1], 2.4)
        sizes = [0.07, 0.11, 0.16, 0.22, 0.12, 0.18]
        gs = VGroup(*[gold([-4.6, 1.2, 0], r) for r in sizes])
        for g in gs:
            g[0].set_opacity(0)
        self.play(FadeOut(qm), FadeIn(nd, shift=DOWN * 0.3), run_time=0.7)
        self.add(gs)
        spots = [(-4.5, 0.2), (-3.6, 1.2), (-3.4, -0.4), (-4.7, -0.9), (-2.4, 0.3), (-3.9, 2.0)]
        self.at("injected gold grains")
        self.play(*[g.animate.move_to([p[0], p[1], 0]) for g, p in zip(gs, spots)], FadeOut(nd), run_time=1.6, rate_func=smooth)
        for i, g in enumerate(gs):
            drift(self, g, 0.1, 0.8 + 0.1 * i, i)
        self.at("coated with")
        for g in gs:
            g[0].set_stroke(opacity=1)
        coat = label("NUCLEOPLASMIN COAT", [-3.6, 2.9, 0], YELLOW, 28, BOLD)
        self.play(*[g[0].animate.set_fill(YELLOW, 0.25).set_stroke(YELLOW, 4) for g in gs], FadeIn(coat), run_time=1.4)
        self.wait(0.6)
        self.at("about 5 to 20")
        sz = label("5 TO 20 NM", [-3.6, -2.2, 0], TEXT, 28, BOLD)
        self.play(FadeOut(coat), FadeIn(sz), Indicate(gs[0], scale_factor=1.6), run_time=0.9)
        self.play(Indicate(gs[3], scale_factor=1.3), run_time=0.9)
        self.at("They entered")
        self.play(FadeOut(sz), run_time=0.4)
        mv = VGroup(gs[1], gs[4], gs[5])
        walk(self, gs[4], [(-1.2, 0.4), (0.2, 0.1), (1.8, 0.4), (3.2, 0.8)], 2.6, smooth) if False else None
        self.play(gs[4].animate.move_to([3.2, 0.7, 0]), gs[1].animate.move_to([1.9, -0.6, 0]),
                  gs[5].animate.move_to([4.5, -0.8, 0]), run_time=2.8, rate_func=smooth)
        self.at("Electron")
        tp = label("TRANSPORT AT PORES", [-3.4, 2.9, 0], GOLD, 28, BOLD)
        pores = [(-0.40, 1.5), (0.40, -1.5), (-0.1, 0.8), (0.1, -0.7), (-0.3, 0.0)]
        self.play(FadeIn(tp), *[g.animate.move_to([p[0], p[1], 0]) for g, p in zip([gs[0], gs[2], gs[3], gs[4], gs[5]], pores)],
                  run_time=2.4, rate_func=smooth)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        w = world(self)
        m = micro_look(self)
        self.add(w, m)
        old = VGroup(gold([-0.3, 0.8, 0]), gold([0.2, -0.6, 0], 0.2), gold([2.7, 0.5, 0], 0.12))
        for i, g in enumerate(old):
            drift(self, g, 0.1, 0.9, i)
        self.add(old)
        pr = label("PREDICT", [-3.4, 2.9, 0], YELLOW, 60, BOLD)
        self.at("Now predict")
        self.play(FadeIn(pr, scale=0.7), run_time=0.8)
        self.wait(0.8)
        self.at("Coat the same")
        coat = chip("INERT COAT", GREY, size=28).move_to([-3.7, 2.3, 0])
        nd = needle([-4.4, 1.7], [-1, 1], 2.4)
        gg = VGroup(*[gold([-4.4, 1.7, 0], 0.14, GREY) for _ in GREY_POS])
        self.play(FadeOut(pr), FadeOut(old), FadeIn(nd, shift=DOWN * 0.3), run_time=0.8)
        self.add(gg)
        self.play(*[g.animate.move_to([p[0], p[1], 0]) for g, p in zip(gg, GREY_POS)], FadeOut(nd), FadeIn(coat),
                  run_time=1.8, rate_func=smooth)
        for i, g in enumerate(gg):
            drift(self, g, 0.1, 0.8 + 0.1 * i, i)
        self.at("Where will most")
        q = label("WHERE DO THEY END UP?", [-3.4, 3.18, 0], YELLOW, 34, BOLD)
        bg = RoundedRectangle(corner_radius=0.12, width=q.width + 0.48, height=q.height + 0.24, stroke_width=0,
                              fill_color=BG, fill_opacity=0.96).move_to(q)
        self.play(FadeIn(bg), FadeIn(q), run_time=0.8)
        self.play(Indicate(gg, color=GREY, scale_factor=1.1), run_time=1.0)
        self.finish()


class S06Pause(Scene):
    def construct(self):
        w = world(self)
        m = micro_look(self)
        gg = grey_grains(self)
        coat = chip("INERT COAT", GREY, size=28).move_to([-3.7, 2.3, 0])
        q = label("WHERE DO THEY END UP?", [-3.4, 3.18, 0], YELLOW, 34, BOLD)
        bg = RoundedRectangle(corner_radius=0.12, width=q.width + 0.48, height=q.height + 0.24, stroke_width=0,
                              fill_color=BG, fill_opacity=0.96).move_to(q)
        self.add(w, m, gg, coat, bg, q)
        self.wait(4.5)


class S07Reveal(SpokenScene):
    def construct(self):
        w = world(self)
        m = micro_look(self)
        gg = grey_grains(self)
        coat = chip("INERT COAT", GREY, size=28).move_to([-3.7, 2.3, 0])
        self.add(w, m, gg, coat)
        self.at("mostly outside")
        self.play(Indicate(gg, color=GREY, scale_factor=1.12), run_time=1.4)
        nt = VGroup(*[gold(p, 0.14, YELLOW, gap=True) for p in [(-4.6, -1.3), (-3.6, -1.6), (-2.6, -1.2)]])
        for i, g in enumerate(nt):
            drift(self, g, 0.1, 0.8 + 0.1 * i, i)
        self.at("Gold coated")
        lab = chip("NO TRANSPORT PART", YELLOW, size=28).move_to([-3.6, -2.5, 0])
        self.play(FadeIn(nt, shift=UP * 0.2), FadeIn(lab), run_time=1.2)
        self.at("also largely")
        self.play(*[g.animate.shift(LEFT * 0.4) for g in nt], run_time=1.6, rate_func=there_and_back)
        full = VGroup(*[gold(p, 0.16, YELLOW, tab=True) for p in [(-0.25, 0.7), (0.2, -0.5), (2.5, 0.4), (3.7, -0.9)]])
        for i, g in enumerate(full):
            drift(self, g, 0.12, 0.9 + 0.1 * i, i)
        self.at("So the coat")
        self.play(FadeIn(full, scale=0.6), run_time=1.0)
        self.at("decided entry")
        dec = label("THE COAT DECIDES", [3.3, 2.7, 0], GOLD, 34, BOLD)
        self.play(FadeIn(dec, scale=0.8), run_time=0.8)
        self.play(Indicate(full, scale_factor=1.25), run_time=1.0)
        self.finish()


class S08Move(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        t_block = RoundedRectangle(corner_radius=0.2, width=3.5, height=1.0, stroke_color=YELLOW, stroke_width=3,
                                   fill_color=YELLOW, fill_opacity=0.9).move_to([-3.6, 2.15, 0])
        t_name = label("SV40 LARGE T", [-3.6, 2.15, 0], BG, 28, BOLD)
        tab = VGroup(RoundedRectangle(corner_radius=0.08, width=2.3, height=0.52, stroke_width=0, fill_color=BLUE,
                                      fill_opacity=1), T("PKKKRKV", size=28, color=BG, weight=BOLD, font=MONO))
        tab[1].move_to(tab[0])
        tab.move_to(t_block.get_top() + UP * 0.3)
        tgroup = VGroup(t_block, t_name)
        add_bob(tgroup, self, 0.06, 0.9)
        self.at("Next")
        self.play(FadeIn(tgroup, shift=RIGHT * 0.3), run_time=1.2)
        self.at("traced the address")
        self.play(FadeIn(tab, shift=DOWN * 0.2), run_time=0.8)
        self.at("short stretch")
        self.play(Indicate(tab, color=BLUE, scale_factor=1.15), run_time=1.2)
        self.at("The normally cytoplasmic")
        rb = [RoundedRectangle(corner_radius=0.12, width=1.5, height=0.9, stroke_color=TEXT, stroke_width=3,
                               fill_color=TEXT, fill_opacity=0.5).move_to([-3.6, y, 0]) for y in (-0.1, -1.95)]
        l1 = label("REPORTER 1", [-3.6, 0.62, 0], TEXT, 28, BOLD)
        l2 = label("REPORTER 2", [-3.6, -1.23, 0], TEXT, 28, BOLD)
        for i, b in enumerate(rb):
            drift(self, b, 0.05, 0.9 + 0.2 * i, i)
        self.play(FadeIn(VGroup(*rb), shift=UP * 0.2), FadeIn(l1), FadeIn(l2), run_time=1.2)
        self.at("reporters were beta")
        n1 = label("β-GALACTOSIDASE", [-3.6, 0.62, 0], TEXT, 28, BOLD)
        n2 = label("PYRUVATE KINASE", [-3.6, -1.23, 0], TEXT, 28, BOLD)
        self.play(Transform(l1, n1), run_time=0.6)
        self.at("pyruvate kinase")
        self.play(Transform(l2, n2), run_time=0.6)
        self.wait(0.6)
        self.at("Attached to either")
        t2 = tab.copy()
        self.play(tab.animate.scale(0.7).move_to(rb[0].get_top() + UP * 0.2), run_time=1.0)
        t2.scale(0.7).move_to(tgroup.get_center())
        self.play(t2.animate.move_to(rb[1].get_top() + UP * 0.2), run_time=0.9)
        tagged = [VGroup(rb[0].copy(), tab.copy()), VGroup(rb[1].copy(), t2.copy())]
        self.at("caused nuclear")
        self.add(*tagged)
        self.remove(tab, t2)
        self.play(FadeOut(l1), FadeOut(l2), FadeOut(tgroup), run_time=0.5)
        self.play(tagged[0].animate.move_to([3.6, 0.8, 0]), tagged[1].animate.move_to([4.4, -1.0, 0]),
                  run_time=2.6, rate_func=smooth)
        for i, g in enumerate(tagged):
            drift(self, g, 0.1, 0.9, i)
        self.finish()


class S09Mutate(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        letters = VGroup(*[T(ch, size=72, color=BLUE, weight=BOLD, font=MONO) for ch in "PKKKRKV"]).arrange(RIGHT, buff=0.22)
        panel = RoundedRectangle(corner_radius=0.2, width=letters.width + 0.9, height=letters.height + 0.9,
                                 stroke_color=BLUE, stroke_width=3, fill_color=BG, fill_opacity=0.96)
        grp = VGroup(panel, letters).move_to([0, 0.6, 0])
        panel.set_z_index(5)
        letters.set_z_index(6)
        add_bob(grp, self, 0.07, 1.0)
        self.at("Next")
        self.play(FadeIn(panel), FadeIn(letters, scale=0.8), run_time=1.2)
        self.at("Swapping lysine")
        self.play(Indicate(letters[2], color=GOLD, scale_factor=1.5), run_time=1.3)
        num = label("128", [letters[2].get_x(), -0.55, 0], GOLD, 34, BOLD)
        num.set_z_index(8)
        numbg = RoundedRectangle(corner_radius=0.06, width=num.width + 0.2, height=num.height + 0.15, stroke_width=0, fill_color=BG, fill_opacity=0.95).move_to(num)
        numbg.set_z_index(7)
        self.play(FadeIn(num), FadeIn(numbg), run_time=0.4)
        self.at("threonine")
        newt = T("T", size=72, color=GREY, weight=BOLD, font=MONO).move_to(letters[2])
        newt.set_z_index(6)
        self.play(Transform(letters[2], newt), panel.animate.set_stroke(GREY), run_time=1.2)
        self.at("abolished")
        for L in letters:
            L.set_color(GREY)
        blk = RoundedRectangle(corner_radius=0.2, width=3.5, height=1.0, stroke_color=YELLOW, stroke_width=3,
                               fill_color=YELLOW, fill_opacity=0.9).move_to([-3.9, -1.7, 0])
        tt = label("SV40 LARGE T", [-3.9, -1.7, 0], BG, 28, BOLD)
        gtab = RoundedRectangle(corner_radius=0.08, width=1.6, height=0.4, stroke_width=0, fill_color=GREY,
                                fill_opacity=1).move_to(blk.get_top() + UP * 0.2)
        blkg = VGroup(blk, tt, gtab)
        self.play(FadeIn(blkg, shift=UP * 0.2), FadeOut(num), run_time=0.8)
        self.play(blkg.animate.shift(RIGHT * 1.4), run_time=1.0)
        self.play(blkg.animate.shift(LEFT * 1.4), run_time=0.8)
        add_bob(blkg, self, 0.08, 0.9)
        self.at("Moving")
        self.play(FadeOut(grp), FadeOut(letters), run_time=0.6)
        ic = icon_row()
        self.play(FadeIn(ic.banner), FadeIn(ic.move, shift=DOWN * 0.2), run_time=0.6)
        self.at("mutating")
        self.play(FadeIn(ic.mutate, shift=DOWN * 0.2), run_time=0.6)
        self.at("blocking")
        self.play(FadeIn(ic.block, shift=DOWN * 0.2), run_time=0.6)
        self.at("Each result")
        for m_ in (ic.move, ic.mutate, ic.block):
            self.play(Indicate(m_, scale_factor=1.12), run_time=0.7)
        self.play(Indicate(ic.items, color=GOLD, scale_factor=1.05), run_time=1.0)
        self.finish()


class S10Readers(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        ic = icon_row()
        self.add(ic)
        c = cargo([-3.0, 0.2, 0], "NLS", BLUE, 1.1)
        add_bob(c, self, 0.07, 0.9)
        self.at("By 1995")
        self.play(FadeIn(c, shift=RIGHT * 0.3), run_time=1.2)
        al = receptor("alpha", [-4.7, 0.25, 0], BLUE, side=LEFT, scale=0.8)
        self.at("important alpha")
        nm_a = label("IMPORTIN ALPHA", [-3.1, -1.4, 0], BLUE, 28, BOLD)
        self.play(FadeIn(al, shift=RIGHT * 0.3), run_time=0.8)
        self.play(al.animate.move_to([-3.85, 0.25, 0]), FadeIn(nm_a), run_time=1.0)
        self.at("important beta")
        be = receptor("beta", [-5.2, 0.25, 0], BLUE, side=LEFT, scale=0.8)
        cx = VGroup(c, al)
        self.play(FadeOut(nm_a), FadeIn(be), run_time=0.5)
        self.play(VGroup(be, c, al).animate.shift(RIGHT * 2.4), run_time=1.6, rate_func=smooth)
        self.at("dock at the pore")
        self.play(Indicate(w.chains, color=TEAL, scale_factor=1.08), run_time=1.2)
        self.at("Loosen rich")
        nes = cargo([3.9, -0.5, 0], "NES", ORANGE, 1.1)
        nl = label("LEUCINE-RICH NES", [3.7, -1.65, 0], ORANGE, 28, BOLD)
        add_bob(nes, self, 0.07, 0.9, 1.5)
        self.play(FadeIn(nes, shift=LEFT * 0.3), FadeIn(nl), run_time=1.0)
        qm = label("?", [2.3, -0.4, 0], YELLOW, 100, BOLD)
        self.at("no known reader")
        self.play(FadeIn(qm, scale=0.5), run_time=0.7)
        qm.add_updater(lambda m, dt: m.set_opacity(0.8 + 0.2 * math.sin(4 * self.renderer.time)))
        self.finish()


def purple_cup(pos, text="CRM1", scale=0.7):
    return receptor(text, pos, PURPLE, side=RIGHT, scale=scale)


class S11Crm1(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        ic = icon_row()
        self.add(ic)
        crm = purple_cup([3.9, 1.0, 0], "CRM1", 0.75)
        nc = cargo([5.1, 0.95, 0], "NES", ORANGE, 0.75)
        cx = VGroup(crm, nc)
        self.play(FadeIn(cx, shift=LEFT * 0.3), run_time=0.8)
        self.play(cx.animate.shift(LEFT * 5.4), run_time=5.5, rate_func=smooth)
        self.at("extra")
        self.play(FadeOut(cx), FadeOut(w[5]), run_time=0.3)
        p1 = RoundedRectangle(corner_radius=0.2, width=6.5, height=3.2, stroke_color=PURPLE, stroke_width=3,
                              fill_color=BG, fill_opacity=1.0).move_to([-3.4, -2.05, 0])
        p1.set_z_index(10)
        h1 = label("MORE CRM1", [-4.9, -0.8, 0], PURPLE, 28, BOLD)
        h1.set_z_index(11)
        pool = VGroup(*[purple_cup([x, -0.8, 0], "", 0.4) for x in (-2.6, -2.0, -1.4)])
        pool.set_z_index(11)
        self.play(FadeIn(VGroup(p1, h1), shift=UP * 0.4), run_time=0.5)
        self.play(FadeIn(pool, scale=0.6), run_time=0.5)
        rows = []
        for y, tag, col in ((-1.65, "REV", ORANGE), (-2.8, "U snRNA", ORANGE)):
            cg = cargo([-1.5, y, 0], tag, col, 0.6)
            cu = purple_cup([-3.0, y, 0], "", 0.5)
            r = VGroup(cu, cg)
            r.set_z_index(11)
            rows.append(r)
        self.play(FadeIn(rows[0]), run_time=0.4)
        self.play(rows[0].animate.shift(LEFT * 2.6), run_time=1.8, rate_func=linear)
        self.at("also")
        self.play(FadeIn(rows[1]), run_time=0.4)
        self.play(rows[1].animate.shift(LEFT * 2.6), run_time=2.0, rate_func=linear)
        self.at("Leptomycin")
        p2 = RoundedRectangle(corner_radius=0.2, width=6.5, height=3.2, stroke_color=RED_STOP, stroke_width=3,
                              fill_color=BG, fill_opacity=1.0).move_to([3.4, -2.05, 0])
        p2.set_z_index(10)
        h2 = label("LEPTOMYCIN B", [3.4, -0.8, 0], RED_STOP, 28, BOLD)
        h2.set_z_index(11)
        self.play(FadeIn(VGroup(p2, h2), shift=UP * 0.4), run_time=0.5)
        rows2 = []
        for y, tag in ((-1.65, "REV"), (-2.8, "U snRNA")):
            cg = cargo([4.3, y, 0], tag, ORANGE, 0.6)
            cu = purple_cup([3.0, y, 0], "", 0.5)
            pl = lmb_plug([3.0, y, 0], 0.7)
            r = VGroup(cu, cg, pl)
            r.set_z_index(11)
            rows2.append(r)
        self.play(FadeIn(VGroup(*rows2)), run_time=0.5)
        for i, r in enumerate(rows2):
            drift(self, r, 0.07, 1.0 + i * 0.2, i)
        self.at("inhibited both")
        self.play(ic.sign.animate.set_fill(RED_STOP, 0.95), Indicate(ic.block, scale_factor=1.15), run_time=1.0)
        self.finish()


class S12Binding(SpokenScene):
    def construct(self):
        w = world(self)
        self.add(w)
        w[5].set_opacity(0)
        ic = icon_row(solid_block=True)
        self.add(ic)
        panel = RoundedRectangle(corner_radius=0.35, width=11.0, height=5.2, stroke_color=TEAL, stroke_width=3,
                                 fill_color=BG, fill_opacity=1.0).move_to([0, -0.35, 0])
        panel.set_z_index(10)
        tt = label("TEST TUBE", [0, 1.85, 0], TEAL, 28, BOLD)
        tt.set_z_index(11)
        self.add(panel, tt)
        crm = purple_cup([-3.6, 0.2, 0], "CRM1", 1.0)
        rg = ran([-2.6, -1.3, 0], True, 1.0)
        nc = cargo([3.4, 0.2, 0], "NES", ORANGE, 1.1)
        for m_ in (crm, rg, nc):
            m_.set_z_index(11)
        self.at("CRM1")
        self.play(FadeIn(crm, shift=RIGHT * 0.3), run_time=0.6)
        self.at("ran GTP")
        self.play(FadeIn(rg, shift=UP * 0.3), run_time=0.6)
        self.at("and an export")
        self.play(FadeIn(nc, shift=LEFT * 0.3), run_time=0.6)
        self.at("formed a complex")
        self.play(crm.animate.move_to([-0.9, 0.2, 0]), rg.animate.move_to([0.1, -0.85, 0]),
                  nc.animate.move_to([1.05, 0.2, 0]), run_time=1.0, rate_func=smooth)
        cplx = VGroup(crm, rg, nc)
        drift(self, cplx, 0.07, 1.0)
        self.play(Indicate(cplx, scale_factor=1.08), run_time=1.0)
        self.at("All three results")
        c3 = cplx.copy()
        self.remove(cplx)
        self.add(c3)
        c3.clear_updaters()
        self.play(FadeOut(tt), c3.animate.scale(0.5).move_to([3.4, -1.85, 0]), panel.animate.set_opacity(0.0),
                  run_time=0.8)
        self.remove(panel)
        i1 = VGroup(purple_cup([-3.9, -1.85, 0], "", 0.45), purple_cup([-3.4, -1.85, 0], "", 0.45))
        i1l = label("MORE CRM1", [-3.4, -2.5, 0], PURPLE, 28, BOLD)
        i2 = lmb_plug([0, -2.3, 0], 0.8)
        i2l = label("LMB", [0, -2.75, 0], RED_STOP, 28, BOLD)
        i2l.set_z_index(8)
        i2bg = RoundedRectangle(corner_radius=0.08, width=i2l.width + 0.3, height=i2l.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=0.95).move_to(i2l)
        i2bg.set_z_index(7)
        i3l = label("COMPLEX", [3.4, -2.65, 0], TEXT, 28, BOLD)
        backdrop = RoundedRectangle(corner_radius=0.2, width=3.4, height=2.5, stroke_width=0, fill_color=BG,
                                    fill_opacity=0.92).move_to([0, 0.8, 0])
        backdrop.set_z_index(5)
        big = purple_cup([0, 0.85, 0], "CRM1", 1.4)
        big.set_z_index(6)
        big.set_opacity(0.45)
        self.play(FadeIn(i1), FadeIn(i1l), FadeIn(i2), FadeIn(i2l), FadeIn(i2bg), FadeIn(i3l), FadeIn(backdrop), FadeIn(big), run_time=0.6)
        ars = VGroup(*[Arrow(s_, [0, -0.45, 0], buff=0.15, color=PURPLE, stroke_width=5, tip_length=0.22)
                       for s_ in ([-3.5, -1.8, 0], [0, -1.7, 0], [3.2, -1.8, 0])])
        ars.set_z_index(6)
        self.play(LaggedStart(*[GrowArrow(a) for a in ars], lag_ratio=0.3), run_time=1.4)
        self.play(big.animate.set_opacity(1.0), run_time=0.6)
        self.at("Together")
        self.play(FadeOut(VGroup(i1, i1l, i2, i2l, i2bg, i3l, c3, ars, backdrop)), w[5].animate.set_opacity(1), run_time=1.2)
        drift(self, big, 0.1, 1.0)
        self.finish()


class S13RanBlock(SpokenScene):
    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        lg = label("RanGTP high", [3.0, 3.05, 0], GREEN, 28, BOLD)
        ld = label("RanGDP high", [-4.35, 3.05, 0], GREY, 28, BOLD)
        self.add(w, field, lg, ld)
        self.at("The same year")
        self.play(Indicate(field.nuclear, color=GREEN, scale_factor=1.12), run_time=1.3)
        self.at("collapsed the")
        self.play(Indicate(VGroup(field.nuclear, field.cytoplasmic), color=GOLD, scale_factor=1.06), run_time=1.5)
        self.wait(1.5)
        self.at("They injected")
        nd = needle([3.4, 0.2], [1, 0.0], 2.6).shift(RIGHT * 3.5)
        self.play(nd.animate.shift(LEFT * 3.5), run_time=1.0, rate_func=smooth)
        gap = chip("RanGAP1", TEAL, size=28).move_to([2.3, 0.2, 0])
        self.at("rang a p1")
        self.play(FadeIn(gap, scale=0.5), run_time=0.4)
        self.play(*[d.animate.set_fill(GREY).set_stroke(GREY) for d in field.nuclear], run_time=0.6)
        self.wait(0.2)
        self.play(*[d.animate.set_fill(GREEN).set_stroke(GREEN) for d in field.nuclear], FadeOut(gap), run_time=0.4)
        bp = chip("RanBP1", TEAL, size=28).move_to([2.3, 0.2, 0])
        self.at("ranb p1")
        self.play(FadeIn(bp, scale=0.5), run_time=0.4)
        self.play(*[d.animate.set_fill(GREY).set_stroke(GREY) for d in field.nuclear], run_time=0.5)
        self.play(*[d.animate.set_fill(GREEN).set_stroke(GREEN) for d in field.nuclear], FadeOut(bp), run_time=0.4)
        mt = VGroup(ran([0, 0, 0], True, 1.0), Line([-0.15, 0.4, 0], [0.1, 0.0, 0], color=RED_STOP, stroke_width=5),
                    Line([0.1, 0.0, 0], [-0.1, -0.4, 0], color=RED_STOP, stroke_width=5)).move_to([2.3, 0.2, 0])
        ml = label("MUTANT RAN", [2.3, 1.0, 0], RED_STOP, 28, BOLD)
        self.at("or a defective")
        self.play(FadeIn(mt, scale=0.5), FadeIn(ml), run_time=0.5)
        self.play(*[d.animate.set_fill(GREY).set_stroke(GREY) for d in field.nuclear], run_time=0.9)
        gc = gc_chip()
        self.play(FadeIn(gc), FadeOut(lg), run_time=0.6)
        self.at("could not stably")
        self.play(mt[0][1].animate.shift(UP * 0.9 + RIGHT * 0.3).set_opacity(0.2), run_time=1.6)
        self.play(Indicate(mt[0][0], color=RED_STOP), run_time=0.9)
        self.finish()


class S13bRanResults(SpokenScene):
    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        for d in field.nuclear:
            d.set_fill(GREY).set_stroke(GREY)
        gc = gc_chip()
        self.add(w, field, gc)
        self.at("All three")
        dep = label("RanGTP DEPLETED", [3.4, 0.1, 0], GREEN, 28, BOLD)
        self.play(FadeIn(dep), Indicate(field.nuclear, color=GREY, scale_factor=1.15), run_time=1.5)
        self.at("Major import")
        imp = VGroup(cargo([-5.3, 0.3, 0], "NLS", BLUE, 0.8), receptor("importin", [-4.2, 0.25, 0], BLUE, side=LEFT, scale=0.7))
        exp = VGroup(cargo([5.2, -0.3, 0], "NES", ORANGE, 0.8), receptor("CRM1", [4.1, -0.35, 0], PURPLE, side=RIGHT, scale=0.75))
        self.play(FadeOut(dep), FadeIn(imp), FadeIn(exp), run_time=0.7)
        self.play(imp.animate.shift(RIGHT * 2.5), exp.animate.shift(LEFT * 2.5), run_time=1.6, rate_func=linear)
        self.at("stopped")
        xs = VGroup(x_mark([-1.0, 1.15, 0]), x_mark([0.95, -1.6, 0]))
        self.play(FadeIn(xs, scale=1.5), run_time=0.5)
        drift(self, imp, 0.05, 1.5)
        drift(self, exp, 0.05, 1.5, 1)
        self.wait(1.2)
        self.at("Export was")
        self.play(FadeOut(imp), FadeOut(exp), FadeOut(xs), run_time=0.5)
        bpanel = RoundedRectangle(corner_radius=0.2, width=5.6, height=4.0, stroke_width=0, fill_color=BG,
                                  fill_opacity=0.97).move_to([-3.6, 0.3, 0])
        self.add(bpanel)
        bars_bg = VGroup(*[Rectangle(width=4.0, height=0.5, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(p)
                           for p in ([-3.6, 1.0, 0], [-3.6, -0.2, 0])])
        bl = VGroup(label("EXPORT", [-3.6, 1.6, 0], PURPLE, 28, BOLD), label("IMPORT", [-3.6, 0.4, 0], BLUE, 28, BOLD))
        self.play(FadeIn(bars_bg), FadeIn(bl), run_time=0.5)
        fills = [Rectangle(width=0.5, height=0.5, stroke_width=0, fill_color=PURPLE, fill_opacity=0.9).align_to(bars_bg[0], LEFT).set_y(1.0),
                 Rectangle(width=1.5, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).align_to(bars_bg[1], LEFT).set_y(-0.2)]
        self.play(*[FadeIn(f) for f in fills], run_time=0.6)
        em = chip("EXPORT MORE SENSITIVE", PURPLE, size=28).move_to([-3.6, -1.2, 0])
        self.play(FadeIn(em), Indicate(fills[0], scale_factor=1.15), run_time=1.0)
        self.finish()


class S14Return(SpokenScene):
    def construct(self):
        w = world(self)
        field = ran_field(self, equal=False, labelled=False)
        for d in field.nuclear:
            d.set_fill(GREY).set_stroke(GREY)
        ic = icon_row(solid_block=True)
        self.add(w, field, ic)
        self.at("None of")
        self.play(*[d.animate.set_fill(GREEN).set_stroke(GREEN) for d in field.nuclear], run_time=1.6)
        imp = VGroup(cargo([-5.3, -0.5, 0], "NLS", BLUE, 0.8), receptor("importin", [-4.2, -0.55, 0], BLUE, side=LEFT, scale=0.7))
        exp = VGroup(cargo([5.2, -0.5, 0], "NES", ORANGE, 0.8), receptor("CRM1", [4.1, -0.55, 0], PURPLE, side=RIGHT, scale=0.75))
        self.play(FadeIn(imp), FadeIn(exp), run_time=0.6)
        self.play(imp.animate.shift(RIGHT * 9.0), exp.animate.shift(LEFT * 9.0), run_time=2.0, rate_func=linear)
        self.remove(imp, exp)
        self.at("Move it")
        self.play(Indicate(ic.move, color=BLUE, scale_factor=1.2), run_time=0.5)
        self.play(Indicate(ic.mutate, color=GOLD, scale_factor=1.2), run_time=0.45)
        self.play(Indicate(ic.block, color=RED_STOP, scale_factor=1.2), run_time=0.5)
        self.at("Each supports")
        self.play(Indicate(ic.items, color=GOLD, scale_factor=1.05), run_time=1.5)
        qc = cargo([-4.0, 0.0, 0], None, BLUE, 1.2)
        qq = label("?", [-4.0, 0.0, 0], BG, 48, BOLD)
        plug = lmb_plug([-2.5, 0.0, 0], 1.0)
        dp = label("DRUG PUZZLE", [-3.3, -1.2, 0], YELLOW, 34, BOLD)
        dp.set_z_index(21)
        dpbg = RoundedRectangle(corner_radius=0.1, width=dp.width + 0.4, height=dp.height + 0.2, stroke_width=0, fill_color=BG, fill_opacity=0.95).move_to(dp)
        dpbg.set_z_index(20)
        grp = VGroup(qc, qq)
        add_bob(grp, self, 0.07, 0.9)
        self.at("The page")
        self.play(FadeIn(grp, shift=UP * 0.2), FadeIn(plug, scale=1.4), run_time=1.0)
        self.at("drug puzzle")
        self.play(FadeIn(dp), FadeIn(dpbg), run_time=0.7)
        self.finish()


class S15End(EndCard):
    LINE = "Move it, mutate it, block its reader: each supports one claim."
