# Chapter 6: Downhill, Not Random
# COLOR MAP (shared with all chapters of the protein 3D structure series)
#   BLUE    the protein / polypeptide chain / candidate conformations (the ball is the chain; the funnel surface is tinted blue)
#   ORANGE  backbone geometry: the Ramachandran map, the three local-shape icons, hydrogen bonds in the helix and sheet
#   YELLOW  nonpolar (oily / greasy) side chains and lipid
#   PURPLE  polar / charged residues
#   TEAL    water
#   GREEN   the native fold, allowed / surviving, contacts that stay
#   RED     forbidden, eliminated, misfolded, the random search, contacts that break
#   GREY    labels, frames, structure
# Nothing here draws a molecular structure: chains are smooth curves and beads, helices and sheets are
# cartoon coils and meanders with dashed bond marks, and the funnel is a computed surface profile.
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
LEFTC = "#FF7FB5"      # tint for the left-handed coil icon: pink, clearly different from the orange right-handed helix
PURPLE = "#B58CE0"
LIGHT = "#C9CED8"


# ------------------------------------------------------------------ small helpers
def tag(txt, color=TEXT, size=26, pos=None):
    """A label with a dark backing so it stays readable over lines and plots."""
    t = T(txt, size=size, color=color)
    bk = Rectangle(width=t.width + 0.24, height=t.height + 0.16, stroke_width=0, fill_color=BG, fill_opacity=0.88).move_to(t)
    g = VGroup(bk, t)
    if pos is not None:
        g.move_to(pos)
    return g.set_z_index(8)


def ex(parts, size=60, color=TEXT):
    """Typeset numbers with tight real superscripts. parts: str (normal), (str,) (superscript), float (gap)."""
    h0 = T("0", size=size, color=color).height
    items, x = [], 0.0
    for p in parts:
        if isinstance(p, (int, float)):
            x += p
            continue
        if isinstance(p, tuple):
            t = T(p[0], size=max(22, int(size * 0.62)), color=color)
            t.move_to([x + t.width / 2, 0.62 * h0 + t.height / 2, 0])
        else:
            t = T(p, size=size, color=color)
            cy = h0 / 2 if p in "≈×=+−" else t.height / 2
            t.move_to([x + t.width / 2, cy, 0])
        x += t.width + 0.02
        items.append(t)
    return VGroup(*items).move_to(ORIGIN)


def chain_pts(seed, n, w, h):
    k = seed * 77 + 3
    while True:
        rng = np.random.RandomState(k)
        k += 1
        ang = 0.0
        pts = [np.zeros(2)]
        for _ in range(n - 1):
            ang += rng.normal(0, 0.9)
            pts.append(pts[-1] + np.array([np.cos(ang), np.sin(ang)]))
        P = np.array(pts)
        ratio = np.ptp(P[:, 0]) / max(np.ptp(P[:, 1]), 1e-6)
        if 0.7 * w / h < ratio < 1.4 * w / h:
            break
    P -= (P.max(0) + P.min(0)) / 2
    P *= min(w / np.ptp(P[:, 0]), h / np.ptp(P[:, 1]))
    return P


def beadchain(seed, n=15, w=11.0, h=4.4, colors=None, r=0.2, op=1.0, cx=0.0, cy=0.0, line_color=BLUE):
    P = chain_pts(seed, n, w, h)
    line = VMobject(stroke_color=line_color, stroke_width=6, stroke_opacity=op, fill_opacity=0)
    line.set_points_smoothly([np.array([x + cx, y + cy, 0.0]) for x, y in P])
    colors = colors or [BLUE] * n
    beads = [Circle(radius=r, stroke_color=colors[i], stroke_width=3, stroke_opacity=op, fill_color=colors[i],
                    fill_opacity=0.5 * op).move_to([x + cx, y + cy, 0]) for i, (x, y) in enumerate(P)]
    return VGroup(line, *beads)


def flicker(mob, make, period=0.25, start=0):
    """Swap the mobject for a new random shape every `period` seconds (a jump, like a new trial)."""
    st = {"t": 0.0, "i": start}

    def upd(m, dt):
        st["t"] += dt
        if st["t"] >= period:
            st["t"] = 0.0
            st["i"] += 1
            m.become(make(st["i"]))
    mob.add_updater(upd)
    return upd


def icon(kind, w=0.3, color=None, sw=3):
    """Backbone-shape glyphs. strand = zigzag; helix = right-handed coil; left = its mirror image.
    Coils are drawn with the front strands solid and the back strands faint, so the slant shows the handedness."""
    color = color or (LEFTC if kind == "left" else ORANGE)
    if kind == "strand":
        pts = [np.array([-w / 2 + w * i / 8, (0.16 * w) * (1 if i % 2 else -1), 0.0]) for i in range(9)]
        m = VMobject(stroke_color=color, stroke_width=sw)
        m.set_points_as_corners(pts)
        return VGroup(m)
    s = 1 if kind == "helix" else -1
    turns = 3
    th = np.linspace(0, 2 * np.pi * turns, 240)
    r = 0.2 * w
    X = -w / 2 + w * th / (2 * np.pi * turns)
    Y = r * np.cos(th)
    Z = s * r * np.sin(th)
    g = VGroup()
    i = 0
    while i < len(th) - 1:
        j = i
        front = Z[i] >= 0
        while j < len(th) - 1 and (Z[j + 1] >= 0) == front:
            j += 1
        if j - i >= 2:
            m = VMobject(stroke_color=color, stroke_width=sw if front else sw * 0.6, stroke_opacity=1.0 if front else 0.3)
            m.set_points_smoothly([np.array([X[k], Y[k], 0.0]) for k in range(i, j + 1)])
            g.add(m)
        i = max(j, i + 1)
    return g


# ------------------------------------------------------------------ Ramachandran map (schematic allowed regions: three islands)
def _ell(phi, psi, c, a, b):
    return ((phi - c[0]) / a) ** 2 + ((psi - c[1]) / b) ** 2 <= 1


def allowed(phi, psi):
    return _ell(phi, psi, (-120, 130), 62, 52) or _ell(phi, psi, (-62, -42), 32, 28) or _ell(phi, psi, (58, 45), 24, 32)


def mask_image(px=200):
    arr = np.zeros((px, px, 4), dtype=np.uint8)
    g = np.array([0x83, 0xC1, 0x67, 150], dtype=np.uint8)
    for r in range(px):
        psi = 180 - (r + 0.5) * 360 / px
        for c in range(px):
            phi = -180 + (c + 0.5) * 360 / px
            if allowed(phi, psi):
                arr[r, c] = g
    return arr


ISL = {"alphaR": ((-62, -42), 32, 28), "beta": ((-120, 130), 62, 52), "alphaL": ((58, 45), 24, 32)}


class Rama:
    def __init__(self, cx, cy, h):
        self.cx, self.cy, self.h = cx, cy, h
        self.frame = Square(h, stroke_color=GREY, stroke_width=3, fill_color=RED, fill_opacity=0.12).move_to([cx, cy, 0])
        self.img = ImageMobject(mask_image()).set_height(h).move_to([cx, cy, 0]).set_z_index(2)
        self.phi = T("φ  (phi)", size=32, color=LIGHT).move_to([cx, cy - h / 2 - 0.78, 0])
        self.psi = T("ψ  (psi)", size=32, color=LIGHT).move_to([cx - h / 2 - 0.15, cy + h / 2 + 0.42, 0])
        self.ticks = VGroup()
        for v, s in ((-180, "−180"), (0, "0"), (180, "+180")):
            self.ticks.add(T(s, size=26, color=GREY).move_to([cx + v / 360 * h, cy - h / 2 - 0.33, 0]))
            self.ticks.add(T(s, size=26, color=GREY).move_to([cx - h / 2 - 0.5, cy + v / 360 * h, 0]))
        self.isl = {}
        for k, (c, a, b) in ISL.items():
            e = Ellipse(width=2 * a / 360 * h, height=2 * b / 360 * h, stroke_color=GREEN, stroke_width=4,
                        fill_color=GREEN, fill_opacity=0.0).move_to(self.c2p(*c)).set_z_index(3)
            self.isl[k] = e

    def c2p(self, phi, psi):
        return np.array([self.cx + phi / 360 * self.h, self.cy + psi / 360 * self.h, 0.0])

    def parts(self):
        return [self.frame, self.img, self.phi, self.psi, self.ticks]


# ------------------------------------------------------------------ the funnel (computed surface profile)
FS = [1.0, 0.82, 0.65, 0.5, 0.36, 0.24]
P_FUN = 1.5


