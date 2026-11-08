"""Counting What Stays  (chapter 5 of the radial glia film series)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, shared by every chapter of this lesson; taken from scenes.old.py)
  BLUE   = the radial glial cell and the progenitor pool (a daughter that stays); a dashed BLUE outline = intermediate progenitor
  GREEN  = a neuron, a daughter that quits, and Q (the fraction that quit)
  TEAL   = cell-cycle events (the numbered cycle boxes, the cell-cycle bar G1 / S / G2 / M)
  GOLD   = the one highlight: evidence tags, citations, the "crossing" marker, "what changed"
  RED    = the open question ("?", the trap, the puzzle cards)
  GREY   = labels, axes, the old reading, de-emphasised things
  TEXT   = neutral white (a daughter before it is sorted, definitions)
  (YELLOW nucleus, PURPLE, ORANGE, PINK are used in other chapters, not here)
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403

FLUID = "#5B86B5"
LGREY = "#BAC0CC"      # brighter grey for corner tags and notes


# ================================================================ the model (computed from the lesson's equation)
def qfun(c, shift=0.0):
    """Q = 1 / (1 + e^-(cycle - 7.5)/1.8), the lesson's illustrative schedule; shift moves the crossing later."""
    return 1.0 / (1.0 + math.exp(-((c - shift) - 7.5) / 1.8))


def run_model(shift=0.0, n=11):
    N, pool, neu, qs = 1.0, [], [], []
    for c in range(1, n + 1):
        q = qfun(c, shift)
        pool.append(N)
        neu.append(2 * N * q)
        qs.append(q)
        N = 2 * N * (1 - q)
    return pool, neu, qs, N


POOL, NEU, QS, _END = run_model(0)
_, NEU1, _, _END1 = run_model(1)
RATIO = sum(NEU1) / sum(NEU)           # about 1.8
assert 1.7 < RATIO < 1.9, RATIO


# ================================================================ small helpers
def left_at(mob, x, y):
    return mob.move_to([x + mob.width / 2, y, 0])


def tb(text, size=24, color=TEXT, pad=0.1, **kw):
    """Text on a dark backing so lines behind it never run through the letters."""
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 2 * pad, height=t.height + 2 * pad, stroke_width=0,
                     fill_color=BG, fill_opacity=0.92).move_to(t)
    g = VGroup(back, t)
    g.set_z_index(8)
    return g


def dot(x, y, r=0.3, color=BLUE, op=0.85, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def ipdot(x, y, r=0.3, color=BLUE):
    """An intermediate progenitor: a faint disc with a dashed BLUE outline."""
    fill = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.14)
    ring = DashedVMobject(Circle(radius=r, stroke_color=color, stroke_width=3.5), num_dashes=14)
    return VGroup(fill, ring).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def check(x, y, s=0.45, color=GREEN):
    c = VMobject(stroke_color=color, stroke_width=11)
    c.set_points_as_corners([[x - s, y, 0], [x - s * 0.35, y - s * 0.75, 0], [x + s, y + s * 0.85, 0]])
    return c


def panel(cx, cy, w, h, color, header, hsize=28, dashed=False):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=3.5,
                           fill_color=color, fill_opacity=0.07).move_to([cx, cy, 0])
    if dashed:
        box = DashedVMobject(box, num_dashes=60)
    head = T(header, hsize, color).move_to([cx, cy + h / 2 - 0.5, 0])
    return VGroup(box, head)


def big(text, cx, cy, color=TEXT, size=96):
    return M(text, size, color).move_to([cx, cy, 0])


def poly(pts, color, w=5):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([np.array(p, dtype=float) for p in pts])
    return m


def slots(n, cx, cy, dx=1.0, dy=0.62):
    """n dot positions in two rows (the top row gets the extra one), centred on (cx, cy)."""
    top = (n + 1) // 2
    bot = n - top
    pts = [[cx + (i - (top - 1) / 2) * dx, cy + dy, 0] for i in range(top)]
    pts += [[cx + (i - (bot - 1) / 2) * dx, cy - dy, 0] for i in range(bot)]
    return pts


def rg_icon(x, y, k=1.0, color=BLUE):
    """A small radial glial cell icon (same look as RGCell: foot, soma, short fibre, foot), centred on the soma at (x, y)."""
    sh = 0.9 * k
    soma = RoundedRectangle(corner_radius=0.4 * k, width=1.15 * k, height=sh, stroke_color=color,
                            stroke_width=3, fill_color=color, fill_opacity=0.35).move_to([x, y, 0])
    top, bot = y + sh / 2, y - sh / 2
    up = top + 0.4 * k
    dn = bot - 0.4 * k
    fib = Line([x, top, 0], [x, up, 0], stroke_color=color, stroke_width=7)
    glow = Line([x, top, 0], [x, up, 0], stroke_color=color, stroke_width=20, stroke_opacity=0.28)
    bfoot = Polygon([x - 0.1 * k, up, 0], [x + 0.1 * k, up, 0], [x + 0.28 * k, up + 0.22 * k, 0],
                    [x - 0.28 * k, up + 0.22 * k, 0], stroke_width=0, fill_color=color, fill_opacity=0.85)
    afoot = Polygon([x - 0.28 * k, dn - 0.22 * k, 0], [x + 0.28 * k, dn - 0.22 * k, 0], [x + 0.1 * k, dn, 0],
                    [x - 0.1 * k, dn, 0], stroke_width=0, fill_color=color, fill_opacity=0.85)
    fib2 = Line([x, bot, 0], [x, dn, 0], stroke_color=color, stroke_width=7)
    return VGroup(glow, fib, fib2, soma, bfoot, afoot)


class RGCell(VGroup):
    """The radial glial cell as a cartoon: apical foot, soma, long fibre, basal foot (no structure drawn)."""

    def __init__(self, x=-4.2, y0=-3.6, y1=3.5, ys=-1.9, k=1.3, color=BLUE):
        sh = 0.9 * k
        afoot = Polygon([x - 0.32 * k, y0, 0], [x + 0.32 * k, y0, 0], [x + 0.12 * k, y0 + 0.3 * k, 0],
                        [x - 0.12 * k, y0 + 0.3 * k, 0], stroke_width=0, fill_color=color, fill_opacity=0.85)
        soma = RoundedRectangle(corner_radius=0.4 * k, width=1.15 * k, height=sh, stroke_color=color,
                                stroke_width=3, fill_color=color, fill_opacity=0.35).move_to([x, ys, 0])
        top = ys + sh / 2
        fibre = Line([x, top, 0], [x, y1 - 0.3 * k, 0], stroke_color=color, stroke_width=8)
        glow = Line([x, top, 0], [x, y1 - 0.3 * k, 0], stroke_color=color, stroke_width=24, stroke_opacity=0.28)
        bfoot = Polygon([x - 0.12 * k, y1 - 0.3 * k, 0], [x + 0.12 * k, y1 - 0.3 * k, 0],
                        [x + 0.32 * k, y1, 0], [x - 0.32 * k, y1, 0], stroke_width=0,
                        fill_color=color, fill_opacity=0.85)
        super().__init__(glow, fibre, soma, afoot, bfoot)
        self.soma_c = np.array([x, ys, 0.0])


# ================================================================ cycle boxes and the Q / count plots
def CX(c):
    """x of cycle c (1 to 11) in the shared cycle row."""
    return -5.25 + 1.05 * (c - 1)


def cycle_boxes(y, h, size, w=0.9):
    out = VGroup()
    for c in range(1, 12):
        r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=TEAL, stroke_width=3,
                             fill_color=TEAL, fill_opacity=0.14).move_to([CX(c), y, 0])
        t = M(str(c), size, TEXT).move_to(r)
        out.add(VGroup(r, t))
    return out


def cycle_word(y=-3.1, size=26):
    return T("cycle", size, GREY).move_to([-6.28, y, 0])


def yq(q):
    return -2.2 + 5.0 * q


def q_axes():
    ax = Line([-6.05, yq(0), 0], [-6.05, yq(1) + 0.05, 0], color=GREY, stroke_width=3)
    base = Line([-6.05, yq(0), 0], [5.9, yq(0), 0], color=GREY, stroke_width=3)
    half = DashedVMobject(Line([-6.05, yq(0.5), 0], [5.9, yq(0.5), 0], color=GREY, stroke_width=2.5), num_dashes=46)
    half.set_stroke(opacity=0.8)
    labs = VGroup(T("0", 26, GREY).move_to([-6.45, yq(0), 0]), T("0.5", 26, GREY).move_to([-6.5, yq(0.5), 0]),
                  T("1", 26, GREY).move_to([-6.45, yq(1), 0]))
    qn = T("Q", 34, GREEN, weight=BOLD).move_to([-6.05, yq(1) + 0.45, 0])
    return VGroup(ax, base, half, labs, qn)


def qpt(c):
    return [CX(c), yq(qfun(c)), 0]


def q_curve_pts(c0, c1, n=None):
    n = n or int(40 * (c1 - c0)) + 1
    cs = np.linspace(c0, c1, n)
    return [[CX(1) + 1.05 * (c - 1), yq(qfun(c)), 0] for c in cs]


def q_curve(c0, c1, color=GREEN, dashed=True, op=0.6):
    """The smooth schedule from cycle c0 to c1 (dashed and faint: illustrative)."""
    p = poly(q_curve_pts(c0, c1), color, 5)
    if not dashed:
        return p
    d = DashedVMobject(p, num_dashes=max(6, int(9 * (c1 - c0))))
    d.set_stroke(opacity=op)
    return d


def yn(v):
    return -2.4 + 0.14 * v


