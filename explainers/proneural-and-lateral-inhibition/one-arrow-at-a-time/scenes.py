"""Proneural genes and lateral inhibition, chapter 3: The Loop, One Arrow at a Time

COLOR MAP (one colour per concept, shared with every chapter; taken from scenes.old.py)
  GREEN  = proneural activity (bar, gene, factor) and the neural fate (cell rim, "neural" tags)
  YELLOW = Delta (the ball on a stick, the Delta gene)
  BLUE   = Notch (the crescent, the inner part of Notch, CSL, the "not you" signal)
  RED    = E(spl) repressor (bar, gene) and every inhibition arrow
  GREY   = cells, nuclei, DNA, bar tracks, labels, cells that are held back
  GOLD   = the question mark, the "predict" prompt and notes that pose a question
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PRO, DEL, NOT, REP = GREEN, YELLOW, BLUE, RED


# ------------------------------------------------------------------------------------------
# small helpers
# ------------------------------------------------------------------------------------------
def arr(a, b, color=GREEN, w=5, tip=0.22):
    return Arrow(np.array(a, float), np.array(b, float), buff=0, color=color, stroke_width=w, tip_length=tip)


def inhib(a, b, color=RED, w=5, half=0.24):
    """A line that ends in a bar: the sign for 'inhibits'."""
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * half, b - perp * half, color=color, stroke_width=(w + 1) if w > 0.5 else 0.001))


def arc_inh(p0, p1, bend=-1.6, color=RED, w=6):
    arc = ArcBetweenPoints(np.array(p0, float), np.array(p1, float), angle=bend, color=color, stroke_width=w)
    end = arc.get_end()
    d = end - arc.point_from_proportion(0.96)
    d = d / np.linalg.norm(d)
    perp = np.array([-d[1], d[0], 0])
    bar = Line(end + perp * 0.42, end - perp * 0.42, color=color, stroke_width=w + 3)
    return VGroup(arc, bar)


def minus(c, color=RED, w=12):
    c = np.array(c, float)
    return Line(c + LEFT * 0.36, c + RIGHT * 0.36, color=color, stroke_width=w)


def ping(scene, c, r=0.28, color=TEXT, run_time=0.7):
    ring = Circle(radius=r, stroke_color=color, stroke_width=4, fill_opacity=0).move_to(c)
    scene.add(ring)
    scene.play(ring.animate.scale(2.4).set_stroke(opacity=0), run_time=run_time)
    scene.remove(ring)


def leader(p0, p1, color=GREY, w=2.5):
    return Line(np.array(p0, float), np.array(p1, float), color=color, stroke_width=w).set_stroke(opacity=0.85)


def bubble2(txt, p0, p1, color=BLUE, size=26):
    """A speech bubble on the line between two cells, with a tail toward each of them."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    ctr = (p0 + p1) / 2
    t = T(txt, size, color)
    w, h = t.width + 0.34, t.height + 0.32
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.18).move_to(ctr)
    parts = [box]
    for tgt in (p0, p1):
        d = tgt - ctr
        d = d / np.linalg.norm(d)
        k = min((w / 2) / max(abs(d[0]), 1e-6), (h / 2) / max(abs(d[1]), 1e-6))
        base = ctr + d * k
        perp = np.array([-d[1], d[0], 0])
        parts.append(Polygon(base + perp * 0.11, base + d * 0.24, base - perp * 0.11, stroke_width=0,
                             fill_color=color, fill_opacity=0.55))
    parts.append(t.move_to(ctr))
    return VGroup(*parts)


def bubble(txt, ctr, toward, color=BLUE, size=26):
    t = T(txt, size, color)
    w, h = t.width + 0.34, t.height + 0.32
    ctr, toward = np.array(ctr, float), np.array(toward, float)
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.18).move_to(ctr)
    d = toward - ctr
    d = d / np.linalg.norm(d)
    k = min((w / 2) / max(abs(d[0]), 1e-6), (h / 2) / max(abs(d[1]), 1e-6))
    base = ctr + d * k
    perp = np.array([-d[1], d[0], 0])
    tail = Polygon(base + perp * 0.11, base + d * 0.24, base - perp * 0.11, stroke_width=0,
                   fill_color=color, fill_opacity=0.55)
    return VGroup(box, tail, t.move_to(ctr))


def xmark(c, s=0.26, color=RED, w=9):
    c = np.array(c, float)
    return VGroup(Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=w),
                  Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=w))


# ------------------------------------------------------------------------------------------
# legend chips (shown once in s10 and kept on screen to the end)
# ------------------------------------------------------------------------------------------
def legend_chips():
    return [chip("proneural factor", PRO, size=26, pad=0.16), chip("E(spl) repressor", REP, size=26, pad=0.16),
            chip("Delta", DEL, size=26, pad=0.16), chip("Notch", NOT, size=26, pad=0.16)]


def legend_col():
    cs = legend_chips()
    g = VGroup(*cs).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    g.move_to([5.4, 1.95, 0])
    return cs


def legend_row():
    cs = legend_chips()
    VGroup(*cs).arrange(RIGHT, buff=0.3).move_to([0, -3.08, 0])
    return cs


# ------------------------------------------------------------------------------------------
# the cell: grey body, a nucleus holding two bars (proneural, repressor), a Delta ball and a Notch crescent
# ------------------------------------------------------------------------------------------
class Cell:
    def __init__(self, cx, cy, R, side, name="", kang=18, cang=-18, ks=1.0, labpos=None, nucr=0.73, lab_size=40, refv=0.5, kstalk=None):
        s = R / 2.2
        self.ks = ks
        self.stalk0 = 0.3 * s * ks + (ks - 1) * 0.25
        self.shift = 0.4 * s * ks
        self.kst = kstalk if kstalk is not None else self.stalk0
        self.cx, self.cy, self.R, self.side, self.s = cx, cy, R, side, s
        self.c = np.array([cx, cy, 0.0])
        self.pro, self.rep, self.delta, self.notch = (ValueTracker(0) for _ in range(4))
        self.cupvis, self.bind, self.pull = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.kvis, self.inh_on = ValueTracker(1), ValueTracker(0)
        self.cupcol = NOT
        self.body = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to(self.c)
        self.nuc = Circle(radius=nucr * R, stroke_color=GREY, stroke_width=2, fill_opacity=0).move_to(self.c).set_stroke(opacity=0.6)
        lp = labpos if labpos is not None else [cx - side * (R + 0.55), cy, 0]
        self.label = T(name, lab_size, GREY, weight=BOLD).move_to(lp) if name else None
        self.H, self.BASE, self.BW = 0.92 * R, cy - 0.46 * R, 0.18 * R
        self.bxp, self.bxr = cx - 0.23 * R, cx + 0.23 * R
        trk = [Rectangle(width=self.BW, height=self.H, stroke_color=GREY, stroke_width=2, fill_opacity=0)
               .set_stroke(opacity=0.45).move_to([x, self.BASE + self.H / 2, 0]) for x in (self.bxp, self.bxr)]
        yref = self.BASE + refv * self.H
        self.refy = yref
        ref = DashedLine([self.bxp - self.BW * 0.9, yref, 0], [self.bxr + self.BW * 0.9, yref, 0], dash_length=0.09,
                         color=TEXT, stroke_width=2.5).set_stroke(opacity=0.7)
        self.ref = ref
        self.tracks = VGroup(*trk, ref)
        ka = np.radians(kang if side > 0 else 180 + kang)
        ca = np.radians(cang if side > 0 else 180 + cang)
        self.kp = self.c + R * np.array([np.cos(ka), np.sin(ka), 0])
        self.cp = self.c + R * np.array([np.cos(ca), np.sin(ca), 0])
        self.u = np.array([side, 0, 0.0])
        self.e, self.cupR = self.stalk0, 0.19 * R * ks
        self.cupc0 = self.cp + self.u * (self.e + self.cupR)
        self.L = 1.0
        self.pro_bar = always_redraw(lambda: self._bar(self.bxp, self.pro.get_value(), PRO))
        self.rep_bar = always_redraw(lambda: self._bar(self.bxr, self.rep.get_value(), REP))
        self.inh = always_redraw(self._inh)
        self.stalk = always_redraw(self._stalk)
        self.knob = always_redraw(self._knob)
        self.cup = always_redraw(self._cup)
        self.dyn = [self.pro_bar, self.rep_bar, self.inh, self.stalk, self.knob, self.cup]
        self.static = VGroup(self.body, self.nuc, *([self.label] if self.label else []))

    def link(self, other):
        self.L = max(0.0, self.side * (other.cupc0[0] - self.kp[0]) - self.kst)

    def _bar(self, x, v, color):
        h = max(1e-3, v * self.H)
        return Rectangle(width=self.BW, height=h, stroke_width=0, fill_color=color, fill_opacity=0.92).move_to([x, self.BASE + h / 2, 0])

    def _inh(self):
        r = self.rep.get_value() * self.inh_on.get_value()
        w = 0.001 if r < 0.02 else 2 + 7 * r
        y = self.BASE + 0.62 * self.H
        return inhib([self.bxr - self.BW / 2, y, 0], [self.bxp + self.BW / 2, y, 0], w=w, half=0.2 * max(0.7, self.s))

    def knob_c(self):
        sh = self.kst + self.L * self.bind.get_value() - self.shift * self.pull.get_value()
        return self.kp + np.array([self.side * sh, 0, 0])

    def knob_r(self, d):
        return self.R * (0.03 + 0.14 * d) * self.ks

    def _knob(self):
        d = self.delta.get_value() * self.kvis.get_value()
        on = d > 0.01
        r = self.knob_r(d) if on else 1e-3
        return Circle(radius=r, stroke_color=DEL, stroke_width=3 if on else 0, fill_color=DEL,
                      fill_opacity=0.92 if on else 0).move_to(self.knob_c())

    def _stalk(self):
        on = self.delta.get_value() * self.kvis.get_value() > 0.01
        return Line(self.kp, self.knob_c(), color=GREY, stroke_width=5 if on else 0.001)

    def cup_c(self):
        return self.cupc0 + self.u * self.shift * self.pull.get_value()

    def _cup(self):
        v = self.cupvis.get_value()
        w = max(0.001, v * (3 + 10 * self.notch.get_value()) * (0.55 + 0.45 * self.s) * (1 + (self.ks - 1) * 0.5))
        c = self.cup_c()
        st = PI / 2 if self.side > 0 else -PI / 2
        arc = Arc(radius=self.cupR, start_angle=st, angle=PI, arc_center=c, color=self.cupcol, stroke_width=w)
        stem = Line(self.cp, c - self.u * self.cupR, color=self.cupcol, stroke_width=max(0.001, v * 4.5))
        return VGroup(arc, stem)

    def dashed_cup(self):
        st = PI / 2 if self.side > 0 else -PI / 2
        arc = Arc(radius=self.cupR, start_angle=st, angle=PI, arc_center=self.cup_c(), color=NOT, stroke_width=6)
        return DashedVMobject(arc, num_dashes=13).set_stroke(opacity=0.85)

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


