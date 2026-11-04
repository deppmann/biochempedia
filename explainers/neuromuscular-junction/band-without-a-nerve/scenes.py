"""Neuromuscular junction, chapter 2: A Band Without a Nerve  (Biochemistrypedia chaptered film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by every chapter of this lesson)
  BLUE   = acetylcholine receptors and their clusters ("band" of clusters, "receptor clusters")
  INDIGO = receptor-subunit RNA (the shaded band in s09; its own colour, not the receptor blue)
  PURPLE = the motor neuron: axon and nerve terminal
  YELLOW = agrin (the nerve's clustering signal)
  TEAL   = Lrp4 (not used in this chapter)
  GREEN  = MuSK
  ORANGE = rapsyn
  RED    = acetylcholine, "not there / not needed / no band / false"
  GREY   = muscle (diaphragm schematic), labels
  GOLD   = the prepattern (the muscle's rough map): dashed outline of the band, highlights on the table
  PINK   = the fluorescent toxin that labels receptors
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E983B8"
INDIGO = "#6F7DFF"
LG = "#D1D6DF"          # light grey for secondary labels (readable on the dark ground)

NERVE, RECEPTOR, AGRIN, LRP4, MUSK, RAPSYN, ACH = PURPLE, BLUE, YELLOW, TEAL, GREEN, ORANGE, RED
PREPAT, TOXIN, RNA = GOLD, PINK, INDIGO


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def cdim(c, o=0.45):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def cluster(x, y, s=0.6, color=RECEPTOR):
    """A receptor cluster: a tight clump of three dots."""
    r = 0.10 * s
    off = 0.17 * s
    pts = [(-off, -off * 0.6), (off, -off * 0.6), (0, off * 0.9)]
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to([x + a, y + b, 0])
                    for a, b in pts])


def strike(chp, color=RED):
    w, h = chp.width, chp.height
    c = chp.get_center()
    return Line(c + np.array([-w / 2, -h / 2, 0]), c + np.array([w / 2, h / 2, 0]), color=color, stroke_width=7)


def arr(a, b, color=GREY, w=7, tip=0.28):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def cross_mark(c, r=0.3, w=8):
    c = np.array(c, dtype=float)
    return VGroup(Line(c + np.array([-r, -r, 0]), c + np.array([r, r, 0]), color=RED, stroke_width=w),
                  Line(c + np.array([-r, r, 0]), c + np.array([r, -r, 0]), color=RED, stroke_width=w))


def leader(a, b, color=GREY, w=2.5):
    return Line(a, b, color=color, stroke_width=w)


# ---- the schematic diaphragm (built around the origin, then placed) -------------------------
DW, DH = 6.3, 6.0          # diaphragm schematic size at scale 1
EY = 0.0                 # centre line when two sit side by side
LX, RX = -3.5, 3.5
BX, BY, BS = -0.4, -0.25, 1.05       # the single enlarged diaphragm (s09, s10)
TDX, TDY, TDS = 3.5, -0.1, 1.04     # the table-side diaphragm (s11 to s14)
HY = 3.5                            # headings above the table-side diaphragm


def place(m, cx, cy, s=1.0):
    return m.scale(s, about_point=ORIGIN).shift([cx, cy, 0])


def ellipse_rel():
    return Ellipse(width=DW, height=DH, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)


def wide_band_rel(seed=3):
    """band formed with no nerve: wide, sparse (16 clusters)"""
    rng = np.random.RandomState(seed)
    xs, ys = [-1.3, -0.45, 0.45, 1.3], [-1.85, -0.62, 0.62, 1.85]
    return VGroup(*[cluster(x + rng.uniform(-0.12, 0.12), y + rng.uniform(-0.1, 0.1), s=0.8)
                    for y in ys for x in xs])


def narrow_band_rel():
    """band under a nerve: narrow, dense (40 clusters, the same glyph)"""
    xs, ys = np.linspace(-0.72, 0.72, 4), np.linspace(-2.05, 2.05, 10)
    return VGroup(*[cluster(x, y, s=0.8) for y in ys for x in xs])


def terminal_rel():
    bar = RoundedRectangle(corner_radius=0.3, width=2.3, height=5.0, stroke_color=NERVE, stroke_width=3,
                           fill_color=NERVE, fill_opacity=0.16)
    ax = Line([0, 2.5, 0], [0, 3.2, 0], color=NERVE, stroke_width=12)
    return VGroup(bar, ax)


def terminal_label(cx, cy, s=1.0):
    """'nerve terminal' sits just right of the terminal, with a short leader"""
    t = VGroup(T("nerve", 26, NERVE), T("terminal", 26, NERVE)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    t.move_to([cx + 2.15 * s, cy + 0.5 * s, 0])
    ld = leader([t.get_left()[0] - 0.05, t.get_center()[1], 0], [cx + 1.18 * s, t.get_center()[1], 0], NERVE, 2.5)
    return VGroup(t, ld)


def shade_rel(wide=True):
    if wide:
        spec = [(3.4, 4.4, 0.12), (3.0, 4.0, 0.2), (2.2, 3.3, 0.2)]
    else:
        spec = [(1.9, 4.2, 0.2)]
    return VGroup(*[RoundedRectangle(corner_radius=0.5, width=w, height=h, stroke_width=0, fill_color=RNA,
                                     fill_opacity=o) for w, h, o in spec])


def outline_rel(w=3.5, h=4.5):
    return DashedVMobject(RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=PREPAT, stroke_width=5),
                          num_dashes=40)


def outline_narrow():
    return outline_rel(1.95, 4.6)


def scatter_rel(seed=1, r=0.09):
    """single receptors spread evenly over the muscle (no clusters)"""
    rng = np.random.RandomState(seed)
    pts = []
    for row in range(8):
        for col in range(8):
            x = -2.65 + col * 0.76 + rng.uniform(-0.2, 0.2) + (0.38 if row % 2 else 0)
            y = -2.45 + row * 0.74 + rng.uniform(-0.18, 0.18)
            if (x / 2.9) ** 2 + (y / 2.75) ** 2 < 1:
                pts.append((x, y))
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=RECEPTOR, fill_opacity=0.95).move_to([x, y, 0])
                    for x, y in pts])


def head(text, color, cx, y=3.5, size=30):
    return T(text, size, color).move_to([cx, y, 0])


def schem_label(pos=(0, 3.5), size=26):
    return T("schematic, not data", size, LG).move_to([pos[0], pos[1], 0])


# ---- the embryo drawing (s03 -> s05) -----------------------------------------------------------
def _spine(t):
    th = np.radians(160 - 215 * t)
    return np.array([2.5 * np.cos(th), 2.5 * np.sin(th) - 0.2, 0.0])


def _nrm(t):
    th = np.radians(160 - 215 * t)
    return np.array([np.cos(th), np.sin(th), 0.0])


def _tan(t):
    th = np.radians(160 - 215 * t)
    return np.array([np.sin(th), -np.cos(th), 0.0])


def _hh(t):
    return 0.12 + 0.95 * (1 - t) ** 0.7 + 0.3 * np.exp(-((t - 0.07) / 0.09) ** 2)


SPOT_T = 0.5


def embryo_outline():
    ts = np.linspace(0, 1, 46)
    outer = [_spine(t) + _nrm(t) * _hh(t) for t in ts]
    inner = [_spine(t) - _nrm(t) * _hh(t) for t in ts[::-1]]
    p0, n0, t0, h0 = _spine(0), _nrm(0), _tan(0), _hh(0)
    cap = [p0 + h0 * (np.cos(ph) * n0 + np.sin(ph) * (-t0)) for ph in np.linspace(np.pi, 0, 14)[1:-1]]
    pts = outer + inner + cap
    pts = pts + [pts[0]]
    e = VMobject(stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14)
    e.set_points_smoothly(pts)
    eye = Circle(radius=0.11, stroke_width=0, fill_color=LG, fill_opacity=1).move_to(
        _spine(0.05) + _nrm(0.05) * 0.55)
    return VGroup(e, eye)


def spot_c():
    return _spine(SPOT_T)


def embryo_nerve_arrow():
    c, n = spot_c(), _nrm(SPOT_T)
    return arr(c + n * (_hh(SPOT_T) + 1.35), c + n * 0.5, NERVE, w=9, tip=0.35)


def embryo_spot():
    return DashedVMobject(Circle(radius=0.5, stroke_color=NERVE, stroke_width=4), num_dashes=16).move_to(spot_c())


def embryo_diaphragm():
    n = _nrm(SPOT_T)
    ang = np.arctan2(n[1], n[0])
    d = Ellipse(width=1.3, height=0.72, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.4)
    return d.rotate(ang).move_to(spot_c())


E_S, E_X, E_Y = 0.8, 2.45, -0.4     # the embryo's place on the date card (s04, s05)


def epl(m, s=E_S, cx=E_X, cy=E_Y):
    return place(m, cx, cy, s)


def ept(x, y, z=0):
    """a point in embryo-relative coordinates, in the s04 placement"""
    return np.array([E_X + x * E_S, E_Y + y * E_S, 0])


# ---- the table (s11 -> s16) ---------------------------------------------------------------------
ROWS = [("no motor axons", NERVE), ("no agrin", AGRIN), ("no MuSK", MUSK), ("no rapsyn", RAPSYN)]
ROW_Y = [1.55, 0.35, -0.85, -2.05]
RES_X = -1.5
RESULTS = {0: ("band", BLUE), 1: ("early band", BLUE), 2: ("no band", RED), 3: ("no band", RED)}


def table_frame():
    h1 = T("removed", 26, LG).move_to([-5.0, 2.65, 0])
    h2 = T("band of clusters?", 26, LG).move_to([RES_X, 2.65, 0])
    lines = VGroup(*[Line([-6.6, y, 0], [0.1, y, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.5)
                     for y in [2.15, 0.95, -0.25, -1.45, -2.65]])
    return VGroup(h1, h2, lines)


def row_label(i):
    t, c = ROWS[i]
    ch = bchip(t, c, 30)
    ch.move_to([-6.5 + ch.width / 2, ROW_Y[i], 0])
    return ch


def row_result(i, filled=True):
    if not filled:
        return T("?", 36, LG).move_to([RES_X, ROW_Y[i], 0])
    t, c = RESULTS[i]
    return T(t, 32, c, weight=BOLD).move_to([RES_X, ROW_Y[i], 0])


def row_box(i, color=PREPAT, w=6.8):
    return RoundedRectangle(corner_radius=0.15, width=w, height=1.0, stroke_color=color, stroke_width=4,
                            fill_opacity=0).move_to([-3.25, ROW_Y[i], 0])


def table_ellipse():
    return place(ellipse_rel(), TDX, TDY, TDS)


def below(text, color=LG, size=26):
    return T(text, size, color).move_to([TDX, -3.55, 0])


def pause_frame():
    """the question of s06, rebuilt (also the still of s07)"""
    dl = place(ellipse_rel(), LX, EY)
    dr = place(ellipse_rel(), RX, EY)
    hl = head("if the nerve chooses", NERVE, LX)
    hr = head("if the muscle chooses", LG, RX)
    ql = T("?", 130, LG, weight=BOLD).move_to([LX, EY, 0])
    qr = T("?", 130, LG, weight=BOLD).move_to([RX, EY, 0])
    return dl, dr, hl, hr, ql, qr


class S00Title(TitleCard):
    LESSON = "Building the neuromuscular junction"
    TITLE = "A Band Without a Nerve"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    """the chain from chapter one, nerve greyed out: no nerve, no clusters?"""

    def construct(self):
        names = [("nerve", NERVE), ("agrin", AGRIN), ("MuSK", MUSK), ("clusters", RECEPTOR)]
        chips = [bchip(t, c, 56) for t, c in names]
        ys = [2.75, 0.95, -0.85, -2.65]
        for c, y in zip(chips, ys):
            c.move_to([-3.7, y, 0])
        ars = [arr(chips[i].get_bottom() + DOWN * 0.08, chips[i + 1].get_top() + UP * 0.08, GREY, w=8)
               for i in range(3)]
        q = T("?", 150, RED, weight=BOLD).next_to(chips[3], RIGHT, buff=0.5)
        l1 = T("No nerve,", 84, TEXT, font=TITLE_FONT)
        l2 = T("no clusters?", 84, TEXT, font=TITLE_FONT)
        ques = VGroup(l1, l2).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        fit(ques, max_w=7.2)
        ques.move_to([3.0, 0.5, 0])
        # the whole chain from chapter one is on screen from the first frame
        self.add(*chips, *ars)
        self.at("if agrin")
        self.play(Indicate(chips[1], color=AGRIN, scale_factor=1.12), run_time=0.5)
        self.at("from the nerve")
        self.play(Indicate(chips[0], color=NERVE, scale_factor=1.12), run_time=0.45)
        self.at("switches on")
        self.play(Indicate(chips[2], color=MUSK, scale_factor=1.12), run_time=0.6)
        self.at("then no nerve")
        self.play(Create(strike(chips[0])), *cdim(chips[0]), ars[0].animate.set_opacity(0.3), FadeIn(l1, shift=UP * 0.2),
                  run_time=0.7)
        self.at("no clusters")
        self.play(FadeIn(q, scale=1.4), FadeIn(l2, shift=UP * 0.2), Indicate(chips[3], color=BLUE, scale_factor=1.1),
                  run_time=0.7)
        self.at("is that true")
        self.play(Indicate(q, color=RED, scale_factor=1.25), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
DC, DR = np.array([-1.3, -0.2, 0.0]), 3.5
CELLS = [(-2.6, 1.3), (-0.4, 1.6), (-1.8, 0.3), (0.2, -0.1), (-2.9, -1.1), (-0.9, -1.1), (-1.6, -2.3)]
CELL_A = [15, -10, -25, 20, 5, -15, 10]


def dish_clusters():
    return VGroup(*[cluster(x + 0.2, y + 0.02, 1.0) for x, y in CELLS])


def dish_stuff():
    dish = Circle(radius=DR, stroke_color=TEXT, stroke_width=5, fill_color=GREY, fill_opacity=0.07).move_to(DC)
    cells = VGroup(*[RoundedRectangle(corner_radius=0.25, width=2.1, height=0.55, stroke_color=GREY, stroke_width=2,
                                      fill_color=GREY, fill_opacity=0.4).rotate(a * DEGREES).move_to([x, y, 0])
                     for (x, y), a in zip(CELLS, CELL_A)])
    return dish, cells


def dish_labels():
    dl = T("culture dish", 28, TEXT).move_to([4.6, 3.1, 0])
    dline = leader([3.4, 2.95, 0], DC + np.array([DR * np.cos(np.radians(40)), DR * np.sin(np.radians(40)), 0]) + np.array([0.05, 0.05, 0]),
                   TEXT, 2.5)
    ml = T("muscle cells", 28, LG).move_to([4.7, -0.9, 0])
    mline = leader([3.5, -0.78, 0], [1.4, -0.28, 0], LG, 2.5)
    nch = bchip("neurons", NERVE, 34).move_to([4.7, 1.7, 0])
    rl = T("receptor clusters", 28, RECEPTOR).move_to([4.5, -2.4, 0])
    return dl, dline, ml, mline, nch, rl


class S02Dish(SpokenScene):
    def construct(self):
        dish, cells = dish_stuff()
        dl, dline, ml, mline, nch, rl = dish_labels()
        # the dish is on screen from the first frame (no blank beat after s01)
        self.add(dish, dl, dline)
        self.at("muscle cells grown")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.1), run_time=1.1)
        self.play(FadeIn(ml), Create(mline), run_time=0.4)
        self.at("no neurons at all")
        self.play(FadeIn(nch, shift=LEFT * 0.2), run_time=0.4)
        self.play(Create(strike(nch)), *cdim(nch), run_time=0.5)
        cl = dish_clusters()
        self.at("make small receptor clusters")
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in cl], lag_ratio=0.12), FadeIn(rl), run_time=1.5)
        self.at("by themselves")
        self.play(Indicate(cl, color=RECEPTOR, scale_factor=1.25), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Embryo(SpokenScene):
    def construct(self):
        dish, cells = dish_stuff()
        dl, dline, ml, mline, nch, rl = dish_labels()
        cl = dish_clusters()
        old = VGroup(dish, cells, dl, dline, ml, mline, nch, strike(nch), rl, cl)
        self.add(old)
        emb = place(embryo_outline(), 0.1, -0.2, 1.0)
        arrow = place(embryo_nerve_arrow(), 0.1, -0.2, 1.0)
        spot = place(embryo_spot(), 0.1, -0.2, 1.0)
        el = T("mouse embryo", 28, LG).move_to([-4.6, -3.2, 0])
        nl = T("nerve?", 32, NERVE).move_to(arrow.get_start() + np.array([1.2, 0.1, 0]))
        sl = T("spot?", 32, NERVE).move_to(spot.get_center() + np.array([-1.2, 0.0, 0]))
        sl_ld = leader(sl.get_right() + RIGHT * 0.05, spot.get_center() + np.array([-0.52, 0, 0]), NERVE, 2.5)
        self.wait(0.3)
        self.at("not an embryo")
        self.play(old.animate.shift(LEFT * 9).set_opacity(0), FadeIn(emb, shift=RIGHT * 0.3), run_time=1.0)
        self.at("in an animal")
        self.play(FadeIn(el), Indicate(emb[0], color=GREY, scale_factor=1.03), run_time=0.7)
        self.at("a nerve might")
        self.play(FadeIn(arrow, shift=DOWN * 0.3), FadeIn(nl), run_time=0.7)
        self.at("marked the spot")
        self.play(Create(spot), FadeIn(sl), Create(sl_ld), run_time=0.4)
        self.at("spot first")
        self.play(Indicate(spot, color=NERVE, scale_factor=1.25), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s04_end():
    """everything on screen at the end of s04 (rebuilt at the start of s05)"""
    emb = epl(embryo_outline())
    d = epl(embryo_diaphragm())
    dc = ept(*spot_c()[:2])
    dl = T("diaphragm", 28, LG).move_to([5.75, 1.15, 0])
    dld = leader(dl.get_left() + LEFT * 0.08, dc + np.array([0.3, -0.02, 0]), LG, 2.5)
    n = _nrm(SPOT_T)
    xm = cross_mark(ept(*(spot_c() + n * (_hh(SPOT_T) + 0.95))[:2]), 0.28, 8)
    nt = T("no motor axons", 28, RED).move_to(ept(*(spot_c() + n * (_hh(SPOT_T) + 0.95))[:2]) + np.array([0.2, 0.62, 0]))
    yr = T("2001", 100, GOLD, font=TITLE_FONT).move_to([-3.4, 1.8, 0])
    g1 = T("Yang, Burden and colleagues", 28, TEXT).move_to([-3.4, 0.3, 0])
    g2 = T("Lin, Sanes, Lee and colleagues", 28, TEXT).move_to([-3.4, -0.5, 0])
    return emb, d, dl, dld, xm, nt, yr, g1, g2


class S04Mice(SpokenScene):
    def construct(self):
        emb = place(embryo_outline(), 0.1, -0.2, 1.0)
        arrow = place(embryo_nerve_arrow(), 0.1, -0.2, 1.0)
        spot = place(embryo_spot(), 0.1, -0.2, 1.0)
        el = T("mouse embryo", 28, LG).move_to([-4.6, -3.2, 0])
        nl = T("nerve?", 32, NERVE).move_to(arrow.get_start() + np.array([1.2, 0.1, 0]))
        sl = T("spot?", 32, NERVE).move_to(spot.get_center() + np.array([-1.2, 0.0, 0]))
        sl_ld = leader(sl.get_right() + RIGHT * 0.05, spot.get_center() + np.array([-0.52, 0, 0]), NERVE, 2.5)
        self.add(emb, arrow, spot, el, nl, sl, sl_ld)
        e_end, d, dl, dld, xm, nt, yr, g1, g2 = s04_end()
        k = E_S
        sh = np.array([E_X - 0.1 * k, E_Y + 0.2 * k, 0])
        self.at("in 2001")
        self.play(FadeOut(el), FadeOut(nl), FadeOut(sl), FadeOut(sl_ld), FadeOut(arrow), FadeOut(spot),
                  emb.animate.scale(k, about_point=ORIGIN).shift(sh),
                  FadeIn(yr, shift=RIGHT * 0.3), run_time=1.3)
        self.at("two groups")
        self.play(FadeIn(g1, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(g2, shift=UP * 0.15), run_time=0.5)
        self.at("mouse embryos")
        self.play(Indicate(emb[0], color=GREY, scale_factor=1.04), run_time=0.8)
        self.at("whose diaphragm")
        # the 'nerve might have marked the spot' guess is cleared: arrow and spot leave, the diaphragm arrives
        self.play(FadeIn(d, scale=0.6), FadeIn(dl), Create(dld), run_time=0.9)
        self.at("no motor axons")
        self.play(Create(xm), FadeIn(nt, scale=0.9), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
S5C = (-3.0, -0.1)      # the big diaphragm of s05
IX = 3.9                # centre of the close-up on the right


def s05_parts():
    big = place(ellipse_rel(), S5C[0], S5C[1], 1.08)
    dlab = T("diaphragm", 30, LG).move_to([S5C[0], 3.5, 0])
    sch = T("schematic", 26, LG).move_to([S5C[0], -3.55, 0])
    return big, dlab, sch


def receptor_block(x, base_y):
    return RoundedRectangle(corner_radius=0.12, width=0.75, height=1.3, stroke_color=RECEPTOR, stroke_width=3,
                            fill_color=RECEPTOR, fill_opacity=0.5).move_to([x, base_y + 0.65, 0])


def toxin_dot(x, y):
    return Circle(radius=0.27, stroke_color=TOXIN, stroke_width=3, fill_color=TOXIN, fill_opacity=0.95).move_to([x, y, 0])


def s05_labelled_spots():
    return place(wide_band_rel(), S5C[0], S5C[1], 1.08).set_color(TOXIN)


def s05_zoom_link():
    source = np.array([S5C[0] + 1.3, S5C[1] + 0.62, 0])
    ring = Circle(radius=0.38, color=TOXIN, stroke_width=3).move_to(source)
    link = leader(source + RIGHT * 0.38, [IX - 2.85, 0.65, 0], TOXIN, 3)
    return VGroup(ring, link)


def s05_inset():
    frame = RoundedRectangle(corner_radius=0.25, width=5.7, height=4.7, stroke_color=GREY, stroke_width=2,
                             fill_color=GREY, fill_opacity=0.05).move_to([IX, -0.35, 0])
    up = T("up close", 26, LG).move_to([IX - 1.9, 1.55, 0])
    mem = RoundedRectangle(corner_radius=0.1, width=4.9, height=0.3, stroke_color=GREY, stroke_width=3,
                           fill_color=GREY, fill_opacity=0.45).move_to([IX, -1.2, 0])
    recs = VGroup(*[receptor_block(IX + dx, -1.05) for dx in (-1.6, 0.0, 1.6)])
    return frame, up, mem, recs


class S05Stain(SpokenScene):
    def construct(self):
        # rebuild the end of s04
        emb, d, dl, dld, xm, nt, yr, g1, g2 = s04_end()
        self.add(emb, d, dl, dld, xm, nt, yr, g1, g2)
        big, dlab, sch = s05_parts()
        self.at("the diaphragm is")
        # clear the old layer first, then grow the new diaphragm (no ghosts of the date card)
        self.play(*[FadeOut(m) for m in (emb, dl, dld, xm, nt, yr, g1, g2)], run_time=0.5)
        self.play(ReplacementTransform(d, big), FadeIn(dlab), FadeIn(sch), run_time=0.9)
        self.at("drives breathing")
        self.play(Indicate(big, color=GREY, scale_factor=1.03), run_time=0.9)
        chip_t = bchip("fluorescent toxin", TOXIN, 28).move_to([3.9, 3.0, 0])
        wash = place(Ellipse(width=DW, height=DH, stroke_width=0, fill_color=TOXIN, fill_opacity=0.13), S5C[0], S5C[1], 1.08)
        self.at("stained it with a toxin")
        ap = arr([2.0, 2.85, 0], [-0.55, 1.35, 0], TOXIN, w=7)
        drops = VGroup(*[Circle(radius=0.14, stroke_width=0, fill_color=TOXIN, fill_opacity=0.95).move_to([2.0, 2.85, 0])
                         for _ in range(3)])
        self.play(FadeIn(chip_t, shift=DOWN * 0.2), GrowArrow(ap), run_time=0.4)
        self.play(LaggedStart(*[d_.animate.move_to([-0.2 - 0.9 * i, 1.0 - 0.6 * i, 0]) for i, d_ in enumerate(drops)],
                              lag_ratio=0.2), FadeIn(drops), FadeIn(wash, rate_func=smooth),
                  FadeIn(s05_labelled_spots()), run_time=0.8)
        frame, up, mem, recs = s05_inset()
        self.at("that labels")
        self.play(FadeOut(drops), FadeIn(frame), FadeIn(up), FadeIn(mem), FadeIn(recs), Create(s05_zoom_link()), run_time=0.5)
        tds = VGroup(*[toxin_dot(IX + dx, 1.0) for dx in (-1.6, 0.0, 1.6)])
        self.at("labels the")
        self.play(FadeIn(tds, shift=DOWN * 0.2), run_time=0.4)
        self.play(*[t.animate.move_to([IX + dx, 0.51, 0]) for t, dx in zip(tds, (-1.6, 0.0, 1.6))], run_time=0.7)
        self.at("acetylcholine receptors")
        rl = T("acetylcholine receptors", 28, RECEPTOR).move_to([IX, -2.1, 0])
        self.play(FadeIn(rl), *[Indicate(r, color=RECEPTOR, scale_factor=1.15) for r in recs], run_time=0.9)
        self.finish()


def s05_final():
    big, dlab, sch = s05_parts()
    chip_t = bchip("fluorescent toxin", TOXIN, 28).move_to([3.9, 3.0, 0])
    ap = arr([2.0, 2.85, 0], [-0.55, 1.35, 0], TOXIN, w=7)
    frame, up, mem, recs = s05_inset()
    tds = VGroup(*[toxin_dot(IX + dx, 0.51) for dx in (-1.6, 0.0, 1.6)])
    rl = T("acetylcholine receptors", 28, RECEPTOR).move_to([IX, -2.1, 0])
    wash = place(Ellipse(width=DW, height=DH, stroke_width=0, fill_color=TOXIN, fill_opacity=0.13), S5C[0], S5C[1], 1.08)
    return big, [dlab, sch, chip_t, ap, wash, s05_labelled_spots(), frame, up, mem, recs, tds, rl, s05_zoom_link()]


# ---------------------------------------------------------------------------------------------
class S06Q(SpokenScene):
    def construct(self):
        big, rest = s05_final()
        self.add(big, *rest)
        dl, dr, hl, hr, ql, qr = pause_frame()
        self.at("if the nerve chooses")
        self.play(*[FadeOut(m) for m in rest], ReplacementTransform(big, dl), FadeIn(dr), FadeIn(hl), run_time=1.0)
        self.at("what should the stain show")
        self.play(FadeIn(ql, scale=0.6), run_time=0.6)
        self.at("and if the muscle chooses")
        self.play(FadeIn(hr), run_time=0.5)
        self.play(FadeIn(qr, scale=0.6), run_time=0.6)
        self.finish()


class S07Pause(NarratedScene):
    """a silent beat: the question stays on screen, still, with a visible countdown"""

    def construct(self):
        self.add(*pause_frame())
        lab = T("Pause and predict", 36, GOLD, weight=BOLD).move_to([0, -3.4, 0])
        bar = Rectangle(width=6.0, height=0.14, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([0, -3.75, 0])
        track = Rectangle(width=6.0, height=0.14, stroke_width=0, fill_color=GREY, fill_opacity=0.35).move_to(bar)
        self.add(track, bar, lab)
        self.play(bar.animate.stretch(0.001, 0, about_edge=LEFT), run_time=4.7, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s08_final():
    """left: no motor axons, wide band; right: normal, narrow band under a nerve"""
    dl = place(ellipse_rel(), LX, EY)
    cl = place(wide_band_rel(), LX, EY)
    ol = place(outline_rel(), LX, EY)
    dr = place(ellipse_rel(), RX, EY)
    term = place(terminal_rel(), RX, EY)
    cr = place(narrow_band_rel(), RX, EY)
    orr = place(outline_narrow(), RX, EY)
    tl = terminal_label(RX, EY)
    hl = head("no motor axons", NERVE, LX)
    hr = head("normal", TEXT, RX)
    sch = schem_label()
    return dl, cl, ol, dr, term, cr, orr, tl, hl, hr, sch


class S08Band(SpokenScene):
    def construct(self):
        dl, dr, hl, hr, ql, qr = pause_frame()
        self.add(dl, dr, hl, hr, ql, qr)
        _, wide, ol, _, term, cr, orr, tl, hl2, hr2, sch = s08_final()
        # both diaphragms are shown from the start: question marks out, the normal one (nerve terminal and
        # its clusters) in at full opacity, headings swapped
        self.play(FadeOut(ql), FadeOut(qr), FadeOut(hl), FadeOut(hr), FadeIn(hl2), FadeIn(hr2), FadeIn(sch),
                  FadeIn(term), FadeIn(tl), FadeIn(cr), FadeIn(orr), FadeIn(wide), FadeIn(ol), run_time=0.8)
        self.at("receptor clusters")
        self.play(Indicate(wide, color=RECEPTOR, scale_factor=1.06), run_time=0.7)
        self.at("across the middle")
        self.play(Indicate(ol, color=PREPAT, scale_factor=1.03), run_time=0.8)
        self.at("where the nerve")
        self.play(Indicate(orr, color=PREPAT, scale_factor=1.03),
                  Indicate(term[0], color=NERVE, scale_factor=1.03), run_time=0.6)
        self.at("would normally arrive")
        self.play(Indicate(term[1], color=NERVE, scale_factor=1.4), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def big_state():
    """the single no-axon diaphragm, enlarged, with the band's clusters (s09)"""
    dl = place(ellipse_rel(), BX, BY, BS)
    cl = place(wide_band_rel(), BX, BY, BS)
    hl = head("no motor axons", NERVE, BX, y=3.55)
    return dl, cl, hl