class Fun:
    def __init__(self, cx, ytop, R, H, k):
        self.cx, self.ytop, self.R, self.H, self.k = cx, ytop, R, H, k

    def yc(self, f, D, p):
        return self.ytop - D * self.H * (1 - f ** p)

    def cen(self, f, D, p):
        return np.array([self.cx, self.yc(f, D, p), 0.0])

    def surf(self, f, th, D=1.0, p=P_FUN):
        return np.array([self.cx + self.R * f * np.cos(th), self.yc(f, D, p) + self.R * f * self.k * np.sin(th), 0.0])

    def make(self, D=1.0, p=P_FUN, hs=0.09):
        """D = 0 is a flat plane, D = 1 the full funnel; in between the plane is bending."""
        R, k = self.R, self.k
        on = min(1.0, 3.0 * D)
        rim = Ellipse(width=2 * R, height=2 * R * k, stroke_color=interpolate_color(ManimColor(GREEN), ManimColor(GREY), on),
                      stroke_width=4, fill_color=interpolate_color(ManimColor(GREEN), ManimColor(BLUE), on),
                      fill_opacity=0.18 - 0.08 * on).move_to(self.cen(1.0, D, p))
        rings = [Ellipse(width=2 * R * f, height=2 * R * f * k, stroke_color=GREY, stroke_width=2, stroke_opacity=0.6 * on,
                         fill_opacity=0).move_to(self.cen(f, D, p)) for f in FS[1:]]
        walls = [ParametricFunction(lambda t, th=th: self.surf(t, th, D, p), t_range=[0.07, 1.0, 0.02], stroke_color=GREY,
                                    stroke_width=3, stroke_opacity=0.8 * on) for th in (0.0, np.pi)]
        hole = Ellipse(width=2 * R * hs, height=2 * R * hs * k, stroke_color=GREEN, stroke_width=4,
                       fill_color=GREEN if on > 0.99 else BG, fill_opacity=0.7 if on > 0.99 else 1.0).move_to(self.cen(0.0, D, p))
        return VGroup(rim, *rings, *walls, hole)


FUN = Fun(0.0, 1.2, 4.7, 3.7, 0.34)          # the one funnel geometry used from scene 16 to 30


def plane(a):
    """The golf-course plane (a = 0) tilting into the funnel (a = 1)."""
    ytop = 0.3 + 0.9 * a
    R = 5.6 - 0.9 * a
    k = 0.5 - 0.16 * a
    return Fun(0.0, ytop, R, 3.7, k).make(a, P_FUN, hs=0.17 - 0.08 * a)


def WL(f):
    """A point on the left wall of the funnel (its silhouette)."""
    return FUN.surf(f, np.pi, 1.0, P_FUN)


def ball(pos, r=0.2):
    return Circle(radius=r, stroke_color=TEXT, stroke_width=3, fill_color=BLUE, fill_opacity=1.0).move_to(pos).set_z_index(10)


def rollw(sc, b, f0, f1, t=1.0, rate=smooth, extra=()):
    """Roll the ball down the left wall of the funnel."""
    sc.play(UpdateFromAlphaFunc(b, lambda m, a: m.move_to(WL(f0 + (f1 - f0) * a))), *extra, run_time=t, rate_func=rate)


SX = -5.4   # the drop ruler: every step down the funnel is marked in this one column


def stepmark(f0, f1):
    """A visible drop marker for one step down the funnel: a dashed level line to the ruler and a green drop arrow."""
    a, b = WL(f0), WL(f1)
    lv = DashedLine([a[0] - 0.25, a[1], 0], [SX, a[1], 0], color=GREEN, stroke_width=2)
    lv2 = DashedLine([b[0] - 0.25, b[1], 0], [SX, b[1], 0], color=GREEN, stroke_width=2)
    ar = Arrow([SX, a[1], 0], [SX, b[1], 0], buff=0, color=GREEN, stroke_width=7, tip_length=0.22, max_tip_length_to_length_ratio=0.7)
    return VGroup(lv, lv2, ar).set_z_index(9)


def droplabel(f0, f1, txt="energy\ndrops"):
    a, b = WL(f0), WL(f1)
    t = T(txt, size=28, color=GREEN, line_spacing=0.6)
    t.next_to([SX, (a[1] + b[1]) / 2, 0], LEFT, buff=0.12)
    return t.set_z_index(9)


def arrows_in(fun, p, f0=0.94, f1=0.72):
    ths = np.linspace(0, 2 * np.pi, 8, endpoint=False) + 0.39
    out = []
    for th in ths:
        a, b = fun.surf(f0, th, 1.0, p), fun.surf(f1, th, 1.0, p)
        d = (b - a) / np.linalg.norm(b - a)
        out.append(Arrow(a, a + 0.8 * d, buff=0, stroke_width=6, color=TEXT, tip_length=0.28,
                         max_tip_length_to_length_ratio=0.5).set_z_index(9))   # every arrow the same length on screen
    return VGroup(*out)


# ------------------------------------------------------------------ the one-residue column and the 100-bead chain
COLX = -4.7
ICY = {"strand": 2.0, "left": 0.6, "helix": -0.8}
BEADY = -2.4
LABEL = {"strand": "strand-like", "left": "left-handed", "helix": "helix-like"}


def column(x=COLX, w=2.5):
    ic = {k: icon(k, w, sw=8).move_to([x, ICY[k], 0]) for k in ("strand", "left", "helix")}
    b = Circle(radius=0.34, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.6).move_to([x, BEADY, 0])
    stem = DashedLine([x, BEADY + 0.34, 0], [x, ICY["helix"] - 0.55, 0], color=GREY, stroke_width=2)
    return ic, b, stem


def labelled_islands(ic, r):
    labs, ars = VGroup(), VGroup()
    for kind, isl in [("helix", "alphaR"), ("strand", "beta"), ("left", "alphaL")]:
        lab = tag(LABEL[kind], size=28).next_to(ic[kind], RIGHT, buff=0.3)
        e = r.isl[isl]
        ar = Arrow(lab.get_right() + RIGHT * 0.05, e.get_left() + LEFT * 0.05, buff=0.05, color=ORANGE, stroke_width=4,
                   max_tip_length_to_length_ratio=0.15).set_z_index(6)
        labs.add(lab)
        ars.add(ar)
    return labs, ars


def bigcount(s=1.0):
    a = ex(["3", ("100",)], size=130)
    b = ex(["≈", 0.15, "5", 0.12, "×", 0.12, "10", ("47",)], size=52)
    return VGroup(a, b).arrange(DOWN, buff=0.35).scale(s)


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Protein three-dimensional structure"
    TITLE = "Downhill, Not Random"


