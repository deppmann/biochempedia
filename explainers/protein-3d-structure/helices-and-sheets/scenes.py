# COLOR MAP (shared with the other chapters of this lesson; one color per concept)
#   BLUE    the protein / polypeptide chain / backbone, strands and helices
#   ORANGE  backbone geometry constraints: phi/psi, the Ramachandran plot, residues-per-turn counter;
#           also the C=O groups of the backbone (chips and dots)
#   YELLOW  nonpolar side chains (not used in this chapter)
#   PURPLE  polar residues (here only the second strand in the "far apart" scene, and chain B of collagen)
#   TEAL    water (not used here) and the interactive cue on cards; here also the N-H groups of the backbone
#           and the first strand in the "far apart" scene
#   GREEN   allowed / surviving (the Ramachandran islands), "helix intact"
#   RED     forbidden, broken, disease (clash flash, lost hydrogen bond, brittle bone)
#   GOLD    proline and its ring (this chapter's rule-breaker), also hydroxyproline
#   TEXT    hydrogen bonds (dashed white lines), glycine, "secondary structure" highlights
#   GREY    labels, frames, structure, bonds with no partner
# NOTHING here draws a molecular structure: chains are smooth curves, residues are beads,
# C=O / N-H are text chips, proline is a labelled loop, and the Ramachandran plot is computed.
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CE0"
LIGHT = "#C9CED8"
C2 = "#9ADBEE"
C3 = "#2F86A8"

ANG = np.radians(100.0)                      # 3.6 residues per turn
HX0, HY, HR, HRISE, HN = -5.4, -0.1, 2.5, 1.3, 9
NHB = 5                                      # hydrogen bonds i -> i+4 in a 9-residue helix: i = 0..4
GL = 0.42                                    # C=O dot sits this far ahead of the bead, N-H dot this far behind


# ------------------------------------------------------------------ helpers
def tag(txt, color=TEXT, size=28, pos=None):
    t = T(txt, size=size, color=color)
    bk = Rectangle(width=t.width + 0.24, height=t.height + 0.16, stroke_width=0, fill_color=BG, fill_opacity=0.85).move_to(t)
    g = VGroup(bk, t)
    if pos is not None:
        g.move_to(pos)
    return g.set_z_index(8)


def greek(g, rest="", size=48, color=BLUE):
    """A Greek letter in the mono font (the body font draws alpha like a Latin a), then the rest of the label."""
    a = M(g, size=size, color=color, weight=BOLD)
    if not rest:
        return a
    r = T(rest, size=size, color=color)
    return VGroup(a, r).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)


def ahelix(size=52):
    return greek("α", "helix", size=size)


def hb(a, b, color=TEXT, w=4.0, trim=0.0, dash=0.12):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    d = b - a
    u = d / max(np.linalg.norm(d), 1e-6)
    return DashedLine(a + u * trim, b - u * trim, dash_length=dash, dashed_ratio=0.55, color=color, stroke_width=w)


def pro_dot(pos, r=0.36, size=24):
    c = Circle(radius=r, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.95)
    t = T("Pro", size=size, color=BG, weight=BOLD)
    return VGroup(c, t).move_to(pos).set_z_index(7)


def tip(p, direction, color=TEXT, size=0.34):
    a = np.arctan2(direction[1], direction[0])
    return Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(size).rotate(a - PI / 2).move_to(p).set_z_index(9)


def cross(c, s=0.3, color=RED, w=7):
    c = np.array(c, dtype=float)
    return VGroup(Line(c + UL * s, c + DR * s, color=color, stroke_width=w), Line(c + UR * s, c + DL * s, color=color, stroke_width=w)).set_z_index(9)


class Hx:
    """Side-on right-handed helix: the axis is horizontal, 100 degrees per residue.
    Front strands (towards the viewer) run down to the right, back strands up to the right, so the front is bold."""

    def __init__(s, x0=HX0, y0=HY, R=HR, rise=HRISE, N=HN, shear=0.0, kink=0.0, kink_at=4.0):
        s.x0, s.y0, s.R, s.rise, s.N, s.shear, s.kink, s.kink_at = x0, y0, R, rise, N, shear, kink, kink_at

    def raw(s, t):
        return np.array([s.x0 + s.rise * t + s.shear * s.R * np.sin(ANG * t), s.y0 + s.R * np.cos(ANG * t), 0.0])

    def P(s, t):
        p = s.raw(t)
        if s.kink and t > s.kink_at:
            c = np.array([s.x0 + s.rise * s.kink_at, s.y0, 0.0])
            a = s.kink * min(1.0, (t - s.kink_at) / 0.8)
            d = p - c
            ca, sa = np.cos(a), np.sin(a)
            p = c + np.array([ca * d[0] - sa * d[1], sa * d[0] + ca * d[1], 0.0])
        return p

    def guides(s):
        xa, xb = s.x0 - 0.3, s.x0 + s.rise * (s.N - 1) + 0.3
        return VGroup(*[DashedLine([xa, s.y0 + sg * s.R, 0], [xb, s.y0 + sg * s.R, 0], dash_length=0.2, color=GREY, stroke_width=2)
                        .set_opacity(0.35).set_z_index(0) for sg in (1, -1)])

    def front(s, i):
        return np.sin(ANG * i) >= -1e-9

    def chain(s, w=11, color=BLUE):
        segs = VGroup()
        k = 0
        while 1.8 * k < s.N - 1 - 1e-6:
            t0, t1 = 1.8 * k, min(1.8 * (k + 1), s.N - 1)
            fr = (k % 2 == 0)
            f = ParametricFunction(lambda t: s.P(t), t_range=[t0, t1, 0.04], color=color, stroke_width=w if fr else w * 0.3)
            f.set_stroke(opacity=1.0 if fr else 0.28)
            f.set_z_index(3 if fr else 1)
            segs.add(f)
            k += 1
        return segs

    def bead(s, i, numbers=True, r=0.29):
        fr = s.front(i)
        c = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=1.0 if fr else 0.35)
        g = VGroup(c)
        if numbers:
            g.add(T(str(i + 1), size=26, color=BG, weight=BOLD).move_to(c))
        g.move_to(s.P(i)).set_z_index(5 if fr else 2)
        return g

    def co(s, i):
        return s.P(i) + RIGHT * GL

    def nh(s, i):
        return s.P(i) + LEFT * GL

    def dots(s, i, nh=True):
        fr = s.front(i)
        o = 1.0 if fr else 0.35
        g = VGroup(Dot(s.co(i), radius=0.1, color=ORANGE).set_opacity(o))
        if nh:
            g.add(Dot(s.nh(i), radius=0.1, color=TEAL).set_opacity(o))
        return g.set_z_index(6)

    def line(s, i, color=TEXT, w=2.5):
        return hb(s.co(i), s.nh(i + 4), color=color, w=w, trim=0.08).set_stroke(opacity=0.4)

    def stub(s, i):
        p = s.P(i)
        sg = 1 if np.cos(ANG * i) >= 0 else -1
        fr = s.front(i)
        e = p + np.array([0.12, sg * 0.78, 0.0])
        st = p + np.array([0.03, sg * 0.28, 0.0])
        g = VGroup(Line(st, e, color=LIGHT, stroke_width=11), Dot(e, radius=0.19, color=LIGHT))
        g.set_opacity(1.0 if fr else 0.5)
        return g.set_z_index(4)


class HView:
    """Chain, numbered beads, C=O / N-H dots and i -> i+4 lines of one helix."""

    def __init__(s, hx, pros=(), skip=(), nlines=NHB, numbers=True):
        s.hx = hx
        s.chain = hx.chain()
        s.guides = hx.guides()
        s.beads = {i: (pro_dot(hx.P(i)) if i in pros else hx.bead(i, numbers)) for i in range(hx.N)}
        s.dots = {i: hx.dots(i, nh=(i not in pros)) for i in range(hx.N)}
        s.lines = {i: hx.line(i) for i in range(nlines) if i not in skip}

    def group(s, beads=True, dots=True, lines=True):
        g = VGroup(s.guides, s.chain)
        if beads:
            g.add(*s.beads.values())
        if dots:
            g.add(*s.dots.values())
        if lines:
            g.add(*s.lines.values())
        return g


