"""What a Root Has to Reach (plant-nutrition film 1)

COLOUR MAP: phosphate BLUE dots; nitrate GREEN dots; phloem GOLD arrow; water TEAL; soil tan;
roots cream; fungal hyphae WHITE; leaves LEAF green (yellow when starved). All schematic.
"""
import math, random
import numpy as np
from bp_style import *  # noqa: F401,F403

SOIL = "#B08A57"
TAN = "#C9A66B"
ROOTC = "#F2E3C0"
STELE = "#D9C597"
LEAF = "#4E9A52"
YEL = "#E0C341"
PURP = "#B58CD9"
PINK = "#E58FB6"
SKY = "#9FB4C8"
WATER = TEAL
C0 = np.array([-2.4, 0.0, 0.0])   # the root's centre in the soil scenes
RR = 1.3                           # root radius


def L(text, size=28, color=TEXT, **kw):
    t = T(text, size=size, color=color, **kw)
    t.set_stroke(BG, 6, background=True)
    t.set_z_index(20)
    return t


def lines(parts, size=28, color=TEXT, buff=0.12, **kw):
    return VGroup(*[L(p, size, color) for p in parts]).arrange(DOWN, buff=buff)


def plate(m, col="#2E2823", pad=0.14):
    r = RoundedRectangle(corner_radius=0.1, width=m.width + 2 * pad, height=m.height + 2 * pad, stroke_width=0,
                         fill_color=col, fill_opacity=0.93).move_to(m).set_z_index(19)
    return VGroup(r, m)


def soil_bg():
    return Rectangle(width=14.3, height=8.1, stroke_width=0, fill_color=SOIL, fill_opacity=0.2).set_z_index(-5)


# ---------- moving dots ----------
def _dot_u(d, dt):
    d._t += dt
    if d._go is not None:
        tgt, sp, kill = d._go
        v = tgt - d._b
        n = float(np.linalg.norm(v))
        if n <= sp * dt:
            d._b = tgt.copy()
            d._go = None
            if kill:
                d.set_opacity(0)
        else:
            d._b = d._b + v / n * sp * dt
    d.move_to(d._b + d._amp * np.array([math.sin(1.3 * d._t + d._ph[0]), math.cos(1.1 * d._t + d._ph[1]), 0]))


def mk_dot(color, pos, r=0.09, seed=0, amp=0.1):
    d = Dot([pos[0], pos[1], 0], radius=r, color=color)
    d._b = np.array([pos[0], pos[1], 0.0])
    d._t = 0.0
    d._ph = (seed * 1.7, seed * 2.3)
    d._amp = amp
    d._go = None
    d.add_updater(_dot_u)
    return d


def send(d, tgt, sp, kill=True):
    d._go = (np.array([tgt[0], tgt[1], 0.0]), sp, kill)


def scatter(n, seed, avoid=None, rmin=1.7, xr=6.5, yr=3.5, gap=0.55):
    rng = random.Random(seed)
    pts = []
    while len(pts) < n:
        x, y = rng.uniform(-xr, xr), rng.uniform(-yr, yr)
        if avoid is not None and math.hypot(x - avoid[0], y - avoid[1]) < rmin:
            continue
        if all(math.hypot(x - a, y - b) > gap for a, b in pts):
            pts.append((x, y))
    return pts


def phos_dots(depleted=False, n=80, seed=3, C=C0, near=2.8):
    out = []
    for i, (x, y) in enumerate(scatter(n, seed, C, 1.7)):
        d0 = math.hypot(x - C[0], y - C[1])
        if depleted and d0 < near and i % 4 != 0:
            continue
        out.append(mk_dot(BLUE, (x, y), seed=i, amp=0.09 + 0.03 * (i % 3)))
    return out


def stream_dot(C, ang, r0, rout, tr, color=GREEN, r=0.1, start=None):
    d = Dot(radius=r, color=color)
    d._r = start if start is not None else r0 + (rout - r0) * random.random()
    d._r0, d._rout, d._ang, d._C, d._tr = r0, rout, ang, np.array(C, dtype=float), tr

    def u(m, dt):
        m._r -= tr_speed(m) * dt
        if m._r < m._r0:
            m._r = m._rout
        m.move_to(m._C + m._r * np.array([math.cos(m._ang), math.sin(m._ang), 0]))
        m.set_opacity(max(0.0, min(1.0, (m._rout - m._r) / 0.4)) * m._on.get_value())

    def tr_speed(m):
        return m._tr.get_value()
    d._on = ValueTracker(1.0)
    d.add_updater(u)
    d.move_to(d._C + d._r * np.array([math.cos(ang), math.sin(ang), 0]))
    return d


def path_dot(pts, speed, phase, color=BLUE, r=0.09, rev=True):
    pts = [np.array([p[0], p[1], 0.0]) for p in pts]
    seg = [float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1)]
    tot = sum(seg)
    d = Dot(radius=r, color=color)
    d._t = 0.0

    def u(m, dt):
        m._t += dt
        p = (phase + speed * m._t) % 1.0
        if rev:
            p = 1 - p
        s = p * tot
        i = 0
        while i < len(seg) - 1 and s > seg[i]:
            s -= seg[i]
            i += 1
        m.move_to(pts[i] + (pts[i + 1] - pts[i]) * (s / max(seg[i], 1e-6)))
    d.add_updater(u)
    u(d, 0)
    return d


def pulse(m, a=0.1, w=4.0):
    m._t = 0.0
    m._h = m.height

    def u(x, dt):
        x._t += dt
        x.set_height(x._h * (1 + a * math.sin(w * x._t)))
    m.add_updater(u)
    return m


def ring_timer(c, r=0.5):
    return Circle(radius=r, color=GREY, stroke_width=4).move_to(c)


# ---------- roots ----------
def root_mob(C=C0, r=RR):
    outer = Circle(radius=r, stroke_color=ROOTC, stroke_width=4, fill_color=ROOTC, fill_opacity=0.9).move_to(C)
    stele = Circle(radius=r * 0.45, stroke_color=STELE, stroke_width=2, fill_color=STELE, fill_opacity=0.95).move_to(C)
    return VGroup(outer, stele)