def contact_pair():
    """Two big cells for the zoom on the contact (scenes 3 and 4): Delta and Notch about three times larger."""
    return link_pair(Cell(-3.9, 0.0, 2.7, +1, kang=0, cang=0, nucr=0.62, kstalk=0.72), Cell(3.9, 0.0, 2.7, -1, kang=0, cang=0, nucr=0.62, kstalk=0.72))


TOPY, TOPR = 1.9, 1.85


def top_pair():
    return link_pair(Cell(-4.9, TOPY, TOPR, +1, "A", ks=1.3, labpos=[-6.45, 3.55, 0], lab_size=36),
                     Cell(-0.1, TOPY, TOPR, -1, "B", ks=1.3, labpos=[1.55, 3.55, 0], lab_size=36))


def med_pair():
    return link_pair(Cell(-3.05, 0.6, 1.85, +1, "A", kang=15, cang=-15), Cell(3.05, 0.6, 1.85, -1, "B", kang=15, cang=15))


# ------------------------------------------------------------------------------------------
# the cluster of five cells (scenes 1 and 2)
# ------------------------------------------------------------------------------------------
RR = 0.8
RING = [(3.9 * np.cos(np.radians(a)), -0.1 + 2.7 * np.sin(np.radians(a))) for a in (90, 162, 234, 306, 18)]


def ring_cells():
    bodies, bs = [], []
    for x, y in RING:
        bodies.append(Circle(radius=RR, stroke_color=GREEN, stroke_width=5, fill_color=GREY, fill_opacity=0.10).move_to([x, y, 0]))
        bs.append(Rectangle(width=0.26, height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.92).move_to([x, y, 0]))
    return bodies, bs


def ring_pts():
    return [np.array([x, y, 0.0]) for x, y in RING]


def ring_arrows():
    out = []
    P = ring_pts()
    for i in range(5):
        j = (i + 1) % 5
        d = (P[j] - P[i]) / np.linalg.norm(P[j] - P[i])
        out.append(DoubleArrow(P[i] + d * (RR + 0.12), P[j] - d * (RR + 0.12), buff=0, color=NOT, stroke_width=5,
                               tip_length=0.22, max_stroke_width_to_length_ratio=20))
    return out


def ring_bubbles():
    P = ring_pts()
    return [bubble2("not you", P[i], P[(i + 1) % 5]) for i in range(5)]


def ring_centre_label():
    return VGroup(T("each cell signals", 32, NOT), T("its neighbours", 32, NOT)).arrange(DOWN, buff=0.12).move_to([0, -0.1, 0])


# ------------------------------------------------------------------------------------------
# the nucleus stage (scenes 5 to 9): a big nucleus, DNA through the middle, large gene boxes
# ------------------------------------------------------------------------------------------
DNAY = -1.6
PRO_X, TG_X, DEL_X = -4.3, 3.0, 5.0
CSL_X = -1.1
GH = 2.7
GTOP = DNAY + 0.03 + GH
FAC_Y = 2.2
ONE_Y = 1.52


def mk_stage():
    """The nucleus fills about three quarters of the frame height; DNA runs through its middle."""
    nuc = RoundedRectangle(width=13.2, height=6.3, corner_radius=1.6, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.05).move_to([0, -0.55, 0])
    dna = Line([-6.3, DNAY, 0], [6.4, DNAY, 0], color=GREY, stroke_width=10)
    dl = T("DNA", 28, GREY).move_to([-5.75, DNAY - 0.55, 0])
    nl = T("nucleus", 28, GREY).move_to([5.3, -3.3, 0])
    return nuc, dna, dl, nl


class Gene(VGroup):
    def __init__(self, label, color, x, w=3.4, level=0.5):
        rect = Rectangle(width=w, height=GH, stroke_width=3)
        txt = T(label, 36, color)
        super().__init__(rect, txt)
        self.col = color
        self.move_to([x, DNAY + GH / 2 + 0.03, 0])
        self.setl(level)

    def setl(self, v):
        self[0].set_fill(self.col, 0.05 + 0.5 * v).set_stroke(self.col, opacity=0.3 + 0.7 * v)
        self[1].set_opacity(0.55 + 0.45 * v)
        return self

    def lvl(self, v):
        return [self[0].animate.set_fill(self.col, 0.05 + 0.5 * v).set_stroke(self.col, opacity=0.3 + 0.7 * v),
                self[1].animate.set_opacity(0.55 + 0.45 * v)]


def mk_csl(with_text=True):
    box = RoundedRectangle(corner_radius=0.16, width=2.2, height=1.6, stroke_color=NOT, stroke_width=3,
                           fill_color=NOT, fill_opacity=0.2)
    box.move_to([CSL_X, DNAY + 0.03 + 0.8, 0])
    txt = T("CSL", 46, NOT).move_to(box)
    return box, txt


def dock_pos():
    return np.array([CSL_X, DNAY + 0.03 + 1.6 + 0.55, 0])


def mk_blob(pos, r=0.5):
    return Circle(radius=r, stroke_color=NOT, stroke_width=3, fill_color=NOT, fill_opacity=0.92).move_to(pos)


def csl_arrow():
    return arr([CSL_X + 1.2, DNAY + 0.8, 0], [TG_X - 1.7 - 0.08, DNAY + 0.8, 0], color=NOT, w=7)


def soh_label():
    return T("Suppressor of Hairless in the fly", 28, GREY).move_to([CSL_X - 0.2, DNAY - 1.45, 0])


def dnabp_label():
    return T("DNA-binding protein", 28, NOT).move_to([CSL_X, DNAY - 0.55, 0])


def mk_cap():
    return T("Enhancer of split", 30, REP).move_to([TG_X, DNAY - 0.55, 0])


def mk_repchip(x, y):
    return chip("E(spl) repressor", REP, size=28, pad=0.16).move_to([x, y, 0])


def mk_fac():
    return chip("proneural factor", PRO, size=28, pad=0.16).move_to([PRO_X, FAC_Y, 0])


REP_REST_Y = GTOP + 0.04 + 0.45


def rep_bar_over(x):
    return Line([x - 1.8, GTOP + 0.03, 0], [x + 1.8, GTOP + 0.03, 0], color=REP, stroke_width=10)


# ------------------------------------------------------------------------------------------
# the comparison table (scenes 10 to 14): small tags with an arrow in front of each name
# ------------------------------------------------------------------------------------------
COLX = {"A": -5.4, "B": 0.35}
LINEY = {(1, 0): -0.65, (2, 0): -1.55, (3, 0): -2.4, (3, 1): -2.95}
RULES = [-0.15, -1.1, -2.0, -3.3]
STEPY = {1: -0.65, 2: -1.55, 3: -2.68}
TSPEC = {
    1: {"A": [[("up", "Delta", DEL)]], "B": [[("up", "Notch", NOT), ("up", "repressor", REP)]]},
    2: {"B": [[("dn", "proneural", PRO), ("dn", "Delta", DEL)]]},
    3: {"A": [[("dn", "Notch", NOT), ("dn", "repressor", REP)],
              [("up", "proneural", PRO), ("up", "Delta", DEL)]]},
}
STEP_KEYS = {1: [(1, "A", 0, 0), (1, "B", 0, 0), (1, "B", 0, 1)],
             2: [(2, "B", 0, 0), (2, "B", 0, 1)],
             3: [(3, "A", 0, 0), (3, "A", 0, 1), (3, "A", 1, 0)],
             4: [(3, "A", 1, 1)]}
TAGSZ = 32


def tag(sign, text, color):
    tri = Triangle().scale(0.16).set_fill(color, 1).set_stroke(width=0)
    if sign == "dn":
        tri.rotate(PI)
    return VGroup(tri, T(text, TAGSZ, color)).arrange(RIGHT, buff=0.12)


