"""Where Does a Plant Add New Body?  (Biochemistrypedia explainer, levelled-up film)

COLOUR MAP: dividing cells TEAL, elongating cells AMBER, mature cells GREEN, vacuole pale blue,
new leaves light green, red only for "blocked".
ONE WORLD for the root scenes: a root tip drawn as 4 cell files, tip at the left, flowing in the
tip's frame. Every cell is placed from one age -> position map (cells are short for ages 0-4,
lengthen over ages 4-8, then stay at their final length), so the picture is computed, not sketched.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F2A93B"
GRN = "#7BC96F"
VAC = "#8FD3F4"
SOILC = "#A08060"
LEAF = "#B5E86A"
BODY = "#6F9A6A"
PALE = "#C8B79A"
CAPC = "#B8BEC9"

L0, LF, TB = 0.3, 1.5, 1.8
X0, XR = -5.0, 6.3
NROW, RH, RG, RY = 4, 0.8, 0.05, -0.1
HAIR = 0.45


def sm(u):
    u = min(max(float(u), 0.0), 1.0)
    return u * u * (3 - 2 * u)


_S = np.arange(0, 30, 0.02)


class Prof:
    """Age -> position map of a cell file. stretch 1 = normal, 0 = elongation blocked."""

    def __init__(s, stretch=1.0):
        lf = L0 + (LF - L0) * stretch
        L = L0 + (lf - L0) * np.array([sm((q - 4) / 4) for q in _S])
        s.cum = np.concatenate([[0], np.cumsum(L[:-1] * 0.02)])

    def x(s, n):
        return X0 + float(np.interp(max(n, 0), _S, s.cum))

    def n_of(s, x):
        return float(np.interp(x - X0, s.cum, _S))


P1 = Prof(1.0)
XD, XE = P1.x(4), P1.x(8)
ZONES = [(X0, XD, "zone of\ndivision", TEAL), (XD, XE, "zone of\nelongation", AMBER), (XE, XR, "zone of\nmaturation", GRN)]


def zone_group(k):
    l, r, txt, col = ZONES[k]
    bar = Line([l + 0.08, 2.4, 0], [r - 0.08, 2.4, 0], color=col, stroke_width=7)
    lab = T(txt, 28, col).move_to([(l + r) / 2, 3.05, 0])
    return VGroup(bar, lab)


def cell_color(n, stage):
    w1, w2 = sm((n - 3.7) / 0.6), sm((n - 7.7) / 0.6)
    col = interpolate_color(ManimColor(TEAL), ManimColor(AMBER), w1)
    col = interpolate_color(col, ManimColor(GRN), w2)
    zf = w1 + w2
    rev = min(max(stage - zf, 0.0), 1.0)
    return interpolate_color(ManimColor(GREY), col, rev), rev


def set_updater_group(grp, fn):
    def upd(m):
        m.submobjects = list(fn().submobjects)
    grp.add_updater(upd)


class World:
    """The carried root tip. Trackers: stage 0-3 (colour reveal), vac, hairs, focus, sync, stretch, rate."""

    def __init__(s, sc, stage=0.0, vac=0.0, hairs=0.0, focus=0.0, sync=0.0, stretch=1.0, rate=1.0,
                 cap=0.0, zoom=1.0, gop=1.0, tv0=20.0, anchor=None):
        mk = ValueTracker
        s.stage, s.vac, s.hairs, s.focus, s.sync = mk(stage), mk(vac), mk(hairs), mk(focus), mk(sync)
        s.stretch, s.rate, s.cap, s.zoom, s.gop, s.T = mk(stretch), mk(rate), mk(cap), mk(zoom), mk(gop), mk(tv0)
        s.anchor = np.array(anchor if anchor is not None else [0, 0, 0], dtype=float)
        s.T.add_updater(lambda m, dt: m.increment_value(dt * s.rate.get_value() / TB))
        rng = np.random.RandomState(7)
        s.grains = VGroup(*[Dot([rng.uniform(-7, 7), rng.uniform(-3.7, 3.7), 0], radius=rng.uniform(0.03, 0.07),
                                color=SOILC) for _ in range(70)])

        def gupd(m, dt):
            v = (L0 + (LF - L0) * s.stretch.get_value()) / TB * s.rate.get_value()
            op = 0.4 * s.gop.get_value()
            for d in m:
                d.shift(RIGHT * v * dt)
                if d.get_x() > 7.1:
                    d.shift(LEFT * 14.2)
                d.set_opacity(op)
        s.grains.add_updater(gupd)
        s.root = VGroup()
        set_updater_group(s.root, s.build)
        sc.add(s.T, s.grains, s.root)

    def build(s):
        tv = s.T.get_value()
        st, vac, hairs = s.stage.get_value(), s.vac.get_value(), s.hairs.get_value()
        foc, sync, capv = s.focus.get_value(), s.sync.get_value(), s.cap.get_value()
        P = Prof(s.stretch.get_value())
        g = VGroup()
        cap = RoundedRectangle(corner_radius=0.6, width=1.2, height=NROW * RH + (NROW - 1) * RG, stroke_width=3,
                               stroke_color=CAPC, fill_color=CAPC, fill_opacity=0.12 + 0.3 * capv).move_to([-5.6, RY, 0])
        cap.set_stroke(CAPC, 3, opacity=0.5 + 0.5 * capv)
        g.add(cap)
        vacs, hs, lines = VGroup(), VGroup(), VGroup()
        for r in range(NROW):
            y = RY + (NROW - 1) / 2 * (RH + RG) - r * (RH + RG)
            ph = (r / NROW) * (1 - sync)
            f = (tv + ph) % 1.0
            base = int(np.floor(tv + ph))
            dim = 1 - 0.65 * foc if r != 1 else 1.0
            for j in range(-1, 40):
                n = f + j
                l, rr = P.x(n), P.x(n + 1)
                if l >= XR:
                    break
                rr = min(rr, XR)
                w = rr - l - 0.05
                if w < 0.04:
                    continue
                col, rev = cell_color(n, st)
                c = RoundedRectangle(corner_radius=min(0.1, w / 2.5), width=w, height=RH)
                c.set_fill(col, opacity=(0.14 + 0.5 * rev) * dim)
                c.set_stroke(col, 2, opacity=(0.5 + 0.5 * rev) * dim)
                c.move_to([(l + rr) / 2, y, 0])
                g.add(c)
                if vac > 0.01 and n >= 4:
                    vf = 0.15 + 0.6 * sm((n - 4) / 4)
                    vw, vh = max(0.06, (w - 0.1) * (0.3 + 0.6 * vf)), RH * (0.25 + 0.5 * vf)
                    v = RoundedRectangle(corner_radius=min(0.08, vw / 2.5, vh / 2.5), width=vw, height=vh)
                    v.set_fill(VAC, opacity=0.8 * vac * dim).set_stroke(width=0).move_to([(l + rr) / 2, y, 0])
                    vacs.add(v)
                if hairs > 0.01 and n >= 9 and r in (0, NROW - 1):
                    ln = min(HAIR, 0.3 * (n - 9)) * hairs
                    if ln > 0.03:
                        idx = base + j
                        sl = 0.18 * np.sin(idx * 1.7)
                        sgn = 1 if r == 0 else -1
                        yb = y + sgn * RH / 2
                        hs.add(Line([(l + rr) / 2, yb, 0], [(l + rr) / 2 + sl, yb + sgn * ln, 0], color=GRN, stroke_width=3))
                if j == -1 and rr > l:
                    lines.add(Line([rr, y - RH / 2, 0], [rr, y + RH / 2, 0], color=TEXT, stroke_width=3).set_opacity((1 - f) * 0.8 * dim))
        g.add(vacs, hs, lines)
        if foc > 0.01:
            y1 = RY + (NROW - 1) / 2 * (RH + RG) - 1 * (RH + RG)
            fr = Rectangle(width=XR - X0 + 0.1, height=RH + 0.1, stroke_color=TEXT, stroke_width=4, fill_opacity=0)
            fr.set_stroke(TEXT, 4, opacity=foc).move_to([(XR + X0) / 2, y1, 0])
            g.add(fr)
        z = s.zoom.get_value()
        if z < 0.999:
            tip = np.array([-6.2, RY, 0])
            scl = 0.1 + 0.9 * sm(z)
            g.shift(-tip).scale(scl, about_point=ORIGIN).shift(s.anchor + sm(z) * (tip - s.anchor))
        return g


class Marks:
    XS = [-4.6 + 1.2 * k for k in range(8)]

    def __init__(s, sc, w, mk=0.0, t0=20.0):
        s.mk, s.w, s.t0 = ValueTracker(mk), w, t0
        s.n0 = [P1.n_of(x) for x in s.XS]
        s.grp = VGroup()
        set_updater_group(s.grp, s.build)
        sc.add(s.grp)

    def build(s):
        g = VGroup()
        d = s.w.T.get_value() - s.t0
        for k, n0 in enumerate(s.n0):
            op = min(max(s.mk.get_value() * len(s.n0) - k, 0), 1)
            x = P1.x(n0 + d)
            if op > 0.02 and x < XR - 0.05:
                g.add(Line([x, RY - 1.8, 0], [x, RY + 1.8, 0], color="#FFFFFF", stroke_width=6).set_opacity(op))
        return g


class Glows:
    def __init__(s, sc, pts_fn, tv=1.0):
        s.tv, s.t, s.pts_fn = ValueTracker(tv), ValueTracker(0), pts_fn
        s.t.add_updater(lambda m, dt: m.increment_value(dt))
        s.grp = VGroup()
        set_updater_group(s.grp, s.build)
        sc.add(s.t, s.grp)

    def build(s):
        g = VGroup()
        tv, t = s.tv.get_value(), s.t.get_value()
        if tv < 0.02:
            return g
        for i, p in enumerate(s.pts_fn()):
            ph = i * 1.3
            pulse = 0.5 + 0.5 * np.sin(2 * np.pi * t / 1.6 + ph)
            rp = ((t / 1.8) + ph / 6.28) % 1
            g.add(Circle(radius=(0.34 + 0.1 * pulse) * tv, stroke_width=0).set_fill(TEAL, 0.25).move_to(p))
            g.add(Circle(radius=(0.15 + 0.6 * rp) * tv).set_stroke(TEAL, 3, opacity=1 - rp).move_to(p))
            g.add(Dot(p, radius=(0.16 + 0.04 * pulse) * tv, color=TEAL))
        return g


# ---------------------------------------------------------------- oak and seedling
CX, SY = -1.0, 0.3          # seedling axis and soil surface
OX, OSY = -3.2, -0.7        # oak axis and soil surface
LEAFPTS = [(-2.9, 1.8), (-2.6, 2.6), (-1.9, 3.2), (-1.0, 3.55), (0, 3.6), (1.0, 3.45), (1.9, 3.1), (2.6, 2.5),
           (2.9, 1.8), (2.3, 1.0), (1.4, 0.55), (-1.4, 0.55), (-2.3, 1.0), (0.0, 1.0)]
OAK_TIPS = [(-2.6, 2.7), (0, 3.6), (2.6, 2.7), (2.9, 1.5)]
OAK_ROOT_TIPS = [(0, -3.3), (-1.7, -2.5), (1.7, -2.5), (-2.8, -1.7), (2.8, -1.7)]


def soil_rect(top):
    r = Rectangle(width=14.4, height=top + 3.9, stroke_width=0, fill_color=SOILC, fill_opacity=0.16)
    r.move_to([0, (top - 3.9) / 2, 0])
    ln = Line([-7.1, top, 0], [7.1, top, 0], color=SOILC, stroke_width=3)
    return VGroup(r, ln)


def make_oak(roots=False):
    trunk = Polygon([OX - 0.5, OSY, 0], [OX - 0.32, 1.3, 0], [OX + 0.32, 1.3, 0], [OX + 0.5, OSY, 0],
                    stroke_width=0, fill_color="#6B5642", fill_opacity=1)
    br = VGroup(Line([OX, 1.0, 0], [OX - 1.3, 1.9, 0]), Line([OX, 1.0, 0], [OX + 1.3, 1.9, 0]),
                Line([OX, 1.2, 0], [OX, 2.3, 0])).set_stroke("#6B5642", 9)
    crown = VGroup(*[Circle(radius=r).move_to([OX + x, y, 0]) for x, y, r in
                     [(-1.7, 1.75, 1.2), (1.7, 1.75, 1.2), (0, 2.35, 1.25), (-0.9, 1.2, 1.0), (0.9, 1.2, 1.0)]])
    crown.set_fill("#35553A", 0.95).set_stroke("#4F7A52", 2)
    g = VGroup(trunk, br, crown)
    if roots:
        rt = VGroup(Line([OX, OSY, 0], [OX, -3.3, 0]), Line([OX, -1.3, 0], [OX - 1.7, -2.5, 0]),
                    Line([OX, -1.3, 0], [OX + 1.7, -2.5, 0]), Line([OX, -0.9, 0], [OX - 2.8, -1.7, 0]),
                    Line([OX, -0.9, 0], [OX + 2.8, -1.7, 0])).set_stroke(PALE, 6)
        g.add(rt)
    return g


def make_leaves(sc):
    leaves = VGroup()
    for i, (x, y) in enumerate(LEAFPTS):
        e = Ellipse(width=0.5, height=0.26).set_fill(LEAF, 1).set_stroke(width=0)
        e.rotate((i * 37 % 90 - 20) * DEGREES).move_to([OX + x, y, 0])
        e.tt, e.ph = 0.0, i * 0.9

        def sway(m, dt):
            m.tt += dt
            m.rotate(0.35 * dt * np.cos(2.2 * m.tt + m.ph))
        e.add_updater(sway)
        leaves.add(e)
    return leaves


def seed_tips(g, tv=1.0):
    top = SY + 1.5 + 0.35 * g
    rooty = SY - 1.9 - 0.35 * g
    tips = [((CX, top), (0, 1)), ((CX, rooty), (0, -1))]
    for j, (thr, yb) in enumerate([(-1, SY - 0.5), (-1, SY - 1.0), (0.7, SY - 1.5), (1.4, SY - 1.8)]):
        ln = 1.5 * (1 if thr < 0 else sm((g - thr) / 0.6))
        if ln > 0.25:
            sd = (-1) ** j
            tips.append(((CX + sd * ln * 0.8, yb - ln * 0.6), (sd * 0.8, -0.6)))
    return tips


class Seed:
    def __init__(s, sc, g=0.0, tipv=0.0):
        s.g = ValueTracker(g)
        s.grp = VGroup()
        set_updater_group(s.grp, s.build)
        s.glow = Glows(sc, lambda: [np.array([p[0], p[1], 0]) for p, _ in seed_tips(s.g.get_value())], tipv)
        sc.add(s.grp)

    def build(s):
        g = s.g.get_value()
        gr = VGroup()
        top, rooty = SY + 1.5 + 0.35 * g, SY - 1.9 - 0.35 * g
        gr.add(Line([CX, SY, 0], [CX, top, 0], color=BODY, stroke_width=9))
        gr.add(Line([CX, SY, 0], [CX, rooty, 0], color=PALE, stroke_width=7))
        for k, thr in enumerate([-1, -1, 0.6, 1.2, 1.7]):
            sz = 1.0 if thr < 0 else sm((g - thr) / 0.5)
            if sz < 0.05:
                continue
            sd = (-1) ** k
            yk = SY + 0.5 + 0.42 * k
            e = Ellipse(width=1.2 * sz, height=0.5 * sz).set_fill(BODY, 0.9).set_stroke(width=0)
            e.rotate(sd * 30 * DEGREES).move_to([CX + sd * 0.55 * sz, yk + 0.2 * sz, 0])
            gr.add(e)
        for j, (thr, yb) in enumerate([(-1, SY - 0.5), (-1, SY - 1.0), (0.7, SY - 1.5), (1.4, SY - 1.8)]):
            ln = 1.5 * (1 if thr < 0 else sm((g - thr) / 0.6))
            if ln > 0.05:
                sd = (-1) ** j
                gr.add(Line([CX, yb, 0], [CX + sd * ln * 0.8, yb - ln * 0.6, 0], color=PALE, stroke_width=5))
        return gr


def tip_arrows(sc, seed, ar):
    t = ValueTracker(0)
    t.add_updater(lambda m, dt: m.increment_value(dt))
    grp = VGroup()

    def fn():
        g = VGroup()
        a = ar.get_value()
        if a < 0.02:
            return g
        for (p, d) in seed_tips(seed.g.get_value()):
            d = np.array([d[0], d[1], 0.0])
            d = d / np.linalg.norm(d)
            p = np.array([p[0], p[1], 0.0])
            ln = (0.55 + 0.25 * np.sin(2 * np.pi * t.get_value() / 1.4)) * a
            g.add(Arrow(p + d * 0.3, p + d * (0.3 + ln), buff=0, stroke_width=7, tip_length=0.22,
                        max_tip_length_to_length_ratio=0.6, color=TEXT))
        return g
    set_updater_group(grp, fn)
    sc.add(t, grp)
    return grp


def make_clock(sc, pos):
    t = ValueTracker(0)
    t.add_updater(lambda m, dt: m.increment_value(dt))
    face = Circle(radius=0.45, color=TEXT, stroke_width=4)
    hand = VGroup()

    def fn():
        a = 2 * np.pi * t.get_value() / 6
        return VGroup(Line(ORIGIN, [0.34 * np.sin(a), 0.34 * np.cos(a), 0], color=TEXT, stroke_width=5).shift(pos), Dot(pos, radius=0.05, color=TEXT))
    set_updater_group(hand, fn)
    face.move_to(pos)
    sc.add(t, hand)
    return VGroup(face, hand)


def question_mark(sc, pos, size=110):
    q = T("?", size, GOLD, weight=BOLD).move_to(pos)
    t = ValueTracker(0)
    t.add_updater(lambda m, dt: m.increment_value(dt))
    q.add_updater(lambda m: m.move_to(pos + UP * 0.1 * np.sin(2.2 * t.get_value())))
    sc.add(t)
    return q


def eq_lines():
    l1 = T("growth per hour =", 34, TEXT).move_to([0, 3.4, 0])
    p1 = T("new cells per file per hour", 30, TEAL)
    x = T("×", 30, TEXT)
    p3 = T("final cell length", 30, AMBER)
    row = VGroup(p1, x, p3).arrange(RIGHT, buff=0.3).move_to([0, 2.7, 0])
    u1 = Line(p1.get_corner(DL) + DOWN * 0.08, p1.get_corner(DR) + DOWN * 0.08, color=TEAL, stroke_width=5)
    u3 = Line(p3.get_corner(DL) + DOWN * 0.08, p3.get_corner(DR) + DOWN * 0.08, color=AMBER, stroke_width=5)
    return l1, p1, x, p3, u1, u3


# ---------------------------------------------------------------- scenes
class S00Title(TitleCard):
    TITLE = "Where Does a Plant Add New Body?"
    LESSON = "Plant Body and Growth"


class S01Hook(SpokenScene):
    def construct(self):
        soil = soil_rect(OSY)
        oak = make_oak()
        self.add(soil)
        self.play(FadeIn(oak), run_time=1.2)
        self.at("300")
        lab = T("about 300 years old", 32, TEXT).move_to([3.4, 0.4, 0])
        arr = Arrow([0.9, 0.4, 0], [OX + 0.6, 0.4, 0], buff=0.05, color=TEXT, stroke_width=5)
        self.play(FadeIn(lab), GrowArrow(arr), run_time=0.8)
        self.at("new leaves")
        leaves = make_leaves(self)
        self.play(LaggedStart(*[GrowFromCenter(l) for l in leaves], lag_ratio=0.1, run_time=0.9))
        self.at("made")
        q = T("?", 140, GOLD, weight=BOLD).move_to([OX, 2.0, 0])
        self.play(GrowFromCenter(q), run_time=0.5)
        self.at("but this spring's leaves")
        tg1 = T("this spring: months old", 28, LEAF).move_to([3.7, 2.8, 0])
        a1 = Arrow([1.3, 2.8, 0], [OX + 2.55, 2.55, 0], buff=0.05, color=LEAF, stroke_width=4)
        tg2 = T("this spring: months old", 28, LEAF).move_to([3.7, 1.5, 0])
        a2 = Arrow([1.3, 1.5, 0], [OX + 2.95, 1.8, 0], buff=0.05, color=LEAF, stroke_width=4)
        self.play(FadeIn(tg1), GrowArrow(a1), run_time=0.7)
        self.play(FadeIn(tg2), GrowArrow(a2), run_time=0.7)
        self.finish()


class S02Meristem(SpokenScene):
    def construct(self):
        soil = soil_rect(SY)
        oak = make_oak()
        osoil = soil_rect(OSY)
        self.add(osoil, oak)
        self.play(FadeOut(oak, scale=0.5), FadeOut(osoil), FadeIn(soil), run_time=1.2)
        seed = Seed(self, g=0.0, tipv=0.0)
        self.at("meristems")
        self.play(seed.glow.tv.animate.set_value(1), run_time=1.0)
        self.at("A meristem")
        lab = VGroup(T("meristem:", 30, TEAL, weight=BOLD), T("cells that keep dividing", 28, TEXT)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, 2.6, 0])
        ar = Arrow([1.05, 2.45, 0], [CX + 0.35, 2.3, 0], buff=0.05, color=TEAL, stroke_width=5)
        self.play(FadeIn(lab), GrowArrow(ar), run_time=0.9)
        self.at("many plants keep")
        chips = VGroup(*[chip(f"Year {i}", GREY, 28, fill_opacity=0.1) for i in (1, 2, 3)]).arrange(DOWN, buff=0.3).move_to([5.0, -0.3, 0])
        self.play(LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.2), run_time=1.0)
        self.play(chips[0][0].animate.set_fill(TEAL, 0.4).set_stroke(TEAL), run_time=0.3)
        self.at("years")
        self.play(seed.g.animate.set_value(1.0), chips[0][0].animate.set_fill(GREY, 0.1).set_stroke(GREY),
                  chips[1][0].animate.set_fill(TEAL, 0.4).set_stroke(TEAL), run_time=1.8)
        self.at("So they keep")
        self.play(seed.g.animate.set_value(2.0), chips[1][0].animate.set_fill(GREY, 0.1).set_stroke(GREY),
                  chips[2][0].animate.set_fill(TEAL, 0.4).set_stroke(TEAL), run_time=2.0)
        self.finish()


class S03Primary(SpokenScene):
    def construct(self):
        self.add(soil_rect(SY))
        seed = Seed(self, g=2.0, tipv=1.0)
        ar = ValueTracker(0)
        tip_arrows(self, seed, ar)
        self.wait(0.3)
        self.at("Apical meristems")
        l1 = T("apical meristems", 30, TEAL, weight=BOLD).move_to([4.4, 2.5, 0])
        self.play(FadeIn(l1), ar.animate.set_value(1), run_time=0.8)
        self.at("Growth from them")
        l2 = T("primary growth", 30, TEXT).move_to([4.4, 1.7, 0])
        self.play(FadeIn(l2), run_time=0.6)
        self.at("mainly growth")
        l3 = T("mainly length", 30, TEXT).move_to([4.4, 0.9, 0])
        self.play(FadeIn(l3), run_time=0.6)
        self.finish()


class S04Division(SpokenScene):
    def construct(self):
        soil = soil_rect(SY)
        seed = Seed(self, g=2.0, tipv=1.0)
        self.add(soil)
        S = np.array([CX, SY - 1.9 - 0.7, 0])
        w = World(self, stage=0, zoom=0.0, gop=0.0, anchor=S)
        seed.grp.clear_updaters()
        seed.glow.grp.clear_updaters()
        self.play(w.zoom.animate.set_value(1.0), FadeOut(seed.grp), FadeOut(soil), FadeOut(seed.glow.grp), run_time=2.6)
        self.play(w.gop.animate.set_value(1.0), run_time=0.3)
        self.at("A root cap")
        capl = T("root cap", 28, CAPC).move_to([-5.6, -2.45, 0])
        self.play(w.cap.animate.set_value(1), FadeIn(capl), run_time=0.8)
        self.at("small cells")
        self.play(w.stage.animate.set_value(1), run_time=1.5)
        self.at("This is the zone")
        self.play(FadeIn(zone_group(0)), run_time=0.8)
        self.finish()


class S05Elongation(SpokenScene):
    def construct(self):
        w = World(self, stage=1, cap=1)
        self.add(T("root cap", 28, CAPC).move_to([-5.6, -2.45, 0]), zone_group(0))
        self.wait(0.2)
        self.at("division tapers")
        self.wait(0.2)
        self.at("Cells lengthen")
        tag = T("about 20 times longer (illustrative, not to scale)", 24, TEXT).move_to([0, -3.4, 0])
        self.play(w.stage.animate.set_value(2), FadeIn(tag), run_time=1.4)
        self.at("water fills")
        self.play(w.vac.animate.set_value(1), run_time=0.9)
        self.at("vacuoles")
        vl = T("vacuole", 28, VAC).move_to([-1.2, 2.2, 0])
        va = Arrow([-1.2, 1.9, 0], [-1.2, 1.5, 0], buff=0.03, color=VAC, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(vl), GrowArrow(va), run_time=0.6)
        self.at("This is the zone")
        self.play(FadeOut(vl), FadeOut(va), run_time=0.3)
        self.play(FadeIn(zone_group(1)), run_time=0.7)
        self.finish()


class S06Maturation(SpokenScene):
    def construct(self):
        w = World(self, stage=2, vac=1, cap=1)
        self.add(T("root cap", 28, CAPC).move_to([-5.6, -2.45, 0]), zone_group(0), zone_group(1))
        self.wait(0.2)
        self.at("cells stop")
        self.play(w.stage.animate.set_value(3), run_time=1.8)
        self.at("root hairs")
        self.play(w.hairs.animate.set_value(1), run_time=2.4)
        self.at("This is the zone")
        self.play(FadeIn(zone_group(2)), run_time=0.8)
        self.finish()


class S07Conveyor(SpokenScene):
    def construct(self):
        w = World(self, stage=3, vac=1, hairs=1, cap=1)
        self.add(T("root cap", 28, CAPC).move_to([-5.6, -2.45, 0]), zone_group(0), zone_group(1), zone_group(2))
        self.at("Now follow")
        self.play(w.focus.animate.set_value(1), run_time=1.4)
        self.at("New cells leave")
        self.wait(0.2)
        self.at("steady rhythm")
        met = VGroup()
        mt = ValueTracker(0)
        mt.add_updater(lambda m, dt: m.increment_value(dt))
        base = Polygon([5.3, -3.45, 0], [6.3, -3.45, 0], [5.8, -2.55, 0], stroke_width=3, stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.15)

        def mfn():
            a = 0.5 * np.sin(np.pi * mt.get_value() / TB)
            piv = np.array([5.8, -3.35, 0])
            end = piv + 0.95 * np.array([np.sin(a), np.cos(a), 0])
            return VGroup(Line(piv, end, color=GOLD, stroke_width=5), Dot(end, radius=0.1, color=GOLD))
        set_updater_group(met, mfn)
        self.add(mt, met)
        self.play(FadeIn(base), run_time=0.5)
        self.at("Each one stretches")
        self.wait(0.2)
        self.at("Meanwhile")
        ar = Arrow([-2.4, -3.2, 0], [-4.9, -3.2, 0], buff=0, color=TEXT, stroke_width=7)
        tl = T("tip moves forward", 28, TEXT).move_to([0.9, -3.2, 0])
        self.play(GrowArrow(ar), FadeIn(tl), run_time=0.8)
        self.finish()


class S08Predict(SpokenScene):
    def construct(self):
        w = World(self, stage=3, vac=1, hairs=1, sync=1, cap=1, rate=0.0)
        m = Marks(self, w, mk=0.0)
        self.play(m.mk.animate.set_value(1.0), run_time=3.2, rate_func=linear)
        self.at("A day later")
        clk = make_clock(self, np.array([5.9, 3.05, 0]))
        txt = T("1 day later?", 30, TEXT).move_to([3.5, 3.05, 0])
        self.add(clk)
        self.play(FadeIn(txt), run_time=0.7)
        self.finish()


class S09Pause(NarratedScene):
    def construct(self):
        w = World(self, stage=3, vac=1, hairs=1, sync=1, cap=1, rate=0.0)
        Marks(self, w, mk=1.0)
        clk = make_clock(self, np.array([5.9, 3.05, 0]))
        self.add(clk, T("1 day later?", 30, TEXT).move_to([3.5, 3.05, 0]),
                 T("Which gaps widen?", 34, TEXT).move_to([-1.4, 3.05, 0]))
        self.add(question_mark(self, np.array([-5.5, 2.95, 0]), 100))
        self.finish()


class S10Reveal(SpokenScene):
    def construct(self):
        w = World(self, stage=3, vac=1, hairs=1, sync=1, cap=1, rate=0.0)
        Marks(self, w, mk=1.0)
        DN = 1.8
        self.add(T("root cap", 28, CAPC).move_to([-5.6, -2.45, 0]))
        w.rate.set_value(DN * TB / 6.8)
        self.at("zone of elongation")
        b1 = Line([XD + 0.08, 2.4, 0], [XE - 0.08, 2.4, 0], color=AMBER, stroke_width=7)
        l1 = T("widened", 32, AMBER, weight=BOLD).move_to([(XD + XE) / 2, 3.0, 0])
        self.play(Create(b1), FadeIn(l1), run_time=0.8)
        self.at("In the mature region")
        b2 = Line([XE + 0.08, 2.4, 0], [XR - 0.08, 2.4, 0], color=GRN, stroke_width=7)
        l2 = T("no change", 32, GRN, weight=BOLD).move_to([(XE + XR) / 2, 3.0, 0])
        self.play(Create(b2), FadeIn(l2), run_time=0.8)
        self.wait(max(0.01, 6.8 - self.elapsed()))
        w.rate.set_value(0.0)
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        w = World(self, stage=3, vac=1, hairs=1, sync=1, cap=1)
        l1, p1, x, p3, u1, u3 = eq_lines()
        self.add(T("root cap", 28, CAPC).move_to([-5.6, -2.45, 0]))
        self.at("So how fast")
        self.play(FadeIn(l1), run_time=0.8)
        self.at("Count the new cells")
        self.play(FadeIn(p1), Create(u1), run_time=1.0)
        self.at("Multiply by")
        self.play(FadeIn(x), FadeIn(p3), Create(u3), run_time=1.0)
        self.finish()


class S12Scope(SpokenScene):
    def construct(self):
        w = World(self, stage=3, vac=1, hairs=1, sync=1, cap=1)
        l1, p1, x, p3, u1, u3 = eq_lines()
        self.add(T("root cap", 28, CAPC).move_to([-5.6, -2.45, 0]), l1, p1, x, p3, u1, u3)
        self.at("That product")
        box = SurroundingRectangle(VGroup(l1, p1, p3), color=GOLD, buff=0.2, stroke_width=4)
        self.play(Create(box), run_time=1.0)
        self.at("It holds")
        tag = T("steady state: zones keep their size; every cell file alike", 26, TEXT).move_to([0, -3.4, 0])
        self.play(FadeIn(tag), run_time=0.8)
        self.at("every file")
        scan = Line([X0, RY - 1.8, 0], [X0, RY + 1.8, 0], color="#FFFFFF", stroke_width=4).set_opacity(0.85)
        self.play(scan.animate.shift(RIGHT * 11), run_time=3.2, rate_func=linear)
        self.play(FadeOut(scan), run_time=0.3)
        self.finish()


class S13Block(SpokenScene):
    def construct(self):
        w = World(self, stage=3, vac=1, hairs=1, sync=1, cap=1)
        l1, p1, x, p3, u1, u3 = eq_lines()
        box = SurroundingRectangle(VGroup(l1, p1, p3), color=GOLD, buff=0.2, stroke_width=4)
        eq = VGroup(l1, p1, x, p3, u1, u3, box)
        self.add(T("root cap", 28, CAPC).move_to([-5.6, -2.45, 0]), eq)
        self.at("block stretching")
        self.play(FadeOut(eq), run_time=0.5)
        bl = T("stretching blocked", 32, RED, weight=BOLD).move_to([-1.6, 3.05, 0])
        bar = Line([XD + 0.08, 2.4, 0], [XE - 0.08, 2.4, 0], color=RED, stroke_width=7)
        self.play(FadeIn(bl), Create(bar), w.stretch.animate.set_value(0.0), run_time=3.6)
        self.at("Cells keep coming")
        self.wait(0.2)
        self.at("barely creeps")
        tag = VGroup(T("growth falls to 1/20 of normal", 28, TEXT),
                     T("(illustrative numbers, not to scale)", 24, TEXT)).arrange(DOWN, buff=0.1).move_to([0, -3.2, 0])
        self.play(FadeIn(tag), run_time=0.8)
        self.finish()


def shoot_node_y(tau, m):
    return 2.5 - 1.25 * (tau - m)


class S14Shoot(SpokenScene):
    SX = -2.0

    def construct(self):
        SX = self.SX
        tau = ValueTracker(0.0)
        budv = ValueTracker(0.0)
        gl = Glows(self, lambda: [np.array([SX, 3.05, 0])], 1.0)
        grp = VGroup()

        def fn():
            g = VGroup(Line([SX, -3.8, 0], [SX, 3.0, 0], color="#5FA85A", stroke_width=14))
            tu = tau.get_value()
            for m in range(int(np.floor(tu)) - 5, int(np.floor(tu)) + 1):
                a = tu - m
                if a < 0 or a > 5:
                    continue
                y = shoot_node_y(tu, m)
                sd = 1 if m % 2 == 0 else -1
                ln = 0.2 + 1.5 * sm(a / 2.2)
                e = Ellipse(width=ln, height=0.12 + 0.34 * sm(a / 2.2)).set_fill(LEAF, 0.95).set_stroke(width=0)
                e.rotate(sd * 35 * DEGREES).move_to([SX + sd * (ln / 2 * np.cos(35 * DEGREES) + 0.05), y + ln / 2 * np.sin(35 * DEGREES), 0])
                g.add(e)
                g.add(Circle(radius=0.14, stroke_width=0).set_fill("#3E7A3A", 1).move_to([SX, y, 0]))
                bv = budv.get_value()
                if bv > 0.02:
                    g.add(Dot([SX + sd * 0.2, y + 0.22, 0], radius=0.11 * bv, color=TEAL))
            return g
        set_updater_group(grp, fn)
        self.add(tau, budv, grp)
        self.play(tau.animate.set_value(1.9), run_time=2.0, rate_func=linear)
        nc = T("no cap", 28, TEXT).move_to([SX + 1.7, 3.2, 0])
        self.at("though it has no cap")
        self.play(FadeIn(nc), tau.animate.set_value(3.2), run_time=2.0, rate_func=linear)
        self.at("At each node")
        nl = T("node", 28, TEXT)
        il = T("internode", 28, TEXT)
        bl = T("bud", 28, TEAL)

        def lab_upd(m):
            tu = tau.get_value()
            y1, y2 = shoot_node_y(tu, 1), shoot_node_y(tu, 2)
            nl.move_to([SX + 2.4, y1, 0])
            il.move_to([SX + 2.5, (y1 + y2) / 2, 0])
            bl.move_to([SX - 2.9, y1 - 0.5, 0])
        lg = VGroup(nl, il, bl)
        lg.add_updater(lab_upd)
        lines = VGroup()

        def line_fn():
            tu = tau.get_value()
            y1, y2 = shoot_node_y(tu, 1), shoot_node_y(tu, 2)
            g = VGroup(Line([SX + 1.5, y1, 0], [SX + 0.2, y1, 0], color=TEXT, stroke_width=3),
                       Line([SX + 1.5, (y1 + y2) / 2, 0], [SX + 0.2, (y1 + y2) / 2, 0], color=TEXT, stroke_width=3))
            if budv.get_value() > 0.02:
                g.add(Line([SX - 2.2, y1 - 0.5, 0], [SX - 0.25, y1 + 0.18, 0], color=TEAL, stroke_width=3))
            return g
        set_updater_group(lines, line_fn)
        self.add(lines, lg)
        self.play(FadeIn(nl), FadeIn(il), tau.animate.set_value(3.35), run_time=0.8, rate_func=linear)
        self.at("one or more leaves")
        panel = Rectangle(width=3.5, height=3.0, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([4.9, 1.6, 0])
        mini = VGroup(Line([4.9, 0.6, 0], [4.9, 2.8, 0], color="#5FA85A", stroke_width=10),
                      Ellipse(width=1.2, height=0.4).set_fill(LEAF, 0.95).set_stroke(width=0).rotate(35 * DEGREES).move_to([5.5, 2.0, 0]),
                      Ellipse(width=1.2, height=0.4).set_fill(LEAF, 0.95).set_stroke(width=0).rotate(-35 * DEGREES).move_to([4.3, 2.0, 0]),
                      Circle(radius=0.12, stroke_width=0).set_fill("#3E7A3A", 1).move_to([4.9, 1.6, 0]))
        mt = T("two leaves per node", 24, TEXT).move_to([4.9, 0.25, 0])
        self.play(FadeIn(panel), FadeIn(mini), FadeIn(mt), tau.animate.set_value(3.55), run_time=0.8, rate_func=linear)
        self.at("with a bud")
        self.play(budv.animate.set_value(1.0), FadeIn(bl), tau.animate.set_value(3.9), run_time=1.6, rate_func=linear)
        self.finish()


class S15Close(SpokenScene):
    def construct(self):
        self.add(soil_rect(OSY))
        oak = make_oak(roots=True)
        K15 = 0.85
        oak.scale(K15, about_point=np.array([OX, OSY, 0]))
        gl = Glows(self, lambda: [np.array([OX + x * K15, OSY + (y - OSY) * K15, 0]) for x, y in OAK_TIPS + [(a, b) for a, b in OAK_ROOT_TIPS]], 0.0)
        self.add(oak)
        self.at("So a plant's new cells")
        self.play(gl.tv.animate.set_value(1.0), run_time=1.2)
        self.at("For a root")
        tag = T("root, steady state, per cell file", 24, TEXT).move_to([3.4, -0.1, 0])
        self.play(FadeIn(tag), run_time=0.6)
        self.at("growth equals")
        r1 = T("growth per hour =", 32, TEXT).move_to([3.4, 2.5, 0])
        self.play(FadeIn(r1), run_time=0.6)
        self.at("new cells per file")
        r2 = T("new cells per file per hour", 30, TEAL).move_to([3.4, 1.75, 0])
        self.play(FadeIn(r2), run_time=0.7)
        self.at("times their final")
        r3 = T("× final cell length", 30, AMBER).move_to([3.4, 1.0, 0])
        self.play(FadeIn(r3), run_time=0.7)
        self.finish()


class S16End(EndCard):
    LINE = "At steady state, root growth = cells per file per hour × final length."