HAIR_ANG = [math.radians(a) for a in range(10, 360, 36)]


def hair_group(tr, C=C0, r=RR, L0=0.4, L1=2.2, L2=None, sw=8, angs=HAIR_ANG):
    """Hairs whose length follows tracker tr (0 = short L0, 1 = L1, 2 = L2)."""
    hs = VGroup()
    for a in angs:
        d = np.array([math.cos(a), math.sin(a), 0])
        ln = Line(C + d * r, C + d * (r + L0), color=ROOTC, stroke_width=sw)
        ln.set_cap_style(CapStyleType.ROUND)

        def u(m, dt, d=d):
            v = tr.get_value()
            if L2 is None:
                length = L0 + (L1 - L0) * min(1, max(0, v))
            else:
                length = L0 + (L1 - L0) * min(1, v) + (L2 - L1) * min(1, max(0, v - 1))
            m.put_start_and_end_on(C + d * r, C + d * (r + length))
        ln.add_updater(u)
        hs.add(ln)
    return hs


def hair_tip(a, C=C0, r=RR, length=2.2):
    return C + np.array([math.cos(a), math.sin(a), 0]) * (r + length)


def hypha_paths(C=C0, s=1.0):
    ends = [(5.8, -2.8), (6.2, -0.9), (5.9, 0.9), (4.6, 1.7), (3.2, -3.4)]
    paths = []
    rng = random.Random(7)
    for k, e in enumerate(ends):
        a0 = math.atan2(e[1] - C[1], e[0] - C[0])
        start = C + np.array([math.cos(a0), math.sin(a0), 0]) * RR * s
        p = [start]
        for f in (0.3, 0.55, 0.8):
            q = start + (np.array([e[0], e[1], 0]) - start) * f
            q = q + np.array([rng.uniform(-0.25, 0.25), rng.uniform(-0.25, 0.25), 0])
            p.append(q)
        p.append(np.array([e[0], e[1], 0.0]))
        paths.append(p)
    return paths


# ---------- plants ----------
LEVELS = [(-2.2, 1.7), (-1.2, 1.6), (-0.2, 1.4), (0.8, 1.1), (1.8, 0.85)]


def leaf_u(m, dt):
    m._t += dt
    ang = m._amp * math.sin(m._w * m._t + m._ph)
    m.rotate(ang - m._ang, about_point=m._base)
    m._ang = ang
    if m._fade is not None:
        c0, c1, t0, dur = m._fade
        k = min(1.0, (m._t - t0) / dur)
        col = interpolate_color(ManimColor(c0), ManimColor(c1), k)
        m.set_fill(col, 0.85)
        m.set_stroke(col, 2)
        if k >= 1:
            m._fade = None
            m._col = c1
    if m._flick > m._t:
        m.set_opacity(0.85 * (0.55 + 0.45 * abs(math.sin(14 * m._t))))
    elif m._flick > 0:
        m._flick = 0
        m.set_opacity(0.85)


def leaf_fade(m, col, dur=2.0):
    m._fade = (m._col, col, m._t, dur)


def leaf_flick(m, secs=2.0):
    m._flick = m._t + secs


class Plant:
    def __init__(self, cx, seed=0):
        self.cx = cx
        self.stem = Line([cx, -3.1, 0], [cx, 2.4, 0], color="#3E7A45", stroke_width=16)
        self.leaves = []   # (level, side, mob)
        rng = random.Random(seed)
        for lv, (y, w) in enumerate(LEVELS):
            for s in (-1, 1):
                a = math.radians(22 + 4 * lv)
                base = np.array([cx, y, 0.0])
                dirv = np.array([s * math.cos(a), math.sin(a), 0])
                ctr = base + dirv * w / 2
                lf = Ellipse(width=w, height=0.5 + 0.03 * lv, stroke_color=LEAF, stroke_width=2,
                             fill_color=LEAF, fill_opacity=0.85).move_to(ctr)
                lf.rotate(math.atan2(dirv[1], dirv[0]), about_point=ctr)
                lf._t = rng.uniform(0, 5)
                lf._base, lf._amp, lf._w, lf._ph = base, 0.035, rng.uniform(0.8, 1.3), rng.uniform(0, 6)
                lf._ang, lf._fade, lf._col, lf._flick = 0.0, None, LEAF, 0
                lf.add_updater(leaf_u)
                self.leaves.append((lv, s, lf))
        self.bud = Ellipse(width=0.4, height=0.8, stroke_color=LEAF, stroke_width=2, fill_color=LEAF,
                           fill_opacity=0.85).move_to([cx, 2.75, 0])
        self.bud._t, self.bud._base, self.bud._amp, self.bud._w, self.bud._ph = 0, np.array([cx, 2.4, 0]), 0.0, 1, 0
        self.bud._ang, self.bud._fade, self.bud._col, self.bud._flick = 0.0, None, LEAF, 0
        self.bud.add_updater(leaf_u)
        self.roots = VGroup(*[Line([cx, -3.1, 0], [cx + dx, -3.7, 0], color=ROOTC, stroke_width=5)
                              for dx in (-0.9, -0.4, 0.4, 0.9)])
        self.group = VGroup(self.roots, self.stem, *[l[2] for l in self.leaves], self.bud)

    def lv(self, levels):
        return [l[2] for l in self.leaves if l[0] in levels]

    def mobs(self):
        return [l[2] for l in self.leaves] + [self.bud]


def soil_band():
    return Rectangle(width=14.3, height=0.8, stroke_width=0, fill_color=SOIL, fill_opacity=0.5).move_to([0, -3.4, 0])


def tile(sym, color=TAN, w=0.8, size=28):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=0.7, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=0.95)
    return VGroup(box, T(sym, size=size, color=BG, weight=BOLD).move_to(box)).set_z_index(10)


TCOL = {"N": GREEN, "P": BLUE}


def etile(sym, w=0.8):
    return tile(sym, TCOL.get(sym, TAN), w)


