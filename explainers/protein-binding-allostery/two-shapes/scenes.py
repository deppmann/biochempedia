"""Two Shapes Make the S  (Biochemistrypedia: Protein binding & allostery, chapter 3)

COLOR MAP (one color per concept, whole series; same as chapter 1 / scenes.old.py)
  BLUE   = hemoglobin, and the T (tense, weak-grip) shape
  GREEN  = the R (relaxed, tight-grip) shape
  YELLOW = O2, and how full the sites are (the real, mixed hemoglobin curve is yellow)
  GOLD   = call-outs, salt-bridge links, cooperativity, Hill slope
  PURPLE = myoglobin (MB);  HEME = the heme discs (the four sites)
  TEXT   = neutral labels;  GREY = axes, secondary labels
Curves are computed, never sketched. The two-state (MWC) model of the lesson's "illustrative fit":
  K_R = 0.37 torr, K_T = 110 torr, L = 1.7e7 (T:R with no oxygen), four sites.
  f_R = (1+x/K_R)^4 / ((1+x/K_R)^4 + L (1+x/K_T)^4);  Y = f_R Y_R + (1-f_R) Y_T,  Y_i = x/(x+K_i).
Single-site curves are x/(K+x); the steep carrier is the Hill curve x^n/(P50^n+x^n).
NO molecular structures are drawn: blocks, chips, cups, bars and curves only.
"""
import numpy as np

from bp_style import *

MB = "#B48EDE"
HEME = "#E8935A"

KR, KT, L0 = 0.37, 110.0, 1.7e7
XMAX = 150


def hill(x, p50, n):
    return x ** n / (p50 ** n + x ** n)


def mwc(x, kr=KR, kt=KT, l0=L0):
    """(fraction of molecules in R, fullness of an R site, of a T site, fullness of the mix)."""
    a, b = 1 + x / kr, 1 + x / kt
    r, t = a ** 4, l0 * b ** 4
    fr = r / (r + t)
    yr, yt = (x / kr) / a, (x / kt) / b
    return fr, yr, yt, fr * yr + (1 - fr) * yt


def mix(x):
    return mwc(x)[3]




# ------------------------------------------------------------------ axes and curves
AX_CX, AX_CY, AX_W, AX_H = 0.5, -0.55, 10.4, 4.8
BAR_Y3 = 2.85     # the population bar above the axes in the curve scenes


def mk_axes(w=AX_W, h=AX_H, cx=AX_CX, cy=AX_CY, xmax=XMAX, ticks=(50, 100, 150),
            xlab="oxygen pressure pO₂ (torr)", ylab="fraction of sites full", yticks=((0.5, "0.5"), (1, "1")), ybuff=1.0):
    ax = Axes(x_range=[0, xmax, xmax], y_range=[0, 1, 1], x_length=w, y_length=h, tips=False,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 3})
    ax.move_to([cx, cy, 0])
    deco = VGroup()
    for v in ticks:
        deco.add(M(str(v), 26, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.14))
    for v, lab in yticks:
        deco.add(M(lab, 26, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.15))
    if xlab:
        deco.add(T(xlab, 26, GREY).next_to(ax.x_axis, DOWN, buff=0.58))
    if ylab:
        deco.add(T(ylab, 26, GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=ybuff))
    return ax, deco


def faint(ax, kt=KT, kr=KR, op=0.6, xmax=XMAX):
    cT = ax.plot(lambda x: x / (kt + x), x_range=[0, xmax, 0.2], color=BLUE, stroke_width=5).set_stroke(opacity=op)
    cR = ax.plot(lambda x: x / (kr + x), x_range=[0, xmax, 0.2], color=GREEN, stroke_width=6).set_stroke(opacity=op)
    return cT, cR


def faint_labels(ax):
    return (T("T site", 28, BLUE).move_to(ax.c2p(122, 0.30)),
            T("R site", 28, GREEN).move_to(ax.c2p(90, 1.075)))


def mixcurve(ax, x0=0.0, x1=XMAX, w=7):
    return ax.plot(mix, x_range=[x0, x1, 0.25], color=YELLOW, stroke_width=w)


# ------------------------------------------------------------------ cartoons
def o2(r=0.27):
    c = Circle(radius=r, color=YELLOW, fill_opacity=1, stroke_width=0)
    return VGroup(c, T("O₂", 22, BG, weight=BOLD).move_to(c))


def cup(color, sweep, r, center, stroke=7):
    """A cup that opens upward. Its sweep (degrees) is how far it wraps around: a shallow dish is a weak grip, a
    nearly closed ring a tight one."""
    return Arc(radius=r, start_angle=-PI / 2 - sweep * DEGREES / 2, angle=sweep * DEGREES, arc_center=center,
               color=color, stroke_width=stroke)


WEAK, TIGHT = 125, 320


def tetra(shape, size=1.55, links=False, cups=False, op=0.2, hs=1.0):
    """Hemoglobin as a cartoon: four blocks in two columns. T sits close together; R has its columns apart.
    Returns VGroup(blocks, links, hemes, cups); the heme discs are the four sites."""
    col = BLUE if shape == "T" else GREEN
    s = size / 1.55
    gc = 0.10 if shape == "T" else 0.5
    gr = 0.10
    xs = (-(size + gc) / 2, (size + gc) / 2)
    ys = ((size + gr) / 2, -(size + gr) / 2)
    blocks, hemes, cps, lk = VGroup(), VGroup(), VGroup(), VGroup()
    for y in ys:
        for x in xs:
            blocks.add(RoundedRectangle(corner_radius=0.14 * s, width=size, height=size, stroke_color=col,
                                        stroke_width=3, fill_color=col, fill_opacity=op).move_to([x, y, 0]))
            hemes.add(Circle(radius=0.17 * s * hs, stroke_width=0, fill_color=HEME, fill_opacity=1).move_to([x, y, 0]))
            if cups:
                cps.add(cup(col, WEAK if shape == "T" else 290, 0.42 * s, [x, y, 0], stroke=6))
    if links:
        half = gc / 2 + 0.18 * s
        offs = (-0.3 * size, 0.3 * size) if shape == "T" else (0.3 * size,)
        for y in ys:
            for dy in offs:
                lk.add(VGroup(Line([-half, y + dy, 0], [half, y + dy, 0], color=GOLD, stroke_width=3.5),
                              Dot([-half, y + dy, 0], radius=0.06, color=GOLD),
                              Dot([half, y + dy, 0], radius=0.06, color=GOLD)))
    return VGroup(blocks, lk, hemes, cps)


def letter(shape, size=56):
    return T(shape, size, BLUE if shape == "T" else GREEN, weight=BOLD)


def popbar(fr, cx, cy, w, h, minr=0.05):
    """T (blue) on the left, R (green) on the right; R share = fr. Always the same four parts."""
    wr = max(w * fr, minr)
    wt = max(w - wr, 0.02)
    left = cx - w / 2
    rT = Rectangle(width=wt, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to([left + wt / 2, cy, 0])
    rR = Rectangle(width=wr, height=h, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).move_to([left + wt + wr / 2, cy, 0])
    sz = int(min(56, max(26, h * 38)))
    lT = T("T", sz, BG, weight=BOLD).move_to([left + wt / 2, cy, 0])
    lR = T("R", sz, BG, weight=BOLD).move_to([left + wt + wr / 2, cy, 0])
    if wt < 0.8:
        lT.set_opacity(0)
    if wr < 0.8:
        lR.set_opacity(0)
    return VGroup(rT, rR, lT, lR)


def gauge(cx, cy, w, h, frac, color):
    frame = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([cx, cy, 0])
    fw = max(w * frac, 0.03)
    fill = Rectangle(width=fw, height=h, stroke_width=0, fill_color=color, fill_opacity=0.95)
    fill.move_to([cx - w / 2 + fw / 2, cy, 0])
    return VGroup(frame, fill)


def pct(v):
    return f"{round(100 * v)}%"


def pctr(v):
    """The R share, rounded down a hair so that 21.7% reads as the lesson's 21%."""
    return f"{int(100 * v + 0.2)}%"


class Sc(SpokenScene):
    pass


# ------------------------------------------------------------------ the T / R pair (scenes 2 to 5)
TX, RX, SILY, LETY, GRIPY, GRIPLY = -3.6, 3.6, 0.7, 3.35, -2.45, -3.5
SIL = 1.9


def sil_at(shape, cx, links=False):
    return tetra(shape, SIL, links=links).move_to([cx, SILY, 0])


def grip_pic(shape, cx):
    col = BLUE if shape == "T" else GREEN
    cp = cup(col, WEAK if shape == "T" else TIGHT, 0.6, [cx, GRIPY, 0], stroke=9)
    ox = o2(0.26).move_to([cx, GRIPY + (0.74 if shape == "T" else 0.0), 0])
    lab = T("weak grip" if shape == "T" else "tight grip", 32, col).move_to([cx, GRIPLY, 0])
    return cp, ox, lab


def word_lab(shape):
    return T("tense" if shape == "T" else "relaxed", 38, BLUE if shape == "T" else GREEN)


def letter_word(shape, cx):
    """The big letter and its word side by side, centred over the silhouette."""
    g = VGroup(letter(shape), word_lab(shape)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    return g.move_to([cx, LETY, 0])


def bridge_label(sil, text, toward):
    """A label in the gap between the two silhouettes, with a leader line to one bridge of `sil`."""
    lk = sil[1][1 if toward == "T" else 0]          # the highest bridge of the top row
    lab = VGroup(*[T(w, 30, GOLD) for w in text.split("|")]).arrange(DOWN, buff=0.1)
    y = lk.get_center()[1]
    if toward == "T":
        lab.move_to([0.05, y, 0])
        a = Arrow(lab.get_left() + LEFT * 0.05, lk[2].get_center() + RIGHT * 0.02, color=GOLD, buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.12)
    else:
        lab.move_to([0.05, y, 0])
        a = Arrow(lab.get_right() + RIGHT * 0.05, lk[1].get_center() + LEFT * 0.02, color=GOLD, buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.12)
    return VGroup(lab, a)


# ---------------------------------------------------------------- cards
class S00Title(TitleCard):
    LESSON = "Protein Binding and Allostery: How Hemoglobin Loads and Delivers Oxygen"
    TITLE = "Two Shapes Make the S"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = VGroup(T("PROTEIN BINDING AND ALLOSTERY:", size=22, color=GREY),
                        T("HOW HEMOGLOBIN LOADS AND DELIVERS OXYGEN", size=22, color=GREY)).arrange(DOWN, buff=0.12)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.25))
        self.play(Write(title), GrowFromCenter(rule), run_time=self.beat(0.35))
        self.wait(self.beat(0.2))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


