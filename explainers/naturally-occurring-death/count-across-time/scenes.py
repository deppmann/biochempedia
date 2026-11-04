"""Too Many Neurons: Naturally Occurring Cell Death -- chapter 2: Count Across Time (Biochemistrypedia)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by every chapter of this film)
  BLUE   = motor neurons that are present / healthy, and the control (intact) side; also "things that are counted"
  RED    = dying or lost neurons, the loss (also: what is thrown away in the bakery picture)
  YELLOW = the manipulated limb side (operated side, grafted extra leg) and the limb itself
  GREY   = axes, outlines, hypotheses, de-emphasized things
  TEAL   = the "pause and sketch" cue
  Two pale hypothesis tints (lavender, sage) tell the two faint predictions apart in s25 to s27; a tan "paper" and
  dark "ink" draw the schematic stained sections in s17 and s18.
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

PAPER = "#CDBE98"   # stained-section background (schematic of a silver-stained slide)
INK = "#2A2118"     # stained neurons in that schematic
DARK = "#12080A"    # a shrunken, dark nucleus
LGREY = "#B7BBC4"   # credit lines: lighter than GREY so they read on the dark ground
PRED_A = "#A99BCB"  # faint prediction 1 (more births)
PRED_B = "#86C4A4"  # faint prediction 2 (fewer deaths)


# =============================================================================================
# helpers
# =============================================================================================
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def smooth(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


class Plot:
    """a plot frame: origin lower left, u and v run 0..1 across the frame."""

    def __init__(self, x0, y0, w, h):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h

    def P(self, u, v):
        return np.array([self.x0 + u * self.w, self.y0 + v * self.h, 0.0])

    def axes(self, top=1.08):
        return VGroup(Line(self.P(0, 0), self.P(1.0, 0), color=GREY, stroke_width=3),
                      Line(self.P(0, 0), self.P(0, top), color=GREY, stroke_width=3))

    def curve(self, fn, u0, u1, color, w=6, n=70):
        pts = [self.P(u, fn(u)) for u in np.linspace(u0, u1, n)]
        return VMobject(stroke_color=color, stroke_width=w, fill_opacity=0).set_points_as_corners(pts)


def lattice(cx, cy, a, b, sp, seed=1, jitter=0.04):
    rnd = random.Random(seed)
    pts = []
    for r, yy in enumerate(np.arange(-b, b + 0.001, sp * 0.866)):
        for xx in np.arange(-a, a + 0.001, sp):
            xo = xx + (sp / 2 if r % 2 else 0)
            if (xo / a) ** 2 + (yy / b) ** 2 <= 1:
                pts.append([cx + xo + rnd.uniform(-jitter, jitter), cy + yy + rnd.uniform(-jitter, jitter), 0])
    return pts


def tick_row(pl, color=GREY, n=9, w=3, drop=0.16):
    return VGroup(*[Line(pl.P(u, 0), pl.P(u, 0) + DOWN * drop, color=color, stroke_width=w)
                    for u in np.linspace(0.06, 0.94, n)])


# ---- a dorsal-view chick embryo (a cartoon; no anatomy beyond what the film names) ------------
def embryo(cx, cy, s=1.0, wings=False, legs=False, extra_leg=False, bud_stroke=4):
    ys = [1.0, 0.94, 0.84, 0.72, 0.62, 0.52, 0.3, 0.0, -0.4, -0.7, -0.9, -1.0]
    ws = [0.10, 0.36, 0.46, 0.44, 0.30, 0.30, 0.42, 0.50, 0.45, 0.28, 0.14, 0.10]
    yy = np.linspace(1, -1, 50)
    w = np.interp(yy, ys[::-1], ws[::-1])
    hx, hy = 2.1 * s, 3.0 * s
    right = [[cx + wi * hx, cy + y * hy, 0] for y, wi in zip(yy, w)]
    left = [[cx - wi * hx, cy + y * hy, 0] for y, wi in zip(yy[::-1], w[::-1])]
    pts = right + left
    body = VMobject(stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.14)
    body.set_points_smoothly(pts + [pts[0]])

    def bud(x, y):
        return Ellipse(width=1.0 * s, height=0.78 * s, stroke_color=YELLOW, stroke_width=bud_stroke,
                       fill_color=YELLOW, fill_opacity=0.3).move_to([x, y, 0])

    d = dict(body=body)
    if wings:
        d["wing_l"] = bud(cx - 1.15 * s, cy + 0.9 * s)
        d["wing_r"] = bud(cx + 1.15 * s, cy + 0.9 * s)
    if legs:
        d["leg_l"] = bud(cx - 1.12 * s, cy - 1.15 * s)
        d["leg_r"] = bud(cx + 1.12 * s, cy - 1.15 * s)
    if extra_leg:
        d["extra"] = bud(cx + 1.12 * s, cy - 2.15 * s)
    return d


# ---- spinal cord cross-section: more neurons on the intact side than on the operated side ------
CORD_CX, CORD_CY = 0.0, 0.3


def cord_section():
    cx, cy = CORD_CX, CORD_CY
    outline = Ellipse(width=8.0, height=5.0, stroke_color=GREY, stroke_width=3).move_to([cx, cy, 0])
    mid = DashedLine([cx, cy - 2.4, 0], [cx, cy + 2.4, 0], color=GREY, stroke_width=2)
    hl = Ellipse(width=2.9, height=2.4, stroke_color=GREY, stroke_width=2, fill_color=BLUE,
                 fill_opacity=0.07).move_to([cx - 1.85, cy - 0.3, 0])
    hr = Ellipse(width=2.9, height=2.4, stroke_color=GREY, stroke_width=2, fill_color=BLUE,
                 fill_opacity=0.07).move_to([cx + 1.85, cy - 0.3, 0])
    ptsL = lattice(cx - 1.85, cy - 0.3, 1.1, 0.88, 0.5, seed=3)
    rnd = random.Random(11)
    keep = set(rnd.sample(range(len(ptsL)), len(ptsL) // 2))
    ptsR = [[2 * cx - p[0], p[1], 0] for i, p in enumerate(ptsL) if i in keep]
    dotsL = VGroup(*[Dot(p, radius=0.17, color=BLUE) for p in ptsL])
    dotsR = VGroup(*[Dot(p, radius=0.17, color=BLUE) for p in ptsR])
    lab_in = T("intact side", 32, BLUE).move_to([cx - 1.85, -2.7, 0])
    lab_op = T("operated side", 32, YELLOW).move_to([cx + 1.85, -2.7, 0])
    lab_ctrl = T("control", 30, GREY).move_to([cx - 1.85, -3.2, 0])
    return dict(outline=outline, mid=mid, hl=hl, hr=hr, dotsL=dotsL, dotsR=dotsR, lab_in=lab_in,
                lab_op=lab_op, lab_ctrl=lab_ctrl)


def cord_all(c):
    return VGroup(c["outline"], c["mid"], c["hl"], c["hr"], c["dotsL"], c["dotsR"], c["lab_in"], c["lab_op"],
                  c["lab_ctrl"])


CORD_S, CORD_X, CORD_Y = 0.86, -3.3, 0.0   # the cord section grows to this size and moves left in s04 and s05


def cord_small():
    return cord_all(cord_section()).scale(CORD_S).move_to([CORD_X, CORD_Y, 0])


def limb_items(g):
    """The limb, arrow and labels beside a (shrunken) cord group g, laid out for s04 and s05."""
    hy = g[3].get_center()[1] + 0.3          # the operated-side horn is the right-hand one (g[3])
    limb = Ellipse(width=3.0, height=2.6, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                   fill_opacity=0.25).move_to([5.05, hy, 0])
    limb_l = T("limb", 36, YELLOW).move_to(limb)
    a = arr([3.55, hy, 0], [0.3, hy, 0], YELLOW, 6)
    lab = VGroup(T("sets how many", 32), T("are made?", 32)).arrange(DOWN, buff=0.1).move_to([1.95, hy + 1.05, 0])
    lab2 = VGroup(T("(Hamburger's", 28, LGREY), T("reading)", 28, LGREY)).arrange(DOWN, buff=0.08).move_to([1.95, hy - 1.05, 0])
    return limb, limb_l, a, lab, lab2


# ---- the bakery shelf ---------------------------------------------------------------------------
def loaf(x, y, w, h, color=BLUE, op=0.5):
    return RoundedRectangle(corner_radius=min(w, h) * 0.34, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def shelf(cx, cy, k, vs=1.0):
    """Eight slots: four hold loaves, four are empty (dashed). k scales everything but stroke widths; vs stretches
    the loaves upward. cy is the loaves' centre line."""
    lw, lh = 1.18 * k, 1.1 * k * vs
    yb = cy - lh / 2 - 0.12 * k
    px = 5.75 * k
    ytop = cy + lh / 2 + 0.5 * k
    frame = VGroup(Line([cx - px, yb, 0], [cx + px, yb, 0], color=GREY, stroke_width=6),
                   Line([cx - px, yb, 0], [cx - px, ytop, 0], color=GREY, stroke_width=4),
                   Line([cx + px, yb, 0], [cx + px, ytop, 0], color=GREY, stroke_width=4))
    sp = 1.38 * k
    loaves = VGroup(*[loaf(cx + (i - 3.5) * sp, cy, lw, lh) for i in range(4)])
    slots = VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=min(lw, lh) * 0.34, width=lw, height=lh,
                                                     stroke_color=GREY, stroke_width=2).move_to(
        [cx + (i - 3.5) * sp, cy, 0]), num_dashes=14) for i in range(4, 8)])
    return dict(frame=frame, loaves=loaves, slots=slots, group=VGroup(frame, loaves, slots),
                sp=sp, ly=cy, lw=lw, lh=lh, cx=cx)