class S09Rna(SpokenScene):
    def construct(self):
        dl, cl, ol, dr, term, cr, orr, tl, hl, hr, sch = s08_final()
        self.add(dl, cl, ol, dr, term, cr, orr, tl, hl, hr, sch)
        c0 = np.array([LX, EY, 0])
        sh = np.array([BX - LX, BY - EY, 0])
        gb = T("Burden's group", 30, TEXT).move_to([5.2, 2.5, 0])
        sch2 = schem_label((5.2, 3.5), 26)
        # the right-hand panel and the outline leave first; the left diaphragm then grows into place
        self.at("burden's group")
        self.play(*[FadeOut(m) for m in (dr, term, cr, orr, tl, hr, sch, ol)], run_time=0.5)
        self.play(dl.animate.scale(BS, about_point=c0).shift(sh),
                  cl.animate.scale(BS, about_point=c0).shift(sh),
                  hl.animate.move_to([BX, 3.55, 0]), FadeIn(gb), FadeIn(sch2), run_time=1.0)
        rl = T("receptor RNA", 32, RNA, weight=BOLD).move_to([5.2, 1.3, 0])
        self.at("receptor rna")
        self.play(FadeIn(rl, shift=LEFT * 0.2), run_time=0.5)
        shade = place(shade_rel(), BX, BY, BS)
        ld = leader([rl.get_left()[0] - 0.1, 1.3, 0], [BX + 1.7 * BS, 1.3, 0], RNA, 3)
        self.at("concentrated in the same")
        self.play(FadeIn(shade), Create(ld), run_time=1.2)
        self.at("same band")
        self.play(Indicate(shade, color=RNA, scale_factor=1.06), run_time=0.8)
        self.finish()


