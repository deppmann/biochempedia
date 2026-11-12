"""How Does a Trunk Get Wider?  (Biochemistrypedia explainer, chapter 2 of the plant-body film pair)

Same colour map as chapter 1: dividing cells TEAL, elongating AMBER, mature GREEN, new leaves light
green. Added here: xylem / wood BROWN-GOLD, phloem VIOLET, cork DARK GREY.
ONE WORLD: the oak (young shoots glow TEAL), then a cross-section disc, then the radial strip cut
from it. The strip is built from one layout function (Strip) so every scene rebuilds it in the same
place; cell widths and counts are schematic.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

AMBER = "#F2A93B"
GRN = "#7BC96F"
SOILC = "#A08060"
LEAF = "#B5E86A"
PALE = "#C8B79A"
BARK = "#6B5642"
WOODC = "#B98A3E"      # xylem / wood
WOODD = "#8E6527"      # latewood (denser)
WOODL = "#E0B35C"      # wood as text
PHLC = "#A77BD8"       # phloem
PHLL = "#C3A2EE"
CORKC = "#4A4F5A"      # cork, dark grey
CORKL = "#B8BEC9"
EPIC = "#8FB08A"
CORTC = "#56665A"
PHELC = "#B7C46A"
DARK = "#241A08"

# ------------------------------------------------------------------ small helpers


def sm(u):
    u = min(max(float(u), 0.0), 1.0)
    return u * u * (3 - 2 * u)


def set_updater_group(grp, fn):
    def upd(m):
        m.submobjects = list(fn().submobjects)
    grp.add_updater(upd)
    upd(grp)


def darker(c, f=0.45):
    return interpolate_color(ManimColor(c), ManimColor("#000000"), f)


class Glows:
    """Pulsing TEAL meristem glows (as in chapter 1)."""

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


def ticker(sc):
    t = ValueTracker(0)
    t.add_updater(lambda m, dt: m.increment_value(dt))
    sc.add(t)
    return t


def make_clock(sc, pos, r=0.8, speed=1.0, label=None):
    t = ticker(sc)
    face = Circle(radius=r, color=TEXT, stroke_width=5).move_to(pos)
    hand = VGroup()

    def fn():
        a = 2 * np.pi * speed * t.get_value() / 4
        return VGroup(Line(pos, pos + [0.72 * r * np.sin(a), 0.72 * r * np.cos(a), 0], color=TEXT, stroke_width=6),
                      Dot(pos, radius=0.07, color=TEXT))
    set_updater_group(hand, fn)
    sc.add(hand)
    return VGroup(face, hand)


def bob_q(sc, pos, size=110):
    q = T("?", size, GOLD, weight=BOLD).move_to(pos)
    t = ticker(sc)
    q.add_updater(lambda m: m.move_to(pos + UP * 0.12 * np.sin(2.2 * t.get_value())))
    return q


# ------------------------------------------------------------------ the oak

SOIL = -2.2
OXT = -3.2
NAIL_Y = SOIL + 1.0
RULER_X = OXT + 1.75
CROWN = [(-1.7, 0.45, 1.2), (1.7, 0.45, 1.2), (0, 1.05, 1.25), (-0.9, -0.1, 1.0), (0.9, -0.1, 1.0)]
ROOT_LINES = [((OXT, SOIL), (OXT, -3.55)), ((OXT, -2.8), (OXT - 1.6, -3.4)), ((OXT, -2.8), (OXT + 1.6, -3.4)),
              ((OXT, -2.55), (OXT - 2.7, -3.1)), ((OXT, -2.55), (OXT + 2.7, -3.1))]


def tgeo(hk, wk):
    yT = 0.3 + 1.1 * hk
    return dict(yT=yT, csc=0.7 + 0.27 * hk, wB=0.5 + 0.9 * wk, wTp=0.3 + 0.55 * wk)


def trunk_hw(y, hk, wk):
    g = tgeo(hk, wk)
    f = min(max((y - SOIL) / (g["yT"] - SOIL), 0), 1)
    return (g["wB"] + (g["wTp"] - g["wB"]) * f) / 2


def branch_lines(hk):
    g = tgeo(hk, 0)
    yT, c = g["yT"], g["csc"]
    a = [OXT, yT - 0.25, 0]
    return [(a, [OXT - 1.5 * c, yT + 0.95 * c, 0]), (a, [OXT + 1.5 * c, yT + 0.95 * c, 0]), (a, [OXT, yT + 1.4 * c, 0])]


def shoot_tips(hk):
    g = tgeo(hk, 0)
    yT, c = g["yT"], g["csc"]
    return [np.array(p, dtype=float) for p in [(OXT, yT + 2.3 * c, 0), (OXT - 2.8 * c, yT + 0.6 * c, 0),
                                                (OXT + 2.8 * c, yT + 0.6 * c, 0), (OXT - 1.3 * c, yT + 1.9 * c, 0),
                                                (OXT + 1.3 * c, yT + 1.9 * c, 0)]]


def root_tips():
    return [np.array([b[0], b[1], 0.0]) for _, b in ROOT_LINES]


def soil_rect(top=SOIL):
    r = Rectangle(width=14.4, height=top + 3.9, stroke_width=0, fill_color=SOILC, fill_opacity=0.16)
    r.move_to([0, (top - 3.9) / 2, 0])
    ln = Line([-7.1, top, 0], [7.1, top, 0], color=SOILC, stroke_width=3)
    return VGroup(r, ln)


class Tree:
    """The oak. hk = height growth 0-1, wk = trunk width 0-1, tr = trunk translucency, al = opacity."""

    def __init__(s, sc, hk=0.0, wk=0.0, tr=0.0, al=1.0, roots=True):
        s.hk, s.wk, s.tr, s.al, s.roots = ValueTracker(hk), ValueTracker(wk), ValueTracker(tr), ValueTracker(al), roots
        s.grp = VGroup()
        set_updater_group(s.grp, s.build)
        sc.add(s.grp)

    def build(s):
        hk, wk, tr, al = s.hk.get_value(), s.wk.get_value(), s.tr.get_value(), s.al.get_value()
        g = tgeo(hk, wk)
        yT, c = g["yT"], g["csc"]
        out = VGroup()
        if s.roots:
            for a, b in ROOT_LINES:
                out.add(Line([*a, 0], [*b, 0], color=PALE, stroke_width=7).set_opacity(1 - 0.5 * tr))
        for a, b in branch_lines(hk):
            out.add(Line(a, b, color=BARK, stroke_width=10).set_opacity(1 - 0.45 * tr))
        out.add(Polygon([OXT - g["wB"] / 2, SOIL, 0], [OXT - g["wTp"] / 2, yT, 0], [OXT + g["wTp"] / 2, yT, 0],
                        [OXT + g["wB"] / 2, SOIL, 0], stroke_width=0, fill_color=BARK, fill_opacity=1 - 0.72 * tr))
        crown = VGroup(*[Circle(radius=r * c).move_to([OXT + x * c, yT + y * c, 0]) for x, y, r in CROWN])
        crown.set_fill("#35553A", 0.95).set_stroke("#4F7A52", 2)
        out.add(crown)
        if al < 0.999:
            for m in out.family_members_with_points():
                m.set_fill(opacity=m.get_fill_opacity() * al)
                m.set_stroke(opacity=m.get_stroke_opacity() * al)
        return out


class Nail:
    def __init__(s, sc, tree, d=1.0):
        s.d, s.tree = ValueTracker(d), tree
        s.grp = VGroup()
        set_updater_group(s.grp, s.build)
        sc.add(s.grp)

    def build(s):
        hw = trunk_hw(NAIL_Y, s.tree.hk.get_value(), s.tree.wk.get_value())
        ex = OXT + hw
        out_len = 0.12 + 0.55 * (1 - s.d.get_value())
        return VGroup(Line([ex - 0.12, NAIL_Y, 0], [ex + out_len, NAIL_Y, 0], color="#D0D4DC", stroke_width=7),
                      Rectangle(width=0.07, height=0.34, stroke_width=0, fill_color="#D0D4DC", fill_opacity=1).move_to([ex + out_len, NAIL_Y, 0]))


def make_ruler():
    bar = Line([RULER_X, SOIL, 0], [RULER_X, NAIL_Y, 0], color=TEXT, stroke_width=5)
    ticks = VGroup(*[Line([RULER_X - 0.12, SOIL + 0.25 * i, 0], [RULER_X + 0.12, SOIL + 0.25 * i, 0], color=TEXT, stroke_width=4)
                     for i in range(5)])
    lab = M("1 m", 32, TEXT).move_to([RULER_X + 0.85, NAIL_Y, 0])
    return VGroup(bar, ticks), lab


# ------------------------------------------------------------------ cross-section disc

DISC_C = np.array([3.0, -0.5, 0])


def make_disc(c=DISC_C, sc=1.0):
    wood = Circle(radius=1.5 * sc, stroke_width=0, fill_color=WOODC, fill_opacity=0.95)
    texture = VGroup(*[Circle(radius=r * sc, stroke_width=2, stroke_color=WOODD) for r in (0.45, 0.9, 1.3)])
    cam = Annulus(inner_radius=1.5 * sc, outer_radius=1.66 * sc, stroke_width=0, fill_color=TEAL, fill_opacity=1)
    phl = Annulus(inner_radius=1.66 * sc, outer_radius=1.9 * sc, stroke_width=0, fill_color=PHLC, fill_opacity=1)
    cork = Annulus(inner_radius=1.9 * sc, outer_radius=2.02 * sc, stroke_width=0, fill_color=CORKC, fill_opacity=1)
    g = VGroup(wood, texture, cam, phl, cork).move_to(c)
    g.cam = cam
    return g


def ring_pulse(sc, mob, color=TEAL):
    t = ticker(sc)
    ring = mob.copy().set_fill(opacity=0).set_stroke(color, 6, opacity=0.0)
    ring.add_updater(lambda m: m.set_stroke(color, 4 + 4 * np.sin(2 * t.get_value()) ** 2, opacity=0.35 + 0.35 * np.sin(2 * t.get_value()) ** 2))
    return ring


# ------------------------------------------------------------------ the radial strip

RH, RG = 0.7, 0.05
WID = {"F": 0.4, "E": 0.6, "L": 0.2, "T": 0.4, "P": 0.4, "C": 0.15, "EPI": 0.12, "H": 0.15, "K": 0.15, "X": 0.22}
FILL = {"F": WOODC, "E": WOODC, "L": WOODD, "T": TEAL, "P": PHLC, "C": CORTC, "EPI": EPIC, "H": PHELC, "K": TEAL, "X": CORKC}
OLD_N = 22


def mkcol(xl, w, kind, k=1.0):
    """One column of cells (three rows) with its left edge at xl and width w (already scaled)."""
    col = VGroup()
    rh = RH * k
    for j in (-1, 0, 1):
        y = j * (RH + RG) * k
        r = RoundedRectangle(corner_radius=0.04 * k, width=max(w - 0.035 * k, 0.03), height=rh, stroke_width=1.6,
                             stroke_color=darker(FILL[kind], 0.5), fill_color=FILL[kind], fill_opacity=0.95)
        r.move_to([xl + w / 2, y, 0])
        col.add(r)
        if kind == "E":
            col.add(Ellipse(width=w * 0.6, height=rh * 0.68, stroke_width=0, fill_color=BG, fill_opacity=0.95).move_to([xl + w / 2, y, 0]))
        elif kind == "L":
            col.add(Ellipse(width=w * 0.3, height=rh * 0.3, stroke_width=0, fill_color=BG, fill_opacity=0.9).move_to([xl + w / 2, y, 0]))
    col.kind, col.xl, col.w = kind, xl, w
    return col


def ring_kinds():
    return list("EELLLL")


class Strip:
    """The radial strip: wood (inner, left) | cambium | phloem | cortex | epidermis (or periderm).
    cam_left is where the cambium column starts; wood is packed leftwards from it."""

    def __init__(s, sc, extras="", nphl=4, cam_left=2.5, k=1.0, peri=False, bnd=0, pulse=True, add=True):
        s.sc, s.k, s.cam_left = sc, k, cam_left
        kinds = ["F"] * OLD_N + list(extras)
        x = cam_left
        cols = []
        for kd in reversed(kinds):
            w = WID[kd] * k
            x -= w
            cols.append((x, w, kd))
        cols.reverse()
        s.wood = VGroup(*[mkcol(x, w, kd, k) for x, w, kd in cols if x + w > -7.2])
        # annual-ring boundaries: the left edge of each earlywood run that follows latewood
        s.bnd = VGroup()
        edges = [x for (x, w, kd), prev in zip(cols[1:], cols[:-1]) if kd == "E" and prev[2] == "L"]
        for xe in edges[:bnd] if bnd >= 0 else edges:
            s.bnd.add(s.bline(xe))
        s.cam = mkcol(cam_left, WID["T"] * k, "T", k)
        x = cam_left + WID["T"] * k
        s.phl = VGroup(*[mkcol(x + i * WID["P"] * k, WID["P"] * k, "P", k) for i in range(nphl)])
        x += nphl * WID["P"] * k
        s.ctx, s.epi, s.phe, s.ckc, s.cork = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
        if not peri:
            s.ctx = VGroup(*[mkcol(x + i * WID["C"] * k, WID["C"] * k, "C", k) for i in range(4)])
            x += 4 * WID["C"] * k
            s.epi = mkcol(x, WID["EPI"] * k, "EPI", k)
        else:
            s.ctx = VGroup(*[mkcol(x + i * WID["C"] * k, WID["C"] * k, "C", k) for i in range(2)])
            x += 2 * WID["C"] * k
            s.phe = mkcol(x, WID["H"] * k, "H", k)
            x += WID["H"] * k
            s.ckc = mkcol(x, WID["K"] * k, "K", k)
            x += WID["K"] * k
            s.cork = VGroup(*[mkcol(x + i * WID["X"] * k, WID["X"] * k, "X", k) for i in range(4)])
        s.x_end = x
        s.woodgrp = VGroup(s.wood, s.bnd)
        s.outer = VGroup(s.phl, s.ctx, s.epi, s.phe, s.ckc, s.cork)
        s.all = VGroup(s.woodgrp, s.cam, s.outer)
        s.pt = ticker(sc)
        s.glow_on = ValueTracker(1.0 if pulse else 0.0)
        s.pulse = VGroup()
        set_updater_group(s.pulse, s.build_pulse)
        if add:
            sc.add(s.all, s.pulse)

    def bline(s, x):
        return Line([x, -1.22 * s.k, 0], [x, 1.22 * s.k, 0], color="#FFFFFF", stroke_width=4).set_opacity(0.9)

    def build_pulse(s):
        a = s.glow_on.get_value()
        g = VGroup()
        if a < 0.02:
            return g
        ph = 0.5 + 0.5 * np.sin(2.4 * s.pt.get_value())
        r = SurroundingRectangle(s.cam, color=TEAL, buff=0.05, corner_radius=0.06, stroke_width=3 + 3 * ph)
        r.set_stroke(opacity=a * (0.3 + 0.6 * ph))
        g.add(r)
        return g


def sugar_dots(sc, xl, xr, n=11, speed=0.6, ylim=1.12):
    rng = np.random.RandomState(3)
    grp = VGroup(*[Dot([rng.uniform(xl, xr), rng.uniform(-ylim, ylim), 0], radius=0.055, color="#FFD27A") for _ in range(n)])

    def mv(m, dt):
        for d in m:
            d.shift(DOWN * speed * dt)
            if d.get_y() < -ylim:
                d.shift(UP * 2 * ylim)
    grp.add_updater(mv)
    sc.add(grp)
    return grp


# ----- strip actions (shared by several scenes)

def unlist(sc, m):
    """Drop m from the scene's top-level list only (it now lives inside a group that is already in the scene)."""
    sc.mobjects = [x for x in sc.mobjects if x is not m]