BIG_K, BIG_VS, BIG_Y = 1.1, 1.65, -0.15
SM_K, SM_X = 0.6, -3.1
LAY = {1: [0.1], 2: [1.55, -1.55], 3: [2.4, 0.0, -2.4], 4: [2.7, 0.9, -0.9, -2.7]}
CHIP_X = 2.95   # left edge of every row label


def big_shelf():
    return shelf(0, BIG_Y, BIG_K, BIG_VS)


def row(i, y):
    """Small shelf i with what is drawn to its right and its label, built with its loaf line at height y."""
    sh = shelf(SM_X, y, SM_K)
    ly = y
    if i == 0:
        ex, ch = VGroup(), bchip("baked fewer", GREY, 26)
    elif i == 1:
        a = arr([0.55, ly, 0], [1.05, ly, 0], GREY, 4, 0.16)
        small = VGroup(*[loaf(1.3 + j * 0.38, ly, 0.3, 0.28, GREY, 0.35) for j in range(4)])
        ex, ch = VGroup(a, small), bchip("sent away", GREY, 26)
    elif i == 2:
        rolls = VGroup(*[Circle(radius=0.16, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35)
                         .move_to([0.95 + j * 0.4, ly, 0]) for j in range(4)])
        ex, ch = VGroup(rolls), bchip("came out as rolls", GREY, 26)
    else:
        bin_ = Rectangle(width=2.0, height=0.7, stroke_color=GREY, stroke_width=3).move_to([1.75, ly, 0])
        ex, ch = VGroup(bin_), bchip("thrown out", RED, 26)
    ch.move_to([CHIP_X + ch.width / 2, y, 0])
    return dict(sh=sh, ex=ex, ch=ch, all=VGroup(sh["group"], ex, ch))


def bar_items(cx, base, h=2.4, w=2.6, ghost_h=2.4):
    bar = Rectangle(width=w, height=h, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                    fill_opacity=0.5).move_to([cx, base + h / 2, 0])
    ghost = DashedVMobject(Rectangle(width=w, height=ghost_h, stroke_color=GREY, stroke_width=3)
                           .move_to([cx, base + h + ghost_h / 2, 0]), num_dashes=40)
    q = T("?", 90, GREY, weight=BOLD).move_to([cx, base + h + ghost_h / 2, 0])
    return bar, ghost, q


# ---- big blank axis for "pause and sketch" (s10 to s12) ----------------------------------------------
BP = Plot(-5.4, -3.0, 10.8, 5.0)


def predict_pieces():
    axes = BP.axes(1.0)
    ylab = T("count", 28, GREY).rotate(PI / 2).move_to([-5.85, -0.5, 0])
    xlab = T("time", 28, GREY).move_to([5.4 - 0.5, -3.45, 0])
    prompt = bchip("Pause and sketch", TEAL, 30).move_to([0, 3.4, 0])
    q1 = T("What would you count, and when,", 32).move_to([0, 2.8, 0])
    q2 = T("to tell never made from made, then lost?", 32).move_to([0, 2.35, 0])
    return axes, ylab, xlab, prompt, q1, q2


# ---- the two stacked panels used for the time-course schematics (s12 to s16) ----------------------
HP = Plot(-4.9, -0.45, 10.2, 3.0)
DP = Plot(-4.9, -3.15, 10.2, 1.8)


def f_in(u):
    return 0.55 + 0.38 * smooth(u / 0.3)


def f_never(u):
    return 0.5 * f_in(u)


def loss(u):
    return 0.45 * smooth((u - 0.38) / 0.30)


def f_lost(u):
    return f_in(u) * (1 - loss(u))


def death_rate(u):
    e = 1e-3
    return max(0.0, -(f_lost(u + e) - f_lost(u - e)) / (2 * e))


_HMAX = max(death_rate(u) for u in np.linspace(0, 1, 400))


def hump_h(u):
    return 0.85 * death_rate(u) / _HMAX


def panels(tag=False):
    d = {}
    d["up_axes"] = HP.axes(1.05)
    d["lp_axes"] = DP.axes(1.1)
    d["up_ticks"] = tick_row(HP)
    d["lp_ticks"] = tick_row(DP)
    d["lab_up"] = T("healthy neurons", 28, BLUE).move_to([-4.9, 3.1, 0], aligned_edge=LEFT)
    lab_lp = T("dying neurons", 28, RED).move_to([-4.9, -0.95, 0], aligned_edge=LEFT)
    d["lab_lp"] = lab_lp
    if tag:
        d["lab_tag"] = T("operated side", 28, YELLOW).next_to(lab_lp, RIGHT, buff=0.3)
    d["ylab_up"] = T("count", 26, GREY).rotate(PI / 2).move_to([-5.35, HP.P(0, 0.5)[1], 0])
    d["ylab_lp"] = T("count", 26, GREY).rotate(PI / 2).move_to([-5.35, DP.P(0, 0.5)[1], 0])
    d["xlab"] = T("time (stages)", 26, GREY).move_to([5.3, -3.62, 0], aligned_edge=RIGHT)
    d["sch"] = T("schematic, not data", 26, GREY).move_to([-5.0, -3.62, 0], aligned_edge=LEFT)
    c_op = bchip("operated side", YELLOW, 26)
    c_in = bchip("intact side", BLUE, 26)
    leg = VGroup(c_op, c_in).arrange(RIGHT, buff=0.3)
    leg.move_to([6.5 - leg.width / 2, 3.35, 0])
    d["legend"] = leg
    return d


def side_note():
    return T("intact side: normal loss not drawn", 26, GREY).move_to([6.5, 2.7, 0], aligned_edge=RIGHT)


def panels_group(d):
    return VGroup(*d.values())


def hump_poly():
    us = np.linspace(0.30, 0.80, 60)
    pts = [DP.P(0.30, 0)] + [DP.P(u, hump_h(u)) for u in us] + [DP.P(0.80, 0)]
    return VMobject(stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.35).set_points_as_corners(pts)


def gap_bracket(pl, u, v0, v1, color=TEXT):
    a, b = pl.P(u, v0), pl.P(u, v1)
    return VGroup(Line(a, b, color=color, stroke_width=5), Line(a + LEFT * 0.12, a + RIGHT * 0.12, color=color, stroke_width=5),
                  Line(b + LEFT * 0.12, b + RIGHT * 0.12, color=color, stroke_width=5))


# ---- the day-by-day counts (s21 to s29) -------------------------------------------------------------
GP = Plot(-3.9, -2.6, 8.6, 5.0)
YMAX = 25500.0       # s21 and s22 (numbers on the axis)
YMAX_S = 32500.0     # s25 to s29 (schematic, room for the "more births" prediction)
PEAK = 20400.0


def d2u(d):
    return (d - 5.0) / 6.0


def ctrl_n(d):
    if d <= 6.0:
        return 7000 + (PEAK - 7000) * smooth((d - 5.0) / 1.0)
    if d <= 6.5:
        return PEAK
    return PEAK - 8400 * smooth((d - 6.5) / 3.0)


def births_n(d):      # more births: higher from day 6
    return ctrl_n(d) * (1 + 0.5 * smooth((d - 5.3) / 0.7))


def fewer_n(d):       # fewer deaths: equal at the peak, a smaller loss afterwards
    return PEAK - 0.5 * (PEAK - ctrl_n(d)) if d > 6.0 else ctrl_n(d)


def graft_n(d):       # the reported result: equal at day 6, 11 to 28 percent more at the end
    return PEAK - 0.71 * (PEAK - ctrl_n(d)) if d > 6.0 else ctrl_n(d)


def vv(n, ym=None):
    return n / (ym or YMAX)


def gcurve(fn, d0, d1, color, w=8, n=90, ym=None):
    return GP.curve(lambda u: vv(fn(u * 6.0 + 5.0), ym), d2u(d0), d2u(d1), color, w, n)


def scurve(fn, d0, d1, color, w=8, n=90):
    return gcurve(fn, d0, d1, color, w, n, YMAX_S)


def growth_axes(numbers=True):
    d = {}
    d["axes"] = GP.axes(1.0)
    d["xt"] = VGroup(*[VGroup(Line(GP.P(d2u(x), 0), GP.P(d2u(x), 0) + DOWN * 0.15, color=GREY, stroke_width=3),
                              T(str(x), 26, GREY).move_to(GP.P(d2u(x), 0) + DOWN * 0.5)) for x in (6, 8, 10)])
    d["xl"] = T("days of incubation", 26, GREY).move_to(GP.P(0.3, 0) + DOWN * 1.05)
    if numbers:
        d["ylabs"] = VGroup(*[T(s, 26, GREY).move_to(GP.P(0, vv(n)) + LEFT * 0.2, aligned_edge=RIGHT) for s, n in
                              (("0", 0), ("about 12,000", 12000), ("about 20,000", 20000))])
        d["h20"] = DashedLine(GP.P(0, vv(20000)), GP.P(1.0, vv(20000)), color=GREY, stroke_width=2)
        d["h12"] = DashedLine(GP.P(0, vv(12000)), GP.P(1.0, vv(12000)), color=GREY, stroke_width=2)
    else:
        d["yl"] = T("motor neurons (schematic)", 26, GREY).rotate(PI / 2).move_to([GP.x0 - 0.45, GP.P(0, 0.5)[1], 0])
    return d