def first_turn_rect(hx):
    pts = [hx.P(i) for i in range(4)]
    x0, x1 = min(p[0] for p in pts) - 0.6, max(p[0] for p in pts) + 0.6
    y0, y1 = min(p[1] for p in pts) - 0.5, max(p[1] for p in pts) + 0.5
    return RoundedRectangle(corner_radius=0.2, width=x1 - x0, height=y1 - y0, stroke_color=LIGHT, stroke_width=4) \
        .move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0]).set_z_index(1)


def strip(n, x0, step, y, side=0.5, color=BLUE, fill=0.25, numbers=False, ts=26):
    cells = VGroup()
    for i in range(n):
        sq = Square(side, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill).move_to([x0 + step * i, y, 0])
        if numbers:
            cells.add(VGroup(sq, T(str(i + 1), size=ts, color=TEXT).move_to(sq)))
        else:
            cells.add(sq)
    return cells


def cell_sq(c):
    return c[0] if isinstance(c, VGroup) else c


# ---- Ramachandran plot (computed, same model as the earlier film; the three islands the lesson names) ----
def _ell(phi, psi, c, a, b):
    return ((phi - c[0]) / a) ** 2 + ((psi - c[1]) / b) ** 2 <= 1


def allowed(phi, psi):
    return (_ell(phi, psi, (-120, 130), 62, 52) or _ell(phi, psi, (-62, -42), 32, 28) or _ell(phi, psi, (58, 45), 24, 32))


_MASK = {}


def mask_image(px=420):
    if px in _MASK:
        return _MASK[px]
    cc, rr = np.meshgrid(np.arange(px), np.arange(px))
    phi = -180 + (cc + 0.5) * 360 / px
    psi = 180 - (rr + 0.5) * 360 / px
    ok = (_ell(phi, psi, (-120, 130), 62, 52) | _ell(phi, psi, (-62, -42), 32, 28) | _ell(phi, psi, (58, 45), 24, 32))
    arr = np.zeros((px, px, 4), dtype=np.uint8)
    arr[ok] = np.array([0x83, 0xC1, 0x67, 150], dtype=np.uint8)
    _MASK[px] = arr
    return arr


def c2p(cx, cy, W, phi, psi):
    return np.array([cx + phi / 360 * W, cy + psi / 360 * W, 0.0])


RX, RY, RW = -1.9, 0.25, 6.2          # position and size of the Ramachandran plot in the three plot scenes


def rama(cx=RX, cy=RY, W=RW):
    frame = Square(W, color=GREY, stroke_width=3).move_to([cx, cy, 0])
    hl = Line(frame.get_left(), frame.get_right(), color=GREY, stroke_width=1.5).set_opacity(0.5)
    vl = Line(frame.get_bottom(), frame.get_top(), color=GREY, stroke_width=1.5).set_opacity(0.5)
    xt = VGroup(*[M(v, size=26, color=GREY).next_to(frame.get_bottom() + RIGHT * dx, DOWN, buff=0.12)
                  for v, dx in (("-180°", -W / 2 + 0.45), ("0°", 0), ("180°", W / 2 - 0.4))])
    yt = VGroup(*[M(v, size=26, color=GREY).next_to(frame.get_left() + UP * dy, LEFT, buff=0.12)
                  for v, dy in (("180°", W / 2 - 0.2), ("0°", 0), ("-180°", -W / 2 + 0.2))])
    xa = M("φ", size=40, color=ORANGE).next_to(frame.get_corner(DR), RIGHT, buff=0.3).set_y(xt.get_y())
    ya = M("ψ", size=40, color=ORANGE).next_to(yt, LEFT, buff=0.15).set_y(cy)
    img = ImageMobject(mask_image()).set_height(W).move_to([cx, cy, 0]).set_z_index(2)
    return VGroup(frame, hl, vl, xt, yt, xa, ya), img


def island_labels(cx=RX, cy=RY, W=RW, alpha=True):
    b = greek("β", "", size=40, color=TEXT).move_to(c2p(cx, cy, W, -120, 130))
    a = greek("α", "", size=40, color=TEXT).move_to(c2p(cx, cy, W, -62, -42))
    l = T("left-handed", size=26, color=TEXT).move_to(c2p(cx, cy, W, 58, 45) + DOWN * 0.95)
    return (VGroup(b, a, l) if alpha else VGroup(b, l)).set_z_index(6)


# ---- sheet pieces ----
SXS = np.linspace(-4.6, 4.6, 9)
YA, YB = 1.55, -1.55
AMP = 0.4


def zig(y, xs=SXS, amp=AMP, color=BLUE, d=1, w=12, head=0.7, hw=0.5):
    pts = [[x, y + (amp if i % 2 == 0 else -amp), 0] for i, x in enumerate(xs)]
    line = VMobject(stroke_color=color, stroke_width=w).set_points_as_corners(pts)
    hd = make_head(xs, y, amp, color, d, head, hw, len(xs))
    return line, hd


def make_head(xs, y, amp, color, d, head=0.7, hw=0.5, n=9):
    if d > 0:
        xv = xs[-1]
        yv = y + (amp if (n - 1) % 2 == 0 else -amp)
        pts = [[xv, yv + hw, 0], [xv + head, yv, 0], [xv, yv - hw, 0]]
    else:
        xv = xs[0]
        yv = y + amp
        pts = [[xv, yv + hw, 0], [xv - head, yv, 0], [xv, yv - hw, 0]]
    return Polygon(*pts, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=1).set_z_index(4)


def sheet_stubs(y, xs=SXS, amp=AMP, ln=0.75):
    out = VGroup()
    for i, x in enumerate(xs):
        up = (i % 2 == 0)
        p = np.array([x, y + (amp if up else -amp), 0.0])
        e = p + np.array([0.0, ln if up else -ln, 0.0])
        out.add(VGroup(Line(p, e, color=LIGHT, stroke_width=7), Dot(e, radius=0.13, color=LIGHT)))
    return out


def sheet_hbonds(yA, yB, xs=SXS, amp=AMP):
    out = VGroup()
    for i in range(len(xs) - 1):
        xm = (xs[i] + xs[i + 1]) / 2
        out.add(hb([xm, yA - 0.05, 0], [xm, yB + 0.05, 0], w=4))
    return out


def sheet_base(colA=BLUE, colB=BLUE, flipB=False):
    lA, hA = zig(YA, color=colA)
    lB, hB = zig(YB, color=colB, d=-1 if flipB else 1)
    return lA, hA, lB, hB


def nc_labels(flipB=False):
    nA = T("N", size=40, color=LIGHT).move_to([-5.75, YA, 0])
    cA = T("C", size=40, color=LIGHT).move_to([6.15, YA, 0])
    nB = T("N", size=40, color=LIGHT).move_to([6.15 if flipB else -5.75, YB, 0])
    cB = T("C", size=40, color=LIGHT).move_to([-5.75 if flipB else 6.15, YB, 0])
    return nA, cA, nB, cB


# ---- collagen pieces ----
STRAND_COLS = (BLUE, PURPLE, ORANGE)
SY = (1.75, -0.1, -1.95)


def spring(x0, x1, cy, R, pitch, color, hand=-1, w=7, b=0.62):
    """a loosely coiled strand drawn side-on: bold front, faint back, curled like a spring (left-handed for hand=-1)"""
    a = pitch / (2 * PI)
    top = (x1 - x0) / a
    g = VGroup()
    k = 0
    ph = 0.0
    while ph < top - 1e-6:
        ph1 = min(ph + PI, top)
        mid = (ph + ph1) / 2
        fr = np.sin(hand * mid) > 0
        seg = ParametricFunction(lambda t: np.array([x0 + a * t + b * np.sin(hand * t), cy + R * np.cos(hand * t), 0.0]),
                                 t_range=[ph, ph1, 0.04], color=color, stroke_width=w if fr else w * 0.55)
        seg.set_stroke(opacity=1.0 if fr else 0.45).set_z_index(3 if fr else 1)
        g.add(seg)
        ph = ph1
        k += 1
    return g


SBW, SAMP, SLAM = 6.0, 1.3, 3.4