def rider(sym, x, ylo, yhi, speed, phase):
    t = etile(sym, 0.75)
    t._t = 0.0
    t._on = ValueTracker(0.0)

    def u(m, dt):
        m._t += dt
        f = (phase + speed * m._t) % 1.0
        m.move_to([x, ylo + (yhi - ylo) * f, 0])
        m.set_opacity(m._on.get_value() * min(1.0, math.sin(math.pi * f) * 2.5))
    t.add_updater(u)
    u(t, 0)
    return t


def gold_arrow(cx, y0=-1.9, y1=2.3):
    return Arrow([cx, y0, 0], [cx, y1, 0], buff=0, color=GOLD, stroke_width=9, tip_length=0.3)


def glass_mob():
    c = Circle(radius=0.6, stroke_color=TEXT, stroke_width=6)
    h = Line(c.get_center() + np.array([0.42, -0.42, 0]), c.get_center() + np.array([1.1, -1.1, 0]), color=TEXT,
             stroke_width=8)
    return VGroup(c, h).set_z_index(5)


def qcard():
    t = lines(["Nitrogen runs short.", "Old leaves or", "young leaves first?"], 28, TEXT)
    box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.6, height=t.height + 0.6, stroke_color=GOLD,
                           stroke_width=3, fill_color=BG, fill_opacity=0.95)
    g = VGroup(box, t.move_to(box))
    return g.move_to([3.7, 0.4, 0])


P1, P2 = -2.4, 2.4


# =========================================================== scenes
class S00Title(TitleCard):
    LESSON = "Soil, Nutrients and Partners"
    TITLE = "What a Root Has to Reach"


class S01Hook(SpokenScene):
    def construct(self):
        band = Rectangle(width=14.3, height=1.4, stroke_width=0, fill_color=SOIL, fill_opacity=0.5).move_to([0, -3.1, 0])
        rg = random.Random(5)
        dots = [mk_dot(BLUE if i % 2 else GREEN, (-6.5 + 13 * i / 33, -3.1 + rg.uniform(-0.5, 0.5)), r=0.08, seed=i, amp=0.08) for i in range(34)]
        self.add(band, *dots)
        trunk = Line([0, -2.4, 0], [0, 0.4, 0], color="#8B6B3E", stroke_width=24)
        roots = VGroup(*[Line([0, -2.4, 0], [dx, -3.6, 0], color=ROOTC, stroke_width=5) for dx in (-2, -1, 1, 2)])
        canopy = VGroup()
        cs = [(-1.0, 0.7, 1.9), (1.0, 0.7, 1.9), (0, 1.8, 2.2), (-0.8, 1.7, 1.6), (0.8, 1.7, 1.6)]
        for k, (x, y, w) in enumerate(cs):
            e = Ellipse(width=w, height=w * 0.75, stroke_color=LEAF, stroke_width=2, fill_color=LEAF, fill_opacity=0.85).move_to([x, y, 0])
            e._t, e._base, e._amp, e._w, e._ph = 0.0, np.array([0, 0.4, 0]), 0.03, 1.0, k
            e._ang, e._fade, e._col, e._flick = 0.0, None, LEAF, 0
            e.add_updater(leaf_u)
            canopy.add(e)
        self.play(FadeIn(roots), GrowFromEdge(trunk, DOWN), run_time=self.beat(0.1))
        self.play(FadeIn(canopy, scale=0.5), run_time=self.beat(0.12))
        self.at("carbon dioxide")
        a1 = Arrow([-5.2, 2.6, 0], [-2.1, 1.9, 0], buff=0, color=SKY, stroke_width=8)
        l1 = L("carbon dioxide", 30, SKY).move_to([-4.2, 3.3, 0])
        self.play(GrowArrow(a1), FadeIn(l1), run_time=self.beat(0.08))
        self.at("water")
        a2 = Arrow([0, -2.3, 0], [0, 0.3, 0], buff=0, color=WATER, stroke_width=9)
        l2 = L("water", 30, WATER).move_to([-1.2, -1.0, 0])
        self.play(GrowArrow(a2), FadeIn(l2), run_time=self.beat(0.08))
        self.at("elements")
        a3 = Arrow([3.7, -3.2, 0], [3.7, -0.7, 0], buff=0, color=TAN, stroke_width=9)
        l3 = L("mineral elements", 30, TAN).move_to([3.7, -0.3, 0])
        self.play(GrowArrow(a3), FadeIn(l3), run_time=self.beat(0.08))
        q = pulse(Text("?", font=FONT, font_size=90, color=YELLOW, weight=BOLD).move_to([3.7, 1.1, 0]), 0.15, 4)
        self.play(FadeIn(q), run_time=self.beat(0.05))
        self.at("why")
        self.play(Indicate(q, scale_factor=1.3, color=YELLOW), run_time=self.beat(0.1))
        self.finish()


def cell_mob():
    box = RoundedRectangle(corner_radius=0.5, width=5.6, height=5.4, stroke_color=LEAF, stroke_width=4,
                           fill_color=LEAF, fill_opacity=0.12).move_to([-3.2, -0.15, 0])
    return box


CHIPS = [("amino acids", TEAL, 1.2), ("lipids", PURP, -0.2), ("nucleotides", PINK, -1.6)]


def mk_chips():
    out = []
    for name, col, y in CHIPS:
        c = chip(name, col, size=32).move_to([-3.2, y, 0])
        c[0].set_fill("#1A2A25", 1.0)
        c.set_z_index(20)
        out.append(c)
    return out