def neuron_cartoon(cx, cy, s=1.0, color=BLUE):
    soma = Circle(radius=0.8 * s, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.45).move_to([cx, cy, 0])
    lines = []
    for ang in (100, 140, 180, 220, 260):
        a = np.deg2rad(ang)
        p0 = np.array([cx + 0.8 * s * np.cos(a), cy + 0.8 * s * np.sin(a), 0])
        p1 = np.array([cx + 2.5 * s * np.cos(a), cy + 2.2 * s * np.sin(a), 0])
        lines.append(Line(p0, p1, color=color, stroke_width=6))
    lines.append(Line([cx + 0.8 * s, cy, 0], [cx + 5.4 * s, cy, 0], color=color, stroke_width=6))
    return soma, lines


# =============================================================================================
# 0 title
# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Too Many Neurons: Naturally Occurring Cell Death"
    TITLE = "Count Across Time"


# =============================================================================================
# 1 the question: a low count and two histories
# =============================================================================================
class S01Q(SpokenScene):
    def construct(self):
        base_y = -3.0
        BH, GH = 2.4, 2.4            # bar and ghost: 4.8 tall in all, 60% of the frame
        cx = 0.0
        base = Line([cx - 2.1, base_y, 0], [cx + 2.1, base_y, 0], color=GREY, stroke_width=3)
        bar, ghost, q = bar_items(cx, base_y, BH, 2.6, GH)
        lab = T("final count", 34, BLUE).move_to([cx, base_y - 0.5, 0])
        grp = VGroup(base, bar, ghost, q, lab)
        self.play(Create(base), GrowFromEdge(bar, DOWN), run_time=1.2)
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.6)
        self.at("missing neurons")
        self.play(Create(ghost), FadeIn(q, scale=0.6), run_time=0.9)
        self.at("never made")
        shift = LEFT * 3.1
        gtop = np.array([cx - 3.1 + 1.3, base_y + BH + GH / 2, 0])
        c1 = bchip("never made", GREY, 38).move_to([3.4, 1.35, 0])
        orr = T("or", 34, GREY).move_to([3.4, 0.1, 0])
        c2 = bchip("made, then lost", GREY, 38).move_to([3.4, -1.15, 0])
        a1 = arr(c1.get_left(), gtop + RIGHT * 0.05 + UP * 0.5, GREY, 4)
        a2 = arr(c2.get_left(), gtop + RIGHT * 0.05 + DOWN * 0.7, GREY, 4)
        self.play(grp.animate.shift(shift), FadeIn(c1, shift=LEFT * 0.2), GrowArrow(a1), run_time=0.65)
        self.at("or made")
        self.play(FadeIn(orr), run_time=0.3)
        self.at("made and then lost")
        self.play(FadeIn(c2, shift=LEFT * 0.2), GrowArrow(a2), run_time=0.6)
        self.finish()


# =============================================================================================
# 2 Hamburger 1934
# =============================================================================================
class S021934(SpokenScene):
    def construct(self):
        cx, cy, s = -2.4, 0.0, 1.12
        e = embryo(cx, cy, s, wings=True, bud_stroke=5)
        credit = T("Hamburger, 1934", 28, LGREY).move_to([4.2, -3.3, 0])
        self.play(FadeIn(VGroup(e["body"], e["wing_l"], e["wing_r"])), FadeIn(credit), run_time=0.6)
        ghost = DashedVMobject(Ellipse(width=1.0 * s, height=0.78 * s, stroke_color=YELLOW, stroke_width=4)
                               .move_to(e["wing_r"]), num_dashes=16)
        bud = e["wing_r"]
        lab_bud = bchip("wing bud", YELLOW, 30).move_to([3.4, 0.9, 0])
        bud_arrow = arr(lab_bud.get_left(), ghost.get_right() + RIGHT * 0.1, YELLOW, 4)
        self.at("wing bud")
        self.play(FadeIn(lab_bud), GrowArrow(bud_arrow), run_time=0.25)
        self.play(bud.animate.shift(RIGHT * 1.7 + UP * 0.5).set_opacity(0), FadeIn(ghost), run_time=0.5)
        self.at("chick embryos")
        lab_e = T("chick embryo", 36).move_to([3.4, 2.5, 0])
        self.play(FadeIn(lab_e, shift=LEFT * 0.2),
                  GrowArrow(arr(lab_e.get_left(), [cx + 0.7, 2.5, 0], GREY, 4)), run_time=0.5)
        self.at("about three days old")
        age = T("about 3 days old", 32, LGREY).move_to([3.4, 1.8, 0])
        self.play(FadeIn(age, shift=DOWN * 0.1), run_time=0.5)
        self.finish()


# =============================================================================================
# 3 fewer neurons on the operated side
# =============================================================================================
class S03Fewer(SpokenScene):
    def construct(self):
        c = cord_section()
        head = T("spinal cord, cross-section", 30, LGREY).move_to([0, 3.4, 0])
        self.play(FadeIn(head), Create(c["outline"]), Create(c["mid"]), FadeIn(c["hl"]), FadeIn(c["hr"]), run_time=0.8)
        self.at("the operated side")
        self.play(FadeIn(c["lab_op"], shift=UP * 0.1),
                  LaggedStart(*[FadeIn(d, scale=0.4) for d in c["dotsR"]], lag_ratio=0.05), run_time=1.0)
        self.at("fewer motor neurons")
        self.play(Indicate(c["dotsR"], color=BLUE, scale_factor=1.05), run_time=0.8)
        self.at("the intact side")
        self.play(FadeIn(c["lab_in"], shift=UP * 0.1),
                  LaggedStart(*[FadeIn(d, scale=0.4) for d in c["dotsL"]], lag_ratio=0.04), run_time=1.1)
        self.at("its control")
        self.play(FadeIn(c["lab_ctrl"]), run_time=0.5)
        self.finish()


# =============================================================================================
# 4 Hamburger's reading
# =============================================================================================
class S04Read(SpokenScene):
    def construct(self):
        c = cord_section()
        g = cord_all(c)
        self.add(g)
        small = cord_small()
        limb, limb_l, a, lab, lab2 = limb_items(small)
        self.play(g.animate.scale(CORD_S).move_to([CORD_X, CORD_Y, 0]), run_time=1.1)
        self.at("the limb")
        self.play(FadeIn(limb, shift=LEFT * 0.3), FadeIn(limb_l), run_time=0.6)
        self.at("setting how many")
        self.play(GrowArrow(a), FadeIn(lab, shift=DOWN * 0.1), run_time=0.7)
        self.at("neurons the cord makes")
        self.play(Indicate(g, color=BLUE, scale_factor=1.03), run_time=0.8)
        self.play(FadeIn(lab2), run_time=0.5)
        self.finish()


# =============================================================================================
# 5-7 the bakery
# =============================================================================================
def bakery_sign():
    return T("BAKERY", 48, TEXT, font=TITLE_FONT).move_to([0, 2.85, 0])


def eod_label():
    return T("end of the day", 34, LGREY).move_to([0, -2.4, 0])


def same_label():
    return T("the same shelf", 36, TEXT).move_to([0, -2.4, 0])