def s09_final():
    dl, cl, hl = big_state()
    shade = place(shade_rel(), BX, BY, BS)
    gb = T("Burden's group", 30, TEXT).move_to([5.2, 2.5, 0])
    sch2 = schem_label((5.2, 3.5), 26)
    rl = T("receptor RNA", 32, RNA, weight=BOLD).move_to([5.2, 1.3, 0])
    ld = leader([rl.get_left()[0] - 0.1, 1.3, 0], [BX + 1.7 * BS, 1.3, 0], RNA, 3)
    return dl, shade, cl, hl, gb, sch2, rl, ld


class S10Name(SpokenScene):
    def construct(self):
        dl, shade, cl, hl, gb, sch2, rl, ld = s09_final()
        self.add(dl, shade, cl, hl, gb, sch2, rl, ld)
        out = place(outline_rel(), BX, BY, BS)
        lab = T("prepattern", 40, PREPAT, weight=BOLD).move_to([5.1, 0.0, 0])
        pa = arr([lab.get_left()[0] - 0.15, 0.0, 0], [out.get_right()[0] + 0.12, 0.0, 0], PREPAT, w=6)
        self.at("rough map")
        self.play(FadeOut(gb), FadeOut(rl), FadeOut(ld), Create(out), run_time=1.5)
        self.at("called the")
        self.play(FadeIn(lab, shift=LEFT * 0.2), GrowArrow(pa), run_time=0.8)
        self.at("pattern")
        self.play(Indicate(lab, color=PREPAT, scale_factor=1.15), run_time=0.8)
        self.finish()


