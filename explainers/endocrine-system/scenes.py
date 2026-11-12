"""Tap, Drain and a Sensor: how a hormone's level is set (Biochemistrypedia explainer, endocrine system)

COLOUR MAP (one colour per concept, whole film)
  ORANGE = secretion (the gland tap, hormone dots)
  TEAL   = hormone level (water line in the plasma tank)
  GREY   = clearance (the drain: all removal and breakdown)
  RED    = negative feedback (dashed arrow from the level back to the tap)
  animals = charcoal-grey silhouettes
Everything that moves is computed: the tank obeys dL/dt = r (a - k L); the feedback loop uses
a = base / (1 + (L/K)^3) (a schematic Hill-type brake); the daily trace is the tank's own response.
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F28C28"
BIRDC = "#7C8591"
COMBC = "#B9C2CC"
VESS = "#B0524A"
CELLC = "#6EA8FE"
NERVEC = GOLD
LESSON_TITLE = "Hormones and the Endocrine System"


def v3(p):
    p = np.array(p, float)
    return np.array([p[0], p[1], 0.0])


def clip(x, a, b):
    return max(a, min(b, x))


def gate(L, K=0.55):
    return 1.0 / (1.0 + (L / K) ** 3)


def P3(x, y, z=0.0):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ moving dots along a path
class Flow(VGroup):
    """Dots streaming along a polyline; .amount sets how many/how big (0 = off)."""

    def __init__(self, pts, color=ORANGE, spacing=0.42, speed=1.5, r=0.11):
        super().__init__()
        self.pts = [v3(p) for p in pts]
        self.color, self.sp, self.speed, self.r = color, spacing, speed, r
        self.amount, self.phase = 0.0, 0.0
        self.add_updater(lambda m, dt: m._step(dt))

    def _step(self, dt):
        self.phase += dt * self.speed
        P = self.pts
        seg = [float(np.linalg.norm(P[i + 1] - P[i])) for i in range(len(P) - 1)]
        tot = sum(seg)
        if self.amount < 0.03 or tot < 0.05:
            self.submobjects = []
            return
        n = int(tot / self.sp) + 1
        rad = 0.04 + (self.r - 0.04) * clip(self.amount, 0, 1.3)
        dots = []
        for i in range(n):
            s = (self.phase + i * self.sp) % (n * self.sp)
            if s > tot:
                continue
            acc = 0.0
            p = P[-1]
            for j, l in enumerate(seg):
                if s <= acc + l:
                    p = P[j] + (P[j + 1] - P[j]) * ((s - acc) / max(l, 1e-6))
                    break
                acc += l
            dots.append(Dot(p, radius=rad, color=self.color))
        self.submobjects = dots


def polyline(pts, color, width, opacity=1.0):
    m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity, fill_opacity=0)
    m.set_points_as_corners([v3(p) for p in pts])
    return m


def dpath(pts, color=RED, width=6, tee=True):
    """Dashed polyline with an inhibition bar at the end."""
    g = VGroup()
    for a, b in zip(pts[:-1], pts[1:]):
        g.add(DashedLine(P3(*a), P3(*b), dash_length=0.2, dashed_ratio=0.55, stroke_width=width, color=color))
    if tee:
        a, b = v3(pts[-2])[:2], v3(pts[-1])[:2]
        d = (b - a) / np.linalg.norm(b - a)
        perp = np.array([-d[1], d[0]])
        g.add(Line(P3(*(b + perp * 0.3)), P3(*(b - perp * 0.3)), stroke_width=width + 2, color=color))
    return g


# ------------------------------------------------------------------ the plasma tank
class Tank:
    """Blood as a tank. dL/dt = r (a - k L) + inj; a = adr * base * (1 - f + f gate(L)).
    All the pictures (water, stream thickness, arrow lengths, tap handle) read these numbers."""

    def __init__(s, sc, cx=0.5, cy=-0.2, w=3.2, h=4.0, pipe=None, arrows=True, handle=True,
                 L=0.0, base=0.0, f=0.0, adr=1.0, k=1.0, r=0.3):
        s.sc, s.cx, s.cy, s.w, s.h, s.r = sc, cx, cy, w, h, r
        s.top, s.bot, s.l, s.rt = cy + h / 2, cy - h / 2, cx - w / 2, cx + w / 2
        s.Lt, s.base, s.f, s.adr, s.k, s.inj = (ValueTracker(v) for v in (L, base, f, adr, k, 0.0))
        s.run, s.t, s.a, s.D = True, 0.0, 0.0, 0.0
        s.dashed, s.show_in, s.show_out, s.handle_on = False, False, False, handle
        s.nx, s.ny = cx - 0.6, s.top + 0.35
        s.pipe = pipe or [(cx - 3.4, s.ny), (s.nx, s.ny)]
        gap = 0.27
        fr = VMobject(stroke_color=TEXT, stroke_width=6, fill_opacity=0)
        fr.set_points_as_corners([P3(s.l, s.top), P3(s.l, s.bot), P3(cx - gap, s.bot)])
        fr.start_new_path(P3(cx + gap, s.bot))
        fr.add_points_as_corners([P3(s.rt, s.bot), P3(s.rt, s.top)])
        s.frame = fr
        s.stub = VGroup(Line(P3(cx - gap, s.bot), P3(cx - gap, s.bot - 0.4), stroke_width=6, color=GREY),
                        Line(P3(cx + gap, s.bot), P3(cx + gap, s.bot - 0.4), stroke_width=6, color=GREY))
        body = polyline(list(s.pipe) + [(s.nx, s.ny - 0.28)], ORANGE, 16, 0.45)
        s.tap = VGroup(body)
        s.water = Polygon(P3(0, 0), P3(1, 0), P3(1, 1), color=TEAL, fill_color=TEAL, fill_opacity=0.5, stroke_width=0)
        s.surf = VMobject(stroke_color=TEAL, stroke_width=7, fill_opacity=0)
        s.arr = VGroup()
        s.lever = VGroup()
        s.live = VGroup(s.water, s.surf, s.arr, s.lever)
        s.tapflow = Flow(list(s.pipe) + [(s.nx, s.bot + 1)], ORANGE)
        s.drainflow = Flow([(cx, s.bot - 0.4), (cx, s.bot - 0.95)], GREY, spacing=0.34)
        s.live.add_updater(lambda m, dt: s.step(dt))
        s.step(0.0)

    def parts(s):
        return [s.live, s.tapflow, s.drainflow]

    def surf_y(s):
        return s.bot + 0.06 + clip(s.Lt.get_value(), 0, 1) * (s.h - 0.12)

    def step(s, dt):
        L, k = s.Lt.get_value(), s.k.get_value()
        base, f = s.base.get_value(), s.f.get_value()
        s.D = base * (1 - f + f * gate(L))
        s.a = s.adr.get_value() * s.D
        if s.run and dt > 0:
            L = clip(L + (s.r * (s.a - k * L) + s.inj.get_value()) * dt, 0, 1)
            s.Lt.set_value(L)
        s.t += dt
        sy = s.surf_y()
        H = sy - (s.bot + 0.06)
        x0, x1 = s.l + 0.06, s.rt - 0.06
        if H > 0.02:
            s.water.set_points_as_corners([P3(x0, s.bot + 0.06), P3(x1, s.bot + 0.06), P3(x1, sy), P3(x0, sy), P3(x0, s.bot + 0.06)])
            xs = np.linspace(x0, x1, 26)
            wave = [P3(x, sy + 0.035 * math.sin(3.2 * x + 2.5 * s.t)) for x in xs]
            s.water.set_fill(TEAL, 0.5)
            s.surf.clear_points()
            if s.dashed:
                for i in range(0, 25, 2):
                    s.surf.start_new_path(wave[i])
                    s.surf.add_points_as_corners(wave[i + 1:i + 2])
            else:
                s.surf.set_points_as_corners(wave)
        else:
            s.water.set_fill(TEAL, 0)
            s.surf.clear_points()
        s.tapflow.pts = [v3(p) for p in list(s.pipe) + [(s.nx, max(sy, s.bot + 0.1))]]
        s.tapflow.amount = s.a / 0.9
        s.drainflow.amount = k * L / 0.9
        # arrows (in / out) and the tap handle
        s.arr.submobjects = []
        if s.show_in and s.a * 2.6 > 0.12:
            s.arr.add(Arrow(P3(s.rt + 0.15 + 2.6 * s.a, s.cy + 0.9), P3(s.rt + 0.15, s.cy + 0.9), buff=0, color=ORANGE, stroke_width=9, tip_length=0.3))
        if s.show_out and k * L * 2.6 > 0.12:
            s.arr.add(Arrow(P3(s.rt + 0.15, s.cy - 0.9), P3(s.rt + 0.15 + 2.6 * k * L, s.cy - 0.9), buff=0, color=GREY, stroke_width=9, tip_length=0.3))
        s.lever.submobjects = []
        if s.handle_on:
            op = clip(s.a / 0.9, 0, 1)
            th = (math.pi / 2) * (1 - op)
            px, py = s.cx - 1.9, s.ny
            s.lever.add(Line(P3(px, py), P3(px + 0.7 * math.cos(th), py + 0.7 * math.sin(th)), stroke_width=11, color=TEXT),
                        Dot(P3(px, py), radius=0.14, color=TEXT))


# ------------------------------------------------------------------ cockerel silhouette
class Bird(VGroup):
    def __init__(s, h=3.4, comb=1.0):
        super().__init__()
        s.sc = h / 3.2
        k = s.sc
        col = BIRDC

        def f(m):
            return m.set_fill(col, 1).set_stroke(width=0)
        body = f(Ellipse(width=2.1 * k, height=1.35 * k))
        neck = f(Polygon(P3(0.4 * k, 0.2 * k), P3(1.2 * k, 0.25 * k), P3(1.0 * k, 1.0 * k), P3(0.55 * k, 0.95 * k)))
        head = f(Circle(radius=0.34 * k).move_to(P3(1.0 * k, 1.08 * k)))
        beak = f(Polygon(P3(1.28 * k, 1.16 * k), P3(1.72 * k, 1.02 * k), P3(1.28 * k, 0.94 * k)))
        wattle = Circle(radius=0.1 * k).move_to(P3(1.18 * k, 0.72 * k)).set_fill(COMBC, 1).set_stroke(width=0)
        eye = Dot(P3(1.1 * k, 1.15 * k), radius=0.05 * k, color=BG)
        tail = VGroup(*[f(Ellipse(width=1.5 * k, height=0.36 * k).rotate(a).move_to(P3(cx * k, cy * k)))
                        for a, cx, cy in [(0.6, -1.35, 0.7), (1.0, -1.28, 0.9), (1.35, -1.12, 1.0)]])
        legs = VGroup(Line(P3(-0.1 * k, -0.6 * k), P3(-0.15 * k, -1.45 * k)), Line(P3(0.35 * k, -0.6 * k), P3(0.4 * k, -1.45 * k)),
                      Line(P3(-0.15 * k, -1.45 * k), P3(0.15 * k, -1.45 * k)), Line(P3(0.4 * k, -1.45 * k), P3(0.7 * k, -1.45 * k))).set_stroke(col, 9)
        s.body, s.head = body, head
        s.cs = ValueTracker(comb)
        s.comb = Polygon(*[P3(0, 0), P3(1, 0), P3(1, 1)], color=COMBC, fill_color=COMBC, fill_opacity=1, stroke_width=0)
        s.add(tail, legs, body, neck, head, beak, wattle, eye, s.comb)
        s.add_updater(lambda m, dt: m._comb())
        s._comb()

    def _comb(s):
        c, k, v = s.head.get_center(), s.sc, clip(s.cs.get_value(), 0.05, 1.2)
        base = [(-0.22, 0.27), (-0.12, 0.31), (0.0, 0.33), (0.12, 0.31), (0.22, 0.27)]
        pts = [P3(c[0] + x * k, c[1] + y * k) for x, y in base]
        up = [P3(c[0] + (-0.18) * k, c[1] + (0.3 + 0.30 * v) * k), P3(c[0] + (-0.06) * k, c[1] + (0.32 + 0.12 * v) * k),
              P3(c[0] + 0.04 * k, c[1] + (0.33 + 0.36 * v) * k), P3(c[0] + 0.14 * k, c[1] + (0.31 + 0.14 * v) * k)]
        outline = [pts[0], up[0], pts[1], up[1], pts[2], up[2], pts[3], up[3], pts[4], pts[0]]
        s.comb.set_points_as_corners(outline)

    def belly(s):
        return s.body.get_center()

    def start_sway(s, amp=0.05, ph=0.0):
        s.b0 = s.body.get_center().copy()
        s.tt = 0.0

        def sway(m, dt):
            m.tt += dt
            want = m.b0 + P3(0, amp * math.sin(2.2 * m.tt + ph))
            m.shift(want - m.body.get_center())
        s.add_updater(sway)


def bubble(text, at, size=30):
    t = T(text, size, TEXT)
    box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.5, height=t.height + 0.4, stroke_color=TEXT, stroke_width=3,
                           fill_color=BG, fill_opacity=1).move_to(at)
    return VGroup(box, t.move_to(box))


def lab(text, pos, color=TEXT, size=30):
    return T(text, size, color).move_to(P3(*pos))


# ================================================================== scenes
class S00Title(TitleCard):
    TITLE = "Tap, Drain and a Sensor"
    LESSON = LESSON_TITLE


class S01Hook(SpokenScene):
    def construct(self):
        bird = Bird(4.2).move_to(P3(-2.6, -0.4))
        bird.start_sway(0.06)
        self.play(FadeIn(bird), run_time=self.beat(0.05))
        left = VGroup(*[polyline([(-1.0 + 3.4 * i / 40, -0.4 + dy + 0.1 * math.sin(i / 3.0)) for i in range(41)], NERVEC, 6) for dy in (-0.14, 0, 0.14)])
        right = VGroup(*[polyline([(2.4 + 3.6 * i / 40, -0.4 + dy + 0.1 * math.sin(i / 3.0 + 1)) for i in range(41)], NERVEC, 6) for dy in (-0.14, 0, 0.14)])
        self.at("nerves")
        self.play(Create(left), Create(right), run_time=1.2)
        q = T("?", 110, TEXT, weight=BOLD).move_to(P3(-1.3, 3.1))
        q.t = 0.0
        q.add_updater(lambda m, dt: (setattr(m, "t", m.t + dt), m.set_opacity(0.65 + 0.35 * math.sin(3 * m.t)))[0])
        self.at("and what decides")
        self.add(q)
        self.play(FadeIn(q, scale=0.6), run_time=0.6)
        self.at("physician in")
        cap = T("Arnold Berthold, Göttingen, 1849", 32, GOLD).move_to(P3(0, -3.5))
        self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.8)
        # scissors
        piv = P3(2.4, -0.4)
        b1 = VGroup(Line(piv, piv + P3(1.0 * math.cos(0.6), 1.0 * math.sin(0.6)), stroke_width=8, color=TEXT),
                    Circle(radius=0.18, color=TEXT, stroke_width=6).move_to(piv + P3(1.25 * math.cos(0.6), 1.25 * math.sin(0.6))))
        b2 = VGroup(Line(piv, piv + P3(1.0 * math.cos(-0.6), 1.0 * math.sin(-0.6)), stroke_width=8, color=TEXT),
                    Circle(radius=0.18, color=TEXT, stroke_width=6).move_to(piv + P3(1.25 * math.cos(-0.6), 1.25 * math.sin(-0.6))))
        self.at("asked")
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.5)
        self.play(Rotate(b1, -0.6, about_point=piv), Rotate(b2, 0.6, about_point=piv), run_time=0.5)
        self.play(right.animate.shift(RIGHT * 0.45 + DOWN * 0.1), left.animate.shift(LEFT * 0.1), FadeOut(b1), FadeOut(b2), run_time=0.8)
        self.at("young")
        lb = T("young cockerel", 32, TEXT).move_to(P3(-2.6, -2.85))
        self.play(FadeIn(lb), run_time=0.6)
        self.wait(0.3)
        self.finish()


class S02Berthold(SpokenScene):
    def construct(self):
        L = Bird(4.0).move_to(P3(-3.6, -0.2))
        R = Bird(4.0).move_to(P3(3.6, -0.2))
        tL = Ellipse(width=0.5, height=0.32).set_fill(ORANGE, 1).set_stroke(width=0).move_to(L.belly() + P3(-0.15, -0.1, 0))
        tR = Ellipse(width=0.5, height=0.32).set_fill(ORANGE, 1).set_stroke(width=0).move_to(R.belly() + P3(-0.15, -0.1, 0))
        L.start_sway(0.05, 0.0)
        R.start_sway(0.05, 1.5)
        tL.add_updater(lambda m, dt: m.move_to(L.belly() + P3(-0.15, -0.1, 0)))
        tR.add_updater(lambda m, dt: m.move_to(R.belly() + P3(-0.15, -0.1, 0)))
        self.play(FadeIn(L), FadeIn(R), FadeIn(tL), FadeIn(tR), run_time=0.4)
        self.at("castrated")
        self.play(FadeOut(tL, scale=0.2), FadeOut(tR, scale=0.2), run_time=1.0)
        self.at("without testes")
        self.play(L.cs.animate.set_value(0.3), R.cs.animate.set_value(0.3), run_time=2.2)
        self.at("small combs")
        lc = T("castrated", 34, TEXT).move_to(P3(-3.6, -2.85))
        self.play(FadeIn(lc), run_time=0.6)
        self.at("in some birds")
        self.wait(0.6)
        self.at("testis")
        graft = Ellipse(width=0.7, height=0.46).set_fill(ORANGE, 1).set_stroke(TEXT, 3).move_to(R.belly() + P3(-0.2, -0.1, 0))
        graft.add_updater(lambda m, dt: m.move_to(R.belly() + P3(-0.2, -0.1, 0)))
        self.play(FadeIn(graft, scale=2.5), run_time=0.8)
        gl = T("testis graft", 34, ORANGE).move_to(P3(3.6, -2.85))
        self.play(FadeIn(gl), run_time=0.6)
        self.at("cut off")
        stub = polyline([(3.9, -0.45), (4.2, -0.62), (4.4, -0.55), (4.6, -0.72)], NERVEC, 6)
        stub.add_updater(lambda m, dt: m.move_to(R.belly() + P3(0.95, -0.35, 0)))
        xm = VGroup(Line(P3(-0.2, -0.2), P3(0.2, 0.2)), Line(P3(-0.2, 0.2), P3(0.2, -0.2))).set_stroke(TEXT, 8)
        xm.add_updater(lambda m, dt: m.move_to(R.belly() + P3(1.35, -0.45, 0)))
        self.play(Create(stub), run_time=0.8)
        self.play(FadeIn(xm, scale=1.5), run_time=0.5)
        self.at("those birds")
        self.play(R.cs.animate.set_value(1.0), run_time=1.8)
        self.at("crowed", nth=1)
        bub = bubble("crow!", P3(5.7, 2.6), 34)
        self.play(FadeIn(bub, scale=0.7), run_time=0.5)
        self.wait(0.5)
        self.finish()


class S03Blood(SpokenScene):
    def construct(self):
        graft = Ellipse(width=2.0, height=1.3).set_fill(ORANGE, 0.9).set_stroke(TEXT, 3).move_to(P3(-5.2, 2.5))
        gl = T("graft", 30, TEXT).move_to(graft)
        vess = RoundedRectangle(corner_radius=0.45, width=13.2, height=1.3, stroke_color=VESS, stroke_width=5,
                                fill_color=VESS, fill_opacity=0.35).move_to(P3(0, 0.6, 0))
        flow = Flow([(-5.2, 1.9), (-5.2, 0.6), (6.3, 0.6)], ORANGE, spacing=0.55, speed=1.8, r=0.14)
        self.play(FadeIn(VGroup(graft, gl), scale=0.8), Create(vess), run_time=1.2)
        self.add(flow)
        self.at("sent something")
        flow.amount = 1.0
        self.at("blood", nth=0)
        bl = T("blood", 34, VESS).move_to(P3(3.2, 1.7))
        self.play(FadeIn(bl), run_time=0.6)
        self.at("hormone")
        hl = T("hormone", 34, ORANGE).move_to(P3(-1.0, 1.7))
        self.play(FadeIn(hl), run_time=0.6)
        self.at("one group of cells")
        self.play(graft.animate.scale(1.12), run_time=0.4)
        self.play(graft.animate.scale(1 / 1.12), run_time=0.4)
        self.at("into the blood")
        self.play(vess.animate.set_stroke(TEXT, 6), run_time=0.4)
        self.play(vess.animate.set_stroke(VESS, 5), run_time=0.4)
        self.at("distant cells")
        cells = VGroup()
        xs = [-4.5, -1.5, 1.5, 4.5]
        for x in xs:
            cells.add(RoundedRectangle(corner_radius=0.3, width=2.1, height=1.6, stroke_color=GREY, stroke_width=4,
                                       fill_color=GREY, fill_opacity=0.12).move_to(P3(x, -2.1, 0)))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cells], lag_ratio=0.3), run_time=1.6)
        self.at("only cells")
        cups = VGroup()
        for x in (xs[1], xs[3]):
            cups.add(Arc(radius=0.45, start_angle=PI, angle=PI, stroke_color=CELLC, stroke_width=9).move_to(P3(x, -1.0, 0)))
        self.play(Create(cups), run_time=1.0)
        self.at("receptor")
        rl = T("receptor", 32, CELLC).move_to(P3(xs[1] + 0.2, -3.5, 0))
        self.play(FadeIn(rl), run_time=0.6)
        self.at("respond")
        d1 = Dot(P3(xs[1] - 0.8, 0.6, 0), radius=0.14, color=ORANGE)
        d2 = Dot(P3(xs[3] - 0.8, 0.6, 0), radius=0.14, color=ORANGE)
        self.add(d1, d2)
        self.play(d1.animate.move_to(P3(xs[1], -0.7, 0)), d2.animate.move_to(P3(xs[3], -0.7, 0)),
                  cells[1].animate.set_fill(CELLC, 0.55).set_stroke(CELLC, 6), cells[3].animate.set_fill(CELLC, 0.55).set_stroke(CELLC, 6),
                  run_time=1.2)
        self.wait(0.4)
        self.finish()


class S04Tank(SpokenScene):
    def construct(self):
        t = Tank(self, cx=0.5, cy=-0.2, w=3.2, h=4.0, L=0.0, base=0.0, k=0.0)
        self.add(*t.parts())
        self.at("tank")
        self.play(Create(t.frame), run_time=1.0)
        pl = T("plasma (schematic)", 30, TEXT).move_to(P3(-3.5, -1.4, 0))
        self.play(FadeIn(pl), run_time=0.6)
        self.at("gland")
        gl = T("gland: secretion", 32, ORANGE).move_to(P3(-2.1, 3.4, 0))
        self.play(FadeIn(t.tap), FadeIn(gl), run_time=0.8)
        self.at("pouring")
        t.show_in = True
        self.play(t.base.animate.set_value(0.65), run_time=1.0)
        self.at("drain")
        dl = T("clearance (all removal)", 30, GREY).move_to(P3(3.9, -3.0, 0))
        t.show_out = True
        self.play(FadeIn(t.stub), t.k.animate.set_value(1.0), FadeIn(dl), run_time=1.0)
        self.at("water line")
        ll = T("hormone level", 32, TEAL).move_to(P3(-3.0, t.surf_y(), 0))
        ll.add_updater(lambda m, dt: m.move_to(P3(-2.9, t.surf_y(), 0)))
        self.play(FadeIn(ll), run_time=0.6)
        self.at("settles")
        ie = T("in = out", 36, TEXT).move_to(P3(t.rt + 1.9, t.cy, 0))
        self.wait(1.0)
        self.at("what drains out")
        self.play(FadeIn(ie), run_time=0.6)
        self.wait(1.5)
        self.finish()


class S05Capon(SpokenScene):
    def construct(self):
        t = Tank(self, cx=0.5, cy=-0.2, w=3.2, h=4.0, L=0.64, base=0.65, k=1.0)
        t.show_in = t.show_out = True
        bird = Bird(3.0).move_to(P3(-4.4, -0.8))
        bird.start_sway(0.04)
        bird.add_updater(lambda m, dt: m.cs.set_value(0.3 + 0.7 * clip(t.Lt.get_value() / 0.64, 0, 1)))
        self.add(*t.parts(), t.frame, t.stub, t.tap, bird)
        tag = T("model", 32, TEXT).move_to(P3(4.6, 3.2, 0))
        self.play(FadeIn(tag), run_time=0.6)
        self.at("castration shut")
        self.play(t.base.animate.set_value(0.0), run_time=1.0)
        self.at("graft opened")
        graft = Ellipse(width=0.9, height=0.6).set_fill(ORANGE, 1).set_stroke(TEXT, 3).move_to(P3(-5.6, 3.0, 0))
        gl = T("graft", 30, TEXT).next_to(graft, UP, buff=0.12)
        self.play(FadeIn(graft), FadeIn(gl), run_time=0.5)
        self.play(graft.animate.move_to(P3(-3.4, 2.15, 0)), gl.animate.move_to(P3(-3.4, 2.9, 0)), run_time=1.0)
        t.base.set_value(0.65)
        self.at("traits came back")
        bub = bubble("crow!", P3(-5.0, 2.3), 32)
        self.play(FadeIn(bub, scale=0.7), run_time=0.5)
        self.at("never measured")
        t.dashed = True
        nm = T("level not measured\nby Berthold", 30, TEAL, line_spacing=0.8).move_to(P3(4.6, -2.6, 0))
        self.play(FadeIn(nm), run_time=0.8)
        self.wait(0.4)
        self.finish()


# ------------------------------------------------------------------ the stress-axis loop (s06-s11)
COLX, BW, BH = -4.4, 4.2, 1.4
BY = {"hyp": 2.3, "pit": 0.1, "adr": -2.1}
PIPE = [(-2.3, -2.1), (0.9, -2.1), (0.9, 1.15), (3.1, 1.15)]


def gbox(key, name):
    r = RoundedRectangle(corner_radius=0.18, width=BW, height=BH, stroke_color=ORANGE, stroke_width=4,
                         fill_color=ORANGE, fill_opacity=0.12).move_to(P3(COLX, BY[key], 0))
    t = T(name, 30, TEXT)
    fit(t, max_w=BW - 0.4)
    return VGroup(r, t.move_to(r))


class Loop:
    def __init__(s, sc, L=0.57, base=1.2, f=1.0, adr=1.0, pipe=PIPE):
        s.sc = sc
        s.tank = Tank(sc, cx=3.7, cy=-0.9, w=2.8, h=3.4, pipe=pipe, arrows=False, handle=False, L=L, base=base, f=f, adr=adr)
        s.box = {k: gbox(k, n) for k, n in [("hyp", "hypothalamus"), ("pit", "anterior pituitary"), ("adr", "adrenal cortex")]}
        s.ves1 = Rectangle(width=0.36, height=0.8, stroke_color=VESS, stroke_width=4, fill_color=VESS, fill_opacity=0.35).move_to(P3(COLX, 1.2, 0))
        s.ves2 = Rectangle(width=0.36, height=0.8, stroke_color=VESS, stroke_width=4, fill_color=VESS, fill_opacity=0.35).move_to(P3(COLX, -0.9, 0))
        s.crh = Flow([(COLX, 1.6), (COLX, 0.8)], ORANGE, spacing=0.2, speed=1.0, r=0.08)
        s.acth = Flow([(COLX, -0.5), (COLX, -1.3)], ORANGE, spacing=0.2, speed=1.0, r=0.08)
        s.vc = s.va = 1.0
        s.ring = Circle(radius=0.25, color=TEAL, stroke_width=6).move_to(P3(5.4, -0.9, 0))
        s.fbA = dpath([(5.65, -0.9), (6.2, -0.9), (6.2, 3.65), (-1.2, 3.65), (-1.2, 2.3), (-2.3, 2.3)])
        s.fbB = dpath([(-1.2, 2.3), (-1.2, 0.1), (-2.3, 0.1)])
        s.fb = VGroup(s.fbA, s.fbB)
        s.fbvis = 0.0
        s.ctl = VGroup()
        s.ctl.add_updater(lambda m, dt: s._ctl())

    def _ctl(s):
        d = s.tank.D / 0.9
        s.crh.amount = s.vc * d
        s.acth.amount = s.va * d
        s.fb.set_opacity(s.fbvis * clip(s.tank.Lt.get_value() / 0.8, 0, 1))

    def parts(s):
        return [s.ctl, s.crh, s.acth] + s.tank.parts()

    def statics(s):
        return [s.tank.frame, s.tank.stub, s.tank.tap, s.ves1, s.ves2, s.box["hyp"], s.box["pit"], s.box["adr"]]

    def cross_out_adrenal(s):
        b = s.box["adr"]
        if len(b) > 1:
            b[1].set_opacity(0)
        x = VGroup(Line(b.get_corner(UL) + P3(0.3, -0.25), b.get_corner(DR) + P3(-0.3, 0.25)),
                   Line(b.get_corner(DL) + P3(0.3, 0.25), b.get_corner(UR) + P3(-0.3, -0.25))).set_stroke(TEXT, 8)
        return x


class S06Axis(SpokenScene):
    def construct(self):
        lp = Loop(self, L=0.0, base=0.0, f=0.0, adr=0.0)
        t = lp.tank
        self.add(lp.crh, lp.acth, *t.parts())
        bx = lp.box
        names = {k: bx[k][1] for k in bx}
        for k in bx:
            bx[k].remove(names[k])
        self.play(LaggedStart(*[FadeIn(bx[k]) for k in ("hyp", "pit", "adr")], lag_ratio=0.35), run_time=1.6)
        for k in bx:
            bx[k][0].tt = 0.0
            bx[k][0].add_updater(lambda m, dt: (setattr(m, "tt", m.tt + dt), m.set_fill(ORANGE, 0.14 + 0.08 * math.sin(2.5 * m.tt)))[0])
        self.at("human")
        ah = T("adult human", 32, TEXT).move_to(P3(COLX, 3.55, 0))
        self.play(FadeIn(ah), run_time=0.6)
        self.at("hypothalamus")
        bx["hyp"].add(names["hyp"])
        self.play(FadeIn(names["hyp"]), run_time=0.5)
        self.at("crh")
        crhl = T("CRH", 32, ORANGE).move_to(P3(-5.5, 1.2, 0))
        lp.crh.amount = 0.8
        self.play(FadeIn(crhl), FadeIn(lp.ves1), run_time=0.6)
        self.at("short veins")
        pv = T("portal vessels", 30, VESS).move_to(P3(-2.75, 1.2, 0))
        self.play(FadeIn(pv), run_time=0.6)
        self.at("anterior")
        bx["pit"].add(names["pit"])
        self.play(FadeIn(names["pit"]), run_time=0.5)
        self.at("a cth")
        acl = T("ACTH", 32, ORANGE).move_to(P3(-3.2, -0.9, 0))
        lp.acth.amount = 0.8
        self.play(FadeIn(acl), FadeIn(lp.ves2), run_time=0.6)
        self.at("adrenal cortex")
        bx["adr"].add(names["adr"])
        self.play(FadeIn(names["adr"]), run_time=0.5)
        self.at("cortisol")
        cl = T("cortisol", 32, ORANGE).move_to(P3(-0.6, -2.55, 0))
        t.Lt.set_value(0.57)
        t.adr.set_value(1.0)
        t.base.set_value(0.57)
        self.play(FadeIn(t.frame), FadeIn(t.stub), FadeIn(t.tap), FadeIn(cl), run_time=0.8)
        self.wait(0.3)
        self.finish()


class _LoopScene(SpokenScene):
    """Common start: the loop already on screen, steady at L = 0.57."""
    L0, F0, ADR0, VC, VA, FB = 0.57, 1.0, 1.0, 1.0, 1.0, 0.0

    def loop(self, extra=()):
        lp = Loop(self, L=self.L0, base=1.2, f=self.F0, adr=self.ADR0)
        lp.vc, lp.va, lp.fbvis = self.VC, self.VA, self.FB
        self.lp = lp
        self.add(*lp.parts(), *lp.statics(), lp.fb, lp.ring)
        return lp

    def hormone_labels(self):
        a = T("CRH", 32, ORANGE).move_to(P3(-5.5, 1.2, 0))
        b = T("ACTH", 32, ORANGE).move_to(P3(-3.2, -0.9, 0))
        c = T("cortisol", 32, ORANGE).move_to(P3(-0.6, -2.55, 0))
        self.add(a, b, c)
        return a, b, c


class S07Feedback(_LoopScene):
    FB = 0.0

    def construct(self):
        lp = self.loop()
        self.hormone_labels()
        t = lp.tank
        sl = T("sensor", 30, TEAL).move_to(P3(5.95, -1.5, 0))
        lp.ring.set_opacity(0)
        self.at("sensor")
        self.play(lp.ring.animate.set_opacity(1), FadeIn(sl), run_time=0.8)
        self.at("cortisol acts back")
        lp.fbvis = 1.0
        self.play(Create(lp.fbA), Create(lp.fbB), run_time=1.6)
        self.at("turning their taps down")
        self.wait(0.2)
        self.at("when cortisol rises")
        t.inj.set_value(0.3)
        self.wait(1.1)
        t.inj.set_value(0.0)
        self.at("drive to make")
        self.wait(0.2)
        self.at("when it drops")
        t.inj.set_value(-0.35)
        self.wait(1.0)
        t.inj.set_value(0.0)
        self.at("negative feedback")
        nf = T("negative feedback", 38, RED).move_to(P3(2.6, 3.0, 0))
        self.play(FadeIn(nf, shift=DOWN * 0.15), run_time=0.7)
        self.at("opposes")
        self.wait(1.5)
        self.finish()


class S08Predict(_LoopScene):
    FB = 1.0

    def construct(self):
        lp = self.loop()
        self.hormone_labels()
        t = lp.tank
        self.at("suppose")
        self.wait(0.5)
        self.at("adrenal glands")
        self.wait(0.3)
        self.at("removed")
        x = lp.cross_out_adrenal()
        rl = T("adrenals removed", 30, TEXT).move_to(P3(COLX, -3.3, 0))
        t.adr.set_value(0.0)
        self.play(lp.box["adr"].animate.set_opacity(0.4), Create(x), FadeIn(rl), run_time=1.0)
        self.at("cortisol falls")
        lp.vc = lp.va = 0.0
        self.wait(0.5)
        self.at("what happens")
        q = VGroup(T("ACTH:", 38, TEXT), T("up, down or the same?", 38, TEXT)).arrange(DOWN, buff=0.15)
        card = RoundedRectangle(corner_radius=0.2, width=q.width + 0.6, height=q.height + 0.5, stroke_color=GOLD, stroke_width=4,
                                fill_color=BG, fill_opacity=1).move_to(P3(2.3, 2.55, 0))
        q.move_to(card)
        qm = T("?", 60, GREY).move_to(P3(-2.0, -0.9, 0))
        self.play(FadeIn(VGroup(card, q), scale=0.9), FadeIn(qm), run_time=0.8)
        self.wait(0.5)
        self.finish()


class S09Pause(NarratedScene):
    """Predict pause: the question holds, 5 s, with a ring timer."""

    def construct(self):
        lp = Loop(self, L=0.1, base=1.2, f=1.0, adr=0.0)
        lp.vc = lp.va = 0.0
        lp.fbvis = 1.0
        self.add(*lp.parts(), *lp.statics(), lp.fb, lp.ring)
        lp.box["adr"].set_opacity(0.4)
        self.add(lp.cross_out_adrenal(), T("adrenals removed", 30, TEXT).move_to(P3(COLX, -3.3, 0)))
        for s_, p_ in [("CRH", (-5.5, 1.2)), ("ACTH", (-3.2, -0.9)), ("cortisol", (-0.6, -2.55))]:
            self.add(T(s_, 32, ORANGE).move_to(P3(*p_)))
        q = VGroup(T("ACTH:", 38, TEXT), T("up, down or the same?", 38, TEXT)).arrange(DOWN, buff=0.15)
        card = RoundedRectangle(corner_radius=0.2, width=q.width + 0.6, height=q.height + 0.5, stroke_color=GOLD, stroke_width=4,
                                fill_color=BG, fill_opacity=1).move_to(P3(2.3, 2.55, 0))
        q.move_to(card)
        self.add(card, q, T("?", 60, GREY).move_to(P3(-2.0, -0.9, 0)))
        ring_c = P3(6.1, 2.55, 0)
        tv = ValueTracker(0)
        ring = Arc(radius=0.4, start_angle=PI / 2, angle=-2 * PI, stroke_color=GOLD, stroke_width=8)
        ring.add_updater(lambda m: m.become(Arc(radius=0.4, start_angle=PI / 2, angle=-2 * PI * (1 - tv.get_value()) - 0.001, stroke_color=GOLD, stroke_width=8).move_to(ring_c)))
        self.add(ring)
        self.play(tv.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        self.finish()


class S10Reveal(_LoopScene):
    L0, ADR0, FB = 0.08, 0.0, 1.0
    VC, VA = 0.0, 0.0

    def construct(self):
        lp = self.loop()
        t = lp.tank
        lp.box["adr"].set_opacity(0.4)
        x = lp.cross_out_adrenal()
        rl = T("adrenals removed", 30, TEXT).move_to(P3(COLX, -3.3, 0))
        self.add(x, rl)
        a, b, c = self.hormone_labels()
        qm = T("?", 60, GREY).move_to(P3(-2.0, -0.9, 0))
        self.add(qm)
        self.at("rises")
        b2 = T("ACTH up", 34, ORANGE).move_to(P3(-3.0, -0.9, 0))
        lp.va = 1.0
        self.play(FadeOut(qm), FadeOut(b), FadeIn(b2), run_time=0.8)
        self.at("key break")
        self.wait(1.0)
        self.at("hypothalamus")
        a2 = T("CRH up", 34, ORANGE).move_to(P3(-5.7, 1.2, 0))
        lp.vc = 1.0
        self.play(FadeOut(a), FadeIn(a2), run_time=0.8)
        self.at("no adrenal")
        ca = T("cannot answer", 32, TEXT).move_to(P3(COLX, -3.3, 0))
        self.play(FadeOut(rl), FadeIn(ca), run_time=0.6)
        self.at("taking a gland")
        self.wait(2.0)
        self.finish()


def daily(tc):
    """Tank input a(t): a daily wave plus pulses about every 75 min (schematic)."""
    s = math.sin(math.pi * tc / 1.25) ** 6
    return max(0.05, 0.5 + 0.22 * math.cos(2 * math.pi * (tc - 8) / 24) + 0.5 * (s - 0.3125))


class S11Pattern(_LoopScene):
    FB = 1.0

    def construct(self):
        lp = self.loop()
        t = lp.tank
        la, lb, lc = self.hormone_labels()
        short = polyline([(1.2, t.ny), (t.nx, t.ny), (t.nx, t.ny - 0.28)], ORANGE, 16, 0.45)
        self.at("feedback does not")
        pl = T("tap", 32, ORANGE).move_to(P3(0.9, 0.6, 0))
        old = [lp.box["hyp"], lp.box["pit"], lp.box["adr"], lp.ves1, lp.ves2, lp.fbA, lp.fbB, la, lb, lc, lp.crh, lp.acth]
        lp.ctl.clear_updaters()
        self.play(*[FadeOut(m) for m in old], Transform(t.tap[0], short), run_time=1.2)
        t.pipe = [(1.2, t.ny), (t.nx, t.ny)]
        # plot
        X0, X1, Y0, Y1 = -6.2, 0.2, -2.7, 2.9
        ax = VGroup(Line(P3(X0, Y0, 0), P3(X1, Y0, 0), stroke_width=5, color=TEXT), Line(P3(X0, Y0, 0), P3(X0, Y1, 0), stroke_width=5, color=TEXT))
        ticks = VGroup(*[Line(P3(X0 + (X1 - X0) * h / 24, Y0, 0), P3(X0 + (X1 - X0) * h / 24, Y0 - 0.15, 0), stroke_width=4, color=TEXT) for h in (0, 6, 12, 18, 24)])
        tl = VGroup(*[T(str(h), 26, TEXT).move_to(P3(X0 + (X1 - X0) * h / 24, Y0 - 0.45, 0)) for h in (0, 12, 24)])
        xl = T("hours of the day", 28, TEXT).move_to(P3((X0 + X1) / 2, Y0 - 0.95, 0))
        yl = T("hormone level", 28, TEAL).move_to(P3(X0 + 1.4, Y1 - 0.05, 0))
        sch = T("schematic", 28, GREY).move_to(P3(X1 - 0.9, Y1 - 0.05, 0))
        self.play(Create(ax), FadeIn(ticks), FadeIn(tl), FadeIn(xl), FadeIn(yl), FadeIn(sch), run_time=1.4)
        # run the tank on the daily input and trace its own level
        t.f.set_value(0.0)
        t.r = 1.2
        tc = ValueTracker(0.0)
        hist = []
        trace = VMobject(stroke_color=TEAL, stroke_width=7, fill_opacity=0)
        cur = Dot(radius=0.12, color=TEAL)

        def drive(m, dt):
            if cur.t_on:
                x = tc.get_value()
                t.base.set_value(daily(x))
                hist.append((x, t.Lt.get_value()))
                if len(hist) > 1:
                    trace.set_points_as_corners([P3(X0 + (X1 - X0) * a / 24, Y0 + 0.25 + b * 4.2, 0) for a, b in hist])
                cur.move_to(P3(X0 + (X1 - X0) * x / 24, Y0 + 0.25 + t.Lt.get_value() * 4.2, 0))
        cur.t_on = False
        ctl = VGroup()
        ctl.add_updater(drive)
        t.base.set_value(daily(0.0))
        t.Lt.set_value(daily(0.0))
        cur.move_to(P3(X0, Y0 + 0.25 + daily(0.0) * 4.2, 0))
        self.add(ctl, trace, cur)
        self.at("in humans")
        cur.t_on = True
        fb2 = dpath([(5.65, -0.9), (6.2, -0.9), (6.2, 2.15), (1.7, 2.15), (1.7, 1.5)])
        fb2.set_opacity(0.9)
        hint = T("pulses about every\n60 to 90 min", 30, TEAL, line_spacing=0.8).move_to(P3(-3.0, 1.9, 0))

        def tail(m, dt):
            pass
        self.play(tc.animate.set_value(8.3), run_time=5.2, rate_func=linear)
        self.at("pulses")
        self.play(FadeIn(hint), tc.animate.set_value(15.3), run_time=4.3, rate_func=linear)
        self.at("adjusts the tap")
        self.play(Create(fb2), FadeIn(pl), tc.animate.set_value(17.0), run_time=1.0, rate_func=linear)
        self.play(tc.animate.set_value(24.0), run_time=4.4, rate_func=linear)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        t = Tank(self, cx=0.5, cy=-0.2, w=3.2, h=4.0, L=0.57, base=1.2, f=1.0, k=1.0)
        t.show_in = t.show_out = True
        self.add(*t.parts(), t.frame, t.stub, t.tap)
        self.at("secretion in")
        a = T("secretion in", 32, ORANGE).move_to(P3(t.rt + 2.2, t.cy + 1.5, 0))
        self.play(FadeIn(a), run_time=0.5)
        self.at("clearance out")
        b = T("clearance out", 32, GREY).move_to(P3(t.rt + 2.2, t.cy - 1.5, 0))
        self.play(FadeIn(b), run_time=0.5)
        self.at("feedback works")
        ring = Circle(radius=0.25, color=TEAL, stroke_width=6).move_to(P3(t.l - 0.35, t.cy + 0.2, 0))
        fb = dpath([(t.l - 0.6, t.cy + 0.2), (-3.3, t.cy + 0.2), (-3.3, 3.4), (t.cx - 1.9, 3.4), (t.cx - 1.9, 3.05)])
        self.play(FadeIn(ring), Create(fb), run_time=1.4)
        t.inj.set_value(0.25)
        self.wait(1.0)
        t.inj.set_value(0.0)
        self.at("how fast")
        # stopwatch beside the drain
        sw = VGroup(Circle(radius=0.5, color=TEXT, stroke_width=6), Line(P3(0, 0.5, 0), P3(0, 0.72, 0), stroke_width=8, color=TEXT),
                    Line(P3(0, 0, 0), P3(0.28, 0.2, 0), stroke_width=6, color=GREY)).move_to(P3(t.cx + 1.6, t.bot - 0.8, 0))
        self.play(FadeIn(sw, scale=0.6), run_time=0.6)
        hand = sw[2]
        pulse = ValueTracker(0)
        self.add(pulse)
        self.play(Rotate(hand, -2 * PI, about_point=sw[0].get_center()), t.k.animate.set_value(1.6), run_time=2.0)
        self.play(t.k.animate.set_value(0.6), run_time=2.0)
        self.finish()


class S13End(EndCard):
    LINE = "A hormone level balances secretion against clearance; feedback adjusts secretion."