class S30End(EndCard):
    LINE = "Two shapes differ in grip; oxygen shifting their mix makes the S."


# ---------------------------------------------------------------- 1: the question
class S01Q(Sc):
    def construct(self):
        ax, deco = mk_axes()
        mb = ax.plot(lambda x: x / (2 + x), x_range=[0, XMAX, 0.2], color=MB, stroke_width=7)
        hb = mixcurve(ax)
        lmb = T("myoglobin: a hyperbola", 30, MB).move_to(ax.c2p(58, 1.1))
        lhb = T("hemoglobin: an S", 30, YELLOW).move_to(ax.c2p(112, 0.46))
        self.play(FadeIn(ax), FadeIn(deco), run_time=0.5)
        self.play(Create(mb), run_time=1.0)
        self.play(FadeIn(lmb, shift=UP * 0.1), run_time=0.4)
        self.at("hemoglobin draws")
        self.play(Create(hb), run_time=1.2)
        self.play(FadeIn(lhb, shift=UP * 0.1), run_time=0.4)
        self.at("where does the")
        q = T("Where does the S come from?", 46, GOLD).move_to([0, 3.2, 0])
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- 2: four sites, two shapes
class S02Four(Sc):
    def construct(self):
        big = tetra("T", SIL).move_to([0, SILY, 0])
        self.add(big[0])
        self.at("hemoglobin has")
        self.play(Indicate(big[0], color=BLUE, scale_factor=1.03), run_time=0.7)
        self.at("four sites")
        self.play(LaggedStart(*[GrowFromCenter(h) for h in big[2]], lag_ratio=0.3), run_time=1.1)
        lab = T("four hemes: four sites for oxygen", 32, HEME).move_to([0, -2.1, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        self.at("take either")
        Tg = tetra("T", SIL).move_to([TX, SILY, 0])
        Rg = tetra("R", SIL).move_to([RX, SILY, 0])
        rc = big.copy()
        self.add(rc)
        self.play(Transform(big, Tg), Transform(rc, Rg), FadeOut(lab), run_time=0.8)
        self.at("two overall shapes")
        lt, lr = letter("T").move_to([TX, LETY, 0]), letter("R").move_to([RX, LETY, 0])
        note = T("schematic: boxes are subunits, orange dots are hemes", 26, GREY).move_to([0, -2.1, 0])
        self.play(FadeIn(lt, shift=DOWN * 0.15), FadeIn(lr, shift=DOWN * 0.15), FadeIn(note), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- 3: T, the tense shape
class S03T(Sc):
    def construct(self):
        Tg = sil_at("T", TX, links=True)
        Rg = sil_at("R", RX)
        lt, lr = letter("T").move_to([TX, LETY, 0]), letter("R").move_to([RX, LETY, 0])
        self.add(Tg[0], Tg[2], Rg, lt, lr)
        self.play(Rg.animate.fade(0.65), lr.animate.fade(0.65), run_time=0.6)
        self.at("for tense")
        tg = letter_word("T", TX)
        self.play(lt.animate.move_to(tg[0]), FadeIn(tg[1], shift=RIGHT * 0.2), run_time=0.7)
        self.at("held by extra")
        self.play(LaggedStart(*[FadeIn(l, scale=1.4) for l in Tg[1]], lag_ratio=0.2), run_time=1.2)
        cl = bridge_label(Tg, "extra|salt bridges", "T")
        self.play(FadeIn(cl, shift=LEFT * 0.15), run_time=0.6)
        self.play(Indicate(Tg[1], color=GOLD, scale_factor=1.15), run_time=0.9)
        self.at("each heme")
        cp, ox, lab = grip_pic("T", TX)
        self.play(Create(cp), FadeIn(ox, shift=DOWN * 0.3), run_time=0.5)
        self.at("holds oxygen")
        self.play(ox.animate.shift(UP * 0.14), run_time=0.45)
        self.play(ox.animate.shift(DOWN * 0.14), FadeIn(lab, shift=UP * 0.1), run_time=0.45)
        self.play(ox.animate.shift(UP * 0.1), run_time=0.35)
        self.play(ox.animate.shift(DOWN * 0.1), run_time=0.35)
        self.finish()


# ---------------------------------------------------------------- 4: R, the relaxed shape
def build_T_state():
    """Everything scene 3 ends with, for the T side (silhouette, word, grip picture, bridge label)."""
    Tg = sil_at("T", TX, links=True)
    tg = letter_word("T", TX)
    cp, ox, lab = grip_pic("T", TX)
    cl = bridge_label(Tg, "extra|salt bridges", "T")
    return VGroup(Tg, tg, cp, ox, lab), cl


class S04R(Sc):
    def construct(self):
        Tall, cl = build_T_state()
        Rg = sil_at("R", RX, links=True)
        Rbase = VGroup(Rg[0], Rg[2])
        Rdim = Rbase.copy().fade(0.65)
        lr = letter("R").move_to([RX, LETY, 0])
        self.add(Tall, cl, Rdim, lr)
        lr.fade(0.65)
        self.play(Tall.animate.fade(0.65), FadeOut(cl), Transform(Rdim, Rbase), lr.animate.set_opacity(1), run_time=0.7)
        self.at("for relaxed")
        rg = letter_word("R", RX)
        self.play(lr.animate.move_to(rg[0]), FadeIn(rg[1], shift=RIGHT * 0.2), run_time=0.7)
        self.at("fewer of those")
        self.play(LaggedStart(*[FadeIn(l, scale=1.4) for l in Rg[1]], lag_ratio=0.2), run_time=0.8)
        cl2 = bridge_label(Rg, "fewer|bridges", "R")
        self.play(FadeIn(cl2, shift=RIGHT * 0.15), run_time=0.5)
        self.play(Indicate(Rg[1], color=GOLD, scale_factor=1.2), run_time=0.6)
        self.at("each heme")
        cp = cup(GREEN, WEAK, 0.6, [RX, GRIPY, 0], stroke=9)
        ox = o2(0.26).move_to([RX, GRIPY + 0.74, 0])
        self.play(Create(cp), FadeIn(ox, shift=DOWN * 0.3), run_time=0.4)
        self.at("holds oxygen")
        cp2 = cup(GREEN, TIGHT, 0.6, [RX, GRIPY, 0], stroke=9)
        lab = T("tight grip", 32, GREEN).move_to([RX, GRIPLY, 0])
        self.play(Transform(cp, cp2), ox.animate.move_to([RX, GRIPY, 0]), FadeIn(lab, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(cp, color=GREEN, scale_factor=1.12), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- 5: one illustrative fit
class S05Fit(Sc):
    def construct(self):
        Tall, _ = build_T_state()
        Tall.fade(0.65)
        Rg = sil_at("R", RX, links=True)
        rg = letter_word("R", RX)
        cp, ox, lab = grip_pic("R", RX)
        Rall = VGroup(Rg, rg, cp, ox, lab)
        self.add(Tall, Rall)
        ax, deco = mk_axes()
        cT, cR = faint(ax, op=1.0)
        self.play(FadeOut(Tall), FadeOut(Rall), run_time=0.3)
        self.play(FadeIn(ax), FadeIn(deco), run_time=0.25)
        self.at("illustrative fit")
        tag = T("one illustrative fit", 34, GOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)
        self.at("half full only near")
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(110, 0.5), color=GREY, stroke_width=2.5)
        dT = Dot(ax.c2p(110, 0.5), color=BLUE, radius=0.13)
        vT = DashedLine(ax.c2p(110, 0.5), ax.c2p(110, 0), color=BLUE, stroke_width=3)
        lT = VGroup(T("T site", 30, BLUE), T("half full near 110 torr", 28, BLUE)).arrange(DOWN, buff=0.1).move_to(ax.c2p(70, 0.13))
        self.play(Create(cT), run_time=1.6)
        self.play(Create(half), FadeIn(dT, scale=2), Create(vT), FadeIn(lT, shift=UP * 0.1), run_time=0.8)
        self.at("half full below")
        dR = Dot(ax.c2p(0.37, 0.5), color=GREEN, radius=0.13)
        lR = VGroup(T("R site", 30, GREEN), T("half full below 1 torr", 28, GREEN)).arrange(DOWN, buff=0.1).move_to(ax.c2p(62, 0.68))
        arr = Arrow(lR.get_left() + LEFT * 0.05, ax.c2p(1.6, 0.51), color=GREEN, buff=0.04, stroke_width=4,
                    max_tip_length_to_length_ratio=0.12)
        self.play(Create(cR), FadeIn(dR, scale=2), FadeIn(lR, shift=UP * 0.1), GrowArrow(arr), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- 6: empty molecules flicker
G6 = [(-4.3, 1.5), (0.0, 1.5), (4.3, 1.5), (-4.3, -1.6), (0.0, -1.6), (4.3, -1.6)]


def mini(shape, cx, cy, size=1.0):
    g = tetra(shape, size).move_to([cx, cy, 0])
    return VGroup(g, letter(shape, 32).next_to(g, DOWN, buff=0.15))


class S06Flicker(Sc):
    def construct(self):
        Tm = [mini("T", x, y) for x, y in G6]
        Rm = [mini("R", x, y) for x, y in G6]
        # rare, single, brief blinks: never two at once (R is far rarer than any picture can show)
        blinks = {4: [(1.3, 1.95)], 1: [(2.6, 3.25)], 3: [(3.9, 4.55)], 0: [(4.9, 5.5)], 5: [(5.8, 6.4)]}
        sched = [blinks.get(i, []) for i in range(6)]
        state = [False] * 6
        holders = []
        for i in range(6):
            h = Tm[i].copy()

            def upd(m, dt, i=i):
                now = self.elapsed()
                inr = any(a <= now < b for a, b in sched[i])
                if inr != state[i]:
                    state[i] = inr
                    m.become(Rm[i] if inr else Tm[i])
            h.add_updater(upd)
            holders.append(h)
        self.play(LaggedStart(*[FadeIn(h) for h in holders], lag_ratio=0.12), run_time=1.0)
        self.at("wait for oxygen")
        cap = T("no oxygen bound; R blinks are far rarer than shown", 28, GREY).move_to([0, 3.35, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.5)
        self.at("even empty")
        self.wait(self.beat(0.2))
        self.finish()


# ---------------------------------------------------------------- 7: with no oxygen, almost all T
ROWX = [-5, -3, -1, 1, 3, 5]
ROWY = 2.45
CAP7 = "no oxygen: share of molecules in each shape"
BAR7_Y = -0.25


class S07MostlyT(Sc):
    def construct(self):
        mols = [mini("T", x, y) for x, y in G6]
        self.add(*mols)
        self.play(*[m.animate.scale(0.7).move_to([x, ROWY, 0]) for m, x in zip(mols, ROWX)], run_time=1.1)
        self.at("far more stable")
        bar = popbar(0.0, 0, BAR7_Y, 11.2, 1.8)
        cap = T(CAP7, 28, GREY).move_to([0, 0.95, 0])
        self.play(FadeIn(cap), GrowFromEdge(bar, LEFT), run_time=1.0)
        self.at("almost absent")
        lab = T("R: almost none", 32, GREEN).move_to([3.7, -1.75, 0])
        arr = Arrow([4.9, -1.45, 0], [5.55, -1.05, 0], color=GREEN, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.4)
        note = T("R is drawn as a hairline: its true share is far thinner", 26, GREY).move_to([0, -2.75, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), GrowArrow(arr), FadeIn(note), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- 8: the average, weighted
def term(base, sub_, col, size=56):
    b, s = T(base, size, col), T(sub_, int(size * 0.55), col)
    s.next_to(b, DR, buff=0.02).shift(UP * 0.12)
    return VGroup(b, s)


def build_eq(k=1.4):
    w2 = VGroup(T("(1 −", int(60 * k), BLUE), term("f", "R", BLUE, int(64 * k)), T(")", int(60 * k), BLUE)).arrange(RIGHT, buff=0.1)
    eq = VGroup(T("Y", int(64 * k), YELLOW), T("=", int(64 * k)), term("f", "R", GREEN, int(64 * k)), T("×", int(60 * k)),
                term("Y", "R", GREEN, int(64 * k)), T("+", int(60 * k)), w2, T("×", int(60 * k)),
                term("Y", "T", BLUE, int(64 * k))).arrange(RIGHT, buff=0.26)
    return eq


EQ_Y = 1.7


def eq_fit():
    eq = build_eq()
    if eq.width > 12.4:
        eq.set_width(12.4)
    return eq.move_to([0, EQ_Y, 0])


BAR8_Y = -2.2


class S08Avg(Sc):
    def construct(self):
        mols = VGroup(*[mini("T", x, y).scale(0.7).move_to([ROWX[i], ROWY, 0]) for i, (x, y) in enumerate(G6)])
        bar = popbar(0.0, 0, BAR7_Y, 11.2, 1.8)
        cap = T(CAP7, 28, GREY).move_to([0, 0.95, 0])
        lab = T("R: almost none", 32, GREEN).move_to([3.7, -1.75, 0])
        arr = Arrow([4.9, -1.45, 0], [5.55, -1.05, 0], color=GREEN, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.4)
        note = T("R is drawn as a hairline: its true share is far thinner", 26, GREY).move_to([0, -2.75, 0])
        self.add(mols, bar, cap, lab, arr, note)
        self.play(FadeOut(mols), FadeOut(cap), FadeOut(lab), FadeOut(arr), FadeOut(note), run_time=0.5)
        self.at("a mix")
        exl = T("an example mix of T and R", 28, GREY).move_to([0, BAR8_Y - 0.95, 0])
        self.play(Transform(bar, popbar(0.21, 0, BAR8_Y, 10, 1.0)), FadeIn(exl), run_time=1.0)
        self.at("its fullness")
        eq = eq_fit()
        self.play(Write(eq), run_time=1.0)

        def pair(parts, labels, cols):
            boxes = VGroup(*[SurroundingRectangle(p, color=GOLD, buff=0.12, stroke_width=4) for p in parts])
            labs = VGroup(*[T(t, 32, c).next_to(p, DOWN, buff=0.45) for p, t, c in zip(parts, labels, cols)])
            return boxes, labs
        b1, g1 = pair([eq[0]], ["overall fullness"], [YELLOW])
        self.play(Create(b1), FadeIn(g1, shift=UP * 0.1), run_time=0.5)
        self.at("each shape's fullness")
        self.play(FadeOut(b1), FadeOut(g1), run_time=0.2)
        b2, g2 = pair([eq[4], eq[8]], ["R's fullness", "T's fullness"], [GREEN, BLUE])
        self.play(Create(b2), FadeIn(g2, shift=UP * 0.1), run_time=0.6)
        self.at("weighted by")
        self.play(FadeOut(b2), FadeOut(g2), run_time=0.2)
        b3, g3 = pair([eq[2], eq[6]], ["fraction R", "fraction T"], [GREEN, BLUE])
        self.play(Create(b3), FadeIn(g3, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- 9 and 10: the mix at 20 and at 100 torr
SL_Y, BAR_Y, BAR_W = 3.05, 1.2, 8.0
ROW_Y = (-0.35, -1.45, -2.7)


def slider(p):
    x0, x1 = -4.6, 4.6
    line = Line([x0, SL_Y, 0], [x1, SL_Y, 0], color=GREY, stroke_width=3)
    ticks = VGroup()
    for v in (0, 50, 100, 150):
        x = x0 + (x1 - x0) * v / 150
        ticks.add(Line([x, SL_Y - 0.1, 0], [x, SL_Y + 0.1, 0], color=GREY, stroke_width=3),
                  M(str(v), 26, GREY).move_to([x, SL_Y - 0.42, 0]))
    kx = x0 + (x1 - x0) * p / 150
    knob = Dot([kx, SL_Y, 0], radius=0.17, color=YELLOW)
    lab = M(f"{p:.0f} torr", 30, YELLOW).move_to([kx, SL_Y + 0.46, 0])
    name = T("pO₂", 28, GREY).move_to([-5.7, SL_Y, 0])
    return VGroup(line, ticks, name, knob, lab)


def dbar(p):
    return popbar(mwc(p)[0], 0, BAR_Y, BAR_W, 0.9)


def bar_frame():
    """The bar's own scale, separate from the slider: 0% at the left end, 100% at the right, and what it shows."""
    return VGroup(M("0%", 26, GREY).move_to([-BAR_W / 2 - 0.55, BAR_Y, 0]),
                  M("100%", 26, GREY).move_to([BAR_W / 2 + 0.8, BAR_Y, 0]),
                  T("share of molecules in each shape", 26, GREY).move_to([0, BAR_Y + 0.88, 0]))


def rpct(p):
    fr = mwc(p)[0]
    wr = max(BAR_W * fr, 0.05)
    return M(f"{pctr(fr)} R", 30, GREEN).move_to([BAR_W / 2 - wr / 2, BAR_Y - 0.75, 0])


def gx(label, col, y, frac, h=0.55, size=32):
    lab = T(label, size, col)
    lab.move_to([-3.9 - lab.width / 2, y, 0])
    g = gauge(0, y, 7.2, h, frac, col)
    val = M(f"{pct(frac)} full", 30, col)
    val.move_to([3.9 + val.width / 2, y, 0])
    return VGroup(lab, g, val)


def rowR(p):
    return gx("R site", GREEN, ROW_Y[0], mwc(p)[1])


def rowT(p):
    return gx("T site", BLUE, ROW_Y[1], mwc(p)[2])


def rowM(p):
    return gx("mix", YELLOW, ROW_Y[2], mwc(p)[3], h=0.8, size=36)


class S09At20(Sc):
    def construct(self):
        eq = eq_fit()
        bar = popbar(0.21, 0, BAR8_Y, 10, 1.0)
        exl = T("an example mix of T and R", 28, GREY).move_to([0, BAR8_Y - 0.95, 0])
        # the end state of scene 8 (equation, its last highlights, the bar)
        b3 = VGroup(*[SurroundingRectangle(p, color=GOLD, buff=0.12, stroke_width=4) for p in (eq[2], eq[6])])
        g3 = VGroup(*[T(t, 32, c).next_to(p, DOWN, buff=0.45) for p, t, c in zip((eq[2], eq[6]), ("fraction R", "fraction T"), (GREEN, BLUE))])
        self.add(eq, b3, g3, bar, exl)
        self.play(FadeOut(eq), FadeOut(b3), FadeOut(g3), FadeOut(exl), FadeOut(bar), run_time=0.6)
        self.remove(bar)
        bar = popbar(0.21, 0, BAR_Y, BAR_W, 0.9)
        self.play(FadeIn(slider(20), shift=DOWN * 0.15), FadeIn(bar), Transform(bar, dbar(20)), FadeIn(bar_frame()), run_time=0.8)
        self.at("a fifth")
        pc = rpct(20)
        self.play(FadeIn(pc, shift=UP * 0.1), run_time=0.6)
        self.at("together")
        rr, rt = rowR(20), rowT(20)
        self.play(FadeIn(rr, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(rt, shift=RIGHT * 0.2), run_time=0.6)
        self.at("one third full")
        rm = rowM(20)
        self.play(FadeIn(rm, shift=RIGHT * 0.2), run_time=0.7)
        self.play(Indicate(rm[2], color=YELLOW, scale_factor=1.2), run_time=0.7)
        self.finish()


class S10At100(Sc):
    def construct(self):
        p = ValueTracker(20)
        sl = always_redraw(lambda: slider(p.get_value()))
        bar = always_redraw(lambda: dbar(p.get_value()))
        pc = always_redraw(lambda: rpct(p.get_value()))
        rr = always_redraw(lambda: rowR(p.get_value()))
        rt = always_redraw(lambda: rowT(p.get_value()))
        rm = always_redraw(lambda: rowM(p.get_value()))
        self.add(sl, bar, bar_frame(), pc, rr, rt, rm)
        self.at("at 100")
        self.play(p.animate.set_value(100), run_time=2.2, rate_func=smooth)
        self.at("the mix is about")
        self.play(Indicate(rm, color=YELLOW, scale_factor=1.05), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- 11: what is delivered, and what changed
GAUGE_X, GAUGE_W = 0.6, 9.0
GY_FINAL, GY_START = 2.75, 0.85


def top_group(gy):
    """The mix gauge with its two marks and the delivered band, built around height gy."""
    gl, gr = GAUGE_X - GAUGE_W / 2, GAUGE_X + GAUGE_W / 2
    x33, x98 = gl + GAUGE_W * mwc(20)[3], gl + GAUGE_W * mwc(100)[3]
    lab = T("mix", 36, YELLOW).move_to([gl - 0.95, gy, 0])
    g = gauge(GAUGE_X, gy, GAUGE_W, 1.0, mwc(100)[3], YELLOW)
    band = Rectangle(width=x98 - x33, height=1.0, stroke_width=0, fill_color=GOLD, fill_opacity=0.65).move_to([(x33 + x98) / 2, gy, 0])
    m1 = VGroup(Line([x33, gy - 0.5, 0], [x33, gy - 0.9, 0], color=GREY, stroke_width=3),
                M("20 torr: 33%", 26, TEXT).move_to([x33 - 0.2, gy - 1.2, 0]))
    m2 = VGroup(Line([x98, gy - 0.5, 0], [x98, gy - 0.9, 0], color=GREY, stroke_width=3),
                M("100 torr: 98%", 26, TEXT).move_to([x98 - 0.4, gy - 1.2, 0]))
    dl = T("about two-thirds delivered", 40, GOLD).move_to([(x33 + x98) / 2, gy - 2.05, 0])
    return lab, g, m1, m2, band, dl


class S11Deliver(Sc):
    def construct(self):
        sl, bar, pc = slider(100), dbar(100), rpct(100)
        rr, rt, rm = rowR(100), rowT(100), rowM(100)
        bf = bar_frame()
        self.add(sl, bar, bf, pc, rr, rt, rm)
        lab, g, m1, m2, band, dl = top_group(GY_START)
        top = VGroup(lab, g)
        self.play(FadeOut(sl), FadeOut(bar), FadeOut(bf), FadeOut(pc), FadeOut(rr), FadeOut(rt), Transform(rm, top), run_time=0.8)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.5)
        self.at("about two thirds")
        self.play(FadeIn(band), FadeIn(dl, shift=UP * 0.1), run_time=0.8)
        self.at("notice what changed")
        shift = UP * (GY_FINAL - GY_START)
        head = T("share of molecules that are R", 28, GREY).move_to([0, -0.1, 0])
        self.play(rm.animate.shift(shift), VGroup(m1, m2, band, dl).animate.shift(shift), FadeIn(head), run_time=0.9)
        rows = []
        for y, pp in zip((-0.95, -1.95, -2.95), (5, 20, 100)):
            fr = mwc(pp)[0]
            lab_ = M(f"{pp} torr", 28, TEXT)
            lab_.move_to([-4.1 - lab_.width, y, 0])
            lab_.align_to([-4.1, 0, 0], RIGHT)
            b = popbar(fr, 0.3, y, 8, 0.75)
            val = M(("0.2%" if pp == 5 else pctr(fr)) + " R", 28, GREEN)
            val.move_to([4.3 + val.width / 2 + 0.3, y, 0])
            rows.append(VGroup(lab_, b, val))
        self.play(FadeIn(rows[0]), run_time=0.5)
        self.at("the fraction")
        self.play(FadeIn(rows[1]), run_time=0.5)
        self.at("climbed")
        self.play(FadeIn(rows[2]), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- 12: why? R holds oxygen better, so oxygen favors R
WELL_HW, WELL_RIM = 2.4, 1.45
W_TX, W_RX = -3.0, 3.4
STEP = 0.5
YB_T, YB_R = -1.3, -0.2


def well(cx, yb, col):
    return ParametricFunction(lambda t: np.array([cx + t, yb + (WELL_RIM - yb) * (t / WELL_HW) ** 2, 0]),
                              t_range=[-WELL_HW, WELL_HW], color=col, stroke_width=6)


class S12Why(Sc):
    def construct(self):
        wT, wR = well(W_TX, YB_T, BLUE), well(W_RX, YB_R, GREEN)
        mT = tetra("T", 0.7, hs=1.5).move_to([W_TX, YB_T + 1.05, 0])
        mR = tetra("R", 0.7, hs=1.5).move_to([W_RX, YB_R + 1.05, 0])
        lt, lr = letter("T").move_to([W_TX, 3.35, 0]), letter("R").move_to([W_RX, 3.35, 0])
        ar = Arrow([-6.0, 1.5, 0], [-6.0, -2.7, 0], color=GREY, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        arl = T("more stable", 28, GREY).rotate(PI / 2).move_to([-6.45, -0.6, 0])
        self.play(Create(wT), Create(wR), FadeIn(mT), FadeIn(mR), FadeIn(lt), FadeIn(lr), GrowArrow(ar), FadeIn(arl), run_time=1.0)
        self.at("holds oxygen far better")
        oT, oR = o2(0.26).move_to([W_TX + 0.4, 2.7, 0]), o2(0.26).move_to([W_RX + 0.4, 2.7, 0])
        gl = VGroup(T("weak grip", 30, BLUE).move_to([W_TX, -3.3, 0]), T("tight grip", 30, GREEN).move_to([W_RX, -3.3, 0]))
        hT, hR = mT[2][1].get_center(), mR[2][1].get_center()
        self.play(oT.animate.move_to(hT + UP * 0.35), oR.animate.move_to(hR), FadeIn(gl), run_time=0.8)
        # R holds the oxygen: its well deepens a step. T barely holds it: the coin lifts off and its well hardly changes.
        self.play(Transform(wR, well(W_RX, YB_R - STEP, GREEN)), VGroup(mR, oR).animate.shift(DOWN * STEP),
                  Transform(wT, well(W_TX, YB_T - 0.03, BLUE)), oT.animate.shift(UP * 0.25), run_time=0.9)
        self.at("each oxygen bound")
        cur = YB_R - STEP
        coins = [oR]
        for idx in (0, 3):
            c = o2(0.26).move_to([W_RX + 0.4, 2.7, 0])
            self.play(c.animate.move_to(mR[2][idx].get_center()), run_time=0.45)
            cur -= STEP
            self.play(Transform(wR, well(W_RX, cur, GREEN)), VGroup(mR, *coins, c).animate.shift(DOWN * STEP), run_time=0.7)
            coins.append(c)
        self.at("more favorable")
        cap = T("deeper well = more favorable", 32, GOLD).move_to([0.2, 2.45, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.1), Indicate(wR, color=GOLD, scale_factor=1.0), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- 13: oxygen pulls the balance toward R
PIV = np.array([0.0, -1.6, 0.0])


def bpos(s, a):
    return PIV + s * np.array([np.cos(a * DEGREES), -np.sin(a * DEGREES), 0.0])


class S13Reactant(Sc):
    def construct(self):
        a = ValueTracker(-8.0)
        beam = always_redraw(lambda: Line(bpos(-4.8, a.get_value()), bpos(4.8, a.get_value()), color=GREY, stroke_width=10))
        base = Triangle(color=GREY, fill_opacity=1, fill_color=GREY, stroke_width=0).scale(0.34).move_to(PIV + DOWN * 0.4)
        Ti, Ri = tetra("T", 1.3), tetra("R", 1.3)
        Ti.add_updater(lambda m: m.move_to(bpos(-3.2, a.get_value()) + UP * 1.85))
        Ri.add_updater(lambda m: m.move_to(bpos(3.2, a.get_value()) + UP * 1.85))

        def arrows():
            k = a.get_value() / 8.0
            f, b = 1.5 + 0.6 * k, 1.5 - 0.6 * k
            return VGroup(Arrow([-f / 2, 3.28, 0], [f / 2, 3.28, 0], color=GREEN, buff=0, stroke_width=6),
                          Arrow([b / 2, 2.82, 0], [-b / 2, 2.82, 0], color=BLUE, buff=0, stroke_width=6))
        eqa = always_redraw(arrows)
        tl, tr = letter("T", 50).move_to([-1.9, 3.05, 0]), letter("R", 50).move_to([1.9, 3.05, 0])
        Ti.update()
        Ri.update()
        self.play(FadeIn(beam), FadeIn(base), FadeIn(Ti), FadeIn(Ri), FadeIn(tl), FadeIn(tr), FadeIn(eqa), run_time=1.0)
        self.at("reactant")
        chips = [o2(0.27).move_to([x, 3.0, 0]) for x in (3.4, 4.2, 5.0, 5.8)]
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in chips], lag_ratio=0.2), run_time=0.9)
        # the four heme sites of R, relative to R's centre
        offs = [Ri[2][k].get_center() - Ri.get_center() for k in (1, 0, 3, 2)]

        def land(i):
            return chips[i].animate.move_to(Ri.get_center() + offs[i])
        self.at("only R uses")
        self.play(land(0), land(1), run_time=0.9)
        for i in (0, 1):
            chips[i].add_updater(lambda m, o=offs[i]: m.move_to(Ri.get_center() + o))
        cap = T("R uses O₂; T barely does", 34, GOLD).move_to([0, -3.45, 0])
        self.play(FadeIn(cap, shift=UP * 0.1), run_time=0.5)
        self.at("adding oxygen")
        self.play(land(2), land(3), run_time=0.8)
        for i in (2, 3):
            chips[i].add_updater(lambda m, o=offs[i]: m.move_to(Ri.get_center() + o))
        self.play(a.animate.set_value(8.0), run_time=2.0, rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------- 14: the odds of R, oxygen by oxygen
OX0, OSW = -4.3, 5.0
ODDS_Y = [2.35, 1.2, 0.05, -1.1, -2.25]
ODDS_TXT = ["millions to one", "tens of thousands to one", "a few hundred to one",
            "about even, R slightly ahead", "hundreds to one"]
TXT_X = 1.6


def lx(l10):
    return OX0 + (l10 + 8) / 11 * OSW


def odds_log(k):
    return float(np.log10((KT / KR) ** k / L0))


def site_dots(k, cx, cy):
    g = VGroup()
    for j, (dx, dy) in enumerate([(-0.19, 0.19), (0.19, 0.19), (-0.19, -0.19), (0.19, -0.19)]):
        g.add(Circle(radius=0.15, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                     fill_opacity=1 if j < k else 0.0).move_to([cx + dx, cy + dy, 0]))
    return g


def odds_row(k):
    y = ODDS_Y[k]
    l10 = odds_log(k)
    col = BLUE if l10 < -0.3 else GREEN
    icon = site_dots(k, -6.0, y)
    num = M(str(k), 34, YELLOW).move_to([-5.2, y, 0])
    line = Line([OX0, y, 0], [OX0 + OSW, y, 0], color=GREY, stroke_width=2).set_opacity(0.6)
    dot = Dot([lx(l10), y, 0], radius=0.16, color=col)
    txt = T(ODDS_TXT[k], 30, col)
    txt.move_to([TXT_X + txt.width / 2, y, 0])
    return VGroup(icon, num, line, dot, txt)


class S14Odds(Sc):
    def construct(self):
        hl = T("T wins", 28, BLUE).move_to([OX0 + 0.5, 3.4, 0])
        hr = T("R wins", 28, GREEN).move_to([OX0 + OSW + 0.35, 3.4, 0])
        ev = DashedLine([lx(0), 2.7, 0], [lx(0), -2.65, 0], color=GREY, stroke_width=2.5)
        evl = T("even", 28, GREY).move_to([lx(0), 3.4, 0])
        hd = T("O₂ bound", 28, YELLOW).move_to([-5.6, 3.4, 0])
        self.at("follow one molecule")
        rows = [odds_row(k) for k in range(5)]
        axl = T("odds of R to T (log scale: each step is the same multiple)", 26, GREY).move_to([OX0 - 1.45 + 4.1, 2.95, 0])
        self.play(FadeIn(hl), FadeIn(hr), FadeIn(evl), Create(ev), FadeIn(hd), FadeIn(axl), FadeIn(rows[0], shift=RIGHT * 0.2), run_time=0.9)
        self.at("as it fills")
        self.play(FadeIn(rows[1], shift=RIGHT * 0.2), run_time=0.6)
        self.at("each oxygen multiplies")
        self.play(FadeIn(rows[2], shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.3)
        self.play(FadeIn(rows[3], shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.2)
        self.play(FadeIn(rows[4], shift=RIGHT * 0.2), run_time=0.6)
        self.at("same large factor")
        pts = [[lx(odds_log(k)), ODDS_Y[k], 0] for k in range(5)]
        diag = VMobject(stroke_color=GOLD, stroke_width=5).set_points_as_corners(pts)
        fl = T("each oxygen: the same large factor", 32, GOLD).move_to([0.2, -3.0, 0])
        self.play(Create(diag), FadeIn(fl, shift=UP * 0.1), run_time=1.0)
        note = T("illustrative fit: the pattern is the point", 26, GREY).move_to([0.0, -3.55, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------- 15: that factor is the gap in grip
class S15Factor(Sc):
    def construct(self):
        ax, deco = mk_axes()
        cT, cR = faint(ax, op=1.0)
        lT, lR = faint_labels(ax)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(110, 0.5), color=GREY, stroke_width=2.5)
        dT = Dot(ax.c2p(110, 0.5), color=BLUE, radius=0.13)
        dR = Dot(ax.c2p(0.37, 0.5), color=GREEN, radius=0.13)
        self.add(ax, deco, cT, cR, lT, lR)
        self.play(FadeIn(half), FadeIn(dT), FadeIn(dR), run_time=0.8)
        self.at("how much more tightly")
        gap = DoubleArrow(ax.c2p(2, 0.5), ax.c2p(108, 0.5), color=GOLD, buff=0, stroke_width=7, tip_length=0.28)
        self.play(GrowFromCenter(gap), run_time=0.9)
        gl = T("R grips about 300 times tighter", 34, GOLD).move_to(ax.c2p(58, 0.64))
        n1 = M("0.37 torr", 26, GREEN).move_to(ax.c2p(22, 0.40))
        n2 = M("110 torr", 26, BLUE).move_to(ax.c2p(128, 0.60))
        self.play(FadeIn(gl, shift=UP * 0.1), FadeIn(n1), FadeIn(n2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- 16, 17, 18: the curve follows the mix
def plot16(self, x0):
    ax, deco = mk_axes()
    cT, cR = faint(ax)
    lT, lR = faint_labels(ax)
    xt = ValueTracker(x0)
    cur = always_redraw(lambda: ax.plot(mix, x_range=[0, max(xt.get_value(), 0.3), 0.25], color=YELLOW, stroke_width=7))
    dot = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), mix(xt.get_value())), color=YELLOW, radius=0.14))
    vl = always_redraw(lambda: DashedLine(ax.c2p(xt.get_value(), 0), ax.c2p(xt.get_value(), mix(xt.get_value())),
                                          color=GREY, stroke_width=3))
    bar = always_redraw(lambda: popbar(mwc(xt.get_value())[0], AX_CX, BAR_Y3, AX_W, 0.7))

    def readout():
        fr = mwc(xt.get_value())[0]
        s = f"{100 * fr:.1f}%" if fr < 0.095 else f"{round(100 * fr)}%"
        return M(f"R: {s}", 30, GREEN).move_to([AX_CX + AX_W / 2 - 0.9, 3.6, 0])
    ro = always_redraw(readout)
    cap = T("share of molecules in each shape", 26, GREY).move_to([AX_CX - AX_W / 2 + 2.6, 3.6, 0])
    return ax, deco, cT, cR, lT, lR, xt, cur, dot, vl, bar, ro, cap


def sweeper(self, xt, x_start, x_end, t_end):
    """Return f(t): the pressure the dot should have t seconds into the scene if it moves evenly from x_start
    (at the scene start) to x_end (at t_end)."""
    return lambda t: x_start + (x_end - x_start) * min(1.0, t / t_end)


def sweep_to(self, xt, f, t, **kw):
    """Move the dot (smoothly, evenly) to where it should be at scene time t, playing any extra animations too."""
    run = max(0.05, t - self.elapsed())
    extra = kw.pop("extra", [])
    self.play(xt.animate.set_value(f(t)), *extra, run_time=run, rate_func=linear)


MIX_LAB_POS = (95, 0.73)


class S16Low(Sc):
    def construct(self):
        ax, deco, cT, cR, lT, lR, xt, cur, dot, vl, bar, ro, cap = plot16(self, 5.0)
        self.add(ax, deco, cT, cR, lT, lR)
        mixlab = T("hemoglobin, the mix", 30, YELLOW).move_to(ax.c2p(40, 0.52))
        mixarr = always_redraw(lambda: Arrow(mixlab.get_bottom() + LEFT * 0.4, dot.get_top() + UP * 0.04, color=YELLOW, buff=0.05,
                                             stroke_width=4, max_tip_length_to_length_ratio=0.15))
        self.at("at low pressure")
        self.add(cur)
        self.play(FadeIn(vl), FadeIn(dot), FadeIn(mixlab), FadeIn(mixarr), run_time=0.6)
        self.at("nearly everything")
        self.play(FadeIn(bar), FadeIn(ro), FadeIn(cap), run_time=0.8)
        self.at("the curve follows")
        f = sweeper(self, xt, 5.0, 16.0, self.narration_s)
        self.play(xt.animate.set_value(16.0), run_time=max(0.2, self.narration_s - 0.2 - self.elapsed()), rate_func=linear)
        self.finish()


class S17Mid(Sc):
    def construct(self):
        ax, deco, cT, cR, lT, lR, xt, cur, dot, vl, bar, ro, cap = plot16(self, 16.0)
        mixlab = T("hemoglobin, the mix", 30, YELLOW).move_to(ax.c2p(40, 0.52))
        self.add(ax, deco, cT, cR, lT, lR, cur, vl, dot, bar, ro, cap, mixlab)
        # one even sweep through the steep stretch (15 to 46 torr) across the whole narration
        end = self.narration_s - 0.1
        f = sweeper(self, xt, 16.0, 46.0, end)
        sweep_to(self, xt, f, self.t_of("their empty sites") - 0.2, extra=[mixlab.animate.move_to(ax.c2p(*MIX_LAB_POS))])
        sweep_to(self, xt, f, self.t_of("their empty sites") + 1.1,
                 extra=[cR.animate.set_stroke(opacity=1.0, width=7), Indicate(lR, color=GREEN, scale_factor=1.15)])
        t_steep = self.t_of("this is the steep part") - 0.2
        sweep_to(self, xt, f, t_steep)
        shade = Rectangle(width=ax.c2p(46, 0)[0] - ax.c2p(15, 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                          fill_color=GOLD, fill_opacity=0.16).move_to([(ax.c2p(46, 0)[0] + ax.c2p(15, 0)[0]) / 2,
                                                                       (ax.c2p(0, 1)[1] + ax.c2p(0, 0)[1]) / 2, 0])
        steep = ax.plot(mix, x_range=[15, 46, 0.25], color=GOLD, stroke_width=12)
        sl = T("steep part", 34, GOLD).move_to(ax.c2p(66, 0.52))
        sa = Arrow(sl.get_left() + LEFT * 0.05, ax.c2p(30, mix(30)) + RIGHT * 0.1, color=GOLD, buff=0.03, stroke_width=5,
                   max_tip_length_to_length_ratio=0.2)
        self.add(shade)
        self.bring_to_front(cur, dot, bar, ro, cap)
        self.play(FadeIn(shade), FadeIn(steep), FadeIn(sl), GrowArrow(sa), xt.animate.set_value(f(self.elapsed() + 1.2)),
                  run_time=1.2, rate_func=linear)
        self.finish()


class S18High(Sc):
    def construct(self):
        ax, deco, cT, cR, lT, lR, xt, cur, dot, vl, bar, ro, cap = plot16(self, 46.0)
        cR.set_stroke(opacity=1.0, width=7)
        mixlab = T("hemoglobin, the mix", 30, YELLOW).move_to(ax.c2p(*MIX_LAB_POS))
        self.add(ax, deco, cT, cR, lT, lR, cur, vl, dot, bar, ro, cap, mixlab)
        self.at("at high pressure")
        f = sweeper(self, xt, 46.0, 140.0, self.narration_s - 0.3)
        sweep_to(self, xt, f, self.t_of("flattens onto") - 0.2)
        sweep_to(self, xt, f, self.t_of("flattens onto") + 1.0,
                 extra=[Indicate(cR, color=GREEN, scale_factor=1.0), Indicate(lR, color=GREEN, scale_factor=1.15)])
        sweep_to(self, xt, f, self.narration_s - 0.3)
        self.finish()


# ---------------------------------------------------------------- 19 to 21: if the grips were equal
def question_tags(text="Same grip in T and R. What shape is the curve?"):
    return (T("Predict", 36, GOLD, weight=BOLD).move_to([0, 3.5, 0]),
            T(text, 32, TEXT).move_to([0, 2.9, 0]))


def gap_arrow(ax, kr=KR, kt=KT):
    return DoubleArrow(ax.c2p(max(kr * 5, 2), 0.5), ax.c2p(kt, 0.5), color=GOLD, buff=0, stroke_width=7, tip_length=0.28)


class S19Predict1(Sc):
    def construct(self):
        ax, deco = mk_axes()
        cT, cR = faint(ax)
        lT, lR = faint_labels(ax)
        tag, q = question_tags()
        self.play(FadeIn(tag, shift=DOWN * 0.1), FadeIn(ax), FadeIn(deco), run_time=0.6)
        self.play(Create(cT), Create(cR), FadeIn(lT), FadeIn(lR), run_time=1.6)
        self.at("held oxygen equally")
        gap = gap_arrow(ax)
        gl = T("now suppose: no gap in grip", 32, GOLD).move_to(ax.c2p(58, 0.62))
        self.play(GrowFromCenter(gap), FadeIn(gl, shift=UP * 0.1), run_time=0.9)
        self.at("what shape would")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.finish()


def predict1_state(self):
    ax, deco = mk_axes()
    cT, cR = faint(ax)
    lT, lR = faint_labels(ax)
    tag, q = question_tags()
    gap = gap_arrow(ax)
    gl = T("now suppose: no gap in grip", 32, GOLD).move_to(ax.c2p(58, 0.62))
    self.add(ax, deco, cT, cR, lT, lR, tag, q, gap, gl)
    return ax, deco, tag, q, lT, lR, gap, gl, cT, cR


class S20Pause(Sc):
    def construct(self):
        predict1_state(self)
        self.finish()


class S21Reveal1(Sc):
    def construct(self):
        ax, deco, tag, q, lT, lR, gap, gl, cT0, cR0 = predict1_state(self)
        self.remove(cT0, cR0)
        u = ValueTracker(0.0)

        def kT():
            return float(np.exp(np.log(KT) + (np.log(26.0) - np.log(KT)) * u.get_value()))

        def kR():
            return float(np.exp(np.log(KR) + (np.log(26.0) - np.log(KR)) * u.get_value()))
        cT = always_redraw(lambda: ax.plot(lambda x: x / (kT() + x), x_range=[0, XMAX, 0.3], color=BLUE, stroke_width=5).set_stroke(opacity=0.6))
        cR = always_redraw(lambda: ax.plot(lambda x: x / (kR() + x), x_range=[0, XMAX, 0.3], color=GREEN, stroke_width=6).set_stroke(opacity=0.6))
        self.add(cT, cR)
        # the two curves slide together: the gap closes
        self.play(FadeOut(tag), FadeOut(q), FadeOut(lT), FadeOut(lR), FadeOut(gap), FadeOut(gl), u.animate.set_value(1.0),
                  run_time=1.5, rate_func=smooth)
        eqmix = lambda x: mwc(x, 26.0, 26.0)[3]
        cur = ax.plot(eqmix, x_range=[0, XMAX, 0.3], color=YELLOW, stroke_width=7)
        lab = T("a plain hyperbola", 34, YELLOW).move_to(ax.c2p(112, 0.52))
        self.play(Create(cur), FadeIn(lab), run_time=1.0)
        self.at("favor neither")
        xt = ValueTracker(4.0)
        hl = T("equal grip: Hill coefficient 1", 32, GOLD).move_to(ax.c2p(100, 0.30))
        bar = always_redraw(lambda: popbar(mwc(xt.get_value(), 26.0, 26.0)[0], AX_CX, BAR_Y3, AX_W, 0.7))
        dot = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), eqmix(xt.get_value())), color=YELLOW, radius=0.14))
        cap = T("share of molecules in each shape (R hairline: not to scale)", 26, GREY).move_to([AX_CX, 3.6, 0])
        self.play(FadeIn(bar), FadeIn(dot), FadeIn(cap), FadeIn(hl, shift=UP * 0.1), run_time=0.8)
        self.at("mix would never")
        self.play(xt.animate.set_value(140.0), run_time=1.8, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- 22: cooperativity
BAR22_Y = 0.35


class S22Coop(Sc):
    def construct(self):
        title = T("cooperativity", 56, GOLD, font=TITLE_FONT).move_to([0, 3.3, 0])
        bar = popbar(0.0, 0, BAR22_Y, 10, 1.8)
        cap = T("share of molecules in each shape (R hairline: not to scale)", 24, GREY).move_to([0, -1.75, 0])
        self.play(GrowFromEdge(bar, LEFT), FadeIn(cap), run_time=0.5)
        self.at("cooperativity is")
        self.play(Write(title), run_time=0.8)
        self.at("is oxygen")
        chips = VGroup(*[o2(0.3).move_to([x, 2.2, 0]) for x in (-3.0, -1.0, 1.0, 3.0)])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in chips], lag_ratio=0.15), run_time=0.8)
        self.at("shifting the mix")
        # the coins stay in view until the bar has finished moving
        self.play(Transform(bar, popbar(0.8, 0, BAR22_Y, 10, 1.8)),
                  LaggedStart(*[c.animate.shift(DOWN * 0.45) for c in chips], lag_ratio=0.1), run_time=1.8)
        self.at("binds oxygen best")
        lab = T("binds oxygen best", 36, GREEN).move_to([1.0, -0.95, 0])
        self.play(FadeIn(lab, shift=UP * 0.1), Indicate(bar[1], color=GREEN, scale_factor=1.0), run_time=0.9)
        self.at("four sites share")
        bigT = tetra("T", 1.8, links=True, cups=True).move_to([0, -0.25, 0])
        bigR = tetra("R", 1.8, links=True, cups=True).move_to([0, -0.25, 0])
        ol = RoundedRectangle(corner_radius=0.35, width=5.0, height=4.3, stroke_color=GOLD, stroke_width=5).move_to([0, -0.25, 0])
        olR = RoundedRectangle(corner_radius=0.35, width=5.4, height=4.3, stroke_color=GOLD, stroke_width=5).move_to([0, -0.25, 0])
        self.play(FadeOut(bar), FadeOut(lab), FadeOut(cap), FadeOut(chips), FadeIn(bigT), Create(ol), run_time=0.6)
        self.at("one shape")
        l1 = T("one shape, four sites", 32, GOLD).move_to([0, -2.95, 0])
        coins = VGroup(*[o2(0.27).move_to(bigT[2][k].get_center() + UP * 1.2) for k in range(4)])
        self.play(FadeIn(l1, shift=UP * 0.1), FadeIn(coins), run_time=0.4)
        self.play(*[coins[k].animate.move_to(bigT[2][k].get_center()) for k in range(4)], run_time=0.6)
        self.at("a shift changes")
        l2 = T("all four sites change at once", 32, GOLD).move_to([0, -2.95, 0])
        glow = bigT[1].copy().set_color(WHITE).set_stroke(width=8)
        self.play(ShowPassingFlash(glow, time_width=0.8), Transform(bigT, bigR), Transform(ol, olR),
                  FadeOut(l1),
                  *[coins[k].animate.move_to(bigR[2][k].get_center()) for k in range(4)], run_time=0.7)
        self.at("all four at once")
        self.play(FadeIn(l2, shift=UP * 0.1), Indicate(bigT[3], color=GREEN, scale_factor=1.06), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- 23 and 24: the Hill coefficient
HX, HY, HW, HH = -2.2, -0.4, 6.0, 4.8
MX0, MW, MYC, MHT = 1.6, 4.2, -2.2, 0.7        # the horizontal meter: left edge, width, centre height, height
P50M = 25.85


def hax():
    return mk_axes(w=HW, h=HH, cx=HX, cy=HY, xlab="oxygen pressure pO₂ (torr)", ylab="fraction of sites full", ybuff=0.95)


def tangent(ax, p50, y0, slope, half):
    return Line(ax.c2p(p50 - half, y0 - slope * half), ax.c2p(p50 + half, y0 + slope * half), color=GOLD, stroke_width=7)


def meter(v):
    g = VGroup()
    g.add(Rectangle(width=MW, height=MHT, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([MX0 + MW / 2, MYC, 0]))
    w = max(MW * v / 4, 0.03)
    g.add(Rectangle(width=w, height=MHT, stroke_width=0, fill_color=GOLD, fill_opacity=0.95).move_to([MX0 + w / 2, MYC, 0]))
    for i in range(5):
        g.add(M(str(i), 26, GREY).move_to([MX0 + MW * i / 4, MYC - 0.65, 0]))
    hc = T("Hill coefficient", 26, GREY)
    g.add(hc.move_to([MX0 + hc.width / 2, MYC + 0.72, 0]))
    return g


def nlabel(v):
    t = M(f"n = {v:g}", 28, GOLD)
    return t.move_to([MX0 + MW - t.width / 2, MYC + 0.72, 0])


def s_curve(ax):
    return ax.plot(mix, x_range=[0, XMAX, 0.25], color=YELLOW, stroke_width=7)


def hyp_curve(ax):
    return ax.plot(lambda x: x / (P50M + x), x_range=[0, XMAX, 0.25], color=YELLOW, stroke_width=7)


S_SLOPE = 2.806 / (4 * P50M)
INSET_C = (3.75, 1.15)


def hill_inset():
    """A small Hill plot, log[Y/(1-Y)] against log pO2: its slope is the Hill coefficient."""
    ia = Axes(x_range=[0.3, 2.2, 1], y_range=[-2.2, 2.2, 1], x_length=3.3, y_length=3.0, tips=False,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 2.5})
    ia.move_to([INSET_C[0], INSET_C[1], 0])
    frame = VGroup(Line(ia.c2p(0.3, -2.2), ia.c2p(2.2, -2.2), color=GREY, stroke_width=2.5),
                   Line(ia.c2p(0.3, -2.2), ia.c2p(0.3, 2.2), color=GREY, stroke_width=2.5),
                   DashedLine(ia.c2p(0.3, 0), ia.c2p(2.2, 0), color=GREY, stroke_width=1.5).set_opacity(0.6))
    title = T("Hill plot: slope is n", 28, GREY).move_to([INSET_C[0], INSET_C[1] + 2.0, 0])
    xl = T("log pO₂", 24, GREY).move_to([INSET_C[0], INSET_C[1] - 1.85, 0])
    yl = T("log (full / empty)", 24, GREY).rotate(PI / 2).move_to([INSET_C[0] - 2.0, INSET_C[1], 0])
    return ia, VGroup(frame, title, xl, yl)


def hill_line(ia):
    return ia.plot(lambda lx_: lx_ - np.log10(P50M), x_range=[0.3, 2.18, 0.02], color=YELLOW, stroke_width=6)


def hill_mix(ia):
    return ia.plot(lambda lx_: float(np.log10(mix(10 ** lx_) / (1 - mix(10 ** lx_)))), x_range=[0.3, 2.18, 0.02],
                   color=YELLOW, stroke_width=6)


class S23Hill(Sc):
    def construct(self):
        ax, deco = hax()
        curve = s_curve(ax)
        self.at("hill coefficient")
        mt = meter(0)
        self.play(Create(ax), FadeIn(deco), Create(curve), FadeIn(mt), run_time=1.1)
        self.at("how steep")
        dot = Dot(ax.c2p(P50M, 0.5), color=TEXT, radius=0.13)
        tg = tangent(ax, P50M, 0.5, S_SLOPE, 14)
        sl = VGroup(T("how sharply it", 28, GOLD), T("switches at half full", 28, GOLD)).arrange(DOWN, buff=0.06).move_to(ax.c2p(80, 0.34))
        sla = Arrow(sl.get_left() + LEFT * 0.05, ax.c2p(32, 0.45), color=GOLD, buff=0.03, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        self.play(FadeIn(dot, scale=2), Create(tg), FadeIn(sl, shift=UP * 0.1), GrowArrow(sla), run_time=1.0)
        self.at("identical independent")
        ia, itxt = hill_inset()
        hc = hyp_curve(ax)
        tg1 = tangent(ax, P50M, 0.5, 0.25 / P50M, 25)
        lab1 = VGroup(T("identical,", 28, YELLOW), T("independent sites", 28, YELLOW)).arrange(DOWN, buff=0.08).move_to(ax.c2p(100, 0.2))
        hl1 = hill_line(ia)
        s1 = M("slope 1", 26, GOLD).move_to(ia.c2p(1.8, -1.35))
        self.play(FadeOut(sl), FadeOut(sla), Transform(curve, hc), Transform(tg, tg1), FadeIn(lab1), FadeIn(itxt),
                  Create(hl1), FadeIn(s1), run_time=1.2)
        nl = nlabel(1)
        self.play(Transform(mt, meter(1)), FadeIn(nl), run_time=0.7)
        self.at("hemoglobin scores about")
        sc = s_curve(ax)
        tg2 = tangent(ax, P50M, 0.5, S_SLOPE, 14)
        lab2 = T("hemoglobin", 30, YELLOW).move_to(ax.c2p(100, 0.2))
        hm = hill_mix(ia)
        s2 = M("slope 2.8", 26, GOLD).move_to(ia.c2p(0.95, 1.5))
        self.play(Transform(curve, sc), Transform(tg, tg2), FadeOut(lab1), FadeIn(lab2), Transform(hl1, hm), Transform(s1, s2), run_time=1.2)
        self.play(Transform(mt, meter(2.8)), Transform(nl, nlabel(2.8)), run_time=0.9)
        self.finish()


class S24Max(Sc):
    def construct(self):
        ax, deco = hax()
        curve = s_curve(ax)
        dot = Dot(ax.c2p(P50M, 0.5), color=TEXT, radius=0.13)
        tg = tangent(ax, P50M, 0.5, S_SLOPE, 14)
        lab2 = T("hemoglobin", 30, YELLOW).move_to(ax.c2p(100, 0.2))
        ia, itxt = hill_inset()
        hm = hill_mix(ia)
        s2 = M("slope 2.8", 26, GOLD).move_to(ia.c2p(0.95, 1.5))
        inset = VGroup(itxt, hm, s2)
        self.add(ax, deco, curve, dot, tg, lab2, meter(2.8), nlabel(2.8), inset)
        self.play(FadeOut(inset), run_time=0.5)
        self.at("no larger than")
        mx = Line([MX0 + MW, MYC - 0.55, 0], [MX0 + MW, MYC + 0.55, 0], color=GOLD, stroke_width=8)
        mxl = T("cap: 4", 30, GOLD).move_to([MX0 + MW - 0.55, MYC - 1.3, 0])
        icon = tetra("T", 0.6).move_to([1.9, 0.9, 0])
        t4 = VGroup(T("four sites:", 30, GOLD), T("score at most 4", 32, GOLD)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        t4.next_to(icon, RIGHT, buff=0.35)
        self.play(Create(mx), FadeIn(mxl), FadeIn(icon), FadeIn(t4, shift=LEFT * 0.1), run_time=1.0)
        self.at("it measures steepness")
        nc = T("a score, not a count", 36, GOLD, weight=BOLD).move_to([MX0 + MW / 2, -0.6, 0])
        self.play(FadeIn(nc, shift=UP * 0.1), Indicate(tg, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.at("does not count")
        self.play(Indicate(nc, color=GOLD, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------- 25 to 27: steep, but in the wrong place
def q2():
    return (T("Predict", 36, GOLD, weight=BOLD).move_to([0, 3.5, 0]),
            T("Steep like hemoglobin, P50 like myoglobin. How much delivered?", 28, TEXT).move_to([0, 2.9, 0]))


def lines2(ax):
    g = VGroup()
    for x in (20, 100):
        g.add(DashedLine(ax.c2p(x, 0), ax.c2p(x, 1.0), color=GOLD, stroke_width=3.5),
              M(f"{x} torr", 26, GOLD).move_to(ax.c2p(x, 1.0) + UP * 0.32))
    return g


def myo_ghost(ax):
    cur = ax.plot(lambda x: x / (2 + x), x_range=[0, XMAX, 0.2], color=MB, stroke_width=5).set_stroke(opacity=0.8)
    lab = T("myoglobin's P50: 2 torr", 28, MB).move_to(ax.c2p(63, 0.30))
    return cur, lab


class S25Predict2(Sc):
    def construct(self):
        ax, deco = mk_axes()
        cur = ax.plot(lambda x: hill(x, 26.4, 2.8), x_range=[0, XMAX, 0.2], color=YELLOW, stroke_width=7)
        tag, q = q2()
        self.play(FadeIn(ax), FadeIn(deco), FadeIn(tag, shift=DOWN * 0.1), run_time=0.6)
        self.at("as steep as")
        lab = T("hemoglobin's steepness", 28, YELLOW).move_to(ax.c2p(63, 0.47))
        self.play(Create(cur), FadeIn(lab, shift=UP * 0.1), run_time=1.2)
        self.at("myoglobin's p50")
        ghost, glab = myo_ghost(ax)
        self.play(Create(ghost), FadeIn(glab, shift=UP * 0.1), run_time=1.0)
        self.at("how much would")
        self.play(FadeIn(q, shift=UP * 0.1), Create(lines2(ax)), run_time=1.0)
        self.finish()


def steep_state(self):
    ax, deco = mk_axes()
    cur = ax.plot(lambda x: hill(x, 26.4, 2.8), x_range=[0, XMAX, 0.2], color=YELLOW, stroke_width=7)
    lab = T("hemoglobin's steepness", 28, YELLOW).move_to(ax.c2p(63, 0.47))
    ghost, glab = myo_ghost(ax)
    tag, q = q2()
    ln = lines2(ax)
    self.add(ax, deco, cur, lab, ghost, glab, ln, tag, q)
    return ax, deco, cur, lab, ghost, glab, ln, tag, q


class S26Pause(Sc):
    def construct(self):
        steep_state(self)
        self.finish()


class S27Reveal2(Sc):
    def construct(self):
        ax, deco, cur0, lab, ghost, glab, ln, tag, q = steep_state(self)
        self.remove(cur0)
        lp = ValueTracker(np.log(26.4))
        cur = always_redraw(lambda: ax.plot(lambda x: hill(x, float(np.exp(lp.get_value())), 2.8), x_range=[0, XMAX, 0.2],
                                            color=YELLOW, stroke_width=7))
        self.add(cur)
        # the steep curve slides left onto myoglobin's P50
        self.play(FadeOut(q), FadeOut(tag), FadeOut(lab), FadeOut(glab), lp.animate.set_value(np.log(2.0)), run_time=1.3,
                  rate_func=smooth)
        pl = VGroup(T("same steepness,", 28, YELLOW), T("P50 near 2 torr", 28, YELLOW)).arrange(DOWN, buff=0.06).move_to(ax.c2p(62, 0.36))
        y20, y100 = hill(20, 2.0, 2.8), hill(100, 2.0, 2.8)
        d20 = Dot(ax.c2p(20, y20), color=GOLD, radius=0.13)
        d100 = Dot(ax.c2p(100, y100), color=GOLD, radius=0.13)
        band = Line(ax.c2p(20, y20), ax.c2p(100, y100), color=GOLD, stroke_width=12)
        res = VGroup(T("delivered:", 36, GOLD), T("almost none", 36, GOLD)).arrange(DOWN, buff=0.06).move_to(ax.c2p(62, 0.70))
        resa = Arrow(res.get_top() + UP * 0.02, ax.c2p(62, 0.985), color=GOLD, buff=0.05, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(pl, shift=UP * 0.1), FadeIn(d20, scale=2), FadeIn(d100, scale=2), Create(band), run_time=0.7)
        self.play(FadeIn(res, shift=DOWN * 0.1), GrowArrow(resa), run_time=0.5)
        self.at("its steep part")
        sp = VGroup(T("steep", 30, GOLD), T("part", 30, GOLD)).arrange(DOWN, buff=0.05).move_to(ax.c2p(10.5, 0.33))
        sa = Arrow(sp.get_top() + LEFT * 0.2, ax.c2p(2.7, hill(2.7, 2.0, 2.8)) + RIGHT * 0.04, color=GOLD, buff=0.06, stroke_width=5,
                   max_tip_length_to_length_ratio=0.25)
        self.play(FadeIn(sp, shift=UP * 0.1), GrowArrow(sa), run_time=0.9)
        self.at("still full")
        old20 = ln[1]
        sf = T("20 torr: still full", 32, YELLOW).move_to(ax.c2p(20, 1.0) + UP * 0.34)
        sf.align_to(ax.c2p(20, 1.0) + LEFT * 0.15, LEFT)
        self.play(FadeOut(old20), FadeIn(sf, shift=UP * 0.1), Indicate(d20, color=GOLD, scale_factor=1.8), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- 28: both an S, and in the right place
def micro(fn, col, cx, cy):
    a = Axes(x_range=[0, 150, 150], y_range=[0, 1, 1], x_length=3.0, y_length=1.35, tips=False,
             axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 2.5}).move_to([cx, cy, 0])
    return VGroup(a, a.plot(fn, x_range=[0, 150, 0.4], color=col, stroke_width=5))


F_HYP = hill(100, 26, 1) - hill(20, 26, 1)
F_STEEP = hill(100, 2, 2.8) - hill(20, 2, 2.8)
F_HB = mix(100) - mix(20)
ROWS28 = [("hyperbola", "P50 26 torr, n = 1", lambda x: hill(x, 26, 1), TEXT, F_HYP, "about a third"),
          ("steep curve", "P50 2 torr, n = 2.8", lambda x: hill(x, 2, 2.8), TEXT, F_STEEP, "almost none"),
          ("hemoglobin", "P50 26 torr, n = 2.8", mix, YELLOW, F_HB, "about two-thirds")]
Y28 = [2.2, 0.45, -1.3]
BARX, BARW = 0.65, 3.0


def row28(i):
    nm, sb, fn, col, fr, vt = ROWS28[i]
    y = Y28[i]
    ic = micro(fn, col, -5.0, y)
    name = VGroup(T(nm, 34, col), M(sb, 22, GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    name.move_to([-3.3 + name.width / 2, y, 0])
    w = max(BARW * fr, 0.05)
    b = Rectangle(width=w, height=0.7, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([BARX + w / 2, y, 0])
    v = T(vt, 32, col)
    v.move_to([BARX + w + 0.25 + v.width / 2, y, 0])
    return VGroup(ic, name), VGroup(b, v)


class S28Both(Sc):
    def construct(self):
        head1 = T("carrier", 28, GREY).move_to([-4.4, 3.35, 0])
        head2 = T("oxygen delivered, 100 to 20 torr", 28, GREY).move_to([BARX + BARW / 2 + 0.3, 3.35, 0])
        sy = -2.7
        scale = VGroup(Line([BARX, sy, 0], [BARX + BARW, sy, 0], color=GREY, stroke_width=3))
        for f, t in ((0, "0%"), (0.5, "50%"), (1.0, "100%")):
            scale.add(Line([BARX + BARW * f, sy - 0.08, 0], [BARX + BARW * f, sy + 0.08, 0], color=GREY, stroke_width=3),
                      M(t, 26, GREY).move_to([BARX + BARW * f, sy - 0.45, 0]))
        r1, b1 = row28(0)
        r2, b2 = row28(1)
        r3, b3 = row28(2)
        self.play(FadeIn(head1), FadeIn(head2), FadeIn(scale), FadeIn(r1, shift=RIGHT * 0.2), run_time=0.8)
        self.at("delivers only")
        self.play(GrowFromEdge(b1[0], LEFT), FadeIn(b1[1]), run_time=0.9)
        self.wait(0.8)
        self.play(FadeIn(r2, shift=RIGHT * 0.2), run_time=0.6)
        self.play(GrowFromEdge(b2[0], LEFT), FadeIn(b2[1]), run_time=0.6)
        self.at("hemoglobin needs both")
        self.play(FadeIn(r3, shift=RIGHT * 0.2), run_time=0.7)
        self.play(GrowFromEdge(b3[0], LEFT), FadeIn(b3[1]), run_time=0.9)
        self.at("right place")
        box = SurroundingRectangle(VGroup(r3, b3), color=GOLD, buff=0.2, stroke_width=4)
        tx = T("an S, in the right place", 34, GOLD).move_to([0.3, -3.7, 0])
        self.play(Create(box), FadeIn(tx, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- 29, 30: the take-home
class S29Take(Sc):
    def construct(self):
        ax, deco = mk_axes(w=7.2, h=4.2, cx=2.5, cy=-0.65, xlab="oxygen pressure pO₂ (torr)", ylab="fraction of sites full", ybuff=0.95)
        curve = ax.plot(mix, x_range=[0, XMAX, 0.5], color=YELLOW, stroke_width=7)
        xt = ValueTracker(4.0)
        dot = always_redraw(lambda: Dot(ax.c2p(xt.get_value(), mix(xt.get_value())), color=YELLOW, radius=0.15))
        bar = always_redraw(lambda: popbar(mwc(xt.get_value())[0], 2.5, 2.5, 7.2, 0.7))
        cap = T("share of molecules in each shape", 26, GREY).move_to([2.5, 3.3, 0])
        # two grips on the left
        lt, lr = letter("T", 60).move_to([-6.0, 1.45, 0]), letter("R", 60).move_to([-6.0, -1.65, 0])
        cT = cup(BLUE, WEAK, 0.62, [-4.35, 1.2, 0], stroke=10)
        oT = o2(0.28).move_to([-4.35, 1.2 + 0.78, 0])
        cR = cup(GREEN, TIGHT, 0.62, [-4.35, -1.9, 0], stroke=10)
        oR = o2(0.28).move_to([-4.35, -1.9, 0])
        glT = T("weak grip", 34, BLUE).move_to([-4.6, 0.1, 0])
        glR = T("tight grip", 34, GREEN).move_to([-4.6, -3.0, 0])
        self.at("the s comes")
        self.play(FadeIn(ax), FadeIn(deco), Create(curve), run_time=1.3)
        self.at("two shapes")
        self.play(FadeIn(lt), FadeIn(lr), run_time=0.6)
        self.at("differ in grip")
        self.play(Create(cT), Create(cR), FadeIn(oT), FadeIn(oR), FadeIn(glT), FadeIn(glR), run_time=0.9)
        self.at("oxygen shifting")
        self.play(FadeIn(bar), FadeIn(dot), FadeIn(cap), run_time=0.5)
        self.play(xt.animate.set_value(140.0), run_time=1.6, rate_func=linear)
        self.finish()
