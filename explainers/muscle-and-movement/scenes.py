"""Sliding, Not Shrinking: filaments slide, sarcomeres shorten (Biochemistrypedia organismal biology film, chapter 1)

COLOUR MAP (both films): actin thin filament BLUE, myosin thick filament and heads ORANGE, calcium YELLOW,
tropomyosin DARK GREY strand, troponin PURPLE block, ATP GREEN, Z disc BLACK bar (light outline),
calcium store (sarcoplasmic reticulum) PALE TEAL sleeve. Proteins are labelled blocks and rods only.
Every slide, shortening and bend is driven by a tracker (positions computed, not sketched).
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
DGREY = "#7A8497"
TEALP = "#3FB8C0"
ZOUT = "#C9CED8"
PINK = "#E58FB3"

D0 = 5.2          # half length of a resting sarcomere (Z disc centre)
THIN_LEN = 3.8
TY = 1.0          # y of the thin filaments (above and below the thick one)
Y_COVER, Y_OFF = 0.86, 1.2
THICK_HALF = 2.5


def rt(x):
    return max(0.05, x)


def bar(x1, x2, y, h, color, op=0.6):
    return RoundedRectangle(corner_radius=min(0.08, h / 2.2), width=abs(x2 - x1), height=h, stroke_color=color,
                            stroke_width=2, fill_color=color, fill_opacity=op).move_to([(x1 + x2) / 2, y, 0])


def rect(x1, x2, y, h, color, op=1.0):
    return Rectangle(width=abs(x2 - x1), height=h, stroke_width=0, fill_color=color, fill_opacity=op).move_to([(x1 + x2) / 2, y, 0])


def zdisc(x, h=4.4, w=0.2):
    return Rectangle(width=w, height=h, stroke_color=ZOUT, stroke_width=3, fill_color="#000000", fill_opacity=1).move_to([x, 0, 0])


def arrow(a, b, color=TEXT, w=7, tip=0.25):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.6, max_stroke_width_to_length_ratio=14)


def padlock(x, y, s=1.0):
    body = RoundedRectangle(corner_radius=0.08 * s, width=0.8 * s, height=0.6 * s, stroke_color=GOLD, stroke_width=3,
                            fill_color=GOLD, fill_opacity=0.9).move_to([x, y, 0])
    sh = Arc(radius=0.22 * s, start_angle=0, angle=PI, stroke_color=GOLD, stroke_width=7 * s).move_to([x, y + 0.3 * s + 0.11 * s, 0])
    return VGroup(sh, body)


# ---------------------------------------------------------------------------------------------
class Sarc:
    """The one world: a sarcomere whose Z discs, thin filaments and heads follow the tracker `sl`
    (how far each half has slid inward, in the same units as the drawing). Thick filament never changes length."""

    def __init__(self, sl=0.0, cover=False, A=0.0, ca=False):
        self.sl, self.A, self.tm = ValueTracker(sl), ValueTracker(A), ValueTracker(0.0)
        self.tm.add_updater(lambda m, dt: m.increment_value(dt))
        self.zl, self.zr = zdisc(-D0), zdisc(D0)
        self.rods, self.notches, self.strands, self.trns, self.dots, self.meta = [], [], [], [], [], []
        sides = {-1: [self.zl], 1: [self.zr]}
        for side in (-1, 1):
            for vert in (1, -1):
                rod = bar(side * D0, side * (D0 - THIN_LEN), vert * TY, 0.26, BLUE, 0.75)
                xs = [(-2.7 + 0.4 * k) for k in range(-5, 4)]
                nt = VGroup(*[Square(0.13, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([-side * x * -1 if False else (x if side < 0 else -x), vert * 0.87, 0]) for x in xs])
                yc = vert * Y_COVER
                st = Line([side * (D0 - 0.3), yc, 0], [side * (D0 - THIN_LEN + 0.1), yc, 0], color=DGREY, stroke_width=11)
                st.set_cap_style(CapStyleType.ROUND)
                bx = [side * (D0 - 1.1), side * (D0 - 2.5)]
                trn = VGroup(*[Square(0.32, stroke_width=2, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.95).move_to([x, yc, 0]) for x in bx])
                if not cover:
                    st.shift(UP * vert * (Y_OFF - Y_COVER))
                    trn.shift(UP * vert * (Y_OFF - Y_COVER))
                parts = [rod, nt, st, trn]
                if ca:
                    ds = VGroup(*[Circle(0.13, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, vert * (Y_OFF + 0.3), 0]) for x in bx])
                    self.dots.append(ds)
                    parts.append(ds)
                if ca:
                    for dd in ds:
                        dd._y0 = dd.get_center()[1]
                        dd._xx = dd.get_center()[0]
                        dd.add_updater(lambda m: m.set_y(m._y0 + 0.16 * math.sin(self.tm.get_value() * 2.2 + 3 * m._xx)))
                self.rods.append(rod); self.notches.append(nt); self.strands.append(st); self.trns.append(trn)
                self.meta.append((side, vert))
                sides[side].extend(parts)
        for side, ms in sides.items():
            for m in ms:
                self._slide(m, side)
        self.thick = bar(-THICK_HALF, THICK_HALF, 0, 0.64, ORANGE, 0.6)
        self.heads = VGroup()
        j0 = 0
        for side in (-1, 1):
            for vert in (1, -1):
                for j in range(5):
                    h = Line(ORIGIN, RIGHT, color=ORANGE, stroke_width=9)
                    h.set_cap_style(CapStyleType.ROUND)
                    phi = 0.4 * ((j * 0.37 + (0.21 if vert > 0 else 0) + (0.13 if side > 0 else 0)) % 1.0)
                    h.add_updater(self._head_upd(side, vert, -2.4 + 0.4 * j, phi, j0))
                    h.put_start_and_end_on([0, 0, 0], [0.2, 0, 0])
                    self.heads.add(h)
                    j0 += 1
        self.z = VGroup(self.zl, self.zr)

    def _slide(self, m, side):
        m._x0 = m.get_center()[0]
        m.add_updater(lambda mm: mm.shift(RIGHT * ((mm._x0 - side * self.sl.get_value()) - mm.get_center()[0])))

    def _head_upd(self, side, vert, x0, phi, j):
        sg = 1 if side < 0 else -1

        def upd(m):
            sl, A, t = self.sl.get_value(), self.A.get_value(), self.tm.get_value()
            p = ((sl + phi) % 0.4) / 0.4
            xs = x0 - 0.3 - phi
            if p < 0.8:
                xb, yb = xs + 0.4 * p, 0.88
            else:
                q = (p - 0.8) / 0.2
                xb, yb = xs + 0.32 * (1 - q), 0.88 - 0.24 * math.sin(math.pi * q)
            tipx = -D0 + THIN_LEN + sl
            a = A if xb < tipx - 0.05 else 0.0
            xf = x0 - 0.3 + 0.05 * math.cos(t * 2 + j)
            yf = 0.64 + 0.04 * math.sin(t * 2.3 + j)
            x, y = xf + (xb - xf) * a, yf + (yb - yf) * a
            m.put_start_and_end_on([sg * x0, vert * 0.32, 0], [sg * x, vert * y, 0])
        return upd

    def start(self, scene):
        scene.add(self.sl, self.A, self.tm)

    def roll(self, off):
        d = (Y_OFF - Y_COVER) * (1 if off else -1)
        return [m.animate.shift(UP * vert * d) for (side, vert), st, tr in zip(self.meta, self.strands, self.trns) for m in (st,)]

    def everything(self):
        return VGroup(self.z, *self.rods, *self.notches, *self.strands, *self.trns, self.thick, self.heads, *self.dots)


# ---------------------------------------------------------------------------------------------
def chain_mobs(cx, cy, n, w, zh, c, shr=0.17, vis=1.0, arrows=0.0):
    f = 1 - shr * c
    half = n * w / 2
    cen = n // 2
    zs = [cx + (-half + i * w) * f for i in range(n + 1)]
    zw = max(0.07, 0.06 * zh)
    th, hn, off = 0.17 * zh, 0.09 * zh, 0.25 * zh
    g = VGroup()
    ops = [1.0 if (n == 1 or i == cen) else vis for i in range(n)]
    for i in range(n):
        zl, zr = zs[i], zs[i + 1]
        mid = (zl + zr) / 2
        o = ops[i]
        g.add(rect(mid - 0.295 * w, mid + 0.295 * w, cy, th, ORANGE, 0.85 * o))
        for y in (cy + off, cy - off):
            g.add(rect(zl, zl + 0.42 * w, y, hn, BLUE, 0.9 * o))
            g.add(rect(zr - 0.42 * w, zr, y, hn, BLUE, 0.9 * o))
    for i, z in enumerate(zs):
        o = max(ops[max(i - 1, 0)], ops[min(i, n - 1)])
        zb = Rectangle(width=zw, height=zh, stroke_color=ZOUT, stroke_width=2, fill_color="#000000", fill_opacity=1).move_to([z, cy, 0])
        zb.set_stroke(opacity=o).set_fill(opacity=o)
        g.add(zb)
    if arrows > 0.02:
        for z in zs:
            if abs(z - cx) < 1e-6:
                continue
            d = 1 if z < cx else -1
            a = arrow([z, cy + zh * 0.5 + 0.4], [z + d * 0.38, cy + zh * 0.5 + 0.4], TEXT, 5, 0.16)
            a.set_opacity(arrows)
            g.add(a)
    return g


def arm_mobs(ox, oy, k, th, rigid=0.0):
    r = math.radians(th)
    P = lambda x, y: np.array([ox + k * x, oy + k * y, 0.0])
    R = lambda vx, vy: (vx * math.cos(r) - vy * math.sin(r), vx * math.sin(r) + vy * math.cos(r))
    E, S = (0.0, -0.9), (-5.0, -0.9)
    tip = (E[0] + 3.8 * math.cos(r), E[1] + 3.8 * math.sin(r))
    up = Line(P(*S), P(*E), stroke_width=54 * k, color=GREY).set_opacity(0.4)
    fo = Line(P(*E), P(*tip), stroke_width=46 * k, color=GREY).set_opacity(0.4)
    for l in (up, fo):
        l.set_cap_style(CapStyleType.ROUND)
    f = th / 75.0
    f1 = R(1.0, 0.45)
    f2 = R(-0.55, -0.35)
    front = Line(P(-4.0, -0.2), P(E[0] + f1[0], E[1] + f1[1]), stroke_width=36 * k, color=RED)
    back = Line(P(-4.0, -1.6), P(E[0] + f2[0], E[1] + f2[1]), stroke_width=36 * k, color=RED)
    front.set_opacity(max(0.4 + 0.6 * f, rigid))
    back.set_opacity(max(0.4 + 0.6 * (1 - f), rigid))
    for l in (front, back):
        l.set_cap_style(CapStyleType.ROUND)
    joint = Dot(P(*E), radius=0.16 * k * 2, color=TEXT)
    return VGroup(up, fo, back, front, joint)


def looper(tracker, period=3.2, lo=0.0, hi=1.0):
    t = [0.0]

    def u(m, dt):
        t[0] += dt
        m.set_value(lo + (hi - lo) * (0.5 - 0.5 * math.cos(2 * math.pi * t[0] / period)))
    tracker.add_updater(u)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Muscle, Bone and Movement"
    TITLE = "Sliding, Not Shrinking"


def strand_boxes(n=7, w=1.7, h=1.7):
    half = n * w / 2
    box = RoundedRectangle(corner_radius=0.5, width=n * w + 0.25, height=h, stroke_color=RED, stroke_width=4,
                           fill_color=RED, fill_opacity=0.28)
    zs = VGroup(*[Rectangle(width=0.1, height=h, stroke_color=ZOUT, stroke_width=2, fill_color="#000000", fill_opacity=1)
                  .move_to([-half + i * w, 0, 0]) for i in range(n + 1)])
    return box, zs


class S01Hook(SpokenScene):
    def construct(self):
        upper = Line([-5.2, -0.5, 0], [-0.8, -0.5, 0], stroke_width=60, color=GREY).set_opacity(0.35)
        fore = Line([-0.8, -0.5, 0], [1.4, 2.4, 0], stroke_width=50, color=GREY).set_opacity(0.35)
        for l in (upper, fore):
            l.set_cap_style(CapStyleType.ROUND)
        widths = [3.2, 4.0, 4.6, 4.8, 4.6, 4.0, 3.2]
        fibres = VGroup(*[Ellipse(width=wd, height=0.3, stroke_width=2, stroke_color=RED, fill_color=RED, fill_opacity=0.65)
                          .move_to([-3.0, -0.5 + (i - 3) * 0.27, 0]) for i, wd in enumerate(widths)])
        arm = VGroup(upper, fore, fibres).scale(1.3).shift(DOWN * 0.15)
        self.play(FadeIn(arm), run_time=0.8)
        tt = [0.0]

        def shimmer(m, dt):
            tt[0] += dt
            for i, e in enumerate(m):
                e.set_fill(opacity=0.55 + 0.15 * math.sin(tt[0] * 2.5 + i))
        fibres.add_updater(shimmer)
        self.at("shortens")
        self.play(fibres.animate.stretch(0.82, 0, about_point=fibres.get_center()), run_time=1.0)
        self.at("none of its filaments")
        card = chip("The fibre shortens. Do its filaments?", TEXT, 32).move_to([0, -2.9, 0])
        self.play(FadeIn(card, shift=UP * 0.1), run_time=0.7)
        self.at("zoom in")
        box, zs = strand_boxes()
        fibres.clear_updaters()
        f0 = fibres[3]
        self.play(FadeOut(upper), FadeOut(fore), FadeOut(card), *[FadeOut(e) for i, e in enumerate(fibres) if i != 3],
                  Transform(f0, box), run_time=1.5)
        self.play(FadeIn(zs), run_time=0.7)
        zs.add_updater(lambda m, dt=0: None)
        tp = [0.0]

        def pulse(m, dt):
            tp[0] += dt
            m.set_opacity(0.75 + 0.25 * math.sin(tp[0] * 3))
        zs.add_updater(pulse)
        self.finish()


class S02Sarcomere(SpokenScene):
    def construct(self):
        box, zs = strand_boxes()
        self.add(box, zs)
        tp = [0.0]

        def pulse(m, dt):
            tp[0] += dt
            m.set_opacity(0.75 + 0.25 * math.sin(tp[0] * 3))
        zs.add_updater(pulse)
        lab = T("muscle fibre: one long cell", 34, RED).move_to([0, 1.7, 0])
        self.at("one long cell", lead=0.9)
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.9)
        self.at("packed with chains")
        zs.clear_updaters()
        zs.set_opacity(1)
        sweep = Rectangle(width=1.7, height=1.9, stroke_width=0, fill_color=WHITE, fill_opacity=0.18).move_to([-5.1, 0, 0])
        self.play(FadeOut(lab), run_time=0.4)
        self.play(sweep.animate.move_to([5.1, 0, 0]), run_time=rt(self.t_of("sarcomeres") - 0.2 - self.elapsed()), rate_func=linear)
        self.play(FadeOut(sweep), run_time=0.2)
        l2 = T("sarcomeres", 38, TEXT).move_to([0, -1.7, 0])
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.6)
        self.at("each sarcomere runs", lead=0.3)
        hl = Rectangle(width=1.7, height=1.9, stroke_color=WHITE, stroke_width=4, fill_color=WHITE, fill_opacity=0.14)
        self.play(FadeIn(hl), FadeOut(l2), run_time=0.5)
        others = VGroup(box, *[zs[i] for i in range(8) if i not in (3, 4)])
        bigl, bigr = zdisc(-D0), zdisc(D0)
        self.play(FadeOut(others), FadeOut(hl), Transform(zs[3], bigl), Transform(zs[4], bigr), run_time=1.4)
        self.at("one z disc", lead=0.1)
        zl1 = T("Z disc", 30, TEXT).move_to([-D0, 2.65, 0])
        zl2 = T("Z disc", 30, TEXT).move_to([D0, 2.65, 0])
        self.play(FadeIn(zl1), FadeIn(zl2), run_time=0.6)
        self.at("to the next", lead=0.1)
        br = VGroup(Line([-D0, -2.6, 0], [D0, -2.6, 0], color=TEXT, stroke_width=5),
                    Line([-D0, -2.75, 0], [-D0, -2.45, 0], color=TEXT, stroke_width=5),
                    Line([D0, -2.75, 0], [D0, -2.45, 0], color=TEXT, stroke_width=5))
        bl = T("one sarcomere", 32, TEXT).move_to([0, -3.2, 0])
        self.play(Create(br), FadeIn(bl), run_time=0.8)
        self.finish()


class S03Filaments(SpokenScene):
    def construct(self):
        s = Sarc(sl=0.0, cover=True)
        s.start(self)
        zl1 = T("Z disc", 30, TEXT).move_to([-D0, 2.65, 0])
        zl2 = T("Z disc", 30, TEXT).move_to([D0, 2.65, 0])
        self.add(s.z, zl1, zl2)
        grow = [GrowFromEdge(r, LEFT if i < 2 else RIGHT) for i, r in enumerate(s.rods)]
        self.play(*grow, run_time=1.4)
        self.at("actin")
        la = T("actin (thin)", 32, BLUE).move_to([-3.4, 1.8, 0])
        self.play(FadeIn(la, shift=DOWN * 0.1), FadeOut(zl1), FadeOut(zl2), run_time=0.7)
        self.at("a thick filament", lead=0.5)
        self.play(GrowFromCenter(s.thick), run_time=1.2)
        self.at("myosin")
        lm = T("myosin (thick)", 32, ORANGE).move_to([0.9, 1.8, 0])
        self.play(FadeIn(lm, shift=DOWN * 0.1), run_time=0.7)
        self.at("its heads", lead=0.1)
        self.play(FadeIn(s.heads), run_time=0.9)
        lh = T("myosin heads", 32, ORANGE).move_to([0, -2.7, 0])
        self.play(FadeIn(lh, shift=UP * 0.1), run_time=0.6)
        self.at("both sides")
        a1 = arrow([-2.3, -1.8], [-3.8, -1.8], ORANGE)
        a2 = arrow([2.3, -1.8], [3.8, -1.8], ORANGE)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        self.finish()


class S04Switch(SpokenScene):
    def construct(self):
        s = Sarc(sl=0.0, cover=False)
        s.start(self)
        self.add(s.z, *s.rods, s.thick, s.heads)
        nts = VGroup(*s.notches)
        sts = VGroup(*s.strands)
        trns = VGroup(*s.trns)
        self.play(FadeIn(nts), run_time=0.8)
        self.at("strand", lead=0.4)
        self.play(FadeIn(sts), run_time=0.8)
        self.at("tropomyosin")
        lt = T("tropomyosin", 32, "#B3BBCB").move_to([-3.4, 2.1, 0])
        self.play(FadeIn(lt, shift=DOWN * 0.1), run_time=0.6)
        self.at("covers")
        self.play(*[m.animate.shift(DOWN * vert * (Y_OFF - Y_COVER)) for (side, vert), m in zip(s.meta, s.strands)], run_time=1.0)
        self.at("sites", lead=0.1)
        ls = T("myosin-binding sites", 30, WHITE).move_to([-1.0, -2.2, 0])
        ar = arrow([-2.4, -1.85], [-3.0, -1.0], WHITE, 5, 0.2)
        self.play(FadeIn(ls, shift=UP * 0.1), GrowArrow(ar), run_time=0.7)
        self.at("calcium is the switch", lead=0.9)
        sleeve = RoundedRectangle(corner_radius=0.4, width=11.8, height=5.3, stroke_color=TEALP, stroke_width=3,
                                  fill_color=TEALP, fill_opacity=0.08)
        lc = T("calcium store", 28, TEALP).move_to([0, 3.3, 0])
        self.play(FadeOut(lt), FadeOut(ls), FadeOut(ar), FadeIn(sleeve), FadeIn(lc), run_time=0.9)
        self.at("calcium is the switch", lead=0.0)
        xs = [(-4.1, 1), (-2.7, 1), (4.1, 1), (2.7, 1), (-4.1, -1), (-2.7, -1), (4.1, -1), (2.7, -1)]
        dots = VGroup(*[Circle(0.13, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, v * 2.55, 0]) for x, v in xs])
        self.play(FadeIn(dots), run_time=0.3)
        self.play(*[d.animate.move_to([x, v * 1.9, 0]) for d, (x, v) in zip(dots, xs)], run_time=1.4)
        tt = [0.0]

        def hover(m, dt):
            tt[0] += dt
            for i, d in enumerate(m):
                x, v = xs[i]
                d.move_to([x + 0.18 * math.sin(tt[0] * 1.3 + i), v * 1.9 + 0.12 * math.cos(tt[0] * 1.7 + 2 * i), 0])
        dots.add_updater(hover)
        self.at("in skeletal and heart muscle", lead=0.2)
        lsh = T("skeletal and heart muscle", 28, TEXT).move_to([3.6, 3.4, 0])
        self.play(FadeIn(lsh), run_time=0.6)
        self.at("it binds", lead=0.9)
        self.play(FadeIn(trns), run_time=0.6)
        self.at("it binds", lead=0.0)
        dots.clear_updaters()
        self.play(*[d.animate.move_to([x, v * (Y_COVER + 0.3), 0]) for d, (x, v) in zip(dots, xs)], run_time=1.0)
        self.at("and tropinin", lead=0.4)
        lp = T("troponin", 32, PURPLE).move_to([0, 2.15, 0])
        self.play(FadeIn(lp, shift=DOWN * 0.1), run_time=0.5)
        self.at("moves tropomyosin", lead=0.1)
        d = Y_OFF - Y_COVER
        self.play(*[m.animate.shift(UP * vert * d) for (side, vert), m in zip(s.meta, s.strands)],
                  *[m.animate.shift(UP * vert * d) for (side, vert), m in zip(s.meta, s.trns)],
                  *[dd.animate.shift(UP * v * d) for dd, (x, v) in zip(dots, xs)], run_time=1.3)
        self.finish()


class S05Stroke(SpokenScene):
    def construct(self):
        s = Sarc(sl=0.0, cover=False, ca=True)
        s.start(self)
        self.add(s.everything())
        self.at("grab", lead=0.5)
        self.play(s.A.animate.set_value(1.0), run_time=0.8)
        self.at("swing", lead=0.3)
        self.play(s.sl.animate.set_value(0.35), run_time=1.4)
        self.at("heads on each half", lead=0.1)
        a1 = arrow([-2.4, 1.75], [-1.2, 1.75], ORANGE)
        a2 = arrow([2.4, 1.75], [1.2, 1.75], ORANGE)
        a3 = arrow([-2.4, -1.75], [-1.2, -1.75], ORANGE)
        a4 = arrow([2.4, -1.75], [1.2, -1.75], ORANGE)
        arrs = VGroup(a1, a2, a3, a4)
        self.play(FadeIn(arrs), s.sl.animate.set_value(0.42), run_time=0.8)
        self.play(s.sl.animate.set_value(0.85), run_time=rt(self.t_of("inward") - self.elapsed() + 0.3), rate_func=linear)
        self.play(s.sl.animate.set_value(0.95), run_time=rt(self.narration_s + 0.4 - self.elapsed()), rate_func=linear)


class S06Slide(SpokenScene):
    def construct(self):
        s = Sarc(sl=0.95, cover=False, A=1.0, ca=True)
        s.start(self)
        bl = Rectangle(width=1, height=2.3, stroke_width=0, fill_color=WHITE, fill_opacity=0.13)
        br = Rectangle(width=1, height=2.3, stroke_width=0, fill_color=WHITE, fill_opacity=0.13)

        def ub(m, sg):
            tipx = -D0 + THIN_LEN + s.sl.get_value()
            w = max(0.05, tipx + THICK_HALF)
            m.stretch_to_fit_width(w).move_to([sg * (-THICK_HALF + w / 2), 0, 0])
        bl.add_updater(lambda m: ub(m, 1))
        br.add_updater(lambda m: ub(m, -1))
        self.add(s.everything(), bl, br)
        bl.set_z_index(-1); br.set_z_index(-1)
        self.play(s.sl.animate.set_value(1.25), run_time=3.2)
        s.sl.add_updater(lambda m, dt: m.set_value(min(1.4, m.get_value() + 0.03 * dt)))
        self.at("thick filament keeps", lead=0.3)
        tr = VGroup(Line([-THICK_HALF, -2.6, 0], [THICK_HALF, -2.6, 0], color=ORANGE, stroke_width=6),
                    Line([-THICK_HALF, -2.45, 0], [-THICK_HALF, -2.75, 0], color=ORANGE, stroke_width=6),
                    Line([THICK_HALF, -2.45, 0], [THICK_HALF, -2.75, 0], color=ORANGE, stroke_width=6))
        tl = T("thick filament: same length", 30, ORANGE).move_to([0, -3.3, 0])
        self.play(Create(tr), FadeIn(tl), run_time=0.9)
        self.at("thin ones", lead=0.9)
        thr = VGroup(Line([-1.9, 0, 0], [1.9, 0, 0], color=BLUE, stroke_width=6),
                     Line([-1.9, -0.15, 0], [-1.9, 0.15, 0], color=BLUE, stroke_width=6),
                     Line([1.9, -0.15, 0], [1.9, 0.15, 0], color=BLUE, stroke_width=6))
        thr.add_updater(lambda m: m.move_to([s.zl.get_x() + 1.9, 2.6, 0]))
        thr.move_to([s.zl.get_x() + 1.9, 2.6, 0])
        thl = T("thin filament: same length", 30, BLUE).move_to([-3.4, 3.2, 0])
        self.play(Create(thr), FadeIn(thl), run_time=0.9)
        self.at("overlap")
        ol = T("overlap grows", 32, WHITE).move_to([4.9, -2.6, 0])
        self.play(FadeIn(ol, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07Atp(SpokenScene):
    def construct(self):
        thick = bar(-6.5, 6.5, 2.5, 1.0, ORANGE, 0.55)
        actin = bar(-6.8, 6.8, -1.9, 0.5, BLUE, 0.75)
        ax = ValueTracker(0.0)
        bound = ValueTracker(1.0)
        fx, fy = ValueTracker(-0.9), ValueTracker(-1.45)
        ref = [0.0]
        NX = [-0.9 + 1.4 * k for k in range(-5, 6)]
        notches = VGroup(*[Square(0.3, stroke_width=0, fill_color=WHITE, fill_opacity=0.95).move_to([x, -1.6, 0]) for x in NX])
        for m, x0 in zip(notches, NX):
            def u(mm, x0=x0):
                x = x0 + ax.get_value()
                mm.move_to([x, -1.6, 0])
                mm.set_opacity(1.0 if abs(x) < 6.4 else 0.0)
            m.add_updater(u)
        stalk = Line(ORIGIN, RIGHT, color=ORANGE, stroke_width=26)
        stalk.set_cap_style(CapStyleType.ROUND)
        knob = Dot(radius=0.34, color=ORANGE)

        def hu(m):
            if bound.get_value() > 0.5:
                tx, ty = -0.9 + ax.get_value() - ref[0], -1.4
            else:
                tx, ty = fx.get_value(), fy.get_value()
            stalk.put_start_and_end_on([0, 2.0, 0], [tx, ty, 0])
            knob.move_to([tx, ty, 0])
        head = VGroup(stalk, knob)
        head.add_updater(hu)
        self.add(ax, bound, fx, fy)
        self.add(thick, actin, notches, head)
        lh = T("myosin head", 30, ORANGE).move_to([-4.0, 1.2, 0])
        lac = T("actin", 30, BLUE).move_to([5.6, -0.9, 0])
        self.play(FadeIn(lh), FadeIn(lac), ax.animate.set_value(1.4), run_time=1.7, rate_func=smooth)
        self.at("tiny distance", lead=0.3)
        brk = VGroup(Line([-0.9, -2.55, 0], [0.5, -2.55, 0], color=TEXT, stroke_width=5),
                     Line([-0.9, -2.7, 0], [-0.9, -2.4, 0], color=TEXT, stroke_width=5),
                     Line([0.5, -2.7, 0], [0.5, -2.4, 0], color=TEXT, stroke_width=5))
        bt = T("a tiny distance", 30, TEXT).move_to([-0.2, -3.2, 0])
        self.play(Create(brk), FadeIn(bt), run_time=0.8)
        self.at("further along", lead=0.1)
        ring = Circle(0.35, stroke_color=WHITE, stroke_width=4).move_to([-0.9, -1.6, 0])
        self.play(FadeOut(brk), FadeOut(bt), FadeIn(ring), run_time=0.7)
        atp = VGroup(Circle(0.38, stroke_width=0, fill_color=GREEN, fill_opacity=1), T("ATP", 24, "#0f1117", weight=BOLD)).move_to([5.6, 0.6, 0])
        self.at("atp binds", lead=1.6)
        self.play(FadeIn(atp, shift=LEFT * 0.3), run_time=0.7)
        tt = [0.0]
        base = [5.6, 0.6]

        def jit(m, dt):
            tt[0] += dt
            m.move_to([base[0] + 0.15 * math.sin(tt[0] * 2), base[1] + 0.12 * math.cos(tt[0] * 2.6), 0])
        atp.add_updater(jit)
        self.at("atp binds", lead=0.2)
        atp.remove_updater(jit)
        self.play(atp.animate.move_to([0.95, -0.85, 0]), run_time=1.0)
        l1 = T("ATP binds: let go", 30, GREEN).move_to([-4.0, 0.2, 0])
        self.play(FadeIn(l1), run_time=0.5)
        self.at("lets go", lead=0.1)
        fx.set_value(-0.9 + ax.get_value() - ref[0]); fy.set_value(-1.4)
        bound.set_value(0.0)
        self.play(fy.animate.set_value(-0.85), atp.animate.shift(RIGHT * 0.15 + UP * 0.1), run_time=0.8)
        self.at("atp is split", lead=0.2)
        l2 = T("ATP split: re-cock", 30, GREEN).move_to([-4.0, 0.2, 0])
        self.play(FadeOut(l1), FadeIn(l2), run_time=0.5)
        p1 = Circle(0.2, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to(atp.get_center())
        p2 = Circle(0.2, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to(atp.get_center())
        self.play(FadeOut(atp), FadeIn(p1), FadeIn(p2), run_time=0.2)
        self.play(p1.animate.shift(RIGHT * 1.2 + UP * 0.5), p2.animate.shift(RIGHT * 0.9 + DOWN * 0.1), run_time=0.9)
        self.at("recocks", lead=0.2)
        self.play(fx.animate.set_value(-0.9), fy.animate.set_value(-0.95), run_time=1.2)
        self.at("grabs", lead=0.1)
        self.play(fy.animate.set_value(-1.4), run_time=0.6)
        ref[0] = ax.get_value()
        bound.set_value(1.0)
        self.play(FadeOut(ring), run_time=0.3)
        self.at("swings", lead=0.2)
        l3 = T("swing = the pull", 30, GREEN).move_to([-4.0, 0.2, 0])
        self.play(FadeOut(l2), FadeIn(l3), ax.animate.set_value(2.8), p1.animate.shift(RIGHT * 2.5 + UP * 0.8),
                  p2.animate.shift(RIGHT * 2.5 + DOWN * 0.6), run_time=1.5, rate_func=smooth)
        self.finish()


def atp_dots(n=10):
    rng = np.random.RandomState(4)
    base = []
    for i in range(n):
        base.append((rng.uniform(-4.8, 4.8), (1 if i % 2 == 0 else -1) * rng.uniform(1.5, 2.0)))
    return base


class S08Predict(SpokenScene):
    def construct(self):
        s = Sarc(sl=1.3, cover=False, A=1.0, ca=True)
        s.start(self)
        self.add(s.everything())
        base = atp_dots()
        dots = VGroup(*[Circle(0.14, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([x, y, 0]) for x, y in base])
        tt = [0.0]

        def drift(m, dt):
            tt[0] += dt
            for i, d in enumerate(m):
                x, y = base[i]
                d.move_to([x + 0.35 * math.sin(tt[0] * 0.9 + i), y + 0.2 * math.cos(tt[0] * 1.1 + 1.7 * i), 0])
        dots.add_updater(drift)
        self.play(FadeIn(dots), run_time=0.6)
        self.at("take away all the atp")
        lab = T("ATP", 32, GREEN).move_to([-6.0, 2.9, 0])
        self.play(FadeOut(dots), run_time=1.2)
        self.at("do the head stay stuck", lead=0.3)
        card = chip("No ATP: stuck or free?", TEXT, 36).move_to([0, -3.1, 0])
        self.play(FadeIn(card, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        s = Sarc(sl=1.3, cover=False, A=1.0, ca=True)
        s.start(self)
        self.add(s.everything())
        card = chip("No ATP: stuck or free?", TEXT, 36).move_to([0, -3.1, 0])
        self.add(card)
        prog = ValueTracker(1.0)
        ring = always_redraw(lambda: VGroup(
            Circle(0.6, stroke_color=GREY, stroke_width=3),
            Arc(radius=0.6, start_angle=PI / 2, angle=2 * PI * max(prog.get_value(), 0.001), stroke_color=GOLD, stroke_width=10)).move_to([5.9, -3.0, 0]))
        self.add(ring)
        self.play(prog.animate.set_value(0.0), run_time=self.narration_s, rate_func=linear)
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        s = Sarc(sl=1.3, cover=False, A=1.0, ca=True)
        s.start(self)
        self.add(s.everything())
        card = chip("No ATP: stuck or free?", TEXT, 36).move_to([0, -3.1, 0])
        self.add(card)
        c2 = chip("Stuck: heads stay clamped", ORANGE, 36).move_to([0, -3.1, 0])
        self.play(Transform(card, c2), run_time=0.7)
        self.at("without atp", lead=0.2)
        c3 = chip("No ATP: heads cannot let go", ORANGE, 36).move_to([0, -3.1, 0])
        self.play(Transform(card, c3), run_time=0.7)
        self.at("locks stiff", lead=0.4)
        lk = padlock(0, 3.05, 1.2)
        self.play(FadeIn(lk, scale=1.3), run_time=0.7)
        self.at("that is why muscles", lead=0.3)
        arm = arm_mobs(-0.8, 0.0, 1.0, 75.0).set_opacity(0)
        th = ValueTracker(75.0)
        rg = ValueTracker(0.0)
        armr = always_redraw(lambda: arm_mobs(0.3, -0.5, 1.2, th.get_value(), rg.get_value()))
        self.play(FadeOut(s.everything()), FadeOut(card), FadeOut(lk), run_time=0.8)
        self.add(armr)
        self.at("stiffen", lead=0.2)
        self.play(th.animate.set_value(10.0), rg.animate.set_value(1.0), run_time=1.3)
        lk2 = padlock(0.3, 0.8, 1.2)
        self.play(FadeIn(lk2, scale=1.3), run_time=0.5)
        self.at("rigor mortis", lead=0.3)
        lab = T("rigor mortis: heads cannot let go", 32, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.7)
        self.finish()


CY = 0.1
CW, CZH, CN = 1.7, 3.2, 7


class S11SeriesQ(SpokenScene):
    def construct(self):
        c, vis, arr = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        looper(c, 3.2, 0.0, 1.0)
        ch = always_redraw(lambda: chain_mobs(0, CY, CN, CW, CZH, c.get_value(), vis=vis.get_value(), arrows=arr.get_value()))
        self.add(c, vis, arr, ch)
        lab = T("one sarcomere: a tiny shift", 36, TEXT).move_to([0, 2.5, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.7)
        self.at("so how does")
        q = T("how does this become a pull you can see?", 32, YELLOW).move_to([0, -2.2, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.8)
        self.at("the answer is")
        self.play(vis.animate.set_value(1.0), FadeOut(lab), FadeOut(q), run_time=1.8)
        self.finish()


class S12Series(SpokenScene):
    def construct(self):
        c, arr = ValueTracker(0.0), ValueTracker(0.0)
        ch = always_redraw(lambda: chain_mobs(0, CY, CN, CW, CZH, c.get_value(), vis=1.0, arrows=arr.get_value()))
        ell = VGroup(*[Dot(radius=0.05, color=TEXT).move_to([sx * (6.15 + 0.17 * i), CY, 0]) for sx in (-1, 1) for i in range(3)])
        self.add(c, arr, ch, ell)
        sweep = Rectangle(width=CW, height=CZH + 0.4, stroke_width=0, fill_color=WHITE, fill_opacity=0.16).move_to([-5.1, CY, 0])
        self.play(FadeIn(sweep), run_time=0.4)
        self.play(sweep.animate.move_to([5.1, CY, 0]), run_time=rt(self.t_of("tens of thousands") - 0.4 - self.elapsed()), rate_func=linear)
        note = T("schematic: real fibres hold tens of thousands in a row", 26, TEXT).move_to([0, -3.5, 0])
        self.play(FadeIn(note), sweep.animate.move_to([-5.1, CY, 0]), run_time=rt(self.t_of("each one shortens") - 0.4 - self.elapsed()), rate_func=linear)
        self.play(FadeOut(sweep), run_time=0.2)
        self.at("each one shortens", lead=0.2)
        self.play(arr.animate.set_value(1.0), run_time=0.4)
        self.play(c.animate.set_value(0.45), run_time=1.6)
        self.at("their small shortenings", lead=0.3)
        self.play(c.animate.set_value(1.0), run_time=rt(self.t_of("add up") - self.elapsed() + 0.9), rate_func=linear)
        right0 = 0.5 * CN * CW
        ghost = DashedLine([right0, -2.0, 0], [right0, -2.4, 0], color=TEXT, stroke_width=4)
        mk = always_redraw(lambda: Circle(0.2, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to([right0 * (1 - 0.17 * c.get_value()), -2.2, 0]))
        sa = always_redraw(lambda: arrow([right0, -2.2], [right0 * (1 - 0.17 * c.get_value()), -2.2], WHITE, 6, 0.2) if c.get_value() > 0.9 else VGroup())
        self.play(FadeIn(ghost), FadeIn(mk), FadeOut(note), run_time=0.5)
        self.add(sa)
        self.at("visible pull", lead=0.5)
        lb = T("chain end moves the sum", 34, WHITE).move_to([2.6, -3.0, 0])
        self.play(FadeIn(lb, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S13Pull(SpokenScene):
    def construct(self):
        c = ValueTracker(0.0)
        ch = always_redraw(lambda: chain_mobs(0, CY, CN, CW, CZH, c.get_value(), vis=1.0))
        ell = VGroup(*[Dot(radius=0.05, color=TEXT).move_to([sx * (6.15 + 0.17 * i), CY, 0]) for sx in (-1, 1) for i in range(3)])
        self.add(c, ch, ell)
        sweep = Rectangle(width=CW, height=CZH + 0.4, stroke_width=0, fill_color=WHITE, fill_opacity=0.16).move_to([-5.1, CY, 0])
        self.play(FadeIn(sweep), run_time=0.3)
        self.play(sweep.animate.move_to([5.1, CY, 0]), run_time=rt(self.t_of("can pull its ends") - 0.5 - self.elapsed()), rate_func=linear)
        self.play(FadeOut(sweep), run_time=0.2)
        self.at("can pull its ends", lead=0.1)
        self.play(c.animate.set_value(1.0), run_time=2.4)
        self.at("cannot push", lead=0.4)
        xe = 0.5 * CN * CW * (1 - 0.17)
        al = arrow([-xe - 0.3, CY + 2.2], [-xe - 1.6, CY + 2.2], TEXT, 9, 0.3)
        ar = arrow([xe + 0.3, CY + 2.2], [xe + 1.6, CY + 2.2], TEXT, 9, 0.3)
        self.play(GrowArrow(al), GrowArrow(ar), run_time=0.7)
        def X(cx, cy):
            return VGroup(Line([cx - 0.35, cy - 0.35, 0], [cx + 0.35, cy + 0.35, 0], color=RED, stroke_width=10),
                          Line([cx - 0.35, cy + 0.35, 0], [cx + 0.35, cy - 0.35, 0], color=RED, stroke_width=10))
        xs = VGroup(X(-xe - 0.95, CY + 2.2), X(xe + 0.95, CY + 2.2))
        self.play(Create(xs), run_time=0.5)
        lb = T("muscles only pull", 42, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(lb, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S14Antag(SpokenScene):
    def construct(self):
        th = ValueTracker(75.0)
        arm = always_redraw(lambda: arm_mobs(0.3, -0.5, 1.2, th.get_value()))
        self.add(th, arm)
        self.at("stretch it back", lead=1.0)
        self.play(th.animate.set_value(0.0), run_time=1.6)
        self.at("bends the elbow", lead=0.6)
        l1 = T("bends", 40, TEXT).move_to([3.4, 2.9, 0])
        self.play(th.animate.set_value(75.0), FadeIn(l1), run_time=1.3)
        self.at("straightens", lead=0.6)
        l2 = T("straightens", 40, TEXT).move_to([3.4, 2.9, 0])
        self.play(th.animate.set_value(0.0), FadeOut(l1), FadeIn(l2), run_time=1.3)
        self.at("each takes a turn", lead=0.3)
        self.play(th.animate.set_value(75.0), FadeOut(l2), run_time=1.2)
        self.play(th.animate.set_value(0.0), run_time=1.2)
        self.finish()


def heart_icon(x, y, s=0.05):
    f = ParametricFunction(lambda t: np.array([16 * math.sin(t) ** 3, 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t), 0]),
                           t_range=[0, 2 * PI], stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.8)
    return f.scale(s).move_to([x, y, 0])


def gut_icon(x, y):
    f = ParametricFunction(lambda t: np.array([t, 0.28 * math.sin(2.6 * t), 0]), t_range=[-0.9, 0.9], stroke_color=PINK, stroke_width=16)
    f.set_cap_style(CapStyleType.ROUND)
    return f.move_to([x, y, 0])


def fly_icon(x, y):
    body = Ellipse(0.4, 0.8, stroke_width=2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.9)
    head = Dot(radius=0.16, color=GREY).move_to([0, 0.5, 0])
    w1 = Ellipse(0.35, 0.8, stroke_width=2, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.35).rotate(0.7).move_to([-0.5, 0.1, 0])
    w2 = Ellipse(0.35, 0.8, stroke_width=2, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.35).rotate(-0.7).move_to([0.5, 0.1, 0])
    return VGroup(w1, w2, body, head).move_to([x, y, 0])


def toggle(x, y):
    box = RoundedRectangle(corner_radius=0.17, width=0.75, height=0.36, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW, fill_opacity=0.15)
    knob = Circle(0.12, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to(box.get_left() + RIGHT * 0.22)
    return VGroup(box, knob).move_to([x, y, 0])


class S15Rule(SpokenScene):
    def construct(self):
        c = ValueTracker(0.0)
        looper(c, 3.0, 0.0, 1.0)
        th = ValueTracker(0.0)
        th.add_updater(lambda m: m.set_value(75 * c.get_value()))
        p1 = always_redraw(lambda: chain_mobs(-4.3, 1.5, 1, 3.4, 1.7, c.get_value(), shr=0.17))
        p2 = always_redraw(lambda: chain_mobs(0.0, 1.5, 4, 0.95, 1.1, c.get_value()))
        p3 = always_redraw(lambda: arm_mobs(4.55, 1.5, 0.4, th.get_value()))
        self.add(c, th)
        self.at("filament slide", lead=0.0)
        l1 = T("filaments slide", 30, TEXT).move_to([-4.3, 0.15, 0])
        self.add(p1)
        self.play(FadeIn(l1), run_time=0.6)
        self.at("many small slides", lead=0.2)
        l2 = T("many small slides", 30, TEXT).move_to([0, 0.15, 0])
        self.add(p2)
        self.play(FadeIn(l2), run_time=0.6)
        self.at("one pull", lead=0.2)
        l3 = T("one pull", 30, TEXT).move_to([4.3, 0.15, 0])
        self.add(p3)
        self.play(FadeIn(l3), run_time=0.6)
        self.at("same machine", lead=0.4)
        top = T("same machine", 34, TEXT).move_to([0, 3.5, 0])
        rule = Line([-6.2, 3.1, 0], [6.2, 3.1, 0], color=TEXT, stroke_width=4)
        self.play(FadeIn(top, shift=DOWN * 0.1), Create(rule), run_time=0.7)
        self.at("they differ", lead=0.2)
        icons = [(heart_icon(-4.9, -1.4), "heart"), (gut_icon(-0.7, -1.4), "gut"), (fly_icon(3.7, -1.4), "fly")]
        labs = VGroup(*[T(n, 26, TEXT).move_to([m.get_center()[0], -2.4, 0]) for m, n in icons])
        self.play(*[FadeIn(m) for m, n in icons], FadeIn(labs), run_time=0.8)
        self.at("calcium throws", lead=0.3)
        tg = VGroup(toggle(-3.5, -1.4), toggle(0.9, -1.4), toggle(5.1, -1.4))
        self.play(FadeIn(tg), run_time=0.6)
        self.at("throws the switch", lead=0.1)
        qs = VGroup(*[T("?", 40, YELLOW).move_to([t.get_center()[0], -0.75, 0]) for t in tg])
        self.play(FadeIn(qs, shift=DOWN * 0.1), run_time=0.5)
        cap = T("same machine, different switches", 32, YELLOW).move_to([0, -3.3, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S16End(EndCard):
    LINE = "Filaments slide, never shrink; many small slides add up to one pull."
