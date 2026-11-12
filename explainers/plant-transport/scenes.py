"""Pulled From the Top: cohesion-tension in the xylem (Biochemistrypedia explainer)

COLOR MAP (shared by both plant-transport films)
  BLUE   = xylem water, water droplets
  AMBER  = phloem / a push (positive pressure)
  GOLD   = solute dots
  RED    = tension, negative pressure
  GREY   = air, vapour, structure
  GREEN  = leaf cells (structure only)
  YELLOW = questions and crosses
"""
import os
import numpy as np
from bp_style import *  # noqa: F401,F403
M = lambda text, size=30, color=TEXT, **kw: T(text, size, color, **kw)  # numbers in the standard font, as in the second film

AMBER = "#F5A623"
LEAF = "#3B8A57"
BARK = "#6B5B4B"
PSI = "Ψ"
MINUS = "−"


class LiveScene(SpokenScene):
    """SpokenScene plus a faint field of drifting motes, so no held frame is a dead frame."""

    def setup(self):
        super().setup()
        import random
        rng = random.Random(os.environ.get("KX_SCENE_ID", "x"))
        ms = VGroup(*[Circle(radius=rng.uniform(0.18, 0.34), stroke_width=0, fill_color=TEXT, fill_opacity=0.16).move_to(
            [rng.uniform(-6.6, 6.6), rng.uniform(-3.7, 3.7), 0]) for _ in range(12)])
        ph = [rng.uniform(0, 7) for _ in ms]
        sp = [rng.uniform(0.25, 0.5) for _ in ms]
        base = [m.get_center().copy() for m in ms]
        ms.tm = 0.0

        def up(m, dt):
            m.tm += dt
            for i, d in enumerate(m):
                y = ((base[i][1] + 3.8 + sp[i] * m.tm) % 7.6) - 3.8
                d.move_to([base[i][0] + 0.3 * np.sin(m.tm * 0.7 + ph[i]), y, 0])

        ms.add_updater(up)
        self.add(ms)


def psi(sub=None, size=36):
    a = T(PSI, size, TEXT)
    if not sub:
        return a
    b = T(sub, 22, TEXT).next_to(a, DR, buff=0.02).shift(UP * 0.08)
    return VGroup(a, b)


def flow(pts, n=8, color=BLUE, r=0.1, speed=0.12, op=0.95):
    """Dots that loop along a polyline forever (an updater), so a held frame is never dead."""
    pts = [np.array(p, float) for p in pts]
    segs = [float(np.linalg.norm(pts[i + 1] - pts[i])) for i in range(len(pts) - 1)]
    tot = sum(segs)

    def at(u):
        d = u * tot
        for i, s in enumerate(segs):
            if d <= s:
                return pts[i] + (pts[i + 1] - pts[i]) * (d / s if s > 0 else 0)
            d -= s
        return pts[-1]

    g = VGroup(*[Dot(pts[0], radius=r * 1.4, color=color) for _ in range(n)])
    g.tt = 0.0

    def up(m, dt):
        m.tt += dt
        for k, d in enumerate(m):
            u = (m.tt * speed + k / n) % 1
            d.move_to(at(u))
            d.set_opacity(op * min(1, u * 6, (1 - u) * 6))

    g.add_updater(up)
    up(g, 0)
    return g


def wiggle(mob, amp=0.05, speed=2.0):
    """Gentle jitter of every child, to keep a still picture alive."""
    kids = list(mob)
    bases = [k.get_center().copy() for k in kids]
    mob.tw = 0.0

    def up(m, dt):
        m.tw += dt
        for i, (k, b) in enumerate(zip(kids, bases)):
            k.move_to(b + amp * np.array([np.sin(m.tw * speed + i * 1.7), np.cos(m.tw * speed * 0.8 + i * 2.3), 0]))

    mob.add_updater(up)
    return mob


class Tree:
    def __init__(self, cx=-4.0, top=3.6, base=-3.4):
        self.cx, self.top, self.base = cx, top, base
        self.ground = VGroup(
            Line([cx - 2.2, base, 0], [cx + 2.2, base, 0], color=GREY, stroke_width=4),
            *[Line([cx + dx, base, 0], [cx + dx * 1.5, base - 0.35, 0], color=GREY, stroke_width=3) for dx in (-0.6, 0, 0.6)])
        self.trunk = Polygon([cx - 0.5, base, 0], [cx + 0.5, base, 0], [cx + 0.22, top - 1.2, 0], [cx - 0.22, top - 1.2, 0],
                             stroke_color=GREY, stroke_width=3, fill_color=BARK, fill_opacity=0.5)
        self.crown = VGroup(
            Ellipse(width=2.6, height=1.7).move_to([cx - 0.7, 2.5, 0]),
            Ellipse(width=2.8, height=1.8).move_to([cx + 0.6, 2.6, 0]),
            Ellipse(width=2.4, height=1.4).move_to([cx, 2.85, 0])).set_stroke(GREEN, 3).set_fill(LEAF, 0.55)
        self.xyl = Line([cx, base + 0.1, 0], [cx, 2.4, 0], color=BLUE, stroke_width=7).set_opacity(0.55)
        self.all = VGroup(self.ground, self.trunk, self.crown, self.xyl)

    def drops(self, n=7, speed=0.1):
        return flow([[self.cx, self.base + 0.2, 0], [self.cx, 2.3, 0]], n=n, color=BLUE, r=0.1, speed=speed)

    def vapour(self, n=6, speed=0.12):
        c = self.cx
        return flow([[c + 0.3, 3.0, 0], [c + 1.8, 3.4, 0]], n=n, color=GREY, r=0.11, speed=speed, op=0.7)


def heart():
    h = ParametricFunction(lambda t: np.array([16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0]) * 0.07,
                           t_range=[0, TAU]).set_fill(GREY, 0.5).set_stroke(GREY, 4)
    return h


def cross(center, s=0.7, color=YELLOW, w=8):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0]), Line(c + [-s, s, 0], c + [s, -s, 0])).set_stroke(color, w)


def gauge(x, ybot, ytop, yz, level, color=RED, below_color=RED):
    """Vertical gauge: zero line at yz, fill between zero and the tracker's y level."""
    frame = Rectangle(width=0.8, height=ytop - ybot, stroke_color=GREY, stroke_width=3).move_to([x, (ytop + ybot) / 2, 0])
    zero = DashedLine([x - 0.7, yz, 0], [x + 0.7, yz, 0], color=TEXT, stroke_width=3)
    zl = T("0", 26, TEXT).next_to(zero, RIGHT, buff=0.1)

    def mk():
        y = level.get_value()
        h = max(abs(y - yz), 0.001)
        r = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=(below_color if y < yz else color), fill_opacity=0.85)
        r.move_to([x, (y + yz) / 2, 0])
        return r

    fill = always_redraw(mk)
    return VGroup(frame, zero, zl), fill