def count_axes():
    ax = Line([-6.0, yn(0), 0], [-6.0, yn(40) + 0.05, 0], color=GREY, stroke_width=3)
    base = Line([-6.0, yn(0), 0], [5.9, yn(0), 0], color=GREY, stroke_width=3)
    grid = VGroup(*[Line([-6.0, yn(v), 0], [5.9, yn(v), 0], color=GREY, stroke_width=1.5, stroke_opacity=0.3)
                    for v in (10, 20, 30, 40)])
    labs = VGroup(*[T(str(v), 26, GREY).move_to([-6.42, yn(v), 0]) for v in (0, 10, 20, 30, 40)])
    ylab = left_at(T("cells (expected count)", 26, GREY), -6.5, 3.6)
    return VGroup(grid, ax, base, labs, ylab, cycle_word())


def illus_tag():
    t = T("illustrative model", 26, GOLD)
    return t.move_to([6.5 - t.width / 2, 3.6, 0])


def legend():
    a = VGroup(Line([0, 0, 0], [0.7, 0, 0], color=BLUE, stroke_width=6), T("dividing pool entering the round", 26, BLUE))
    a[1].next_to(a[0], RIGHT, buff=0.2)
    b = VGroup(Line([0, 0, 0], [0.7, 0, 0], color=GREEN, stroke_width=6), T("neurons made this round", 26, GREEN))
    b[1].next_to(b[0], RIGHT, buff=0.2)
    g = VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    g.set_z_index(8)
    return left_at(g, -5.7, 2.5)


def series_pts(series, c0, c1):
    return [[CX(c), yn(series[c - 1]), 0] for c in range(c0, c1 + 1)]


def static_series(series, color, c1):
    pts = series_pts(series, 1, c1)
    g = VGroup()
    for i in range(len(pts) - 1):
        g.add(poly([pts[i], pts[i + 1]], color, 5))
    for p in pts:
        g.add(Dot(p, radius=0.1, color=color))
    return g


def extend_anims(series, color, c0, c1):
    """Animations that continue a curve from cycle c0 to cycle c1 (one segment and one dot per cycle)."""
    pts = series_pts(series, c0, c1)
    anims = []
    for i in range(len(pts) - 1):
        seg = poly([pts[i], pts[i + 1]], color, 5)
        d = Dot(pts[i + 1], radius=0.1, color=color)
        anims.append(AnimationGroup(Create(seg), FadeIn(d, scale=0.5)))
    return anims


# ================================================================ model-stage pieces (scenes 5 to 8)
SL_X0, SL_X1, SL_Y = -3.6, 3.6, 2.85
PL, PR, PY, PW, PH = -3.4, 3.4, -0.25, 5.8, 4.0


def sx(q):
    return SL_X0 + (SL_X1 - SL_X0) * q


def slider_static():
    track = Line([SL_X0, SL_Y, 0], [SL_X1, SL_Y, 0], color=GREY, stroke_width=7)
    ticks = VGroup(*[Line([sx(q), SL_Y - 0.12, 0], [sx(q), SL_Y + 0.12, 0], color=GREY, stroke_width=4) for q in (0, 0.5, 1)])
    labs = VGroup(*[T(s, 26, GREY).move_to([sx(q), SL_Y - 0.48, 0]) for q, s in ((0, "0"), (0.5, "0.5"), (1, "1"))])
    name = T("Q", 40, GREEN, weight=BOLD).move_to([SL_X0 - 0.75, SL_Y, 0])
    return VGroup(track, ticks, labs, name)


def knob(q):
    k = Circle(radius=0.22, stroke_color=TEXT, stroke_width=3, fill_color=GREEN, fill_opacity=1).move_to([sx(q), SL_Y, 0])
    k.set_z_index(5)
    return k


def readout(q):
    return M(f"Q = {q:g}", 32, GREEN).move_to([5.35, SL_Y, 0])


def pool_panel():
    return panel(PL, PY, PW, PH, BLUE, "pool of dividing cells", 28)


def neu_panel(header="neurons made this round"):
    return panel(PR, PY, PW, PH, GREEN, header, 28)


PAIR_X = [-4.65, -1.55, 1.55, 4.65]
DOT_Y = -3.05
DR = 0.42


def pair_dots():
    """Eight daughters in four pairs (stay, quit), the stay one blue, the quit one green; index 0..7."""
    ds = []
    for xc in PAIR_X:
        ds.append(dot(xc - 0.6, DOT_Y, DR, BLUE, 0.85))
        ds.append(dot(xc + 0.6, DOT_Y, DR, GREEN, 0.9))
    return ds


GREEN_ORDER = [1, 3, 5, 7, 0, 2, 4, 6]


def recolor_for(ds, q):
    """Animations that colour round(8q) daughters green and the rest blue."""
    k = int(round(8 * q))
    anims = []
    for i, d in enumerate(ds):
        col = GREEN if GREEN_ORDER.index(i) < k else BLUE
        anims.append(d.animate.set_stroke(col).set_fill(col, opacity=0.9 if col == GREEN else 0.85))
    return anims


def pair_boxes():
    return VGroup(*[RoundedRectangle(corner_radius=0.2, width=2.45, height=1.2, stroke_color=GREY, stroke_width=2.5,
                                     fill_opacity=0).move_to([xc, DOT_Y, 0]) for xc in PAIR_X])


def pause_cue():
    """The 'pause: your turn' cue shared by both pause scenes: text at the top left and a bar that shrinks along the bottom."""
    t = T("pause: what do you think?", 30, GOLD, weight=BOLD)
    t.move_to([-6.6 + t.width / 2, 3.62, 0])
    bar_ = Line([-6.3, -3.74, 0], [6.3, -3.74, 0], color=GOLD, stroke_width=7)
    return t, bar_


# ================================================================ columns (scenes 19 to 22)
COLX = [-5.6, -3.55, -1.5, 0.55]
COLY, COLH, COLW = 0.45, 5.7, 2.0
CNT_X = 5.25
Y_RG, Y_IP, Y_NU = 2.0, 0.85, -0.55


def col_boxes(hl=None):
    g = VGroup()
    for i, x in enumerate(COLX):
        col = GOLD if hl == i else GREY
        r = RoundedRectangle(corner_radius=0.15, width=COLW, height=COLH, stroke_color=col, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.05).move_to([x, COLY, 0])
        h = T(f"cycle {i + 1}", 26, col if hl == i else TEXT).move_to([x, 2.88, 0])
        g.add(VGroup(r, h))
    return g


def rg_counter_panel():
    return panel(CNT_X, 1.6, 3.0, 3.2, BLUE, "radial glia", 28)


def neu_counter_panel():
    return panel(CNT_X, -1.65, 3.0, 2.6, GREEN, "neurons", 28)


RGN_Y, NEUN_Y = 1.8, -1.85


def col_rg(i):
    return dot(COLX[i], Y_RG, 0.38, BLUE, 0.85)


def col_ip(i):
    return ipdot(COLX[i], Y_IP, 0.38)


def col_neurons(i):
    """The two neurons made in cycle i+1 (none in cycle 1)."""
    if i == 0:
        return []
    return [dot(COLX[i] - 0.42, Y_NU, 0.34, GREEN, 0.9), dot(COLX[i] + 0.42, Y_NU, 0.34, GREEN, 0.9)]


def col_tags(i):
    plus = T("+0" if i == 0 else "+2", 30, GREEN, weight=BOLD).move_to([COLX[i], -1.4, 0])
    tot = T(f"total {2 * i}", 26, GREEN).move_to([COLX[i], -1.95, 0])
    return VGroup(plus, tot)


def pool_tag():
    return VGroup(T("pool", 26, GOLD), T("1 → 2", 26, GOLD)).arrange(DOWN, buff=0.05).move_to([COLX[0], Y_NU, 0])


def col_arrow(i):
    """Arrow from the intermediate progenitor of column i-1 to the two neurons it makes in column i."""
    return arr([COLX[i - 1] + 0.4, Y_IP - 0.12, 0], [COLX[i] - 0.5, Y_NU + 0.32, 0], GREY, 3, 0.16)


def ghost_slots():
    """Four-cycle IP waiting: arrow to two empty neuron slots outside the last column, plus their label."""
    ar = arr([COLX[3] + 0.45, Y_IP, 0], [2.0, Y_IP, 0], GREY, 4, 0.2)
    g1 = DashedVMobject(Circle(radius=0.3, stroke_color=GREEN, stroke_width=3.5).move_to([2.4, Y_IP, 0]), num_dashes=12)
    g2 = DashedVMobject(Circle(radius=0.3, stroke_color=GREEN, stroke_width=3.5).move_to([3.05, Y_IP, 0]), num_dashes=12)
    lab = T("next cycle", 26, GREEN).move_to([2.72, 0.2, 0])
    return ar, VGroup(g1, g2), lab


def legend_row():
    """Bottom legend, built in place; parts[0..2] are (RG item, IP item, rule)."""
    rg = VGroup(dot(0, 0, 0.2, BLUE, 0.85), T("radial glial cell", 24, BLUE))
    rg[1].next_to(rg[0], RIGHT, buff=0.15)
    ip = VGroup(ipdot(0, 0, 0.2), T("intermediate progenitor", 24, BLUE))
    ip[1].next_to(ip[0], RIGHT, buff=0.15)
    rule = VGroup(T("divides:", 24, GREY), dot(0, 0, 0.2, GREEN, 0.9), dot(0.45, 0, 0.2, GREEN, 0.9), T("two neurons", 24, GREEN))
    rule[1].next_to(rule[0], RIGHT, buff=0.2)
    rule[2].next_to(rule[1], RIGHT, buff=0.08)
    rule[3].next_to(rule[2], RIGHT, buff=0.15)
    row = VGroup(rg, ip, rule).arrange(RIGHT, buff=0.45)
    left_at(row, -6.6, -3.2)
    return rg, ip, rule


# ================================================================ cell-cycle bar (scenes 24, 25)
SEG_E = [("G1", 2.0), ("S", 4.6), ("G2", 1.0), ("M", 0.4)]
SEG_L = [("G1", 11.5), ("S", 4.9), ("G2", 1.1), ("M", 0.5)]
HX = 0.66           # units per hour
BAR_X0 = -6.2
BAR_H = 1.2
Y_E, Y_L = 2.3, -0.3