def s10_final():
    dl, shade, cl, hl, gb, sch2, rl, ld = s09_final()
    out = place(outline_rel(), BX, BY, BS)
    lab = T("prepattern", 40, PREPAT, weight=BOLD).move_to([5.1, 0.0, 0])
    pa = arr([lab.get_left()[0] - 0.15, 0.0, 0], [out.get_right()[0] + 0.12, 0.0, 0], PREPAT, w=6)
    return dl, shade, cl, hl, sch2, out, lab, pa


# ---------------------------------------------------------------------------------------------
class S11Q(SpokenScene):
    def construct(self):
        dl, shade, cl, hl, sch2, out, lab, pa = s10_final()
        self.add(dl, shade, cl, hl, sch2, out, lab, pa)
        # shrink the diaphragm to the right-hand slot (it will hold each case)
        c0 = np.array([BX, BY, 0])
        k = TDS / BS
        sh = np.array([TDX - BX, TDY - BY, 0])
        mv = [m.animate.scale(k, about_point=c0).shift(sh) for m in (dl, shade, cl, out)]
        hp = head("prepattern", PREPAT, TDX, y=HY, size=32)
        tf = table_frame()
        self.at("does the pattern need")
        self.play(*mv, FadeOut(hl), FadeOut(pa), FadeOut(sch2), ReplacementTransform(lab, hp), FadeIn(tf), run_time=1.2)
        labels = [row_label(i) for i in range(4)]
        res = [row_result(0, True)] + [row_result(i, False) for i in (1, 2, 3)]
        self.at("remove one part")
        for i in range(4):
            self.play(FadeIn(labels[i], shift=RIGHT * 0.2), FadeIn(res[i], scale=0.8), run_time=0.45)
            self.wait(0.15)
        self.finish()


