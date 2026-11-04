"""Proneural genes and lateral inhibition, chapter 5: Neighbours Compare  (Biochemistrypedia chaptered film)

COLOR MAP (one colour per concept, shared with chapters 1 to 4; first six are the map from scenes.old.py)
  GREEN  = proneural activity and the neural fate (rims of neural cells, "neural" tags, neuroblasts)
  YELLOW = Delta (knobs, the Delta chip, the arrows that carry it)
  BLUE   = Notch (cups, crescents, the Notch chip, cells in a patch with a different Notch level)
  RED    = E(spl) repressor, inhibition arrows, and the cross that marks "lost" or "blocked"
  GREY   = cells, outlines, labels, cells that are held back (epidermis)
  GOLD   = questions, "Predict" prompts, the year, comparison marks
  PINK   = mutant tissue (the patches in the mosaics, a mutant cell)  [new in this chapter]

The Notch cup on the big cells is the same cup as in chapter three. In the mosaic pictures a Notch
crescent inside a cell stands for that cell's Notch activity: thicker and brighter means more.
The spaced winners in the last scene come from the Collier lateral-inhibition model used in chapter
four (f(x) = x^2 / (0.01 + x^2), g(x) = 1 / (1 + 100 x^2)), run on a small hexagonal sheet.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PRO, DEL, NOT, REP = GREEN, YELLOW, BLUE, RED
MUT = "#E070C0"


def P3(x, y):
    return np.array([x, y, 0.0])


def arr(a, b, color=GREEN, w=5, tip=0.22):
    return Arrow(np.array(a, float), np.array(b, float), buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5)


def inhib(a, b, color=RED, w=5, half=0.24):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * half, b - perp * half, color=color, stroke_width=(w + 1) if w > 0.5 else 0.001))


def cross_mark(center, s=0.32, color=RED, w=8):
    c = np.array(center, float)
    return VGroup(Line(c + P3(-s, -s), c + P3(s, s), color=color, stroke_width=w),
                  Line(c + P3(-s, s), c + P3(s, -s), color=color, stroke_width=w))


def check_mark(center, s=0.6, color=GREEN, w=12):
    c = np.array([center[0], center[1], 0.0])
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([c + P3(-0.55 * s, 0.0), c + P3(-0.15 * s, -0.45 * s), c + P3(0.6 * s, 0.55 * s)])
    return m


def clock(pos, r=0.42):
    face = Circle(radius=r, stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to(pos)
    hand = Line(pos, pos + UP * r * 0.8, color=GOLD, stroke_width=5)
    knob = Line(pos + UP * (r + 0.02), pos + UP * (r + 0.16), color=GOLD, stroke_width=5)
    return VGroup(face, knob), hand


def bubble(txt, ctr, toward, color=RED, size=26):
    t = T(txt, size, color)
    w, h = t.width + 0.32, t.height + 0.3
    ctr, toward = np.array(ctr, float), np.array(toward, float)
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.18).move_to(ctr)
    d = toward - ctr
    d = d / np.linalg.norm(d)
    k = min((w / 2) / max(abs(d[0]), 1e-6), (h / 2) / max(abs(d[1]), 1e-6))
    base = ctr + d * k
    perp = np.array([-d[1], d[0], 0])
    tail = Polygon(base + perp * 0.1, base + d * 0.22, base - perp * 0.1, stroke_width=0, fill_color=color, fill_opacity=0.5)
    return VGroup(box, tail, t.move_to(ctr))


# ------------------------------------------------------------------------------------------
# how a cell looks in each state (stroke colour, width, opacity, fill colour, opacity)
# ------------------------------------------------------------------------------------------
KINDS = dict(
    norm=(GREY, 3, 0.85, GREY, 0.08),
    mut=(MUT, 3, 1.0, MUT, 0.30),
    mutneural=(GREEN, 7, 1.0, MUT, 0.30),
    blue=(NOT, 3, 1.0, NOT, 0.28),
    neural=(GREEN, 6, 1.0, GREEN, 0.28),
    epi=(GREY, 4, 1.0, GREY, 0.38),
)


def paint(m, kind):
    s, w, so, f, fo = KINDS[kind]
    return m.set_stroke(s, w, so).set_fill(f, fo)


def to_kind(m, kind):
    s, w, so, f, fo = KINDS[kind]
    return m.animate.set_stroke(s, w, so).set_fill(f, fo)


# ------------------------------------------------------------------------------------------
# the cell of chapter three: grey body, nucleus with two bars (proneural, repressor), a Delta knob and a Notch cup
# ------------------------------------------------------------------------------------------
class Cell:
    def __init__(self, cx, cy, R, side, name="", kang=18, cang=-18, ks=1.0):
        s = R / 2.2
        self.ks = ks
        self.stalk0 = 0.3 * s * ks + (ks - 1) * 0.25
        self.shift = 0.4 * s * ks
        self.cx, self.cy, self.R, self.side, self.s = cx, cy, R, side, s
        self.c = np.array([cx, cy, 0.0])
        self.pro, self.rep, self.delta, self.notch = (ValueTracker(0) for _ in range(4))
        self.cupvis, self.bind, self.pull = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.kvis, self.inh_on, self.cs = ValueTracker(1), ValueTracker(0), ValueTracker(1)
        self.other = None
        self.body = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(self.c)
        self.nuc = Circle(radius=0.73 * R, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(self.c).set_stroke(opacity=0.6)
        self.label = T(name, 30, GREY).move_to([cx, cy + R + 0.42, 0]) if name else None
        self.H, self.BASE, self.BW = 0.92 * R, cy - 0.46 * R, 0.18 * R
        self.bxp, self.bxr = cx - 0.23 * R, cx + 0.23 * R
        self.tracks = VGroup(*[Rectangle(width=self.BW, height=self.H, stroke_color=GREY, stroke_width=2, fill_opacity=0)
                               .set_stroke(opacity=0.45).move_to([x, self.BASE + self.H / 2, 0]) for x in (self.bxp, self.bxr)])
        ka = np.radians(kang if side > 0 else 180 + kang)
        ca = np.radians(cang if side > 0 else 180 + cang)
        self.kp = self.c + R * np.array([np.cos(ka), np.sin(ka), 0])
        self.cp = self.c + R * np.array([np.cos(ca), np.sin(ca), 0])
        self.u = np.array([side, 0, 0.0])
        self.e, self.cupR = self.stalk0, 0.19 * R * ks
        self.pro_bar = always_redraw(lambda: self._bar(self.bxp, self.pro.get_value(), PRO))
        self.rep_bar = always_redraw(lambda: self._bar(self.bxr, self.rep.get_value(), REP))
        self.inh = always_redraw(self._inh)
        self.stalk = always_redraw(self._stalk)
        self.knob = always_redraw(self._knob)
        self.cup = always_redraw(self._cup)
        self.dyn = [self.pro_bar, self.rep_bar, self.inh, self.stalk, self.knob, self.cup]
        self.static = VGroup(self.body, self.nuc, *([self.label] if self.label else []))

    def link(self, other):
        self.other = other

    def Lval(self):
        if self.other is None:
            return 1.0
        return max(0.0, self.side * (self.other.cup_c()[0] - self.kp[0]) - self.stalk0)

    def _bar(self, x, v, color):
        h = max(1e-3, v * self.H)
        return Rectangle(width=self.BW, height=h, stroke_width=0, fill_color=color, fill_opacity=0.92).move_to([x, self.BASE + h / 2, 0])

    def _inh(self):
        r = self.rep.get_value() * self.inh_on.get_value()
        w = 0.001 if r < 0.02 else 2 + 7 * r
        y = self.BASE + 0.62 * self.H
        return inhib([self.bxr - self.BW / 2, y, 0], [self.bxp + self.BW / 2, y, 0], w=w, half=0.2 * max(0.7, self.s))

    def knob_c(self):
        sh = self.stalk0 + self.Lval() * self.bind.get_value() - self.shift * self.pull.get_value()
        return self.kp + np.array([self.side * sh, 0, 0])

    def _knob(self):
        d = self.delta.get_value() * self.kvis.get_value()
        on = d > 0.01
        r = self.R * (0.03 + 0.14 * d) * self.ks if on else 1e-3
        return Circle(radius=r, stroke_color=DEL, stroke_width=3 if on else 0, fill_color=DEL,
                      fill_opacity=0.92 if on else 0).move_to(self.knob_c())

    def _stalk(self):
        on = self.delta.get_value() * self.kvis.get_value() > 0.01
        return Line(self.kp, self.knob_c(), color=GREY, stroke_width=4 if on else 0.001)

    def cup_c(self):
        return self.cp + self.u * (self.e + self.cupR * self.cs.get_value()) + self.u * self.shift * self.pull.get_value()

    def _cup(self):
        v = self.cupvis.get_value()
        cs = self.cs.get_value()
        w = max(0.001, v * (3 + 10 * self.notch.get_value()) * (0.55 + 0.45 * self.s) * (1 + (self.ks - 1) * 0.5) * (0.5 + 0.5 * cs))
        c = self.cup_c()
        rr = self.cupR * cs
        st = PI / 2 if self.side > 0 else -PI / 2
        arc = Arc(radius=rr, start_angle=st, angle=PI, arc_center=c, color=NOT, stroke_width=w)
        stem = Line(self.cp, c - self.u * rr, color=NOT, stroke_width=max(0.001, v * 3.5))
        return VGroup(arc, stem)

    def setv(self, **kw):
        for k, v in kw.items():
            getattr(self, k).set_value(v)

    def to(self, **kw):
        return [getattr(self, k).animate.set_value(v) for k, v in kw.items()]

    def put(self, scene, bars=True):
        scene.add(self.static)
        if bars:
            scene.add(self.tracks)
        scene.add(*self.dyn)

    def freeze(self):
        for m in self.dyn:
            m.update(0)
            m.clear_updaters()
        return self.dyn

    def _lab(self, fn):
        return [fn(self.label.animate)] if self.label else []

    def win(self):
        return [self.body.animate.set_stroke(GREEN, 6, opacity=1).set_fill(GREEN, 0.2)] + self._lab(lambda a: a.set_color(GREEN))

    def neutral(self):
        return [self.body.animate.set_stroke(GREY, 4, opacity=1).set_fill(GREY, 0.08)] + self._lab(lambda a: a.set_color(GREY).set_opacity(1))

    def lose(self):
        return [self.body.animate.set_stroke(GREY, 4, opacity=0.5).set_fill(GREY, 0.04)] + self._lab(lambda a: a.set_color(GREY).set_opacity(0.6))

    def win_now(self):
        self.body.set_stroke(GREEN, 6, opacity=1).set_fill(GREEN, 0.2)
        if self.label:
            self.label.set_color(GREEN)

    def lose_now(self):
        self.body.set_stroke(GREY, 4, opacity=0.5).set_fill(GREY, 0.04)
        if self.label:
            self.label.set_color(GREY).set_opacity(0.6)


def link_pair(A, B):
    A.link(B)
    B.link(A)
    return A, B


def pair_cells(R=2.35, x=3.85, cy=-0.25, ks=1.2, names=("A", "B")):
    return link_pair(Cell(-x, cy, R, +1, names[0], ks=ks), Cell(x, cy, R, -1, names[1], ks=ks))


def base_vals(A, B):
    for c in (A, B):
        c.setv(pro=0.5, rep=0.35, notch=0.35, delta=0.5, cupvis=1, bind=1, inh_on=1)


# the pair after the loop has run with A slightly ahead (chapter three), and with A's Notch halved
def end_vals(A, B):
    A.setv(pro=0.85, rep=0.1, notch=0.1, delta=0.9, cupvis=1, bind=1, inh_on=1)
    B.setv(pro=0.15, rep=0.8, notch=0.75, delta=0.2, cupvis=1, bind=1, inh_on=1)


# ------------------------------------------------------------------------------------------
# rings of cells: the embryo cross-section and the notum
# ------------------------------------------------------------------------------------------
def ellipse_pts(cx, cy, a, b, n):
    t = np.linspace(0, 2 * np.pi, 3000, endpoint=False)
    x, y = a * np.cos(t), b * np.sin(t)
    seg = np.hypot(np.diff(np.r_[x, x[0]]), np.diff(np.r_[y, y[0]]))
    s = np.r_[0, np.cumsum(seg)][:-1]
    targets = np.linspace(0, s[-1], n, endpoint=False)
    ts = np.interp(targets, s, t)
    return [(cx + a * np.cos(u), cy + b * np.sin(u), u) for u in ts]


VENT = (np.radians(226), np.radians(314))


class Embryo:
    """Cross-section of the fly embryo: a ring of skin cells, and on the underside a nervous system of neuroblasts."""

    def __init__(self, cx=0.0, cy=-0.1, a=3.9, b=2.55, n=44, r=0.19):
        self.cx, self.cy, self.a, self.b, self.r = cx, cy, a, b, r
        self.outline = Ellipse(width=2 * a, height=2 * b, stroke_color=GREY, stroke_width=2).set_stroke(opacity=0.4).move_to([cx, cy, 0])
        pts = ellipse_pts(cx, cy, a, b, n)
        self.ring, self.ring_t = [], []
        for x, y, u in pts:
            c = Circle(radius=r, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.15).move_to([x, y, 0])
            self.ring.append(c)
            self.ring_t.append(u)
        self.vent_idx = [i for i, u in enumerate(self.ring_t) if VENT[0] <= u <= VENT[1]]
        rows = []
        for k, cnt in zip((1, 2, 3), (11, 10, 8)):
            aa, bb = a - 0.5 * k, b - 0.5 * k
            row = []
            span = 0.62 - 0.07 * (k - 1)
            for j in range(cnt):
                u = 1.5 * np.pi - span + 2 * span * j / (cnt - 1)
                row.append(P3(cx + aa * np.cos(u), cy + bb * np.sin(u)))
            rows.append(row)
        self.nb = []
        for row in rows:
            for p in row:
                self.nb.append(Circle(radius=0.2, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.7).move_to(p))
        self.nb_few = [self.nb[i] for i in (1, 4, 6, 9)]
        self.nb_rest = [m for m in self.nb if all(m is not q for q in self.nb_few)]
        self.thin = [self.ring[i] for i in self.vent_idx[1::2]]          # skin cells that are missing on the underside
        self.thin_keep = [self.ring[i] for i in self.vent_idx[0::2]]

    def ghosts(self):
        return VGroup(*[DashedVMobject(Circle(radius=self.r, stroke_color=GREY, stroke_width=3).move_to(c.get_center()), num_dashes=8).set_opacity(0.7)
                        for c in self.thin])


def notum_geom(cx, cy, a, b, sp, r):
    out = []
    rows = int(2 * b / (sp * 0.866)) + 2
    for i in range(-rows // 2, rows // 2 + 1):
        y = i * sp * 0.866
        for j in range(-8, 9):
            x = j * sp + (i % 2) * sp / 2
            if (x / a) ** 2 + (y / b) ** 2 < 0.9:
                out.append(P3(cx + x, cy + y))
    return out


def notum_cells(cx, cy, a, b, sp, r):
    return [Circle(radius=r, stroke_color=GREY, stroke_width=2, fill_color=GREY, fill_opacity=0.10).move_to(p) for p in notum_geom(cx, cy, a, b, sp, r)]


# ------------------------------------------------------------------------------------------
# the sheet of cells for the mosaics: hexagonal packing, 9 columns, 5 rows
# ------------------------------------------------------------------------------------------
SCOLS, SROWS, SD, SR, SCX, SCY = 9, 5, 1.3, 0.57, 0.0, -0.1


def spos(r, c):
    x = SCX + (c - (SCOLS - 1) / 2) * SD + (r % 2 - 0.5) * SD * 0.5
    y = SCY + ((SROWS - 1) / 2 - r) * SD * 0.866
    return P3(x, y)


MUT_COLS = (0, 1, 2, 3)
BLUE_COLS = (7, 8)


class Mosaic:
    def __init__(self, mut=MUT_COLS, blue=()):
        self.cells = {}
        for r in range(SROWS):
            for c in range(SCOLS):
                m = Circle(radius=SR).move_to(spos(r, c))
                paint(m, "mut" if c in mut else "blue" if c in blue else "norm")
                self.cells[(r, c)] = m
        self.group = VGroup(*self.cells.values())

    def col(self, c):
        return [self.cells[(r, c)] for r in range(SROWS)]

    def cols(self, cs):
        return [m for c in cs for m in self.col(c)]

    def qmarks(self, cs=(3, 4)):
        return VGroup(*[T("?", 44, GOLD, font=TITLE_FONT).move_to(spos(r, c) + P3(-0.12 if c == cs[0] else 0.12, 0.02)) for c in cs for r in range(SROWS)])

    def border(self):
        pts = [P3((spos(r, 3)[0] + spos(r, 4)[0]) / 2, spos(r, 3)[1]) for r in range(SROWS)]
        pts = [pts[0] + P3(0, 0.55)] + pts + [pts[-1] - P3(0, 0.55)]
        line = VMobject(stroke_color=GOLD, stroke_width=5, fill_opacity=0)
        line.set_points_as_corners(pts)
        return DashedVMobject(line, num_dashes=24)


def crescent(c, rc, level, color=NOT):
    """A Notch crescent inside a cell of radius rc: bigger and brighter means more activity."""
    ang = 70 + 90 * level
    w = (3 + 17 * level) * (0.45 + 0.55 * rc / 1.5)
    return Arc(radius=0.55 * rc, start_angle=np.radians(90 - ang / 2), angle=np.radians(ang), arc_center=np.array(c, float),
               color=color, stroke_width=w, stroke_opacity=0.35 + 0.65 * level)


def mk_row(cy, R, sp, lv, mid="norm", cx=0.0):
    """Three cells in a row with a Notch crescent in each. The middle one can be normal, epidermis or neural."""
    xs = [cx - sp, cx, cx + sp]
    bodies, cres = [], []
    for i, x in enumerate(xs):
        if i == 1 and mid == "epi":
            b = Ellipse(width=2 * R, height=0.6 * R).move_to([x, cy, 0])
            paint(b, "epi")
        else:
            b = Circle(radius=R).move_to([x, cy, 0])
            paint(b, "neural" if (i == 1 and mid == "neural") else "norm")
        bodies.append(b)
        c = crescent([x, cy, 0], R, lv[i])
        if i == 1 and mid == "epi":
            c.set_stroke(opacity=0)
        cres.append(c)
    return VGroup(*bodies, *cres)


# ------------------------------------------------------------------------------------------
# a balance with two Notch bowls (scene 17)
# ------------------------------------------------------------------------------------------
class Balance:
    PIV = np.array([0.0, -0.4, 0.0])
    L = 4.6

    def __init__(self):
        self.tilt, self.lv, self.rv, self.lvis, self.rvis = (ValueTracker(0) for _ in range(5))
        self.stand = Polygon(self.PIV, self.PIV + P3(-1.3, -2.4), self.PIV + P3(1.3, -2.4), stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.18)
        self.beam = always_redraw(self._beam)
        self.bowl_l = always_redraw(lambda: self._bowl(-1))
        self.bowl_r = always_redraw(lambda: self._bowl(+1))

    def end(self, side):
        th = self.tilt.get_value()
        return self.PIV + side * self.L * P3(np.cos(th), np.sin(th))

    def _beam(self):
        return VGroup(Line(self.end(-1), self.end(1), color=GREY, stroke_width=11), Dot(self.PIV, radius=0.13, color=GOLD))

    def _bowl(self, side):
        lv = (self.lv if side < 0 else self.rv).get_value()
        vis = (self.lvis if side < 0 else self.rvis).get_value()
        r = 0.6 + 0.8 * lv
        e = self.end(side)
        c = e + P3(0, r)
        w = max(0.001, (6 + 22 * lv) * vis)
        return Arc(radius=r, start_angle=PI, angle=PI, arc_center=c, color=NOT, stroke_width=w, stroke_opacity=max(vis, 0.001))


# ==========================================================================================
class S00Title(TitleCard):
    LESSON = "Proneural genes and lateral inhibition"
    TITLE = "Neighbours Compare"


def plain_chip(text, size=28):
    """A chip that stays readable on the dark ground: bright text in a grey box (for 'not neural')."""
    c = chip(text, GREY, size)
    c[1].set_color(TEXT)
    c[0].set_stroke(TEXT, 2.5, 0.8).set_fill(GREY, 0.35)
    return c


def swap(scene, old, new, t=0.25):
    """Fade the old label out completely, then fade the new one in (no morphing, no overlap)."""
    scene.play(FadeOut(old), run_time=t)
    scene.play(FadeIn(new), run_time=t)


# ------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        E = Embryo(cx=-3.65, cy=-0.2, a=3.1, b=2.5, n=38, r=0.18)
        ncells = notum_cells(3.9, -0.2, 2.05, 2.75, 0.7, 0.25)
        notum_out = Ellipse(width=4.1, height=5.5, stroke_color=GREY, stroke_width=3).set_stroke(opacity=0.7).move_to([3.9, -0.2, 0])
        l1 = T("embryo, cross-section", 28, GREY).move_to([-3.65, -3.4, 0])
        l2 = T("notum, back of the thorax", 28, GREY).move_to([3.9, -3.4, 0])
        self.add(E.outline, notum_out, l1, l2)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in E.ring], lag_ratio=0.015),
                  LaggedStart(*[GrowFromCenter(c) for c in ncells], lag_ratio=0.008), run_time=1.1)
        self.at("how do we know")
        q = T("How do we know that real cells compare?", 36, GOLD).move_to([0, 3.3, 0])
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


# ------------------------------------------------------------------------------------------
def hex7(cx, cy, d=1.2):
    return [P3(cx, cy)] + [P3(cx + d * np.cos(np.radians(60 * k + 30)), cy + d * np.sin(np.radians(60 * k + 30))) for k in range(6)]


class S02History(SpokenScene):
    def construct(self):
        y0 = 2.15
        xx = lambda yr: -5.5 + (yr - 1980) / 15 * 11
        axis = Line([-5.9, y0, 0], [5.9, y0, 0], color=GREY, stroke_width=4)
        years = (1980, 1985, 1990, 1995)
        ticks = VGroup(*[Line([xx(y), y0 - 0.12, 0], [xx(y), y0 + 0.12, 0], color=GREY, stroke_width=4) for y in years])
        tl = VGroup(*[M(str(y), 26, GREY).move_to([xx(y), y0 - 0.5, 0]) for y in years])
        self.add(axis, ticks, tl)
        self.at("late 1980s")
        mx = xx(1988)
        stem = Line([mx, y0, 0], [mx, y0 + 0.75, 0], color=GOLD, stroke_width=5)
        dot = Dot([mx, y0, 0], radius=0.17, color=GOLD)
        lab = T("late 1980s", 32, GOLD).move_to([mx, y0 + 1.2, 0])
        self.play(FadeIn(dot, scale=0.4), Create(stem), FadeIn(lab, shift=DOWN * 0.1), run_time=0.7)
        pos = hex7(1.6, -0.6, 1.2)
        cl = VGroup(*[Circle(radius=0.55, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to(p) for p in pos])
        l_eq = T("a cluster of equal cells", 28, GREY).move_to([1.6, -3.0, 0])
        self.play(LaggedStart(*[GrowFromCenter(m) for m in cl], lag_ratio=0.06), FadeIn(l_eq), run_time=0.9)
        self.at("embryos lacking notch")
        c1 = chip("no Notch", NOT, 30).move_to([-4.6, -0.1, 0])
        a = arr([-3.0, -0.6, 0], [-0.55, -0.6, 0], TEXT, 6)
        self.play(FadeIn(c1, shift=RIGHT * 0.2), GrowArrow(a), run_time=0.5)
        self.at("or delta")
        c2 = chip("no Delta", DEL, 30).move_to([-4.6, -1.3, 0])
        self.play(FadeIn(c2, shift=RIGHT * 0.2), run_time=0.5)
        self.at("make too many")
        l_many = T("too many neural cells", 30, GREEN).move_to([1.6, -3.0, 0])
        one = Circle(radius=0.55, stroke_color=GREEN, stroke_width=6, fill_color=GREEN, fill_opacity=0.28).move_to([5.5, -0.6, 0])
        l_one = T("normal: one", 28, GREEN).move_to([5.5, -3.0, 0])
        self.play(*[to_kind(m, "neural") for m in cl], FadeOut(l_eq), GrowFromCenter(one), run_time=0.7)
        self.play(FadeIn(l_many), FadeIn(l_one), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------------------------------
class S03History2(SpokenScene):
    def construct(self):
        A, B = pair_cells(R=2.2, x=3.2, cy=0.2, ks=1.15, names=("cell A", "cell B"))
        for c in (A, B):
            c.setv(delta=0.0, notch=0.4, cupvis=0)
        self.add(*A.dyn, *B.dyn)
        self.add(A.static, B.static)
        self.at("both carrying")
        self.play(Indicate(A.body, color=TEXT, scale_factor=1.03), Indicate(B.body, color=TEXT, scale_factor=1.03), run_time=0.6)
        self.at("the receptor")
        cr = chip("the receptor: Notch", NOT, 28, pad=0.16).move_to([-3.0, -2.95, 0])
        self.play(*A.to(cupvis=1), *B.to(cupvis=1), FadeIn(cr, shift=UP * 0.15), run_time=0.6)
        self.at("and the ligand")
        lg = chip("the ligand: Delta", DEL, 28, pad=0.16).move_to([3.0, -2.95, 0])
        self.play(*A.to(delta=0.65), *B.to(delta=0.65), FadeIn(lg, shift=UP * 0.15), run_time=0.8)
        self.at("make the choice")
        q = T("?", 120, GOLD, font=TITLE_FONT).move_to([0, 0.2, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.play(Indicate(q, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------
def crossed_chips(x=-5.7):
    n = chip("Notch", NOT, 28).move_to([x, 1.7, 0])
    d = chip("Delta", DEL, 28).move_to([x, 0.6, 0])
    xs = VGroup(cross_mark(n.get_right() + P3(0.42, 0), 0.24, RED, 7), cross_mark(d.get_right() + P3(0.42, 0), 0.24, RED, 7))
    return n, d, xs


def nb_label(E, size=26):
    nbl = chip("neuroblasts", GREEN, size).move_to([5.15, -1.0, 0])
    tgt = E.nb_few[3].get_center() + P3(0.12, 0.02)
    ln = Line(nbl.get_left() + LEFT * 0.03, tgt, color=GREEN, stroke_width=3).set_opacity(0.85)
    return nbl, ln


def emb_title(txt):
    return T(txt, 30, GREY).move_to([0, 3.15, 0])


def underside():
    br = Line([-2.7, -3.0, 0], [2.7, -3.0, 0], color=GREY, stroke_width=4)
    ul = T("ventral (underside)", 28, GREY).move_to([0, -3.42, 0])
    return br, ul


class S04Embryo(SpokenScene):
    def construct(self):
        E = Embryo()
        lab = emb_title("normal embryo")
        br, ul = underside()
        self.add(E.outline, *E.ring, lab)
        self.wait(0.3)
        self.at("embryo map")
        self.play(Create(br), FadeIn(ul, shift=UP * 0.1), run_time=0.5)
        self.at("fly embryos")
        nbl, ln = nb_label(E)
        self.add(ln)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in E.nb_few], lag_ratio=0.15), FadeIn(nbl, shift=LEFT * 0.2), Create(ln), run_time=0.6)
        self.at("lacking notch")
        lab2 = emb_title("embryo without Notch or Delta")
        n, d, xs = crossed_chips()
        self.play(FadeOut(lab), run_time=0.2)
        self.play(FadeIn(lab2), FadeIn(n, shift=RIGHT * 0.2), FadeIn(d, shift=RIGHT * 0.2), run_time=0.45)
        self.play(FadeIn(xs), run_time=0.3)
        self.at("too many")
        self.play(LaggedStart(*[GrowFromCenter(m) for m in E.nb_rest], lag_ratio=0.02), run_time=0.55)
        self.at("neuroblasts")
        self.play(Indicate(nbl, color=TEXT, scale_factor=1.1), run_time=0.7)
        self.finish()


def emb_state(scene, thin=False):
    E = Embryo()
    lab = emb_title("embryo without Notch or Delta")
    n, d, xs = crossed_chips()
    nbl, ln = nb_label(E)
    br, ul = underside()
    scene.add(E.outline, *E.ring, ln, *E.nb, lab, n, d, xs, nbl, br, ul)
    return E, lab, n, d, xs, nbl, ln, br, ul


class S05Embryo2(SpokenScene):
    def construct(self):
        E, lab, n, d, xs, nbl, ln, br, ul = emb_state(self)
        self.at("too little")
        gh = E.ghosts().set_opacity(0.9)
        ec = chip("epidermis (thin)", GREY, 26).move_to([5.0, -2.6, 0])
        ec[1].set_color(TEXT)
        eln = Line(ec.get_left() + LEFT * 0.03, E.thin_keep[-1].get_center() + P3(0.28, -0.05), color=TEXT, stroke_width=3).set_opacity(0.85)
        self.play(*[FadeOut(c) for c in E.thin], FadeIn(gh), FadeIn(ec, shift=LEFT * 0.2), run_time=0.6)
        self.at("epidermis")
        self.play(*[c.animate.set_stroke(TEXT, 4, 1.0).set_fill(GREY, 0.5) for c in E.thin_keep], Create(eln), run_time=0.7)
        self.at("underside")
        self.play(Indicate(ul, color=TEXT, scale_factor=1.12), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------
class S06Neurogenic(SpokenScene):
    def construct(self):
        E, lab, n, d, xs, nbl, ln, br, ul = emb_state(self)
        gh = E.ghosts().set_opacity(0.9)
        for c in E.thin:
            self.remove(c)
        self.add(gh)
        for c in E.thin_keep:
            c.set_stroke(TEXT, 4, 1.0).set_fill(GREY, 0.5)
        ec = chip("epidermis (thin)", GREY, 26).move_to([5.0, -2.6, 0])
        ec[1].set_color(TEXT)
        eln = Line(ec.get_left() + LEFT * 0.03, E.thin_keep[-1].get_center() + P3(0.28, -0.05), color=TEXT, stroke_width=3).set_opacity(0.85)
        self.add(ec, eln)
        keep = [c for c in E.ring if all(c is not t for t in E.thin)]
        # the embryo is gone in half a second; no ghost remains when the new picture starts
        rest = [E.outline, *keep, *E.nb, lab, nbl, ln, gh, br, ul, xs, ec, eln, n, d]
        hd = T("neurogenic genes", 40, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
        A = Cell(-3.9, -0.6, 2.45, +1, "")
        B = Cell(3.9, -0.6, 2.45, -1, "")
        A.setv(delta=0.0, cupvis=0)
        B.setv(delta=0.0, cupvis=0, notch=0.4)
        nch = chip("Notch", NOT, 30).move_to([1.0, 1.95, 0])
        dch = chip("Delta", DEL, 30).move_to([-1.3, 1.95, 0])
        self.add(*A.dyn, *B.dyn)
        outs = AnimationGroup(*[FadeOut(m) for m in rest], run_time=0.3)
        ins = AnimationGroup(FadeIn(A.body), FadeIn(B.body), FadeIn(A.nuc), FadeIn(B.nuc),
                             run_time=0.5)
        self.play(AnimationGroup(outs, ins, lag_ratio=0.6))
        self.at("neurogenic")
        self.play(FadeIn(hd, shift=DOWN * 0.1), run_time=0.5)
        self.at("without the receptor")
        ln_n = Line(nch.get_bottom(), P3(0.85, 0.75), color=NOT, stroke_width=3)
        self.play(*B.to(cupvis=1), FadeIn(nch, shift=DOWN * 0.1), Create(ln_n), run_time=0.6)
        cx = cross_mark(B.cup_c() + P3(-0.3, -0.8), 0.3, RED, 8)
        self.at("receptor,")
        self.play(FadeIn(cx, scale=0.6), run_time=0.4)
        self.at("no cell can be told")
        kb = P3(A.kp[0] + 0.33, A.kp[1])
        ln_d = Line(dch.get_bottom(), P3(kb[0], kb[1] + 0.5), color=DEL, stroke_width=3)
        sig = arr([A.kp[0] + 0.85, A.kp[1], 0], [B.cup_c()[0] - 0.2, B.cup_c()[1], 0], DEL, 7)
        self.play(*A.to(delta=0.9), FadeIn(dch, shift=DOWN * 0.1), Create(ln_d), GrowArrow(sig), run_time=0.7)
        self.at("not you")
        bb = bubble("not you", [0.0, -1.5, 0], [0.0, 0.0, 0], RED, 30)
        self.play(FadeIn(bb, scale=0.7), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------
NOTUM = (-2.35, -0.05, 3.5, 3.1)
PATCHES = [(P3(-4.05, 0.7), 1.0), (P3(-1.5, -1.35), 0.95), (P3(-2.2, 2.0), 0.6)]


def notum_scene(scene, with_patches, with_card):
    cx, cy, a, b = NOTUM
    cells = notum_cells(cx, cy, a, b, 0.62, 0.24)
    if with_patches:
        for c in cells:
            if any(np.linalg.norm(c.get_center() - q) < r for q, r in PATCHES):
                paint(c, "mut")
    out = Ellipse(width=2 * a, height=2 * b, stroke_color=GREY, stroke_width=3).set_stroke(opacity=0.7).move_to([cx, cy, 0])
    lab = T("notum", 30, GREY).move_to([cx, cy + b + 0.42, 0])
    card = RoundedRectangle(corner_radius=0.2, width=4.7, height=3.6, stroke_color=GOLD, stroke_width=3, fill_color=GOLD,
                            fill_opacity=0.06).move_to([4.45, 0.2, 0])
    yr = T("1991", 52, GOLD, font=TITLE_FONT).move_to([4.45, 1.35, 0])
    n1 = T("Pascal Heitzler", 32, TEXT).move_to([4.45, 0.2, 0])
    n2 = T("Pat Simpson", 32, TEXT).move_to([4.45, -0.75, 0])
    return cells, out, lab, card, yr, n1, n2


class S07Mosaic(SpokenScene):
    def construct(self):
        cells, out, lab, card, yr, n1, n2 = notum_scene(self, False, True)
        self.add(out, *cells, lab)
        self.at("in 1991")
        self.play(FadeIn(card), FadeIn(yr, shift=DOWN * 0.1), run_time=0.6)
        self.at("in 1991", lead=-1.2)
        self.play(FadeIn(n1, shift=RIGHT * 0.15), run_time=0.5)
        self.at("and pat")
        self.play(FadeIn(n2, shift=RIGHT * 0.15), run_time=0.5)
        self.at("made fly mosaics")
        pk = [c for c in cells if any(np.linalg.norm(c.get_center() - q) < r for q, r in PATCHES)]
        self.play(*[to_kind(c, "mut") for c in pk], run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------------------------
CAP_MUT_Y, CAP_NORM_Y = 3.25, -3.4


def cap_normal():
    return T("normal cells", 30, TEXT).move_to([2.2, CAP_NORM_Y, 0])


class S08Mosaic2(SpokenScene):
    def construct(self):
        cells, out, lab, card, yr, n1, n2 = notum_scene(self, True, True)
        self.add(out, *cells, lab, card, yr, n1, n2)
        M_ = Mosaic(mut=(), blue=())
        for m in M_.cells.values():
            m.set_stroke(opacity=0).set_fill(opacity=0)
        self.add(M_.group)
        self.play(*[FadeOut(m) for m in (out, lab, card, yr, n1, n2)], *[FadeOut(c) for c in cells],
                  *[m.animate.set_stroke(GREY, 3, 0.85).set_fill(GREY, 0.08) for m in M_.cells.values()], run_time=0.6)
        self.at("mutant cells")
        cap = T("mutant cells", 30, MUT).move_to([-3.9, CAP_MUT_Y, 0])
        self.play(*[to_kind(m, "mut") for m in M_.cols(MUT_COLS)], FadeIn(cap, shift=DOWN * 0.1), run_time=0.9)
        self.at("a different level")
        cap2 = T("different Notch level", 26, NOT).move_to([5.0, CAP_MUT_Y, 0])
        self.play(*[to_kind(m, "blue") for m in M_.cols(BLUE_COLS)], FadeIn(cap2, shift=DOWN * 0.1), run_time=0.9)
        self.at("lay")
        bd = M_.border()
        self.play(Create(bd), run_time=0.7)
        self.at("normal cells")
        cap3 = cap_normal()
        self.play(FadeIn(cap3, shift=UP * 0.1), run_time=0.5)
        self.finish()


def mosaic_state8(scene):
    M_ = Mosaic(mut=MUT_COLS, blue=BLUE_COLS)
    cap = T("mutant cells", 30, MUT).move_to([-3.9, CAP_MUT_Y, 0])
    cap2 = T("different Notch level", 26, NOT).move_to([5.0, CAP_MUT_Y, 0])
    cap3 = cap_normal()
    bd = M_.border()
    scene.add(M_.group, cap, cap2, cap3, bd)
    return M_, cap, cap2, cap3, bd


class S09Mosaic3(SpokenScene):
    def construct(self):
        M_, cap, cap2, cap3, bd = mosaic_state8(self)
        aside = T("set aside", 26, NOT).move_to(cap2.get_center())
        self.play(*[m.animate.set_stroke(NOT, 3, 0.45).set_fill(NOT, 0.08) for m in M_.cols(BLUE_COLS)], FadeOut(cap2), run_time=0.4)
        self.play(FadeIn(aside), run_time=0.3)
        self.at("patch borders")
        q = M_.qmarks((3, 4))
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in q], lag_ratio=0.05), run_time=0.6)
        self.at("became precursors")
        self.play(Indicate(q, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.play(*[to_kind(m, "norm") for m in M_.cols(BLUE_COLS)], FadeOut(aside), run_time=0.4)
        self.finish()


def mosaic_state9(scene):
    M_ = Mosaic(mut=MUT_COLS)
    cap = T("mutant cells", 30, MUT).move_to([-3.9, CAP_MUT_Y, 0])
    cap3 = cap_normal()
    bd = M_.border()
    q = M_.qmarks((3, 4))
    scene.add(M_.group, cap, cap3, bd, q)
    return M_, cap, cap3, bd, q


class S10Notch(SpokenScene):
    def construct(self):
        M_, cap, cap3, bd, q = mosaic_state9(self)
        self.at("mutant for notch")
        cap_n = T("Notch-mutant cells", 30, MUT).move_to([-3.9, CAP_MUT_Y, 0])
        swap(self, cap, cap_n, 0.2)
        self.at("became neural")
        tag = chip("neural", GREEN, 30).move_to([-1.3, CAP_NORM_Y, 0])
        self.play(FadeOut(q), FadeOut(bd), *[to_kind(m, "mutneural") for m in M_.col(3)], FadeIn(tag, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S11Predict(SpokenScene):
    def construct(self):
        M_ = Mosaic(mut=MUT_COLS)
        for m in M_.col(3):
            paint(m, "mutneural")
        cap = T("Notch-mutant cells", 30, MUT).move_to([-3.9, CAP_MUT_Y, 0])
        cap3 = cap_normal()
        tag = chip("neural", GREEN, 30).move_to([-1.3, CAP_NORM_Y, 0])
        self.add(M_.group, cap, cap3, tag)
        p1 = T("Predict.", 32, GOLD, weight=BOLD).move_to([1.0, CAP_MUT_Y, 0])
        cap_d = T("Delta-mutant cells", 30, MUT).move_to([-3.9, CAP_MUT_Y, 0])
        # one move on 'Predict': the old answer (green rings, 'neural' chip, old label) is cleared and the new case is named
        self.play(FadeIn(p1, shift=DOWN * 0.1), FadeOut(cap), FadeOut(tag), *[to_kind(m, "mut") for m in M_.col(3)],
                  FadeIn(cap_d), run_time=0.5)
        self.at("what about cells")
        self.play(Indicate(cap_d, color=TEXT, scale_factor=1.08), run_time=0.5)
        self.at("beside normal")
        q = M_.qmarks((3, 4))
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in q], lag_ratio=0.03), run_time=0.3)
        self.at("normal cells")
        p2 = T("neural or not?", 32, GOLD).move_to([3.7, CAP_MUT_Y, 0])
        self.play(FadeIn(p2, shift=LEFT * 0.15), run_time=0.4)
        self.finish()


def delta_prompt_frame(scene):
    M_ = Mosaic(mut=MUT_COLS)
    cap = T("Delta-mutant cells", 30, MUT).move_to([-3.9, CAP_MUT_Y, 0])
    cap3 = cap_normal()
    p1 = T("Predict.", 32, GOLD, weight=BOLD).move_to([1.0, CAP_MUT_Y, 0])
    p2 = T("neural or not?", 32, GOLD).move_to([3.7, CAP_MUT_Y, 0])
    q = M_.qmarks((3, 4))
    scene.add(M_.group, cap, cap3, p1, p2, q)
    return M_, cap, cap3, p1, p2, q


class S12Pause(NarratedScene):
    def construct(self):
        delta_prompt_frame(self)
        pos = P3(6.25, CAP_MUT_Y)
        face, hand = clock(pos, 0.36)
        self.add(face, hand)
        self.play(Rotate(hand, angle=-2 * PI, about_point=pos, rate_func=linear), run_time=4.6)
        self.finish()


# ------------------------------------------------------------------------------------------
def patch_cells(cx, rows=5, cols=4, dx=1.25, dy=1.05, r=0.55, mut=(0, 1)):
    cells = {}
    for rr in range(rows):
        for c in range(cols):
            x = cx + (c - (cols - 1) / 2) * dx + (rr % 2 - 0.5) * dx * 0.5
            y = ((rows - 1) / 2 - rr) * dy
            m = Circle(radius=r).move_to(P3(x, y))
            paint(m, "mut" if c in mut else "norm")
            cells[(rr, c)] = m
    return cells


class S13Delta(SpokenScene):
    def construct(self):
        M_, cap, cap3, p1, p2, q = delta_prompt_frame(self)
        self.at("did not become")
        nn = plain_chip("not neural", 30).move_to([-1.3, CAP_NORM_Y, 0])
        self.play(FadeOut(q), FadeOut(p1), FadeOut(p2), FadeIn(nn, shift=UP * 0.15), run_time=0.6)
        self.at("still had notch")
        cr = VGroup(*[crescent(spos(r, c), SR, 0.7) for c in MUT_COLS for r in range(SROWS)])
        nl = T("they still have Notch", 30, NOT).move_to([2.6, CAP_MUT_Y, 0])
        self.play(FadeIn(cr), FadeIn(nl, shift=DOWN * 0.1), run_time=0.8)
        self.at("normal neighbors")
        sig = VGroup(*[Arrow(spos(r, 4) + P3(-0.1, 0), spos(r, 3) + P3(0.25, 0), buff=0, color=DEL, stroke_width=5, tip_length=0.2,
                             max_tip_length_to_length_ratio=0.5) for r in range(SROWS)])
        self.play(LaggedStart(*[GrowArrow(s) for s in sig], lag_ratio=0.1), run_time=0.8)
        self.at("not you")
        bb = T("not you", 34, RED, weight=BOLD).move_to([2.6, CAP_MUT_Y, 0])
        swap(self, nl, bb, 0.2)
        self.at("losing the receptor")
        # split the frame in two patches: Notch-mutant (left) and Delta-mutant (right)
        L = patch_cells(-3.55)
        Rr = patch_cells(3.55)
        for rr in range(5):
            paint(L[(rr, 1)], "mutneural")
        crR = VGroup(*[crescent(Rr[(rr, c)].get_center(), 0.55, 0.7) for c in (0, 1) for rr in range(5)])
        sigR = VGroup(*[Arrow(Rr[(rr, 2)].get_center() + P3(-0.1, 0), Rr[(rr, 1)].get_center() + P3(0.22, 0), buff=0, color=DEL, stroke_width=5,
                              tip_length=0.2, max_tip_length_to_length_ratio=0.5) for rr in range(5)])
        hL = T("Notch-mutant", 32, MUT).move_to([-3.55, 3.3, 0])
        hR = T("Delta-mutant", 32, MUT).move_to([3.55, 3.3, 0])
        rL = chip("no receptor: neural", GREEN, 28).move_to([-3.55, -3.3, 0])
        rR = plain_chip("no ligand: not neural", 28).move_to([3.55, -3.3, 0])
        gone = [M_.group, cr, sig, bb, cap, cap3, nn]
        self.play(*[FadeOut(m) for m in gone], FadeIn(VGroup(*L.values())), FadeIn(hL), FadeIn(rL), run_time=0.7)
        self.at("losing the ligand")
        self.play(FadeIn(VGroup(*Rr.values())), FadeIn(hR), FadeIn(crR), FadeIn(rR), LaggedStart(*[GrowArrow(s) for s in sigR], lag_ratio=0.1), run_time=0.9)
        self.at("not the same")
        ne = VGroup(Line(P3(-0.35, 0.17), P3(0.35, 0.17), color=GOLD, stroke_width=9), Line(P3(-0.35, -0.17), P3(0.35, -0.17), color=GOLD, stroke_width=9),
                    Line(P3(-0.28, -0.55), P3(0.28, 0.55), color=GOLD, stroke_width=9)).move_to([0, 0.1, 0])
        self.play(FadeIn(ne, scale=0.7), Indicate(rL, color=TEXT, scale_factor=1.06), Indicate(rR, color=TEXT, scale_factor=1.06), run_time=0.8)
        self.finish()


# ------------------------------------------------------------------------------------------
R14, CY14, SP14 = 1.9, -0.5, 4.5
SIDE_Y = -3.25


def row14():
    return mk_row(CY14, R14, SP14, (0.25, 0.6, 0.25), "norm")


class S14Predict2(SpokenScene):
    def construct(self):
        p1 = T("Predict again.", 36, GOLD, weight=BOLD).move_to([0, 3.45, 0])
        row = row14()
        bodies, cres = row[0:3], row[3:6]
        self.add(p1)
        self.play(LaggedStart(*[FadeIn(b) for b in bodies], lag_ratio=0.2), run_time=0.8)
        self.at("a normal cell")
        l_mid = chip("a normal cell", GREY, 26, pad=0.16).move_to([0, SIDE_Y, 0])
        self.play(FadeIn(cres[1], scale=0.7), FadeIn(l_mid, shift=UP * 0.1), run_time=0.6)
        self.at("beside cells")
        self.play(Indicate(bodies[0], color=TEXT, scale_factor=1.04), Indicate(bodies[2], color=TEXT, scale_factor=1.04), run_time=0.8)
        self.at("with less notch")
        l_side = [T("less Notch activity", 26, NOT).move_to([x, SIDE_Y, 0]) for x in (-SP14, SP14)]
        self.play(FadeIn(cres[0], scale=0.7), FadeIn(cres[2], scale=0.7), *[FadeIn(l, shift=UP * 0.1) for l in l_side], run_time=0.7)
        self.at("than its own")
        self.play(Indicate(cres[1], color=TEXT, scale_factor=1.15), run_time=0.8)
        self.at("what does it become")
        q = T("?", 90, GOLD, font=TITLE_FONT).move_to([0, 2.3, 0])
        self.play(FadeIn(q), run_time=0.5)
        self.finish()


def prompt2_frame(scene):
    p1 = T("Predict again.", 36, GOLD, weight=BOLD).move_to([0, 3.45, 0])
    row = row14()
    l_mid = chip("a normal cell", GREY, 26, pad=0.16).move_to([0, SIDE_Y, 0])
    l_side = [T("less Notch activity", 26, NOT).move_to([x, SIDE_Y, 0]) for x in (-SP14, SP14)]
    q = T("?", 90, GOLD, font=TITLE_FONT).move_to([0, 2.3, 0])
    scene.add(p1, row, l_mid, *l_side, q)
    return p1, row, l_mid, l_side, q


class S15Pause(NarratedScene):
    def construct(self):
        prompt2_frame(self)
        pos = P3(6.25, 3.45)
        face, hand = clock(pos, 0.36)
        self.add(face, hand)
        self.play(Rotate(hand, angle=-2 * PI, about_point=pos, rate_func=linear), run_time=4.6)
        self.finish()


class S16Reveal(SpokenScene):
    def construct(self):
        p1, row, l_mid, l_side, q = prompt2_frame(self)
        self.at("became epidermis")
        row_e = mk_row(CY14, R14, SP14, (0.25, 0.6, 0.25), "epi")
        ep = T("epidermis", 32, TEXT).move_to([0, CY14 - 0.95, 0])
        self.play(FadeOut(q), FadeOut(p1), FadeOut(l_mid), ReplacementTransform(row, row_e), run_time=0.8)
        self.play(FadeIn(ep, shift=UP * 0.1), run_time=0.4)
        self.at("with more notch")
        RY1, RY2, RSP, RR = 1.6, -1.55, 3.9, 1.15
        top = mk_row(RY1, RR, RSP, (0.25, 0.6, 0.25), "epi")
        ep_to = T("epidermis", 28, TEXT).move_to([0, RY1 - 0.7, 0])
        inset = mk_row(RY2, RR, RSP, (1.0, 0.6, 1.0), "norm")
        more = [T("more Notch activity", 26, NOT).move_to([x, -3.15, 0]) for x in (-RSP, RSP)]
        self.play(ReplacementTransform(row_e, top), ReplacementTransform(ep, ep_to),
                  *[l_side[i].animate.move_to([x, RY1 - 1.6, 0]) for i, x in enumerate((-RSP, RSP))], run_time=0.9)
        self.play(FadeIn(inset, shift=UP * 0.2), *[FadeIn(m) for m in more], run_time=0.8)
        self.at("the same cell")
        self.play(Indicate(inset[1], color=TEXT, scale_factor=1.12), run_time=0.8)
        self.at("neural precursor")
        ins2 = mk_row(RY2, RR, RSP, (1.0, 0.6, 1.0), "neural")
        nl = T("neural precursor", 28, GREEN).move_to([0, -3.15, 0])
        self.play(ReplacementTransform(inset, ins2), FadeIn(nl, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ------------------------------------------------------------------------------------------
def outcome_tag(word, color, sub):
    return VGroup(T(word, 40, color), T(sub, 26, NOT)).arrange(DOWN, buff=0.15).move_to([0, 2.0, 0])


class S17Relative(SpokenScene):
    def construct(self):
        Bal = Balance()
        hd = T("relative Notch activity biases fate", 36, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
        ll = T("its neighbours'\nNotch", 28, TEXT, line_spacing=0.8).move_to([-4.4, -2.9, 0])
        lr = T("this cell's\nNotch", 28, TEXT, line_spacing=0.8).move_to([4.4, -2.9, 0])
        self.add(Bal.stand, Bal.beam, hd, ll, lr)
        self.add(Bal.bowl_l, Bal.bowl_r)
        self.at("a cell's fate")
        Bal.lv.set_value(0.55)
        Bal.rv.set_value(0.55)
        self.play(Bal.lvis.animate.set_value(1), Bal.rvis.animate.set_value(1), run_time=0.5)
        t1 = outcome_tag("epidermis", GREY, "more Notch than its neighbours")
        self.play(Bal.lv.animate.set_value(0.35), Bal.rv.animate.set_value(1.0), Bal.tilt.animate.set_value(-0.3), FadeIn(t1, shift=DOWN * 0.1), run_time=1.0)
        self.at("relative to")
        t2 = outcome_tag("neural precursor", GREEN, "less Notch than its neighbours")
        self.play(FadeOut(t1), run_time=0.2)
        self.play(Bal.lv.animate.set_value(1.0), Bal.rv.animate.set_value(0.35), Bal.tilt.animate.set_value(0.3), FadeIn(t2, shift=DOWN * 0.1), run_time=1.0)
        self.finish()


# ------------------------------------------------------------------------------------------
def legend():
    s1 = Square(0.3, stroke_width=0, fill_color=PRO, fill_opacity=0.95)
    t1 = T("proneural factor", 26, PRO)
    s2 = Square(0.3, stroke_width=0, fill_color=REP, fill_opacity=0.95)
    t2 = T("E(spl) repressor, driven by Notch", 26, REP)
    return VGroup(VGroup(s1, t1).arrange(RIGHT, buff=0.15), VGroup(s2, t2).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.7).move_to([0, 3.45, 0])


CHIP_Y = -3.4


class S18Table(SpokenScene):
    def construct(self):
        A, B = pair_cells()
        base_vals(A, B)
        for c in (A, B):
            c.setv(pro=0, rep=0)
        lg = legend()
        self.add(*A.dyn, *B.dyn)
        self.add(A.static, B.static, A.tracks, B.tracks, lg)
        self.wait(0.2)
        self.play(*A.to(pro=0.5, rep=0.35), *B.to(pro=0.5, rep=0.35), run_time=0.6)
        self.at("give cell")
        self.play(Indicate(A.body, color=TEXT, scale_factor=1.03), run_time=0.5)
        self.at("half the normal")
        A.cs.set_value(0.7)
        ch = half_chip(A)
        A.cs.set_value(1.0)
        self.play(*A.to(cs=0.7), FadeIn(ch, shift=UP * 0.1), run_time=0.9)
        self.finish()


def half_chip(A):
    ch = chip("half the normal Notch", NOT, 26, pad=0.16).move_to([-0.3, CHIP_Y + 0.1, 0])
    ld = Line(ch.get_top() + P3(-0.2, 0), A.cup_c() + P3(0.0, -0.4), color=NOT, stroke_width=3)
    return VGroup(ld, ch)


def pair_half(scene):
    A, B = pair_cells()
    base_vals(A, B)
    A.setv(cs=0.7)
    A.put(scene)
    B.put(scene)
    lg = legend()
    ch = half_chip(A)
    scene.add(lg, ch)
    return A, B, ch, lg


class S19Table2(SpokenScene):
    def construct(self):
        A, B, ch, lg = pair_half(self)
        self.at("hears its")
        self.play(FadeOut(ch), *A.to(notch=0.1, rep=0.2), run_time=0.9)
        self.at("keeps more")
        self.play(*A.to(pro=0.85, delta=0.8), run_time=0.9)
        self.at("wins")
        na = chip("A: neural", GREEN, 30).move_to([-3.85, CHIP_Y, 0])
        nb = chip("B: epidermis", GREY, 30).move_to([3.85, CHIP_Y, 0])
        self.play(*A.win(), *B.lose(), *A.to(delta=0.9, rep=0.1), *B.to(notch=0.75, rep=0.8, pro=0.15, delta=0.2), run_time=1.0)
        self.play(FadeIn(na, shift=UP * 0.15), FadeIn(nb, shift=UP * 0.15), run_time=0.4)
        self.at("the logic")
        gl = T("the logic of the mosaics, in miniature", 32, GOLD).move_to([0, 3.4, 0])
        self.play(FadeOut(lg), run_time=0.2)
        self.play(FadeIn(gl, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ------------------------------------------------------------------------------------------
def arc_inh(p0, p1, bend=-1.2, color=RED, w=7):
    arc = ArcBetweenPoints(np.array(p0, float), np.array(p1, float), angle=bend, color=color, stroke_width=w)
    end = arc.get_end()
    d = end - arc.point_from_proportion(0.96)
    d = d / np.linalg.norm(d)
    perp = np.array([-d[1], d[0], 0])
    return VGroup(arc, Line(end + perp * 0.3, end - perp * 0.3, color=color, stroke_width=w + 3))


def loop_inh(p0, p1, h=1.4, color=RED, w=7):
    """A red inhibitory arc that leaves p0, rises by h and comes down on p1 with a flat bar."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    up = P3(0, h)
    cb = CubicBezier(p0, p0 + up, p1 + up, p1, color=color, stroke_width=w)
    bar = Line(p1 + P3(-0.32, 0.0), p1 + P3(0.32, 0.0), color=color, stroke_width=w + 3)
    return VGroup(cb, bar)