def build_table():
    items = {}
    for r, cols in TSPEC.items():
        for c, lines in cols.items():
            for li, line in enumerate(lines):
                x = COLX[c]
                for j, (sg, tx, co) in enumerate(line):
                    m = tag(sg, tx, co)
                    m.move_to([x + m.width / 2, LINEY[(r, li)], 0])
                    items[(r, c, li, j)] = m
                    x += m.width + 0.4
    # a dash in the slot where nothing changes, so the row does not look unfinished
    for (r, c) in ((2, "A"), (3, "B")):
        d = T("-", 34, GREY).move_to([COLX[c] + 0.12, LINEY[(r, 0)], 0])
        items[(r, c, 0, 9)] = d
    labs = {r: T(f"Step {r}", 28, GREY, weight=BOLD).move_to([-6.8, STEPY[r], 0], aligned_edge=LEFT) for r in (1, 2, 3)}
    hA = Dot(radius=0.001, fill_opacity=0, stroke_width=0)   # no header row: the cells above are labelled A and B
    hB = Dot(radius=0.001, fill_opacity=0, stroke_width=0)
    rules = VGroup(*[Line([-6.8, y, 0], [6.8, y, 0], color=GREY, stroke_width=1.5).set_stroke(opacity=0.45) for y in RULES])
    return items, labs, hA, hB, rules


def table_state(scene, step, shown_now=0, dim_to=0.45, show_label=True):
    """Add the table as it stands at the start of `step`; earlier rows dimmed. shown_now = how many of
    this step's items are already on screen. Returns the item dict, label dict."""
    items, labs, hA, hB, rules = build_table()
    scene.add(hA, hB, rules)
    row = min(step, 3)
    for r in range(1, row):
        for k, m in items.items():
            if k[0] == r:
                scene.add(m.set_opacity(dim_to))
        scene.add(labs[r].set_opacity(dim_to))
    keys = STEP_KEYS[step][:shown_now]
    for k in keys:
        scene.add(items[k])
    if shown_now and (row, "B", 0, 9) in items:
        scene.add(items[(row, "B", 0, 9)])
    if show_label:
        scene.add(labs[row])
    return items, labs


def table_rows_dim(items, labs, upto, o=0.45):
    anims = []
    for r in range(1, upto + 1):
        for k, m in items.items():
            if k[0] == r:
                anims.append(m.animate.set_opacity(o))
        anims.append(labs[r].animate.set_opacity(o))
    return anims


def top_state(step):
    """Pair at the end of table step `step` (0 = start, 1, 2, 3, 4 = after 'more Delta')."""
    A, B = top_pair()
    for c in (A, B):
        c.setv(pro=0.5, rep=0.5, notch=0.35, delta=0.5, cupvis=1, bind=1, inh_on=1)
    if step >= 1:
        A.setv(delta=0.72)
        B.setv(notch=0.75, rep=0.8)
    if step >= 2:
        B.setv(pro=0.15, delta=0.2)
        B.lose_now()
    if step >= 3:
        A.setv(notch=0.1, rep=0.1, pro=0.85)
    if step >= 4:
        A.setv(delta=0.98)
    return A, B


def start_caption():
    """'start level' label at the dashed tick (cell B side), drawn once in scene 10 and kept to scene 14."""
    y = TOPY
    x0 = -0.1 + TOPR + 0.05
    ln = DashedLine([x0, y, 0], [x0 + 0.33, y, 0], dash_length=0.08, color=TEXT, stroke_width=2.5).set_stroke(opacity=0.7)
    tx = T("start level", 26, TEXT).set_opacity(0.85).move_to([x0 + 0.43, y, 0], aligned_edge=LEFT)
    return VGroup(ln, tx)


def top_scene(scene, step, shown_now=0, with_legend=True, show_label=True, state=None):
    """state = the step whose end-state the cells start in (default: the table step itself)."""
    A, B = top_state(step if state is None else state)
    A.put(scene)
    B.put(scene)
    items, labs = table_state(scene, step, shown_now, show_label=show_label)
    leg = legend_col()
    if with_legend:
        scene.add(*leg)
    cap = start_caption()
    scene.add(cap)
    return A, B, items, labs, leg, cap


def NOTE_Y():
    return -3.6


def note_chip(text, color=GOLD):
    return chip(text, color, size=26, pad=0.16).move_to([0, NOTE_Y(), 0])


# ------------------------------------------------------------------------------------------
# the loop simulation (same equation as the earlier film)
# ------------------------------------------------------------------------------------------
def simulate(a0, b0, n=330, tmax=5.5):
    f = lambda x: 1 / (1 + (x / 0.5) ** 4)
    a, b, dt, out = a0, b0, tmax / n, [(a0, b0)]
    for _ in range(n):
        a, b = a + dt * (f(b) - a), b + dt * (f(a) - b)
        out.append((a, b))
    return out


def run_sim(scene, A, B, arr_, run_time):
    s = ValueTracker(0)
    holder = Mobject()

    def upd(_):
        a, b = arr_[int(round(s.get_value() * (len(arr_) - 1)))]
        A.setv(pro=a, rep=b, notch=b, delta=a)
        B.setv(pro=b, rep=a, notch=a, delta=b)
    holder.add_updater(upd)
    scene.add(holder)
    scene.play(s.animate.set_value(1), run_time=run_time, rate_func=linear)
    holder.remove_updater(upd)
    scene.remove(holder)


# loop geometry for the medium pair
def loop_arcs():
    top = arc_inh([-1.86, 2.02, 0], [1.86, 2.02, 0], bend=-1.6)
    bot = arc_inh([1.86, -0.82, 0], [-1.86, -0.82, 0], bend=-1.6)
    return top, bot


MED_BASE = dict(pro=0.5, rep=0.5)
LEAD = 0.58


def med_base(A, B):
    for c in (A, B):
        c.setv(pro=0.5, rep=0.5, notch=0.35, delta=0.5, kvis=0, cupvis=0, inh_on=1)


def med_scene(scene, legend=True):
    A, B = med_pair()
    med_base(A, B)
    A.put(scene)
    B.put(scene)
    leg = legend_row()
    if legend:
        scene.add(*leg)
    return A, B, leg


def banner_predict():
    return T("Predict", 44, GOLD, font=TITLE_FONT).move_to([0, 3.45, 0])


def case_label(text):
    return T(text, 32, TEXT).move_to([0, 2.9, 0])


def qring_centre():
    return np.array([0.0, 1.3, 0.0])


def qmark():
    return T("?", 64, GOLD, font=TITLE_FONT).move_to(qring_centre())


def cups_dashed(A, B):
    return VGroup(A.dashed_cup(), B.dashed_cup())


# ==========================================================================================
class S00Title(TitleCard):
    LESSON = "Proneural genes and lateral inhibition"
    TITLE = "The Loop, One Arrow at a Time"