def div_start(sc, st, run=0.7):
    """The cambium column doubles in width, pushing everything outside it outward."""
    w = WID["T"] * st.k
    cleft = VGroup(*[Line([st.cam_left + w, y - RH * st.k / 2, 0], [st.cam_left + w, y + RH * st.k / 2, 0], color=BG, stroke_width=6)
                     for y in [j * (RH + RG) * st.k for j in (-1, 0, 1)]])
    sc.play(st.cam.animate.stretch(2, 0, about_edge=LEFT), st.outer.animate.shift(RIGHT * w), run_time=run)
    sc.play(Create(cleft), run_time=0.3)
    return cleft


def div_finish_inward(sc, st, cleft, run=0.7, extra=()):
    w = WID["T"] * st.k
    d = mkcol(st.cam_left, w, "T", st.k)
    sc.add(d)
    sc.play(st.cam.animate.stretch(0.5, 0, about_edge=RIGHT), FadeOut(cleft), *extra, run_time=0.4)
    sc.play(*[r.animate.set_fill(WOODC, 0.95).set_stroke(darker(WOODC, 0.5)) for r in d], run_time=run)
    st.wood.add(d)
    unlist(sc, d)
    st.cam_left += w
    return d


def div_finish_outward(sc, st, cleft, run=0.7, extra=()):
    w = WID["T"] * st.k
    e = mkcol(st.cam_left + w, w, "T", st.k)
    sc.add(e)
    sc.play(st.cam.animate.stretch(0.5, 0, about_edge=LEFT), FadeOut(cleft), *extra, run_time=0.4)
    sc.play(*[r.animate.set_fill(PHLC, 0.95).set_stroke(darker(PHLC, 0.5)) for r in e], run_time=run)
    st.phl.add(e)
    unlist(sc, e)
    return e


