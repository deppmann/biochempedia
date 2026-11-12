"""Which Side Grows Faster?  (plant-signals, film 1)

COLOUR MAP: auxin = GOLD dots; light = BLUE arrows; lit flank = PALE green; shaded flank = ORANGE;
unknown messenger = white dots; question = YELLOW.  Every curve is computed or marked schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PALE = "#9AD98B"
ORANGE = "#F2994A"
LEAF = "#3f8f4f"
SILVER = "#C9D1D9"
CREAM = "#E8E0C8"
NIGHT = "#0d1b4a"
LAMP = np.array([-6.0, 1.5, 0.0])
Z0, Z1 = 0.12, 0.62


def lab(text, x, y, size=28, color=TEXT, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def smooth(u):
    u = float(np.clip(u, 0, 1))
    return u * u * (3 - 2 * u)


class Film(SpokenScene):
    def setup(self):
        super().setup()
        self.clock = ValueTracker(0)
        self.clock.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.clock)

    def room(self, phrase, nth=0, lead=0.2, lo=0.15):
        return max(lo, self.t_of(phrase, nth) - lead - self.elapsed())

    def left(self, lo=0.3):
        return max(lo, self.narration_s - self.elapsed() - 0.05)


class Shoot:
    """A shoot as two columns of cells along a centre line that bends inside a zone (bend > 0 leans LEFT)."""

    def __init__(self, scene, bx, by=-3.5, h=5.0, w=2.0, bend=0.0, cells=0.0, split=0.0, op=1.0, K=12,
                 inner=False, lcol=PALE, rcol=ORANGE):
        self.bx, self.by, self.h, self.w = ValueTracker(bx), ValueTracker(by), ValueTracker(h), w
        self.bend, self.cells, self.split, self.op = ValueTracker(bend), ValueTracker(cells), ValueTracker(split), ValueTracker(op)
        self.K, self.inner, self.lcol, self.rcol = K, inner, lcol, rcol
        self.N = K * 4
        self._key, self._val = None, None
        scene.add(self.bx, self.by, self.h, self.bend, self.cells, self.split, self.op)
        self.mob = always_redraw(self._draw)
        scene.add(self.mob)

    def cl(self, bend=None, h=None):
        bend = self.bend.get_value() if bend is None else bend
        h = self.h.get_value() if h is None else h
        key = (round(self.bx.get_value(), 4), round(self.by.get_value(), 4), round(h, 4), round(bend, 4))
        if key == self._key:
            return self._val
        N = self.N
        pts = [np.array([key[0], key[1], 0.0])]
        ths = [0.0]
        ds = h / N
        for i in range(1, N + 1):
            th = bend * smooth(((i - 0.5) / N - Z0) / (Z1 - Z0))
            pts.append(pts[-1] + np.array([-np.sin(th), np.cos(th), 0]) * ds)
            ths.append(bend * smooth((i / N - Z0) / (Z1 - Z0)))
        self._key, self._val = key, (np.array(pts), np.array(ths))
        return self._val

    def point(self, s, u=0.0, bend=None, h=None):
        pts, ths = self.cl(bend, h)
        f = float(np.clip(s, 0, 1)) * self.N
        i = min(int(f), self.N - 1)
        r = f - i
        p = pts[i] * (1 - r) + pts[i + 1] * r
        th = ths[i] * (1 - r) + ths[i + 1] * r
        return p + np.array([np.cos(th), np.sin(th), 0]) * u * self.w

    def heading(self, bend=None):
        return self.cl(bend)[1][-1]

    def _band(self, a, b, i0, i1, fill, stroke, sw=3):
        pts, ths = self.cl()
        L = [pts[i] + np.array([np.cos(ths[i]), np.sin(ths[i]), 0]) * a * self.w for i in range(i0, i1 + 1)]
        R = [pts[i] + np.array([np.cos(ths[i]), np.sin(ths[i]), 0]) * b * self.w for i in range(i0, i1 + 1)]
        o = self.op.get_value()
        return Polygon(*(L + R[::-1]), stroke_color=stroke, stroke_width=sw, stroke_opacity=o,
                       fill_color=fill, fill_opacity=0.95 * o)

    def _draw(self):
        g = VGroup()
        c, sp = self.cells.get_value(), self.split.get_value()
        lc, rc = self.lcol, interpolate_color(ManimColor(self.lcol), ManimColor(self.rcol), sp)
        for (a, b, col) in ((-0.5, 0.0, ManimColor(lc)), (0.0, 0.5, rc)):
            sc = interpolate_color(col, ManimColor(BG), c)
            for k in range(self.K):
                g.add(self._band(a, b, 4 * k, 4 * k + 4, col, sc))
        if self.inner:
            g.add(self._band(-0.15, 0.15, 3, int(self.N * 0.92), LEAF, LEAF, 1))
        return g


def dots(scene, n, posfn, op=None, color=GOLD, r=0.085):
    def build():
        c = scene.clock.get_value()
        o = 1.0 if op is None else op.get_value()
        g = VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        for i in range(n):
            p, m = posfn(i, c)
            if o * m > 0.02:
                g.add(Dot(p, radius=r, color=color).set_opacity(min(1, o * m)))
        return g
    m = always_redraw(build)
    scene.add(m)
    return m


def jig(i, c, k=1.0):
    return np.array([0.05 * np.sin(c * 1.3 * k + i * 1.7), 0.05 * np.cos(c * 1.1 * k + i * 2.3), 0])


def rays(scene, x0, x1, ys, op):
    def build():
        o = op.get_value()
        c = scene.clock.get_value()
        g = VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        if o < 0.02:
            return g
        for y in ys:
            g.add(Arrow([x0, y, 0], [x1, y, 0], buff=0, color=BLUE, stroke_width=6, tip_length=0.25,
                        max_tip_length_to_length_ratio=0.5).set_opacity(0.9 * o))
            for j in range(3):
                f = (c * 0.35 + j / 3 + y * 0.1) % 1
                g.add(Dot([x0 + f * (x1 - x0), y, 0], radius=0.09, color=TEXT).set_opacity(o * np.sin(np.pi * f)))
        return g
    m = always_redraw(build)
    scene.add(m)
    return m


def lamp():
    bulb = Circle(radius=0.5, stroke_color=BLUE, stroke_width=5, fill_color=TEXT, fill_opacity=0.9).move_to(LAMP)
    base = Rectangle(width=0.5, height=0.3, stroke_color=GREY, fill_color=GREY, fill_opacity=0.6).move_to(LAMP + LEFT * 0.6)
    return VGroup(base, bulb)


def tracker_op(scene, v=0.0):
    t = ValueTracker(v)
    scene.add(t)
    return t


def bars(scene, f1, f2, op=None):
    """Two flank rulers: lit (green) and shaded (orange). f1, f2: functions giving the lengths."""
    base = -3.0
    def build():
        o = 1.0 if op is None else op.get_value()
        g = VGroup(Dot(ORIGIN, radius=0.001).set_opacity(0))
        for x, f, col in ((3.7, f1, PALE), (4.9, f2, ORANGE)):
            L = max(f(), 0.02)
            g.add(Rectangle(width=0.55, height=L, stroke_color=col, stroke_width=3, stroke_opacity=o,
                            fill_color=col, fill_opacity=0.8 * o).move_to([x, base + L / 2, 0]))
            for k in range(1, int(L / 0.5) + 1):
                g.add(Line([x - 0.45, base + 0.5 * k, 0], [x - 0.3, base + 0.5 * k, 0], color=TEXT, stroke_width=2).set_opacity(o))
        return g
    m = always_redraw(build)
    scene.add(m)
    return m


def stream(scene, shoot, u, s_from, s_to, n, speed=0.25, color=TEXT, op=None, block=None, r=0.08):
    def pf(i, c):
        f = (c * speed + i / n) % 1
        s = s_from + f * (s_to - s_from)
        m = float(np.sin(np.pi * min(1, f * 1.0)) ** 0.5)
        if block is not None and ((s_from > s_to and s < block) or (s_from < s_to and s > block)):
            return shoot.point(block, u), 0.0
        return shoot.point(s, u) + jig(i, c) * 0.5, m
    return dots(scene, n, pf, op, color, r)


def mica_poly(shoot, s, u0, u1, ds=0.012):
    a, b = shoot.point(s - ds, u0), shoot.point(s - ds, u1)
    c, d = shoot.point(s + ds, u1), shoot.point(s + ds, u0)
    return Polygon(a, b, c, d, stroke_color=SILVER, stroke_width=2, fill_color=SILVER, fill_opacity=0.95)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    TITLE = "Which Side Grows Faster?"
    LESSON = "Auxin and Plant Hormones"


class S01Hook(Film):
    def construct(self):
        sh = Shoot(self, 1.0, h=5.0, op=0)
        lp = lamp()
        rop = tracker_op(self)
        rays(self, -5.1, -1.4, [0.4, 1.4, 2.4], rop)
        self.play(FadeIn(lp), sh.op.animate.set_value(1), run_time=0.9)
        self.play(rop.animate.set_value(1), run_time=0.8)
        self.at("bends toward the lamp")
        self.play(sh.bend.animate.set_value(0.55), run_time=2.6, rate_func=smooth)
        # tip pulse + tag
        rop2 = tracker_op(self, 0)
        ring = always_redraw(lambda: Circle(radius=0.5 + 0.1 * np.sin(self.clock.get_value() * 5), color=YELLOW,
                                            stroke_width=5).set_stroke(opacity=rop2.get_value()).move_to(sh.point(1, 0)))
        self.add(ring)
        self.at("The tip senses")
        tag = lab("senses light", 3.7, 2.4, 30, YELLOW)
        lead = Line([2.4, 2.4, 0], sh.point(1, 0.5) + RIGHT * 0.5, color=YELLOW, stroke_width=3)
        self.play(rop2.animate.set_value(1), FadeIn(tag), Create(lead), run_time=0.8)
        self.at("bend forms lower down")
        p1, p2 = sh.point(0.15, 0.95), sh.point(0.6, 0.95)
        br = VMobject(color=GREEN, stroke_width=5).set_points_as_corners([p1 + LEFT * 0.25, p1, p2, p2 + LEFT * 0.25])
        bl = lab("bends here", 3.7, (p1[1] + p2[1]) / 2, 30, GREEN)
        self.play(Create(br), FadeIn(bl), run_time=1.0)
        self.at("What carries the message")
        tgt = np.array([3.7, bl.get_center()[1] + 0.9, 0])
        q = lab("?", 3.7, tgt[1], 72, YELLOW)
        self.add(q)
        self.play(q.animate.move_to(tgt + UP * 0.1), run_time=1.0)
        self.play(q.animate.move_to([3.7, min(tgt[1] + 0.6, 1.3), 0]), run_time=0.9)
        self.play(q.animate.move_to(tgt), run_time=self.left(0.3))
        self.finish()


class S02Flanks(Film):
    def construct(self):
        sh = Shoot(self, 1.0, h=5.0, bend=0.55)
        lp = lamp()
        self.add(lp)
        rop = tracker_op(self, 0.45)
        rays(self, -5.1, -1.4, [0.4, 1.4, 2.4], rop)
        self.wait(0.2)
        self.play(sh.bend.animate.set_value(0), sh.cells.animate.set_value(1), run_time=2.4)
        self.at("one on each side")
        self.play(sh.split.animate.set_value(1), run_time=1.4)
        self.at("Each side is called")
        ll = lab("lit flank", -2.2, -1.4, 30, PALE)
        sl = lab("shaded flank", 4.4, -1.4, 30, ORANGE)
        l1 = Line([-0.8, -1.4, 0], [-0.1, -1.4, 0], color=PALE, stroke_width=3)
        l2 = Line([2.1, -1.4, 0], [2.7, -1.4, 0], color=ORANGE, stroke_width=3)
        self.play(FadeIn(ll), FadeIn(sl), Create(l1), Create(l2), run_time=0.8)
        self.at("a flank")
        fl = lab("flank", 1.0, 3.1, 52, TEXT)
        self.play(Write(fl), run_time=0.9)
        self.play(sh.h.animate.set_value(5.3), run_time=self.left(0.3))
        self.finish()


class S03Equal(Film):
    def construct(self):
        sh = Shoot(self, 1.0, h=5.0, cells=1, split=1)
        self.add(lamp())
        rop = tracker_op(self, 0.45)
        rays(self, -5.1, -1.4, [0.4, 1.4, 2.4], rop)
        f = lambda: 0.6 * sh.h.get_value()
        bars(self, f, f)
        self.add(lab("lit", 3.7, -3.5, 28, PALE), lab("shaded", 4.9, -3.5, 28, ORANGE))
        self.play(sh.h.animate.set_value(5.7), run_time=self.room("the shoot grows taller", lo=0.5), rate_func=linear)
        self.play(sh.h.animate.set_value(6.2), run_time=self.room("But it stays perfectly straight"), rate_func=linear)
        tag = lab("same growth on\nboth flanks:\nno bend", 4.9, 2.4, 28, TEXT)
        self.play(FadeIn(tag), sh.h.animate.set_value(6.35), run_time=self.room("however much it grows"), rate_func=linear)
        self.play(sh.h.animate.set_value(6.5), run_time=self.left(0.3), rate_func=linear)
        self.finish()


class S04Unequal(Film):
    def construct(self):
        sh = Shoot(self, 1.0, h=6.5, cells=1, split=1)
        self.add(lamp())
        rop = tracker_op(self, 0.6)
        rays(self, -5.1, -1.4, [0.4, 1.4, 2.4], rop)
        L1, L2 = ValueTracker(3.9), ValueTracker(3.9)
        self.add(L1, L2)
        bars(self, L1.get_value, L2.get_value)
        self.add(lab("lit", 3.7, -3.5, 28, PALE), lab("shaded", 4.9, -3.5, 28, ORANGE))
        self.at("lengthen a little more")
        self.play(L2.animate.set_value(4.7), L1.animate.set_value(4.2), run_time=self.room("curves toward the light"))
        self.play(sh.bend.animate.set_value(0.55), run_time=2.6, rate_func=smooth)
        self.at("A bend is simply")
        cap = lab("bend = difference\nbetween flanks", 4.3, 2.8, 28, TEXT)
        self.play(FadeIn(cap), sh.bend.animate.set_value(0.6), run_time=self.left(0.3))
        self.finish()


def darwin(scene, bA, bB, op=1.0):
    A = Shoot(scene, -2.4, by=-3.5, h=5.0, w=0.9, K=8, bend=bA, op=op)
    B = Shoot(scene, 2.6, by=-3.5, h=5.0, w=0.9, K=8, bend=bB, op=op)
    return A, B


class S05Darwin(Film):
    def construct(self):
        old = Shoot(self, 1.0, h=6.5, cells=1, split=1, bend=0.6)
        lp = lamp()
        self.add(lp)
        rop = tracker_op(self, 0.7)
        rays(self, -5.1, -1.4, [0.4, 1.4, 2.4], rop)
        q = lab("?", 3.3, 0.5, 80, YELLOW)
        self.play(FadeIn(q), run_time=0.6)
        self.at("Charles Darwin")
        A, B = darwin(self, 0.0, 0.0, 0)
        cap = lab("Charles and Francis Darwin, 1880", 0, 3.3, 30, TEXT)
        rop2 = tracker_op(self, 0)
        rays(self, -5.1, -3.3, [-2.0, -0.6, 0.6], rop2)
        rays(self, -0.1, 1.8, [-2.0, -0.6, 0.6], rop2)
        self.play(old.op.animate.set_value(0), FadeOut(q), FadeOut(rop) if False else rop.animate.set_value(0),
                  A.op.animate.set_value(1), B.op.animate.set_value(1), FadeIn(cap), run_time=1.2)
        self.at("canary grass")
        self.play(rop2.animate.set_value(1), run_time=0.8)
        self.at("An opaque cap")
        cy = ValueTracker(2.2)
        capm = always_redraw(lambda: RoundedRectangle(corner_radius=0.2, width=0.95, height=0.75, stroke_color=GREY, stroke_width=4,
                                                      fill_color="#222733", fill_opacity=1).move_to(B.point(1, 0) + UP * 0.3 + UP * cy.get_value()))
        self.add(cy, capm)
        cl = lab("opaque cap", 5.3, 2.3, 30, TEXT)
        self.play(cy.animate.set_value(0), run_time=1.0)
        self.play(FadeIn(cl), run_time=0.5)
        self.at("greatly reduced the bending")
        self.play(A.bend.animate.set_value(0.5), B.bend.animate.set_value(0.08), run_time=self.left(0.4), rate_func=smooth)
        self.finish()


class S06Tip(Film):
    def construct(self):
        A, B = darwin(self, 0.5, 0.08)
        self.add(lamp())
        rop = tracker_op(self, 1)
        rays(self, -5.1, -3.3, [-2.0, -0.6, 0.6], rop)
        rays(self, -0.1, 1.8, [-2.0, -0.6, 0.6], rop)
        capm = always_redraw(lambda: RoundedRectangle(corner_radius=0.2, width=0.95, height=0.75, stroke_color=GREY, stroke_width=4,
                                                      fill_color="#222733", fill_opacity=1).move_to(B.point(1, 0) + UP * 0.3))
        self.add(capm)
        p1, p2 = B.point(0.1, 0.9), B.point(0.55, 0.9)
        br = VMobject(color=BLUE, stroke_width=5).set_points_as_corners([p1 + LEFT * 0.25, p1, p2, p2 + LEFT * 0.25])
        t1 = lab("lower part\nstill lit", 5.4, -1.8, 30, BLUE)
        self.play(Create(br), FadeIn(t1), run_time=1.2)
        self.at("light is sensed mainly near the tip")
        rop2 = tracker_op(self, 0)
        ring = always_redraw(lambda: Circle(radius=0.6 + 0.1 * np.sin(self.clock.get_value() * 5), color=YELLOW,
                                            stroke_width=5).set_stroke(opacity=rop2.get_value()).move_to(B.point(1, 0) + UP * 0.3))
        self.add(ring)
        t2 = lab("light sensed\nnear the tip", 5.4, 2.3, 30, YELLOW)
        self.play(rop2.animate.set_value(1), FadeIn(t2), run_time=0.9)
        self.at("something passes down")
        ar = DashedLine(B.point(0.88, 0.95), B.point(0.3, 0.95), color=TEXT, stroke_width=5).add_tip(tip_length=0.25)
        t3 = lab("something\npasses down?", 5.4, 0.3, 30, TEXT)
        self.play(Create(ar), FadeIn(t3), run_time=1.0)
        stream(self, B, 0.95, 0.88, 0.3, 5, speed=0.3)
        self.wait(self.left(0.3))
        self.finish()


class S07Boysen(Film):
    def construct(self):
        C = Shoot(self, 0.5, by=-3.4, h=0.5, w=1.7, K=10, inner=True)
        cap = lab("Peter Boysen-Jensen, oat, 1910 to 1913", 0, 3.4, 30, TEXT)
        self.play(FadeIn(cap), C.h.animate.set_value(5.8), run_time=3.2, rate_func=smooth)
        self.at("the sheath over")
        t = lab("coleoptile:\nsheath over\nthe first leaf", -3.7, 0.8, 30, PALE)
        ld = Line([-2.3, 0.8, 0], C.point(0.6, -0.5), color=PALE, stroke_width=3)
        self.play(FadeIn(t), Create(ld), run_time=1.0)
        self.at("He slipped thin mica")
        sy = C.point(0.7, 0)[1]
        slit = Line(C.point(0.7, 0.0), C.point(0.7, 0.5), color=BG, stroke_width=8)
        mica = Rectangle(width=1.4, height=0.13, stroke_color=SILVER, fill_color=SILVER, fill_opacity=0.95).move_to([0.5 + 0.63 + 3.0, sy, 0])
        self.add(slit, mica)
        ml = lab("mica", 3.4, sy + 0.5, 30, SILVER)
        self.play(mica.animate.move_to([0.5 + 0.63, sy, 0]), run_time=1.4)
        self.play(FadeIn(ml), run_time=0.4)
        self.at("dissolved chemicals")
        stream(self, C, 0.25, 0.97, 0.2, 10, speed=0.4, block=0.7, r=0.12)
        self.at("into a cut")
        flash = Line(C.point(0.7, -0.5), C.point(0.7, 0.9), color=YELLOW, stroke_width=6)
        self.play(Create(flash), run_time=0.5)
        self.play(FadeOut(flash), run_time=0.5)
        self.wait(self.left(0.3))
        self.finish()


class S08Mica(Film):
    def construct(self):
        A = Shoot(self, -2.6, by=-3.1, h=4.8, w=1.3, K=8, split=1, op=0)
        B = Shoot(self, 3.0, by=-3.1, h=4.8, w=1.3, K=8, split=1, op=0)
        self.add(lamp().scale(0.8).move_to([-6.1, 0.5, 0]))
        ropA, ropB = tracker_op(self, 0), tracker_op(self, 0)
        rays(self, -5.1, -3.3, [-1.8, -0.4, 1.0], ropA)
        rays(self, -0.4, 1.9, [-1.8, -0.4, 1.0], ropB)
        mA = always_redraw(lambda: mica_poly(A, 0.55, -0.05, 0.85).set_opacity(A.op.get_value()))
        mB = always_redraw(lambda: mica_poly(B, 0.55, -0.85, 0.05).set_opacity(B.op.get_value()))
        self.add(mA, mB)
        self.play(A.op.animate.set_value(1), ropA.animate.set_value(1), run_time=1.0)
        self.at("stayed straight")
        la = lab("straight", -2.6, -3.55, 30, TEXT)
        self.play(FadeIn(la), run_time=0.5)
        self.at("With mica on the lit side")
        self.play(B.op.animate.set_value(1), ropB.animate.set_value(1), run_time=1.0)
        self.at("still bent")
        lb = lab("bent", 3.0, -3.55, 30, TEXT)
        self.play(FadeIn(lb), B.bend.animate.set_value(0.5), run_time=2.4, rate_func=smooth)
        self.at("signal runs down")
        ar = DashedLine(B.point(0.95, 0.6), B.point(0.3, 0.6), color=TEXT, stroke_width=5).add_tip(tip_length=0.25)
        self.play(Create(ar), run_time=0.8)
        stream(self, A, 0.3, 0.95, 0.1, 6, speed=0.3, block=0.55)
        stream(self, B, 0.3, 0.95, 0.1, 6, speed=0.3)
        self.wait(self.left(0.3))
        self.finish()


class S09Went(Film):
    def construct(self):
        ov = Rectangle(width=15, height=9, fill_color=NIGHT, fill_opacity=0, stroke_width=0).set_z_index(-10)
        self.add(ov)
        cap = lab("Frits Went, 1928", 0, 3.3, 30, TEXT)
        cx, cy = ValueTracker(-4.0), ValueTracker(-1.0)
        self.add(cx, cy)
        cube = always_redraw(lambda: Rectangle(width=2.4, height=0.6, stroke_color=CREAM, stroke_width=3, fill_color=CREAM,
                                               fill_opacity=0.5).move_to([cx.get_value(), cy.get_value(), 0]))
        self.add(cube)
        self.play(FadeIn(cap), run_time=0.6)
        T1 = Shoot(self, -4.6, by=-0.7, h=1.0, w=0.7, K=3, op=0)
        T2 = Shoot(self, -3.4, by=-0.7, h=1.0, w=0.7, K=3, op=0)
        self.at("stood cut tips")
        self.play(T1.op.animate.set_value(1), T2.op.animate.set_value(1), run_time=0.8)
        self.at("blocks of agar")
        dop = tracker_op(self, 0)
        dtip = tracker_op(self, 1)

        def pf(i, c):
            tx = -4.6 if i % 2 == 0 else -3.4
            f = (c * 0.25 + i / 10) % 1
            x = tx + 0.22 * np.sin(i * 2.1) + (cx.get_value() + 4.0 if False else 0)
            y = -0.3 - f * 1.1
            mm = 1.0 if f < 0.8 else (1 - f) * 5
            if f > 0.35:  # inside the cube: follow it
                return np.array([x + (cx.get_value() + 4.0), y + (cy.get_value() + 1.0), 0]), mm * 1.0
            return np.array([x, y, 0]), mm * dtip.get_value()
        dots(self, 10, pf, dop)
        self.play(dop.animate.set_value(1), run_time=0.8)
        self.at("a gel")
        gl = lab("agar: a gel", -4.0, -2.4, 30, CREAM)
        self.play(FadeIn(gl), run_time=0.6)
        self.at("In darkness")
        self.play(ov.animate.set_fill(NIGHT, 0.65), FadeOut(gl), T1.op.animate.set_value(0), T2.op.animate.set_value(0),
                  dtip.animate.set_value(0), run_time=1.2)
        D = Shoot(self, 2.0, by=-3.4, h=3.8, w=1.2, K=8, op=0)
        self.play(D.op.animate.set_value(1), run_time=0.8)
        self.at("set one block")
        self.play(cx.animate.set_value(1.7), cy.animate.set_value(0.7), run_time=1.5, rate_func=smooth)
        self.at("whose own tip")
        t = lab("own tip\ncut off", 4.9, 1.0, 30, TEXT)
        ld = Line([3.9, 1.0, 0], [2.7, 0.55, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(t), Create(ld), run_time=0.8)
        self.wait(self.left(0.3))
        self.finish()


class S10Curve(Film):
    def construct(self):
        ov = Rectangle(width=15, height=9, fill_color=NIGHT, fill_opacity=0.65, stroke_width=0).set_z_index(-10)
        self.add(ov)
        D = Shoot(self, 2.0, by=-3.4, h=3.8, w=1.2, K=8)
        cube = always_redraw(lambda: Rectangle(width=2.4, height=0.6, stroke_color=CREAM, stroke_width=3, fill_color=CREAM,
                                               fill_opacity=0.5).move_to(D.point(1, -0.25) + UP * 0.3))
        self.add(cube)
        dots(self, 8, lambda i, c: (D.point(1, -0.25) + UP * 0.3 + np.array([0.7 * np.sin(i * 2.3), 0.15 * np.cos(i * 1.9), 0]) + jig(i, c), 1.0))
        self.wait(0.5)
        self.at("curved away from the block")
        self.play(D.bend.animate.set_value(-0.5), run_time=3.4, rate_func=smooth)
        self.at("Something from the tips")
        stream(self, D, -0.25, 0.97, 0.12, 8, speed=0.25, color=GOLD)
        pr = always_redraw(lambda: VGroup(
            DashedLine(D.point(0.12, 0), D.point(0.12, 0) + UP * 3.4, color=TEXT, stroke_width=3),
            Line(D.point(0.12, 0), D.point(0.12, 0) + 3.4 * np.array([-np.sin(D.heading()), np.cos(D.heading()), 0]), color=YELLOW, stroke_width=4)))
        pl = lab("angle measures\nactivity", 5.2, -1.8, 30, YELLOW)
        self.wait(1.2)
        self.play(Create(pr), FadeIn(pl), run_time=1.0)
        self.at("We now call")
        au = lab("auxin", -1.0, 1.3, 52, GOLD)
        self.play(Write(au), run_time=1.0)
        self.play(D.bend.animate.set_value(-0.6), run_time=self.left(0.3))
        self.finish()


class S11Options(Film):
    def construct(self):
        cxs = (-3.0, 4.0)
        tips = VGroup()
        for cx in cxs:
            tips.add(Rectangle(width=1.3, height=3.8, stroke_color=PALE, fill_color=PALE, fill_opacity=0.9).move_to([cx - 0.65, 0, 0]),
                     Rectangle(width=1.3, height=3.8, stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.9).move_to([cx + 0.65, 0, 0]))
        rop = tracker_op(self, 0)
        rays(self, -6.6, -4.4, [-1.0, 0.0, 1.0], rop)
        rays(self, 0.4, 2.6, [-1.0, 0.0, 1.0], rop)
        div = Line([0.0, -2.2, 0], [0.0, 2.6, 0], color=GREY, stroke_width=2)
        self.play(FadeIn(tips), Create(div), rop.animate.set_value(1), run_time=1.0)
        lit = lab("lit", -3.65, -2.3, 28, PALE)
        sha = lab("shaded", -2.3, -2.3, 28, ORANGE)
        lit2 = lab("lit", 3.35, -2.3, 28, PALE)
        sha2 = lab("shaded", 4.7, -2.3, 28, ORANGE)
        self.play(FadeIn(lit), FadeIn(sha), FadeIn(lit2), FadeIn(sha2), run_time=0.6)
        qq = lab("more auxin on the shaded side?", 0, -3.4, 30, YELLOW)
        self.at("with more")
        dop = tracker_op(self, 0)
        D, Mv = ValueTracker(0), ValueTracker(0)
        self.add(D, Mv)
        rng = np.random.RandomState(4)
        base = [(rng.uniform(0.15, 1.2), rng.uniform(-1.6, 1.5)) for _ in range(7)]
        base2 = [(rng.uniform(0.15, 1.2), rng.uniform(-1.6, 1.5)) for _ in range(7)]

        def pf(i, c):
            panel, k = divmod(i, 14)
            cx = cxs[panel]
            if k < 7:   # lit-side dots
                x, y = base[k]
                x = -x
                if panel == 0:
                    return np.array([cx + x, y, 0]) + jig(i, c), 1 - D.get_value()
                return np.array([cx + x * (1 - 2 * smooth(Mv.get_value())), y + 0.3 * smooth(Mv.get_value()) * np.sin(k), 0]) + jig(i, c), 1.0
            x, y = base2[k - 7]
            return np.array([cx + x, y, 0]) + jig(i, c), 1.0
        dots(self, 28, pf, dop)
        self.play(dop.animate.set_value(1), FadeIn(qq), run_time=1.0)
        self.at("Light could destroy")
        dl = lab("destroy", -3.0, 3.1, 40, TEXT)
        self.play(FadeIn(dl), run_time=0.4)
        self.play(D.animate.set_value(1), run_time=2.2)
        self.at("Or light could move")
        ml = lab("move", 4.0, 3.1, 40, TEXT)
        self.play(FadeIn(ml), run_time=0.4)
        self.play(Mv.animate.set_value(1), run_time=2.4)
        self.wait(self.left(0.3))
        self.finish()


def jars_scene(scene, mv_val, with_tips=True):
    objs = {}
    for x in (-4.0, 4.0):
        j = VMobject(color=TEXT, stroke_width=5).set_points_as_corners([[x - 1.3, 0.6, 0], [x - 1.3, -2.6, 0], [x + 1.3, -2.6, 0], [x + 1.3, 0.6, 0]])
        scene.add(j)
    scene.add(lab("total from lit tips", -4.0, -3.2, 28), lab("total from dark tips", 4.0, -3.2, 28))
    return objs


def tip_pair(scene, mv):
    g = VGroup()
    g.add(Rectangle(width=0.8, height=1.0, stroke_color=PALE, fill_color=PALE, fill_opacity=0.9).move_to([-4.4, 2.5, 0]),
          Rectangle(width=0.8, height=1.0, stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.9).move_to([-3.6, 2.5, 0]),
          Rectangle(width=0.8, height=1.0, stroke_color=GREY, fill_color=PALE, fill_opacity=0.35).move_to([3.6, 2.5, 0]),
          Rectangle(width=0.8, height=1.0, stroke_color=GREY, fill_color=PALE, fill_opacity=0.35).move_to([4.4, 2.5, 0]))
    scene.add(g)
    rng = np.random.RandomState(7)
    pts = [(rng.uniform(0.05, 0.35), rng.uniform(-0.4, 0.4)) for _ in range(5)]

    def pf(i, c):
        if i < 5:
            x, y = pts[i]
            x = -4.4 + (x - 0.2) - 0.0 + 1.6 * smooth(mv.get_value()) * (1 if True else 0)
            return np.array([x, 2.5 + y, 0]) + jig(i, c), 1.0
        x, y = pts[i - 5]
        return np.array([4.0 + (x - 0.2) * 2, 2.5 + y, 0]) + jig(i, c), 1.0
    return g, pf


class S12Predict(Film):
    def construct(self):
        mv = ValueTracker(0)
        self.add(mv)
        for x in (-4.0, 4.0):
            j = VGroup(Rectangle(width=2.6, height=3.2, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to([x, -1.0, 0]), VMobject(color=TEXT, stroke_width=5).set_points_as_corners([[x - 1.3, 0.6, 0], [x - 1.3, -2.6, 0], [x + 1.3, -2.6, 0], [x + 1.3, 0.6, 0]]))
            self.play(Create(j), run_time=0.6)
        self.at("Collect all the")
        l1 = lab("total from lit tips", -4.0, -3.2, 28)
        tipL = VGroup(Rectangle(width=0.8, height=1.0, stroke_color=PALE, fill_color=PALE, fill_opacity=0.9).move_to([-4.4, 2.5, 0]),
                      Rectangle(width=0.8, height=1.0, stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.9).move_to([-3.6, 2.5, 0]))
        rop = tracker_op(self, 0)
        rays(self, -6.6, -5.0, [2.5], rop)
        self.play(FadeIn(tipL), FadeIn(l1), rop.animate.set_value(1), run_time=0.9)
        self.at("tips kept dark")
        l2 = lab("total from dark tips", 4.0, -3.2, 28)
        tipD = VGroup(Rectangle(width=0.8, height=1.0, stroke_color=GREY, fill_color=PALE, fill_opacity=0.35).move_to([3.6, 2.5, 0]),
                      Rectangle(width=0.8, height=1.0, stroke_color=GREY, fill_color=PALE, fill_opacity=0.35).move_to([4.4, 2.5, 0]))
        self.play(FadeIn(tipD), FadeIn(l2), run_time=0.9)
        rng = np.random.RandomState(7)
        pts = [(rng.uniform(0.05, 0.35), rng.uniform(-0.4, 0.4)) for _ in range(5)]
        dop = tracker_op(self, 0)

        def pf(i, c):
            if i < 5:
                x, y = pts[i]
                return np.array([-4.5 + x * 2 + 0.8 * smooth(mv.get_value()), 2.5 + y, 0]) + jig(i, c), 1.0
            x, y = pts[i - 5]
            return np.array([3.5 + x * 2 + 0.2 * np.sin(c + i), 2.5 + y, 0]) + jig(i, c), 1.0
        dots(self, 10, pf, dop)
        self.play(dop.animate.set_value(1), run_time=0.6)
        self.at("If light only moves")
        self.play(mv.animate.set_value(1), run_time=self.room("how should the totals compare"), rate_func=smooth)
        card = VGroup(RoundedRectangle(corner_radius=0.2, width=4.2, height=2.0, stroke_color=YELLOW, stroke_width=4),
                      lab("How should the\ntotals compare?", 0, 0, 30, YELLOW)).move_to([0, -0.8, 0])
        self.play(FadeIn(card), run_time=0.8)
        self.wait(self.left(0.3))
        self.finish()


class S13Pause(Film):
    def construct(self):
        for x in (-4.0, 4.0):
            self.add(Rectangle(width=2.6, height=3.2, stroke_width=0, fill_color=TEXT, fill_opacity=0.12).move_to([x, -1.0, 0]))
            self.add(VMobject(color=TEXT, stroke_width=5).set_points_as_corners([[x - 1.3, 0.6, 0], [x - 1.3, -2.6, 0], [x + 1.3, -2.6, 0], [x + 1.3, 0.6, 0]]))
        self.add(lab("total from lit tips", -4.0, -3.2, 28), lab("total from dark tips", 4.0, -3.2, 28))
        self.add(Rectangle(width=0.8, height=1.0, stroke_color=PALE, fill_color=PALE, fill_opacity=0.9).move_to([-4.4, 2.5, 0]),
                 Rectangle(width=0.8, height=1.0, stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.9).move_to([-3.6, 2.5, 0]),
                 Rectangle(width=0.8, height=1.0, stroke_color=GREY, fill_color=PALE, fill_opacity=0.35).move_to([3.6, 2.5, 0]),
                 Rectangle(width=0.8, height=1.0, stroke_color=GREY, fill_color=PALE, fill_opacity=0.35).move_to([4.4, 2.5, 0]))
        self.add(VGroup(RoundedRectangle(corner_radius=0.2, width=4.2, height=2.0, stroke_color=YELLOW, stroke_width=4),
                        lab("How should the\ntotals compare?", 0, 0, 30, YELLOW)).move_to([0, -0.8, 0]))
        rng = np.random.RandomState(7)
        pts = [(rng.uniform(0.05, 0.35), rng.uniform(-0.4, 0.4)) for _ in range(5)]
        dots(self, 10, lambda i, c: (np.array([(-4.5 + pts[i][0] * 2 + 0.8) if i < 5 else (3.5 + pts[i - 5][0] * 2), 2.5 + pts[i % 5][1], 0]) + jig(i, c), 1.0))
        p = ValueTracker(0)
        self.add(p)
        ring = always_redraw(lambda: VGroup(Circle(radius=0.45, color=GREY, stroke_width=4),
                                            Arc(radius=0.45, start_angle=PI / 2, angle=-TAU * max(0.001, 1 - p.get_value()), color=YELLOW, stroke_width=7)).move_to([6.1, -1.7, 0]))
        self.add(ring)
        self.play(p.animate.set_value(1), run_time=self.beat(0.92), rate_func=linear)
        self.finish()


class S14Reveal(Film):
    def construct(self):
        cap = lab("Briggs and colleagues, 1957", 0, 3.3, 30, TEXT)
        tip = Shoot(self, -3.6, by=-1.6, h=3.2, w=2.2, K=6, split=1, op=0)
        rop = tracker_op(self, 0)
        rays(self, -6.6, -4.9, [-0.4, 0.8], rop)
        self.play(FadeIn(cap), tip.op.animate.set_value(1), rop.animate.set_value(1), run_time=1.0)
        self.at("thin barrier")
        bh = ValueTracker(0)
        self.add(bh)
        bar = always_redraw(lambda: Rectangle(width=0.12, height=max(0.01, bh.get_value()), stroke_color=SILVER, fill_color=SILVER, fill_opacity=1)
                            .move_to([-3.6, -2.2 + bh.get_value() / 2, 0]))
        self.add(bar)
        self.play(bh.animate.set_value(2.85), run_time=1.3)
        self.at("caught each half")
        bl = VGroup(Rectangle(width=1.0, height=0.6, stroke_color=CREAM, fill_color=CREAM, fill_opacity=0.5).move_to([-4.2, -1.9, 0]),
                    Rectangle(width=1.0, height=0.6, stroke_color=CREAM, fill_color=CREAM, fill_opacity=0.5).move_to([-3.0, -1.9, 0]))
        nL, nR, ex = ValueTracker(0), ValueTracker(0), tracker_op(self, 0)
        self.add(nL, nR)

        def pf(i, c):
            blk, k = divmod(i, 12)
            if k < 12 and i < 24:
                n = nL.get_value() if blk == 0 else nR.get_value()
                x0 = -4.2 if blk == 0 else -3.0
                p = np.array([x0 - 0.35 + (k % 4) * 0.23, -2.05 + (k // 4) * 0.2, 0])
                return p + jig(i, c) * 0.5, float(np.clip(n - k, 0, 1))
            j = i - 24
            f = (c * 0.3 + j / 6) % 1
            x = -3.0 + 0.15 + 0.3 * np.sin(j * 2.1)
            return np.array([x, 1.2 - f * 3.0, 0]), float(np.sin(np.pi * f) ** 0.5) * ex.get_value()
        dots(self, 30, pf)
        self.play(FadeIn(bl), nL.animate.set_value(3), nR.animate.set_value(3), run_time=2.6)
        self.at("Lit tips gave the same total")
        lv = ValueTracker(0)
        self.add(lv)
        jar_x = (3.4, 5.5)
        jj = VGroup()
        for x in jar_x:
            jj.add(VMobject(color=TEXT, stroke_width=5).set_points_as_corners([[x - 0.75, 0.0, 0], [x - 0.75, -2.6, 0], [x + 0.75, -2.6, 0], [x + 0.75, 0.0, 0]]))
        fill = always_redraw(lambda: VGroup(*[Rectangle(width=1.4, height=max(0.01, lv.get_value()), stroke_width=0, fill_color=GOLD, fill_opacity=0.8)
                                              .move_to([x, -2.6 + max(0.01, lv.get_value()) / 2 + 0.03, 0]) for x in jar_x]))
        self.add(fill)
        jl = VGroup(lab("lit", 3.4, -3.1, 28), lab("dark", 5.5, -3.1, 28), lab("levels schematic", 4.45, -3.55, 24, GREY))
        self.play(FadeIn(jj), FadeIn(jl), run_time=0.6)
        self.play(lv.animate.set_value(1.5), run_time=1.8)
        same = lab("same total", 4.45, 0.7, 30, GOLD)
        self.play(FadeIn(same), run_time=0.5)
        self.at("more came from")
        self.play(nR.animate.set_value(11), ex.animate.set_value(1), run_time=2.0)
        self.wait(self.left(0.3))
        self.finish()


class S15Moved(Film):
    def construct(self):
        sh = Shoot(self, 1.0, h=6.5, cells=1, split=1)
        self.add(lamp())
        rop = tracker_op(self, 0.6)
        rays(self, -5.1, -1.4, [0.4, 1.4, 2.4], rop)
        Mv = ValueTracker(0)
        self.add(Mv)
        rng = np.random.RandomState(3)
        spec = [(rng.uniform(0.76, 0.98), rng.uniform(0.08, 0.42)) for _ in range(14)]
        dop = tracker_op(self, 0)
        fl = ValueTracker(0)
        self.add(fl)

        def pf(i, c):
            s, u = spec[i]
            if i < 7:   # start on the lit side, end on the shaded side
                uu = -u + (2 * u) * smooth(Mv.get_value())
                s2 = s - 0.3 * smooth(fl.get_value()) * ((c * 0.3 + i / 7) % 1)
                return sh.point(s2, uu) + jig(i, c), 1.0
            uu = u
            s2 = s - 0.6 * smooth(fl.get_value()) * ((c * 0.3 + i / 7) % 1)
            return sh.point(s2, uu) + jig(i, c), 1.0
        dots(self, 14, pf, dop, r=0.12)
        sh.h.add_updater(lambda m, dt: m.increment_value(dt * 0.04))
        self.play(dop.animate.set_value(1), run_time=0.8)
        self.at("the unchanged total")
        t1 = lab("total unchanged", 4.7, 2.3, 30, GOLD)
        self.play(FadeIn(t1), run_time=0.6)
        self.at("moving to the shaded side")
        self.play(Mv.animate.set_value(1), run_time=self.room("rather than being destroyed"), rate_func=smooth)
        t2 = lab("moved, not destroyed", 4.4, 2.3, 30, GOLD)
        self.play(Transform(t1, t2), fl.animate.set_value(0.6), run_time=0.8)
        self.play(fl.animate.set_value(1), run_time=max(0.2, self.room("shaded flank grew faster")))
        self.at("shaded flank grew faster")
        L1, L2 = ValueTracker(3.9), ValueTracker(3.9)
        self.add(L1, L2)
        bars(self, L1.get_value, L2.get_value)
        self.add(lab("lit", 3.7, -3.5, 28, PALE), lab("shaded", 4.9, -3.5, 28, ORANGE))
        self.play(L2.animate.set_value(4.7), L1.animate.set_value(4.2), run_time=self.room("the shoot bent toward"))
        self.play(sh.bend.animate.set_value(0.55), run_time=self.left(0.3), rate_func=smooth)
        self.finish()


class S16Scope(Film):
    def construct(self):
        sh = Shoot(self, 1.0, h=6.5, cells=1, split=1)
        lpm = lamp()
        self.add(lpm)
        rop = tracker_op(self, 0.6)
        rays(self, -5.1, -1.4, [0.4, 1.4, 2.4], rop)
        self.wait(0.3)
        ox, oy, SX, SY = -2.6, -2.8, 2.15, 2.0
        g = lambda a: 2.2 * a * np.exp(1 - a)
        P = lambda a, v: np.array([ox + a * SX, oy + v * SY, 0])
        self.play(FadeOut(lpm), sh.bx.animate.set_value(-5.4), sh.h.animate.set_value(4.4), sh.cells.animate.set_value(0), FadeOut(self.mobjects[1]) if False else rop.animate.set_value(0), run_time=1.8, rate_func=smooth)
        ax = VGroup(Arrow(P(0, 0), P(4.1, 0), buff=0, color=TEXT, stroke_width=4, tip_length=0.2),
                    Arrow(P(0, 0), P(0, 2.5), buff=0, color=TEXT, stroke_width=4, tip_length=0.2))
        xl, yl = lab("auxin level", 1.7, -3.4, 28), lab("growth", -1.6, 3.0, 28)
        pin = lab("measured in grass\ncoleoptile tips", -4.9, 2.4, 28, TEXT)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(pin), run_time=1.0)
        self.at("not in strict proportion")
        dl = DashedLine(P(0, 0), P(1.18, 2.6), color=GREY, stroke_width=4)
        self.play(Create(dl), run_time=1.2)
        self.play(FadeOut(dl), run_time=0.5)
        self.at("It rises to a peak")
        rise = ParametricFunction(lambda a: P(a, g(a)), t_range=[0, 1], color=YELLOW, stroke_width=6)
        mk = Dot(P(0.5, g(0.5)), radius=0.12, color=ORANGE)
        self.play(Create(rise), run_time=2.0, rate_func=linear)
        self.play(FadeIn(mk), run_time=0.3)
        ml = lab("shaded flank here (assumed)", 2.4, -2.0, 28, ORANGE)
        ma = Arrow([-0.1, -1.7, 0], P(0.5, g(0.5)) + DOWN * 0.15, buff=0.05, color=ORANGE, stroke_width=3, tip_length=0.2)
        self.play(FadeIn(ml), Create(ma), run_time=0.8)
        self.at("Past that peak")
        fall = ParametricFunction(lambda a: P(a, g(a)), t_range=[1, 4], color=YELLOW, stroke_width=6)
        nl = lab("not proportional;\nfalls past a peak\n(schematic)", 4.2, 1.6, 28, TEXT)
        self.play(Create(fall), FadeIn(nl), run_time=self.left(0.4), rate_func=linear)
        self.finish()


class S17Rule(Film):
    def construct(self):
        xs = (-4.4, 0.2, 4.8)
        p1 = Shoot(self, xs[0], by=-2.9, h=4.0, cells=1, split=1)
        p1.h.add_updater(lambda m, dt: m.increment_value(dt * 0.06))
        c1 = lab("equal growth", xs[0], -3.5, 28, TEXT)
        self.add(c1)
        p2 = Shoot(self, xs[1], by=-2.9, h=4.4, cells=1, split=1, op=0)
        p3 = Shoot(self, xs[2], by=-2.9, h=4.4, cells=1, split=1, op=0)
        r2, r3 = tracker_op(self, 0), tracker_op(self, 0)
        rays(self, -2.6, -1.6, [0.0, 0.9], r2)
        rays(self, 2.2, 3.4, [0.0, 0.9], r3)
        self.wait(0.8)
        self.play(p2.op.animate.set_value(1), r2.animate.set_value(1), FadeIn(lab("unequal growth", xs[1], -3.5, 28, TEXT)), run_time=0.8)
        self.at("difference in growth")
        self.play(p2.bend.animate.set_value(0.55), run_time=1.9, rate_func=smooth)
        self.at("Light makes that difference")
        Mv = ValueTracker(0)
        self.add(Mv)
        rng = np.random.RandomState(5)
        spec = [(rng.uniform(0.78, 0.97), rng.uniform(0.08, 0.42)) for _ in range(10)]
        dop = tracker_op(self, 0)
        dots(self, 10, lambda i, c: (p3.point(spec[i][0], (-spec[i][1] if i < 5 else spec[i][1]) * (1 - 2 * smooth(Mv.get_value())) if i < 5 else spec[i][1]) + jig(i, c), 1.0), dop)
        self.play(p3.op.animate.set_value(1), r3.animate.set_value(1), dop.animate.set_value(1), FadeIn(lab("auxin moves", xs[2], -3.5, 28, GOLD)), run_time=0.9)
        self.at("to the shaded flank")
        self.play(Mv.animate.set_value(1), run_time=1.6, rate_func=smooth)
        self.play(p3.bend.animate.set_value(0.55), run_time=self.left(0.3), rate_func=smooth)
        self.finish()


class S18End(EndCard):
    LINE = "A bend is uneven growth: light shifts auxin to the shaded flank."