def cycle_bar(segs, y, h=BAR_H, gold_g1=False):
    g = VGroup()
    x = BAR_X0
    for k, (name, hrs) in enumerate(segs):
        w = hrs * HX
        col = GOLD if (gold_g1 and k == 0) else TEAL
        op = 0.5 if k % 2 == 0 else 0.25
        r = Rectangle(width=w, height=h, stroke_color=TEXT, stroke_width=1.5, fill_color=col,
                      fill_opacity=op).move_to([x + w / 2, y, 0])
        g.add(r)
        x += w
    return g


def seg_labels(bar, y, h=BAR_H):
    """G1, S and M above the bar, G2 below it, so the two short segments never touch."""
    out = VGroup()
    for r, name in zip(bar, ("G1", "S", "G2", "M")):
        yy = y - h / 2 - 0.4 if name == "G2" else y + h / 2 + 0.4
        out.add(T(name, 28, TEAL, weight=BOLD).move_to([r.get_center()[0], yy, 0]))
    return out


def hour_axis(y=-2.6):
    ln = Line([BAR_X0, y, 0], [BAR_X0 + 18 * HX, y, 0], color=GREY, stroke_width=3)
    g = VGroup(ln)
    for h in range(0, 19, 2):
        x = BAR_X0 + h * HX
        g.add(Line([x, y, 0], [x, y - 0.14, 0], color=GREY, stroke_width=3))
        g.add(T(str(h), 26, GREY).move_to([x, y - 0.42, 0]))
    g.add(left_at(T("time (hours)", 26, GREY), -6.5, -3.55))
    return g


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "The Ventricular Zone: Radial Glia as Stem Cells"
    TITLE = "Counting What Stays"


class S01Q(SpokenScene):
    def construct(self):
        cell = RGCell()
        tally = panel(2.8, 0.1, 6.0, 4.6, GREEN, "neurons in the cortex", 30)
        zero = big("0", 2.8, -0.2, GREEN, 120)
        self.play(FadeIn(cell), FadeIn(tally), FadeIn(zero), run_time=0.7)
        sx_, sy_ = cell.soma_c[0], cell.soma_c[1]
        keep = dot(sx_ + 1.15, sy_ + 0.45, 0.32, BLUE, 0.85)
        self.at("keeps some daughters")
        kl = T("kept", 28, BLUE).move_to([sx_ + 1.15, sy_ + 1.1, 0])
        self.play(FadeIn(keep, scale=0.3), FadeIn(kl), run_time=0.6)
        spent = dot(sx_ + 1.15, sy_ - 0.5, 0.32, GREEN, 0.9)
        sl = T("spent", 28, GREEN).move_to([sx_ + 1.15, sy_ - 1.1, 0])
        self.at("spends others")
        self.play(FadeIn(spent, scale=0.3), FadeIn(sl), run_time=0.4)
        self.play(FadeOut(sl), spent.animate.move_to([0.3, 0.1, 0]), run_time=0.8)
        self.play(FadeOut(spent, scale=0.4), run_time=0.2)
        q = big("?", 2.8, -0.2, RED, 120)
        self.at("does the cortex")
        self.play(FadeOut(zero), FadeOut(kl), run_time=0.12)
        self.play(FadeIn(q, scale=0.6), run_time=0.3)
        self.finish()


POOL_X = [-4.5, -1.5, 1.5, 4.5]
POOL_Y, D_Y = 2.55, -0.45


def s02_pool():
    return VGroup(*[dot(x, POOL_Y, 0.75, BLUE, 0.35) for x in POOL_X])


def s02_daughters():
    ds = []
    for x in POOL_X:
        for dx in (-0.62, 0.62):
            ds.append(dot(x + dx, D_Y, 0.55, TEXT, 0.2))
    return ds


def s02_tags():
    return [T("simple model", 26, LGREY), T("one round = one cell cycle for the pool", 26, LGREY), T("no cell death", 26, LGREY)]


def s02_tag_group():
    g = VGroup(*s02_tags()).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    return left_at(g, -6.6, -2.85)


class S02Setup(SpokenScene):
    def construct(self):
        tags = s02_tags()
        g = VGroup(*tags).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        left_at(g, -6.6, -2.85)
        hero = T("a simple model", 60, TEXT, font=TITLE_FONT).move_to([0, 0.4, 0])
        self.play(FadeIn(hero, shift=UP * 0.15), run_time=0.7)
        pool = s02_pool()
        plab = T("N dividing cells", 32, BLUE).move_to([0, 1.2, 0])
        self.at("pool of dividing cells")
        self.play(Transform(hero, tags[0]), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in pool], lag_ratio=0.25), FadeIn(plab), run_time=1.0)
        self.at("each dividing once per round")
        self.play(FadeIn(tags[1]), run_time=0.5)
        self.at("none dying")
        self.play(FadeIn(tags[2]), run_time=0.5)
        ds = s02_daughters()
        dl = T("2N daughters", 32, TEXT).move_to([0, -1.35, 0])
        self.at("every cell makes")
        self.play(LaggedStart(*[TransformFromCopy(pool[k], VGroup(ds[2 * k], ds[2 * k + 1])) for k in range(4)],
                              lag_ratio=0.3), run_time=1.6)
        self.play(FadeIn(dl), run_time=0.4)
        self.finish()


STAY = [0, 2, 3, 5, 6, 7]
QUIT = [1, 4]
LBOX, RBOX = (-3.4, 0.45), (3.4, 0.45)
ROW_Y = 2.55


def eq_pq(size=54):
    g = VGroup(M("P", size, BLUE), M("+", size, TEXT), M("Q", size, GREEN), M("= 1", size, TEXT)).arrange(RIGHT, buff=0.3)
    return g.move_to([0, 3.25, 0])


def box_at(cx, cy, color):
    return RoundedRectangle(corner_radius=0.2, width=4.4, height=2.8, stroke_color=color, stroke_width=3.5,
                            fill_color=color, fill_opacity=0.07).move_to([cx, cy, 0])


def p_label():
    return VGroup(M("P", 44, BLUE), T("stay as progenitors", 28, BLUE)).arrange(RIGHT, buff=0.25).move_to([LBOX[0], -1.35, 0])


def q_label():
    return VGroup(M("Q", 44, GREEN), T("quit as neurons", 28, GREEN)).arrange(RIGHT, buff=0.25).move_to([RBOX[0], -1.35, 0])


def stay_slots():
    return slots(6, *LBOX, dx=1.3, dy=0.7)


def quit_slots():
    return [[RBOX[0] - 0.75, RBOX[1], 0], [RBOX[0] + 0.75, RBOX[1], 0]]


class S03Pq(SpokenScene):
    def construct(self):
        pool, ds, tags = s02_pool(), s02_daughters(), s02_tags()
        g = s02_tag_group()
        plab = T("N dividing cells", 32, BLUE).move_to([0, 1.2, 0])
        dl = T("2N daughters", 32, TEXT).move_to([0, -1.35, 0])
        self.add(pool, plab, dl, g, *ds)
        lb, rb = box_at(*LBOX, BLUE), box_at(*RBOX, GREEN)
        pl, ql = p_label(), q_label()
        self.at("Call P")
        # the daughters take the parents' place on the top row; the sorting boxes then slide in below them
        self.play(FadeOut(pool), FadeOut(plab), FadeOut(g), run_time=0.4)
        self.play(*[d.animate.shift(UP * (ROW_Y - D_Y)) for d in ds], dl.animate.move_to([0, 3.45, 0]), run_time=0.7)
        self.play(FadeIn(lb, shift=UP * 0.3), FadeIn(pl[0]), run_time=0.5)
        sp, qp = stay_slots(), quit_slots()
        self.at("stay progenitors")
        self.play(*[ds[i].animate.move_to(p).scale(0.9).set_stroke(BLUE).set_fill(BLUE, opacity=0.85)
                    for i, p in zip(STAY, sp)], FadeIn(pl[1]), FadeOut(dl), run_time=1.0)
        self.at("Call Q")
        self.play(FadeIn(rb, shift=UP * 0.3), FadeIn(ql[0]), run_time=0.5)
        self.at("quit as neurons")
        self.play(*[ds[i].animate.move_to(p).scale(0.9).set_stroke(GREEN).set_fill(GREEN, opacity=0.9)
                    for i, p in zip(QUIT, qp)], FadeIn(ql[1]), run_time=1.0)
        self.at("together they make")
        eq = eq_pq()
        self.play(FadeIn(eq, shift=DOWN * 0.2), run_time=0.8)
        self.finish()


def s03_final():
    ds = s02_daughters()
    sp, qp = stay_slots(), quit_slots()
    for i, p in zip(STAY, sp):
        ds[i].move_to(p).scale(0.9).set_stroke(BLUE).set_fill(BLUE, opacity=0.85)
    for i, p in zip(QUIT, qp):
        ds[i].move_to(p).scale(0.9).set_stroke(GREEN).set_fill(GREEN, opacity=0.9)
    return ds