def add_wood(sc, st, kind, run=0.3):
    """Conveyor: the cambium stays put, the wood slides inward and a new cell grows beside the cambium."""
    w = WID[kind] * st.k
    cell = mkcol(st.cam_left - w, w, kind, st.k)
    sc.play(st.woodgrp.animate.shift(LEFT * w), GrowFromEdge(cell, RIGHT), run_time=run, rate_func=smooth)
    st.wood.add(cell)
    unlist(sc, cell)


def add_year(sc, st, total, extra=None):
    per = total / 6.0
    for kd in ring_kinds():
        add_wood(sc, st, kd, run=per)


class Dial:
    COL = ["#7BC96F", "#F2C14E", "#C0763A", "#7FA6D8"]   # spring, summer, autumn, winter (clockwise from the top-right)

    def __init__(s, sc, pos, ang=45, r=1.5):
        s.pos, s.r = np.array(pos, dtype=float), r
        s.ang = ValueTracker(ang)
        segs = VGroup(*[AnnularSector(inner_radius=0, outer_radius=r, angle=-PI / 2, start_angle=PI / 2 - i * PI / 2,
                                      fill_color=c, fill_opacity=0.45, stroke_width=2, stroke_color=TEXT).move_to(s.pos + [r / 2 * (1 if i < 2 else -1) * 0.0, 0, 0])
                        for i, c in enumerate(s.COL)])
        s.base = VGroup(*[Sector(radius=r, start_angle=PI / 2 - (i + 1) * PI / 2, angle=PI / 2, arc_center=s.pos, fill_color=c, fill_opacity=0.5,
                                 stroke_width=2, stroke_color=TEXT) for i, c in enumerate(s.COL)])
        s.names = VGroup(*[T(n, 22, TEXT).move_to(s.pos + (0.63 * r) * np.array([np.sin(np.radians(a)), np.cos(np.radians(a)), 0]))
                           for n, a in (("spring", 45), ("summer", 135), ("winter", 315))])
        s.mark = s.build()
        s.mark.add_updater(lambda m: m.become(s.build()))
        s.grp = VGroup(s.base, s.names, s.mark)
        sc.add(s.mark)

    def build(s):
        a = np.radians(s.ang.get_value())
        d = np.array([np.sin(a), np.cos(a), 0])
        tri = Triangle(color=TEXT, fill_opacity=1, stroke_width=0).scale(0.17)
        tri.rotate(-a + PI)   # point inward
        tri.move_to(s.pos + d * (s.r + 0.2))
        return tri


# ------------------------------------------------------------------ states of the strip (one place)
# S5: start of the strip scenes.  S7: after the two inward divisions and one outward one.
S5 = dict(extras="", nphl=4, cam_left=2.5)
S7 = dict(extras="", nphl=5, cam_left=3.3)
S7_PAN = -2.1
RINGS_CAM = 1.2
RING1 = dict(extras="FF" + "".join(ring_kinds()), nphl=5, cam_left=RINGS_CAM)


def ring_state(n, bnd=0):
    return dict(extras="FF" + "".join(ring_kinds()) * n, nphl=5, cam_left=RINGS_CAM, bnd=bnd)


# ------------------------------------------------------------------ scenes

class S00Title(TitleCard):
    TITLE = "How Does a Trunk Get Wider?"
    LESSON = "Plant Body and Growth"