class S02Molecules(SpokenScene):
    def construct(self):
        cell = cell_mob()
        rng = random.Random(4)
        mot = [mk_dot(LEAF, (-3.2 + rng.uniform(-2.3, 2.3), -0.15 + rng.uniform(-2.2, 2.2)), r=0.07, seed=i, amp=0.25) for i in range(18)]
        self.play(FadeIn(cell), run_time=self.beat(0.06))
        self.add(*mot)
        self.at("organic molecules")
        head = L("organic molecules", 34, TEXT).move_to([-3.2, 3.3, 0])
        self.play(FadeIn(head), run_time=self.beat(0.05))
        chips = mk_chips()
        for cue, ch in zip(["amino acid", "lipid", "nucleotide"], chips):
            self.at(cue)
            sq = VGroup(*[Square(0.22, stroke_width=0, fill_color=ch[0].get_stroke_color(), fill_opacity=0.9).move_to(
                ch.get_center() + np.array([rng.uniform(-2, 2), rng.uniform(-0.8, 0.8), 0])) for _ in range(6)])
            self.play(FadeIn(sq), run_time=0.3)
            self.play(*[s.animate.move_to(ch.get_center()).set_opacity(0) for s in sq], FadeIn(ch), run_time=self.beat(0.07))
        self.at("you cannot")
        head_h = Circle(radius=0.45, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.15).move_to([4.2, 2.3, 0])
        body = RoundedRectangle(corner_radius=0.4, width=1.4, height=1.9, stroke_color=TEXT, stroke_width=4,
                                fill_color=TEXT, fill_opacity=0.15).move_to([4.2, 0.95, 0])
        human = VGroup(head_h, body)
        self.play(FadeIn(human, shift=LEFT * 0.3), run_time=self.beat(0.06))
        self.at("you must")
        plate = chip("x", GOLD)  # placeholder to get style
        txt = lines(["some amino acids", "and vitamins:", "must be eaten"], 28, GOLD)
        box = RoundedRectangle(corner_radius=0.14, width=txt.width + 0.5, height=txt.height + 0.4, stroke_color=GOLD,
                               stroke_width=2.5, fill_color=GOLD, fill_opacity=0.14)
        pl = VGroup(box, txt.move_to(box)).move_to([4.2, -1.9, 0])
        self.play(FadeIn(pl, shift=UP * 0.2), run_time=self.beat(0.06))
        self.finish()


class S03Element(SpokenScene):
    def construct(self):
        cell = cell_mob()
        rng = random.Random(4)
        mot = [mk_dot(LEAF, (-3.2 + rng.uniform(-2.3, 2.3), -0.15 + rng.uniform(-2.2, 2.2)), r=0.07, seed=i, amp=0.25) for i in range(18)]
        chips = mk_chips()
        self.add(cell, *mot, *chips)
        self.at("element")
        sets = [["N", "C", "H"], ["C", "H", "O"], ["P", "N", "O"]]
        anims = []
        tiles_all = VGroup()
        for ch, s in zip(chips, sets):
            tl = VGroup(*[etile(x, 0.8) for x in s]).arrange(RIGHT, buff=0.25).move_to(ch.get_center())
            tiles_all.add(tl)
            anims.append(ReplacementTransform(ch, tl))
        self.play(*anims, run_time=self.beat(0.15))
        self.at("each element")
        arrows = VGroup(
            Arrow([-4.6, 3.6, 0], [-4.6, 2.65, 0], buff=0, color=TAN, stroke_width=8),
            Arrow([-1.8, 3.6, 0], [-1.8, 2.65, 0], buff=0, color=TAN, stroke_width=8),
            Arrow([2.6, 1.3, 0], [-0.3, 1.1, 0], buff=0, color=TAN, stroke_width=8),
            Arrow([2.6, -1.5, 0], [-0.3, -1.3, 0], buff=0, color=TAN, stroke_width=8))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=self.beat(0.15))
        self.at("outside")
        lab = L("from outside", 32, TAN).move_to([3.7, -0.2, 0])
        self.play(FadeIn(lab), run_time=self.beat(0.05))
        self.at("that is the one thing")
        self.play(FadeOut(arrows), FadeOut(lab), run_time=0.5)
        tl = chip("make an element?", GREY, size=32).move_to([3.7, 0.0, 0])
        self.play(FadeIn(tl, scale=0.8), run_time=self.beat(0.06))
        self.at("cannot")
        lock_b = RoundedRectangle(corner_radius=0.1, width=1.0, height=0.75, stroke_color=GOLD, stroke_width=3,
                                  fill_color=GOLD, fill_opacity=0.9)
        sh = Arc(radius=0.3, start_angle=0, angle=PI, color=GOLD, stroke_width=7).next_to(lock_b, UP, buff=-0.02)
        lock = VGroup(sh, lock_b).move_to([3.7, 1.7, 0])
        cross = VGroup(Line([-1.8, -0.45, 0], [1.8, 0.45, 0]), Line([-1.8, 0.45, 0], [1.8, -0.45, 0])).set_color(RED).set_stroke(width=9).move_to(tl)
        self.play(GrowFromCenter(lock), Create(cross), run_time=self.beat(0.1))
        self.at("for itself")
        self.play(Indicate(lock, color=GOLD), run_time=self.beat(0.1))
        self.finish()


EL3 = ["C", "H", "O"]
EL14 = ["N", "P", "K", "Ca", "Mg", "S", "Fe", "Mn", "Zn", "Cu", "B", "Mo", "Cl", "Ni"]


def soil_tile_pos(i):
    row, col = divmod(i, 7)
    return np.array([-4.5 + col * 1.5, -1.0 - row * 1.1, 0])


class S04List(SpokenScene):
    def construct(self):
        band = Rectangle(width=14.3, height=3.3, stroke_width=0, fill_color=SOIL, fill_opacity=0.3).move_to([0, -2.05, 0])
        cloud = VGroup(*[Circle(radius=r, stroke_color=SKY, stroke_width=3, fill_color=SKY, fill_opacity=0.18).move_to([x, y, 0])
                         for x, y, r in [(-1.4, 3.1, 0.5), (-0.5, 3.35, 0.65), (0.6, 3.3, 0.6), (1.4, 3.05, 0.45)]])
        clab = L("carbon dioxide and water", 28, SKY).move_to([4.2, 3.2, 0])
        t3 = [etile(x, 0.9) for x in EL3]
        t14 = [etile(x, 0.9) for x in EL14]
        alltl = t3 + t14
        for i, t in enumerate(alltl):
            row, col = divmod(i, 9)
            n = 9 if row == 0 else 8
            t.move_to([(col - (n - 1) / 2) * 1.35, 0.6 - row * 1.0, 0])
        self.add(band)
        self.at("17")
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in alltl], lag_ratio=0.1), run_time=self.beat(0.2))
        self.at("carbon")
        self.play(FadeIn(cloud), FadeIn(clab), run_time=0.5)
        self.play(*[t.animate.move_to([-1.2 + k * 1.2, 2.0 - (0 if False else 0) - 0.0, 0] if False else [(-1.2 + k * 1.2), 1.75, 0]) for k, t in enumerate(t3)], run_time=self.beat(0.12))
        self.at("other")
        self.play(*[t.animate.move_to(soil_tile_pos(i)) for i, t in enumerate(t14)], run_time=self.beat(0.15))
        sl = L("soil", 30, TAN).move_to([-6.0, -3.4, 0])
        self.at("mineral nutrients")
        c = lines(["17 = 3 from carbon dioxide and water", "+ 14 mineral nutrients, mostly from soil"], 28, TEXT).move_to([0, 0.35, 0])
        self.play(FadeIn(c), FadeIn(sl), run_time=0.6)
        self.finish()