class S04Formula(SpokenScene):
    def construct(self):
        ds = s03_final()
        self.add(box_at(*LBOX, BLUE), box_at(*RBOX, GREEN), p_label(), q_label(), eq_pq(), *ds)
        f1 = VGroup(T("next pool", 28, BLUE), M("= 2N × P", 38, TEXT)).arrange(DOWN, buff=0.12).move_to([LBOX[0], -2.35, 0])
        f2 = VGroup(T("neurons made this round", 28, GREEN), M("= 2N × Q", 38, TEXT)).arrange(DOWN, buff=0.12).move_to([RBOX[0], -2.35, 0])
        n1 = T("all dividing cells:", 28, LGREY)
        n2 = T("radial glia + intermediate progenitors", 28, LGREY)
        note = VGroup(n1, n2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        left_at(note, -6.6, -3.4)
        self.at("next pool")
        self.play(FadeIn(f1, shift=UP * 0.15), Indicate(VGroup(*[ds[i] for i in STAY]), color=BLUE, scale_factor=1.12), run_time=0.9)
        self.at("neurons come from")
        self.play(FadeIn(f2, shift=UP * 0.15), Indicate(VGroup(*[ds[i] for i in QUIT]), color=GREEN, scale_factor=1.12), run_time=0.9)
        self.at("every dividing cell")
        self.play(FadeIn(n1), run_time=0.5)
        self.at("not just stem cells")
        self.play(FadeIn(n2), run_time=0.6)
        self.finish()


NUMY, SUBY, TAGY = PY - 0.05, PY - 1.6, PY - 0.95


def opts_group():
    return VGroup(T("shrink", 28, GREY), T("·", 28, GREY), T("hold", 28, GREY), T("·", 28, GREY),
                  T("grow", 28, GREY)).arrange(RIGHT, buff=0.3).move_to([PL, SUBY, 0])


class S05Predict1(SpokenScene):
    def construct(self):
        track = slider_static()
        k, ro = knob(0.5), readout(0.5)
        pp, np_ = pool_panel(), neu_panel()
        ds = pair_dots()
        for d in ds:
            d.set_stroke(TEXT).set_fill(TEXT, opacity=0.2)
        self.at("Suppose Q")
        self.play(FadeIn(track), FadeIn(k, scale=0.3), FadeIn(ro), FadeIn(pp), FadeIn(np_), run_time=0.9)
        self.at("Half the daughters quit")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in ds], lag_ratio=0.12), run_time=0.8)
        self.play(*recolor_for(ds, 0.5), Indicate(k, color=GREEN), run_time=0.8)
        qm1, qm2 = big("?", PL, NUMY, RED), big("?", PR, NUMY, RED)
        og = opts_group()
        self.at("Does the pool shrink")
        self.play(FadeIn(qm1, scale=0.6), run_time=0.6)
        self.at("shrink")
        self.play(FadeIn(og[0]), run_time=0.3)
        self.at("hold")
        self.play(FadeIn(og[1]), FadeIn(og[2]), run_time=0.3)
        self.at("or grow")
        self.play(FadeIn(og[3]), FadeIn(og[4]), run_time=0.3)
        self.at("And does it make neurons")
        self.play(FadeIn(qm2, scale=0.6), run_time=0.6)
        self.finish()


def s05_end_parts():
    return [slider_static(), knob(0.5), readout(0.5), pool_panel(), neu_panel(), *pair_dots(),
            opts_group(), big("?", PL, NUMY, RED), big("?", PR, NUMY, RED)]


class S06Pause(NarratedScene):
    def construct(self):
        parts = s05_end_parts()
        self.add(*parts)
        pp, np_ = parts[3], parts[4]
        t, bar_ = pause_cue()
        y = bar_.get_start()[1]
        self.play(FadeIn(t), FadeIn(bar_), run_time=0.3)
        shrink = UpdateFromAlphaFunc(bar_, lambda m, a: m.put_start_and_end_on([-6.3, y, 0], [6.3 - 12.5 * a, y, 0]),
                                     run_time=4.3, rate_func=linear)
        pulses = Succession(Indicate(VGroup(pp, np_), color=GOLD, scale_factor=1.03, run_time=0.9), Wait(0.8),
                            Indicate(VGroup(pp, np_), color=GOLD, scale_factor=1.03, run_time=0.9), Wait(0.7))
        self.play(shrink, pulses)
        self.finish()


def s07_end_parts():
    """The end of scene 7 (also the start of scene 8)."""
    ps = [slider_static(), knob(0.5), readout(0.5), pool_panel(), neu_panel("neurons so far")]
    ps += pair_dots()
    ps += [big("N", PL, NUMY, BLUE), T("holds", 36, BLUE).move_to([PL, SUBY, 0]),
           big("3N", PR, NUMY, GREEN), T("round 3", 28, LGREY).move_to([PR, SUBY, 0]),
           T("+N each round", 36, GREEN).move_to([PR, TAGY, 0]), pair_boxes()]
    return ps


class S07Rev1(SpokenScene):
    def construct(self):
        track = slider_static()
        k, ro = knob(0.5), readout(0.5)
        pp, np_ = pool_panel(), neu_panel()
        ds = pair_dots()
        og = opts_group()
        qm1, qm2 = big("?", PL, NUMY, RED), big("?", PR, NUMY, RED)
        self.add(track, k, ro, pp, np_, *ds, og, qm1, qm2)
        N = big("N", PL, NUMY, BLUE)
        holds = T("holds", 36, BLUE).move_to([PL, SUBY, 0])
        self.at("It holds")
        self.play(ReplacementTransform(qm1, N), FadeOut(og), run_time=0.4)
        self.play(FadeIn(holds), run_time=0.3)
        n1 = big("N", PR, NUMY, GREEN)
        rnd = T("round 1", 28, LGREY).move_to([PR, SUBY, 0])
        self.at("and it makes neurons")
        self.play(ReplacementTransform(qm2, n1), FadeIn(rnd), run_time=0.7)
        boxes = pair_boxes()
        self.at("as if every division")
        self.play(FadeIn(boxes), run_time=0.6)
        self.at("keeps one daughter")
        self.play(*[Indicate(ds[i], color=BLUE, scale_factor=1.3) for i in (0, 2, 4, 6)], run_time=0.8)
        self.at("spends one")
        self.play(*[Indicate(ds[i], color=GREEN, scale_factor=1.3) for i in (1, 3, 5, 7)], run_time=0.8)
        self.at("A steady pool")
        n2, r2 = big("2N", PR, NUMY, GREEN), T("round 2", 28, LGREY).move_to([PR, SUBY, 0])
        newh = T("neurons so far", 28, GREEN).move_to(np_[1])
        tag = T("+N each round", 36, GREEN).move_to([PR, TAGY, 0])
        self.play(ReplacementTransform(n1, n2), ReplacementTransform(rnd, r2), Transform(np_[1], newh), FadeIn(tag),
                  Indicate(N, color=BLUE, scale_factor=1.12), run_time=0.7)
        self.at("not an idle")
        n3, r3 = big("3N", PR, NUMY, GREEN), T("round 3", 28, LGREY).move_to([PR, SUBY, 0])
        self.play(ReplacementTransform(n2, n3), ReplacementTransform(r2, r3), Indicate(N, color=BLUE, scale_factor=1.12), run_time=0.7)
        self.finish()


class S08Rule(SpokenScene):
    def construct(self):
        ps = s07_end_parts()
        track, k, ro, pp, np_ = ps[:5]
        ds = ps[5:13]
        N, holds, n3, r3, tag, boxes = ps[13:]
        self.add(*ps)
        self.at("Below")
        ro2 = readout(0.25)
        newh = T("neurons made this round", 28, GREEN).move_to(np_[1])
        v1 = big("0.5N", PR, NUMY, GREEN, 80)
        self.play(FadeOut(boxes), k.animate.move_to([sx(0.25), SL_Y, 0]), ReplacementTransform(ro, ro2),
                  *recolor_for(ds, 0.25), Transform(np_[1], newh), FadeOut(n3), FadeOut(r3), FadeOut(tag), FadeOut(N), FadeOut(holds),
                  FadeIn(v1, scale=0.8), run_time=0.8)
        gl = big("1.5N", PL, NUMY, BLUE, 80)
        glab = T("> N: grows", 36, BLUE).move_to([PL, SUBY, 0])
        self.at("the pool grows")
        self.play(FadeIn(gl), FadeIn(glab), run_time=0.4)
        self.at("Above it")
        ro3 = readout(0.75)
        v2 = big("1.5N", PR, NUMY, GREEN, 80)
        self.play(k.animate.move_to([sx(0.75), SL_Y, 0]), ReplacementTransform(ro2, ro3), *recolor_for(ds, 0.75),
                  FadeOut(gl), FadeOut(glab), ReplacementTransform(v1, v2), run_time=0.6)
        sl = big("0.5N", PL, NUMY, BLUE, 80)
        slab = T("< N: shrinks", 36, BLUE).move_to([PL, SUBY, 0])
        self.at("the pool shrinks")
        self.play(FadeIn(sl), FadeIn(slab), run_time=0.4)
        self.finish()


BOX_Y, BOX_H = -0.15, 4.0


def s09_tags():
    t = T("mouse dorsal cortex", 36, LGREY).move_to([0, 3.3, 0])
    c = T("Takahashi, Nowakowski and Caviness", 30, GOLD).move_to([0, -3.35, 0])
    return t, c


def s09_state():
    t, c = s09_tags()
    boxes = cycle_boxes(BOX_Y, BOX_H, 44)
    br = Brace(boxes, UP, color=TEAL, buff=0.15)
    lab = T("about 11 cycles of neurogenesis", 36, TEAL).next_to(br, UP, buff=0.12)
    cw = cycle_word(BOX_Y - BOX_H / 2 - 0.4, 30)
    return t, c, boxes, br, lab, cw


class S09Takahashi(SpokenScene):
    def construct(self):
        t, c, boxes, br, lab, cw = s09_state()
        self.play(FadeIn(t, shift=DOWN * 0.15), LaggedStart(*[FadeIn(b, scale=0.7) for b in boxes], lag_ratio=0.1),
                  FadeIn(cw), run_time=1.2)
        self.at("Takahashi")
        self.play(FadeIn(c, shift=UP * 0.15), run_time=0.6)
        self.at("about eleven cycles")
        self.play(FadeIn(br), FadeIn(lab), run_time=0.7)
        self.finish()


def q_tags_small():
    t = T("mouse dorsal cortex", 26, LGREY)
    c = T("Takahashi, Nowakowski and Caviness", 26, GOLD)
    return left_at(t, -5.2, 3.65), c.move_to([6.5 - c.width / 2, 3.65, 0])


def s10_legend():
    sample = DashedVMobject(Line([0, 0, 0], [0.8, 0, 0], color=GREEN, stroke_width=5), num_dashes=5)
    sample.set_stroke(opacity=0.6)
    txt = T("smooth schedule used next (illustrative)", 26, LGREY)
    txt.next_to(sample, RIGHT, buff=0.2)
    return left_at(VGroup(sample, txt), -5.6, 2.45)