def pair_end(scene):
    A, B = pair_cells()
    A.setv(cs=0.7)
    end_vals(A, B)
    A.win_now()
    B.lose_now()
    A.put(scene)
    B.put(scene)
    return A, B


class S20Compete(SpokenScene):
    def construct(self):
        A, B = pair_end(self)
        cy = A.cy
        na = chip("A: neural", GREEN, 30).move_to([-3.85, CHIP_Y, 0])
        nb = chip("B: epidermis", GREY, 30).move_to([3.85, CHIP_Y, 0])
        nm = T("Heitzler and Simpson", 34, GOLD).move_to([0, 3.4, 0])
        self.add(na, nb)
        self.play(FadeIn(nm, shift=DOWN * 0.1), run_time=0.4)
        self.at("that the cells")
        self.play(FadeOut(nm), run_time=0.25)
        ya = cy - 1.85
        pa = Arrow([-1.9, ya, 0], [-0.25, ya, 0], buff=0, color=TEXT, stroke_width=16, tip_length=0.4, max_tip_length_to_length_ratio=0.6)
        pb = Arrow([1.9, ya, 0], [0.25, ya, 0], buff=0, color=TEXT, stroke_width=16, tip_length=0.4, max_tip_length_to_length_ratio=0.6)
        cp = T("competition", 32, GOLD).move_to([0, ya - 0.8, 0])
        self.play(GrowArrow(pa), GrowArrow(pb), FadeIn(cp, shift=DOWN * 0.1), run_time=0.6)
        self.at("notch receives")
        self.play(Indicate(B.cup, color=TEXT, scale_factor=1.25), run_time=0.8)
        self.at("an inhibitory signal")
        # A's Delta ball steps back from B's receptor so the inhibitory signal can be drawn from the ball to the receptor
        self.play(FadeOut(cp), FadeOut(pa), FadeOut(pb), *A.to(bind=0.1), run_time=0.5)
        p0 = A.knob_c() + P3(0.15, 0.42)
        p1 = B.cup_c() + P3(0.0, 0.55)
        sg = loop_inh(p0, p1, 1.1)
        tx = T("inhibitory signal", 32, RED).move_to([(p0[0] + p1[0]) / 2, p0[1] + 1.55, 0])
        self.play(Create(sg), FadeIn(tx, shift=UP * 0.1), run_time=0.7)
        self.at("the precursors")
        pr = chip("A: precursor", GREEN, 30).move_to([-3.85, CHIP_Y, 0])
        swap(self, na, pr, 0.25)
        self.finish()