class S05Bakery(SpokenScene):
    def construct(self):
        g = cord_small()
        limb, limb_l, a, lab, lab2 = limb_items(g)
        old = VGroup(g, limb, limb_l, a, lab, lab2)
        self.add(old)
        self.at("fits the count")
        self.play(Indicate(a, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.at("so do others")
        self.play(Indicate(lab, color=TEXT, scale_factor=1.05), run_time=0.7)
        sh = big_shelf()
        sign = bakery_sign()
        self.at("think of a bakery")
        self.play(FadeOut(old), FadeIn(sign), Create(sh["frame"]), run_time=0.7)
        self.play(FadeIn(sh["loaves"], lag_ratio=0.1), run_time=0.6)
        self.at("ends the day")
        eod = eod_label()
        self.play(FadeIn(eod), run_time=0.4)
        self.at("half empty")
        self.play(Create(sh["slots"]), run_time=0.9)
        self.finish()


class S06Bakery2(SpokenScene):
    def construct(self):
        sh = big_shelf()
        sign = bakery_sign()
        eod = eod_label()
        self.add(sh["group"], sign, eod)
        r0 = row(0, LAY[1][0])
        self.play(ReplacementTransform(sh["group"], r0["sh"]["group"]), FadeOut(sign), FadeOut(eod), run_time=0.5)
        self.at("baked fewer")
        self.play(FadeIn(r0["ch"], shift=LEFT * 0.2), Indicate(r0["sh"]["slots"], color=GREY, scale_factor=1.04),
                  run_time=0.7)
        r1 = row(1, LAY[2][1])
        self.at("sent some away")
        self.play(r0["all"].animate.shift(UP * (LAY[2][0] - LAY[1][0])), FadeIn(r1["all"], shift=LEFT * 0.2), run_time=0.8)
        r2 = row(2, LAY[3][2])
        self.at("baked some as rolls")
        self.play(r0["all"].animate.shift(UP * (LAY[3][0] - LAY[2][0])),
                  r1["all"].animate.shift(UP * (LAY[3][1] - LAY[2][1])), FadeIn(r2["all"], shift=LEFT * 0.2),
                  run_time=0.8)
        self.finish()


class S07Bakery3(SpokenScene):
    def construct(self):
        rs = [row(i, LAY[3][i]) for i in range(3)]
        for r in rs:
            self.add(r["all"])
        r3 = row(3, LAY[4][3])
        s3 = r3["sh"]
        full = VGroup(*[loaf(SM_X + (i - 3.5) * s3["sp"], s3["ly"], s3["lw"], s3["lh"]) for i in range(4, 8)])
        moves = [rs[i]["all"].animate.shift(UP * (LAY[4][i] - LAY[3][i])) for i in range(3)]
        self.at("a full batch")
        self.play(*moves, FadeIn(s3["frame"]), FadeIn(s3["loaves"]), FadeIn(full), run_time=0.8)
        self.at("threw half away")
        self.play(FadeIn(r3["ex"]), FadeIn(r3["ch"], shift=LEFT * 0.2), run_time=0.4)
        targets = [[1.2 + j * 0.42, s3["ly"], 0] for j in range(4)]
        self.play(*[ld.animate.set_color(RED).scale(0.55).move_to(t) for ld, t in zip(full, targets)],
                  FadeIn(s3["slots"]), run_time=1.0)
        self.at("the shelf looks the same")
        allr = rs + [r3]
        self.play(*[Indicate(r["sh"]["slots"], color=TEXT, scale_factor=1.03) for r in allr], run_time=1.0)
        self.at("every time")
        big = big_shelf()
        extras = VGroup(*[r["ex"] for r in allr if len(r["ex"])], *[r["ch"] for r in allr], full)
        same = same_label()
        self.play(FadeOut(extras), *[FadeOut(allr[i]["sh"]["group"]) for i in range(1, 4)],
                  ReplacementTransform(allr[0]["sh"]["group"], big["group"]), FadeIn(same), run_time=1.3)
        self.finish()


class S08Beat(NarratedScene):
    def construct(self):
        big = big_shelf()
        self.add(big["group"], same_label())
        self.finish()


# =============================================================================================
# 9 the shelf is the short bar
# =============================================================================================
class S09Shelf(SpokenScene):
    def construct(self):
        big = big_shelf()
        same = same_label()
        self.add(big["group"], same)
        base_y, bx = -3.0, -1.0
        bar, ghost, q = bar_items(bx, base_y, 2.4, 2.6, 2.4)
        axis = Arrow([-6.0, base_y, 0], [bx + 1.7, base_y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
        tl = T("time", 28, GREY).move_to([-5.2, base_y - 0.42, 0])
        lab = T("final count", 34, BLUE).move_to([bx, base_y - 0.5, 0])
        c1 = bchip("never made?", GREY, 34).move_to([3.7, 1.9, 0])
        c2 = bchip("made, then lost?", GREY, 34).move_to([3.7, 0.7, 0])
        self.at("low neuron count")
        self.play(FadeOut(big["frame"]), FadeOut(same), ReplacementTransform(big["loaves"], bar),
                  ReplacementTransform(big["slots"], ghost), Create(axis), run_time=1.5)
        self.play(FadeIn(q, scale=0.6), FadeIn(lab), run_time=0.6)
        self.at("a count made only at the end")
        end = T("count made only at the end", 30, YELLOW).move_to([bx + 4.6, base_y + 1.2, 0])
        ea, a1, a2 = s09_arrows(end, c1, c2)
        self.play(FadeIn(tl), FadeIn(end, shift=LEFT * 0.2), GrowArrow(ea), Indicate(bar, color=BLUE, scale_factor=1.05),
                  run_time=0.9)
        self.at("the histories apart")
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(c2, shift=LEFT * 0.2), GrowArrow(a1), GrowArrow(a2), run_time=0.9)
        self.finish()


# =============================================================================================
# 10-11 predict, then the pause
# =============================================================================================
def s09_arrows(end, c1, c2, bx=-1.0, base_y=-3.0):
    return (arr(end.get_left() + LEFT * 0.05, [bx + 1.4, base_y + 1.0, 0], YELLOW, 4),
            arr(c1.get_left(), [bx + 1.4, base_y + 4.0, 0], GREY, 4),
            arr(c2.get_left(), [bx + 1.4, base_y + 3.6, 0], GREY, 4))


def s09_end_items():
    base_y, bx = -3.0, -1.0
    bar, ghost, q = bar_items(bx, base_y, 2.4, 2.6, 2.4)
    axis = Arrow([-6.0, base_y, 0], [bx + 1.7, base_y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
    tl = T("time", 28, GREY).move_to([-5.2, base_y - 0.42, 0])
    lab = T("final count", 34, BLUE).move_to([bx, base_y - 0.5, 0])
    end = T("count made only at the end", 30, YELLOW).move_to([bx + 4.6, base_y + 1.2, 0])
    c1 = bchip("never made?", GREY, 34).move_to([3.7, 1.9, 0])
    c2 = bchip("made, then lost?", GREY, 34).move_to([3.7, 0.7, 0])
    return VGroup(bar, ghost, q, axis, tl, lab, end, c1, c2, *s09_arrows(end, c1, c2))


class S10Predict(SpokenScene):
    def construct(self):
        old = s09_end_items()
        self.add(old)
        axes, ylab, xlab, prompt, q1, q2 = predict_pieces()
        self.play(FadeOut(old), Create(axes), FadeIn(ylab), FadeIn(xlab), FadeIn(prompt, shift=DOWN * 0.1), run_time=1.0)
        self.at("what would you count")
        self.play(FadeIn(q1, shift=DOWN * 0.1), run_time=0.7)
        self.at("tell never made")
        self.play(FadeIn(q2, shift=DOWN * 0.1), run_time=0.7)
        self.finish()


class S11Pause(NarratedScene):
    def construct(self):
        self.add(*predict_pieces())
        self.finish()


# =============================================================================================
# 12 count at stages, both sides, healthy and dying
# =============================================================================================
class S12Rev1(SpokenScene):
    def construct(self):
        axes, ylab, xlab, prompt, q1, q2 = predict_pieces()
        self.add(axes, ylab, xlab, prompt, q1, q2)
        big_ticks = tick_row(BP)
        self.play(FadeOut(prompt), FadeOut(q1), FadeOut(q2), FadeOut(ylab), run_time=0.4)
        self.at("closely spaced stages")
        self.play(LaggedStart(*[GrowFromCenter(t) for t in big_ticks], lag_ratio=0.1), run_time=1.3)
        p = panels()
        self.at("on both sides")
        self.play(FadeIn(p["legend"], shift=DOWN * 0.15), run_time=0.7)
        self.at("healthy neurons")
        self.play(ReplacementTransform(axes, p["up_axes"]), ReplacementTransform(big_ticks, p["up_ticks"]),
                  ReplacementTransform(xlab, p["xlab"]), FadeIn(p["lab_up"]), FadeIn(p["ylab_up"]), run_time=1.0)
        self.at("count dying ones")
        self.play(FadeIn(p["lp_axes"]), FadeIn(p["lp_ticks"]), FadeIn(p["lab_lp"]), FadeIn(p["ylab_lp"]),
                  FadeIn(p["sch"]), run_time=0.9)
        self.finish()


# =============================================================================================
# 13 the pyknotic nucleus
# =============================================================================================
class S13Pyk(SpokenScene):
    def construct(self):
        pg = panels_group(panels())
        self.add(pg)
        cell = Circle(radius=2.3, stroke_color=RED, stroke_width=5, fill_color=RED, fill_opacity=0.12).move_to([-2.4, 0.1, 0])
        nuc = Circle(radius=1.15, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35).move_to(cell)
        cap = T("a dying neuron", 34, RED).move_to([-2.4, -2.95, 0])
        self.play(FadeOut(pg), GrowFromCenter(cell), FadeIn(nuc, scale=0.7), FadeIn(cap), run_time=0.6)
        tags = [T(w, 40, TEXT).move_to([3.3, y, 0]) for w, y in (("small", 2.0), ("dark", 1.2), ("condensed", 0.4))]
        small = Circle(radius=0.55, stroke_color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.5).move_to(cell)
        self.at("small")
        self.play(Transform(nuc, small), FadeIn(tags[0], shift=LEFT * 0.2), run_time=0.5)
        dark = Circle(radius=0.55, stroke_color=RED, stroke_width=4, fill_color=DARK, fill_opacity=1.0).move_to(cell)
        self.at("dark")
        self.play(Transform(nuc, dark), FadeIn(tags[1], shift=LEFT * 0.2), run_time=0.5)
        cond = Circle(radius=0.38, stroke_color=RED, stroke_width=5, fill_color=DARK, fill_opacity=1.0).move_to(cell)
        self.at("condensed")
        self.play(Transform(nuc, cond), FadeIn(tags[2], shift=LEFT * 0.2), run_time=0.7)
        lab = bchip("pyknotic nucleus", RED, 36).move_to([3.1, -1.0, 0])
        lab2 = T("often a dying cell", 36, TEXT).move_to([3.1, -1.9, 0])
        self.at("it is called")
        self.play(FadeIn(lab, shift=LEFT * 0.2), GrowArrow(arr(lab.get_left(), [-1.7, -0.1, 0], RED, 4)), run_time=0.7)
        self.play(FadeIn(lab2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# =============================================================================================
# 14 never made
# =============================================================================================
class S14Rev2(SpokenScene):
    def construct(self):
        self.add(panels_group(panels(tag=True)), side_note())
        c_in = HP.curve(f_in, 0.02, 1.0, BLUE, 8)
        c_op = HP.curve(f_never, 0.02, 1.0, YELLOW, 6)
        lab = bchip("predicted under reduced production", GREY, 26).move_to([0.4, 0.2, 0])
        self.at("never made")
        self.play(Create(c_in), FadeIn(lab, shift=UP * 0.1), run_time=0.9)
        self.at("the operated side")
        self.play(Create(c_op), run_time=1.0)
        self.at("never catches up")
        br = gap_bracket(HP, 0.985, f_never(1.0), f_in(1.0))
        self.play(Create(br), run_time=0.6)
        self.at("no extra dying cells")
        flat = DashedLine(DP.P(0.02, 0.03), DP.P(1.0, 0.03), color=RED, stroke_width=4)
        none = T("no extra dying cells", 28, RED).move_to(DP.P(0.5, 0.55))
        self.play(Create(flat), FadeIn(none), run_time=0.8)
        self.finish()


# =============================================================================================
# 14b the caution
# =============================================================================================
CP = Plot(-5.4, -3.4, 10.8, 1.6)   # the faded dying-neurons panel behind the inset


def caution_hump(u):
    if not 0.18 <= u <= 0.82:
        return 0.0
    return 0.95 * hump_h(0.30 + (u - 0.18) / 0.64 * 0.5) / 0.85


class S14bCaution(SpokenScene):
    def construct(self):
        pg = panels_group(panels(tag=True))
        note = side_note()
        self.add(pg, note)
        title = T("a missing hump is not proof on its own", 38, TEXT).move_to([0, 3.4, 0])
        tick_y = 0.1
        line = Line([-5.6, tick_y, 0], [5.6, tick_y, 0], color=GREY, stroke_width=3)
        ta = Line([-4.1, tick_y - 0.28, 0], [-4.1, tick_y + 0.28, 0], color=TEXT, stroke_width=5)
        tb = Line([4.1, tick_y - 0.28, 0], [4.1, tick_y + 0.28, 0], color=TEXT, stroke_width=5)
        la = T("count", 30, LGREY).move_to([-4.1, tick_y - 0.7, 0])
        lb = T("next count", 30, LGREY).move_to([4.1, tick_y - 0.7, 0])
        # the faded dying-neurons panel with the hump a sparse count can miss
        cax = CP.axes(1.05)
        pts = [CP.P(0.18, 0)] + [CP.P(u, caution_hump(u)) for u in np.linspace(0.18, 0.82, 60)] + [CP.P(0.82, 0)]
        hump = DashedVMobject(VMobject(stroke_color=RED, stroke_width=4, fill_opacity=0).set_points_as_corners(pts), num_dashes=70)
        hump.set_stroke(opacity=0.55)
        hump_l = T("dying neurons: the hump", 28, RED).move_to(CP.P(0.5, 1.0) + UP * 0.28).set_opacity(0.8)
        zero1 = Dot(CP.P(0.118, 0), radius=0.13, color=TEXT)
        zero2 = Dot(CP.P(0.882, 0), radius=0.13, color=TEXT)
        self.play(FadeOut(pg), FadeOut(note), FadeIn(title), FadeIn(VGroup(line, ta, tb, la, lb)), FadeIn(cax),
                  FadeIn(hump), FadeIn(hump_l), run_time=0.35)
        self.add(zero1, zero2)
        cellp = [-4.1, 1.5, 0]
        dead = Circle(radius=0.8, stroke_color=RED, stroke_width=4, fill_color=DARK, fill_opacity=1).move_to(cellp)
        nuc = Circle(radius=0.36, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.9).move_to(cellp)
        cellg = VGroup(dead, nuc)
        self.at("dying cells")
        self.play(FadeIn(cellg, scale=0.6), run_time=0.6)
        eater = Circle(radius=1.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([-5.6, 1.9, 0])
        self.at("cleared fast")
        self.play(FadeIn(eater), eater.animate.move_to(cellp), run_time=0.5)
        self.play(cellg.animate.scale(0.2).set_opacity(0), run_time=0.4)
        gone = T("gone before the next count", 36, LGREY).move_to([0.3, 1.5, 0])
        self.play(eater.animate.move_to([0.0, 1.5, 0]).set_opacity(0.0), FadeIn(gone), run_time=0.4)
        self.at("count often")
        xs_u = np.linspace(0.3, 0.7, 5)
        extra = VGroup(*[Line([CP.P(u, 0)[0], tick_y - 0.2, 0], [CP.P(u, 0)[0], tick_y + 0.2, 0], color=TEXT, stroke_width=4)
                         for u in xs_u])
        dots = VGroup(*[Dot(CP.P(u, caution_hump(u)), radius=0.13, color=RED) for u in xs_u])
        self.play(FadeOut(gone), LaggedStart(*[GrowFromCenter(t) for t in extra], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(d_, scale=0.3) for d_ in dots], lag_ratio=0.12), run_time=1.0)
        self.at("birth date the cells")
        bd = bchip("birth-date the cells", TEAL, 34).move_to([0, 1.5, 0])
        self.play(FadeIn(bd, shift=UP * 0.15), run_time=0.6)
        self.at("a missing hump")
        self.play(Indicate(hump, color=RED, scale_factor=1.04), Indicate(title, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.finish()


# =============================================================================================
# 15 made, then lost
# =============================================================================================
class S15Rev3(SpokenScene):
    def construct(self):
        self.add(panels_group(panels(tag=True)), side_note())
        self.add(HP.curve(f_in, 0.02, 1.0, BLUE, 8))
        lab = bchip("made, then lost", GREY, 30).move_to([0.4, 0.2, 0])
        self.at("made then lost")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
        c1 = HP.curve(f_lost, 0.02, 0.38, YELLOW, 5, 30)
        self.at("the sides start equal")
        self.play(Create(c1), run_time=1.0)
        hump = hump_poly()
        self.at("then dying cells appear")
        self.play(GrowFromEdge(hump, DOWN), run_time=1.1)
        c2 = HP.curve(f_lost, 0.38, 1.0, YELLOW, 6, 60)
        self.at("the count falls behind")
        self.play(Create(c2), run_time=1.3)
        self.finish()


class S16Beat(NarratedScene):
    def construct(self):
        self.add(panels_group(panels(tag=True)), side_note())
        self.add(HP.curve(f_in, 0.02, 1.0, BLUE, 8))
        self.add(bchip("made, then lost", GREY, 30).move_to([0.4, 0.2, 0]))
        self.add(HP.curve(f_lost, 0.02, 1.0, YELLOW, 6, 90))
        self.add(hump_poly())
        self.finish()


# =============================================================================================
# 17-18 Levi-Montalcini and Levi
# =============================================================================================
SXS = [-4.65, -1.55, 1.55, 4.65]
SY = -0.45


def stained_panel(cx, cy, seed, n=14):
    rnd = random.Random(seed)
    pan = RoundedRectangle(corner_radius=0.15, width=2.9, height=2.9, stroke_color=GREY, stroke_width=3,
                           fill_color=PAPER, fill_opacity=0.92).move_to([cx, cy, 0])
    cells = []
    for _ in range(n):
        x = cx + rnd.uniform(-1.05, 1.05)
        y = cy + rnd.uniform(-1.05, 1.05)
        a = rnd.uniform(0, 6.28)
        cells.append(VGroup(Line([x, y, 0], [x + 0.32 * np.cos(a), y + 0.32 * np.sin(a), 0], color=INK, stroke_width=2),
                            Dot([x, y, 0], radius=0.11, color=INK)))
    g = VGroup(pan, *cells)
    g.cells = cells
    return g


def shrink_cells(panels_, instant=False):
    """The cells of the last two panels begin to shrink and fade (sets up s18). Returns animations, or applies at once."""
    anims = []
    for pi, frac, sc in ((2, 2, 0.6), (3, 1, 0.4)):
        for j, c in enumerate(panels_[pi].cells):
            if (frac == 2 and j % 2 == 0) or (frac == 1 and j % 3 != 0):
                if instant:
                    c.scale(sc).set_opacity(0.55)
                else:
                    anims.append(c.animate.scale(sc).set_opacity(0.55))
    return anims


class S17Rlm2(SpokenScene):
    def construct(self):
        scales = [0.28, 0.31, 0.34, 0.37]
        ey = 2.05
        embs, ghosts = [], []
        for x, sc in zip(SXS, scales):
            e = embryo(x, ey, sc, wings=True, bud_stroke=2)
            e["wing_r"].set_stroke(opacity=0).set_fill(opacity=0)
            ghosts.append(DashedVMobject(Ellipse(width=1.0 * sc, height=0.78 * sc, stroke_color=YELLOW, stroke_width=3)
                                         .move_to(e["wing_r"]), num_dashes=10))
            embs.append(VGroup(e["body"], e["wing_l"], ghosts[-1]))
        sects = [stained_panel(x, SY, i + 5) for i, x in enumerate(SXS)]
        arrows = [arr([SXS[i] + 0.95, ey, 0], [SXS[i + 1] - 0.95, ey, 0], GREY, 3, 0.15) for i in range(3)]
        tag = bchip("limb bud removed", YELLOW, 26).move_to([-2.6, 3.5, 0])
        tag_a = arr(tag.get_left() + LEFT * 0.0, ghosts[0].get_center() + UP * 0.15, YELLOW, 3, 0.15)
        stage = [T(w, 28, LGREY).move_to([x, -2.25, 0]) for w, x in zip(("earlier", "later", "later still", "latest"), SXS)]
        foot1 = T("Schematic, not the original sections", 26, LGREY).move_to([-3.35, -3.6, 0])
        foot2 = T("Turin and Piedmont, 1942 to 1944", 26, LGREY).move_to([3.35, -3.6, 0])
        self.play(LaggedStart(*[FadeIn(e) for e in embs], lag_ratio=0.15), *[GrowArrow(a) for a in arrows],
                  FadeIn(tag, shift=DOWN * 0.1), GrowArrow(tag_a), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in sects], lag_ratio=0.1), FadeIn(foot1), FadeIn(foot2),
                  run_time=0.7)
        n1 = bchip("Rita Levi-Montalcini", TEXT, 28).move_to([-3.0, -2.95, 0])
        n2 = bchip("Giuseppe Levi", TEXT, 28).move_to([3.0, -2.95, 0])
        self.at("rita levi montalcini")
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.5)
        self.at("giuseppe levi")
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.5)
        self.at("staged sections")
        self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in stage], lag_ratio=0.2), run_time=1.0)
        self.at("like these")
        self.play(*shrink_cells(sects), run_time=1.6)
        self.finish()


class S18Rlm3(SpokenScene):
    def construct(self):
        sects = VGroup(*[stained_panel(x, SY, i + 5) for i, x in enumerate(SXS)])
        shrink_cells(list(sects), instant=True)
        self.add(sects)
        s = 1.25
        soma, lines = neuron_cartoon(-1.8, 0.0, s)
        self.play(FadeOut(sects), run_time=0.5)
        self.play(GrowFromCenter(soma), *[Create(l) for l in lines], run_time=1.0)
        top = T("neurons already formed", 40, BLUE).move_to([0, 3.4, 0])
        self.at("already formed")
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.6)
        top2 = T("now degenerating", 40, RED).move_to([0, 3.4, 0])
        dashed = [DashedVMobject(l.copy().set_color(RED), num_dashes=10, dashed_ratio=0.5) for l in lines]
        self.at("now degenerating")
        self.play(ReplacementTransform(top, top2),
                  soma.animate.scale(0.7).set_color(RED).set_fill(RED, 0.6),
                  *[ReplacementTransform(l, d) for l, d in zip(lines, dashed)], run_time=1.2)
        self.play(*[dd.animate.shift([random.Random(i * 3 + j).uniform(-0.18, 0.18),
                                      random.Random(i * 5 + j).uniform(-0.18, 0.18), 0])
                    for i, d in enumerate(dashed) for j, dd in enumerate(d)], run_time=0.8)
        lab = bchip("made, then lost", RED, 44).move_to([3.2, -2.4, 0])
        self.at("the missing neurons had been made")
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.7)
        self.finish()