class S05Rule(SpokenScene):
    def construct(self):
        band = Rectangle(width=14.3, height=3.3, stroke_width=0, fill_color=SOIL, fill_opacity=0.3).move_to([0, -2.05, 0])
        t14 = [etile(x, 0.9).move_to(soil_tile_pos(i)) for i, x in enumerate(EL14)]
        self.add(band, *t14)
        # gentle wobble so the tiles are alive
        for k, t in enumerate(t14):
            t._b = t.get_center().copy()
            t._tt = k * 0.5

            def u(m, dt):
                m._tt += dt
                m.move_to(m._b + np.array([0, 0.06 * math.sin(2 * m._tt), 0]))
            t.add_updater(u)
        labs = []
        specs = [("form", 2.9), ("how far it moves", 2.0), ("who can take it up: plant or partner", 1.1)]
        cues = ["form", "how far", "who can take"]
        for (txt, y), cue in zip(specs, cues):
            self.at(cue)
            ch = chip(txt, TEXT, size=36).move_to([0, y + 0.1, 0])
            labs.append(ch)
            self.play(FadeIn(ch, shift=UP * 0.2), run_time=0.6)
        self.play(labs[1].animate.set_color(YELLOW), labs[0].animate.set_opacity(0.7), labs[2].animate.set_opacity(0.7), run_time=0.5)
        self.at("this film")
        ruler = VGroup(Line([-6, 0, 0], [6, 0, 0], color=YELLOW, stroke_width=5),
                       *[Line([x, -0.14, 0], [x, 0.14, 0], color=YELLOW, stroke_width=4) for x in np.arange(-6, 6.1, 1.0)]).move_to([0, -3.2, 0])
        self.play(Create(ruler), run_time=self.beat(0.12))
        self.play(ruler.animate.shift(RIGHT * 0.5), run_time=self.beat(0.08))
        self.finish()


def phos_label_world(self, with_label=True):
    pass


class S06Root(SpokenScene):
    def construct(self):
        self.add(soil_bg())
        dots = phos_dots(False)
        self.play(FadeIn(VGroup(*dots)), run_time=self.beat(0.08))
        self.add(*dots)
        self.at("phosphate")
        tgt = max(dots, key=lambda d: d.get_x())
        lab = plate(L("phosphate", 32, BLUE).move_to([4.0, 2.6, 0]))
        self.play(FadeIn(lab), run_time=0.5)
        self.at("here is")
        root = root_mob()
        self.play(GrowFromCenter(root), run_time=self.beat(0.15))
        self.at("behind")
        # small inset: side view of the root with the cut
        cap = RoundedRectangle(corner_radius=0.3, width=0.6, height=1.6, stroke_color=ROOTC, stroke_width=3,
                               fill_color=ROOTC, fill_opacity=0.5).move_to([4.8, -1.8, 0])
        cut = DashedLine([4.3, -2.1, 0], [5.3, -2.1, 0], color=YELLOW, stroke_width=4)
        tiplab = plate(L("tip", 28, TEXT).next_to(cap, UP, buff=0.15).shift(LEFT * 0.0))
        self.play(FadeIn(cap), Create(cut), FadeIn(tiplab), run_time=self.beat(0.1))
        self.at("dotted")
        self.play(Indicate(VGroup(*dots[:12]), color=BLUE, scale_factor=1.3), run_time=self.beat(0.12))
        self.finish()


def ring_mob(C=C0, rin=RR, rout=2.8, op=0.13):
    return Annulus(inner_radius=rin, outer_radius=rout, stroke_width=0, fill_color=WHITE, fill_opacity=op).move_to(C)


class S07Halo(SpokenScene):
    def construct(self):
        self.add(soil_bg())
        dots = phos_dots(False)
        self.add(*dots)
        root = root_mob()
        self.add(root)
        self.at("takes")
        rng = random.Random(1)
        far = []
        for i, d in enumerate(dots):
            v = d._b - C0
            dist = float(np.linalg.norm(v))
            if dist < 2.8 and i % 4 != 0:
                surf = C0 + v / dist * (RR - 0.05)
                send(d, surf, rng.uniform(0.45, 0.9))
            elif dist > 3.0:
                far.append(d)
        self.at("runs low")
        ring = ring_mob()
        lab = plate(lines(["lower available phosphate:", "depletion zone", "(schematic)"], 28, WHITE).move_to([3.9, 2.4, 0]))
        leader = Line([2.2, 2.0, 0], [-0.1, 1.3, 0], color=WHITE, stroke_width=3)
        self.play(FadeIn(ring), FadeIn(lab), Create(leader), run_time=self.beat(0.1))
        self.at("creeps")
        for d in far:
            v = C0 - d._b
            send(d, d._b + v / np.linalg.norm(v) * 0.5, 0.07, False)
        sl = plate(L("very slow creep", 28, BLUE).move_to([3.9, -1.0, 0]))
        al = VGroup(*[Arrow([x, y, 0], [x - 0.5, y * 0.8, 0], buff=0, color=BLUE, stroke_width=4, tip_length=0.18) for x, y in [(4.9, -2.2), (4.2, 1.0 * 0 - 3.0)]])
        self.play(FadeIn(sl), run_time=self.beat(0.08))
        self.at("arrives")
        self.play(Indicate(sl, color=BLUE), run_time=self.beat(0.1))
        self.finish()


