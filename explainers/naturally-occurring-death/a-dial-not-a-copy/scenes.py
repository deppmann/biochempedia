"""Too Many Neurons: chapter 3, "A Dial With a Ceiling"  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, same as chapters 1 and 2)
  BLUE   = motor neurons that are present / healthy, and the normal (control) case
  RED    = dying or lost neurons, the fraction that dies
  YELLOW = the manipulated limb side: the grafted extra leg, the target and its support
  GREEN  = activity (muscle activity, circuit activity)
  GREY   = axes, outlines, hypotheses, toy model, de-emphasized (the "copy" bar is a lighter grey)
  WHITE  = the ceiling (TEXT colour)
  A dead neuron is drawn the same way everywhere: a hollow grey ring (it flashes red as it goes).
"""
import math
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

GHOSTC = "#B9BFCB"   # lighter grey: the hypothetical "copy" bar


# ---------------------------------------------------------------------------------------------
# small helpers
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


def ghost_anim(d):
    return d.animate.set_fill(BLUE, opacity=0).set_stroke(GREY, width=2.5, opacity=0.9)


def set_ghost(d):
    d.set_fill(BLUE, opacity=0).set_stroke(GREY, width=2.5, opacity=0.9)


def refill_anim(d):
    return d.animate.set_fill(BLUE, opacity=1).set_stroke(BLUE, width=0, opacity=1)


def flash_ghost(scene, dots, lag=0.1, t=1.4):
    """dots flash red and end as hollow rings (the one picture of death in this film)."""
    scene.play(LaggedStart(*[d.animate.set_color(RED) for d in dots], lag_ratio=lag), run_time=t * 0.55)
    scene.play(LaggedStart(*[ghost_anim(d) for d in dots], lag_ratio=lag), run_time=t * 0.45 + 0.2)


# ---------------------------------------------------------------------------------------------
# bar chart: survivors (scenes 1 to 7)
Y0 = -2.5
K = 5.1 / 24000.0
XN, XG, XO = -4.9, -2.0, 0.9
BW = 2.0
RC = 4.7   # right column centre x
YL = Y0 + 20000 * K   # the ceiling line


def yv(n):
    return Y0 + n * K


def bar_rect(x, n0, n1, color, op=0.5, sw=3):
    h = max((n1 - n0) * K, 0.01)
    return Rectangle(width=BW, height=h, stroke_color=color, stroke_width=sw, fill_color=color,
                     fill_opacity=op).move_to([x, yv(n0) + h / 2, 0])


class Chart:
    def __init__(s):
        s.base = Line([-5.9, Y0, 0], [2.3, Y0, 0], color=GREY, stroke_width=3)
        s.zero = T("0", 26, GREY).move_to([-6.3, Y0, 0])
        s.unit = T("chick leg-column motor neurons", 26, GREY).move_to([-6.5, 3.55, 0], aligned_edge=LEFT)
        s.nbar = bar_rect(XN, 0, 12000, BLUE)
        s.nval = T("12,000", 30, BLUE, weight=BOLD).move_to([XN, yv(12000) + 0.35, 0])
        s.nlab = T("normal\nsurvivors", 26, BLUE, line_spacing=0.9).move_to([XN, Y0 - 0.6, 0])
        s.gq = bar_rect(XG, 0, 12000, GHOSTC, 0.2, 3)
        s.q = T("?", 64, GHOSTC, weight=BOLD).move_to([XG, yv(6000), 0])
        s.glab = T("hypothetical:\nsupport doubled", 26, GHOSTC, line_spacing=0.9).move_to([XG, Y0 - 0.6, 0])
        s.g24 = bar_rect(XG, 0, 24000, GHOSTC, 0.2, 3)
        s.g24val = T("24,000", 30, GHOSTC, weight=BOLD).move_to([XG, yv(24000) + 0.35, 0])
        s.gtxt = T("copy:\ndoubled", 28, GHOSTC, line_spacing=0.9).move_to([XG, yv(8000), 0])
        # dims the part of the copy bar above the ceiling
        s.gcap = Rectangle(width=BW, height=(24000 - 20000) * K, stroke_width=0, fill_color=BG,
                           fill_opacity=0.8).move_to([XG, (yv(20000) + yv(24000)) / 2, 0])
        s.cline = DashedLine([-5.9, YL, 0], [3.05, YL, 0], color=TEXT, stroke_width=4, dash_length=0.2)
        s.cline_hi = DashedLine([-5.9, YL, 0], [3.05, YL, 0], color=TEXT, stroke_width=8, dash_length=0.2)
        s.cval = T("about 20,000", 30, TEXT, weight=BOLD).move_to([RC, YL, 0])
        s.cpk = T("present at the peak", 26, TEXT).move_to([RC, YL - 0.5, 0])
        s.cbig = T("ceiling", 40, TEXT, weight=BOLD).move_to([RC, YL + 0.65, 0])
        s.csub = T("if no new neurons join\nafter the peak", 24, TEXT, line_spacing=0.9).move_to([RC, YL - 0.8, 0])
        s.obar = bar_rect(XO, 0, 13300, YELLOW)
        s.oext = bar_rect(XO, 13300, 15400, YELLOW, 0.2, 2.5)
        s.oval = T("13,300", 28, YELLOW, weight=BOLD).move_to([XO, yv(13300) + 0.35, 0])
        s.oval2 = T("13,300 to 15,400", 26, YELLOW, weight=BOLD).move_to([XO, yv(15400) + 0.35, 0])
        s.olab = T("vigorously\nmoving grafts", 26, YELLOW, line_spacing=0.9).move_to([XO, Y0 - 0.6, 0])
        s.ref = DashedLine([XO - 1.1, yv(12000), 0], [XO + 1.15, yv(12000), 0], color=TEXT, stroke_width=3,
                           dash_length=0.12)
        bx = XO + 1.35

        def brk(top):
            return VGroup(Line([bx, yv(12000), 0], [bx, yv(top), 0], color=YELLOW, stroke_width=5),
                          Line([bx - 0.12, yv(12000), 0], [bx + 0.12, yv(12000), 0], color=YELLOW, stroke_width=5),
                          Line([bx - 0.12, yv(top), 0], [bx + 0.12, yv(top), 0], color=YELLOW, stroke_width=5))
        s.brk1 = brk(13300)
        s.brk2 = brk(15400)
        s.bl1 = T("+11%", 28, YELLOW, weight=BOLD).next_to(s.brk1[0], RIGHT, buff=0.22)
        s.bl2 = T("+11% to +28%", 28, YELLOW, weight=BOLD).next_to(s.brk2[0], RIGHT, buff=0.22)
        s.notes = T("selected graft cases;\n1976 percentages applied\nto 1975 counts:\nan illustration", 24, GREY,
                    line_spacing=0.9).move_to([RC + 0.15, -1.75, 0])
        s.qtxt = T("Could the\nsurvivors\ndouble too?", 44, TEXT, font=TITLE_FONT, line_spacing=0.95).move_to([RC, 0.6, 0])
        s.prompt = bchip("Pause and predict", TEAL, 28).move_to([RC, -1.5, 0])

    def common(s):
        return [s.base, s.zero, s.unit]

    def stage1(s):
        return s.common() + [s.nbar, s.nval, s.nlab, s.gq, s.q, s.glab, s.qtxt, s.prompt]

    def stage3(s):
        return s.common() + [s.nbar, s.nval, s.nlab, s.g24, s.g24val, s.gtxt, s.glab, s.gcap, s.cline, s.cval, s.cpk]

    def stage4(s):
        return s.common() + [s.nbar, s.nval, s.nlab, s.g24, s.g24val, s.gtxt, s.glab, s.gcap, s.cline_hi, s.cval,
                             s.cbig, s.csub]

    def stage5(s):
        return [m for m in s.stage4() if m is not s.csub] + [s.obar, s.oext, s.oval2, s.olab, s.ref, s.brk2, s.bl2]


