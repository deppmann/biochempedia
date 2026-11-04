"""Ocular dominance, chapter 3: Two Closed Eyes  (Biochemistrypedia chaptered film)  -- fix round

COLOR MAP (one colour per concept, shared by every chapter of the series)
  ORANGE = the right eye (contralateral to the recorded left hemisphere); histogram group 1 end.
           In this chapter eye B, the eye that is closed first, is the orange one.
  BLUE   = the left eye (ipsilateral); histogram group 7 end. Eye A, the eye that stays open.
           Whenever one input wins a contest in this film it is the blue one.
  PURPLE = a cortical cell driven by both eyes (the shared cell); histogram middle groups
  GREEN  = the disuse idea
  PINK   = the competition idea
  GREY   = abnormal or unresponsive cells, the tray they are counted in, outlines, neutral things
  GOLD   = tags and labels ("toy bookkeeping", "1965", the window, the highlighted row)
  RED    = a crossed-out idea or a warning
Histogram bars run orange (group 1) through purple (group 4) to blue (group 7).
Eyes drawn as a face seen from the front: right eye (orange) on the left of the picture.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F2994A"
PURPLE = "#B58CD9"
PINK = "#E86FB0"
DISUSE = GREEN
COMPETE = PINK
LG = "#BCC3CF"   # light grey for small labels (brighter than GREY)


# ------------------------------------------------------------------ eyes
def make_eye(color, scale=1.0, closed=False):
    ell = Ellipse(width=2.0, height=1.1, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.15)
    pup = Circle(radius=0.3, stroke_width=0, fill_color=color, fill_opacity=1)
    glint = Circle(radius=0.08, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pup.get_center() + UR * 0.1)
    lashes = VGroup(*[Line([x, 0, 0], [x * 1.3, -0.3, 0], color=color, stroke_width=4) for x in (-0.75, -0.375, 0, 0.375, 0.75)]).set_opacity(0)
    g = VGroup(ell, pup, glint, lashes).scale(scale)
    if closed:
        g[0].stretch_to_fit_height(g[0].width * 0.07)
        g[1].set_opacity(0)
        g[2].set_opacity(0)
        g[3].set_opacity(1)
    return g


def close_eyes(scene, *eyes, rt=0.8):
    """Stage 1: the lid comes down and the pupil fades completely. Stage 2: only then the lashes are drawn."""
    a = []
    for g in eyes:
        a += [g[0].animate.stretch_to_fit_height(g[0].width * 0.07), g[1].animate.set_opacity(0), g[2].animate.set_opacity(0)]
    scene.play(*a, run_time=rt * 0.65)
    scene.play(*[g[3].animate.set_opacity(1) for g in eyes], run_time=rt * 0.35)


def arrow(a, b, color=TEXT, w=6, tip=0.25):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def P(x, y):
    return np.array([x, y, 0.0])


H_NORMAL = [3, 6, 10, 12, 9, 5, 2]
H_SHIFT = [0.5, 1, 2, 3, 6, 10, 13]
H_BOTH = [3, 5, 7, 8, 7, 5, 3]
H_LOW = [v * 0.45 for v in H_BOTH]      # disuse prediction: the same hump at a low scale (many cells fall into the silent tray)


def gcol(i):
    O, Pu, B = ManimColor(ORANGE), ManimColor(PURPLE), ManimColor(BLUE)
    return interpolate_color(O, Pu, i / 3) if i <= 3 else interpolate_color(Pu, B, (i - 3) / 3)


class Hist:
    """A seven-group histogram. Labels, numbers and boxes all use the same x positions (hx)."""

    def __init__(self, cx=0.0, sp=1.1, base=-2.4, unit=0.37, bw=None, ylab="number of cells", ends=True, ns=26):
        self.cx, self.sp, self.base, self.unit = cx, sp, base, unit
        self.bw = bw or sp - 0.1
        self.hx = [cx + (i - 3) * sp for i in range(7)]
        self.ylab, self.ends, self.ns = ylab, ends, ns

    def frame(self):
        hx, b, pad = self.hx, self.base, self.sp * 0.6
        ax = Line([hx[0] - pad, b, 0], [hx[-1] + pad, b, 0], color=LG, stroke_width=3)
        nums = VGroup(*[T(str(i + 1), self.ns, TEXT).move_to([hx[i], b - 0.4, 0]) for i in range(7)])
        g = VGroup(ax, nums)
        if self.ylab:
            g.add(T(self.ylab, 26, LG).rotate(PI / 2).move_to([hx[0] - pad - 0.4, b + (1.7 if len(self.ylab) > 8 else 0.9), 0]))
        if self.ends:
            g.add(T("right eye", 26, ORANGE).move_to([hx[0], b - 0.9, 0]), T("left eye", 26, BLUE).move_to([hx[6], b - 0.9, 0]))
        return g

    @property
    def endO(self):
        return None

    def bars(self, h):
        out = VGroup()
        for i, v in enumerate(h):
            hh = max(v * self.unit, 0.03)
            out.add(Rectangle(width=self.bw, height=hh, stroke_color=gcol(i), stroke_width=2, fill_color=gcol(i),
                              fill_opacity=0.6).move_to([self.hx[i], self.base + hh / 2, 0]))
        return out

    def eyes(self, closedO=False, closedB=False, scale=0.7, y=3.2):
        return VGroup(make_eye(ORANGE, scale, closedO).move_to([self.hx[0], y, 0]),
                      make_eye(BLUE, scale, closedB).move_to([self.hx[6], y, 0]))

    def bins(self, height=4.9):
        g = VGroup()
        for x in self.hx:
            g.add(Rectangle(width=self.bw + 0.02, height=height, stroke_color=LG, stroke_width=1.5, fill_opacity=0)
                  .set_stroke(opacity=0.5).move_to([x, self.base + height / 2, 0]))
        return g

    def dots(self, counts, r=0.26):
        out = VGroup()
        for gi, n in enumerate(counts):
            for k in range(n):
                out.add(Circle(radius=r, stroke_color=gcol(gi), stroke_width=3, fill_color=gcol(gi), fill_opacity=0.6)
                        .move_to([self.hx[gi], self.base + r + 0.03 + k * (2 * r + 0.06), 0]))
        return out


# ------------------------------------------------------------------ panels
def panel(cx, color, w=5.6, h=6.2, py=-0.3):
    return RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.04).move_to([cx, py, 0])


def bigpanel(color):
    return panel(0, color, 12.4, 6.6, -0.45)


def head(text, color, cx, y=3.35, size=34):
    return T(text, size, color, weight=BOLD).move_to([cx, y, 0])


def mini_disuse(cx):
    e = make_eye(ORANGE, 0.9).move_to([cx - 1.5, 0.3, 0])
    c = Circle(radius=0.85, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to([cx + 1.55, 0.3, 0])
    l = Line([cx - 0.55, 0.3, 0], [cx + 0.7, 0.3, 0], color=ORANGE, stroke_width=4)
    return VGroup(e, c, l)


def mini_comp(cx):
    eo = make_eye(ORANGE, 0.8).move_to([cx - 1.75, 1.3, 0])
    eb = make_eye(BLUE, 0.8).move_to([cx + 1.75, 1.3, 0])
    c = Circle(radius=0.85, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to([cx, -0.9, 0])
    lo = Line([cx - 1.4, 0.95, 0], [cx - 0.6, -0.35, 0], color=ORANGE, stroke_width=7)
    lb = Line([cx + 1.4, 0.95, 0], [cx + 0.6, -0.35, 0], color=BLUE, stroke_width=7)
    return VGroup(eo, eb, c, lo, lb)


# ------------------------------------------------------------------ the duel: two eyes, one shared cell
def sw(share):
    return 2 + 16 * share


class Duel:
    """Two eyes send inputs to one shared cell; line thickness and the fixed-length bar show each eye's share (orange share)."""
    BW = 9.0

    def __init__(self, share=0.5, dy=0.0, bar=True, closedO=False):
        self.dy, self.has_bar = dy, bar
        self.eO = make_eye(ORANGE, 1.4, closedO).move_to(self.q(-4.6, 1.45))
        self.eB = make_eye(BLUE, 1.4).move_to(self.q(4.6, 1.45))
        self.cell = Circle(radius=1.1, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to(self.q(0, -0.2))
        self.lO, self.lB = self.lines(share)
        self.sO, self.sB = self.segs(share) if bar else (VGroup(), VGroup())
        self.lbO = T("right eye", 26, ORANGE).move_to(self.q(-4.6, 0.45))
        self.lbB = T("left eye", 26, BLUE).move_to(self.q(4.6, 0.45))
        self.cl = T("one shared cell", 26, PURPLE).move_to(self.q(0, -1.75))
        self.cap = T("each eye's share of the cell", 26, LG).move_to(self.q(0, -3.2))

    def q(self, x, y):
        return P(x, y + self.dy)

    def lines(self, share):
        lo = Line(self.q(-3.15, 1.2), self.q(-0.92, 0.38), color=ORANGE, stroke_width=sw(share))
        lb = Line(self.q(3.15, 1.2), self.q(0.92, 0.38), color=BLUE, stroke_width=sw(1 - share))
        return lo, lb

    def segs(self, share):
        wO, wB = max(self.BW * share, 0.03), max(self.BW * (1 - share), 0.03)
        so = Rectangle(width=wO, height=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.85).move_to(self.q(-self.BW / 2 + wO / 2, -2.45))
        sb = Rectangle(width=wB, height=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to(self.q(self.BW / 2 - wB / 2, -2.45))
        return so, sb

    def core(self):
        return VGroup(self.eO, self.eB, self.cell, self.lO, self.lB)

    def all(self):
        return VGroup(self.core(), self.sO, self.sB, self.lbO, self.lbB, self.cl, self.cap)

    def to(self, share):
        lo, lb = self.lines(share)
        anims = [Transform(self.lO, lo), Transform(self.lB, lb)]
        if self.has_bar:
            so, sb = self.segs(share)
            anims += [Transform(self.sO, so), Transform(self.sB, sb)]
        return anims


def balance(angle, wO=0.0, wB=0.0, sO=0.4, sB=0.6):
    """A balance scale. Positive angle: the orange (left) side is heavier and sits lower."""
    piv = P(0, 2.45)
    L, th = 1.9, np.radians(angle)
    lend = piv + L * np.array([-np.cos(th), -np.sin(th), 0])
    rend = piv + L * np.array([np.cos(th), np.sin(th), 0])
    parts = [Line(lend, rend, color=TEXT, stroke_width=6), Line(piv, P(0, 2.0), color=LG, stroke_width=5), Dot(piv, radius=0.1, color=TEXT)]
    blocks = []
    for end, col, w, s in ((lend, ORANGE, wO, sO), (rend, BLUE, wB, sB)):
        pc = end + P(0, -1.0)
        parts += [Line(end, pc + P(-0.5, 0), color=LG, stroke_width=2.5), Line(end, pc + P(0.5, 0), color=LG, stroke_width=2.5),
                  Line(pc + P(-0.6, 0), pc + P(0.6, 0), color=TEXT, stroke_width=6)]
        blocks.append(Square(s, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.7 * w)
                      .move_to(pc + P(0, s / 2 + 0.03)).set_stroke(opacity=w))
    return VGroup(*parts, *blocks)


# ------------------------------------------------------------------ the toy table
TC = dict(lab=-6.6, A=-2.4, B=-1.05, dis=1.75, com=5.0)
TROW = [0.45, -0.75, -1.95]
TROWS = [("both eyes open", "10", "10", "100%", "50%"),
         ("one eye closed", "10", "1", "10%", "1÷11 ≈ 9%"),
         ("both eyes closed", "1", "1", "10%", "50%")]
COLC = dict(A=BLUE, B=ORANGE, dis=DISUSE, com=COMPETE)


class Tbl:
    def __init__(self):
        self.title = T("toy bookkeeping: illustrative, not measured", 28, GOLD).move_to([0, 3.55, 0])
        hd = {}
        for key, txt in (("A", "eye A"), ("B", "eye B"), ("dis", "disuse"), ("com", "competition")):
            hd[key] = T(txt, 28, COLC[key], weight=BOLD).move_to([TC[key], 2.45, 0])
        self.hd = hd
        self.units = T("units of useful activity", 26, LG).move_to([(TC["A"] + TC["B"]) / 2, 3.0, 0])
        self.sub = VGroup(VGroup(T("own connections", 26, LG), T("kept", 26, LG)).arrange(DOWN, buff=0.12).move_to([TC["dis"], 1.63, 0]),
                          VGroup(T("share of", 26, LG), T("influence", 26, LG)).arrange(DOWN, buff=0.12).move_to([TC["com"], 1.63, 0]))
        grid = VGroup(Line([-6.7, 1.1, 0], [6.7, 1.1, 0], color=GREY, stroke_width=3),
                      Line([0.1, 2.85, 0], [0.1, -2.55, 0], color=GREY, stroke_width=1.5).set_opacity(0.5),
                      Line([3.4, 2.85, 0], [3.4, -2.55, 0], color=GREY, stroke_width=1.5).set_opacity(0.5),
                      Line([-6.7, -2.55, 0], [6.7, -2.55, 0], color=GREY, stroke_width=2))
        for y in (-0.15, -1.35):
            grid.add(Line([-6.7, y, 0], [6.7, y, 0], color=GREY, stroke_width=1.5).set_opacity(0.4))
        self.grid = grid
        self.static = VGroup(grid, self.units, self.sub, *hd.values())
        self.lab, self.v = [], []
        for r, row in enumerate(TROWS):
            self.lab.append(T(row[0], 26, TEXT).move_to([TC["lab"], TROW[r], 0], aligned_edge=LEFT))
            self.lab[-1].align_to(P(-6.45, 0), LEFT)
            vals = {}
            for key, txt in zip(("A", "B", "dis", "com"), row[1:]):
                vals[key] = M(txt, 28 if len(txt) > 5 else 34, COLC[key]).move_to([TC[key], TROW[r], 0])
            self.v.append(vals)
        self.note = T("bookkeeping shares, not fractions of a cell", 26, LG).move_to([0, -3.1, 0])

    def hl(self, r):
        return Rectangle(width=13.3, height=1.15, stroke_color=GOLD, stroke_width=3, fill_opacity=0).move_to([0, TROW[r], 0])

    def rows(self, n, skip=()):
        g = VGroup()
        for r in range(n):
            g.add(self.lab[r])
            for key in ("A", "B", "dis", "com"):
                if (r, key) not in skip:
                    g.add(self.v[r][key])
        return g


# ------------------------------------------------------------------ the question frame (s13, s14, carried into s15)
def question_parts(closed=True):
    eO = make_eye(ORANGE, 1.7, closed).move_to([-3.9, 1.75, 0])
    eB = make_eye(BLUE, 1.7, closed).move_to([3.9, 1.75, 0])
    head_ = T("Predict", 56, GOLD, font=TITLE_FONT).move_to([0, 3.3, 0])
    c1 = chip("young kittens", GOLD, size=28).move_to([0, 2.2, 0])
    c2 = chip("same weeks", GOLD, size=28).move_to([0, 1.3, 0])
    cd = chip("Disuse expects?", DISUSE, size=34).move_to([-3.4, -0.1, 0])
    cc = chip("Competition expects?", COMPETE, size=34).move_to([3.4, -0.1, 0])
    axes, qs = VGroup(), VGroup()
    for cx in (-3.4, 3.4):
        axes.add(Hist(cx, 0.8, base=-2.95, ylab=None, ends=False).frame())
        qs.add(T("?", 110, GOLD, weight=BOLD).move_to([cx, -1.5, 0]))
    return dict(eO=eO, eB=eB, head=head_, c1=c1, c2=c2, cd=cd, cc=cc, axes=axes, qs=qs)


# ------------------------------------------------------------------ the abnormal tray (s17 to s21)
TRAY_X = 4.85


def tray_box(x=TRAY_X, w=2.7, h=3.0, y=-0.8):
    return Rectangle(width=w, height=h, stroke_color=LG, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0])


def tray_cells(n=5, x=TRAY_X):
    pos = [(-0.55, -1.6), (0.55, -1.6), (-0.55, -0.95), (0.55, -0.95), (-0.55, -0.3), (0.55, -0.3)]
    return VGroup(*[Circle(radius=0.26, stroke_color=LG, stroke_width=3, fill_color=GREY, fill_opacity=0.6).move_to([x + dx, y, 0])
                    for dx, y in pos[:n]])


def tray_label(x=TRAY_X):
    return VGroup(T("abnormal or", 26, TEXT).move_to([x, -2.75, 0]), T("unresponsive", 26, TEXT).move_to([x, -3.15, 0]))


def schem():
    return chip("schematic", GOLD, size=26).move_to([5.3, 3.4, 0])


def legend():
    sw1 = Square(0.3, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.6).move_to([-6.25, 2.2, 0])
    t1 = T("both eyes closed", 26, TEXT).move_to([-6.0, 2.2, 0], aligned_edge=LEFT)
    sw2 = Square(0.3, stroke_color=TEXT, stroke_width=3, fill_opacity=0).move_to([-6.25, 1.65, 0])
    t2 = T("one eye closed", 26, TEXT).move_to([-6.0, 1.65, 0], aligned_edge=LEFT)
    return VGroup(sw1, t1), VGroup(sw2, t2)


def both_state(cx=0.0):
    """The end state of s18: the histogram with both eyes closed, the one-eye-closed outline, the notes."""
    h = Hist(cx)
    d = dict(h=h, frame=h.frame(), bars=h.bars(H_BOTH), eyes=h.eyes(True, True), tag=schem())
    gh = h.bars(H_SHIFT)
    for b in gh:
        b.set_fill(opacity=0).set_stroke(TEXT, width=3, opacity=0.95)
    d["ghost"] = gh
    ytop = h.base + 8 * h.unit + 0.4
    br = VGroup(Line([h.hx[2] - 0.5, ytop, 0], [h.hx[4] + 0.5, ytop, 0], color=TEXT, stroke_width=4),
                Line([h.hx[2] - 0.5, ytop, 0], [h.hx[2] - 0.5, ytop - 0.2, 0], color=TEXT, stroke_width=4),
                Line([h.hx[4] + 0.5, ytop, 0], [h.hx[4] + 0.5, ytop - 0.2, 0], color=TEXT, stroke_width=4))
    mid = VGroup(T("most cells in", 26, TEXT), T("the middle groups", 26, TEXT)).arrange(DOWN, buff=0.06).move_to([cx + 0.1, ytop + 0.65, 0])
    d["note"] = VGroup(br, mid)
    d["leg1"], d["leg2"] = legend()
    return d


# ================================================================== scenes
class S00Title(TitleCard):
    LESSON = "Ocular Dominance and the Critical Period"
    TITLE = "Two Closed Eyes"


class S01(SpokenScene):
    def construct(self):
        h = Hist(0)
        frame, bars, eyes = h.frame(), h.bars(H_NORMAL), h.eyes()
        ret = chip("its retina still works", ORANGE, size=26).move_to([0, 3.2, 0])
        self.add(frame, bars, eyes)
        self.at("closed eye")
        close_eyes(self, eyes[0], rt=0.7)
        self.at("lost the cortex")
        self.play(Transform(bars, h.bars(H_SHIFT)), run_time=1.3)
        self.at("retina still worked")
        self.play(FadeIn(ret, shift=RIGHT * 0.1), run_time=0.5)
        pL, pR = panel(-3.4, DISUSE), panel(3.4, COMPETE)
        hL, hR = head("disuse?", DISUSE, -3.4, size=40), head("competition?", COMPETE, 3.4, size=40)
        mL, mR = mini_disuse(-3.4), mini_comp(3.4)
        self.at("was that disuse")
        self.play(FadeOut(VGroup(frame, bars, eyes, ret)), FadeIn(pL), FadeIn(pR), FadeIn(mL), FadeIn(mR), FadeIn(hL, shift=DOWN * 0.1), run_time=0.6)
        self.at("or competition")
        self.play(FadeIn(hR, shift=DOWN * 0.1), run_time=0.4)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        pL, pR = panel(-3.4, DISUSE), panel(3.4, COMPETE)
        hL, hR = head("disuse?", DISUSE, -3.4, size=40), head("competition?", COMPETE, 3.4, size=40)
        mL, mR = mini_disuse(-3.4), mini_comp(3.4)
        self.add(pL, pR, hL, hR, mL, mR)
        big = bigpanel(DISUSE)
        hD = head("Disuse", DISUSE, 0, size=40)
        eye = make_eye(ORANGE, 2.2).move_to([-3.9, 0.2, 0])
        cell = Circle(radius=2.2, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to([3.9, 0.2, 0])
        self.play(FadeOut(VGroup(pR, hR, mR, mL)), Transform(pL, big), Transform(hL, hD), FadeIn(eye), FadeIn(cell), run_time=0.6)
        self.at("connections that carry")
        line = Line([-1.7, 0.2, 0], [1.7, 0.2, 0], color=ORANGE, stroke_width=14)
        self.play(Create(line), run_time=0.6)
        con = T("connection", 28, LG).move_to([0.05, 1.0, 0])
        self.play(FadeIn(con), run_time=0.3)
        self.at("little signal")
        weak = T("little signal", 32, ORANGE).move_to([0.05, -0.8, 0])
        self.play(FadeIn(weak), run_time=0.2)
        for op, wd in ((0.95, 10), (0.55, 6), (0.25, 3.5)):
            dot = Dot([-1.7, 0.2, 0], radius=0.17, color=ORANGE).set_opacity(op)
            self.add(dot)
            thin = Line([-1.7, 0.2, 0], [1.7, 0.2, 0], color=ORANGE, stroke_width=wd).set_opacity(max(op, 0.45))
            self.play(dot.animate.move_to([1.7, 0.2, 0]), Transform(line, thin), run_time=0.28, rate_func=linear)
            self.remove(dot)
        self.at("wither")
        self.play(line.animate.set_stroke(width=1.5, opacity=0.25), run_time=0.5)
        self.play(Uncreate(line), FadeOut(con), run_time=0.5)
        lab = T("its own use", 34, ORANGE).move_to([-3.9, -1.8, 0])
        self.at("own use")
        self.play(FadeIn(lab, shift=UP * 0.1), Indicate(eye, color=ORANGE, scale_factor=1.08), run_time=0.8)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        big = bigpanel(DISUSE)
        hD = head("Disuse", DISUSE, 0, size=40)
        eye = make_eye(ORANGE, 2.2).move_to([-3.9, 0.2, 0])
        cell = Circle(radius=2.2, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to([3.9, 0.2, 0])
        self.add(big, hD, eye, cell)
        d = Duel(0.5)
        self.play(Transform(big, bigpanel(COMPETE)), Transform(hD, head("Competition", COMPETE, 0, size=40)),
                  Transform(eye, d.eO), Transform(cell, d.cell), FadeIn(d.eB), FadeIn(d.lbO), FadeIn(d.lbB), run_time=0.5)
        self.remove(eye, cell)
        self.add(d.eO, d.cell)
        self.play(Create(d.lO), Create(d.lB), run_time=0.45)
        self.at("compete for influence")
        self.play(Indicate(d.lO, color=ORANGE, scale_factor=1.15), Indicate(d.lB, color=BLUE, scale_factor=1.15), run_time=0.8)
        self.at("shared cell")
        self.play(FadeIn(d.cl, shift=UP * 0.1), Indicate(d.cell, color=PURPLE, scale_factor=1.08), run_time=0.8)
        self.at("one eye's advantage")
        self.play(FadeIn(d.sO), FadeIn(d.sB), FadeIn(d.cap), run_time=0.5)
        self.at("advantage")
        self.play(*d.to(0.22), run_time=1.0)
        self.at("other its")
        self.play(Indicate(d.sO, color=ORANGE, scale_factor=1.08), run_time=0.8)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        d = Duel(0.22)
        self.add(bigpanel(COMPETE), head("Competition", COMPETE, 0, size=40), d.all())
        sc = balance(0)
        self.at("an eye's fate")
        self.play(FadeIn(sc), run_time=0.6)
        lO = T("its use", 26, ORANGE).move_to([-4.6, 2.55, 0])
        lB = T("other eye's use", 26, BLUE).move_to([4.6, 2.55, 0])
        self.at("its use")
        self.play(FadeIn(lO, shift=DOWN * 0.1), Transform(sc, balance(7, 1, 0)), run_time=0.45)
        self.at("other eyes")
        self.play(FadeIn(lB, shift=DOWN * 0.1), Transform(sc, balance(-7, 1, 1)), run_time=0.7)
        self.finish()


def mini_duel(cx):
    eO = make_eye(ORANGE, 0.9).move_to([cx - 1.7, 1.2, 0])
    eB = make_eye(BLUE, 0.9).move_to([cx + 1.7, 1.2, 0])
    cell = Circle(radius=1.1, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to([cx, -1.15, 0])
    lO = Line([cx - 1.35, 0.8, 0], [cx - 0.7, -0.2, 0], color=ORANGE, stroke_width=3).set_opacity(0.55)
    lB = Line([cx + 1.35, 0.8, 0], [cx + 0.7, -0.2, 0], color=BLUE, stroke_width=15)
    tO = T("closed", 28, ORANGE).move_to([cx - 1.7, 2.3, 0])
    tB = T("open", 28, BLUE).move_to([cx + 1.7, 2.3, 0])
    lost = T("the closed eye loses", 30, ORANGE).move_to([cx, -2.85, 0])
    return eO, eB, cell, lO, lB, lost, tO, tB


class S05(SpokenScene):
    def construct(self):
        pL, pR = panel(-3.4, DISUSE, h=6.6, py=-0.45), panel(3.4, COMPETE, h=6.6, py=-0.45)
        hL, hR = head("Disuse", DISUSE, -3.4), head("Competition", COMPETE, 3.4)
        L, R = mini_duel(-3.4), mini_duel(3.4)
        self.add(pL, pR, hL, hR, *L[:3], *R[:3])
        self.at("one closed eye")
        close_eyes(self, L[0], R[0], rt=0.6)
        self.play(FadeIn(L[6]), FadeIn(R[6]), FadeIn(L[7]), FadeIn(R[7]), run_time=0.3)
        self.at("both ideas predict")
        self.play(Create(L[3]), Create(L[4]), Create(R[3]), Create(R[4]), run_time=1.0)
        eq = T("=", 90, TEXT, weight=BOLD).move_to([0, -0.4, 0])
        self.at("same loss")
        self.play(FadeIn(L[5], shift=UP * 0.1), FadeIn(R[5], shift=UP * 0.1), FadeIn(eq, scale=1.3), run_time=0.7)
        self.at("cannot tell them apart")
        self.play(Indicate(eq, color=GOLD, scale_factor=1.3), run_time=1.0)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        eO = make_eye(ORANGE, 2.8).move_to([-3.3, 0.7, 0])
        eB = make_eye(BLUE, 2.8).move_to([3.3, 0.7, 0])
        tO = T("right eye", 30, ORANGE).move_to([-3.3, -1.3, 0])
        tB = T("left eye", 30, BLUE).move_to([3.3, -1.3, 0])
        self.add(eO, eB, tO, tB)
        self.at("part company", lead=0.0)
        close_eyes(self, eO, eB, rt=0.8)
        both = T("both eyes closed", 50, TEXT, font=TITLE_FONT).move_to([0, -2.8, 0])
        self.play(FadeIn(both, shift=UP * 0.1), run_time=0.4)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        t = Tbl()
        eO = make_eye(ORANGE, 2.8, True).move_to([-3.3, 0.7, 0])
        eB = make_eye(BLUE, 2.8, True).move_to([3.3, 0.7, 0])
        self.add(eO, eB)
        self.play(FadeOut(VGroup(eO, eB)), FadeIn(t.static), run_time=0.4)
        self.at("toy bookkeeping")
        self.play(FadeIn(t.title, shift=DOWN * 0.1), run_time=0.6)
        self.at("not measured")
        self.play(Indicate(t.title, color=GOLD, scale_factor=1.05), run_time=0.8)
        self.finish()


SQ = 0.27
SQ_STEP = 0.31


def key_rows():
    """Two key rows that sit in the first two row slots of the table (labels, unit squares inside the A and B cells)."""
    x0 = -3.05
    lA = VGroup(T("open eye", 30, BLUE), T("10 units", 26, BLUE)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    lA.move_to([-6.6, TROW[0], 0], aligned_edge=LEFT)
    lA.align_to(P(-6.45, 0), LEFT)
    lB = VGroup(T("sutured eye", 30, ORANGE), T("1 unit", 26, ORANGE)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    lB.move_to([-6.6, TROW[1], 0], aligned_edge=LEFT)
    lB.align_to(P(-6.45, 0), LEFT)
    sA = VGroup(*[Square(SQ, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.65).move_to([x0 + SQ_STEP * i, TROW[0], 0]) for i in range(10)])
    sB = VGroup(Square(SQ, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.65).move_to([x0, TROW[1], 0]))
    return lA, sA, lB, sB


class S08(SpokenScene):
    def construct(self):
        t = Tbl()
        self.add(t.static, t.title)
        lA, sA, lB, sB = key_rows()
        self.at("open")
        self.play(FadeIn(lA[0]), run_time=0.2)
        self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.3) for s_ in sA], lag_ratio=0.1), run_time=0.9)
        self.play(FadeIn(lA[1]), run_time=0.25)
        self.at("useful activity")
        self.play(Indicate(t.units, color=GOLD, scale_factor=1.1), run_time=0.7)
        self.at("sutured")
        self.play(FadeIn(lB[0]), FadeIn(sB, shift=DOWN * 0.3), run_time=0.6)
        self.at("1 unit")
        self.play(FadeIn(lB[1]), run_time=0.4)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        t = Tbl()
        lA, sA, lB, sB = key_rows()
        self.add(t.static, t.title, lA, sA, lB, sB)
        hl = t.hl(0)
        self.at("both eyes open", lead=0.0)
        self.play(FadeIn(hl), FadeOut(lA), FadeOut(lB), FadeOut(sB), FadeIn(t.lab[0]),
                  TransformFromCopy(sA, t.v[0]["A"]), TransformFromCopy(sA, t.v[0]["B"]), run_time=0.8)
        self.remove(sA)
        self.at("keeps all of")
        self.play(Indicate(t.hd["dis"], color=DISUSE, scale_factor=1.2), FadeIn(t.v[0]["dis"], scale=1.2), run_time=0.8)
        self.at("Competition gives")
        self.play(Indicate(t.hd["com"], color=COMPETE, scale_factor=1.2), run_time=0.8)
        self.at("half the influence")
        self.play(FadeIn(t.v[0]["com"], scale=1.2), run_time=0.6)
        self.play(FadeIn(t.note, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        t = Tbl()
        hl = t.hl(0)
        self.add(t.static, t.title, t.rows(1), t.note, hl)
        self.play(Transform(hl, t.hl(1)), FadeIn(t.lab[1]), FadeIn(t.v[1]["A"]), FadeIn(t.v[1]["B"]), FadeOut(t.note), run_time=0.8)
        self.at("Under disuse")
        self.play(Indicate(t.hd["dis"], color=DISUSE, scale_factor=1.2), run_time=0.8)
        self.at("a tenth")
        self.play(FadeIn(t.v[1]["dis"], scale=1.2), run_time=0.6)
        self.at("Under competition")
        self.play(Indicate(t.hd["com"], color=COMPETE, scale_factor=1.2), run_time=0.8)
        self.at("shrinks to")
        self.play(FadeIn(t.v[1]["com"], scale=1.2), run_time=0.7)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        t = Tbl()
        hl = t.hl(1)
        self.add(t.static, t.title, t.rows(2), hl)
        self.play(Transform(hl, t.hl(2)), FadeIn(t.lab[2]), FadeIn(t.v[2]["A"]), FadeIn(t.v[2]["B"]), run_time=0.8)
        self.at("Under disuse")
        self.play(Indicate(t.hd["dis"], color=DISUSE, scale_factor=1.2), run_time=0.8)
        self.at("each eye is")
        self.play(FadeIn(t.v[2]["dis"], scale=1.2), run_time=0.6)
        self.at("single closed eye")
        self.play(Indicate(t.v[1]["dis"], color=GOLD, scale_factor=1.4), Indicate(t.v[2]["dis"], color=GOLD, scale_factor=1.4), run_time=1.0)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        t = Tbl()
        self.add(t.static, t.title, t.rows(3, skip=[(2, "com")]), t.hl(2))
        self.play(Indicate(t.hd["com"], color=COMPETE, scale_factor=1.2), run_time=0.8)
        eq = T("=", 48, TEXT, weight=BOLD).move_to([(TC["A"] + TC["B"]) / 2, TROW[2], 0])
        self.at("neither eye")
        self.play(FadeIn(eq, scale=1.4), run_time=0.5)
        q = T("?", 60, GOLD, weight=BOLD).move_to([TC["com"], TROW[2], 0])
        self.at("advantage")
        self.play(FadeIn(q, scale=1.4), run_time=0.5)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        t = Tbl()
        old = VGroup(t.static, t.title, t.rows(3, skip=[(2, "com")]), t.hl(2),
                     T("=", 48, TEXT, weight=BOLD).move_to([(TC["A"] + TC["B"]) / 2, TROW[2], 0]),
                     T("?", 60, GOLD, weight=BOLD).move_to([TC["com"], TROW[2], 0]))
        d = question_parts(closed=False)
        self.add(old)
        self.play(FadeOut(old), FadeIn(d["head"]), FadeIn(d["eO"]), FadeIn(d["eB"]), FadeIn(d["axes"]), run_time=0.5)
        self.at("Close both eyes")
        close_eyes(self, d["eO"], d["eB"], rt=0.7)
        self.at("young kittens")
        self.play(FadeIn(d["c1"], shift=UP * 0.1), run_time=0.4)
        self.at("same weeks")
        self.play(FadeIn(d["c2"], shift=UP * 0.1), run_time=0.4)
        self.at("What does")
        self.play(FadeIn(d["cd"], shift=UP * 0.1), FadeIn(d["cc"], shift=UP * 0.1), run_time=0.6)
        self.at("histogram")
        self.play(FadeIn(d["qs"], scale=1.3), run_time=0.8)
        self.finish()


class S14Pause(NarratedScene):
    def construct(self):
        d = question_parts()
        self.add(*d.values())
        yp = chip("your prediction", GOLD, size=30).move_to([0, -1.5, 0])
        self.wait(0.3)
        self.play(FadeIn(yp, shift=UP * 0.1), run_time=0.5)
        self.play(Indicate(d["qs"][0], color=GOLD, scale_factor=1.15), Indicate(d["qs"][1], color=GOLD, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---- s15 / s21: a small histogram card
def card_hist(cx, base, unit, ylab=True, ends=True):
    return Hist(cx, 0.62, base=base, unit=unit, bw=0.5, ylab="cells" if ylab else None, ends=ends)


def silent_tray(x, base, n=8, w=1.3, h=2.5):
    box = Rectangle(width=w, height=h, stroke_color=LG, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([x, base + h / 2, 0])
    cells = VGroup(*[Circle(radius=0.2, stroke_color=LG, stroke_width=3, fill_color=GREY, fill_opacity=0.6)
                     .move_to([x + (-0.3 if k % 2 == 0 else 0.3), base + 0.35 + (k // 2) * 0.55, 0]) for k in range(n)])
    return box, cells


class S15(SpokenScene):
    def construct(self):
        d = question_parts()
        self.add(*d.values())
        BAS, U = 0.15, 0.27
        hL, hR = card_hist(-3.9, BAS, U), card_hist(3.45, BAS, U)
        chL = chip("disuse: 10% each", DISUSE, size=28).move_to([-3.4, 3.6, 0])
        chR = chip("competition: 50% each", COMPETE, size=28).move_to([3.4, 3.6, 0])
        divider = Line([0.0, 3.8, 0], [0.0, -3.5, 0], color=GREY, stroke_width=1.5).set_opacity(0.4)
        titL, titR = T("eye balance", 28, TEXT).move_to([-3.9, 2.7, 0]), T("eye balance", 28, TEXT).move_to([3.45, 2.7, 0])
        axtL = T("preference group", 26, LG).move_to([-3.9, -1.2, 0])
        axtR = T("preference group", 26, LG).move_to([3.45, -1.2, 0])
        rsL = T("response strength", 26, LG).move_to([-3.9, -2.12, 0])
        rsR = T("response strength", 26, LG).move_to([3.45, -2.12, 0])
        outL = Rectangle(width=4.2, height=0.5, stroke_color=LG, stroke_width=3).move_to([-3.9, -2.65, 0])
        outR = Rectangle(width=4.2, height=0.5, stroke_color=LG, stroke_width=3).move_to([3.45, -2.65, 0])
        self.play(FadeOut(VGroup(*d.values())), FadeIn(divider), FadeIn(chL), FadeIn(hL.frame()), FadeIn(titL), FadeIn(axtL),
                  FadeIn(rsL), FadeIn(outL), run_time=0.7)
        fillL = Rectangle(width=0.9, height=0.5, stroke_width=0, fill_color=DISUSE, fill_opacity=0.85).move_to([-3.9 - 2.1 + 0.45, -2.65, 0])
        self.at("weak responses")
        self.play(GrowFromEdge(fillL, LEFT), FadeIn(T("weak", 30, DISUSE).move_to([-3.9, -3.3, 0])), run_time=0.7)
        barsL = hL.bars(H_LOW)
        self.at("both eyes")
        self.play(FadeIn(barsL, shift=UP * 0.2), run_time=0.7)
        box, cells = silent_tray(-0.9, BAS)
        trayT = T("silent", 26, TEXT).move_to([-0.9, BAS + 2.75, 0])
        self.at("many silent")
        self.play(FadeIn(box), FadeIn(trayT), LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cells], lag_ratio=0.12), run_time=1.0)
        barsR = hR.bars(H_BOTH)
        fillR = Rectangle(width=3.6, height=0.5, stroke_width=0, fill_color=COMPETE, fill_opacity=0.85).move_to([3.45 - 2.1 + 1.8, -2.65, 0])
        self.at("Competition expects")
        self.play(FadeIn(chR), FadeIn(hR.frame()), FadeIn(titR), FadeIn(axtR), FadeIn(rsR), FadeIn(outR), FadeIn(barsR, shift=UP * 0.2),
                  GrowFromEdge(fillR, LEFT), FadeIn(T("normal", 30, COMPETE).move_to([3.45, -3.3, 0])), run_time=0.8)
        self.at("balance to hold")
        self.play(Indicate(barsR, color=COMPETE, scale_factor=1.04), run_time=0.8)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        name = T("Wiesel and Hubel", 60, TEXT, font=TITLE_FONT).move_to([0, 2.5, 0])
        eO = make_eye(ORANGE, 2.2, True).move_to([-3.2, -0.05, 0])
        eB = make_eye(BLUE, 2.2, True).move_to([3.2, -0.05, 0])
        yr = T("1965", 66, GOLD, font=TITLE_FONT).move_to([0, -2.6, 0])
        rule = Line([-1.4, 1.75, 0], [1.4, 1.75, 0], color=GOLD, stroke_width=3)
        self.add(name, eO, eB)
        self.play(FadeIn(rule), run_time=0.4)
        self.at("1965")
        self.play(FadeIn(yr, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        h = Hist(0)
        frame, bx, eyes = h.frame(), h.bins(), h.eyes(True, True)
        tag = schem()
        self.add(frame, bx, eyes, tag)
        dots = h.dots([1, 2, 3, 3, 3, 2, 1])
        self.at("scored many cells")
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 1.8) for d in dots], lag_ratio=0.1), run_time=1.8)
        self.at("seven group scale")
        self.play(Indicate(frame[1], color=TEXT, scale_factor=1.15), run_time=0.8)
        box, lab = tray_box(), tray_label()
        grp = VGroup(frame, bx, eyes, dots)
        self.at("also counted")
        self.play(grp.animate.shift(LEFT * 1.5), FadeIn(box), FadeIn(lab), run_time=0.8)
        tr = tray_cells(5)
        self.at("abnormally")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 1.5) for c in tr[:3]], lag_ratio=0.25), run_time=1.0)
        self.at("not at all")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 1.5) for c in tr[3:]], lag_ratio=0.25), run_time=0.8)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        h = Hist(-1.5)
        frame, bx, eyes = h.frame(), h.bins(), h.eyes(True, True)
        dots = h.dots([1, 2, 3, 3, 3, 2, 1])
        box, lab, tr = tray_box(), tray_label(), tray_cells(5)
        tag = schem()
        self.add(frame, bx, eyes, dots, box, lab, tr, tag)
        zero = h.bars([0] * 7)
        self.add(zero)
        d = both_state(0.0)
        tgt = h.bars(H_BOTH)
        self.play(Transform(zero, tgt), FadeOut(dots), FadeOut(bx), FadeOut(VGroup(box, lab, tr)), run_time=1.0)
        grp = VGroup(frame, zero, eyes)
        self.play(grp.animate.shift(RIGHT * 1.5), run_time=0.6)
        self.at("each eye")
        self.play(Indicate(zero[0], color=ORANGE, scale_factor=1.08), Indicate(zero[6], color=BLUE, scale_factor=1.08), run_time=0.9)
        self.at("balance moved")
        self.play(FadeIn(d["note"]), FadeIn(d["leg1"]), run_time=0.6)
        self.at("one eye closure")
        self.play(FadeIn(d["ghost"]), FadeIn(d["leg2"]), run_time=0.9)
        self.finish()