class S01(SpokenScene):
    def construct(self):
        mk = lambda i: beadchain(3 + i, n=16, w=12.4, h=4.6, cy=0.85, r=0.24, op=(1.0 if i == 0 else 0.3))
        chain = mk(0)
        self.play(FadeIn(chain), run_time=0.5)
        ghost = mk(10)
        ghost.set_opacity(0.3)
        self.add(ghost)
        flicker(ghost, lambda i: beadchain(10 + i, n=16, w=12.4, h=4.6, cy=0.85, r=0.24, op=0.3), period=0.3)
        q = VGroup(T("How does the chain find its fold", size=42), T("without trying every shape?", size=42, color=YELLOW))
        q.arrange(DOWN, buff=0.15).move_to([0, -2.95, 0])
        self.wait(0.3)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.at("without trying every")
        self.play(Indicate(q[1], color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.finish()


def chain100():
    """100 beads in four rows of 25: the chain."""
    DX = 0.4
    X0 = -DX * 12
    ys = [-1.35, -1.95, -2.55, -3.15]
    lines, beads = VGroup(), VGroup()
    for y in ys:
        lines.add(Line([X0 - 0.15, y, 0], [X0 + 24 * DX + 0.15, y, 0], stroke_color=BLUE, stroke_width=3))
        for c in range(25):
            beads.add(Circle(radius=0.12, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.6).move_to([X0 + c * DX, y, 0]))
    return lines, beads


class S02(SpokenScene):
    def construct(self):
        lines, beads = chain100()
        head = T("Count the options", size=40, font=TITLE_FONT).move_to([0, 3.5, 0])
        self.play(FadeIn(head), run_time=0.4)
        self.play(FadeIn(lines), LaggedStart(*[FadeIn(b, scale=0.5) for b in beads], lag_ratio=0.008), run_time=1.0)
        n1 = T("1", size=26, color=GREY).move_to(beads[0].get_center() + LEFT * 0.5)
        n2 = T("100", size=26, color=GREY).move_to(beads[-1].get_center() + RIGHT * 0.65)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.25)
        self.at("give each residue")
        big = Circle(radius=0.42, stroke_color=YELLOW, stroke_width=5, fill_color=BLUE, fill_opacity=0.6).move_to([0, 0.2, 0])
        bl = T("one residue", size=28, color=YELLOW).next_to(big, RIGHT, buff=0.3)
        self.play(Indicate(beads[0], scale_factor=2.0, color=YELLOW), FadeIn(big, scale=0.6), FadeIn(bl), run_time=0.8)
        self.at("just three backbone")
        kinds = ("strand", "left", "helix")
        xs = [-3.7, 0.0, 3.7]
        ics = [icon(k, 2.8, sw=8).move_to([x, 1.8, 0]) for k, x in zip(kinds, xs)]
        cons = [DashedLine(big.get_top(), [x, 1.25, 0], color=GREY, stroke_width=2) for x in xs]
        cap = T("3 backbone shapes per residue", size=34, color=ORANGE).move_to([0, 2.85, 0])
        self.play(*[Create(c) for c in cons], *[FadeIn(i, shift=DOWN * 0.1) for i in ics], FadeIn(cap), run_time=1.0)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        ic, b, stem = column()
        rama = Rama(3.2, 0.0, 5.4)
        self.play(FadeIn(b), FadeIn(stem), *[FadeIn(i) for i in ic.values()], run_time=0.5)
        self.at("island of the map")
        self.play(*[FadeIn(p) for p in rama.parts()], run_time=0.8)
        for kind, isl in [("helix", "alphaR"), ("strand", "beta"), ("left", "alphaL")]:
            self.at({"helix": "helix like", "strand": "strand like", "left": "left handed"}[kind])
            lab = tag(LABEL[kind], size=28).next_to(ic[kind], RIGHT, buff=0.3)
            e = rama.isl[isl]
            ar = Arrow(lab.get_right() + RIGHT * 0.05, e.get_left() + LEFT * 0.05, buff=0.05, color=ORANGE, stroke_width=4,
                       max_tip_length_to_length_ratio=0.15).set_z_index(6)
            self.play(FadeIn(lab), Indicate(ic[kind], color=YELLOW, scale_factor=1.2), Create(ar),
                      e.animate.set_fill(GREEN, 0.35), run_time=0.7)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        cap = T("3 shapes per residue, 100 residues", size=34, color=GREY).move_to([0, 2.95, 0])
        a = ex(["3", ("100",)], size=170).move_to([0, 0.9, 0])
        self.play(FadeIn(cap), FadeIn(a, shift=UP * 0.1), run_time=0.7)
        self.at("47 zeros")
        b = ex(["≈", 0.2, "5", 0.15, "×", 0.15, "10", ("47",)], size=84)
        sh = T("shapes", size=60)
        VGroup(b, sh).arrange(RIGHT, buff=0.35, aligned_edge=DOWN).move_to([0, -1.5, 0])
        self.play(FadeIn(b, shift=UP * 0.15), FadeIn(sh, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        mk = lambda i: beadchain(40 + i, n=15, w=10.6, h=3.0, cy=2.0, r=0.22)
        chain = mk(0)
        self.play(FadeIn(chain), run_time=0.6)
        self.at("tried a new shape")
        flicker(chain, mk, period=0.14)
        self.at("tenth of a trillionth")
        t1 = VGroup(T("1 shape per", size=62), ex(["10", ("−13",), 0.2, "s"], size=62)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        t1.move_to([0, -0.9, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.7)
        self.at("as fast as a bond")
        c = np.array([-4.4, -2.55, 0.0])
        a1 = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.5).move_to(c + LEFT * 0.7)
        a2 = Circle(radius=0.3, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.5).move_to(c + RIGHT * 0.7)
        rod = Line(c + LEFT * 0.7, c + RIGHT * 0.7, color=ORANGE, stroke_width=10)
        spin = VGroup(rod, a1, a2)
        spin.add_updater(lambda m, dt: m.rotate(dt * 9, about_point=c))
        lab = T("as fast as a bond can turn", size=38, color=LIGHT).move_to([1.2, -2.55, 0])
        self.play(FadeIn(spin), FadeIn(lab), run_time=0.4)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        base = -2.7
        cc = np.array([-4.8, 0.7, 0.0])
        face = Circle(radius=1.2, stroke_color=GREY, stroke_width=5).move_to(cc)
        hand = Line(cc, cc + UP * 1.0, color=TEXT, stroke_width=6)
        ticks = VGroup(*[Line(cc + 1.05 * np.array([np.sin(a), np.cos(a), 0]), cc + 1.2 * np.array([np.sin(a), np.cos(a), 0]), color=GREY, stroke_width=3)
                         for a in np.arange(0, 2 * np.pi, np.pi / 6)])
        hand.add_updater(lambda m, dt: m.rotate(-dt * 7, about_point=cc))
        clk = T("time passing", size=28, color=GREY).move_to(cc + DOWN * 1.75)
        floor = Line([-2.7, base, 0], [6.5, base, 0], color=GREY, stroke_width=3)
        yax = Arrow([-2.7, base, 0], [-2.7, 3.0, 0], buff=0, color=GREY, stroke_width=4)
        yl = T("years (linear scale)", size=26, color=GREY).rotate(PI / 2).move_to([-3.15, 0.2, 0])
        self.add(floor, yax, yl)
        self.at("trying them all")
        bar = Rectangle(width=2.0, height=0.01, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to([4.5, base + 0.005, 0])
        tr = ValueTracker(0.01)
        bar.add_updater(lambda m: m.become(Rectangle(width=2.0, height=tr.get_value(), stroke_width=0, fill_color=RED, fill_opacity=0.9)
                                           .move_to([4.5, base, 0], aligned_edge=DOWN)))
        self.add(bar)
        self.play(FadeIn(face), FadeIn(ticks), FadeIn(hand), FadeIn(clk), tr.animate.set_value(4.3), run_time=1.4, rate_func=smooth)
        bar.clear_updaters()
        rl = VGroup(T("the random search", size=30, color=RED), ex(["≈", 0.15, "10", ("27",), 0.2, "years"], size=40, color=RED)).arrange(DOWN, buff=0.1).move_to([4.5, 2.5, 0])
        self.play(FadeIn(rl, shift=DOWN * 0.1), run_time=0.4)
        self.at("the universe has existed")
        ub = Rectangle(width=2.0, height=0.07, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to([0.2, base, 0], aligned_edge=DOWN)
        ul = VGroup(T("age of the universe", size=30, color=TEXT), ex(["≈", 0.15, "10", ("10",), 0.2, "years"], size=40)).arrange(DOWN, buff=0.1).move_to([0.2, -1.4, 0])
        self.play(FadeIn(ub), FadeIn(ul, shift=DOWN * 0.1), run_time=0.7)
        note = T("(universe bar drawn thicker than true scale)", size=26, color=GREY).move_to([1.9, -3.35, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        W, Hh, Y = 5.4, 3.4, -0.5
        red = VGroup(RoundedRectangle(corner_radius=0.2, width=W, height=Hh, stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.15),
                     VGroup(T("the random search", size=38, color=RED), ex(["≈", 0.15, "10", ("27",), 0.2, "years"], size=54, color=RED)).arrange(DOWN, buff=0.25))
        red[1].move_to(red[0])
        red.move_to([3.9, Y, 0])
        self.play(FadeIn(red), run_time=0.3)
        self.at("small proteins fold")
        grn = VGroup(RoundedRectangle(corner_radius=0.2, width=W, height=Hh, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.15),
                     T("real folding", size=46, color=GREEN))
        grn[1].move_to(grn[0].get_center() + UP * 0.55)
        grn.move_to([-3.9, Y, 0])
        self.play(FadeIn(grn), run_time=0.5)
        sub = T("microseconds to seconds", size=28, color=TEXT).move_to(grn[0].get_center() + DOWN * 0.6)
        self.at("microseconds to seconds")
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.4)
        self.at("gap is", lead=0.4)
        gap = DoubleArrow([-1.15, Y, 0], [1.15, Y, 0], buff=0, color=YELLOW, stroke_width=7)
        gl = T("the gap", size=38, color=YELLOW).move_to([0, Y + 0.55, 0])
        title = T("Levinthal's paradox", size=64, font=TITLE_FONT).move_to([0, 2.75, 0])
        rule = Line(title.get_left() + DOWN * 0.5, title.get_right() + DOWN * 0.5, color=GOLD, stroke_width=4)
        self.play(Create(gap), FadeIn(gl), FadeIn(title, shift=DOWN * 0.1), Create(rule), run_time=0.6)
        self.finish()


def count_left():
    return bigcount(0.8).move_to([-4.3, 0.45, 0])


def question_8():
    return T("Does the filter solve it?", size=46, color=YELLOW).move_to([0, -3.3, 0])


class S08(SpokenScene):
    def construct(self):
        cnt = count_left()
        r = Rama(1.4, 0.45, 4.6)
        q = question_8()
        self.play(FadeIn(cnt), FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.at("plot forbids most")
        self.play(*[FadeIn(p) for p in r.parts()], run_time=0.8)
        ft = tag("forbidden", RED, 26, r.c2p(100, -125))
        self.play(FadeIn(ft), run_time=0.5)
        self.at("does that solve")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.06), run_time=0.8)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        cnt = count_left()
        r = Rama(1.4, 0.45, 4.6)
        ft = tag("forbidden", RED, 26, r.c2p(100, -125))
        q = question_8()
        self.add(cnt, *r.parts(), ft, q)
        cen = np.array([5.45, 0.45, 0.0])
        ring_bg = Circle(radius=0.85, stroke_color=GREY, stroke_width=6).move_to(cen)
        ring = Circle(radius=0.85, stroke_color=GOLD, stroke_width=10).move_to(cen).rotate(PI / 2).flip(UP)
        think = T("Think", size=34, color=GOLD).move_to(cen)
        self.add(ring_bg, think)
        self.play(Create(ring), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        ic, b, stem = column()
        r = Rama(3.2, 0.0, 5.4)
        labs, ars = labelled_islands(ic, r)
        self.add(*r.parts(), b, stem, *ic.values(), labs, ars, *r.isl.values())
        for e in r.isl.values():
            e.set_fill(GREEN, 0.35)
        self.at("the count already used it")
        fl = T("filter already applied", size=44, color=GREEN).move_to([-3.6, -3.3, 0])
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.6)
        self.at("three shapes per residue")
        self.play(*[Indicate(i, color=YELLOW, scale_factor=1.2) for i in ic.values()], run_time=0.9)
        self.at("what the filter left behind")
        self.play(*[Indicate(e, color=YELLOW, scale_factor=1.3) for e in r.isl.values()], run_time=0.9)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        ic, b, stem = column()
        self.add(b, stem, *ic.values())
        self.at("only two shapes")
        cross = Cross(ic["left"], stroke_color=RED, stroke_width=7)
        self.play(Create(cross), run_time=0.4)
        self.play(FadeOut(ic["left"]), FadeOut(cross), run_time=0.4)
        eq = VGroup(ex(["2", ("100",)], size=130), ex(["≈", 0.15, "10", ("30",)], size=64)).arrange(DOWN, buff=0.35)
        sh = T("shapes", size=50).next_to(eq[1], RIGHT, buff=0.3)
        eq.add(sh)
        eq.move_to([1.7, 1.0, 0])
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.7)
        self.at("billions of years")
        yrs = T("billions of years", size=64, color=RED).move_to([1.7, -1.7, 0])
        self.play(FadeIn(yrs, shift=UP * 0.1), run_time=0.7)
        self.finish()


def factor_row(vals, y=1.0):
    """Boxes for residue 1, 2, 3 ... 99, 100, joined by multiplication signs."""
    W = 1.45
    names = ["residue 1", "residue 2", "residue 3", None, "residue 99", "residue 100"]
    xs = [-5.3, -3.2, -1.1, 0.95, 2.9, 5.0]
    boxes, dots, labs, times = [], None, VGroup(), VGroup()
    for n, x in zip(names, xs):
        if n is None:
            dots = T("···", size=60, color=GREY).move_to([x, y, 0])
            continue
        bx = VGroup(RoundedRectangle(corner_radius=0.15, width=W, height=1.9, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.2),
                    T(str(vals), size=90, color=TEXT)).move_to([x, y, 0])
        bx[1].move_to(bx[0])
        boxes.append(bx)
        labs.add(T(n, size=28, color=LIGHT).move_to([x, y - 1.35, 0]))
    for x in (-4.25, -2.15, -0.05, 1.9, 3.95):
        times.add(T("×", size=44, color=GREY).move_to([x, y, 0]))
    return VGroup(*boxes), dots, labs, times


class S12(SpokenScene):
    def construct(self):
        boxes, dots, labs, times = factor_row(3)
        lab = T("factor per residue:", size=44)
        three = T("3", size=60, color=TEXT)
        hd = VGroup(lab, three).arrange(RIGHT, buff=0.3).move_to([0, 3.0, 0])
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in boxes], lag_ratio=0.12), FadeIn(dots), FadeIn(times), FadeIn(labs), FadeIn(hd), run_time=1.4)
        self.at("makes each factor smaller")
        two = T("2", size=60, color=GREEN).move_to(three)
        newb = [T("2", size=90, color=GREEN).move_to(b[0]) for b in boxes]
        self.play(LaggedStart(*[Transform(b[1], n) for b, n in zip(boxes, newb)], lag_ratio=0.12), Transform(three, two),
                  *[b[0].animate.set_stroke(GREEN).set_fill(GREEN, 0.2) for b in boxes], run_time=1.2)
        self.at("there are still")
        br = Brace(Line([-6.0, -0.8, 0], [5.7, -0.8, 0]), DOWN, color=GREY)
        bl = T("still 100 factors", size=48, color=YELLOW).next_to(br, DOWN, buff=0.2)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.8)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        boxes, dots, labs, times = factor_row(2, y=-2.3)
        for b in boxes:
            b[0].set_stroke(GREEN).set_fill(GREEN, 0.2)
            b[1].set_color(GREEN)
        back = VGroup(boxes, dots, times).set_opacity(0.3)
        self.add(back)
        self.at("not fewer shapes")
        n1 = T("not", size=96, color=RED)
        t1 = T("fewer shapes", size=96, color=TEXT)
        VGroup(n1, t1).arrange(RIGHT, buff=0.5).move_to([0, 2.0, 0])
        self.play(FadeIn(n1), FadeIn(t1), run_time=0.6)
        self.play(Create(Line(t1.get_left() + LEFT * 0.1, t1.get_right() + RIGHT * 0.1, color=RED, stroke_width=9)), run_time=0.4)
        self.at("the residues do not choose")
        t2 = fit(T("the residues do not choose blindly", size=66, color=GREEN), max_w=12.4).move_to([0, 0.3, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.8)
        self.finish()


def wrong_dots():
    pts = [(-3.6, -0.5), (-2.2, 1.4), (-0.9, -1.2), (1.6, 1.5), (3.0, -0.9), (4.0, 0.9), (-4.4, 1.0), (0.9, -1.6), (-1.7, -0.2), (2.6, 0.2),
           (-0.3, 1.9), (3.9, -0.3)]
    return VGroup(*[Dot([x, y, 0], radius=0.12, color=RED).set_opacity(0.8) for x, y in pts])


class S14(SpokenScene):
    def construct(self):
        f = plane(0)
        self.play(FadeIn(f[0]), run_time=0.8)
        self.at("one hole")
        self.add(f)
        self.play(FadeIn(f[-1], scale=1.5), run_time=0.6)
        ht = tag("the one right shape", GREEN, 34, [-3.9, 3.35, 0])
        ld = Line(ht.get_right() + RIGHT * 0.05, f[-1].get_left() + UP * 0.1, color=GREEN, stroke_width=4)
        self.play(FadeIn(ht), Create(ld), run_time=0.5)
        self.at("every wrong shape")
        dots = wrong_dots()
        w = tag("every wrong shape: equally good", RED, 34, [0, -3.2, 0])
        self.play(FadeIn(w, shift=UP * 0.1), FadeIn(dots, lag_ratio=0.1), run_time=0.9)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        f = plane(0)
        self.add(f)
        b = ball([-4.0, -0.9, 0], r=0.27)
        self.add(b)
        trail = VGroup()
        self.add(trail)
        path = [(-2.6, 1.9), (-1.4, -1.4), (2.4, 1.7), (3.8, -0.8), (1.0, -1.2), (-0.5, 1.9)]
        self.at("the ball rolls at random")
        last = np.array([-4.0, -0.9, 0.0])
        misses = []
        for (x, y) in path:
            p = np.array([x, y, 0.0])
            ln = Line(last, p, color=GREY, stroke_width=3, stroke_opacity=0.6)
            d = Dot(p, radius=0.11, color=RED).set_opacity(0.85)
            self.add(ln)
            self.play(b.animate.move_to(p), run_time=0.3, rate_func=smooth)
            self.add(d)
            trail.add(ln, d)
            misses.append(d)
            last = p
        self.at("almost never drops in")
        for (x, y) in [(1.1, 0.3), (-3.0, -1.2)]:
            p = np.array([x, y, 0.0])
            ln = Line(last, p, color=GREY, stroke_width=3, stroke_opacity=0.6)
            self.add(ln)
            self.play(b.animate.move_to(p), run_time=0.45)
            trail.add(ln)
            last = p
        ml = tag("misses", RED, 30, [-3.0, 2.9, 0])
        mld = Line(ml.get_bottom() + DOWN * 0.02, misses[0].get_center() + UP * 0.12, color=RED, stroke_width=3)
        self.play(FadeIn(ml), Create(mld), run_time=0.4)
        self.at("random search")
        lab = T("random search", size=54, color=RED).move_to([0, -3.2, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        f = plane(0)
        self.add(f)
        self.at("tilt the ground toward the hole")
        self.play(UpdateFromAlphaFunc(f, lambda m, a: m.become(plane(a))), run_time=1.6, rate_func=smooth)
        self.at("from every side")
        ars = arrows_in(FUN, P_FUN)
        self.play(LaggedStart(*[GrowArrow(a) for a in ars], lag_ratio=0.1), run_time=0.9)
        self.at("each roll tends")
        ths = [-0.45, -2.6, 0.9, 2.3]
        bs = [ball(FUN.surf(1.0, th, 1.0, P_FUN), 0.16) for th in ths]
        self.play(FadeOut(ars), *[FadeIn(x, scale=1.4) for x in bs], run_time=0.4)
        ends = []
        for x, th in zip(bs, ths):
            def fn(m, a, th=th):
                m.move_to(FUN.surf(1.0 - 0.7 * a, th + 0.5 * np.sin(4 * a), 1.0, P_FUN))
            ends.append(UpdateFromAlphaFunc(x, fn))
        self.play(*ends, run_time=2.2, rate_func=rush_into)
        self.finish()


def bowl_balls():
    ths = [-0.45, -2.6, 0.9, 2.3]
    return [ball(FUN.surf(0.3, th + 0.5 * np.sin(4), 1.0, P_FUN), 0.16) for th in ths]


class S17(SpokenScene):
    def construct(self):
        f = FUN.make(1.0, P_FUN)
        bs = bowl_balls()
        self.add(f, *bs)
        self.at("the folding funnel")
        tt = T("the folding funnel", size=48, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.play(FadeOut(VGroup(*bs)), FadeIn(tt, shift=DOWN * 0.1), run_time=1.3)
        self.at("its width stands for")
        ar = DoubleArrow([-4.7, 1.2, 0], [4.7, 1.2, 0], buff=0, color=YELLOW, stroke_width=6).set_z_index(7)
        self.play(Create(ar), run_time=0.7)
        self.at("many unfolded shapes")
        lab = tag("many unfolded shapes", YELLOW, 36, [0, 1.85, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        f = FUN.make(1.0, P_FUN)
        tt = T("the folding funnel", size=48, font=TITLE_FONT).move_to([0, 3.4, 0])
        ar = DoubleArrow([-4.7, 1.2, 0], [4.7, 1.2, 0], buff=0, color=YELLOW, stroke_width=6).set_z_index(7)
        lab = tag("many unfolded shapes", YELLOW, 36, [0, 1.85, 0])
        self.add(f, tt, ar, lab)
        self.at("its depth stands for")
        ax = Arrow([-6.55, -2.7, 0], [-6.55, 2.8, 0], buff=0, color=GREEN, stroke_width=6)
        el = T("energy:\nlower = more\nfavorable\ncontacts", size=26, color=GREEN, line_spacing=0.7).move_to([-5.3, -0.9, 0])
        hi = T("high", size=26, color=GREY).move_to([-5.95, 2.2, 0])
        lo = T("low", size=26, color=GREY).move_to([-5.95, -2.2, 0])
        self.play(Create(ax), FadeIn(el), FadeIn(hi), FadeIn(lo), run_time=1.0)
        self.at("the native fold sits")
        nf = T("native fold", size=40, color=GREEN).move_to([0, -3.35, 0])
        nl = Line(nf.get_top() + UP * 0.05, FUN.cen(0.0, 1.0, P_FUN) + DOWN * 0.25, color=GREEN, stroke_width=3)
        self.play(FadeIn(nf, shift=UP * 0.1), Create(nl), Indicate(f[-1], color=GREEN, scale_factor=1.6), run_time=0.9)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        f = FUN.make(1.0, P_FUN)
        b = ball(WL(1.0), 0.18)
        self.add(f, b)
        q = VGroup(T("What makes", size=50), T("the slope?", size=50)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-4.85, -2.1, 0])
        self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=0.7)
        self.at("the same forces")
        a = VGroup(T("the same forces", size=34, color=GREEN), T("that make the", size=34, color=GREEN),
                   T("fold stable", size=34, color=GREEN)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([4.7, -1.9, 0])
        self.play(FadeIn(a, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        f = FUN.make(1.0, P_FUN)
        b = ball(WL(1.0), 0.18)
        self.add(f, b)
        core = DashedVMobject(Circle(radius=1.15, color=GREY, stroke_width=3)).move_to([-4.6, -2.1, 0])
        cl = T("core", size=26, color=GREY).move_to([-4.6, -3.55, 0])
        self.at("two oily side chains")
        A = VGroup(Circle(radius=0.5, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.35), T("oily", size=26, color=YELLOW)).move_to([-6.0, -2.1, 0])
        B = VGroup(Circle(radius=0.5, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.35), T("oily", size=26, color=YELLOW)).move_to([-3.2, -2.1, 0])
        wat = VGroup(*[chip("H₂O", TEAL, 26, 0.1).move_to(p) for p in [[-5.8, -0.95, 0], [-3.75, -0.95, 0], [-4.8, -0.4, 0]]])
        self.play(FadeIn(A), FadeIn(B), FadeIn(wat), run_time=0.6)
        self.at("meet in the core")
        self.play(FadeIn(core), FadeIn(cl), A.animate.move_to([-5.15, -2.1, 0]), B.animate.move_to([-4.05, -2.1, 0]), run_time=1.0)
        self.at("some water is freed")
        outs = [LEFT * 0.7 + UP * 0.5, RIGHT * 0.4 + UP * 0.5, UP * 0.7]
        self.play(*[w.animate.shift(d).set_opacity(0.0) for w, d in zip(wat, outs)], run_time=1.2)
        fw = T("water freed", size=30, color=TEAL).move_to([-4.8, -0.7, 0])
        self.play(FadeIn(fw), run_time=0.4)
        self.at("the energy drops")
        sm = stepmark(1.0, 0.86)
        dl = droplabel(1.0, 0.86)
        rollw(self, b, 1.0, 0.86, t=0.8, extra=[Create(sm), FadeIn(dl)])
        self.finish()


def helix_stretch(coil, cx=-4.6, cy=-2.35, w=3.4):
    xs = np.linspace(-w / 2, w / 2, 200)
    out = []
    for x in xs:
        if coil:
            y = 0.5 * np.sin(x * 2 * np.pi / 0.85)
        else:
            y = 0.35 * np.sin(2.1 * x + 0.5) * np.sin(0.9 * x + 1.0) + 0.12 * np.sin(5.3 * x)
        out.append(np.array([cx + x, cy + y, 0.0]))
    m = VMobject(stroke_color=BLUE, stroke_width=7)
    m.set_points_smoothly(out)
    return m


class S21(SpokenScene):
    def construct(self):
        f = FUN.make(1.0, P_FUN)
        b = ball(WL(0.86), 0.18)
        old = stepmark(1.0, 0.86)
        self.add(f, b, old)
        limp = helix_stretch(False)
        ll = T("backbone stretch", size=30, color=BLUE).move_to([-4.6, -1.15, 0])
        self.play(FadeIn(limp), FadeIn(ll), run_time=0.7)
        self.at("its first helical")
        self.play(Transform(limp, helix_stretch(True)), run_time=0.8)
        self.at("hydrogen bonds")
        dl = VGroup()
        for k in range(3):
            x0 = -4.6 - 1.7 + 0.85 * 0.25 + 0.85 * k
            dl.add(DashedLine([x0, -1.85, 0], [x0 + 0.85, -1.85, 0], color=ORANGE, stroke_width=5, dash_length=0.1))
            dl.add(DashedLine([x0 + 0.425, -2.85, 0], [x0 + 1.275, -2.85, 0], color=ORANGE, stroke_width=5, dash_length=0.1))
        hl = T("hydrogen bonds", size=30, color=ORANGE).move_to([-4.6, -1.15, 0])
        self.play(Create(dl), Transform(ll, hl), run_time=0.7)
        self.at("it drops a little more")
        sm = stepmark(0.86, 0.72)
        d2 = droplabel(0.86, 0.72)
        rollw(self, b, 0.86, 0.72, t=0.8, extra=[Create(sm), FadeIn(d2)])
        self.finish()


class S22(SpokenScene):
    def construct(self):
        f = FUN.make(1.0, P_FUN)
        b = ball(WL(0.72), 0.18)
        old = VGroup(stepmark(1.0, 0.86), stepmark(0.86, 0.72))
        self.add(f, b, old)
        bd = lambda x, y: Circle(radius=0.55, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.3).move_to([x, y, 0])
        a1, a2 = bd(-5.9, -1.6), bd(-3.9, -1.6)
        la = T("residue A", size=26, color=LIGHT).next_to(a1, DOWN, buff=0.2)
        lb = T("residue B", size=26, color=LIGHT).next_to(a2, DOWN, buff=0.2)
        lk1 = Line(a1.get_right(), a2.get_left(), color=GREEN, stroke_width=8).set_z_index(5)
        g1 = VGroup(lk1, a1, a2, la, lb)
        self.at("partly correct shapes")
        self.play(FadeIn(g1), run_time=0.6)
        self.at("tend to last")
        l1 = T("right contact: stays", size=30, color=GREEN).move_to([-4.9, -3.35, 0])
        lk1b = Line(a1.get_right() + UP * 0.22, a2.get_left() + UP * 0.25, color=GREEN, stroke_width=8).set_z_index(5)
        lk1c = Line(a1.get_right() + DOWN * 0.22, a2.get_left() + DOWN * 0.25, color=GREEN, stroke_width=8).set_z_index(5)
        sm = stepmark(0.72, 0.6)
        dd = droplabel(0.72, 0.6)
        rollw(self, b, 0.72, 0.6, t=0.8, extra=[FadeIn(l1, shift=UP * 0.1), Create(lk1b), Create(lk1c), Create(sm), FadeIn(dd),
                                               Indicate(lk1, color=GREEN, scale_factor=1.15)])
        self.at("wrong contacts")
        c1, c2 = bd(4.0, -1.6), bd(6.0, -1.6)
        lc = T("residue A", size=26, color=LIGHT).next_to(c1, DOWN, buff=0.2)
        ld = T("residue B", size=26, color=LIGHT).next_to(c2, DOWN, buff=0.2)
        lk2 = Line(c1.get_right(), c2.get_left(), color=RED, stroke_width=8).set_z_index(5)
        l2 = T("wrong contact", size=30, color=RED).move_to([5.0, -3.35, 0])
        self.play(FadeIn(VGroup(c1, c2, lc, ld, lk2, l2)), run_time=0.6)
        self.at("to break apart")
        for _ in range(3):
            self.play(lk2.animate.set_stroke(opacity=0.1), run_time=0.1)
            self.play(lk2.animate.set_stroke(opacity=1.0), run_time=0.1)
        l3 = T("breaks apart again", size=30, color=RED).move_to(l2)
        self.play(c1.animate.shift(LEFT * 0.35), c2.animate.shift(RIGHT * 0.35), lc.animate.shift(LEFT * 0.35), ld.animate.shift(RIGHT * 0.35),
                  FadeOut(lk2), Transform(l2, l3), run_time=0.8)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        f = FUN.make(1.0, P_FUN)
        fs = [1.0, 0.86, 0.72, 0.6]
        b = ball(WL(0.6), 0.18)
        old = VGroup(*[stepmark(fs[i], fs[i + 1]) for i in range(3)])
        self.add(f, b, old)
        self.at("keep more of what")
        t1 = tag("keep more of what is right", GREEN, 40, [0, 3.35, 0])
        self.play(FadeIn(t1, shift=DOWN * 0.1), run_time=0.5)
        steps = [0.6, 0.5, 0.41, 0.33, 0.25, 0.17, 0.1]
        cue = False
        for i in range(len(steps) - 1):
            if not cue and self.elapsed() >= self.t_of("a small preference") - 0.3:
                cue = True
                t2 = tag("a small preference at each step", GOLD, 40, [0, 3.35, 0])
                self.play(FadeOut(t1), FadeIn(t2), run_time=0.4)
            sm = stepmark(steps[i], steps[i + 1])
            rollw(self, b, steps[i], steps[i + 1], t=0.3, extra=[Create(sm)])
            self.wait(0.2)
        self.finish()


# --------------------------- cross-section of one funnel wall (scenes 24 to 26)
X0P, LP, HP, YB = 0.6, 6.4, 4.4, -2.2
AB, XB, SB = 1.25, -3.3, 0.5          # the small hill (first contacts)
DB, XU, SU = 1.3, -5.0, 0.55          # the shallow basin of the unfolded state
DT, XT, ST = 0.7, -2.1, 0.25          # the kinetic trap
XAX0, YAX0 = -6.2, -3.05


def prof(x, trap=False):
    s = abs(x - X0P) / LP
    y = YB + HP * s ** 1.5
    if x < X0P:
        y += AB * np.exp(-(((x - XB) / SB) ** 2)) - DB * np.exp(-(((x - XU) / SU) ** 2))
        if trap:
            y -= DT * np.exp(-(((x - XT) / ST) ** 2))
    return y


XL = np.linspace(-5.6, X0P, 260)
XR = np.linspace(X0P, 1.5, 60)


def curve(trap=False):
    pl = [np.array([x, prof(x, trap), 0.0]) for x in XL]
    pr = [np.array([x, prof(x, trap), 0.0]) for x in XR]
    m = VMobject(stroke_color=LIGHT, stroke_width=6)
    m.set_points_smoothly(pl)
    stub = VMobject(stroke_color=LIGHT, stroke_width=6, stroke_opacity=0.3)
    stub.set_points_smoothly(pr)
    fillp = VMobject(stroke_width=0, fill_color=BLUE, fill_opacity=0.12)
    fillp.set_points_as_corners([np.array([-5.6, YAX0, 0.0])] + pl + pr + [np.array([1.5, YAX0, 0.0])])
    return VGroup(fillp, m, stub)


def onc(x, trap=False, r=0.2):
    return np.array([x, prof(x, trap) + r + 0.02, 0.0])


def xbasin():
    xs = np.linspace(-5.4, -4.2, 400)
    return xs[np.argmin([prof(x) for x in xs])]


def xpeak():
    xs = np.linspace(-4.0, -2.8, 400)
    return xs[np.argmax([prof(x) for x in xs])]


def xtrap():
    xs = np.linspace(-2.5, -1.7, 400)
    return xs[np.argmin([prof(x, True) for x in xs])]


def xlip():
    xs = np.linspace(-2.0, -1.0, 400)
    return xs[np.argmax([prof(x, True) for x in xs])]


def move_x(sc, b, x0, x1, trap=False, t=1.0, rate=smooth, extra=()):
    sc.play(UpdateFromAlphaFunc(b, lambda m, a: m.move_to(onc(x0 + (x1 - x0) * a, trap))), *extra, run_time=t, rate_func=rate)


def axes_group():
    yax = Arrow([XAX0, YAX0, 0], [XAX0, 3.4, 0], buff=0, color=GREY, stroke_width=4)
    xax = Arrow([XAX0, YAX0, 0], [2.7, YAX0, 0], buff=0, color=GREY, stroke_width=4)
    yl = T("energy (free energy)", size=26, color=LIGHT).rotate(PI / 2).move_to([-6.55, 0.2, 0])
    xl = T("progress toward the native fold", size=26, color=LIGHT).move_to([-1.9, -3.5, 0])
    return VGroup(yax, xax, yl, xl)


def native_label():
    return T("native fold", size=28, color=GREEN).move_to([X0P, -2.62, 0])


def chap_chain(cx, cy):
    pts = []
    for i in np.linspace(0, 1, 120):
        xx = 2.2 * i - 1.1
        y = 0.42 * np.sin(i * 24) if i < 0.5 else 0.14 * np.sin(i * 7)
        pts.append(np.array([cx + xx, cy + y, 0.0]))
    m = VMobject(stroke_color=BLUE, stroke_width=6)
    m.set_points_smoothly(pts)
    return m


C1, C2 = (1.9, 1.6), (5.2, 1.6)


def clump_links(x1=4.1):
    return VGroup(*[Line([3.0, C1[1] + dy, 0], [x1, C2[1] + dy, 0], color=RED, stroke_width=6) for dy in (-0.35, 0.0, 0.35)])


def cage():
    return DashedVMobject(RoundedRectangle(corner_radius=0.3, width=3.4, height=2.6, color=ORANGE, stroke_width=6)).move_to([C1[0], C1[1], 0])


class S24(SpokenScene):
    def construct(self):
        fun = FUN.make(1.0, P_FUN)
        b = ball(WL(1.0), 0.18)
        # the slice of the funnel wall that will become the energy profile
        fs = np.linspace(1.0, 0.07, 260)
        sl = VMobject(stroke_color=YELLOW, stroke_width=7)
        sl.set_points_smoothly([WL(f) for f in fs])
        sll = tag("one slice through the funnel", YELLOW, 28, [-4.3, -1.3, 0])
        self.play(FadeIn(fun), FadeIn(b), run_time=0.4)
        self.play(Create(sl), FadeIn(sll), run_time=0.5)
        cv = curve(False)
        ax = axes_group()
        nat = native_label()
        xb, xp = xbasin(), xpeak()
        unf = T("unfolded", size=28, color=BLUE).move_to([xb + 0.3, 2.2, 0])
        self.play(FadeOut(fun), FadeOut(sll), Transform(sl, cv[1]), FadeIn(cv[0]), FadeIn(cv[2]), FadeIn(ax), FadeIn(nat), FadeIn(unf),
                  b.animate.move_to(onc(xb)), run_time=1.1)
        self.remove(sl)
        self.add(cv)
        self.at("first few contacts")
        cost = VGroup(DashedLine([xb - 0.4, prof(xb), 0], [xp + 0.45, prof(xb), 0], color=GREY, stroke_width=2),
                      DoubleArrow([xp, prof(xb), 0], [xp, prof(xp), 0], buff=0, color=GOLD, stroke_width=5, tip_length=0.18),
                      T("small\nuphill cost", size=26, color=GOLD, line_spacing=0.6).move_to([xp - 0.9, prof(xb) - 0.6, 0]))
        self.play(FadeOut(unf), FadeIn(cost), run_time=0.3)
        move_x(self, b, xb, xb + 0.85, t=0.7, rate=rate_functions.ease_in_quad)
        move_x(self, b, xb + 0.85, xb + 0.45, t=0.35)
        move_x(self, b, xb + 0.45, xp, t=0.85, rate=smooth)
        lab = tag("first contacts", GOLD, 30, [xp + 1.55, prof(xp) + 0.75, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.4)
        self.at("once a core forms")
        l2 = tag("core forms", GREEN, 30, [-0.4, 1.35, 0])
        move_x(self, b, xp, xp + 0.3, t=0.35)
        self.play(FadeOut(lab), FadeOut(cost), FadeIn(l2, shift=DOWN * 0.1), run_time=0.4)
        self.at("the rest runs downhill")
        move_x(self, b, xp + 0.3, X0P, t=1.5, rate=rush_into)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        c = curve(False)
        ax = axes_group()
        nat = native_label()
        xs0 = -2.9
        b = ball(onc(xs0), 0.2)
        self.add(c, ax, nat, b)
        self.at("have dips")
        c2 = curve(True)
        self.play(Transform(c, c2), b.animate.move_to(onc(xs0, True)), run_time=0.9)
        self.at("kinetic traps")
        xm = xtrap()
        tl = tag("kinetic trap", RED, 32, [-0.5, -0.1, 0])
        ar = Arrow(tl.get_bottom(), [xm, prof(xm, True) + 0.5, 0], buff=0.08, color=RED, stroke_width=5, tip_length=0.22)
        self.play(FadeIn(tl), Create(ar), run_time=0.5)
        move_x(self, b, xs0, xm, trap=True, t=0.8, rate=rush_into)
        move_x(self, b, xm, xm + 0.25, trap=True, t=0.2)
        move_x(self, b, xm + 0.25, xm, trap=True, t=0.2)
        self.play(FadeOut(ar), run_time=0.2)
        self.at("chaperones stop half")
        ch1, ch2 = chap_chain(*C1), chap_chain(*C2)
        links = clump_links(3.5)
        cl = T("clump", size=30, color=RED).move_to([3.25, 2.55, 0])
        hl = T("half-folded chains", size=28, color=LIGHT).move_to([3.55, -0.25, 0])
        self.play(FadeIn(ch1), FadeIn(ch2), FadeIn(hl), run_time=0.5)
        self.play(ch2.animate.shift(LEFT * 0.6), run_time=0.7)
        self.play(FadeIn(links), FadeIn(cl), run_time=0.4)
        self.at("from clumping")
        cg = cage()
        cgl = tag("chaperone", ORANGE, 32, [C1[0], 3.3, 0])
        self.play(Create(cg), FadeIn(cgl), FadeOut(links), FadeOut(cl), run_time=0.8)
        self.play(ch2.animate.shift(RIGHT * 0.75), run_time=0.6)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        c = curve(True)
        ax = axes_group()
        nat = native_label()
        xm = xtrap()
        b = ball(onc(xm, True), 0.2)
        ch1, ch2 = chap_chain(*C1), chap_chain(*C2)
        ch2.shift(RIGHT * 0.15)
        cg = cage()
        cgl = tag("chaperone", ORANGE, 32, [C1[0], 3.3, 0])
        hl = T("half-folded chains", size=28, color=LIGHT).move_to([3.55, -0.25, 0])
        tl = tag("kinetic trap", RED, 32, [-0.5, -0.1, 0])
        grp = VGroup(cg, ch1, ch2, cgl, hl)
        self.add(c, ax, nat, b, grp, tl)
        self.at("do not choose the destination")
        self.play(grp.animate.set_opacity(0.2), run_time=0.7)
        xl = xlip()
        self.wait(0.2)
        move_x(self, b, xm, xm + 0.28, trap=True, t=0.3)
        move_x(self, b, xm + 0.28, xm - 0.2, trap=True, t=0.35)
        move_x(self, b, xm - 0.2, xm + 0.5, trap=True, t=0.4)
        move_x(self, b, xm + 0.5, xl, trap=True, t=0.35, extra=(FadeOut(tl),))
        move_x(self, b, xl, X0P, trap=True, t=1.0, rate=rush_into)
        self.at("in its environment")
        sl = T("the sequence chooses", size=40, color=GREEN).move_to([-3.2, 2.6, 0])
        self.play(FadeIn(sl, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S27(SpokenScene):
    def construct(self):
        cols = [PURPLE] * 15
        for i in (3, 8, 12):
            cols[i] = YELLOW
        mk = lambda i: beadchain(60 + i, n=15, w=9.4, h=3.4, colors=cols, cy=0.1, r=0.24)
        chain = mk(0)
        self.play(FadeIn(chain), run_time=0.3)
        flicker(chain, mk, period=0.45)
        lg = VGroup(Circle(radius=0.16, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.6), T("oily", size=26, color=YELLOW),
                    Circle(radius=0.16, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.6), T("polar", size=26, color=PURPLE))
        lg.arrange(RIGHT, buff=0.2)
        lg.move_to([-4.9, 3.45, 0])
        self.play(FadeIn(lg), run_time=0.3)
        self.at("disordered proteins")
        dl = tag("disordered region", PURPLE, 36, [0, -3.2, 0])
        self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.5)
        self.at("too few oily residues")
        yl = tag("few oily residues", YELLOW, 32, [-3.2, 2.85, 0])
        ld = always_redraw(lambda: Line(yl.get_bottom(), chain[1 + 8].get_center() + UP * 0.25, color=YELLOW, stroke_width=3))
        self.play(FadeIn(yl, shift=DOWN * 0.1), FadeIn(ld), run_time=0.5)
        self.at("pay for a core")
        dc = DashedVMobject(Circle(radius=1.3, color=RED, stroke_width=4)).move_to([0, 0.1, 0])
        nc = tag("no core forms", RED, 34, [3.4, 2.85, 0])
        self.play(Create(dc), FadeIn(nc, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


def coilchain(cx, cy, w=5.4):
    pts = []
    xs = np.linspace(-w / 2, w / 2, 220)
    for x in xs:
        u = (x + w / 2) / w
        if 0.12 < u < 0.42 or 0.58 < u < 0.88:
            y = 0.7 * np.sin(x * 9.0)
        else:
            y = 0.25 * np.sin(x * 3.0)
        pts.append(np.array([cx + x, cy + y, 0.0]))
    m = VMobject(stroke_color=BLUE, stroke_width=7)
    m.set_points_smoothly(pts)
    return m


def sheetchain(cx, cy, w=4.6, color=RED, sc=1.0):
    levels = [-1.3, -0.45, 0.45, 1.3]
    pts = []
    for i, y in enumerate(levels):
        xs = np.linspace(-w / 2, w / 2, 40)
        if i % 2:
            xs = xs[::-1]
        for x in xs:
            pts.append(np.array([cx + sc * x, cy + sc * y, 0.0]))
    pts = [p for j, p in enumerate(pts) if j == 0 or np.linalg.norm(p - pts[j - 1]) > 1e-6]
    m = VMobject(stroke_color=color, stroke_width=6)
    m.set_points_smoothly(pts)
    return m


def sheetbonds(cx, cy, w=4.6, sc=1.0):
    g = VGroup()
    for x in np.linspace(-w / 2 + 0.7, w / 2 - 0.7, 4):
        for ya, yb in [(-1.3, -0.45), (-0.45, 0.45), (0.45, 1.3)]:
            g.add(DashedLine([cx + sc * x, cy + sc * ya + 0.06, 0], [cx + sc * x, cy + sc * yb - 0.06, 0], color=ORANGE, stroke_width=3, dash_length=0.07))
    return g


class S28(SpokenScene):
    def construct(self):
        A = coilchain(-3.7, 0.4)
        self.at("prions take one sequence")
        la = T("normal: helix-rich", size=34, color=GREEN).move_to([-3.7, -1.55, 0])
        hx = T("helix", size=30, color=BLUE).move_to([-3.7, 1.55, 0])
        sq = tag("one sequence", GREY, 30, [-3.7, 2.8, 0])
        self.play(FadeIn(A), FadeIn(la), FadeIn(hx), FadeIn(sq), run_time=0.8)
        self.at("a second fold")
        sc = 0.5
        B = sheetchain(3.9, 0.3, sc=sc)
        ar = Arrow([-0.8, 0.3, 0], [1.6, 0.3, 0], buff=0, color=TEXT, stroke_width=6)
        sf = T("a second fold", size=30, color=RED).move_to([0.4, 0.95, 0])
        self.play(GrowArrow(ar), FadeIn(sf), FadeIn(B), run_time=0.9)
        self.at("rich in beta sheet")
        bd = sheetbonds(3.9, 0.3, sc=sc)
        lb = T("prion: sheet-rich", size=34, color=RED).move_to([3.9, -1.7, 0])
        self.play(Create(bd), FadeIn(lb), run_time=0.8)
        self.at("that aggregates")
        B2 = sheetchain(3.9, 2.0, sc=sc)
        B3 = sheetchain(3.9, -1.4, sc=sc)
        for x in (B2, B3):
            x.set_stroke(opacity=0.7)
        ag = tag("aggregates", RED, 34, [3.9, 3.35, 0])
        self.play(FadeIn(B2, shift=DOWN * 0.2), FadeIn(B3, shift=UP * 0.2), FadeIn(ag), lb.animate.move_to([3.9, -3.0, 0]), run_time=0.9)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        water = Rectangle(width=13.6, height=7.6, stroke_width=0, fill_color=TEAL, fill_opacity=0.14).set_z_index(0)
        wl = T("water", size=32, color=TEAL).move_to([-5.7, 3.2, 0])
        c = np.array([-1.0, 0.0, 0.0])
        prot = Circle(radius=2.3, stroke_color=BLUE, stroke_width=5, fill_color=BLUE, fill_opacity=0.14).move_to(c).set_z_index(3)
        outer = VGroup(*[Circle(radius=0.29, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.6)
                         .move_to(c + 2.3 * np.array([np.cos(a), np.sin(a), 0])) for a in np.linspace(0, 2 * np.pi, 10, endpoint=False) + 0.3]).set_z_index(4)
        inner = VGroup(*[Circle(radius=0.29, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.6)
                         .move_to(c + 1.0 * np.array([np.cos(a), np.sin(a), 0])) for a in np.linspace(0, 2 * np.pi, 5, endpoint=False) + 0.9]).set_z_index(4)
        lg = VGroup(VGroup(Circle(radius=0.17, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=0.6), T("greasy", size=28, color=YELLOW)).arrange(RIGHT, buff=0.2),
                    VGroup(Circle(radius=0.17, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.6), T("polar", size=28, color=PURPLE)).arrange(RIGHT, buff=0.2))
        lg.arrange(RIGHT, buff=0.6).move_to([4.4, 3.3, 0]).set_z_index(6)
        self.play(FadeIn(water), FadeIn(wl), FadeIn(prot), FadeIn(outer), FadeIn(inner), FadeIn(lg), run_time=0.9)
        self.at("sit in lipid")
        band = Rectangle(width=13.6, height=5.2, stroke_color=YELLOW, stroke_width=3, fill_color=BG, fill_opacity=1.0).set_z_index(1)
        tint = Rectangle(width=13.6, height=5.2, stroke_width=0, fill_color=YELLOW, fill_opacity=0.14).set_z_index(2)
        ll = T("lipid", size=36, color=YELLOW).move_to([-5.8, 0, 0]).set_z_index(5)
        wl2 = T("water", size=32, color=TEAL).move_to([-5.7, -3.2, 0])
        self.play(FadeIn(band), FadeIn(tint), FadeIn(ll), FadeIn(wl2), run_time=0.9)
        self.at("their surface flips")
        self.play(*[o.animate.set_color(YELLOW).set_fill(YELLOW, 0.6) for o in outer],
                  *[i.animate.set_color(PURPLE).set_fill(PURPLE, 0.6) for i in inner], run_time=1.2)
        self.at("greasy residues face")
        gt = tag("greasy residues\nface the lipid", TEXT, 34, [3.9, -0.3, 0])
        gt[1].set_color(YELLOW)
        ga = Arrow(gt.get_left(), outer[0].get_center() + RIGHT * 0.4, buff=0.1, color=YELLOW, stroke_width=5).set_z_index(9)
        self.play(FadeIn(gt), Create(ga), run_time=0.7)
        self.finish()


class S30(SpokenScene):
    def construct(self):
        f = FUN.make(1.0, P_FUN)
        b = ball(WL(1.0), 0.2)
        self.add(f, b)
        self.at("folding is downhill")
        t1 = T("Folding is downhill,", size=48, font=TITLE_FONT)
        t1b = T("not random", size=48, font=TITLE_FONT, color=RED)
        VGroup(t1, t1b).arrange(RIGHT, buff=0.3).move_to([0, 3.4, 0])
        t1b.set_opacity(0)
        self.add(t1b)
        self.play(FadeIn(t1), run_time=0.4)
        rollw(self, b, 1.0, 0.5, t=1.0, rate=linear)
        self.at("not random")
        t2 = T("native-like contacts tilt the landscape toward the fold", size=32, color=GREEN).move_to([0, -3.4, 0])
        self.play(t1b.animate.set_opacity(1), run_time=0.3)
        rollw(self, b, 0.5, 0.07, t=1.1, rate=rush_into)
        self.at("native like contacts")
        self.play(FadeIn(t2, shift=UP * 0.1), Indicate(f[-1], color=GREEN, scale_factor=1.5), run_time=0.8)
        self.finish()


class S31End(EndCard):
    LINE = "Folding is downhill, not random: native-like contacts tilt the landscape."

    def construct(self):
        a = T("Folding is downhill, not random:", size=48, font=TITLE_FONT)
        b = T("native-like contacts tilt the landscape.", size=48, font=TITLE_FONT, color=GREEN)
        sub = T("biochemistrypedia.com", size=26, color=TEAL)
        g = VGroup(a, b).arrange(DOWN, buff=0.3)
        VGroup(g, sub).arrange(DOWN, buff=0.6)
        self.play(FadeIn(a, shift=UP * 0.15), run_time=self.beat(0.2))
        self.play(FadeIn(b, shift=UP * 0.15), run_time=self.beat(0.2))
        self.play(FadeIn(sub), run_time=self.beat(0.1))
        self.finish()