def rise_bar(scene, mob, x, v0, v1, color, op, sw, t):
    def f(m, a):
        m.become(bar_rect(x, 0, v0 + (v1 - v0) * smooth(a), color, op, sw))
    scene.play(UpdateFromAlphaFunc(mob, f), run_time=t)


# ---------------------------------------------------------------------------------------------
# dial
D_START = 210 * DEGREES
D_SWEEP = -240 * DEGREES
D_CEIL = 0.72


def dial_angle(f):
    return D_START + D_SWEEP * f


def make_dial(c, r, f, color=YELLOW, ceil=True, hi=False, stop_w=9):
    c3 = np.array([c[0], c[1], 0.0])
    f = max(f, 0.004)
    usable = Arc(radius=r, start_angle=D_START, angle=D_SWEEP * D_CEIL, arc_center=c3, stroke_color=GREY,
                 stroke_width=8)
    beyond = Arc(radius=r, start_angle=dial_angle(D_CEIL), angle=D_SWEEP * (1 - D_CEIL), arc_center=c3,
                 stroke_color=GREY, stroke_width=8).set_stroke(opacity=0.3)
    prog = Arc(radius=r, start_angle=D_START, angle=D_SWEEP * f, arc_center=c3, stroke_color=color, stroke_width=11)
    a = dial_angle(D_CEIL)
    u = np.array([math.cos(a), math.sin(a), 0.0])
    stop = Line(c3 + u * (r - 0.22), c3 + u * (r + 0.26), color=TEXT, stroke_width=stop_w + (5 if hi else 0))
    th = dial_angle(f)
    v = np.array([math.cos(th), math.sin(th), 0.0])
    ptr = Line(c3, c3 + v * r * 0.8, color=TEXT, stroke_width=6)
    hub = Dot(c3, radius=0.13, color=TEXT)
    return VGroup(usable, beyond, prog, stop, ptr, hub)


def dial_updater(mob, c, r, f0, f1, color=YELLOW):
    def f(m, a):
        m.become(make_dial(c, r, f0 + (f1 - f0) * smooth(a), color))
    return UpdateFromAlphaFunc(mob, f)


def turn_dial(scene, mob, c, r, f0, f1, t, color=YELLOW):
    scene.play(dial_updater(mob, c, r, f0, f1, color), run_time=t)


def stop_pos(c, r, extra=0.0):
    a = dial_angle(D_CEIL)
    return np.array([c[0] + math.cos(a) * (r + 0.26 + extra), c[1] + math.sin(a) * (r + 0.26 + extra), 0.0])


DC = (4.75, -1.55)
DRAD = 1.55
DIAL_F = 0.25


# ---------------------------------------------------------------------------------------------
# cord column, graft, muscle (scenes 8 to 10)
COLX, GX, CY = -2.3, 3.4, 0.1
CW, CH = 1.9, 5.4
COL_IDX_RED = [1, 4, 6, 9, 11, 14, 16, 19, 22, 25]   # the ten that die when nothing is done
COL_FEW = [4, 14, 22]                                 # the three that still die with curare
COL_RESCUED = [i for i in COL_IDX_RED if i not in COL_FEW]


def column_box():
    return RoundedRectangle(corner_radius=0.3, width=CW, height=CH, stroke_color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.1).move_to([COLX, CY, 0])


def column_dots():
    ds = VGroup()
    for i in range(9):
        for j in range(3):
            ds.add(Dot([COLX + (j - 1) * 0.55, CY + 2.32 - i * 0.58, 0], radius=0.2, color=BLUE))
    return ds


def graft_ellipse():
    return Ellipse(width=4.0, height=2.8, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                   fill_opacity=0.22).move_to([GX, CY, 0])


def muscle(color=YELLOW):
    sp = Ellipse(width=4.2, height=1.9, stroke_color=color, stroke_width=4, fill_color=color,
                 fill_opacity=0.3).move_to([GX, CY, 0])
    fib = VGroup(*[Line([GX - 1.8 + abs(dy) * 0.6, CY + dy, 0], [GX + 1.8 - abs(dy) * 0.6, CY + dy, 0], color=color,
                        stroke_width=2).set_stroke(opacity=0.7) for dy in (-0.5, 0.0, 0.5)])
    return VGroup(sp, fib)


NX0, NX1 = COLX + CW / 2 + 0.05, GX - 2.0
NYS = [CY + 1.5, CY + 0.5, CY - 0.5, CY - 1.5]


def _npt(y, t):
    ye = CY + (y - CY) * 0.45
    return [NX0 + (NX1 - NX0) * t, y + (ye - y) * t, 0]


def nerves_full():
    g = VGroup()
    for y in NYS:
        g.add(Line(_npt(y, 0), _npt(y, 1), color=BLUE, stroke_width=5))
    return g


def nerves_patchy():
    """thin, broken, partly missing: a few short pieces only (the lower-middle nerve is absent)."""
    pieces = {0: [(0.0, 0.22), (0.36, 0.52), (0.72, 0.82)], 1: [(0.0, 0.3), (0.5, 0.58)], 2: [],
              3: [(0.0, 0.2), (0.45, 0.62), (0.8, 0.95)]}
    g = VGroup()
    for k, y in enumerate(NYS):
        for a, b in pieces[k]:
            g.add(Line(_npt(y, a), _npt(y, b), color=BLUE, stroke_width=3.5).set_stroke(opacity=1))
    return g


def s8_state():
    """the graft picture that scenes 8 and 9 share."""
    box, dots = column_box(), column_dots()
    graft = graft_ellipse()
    glab = T("graft", 32, YELLOW).move_to([GX, CY, 0])
    dial2 = make_dial((-5.3, 0.9), 0.95, DIAL_F)
    dlab = T("turned only\na little", 26, GREY, line_spacing=0.9).move_to([-5.3, -0.55, 0])
    unk = T("how much support it gave\nis unknown", 30, YELLOW, line_spacing=0.9).move_to([GX, -2.75, 0])
    return box, dots, graft, glab, dial2, dlab, unk


# ---------------------------------------------------------------------------------------------
# tubes (scenes 18 to 18f)
_rs = random.Random(11)
FADE_SET = sorted(_rs.sample(range(40), 15))
_rs2 = random.Random(2)
JIT = [(_rs2.uniform(-0.1, 0.1), _rs2.uniform(-0.1, 0.1)) for _ in range(40)]
FADE_FEW = [FADE_SET[i] for i in (0, 4, 8, 12)]   # the four that still fade with a synthesis blocker


def make_tube(cx, cy, w, h, r, color=BLUE, fill=0.1):
    box = RoundedRectangle(corner_radius=min(0.45, h * 0.25), width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=fill).move_to([cx, cy, 0])
    dots = VGroup()
    sx, sy = w / 8.6, h / 5.6
    for i in range(5):
        for j in range(8):
            jx, jy = JIT[i * 8 + j]
            dots.add(Dot([cx + (j - 3.5) * sx + jx * sx, cy + (2 - i) * sy + jy * sy, 0], radius=r, color=BLUE))
    return box, dots


def ghost_all(dots):
    for i in FADE_SET:
        set_ghost(dots[i])


CORD_W, CORD_H, CORD_R, CORD_Y = 3.0, 4.3, 0.13, 0.25
CORD_XS = [-4.95, -1.65, 1.65, 4.95]   # slot 0 is cervical


def cord_slots():
    return [RoundedRectangle(corner_radius=0.4, width=CORD_W, height=CORD_H, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.08).move_to([x, CORD_Y, 0]) for x in CORD_XS]