# =============================================================================================
# 19 the 1949 paper
# =============================================================================================
G_XS = [-4.3, 0.0, 4.3]
G_Y = -0.15


def ganglion(cx, cy, seed=2):
    cord = RoundedRectangle(corner_radius=0.2, width=0.6, height=4.4, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.2).move_to([cx - 1.2, cy, 0])
    gang = Ellipse(width=2.9, height=4.3, stroke_color=GREY, stroke_width=3, fill_color=BLUE,
                   fill_opacity=0.06).move_to([cx + 0.7, cy, 0])
    pts = lattice(cx + 0.7, cy, 1.0, 1.7, 0.56, seed=seed)
    return cord, gang, pts


class S191949(SpokenScene):
    def construct(self):
        head = T("1949, St. Louis", 46, TEXT, font=TITLE_FONT).move_to([-3.2, 3.3, 0])
        parts = [ganglion(x, G_Y, seed=2) for x in G_XS]
        pts = parts[0][2]
        n = len(pts)
        rnd = random.Random(7)
        order = list(range(n))
        rnd.shuffle(order)
        few = set(order[:int(round(n * 0.4))])        # earliest stage: few cells
        keep3 = set(order[:int(round(n * 0.62))])     # last stage: fewer than the peak, not the starting number
        d1 = VGroup(*[Dot(p_, radius=0.16, color=BLUE) for i, p_ in enumerate(pts) if i in few])
        d2 = VGroup(*[Dot(p_ + np.array([4.3, 0, 0]), radius=0.16, color=BLUE) for p_ in pts])
        d3_all = [Dot(p_ + np.array([8.6, 0, 0]), radius=0.16, color=BLUE) for p_ in pts]
        d3 = VGroup(*d3_all)
        cord_l = [T("cord", 26, LGREY).move_to([x - 1.2, -2.75, 0]) for x in G_XS]
        gang_l = [T("ganglion", 26, LGREY).move_to([x + 0.8, -2.75, 0]) for x in G_XS]
        st = [T(w, 30, TEXT).move_to([x - 0.2, -3.4, 0]) for w, x in zip(("earlier", "later", "later still"), G_XS)]
        sens = T("sensory neurons", 30, BLUE).move_to([G_XS[0] + 0.7, 2.62, 0])
        # The first word already has an identifiable, populated ganglion.
        self.add(head, parts[0][0], parts[0][1], d1, sens, st[0], cord_l[0], gang_l[0])
        self.play(*[FadeIn(p_[0]) for p_ in parts[1:]],
                  *[FadeIn(p_[1]) for p_ in parts[1:]], run_time=0.6)
        self.at("sensory neurons")
        self.play(Indicate(sens, color=BLUE, scale_factor=1.1), run_time=0.6)
        a1 = arr([G_XS[0] + 1.0, -3.4, 0], [G_XS[1] - 1.0, -3.4, 0], GREY, 3, 0.15)
        a2 = arr([G_XS[1] + 1.0, -3.4, 0], [G_XS[2] - 1.0, -3.4, 0], GREY, 3, 0.15)
        self.at("chick spinal ganglia")
        self.play(*[FadeIn(t) for t in cord_l[1:] + gang_l[1:]], run_time=0.4)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in d2], lag_ratio=0.02), FadeIn(st[1]), GrowArrow(a1),
                  run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in d3], lag_ratio=0.02), FadeIn(st[2]), GrowArrow(a2),
                  run_time=0.4)
        self.at("supported that reading")
        gone = [d for i, d in enumerate(d3_all) if i not in keep3]
        self.play(*[d.animate.set_color(RED).scale(1.3) for d in gone], run_time=0.6)
        self.play(*[FadeOut(d, scale=0.3) for d in gone], run_time=0.8)
        self.finish()