def band_case(tag):
    """the band, its RNA-style shading and the gold outline, placed in the table diaphragm"""
    return place(wide_band_rel(3), TDX, TDY, TDS), place(shade_rel(), TDX, TDY, TDS), place(outline_rel(), TDX, TDY, TDS)


class S12Agrin(SpokenScene):
    def construct(self):
        # carried: prepattern diaphragm + table with first row filled
        e = table_ellipse()
        band0, shade0, out0 = band_case("a")
        hp = head("prepattern", PREPAT, TDX, y=HY, size=32)
        tf = table_frame()
        labels = [row_label(i) for i in range(4)]
        res = [row_result(0, True)] + [row_result(i, False) for i in (1, 2, 3)]
        self.add(e, shade0, band0, out0, hp, tf, *labels, *res)
        box = row_box(1, AGRIN)
        h2 = head("no agrin", AGRIN, TDX, y=HY, size=32)
        band, shade, out = band_case("b")
        early = below("early band", PREPAT)
        self.at("lacking")
        # clear the old answer in the same beat as the new case label
        self.play(Create(box), FadeOut(shade0), FadeOut(band0), FadeOut(out0), FadeTransform(hp, h2), run_time=0.7)
        self.at("still build the early band")
        self.play(FadeIn(shade), LaggedStart(*[FadeIn(c, scale=0.3) for c in band], lag_ratio=0.05), run_time=1.3)
        newres = row_result(1, True)
        self.play(Create(out), FadeIn(early), ReplacementTransform(res[1], newres), run_time=0.8)
        self.at("signal is not needed")
        self.play(Indicate(newres, color=BLUE, scale_factor=1.2), run_time=0.9)
        self.finish()