class S08Hairs(SpokenScene):
    def construct(self):
        self.add(soil_bg())
        dots = phos_dots(True)
        self.add(*dots)
        ring = ring_mob()
        root = root_mob()
        self.add(ring)
        tr = ValueTracker(0)
        hairs = hair_group(tr, L0=0.35, L1=1.1, L2=2.2)
        self.add(hairs, root)
        self.at("hairs")
        lab = plate(L("root hairs", 32, ROOTC).move_to([4.2, 2.3, 0]))
        lead = Line([3.0, 2.2, 0], list(hair_tip(HAIR_ANG[0], length=1.1)), color=ROOTC, stroke_width=3)
        self.play(FadeIn(lab), Create(lead), tr.animate.set_value(1.0), run_time=self.beat(0.15))
        self.at("tube")
        base = C0 + np.array([math.cos(HAIR_ANG[0]), math.sin(HAIR_ANG[0]), 0]) * RR
        cellc = Circle(radius=0.3, stroke_color=YELLOW, stroke_width=5).move_to(base)
        cl = plate(L("one surface cell", 28, YELLOW).move_to([4.2, 0.6, 0]))
        cl_l = Line([2.8, 0.6, 0], list(base + np.array([0.3, 0, 0])), color=YELLOW, stroke_width=3)
        self.play(Create(cellc), FadeIn(cl), Create(cl_l), run_time=self.beat(0.1))
        self.at("push")
        self.play(FadeOut(cellc), FadeOut(cl), FadeOut(cl_l), run_time=0.4)
        grains = VGroup(*[Circle(radius=0.28, stroke_color=SOIL, stroke_width=2, fill_color=SOIL, fill_opacity=0.35).move_to(
            C0 + 3.2 * np.array([math.cos(a + math.radians(18)), math.sin(a + math.radians(18)), 0])) for a in HAIR_ANG])
        self.play(FadeIn(grains), tr.animate.set_value(2.0), run_time=self.beat(0.2), rate_func=linear)
        # dots near the tips flow in
        tips = [hair_tip(a, length=2.2) for a in HAIR_ANG]
        for d in dots:
            for tp in tips:
                if np.linalg.norm(d._b - tp) < 1.0 and d._go is None:
                    send(d, tp, 0.5)
                    break
        self.at("depleted")
        dl = plate(L("depletion zone", 28, WHITE).move_to([4.2, -2.6, 0]))
        self.play(FadeIn(dl), Indicate(ring, color=WHITE), run_time=self.beat(0.1))
        self.finish()


class S09Fungus(SpokenScene):
    def construct(self):
        self.add(soil_bg())
        dots = phos_dots(True)
        self.add(*dots)
        tr = ValueTracker(2.0)
        hairs = hair_group(tr, L0=0.35, L1=1.1, L2=2.2)
        root = root_mob()
        self.add(hairs, root)
        paths = hypha_paths()
        self.at("fungal partner")
        hy = VGroup()
        for p in paths:
            hy.add(VMobject(stroke_color=WHITE, stroke_width=3).set_points_smoothly([*p]))
        self.play(LaggedStart(*[Create(h) for h in hy], lag_ratio=0.2), run_time=self.beat(0.3))
        self.at("mycorrhiza")
        lab = plate(lines(["hyphae of a mycorrhiza", "(fungal partner)"], 28, WHITE).move_to([3.8, 2.9, 0]))
        self.play(FadeIn(lab), run_time=0.6)
        self.at("thinner")
        self.play(Indicate(hy[0], color=WHITE, scale_factor=1.0), run_time=self.beat(0.1))
        self.at("they run")
        pd = VGroup()
        k = 0
        for p in paths:
            for j in range(3):
                pd.add(path_dot(p, 0.12, j / 3 + k * 0.1))
            k += 1
        self.play(FadeIn(pd), run_time=0.5)
        self.add(pd)
        self.at("bring")
        self.wait(self.beat(0.1))
        self.finish()