def q_marker(c, ring=False):
    g = VGroup(Dot(qpt(c), radius=0.14, color=GREEN))
    g[0].set_z_index(6)
    if ring:
        g.add(Circle(radius=0.3, stroke_color=GOLD, stroke_width=5).move_to(qpt(c)))
    return g


def q_label_at(c, text, dx=0.0, dy=0.6, color=GREEN):
    p = qpt(c)
    return T(text, 26, color).move_to([p[0] + dx, p[1] + dy, 0])


class S10Sched(SpokenScene):
    def construct(self):
        t, c, big_boxes, br, lab, cw = s09_state()
        self.add(t, c, big_boxes, br, lab, cw)
        small = cycle_boxes(-3.1, 0.75, 26)
        axes = q_axes()
        t2, c2 = q_tags_small()
        lg = s10_legend()
        self.play(FadeOut(br), FadeOut(lab), Transform(big_boxes, small), Transform(t, t2), Transform(c, c2),
                  Transform(cw, cycle_word()), FadeIn(axes), FadeIn(lg), run_time=0.7)
        m1, l1 = q_marker(1), q_label_at(1, "near 0", 0.55, 0.5)
        self.at("near zero")
        self.play(FadeIn(m1, scale=0.3), FadeIn(l1), run_time=0.5)
        a = q_curve(1, 8)
        self.at("It passes")
        self.play(Create(a), run_time=1.2, rate_func=linear)
        m8, l8 = q_marker(8, ring=True), q_label_at(8, "past 0.5", -0.7, 0.75, GOLD)
        self.at("eighth")
        self.play(FadeIn(m8, scale=0.3), FadeIn(l8), Indicate(big_boxes[7], color=TEAL, scale_factor=1.2), run_time=0.6)
        b = q_curve(8, 10)
        self.at("reaches about")
        self.play(Create(b), run_time=1.1, rate_func=linear)
        m10, l10 = q_marker(10), q_label_at(10, "about 0.8", -0.7, 0.6)
        self.at("by the tenth")
        self.play(FadeIn(m10, scale=0.3), FadeIn(l10), Indicate(big_boxes[9], color=TEAL, scale_factor=1.2), run_time=0.5)
        d_ = q_curve(10, 11)
        self.play(Create(d_), run_time=0.4, rate_func=linear)
        self.finish()


def q_static():
    """The finished Q plot of scene 10 as static pieces."""
    t2, c2 = q_tags_small()
    g = VGroup(q_axes(), cycle_boxes(-3.1, 0.75, 26), cycle_word(), t2, c2, s10_legend(), q_curve(1, 11),
               q_marker(1), q_label_at(1, "near 0", 0.55, 0.5), q_marker(8, ring=True),
               q_label_at(8, "past 0.5", -0.7, 0.75, GOLD), q_marker(10), q_label_at(10, "about 0.8", -0.7, 0.6))
    return g


class S11Mixed(SpokenScene):
    def construct(self):
        qs = q_static()
        self.add(qs)
        chip1 = chip("ventricular zone estimate", GOLD, size=30)
        left_at(chip1, -5.6, 1.5)
        n1 = left_at(T("not a direct count of stem cells kept", 26, LGREY), -5.6, 0.82)
        n2 = VGroup(T("old compartments,", 28, GOLD), T("not today's cell classes", 28, GOLD)).arrange(DOWN, buff=0.1).move_to([3.4, -1.3, 0])
        self.at("Takahashi measured")
        self.play(*[Indicate(qs[i][0], color=GOLD, scale_factor=2.2) for i in (7, 9, 11)], run_time=0.9)
        self.at("ventricular zone proper")
        self.play(FadeIn(chip1, shift=RIGHT * 0.2), run_time=0.7)
        self.at("apart from cells")
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.6)
        self.at("Those old compartments")
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S12Run(SpokenScene):
    def construct(self):
        boxes = cycle_boxes(-3.1, 0.75, 26)
        tg = illus_tag()
        self.add(boxes, tg)
        axes = count_axes()
        lg = legend()
        self.at("Follow one founder")
        self.play(FadeIn(axes), FadeIn(lg), run_time=0.6)
        p1 = Dot(series_pts(POOL, 1, 1)[0], radius=0.1, color=BLUE)
        n1 = Dot(series_pts(NEU, 1, 1)[0], radius=0.1, color=GREEN)
        one = T("1", 26, BLUE).next_to(p1, UP, buff=0.12)
        self.play(FadeIn(p1, scale=0.4), FadeIn(n1, scale=0.4), FadeIn(one), run_time=0.3)
        self.at("through that schedule")
        self.play(LaggedStart(*extend_anims(POOL, BLUE, 1, 3), lag_ratio=0.8),
                  LaggedStart(*extend_anims(NEU, GREEN, 1, 3), lag_ratio=0.8), FadeOut(one), run_time=1.1)
        self.at("numbers are")
        self.play(Indicate(tg, color=GOLD, scale_factor=1.15), run_time=0.8)
        self.finish()


def count_static(c1):
    return VGroup(cycle_boxes(-3.1, 0.75, 26), count_axes(), legend(), static_series(POOL, BLUE, c1), static_series(NEU, GREEN, c1),
                  illus_tag())


class S13Early(SpokenScene):
    def construct(self):
        self.add(count_static(3))
        self.at("Early on")
        self.play(LaggedStart(*extend_anims(POOL, BLUE, 3, 5), lag_ratio=0.8),
                  LaggedStart(*extend_anims(NEU, GREEN, 3, 5), lag_ratio=0.8), run_time=1.3)
        self.at("pool multiplies")
        self.play(LaggedStart(*extend_anims(POOL, BLUE, 5, 7), lag_ratio=0.8),
                  LaggedStart(*extend_anims(NEU, GREEN, 5, 7), lag_ratio=0.8), run_time=1.3)
        self.finish()


class S14Late(SpokenScene):
    def construct(self):
        self.add(count_static(7))
        self.at("Late")
        self.play(LaggedStart(*extend_anims(POOL, BLUE, 7, 11), lag_ratio=0.9),
                  LaggedStart(*extend_anims(NEU, GREEN, 7, 11), lag_ratio=0.9), run_time=1.6)
        pk_line = DashedVMobject(Line([CX(9), yn(0), 0], [CX(9), yn(40) - 0.1, 0], color=GREEN, stroke_width=3), num_dashes=24)
        pk_ring = Circle(radius=0.22, stroke_color=GREEN, stroke_width=4).move_to([CX(9), yn(NEU[8]), 0])
        pk_lab = tb("peak: cycle 9", 26, GREEN)
        pk_lab.move_to([CX(9) + 1.7, yn(NEU[8]) + 0.15, 0])
        self.at("Output peaks")
        self.play(Create(pk_line), Create(pk_ring), FadeIn(pk_lab), run_time=0.8)
        q_line = DashedVMobject(Line([CX(7.5), yn(0), 0], [CX(7.5), yn(40) - 1.8, 0], color=GOLD, stroke_width=3), num_dashes=20)
        q_lab = tb("Q passes 0.5", 26, GOLD)
        q_lab.move_to([CX(7.5) - 1.3, yn(0) + 0.45, 0])
        self.at("just after Q passes")
        self.play(Create(q_line), FadeIn(q_lab), run_time=0.7)
        pp = Circle(radius=0.22, stroke_color=BLUE, stroke_width=4).move_to([CX(8), yn(POOL[7]), 0])
        self.at("while the pool is still near")
        self.play(Create(pp), run_time=0.5)
        tot = tb("about 150 neurons in all", 28, GREEN)
        tot.move_to([-5.6 + tot.width / 2, 1.1, 0])
        self.at("its largest")
        self.play(FadeIn(tot, shift=UP * 0.1), Indicate(pp, color=BLUE, scale_factor=1.4), run_time=0.8)
        self.finish()


LQ0 = -5.5      # lever plot: x of cycle 1
LQD = 0.55      # lever plot: x step per cycle
BASE = -2.0


def lx(c):
    return LQ0 + LQD * (c - 1)


def ly(q):
    return BASE + 4.9 * q


def lever_curve(shift):
    cs = np.linspace(1, 11, 41)
    return poly([[lx(c), ly(qfun(c, shift)), 0] for c in cs], GREEN, 5)


def lever_dots(shift):
    return VGroup(*[Dot([lx(c), ly(qfun(c, shift)), 0], radius=0.09, color=GREEN) for c in range(1, 12)])


BX0, BX1, BW, BH0 = 2.9, 5.5, 1.5, 2.2


def bar(x, h, color=GREEN, w=BW):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=0.5).move_to([x, BASE + h / 2, 0])


def two_lines(a, b, size, color, x, y):
    return VGroup(T(a, size, color), T(b, size, color)).arrange(DOWN, buff=0.06).move_to([x, y, 0])