class S13Musk(SpokenScene):
    def construct(self):
        e = table_ellipse()
        band, shade, out = band_case("b")
        early = below("early band", PREPAT)
        h2 = head("no agrin", AGRIN, TDX, y=HY, size=32)
        tf = table_frame()
        labels = [row_label(i) for i in range(4)]
        res = [row_result(0, True), row_result(1, True), row_result(2, False), row_result(3, False)]
        box = row_box(1, AGRIN)
        self.add(e, shade, band, out, early, h2, tf, *labels, *res, box)
        box3 = row_box(2, MUSK)
        h3 = head("no MuSK", MUSK, TDX, y=HY, size=32)
        dots = place(scatter_rel(1), TDX, TDY, TDS)
        cap = below("receptors, evenly spread")
        self.at("lacking")
        # clear the old answer in the same beat as the new case
        self.play(FadeOut(box), FadeOut(band), FadeOut(shade), FadeOut(out),
                  ReplacementTransform(box.copy(), box3), FadeTransform(h2, h3), FadeOut(early), run_time=0.6)
        self.at("make receptors")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.03), FadeIn(cap), run_time=1.1)
        nb = row_result(2, True)
        self.at("but no band")
        self.play(ReplacementTransform(res[2], nb), run_time=0.5)
        self.at("own kinase")
        self.play(Indicate(box3, color=MUSK, scale_factor=1.03), run_time=0.8)
        self.at("needed for the band")
        self.play(Indicate(nb, color=RED, scale_factor=1.2), run_time=0.8)
        self.finish()