class S10Nitrate(SpokenScene):
    def construct(self):
        self.add(soil_bg())
        divider = Line([0, -3.8, 0], [0, 3.8, 0], color=GREY, stroke_width=3)
        CL, CR = np.array([-3.4, 0, 0]), np.array([3.4, 0, 0])
        rl = root_mob(CL, 0.9)
        rr = root_mob(CR, 0.9)
        ringl = ring_mob(CL, 0.9, 1.9)
        ringr = ring_mob(CR, 0.9, 1.7, 0.07)
        rng = random.Random(9)
        ld = []
        for i in range(26):
            a = rng.uniform(0, 2 * PI)
            r = rng.uniform(1.0, 3.0) if i % 3 == 0 else rng.uniform(1.9, 3.0)
            ld.append(mk_dot(BLUE, (CL[0] + r * math.cos(a), r * math.sin(a)), seed=i, amp=0.07))
        ll = L("phosphate", 32, BLUE).move_to([-3.4, 3.35, 0])
        lr = L("nitrate", 32, GREEN).move_to([3.4, 3.35, 0])
        sp = ValueTracker(0.04)
        nd = [stream_dot(CR, 2 * PI * i / 24 + 0.2 * (i % 3), 0.95, 3.0, sp) for i in range(24)]
        self.add(divider, ringl, ringr, rl, rr, *ld, *nd)
        self.add(ll, lr)
        self.at("different story")
        self.wait(self.beat(0.05))
        self.at("moves")
        self.play(sp.animate.set_value(0.5), run_time=0.8)
        self.at("readily")
        self.wait(0.1)
        self.at("water")
        ars = VGroup(*[Arrow(CR + 2.3 * np.array([math.cos(a), math.sin(a), 0]), CR + 1.6 * np.array([math.cos(a), math.sin(a), 0]),
                             buff=0, color=WATER, stroke_width=7, tip_length=0.2) for a in [math.radians(x) for x in range(30, 360, 60)]])
        for a in ars:
            pulse(a, 0.12, 3)
        self.play(FadeIn(ars), run_time=0.6)
        self.add(ars)
        self.at("for nitrate")
        cap = L("nitrate: reach matters less", 30, GREEN).move_to([3.4, -3.3, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.finish()


def plant_scene_base(self, cx=P1, flick=False):
    pl = Plant(cx)
    self.add(soil_band(), pl.group)
    return pl


class S11Inside(SpokenScene):
    def construct(self):
        self.add(soil_band())
        pl = Plant(P1)
        self.play(FadeIn(pl.group), run_time=self.beat(0.12))
        self.at("phloem")
        ga = gold_arrow(P1)
        self.play(GrowArrow(ga), run_time=self.beat(0.08))
        lab = L("mobile in the phloem", 30, GOLD).move_to([3.5, 0.0, 0])
        self.play(FadeIn(lab), run_time=0.5)
        riders = [rider(s, P1, -1.9, 2.3, 0.18, k * 0.25) for k, s in enumerate(["N", "P", "K", "Mg"])]
        self.add(*riders)
        self.at("out of old")
        olds = pl.lv([0, 1])
        self.play(*[Indicate(o, color=YELLOW, scale_factor=1.1) for o in olds], run_time=self.beat(0.1))
        for sym, cue, r in zip(["nitrogen", "phosphorus", "potassium", "magnesium"], ["nitrogen", "phosphorus", "potassium", "magnesium"], riders):
            self.at(cue)
            r._on.set_value(1.0)
        self.wait(self.beat(0.1))
        self.finish()


class S12Predict(SpokenScene):
    def construct(self):
        band = soil_band()
        pl = Plant(P1)
        rng = random.Random(3)
        gd = [mk_dot(GREEN, (P1 + rng.uniform(-3, 3), -3.4 + rng.uniform(-0.25, 0.25)), r=0.08, seed=i, amp=0.07) for i in range(18)]
        self.add(band, pl.group, *gd)
        self.at("nitrogen")
        keep = 0
        for i, d in enumerate(gd):
            if i % 6 != 0:
                send(d, (P1, -3.2), rng.uniform(0.3, 0.8))
        for m in pl.mobs():
            leaf_flick(m, 2.0)
        self.at("which leaves")
        q = qcard()
        self.play(FadeIn(q), run_time=0.5)
        self.at("old")
        tag_o = L("old leaves", 28, YEL).move_to([-5.7, -1.6, 0])
        ao = Arrow([-4.5, -1.6, 0], [-4.05, -1.8, 0], buff=0, color=YEL, stroke_width=5, tip_length=0.15)
        self.play(FadeIn(tag_o), GrowArrow(ao), run_time=0.4)
        self.at("young ones")
        tag_y = L("young leaves", 28, LEAF).move_to([-5.7, 1.6, 0])
        ay = Arrow([-4.45, 1.6, 0], [-3.3, 1.8, 0], buff=0, color=LEAF, stroke_width=5, tip_length=0.15)
        self.play(FadeIn(tag_y), GrowArrow(ay), run_time=0.4)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        band = soil_band()
        pl = Plant(P1)
        rng = random.Random(3)
        gd = [mk_dot(GREEN, (P1 + rng.uniform(-3, 3), -3.4 + rng.uniform(-0.25, 0.25)), r=0.08, seed=i, amp=0.07) for i in range(3)]
        q = qcard()
        tag_o = L("old leaves", 28, YEL).move_to([-5.7, -1.6, 0])
        ao = Arrow([-4.5, -1.6, 0], [-4.05, -1.8, 0], buff=0, color=YEL, stroke_width=5, tip_length=0.15)
        tag_y = L("young leaves", 28, LEAF).move_to([-5.7, 1.6, 0])
        ay = Arrow([-4.45, 1.6, 0], [-3.3, 1.8, 0], buff=0, color=LEAF, stroke_width=5, tip_length=0.15)
        self.add(band, pl.group, *gd, q, tag_o, ao, tag_y, ay)
        tc = ring_timer([5.9, -3.1, 0], 0.5)
        arc = Arc(radius=0.5, start_angle=PI / 2, angle=-2 * PI, color=GOLD, stroke_width=7).move_to(tc)
        self.add(tc)
        self.play(Create(arc), run_time=4.8, rate_func=linear)
        self.finish()


class S14Reveal(SpokenScene):
    def construct(self):
        self.add(soil_band())
        pl = Plant(P1)
        self.add(pl.group)
        ga = gold_arrow(P1)
        riders = [rider("N", P1, -1.9, 2.3, 0.18, k * 0.34) for k in range(3)]
        self.add(ga, *riders)
        self.play(*[Indicate(o, color=YELLOW, scale_factor=1.1) for o in pl.lv([0, 1])], run_time=self.beat(0.1))
        self.at("pulls")
        for r in riders:
            r._on.set_value(1.0)
        self.at("sends")
        self.wait(0.2)
        self.at("so the old")
        for m in pl.lv([0, 1]):
            leaf_fade(m, YEL, 2.0)
        lab = L("old, lower leaves first", 30, YEL).move_to([3.7, -1.3, 0])
        self.play(FadeIn(lab), run_time=0.5)
        self.finish()


def plant1_state(self):
    pl = Plant(P1)
    for m in pl.lv([0, 1]):
        m.set_fill(YEL, 0.85).set_stroke(YEL, 2)
        m._col = YEL
    return pl


class S15Immobile(SpokenScene):
    def construct(self):
        self.add(soil_band())
        p1 = plant1_state(self)
        ga = gold_arrow(P1)
        riders = [rider("N", P1, -1.9, 2.3, 0.18, k * 0.34) for k in range(3)]
        for r in riders:
            r._on.set_value(1.0)
        p2 = Plant(P2, seed=5)
        l1 = L("old leaves first", 28, YEL).move_to([P1, 3.45, 0])
        self.add(p1.group, ga, *riders, l1)
        self.play(FadeIn(p2.group), run_time=self.beat(0.08))
        fe = etile("Fe", 0.9).move_to([P2 - 1.0, -1.95, 0])
        ca = etile("Ca", 0.9).move_to([P2 + 1.0, -0.95, 0])
        self.play(FadeIn(fe, scale=0.7), run_time=0.4)
        self.play(FadeIn(ca, scale=0.7), run_time=0.4)
        self.at("once")
        self.play(Indicate(fe, color=TAN), Indicate(ca, color=TAN), run_time=self.beat(0.12))
        self.at("stay")
        self.wait(0.1)
        self.at("shortage")
        for m in p2.lv([3, 4]) + [p2.bud]:
            leaf_fade(m, YEL, 2.0)
        self.at("young leaves")
        l2 = L("young leaves first", 28, YEL).move_to([P2, 3.45, 0])
        self.play(FadeIn(l2), run_time=0.5)
        self.finish()


def two_plants(self):
    self.add(soil_band())
    p1 = plant1_state(self)
    p2 = Plant(P2, seed=5)
    for m in p2.lv([3, 4]) + [p2.bud]:
        m.set_fill(YEL, 0.85).set_stroke(YEL, 2)
        m._col = YEL
    ga = gold_arrow(P1)
    riders = [rider("N", P1, -1.9, 2.3, 0.18, k * 0.34) for k in range(3)]
    for r in riders:
        r._on.set_value(1.0)
    fe = etile("Fe", 0.9).move_to([P2 - 1.0, -1.95, 0])
    ca = etile("Ca", 0.9).move_to([P2 + 1.0, -0.95, 0])
    self.add(p1.group, p2.group, ga, *riders, fe, ca)
    return p1, p2


class S16Hedge(SpokenScene):
    def construct(self):
        p1, p2 = two_plants(self)
        g = glass_mob()
        g._t = 0.0

        def gu(m, dt):
            m._t += dt
            f = 0.5 - 0.5 * math.cos(m._t * 0.55)
            m.move_to([-2.4 + 4.8 * f, 0.3 + 0.9 * math.sin(m._t * 1.1), 0])
        g.add_updater(gu)
        gu(g, 0)
        self.add(g)
        lab = L("a clue, not a diagnosis", 32, TEXT).move_to([0, 3.4, 0])
        self.at("clues")
        self.play(FadeIn(lab), run_time=0.5)
        self.at("different shortages")
        a = p1.lv([0])[0]
        b = p2.lv([4])[0]
        self.play(Indicate(a, color=YELLOW), Indicate(b, color=YELLOW), run_time=self.beat(0.12))
        self.finish()


def mini_panel(c, w=4.0, h=4.6):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2).move_to(c)


class S17Rule(SpokenScene):
    def construct(self):
        yc = 0.9
        # panel A: depletion ring, hairs, hyphae
        ca = np.array([-4.5, yc, 0])
        s = 0.5
        pA = mini_panel(ca)
        rA = root_mob(ca, 0.6)
        ringA = ring_mob(ca, 0.6, 1.3)
        trA = ValueTracker(1.0)
        hA = hair_group(trA, C=ca, r=0.6, L0=0.3, L1=0.7, sw=5)
        hyA = VGroup()
        pdA = VGroup()
        for k, a in enumerate([0.3, -0.5, 2.6, 3.6]):
            e = ca + 1.85 * np.array([math.cos(a), math.sin(a) * 0.9, 0])
            st = ca + 0.6 * np.array([math.cos(a), math.sin(a), 0])
            hyA.add(Line(st, e, color=WHITE, stroke_width=2))
            pdA.add(path_dot([st, e], 0.2, k * 0.25, BLUE, 0.07))
        # panel B: nitrate drifting in
        cb = np.array([0.0, yc, 0])
        pB = mini_panel(cb)
        rB = root_mob(cb, 0.5)
        sp = ValueTracker(0.35)
        nB = [stream_dot(cb, 2 * PI * i / 10, 0.55, 1.8, sp, r=0.08) for i in range(10)]
        # panel C: plant with a gold arrow
        cc = np.array([4.5, yc, 0])
        pC = mini_panel(cc)
        stem = Line(cc + np.array([0, -1.9, 0]), cc + np.array([0, 1.5, 0]), color="#3E7A45", stroke_width=9)
        lv = VGroup(*[Ellipse(width=1.0, height=0.34, stroke_color=LEAF, fill_color=LEAF, fill_opacity=0.85).move_to(
            cc + np.array([sx * 0.55, y, 0])).rotate(sx * 0.35) for y in (-1.2, -0.3, 0.6) for sx in (-1, 1)])
        gC = Arrow(cc + np.array([0, -1.2, 0]), cc + np.array([0, 1.5, 0]), buff=0, color=GOLD, stroke_width=6, tip_length=0.22)
        tC = rider("N", cc[0], cc[1] - 1.2, cc[1] + 1.4, 0.2, 0.0)
        tC.scale(0.7)
        tC._on.set_value(1.0)
        self.add(soil_bg())
        self.play(FadeIn(pA), FadeIn(rA), FadeIn(ringA), FadeIn(hA), Create(hyA), run_time=self.beat(0.08))
        self.add(pdA)
        self.at("one question")
        self.play(FadeIn(pB), FadeIn(rB), run_time=0.5)
        self.add(*nB)
        self.at("again and")
        self.play(FadeIn(pC), FadeIn(stem), FadeIn(lv), GrowArrow(gC), run_time=0.6)
        self.add(tC)
        self.at("it cannot")
        t1 = L("It cannot make an element.", 32, TEXT).move_to([0, -2.1, 0])
        self.play(FadeIn(t1), run_time=0.5)
        self.at("how far does")
        t2 = L("How far does each nutrient move?", 32, GOLD).move_to([0, -2.8, 0])
        self.play(FadeIn(t2), run_time=0.5)
        self.at("how will")
        t3 = L("How will the plant reach it?", 32, TEXT).move_to([0, -3.45, 0])
        self.play(FadeIn(t3), run_time=0.5)
        self.finish()


class S18End(EndCard):
    LINE = "How far a nutrient moves shapes how a plant must reach it."