# ------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        bodies, bars = ring_cells()
        self.play(LaggedStart(*[GrowFromCenter(b) for b in bodies], lag_ratio=0.1),
                  LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars], lag_ratio=0.1), run_time=0.8)
        q = VGroup(T("What picks", 46, GOLD, font=TITLE_FONT), T("one?", 46, GOLD, font=TITLE_FONT)).arrange(DOWN, buff=0.18).move_to([0, -0.1, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.at("has pronural factor")
        chp = chip("proneural factor", PRO, size=26, pad=0.16).move_to([-5.2, 3.3, 0])
        self.play(FadeIn(chp, shift=RIGHT * 0.2), *[Indicate(r, color=PRO, scale_factor=1.25) for r in bars], run_time=0.9)
        self.at("so what picks one")
        self.play(*[Indicate(b, color=TEXT, scale_factor=1.08) for b in bodies], Indicate(q, color=GOLD, scale_factor=1.1), run_time=0.9)
        self.finish()


def s01_end_state(scene):
    bodies, bars = ring_cells()
    chp = chip("proneural factor", PRO, size=26, pad=0.16).move_to([-5.2, 3.3, 0])
    scene.add(*bodies, *bars, chp)
    return bodies, bars, chp


class S02Notyou(SpokenScene):
    def construct(self):
        bodies, bars, chp = s01_end_state(self)
        self.at("signal to each other")
        arrows = ring_arrows()
        lab = ring_centre_label()
        self.play(LaggedStart(*[GrowFromCenter(a) for a in arrows], lag_ratio=0.12), FadeIn(lab), run_time=1.0)
        self.at("through notch")
        nch = chip("Notch signal", NOT, size=26, pad=0.16).move_to([-5.35, 2.55, 0])
        self.play(FadeIn(nch, shift=RIGHT * 0.2), *[Indicate(a, color=NOT, scale_factor=1.15) for a in arrows], run_time=0.8)
        self.at("says not you")
        bubs = ring_bubbles()
        self.play(LaggedStart(*[ReplacementTransform(a, b) for a, b in zip(arrows, bubs)], lag_ratio=0.12), run_time=1.1)
        self.finish()


def s02_end_state(scene):
    bodies, bars, chp = s01_end_state(scene)
    nch = chip("Notch signal", NOT, size=26, pad=0.16).move_to([-5.35, 2.55, 0])
    lab = ring_centre_label()
    bubs = ring_bubbles()
    scene.add(nch, lab, *bubs)
    return bodies, bars, [chp, nch, lab, *bubs]


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# the contact (scenes 3 and 4): a zoom on two touching cells. Delta (ball on a thick stalk) is anchored in the
# left cell's membrane, Notch (a crescent on a thick stem, with a tail and a small blob inside) in the right cell's.
# ------------------------------------------------------------------------------------------
CR = 6.5            # radius of each big cell (only the facing arc is on screen)
XL0, XR = -3.9, 2.9   # membrane positions: left cell before it slides in, right cell
STALK, BALLR = 2.2, 1.1
CUPC0, CUPR = 0.7, 1.45
SLIDE, PULLD = 2.4, 1.3
APEX_P1 = CUPC0 - PULLD + CUPR   # where the Notch stem leaves the crescent once the pull is complete
CUT1_X = 1.85
TAIL = 1.0
BLOBR = 0.6
NUCR = 4.6
BIGY = 0.0
BRIGHT = "#E8F6FF"


class Contact:
    def __init__(self):
        self.bind, self.pull = ValueTracker(0), ValueTracker(0)
        self.dvis, self.nvis, self.vis = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.hl = ValueTracker(0)
        self.cut = False       # after the first cut the outer stem is a separate piece
        self.stubvis = ValueTracker(1)
        self.tailvis = ValueTracker(1)
        self.blobpos = ValueTracker(0)   # 0 = at the tail, 1 = in the nucleus
        self.blobx0 = XR + TAIL
        self.blobx1 = 6.0
        self.bodyL = always_redraw(self._bodyL)
        self.bodyR = always_redraw(self._bodyR)
        self.nucL = always_redraw(self._nucL)
        self.nucR = always_redraw(self._nucR)
        self.tail = always_redraw(self._tail)
        self.blob = always_redraw(self._blob)
        self.stem = always_redraw(self._stem)
        self.stub = always_redraw(self._stub)
        self.cupm = always_redraw(self._cup)
        self.dstalk = always_redraw(self._dstalk)
        self.ball = always_redraw(self._ball)
        self.dyn = [self.bodyL, self.bodyR, self.nucL, self.nucR, self.tail, self.stem, self.stub, self.cupm, self.dstalk, self.ball, self.blob]

    # positions
    def xL(self):
        return XL0 + SLIDE * self.bind.get_value() - PULLD * self.pull.get_value()

    def ball_c(self):
        d = self.dvis.get_value()
        return np.array([self.xL() + STALK * max(d, 0.02), BIGY, 0.0])

    def ball_r(self):
        return BALLR * self.dvis.get_value()

    def cup_cx(self):
        return CUPC0 - PULLD * self.pull.get_value()

    def apex(self):
        return np.array([self.cup_cx() + CUPR, BIGY, 0.0])

    def cup_bottom(self):
        return np.array([self.cup_cx(), BIGY - CUPR - 0.06, 0.0])

    def blob_c(self):
        p = self.blobpos.get_value()
        return np.array([self.blobx0 + (self.blobx1 - self.blobx0) * p, BIGY, 0.0])

    # parts
    def _bodyL(self):
        v = self.vis.get_value()
        hl = self.hl.get_value()
        col = interpolate_color(ManimColor(GREY), ManimColor(BRIGHT), hl)
        return Circle(radius=CR, stroke_color=col, stroke_width=(6 + 5 * hl) * (1 if v > 0.01 else 0.001), fill_color=GREY,
                      fill_opacity=0.08 * v).move_to([self.xL() - CR, BIGY, 0]).set_stroke(opacity=v)

    def _bodyR(self):
        v = self.vis.get_value()
        return Circle(radius=CR, stroke_color=GREY, stroke_width=6 if v > 0.01 else 0.001, fill_color=GREY,
                      fill_opacity=0.08 * v).move_to([XR + CR, BIGY, 0]).set_stroke(opacity=v)

    def _nucL(self):
        v = self.vis.get_value()
        return Circle(radius=NUCR, stroke_color=GREY, stroke_width=3 if v > 0.01 else 0.001, fill_opacity=0).move_to(
            [self.xL() - CR, BIGY, 0]).set_stroke(opacity=0.6 * v)

    def _nucR(self):
        v = self.vis.get_value()
        return Circle(radius=NUCR, stroke_color=GREY, stroke_width=3 if v > 0.01 else 0.001, fill_opacity=0).move_to(
            [XR + CR, BIGY, 0]).set_stroke(opacity=0.6 * v)

    def _dstalk(self):
        d = self.dvis.get_value()
        on = d > 0.02
        return Line([self.xL() - 0.6, BIGY, 0], self.ball_c(), color=GREY, stroke_width=24 if on else 0.001)

    def _ball(self):
        d = self.dvis.get_value()
        on = d > 0.02
        return Circle(radius=max(self.ball_r(), 1e-3), stroke_color=DEL, stroke_width=3 if on else 0, fill_color=DEL,
                      fill_opacity=0.95 if on else 0).move_to(self.ball_c())

    def _cup(self):
        v = self.nvis.get_value()
        arc = Arc(radius=CUPR, start_angle=-PI / 2, angle=PI, arc_center=[self.cup_cx(), BIGY, 0], color=NOT,
                  stroke_width=max(0.001, 22 * v))
        return arc

    def _stem(self):
        v = self.nvis.get_value()
        a = self.apex()
        end = a + np.array([CUT1_X - APEX_P1, 0, 0]) if self.cut else np.array([XR, BIGY, 0])
        # thick when relaxed, thinner as it stretches
        w = (20 - 9 * min(1, self.pull.get_value())) * v
        return Line(a, end, color=NOT, stroke_width=max(0.001, w))

    def _stub(self):
        v = self.nvis.get_value() * self.stubvis.get_value() * (1.0 if self.cut else 0.0)
        return Line([CUT1_X, BIGY, 0], [XR, BIGY, 0], color=NOT, stroke_width=max(0.001, 11 * v)).set_stroke(opacity=max(v, 0.0))

    def _tail(self):
        v = self.nvis.get_value() * self.tailvis.get_value()
        b = self.blob_c()
        return Line(b - np.array([TAIL, 0, 0]), b, color=NOT, stroke_width=max(0.001, 20 * v))

    def _blob(self):
        v = self.nvis.get_value()
        on = v > 0.02
        return Circle(radius=max(BLOBR * v, 1e-3), stroke_color=NOT, stroke_width=3 if on else 0, fill_color=NOT,
                      fill_opacity=0.95 if on else 0).move_to(self.blob_c())

    def put(self, scene):
        scene.add(*self.dyn)

    def freeze(self):
        for m in self.dyn:
            m.update(0)
            m.clear_updaters()
        return self.dyn


def delta_chip():
    return chip("Delta", DEL, size=30, pad=0.18).move_to([-3.6, 3.1, 0])


def notch_chip():
    return chip("Notch", NOT, size=30, pad=0.18).move_to([1.2, -3.3, 0])


def delta_leader(K, chip_):
    return always_redraw(lambda: leader(chip_.get_bottom() + DOWN * 0.02, K.ball_c() + np.array([0, K.ball_r() + 0.04, 0]), color=DEL, w=3))


def notch_leader(K, chip_):
    return always_redraw(lambda: leader(chip_.get_top() + UP * 0.02, K.cup_bottom(), color=NOT, w=3))


def inner_chip():
    return chip("inner part of Notch", NOT, size=30, pad=0.18).move_to([4.9, 3.25, 0])


def inner_leader(K, chip_):
    return always_redraw(lambda: leader(chip_.get_bottom() + DOWN * 0.02, K.blob_c() + np.array([0, BLOBR + 0.04, 0]), color=NOT, w=3))


def pull_marks():
    tug = arr([1.7, 2.35, 0], [-0.6, 2.35, 0], color=DEL, w=14, tip=0.45)
    tl = T("pull", 34, DEL).move_to([0.55, 2.95, 0])
    return tug, tl


def nucleus_text():
    return T("nucleus", 30, GREY).move_to([5.95, -2.6, 0])


class S03Delta(SpokenScene):
    def construct(self):
        K = Contact()
        bodies, bars, others = s02_end_state(self)
        self.add(*K.dyn)
        self.play(*[FadeOut(m) for m in (*bodies, *bars, *others)], K.vis.animate.set_value(1), run_time=0.9)
        self.at("protein in the")
        dch = delta_chip()
        dl = delta_leader(K, dch)
        self.play(K.dvis.animate.set_value(1.0), FadeIn(dch, shift=UP * 0.15), Create(dl), run_time=0.8)
        self.at("membrane of one")
        self.play(K.hl.animate.set_value(1), run_time=0.4)
        self.play(K.hl.animate.set_value(0), run_time=0.5)
        self.at("binds notch")
        nch = notch_chip()
        nl = notch_leader(K, nch)
        self.play(K.nvis.animate.set_value(1), FadeIn(nch, shift=DOWN * 0.15), Create(nl), run_time=0.7)
        self.at("the cell it touches")
        self.play(K.bind.animate.set_value(1), run_time=0.9)
        self.at("pulls")
        tug, tl = pull_marks()
        self.play(K.pull.animate.set_value(1), GrowArrow(tug), FadeIn(tl), run_time=0.9)
        self.finish()


def s03_end_state(scene):
    K = Contact()
    K.vis.set_value(1)
    K.dvis.set_value(1)
    K.nvis.set_value(1)
    K.bind.set_value(1)
    K.pull.set_value(1)
    dch, nch = delta_chip(), notch_chip()
    dl, nl = delta_leader(K, dch), notch_leader(K, nch)
    tug, tl = pull_marks()
    K.put(scene)
    scene.add(dch, nch, dl, nl, tug, tl)
    return K, dict(dch=dch, nch=nch, dl=dl, nl=nl, tug=tug, tl=tl)


def cut_marks():
    out = []
    for k, x in enumerate((CUT1_X, XR)):
        p = np.array([x, BIGY, 0.0])
        mark = Line(p + np.array([-0.3, -0.75, 0]), p + np.array([0.3, 0.75, 0]), color=TEXT, stroke_width=14)
        num = T(str(k + 1), 44, TEXT, weight=BOLD).move_to(p + np.array([0, 1.35, 0]))
        out.append((mark, num))
    return out


class S04Cuts(SpokenScene):
    def construct(self):
        K, S = s03_end_state(self)
        nt = nucleus_text()
        (m1, n1), (m2, n2) = cut_marks()
        self.play(FadeOut(S["tug"]), FadeOut(S["tl"]), FadeIn(nt), Create(m1), FadeIn(n1), run_time=0.4)
        K.cut = True
        self.play(Create(m2), FadeIn(n2), run_time=0.4)
        self.at("free the inner")
        ich = inner_chip()
        il = inner_leader(K, ich)
        # the outer pieces fall away with the sending cell, the stub between the cuts fades, the inner part is free
        self.play(K.pull.animate.set_value(1.8), K.stubvis.animate.set_value(0), FadeOut(m1), FadeOut(n1), FadeOut(m2), FadeOut(n2),
                  FadeIn(ich, shift=DOWN * 0.15), Create(il), run_time=0.9)
        ping(self, K.blob_c(), r=0.5, color=NOT, run_time=0.6)
        self.at("part enters")
        self.play(K.blobpos.animate.set_value(1), K.tailvis.animate.set_value(0), run_time=1.1)
        ov = Circle(radius=NUCR, stroke_color=TEXT, stroke_width=7, fill_opacity=0).move_to([XR + CR, BIGY, 0])
        self.play(FadeIn(ov), run_time=0.25)
        self.play(FadeOut(ov), run_time=0.4)
        self.finish()


def s04_end_state(scene):
    K, S = s03_end_state(scene)
    scene.remove(S["tug"], S["tl"])
    K.cut = True
    K.pull.set_value(1.8)
    K.stubvis.set_value(0)
    K.tailvis.set_value(0)
    K.blobpos.set_value(1)
    nt = nucleus_text()
    ich = inner_chip()
    il = inner_leader(K, ich)
    scene.add(nt, ich, il)
    return K, S, nt, ich, il


# ------------------------------------------------------------------------------------------
class S05Csl(SpokenScene):
    def construct(self):
        K, S, nt, ich, il = s04_end_state(self)
        nuc, dna, dl, nlab = mk_stage()
        box, txt = mk_csl()
        gone = [S["dch"], S["nch"], S["dl"], S["nl"], nt, ich, il]
        blob = K.blob
        dyn = K.freeze()
        self.add(*dyn)
        others = [m for m in dyn if m not in (K.nucR, K.blob)]
        self.play(ReplacementTransform(K.nucR, nuc), *[FadeOut(m) for m in gone + others],
                  blob.animate.move_to([-3.4, 0.9, 0]).scale(0.85), FadeIn(nlab), run_time=0.9)
        self.at("dna binding protein")
        bp = dnabp_label()
        self.play(Create(dna), FadeIn(dl), FadeIn(box, shift=DOWN * 0.2), FadeIn(bp, shift=UP * 0.1), run_time=0.7)
        self.at("called csl")
        soh = soh_label()
        self.play(Write(txt), FadeIn(soh, shift=UP * 0.1), run_time=0.6)
        self.at("turns on")
        self.play(blob.animate.move_to(dock_pos()), run_time=0.8)
        self.at("target genes")
        tg = Gene("target genes", GREY, TG_X, level=0.12)
        ar = csl_arrow()
        self.play(FadeIn(tg), GrowArrow(ar), run_time=0.5)
        self.play(*tg.lvl(1.0), run_time=0.8)
        self.finish()


def s05_end_state(scene, tg_color=GREY, label="target genes", soh=True):
    nuc, dna, dl, nlab = mk_stage()
    box, txt = mk_csl()
    blob = mk_blob(dock_pos())
    tg = Gene(label, tg_color, TG_X, level=1.0)
    ar = csl_arrow()
    bp = dnabp_label()
    scene.add(nuc, dna, dl, nlab, box, txt, blob, tg, ar, bp)
    out = dict(nuc=nuc, dna=dna, dl=dl, nlab=nlab, box=box, txt=txt, blob=blob, tg=tg, ar=ar, bp=bp)
    if soh:
        out["soh"] = soh_label()
        scene.add(out["soh"])
    return out


class S06Espl(SpokenScene):
    def construct(self):
        S = s05_end_state(self)
        self.at("pronural cluster")
        cl = T("in a proneural cluster", 30, PRO).move_to([0.4, 2.0, 0])
        self.play(FadeOut(S["soh"]), FadeIn(cl, shift=DOWN * 0.1), run_time=0.7)
        self.at("targets that matter")
        self.play(Indicate(S["tg"], color=TEXT, scale_factor=1.08), run_time=0.9)
        self.at("enhancer of split")
        new = Gene("E(spl)", REP, TG_X, level=1.0)
        cap = mk_cap()
        self.play(ReplacementTransform(S["tg"], new), FadeIn(cap, shift=UP * 0.1), FadeOut(cl), run_time=0.9)
        self.finish()


def s06_end_state(scene):
    S = s05_end_state(scene, tg_color=REP, label="E(spl)", soh=False)
    cap = mk_cap()
    scene.add(cap)
    S["cap"] = cap
    return S


class S07Espl2(SpokenScene):
    def construct(self):
        S = s06_end_state(self)
        pg = Gene("proneural", PRO, PRO_X, level=0.6)
        self.play(FadeIn(pg), run_time=0.4)
        self.at("make repressors")
        rep = mk_repchip(TG_X, 2.05)
        self.play(FadeIn(rep, shift=UP * 0.3), run_time=0.5)
        self.at("that switch")
        self.play(rep.animate.move_to([PRO_X, REP_REST_Y, 0]), run_time=0.6)
        self.at("genes off")
        bar = rep_bar_over(PRO_X)
        self.play(Create(bar), *pg.lvl(0.08), run_time=0.5)
        self.finish()


def s07_end_state(scene):
    S = s06_end_state(scene)
    pg = Gene("proneural", PRO, PRO_X, level=0.08)
    rep = mk_repchip(PRO_X, REP_REST_Y)
    bar = rep_bar_over(PRO_X)
    scene.add(pg, rep, bar)
    S.update(pg=pg, rep=rep, bar=bar)
    return S


class S08Return(SpokenScene):
    def construct(self):
        S = s07_end_state(self)
        clear = [S[k] for k in ("box", "txt", "blob", "ar", "cap", "tg", "bp", "rep", "bar")]
        self.play(*[FadeOut(m) for m in clear], run_time=0.55)
        self.at("factors do two")
        fac = mk_fac()
        self.play(FadeIn(fac, shift=UP * 0.2), run_time=0.5)
        self.at("raise their own")
        ar = arr(fac.get_bottom() + DOWN * 0.04, [PRO_X, GTOP + 0.08, 0], color=PRO, w=8, tip=0.28)
        one = T("1: own expression", 30, TEXT)
        one.move_to([PRO_X + 0.3 + one.width / 2, ONE_Y, 0])
        self.play(GrowArrow(ar), FadeIn(one, shift=RIGHT * 0.15), run_time=0.5)
        self.play(*S["pg"].lvl(1.0), run_time=0.9)
        self.finish()


def s08_end_state(scene):
    nuc, dna, dl, nlab = mk_stage()
    pg = Gene("proneural", PRO, PRO_X, level=1.0)
    fac = mk_fac()
    ar = arr(fac.get_bottom() + DOWN * 0.04, [PRO_X, GTOP + 0.08, 0], color=PRO, w=8, tip=0.28)
    one = T("1: own expression", 30, TEXT)
    one.move_to([PRO_X + 0.3 + one.width / 2, ONE_Y, 0])
    scene.add(nuc, dna, dl, nlab, pg, fac, ar, one)
    return dict(nuc=nuc, dna=dna, dl=dl, pg=pg, fac=fac, ar=ar, one=one)


MEMY = 3.1


class S09Return2(SpokenScene):
    def construct(self):
        S = s08_end_state(self)
        self.at("standard model")
        dg = Gene("Delta", DEL, DEL_X, w=2.2, level=0.2)
        std = chip("standard model", GREY, size=28, pad=0.16).move_to([-4.8, 3.55, 0])
        self.play(FadeIn(dg), FadeIn(std, shift=DOWN * 0.1), run_time=0.5)
        # the membrane and the Delta knob come in together on "raise Delta"
        self.at("raise delta")
        fac = S["fac"]
        a2 = arr(fac.get_right() + RIGHT * 0.06, [DEL_X - 0.5, GTOP + 0.1, 0], color=PRO, w=8, tip=0.28)
        two = T("2: Delta", 30, TEXT).move_to([0.9, 2.1, 0])
        mem = Line([-6.4, MEMY, 0], [6.4, MEMY, 0], color=GREY, stroke_width=7)
        ml = T("cell membrane", 28, GREY).move_to([1.9, 3.5, 0])
        up = arr([DEL_X + 0.25, GTOP + 0.05, 0], [DEL_X + 0.25, MEMY - 0.1, 0], color=DEL, w=6)
        stalk = Line([DEL_X + 0.25, MEMY, 0], [DEL_X + 0.25, MEMY + 0.3, 0], color=GREY, stroke_width=6)
        knob = Circle(radius=0.03, stroke_color=DEL, stroke_width=3, fill_color=DEL, fill_opacity=0.92).move_to([DEL_X + 0.25, MEMY + 0.52, 0])
        self.play(GrowArrow(a2), FadeIn(two, shift=RIGHT * 0.15), *dg.lvl(1.0), FadeIn(mem), FadeIn(ml), run_time=0.45)
        self.play(GrowArrow(up), FadeIn(stalk), knob.animate.scale(8), run_time=0.55)
        self.finish()


# ------------------------------------------------------------------------------------------
class S10Pair(SpokenScene):
    def construct(self):
        A, B = top_pair()
        for c in (A, B):
            c.setv(pro=0, rep=0, delta=0, notch=0, cupvis=0, bind=1, inh_on=1)
        self.add(*A.dyn, *B.dyn)
        items, labs, hA, hB, rules = build_table()
        leg = legend_col()
        cap = start_caption()
        self.play(FadeIn(A.static), FadeIn(B.static), FadeIn(A.tracks), FadeIn(B.tracks), run_time=0.3)
        # label once, with chips that stay: the four things in each cell, one colour each
        base = dict(pro=0.5, rep=0.5, delta=0.5, notch=0.35)
        pa, pb = [A.bxp, A.BASE + 0.5 * A.H, 0], [B.bxp, B.BASE + 0.5 * B.H, 0]
        ra, rb = [A.bxr, A.BASE + 0.5 * A.H, 0], [B.bxr, B.BASE + 0.5 * B.H, 0]
        self.play(*A.to(pro=base["pro"]), *B.to(pro=base["pro"]), FadeIn(leg[0], shift=LEFT * 0.2), run_time=0.28)
        self.play(*A.to(rep=base["rep"]), *B.to(rep=base["rep"]), FadeIn(leg[1], shift=LEFT * 0.2), FadeIn(cap), run_time=0.28)
        self.play(*A.to(delta=base["delta"]), *B.to(delta=base["delta"]), FadeIn(leg[2], shift=LEFT * 0.2), run_time=0.28)
        self.play(*A.to(cupvis=1, notch=base["notch"]), *B.to(cupvis=1, notch=base["notch"]), FadeIn(leg[3], shift=LEFT * 0.2), run_time=0.28)
        self.at("a and b")
        self.play(Indicate(A.label, color=TEXT, scale_factor=1.4), Indicate(B.label, color=TEXT, scale_factor=1.4), run_time=0.6)
        self.at("one step at a time")
        self.play(FadeIn(hA), FadeIn(hB), Create(rules), run_time=0.9)
        self.finish()


class S11Step1(SpokenScene):
    def construct(self):
        A, B, items, labs, leg, cap = top_scene(self, 1, 0, show_label=False, state=0)
        self.at("step one")
        self.play(FadeIn(labs[1], shift=RIGHT * 0.15), run_time=0.5)
        self.at("a little more delta")
        self.play(*A.to(delta=0.72), run_time=0.8)
        self.play(FadeIn(items[(1, "A", 0, 0)], shift=RIGHT * 0.15), run_time=0.4)
        self.at("gets more notch")
        self.play(*B.to(notch=0.75), run_time=0.8)
        self.play(FadeIn(items[(1, "B", 0, 0)], shift=RIGHT * 0.15), run_time=0.4)
        self.at("makes more repressor")
        self.play(*B.to(rep=0.8), run_time=0.8)
        self.play(FadeIn(items[(1, "B", 0, 1)], shift=RIGHT * 0.15), run_time=0.4)
        self.finish()


class S12Step2(SpokenScene):
    def construct(self):
        # the cells start where step 1 left them; the bars move on the words
        A, B, items, labs, leg, cap = top_scene(self, 2, 0, show_label=False, state=1)
        self.at("step two")
        self.play(FadeIn(labs[2], shift=RIGHT * 0.15), FadeIn(items[(2, "A", 0, 9)]), run_time=0.5)
        self.at("is repressed")
        self.play(*B.lose(), run_time=0.8)
        ping(self, [B.cx, B.BASE + 0.62 * B.H, 0], r=0.25, color=REP, run_time=0.6)
        self.at("less pronural factor")
        self.play(*B.to(pro=0.15), run_time=0.8)
        self.play(FadeIn(items[(2, "B", 0, 0)], shift=RIGHT * 0.15), run_time=0.4)
        self.at("makes less delta")
        self.play(*B.to(delta=0.2), run_time=0.8)
        self.play(FadeIn(items[(2, "B", 0, 1)], shift=RIGHT * 0.15), run_time=0.4)
        self.finish()


class S13Step3(SpokenScene):
    def construct(self):
        # the cells start where step 2 left them (B already repressed); A's bars move on the words
        A, B, items, labs, leg, cap = top_scene(self, 3, 0, show_label=False, state=2)
        self.at("step three")
        self.play(FadeIn(labs[3], shift=RIGHT * 0.15), FadeIn(items[(3, "B", 0, 9)]), run_time=0.5)
        self.at("signal coming back")
        ping(self, A.cupc0, r=0.3, color=NOT, run_time=0.8)
        self.at("is weaker")
        self.play(*A.to(notch=0.1), run_time=0.8)
        self.play(FadeIn(items[(3, "A", 0, 0)], shift=RIGHT * 0.15), run_time=0.4)
        self.at("makes less repressor")
        self.play(*A.to(rep=0.1), run_time=0.8)
        self.play(FadeIn(items[(3, "A", 0, 1)], shift=RIGHT * 0.15), run_time=0.4)
        self.at("more pronural factor")
        self.play(*A.to(pro=0.85), run_time=0.8)
        self.play(FadeIn(items[(3, "A", 1, 0)], shift=RIGHT * 0.15), run_time=0.4)
        self.finish()


class S14Step3b(SpokenScene):
    def construct(self):
        A, B, items, labs, leg, cap = top_scene(self, 3, 3)
        # step 3 is fully shown; the pair is at the end of step 3, with A's Delta still at its step-1 size
        A.setv(delta=0.72)
        r1 = A.knob_r(0.72)
        ghost = DashedVMobject(Circle(radius=r1, stroke_color=TEXT, stroke_width=3.5), num_dashes=14)
        # step 3 row is the one narrated here: rows above fade to 40 percent
        self.at("more delta")
        ghost.move_to(A.knob_c())
        self.add(ghost)
        self.play(*A.to(delta=0.98), run_time=0.9)
        self.play(FadeIn(items[(3, "A", 1, 1)], shift=RIGHT * 0.15), *table_rows_dim(items, labs, 2, 0.4), run_time=0.4)
        self.at("returning signal pushes")
        # the returning signal pushes A's own Delta up again: an arrow from A's Delta ball back to A's own bar
        ytop = A.BASE + 0.85 * A.H
        p0 = [A.knob_c()[0] - A.knob_r(0.98) - 0.08, ytop + 0.12, 0]
        p1 = [A.bxp + A.BW / 2 + 0.06, ytop + 0.12, 0]
        pa = arr(p0, p1, color=DEL, w=10, tip=0.32)
        n1 = note_chip("same direction as the first lead", DEL)
        self.play(GrowArrow(pa), FadeIn(n1, shift=UP * 0.15), run_time=0.8)
        self.at("ends up bigger")
        q = T("?", 60, GOLD, font=TITLE_FONT).move_to([-2.5, 3.35, 0])
        n2 = note_chip("bigger or smaller?", GOLD)
        self.play(FadeOut(pa), FadeOut(n1), FadeOut(ghost), run_time=0.35)
        self.play(FadeIn(q, scale=0.6), FadeIn(n2, shift=UP * 0.15), run_time=0.6)
        self.play(Indicate(q, color=GOLD, scale_factor=1.15), run_time=0.7)
        self.at("how steep")
        n3 = note_chip("depends on how steep the loop is", GOLD)
        self.play(FadeOut(n2), run_time=0.25)
        self.play(FadeIn(n3, shift=UP * 0.15), run_time=0.4)
        self.at("that comes next")
        n4 = note_chip("direction, not yet size", GOLD)
        self.play(FadeOut(n3), run_time=0.25)
        self.play(FadeIn(n4, shift=UP * 0.15), run_time=0.4)
        self.finish()


# ------------------------------------------------------------------------------------------
class S15Loop(SpokenScene):
    def construct(self):
        A, B, leg = med_scene(self)
        top, bot = loop_arcs()
        self.at("each cell inhibits")
        lt = T("inhibits", 28, REP).move_to([0, 3.3, 0])
        self.play(Create(top), FadeIn(lt, shift=DOWN * 0.1), run_time=0.9)
        self.at("so a inhibits")
        self.play(Indicate(A.body, color=TEXT, scale_factor=1.03), run_time=0.7)
        self.at("the cell that")
        lb = T("inhibits", 28, REP).move_to([0, -2.2, 0])
        self.play(Indicate(B.body, color=TEXT, scale_factor=1.03), run_time=0.6)
        self.at("inhibits a")
        self.play(Create(bot), FadeIn(lb, shift=UP * 0.1), Indicate(A.body, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.finish()


class S16Positive(SpokenScene):
    def construct(self):
        A, B, leg = med_scene(self)
        top, bot = loop_arcs()
        lt = T("inhibits", 28, REP).move_to([0, 3.3, 0])
        lb = T("inhibits", 28, REP).move_to([0, -2.2, 0])
        self.add(top, bot, lt, lb)
        self.at("two inhibitions")
        m1, m2 = minus([0, 2.8, 0]), minus([0, -1.6, 0])
        self.play(FadeOut(lt), FadeOut(lb), FadeIn(m1, scale=0.6), FadeIn(m2, scale=0.6), run_time=0.6)
        self.at("in a row")
        self.play(m1.animate.move_to([-0.55, 0.6, 0]), m2.animate.move_to([0.55, 0.6, 0]), run_time=0.8)
        self.at("positive feedback")
        self.play(m1.animate.move_to([0, 0.6, 0]).set_color(GREEN).set_stroke(width=14).scale(1.5),
                  m2.animate.move_to([0, 0.6, 0]).rotate(PI / 2).set_color(GREEN).set_stroke(width=14).scale(1.5), run_time=0.8)
        pf = T("positive feedback", 34, GREEN).move_to([0, -2.2, 0])
        self.play(FadeIn(pf, shift=UP * 0.15), run_time=0.5)
        self.at("switch making")
        card = VGroup(RoundedRectangle(corner_radius=0.14, width=3.9, height=1.0, stroke_color=TEAL, stroke_width=2.5,
                                       fill_color=TEAL, fill_opacity=0.14),
                      VGroup(T("Link: signaling circuits", 26, TEAL), T("a switch-making loop", 26, GREY)).arrange(DOWN, buff=0.06))
        card[1].move_to(card[0])
        card.move_to([4.7, 3.1, 0])
        self.play(FadeIn(card, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


LEAD17 = 0.80       # the first tiny lead, exaggerated a little so the eye can see it
COINY = 0.6


def coin_face(face, y=COINY, sx=1.0):
    c = VGroup(Circle(radius=0.58, stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.35),
               T(face, 42, GOLD, weight=BOLD))
    c.stretch(max(sx, 0.07), 0)
    return c.move_to([0, y, 0])


def coin_mob(tr, final):
    """A coin that is tossed over the pair, spins and lands showing `final` ("A" or "B")."""
    flips = 5 if final == "A" else 4   # an odd number of half turns ends on A, an even number on B
    def f():
        p = tr.get_value()
        ph = p * flips * PI
        idx = min(int(ph / PI), flips - 1)
        face = "A" if idx % 2 == 0 else "B"
        return coin_face(face, COINY + 1.15 * np.sin(PI * p), abs(np.cos(ph)))
    return always_redraw(f)


def toss(scene, final, run_time=0.9):
    tr = ValueTracker(0)
    coin = coin_mob(tr, final)
    scene.add(coin)
    scene.play(tr.animate.set_value(1), run_time=run_time, rate_func=smooth)
    scene.remove(coin)
    landed = coin_face(final)
    scene.add(landed)
    return landed


class S17Chance(SpokenScene):
    def construct(self):
        A, B, leg = med_scene(self)
        top, bot = loop_arcs()
        self.add(top, bot)
        run = T("run 1", 30, GOLD).move_to([-5.7, 3.2, 0])
        self.at("if the loop is steep")
        lab = chip("steep loop", GOLD, size=26, pad=0.16).move_to([0, 3.35, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), FadeIn(run), top.animate.set_stroke(width=9), bot.animate.set_stroke(width=9), run_time=0.8)
        # run 1: a coin over the pair is tossed and lands on A
        self.at("noise gives")
        landed = toss(self, "A", 0.9)
        note = chip("tiny random lead", GOLD, size=26, pad=0.16).move_to([-3.05, -1.85, 0])
        self.play(*A.to(pro=LEAD17, delta=LEAD17), *B.to(rep=LEAD17, notch=LEAD17), FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.at("magnifies")
        sim = simulate(LEAD17, 0.50, tmax=4.0)
        self.play(FadeOut(note), FadeOut(landed), run_time=0.3)
        run_sim(self, A, B, sim, 1.3)
        win = chip("neural", GREEN, size=26, pad=0.16).move_to([-3.05, -1.85, 0])
        self.play(FadeIn(win), *A.win(), *B.lose(), run_time=0.35)
        # run 2: reset, another toss, this time it lands on B
        run2 = T("another run", 30, GOLD).move_to([-5.7, 3.2, 0])
        self.play(FadeOut(win), Transform(run, run2), *A.neutral(), *B.neutral(), *A.to(pro=0.5, rep=0.5, delta=0.5, notch=0.35),
                  *B.to(pro=0.5, rep=0.5, delta=0.5, notch=0.35), run_time=0.3)
        landed2 = toss(self, "B", 0.75)
        note2 = chip("tiny random lead", GOLD, size=26, pad=0.16).move_to([3.05, -1.85, 0])
        self.play(*A.to(pro=0.5, delta=0.5), *B.to(pro=LEAD17, delta=LEAD17), *A.to(rep=LEAD17, notch=LEAD17), FadeIn(note2, shift=UP * 0.1), run_time=0.4)
        self.play(FadeOut(note2), FadeOut(landed2), run_time=0.2)
        sim2 = simulate(0.50, LEAD17, tmax=3.0)
        run_sim(self, A, B, sim2, 0.9)
        winb = chip("neural", GREEN, size=26, pad=0.16).move_to([3.05, -1.85, 0])
        run3 = T("another run: B wins", 30, GOLD)
        run3.move_to([-6.6 + run3.width / 2, 3.2, 0])
        self.play(*B.win(), *A.lose(), FadeIn(winb), Transform(run, run3), run_time=0.35)
        self.finish()


# ------------------------------------------------------------------------------------------
def s17_end_state(scene):
    A, B, leg = med_scene(scene)
    top, bot = loop_arcs()
    top.set_stroke(width=9)
    bot.set_stroke(width=9)
    a, b = simulate(0.50, LEAD17, tmax=3.0)[-1]
    A.setv(pro=a, rep=b, notch=b, delta=a)
    B.setv(pro=b, rep=a, notch=a, delta=b)
    B.win_now()
    A.lose_now()
    lab = chip("steep loop", GOLD, size=26, pad=0.16).move_to([0, 3.35, 0])
    run3 = T("another run: B wins", 30, GOLD)
    run3.move_to([-6.6 + run3.width / 2, 3.2, 0])
    winb = chip("neural", GREEN, size=26, pad=0.16).move_to([3.05, -1.85, 0])
    scene.add(top, bot, lab, run3, winb)
    return A, B, leg, [top, bot, lab, run3, winb]


class S18Predict(SpokenScene):
    def construct(self):
        A, B, leg, old = s17_end_state(self)
        ban = banner_predict()
        self.play(*[FadeOut(m) for m in old], *A.to(pro=0.5, rep=0.5), *B.to(pro=0.5, rep=0.5), *A.neutral(), *B.neutral(),
                  run_time=0.6)
        self.play(FadeIn(ban, shift=DOWN * 0.15), run_time=0.4)
        self.at("neither cell has")
        self.play(*A.to(cupvis=1, notch=0.6), *B.to(cupvis=1, notch=0.6), run_time=0.7)
        cl = case_label("No Notch in either cell")
        self.at("any notch")
        dashed = cups_dashed(A, B)
        xs = VGroup(*[xmark(c.cup_c(), s=0.16, w=7) for c in (A, B)])
        self.play(*A.to(cupvis=0), *B.to(cupvis=0), FadeIn(dashed), Create(xs), FadeIn(cl, shift=UP * 0.15), run_time=0.7)
        self.at("what happens")
        q = qmark()
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.play(Indicate(q, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.finish()


def pause_state(scene):
    A, B, leg = med_scene(scene)
    dashed = cups_dashed(A, B)
    xs = VGroup(*[xmark(c.cup_c(), s=0.16, w=7) for c in (A, B)])
    ban, cl = banner_predict(), case_label("No Notch in either cell")
    scene.add(dashed, xs, ban, cl)
    return A, B, dict(dashed=dashed, xs=xs, ban=ban, cl=cl)


class S19Pause(NarratedScene):
    def construct(self):
        A, B, S = pause_state(self)
        c0 = qring_centre()
        track = Circle(radius=0.8, stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to(c0).set_stroke(opacity=0.5)
        tr = ValueTracker(0)
        sweep = always_redraw(lambda: Arc(radius=0.8, start_angle=PI / 2, angle=-2 * PI * max(0.001, 1 - tr.get_value()),
                                          arc_center=c0, color=GOLD, stroke_width=9))
        q = qmark()
        self.add(track, sweep, q)
        self.play(tr.animate.set_value(1), run_time=self.narration_s - 0.2, rate_func=linear)
        self.finish()


GLOW = "#8EE3FF"


def glow_rings(cells, tr):
    """A bright disc that breathes behind each always-on crescent, plus a ring that keeps expanding outward."""
    out = []
    for c in cells:
        c.cupcol = GLOW
        c.cup.set_z_index(4)

        def disc(c=c):
            p = tr.get_value()
            pulse = 0.5 + 0.5 * np.sin(2 * PI * 2.5 * p)
            r = c.cupR * (1.3 + 0.22 * pulse)
            v = c.cupvis.get_value()
            return Circle(radius=r, stroke_color=GLOW, stroke_width=6 if v > 0.02 else 0.001, fill_color=GLOW,
                          fill_opacity=(0.3 + 0.15 * pulse) * v).move_to(c.cup_c()).set_stroke(opacity=0.9 * v).set_z_index(3)

        def wave(c=c):
            ph = (tr.get_value() * 2.5) % 1.0
            r = c.cupR * (1.5 + 2.0 * ph)
            v = c.cupvis.get_value()
            return Circle(radius=r, stroke_color=GLOW, stroke_width=(1 + 6 * (1 - ph)) if v > 0.02 else 0.001, fill_opacity=0).move_to(
                c.cup_c()).set_stroke(opacity=0.95 * (1 - ph) * v).set_z_index(3)
        out.append(always_redraw(disc))
        out.append(always_redraw(wave))
    return out


def run_clock(scene, tr, speed=0.8):
    tr.add_updater(lambda m, dt: m.increment_value(dt * speed))
    scene.add(tr)


class S20Reveal(SpokenScene):
    def construct(self):
        A, B, S = pause_state(self)
        q = qmark()
        c0 = qring_centre()
        track = Circle(radius=0.8, stroke_color=GREY, stroke_width=5, fill_opacity=0).move_to(c0).set_stroke(opacity=0.5)
        self.add(q, track)
        self.at("neither cell can be told")
        bub = bubble("not you", [0, 1.3, 0], [-1.0, 1.3, 0], color=NOT, size=26)
        self.play(FadeOut(q), FadeOut(track), FadeOut(S["ban"]), FadeIn(bub, scale=0.7), run_time=0.7)
        self.at("not you")
        cr = xmark([0, 2.15, 0], s=0.3, w=10)
        self.play(Create(cr), bub.animate.set_opacity(0.3), run_time=0.5)
        self.at("keep pronural genes on")
        self.play(FadeOut(bub), FadeOut(cr), *A.to(rep=0.0, pro=1.0), *B.to(rep=0.0, pro=1.0), run_time=1.0)
        self.at("become neural")
        chips = VGroup(*[chip("neural", GREEN, size=26, pad=0.16).move_to([c.cx, -1.68, 0]) for c in (A, B)])
        self.play(*A.win(), *B.win(), FadeIn(chips, shift=UP * 0.15), run_time=0.8)
        self.finish()


def reveal_state(scene):
    A, B, leg = med_scene(scene)
    A.setv(pro=1.0, rep=0.0)
    B.setv(pro=1.0, rep=0.0)
    A.win_now()
    B.win_now()
    dashed = cups_dashed(A, B)
    xs = VGroup(*[xmark(c.cup_c(), s=0.16, w=7) for c in (A, B)])
    chips = VGroup(*[chip("neural", GREEN, size=26, pad=0.16).move_to([c.cx, -1.68, 0]) for c in (A, B)])
    cl = case_label("No Notch in either cell")
    scene.add(dashed, xs, chips, cl)
    return A, B, dict(dashed=dashed, xs=xs, chips=chips, cl=cl)


def neuro_label():
    g = VGroup(T("neurogenic phenotype", 38, TEXT, font=TITLE_FONT), T("in miniature", 28, GREY)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    return g.move_to([0, 2.95, 0])


class S21Reveal2(SpokenScene):
    def construct(self):
        A, B, S = reveal_state(self)
        self.at("too many neural cells")
        top = T("too much neural tissue", 36, TEXT).move_to([0, 2.9, 0])
        self.play(FadeOut(S["cl"]), Indicate(A.body, color=GREEN, scale_factor=1.04),
                  Indicate(B.body, color=GREEN, scale_factor=1.04), run_time=0.5)
        self.play(FadeIn(top, shift=DOWN * 0.15), run_time=0.5)
        self.at("neurogenic phenotype")
        g = neuro_label()
        self.play(FadeOut(top), run_time=0.3)
        self.play(FadeIn(g[0], shift=UP * 0.1), run_time=0.5)
        self.at("in miniature")
        self.play(FadeIn(g[1], shift=UP * 0.1), run_time=0.6)
        self.finish()


class S22Always(SpokenScene):
    def construct(self):
        A, B, S = reveal_state(self)
        g = neuro_label()
        self.remove(S["cl"])
        self.add(g)
        self.at("now the reverse")
        cl = case_label("Notch always on")
        cl.set_color(NOT)
        self.play(FadeOut(g), FadeOut(S["chips"]), FadeOut(S["dashed"]), FadeOut(S["xs"]), *A.neutral(), *B.neutral(),
                  *A.to(pro=0.5, rep=0.5), *B.to(pro=0.5, rep=0.5), run_time=0.6)
        self.play(FadeIn(cl, shift=DOWN * 0.1), run_time=0.4)
        self.at("switch notch on")
        tr = ValueTracker(0)
        rings = glow_rings((A, B), tr)
        self.add(*rings)
        run_clock(self, tr)
        self.play(*A.to(cupvis=1, notch=1.0), *B.to(cupvis=1, notch=1.0), run_time=0.9)
        self.at("whatever delta")
        sub = T("whatever Delta they receive", 28, DEL).move_to([0, -2.35, 0])
        d1 = Circle(radius=0.1, stroke_width=0, fill_color=DEL, fill_opacity=0.92).move_to([-0.55, 1.35, 0])
        d2 = Circle(radius=0.1, stroke_width=0, fill_color=DEL, fill_opacity=0.92).move_to([0.55, 1.35, 0])
        self.add(d1, d2)
        self.play(FadeIn(sub, shift=UP * 0.1), d1.animate.scale(3.0), d2.animate.scale(0.4), run_time=0.8, rate_func=linear)
        self.play(d1.animate.scale(0.15), d2.animate.scale(7.0), run_time=0.8, rate_func=linear)
        self.finish()


def always_state(scene):
    A, B, leg = med_scene(scene)
    A.setv(cupvis=1, notch=1.0)
    B.setv(cupvis=1, notch=1.0)
    cl = case_label("Notch always on")
    cl.set_color(NOT)
    sub = T("whatever Delta they receive", 28, DEL).move_to([0, -2.35, 0])
    tr = ValueTracker(1.2)
    rings = glow_rings((A, B), tr)
    scene.add(cl, sub, *rings)
    run_clock(scene, tr)
    return A, B, dict(cl=cl, sub=sub, rings=rings, tr=tr)


class S23Always2(SpokenScene):
    def construct(self):
        A, B, S = always_state(self)
        self.at("repressor stays high")
        self.play(FadeOut(S["sub"]), *A.to(rep=1.0, pro=0.1), *B.to(rep=1.0, pro=0.1), run_time=1.2)
        self.at("neither becomes neural")
        chips = VGroup(*[chip("not neural", GREY, size=26, pad=0.16).move_to([c.cx, -1.68, 0]) for c in (A, B)])
        self.play(*A.lose(), *B.lose(), FadeIn(chips, shift=UP * 0.15), run_time=0.8)
        self.at("no precursor")
        pre = VGroup(xmark([0, 0, 0], s=0.18, w=8), T("no neural precursor", 30, TEXT)).arrange(RIGHT, buff=0.2).move_to([0, -2.3, 0])
        self.play(FadeIn(pre, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S24Takeaway(SpokenScene):
    def construct(self):
        A, B, leg = med_scene(self)
        top, bot = loop_arcs()
        self.add(top, bot)
        self.at("double negative")
        m1, m2 = minus([0, 2.8, 0]), minus([0, -1.6, 0])
        self.play(FadeIn(m1, scale=0.6), FadeIn(m2, scale=0.6), run_time=0.6)
        self.at("positive feedback")
        ban = T("Two inhibitions make positive feedback", 34, TEXT, font=TITLE_FONT).move_to([0, 3.4, 0])
        self.play(m1.animate.move_to([0, 0.6, 0]).set_color(GREEN).set_stroke(width=14).scale(1.5),
                  m2.animate.move_to([0, 0.6, 0]).rotate(PI / 2).set_color(GREEN).set_stroke(width=14).scale(1.5),
                  FadeIn(ban, shift=DOWN * 0.1), run_time=0.9)
        self.at("small lead")
        self.play(*A.to(pro=LEAD, delta=LEAD), *B.to(rep=LEAD, notch=LEAD), run_time=0.5)
        self.at("can grow")
        sim = simulate(LEAD, 0.50, tmax=3.4)
        run_sim(self, A, B, sim, 1.3)
        self.finish()


class S25End(EndCard):
    LINE = "A double negative acts as positive feedback; a small lead can grow."

    def construct(self):
        l1 = T("A double negative acts as positive feedback;", 38, font=TITLE_FONT)
        l2 = T("a small lead can grow.", 38, font=TITLE_FONT)
        line = VGroup(l1, l2).arrange(DOWN, buff=0.25)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", 22, color=TEAL)
        VGroup(line, sub).arrange(DOWN, buff=0.45)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