# =============================================================================================
# 20 the target's job
# =============================================================================================
class S20Job(SpokenScene):
    def construct(self):
        limb = Ellipse(width=2.8, height=2.4, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                       fill_opacity=0.25).move_to([-4.9, 0.0, 0])
        limb_l = T("target", 34, YELLOW).move_to(limb)
        hd = T("the target's main job", 40, YELLOW).move_to([1.3, 2.6, 0])
        l1 = T("to make neurons", 54, TEXT, font=TITLE_FONT).move_to([1.3, 0.75, 0])
        fit(l1, max_w=9.0)
        strike = Line(l1.get_left() + LEFT * 0.15, l1.get_right() + RIGHT * 0.15, color=RED, stroke_width=8)
        l2 = T("to keep them alive", 54, BLUE, font=TITLE_FONT).move_to([1.3, -1.15, 0])
        fit(l2, max_w=9.0)
        self.play(FadeIn(limb, shift=RIGHT * 0.2), FadeIn(limb_l), FadeIn(hd, shift=DOWN * 0.1), run_time=0.6)
        self.at("not to call neurons")
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.4)
        self.play(Create(strike), run_time=0.6)
        self.at("it was to keep")
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.8)
        self.finish()


# =============================================================================================
# 21-23 Hamburger 1975
# =============================================================================================
def s22_items():
    g = growth_axes(True)
    head = T("lumbar lateral motor column", 36, TEXT, font=TITLE_FONT).move_to([1.2, 3.4, 0])
    credit = T("Hamburger, 1975", 28, LGREY).move_to([1.2, 2.82, 0])
    yl = T("motor neurons (raw counts)", 26, GREY).move_to([-6.6, 2.75, 0], aligned_edge=LEFT)
    return g, head, credit, yl


def s21_embryo():
    # A dedicated left panel keeps the normal embryo away from the data axes.
    e = embryo(-4.6, 0.2, 0.95, wings=True, legs=True, bud_stroke=5)
    lab = T("normal embryo:\nall its limbs", 26, LGREY, line_spacing=0.9).move_to([-4.6, -3.25, 0])
    return e, lab


