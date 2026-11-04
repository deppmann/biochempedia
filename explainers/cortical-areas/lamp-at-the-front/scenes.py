"""Mapping the Cortex: Areas and Arealization, chapter 3: A Lamp at the Front  (Biochemistrypedia chaptered film)

The recurring picture is the dorsal map drawn as a flat bar, front on the LEFT, back on the RIGHT (the working model's
four abstract bands; the top edge is the medial edge). Under it, a plot of the FGF8 level along the same axis. Every
curve, border and crossing is computed from the lesson's equation C = C0 exp(-x/lambda) (lambda = 0.3 of the sheet,
borders at 0.15, 0.42, 0.70 of the way back, thresholds T = C0 exp(-border/lambda)); the ramp in s27 is C = C0 (1 - x).
The second lamp at the back (s21, s22) adds a short-range term 0.55 exp(-(1 - x)/0.06), so the first three borders
stay where they were and only a new crossing appears near the back.

COLOR MAP (one color per concept, shared with every chapter of this lesson)
  PURPLE = front band (motor side)      GREEN = second band (touch side), and the barrels
  SAND   = third band                   PINK  = back band (visual side)
  YELLOW = FGF8 and the lamp (the curve, the glow under it, the shift arrows and the "shift" label)
  ORANGE = cortical hem, Wnt and BMP
  TEAL   = injected DNA and the cells that took it up, the model tags
  BLUE   = lambda, the decay length
  TEXT   = cells, labels that matter, equations
  RED    = a blocker / something removed or lost
  INNER  = the second, inner gradient that the lamp helps set (named in a later chapter)
  GREY   = the sheet, axes, thresholds, de-emphasised things (labels use the lighter GREY_L)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#E58BB5"
SAND = "#D9B77E"
INNER = "#9FB1FF"
PALEY = "#FFF3B0"
THR = "#AEB6C8"
ORANGE = "#F2994A"
GREY_L = "#C3CAD6"
BAND = [PURPLE, GREEN, SAND, PINK]
BNAME = ["motor", "touch", "abstract", "vision"]

X0, W = -4.6, 9.4            # the sheet along x
LX = X0 - 0.25               # the lamp sits just outside the front edge
RX = X0 + W + 0.25           # the second lamp sits just outside the back edge
LAM = 0.3                    # decay length, as a fraction of the sheet
LAM2 = 0.06                  # decay length of the (short-range) second lamp
BACK = 0.55                  # strength of the second lamp
FA = np.array([0.15, 0.42, 0.70])
TH_EXP = np.exp(-FA / LAM)   # thresholds that put the borders at FA when C0 = 1
TH_RAMP = 1 - FA
YMAX = 2.1                   # top of the plot, in units of the normal C0
CY, MH = 2.2, 1.3            # the map's centre line and height; the plot sits under it
PB, PH = -3.0, 3.5
UP_A, DOWN_A = 2.0, 0.5      # the lamp doubled and halved (same factor in every scene)


def px(f):
    return X0 + f * W


def lab(text, x, y, size=26, color=GREY_L, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def tag(text, x, y, size=26, color=TEXT, bg=0.88, weight=NORMAL, anchor="c"):
    """A label with a dark backing so no line shows through the letters."""
    t = T(text, size, color, weight=weight)
    if anchor == "l":
        t.move_to([x + t.width / 2, y, 0])
    elif anchor == "r":
        t.move_to([x - t.width / 2, y, 0])
    else:
        t.move_to([x, y, 0])
    b = RoundedRectangle(corner_radius=0.08, width=t.width + 0.24, height=t.height + 0.18, stroke_width=0,
                         fill_color=BG, fill_opacity=bg).move_to(t)
    return VGroup(b, t)


def prompt(text, y=3.35, size=30):
    t = T(text, size, TEXT, font=TITLE_FONT)
    fit(t, max_w=12.4)
    return t.move_to([0, y, 0])


def glow(x, y, r=0.34, dim=1.0, color=YELLOW):
    g = VGroup()
    for k, o in ((2.6, 0.08), (1.9, 0.14), (1.35, 0.25)):
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=color, fill_opacity=o * dim))
    g.add(Circle(radius=r, stroke_color=color, stroke_width=3, stroke_opacity=max(0.3, dim), fill_color=color,
                 fill_opacity=0.95 * dim))
    return g.move_to([x, y, 0])


def cell(x, y, r=0.13, color=TEXT, fo=0.7):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fo).move_to([x, y, 0])


def x_mark(x, y, r=0.4, color=RED, sw=8):
    return VGroup(Line([x - r, y - r, 0], [x + r, y + r, 0], stroke_color=color, stroke_width=sw),
                  Line([x - r, y + r, 0], [x + r, y - r, 0], stroke_color=color, stroke_width=sw))


def arrow(a, b, color=TEXT, sw=6, tip=0.22):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0, color=color, stroke_width=sw, tip_length=tip,
                 max_stroke_width_to_length_ratio=100, max_tip_length_to_length_ratio=0.45)


ROWS = [4, 5, 5, 4]          # barrels per row, top row first


def barrel_rows(cx, cy, sp=0.2, r=0.07, rows=ROWS, color=GREEN, op=0.85):
    """The barrel field: one VGroup per row (top row first)."""
    g = VGroup()
    for j, n in enumerate(rows):
        y = cy + ((len(rows) - 1) / 2 - j) * sp
        g.add(VGroup(*[Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=op).move_to(
            [cx + (i - (n - 1) / 2) * sp, y, 0]) for i in range(n)]))
    return g


def ghost_borders(cy, mh, fs, color=GREY_L, op=0.6):
    g = VGroup()
    for f in fs:
        g.add(DashedLine([px(f), cy - mh / 2, 0], [px(f), cy + mh / 2, 0], dash_length=0.12, stroke_color=color,
                         stroke_width=3, stroke_opacity=op))
    return g


# =============================================================================================
class Stage:
    """The map (top) and the level plot (bottom), all driven by trackers so a scene can slide the borders."""

    KEYS = ("map", "ends", "axes", "curve", "glow", "thr", "mk", "dl", "lamp1", "lamp2", "field", "flabel", "p2",
            "plabel", "fglabel", "ghost", "hem", "bl")

    def __init__(self, A=1.0, Bk=0.0, Ab=None, Bb=None, mix=0.0, vis=(), cy=CY, mh=MH, rev=1.0, pb=PB, ph=PH):
        self.pb, self.ph = pb, ph
        self.tA, self.tB = ValueTracker(A), ValueTracker(Bk)                       # the curve
        self.tAb = ValueTracker(A if Ab is None else Ab)                           # the level the borders follow
        self.tBb = ValueTracker(Bk if Bb is None else Bb)
        self.tmix, self.rev, self.pulse = ValueTracker(mix), ValueTracker(rev), ValueTracker(1.0)
        self.cy, self.mh = ValueTracker(cy), ValueTracker(mh)
        self.lamp_dx = ValueTracker(0.0)
        self.v = {k: ValueTracker(1.0 if k in vis else 0.0) for k in self.KEYS}
        self.v["ghost"].set_value(1.0)
        self.m = {}
        order = [("map", self._map), ("hem", self._hem), ("ends", self._ends), ("axes", self._axes), ("glow", self._glow),
                 ("ghost", self._ghost), ("curve", self._curve), ("thr", self._thr), ("field", self._field),
                 ("p2", self._p2), ("dl", self._dl), ("mk", self._mk), ("lamps", self._lamps), ("fglabel", self._fglabel)]
        self.mobs = []
        for name, fn in order:
            mob = always_redraw(fn)
            self.m[name] = mob
            self.mobs.append(mob)

    def install(self, scene):
        scene.add(*self.mobs)

    # ---- geometry ----
    @property
    def ys(self):
        return self.ph / YMAX

    def py(self, level):
        return self.pb + level * self.ys

    @staticmethod
    def _lev(f, A, B, mix):
        f = np.asarray(f, float)
        e = A * np.exp(-f / LAM) + B * np.exp(-np.maximum(1 - f, 0) / LAM2)
        return (1 - mix) * e + mix * A * (1 - f)

    def levc(self, f):
        return self._lev(np.asarray(f, float), self.tA.get_value(), self.tB.get_value(), self.tmix.get_value())

    def levb(self, f):
        return self._lev(np.asarray(f, float), self.tAb.get_value(), self.tBb.get_value(), self.tmix.get_value())

    def thr(self):
        m = self.tmix.get_value()
        return (1 - m) * TH_EXP + m * TH_RAMP

    def crossings(self):
        f = np.linspace(-0.2003, 1.2001, 1401)
        L = self.levb(f)
        out = []
        for i, t in enumerate(self.thr()):
            d = L - t
            for k in np.nonzero(d[:-1] * d[1:] < 0)[0]:
                out.append((f[k] + d[k] / (d[k] - d[k + 1]) * (f[1] - f[0]), i))
        return sorted(out)

    def segs(self):
        cr = sorted({round(float(f), 5) for f, i in self.crossings() if 0 < f < 1})
        edges = [0.0] + cr + [1.0]
        T_ = self.thr()
        out = []
        for a, b in zip(edges[:-1], edges[1:]):
            if b - a < 1e-4:
                continue
            L = float(self.levb(np.array([(a + b) / 2]))[0])
            out.append((a, b, int(np.sum(T_ > L))))
        return out

    def field_x(self, which="first"):
        g = [(a + b) / 2 for a, b, i in self.segs() if i == 1]
        if not g:
            return None
        return px(g[0] if which == "first" else g[-1])

    def n_green(self):
        return sum(1 for a, b, i in self.segs() if i == 1)

    def map_bottom(self):
        return self.cy.get_value() - self.mh.get_value() / 2

    # ---- builders ----
    def _map(self):
        a = self.v["map"].get_value()
        if a < 0.01:
            return VGroup()
        cy, h = self.cy.get_value(), self.mh.get_value()
        g = VGroup()
        segs = self.segs()
        for f0, f1, idx in segs:
            g.add(Rectangle(width=(f1 - f0) * W, height=h, stroke_width=0, fill_color=BAND[idx],
                            fill_opacity=0.42 * a).move_to([px((f0 + f1) / 2), cy, 0]))
        for f0, f1, idx in segs[1:]:
            g.add(Line([px(f0), cy - h / 2, 0], [px(f0), cy + h / 2, 0], stroke_color=TEXT, stroke_width=3,
                       stroke_opacity=0.75 * a))
        g.add(Rectangle(width=W, height=h, stroke_color=GREY, stroke_width=3, stroke_opacity=a, fill_opacity=0).move_to(
            [X0 + W / 2, cy, 0]))
        bl = self.v["bl"].get_value()
        if bl > 0.01:
            for f0, f1, idx in segs:
                g.add(T(BNAME[idx], 26, TEXT).set_opacity(bl).move_to([px((f0 + f1) / 2), cy - h / 2 + 0.38, 0]))
        return g

    def _hem(self):
        a = self.v["hem"].get_value()
        if a < 0.01:
            return VGroup()
        y = self.cy.get_value() + self.mh.get_value() / 2
        g = VGroup()
        for hgt, op in ((0.62, 0.10), (0.42, 0.16), (0.24, 0.30)):
            g.add(Rectangle(width=W, height=hgt, stroke_width=0, fill_color=ORANGE, fill_opacity=op * a).move_to(
                [X0 + W / 2, y, 0]))
        g.add(Line([X0, y, 0], [X0 + W, y, 0], stroke_color=ORANGE, stroke_width=8, stroke_opacity=a))
        return g

    def _ends(self):
        a = self.v["ends"].get_value()
        if a < 0.01:
            return VGroup()
        y = self.cy.get_value() - self.mh.get_value() / 2 - 0.38
        return VGroup(T("front", 26, GREY_L).move_to([X0 + 0.5, y, 0]), T("back", 26, GREY_L).move_to([X0 + W - 0.45, y, 0])
                      ).set_opacity(a)

    def _axes(self):
        a = self.v["axes"].get_value()
        if a < 0.01:
            return VGroup()
        pb, top = self.pb, self.pb + self.ph + 0.25
        g = VGroup(
            Arrow([X0, pb, 0], [X0 + W + 0.35, pb, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2),
            Arrow([X0, pb, 0], [X0, top, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2),
            T("FGF8 level", 26, GREY_L).rotate(PI / 2).move_to([X0 - 0.5, pb + self.ph / 2 + 0.1, 0]),
            T("front", 26, GREY_L).move_to([X0 + 0.5, pb - 0.4, 0]),
            T("back", 26, GREY_L).move_to([X0 + W - 0.45, pb - 0.4, 0]))
        return g.set_opacity(a)

    def _curve_pts(self, f, L):
        return [[px(fi), self.py(min(Li, YMAX)), 0] for fi, Li in zip(f, L)]

    def _curve(self):
        a = self.v["curve"].get_value()
        r = self.rev.get_value()
        if a < 0.01 or r < 0.02:
            return VGroup()
        f = np.linspace(0, r, max(8, int(120 * r)))
        pts = self._curve_pts(f, self.levc(f))
        line = VMobject(stroke_color=YELLOW, stroke_width=6, stroke_opacity=a, fill_opacity=0)
        line.set_points_as_corners(pts)
        halo = VMobject(stroke_color=YELLOW, stroke_width=15, stroke_opacity=0.16 * a, fill_opacity=0)
        halo.set_points_as_corners(pts)
        return VGroup(halo, line)

    def _glow(self):
        a = self.v["glow"].get_value()
        r = self.rev.get_value()
        if a < 0.01:
            return VGroup()
        n = 64
        g = VGroup()
        for k in range(n):
            fm = (k + 0.5) / n
            if fm > r:
                break
            L = float(self.levc(np.array([fm]))[0])
            h = min(L, YMAX) * self.ys
            if h < 0.02:
                continue
            g.add(Rectangle(width=W / n + 0.01, height=h, stroke_width=0, fill_color=YELLOW,
                            fill_opacity=a * min(0.6, 0.06 + 0.30 * L)).move_to([px(fm), self.pb + h / 2, 0]))
        return g

    def _ghost(self):
        a = self.v["curve"].get_value() * self.v["ghost"].get_value()
        d = abs(self.tA.get_value() - self.tAb.get_value()) + abs(self.tB.get_value() - self.tBb.get_value())
        if a < 0.01 or d < 0.02:
            return VGroup()
        f = np.linspace(0, 1, 100)
        m = VMobject(stroke_color="#C9B64E", stroke_width=3.5, stroke_opacity=0.85 * a * min(1, d * 3), fill_opacity=0)
        m.set_points_as_corners(self._curve_pts(f, self.levb(f)))
        return DashedVMobject(m, num_dashes=48)

    def _thr(self):
        a = self.v["thr"].get_value()
        if a < 0.01:
            return VGroup()
        g = VGroup()
        for t in self.thr():
            g.add(DashedLine([X0, self.py(t), 0], [X0 + W, self.py(t), 0], dash_length=0.16, stroke_color=THR,
                             stroke_width=2.6, stroke_opacity=0.9 * a))
        return g

    def _dots(self):
        out = []
        for f, i in self.crossings():
            if -0.14 < f < 1.04:
                out.append((f, i))
        return out

    def _mk(self):
        a = self.v["mk"].get_value()
        if a < 0.01:
            return VGroup()
        g = VGroup()
        T_ = self.thr()
        for f, i in self._dots():
            off = f < 0 or f > 1
            if off:
                continue
            g.add(Circle(radius=0.1, stroke_color=TEXT, stroke_width=3, stroke_opacity=a, fill_color=TEXT, fill_opacity=a).move_to(
                [px(f), self.py(T_[i]), 0]))
        return g

    def _dl(self):
        a = self.v["dl"].get_value()
        if a < 0.01:
            return VGroup()
        g = VGroup()
        T_ = self.thr()
        yb = self.map_bottom()
        for f, i in self._dots():
            if 0 < f < 1:
                g.add(DashedLine([px(f), self.py(T_[i]) + 0.1, 0], [px(f), yb, 0], dash_length=0.07, stroke_color=TEXT,
                                 stroke_width=2.4, stroke_opacity=0.8 * a))
        return g

    def _lamps(self):
        g = VGroup()
        cy = self.cy.get_value()
        a1 = self.v["lamp1"].get_value()
        if a1 > 0.01:
            br = 0.55 + 0.45 * self.tA.get_value()
            g.add(glow(LX + self.lamp_dx.get_value(), cy, 0.30 * min(1.35, 0.7 + 0.3 * self.tA.get_value()) * self.pulse.get_value(),
                       dim=a1 * min(1.0, br)))
        a2 = self.v["lamp2"].get_value()
        if a2 > 0.01:
            g.add(glow(RX, cy, 0.24, dim=0.85 * a2))
        return g

    def _field(self):
        a = self.v["field"].get_value()
        x = self.field_x("first")
        if a < 0.01 or x is None:
            return VGroup()
        cy = self.cy.get_value()
        g = barrel_rows(x, cy).set_opacity(a)
        out = VGroup(g)
        fl = self.v["flabel"].get_value()
        if fl > 0.01:
            out.add(T("barrel field", 26, GREEN).set_opacity(fl).move_to([x, self.map_bottom() - 0.28, 0]))
        return out

    def _p2(self):
        a = self.v["p2"].get_value()
        if a < 0.01 or self.n_green() < 2:
            return VGroup()
        x = self.field_x("last")
        cy = self.cy.get_value()
        g = barrel_rows(x, cy, sp=0.13, r=0.04, rows=[2, 3, 3, 2]).set_opacity(a)
        out = VGroup(g)
        pl = self.v["plabel"].get_value()
        if pl > 0.01:
            out.add(T("partial second field", 26, GREEN).set_opacity(pl).move_to(
                [min(x, 4.2) - 0.1, cy + self.mh.get_value() / 2 + 0.3, 0]))
        return out

    def _fglabel(self):
        a = self.v["fglabel"].get_value()
        if a < 0.01:
            return VGroup()
        dx = self.lamp_dx.get_value()
        x, y = (LX + dx, self.cy.get_value() + 0.85) if abs(dx) > 0.01 else (LX - 1.0, self.cy.get_value())
        return T("FGF8", 28, YELLOW, weight=BOLD).set_opacity(a).move_to([x, y, 0])


def tag_model(text="working model", color=TEAL):
    t = T(text, 26, color)
    b = RoundedRectangle(corner_radius=0.12, width=t.width + 0.4, height=t.height + 0.3, stroke_color=color,
                         stroke_width=2, fill_color=BG, fill_opacity=0.9)
    return VGroup(b, t.move_to(b)).move_to([0.2, -3.5, 0])


def tag_working_model():
    return tag_model("working model", TEAL)


class Probe:
    """A cell on the map and the level it reads on the curve (the vertical drop, the dot, the horizontal tick).
    The cell sits on the lower edge of the map so it never lands on the barrel field."""

    def __init__(self, st, f, vis=0.0, color=TEXT):
        self.st, self.f, self.color = st, f, color
        self.tf = ValueTracker(f)
        self.v = ValueTracker(vis)
        self.mob = always_redraw(self._build)

    def _build(self):
        a = self.v.get_value()
        if a < 0.01:
            return VGroup()
        st = self.st
        f = self.tf.get_value()
        x = px(f)
        y = st.py(min(float(st.levc(np.array([f]))[0]), YMAX))
        cy = st.cy.get_value()
        cyy = cy - st.mh.get_value() / 2 + 0.16
        g = VGroup(
            DashedLine([x, cyy - 0.12, 0], [x, y, 0], dash_length=0.09, stroke_color=self.color, stroke_width=3, stroke_opacity=a),
            DashedLine([X0, y, 0], [x, y, 0], dash_length=0.09, stroke_color=self.color, stroke_width=3, stroke_opacity=a),
            Dot([x, y, 0], radius=0.11, color=self.color).set_opacity(a),
            cell(x, cyy, 0.12, self.color).set_opacity(a))
        return g


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Mapping the Cortex: Areas and Arealization"
    TITLE = "A Lamp at the Front"


# ---------------------------------------------------------------------------------------------
BIG_CY, BIG_MH = 0.1, 2.8      # the big map used while the sources are introduced (s01 to s04)


def big_stage(vis=("map", "ends")):
    return Stage(vis=vis, cy=BIG_CY, mh=BIG_MH)


class S01(SpokenScene):
    """The dorsal map, a small lamp at its front edge, and the question."""

    def construct(self):
        st = big_stage(vis=())
        st.install(self)
        q = T("Can one signal at the edge of the sheet\ndecide where a border falls?", 36, TEXT, font=TITLE_FONT,
              line_spacing=0.95).move_to([0, 2.75, 0])
        self.play(st.v["map"].animate.set_value(1), st.v["ends"].animate.set_value(1), run_time=0.9)
        self.at("at the edge")
        self.play(st.v["lamp1"].animate.set_value(1), run_time=0.6)
        self.at("decide where")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
        ln = Line([px(FA[1]), BIG_CY - BIG_MH / 2, 0], [px(FA[1]), BIG_CY + BIG_MH / 2, 0], stroke_color=TEXT, stroke_width=8)
        self.at("border falls")
        self.play(Create(ln), run_time=0.4)
        self.play(FadeOut(ln), run_time=0.5)
        self.finish()


class S02(SpokenScene):
    """The bands get names; a gradient across the sheet needs a source (a question mark at the front)."""

    def construct(self):
        st = big_stage(vis=("map", "ends", "lamp1"))
        st.install(self)
        q = T("Can one signal at the edge of the sheet\ndecide where a border falls?", 36, TEXT, font=TITLE_FONT,
              line_spacing=0.95).move_to([0, 2.75, 0])
        self.add(q)
        self.play(FadeOut(q), st.v["lamp1"].animate.set_value(0), st.v["bl"].animate.set_value(1), run_time=0.5)
        n = 80
        wash = VGroup(*[Rectangle(width=W / n + 0.02, height=BIG_MH, stroke_width=0, fill_color=TEXT,
                                  fill_opacity=0.34 * (1 - k / (n - 1)) ** 1.3).move_to([px((k + 0.5) / n), BIG_CY, 0]) for k in range(n)])
        garrow = arrow([X0 + 0.2, BIG_CY + BIG_MH / 2 + 0.55], [X0 + W - 0.2, BIG_CY + BIG_MH / 2 + 0.55], GREY_L, 5, 0.25)
        glab = lab("a gradient across the sheet", 0.1, BIG_CY + BIG_MH / 2 + 1.1, 30, TEXT)
        self.at("gradient")
        self.play(FadeIn(wash), FadeIn(garrow), FadeIn(glab, shift=DOWN * 0.1), run_time=0.8)
        ring = VGroup(Circle(radius=0.42, stroke_width=0, fill_color=YELLOW, fill_opacity=0.16),
                      DashedVMobject(Circle(radius=0.42, stroke_color=YELLOW, stroke_width=7), num_dashes=14)).move_to([LX, BIG_CY, 0])
        qm = T("?", 44, YELLOW, weight=BOLD).move_to([LX, BIG_CY, 0])
        ql = T("source?", 30, YELLOW, weight=BOLD)
        ql.move_to([X0 - 0.35 - ql.width / 2, BIG_CY + 0.85, 0])
        self.at("source of position")
        self.play(FadeIn(ring, scale=0.6), FadeIn(qm, scale=0.6), FadeIn(ql, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


class S03(SpokenScene):
    """Two glowing sources: the medial edge (the top edge of the map) and the front."""

    def construct(self):
        st = big_stage(vis=("map", "ends", "bl"))
        st.install(self)
        ring = VGroup(Circle(radius=0.42, stroke_width=0, fill_color=YELLOW, fill_opacity=0.16),
                      DashedVMobject(Circle(radius=0.42, stroke_color=YELLOW, stroke_width=7), num_dashes=14)).move_to([LX, BIG_CY, 0])
        qm = T("?", 44, YELLOW, weight=BOLD).move_to([LX, BIG_CY, 0])
        self.add(ring, qm)
        self.at("signaling centers")
        self.play(st.v["hem"].animate.set_value(1), run_time=0.8)
        self.play(Indicate(st.m["hem"], color=ORANGE, scale_factor=1.04), run_time=0.6)
        self.at("the edges")
        self.play(FadeOut(ring), FadeOut(qm), st.v["lamp1"].animate.set_value(1), run_time=0.6)
        self.play(Indicate(st.m["lamps"], color=YELLOW, scale_factor=1.2), run_time=0.6)
        self.finish()


class S04(SpokenScene):
    """The cortical hem, along the medial edge, releases Wnt and BMP."""

    def construct(self):
        st = big_stage(vis=("map", "ends", "bl", "lamp1", "hem"))
        st.install(self)
        top = BIG_CY + BIG_MH / 2
        l_hem = T("cortical hem", 30, ORANGE, weight=BOLD).move_to([1.6, top + 0.5, 0])
        l_med = T("medial edge", 28, GREY_L).move_to([-3.4, top + 0.5, 0])
        t_hem = Line([1.6, top + 0.26, 0], [1.6, top + 0.08, 0], stroke_color=ORANGE, stroke_width=3)
        t_med = Line([-3.4, top + 0.26, 0], [-3.4, top + 0.08, 0], stroke_color=GREY_L, stroke_width=3)
        self.at("cortical hem")
        self.play(FadeIn(l_hem, shift=DOWN * 0.1), FadeIn(t_hem), Indicate(st.m["hem"], color=ORANGE, scale_factor=1.05), run_time=0.7)
        self.at("medial edge")
        self.play(FadeIn(l_med, shift=DOWN * 0.1), FadeIn(t_med), run_time=0.6)
        self.at("releases")
        rng = np.random.RandomState(7)
        dots = VGroup(*[Circle(radius=0.07, stroke_width=0, fill_color=ORANGE, fill_opacity=0.9).move_to(
            [rng.uniform(-3.5, 4.0), top - 0.12, 0]) for _ in range(14)])
        self.add(dots)
        self.play(*[d.animate.shift(DOWN * rng.uniform(0.7, 1.15)).set_opacity(0.0) for d in dots], run_time=0.75)
        self.remove(dots)
        wnt = chip("Wnt", ORANGE, 30)
        bmp = chip("BMP", ORANGE, 30)
        for c, x in ((wnt, -0.2), (bmp, 2.8)):
            c[0].set_fill(BG, 0.92)
            c.move_to([x, top - 0.95, 0])
        w_arr = arrow([-0.2, top - 0.1], [-0.2, top - 0.5], ORANGE, 5, 0.18)
        b_arr = arrow([2.8, top - 0.1], [2.8, top - 0.5], ORANGE, 5, 0.18)
        self.at("wnt")
        self.play(FadeIn(w_arr), FadeIn(wnt, shift=DOWN * 0.25), run_time=0.5)
        self.at("bmp")
        self.play(FadeIn(b_arr), FadeIn(bmp, shift=DOWN * 0.25), run_time=0.5)
        self.finish()


class S05(SpokenScene):
    """The front source, FGF8, and its curve. The map rises and the plot comes in for the curve."""

    def construct(self):
        st = Stage(vis=("map", "ends", "bl", "lamp1", "hem"), cy=BIG_CY, mh=BIG_MH, rev=0.0)
        st.install(self)
        self.play(st.cy.animate.set_value(CY), st.mh.animate.set_value(MH), st.v["ends"].animate.set_value(0),
                  st.v["bl"].animate.set_value(0), st.v["hem"].animate.set_value(0.35), st.v["axes"].animate.set_value(1),
                  st.v["curve"].animate.set_value(1), run_time=0.8)
        self.at("the front")
        self.play(st.pulse.animate.set_value(1.5), run_time=0.35)
        self.play(st.pulse.animate.set_value(1.0), run_time=0.35)
        self.at("growth factor")
        self.play(st.rev.animate.set_value(1.0), run_time=1.1, rate_func=linear)
        cl = tag("FGF8 level", -2.2, -1.35, 30, YELLOW, weight=BOLD)
        self.at("fgf8")
        self.play(st.v["fglabel"].animate.set_value(1), FadeIn(cl, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
NORM_W = [0.15, 0.27, 0.28, 0.30]
FIN_W = [0.0, 0.34, 0.30, 0.36]


def card_shell(cx, color, title):
    box = RoundedRectangle(corner_radius=0.25, width=6.2, height=5.9, stroke_color=color, stroke_width=3.5,
                           fill_color=color, fill_opacity=0.06).move_to([cx, -0.1, 0])
    return box, T(title, 46, TEXT, font=TITLE_FONT).move_to([cx, 2.3, 0])


def lamp_icon(cx, cy, big=False):
    return glow(cx, cy, 0.3 if big else 0.2)


class LossBar:
    """The necessary-card bar: normal at (tl, ts) = (0, 0); the front band lost at tl = 1; the others slide forward at ts = 1."""

    def __init__(self, cx, cy, w=5.2, h=0.9, tl=0.0, ts=0.0, shown=0.0):
        self.tcx, self.cy, self.w, self.h = ValueTracker(cx), cy, w, h
        self.tl, self.ts, self.shown = ValueTracker(tl), ValueTracker(ts), ValueTracker(shown)
        self.mob = always_redraw(self._build)

    def _build(self):
        a = self.shown.get_value()
        if a < 0.01:
            return VGroup()
        tl, ts = self.tl.get_value(), self.ts.get_value()
        x0 = self.tcx.get_value() - self.w / 2
        g = VGroup()
        # front band: fades out, leaving a dashed outline of where it was
        wp = NORM_W[0] * self.w
        g.add(Rectangle(width=wp, height=self.h, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE,
                        fill_opacity=0.45 * (1 - tl) * a, stroke_opacity=(1 - tl) * a).move_to([x0 + wp / 2, self.cy, 0]))
        if tl > 0.02 and ts < 0.98:
            ghost = DashedVMobject(Rectangle(width=wp, height=self.h, stroke_color=RED, stroke_width=3,
                                             stroke_opacity=tl * (1 - ts) * a).move_to([x0 + wp / 2, self.cy, 0]), num_dashes=20)
            g.add(ghost)
        pos = x0 + NORM_W[0] * self.w * (1 - ts)
        for k in (1, 2, 3):
            wd = ((1 - ts) * NORM_W[k] + ts * FIN_W[k]) * self.w
            g.add(Rectangle(width=max(wd, 0.002), height=self.h, stroke_color=BAND[k], stroke_width=2, fill_color=BAND[k],
                            fill_opacity=0.45 * a, stroke_opacity=a).move_to([pos + wd / 2, self.cy, 0]))
            pos += wd
        return g


class S06(SpokenScene):
    """Card one: necessary. Remove or block; look for loss or shift (a neutral bar first, the example after)."""

    def construct(self):
        cx = 0.0
        box, title = card_shell(cx, RED, "Necessary?")
        icon = VGroup(lamp_icon(cx - 2.3, 0.9), x_mark(cx - 2.3, 0.9, 0.32, RED, 8))
        t1 = T("remove or block it", 30, TEXT).move_to([cx + 0.55, 0.9, 0])
        arr = arrow([cx, 0.2], [cx, -0.4], GREY_L, 5, 0.22)
        bar = LossBar(cx, -1.1)
        t2 = T("look for loss or shift", 30, TEXT).move_to([cx, -2.35, 0])
        ex = T("for example", 26, GREY_L).move_to([cx + 1.55, -0.3, 0])
        self.add(bar.mob)
        self.at("necessary")
        self.play(FadeIn(box), FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.at("remove or block")
        self.play(FadeIn(icon[0], scale=0.5), run_time=0.4)
        self.play(Create(icon[1]), FadeIn(t1, shift=RIGHT * 0.1), run_time=0.7)
        self.at("look for the loss")
        self.play(GrowArrow(arr), bar.shown.animate.set_value(1), FadeIn(t2), run_time=0.5)
        self.at("the loss")
        self.play(FadeIn(ex), bar.tl.animate.set_value(1), run_time=0.6)
        self.at("shift")
        self.play(bar.ts.animate.set_value(1), run_time=1.0)
        self.finish()


class S07(SpokenScene):
    """Card two: sufficient. Add or add more; look for induced, enlarged or moved."""

    def construct(self):
        bar1 = LossBar(0.0, -1.1, tl=1.0, ts=1.0, shown=1.0)
        c1 = VGroup(*card_shell(0.0, RED, "Necessary?"))
        icon1 = VGroup(lamp_icon(-2.3, 0.9), x_mark(-2.3, 0.9, 0.32, RED, 8))
        t11 = T("remove or block it", 30, TEXT).move_to([0.55, 0.9, 0])
        arr1 = arrow([0.0, 0.2], [0.0, -0.4], GREY_L, 5, 0.22)
        t12 = T("look for loss or shift", 30, TEXT).move_to([0.0, -2.35, 0])
        ex1 = T("for example", 26, GREY_L).move_to([1.55, -0.3, 0])
        left = VGroup(c1, icon1, t11, arr1, t12, ex1)
        self.add(left, bar1.mob)
        cx = 3.3
        box, title = card_shell(cx, YELLOW, "Sufficient?")
        self.at("sufficient")
        self.play(left.animate.shift(LEFT * 3.3), bar1.tcx.animate.set_value(-3.3), FadeIn(box), FadeIn(title, shift=DOWN * 0.1), run_time=0.9)
        icon = VGroup(lamp_icon(cx - 2.3, 0.9, True), Line([cx - 2.62, 0.9, 0], [cx - 1.98, 0.9, 0], stroke_color=TEXT, stroke_width=7),
                      Line([cx - 2.3, 0.58, 0], [cx - 2.3, 1.22, 0], stroke_color=TEXT, stroke_width=7))
        t1 = T("add it, or add more", 30, TEXT).move_to([cx + 0.55, 0.9, 0])
        self.at("add it")
        self.play(FadeIn(icon, scale=0.6), FadeIn(t1, shift=RIGHT * 0.1), run_time=0.8)
        arr = arrow([cx, 0.2], [cx, -0.4], GREY_L, 5, 0.22)
        x0 = cx - 2.6
        strip = VGroup()
        pos = x0
        for wd, c in zip(NORM_W, BAND):
            strip.add(Rectangle(width=wd * 5.2, height=0.9, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.45).move_to(
                [pos + wd * 2.6, -1.1, 0]))
            pos += wd * 5.2
        t2 = T("look for a structure induced,\nenlarged or moved", 28, TEXT, line_spacing=0.9).move_to([cx, -2.4, 0])
        ex = T("for example", 26, GREY_L).move_to([cx + 1.55, -0.3, 0])
        self.at("look for a structure")
        self.play(GrowArrow(arr), FadeIn(strip), FadeIn(t2), run_time=0.8)
        sand_mid = x0 + (NORM_W[0] + NORM_W[1] + NORM_W[2] / 2) * 5.2
        blk = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.7, stroke_color=GREEN, stroke_width=3, fill_color=GREEN,
                               fill_opacity=0.8).move_to([sand_mid - 0.2, -1.1, 0])
        self.at("induced")
        self.play(FadeIn(blk, scale=0.4), FadeIn(ex), run_time=0.5)
        self.at("enlarged")
        self.play(blk.animate.stretch_to_fit_width(1.1).move_to([sand_mid - 0.2, -1.1, 0]), run_time=0.7)
        self.at("moved")
        self.play(blk.animate.shift(RIGHT * 0.25), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def mini_card(cx, cy, color, title, body, icon_kind):
    box = RoundedRectangle(corner_radius=0.2, width=5.9, height=2.0, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.07).move_to([cx, cy, 0])
    ttl = T(title, 36, TEXT, font=TITLE_FONT).move_to([cx, cy + 0.6, 0])
    ic = glow(cx - 2.35, cy - 0.35, 0.16)
    if icon_kind == "x":
        mk = x_mark(cx - 2.35, cy - 0.35, 0.2, RED, 6)
    else:
        mk = VGroup(Line([cx - 2.55, cy - 0.35, 0], [cx - 2.15, cy - 0.35, 0], stroke_color=BG, stroke_width=6),
                    Line([cx - 2.35, cy - 0.55, 0], [cx - 2.35, cy - 0.15, 0], stroke_color=BG, stroke_width=6))
    bd = T(body, 28, TEXT).move_to([cx + 0.5, cy - 0.35, 0])
    return VGroup(box, ttl, ic, mk, bd)


class S08(SpokenScene):
    """Fukuchi-Shimogori and Grove, 2001, and the two kinds of test they ran."""

    def construct(self):
        yr = T("2001", 70, GREY_L, font=MONO, weight=BOLD).move_to([0, 3.0, 0])
        n1 = T("Tomomi Fukuchi-Shimogori", 46, TEXT, font=TITLE_FONT).move_to([0, 1.8, 0])
        a = T("and", 28, GREY_L).move_to([0, 1.15, 0])
        n2 = T("Elizabeth Grove", 46, TEXT, font=TITLE_FONT).move_to([0, 0.5, 0])
        k1 = mini_card(-3.1, -1.3, RED, "Necessary", "remove or block it", "x")
        k2 = mini_card(3.1, -1.3, YELLOW, "Sufficient", "add more of it", "+")
        lamp = glow(-1.9, -3.2, 0.2)
        tl = T("FGF signalling", 34, YELLOW, weight=BOLD).move_to([0.3, -3.2, 0])
        self.at("2001")
        dim = Rectangle(width=12.8, height=2.4, stroke_width=0, fill_color=BG, fill_opacity=0.62).move_to([0, -1.3, 0])
        self.play(FadeIn(yr, scale=0.9), FadeIn(k1, shift=UP * 0.1), FadeIn(k2, shift=UP * 0.1), FadeIn(dim),
                  run_time=0.7)
        self.at("tomomi")
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.7)
        self.at("and elizabeth")
        self.play(FadeIn(a), FadeIn(n2, shift=UP * 0.1), run_time=0.7)
        self.at("both kinds")
        self.play(FadeOut(dim), Indicate(k1, color=RED, scale_factor=1.03), Indicate(k2, color=YELLOW, scale_factor=1.03), run_time=0.8)
        self.at("fgf signaling")
        self.play(FadeIn(lamp, scale=0.5), FadeIn(tl, shift=LEFT * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
BX, BY = -1.6, -0.1


def ring_pts(n=22, a=1.75, b=1.15, cx=BX, cy=BY - 0.1):
    return [(cx + a * np.cos(t), cy + b * np.sin(t)) for t in np.linspace(0, 2 * np.pi, n, endpoint=False)]


class S09(SpokenScene):
    """Electroporation: a needle, DNA, paddles, pulses, and cells at one spot that glow; the spot is the front of the map."""

    def construct(self):
        brain = Ellipse(width=6.4, height=4.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([BX, BY, 0])
        vent = Ellipse(width=3.0, height=1.9, stroke_color="#6FA8DC", stroke_width=2, fill_color="#24496B", fill_opacity=0.8).move_to([BX, BY - 0.1, 0])
        wall = VGroup(*[cell(x, y, 0.11, GREY, 0.6) for x, y in ring_pts()])
        l_b = T("embryonic brain", 28, GREY_L).move_to([-4.6, 3.0, 0])
        l_v = T("ventricle", 28, TEXT).move_to([BX, -3.15, 0])
        l_vl = Line([BX, -2.9, 0], [BX, BY - 0.1 - 0.95, 0], stroke_color=GREY_L, stroke_width=2.5)
        self.at("used")
        self.play(FadeIn(brain, shift=UP * 0.1), FadeIn(vent), FadeIn(wall), FadeIn(l_b), FadeIn(l_v), FadeIn(l_vl), run_time=0.55)
        needle = VGroup(Line([BX, 3.55, 0], [BX, 0.55, 0], stroke_color=TEXT, stroke_width=6),
                        Rectangle(width=0.5, height=0.5, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.6).move_to([BX, 3.5, 0]))
        rng = np.random.RandomState(4)
        dna = VGroup(*[Circle(radius=0.09, stroke_color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.9).move_to(
            [BX + rng.uniform(-1.1, 1.1), BY - 0.1 + rng.uniform(-0.65, 0.15), 0]) for _ in range(9)])
        l_dna = T("DNA", 28, TEAL, weight=BOLD).move_to([BX - 0.8, BY + 0.5, 0])
        self.at("electroporation")
        self.play(Create(needle), run_time=0.7)
        self.play(FadeIn(dna, scale=0.3, lag_ratio=0.1), FadeIn(l_dna), run_time=0.8)
        pl = RoundedRectangle(corner_radius=0.1, width=0.5, height=2.4, stroke_color="#B9C0CF", stroke_width=3, fill_color="#B9C0CF",
                              fill_opacity=0.5).move_to([BX - 3.95, BY, 0])
        pr = pl.copy().move_to([BX + 3.95, BY, 0])
        plus = T("+", 34, TEXT, weight=BOLD).move_to([BX + 3.95, BY + 1.6, 0])
        minus = T("-", 40, TEXT, weight=BOLD).move_to([BX - 3.95, BY + 1.6, 0])
        self.at("brief electric")
        self.play(FadeOut(needle), FadeIn(pl, shift=RIGHT * 0.3), FadeIn(pr, shift=LEFT * 0.3), FadeIn(plus), FadeIn(minus), run_time=0.7)
        flines = VGroup(*[Line([BX - 3.65, BY + d, 0], [BX + 3.65, BY + d, 0], stroke_color=TEXT, stroke_width=5) for d in (-0.85, -0.3, 0.3, 0.85)])
        self.at("pulses drive")
        self.add(flines)
        for rep in range(3):
            flines.set_stroke(opacity=1.0)
            self.wait(0.15)
            if rep == 0:
                self.play(*[d.animate.shift(RIGHT * 0.25) for d in dna], l_dna.animate.shift(RIGHT * 0.25), run_time=0.3)
            flines.set_stroke(opacity=0.15)
            self.wait(0.15)
            if rep == 1:
                self.play(*[d.animate.shift(RIGHT * 0.25) for d in dna], l_dna.animate.shift(RIGHT * 0.25), run_time=0.3)
        flines.set_stroke(opacity=1.0)
        self.wait(0.15)
        self.play(FadeOut(flines), run_time=0.2)
        self.at("injected dna")
        self.play(Indicate(dna, color=TEAL, scale_factor=1.15), run_time=0.7)
        pts_all = ring_pts()
        spot_i = [k for k, (x, y) in enumerate(pts_all) if y > BY + 0.5 and x > BX + 0.3]
        spot = [pts_all[k] for k in spot_i]
        self.at("into progenitors")
        self.play(*[d.animate.move_to([spot[k % len(spot)][0] - 0.1, spot[k % len(spot)][1] - 0.3, 0]) for k, d in enumerate(dna[:4])],
                  FadeOut(dna[4:]), FadeOut(l_dna), FadeOut(pl), FadeOut(pr), FadeOut(plus), FadeOut(minus), run_time=0.7)
        halo = [Circle(radius=0.3, stroke_color=TEAL, stroke_width=3).move_to([x, y, 0]) for x, y in spot]
        mx, my = 4.85, 2.4
        mini = VGroup()
        pos = mx - 1.8
        for wd, c in zip(NORM_W, BAND):
            mini.add(Rectangle(width=wd * 3.6, height=0.8, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.45).move_to(
                [pos + wd * 1.8, my, 0]))
            pos += wd * 3.6
        mini.add(Rectangle(width=3.6, height=0.8, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([mx, my, 0]))
        l_map = T("cortical map", 28, GREY_L).move_to([mx, my - 0.8, 0])
        l_fr = T("front", 26, GREY_L).move_to([mx - 1.8 + 0.4, my + 0.7, 0])
        tgl = glow(mx - 1.8 + 0.12, my, 0.13, color=TEAL)
        lnk = arrow([spot[1][0] + 0.25, spot[1][1] + 0.1], [mx - 1.8 - 0.1, my + 0.0], TEAL, 5, 0.22)
        self.at("chosen spot")
        self.play(*[wall[k].animate.set_color(TEAL).set_fill(TEAL, 0.95) for k in spot_i],
                  *[FadeOut(d) for d in dna[:4]], *[GrowFromCenter(h) for h in halo], run_time=0.7)
        self.play(FadeIn(mini), FadeIn(l_map), FadeIn(l_fr), FadeIn(tgl, scale=0.5), GrowArrow(lnk), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
ROWC = ["#58C4DD", "#F2994A", "#C9A0FF", "#FF7B9C"]


class S10(SpokenScene):
    """The barrel field on the map, matched row for row to the whisker pad."""

    def construct(self):
        cy = 1.6
        st = Stage(vis=("map",), cy=cy, mh=2.4)
        st.install(self)
        fx = st.field_x()
        sp = 0.46
        field = barrel_rows(fx, cy, sp=sp, r=0.13)
        l_f = T("barrel field", 32, GREEN, weight=BOLD).move_to([fx, 3.3, 0])
        pc = (fx, -2.1)
        psp = 0.62
        snout = Ellipse(width=6.6, height=3.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([pc[0], pc[1], 0])
        nose = Circle(radius=0.28, stroke_color="#E9A0A0", stroke_width=2, fill_color="#E9A0A0", fill_opacity=0.9).move_to([pc[0] - 3.35, pc[1], 0])
        l_n = T("nose", 28, TEXT).move_to([pc[0] - 3.35 - 0.95, pc[1], 0])
        pad = barrel_rows(pc[0] + 0.1, pc[1], sp=psp, r=0.17, color=TEXT)
        l_w = T("whisker pad", 30, TEXT).move_to([pc[0] + 4.55, pc[1], 0])
        self.at("their readout")
        self.play(st.v["map"].animate.set_value(1), run_time=0.6)
        self.at("barrel field")
        self.play(FadeIn(field, lag_ratio=0.03), FadeIn(l_f), run_time=0.9)
        self.at("one cluster")
        self.play(FadeIn(snout), FadeIn(nose), FadeIn(l_n), FadeIn(pad, lag_ratio=0.03), FadeIn(l_w), run_time=1.1)
        self.at("each large whisker")
        for j in range(4):
            n = ROWS[j]
            wd = 4 * sp + 0.5
            fr = RoundedRectangle(corner_radius=0.15, width=wd, height=0.44, stroke_color=ROWC[j], stroke_width=4, fill_color=ROWC[j],
                                  fill_opacity=0.18).move_to(field[j].get_center())
            wdp = 4 * psp + 0.64
            pr = RoundedRectangle(corner_radius=0.18, width=wdp, height=0.52, stroke_color=ROWC[j], stroke_width=4, fill_color=ROWC[j],
                                  fill_opacity=0.18).move_to(pad[j].get_center())
            yf, yp = field[j].get_center()[1], pad[j].get_center()[1]
            xa, xb = field[j].get_center()[0] + wd / 2, pad[j].get_center()[0] + wdp / 2
            link = VMobject(stroke_color=ROWC[j], stroke_width=4, stroke_opacity=0.95, fill_opacity=0)
            link.set_points_as_corners([[xa, yf, 0], [xb, yp, 0]])
            wh = Line(pad[j][0].get_center() + LEFT * 0.35, pad[j][0].get_center() + np.array([-1.1, 0.22 * (j - 1.5), 0]),
                      stroke_color=ROWC[j], stroke_width=5)
            self.play(FadeIn(fr), FadeIn(pr), Create(link), Create(wh), run_time=0.45)
        self.finish()


# ---------------------------------------------------------------------------------------------
def full_stage(**kw):
    vis = ("map", "axes", "lamp1", "curve", "glow", "thr", "mk", "dl", "field", "flabel", "fglabel")
    return Stage(vis=kw.pop("vis", vis), **kw)


class S11(SpokenScene):
    """FGF8 as a lamp: brightness, thresholds, and the borders where they cross."""

    def construct(self):
        st = Stage(vis=("map", "axes", "lamp1", "curve", "field", "fglabel"))
        st.v["ghost"].set_value(0)
        st.install(self)
        pr = Probe(st, 0.37)
        self.add(pr.mob)
        wm = tag_working_model()
        thr_l = tag("border threshold", 2.45, py_thr0(st) + 0.3, 26, TEXT, anchor="l")
        bx = px(FA[1])
        bord_l = tag("area border", bx, 3.4, 26, TEXT)
        bord_t = Line([bx, 3.1, 0], [bx, CY + MH / 2 + 0.02, 0], stroke_color=TEXT, stroke_width=3)
        self.at("picture")
        self.play(Indicate(st.m["lamps"], color=YELLOW, scale_factor=1.3), run_time=0.6)
        self.at("as a lamp")
        self.play(st.v["glow"].animate.set_value(1), st.pulse.animate.set_value(1.35), run_time=0.7)
        self.play(st.pulse.animate.set_value(1.0), run_time=0.3)
        self.at("front of a room")
        self.play(st.v["thr"].animate.set_value(1), FadeIn(thr_l), run_time=0.6)
        self.play(st.v["mk"].animate.set_value(1), st.v["dl"].animate.set_value(1), FadeIn(wm), FadeIn(bord_l), FadeIn(bord_t), run_time=0.6)
        self.at("cells judge")
        self.play(pr.v.animate.set_value(1), run_time=0.4)
        self.at("how far forward")
        self.play(pr.tf.animate.set_value(0.22), run_time=0.6)
        self.play(pr.tf.animate.set_value(0.37), run_time=0.6)
        self.at("how bright")
        self.play(pr.tf.animate.set_value(0.10), run_time=0.9)
        self.finish()


def py_thr0(st):
    return st.py(float(st.thr()[0]))


def _s12_state(scene, up=True, with_normal=False):
    st = full_stage(A=UP_A, Ab=1.0, vis=("map", "axes", "lamp1", "curve", "glow", "thr", "field", "flabel", "fglabel"))
    st.install(scene)
    wm = tag_working_model()
    scene.add(wm)
    if with_normal:
        scene.add(normal_label(st))
    return st, wm


def normal_label(st, f=0.11):
    """A label for the dashed 'normal lamp' curve left behind when the lamp is turned up."""
    y = st.py(float(np.exp(-f / LAM)))
    ly = st.py(float(np.exp(-0.28 / LAM))) - 0.42
    t = tag("normal", px(f) + 0.12, ly, 26, "#C9B64E", anchor="l")
    ln = Line([px(f) + 0.3, ly + 0.25, 0], [px(f) + 0.04, y - 0.03, 0], stroke_color="#C9B64E", stroke_width=2.5)
    return VGroup(ln, t)


class S12(SpokenScene):
    """Turn the lamp up. The borders and the barrel field hold still. The question."""

    def construct(self):
        st = full_stage()
        st.install(self)
        wm = tag_working_model()
        self.add(wm)
        self.at("turn the lamp up")
        self.play(st.tA.animate.set_value(UP_A), st.v["mk"].animate.set_value(0), st.v["dl"].animate.set_value(0),
                  FadeIn(normal_label(st)), run_time=1.2)
        self.at("add extra")
        self.play(Indicate(st.m["lamps"], color=YELLOW, scale_factor=1.35), run_time=0.8)
        self.at("which way should")
        q = prompt("Which way should the barrel field move?")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        st, wm = _s12_state(self, with_normal=True)
        q = prompt("Which way should the barrel field move?")
        self.add(q)
        self.finish()


class S14(SpokenScene):
    """Toward the back: cells read themselves as farther forward, so each border falls back."""

    def construct(self):
        st, wm = _s12_state(self)
        nl = normal_label(st)
        self.add(nl)
        st.v["flabel"].set_value(0)
        f0 = 0.45
        pr = Probe(st, f0)
        self.add(pr.mob)
        fx = st.field_x()
        arr = arrow([fx - 0.4, 3.15], [fx + 1.9, 3.15], TEXT, 8, 0.3)
        self.at("toward the back")
        self.play(FadeIn(arr, shift=RIGHT * 0.3), run_time=0.7)
        cyy = CY - MH / 2 + 0.16
        t_cell = tag("this cell", px(f0) + 0.2, CY - MH / 2 - 0.35, 26, TEXT, anchor="l")
        y_read = st.py(float(st.levc(np.array([f0]))[0]))
        t_read = tag("level it reads", 2.3, y_read, 26, TEXT)
        l_read = Line([px(f0) + 0.15, y_read, 0], [2.3 - 1.0, y_read, 0], stroke_color=TEXT, stroke_width=2.5)
        self.at("cells read themselves")
        self.play(FadeOut(arr), FadeOut(nl), pr.v.animate.set_value(1), FadeIn(t_cell), FadeIn(t_read), FadeIn(l_read), run_time=0.8)
        # the same level on the old (normal) curve: a cell that sits farther forward
        fa = f0 - LAM * np.log(UP_A)
        ring = DashedVMobject(Circle(radius=0.14, stroke_color=GREY_L, stroke_width=3), num_dashes=14).move_to([px(fa), cyy, 0])
        gdot = Dot([px(fa), y_read, 0], radius=0.11, color="#C9B64E")
        gl = DashedLine([px(fa), cyy - 0.14, 0], [px(fa), y_read, 0], dash_length=0.09, stroke_color="#C9B64E", stroke_width=3)
        t_ring = tag("reads itself as here", px(fa) - 0.2, CY - MH / 2 - 0.35, 26, GREY_L, anchor="r")
        t_old = tag("normal curve", px(fa) - 0.3, y_read - 0.55, 26, "#C9B64E", anchor="c")
        self.at("farther forward")
        self.play(FadeIn(ring), FadeIn(gdot, scale=0.5), Create(gl), FadeIn(t_ring), FadeIn(t_old), run_time=0.8)
        self.at("so each border")
        gb = ghost_borders(CY, MH, FA)
        self.play(FadeOut(VGroup(ring, gdot, gl, t_ring, t_old, t_cell, t_read, l_read)), pr.v.animate.set_value(0),
                  st.v["mk"].animate.set_value(1), st.v["dl"].animate.set_value(1), FadeIn(gb), run_time=0.5)
        self.at("falls farther back")
        self.play(st.tAb.animate.set_value(UP_A), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S15(SpokenScene):
    """Direct arrows from the lamp to near and far cells; an inner gradient also responds."""

    def construct(self):
        st = Stage(A=UP_A, Ab=UP_A, vis=("map", "axes", "lamp1", "curve", "glow", "thr", "mk", "dl", "field", "fglabel"))
        st.install(self)
        wm = tag_working_model()
        gb = ghost_borders(CY, MH, FA)
        self.add(wm, gb)
        cy = 0.0
        mh = 3.6
        self.at("later work")
        self.play(st.v["axes"].animate.set_value(0), st.v["curve"].animate.set_value(0), st.v["glow"].animate.set_value(0),
                  st.v["thr"].animate.set_value(0), st.v["mk"].animate.set_value(0), st.v["dl"].animate.set_value(0),
                  st.v["field"].animate.set_value(0), FadeOut(wm), FadeOut(gb),
                  st.cy.animate.set_value(cy), st.mh.animate.set_value(mh), run_time=0.9)
        cn = (-2.0, cy + 0.9)
        cf = (3.3, cy - 0.8)
        c_near = cell(cn[0], cn[1], 0.22)
        c_far = cell(cf[0], cf[1], 0.22)
        l_n = T("near", 28, TEXT).move_to([cn[0] + 0.7, cn[1] + 0.05, 0])
        l_f = T("far", 28, TEXT).move_to([cf[0] + 0.6, cf[1], 0])
        a_n = arrow([LX + 0.55, cy + 0.15], [cn[0] - 0.3, cn[1] - 0.08], YELLOW, 7, 0.28)
        a_f = arrow([LX + 0.55, cy - 0.1], [cf[0] - 0.3, cf[1] + 0.03], YELLOW, 7, 0.28)
        self.at("fgf8")
        self.play(st.pulse.animate.set_value(1.4), run_time=0.35)
        self.play(st.pulse.animate.set_value(1.0), run_time=0.35)
        self.at("act directly")
        self.play(FadeIn(c_near, scale=0.4), FadeIn(l_n), FadeIn(a_n), run_time=0.8)
        self.at("at a distance")
        self.play(FadeIn(c_far, scale=0.4), FadeIn(l_f), FadeIn(a_f), run_time=1.0)
        grp = VGroup(c_near, c_far, l_n, l_f, a_n, a_f)
        bar_y = -2.75
        bar = VGroup(*[Rectangle(width=W / 40, height=0.8, stroke_width=0, fill_color=INNER,
                                 fill_opacity=0.12 + 0.6 * (k / 39)).move_to([px((k + 0.5) / 40), bar_y, 0]) for k in range(40)])
        bar_o = Rectangle(width=W, height=0.8, stroke_color=INNER, stroke_width=3, fill_opacity=0).move_to([X0 + W / 2, bar_y, 0])
        l_b = T("gradients the lamp helps set", 30, INNER).move_to([0.1, bar_y - 0.8, 0])
        self.at("cells also respond")
        self.play(st.cy.animate.set_value(cy + 0.8), grp.animate.shift(UP * 0.8), run_time=0.7)
        i_n = arrow([cn[0], bar_y + 0.45], [cn[0], cn[1] + 0.8 - 0.3], INNER, 6, 0.24)
        i_f = arrow([cf[0], bar_y + 0.45], [cf[0], cf[1] + 0.8 - 0.3], INNER, 6, 0.24)
        self.play(FadeIn(bar), Create(bar_o), FadeIn(l_b, shift=UP * 0.1), run_time=0.7)
        self.at("through the gradients")
        self.play(FadeIn(i_n), FadeIn(i_f), run_time=0.8)
        self.at("it helps set")
        self.play(Indicate(bar_o, color=INNER, scale_factor=1.02), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def cup_mob(x, y, c=RED, s=0.7):
    u = Arc(radius=0.26 * s, start_angle=PI, angle=PI, stroke_color=c, stroke_width=7).move_to([x, y, 0])
    stem = Line([x, y - 0.26 * s, 0], [x, y - 0.26 * s - 0.2 * s, 0], stroke_color=c, stroke_width=7)
    return VGroup(u, stem)


CUP_XS = [-3.95 + 0.64 * k for k in range(7)]
CUP_Y = 0.52


def caught_final(with_pale=True):
    """The end of s16: receptor fragments (red cups) holding the FGF8 they caught."""
    g = VGroup()
    for k, x in enumerate(CUP_XS):
        if k >= 4 and not with_pale:
            continue
        col = YELLOW if k < 4 else PALEY
        g.add(cup_mob(x, CUP_Y), Circle(radius=0.1, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.45).move_to([x, CUP_Y + 0.02, 0]))
    return g


def s16_tags():
    return VGroup(tag("receptor fragment", 0.5, CUP_Y + 0.25, 26, RED, anchor="l"), tag("FGF8 caught", 0.5, CUP_Y - 0.3, 26, YELLOW, anchor="l"))


class S16(SpokenScene):
    """Block the lamp: receptor fragments mop up FGF8; the curve sinks; where does the field go?"""

    def construct(self):
        st = full_stage(vis=("map", "axes", "lamp1", "curve", "glow", "thr", "mk", "dl", "field", "flabel", "fglabel"))
        st.install(self)
        wm = tag_working_model()
        self.add(wm)
        xm = x_mark(LX, CY, 0.45, RED, 9)
        l_blk = tag("blocked", LX + 0.2, CY + 0.95, 28, RED, weight=BOLD)
        self.at("block the lamp")
        self.play(Create(xm), FadeIn(l_blk, shift=DOWN * 0.1), st.v["dl"].animate.set_value(0), st.v["mk"].animate.set_value(0),
                  st.v["flabel"].animate.set_value(0), run_time=0.7)
        dots = VGroup(*[Circle(radius=0.1, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.95).move_to(
            [LX + 0.6, CY - 0.55, 0]) for k in range(4)])
        pale = VGroup(*[Circle(radius=0.1, stroke_color=PALEY, stroke_width=2.5, fill_color=PALEY, fill_opacity=0.9).move_to(
            [LX + 0.6, CY - 0.55, 0]) for k in range(3)])
        cups = VGroup(*[cup_mob(CUP_XS[k], CUP_Y + 0.35) for k in range(4)])
        cups2 = VGroup(*[cup_mob(CUP_XS[4 + k], CUP_Y + 0.35) for k in range(3)])
        tg = s16_tags()
        self.at("a soluble")
        self.add(dots)
        self.play(*[dots[k].animate.move_to([CUP_XS[k], CUP_Y + 0.02, 0]) for k in range(4)], run_time=0.8)
        self.at("receptor fragment")
        self.play(FadeIn(cups, shift=UP * 0.0), FadeIn(tg[0], shift=LEFT * 0.1), run_time=0.8)
        self.at("that binds")
        self.play(*[cups[k].animate.shift(DOWN * 0.35) for k in range(4)], run_time=0.9)
        self.at("fgf8")
        self.play(*[dots[k].animate.set_opacity(0.45) for k in range(4)], FadeIn(tg[1], shift=LEFT * 0.1),
                  st.tA.animate.set_value(0.7), run_time=1.3)
        self.at("probably related")
        self.add(pale)
        self.play(*[pale[k].animate.move_to([CUP_XS[4 + k], CUP_Y + 0.02, 0]) for k in range(3)], FadeIn(cups2), run_time=0.8)
        self.play(*[cups2[k].animate.shift(DOWN * 0.35) for k in range(3)], *[pale[k].animate.set_opacity(0.45) for k in range(3)],
                  run_time=0.9)
        self.at("where does the field go")
        q = prompt("Where does the field go?")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


def _s16_state(scene, with_label=False, with_mol=False):
    st = full_stage(A=0.7, Ab=1.0, vis=("map", "axes", "lamp1", "curve", "glow", "thr", "field", "fglabel") + (("flabel",) if with_label else ()))
    st.install(scene)
    wm = tag_working_model()
    xm = x_mark(LX, CY, 0.45, RED, 9)
    l_blk = tag("blocked", LX + 0.2, CY + 0.95, 28, RED, weight=BOLD)
    scene.add(wm, xm, l_blk)
    if with_mol:
        scene.add(caught_final(), s16_tags())
    return st, wm, xm, l_blk


class S17Pause(NarratedScene):
    def construct(self):
        st, wm, xm, lb = _s16_state(self, with_mol=True)
        q = prompt("Where does the field go?")
        self.add(q)
        self.finish()


class S18(SpokenScene):
    """Toward the front. More FGF8 moves it back, less moves it forward: opposite shifts."""

    def construct(self):
        st, wm, xm, lb = _s16_state(self, with_mol=False)
        mol = VGroup(caught_final(), s16_tags())
        self.add(mol)
        q0 = prompt("Where does the field go?")
        self.add(q0)
        fx0 = st.field_x()
        self.at("toward the front")
        self.play(FadeOut(mol), FadeOut(q0), FadeOut(lb), st.v["mk"].animate.set_value(1), run_time=0.4)
        self.play(st.tAb.animate.set_value(0.7), run_time=1.3)
        up = Stage(A=UP_A)
        gx = up.field_x()
        gy = 1.05
        bn = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.7, height=0.6, stroke_color=GREY_L, stroke_width=3), num_dashes=24).move_to([fx0, gy, 0])
        bg = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=2.3, height=0.6, stroke_color=YELLOW, stroke_width=3), num_dashes=24).move_to([gx, gy, 0])
        tn = T("normal", 26, GREY_L).move_to([fx0, gy, 0])
        tg = T("extra FGF8", 26, YELLOW).move_to([gx, gy, 0])
        gl1 = DashedLine([fx0, gy + 0.3, 0], [fx0, CY - MH / 2 - 0.0, 0], dash_length=0.08, stroke_color=GREY_L, stroke_width=2.5)
        gl2 = DashedLine([gx, gy + 0.3, 0], [gx, CY - MH / 2 - 0.0, 0], dash_length=0.08, stroke_color=YELLOW, stroke_width=2.5)
        a1 = arrow([0.5, 3.38], [1.3, 3.38], TEXT, 6, 0.22)
        t1 = T("more FGF8:\nmoved back", 30, TEXT, line_spacing=0.85).move_to([3.1, 3.38, 0])
        a2 = arrow([-0.9, 3.38], [-1.7, 3.38], TEXT, 6, 0.22)
        t2 = T("less FGF signalling:\nmoved forward", 30, TEXT, line_spacing=0.85).move_to([-3.9, 3.38, 0])
        self.at("more fgf8")
        self.play(FadeIn(bn), FadeIn(bg), FadeIn(tn), FadeIn(tg), FadeIn(gl1), FadeIn(gl2), run_time=0.7)
        self.at("moves it back")
        self.play(FadeIn(a1), FadeIn(t1, shift=RIGHT * 0.1), run_time=0.7)
        self.at("less fgf")
        self.play(FadeIn(a2), FadeIn(t2, shift=LEFT * 0.1), run_time=0.8)
        self.at("opposite shifts")
        self.play(Indicate(t1, color=TEXT, scale_factor=1.05), Indicate(t2, color=TEXT, scale_factor=1.05), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def _s19_state(scene, lamp2=1.0, Bk=0.0, Bb=0.0):
    st = full_stage(Bk=Bk, Bb=Bb)
    st.v["lamp2"].set_value(lamp2)
    st.install(scene)
    wm = tag_working_model()
    scene.add(wm)
    return st, wm


def lamp2_label():
    lbl = tag("extra FGF8 source", RX - 0.7, 3.3, 28, YELLOW, weight=BOLD)
    ln = Line([RX, 3.05, 0], [RX, CY + 0.6, 0], stroke_color=YELLOW, stroke_width=3)
    return VGroup(lbl, ln)


def far_arrow():
    a = DoubleArrow([LX + 0.7, 0.95, 0], [RX - 0.7, 0.95, 0], buff=0, color=GREY_L, stroke_width=4, tip_length=0.2)
    t = tag("far from the first", 2.9, 1.3, 26, GREY_L)
    return VGroup(a, t)


class S19(SpokenScene):
    """A second lamp at the back edge. What should happen?"""

    def construct(self):
        st, wm = _s19_state(self, lamp2=0.0)
        l2 = lamp2_label()
        self.at("a new lamp")
        self.play(st.v["lamp2"].animate.set_value(1), FadeIn(l2, shift=DOWN * 0.1), run_time=0.8)
        self.at("at the back")
        self.play(Indicate(st.m["lamps"], color=YELLOW, scale_factor=1.25), run_time=0.5)
        fa = far_arrow()
        self.at("far from the first")
        self.play(FadeIn(fa), run_time=0.6)
        q = prompt("What should happen?")
        self.at("what should happen")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


class S20Pause(NarratedScene):
    def construct(self):
        st, wm = _s19_state(self)
        self.add(lamp2_label(), far_arrow())
        q = prompt("What should happen?")
        self.add(q)
        self.finish()


class S21(SpokenScene):
    """Near the new lamp the level climbs again; a new crossing near the back; part of the pattern repeats.
    The first three borders and the barrel field stay where they were."""

    def construct(self):
        st, wm = _s19_state(self)
        self.add(lamp2_label())
        f0 = 0.97
        pr = Probe(st, f0)
        self.add(pr.mob)
        self.at("near the new lamp")
        self.play(st.v["mk"].animate.set_value(0), st.v["dl"].animate.set_value(0), st.v["flabel"].animate.set_value(0), st.tB.animate.set_value(BACK), run_time=0.8)
        self.at("cells read a high level")
        self.play(pr.v.animate.set_value(1), run_time=0.8)
        self.at("as if they sat")
        gy = float(st.levc(np.array([f0]))[0])
        fa = float(LAM * np.log(1.0 / gy))
        cyy = CY - MH / 2 + 0.16
        arr = arrow([px(f0) - 0.25, cyy], [px(fa) + 0.25, cyy], TEXT, 5, 0.22)
        ring = DashedVMobject(Circle(radius=0.14, stroke_color=GREY_L, stroke_width=3), num_dashes=14).move_to([px(fa), cyy, 0])
        t_cell = tag("this cell", px(f0) - 0.2, CY - MH / 2 - 0.4, 26, TEXT, anchor="r")
        t_ring = tag("reads itself as here", px(fa), CY - MH / 2 - 0.4, 26, GREY_L)
        self.play(GrowArrow(arr), FadeIn(ring), FadeIn(t_cell), FadeIn(t_ring), run_time=0.9)
        self.at("part of the pattern")
        self.play(FadeOut(arr), FadeOut(ring), FadeOut(t_cell), FadeOut(t_ring), pr.v.animate.set_value(0), st.tBb.animate.set_value(BACK), run_time=0.4)
        self.play(st.v["mk"].animate.set_value(1), st.v["dl"].animate.set_value(1), st.v["flabel"].animate.set_value(1), run_time=0.6)
        self.at("repeats there")
        gs = [(a, b) for a, b, i in st.segs() if i == 1]
        a0, b0 = gs[-1]
        box = DashedVMobject(Rectangle(width=(b0 - a0) * W + 0.15, height=MH + 0.2, stroke_color=TEXT, stroke_width=4), num_dashes=24).move_to(
            [px((a0 + b0) / 2), CY, 0])
        self.play(FadeIn(box), run_time=0.6)
        self.finish()


class S22(SpokenScene):
    """A small second patch of barrels forms near the back."""

    def construct(self):
        st, wm = _s19_state(self, Bk=BACK, Bb=BACK)
        st.v["mk"].set_value(1), st.v["dl"].set_value(1)
        self.at("partial second barrel field")
        self.play(st.v["p2"].animate.set_value(1), st.v["plabel"].animate.set_value(1), run_time=1.0)
        self.at("behind the normal one")
        self.play(Indicate(st.m["field"], color=GREEN, scale_factor=1.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def equation(size=38, x=0.0, y=3.35):
    """C = C0 e^(-x/lambda), built from pieces so the 0 and the exponent sit where they should."""
    p = [M("C = C", size, TEXT), M("0", int(size * 0.62), TEXT), M(" e", size, TEXT), M("-x/λ", int(size * 0.62), TEXT)]
    p[1].next_to(p[0], RIGHT, buff=0.03).shift(DOWN * 0.1)
    p[2].next_to(p[1], RIGHT, buff=0.03).shift(UP * 0.1)
    p[3].next_to(p[2], RIGHT, buff=0.03).shift(UP * 0.17)
    g = VGroup(*p)
    return g.move_to([x, y, 0])


def _s23_state(scene, vis_extra=(), **kw):
    st = full_stage(vis=("map", "axes", "lamp1", "curve", "glow", "field", "fglabel") + tuple(vis_extra), **kw)
    st.install(scene)
    illus = tag_model("illustrative model", TEAL)
    return st, illus


class S23(SpokenScene):
    """The curve as an exponential; the equation; the model is illustrative (one tag, replacing the working-model tag)."""

    def construct(self):
        st, illus = _s23_state(self)
        wm = tag_working_model()
        self.add(wm)
        eq = equation()
        self.at("how far does a border move")
        self.play(st.rev.animate.set_value(0.0), run_time=0.01)
        self.play(st.rev.animate.set_value(1.0), run_time=1.5, rate_func=linear)
        self.at("a simple model")
        self.play(Write(eq), run_time=1.0)
        self.at("its numbers are illustrative")
        self.play(FadeOut(wm), FadeIn(illus), Indicate(eq, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.finish()


class S24(SpokenScene):
    """Equal steps back each leave the same fraction; the decay length leaves a little over a third."""

    def construct(self):
        st, illus = _s23_state(self)
        eq = equation()
        self.add(eq, illus)
        self.add(tag("Longer decay length than the lesson’s worked example",
                      0.1, 1.02, 22, TEAL))
        yb = st.pb
        fs = [0.0, LAM, 2 * LAM, 3 * LAM]
        ys = [st.py(float(st.levc(np.array([f]))[0])) for f in fs]
        ticks = VGroup(*[Line([px(f), yb - 0.12, 0], [px(f), yb + 0.12, 0], stroke_color=TEXT, stroke_width=4) for f in fs])
        dots = VGroup(*[Dot([px(f), y, 0], radius=0.12, color=TEXT) for f, y in zip(fs, ys)])
        stairs = VGroup()
        for k in range(3):
            stairs.add(DashedLine([px(fs[k]), ys[k], 0], [px(fs[k + 1]), ys[k], 0], dash_length=0.1, stroke_color=TEXT, stroke_width=3),
                       DashedLine([px(fs[k + 1]), ys[k], 0], [px(fs[k + 1]), ys[k + 1], 0], dash_length=0.1, stroke_color=TEXT, stroke_width=3))
        steps = VGroup(*[arrow([px(fs[k]) + 0.03, yb + 0.4], [px(fs[k + 1]) - 0.03, yb + 0.4], TEXT, 5, 0.18) for k in range(3)])
        l_lam = M("λ", 46, BLUE, weight=BOLD).move_to([(px(fs[0]) + px(fs[1])) / 2, yb + 0.95, 0])
        l100 = tag("100%", px(0.0) + 0.75, ys[0] + 0.4, 28, TEXT)
        l37 = tag("about 37%", px(LAM) + 1.55, ys[1] + 0.45, 28, TEXT)
        l37_ln = Line([px(LAM) + 0.15, ys[1] + 0.12, 0], [px(LAM) + 0.55, ys[1] + 0.38, 0], stroke_color=TEXT, stroke_width=2.5)
        self.at("level fall")
        self.play(FadeIn(dots[0], scale=0.5), FadeIn(l100, shift=UP * 0.1), run_time=0.5)
        self.at("same fraction")
        self.play(LaggedStart(*[AnimationGroup(Create(stairs[2 * k]), Create(stairs[2 * k + 1]), FadeIn(dots[k + 1], scale=0.5))
                                for k in range(3)], lag_ratio=0.45), run_time=1.2)
        self.at("each step back")
        self.play(LaggedStart(*[GrowArrow(a) for a in steps], lag_ratio=0.25), FadeIn(ticks), run_time=1.0)
        self.at("decay length")
        self.play(Indicate(steps[0], color=BLUE, scale_factor=1.15), FadeIn(l_lam, shift=UP * 0.1), FadeIn(l37), FadeIn(l37_ln),
                  Indicate(dots[1], color=YELLOW, scale_factor=1.6), run_time=0.8)
        self.at("a little over")
        self.play(Indicate(l37, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.finish()


class S25(SpokenScene):
    """Double the lamp: every border moves back by the same distance, lambda ln 2, about 0.7 lambda."""

    def construct(self):
        st, illus = _s23_state(self)
        eq = equation()
        self.add(eq, illus)
        self.add(tag("Longer decay length than the lesson’s worked example",
                      0.1, 1.02, 22, TEAL))
        self.at("double the lamp")
        self.play(st.tA.animate.set_value(UP_A), run_time=1.2)
        bx = 0.9
        lam_bar = VGroup(Line([bx, -0.3, 0], [bx + LAM * W, -0.3, 0], stroke_color=BLUE, stroke_width=7),
                         M("λ", 38, BLUE, weight=BOLD).move_to([bx + LAM * W + 0.45, -0.3, 0]))
        self.at("decay length")
        self.play(FadeIn(lam_bar, shift=RIGHT * 0.1), run_time=0.6)
        sub = T("λ and thresholds fixed", 28, GREY_L).move_to([2.9, 0.2, 0])
        self.at("thresholds fixed")
        self.play(st.v["thr"].animate.set_value(1), FadeIn(sub), run_time=0.6)
        self.at("every border")
        self.play(st.v["mk"].animate.set_value(1), run_time=0.5)
        gb = ghost_borders(CY, MH, FA)
        self.add(gb)
        self.at("moves back")
        self.play(st.tAb.animate.set_value(UP_A), run_time=0.9)
        T_ = TH_EXP
        steps = VGroup()
        for i in range(3):
            f1 = LAM * np.log(UP_A / T_[i])
            y = st.py(T_[i])
            steps.add(VGroup(Line([px(FA[i]) + 0.1, y, 0], [px(f1) - 0.1, y, 0], stroke_color=BG, stroke_width=12),
                             arrow([px(FA[i]) + 0.1, y], [px(f1) - 0.1, y], YELLOW, 6, 0.2)))
        self.at("same distance")
        eq2 = M("shift = λ ln 2 ≈ 0.7 λ", 34, TEXT).move_to([2.2, -1.4, 0])
        self.play(LaggedStart(*[FadeIn(a) for a in steps], lag_ratio=0.2), FadeIn(eq2, shift=UP * 0.1), run_time=0.9)
        lamd = LAM * np.log(2)
        sb = VGroup(Line([bx, -0.85, 0], [bx + lamd * W, -0.85, 0], stroke_color=YELLOW, stroke_width=7),
                    T("shift", 28, YELLOW, weight=BOLD).move_to([bx + lamd * W + 0.6, -0.85, 0]))
        self.at("that distance")
        self.play(Create(sb[0]), FadeIn(sb[1]), run_time=0.8)
        self.at("seven tenths")
        self.play(Indicate(eq2, color=YELLOW, scale_factor=1.04), run_time=0.7)
        self.at("decay length", nth=1)
        self.play(Indicate(lam_bar[0], color=BLUE, scale_factor=1.05), Indicate(sb[0], color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.finish()


class S26(SpokenScene):
    """Halve the lamp: every border moves forward by the same amount; a border past the edge is lost."""

    def construct(self):
        st, illus = _s23_state(self, vis_extra=("thr", "mk"))
        st.lamp_dx.set_value(-0.5)
        eq = equation()
        self.add(eq, illus)
        gb = ghost_borders(CY, MH, FA)
        self.add(gb)
        self.at("the lamp and")
        self.play(st.tA.animate.set_value(DOWN_A), st.v["mk"].animate.set_value(0), run_time=0.9)
        self.at("each border moves forward")
        self.play(st.v["mk"].animate.set_value(1), run_time=0.3)
        self.play(st.tAb.animate.set_value(DOWN_A), run_time=1.2)
        T_ = TH_EXP
        steps = VGroup()
        for i in range(1, 3):
            f1 = LAM * np.log(DOWN_A / T_[i])
            y = st.py(T_[i])
            steps.add(VGroup(Line([px(FA[i]) - 0.1, y, 0], [px(f1) + 0.1, y, 0], stroke_color=BG, stroke_width=12),
                             arrow([px(FA[i]) - 0.1, y], [px(f1) + 0.1, y], YELLOW, 6, 0.2)))
        self.at("same amount")
        self.play(LaggedStart(*[FadeIn(a) for a in steps], lag_ratio=0.2), run_time=0.8)
        # the front band (purple) is pushed past the edge: dashed outline with a red cross, and a red dot on the axis
        wp = FA[0] * W
        ly = CY - MH / 2 - 0.5
        lost_box = VGroup(Rectangle(width=wp, height=0.5, stroke_width=0, fill_color=PURPLE, fill_opacity=0.3).move_to([X0 + wp / 2, ly, 0]),
                          DashedVMobject(Rectangle(width=wp, height=0.5, stroke_color=PURPLE, stroke_width=4).move_to([X0 + wp / 2, ly, 0]), num_dashes=24))
        lost_x = x_mark(X0 + wp / 2, ly, 0.2, RED, 6)
        lost_arr = arrow([X0 + 0.35, CY - MH / 2 - 0.02], [X0 + 0.35, ly + 0.28], PURPLE, 4, 0.16)
        lost_b = tag("front band", X0 + wp + 0.15, ly, 26, PURPLE, anchor="l")
        lost_dot = Circle(radius=0.12, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.9).move_to([X0, st.py(T_[0]), 0])
        lost_t = tag("lost", X0 + 0.3, st.py(T_[0]) + 0.35, 30, RED, weight=BOLD, anchor="l")
        self.at("past the edges")
        self.play(Create(lost_box), FadeIn(lost_arr), Create(lost_x), FadeIn(lost_b), FadeIn(lost_dot, scale=0.5), run_time=0.7)
        self.at("lost")
        self.play(FadeIn(lost_t, scale=0.7), Indicate(lost_dot, color=RED, scale_factor=1.6), run_time=0.6)
        self.finish()


def step_arrow(x0, x1, y):
    """A shift arrow in the shift yellow, with a dark halo so it reads over the glow."""
    return VGroup(Line([x0, y, 0], [x1, y, 0], stroke_color=BG, stroke_width=12), arrow([x0, y], [x1, y], YELLOW, 6, 0.2))


def ramp_arrows(st, up):
    g = VGroup()
    for i in range(3):
        f1 = 1 - (1 - FA[i]) / up
        y = st.py(TH_RAMP[i])
        g.add(step_arrow(px(FA[i]) + 0.1, px(f1) - 0.1, y))
    return g


class S27(SpokenScene):
    """The equal steps belong to the exponential; a straight ramp gives unequal steps (held on screen at the end)."""

    def construct(self):
        st, illus = _s23_state(self, vis_extra=("thr", "mk"), A=UP_A)
        eq = equation()
        self.add(eq, illus)
        T_ = TH_EXP
        steps = VGroup()
        for i in range(3):
            f1 = LAM * np.log(UP_A / T_[i])
            steps.add(step_arrow(px(FA[i]) + 0.1, px(f1) - 0.1, st.py(T_[i])))
        st.tAb.set_value(UP_A)
        gb = ghost_borders(CY, MH, FA)
        self.add(steps, gb)
        shape_l = T("shape matters", 44, TEXT, font=TITLE_FONT).move_to([0.0, 3.35, 0])
        # comparison panel (to one scale): the exponential's equal steps beside the ramp's unequal steps
        k = 0.7 / (LAM * np.log(UP_A))            # units per fraction of the sheet
        l_e = T("exponential: equal steps", 26, TEXT).move_to([2.7, 0.4, 0])
        l_r = T("ramp: unequal steps", 26, TEXT).move_to([2.5, -0.5, 0])
        pe = VGroup(*[step_arrow(0.5 + 1.25 * j, 0.5 + 1.25 * j + 0.7, 0.0) for j in range(3)])
        pr_ = VGroup()
        xx = 0.5
        for i in range(3):
            ln = (1 - FA[i]) * (1 - 1 / UP_A) * k
            pr_.add(step_arrow(xx, xx + ln, -0.9))
            xx += ln + 0.3
        self.at("equal steps")
        self.play(Indicate(steps, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("exponential shape")
        self.play(Indicate(st.m["curve"], color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("straight line ramp")
        self.play(ReplacementTransform(steps, pe), FadeIn(l_e), FadeOut(eq), FadeOut(gb), st.tA.animate.set_value(1.0),
                  st.tAb.animate.set_value(1.0), run_time=0.6)
        self.play(st.tmix.animate.set_value(1.0), run_time=0.6)
        gb2 = ghost_borders(CY, MH, FA)
        self.add(gb2)
        self.at("unequal steps")
        self.play(st.tA.animate.set_value(UP_A), FadeIn(shape_l, shift=UP * 0.1), run_time=0.4)
        self.play(st.tAb.animate.set_value(UP_A), run_time=0.8)
        steps2 = ramp_arrows(st, UP_A)
        self.play(LaggedStart(*[FadeIn(a) for a in steps2], lag_ratio=0.2), FadeIn(l_r), FadeIn(pr_), run_time=0.8)
        self.finish()
        self.wait(3.0)


class S28(SpokenScene):
    """What survives both shapes: the direction, and a graded response to dose."""

    def construct(self):
        rows = [(1.0, DOWN_A, "half\nlamp"), (-0.5, 1.0, "normal"), (-2.0, UP_A, "double\nlamp")]
        strips = [Stage(A=a, vis=(), cy=cy, mh=1.0) for cy, a, n in rows]
        labs = []
        for cy, a, n in rows:
            l = T(n, 26, GREY_L)
            l.move_to([-5.35 - l.width / 2, cy, 0])
            labs.append(l)
        for st_ in strips:
            st_.install(self)
        fb = VGroup(T("front", 26, GREY_L).move_to([X0 + 0.5, 1.0 + 0.5 + 0.32, 0]), T("back", 26, GREY_L).move_to([X0 + W - 0.45, 1.0 + 0.5 + 0.32, 0]))
        ghost = VGroup(Rectangle(width=0.55, height=1.0, stroke_width=0, fill_color=PURPLE, fill_opacity=0.25),
                       DashedVMobject(Rectangle(width=0.55, height=1.0, stroke_color=PURPLE, stroke_width=4), num_dashes=16)).move_to([X0 - 0.3, 1.0, 0])
        lost = T("front band\nlost", 26, RED, line_spacing=0.9)
        lost.move_to([X0 - 0.15 - lost.width / 2, 2.18, 0])
        lost_l = Line([X0 - 0.3, 1.83, 0], [X0 - 0.3, 1.55, 0], stroke_color=RED, stroke_width=3)
        self.add(fb)
        self.at("survives both shapes")
        for st_, l in zip(strips, labs):
            self.play(st_.v["map"].animate.set_value(1), FadeIn(l), run_time=0.45)
        self.play(FadeIn(ghost), FadeIn(lost), FadeIn(lost_l), run_time=0.3)
        h1 = T("direction", 42, TEXT, font=TITLE_FONT).move_to([-2.4, 3.1, 0])
        h2 = T("graded dose", 42, TEXT, font=TITLE_FONT).move_to([3.0, 3.1, 0])
        h2.shift(UP * (h1[0].get_bottom()[1] - h2[1].get_bottom()[1]))
        links = VGroup()
        for i in range(3):
            pts = [(LAM * np.log(a / TH_EXP[i]), cy) for cy, a, n in rows]
            for k in range(2):
                (f0, y0), (f1, y1) = pts[k], pts[k + 1]
                if f0 <= 0.0:
                    continue
                links.add(Arrow([px(f0), y0 - 0.5, 0], [px(f1), y1 + 0.5, 0], buff=0, color=TEXT, stroke_width=3, tip_length=0.16,
                                max_stroke_width_to_length_ratio=100, max_tip_length_to_length_ratio=0.3))
        dose = arrow([5.75, 1.0], [5.75, -2.0], YELLOW, 6, 0.24)
        dose_l = T("more lamp", 26, YELLOW).rotate(-PI / 2).move_to([6.2, -0.5, 0])
        self.at("the direction")
        self.play(FadeIn(h1, shift=DOWN * 0.1), Create(links), run_time=1.2)
        self.at("graded response")
        self.play(FadeIn(h2, shift=DOWN * 0.1), FadeIn(dose), FadeIn(dose_l), run_time=0.8)
        self.at("to dose")
        self.play(*[Indicate(l, color=TEXT, scale_factor=1.1) for l in labs], run_time=0.9)
        self.finish()


class S29(SpokenScene):
    """The takeaway: one line, and the working model with the lamp dimming and brightening so the borders slide."""

    def construct(self):
        st = full_stage(cy=CY, mh=MH, vis=("map", "axes", "lamp1", "curve", "glow", "thr", "mk", "dl", "fglabel"))
        for k in ("map", "axes", "lamp1", "curve", "glow", "thr", "fglabel", "mk", "dl"):
            st.v[k].set_value(0)
        wm = tag_working_model()
        rule = T("Graded signals help place areas.", 44, TEXT, font=TITLE_FONT)
        fit(rule, max_w=12.4)
        rule.move_to([0, 3.35, 0])
        st.install(self)
        self.play(*[st.v[k].animate.set_value(1) for k in ("map", "axes", "lamp1", "curve", "glow", "thr", "fglabel", "mk", "dl")], run_time=0.8)
        self.at("graded signals")
        self.play(Write(rule), run_time=1.1)
        self.at("working model")
        self.play(FadeIn(wm), run_time=0.5)
        self.at("change the dose")
        self.play(st.tA.animate.set_value(UP_A), st.tAb.animate.set_value(UP_A), run_time=0.8)
        self.play(st.tA.animate.set_value(DOWN_A), st.tAb.animate.set_value(DOWN_A), run_time=0.9)
        self.at("border slide")
        self.play(st.tA.animate.set_value(1.0), st.tAb.animate.set_value(1.0), run_time=0.8)
        self.finish()


class S30End(EndCard):
    LINE = "Graded signals help place areas;\nin our working model, dose moves borders."
