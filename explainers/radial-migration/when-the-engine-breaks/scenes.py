"""Radial migration, chapter 3: When the Engine Breaks  (Biochemistrypedia chaptered explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared with chapters 1 and 2)
  BLUE   = the migrating neuron (soma outline, leading process); also "neurons using the normal copy"
  ORANGE = the nucleus
  YELLOW = centrosome and Golgi
  GREEN  = radial glial fiber (the ladder)
  TEAL   = microtubules
  PURPLE = dynein, and LIS1 (its regulator; also NDEL1, the dynein regulator)
  PINK   = myosin II
  RED    = stalled / defective / mutant (mutant copy, stalled neurons, the question mark of a failure)
  GREY   = ventricle and outer surface, brain outlines, labels, de-emphasized
  GOLD   = doublecortin (DCX)
  PERIWINKLE = Cdk5 (kinase)
  Brain outlines: grey ring = grey matter (cortex), dark blue-grey inside = white matter
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E87FB0"
CDK = "#8FA8FF"           # Cdk5, the kinase
NEURON_FILL = "#16303c"   # BLUE at about 25 percent over the background, but opaque
WM = "#222838"            # white matter


# ---------------------------------------------------------------------------------------------
# helpers shared with the earlier chapters
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def lab_left(text, color, x, y, tip, size=26):
    """text whose right edge sits at x, with an arrow to `tip`."""
    t = T(text, size, color)
    t.move_to([x - t.width / 2, y, 0])
    a = arr([x + 0.12, y, 0], tip, color)
    return VGroup(t, a)


def lab_right(text, color, x, y, tip, size=26):
    """text whose left edge sits at x, with an arrow to `tip`."""
    t = T(text, size, color)
    t.move_to([x + t.width / 2, y, 0])
    a = arr([x - 0.12, y, 0], tip, color)
    return VGroup(t, a)


def bar(y, x0=-2.6, x1=2.6):
    return RoundedRectangle(corner_radius=0.08, width=x1 - x0, height=0.2, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.45).move_to([(x0 + x1) / 2, y, 0])


def fiber(x, y0=-3.0, y1=3.0, rungs=False, width=5):
    g = VGroup(Line([x, y0, 0], [x, y1, 0], color=GREEN, stroke_width=width))
    if rungs:
        for y in np.arange(y0 + 0.2, y1, 0.6):
            g.add(Line([x - 0.14, y, 0], [x + 0.14, y, 0], color=GREEN, stroke_width=2.5, stroke_opacity=0.7))
    return g


def chipfix(text, color, size=26):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def ring(pos, color, r=0.34):
    return Circle(radius=r, stroke_color=color, stroke_width=5).move_to(pos)


def tag(text, size=24, color=GREY, **kw):
    """label with an opaque backing so lines behind it do not run through the letters."""
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.1, stroke_width=0, fill_color=BG,
                     fill_opacity=0.9).move_to(t)
    return VGroup(back, t)


def left_text(text, size, color, x, y, **kw):
    t = T(text, size, color, **kw)
    return t.move_to([x + t.width / 2, y, 0])


def right_text(text, size, color, x, y, **kw):
    t = T(text, size, color, **kw)
    return t.move_to([x - t.width / 2, y, 0])


class Cell:
    """A migrating neuron drawn from a few trackers (local y, scaled by sc, placed at x, y0)."""
    RX, RY = 0.55, 0.7   # soma half-width and half-height

    def __init__(self, x=0.0, y0=0.0, sc=1.0, soma=-2.4, tip=-0.4, tail=-3.35, ws=0.0, wy=-0.4,
                 cs=-1.45, op=0.0, cs_op=0.0, gg_op=0.0, nuc_op=1.0):
        self.x, self.y0, self.sc = x, y0, sc
        self.t = {k: ValueTracker(v) for k, v in dict(soma=soma, tip=tip, tail=tail, ws=ws, wy=wy, cs=cs,
                                                      op=op, cs_op=cs_op, gg_op=gg_op, nuc_op=nuc_op).items()}
        self.mob = always_redraw(self.build)

    def P(self, x, y):
        return np.array([self.x + self.sc * x, self.y0 + self.sc * y, 0.0])

    def v(self, k):
        return self.t[k].get_value()

    def set(self, **kw):
        for k, val in kw.items():
            self.t[k].set_value(val)

    def to(self, **kw):
        return [self.t[k].animate.set_value(val) for k, val in kw.items()]

    def build(self):
        sc = self.sc
        op = self.v("op")
        if op < 0.02:
            return VGroup()
        soma, tip, tail = self.v("soma"), self.v("tip"), self.v("tail")
        ws, wy, cs = self.v("ws"), self.v("wy"), self.v("cs")
        lw = 10 * sc
        g = VGroup()
        if tail < soma - self.RY - 0.02:
            g.add(Line(self.P(0, tail), self.P(0, soma - self.RY), color=BLUE, stroke_width=lw))
            g.add(Dot(self.P(0, tail), radius=0.09 * sc, color=BLUE))
        if tip > soma + self.RY + 0.02:
            g.add(Line(self.P(0, soma + self.RY), self.P(0, tip), color=BLUE, stroke_width=lw))
            g.add(Dot(self.P(0, tip), radius=0.13 * sc, color=BLUE))
        if ws > 0.03:
            g.add(Ellipse(width=1.0 * ws * sc, height=2.0 * ws * sc, stroke_color=BLUE, stroke_width=5 * sc,
                          fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, wy)))
        g.add(Ellipse(width=2 * self.RX * sc, height=2 * self.RY * sc, stroke_color=BLUE, stroke_width=5 * sc,
                      fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, soma)))
        g.add(Ellipse(width=0.74 * sc, height=1.0 * sc, stroke_color=ORANGE, stroke_width=4 * sc,
                      fill_color=ORANGE, fill_opacity=0.55 * self.v("nuc_op")).set_stroke(opacity=self.v("nuc_op"))
              .move_to(self.P(0, soma)))
        cso, ggo = self.v("cs_op"), self.v("gg_op")
        if cso > 0.02:
            g.add(Dot(self.P(0, cs), radius=0.11 * sc, color=YELLOW).set_opacity(cso))
        if ggo > 0.02:
            for dy in (0.30, 0.42, 0.54):
                g.add(Line(self.P(-0.2, cs + dy), self.P(0.2, cs + dy), color=YELLOW,
                           stroke_width=max(2.5, 5 * sc), stroke_opacity=ggo))
        if op < 0.99:
            for m in g.family_members_with_points():
                m.set_stroke(opacity=m.get_stroke_opacity() * op)
                m.set_fill(opacity=m.get_fill_opacity() * op)
        return g

    def stroke_one(self, soma):
        """leading process extends, swelling forms ahead of the nucleus, centrosome and Golgi move in."""
        return dict(tip=soma + 3.5, ws=1.0, wy=soma + 2.0, cs=soma + 2.35)

    def stroke_two(self, soma):
        return dict(soma=soma + 1.5, ws=0.0, tail=soma + 1.5 - 0.95)


class Multi:
    """A multipolar neuron: the same soma and nucleus as Cell, with several short processes (lengths in
    soma units, scaled by sc). Position and lengths are trackers so they can extend, retract and drift."""
    RX, RY = 0.55, 0.7
    ANG = [90, 30, 150, 210, 330, 270]

    def __init__(self, x=0.0, y=0.0, sc=1.0, L=None, op=1.0):
        self.sc = sc
        self.px, self.py, self.op = ValueTracker(x), ValueTracker(y), ValueTracker(op)
        self.L = [ValueTracker(v) for v in (L or [0.0] * 6)]
        self.mob = always_redraw(self.build)

    def pos(self):
        return np.array([self.px.get_value(), self.py.get_value(), 0.0])

    def build(self):
        o = self.op.get_value()
        if o < 0.02:
            return VGroup()
        c, sc = self.pos(), self.sc
        g = VGroup()
        for t, a in zip(self.L, self.ANG):
            ln = t.get_value()
            if ln > 0.04:
                d = np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0.0])
                e = c + d * ln * sc
                g.add(Line(c, e, color=BLUE, stroke_width=10 * sc))
                g.add(Dot(e, radius=0.1 * sc, color=BLUE))
        g.add(Ellipse(width=2 * self.RX * sc, height=2 * self.RY * sc, stroke_color=BLUE, stroke_width=5 * sc,
                      fill_color=NEURON_FILL, fill_opacity=1).move_to(c).set_z_index(2))
        g.add(Ellipse(width=0.74 * sc, height=1.0 * sc, stroke_color=ORANGE, stroke_width=4 * sc,
                      fill_color=ORANGE, fill_opacity=0.55).move_to(c).set_z_index(3))
        if o < 0.99:
            for m in g.family_members_with_points():
                m.set_stroke(opacity=m.get_stroke_opacity() * o)
                m.set_fill(opacity=m.get_fill_opacity() * o)
        return g

    def to(self, x=None, y=None, L=None, op=None):
        anims = []
        if x is not None:
            anims.append(self.px.animate.set_value(x))
        if y is not None:
            anims.append(self.py.animate.set_value(y))
        if op is not None:
            anims.append(self.op.animate.set_value(op))
        for i, v in (L or {}).items():
            anims.append(self.L[i].animate.set_value(v))
        return anims




# ---------------------------------------------------------------------------------------------
# more helpers (fix round)
# ---------------------------------------------------------------------------------------------
def chip2(lines, color, size=28, pad=0.22):
    """a chip with two or more stacked lines of text and an opaque backing."""
    labs = VGroup(*[T(s, size, color) for s in lines]).arrange(DOWN, buff=0.1)
    w, h = labs.width + 2 * pad, labs.height + 2 * pad
    back = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_width=0, fill_color=BG, fill_opacity=1)
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.16)
    labs.move_to(box)
    return VGroup(back, box, labs)


def stack(lines, size, color, x, y, align=LEFT, weight=NORMAL):
    """lines of text stacked and aligned; x is the left edge (align LEFT) or the centre (align ORIGIN)."""
    g = VGroup(*[T(s, size, color, weight=weight) for s in lines]).arrange(DOWN, buff=0.1, aligned_edge=align)
    if np.allclose(align, LEFT):
        g.move_to([x + g.width / 2, y, 0])
    else:
        g.move_to([x, y, 0])
    return g


def lab_right_lines(lines, color, x, y, tip, size=26):
    g = stack(lines, size, color, x, y)
    a = arr([x - 0.12, y, 0], tip, color)
    return VGroup(g, a)


# ---------------------------------------------------------------------------------------------
# brain outlines (schematic)
# ---------------------------------------------------------------------------------------------
class Brain:
    """A coronal-slice outline. amp > 0 gives folds (rounded gyri, sharp sulci); thick = cortex thickness
    as a fraction of the radius. Points inside are addressed by (angle, fraction of the outer radius)."""

    def __init__(self, cx, cy, a, b, amp=0.0, n=14, thick=0.2, steps=240):
        self.cx, self.cy, self.a, self.b, self.amp, self.n, self.thick = cx, cy, a, b, amp, n, thick
        self.th = np.linspace(0, 2 * np.pi, steps, endpoint=False)

    def wob(self, th):
        th = np.asarray(th, dtype=float)
        if self.amp == 0:
            return np.ones_like(th)
        return 1 + self.amp * (2 * np.abs(np.sin(self.n * th / 2)) - 1)

    def pt(self, th, f=1.0):
        w = self.wob(th)
        return np.array([self.cx + f * self.a * np.cos(th) * w, self.cy + f * self.b * np.sin(th) * w, 0.0])

    def poly(self, f, **kw):
        return Polygon(*[self.pt(t, f) for t in self.th], **kw)

    def shape(self):
        outer = self.poly(1.0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.55)
        inner = self.poly(1 - self.thick, stroke_color=GREY, stroke_width=2, stroke_opacity=0.6, fill_color=WM,
                          fill_opacity=1)
        return VGroup(outer, inner)

    def layers(self, k=2):
        return VGroup(*[self.poly(1 - self.thick * (i + 1) / (k + 1), stroke_color=TEXT, stroke_width=3,
                                  stroke_opacity=0.6, fill_opacity=0) for i in range(k)])

    def shuffled(self, k=3, seed=3, lo=0.07):
        """the same k bands, broken into arcs that sit at the wrong depth: shuffled layers."""
        rs = np.random.RandomState(seed)
        g = VGroup()
        for _ in range(k):
            t = rs.uniform(0, 0.5)
            while t < 2 * np.pi:
                span = rs.uniform(0.25, 0.6)
                t1 = min(t + span, 2 * np.pi)
                f = rs.uniform(1 - self.thick + lo, 1 - lo * 0.8)
                ths = np.linspace(t, t1, 14)
                m = VMobject(stroke_color=TEXT, stroke_width=5, stroke_opacity=0.95)
                m.set_points_as_corners([self.pt(x, f) for x in ths])
                g.add(m)
                t = t1 + rs.uniform(0.05, 0.22)
        return g


# ---------------------------------------------------------------------------------------------
# chromosomes
# ---------------------------------------------------------------------------------------------
def xchrom(cx, cy, h=4.2, w=0.5, col=GREY, fo=0.4, sw=3):
    mk = lambda ang: RoundedRectangle(corner_radius=w / 2, width=w, height=h, stroke_color=col, stroke_width=sw,
                                      fill_color=col, fill_opacity=fo).rotate(ang)
    return VGroup(mk(0.33), mk(-0.33)).move_to([cx, cy, 0])


def x_band_pos(cx, cy, h, t=-0.6):
    """a point along the first arm of xchrom (t from -1 bottom to 1 top)."""
    d = np.array([-np.sin(0.33), np.cos(0.33), 0.0])
    return np.array([cx, cy, 0.0]) + t * (h / 2) * d


def x_band(cx, cy, h, w, color=GOLD, t=-0.6):
    p = x_band_pos(cx, cy, h, t)
    return Rectangle(width=w + 0.18, height=0.2, stroke_width=0, fill_color=color, fill_opacity=0.95).rotate(0.33).move_to(p)


CH_W = 0.8
CH_TOP, CH_P, CH_Q = 3.0, 2.5, 3.62


def chr17(cx):
    """chromosome 17: short p arm on top, long q arm below, joined at the centromere."""
    p = RoundedRectangle(corner_radius=CH_W / 2, width=CH_W, height=CH_P, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.35).move_to([cx, CH_TOP - CH_P / 2, 0])
    q = RoundedRectangle(corner_radius=CH_W / 2, width=CH_W, height=CH_Q, stroke_color=GREY, stroke_width=3,
                         fill_color=GREY, fill_opacity=0.35).move_to([cx, CH_TOP - CH_P + 0.12 - CH_Q / 2, 0])
    return VGroup(p, q)


BAND_Y = 2.42
TICK_Y = [1.98, 1.64, 1.3]


def band17(cx):
    return Rectangle(width=CH_W, height=0.26, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95).move_to(
        [cx, BAND_Y, 0])


def ticks17(cx):
    return VGroup(*[Rectangle(width=0.5, height=0.07, stroke_width=0, fill_color=TEXT, fill_opacity=0.8).move_to(
        [cx, y, 0]) for y in TICK_Y])


def gap_rect(cx, y0, y1):
    return Rectangle(width=CH_W + 0.3, height=y1 - y0, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(
        [cx, (y0 + y1) / 2, 0])


def gap_dash(cx, y0, y1):
    return DashedVMobject(Rectangle(width=CH_W + 0.3, height=y1 - y0, stroke_color=RED, stroke_width=3.5).move_to(
        [cx, (y0 + y1) / 2, 0]), num_dashes=28)


CX_L, CX_R = -1.6, 1.6   # the two copies of chromosome 17 (centred)
MD_POS = np.array([4.35, -0.2, 0.0])


def md_chip():
    return chip2(["Miller-Dieker", "lissencephaly"], RED, 30).move_to(MD_POS)


def md_arrow(y_end):
    return arr(MD_POS + np.array([-0.9, 0.75, 0]), [CX_R + 0.5, y_end, 0], RED, w=5)


def lis_left_labels():
    return VGroup(lab_left("17p13.3", GREY, CX_L - 0.95, BAND_Y + 0.4, [CX_L - 0.45, BAND_Y + 0.08, 0]),
                  lab_left("LIS1", PURPLE, CX_L - 0.95, BAND_Y - 0.35, [CX_L - 0.45, BAND_Y - 0.05, 0], size=30))


# ---------------------------------------------------------------------------------------------
# the wall (zoomed, used in chapter 3 s14 to s19). Labels sit in the column right of the wall.
# ---------------------------------------------------------------------------------------------
WX0, WX1 = -5.5, 2.4
COLX = WX1 + 0.3
CELL_X = -2.6
FIBS = (-4.9, 1.8)
ZZ = dict(vz=(-3.3, -0.6), svz=(-0.6, 2.1), iz=(2.1, 3.4))                    # zoomed on the lower wall
ZF = dict(vz=(-3.3, -1.9), svz=(-1.9, -0.4), iz=(-0.4, 2.1), cp=(2.1, 3.3))   # the whole wall
ZOP = dict(vz=0.18, svz=0.10, iz=0.0, cp=0.24)


def wallw(zones, top_bar=True, fibs=FIBS, extra_fibs=()):
    g, z = VGroup(), {}
    for key, (y0, y1) in zones.items():
        r = Rectangle(width=WX1 - WX0, height=y1 - y0, stroke_width=0, fill_color=GREY,
                      fill_opacity=ZOP[key]).move_to([(WX0 + WX1) / 2, (y0 + y1) / 2, 0])
        z[key] = r
        g.add(r)
    for x in tuple(fibs) + tuple(extra_fibs):
        g.add(Line([x, -3.3, 0], [x, 3.4 if not top_bar else 3.3, 0], color=GREEN, stroke_width=4, stroke_opacity=0.55))
    g.add(bar(-3.4, WX0, WX1))
    if top_bar:
        g.add(bar(3.4, WX0, WX1))
    return g, z


def zl(text, y, color=GREY, size=26):
    return left_text(text, size, color, COLX, y)


# ---------------------------------------------------------------------------------------------
# chapter frames that a later silent scene rebuilds exactly
# ---------------------------------------------------------------------------------------------
GIRL_X = -5.3
XN_X, XM_X, XPAIR_Y = -3.5, -2.2, 0.75
CELLS = [(0.3, 0.55), (2.7, 0.55), (5.1, 0.55)]
OFF = [0, 1, 0]   # which X each cell switches off: normal, mutant, normal
CELL_R = 1.1


def girl(cx=GIRL_X, cy=0.5):
    head = Circle(radius=0.48, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25).move_to(
        [cx, cy + 1.25, 0])
    body = Polygon([cx, cy + 0.65, 0], [cx - 0.85, cy - 1.35, 0], [cx + 0.85, cy - 1.35, 0], stroke_color=TEXT,
                   stroke_width=3, fill_color=TEXT, fill_opacity=0.25)
    return VGroup(head, body).scale(1.15, about_point=np.array([cx, cy, 0.0]))


def mini_x_cell(cx, cy):
    """a cell holding two X chromosomes (normal on the left, mutant on the right)."""
    cell = Circle(radius=CELL_R, stroke_color=GREY, stroke_width=3, fill_color=NEURON_FILL, fill_opacity=1).move_to(
        [cx, cy, 0])
    xn = xchrom(cx - 0.42, cy, h=1.75, w=0.3, col=GREY)
    xm = xchrom(cx + 0.42, cy, h=1.75, w=0.3, col=RED)
    return cell, xn, xm


def off_cross(x_mob):
    """a clear cross over the switched-off X."""
    c = x_mob.get_center()
    return VGroup(Line(c + [-0.3, -0.5, 0], c + [0.3, 0.5, 0], color=TEXT, stroke_width=6),
                  Line(c + [-0.3, 0.5, 0], c + [0.3, -0.5, 0], color=TEXT, stroke_width=6))


def predict_parts():
    p = {}
    p["girl"] = girl()
    p["xn"] = xchrom(XN_X, XPAIR_Y, h=3.0, w=0.45, col=GREY)
    p["xm"] = xchrom(XM_X, XPAIR_Y, h=3.0, w=0.45, col=RED)
    p["mut_l"] = VGroup(T("one mutant copy", 26, RED).move_to([XM_X - 0.6, -1.95, 0]),
                        arr([XM_X, -1.7, 0], [XM_X, -1.0, 0], RED, w=4)).set_z_index(1)
    p["cells"] = [mini_x_cell(cx, cy) for (cx, cy) in CELLS]
    p["crosses"] = [off_cross(c[1] if OFF[i] == 0 else c[2]) for i, c in enumerate(p["cells"])]
    p["caps"] = [T("one X off", 26, GREY).move_to([cx, cy - CELL_R - 0.4, 0]) for (cx, cy) in CELLS]
    p["cap"] = T("Pause and predict", 38, TEAL, weight=BOLD).move_to([0.6, 3.1, 0])
    p["q"] = T("What would her cortex look like?", 36, TEXT).move_to([0.6, -2.9, 0])
    return p


def band_brain():
    return Brain(-2.9, 0.0, 2.5, 2.9, amp=0.05, n=14, thick=0.13)


def band_frame():
    """final frame of s11 (rebuilt by s12)."""
    b = band_brain()
    panel = RoundedRectangle(corner_radius=0.2, width=6.2, height=7.0, stroke_color=GREY, stroke_width=3,
                             fill_color="#0a0c11", fill_opacity=1).move_to([-2.9, 0, 0])
    shp = b.shape()
    bo = b.poly(0.72, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55)
    bi = b.poly(0.56, stroke_color=GREY, stroke_width=2, stroke_opacity=0.6, fill_color=WM, fill_opacity=1)
    l1 = lab_right("cortex", TEXT, 1.1, 2.6, b.pt(np.radians(60), 0.93))
    l2 = lab_right("grey matter band", TEXT, 1.1, 1.3, b.pt(np.radians(30), 0.64))
    sub = VGroup(T("subcortical band", 30, TEXT), T("heterotopia", 30, TEXT)).arrange(DOWN, buff=0.12,
                                                                                        aligned_edge=LEFT)
    sub.move_to([1.0 + sub.width / 2, -0.3, 0])
    dbl = left_text("double cortex", 44, TEXT, 1.0, -1.6, weight=BOLD)
    sch = T("schematic", 22, GREY).move_to([5.7, -3.45, 0])
    return VGroup(panel, shp, bo, bi, l1, l2, sub, dbl, sch)


# the bipolar cell in the whole wall (s17 to s19)
BSC = 1.65


def bip_cell(**kw):
    args = dict(x=CELL_X, y0=0.0, sc=BSC, soma=-1.1 / BSC, tip=0.45, tail=-1.45, op=1.0)
    args.update(kw)
    return Cell(**args)


def s18_cell():
    return bip_cell(soma=0.3, tip=1.8, tail=-0.65, cs_op=1, cs=1.45)


def s18_static():
    """One neuron and one nucleus-centred stall marker, shared with the pause."""
    g, _ = wallw(ZF, extra_fibs=(CELL_X + 0.5,))
    c = s18_cell()
    return dict(wall=g,
                lis=chipfix("LIS1", PURPLE, 34).move_to([0.25, 1.2, 0]),
                turn=stack(["multipolar-to-bipolar", "turn"], 28, TEXT, -0.3, -0.25),
                climb=stack(["two-stroke", "climb"], 30, TEXT, -0.3, -0.25),
                halo=ring(c.P(0, 0.3), RED, 1.1),
                stall=tag("stall", 30, RED).move_to([-4.6, 0.5, 0]))


def stroke_chips(x=3.9, y1=2.45, y2=1.15):
    c1 = chip2(["stroke 1:", "leading process extends"], GREY, 26).move_to([x, y1, 0])
    c2 = chip2(["stroke 2:", "nucleus catches up"], GREY, 26).move_to([x, y2, 0])
    return c1, c2


def lit(c, on):
    col = TEXT if on else GREY
    return [c[1].animate.set_stroke(col).set_fill(col, 0.16), c[2].animate.set_color(col)]


def mini(x, y, col=BLUE, proc=0.7, tail=0.4, s=1.0):
    """a small stalled-neuron icon: leading process, soma, nucleus, short tail (scaled about its soma)."""
    g = VGroup()
    g.add(Line([x, y + 0.3, 0], [x, y + 0.3 + proc, 0], color=col, stroke_width=7))
    g.add(Dot([x, y + 0.3 + proc, 0], radius=0.09, color=col))
    g.add(Line([x, y - 0.3, 0], [x, y - 0.3 - tail, 0], color=col, stroke_width=7))
    g.add(Ellipse(width=0.62, height=0.8, stroke_color=col, stroke_width=4, fill_color=NEURON_FILL,
                  fill_opacity=1).move_to([x, y, 0]))
    g.add(Ellipse(width=0.4, height=0.54, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                  fill_opacity=0.55).move_to([x, y, 0]))
    return g.scale(s, about_point=np.array([x, y, 0.0]))


def recolor_mini(g, col):
    return [g[0].animate.set_color(col), g[1].animate.set_color(col), g[2].animate.set_color(col),
            g[3].animate.set_stroke(col)]


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Radial Migration: Climbing the Glial Ladder"
    TITLE = "When the Engine Breaks"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """a neuron whose front keeps reaching while its nucleus stays low in the wall."""

    def construct(self):
        sc = 1.6
        vent, outer = bar(-3.4, -4.8, 4.8), bar(3.4, -4.8, 4.8)
        fib = fiber(-0.2 + 0.5 * sc, -3.3, 3.3, width=6)
        cell = Cell(x=-0.2, y0=-0.4, sc=sc, soma=-1.0, tip=0.35, tail=-1.55, op=0)
        self.add(cell.mob)
        sch = T("schematic", 24, GREY).move_to([5.3, -3.45, 0])
        self.play(FadeIn(vent), FadeIn(outer), Create(fib), cell.t["op"].animate.set_value(1), FadeIn(sch),
                  run_time=0.7)
        self.at("when the")
        self.play(*cell.to(tip=1.5), run_time=1.5)
        self.at("nucleus")
        nuc_l = lab_left("nucleus", ORANGE, -1.5, cell.P(0, -1.0)[1], [-0.9, cell.P(0, -1.0)[1], 0], size=30)
        halo = Ellipse(width=1.6, height=2.0, stroke_color=ORANGE, stroke_width=4).move_to(cell.P(0, -1.0))
        self.play(FadeIn(nuc_l), Create(halo), run_time=0.5)
        self.at("catch up")
        qm = T("?", 90, RED, weight=BOLD).move_to([-0.2 + 0.0, 2.85, 0])
        self.play(FadeIn(qm, scale=0.6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Stall(SpokenScene):
    """many neurons stopped at different depths of the wall, short of the cortical plate."""

    XS = [-5.4, -3.6, -1.8, 0.0, 1.8, 3.6, 5.4]
    AFTER = [-2.1, -0.7, -1.5, -0.3, -1.1, -1.9, -0.6]
    S = 1.2

    def construct(self):
        plate = Rectangle(width=12.4, height=0.9, stroke_width=0, fill_color=GREY, fill_opacity=0.22).move_to(
            [0, 2.75, 0])
        fibs = VGroup(*[Line([x, -3.3, 0], [x, 3.2, 0], color=GREEN, stroke_width=4, stroke_opacity=0.55)
                        for x in self.XS])
        vent = bar(-3.4, -6.2, 6.2)
        vent_l = tag("ventricle", 24, GREY).move_to([-5.45, -3.0, 0])
        plate_l = tag("cortical plate", 26, GREY).move_to([4.6, 2.75, 0])
        cells = [mini(x, -2.35, s=self.S) for x in self.XS]
        self.add(plate, fibs, vent, vent_l, plate_l)
        self.add(*cells)
        self.at("Disrupt that machinery")
        dy = chip2(["dynein pull disrupted"], PURPLE, 28).move_to([-3.0, 1.5, 0])
        self.play(FadeIn(dy, scale=0.8), run_time=0.5)
        self.play(Indicate(dy, color=PURPLE, scale_factor=1.08), run_time=0.5)
        self.at("neurons can")
        self.play(*[c.animate.shift(UP * (y + 2.35 - 0.35)) for c, y in zip(cells, self.AFTER)],
                  run_time=0.85)
        self.at("stall")
        self.play(*[c.animate.shift(UP * 0.35) for c in cells], run_time=0.25)
        self.play(*[a for c in cells for a in recolor_mini(c, RED)], run_time=0.25)
        self.at("short of")
        gap = DoubleArrow([0.9, 1.2, 0], [0.9, 2.28, 0], color=RED, stroke_width=4, tip_length=0.2, buff=0)
        gl = T("short", 28, RED).move_to([1.55, 1.75, 0])
        self.play(GrowFromCenter(gap), FadeIn(gl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Liss(SpokenScene):
    """a folded cortex beside a smooth, thick one."""

    def construct(self):
        L = Brain(-3.5, 0.3, 2.7, 2.6, amp=0.07, n=14, thick=0.14)
        R = Brain(3.5, 0.3, 2.7, 2.6, amp=0.0, thick=0.40)
        Ls, Rs = L.shape(), R.shape()
        lay = L.layers(2)
        l_l = T("folded cortex", 28, GREY).move_to([-3.5, -2.8, 0])
        self.play(FadeIn(Ls), FadeIn(lay), FadeIn(l_l), run_time=0.9)
        self.at("can be")
        r_l = T("lissencephaly", 36, TEXT, weight=BOLD).move_to([3.5, -2.75, 0])
        self.play(FadeIn(Rs), run_time=0.6)
        self.play(FadeIn(r_l, shift=UP * 0.1), run_time=0.4)
        self.at("reduced or absent")
        sub = T("reduced or absent folding", 26, GREY).move_to([3.5, -3.3, 0])
        self.play(FadeIn(sub, shift=UP * 0.1), Indicate(Rs[0], color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("also thick")
        p_in, p_out = R.pt(np.pi / 2, 1 - R.thick), R.pt(np.pi / 2, 1.0)
        dbl = DoubleArrow(p_in, p_out, color=TEXT, stroke_width=6, tip_length=0.22, buff=0)
        th_l = tag("thick cortex", 30, TEXT).move_to([p_out[0], p_out[1] + 0.45, 0])
        self.play(GrowFromCenter(dbl), FadeIn(th_l), run_time=0.7)
        self.at("poorly layered")
        jb = R.shuffled(k=3, seed=5, lo=0.09)
        pl = T("poorly layered", 30, TEXT).move_to([3.5, -0.3, 0])
        pa = arr([3.5, -0.7, 0], R.pt(-np.pi / 2, 0.8), TEXT, w=4)
        self.play(FadeIn(jb), FadeIn(pl), FadeIn(pa), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Lis1(SpokenScene):
    """two copies of chromosome 17; one loses the LIS1 band."""

    def construct(self):
        cl, cr = chr17(CX_L), chr17(CX_R)
        bl, br = band17(CX_L), band17(CX_R)
        c_l = T("chromosome 17", 26, GREY).move_to([0, -3.55, 0])
        self.play(Create(cl), Create(cr), FadeIn(c_l), run_time=1.0)
        self.add(bl, br)
        self.play(FadeIn(bl), FadeIn(br), run_time=0.4)
        self.at("of l i s one")
        right_l = lab_right("LIS1", PURPLE, CX_R + 0.95, BAND_Y - 0.35, [CX_R + 0.45, BAND_Y - 0.05, 0], size=30)
        self.play(FadeIn(lis_left_labels()), FadeIn(right_l), run_time=0.5)
        self.at("enough to cause")
        gap, dash = gap_rect(CX_R, 2.27, 2.57), gap_dash(CX_R, 2.27, 2.57)
        lost = lab_right_lines(["one copy lost", "is enough"], RED, CX_R + 0.95, BAND_Y + 0.1,
                               [CX_R + 0.62, BAND_Y, 0])
        self.play(FadeOut(br), FadeIn(gap), Create(dash), FadeOut(right_l), run_time=0.6)
        self.play(FadeIn(lost), run_time=0.5)
        self.at("Miller")
        md = md_chip()
        ma = md_arrow(1.9)
        self.play(FadeIn(md, shift=UP * 0.1), GrowArrow(ma), run_time=0.7)
        self.finish()


class S05Md(SpokenScene):
    """the deleted segment widens over the neighbouring genes."""

    def construct(self):
        cl, cr = chr17(CX_L), chr17(CX_R)
        bl = band17(CX_L)
        tl, tr = ticks17(CX_L), ticks17(CX_R)
        gap, dash = gap_rect(CX_R, 2.27, 2.57), gap_dash(CX_R, 2.27, 2.57)
        c_l = T("chromosome 17", 26, GREY).move_to([0, -3.55, 0])
        md, ma = md_chip(), md_arrow(1.9)
        self.add(cl, cr, bl, c_l, lis_left_labels(), md, ma, tl, tr, gap, dash)
        self.wait(0.3)
        self.at("also removes")
        gap2, dash2 = gap_rect(CX_R, 1.0, 2.57), gap_dash(CX_R, 1.0, 2.57)
        ghosts = VGroup(*[Rectangle(width=0.5, height=0.07, stroke_width=0, fill_color=RED, fill_opacity=0.7)
                          .move_to([CX_R, y, 0]) for y in TICK_Y])
        self.play(Transform(gap, gap2), Transform(dash, dash2), Transform(ma, md_arrow(0.95)), run_time=1.1)
        self.add(ghosts)
        self.play(FadeIn(ghosts), run_time=0.3)
        self.at("neighboring genes")
        br_ = Brace(ghosts, direction=RIGHT, buff=0.5, color=GREY)
        ng = stack(["neighbouring", "genes"], 26, GREY, 2.75, 1.64)
        yt = T("YWHAE", 28, TEXT).move_to([-0.1, TICK_Y[1], 0])
        yw = VGroup(yt, arr([yt.get_right()[0] + 0.1, TICK_Y[1], 0], [CX_R - 0.42, TICK_Y[1], 0], TEXT))
        self.play(FadeIn(br_), FadeIn(ng), run_time=0.5)
        self.play(FadeIn(yw), run_time=0.5)
        self.at("more severe")
        ta = T("LIS1 loss alone", 26, TEXT).move_to([2.8 + 1.3, -1.3, 0])
        ta.align_to([2.8, 0, 0], LEFT)
        tb = T("LIS1 + neighbours", 26, TEXT)
        tb.move_to([2.8 + tb.width / 2, -2.2, 0])
        ba = Rectangle(width=1.0, height=0.3, stroke_width=0, fill_color=RED, fill_opacity=0.55).move_to(
            [2.8 + 0.5, -1.7, 0])
        bb = Rectangle(width=3.0, height=0.3, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to(
            [2.8 + 1.5, -2.6, 0])
        sev = T("more severe", 30, RED, weight=BOLD).move_to([2.8 + 1.1, -3.2, 0])
        self.play(FadeIn(ta), FadeIn(ba), FadeIn(tb), run_time=0.4)
        self.play(GrowFromEdge(bb, LEFT), FadeIn(sev, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Mouse(SpokenScene):
    """a smooth mouse cortex with disordered layers; what you measure in mice."""

    def construct(self):
        B = Brain(-2.6, 0.2, 3.2, 3.0, amp=0.0, thick=0.26)
        shp, lay = B.shape(), B.layers(3)
        self.play(FadeIn(shp), FadeIn(lay), run_time=0.9)
        self.at("smooth")
        sm = stack(["mouse cortex:", "smooth to begin with"], 28, GREY, 1.3, 2.5)
        self.play(FadeIn(sm, shift=UP * 0.1), run_time=0.6)
        self.at("in mice")
        nl = VGroup(T("normal layers", 28, TEXT).move_to([1.3 + 1.45, 1.1, 0]),
                    arr([1.2, 1.1, 0], B.pt(np.radians(8), 0.87), TEXT, w=4))
        self.play(FadeIn(nl), run_time=0.6)
        self.at("migration speed")
        c1 = chipfix("migration speed", BLUE, 30)
        c1.move_to([1.3 + c1.width / 2, -0.35, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.6)
        self.at("where neurons end")
        c2 = chipfix("where neurons end up", BLUE, 30)
        c2.move_to([1.3 + c2.width / 2, -1.45, 0])
        sh = B.shuffled(k=4, seed=11, lo=0.08)
        ex = VGroup(T("example mouse phenotype:", 26, GREY), T("disordered layers", 30, RED)).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT)
        ex.move_to([1.3 + ex.width / 2, 1.2, 0])
        self.play(FadeIn(c2, shift=LEFT * 0.2), FadeOut(lay), FadeIn(sh), FadeOut(nl), run_time=0.8)
        note = T("loss of folds is not the readout", 26, GREY)
        note.move_to([1.3 + note.width / 2, -2.8, 0])
        self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Dcx(SpokenScene):
    """DCX on the X chromosome; doublecortin clamps along a microtubule; boys with a mutation."""

    def construct(self):
        cx, cy, h, w = -4.7, 0.2, 5.4, 0.55
        X = xchrom(cx, cy, h=h, w=w)
        xl = T("X chromosome", 26, GREY).move_to([cx, -3.3, 0])
        band = x_band(cx, cy, h, w, t=-0.3)
        bp = x_band_pos(cx, cy, h, t=-0.3)
        self.at("A second gene")
        self.play(Create(X), FadeIn(xl), run_time=0.9)
        self.at("double cortin")
        self.play(FadeIn(band), run_time=0.4)
        dl = lab_right("DCX", GOLD, -2.85, bp[1], [bp[0] + 0.45, bp[1] - 0.02, 0], size=32)
        self.play(FadeIn(dl), run_time=0.4)
        # the protein, then the microtubule, then the clamps
        self.at("Its protein")
        prot = chipfix("doublecortin", GOLD, 30).move_to([1.0, bp[1], 0])
        pa = arr([dl[0].get_right()[0] + 0.15, bp[1], 0], [prot.get_left()[0] - 0.05, bp[1], 0], GOLD, w=5)
        self.play(GrowArrow(pa), FadeIn(prot, shift=LEFT * 0.2), run_time=0.6)
        self.at("binds")
        ty = 1.75
        tube = RoundedRectangle(corner_radius=0.27, width=7.3, height=0.54, stroke_color=TEAL, stroke_width=4,
                                fill_color=TEAL, fill_opacity=0.35).move_to([2.55, ty, 0])
        mt = T("microtubule", 30, TEAL).move_to([2.55, ty + 0.85, 0])
        self.play(GrowFromEdge(tube, LEFT), FadeIn(mt), run_time=0.7)
        xs = np.arange(-0.6, 5.9, 0.95)
        clamps = [RoundedRectangle(corner_radius=0.12, width=0.28, height=1.0, stroke_color=GOLD, stroke_width=3,
                                   fill_color=GOLD, fill_opacity=0.85).move_to([x, ty, 0]) for x in xs]
        starts = [Dot(prot.get_center(), radius=0.12, color=GOLD) for _ in xs]
        protein_link = arr(prot.get_top() + UP * 0.08, [1.0, ty - 0.32, 0], GOLD, w=5)
        self.play(GrowArrow(protein_link), run_time=0.3)
        self.add(*starts)
        self.play(LaggedStart(*[Transform(s, c) for s, c in zip(starts, clamps)], lag_ratio=0.3), run_time=2.3)
        self.at("Boys with a mutation")
        mutring = Circle(radius=0.4, stroke_color=RED, stroke_width=6).move_to(bp)
        boys = VGroup(T("boys with a mutation:", 28, GREY), T("typically lissencephaly", 32, RED)).arrange(
            DOWN, buff=0.14).move_to([2.6, -1.9, 0])
        self.play(Create(mutring), FadeIn(boys, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Predq(SpokenScene):
    """a girl with two X chromosomes, one mutant; each cell switches one off at random."""

    def construct(self):
        p = predict_parts()
        self.play(FadeIn(p["girl"]), run_time=0.7)
        self.at("one mutant copy")
        self.play(FadeIn(p["xn"]), FadeIn(p["xm"]), run_time=0.6)
        self.play(FadeIn(p["mut_l"]), run_time=0.4)
        self.at("Each of her cells")
        self.play(LaggedStart(*[FadeIn(VGroup(c, a, b)) for c, a, b in p["cells"]], lag_ratio=0.2), run_time=1.0)

        def off(i):
            c, a, b = p["cells"][i]
            x = a if OFF[i] == 0 else b
            return [x.animate.set_opacity(0.25), FadeIn(p["crosses"][i]), FadeIn(p["caps"][i])]
        self.at("switches off")
        self.play(*off(0), run_time=0.5)
        self.at("one X")
        self.play(*off(1), run_time=0.5)
        self.at("at random")
        self.play(*off(2), run_time=0.5)
        self.at("What would her cortex")
        self.play(FadeIn(p["cap"], shift=DOWN * 0.1), FadeIn(p["q"], shift=UP * 0.1), run_time=0.7)
        self.finish()


class S09Pause(NarratedScene):
    """5 s: the question, still."""

    def construct(self):
        p = predict_parts()
        self.add(p["girl"], p["xn"], p["xm"], p["mut_l"], p["cap"], p["q"])
        for i, (c, a, b) in enumerate(p["cells"]):
            (a if OFF[i] == 0 else b).set_opacity(0.25)
            self.add(c, a, b, p["crosses"][i], p["caps"][i])
        self.finish()


# ---------------------------------------------------------------------------------------------
class S10Mosaic(SpokenScene):
    """normal-copy neurons migrate; some mutant-copy neurons stall in the white matter."""

    KINDS = "BRBBRBRRBR"
    STALLED = {1, 6, 9}
    R = 0.38

    def construct(self):
        x0, x1 = -6.0, 2.6
        xs = np.linspace(-5.35, 2.0, 10)
        rs = np.random.RandomState(7)
        mid = (x0 + x1) / 2
        plate = Rectangle(width=x1 - x0, height=1.3, stroke_width=0, fill_color=GREY, fill_opacity=0.24).move_to(
            [mid, 2.65, 0])
        wmb = Rectangle(width=x1 - x0, height=2.2, stroke_width=0, fill_color=WM, fill_opacity=1).move_to(
            [mid, 0.2, 0])
        wmb_edge = Rectangle(width=x1 - x0, height=2.2, stroke_color=GREY, stroke_width=2, stroke_opacity=0.5,
                             fill_opacity=0).move_to([mid, 0.2, 0])
        vent, topb = bar(-3.4, x0, x1), bar(3.4, x0, x1)
        cl_ = left_text("cortical plate", 26, GREY, COLX + 0.8, 2.65)
        wm_l = left_text("white matter", 26, GREY, COLX + 0.8, 0.2)
        vl = left_text("ventricle", 26, GREY, COLX + 0.8, -3.3)
        cells = []
        for i, x in enumerate(xs):
            col = BLUE if self.KINDS[i] == "B" else RED
            y = (-2.8, -2.1, -1.4)[i % 3]
            cells.append(Circle(radius=self.R, stroke_color=col, stroke_width=3, fill_color=col,
                                fill_opacity=0.6).move_to([x, y, 0]))
        leg = VGroup(VGroup(Dot(radius=0.14, color=BLUE), T("normal copy", 26, BLUE)).arrange(RIGHT, buff=0.2),
                     VGroup(Dot(radius=0.14, color=RED), T("mutant copy", 26, RED)).arrange(RIGHT, buff=0.2)
                     ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        leg.move_to([COLX + 0.8 + leg.width / 2, -1.5, 0])
        self.add(plate, wmb, wmb_edge, vent, topb)
        self.play(FadeIn(plate), FadeIn(wmb), FadeIn(wmb_edge), FadeIn(vent), FadeIn(topb), FadeIn(cl_), FadeIn(wm_l),
                  FadeIn(vl), run_time=0.5)
        self.at("mosaic")
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cells], lag_ratio=0.08), run_time=1.2)
        self.at("neurons using")
        self.play(FadeIn(leg), run_time=0.5)
        blues = [c for i, c in enumerate(cells) if self.KINDS[i] == "B"]
        reds = [(i, c) for i, c in enumerate(cells) if self.KINDS[i] == "R"]
        self.at("normal copy")
        self.play(*[Indicate(c, color=BLUE, scale_factor=1.35) for c in blues], run_time=0.7)
        self.at("migrate")
        self.play(*[c.animate.move_to([c.get_center()[0], rs.uniform(2.4, 2.9), 0]) for c in blues], run_time=1.5)
        self.at("some using")
        stalled_y = {1: 0.7, 6: -0.1, 9: 0.5}
        anims = [c.animate.move_to([c.get_center()[0], stalled_y[i], 0]) for i, c in reds if i in self.STALLED]
        anims_up = [c.animate.move_to([c.get_center()[0], rs.uniform(2.4, 2.9), 0]) for i, c in reds
                    if i not in self.STALLED]
        self.play(*anims, *anims_up, run_time=1.1)
        self.at("mutant copy")
        sr = [ring(c.get_center(), RED, 0.62) for i, c in reds if i in self.STALLED]
        sl = tag("stalled", 30, RED).move_to([COLX + 0.8 + 0.85, 1.2 - 0.0, 0])
        self.play(*[FadeIn(r, scale=1.5) for r in sr], FadeIn(sl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11Band(SpokenScene):
    """stalled neurons gather into a second grey band: double cortex."""

    def construct(self):
        b = band_brain()
        panel = RoundedRectangle(corner_radius=0.2, width=6.2, height=7.0, stroke_color=GREY, stroke_width=3,
                                 fill_color="#0a0c11", fill_opacity=1).move_to([-2.9, 0, 0])
        shp = b.shape()
        sch = T("schematic", 22, GREY).move_to([5.7, -3.45, 0])
        self.play(FadeIn(panel), FadeIn(shp), FadeIn(sch), run_time=0.5)
        rs = np.random.RandomState(4)
        angs = np.linspace(0, 2 * np.pi, 34, endpoint=False)
        dots = VGroup(*[Dot(b.pt(t + rs.uniform(-0.05, 0.05), 0.64 + rs.uniform(-0.04, 0.04)), radius=0.12,
                            color=RED) for t in angs])
        bo = b.poly(0.72, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.55)
        bi = b.poly(0.56, stroke_color=GREY, stroke_width=2, stroke_opacity=0.6, fill_color=WM, fill_opacity=1)
        self.at("stalled neurons")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.03), run_time=0.9)
        self.at("band of gray matter")
        self.add(bo, bi)
        self.bring_to_front(dots)
        self.play(FadeIn(bo), FadeIn(bi), run_time=0.7)
        self.play(FadeOut(dots), run_time=0.4)
        self.at("beneath the cortex")
        l1 = lab_right("cortex", TEXT, 1.1, 2.6, b.pt(np.radians(60), 0.93))
        l2 = lab_right("grey matter band", TEXT, 1.1, 1.3, b.pt(np.radians(30), 0.64))
        self.play(FadeIn(l1), run_time=0.5)
        self.play(FadeIn(l2), run_time=0.5)
        self.at("It is called")
        sub = VGroup(T("subcortical band", 30, TEXT), T("heterotopia", 30, TEXT)).arrange(DOWN, buff=0.12,
                                                                                            aligned_edge=LEFT)
        sub.move_to([1.0 + sub.width / 2, -0.3, 0])
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.5)
        self.at("double cortex")
        dbl = left_text("double cortex", 44, TEXT, 1.0, -1.6, weight=BOLD)
        self.play(FadeIn(dbl, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S12Beat(NarratedScene):
    def construct(self):
        self.add(band_frame())
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13Cdk(SpokenScene):
    """Cdk5 with p35 phosphorylates doublecortin and NDEL1; mice lacking it have disordered layers."""

    def construct(self):
        cdk = chipfix("Cdk5", CDK, 54).move_to([-3.8, 0.5, 0])
        p35 = chipfix("p35", CDK, 40).move_to([-3.8, -1.2, 0])
        link = Line(cdk.get_bottom(), p35.get_top(), color=CDK, stroke_width=6)
        kin = T("kinase + activator", 30, TEXT).move_to([-3.8, 2.0, 0])
        self.at("kinase called")
        self.play(FadeIn(kin), run_time=0.3)
        self.at("cdk5")
        self.play(FadeIn(cdk), FadeIn(p35), Create(link), run_time=0.6)
        dcx = chipfix("doublecortin", GOLD, 42).move_to([2.5, 1.4, 0])
        ndel = chipfix("NDEL1", PURPLE, 44).move_to([2.5, -1.0, 0])
        a1 = arr(cdk.get_right() + RIGHT * 0.1, dcx.get_left() + LEFT * 0.1, TEXT, w=6)
        a2 = arr(cdk.get_right() + RIGHT * 0.1, ndel.get_left() + LEFT * 0.1, TEXT, w=6)
        tg = T("phosphorylates", 28, TEXT).move_to([-0.15, 2.65, 0])
        reg = T("dynein regulator", 30, PURPLE).move_to([2.5, -2.05, 0])
        def phosphate(target):
            return VGroup(Dot(radius=0.27, color=TEXT), T("P", 26, BG, weight=BOLD)).move_to(
                target.get_corner(UL) + LEFT * 0.05)
        pb1, pb2 = phosphate(dcx), phosphate(ndel)
        self.at("targets include")
        self.play(FadeIn(tg), run_time=0.3)
        self.at("double cortin")
        self.play(GrowArrow(a1), FadeIn(dcx), FadeIn(pb1), run_time=0.5)
        self.play(GrowArrow(a2), FadeIn(ndel), FadeIn(reg), FadeIn(pb2), run_time=0.5)
        self.at("dynein regulator")
        self.play(Indicate(ndel, color=PURPLE, scale_factor=1.06), run_time=0.5)
        self.at("Mice lacking")
        Bn = Brain(-3.1, 0.15, 2.6, 2.3, thick=0.36)
        Bk = Brain(3.1, 0.15, 2.6, 2.3, thick=0.36)
        ln, lk = Bn.layers(3), Bk.layers(3)
        normal = T("normal", 34, TEXT).move_to([-3.1, 3.0, 0])
        knockout = T("Cdk5 or p35 knockout", 30, TEXT).move_to([3.1, 3.0, 0])
        nn = T("ordered layers", 30, TEXT).move_to([-3.1, -2.8, 0])
        self.play(*[FadeOut(m) for m in (kin, cdk, p35, link, tg, a1, a2, dcx, ndel, reg, pb1, pb2)],
                  FadeIn(Bn.shape()), FadeIn(Bk.shape()), FadeIn(ln), FadeIn(lk),
                  FadeIn(normal), FadeIn(knockout), FadeIn(nn), run_time=0.5)
        self.at("disordered layers", lead=0.4)
        dis = T("disordered layers", 32, RED).move_to([3.1, -2.8, 0])
        shuffled = Bk.shuffled(k=4, seed=12, lo=0.03).set_color(RED)
        self.play(FadeOut(lk), FadeIn(shuffled), FadeIn(dis), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14Route(SpokenScene):
    """back to the wall (zoomed on its lower part): a newborn neuron first moves from the ventricular to the
    subventricular zone."""

    def construct(self):
        g, z = wallw(ZZ, top_bar=False)
        nb = Multi(x=CELL_X, y=-1.9, sc=1.95, op=0)
        self.add(nb.mob)
        vzl = zl("ventricular zone", -2.3)
        svl = zl("subventricular zone", 0.75, TEXT)
        self.play(FadeIn(g), nb.op.animate.set_value(1), FadeIn(vzl), FadeIn(svl), run_time=0.3)
        self.at("two stroke climb")
        climb = Arrow([0.0, 2.2, 0], [0.0, 3.35, 0], color=TEXT, stroke_width=7, tip_length=0.3, buff=0)
        cl = zl("two-stroke climb", 2.75, TEXT)
        self.play(GrowArrow(climb), FadeIn(cl), run_time=0.6)
        self.at("whole trip")
        whole = DoubleArrow([-6.0, -3.3, 0], [-6.0, 3.4, 0], color=GREY, stroke_width=5, tip_length=0.25, buff=0)
        wl = T("whole trip", 26, TEXT).rotate(PI / 2).move_to([-6.5, 0.2, 0])
        self.play(GrowFromCenter(whole), FadeIn(wl), run_time=0.6)
        self.at("embryonic rat")
        cap = stack(["Noctor, Kriegstein", "and colleagues, 2004:", "embryonic rat", "cortical slices"], 22, GREY,
                    COLX, -0.65)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.at("newborn neurons")
        nlab = tag("newborn neuron", 26, TEXT).move_to([0.0, -1.2, 0])
        self.play(FadeIn(nlab), Indicate(nb.mob, color=BLUE, scale_factor=1.04), run_time=0.6)
        self.at("first move")
        self.play(FadeOut(nlab), *nb.to(y=0.75), run_time=1.4)
        self.at("subventricular zone")
        self.play(z["svz"].animate.set_fill(GREY, 0.32), run_time=0.4)
        self.play(z["svz"].animate.set_fill(GREY, 0.10), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
L15_START = [0.0] * 6
L15_BASE = [0.75, 0.6, 0.8, 0.65, 0.7, 0.6]
L15_END = [0.8, 0.7, 0.6, 0.5, 0.6, 0.7]
S15_Y = 0.75
S15_END = (CELL_X + 0.2, 0.9)


class S15Multi(SpokenScene):
    """multipolar: several short processes extend and retract; slow drift; little net progress; a clock ticks."""

    def construct(self):
        g, z = wallw(ZZ, top_bar=False)
        svl = zl("subventricular zone", -2.6, TEXT)
        m = Multi(x=CELL_X, y=S15_Y, sc=1.95, L=L15_START, op=1)
        self.add(g, svl, m.mob)
        self.wait(0.2)
        self.at("multipolar")
        self.play(LaggedStart(*[t.animate.set_value(v) for t, v in zip(m.L, L15_BASE)], lag_ratio=0.18),
                  run_time=1.4)
        self.at("several short")
        ml = left_text("multipolar", 40, BLUE, COLX, -0.2, weight=BOLD)
        self.play(FadeIn(ml, shift=DOWN * 0.1), run_time=0.4)
        self.play(*m.to(L={0: 0.55, 2: 1.0, 4: 0.9, 5: 0.45}), run_time=0.9)
        self.play(*m.to(L={0: 0.8, 1: 0.45, 3: 0.9, 5: 0.7}), run_time=0.8)
        # the clock starts when the drifting starts
        self.at("move slowly")
        cc = np.array([4.4, 2.15, 0.0])
        face = Circle(radius=0.95, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(cc)
        ticks = VGroup(*[Line(cc + 0.78 * np.array([np.cos(a), np.sin(a), 0]), cc + 0.9 * np.array([np.cos(a), np.sin(a), 0]),
                              color=GREY, stroke_width=3) for a in np.linspace(0, 2 * np.pi, 12, endpoint=False)])
        hand = Line(cc, cc + UP * 0.72, color=GOLD, stroke_width=6)
        hand.add_updater(lambda mob, dt: mob.rotate(-dt * 2.0, about_point=cc))
        self.play(FadeIn(face), FadeIn(ticks), FadeIn(hand), run_time=0.3)
        start = m.pos().copy()
        trail = TracedPath(m.pos, stroke_color=TEXT, stroke_width=3, stroke_opacity=0.85, dissipating_time=None)
        self.add(trail)
        self.play(*m.to(x=CELL_X + 1.0, y=S15_Y + 0.5, L={0: 0.5, 2: 1.0, 4: 0.9, 5: 0.5}), run_time=1.1)
        self.at("change direction")
        self.play(*m.to(x=CELL_X - 0.3, y=S15_Y - 0.35, L={0: 0.9, 1: 0.8, 3: 0.4, 4: 0.5}), run_time=1.1)
        self.at("little net progress")
        self.play(*m.to(x=S15_END[0], y=S15_END[1], L={i: v for i, v in enumerate(L15_END)}), run_time=1.0)
        nl = left_text("little net progress", 26, GREY, COLX, -1.2)
        self.play(FadeIn(nl), run_time=0.4)
        self.at("about a day")
        dl = stack(["about a day", "or longer"], 30, GOLD, 4.4, 0.55, align=ORIGIN)
        self.play(FadeIn(dl, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S16Back(SpokenScene):
    """the s15 neuron moves back toward the ventricle; why is not settled."""

    def construct(self):
        g, z = wallw(ZZ, top_bar=False)
        svl = zl("subventricular zone", -2.6, TEXT)
        m = Multi(x=S15_END[0], y=S15_END[1], sc=1.95, L=L15_END, op=1)
        self.add(g, svl, m.mob)
        self.wait(0.2)
        self.at("move back")
        down = Arrow([0.75, 1.5, 0], [0.75, -0.3, 0], color=TEXT, stroke_width=7, tip_length=0.3, buff=0)
        self.play(GrowArrow(down), *m.to(x=CELL_X, y=-0.4, L={0: 0.6, 2: 1.0, 5: 0.9}), run_time=1.2)
        self.at("ventricle")
        vl = zl("ventricle", -3.4, TEXT)
        self.play(*m.to(y=-1.1, L={0: 0.5, 1: 0.5, 3: 0.8, 4: 0.8}), FadeIn(vl), run_time=1.2)
        self.at("Why some")
        q = T("?", 110, RED, weight=BOLD).move_to([0.35, -1.1, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.7)
        self.finish()


class S17Bipolar(SpokenScene):
    """multipolar to bipolar, then the climb: leading process first, then the nucleus catches up."""

    def construct(self):
        sc = BSC
        g, z = wallw(ZF, extra_fibs=(CELL_X + 0.5,))
        m = Multi(x=CELL_X, y=-1.1, sc=sc, L=[0.8, 0.6, 0.8, 0.6, 0.6, 0.55], op=1)
        cell = bip_cell(op=0, cs_op=1, cs=-0.1)
        self.add(g, m.mob, cell.mob)
        self.wait(0.2)
        self.at("turn bipolar")
        tl = stack(["transition to", "sustained", "bipolar", "locomotion"], 28, TEXT, COLX, -0.8)
        self.play(FadeIn(tl), *m.to(L={0: 1.1 / sc + 0.45, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 1.45 - 1.1 / sc}), run_time=1.2)
        m.op.set_value(0)
        cell.t["op"].set_value(1)
        self.at("sustained climb")
        self.play(FadeOut(tl), *cell.to(tip=1.8, cs=1.05), run_time=1.0)
        self.at("cortical plate")
        cpl = zl("cortical plate", 2.7, TEXT)
        self.play(FadeIn(cpl), *cell.to(soma=0.3, tail=-0.65), run_time=1.2)
        self.at("front goes first")
        fg = tag("front goes first", 28, TEXT).move_to([0.3, 2.35, 0])
        self.play(FadeIn(fg), *cell.to(tip=1.8, cs=1.45), run_time=1.0)
        self.finish()


class S18Listurn(SpokenScene):
    """LIS1 tags at the turn and at the climb on the same bipolar neuron: one defect, more than one step."""

    def construct(self):
        P = s18_static()
        main = s18_cell()
        self.add(P["wall"], main.mob)
        self.at("this turn")
        self.play(FadeIn(P["lis"]), FadeIn(P["turn"]), FadeIn(P["halo"]), FadeIn(P["stall"]), run_time=0.5)
        self.at("one defect")
        self.play(Indicate(P["lis"], color=PURPLE), run_time=0.5)
        self.at("stall cells")
        self.play(ReplacementTransform(P["turn"], P["climb"]),
                  P["lis"].animate.move_to([0.25, 1.6, 0]), run_time=0.7)
        self.finish()


class S19Beat(NarratedScene):
    def construct(self):
        P = s18_static()
        P["lis"].move_to([0.25, 1.6, 0])
        main = s18_cell()
        self.add(P["wall"], main.mob, *[P[k] for k in ("lis", "climb", "halo", "stall")])
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20Take(SpokenScene):
    """one cycle, the failure, then: track the nucleus, not the tip."""

    def construct(self):
        sc, y0, x = 1.1, 0.0, -2.8
        fib = fiber(x + 0.5 * sc, -3.4, 3.4, rungs=True)
        cell = Cell(x=x, y0=y0, sc=sc, soma=-2.2, tip=-0.3, tail=-3.15, op=0)
        self.add(fib, cell.mob)
        c1, c2 = stroke_chips()
        self.play(cell.t["op"].animate.set_value(1), run_time=0.3)
        self.at("two stroke cycle")
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(c2, shift=LEFT * 0.2), *lit(c1, True),
                  *cell.to(tip=1.3), run_time=0.9)
        self.play(*lit(c1, False), *lit(c2, True), *cell.to(soma=-0.7, tail=-1.65), run_time=0.9)
        self.at("one way")
        ow = T("one way, not the only way", 28, GREY).move_to([3.7, -3.0, 0])
        self.play(FadeIn(ow, shift=UP * 0.1), run_time=0.5)
        self.at("migration can fail")
        self.play(*lit(c2, False), *lit(c1, True), *cell.to(tip=2.5), run_time=0.8)
        rn = ring(cell.P(0, cell.v("soma")), ORANGE, 0.8)
        self.play(FadeIn(rn, scale=1.6), *lit(c1, False), *lit(c2, True), run_time=0.6)
        self.at("film a migrating")
        cx0, cx1, cy0, cy1, k = -5.0, -0.6, -3.8, 3.1, 0.55
        corners = VGroup(*[VMobject(stroke_color=TEXT, stroke_width=4).set_points_as_corners(pts) for pts in (
            [[cx0, cy1 - k, 0], [cx0, cy1, 0], [cx0 + k, cy1, 0]], [[cx1 - k, cy1, 0], [cx1, cy1, 0], [cx1, cy1 - k, 0]],
            [[cx0, cy0 + k, 0], [cx0, cy0, 0], [cx0 + k, cy0, 0]], [[cx1 - k, cy0, 0], [cx1, cy0, 0], [cx1, cy0 + k, 0]])])
        self.play(FadeIn(corners), run_time=0.5)
        self.at("track the nucleus")
        tn = left_text("track the nucleus", 40, ORANGE, 0.2, -0.6, weight=BOLD)
        self.play(rn.animate.set_stroke(width=8), FadeIn(tn, shift=UP * 0.1), run_time=0.7)
        self.at("not the tip")
        tp = cell.P(0, cell.v("tip"))
        cross = VGroup(Line(tp + [-0.3, -0.3, 0], tp + [0.3, 0.3, 0], color=RED, stroke_width=7),
                       Line(tp + [-0.3, 0.3, 0], tp + [0.3, -0.3, 0], color=RED, stroke_width=7))
        nt = left_text("not the tip", 40, GREY, 0.2, -1.7, weight=BOLD)
        self.play(Create(cross), FadeIn(nt, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S21End(EndCard):
    LINE = "When you film a migrating neuron, track the nucleus, not the tip."