def cord_other_labels():
    x0, x1 = CORD_XS[1] - CORD_W / 2, CORD_XS[3] + CORD_W / 2
    y = CORD_Y - CORD_H / 2 - 0.3
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=4),
                Line([x0, y + 0.12, 0], [x0, y - 0.12, 0], color=GREY, stroke_width=4),
                Line([x1, y + 0.12, 0], [x1, y - 0.12, 0], color=GREY, stroke_width=4))
    lab = T("other levels", 28, GREY).move_to([(x0 + x1) / 2, y - 0.5, 0])
    return br, lab


def cord_cerv_label():
    return T("cervical\n(neck level)", 28, BLUE, line_spacing=0.9).move_to(
        [CORD_XS[0], CORD_Y - CORD_H / 2 - 0.75, 0])


def cord_cerv_tube():
    box, dots = make_tube(CORD_XS[0], CORD_Y, CORD_W, CORD_H, CORD_R)
    box.set_stroke(BLUE, 5).set_fill(BLUE, 0.15)
    return box, dots


MX, MY, MZ = 0.0, -0.1, 1.4     # where the moved tube ends up (centre, zoom)


def moved_final():
    """scene 18e's last picture: the moved tube zoomed to fill the frame, day 5, same dots gone."""
    box, dots = make_tube(MX, MY, CORD_W, CORD_H, CORD_R)
    box.set_stroke(BLUE, 5).set_fill(BLUE, 0.15)
    ghost_all(dots)
    tube = VGroup(box, dots).scale(MZ).move_to([MX, MY, 0])
    lab = T("the cervical tube, moved to another level", 30, TEXT).move_to([MX, 3.45, 0])
    d5 = bchip("day 5", TEXT, 44).move_to([5.0, 0.4, 0])
    return tube, lab, d5


# ---------------------------------------------------------------------------------------------
# dose plot (scenes 13 to 15b)
PX0, PY0, PW, PH = -4.4, -2.35, 10.2, 4.9
DOSES = [100, 1000, 5000, 20000]


def u_of(d):
    return (math.log10(d) - 1.7) / 2.9


def PP(u, v):
    return np.array([PX0 + u * PW, PY0 + v * PH, 0.0])


def toy(d):
    return max(0.0, 1.0 - 1000.0 / d)


class DosePlot:
    def __init__(s):
        s.axes = VGroup(Line(PP(0, 0), PP(1.0, 0), color=GREY, stroke_width=3),
                        Line(PP(0, 0), PP(0, 1.06), color=GREY, stroke_width=3))
        s.yl = VGroup(*[T(t, 26, GREY).move_to(PP(0, v) + LEFT * 0.6) for t, v in (("0%", 0), ("50%", 0.5), ("100%", 1.0))])
        s.ylab = T("fraction dying", 26, GREY).rotate(90 * DEGREES).move_to([-6.4, PY0 + PH / 2, 0])
        s.xt = VGroup(*[VGroup(Line(PP(u_of(d), 0), PP(u_of(d), 0) + DOWN * 0.15, color=GREY, stroke_width=3),
                               T(f"{d:,}", 26, GREY).move_to(PP(u_of(d), 0) + DOWN * 0.5)) for d in DOSES])
        s.xlab = T("dose (cells transplanted, log scale)", 26, GREY).move_to([PX0 + PW / 2, -3.5, 0])
        s.cap = DashedLine(PP(u_of(1000), 0), PP(u_of(1000), 1.06), color=TEXT, stroke_width=3, dash_length=0.15)
        s.cap_l = T("host supports only\n1,000 cells", 26, TEXT, line_spacing=0.9).next_to(PP(u_of(1000), 0.9), LEFT, buff=0.2)
        s.chip_toy = bchip("toy model", GREY, 30).move_to(PP(0.18, 0.55))
        s.qtxt = T("What fraction dies as the dose rises?", 38, TEXT, font=TITLE_FONT).move_to([0.6, 3.4, 0])
        s.prompt = bchip("Pause and sketch", TEAL, 28).move_to(PP(0.8, 0.12))
        s.sch = T("hypothetical", 26, GREY).move_to(PP(0.2, 0.36))

        def curve(f, u0, u1, n=80, color=GREY, w=7):
            pts = [PP(u, f(10 ** (1.7 + 2.9 * u))) for u in np.linspace(u0, u1, n)]
            return VMobject(stroke_color=color, stroke_width=w, fill_opacity=0).set_points_as_corners(pts)
        s.curve_a = curve(toy, u_of(100), u_of(1000), 20)
        s.curve_b = curve(toy, u_of(1000), u_of(20000), 90)
        s.dots = [Dot(PP(u_of(d), toy(d)), radius=0.14, color=GREY) for d in DOSES]
        s.dlabs = [T(t, 28, GREY, weight=BOLD) for t in ("0%", "0%", "80%", "95%")]
        offs = [(0.0, 0.5), (-0.55, 0.5), (-0.8, 0.45), (-0.85, 0.45)]   # above and left of each point
        for lab, d, (ox, oy) in zip(s.dlabs, s.dots, offs):
            lab.move_to(d.get_center() + np.array([ox, oy, 0]))
        # A separate annotation above the plot has no y-axis position or extent.
        # Its open bracket refers to the range of doses, not a measured fraction.
        s.band = VGroup(Line([-3.8, 3.05, 0], [5.5, 3.05, 0], color=RED, stroke_width=4),
                        Line([-3.8, 3.05, 0], [-3.8, 2.85, 0], color=RED, stroke_width=4),
                        Line([5.5, 3.05, 0], [5.5, 2.85, 0], color=RED, stroke_width=4))
        s.obs = T("same fraction died at every dose tested", 30, RED, weight=BOLD).move_to([0.85, 3.5, 0])
        s.schem = T("schematic:\nfraction not specified", 32, TEXT, line_spacing=0.95).move_to([-2.0, 1.45, 0])

    def base_mobs(s):
        return [s.axes, s.yl, s.ylab, s.xt, s.xlab, s.cap, s.cap_l]


# ---------------------------------------------------------------------------------------------
# rule card
def rule_card():
    card = RoundedRectangle(corner_radius=0.3, width=11.4, height=3.5, stroke_color=GOLD, stroke_width=3,
                            fill_color=GOLD, fill_opacity=0.06)
    lab = T("THE RULE", 22, GOLD, weight=BOLD).move_to([0, 1.2, 0])
    l1 = T("Make too many.", 46, TEXT, font=TITLE_FONT).move_to([0, 0.35, 0])
    l2 = T("Then let the target keep what it can support.", 38, TEXT, font=TITLE_FONT).move_to([0, -0.7, 0])
    return card, lab, l1, l2


def rule_group():
    card, lab, l1, l2 = rule_card()
    return VGroup(card, lab, l1, l2).move_to([0, 0.2, 0])


def scope_tags():
    t1 = bchip("many peripheral neurons", BLUE, 36).move_to([0, 2.95, 0])
    t2 = bchip("motor neurons at their muscles", BLUE, 36).move_to([0, -2.55, 0])
    return t1, t2


def clock(c, r, color=BLUE):
    c3 = np.array([c[0], c[1], 0.0])
    face = Circle(radius=r, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.12).move_to(c3)
    h1 = Line(c3, c3 + np.array([0, r * 0.62, 0]), color=color, stroke_width=5)
    h2 = Line(c3, c3 + np.array([r * 0.45, -r * 0.15, 0]), color=color, stroke_width=5)
    return VGroup(face, h1, h2, Dot(c3, radius=0.07, color=color))


# the "own clock" picture (scenes 16, 16b, 17)
OL, OHX, OHY, ODY = 9.4, -0.4, 2.0, 0.1
OFF0, OFF1 = 1.0, 2.2


