"""Winners Push Losers  (Developmental Neuroscience, competition for targets, chapter 5)

COLOR MAP (one color per concept, same as the other chapters)
  BLUE   = a neuron whose fate is not yet decided
  GREEN  = a winner / a neuron that is protected or survives (survival pathways, AKT)
  RED    = a loser / a neuron that dies or is pushed toward death
  YELLOW = nerve growth factor (NGF)
  PURPLE = the receptor TrkA (its level)
  ORANGE = the punishment signal (BDNF and NT-4)
  SAND   = the receptor TrkB (new in this chapter, few on these neurons)
  TEAL   = p75 and what runs from it (JNK, c-Jun), and the p75-null mouse
  TEXT   = wild-type (white), plain labels
  GOLD   = question marks, prediction numbers, "schematic" tags and one highlight
  GREY   = target, axes, panel frames, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SAND = "#C9A27E"
SOFT = "#B8BEC9"   # secondary text, lighter than GREY so it reads on the dark ground


def P(x, y):
    return np.array([x, y, 0.0])


# ----------------------------------------------------------------------------------------------
# small drawing helpers
# ----------------------------------------------------------------------------------------------
def soma(p, color=BLUE, r=1.0, op=0.5):
    return Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=op).move_to(p)


def to_state(d, color, op=0.5):
    return d.animate.set_stroke(color, opacity=1.0 if op > 0.3 else op + 0.3).set_fill(color, opacity=op)


def dot(p, color, r=0.1):
    return Circle(radius=r, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=1).move_to(p)


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def hbar(x0, y, w, color=PURPLE, h=0.4):
    return Rectangle(width=max(w, 0.04), height=h, stroke_color=color, stroke_width=2, fill_color=color,
                     fill_opacity=0.85).move_to(P(x0 + max(w, 0.04) / 2, y))


def recep(c, r, ang, color, hollow=False):
    a = np.deg2rad(ang)
    rc = RoundedRectangle(corner_radius=0.05, width=0.2, height=0.5, stroke_color=color, stroke_width=3,
                          fill_color=color, fill_opacity=0.12 if hollow else 0.95)
    rc.rotate(a - PI / 2)
    return rc.move_to(c + r * P(np.cos(a), np.sin(a)))


def tick_mark(c, color=GREEN, s=1.0):
    return VMobject(stroke_color=color, stroke_width=10).set_points_as_corners(
        [c + s * P(-0.3, 0.0), c + s * P(-0.1, -0.25), c + s * P(0.35, 0.3)])


def left_text(text, size, color, x, y):
    t = T(text, size, color)
    return t.move_to(P(x + t.width / 2, y))


# ----------------------------------------------------------------------------------------------
# the two-neuron stage (scenes 1-11)
# ----------------------------------------------------------------------------------------------
SC, WC = P(-4.1, 0.5), P(4.1, 0.5)
RS, RW = 1.7, 1.3
BAR_Y = -1.9
RING = RS + 0.4
CAP_Y = -3.25
A_Y = 0.95            # height of the factor stream between the two cells
CHIP_B, CHIP_N = P(0.0, 1.85), P(0.0, 0.05)


def stage(dy=0.0, bar_y=BAR_Y, bar_h=0.5, sc=(GREEN, 0.5), wc=(BLUE, 0.4), sbar=4.0, wbar=1.1):
    s0, w0 = SC + P(0, dy), WC + P(0, dy)
    d = {}
    d["S"] = soma(s0, sc[0], RS, sc[1])
    d["W"] = soma(w0, wc[0], RW, wc[1])
    d["bS"] = hbar(SC[0] - 2.0, bar_y, sbar, h=bar_h)
    d["bW"] = hbar(WC[0] - 2.0, bar_y, wbar, h=bar_h)
    d["tS"] = T("strong (high TrkA)", 28, TEXT).move_to(P(SC[0], bar_y - bar_h / 2 - 0.4))
    d["tW"] = T("weak (low TrkA)", 28, TEXT).move_to(P(WC[0], bar_y - bar_h / 2 - 0.4))
    d["trkb"] = VGroup(recep(s0, RS, 90, SAND, True), recep(w0, RW, 90, SAND, True))
    d["p75S"] = VGroup(*[recep(s0, RS, a, TEAL) for a in (-60, -35, -10)])
    d["p75W"] = VGroup(*[recep(w0, RW, a, TEAL) for a in (135, 160, 185)])
    d["p75"] = VGroup(d["p75S"], d["p75W"])
    d["lpS"] = T("p75", 28, TEAL).move_to(s0 + P(2.45, -1.3))
    d["lpW"] = T("p75", 28, TEAL).move_to(w0 + P(-1.9, 1.25))
    d["lbl"] = VGroup(d["lpS"], d["lpW"])
    d["cb"] = chip("BDNF", ORANGE, 28).move_to(CHIP_B + P(0, dy))
    d["cn"] = chip("NT-4", ORANGE, 28).move_to(CHIP_N + P(0, dy))
    d["aW"] = arr(P(-2.3, A_Y + dy), P(2.45, A_Y + dy), ORANGE, 8, 0.3)
    d["aS"] = arr(P(-1.2, A_Y + dy), P(-2.1, 0.3 + dy), ORANGE, 8, 0.3)
    return d


def add_stage(sc, d, bars=True, trkb=False, p75=False, chips=False, arrows=False):
    sc.add(d["S"], d["W"])
    if bars:
        sc.add(d["bS"], d["bW"], d["tS"], d["tW"])
    if trkb:
        sc.add(d["trkb"])
    if p75:
        sc.add(d["p75"], d["lbl"])
    if chips:
        sc.add(d["cb"], d["cn"])
    if arrows:
        sc.add(d["aS"], d["aW"])


def akt_gauge(level=1.0, dy=0.0):
    h = 1.9
    gx = SC[0] + 0.65
    cy = SC[1] + dy
    frame = Rectangle(width=0.5, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(P(gx, cy))
    fh = max(h * level, 0.02)
    fill = Rectangle(width=0.5, height=fh, stroke_width=0, fill_color=GREEN, fill_opacity=0.95)
    fill.move_to(P(gx, cy - h / 2 + fh / 2))
    return frame, fill


def weak_gauge(level=0.0, dy=0.0):
    h = 1.4
    gx = WC[0] + 0.4
    cy = WC[1] + dy
    frame = Rectangle(width=0.4, height=h, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to(P(gx, cy))
    fh = max(h * level, 0.02)
    fill = Rectangle(width=0.4, height=fh, stroke_width=0, fill_color=GREEN, fill_opacity=0.95)
    fill.move_to(P(gx, cy - h / 2 + fh / 2))
    return frame, fill


BAL_CY, BAL_L = 2.55, 2.0


def balance(cx, th, hs, hd, cy=BAL_CY, L=BAL_L, bw=0.8):
    c, s = np.cos(th), np.sin(th)
    left, right = P(cx - L * c, cy - L * s), P(cx + L * c, cy + L * s)
    beam = Line(left, right, color=TEXT, stroke_width=8)
    piv = Polygon(P(cx - 0.25, cy - 0.4), P(cx + 0.25, cy - 0.4), P(cx, cy - 0.02), stroke_color=GREY,
                  stroke_width=3, fill_color=GREY, fill_opacity=0.6)
    bl = Rectangle(width=bw, height=hs, stroke_color=GREEN, stroke_width=2, fill_color=GREEN,
                   fill_opacity=0.85).move_to(left + P(0, hs / 2 + 0.06))
    br = Rectangle(width=bw, height=hd, stroke_color=RED, stroke_width=2, fill_color=RED,
                   fill_opacity=0.85).move_to(right + P(0, hd / 2 + 0.06))
    return VGroup(beam, piv, bl, br)


def bal_labels(cx):
    return VGroup(T("survival", 28, GREEN).move_to(P(cx - 1.55, BAL_CY - 0.65)),
                  T("death signal", 28, RED).move_to(P(cx + 1.45, BAL_CY - 0.65)))


# ----------------------------------------------------------------------------------------------
# checklist (scenes 2-3)
# ----------------------------------------------------------------------------------------------
ROW_Y = [2.0, 0.55, -0.9, -2.35]
TXT_X = -3.5


def row_shell(i):
    return RoundedRectangle(corner_radius=0.15, width=12.2, height=1.3, stroke_color=GREY, stroke_width=2.5,
                            fill_color=GREY, fill_opacity=0.06).move_to(P(0, ROW_Y[i]))


def row_num(i, lit=False):
    c = Circle(radius=0.34, stroke_color=GOLD if lit else GREY, stroke_width=3, fill_opacity=0).move_to(P(-5.6, ROW_Y[i]))
    n = T(str(i + 1), 28, GOLD if lit else GREY, weight=BOLD).move_to(c)
    return VGroup(c, n)


def lit(n):
    return [n[0].animate.set_stroke(GOLD), n[1].animate.set_color(GOLD)]


def row_icon(i, level=1.0):
    y = ROW_Y[i]
    if i == 0:
        return VGroup(soma(P(-5.0, y), GREEN, 0.3, 0.7), arr(P(-4.6, y), P(-3.95, y), ORANGE, 5, 0.2))
    if i == 1:
        return VGroup(arr(P(-5.1, y), P(-4.55, y), ORANGE, 5, 0.2), soma(P(-4.2, y), RED, 0.3, 0.35))
    if i == 2:
        return VGroup(soma(P(-4.55, y), GREEN, 0.28, 0.7), Circle(radius=0.46, stroke_color=GREEN, stroke_width=4).move_to(P(-4.55, y)))
    frame = Rectangle(width=1.1, height=0.34, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to(P(-4.55, y))
    w = max(1.1 * level, 0.05)
    fill = Rectangle(width=w, height=0.34, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95).move_to(P(-5.1 + w / 2, y))
    return VGroup(frame, fill)


ROW_TXT = ["comes from strongly supported neurons", "kills weak neurons", "spares strong neurons",
           "starts only after TrkA has risen"]


def row_text(i):
    return left_text(ROW_TXT[i], 34, TEXT, TXT_X, ROW_Y[i])


# ----------------------------------------------------------------------------------------------
# prediction cards (scenes 12-13, 22)
# ----------------------------------------------------------------------------------------------
CX = [-4.55, 0.0, 4.55]
CY, CW, CH = -0.35, 4.2, 5.8
HEAD_Y = 3.25
B1 = [["competing", "neurons differ", "in TrkA level"], ["low TrkA neurons", "show high p75", "death signaling"],
      ["removing p75", "delays the loss"]]
B2 = [["tested in", "Bax-null ganglia"], ["read out by", "phosphorylated", "c-Jun"], ["tested in", "p75-null mice"]]


def card_shell(i):
    return RoundedRectangle(corner_radius=0.2, width=CW, height=CH, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.08).move_to(P(CX[i], CY))


def card_num(i):
    return T(str(i + 1), 72, GOLD, weight=BOLD).move_to(P(CX[i], CY + 2.15))


def card_block(i, which, y0, size, color, step=0.58):
    lines = (B1 if which == 1 else B2)[i]
    return VGroup(*[T(l, size, color).move_to(P(CX[i], y0 - step * k)) for k, l in enumerate(lines)])


def card_b1(i):
    return card_block(i, 1, 0.85, 35, TEXT)


def card_b2(i):
    return card_block(i, 2, -1.1, 31, SOFT, 0.52)


def head_text():
    return T("mouse superior cervical ganglion", 30, TEXT).move_to(P(0, HEAD_Y))


def tag(n):
    c = Circle(radius=0.34, stroke_color=GOLD, stroke_width=3, fill_opacity=0).move_to(P(-6.3, HEAD_Y))
    return VGroup(c, T(str(n), 30, GOLD, weight=BOLD).move_to(c))


# ----------------------------------------------------------------------------------------------
# the stained ganglion (scenes 13-14): neurons and TrkA levels are fixed here, computed once
# ----------------------------------------------------------------------------------------------
GY = -0.3
GW, GH = 11.6, 5.5


def _ganglion():
    rng = np.random.default_rng(23)
    pts, lv = [], []
    for j in range(6):
        for i in range(10):
            x = -5.4 + 1.2 * i + (0.6 if j % 2 else 0.0) + rng.uniform(-0.1, 0.1)
            y = GY + 2.15 - 0.86 * j + rng.uniform(-0.08, 0.08)
            if (x / (GW / 2 - 0.45)) ** 2 + ((y - GY) / (GH / 2 - 0.4)) ** 2 <= 1.0:
                pts.append(P(x, y))
                base = 0.92 if rng.random() < 0.5 else 0.22
                lv.append(float(np.clip(base + rng.normal(0, 0.06), 0.08, 1.0)))
    return pts, lv


G_PTS, G_LV = _ganglion()
G_DIM = [i for i, v in enumerate(G_LV) if v < 0.5]


def g_outline():
    return Ellipse(width=GW, height=GH, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                   fill_opacity=0.07).move_to(P(0, GY))


def g_cells(stained=True):
    out = []
    for p, v in zip(G_PTS, G_LV):
        if stained:
            hi = v > 0.5
            out.append(Circle(radius=0.3, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                              fill_opacity=0.95 if hi else 0.42).move_to(p))
            out[-1].set_stroke(PURPLE, opacity=1.0 if hi else 0.85)
        else:
            out.append(Circle(radius=0.3, stroke_color=GREY, stroke_width=2.5, fill_color=GREY,
                              fill_opacity=0.15).move_to(p))
    return VGroup(*out)


def g_rings():
    return VGroup(*[Circle(radius=0.38, stroke_color=TEAL, stroke_width=3, fill_opacity=0).move_to(G_PTS[i]) for i in G_DIM])


def g_legend(jun=False):
    y = -3.45
    a = VGroup(Circle(radius=0.16, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.95),
               T("high TrkA", 26, TEXT))
    a[1].next_to(a[0], RIGHT, buff=0.15)
    b = VGroup(Circle(radius=0.16, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.42),
               T("low TrkA", 26, TEXT))
    b[1].next_to(b[0], RIGHT, buff=0.15)
    c = VGroup(Circle(radius=0.2, stroke_color=TEAL, stroke_width=3.5, fill_opacity=0), T("phosphorylated c-Jun", 26, TEAL))
    c[1].next_to(c[0], RIGHT, buff=0.15)
    row = VGroup(a, b, c).arrange(RIGHT, buff=0.8).move_to(P(0, y))
    if jun:
        return a, b, c, row
    return VGroup(a, b), c


def schem_tag(x=4.9, y=3.45):
    return T("schematic, not data", 26, GOLD).move_to(P(x, y))


# ----------------------------------------------------------------------------------------------
# the neuron-number plot (scenes 17-26): every curve is computed from
#   normal:      N(t) = 0.5 + 0.5 exp(-t/1)   (t in weeks)
#   p75-null:    N(t) = 0.5 + 0.5 exp(-t/5)   slower fall, same floor (2008 study: normal by 6 months)
#   earlier one: N(t) = 0.72 + 0.28 exp(-t/5) slower fall, floor stays above normal
# The age axis is a square-root scale so the first week and the first month stay readable.
# ----------------------------------------------------------------------------------------------
PX0, PXL = -5.0, 8.4
PX1 = PX0 + PXL
PY0, PY1 = -2.75, 2.85
TAX = 40.0       # adult
T6M = 26.0
TEND = 8.0       # the p75-null and normal curves are first drawn out to about two months
NLO, NHI = 0.35, 1.08


def wx(t):
    return PX0 + PXL * np.sqrt(t / TAX)


def ny(N):
    return PY0 + (N - NLO) / (NHI - NLO) * (PY1 - PY0)


def Nw(t):
    return 0.5 + 0.5 * np.exp(-t / 1.0)


def Nn(t):
    return 0.5 + 0.5 * np.exp(-t / 5.0)


def Nm(t):
    return 0.72 + 0.28 * np.exp(-t / 5.0)


def cpts(fn, t0=0.0, t1=TEND, n=120):
    us = np.linspace(np.sqrt(t0), np.sqrt(t1), n)
    return [P(wx(u * u), ny(fn(u * u))) for u in us]


def curve(fn, color, w=6, t0=0.0, t1=TEND, dashed=False):
    c = VMobject(stroke_color=color, stroke_width=w).set_points_smoothly(cpts(fn, t0, t1))
    if dashed:
        return DashedVMobject(c, num_dashes=60, dashed_ratio=0.55)
    return c


def gap_band(f_up, f_dn, t0, t1, color, op):
    us = np.linspace(np.sqrt(t0), np.sqrt(t1), 80)
    up = [P(wx(u * u), ny(f_up(u * u))) for u in us]
    dn = [P(wx(u * u), ny(f_dn(u * u))) for u in us[::-1]]
    return Polygon(*up, *dn, stroke_width=0, fill_color=color, fill_opacity=op)


def plot_axes():
    return VGroup(Line(P(PX0, PY0), P(PX1 + 0.1, PY0), color=GREY, stroke_width=3),
                  Line(P(PX0, PY0), P(PX0, PY1), color=GREY, stroke_width=3))


def ylabel():
    return T("neuron number", 26, GREY).rotate(PI / 2).move_to(P(PX0 - 1.75, (PY0 + PY1) / 2))


def yticks():
    g = VGroup()
    for N, txt in ((1.0, "start"), (0.5, "half")):
        y = ny(N)
        g.add(Line(P(PX0 - 0.12, y), P(PX0, y), color=GREY, stroke_width=3))
        t = T(txt, 26, GREY)
        g.add(t.move_to(P(PX0 - 0.5 - t.width / 2, y)))
    return g


def xticks():
    g = VGroup()
    for t, txt in ((0, "birth"), (1, "1 week"), (4.345, "1 month"), (T6M, "6 months"), (TAX, "adult")):
        g.add(Line(P(wx(t), PY0), P(wx(t), PY0 - 0.12), color=GREY, stroke_width=3))
        g.add(T(txt, 26, GREY).move_to(P(wx(t), PY0 - 0.45)))
    g.add(T("age", 26, GREY).move_to(P(PX1 + 1.35, PY0 - 0.45)))
    return g


LEG_Y = [1.6, 1.0, 0.4]
LEG_X = 4.1


def leg(i, color, text):
    y = LEG_Y[i]
    ln = Line(P(LEG_X, y), P(LEG_X + 0.55, y), color=color, stroke_width=6)
    t = T(text, 28, color)
    t.move_to(P(LEG_X + 0.75 + t.width / 2, y))
    return VGroup(ln, t)


def start_marks():
    d = dot(P(wx(0), ny(1.0)), TEXT, 0.16)
    lb = left_text("number at birth", 26, TEXT, wx(0) + 0.45, ny(1.0) + 0.45)
    return d, lb


def plot_base(sc, legend=(True, True), tagged=True):
    sc.add(plot_axes(), ylabel(), yticks(), xticks())
    if legend[0]:
        sc.add(leg(0, TEXT, "normal"))
    if legend[1]:
        sc.add(leg(1, TEAL, "p75-null"))
    if tagged:
        sc.add(schem_tag())


def question_texts():
    g = left_text("Sketch the p75-null curve", 40, GOLD, -5.2, 3.45)
    p = T("pause and predict", 28, GOLD).move_to(P(4.6, 3.45))
    return g, p


def question_frame(sc):
    plot_base(sc, tagged=False)
    d, lb = start_marks()
    sc.add(d, lb)
    g, p = question_texts()
    sc.add(g, p)


# ==============================================================================================
class S00Title(TitleCard):
    LESSON = "Competition: How Neurons Win a Target"
    TITLE = "Winners Push Losers"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    def construct(self):
        d = stage(sbar=3.0, wbar=1.6)
        self.play(FadeIn(d["S"], scale=0.7), FadeIn(d["W"], scale=0.7), run_time=0.8)
        self.play(GrowFromEdge(d["bS"], LEFT), GrowFromEdge(d["bW"], LEFT), FadeIn(d["tS"]), FadeIn(d["tW"]), run_time=0.7)
        self.at("winner pulls ahead")
        glow = Circle(radius=RING, stroke_color=GREEN, stroke_width=8, stroke_opacity=0.55, fill_opacity=0).move_to(SC)
        self.play(Transform(d["bS"], hbar(SC[0] - 2.0, BAR_Y, 4.0, h=0.5)),
                  Transform(d["bW"], hbar(WC[0] - 2.0, BAR_Y, 1.1, h=0.5)), FadeIn(glow, scale=0.9), run_time=1.2)
        q = T("?", 210, GOLD, weight=BOLD).move_to(P(0, 0.5))
        self.at("does it need help")
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
HEAD_SMALL = "A punishment signal: what should it look like?"


class S02(SpokenScene):
    def construct(self):
        big = T("What should a punishment signal look like?", 42, TEXT).move_to(P(0, 0.4))
        q = T("?", 150, GOLD, weight=BOLD).move_to(P(0, -1.6))
        self.play(FadeIn(big, shift=UP * 0.15), run_time=1.0)
        self.play(FadeIn(q, scale=0.5), run_time=0.6)
        shells = [row_shell(i) for i in range(4)]
        nums = [row_num(i) for i in range(4)]
        head = T(HEAD_SMALL, 34, TEXT).move_to(P(0, 3.3))
        self.at("it should")
        self.play(Transform(big, head), FadeOut(q), *[FadeIn(s) for s in shells], *[FadeIn(n) for n in nums], run_time=0.8)
        self.at("strongly supported")
        self.play(*lit(nums[0]), FadeIn(row_icon(0)), FadeIn(row_text(0), shift=RIGHT * 0.3), run_time=0.9)
        self.at("kill weak ones")
        self.play(*lit(nums[1]), FadeIn(row_icon(1)), FadeIn(row_text(1), shift=RIGHT * 0.3), run_time=0.9)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        self.add(T(HEAD_SMALL, 34, TEXT).move_to(P(0, 3.3)))
        shells = [row_shell(i) for i in range(4)]
        nums = [row_num(i, lit=(i < 2)) for i in range(4)]
        self.add(*shells, *nums, row_icon(0), row_icon(1), row_text(0), row_text(1))
        self.at("spare strong ones")
        self.play(*lit(nums[2]), FadeIn(row_icon(2)), FadeIn(row_text(2), shift=RIGHT * 0.3), run_time=0.9)
        self.at("start only")
        small = row_icon(3, level=0.2)
        self.play(*lit(nums[3]), FadeIn(row_text(3), shift=RIGHT * 0.3), FadeIn(small), run_time=0.9)
        self.at("has risen")
        self.play(Transform(small, row_icon(3, level=1.0)), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04(SpokenScene):
    def construct(self):
        d = stage()
        add_stage(self, d)
        lab = T("NGF-dependent genes", 26, YELLOW)
        lb = chip("BDNF", ORANGE, 26)
        ln = chip("NT-4", ORANGE, 26)
        row = VGroup(lab, lb, ln).arrange(RIGHT, buff=0.45).move_to(P(0, 3.2))
        panel = RoundedRectangle(corner_radius=0.15, width=row.width + 0.7, height=row.height + 0.5, stroke_color=GREY,
                                 stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to(row)
        self.play(FadeIn(panel), FadeIn(lab), FadeIn(lb), FadeIn(ln), run_time=1.0)
        self.at("gene list")
        self.play(Indicate(panel, color=ORANGE, scale_factor=1.06), run_time=0.9)
        cap = T("strongly supported", 28, GREEN).move_to(P(SC[0], CAP_Y))
        glow = Circle(radius=RS + 0.2, stroke_color=GREEN, stroke_width=10, stroke_opacity=0.4, fill_opacity=0).move_to(SC)
        self.at("strongly supported neurons")
        self.play(FadeIn(cap), FadeIn(glow), to_state(d["S"], GREEN, 0.7), run_time=0.8)
        self.at("bdnf")
        cb0 = lb.copy()
        dots = VGroup(*[dot(P(-2.35, 1.2 + 0.2 * k), ORANGE, 0.12) for k in range(3)])
        self.add(dots)
        self.play(cb0.animate.move_to(CHIP_B), *[x.animate.move_to(CHIP_B + P(-0.9 - 0.1 * k, -0.1 * k)) for k, x in enumerate(dots)],
                  run_time=1.2)
        self.play(FadeOut(dots), run_time=0.2)
        self.at("nt4")
        cn0 = ln.copy()
        dots2 = VGroup(*[dot(P(-2.35, 0.7 - 0.2 * k), ORANGE, 0.12) for k in range(3)])
        self.add(dots2)
        self.play(cn0.animate.move_to(CHIP_N), *[x.animate.move_to(CHIP_N + P(-0.9 - 0.1 * k, 0.1 * k)) for k, x in enumerate(dots2)],
                  run_time=1.0)
        self.play(FadeOut(dots2), run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05(SpokenScene):
    def construct(self):
        d = stage(sc=(GREEN, 0.7))
        add_stage(self, d, chips=True)
        self.play(Indicate(d["S"], color=GREEN, scale_factor=1.05), Indicate(d["W"], color=BLUE, scale_factor=1.05), run_time=1.2)
        self.at("usual receptor")
        self.play(FadeIn(d["trkb"], scale=0.5), run_time=0.7)
        lt = T("TrkB: few", 28, SAND).move_to(P(WC[0], 2.85))
        self.at("track b")
        self.play(FadeIn(lt, shift=DOWN * 0.15), run_time=0.6)
        self.at("they do carry")
        self.play(LaggedStart(*[FadeIn(r, scale=0.4) for r in list(d["p75S"]) + list(d["p75W"])], lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(d["lbl"]), run_time=0.5)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        d = stage(sc=(GREEN, 0.7))
        add_stage(self, d, trkb=True, p75=True, chips=True)
        self.at("belongs to")
        fam = chip("p75: tumour necrosis factor (TNF) receptor family", TEAL, 26).move_to(P(0.0, 3.2))
        self.play(FadeIn(fam, shift=DOWN * 0.2), Indicate(d["p75"], color=TEAL, scale_factor=1.3), run_time=1.2)
        self.at("it can promote death")
        dth = arr(P(3.3, 1.1), P(4.15, 0.4), RED, 8, 0.3)
        dl = T("death", 30, RED).move_to(P(WC[0] + 0.3, -0.15))
        self.play(GrowArrow(dth), FadeIn(dl), to_state(d["W"], RED, 0.35), run_time=1.0)
        self.finish()


class S07(SpokenScene):
    def construct(self):
        d = stage(sc=(GREEN, 0.7), wc=(RED, 0.35))
        add_stage(self, d, trkb=True, p75=True, chips=True)
        dth = arr(P(3.3, 1.1), P(4.15, 0.4), RED, 8, 0.3)
        dl = T("death", 30, RED).move_to(P(WC[0] + 0.3, -0.15))
        self.add(dth, dl)
        self.wait(0.4)
        self.play(FadeOut(dth), FadeOut(dl), to_state(d["W"], BLUE, 0.4), run_time=0.5)
        self.at("act on")
        self.play(GrowArrow(d["aW"]), run_time=0.9)
        self.at("strong ones included")
        self.play(GrowArrow(d["aS"]), run_time=0.9)
        q = T("Why are the winners spared?", 46, GOLD).move_to(P(0, 3.25))
        self.at("why are the winners spared")
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(T("pause and predict", 28, GOLD).move_to(P(0, -3.45))), run_time=0.4)
        self.finish()


class S08Pause(NarratedScene):
    def construct(self):
        d = stage(sc=(GREEN, 0.7))
        add_stage(self, d, trkb=True, p75=True, chips=True, arrows=True)
        self.add(T("Why are the winners spared?", 46, GOLD).move_to(P(0, 3.25)))
        self.add(T("pause and predict", 28, GOLD).move_to(P(0, -3.45)))
        self.wait(5.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09(SpokenScene):
    def construct(self):
        d = stage(sc=(GREEN, 0.7))
        add_stage(self, d, trkb=True, p75=True, chips=True, arrows=True)
        ng = chip("NGF", YELLOW, 28).move_to(P(SC[0], 3.4))
        dots = VGroup(*[dot(P(SC[0] + dx, 2.95 + dy), YELLOW, 0.12) for dx, dy in [(-0.4, 0.0), (0.0, 0.25), (0.4, 0.0)]])
        self.at("strong ngf")
        self.play(FadeIn(ng, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(dots), run_time=0.3)
        self.play(dots.animate.shift(DOWN * 1.1), run_time=0.8)
        self.at("signaling")
        glowbar = Rectangle(width=4.0, height=0.5, stroke_color=PURPLE, stroke_width=7, fill_opacity=0).move_to(P(SC[0], BAR_Y))
        self.play(Create(glowbar), run_time=0.45)
        ring = Circle(radius=RING, stroke_color=GREEN, stroke_width=9, fill_opacity=0).move_to(SC)
        cap = T("protected", 30, GREEN).move_to(P(SC[0], CAP_Y))
        self.at("is protected")
        self.play(Create(ring), FadeIn(cap), to_state(d["S"], GREEN, 0.7), run_time=0.9)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        d = stage(sc=(GREEN, 0.7))
        add_stage(self, d, trkb=True, p75=True, chips=True, arrows=True)
        ring = Circle(radius=RING, stroke_color=GREEN, stroke_width=9, fill_opacity=0).move_to(SC)
        self.add(ring, T("protected", 30, GREEN).move_to(P(SC[0], CAP_Y)))
        one = T("one likely reason", 34, GOLD).move_to(P(SC[0], 3.5))
        self.at("one likely reason")
        self.play(FadeIn(one), run_time=0.6)
        up = arr(P(SC[0], -1.62), P(SC[0], -1.1), PURPLE, 8, 0.28)
        self.at("signaling keeps")
        self.play(GrowArrow(up), Indicate(d["bS"], color=PURPLE, scale_factor=1.05), run_time=0.9)
        frame, fill = akt_gauge(1.0)
        lowfill = akt_gauge(0.05)[1]
        sp = T("survival pathways", 28, GREEN).move_to(P(SC[0], 2.95))
        self.at("survival pathways")
        self.play(FadeIn(frame), FadeIn(lowfill), FadeIn(sp), run_time=0.4)
        self.play(Transform(lowfill, fill), run_time=0.8)
        akt = T("AKT", 30, GREEN, weight=BOLD).move_to(P(SC[0] - 0.7, SC[1]))
        self.at("such as")
        self.play(FadeIn(akt), run_time=0.6)
        self.finish()


class S11(SpokenScene):
    def construct(self):
        DY = -0.5
        d = stage(dy=DY, bar_y=-2.1, bar_h=0.36, sc=(GREEN, 0.7))
        add_stage(self, d, trkb=True, p75=True, chips=True, arrows=True)
        fs, ff = akt_gauge(1.0, DY)
        self.add(fs, ff, T("AKT", 30, GREEN, weight=BOLD).move_to(P(SC[0] - 0.7, SC[1] + DY)))
        bs = balance(SC[0], 0.0, 0.6, 0.25)
        bs_t = balance(SC[0], 0.15, 0.6, 0.25)
        self.play(FadeIn(bs), FadeIn(bal_labels(SC[0])), run_time=0.35)
        self.at("outweighs")
        self.play(Transform(bs, bs_t), run_time=1.1)
        bw = balance(WC[0], 0.0, 0.2, 0.6)
        bw_t = balance(WC[0], -0.15, 0.2, 0.6)
        wf, wfill = weak_gauge(0.0, DY)
        self.at("weakly supported neuron")
        self.play(FadeIn(bw), FadeIn(bal_labels(WC[0])), FadeIn(wf), run_time=0.8)
        self.at("no such cushion")
        self.play(Transform(bw, bw_t), to_state(d["W"], RED, 0.35), Indicate(wf, color=GREY, scale_factor=1.15), run_time=1.1)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S12(SpokenScene):
    def construct(self):
        shells = [card_shell(i) for i in range(3)]
        self.play(*[FadeIn(s, scale=0.9) for s in shells], run_time=0.9)
        self.at("three predictions")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(card_num(i), scale=0.5), FadeIn(card_b1(i)), FadeIn(card_b2(i))) for i in range(3)],
                              lag_ratio=0.3), run_time=1.3)
        self.at("mouse superior")
        self.play(FadeIn(head_text(), shift=DOWN * 0.2), run_time=0.8)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        shells = [card_shell(i) for i in range(3)]
        nums = [card_num(i) for i in range(3)]
        b1s = [VGroup(card_b1(i), card_b2(i)) for i in range(3)]
        head = head_text()
        self.add(*shells, *nums, *b1s, head)
        t1 = tag(1)
        ell = g_outline()
        cells0 = g_cells(False)
        self.play(*[FadeOut(m) for m in shells + b1s], FadeOut(nums[1]), FadeOut(nums[2]), Transform(nums[0], t1),
                  run_time=0.4)
        self.play(FadeIn(ell), run_time=0.35)
        self.at("competing neurons")
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cells0], lag_ratio=0.02), run_time=0.7)
        stained = g_cells(True)
        self.at("differ in")
        self.play(Transform(cells0, stained), run_time=0.75)
        self.at("level")
        key = g_legend()[0]
        self.add(schem_tag(4.95, 2.8))
        self.play(FadeIn(key), run_time=0.6)
        bax = T("Bax-null ganglion", 30, TEXT).move_to(P(0, 2.75))
        self.at("this was tested")
        self.play(FadeIn(bax, shift=DOWN * 0.15), run_time=0.7)
        self.finish()


class S14(SpokenScene):
    def construct(self):
        self.add(head_text(), tag(2), g_outline(), g_cells(True), g_legend()[0], schem_tag(4.95, 2.8))
        bax = T("Bax-null ganglion", 30, TEXT).move_to(P(0, 2.75))
        self.add(bax)
        cells = g_cells(True)
        dims = VGroup(*[cells[i] for i in G_DIM])
        self.play(FadeOut(bax), run_time=0.4)
        lowl = T("low TrkA neurons", 30, PURPLE).move_to(P(0, 2.75))
        self.at("neurons with low")
        self.play(FadeIn(lowl), Indicate(dims, color=PURPLE, scale_factor=1.25), run_time=1.0)
        rings = g_rings()
        self.at("show high")
        self.play(LaggedStart(*[FadeIn(r, scale=0.6) for r in rings], lag_ratio=0.06), run_time=1.1)
        hi = T("high p75 death signaling", 30, TEAL).move_to(P(0, 2.75))
        self.at("death signaling")
        self.play(FadeOut(lowl), FadeIn(hi), run_time=0.5)
        a, b, c, row = g_legend(True)
        self.at("read out by")
        self.play(FadeIn(c, shift=UP * 0.15), run_time=0.7)
        self.at("phosphorylated")
        self.play(*[Indicate(r, color=TEAL, scale_factor=1.2) for r in rings], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
NX, NY, NR = -2.2, -0.3, 3.45    # the one big neuron of scene 15


def chain_boxes():
    p = chip("p75", TEAL, 56, pad=0.25)
    p[0].set_fill(BG, 1.0)
    p[0].set_stroke(TEAL, width=5)
    j = chip("JNK", TEAL, 56, pad=0.25, fill_opacity=0.3)
    c = chip("c-Jun", TEAL, 56, pad=0.25, fill_opacity=0.3)
    x = chip("death", RED, 56, pad=0.25, fill_opacity=0.5)
    p.move_to(P(NX, NY + NR))
    j.move_to(P(NX, NY + NR - 1.75))
    c.move_to(P(NX, NY + NR - 3.45))
    x.move_to(P(NX, NY + NR - 5.15))
    return p, j, c, x


class S15(SpokenScene):
    def construct(self):
        self.add(tag(2))
        p, j, c, x = chain_boxes()
        cell = Circle(radius=NR, stroke_color=BLUE, stroke_width=8, fill_opacity=0).move_to(P(NX, NY))
        self.play(FadeIn(cell), FadeIn(c, scale=0.6), run_time=0.8)
        cap = left_text("transcription factor", 36, TEXT, 1.9, c.get_center()[1])
        lead = Line(c.get_right() + RIGHT * 0.1, P(1.8, c.get_center()[1]), color=GREY, stroke_width=3)
        self.at("transcription factor")
        self.play(FadeIn(cap, shift=RIGHT * 0.15), Create(lead), run_time=0.7)
        capj = left_text("stress kinase", 36, TEXT, 1.9, j.get_center()[1])
        leadj = Line(j.get_right() + RIGHT * 0.1, P(1.8, j.get_center()[1]), color=GREY, stroke_width=3)
        self.at("stress kinase")
        self.play(FadeIn(j, scale=0.6), FadeIn(capj, shift=RIGHT * 0.15), Create(leadj), run_time=0.8)
        a1 = arr(p.get_bottom() + DOWN * 0.08, j.get_top() + UP * 0.08, TEAL, 8, 0.3)
        self.at("p75")
        self.play(FadeIn(p, scale=0.6), GrowArrow(a1), run_time=0.9)
        a2 = arr(j.get_bottom() + DOWN * 0.08, c.get_top() + UP * 0.08, TEAL, 8, 0.3)
        self.at("helps activate")
        self.play(GrowArrow(a2), Indicate(c, color=TEAL, scale_factor=1.1), run_time=1.0)
        a3 = arr(c.get_bottom() + DOWN * 0.08, x.get_top() + UP * 0.08, RED, 8, 0.3)
        self.at("way to death")
        self.play(GrowArrow(a3), FadeIn(x), cell.animate.set_stroke(RED, width=8), run_time=0.35)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        self.add(tag(3))
        top = chip("p75-null mouse", TEAL, 44).move_to(P(0, 3.0))
        pre = T("prediction", 30, GOLD).move_to(P(4.9, 3.0))
        self.play(FadeIn(top, shift=DOWN * 0.2), FadeIn(pre), run_time=0.8)
        # row A: the punishment signal removed
        pun = chip("punishment through p75", ORANGE, 40).move_to(P(-1.3, 1.1))
        rem = T("removed", 44, TEXT).move_to(P(4.1, 1.1))
        self.at("removing punishment")
        self.play(FadeIn(pun, shift=RIGHT * 0.2), run_time=0.6)
        cross = Line(pun.get_left() + RIGHT * 0.1, pun.get_right() + LEFT * 0.1, color=RED, stroke_width=9)
        self.play(Create(cross), FadeIn(rem, shift=LEFT * 0.2), run_time=0.6)
        # row B: the loss comes later
        arrow_b = arr(P(-5.2, -0.5), P(-3.7, -0.5), GREY, 7, 0.3)
        lab_b = T("the loss comes later", 46, TEXT).move_to(P(0.3, -0.5))
        self.at("delay the loss")
        self.play(GrowArrow(arrow_b), FadeIn(lab_b, shift=RIGHT * 0.2), run_time=0.8)
        # row C: but it is not prevented
        lab_c = T("but is not prevented", 46, GOLD).move_to(P(0, -2.1))
        self.at("but not prevent it")
        self.play(FadeIn(lab_c, shift=UP * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S17(SpokenScene):
    def construct(self):
        ax = plot_axes()
        self.at("neuron number")
        self.play(Create(ax), FadeIn(ylabel()), FadeIn(yticks()), run_time=0.9)
        self.at("against age")
        self.play(FadeIn(xticks()), run_time=0.8)
        d, lb = start_marks()
        self.at("normal mice")
        self.play(FadeIn(leg(0, TEXT, "normal")), FadeIn(d, scale=0.4), FadeIn(lb), run_time=0.7)
        self.at("in mice lacking")
        self.play(FadeIn(leg(1, TEAL, "p75-null")), run_time=0.6)
        g, p = question_texts()
        self.at("what does the second curve do")
        self.play(FadeIn(g, shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(p), run_time=0.4)
        self.finish()


class S18Pause(NarratedScene):
    def construct(self):
        question_frame(self)
        self.wait(5.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19(SpokenScene):
    def construct(self):
        plot_base(self)
        st = dot(P(wx(0), ny(1.0)), TEXT, 0.16)
        st2 = Circle(radius=0.27, stroke_color=TEAL, stroke_width=5, fill_opacity=0).move_to(st)
        lb = left_text("both start here", 26, TEXT, wx(0) + 0.45, ny(1.0) + 0.45)
        self.add(st)
        self.at("both start")
        self.play(FadeIn(st2, scale=0.4), FadeIn(lb), Indicate(st, color=TEXT, scale_factor=2.0), run_time=1.2)
        c = curve(Nw, TEXT)
        self.at("normal curve falls")
        self.play(FadeOut(lb), Create(c), run_time=1.6, rate_func=linear)
        seg = curve(Nw, GOLD, w=12, t0=0.0, t1=1.0)
        mid = wx(0.3), ny(Nw(0.3))
        lab = T("first days after birth", 28, GOLD).move_to(P(-0.4, 1.9))
        lead = Line(P(mid[0] + 0.2, mid[1] + 0.12), lab.get_left() + LEFT * 0.12, color=GOLD, stroke_width=4)
        self.at("first days")
        self.play(Create(seg), FadeIn(lab), Create(lead), run_time=0.9)
        self.finish()


class S20(SpokenScene):
    def construct(self):
        plot_base(self)
        st = dot(P(wx(0), ny(1.0)), TEXT, 0.16)
        self.add(st, curve(Nw, TEXT))
        cn = curve(Nn, TEAL)
        self.at("falls more slowly")
        self.play(Create(cn), run_time=2.0, rate_func=linear)
        band = gap_band(Nn, Nw, 0.0, TEND, TEAL, 0.28)
        self.at("so for a while")
        self.play(FadeIn(band), run_time=0.8)
        lb = T("more neurons, for a while", 30, TEAL).move_to(P(-0.8, 2.45))
        lead = Line(P(-3.0, 2.15), P(wx(1.6), ny(0.5 * (Nn(1.6) + Nw(1.6))) + 0.2), color=TEAL, stroke_width=4)
        self.at("more neurons")
        self.play(FadeIn(lb, shift=DOWN * 0.1), Create(lead), run_time=0.7)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        plot_base(self)
        st = dot(P(wx(0), ny(1.0)), TEXT, 0.16)
        band = gap_band(Nn, Nw, 0.0, TEND, TEAL, 0.2)
        self.add(st, band, curve(Nw, TEXT), curve(Nn, TEAL))
        # a row of weak neurons that fades slowly
        row = VGroup(*[dot(P(0.2 + 0.55 * k, 0.15), RED, 0.17) for k in range(7)])
        rl = T("losers (weak neurons)", 28, RED).move_to(P(1.7, -0.45))
        self.at("losers still die")
        self.play(FadeIn(row, scale=0.6), FadeIn(rl), run_time=0.5)
        fades = [row[k].animate.set_fill(RED, opacity=0.15).set_stroke(RED, opacity=0.2) for k in (6, 5, 4)]
        self.play(LaggedStart(*fades, lag_ratio=0.5), run_time=0.45)
        ng = chip("too little NGF", YELLOW, 28).move_to(P(0.9, 2.35))
        self.at("too little")
        self.play(FadeIn(ng, shift=DOWN * 0.15),
                  *[row[k].animate.set_fill(RED, opacity=0.15).set_stroke(RED, opacity=0.2) for k in (3,)], run_time=0.8)
        bx = chip("Bax", RED, 28).move_to(P(3.7, 2.35))
        ar = arr(P(2.4, 2.35), P(3.15, 2.35), GREY, 5, 0.22)
        self.at("through")
        self.play(GrowArrow(ar), FadeIn(bx, shift=LEFT * 0.15),
                  *[row[k].animate.set_fill(RED, opacity=0.15).set_stroke(RED, opacity=0.2) for k in (2,)], run_time=0.8)
        ep = chip("extra push", ORANGE, 28).move_to(P(0.9, 1.3))
        self.at("only the extra push")
        self.play(FadeIn(ep), run_time=0.6)
        cross = Line(ep.get_left() + RIGHT * 0.12, ep.get_right() + LEFT * 0.12, color=RED, stroke_width=8)
        self.play(Create(cross), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S22(SpokenScene):
    def construct(self):
        shells = [card_shell(i) for i in range(3)]
        nums = [card_num(i) for i in range(3)]
        t1 = [card_b1(i) for i in range(3)]
        t2 = [card_b2(i) for i in range(3)]
        self.play(*[FadeIn(m) for m in shells + nums + t1 + t2], run_time=0.6)
        ticks = [tick_mark(P(CX[i], CY - 2.5), GREEN, 1.1) for i in range(3)]
        self.at("predictions held")
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.35), run_time=1.0)
        self.at("including the delay")
        self.play(Indicate(VGroup(shells[2], t1[2], t2[2], ticks[2]), color=GREEN, scale_factor=1.05), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
LX0, LX1, RX0, RX1 = -6.7, -0.15, 0.15, 6.7
MY0, MY1 = -2.4, 2.3
YB, YT = MY0 + 0.45, MY1 - 0.85     # y of zero neurons alive, y of all alive
TL, TR = 0.9, 4.3                    # curves run from x0+TL to x0+TR


def mpan(x0, x1, title, tcol):
    fr = Rectangle(width=x1 - x0, height=MY1 - MY0, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                   fill_opacity=0.05).move_to(P((x0 + x1) / 2, (MY0 + MY1) / 2))
    t = T(title, 32, tcol).move_to(P((x0 + x1) / 2, MY1 + 0.5))
    base = Line(P(x0 + TL - 0.15, YB), P(x0 + TR + 0.15, YB), color=GREY, stroke_width=3)
    yl = T("neurons alive", 26, GREY).rotate(PI / 2).move_to(P(x0 + 0.4, (YB + YT) / 2))
    tm = T("time", 26, GREY).move_to(P(x0 + (TL + TR) / 2, MY0 - 0.35))
    return VGroup(fr, t, base, yl, tm)


def model_curves(x0, p):
    """Surviving fraction of the five losers: dL/dt = -(a_i + p g(t)) L, g rising from 0 to 1."""
    ts = np.linspace(0, 3.0, 160)
    g = 1 - np.exp(-ts / 0.5)
    outs, ends = [], []
    for a in (0.3, 0.4, 0.5, 0.6, 0.7):
        L = np.empty_like(ts)
        L[0] = 1.0
        for k in range(1, len(ts)):
            dt = ts[k] - ts[k - 1]
            L[k] = L[k - 1] * np.exp(-(a + p * g[k - 1]) * dt)
        pts = [P(x0 + TL + (TR - TL) * t / 3.0, YB + L[k] * (YT - YB)) for k, t in enumerate(ts)]
        outs.append(VMobject(stroke_color=RED, stroke_width=4).set_points_smoothly(pts[::4] + [pts[-1]]))
        ends.append(pts[-1][1])
    return outs, float(np.mean(ends))


def model_winners(x0):
    return [Line(P(x0 + TL, YT + dy), P(x0 + TR, YT + dy), color=GREEN, stroke_width=5) for dy in (0.0, 0.1)]


class S23(SpokenScene):
    def construct(self):
        pl, pr = mpan(LX0, LX1, "with punishment", ORANGE), mpan(RX0, RX1, "without punishment", TEAL)
        tg = T("schematic model runs", 26, GOLD).move_to(P(0, -3.55))
        self.play(FadeIn(pl), FadeIn(pr), FadeIn(tg), run_time=0.9)
        wl, wr = model_winners(LX0), model_winners(RX0)
        self.add(*wl, *wr)
        for x0 in (LX0, RX0):
            self.add(T("winners", 26, GREEN).move_to(P(x0 + TR + 1.0, YT + 0.05)))
        self.at("punishment made")
        cl, ml = model_curves(LX0, 3.0)
        self.play(*[Create(c, rate_func=linear) for c in cl], FadeIn(T("losers", 26, RED).move_to(P(LX0 + TR + 0.95, ml))),
                  run_time=1.3)
        self.at("without it")
        cr, mr = model_curves(RX0, 0.0)
        self.play(*[Create(c, rate_func=linear) for c in cr], FadeIn(T("losers", 26, RED).move_to(P(RX0 + TR + 0.95, mr))),
                  run_time=0.8)
        self.at("weak neurons lingered")
        self.play(Indicate(VGroup(*cr), color=RED, scale_factor=1.03), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def base_curves(sc):
    """State at the end of scene 21: the first two months."""
    st = dot(P(wx(0), ny(1.0)), TEXT, 0.16)
    sc.add(st, curve(Nw, TEXT), curve(Nn, TEAL))


def lab2008(endp, extra=False):
    """The 2008 label sits just under the end of its curve (same place in scenes 24 to 26)."""
    l1 = T("2008 study", 26, TEAL).move_to(P(endp[0], endp[1] - 0.55))
    out = [l1]
    if extra:
        out.append(T("normal number", 28, TEXT).move_to(P(endp[0], endp[1] - 0.88)))
    return out


class S24(SpokenScene):
    def construct(self):
        plot_base(self)
        base_curves(self)
        endp = P(wx(T6M), ny(Nn(T6M)))
        q = T("endpoint: less settled", 32, GOLD).move_to(P(1.0, 1.0))
        self.at("less settled")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.7)
        lab = lab2008(endp)[0]
        self.at("2008 study")
        self.play(FadeOut(q), run_time=0.5)
        ext_n = curve(Nn, TEAL, t0=TEND, t1=T6M)
        ext_w = curve(Nw, TEXT, t0=TEND, t1=T6M)
        self.at("null ganglion")
        self.play(Create(ext_w), Create(ext_n), run_time=1.9, rate_func=linear)
        meet = Circle(radius=0.25, stroke_color=GOLD, stroke_width=6, fill_opacity=0).move_to(endp)
        self.at("6 months")
        self.play(FadeIn(meet, scale=2.5), FadeIn(lab, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


def end_state_2008(sc, extra=False):
    """The 2008 curve to six months, with its end label, as left by scene 24."""
    plot_base(sc)
    st = dot(P(wx(0), ny(1.0)), TEXT, 0.16)
    endp = P(wx(T6M), ny(Nn(T6M)))
    meet = Circle(radius=0.25, stroke_color=GOLD, stroke_width=6, fill_opacity=0).move_to(endp)
    sc.add(st, curve(Nw, TEXT, t1=T6M), curve(Nn, TEAL, t1=T6M), meet, *lab2008(endp, extra))
    nl = T("normal", 28, TEXT).move_to(P(wx(TAX) + 0.55 + 0.4, ny(Nw(TAX))))
    return nl


class S25(SpokenScene):
    def construct(self):
        nl = end_state_2008(self)
        self.add(curve(Nw, TEXT, t0=T6M, t1=TAX), nl)
        endm = P(wx(TAX), ny(Nm(TAX)))
        dsh = curve(Nm, TEAL, w=6, dashed=True, t1=TAX)
        l1 = left_text("earlier study", 28, TEAL, endm[0] + 0.3, endm[1] + 0.2)
        self.at("earlier study")
        self.play(Create(dsh), FadeIn(l1), run_time=2.2, rate_func=linear)
        l2 = left_text("Miller laboratory", 28, TEAL, endm[0] + 0.3, endm[1] - 0.25)
        self.at("laboratory")
        self.play(FadeIn(l2, shift=DOWN * 0.1), run_time=0.6)
        self.at("found the loss delayed")
        self.play(ShowPassingFlash(curve(Nm, GOLD, w=12, t1=12), time_width=0.8), run_time=1.2)
        band = gap_band(Nm, Nw, 20.0, TAX, TEAL, 0.25)
        ex = T("excess", 30, TEAL).move_to(P(wx(30.0), ny(0.5 * (Nm(30.0) + Nw(30.0)))))
        self.at("excess")
        self.play(FadeIn(band), FadeIn(ex), run_time=0.7)
        ad = Line(P(wx(TAX), PY0), P(wx(TAX), PY1 - 0.1), color=GOLD, stroke_width=4)
        adt = T("adult", 26, GOLD).move_to(P(wx(TAX), PY0 - 0.45))
        self.at("adulthood")
        self.play(Create(ad), FadeIn(adt), run_time=0.7)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        nl = end_state_2008(self)
        v1 = lab2008(P(wx(T6M), ny(Nn(T6M))), True)[1]
        self.add(curve(Nw, TEXT, t0=T6M, t1=TAX), nl)
        endm = P(wx(TAX), ny(Nm(TAX)))
        self.add(curve(Nm, TEAL, w=6, dashed=True, t1=TAX),
                 left_text("earlier study", 28, TEAL, endm[0] + 0.3, endm[1] + 0.2),
                 left_text("Miller laboratory", 28, TEAL, endm[0] + 0.3, endm[1] - 0.25))
        self.add(gap_band(Nm, Nw, 20.0, TAX, TEAL, 0.12))
        lb = T("both: the loss is delayed", 32, GOLD).move_to(P(-0.2, 2.35))
        self.at("both found")
        self.play(FadeIn(lb, shift=DOWN * 0.15), run_time=0.7)
        xa = wx(36.0)
        da = DoubleArrow(P(xa, ny(Nw(36.0)) + 0.12), P(xa, ny(Nm(36.0)) - 0.12), color=GOLD, buff=0, stroke_width=6,
                         tip_length=0.2)
        ymid = 0.5 * (ny(Nw(36.0)) + ny(Nm(36.0)))
        dl = VGroup(T("differ at the", 28, GOLD), T("latest ages", 28, GOLD)).arrange(DOWN, buff=0.1, aligned_edge=RIGHT)
        dl.move_to(P(xa - 0.35 - dl.width / 2, ymid))
        v2 = left_text("excess", 28, TEXT, endm[0] + 0.3, endm[1] - 0.7)
        self.at("different numbers")
        self.play(GrowFromCenter(da), FadeIn(dl), run_time=1.0)
        self.at("latest ages")
        self.play(FadeIn(v1), FadeIn(v2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
S27_Y = [1.8, -0.42, -2.64]
ROW_H = 2.16


def srow(i):
    return RoundedRectangle(corner_radius=0.15, width=12.9, height=ROW_H, stroke_color=GREY, stroke_width=2.5,
                            fill_color=GREY, fill_opacity=0.06).move_to(P(0, S27_Y[i]))


class S27(SpokenScene):
    def construct(self):
        hd = T("Takeaway", 64, GOLD, weight=BOLD).move_to(P(0, 0.2))
        self.play(FadeIn(hd, scale=0.8), run_time=0.7)
        hd_small = T("Takeaway", 40, GOLD).move_to(P(0, 3.4))
        # row 1: winners punish losers through p75
        y = S27_Y[0]
        g1 = soma(P(-5.7, y), GREEN, 0.62, 0.7)
        r1 = soma(P(-3.0, y), RED, 0.5, 0.35)
        rc = recep(P(-3.0, y), 0.5, 180, TEAL)
        a1 = arr(P(-4.9, y), P(-3.85, y), ORANGE, 7, 0.28)
        g1g = VGroup(g1, a1, r1, rc)
        t0 = left_text("in the proposed model", 32, SOFT, -2.3, y + 0.68)
        t1 = left_text("winners speed the death of losers", 37, TEXT, -2.3, y)
        t2 = left_text("through p75", 40, TEAL, -2.3, y - 0.68)
        self.at("in the proposed model")
        self.play(Transform(hd, hd_small), FadeIn(srow(0)), FadeIn(g1g), FadeIn(t0), run_time=1.0)
        self.at("winners")
        self.play(FadeIn(t1, shift=RIGHT * 0.2), run_time=0.7)
        self.at("through")
        self.play(FadeIn(t2, shift=RIGHT * 0.2), Indicate(rc, color=TEAL, scale_factor=1.4), run_time=0.7)
        # row 2: without p75, delayed
        y = S27_Y[1]
        bx0, bx1 = -6.1, -2.4
        mini = VGroup(Line(P(bx0, y - 0.75), P(bx1, y - 0.75), color=GREY, stroke_width=3),
                      Line(P(bx0, y - 0.75), P(bx0, y + 0.8), color=GREY, stroke_width=3))
        us = np.linspace(0, 1, 70)

        def mc(fn, col):
            pts = [P(bx0 + 0.1 + (bx1 - bx0 - 0.3) * u, y - 0.7 + 1.45 * (fn(8.0 * u * u) - 0.45) / 0.58) for u in us]
            return VMobject(stroke_color=col, stroke_width=5).set_points_smoothly(pts)

        cw, cn = mc(Nw, TEXT), mc(Nn, TEAL)
        u0 = left_text("without p75", 32, SOFT, -1.9, y + 0.4)
        u1 = left_text("the loss is delayed", 42, TEXT, -1.9, y - 0.3)
        self.at("without it")
        self.play(FadeIn(srow(1)), FadeIn(mini), FadeIn(u0), run_time=0.8)
        self.at("the loss is delayed")
        self.play(FadeIn(u1, shift=RIGHT * 0.2), Create(cw), Create(cn), run_time=1.3)
        # row 3: endpoint less settled
        y = S27_Y[2]
        qm = T("?", 100, GOLD, weight=BOLD).move_to(P(-4.2, y))
        v0 = left_text("whether any neurons are", 40, TEXT, -1.9, y + 0.68)
        v1 = VGroup(left_text("permanently spared", 40, TEXT, -1.9, y),
                    left_text("is less settled", 40, TEXT, -1.9, y - 0.68))
        self.at("whether any")
        self.play(FadeIn(srow(2)), FadeIn(qm, scale=0.5), FadeIn(v0, shift=RIGHT * 0.2), run_time=0.9)
        self.at("permanently spared")
        self.play(FadeIn(v1, shift=RIGHT * 0.2), run_time=0.7)
        self.at("less settled")
        self.play(Indicate(qm, color=GOLD, scale_factor=1.25), run_time=0.9)
        self.finish()


class S28End(EndCard):
    LINE = "In the proposed model, winners speed losers' death through p75."