class S19Beat(NarratedScene):
    def construct(self):
        d = both_state(0.0)
        self.add(d["frame"], d["bars"], d["eyes"], d["tag"], d["ghost"], d["note"], d["leg1"], d["leg2"])
        self.finish()


class S20(SpokenScene):
    def construct(self):
        d = both_state(0.0)
        self.add(d["frame"], d["bars"], d["eyes"], d["tag"], d["ghost"], d["note"], d["leg1"], d["leg2"])
        box, lab, tr = tray_box(), tray_label(), tray_cells(5)
        hdr = T("a share of cells", 30, TEXT).move_to([TRAY_X, 1.05, 0])
        grp = VGroup(d["frame"], d["bars"], d["eyes"])
        self.play(FadeOut(VGroup(d["ghost"], d["note"], d["leg1"], d["leg2"], d["tag"])),
                  VGroup(d["frame"], d["bars"]).animate.shift(LEFT * 1.5).set_opacity(0.35), d["eyes"].animate.shift(LEFT * 1.5), FadeIn(box), FadeIn(lab), FadeIn(tr), run_time=0.8)
        self.at("respond abnormally")
        self.play(FadeIn(hdr), box.animate.set_stroke(GOLD, width=6), Indicate(tr, color=TEXT, scale_factor=1.12), run_time=1.0)
        warn = VGroup(T("going without vision", 30, RED), T("is not harmless", 30, RED)).arrange(DOWN, buff=0.1)
        wbox = RoundedRectangle(corner_radius=0.14, width=warn.width + 0.5, height=warn.height + 0.4, stroke_color=RED, stroke_width=2.5,
                                fill_color=RED, fill_opacity=0.14)
        chp = VGroup(wbox, warn.move_to(wbox)).move_to([TRAY_X - 0.1, 2.25, 0])
        self.at("going without vision")
        self.play(FadeIn(chp, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        BAS, U = -1.3, 0.5
        hR = card_hist(2.5, BAS, U, ylab=False)
        hL = card_hist(-4.1, BAS, U)
        tR = T("what they found (schematic)", 28, TEXT).move_to([3.3, 3.3, 0])
        barsR = hR.bars(H_BOTH)
        boxR, cellsR = tray_box(5.85, 1.7, 2.7, BAS + 1.35), tray_cells(5, 5.85)
        for c, (px, py) in zip(cellsR, [(-0.35, 0.35), (0.35, 0.35), (-0.35, 0.95), (0.35, 0.95), (-0.35, 1.55)]):
            c.move_to([5.85 + px, BAS + py, 0]).scale(0.8)
        labR = VGroup(T("abnormal or", 26, TEXT), T("unresponsive", 26, TEXT)).arrange(DOWN, buff=0.04).move_to([5.85, BAS + 3.25, 0])
        self.add(Line([-0.2, 3.0, 0], [-0.2, -3.0, 0], color=LG, stroke_width=4).set_opacity(0.8), hR.frame(), barsR, tR, boxR, cellsR, labR)
        tL = T("disuse predicts", 28, DISUSE).move_to([-3.7, 3.3, 0])
        barsL = hL.bars(H_LOW)
        boxL, cellsL = silent_tray(-1.2, BAS, 8, 1.3, 2.7)
        labL = T("silent", 26, TEXT).move_to([-1.2, BAS + 3.1, 0])
        for c in cellsL:
            c.scale(0.85)
        self.at("large loss")
        self.play(FadeIn(hL.frame()), FadeIn(barsL), FadeIn(tL), FadeIn(boxL), FadeIn(cellsL), FadeIn(labL), run_time=0.6)
        cross = VGroup(Line([-6.4, 2.7, 0], [-0.6, -2.0, 0], color=RED, stroke_width=12),
                       Line([-6.4, -2.0, 0], [-0.6, 2.7, 0], color=RED, stroke_width=12))
        self.at("absent")
        self.play(Create(cross), run_time=0.7)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        d = Duel(0.5)
        self.add(bigpanel(COMPETE), head("Competition", COMPETE, 0, size=40), d.all())
        self.at("single closed")
        close_eyes(self, d.eO, rt=0.6)
        self.play(Transform(d.lbO, T("right eye (closed)", 26, ORANGE).move_to(d.q(-4.6, 0.45))), run_time=0.3)
        self.at("its cells")
        self.play(*d.to(0.1), run_time=1.0)
        cause = chip("the open eye's advantage", BLUE, size=28).move_to([3.6, -0.75, 0])
        car = arrow(P(3.1, -0.35), P(2.4, 0.7), BLUE, 6, 0.3)
        self.at("mainly the open")
        self.play(FadeIn(cause, shift=DOWN * 0.1), GrowArrow(car), Indicate(d.lB, color=BLUE, scale_factor=1.15), run_time=0.8)
        self.finish()


class S23(SpokenScene):
    def construct(self):
        d = Duel(0.5, dy=-2.0, bar=False)
        rl = T("THE RULE, PART 1", 30, GOLD, weight=BOLD).move_to([0, 3.4, 0])
        l1 = T("The two eyes compete", 56, TEXT, font=TITLE_FONT).move_to([0, 2.45, 0])
        l2 = T("for the cells they share.", 56, TEXT, font=TITLE_FONT).move_to([0, 1.4, 0])
        self.add(d.core(), d.lbO, d.lbB)
        self.at("first part")
        self.play(FadeIn(rl, shift=DOWN * 0.1), run_time=0.5)
        self.at("two eyes compete")
        self.play(FadeIn(l1, shift=UP * 0.1), Indicate(d.lO, color=ORANGE, scale_factor=1.2), Indicate(d.lB, color=BLUE, scale_factor=1.2), run_time=0.9)
        self.at("cells they share")
        self.play(FadeIn(l2, shift=UP * 0.1), Indicate(d.cell, color=PURPLE, scale_factor=1.12), run_time=0.9)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        t = Tbl()
        grp = VGroup(t.static, t.title, t.rows(3))
        self.add(grp)
        lab = T("bookkeeping only", 52, GOLD, font=TITLE_FONT).move_to([0, -3.25, 0])
        self.at("only bookkeeping")
        self.play(grp.animate.set_opacity(0.3), FadeIn(lab, scale=0.9), run_time=0.8)
        self.finish()


def pct(share, d):
    tO = T(f"{round(share * 100)}%", 28, BG, weight=BOLD).move_to(d.q(-Duel.BW / 2 + Duel.BW * share / 2, -2.45))
    tB = T(f"{round((1 - share) * 100)}%", 28, BG, weight=BOLD).move_to(d.q(Duel.BW / 2 - Duel.BW * (1 - share) / 2, -2.45))
    return tO, tB


class S25(SpokenScene):
    def construct(self):
        d = Duel(0.5)
        self.add(bigpanel(COMPETE), head("Competition", COMPETE, 0, size=40), d.all())
        tO, tB = pct(0.5, d)
        self.add(tO, tB)
        loop = CurvedArrow(P(2.75, 1.05), P(1.75, 0.68), angle=-TAU * 0.78, color=GOLD, stroke_width=7)
        fb = T("feedback", 32, GOLD).move_to([4.7, -0.8, 0])
        self.at("feedback")
        self.play(Create(loop), FadeIn(fb, shift=DOWN * 0.1), run_time=0.8)
        self.at("gets ahead")
        nO, nB = pct(0.45, d)
        self.play(*d.to(0.45), Transform(tO, nO), Transform(tB, nB), Indicate(loop, color=GOLD, scale_factor=1.05), run_time=0.6)
        self.at("strengthened")
        nO, nB = pct(0.35, d)
        self.play(*d.to(0.35), Transform(tO, nO), Transform(tB, nB), Indicate(loop, color=GOLD, scale_factor=1.05), run_time=0.45)
        self.at("further")
        nO, nB = pct(0.2, d)
        self.play(*d.to(0.2), Transform(tO, nO), Transform(tB, nB), Indicate(loop, color=GOLD, scale_factor=1.05), run_time=0.6)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        h = Hist(0)
        frame, bars, eyes = h.frame(), h.bars(H_NORMAL), h.eyes()
        win = chip("young: inside the window", GOLD, size=26).move_to([0, 3.2, 0])
        self.add(frame, bars, eyes, win)
        self.at("strong imbalance")
        close_eyes(self, eyes[0], rt=0.7)
        self.play(Transform(frame[3], T("right eye (closed)", 26, ORANGE).move_to([h.hx[0], h.base - 0.9, 0])),
                  Transform(frame[4], T("left eye (open)", 26, BLUE).move_to([h.hx[6], h.base - 0.9, 0])), run_time=0.3)
        self.at("move most cells")
        self.play(Transform(bars, h.bars(H_SHIFT)), run_time=0.9)
        most = chip("most cells", BLUE, size=30).move_to([-0.9, 0.9, 0])
        ar = arrow(P(0.1, 0.75), P(0.75, 0.2), BLUE, 6, 0.3)
        self.play(FadeIn(most), GrowArrow(ar), run_time=0.5)
        fx = chip("a fixed fraction", RED, size=30).move_to([-3.2, 1.9, 0])
        xx = Line(fx.get_left() + RIGHT * 0.1, fx.get_right() - RIGHT * 0.1, color=RED, stroke_width=6)
        self.at("not a fixed fraction")
        self.play(FadeIn(fx, shift=DOWN * 0.1), run_time=0.4)
        self.play(Create(xx), run_time=0.5)
        self.finish()


def gradient_bar(x0, x1, y, thick=0.6, n=40, op=0.65):
    g = VGroup()
    w = (x1 - x0) / n
    for i in range(n):
        t = i / (n - 1)
        col = interpolate_color(ManimColor(ORANGE), ManimColor(PURPLE), t * 2) if t < 0.5 else interpolate_color(ManimColor(PURPLE), ManimColor(BLUE), (t - 0.5) * 2)
        g.add(Rectangle(width=w + 0.01, height=thick, stroke_width=0, fill_color=col, fill_opacity=op).move_to([x0 + w * (i + 0.5), y, 0]))
    return g


class S27(SpokenScene):
    def construct(self):
        AY = 0.3
        eO = make_eye(ORANGE, 1.4).move_to([-4.8, 3.15, 0])
        eB = make_eye(BLUE, 1.4).move_to([4.8, 3.15, 0])
        bar = gradient_bar(-5.5, 5.5, AY, thick=1.8)
        tO = T("right eye", 32, ORANGE).move_to([-4.8, AY - 1.35, 0])
        tB = T("left eye", 32, BLUE).move_to([4.8, AY - 1.35, 0])
        cap = T("balance between the eyes", 36, TEXT).move_to([0, -3.3, 0])
        mk = Dot([0.0, AY, 0], radius=0.4, color=GOLD)
        mkl = T("balance now", 32, GOLD).move_to([0.0, AY - 1.35, 0])
        self.add(eO, eB, bar, tO, tB, cap, mk, mkl)
        ar = arrow([0.55, AY, 0], [2.2, AY, 0], TEXT, 16, 0.55)
        dl = T("direction of change", 40, TEXT).move_to([-1.5, AY + 1.55, 0])
        self.at("direction of change")
        self.play(GrowArrow(ar), FadeIn(dl, shift=DOWN * 0.1), run_time=1.0)
        dash = DashedLine([2.35, AY, 0], [3.2, AY, 0], color=TEXT, stroke_width=7)
        circ = VGroup(Circle(radius=0.8, stroke_width=0, fill_color=BG, fill_opacity=1),
                      DashedVMobject(Circle(radius=0.8, color=TEXT, stroke_width=7))).move_to([4.05, AY, 0])
        q = T("?", 80, TEXT, weight=BOLD).move_to([4.05, AY, 0])
        nl = T("not given by the rule", 34, TEXT).move_to([4.05, AY + 1.55, 0])
        self.at("does not say", lead=0.4)
        self.play(Create(dash), Create(circ), FadeIn(q), FadeIn(nl, shift=DOWN * 0.1), run_time=0.9)
        self.at("finally settles")
        self.play(Indicate(circ, color=GOLD, scale_factor=1.12), run_time=0.8)
        self.finish()


class S28(SpokenScene):
    def construct(self):
        BAS, U = -1.9, 0.36
        hL = Hist(-3.4, 0.75, base=BAS, unit=U, bw=0.66, ns=26)
        hR = Hist(3.4, 0.75, base=BAS, unit=U, bw=0.66, ns=26, ylab=None)
        tk = T("TAKEAWAY", 28, GOLD, weight=BOLD).move_to([0, 3.65, 0])
        sch = chip("schematic", GOLD, size=26).move_to([5.6, 3.65, 0])
        lL = T("both eyes closed", 30, TEXT).move_to([-3.4, 3.15, 0])
        frL, bL = hL.frame(), hL.bars(H_BOTH)
        frR, bR = hR.frame(), hR.bars(H_SHIFT)
        self.add(tk, sch, frL, lL)
        self.play(FadeIn(bL, shift=UP * 0.15), run_time=0.8)
        lR = T("one eye closed", 30, TEXT).move_to([2.75, 3.15, 0])
        self.at("far less")
        self.play(FadeIn(frR), FadeIn(bR), FadeIn(lR), run_time=0.8)
        self.at("So what hurt")
        self.play(Indicate(lR, color=GOLD, scale_factor=1.08), run_time=0.7)
        cause = VGroup(T("the open eye's", 28, BLUE), T("advantage", 28, BLUE)).arrange(DOWN, buff=0.05)
        cbox = RoundedRectangle(corner_radius=0.14, width=cause.width + 0.5, height=cause.height + 0.4, stroke_color=BLUE, stroke_width=2.5,
                                fill_color=BLUE, fill_opacity=0.16)
        cz = VGroup(cbox, cause.move_to(cbox)).move_to([1.75, 1.3, 0])
        ar = arrow(P(3.15, 1.4), P(4.5, 1.95), BLUE, 6, 0.3)
        self.at("mainly the open")
        self.play(FadeIn(cz, shift=UP * 0.1), GrowArrow(ar), bR[5].animate.set_stroke(TEXT, width=5), bR[6].animate.set_stroke(TEXT, width=5), run_time=0.8)
        fin = Text("competition, not disuse alone", font=TITLE_FONT, font_size=44, color=TEXT,
                   t2c={"competition": COMPETE, "disuse": DISUSE}).move_to([0, -3.4, 0])
        self.at("open eye's")
        self.play(FadeIn(fin, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        base = -2.2
        bO = Rectangle(width=2.2, height=4.2, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.6).move_to([-2.8, base + 2.1, 0])
        bB = Rectangle(width=2.2, height=4.2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.6).move_to([2.8, base + 2.1, 0])
        ax = Line([-4.8, base, 0], [4.8, base, 0], color=LG, stroke_width=3)
        eO = make_eye(ORANGE, 0.9).move_to([-2.8, -3.0, 0])
        eB = make_eye(BLUE, 0.9).move_to([2.8, -3.0, 0])
        cap = T("amount of activity", 38, TEXT).move_to([0, 3.4, 0])
        self.add(ax, eO, eB, cap)
        self.play(GrowFromEdge(bO, DOWN), GrowFromEdge(bB, DOWN), run_time=0.7)
        q = T("?", 140, GOLD, weight=BOLD).move_to([0, -0.1, 0])
        self.at("all that counts")
        self.play(FadeIn(q, scale=1.4), run_time=0.6)
        self.at("next chapter")
        self.play(Indicate(q, color=GOLD, scale_factor=1.15), run_time=0.7)
        eq = T("equal", 38, TEXT).move_to([0, 2.55, 0])
        self.at("keeps the amounts equal")
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


class S30End(EndCard):
    LINE = "What hurt one closed eye was mainly the open eye's advantage."