class S01Hook(SpokenScene):
    def construct(self):
        self.add(soil_rect())
        tree = Tree(self, 0, 0, al=0.0)
        gl = Glows(self, lambda: shoot_tips(tree.hk.get_value()) + root_tips(), 0.0)
        self.play(tree.al.animate.set_value(1.0), run_time=1.0)
        self.at("growth in length")
        self.play(gl.tv.animate.set_value(1.0), run_time=1.0)
        self.at("so drive")
        self.play(gl.tv.animate.set_value(0.0), run_time=0.4)
        nail = Nail(self, tree, d=0.0)
        ex = OXT + trunk_hw(NAIL_Y, 0, 0)
        hc = ex + 0.12 + 0.55 + 0.21
        hammer = VGroup(Line([hc + 0.1, NAIL_Y, 0], [hc + 1.2, NAIL_Y + 0.9, 0], color=PALE, stroke_width=9),
                        Rectangle(width=0.32, height=0.62, stroke_width=0, fill_color=CORKL, fill_opacity=1).move_to([hc, NAIL_Y, 0]))
        self.play(FadeIn(hammer, shift=LEFT * 0.3), run_time=0.3)
        self.at("nail")
        for i in range(1, 4):
            after = ex + 0.12 + 0.55 * (1 - i / 3)
            sh = hc - (after + 0.2)
            self.play(hammer.animate.shift(LEFT * sh), nail.d.animate.set_value(i / 3), run_time=0.2)
            self.play(hammer.animate.shift(RIGHT * (sh if i < 3 else sh * 0.4)), run_time=0.22)
        self.at("meter")
        ruler, lab = make_ruler()
        self.play(Create(ruler), FadeIn(lab), FadeOut(hammer), run_time=0.9)
        self.at("how high")
        clk = make_clock(self, np.array([3.4, 1.7, 0]), r=0.85, speed=2.0)
        self.play(FadeIn(clk), run_time=0.6)
        t = T("20 years later?", 36, TEXT).move_to([3.4, 0.35, 0])
        self.at("many years")
        self.play(FadeIn(t, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S02Pause(NarratedScene):
    def construct(self):
        self.add(soil_rect())
        tree = Tree(self, 0, 0)
        Nail(self, tree, d=1.0)
        ruler, lab = make_ruler()
        self.add(ruler, lab)
        self.add(make_clock(self, np.array([3.4, 1.7, 0]), r=0.85, speed=0.5))
        self.add(T("20 years later?", 36, TEXT).move_to([3.4, 0.35, 0]))
        self.add(bob_q(self, np.array([RULER_X + 2.9, NAIL_Y + 0.05, 0]), 110))
        self.finish()




def drive(sc, tr, target, dur, smooth_=True):
    """Move a ValueTracker to target over dur seconds while the scene carries on (no blocking play)."""
    sc.add(tr)
    s0, t = tr.get_value(), [0.0]

    def upd(m, dt):
        t[0] += dt
        u = min(t[0] / dur, 1.0)
        m.set_value(s0 + (target - s0) * (sm(u) if smooth_ else u))
        if u >= 1:
            m.remove_updater(upd)
    tr.add_updater(upd)


def fade_line(a, b, col=TEAL, w=6, keep=0.55, n=8):
    """A line that fades to nothing before its far end (the cambium stops short of the tips)."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    g = VGroup()
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        op = 1.0 if u1 <= keep else max(0.0, 1 - (u1 - keep) / (1 - keep + 1e-6))
        if op > 0.02:
            g.add(Line(a + (b - a) * u0, a + (b - a) * u1, color=col, stroke_width=w).set_opacity(op))
    return g


def col_pulse(sc, mob, color=TEAL, buff=0.05):
    t = ticker(sc)
    r = VGroup()

    def fn():
        ph = 0.5 + 0.5 * np.sin(2.4 * t.get_value())
        x = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.06, stroke_width=3 + 3 * ph)
        x.set_stroke(opacity=0.3 + 0.6 * ph)
        return VGroup(x)
    set_updater_group(r, fn)
    sc.add(r)
    return r


def recolor(col, color):
    return [r.animate.set_fill(color, 0.95).set_stroke(darker(color, 0.5)) for r in col if isinstance(r, RoundedRectangle)]


def eq_lines():
    l1 = T("growth per hour =", 34, TEXT).move_to([0, 3.4, 0])
    p1 = T("new cells per file per hour", 30, TEAL)
    x = T("×", 30, TEXT)
    p3 = T("final cell length", 30, AMBER)
    row = VGroup(p1, x, p3).arrange(RIGHT, buff=0.3).move_to([0, 2.7, 0])
    u1 = Line(p1.get_corner(DL) + DOWN * 0.08, p1.get_corner(DR) + DOWN * 0.08, color=TEAL, stroke_width=5)
    u3 = Line(p3.get_corner(DL) + DOWN * 0.08, p3.get_corner(DR) + DOWN * 0.08, color=AMBER, stroke_width=5)
    return l1, p1, x, p3, u1, u3


def side_labels(st):
    centre = T("centre", 30, TEXT).move_to([-5.9, 1.85, 0])
    return centre


class S03Reveal(SpokenScene):
    def construct(self):
        self.add(soil_rect())
        tree = Tree(self, 0, 0)
        Nail(self, tree, d=1.0)
        ruler, lab = make_ruler()
        self.add(ruler, lab)
        gl = Glows(self, lambda: shoot_tips(tree.hk.get_value()), 0.0)
        clk = make_clock(self, np.array([5.9, 3.0, 0]), r=0.6, speed=2.0)
        self.add(clk, T("20 years", 32, TEXT).move_to([4.35, 3.0, 0]))
        drive(self, tree.hk, 1.0, 6.0, smooth_=False)
        self.at("still")
        dash = DashedLine([RULER_X + 1.55, NAIL_Y, 0], [6.2, NAIL_Y, 0], color=TEXT, stroke_width=4)
        same = T("still 1 m", 32, TEXT).move_to([3.5, NAIL_Y - 0.5, 0])
        self.play(Create(dash), FadeIn(same), run_time=0.8)
        self.at("that part")
        stop = T("stopped lengthening", 30, TEXT).move_to([3.3, -0.35, 0])
        sa = Arrow([1.0, -0.35, 0], [OXT + trunk_hw(-0.35, 1, 0) + 0.1, -0.35, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.22)
        self.play(FadeIn(stop), GrowArrow(sa), run_time=0.7)
        self.at("a tree gets taller")
        self.play(FadeOut(stop), FadeOut(sa), FadeOut(same), FadeOut(dash), gl.tv.animate.set_value(1.0), run_time=0.8)
        yl = T("young shoots", 32, TEAL).move_to([2.4, 2.35, 0])
        ya = Arrow([1.0, 2.3, 0], [-0.25, 2.1, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.22)
        self.at("young shoots")
        self.play(FadeIn(yl), GrowArrow(ya), run_time=0.7)
        self.at("but the trunk")
        self.play(FadeOut(yl), FadeOut(ya), gl.tv.animate.set_value(0.0), run_time=0.5)
        drive(self, tree.wk, 1.0, 1.8)
        la = Arrow([-3.8, -0.4, 0], [-4.8, -0.4, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.24)
        ra = Arrow([-2.5, -0.4, 0], [-1.5, -0.4, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.24)
        wl = T("wider", 36, TEXT).move_to([-0.2, -0.4, 0])
        self.wait(0.6)
        self.play(GrowArrow(la), GrowArrow(ra), FadeIn(wl), run_time=0.9)
        self.finish()


def trunk_state():
    return dict(hk=1.0, wk=1.0)


class S04Cambium(SpokenScene):
    def construct(self):
        self.add(soil_rect())
        tree = Tree(self, 1.0, 1.0)
        g = tgeo(1, 1)
        yT = g["yT"]
        self.add(ticker(self))
        drive(self, tree.tr, 1.0, 1.4)
        pt = ticker(self)
        cyl = Polygon([OXT - g["wB"] / 2 + 0.13, SOIL + 0.03, 0], [OXT - g["wTp"] / 2 + 0.1, yT - 0.03, 0],
                      [OXT + g["wTp"] / 2 - 0.1, yT - 0.03, 0], [OXT + g["wB"] / 2 - 0.13, SOIL + 0.03, 0], color=TEAL, fill_opacity=0.0)
        cyl.add_updater(lambda m: m.set_stroke(TEAL, 5 + 2 * np.sin(2.4 * pt.get_value()), opacity=0.8 + 0.2 * np.sin(2.4 * pt.get_value())))
        self.at("cylinder")
        self.play(Create(cyl, run_time=1.6))
        gl = Glows(self, lambda: [np.array([OXT + sgn * (trunk_hw(y, 1, 1) - 0.12), y, 0.0]) for y in (-1.6, -0.5, 0.6) for sgn in (-1, 1)], 0.0)
        self.play(gl.tv.animate.set_value(0.45), run_time=0.5)
        l1 = T("vascular cambium", 32, TEAL).move_to([3.0, 3.25, 0])
        l2 = T("(lateral meristem)", 30, TEAL).move_to([3.0, 2.7, 0])
        self.at("vascular cambium")
        a1 = Arrow([0.9, 3.0, 0], [OXT + 0.45, 0.9, 0], buff=0.05, color=TEAL, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(l1), GrowArrow(a1), run_time=0.8)
        disc = make_disc()
        ring = ring_pulse(self, disc.cam)
        self.at("it lies between")
        self.play(FadeOut(a1), FadeIn(disc, scale=0.85), run_time=0.9)
        self.add(ring)
        xl = T("xylem", 32, DARK, weight=BOLD).move_to(DISC_C)
        self.at("xylem")
        self.play(FadeIn(xl), run_time=0.5)
        pl = T("phloem", 32, PHLL).move_to([3.0, -3.25, 0])
        pa = Arrow([3.0, -2.95, 0], [3.0, -2.3, 0], buff=0, color=PHLL, stroke_width=4, tip_length=0.2)
        self.at("phloem")
        self.play(FadeIn(pl), GrowArrow(pa), run_time=0.6)
        self.at("lateral meristem")
        self.play(FadeIn(l2), run_time=0.6)
        self.at("running along")
        self.play(FadeOut(l2), FadeOut(l1), run_time=0.4)
        lines = VGroup()
        for a, b in branch_lines(1.0):
            lines.add(fade_line(a, b, keep=0.6, w=5))
        for a, b in ROOT_LINES:
            lines.add(fade_line([*a, 0], [*b, 0], keep=0.6, w=5))
        lines.add(fade_line([OXT, yT - 0.05, 0], [OXT, yT + 0.4, 0], keep=0.9, w=5))
        self.play(LaggedStart(*[Create(m) for m in lines], lag_ratio=0.15, run_time=2.0))
        lt = T("fades out before the tips", 28, TEAL).move_to([3.0, 3.2, 0])
        self.finish()


class S05Strip(SpokenScene):
    def construct(self):
        disc = make_disc()
        ring = ring_pulse(self, disc.cam)
        self.add(disc, ring)
        self.at("thin strip")
        slice_ = Rectangle(width=2.02, height=0.26, stroke_color=TEXT, stroke_width=5, fill_opacity=0).move_to([DISC_C[0] + 1.01, DISC_C[1], 0])
        self.play(Create(slice_), run_time=0.8)
        st = Strip(self, add=False, **S5)
        bar = Rectangle(width=st.x_end + 6.3 + 0.1, height=2.4, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([(st.x_end - 6.3) / 2, 0, 0])
        self.at("out to its surface")
        self.play(FadeOut(disc), FadeOut(ring), ReplacementTransform(slice_, bar), run_time=0.9)
        self.play(FadeIn(st.all), FadeOut(bar), run_time=0.8)
        self.add(st.pulse)
        centre = T("centre", 30, TEXT).move_to([-5.9, 1.85, 0])
        surf = T("surface", 30, TEXT).move_to([5.2, 1.85, 0])
        sch = T("schematic: cell sizes and counts not to scale", 22, TEXT).move_to([0, -3.5, 0])
        self.play(FadeIn(centre), FadeIn(surf), FadeIn(sch), run_time=0.7)
        gl = Glows(self, lambda: [np.array([2.7, y, 0.0]) for y in (-0.75, 0, 0.75)], 0.0)
        self.at("the vascular cambium")
        self.add(gl.t)
        cl = T("vascular cambium", 32, TEAL).move_to([2.7, -2.2, 0])
        ca = Arrow([2.7, -1.85, 0], [2.7, -1.25, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.22)
        self.play(FadeIn(cl), GrowArrow(ca), gl.tv.animate.set_value(0.4), run_time=0.8)
        self.finish()


S6 = dict(extras="FF", nphl=4, cam_left=3.3)


class S06Inward(SpokenScene):
    def construct(self):
        st = Strip(self, **S5)
        centre = T("centre", 30, TEXT).move_to([-5.9, 1.85, 0])
        surf = T("surface", 30, TEXT).move_to([5.2, 1.85, 0])
        self.add(centre)
        st.outer.add(surf)
        self.add(surf)
        self.at("divides")
        cl = div_start(self, st)
        self.at("inward")
        arr = Arrow([st.cam_left + 0.6, 1.6, 0], [st.cam_left - 0.9, 1.6, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.28)
        self.play(GrowArrow(arr), run_time=0.3)
        d = div_finish_inward(self, st, cl, extra=[FadeOut(arr)])
        self.at("they become")
        lab = T("secondary xylem = wood", 32, WOODL).move_to([0.5, -2.1, 0])
        self.play(FadeIn(lab), run_time=0.4)
        cl2 = div_start(self, st, run=0.5)
        d2 = div_finish_inward(self, st, cl2, run=0.5)
        blk = SurroundingRectangle(VGroup(*st.wood[-4:]), color=WOODL, buff=0.07, stroke_width=5, corner_radius=0.08)
        self.play(Create(blk), run_time=0.5)
        self.at("which is wood")
        self.play(Indicate(lab, color=WOODL, scale_factor=1.08), run_time=0.8)
        self.finish()


class S07Outward(SpokenScene):
    def construct(self):
        st = Strip(self, **S6)
        centre = T("centre", 30, TEXT).move_to([-5.9, 1.85, 0])
        self.add(centre)
        self.at("other daughters")
        cl = div_start(self, st)
        self.at("outward")
        arr = Arrow([st.cam_left + 0.2, 1.6, 0], [st.cam_left + 1.7, 1.6, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.28)
        self.play(GrowArrow(arr), run_time=0.3)
        e = div_finish_outward(self, st, cl, extra=[FadeOut(arr)])
        self.at("secondary phloem")
        box = SurroundingRectangle(st.phl, color=PHLC, buff=0.07, stroke_width=5, corner_radius=0.08)
        lab = T("secondary phloem", 32, PHLL).move_to([4.7, -2.1, 0])
        self.play(Create(box), FadeIn(lab), run_time=0.8)
        self.at("the tissue that carries")
        xl = st.phl[-1].get_right()[0]
        dots = sugar_dots(self, st.cam_left + 0.4 + 0.05, xl - 0.05)
        sl = T("sugars from the leaves\nto the rest of the plant", 28, "#FFD27A").move_to([4.0, 2.2, 0])
        self.play(FadeIn(sl), run_time=0.8)
        self.finish()


class S08Seasons(SpokenScene):
    def construct(self):
        st = Strip(self, **S7)
        dial = Dial(self, [5.15, 2.3, 0], ang=45)
        self.add(T("centre", 30, TEXT).move_to([-5.9, 1.85, 0]))
        st_centre = self.mobjects[-1]
        self.play(st.all.animate.shift(RIGHT * S7_PAN), FadeOut(st_centre), FadeIn(dial.base), FadeIn(dial.names), run_time=1.4)
        st.cam_left = RINGS_CAM
        self.at("the cambium works")
        drive(self, dial.ang, 135, 2.2)
        self.wait(2.0)
        self.at("rests in winter")
        drive(self, dial.ang, 315, 0.9)
        rest = T("rests", 32, "#7FA6D8").move_to([RINGS_CAM + 0.2, 1.85, 0])
        self.play(FadeIn(rest), st.glow_on.animate.set_value(0.0), *[r.animate.set_fill(opacity=0.3) for r in st.cam if isinstance(r, RoundedRectangle)], run_time=0.8)
        self.at("spring wood")
        drive(self, dial.ang, 45, 0.7)
        self.play(FadeOut(rest), st.glow_on.animate.set_value(1.0), *[r.animate.set_fill(opacity=0.95) for r in st.cam if isinstance(r, RoundedRectangle)], run_time=0.5)
        add_wood(self, st, "E", 0.55)
        add_wood(self, st, "E", 0.55)
        el = T("earlywood: large vessels", 30, WOODL).move_to([-0.2, 1.8, 0])
        self.play(FadeIn(el), run_time=0.5)
        self.at("late summer wood")
        drive(self, dial.ang, 120, 0.6)
        for _ in range(4):
            add_wood(self, st, "L", 0.33)
        ll = T("latewood: smaller vessels", 30, WOODL).move_to([0.6, -1.85, 0])
        self.play(FadeIn(ll), run_time=0.5)
        self.finish()


class S09Ring(SpokenScene):
    def construct(self):
        st = Strip(self, **ring_state(1))
        dial = Dial(self, [5.15, 2.3, 0], ang=120)
        self.add(dial.base, dial.names)
        self.at("where one")
        drive(self, dial.ang, 45, 0.5)
        add_wood(self, st, "E", 0.5)
        add_wood(self, st, "E", 0.5)
        drive(self, dial.ang, 120, 0.7)
        for _ in range(4):
            add_wood(self, st, "L", 0.3)
        self.at("a line appears")
        x2 = st.cam_left - 2.0
        ln = st.bline(x2)
        self.play(Create(ln), run_time=0.5)
        st.bnd.add(ln)
        ring_lab = T("annual ring", 32, TEXT).move_to([x2, -1.85, 0])
        self.at("appears")
        self.play(FadeIn(ring_lab), run_time=0.5)
        st.bnd.add(ring_lab)
        drive(self, dial.ang, 45, 0.4)
        for kd in ring_kinds():
            add_wood(self, st, kd, 0.24)
        ln3 = st.bline(st.cam_left - 2.0)
        self.add(ln3)
        st.bnd.add(ln3)
        self.at("each year usually")
        drive(self, dial.ang, 120, 1.2)
        for kd in ring_kinds():
            add_wood(self, st, kd, 0.2)
        ln4 = st.bline(st.cam_left - 2.0)
        self.add(ln4)
        st.bnd.add(ln4)
        self.at("one ring")
        ul = T("usually one per year", 32, TEXT).move_to([-2.0, 1.85, 0])
        self.play(FadeIn(ul), run_time=0.6)
        self.finish()


class S10Cork(SpokenScene):
    def construct(self):
        st = Strip(self, **ring_state(4, 3))
        self.play(st.all.animate.scale(1.25, about_point=[RINGS_CAM, 0, 0]).shift(LEFT * 0.9), run_time=1.6)
        epi, ctx = st.epi, st.ctx
        ex = epi.get_center()[0]
        self.at("its old skin")
        el = T("epidermis", 30, EPIC).move_to([ex, 1.95, 0])
        ea = Arrow([ex, 1.65, 0], [ex, 1.45, 0], buff=0, color=EPIC, stroke_width=4, tip_length=0.15)
        self.play(FadeIn(el), GrowArrow(ea), run_time=0.7)
        self.at("splits")
        self.play(epi[0].animate.rotate(0.5).shift(UP * 0.17 + RIGHT * 0.1), epi[1].animate.rotate(-0.35).shift(RIGHT * 0.13),
                  epi[2].animate.rotate(0.45).shift(DOWN * 0.15 + RIGHT * 0.08), run_time=0.9)
        self.at("a second lateral meristem")
        ck = ctx[3]
        self.play(FadeOut(el), FadeOut(ea), Indicate(ck, color=TEAL, scale_factor=1.25), run_time=0.9)
        self.at("the cork cambium")
        cx = ck.get_center()[0]
        self.play(*recolor(ck, TEAL), run_time=0.7)
        cp = col_pulse(self, ck)
        kl = T("cork cambium", 32, TEAL).move_to([cx, 2.15, 0])
        ka = Arrow([cx, 1.85, 0], [cx, 1.45, 0], buff=0, color=TEAL, stroke_width=4, tip_length=0.15)
        self.play(FadeIn(kl), GrowArrow(ka), run_time=0.6)
        self.at("usually forms just beneath")
        self.play(Indicate(epi, color=EPIC, scale_factor=1.2), run_time=1.0)
        self.at("outward it makes cork")
        x0 = ck.get_right()[0]
        w = WID["X"] * 1.25
        cork = VGroup(*[mkcol(x0 + i * w, w, "X", 1.25) for i in range(4)])
        flake = [m.animate.shift(RIGHT * (1.5 + 0.2 * i) + UP * (0.5 - 0.5 * i)).rotate(0.6 - 0.5 * i).set_opacity(0) for i, m in enumerate(epi)]
        self.play(AnimationGroup(*flake, run_time=2.4), LaggedStart(*[GrowFromEdge(c, LEFT) for c in cork], lag_ratio=0.5, run_time=2.2))
        self.at("waterproofed walls")
        kw = T("cork:\nwaterproofed walls", 30, CORKL).move_to([4.95, -2.2, 0])
        kwa = Arrow([x0 + 2 * w, -1.8, 0], [x0 + 2 * w, -1.45, 0], buff=0, color=CORKL, stroke_width=4, tip_length=0.15)
        self.play(*[r.animate.set_stroke(CORKL, 5) for c in cork for r in c if isinstance(r, RoundedRectangle)], FadeIn(kw), GrowArrow(kwa), run_time=1.2)
        self.at("inward it makes")
        ph = ctx[2]
        self.play(*recolor(ph, PHELC), run_time=0.8)
        pcx = ph.get_center()[0]
        self.at("the falloderm")
        pl = T("phelloderm", 30, PHELC).move_to([pcx - 2.3, -2.15, 0])
        pa = Arrow([pcx - 1.5, -1.9, 0], [pcx - 0.05, -1.45, 0], buff=0, color=PHELC, stroke_width=4, tip_length=0.15)
        self.play(FadeIn(pl), GrowArrow(pa), run_time=0.7)
        self.at("cork cork cambium")
        self.play(FadeOut(kl), FadeOut(ka), Indicate(cork, color=CORKL, scale_factor=1.15), run_time=0.5)
        self.at("cork cambium and falloderm")
        self.play(Indicate(ck, color=TEAL, scale_factor=1.4), run_time=0.5)
        self.at("and falloderm")
        self.play(Indicate(ph, color=PHELC, scale_factor=1.4), run_time=0.5)
        self.at("together form")
        xa, xb = ph.get_left()[0], cork[-1].get_right()[0]
        br = VGroup(Line([xa, 1.55, 0], [xb, 1.55, 0], color=TEXT, stroke_width=5), Line([xa, 1.55, 0], [xa, 1.4, 0], color=TEXT, stroke_width=5),
                    Line([xb, 1.55, 0], [xb, 1.4, 0], color=TEXT, stroke_width=5))
        self.play(Create(br), run_time=0.5)
        self.at("form the periderm")
        pd = T("periderm", 36, TEXT, weight=BOLD).move_to([(xa + xb) / 2, 2.15, 0])
        self.play(FadeIn(pd), run_time=0.6)
        self.at("the periderm replaces")
        pd2 = T("periderm:\nreplaces the epidermis", 34, TEXT, weight=BOLD).move_to([(xa + xb) / 2 - 0.4, 2.5, 0])
        self.play(Transform(pd, pd2), run_time=1.0)
        self.finish()


PERI = dict(k=1.25, cam_left=0.3, peri=True)


def peri_strip(sc, **kw):
    a = dict(ring_state(4, 3))
    a.update(PERI)
    a.update(kw)
    return Strip(sc, **a)


class S11Bark(SpokenScene):
    def construct(self):
        st = peri_strip(self)
        xa, xb = st.cam.get_right()[0], st.cork[-1].get_right()[0]
        self.at("bark is")
        br = VGroup(Line([xa, 1.6, 0], [xb, 1.6, 0], color=TEXT, stroke_width=6), Line([xa, 1.6, 0], [xa, 1.43, 0], color=TEXT, stroke_width=6),
                    Line([xb, 1.6, 0], [xb, 1.43, 0], color=TEXT, stroke_width=6))
        bl = T("bark", 40, TEXT, weight=BOLD).move_to([(xa + xb) / 2, 2.2, 0])
        self.play(Create(br), FadeIn(bl), run_time=1.4)
        self.at("outside the vascular cambium")
        cl = T("vascular cambium", 30, TEAL).move_to([-1.3, 2.05, 0])
        ca = Arrow([-0.15, 1.85, 0], [st.cam.get_center()[0] - 0.1, 1.45, 0], buff=0, color=TEAL, stroke_width=4, tip_length=0.18)
        self.play(FadeIn(cl), GrowArrow(ca), run_time=0.8)
        self.at("so its inner part")
        px0, px1 = st.phl[0].get_left()[0], st.phl[-1].get_right()[0]
        dots = sugar_dots(self, px0 + 0.05, px1 - 0.05, n=12, ylim=1.3)
        gb = col_pulse(self, st.phl, color=PHLC, buff=0.07)
        lv = T("living", 34, PHLL, weight=BOLD).move_to([(px0 + px1) / 2, -2.0, 0])
        self.at("living phloem")
        self.play(FadeIn(lv), run_time=0.7)
        self.at("dead cork")
        cx = st.cork.get_center()[0]
        dd = T("dead", 34, CORKL, weight=BOLD).move_to([cx, -2.0, 0])
        self.play(*[r.animate.set_fill(opacity=0.12) for c in st.cork for r in c if isinstance(r, RoundedRectangle)], FadeIn(dd), run_time=1.0)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        st = peri_strip(self, pulse=False)
        l1, p1, x, p3, u1, u3 = eq_lines()
        self.at("this is the first")
        self.play(FadeIn(l1), run_time=0.5)
        self.play(FadeIn(p1), Create(u1), FadeIn(x), FadeIn(p3), Create(u3), run_time=1.0)
        old = VGroup(l1, p1, x, p3, u1, u3)
        n1 = T("one year: ring width =", 34, TEXT).move_to([0, 3.4, 0])
        q1 = T("new wood cells in one radial row", 30, TEAL)
        qx = T("×", 30, TEXT)
        q3 = T("their average width", 30, AMBER)
        row = VGroup(q1, qx, q3).arrange(RIGHT, buff=0.3).move_to([0, 2.65, 0])
        v1 = Line(q1.get_corner(DL) + DOWN * 0.08, q1.get_corner(DR) + DOWN * 0.08, color=TEAL, stroke_width=5)
        v3 = Line(q3.get_corner(DL) + DOWN * 0.08, q3.get_corner(DR) + DOWN * 0.08, color=AMBER, stroke_width=5)
        new = VGroup(n1, q1, qx, q3, v1, v3)
        self.at("turned sideways")
        self.play(old.animate.rotate(PI / 2).scale(0.3).move_to([-5.9, 2.3, 0]), run_time=0.9)
        self.play(ReplacementTransform(old, new), run_time=1.1)
        ring4 = list(st.wood[-6:])
        xl, xr = ring4[0].get_left()[0], ring4[-1].get_right()[0]
        self.at("over one year")
        br = Brace(Line([xl, -1.45, 0], [xr, -1.45, 0]), DOWN, color=TEXT, buff=0.05)
        bt = T("one year", 30, TEXT).next_to(br, DOWN, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(bt), run_time=0.8)
        self.at("count the new wood cells")
        mid = Rectangle(width=xr - xl + 0.08, height=0.875 + 0.08, stroke_color=TEAL, stroke_width=6, fill_opacity=0).move_to([(xl + xr) / 2, 0, 0])
        self.play(Create(mid), run_time=0.6)
        nums = VGroup(*[M(str(i + 1), 26, TEAL).move_to([c.get_center()[0], 1.72 + (0.32 if i in (3, 5) else 0), 0]) for i, c in enumerate(ring4)])
        self.play(LaggedStart(*[FadeIn(n_, shift=DOWN * 0.1) for n_ in nums], lag_ratio=0.5, run_time=2.4))
        self.at("multiply by their average width")
        self.play(FadeOut(br), FadeOut(bt), run_time=0.4)
        wid = VGroup()
        for i, c in enumerate(ring4):
            l, r = c.get_left()[0] + 0.02, c.get_right()[0] - 0.02
            y = -1.7 if i % 2 == 0 else -1.95
            wid.add(VGroup(Line([l, y, 0], [r, y, 0], color=AMBER, stroke_width=7), Line([l, y - 0.1, 0], [l, y + 0.1, 0], color=AMBER, stroke_width=3),
                           Line([r, y - 0.1, 0], [r, y + 0.1, 0], color=AMBER, stroke_width=3)))
        self.play(Create(v3), LaggedStart(*[Create(m) for m in wid], lag_ratio=0.4, run_time=2.2))
        self.at("cell widths change")
        tint = VGroup(*[Rectangle(width=c.get_width() - 0.04, height=0.875, stroke_width=0, fill_color=AMBER, fill_opacity=0.4).move_to([c.get_center()[0], 0, 0])
                        for c in ring4])
        self.play(FadeIn(tint), run_time=1.0)
        self.at("so the average matters")
        aw = (xr - xl) / 6
        avg = VGroup(*[Line([xl + i * aw + 0.02, -2.4, 0], [xl + (i + 1) * aw - 0.02, -2.4, 0], color=AMBER, stroke_width=9) for i in range(6)])
        al = T("average width, six times", 28, AMBER).move_to([xl - 2.6, -2.4, 0])
        self.play(LaggedStart(*[Create(a) for a in avg], lag_ratio=0.25, run_time=1.6), FadeIn(al))
        self.at("that gives the width")
        da = DoubleArrow([xl, -3.0, 0], [xr, -3.0, 0], buff=0, color=TEXT, stroke_width=6, tip_length=0.2)
        dl = T("ring width", 32, TEXT).move_to([(xl + xr) / 2, -3.45, 0])
        self.play(GrowFromCenter(da), FadeIn(dl), run_time=0.9)
        self.finish()


class S14Maize(SpokenScene):
    def construct(self):
        cen = np.array([-3.1, -0.55, 0])
        disc = VGroup(Circle(radius=2.1, stroke_color=EPIC, stroke_width=5, fill_color="#2E4A33", fill_opacity=0.75)).move_to(cen)
        self.at("maize")
        self.play(FadeIn(disc, scale=0.9), run_time=1.0)
        self.at("no conventional vascular cambium")
        l1 = T("no conventional vascular cambium", 30, TEXT).move_to([-3.1, 2.75, 0])
        self.play(FadeIn(l1), run_time=0.8)
        self.at("its bundles are scattered")
        rng = np.random.RandomState(11)
        pts = []
        while len(pts) < 20:
            p = rng.uniform(-1.8, 1.8, 2)
            if np.hypot(*p) < 1.8 and all(np.hypot(*(p - q)) > 0.62 for q in pts):
                pts.append(p)
        bundles = VGroup()
        for p in pts:
            c = cen + [p[0], p[1], 0]
            bundles.add(VGroup(Circle(radius=0.22, stroke_color=PALE, stroke_width=3, fill_color="#14171f", fill_opacity=1).move_to(c),
                               Dot(c + [-0.07, 0.0, 0], radius=0.075, color=WOODC), Dot(c + [0.08, 0.0, 0], radius=0.075, color=PHLC)))
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bundles], lag_ratio=0.12, run_time=2.4))
        self.at("no wood")
        l2 = T("no wood", 34, TEXT, weight=BOLD).move_to([-3.1, 2.2, 0])
        self.play(FadeIn(l2), run_time=0.6)
        self.at("it grew tall")
        sx = 3.0
        stalk = Line([sx, -3.4, 0], [sx, 2.9, 0], color="#6F9A6A", stroke_width=14)
        leaves = VGroup(*[Ellipse(width=1.3, height=0.32, stroke_width=0, fill_color=LEAF, fill_opacity=0.95).rotate(0.4).move_to([sx - 0.75, y + 0.2, 0])
                          for y in (-2.1, -0.5, 1.1)])
        self.play(FadeIn(stalk), FadeIn(leaves), run_time=1.0)
        gl = Glows(self, lambda: [np.array([sx, 2.9, 0.0])], 0.0)
        self.at("shoot tip")
        st_l = T("shoot tip", 30, TEAL).move_to([5.3, 3.1, 0])
        self.play(gl.tv.animate.set_value(1.0), FadeIn(st_l), run_time=0.8)
        gl2 = Glows(self, lambda: [np.array([sx, y - 0.1, 0.0]) for y in (-2.1, -0.5, 1.1)], 0.0)
        self.at("meristems at the bases")
        bl = T("leaf and\ninternode bases", 30, TEAL).move_to([5.2, -0.7, 0])
        self.play(gl2.tv.animate.set_value(1.0), FadeIn(bl), run_time=0.9)
        self.finish()


class S15Close(SpokenScene):
    def construct(self):
        self.add(soil_rect())
        tree = Tree(self, 1.0, 1.0)
        gl = Glows(self, lambda: shoot_tips(1.0), 0.0)
        self.at("shoot tips add height")
        self.play(gl.tv.animate.set_value(1.0), run_time=1.0)
        up = Arrow([-0.1, 1.0, 0], [-0.1, 3.1, 0], buff=0, color=TEAL, stroke_width=8, tip_length=0.3)
        hl = T("height", 34, TEAL).move_to([0.9, 2.2, 0])
        self.play(GrowArrow(up), FadeIn(hl), run_time=0.9)
        self.at("its vascular cambium")
        disc = make_disc(np.array([3.2, -0.4, 0]))
        ring = ring_pulse(self, disc.cam)
        self.play(FadeIn(disc, scale=0.85), run_time=0.8)
        self.add(ring)
        self.at("adds width and wood")
        outs = VGroup(*[Arrow(disc.get_center() + 2.1 * np.array([np.cos(a), np.sin(a), 0]), disc.get_center() + 2.75 * np.array([np.cos(a), np.sin(a), 0]),
                              buff=0, color=TEXT, stroke_width=6, tip_length=0.2) for a in np.radians([25, 115, 205, 335])])
        wl = T("wider: wood inward,\nphloem outward", 30, TEXT).move_to([2.0, -3.2, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in outs], lag_ratio=0.2, run_time=1.0), FadeIn(wl), run_time=1.0)
        self.finish()


class S16End(EndCard):
    LINE = "The vascular cambium widens a trunk: wood inward, phloem outward."
