"""Digest Outside, Fuse in Two Steps  (Biochemistrypedia explainer, lesson: Microbes, Protists and Fungi, film 2 of 2)

COLOUR MAP (same as film 1, fixed)
  GREEN  = eukaryotes (fungi, yeast, animals, plants)       BLUE/ORANGE = bacteria / archaea (not used here)
  WHITE  = starch chains and small sugars (beads)           YELLOW = enzymes / the thing being highlighted
  RED    = one mating partner's nucleus, 'no' stamps        YELLOW dot = the other partner's nucleus
  ORANGE-RED swirl = fused diploid nucleus                  TEAL = chitin (the wall)
  BEIGE  = bread
Trees and the cycle are schematic and say so on screen. No molecule is drawn.
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

WH = "#FFFFFF"
BREAD = "#D9B77E"
CRUST = "#A9763A"
SOIL = "#6B4A2B"
DIP = "#F0703C"          # diploid (fused) nucleus
LIGHTG = "#B9E3A6"
HY = 0.2                 # centre line of the joined hypha in every mating scene
HH = 2.2                 # its height
NX = 1.25                # x of the two nuclei in the joined cell


# ------------------------------------------------------------------ helpers
def motes(scene, n=22, seed=1):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=rng.uniform(0.03, 0.06), color=rng.choice([TEAL, GREY, TEXT])).set_opacity(rng.uniform(0.15, 0.32))
        d.move_to([rng.uniform(-6.8, 6.8), rng.uniform(-3.8, 3.8), 0])
        d.v = (rng.uniform(-0.25, 0.25), rng.uniform(0.1, 0.3))

        def drift(m, dt):
            m.shift([m.v[0] * dt, m.v[1] * dt, 0])
            if m.get_y() > 4.1:
                m.shift(DOWN * 8.2)
            if abs(m.get_x()) > 7.2:
                m.shift(LEFT * 14.4 * (1 if m.get_x() > 0 else -1))
        d.add_updater(drift)
        g.add(d)
    g.set_z_index(-10)
    scene.add(g)
    return g


def bob(m, amp=0.06, sp=0.9, ph=0.0):
    m._t = ph
    m._last = np.zeros(3)

    def f(mm, dt):
        mm._t += dt * sp
        new = np.array([amp * math.sin(mm._t * 1.3), amp * math.cos(mm._t), 0.0])
        mm.shift(new - mm._last)
        mm._last = new
    m.add_updater(f)
    return m


def pulse(m, base=1.0, amp=0.08, sp=2.0):
    m._pt = 0.0
    m._ps = 1.0

    def f(mm, dt):
        mm._pt += dt * sp
        s = base + amp * math.sin(mm._pt)
        mm.scale(s / mm._ps)
        mm._ps = s
    m.add_updater(f)
    return m


def pl_partial(pts, f):
    pts = [np.array(p, float) for p in pts]
    L = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(len(pts) - 1)]
    d = max(1e-3, min(1.0, f)) * sum(L)
    out = [pts[0]]
    for i, l in enumerate(L):
        if d >= l:
            out.append(pts[i + 1])
            d -= l
        else:
            out.append(pts[i] + (pts[i + 1] - pts[i]) * (d / l))
            break
    if len(out) < 2:
        out.append(pts[0] + np.array([1e-3, 0, 0]))
    return out


def pl_point(pts, f):
    return pl_partial(pts, f)[-1]


def cross_at(c, s=0.3, sw=9):
    c = np.array(list(c)[:2] + [0.0], float)
    return VGroup(Line(c + [-s, s, 0], c + [s, -s, 0], stroke_color=RED, stroke_width=sw),
                  Line(c + [-s, -s, 0], c + [s, s, 0], stroke_color=RED, stroke_width=sw))


def bread(op=1.0):
    crust = RoundedRectangle(corner_radius=1.1, width=8.0, height=5.0, stroke_color=CRUST, stroke_width=10,
                             fill_color=BREAD, fill_opacity=0.9 * op)
    crust.set_stroke(opacity=op)
    rng = random.Random(7)
    crumbs = VGroup(*[Dot(radius=rng.uniform(0.04, 0.09), color=CRUST).set_opacity(0.45 * op)
                      .move_to([rng.uniform(-3.4, 3.4), rng.uniform(-2.0, 2.0), 0]) for _ in range(16)])
    return VGroup(crust, crumbs).move_to([1.3, -0.8, 0])


def fuzz_dots(cx, cy, rx, ry, n=40, seed=3, r=0.09, op=0.75):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        a = rng.uniform(0, 2 * PI)
        d = math.sqrt(rng.random())
        g.add(Dot(radius=rng.uniform(r * 0.6, r * 1.3), color=GREEN).set_opacity(op)
              .move_to([cx + rx * d * math.cos(a), cy + ry * d * math.sin(a), 0]))
    return g


def net_segments(seed, root, ang, L, depth=5, spread=0.62):
    rng = random.Random(seed)
    segs = []

    def rec(p, a, l, d):
        q = p + l * np.array([math.cos(a), math.sin(a), 0.0])
        segs.append((p, q, d))
        if d < depth:
            for s in (-1, 1):
                rec(q, a + s * spread * rng.uniform(0.7, 1.25), l * rng.uniform(0.74, 0.86), d + 1)
    rec(np.array(root, float), ang, L, 0)
    return segs


def fit_segs(segs, cx, cy, w, h):
    pts = np.array([p for s in segs for p in (s[0], s[1])])
    lo, hi = pts.min(0), pts.max(0)
    sc = min(w / max(hi[0] - lo[0], 1e-6), h / max(hi[1] - lo[1], 1e-6))
    mid = (lo + hi) / 2
    f = lambda p: (p - mid) * sc + np.array([cx, cy, 0.0])
    return [(f(p), f(q), d) for p, q, d in segs], f


class Net(VGroup):
    """A branching hyphal network that grows with a tracker g in 0..1 (one generation of branches at a time)."""

    def __init__(self, segs, depth, color=GREEN, g=0.0, w0=9.0, dw=1.3):
        super().__init__()
        self.segs, self.D, self._last = segs, depth, None
        self.g = ValueTracker(g)
        for p, q, d in segs:
            m = VMobject(stroke_color=color, stroke_width=max(2.5, w0 - d * dw))
            m.set_cap_style(CapStyleType.ROUND)
            m.set_points_as_corners([p, p + np.array([1e-3, 0, 0])])
            m.set_stroke(opacity=0)
            self.add(m)
        self.add_updater(lambda m, dt: m._upd())
        self._upd()

    def _upd(self):
        gv = self.g.get_value()
        if gv == self._last:
            return
        self._last = gv
        u = gv * (self.D + 1)
        for m, (p, q, d) in zip(self.submobjects, self.segs):
            f = min(1.0, max(0.0, u - d))
            if f <= 0:
                m.set_stroke(opacity=0)
            else:
                m.set_points_as_corners([p, p + (q - p) * f])
                m.set_stroke(opacity=1)


def nuc(color, r=0.5, bars=True):
    c = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.85)
    g = VGroup(c)
    if bars:
        for dx in (-0.22, 0.0, 0.22):
            g.add(Line([dx * r / 0.5, -0.2 * r / 0.5, 0], [dx * r / 0.5, 0.2 * r / 0.5, 0], stroke_color=BG, stroke_width=5))
    return g


def pair(cx, sep=0.7, y=HY, r=0.5):
    a = nuc(RED, r).move_to([cx - sep, y, 0])
    b = nuc(YELLOW, r).move_to([cx + sep, y, 0])
    return VGroup(a, b)


def swirl(r=0.7):
    base = Circle(radius=r, stroke_color=DIP, stroke_width=5, fill_color=DIP, fill_opacity=0.92)
    a1 = Arc(radius=r * 0.55, start_angle=0, angle=PI * 1.3, stroke_color=RED, stroke_width=9)
    a2 = Arc(radius=r * 0.55, start_angle=PI, angle=PI * 1.3, stroke_color=YELLOW, stroke_width=9)
    g = VGroup(base, a1, a2)

    def spin(m, dt):
        c = m[0].get_center()
        m[1].rotate(dt * 0.9, about_point=c)
        m[2].rotate(dt * 0.9, about_point=c)
    g.add_updater(spin)
    return g


def mottled(r=0.5):
    g = VGroup(Circle(radius=r, stroke_color=DIP, stroke_width=4, fill_color=DIP, fill_opacity=0.9))
    spots = [(-0.4, 0.3, RED), (0.35, 0.35, YELLOW), (0.0, -0.1, RED), (-0.3, -0.4, YELLOW), (0.4, -0.3, RED)]
    for x, y, c in spots:
        g.add(Dot(radius=r * 0.2, color=c).move_to([x * r, y * r, 0]))
    return g


def flow(n=14, seed=5, y0=HY - 0.8, y1=HY + 0.8, x0=-6.4, x1=6.4, sp=0.35):
    rng = random.Random(seed)
    g = VGroup()
    for _ in range(n):
        d = Dot(radius=0.065, color=LIGHTG).set_opacity(0.55).move_to([rng.uniform(x0, x1), rng.uniform(y0, y1), 0])
        d.v = sp * rng.uniform(0.6, 1.4)

        def f(m, dt, x0=x0, x1=x1):
            m.shift([m.v * dt, 0, 0])
            if m.get_x() > x1:
                m.shift(LEFT * (x1 - x0))
        d.add_updater(f)
        g.add(d)
    return g


def beetle():
    body = Ellipse(width=0.95, height=1.35, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.35)
    head = Circle(radius=0.22, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.35).move_to([0, 0.78, 0])
    mid = Line([0, 0.6, 0], [0, -0.65, 0], stroke_color=TEAL, stroke_width=3)
    legs = VGroup(*[Line([sx * 0.45, y, 0], [sx * 0.9, y - 0.12, 0], stroke_color=TEAL, stroke_width=4) for sx in (-1, 1) for y in (0.35, 0, -0.35)])
    return VGroup(legs, body, head, mid)


def sun():
    c = Circle(radius=0.38, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.5)
    rays = VGroup(*[Line([0.55 * math.cos(a), 0.55 * math.sin(a), 0], [0.85 * math.cos(a), 0.85 * math.sin(a), 0], stroke_color=YELLOW, stroke_width=5)
                    for a in [i * PI / 4 for i in range(8)]])
    return VGroup(rays, c)


def tree_inset(cx_left, cy, k, fs):
    """Schematic cladogram: plants branch off first, fungi and animals are sisters. Spine at x = cx_left."""
    X = lambda x: cx_left + (x + 3.2) * k
    Y = lambda y: cy + y * k
    sw = 6 if k > 0.7 else 4
    ls = [Line([X(-3.2), Y(1.9), 0], [X(-3.2), Y(-1.0), 0]),
          Line([X(-3.2), Y(1.9), 0], [X(3.0), Y(1.9), 0]),
          Line([X(-3.2), Y(-1.0), 0], [X(-0.4), Y(-1.0), 0]),
          Line([X(-0.4), Y(-0.2), 0], [X(-0.4), Y(-1.8), 0])]
    top = [Line([X(-0.4), Y(-0.2), 0], [X(3.0), Y(-0.2), 0]), Line([X(-0.4), Y(-1.8), 0], [X(3.0), Y(-1.8), 0])]
    for l in ls + top:
        l.set_stroke(TEXT, sw)
    for l in top:
        l.set_stroke(GREEN, sw)
    labs = [T(n, fs, GREEN).move_to([X(3.2), Y(y), 0], aligned_edge=LEFT) for n, y in (("plants", 1.9), ("fungi", -0.2), ("animals", -1.8))]
    dots = [Dot(radius=0.09 + 0.05 * k, color=GREEN).move_to([X(3.0), Y(y), 0]) for y in (1.9, -0.2, -1.8)]
    return VGroup(*ls, *top, *dots, *labs)


def counter(val, sc=None):
    a = T("sets of chromosomes in this cell:", 28)
    n = M(str(val), 48, YELLOW)
    g = VGroup(a, n).arrange(RIGHT, buff=0.3)
    return g.move_to([0, -2.8, 0])


def corner_label(txt="schematic: a cycle found in many fungi"):
    return T(txt, 22, TEXT).move_to([-6.7, 3.5, 0], aligned_edge=LEFT)


def joined_world(scene, with_counter=True, with_corner=True, bobbing=True):
    tube = RoundedRectangle(corner_radius=0.6, width=13.4, height=HH, stroke_color=GREEN, stroke_width=5,
                            fill_color=GREEN, fill_opacity=0.22).move_to([0, HY, 0])
    dots = flow()
    nr = nuc(RED).move_to([-NX, HY, 0])
    ny = nuc(YELLOW).move_to([NX, HY, 0])
    if bobbing:
        bob(nr, 0.05, 0.9, 0.0)
        bob(ny, 0.05, 0.8, 2.0)
    scene.add(tube, dots, nr, ny)
    out = dict(tube=tube, dots=dots, nr=nr, ny=ny)
    if with_corner:
        out["corner"] = corner_label()
        scene.add(out["corner"])
    if with_counter:
        out["counter"] = counter(2)
        scene.add(out["counter"])
    return out


def question():
    q = VGroup(T("Is this cell ", 50), T("diploid", 50, DIP), T("?", 50)).arrange(RIGHT, buff=0.28, aligned_edge=DOWN)
    return q.move_to([0, 2.55, 0])


# ------------------------------------------------------------------ s00
class S00Title(TitleCard):
    LESSON = "Microbes, Protists and Fungi"
    TITLE = "Digest Outside, Fuse in Two Steps"

    def construct(self):
        motes(self)
        super().construct()


# ------------------------------------------------------------------ s01
class S01Link(SpokenScene):
    def construct(self):
        motes(self)
        big = tree_inset(-3.2, 0.2, 1.0, 36)
        sch = T("schematic", 24, TEXT).move_to([3.5, -3.1, 0])
        self.play(LaggedStart(*[FadeIn(m) for m in big], lag_ratio=0.04), FadeIn(sch), run_time=2.6)
        self.at("fungi")
        fl = big[-2]
        self.play(Indicate(fl, color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.at("animals")
        self.play(Indicate(big[-1], color=YELLOW, scale_factor=1.25), run_time=1.0)
        # fungi and animals twigs thicken: they sit side by side
        self.play(*[m.animate.set_stroke(YELLOW, 8) for m in big[3:7]], run_time=0.8)
        self.at("plants")
        self.play(Indicate(big[-3], color=YELLOW, scale_factor=1.25), run_time=1.0)
        self.at("yet a fungus")
        br = bread()
        patch = fuzz_dots(2.2, -0.5, 1.7, 1.0, 46, seed=2)
        small = tree_inset(-6.5, 2.2, 0.36, 22)
        sch2 = T("schematic", 22, TEXT).move_to([-5.3, 0.95, 0])
        self.play(Transform(big, small), Transform(sch, sch2), run_time=1.0)
        self.play(FadeIn(br, scale=0.9), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in patch], lag_ratio=0.05), run_time=2.0)
        self.at("so how does")
        qm = T("?", 150, YELLOW, weight=BOLD).move_to([2.2, 0.0, 0])
        qm.set_z_index(5)
        self.play(FadeIn(qm, scale=0.4), run_time=0.8)
        pulse(qm, 1.0, 0.07, 3.0)
        self.at("no mouth")
        c1 = chip("no mouth", RED, 30).move_to([-5.2, -2.4, 0])
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.7)
        self.at("no gut")
        c2 = chip("no gut", RED, 30).move_to([-5.2, -3.3, 0])
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ s02
class S02Hypha(SpokenScene):
    def construct(self):
        motes(self)
        br = bread()
        self.add(br)
        D = 5
        raw = net_segments(4, [0, 0, 0], 0.5, 1.5, depth=D, spread=0.58)
        segs, f = fit_segs(raw, 1.2, -0.7, 6.4, 3.7)
        root = segs[0][0]
        net = Net(segs, D, color=LIGHTG, w0=18.0, dw=2.8)
        spore = Dot(radius=0.2, color=GREEN).move_to(root + UP * 3.2)
        ring = Circle(radius=0.3, stroke_color=GREEN, stroke_width=4).move_to(spore)
        sp = VGroup(spore, ring)
        # slow bread-crumb drift and a pulsing spore ring keep the picture alive through every held sentence
        for k, m in enumerate(br[1]):
            m.v = (0.12 * (-1) ** k, 0.07 * (1 if k % 3 else -1))
            m.add_updater(lambda mm, dt: mm.shift([mm.v[0] * dt, mm.v[1] * dt, 0]))
        pulse(ring, 1.0, 0.18, 3.0)
        self.at("spore")
        self.add(net)
        self.play(FadeIn(sp, shift=DOWN * 0.3), run_time=0.5)
        self.at("land")
        self.play(sp.animate.move_to(root), run_time=1.0, rate_func=rush_into)
        self.play(Indicate(sp, color=YELLOW, scale_factor=1.4), run_time=0.8)
        self.at("it grows")
        self.play(net.g.animate.set_value(1 / (D + 1)), run_time=1.8, rate_func=linear)
        self.at("hypha")
        e = segs[0][1]
        lab = T("hypha", 40, GREEN).move_to(root + [-0.3, -0.85, 0])
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.8)
        self.at("the hypha branches")
        self.play(FadeOut(lab), net.g.animate.set_value(1.0), run_time=4.4, rate_func=linear)
        self.at("mycelium")
        ml = T("mycelium", 44, GREEN).move_to([1.2, 2.6, 0])
        self.play(FadeIn(ml, shift=DOWN * 0.15), run_time=0.8)
        self.at("that fuzz")
        fz = fuzz_dots(1.2, -0.7, 3.0, 1.7, 55, seed=9, r=0.1, op=0.6)
        self.play(FadeOut(ml), LaggedStart(*[FadeIn(d, scale=0.3) for d in fz], lag_ratio=0.03), run_time=1.5)
        ml2 = T("mold", 44, GREEN).move_to([1.2, 2.6, 0])
        self.play(FadeIn(ml2, shift=DOWN * 0.15), VGroup(br, net, fz, sp).animate.scale(0.92, about_point=[1.2, -0.7, 0]), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------ s03
class S03Wall(SpokenScene):
    def construct(self):
        motes(self)
        cy = -0.3
        tube = RoundedRectangle(corner_radius=1.1, width=13.2, height=2.2, stroke_color=TEAL, stroke_width=16,
                                fill_color=GREEN, fill_opacity=0.22).move_to([0, cy, 0])
        dots = flow(16, seed=8, y0=cy - 0.7, y1=cy + 0.7)
        self.play(FadeIn(tube, scale=0.95), FadeIn(dots), run_time=1.2)
        self.at("wall")
        wl = T("wall: contains chitin", 36, TEAL).move_to([-1.8, -2.5, 0])
        arr = Arrow([-1.8, -2.1, 0], [-1.8, cy - 1.15, 0], buff=0.0, stroke_width=6, color=TEAL, max_tip_length_to_length_ratio=0.4)
        self.play(FadeIn(wl, shift=UP * 0.15), GrowArrow(arr), run_time=1.0)
        self.play(Indicate(tube, color=TEAL, scale_factor=1.02), run_time=1.0)
        self.at("insect")
        bt = beetle().scale(1.1).move_to([4.6, 2.2, 0])
        bl = T("chitin", 34, TEAL).move_to([2.7, 2.2, 0])
        self.play(FadeIn(bt, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(bl, shift=RIGHT * 0.2), run_time=0.8)
        self.at("fungi do not")
        sn = sun().move_to([-4.6, 2.75, 0])
        self.play(FadeIn(sn, scale=0.6), run_time=0.9)
        self.at("photosynthesize")
        cr = cross_at([-4.6, 2.75], 0.55, 11)
        nl = T("no photosynthesis", 32, RED).move_to([-3.4, 1.55, 0])
        self.play(Create(cr), FadeIn(nl, shift=UP * 0.15), run_time=1.0)
        self.at("must come from")
        bd = RoundedRectangle(corner_radius=0.35, width=2.8, height=1.2, stroke_color=CRUST, stroke_width=6,
                              fill_color=BREAD, fill_opacity=0.9).move_to([4.6, -2.6, 0])
        bl2 = T("bread", 30, BG, weight=BOLD).move_to(bd)
        ar2 = Arrow([4.6, -1.95, 0], [4.6, cy - 1.15, 0], buff=0.0, stroke_width=6, color=YELLOW, max_tip_length_to_length_ratio=0.4)
        self.play(FadeIn(bd, shift=UP * 0.2), FadeIn(bl2), GrowArrow(ar2), run_time=1.0)
        self.play(Indicate(bd, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ s04
class S04Absorb(SpokenScene):
    def construct(self):
        motes(self)
        wash = Rectangle(width=13.6, height=7.6, fill_color=BREAD, fill_opacity=0.18, stroke_width=0).set_z_index(-5)
        self.add(wash)
        TIPX, TY = 1.5, 0.0
        tube = RoundedRectangle(corner_radius=0.9, width=9.2, height=1.8, stroke_color=GREEN, stroke_width=6,
                                fill_color=GREEN, fill_opacity=0.25).move_to([TIPX - 4.6 + 0.0, TY, 0])
        tube.shift(RIGHT * 0.0)
        inner = flow(8, seed=2, y0=-0.6, y1=0.6, x0=-6.4, x1=1.0, sp=0.3)
        chains, chain_lines, beads = VGroup(), VGroup(), VGroup()
        for y in (2.2, 0.0, -2.2):
            xs = [3.3 + 0.5 * i for i in range(7)]
            for a, b in zip(xs[:-1], xs[1:]):
                chain_lines.add(Line([a, y, 0], [b, y, 0], stroke_color=WH, stroke_width=4))
            for x in xs:
                beads.add(Dot(radius=0.13, color=WH).move_to([x, y, 0]))
        self.play(FadeIn(tube), FadeIn(inner), FadeIn(chain_lines), FadeIn(beads), run_time=1.5)
        self.at("growing tip")
        self.play(Indicate(tube, color=YELLOW, scale_factor=1.03), run_time=1.2)
        self.at("enzymes")
        rng = random.Random(3)
        wedges = VGroup()
        for i in range(12):
            w = Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=1, stroke_color=YELLOW).scale(0.15).rotate(rng.uniform(0, 2 * PI))
            w.move_to([TIPX + 0.2, rng.uniform(-0.3, 0.3), 0]).set_opacity(0)
            wedges.add(w)
        el = T("enzymes", 36, YELLOW).move_to([-0.6, 2.0, 0])
        tg = [[rng.uniform(2.1, 3.0), y + rng.uniform(-0.5, 0.5), 0] for y in (2.2, 0.0, -2.2) for _ in range(4)]
        self.add(wedges)
        self.play(FadeIn(el, shift=UP * 0.15),
                  LaggedStart(*[AnimationGroup(w.animate.set_opacity(1).move_to(t)) for w, t in zip(wedges, tg)], lag_ratio=0.12), run_time=2.6)
        for i, w in enumerate(wedges):
            bob(w, 0.07, 1.2, i)
        self.at("the enzymes cut")
        self.play(*[w.animate.move_to([3.8 + 0.4 * (i % 4), (2.2, 0.0, -2.2)[i // 4], 0]) for i, w in enumerate(wedges)], run_time=1.2)
        self.at("starch")
        sl = T("starch", 36, WH).move_to([5.0, 3.1, 0])
        self.play(FadeIn(sl, shift=DOWN * 0.15), run_time=0.8)
        self.at("large molecule")
        self.play(Indicate(VGroup(chain_lines, beads), color=WH, scale_factor=1.05), run_time=1.2)
        self.at("small sugars")
        rng2 = random.Random(5)
        self.play(FadeOut(chain_lines), FadeOut(sl),
                  *[b.animate.shift([rng2.uniform(-0.2, 0.2), rng2.uniform(-0.28, 0.28), 0]) for b in beads],
                  *[w.animate.move_to([2.6 + 0.2 * (i % 3), (2.2, 0.0, -2.2)[i // 4], 0]) for i, w in enumerate(wedges)], run_time=1.3)
        sg = T("small sugars", 36, WH).move_to([4.6, -3.25, 0])
        self.play(FadeIn(sg, shift=UP * 0.15), run_time=0.8)
        for i, b in enumerate(beads):
            bob(b, 0.07, 1.0, i * 0.4)
        self.at("outside the fungus")
        self.play(Indicate(beads, color=WH, scale_factor=1.15), run_time=1.4)
        self.at("then the hypha")
        self.play(FadeOut(el), run_time=0.5)
        self.at("takes the sugars in")
        tg2 = [[1.0 - rng2.uniform(0, 2.4), rng2.uniform(-0.55, 0.55), 0] for _ in beads]
        self.play(LaggedStart(*[b.animate.move_to(t) for b, t in zip(beads, tg2)], lag_ratio=0.06), FadeOut(sg), run_time=2.2)
        self.finish()


# ------------------------------------------------------------------ s05
class S05Compare(SpokenScene):
    def construct(self):
        motes(self)
        div = DashedLine([0, 3.5, 0], [0, -3.5, 0], color=GREY, stroke_width=3)
        tube = RoundedRectangle(corner_radius=0.8, width=7.0, height=1.6, stroke_color=GREEN, stroke_width=6,
                                fill_color=GREEN, fill_opacity=0.25).move_to([-3.1, 0.7, 0])
        tipx = -3.1 + 3.5
        inner = flow(6, seed=4, y0=0.2, y1=1.2, x0=-6.4, x1=tipx - 0.5, sp=0.3)
        tl = T("fungus", 38, GREEN).move_to([-4.0, 2.4, 0])
        self.play(FadeIn(tube), FadeIn(inner), FadeIn(tl), FadeIn(div), run_time=1.0)
        self.at("digests first")
        rng = random.Random(2)
        wedges = VGroup(*[Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=1, stroke_color=YELLOW).scale(0.14).rotate(rng.uniform(0, 6)).move_to([tipx, 0.7 + rng.uniform(-.3, .3), 0]).set_opacity(0) for _ in range(6)])
        self.add(wedges)
        c1 = chip("1  digest outside", YELLOW, 30).move_to([-3.1, -1.5, 0])
        self.play(LaggedStart(*[w.animate.set_opacity(1).shift([rng.uniform(0.5, 1.5), rng.uniform(-0.8, 0.8), 0]) for w in wedges], lag_ratio=0.1),
                  FadeIn(c1, shift=UP * 0.15), run_time=1.5)
        beads = VGroup(*[Dot(radius=0.12, color=WH).move_to([tipx + 0.5 + 0.3 * (i % 3), 0.7 + 0.45 * (i // 3 - 0.5), 0]) for i in range(6)])
        self.play(FadeIn(beads), run_time=0.4)
        self.at("takes food in")
        c2 = chip("2  absorb", TEAL, 30).move_to([-3.1, -2.7, 0])
        ar = Arrow([-3.1, -1.95, 0], [-3.1, -2.25, 0], buff=0, stroke_width=5, color=GREY, max_tip_length_to_length_ratio=0.9)
        self.play(*[b.animate.move_to([tipx - 0.4 - 0.4 * i, 0.7 + 0.25 * (i % 2), 0]) for i, b in enumerate(beads)],
                  FadeIn(c2, shift=UP * 0.15), GrowArrow(ar), run_time=1.8)
        self.at("most animals")
        body = Ellipse(width=5.0, height=2.8, stroke_color=GREEN, stroke_width=6, fill_color=GREEN, fill_opacity=0.15).move_to([3.6, 0.7, 0])
        gp = [[1.4, 0.7, 0], [2.4, 1.2, 0], [3.2, 0.3, 0], [4.2, 1.2, 0], [4.9, 0.3, 0], [5.8, 0.7, 0]]
        gut = VMobject(stroke_color=GREEN, stroke_width=18).set_points_smoothly([np.array(p) for p in gp])
        gut.set_stroke(opacity=0.55)
        al = T("animal", 38, GREEN).move_to([3.6, 2.4, 0])
        self.play(FadeIn(body, scale=0.9), Create(gut), FadeIn(al), run_time=1.5)
        self.at("the reverse")
        self.play(Indicate(c1, color=YELLOW, scale_factor=1.07), Indicate(c2, color=TEAL, scale_factor=1.07), run_time=1.2)
        self.at("take food into")
        d1 = chip("1  take in", TEAL, 30).move_to([3.6, -1.5, 0])
        food = Dot(radius=0.2, color=WH).move_to([0.9, 0.7, 0])
        tr = ValueTracker(0.0)
        food.add_updater(lambda m: m.move_to(pl_point(gp, tr.get_value())))
        self.add(food)
        self.play(FadeIn(d1, shift=UP * 0.15), run_time=0.6)
        self.play(tr.animate.set_value(0.55), run_time=1.6, rate_func=linear)
        self.at("digest it there")
        d2 = chip("2  digest inside", YELLOW, 30).move_to([3.6, -2.7, 0])
        ar2 = Arrow([3.6, -1.95, 0], [3.6, -2.25, 0], buff=0, stroke_width=5, color=GREY, max_tip_length_to_length_ratio=0.9)
        self.play(gut.animate.set_stroke(YELLOW, opacity=0.9), FadeIn(d2, shift=UP * 0.15), GrowArrow(ar2), run_time=1.0)
        self.play(tr.animate.set_value(1.0), run_time=1.2, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ s06
class S06Thin(SpokenScene):
    def construct(self):
        motes(self)
        cy = 0.7
        hc = np.array([-3.5, cy, 0])
        bc = np.array([3.2, cy, 0])
        rh, rb = 1.4, 2.7
        hy = Circle(radius=rh, stroke_color=TEAL, stroke_width=10, fill_color=GREEN, fill_opacity=0.28).move_to(hc)
        self.at("a thin thread")
        hl = T("hypha, cut across", 30, GREEN).move_to([-3.5, 2.75, 0])
        self.play(FadeIn(hy, scale=0.5), FadeIn(hl, shift=DOWN * 0.15), run_time=1.5)
        self.play(Indicate(hy, color=GREEN, scale_factor=1.08), run_time=1.0)

        def arrows(c, r):
            arr, ptsl = VGroup(), []
            for k in range(8):
                a = k * PI / 4 + PI / 8
                p0 = c + r * 1.02 * np.array([math.cos(a), math.sin(a), 0])
                p1 = c + r * 0.15 * np.array([math.cos(a), math.sin(a), 0])
                arr.add(Arrow(p0, p1, buff=0, stroke_width=5, color=YELLOW, max_tip_length_to_length_ratio=0.2, tip_length=0.18))
                ptsl.append((p0, p1))
            return arr, ptsl

        def travellers(ptsl, sp, seedoff):
            ds = VGroup()
            for i, (p0, p1) in enumerate(ptsl):
                d = Dot(radius=0.1, color=WH)
                L = np.linalg.norm(p1 - p0)
                d._ph = (i * 0.37 + seedoff) % 1.0
                d._p0, d._p1, d._T = p0, p1, L / sp

                def f(m, dt):
                    m._ph = (m._ph + dt / m._T) % 1.0
                    m.move_to(m._p0 + (m._p1 - m._p0) * m._ph)
                d.add_updater(f)
                f(d, 0)
                ds.add(d)
            return ds

        self.at("every part")
        a1, p1l = arrows(hc, rh)
        sl = T("shorter\ntransport distance", 28, YELLOW).move_to([-3.5, -2.15, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in a1], lag_ratio=0.08), FadeIn(sl, shift=UP * 0.15), run_time=2.0)
        t1 = travellers(p1l, 1.1, 0.0)
        self.add(t1)
        self.at("close to the surface")
        bl = Circle(radius=rb, stroke_color=GREY, stroke_width=8, fill_color=GREY, fill_opacity=0.22).move_to(bc)
        self.play(FadeIn(bl, scale=0.6), run_time=1.0)
        a2, p2l = arrows(bc, rb)
        ll = T("longer\ntransport distance", 28, YELLOW).move_to([3.2, -2.45, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in a2], lag_ratio=0.06), FadeIn(ll, shift=UP * 0.15), run_time=1.4)
        t2 = travellers(p2l, 1.1, 0.2)
        self.add(t2)
        self.at("food comes in")
        self.play(Indicate(t1, color=WH, scale_factor=1.3), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ s07
class S07Yeast(SpokenScene):
    def construct(self):
        motes(self)
        D = 4
        raw = net_segments(6, [0, 0, 0], 0.4, 1.3, depth=D, spread=0.7)
        segs, _ = fit_segs(raw, 0.0, 0.2, 9.5, 4.4)
        net = Net(segs, D, g=1.0)
        self.play(FadeIn(net), run_time=0.9)
        self.at("threads")
        cr = cross_at([0, 0.2], 1.0, 14)
        self.play(Create(cr), run_time=0.9)
        self.at("a yeast")
        cell = Ellipse(width=4.8, height=3.4, stroke_color=GREEN, stroke_width=8, fill_color=GREEN, fill_opacity=0.28).move_to([-1.6, 0.0, 0])
        self.play(FadeOut(net), FadeOut(cr), FadeIn(cell, scale=0.5), run_time=1.2)
        yl = T("yeast", 48, GREEN).move_to([-1.6, 2.5, 0])
        self.play(FadeIn(yl, shift=DOWN * 0.15), run_time=0.8)
        self.at("single cell")
        self.play(Indicate(cell, color=GREEN, scale_factor=1.06), run_time=1.3)
        self.at("baker's yeast")
        self.play(Indicate(cell, color=YELLOW, scale_factor=1.04), run_time=1.0)
        self.at("budding")
        bud = Circle(radius=0.05, stroke_color=GREEN, stroke_width=8, fill_color=GREEN, fill_opacity=0.28).move_to([0.45, 0.4, 0])
        bl = T("budding", 44, YELLOW).move_to([3.6, 2.4, 0])
        self.add(bud)
        self.play(bud.animate.scale(14).move_to([1.15, 0.5, 0]), FadeIn(bl, shift=DOWN * 0.15), run_time=2.4)
        self.at("pinching")
        self.play(bud.animate.move_to([3.6, 0.3, 0]), run_time=1.8)
        self.at("larger one")
        self.play(Indicate(cell, color=GREEN, scale_factor=1.06), bud.animate.shift([0.4, -0.5, 0]), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ s08
class S08Mating(SpokenScene):
    def construct(self):
        motes(self)
        br = bread()
        self.add(br)
        lab = corner_label()
        tl = ValueTracker(-4.2)
        tr = ValueTracker(4.2)
        tubeL = always_redraw(lambda: RoundedRectangle(corner_radius=0.6, width=max(1.3, tl.get_value() + 6.8), height=HH, stroke_color=GREEN, stroke_width=5,
                                                       fill_color=GREEN, fill_opacity=0.22).move_to([(tl.get_value() - 6.8) / 2, HY, 0]))
        tubeR = always_redraw(lambda: RoundedRectangle(corner_radius=0.6, width=max(1.3, 6.8 - tr.get_value()), height=HH, stroke_color=GREEN, stroke_width=5,
                                                       fill_color=GREEN, fill_opacity=0.22).move_to([(tr.get_value() + 6.8) / 2, HY, 0]))
        nl = nuc(RED)
        ny = nuc(YELLOW)
        nl.add_updater(lambda m: m.move_to([tl.get_value() - 1.2, HY, 0]))
        ny.add_updater(lambda m: m.move_to([tr.get_value() + 1.2, HY, 0]))
        nl.move_to([tl.get_value() - 1.2, HY, 0])
        ny.move_to([tr.get_value() + 1.2, HY, 0])
        dots = flow(12, seed=3)
        self.add(tubeL, tubeR, dots, nl, ny)
        self.play(FadeOut(br), FadeIn(lab), run_time=1.4)
        self.at("fungi mate")
        self.play(Indicate(nl, scale_factor=1.25), Indicate(ny, scale_factor=1.25), run_time=1.2)
        self.at("two hyphae")
        self.wait(0.3)
        self.at("mating types")
        t1 = T("mating type 1", 30, RED).move_to([-4.0, -1.6, 0])
        t2 = T("mating type 2", 30, YELLOW).move_to([4.0, -1.6, 0])
        self.play(FadeIn(t1, shift=UP * 0.15), FadeIn(t2, shift=UP * 0.15), run_time=1.0)
        self.at("grow toward")
        self.play(tl.animate.set_value(-0.05), tr.animate.set_value(0.05), run_time=1.6, rate_func=smooth)
        self.at("meet")
        wall = Line([0, HY - HH / 2, 0], [0, HY + HH / 2, 0], stroke_color=TEXT, stroke_width=7)
        self.play(FadeIn(wall), Flash(np.array([0, HY, 0]), color=YELLOW, flash_radius=0.8), run_time=0.9)
        self.at("their cytoplasm")
        joined = RoundedRectangle(corner_radius=0.6, width=13.6, height=HH, stroke_color=GREEN, stroke_width=5,
                                  fill_color=GREEN, fill_opacity=0.22).move_to([0, HY, 0])
        self.remove(tubeL, tubeR)
        self.add(joined)
        joined.set_z_index(-1)
        self.play(FadeOut(wall), FadeOut(t1), FadeOut(t2), run_time=1.0)
        mid = VGroup(*[Dot(radius=0.07, color=LIGHTG).set_opacity(0.8).move_to([0.1 * k - 0.3, HY + 0.2 * (k % 3 - 1), 0]) for k in range(5)])
        self.add(mid)
        self.play(*[d.animate.shift([(-1) ** k * 1.2, 0, 0]) for k, d in enumerate(mid)], run_time=1.5)
        self.at("this step")
        self.wait(0.2)
        self.at("plasmogamy")
        pl = T("plasmogamy: cytoplasm joins", 40, GREEN).move_to([0, 2.45, 0])
        self.play(FadeIn(pl, shift=DOWN * 0.15), Indicate(joined, color=GREEN, scale_factor=1.03), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ s09
class S09TwoNuclei(SpokenScene):
    def construct(self):
        motes(self)
        w = joined_world(self, with_counter=False)
        self.at("haploid nucleus")
        l1 = T("haploid: 1 set", 32, RED).move_to([-2.9, 2.35, 0])
        l2 = T("haploid: 1 set", 32, YELLOW).move_to([2.9, 2.35, 0])
        self.play(FadeIn(l1, shift=DOWN * 0.15), Indicate(w["nr"], scale_factor=1.3), run_time=1.0)
        self.play(FadeIn(l2, shift=DOWN * 0.15), Indicate(w["ny"], scale_factor=1.3), run_time=1.0)
        self.at("one set of chromosomes")
        self.play(Circumscribe(w["nr"], color=RED, buff=0.15), Circumscribe(w["ny"], color=YELLOW, buff=0.15), run_time=1.6)
        self.at("holds both")
        c = counter(1)
        self.play(FadeIn(c, shift=UP * 0.2), run_time=0.9)
        self.at("one from each partner")
        c2 = counter(2)
        self.play(Transform(c, c2), Indicate(w["nr"], scale_factor=1.25), Indicate(w["ny"], scale_factor=1.25), run_time=1.4)
        self.at("side by side")
        self.play(w["nr"].animate.shift(LEFT * 0.25), w["ny"].animate.shift(RIGHT * 0.25), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ s10
class S10Predict(SpokenScene):
    def construct(self):
        motes(self)
        w = joined_world(self)
        self.at("two sets of chromosomes")
        c = w["counter"]
        self.play(Indicate(c[1], color=YELLOW, scale_factor=1.6), run_time=1.2)
        self.at("in one cell")
        self.play(Circumscribe(w["tube"], color=GREEN, buff=0.1), run_time=1.6)
        self.at("so is this cell")
        q = question()
        self.play(Write(q), run_time=1.6)
        self.at("think about where")
        self.play(Indicate(w["nr"], scale_factor=1.35), Indicate(w["ny"], scale_factor=1.35), run_time=1.5)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        motes(self)
        w = joined_world(self)
        q = question()
        self.add(q)
        ring_bg = Circle(radius=0.5, stroke_color=GREY, stroke_width=5).move_to([6.0, 2.9, 0])
        bars = VGroup(Rectangle(width=0.1, height=0.4, fill_color=TEXT, fill_opacity=1, stroke_width=0).move_to([5.9, 2.9, 0]),
                      Rectangle(width=0.1, height=0.4, fill_color=TEXT, fill_opacity=1, stroke_width=0).move_to([6.1, 2.9, 0]))
        tr = ValueTracker(1.0)
        arc = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=2 * PI * max(tr.get_value(), 0.001), stroke_color=YELLOW, stroke_width=7, arc_center=[6.0, 2.9, 0]))
        self.add(ring_bg, bars, arc)
        self.play(tr.animate.set_value(0.0), run_time=4.9, rate_func=linear)
        self.finish()


# ------------------------------------------------------------------ s12
class S12Reveal(SpokenScene):
    def construct(self):
        motes(self)
        w = joined_world(self)
        q = question()
        self.add(q)
        self.at("not yet")
        cr = cross_at(q[1].get_center(), 0.45, 10)
        self.play(Create(cr), run_time=0.9)
        self.at("a diploid nucleus")
        ghost = swirl(0.75).move_to([-2.6, 2.5, 0])
        self.play(FadeOut(q), FadeOut(cr), FadeOut(w["counter"]), FadeIn(ghost, scale=0.5), run_time=1.2)
        self.at("both sets")
        gl = T("one nucleus, both sets", 34, DIP).move_to([0.2, 2.5, 0], aligned_edge=LEFT)
        gl.align_to([-1.4, 0, 0], LEFT)
        self.play(FadeIn(gl, shift=RIGHT * 0.2), run_time=0.9)
        self.at("here the two sets")
        self.play(FadeOut(ghost), FadeOut(gl), run_time=0.8)
        self.at("two separate nuclei")
        self.play(Indicate(w["nr"], scale_factor=1.4), Indicate(w["ny"], scale_factor=1.4), run_time=1.6)
        self.at("a cell like this")
        dk = T("dikaryon: two separate haploid nuclei", 36, TEXT).move_to([0, 2.5, 0])
        self.play(FadeIn(dk, shift=DOWN * 0.15), run_time=1.0)
        self.at("mushroom")
        tg = T("in mushroom-forming fungi,\nthis stage lasts long", 30, GREEN).move_to([0, -2.75, 0])
        self.play(FadeIn(tg, shift=UP * 0.15), run_time=1.0)
        self.at("forming fungi")
        septa = VGroup(*[Line([x, HY - HH / 2, 0], [x, HY + HH / 2, 0], stroke_color=TEXT, stroke_width=5) for x in (-2.2, 2.2)])
        self.play(FadeIn(septa), run_time=0.8)
        self.at("can last")
        src = VGroup(w["nr"], w["ny"])
        pl, pr = pair(-4.4), pair(4.4)
        self.play(TransformFromCopy(src, pl), TransformFromCopy(src, pr), run_time=1.6)
        self.at("a long time")
        self.play(Indicate(pl, scale_factor=1.15), Indicate(pr, scale_factor=1.15), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ s13
class S13Karyogamy(SpokenScene):
    def construct(self):
        motes(self)
        w = joined_world(self, with_counter=False)
        septa = VGroup(*[Line([x, HY - HH / 2, 0], [x, HY + HH / 2, 0], stroke_color=TEXT, stroke_width=5) for x in (-2.2, 2.2)])
        pl, pr = pair(-4.4), pair(4.4)
        side = VGroup(pl, pr).set_opacity(0.4)
        self.add(septa, side)
        self.at("only a later step")
        lt = T("a later step", 36, YELLOW).move_to([0, 2.5, 0])
        self.play(FadeIn(lt, shift=DOWN * 0.15), run_time=0.9)
        self.at("fuses the two nuclei")
        self.play(w["nr"].animate.move_to([-0.55, HY, 0]), w["ny"].animate.move_to([0.55, HY, 0]), run_time=1.6)
        self.at("into one diploid")
        sw = swirl(0.75).move_to([0, HY, 0])
        self.play(FadeOut(lt), FadeIn(sw, scale=0.6), FadeOut(w["nr"]), FadeOut(w["ny"]), run_time=1.3)
        self.at("diploid nucleus")
        dl = T("diploid: 2 sets in one nucleus", 36, DIP).move_to([0, 2.5, 0])
        self.play(FadeIn(dl, shift=DOWN * 0.15), run_time=0.9)
        self.at("that step is")
        kl = T("karyogamy", 54, YELLOW, weight=BOLD).move_to([0, -2.1, 0])
        self.play(FadeIn(kl, scale=0.7), run_time=1.0)
        self.at("joins cells")
        t1 = T("plasmogamy = cells join", 34, GREEN).move_to([0, -2.0, 0])
        self.play(FadeOut(kl), run_time=0.4)
        self.play(FadeIn(t1, shift=UP * 0.15), Indicate(w["tube"], color=GREEN, scale_factor=1.03), run_time=1.2)
        self.at("joins nuclei")
        t2 = T("karyogamy = nuclei join", 34, YELLOW).move_to([0, -3.0, 0])
        self.play(FadeIn(t2, shift=UP * 0.15), Indicate(sw, scale_factor=1.3), run_time=1.2)
        self.finish()


# ------------------------------------------------------------------ s14
class S14Meiosis(SpokenScene):
    def construct(self):
        motes(self)
        tube = RoundedRectangle(corner_radius=0.6, width=13.4, height=HH, stroke_color=GREEN, stroke_width=5,
                                fill_color=GREEN, fill_opacity=0.22).move_to([0, HY, 0])
        dots = flow()
        sw = swirl(0.8).move_to([0, HY, 0])
        corner = corner_label()
        self.add(tube, dots, sw, corner)
        self.at("meiosis")
        ml = T("meiosis", 48, YELLOW, weight=BOLD).move_to([0, 2.5, 0])
        self.play(FadeIn(ml, shift=DOWN * 0.15), run_time=0.8)
        self.at("follows")
        a, b = mottled(0.55).move_to([0, HY, 0]), mottled(0.55).move_to([0, HY, 0])
        self.add(a, b)
        self.play(FadeOut(sw), a.animate.move_to([-1.2, HY, 0]), b.animate.move_to([1.2, HY, 0]), run_time=1.4)
        self.at("the cycle comes back")
        c, d = mottled(0.45).move_to(a), mottled(0.45).move_to(b)
        self.add(c, d)
        self.play(a.animate.move_to([-3.4, HY, 0]).scale(0.82), c.animate.move_to([-1.1, HY, 0]),
                  b.animate.move_to([3.4, HY, 0]).scale(0.82), d.animate.move_to([1.1, HY, 0]), run_time=1.6)
        self.at("where it began")
        nn = VGroup(a, c, d, b)
        self.play(*[Indicate(n, scale_factor=1.25) for n in nn], run_time=1.4)
        self.at("it makes haploid spores")
        soil = Rectangle(width=13.6, height=1.1, fill_color=SOIL, fill_opacity=0.9, stroke_width=0).move_to([0, -3.25, 0]).set_z_index(-3)
        tag = T("spore number and packaging vary among fungi", 24, TEXT).move_to([0, 2.5, 0])
        spores = VGroup(*[Circle(radius=0.68, stroke_color=GREEN, stroke_width=6, fill_color=GREEN, fill_opacity=0.25).move_to(n) for n in nn])
        self.play(FadeOut(ml), run_time=0.4)
        self.play(FadeIn(soil), FadeIn(tag), LaggedStart(*[Create(s) for s in spores], lag_ratio=0.15), run_time=1.6)
        self.at("each carrying one set")
        grp = [VGroup(s, n) for s, n in zip(spores, nn)]
        self.play(*[g.animate.shift([(i - 1.5) * 0.4, -3.05, 0]) for i, g in enumerate(grp)], run_time=2.3, rate_func=smooth)
        self.at("again")
        sprouts = VGroup(*[Line(g[0].get_center() + [0, 0.62, 0], g[0].get_center() + [0.05 * (-1) ** i, 1.1, 0], stroke_color=GREEN, stroke_width=7)
                           for i, g in enumerate(grp)])
        self.play(LaggedStart(*[Create(s) for s in sprouts], lag_ratio=0.2), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------ s15
class S15Close(SpokenScene):
    def construct(self):
        motes(self)
        names1 = [("spore", GREEN), ("hypha", GREEN), ("enzymes out", YELLOW), ("sugars in", WH)]
        names2 = [("plasmogamy", GREEN), ("dikaryon", TEXT), ("karyogamy", YELLOW), ("meiosis", DIP), ("spores", GREEN)]

        def row(names, y):
            chips = [chip(n, c, 26, pad=0.2) for n, c in names]
            g = VGroup(*chips).arrange(RIGHT, buff=0.62)
            g.move_to([0, y, 0])
            arrs = [Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.06, stroke_width=5, color=GREY,
                          max_tip_length_to_length_ratio=0.6) for i in range(len(chips) - 1)]
            return chips, arrs

        c1, a1 = row(names1, 1.4)
        c2, a2 = row(names2, -1.3)
        allc = VGroup(*c1, *c2, *a1, *a2)
        r1l = T("eating", 30, TEXT).move_to([0, 2.7, 0])
        r2l = T("mating", 30, TEXT).move_to([0, -0.2, 0])
        for c in c1 + c2:
            c[0].set_stroke(opacity=0.3).set_fill(opacity=0.03)
            c[1].set_opacity(0.35)
        for a in a1 + a2:
            a.set_opacity(0.3)
        self.add(allc)
        self.play(FadeIn(r1l), FadeIn(r2l), run_time=0.6)
        dot = Dot(radius=0.16, color=YELLOW).move_to(c1[0].get_center() + DOWN * 0.7)
        self.add(dot)

        def lit(chips, arrs, i):
            anims = [chips[i][0].animate.set_stroke(opacity=1).set_fill(opacity=0.16), chips[i][1].animate.set_opacity(1)]
            if i > 0:
                anims.append(arrs[i - 1].animate.set_opacity(1))
            return anims

        self.at("a fungus eats")
        self.play(*lit(c1, a1, 0), *lit(c1, a1, 1), dot.animate.move_to(c1[1].get_center() + DOWN * 0.7), run_time=1.2)
        self.at("digesting outside")
        self.play(*lit(c1, a1, 2), dot.animate.move_to(c1[2].get_center() + DOWN * 0.7), run_time=1.2)
        self.at("absorbing")
        self.play(*lit(c1, a1, 3), dot.animate.move_to(c1[3].get_center() + DOWN * 0.7), run_time=1.2)
        self.at("and it mates")
        self.play(*lit(c2, a2, 0), dot.animate.move_to(c2[0].get_center() + DOWN * 0.7), run_time=1.2)
        self.at("in two steps")
        self.play(*lit(c2, a2, 1), *lit(c2, a2, 2), *lit(c2, a2, 3), *lit(c2, a2, 4), dot.animate.move_to(c2[4].get_center() + DOWN * 0.7), run_time=1.6)
        self.at("cells fuse first")
        self.play(Indicate(c2[0], color=GREEN, scale_factor=1.25), run_time=1.0)
        self.at("nuclei later")
        self.play(Indicate(c2[2], color=YELLOW, scale_factor=1.25), dot.animate.move_to(c2[2].get_center() + DOWN * 0.7), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------ s16
class S16End(EndCard):
    LINE = "Fungi digest outside, then absorb, and fuse cells before nuclei."
