"""Radial migration, chapter 2: What Brings the Nucleus Up  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, shared by all chapters; taken from scenes.old.py)
  BLUE   = the migrating neuron (soma outline, leading process, swelling) and the tip
  ORANGE = the nucleus
  YELLOW = centrosome
  GREEN  = radial glial fiber (not used in this chapter)
  TEAL   = microtubules (the cage)
  PURPLE = dynein, and LIS1 (its regulator); also the LIS1/dynein knockdown
  PINK   = myosin II (and blebbistatin, which blocks it)
  RED    = stalled / blocked
  GREY   = labels, structure, de-emphasised
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E87FB0"
NEURON_FILL = "#16303c"
X0 = -2.3                      # x of the neuron's axis in the single-cell scenes


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def lab_left(text, color, x, y, tip, size=26):
    """text whose right edge sits at x, with an arrow to `tip`."""
    t = T(text, size, color)
    t.move_to([x - t.width / 2, y, 0])
    return VGroup(t, arr([x + 0.12, y, 0], tip, color))


def lab_right(text, color, x, y, tip, size=26):
    """text whose left edge sits at x, with an arrow to `tip`."""
    t = T(text, size, color)
    t.move_to([x + t.width / 2, y, 0])
    return VGroup(t, arr([x - 0.12, y, 0], tip, color))


def chipfix(text, color, size=28):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def lit(c, on):
    col = TEXT if on else GREY
    return [c[1].animate.set_stroke(col).set_fill(col, 0.16), c[2].animate.set_color(col)]


def ring(pos, color, r=0.34, w=5):
    return Circle(radius=r, stroke_color=color, stroke_width=w).move_to(pos)


def fade(g, op):
    if op < 0.99:
        for m in g.family_members_with_points():
            m.set_stroke(opacity=m.get_stroke_opacity() * op)
            m.set_fill(opacity=m.get_fill_opacity() * op)
    return g


def dyn(fn, tr):
    """always_redraw of fn(), faded by tracker tr (so it can be faded in and out)."""
    def f():
        o = tr.get_value()
        return VGroup() if o < 0.02 else fade(fn(), o)
    return always_redraw(f)


def tag():
    """corner tag, only on scenes that draw the neuron"""
    g = T("Schematic model", 24, GREY)
    g.move_to([6.7 - g.width / 2, -3.65, 0])
    return g


def nring(pos, color=RED, w=5, width=1.62, height=1.97):
    return Ellipse(width=width, height=height, stroke_color=color, stroke_width=w).move_to(pos)


def cross(pos, s=0.2, color=RED, w=7):
    p = np.array(pos, dtype=float)
    return VGroup(Line(p + [-s, -s, 0], p + [s, s, 0], color=color, stroke_width=w),
                  Line(p + [-s, s, 0], p + [s, -s, 0], color=color, stroke_width=w))


def dyn_shape(mx, y, r=0.26, side=1, tail=None, glow=0.0, gap=0.32):
    """a dynein dimer on a vertical microtubule at x=mx: two stepping feet on the track, a round head, an optional tail."""
    g = VGroup()
    hx = mx + side * (r + gap)
    ph = 2 * np.pi * y / 0.8
    for s in (1, -1):
        fy = y + s * (0.30 + 0.14 * np.sin(ph))
        g.add(Line([hx, y, 0], [mx + side * 0.04, fy, 0], color=PURPLE, stroke_width=6))
        g.add(Dot([mx + side * 0.04, fy, 0], radius=0.07, color=PURPLE))
    if glow > 0.02:
        g.add(Dot([hx, y, 0], radius=r + 0.2, color=PURPLE).set_opacity(0.35 * glow))
    g.add(Circle(radius=r, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.9)
          .move_to([hx, y, 0]))
    if tail is not None:
        g.add(Line([hx + side * r, y, 0], [tail, y, 0], color=PURPLE, stroke_width=6))
    return g



def badge(sign, pos, r=0.22):
    c = Circle(radius=r, stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(pos)
    t = T(sign, 34, TEXT, weight=BOLD).move_to(pos)
    return VGroup(c, t)


def leader(a, b, color=GREY, w=3):
    return Line(a, b, color=color, stroke_width=w, stroke_opacity=0.9)


# ---------------------------------------------------------------------------------------------
# the neuron
# ---------------------------------------------------------------------------------------------
class Rig:
    """The migrating neuron drawn from trackers.  ny nucleus y, cs centrosome y, ty tip y, sw swelling size,
    cage / fwd = how much of the cage / the forward microtubules is drawn, op = overall opacity,
    cop = opacity of the microtubules only.  z / zc zoom the drawing about height zc."""
    A, B = 0.85, 1.0
    SX, SY = 1.8, 1.5
    PW = 0.9
    L = 2.7
    SWY, SWW, SWH = 2.25, 2.4, 2.2
    DEF = dict(ny=-1.6, cs=-0.15, ty=3.4, sw=0.0, cage=0.0, fwd=0.0, op=1.0, cso=1.0, cop=1.0)

    def __init__(self, z=1.0, zc=0.0, lfmax=2.6, show_tail=True, **kw):
        d = dict(self.DEF)
        d.update(kw)
        self.z, self.zc, self.lfmax = z, zc, lfmax
        self.show_tail = show_tail
        self.t = {k: ValueTracker(v) for k, v in d.items()}
        self.mobs = [always_redraw(f) for f in (self.body, self.cage_m, self.fwd_m, self.nuc_m, self.cs_m)]

    def v(self, k):
        return self.t[k].get_value()

    def to(self, **kw):
        return [self.t[k].animate.set_value(val) for k, val in kw.items()]

    def P(self, x, y):
        return np.array([X0 + x * self.z, self.zc + (y - self.zc) * self.z, 0.0])

    def tye(self):
        ty, sw = self.v("ty"), self.v("sw")
        return min(ty, self.SWY + self.SWH * sw / 2 - 0.15) if sw > 0.03 else ty

    def hw(self, y):
        ny, ty, sw = self.v("ny"), self.tye(), self.v("sw")
        h = 0.0
        d = (y - ny) / self.SY
        if abs(d) < 1:
            h = self.SX * np.sqrt(1 - d * d)
        if ny + self.SY - 0.4 < y < ty:
            h = max(h, self.PW / 2)
        if sw > 0.03:
            e = (y - self.SWY) / (self.SWH * sw / 2)
            if abs(e) < 1:
                h = max(h, self.SWW * sw / 2 * np.sqrt(1 - e * e))
        return h

    def cagex(self, w, y):
        d = self.v("cs") - y
        s = min(1.0, 0.85 * self.hw(y) / 1.5)
        return w * (1 - np.exp(-1.3 * d)) * s

    def cage_pt(self, w, side, f):
        y = self.v("cs") - self.L * f
        return self.P(side * self.cagex(w, y), y)

    def lf(self):
        return max(0.4, min(self.lfmax, 3.1 - self.v("cs")))

    def fwd_x(self, side, y):
        """x (neuron axis units) of a forward microtubule at height y (clamped to its end)"""
        cs, lf, f = self.v("cs"), self.lf(), self.v("fwd")
        u = min(max((y - cs) / (lf * max(f, 0.01)), 0.0), 1.0)
        return side * 0.3 * f * u

    # pieces ------------------------------------------------------------------------------
    def body(self):
        ny, ty, sw, op, z = self.v("ny"), self.tye(), self.v("sw"), self.v("op"), self.z
        if op < 0.02:
            return VGroup()
        g = VGroup()
        if self.show_tail:
            g.add(Line(self.P(0, ny - self.SY - 0.4), self.P(0, ny - self.SY + 0.1), color=BLUE, stroke_width=10))
            g.add(Dot(self.P(0, ny - self.SY - 0.4), radius=0.09 * z, color=BLUE))
        y0 = ny + self.SY - 0.3
        g.add(RoundedRectangle(corner_radius=0.3, width=self.PW * z, height=(ty - y0) * z, stroke_color=BLUE,
                               stroke_width=5, fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, (ty + y0) / 2)))
        if sw > 0.03:
            g.add(Ellipse(width=self.SWW * sw * z, height=self.SWH * sw * z, stroke_color=BLUE, stroke_width=5,
                          fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, self.SWY)))
        g.add(Ellipse(width=2 * self.SX * z, height=2 * self.SY * z, stroke_color=BLUE, stroke_width=5,
                      fill_color=NEURON_FILL, fill_opacity=1).move_to(self.P(0, ny)))
        return fade(g, op)

    def cage_m(self):
        f, op, cs = self.v("cage"), self.v("op") * self.v("cop"), self.v("cs")
        if f < 0.02 or op < 0.02:
            return VGroup()
        g = VGroup()
        for w in (1.22, 1.5):
            for side in (-1, 1):
                ys = np.linspace(cs, cs - self.L * f, max(5, int(40 * f)))
                m = VMobject(stroke_color=TEAL, stroke_width=5)
                m.set_points_smoothly([self.P(side * self.cagex(w, y), y) for y in ys])
                g.add(m)
        return fade(g, op)

    def fwd_m(self):
        f, op, cs = self.v("fwd"), self.v("op") * self.v("cop"), self.v("cs")
        if f < 0.02 or op < 0.02:
            return VGroup()
        g = VGroup(*[Line(self.P(0, cs), self.P(s * 0.3 * f, cs + self.lf() * f), color=TEAL, stroke_width=5)
                     for s in (-1, 1)])
        return fade(g, op)

    def nuc_m(self):
        op, z = self.v("op"), self.z
        if op < 0.02:
            return VGroup()
        return fade(VGroup(Ellipse(width=2 * self.A * z, height=2 * self.B * z, stroke_color=ORANGE, stroke_width=5,
                                   fill_color=ORANGE, fill_opacity=0.55).move_to(self.P(0, self.v("ny")))), op)

    def cs_m(self):
        o = self.v("cso") * self.v("op")
        if o < 0.02:
            return VGroup()
        return fade(VGroup(Dot(self.P(0, self.v("cs")), radius=0.17 * self.z, color=YELLOW)), o)

    # labels that follow the parts ----------------------------------------------------------
    def nuc_label(self, tr):
        return dyn(lambda: lab_left("nucleus", ORANGE, X0 - 1.95, self.v("ny"), [X0 - 0.9, self.v("ny"), 0]), tr)

    def cs_label(self, tr):
        return dyn(lambda: lab_left("centrosome", YELLOW, X0 - 1.0, self.v("cs"), [X0 - 0.25, self.v("cs"), 0]), tr)


SWD_Y = (1.9, 2.35)       # heights of the swelling dynein


def swell_marks(rig, mk, gl):
    """dynein in the swelling: each head sits on the swelling wall and reaches (touches) a forward microtubule"""
    def f():
        grp = VGroup()
        g = gl.get_value()
        for side in (-1, 1):
            for y in SWD_Y:
                hx = rig.hw(y) - 0.14
                p = np.array([X0 + side * hx, y, 0.0])
                q = np.array([X0 + rig.fwd_x(side, y), y, 0.0])
                grp.add(Arrow(p, q, buff=0, color=PURPLE, stroke_width=6, tip_length=0.2,
                              max_tip_length_to_length_ratio=0.5))
                if g > 0.02:
                    grp.add(Dot(p, radius=0.3, color=PURPLE).set_opacity(0.35 * g))
                grp.add(Dot(p, radius=0.17, color=PURPLE))
        return grp
    return dyn(f, mk)


def nuc_marks(rig, mk, gl):
    """dynein on the nuclear envelope, reaching out to the cage"""
    def f():
        grp = VGroup()
        g = gl.get_value()
        ny = rig.v("ny")
        for side in (-1, 1):
            for dy in (0.85, 0.55):
                yb = ny + dy
                bx = rig.A * np.sqrt(1 - (dy / rig.B) ** 2)
                cx = rig.cagex(1.22, yb)
                on = rig.P(side * cx, yb)
                grp.add(Line(rig.P(side * bx, yb), on, color=PURPLE, stroke_width=6))
                if g > 0.02:
                    grp.add(Dot(on, radius=0.34, color=PURPLE).set_opacity(0.35 * g))
                grp.add(Dot(on, radius=0.15, color=PURPLE))
        return grp
    return dyn(f, mk)


def follow_arrow(rig, key, x, up0, up1, color=PURPLE, w=9):
    """an up arrow beside a part that moves (key 'cs' or 'ny'), following it"""
    def f():
        y = rig.v(key)
        return Arrow([x, y + up0, 0], [x, y + up1, 0], buff=0, color=color, stroke_width=w, tip_length=0.3,
                     max_tip_length_to_length_ratio=0.5)
    return always_redraw(f)


def follow_chip(rig, key, text, x, dy=0.0, size=28):
    def f():
        c = chipfix(text, TEXT, size)
        c.move_to([x + c.width / 2, rig.v(key) + dy, 0])
        return c
    return always_redraw(f)


# ---------------------------------------------------------------------------------------------
# the two panels (held in place / rides on something that can move), centrosome always at the top
# ---------------------------------------------------------------------------------------------
def swelling_outline():
    ys = np.linspace(-2.4, 2.5, 100)
    widths = [max(0.62, 2.6 * np.sqrt(max(0, 1 - ((y - 0.1) / 2.15) ** 2))) for y in ys]
    pts = [[w, y, 0] for w, y in zip(widths, ys)]
    pts += [[-w, y, 0] for w, y in zip(widths[::-1], ys[::-1])]
    return VMobject(stroke_color=BLUE, stroke_width=5, fill_color=NEURON_FILL, fill_opacity=1).set_points_as_corners(pts + [pts[0]])


class Panels:
    CY = -0.35
    TOPA = 2.0              # local height of the microtubule's minus end (centrosome) in the swelling panel
    MA = -0.8               # x of the microtubule in panel A
    MB = -1.3               # x of the microtubule in panel B

    def __init__(self, a=0.0, b=-0.9, ha=0.0, hb=0.0, opa=1.0, opb=1.0, sa=0.78, sb=0.78, xa=-3.45, xb=3.45,
                 ar=0.0, xl=0.0):
        self.t = {k: ValueTracker(v) for k, v in dict(a=a, b=b, ha=ha, hb=hb, opa=opa, opb=opb, sa=sa, sb=sb,
                                                       xa=xa, xb=xb, ar=ar, xl=xl).items()}
        self.mobs = [always_redraw(f) for f in (self.pa, self.pb, self.head_a, self.head_b)]

    def v(self, k):
        return self.t[k].get_value()

    def place(self, g, s, cx):
        return g.scale(s, about_point=ORIGIN).shift([cx, self.CY, 0])

    # panel A ------------------------------------------------------------------------------
    def pa(self):
        op, s, cx, h = self.v("opa"), self.v("sa"), self.v("xa"), self.v("ha")
        if op < 0.02:
            return VGroup()
        top = self.TOPA - self.v("a")
        g = VGroup(RoundedRectangle(corner_radius=0.2, width=5.8, height=6.0, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.05),
                   swelling_outline(),
                   Line([self.MA, top - 2.4, 0], [self.MA, top, 0], color=TEAL, stroke_width=9),
                   Dot([self.MA, top, 0], radius=0.26, color=YELLOW))
        if s > 0.6:
            g.add(T("swelling", 26, BLUE).move_to([0, -2.68, 0]))
        if h > 0.02 and s > 0.6:
            box = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.75, height=1.1, stroke_color=GREY,
                                                  stroke_width=3), num_dashes=28).move_to([1.5, 0.4, 0])
            lab = VGroup(T("proposed", 24, GREY), T("anchor", 24, GREY)).arrange(DOWN, buff=0.04).move_to([1.5, 0.4, 0])
            g.add(fade(VGroup(box, lab), h))
        g.add(dyn_shape(self.MA, 0.4, r=0.38, tail=0.62 if h > 0.02 else None))
        # a single arrow for the direction the centrosome moves
        ar = self.v("ar")
        if ar > 0.02:
            g.add(fade(Arrow([self.MA - 0.9, self.TOPA, 0], [self.MA - 0.9, top - 0.05, 0], buff=0, color=YELLOW,
                             stroke_width=8, tip_length=0.3, max_tip_length_to_length_ratio=0.5), ar))
        xl = self.v("xl")
        if xl > 0.02:
            g.add(fade(VGroup(cross([-0.38, 1.2, 0], 0.22), T("cannot walk", 26, TEXT).move_to([1.0, 1.2, 0])), xl))
        return fade(self.place(g, s, cx), op)

    # panel B ------------------------------------------------------------------------------
    def pb(self):
        op, s, cx, h, y = self.v("opb"), self.v("sb"), self.v("xb"), self.v("hb"), self.v("b")
        if op < 0.02:
            return VGroup()
        g = VGroup(RoundedRectangle(corner_radius=0.2, width=5.8, height=6.0, stroke_color=GREY, stroke_width=3,
                                    fill_color=GREY, fill_opacity=0.05),
                   Line([self.MB, -2.4, 0], [self.MB, 2.0, 0], color=TEAL, stroke_width=9),
                   Dot([self.MB, 2.3, 0], radius=0.26, color=YELLOW))
        if h > 0.02:
            disc = Circle(radius=0.75, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.4)
            lab = VGroup(T("cargo, for example", 24, GREY), T("the nucleus", 24, GREY)).arrange(DOWN, buff=0.05)
            lab.move_to([1.25, y - 1.35, 0])
            g.add(fade(disc.move_to([1.35, y, 0]), h))
            if s > 0.6:
                g.add(fade(lab, h))
        g.add(dyn_shape(self.MB, y, r=0.38, tail=0.6 if h > 0.02 else None))
        return fade(self.place(g, s, cx), op)

    # titles (not scaled, so they stay readable on a thumbnail) ---------------------------------
    def head_a(self):
        op, s, cx = self.v("opa"), self.v("sa"), self.v("xa")
        if op < 0.02:
            return VGroup()
        col = TEXT if s > 0.6 else GREY
        return fade(T("held in place", 26, col).move_to([cx, self.CY + 3.0 * s + 0.35, 0]), op)

    def head_b(self):
        op, s, cx = self.v("opb"), self.v("sb"), self.v("xb")
        if op < 0.02:
            return VGroup()
        col = TEXT if s > 0.6 else GREY
        g = VGroup(T("attached to something", 26, col), T("that can move", 26, col)).arrange(DOWN, buff=0.05)
        return fade(g.move_to([cx, self.CY + 3.0 * s + 0.55, 0]), op)

    # preset layouts
    EQ = dict(sa=0.78, sb=0.78, xa=-3.45, xb=3.45)
    ACT_A = dict(sa=0.98, sb=0.4, xa=-2.2, xb=5.0)
    ACT_B = dict(sa=0.4, sb=0.98, xa=-5.0, xb=2.2)

    def to(self, **kw):
        return [self.t[k].animate.set_value(val) for k, val in kw.items()]


# ---------------------------------------------------------------------------------------------
# the experiment layout: movies on the left, the table on the right
# ---------------------------------------------------------------------------------------------
# positions in a movie are fractions of the panel height
N0F, C0F, T0F = 0.30, 0.62, 0.80
CTL_END = dict(n=0.52, c=0.82, t=0.95)
KD_END = dict(n=N0F, c=C0F, t=0.95)
BL_END = dict(n=N0F, c=0.84, t=0.95)


def smooth(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def control_path(p):
    """one loop of the control movie: centrosome (and tip) ahead, then the nucleus follows, then back to the start"""
    p = p % 1.0
    if p < 0.08:
        u1, u2, back = 0.0, 0.0, 0.0
    elif p < 0.40:
        u1, u2, back = smooth((p - 0.08) / 0.32), 0.0, 0.0
    elif p < 0.72:
        u1, u2, back = 1.0, smooth((p - 0.40) / 0.32), 0.0
    elif p < 0.90:
        u1, u2, back = 1.0, 1.0, 0.0
    else:
        u1, u2, back = 1.0, 1.0, smooth((p - 0.90) / 0.10)
    k1, k2 = u1 * (1 - back), u2 * (1 - back)
    return (N0F + (CTL_END["n"] - N0F) * k2, C0F + (CTL_END["c"] - C0F) * k1, T0F + (CTL_END["t"] - T0F) * k1)


class Mini:
    """one filmed neuron inside a panel: process, soma, nucleus, centrosome, tip"""
    def __init__(self, cx, yb, H, s, ox=0.0, n=N0F, c=C0F, t=T0F, op=1.0, auto=None):
        self.cx, self.yb, self.H, self.s, self.ox, self.auto = cx, yb, H, s, ox, auto
        self.t = {k: ValueTracker(v) for k, v in dict(n=n, c=c, t=t, op=op).items()}
        self.mob = always_redraw(self.build)

    def v(self, k):
        return self.t[k].get_value()

    def to(self, **kw):
        return [self.t[k].animate.set_value(val) for k, val in kw.items()]

    def fr(self):
        if self.auto is not None:
            return control_path(self.auto.get_value())
        return self.v("n"), self.v("c"), self.v("t")

    def pt(self, which):
        n, c, t = self.fr()
        f = {"n": n, "c": c, "t": t}[which]
        return np.array([self.cx + self.ox, self.yb + f * self.H, 0.0])

    def build(self):
        op, s = self.v("op"), self.s
        if op < 0.02:
            return VGroup()
        pn, pc, pt = self.pt("n"), self.pt("c"), self.pt("t")
        g = VGroup(Line(pn + [0, 0.8 * s, 0], pt, color=BLUE, stroke_width=10),
                   Dot(pt, radius=max(0.15, 0.14 * s), color=BLUE),
                   Ellipse(width=2.3 * s, height=2.0 * s, stroke_color=BLUE, stroke_width=5, fill_color=NEURON_FILL,
                           fill_opacity=1).move_to(pn),
                   Ellipse(width=1.36 * s, height=1.7 * s, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE,
                           fill_opacity=0.55).move_to(pn),
                   Dot(pc, radius=max(0.15, 0.17 * s), color=YELLOW))
        return fade(g, op)

    def labels(self):
        """tip / centrosome / nucleus labels that follow the parts (to the right of the neuron)"""
        s = self.s

        def f(which, text, col, dx):
            p = self.pt(which)
            return lab_right(text, col, p[0] + dx, p[1], p + [0.17, 0, 0], size=24)
        return [always_redraw(lambda: f("t", "tip", BLUE, 0.45)),
                always_redraw(lambda: f("c", "centrosome", YELLOW, 0.36)),
                always_redraw(lambda: f("n", "nucleus", ORANGE, 0.68 * s + 0.4))]


class Exp:
    YB, TX = -2.75, -0.5
    ROWY = [1.5, 0.1, -1.3]
    COLX = [2.215, 4.045, 5.875]
    ROWS = [("tip", BLUE), ("centrosome", YELLOW), ("nucleus", ORANGE)]
    COLS = [("control", TEXT), ("LIS1/dynein\nknockdown", PURPLE), ("myosin II\nblock", PINK)]
    PANEL_HEAD = ["control", "LIS1 or\ndynein\nknockdown", "blebbistatin"]
    PANEL_COL = [TEXT, PURPLE, PINK]
    CTL = {(0, 0): ("extends", TEXT), (1, 0): ("moves\nahead", TEXT), (2, 0): ("follows", TEXT)}
    KD = {(0, 1): ("extends", TEXT), (1, 1): ("stalls", RED), (2, 1): ("stalls", RED)}
    BL = {(0, 2): ("extends", TEXT), (1, 2): ("keeps\nmoving", TEXT), (2, 2): ("stops", RED)}

    def __init__(self, layout="L3", active=1, ops=1.0, states=None, known=(), qs=(), auto=True, auto_ph=0.0):
        states = states or {}
        self.layout = layout
        self.auto = ValueTracker(auto_ph) if auto else None
        if layout == "L3":
            geo = [(-5.25, 3.1, 0.75, -0.7), (-2.85, 1.5, 0.62, 0.0), (-1.3, 1.5, 0.62, 0.0)]
            H = 4.9
            idx = [0, 1, 2]
        else:
            geo = {0: (-5.3, 3.0, 0.95, -0.2), active: (-2.15, 3.0, 0.95, -0.2)}
            H = 5.6
            idx = [0, active]
            geo = [geo.get(i) for i in range(3)]
        self.idx, self.H = idx, H
        self.minis, self.frames, self.heads = {}, {}, {}
        for i in idx:
            cx, W, s, ox = geo[i]
            st = dict(states.get(i, {}))
            self.minis[i] = Mini(cx, self.YB, H, s, ox, op=ops, auto=self.auto if i == 0 else None, **st)
            self.frames[i] = RoundedRectangle(corner_radius=0.15, width=W, height=H, stroke_color=GREY, stroke_width=3,
                                              fill_color=GREY, fill_opacity=0.06).move_to([cx, self.YB + H / 2, 0])
            txt = self.PANEL_HEAD[i] if layout == "L3" else self.PANEL_HEAD[i].replace("\n", " ")
            if layout != "L3" and i == 1:
                txt = "LIS1 or dynein\nknockdown"
            self.heads[i] = T(txt, 24, self.PANEL_COL[i], line_spacing=0.8)
            head_x = cx + ({1: -0.18, 2: 0.25}.get(i, 0) if layout == "L3" else 0)
            self.heads[i].move_to([head_x, self.YB + H + 0.12 + self.heads[i].height / 2, 0])

        if self.auto is not None:
            self.auto.add_updater(lambda m, dt: m.increment_value(dt / 4.5))
        self.table = self.make_table()
        self.cells = {}
        for (r, c), (txt, col) in dict(known).items():
            self.cells[(r, c)] = self.cell(r, c, txt, col)
        for (r, c) in qs:
            self.cells[(r, c)] = self.cell(r, c, "?", GOLD)

    def make_table(self):
        g = VGroup()
        xs = [1.3, 3.13, 4.96]
        for y in (2.2, 0.8, -0.6, -2.0):
            g.add(Line([self.TX, y, 0], [6.79, y, 0], color=GREY, stroke_width=2, stroke_opacity=0.7))
        for x in xs:
            g.add(Line([x, 3.1, 0], [x, -2.0, 0], color=GREY, stroke_width=2, stroke_opacity=0.7))
        for (txt, col), x in zip(self.COLS, self.COLX):
            g.add(T(txt, 24, col, line_spacing=0.8).move_to([x, 2.7, 0]))
        for (txt, col), y in zip(self.ROWS, self.ROWY):
            g.add(T(txt, 24, col).move_to([0.4, y, 0]))
        return g

    def cell(self, r, c, text, color=TEXT):
        return T(text, 24, color, line_spacing=0.8).move_to([self.COLX[c], self.ROWY[r], 0])

    def mobs(self):
        out = list(self.frames.values()) + list(self.heads.values()) + [m.mob for m in self.minis.values()]
        out.append(self.table)
        out += list(self.cells.values())
        if self.auto is not None:
            out.append(self.auto)
        return out


def pause_tag():
    return T("Pause and predict.", 32, GOLD, weight=BOLD).move_to([3.4, -3.15, 0])


def slice_caption(lines=("Slices of embryonic rat cortex",), size=24):
    g = VGroup(*[T(s, size, GREY) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    return g.move_to([-6.7, -3.4, 0], aligned_edge=LEFT)


NS = dict(ny=-1.2, cs=1.35, sw=1.0, cage=1.0, fwd=1.0)


def myo_cloud(grey_label):
    """myosin II shown as a diffuse cloud around the whole cell, location unknown"""
    pts = [(-2.55, 0.1, .6), (-2.4, 2.9, .55), (-2.3, -2.7, .55), (1.9, 3.0, .5), (2.1, 1.6, .6),
           (2.4, 0.2, .65), (2.45, -1.3, .6), (1.8, -2.6, .6), (-0.2, -3.2, .5), (0.0, 3.6, .4)]
    cloud = VGroup(*[Circle(radius=r * k, stroke_width=0, fill_color=GREY, fill_opacity=0.085)
                     .move_to([X0 + x, y, 0]) for x, y, r in pts for k in (1.0, 0.75, 0.5)])
    col = GREY if grey_label else PINK
    c = chipfix("myosin II ?", col, 28).move_to([X0 + 2.4, 0.2, 0])
    return VGroup(cloud, c)

# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Radial Migration: Climbing the Glial Ladder"
    TITLE = "What Brings the Nucleus Up"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """two strokes per step: the centrosome moves ahead, then the nucleus catches up; what makes it?"""

    def construct(self):
        rig = Rig(op=0.0)
        self.add(*rig.mobs)
        self.play(rig.t["op"].animate.set_value(1), run_time=0.8)

        c1 = chipfix("stroke 1   centrosome ahead", GREY, 28)
        c2 = chipfix("stroke 2   nucleus catches up", GREY, 28)
        c1.move_to([0.5 + c1.width / 2, 1.1, 0])
        c2.move_to([0.5 + c2.width / 2, 0.1, 0])
        self.at("two strokes")
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(c2, shift=LEFT * 0.2), run_time=0.7)

        lop = ValueTracker(0.0)
        cs_l = rig.cs_label(lop)
        self.add(cs_l)
        self.at("The centrosome")
        self.play(lop.animate.set_value(1), run_time=0.4)
        self.at("moves ahead")
        self.play(*lit(c1, True), *rig.to(cs=0.85), run_time=0.8)

        nop = ValueTracker(0.0)
        nuc_l = rig.nuc_label(nop)
        self.add(nuc_l)
        self.at("then the nucleus")
        self.play(nop.animate.set_value(1), run_time=0.4)
        self.at("catches up")
        self.play(*lit(c1, False), *lit(c2, True), *rig.to(ny=-0.6), run_time=1.3)

        q = T("?", 130, GOLD, weight=BOLD).move_to([-5.6, 1.5, 0])
        self.at("But what makes")
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------

class S02Cage(SpokenScene):
    """a close look: microtubule bundles wrap the nucleus and converge on the centrosome ahead of it"""

    def construct(self):
        rig = Rig(ny=-0.6, cs=0.85, ty=1.8, z=1.75, zc=-0.4, show_tail=False)
        self.add(*rig.mobs, tag())
        ycs, ynu = rig.P(0, 0.85)[1], rig.P(0, -0.6)[1]
        self.add(lab_right("centrosome", YELLOW, 0.7, ycs, [X0 + 0.32, ycs, 0]),
                 lab_right("nucleus", ORANGE, 0.7, ynu, [X0 + 1.0, ynu, 0]))
        em = VGroup(*[T(s, 24, GREY) for s in ("Cage seen by electron microscopy", "in fixed anterior-SVZ neuroblasts",
                                               "from newborn rats (Schaar and", "McConnell, 2005)")])
        em.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([0.7, 2.75, 0], aligned_edge=LEFT)
        self.play(FadeIn(em, shift=UP * 0.1), run_time=0.6)

        pt = ValueTracker(-1.0)

        def pulse():
            p = pt.get_value()
            if p < 0:
                return VGroup()
            return VGroup(*[Dot(rig.cage_pt(w, s, 1 - p), radius=0.12, color=TEXT) for w in (1.22, 1.5) for s in (-1, 1)])
        self.add(always_redraw(pulse))

        self.at("bundles of microtubules")
        self.play(rig.t["cage"].animate.set_value(1.0), run_time=2.2, rate_func=linear)
        tgt = rig.cage_pt(1.5, 1, 0.5)
        mt_l = lab_right("microtubules", TEAL, 0.7, 0.3, tgt + [0.04, 0, 0])
        self.at("like a cage")
        self.play(FadeIn(mt_l), run_time=0.5)
        self.at("They run forward")
        self.play(pt.animate.set_value(1.0), run_time=1.3, rate_func=linear)
        self.play(Indicate(rig.mobs[4], color=YELLOW, scale_factor=1.8), run_time=0.7)
        pt.set_value(-1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Dir(SpokenScene):
    """microtubules have a direction: minus ends at the centrosome, plus ends at the rear of the cage and out front"""

    def construct(self):
        rig = Rig(ny=-0.6, cs=0.85, cage=1.0, ty=2.7, z=1.3, zc=-0.4, lfmax=1.0)
        self.add(*rig.mobs, tag())
        cs = 0.85
        ycs, ynu = rig.P(0, cs)[1], rig.P(0, -0.6)[1]
        self.add(lab_left("centrosome", YELLOW, X0 - 1.25, ycs, [X0 - 0.3, ycs, 0]),
                 lab_right("nucleus", ORANGE, 0.8, ynu, [X0 + 1.05, ynu, 0]))
        self.wait(0.3)
        self.at("have a direction")
        self.play(*[m.animate.set_stroke(width=9) for m in rig.mobs[1]], run_time=0.5)
        self.play(*[m.animate.set_stroke(width=5) for m in rig.mobs[1]], run_time=0.5)

        def mid(side, f):
            return (rig.cage_pt(1.5, side, f) + rig.cage_pt(1.22, side, f)) / 2
        minus = VGroup(*[badge("\u2212", mid(s, 0.0) + [s * 0.27, 0.0, 0]) for s in (-1, 1)])
        lm = T("minus end", 28, TEXT).move_to([1.2 + 0.7, 2.45, 0])
        lead_m = leader([0.85, 2.45, 0], minus[1].get_center() + [0.24, 0.1, 0])
        self.at("minus ends")
        self.play(FadeIn(minus, scale=1.4), FadeIn(lm), Create(lead_m), run_time=0.7)
        self.at("gather at the centrosome")
        self.play(Indicate(rig.mobs[4], color=YELLOW, scale_factor=1.8), run_time=0.8)

        rear = VGroup(*[badge("+", rig.cage_pt(1.5, s, 1.0) + [0, -0.3, 0]) for s in (-1, 1)])
        lp = T("plus end", 28, TEXT).move_to([1.0 + 0.8, -2.65, 0])
        lead_p = leader([0.9, -2.65, 0], rear[1].get_center() + [0.24, 0.0, 0])
        self.at("plus ends")
        self.play(FadeIn(rear, scale=1.4), FadeIn(lp), Create(lead_p), run_time=0.5)
        self.play(rig.t["fwd"].animate.set_value(1.0), run_time=0.3, rate_func=linear)
        front = VGroup(*[badge("+", rig.P(s * 0.3, cs + rig.lf()) + [0, 0.34, 0]) for s in (-1, 1)])
        lf_ = T("plus end", 28, TEXT).move_to([0.6 + 0.8, 3.2, 0])
        lead_f = leader([0.5, 3.2, 0], front[1].get_center() + [0.24, 0.0, 0])
        self.at("away from it")
        self.play(FadeIn(front, scale=1.4), FadeIn(lf_), Create(lead_f), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Motor(SpokenScene):
    """a close-up of one microtubule: the dynein motor walks toward the minus end, toward the centrosome"""

    def construct(self):
        mx = -1.5
        mt = Line([mx, -3.05, 0], [mx, 2.8, 0], color=TEAL, stroke_width=10)
        cs = Dot([mx, 3.05, 0], radius=0.3, color=YELLOW)
        cs_l = lab_right("centrosome", YELLOW, 0.1, 3.05, [mx + 0.4, 3.05, 0])
        minus = T("−", 52, TEXT, weight=BOLD).move_to([mx - 0.75, 2.45, 0])
        plus = T("+", 52, TEXT, weight=BOLD).move_to([mx - 0.75, -2.7, 0])
        self.play(Create(mt), FadeIn(cs), run_time=0.7)
        self.play(FadeIn(minus), FadeIn(plus), FadeIn(cs_l), run_time=0.3)

        y = ValueTracker(-2.3)
        gl = ValueTracker(0.0)
        motor = always_redraw(lambda: dyn_shape(mx, y.get_value(), r=0.32, glow=gl.get_value()))
        d_op = ValueTracker(0.0)
        self.add(dyn(lambda: dyn_shape(mx, y.get_value(), r=0.32, glow=gl.get_value()), d_op))
        self.play(d_op.animate.set_value(1.0), run_time=0.5)
        dl = dyn(lambda: lab_right("dynein", PURPLE, 0.1, y.get_value(), [mx + 1.05, y.get_value(), 0], size=28),
                 ValueTracker(1.0))
        self.add(dl)
        cap = VGroup(T("cytoplasmic dynein", 28, TEXT), T("walks toward minus ends", 28, TEXT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([2.0, -0.3, 0], aligned_edge=LEFT)
        self.at("walks toward minus ends")
        self.play(FadeIn(cap, shift=UP * 0.1), y.animate.set_value(0.4), run_time=1.6, rate_func=linear)
        self.at("toward the centrosome")
        self.play(y.animate.set_value(2.0), run_time=1.1, rate_func=linear)
        self.play(Indicate(cs, color=YELLOW, scale_factor=1.5), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Hold(SpokenScene):
    """two panels open side by side: dynein held in place, dynein attached to something that can move"""

    def construct(self):
        pn = Panels(opa=0.0, opb=0.0)
        self.add(*pn.mobs)
        self.play(*pn.to(opa=1, opb=1), run_time=1.0)
        self.at("what holds it")
        self.play(*pn.to(ha=1, hb=1), run_time=0.7)
        self.finish()


class S06Anch(SpokenScene):
    """panel A: held dynein cannot walk, so it drags the microtubule and the centrosome comes toward it"""

    def construct(self):
        pn = Panels(ha=1.0, hb=1.0)
        self.add(*pn.mobs)
        self.play(*pn.to(**Panels.ACT_A), run_time=0.7)
        self.at("held in place")
        self.play(Indicate(pn.mobs[2], color=TEXT, scale_factor=1.1), run_time=0.7)
        self.at("cannot walk")
        self.play(*pn.to(xl=1.0), run_time=0.4)
        self.at("drags the microtubule")
        self.play(*pn.to(xl=0.0, a=0.7), run_time=2.2, rate_func=linear)
        self.at("the centrosome comes")
        self.play(*pn.to(ar=1.0, a=1.1), run_time=2.0, rate_func=linear)
        self.finish()


class S07Free(SpokenScene):
    """panel B: dynein riding on a disc carries it along the microtubule toward the centrosome"""

    def construct(self):
        pn = Panels(a=1.1, ha=1.0, hb=1.0, ar=1.0, **Panels.ACT_B)
        self.add(*pn.mobs)
        self.wait(0.4)
        self.at("rides on")
        self.play(Indicate(pn.mobs[3], color=TEXT, scale_factor=1.05), run_time=0.8)
        self.at("it carries")
        self.play(*pn.to(b=-0.1), run_time=1.0, rate_func=linear)
        self.at("toward the centrosome")
        self.play(*pn.to(b=1.25), run_time=1.3, rate_func=linear)
        self.play(Indicate(pn.mobs[1], color=YELLOW, scale_factor=1.05), run_time=0.6)
        self.finish()


class S08Beat(NarratedScene):
    """a pause on the two panels"""

    def construct(self):
        pn = Panels(a=1.1, b=1.25, ha=1.0, hb=1.0, ar=1.0)
        self.add(*pn.mobs)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09S1(SpokenScene):
    """back to the neuron: a swelling forms; stroke one, dynein in the swelling pulls the microtubules forward"""

    def construct(self):
        rig = Rig(ny=-1.6, cs=-0.15, sw=0.0, cage=1.0, fwd=1.0, op=0.0)
        self.add(*rig.mobs)
        sm, sg = ValueTracker(0.0), ValueTracker(0.0)
        nm, ng = ValueTracker(0.0), ValueTracker(0.0)
        self.add(swell_marks(rig, sm, sg), nuc_marks(rig, nm, ng), tag())
        one = ValueTracker(0.0)
        self.add(rig.nuc_label(one), rig.cs_label(one))
        self.play(rig.t["op"].animate.set_value(1), one.animate.set_value(1), run_time=0.5)
        swl = lab_right("swelling", BLUE, 0.4, 3.2, [X0 + 0.9, 3.05, 0])
        self.play(*rig.to(sw=1.0), FadeIn(swl, shift=LEFT * 0.2), run_time=1.0)
        self.at("uses both")
        self.play(sm.animate.set_value(0.5), nm.animate.set_value(0.5), run_time=0.6)
        self.at("stroke one")
        arrow = follow_arrow(rig, "cs", X0 + 2.25, -0.2, 0.5)
        chp = follow_chip(rig, "cs", "stroke one", X0 + 2.7, dy=0.15)
        self.add(arrow, chp)
        self.play(nm.animate.set_value(0.0), run_time=0.5)
        dl = lab_right("dynein", PURPLE, 0.4, 2.65, [X0 + 1.3, 2.4, 0], size=26)
        self.at("in the swelling")
        self.play(sm.animate.set_value(1.0), sg.animate.set_value(1.0), FadeIn(dl), run_time=0.6)
        self.at("pulls the microtubules")
        self.play(*rig.to(cs=1.35), run_time=2.5, rate_func=linear)
        self.at("the centrosome comes")
        self.play(Indicate(rig.mobs[4], color=YELLOW, scale_factor=2.0), run_time=0.8)
        self.finish()


class S10S2(SpokenScene):
    """stroke two: dynein on the nucleus walks along the cage and carries the nucleus toward the centrosome"""

    def construct(self):
        rig = Rig(ny=-1.6, cs=1.35, sw=1.0, cage=1.0, fwd=1.0)
        self.add(*rig.mobs)
        sm, sg = ValueTracker(0.0), ValueTracker(0.0)
        nm, ng = ValueTracker(0.0), ValueTracker(0.0)
        self.add(swell_marks(rig, sm, sg), nuc_marks(rig, nm, ng), tag())
        one = ValueTracker(1.0)
        self.add(rig.nuc_label(one), rig.cs_label(one))
        chp1 = chipfix("stroke one", TEXT, 28).move_to([X0 + 2.7 + 0.92, 1.5, 0])
        chp2 = follow_chip(rig, "ny", "stroke two", X0 + 2.7, dy=0.15)
        self.add(chp1)
        self.play(FadeOut(chp1), FadeIn(chp2), run_time=0.5)
        arrow = follow_arrow(rig, "ny", X0 + 2.25, -0.2, 0.5)
        self.add(arrow)
        dl = lab_left("dynein", PURPLE, X0 - 1.95, 0.1, [X0 - 1.05, -0.8, 0])
        self.at("on the nucleus")
        self.play(nm.animate.set_value(1.0), ng.animate.set_value(1.0), FadeIn(dl), run_time=0.7)
        self.at("walks along the cage")
        self.play(*rig.to(ny=-0.5), FadeOut(dl), run_time=4.5, rate_func=linear)
        self.at("which now sits ahead")
        self.play(Indicate(rig.mobs[4], color=YELLOW, scale_factor=2.0), run_time=0.8)
        self.finish()


class S11Lis(SpokenScene):
    """LIS1 tags at both dynein sites: it binds and regulates dynein, it is not the motor"""

    def construct(self):
        rig = Rig(ny=-0.5, cs=1.35, sw=1.0, cage=1.0, fwd=1.0)
        self.add(*rig.mobs)
        sm, sg = ValueTracker(1.0), ValueTracker(0.0)
        nm, ng = ValueTracker(1.0), ValueTracker(0.0)
        self.add(swell_marks(rig, sm, sg), nuc_marks(rig, nm, ng), tag())
        one = ValueTracker(1.0)
        self.add(rig.nuc_label(one), rig.cs_label(one))
        l1 = T("LIS1 binds and regulates dynein;", 28, TEXT)
        l2 = T("it is not the motor.", 28, TEXT)
        lab = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0.5, -1.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.6)
        c1 = chipfix("LIS1", PURPLE, 28).move_to([1.4, 2.9, 0])
        a1 = arr([c1.get_left()[0] - 0.05, 2.88, 0], [X0 + 1.25, 2.38, 0], PURPLE)
        yb = -0.5 + 0.85
        cx = rig.cagex(1.22, yb)
        c2 = chipfix("LIS1", PURPLE, 28).move_to([1.4, yb, 0])
        a2 = arr([c2.get_left()[0] - 0.05, yb, 0], [X0 + cx + 0.22, yb, 0], PURPLE)
        self.at("binds dynein")
        self.play(Indicate(l1, color=PURPLE, scale_factor=1.05), run_time=0.7)
        self.at("in both places")
        self.play(FadeIn(c1), FadeIn(a1), FadeIn(c2), FadeIn(a2), run_time=0.6)
        self.at("not the motor")
        self.play(l2.animate.set_color(GOLD), run_time=0.6)
        self.finish()


class S12Myo(SpokenScene):
    """a second force: an actomyosin icon with a question mark; blebbistatin blocks myosin II"""

    def construct(self):
        rig = Rig(ny=-0.5, cs=1.35, sw=1.0, cage=1.0, fwd=1.0)
        self.add(*rig.mobs)
        sm, sg = ValueTracker(0.35), ValueTracker(0.0)
        nm, ng = ValueTracker(0.35), ValueTracker(0.0)
        self.add(swell_marks(rig, sm, sg), nuc_marks(rig, nm, ng), tag())
        one = ValueTracker(1.0)
        self.add(rig.nuc_label(one), rig.cs_label(one))

        region = DashedVMobject(RoundedRectangle(width=9.2, height=6.5, corner_radius=0.6, stroke_color=GREY, stroke_width=4), num_dashes=64)
        region.move_to([-0.25, 0.25, 0])
        reg_l = T("location argued", 26, GREY).move_to([X0, -3.45, 0])
        actin = Line([0.5, 2.4, 0], [3.9, 2.4, 0], color=GREY, stroke_width=7)
        heads = VGroup(*[Circle(radius=0.2, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.85)
                         .move_to([x, 1.95, 0]) for x in (1.0, 2.0, 3.0)])
        stems = VGroup(*[Line([x, 2.15, 0], [x, 2.4, 0], color=PINK, stroke_width=5) for x in (1.0, 2.0, 3.0)])
        t_act = T("actin", 26, GREY).move_to([2.2, 2.95, 0])
        t_myo = T("myosin II", 28, PINK).move_to([2.2, 1.4, 0])
        icon = VGroup(actin, stems, heads, t_act, t_myo)
        q = T("?", 70, PINK, weight=BOLD).move_to([3.9, 1.4, 0])
        self.wait(0.3)
        self.at("second force")
        self.play(FadeIn(region), FadeIn(reg_l), run_time=0.8)
        self.at("actin and myosin")
        self.play(FadeIn(icon, shift=LEFT * 0.2), run_time=0.8)
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        drug = chipfix("blebbistatin", RED, 28).move_to([2.2, -0.9, 0])
        bar = Line([1.7, 0.75, 0], [2.7, 0.75, 0], color=RED, stroke_width=8)
        stem = Line([2.2, -0.5, 0], [2.2, 0.75, 0], color=RED, stroke_width=8)
        self.at("a drug called")
        self.play(FadeIn(drug, shift=UP * 0.2), run_time=0.6)
        self.at("blocks myosin")
        self.play(FadeIn(VGroup(stem, bar), shift=UP * 0.1), run_time=0.4)
        self.play(Indicate(t_myo, color=RED, scale_factor=1.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tracked_ring(trk, fn):
    return dyn(fn, trk)


class S13Setup(SpokenScene):
    """the experiment: three movies; label tip, centrosome and nucleus; film. The control is shown moving."""

    def construct(self):
        ex = Exp("L3", ops=0.0, auto=False, auto_ph=0.0)
        c0 = ex.minis[0]
        self.add(*[m.mob for m in ex.minis.values()])
        self.play(*[FadeIn(f) for f in ex.frames.values()], *[FadeIn(h) for h in ex.heads.values()],
                  FadeIn(ex.table), *[m.t["op"].animate.set_value(1) for m in ex.minis.values()], run_time=1.2)
        cap = slice_caption(("Slices of embryonic rat cortex;", "blebbistatin also draws on gel experiments"), 24)
        self.at("slices of embryonic", lead=0.45)
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        # a first look at the control movie
        self.at("cortex", lead=-0.2)
        self.play(*c0.to(c=CTL_END["c"], t=CTL_END["t"]), run_time=0.4, rate_func=linear)
        self.play(*c0.to(n=CTL_END["n"]), run_time=0.4, rate_func=linear)
        self.play(*c0.to(n=N0F, c=C0F, t=T0F), run_time=0.15)
        lt, lc, ln = c0.labels()
        self.at("Label the", lead=0.45)
        self.add(lt)
        self.play(FadeIn(lt), run_time=0.2)
        self.at("centrosome", lead=0.45)
        self.add(lc)
        self.play(FadeIn(lc), run_time=0.4)
        self.at("and the nucleus", lead=0.45)
        self.add(ln)
        self.play(FadeIn(ln), run_time=0.4)
        self.at("film the neurons", lead=0.45)
        q1 = ex.cell(0, 0, "extends", TEXT)
        q2 = ex.cell(1, 0, "moves\nahead", TEXT)
        q3 = ex.cell(2, 0, "follows", TEXT)
        self.play(*c0.to(c=CTL_END["c"], t=CTL_END["t"]), FadeIn(q1), FadeIn(q2), run_time=0.7, rate_func=linear)
        self.play(*c0.to(n=CTL_END["n"]), FadeIn(q3), run_time=0.8, rate_func=linear)
        self.finish()


def ctl_cells():
    return Exp.CTL


class S14Predq(SpokenScene):
    """pause and predict: knock down LIS1 or block myosin II; what do tip, centrosome, nucleus do?"""

    def construct(self):
        ex = Exp("L3", known=Exp.CTL)
        self.add(*ex.mobs())
        c0 = ex.minis[0]
        self.add(*c0.labels())
        cap = slice_caption(("Slices of embryonic rat cortex;", "blebbistatin also draws on gel experiments"), 24)
        self.add(cap)
        self.at("Knock down", lead=0.45)
        self.play(Indicate(ex.heads[1], color=PURPLE, scale_factor=1.12), Indicate(ex.table[8], color=PURPLE, scale_factor=1.15),
                  run_time=0.9)
        self.at("or block myosin", lead=0.45)
        self.play(Indicate(ex.heads[2], color=PINK, scale_factor=1.12), Indicate(ex.table[9], color=PINK, scale_factor=1.15),
                  run_time=0.9)
        pp = pause_tag()
        qs = [ex.cell(r, c, "?", GOLD) for r in range(3) for c in (1, 2)]
        self.at("What are the", lead=0.45)
        self.play(FadeIn(pp), *[FadeIn(q, scale=0.7) for q in qs], run_time=0.2)

        trk = {k: ValueTracker(0.0) for k in "tcn"}
        cols = dict(t=BLUE, c=YELLOW, n=ORANGE)

        def rings(k):
            def f():
                g = VGroup()
                for i in ex.idx:
                    m = ex.minis[i]
                    if k == "n":
                        g.add(nring(m.pt("n"), cols[k], 5, 1.36 * m.s + 0.35, 1.7 * m.s + 0.3))
                    else:
                        g.add(ring(m.pt(k), cols[k], 0.3 if k == "c" else 0.28))
                return g
            return dyn(f, trk[k])
        self.add(*[rings(k) for k in "tcn"])
        self.at("the tip", lead=0.45)
        self.play(trk["t"].animate.set_value(1), Indicate(ex.table[10], color=BLUE, scale_factor=1.2), run_time=0.5)
        self.at("the centrosome", lead=0.45)
        self.play(trk["t"].animate.set_value(0), trk["c"].animate.set_value(1),
                  Indicate(ex.table[11], color=YELLOW, scale_factor=1.2), run_time=0.5)
        self.at("the nucleus", lead=0.45)
        self.play(trk["c"].animate.set_value(0), trk["n"].animate.set_value(1),
                  Indicate(ex.table[12], color=ORANGE, scale_factor=1.2), run_time=0.5)
        self.play(trk["n"].animate.set_value(0), run_time=0.4)
        self.finish()


class S15Pause(NarratedScene):
    """hold the question on screen (the control keeps playing for reference)"""

    def construct(self):
        ex = Exp("L3", known=Exp.CTL, qs=[(r, c) for r in range(3) for c in (1, 2)])
        self.add(*ex.mobs())
        self.add(*ex.minis[0].labels())
        self.add(slice_caption(("Slices of embryonic rat cortex;", "blebbistatin also draws on gel experiments"), 24),
                 pause_tag())
        self.finish()


def l2_cap(extra=False):
    first = "Embryonic rat cortex slices, plus gels;" if extra else "Slices of embryonic rat cortex;"
    return slice_caption((first, "other cell types differ."), 24)


class S16Kd(SpokenScene):
    """knockdown movie beside the control: the centrosome and nucleus stall, the tip keeps growing"""

    def construct(self):
        ex = Exp("L2", active=1, known=Exp.CTL, qs=[(r, c) for r in range(3) for c in (1, 2)])
        self.add(*ex.mobs(), l2_cap())
        km = ex.minis[1]
        self.wait(1.0)
        self.at("the centrosome", lead=0.45)
        r1 = ring(km.pt("c"), RED, 0.3)
        self.play(FadeIn(r1, scale=1.6), run_time=0.5)
        self.at("stalls", lead=0.45)
        self.remove(ex.cells[(1, 1)])
        self.play(FadeIn(ex.cell(1, 1, "stalls", RED)), run_time=0.5)
        self.at("The nucleus", lead=0.45)
        r2 = nring(km.pt("n"), RED, 5, 1.36 * km.s + 0.35, 1.7 * km.s + 0.3)
        self.play(FadeIn(r2, scale=1.4), run_time=0.5)
        self.at("stalls too", lead=0.45)
        self.remove(ex.cells[(2, 1)])
        self.play(FadeIn(ex.cell(2, 1, "stalls", RED)), run_time=0.5)
        self.at("the tip keeps", lead=0.45)
        self.remove(ex.cells[(0, 1)])
        self.play(*km.to(t=KD_END["t"]), FadeIn(ex.cell(0, 1, "extends", TEXT)),
                  run_time=1.5, rate_func=linear)
        self.finish()



def kd_marks(scene_adder, ex):
    km = ex.minis[1]
    scene_adder(ring(km.pt("c"), RED, 0.3).set_stroke(opacity=0.6),
                nring(km.pt("n"), RED, 5, 1.36 * km.s + 0.35, 1.7 * km.s + 0.3).set_stroke(opacity=0.6))


class S17Beat(NarratedScene):
    """a pause on the knockdown result; the control keeps playing beside it"""

    def construct(self):
        known = dict(Exp.CTL)
        known.update(Exp.KD)
        ex = Exp("L2", active=1, known=known, qs=[(r, 2) for r in range(3)], states={1: KD_END})
        self.add(*ex.mobs(), l2_cap())
        kd_marks(self.add, ex)
        self.finish()


class S18Bleb(SpokenScene):
    """blebbistatin movie beside the control: the centrosome keeps moving, the nucleus stops, the gap grows"""

    def construct(self):
        known = dict(Exp.CTL)
        known.update(Exp.KD)
        ex = Exp("L2", active=2, known=known, qs=[(r, 2) for r in range(3)])
        self.add(*ex.mobs(), l2_cap(True))
        bm = ex.minis[2]
        self.wait(0.5)
        self.remove(ex.cells[(0, 2)])
        self.play(*bm.to(t=BL_END["t"]), FadeIn(ex.cell(0, 2, "extends", TEXT)),
                  run_time=1.0, rate_func=linear)
        self.at("the centrosome keeps", lead=0.45)
        self.play(*bm.to(c=0.72), run_time=0.45, rate_func=linear)
        self.at("keeps moving", lead=0.45)
        self.remove(ex.cells[(1, 2)])
        self.play(FadeIn(ex.cell(1, 2, "keeps\nmoving", TEXT)), run_time=0.5)
        self.at("The nucleus", lead=0.45)
        r = nring(bm.pt("n"), RED, 5, 1.36 * bm.s + 0.35, 1.7 * bm.s + 0.3)
        self.play(FadeIn(r, scale=1.4), run_time=0.5)
        self.at("stops", lead=0.45)
        self.remove(ex.cells[(2, 2)])
        self.play(FadeIn(ex.cell(2, 2, "stops", RED)), run_time=0.5)

        def gap():
            p = bm.pt("n")
            x = p[0] + 0.62
            return DoubleArrow([x, p[1] + 0.9 * bm.s, 0], [x, bm.pt("c")[1] - 0.2, 0], color=TEXT, stroke_width=6,
                               tip_length=0.22, buff=0, max_tip_length_to_length_ratio=0.45)

        def gap_label():
            p = bm.pt("n")
            x = p[0] + 0.62
            y = (p[1] + 0.9 * bm.s + bm.pt("c")[1] - 0.2) / 2
            return T("gap", 26, TEXT).move_to([x + 0.42, y, 0])
        self.at("the gap", lead=0.45)
        self.add(always_redraw(gap), always_redraw(gap_label))
        self.play(*bm.to(c=BL_END["c"]), run_time=2.0, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------

def myo_state(grey_label):
    return myo_cloud(grey_label)


def pull_chip():
    c = chipfix("dynein pull", PURPLE, 28).move_to([1.7, 2.3, 0])
    a = arr([c.get_left()[0] - 0.05, 2.3, 0], [X0 + 1.3, 2.3, 0], PURPLE)
    return VGroup(c, a)


class S19Blebwhy(SpokenScene):
    """the dynein pull is still there, but the nucleus has lost a force: myosin II shown as a diffuse, unlocated cloud"""

    def construct(self):
        rig = Rig(**NS)
        self.add(*rig.mobs)
        sm, sg = ValueTracker(1.0), ValueTracker(1.0)
        self.add(swell_marks(rig, sm, sg), tag())
        one = ValueTracker(1.0)
        self.add(rig.nuc_label(one), rig.cs_label(one))
        pc = pull_chip()
        self.play(FadeIn(pc), run_time=0.6)
        self.at("still there")
        self.play(Indicate(pc[0], color=PURPLE, scale_factor=1.12), run_time=0.7)
        mp, mg = myo_cloud(False), myo_cloud(True)
        self.at("but the nucleus")
        self.play(FadeIn(mp), run_time=0.6)
        self.at("lost a force")
        self.play(ReplacementTransform(mp, mg), run_time=0.8)
        self.finish()


class S20Beat(NarratedScene):
    """a pause on the lost force"""

    def construct(self):
        rig = Rig(**NS)
        self.add(*rig.mobs)
        sm, sg = ValueTracker(1.0), ValueTracker(1.0)
        self.add(swell_marks(rig, sm, sg), tag())
        one = ValueTracker(1.0)
        self.add(rig.nuc_label(one), rig.cs_label(one))
        self.add(pull_chip(), myo_cloud(True))
        self.finish()


class S21Dispute(SpokenScene):
    """where does myosin II act: behind the nucleus or at the front?"""

    def construct(self):
        rig = Rig(**NS)
        self.add(*rig.mobs)
        sm, sg = ValueTracker(1.0), ValueTracker(1.0)
        self.add(swell_marks(rig, sm, sg), tag())
        one = ValueTracker(1.0)
        self.add(rig.nuc_label(one), rig.cs_label(one))
        pc, mg = pull_chip(), myo_cloud(True)
        self.add(pc, mg)
        self.at("where myosin")
        self.play(FadeOut(pc), FadeOut(mg), sm.animate.set_value(0.0), rig.t["cop"].animate.set_value(0.3),
                  run_time=0.6)
        ny = -1.2
        back = arr([X0 + 1.1, -2.75, 0], [X0 + 1.1, -1.85, 0], PINK, w=9, tip=0.3)
        back_t = T("behind the nucleus", 28, PINK).move_to([X0 + 1.3 + 1.7, -2.3, 0])
        back_q = T("?", 64, PINK, weight=BOLD).move_to([X0 + 1.3 + 3.95, -2.3, 0])
        self.at("behind the nucleus")
        self.play(GrowArrow(back), FadeIn(back_t), run_time=0.7)
        self.play(FadeIn(back_q, scale=0.6), run_time=0.4)
        front = arr([X0 + 0.5, 1.45, 0], [X0 + 0.5, 2.75, 0], PINK, w=9, tip=0.3)
        front_t = T("at the front", 28, PINK).move_to([X0 + 1.5 + 1.0, 2.1, 0])
        front_q = T("?", 64, PINK, weight=BOLD).move_to([X0 + 1.5 + 2.45, 2.1, 0])
        self.at("at the front")
        self.play(GrowArrow(front), FadeIn(front_t), run_time=0.7)
        self.play(FadeIn(front_q, scale=0.6), run_time=0.4)
        self.at("still argued")
        self.play(Indicate(back_q, color=PINK, scale_factor=1.3), Indicate(front_q, color=PINK, scale_factor=1.3),
                  run_time=0.8)
        self.finish()


class S22Take(SpokenScene):
    """closing card: a cell can keep reaching without arriving; measure at the nucleus"""

    def construct(self):
        rig = Rig(**NS)
        rig.t["cage"].set_value(0.0)
        rig.t["fwd"].set_value(0.0)
        self.add(*rig.mobs, tag())
        l1 = T("A cell can keep reaching", 38, TEXT).move_to([0.6, 1.9, 0], aligned_edge=LEFT)
        l2 = T("without arriving.", 38, TEXT).next_to(l1, DOWN, aligned_edge=LEFT, buff=0.2)
        l3 = T("Measure at the nucleus.", 38, GOLD, weight=BOLD).move_to([0.6, -0.5, 0], aligned_edge=LEFT)
        self.wait(0.2)
        self.at("keep reaching")
        self.play(FadeIn(l1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("without arriving")
        self.play(FadeIn(l2, shift=RIGHT * 0.2), run_time=0.6)
        stay = ring(rig.P(0, -1.2), GOLD, 1.25)
        self.at("Measure migration")
        self.play(FadeIn(l3, shift=RIGHT * 0.2), FadeIn(stay, scale=1.2), run_time=0.9)
        self.finish()


class S23End(EndCard):
    LINE = "A cell can keep reaching without arriving.\nMeasure migration at the nucleus."
