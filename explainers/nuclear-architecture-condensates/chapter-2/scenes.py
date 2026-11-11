"""Real Bodies, Real Tests: chapter 2, one carried nucleus.

COLOR MAP (chapter 1's, plus GREEN = RNA)
  BLUE   protein molecules
  TEAL   droplets / dense phase
  ORANGE binding sites
  YELLOW saturation concentration
  PURPLE DNA / chromatin
  GREEN  RNA
  GREY   outlines, leader lines
  TEXT   words
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
P_LIGHT = "#D9C4F0"
P_MID = "#B58CD9"
P_DEEP = "#8556B0"
A_COL = "#E8D2FF"
B_COL = "#7A52A8"

C = np.array([-1.5, 0.0, 0.0])
R = 3.2
LAB_X = 2.35                      # left edge of the label column
NC = C + np.array([-0.5, -0.7, 0.0])   # nucleolus centre
NS_BIG = 1.3                     # nucleolus scale while it is the subject
NS_SMALL = 0.78                   # nucleolus scale once the other bodies join

BODY_POS = {                      # relative to C
    "speckles": (0.3, 1.9),
    "cajal": (1.9, 0.9),
    "pml": (0.6, 0.5),
    "para": (2.3, -0.4),
}
BODY_R = {"speckles": .36, "cajal": .26, "pml": .30, "para": .32}
SEC = {"light": (20, 140), "mid": (140, 260), "deep": (260, 380)}
TINT = {"light": P_LIGHT, "mid": P_MID, "deep": P_DEEP}


def bpos(name):
    return C + np.array([*BODY_POS[name], 0.0])


# ---------------------------------------------------------------- basics
def nucleus(c=C, r=R):
    return Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=.22).move_to(c)


def protein_field(c=C, n=40, seed=11, radius=R, rad=.065, op=.62):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(n):
        a = rng.uniform(0, TAU)
        rr = np.sqrt(rng.uniform(.04, (radius - .18) ** 2))
        d = Dot(c + [rr * np.cos(a), rr * np.sin(a), 0], radius=rad, color=BLUE)
        d.set_opacity(op)
        d.velocity = np.array([rng.uniform(-.32, .32), rng.uniform(-.28, .28), 0])

        def drift(m, dt, centre=np.array(c, dtype=float).copy(), lim=radius - .15):
            m.shift(m.velocity * dt)
            if np.linalg.norm((m.get_center() - centre)[:2]) > lim:
                m.shift(-2 * m.velocity * dt)
                m.velocity *= -1
        d.add_updater(drift)
        dots.add(d)
    return dots


class Glow(VGroup):
    BASE = (.08, .12, .42)

    def __init__(self, p, r, k=1.0):
        super().__init__(
            Circle(radius=r * 1.65, stroke_width=0, fill_color=BLUE).move_to(p),
            Circle(radius=r * 1.15, stroke_width=0, fill_color=TEXT).move_to(p),
            Circle(radius=r, stroke_width=0, fill_color=BLUE).move_to(p),
        )
        self.set_level(k)

    def set_level(self, k):
        for c, b in zip(self.submobjects, self.BASE):
            c.set_fill(opacity=b * k)
        return self


def glow_anim(g, k0, k1, run_time=1.0):
    return UpdateFromAlphaFunc(g, lambda m, a: m.set_level(k0 + (k1 - k0) * a), run_time=run_time)


def glow_set():
    gs = {"nucleolus": Glow(NC, .5)}
    for k in BODY_POS:
        gs[k] = Glow(bpos(k), BODY_R[k])
    return gs


def lab(text, color=TEXT, x=LAB_X, y=0.0, size=28, align=LEFT):
    t = T(text, size, color)
    t.move_to([x, y, 0], aligned_edge=align)
    return t


def leader(label, target, color=GREY):
    return Line(label.get_left() + LEFT * .1, target, stroke_color=color, stroke_width=2.5)


def schematic():
    return T("schematic", 28, GREY).move_to([-6.75, 3.45, 0], aligned_edge=LEFT)


def dial(centre=ORIGIN, value=.30, with_label=True):
    arc = Arc(radius=.72, start_angle=PI, angle=-PI, color=GREY, stroke_width=5).move_to(centre)
    ticks = VGroup(*[Line(centre + [.62 * np.cos(PI - a), .62 * np.sin(PI - a), 0],
                          centre + [.76 * np.cos(PI - a), .76 * np.sin(PI - a), 0],
                          color=GREY, stroke_width=3) for a in np.linspace(0, PI, 7)])
    ang = PI - value * PI
    needle = Line(centre, centre + [.58 * np.cos(ang), .58 * np.sin(ang), 0], color=TEXT, stroke_width=5)
    hub = Dot(centre, radius=.08, color=TEXT)
    g = VGroup(arc, ticks, needle, hub)
    if with_label:
        g.add(T("total protein", 28).next_to(arc, UP, buff=.38))
    return g


DIAL_CORNER = np.array([-5.85, 2.55, 0.0])


def dial_icon(value=.60):
    return dial(DIAL_CORNER, value, with_label=False).scale(.42, about_point=DIAL_CORNER)


# ---------------------------------------------------------------- chromatin territories
def _in_sector(p, k, margin=.13, rmin=.5, rmax=R - .4):
    d = p - C[:2]
    r = np.hypot(*d)
    if r < rmin or r > rmax:
        return False
    a0, a1 = [np.radians(x) for x in SEC[k]]
    rel = (np.arctan2(d[1], d[0]) - a0) % TAU
    return margin < rel < (a1 - a0) - margin


def walk(k, seed, n=71, step=.34, rmax=R - .4):
    rng = np.random.default_rng(seed)
    a_mid = np.radians(sum(SEC[k]) / 2)
    p = C[:2] + 1.7 * np.array([np.cos(a_mid), np.sin(a_mid)])
    v = np.array([1.0, 0.0])
    pts = [p]
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        nv = v * .55 + rng.normal(size=2) * .6
        nv = nv / np.linalg.norm(nv) * step
        q = pts[-1] + nv
        if _in_sector(q, k, rmax=rmax):
            pts.append(q)
            v = nv
        else:
            v = -v + rng.normal(size=2) * .3
    return [np.array([x, y, 0.0]) for x, y in pts]


class Terr(VGroup):
    def __init__(self, hic=False):
        super().__init__()
        self.secs, self.segs, self.kind, self.yarn, self.region_of, self.outer = [], [], [], VGroup(), [], []
        for i, k in enumerate(SEC):
            a0, a1 = SEC[k]
            s = Sector(radius=R - .1, angle=np.radians(a1 - a0 - 4), start_angle=np.radians(a0 + 2),
                       arc_center=C, stroke_width=0, fill_color=TINT[k], fill_opacity=.22)
            self.secs.append(s)
            pts = walk(k, 40 + i)
            segs = VGroup()
            for j in range(10):
                chunk = pts[j * 7: j * 7 + 8]
                seg = VMobject(stroke_color=TINT[k], stroke_width=3.5).set_points_smoothly(chunk)
                segs.add(seg)
            self.segs.append(segs)
            self.region_of.append(k)
            order = sorted(range(10), key=lambda j: -np.hypot(*(segs[j].get_center() - C)[:2]))
            kinds = ["A"] * 10
            for j in order[:3]:
                kinds[j] = "B"
            self.outer.append(set(order[:3]))
            kinds[order[5]] = "B"
            self.kind.append(kinds)
            for sd in (7, 8):
                yp = walk(k, 100 + i * 3 + sd, n=100, step=.2)
                y = VMobject(stroke_color=TINT[k], stroke_width=2).set_points_smoothly(yp)
                y.set_stroke(opacity=0)
                self.yarn.add(y)
            self.add(s, segs)
        self.add(self.yarn)
        self.level = 1.0
        if hic:
            self.apply_hic(moved=True)

    def set_level(self, f):
        self.level = f
        for s in self.secs:
            s.set_fill(opacity=.22 * f)
        for segs in self.segs:
            for sg in segs:
                sg.set_stroke(opacity=f)
        return self

    def outward(self, i, j):
        sg = self.segs[i][j]
        d = sg.get_center() - C
        d[2] = 0
        dist = np.linalg.norm(d)
        return d / dist * max(0.0, (R - .42) - dist)

    def apply_hic(self, moved=True):
        for i in range(3):
            for j in range(10):
                sg = self.segs[i][j]
                if self.kind[i][j] == "A":
                    sg.set_stroke(A_COL, width=5)
                else:
                    sg.set_stroke(B_COL, width=7)
                    if moved and j in self._outer(i):
                        sg.shift(self.outward(i, j))

    def _outer(self, i):
        return self.outer[i]


def hic_pairs(t):
    """Segments that touch in space: (region, seg) pairs, fixed."""
    return [((0, 1), (1, 2)), ((0, 5), (2, 3)), ((1, 6), (2, 8)), ((0, 8), (1, 0)), ((1, 4), (2, 1)), ((0, 3), (2, 6))]


def blink_arcs(t, pairs):
    arcs = VGroup()
    for n, ((i1, j1), (i2, j2)) in enumerate(pairs):
        p, q = t.segs[i1][j1].get_center(), t.segs[i2][j2].get_center()
        a = ArcBetweenPoints(p, q, angle=.9 * (-1) ** n).set_stroke(TEXT, 3)
        a.t = n * .9
        a.freq = 1.4 + .15 * n

        def blink(m, dt):
            m.t += dt
            m.set_stroke(opacity=max(0.0, np.sin(m.t * m.freq)) ** 2)
        a.add_updater(blink)
        arcs.add(a)
    return arcs


# ---------------------------------------------------------------- nucleolus
FCO = [(-.45, .3), (.42, .38), (.1, -.55), (-.6, -.3)]


def make_nucleolus(c=NC, s=NS_BIG, gc_col=GREY, dfc_col=GREY, fc_col=TEXT):
    rng = np.random.default_rng(3)
    gc = Circle(radius=1.25 * s, stroke_color=gc_col, stroke_width=3, fill_color=gc_col, fill_opacity=.38).move_to(c)
    dots = VGroup()
    for _ in range(40):
        a = rng.uniform(0, TAU)
        rr = 1.25 * s * np.sqrt(rng.uniform(.25, .97))
        dots.add(Dot(c + [rr * np.cos(a), rr * np.sin(a), 0], radius=.03 * s, color=TEXT).set_opacity(.5))
    dfc = VGroup(*[Circle(radius=.34 * s, stroke_color=dfc_col, stroke_width=2.5, fill_color=dfc_col, fill_opacity=.6)
                   .move_to(c + np.array([x, y, 0]) * s) for x, y in FCO])
    fc = VGroup(*[Circle(radius=.15 * s, stroke_width=0, fill_color=fc_col, fill_opacity=.7)
                  .move_to(c + np.array([x, y, 0]) * s) for x, y in FCO])
    return VGroup(gc, dots, dfc, fc)


def gene_strands(c=NC, s=NS_BIG):
    out = VGroup()
    for x, y in FCO:
        fcp = c + np.array([x, y, 0]) * s
        d = np.array([x, y, 0.0])
        d = d / np.linalg.norm(d)
        end = fcp + d * .85 * s
        line = Line(end, fcp, stroke_color=PURPLE, stroke_width=3.5)
        blocks = VGroup(*[Square(.12 * s, stroke_width=0, fill_color=PURPLE, fill_opacity=.95)
                          .move_to(fcp + d * (.38 + .2 * q) * s) for q in range(1, 4)])
        out.add(VGroup(line, blocks))
    return out


def rna_threads(c=NC, s=NS_BIG):
    out = VGroup()
    for k, (x, y) in enumerate(FCO):
        fcp = c + np.array([x, y, 0]) * s
        d = np.array([x, y, 0.0])
        d = d / np.linalg.norm(d)
        perp = np.array([-d[1], d[0], 0.0])
        d2 = d * np.cos(.9) + perp * np.sin(.9)
        pts = [fcp + d2 * (.16 + .17 * q) * s + perp * (.04 * np.sin(q * 1.7 + k)) * s for q in range(6)]
        out.add(VMobject(stroke_color=GREEN, stroke_width=4).set_points_smoothly(pts))
    return out


def subunits(c=NC, s=NS_BIG, n=6):
    out = VGroup()
    rng = np.random.default_rng(8)
    for i in range(n):
        a = rng.uniform(PI * .6, PI * 1.5)   # toward the lower-left nuclear edge
        d = Dot(c + 1.25 * s * np.array([np.cos(a), np.sin(a), 0]), radius=.09, color=TEXT).set_opacity(.8)
        d.dir = np.array([np.cos(a), np.sin(a), 0])
        d.t = i * .9
        d.start = d.get_center().copy()

        def mv(m, dt):
            m.t += dt
            ph = (m.t % 5.0) / 5.0
            m.move_to(m.start + m.dir * ph * .65)
            m.set_opacity(.8 * min(1, ph * 6, (1 - ph) * 2.5))
        d.add_updater(mv)
        out.add(d)
    return out


# ---------------------------------------------------------------- icons for bodies
def icon(name, p, k=1.0):
    p = np.array(p, dtype=float)
    if name == "speckles":
        offs = [(-.28, .1, .5, .3, .5), (.22, .2, .42, .24, -.6), (.0, -.2, .5, .26, .2), (.34, -.14, .3, .2, 1.0)]
        g = VGroup(*[Ellipse(width=w, height=h, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=.55)
                     .rotate(a).move_to(p + [x, y, 0]) for x, y, w, h, a in offs])
    elif name == "cajal":
        g = VGroup(Circle(radius=.3, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=.55).move_to(p))
    elif name == "pml":
        ring = Circle(radius=.36, stroke_color=BLUE, stroke_width=7).move_to(p)
        dots = VGroup(*[Dot(p + .36 * np.array([np.cos(a), np.sin(a), 0]), radius=.07, color=TEXT)
                        for a in np.linspace(0, TAU, 7)[:-1]])
        g = VGroup(ring, dots)
    else:  # para
        body = Ellipse(width=1.0, height=.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=.4).move_to(p)
        xs = np.linspace(-.5, .5, 9)
        thread = VMobject(stroke_color=GREEN, stroke_width=4).set_points_smoothly(
            [p + [x, .07 * np.sin(x * 9), 0] for x in xs])
        g = VGroup(body, thread)
    return g


BODY_LAB = {"speckles": "speckles\nsplicing factors", "cajal": "Cajal body\ncoilin",
            "pml": "PML body\nPML protein", "para": "paraspeckle\nNEAT1 RNA"}
BODY_LAB_Y = {"speckles": 2.65, "cajal": 1.35, "pml": .15, "para": -1.1}


def patch_blob(c=None, r=.55):
    c = C + np.array([-1.9, 1.3, 0.0]) if c is None else c
    rng = np.random.default_rng(21)
    pts = [c + (r * (1 + .22 * rng.uniform(-1, 1))) * np.array([np.cos(a), np.sin(a), 0]) for a in np.linspace(0, TAU, 9)[:-1]]
    pts.append(pts[0])
    return VMobject(stroke_color=B_COL, stroke_width=4, fill_color=B_COL, fill_opacity=.75).set_points_smoothly(pts)


def exchange_dots(centres):
    out = VGroup()
    for n, (c, r) in enumerate(centres):
        for k in range(3):
            d = Dot(c, radius=.06, color=BLUE)
            ang = (n * 1.3 + k * 2.1)
            d.dir = np.array([np.cos(ang), np.sin(ang), 0])
            d.c = np.array(c, dtype=float)
            d.r = r
            d.t = k * 1.1 + n * .37
            d.inward = (k % 2 == 1)

            def mv(m, dt):
                m.t += dt
                ph = (m.t % 3.3) / 3.3
                f = (1 - ph) if m.inward else ph
                m.move_to(m.c + m.dir * (m.r * .3 + f * (m.r * 2.4)))
                m.set_opacity(.9 * min(1, ph * 5, (1 - ph) * 5))
            d.add_updater(mv)
            out.add(d)
    return out


def question_marks(positions, size=44):
    return VGroup(*[T("?", size, TEXT, weight=BOLD).move_to(p) for p in positions])


def body_q_positions():
    ps = {k: bpos(k) + UP * (BODY_R[k] + .45) for k in BODY_POS}
    ps["nucleolus"] = NC + UP * (1.25 * NS_SMALL + .4)
    return ps


# ---------------------------------------------------------------- frog + tube
FC_C = np.array([-2.6, -0.1, 0.0])
FC_S = 2.1            # nucleolus scale in the frog zoom (radius 2.6)
TUBE_C = np.array([4.3, -0.7, 0.0])
PALE = "#9ADCE0"
DEEP = "#2A8E96"


def frog_nucleolus(teal=True):
    n = make_nucleolus(FC_C, FC_S)
    if teal:
        n[0].set_stroke(DEEP, 3).set_fill(DEEP, .5)
        for m in n[2]:
            m.set_stroke(PALE, 2.5).set_fill(PALE, .55)
        for m in n[3]:
            m.set_fill(TEXT, .55)
    return n


def wobble(m, A=.03):
    m.t = float(np.random.default_rng().uniform(0, 6))

    def f(mm, dt):
        mm.t += dt
        k = A * 1.7 * np.cos(1.7 * mm.t) * dt
        mm.stretch(1 + k, 0)
        mm.stretch(1 - k, 1)
    m.add_updater(f)
    return m


def tube(c=TUBE_C):
    w, h = .95, 2.2
    top = c + [0, h, 0]
    left = Line(top + [-w, 0, 0], c + [-w, -.2, 0])
    right = Line(top + [w, 0, 0], c + [w, -.2, 0])
    bottom = Arc(radius=w, start_angle=PI, angle=PI, arc_center=c + [0, -.2, 0])
    g = VGroup(left, right, bottom).set_stroke(GREY, 5)
    return g


def tube_dots(ref, n=22, seed=5):
    """Dots drifting inside the tube outline `ref` (they follow it when it moves)."""
    rng = np.random.default_rng(seed)
    out = VGroup()
    c0 = ref.get_center() - np.array([0, .525, 0])
    for i in range(n):
        col = PALE if i % 2 else DEEP
        p = c0 + [rng.uniform(-.75, .75), rng.uniform(-.9, 1.4), 0]
        d = Dot(p, radius=.09, color=col)
        d.velocity = np.array([rng.uniform(-.35, .35), rng.uniform(-.3, .3), 0])

        def drift(m, dt, ref=ref):
            m.shift(m.velocity * dt)
            q = m.get_center() - (ref.get_center() - np.array([0, .525, 0]))
            if abs(q[0]) > .75 or q[1] > 1.4 or q[1] < -.95:
                m.shift(-2 * m.velocity * dt)
                m.velocity *= -1
        d.add_updater(drift)
        out.add(d)
    return out


def make_tube(c=TUBE_C):
    outline = tube(c)
    return VGroup(outline, tube_dots(outline), tube_rna(c))


def tube_rna(c=TUBE_C):
    out = VGroup()
    for k, (x, y) in enumerate([(-.4, .7), (.3, .1), (-.3, -.6), (.4, 1.1)]):
        p = c + [x, y, 0]
        pts = [p + [-.3 + .15 * q, .08 * np.sin(q * 2 + k), 0] for q in range(5)]
        out.add(VMobject(stroke_color=GREEN, stroke_width=3.5).set_points_smoothly(pts))
    return out


def question_card(text="What forms in the tube?"):
    t = T(text, 31, TEXT, weight=BOLD)
    box = RoundedRectangle(width=t.width + .5, height=t.height + .34, corner_radius=.14, stroke_color=TEXT,
                           stroke_width=2, fill_color=BG, fill_opacity=.92)
    return VGroup(box, t).move_to([3.4, 3.2, 0])


def drop(c, r=.36):
    return VGroup(Circle(radius=r, stroke_color=DEEP, stroke_width=3, fill_color=DEEP, fill_opacity=.65).move_to(c),
                  Circle(radius=r * .5, stroke_width=0, fill_color=PALE, fill_opacity=.9).move_to(c))


# ---------------------------------------------------------------- chromatin fibre
BALL_C = np.array([0.0, -0.3, 0.0])


def ball_pts(c, rad, n=70):
    th = np.linspace(0, 9 * PI, n)
    ang = th * .9 + .3 * np.sin(2.3 * th)
    rr = rad * (.55 + .4 * np.sin(1.7 * th + .5))
    return np.stack([c[0] + rr * np.cos(ang), c[1] + rr * np.sin(ang), np.zeros(n)], axis=1)


def fibre_pts(n=70):
    t = np.linspace(0, 1, n)
    x = -5.3 + 10.6 * t + 1.1 * np.sin(31 * t)
    y = -0.2 + 1.6 * np.sin(5.2 * t) + 1.0 * np.sin(23 * t + 1)
    return np.stack([x, y, np.zeros(n)], axis=1)


BRIDGES = [(5, 26), (16, 38), (29, 51), (42, 64), (10, 57)]


def ball_curve(c, rad):
    return VMobject(stroke_color=PURPLE, stroke_width=7).set_points_smoothly(ball_pts(c, rad))


# ================================================================ scenes
class S00Link(SpokenScene):
    def construct(self):
        SL, SR, sr = np.array([-3.5, .2, 0.]), np.array([3.5, .2, 0.]), 1.9
        lo, ro = nucleus(SL, sr), nucleus(SR, sr)
        ld = protein_field(SL, 22, 5, sr, .055)
        rd = protein_field(SR, 22, 6, sr, .055)
        drops = VGroup(*[Circle(radius=.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=.5)
                         .move_to(SL + np.array(o) * .62) for o in [(-.95, .9, 0), (.65, 1.05, 0), (0, .15, 0), (-1.05, -.75, 0), (.9, -.72, 0)]])
        sites = VGroup(*[VGroup(*[RoundedRectangle(width=.1, height=.38, corner_radius=.03, stroke_color=ORANGE,
                                                    stroke_width=2, fill_color=ORANGE, fill_opacity=.4)
                                  for _ in range(4)]).arrange(RIGHT, buff=.04).move_to(SR + np.array(o) * .62)
                         for o in [(-.95, .9, 0), (.65, 1.05, 0), (0, .15, 0), (-1.05, -.75, 0), (.9, -.72, 0)]])
        ll = T("bigger, not brighter", 28, TEAL).move_to(SL + DOWN * 2.45)
        rl = T("brighter, not bigger", 28, ORANGE).move_to(SR + DOWN * 2.45)
        d = dial(np.array([0, .5, 0]), .30)
        self.add(lo, ro, ld, rd, drops, sites, ll, rl, d, schematic())
        self.wait(.6)
        self.at("Add protein")
        needle = d[2]
        self.play(Rotate(needle, angle=-.3 * PI, about_point=d[3].get_center()), run_time=1.0)
        self.at("bigger")
        self.play(drops.animate.scale(1.18), run_time=.6)
        self.play(drops.animate.scale(1 / 1.18), run_time=.5)
        self.at("brighter")
        self.play(*[s.animate.scale(1.12) for s in sites], run_time=.6)
        self.play(*[s.animate.scale(1 / 1.12) for s in sites], run_time=.5)
        self.at("Now meet")
        big = nucleus()
        ico = dial_icon(.60)
        dots = protein_field()
        self.play(ReplacementTransform(lo, big), ro.animate.move_to(C).scale(R / sr), FadeOut(VGroup(ld, rd, drops, sites, ll, rl)),
                  FadeOut(d[4]), Transform(VGroup(*d[:4]), ico), run_time=1.0)
        self.play(FadeOut(ro), FadeIn(dots), run_time=.5)
        self.at("chromatin a real")
        gs = glow_set()
        order = ["nucleolus", "speckles", "cajal", "pml", "para"]
        for k in order:
            self.add(gs[k].set_level(0))
        self.play(*[glow_anim(gs[k], 0, 1, 1.4) for k in order], run_time=1.4)
        self.at("tested as liquids")
        qpos = body_q_positions()
        qs = VGroup(*[T("?", 44, TEXT, weight=BOLD).move_to(qpos[k]) for k in ["nucleolus", "speckles", "cajal", "pml", "para"]])
        for q in qs:
            self.play(FadeIn(q, scale=1.4), run_time=.22)
        self.at("what did those tests show")
        self.play(*[q.animate.scale(1.45) for q in qs], rate_func=there_and_back, run_time=.9)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Nuclear architecture and condensates"
    TITLE = "Real Bodies, Real Tests"

    def construct(self):
        dots = protein_field()
        gs = glow_set()
        for g in gs.values():
            g.set_level(.5)
        world = [nucleus(), dots, *gs.values(), dial_icon(.60), schematic()]
        for m in world:
            m.set_z_index(-3)
        band = Rectangle(width=14.3, height=3.6, stroke_width=0, fill_color=BG, fill_opacity=.88).set_z_index(-2)
        self.add(*world, band)
        super().construct()


class S02Territories(SpokenScene):
    def construct(self):
        nuc, dots, gs = nucleus(), protein_field(), glow_set()
        ico = dial_icon(.60)
        self.add(nuc, dots, *gs.values(), ico, schematic())
        self.wait(.2)
        self.play(*[glow_anim(g, 1, .3, 1.2) for g in gs.values()], run_time=1.2)
        self.at("each chromosome")
        t = Terr()
        pts = [C + 1.7 * np.array([np.cos(np.radians(sum(SEC[k]) / 2)), np.sin(np.radians(sum(SEC[k]) / 2)), 0]) for k in SEC]
        self.play(*[GrowFromPoint(sc, pts[i]) for i, sc in enumerate(t.secs)], run_time=2.4)
        self.play(*[Create(segs, lag_ratio=.12) for segs in t.segs], run_time=1.6)
        self.at("chromosome territory")
        lb = lab("chromosome\nterritory", P_LIGHT, LAB_X, 2.4)
        tgt = C + 1.6 * np.array([np.cos(np.radians(75)), np.sin(np.radians(75)), 0])
        ld = leader(lb, tgt)
        self.play(FadeIn(lb), Create(ld), run_time=.8)
        self.at("balls of yarn")
        self.add(t.yarn)
        self.play(*[y.animate.set_stroke(opacity=.75) for y in t.yarn], run_time=1.0)
        self.wait(.3)
        self.play(*[y.animate.set_stroke(opacity=0) for y in t.yarn], run_time=.8)
        self.at("loose loops")
        loops = VGroup()
        for n, r in enumerate([1.1, 1.8, 2.4]):
            c0 = C + r * np.array([np.cos(np.radians(20)), np.sin(np.radians(20)), 0])
            e = Ellipse(width=.95, height=.42, stroke_color=P_LIGHT, stroke_width=5).rotate(np.radians(20) + PI / 2 - .3 + .3 * n).move_to(c0)
            e.t = n * 1.3

            def w(m, dt):
                m.t += dt
                m.rotate(.45 * np.sin(2.4 * m.t) * dt)
            e.add_updater(w)
            loops.add(e)
        self.play(FadeOut(lb), FadeOut(ld), run_time=.4)
        self.play(Create(loops), run_time=1.0)
        l2 = lab("loops poke\nacross", P_LIGHT, LAB_X, -.6)
        l2g = leader(l2, C + 1.8 * np.array([np.cos(np.radians(20)), np.sin(np.radians(20)), 0]))
        self.play(FadeIn(l2), Create(l2g), run_time=.6)
        self.finish()


class S03Hic(SpokenScene):
    def construct(self):
        nuc, dots, gs = nucleus(), protein_field(), glow_set()
        for g in gs.values():
            g.set_level(.3)
        t = Terr()
        self.add(nuc, dots, *gs.values(), t, dial_icon(.60), schematic())
        pairs = hic_pairs(t)
        self.at("maps")
        lb = lab("Hi-C: which\nparts touch", TEXT, LAB_X, 2.5)
        arcs = blink_arcs(t, pairs)
        self.play(FadeIn(lb), FadeIn(arcs), run_time=1.0)
        self.at("two broad compartments")
        self.wait(.5)
        self.at("R is open")      # transcript spells "A is open" as "R is open"
        aS = [t.segs[i][j] for i in range(3) for j in range(10) if t.kind[i][j] == "A"]
        la = lab("A: open,\nmostly active", A_COL, LAB_X, .75)
        self.play(*[sg.animate.set_stroke(A_COL, width=5.5) for sg in aS], FadeIn(la), run_time=1.2)
        self.at("B is closed")
        bS = [(i, j) for i in range(3) for j in range(10) if t.kind[i][j] == "B"]
        lbq = lab("B: closed,\nmostly quiet", "#A98BD0", LAB_X, -.55)
        self.play(*[t.segs[i][j].animate.set_stroke(B_COL, width=7.5) for i, j in bS], FadeIn(lbq), run_time=1.2)
        self.at("a mesh")
        lam = VGroup(Circle(radius=R - .13, stroke_color=GREY, stroke_width=8).move_to(C),
                     *[Line(C + (R - .13) * np.array([np.cos(a), np.sin(a), 0]), C + (R - .38) * np.array([np.cos(a), np.sin(a), 0]),
                            stroke_color=GREY, stroke_width=2.5) for a in np.linspace(0, TAU, 49)[:-1]])
        ll = lab("lamina", GREY, LAB_X, -2.0)
        lg = leader(ll, C + (R - .13) * np.array([np.cos(np.radians(-30)), np.sin(np.radians(-30)), 0]))
        self.play(Create(lam), FadeIn(ll), Create(lg), run_time=1.4)
        moves = []
        for i in range(3):
            for j in t._outer(i):
                moves.append(t.segs[i][j].animate.shift(t.outward(i, j)))
        self.play(*moves, run_time=1.8)
        self.at("Standard maps")
        self.play(FadeOut(VGroup(la, lbq, ll, lg, lb)), run_time=.5)
        self.at("millions of cells")
        ghosts = VGroup(*[Circle(radius=R * (.985 ** k), stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=.05)
                          .move_to(C + np.array([.09 * k, .07 * k, 0])).set_stroke(opacity=.55 - .03 * k) for k in range(14, 0, -1)])
        ghosts.set_z_index(-5)
        avg = VGroup(*[ArcBetweenPoints(C + np.array([*a, 0.0]), C + np.array([*b, 0.0]), angle=.7).set_stroke(TEXT, 14, opacity=.18)
                       for a, b in [((-1.5, 1.2), (1.2, 1.5)), ((-2, -.5), (.5, -1.8)), ((.5, 1.9), (2, -.8)), ((-1.0, 0), (1.4, .2))]])
        lm = lab("average of\nmillions", TEXT, LAB_X, 1.4)
        self.play(FadeIn(ghosts, lag_ratio=.05), FadeOut(arcs), run_time=1.0)
        self.play(FadeIn(avg), FadeIn(lm), run_time=.5)
        self.at("one nucleus")
        self.play(FadeOut(ghosts), FadeOut(avg), FadeOut(lm), run_time=.9)
        self.play(*[UpdateFromAlphaFunc(t, lambda m, a: m.set_level(1 - .6 * a)) for _ in [0]],
                  *[glow_anim(g, .3, 1, 1.1) for g in gs.values()], run_time=1.1)
        self.finish()


def final_terr(level=.4):
    t = Terr()
    t.apply_hic(moved=False)
    # replicate the shifts from S03 with the same outer set
    for i in range(3):
        for j in t._outer(i):
            t.segs[i][j].shift(t.outward(i, j))
    return t.set_level(level)


class S05Nucleolus(SpokenScene):
    def construct(self):
        nuc, dots, gs = nucleus(), protein_field(), glow_set()
        t = final_terr(.4)
        for k, g in gs.items():
            g.set_level(1)
        self.add(nuc, dots, t, *gs.values(), dial_icon(.60), schematic())
        gn = gs["nucleolus"]
        n = make_nucleolus(NC, NS_BIG)
        self.play(*[glow_anim(gs[k], 1, .3, 1.5) for k in ("speckles", "cajal", "pml", "para")], run_time=1.5)
        self.play(glow_anim(gn, 1, 1.5, .8), run_time=.8)
        self.at("The nucleolus")
        self.play(FadeOut(gn), FadeIn(n[0]), run_time=1.0)
        self.play(FadeIn(n[1]), FadeIn(n[2]), FadeIn(n[3]), run_time=.8)
        self.at("repeated genes")
        gsn = gene_strands()
        self.play(Create(gsn, lag_ratio=.25), run_time=1.5)
        self.at("ribosomal RNA")
        self.play(Indicate(gsn, color=PURPLE, scale_factor=1.12), run_time=1.2)
        self.at("three parts")
        self.play(Indicate(n[3], color=TEXT, scale_factor=1.35), run_time=.7)
        self.play(Indicate(n[2], color=TEXT, scale_factor=1.15), run_time=.7)
        self.play(Indicate(n[0], color=TEXT, scale_factor=1.04), run_time=.7)
        arrow = Arrow(NC + np.array(FCO[0] + (0,)) * NS_BIG, NC + np.array([-1.15, .5, 0]) * NS_BIG, buff=.0,
                      stroke_width=7, color=TEXT, max_tip_length_to_length_ratio=.4)
        self.at("assembly line")
        al = lab("assembly line", TEXT, -6.75, -0.4)
        alg = Line(al.get_right() + RIGHT * .1, NC + np.array([-1.0, .35, 0]) * NS_BIG, stroke_color=GREY, stroke_width=2.5)
        self.play(GrowArrow(arrow), FadeIn(al), Create(alg), run_time=1.2)
        self.at("Fibrular centers")
        fcl = lab("fibrillar centre\ngenes, machinery", TEXT, LAB_X, .45)
        fcg = leader(fcl, NC + np.array([FCO[1][0] + .15, FCO[1][1], 0]) * NS_BIG)
        self.play(FadeIn(fcl), Create(fcg), Indicate(n[3], color=TEXT, scale_factor=1.3), run_time=1.2)
        self.at("New RNA")
        rna = rna_threads()
        self.play(Create(rna, lag_ratio=.2), run_time=1.6)
        self.at("processing begins")
        dl = lab("dense fibrillar\nprocessing", TEXT, LAB_X, -1.0)
        dg = leader(dl, NC + np.array([FCO[2][0] + .34, FCO[2][1], 0]) * NS_BIG)
        self.play(FadeIn(dl), Create(dg), Indicate(n[2], color=TEXT, scale_factor=1.12), run_time=1.2)
        self.at("outer granular component")
        gl = lab("granular component\nassembly", TEXT, LAB_X, -2.3)
        gg = leader(gl, NC + 1.25 * NS_BIG * np.array([np.cos(np.radians(-30)), np.sin(np.radians(-30)), 0]))
        self.play(FadeIn(gl), Create(gg), run_time=1.0)
        self.at("assembles ribosomal subunits")
        sub = subunits()
        self.add(sub)
        self.play(FadeOut(arrow), FadeOut(al), FadeOut(alg), run_time=.6)
        self.finish()


class S06Small(SpokenScene):
    def construct(self):
        nuc, dots, gs = nucleus(), protein_field(), glow_set()
        t = final_terr(.4)
        for k in ("speckles", "cajal", "pml", "para"):
            gs[k].set_level(.3)
        n = make_nucleolus(NC, NS_BIG)
        fcl = lab("fibrillar centre\ngenes, machinery", TEXT, LAB_X, .45)
        dl = lab("dense fibrillar\nprocessing", TEXT, LAB_X, -1.0)
        gl = lab("granular component\nassembly", TEXT, LAB_X, -2.3)
        gsn, rna = gene_strands(), rna_threads()
        sub = subunits()
        lgs = VGroup(fcl, dl, gl, leader(fcl, NC + np.array([FCO[1][0] + .15, FCO[1][1], 0]) * NS_BIG),
                     leader(dl, NC + np.array([FCO[2][0] + .34, FCO[2][1], 0]) * NS_BIG),
                     leader(gl, NC + 1.25 * NS_BIG * np.array([np.cos(np.radians(-30)), np.sin(np.radians(-30)), 0])))
        self.add(nuc, dots, t, *[gs[k] for k in ("speckles", "cajal", "pml", "para")], n, gsn, rna, lgs, sub, dial_icon(.60), schematic())
        self.wait(.3)
        nl = T("nucleolus", 28, TEXT).move_to(NC + DOWN * 1.4)
        self.play(FadeOut(lgs), FadeOut(gsn), FadeOut(rna), FadeOut(sub),
                  n.animate.scale(NS_SMALL / NS_BIG, about_point=NC), FadeIn(nl), run_time=1.6)
        labs, icons = {}, {}
        for name, phrase in [("speckles", "Speckles"), ("cajal", "Casual bodies"), ("pml", "PML bodies"), ("para", "Pair speckles")]:
            self.at(phrase)
            ic = icon(name, bpos(name))
            lb = lab(BODY_LAB[name], TEXT, LAB_X, BODY_LAB_Y[name])
            ld = leader(lb, bpos(name) + RIGHT * .55)
            icons[name] = ic
            self.play(glow_anim(gs[name], .3, 1, .5), FadeIn(ic, scale=.6), FadeIn(lb), Create(ld), run_time=.9)
            self.play(Indicate(ic, color=BLUE, scale_factor=1.15), run_time=.7)
        self.finish()


def nucleus_world(labels=False, level=.4, qs=False):
    nuc, dots, t = nucleus(), protein_field(), final_terr(level)
    n = make_nucleolus(NC, NS_SMALL)
    ics = VGroup(*[icon(k, bpos(k)) for k in BODY_POS])
    return nuc, dots, t, n, ics


class S07RealOpen(SpokenScene):
    def construct(self):
        nuc, dots, t, n, ics = nucleus_world()
        lbls = VGroup()
        for k in BODY_POS:
            lb = lab(BODY_LAB[k], TEXT, LAB_X, BODY_LAB_Y[k])
            lbls.add(lb, leader(lb, bpos(k) + RIGHT * .55))
        nl = T("nucleolus", 28, TEXT).move_to(NC + DOWN * 1.4)
        self.add(nuc, dots, t, n, ics, lbls, nl, dial_icon(.60), schematic())
        self.wait(.4)
        self.play(FadeOut(lbls), FadeOut(nl), run_time=.8)
        centres = [(NC, 1.0)] + [(bpos(k), .45) for k in BODY_POS]
        ex = exchange_dots(centres)
        self.add(ex)
        self.at("help with a job")
        ticks = VGroup(*[T("✓", 40, GREEN, weight=BOLD).move_to(p) for p in
                         (NC + UP * 1.35 + RIGHT * .0, bpos("speckles") + UP * .62)])
        self.play(FadeIn(ticks, scale=1.4, lag_ratio=.4), run_time=1.0)
        self.at("how does each one form")
        qpos = body_q_positions()
        qpos["speckles"] = qpos["speckles"] + UP * .0
        qs = VGroup(*[T("?", 44, TEXT, weight=BOLD).move_to(qpos[k]) for k in ["nucleolus", "speckles", "cajal", "pml", "para"]])
        qs[0].move_to(NC + UP * 1.2 + LEFT * .6)
        self.play(FadeOut(ticks), FadeIn(qs, lag_ratio=.15), run_time=1.2)
        self.at("tested closely")
        patch = patch_blob()
        ring1 = Circle(radius=1.05, stroke_color=TEXT, stroke_width=4).move_to(NC)
        ring2 = Circle(radius=.8, stroke_color=TEXT, stroke_width=4).move_to(patch.get_center())
        dim = [ics[1], ics[2], ics[3], ics[0]]
        self.play(FadeIn(patch), Create(ring1), Create(ring2), *[m.animate.set_opacity(.35) for m in ics],
                  *[q.animate.set_opacity(.8) for q in qs[1:]], FadeOut(qs[0]), run_time=1.6)
        self.finish()


class S08FrogPredict(SpokenScene):
    def construct(self):
        nuc, dots, t, n, ics = nucleus_world()
        patch = patch_blob()
        for m in ics:
            m.set_opacity(.35)
        ring1 = Circle(radius=1.05, stroke_color=TEXT, stroke_width=4).move_to(NC)
        ring2 = Circle(radius=.8, stroke_color=TEXT, stroke_width=4).move_to(patch.get_center())
        self.add(nuc, dots, t, ics, patch, n, ring1, ring2, dial_icon(.60), schematic())
        self.wait(.2)
        big = frog_nucleolus(teal=False)
        self.play(FadeOut(VGroup(nuc, dots, t, ics, patch, ring1, ring2)), ReplacementTransform(n, big), run_time=2.4)
        self.at("of a frog")
        tag = T("frog oocyte nucleolus", 30, TEXT).move_to(FC_C + UP * 3.2)
        self.play(FadeIn(tag), run_time=.6)
        self.at("Its dense")
        self.play(big[0].animate.set_stroke(DEEP).set_fill(DEEP, .5),
                  *[m.animate.set_stroke(PALE).set_fill(PALE, .55) for m in big[2]], run_time=1.4)
        for m in list(big[2]) + [big[0]]:
            wobble(m)
        self.at("without mixing")
        l2 = T("two liquids, unmixed", 30, TEAL).move_to(FC_C + DOWN * 3.2)
        self.play(FadeIn(l2), run_time=.7)
        self.at("What should purified")
        q = question_card()
        self.play(FadeIn(q, shift=DOWN * .2), run_time=.7)
        self.at("mixed with RNA")
        tb = make_tube()
        tb.shift(RIGHT * 6)
        self.add(tb)
        self.play(tb.animate.shift(LEFT * 6), run_time=1.4)
        tl = T("purified proteins\n+ RNA", 28, TEXT).move_to(TUBE_C + DOWN * 2.3)
        self.play(FadeIn(tl), run_time=.5)
        self.finish()


class S09Think(NarratedScene):
    def construct(self):
        big = frog_nucleolus()
        for m in list(big[2]) + [big[0]]:
            wobble(m)
        tag = T("frog oocyte nucleolus", 30, TEXT).move_to(FC_C + UP * 3.2)
        l2 = T("two liquids, unmixed", 30, TEAL).move_to(FC_C + DOWN * 3.2)
        tb = make_tube()
        tl = T("purified proteins\n+ RNA", 28, TEXT).move_to(TUBE_C + DOWN * 2.3)
        q = question_card()
        self.add(big, tag, l2, tb, tl, q)
        self.finish()


class S10FrogAnswer(SpokenScene):
    def construct(self):
        big = frog_nucleolus()
        for m in list(big[2]) + [big[0]]:
            wobble(m)
        tag = T("frog oocyte nucleolus", 30, TEXT).move_to(FC_C + UP * 3.2)
        l2 = T("two liquids, unmixed", 30, TEAL).move_to(FC_C + DOWN * 3.2)
        tb = make_tube()
        dots = tb[1]
        tl = T("purified proteins\n+ RNA", 28, TEXT).move_to(TUBE_C + DOWN * 2.3)
        q = question_card()
        self.add(big, tag, l2, tb, tl, q)
        self.at("They reproduce")
        self.play(FadeOut(q), run_time=.5)
        centres = [TUBE_C + np.array(o) for o in [(-.3, .75, 0), (.3, 0.0, 0), (-.25, -.65, 0)]]
        for d in dots:
            d.clear_updaters()
        self.play(*[d.animate.move_to(centres[i % 3] + np.array([.12 * np.cos(i), .12 * np.sin(i), 0])) for i, d in enumerate(dots)],
                  run_time=1.6)
        self.at("drops with one phase")
        drops = VGroup(*[drop(c, .45) for c in centres])
        self.play(FadeOut(dots), FadeIn(drops, scale=.6), FadeOut(tb[2]), FadeOut(l2), run_time=.9)
        self.at("other")
        eq = T("=", 80, TEXT, weight=BOLD).move_to([1.75, -.1, 0])
        self.play(FadeIn(eq, scale=1.4), run_time=.6)
        self.at("strong evidence")
        ev = T("strong liquid evidence", 32, TEAL, weight=BOLD).move_to(FC_C + DOWN * 3.2)
        self.play(FadeIn(ev), run_time=.8)
        self.at("frog nucleolus contains")
        self.play(FadeOut(eq), FadeOut(VGroup(tb[0], drops, tl)), run_time=1.0)
        self.finish()


class S11Bridging(SpokenScene):
    def construct(self):
        nuc, dots, t, n, ics = nucleus_world()
        patch = patch_blob()
        for m in ics:
            m.set_opacity(.35)
        ring1 = Circle(radius=1.05, stroke_color=TEXT, stroke_width=4).move_to(NC)
        ring2 = Circle(radius=.8, stroke_color=TEXT, stroke_width=4).move_to(patch.get_center())
        big = frog_nucleolus()
        ev = T("strong liquid evidence", 32, TEAL, weight=BOLD).move_to(FC_C + DOWN * 3.2)
        tag = T("frog oocyte nucleolus", 30, TEXT).move_to(FC_C + UP * 3.2)
        self.add(big, ev, tag)
        self.wait(.2)
        self.play(FadeOut(VGroup(big, ev, tag)), FadeIn(VGroup(nuc, dots, t, ics, n, patch, ring1, ring2)), run_time=1.2)
        self.wait(.2)
        self.play(FadeOut(VGroup(nuc, dots, t, ics, n, ring1, ring2)), run_time=.9)
        fibre = VMobject(stroke_color=PURPLE, stroke_width=6).set_points_smoothly(fibre_pts())
        self.play(Transform(patch, fibre), run_time=1.2)
        self.remove(patch)
        a = ValueTracker(0.0)
        fibre = VMobject(stroke_color=PURPLE, stroke_width=6)
        fp, bp = fibre_pts(), ball_pts(BALL_C, 2.0)
        fibre.add_updater(lambda m: m.set_points_smoothly((1 - a.get_value()) * fp + a.get_value() * bp))
        fibre.set_points_smoothly(fp)
        self.add(fibre)
        self.at("adds a third")
        ic1 = Circle(radius=.2, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=.5).move_to([-4.6, 3.25, 0])
        ic2 = VGroup(*[RoundedRectangle(width=.1, height=.34, corner_radius=.03, stroke_color=ORANGE, stroke_width=2,
                                         fill_color=ORANGE, fill_opacity=.4) for _ in range(3)]).arrange(RIGHT, buff=.04).move_to([-3.8, 3.25, 0])
        ic3 = chip("bridging", BLUE, 28).move_to([-2.2, 3.25, 0])
        self.play(FadeIn(ic1), FadeIn(ic2), FadeIn(ic3, scale=.8), run_time=.6)
        sch = schematic()
        self.at("bridge distant")
        br = VGroup()
        for i, j in BRIDGES:
            ln = Line(ORIGIN, ORIGIN, stroke_color=BLUE, stroke_width=3.5)
            e1, e2 = Dot(radius=.08, color=BLUE), Dot(radius=.08, color=BLUE)

            def upd(m, i=i, j=j, ln=ln, e1=e1, e2=e2):
                v = (1 - a.get_value()) * fp + a.get_value() * bp
                ln.put_start_and_end_on(v[i], v[j])
                e1.move_to(v[i])
                e2.move_to(v[j])
            m = VGroup(ln, e1, e2)
            m.add_updater(upd)
            br.add(m)
        self.add(br)
        self.play(FadeIn(br, lag_ratio=.3), FadeIn(sch), run_time=1.6)
        self.wait(.3)
        self.at("the fiber")
        self.play(a.animate.set_value(1.0), run_time=3.2, rate_func=smooth)
        self.at("phase transition")
        cl = T("chromatin collapse", 30, PURPLE).move_to([2.8, 3.0, 0])
        self.play(FadeIn(cl), run_time=.6)
        self.at("a ball of chromatin")
        bl = T("ball of chromatin", 30, PURPLE).move_to(BALL_C + DOWN * 2.75)
        self.play(FadeOut(cl), FadeIn(bl), run_time=.5)
        self.at("liquid drop")
        dc = np.array([4.5, -.3, 0.0])
        dr = Circle(radius=1.2, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=.5).move_to(dc)
        dl = T("drop of protein", 30, TEAL).move_to(dc + DOWN * 2.45)
        self.play(FadeIn(dr, scale=.6), FadeIn(dl), run_time=.9)
        self.wait(.6)
        self.play(FadeOut(dr), FadeOut(dl), FadeOut(bl), FadeOut(br), FadeOut(VGroup(ic1, ic2, ic3)), run_time=1.0)
        fibre.clear_updaters()
        self.finish()


class S12Split(SpokenScene):
    def construct(self):
        ball = ball_curve(BALL_C, 2.0)
        self.add(ball)
        self.wait(.2)
        div = DashedLine([0, -3.5, 0], [0, 3.5, 0], stroke_color=GREY, stroke_width=3)
        RB = np.array([3.5, 0.0, 0.0])
        LB = np.array([-3.5, 0.0, 0.0])
        self.play(Create(div), ball.animate.move_to(RB), run_time=1.6)
        self.at("In early fruit fly")
        tagL = T("fly embryo", 32, TEXT).move_to(LB + UP * 3.0)
        self.play(FadeIn(tagL), run_time=.6)
        self.at("foci of")
        focus = Circle(radius=2.0, stroke_width=0, fill_color=BLUE, fill_opacity=.5).move_to(LB)
        rim = Ellipse(width=4.1, height=4.1, stroke_color=TEAL, stroke_width=7).move_to(LB)
        wobble(rim)
        self.play(FadeIn(focus, scale=.5), Create(rim), run_time=1.4)
        self.at("liquid like")
        ll = T("liquid-like", 32, TEAL).move_to(LB + DOWN * 3.1)
        self.play(FadeIn(ll), run_time=.6)
        self.at("In mouse")
        tagR = T("mouse fibroblast", 32, TEXT).move_to(RB + UP * 3.0)
        self.play(FadeIn(tagR), run_time=.6)
        self.at("half body FRAP")
        flash = Circle(radius=2.3, stroke_color=TEXT, stroke_width=8).move_to(RB)
        half = Sector(radius=2.05, angle=PI, start_angle=PI / 2, arc_center=RB, stroke_width=0, fill_color=BG, fill_opacity=.82)
        self.play(FadeIn(flash), run_time=.25)
        self.play(FadeOut(flash), FadeIn(half), run_time=.5)
        self.at("found no preferential")
        rng = np.random.default_rng(4)
        ds = VGroup(*[Dot(RB + np.array([-2.5 - rng.uniform(0, .5), rng.uniform(-1.6, 1.6), 0]), radius=.09, color=BLUE) for _ in range(9)])
        self.play(FadeIn(ds), run_time=.5)
        self.play(*[d.animate.move_to(RB + np.array([-rng.uniform(.2, 1.4), rng.uniform(-1.3, 1.3), 0])) for d in ds],
                  half.animate.set_fill(BG, .45), run_time=2.0)
        mid = DashedLine(RB + UP * 2.3, RB + DOWN * 2.3, stroke_color=TEXT, stroke_width=3)
        self.at("heterochromatin clusters")
        nl = T("no internal mixing", 32, TEXT).move_to(RB + DOWN * 3.1)
        self.play(FadeIn(nl), Create(mid), run_time=.8)
        self.at("favoring")
        fl = T("favours collapsed chromatin", 32, PURPLE).move_to(RB + DOWN * 3.1)
        self.play(FadeOut(nl), run_time=.3)
        self.play(FadeIn(fl), run_time=.5)
        self.wait(.5)
        words = T("one system each", 36, TEXT).move_to([0, 3.4, 0])
        left = VGroup(tagL, focus, rim, ll)
        right = VGroup(tagR, ball, half, ds, mid, fl)
        self.play(FadeOut(div), FadeIn(words), left.animate.scale(.7).move_to([-3.3, -.2, 0]),
                  right.animate.scale(.7).move_to([3.3, -.2, 0]), run_time=1.1)
        self.finish()


class S13Close(SpokenScene):
    def construct(self):
        LB, RB = np.array([-3.3, -.2, 0.0]), np.array([3.3, -.2, 0.0])
        focus = Circle(radius=2.0, stroke_width=0, fill_color=BLUE, fill_opacity=.5).move_to(LB)
        rim = Ellipse(width=4.1, height=4.1, stroke_color=TEAL, stroke_width=7).move_to(LB)
        wobble(rim)
        tagL = T("fly embryo", 32, TEXT).move_to(LB + UP * 3.0)
        ll = T("liquid-like", 32, TEAL).move_to(LB + DOWN * 3.1)
        left = VGroup(tagL, focus, rim, ll).scale(.7).move_to(LB)
        ball = ball_curve(RB, 2.0)
        tagR = T("mouse fibroblast", 32, TEXT).move_to(RB + UP * 3.0)
        fl = T("favours collapsed chromatin", 32, PURPLE).move_to(RB + DOWN * 3.1)
        right = VGroup(tagR, ball, fl).scale(.7).move_to(RB)
        words = T("one system each", 36, TEXT).move_to([0, 3.4, 0])
        self.add(left, right, words)
        self.wait(.6)
        self.at("heterochromatin")
        nuc, dots, t, n, ics = nucleus_world(level=1.0)
        t.set_level(.85)
        nl = T("nucleolus", 28, TEXT).move_to(NC + DOWN * 1.4)
        self.play(FadeOut(left), FadeOut(right), FadeOut(words), FadeIn(nuc), FadeIn(dots), FadeIn(t), run_time=1.4)
        self.play(FadeIn(n), FadeIn(ics), FadeIn(nl), run_time=1.0)
        words1 = {"speckles": "speckles", "cajal": "Cajal", "pml": "PML", "para": "paraspeckle"}
        lbls = VGroup()
        for k in BODY_POS:
            lb = lab(words1[k], TEXT, LAB_X, BODY_LAB_Y[k] - .2)
            lbls.add(lb, leader(lb, bpos(k) + RIGHT * .55))
        ev = T("strong liquid evidence", 32, TEAL, weight=BOLD).move_to([NC[0], -3.62, 0])
        self.play(FadeIn(lbls), run_time=.7)
        self.at("still contested")
        qpos = body_q_positions()
        qs = VGroup(*[T("?", 44, TEXT, weight=BOLD).move_to(qpos[k]) for k in ["speckles", "cajal", "pml", "para"]])
        self.play(FadeOut(nl), FadeIn(ev), FadeIn(qs, scale=1.4, lag_ratio=.2), run_time=1.2)
        self.play(*[q.animate.scale(1.3) for q in qs], rate_func=there_and_back, run_time=.8)
        self.at("The text below")
        self.play(*[m.animate.shift(DOWN * .55).set_opacity(.3) for m in lbls], run_time=1.4)
        self.finish()


class S14End(EndCard):
    LINE = "Nuclear bodies are real; how each forms is tested body by body."