# ------------------------------------------------------------------------------------------
XA_, XB_ = -3.35, 3.35
ROW_T, ROW_B = 0.95, -1.85


class Loop:
    def __init__(self):
        cellA = RoundedRectangle(corner_radius=0.3, width=5.15, height=5.1, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                                 fill_opacity=0.08).move_to([-4.075, -0.35, 0])
        cellB = cellA.copy().move_to([4.075, -0.35, 0])
        labA = T("cell A", 28, GREY).move_to([XA_, 1.8, 0])
        labB = T("cell B", 28, GREY).move_to([XB_, 1.8, 0])
        self.cells = VGroup(cellA, cellB, labA, labB)
        self.dA = chip("Delta", YELLOW, 28, pad=0.16).move_to([XA_, ROW_T, 0])
        self.nA = chip("Notch activity", BLUE, 26, pad=0.16).move_to([XA_, ROW_B, 0])
        self.nB = chip("Notch activity", BLUE, 26, pad=0.16).move_to([XB_, ROW_T, 0])
        self.dB = chip("Delta", YELLOW, 28, pad=0.16).move_to([XB_, ROW_B, 0])
        self.chips = VGroup(self.dA, self.nA, self.nB, self.dB)
        hh = self.dA.height / 2
        self.s_top = Arrow([self.dA.get_right()[0] + 0.05, ROW_T, 0], [self.nB.get_left()[0] - 0.05, ROW_T, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.24)
        self.s_bot = Arrow([self.dB.get_left()[0] - 0.05, ROW_B, 0], [self.nA.get_right()[0] + 0.05, ROW_B, 0], buff=0, color=YELLOW, stroke_width=5, tip_length=0.24)
        self.s_inB = inhib([XB_, ROW_T - hh - 0.05, 0], [XB_, ROW_B + hh + 0.05, 0])
        self.s_inA = inhib([XA_, ROW_B + hh + 0.05, 0], [XA_, ROW_T - hh - 0.05, 0])
        self.arrows = VGroup(self.s_top, self.s_inB, self.s_bot, self.s_inA)
        self.seg = [(P3(self.dA.get_right()[0] + 0.1, ROW_T), P3(self.nB.get_left()[0] - 0.1, ROW_T)),
                    (P3(XB_, ROW_T - hh - 0.1), P3(XB_, ROW_B + hh + 0.1)),
                    (P3(self.dB.get_left()[0] - 0.1, ROW_B), P3(self.nA.get_right()[0] + 0.1, ROW_B)),
                    (P3(XA_, ROW_B + hh + 0.1), P3(XA_, ROW_T - hh - 0.1))]


class S21Model(SpokenScene):
    def construct(self):
        A, B = pair_end(self)
        L = Loop()
        hd = T("lateral inhibition with feedback", 38, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.add(hd)
        self.at("that picture")
        A.freeze()
        B.freeze()
        self.play(*[FadeOut(m) for m in (A.static, A.tracks, *A.dyn, B.static, B.tracks, *B.dyn)],
                  FadeIn(L.cells), FadeIn(L.chips), *[FadeIn(a) for a in L.arrows], run_time=0.6)
        self.at("lateral inhibition")
        self.play(Indicate(L.s_inA, color=TEXT, scale_factor=1.15), Indicate(L.s_inB, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.at("feedback")
        dot = Dot(radius=0.16, color=TEXT).move_to(L.seg[0][0])
        self.add(dot)
        for i in range(4):
            if i:
                dot.move_to(L.seg[i][0])
            self.play(dot.animate.move_to(L.seg[i][1]), run_time=0.32, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.2)
        self.at("mathematical model")
        mm = T("a mathematical model", 40, GOLD, font=TITLE_FONT).move_to([0, 3.4, 0])
        swap(self, hd, mm, 0.25)
        self.finish()


# ------------------------------------------------------------------------------------------
def spaced_sheet(seed=2, rows=4, cols=9):
    def nb(r, c):
        out = [(r, c - 1), (r, c + 1)]
        out += [(r - 1, c - 1), (r - 1, c), (r + 1, c - 1), (r + 1, c)] if r % 2 == 0 else [(r - 1, c), (r - 1, c + 1), (r + 1, c), (r + 1, c + 1)]
        return [(a, b) for a, b in out if 0 <= a < rows and 0 <= b < cols]
    f = lambda x: x * x / (0.01 + x * x)
    g = lambda x: 1 / (1 + 100 * x * x)
    rng = np.random.default_rng(seed)
    d = 0.5 + 0.02 * rng.standard_normal((rows, cols))
    n = np.full((rows, cols), 0.5)
    nbs = {(r, c): nb(r, c) for r in range(rows) for c in range(cols)}
    for _ in range(6000):
        nn = np.zeros_like(n)
        for (r, c), lst in nbs.items():
            nn[r, c] = f(np.mean([d[a, b] for a, b in lst]))
        n = n + 0.05 * (nn - n)
        d = d + 0.05 * (g(n) - d)
    return d > 0.5


def card(y, n, color, h=1.3, op=1.0):
    box = RoundedRectangle(corner_radius=0.25, width=11.6, height=h, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.10 * op).move_to([0.4, y, 0]).set_stroke(opacity=op)
    num = VGroup(Circle(radius=0.45, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.15),
                 T(str(n), 38, GOLD, TITLE_FONT)).move_to([-4.6, y, 0])
    return box, num


class S22Answer(SpokenScene):
    def construct(self):
        ys = [2.85, 1.6, 0.35]
        cols = [GREEN, NOT, GREY]
        cs = [card(y, n + 1, c, 1.1, 0.35) for n, (y, c) in enumerate(zip(ys, cols))]
        t1 = T("Who may become neural?", 38, GREEN).move_to([-3.6, ys[0], 0], aligned_edge=LEFT).set_opacity(0.45)
        t2 = T("Who does?", 38, NOT).move_to([-3.6, ys[1], 0], aligned_edge=LEFT).set_opacity(0.45)
        t3 = T("Does the logic carry over to vertebrates?", 32, TEXT).move_to([-3.6, ys[2], 0], aligned_edge=LEFT).set_opacity(0.45)
        self.add(*[b for b, n in cs], *[n for b, n in cs], t1, t2, t3)
        self.wait(0.3)
        self.at("second puzzle")
        b2 = card(ys[1], 2, NOT, 1.1, 1.0)[0]
        ck = check_mark([5.45, ys[1], 0], 0.55, GREEN, 12)
        win = spaced_sheet()
        d, r_, cx, cy = 0.78, 0.33, 3.0, -2.15
        cells = {}
        for r in range(4):
            for c in range(9):
                p = P3(cx + (c - 4) * d + (r % 2 - 0.5) * d / 2, cy + (1.5 - r) * d * 0.866)
                m = Circle(radius=r_).move_to(p)
                paint(m, "norm")
                cells[(r, c)] = m
        sheet = VGroup(*cells.values())
        self.play(ReplacementTransform(cs[1][0], b2), t2.animate.set_opacity(1), Create(ck),
                  LaggedStart(*[GrowFromCenter(m) for m in sheet], lag_ratio=0.012), run_time=1.0)
        self.at("one qualification")
        fn = T("* spacing", 32, GOLD).move_to([3.9, ys[1], 0])
        self.play(FadeIn(fn, shift=LEFT * 0.15), Indicate(sheet, color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("in a sheet")
        cap = T("In a sheet,\nthe loop alone\ngives spaced winners.", 28, TEXT, line_spacing=0.8).move_to([-6.4, -2.15, 0], aligned_edge=LEFT)
        self.play(FadeIn(cap, shift=RIGHT * 0.15), run_time=0.6)
        self.at("the loop alone")
        winners = [cells[(r, c)] for r in range(4) for c in range(9) if win[r, c]]
        self.play(LaggedStart(*[to_kind(m, "neural") for m in winners], lag_ratio=0.1), run_time=1.3)
        self.finish()


# ------------------------------------------------------------------------------------------
class S23Takeaway(SpokenScene):
    def construct(self):
        R = 2.3
        cy = 0.0
        bA = Circle(radius=R).move_to([-3.4, cy, 0])
        bB = Circle(radius=R).move_to([3.4, cy, 0])
        paint(bA, "norm")
        paint(bB, "norm")
        cA = crescent([-3.4, cy, 0], R, 0.3)
        cB = crescent([3.4, cy, 0], R, 0.9)
        hd = T("Compare, then decide", 40, TEXT, font=TITLE_FONT).move_to([0, 3.3, 0])
        self.add(hd, bA, bB)
        self.play(AnimationGroup(FadeIn(cA, scale=0.7), FadeIn(cB, scale=0.7), lag_ratio=0.5), run_time=0.5)
        self.at("compare")
        cmp_ = DoubleArrow([-0.85, cy, 0], [0.85, cy, 0], color=GOLD, stroke_width=7, buff=0, tip_length=0.26)
        cl = T("compare", 30, GOLD).move_to([0, cy + 0.55, 0])
        self.play(GrowFromCenter(cmp_), FadeIn(cl), run_time=0.6)
        self.at("notch signals")
        ls = [T("less Notch signal", 28, NOT).move_to([-3.4, cy - 2.8, 0]), T("more Notch signal", 28, NOT).move_to([3.4, cy - 2.8, 0])]
        self.play(*[FadeIn(l, shift=UP * 0.1) for l in ls], run_time=0.5)
        self.at("the comparison")
        self.play(Indicate(cmp_, color=TEXT, scale_factor=1.1), run_time=0.7)
        self.at("decide")
        ra = chip("neural", GREEN, 30).move_to([-3.4, -3.5, 0])
        rb = chip("epidermis", GREY, 30).move_to([3.4, -3.5, 0])
        self.play(to_kind(bA, "neural"), to_kind(bB, "epi"),
                  FadeIn(ra, shift=UP * 0.1), FadeIn(rb, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S24End(EndCard):
    LINE = "Neighbours compare Notch signals, and the comparison helps decide the winner."

    def construct(self):
        line = T("Neighbours compare Notch signals,\nand the comparison helps\ndecide the winner.", 44, font=TITLE_FONT, line_spacing=0.9)
        box = RoundedRectangle(corner_radius=0.3, width=line.width + 1.0, height=line.height + 0.9, stroke_color=GOLD, stroke_width=4,
                               fill_color=GOLD, fill_opacity=0.07)
        card_ = VGroup(box, line.move_to(box))
        sub = T("biochemistrypedia.com", 26, TEAL)
        g = VGroup(card_, sub).arrange(DOWN, buff=0.4)
        fit(g, max_w=12.4, max_h=7.0)
        self.add(card_)
        self.wait(0.3)
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