def braid(cx, cy, w, amp, lam, bulge=0.0, cols=STRAND_COLS, sw=9):
    """three strands wound round each other (side view): bold front half-turns, faint back half-turns"""
    out = VGroup()
    k_per = w / (lam / 2)
    for k in range(3):
        ph = 2 * PI * k / 3
        g = VGroup()
        n = int(np.ceil(k_per))
        for j in range(n):
            u0 = j * lam / 2 - w / 2
            u1 = min(u0 + lam / 2, w / 2)
            mid = (u0 + u1) / 2
            fr = np.sin(2 * PI * mid / lam + ph) > 0

            def f(x, ph=ph):
                a = amp * (1 + bulge * np.exp(-x * x / (0.05 * w * w)))
                th = 2 * PI * x / lam + ph
                return np.array([cx + x + 0.3 * amp * np.sin(th + PI / 2), cy + a * np.cos(th), 0.0])
            seg = ParametricFunction(f, t_range=[u0, u1, 0.04], color=cols[k], stroke_width=sw if fr else sw * 0.4)
            seg.set_stroke(opacity=1.0 if fr else 0.35).set_z_index(3 if fr else 1)
            g.add(seg)
        out.add(g)
    return out


ER = 1.35                      # radius of one chain in the end-on view
EX, EY = 3.1, -0.65            # centre of the end-on view
BX = -3.8                      # centre of the side-view braid once it moves left


def endon(cx, cy, spread=1.8, r=ER):
    circles = VGroup()
    for k in range(3):
        a = PI / 2 + 2 * PI * k / 3
        c = Circle(radius=r, stroke_color=STRAND_COLS[k], stroke_width=6, fill_color=STRAND_COLS[k], fill_opacity=0.22)
        c.move_to([cx + spread * np.cos(a), cy + spread * np.sin(a), 0])
        circles.add(c)
    return circles


def slot(cx, cy, r=0.42):
    return DashedVMobject(Circle(radius=r, color=TEXT, stroke_width=4), num_dashes=16).move_to([cx, cy, 0]).set_z_index(6)


def inward_arrows(cx, cy, r0=1.55, r1=0.62):
    arrows = VGroup()
    for k in range(3):
        a = PI / 2 + 2 * PI * k / 3
        st = np.array([cx + r0 * np.cos(a), cy + r0 * np.sin(a), 0])
        en = np.array([cx + r1 * np.cos(a), cy + r1 * np.sin(a), 0])
        arrows.add(Arrow(st, en, buff=0, color=TEXT, stroke_width=9, max_tip_length_to_length_ratio=0.45,
                         max_stroke_width_to_length_ratio=12).set_z_index(7))
    return arrows