def scissors(pivot, open_=0.3):
    """Shears with blades pointing LEFT from the pivot. .a and .b are the blades."""
    p = np.array(pivot, float)
    ca, sa = np.cos(open_), np.sin(open_)
    a = Line(p, p + [-1.5 * ca, 1.5 * sa, 0]).set_stroke(TEXT, 9)
    b = Line(p, p + [-1.5 * ca, -1.5 * sa, 0]).set_stroke(TEXT, 9)
    ha = Circle(radius=0.3, color=GREY, stroke_width=6).move_to(p + [1.1, -0.55, 0])
    hb = Circle(radius=0.3, color=GREY, stroke_width=6).move_to(p + [1.1, 0.55, 0])
    ra = Line(p, p + [1.0, -0.4, 0]).set_stroke(GREY, 8)
    rb = Line(p, p + [1.0, 0.4, 0]).set_stroke(GREY, 8)
    g = VGroup(ra, rb, a, b, ha, hb)
    g.a, g.b, g.p = a, b, p
    return g


def lab(text, size=30, color=TEXT):
    return T(text, size, color)


# ---- the water-potential staircase -------------------------------------------------------------
ST_X = [-2.4, 0.0, 2.4, 5.0]
ST_TOP = [2.04, 1.68, 0.6, -3.0]


def plant_cartoon():
    soil = Rectangle(width=2.6, height=0.8, stroke_color=BARK, fill_color=BARK, fill_opacity=0.5).move_to([-5.2, -3.1, 0])
    roots = VGroup(*[Line([-5.2, -2.7, 0], [-5.2 + d, -3.6, 0]) for d in (-0.8, -0.3, 0.4, 0.9)]).set_stroke(GREY, 3)
    stem = Line([-5.2, -2.7, 0], [-5.2, 2.0, 0], color=GREEN, stroke_width=8)
    l1 = Ellipse(width=1.5, height=0.8).rotate(0.5).move_to([-5.9, 1.5, 0])
    l2 = Ellipse(width=1.5, height=0.8).rotate(-0.5).move_to([-4.5, 0.5, 0])
    l3 = Ellipse(width=1.4, height=0.8).rotate(-0.4).move_to([-4.6, 2.2, 0])
    leaves = VGroup(l1, l2, l3).set_stroke(GREEN, 3).set_fill(LEAF, 0.6)
    return VGroup(soil, roots, stem, leaves), soil, roots, leaves


def stairs():
    blocks, labels = [], []
    names = ["soil", "root", "leaf", "air"]
    vals = [MINUS + "0.3", MINUS + "0.6", MINUS + "1.5", "about " + MINUS + "94"]
    for i in range(4):
        top = ST_TOP[i]
        h = top - (-3.5)
        col = GREY if i < 3 else GREY
        b = Rectangle(width=2.4, height=h, stroke_color=BLUE if i < 3 else GREY, stroke_width=3,
                      fill_color=BLUE if i < 3 else GREY, fill_opacity=0.18).move_to([ST_X[i], top - h / 2, 0])
        blocks.append(b)
        if i < 3:
            lb = VGroup(T(names[i], 32, TEXT), M(vals[i], 30, TEXT)).arrange(DOWN, buff=0.12).move_to([ST_X[i], top - 0.7, 0])
        else:
            lb = VGroup(T("air", 32, TEXT), T("(50% humidity)", 24, TEXT), M(vals[i], 28, TEXT)).arrange(DOWN, buff=0.1).move_to([ST_X[i], -1.6, 0])
        labels.append(lb)
    zero = DashedLine([-3.6, 2.4, 0], [6.2, 2.4, 0], color=BLUE, stroke_width=3)
    zl = T("0 = pure water", 24, BLUE).move_to([5.0, 2.75, 0])
    head = T("water potential in MPa (illustrative, not to scale)", 26, TEXT).move_to([1.2, 3.4, 0])
    return blocks, labels, VGroup(zero, zl), head


def step_pt(i, dy=0.22, dx=0.0):
    return np.array([ST_X[i] + dx, ST_TOP[i] + dy, 0])


def stair_stream():
    pts = [[-3.4, 2.26, 0], [-1.2, 2.26, 0], [-1.2, 1.9, 0], [1.2, 1.9, 0], [1.2, 0.82, 0], [3.4, 0.82, 0]]
    return flow(pts, n=7, color=BLUE, r=0.09, speed=0.08)


def sway(mob, amp=0.06, speed=1.2, about=None):
    mob.ts = 0.0
    mob.last = 0.0
    c = about if about is not None else mob.get_bottom()

    def up(m, dt):
        m.ts += dt
        a = amp * np.sin(m.ts * speed)
        m.rotate(a - m.last, about_point=c)
        m.last = a
    mob.add_updater(up)
    return mob


# =================================================================================================
class S00Title(TitleCard):
    LESSON = "Moving Water and Sugar in Plants"
    TITLE = "Pulled From the Top"