class S14Rapsyn(SpokenScene):
    def construct(self):
        e = table_ellipse()
        dots = place(scatter_rel(1), TDX, TDY, TDS)
        h3 = head("no MuSK", MUSK, TDX, y=HY, size=32)
        tf = table_frame()
        labels = [row_label(i) for i in range(4)]
        res = [row_result(0, True), row_result(1, True), row_result(2, True), row_result(3, False)]
        box3 = row_box(2, MUSK)
        cap3 = below("receptors, evenly spread")
        self.add(e, dots, h3, tf, *labels, *res, box3, cap3)
        box4 = row_box(3, RAPSYN)
        h4 = head("no rapsyn", RAPSYN, TDX, y=HY, size=32)
        dots2 = place(scatter_rel(7, 0.075), TDX, TDY, TDS)
        cap4 = below("receptors made, not gathered")
        # receptors stay on screen the whole time: the old scatter is swapped for the new case at once
        self.play(ReplacementTransform(box3, box4), FadeTransform(h3, h4), FadeOut(dots), FadeIn(dots2),
                  FadeTransform(cap3, cap4), run_time=0.5)
        nb = row_result(3, True)
        self.at("there is no band")
        self.play(ReplacementTransform(res[3], nb), run_time=0.5)
        self.at("clusters either")
        self.play(Indicate(nb, color=RED, scale_factor=1.2), Indicate(dots2, color=RECEPTOR, scale_factor=1.02),
                  run_time=0.6)
        self.finish()


def full_table_state():
    tf = table_frame()
    labels = [row_label(i) for i in range(4)]
    res = [row_result(i, True) for i in range(4)]
    return tf, labels, res


CARD_C = (5.1, -0.35)
CARD_W, CARD_H = 3.25, 2.7


def prop_card():
    card = RoundedRectangle(corner_radius=0.25, width=CARD_W, height=CARD_H, stroke_color=PREPAT, stroke_width=5,
                            fill_color=PREPAT, fill_opacity=0.1).move_to([CARD_C[0], CARD_C[1], 0])
    t1 = T("The muscle", 40, TEXT, font=TITLE_FONT)
    t2 = T("proposes.", 40, PREPAT, font=TITLE_FONT)
    VGroup(t1, t2).arrange(DOWN, buff=0.25).move_to(card)
    return card, t1, t2