# ------------------------------------------------------------------ scenes
class S00Title(TitleCard):
    LESSON = "Protein Three-Dimensional Structure"
    TITLE = "Helices, Sheets and the Rule-Breakers"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), FadeIn(title, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(GrowFromCenter(rule), run_time=self.beat(0.25))
        self.wait(self.beat(0.3))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


class S01(SpokenScene):
    def construct(self):
        ax, img = rama()
        labs = island_labels()
        self.play(FadeIn(ax), run_time=0.6)
        self.at("islands")
        self.play(FadeIn(img), FadeIn(labs), run_time=0.9)
        bx = 4.0
        boxes, arrows = VGroup(), VGroup()
        for (phi, psi, by) in ((-120, 130, 2.5), (58, 45, 1.0), (-62, -42, -0.5)):
            box = VGroup(RoundedRectangle(corner_radius=0.15, width=1.4, height=1.1, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.12), T("?", size=56, color=GREY))
            box[1].move_to(box[0])
            box.move_to([bx, by, 0])
            edge = {-120: -58, 58: 82, -62: -30}[phi]
            st = c2p(RX, RY, RW, edge, psi) + RIGHT * 0.1
            st[1] = by
            ar = Arrow(st, box.get_left() + LEFT * 0.05, buff=0.05, color=ORANGE, stroke_width=5, max_tip_length_to_length_ratio=0.12)
            boxes.add(box)
            arrows.add(ar)
        self.at("why do")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), FadeIn(boxes, shift=LEFT * 0.2), run_time=0.8)
        q = VGroup(T("Why do the islands", size=34), T("become helices and sheets?", size=34)).arrange(DOWN, buff=0.15).move_to([3.95, -1.9, 0])
        self.at("helices and sheets")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        ax, img = rama()
        labs = island_labels()
        self.add(ax, img, labs)
        ringA = Ellipse(width=2 * 32 / 360 * RW + 0.35, height=2 * 28 / 360 * RW + 0.35, color=YELLOW, stroke_width=6) \
            .move_to(c2p(RX, RY, RW, -62, -42)).set_z_index(6)
        ringB = Ellipse(width=2 * 62 / 360 * RW + 0.35, height=2 * 52 / 360 * RW + 0.35, color=YELLOW, stroke_width=6) \
            .move_to(c2p(RX, RY, RW, -120, 130)).set_z_index(6)
        self.at("each island")
        self.play(Create(ringA), Create(ringB), run_time=0.7)
        hx = Hx()
        chain = hx.chain()
        self.at("regular shape")
        self.play(FadeOut(ax), FadeOut(img), FadeOut(labs), FadeOut(ringB), ReplacementTransform(ringA, chain), run_time=1.2)
        v = HView(hx)
        self.at("that shape lets")
        self.play(LaggedStart(*[FadeIn(b) for b in v.beads.values()], *[FadeIn(d) for d in v.dots.values()], lag_ratio=0.08), run_time=0.9)
        lab = tag("hydrogen bonds", TEXT, 40, [-0.2, 3.3, 0])
        self.at("hydrogen bond")
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.4)
        self.play(LaggedStart(*[Create(l) for l in v.lines.values()], lag_ratio=0.2), run_time=1.2)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        yA, yB = 2.5, -2.5
        topbar = Line([-4.8, yA, 0], [3.0, yA, 0], color=BLUE, stroke_width=12)
        botbar = Line([-4.8, yB, 0], [3.0, yB, 0], color=BLUE, stroke_width=12)
        bt = T("backbone", size=34, color=LIGHT).move_to([4.7, yA, 0])
        bb = T("backbone", size=34, color=LIGHT).move_to([4.7, yB, 0])
        xc = -0.9
        co = chip("C=O", ORANGE, size=46).move_to([xc, yA - 1.3, 0])
        nh = chip("N–H", TEAL, size=46).move_to([xc, yB + 1.3, 0])
        stem1 = Line([xc, yA, 0], co.get_top(), color=BLUE, stroke_width=7)
        stem2 = Line([xc, yB, 0], nh.get_bottom(), color=BLUE, stroke_width=7)
        self.play(Create(topbar), Create(botbar), FadeIn(bt), FadeIn(bb), run_time=0.8)
        self.at("c o")
        self.play(Create(stem1), FadeIn(co, scale=1.3), run_time=0.5)
        self.at("n h")
        self.play(Create(stem2), FadeIn(nh, scale=1.3), run_time=0.5)
        bond = hb(co.get_bottom(), nh.get_top(), color=TEXT, w=6, trim=0.05, dash=0.16)
        self.play(Create(bond), run_time=0.7)
        bl = T("hydrogen bond", size=38, color=TEXT).move_to([xc + 2.6, 0, 0])
        self.play(FadeIn(bl), run_time=0.4)
        sec = chip("secondary structure", TEXT, size=44).move_to([0, -3.4, 0])
        self.at("shapes built this way")
        self.play(Indicate(bond, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("secondary structure")
        self.play(FadeIn(sec, shift=UP * 0.2), run_time=0.6)
        self.finish()


class S04(SpokenScene):
    def chain_mob(self):
        L = [[x, 0.95 * np.sin(0.9 * (x + 2.0)), 0] for x in np.linspace(-6.4, -2.4, 40)]
        coil = [[-2.2 + 4.4 * u + 0.45 * (np.cos(2 * PI * 4 * u) - 1), 1.55 * np.sin(2 * PI * 4 * u), 0] for u in np.linspace(0, 1, 140)]
        Rr = [[x, 0.95 * np.sin(0.9 * (x - 2.0)), 0] for x in np.linspace(2.4, 6.4, 40)]
        m = VMobject(stroke_color=BLUE, stroke_width=8)
        m.set_points_smoothly([np.array(p) for p in L + coil + Rr])
        return m

    def construct(self):
        ch = self.chain_mob().shift(UP * 0.5)
        self.play(Create(ch), run_time=0.8)
        box = RoundedRectangle(corner_radius=0.25, width=5.4, height=4.2, stroke_color=TEXT, stroke_width=6,
                               fill_color=TEXT, fill_opacity=0.08).move_to([0.0, 0.5, 0])
        self.play(Create(box), run_time=0.6)
        lab = T("local", size=58, color=TEXT).move_to([0, 3.35, 0])
        self.at("local")
        self.play(FadeIn(lab, shift=DOWN * 0.15), run_time=0.5)
        self.at("stretch of chain")
        self.play(Indicate(box, color=TEXT, scale_factor=1.04), run_time=0.7)
        by = -2.2
        br = Line([-6.4, by, 0], [6.4, by, 0], color=LIGHT, stroke_width=5)
        t1 = Line([-6.4, by - 0.2, 0], [-6.4, by + 0.2, 0], color=LIGHT, stroke_width=5)
        t2 = Line([6.4, by - 0.2, 0], [6.4, by + 0.2, 0], color=LIGHT, stroke_width=5)
        wl = T("the whole protein", size=42, color=TEXT).move_to([0, by - 0.7, 0])
        self.at("whole protein")
        self.play(Create(br), Create(t1), Create(t2), FadeIn(wl, shift=UP * 0.1), run_time=0.7)
        self.finish()


TITLE_POS = np.array([4.9, 3.4, 0.0])


def turn_arrow(hx, t0=3.5, t1=5.4, off=0.7, color=ORANGE):
    f = lambda t: hx.P(t) + RIGHT * off
    line = ParametricFunction(f, t_range=[t0, t1 - 0.08, 0.03], color=color, stroke_width=11).set_z_index(9)
    d = f(t1) - f(t1 - 0.12)
    return VGroup(line, tip(f(t1), d, color, 0.45))


class S05(SpokenScene):
    def construct(self):
        hx = Hx()
        chain = hx.chain()
        lab = ahelix(52).move_to(TITLE_POS)
        self.add(hx.guides())
        self.play(AnimationGroup(LaggedStart(*[Create(s_) for s_ in chain], lag_ratio=0.8, run_time=2.3),
                                 Succession(Wait(0.9), FadeIn(lab, shift=DOWN * 0.1, run_time=0.4))))
        self.at("right handed")
        arr = turn_arrow(hx)
        rh = VGroup(T("right-handed: front turn runs down-right", size=38, color=ORANGE)).move_to([-0.4, -3.4, 0])
        self.play(Create(arr[0]), FadeIn(arr[1]), FadeIn(rh, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        hx = Hx()
        v = HView(hx, nlines=0)
        lab = ahelix(52).move_to(TITLE_POS)
        self.add(v.chain, lab)
        self.at("it has")
        self.play(LaggedStart(*[FadeIn(v.beads[i], scale=1.5) for i in range(hx.N)], lag_ratio=0.08), run_time=0.9)
        xa, xb = hx.P(0)[0], hx.P(3.6)[0]
        yb = 2.85
        br = VGroup(Line([xa, yb, 0], [xb, yb, 0], color=ORANGE, stroke_width=6),
                    Line([xa, yb, 0], [xa, yb - 0.4, 0], color=ORANGE, stroke_width=6),
                    Line([xb, yb, 0], [xb, yb - 0.4, 0], color=ORANGE, stroke_width=6))
        self.at("over three")
        tr = ValueTracker(0.0)
        num = always_redraw(lambda: M(f"{tr.get_value():.1f}", size=62, color=ORANGE).move_to([-5.2, 3.45, 0]))
        unit = T("residues per turn", size=38, color=ORANGE).move_to([-2.2, 3.4, 0])
        rings = [Circle(radius=0.42, stroke_color=ORANGE, stroke_width=6).move_to(hx.P(i)).set_z_index(8) for i in range(4)]
        self.add(num)
        self.play(Create(br), tr.animate.set_value(3.6), LaggedStart(*[Create(r) for r in rings], lag_ratio=0.25), run_time=1.0, rate_func=smooth)
        self.at("residues per turn")
        self.play(FadeIn(unit, shift=LEFT * 0.1), run_time=0.4)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        hx = Hx()
        v = HView(hx, nlines=0)
        lab = ahelix(52).move_to(TITLE_POS)
        self.add(v.group(lines=False), lab)
        lines = [hx.line(i) for i in range(NHB)]
        p0, p4 = hx.P(0), hx.P(4)
        c_o = chip("i · C=O", ORANGE, size=32).move_to(p0 + np.array([0.5, 1.0, 0])).set_z_index(9)
        n_h = chip("i+4 · N–H", TEAL, size=32).move_to(p4 + np.array([-0.2, 1.3, 0])).set_z_index(9)
        l0 = Line(c_o.get_bottom(), hx.co(0), color=ORANGE, stroke_width=4)
        l4 = Line(n_h.get_bottom(), hx.nh(4), color=TEAL, stroke_width=4)
        main = lines[0].set_stroke(width=8)
        self.at("each")
        self.play(FadeIn(c_o, scale=1.2), Create(l0), run_time=0.5)
        self.at("bonds to")
        self.play(Create(main), run_time=0.5)
        self.at("nh")
        self.play(FadeIn(n_h, scale=1.2), Create(l4), run_time=0.5)
        for i in range(1, NHB):
            lines[i].set_stroke(opacity=0.3, width=2.5)
        self.at("residues ahead")
        self.play(LaggedStart(*[Create(l) for l in lines[1:]], lag_ratio=0.45), run_time=1.1)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        hx = Hx()
        v = HView(hx)
        lab = ahelix(52).move_to(TITLE_POS)
        self.add(v.group(), lab)
        rect = first_turn_rect(hx)
        self.at("first turn")
        self.play(Create(rect), run_time=0.6)
        rings = VGroup(*[Circle(radius=0.2, stroke_color=LIGHT, stroke_width=4).move_to(hx.nh(i)).set_z_index(8) for i in range(4)])
        ghosts = VGroup()
        for i in range(4):
            a = hx.nh(i) + LEFT * 0.2
            ghosts.add(DashedLine(a, a + LEFT * 0.85, dash_length=0.12, color=LIGHT, stroke_width=4).set_z_index(8))
            ghosts.add(tip(a + LEFT * 0.9, LEFT, LIGHT, 0.2))
        nl = tag("N–H groups: no partner four residues back", LIGHT, 34, [0, -3.45, 0])
        self.at("nh")
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=0.7)
        self.at("no partner")
        self.play(LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.1), FadeIn(nl), run_time=0.9)
        stubs = [hx.stub(i) for i in range(hx.N)]
        sl = tag("side chains", TEXT, 44, [-2.6, 3.4, 0])
        self.at("side chains")
        self.play(FadeOut(nl), FadeOut(rings), FadeOut(ghosts), FadeOut(rect),
                  LaggedStart(*[GrowFromPoint(s, s[0].get_start()) for s in stubs], lag_ratio=0.1), FadeIn(sl), run_time=1.3)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        hx = Hx()
        v = HView(hx)
        lab = ahelix(52).move_to(TITLE_POS)
        stubs = VGroup(*[hx.stub(i) for i in range(hx.N)])
        helix = VGroup(v.group(), stubs)
        self.add(helix, lab)
        sc, dy = 0.82, 1.15
        pivot = np.array([0.0, HY, 0.0])
        n = hx.N
        step = 1.0
        x0 = -(n - 1) * step / 2
        sy = -2.55
        cells = strip(n, x0, step, sy, side=0.58, numbers=True)
        scale_pt = lambda p: np.array([sc * p[0], HY + sc * (p[1] - HY) + dy, 0])
        hl = (0, 4, 8)
        lab2 = ahelix(48).move_to([5.0, 3.4, 0])
        self.add(lab2)
        self.play(helix.animate.scale(sc, about_point=pivot).shift(UP * dy), FadeOut(lab), FadeIn(cells, shift=UP * 0.2), run_time=0.6)
        ringsb = [Circle(radius=0.28, stroke_color=TEXT, stroke_width=5).move_to(scale_pt(hx.P(i))).set_z_index(8) for i in hl]
        arcs = VGroup(*[ArcBetweenPoints(cells[i].get_bottom(), cells[i + 4].get_bottom(), angle=PI / 4, color=TEXT, stroke_width=5)
                        for i in (0, 4)])
        self.at("the partners")
        self.play(*[cell_sq(cells[i]).animate.set_stroke(TEXT).set_fill(TEXT, 0.35) for i in hl], *[Create(r) for r in ringsb],
                  LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.4), run_time=1.0)
        nl = T("partners are near in sequence", size=38, color=TEXT).move_to([0, -3.65, 0])
        self.at("near each other")
        self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------ the sheet
class S10(SpokenScene):
    def construct(self):
        lA, hA, lB, hB = sheet_base()
        nA, cA, nB, cB = nc_labels()
        self.at("second")
        self.play(Create(lA), FadeIn(hA), run_time=0.7)
        self.at("beta sheet")
        self.play(Create(lB), FadeIn(hB), run_time=0.7)
        lab = greek("β", "strands", size=52, color=BLUE).move_to([0, 3.4, 0])
        self.at("its strands")
        self.play(FadeIn(lab, shift=DOWN * 0.1), *[FadeIn(x) for x in (nA, cA, nB, cB)], run_time=0.5)
        gA = DashedLine([-5.4, YA, 0], [5.4, YA, 0], color=GREY, stroke_width=3, dash_length=0.15).set_z_index(0)
        gB = DashedLine([-5.4, YB, 0], [5.4, YB, 0], color=GREY, stroke_width=3, dash_length=0.15).set_z_index(0)
        fl = T("stretched nearly flat", size=40, color=LIGHT).move_to([0, -3.4, 0])
        self.at("nearly flat")
        self.play(Create(gA), Create(gB), FadeIn(fl, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        lA, hA, lB, hB = sheet_base()
        nA, cA, nB, cB = nc_labels()
        lab = greek("β", "strands", size=52, color=BLUE).move_to([0, 3.4, 0])
        self.add(lA, hA, lB, hB, lab, nA, cA, nB, cB)
        sA, sB = sheet_stubs(YA), sheet_stubs(YB)
        up = tag("above the sheet", LIGHT, 34, [-4.9, 3.25, 0])
        dn = tag("below the sheet", LIGHT, 34, [-4.9, -3.35, 0])
        self.at("side chains")
        self.play(LaggedStart(*[GrowFromPoint(s, s[0].get_start()) for s in list(sA) + list(sB)], lag_ratio=0.07), run_time=1.1)
        self.at("above")
        self.play(FadeIn(up), run_time=0.3)
        self.at("below")
        self.play(FadeIn(dn), run_time=0.3)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        lA, hA, lB, hB = sheet_base()
        nA, cA, nB, cB = nc_labels()
        sA, sB = sheet_stubs(YA), sheet_stubs(YB)
        self.add(lA, hA, lB, hB, sA, sB, nA, cA, nB, cB)
        zip_ = sheet_hbonds(YA, YB)
        self.at("bonds")
        self.play(LaggedStart(*[Create(z) for z in zip_], lag_ratio=0.2), run_time=1.6)
        par = T("parallel", size=50, color=TEXT).move_to([0, -3.4, 0])
        self.at("they can")
        self.play(FadeIn(par, shift=UP * 0.1), run_time=0.5)
        hB2 = make_head(SXS, YB, AMP, BLUE, -1)
        anti = T("antiparallel", size=50, color=TEXT).move_to([0, -3.4, 0])
        nB2 = T("N", size=40, color=LIGHT).move_to(cB.get_center())
        cB2 = T("C", size=40, color=LIGHT).move_to(nB.get_center())
        self.at("opposite directions")
        self.play(FadeOut(hB, shift=RIGHT * 0.3), FadeIn(hB2, shift=RIGHT * 0.3), Transform(par, anti),
                  Transform(nB, nB2), Transform(cB, cB2), run_time=0.8)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        lA, hA, lB, hB = sheet_base()
        sA, sB = sheet_stubs(YA), sheet_stubs(YB)
        zip_ = sheet_hbonds(YA, YB)
        hB2 = make_head(SXS, YB, AMP, BLUE, -1)
        nA, cA, nB, cB = nc_labels(flipB=True)
        sheet = VGroup(lA, hA, lB, hB2, sA, sB, zip_, nA, cA, nB, cB)
        self.add(sheet)
        self.at("those strands")
        self.play(sheet.animate.scale(0.74).move_to([0, 1.55, 0]), run_time=0.7)
        self.play(lA.animate.set_color(TEAL), hA.animate.set_color(TEAL), lB.animate.set_color(PURPLE), hB2.animate.set_color(PURPLE),
                  run_time=0.4)
        n = 22
        step = 0.5
        x0 = -step * (n - 1) / 2
        cells = strip(n, x0, step, -1.35, side=0.42)
        seg1, seg2 = range(3, 6), range(16, 19)
        self.at("far apart")
        self.play(FadeIn(cells, shift=UP * 0.1), run_time=0.4)
        a1 = VGroup(*[cells[i] for i in seg1])
        a2 = VGroup(*[cells[i] for i in seg2])
        self.play(a1.animate.set_stroke(TEAL).set_fill(TEAL, 0.9), a2.animate.set_stroke(PURPLE).set_fill(PURPLE, 0.9), run_time=0.4)
        arc = ArcBetweenPoints(cells[4].get_bottom(), cells[17].get_bottom(), angle=PI / 2.2, color=TEXT, stroke_width=5)
        lab = T("far apart in sequence", size=44, color=TEXT).move_to([0, -3.5, 0])
        self.at("in the sequence")
        self.play(Create(arc), FadeIn(lab), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------ proline
PBY = -1.5
PN, PCA = np.array([-2.6, PBY, 0.0]), np.array([2.6, PBY, 0.0])


def calpha(size=32, color=BLUE):
    return VGroup(T("C", size=size, color=color), M("α", size=size, color=color)).arrange(RIGHT, buff=0.04, aligned_edge=DOWN)


def pro_cartoon():
    bar = Line([-6.0, PBY, 0], [6.0, PBY, 0], color=BLUE, stroke_width=12)
    nchip = chip("N", BLUE, size=42).move_to(PN).set_z_index(6)
    ca = Dot(PCA, radius=0.22, color=BLUE).set_z_index(6)
    cal = calpha(34).move_to(PCA + DOWN * 0.7)
    loop = VMobject(stroke_color=GOLD, stroke_width=10).set_z_index(5)
    loop.set_points(CubicBezier(PCA + UP * 0.12, np.array([3.9, 3.5, 0]), np.array([-3.9, 3.5, 0]), PN + UP * 0.38).get_points())
    return bar, nchip, ca, cal, loop


def loop_poly(loop, nchip, ca):
    pts = [loop.point_from_proportion(p) for p in np.linspace(0, 1, 40)]
    pts += [nchip.get_top(), ca.get_center()]
    return Polygon(*pts, stroke_width=0, fill_color=GOLD, fill_opacity=0.25).set_z_index(1)


class S14(SpokenScene):
    def construct(self):
        bar, nchip, ca, cal, loop = pro_cartoon()
        bb = T("backbone", size=32, color=LIGHT).move_to([-5.0, PBY - 0.65, 0])
        pl = T("proline", size=54, color=GOLD, font=TITLE_FONT).move_to([-4.9, 3.1, 0])
        rb = T("a rule-breaker", size=54, color=GOLD, font=TITLE_FONT).move_to([-4.0, 3.1, 0])
        self.play(Create(bar), FadeIn(nchip), FadeIn(ca), FadeIn(cal), FadeIn(bb), FadeIn(rb, shift=DOWN * 0.1), run_time=0.9)
        self.at("proline")
        self.play(Transform(rb, pl), run_time=0.5)
        sc = tag("side chain", GOLD, 36, [3.9, 2.9, 0])
        self.at("side chain")
        self.play(FadeIn(sc, shift=DOWN * 0.1), Create(loop), run_time=1.9, rate_func=linear)
        self.at("own backbone")
        self.play(Indicate(bar, color=BLUE, scale_factor=1.0), run_time=0.7)
        nl = tag("backbone nitrogen", BLUE, 32, [-1.2, PBY - 1.0, 0])
        self.at("nitrogen")
        self.play(Indicate(nchip, color=BLUE, scale_factor=1.3), FadeIn(nl), run_time=0.6)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        bar, nchip, ca, cal, loop = pro_cartoon()
        pl = T("proline", size=54, color=GOLD, font=TITLE_FONT).move_to([-4.9, 3.1, 0])
        bb = T("backbone", size=32, color=LIGHT).move_to([-5.0, PBY - 0.65, 0])
        self.add(bar, nchip, ca, cal, loop, pl, bb)
        poly = loop_poly(loop, nchip, ca)
        ringlab = T("ring", size=56, color=GOLD).move_to([0, 0.7, 0])
        self.at("that makes a ring")
        self.play(FadeIn(poly), FadeIn(ringlab), run_time=0.8)
        self.at("proline has no")
        ghost = VGroup(DashedVMobject(Circle(radius=0.4, color=GREY, stroke_width=3), num_dashes=12), T("H", size=40, color=GREY)).move_to(PN + DOWN * 1.5)
        tie = hb(nchip.get_bottom(), ghost.get_top(), color=GREY, w=3, trim=0.05)
        circ = Circle(radius=0.62, color=RED, stroke_width=6).move_to(nchip)
        crs = cross(ghost.get_center(), 0.45)
        nl = tag("no N–H to donate", RED, 36, [0.9, PBY - 1.5, 0])
        self.play(Create(circ), FadeIn(ghost), Create(tie), run_time=0.7)
        self.at("donate")
        self.play(Create(crs), FadeIn(nl), run_time=0.5)
        self.at("its ring is bulky")
        bulky = T("bulky", size=56, color=GOLD).move_to([0, 0.7, 0])
        self.play(Transform(ringlab, bulky), poly.animate.set_fill(GOLD, 0.5), loop.animate.set_stroke(width=18), run_time=0.8)
        self.finish()


ICON = np.array([5.3, 3.15, 0.0])
QPOS = np.array([-2.7, 3.4, 0.0])


def question_and_timer(running=False):
    q = T("Where can proline sit?", size=52, color=TEXT).move_to(QPOS)
    ctr = np.array([q.get_right()[0] + 1.0, QPOS[1] - 0.05, 0.0])
    return q, ctr


class S16(SpokenScene):
    def construct(self):
        hx = Hx()
        v = HView(hx)
        self.add(v.group())
        icon = pro_dot(ICON, r=0.7, size=44)
        q, ctr = question_and_timer()
        back = Circle(radius=0.6, color=GREY, stroke_width=6).move_to(ctr)
        self.at("where in a helix")
        self.play(FadeIn(q, shift=UP * 0.1), FadeIn(back), run_time=0.5)
        self.at("proline")
        self.play(FadeIn(icon, scale=2.0), run_time=0.5)
        self.play(icon.animate.shift(DOWN * 0.3), run_time=0.4, rate_func=there_and_back)
        self.finish()


class S17Pause(NarratedScene):
    def construct(self):
        hx = Hx()
        v = HView(hx)
        self.add(v.group())
        icon = pro_dot(ICON, r=0.7, size=44)
        q, ctr = question_and_timer()
        self.add(icon, q)
        tr = ValueTracker(1.0)
        ring = always_redraw(lambda: Arc(start_angle=PI / 2, angle=TAU * tr.get_value(), radius=0.6, color=GOLD, stroke_width=12)
                             .move_to(ctr))
        back = Circle(radius=0.6, color=GREY, stroke_width=6).move_to(ctr)
        self.add(back, ring)
        self.play(tr.animate.set_value(0.001), run_time=4.6, rate_func=linear)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        hx = Hx()
        v = HView(hx)
        self.add(v.group())
        icon = pro_dot(ICON, r=0.7, size=44)
        q, ctr = question_and_timer()
        self.add(icon, q)
        rect = first_turn_rect(hx)
        self.at("in the first turn")
        self.play(FadeOut(q), icon.animate.move_to(hx.P(2)).scale(0.5), FadeOut(v.beads[2]), FadeOut(v.dots[2][1]), Create(rect),
                  run_time=1.0)
        ghosts = VGroup()
        rings = VGroup()
        for i in (0, 1, 3):
            a = hx.nh(i) + LEFT * 0.2
            rings.add(Circle(radius=0.2, stroke_color=LIGHT, stroke_width=4).move_to(hx.nh(i)).set_z_index(8))
            ghosts.add(DashedLine(a, a + LEFT * 0.85, dash_length=0.12, color=LIGHT, stroke_width=4).set_z_index(8))
            ghosts.add(tip(a + LEFT * 0.9, LEFT, LIGHT, 0.2))
        nl = tag("first turn: no partners four back anyway", LIGHT, 38, [0, -3.45, 0])
        self.at("groups have no partners")
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), LaggedStart(*[Create(g) for g in ghosts], lag_ratio=0.1),
                  FadeIn(nl), run_time=1.0)
        ok = VGroup(M("✓", size=52, color=GREEN), T("helix intact", size=46, color=GREEN)).arrange(RIGHT, buff=0.25).move_to([0.2, 3.35, 0])
        self.at("losing one")
        self.play(FadeIn(ok, shift=DOWN * 0.15), Indicate(v.chain, color=GREEN, scale_factor=1.0), run_time=0.9)
        self.finish()


class S19(SpokenScene):
    def construct(self):
        hx = Hx()
        v = HView(hx)
        self.add(v.group())
        icon = pro_dot(ICON, r=0.7, size=44)
        self.add(icon)
        hx2 = Hx(x0=-5.0, y0=0.6, R=2.1, rise=1.15, kink=-0.38)
        v2 = HView(hx2, pros=(4,), skip=(0,))
        self.at("in the middle")
        self.play(icon.animate.move_to(hx.P(4)).scale(0.5), FadeOut(v.beads[4]), FadeOut(v.dots[4][1]), run_time=0.7)
        self.at("proline breaks")
        anims = [Transform(v.chain, v2.chain)]
        for i in range(hx.N):
            if i != 4:
                anims.append(Transform(v.beads[i], v2.beads[i]))
                anims.append(Transform(v.dots[i], v2.dots[i]))
        for i, l in v.lines.items():
            if i != 0:
                anims.append(Transform(l, v2.lines[i]))
        anims.append(Transform(v.guides, v2.guides))
        self.play(*anims, run_time=1.3)
        self.at("cannot donate")
        a, b = hx2.co(0), hx2.nh(4)
        mid = (a + b) / 2
        lost = v.lines[0]
        self.play(lost.animate.set_color(RED).set_stroke(width=8), run_time=0.4)
        xx = cross(mid, 0.4)
        nl = tag("no N–H: bond lost", RED, 42, [-2.4, -3.2, 0])
        self.play(FadeIn(xx, scale=1.5), FadeIn(nl), run_time=0.5)
        self.play(lost.animate.set_stroke(opacity=0.45), run_time=0.5)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        # two stacked turns of the backbone, schematic: the proline ring on this turn presses into the turn before it
        cxr = 0.6
        up = ParametricFunction(lambda x: np.array([x, 2.3 + 0.9 * np.exp(-(x - cxr) ** 2 / 0.9), 0.0]), t_range=[-6.2, 6.2, 0.05],
                                color=BLUE, stroke_width=11)
        lo = Line([-6.2, -2.0, 0], [6.2, -2.0, 0], color=BLUE, stroke_width=11)
        ring = Circle(radius=1.1, stroke_color=GOLD, stroke_width=9, fill_color=GOLD, fill_opacity=0.35).move_to([cxr, -0.05, 0])
        t_before = T("turn before", size=36, color=BLUE).move_to([-4.2, 3.2, 0])
        t_this = T("this turn", size=36, color=BLUE).move_to([-4.2, -2.7, 0])
        self.add(lo, t_this)
        pl = tag("proline ring", GOLD, 36, [-3.2, -0.4, 0])
        self.play(FadeIn(ring, scale=0.6), FadeIn(pl, shift=RIGHT * 0.1), Create(up), FadeIn(t_before), run_time=0.7)
        hit = np.array([cxr, 1.08, 0.0])
        self.at("bumps into")
        rays = VGroup(*[Line(hit + 1.0 * np.array([np.cos(a), np.sin(a), 0]), hit + 1.9 * np.array([np.cos(a), np.sin(a), 0]),
                             color=RED, stroke_width=10) for a in np.linspace(0.15, PI - 0.15, 9)])
        flash = Circle(radius=1.0, color=RED, stroke_width=8, fill_color=RED, fill_opacity=0.7).move_to(hit).set_z_index(9)
        self.play(ring.animate.scale(1.08, about_point=np.array([cxr, -1.15, 0])), FadeIn(flash, scale=0.4), Create(rays), run_time=0.45)
        clash = tag("clash", RED, 52, [cxr + 3.0, 0.6, 0])
        self.at("turn before")
        self.play(FadeIn(clash), Indicate(up, color=RED, scale_factor=1.0), run_time=0.7)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        cx, cy, W = -1.9, 0.15, 6.4
        ax, img = rama(cx, cy, W)
        self.add(ax, img, island_labels(cx, cy, W, alpha=False))
        lx = cx + (-65) / 360 * W
        band = Line([lx, cy - W / 2, 0], [lx, cy + W / 2, 0], color=GOLD, stroke_width=3).set_opacity(0.4).set_z_index(5)
        self.at("its fixed angle")
        self.play(Create(band), run_time=0.7)
        txt = VGroup(M("φ ≈ −65°", size=50, color=GOLD), T("fixed by the ring", size=36, color=GOLD)).arrange(DOWN, buff=0.2).move_to([4.2, 1.9, 0])
        self.play(FadeIn(txt, shift=LEFT * 0.1), run_time=0.5)
        mk = Dot(c2p(cx, cy, W, -65, -42), radius=0.17, color=GOLD).set_z_index(7)
        halo = Circle(radius=0.42, color=GOLD, stroke_width=7).move_to(mk).set_z_index(7)
        lab = T("helical island", size=44, color="#9BE07F").move_to([4.2, c2p(cx, cy, W, 0, -42)[1], 0])
        lead = Line(halo.get_right(), lab.get_left() + LEFT * 0.15, color=GREEN, stroke_width=3).set_z_index(7)
        self.at("that angle")
        self.play(FadeIn(mk, scale=2.0), Create(halo), run_time=0.6)
        self.at("helical one")
        self.play(FadeIn(lab, shift=LEFT * 0.1, run_time=0.25), Create(lead), Indicate(halo, color=GREEN, scale_factor=1.3), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------ collagen
def three_springs():
    return [spring(-5.6, 5.6, SY[k], 0.7, 2.0, STRAND_COLS[k]) for k in range(3)]


class S22(SpokenScene):
    def construct(self):
        sp = three_springs()
        lab = T("collagen", size=58, color=TEXT, font=TITLE_FONT).move_to([0, 3.35, 0])
        self.add(*sp)
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.4)
        icon = Circle(radius=0.75, stroke_color=GOLD, stroke_width=10, fill_color=GOLD, fill_opacity=0.4).move_to([-5.0, SY[2], 0]).set_z_index(8)
        il = tag("proline ring", GOLD, 34, [-5.0, -3.35, 0])
        self.at("same ring")
        self.play(FadeIn(icon, scale=0.5), FadeIn(il), run_time=0.5)
        rl = tag("ring pre-shapes the strand", GOLD, 34, [-0.9, -3.35, 0])
        self.at("pre shapes")
        self.play(FadeIn(rl, shift=UP * 0.1), *[s_.animate.set_stroke(width=9) for g in sp for s_ in g[::2]], run_time=0.8)
        eh = tag("extended helix", TEXT, 34, [5.0, -3.35, 0])
        self.at("extended helix")
        self.play(FadeIn(eh, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        names = ["Gly", "X", "Y"] * 3
        step = 1.36
        xs = [(i - 4) * step for i in range(9)]
        cy = 0.7
        link = Line([xs[0] - 0.4, cy, 0], [xs[-1] + 0.4, cy, 0], color=BLUE, stroke_width=8).set_z_index(0)
        cells = VGroup()
        for i, (n, x) in enumerate(zip(names, xs)):
            c = chip(n, GREY, size=40, pad=0.14).move_to([x, cy, 0])
            c[0].set_fill(BG, 1.0).set_z_index(2)
            c[1].set_z_index(3)
            cells.add(c)
        self.play(Create(link), LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.1), run_time=0.8)
        brs = VGroup()
        for k in range(3):
            xa, xb = xs[3 * k] - 0.62, xs[3 * k + 2] + 0.62
            y = cy - 0.85
            brs.add(VGroup(Line([xa, y, 0], [xb, y, 0], color=TEXT, stroke_width=5),
                           Line([xa, y, 0], [xa, y + 0.2, 0], color=TEXT, stroke_width=5),
                           Line([xb, y, 0], [xb, y + 0.2, 0], color=TEXT, stroke_width=5)))
        rl = T("repeating pattern: Gly-X-Y", size=50, color=WHITE).move_to([0, 2.5, 0])
        self.at("a pattern")
        self.play(Create(brs), FadeIn(rl, run_time=0.25), run_time=0.5)
        gly = VGroup(*[cells[i] for i in (0, 3, 6)])
        self.at("glycine")
        self.play(gly.animate.set_color(TEXT), *[cells[i][0].animate.set_fill(TEXT, 0.25) for i in (0, 3, 6)], run_time=0.5)
        xy = VGroup(*[cells[i] for i in range(9) if i % 3])
        self.at("then two other")
        self.play(Indicate(xy, color=LIGHT, scale_factor=1.1), run_time=0.9)
        xo = T("X and Y are often Pro and Hyp", size=42, color=GOLD).move_to([0, -1.5, 0])
        self.at("often")
        self.play(FadeIn(xo, shift=UP * 0.1, run_time=0.25), run_time=0.5)
        newx = [chip("Pro", GOLD, size=40, pad=0.14).move_to(cells[i]) for i in (1, 7)]
        newy = [chip("Hyp", GOLD, size=40, pad=0.14).move_to(cells[i]) for i in (2, 8)]
        for c in newx + newy:
            c[0].set_fill(BG, 1.0)
        pl = T("Pro = proline", size=34, color=GOLD).move_to([-3.0, -2.7, 0])
        self.at("proline")
        self.play(*[Transform(cells[i], newx[j]) for j, i in enumerate((1, 7))], FadeIn(pl, shift=UP * 0.1), run_time=0.6)
        hl = T("Hyp = hydroxyproline", size=34, color=GOLD).move_to([2.6, -2.7, 0])
        self.at("hydroxyproline")
        self.play(*[Transform(cells[i], newy[j]) for j, i in enumerate((2, 8))], FadeIn(hl, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        sp = three_springs()
        self.add(*sp)
        big = braid(0, 0.1, 12.4, 1.7, 5.0)
        self.at("three chains")
        self.play(*[ReplacementTransform(sp[k], big[k]) for k in range(3)], run_time=1.6)
        tl = T("triple helix", size=56, color=TEXT, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.at("triple helix")
        self.play(FadeIn(tl, shift=DOWN * 0.1), run_time=0.5)
        small = braid(BX, EY + 0.4, SBW, SAMP, SLAM)
        circles = endon(EX, EY)
        sl = slot(EX, EY)
        sv = T("side view", size=42, color=WHITE).move_to([BX, EY - 1.5, 0])
        ev = T("end-on view", size=42, color=WHITE).move_to([EX, -3.55, 0])
        self.at("every third")
        self.play(*[ReplacementTransform(big[k], small[k]) for k in range(3)], FadeOut(tl), FadeIn(circles), FadeIn(sv), FadeIn(ev), run_time=1.2)
        arrows = inward_arrows(EX, EY)
        cl = VGroup(T("every third residue", size=46, color=GOLD, weight=BOLD), T("points to the centre", size=46, color=GOLD, weight=BOLD)).arrange(DOWN, buff=0.12)
        cl.move_to([-3.4, 3.0, 0])
        cl = VGroup(cl, Arrow(cl.get_right() + RIGHT * 0.1, [EX - 0.5, EY + 0.35, 0], buff=0.05, color=GOLD, stroke_width=8).set_z_index(9))
        self.at("crowded center")
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(sl), FadeIn(cl, run_time=0.3),
                  Indicate(sl, color=TEXT, scale_factor=1.4), run_time=1.0)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        small = braid(BX, EY + 0.4, SBW, SAMP, SLAM)
        circles = endon(EX, EY)
        sl = slot(EX, EY)
        arrows = inward_arrows(EX, EY)
        cl = VGroup(T("every third residue", size=46, color=GOLD, weight=BOLD), T("points to the centre", size=46, color=GOLD, weight=BOLD)).arrange(DOWN, buff=0.12)
        cl.move_to([-3.4, 3.0, 0])
        cl = VGroup(cl, Arrow(cl.get_right() + RIGHT * 0.1, [EX - 0.5, EY + 0.35, 0], buff=0.05, color=GOLD, stroke_width=8).set_z_index(9))
        sv = T("side view", size=42, color=WHITE).move_to([BX, EY - 1.5, 0])
        ev = T("end-on view", size=42, color=WHITE).move_to([EX, -3.55, 0])
        self.add(small, circles, sl, arrows, cl, sv, ev)
        h = T("H", size=96, color=TEXT, weight=BOLD).move_to([EX, EY, 0]).set_z_index(8)
        gl = tag("glycine: just an H", TEXT, 44, [EX, -3.55, 0])
        big_slot = slot(EX, EY, r=0.95)
        wide = endon(EX, EY, spread=2.3)
        self.at("only glycine")
        self.play(FadeOut(arrows), FadeOut(cl), FadeOut(ev), FadeOut(sl), FadeIn(big_slot), FadeIn(h, scale=1.8),
                  *[Transform(circles[k], wide[k]) for k in range(3)], FadeIn(gl), run_time=0.9)
        self.at("small enough")
        self.play(Indicate(h, color=GREEN, scale_factor=1.25), run_time=0.7)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        BY = 0.9
        small = braid(BX, BY, SBW, SAMP, SLAM)
        wide = endon(EX, EY, spread=2.3)
        big_slot = slot(EX, EY, r=0.95)
        h = T("H", size=96, color=TEXT, weight=BOLD).move_to([EX, EY, 0]).set_z_index(8)
        gl = tag("glycine: just an H", TEXT, 44, [EX, -3.55, 0])
        self.add(small, wide, big_slot, h, gl)
        blob = Circle(radius=1.2, stroke_color=RED, stroke_width=6, fill_color=RED, fill_opacity=0.85).move_to([EX, EY, 0]).set_z_index(8)
        bl = VGroup(T("larger residue", size=38, color=RED), T("replaces glycine", size=38, color=RED)).arrange(DOWN, buff=0.1).move_to([BX, -1.55, 0])
        bulged = braid(BX, BY, SBW, SAMP, SLAM, bulge=0.8)
        wider = endon(EX, EY, spread=2.6)
        crack = VMobject(stroke_color=RED, stroke_width=8).set_points_as_corners(
            [[BX - 0.3, 2.5, 0], [BX + 0.3, 1.75, 0], [BX - 0.3, 1.0, 0], [BX + 0.3, 0.25, 0], [BX - 0.3, -0.5, 0]]).set_z_index(9)
        self.at("put a larger residue")
        self.play(Indicate(h, color=TEXT, scale_factor=1.2), run_time=0.5)
        hx_ = crs = None
        self.play(h.animate.scale(0.45).move_to([EX + 2.9, 2.6, 0]), FadeOut(gl), FadeOut(big_slot), FadeIn(blob, scale=0.3), FadeIn(bl), run_time=0.9)
        self.play(Create(cross([EX + 2.9, 2.6, 0], 0.4)), run_time=0.3)
        self.play(*[Transform(wide[k], wider[k]) for k in range(3)], *[Transform(small[k], bulged[k]) for k in range(3)], Create(crack), run_time=1.0)
        ty = T("type I collagen", size=46, color=TEXT).move_to([BX, 3.4, 0])
        self.at("in type")
        self.play(FadeIn(ty, shift=UP * 0.1), run_time=0.5)
        oi = VGroup(T("osteogenesis imperfecta", size=38, color=RED), T("(brittle-bone disease)", size=36, color=RED)).arrange(DOWN, buff=0.12).move_to([BX, -3.0, 0])
        self.at("that is a common cause")
        self.play(FadeIn(oi, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S27(SpokenScene):
    def construct(self):
        div = Line([0, -3.5, 0], [0, 3.5, 0], color=GREY, stroke_width=2).set_opacity(0.6)
        hx = Hx(x0=-6.2, y0=-0.1, R=2.2, rise=0.62, N=9, kink=-0.38, kink_at=4.0)
        v = HView(hx, pros=(4,), skip=(0,))
        braid_r = braid(3.4, -0.1, 5.8, 2.0, 3.2)
        pros = VGroup()
        for dx, k in zip((-1.9, 0.1, 1.9), range(3)):
            ph = 2 * PI * k / 3
            pros.add(pro_dot([3.4 + dx, -0.1 + 2.0 * np.sin(2 * PI * dx / 3.2 + ph), 0], r=0.38, size=26))
        self.play(FadeIn(div), Create(v.chain), *[FadeIn(b) for b in v.beads.values()], *[FadeIn(d) for d in v.dots.values()],
                  *[Create(l) for l in v.lines.values()], Create(braid_r), run_time=0.8)
        l1 = tag("proline breaks the helix", RED, 36, [-3.3, 2.9, 0])
        l2 = tag("proline builds collagen", GOLD, 36, [3.4, 2.9, 0])
        self.at("structure")
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=0.4)
        self.at("builds another")
        self.play(FadeIn(l2, shift=DOWN * 0.1), FadeIn(pros, scale=1.4), run_time=0.5)
        self.at("one residue")
        self.play(Indicate(v.beads[4], color=GOLD, scale_factor=1.5), Indicate(pros, color=GOLD, scale_factor=1.4), run_time=1.0)
        self.finish()


class S28(SpokenScene):
    def construct(self):
        hx = Hx(x0=-6.4, y0=0.3, R=1.9, rise=0.5, N=9)
        helix = VGroup(hx.guides(), hx.chain(w=10))
        xs = np.linspace(3.0, 6.2, 7)
        la, ha = zig(1.5, xs=xs, amp=0.3, w=10, head=0.55, hw=0.4)
        lb, hb_ = zig(-0.9, xs=xs, amp=0.3, w=10, head=0.55, hw=0.4)
        sheet = VGroup(la, ha, lb, hb_)
        items = [helix, sheet]
        self.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in items], lag_ratio=0.2), run_time=1.0)
        self.play(helix.animate.shift(LEFT * 0.3), sheet.animate.shift(RIGHT * 0.3), run_time=1.8, rate_func=smooth)
        q = T("?", size=190, color=GREY, font=TITLE_FONT).move_to([0, 0.9, 0])
        self.at("but it does not choose")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        wl = T("what chooses?", size=54, color=TEXT).next_to(q, DOWN, buff=0.3)
        self.at("which ones")
        self.play(FadeIn(wl, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        hx = Hx(x0=-6.4, y0=0.5, R=2.2, rise=0.62, N=9)
        v = HView(hx)
        xs = np.linspace(1.4, 5.6, 9)
        lA, hA = zig(1.7, xs=xs, amp=0.3, w=10, head=0.6, hw=0.42)
        lB, hB = zig(-0.7, xs=xs, amp=0.3, w=10, head=0.6, hw=0.42)
        zs = sheet_hbonds(1.7, -0.7, xs=xs)
        sheet = VGroup(lA, hA, lB, hB, zs)
        full = VGroup(v.group(), sheet)
        self.play(FadeIn(full), run_time=0.4)
        cap = T("the backbone hydrogen-bonding to itself", size=46, color=TEXT).move_to([0, -3.3, 0])
        self.at("backbone")
        self.play(FadeIn(cap, shift=UP * 0.1), *[Indicate(l, color=TEXT, scale_factor=1.0) for l in v.lines.values()],
                  Indicate(zs, color=TEXT, scale_factor=1.0), run_time=1.0)
        self.finish()


class S30End(EndCard):
    LINE = "Helices and sheets are the backbone hydrogen-bonding to itself, in shapes the map allows."

    def construct(self):
        l1 = T("Helices and sheets are the backbone", size=44, font=TITLE_FONT)
        l2 = T("hydrogen-bonding to itself,", size=44, font=TITLE_FONT)
        l3 = T("in shapes the map allows.", size=44, font=TITLE_FONT)
        line = VGroup(l1, l2, l3).arrange(DOWN, buff=0.22)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