class S01Hook(LiveScene):
    def construct(self):
        tr = Tree(-2.5)
        self.play(FadeIn(tr.ground), GrowFromEdge(tr.trunk, DOWN), FadeIn(tr.crown, scale=0.9), run_time=1.0)
        self.at("lifts water")
        self.play(Create(tr.xyl), run_time=1.0)
        dr = tr.drops(8, 0.09)
        self.add(dr)
        sb = DoubleArrow([0.2, -3.3, 0], [0.2, 2.5, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.25)
        sl = T("100 m", 48, TEXT).move_to([1.7, 0.8, 0])
        self.at("100 meters")
        self.play(GrowFromCenter(sb), FadeIn(sl), run_time=1.2)
        self.at("no heart")
        h = heart().move_to([3.2, -2.5, 0])
        x = cross(h.get_center(), 0.9, TEXT, 8)
        hl = T("no pump", 34, TEXT).move_to([3.2, -1.2, 0])
        self.play(FadeIn(h, scale=0.8), run_time=0.5)
        self.play(Create(x), FadeIn(hl), run_time=0.6)
        vp = tr.vapour()
        self.add(vp)
        self.at("where does the force")
        q = T("?", 150, YELLOW, weight=BOLD).move_to([3.0, 2.2, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.play(Indicate(q, color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.finish()


class S02Potential(LiveScene):
    def construct(self):
        # opening: one number
        big = T(PSI, 150, TEXT).move_to([0, 0.6, 0])
        gl, gfill = None, None
        lv_l = ValueTracker(1.2)
        gL, fL = gauge(-5.6, -2.6, 2.4, 1.2, lv_l, color=GOLD, below_color=GOLD)
        self.play(FadeIn(big, scale=0.7), run_time=0.8)
        self.at("one number")
        self.play(FadeIn(gL), run_time=0.8)
        self.at("water potential")
        wp = T("water potential", 44, TEXT).move_to([0, -1.0, 0])
        self.play(FadeIn(wp, shift=UP * 0.2), run_time=0.8)
        self.play(big.animate.scale(1.12), run_time=1.2)
        self.at("pure water at atmospheric")
        self.play(FadeOut(big), FadeOut(wp), run_time=0.5)

        def beaker(cx):
            w, h, cy = 3.0, 2.8, -0.9
            walls = VMobject().set_points_as_corners([[cx - w / 2, cy + h / 2, 0], [cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0]]).set_stroke(TEXT, 5)
            water = Rectangle(width=w - 0.1, height=2.2, stroke_width=0, fill_color=BLUE, fill_opacity=0.45).move_to([cx, cy - h / 2 + 1.13, 0])
            return walls, water

        w1, wa1 = beaker(-3.0)
        d1 = wiggle(VGroup(*[Dot([-3.0 + dx, -1.3 + dy, 0], radius=0.1, color=BLUE) for dx, dy in [(-0.8, 0.2), (0, -0.4), (0.7, 0.3), (-0.3, -0.9), (0.6, -0.8)]]), 0.12, 1.5)
        self.play(Create(w1), FadeIn(wa1), FadeIn(d1), run_time=1.0)
        self.at("is set at zero")
        r1 = VGroup(psi(None, 40), M("= 0 MPa", 34, TEXT)).arrange(RIGHT, buff=0.15).move_to([-3.0, 1.2, 0])
        mk1 = Line([-5.9, 1.2, 0], [-5.3, 1.2, 0], color=GOLD, stroke_width=8)
        self.play(FadeIn(r1), FadeIn(mk1), run_time=0.7)
        self.add(fL)
        self.at("dissolve a solute")
        w2, wa2 = beaker(3.0)
        d2 = wiggle(VGroup(*[Dot([3.0 + dx, -1.3 + dy, 0], radius=0.1, color=BLUE) for dx, dy in [(-0.8, 0.2), (0, -0.4), (0.7, 0.3), (-0.3, -0.9), (0.6, -0.8)]]), 0.12, 1.5)
        self.play(Create(w2), FadeIn(wa2), FadeIn(d2), run_time=0.8)
        sol = VGroup(*[RegularPolygon(6, radius=0.15).set_stroke(GOLD, 2).set_fill(GOLD, 0.9).move_to([3.0 + dx, 2.0 + 0.4 * (i % 2), 0])
                       for i, dx in enumerate([-1.0, -0.6, -0.2, 0.2, 0.6, 1.0, -0.4, 0.4])])
        self.play(FadeIn(sol), run_time=0.3)
        self.play(*[s.animate.move_to([s.get_center()[0], -1.0 - 0.45 * (i % 3), 0]) for i, s in enumerate(sol)], run_time=1.8)
        sol2 = wiggle(VGroup(*[s for s in sol]), 0.1, 1.8)
        lv_r = ValueTracker(1.2)
        gR, fR = gauge(5.6, -2.6, 2.4, 1.2, lv_r, color=GOLD, below_color=GOLD)
        self.add(gR, fR)
        r2 = VGroup(psi(None, 40), M("< 0", 34, TEXT)).arrange(RIGHT, buff=0.15).move_to([3.0, 1.2, 0])
        self.at("drops below zero")
        self.play(lv_r.animate.set_value(-0.4), FadeIn(r2), run_time=1.4)
        self.at("water crossing a membrane")
        mem = DashedLine([0, -2.3, 0], [0, 0.6, 0], color=TEXT, stroke_width=6)
        ml = T("membrane", 30, TEXT).move_to([0, 1.0, 0])
        self.play(Create(mem), FadeIn(ml), run_time=0.8)
        fl = flow([[-1.3, -1.0, 0], [1.3, -1.0, 0]], n=6, color=BLUE, r=0.14, speed=0.2)
        fl2 = flow([[-1.3, -1.7, 0], [1.3, -1.7, 0]], n=5, color=BLUE, r=0.14, speed=0.17)
        self.add(fl, fl2)
        self.at("toward lower")
        ar = Arrow([-1.2, -2.75, 0], [1.2, -2.75, 0], buff=0, color=BLUE, stroke_width=7)
        al = VGroup(T("toward lower", 30, BLUE), psi(None, 34)).arrange(RIGHT, buff=0.15).move_to([0, -3.3, 0])
        self.play(GrowArrow(ar), FadeIn(al), run_time=0.8)
        self.finish()


class S03Ladder(LiveScene):
    def construct(self):
        plant, soil, roots, leaves = plant_cartoon()
        blocks, labels, zero, head = stairs()
        self.at("line up a plant")
        self.play(FadeIn(plant), FadeIn(head), run_time=1.0)
        drop = Dot(step_pt(0), radius=0.2, color=BLUE)
        self.play(FadeIn(zero), run_time=0.5)
        self.at("the soil sits")
        self.play(FadeIn(blocks[0]), FadeIn(labels[0]), Indicate(soil, color=BLUE), FadeIn(drop), run_time=1.0)
        self.at("the root lower")
        self.play(drop.animate.move_to(step_pt(0, 0.22, 1.2)), run_time=0.4)
        self.play(FadeIn(blocks[1]), FadeIn(labels[1]), Indicate(roots, color=BLUE),
                  drop.animate.move_to(step_pt(1)), run_time=0.9)
        self.at("the leaf lower")
        self.play(drop.animate.move_to(step_pt(1, 0.22, 1.2)), run_time=0.4)
        self.play(FadeIn(blocks[2]), FadeIn(labels[2]), Indicate(leaves, color=BLUE),
                  drop.animate.move_to(step_pt(2)), run_time=0.9)
        self.add(stair_stream())
        self.at("the air sits far")
        cl = DashedLine([3.6, 0.6, 0], [3.6, -3.0, 0], color=YELLOW, stroke_width=4)
        self.play(FadeIn(blocks[3]), FadeIn(labels[3]), Create(cl), run_time=1.2)
        self.play(Indicate(labels[3], color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


class S04Cliff(LiveScene):
    def construct(self):
        plant, soil, roots, leaves = plant_cartoon()
        blocks, labels, zero, head = stairs()
        cl = DashedLine([3.6, 0.6, 0], [3.6, -3.0, 0], color=YELLOW, stroke_width=4)
        self.add(plant, head, zero, *blocks, *labels, cl)
        drop = Dot(step_pt(0), radius=0.2, color=BLUE)
        self.add(stair_stream())
        self.at("water runs downhill")
        self.add(drop)
        for i in range(2):
            self.play(drop.animate.move_to(step_pt(i, 0.22, 1.2)), run_time=0.3)
            self.play(drop.animate.move_to(step_pt(i + 1)), run_time=0.45)
        self.at("biggest drop")
        self.play(Indicate(cl, color=YELLOW, scale_factor=1.0), cl.animate.set_stroke(width=10), run_time=1.0)
        self.play(cl.animate.set_stroke(width=4), run_time=0.4)
        self.at("dry air")
        self.play(drop.animate.move_to(step_pt(2, 0.22, 1.2)), run_time=0.3)
        self.play(drop.animate.move_to([4.2, -2.9, 0]), run_time=0.7, rate_func=rush_into)
        puff = Circle(radius=0.3, color=GREY, fill_color=GREY, fill_opacity=0.5).move_to(drop)
        self.play(Transform(drop, puff), run_time=0.4)
        self.play(drop.animate.shift(UP * 0.8).set_opacity(0.3), run_time=1.2)
        self.finish()


class S05Evap(LiveScene):
    def construct(self):
        top = [[x, 0.9, 0] for x in (-4.8, -2.4, 0, 2.4, 4.8)]
        bot = [[x, -1.3, 0] for x in (-3.6, -1.2, 1.2, 3.6)]
        cells = VGroup(*[Ellipse(width=2.1, height=1.9).move_to(p).set_stroke(BLUE, 7).set_fill(LEAF, 0.4) for p in top + bot])
        epi = VGroup(Line([-6.6, 2.3, 0], [3.25, 2.3, 0]), Line([3.95, 2.3, 0], [6.6, 2.3, 0]), Line([-6.6, -2.7, 0], [6.6, -2.7, 0])).set_stroke(GREY, 6)
        self.at("inside a leaf")
        self.play(Create(epi), FadeIn(cells, lag_ratio=0.1), run_time=1.4)
        self.at("water evaporates")
        l1 = T("wet walls", 32, BLUE).move_to([0, -3.3, 0])
        self.play(FadeIn(l1), Indicate(cells, color=BLUE, scale_factor=1.03), run_time=1.0)
        a = flow([[3.6, -0.4, 0], [3.6, 2.3, 0], [3.6, 3.5, 0]], n=6, color=GREY, r=0.12, speed=0.1, op=0.8)
        b = flow([[3.4, 0.9, 0], [3.6, 1.5, 0], [3.6, 2.3, 0], [3.6, 3.5, 0]], n=5, color=GREY, r=0.12, speed=0.09, op=0.8)
        c = flow([[3.8, 0.9, 0], [3.6, 1.5, 0], [3.6, 2.3, 0], [3.6, 3.5, 0]], n=5, color=GREY, r=0.12, speed=0.11, op=0.8)
        self.add(a, b, c)
        self.at("mesophyll cells")
        l2 = T("mesophyll cells", 32, GREEN).move_to([0, -3.3, 0])
        self.play(ReplacementTransform(l1, l2), run_time=0.6)
        self.play(Indicate(cells, color=GREEN, scale_factor=1.04), run_time=1.0)
        self.at("these inner cells")
        l3 = T("photosynthesis", 32, GREEN).move_to([0, -3.3, 0])
        self.play(ReplacementTransform(l2, l3), cells.animate.set_fill(LEAF, 0.65), run_time=1.0)
        self.at("the vapor diffuses")
        l4 = T("drier air", 34, GREY).move_to([-3.2, 3.2, 0])
        ar = Arrow([2.2, 3.2, 0], [-1.0, 3.2, 0], buff=0, color=GREY, stroke_width=5)
        self.play(FadeOut(l3), FadeIn(l4), run_time=0.6)
        self.play(Indicate(a, color=GREY), run_time=1.0)
        self.finish()


class S06Tension(LiveScene):
    def construct(self):
        d = ValueTracker(0.15)
        cx = -2.6
        wl = Rectangle(width=2.6, height=4.2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.35).move_to([-4.9, -1.5, 0])
        wr = Rectangle(width=2.6, height=4.2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.35).move_to([-0.3, -1.5, 0])

        def water():
            pts = [[cx - 1.0, -3.6, 0], [cx + 1.0, -3.6, 0], [cx + 1.0, 0.6, 0]]
            for k in range(21):
                u = 1 - k / 10
                pts.append([cx + u * 1.0, 0.6 - d.get_value() * (1 - u * u), 0])
            m = Polygon(*pts, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.5)
            return m

        wat = always_redraw(water)
        al = T("air", 32, GREY).move_to([-5.0, 2.3, 0])
        self.play(FadeIn(wl), FadeIn(wr), FadeIn(wat), run_time=1.0)
        vp = flow([[cx, 0.5, 0], [cx, 3.4, 0]], n=6, color=GREY, r=0.12, speed=0.09, op=0.75)
        self.add(vp)
        self.play(FadeIn(al), run_time=0.4)
        self.at("the water still held")
        ring = SurroundingRectangle(VGroup(wl, wr), color=BLUE, buff=0.05).set_stroke(width=3)
        pl = T("tiny pore in the wall", 28, TEXT).move_to([2.4, -2.6, 0]).set_opacity(0)
        self.play(d.animate.set_value(0.3), run_time=1.5)
        self.at("held more tightly")
        self.play(d.animate.set_value(0.5), run_time=2.0)
        lv = ValueTracker(1.2)
        frame, fill = gauge(3.9, -3.2, 3.0, 1.2, lv)
        self.at("its pressure")
        self.play(FadeIn(frame), run_time=0.5)
        self.add(fill)
        pp = psi("p", 36).move_to([3.9, 3.4, 0])
        self.play(FadeIn(pp), run_time=0.3)
        self.at("falls below zero")
        self.play(d.animate.set_value(0.75), lv.animate.set_value(-0.6), run_time=1.6)
        self.at("that is tension")
        ar = VGroup(*[Arrow([cx + dx, -0.3, 0], [cx + dx, 0.9, 0], buff=0, color=RED, stroke_width=8, tip_length=0.25) for dx in (-0.5, 0, 0.5)])
        tl = T("tension: a pull", 32, RED).move_to([3.9, -3.55, 0])
        self.play(FadeIn(ar, shift=UP * 0.2), FadeIn(tl), run_time=0.8)
        self.finish()


class S07Straw(LiveScene):
    def construct(self):
        blk = Rectangle(width=3.2, height=1.8, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.4).move_to([0, 0.3, 0])
        self.play(FadeIn(blk), run_time=0.6)
        self.at("stretched")
        out = VGroup(Arrow([1.7, 0.3, 0], [3.5, 0.3, 0], buff=0, color=RED, stroke_width=9),
                     Arrow([-1.7, 0.3, 0], [-3.5, 0.3, 0], buff=0, color=RED, stroke_width=9))
        sl = T("stretched", 44, RED).move_to([0, -1.5, 0])
        self.play(GrowArrow(out[0]), GrowArrow(out[1]), blk.animate.stretch_to_fit_width(4.4), FadeIn(sl), run_time=1.2)
        self.at("not squeezed")
        inn = VGroup(Arrow([-4.8, 2.5, 0], [-2.8, 2.5, 0], buff=0, color=GREY, stroke_width=7),
                     Arrow([4.8, 2.5, 0], [2.8, 2.5, 0], buff=0, color=GREY, stroke_width=7))
        nl = T("not squeezed", 40, GREY).move_to([0, 2.5, 0])
        cx = VGroup(cross([-3.8, 2.5, 0], 0.35, YELLOW, 7), cross([3.8, 2.5, 0], 0.35, YELLOW, 7))
        self.play(FadeIn(inn), FadeIn(nl), run_time=0.8)
        self.play(Create(cx), run_time=0.4)
        self.wait(0.8)
        self.at("picture a sealed syringe")
        self.play(FadeOut(VGroup(out, sl, inn, nl, cx)), FadeOut(blk), run_time=0.6)
        by = 0.3
        barrel = VMobject().set_points_as_corners([[-1.0, by + 1.5, 0], [-5.4, by + 1.5, 0], [-5.4, by - 1.5, 0], [-1.0, by - 1.5, 0]]).set_stroke(TEXT, 6)
        tip = Line([-5.4, by, 0], [-6.4, by, 0]).set_stroke(TEXT, 8)
        px = ValueTracker(-1.0)

        def parts():
            x = px.get_value()
            top = Line([-5.4, by + 1.5, 0], [x + 1.0, by + 1.5, 0]).set_stroke(TEXT, 6)
            bot = Line([-5.4, by - 1.5, 0], [x + 1.0, by - 1.5, 0]).set_stroke(TEXT, 6)
            wat = Rectangle(width=x + 5.4, height=2.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.5).move_to([(x - 5.4) / 2, by, 0])
            head = Rectangle(width=0.35, height=3.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.9).move_to([x + 0.18, by, 0])
            rod = Line([x + 0.35, by, 0], [x + 3.6, by, 0]).set_stroke(GREY, 12)
            plate = Line([x + 3.6, by - 0.9, 0], [x + 3.6, by + 0.9, 0]).set_stroke(GREY, 12)
            return VGroup(wat, top, bot, head, rod, plate)

        sy = always_redraw(parts)
        sym = T("sealed", 30, TEXT).move_to([-3.2, by + 2.2, 0])
        self.play(FadeIn(tip), FadeIn(sy), FadeIn(sym), run_time=1.0)
        molec = wiggle(VGroup(*[Dot([-5.0 + 0.55 * i, by + (0.5 if i % 2 else -0.5), 0], radius=0.09, color=BLUE) for i in range(7)]), 0.1, 1.7)
        self.add(molec)
        self.at("its plunger pulled")
        self.play(px.animate.set_value(0.6), run_time=2.0)
        self.at("if no bubble")
        nb = T("no bubble", 36, TEXT).move_to([-2.0, by - 2.3, 0])
        self.play(FadeIn(nb), run_time=0.5)
        self.at("the water pulls")
        pa = VGroup(Arrow([0.8, by + 1.8, 0], [-0.3, by + 1.8, 0], buff=0, color=RED, stroke_width=9),
                    Arrow([0.8, by - 1.8, 0], [-0.3, by - 1.8, 0], buff=0, color=RED, stroke_width=9),
                    Arrow([1.6, by, 0], [0.4, by, 0], buff=0, color=RED, stroke_width=9))
        pl = T("water pulls the plunger", 32, RED).move_to([2.6, by + 2.4, 0])
        self.play(FadeIn(pa, shift=LEFT * 0.2), FadeIn(pl), run_time=0.8)
        note = T("a model of tension, not of flow", 26, TEXT).move_to([2.2, -3.4, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


class S08Cohesion(LiveScene):
    def construct(self):
        cx = -2.0
        rows = 16
        cols = [-0.5, 0.0, 0.5]
        base = [(cx + c + (0.22 if k % 2 else -0.0), 2.8 - 0.5 * k) for k in range(rows) for c in cols]
        sh = ValueTracker(0.0)
        show_links = ValueTracker(0.0)
        tube = VMobject().set_points_as_corners([[cx - 0.95, 3.7, 0], [cx - 0.95, -3.7, 0]]).set_stroke(GREY, 5)
        tube2 = VMobject().set_points_as_corners([[cx + 0.95, 3.7, 0], [cx + 0.95, -3.7, 0]]).set_stroke(GREY, 5)
        mols = VGroup(*[Dot([x, y, 0], radius=0.17, color=BLUE) for x, y in base])
        pairs = []
        for k in range(rows):
            for j in range(3):
                i = k * 3 + j
                if j < 2:
                    pairs.append((i, i + 1))
                if k < rows - 1:
                    pairs.append((i, i + 3))
        links = VGroup(*[DashedLine([0, 0, 0], [0.5, 0, 0], color=TEXT, stroke_width=3, dash_length=0.08) for _ in pairs])
        clock = [0.0]

        def up(m, dt):
            clock[0] += dt
            t = clock[0]
            for i, d in enumerate(mols):
                x, y = base[i]
                y = y + sh.get_value() + 0.04 * np.sin(t * 2 + i)
                x = x + 0.04 * np.cos(t * 1.7 + i * 1.3)
                d.move_to([x, y, 0])
                vis = 1.0 if -3.45 <= y <= 3.45 else 0.0
                d.set_opacity(vis)
            for n, (a, b) in enumerate(pairs):
                pa, pb = mols[a].get_center(), mols[b].get_center()
                ln = links[n]
                ln.put_start_and_end_on(pa, pb)
                on = 1.0 if np.sin(t * 2.5 + n * 1.9) > -0.3 else 0.15
                vis = min(mols[a].get_fill_opacity(), mols[b].get_fill_opacity())
                ln.set_stroke(opacity=on * vis * show_links.get_value())

        grp = VGroup(mols, links)
        grp.add_updater(up)
        up(grp, 0)
        self.play(FadeIn(tube), FadeIn(tube2), run_time=0.6)
        self.add(grp)
        pull = Arrow([-4.4, -0.5, 0], [-4.4, 3.0, 0], buff=0, color=RED, stroke_width=10)
        pl = T("pull", 36, RED).move_to([-4.4, -1.1, 0])
        self.at("pull not just snap")
        self.play(GrowArrow(pull), FadeIn(pl), run_time=0.8)
        self.at("water molecules cling")
        self.play(show_links.animate.set_value(1.0), run_time=1.2)
        self.at("hydrogen bonds")
        hb = T("hydrogen bonds", 36, TEXT).move_to([3.7, 0.6, 0])
        hba = Arrow([1.4, 0.6, 0], [cx + 0.7, 0.6, 0], buff=0.05, color=TEXT, stroke_width=5)
        self.play(FadeIn(hb), GrowArrow(hba), run_time=0.8)
        self.at("this cohesion")
        co = T("cohesion", 44, BLUE).move_to([3.4, -1.0, 0])
        self.play(FadeIn(co), run_time=0.6)
        self.at("pulled like a rope")
        self.play(sh.animate.set_value(0.9), run_time=2.8, rate_func=linear)
        self.finish()


class S09Xylem(LiveScene):
    def construct(self):
        tracheids, vessels, blobs = VGroup(), VGroup(), VGroup()
        for k, x in enumerate([-4.65, -3.75, -2.85, -1.95]):
            cuts = [-3.0 + 2.0 * (1 + (k % 3) * 0.3), 1.0 + 0.3 * (k % 3)]
            outline = Rectangle(width=0.7, height=6.0, stroke_color=BLUE, stroke_width=3).move_to([x, 0, 0])
            tracheids.add(outline)
            for c in [-1.0 + 0.4 * k, 1.4 - 0.3 * k]:
                tracheids.add(Line([x - 0.35, c, 0], [x + 0.35, c, 0]).set_stroke(BLUE, 3))
            for c in [-2.2 + 0.4 * k, 0.2 + 0.3 * k, 2.2 - 0.3 * k]:
                blobs.add(Ellipse(width=0.35, height=0.5).move_to([x, c, 0]).set_fill(LEAF, 0.8).set_stroke(GREEN, 2))
        for k, x in enumerate([1.6, 3.8]):
            vessels.add(Rectangle(width=1.5, height=6.0, stroke_color=BLUE, stroke_width=3).move_to([x, 0, 0]))
            for c in (-1.0, 1.0):
                vessels.add(Line([x - 0.75, c, 0], [x - 0.3, c, 0]).set_stroke(BLUE, 4), Line([x + 0.3, c, 0], [x + 0.75, c, 0]).set_stroke(BLUE, 4))
            for c in (-2.2, 0.0, 2.2):
                blobs.add(Ellipse(width=0.6, height=0.7).move_to([x, c, 0]).set_fill(LEAF, 0.8).set_stroke(GREEN, 2))
        self.play(FadeIn(tracheids), FadeIn(vessels), FadeIn(blobs), run_time=1.2)
        self.at("tracheids")
        t1 = T("tracheids", 34, TEXT).move_to([-3.3, 3.45, 0])
        self.play(FadeIn(t1), Indicate(tracheids, color=BLUE, scale_factor=1.02), run_time=0.9)
        self.at("vessel elements")
        t2 = T("vessel elements", 34, TEXT).move_to([2.7, 3.45, 0])
        self.play(FadeIn(t2), Indicate(vessels, color=BLUE, scale_factor=1.02), run_time=0.9)
        self.at("they are dead")
        dl = T("dead when working", 34, YELLOW).move_to([4.6, -3.45, 0])
        self.play(FadeIn(dl), run_time=0.6)
        self.at("contents gone")
        self.play(FadeOut(blobs, scale=0.3), run_time=1.0)
        self.at("they leave a hollow")
        hl = T("hollow pathway", 34, BLUE).move_to([-3.0, -3.45, 0])
        self.play(FadeIn(hl), FadeOut(dl), run_time=0.6)
        fills = VGroup(*[Rectangle(width=0.5, height=5.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.4).move_to([x, 0, 0]) for x in (-4.65, -3.75, -2.85, -1.95)],
                       *[Rectangle(width=1.4, height=5.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.4).move_to([x, 0, 0]) for x in (1.6, 3.8)])
        self.play(*[GrowFromEdge(f, DOWN) for f in fills], run_time=2.4)
        fl = [flow([[x, -2.8, 0], [x, 2.8, 0]], n=4, color=BLUE, r=0.1, speed=0.12) for x in (-4.65, -3.75, -2.85, -1.95, 1.6, 3.8)]
        self.add(*fl)
        up_a = Arrow([6.0, -2.4, 0], [6.0, 2.4, 0], buff=0, color=BLUE, stroke_width=8)
        lf = T("leaf", 30, TEXT).move_to([6.0, 3.0, 0])
        rt = T("root", 30, TEXT).move_to([6.0, -3.0, 0])
        self.play(FadeIn(up_a), FadeIn(lf), FadeIn(rt), run_time=0.8)
        self.finish()


class S10Dixon(LiveScene):
    def construct(self):
        tr = Tree(-3.8)
        self.add(tr.all)
        dr = tr.drops(7, 0.08)
        self.add(dr)
        cap = chip("Dixon and Joly, 1890s", TEXT, 34).move_to([2.2, 3.0, 0])
        self.at("henry dixon")
        self.play(FadeIn(cap, shift=DOWN * 0.2), run_time=0.8)
        sub = T("cohesion-tension", 34, TEXT).move_to([2.2, 2.0, 0])
        self.at("proposed this")
        self.play(FadeIn(sub), run_time=0.7)
        # icons
        vi = VGroup(*[Circle(radius=r, color=GREY, fill_color=GREY, fill_opacity=0.5).move_to(p) for r, p in [(0.2, [0.4, 0.8, 0]), (0.28, [0.8, 1.0, 0]), (0.2, [0.7, 0.6, 0])]]).move_to([0.8, 0.8, 0])
        ci = VGroup(Rectangle(width=0.5, height=1.1, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.5)).move_to([0.8, -0.5, 0])
        lvl = ValueTracker(-0.5)
        gi_frame = Rectangle(width=0.5, height=1.2, stroke_color=GREY, stroke_width=3).move_to([0.8, -1.9, 0])
        gi_fill = Rectangle(width=0.5, height=0.7, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to([0.8, -2.15, 0])
        zl = Line([0.45, -1.65, 0], [1.15, -1.65, 0]).set_stroke(TEXT, 3)
        self.at("evaporation pulls")
        t1 = lab("evaporation pulls", 32).move_to([4.0, 0.8, 0])
        vp = tr.vapour(8, 0.15)
        self.add(vp)
        self.play(FadeIn(vi), FadeIn(t1), Indicate(tr.crown, color=GREY, scale_factor=1.05), run_time=1.0)
        self.at("cohesion passes")
        t2 = lab("cohesion passes it down", 30).move_to([4.0, -0.5, 0])
        self.play(FadeIn(ci), FadeIn(t2), Indicate(tr.xyl, color=BLUE, scale_factor=1.6), run_time=1.0)
        self.at("the column stays")
        t3 = lab("column stays under tension", 30).move_to([4.0, -1.9, 0])
        self.play(FadeIn(gi_frame), FadeIn(zl), FadeIn(gi_fill), FadeIn(t3), run_time=1.0)
        self.play(Indicate(gi_fill, color=RED, scale_factor=1.15), run_time=1.0)
        self.finish()


class S11Gravity(LiveScene):
    def construct(self):
        tr = Tree(-4.4)
        self.add(tr.all)
        dr = tr.drops(7, 0.04)
        self.add(dr)
        h = ValueTracker(0.0)
        bx, yb, yt = -2.4, -3.3, 2.4
        frame = Rectangle(width=0.7, height=yt - yb, stroke_color=GREY, stroke_width=3).move_to([bx, (yt + yb) / 2, 0])
        fill = always_redraw(lambda: Rectangle(width=0.7, height=max(h.get_value() * (yt - yb), 0.001), stroke_width=0, fill_color=RED, fill_opacity=0.85).move_to([bx, yb + h.get_value() * (yt - yb) / 2, 0]))
        m0 = M("0 m", 26, TEXT).move_to([bx + 1.0, yb, 0])
        m1 = M("110 m", 26, TEXT).move_to([bx + 1.15, yt, 0])
        self.at("height adds a cost")
        self.play(FadeIn(frame), FadeIn(m0), FadeIn(m1), run_time=0.8)
        self.add(fill)
        mc = always_redraw(lambda: M(f"{h.get_value() * 110:.0f} m", 40, TEXT).move_to([3.0, 1.0, 0]))
        pc = always_redraw(lambda: M(f"{h.get_value() * 110 * 0.01:.2f} MPa", 40, RED).move_to([3.0, -0.2, 0]))
        self.add(mc, pc)
        per = T("about 0.01 MPa per m", 32, TEXT).move_to([3.0, 2.3, 0])
        self.at("each meter takes")
        self.play(FadeIn(per), h.animate.set_value(0.09), run_time=2.0)
        self.at("just to hold")
        sl = T("just to hold a still column", 30, TEXT).move_to([3.0, -1.4, 0])
        self.play(FadeIn(sl), run_time=0.6)
        self.at("at the top")
        self.play(FadeOut(sl), h.animate.set_value(1.0), run_time=4.5, rate_func=linear)
        self.at("gravity alone")
        fin = T("over 1 MPa", 44, RED).move_to([3.0, -1.5, 0])
        bf = T("before any flow", 32, TEXT).move_to([3.0, -2.6, 0])
        self.play(FadeIn(fin, scale=1.2), FadeIn(bf), run_time=0.8)
        self.finish()


def question_scene(scene, with_shears=True, cx=-3.5):
    tr = Tree(cx)
    scene.add(tr.all)
    return tr


class S12Predict(LiveScene):
    def construct(self):
        cx = -3.5
        tr = Tree(cx)
        self.add(tr.all)
        self.add(tr.drops(7, 0.1))
        self.at("roots can push")
        ar = Arrow([cx - 1.0, -3.0, 0], [cx - 1.0, -1.6, 0], buff=0, color=AMBER, stroke_width=9)
        al = T("push", 32, AMBER).move_to([cx - 1.9, -2.3, 0])
        self.play(GrowArrow(ar), FadeIn(al), run_time=0.8)
        self.at("if xylem water")
        self.play(ar.animate.shift(UP * 0.5), run_time=1.2)
        self.play(ar.animate.shift(DOWN * 0.5), run_time=1.0)
        sh = scissors([cx + 3.0, 0.3, 0])
        self.at("what would happen")
        q = chip("Pushed? What happens at the cut?", TEXT, 34).move_to([2.6, 2.6, 0])
        fit(q, 7.5)
        self.play(FadeIn(sh), FadeIn(q), run_time=0.6)
        self.play(sh.animate.shift(LEFT * 1.8), run_time=1.5)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        cx = -3.5
        tr = Tree(cx)
        self.add(tr.all)
        self.add(tr.drops(7, 0.1))
        sh = scissors([cx + 1.2, 0.3, 0])
        q = chip("Pushed? What happens at the cut?", TEXT, 34).move_to([2.6, 2.6, 0])
        fit(q, 7.5)
        ar = Arrow([cx - 1.0, -3.0, 0], [cx - 1.0, -1.6, 0], buff=0, color=AMBER, stroke_width=9)
        al = T("push", 32, AMBER).move_to([cx - 1.9, -2.3, 0])
        self.add(sh, q, ar, al)
        tmr = ValueTracker(0.0)
        base = Circle(radius=0.5, color=GREY, stroke_width=6).move_to([5.8, -3.0, 0])
        arc = always_redraw(lambda: Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * max(tmr.get_value(), 0.001), color=YELLOW, stroke_width=8).move_to([5.8, -3.0, 0]) if False else
                            Arc(radius=0.5, start_angle=PI / 2, angle=-TAU * max(tmr.get_value(), 0.001), color=YELLOW, stroke_width=8, arc_center=[5.8, -3.0, 0]))
        self.add(base, arc)
        self.play(tmr.animate.set_value(1.0), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


class S14Reveal(LiveScene):
    def construct(self):
        tx = -3.6
        tube = VGroup(Line([tx - 0.8, -3.6, 0], [tx - 0.8, 3.6, 0]), Line([tx + 0.8, -3.6, 0], [tx + 0.8, 3.6, 0])).set_stroke(BLUE, 5)
        wat = Rectangle(width=1.5, height=3.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.45).move_to([tx, -1.65, 0])
        up_part = Rectangle(width=1.5, height=3.3, stroke_width=0, fill_color=BLUE, fill_opacity=0.45).move_to([tx, 1.95, 0])
        self.add(tube, wat, up_part)
        fl = flow([[tx, -3.4, 0], [tx, 0.1, 0]], n=5, color=BLUE, r=0.12, speed=0.1)
        self.add(fl)
        sh = scissors([tx + 2.6, 0.3, 0], 0.4)
        self.play(FadeIn(sh), run_time=0.4)
        self.play(sh.animate.shift(LEFT * 1.6), run_time=0.8)
        self.play(Rotate(sh.a, -0.38, about_point=sh.p + LEFT * 1.6), Rotate(sh.b, 0.38, about_point=sh.p + LEFT * 1.6), run_time=0.3)
        self.play(up_part.animate.shift(UP * 0.8).set_opacity(0), FadeOut(sh), run_time=0.7)
        self.at("pushed water would")
        arcs = VGroup(*[DashedVMobject(ArcBetweenPoints([tx + dx * 0.15, 0.4, 0], [tx + dx, 0.2, 0], angle=-1.9)).set_stroke(BLUE, 5).set_opacity(0.7) for dx in (0.9, 1.7, 2.5, -0.9, -1.7)])
        self.play(FadeIn(arcs), run_time=0.8)
        self.at("it does not")
        x = cross([tx + 1.7, 1.4, 0], 1.3, YELLOW, 10)
        self.play(Create(x), run_time=0.5)
        self.at("cut the xylem")
        self.play(FadeOut(arcs), FadeOut(x), run_time=0.5)
        vp = flow([[tx, 0.0, 0], [tx, 0.0, 0]], n=1)
        tl = T("transpiring tree: water pulled up", 28, GREY).move_to([0.8, 2.8, 0]) if False else None
        self.wait(1.0)
        self.at("air is drawn")
        bub = flow([[tx, 0.7, 0], [tx, -1.8, 0]], n=5, color=GREY, r=0.2, speed=0.2, op=0.9)
        newwat = Rectangle(width=1.5, height=3.4, stroke_width=0, fill_color=BLUE, fill_opacity=0.45).move_to([tx, -1.9, 0])
        self.add(bub)
        self.play(Transform(wat, newwat), run_time=1.2)
        al = T("air drawn in", 36, GREY).move_to([1.0, -0.3, 0])
        aa = Arrow([-0.8, -0.3, 0], [-2.6, -0.3, 0], buff=0, color=GREY, stroke_width=5)
        self.play(FadeIn(al), GrowArrow(aa), run_time=0.6)
        self.at("the water was under")
        lv = ValueTracker(-0.8)
        frame, fill = gauge(4.3, -3.2, 3.0, 1.2, lv)
        self.add(frame, fill)
        pp = psi("p", 36).move_to([4.3, 3.4, 0])
        ul = T("under tension", 32, RED).move_to([4.3, -3.55, 0])
        self.play(FadeIn(frame), FadeIn(pp), FadeIn(ul), run_time=0.8)
        self.play(Indicate(fill, color=RED, scale_factor=1.05), run_time=1.0)
        self.finish()


class S15Rule(LiveScene):
    def construct(self):
        cx = -2.6
        tr = Tree(cx)
        self.add(tr.all)
        dr = tr.drops(8, 0.06)
        self.add(dr)
        self.at("so the force comes")
        vp = tr.vapour(8, 0.15)
        self.add(vp)
        ft = T("from the top", 40, TEXT).move_to([4.4, 3.2, 0])
        self.play(FadeIn(ft), run_time=0.7)
        self.at("evaporation lowers")
        lv = ValueTracker(1.2)
        frame, fill = gauge(1.0, 0.0, 3.2, 1.2, lv)
        pl = T("lowest pressure", 30, RED).move_to([3.9, 1.7, 0])
        self.play(FadeIn(frame), run_time=0.4)
        self.add(fill)
        self.play(lv.animate.set_value(0.3), FadeIn(pl), run_time=1.2)
        # corner staircase, pulses once
        st = VGroup(*[Rectangle(width=0.5, height=h, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.25).move_to([4.5 + 0.55 * i, -3.4 + h / 2, 0])
                      for i, h in enumerate([1.1, 1.0, 0.6, 0.1])])
        self.play(FadeIn(st), run_time=0.4)
        self.play(Indicate(st, color=BLUE, scale_factor=1.2), run_time=0.8)
        self.at("the water column below")
        ua = Arrow([cx + 1.1, -2.6, 0], [cx + 1.1, 1.8, 0], buff=0, color=BLUE, stroke_width=10)
        ul = T("pulled up", 36, BLUE).move_to([1.3, -1.0, 0]) if False else T("pulled up", 36, BLUE).next_to(ua, RIGHT, buff=0.2)
        self.play(GrowArrow(ua), FadeIn(ul), run_time=1.5)
        self.finish()


class S16Close(LiveScene):
    def construct(self):
        cx = -4.2
        tr = Tree(cx)
        self.add(tr.all)
        self.add(tr.drops(8, 0.05))
        self.at("water leaves for")
        # a staircase of three blocks and the dry-air floor
        blocks = VGroup(*[Rectangle(width=1.1, height=h, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.25).move_to([0.2 + 1.2 * i, -3.0 + h / 2, 0])
                          for i, h in enumerate([5.0, 4.4, 3.2])], Rectangle(width=1.4, height=0.2, stroke_color=GREY, fill_color=GREY, fill_opacity=0.4).move_to([4.2, -2.9, 0]))
        drop = Dot([0.2, 2.2, 0], radius=0.18, color=BLUE)
        self.play(FadeIn(blocks), FadeIn(drop), run_time=0.8)
        self.play(drop.animate.move_to([1.4, 1.6, 0]), run_time=0.6)
        self.play(drop.animate.move_to([2.6, 0.6, 0]), run_time=0.6)
        self.at("the dry air")
        al = T("dry air: lowest", 34, GREY).move_to([5.0, -1.6, 0])
        self.play(FadeIn(al), drop.animate.move_to([4.2, -2.5, 0]), run_time=1.0)
        self.at("so the xylem")
        self.play(FadeOut(blocks), FadeOut(drop), FadeOut(al), run_time=0.7)
        w1 = T("pulled,", 80, RED, weight=BOLD).move_to([2.8, 1.0, 0])
        w2 = T("not pushed", 70, TEXT, weight=BOLD).move_to([2.8, -0.8, 0])
        self.play(FadeIn(w1, scale=1.1), run_time=0.7)
        self.at("not pushed")
        self.play(FadeIn(w2, scale=1.1), run_time=0.7)
        self.finish()


class S17End(EndCard):
    LINE = "Evaporation lowers the pressure at the top, so xylem water is pulled."