class S15Lever(SpokenScene):
    def construct(self):
        ax = Line([-6.0, ly(0), 0], [-6.0, ly(1) + 0.05, 0], color=GREY, stroke_width=3)
        base = Line([-6.0, ly(0), 0], [0.4, ly(0), 0], color=GREY, stroke_width=3)
        halfl = DashedVMobject(Line([-6.0, ly(0.5), 0], [0.4, ly(0.5), 0], color=GREY, stroke_width=2.5), num_dashes=24)
        ticks = VGroup(*[Line([lx(c), ly(0), 0], [lx(c), ly(0) - 0.12, 0], color=GREY, stroke_width=3) for c in range(1, 12)])
        labs = VGroup(T("0", 26, GREY).move_to([-6.4, ly(0), 0]), T("0.5", 26, GREY).move_to([-6.45, ly(0.5), 0]),
                      T("1", 26, GREY).move_to([-6.4, ly(1), 0]),
                      T("1", 26, GREY).move_to([lx(1), ly(0) - 0.45, 0]), T("6", 26, GREY).move_to([lx(6), ly(0) - 0.45, 0]),
                      T("11", 26, GREY).move_to([lx(11), ly(0) - 0.45, 0]),
                      T("cycle", 26, GREY).move_to([lx(6), ly(0) - 0.9, 0]))
        qn = T("Q", 34, GREEN, weight=BOLD).move_to([-6.0, ly(1) + 0.5, 0])
        curve, dts = lever_curve(0), lever_dots(0)
        cross = DashedVMobject(Line([lx(7.5), ly(0), 0], [lx(7.5), ly(1) + 0.1, 0], color=GOLD, stroke_width=4), num_dashes=18)
        cl = T("Q = 0.5", 26, GOLD).move_to([lx(7.5), ly(1) + 0.5, 0])
        crossg = VGroup(cross, cl)
        self.play(FadeIn(VGroup(ax, base, halfl, ticks, labs, qn)), run_time=0.5)
        self.play(Create(curve), FadeIn(dts), run_time=0.8)
        self.play(FadeIn(crossg), run_time=0.4)
        hd = T("total neurons", 32, GREEN).move_to([4.2, 3.3, 0])
        b0 = bar(BX0, BH0)
        v0 = T("about 150", 28, GREEN).move_to([BX0, BASE + BH0 + 0.4, 0])
        l0 = two_lines("crossing at", "cycle 7.5", 26, GREY, BX0, BASE - 0.75)
        self.at("In this model")
        self.play(FadeIn(hd), GrowFromEdge(b0, DOWN), FadeIn(v0), FadeIn(l0), run_time=0.9)
        l1 = two_lines("crossing one", "cycle later", 26, GREY, BX1, BASE - 0.75)
        b1 = bar(BX1, BH0)
        self.at("moving the crossing")
        self.play(FadeIn(l1), GrowFromEdge(b1, DOWN), run_time=0.6)
        self.at("one cycle later")
        curve2, dts2 = lever_curve(1), lever_dots(1)
        h1 = BH0 * RATIO
        b1t = bar(BX1, h1)
        ghost = crossg.copy()
        ghost.set_stroke(opacity=0.35)
        ghost[1].set_opacity(0)
        self.add(ghost)
        self.play(Transform(curve, curve2), Transform(dts, dts2), crossg.animate.shift(RIGHT * LQD), Transform(b1, b1t),
                  run_time=1.2)
        v1 = T("about 1.8×", 28, GREEN).move_to([BX1, BASE + h1 + 0.4, 0])
        self.at("nearly doubles")
        self.play(FadeIn(v1, shift=UP * 0.1), run_time=0.6)
        tg = T("same eleven cycles · about a dozen cells still dividing", 26, LGREY).move_to([0.2, -3.5, 0])
        self.at("over the same")
        self.play(FadeIn(tg), run_time=0.6)
        self.finish()


def blob(a, b, wob, k, color, cx, cy, op=0.18, sw=4):
    f = ParametricFunction(lambda t: np.array([a * (1 + wob * math.sin(k * t)) * math.cos(t),
                                               b * (1 + wob * math.sin(k * t)) * math.sin(t), 0]),
                           t_range=[0, 2 * PI], stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)
    return f.move_to([cx, cy, 0])


def tiny_boxes(n, cx, y, extra=0, h=0.5):
    g = VGroup()
    tot = n + extra
    for i in range(tot):
        x = cx + (i - (tot - 1) / 2) * 0.44
        ex = i >= n
        r = Rectangle(width=0.36, height=h, stroke_color=GOLD if ex else TEAL, stroke_width=3,
                      fill_color=GOLD if ex else TEAL, fill_opacity=0.35 if ex else 0.4).move_to([x, y, 0])
        g.add(r)
    return g


class S16Expand(SpokenScene):
    def construct(self):
        mouse = blob(2.9, 2.2, 0.0, 1, GREEN, -3.5, 1.1)
        ml = T("mouse cortex", 30, LGREY).move_to([-3.5, 1.1, 0])
        mb = tiny_boxes(11, -3.5, -2.45, 0, 0.75)
        big_c = blob(3.2, 2.6, 0.03, 13, GREEN, 3.45, 1.1)
        bl = T("larger cortex", 30, LGREY).move_to([3.45, 1.1, 0])
        bb = tiny_boxes(11, 3.45, -2.45, 3, 0.75)
        self.play(FadeIn(mouse, scale=0.7), FadeIn(ml), FadeIn(mb), FadeIn(big_c, scale=0.7), FadeIn(bl),
                  FadeIn(bb[:11]), run_time=0.9)
        el = T("extra cycles", 28, GOLD).move_to([bb[12].get_center()[0] - 0.2, -3.15, 0])
        self.at("a few extra")
        self.play(FadeIn(bb[11:], shift=UP * 0.1), FadeIn(el), run_time=0.8)
        tg = T("a candidate: see human brain expansion", 30, GOLD).move_to([0, -3.62, 0])
        self.at("candidate")
        self.play(FadeIn(tg), run_time=0.5)
        self.at("bigger cortices")
        self.play(Indicate(big_c, color=GREEN, scale_factor=1.04), run_time=0.9)
        self.finish()


TRAP_P = (0.0, 2.2)
D1, D2 = (-2.9, -1.25), (2.9, -1.25)
SHIFT = -2.3


def s17_final():
    parent = rg_icon(*TRAP_P, 1.25)
    pl = left_at(T("radial glial cell", 32, BLUE), 1.1, TRAP_P[1])
    p1 = rg_icon(*D1, 1.2)
    ip = ipdot(*D2, 1.0)
    l1 = T("radial glial cell", 28, BLUE).move_to([D1[0], -3.2, 0])
    l2 = T("intermediate progenitor", 28, BLUE).move_to([D2[0], -3.2, 0])
    a1 = arr([TRAP_P[0] - 0.5, 0.8, 0], [D1[0] + 0.2, 0.2, 0], GREY, 4)
    a2 = arr([TRAP_P[0] + 0.5, 0.8, 0], [D2[0] - 0.2, -0.12, 0], GREY, 4)
    return parent, pl, a1, a2, p1, ip, l1, l2


class S17Trap(SpokenScene):
    def construct(self):
        trap = T("a trap", 40, RED, weight=BOLD).move_to([-5.0, 3.3, 0])
        parent, pl, a1, a2, p1, ip, l1, l2 = s17_final()
        self.at("a trap")
        self.play(FadeIn(trap, scale=0.7), run_time=0.5)
        self.at("Suppose every radial glial division")
        self.play(FadeIn(parent, scale=0.5), FadeIn(pl), run_time=0.7)
        self.at("makes a radial glial cell")
        self.play(GrowArrow(a1), FadeIn(p1, scale=0.5), FadeIn(l1), run_time=1.0)
        self.at("and an intermediate progenitor")
        self.play(GrowArrow(a2), FadeIn(ip, scale=0.5), FadeIn(l2), run_time=1.0)
        self.finish()


class S18Trap2(SpokenScene):
    def construct(self):
        trap = T("a trap", 40, RED, weight=BOLD).move_to([-5.0, 3.3, 0])
        parts = VGroup(*s17_final())
        self.add(trap, parts)
        self.play(parts.animate.shift(RIGHT * SHIFT), run_time=0.8)
        pn = panel(4.65, -0.2, 4.2, 4.4, TEXT, "pool, counted as one", 28)
        qz = VGroup(M("Q = 0", 44, GREEN), T("no daughter quits", 28, LGREY)).arrange(DOWN, buff=0.12).move_to([4.65, -1.5, 0])
        self.at("no daughter quits")
        self.play(FadeIn(pn), FadeIn(qz, shift=UP * 0.15), run_time=0.7)
        lump = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=8.2, height=2.9, stroke_color=TEXT, stroke_width=3.5)
                              .move_to([(D1[0] + D2[0]) / 2 + SHIFT, -1.15, 0]), num_dashes=50)
        one = big("1", 3.45, 0.35, TEXT, 110)
        self.at("Count it as one pool")
        self.play(Create(lump), FadeIn(one), run_time=0.9)
        ar = arr([3.95, 0.35, 0], [4.85, 0.35, 0], GOLD, 6, 0.25)
        two = big("2", 5.6, 0.35, GOLD, 110)
        self.at("seems to double")
        self.play(GrowArrow(ar), FadeIn(two, scale=0.5), run_time=0.8)
        self.finish()


def pause_scene_cue(scene, pulse_targets):
    t, bar_ = pause_cue()
    y = bar_.get_start()[1]
    scene.play(FadeIn(t), FadeIn(bar_), run_time=0.3)
    shrink = UpdateFromAlphaFunc(bar_, lambda m, a: m.put_start_and_end_on([-6.3, y, 0], [6.3 - 12.5 * a, y, 0]),
                                 run_time=4.3, rate_func=linear)
    pulses = Succession(Indicate(pulse_targets, color=GOLD, scale_factor=1.03, run_time=0.9), Wait(0.8),
                        Indicate(pulse_targets, color=GOLD, scale_factor=1.03, run_time=0.9), Wait(0.7))
    scene.play(shrink, pulses)


class S19Predict2(SpokenScene):
    def construct(self):
        cols = col_boxes()
        rgrp, ngrp = rg_counter_panel(), neu_counter_panel()
        rg_item, ip_item, rule_item = legend_row()
        self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.2), FadeIn(rgrp), FadeIn(ngrp),
                  FadeIn(rg_item, shift=UP * 0.1), FadeIn(col_rg(0), scale=0.4), run_time=0.9)
        self.at("for four cycles")
        self.play(LaggedStart(*[Indicate(c[1], color=GOLD, scale_factor=1.25) for c in cols], lag_ratio=0.3), run_time=1.2)
        self.at("Each intermediate progenitor")
        self.play(FadeIn(ip_item, shift=UP * 0.1), run_time=0.6)
        self.at("divides into two neurons")
        self.play(FadeIn(rule_item, shift=UP * 0.1), run_time=0.8)
        q1 = big("?", CNT_X, RGN_Y, RED, 72)
        q2 = big("?", CNT_X, NEUN_Y, RED, 72)
        self.at("How many radial glia")
        self.play(FadeIn(q1, scale=0.6), run_time=0.6)
        self.at("and how many neurons")
        self.play(FadeIn(q2, scale=0.6), run_time=0.6)
        self.finish()