def s21_chart():
    pl = Plot(-1.7, -2.6, 7.8, 4.5)
    ticks = VGroup(*[VGroup(
        Line(pl.P(d2u(day), 0), pl.P(d2u(day), 0) + DOWN * 0.15, color=GREY, stroke_width=3),
        T(str(day), 26, GREY).move_to(pl.P(d2u(day), 0) + DOWN * 0.4))
        for day in (5, 6, 8, 11)])
    xlab = T("embryonic day", 26, GREY).move_to([2.2, -3.45, 0])
    ylab = T("motor neurons (raw counts)", 26, GREY).move_to([2.2, 2.3, 0])
    return VGroup(pl.axes(), ticks, xlab, ylab)


class S211975(SpokenScene):
    def construct(self):
        g, head, credit, yl = s22_items()
        chart = s21_chart()
        e, lab = s21_embryo()
        # Body and all four buds appear together, with no partial limb-less drawing.
        self.play(FadeIn(credit), FadeIn(head), FadeIn(chart),
                  FadeIn(VGroup(*e.values())), run_time=0.6)
        dchip = bchip("the death itself", RED, 32).move_to([2.5, 1.2, 0])
        self.at("counted the death")
        self.play(FadeIn(dchip, shift=LEFT * 0.2), run_time=0.5)
        self.at("normal embryos")
        self.play(FadeOut(dchip), FadeIn(lab), run_time=0.45)
        self.at("all their limbs")
        self.play(*[Indicate(e[k], color=YELLOW, scale_factor=1.15) for k in ("wing_l", "wing_r", "leg_l", "leg_r")],
                  run_time=0.6)
        self.finish()


def lead_in():
    seg = gcurve(ctrl_n, 5.0, 6.0, BLUE, 8, 40)
    d = DashedVMobject(seg, num_dashes=16)
    lab = T("dashed part:\nnot measured", 26, LGREY, line_spacing=0.9).move_to([-2.25, -1.45, 0], aligned_edge=LEFT)
    return d, lab


def s22_end_items():
    c1 = gcurve(ctrl_n, 6.0, 6.5, BLUE, 8, 40)
    c2 = gcurve(ctrl_n, 6.5, 11.0, BLUE, 8, 90)
    d6 = DashedLine(GP.P(d2u(6.0), 0), GP.P(d2u(6.0), vv(PEAK)), color=GREY, stroke_width=2)
    dot = Dot(GP.P(d2u(6.0), vv(ctrl_n(6.0))), radius=0.16, color=BLUE)
    br = gap_bracket(GP, 0.965, vv(12000), vv(PEAK), RED)
    lab = VGroup(*[T(s_, 26, RED) for s_ in ("about 40%", "of the peak", "lost")]).arrange(DOWN, buff=0.1)
    lab.move_to([5.75, 0.1, 0])
    loss_w = Rectangle(width=GP.w * 3.0 / 6.0, height=GP.h * 1.0, stroke_width=0, fill_color=RED,
                       fill_opacity=0.14).move_to((GP.P(d2u(6.5), 0) + GP.P(d2u(9.5), 1.0)) / 2)
    loss_l = T("most of the loss", 28, RED).move_to(GP.P(d2u(8.0), 0.9))
    edge_labs = VGroup(*[T(s_, 26, RED).move_to(GP.P(d2u(x), 0) + DOWN * 0.5) for s_, x in (("6.5", 6.5), ("9.5", 9.5))])
    edge_ticks = VGroup(*[Line(GP.P(d2u(x), 0), GP.P(d2u(x), 0) + DOWN * 0.15, color=RED, stroke_width=3) for x in (6.5, 9.5)])
    return c1, c2, d6, dot, br, lab, loss_w, loss_l, VGroup(edge_labs, edge_ticks)


class S22Curve(SpokenScene):
    def construct(self):
        g, head, credit, yl = s22_items()
        e, elab = s21_embryo()
        native_chart = VGroup(g["axes"], g["xt"], g["xl"], g["ylabs"], yl)
        chart = s21_chart()
        self.add(VGroup(*e.values()), head, credit, elab, chart)
        c1, c2, d6, dot, br, lab, loss_w, loss_l, edges = s22_end_items()
        lead, lead_lab = lead_in()
        self.play(FadeOut(VGroup(*e.values(), elab, chart)), run_time=0.3)
        self.play(FadeIn(native_chart), run_time=0.3)
        self.play(Create(lead, run_time=1.0), FadeIn(lead_lab, run_time=0.8))
        self.at("peaked near")
        self.play(FadeIn(g["h20"]), Create(c1), run_time=0.5)
        self.at("day six")
        self.play(Create(d6), FadeIn(dot, scale=2), run_time=0.6)
        self.at("two in five")
        self.play(FadeIn(g["h12"]), Create(c2), FadeIn(loss_w), run_time=1.2)
        self.play(Create(br), FadeIn(lab), run_time=0.4)
        self.at("most within three days")
        self.play(FadeIn(loss_l), FadeIn(edges), run_time=0.9)
        self.finish()


class S23Beat(NarratedScene):
    def construct(self):
        g, head, credit, yl = s22_items()
        c1, c2, d6, dot, br, lab, loss_w, loss_l, edges = s22_end_items()
        lead, lead_lab = lead_in()
        self.add(g["axes"], g["xt"], g["xl"], g["ylabs"], g["h20"], g["h12"], head, credit, yl, loss_w, lead, lead_lab,
                 c1, c2, d6, dot, br, lab, loss_l, edges)
        self.finish()


# =============================================================================================
# 24 Hollyday and Hamburger 1976
# =============================================================================================
class S241976(SpokenScene):
    def construct(self):
        cx, cy, s = -0.6, 0.0, 1.1
        e = embryo(cx, cy, s, legs=True, extra_leg=True)
        credit = T("Hollyday and Hamburger, 1976", 28, LGREY).move_to([3.4, 3.4, 0])
        mid = DashedLine([cx, 3.3, 0], [cx, -3.5, 0], color=GREY, stroke_width=2)
        ctl = T("control side", 34, BLUE).move_to([-4.4, 2.3, 0])
        grf = T("grafted side", 34, YELLOW).move_to([3.5, 2.3, 0])
        self.play(FadeIn(credit, shift=DOWN * 0.1), Create(e["body"]), Create(mid), run_time=1.2)
        self.play(FadeIn(e["leg_l"]), FadeIn(e["leg_r"]), FadeIn(ctl), FadeIn(grf), run_time=0.7)
        extra = e["extra"]
        ghost = DashedVMobject(Ellipse(width=1.0 * s, height=0.78 * s, stroke_color=YELLOW, stroke_width=4)
                               .move_to(extra), num_dashes=16)
        extra.shift(RIGHT * 3.0 + DOWN * 0.3)
        extra.set_fill(opacity=0).set_stroke(opacity=0)
        self.at("grafted an extra leg")
        self.play(FadeIn(ghost), extra.animate.shift(LEFT * 3.0 + UP * 0.3).set_fill(opacity=0.3).set_stroke(opacity=1),
                  run_time=1.1)
        lab_x = bchip("extra leg", YELLOW, 32).move_to([3.6, -2.4, 0])
        self.play(FadeIn(lab_x, shift=LEFT * 0.2), GrowArrow(arr(lab_x.get_left(), extra.get_right(), YELLOW, 4)),
                  run_time=0.6)
        lab_n = bchip("normal leg", YELLOW, 32).move_to([3.6, -0.3, 0])
        self.at("the normal one")
        self.play(FadeIn(lab_n, shift=LEFT * 0.2), GrowArrow(arr(lab_n.get_left(), e["leg_r"].get_right(), YELLOW, 4)),
                  run_time=0.6)
        self.finish()


# =============================================================================================
# 25-26 predict the grafted side
# =============================================================================================
def pred_base():
    g = growth_axes(False)
    ctrl = scurve(ctrl_n, 5.0, 11.0, BLUE, 8, 100)
    lab_c = T("control", 28, BLUE).move_to(GP.P(0.88, vv(ctrl_n(10.4), YMAX_S)) + DOWN * 0.5)
    return g, ctrl, lab_c


def pred_curves():
    mb = scurve(births_n, 5.0, 11.0, PRED_A, 5, 100)
    fd = scurve(fewer_n, 5.0, 11.0, PRED_B, 5, 100)
    mb_l = T("more births", 28, PRED_A).move_to([1.3, 1.5, 0])
    fd_l = T("fewer deaths", 26, PRED_B).move_to(GP.P(0.83, (vv(fewer_n(10.0), YMAX_S) + vv(ctrl_n(10.0), YMAX_S)) / 2))
    return mb, fd, mb_l, fd_l


def pred_question():
    q1 = T("If more target meant more births,", 28).move_to([-0.6, 3.6, 0])
    q2 = T("where would the grafted side's count be at day 6?", 28).move_to([-0.6, 3.2, 0])
    return q1, q2


def day6_marks():
    d6 = DashedLine(GP.P(d2u(6.0), 0), GP.P(d2u(6.0), 1.0), color=GREY, stroke_width=2)
    d6l = T("day 6", 28, TEXT).move_to(GP.P(d2u(6.0), 1.0) + UP * 0.1)
    return d6, d6l