def own_objs(off):
    left = OHX - OL / 2

    def age_bar(cx, cy, color):
        bar = Rectangle(width=OL, height=0.9, stroke_color=color, stroke_width=3, fill_color=color,
                        fill_opacity=0.28).move_to([cx, cy, 0])
        tk = VGroup(*[Line([cx - OL / 2 + i * OL / 10, cy + 0.45, 0], [cx - OL / 2 + i * OL / 10, cy + 0.62, 0],
                           color=color, stroke_width=3) for i in range(11)])
        return VGroup(bar, tk)
    host = age_bar(OHX, OHY, GREY)
    donor = age_bar(OHX + off, ODY, BLUE)
    hl = VGroup(T("host age", 30, GREY), Arrow([0, 0, 0], [0.7, 0, 0], buff=0, color=GREY, stroke_width=4,
                                                 tip_length=0.2)).arrange(RIGHT, buff=0.2)
    hl.move_to([left + 1.5, OHY + 0.95, 0])
    dl = VGroup(T("donor age", 30, BLUE), Arrow([0, 0, 0], [0.7, 0, 0], buff=0, color=BLUE, stroke_width=4,
                                                       tip_length=0.2)).arrange(RIGHT, buff=0.2)
    dl.move_to([left + off + 1.5, ODY + 0.95, 0])
    xg = left + 0.65 * OL
    win = Rectangle(width=1.3, height=1.3, stroke_color=RED, stroke_width=4, fill_color=BLUE,
                    fill_opacity=0.75).move_to([xg + off, ODY, 0])
    wl = T("death", 28, RED, weight=BOLD).next_to(win, DOWN, buff=0.12)
    guide = DashedLine([xg, OHY - 0.45, 0], [xg, ODY - 1.2, 0], color=GREY, stroke_width=3, dash_length=0.12)
    gl = T("if the host's age set it", 24, GREY).move_to([xg - 2.2, ODY - 1.4, 0])
    return host, donor, hl, dl, win, wl, guide, gl