class S20Pause(NarratedScene):
    def construct(self):
        rg_item, ip_item, rule_item = legend_row()
        q1 = big("?", CNT_X, RGN_Y, RED, 72)
        q2 = big("?", CNT_X, NEUN_Y, RED, 72)
        rgp, ngp = rg_counter_panel(), neu_counter_panel()
        self.add(col_boxes(), col_rg(0), rgp, ngp, rg_item, ip_item, rule_item, q1, q2)
        pause_scene_cue(self, VGroup(rgp, ngp))
        self.finish()


def s21_final():
    parts = [col_boxes(hl=0), rg_counter_panel(), neu_counter_panel()]
    for i in range(4):
        parts += [col_rg(i), col_ip(i), col_tags(i), *col_neurons(i)]
        if i:
            parts.append(col_arrow(i))
    ar, gh, gl = ghost_slots()
    parts += [ar, gh, gl, pool_tag()]
    parts += list(legend_row())
    parts += [big("1", CNT_X, RGN_Y, BLUE, 72), big("6", CNT_X, NEUN_Y, GREEN, 72), s21_note()]
    return parts


def s21_note():
    return VGroup(T("no gain in", 24, GOLD), T("stem cells", 24, GOLD)).arrange(DOWN, buff=0.05).move_to([CNT_X, 0.55, 0])


class S21Rev2(SpokenScene):
    def construct(self):
        cols = col_boxes()
        rgp, ngp = rg_counter_panel(), neu_counter_panel()
        rg_item, ip_item, rule_item = legend_row()
        q1 = big("?", CNT_X, RGN_Y, RED, 72)
        q2 = big("?", CNT_X, NEUN_Y, RED, 72)
        self.add(cols, rgp, ngp, rg_item, ip_item, rule_item, q1, q2)
        rgs = [col_rg(i) for i in range(4)]
        self.add(rgs[0])
        ips = [col_ip(i) for i in range(4)]
        tg = [col_tags(i) for i in range(4)]
        one = big("1", CNT_X, RGN_Y, BLUE, 72)
        self.at("Still one radial glial cell")
        self.play(LaggedStart(*[FadeIn(r, scale=0.4) for r in rgs[1:]], lag_ratio=0.25), ReplacementTransform(q1, one), run_time=1.0)
        self.at("and six neurons")
        cur = big("0", CNT_X, NEUN_Y, GREEN, 72)
        self.play(FadeIn(ips[0], scale=0.4), ReplacementTransform(q2, cur), FadeIn(tg[0]), run_time=0.4)
        for i, val in ((1, "2"), (2, "4"), (3, "6")):
            nt = big(val, CNT_X, NEUN_Y, GREEN, 72)
            anims = [FadeIn(col_arrow(i)), *[FadeIn(d, scale=0.4) for d in col_neurons(i)], FadeIn(tg[i]),
                     ReplacementTransform(cur, nt)]
            if i < 3:
                anims.append(FadeIn(ips[i], scale=0.4))
            self.play(*anims, run_time=0.5)
            cur = nt
        self.at("One more intermediate progenitor")
        self.play(FadeIn(ips[3], scale=0.4), run_time=0.5)
        self.play(Indicate(ips[3], color=BLUE, scale_factor=1.3), run_time=0.5)
        ar, gh, gl = ghost_slots()
        self.at("is about to make two more")
        self.play(GrowArrow(ar), FadeIn(gh), FadeIn(gl), run_time=0.8)
        d1 = pool_tag()
        self.at("That first doubling")
        self.play(Transform(cols, col_boxes(hl=0)), FadeIn(d1), Indicate(VGroup(rgs[0], ips[0]), color=GOLD, scale_factor=1.25),
                  run_time=0.8)
        nog = s21_note()
        self.at("not a gain")
        self.play(FadeIn(nog, shift=UP * 0.1), run_time=0.7)
        self.finish()


def s22_final():
    L = panel(-3.4, 0.3, 5.8, 5.2, BLUE, "radial glia", 32)
    R = panel(3.4, 0.3, 5.8, 5.2, BLUE, "intermediate progenitors", 28, dashed=True)
    one = big("1", -3.4, 0.85, BLUE, 110)
    loop = Arc(radius=1.0, start_angle=PI * 0.15, angle=PI * 1.7, arc_center=[-3.4, 0.85, 0], stroke_color=BLUE, stroke_width=5)
    loop.add_tip(tip_length=0.25)
    ipn = big("1", 1.45, 0.85, BLUE, 110)
    wait_ = T("waiting", 30, BLUE).move_to([1.45, -0.3, 0])
    ipd = ipdot(3.2, 0.85, 0.6)
    lab = T("keeps the source going", 30, TEXT).move_to([-3.4, -1.6, 0])
    return [L, R, one, loop, ipn, wait_, ipd, lab]


class S22Twopools(SpokenScene):
    def construct(self):
        self.add(*s21_final())
        self.play(Wait(0.1))
        L, R, one, loop, ipn, wait_, ipd, lab = s22_final()
        self.at("count two pools")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        self.play(FadeIn(L), FadeIn(R), FadeIn(one, scale=0.6), FadeIn(ipd, scale=0.6), FadeIn(ipn, scale=0.6), FadeIn(wait_),
                  run_time=0.9)
        self.at("radial glia are the source")
        self.play(Create(loop), run_time=0.9)
        self.at("keeps neurogenesis going")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S23Twopools2(SpokenScene):
    def construct(self):
        self.add(*s22_final())
        ar = arr([3.95, 0.85, 0], [4.6, 0.85, 0], GREY, 5, 0.24)
        n1, n2 = dot(5.05, 0.85, 0.3, GREEN, 0.9), dot(5.65, 0.85, 0.3, GREEN, 0.9)
        nl = T("two neurons", 26, GREEN).move_to([4.95, 0.15, 0])
        self.at("Intermediate progenitors multiply")
        self.play(GrowArrow(ar), FadeIn(n1, scale=0.4), FadeIn(n2, scale=0.4), FadeIn(nl), run_time=1.0)
        dl = T("one cycle later", 26, GREY).move_to([4.85, 1.65, 0])
        self.at("and delay")
        self.play(FadeIn(dl), run_time=0.5)
        lab = T("multiplies and delays output", 28, GOLD).move_to([3.4, -1.5, 0])
        self.at("what each spent daughter yields")
        self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.7)
        self.finish()


def t_tags():
    mc = T("mouse dorsal cortex", 26, LGREY)
    mc.move_to([6.5 - mc.width / 2, 3.65, 0])
    sch = T("segment lengths are schematic", 24, LGREY)
    sch.move_to([6.6 - sch.width / 2, -3.55, 0])
    return mc, sch


def t18_label():
    """'about 18 hours' at the right end of the lower bar: a thin tick down from the bar end to the label."""
    xe = BAR_X0 + 18 * HX
    lab = T("about 18 hours", 36, TEXT)
    lab.move_to([xe - lab.width / 2 + 0.9, -1.95, 0])
    tick = Line([xe, Y_L - BAR_H / 2, 0], [xe, -1.62, 0], color=TEXT, stroke_width=3)
    return VGroup(tick, lab)


def g1_brace():
    ln = Line([BAR_X0 + 2.0 * HX, Y_L - BAR_H / 2 - 0.05, 0], [BAR_X0 + 11.5 * HX, Y_L - BAR_H / 2 - 0.05, 0])
    br = Brace(ln, DOWN, color=GOLD, buff=0.0)
    return br


class S24Clock(SpokenScene):
    def construct(self):
        axis = hour_axis()
        early = cycle_bar(SEG_E, Y_E)
        el = seg_labels(early, Y_E)
        cur = cycle_bar(SEG_E, Y_L)
        cl = seg_labels(cur, Y_L)
        t8 = left_at(T("about 8 hours", 36, TEXT), early.get_right()[0] + 0.3, Y_E)
        mc, sch = t_tags()
        self.at("The cycle itself slows")
        self.play(FadeIn(early), FadeIn(el), FadeIn(cur), FadeIn(cl), FadeIn(axis), run_time=0.9)
        self.at("In mouse dorsal cortex")
        self.play(FadeIn(mc), FadeIn(sch), run_time=0.5)
        self.at("lengthens from about")
        self.play(FadeIn(t8), run_time=0.5)
        late = cycle_bar(SEG_L, Y_L)
        ll = seg_labels(late, Y_L)
        self.at("to about eighteen")
        t18 = t18_label()
        self.play(Transform(cur, late), Transform(cl, ll), FadeIn(t18), run_time=1.5)
        br = g1_brace()
        add = T("added time: nearly all in G1", 30, GOLD).next_to(br, DOWN, buff=0.12)
        self.at("Nearly all the added time")
        self.play(FadeIn(br), FadeIn(add, shift=UP * 0.1), run_time=0.6)
        self.at("in G1")
        self.play(cur[0].animate.set_fill(GOLD, opacity=0.6), Indicate(cl[0], color=GOLD), run_time=0.7)
        self.finish()


def s24_final():
    axis = hour_axis()
    early = cycle_bar(SEG_E, Y_E)
    el = seg_labels(early, Y_E)
    t8 = left_at(T("about 8 hours", 36, TEXT), early.get_right()[0] + 0.3, Y_E)
    mc, sch = t_tags()
    late = cycle_bar(SEG_L, Y_L, gold_g1=True)
    ll = seg_labels(late, Y_L)
    t18 = t18_label()
    br = g1_brace()
    add = T("added time: nearly all in G1", 30, GOLD).next_to(br, DOWN, buff=0.12)
    return [axis, early, el, t8, mc, sch, late, ll, t18, br, add], late, add, br


