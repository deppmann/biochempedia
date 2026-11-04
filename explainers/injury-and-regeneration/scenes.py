"""Injury and regeneration, chapter 1: One Cut, Two Fates  (Biochemistrypedia chaptered film)

COLOR MAP (one color per concept, shared by all chapters of this lesson)
  BLUE   = the neuron: cell body, axon, the attached (proximal) piece, the attached piece's question
  RED    = the cut-off (distal) piece and its destruction; also the tissue's resistance
  GOLD   = growth cones, regrowth, the program bracket, the neuron's drive to grow
  SAGE   = repair glia and the nerve's surrounding tissue (Schwann cells); debris clearing
  GREY   = labels, outlines, the spinal cord's surrounding tissue, the time axis, de-emphasized
  TEXT   = cut marks, ticks, question marks, headings
  (kept from the earlier film for the later chapters: TEAL = NMNAT2/Wlds, ORANGE = NMN,
   GREEN = NAD+/ATP, YELLOW = calcium, PURPLE = calpain)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SAGE = "#9BB99B"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def seg(p0, p1, w=0.5, color=BLUE, op=0.3, sw=3.5):
    """A thick rounded tube between two points (an axon piece)."""
    p0 = np.array([p0[0], p0[1], 0.0])
    p1 = np.array([p1[0], p1[1], 0.0])
    length = np.linalg.norm(p1 - p0)
    r = RoundedRectangle(corner_radius=min(w / 2, length / 2 - 0.001), width=length, height=w,
                         stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)
    ang = np.arctan2(p1[1] - p0[1], p1[0] - p0[0])
    if abs(ang) > 1e-6:
        r.rotate(ang)
    return r.move_to((p0 + p1) / 2)


def beads(x0, x1, y, h=0.5, n=7, color=RED, op=0.25):
    pitch = (x1 - x0) / n
    g = VGroup()
    for i in range(n):
        w = pitch * 0.62
        g.add(RoundedRectangle(corner_radius=min(h, w) / 2, width=w, height=h * 0.9, stroke_color=color,
                               stroke_width=3.5, fill_color=color, fill_opacity=op)
              .move_to([x0 + pitch * (i + 0.5), y + (0.05 if i % 2 else -0.05), 0]))
    return g


def soma(x, y, r=1.0):
    back = Circle(radius=r, stroke_color=BLUE, stroke_width=4, fill_color=BG, fill_opacity=1)
    fill = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.3)
    nuc = Circle(radius=r * 0.38, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.35)
    g = VGroup(back, fill, nuc).move_to([x, y, 0])
    g.nuc = nuc
    return g


def cutmark(x, y, h=0.9, ang=0.0):
    g = VGroup(*[Line([dx - 0.12, -h / 2, 0], [dx + 0.12, h / 2, 0], color=TEXT, stroke_width=5)
                 for dx in (-0.2, 0.2)])
    if ang:
        g.rotate(ang)
    return g.move_to([x, y, 0])


def cone(x, y, color=GOLD, s=1.0, ang=0.0):
    """A broad, fingered growth tip (a schematic cell shape, not a molecule). Points along +x at ang=0."""
    p = Polygon([-0.45, -0.16, 0], [0.03, -0.37, 0], [0.48, -0.33, 0],
                [0.25, -0.10, 0], [0.58, 0, 0], [0.25, 0.10, 0],
                [0.48, 0.33, 0], [0.03, 0.37, 0], [-0.45, 0.16, 0],
                stroke_color=color, fill_color=color, fill_opacity=0.45, stroke_width=3)
    p.scale(s)
    if ang:
        p.rotate(ang)
    return p.shift([x, y, 0])


def glia(x, y, color=SAGE, ang=0.0):
    e = Ellipse(width=1.25, height=0.55, color=color, fill_opacity=0.25, stroke_width=3)
    if ang:
        e.rotate(ang)
    return e.move_to([x, y, 0])


def target(x, y, s=1.0):
    body = RoundedRectangle(width=0.85, height=1.55, corner_radius=0.35, color=GREY, fill_opacity=0.2)
    lines = VGroup(*[Line([-0.25, z, 0], [0.25, z, 0], color=GREY) for z in (-0.42, 0, 0.42)])
    return VGroup(body, lines).scale(s).move_to([x, y, 0])


def qm(x, y, size=54):
    return T("?", size, TEXT, weight=BOLD).move_to([x, y, 0])


def tick(x, y, r=0.3, color=TEXT):
    c = Circle(radius=r, stroke_color=color, stroke_width=3.5, fill_color=BG, fill_opacity=1)
    ck = VMobject(stroke_color=color, stroke_width=5)
    ck.set_points_as_corners([[-0.45 * r, -0.02 * r, 0], [-0.1 * r, -0.4 * r, 0], [0.5 * r, 0.42 * r, 0]])
    return VGroup(c, ck).move_to([x, y, 0])


def bracket(x0, x1, y, color=GOLD, d=0.2, w=5):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([[x0, y - d, 0], [x0, y, 0], [x1, y, 0], [x1, y - d, 0]])
    return m


def chip_to(c, o):
    """Animations that set a bchip (back, box, label) to opacity o (1.0 = normal)."""
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def dim(m, f):
    """Scale the stroke and fill opacity of every part (a bracket keeps no fill)."""
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=sm.get_stroke_opacity() * f)
        sm.set_fill(opacity=sm.get_fill_opacity() * f)
    return m


def veil(o=0.5, w=14.3, h=8.1, at=(0, 0)):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=o).move_to([at[0], at[1], 0])


def dimmed(m, f):
    return dim(m.copy(), f)


def beads_line(p0, p1, n=7, h=0.8, color=RED, op=0.28, jitter=0.05):
    """Separate rounded fragments along the straight line p0 -> p1 (any angle)."""
    p0 = np.array([p0[0], p0[1], 0.0])
    p1 = np.array([p1[0], p1[1], 0.0])
    d = p1 - p0
    L = np.linalg.norm(d)
    u = d / L
    perp = np.array([-u[1], u[0], 0.0])
    ang = np.arctan2(u[1], u[0])
    pitch = L / n
    g = VGroup()
    for i in range(n):
        w = pitch * 0.64
        r = RoundedRectangle(corner_radius=min(h, w) / 2 - 0.001, width=w, height=h * 0.9, stroke_color=color,
                             stroke_width=3.5, fill_color=color, fill_opacity=op)
        r.rotate(ang)
        r.move_to(p0 + u * pitch * (i + 0.5) + perp * (jitter if i % 2 else -jitter))
        g.add(r)
    return g


# ---- the long diagonal neuron used in s02-s04 ---------------------------------------------------
SO = np.array([-5.3, 2.3, 0.0])      # cell body centre
BE = np.array([5.15, -2.5, 0.0])      # far end of the axon (at the muscle)
UN = (BE - SO) / np.linalg.norm(BE - SO)
PN = np.array([-UN[1], UN[0], 0.0])  # perpendicular, pointing up and to the right
ANG = float(np.arctan2(UN[1], UN[0]))
CUTP = SO + 0.55 * (BE - SO)
SR = 1.2
AXW = 1.0
GAPH = 0.7                           # half-gap between the two pieces after the cut


def hn_soma():
    s = soma(SO[0], SO[1], SR)
    st = VGroup(*[Line(s.get_center() + SR * np.array([np.cos(a), np.sin(a), 0]),
                       s.get_center() + (SR + 0.42) * np.array([np.cos(a), np.sin(a), 0]),
                       color=BLUE, stroke_width=5) for a in (PI / 2 + 0.55, PI / 2 + 0.1, PI - 0.25, -PI / 2 - 0.45)])
    return VGroup(st, s)


def hn_muscle():
    m = target(6.1, BE[1] - 0.05, 1.3)
    lab = T("muscle", 26, GREY).move_to([6.1, BE[1] + 1.2, 0])
    return VGroup(m, lab)


def hn_whole():
    return seg(SO + UN * SR * 0.95, BE, AXW, BLUE)


def hn_prox(g=0.0):
    return seg(SO + UN * SR * 0.95, CUTP - UN * g, AXW, BLUE)


def hn_dist(g=0.0, color=RED):
    return seg(CUTP + UN * g, BE, AXW, color)


def hn_dist_beads(g=GAPH, op=0.28):
    return beads_line(CUTP + UN * (g + 0.0), BE, 7, AXW * 0.95, RED, op)


def hn_cutmark():
    return cutmark(CUTP[0], CUTP[1], 2.1, ANG)


def lbl_dist():
    c = bchip("distal: cut off", RED, 28).move_to([4.4, 1.15, 0])
    pt = CUTP + UN * (GAPH + 3.2) + PN * 0.55
    a = arr([4.2, 0.78, 0], [pt[0], pt[1] + 0.15, 0], RED, 4, 0.2)
    return VGroup(c, a)


def lbl_prox():
    c = bchip("proximal: attached", BLUE, 28).move_to([-3.3, -1.05, 0])
    pt = SO + UN * 2.3 - PN * 0.55
    a = arr([-3.3, -0.68, 0], [pt[0], pt[1] - 0.15, 0], BLUE, 4, 0.2)
    return VGroup(c, a)


# ---- the timeline scenes (s05-s07) --------------------------------------------------------------
XT0, XN = -6.0, -2.6
TBH = 0.72
ROW_A, ROW_B1, ROW_B2, ROW_C, TAX = 0.2, -0.55, -1.3, -2.05, -2.75


def t_axis(y, ticks=True):
    ax = arr([-6.4, y, 0], [6.55, y, 0], GREY, 4)
    t0 = Line([XT0, y - 0.15, 0], [XT0, y + 0.15, 0], color=GREY, stroke_width=4)
    t1 = Line([XN, y - 0.15, 0], [XN, y + 0.15, 0], color=GREY, stroke_width=4)
    l0 = T("0", 26, GREY).move_to([XT0, y - 0.5, 0])
    l1 = T("1.5 to 2 days", 26, GREY).move_to([XN, y - 0.5, 0])
    tt = T("time after the cut (schematic)", 26, GREY).move_to([3.6, y - 0.5, 0])
    return VGroup(ax, t0, t1, l0, l1, tt)


def band(x0, x1, y, color, op=0.3, h=TBH):
    return RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([(x0 + x1) / 2, y, 0])


def inside(text, b, color=TEXT, size=26):
    t = T(text, size, color)
    return t.move_to(b.get_center()).align_to(b, LEFT).shift(RIGHT * 0.2)


def row_label(text, y, x_right=-2.35, color=SAGE, size=26):
    t = T(text, size, color)
    return t.move_to([x_right - t.width / 2, y, 0])


def rowA(y, h):
    b = band(XT0, XN, y, RED, 0.3, h)
    return VGroup(b, inside("normal", b), beads(XN, XN + 2.0, y, h, 3, RED, 0.3))


def band_b1():
    return band(-2.2, 0.4, ROW_B1, SAGE)


def band_b2():
    return band(-2.2, 2.2, ROW_B2, SAGE)


def b2_open():
    d = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=2.4, height=TBH, stroke_color=SAGE,
                                        stroke_width=3).move_to([3.4, ROW_B2, 0]), num_dashes=28)
    return VGroup(d, T("incomplete", 26, SAGE).move_to([3.4, ROW_B2, 0]))


def band_c():
    return band(-1.0, 5.8, ROW_C, GOLD)


def timeline_ab():
    """The s06 end state: axis, row A, rows B1 and B2 with their labels."""
    b1, b2 = band_b1(), band_b2()
    return VGroup(t_axis(TAX), rowA(ROW_A, TBH), b1, inside("fast", b1), row_label("nerve", ROW_B1),
                  b2, inside("slow", b2), b2_open(), row_label("brain and cord", ROW_B2))


# ---- the sensory (dorsal root ganglion) neuron: one nucleus, two branches ----------------------
class DGR:
    """A ganglion neuron drawn upright: the nerve branch runs down, the cord branch runs up, the soma sits to the
    right on a short stem at the junction."""

    def __init__(self, cx, cy=0.15, half=2.75, drop=1.9, r=0.8):
        self.cx, self.r, self.w = cx, r, 0.5
        self.L, self.R = cy - half, cy + half
        self.jy = cy - 0.2
        self.sx = cx + drop
        n0, n1 = self.L - 0.1, self.jy - 0.9
        c0, c1 = self.jy + 0.9, self.R + 0.1
        self.nbox, self.cbox = (n0, n1, 1.6), (c0, c1, 1.8)
        self.yp = n1 - 0.6
        self.yc = c0 + 0.6

    def ctx(self):
        n0, n1, nw = self.nbox
        c0, c1, cw = self.cbox
        nerve = RoundedRectangle(corner_radius=0.3, width=nw, height=n1 - n0, stroke_color=SAGE, stroke_width=2.5,
                                 fill_color=SAGE, fill_opacity=0.08).move_to([self.cx, (n0 + n1) / 2, 0])
        cord = RoundedRectangle(corner_radius=0.3, width=cw, height=c1 - c0, stroke_color=GREY, stroke_width=2.5,
                                fill_color=GREY, fill_opacity=0.08).move_to([self.cx, (c0 + c1) / 2, 0])
        return nerve, cord

    def cell(self):
        stem = seg((self.cx, self.jy), (self.sx - self.r * 0.6, self.jy), self.w * 0.85, BLUE)
        return VGroup(stem, soma(self.sx, self.jy, self.r))

    def peri_whole(self):
        return seg((self.cx, self.L), (self.cx, self.jy), self.w, BLUE)

    def cent_whole(self):
        return seg((self.cx, self.jy), (self.cx, self.R), self.w, BLUE)

    def peri_pieces(self, gap=0.0):
        prox = seg((self.cx, self.yp + gap), (self.cx, self.jy), self.w, BLUE)
        dist = seg((self.cx, self.L - gap), (self.cx, self.yp - gap), self.w, RED)
        return prox, dist

    def cent_pieces(self, gap=0.0):
        prox = seg((self.cx, self.jy), (self.cx, self.yc - gap), self.w, BLUE)
        dist = seg((self.cx, self.yc + gap), (self.cx, self.R + gap), self.w, RED)
        return prox, dist

    def mark_p(self, h=1.0):
        return cutmark(self.cx, self.yp, h, PI / 2)

    def mark_c(self, h=1.0):
        return cutmark(self.cx, self.yc, h, PI / 2)


def lleft(text, x0, y, size=26, color=TEXT):
    """Text whose left edge sits at x0."""
    t = T(text, size, color)
    return t.move_to([x0 + t.width / 2, y, 0])


def lright(text, x1, y, size=26, color=TEXT):
    """Text whose right edge sits at x1."""
    t = T(text, size, color)
    return t.move_to([x1 - t.width / 2, y, 0])


def heading(text, y=3.25, size=44):
    return T(text, size, TEXT, font=TITLE_FONT).move_to([0, y, 0])


def candidates(y=-3.4):
    """The two open candidates, as a neutral pair of equal weight."""
    c1 = bchip("the tissue?", TEXT, 26)
    o = T("or", 26, GREY)
    c2 = bchip("the signal to the cell body?", TEXT, 26)
    # Match both the backing and outline dimensions, preserving equal label weight.
    for c in (c1, c2):
        for box in (c[0], c[1]):
            box.stretch_to_fit_width(5.1)
            box.stretch_to_fit_height(0.7)
    return VGroup(c1, o, c2).arrange(RIGHT, buff=0.35).move_to([0, y, 0])


# ---- the closing idea scenes (s14, s15, s17) ----------------------------------------------------
def idea_body(y, s):
    """cell body, attached piece, cut-off fragments and the gold bracket; s scales the thickness."""
    sm = soma(-5.6, y, 0.95 * s)
    prox = seg((-5.6 + 0.95 * s * 0.9, y), (-0.3, y), 0.8 * s, BLUE)
    bd = beads(0.3, 5.6, y, 0.75 * s, 7, RED, 0.25)
    br = bracket(0.3, 5.6, y - 0.75 * s * 0.5 - 0.3 * s, GOLD, -0.2 * s, 5)
    return VGroup(sm, prox, bd, br)


IDEA_Y, IDEA_S = 1.15, 1.25


def idea_line1():
    a = T("The cut-off piece destroys itself,", 40)
    b = T("by a program it carries.", 40, t2c={"program": GOLD})
    return VGroup(a, b).arrange(DOWN, buff=0.2).move_to([0, -1.55, 0])


def idea_line1_small():
    g = VGroup(T("The cut-off piece", 28), T("destroys itself,", 28),
               T("by a program it carries.", 28, t2c={"program": GOLD})).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    return g.move_to([3.4, 1.75, 0])


def beam_frame(cx, cy, half, tip):
    pv = np.array([cx, cy, 0.0])
    post = Line([cx, cy - 1.3, 0], [cx, cy, 0], color=GREY, stroke_width=6)
    base = Line([cx - 0.6, cy - 1.3, 0], [cx + 0.6, cy - 1.3, 0], color=GREY, stroke_width=6)
    beam = Line(pv + LEFT * half, pv + RIGHT * half, color=GREY, stroke_width=7)
    if tip:
        beam.rotate(tip, about_point=pv)
    pivot = Dot(pv, radius=0.1, color=GREY)
    return VGroup(post, base, beam, pivot), beam.get_start(), beam.get_end()


def pan(end, text, color, size=26, drop=1.0):
    c = chip(text, color, size=size)
    c.move_to(np.array(end) + DOWN * drop)
    s = Line(end, c.get_top(), color=GREY, stroke_width=3)
    return VGroup(s, c)


def idea_bal(tip, withpans=True):
    fr, le, re = beam_frame(0.0, -0.2, 3.4, tip)
    if not withpans:
        return fr, None, None
    return fr, pan(le, "the neuron's\ndrive to grow", GOLD, drop=0.65), pan(re, "resistance of the\nsurrounding tissue", RED, drop=0.65)


def idea_line2():
    g = VGroup(T("The attached piece tends to regrow", 30), T("where drive outweighs resistance.", 30)
               ).arrange(DOWN, buff=0.12)
    return g.move_to([0, -2.55, 0])


def rule_note():
    return T("a rule of thumb, not a measured quantity", 26, GREY).move_to([0, -3.3, 0])


def link_arrow(tip):
    y_end = -0.2 - (0.55 + 0.68 * (1 if tip else 0)) * 0 - (0.7 if tip else 0.0)
    return arr([-4.55, 2.55, 0], [-4.55, y_end, 0], BLUE, 4, 0.2)


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Injury and Regeneration: Why the Brain Does Not Regrow"
    TITLE = "One Cut, Two Fates"


class S01Q(SpokenScene):
    def construct(self):
        XA, XB = -3.4, 3.4
        YC, YE = -0.3, -3.2

        def panel(cx, ctx_color, label):
            ctx = RoundedRectangle(corner_radius=0.5, width=2.0, height=5.5, stroke_color=ctx_color, stroke_width=2.5,
                                   fill_color=ctx_color, fill_opacity=0.1).move_to([cx, -0.75, 0])
            whole = seg((cx, 1.95), (cx, YE), 0.6, BLUE)
            sm = soma(cx, 2.6, 0.65)
            lab = T(label, 30).move_to([cx, 3.55, 0])
            return ctx, whole, sm, lab

        ca, wa, sa, la = panel(XA, SAGE, "Arm nerve")
        cb, wb, sb, lb = panel(XB, GREY, "Spinal cord")
        vb = veil(0.55, 3.0, 8.1, (XB, 0.0))
        qd = qm(0, 0.3, 150)
        dim(qd, 0.6)
        self.play(FadeIn(VGroup(ca, wa, sa, la)), FadeIn(VGroup(cb, wb, sb, lb)), FadeIn(qd), FadeIn(vb), run_time=0.6)
        self.at("in your arm")
        prox_a = seg((XA, 1.95), (XA, YC + 0.15), 0.6, BLUE)
        dist_a = seg((XA, YC - 0.15), (XA, YE), 0.6, RED)
        self.remove(wa)
        self.add(prox_a, dist_a, sa)
        cm_a = cutmark(XA, YC, 1.3, PI / 2)
        self.play(prox_a.animate.shift(UP * 0.15), dist_a.animate.shift(DOWN * 0.15), FadeIn(cm_a), run_time=0.5)
        self.at("can grow back")
        tip = cone(XA, YC + 0.2, s=0.9, ang=-PI / 2)
        new = seg((XA, YC + 0.3), (XA, YC + 0.2), 0.6, BLUE)
        self.add(new, tip)
        self.play(FadeOut(dist_a), FadeOut(cm_a), run_time=0.3)
        self.play(Transform(new, seg((XA, YC + 0.3), (XA, YE + 0.25), 0.6, BLUE)), tip.animate.move_to([XA, YE + 0.1, 0]),
                  run_time=1.3, rate_func=linear)
        ga = lright("grows back", XA - 1.25, -1.8, 28, SAGE)
        self.play(FadeIn(ga), run_time=0.3)
        self.at("your spinal cord")
        self.play(FadeOut(vb), run_time=0.6)
        self.at("and they mostly")
        prox_b = seg((XB, 1.95), (XB, YC + 0.15), 0.6, BLUE)
        dist_b = seg((XB, YC - 0.15), (XB, YE), 0.6, RED)
        self.remove(wb)
        self.add(prox_b, dist_b, sb)
        cm_b = cutmark(XB, YC, 1.3, PI / 2)
        self.play(prox_b.animate.shift(UP * 0.15), dist_b.animate.shift(DOWN * 0.15), FadeIn(cm_b), run_time=0.5)
        self.at("mostly do not")
        bulb = Circle(radius=0.27, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.6).move_to([XB, YC + 0.05, 0])
        self.play(FadeOut(dist_b), FadeIn(bulb), run_time=0.4)
        gb = VGroup(T("mostly", 28, GREY), T("stalls", 28, GREY)).arrange(DOWN, buff=0.1).move_to([XB + 2.3, -1.4, 0])
        self.play(FadeIn(gb), run_time=0.3)
        self.at("Why")
        self.play(Transform(qd, qm(0, 0.3, 160)), run_time=0.5)
        self.finish()


class S02Cut(SpokenScene):
    def construct(self):
        whole = hn_whole()
        sm, mus = hn_soma(), hn_muscle()
        self.add(whole, sm, mus)
        self.wait(0.3)
        self.at("splits each")
        prox, dist = hn_prox(0.0), hn_dist(0.0, BLUE)
        self.remove(whole)
        self.add(prox, dist, sm)
        cm = hn_cutmark()
        self.play(Transform(prox, hn_prox(GAPH)), Transform(dist, hn_dist(GAPH, BLUE)), FadeIn(cm), run_time=0.6)
        self.at("in two")
        self.play(dist.animate.set_color(RED).set_fill(RED, 0.3), run_time=0.6)
        self.at("different fates")
        self.play(Indicate(prox, color=BLUE, scale_factor=1.04), run_time=0.7)
        self.play(Indicate(dist, color=RED, scale_factor=1.04), run_time=0.7)
        self.finish()


class S03Distal(SpokenScene):
    def construct(self):
        prox, dist = hn_prox(GAPH), hn_dist(GAPH)
        sm, mus, cm = hn_soma(), hn_muscle(), hn_cutmark()
        self.add(prox, dist, sm, mus, cm)
        self.at("the piece cut off")
        lab = lbl_dist()
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        self.at("breaks down")
        bd = hn_dist_beads(GAPH, 0.3)
        self.play(ReplacementTransform(dist, bd), run_time=0.9)
        # shrink the neuron to the top, then two tissue boxes with the same breakdown
        neuron = VGroup(prox, bd, sm, mus[0], cm)
        c_old = neuron.get_center()
        sc, c_new = 0.5, np.array([0.0, 1.95, 0.0])
        f = lambda p: c_new + sc * (np.array([p[0], p[1], 0.0]) - c_old)
        lab_new_c = f(CUTP + UN * 4.0) + np.array([0.4, 0.95, 0.0])
        tgt = f(CUTP + UN * 3.2) + PN * 0.3
        self.at("in a limb nerve")
        self.play(neuron.animate.scale(sc, about_point=c_old).move_to(c_new), FadeOut(mus[1]),
                  lab.animate.scale(0.0001).move_to(lab_new_c).set_opacity(0), run_time=0.6)
        self.remove(lab)
        lab2 = bchip("distal: cut off", RED, 26).move_to([4.6, 2.05, 0])
        ar2 = arr([3.75, 1.72, 0], tgt, RED, 4, 0.18)

        def box(x, col, name):
            b = RoundedRectangle(corner_radius=0.35, width=5.9, height=2.3, stroke_color=col, stroke_width=3,
                                 fill_color=col, fill_opacity=0.1).move_to([x, -2.35, 0])
            fr = beads(x - 2.4, x + 2.4, -2.75, 0.8, 6, RED, 0.3)
            lb = T(name, 30, col).move_to([x - 0.45, -1.6, 0])
            tk = tick(x + lb.width / 2 - 0.45 + 0.55, -1.6, 0.27)
            return VGroup(b, fr), VGroup(lb, tk)
        b1, l1 = box(-3.4, SAGE, "limb nerve")
        b2, l2 = box(3.4, GREY, "spinal cord")
        self.play(FadeIn(b1), FadeIn(VGroup(lab2, ar2)), FadeIn(l1), run_time=0.5)
        self.at("in the spinal cord")
        self.play(FadeIn(b2), FadeIn(l2), run_time=0.6)
        self.finish()


class S04Proximal(SpokenScene):
    def construct(self):
        prox = hn_prox(GAPH)
        sm, mus, cm = hn_soma(), hn_muscle(), hn_cutmark()
        debris = hn_dist_beads(GAPH, 0.12)
        dim(debris, 0.8)
        ld = lbl_dist()
        dim(ld, 0.6)
        self.add(prox, sm, mus, cm, debris, ld)
        self.at("the attached piece")
        lp = lbl_prox()
        self.play(FadeIn(lp, shift=DOWN * 0.1), run_time=0.5)
        self.at("grow a new tip")
        tip_c = CUTP - UN * GAPH + UN * 0.42
        tip = cone(tip_c[0], tip_c[1], s=1.15, ang=ANG)
        self.play(FadeOut(cm), FadeIn(tip, scale=0.4), run_time=0.7)
        self.at("depending on")
        q = qm(tip_c[0] + 0.85, tip_c[1] + 0.8, 82)
        self.play(FadeIn(q, scale=0.6), run_time=0.4)
        self.at("on the neuron")
        nl = bchip("the neuron", BLUE, 28).move_to([SO[0] + 0.1, SO[1] - 2.0, 0])
        self.play(Indicate(sm, color=BLUE, scale_factor=1.06), FadeIn(nl), run_time=0.8)
        self.at("what surrounds")
        lw = bchip("what surrounds it", SAGE, 28).move_to([CUTP[0] + 0.6, CUTP[1] - 2.5, 0])
        leader = arr(lw.get_top(), [tip_c[0] + 0.5, tip_c[1] - 0.65, 0], SAGE, 4, 0.2)
        self.play(FadeIn(lw), GrowArrow(leader), run_time=0.55)
        self.finish()


def t1_state():
    ax = t_axis(-2.5)
    a = band(XT0, XN, -0.8, RED, 0.3, 1.5)
    normal = inside("looks normal", a)
    frag = beads(XN + 0.15, 5.7, -0.8, 1.3, 8, RED, 0.3)
    debris = seg((XT0, 1.15), (XN, 1.15), 1.1, RED)
    title = T("cut-off piece · mouse sciatic nerve", 32, TEXT).move_to([0, 3.0, 0])
    link = DashedLine([XN, 2.0, 0], [XN, -2.5, 0], color=GREY, stroke_width=2)
    return VGroup(ax, a, normal, frag, debris, title, link)


class S05T1(SpokenScene):
    def construct(self):
        state = t1_state()
        ax, a, normal, frag, debris, title, link = state
        piece = seg((XT0, 1.15), (XN, 1.15), 1.1, RED)
        self.add(ax, piece, title, link)
        self.at("looks normal")
        self.play(GrowFromEdge(a, LEFT), FadeIn(normal), run_time=0.7)
        self.at("half to two days")
        self.play(Indicate(ax[4], color=TEXT, scale_factor=1.08), run_time=0.5)
        self.at("falls apart")
        self.play(FadeOut(piece), FadeIn(frag), run_time=0.65)
        self.finish()


def clearing_row(y, name, slow=False):
    label = lleft(name, -6.1, y + 0.9, 30, SAGE if not slow else TEXT)
    debris = beads(-1.8, 5.6, y + 0.9, 0.65, 7, RED, 0.28)
    bar = band(-2.0, 2.2 if slow else 0.5, y, SAGE, 0.3, 0.85)
    text = inside("slow" if slow else "fast", bar, size=28)
    result = VGroup(bar, text)
    if slow:
        # An open continuation, rather than a closed ghost box.
        result.add(DashedLine([2.2, y+0.425, 0], [5.9, y+0.425, 0], color=SAGE),
                   DashedLine([2.2, y-0.425, 0], [5.9, y-0.425, 0], color=SAGE),
                   T("incomplete", 28, SAGE).move_to([4.1, y, 0]))
    return label, debris, result


class S06T2(SpokenScene):
    def construct(self):
        hd = heading("Debris clearing", 3.15, 42)
        axis = t_axis(-2.8)
        l1, d1, r1 = clearing_row(1.25, "nerve")
        l2, d2, r2 = clearing_row(-1.1, "brain and cord", True)
        self.add(hd, axis, l1, d1, l2, d2)
        self.at("cleared quickly")
        self.play(FadeIn(r1), LaggedStart(*[FadeOut(m) for m in d1], lag_ratio=0.08), run_time=0.75)
        self.at("slowly in")
        self.play(FadeIn(r2), run_time=0.45)
        self.play(*[FadeOut(d2[i]) for i in range(3)], run_time=0.65)
        self.finish()


class S07T3(SpokenScene):
    def construct(self):
        base = timeline_ab().scale(0.85, about_point=ORIGIN).shift(DOWN * 0.5)
        self.add(base)

        def track(y):
            return VGroup(seg((-4.95, y), (-2.5, y), 0.95, BLUE), soma(-5.65, y, 0.9))
        T1Y, T2Y = 2.8, 0.95
        RY = 2.1
        # Lower summary leaves room for two separate, enlarged neurons.
        cy = ROW_C * 0.85 - 0.5
        # reserve the delay mark first
        self.at("after a delay")
        dl1 = DashedLine([XT0, cy, 0], [-4.15, cy, 0], color=GREY, stroke_width=4)
        dl2 = DashedLine([-2.85, cy, 0], [-1.0, cy, 0], color=GREY, stroke_width=4)
        dtxt = T("delay", 26, GREY).move_to([-3.5, cy, 0])
        c = band_c().scale(0.85, about_point=ORIGIN).shift(DOWN * 0.5)
        self.play(Create(dl1), FadeIn(dtxt), Create(dl2), GrowFromEdge(c, LEFT),
                  FadeIn(inside("weeks to months or longer", c, size=24)), run_time=0.7)
        self.at("attached piece")
        t1 = track(T1Y)
        self.play(FadeIn(t1), run_time=0.4)
        self.at("may regrow")
        tip = cone(-2.3, T1Y, s=1.15)
        grow = seg((-4.95, T1Y), (-2.3, T1Y), 0.6, BLUE)
        self.add(grow, tip)
        self.remove(t1[0])
        self.play(Transform(grow, seg((-4.95, T1Y), (-2.0, T1Y), 0.6, BLUE)),
                  tip.animate.move_to([-1.9, T1Y, 0]), run_time=0.8, rate_func=linear)

        # ruler: 1 tick = 1 mm
        ruler = VGroup(Line([-2.5, RY, 0], [2.5, RY, 0], color=GREY, stroke_width=3),
                       *[Line([x, RY, 0], [x, RY - 0.2, 0], color=GREY, stroke_width=3) for x in np.arange(-2.5, 2.6, 1.0)],
                       *[T(str(i), 26, GREY).move_to([-2.5 + i, RY - 0.5, 0]) for i in range(6)],
                       T("mm", 26, GREY).move_to([3.15, RY - 0.5, 0]))
        rl = VGroup(T("in people, often about", 26, GREY), T("1 mm a day", 26, TEXT)).arrange(DOWN, buff=0.08)
        rl.move_to([4.65, 2.95, 0])
        self.at("in people that is")
        self.play(FadeIn(ruler), FadeIn(rl), run_time=0.5)
        self.at("often about")
        for i in range(1, 4):
            x = -2.5 + i
            self.play(Transform(grow, seg((-4.95, T1Y), (x, T1Y), 0.6, BLUE)), tip.animate.move_to([x + 0.4, T1Y, 0]),
                      run_time=0.55, rate_func=linear)
            self.wait(0.2)
        self.at("or it stalls")
        t2 = track(T2Y)
        tip2 = cone(-2.3, T2Y, s=1.15)
        grow2 = seg((-4.95, T2Y), (-2.3, T2Y), 0.6, BLUE)
        self.remove(t2[0])
        self.play(FadeIn(t2[1]), FadeIn(grow2), run_time=0.3)
        self.add(tip2)
        self.play(Transform(grow2, seg((-4.95, T2Y), (-1.7, T2Y), 0.6, BLUE)), tip2.animate.move_to([-1.3, T2Y, 0]),
                  run_time=1.0, rate_func=linear)
        self.at("as many central")
        stop = Line([-0.65, T2Y - 0.45, 0], [-0.65, T2Y + 0.45, 0], color=RED, stroke_width=14)
        st = T("stalls", 34, RED, weight=BOLD).move_to([0.4, T2Y, 0])
        self.add(stop, st)
        self.play(tip2.animate.set_stroke(opacity=0.6).set_fill(opacity=0.25), run_time=0.3)
        self.finish()


class S08Branch(SpokenScene):
    def construct(self):
        d = DGR(-0.9)
        nerve, cord = d.ctx()
        peri, cent, cell = d.peri_whole(), d.cent_whole(), d.cell()
        PALE = "#D5DAE3"
        ln = T("nerve", 28, SAGE).move_to([d.cx, -3.3, 0])
        lc = T("spinal cord", 28, GREY).move_to([d.cx, 3.5, 0])
        self.add(nerve, cord, peri, cent, cell, ln, lc)
        self.at("sensory neuron")
        sensory = lleft("sensory neuron", 3.2, 0.0, 30, BLUE)
        self.play(FadeIn(sensory), run_time=0.35)
        self.at("spinal ganglion")
        gang = Circle(radius=1.35, stroke_color=PALE, stroke_width=4.5, fill_opacity=0).move_to([d.sx, d.jy, 0])
        gl = lleft("spinal ganglion", 3.2, d.jy + 1.45, 28, PALE)
        ga = arr([3.2, d.jy + 1.3, 0], [d.sx + 1.0, d.jy + 0.95, 0], PALE, 4, 0.18)
        self.play(Create(gang), FadeIn(gl), GrowArrow(ga), run_time=0.8)
        self.at("one nucleus")
        nl = lleft("one nucleus", 3.2, d.jy - 1.3, 28, TEXT)
        na = arr([3.2, d.jy - 1.15, 0], [d.sx + 0.35, d.jy - 0.2, 0], TEXT, 4, 0.18)
        self.play(FadeIn(nl), GrowArrow(na), Indicate(cell[1].nuc, color=TEXT, scale_factor=1.3), run_time=0.8)
        self.at("two branches")
        bl = lright("branch in the nerve", -2.6, -1.75, 28, BLUE)
        ba = arr([-2.5, -1.75, 0], [d.cx - 0.3, -1.75, 0], BLUE, 4, 0.18)
        br = lright("branch in the cord", -2.6, 1.9, 28, BLUE)
        bb = arr([-2.5, 1.9, 0], [d.cx - 0.3, 1.9, 0], BLUE, 4, 0.18)
        self.play(FadeIn(bl), GrowArrow(ba), Indicate(peri, color=BLUE, scale_factor=1.05), run_time=0.6)
        self.play(FadeIn(br), GrowArrow(bb), Indicate(cent, color=BLUE, scale_factor=1.05), run_time=0.6)
        self.finish()


def two_panels():
    return DGR(-4.3), DGR(2.6)


def exp_labels():
    return (T("experiment 1", 28, GREY).move_to([-3.4, 3.45, 0]), T("experiment 2", 28, GREY).move_to([3.5, 3.45, 0]))


def prompt_which():
    return T("Which branch regrows?", 38, TEXT).move_to([0, -3.45, 0])


class S09Branchq(SpokenScene):
    def construct(self):
        d1, d2 = two_panels()
        n1, c1 = d1.ctx()
        n2, c2 = d2.ctx()
        p1, e1 = d1.peri_whole(), d1.cent_whole()
        p2, e2 = d2.peri_whole(), d2.cent_whole()
        t1, t2 = exp_labels()
        self.play(FadeIn(VGroup(n1, c1, p1, e1, d1.cell(), n2, c2, p2, e2, d2.cell())), FadeIn(t1), FadeIn(t2), run_time=0.5)
        self.at("each branch")
        pp, pd = d1.peri_pieces(0.0)
        self.remove(p1)
        self.add(pp, pd)
        m1 = d1.mark_p()
        self.play(pp.animate.shift(UP * 0.2), pd.animate.shift(DOWN * 0.2), FadeIn(m1), run_time=0.5)
        self.at("separate experiments")
        cp, cd = d2.cent_pieces(0.0)
        self.remove(e2)
        self.add(cp, cd)
        m2 = d2.mark_c()
        self.play(cp.animate.shift(DOWN * 0.2), cd.animate.shift(UP * 0.2), FadeIn(m2), run_time=0.5)
        self.at("which one regrows")
        self.play(FadeIn(qm(d1.cx + 1.4, d1.yp, 66), scale=0.6), FadeIn(qm(d2.cx + 1.4, d2.yc, 66), scale=0.6),
                  FadeIn(prompt_which()), run_time=0.5)
        self.finish()


def final_s09():
    """Both injuries made, question marks up. Returns the pieces by name so s11 can act on them."""
    d1, d2 = two_panels()
    n1, c1 = d1.ctx()
    n2, c2 = d2.ctx()
    pp, pd = d1.peri_pieces(0.2)
    cp, cd = d2.cent_pieces(0.2)
    P = dict(n1=n1, c1=c1, n2=n2, c2=c2, pp=pp, pd=pd, cp=cp, cd=cd, e1=d1.cent_whole(), p2=d2.peri_whole(),
             cell1=d1.cell(), cell2=d2.cell(), m1=d1.mark_p(), m2=d2.mark_c(),
             q1=qm(d1.cx + 1.4, d1.yp, 66), q2=qm(d2.cx + 1.4, d2.yc, 66), pr=prompt_which())
    P["t1"], P["t2"] = exp_labels()
    return d1, d2, P


class S10Pause(NarratedScene):
    def construct(self):
        d1, d2, P = final_s09()
        self.add(*P.values())
        self.finish()


def end_s11(d1, d2, P):
    """The s11 end state, as a dict of mobjects."""
    new = seg((d1.cx, d1.yp + 0.2), (d1.cx, d1.L + 0.3), d1.w, BLUE)
    tip = cone(d1.cx, d1.L + 0.3, s=0.8, ang=-PI / 2)
    stub = seg((d2.cx, d2.yc - 0.2), (d2.cx, d2.yc + 0.2), d2.w * 1.15, BLUE)
    bulb = Circle(radius=0.32, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.6).move_to([d2.cx, d2.yc + 0.12, 0])
    ban = T("same kind of neuron, different outcome", 32).move_to([0, 3.55, 0])
    brk = bracket(-4.9, 5.0, 3.18, GREY, 0.14, 4)
    return dict(n1=P["n1"], c1=P["c1"], n2=P["n2"], c2=P["c2"], pp=P["pp"], e1=P["e1"], p2=P["p2"], cp=P["cp"],
                cell1=P["cell1"], cell2=P["cell2"], new=new, tip=tip, stub=stub, bulb=bulb, ban=ban, brk=brk,
                cand=candidates())


class S11Branchr(SpokenScene):
    def construct(self):
        d1, d2, P = final_s09()
        self.add(*P.values())
        self.play(*[FadeOut(P[k]) for k in ("q1", "q2", "pr")], run_time=0.3)
        self.at("the branch in the nerve")
        self.play(Indicate(P["pp"], color=BLUE, scale_factor=1.05), run_time=0.7)
        self.at("regrows")
        new = seg((d1.cx, d1.yp + 0.2), (d1.cx, d1.yp + 0.1), d1.w, BLUE)
        tip = cone(d1.cx, d1.yp + 0.1, s=0.8, ang=-PI / 2)
        self.add(new, tip)
        self.play(FadeOut(P["pd"]), FadeOut(P["m1"]),
                  Transform(new, seg((d1.cx, d1.yp + 0.2), (d1.cx, d1.L + 0.3), d1.w, BLUE)),
                  tip.animate.move_to([d1.cx, d1.L + 0.3, 0]), run_time=1.3, rate_func=linear)
        self.at("the branch in the cord")
        self.play(Indicate(P["cp"], color=BLUE, scale_factor=1.05), run_time=0.7)
        self.at("mostly does not")
        stub = seg((d2.cx, d2.yc - 0.2), (d2.cx, d2.yc - 0.1), d2.w, BLUE)
        bulb = Circle(radius=0.32, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.6).move_to([d2.cx, d2.yc - 0.1, 0])
        self.add(stub, bulb)
        self.play(FadeOut(P["cd"]), FadeOut(P["m2"]), Transform(stub, seg((d2.cx, d2.yc - 0.2), (d2.cx, d2.yc + 0.2), d2.w * 1.15, BLUE)),
                  bulb.animate.move_to([d2.cx, d2.yc + 0.12, 0]), run_time=0.8)
        ban = T("same kind of neuron, different outcome", 32).move_to([0, 3.55, 0])
        brk = bracket(-4.9, 5.0, 3.18, GREY, 0.14, 4)
        self.at("same kind of neuron")
        self.play(FadeOut(P["t1"]), FadeOut(P["t2"]), run_time=0.2)
        self.play(FadeIn(ban, shift=DOWN * 0.1), Create(brk), run_time=0.7)
        cand = candidates()
        self.at("is it the tissue")
        self.play(FadeIn(cand), run_time=0.5)
        self.at("what each injury")
        self.wait(0.35)
        self.finish()


class S12Beat(NarratedScene):
    def construct(self):
        d1, d2, P = final_s09()
        E = end_s11(d1, d2, P)
        self.add(*E.values())
        self.add(veil(0.5))
        self.finish()


class S13Cond(SpokenScene):
    def construct(self):
        d = DGR(-1.0, cy=0.15, half=3.1, drop=2.2, r=1.0)
        nerve, cord = d.ctx()
        cand = candidates()
        ln = T("nerve", 28, SAGE).move_to([1.6, -2.2, 0])
        lc = T("spinal cord", 28, GREY).move_to([d.cx, 3.5, 0])
        peri, cent, cell = d.peri_whole(), d.cent_whole(), d.cell()
        self.add(nerve, cord, peri, cent, cell, ln, lc)
        self.at("nerve branch first")
        pp, pd = d.peri_pieces(0.0)
        self.remove(peri)
        self.add(pp, pd)
        m1 = d.mark_p(1.2)
        first = lright("first", -2.25, d.yp, 28, TEXT)
        self.play(pp.animate.shift(UP * 0.2), pd.animate.shift(DOWN * 0.2), FadeIn(m1), FadeIn(first), run_time=0.6)
        self.play(FadeOut(pd), run_time=0.2)
        # a visible gap in time, then the central cut
        arrow = arr([3.9, d.yp, 0], [3.9, d.yc, 0], GREY, 5)
        tlab = T("time passes", 28, GREY).move_to([5.25, (d.yp + d.yc) / 2, 0])
        self.play(GrowArrow(arrow), FadeIn(tlab), run_time=0.3)
        self.at("and the cord branch")
        cp, cd = d.cent_pieces(0.0)
        self.remove(cent)
        self.add(cp, cd)
        m2 = d.mark_c(1.2)
        later = lright("later", -2.25, d.yc, 28, TEXT)
        uy = d.yc
        usual = DashedLine([d.cx - 0.95, uy, 0], [d.cx + 0.95, uy, 0], color=GREY, stroke_width=3)
        ul = lleft("usual stub", 0.65, uy, 26, GREY)
        self.play(cp.animate.shift(DOWN * 0.2), cd.animate.shift(UP * 0.2), FadeIn(m2), FadeIn(later),
                  FadeIn(usual), FadeIn(ul), run_time=0.4)
        self.at("regrows better")
        newc = seg((d.cx, d.yc - 0.2), (d.cx, d.yc - 0.1), d.w, BLUE)
        tip = cone(d.cx, d.yc - 0.1, s=0.8, ang=PI / 2)
        self.add(newc, tip)
        self.play(FadeOut(cd),
                  Transform(newc, seg((d.cx, d.yc - 0.2), (d.cx, d.yc + 0.45), d.w, BLUE)),
                  tip.animate.move_to([d.cx, d.yc + 0.5, 0]), run_time=1.0, rate_func=linear)
        self.bring_to_front(m2)
        gl = VGroup(T("grows further than usual", 26, GOLD), T("(but still limited)", 26, GOLD)
                    ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        gl.move_to([1.0 + gl.width / 2, 2.55, 0])
        self.play(FadeIn(gl), run_time=0.4)
        self.at("conditioning lesion")
        cl = lright("conditioning lesion", -2.25, d.yp, 28, TEXT)
        self.play(FadeOut(first), FadeIn(cl), run_time=0.3)
        self.at("neuron's own state")
        self.play(Indicate(cell[1], color=BLUE, scale_factor=1.15), FadeIn(T("state matters", 34, TEXT).move_to([-3.3, -3.35, 0])), run_time=0.9)
        self.at("the tissue may too", lead=0.1)
        self.play(FadeIn(T("tissue may too", 34, TEXT).move_to([3.0, -3.35, 0])), Indicate(VGroup(nerve, cord), color=GREY, scale_factor=1.02), run_time=0.9)
        self.finish()


def s14_final():
    return heading("One cut, two fates"), idea_body(IDEA_Y, IDEA_S), idea_line1()


class S14Idea1(SpokenScene):
    def construct(self):
        s = IDEA_S
        sm = soma(-5.6, IDEA_Y, 0.95 * s)
        whole = seg((-5.6 + 0.95 * s * 0.9, IDEA_Y), (5.6, IDEA_Y), 0.8 * s, BLUE)
        intro = T("The cut-off piece", 40, TEXT).move_to([0, -2.65, 0])
        self.add(whole, sm, intro)
        self.at("the one idea")
        oi = T("the one idea", 52, TEXT, font=TITLE_FONT).move_to([0, -1.5, 0])
        self.play(FadeIn(oi, shift=UP * 0.1), run_time=0.6)
        hd = heading("One cut, two fates")
        self.at("one cut")
        cmk = cutmark(0.0, IDEA_Y, 1.9)
        self.play(FadeIn(hd, shift=DOWN * 0.1), FadeIn(cmk), run_time=0.6)
        self.at("two fates")
        a0 = seg((-5.6 + 0.95 * s * 0.9, IDEA_Y), (-0.0, IDEA_Y), 0.8 * s, BLUE)
        b0 = seg((0.0, IDEA_Y), (5.6, IDEA_Y), 0.8 * s, BLUE)
        self.remove(whole)
        self.add(a0, b0, sm)
        body = idea_body(IDEA_Y, s)
        self.play(Transform(a0, body[1]), Transform(b0, seg((0.3, IDEA_Y), (5.6, IDEA_Y), 0.8 * s, RED)), run_time=0.8)
        ln = idea_line1()
        self.at("cut off piece")
        self.play(FadeOut(oi), FadeOut(intro), run_time=0.15)
        self.play(FadeIn(ln[0], shift=UP * 0.1), run_time=0.6)
        self.at("destroys itself")
        self.play(ReplacementTransform(b0, body[2]), FadeOut(cmk), run_time=0.8)
        self.at("by a program")
        self.play(Create(body[3]), FadeIn(ln[1], shift=UP * 0.1), run_time=0.8)
        self.finish()


def s15_small():
    return idea_body(2.9, 0.6), idea_line1_small()


class S15Idea2(SpokenScene):
    def construct(self):
        hd, body, line1 = s14_final()
        self.add(hd, body, line1)
        self.at("attached piece")
        sbody, sline = s15_small()
        self.play(FadeOut(hd), ReplacementTransform(body, sbody), ReplacementTransform(line1, sline), run_time=0.6)
        body = sbody
        self.play(Indicate(body[1], color=BLUE, scale_factor=1.15), run_time=0.3)
        fr0, _, _ = idea_bal(0.0, False)
        self.at("tends to regrow")
        l2 = idea_line2()
        self.play(FadeIn(fr0), FadeIn(l2), run_time=0.7)
        fr, pl, pr = idea_bal(0.0)
        self.at("neurons drive")
        link0 = arr([-4.1, 2.55, 0], [-4.1, 0.1, 0], BLUE, 4, 0.2)
        self.play(FadeIn(pl), GrowArrow(link0), run_time=0.7)
        self.at("outweighs")
        self.play(Indicate(pl[1], color=GOLD, scale_factor=1.08), run_time=0.6)
        self.at("resistance of the")
        self.play(FadeIn(pr), run_time=0.3)
        frt, plt_, prt = idea_bal(0.16)
        link1 = arr([-4.1, 2.55, 0], [-4.1, -0.45, 0], BLUE, 4, 0.2)
        self.play(Transform(fr0, frt), Transform(pl, plt_), Transform(pr, prt), Transform(link0, link1),
                  run_time=0.6)
        self.at("tissue around")
        self.play(FadeIn(rule_note()), run_time=0.6)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        sbody, sline = s15_small()
        frt, plt_, prt = idea_bal(0.16)
        link1 = arr([-4.1, 2.55, 0], [-4.1, -0.45, 0], BLUE, 4, 0.2)
        g = VGroup(sbody, sline, frt, plt_, prt, link1, idea_line2(), rule_note())
        self.add(g, veil(0.5))
        self.finish()


class S17Take(SpokenScene):
    def construct(self):
        hd = heading("Two things to ask of any cut", 3.3, 40)

        def card(x):
            return RoundedRectangle(corner_radius=0.3, width=6.4, height=6.0, stroke_color=GREY, stroke_width=2.5,
                                    fill_color=GREY, fill_opacity=0.06).move_to([x, -0.35, 0])
        c1, c2 = card(-3.5), card(3.5)
        # left icon: the cut-off piece and its program
        i1 = VGroup(T("cut-off piece", 28, RED).move_to([-3.5, 2.1, 0]),
                    beads(-6.2, -0.8, 1.2, 0.9, 7, RED, 0.25), bracket(-6.2, -0.8, 0.55, GOLD, -0.2, 5))
        # right icon: the attached piece and the balance
        fr, le, re = beam_frame(3.5, 0.05, 1.8, 0.0)
        pl, pr = pan(le, "neuron’s\ndrive", GOLD, 26, 1.25), pan(re, "tissue’s\nresistance", RED, 26, 1.25)
        i2 = VGroup(T("attached piece", 28, BLUE).move_to([3.5, 2.1, 0]),
                    seg((0.9, 1.5), (6.1, 1.5), 0.7, BLUE), fr, pl, pr)
        self.add(hd, c1, c2, i1, i2)
        self.at("two things")
        self.wait(0.25)
        q1 = VGroup(T("What does the", 36), T("cut-off piece do?", 36)).arrange(DOWN, buff=0.12).move_to([-3.5, -2.65, 0])
        a1 = bchip("a program", GOLD, 36).move_to([-3.5, -0.45, 0])
        q2 = VGroup(T("At the attached piece,", 36), T("which side wins?", 36)).arrange(DOWN, buff=0.12).move_to([3.5, -2.65, 0])
        self.at("What does the cut off piece")
        self.play(FadeIn(q1, shift=UP * 0.1), FadeIn(a1), run_time=0.7)
        self.at("And at the attached piece")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.6)
        self.at("which side wins")
        # The closing question stays open: neither side is selected.
        self.wait(0.3)
        self.finish()


class S18End(EndCard):
    LINE = "Ask what the cut-off piece does, and which side wins."