def brace_labels(rows, color, l1, l2):
    bx = VGroup(*[row_box(i, color) for i in rows])
    b = Brace(bx, direction=RIGHT, color=color, buff=0.08)
    lab = VGroup(T(l1, 28, TEXT), T(l2, 28, TEXT)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    lab.next_to(b, RIGHT, buff=0.2)
    return b, lab


class S15Proposes(SpokenScene):
    def construct(self):
        e = table_ellipse()
        dots2 = place(scatter_rel(7, 0.075), TDX, TDY, TDS)
        h4 = head("no rapsyn", RAPSYN, TDX, y=HY, size=32)
        tf, labels, res = full_table_state()
        box4 = row_box(3, RAPSYN)
        cap4 = below("receptors made, not gathered")
        self.add(e, dots2, h4, tf, *labels, *res, box4, cap4)
        bx = [row_box(2, PREPAT), row_box(3, PREPAT)]
        b1, l1 = brace_labels((2, 3), PREPAT, "muscle's own", "machinery")
        b2, l2 = brace_labels((0, 1), GREY, "nerve's signal", "not needed")
        card, t1, t2 = prop_card()
        self.at("own machinery")
        self.play(FadeOut(e), FadeOut(dots2), FadeOut(h4), FadeOut(cap4), ReplacementTransform(box4, bx[1]),
                  Create(bx[0]), GrowFromCenter(b1), FadeIn(l1, shift=LEFT * 0.2), run_time=0.7)
        # the guiding idea arrives with the muscle's machinery and stays up for the rest of the scene
        self.play(FadeIn(card, scale=0.9), FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.at("to start the band")
        self.play(Indicate(VGroup(*bx), color=PREPAT, scale_factor=1.02), run_time=0.8)
        self.at("nerve signal is not")
        self.play(GrowFromCenter(b2), FadeIn(l2, shift=LEFT * 0.2), run_time=0.8)
        self.at("the muscle proposes")
        self.play(Write(t2), run_time=0.9)
        self.play(Indicate(t2, color=PREPAT, scale_factor=1.12), run_time=0.6)
        self.finish()


def s15_final():
    tf, labels, res = full_table_state()
    bx = [row_box(2, PREPAT), row_box(3, PREPAT)]
    b1, l1 = brace_labels((2, 3), PREPAT, "muscle's own", "machinery")
    b2, l2 = brace_labels((0, 1), GREY, "nerve's signal", "not needed")
    card, t1, t2 = prop_card()
    return tf, labels, res, bx, [b1, l1, b2, l2], card, t1, t2


# ---------------------------------------------------------------------------------------------
class S16Still(SpokenScene):
    def construct(self):
        tf, labels, res, bx, braces, card, t1, t2 = s15_final()
        self.add(tf, *labels, *res, *bx, *braces, card, t1, t2)
        dl = place(ellipse_rel(), LX, EY)
        dr = place(ellipse_rel(), RX, EY)
        term = place(terminal_rel(), RX, EY)
        tl = terminal_label(RX, EY)
        hl = head("no motor axons", NERVE, LX)
        hr = head("normal", TEXT, RX)
        cl = place(wide_band_rel(), LX, EY)
        cr = place(narrow_band_rel(), RX, EY)
        sch = schem_label()
        # the guiding-idea card stays up through the opening words, then the two diaphragms replace the table.
        # The no-axon side already carries its band (from s08), so it is never shown empty.
        self.wait(0.7)
        self.play(FadeOut(tf), *[FadeOut(m) for m in labels + res + bx + braces], FadeOut(card), FadeOut(t1),
                  FadeOut(t2), FadeIn(dl), FadeIn(dr), FadeIn(hl), FadeIn(hr), FadeIn(sch),
                  FadeIn(cl), run_time=0.9)
        self.play(FadeIn(term), FadeIn(tl), run_time=0.5)
        self.play(Indicate(term[0], color=NERVE, scale_factor=1.03), run_time=0.5)
        self.at("contact makes far more clustering")
        self.play(LaggedStart(*[FadeIn(c, scale=0.3) for c in cr], lag_ratio=0.02), run_time=1.4)
        self.at("narrows the band")
        ob = place(outline_narrow(), RX, EY)
        nlb = T("narrower band", 28, PREPAT).move_to([RX, -3.5, 0])
        self.add(nlb)
        self.play(Create(ob), run_time=0.9)
        self.at("without a nerve")
        self.play(Indicate(cl, color=RECEPTOR, scale_factor=1.05), run_time=0.8)
        self.at("the band was wider")
        ow = place(outline_rel(), LX, EY)
        wlb = T("wider band", 28, PREPAT).move_to([LX, -3.5, 0])
        self.add(wlb)
        self.play(Create(ow), run_time=0.9)
        nt = T("clusters under no terminal", 28, RED).move_to([LX, -3.5, 0])
        self.at("to no terminal")
        self.play(FadeOut(wlb), FadeIn(nt, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S17Apart(SpokenScene):
    def construct(self):
        cards = []
        for y in (1.6, -1.6):
            cards.append(RoundedRectangle(corner_radius=0.25, width=12.4, height=2.8, stroke_color=GREY, stroke_width=3,
                                          fill_color=GREY, fill_opacity=0.08).move_to([0, y, 0]))
        t1 = T("Clusters can form without a nerve", 40, TEXT)
        t2 = T("A synapse can form without a nerve", 40, TEXT)
        fit(t1, max_w=7.6)
        fit(t2, max_w=7.6)
        t1.move_to([-0.6, 1.6, 0])
        t2.move_to([-0.6, -1.6, 0])
        ic1 = cluster(-5.5, 1.55, 1.9)
        ic2 = VGroup(RoundedRectangle(corner_radius=0.2, width=0.9, height=1.2, stroke_color=NERVE, stroke_width=3,
                                      fill_color=NERVE, fill_opacity=0.25),
                     cluster(0, 0, 0.9)).move_to([-5.5, -1.6, 0])
        v1 = T("true", 46, BLUE, weight=BOLD).move_to([5.1, 1.6, 0])
        v2 = T("false", 46, RED, weight=BOLD).move_to([5.1, -1.6, 0])
        hd = T("two statements", 28, LG).move_to([0, 3.5, 0])
        self.at("keep two statements apart")
        self.play(FadeIn(cards[0]), FadeIn(cards[1]), FadeIn(hd), FadeIn(t1, shift=RIGHT * 0.2),
                  FadeIn(t2, shift=RIGHT * 0.2), run_time=0.9)
        self.at("clusters can form")
        self.play(FadeIn(ic1, scale=0.5), FadeIn(v1, scale=0.8),
                  cards[0].animate.set_stroke(BLUE, 4), run_time=0.5)
        self.at("a synapse", lead=0)
        self.play(FadeIn(ic2, scale=0.5), FadeIn(v2, scale=0.8), cards[1].animate.set_stroke(RED, 4),
                  Create(Line(t2.get_left() + LEFT * 0.1, t2.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)),
                  run_time=0.35)
        # Actual aligned speech starts at 4.88 s; retain the completed verdict for two seconds.
        self.wait(2.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S18Take(SpokenScene):
    def construct(self):
        cx, cy = 3.4, -0.1
        dia = place(ellipse_rel(), cx, cy, 1.0)
        band = place(wide_band_rel(), cx, cy, 1.0)
        out = place(outline_rel(), cx, cy, 1.0)
        L = -6.4
        tk = T("Takeaway", 28, LG).align_to([L, 0, 0], LEFT).set_y(3.0)
        m1 = T("The muscle draws", 40, TEXT, font=TITLE_FONT).align_to([L, 0, 0], LEFT).set_y(1.6)
        m2 = T("a rough map.", 40, PREPAT, font=TITLE_FONT).align_to([L, 0, 0], LEFT).set_y(0.9)
        n1 = T("The nerve's work", 40, TEXT, font=TITLE_FONT).align_to([L, 0, 0], LEFT).set_y(-0.6)
        n2 = T("is to edit it.", 40, NERVE, font=TITLE_FONT).align_to([L, 0, 0], LEFT).set_y(-1.3)
        tag = T("The muscle proposes. The nerve disposes.", 28, PREPAT).align_to([L, 0, 0], LEFT).set_y(-3.1)
        self.at("takeaway")
        self.play(FadeIn(tk), FadeIn(dia), run_time=0.6)
        self.at("the muscle draws")
        self.play(FadeIn(m1, shift=RIGHT * 0.2), LaggedStart(*[FadeIn(c, scale=0.3) for c in band], lag_ratio=0.04),
                  run_time=0.9)
        self.at("rough map")
        self.play(FadeIn(m2, shift=RIGHT * 0.2), Create(out), run_time=0.9)
        # the nerve edits: terminal arrives, band narrows
        term = place(terminal_rel(), cx, cy, 1.0)
        narrow = place(narrow_band_rel(), cx, cy, 1.0)
        self.at("the nerve's work")
        self.play(FadeIn(n1, shift=RIGHT * 0.2), FadeIn(term), run_time=0.9)
        self.at("to edit it")
        self.play(FadeIn(n2, shift=RIGHT * 0.2), FadeOut(band), FadeOut(out),
                  LaggedStart(*[FadeIn(c, scale=0.3) for c in narrow], lag_ratio=0.02), run_time=1.3)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S19End(EndCard):
    LINE = "The muscle draws a rough map by itself; the nerve edits it."
