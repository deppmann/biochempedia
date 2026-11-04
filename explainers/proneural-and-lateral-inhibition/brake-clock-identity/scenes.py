"""Proneural genes and lateral inhibition, chapter 6: Vertebrates: a Brake, a Clock and Identity  (Biochemistrypedia chaptered film)

COLOR MAP (one colour per concept, shared with every chapter of the series)
  GREEN   = proneural activity and the neural fate (cell rim, neurons); here also Ascl1 (achaete-scute family)
  YELLOW  = Delta / Dll1 (knob on the membrane, the Dll1 trace)
  BLUE    = Notch (cup on the membrane, Notch activity, "held back" / progenitor rim)
  RED     = Hes repressors (Hes1, Hes5) and every inhibition mark; also the cross that means removed / not
  GREY    = cells, nuclei, DNA, axes, labels
  GOLD    = the question mark, the prompt cards, "compete again" and the tissue brick
  TEAL    = Neurog2 (atonal-type proneural family) and the dorsal forebrain
  TEXT    = plain text, the light used in the optogenetic prompt
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PRO, DEL, NOT, REP, NG2 = GREEN, YELLOW, BLUE, RED, TEAL
ASC = GREEN
LIGHT = TEXT


# ------------------------------------------------------------------------------------------------
# small helpers
# ------------------------------------------------------------------------------------------------
def P3(x, y, z=0.0):
    return np.array([float(x), float(y), 0.0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(P3(*a) if len(a) == 2 else np.array(a, float), P3(*b) if len(b) == 2 else np.array(b, float), buff=0.06,
                 color=color, stroke_width=w, tip_length=tip, max_tip_length_to_length_ratio=0.35)


def inhib(a, b, color=RED, w=5, half=0.24):
    """A line that ends in a bar: the sign for 'inhibits'."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.06
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * half, b - perp * half, color=color, stroke_width=w + 1))


def cross_mark(c, s=0.35, color=RED, w=8):
    c = np.array([c[0], c[1], 0.0])
    return VGroup(Line(c + P3(-s, -s), c + P3(s, s), color=color, stroke_width=w),
                  Line(c + P3(-s, s), c + P3(s, -s), color=color, stroke_width=w))


def clock_icon(c, r=0.42, color=GREY, hand_color=None):
    c = P3(*c)
    face = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(c)
    h1 = Line(c, c + UP * r * 0.8, color=hand_color or color, stroke_width=5)
    h2 = Line(c, c + RIGHT * r * 0.5, color=hand_color or color, stroke_width=4)
    g = VGroup(face, h1, h2)
    g.hand = h1
    g.center_pt = c
    return g


def sun_icon(c, r=0.2, color=LIGHT):
    c = P3(*c)
    core = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).move_to(c)
    rays = [Line(c + r * 1.45 * P3(np.cos(a), np.sin(a)), c + r * 2.1 * P3(np.cos(a), np.sin(a)), color=color, stroke_width=3)
            for a in np.linspace(0, 2 * PI, 9)[:-1]]
    return VGroup(core, *rays)


def cup(x_edge, y, facing, r=0.2, color=NOT, w=6):
    """Notch: a cup on a membrane edge that opens toward `facing` (+1 right, -1 left)."""
    if facing > 0:
        return Arc(radius=r, start_angle=PI / 2, angle=PI, arc_center=P3(x_edge + r, y), color=color, stroke_width=w)
    return Arc(radius=r, start_angle=-PI / 2, angle=PI, arc_center=P3(x_edge - r, y), color=color, stroke_width=w)


def knob(x_edge, y, facing, r=0.14, stalk=0.18, color=DEL):
    """Delta: a knob on a short stalk, pointing toward `facing`."""
    tip = P3(x_edge + facing * stalk, y)
    return VGroup(Line(P3(x_edge, y), tip, color=GREY, stroke_width=4),
                  Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.9).move_to(tip + P3(facing * r, 0)))


def ch(text, color=BLUE, size=26, pad=0.16):
    return chip(text, color, size=size, pad=pad)


def neuron_blob(x, y, r=0.5):
    return Circle(radius=r, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.4).move_to(P3(x, y))


class Sc(SpokenScene):
    def until(self, t):
        """Wait until t seconds into the scene (for a moment the transcript did not catch)."""
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


# ------------------------------------------------------------------------------------------------
# the neural tube (a ring of cells) and the strip of wall used for most of the first half
# ------------------------------------------------------------------------------------------------
class Ring:
    def __init__(self, center=(-3.1, 0.0), r0=1.25, r1=3.5, n=18):
        self.c, self.r0, self.r1, self.n = center, r0, r1, n

    def pt(self, r, a, warp=False, outer=True):
        if warp:
            s = 1 + 0.08 * np.sin(3 * a) + 0.04 * np.cos(5 * a + 1) if outer else 1 + 0.45 * np.sin(2 * a + 0.3)
            r = r * s
            cx, cy = self.c[0] + 0.1, self.c[1] - 0.1
        else:
            cx, cy = self.c
        return P3(cx + r * np.cos(a), cy + r * np.sin(a))

    def cells(self, gap=0.05, warp=False, rim=GREY, op=0.08):
        out = []
        for i in range(self.n):
            a0, a1 = 2 * PI * i / self.n + gap, 2 * PI * (i + 1) / self.n - gap
            pts = [self.pt(self.r1, a, warp, True) for a in np.linspace(a0, a1, 7)] + [self.pt(self.r0, a, warp, False) for a in np.linspace(a1, a0, 7)]
            out.append(Polygon(*pts, stroke_color=rim, stroke_width=3, fill_color=GREY, fill_opacity=op))
        return out

    def mid(self, i, off=0.0):
        a = 2 * PI * (i + 0.5) / self.n
        return self.pt((self.r0 + self.r1) / 2, a), P3(-np.sin(a), np.cos(a)), a


SX = [-5.425 + 1.55 * i for i in range(8)]
SY, SW, SH = 0.35, 1.0, 5.0
NY = -3.0   # y of a neuron that has left the wall


def pcell(i):
    return RoundedRectangle(corner_radius=0.45, width=SW, height=SH, stroke_color=GREY, stroke_width=3.5,
                            fill_color=GREY, fill_opacity=0.08).move_to(P3(SX[i], SY))