class S25Hyp(SpokenScene):
    def construct(self):
        parts, late, add, br = s24_final()
        self.add(*parts)
        hyp = chip("hypothesis: more time for fate determinants", GOLD, size=28)
        hyp.move_to([(BAR_X0 + 2.0 * HX + BAR_X0 + 11.5 * HX) / 2, add.get_center()[1] - 0.22, 0])
        self.at("One hypothesis")
        self.play(FadeOut(add), FadeIn(hyp, shift=UP * 0.15), run_time=0.7)
        self.at("a longer G1")
        self.play(Indicate(late[0], color=GOLD, scale_factor=1.05), run_time=0.9)
        self.at("fate determinants")
        self.play(Indicate(hyp, color=GOLD, scale_factor=1.06), run_time=0.7)
        self.finish()


DCX = -3.4          # culture dish centre x
RIM = 2.2


def dish():
    bowl = Arc(radius=3.1, start_angle=PI, angle=PI, stroke_color=GREY, stroke_width=6).stretch(1.15, 1)
    bowl.move_to([DCX, RIM - bowl.height / 2, 0])
    bowl.set_fill(FLUID, opacity=0.3)
    rimline = Line([DCX - 3.1, RIM, 0], [DCX + 3.1, RIM, 0], stroke_color=GREY, stroke_width=6)
    return VGroup(bowl, rimline)


def embryo(cx, cy):
    """A simple embryo: a curved body with a rounded head end and a stripe for the neural tube."""
    body = Arc(radius=1.05, start_angle=PI * 0.2, angle=PI * 1.35, arc_center=[cx, cy, 0], stroke_color=TEXT,
               stroke_width=78, stroke_opacity=0.55, cap_style=CapStyleType.ROUND)
    stripe = Arc(radius=1.05, start_angle=PI * 0.3, angle=PI * 1.2, arc_center=[cx, cy, 0], stroke_color=TEAL,
                 stroke_width=10, cap_style=CapStyleType.ROUND)
    head = Circle(radius=0.5, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.25).move_to(
        [cx + 1.05 * math.cos(PI * 1.55), cy + 1.05 * math.sin(PI * 1.55), 0])
    return VGroup(body, stripe)


class S26Drug(SpokenScene):
    def construct(self):
        cx = DCX
        d = dish()
        emb = embryo(cx, 0.85)
        el = T("mouse embryo", 30, LGREY).move_to([cx, -1.95, 0])
        cit = T("Calegari and Huttner, 2003", 28, GOLD).move_to([cx, -3.0, 0])
        self.at("cultured mouse embryos")
        self.play(FadeIn(d), FadeIn(emb, scale=0.8), FadeIn(el), FadeIn(cit), run_time=1.3)
        X = 3.9
        drug = chip("drug", TEXT, size=32).move_to([X, 3.0, 0])
        g1 = chip("longer G1", TEAL, size=34).move_to([X, 1.45, 0])
        a1 = arr([X, 2.55, 0], [X, 1.95, 0], GREY, 5)
        self.at("a drug that lengthened")
        self.play(FadeIn(drug, shift=DOWN * 0.2), run_time=0.5)
        self.at("lengthened")
        self.play(GrowArrow(a1), FadeIn(g1, shift=UP * 0.15), run_time=0.6)
        en = chip("early neurons", GREEN, size=34).move_to([X, -0.4, 0])
        a2 = DashedVMobject(arr([X, 0.95, 0], [X, 0.15, 0], GREY, 5), num_dashes=8)
        q = T("?", 72, RED, weight=BOLD).move_to([X + 0.8, 0.55, 0])
        nn = VGroup(*[dot(cx + dx, 0.85 + dy, 0.17, GREEN, 0.95, 2)
                      for dx, dy in ((-0.9, 0.4), (-0.55, 0.85), (0.1, 1.0), (0.75, 0.75))])
        self.at("led to early neurogenesis")
        self.play(FadeIn(nn, scale=0.3), Create(a2), FadeIn(q, scale=0.5), FadeIn(en, shift=UP * 0.2), run_time=1.0)
        co = T("cause or consequence?", 32, RED).move_to([X, -1.45, 0])
        self.at("causes the switch")
        self.play(FadeIn(co, shift=UP * 0.1), run_time=0.6)
        op = T("open", 44, RED, weight=BOLD).move_to([X, -2.35, 0])
        self.at("still open")
        self.play(FadeIn(op, scale=0.6), run_time=0.5)
        self.finish()


def puzzle_card(cx, n, q_text, color=RED):
    box = RoundedRectangle(corner_radius=0.25, width=6.0, height=6.6, stroke_color=GREY, stroke_width=3.5,
                           fill_color=GREY, fill_opacity=0.07).move_to([cx, 0.0, 0])
    head = T(f"Puzzle {n}", 38, RED, weight=BOLD).move_to([cx, 2.6, 0])
    q = T(q_text, 32, RED, line_spacing=0.8).move_to([cx, 1.3, 0])
    return VGroup(box, head, q)


class S27Answer(SpokenScene):
    def construct(self):
        c1 = puzzle_card(-3.2, 1, "scaffold\nor source?")
        c2 = puzzle_card(3.2, 2, "why divide at\nthe ventricle?")
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.6)
        ck = check(-3.2, -2.35)
        a1 = T("the scaffold\nis the source", 32, GREEN, line_spacing=0.8).move_to([-3.2, -0.5, 0])
        self.at("has an answer")
        self.play(Create(ck), run_time=0.7)
        self.at("The scaffold is the source")
        self.play(FadeIn(a1, shift=UP * 0.1), run_time=0.7)
        half = VGroup(Circle(radius=0.42, stroke_color=GOLD, stroke_width=6),
                      Sector(radius=0.42, start_angle=PI / 2, angle=PI, fill_color=GOLD, fill_opacity=0.9, stroke_width=0)).move_to([3.2, -2.2, 0])
        hl = T("partly settled", 26, GOLD).move_to([3.2, -2.85, 0])
        self.at("The second has a partial answer")
        self.play(FadeIn(half, scale=0.5), FadeIn(hl), run_time=0.7)
        a2a = T("fits the centrosome", 30, GOLD).move_to([3.2, 0.2, 0])
        self.at("The trip to the ventricle")
        self.play(FadeIn(a2a, shift=UP * 0.1), run_time=0.7)
        a2b = T("may let more cells\nshare the surface", 30, GOLD, line_spacing=0.8).move_to([3.2, -0.95, 0])
        self.at("may let more cells")
        self.play(FadeIn(a2b, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S28Take(SpokenScene):
    def construct(self):
        top = T("The cortex gets a count", 44, TEXT, font=TITLE_FONT).move_to([0, 3.45, 0])
        h1 = T("radial glia kept by each division", 34, BLUE).move_to([0, 2.75, 0])

        def opt(x, y, n, label, color=BLUE):
            ds = [dot(x + (i - (n - 1) / 2) * 1.2, y, 0.5, color, 0.85) for i in range(n)]
            return VGroup(VGroup(*ds), T(label, 34, TEXT).move_to([x, y - 0.95, 0]))
        o2 = opt(-3.7, 1.7, 2, "two")
        o1 = opt(0.0, 1.7, 1, "one")
        o0 = VGroup(DashedVMobject(Circle(radius=0.5, stroke_color=GREY, stroke_width=3.5).move_to([3.7, 1.7, 0]), num_dashes=14),
                    T("none", 34, TEXT).move_to([3.7, 0.75, 0]))
        sep = Line([-6.2, -0.1, 0], [6.2, -0.1, 0], color=GREY, stroke_width=2, stroke_opacity=0.5)
        h2 = T("neurons from each spent daughter", 34, GREEN).move_to([0, -0.7, 0])
        # row 2: a spent daughter makes one neuron directly (left) or goes through an intermediate progenitor (right)
        RY = -1.95
        sp_a = dot(-5.7, RY, 0.4, TEXT, 0.2)
        ar_a = arr([-5.15, RY, 0], [-4.1, RY, 0], GREY, 5)
        ne_a = dot(-3.5, RY, 0.4, GREEN, 0.9)
        la = T("one neuron, directly", 28, GREEN).move_to([-4.4, -3.05, 0])
        sp_b = dot(0.9, RY, 0.4, TEXT, 0.2)
        ar_b = arr([1.45, RY, 0], [2.3, RY, 0], GREY, 5)
        ip_b = ipdot(2.85, RY, 0.4)
        ar_c = arr([3.4, RY, 0], [4.3, RY, 0], GREY, 5)
        ne_b = VGroup(dot(4.85, RY, 0.4, GREEN, 0.9), dot(5.7, RY, 0.4, GREEN, 0.9))
        lb = VGroup(T("or, usually, two,", 28, GREEN), T("through an intermediate progenitor", 28, GREEN)).arrange(DOWN, buff=0.06).move_to([3.35, -3.1, 0])
        self.at("What the cortex gets is a count")
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.7)
        self.at("how many radial glia")
        self.play(FadeIn(h1, shift=DOWN * 0.1), FadeIn(sep), run_time=0.5)
        self.at("each division keeps")
        self.play(LaggedStart(FadeIn(o2, scale=0.8), FadeIn(o1, scale=0.8), FadeIn(o0, scale=0.8), lag_ratio=0.35), run_time=0.8)
        self.at("keeps")
        self.play(FadeIn(h2, shift=DOWN * 0.1), run_time=0.4)
        self.at("and what", lead=0.35)
        self.play(FadeIn(sp_a, scale=0.6), FadeIn(sp_b, scale=0.6), run_time=0.3)
        self.play(GrowArrow(ar_a), FadeIn(ne_a, scale=0.6), FadeIn(la), GrowArrow(ar_b), FadeIn(ip_b, scale=0.6),
                  GrowArrow(ar_c), FadeIn(ne_b, scale=0.6), FadeIn(lb), run_time=0.6)
        self.finish()


class S29End(EndCard):
    LINE = "Count radial glia kept, and neurons yielded per spent daughter."