def prompt_chip():
    return bchip("Pause and sketch", TEAL, 30).move_to([0.9, -2.0, 0])


class S25Pred(SpokenScene):
    def construct(self):
        g, ctrl, lab_c = pred_base()
        self.add(g["axes"], g["xt"], g["xl"], g["yl"], ctrl, lab_c)
        mb, fd, mb_l, fd_l = pred_curves()
        q1, q2 = pred_question()
        self.at("if more target")
        self.play(FadeIn(q1, shift=DOWN * 0.1), run_time=0.6)
        self.at("more births")
        self.play(Create(mb), FadeIn(mb_l), run_time=1.0)
        self.at("where would the grafted")
        self.play(FadeIn(q2, shift=DOWN * 0.1), run_time=0.6)
        d6, d6l = day6_marks()
        self.at("at day six")
        self.play(Create(d6), FadeIn(d6l), Create(fd), FadeIn(fd_l), FadeIn(prompt_chip(), shift=UP * 0.1), run_time=1.0)
        self.finish()


class S26Pause(NarratedScene):
    def construct(self):
        g, ctrl, lab_c = pred_base()
        mb, fd, mb_l, fd_l = pred_curves()
        q1, q2 = pred_question()
        d6, d6l = day6_marks()
        self.add(g["axes"], g["xt"], g["xl"], g["yl"], ctrl, lab_c, mb, mb_l, fd, fd_l, q1, q2, d6, d6l, prompt_chip())
        self.finish()


# =============================================================================================
# 27-29 the result
# =============================================================================================
def result_items():
    g, ctrl, lab_c = pred_base()
    mb, fd, mb_l, fd_l = pred_curves()
    d6, d6l = day6_marks()
    return g, ctrl, lab_c, mb, fd, mb_l, fd_l, d6, d6l


def eq_label():
    return VGroup(T("grafted side:", 28, YELLOW), T("equal to control", 28, YELLOW)).arrange(DOWN, buff=0.1).move_to([-1.4, -1.4, 0])


class S27Rev(SpokenScene):
    def construct(self):
        g, ctrl, lab_c, mb, fd, mb_l, fd_l, d6, d6l = result_items()
        self.add(g["axes"], g["xt"], g["xl"], g["yl"], ctrl, lab_c, mb, mb_l, fd, fd_l, d6, d6l)
        pt = GP.P(d2u(6.0), vv(ctrl_n(6.0), YMAX_S))
        dot = Dot(pt, radius=0.17, color=YELLOW)
        ring = Circle(radius=0.3, color=YELLOW, stroke_width=5).move_to(pt)
        self.at("before the normal loss")
        self.play(FadeIn(dot, scale=2), Create(ring), run_time=0.8)
        eq = eq_label()
        self.at("the grafted side had no more")
        self.play(FadeIn(eq, shift=RIGHT * 0.2), mb.animate.set_stroke(opacity=0.25), mb_l.animate.set_opacity(0.25), run_time=0.9)
        self.at("than the control")
        self.play(Indicate(lab_c, color=BLUE, scale_factor=1.15), run_time=0.8)
        self.finish()


def s28_start_items():
    g, ctrl, lab_c, mb, fd, mb_l, fd_l, d6, d6l = result_items()
    mb.set_stroke(opacity=0.25)
    mb_l.set_opacity(0.25)
    pt = GP.P(d2u(6.0), vv(ctrl_n(6.0), YMAX_S))
    dot = Dot(pt, radius=0.17, color=YELLOW)
    ring = Circle(radius=0.3, color=YELLOW, stroke_width=5).move_to(pt)
    eq = eq_label()
    return g, ctrl, lab_c, mb, fd, mb_l, fd_l, d6, d6l, dot, ring, eq


def s28_end_items():
    gc = scurve(graft_n, 6.0, 11.0, YELLOW, 6, 100)
    cap = T("in embryos whose grafts moved vigorously", 32, YELLOW).move_to([-0.6, 3.35, 0])
    end_c = ctrl_n(11.0)
    ex = GP.P(1.0, 0)[0] + 0.25
    y0, y11, y28 = (GP.P(0, vv(end_c * f, YMAX_S))[1] for f in (1.0, 1.11, 1.28))
    br = VGroup(Line([ex, y0, 0], [ex, y28, 0], color=YELLOW, stroke_width=5),
                Line([ex - 0.14, y0, 0], [ex + 0.14, y0, 0], color=YELLOW, stroke_width=5),
                Line([ex - 0.14, y11, 0], [ex + 0.14, y11, 0], color=YELLOW, stroke_width=5),
                Line([ex - 0.14, y28, 0], [ex + 0.14, y28, 0], color=YELLOW, stroke_width=5))
    t11 = T("+11%", 28, YELLOW).move_to([ex + 0.3, y11 - 0.12, 0], aligned_edge=LEFT)
    t28 = T("+28%", 28, YELLOW).move_to([ex + 0.3, y28 + 0.15, 0], aligned_edge=LEFT)
    lab = T("about 11% to 28% more", 30, YELLOW)
    lab.move_to([ex + 0.2 - lab.width / 2, y28 + 1.15, 0])
    return gc, cap, br, t11, t28, lab


class S28Rev2(SpokenScene):
    def construct(self):
        g, ctrl, lab_c, mb, fd, mb_l, fd_l, d6, d6l, dot, ring, eq = s28_start_items()
        self.add(g["axes"], g["xt"], g["xl"], g["yl"], ctrl, lab_c, mb, mb_l, fd, fd_l, d6, d6l, dot, ring, eq)
        gc, cap, br, t11, t28, lab = s28_end_items()
        self.play(FadeOut(VGroup(ring, eq, mb, mb_l, fd, fd_l)), FadeIn(cap, shift=DOWN * 0.1), Create(gc, run_time=2.6))
        self.at("it had more")
        self.play(Indicate(gc, color=YELLOW, scale_factor=1.0), run_time=0.5)
        self.at("about a tenth")
        self.play(FadeIn(lab, shift=DOWN * 0.1), Create(br), FadeIn(t11), FadeIn(t28), run_time=0.9)
        self.finish()


class S29Beat(NarratedScene):
    def construct(self):
        g, ctrl, lab_c, mb, fd, mb_l, fd_l, d6, d6l, dot, ring, eq = s28_start_items()
        gc, cap, br, t11, t28, lab = s28_end_items()
        self.add(g["axes"], g["xt"], g["xl"], g["yl"], ctrl, lab_c, d6, d6l, dot, gc, cap, br, t11, t28, lab)
        self.finish()


# =============================================================================================
# 30-32 the takeaway
# =============================================================================================
def s30_cards():
    l0 = T("more target", 46, YELLOW, font=TITLE_FONT).move_to([0, 2.6, 0])
    l1 = T("more births", 64, TEXT, font=TITLE_FONT).move_to([0, 0.5, 0])
    strike = Line(l1.get_left() + LEFT * 0.15, l1.get_right() + RIGHT * 0.15, color=RED, stroke_width=8)
    l2 = T("fewer deaths", 64, BLUE, font=TITLE_FONT).move_to([0, -1.9, 0])
    a1 = arr([0, 2.05, 0], [0, 1.25, 0], GREY, 5)
    a2 = arr([0, -0.2, 0], [0, -1.2, 0], GREY, 5)
    return l0, l1, strike, l2, a1, a2


class S30Take(SpokenScene):
    def construct(self):
        l0, l1, strike, l2, a1, a2 = s30_cards()
        self.at("more target")
        self.play(FadeIn(l0, shift=UP * 0.1), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(l1, shift=UP * 0.1), run_time=0.6)
        self.at("more births")
        self.play(Create(strike), run_time=0.5)
        self.at("it meant fewer deaths")
        self.play(GrowArrow(a2), FadeIn(l2, shift=UP * 0.1), run_time=0.7)
        self.finish()


def s31_items():
    tk = T("Takeaway", 36, GOLD, weight=BOLD).move_to([0, 3.0, 0])
    head = T("To read a history from a count:", 50, TEXT, font=TITLE_FONT).move_to([0, 1.5, 0])
    step1 = bchip("1   count along the way", BLUE, 44).move_to([0, -0.1, 0])
    step2 = bchip("2   birth-date the cells", TEAL, 44).move_to([0, -1.7, 0])
    return tk, head, step1, step2


class S31Take2(SpokenScene):
    def construct(self):
        l0, l1, strike, l2, a1, a2 = s30_cards()
        old = VGroup(l0, l1, strike, l2, a1, a2)
        self.add(old)
        tk, head, step1, step2 = s31_items()
        self.play(FadeOut(old), FadeIn(tk), run_time=0.45)
        self.at("a count tells you")
        self.play(FadeIn(head, shift=UP * 0.1), run_time=0.7)
        self.at("only if you also")
        self.play(FadeIn(step1, shift=UP * 0.1), run_time=0.6)
        self.at("along the way")
        self.play(FadeIn(step2, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S32End(EndCard):
    LINE = "A count tells a history only if you counted along the way."

    def construct(self):
        old = VGroup(*s31_items())
        self.add(old)
        line = T(self.LINE, 40, font=TITLE_FONT)
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", 26, TEAL)
        VGroup(line, sub).arrange(DOWN, buff=0.4)
        self.play(FadeOut(old), FadeIn(line, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