def pnuc(i):
    return Circle(radius=0.36, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to(P3(SX[i], SY)).set_stroke(opacity=0.7)


def blob(i):
    return neuron_blob(SX[i], NY)


class Wall:
    """The strip of eight progenitors (a slice through the neural tube wall)."""

    def __init__(self):
        self.cells = [pcell(i) for i in range(8)]
        self.nucs = [pnuc(i) for i in range(8)]

    def show(self, scene, fade=False):
        grp = []
        for i in range(8):
            grp += [self.cells[i], self.nucs[i]]
        if fade:
            scene.play(LaggedStart(*[FadeIn(m) for m in grp], lag_ratio=0.04), run_time=0.8)
        else:
            scene.add(*grp)


# ------------------------------------------------------------------------------------------------
# plots computed from equations
# ------------------------------------------------------------------------------------------------
class Plot:
    def __init__(self, x0, x1, y0, y1, tmax, ymax=1.0):
        self.x0, self.x1, self.y0, self.y1, self.tmax, self.ymax = x0, x1, y0, y1, tmax, ymax

    def pt(self, t, v):
        return P3(self.x0 + (self.x1 - self.x0) * t / self.tmax, self.y0 + (self.y1 - self.y0) * v / self.ymax)

    def axes(self, ticks=(), xlab=None, ylab=None, size=26, yaxis=True, yticks=(), ylab_dx=0.55):
        g = [Arrow(P3(self.x0, self.y0), P3(self.x1 + 0.25, self.y0), color=GREY, stroke_width=3, buff=0, tip_length=0.18,
                   max_tip_length_to_length_ratio=0.2)]
        if yaxis:
            g.append(Line(P3(self.x0, self.y0), P3(self.x0, self.y1 + 0.1), color=GREY, stroke_width=3))
        for t in ticks:
            p = self.pt(t, 0)
            g.append(Line(p + DOWN * 0.07, p + UP * 0.07, color=GREY, stroke_width=3))
            g.append(T(str(t), size, GREY).move_to(p + DOWN * 0.32))
        for v, txt in yticks:
            p = self.pt(0, v)
            g.append(Line(p + LEFT * 0.08, p + RIGHT * 0.08, color=GREY, stroke_width=3))
            g.append(T(txt, size, GREY).next_to(p + LEFT * 0.12, LEFT, buff=0.05))
        if xlab:
            g.append(T(xlab, size, GREY).move_to(P3(self.x1 - 0.1, self.y0 - (0.7 if ticks else 0.5))).align_to(P3(self.x1 + 0.3, 0), RIGHT))
        if ylab:
            lab = T(ylab[0], size, ylab[1]).rotate(PI / 2)
            lab.move_to(P3(self.x0 - ylab_dx, (self.y0 + self.y1) / 2))
            g.append(lab)
        return VGroup(*g)

    def curve(self, ts, vs, color, w=5, i0=0, i1=None):
        i1 = len(ts) if i1 is None else i1
        pts = [self.pt(t, v) for t, v in zip(ts[i0:i1], vs[i0:i1])]
        m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
        m.set_points_as_corners(pts)
        return m


def hes_series(tau, drop=None, T_win=9.0, warm=8.0, dt=0.01, a=20.0, n=6, P0=0.3, mu=2.2):
    """Hes1 as a delayed negative feedback loop (mRNA m, protein p):
         dm/dt = a / (1 + (p(t - tau) / P0)^n) - mu m      dp/dt = m - mu p
    Returns time (hours, from 0 at the start of the window) and Hes1 protein scaled to 0..1.
    With `drop` (hours into the window) the production term decays away, as in a cell that leaves the cycle."""
    N = int((warm + T_win) / dt)
    d = int(tau / dt)
    m = np.zeros(N + 1)
    p = np.zeros(N + 1)
    m[0], p[0] = 0.2, 0.05
    for i in range(N):
        pd = p[i - d] if i >= d else 0.0
        al = a
        if drop is not None and i * dt > warm + drop:
            al = a * np.exp(-(i * dt - warm - drop) / 0.35)
        m[i + 1] = m[i] + dt * (al / (1 + (pd / P0) ** n) - mu * m[i])
        p[i + 1] = p[i] + dt * (m[i] - mu * p[i])
    w0 = int(warm / dt)
    return np.arange(N + 1 - w0) * dt, p[w0:]


def lag_hill(t, pn, K=0.5, nH=4, tl=0.15):
    """A target repressed by Hes1 (Hill function), followed with a short lag."""
    target = 1 / (1 + (pn / K) ** nH)
    y = np.zeros_like(pn)
    y[0] = target[0]
    for i in range(1, len(t)):
        y[i] = y[i - 1] + (t[i] - t[i - 1]) * (target[i - 1] - y[i - 1]) / tl
    return y


_NORM = {}


def hes_norm(tau):
    """Scale Hes1 protein to 0..1 using the undisturbed oscillation, so a dropped run uses the same scale."""
    if tau not in _NORM:
        t, p = hes_series(tau)
        _NORM[tau] = (p.min(), p.max())
    lo, hi = _NORM[tau]
    return lo, hi


def traces(tau, drop=None, T_win=9.0):
    t, p = hes_series(tau, drop=drop, T_win=T_win)
    lo, hi = hes_norm(tau)
    pn = np.clip((p - lo) / (hi - lo), 0, 1.05)
    ng = lag_hill(t, pn, tl=0.10)      # Neurog2 and Dll1 follow Hes1 repression with the same short lag,
    dl = lag_hill(t, pn, tl=0.12)      # so they peak together, opposite to Hes1
    return t, pn, ng, dl


def peaks(t, y, lo=0.0):
    return [i for i in range(1, len(y) - 1) if y[i] > y[i - 1] and y[i] >= y[i + 1] and t[i] > lo]


def troughs(t, y, lo=0.0):
    return [i for i in range(1, len(y) - 1) if y[i] < y[i - 1] and y[i] <= y[i + 1] and t[i] > lo]


# ------------------------------------------------------------------------------------------------
# the forebrain cross-section: two hemispheres, each with a dorsal cortex and a ventral eminence
# ------------------------------------------------------------------------------------------------
FC = (-3.3, 0.0)
LOBES = (-4.85, -1.75)
FRX, FRY, FCUT = 1.5, 3.0, 0.3


def lobe_pt(cx, th):
    return P3(cx + FRX * np.cos(th), FRY * np.sin(th))


class Fore:
    def __init__(self):
        th1 = np.arcsin(FCUT / FRY)
        self.dors, self.vent, self.outline, self.cuts = [], [], [], []
        for cx in LOBES:
            top = [lobe_pt(cx, t) for t in np.linspace(th1, PI - th1, 40)]
            bot = [lobe_pt(cx, t) for t in np.linspace(PI - th1, 2 * PI + th1, 60)]
            self.dors.append(Polygon(*top, stroke_width=0, fill_color=TEAL, fill_opacity=0.0))
            self.vent.append(Polygon(*bot, stroke_width=0, fill_color=GREEN, fill_opacity=0.0))
            self.outline.append(Ellipse(width=2 * FRX, height=2 * FRY, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                                        fill_opacity=0.07).move_to(P3(cx, 0)))
            dx = FRX * np.cos(th1)
            self.cuts.append(DashedLine(P3(cx - dx, FCUT), P3(cx + dx, FCUT), color=GREY, stroke_width=2.5, dash_length=0.15))
        self.l_dors = T("dorsal: cortex", 26, GREY).move_to(P3(FC[0], 3.5))
        self.l_vent = T("ventral: ganglionic eminences", 26, GREY).move_to(P3(FC[0], -3.5))
        self.base = VGroup(*self.outline, *self.dors, *self.vent, *self.cuts, self.l_dors, self.l_vent)

    def shade_dors(self, op=0.35):
        return [d.animate.set_fill(TEAL, op) for d in self.dors] + [self.l_dors.animate.set_color(TEAL)]

    def shade_vent(self, op=0.35):
        return [v.animate.set_fill(GREEN, op) for v in self.vent] + [self.l_vent.animate.set_color(GREEN)]

    def shade_now(self):
        for d in self.dors:
            d.set_fill(TEAL, 0.35)
        for v in self.vent:
            v.set_fill(GREEN, 0.35)
        self.l_dors.set_color(TEAL)
        self.l_vent.set_color(GREEN)


POS_D, POS_V = P3(FC[0], 1.55), P3(FC[0], -1.55)


def predict_banner(x=3.6, y=3.3):
    return ch("Predict", GOLD, size=32).move_to(P3(x, y))


# ==============================================================================================
class S00Title(TitleCard):
    LESSON = "Proneural genes and lateral inhibition"
    TITLE = "Vertebrates: a Brake, a Clock and Identity"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD)
        lesson = T(self.LESSON.upper(), size=26, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(title, max_w=12.0)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.36)
        self.play(FadeIn(g, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S01Question(Sc):
    def construct(self):
        rg = Ring(center=(-3.1, 0.0), r0=1.25, r1=3.5, n=18)
        cells = rg.cells()
        nucs = [Dot(rg.mid(i)[0], radius=0.17, color=GREY) for i in range(rg.n)]
        self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cells], lag_ratio=0.03), FadeIn(VGroup(*nucs)), run_time=0.8)
        self.at("neural tube")
        t1 = T("neural tube", 36, TEXT).move_to(P3(4.0, 2.9))
        ld = Line(P3(2.2, 2.85), rg.pt(3.4, 0.8), color=GREY, stroke_width=3)
        self.play(FadeIn(t1, shift=LEFT * 0.2), Create(ld), run_time=0.5)

        def divide(idx):
            anims, extra, furrows = [], [], []
            for i in idx:
                c, tang, a = rg.mid(i)
                e = Dot(c, radius=0.17, color=GREY)
                extra.append(e)
                fur = Line(rg.pt(1.4, 2 * PI * (i + 0.5) / rg.n), rg.pt(3.35, 2 * PI * (i + 0.5) / rg.n), color=GREY, stroke_width=3)
                furrows.append(fur)
                anims += [nucs[i].animate.shift(tang * 0.3), e.animate.shift(-tang * 0.3)]
            self.add(*extra)
            return anims, furrows

        anims, furrows = divide((2, 8, 14))
        self.play(*anims, *[Create(f) for f in furrows], run_time=0.7)
        self.at("already neural")
        t2 = T("cells already neural", 36, GREEN).move_to(P3(3.9, 1.55))
        ld2 = Line(P3(1.5, 1.45), rg.pt(3.4, 0.25), color=GREEN, stroke_width=3)
        self.play(*[c.animate.set_stroke(GREEN, 4) for c in cells], FadeIn(t2, shift=LEFT * 0.2), Create(ld2), run_time=0.8)
        self.at("so what")
        q = VGroup(T("What do the same", 46, GOLD, font=TITLE_FONT), T("parts do here?", 46, GOLD, font=TITLE_FONT)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        q.move_to(P3(3.7, -0.8))
        self.play(FadeIn(q), run_time=0.35)
        self.at("same parts")
        anims, furrows = divide((5, 11, 17))
        self.play(*anims, *[Create(f) for f in furrows], *[Indicate(c, color=GOLD, scale_factor=1.05) for c in cells[::3]], run_time=1.2)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S02Push(Sc):
    def construct(self):
        w = Wall()
        for c_ in w.cells:
            c_.stretch_to_fit_height(5.5).move_to(P3(c_.get_center()[0], 0.3))
        w.show(self, fade=True)
        self.at("pronural factors")
        pf = ch("proneural factors", PRO, size=26).move_to(P3(SX[3], 3.45))
        self.play(FadeIn(pf, shift=DOWN * 0.15), run_time=0.5)
        self.at("push")
        ar = arr((SX[3], 3.1), (SX[3], SY + 0.55), PRO, 7)
        self.play(GrowArrow(ar), w.nucs[3].animate.set_fill(GREEN, 0.7).set_stroke(GREEN, 4), w.cells[3].animate.set_stroke(GREEN, 4), run_time=0.8)
        self.at("become a neuron")
        b = neuron_blob(SX[3], -3.3, 0.45)
        lab = T("neuron", 28, GREEN).move_to(P3(SX[3] + 1.35, -3.3))
        self.play(FadeOut(pf), FadeOut(ar), FadeOut(w.nucs[3]), ReplacementTransform(w.cells[3], b), FadeIn(lab, shift=UP * 0.1), run_time=1.0)
        self.at("Notch holds")
        cups = [cup(SX[2] + 0.5, SY, +1, 0.3, w=9), cup(SX[4] - 0.5, SY, -1, 0.3, w=9)]
        nl = ch("Notch", NOT, size=28).move_to(P3(SX[3], 3.45))
        self.play(FadeIn(nl, shift=DOWN * 0.15), *[Create(c) for c in cups], run_time=0.6)
        self.at("neighbors")
        pl = [T("progenitor", 26, NOT).move_to(P3(SX[i], -2.72)) for i in (2, 4)]
        self.play(*[w.cells[i].animate.set_stroke(NOT, 6) for i in (2, 4)], *[FadeIn(p, shift=UP * 0.1) for p in pl], run_time=0.6)
        self.at("as progenitors")
        self.play(*[Indicate(w.nucs[i], color=TEXT, scale_factor=1.4) for i in (0, 1, 2, 4, 5, 6, 7)], run_time=0.9)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S03Hes(Sc):
    def construct(self):
        ls = RoundedRectangle(corner_radius=0.2, width=5.8, height=1.0, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(P3(-3.6, 2.6))
        rs = RoundedRectangle(corner_radius=0.2, width=3.3, height=1.0, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(P3(4.7, 2.6))
        slots = VGroup(DashedVMobject(ls, num_dashes=30), DashedVMobject(rs, num_dashes=22))
        dna = Rectangle(width=9.0, height=0.3, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35).move_to(P3(0, -2.6))
        gene = RoundedRectangle(corner_radius=0.15, width=5.4, height=1.0, stroke_color=PRO, stroke_width=4, fill_color=PRO, fill_opacity=0.35).move_to(P3(0, -1.8))
        gl = T("proneural gene", 32, PRO).move_to(gene)
        self.play(FadeIn(slots), FadeIn(dna), FadeIn(gene), FadeIn(gl), run_time=0.5)
        self.at("relatives")
        rel = DoubleArrow(P3(-0.5, 2.6), P3(2.8, 2.6), color=GREY, stroke_width=5, buff=0, tip_length=0.22)
        rl = T("relatives", 26, GREY).move_to(P3(1.15, 3.2))
        self.play(GrowFromCenter(rel), FadeIn(rl), run_time=0.6)
        self.at("enhancer of split")
        e = ch("Enhancer of split, E(spl)", REP, size=28).move_to(P3(-3.6, 2.6))
        fly = T("fly", 26, GREY).move_to(P3(-3.6, 1.85))
        self.play(FadeOut(slots[0]), run_time=0.15)
        self.play(FadeIn(e, scale=0.85), FadeIn(fly), run_time=0.45)
        self.at("hes genes")
        h = ch("Hes genes", REP, size=32).move_to(P3(4.7, 2.6))
        vt = T("vertebrate", 26, GREY).move_to(P3(4.7, 1.85))
        self.play(FadeOut(slots[1]), run_time=0.15)
        self.play(FadeIn(h, scale=0.85), FadeIn(vt), run_time=0.45)
        self.at("hes inhibits")
        hc = ch("Hes", REP, size=34).move_to(P3(0, 0.45))
        self.play(FadeIn(hc, scale=0.7), run_time=0.6)
        self.at("pronural genes")
        ib = inhib(P3(0, 0.05), P3(0, -1.2), REP, 8, 0.5)
        self.play(Create(ib), gene.animate.set_fill(PRO, 0.05).set_stroke(PRO, 4, opacity=0.3), gl.animate.set_opacity(0.35), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S04Parts(Sc):
    def construct(self):
        cell = RoundedRectangle(corner_radius=1.4, width=6.2, height=7.0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08)
        nuc = Circle(radius=2.6, stroke_color=GREY, stroke_width=3, fill_opacity=0).set_stroke(opacity=0.7).move_to(P3(0, 0.1))
        cl = T("progenitor", 28, GREY).move_to(P3(0, 3.05))
        self.play(FadeIn(cell), FadeIn(nuc), FadeIn(cl), run_time=0.6)
        self.at("notch")
        c1 = cup(-3.1, 0.6, -1, 0.35, w=9)
        l1 = ch("Notch", NOT, size=30).move_to(P3(-5.4, 0.6))
        ld1 = Line(P3(-4.5, 0.6), P3(-3.5, 0.6), color=GREY, stroke_width=3)
        self.play(Create(c1), FadeIn(l1, shift=RIGHT * 0.2), Create(ld1), run_time=0.6)
        self.at("ligand")
        k = knob(3.1, 0.6, +1, 0.24, 0.3)
        self.play(FadeIn(k, shift=LEFT * 0.2), run_time=0.5)
        self.at("delta like")
        l2 = ch("Dll1", DEL, size=30).move_to(P3(5.4, 0.6))
        ld2 = Line(P3(4.65, 0.6), P3(3.75, 0.6), color=GREY, stroke_width=3)
        self.play(FadeIn(l2, shift=LEFT * 0.2), Create(ld2), run_time=0.5)
        self.at("repressors")
        rl = T("repressors", 30, REP).move_to(P3(0, 1.95))
        self.play(FadeIn(rl, shift=DOWN * 0.1), run_time=0.4)
        self.at("hess one")
        a = ch("Hes1", REP, size=36).move_to(P3(-1.15, 0.95))
        self.play(FadeIn(a, scale=0.8), run_time=0.4)
        self.at("hess five")
        b = ch("Hes5", REP, size=36).move_to(P3(1.15, 0.95))
        self.play(FadeIn(b, scale=0.8), run_time=0.4)
        self.at("pronural factors")
        pl = T("proneural factors", 30, PRO).move_to(P3(0, -0.05))
        c = ch("Ascl1", ASC, size=36).move_to(P3(-1.2, -1.0))
        d = ch("Neurog2", NG2, size=34).move_to(P3(1.3, -1.0))
        self.play(FadeIn(pl, shift=UP * 0.1), FadeIn(c, scale=0.8), FadeIn(d, scale=0.8), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S05Dll1(Sc):
    def construct(self):
        w = Wall()
        w.show(self)
        self.at("starts to differentiate")
        self.play(w.nucs[3].animate.set_fill(GREEN, 0.55).set_stroke(GREEN, 4),
                  w.cells[3].animate.set_stroke(GREEN, 5).set_fill(GREEN, 0.2), run_time=0.9)
        self.at("raises")
        kl = knob(SX[3] - 0.5, SY, -1, 0.17, 0.22)
        kr = knob(SX[3] + 0.5, SY, +1, 0.17, 0.22)
        base = Line(P3(SX[3] - 0.25, -2.0), P3(SX[3] + 0.25, -2.0), color=GREY, stroke_width=3)
        bar = Rectangle(width=0.36, height=0.1, stroke_width=0, fill_color=DEL, fill_opacity=0.9).move_to(P3(SX[3], -2.0 + 0.05))
        self.add(base)
        self.play(FadeIn(kl, scale=0.4), FadeIn(kr, scale=0.4), Transform(bar, Rectangle(width=0.36, height=0.7, stroke_width=0, fill_color=DEL, fill_opacity=0.9).move_to(P3(SX[3], -2.0 + 0.35))), run_time=0.8)
        self.at("delta like")
        lab = ch("Dll1", DEL, size=30).move_to(P3(SX[3], 3.4))
        self.play(FadeIn(lab, shift=DOWN * 0.1), Transform(bar, Rectangle(width=0.36, height=1.9, stroke_width=0, fill_color=DEL, fill_opacity=0.9).move_to(P3(SX[3], -2.0 + 0.95))), run_time=1.5)
        self.at("that keeps")
        cl = cup(SX[2] + 0.5, SY, +1, 0.3, w=9)
        cr = cup(SX[4] - 0.5, SY, -1, 0.3, w=9)
        self.play(Create(cl), Create(cr), run_time=0.7)
        self.at("around it")
        self.play(w.cells[2].animate.set_stroke(NOT, 6), w.cells[4].animate.set_stroke(NOT, 6), run_time=0.6)
        self.at("as progenitors")
        pl = [T("stay\nprogenitors", 26, NOT).move_to(P3(SX[i], -2.85)) for i in (2, 4)]
        self.play(*[FadeIn(p, shift=UP * 0.1) for p in pl], run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S06Spaced(Sc):
    def construct(self):
        w = Wall()
        for i_ in range(8):
            w.cells[i_].stretch_to_fit_height(5.8).move_to(P3(SX[i_], 0.15))
            w.nucs[i_].move_to(P3(SX[i_], 0.15))
        w.show(self)
        day = T("Day 1", 34, TEXT).move_to(P3(3.4, 3.45))
        sch = T("schematic", 26, GREY).move_to(P3(5.6, 3.45))
        self.add(day, sch)

        def to_neuron(i, flash=False):
            an = [w.cells[i].animate.set_fill(GREEN, 0.4).set_stroke(GREEN, 5), w.nucs[i].animate.set_fill(GREEN, 0.7).set_stroke(GREEN, 4)]
            if flash:
                an.append(Flash(P3(SX[i], 0.15), color=GOLD, line_length=0.35, flash_radius=0.9, num_lines=10))
                an.append(Indicate(w.cells[i], color=GOLD, scale_factor=1.1))
            return an

        self.at("first appear")
        self.play(*to_neuron(1), *to_neuron(5), run_time=0.7)
        self.at("spaced apart")
        sp = DoubleArrow(P3(SX[1], -3.05), P3(SX[5], -3.05), color=GREY, stroke_width=5, buff=0, tip_length=0.22)
        spl = T("spaced apart", 28, GREY).move_to(P3((SX[1] + SX[5]) / 2, -3.5))
        self.play(GrowFromCenter(sp), FadeIn(spl), run_time=0.6)
        self.at("new ones")
        d2 = T("Day 2", 34, TEXT).move_to(day)
        self.play(FadeOut(sp), FadeOut(spl), ReplacementTransform(day, d2), run_time=0.5)
        self.at("the gaps")
        gp = T("new ones in the gaps", 28, GOLD).move_to(P3(-3.6, 3.45))
        self.play(*to_neuron(3, True), *to_neuron(7, True), FadeIn(gp), run_time=0.7)
        self.at("cells leave")
        d3 = T("Day 3", 34, TEXT).move_to(d2)
        leave = []
        for i in (1, 3, 5, 7):
            leave += [ReplacementTransform(w.cells[i], neuron_blob(SX[i], -3.25, 0.5)), FadeOut(w.nucs[i])]
        self.play(ReplacementTransform(d2, d3), FadeOut(gp), *leave, run_time=0.6)
        self.at("the pool")
        pool = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=12.6, height=6.1, stroke_color=GREY, stroke_width=3,
                                               fill_opacity=0).move_to(P3(0, 0.15)), num_dashes=80)
        pl = T("progenitor pool", 28, TEXT).move_to(P3(-3.6, 3.45))
        self.play(Create(pool), FadeIn(pl), run_time=0.9)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S07Brake(Sc):
    def construct(self):
        wr, wc = 1.7, P3(-3.6, 0.7)
        wheel = Circle(radius=wr, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.08).move_to(wc)
        spokes = VGroup(*[Line(wc - wr * P3(np.cos(a), np.sin(a)), wc + wr * P3(np.cos(a), np.sin(a)), color=GREY, stroke_width=4) for a in (0, PI / 4, PI / 2, 3 * PI / 4)])
        hub = Circle(radius=0.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.5).move_to(wc)
        wheel_g = VGroup(wheel, spokes, hub)
        # the progenitors stay on screen under the wheel
        row = VGroup(*[Circle(radius=0.4, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to(P3(-5.6 + 1.0 * k, -1.85)) for k in range(5)])
        rowl = T("progenitors", 28, GREY).move_to(P3(-3.6, -2.7))
        self.play(FadeIn(wheel_g), FadeIn(row), FadeIn(rowl), run_time=0.6)
        self._spin = ValueTracker(2.0)
        wheel_g.add_updater(lambda m, dt: m.rotate(self._spin.get_value() * dt, about_point=wc))
        self.at("break")
        pad = RoundedRectangle(corner_radius=0.12, width=0.5, height=1.8, stroke_color=REP, stroke_width=4, fill_color=REP, fill_opacity=0.6).move_to(wc + RIGHT * (wr + 1.4))
        bl = T("a brake", 46, REP, font=TITLE_FONT).move_to(P3(-3.6, 3.25))
        self.play(pad.animate.move_to(wc + RIGHT * (wr + 0.28)), FadeIn(bl, shift=UP * 0.15), self._spin.animate.set_value(0.3), run_time=0.8)
        self.at("progenitors are used")
        gx, gy, gh = 3.2, 0.1, 5.4
        track = RoundedRectangle(corner_radius=0.2, width=1.8, height=gh, stroke_color=GREY, stroke_width=4, fill_opacity=0).move_to(P3(gx, gy))
        lvl = ValueTracker(1.0)
        fop = ValueTracker(0.0)
        fill = always_redraw(lambda: Rectangle(width=1.56, height=max(0.02, (gh - 0.24) * lvl.get_value()), stroke_width=0, fill_color=GREEN, fill_opacity=0.7 * fop.get_value())
                             .move_to(P3(gx, gy - (gh - 0.24) / 2 + (gh - 0.24) * lvl.get_value() / 2)))
        pl = T("progenitor pool", 28, GREEN).move_to(P3(gx, gy - gh / 2 - 0.45))
        ghy = gy - (gh - 0.24) / 2 + (gh - 0.24) * 0.25
        ghost = DashedLine(P3(gx - 1.1, ghy), P3(gx + 1.1, ghy), color=REP, stroke_width=3, dash_length=0.15).set_opacity(0.6)
        ghl = T("without a\nbrake", 26, REP).set_opacity(0.8).move_to(P3(gx + 2.35, ghy))
        self.add(fill)
        self.play(FadeIn(track), FadeIn(pl), FadeIn(ghost), FadeIn(ghl), fop.animate.set_value(1.0), run_time=0.6)
        self.at("used up")
        wb = T("with the\nbrake", 26, GREEN)
        self.play(lvl.animate.set_value(0.62), run_time=1.0, rate_func=smooth)
        wb.move_to(P3(gx + 2.35, gy - (gh - 0.24) / 2 + (gh - 0.24) * 0.62))
        self.play(FadeIn(wb, shift=LEFT * 0.1), run_time=0.3)
        self.at("a cell held back")
        fill.clear_updaters()
        wheel_g.clear_updaters()
        self.remove(fill)
        # part two: a row of progenitors; one is held back, divides, and joins the contest again
        XS = [-5.4, -2.7, 0.0, 2.7, 5.4]

        def pc(x, op=0.08, rim=GREY, sw=4):
            return RoundedRectangle(corner_radius=0.75, width=1.7, height=4.4, stroke_color=rim, stroke_width=sw, fill_color=GREY, fill_opacity=op).move_to(P3(x, -0.2))

        def pn(x):
            return Circle(radius=0.4, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(P3(x, -0.2))

        cells = [pc(x) for x in XS]
        nucs = [pn(x) for x in XS]
        small = T("a brake", 30, REP, font=TITLE_FONT).move_to(P3(-5.4, 3.45))
        self.play(FadeOut(wheel_g), FadeOut(pad), FadeOut(track), FadeOut(fill), FadeOut(pl), FadeOut(ghost), FadeOut(ghl), FadeOut(wb),
                  FadeOut(row), FadeOut(rowl), ReplacementTransform(bl, small),
                  *[FadeIn(c) for c in cells], *[FadeIn(n) for n in nucs], run_time=0.5)
        self.at("held back")
        hl = T("held back", 30, NOT).move_to(P3(0, -2.95))
        self.play(cells[2].animate.set_stroke(NOT, 7), FadeIn(hl, shift=UP * 0.1), run_time=0.5)
        self.at("dividing")
        d1, d2 = pc(-0.95, 0.08, GREY, 4), pc(0.95, 0.08, GREY, 4)
        n1, n2 = pn(-0.95), pn(0.95)
        pl2 = T("progenitors", 30, GREY).move_to(P3(0, -2.95))
        self.play(Transform(cells[2], VGroup(d1, d2)), Transform(nucs[2], VGroup(n1, n2)), ReplacementTransform(hl, pl2),
                  cells[1].animate.shift(LEFT * 0.2), nucs[1].animate.shift(LEFT * 0.2),
                  cells[3].animate.shift(RIGHT * 0.2), nucs[3].animate.shift(RIGHT * 0.2), run_time=1.2)
        self.at("compete again")
        top = DoubleArrow(P3(-5.9, 2.5), P3(5.9, 2.5), color=GOLD, stroke_width=6, buff=0, tip_length=0.25)
        tl = T("compete again", 36, GOLD).move_to(P3(0, 3.1))
        self.play(*[c.animate.set_stroke(GOLD, 5) for c in (cells[0], cells[1], cells[3], cells[4])], cells[2].animate.set_stroke(GOLD, 5),
                  GrowFromCenter(top), FadeIn(tl, shift=DOWN * 0.1), run_time=0.8)
        self.at("later")
        clk = clock_icon((4.6, 3.1), 0.38, GOLD)
        self.play(FadeIn(clk), run_time=0.3)
        self.play(Rotate(clk.hand, angle=-2 * PI, about_point=clk.center_pt, rate_func=linear), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
BA, BB = -2.7, 2.7           # centres of the two big cells
BW_, BH_ = 3.7, 5.0
BY = -0.4
Y_SLOT1, Y_SLOT2 = 1.4, -0.8
BEDGE = BW_ / 2              # half width: cell edges at +-(BB - BEDGE)


def big_cells():
    a = RoundedRectangle(corner_radius=1.0, width=BW_, height=BH_, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(P3(BA, BY))
    b = a.copy().move_to(P3(BB, BY))
    return a, b


EA = BA + BW_ / 2   # A's right edge
EB = BB - BW_ / 2   # B's left edge


def a_cup():   # Notch on cell A, facing B, at slot 1
    return cup(EA, Y_SLOT1, +1, 0.28, w=9)


def b_cup():   # Notch on cell B, facing A, at slot 2
    return cup(EB, Y_SLOT2, -1, 0.28, w=9)


def b_knob(r=0.2):
    """Delta on B, reaching toward A's Notch cup at slot 1: the ball sits just outside the cup's mouth."""
    cx = EA + 0.28 + r + 0.08
    ball = Circle(radius=r, stroke_color=DEL, stroke_width=3, fill_color=DEL, fill_opacity=0.9).move_to(P3(cx, Y_SLOT1))
    stalk = Line(P3(EB, Y_SLOT1), P3(cx + r, Y_SLOT1), color=GREY, stroke_width=4)
    return VGroup(stalk, ball)


class S08Stem(Sc):
    def construct(self):
        a, b = big_cells()
        nch = VGroup(ch("Notch", NOT, size=28), T("?", 54, GOLD, font=TITLE_FONT)).arrange(DOWN, buff=0.15).move_to(P3(0, 0.3))
        nu = [Circle(radius=0.75, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to(P3(x, BY - 0.9)) for x in (BA - 0.4, BB + 0.4)]
        self.play(FadeIn(a), FadeIn(b), *[FadeIn(n_) for n_ in nu], FadeIn(nch, scale=0.8), run_time=0.6)
        self.at("stem cell")
        la = T("stem cell?", 34, GOLD).move_to(P3(BA, 2.75))
        qa = arr((-0.2, 0.3), (EA - 0.2, 0.3), GOLD, 5)
        self.add(la)
        self.play(GrowArrow(qa), run_time=0.6)
        self.at("non stem")
        lb = T("non-stem cell?", 34, GOLD).move_to(P3(BB, 2.75))
        qb = arr((0.2, 0.3), (EB + 0.2, 0.3), GOLD, 5)
        self.add(lb)
        self.play(GrowArrow(qb), run_time=0.6)
        self.at("both cells")
        ca, cb = a_cup(), b_cup()
        la2 = T("stem cell", 34, TEXT).move_to(la)
        lb2 = T("non-stem cell", 34, TEXT).move_to(lb)
        self.play(FadeOut(nch), FadeOut(qa), FadeOut(qb), Create(ca), Create(cb), Transform(la, la2), Transform(lb, lb2), run_time=0.7)
        self.at("receptor")
        t = T("both cells have the receptor", 34, NOT).move_to(P3(0, -3.35))
        self.play(FadeIn(t, shift=UP * 0.1), Indicate(ca, color=NOT, scale_factor=1.6), Indicate(cb, color=NOT, scale_factor=1.6), run_time=0.9)
        self.finish()


class S09Stem2(Sc):
    def construct(self):
        a, b = big_cells()
        ca, cb = a_cup(), b_cup()
        kb = b_knob()
        self.add(a, b, ca, cb, kb)
        # Notch activity gauges inside each cell, Delta trace inside B
        base_y, gmax = -1.95, 3.1
        gax, gbx = BA - 0.7, BB - 1.05
        base_a = Line(P3(gax - 0.5, base_y), P3(gax + 0.5, base_y), color=GREY, stroke_width=3)
        base_b = Line(P3(gbx - 0.5, base_y), P3(gbx + 0.5, base_y), color=GREY, stroke_width=3)
        bar_a = Rectangle(width=0.8, height=0.1, stroke_width=0, fill_color=NOT, fill_opacity=0.9).move_to(P3(gax, base_y + 0.05))
        bar_b = Rectangle(width=0.8, height=0.1, stroke_width=0, fill_color=NOT, fill_opacity=0.9).move_to(P3(gbx, base_y + 0.05))
        na = T("Notch activity", 26, NOT).move_to(P3(BA, -2.5))
        nb2 = T("Notch activity", 26, NOT).move_to(P3(gbx + 0.9, -2.5))
        self.at("notch")
        self.play(FadeIn(base_a), FadeIn(base_b), FadeIn(bar_a), FadeIn(bar_b), FadeIn(na), FadeIn(nb2), run_time=0.6)
        self.at("more strongly")
        hi = Rectangle(width=0.8, height=gmax, stroke_width=0, fill_color=NOT, fill_opacity=0.9).move_to(P3(gax, base_y + gmax / 2))
        lo = Rectangle(width=0.8, height=0.55, stroke_width=0, fill_color=NOT, fill_opacity=0.9).move_to(P3(gbx, base_y + 0.275))
        self.play(Transform(bar_a, hi), Transform(bar_b, lo), ca.animate.set_stroke(width=16), run_time=1.0)
        self.at("stays")
        self.play(a.animate.set_stroke(NOT, 7), run_time=0.6)
        self.at("progenitor")
        pa = T("progenitor", 36, NOT).move_to(P3(BA, 2.95))
        self.play(FadeIn(pa, shift=DOWN * 0.1), run_time=0.5)
        self.at("keeps sending")
        px = Plot(BB + 0.55, BB + 1.7, -1.95, 1.0, 3.0, 1.0)
        ax = px.axes(yaxis=True)
        dl = T("Delta sent", 26, DEL).move_to(P3(BB + 0.85, 1.55))
        ball = kb[1]
        self.play(FadeIn(ax), FadeIn(dl), ball.animate.scale(1.5).shift(RIGHT * 0.22), run_time=0.4)
        tr = px.curve([0, 3.0], [0.88, 0.88], DEL, 7)
        self.play(Create(tr, rate_func=linear), run_time=1.0)
        self.at("differentiates")
        nb = T("neuron", 36, GREEN).move_to(P3(BB, 2.95))
        self.play(b.animate.set_stroke(GREEN, 7).set_fill(GREEN, 0.18), FadeIn(nb, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S10Ko(Sc):
    def construct(self):
        rg = Ring(center=(-3.2, 0.0), r0=1.2, r1=3.3, n=18)
        cells = rg.cells()
        self.add(*cells)
        self.at("lacking")
        chp = ch("Hes1", REP, size=38).move_to(P3(2.9, 2.9))
        x = cross_mark(P3(4.6, 2.9), 0.35, RED, 8)
        nl = T("Hes1 knockout", 34, RED).move_to(P3(3.9, 1.95))
        self.play(FadeIn(chp, scale=0.8), Create(x), FadeIn(nl, shift=DOWN * 0.1), run_time=0.6)
        self.at("make neurons")
        green_idx = [i for i in range(rg.n) if i % 3 != 1]
        early = T("neurons too early", 38, GREEN).move_to(P3(3.9, 0.6))
        self.play(FadeIn(early), run_time=0.3)
        self.play(LaggedStart(*[cells[i].animate.set_fill(GREEN, 0.45).set_stroke(GREEN, 4) for i in green_idx], lag_ratio=0.07), run_time=1.3)
        self.at("severe")
        warped = rg.cells(warp=True)
        for i, wc in enumerate(warped):
            if i in green_idx:
                wc.set_fill(GREEN, 0.45).set_stroke(GREEN, 4)
        defects = VGroup(T("severe neural", 38, RED), T("tube defects", 38, RED)).arrange(DOWN, buff=0.15).move_to(P3(3.9, -1.0))
        self.play(*[Transform(c, w) for c, w in zip(cells, warped)], FadeIn(defects, shift=LEFT * 0.2), run_time=1.7)
        self.finish()


# ------------------------------------------------------------------------------------------------
def pool_plot():
    return Plot(-4.6, 5.3, -2.5, 2.3, 6.0, 1.0)


def pool_curve(px, k, color, w=6):
    ts = np.linspace(0, 6.0, 120)
    return px.curve(ts, np.exp(-k * ts), color, w)


class S11Ko2(Sc):
    def construct(self):
        px = pool_plot()
        ax = px.axes(xlab="time (days, schematic)", ylab=("progenitors left", GREEN), yticks=[(1.0, "100%"), (0.0, "0")], ylab_dx=1.45)
        c0, c1 = pool_curve(px, 0.18, GREY), pool_curve(px, 0.45, RED)

        def leg(txt, col, y, w=6):
            g = VGroup(Line(P3(0, 0), P3(0.7, 0), color=col, stroke_width=w), T(txt, 28, col)).arrange(RIGHT, buff=0.2)
            return g.move_to(P3(0, y)).align_to(P3(0.7, 0), LEFT)
        l0, l1, l2 = leg("normal", GREY, 2.15), leg("no Hes1", RED, 1.5), leg("no Hes1 and Hes5", RED, 0.85, 10)
        sc = T("schematic", 26, GREY).move_to(P3(5.2, 3.3))
        self.add(ax, c0, c1, l0, l1, sc)
        self.at("hes5")
        chp = ch("Hes5", REP, size=32).move_to(P3(-0.6, 3.3))
        x = cross_mark(P3(1.0, 3.3), 0.32, RED, 8)
        self.play(FadeIn(chp, scale=0.8), Create(x), run_time=0.6)
        self.at("progenitors are lost")
        c2 = pool_curve(px, 0.9, RED, 10)
        self.play(Create(c2, rate_func=linear), FadeIn(l2, shift=UP * 0.1), run_time=1.3)
        self.at("faster")
        self.play(Indicate(c2, color=RED, scale_factor=1.04), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
TICKS = (0, 2, 4, 6, 8)


class S12Clock(Sc):
    def construct(self):
        t, pn, _, _ = traces(0.30, T_win=8.0)
        px = Plot(-5.0, 5.2, -2.3, 2.3, 8.0, 1.1)
        ax = px.axes(ticks=TICKS, xlab="time (hours)", ylab=("Hes1 level (arbitrary units)", REP), ylab_dx=0.75)
        self.add(ax)
        self.at("surprise")
        clk = clock_icon((6.1, 3.2), 0.55, GOLD)
        self.play(FadeIn(clk, scale=0.7), run_time=0.3)
        self.play(Rotate(clk.hand, angle=-2 * PI, about_point=clk.center_pt, rate_func=linear), run_time=0.8)
        self.at("cultured cells")
        cc = ch("cultured cells", GOLD, size=32).move_to(P3(3.2, 3.2))
        self.play(FadeIn(cc, shift=DOWN * 0.1), run_time=0.5)
        cur = px.curve(t, pn, REP, 7)
        self.at("rises")
        self.play(Create(cur, rate_func=linear), run_time=1.6)
        self.at("two hours")
        pk = peaks(t, pn, 0.5)[:2]
        a, b = px.pt(t[pk[0]], 1.0) + UP * 0.4, px.pt(t[pk[1]], 1.0) + UP * 0.4
        da = DoubleArrow(a, b, color=TEXT, stroke_width=5, buff=0, tip_length=0.2)
        lb = T("about 2 hours", 32, TEXT).move_to((a + b) / 2 + UP * 0.45)
        self.play(GrowFromCenter(da), FadeIn(lb, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------------
class S13Clock2(Sc):
    def construct(self):
        gene = RoundedRectangle(corner_radius=0.15, width=3.0, height=1.0, stroke_color=REP, stroke_width=4, fill_color=REP, fill_opacity=0.25).move_to(P3(-4.4, 0.25))
        gl = T("Hes1 gene", 28, REP).move_to(gene)
        dna = Rectangle(width=4.2, height=0.3, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.35).move_to(P3(-4.4, -0.4))
        dnal = T("DNA", 26, GREY).move_to(P3(-4.4, -0.95))
        prot = ch("protein", REP, size=34).move_to(P3(4.7, 0.0))
        rna = ch("RNA", REP, size=34).move_to(P3(0.2, 2.6))
        # the repression arrow from protein back to the gene
        cb = CubicBezier(P3(4.7, -0.7), P3(4.2, -3.5), P3(-2.2, -3.4), P3(-3.0, 0.0), stroke_color=REP, stroke_width=7)
        self.play(FadeIn(dna), FadeIn(gene), FadeIn(gl), FadeIn(dnal), FadeIn(prot, shift=LEFT * 0.1), run_time=0.6)
        self.at("represses")
        end = cb.point_from_proportion(1.0)
        tan = end - cb.point_from_proportion(0.97)
        tan = tan / np.linalg.norm(tan)
        perp = P3(-tan[1], tan[0])
        bar = Line(end + perp * 0.45, end - perp * 0.45, color=REP, stroke_width=10)
        minus = VGroup(Circle(radius=0.32, stroke_color=REP, stroke_width=4, fill_color=BG, fill_opacity=1),
                       Line(LEFT * 0.17, RIGHT * 0.17, color=REP, stroke_width=8)).move_to(cb.point_from_proportion(0.5))
        self.play(Create(VGroup(cb, bar), rate_func=linear), run_time=0.6)
        self.at("its own gene")
        self.play(FadeIn(minus, scale=0.6), Indicate(gene, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.at("RNA and protein")
        a1 = arr((-3.0, 0.8), (-1.45, 2.35), GREY, 6)
        a2 = arr((1.9, 2.35), (3.8, 0.55), GREY, 6)
        tl1 = T("transcription", 26, GREY).move_to(P3(-3.9, 2.1))
        tl2 = T("translation", 26, GREY).move_to(P3(5.0, 2.1))
        self.play(FadeIn(rna, shift=UP * 0.1), GrowArrow(a1), FadeIn(tl1), run_time=0.7)
        self.play(GrowArrow(a2), FadeIn(tl2), Indicate(prot, color=TEXT, scale_factor=1.12), run_time=0.7)
        self.at("short")
        tags = VGroup()
        bars = []
        for (x, y) in ((0.2, 1.85), (4.9, 1.2)):
            bb = Rectangle(width=1.6, height=0.16, stroke_width=0, fill_color=TEXT, fill_opacity=0.9).move_to(P3(x, y))
            tg = T("~20 min", 26, TEXT).move_to(P3(x, y - 0.4 if x < 1 else y - 0.38))
            bars.append(bb)
            tags.add(bb, tg)
        sl = T("short-lived", 28, TEXT).move_to(P3(0.2, 0.55))
        self.play(FadeIn(tags), FadeIn(sl), run_time=0.4)
        self.play(*[b.animate.set_fill(TEXT, 0.12) for b in bars], run_time=0.8)
        self.at("making new")
        clk = clock_icon((0.0, 0.6), 0.45, TEXT)
        dl = T("delay", 32, TEXT).move_to(P3(1.4, 0.6))
        dot = Dot(P3(-3.0, 0.8), radius=0.17, color=TEXT)
        path = VMobject().set_points_as_corners([P3(-3.0, 0.8), P3(-1.45, 2.35), P3(1.9, 2.35), P3(3.8, 0.55)])
        self.play(FadeOut(sl), FadeIn(clk, scale=0.6), FadeIn(dl, shift=UP * 0.1), FadeIn(dot), run_time=0.25)
        self.play(MoveAlongPath(dot, path, rate_func=linear), Rotate(clk.hand, angle=-2 * PI, about_point=clk.center_pt, rate_func=linear), run_time=0.6)
        self.at("takes time")
        self.play(FadeOut(dot), Indicate(dl, color=TEXT, scale_factor=1.2), Rotate(clk.hand, angle=-2 * PI, about_point=clk.center_pt, rate_func=linear), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
PANEL_Y = (2.15, 0.0, -2.15)
PX0, PX1 = -4.0, 5.8


def panels(tmax=9.0, ticks=True):
    ps = [Plot(PX0, PX1, y - 0.7, y + 0.7, tmax, 1.05) for y in PANEL_Y]
    axs = []
    for k, p in enumerate(ps):
        axs.append(p.axes(ticks=(0, 2, 4, 6, 8) if (ticks and k == 2) else (), xlab="time (hours)" if (ticks and k == 2) else None))
    return ps, axs


LABELS = (("Hes1", REP), ("Neurog2", NG2), ("Dll1", DEL))


def panel_labels():
    return [T(n, 30, c).move_to(P3(-5.5, y)) for (n, c), y in zip(LABELS, PANEL_Y)]


class S14Clock3(Sc):
    def construct(self):
        t, pn, ng, dl = traces(0.42, T_win=9.0)
        ps, axs = panels()
        labs = panel_labels()
        self.add(*axs)
        self.at("mouse neural")
        mp = ch("mouse neural progenitors", GOLD, size=28).move_to(P3(-2.2, 3.45))
        self.play(FadeIn(mp, shift=DOWN * 0.1), run_time=0.5)
        self.at("hess")
        self.play(FadeIn(labs[0]), run_time=0.3)
        self.at("oscillates")
        c0 = ps[0].curve(t, pn, REP, 7)
        per = T("period about 2 to 3 hours", 28, TEXT).move_to(P3(3.6, 3.45))
        self.play(FadeIn(per, shift=DOWN * 0.1), Create(c0, rate_func=linear), run_time=1.8)
        self.until(3.85)
        c1 = ps[1].curve(t, ng, NG2, 7)
        self.play(FadeIn(labs[1]), Create(c1, rate_func=linear), run_time=1.3)
        self.at("delta like")
        c2 = ps[2].curve(t, dl, DEL, 7)
        self.play(FadeIn(labs[2]), Create(c2, rate_func=linear), run_time=1.1)
        self.at("opposite phase")
        pk = [i for i in peaks(t, pn, 3.0)][0]
        tr = [i for i in troughs(t, pn, t[pk])][0]
        x1, x2 = ps[0].pt(t[pk], 0)[0], ps[0].pt(t[tr], 0)[0]
        g1 = DashedLine(P3(x1, 2.9), P3(x1, -2.85), color=TEXT, stroke_width=3, dash_length=0.12)
        g2 = DashedLine(P3(x2, 2.9), P3(x2, -2.85), color=TEXT, stroke_width=3, dash_length=0.12)
        self.play(Create(g1), run_time=0.5)
        self.play(Create(g2), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------------
DROP = 4.5


class S15Commit(Sc):
    def construct(self):
        t, pn, ng, dl = traces(0.42, drop=DROP, T_win=9.0)
        ps, axs = panels()
        labs = panel_labels()
        self.add(*axs, labs[0], labs[1])
        self.at("becoming neurons")
        lab = ch("a cell becoming a neuron", GREEN, size=28).move_to(P3(1.4, 3.45))
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        k = int(DROP / 0.01)
        s1 = ps[0].curve(t, pn, REP, 7, 0, k + 1)
        s2 = ps[0].curve(t, pn, REP, 7, k, 901)
        self.until(0.95)
        self.play(Create(s1, rate_func=linear), run_time=1.15)
        self.at("falls")
        self.play(Create(s2, rate_func=linear), run_time=0.8)
        self.at("neurogenin two")
        n1 = ps[1].curve(t, ng, NG2, 7, 0, k + 1)
        n2 = ps[1].curve(t, ng, NG2, 7, k, 901)
        self.play(Create(n1, rate_func=linear), run_time=0.8)
        self.play(Create(n2, rate_func=linear), run_time=0.8)
        self.at("brief pulse")
        d1 = ps[2].curve(t, dl, DEL, 7)
        i0 = peaks(t, dl, 0.5)[0]
        self.add(labs[2])
        self.play(FadeIn(labs[2]), Create(d1, rate_func=linear), run_time=1.2)
        px = ps[2].pt(t[i0], 0)[0]
        box = DashedVMobject(Rectangle(width=1.7, height=1.3, stroke_color=GOLD, stroke_width=3, fill_opacity=0).move_to(P3(px, -2.2)), num_dashes=30)
        bp = T("brief pulse", 28, GOLD).move_to(P3(-3.3, -1.12))
        self.play(Create(box), FadeIn(bp), run_time=0.3)
        self.at("not a commitment")
        nc = T(": not a commitment", 28, RED).next_to(bp, RIGHT, buff=0.05)
        pl = T("stays high: commitment", 28, GREEN).move_to(P3(4.1, -1.12))
        self.play(FadeIn(nc, shift=RIGHT * 0.1), FadeIn(pl, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
# the prompt card: light held steady, or made to oscillate
# ------------------------------------------------------------------------------------------------
R1 = Plot(-3.4, 2.9, 0.95, 2.45, 9.0, 1.1)
R2 = Plot(-3.4, 2.9, -2.0, -0.5, 9.0, 1.1)
LY1, LY2 = 2.85, -0.15
OY1, OY2 = 1.65, -1.35


def ascl1(steady, T_win=9.0, dt=0.02):
    ts = np.arange(0, T_win + dt, dt)
    x = np.zeros_like(ts)
    for i in range(len(ts) - 1):
        on = 1.0 if (steady or (ts[i] % 3.0) < 1.5) else 0.0
        x[i + 1] = x[i] + dt * (2.0 * on - 2.0 * x[i])
    return ts, np.clip(x, 0, 1.05)


def light_bar(y, steady):
    p = R1
    if steady:
        return VGroup(Rectangle(width=p.x1 - p.x0, height=0.2, stroke_width=0, fill_color=LIGHT, fill_opacity=0.8).move_to(P3((p.x0 + p.x1) / 2, y)))
    w = (p.x1 - p.x0) / 6.0
    return VGroup(*[Rectangle(width=w, height=0.2, stroke_width=0, fill_color=LIGHT, fill_opacity=0.8).move_to(P3(p.x0 + w * (0.5 + 2 * k), y)) for k in range(3)])


def outcome_box(y):
    box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.2, height=2.5, stroke_color=GOLD, stroke_width=3, fill_opacity=0).move_to(P3(4.9, y)), num_dashes=40)
    q = T("?", 72, GOLD, font=TITLE_FONT).move_to(P3(4.9, y))
    return VGroup(box, q)


class Prompt16:
    """The pieces of the Ascl1 prompt card, so the pause and the reveal can rebuild them."""

    def __init__(self):
        self.banner = predict_banner(4.5, 3.4)
        self.cult = T("cultured mouse progenitors", 30, TEXT).move_to(P3(-1.2, 3.45))
        self.sun = sun_icon((-5.7, LY1))
        self.ll = T("light", 26, LIGHT).move_to(P3(-4.7, LY1))
        self.ll2 = T("light", 26, LIGHT).move_to(P3(-4.7, LY2))
        self.lb1, self.lb2 = light_bar(LY1, True), light_bar(LY2, False)
        self.ax1 = R1.axes(ylab=("level", GREY), ylab_dx=0.45)
        self.ax2 = R2.axes(xlab="time", ylab=("level", GREY), ylab_dx=0.45)
        self.t1, self.x1 = ascl1(True)
        self.t2, self.x2 = ascl1(False)
        self.c1 = R1.curve(self.t1, self.x1, ASC, 7)
        self.c2 = R2.curve(self.t2, self.x2, ASC, 7)
        self.n1 = VGroup(T("Ascl1", 30, ASC), T("steady", 30, TEXT)).arrange(DOWN, buff=0.1).move_to(P3(-5.35, 1.7))
        self.n2 = VGroup(T("Ascl1", 30, ASC), T("oscillating", 30, TEXT)).arrange(DOWN, buff=0.1).move_to(P3(-5.35, -1.25))
        self.o1, self.o2 = outcome_box(OY1), outcome_box(OY2)

    def add_all(self, scene):
        scene.add(self.banner, self.cult, self.sun, self.ll, self.ll2, self.lb1, self.lb2, self.ax1, self.ax2, self.c1, self.c2, self.n1, self.n2, self.o1, self.o2)


class S16Predict(Sc):
    def construct(self):
        pr = Prompt16()
        self.add(pr.banner, pr.ax1, pr.ax2)
        self.at("cultured progenitors")
        self.play(FadeIn(pr.cult, shift=DOWN * 0.1), run_time=0.5)
        self.at("use light")
        self.play(FadeIn(pr.sun, scale=0.6), FadeIn(pr.ll), FadeIn(pr.ll2), run_time=0.5)
        self.at("hold")
        self.play(FadeIn(pr.lb1), run_time=0.3)
        self.play(Create(pr.c1, rate_func=linear), run_time=1.0)
        self.at("steady")
        self.play(FadeIn(pr.n1, shift=RIGHT * 0.15), run_time=0.4)
        self.at("make it oscillate")
        self.play(FadeIn(pr.lb2), run_time=0.3)
        self.play(Create(pr.c2, rate_func=linear), FadeIn(pr.n2, shift=RIGHT * 0.15), run_time=1.3)
        self.at("which become")
        self.play(FadeIn(pr.o1, scale=0.8), FadeIn(pr.o2, scale=0.8), run_time=0.6)
        self.finish()


class S17Pause(NarratedScene):
    def construct(self):
        pr = Prompt16()
        pr.add_all(self)
        clk = clock_icon((6.25, 3.4), 0.48, GOLD)
        self.add(clk)
        self.play(Rotate(clk.hand, angle=-2 * PI, about_point=clk.center_pt, rate_func=linear), run_time=self.narration_s - 0.2)
        self.finish()


class S18Reveal(Sc):
    def construct(self):
        pr = Prompt16()
        pr.add_all(self)
        self.at("pushed cells")
        neu = VGroup(*[neuron_blob(4.9 + dx, OY1 + 0.2, 0.42) for dx in (-0.95, 0.0, 0.95)])
        nl = T("neurons", 30, GREEN).move_to(P3(4.9, OY1 - 0.7))
        self.play(FadeOut(pr.o1[1]), FadeIn(neu, scale=0.6), FadeIn(nl, shift=UP * 0.1), pr.o1[0].animate.set_stroke(GREEN), run_time=0.9)
        self.at("oscillating")
        self.play(Indicate(pr.c2, color=ASC, scale_factor=1.03), run_time=0.9)
        self.at("kept them")
        prog = VGroup(*[Circle(radius=0.42, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to(P3(4.9 + dx, OY2 + 0.2)) for dx in (-0.95, 0.0, 0.95)])
        self.play(FadeOut(pr.o2[1]), FadeIn(prog, scale=0.6), pr.o2[0].animate.set_stroke(GREY), run_time=0.8)
        self.at("dividing")
        new = VGroup(*[p.copy() for p in prog])
        self.add(new)
        pl = T("progenitors", 30, GREY).move_to(P3(4.9, OY2 - 0.85))
        src = T("Imayoshi and colleagues, 2013 (cultured mouse progenitors)", 30, TEXT).move_to(P3(0.2, -3.45))
        self.play(*[p.animate.scale(0.7).shift(UP * 0.4) for p in prog], *[n.animate.scale(0.7).shift(DOWN * 0.2) for n in new],
                  FadeIn(pl, shift=UP * 0.1), FadeIn(src, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------------
def question_text(x=3.7, y=1.3, size=42):
    return VGroup(*[T(s, size, GOLD, font=TITLE_FONT) for s in ("Does a proneural", "factor also decide", "what kind of", "neuron forms?")]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(P3(x, y))


class S19Identity(Sc):
    def construct(self):
        f = Fore()
        self.add(f.base)
        lq = T("Last question", 34, GOLD).move_to(P3(3.7, 3.2))
        q = question_text()
        self.add(lq, q)
        self.at("factor")
        n2 = ch("Neurog2", NG2, size=30).move_to(POS_D)
        a1 = ch("Ascl1", ASC, size=30).move_to(POS_V)
        self.play(FadeIn(n2, scale=0.8), FadeIn(a1, scale=0.8), run_time=0.6)
        self.at("what kind")
        rows = VGroup()
        for name, col, y in (("Neurog2", NG2, -1.45), ("Ascl1", ASC, -2.75)):
            c = ch(name, col, size=30).move_to(P3(1.9, y))
            ar = arr((3.05, y), (3.75, y), GOLD, 5)
            bx = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=2.9, height=1.0, stroke_color=GOLD, stroke_width=3, fill_opacity=0).move_to(P3(5.25, y)), num_dashes=30)
            qq = T("neuron type?", 28, GOLD).move_to(P3(5.25, y))
            rows.add(c, ar, bx, qq)
        self.play(FadeIn(rows, shift=LEFT * 0.15), run_time=0.8)
        self.finish()


def fore_state(scene, shade=True, swapped=False, names=True):
    f = Fore()
    scene.add(f.base)
    if shade:
        f.shade_now()
    n2 = ch("Neurog2\ncoding region", NG2, size=26).move_to(POS_V if swapped else POS_D)
    a1 = ch("Ascl1\ncoding region", ASC, size=26).move_to(POS_D if swapped else POS_V)
    n2[0].set_fill(BG, 0.9)
    a1[0].set_fill(BG, 0.9)
    scene.add(n2, a1)
    return f, n2, a1


def bar_chart(name, color, cx, ytop, hd, hv, base_h=1.9):
    """Two bars (dorsal, ventral) for one factor. Chart baseline at ytop - base_h - 0.2."""
    yb = ytop - base_h - 0.35
    ttl = T(name, 34, color).move_to(P3(cx, ytop + 0.35))
    axis = Line(P3(cx - 2.4, yb), P3(cx + 2.4, yb), color=GREY, stroke_width=3)
    yaxis = Line(P3(cx - 2.4, yb), P3(cx - 2.4, yb + base_h + 0.15), color=GREY, stroke_width=3)
    ylab = T("level", 26, GREY).rotate(PI / 2).move_to(P3(cx - 2.75, yb + base_h / 2))
    bd = Rectangle(width=1.5, height=hd, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to(P3(cx - 1.0, yb + hd / 2))
    bv = Rectangle(width=1.5, height=hv, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to(P3(cx + 1.0, yb + hv / 2))
    ld = T("dorsal", 26, GREY).move_to(P3(cx - 1.0, yb - 0.32))
    lv = T("ventral", 26, GREY).move_to(P3(cx + 1.0, yb - 0.32))
    return ttl, axis, yaxis, ylab, bd, bv, ld, lv


class S20Forebrain(Sc):
    def construct(self):
        f = Fore()
        self.add(f.base)
        n2 = ch("Neurog2", NG2, size=30).move_to(POS_D)
        a1 = ch("Ascl1", ASC, size=30).move_to(POS_V)
        self.add(n2, a1)
        t1, ax1, ya1, yl1, bd1, bv1, ld1, lv1 = bar_chart("Neurog2", NG2, 4.1, 3.0, 2.0, 0.4, base_h=2.1)
        t2, ax2, ya2, yl2, bd2, bv2, ld2, lv2 = bar_chart("Ascl1", ASC, 4.1, -0.75, 0.45, 2.0, base_h=2.1)
        self.add(ax1, ya1, yl1, ld1, lv1, ax2, ya2, yl2, ld2, lv2)
        mf = T("mouse forebrain", 30, TEXT).move_to(P3(4.1, 3.5))
        self.add(mf)
        self.at("neurogenin")
        self.play(FadeOut(mf), FadeIn(t1, shift=LEFT * 0.2), Indicate(n2, color=TEXT, scale_factor=1.15), run_time=0.6)
        self.at("dorsal")
        self.play(*f.shade_dors(), GrowFromEdge(bd1, DOWN), GrowFromEdge(bv1, DOWN), run_time=1.0)
        self.until(5.1)
        self.play(FadeIn(t2, shift=LEFT * 0.2), Indicate(a1, color=TEXT, scale_factor=1.15), run_time=0.6)
        self.at("ventral")
        self.play(*f.shade_vent(), GrowFromEdge(bv2, DOWN), GrowFromEdge(bd2, DOWN), run_time=1.0)
        self.finish()


class Cards:
    def __init__(self):
        def card(y, l1, l2):
            r = RoundedRectangle(corner_radius=0.2, width=6.0, height=2.0, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.1).move_to(P3(3.7, y))
            a = T(l1, 28, GOLD)
            b = T(l2, 30, TEXT)
            VGroup(a, b).arrange(DOWN, buff=0.2).move_to(r)
            return VGroup(r, a, b)
        self.c1 = card(1.25, "if the factor carries identity:", "dorsal cells turn ventral")
        self.c2 = card(-1.25, "if the territory carries identity:", "dorsal cells stay dorsal")
        self.ban = predict_banner(3.7, 3.3)


class S21Swap(Sc):
    def construct(self):
        f, n2, a1 = fore_state(self)
        cap = T("swap the coding regions", 34, GOLD).move_to(P3(3.7, 3.3))
        self.at("swap")
        pa = ArcBetweenPoints(POS_D, POS_V, angle=1.1)
        pb = ArcBetweenPoints(POS_V, POS_D, angle=1.1)
        ga = ArcBetweenPoints(POS_D + RIGHT * 0.2 + DOWN * 0.6, POS_V + RIGHT * 0.2 + UP * 0.6, angle=1.1, color=GOLD, stroke_width=5).add_tip(tip_length=0.25)
        gb = ArcBetweenPoints(POS_V + LEFT * 0.2 + UP * 0.6, POS_D + LEFT * 0.2 + DOWN * 0.6, angle=1.1, color=GOLD, stroke_width=5).add_tip(tip_length=0.25)
        self.play(FadeIn(cap), Create(ga), Create(gb), MoveAlongPath(n2, pa), MoveAlongPath(a1, pb), run_time=1.8)
        self.play(FadeOut(ga), FadeOut(gb), run_time=0.3)
        cd = Cards()
        self.until(3.5)
        self.play(FadeOut(cap), FadeIn(cd.ban, shift=DOWN * 0.1), run_time=0.4)
        self.at("the factor")
        self.play(FadeIn(cd.c1, shift=LEFT * 0.2), run_time=0.4)
        self.at("territory")
        self.play(FadeIn(cd.c2, shift=LEFT * 0.2), run_time=0.4)
        self.finish()


class S22Pause(NarratedScene):
    def construct(self):
        f, n2, a1 = fore_state(self, swapped=True)
        cd = Cards()
        self.add(cd.ban, cd.c1, cd.c2)
        clk = clock_icon((6.1, 3.25), 0.5, GOLD)
        self.add(clk)
        self.play(Rotate(clk.hand, angle=-2 * PI, about_point=clk.center_pt, rate_func=linear), run_time=self.narration_s - 0.2)
        self.finish()


# ------------------------------------------------------------------------------------------------
# the two result panels
# ------------------------------------------------------------------------------------------------
def marker_chip(text, lit, size=26):
    c = ch(text, GREEN if lit else GREY, size=size)
    if not lit:
        c[0].set_fill(GREY, 0.0).set_stroke(GREY, 2.5, opacity=0.5)
        c[1].set_opacity(0.55)
    return c


class S23Swapreveal(Sc):
    def construct(self):
        hd = T("Ascl1 in dorsal cells", 38, ASC).move_to(P3(0, 3.3))
        cell = Circle(radius=2.2, stroke_color=TEAL, stroke_width=6, fill_color=TEAL, fill_opacity=0.3).move_to(P3(-3.6, 0.6))
        dl = T("dorsal cell", 28, TEAL).move_to(P3(-3.6, -2.0))
        p1 = chip("fully ventral", GOLD, size=28)
        p2 = chip("fully dorsal", GOLD, size=28)
        VGroup(p1, p2).arrange(DOWN, buff=0.6).move_to(P3(3.6, 1.7))
        x1 = cross_mark(P3(p1.get_right()[0] + 0.6, p1.get_center()[1]), 0.28, RED, 7)
        x2 = cross_mark(P3(p1.get_right()[0] + 0.6, p2.get_center()[1]), 0.28, RED, 7)
        self.add(hd, cell, dl)
        self.at("neither")
        self.play(FadeIn(p1), FadeIn(p2), Create(x1), Create(x2), run_time=0.7)
        self.at("pushed")
        patch = Circle(radius=1.0, stroke_width=0, fill_color=GREEN, fill_opacity=0.6).move_to(P3(-3.0, 1.3))
        mh = T("ventral markers", 30, GREY).move_to(P3(3.6, 2.6))
        m1, m2 = marker_chip("Dlx1", True, 30), marker_chip("GAD67", True, 30)
        VGroup(m1, m2).arrange(RIGHT, buff=0.4).move_to(P3(3.6, 1.5))
        m3 = marker_chip("other ventral markers", False, 30).move_to(P3(3.6, 0.3))
        self.play(FadeOut(VGroup(p1, p2, x1, x2)), FadeIn(mh), FadeIn(m3), run_time=0.4)
        self.play(FadeIn(m1, scale=0.8), FadeIn(m2, scale=0.8), GrowFromCenter(patch), run_time=1.0)
        self.at("partly")
        pl = T("partly ventral", 46, ASC, font=TITLE_FONT).move_to(P3(-3.6, -3.1))
        sm = T("some ventral markers on,\nothers not", 32, TEXT).move_to(P3(3.6, -1.1))
        self.play(FadeIn(pl, shift=UP * 0.15), FadeIn(sm), run_time=0.8)
        self.finish()


class S24Swapreveal2(Sc):
    def construct(self):
        # the S23 result, moved to the left half
        hd = T("Ascl1 in dorsal cells", 32, ASC).move_to(P3(-3.5, 3.45))
        cell = Circle(radius=1.4, stroke_color=TEAL, stroke_width=5, fill_color=TEAL, fill_opacity=0.3).move_to(P3(-3.5, 1.85))
        patch = Circle(radius=0.62, stroke_width=0, fill_color=GREEN, fill_opacity=0.6).move_to(P3(-3.1, 2.15))
        m1, m2 = marker_chip("Dlx1", True, 32), marker_chip("GAD67", True, 32)
        VGroup(m1, m2).arrange(RIGHT, buff=0.3).move_to(P3(-3.5, -0.1))
        m3 = marker_chip("other ventral markers", False, 30).move_to(P3(-3.5, -1.05))
        pl = T("partly ventral", 40, ASC, font=TITLE_FONT).move_to(P3(-3.5, -2.2))
        self.add(hd, cell, patch, m1, m2, m3, pl)
        self.at("ventral forebrain")
        hv = T("Neurog2 in ventral cells", 32, NG2).move_to(P3(3.5, 3.45))
        vc = Circle(radius=1.4, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.3).move_to(P3(3.5, 1.85))
        vl = T("ventral cell", 30, GREEN).move_to(P3(3.5, 1.85))
        self.play(FadeIn(hv, shift=DOWN * 0.1), FadeIn(vc, scale=0.85), FadeIn(vl), run_time=0.7)
        self.at("restored neurons")
        nb = Circle(radius=1.4, stroke_color=GREEN, stroke_width=7, fill_color=GREEN, fill_opacity=0.55).move_to(P3(3.5, 1.85))
        nl = T("neuron", 34, TEXT, weight=BOLD).move_to(P3(3.5, 1.85))
        k1, k2 = marker_chip("Dlx1", True, 32), marker_chip("GAD67", True, 32)
        VGroup(k1, k2).arrange(RIGHT, buff=0.3).move_to(P3(3.5, -0.1))
        kl = T("keeps ventral markers", 30, GREEN).move_to(P3(3.5, -0.95))
        self.play(Transform(vc, nb), FadeOut(vl), FadeIn(nl), FadeIn(k1, shift=UP * 0.1), FadeIn(k2, shift=UP * 0.1), FadeIn(kl), run_time=1.0)
        self.at("did not push")
        d1, d2 = marker_chip("Tbr1", False, 32), marker_chip("NeuroD", False, 32)
        VGroup(d1, d2).arrange(RIGHT, buff=0.3).move_to(P3(3.5, -1.95))
        dl = T("no dorsal markers (Tbr1, NeuroD)", 28, RED).move_to(P3(3.5, -2.75))
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(dl, shift=UP * 0.1), run_time=0.7)
        self.at("swaps")
        axis = DashedLine(P3(0, 3.75), P3(0, -3.0), color=GOLD, stroke_width=4, dash_length=0.15)
        self.play(Create(axis), run_time=0.6)
        self.at("mirror")
        mi = T("not mirror images", 42, GOLD).move_to(P3(0, -3.45))
        self.play(FadeIn(mi, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------------
def brake_icon(c, wr=1.45):
    wc = P3(*c)
    wheel = Circle(radius=wr, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.08).move_to(wc)
    spokes = VGroup(*[Line(wc - wr * P3(np.cos(a), np.sin(a)), wc + wr * P3(np.cos(a), np.sin(a)), color=GREY, stroke_width=4) for a in (0, PI / 4, PI / 2, 3 * PI / 4)])
    pad = RoundedRectangle(corner_radius=0.1, width=0.42, height=1.5, stroke_color=REP, stroke_width=4, fill_color=REP, fill_opacity=0.6).move_to(wc + RIGHT * (wr + 0.24))
    return VGroup(wheel, spokes, pad)


def clock_big(c, r=1.45):
    cc = P3(*c)
    face = Circle(radius=r, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.08).move_to(cc)
    ticks = VGroup(*[Line(cc + 0.82 * r * P3(np.cos(a), np.sin(a)), cc + 0.96 * r * P3(np.cos(a), np.sin(a)), color=GREY, stroke_width=3) for a in np.linspace(0, 2 * PI, 13)[:-1]])
    h1 = Line(cc, cc + UP * r * 0.7, color=TEXT, stroke_width=6)
    h2 = Line(cc, cc + RIGHT * r * 0.45, color=TEXT, stroke_width=5)
    g = VGroup(face, ticks, h1, h2)
    g.hand = h1
    g.cc = cc
    return g


class S25Takeaway(Sc):
    def construct(self):
        title = VGroup(T("In vertebrates,", 40, TEXT, font=TITLE_FONT), T("the loop is", 40, TEXT, font=TITLE_FONT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        title.move_to(P3(-4.3, 3.0))
        self.add(title)
        self.at("break")
        bi = brake_icon((-5.0, 0.0))
        bl = T("a brake", 48, REP, font=TITLE_FONT).move_to(P3(-4.7, -2.4))
        self.play(FadeIn(bi, scale=0.8), FadeIn(bl, shift=UP * 0.1), run_time=0.5)
        self.at("a clock")
        ci = clock_big((-1.1, 0.0))
        cl = T("a clock", 48, TEXT, font=TITLE_FONT).move_to(P3(-1.1, -2.4))
        self.play(FadeIn(ci, scale=0.8), FadeIn(cl, shift=UP * 0.1), run_time=0.4)
        self.play(Rotate(ci.hand, angle=-2 * PI, about_point=ci.cc, rate_func=linear), run_time=0.6)
        # identity: one tall bar; the factor fills part of it, the tissue and the history fill the rest
        self.at("the factor")
        bx, by0, bh, bw = 2.2, -3.0, 5.6, 1.5
        frame = Rectangle(width=bw, height=bh, stroke_color=GREY, stroke_width=4, fill_opacity=0).move_to(P3(bx, by0 + bh / 2))
        idl = T("identity", 40, TEXT, font=TITLE_FONT).move_to(P3(bx, by0 + bh + 0.4))
        seg_h = {"f": 1.7, "t": 2.1, "h": 1.8}
        s1 = Rectangle(width=bw, height=seg_h["f"], stroke_width=0, fill_color=GREEN, fill_opacity=0.55).move_to(P3(bx, by0 + seg_h["f"] / 2))
        s2 = Rectangle(width=bw, height=seg_h["t"], stroke_width=0, fill_color=GOLD, fill_opacity=0.5).move_to(P3(bx, by0 + seg_h["f"] + seg_h["t"] / 2))
        s3 = Rectangle(width=bw, height=seg_h["h"], stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to(P3(bx, by0 + seg_h["f"] + seg_h["t"] + seg_h["h"] / 2))
        l1 = T("the factor:\npart of it", 30, GREEN).move_to(P3(bx + 3.0, by0 + seg_h["f"] / 2))
        l2 = T("the tissue", 30, GOLD).move_to(P3(bx + 3.0, by0 + seg_h["f"] + seg_h["t"] / 2))
        l3 = T("the cell's\nhistory", 30, GREY).move_to(P3(bx + 3.0, by0 + seg_h["f"] + seg_h["t"] + seg_h["h"] / 2))
        self.play(FadeIn(frame), FadeIn(idl, shift=DOWN * 0.1), FadeIn(s1, shift=UP * 0.2), FadeIn(l1, shift=LEFT * 0.1), run_time=0.7)
        self.at("the tissue")
        self.play(FadeIn(s2, shift=UP * 0.2), FadeIn(l2, shift=LEFT * 0.1), run_time=0.5)
        self.at("history")
        self.play(FadeIn(s3, shift=UP * 0.2), FadeIn(l3, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


class S26End(EndCard):
    LINE = "A brake and a clock; the factor carries part of identity."

    def construct(self):
        line = T(self.LINE, size=40, font=TITLE_FONT)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=26, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.45)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.4)
        self.play(FadeIn(sub), run_time=0.3)
        # hold the takeaway for at least five seconds so it can be read
        rest = 5.6 - self.elapsed()
        if rest > 0:
            self.wait(rest)