def own_clock():
    ck = clock([-4.2, -2.65, 0], 0.8)
    ckl = T("own clock", 38, BLUE, weight=BOLD).move_to([-1.5, -2.45, 0])
    sep = T("a separate result", 26, GREY).move_to([-1.5, -3.1, 0])
    return ck, ckl, sep


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Too Many Neurons: Naturally Occurring Cell Death"
    TITLE = "A Dial With a Ceiling"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        c = Chart()
        self.at("The extra leg")
        self.add(c.base)
        self.play(FadeIn(c.zero), FadeIn(c.unit), FadeIn(c.nlab), run_time=0.4)
        rise_bar(self, c.nbar, XN, 0, 12000, BLUE, 0.5, 3, 1.0)
        self.play(FadeIn(c.nval), run_time=0.4)
        self.at("Suppose it doubled")
        self.play(FadeIn(c.gq), FadeIn(c.q, scale=0.5), FadeIn(c.glab), run_time=0.8)
        self.at("Could the survivors")
        self.play(FadeIn(c.qtxt, shift=LEFT * 0.2), run_time=0.8)
        self.at("double too")
        self.play(FadeIn(c.prompt, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S02Pause(SpokenScene):
    def construct(self):
        c = Chart()
        self.add(*c.stage1())
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Rev(SpokenScene):
    def construct(self):
        c = Chart()
        self.add(*c.stage1())
        self.at("Twice")
        self.play(FadeOut(c.qtxt), FadeOut(c.prompt), FadeOut(c.q), run_time=0.4)
        rise_bar(self, c.gq, XG, 12000, 24000, GHOSTC, 0.2, 3, 1.4)
        self.play(FadeIn(c.g24val), FadeIn(c.gtxt), run_time=0.5)
        self.at("but only about")
        self.add(c.gcap)
        c.gcap.set_opacity(0)
        c.gcap.set_fill(BG, opacity=0)
        self.play(Create(c.cline), c.gcap.animate.set_fill(BG, opacity=0.8), run_time=0.9)
        self.at("about 20")
        self.play(FadeIn(c.cval, shift=LEFT * 0.2), run_time=0.6)
        self.at("were present")
        self.play(FadeIn(c.cpk, shift=LEFT * 0.2), Indicate(c.cline, color=TEXT, scale_factor=1.0), run_time=0.8)
        self.finish()


class S04Ceiling(SpokenScene):
    def construct(self):
        c = Chart()
        self.add(*c.stage3())
        self.at("If no new neurons")
        self.play(FadeOut(c.cpk), FadeIn(c.csub), run_time=0.7)
        self.at("no target can rescue")
        self.wait(0.1)
        self.at("That is the ceiling")
        self.play(ReplacementTransform(c.cline, c.cline_hi), FadeIn(c.cbig, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


class S05Obs(SpokenScene):
    def construct(self):
        c = Chart()
        self.add(*c.stage4())
        self.play(FadeOut(c.csub), run_time=0.5)
        self.at("well below it")
        self.add(c.obar)
        c.obar.become(bar_rect(XO, 0, 1, YELLOW))
        self.play(FadeIn(c.olab), run_time=0.3)
        rise_bar(self, c.obar, XO, 0, 13300, YELLOW, 0.5, 3, 1.0)
        self.play(FadeIn(c.oval), run_time=0.4)
        self.at("In embryos")
        self.play(FadeIn(c.notes), run_time=0.6)
        self.at("survivors rose")
        self.play(Create(c.ref), run_time=0.5)
        self.at("a tenth")
        self.play(Create(c.brk1), FadeIn(c.bl1), run_time=0.5)
        self.at("over a quarter")
        self.play(FadeIn(c.oext), ReplacementTransform(c.brk1, c.brk2), ReplacementTransform(c.bl1, c.bl2),
                  ReplacementTransform(c.oval, c.oval2), run_time=0.9)
        self.finish()


class S06Beat(SpokenScene):
    def construct(self):
        c = Chart()
        self.add(*c.stage5(), c.notes)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Dial(SpokenScene):
    def construct(self):
        c = Chart()
        self.add(*c.stage5())
        self.add(c.notes)
        dial = make_dial(DC, DRAD, 0.0)
        tchip = bchip("target", YELLOW, 30).move_to([RC, -3.3, 0])
        more = bchip("more target", YELLOW, 30).move_to([RC, -3.3, 0])
        fewer = bchip("fewer deaths", RED, 30).move_to([RC, -3.3, 0])
        cl = T("ceiling", 30, TEXT, weight=BOLD).move_to([6.05, 0.8, 0])
        cl_ld = Line([6.1, 0.55, 0], stop_pos(DC, DRAD) + np.array([0.0, 0.05, 0]), color=TEXT, stroke_width=3)
        dl = T("a dial with a ceiling", 28, TEXT).move_to([RC, -3.3, 0])
        pointer = arr([4.2, -0.15, 0], [3.75, 0.12, 0], YELLOW, 5, 0.2)
        # clear every old label from the right column before the dial arrives
        self.play(FadeOut(c.notes), run_time=0.5)
        self.at("turns a dial")
        self.play(FadeIn(dial), FadeIn(tchip, shift=DOWN * 0.15), run_time=0.7)
        self.at("More target")
        self.play(ReplacementTransform(tchip, more), dial_updater(dial, DC, DRAD, 0.0, DIAL_F), run_time=1.0)
        self.at("fewer deaths")
        self.play(ReplacementTransform(more, fewer), GrowArrow(pointer), run_time=0.5)
        self.at("up to the ceiling")
        self.play(ReplacementTransform(fewer, dl), FadeOut(c.cbig), FadeIn(cl), Create(cl_ld),
                  Indicate(dial[3], color=TEXT, scale_factor=1.6), run_time=0.9)
        self.finish()


class S08Why(SpokenScene):
    def construct(self):
        # hard cut to the graft picture, with the dial shrunk at the left
        box, dots, graft, glab, dial2, dlab, unk = s8_state()
        self.add(box, dots, graft, glab, dial2, dlab)
        qm = T("?", 110, GREY, weight=BOLD).move_to([(NX0 + NX1) / 2, CY, 0])
        ner = nerves_patchy()
        self.at("turn so little")
        self.play(Indicate(dial2, color=YELLOW, scale_factor=1.12), run_time=0.9)
        self.at("experiment cannot tell")
        self.play(FadeIn(qm, scale=0.6), FadeIn(unk, shift=UP * 0.1), run_time=0.8)
        self.at("partly innervated")
        self.play(FadeOut(qm), LaggedStart(*[Create(m) for m in ner], lag_ratio=0.06), run_time=0.65)
        self.finish()


class S09Act(SpokenScene):
    def construct(self):
        box, dots, graft, glab, dial2, dlab, unk = s8_state()
        ner = nerves_patchy()
        self.add(box, dots, graft, glab, dial2, dlab, unk, ner)
        mus = muscle()
        mlab = T("activity at the muscle", 30, GREEN).move_to([GX, CY - 1.6, 0])
        nfull = nerves_full()
        self.at("Activity at")
        self.play(FadeOut(dial2), FadeOut(dlab), FadeOut(unk), FadeOut(glab), ReplacementTransform(graft, mus[0]),
                  FadeIn(mus[1]), ReplacementTransform(ner, nfull), FadeIn(mlab), run_time=0.6)
        for k in range(2):
            ring = Ellipse(width=4.2, height=1.9, stroke_color=GREEN, stroke_width=5)
            ring.move_to([GX, CY, 0])
            self.play(ring.animate.scale(1.5).set_stroke(opacity=0), run_time=0.7)
            self.remove(ring)
        self.finish()


class S10Curare(SpokenScene):
    def construct(self):
        box, dots = column_box(), column_dots()
        mus = muscle()
        nfull = nerves_full()
        mlab = T("activity at the muscle", 30, GREEN).move_to([GX, CY - 1.6, 0])
        self.add(box, dots, mus, nfull, mlab)
        die = [dots[i] for i in COL_IDX_RED]
        few = [dots[i] for i in COL_FEW]
        rescued = [dots[i] for i in COL_RESCUED]
        normal = T("normal: many die", 30, RED, weight=BOLD).move_to([COLX, -3.3, 0])
        withc = T("with curare: fewer die", 30, BLUE, weight=BOLD).move_to([COLX, -3.3, 0])
        cur = bchip("curare", TEXT, 34).move_to([GX, CY + 1.55, 0])
        par_t = T("paralysed", 32, TEXT)
        par = VGroup(RoundedRectangle(corner_radius=0.12, width=par_t.width + 0.4, height=par_t.height + 0.3,
                                      stroke_width=0, fill_color=BG, fill_opacity=0.9).move_to(par_t), par_t
                     ).move_to([GX, CY, 0])
        mus_g = muscle(GREY)
        # 1: untreated, some die
        self.at("In chick embryos")
        self.play(LaggedStart(*[d.animate.set_color(RED) for d in die], lag_ratio=0.08), run_time=0.5)
        self.play(LaggedStart(*[ghost_anim(d) for d in die], lag_ratio=0.08), FadeIn(normal, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)
        # 2: curare on, muscle paralysed, every dot reset to neutral in the same beat
        self.at("paralyzing the muscle")
        self.play(FadeOut(normal), FadeOut(mlab), Transform(mus, mus_g), FadeIn(cur, shift=DOWN * 0.15), FadeIn(par),
                  *[refill_anim(d) for d in die], run_time=0.8)
        # 3: run it again, clearly fewer die
        self.at("rescues")
        self.play(LaggedStart(*[d.animate.set_color(RED) for d in few], lag_ratio=0.25), run_time=0.7)
        self.play(LaggedStart(*[ghost_anim(d) for d in few], lag_ratio=0.25), FadeIn(withc, shift=UP * 0.1), run_time=0.8)
        # 4: the rescued ones are marked
        self.at("would otherwise die")
        rings = VGroup(*[Circle(radius=0.3, stroke_color=TEXT, stroke_width=3).move_to(d.get_center()) for d in rescued])
        rl = T("rescued", 30, TEXT, weight=BOLD).move_to([-5.4, 0.1, 0])
        ra = arr(rl.get_right() + RIGHT * 0.05, [COLX - CW / 2 - 0.1, 0.1, 0], TEXT, 4, 0.2)
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.08), FadeIn(rl), GrowArrow(ra), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
ROWY = [1.1, 0.55, 0.0, -0.55, -1.1]


def mini_col(cx, cy, rows):
    box = RoundedRectangle(corner_radius=0.3, width=2.2, height=3.4, stroke_color=BLUE, stroke_width=3,
                           fill_color=BLUE, fill_opacity=0.1).move_to([cx, cy, 0])
    dots = VGroup(*[Dot([cx + (j - 1) * 0.55, cy + ROWY[i], 0], radius=0.18, color=BLUE) for i in rows for j in range(3)])
    return box, dots


class S11Q2(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.3, width=12.0, height=1.9, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([0, 2.7, 0])
        q = T("Is every developmental death the target's doing?", 44, TEXT, font=TITLE_FONT).move_to(card)
        fit(q, max_w=11.2)
        ly = -0.5
        lb, ld = mini_col(-3.7, ly, [0, 1, 2, 3])
        new = VGroup(*[Dot([-3.7 + (j - 1) * 0.55, ly + ROWY[4], 0], radius=0.18, color=BLUE).set_stroke(TEXT, 3)
                       for j in range(3)])
        a = bchip("add cells", BLUE, 36).move_to([-3.7, -2.9, 0])
        mid = T("instead of", 30, GREY).move_to([0.0, ly, 0])
        rb, rd = mini_col(3.7, ly, [0, 1, 2, 3, 4])
        b = bchip("add target", YELLOW, 36).move_to([3.7, -2.9, 0])
        tgt = Ellipse(width=2.0, height=1.5, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                      fill_opacity=0.25).move_to([5.9, ly, 0])
        # the right-hand panel sits at x 2.6 to 6.9; shift the column left a little so the target fits
        right = VGroup(rb, rd, b).shift(LEFT * 0.9)
        tgt.move_to([5.55, ly, 0])
        right.add(tgt)
        self.at("Is every")
        self.play(FadeIn(card), Write(q), run_time=1.6)
        self.add(lb, ld)
        self.play(FadeIn(lb), FadeIn(ld), run_time=0.5)
        self.at("One test adds cells")
        for d in new:
            d.shift(LEFT * 2.6)
        self.play(FadeIn(a, shift=UP * 0.2), FadeIn(new), run_time=0.3)
        self.play(*[d.animate.shift(RIGHT * 2.6) for d in new], lb.animate.set_stroke(TEXT, 4), run_time=0.8)
        self.at("instead of target")
        self.play(FadeIn(mid), FadeIn(right, shift=LEFT * 0.2), run_time=0.7)
        x = VGroup(Line([1.7, ly + 1.9, 0], [6.5, ly - 1.9, 0], color=GREY, stroke_width=8),
                   Line([1.7, ly - 1.9, 0], [6.5, ly + 1.9, 0], color=GREY, stroke_width=8))
        self.play(right.animate.set_opacity(0.4), Create(x), run_time=0.7)
        self.finish()


class S12Setup(SpokenScene):
    def construct(self):
        credit = T("Southwell and colleagues, 2012", 34, GREY).move_to([0, 3.4, 0])
        c1 = bchip("precursors of\ncortical interneurons", BLUE, 30, ).move_to([-3.9, 2.15, 0])
        hbox = RoundedRectangle(corner_radius=0.3, width=3.6, height=1.6, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.12).move_to([2.6, 2.15, 0])
        hlab = T("host mice", 34, TEXT).move_to(hbox)
        ar = arr([-1.35, 2.15, 0], [0.65, 2.15, 0], GREY, 6)
        AX = -1.9
        xs = [-5.0 + 2.5 * k for k in range(5)]
        radii = [0.07 * math.sqrt(200 ** (k / 4)) for k in range(5)]
        axis = Line([-5.6, AX, 0], [5.6, AX, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[Line([x, AX - 0.13, 0], [x, AX + 0.13, 0], color=GREY, stroke_width=3) for x in xs])
        t1 = T("1×", 32, TEXT, weight=BOLD).move_to([xs[0], AX - 0.5, 0])
        t200 = T("200×", 32, TEXT, weight=BOLD).move_to([xs[4], AX - 0.5, 0])
        alab = T("cells transplanted (log scale)", 26, GREY).move_to([0, AX - 0.5, 0])
        circs = VGroup(*[Circle(radius=r, stroke_color=BLUE, stroke_width=3, fill_color=BLUE,
                                fill_opacity=0.35).move_to([x, AX + 0.1 + r, 0]) for x, r in zip(xs, radii)])
        fan = VGroup(*[Line([2.6, 1.35, 0], [x, AX + 0.1 + 2 * r + 0.1, 0], color=GREY, stroke_width=2).set_stroke(opacity=0.7)
                       for x, r in zip(xs, radii)])
        by = -2.95
        brk = VGroup(Line([-5.0, by, 0], [5.0, by, 0], color=TEXT, stroke_width=4),
                     Line([-5.0, by + 0.13, 0], [-5.0, by - 0.13, 0], color=TEXT, stroke_width=4),
                     Line([5.0, by + 0.13, 0], [5.0, by - 0.13, 0], color=TEXT, stroke_width=4))
        blab = T("200-fold range of doses", 32, TEXT, weight=BOLD).move_to([0, -3.45, 0])
        # built big and stacked in the middle of the frame; it settles to the top row when the dose axis arrives
        c1_i = c1.copy().scale(1.3).move_to([0, 1.75, 0])
        hbox_i = hbox.copy().scale(1.3).move_to([0, -1.2, 0])
        hlab_i = hlab.copy().scale(1.3).move_to([0, -1.2, 0])
        ar_i = arr([0, 0.9, 0], [0, -0.05, 0], GREY, 7)
        self.at("Derek Southwell")
        self.play(FadeIn(credit), FadeIn(hbox_i), run_time=0.7)
        self.at("transplanted")
        self.play(FadeIn(c1_i[0]), FadeIn(c1_i[1]), GrowArrow(ar_i), run_time=0.7)
        self.at("precursors of cortical")
        self.play(FadeIn(c1_i[2]), run_time=0.7)
        self.at("into host mice")
        self.play(FadeIn(hlab_i), Indicate(hbox_i, color=GREY, scale_factor=1.06), run_time=0.5)
        self.play(Transform(c1_i, c1), Transform(hbox_i, hbox), Transform(hlab_i, hlab), Transform(ar_i, ar),
                  credit.animate.scale(30 / 34).move_to([0, 3.45, 0]), run_time=0.6)
        self.at("across a")
        self.play(Create(axis), Create(ticks), FadeIn(alab), FadeIn(t1), FadeIn(t200), run_time=0.3)
        self.play(LaggedStart(*[AnimationGroup(Create(f), GrowFromCenter(ci)) for f, ci in zip(fan, circs)],
                              lag_ratio=0.2), run_time=0.8)
        self.at("200 fold")
        self.play(Create(brk), FadeIn(blab), run_time=0.8)
        self.finish()


class S13Pred(SpokenScene):
    def construct(self):
        p = DosePlot()
        self.at("Predict")
        self.play(Create(p.axes), FadeIn(p.ylab), FadeIn(p.yl), FadeIn(p.xt), FadeIn(p.xlab), run_time=0.8)
        self.at("Take a toy model")
        self.play(FadeIn(p.chip_toy, shift=DOWN * 0.15), Create(p.cap), run_time=0.45)
        self.at("can support")
        self.play(FadeIn(p.cap_l), Indicate(p.cap, color=TEXT, scale_factor=1.0), run_time=0.8)
        self.at("What fraction dies")
        self.play(FadeIn(p.qtxt, shift=DOWN * 0.15), Indicate(p.ylab, color=TEXT, scale_factor=1.15), run_time=0.9)
        self.at("the dose rises")
        self.play(FadeIn(p.prompt, shift=DOWN * 0.15), run_time=0.5)
        self.finish()


class S14Pause(SpokenScene):
    def construct(self):
        p = DosePlot()
        self.add(*p.base_mobs(), p.chip_toy, p.qtxt, p.prompt)
        self.finish()


class S15Rev(SpokenScene):
    def construct(self):
        p = DosePlot()
        self.add(*p.base_mobs(), p.chip_toy)
        self.at("In the toy model")
        self.play(FadeIn(p.sch), run_time=0.5)
        self.at("none die")
        self.play(Create(p.curve_a), FadeIn(p.dots[0]), FadeIn(p.dlabs[0]), FadeIn(p.dots[1]), FadeIn(p.dlabs[1]),
                  run_time=1.0)
        self.at("passes a thousand")
        self.play(Indicate(p.cap, color=TEXT, scale_factor=1.0), run_time=0.6)
        self.at("the fraction climbs")
        self.play(Create(p.curve_b), run_time=1.6)
        self.play(FadeIn(p.dots[2]), FadeIn(p.dlabs[2]), run_time=0.4)
        self.at("percent")
        self.play(FadeIn(p.dots[3]), FadeIn(p.dlabs[3]), run_time=0.5)
        self.finish()


class S15bReal(SpokenScene):
    def construct(self):
        p = DosePlot()
        curves = VGroup(p.curve_a, p.curve_b)
        texts = VGroup(*p.dots, *p.dlabs, p.sch)
        self.add(*p.base_mobs(), p.chip_toy, curves, texts)
        self.at("the real result")
        self.play(curves.animate.set_stroke(opacity=0.1), FadeOut(texts),
                  FadeOut(p.cap), FadeOut(p.cap_l), FadeOut(p.chip_toy), run_time=0.8)
        self.at("about the same fraction")
        self.play(Create(p.band), FadeIn(p.obs), FadeIn(p.schem), run_time=0.65)
        self.at("every dose tested")
        self.play(Indicate(p.xt, color=TEXT, scale_factor=1.05), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S16Own(SpokenScene):
    def construct(self):
        host, donor, hl, dl, win, wl, guide, gl = own_objs(OFF0)
        ck, ckl, sep = own_clock()
        self.at("The cells")
        self.play(FadeIn(host), FadeIn(donor), FadeIn(hl), FadeIn(dl), run_time=0.9)
        self.at("at their own age")
        self.play(FadeIn(win), FadeIn(wl), Create(guide), FadeIn(gl), run_time=0.7)
        self.at("not the hosts")
        carried = VGroup(donor, dl, win, wl)
        self.play(carried.animate.shift(RIGHT * (OFF1 - OFF0)), run_time=1.3)
        self.at("They carried")
        self.play(FadeIn(ck, scale=0.6), FadeIn(ckl), FadeIn(sep), run_time=0.8)
        self.finish()


class S16bCircuit(SpokenScene):
    def construct(self):
        host, donor, hl, dl, win, wl, guide, gl = own_objs(OFF1)
        ck, ckl, sep = own_clock()
        self.add(host, donor, hl, dl, win, wl, guide, gl, ck, ckl, sep)
        DC3, DR3 = (2.9, -2.55), 0.95
        dial = make_dial(DC3, DR3, 0.0, GREEN)
        dlab = T("circuit\nactivity", 30, GREEN, line_spacing=0.9).move_to([5.35, -2.55, 0])
        self.at("during this window")
        self.play(Indicate(win, color=RED, scale_factor=1.15), run_time=0.9)
        self.at("circuit activity")
        self.play(FadeIn(dial), FadeIn(dlab), run_time=0.8)
        self.at("tune how many")
        turn_dial(self, dial, DC3, DR3, 0.0, 0.3, 1.0, GREEN)
        self.finish()


class S17Beat(SpokenScene):
    def construct(self):
        host, donor, hl, dl, win, wl, guide, gl = own_objs(OFF1)
        ck, ckl, sep = own_clock()
        dial = make_dial((2.9, -2.55), 0.95, 0.3, GREEN)
        dlab = T("circuit\nactivity", 30, GREEN, line_spacing=0.9).move_to([5.35, -2.55, 0])
        self.add(host, donor, hl, dl, win, wl, guide, gl, ck, ckl, sep, dial, dlab)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18Cerv(SpokenScene):
    def construct(self):
        tubes = cord_slots()
        head = T("chick spinal cord", 34, TEXT).move_to([0, 3.15, 0])
        credit = T("Yaginuma and colleagues, 1996", 26, GREY).move_to([0, -3.55, 0])
        box, dots = cord_cerv_tube()
        clab = cord_cerv_label()
        br, olab = cord_other_labels()
        self.at("The chick has")
        self.play(FadeIn(head), FadeIn(credit), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t) for t in tubes], lag_ratio=0.2), run_time=0.8)
        self.at("neck level")
        self.play(FadeIn(box), FadeIn(dots), FadeIn(clab, shift=UP * 0.1), run_time=0.5)
        self.play(Create(br), FadeIn(olab), run_time=0.5)
        self.at("cervical cord")
        self.play(Indicate(clab, color=BLUE, scale_factor=1.1), run_time=0.6)
        self.finish()


def timeline():
    y = -2.15
    xa, xb = -5.0, -2.8
    segs = VGroup(Line([-6.3, y, 0], [-1.95, y, 0], color=GREY, stroke_width=3),
                  Line([-1.3, y, 0], [6.3, y, 0], color=GREY, stroke_width=3),
                  Line([-1.85, y - 0.2, 0], [-1.6, y + 0.2, 0], color=GREY, stroke_width=3),
                  Line([-1.65, y - 0.2, 0], [-1.4, y + 0.2, 0], color=GREY, stroke_width=3))
    t4 = VGroup(Line([xa, y - 0.13, 0], [xa, y + 0.13, 0], color=GREY, stroke_width=3),
                T("day 4", 30, GREY).move_to([xa, y - 0.5, 0]))
    t5 = VGroup(Line([xb, y - 0.13, 0], [xb, y + 0.13, 0], color=GREY, stroke_width=3),
                T("day 5", 30, GREY).move_to([xb, y - 0.5, 0]))
    return segs, t4, t5, y, xa, xb


def wave_tube():
    box, dots = make_tube(0, 1.3, 10.0, 3.0, 0.2)
    head = T("cervical motor neurons", 32, BLUE).move_to([0, 3.4, 0])
    return box, dots, head


class S18bWhen(SpokenScene):
    def construct(self):
        box, dots, head = wave_tube()
        self.add(box, dots, head)
        segs, t4, t5, y, xa, xb = timeline()
        early = Rectangle(width=xb - xa, height=0.6, stroke_width=0, fill_color=RED, fill_opacity=0.5).move_to(
            [(xa + xb) / 2, y + 0.3, 0])
        early_l = T("early wave", 30, RED).move_to([0, -0.55, 0])
        later = DashedVMobject(Rectangle(width=6.6, height=0.6, stroke_color=GREY, stroke_width=3).move_to([2.0, y + 0.3, 0]),
                               num_dashes=50)
        later_l = T("later death", 28, GREY).move_to([2.0, y + 0.95, 0])
        later_l2 = T("follows target contact", 28, GREY).move_to([2.0, y - 0.5, 0])
        mark = Triangle(color=TEXT, fill_opacity=1, stroke_width=0).scale(0.2).rotate(180 * DEGREES).move_to(
            [xa, y + 0.85, 0])
        self.at("Around day")
        self.play(Create(segs), FadeIn(t4), FadeIn(t5), FadeIn(mark), run_time=0.8)
        self.at("four to five")
        self.play(FadeIn(early), mark.animate.move_to([xb, y + 0.85, 0]), run_time=1.2)
        fade = [dots[i] for i in FADE_SET]
        self.at("a wave of cervical")
        self.play(FadeIn(early_l), LaggedStart(*[d.animate.set_color(RED) for d in fade], lag_ratio=0.1), run_time=1.1)
        self.at("neurons dies")
        self.play(LaggedStart(*[ghost_anim(d) for d in fade], lag_ratio=0.08), run_time=1.0)
        self.at("before the later")
        self.play(FadeIn(later), FadeIn(later_l), run_time=0.6)
        self.at("follows target contact")
        self.play(FadeIn(later_l2, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


TW, TH_, TR_ = 3.3, 4.6, 0.15
TCY = 0.0
TXL, TXR = -5.05, -1.35


def pair_tubes():
    bl, dl_ = make_tube(TXL, TCY, TW, TH_, TR_)
    br, dr_ = make_tube(TXR, TCY, TW, TH_, TR_)
    br.set_stroke(TEXT, 3)
    ghost_all(dl_)
    ghost_all(dr_)
    ll = T("no treatment", 28, GREY).move_to([TXL, TCY - TH_ / 2 - 0.4, 0])
    rl = T("treated", 28, TEXT, weight=BOLD).move_to([TXR, TCY - TH_ / 2 - 0.4, 0])
    eq = T("=", 44, TEXT, weight=BOLD).move_to([(TXL + TXR) / 2, TCY, 0])
    same = T("same dots fade", 34, TEXT, weight=BOLD).move_to([(TXL + TXR) / 2, TCY + TH_ / 2 + 0.5, 0])
    return bl, dl_, br, dr_, ll, rl, eq, same


class S18cTarget(SpokenScene):
    def construct(self):
        bl, dl_, br, dr_, ll, rl, eq, same = pair_tubes()
        self.add(bl, dl_, br, dr_, ll, rl)
        cx = 4.65
        rows = [("bigger target", YELLOW, 2.2), ("paralysis (curare)", TEXT, 0.4), ("trophic factors", TEXT, -1.4)]
        chips, tags, ars = [], [], []
        for txt, col, yy in rows:
            ch = bchip(txt, col, 30).move_to([cx, yy, 0])
            tg = T("= no change", 26, TEXT).next_to(ch, DOWN, buff=0.15)
            ar = arr(ch.get_left(), [TXR + TW / 2 + 0.12, TCY + (yy - 0.3) * 0.3, 0], col, 4)
            chips.append(ch)
            tags.append(tg)
            ars.append(ar)
        self.at("A bigger target")
        self.play(FadeIn(chips[0], shift=LEFT * 0.2), GrowArrow(ars[0]), run_time=0.5)
        self.play(Indicate(dr_, color=BLUE, scale_factor=1.0), FadeIn(tags[0]), run_time=0.7)
        self.at("did not change")
        self.play(FadeIn(eq), FadeIn(same, shift=DOWN * 0.1), run_time=0.7)
        for ph, i in (("nor did paralysis", 1), ("or the trophic", 2)):
            self.at(ph)
            self.play(FadeIn(chips[i], shift=LEFT * 0.2), GrowArrow(ars[i]), FadeIn(tags[i]), run_time=0.4)
        # Preserve a full two-second read of all three interventions.
        self.wait(2.1)
        self.finish()


class S18dActive(SpokenScene):
    def construct(self):
        TX, TY, TWD, THT = -2.9, 0.15, 6.4, 4.5
        box, dots = make_tube(TX, TY, TWD, THT, 0.17)
        # Start the blocker experiment at day 4, before the death wave.
        head = T("cervical motor neurons", 32, BLUE).move_to([TX, 3.0, 0])
        tube_r = TX + TWD / 2
        ch = bchip("drug: blocks RNA or\nprotein synthesis", TEXT, 30).move_to([4.3, 2.0, 0])
        blk = Rectangle(width=0.6, height=2.6, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([tube_r + 0.4, TY, 0])
        ar = arr(ch.get_bottom() + DOWN * 0.02, [tube_r + 0.5, TY + 1.4, 0], TEXT, 5)
        d4 = bchip("day 4", TEXT, 30).move_to([TX, -3.4, 0])
        d5 = bchip("day 5", TEXT, 30).move_to([TX, -3.4, 0])
        fewer = T("fewer die", 30, RED).move_to([TX, -2.65, 0])
        need = T("needs new RNA\nand protein", 36, TEXT, weight=BOLD, line_spacing=0.9).move_to([4.3, -0.3, 0])
        act = T("an active program", 36, YELLOW, weight=BOLD).move_to([4.3, -1.35, 0])
        self.add(box, dots, head, d4, ch, blk)
        few = [dots[i] for i in FADE_FEW]
        self.at("Drugs that block")
        self.play(GrowArrow(ar), run_time=0.7)
        self.at("reduced it")
        self.play(FadeOut(d4), run_time=0.15)
        self.play(FadeIn(d5), run_time=0.2)
        self.play(LaggedStart(*[d.animate.set_color(RED) for d in few], lag_ratio=0.2), run_time=0.6)
        self.play(LaggedStart(*[ghost_anim(d) for d in few], lag_ratio=0.2), FadeIn(fewer), run_time=0.7)
        self.at("So it needs")
        self.play(FadeIn(need, shift=UP * 0.1), run_time=0.7)
        self.at("an active program")
        self.play(FadeIn(act, shift=UP * 0.1), run_time=0.6)
        self.finish()


def outline_slot(x):
    return DashedVMobject(RoundedRectangle(corner_radius=0.4, width=CORD_W, height=CORD_H, stroke_color=BLUE,
                                           stroke_width=3).move_to([x, CORD_Y, 0]), num_dashes=24)


class S18eMoved(SpokenScene):
    def construct(self):
        tubes = cord_slots()
        head = T("chick spinal cord", 34, TEXT).move_to([0, 3.15, 0])
        box, dots = cord_cerv_tube()
        tube = VGroup(box, dots)
        clab = cord_cerv_label()
        br, olab = cord_other_labels()
        self.add(head, *tubes, tube, clab, br, olab)
        outline = outline_slot(CORD_XS[0])
        SMALL = 0.8
        ty = CORD_Y
        tl = T("cervical tube", 30, BLUE, weight=BOLD).move_to([CORD_XS[0], 3.35, 0])
        al = T("another level", 30, TEXT, weight=BOLD).move_to([CORD_XS[2], 2.85, 0])
        d4 = bchip("day 4", TEXT, 44).move_to([5.0, 0.4, 0])
        d5 = bchip("day 5", TEXT, 44).move_to([5.0, 0.4, 0])
        self.add(d4)
        # 1: lift the tube out of its slot, named, with the other slots dimmed
        self.at("Moved")
        self.play(FadeOut(head), FadeOut(clab), FadeOut(br), FadeOut(olab), FadeIn(outline), FadeIn(tl),
                  FadeOut(tubes[1]), tubes[2].animate.set_opacity(0.3), tubes[3].animate.set_opacity(0.3),
                  tube.animate.scale(SMALL).move_to([CORD_XS[0], ty, 0]), run_time=0.6)
        # 2: carry it across, the destination named
        self.at("to another")
        self.play(tube.animate.move_to([CORD_XS[2], ty, 0]), tl.animate.move_to([CORD_XS[2], 3.35, 0]),
                  FadeIn(al), run_time=1.0)
        self.play(FadeOut(tl), run_time=0.1)
        # 3: set it down in another slot
        self.at("of the cord")
        self.play(tube.animate.scale(1 / SMALL).move_to([CORD_XS[2], CORD_Y, 0]), FadeOut(tubes[2]),
                  run_time=0.5)
        # 4: zoom it to fill the frame, day 4 with every dot lit
        self.at("the cervical tube")
        lab = T("the cervical tube, moved to another level", 30, TEXT).move_to([MX, 3.45, 0])
        others = VGroup(tubes[0], tubes[3], outline, al)
        self.play(FadeOut(others), tube.animate.scale(MZ).move_to([MX, MY, 0]), FadeIn(lab), run_time=0.55)
        fade = [dots[i] for i in FADE_SET]
        self.at("still lost")
        self.play(FadeOut(d4), run_time=0.1)
        self.play(FadeIn(d5), run_time=0.15)
        self.play(LaggedStart(*[ghost_anim(d) for d in fade], lag_ratio=0.04), run_time=1.0)
        self.at("on schedule")
        self.play(Indicate(d5, color=TEXT, scale_factor=1.15), run_time=0.8)
        self.finish()


class S18fBeat(SpokenScene):
    def construct(self):
        tube, lab, d5 = moved_final()
        self.add(tube, lab, d5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19Close(SpokenScene):
    def construct(self):
        g = rule_group()
        card, lab, l1, l2 = g
        self.at("So")
        self.play(FadeIn(card), FadeIn(lab), run_time=0.6)
        self.at("make too many")
        self.play(Write(l1), run_time=0.9)
        self.at("then let the target")
        self.play(Write(l2), run_time=1.6)
        self.finish()


class S20Scope(SpokenScene):
    def construct(self):
        g = rule_group()          # same size and place as in scene 19
        self.add(g)
        t1, t2 = scope_tags()
        self.at("That holds")
        self.wait(0.4)
        self.at("many peripheral neurons")
        self.play(FadeIn(t1, shift=DOWN * 0.2), run_time=0.7)
        self.at("motor neurons at")
        self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.7)
        self.finish()


class S21Take(SpokenScene):
    def construct(self):
        # opens on scene 20's last picture and dissolves into the takeaway: no black frame between them
        g = rule_group()
        t1, t2 = scope_tags()
        old = VGroup(g, t1, t2)
        self.add(old)
        C, R_ = (-3.5, 0.2), 2.3
        dial = make_dial(C, R_, 0.0)
        cl = T("ceiling", 32, TEXT, weight=BOLD).move_to(stop_pos(C, R_, 0.55) + RIGHT * 0.25)
        tk = T("TAKEAWAY", 24, GOLD, weight=BOLD).move_to([2.0, 3.35, 0])
        a = T("In the limb,\nthe target helps\nset survival,", 40, TEXT, font=TITLE_FONT, line_spacing=0.95)
        b = T("like a dial with\na ceiling.", 40, YELLOW, font=TITLE_FONT, line_spacing=0.95)
        c = T("Count across time,\nand you can see it.", 34, GREY, font=TITLE_FONT, line_spacing=0.95)
        VGroup(a, b).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([2.7, 0.9, 0])
        c.move_to([2.7, -2.4, 0]).align_to(a, LEFT)
        self.play(FadeOut(old), FadeIn(dial), FadeIn(tk), run_time=0.9)
        self.at("in the limb")
        self.play(FadeIn(a, shift=LEFT * 0.2), run_time=1.2)
        self.at("like a dial")
        self.play(FadeIn(b, shift=LEFT * 0.2), dial_updater(dial, C, R_, 0.0, DIAL_F), run_time=1.2)
        self.play(FadeIn(cl), run_time=0.4)
        self.at("Count across time")
        self.play(FadeIn(c, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S22End(EndCard):
    LINE = "In limbs, targets help set survival, like a dial with a ceiling."
