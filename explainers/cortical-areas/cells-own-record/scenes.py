"""Mapping the Cortex: Areas and Arealization, chapter 4: The Cells' Own Record  (Biochemistrypedia chaptered film)

The cortex map is drawn as a bar seen from above: front on the LEFT, back on the RIGHT (the same convention as the
lesson's earlier film). Chapter 4 reads the cell's own record (four transcription factors), then runs the two tests
(remove the factor, add more) and builds a table of the results.

Fix round: the map is now a tall block (stage 1, h=3.6) in the test scenes; in the table scenes the table sits in a band
at the top, the map at the left below it, and an evidence panel (year, group, plot) at the right below it.

COLOR MAP (one color per concept, whole chapter series; same as chapters 1 to 3)
  PURPLE = motor area
  GREEN  = somatosensory (touch) area
  PINK   = visual area
  SAND   = auditory area (not drawn in this chapter)
  ORANGE = Emx2
  BLUE   = Pax6
  COUP   = COUP-TFI (periwinkle, new in this chapter)
  SP8    = Sp8 (lime, new in this chapter)
  YELLOW = the lamp / FGF8, the signal from the front edge
  TEAL   = neurons (not drawn in this chapter)
  TEXT   = thalamus and thalamic axons (the input); also names and the main text
  RED    = a factor removed / blocked / the loss test
  GOLD   = years, and the one highlight of the table
  GREY   = the sheet, progenitors, labels, de-emphasised things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58BB5"
COUP = "#9AA5FF"
SP8 = "#C9F27A"
NUC = "#3C4A63"
PALE = "#C9CFDB"
AREA_COL = [PURPLE, GREEN, PINK]
AREA_NAME = ["motor", "touch", "vision"]
WT = (0.38, 0.70)               # borders of the normal map, as fractions front to back
FAC = [("Emx2", ORANGE), ("Pax6", BLUE), ("COUP-TFI", COUP), ("Sp8", SP8)]
BACK_B = (0.52, 0.86)           # borders after Emx2 loss
FWD_B = (0.28, 0.58)            # borders after Emx2 gain / Pax6 loss
COUP_B = (0.62, 0.80)           # borders after COUP-TFI loss

# stages of the map
STG1 = dict(x0=-5.0, w=10.0, cy=0.15, h=3.6)     # test scenes (s09 to s19)
STG2 = dict(x0=-5.7, w=6.2, cy=-1.95, h=3.2)     # beneath the table (s20 to s27)
STG3 = dict(x0=-5.7, w=6.2, cy=-0.9, h=1.5)    # s25, with the marker band above and the thalamus below


# ---------------------------------------------------------------------------------------------
# small helpers
def emx(f, k=0.55):
    return 0.05 + k * f


def pax(f, k=0.55):
    return 0.05 + k * (1 - f)


def glow(x, y, r=0.34, dim=1.0):
    g = VGroup()
    for k, o in ((2.6, 0.08), (1.9, 0.14), (1.35, 0.25)):
        g.add(Circle(radius=r * k, stroke_width=0, fill_color=YELLOW, fill_opacity=o * dim))
    g.add(Circle(radius=r, stroke_color=YELLOW, stroke_width=3, stroke_opacity=max(0.3, dim),
                 fill_color=YELLOW, fill_opacity=0.95 * dim))
    return g.move_to([x, y, 0])


def mk_map(b=WT, st=STG1, size=26, op=0.4, labels=True, pred=False):
    """three area blocks. Each block is a group (filled rectangle, dashed overlay) so that a solid map and a dashed
    'prediction' map are the same kind of object and can transform into each other."""
    x0, w, cy, h = st["x0"], st["w"], st["cy"], st["h"]
    xs = [x0, x0 + b[0] * w, x0 + b[1] * w, x0 + w]
    blocks, labs = VGroup(), VGroup()
    for i in range(3):
        bw = xs[i + 1] - xs[i]
        c = [(xs[i] + xs[i + 1]) / 2, cy, 0]
        r = Rectangle(width=bw, height=h, stroke_color=AREA_COL[i], stroke_width=0 if pred else 3,
                      fill_color=AREA_COL[i], fill_opacity=0.12 if pred else op).move_to(c)
        d = DashedVMobject(Rectangle(width=bw, height=h, stroke_color=AREA_COL[i], stroke_width=4).move_to(c),
                           num_dashes=28, dashed_ratio=0.55, color=AREA_COL[i])
        d.set_stroke(color=AREA_COL[i], width=4, opacity=1.0 if pred else 0.0)
        blocks.add(VGroup(r, d))
        t = T(AREA_NAME[i] if labels else "", size, TEXT)
        if labels and t.width > bw - 0.2:
            t.scale((bw - 0.2) / t.width)
        t.move_to(c)
        labs.add(t)
    return VGroup(blocks, labs)


def centers(b, st):
    xs = [st["x0"], st["x0"] + b[0] * st["w"], st["x0"] + b[1] * st["w"], st["x0"] + st["w"]]
    return [(xs[i] + xs[i + 1]) / 2 for i in range(3)]


def fb_labels(st):
    off = 0.82 if st["w"] > 9 else 0.62
    return VGroup(T("front", 26, GREY).move_to([st["x0"] - off, st["cy"], 0]),
                  T("back", 26, GREY).move_to([st["x0"] + st["w"] + off - 0.04, st["cy"], 0]))


def ghost(st, b=WT, ext=0.28, top=True, bottom=True):
    """short dashed ticks outside the map at the normal border positions (they never cross a label)."""
    g = VGroup()
    for bb in b:
        x = st["x0"] + bb * st["w"]
        for sgn, on in ((1, top), (-1, bottom)):
            if on:
                y0 = st["cy"] + sgn * (st["h"] / 2 + 0.03)
                y1 = st["cy"] + sgn * (st["h"] / 2 + ext)
                g.add(DashedLine([x, y0, 0], [x, y1, 0], dash_length=0.09, stroke_color=GREY, stroke_width=4))
    return g


def ol_label(text):
    return T(text, 26, TEXT).move_to([0, -2.2, 0]).align_to([6.7, 0, 0], RIGHT)


def outline(st, pad=0.14):
    return DashedVMobject(Rectangle(width=st["w"] + 2 * pad, height=st["h"] + 2 * pad, stroke_color=TEXT, stroke_width=3)
                          .move_to([st["x0"] + st["w"] / 2, st["cy"], 0]), num_dashes=70)


def bchip(text, color, size=26, pad=0.2):
    c = chip(text, color, size, pad)
    c[0].set_fill(BG, opacity=0.92)
    return c


def box(w, h, cx, cy, color=GREY, fo=0.1, sw=3, r=0.2):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fo).move_to([cx, cy, 0])


def lab(text, x, y, size=26, color=GREY, **kw):
    return T(text, size, color, **kw).move_to([x, y, 0])


def tag(text, x, y, color, size=28):
    return lab(text, x, y, size, color, weight=BOLD)


def strips(fn, color, cy, h, x0, w, n=28, mult=1.0):
    g = VGroup()
    for i in range(n):
        f = (i + 0.5) / n
        g.add(Rectangle(width=w / n + 0.01, height=h, stroke_width=0, fill_color=color,
                        fill_opacity=mult * float(min(1.0, fn(f) / 0.6 * 0.9))).move_to([x0 + f * w, cy, 0]))
    return g


def axes_xy(x0, w, base, H, extra=0.3):
    return VGroup(Line([x0, base, 0], [x0 + w + 0.2, base, 0], stroke_color=GREY, stroke_width=3),
                  Line([x0, base, 0], [x0, base + H + extra, 0], stroke_color=GREY, stroke_width=3))


def curve(fn, color, x0, w, base, H, lift=0.0, sw=6, n=48, mult=1.0):
    pts = [[x0 + f * w, base + mult * fn(f) / 0.6 * H + lift, 0] for f in np.linspace(0, 1, n)]
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_as_corners(pts)
    return m


def dashed(m, n=34):
    return DashedVMobject(m, num_dashes=n)


def fade_all(scene, *mobs, run_time=0.4, **kw):
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time, **kw)


# the big plot of s03, s04, s05, s09, s14
BP = dict(x0=-4.6, w=9.2, base=-2.55, H=4.9)


def big_axes():
    ax = axes_xy(BP["x0"], BP["w"], BP["base"], BP["H"])
    arrow = Arrow([-3.0, -3.1, 0], [3.0, -3.1, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
    fr = lab("front", -4.0, -3.1, 26, GREY)
    bk = lab("back", 4.0, -3.1, 26, GREY)
    lv = lab("level", -5.2, -0.4, 26, GREY).rotate(PI / 2)
    return VGroup(ax, arrow, fr, bk, lv)


def big_curve(fn, color, H=None, lift=0.0, sw=7):
    return curve(fn, color, BP["x0"], BP["w"], BP["base"], BP["H"] if H is None else H, lift=lift, sw=sw)


# ---- the stage-1 test scenes ------------------------------------------------------------------
def top_chip(text, color):
    return bchip(text, color, 32).move_to([0, 3.3, 0])


def q_lines():
    return VGroup(lab("Which way do the borders move?", 0, -2.5, 36, TEXT), lab("Which areas grow?", 0, -3.2, 36, TEXT))


def size_tags(b, st, which, y=None):
    """'bigger' / 'smaller' tags above the map blocks. which = {block index: 'bigger' | 'smaller'}"""
    cs = centers(b, st)
    y = st["cy"] + st["h"] / 2 + 0.55 if y is None else y
    g = VGroup()
    for i, w in which.items():
        g.add(tag(w, cs[i], y, AREA_COL[i], 30))
    return g


def cite_block(year, lines, sizes=None, col_x=(-4.9, -3.5, -3.1), rows=(-2.6, -3.1, -3.6)):
    """year at the left, a rule, and the names in a column: one block, one alignment."""
    n = len(lines)
    ys = rows[:n]
    yc = sum(ys) / n
    yr = lab(year, col_x[0], yc, 56, GOLD, weight=BOLD)
    rule = Line([col_x[1], ys[0] + 0.25, 0], [col_x[1], ys[-1] - 0.25, 0], stroke_color=GOLD, stroke_width=3)
    names = []
    for i, ln in enumerate(lines):
        sz = (sizes or [32] * n)[i]
        names.append(lab(ln, col_x[2], ys[i], sz, TEXT if i < 2 or n == 2 else PALE).align_to([col_x[2], 0, 0], LEFT))
    return yr, rule, names


# ---- the table ------------------------------------------------------------------------------
TX = [-5.55, -2.5, 1.5, 5.0]
TROWY = [2.735, 1.805, 0.875]
TH_Y = 3.58
ROWS = [("Emx2", ORANGE), ("COUP-TFI", COUP), ("Pax6", BLUE)]
TXT = {(0, 1): "borders move back", (0, 2): "borders move forward", (0, 3): "opposite shifts",
       (1, 1): "motor spreads,\nsensory squeezed", (1, 2): "not covered here", (1, 3): "loss result only",
       (2, 1): "markers shift", (2, 2): "map barely moved", (2, 3): "role unsettled"}


def tbl_lines(nrows=3):
    g = VGroup()
    for y, op in ((3.2, 0.9), (2.27, 0.4), (1.34, 0.4), (0.41, 0.4))[:nrows + 1]:
        g.add(Line([-6.7, y, 0], [6.7, y, 0], stroke_color=GREY, stroke_width=2.5, stroke_opacity=op))
    for x in (-4.45, -0.45, 3.45):
        g.add(Line([x, 3.78, 0], [x, 3.2 - 0.93 * nrows, 0], stroke_color=GREY, stroke_width=2, stroke_opacity=0.35))
    return g


def tbl_head():
    return VGroup(*[T(txt, 28, TEXT, weight=BOLD).move_to([x, TH_Y, 0]) for x, txt in zip(TX, ("factor", "lose it", "raise it", "verdict"))])


def tbl_label(i):
    name, col = ROWS[i]
    return chip(name, col, 26, 0.14).move_to([TX[0], TROWY[i], 0])


def tbl_cell(i, j, text=None, color=TEXT, size=26):
    txt = text if text is not None else TXT[(i, j)]
    if "\n" in txt:
        size = min(size, 22)       # two-line cells: smaller, so they have padding inside the row
    cell = T(txt, size, color, line_spacing=0.25)
    # Compact line spacing preserves 22-point type and at least 0.155 units of row padding.
    if cell.height > 0.62:
        cell.scale_to_fit_height(0.62)
    return cell.move_to([TX[j], TROWY[i], 0])


def row_hl(i, color=GOLD):
    return RoundedRectangle(corner_radius=0.12, width=13.3, height=0.88, stroke_color=color, stroke_width=4,
                            fill_opacity=0).move_to([0, TROWY[i], 0])


def cell_hl(i, j, color=GOLD, w=3.8):
    return RoundedRectangle(corner_radius=0.1, width=w, height=0.88, stroke_color=color, stroke_width=4,
                            fill_opacity=0).move_to([TX[j], TROWY[i], 0])


def tbl_carry(rows=(), cells=None):
    """frame (lines and header), labels for `rows`, and the cells in `cells` ({(i, j): text or None for the default})."""
    out = [tbl_lines(max(rows, default=0) + 1), tbl_head()] + [tbl_label(i) for i in rows]
    for (i, j), t in (cells or {}).items():
        out.append(tbl_cell(i, j, t))
    return out


# =============================================================================================
class S00Title(TitleCard):
    LESSON = "Mapping the Cortex: Areas and Arealization"
    TITLE = "The Cells' Own Record"


# ---------------------------------------------------------------------------------------------
SH = dict(x0=-4.2, w=10.0, cy=-0.6, h=3.2)


def sheet_bar():
    return Rectangle(width=SH["w"], height=SH["h"], stroke_color=GREY, stroke_width=3, fill_color=GREY,
                     fill_opacity=0.18).move_to([SH["x0"] + SH["w"] / 2, SH["cy"], 0])


SMALL_P = [(-3.5, -0.1), (-3.0, -1.5), (-1.7, 0.3), (-1.5, -1.2), (3.0, -0.1), (2.9, -1.45), (4.4, 0.35), (4.5, -1.2), (5.2, -0.55)]


def small_cells():
    g = VGroup()
    for x, y in SMALL_P:
        g.add(Circle(radius=0.34, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.3).move_to([x, y, 0]))
    return g


BIG_C = (0.8, -0.6)


def big_cell(r=1.1):
    cell = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.3).move_to([BIG_C[0], BIG_C[1], 0])
    n1 = Circle(radius=r * 0.42, stroke_color=TEXT, stroke_width=3, fill_color=NUC, fill_opacity=0.95).move_to([BIG_C[0], BIG_C[1], 0])
    n2 = Circle(radius=r * 0.12, stroke_width=0, fill_color="#7C8CAD", fill_opacity=0.95).move_to([BIG_C[0] + r * 0.1, BIG_C[1] + r * 0.08, 0])
    return cell, VGroup(n1, n2)


def front_back_sheet():
    return VGroup(lab("front", SH["x0"] + 0.5, 1.5, 26), lab("back", SH["x0"] + SH["w"] - 0.5, 1.5, 26))


def lamp_state():
    return glow(-5.55, SH["cy"], 0.4), lab("the lamp", -5.55, 0.15, 26, YELLOW)


Q1 = "How does each cell record where it sits?"


class S01(SpokenScene):
    """The sheet with its lamp outside; one progenitor grows to show its nucleus; the question."""

    def construct(self):
        sh = sheet_bar()
        cells = small_cells()
        fb = front_back_sheet()
        self.play(FadeIn(sh), FadeIn(cells, lag_ratio=0.05), FadeIn(fb), run_time=0.35)
        lamp, lamp_l = lamp_state()
        self.at("lamp")
        self.play(FadeIn(lamp, scale=0.5), FadeIn(lamp_l), run_time=0.4)
        self.at("outside the cells")
        self.play(Indicate(lamp, color=YELLOW, scale_factor=1.15), run_time=1.0)
        cell, nuc = big_cell()
        mid = Circle(radius=0.34, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.3).move_to([BIG_C[0], BIG_C[1], 0])
        self.add(mid)
        q = lab(Q1, 0.3, 2.75, 36, TEXT)
        self.at("How does each cell")
        self.play(ReplacementTransform(mid, cell), FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(nuc, scale=0.5), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
DNA_Y = 0.55
GX = [-0.95, 0.95]
TF_FREE = [(-1.6, -0.5), (1.3, -0.5), (-0.3, -1.0), (-1.1, -1.7), (0.9, -1.75), (1.9, -1.1)]


def nucleus_big():
    n = Circle(radius=2.77, stroke_color=TEXT, stroke_width=4, fill_color=NUC, fill_opacity=0.9)
    n2 = Circle(radius=0.34, stroke_width=0, fill_color="#7C8CAD", fill_opacity=0.9).move_to([-0.2, 2.0, 0]) if False else VGroup()
    return n


def gene_box(x, on):
    b = RoundedRectangle(corner_radius=0.1, width=1.3, height=0.52, stroke_color=TEXT if on else GREY, stroke_width=3,
                         fill_color=TEXT, fill_opacity=0.85 if on else 0.0).move_to([x, DNA_Y + 0.29, 0])
    t = T("gene", 26, BG if on else GREY).move_to(b)
    return VGroup(b, t)


def tf_blob(x, y, color=TEXT, op=0.28):
    return RoundedRectangle(corner_radius=0.22, width=0.78, height=0.5, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


class S02(SpokenScene):
    """Zoom into the nucleus: levels of transcription factors; they switch genes on or off."""

    def construct(self):
        sh = sheet_bar()
        cells = small_cells()
        lamp, lamp_l = lamp_state()
        fb = front_back_sheet()
        cell, nuc = big_cell()
        q = lab(Q1, 0.3, 2.75, 36, TEXT)
        self.add(sh, cells, lamp, lamp_l, fb, cell, nuc, q)
        c = np.array([BIG_C[0], BIG_C[1], 0.0])
        zoom = 2.77 / (1.1 * 0.42)
        self.play(FadeOut(VGroup(sh, cells, lamp, lamp_l, fb, q)),
                  cell.animate.scale(zoom, about_point=c).shift(-c).set_opacity(0),
                  nuc[0].animate.scale(zoom, about_point=c).shift(-c),
                  nuc[1].animate.scale(zoom, about_point=c).shift(-c).set_opacity(0), run_time=1.4)
        self.remove(cell)
        dna = Line([-2.2, DNA_Y, 0], [2.2, DNA_Y, 0], stroke_color=GREY, stroke_width=5)
        dna_l = lab("DNA", -1.95, DNA_Y - 0.42, 26, PALE)
        genes = [gene_box(GX[0], False), gene_box(GX[1], False)]
        self.at("position is recorded")
        self.play(Create(dna), FadeIn(dna_l), *[FadeIn(g, shift=UP * 0.1) for g in genes], run_time=0.9)
        # a level gauge, and the transcription factors, a few at first
        gx = -5.0
        gframe = Rectangle(width=0.55, height=3.2, stroke_color=GREY, stroke_width=3).move_to([gx, -0.1, 0])
        glab = lab("level", gx, 1.9, 28, TEXT)
        gfill = Rectangle(width=0.55, height=0.8, stroke_width=0, fill_color=TEXT, fill_opacity=0.7).move_to([gx, -1.7 + 0.4, 0])
        tfs = [tf_blob(x, y) for x, y in TF_FREE]
        self.at("levels of")
        self.play(FadeIn(gframe), FadeIn(glab), FadeIn(gfill), *[FadeIn(t, scale=0.4) for t in tfs[:2]], run_time=0.5)
        lbl = lab("transcription\nfactors", 4.9, -0.9, 30, TEXT, line_spacing=0.9)
        arr = Arrow([3.6, -0.9, 0], [2.4, -0.9, 0], buff=0.05, color=TEXT, stroke_width=4, tip_length=0.2)
        self.at("transcription factors")
        self.play(FadeIn(lbl, shift=LEFT * 0.15), GrowArrow(arr), run_time=0.5)
        gfill2 = Rectangle(width=0.55, height=3.0, stroke_width=0, fill_color=TEXT, fill_opacity=0.7).move_to([gx, -1.7 + 1.5, 0])
        self.play(LaggedStart(*[FadeIn(t, scale=0.4) for t in tfs[2:]], lag_ratio=0.25),
                  Transform(gfill, gfill2), run_time=1.3)
        self.at("proteins that switch")
        self.play(Indicate(VGroup(*tfs), color=TEXT, scale_factor=1.08), run_time=0.9)
        on_g = gene_box(GX[0], True)
        on_t = tag("on", GX[0], 1.75, TEXT, 32)
        self.at("on or off")
        self.play(tfs[0].animate.move_to([GX[0], DNA_Y - 0.4, 0]).set_fill(opacity=0.7), Transform(genes[0], on_g),
                  FadeIn(on_t), run_time=0.7)
        off_t = tag("off", GX[1], 1.75, GREY, 32)
        lid = Rectangle(width=1.1, height=0.12, stroke_width=0, fill_color=GREY, fill_opacity=0.95).move_to([GX[1], DNA_Y + 0.0, 0])
        self.at("or off")
        self.play(tfs[1].animate.move_to([GX[1], DNA_Y - 0.4, 0]).set_fill(opacity=0.7), FadeIn(lid), FadeIn(off_t), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    """Two ramps in opposite directions across the dorsal map (a plot computed from the ramp equations)."""

    def construct(self):
        axs = big_axes()
        self.play(FadeIn(axs), run_time=0.4)
        c1 = big_curve(emx, TEXT)
        c2 = big_curve(pax, GREY)
        self.at("run in opposite")
        self.play(Create(c1), run_time=0.7)
        self.at("opposite directions")
        self.play(Create(c2), run_time=1.0)
        self.at("front to back axis")
        self.play(Indicate(axs[1], color=TEXT, scale_factor=1.0), Indicate(axs[2], color=TEXT), Indicate(axs[3], color=TEXT),
                  run_time=1.3)
        self.finish()


class S04(SpokenScene):
    """Name the two ramps: Emx2 high at the back, Pax6 high at the front."""

    def construct(self):
        axs = big_axes()
        c1 = big_curve(emx, TEXT)
        c2 = big_curve(pax, GREY)
        self.add(axs, c1, c2)
        ex, ey = BP["x0"] + BP["w"], BP["base"] + emx(1) / 0.6 * BP["H"]
        px_, py = BP["x0"], BP["base"] + pax(0) / 0.6 * BP["H"]
        d1 = Dot([ex, ey, 0], radius=0.17, color=ORANGE)
        d2 = Dot([px_, py, 0], radius=0.17, color=BLUE)
        l1 = lab("Emx2", 3.9, 2.95, 34, ORANGE, weight=BOLD)
        l2 = lab("Pax6", -3.9, 2.95, 34, BLUE, weight=BOLD)
        self.at("is highest at the back", lead=0.6)
        self.play(c1.animate.set_color(ORANGE), FadeIn(l1, shift=DOWN * 0.1), run_time=0.7)
        self.at("highest at the back")
        self.play(FadeIn(d1, scale=0.3), Indicate(d1, color=ORANGE, scale_factor=1.8), run_time=0.9)
        self.at("is highest at the front", lead=0.6)
        self.play(c2.animate.set_color(BLUE), FadeIn(l2, shift=DOWN * 0.1), run_time=0.6)
        self.at("highest at the front")
        self.play(FadeIn(d2, scale=0.3), Indicate(d2, color=BLUE, scale_factor=1.8), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
RC = (1.5, -0.1)     # centre of the 2D sheet in s05, s06
RW, RH_ = 7.8, 4.4
RX0, RY0 = RC[0] - RW / 2, RC[1] - RH_ / 2


def lv4(u, vm):
    """levels of Emx2, Pax6, COUP-TFI and Sp8 at front-to-back position u (0 front, 1 back) and
    lateral-to-medial position vm (0 lateral, 1 medial)."""
    return [u * vm, (1 - u) * (1 - vm), u * (1 - vm), (1 - u) * vm]


def tile_layer(idx, nx=22, ny=11, scale=1.0):
    """tiles tinted by the two factors idx = (a, b); opacity grows with the higher of the two."""
    g = VGroup()
    tw, th = RW / nx, RH_ / ny
    for i in range(nx):
        for j in range(ny):
            u = (i + 0.5) / nx
            vm = (j + 0.5) / ny
            v = lv4(u, vm)
            a, b = idx
            k = a if v[a] >= v[b] else b
            op = scale * 0.85 * max(v[a], v[b]) ** 1.5
            g.add(Rectangle(width=tw + 0.01, height=th + 0.01, stroke_width=0, fill_color=FAC[k][1], fill_opacity=op)
                  .move_to([RX0 + (i + 0.5) * tw, RY0 + (j + 0.5) * th, 0]))
    return g


def rect_sheet():
    return Rectangle(width=RW, height=RH_, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([RC[0], RC[1], 0])


def rect_labels():
    """front / back at the sides of the sheet, and the midline-to-outward arrow with its own label on the far left."""
    return VGroup(lab("front", RX0 - 0.7, RC[1], 26, GREY), lab("back", RX0 + RW + 0.7, RC[1], 26, GREY))


def mid_arrow():
    ar = Arrow([-4.35, 2.0, 0], [-4.35, -2.2, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.22)
    t = lab("midline to\noutward", -5.55, -0.1, 26, TEXT, line_spacing=0.9)
    med = lab("medial", -4.35, 2.5, 26, GREY)
    lat = lab("lateral", -4.35, -2.65, 26, GREY)
    return VGroup(ar, t, med, lat)


CHIP_POS = {"Sp8": (RX0 + 1.0, RY0 + RH_ - 0.5), "Emx2": (RX0 + RW - 1.0, RY0 + RH_ - 0.5),
            "Pax6": (RX0 + 1.1, RY0 + 0.5), "COUP-TFI": (RX0 + RW - 1.2, RY0 + 0.5)}


def fac_chip(name):
    col = dict(FAC)[name]
    return bchip(name, col, 26).move_to([*CHIP_POS[name], 0]).set_z_index(5)


class S05(SpokenScene):
    """From the plot to a 2D sheet: Emx2 and Pax6 vary medial to lateral too, and two more factors join."""

    def construct(self):
        axs = big_axes()
        c1 = big_curve(emx, ORANGE)
        c2 = big_curve(pax, BLUE)
        l1 = lab("Emx2", 3.9, 2.95, 34, ORANGE, weight=BOLD)
        l2 = lab("Pax6", -3.9, 2.95, 34, BLUE, weight=BOLD)
        self.add(axs, c1, c2, l1, l2)
        sheet = rect_sheet()
        rl = rect_labels()
        self.play(FadeOut(VGroup(axs, c1, c2, l1, l2)), FadeIn(sheet), FadeIn(rl), run_time=0.6)
        self.play(FadeIn(fac_chip("Emx2"), scale=0.8), run_time=0.4)
        self.at("from the")
        self.play(FadeIn(fac_chip("Pax6"), scale=0.8), run_time=0.4)
        la = tile_layer((0, 1))
        ma = mid_arrow()
        self.at("midline outward")
        self.play(FadeIn(ma, shift=DOWN * 0.1), FadeIn(la), run_time=1.0)
        lb = tile_layer((2, 3))
        more = lab("two more factors join", RC[0], -2.75, 28, GOLD)
        self.at("two more factors")
        self.play(FadeIn(lb), FadeIn(fac_chip("COUP-TFI"), scale=0.8), FadeIn(more), run_time=0.7)
        self.at("join them")
        self.play(FadeIn(fac_chip("Sp8"), scale=0.8), run_time=0.5)
        self.finish()


CELL_P = [(-1.2, -0.55), (1.6, 1.15), (4.4, -0.55)]
CELL_R = 1.5


def cell_chart(p, r=CELL_R):
    cx, cy = p
    u = (cx - RX0) / RW
    vm = (cy - RY0) / RH_
    vals = lv4(u, vm)
    circ = Circle(radius=r, stroke_color=TEXT, stroke_width=3.5, fill_color=BG, fill_opacity=0.95).move_to([cx, cy, 0])
    base = Line([cx - 0.85, cy - 0.8, 0], [cx + 0.85, cy - 0.8, 0], stroke_color=GREY, stroke_width=2.5)
    bs = VGroup()
    for k, (nm, col) in enumerate(FAC):
        hgt = max(vals[k] * 1.9, 0.03)
        bs.add(Rectangle(width=0.31, height=hgt, stroke_width=0, fill_color=col, fill_opacity=0.95)
               .move_to([cx + (k - 1.5) * 0.41, cy - 0.8 + hgt / 2, 0]))
    return VGroup(circ, base), bs


KEY_Y = -2.5


def key_items():
    items = []
    for nm, col in FAC:
        sw = Square(side_length=0.3, stroke_width=0, fill_color=col, fill_opacity=0.95)
        items.append(VGroup(sw, T(nm, 26, TEXT)).arrange(RIGHT, buff=0.15))
    VGroup(*items).arrange(RIGHT, buff=0.65).move_to([RC[0] + 0.4, KEY_Y, 0])
    return items


class S06(SpokenScene):
    """Each progenitor reads its own mix: a small bar chart of the four levels, different at each position."""

    def construct(self):
        sheet = rect_sheet()
        rl = rect_labels()
        ma = mid_arrow()
        la, lb = tile_layer((0, 1)), tile_layer((2, 3))
        chips = VGroup(*[fac_chip(n) for n, _ in FAC])
        more = lab("two more factors join", RC[0], -2.75, 28, GOLD)
        self.add(sheet, rl, ma, la, lb, chips, more)
        self.at("The levels")
        parts = [cell_chart(p) for p in CELL_P]
        self.play(Transform(la, tile_layer((0, 1), scale=0.35)), Transform(lb, tile_layer((2, 3), scale=0.35)),
                  FadeOut(chips), FadeOut(more),
                  Transform(rl, VGroup(lab("front", RX0, 2.8, 26, GREY), lab("back", RX0 + RW, 2.8, 26, GREY))),
                  *[FadeIn(pt[0], scale=0.5) for pt in parts], run_time=0.5)
        keys = key_items()
        note = lab("bar height = level", RC[0] + 0.4, -3.12, 28, TEXT)
        # Introduce each factor in all three cells with its key, so no cell stays empty.
        for k in range(4):
            self.play(*[GrowFromEdge(pt[1][k], DOWN) for pt in parts], FadeIn(keys[k], shift=UP * 0.1),
                      *([FadeIn(note)] if k == 0 else []), run_time=0.3)
        self.at("progenitor's")
        self.wait(0.8)
        self.at("record of where")
        self.play(*[Indicate(pt[0][0], color=TEXT, scale_factor=1.06) for pt in parts], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s07: the record and the lamp
G_X0, G_W, G_H = -2.6, 5.6, 2.8
G_EM_Y, G_PX_Y = 1.8, -1.6
SHIFT = 0.9


def grad_strip(fn, color, cy):
    g = strips(fn, color, cy, G_H, G_X0, G_W, n=24)
    fr = Rectangle(width=G_W, height=G_H, stroke_color=GREY, stroke_width=2.5).move_to([G_X0 + G_W / 2, cy, 0])
    return VGroup(g, fr)


def grad_ghost(cy):
    return DashedVMobject(Rectangle(width=G_W, height=G_H, stroke_color=GREY, stroke_width=3).move_to([G_X0 + G_W / 2, cy, 0]), num_dashes=60)


LAMP7 = (-5.75, 0.1)


class S07(SpokenScene):
    """The record and the lamp are linked: lamp to both gradients; changing FGF8 shifts both; a dashed, questioned arrow back."""

    def construct(self):
        ea = grad_strip(emx, ORANGE, G_EM_Y)
        pa = grad_strip(pax, BLUE, G_PX_Y)
        l_e = tag("Emx2", 4.6, G_EM_Y, ORANGE, 34)
        l_p = tag("Pax6", 4.6, G_PX_Y, BLUE, 34)
        fb = VGroup(lab("front", G_X0 + 0.5, -3.45, 26), lab("back", G_X0 + G_W - 0.5, -3.45, 26))
        self.at("The record")
        self.play(FadeIn(ea), FadeIn(pa), FadeIn(l_e), FadeIn(l_p), FadeIn(fb), run_time=0.5)
        lamp = glow(*LAMP7, 0.32)
        lamp_l = VGroup(lab("the lamp", LAMP7[0], -0.75, 26, YELLOW), tag("FGF8", LAMP7[0], -1.2, YELLOW, 28))
        self.at("and the lamp")
        self.play(FadeIn(lamp, scale=0.5), FadeIn(lamp_l), run_time=0.5)
        s1 = Arrow([-5.2, 0.5, 0], [-3.75, 1.5, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=0.25)
        s2 = Arrow([-5.2, -0.3, 0], [-3.75, -1.4, 0], buff=0, color=YELLOW, stroke_width=6, tip_length=0.25)
        self.at("are linked")
        self.play(GrowArrow(s1), GrowArrow(s2), run_time=0.8)
        self.at("Changing")
        self.play(Indicate(lamp, color=YELLOW, scale_factor=1.3), run_time=0.9)
        g1, g2 = grad_ghost(G_EM_Y), grad_ghost(G_PX_Y)
        shift_tag = tag("gradients shift", 5.0, 0.1, TEXT, 28)
        self.at("shifts the gradients")
        self.add(g1, g2)
        self.play(ea.animate.shift(LEFT * SHIFT), pa.animate.shift(LEFT * SHIFT), FadeIn(shift_tag), run_time=1.4)
        back = DashedLine([-3.85, 2.4, 0], [-5.45, 0.85, 0], dash_length=0.14, stroke_color=GREY, stroke_width=6)
        back.add_tip(tip_length=0.28)
        q = tag("?", -5.4, 2.2, TEXT, 54)
        self.at("Whether", lead=0.0)
        self.play(Create(back), run_time=0.9)
        self.at("acts back on it")
        self.play(FadeIn(q, scale=0.4), run_time=0.5)
        self.at("still argued")
        self.play(Indicate(q, color=TEXT, scale_factor=1.4), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
CARD_W, CARD_H, CARD_CY = 6.3, 4.8, -0.15
CARD_X = (-3.35, 3.35)


def card_frame(i):
    return box(CARD_W, CARD_H, CARD_X[i], CARD_CY, GREY, 0.08)


def card_strip(i, lifted=False):
    cx = CARD_X[i] - (0.3 if lifted else 0.0)
    w, h = 4.4, 1.5
    st = strips(lambda f: emx(f) + (0.25 if lifted else 0.0), ORANGE, 0.3, h, cx - w / 2, w, n=20)
    fr = Rectangle(width=w, height=h, stroke_color=GREY, stroke_width=2.5).move_to([cx, 0.3, 0])
    return VGroup(st, fr)


def card_x():
    cx = CARD_X[0]
    return VGroup(Line([cx - 2.2, 1.05, 0], [cx + 2.2, -0.45, 0], stroke_color=RED, stroke_width=9),
                  Line([cx - 2.2, -0.45, 0], [cx + 2.2, 1.05, 0], stroke_color=RED, stroke_width=9))


def card_titles():
    return lab("remove the factor", CARD_X[0], 1.7, 34, RED), lab("add more", CARD_X[1], 1.7, 34, TEXT)


def card_caps():
    return tag("Emx2", CARD_X[0], -1.1, ORANGE, 32), tag("more Emx2", CARD_X[1], -1.1, ORANGE, 32)


def card_up():
    return Arrow([CARD_X[1] + 2.55, -0.4, 0], [CARD_X[1] + 2.55, 1.0, 0], buff=0, color=TEXT, stroke_width=8, tip_length=0.3)


def cards_final():
    t1, t2 = card_titles()
    c1, c2 = card_caps()
    return VGroup(card_frame(0), card_frame(1), t1, t2, card_strip(0), card_x(), card_strip(1, True), card_up(), c1, c2)


class S08(SpokenScene):
    """A gradient lines up with the map: only a correlation. So the two tests: remove, add."""

    def construct(self):
        st = strips(emx, ORANGE, 2.7, 1.2, -5.0, 10.0, n=30)
        stf = Rectangle(width=10.0, height=1.2, stroke_color=GREY, stroke_width=2).move_to([0, 2.7, 0])
        sl = tag("Emx2 gradient", -3.2, 3.62, ORANGE, 28)
        stg = dict(x0=-5.0, w=10.0, cy=0.5, h=2.2)
        m = mk_map(WT, stg)
        fb = fb_labels(stg)
        corr = lab("only a correlation", 0, -1.55, 44, GOLD, font=TITLE_FONT)
        self.play(FadeIn(st), FadeIn(stf), FadeIn(sl), run_time=0.6)
        self.play(FadeIn(m), FadeIn(fb), run_time=0.6)
        self.at("only a correlation")
        self.play(FadeIn(corr, shift=UP * 0.12), run_time=0.8)
        self.at("So run both tests")
        a, b = card_frame(0), card_frame(1)
        t1 = lab("test 1", CARD_X[0], 1.7, 34, GREY)
        t2 = lab("test 2", CARD_X[1], 1.7, 34, GREY)
        self.play(FadeOut(VGroup(st, stf, sl, m, fb, corr)), FadeIn(a), FadeIn(b), FadeIn(t1), FadeIn(t2), run_time=0.8)
        T1, T2 = card_titles()
        c1, c2 = card_caps()
        s1 = card_strip(0)
        self.at("remove the factor")
        self.play(Transform(t1, T1), FadeIn(s1), FadeIn(c1), run_time=0.5)
        self.play(Create(card_x()), run_time=0.5)
        s2 = card_strip(1, True)
        self.at("then add more")
        self.play(Transform(t2, T2), FadeIn(s2), FadeIn(c2), run_time=0.5)
        self.play(GrowArrow(card_up()), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s9_end_state():
    return top_chip("no Emx2", RED), mk_map(WT, STG1), fb_labels(STG1), q_lines()


class S09(SpokenScene):
    """Emx2 is highest at the back. Delete it. Which way should the borders move, and which areas should grow?"""

    def construct(self):
        cards = cards_final()
        self.add(cards)
        ax = big_axes()
        cv = big_curve(emx, ORANGE)
        el = lab("Emx2", 3.9, 2.95, 34, ORANGE, weight=BOLD)
        self.play(FadeOut(cards), FadeIn(ax), run_time=0.5)
        self.at("is highest at the back", lead=0.6)
        self.play(Create(cv), FadeIn(el), run_time=0.7)
        dot = Dot([BP["x0"] + BP["w"], BP["base"] + emx(1) / 0.6 * BP["H"], 0], radius=0.17, color=ORANGE)
        self.at("highest at the back")
        self.play(FadeIn(dot, scale=0.3), Indicate(dot, color=ORANGE, scale_factor=1.8), run_time=0.9)
        chip_, m, fb, q = s9_end_state()
        self.at("Delete it")
        self.play(FadeOut(VGroup(ax, cv, el, dot)), run_time=0.5)
        self.play(FadeIn(m), FadeIn(fb), FadeIn(chip_, scale=0.7), run_time=0.8)
        self.at("Which way should the borders move")
        self.play(FadeIn(q[0], shift=UP * 0.1), run_time=0.6)
        self.at("which areas should grow")
        self.play(FadeIn(q[1], shift=UP * 0.1), LaggedStart(*[Indicate(r, color=TEXT, scale_factor=1.03) for r in m[0]], lag_ratio=0.35),
                  run_time=1.3)
        self.finish()


class S10Pause(NarratedScene):
    """The question stays on screen, still."""

    def construct(self):
        chip_, m, fb, q = s9_end_state()
        self.add(chip_, m, fb, q)
        self.finish()


LEG = lambda: lab("dashed ticks: normal borders", 0, -2.35, 26, GREY)


def arrow_row(direction, y=-2.9):
    if direction > 0:
        return Arrow([-2.4, y, 0], [2.4, y, 0], buff=0, color=TEXT, stroke_width=9, tip_length=0.35)
    return Arrow([2.4, y, 0], [-2.4, y, 0], buff=0, color=TEXT, stroke_width=9, tip_length=0.35)


class S11(SpokenScene):
    """Emx2 deleted: the borders move back; front and middle areas grow, visual shrinks."""

    def construct(self):
        chip_, m, fb, q = s9_end_state()
        self.add(chip_, m, fb, q)
        gh = ghost(STG1)
        leg = LEG()
        arr = arrow_row(+1)
        al = lab("the borders move back", 0, -3.5, 32, TEXT)
        self.play(FadeOut(q), FadeIn(gh), FadeIn(leg), run_time=0.4)
        self.play(Transform(m, mk_map(BACK_B, STG1)), GrowArrow(arr), FadeIn(al), run_time=1.5)
        tg1 = size_tags(BACK_B, STG1, {0: "bigger", 1: "bigger"})
        self.at("the front and middle areas grow")
        self.play(FadeIn(tg1, shift=DOWN * 0.1), Indicate(m[0][0], color=PURPLE, scale_factor=1.02),
                  Indicate(m[0][1], color=GREEN, scale_factor=1.02), run_time=1.1)
        tg2 = size_tags(BACK_B, STG1, {2: "smaller"})
        self.at("and the visual area shrinks")
        self.play(FadeIn(tg2, shift=DOWN * 0.1), Indicate(m[0][2], color=PINK, scale_factor=0.92), run_time=1.0)
        self.finish()


def s11_end_state():
    chip_ = top_chip("no Emx2", RED)
    m = mk_map(BACK_B, STG1)
    fb = fb_labels(STG1)
    gh = ghost(STG1)
    tg = size_tags(BACK_B, STG1, {0: "bigger", 1: "bigger", 2: "smaller"})
    return chip_, m, fb, gh, tg


class S12(SpokenScene):
    """Bishop, Goudreau and O'Leary, 2000, in mice lacking Emx2."""

    def construct(self):
        chip_, m, fb, gh, tg = s11_end_state()
        leg = LEG()
        arr = arrow_row(+1)
        al = lab("the borders move back", 0, -3.5, 32, TEXT)
        self.add(chip_, m, fb, gh, tg, leg, arr, al)
        yr, rule, names = cite_block("2000", ["Kathie Bishop", "Guy Goudreau", "Dennis O'Leary"])
        self.at("In 2000")
        self.play(FadeOut(VGroup(arr, al, leg)), FadeIn(yr, shift=UP * 0.1), Create(rule), run_time=0.6)
        self.at("Bishop")
        self.play(FadeIn(names[0], shift=RIGHT * 0.15), run_time=0.5)
        self.at("Guy")
        self.play(FadeIn(names[1], shift=RIGHT * 0.15), run_time=0.5)
        self.at("Dennis")
        self.play(FadeIn(names[2], shift=RIGHT * 0.15), run_time=0.5)
        mice = top_chip("mice lacking Emx2", RED)
        self.at("mice lacking")
        self.play(Transform(chip_, mice), run_time=0.7)
        self.finish()


def s12_end_state():
    chip_ = top_chip("mice lacking Emx2", RED)
    m = mk_map(BACK_B, STG1)
    fb = fb_labels(STG1)
    gh = ghost(STG1)
    tg = size_tags(BACK_B, STG1, {0: "bigger", 1: "bigger", 2: "smaller"})
    yr, rule, names = cite_block("2000", ["Kathie Bishop", "Guy Goudreau", "Dennis O'Leary"])
    return chip_, m, fb, gh, tg, yr, rule, names


class S13(SpokenScene):
    """Without working Pax6 the shift went the other way."""

    def construct(self):
        chip_, m, fb, gh, tg, yr, rule, names = s12_end_state()
        self.add(chip_, m, fb, gh, tg, yr, rule, *names)
        ax = big_axes()
        cv = big_curve(pax, BLUE)
        pl = lab("Pax6", -3.9, 2.95, 34, BLUE, weight=BOLD)
        dot = Dot([BP["x0"], BP["base"] + pax(0) / 0.6 * BP["H"], 0], radius=0.17, color=BLUE)
        # a clean frame, then the Pax6 ramp drawn large
        self.play(FadeOut(VGroup(chip_, m, fb, gh, tg, yr, rule, *names)), run_time=0.25)
        self.play(FadeIn(ax), Create(cv), FadeIn(pl), FadeIn(dot), run_time=0.5)
        # the ramp fades and the map returns with the cause named
        nm = mk_map(WT, STG1)
        nfb = fb_labels(STG1)
        chip2 = top_chip("Pax6 not working", RED)
        self.wait(0.2)
        self.play(FadeOut(VGroup(ax, cv, pl, dot)), run_time=0.25)
        self.play(FadeIn(nm), FadeIn(nfb), FadeIn(chip2, scale=0.7), run_time=0.35)
        self.at("the shift went the other way")
        gh2 = ghost(STG1)
        arr = arrow_row(-1)
        al = lab("the shift goes the other way", 0, -3.5, 32, TEXT)
        self.add(gh2)
        self.play(Transform(nm, mk_map(FWD_B, STG1)), GrowArrow(arr), FadeIn(al), run_time=1.5)
        self.at("Front areas shrank")
        self.play(FadeIn(size_tags(FWD_B, STG1, {0: "smaller"}), shift=DOWN * 0.1), Indicate(nm[0][0], color=PURPLE, scale_factor=0.97),
                  run_time=1.0)
        self.at("visual area grew forward")
        self.play(FadeIn(size_tags(FWD_B, STG1, {2: "bigger"}), shift=DOWN * 0.1), Indicate(nm[0][2], color=PINK, scale_factor=1.03),
                  run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
G_AX = dict(H=4.0, lift=0.75)


def gain_plot():
    """the big Emx2 plot of s14: the normal curve dashed, the raised curve solid and parallel to it."""
    ax = big_axes()
    orig = dashed(big_curve(emx, ORANGE, H=G_AX["H"], sw=5), 40)
    up = big_curve(emx, ORANGE, H=G_AX["H"], lift=G_AX["lift"], sw=7)
    el = lab("Emx2 raised", 3.4, 2.95, 34, ORANGE, weight=BOLD)
    nl = lab("normal Emx2", 4.0, 0.3, 28, ORANGE)
    sl = bchip("same slope", TEXT, 32, 0.12).move_to([-1.7, 0.6, 0])
    return ax, orig, up, el, nl, sl


def s14_end_state():
    chip_ = top_chip("Emx2 raised", ORANGE)
    m = mk_map(WT, STG1)
    fb = fb_labels(STG1)
    ol = outline(STG1)
    ol_l = ol_label("whole cortex")
    q = lab("What would show it allocates territory?", 0, -3.2, 36, TEXT)
    return chip_, m, fb, ol, ol_l, q


class S14(SpokenScene):
    """Raise Emx2 everywhere, keeping its slope; what would show that it allocates territory?"""

    def construct(self):
        chip_, m, fb, gh, tg, yr, rule, names = (top_chip("Pax6 not working", RED), mk_map(FWD_B, STG1), fb_labels(STG1),
                                                 ghost(STG1), size_tags(FWD_B, STG1, {0: "smaller", 2: "bigger"}), None, None, None)
        arr = arrow_row(-1)
        al = lab("the shift goes the other way", 0, -3.5, 32, TEXT)
        self.add(chip_, m, fb, gh, tg, arr, al)
        ax, orig, up, el, nl, sl = gain_plot()
        flat = big_curve(emx, ORANGE, H=G_AX["H"], sw=7)
        self.play(FadeOut(VGroup(chip_, m, fb, gh, tg, arr, al)), FadeIn(ax), FadeIn(flat), run_time=0.5)
        self.at("raise")
        self.add(orig)
        self.play(Transform(flat, up), FadeIn(el), FadeIn(nl), run_time=1.3)
        self.at("keeping its slope")
        self.play(FadeIn(sl), run_time=0.25)
        chip2, m2, fb2, ol, ol_l, q = s14_end_state()
        self.at("What would show", lead=0.0)
        plot_q = q.copy().move_to([0, 3.55, 0])
        self.play(FadeIn(plot_q), run_time=0.35)
        self.wait(0.45)
        self.play(FadeOut(VGroup(ax, orig, flat, el, nl, sl)), FadeIn(chip2, scale=0.8), FadeIn(m2), FadeIn(fb2), Create(ol),
                  FadeIn(ol_l), Transform(plot_q, q), run_time=0.8)
        self.finish()


class S15Pause(NarratedScene):
    """The question stays on screen, still."""

    def construct(self):
        chip_, m, fb, ol, ol_l, q = s14_end_state()
        self.add(chip_, m, fb, ol, ol_l, q)
        self.finish()


EXP_LAB = "expected: whole cortex same size"


def s16_end_state():
    chip_ = top_chip("Emx2 raised", ORANGE)
    m = mk_map(FWD_B, STG1, pred=True)
    fb = fb_labels(STG1)
    ol = outline(STG1)
    ol_l = ol_label(EXP_LAB)
    gh = ghost(STG1)
    return chip_, m, fb, ol, ol_l, gh


class S16(SpokenScene):
    """The map should move the opposite way, with the whole cortex about the same size (a prediction, drawn dashed)."""

    def construct(self):
        chip_, m, fb, ol, ol_l, q = s14_end_state()
        self.add(chip_, m, fb, ol, ol_l, q)
        gh = ghost(STG1)
        arr = arrow_row(-1)
        al = lab("expected: borders move forward", 0, -3.5, 32, TEXT)
        self.play(FadeOut(q), FadeIn(gh), run_time=0.4)
        self.at("opposite way")
        self.play(Transform(m, mk_map(FWD_B, STG1, pred=True)), GrowArrow(arr), FadeIn(al), run_time=1.4)
        self.at("whole cortex")
        self.play(Indicate(ol, color=TEXT, scale_factor=1.0), Transform(ol_l, ol_label(EXP_LAB)), run_time=1.2)
        self.finish()


def s16_full():
    chip_, m, fb, ol, ol_l, gh = s16_end_state()
    arr = arrow_row(-1)
    al = lab("expected: borders move forward", 0, -3.5, 32, TEXT)
    return chip_, m, fb, ol, ol_l, gh, arr, al


class S17(SpokenScene):
    """Hamasaki and colleagues, 2004, from O'Leary's laboratory. The prediction stays still."""

    def construct(self):
        chip_, m, fb, ol, ol_l, gh, arr, al = s16_full()
        self.add(chip_, m, fb, ol, ol_l, gh, arr, al)
        yr, rule, names = cite_block("2004", ["Tadashi Hamasaki", "and colleagues", "in O'Leary's laboratory"], sizes=[32, 32, 30])
        self.at("In 2004")
        self.play(FadeOut(VGroup(arr, al)), FadeIn(yr, shift=UP * 0.1), Create(rule), run_time=0.7)
        self.at("Hamasaki")
        self.play(FadeIn(names[0], shift=RIGHT * 0.15), FadeIn(names[1], shift=RIGHT * 0.15), run_time=0.7)
        self.at("laboratory")
        self.play(FadeIn(names[2], shift=RIGHT * 0.15), run_time=0.6)
        self.finish()


def s17_end_state():
    chip_, m, fb, ol, ol_l, gh = s16_end_state()
    yr, rule, names = cite_block("2004", ["Tadashi Hamasaki", "and colleagues", "in O'Leary's laboratory"], sizes=[32, 32, 30])
    return chip_, m, fb, ol, ol_l, gh, yr, rule, names


class S18(SpokenScene):
    """The visual area grew, the front area shrank, the total did not change: the prediction becomes the finding."""

    def construct(self):
        chip_, m, fb, ol, ol_l, gh, yr, rule, names = s17_end_state()
        self.add(chip_, m, fb, ol, ol_l, gh, yr, rule, *names)
        self.at("The visual area grew", lead=0.0)
        self.play(Transform(m, mk_map(FWD_B, STG1)), Transform(ol_l, ol_label("whole cortex outline")), run_time=0.5)
        self.at("grew")
        self.play(FadeIn(size_tags(FWD_B, STG1, {2: "bigger"}), shift=DOWN * 0.1), Indicate(m[0][2], color=PINK, scale_factor=1.03),
                  run_time=0.9)
        self.at("front area shrank")
        self.play(FadeIn(size_tags(FWD_B, STG1, {0: "smaller"}), shift=DOWN * 0.1), Indicate(m[0][0], color=PURPLE, scale_factor=0.97),
                  run_time=0.9)
        self.at("Total cortical area")
        self.play(Indicate(ol, color=TEXT, scale_factor=1.0), Transform(ol_l, ol_label("whole cortex: unchanged")),
                  run_time=1.2)
        self.finish()


def s18_end_state():
    chip_ = top_chip("Emx2 raised", ORANGE)
    m = mk_map(FWD_B, STG1)
    fb = fb_labels(STG1)
    ol = outline(STG1)
    ol_l = ol_label("whole cortex: unchanged")
    gh = ghost(STG1)
    tg = size_tags(FWD_B, STG1, {0: "smaller", 2: "bigger"})
    yr, rule, names = cite_block("2004", ["Tadashi Hamasaki", "and colleagues", "in O'Leary's laboratory"], sizes=[32, 32, 30])
    return chip_, m, fb, ol, ol_l, gh, tg, yr, rule, names


class S19(SpokenScene):
    """Loss and gain move the borders in opposite directions: evidence for allocating territory."""

    def construct(self):
        chip_, m, fb, ol, ol_l, gh, tg, yr, rule, names = s18_end_state()
        self.add(chip_, m, fb, ol, ol_l, gh, tg, yr, rule, *names)
        l_loss = lab("Emx2 loss: borders move back", -3.45, -2.3, 30, RED)
        a_loss = Arrow([-5.9, -2.95, 0], [-1.0, -2.95, 0], buff=0, color=RED, stroke_width=9, tip_length=0.33)
        l_gain = lab("Emx2 gain: borders move forward", 3.45, -2.3, 30, ORANGE)
        a_gain = Arrow([5.9, -2.95, 0], [1.0, -2.95, 0], buff=0, color=ORANGE, stroke_width=9, tip_length=0.33)
        self.at("Loss", lead=0.0)
        self.play(FadeOut(VGroup(tg, yr, rule, *names, ol, ol_l)), Transform(m, mk_map(BACK_B, STG1)),
                  Transform(chip_, top_chip("Emx2 loss", RED)), FadeIn(l_loss), GrowArrow(a_loss), run_time=0.8)
        self.at("gain")
        self.play(Transform(m, mk_map(FWD_B, STG1)), Transform(chip_, top_chip("Emx2 gain", ORANGE)), FadeIn(l_gain),
                  GrowArrow(a_gain), run_time=1.2)
        self.at("opposite directions")
        self.play(Indicate(a_loss, color=RED, scale_factor=1.05), Indicate(a_gain, color=ORANGE, scale_factor=1.05), run_time=1.2)
        alloc = lab("allocating territory", 0, -2.6, 46, TEXT, font=TITLE_FONT)
        self.at("allocating territory")
        self.play(FadeOut(VGroup(l_loss, a_loss, l_gain, a_gain)), run_time=0.35)
        self.play(FadeIn(alloc, shift=UP * 0.12), run_time=0.7)
        perm = lab("not simply permitting cortex to exist", 0, -3.4, 40, PALE, font=TITLE_FONT)
        self.at("not simply permitting")
        self.play(FadeIn(perm, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s20 to s27: the table at the top, the map at the left, the evidence panel at the right
PX = 4.3     # centre of the evidence panel


def panel_title(color, name, tagtext, tagcolor):
    return VGroup(bchip(name, color, 28).move_to([PX - 1.15, -0.1, 0]), bchip(tagtext, tagcolor, 28).move_to([PX + 1.45, -0.1, 0]))


def coup_card(stage):
    """the COUP-TFI evidence card: stage 0 = factor and loss, 1 = + year and laboratory, 2 = + the knockout line."""
    parts = [panel_title(COUP, "COUP-TFI", "loss", RED)]
    if stage >= 1:
        parts.append(tag("2007", PX, -1.0, GOLD, 40))
        parts.append(lab("Michèle Studer's\nlaboratory", PX, -1.95, 30, TEXT, line_spacing=0.9))
    if stage >= 2:
        parts.append(lab("cortex-only knockout", PX, -3.0, 30, PALE))
    return parts


class S20(SpokenScene):
    """The table begins: header and row one (Emx2), cell by cell; the map moves under it; COUP-TFI is next."""

    def construct(self):
        chip_, m, fb, ol, ol_l, gh, tg, yr, rule, names = s18_end_state()
        alloc = lab("allocating territory", 0, -2.6, 46, TEXT, font=TITLE_FONT)
        perm = lab("not simply permitting cortex to exist", 0, -3.4, 40, PALE, font=TITLE_FONT)
        chip3 = top_chip("Emx2 gain", ORANGE)
        m3 = mk_map(FWD_B, STG1)
        self.add(chip3, m3, fb, gh, alloc, perm)
        fr = tbl_lines(2)
        head = tbl_head()
        new_fb = fb_labels(STG2)
        self.play(FadeOut(VGroup(chip3, gh, alloc, perm, fb)), Transform(m3, mk_map(WT, STG2)), FadeIn(fr),
                  LaggedStart(*[FadeIn(h) for h in head], lag_ratio=0.12), FadeIn(new_fb), run_time=0.5)
        self.play(FadeIn(tbl_label(0), shift=RIGHT * 0.15), run_time=0.2)
        for j in (1, 2, 3):
            self.play(FadeIn(tbl_cell(0, j), shift=UP * 0.08), run_time=0.2)
        lab1 = tbl_label(1)
        self.at("tells a similar story", lead=0.2)
        self.play(FadeIn(lab1, shift=RIGHT * 0.15), FadeIn(coup_card(0)[0]), run_time=0.4)
        hl = cell_hl(1, 1)
        self.at("for loss")
        self.play(Create(hl), run_time=0.4)
        self.finish()


def table_scene_base(scene, rows, cells, mapb=WT, st=STG2):
    """add the carried state of the table scenes to the scene; return (map, fb, frame objects)."""
    items = tbl_carry(rows, cells)
    m = mk_map(mapb, st)
    fb = fb_labels(st)
    scene.add(m, fb, *items)
    return m, fb, items


BASE01 = {(0, 1): None, (0, 2): None, (0, 3): None}


class S21(SpokenScene):
    """COUP-TFI row: Studer's laboratory, 2007, a cortex-only knockout."""

    def construct(self):
        m, fb, items = table_scene_base(self, (0, 1), BASE01)
        card0 = coup_card(0)
        hl = cell_hl(1, 1)
        self.add(hl, *card0)
        c1, c2, c3 = coup_card(1)[1], coup_card(1)[2], coup_card(2)[3]
        self.at("In 2007")
        self.play(FadeIn(c1, shift=UP * 0.08), run_time=0.5)
        self.at("laboratory", lead=0.3)
        self.play(FadeIn(c2, shift=UP * 0.08), run_time=0.6)
        self.at("removed it")
        self.play(Indicate(card0[0][1], color=RED, scale_factor=1.12), run_time=0.7)
        self.at("cortex alone")
        self.play(FadeIn(c3, shift=UP * 0.08), Indicate(m[0], color=TEXT, scale_factor=1.02), run_time=1.0)
        self.finish()


class S22(SpokenScene):
    """Loss of COUP-TFI from cortex: motor spreads across most of the sheet, sensory squeezed back."""

    def construct(self):
        m, fb, items = table_scene_base(self, (0, 1), BASE01)
        hl = cell_hl(1, 1)
        card = coup_card(2)
        self.add(hl, *card)
        gh = ghost(STG2, ext=0.18, top=False)
        self.add(gh)
        new = tbl_cell(1, 1)
        self.at("Frontal motor areas")
        self.play(Transform(m, mk_map(COUP_B, STG2)), FadeIn(new, shift=UP * 0.08), run_time=2.0)
        cs = centers(COUP_B, STG2)
        yb = STG2["cy"] + STG2["h"] / 2 + 0.36
        t_big = tag("bigger", cs[0], yb, PURPLE, 30)
        t_sq = tag("sensory squeezed", (cs[1] + cs[2]) / 2 + 0.1, yb, GREEN, 28)
        self.play(FadeIn(t_big, shift=DOWN * 0.1), run_time=0.5)
        self.at("sensory areas were squeezed", lead=0.25)
        self.play(FadeIn(t_sq, shift=DOWN * 0.1), Indicate(m[0][1], color=GREEN, scale_factor=0.95),
                  Indicate(m[0][2], color=PINK, scale_factor=0.9), run_time=1.2)
        self.finish()


# ---- the Pax6 plot beside the map -------------------------------------------------------------
PP = dict(x0=2.4, w=4.0, base=-3.2, H=0.7)


def pax_plot():
    ax = axes_xy(PP["x0"], PP["w"], PP["base"], 2.0, extra=0.0)
    fr = lab("front", PP["x0"] + 0.35, -3.55, 26, GREY)
    bk = lab("back", PP["x0"] + PP["w"] - 0.2, -3.55, 26, GREY)
    lv = lab("level", PP["x0"] - 0.5, -2.2, 26, GREY).rotate(PI / 2)
    cv = curve(pax, BLUE, PP["x0"], PP["w"], PP["base"], PP["H"], sw=6)
    return VGroup(ax, fr, bk, lv), cv


def pax_plot_final():
    axs, cv = pax_plot()
    orig = dashed(cv.copy().set_stroke(width=4), 30)
    high = curve(pax, BLUE, PP["x0"], PP["w"], PP["base"], PP["H"], sw=7, mult=3.0)
    pl = tag("Pax6", 5.85, -1.95, BLUE, 30)
    t3 = lab("up to 3× normal", 5.0, -1.35, 26, BLUE)
    nl = lab("normal", 3.35, -2.2, 26, BLUE)
    return axs, orig, high, pl, t3, nl


def price_block():
    return tag("2007", PX, -0.12, GOLD, 34), lab("David Price's group", PX, -0.7, 30, TEXT)


class S23(SpokenScene):
    """Pax6, the cautionary case: Price's group raised it up to three times normal."""

    def construct(self):
        m, fb, items = table_scene_base(self, (0, 1), {**BASE01, (1, 1): None}, COUP_B)
        hl = cell_hl(1, 1)
        card = coup_card(2)
        gh = ghost(STG2, ext=0.18, top=False)
        self.add(hl, *card, gh)
        l2 = tbl_label(2)
        axs, cv = pax_plot()
        pl = tag("Pax6", 5.85, -1.95, BLUE, 30)
        self.play(FadeOut(VGroup(hl, gh, *card)), Transform(m, mk_map(WT, STG2)), Transform(items[0], tbl_lines(3)), FadeIn(l2), run_time=0.9)
        self.play(FadeIn(axs), Create(cv), FadeIn(pl), run_time=0.8)
        yr, grp = price_block()
        self.at("In 2007", lead=0.2)
        self.play(FadeIn(yr, shift=UP * 0.08), run_time=0.5)
        self.at("David")
        self.play(FadeIn(grp, shift=UP * 0.08), run_time=0.5)
        orig = dashed(cv.copy().set_stroke(width=4), 30)
        high = curve(pax, BLUE, PP["x0"], PP["w"], PP["base"], PP["H"], sw=7, mult=3.0)
        nl = lab("normal", 3.35, -2.2, 26, BLUE)
        self.at("raised it")
        self.add(orig)
        self.play(Transform(cv, high), FadeIn(nl), run_time=1.2)
        t3 = lab("up to 3× normal", 5.0, -1.35, 26, BLUE)
        self.at("three times normal")
        self.play(FadeIn(t3, shift=UP * 0.1), run_time=0.7)
        self.finish()


def s23_state(scene):
    m, fb, items = table_scene_base(scene, (0, 1, 2), {**BASE01, (1, 1): None}, WT)
    axs, orig, high, pl, t3, nl = pax_plot_final()
    yr, grp = price_block()
    scene.add(axs, orig, high, pl, t3, nl, yr, grp)
    return m, fb, items, (axs, orig, high, pl, t3, nl, yr, grp)


class S24(SpokenScene):
    """The map barely moved."""

    def construct(self):
        m, fb, items, plot = s23_state(self)
        c = tbl_cell(2, 2)
        self.at("The map barely moved", lead=0.0)
        self.play(FadeIn(c, shift=UP * 0.08), Indicate(m[0], color=TEXT, scale_factor=1.01), run_time=0.9)
        self.finish()


# ---- s25: markers shift, connections do not ----------------------------------------------------
BAND_Y, BAND_H = 0.13, 0.42


def marker_band(b):
    x0, w = STG3["x0"], STG3["w"]
    fr = Rectangle(width=w, height=BAND_H, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.12).move_to([x0 + w / 2, BAND_Y, 0])
    bars = VGroup(*[Line([x0 + bb * w, BAND_Y - BAND_H / 2 + 0.03, 0], [x0 + bb * w, BAND_Y + BAND_H / 2 - 0.03, 0], stroke_color=TEXT, stroke_width=7) for bb in b])
    return fr, bars


def band_ghost(b):
    x0, w = STG3["x0"], STG3["w"]
    return VGroup(*[DashedLine([x0 + bb * w, BAND_Y - BAND_H / 2 - 0.02, 0], [x0 + bb * w, BAND_Y + BAND_H / 2 + 0.02, 0], dash_length=0.07,
                               stroke_color=GREY, stroke_width=5) for bb in b])


MK_SHIFT = (0.28, 0.60)


def thalamus_axons():
    cs = centers(WT, STG3)
    bot = STG3["cy"] - STG3["h"] / 2
    tcx = sum(cs) / 3
    th = bchip("thalamus", TEXT, 26).move_to([tcx, -2.75, 0])
    ax_ = VGroup(*[CubicBezier([tcx + (k - 1) * 0.55, -2.46, 0], [tcx + (k - 1) * 0.55, -2.15, 0], [cc, -2.1, 0], [cc, bot - 0.08, 0],
                               stroke_color=TEXT, stroke_width=5) for k, cc in enumerate(cs)])
    dots = VGroup(*[Dot([cc, bot - 0.06, 0], radius=0.12, color=TEXT) for cc in cs])
    return th, ax_, dots


def legend_rows():
    s1 = VGroup(Line([2.05, -1.65, 0], [2.05, -2.05, 0], stroke_color=TEXT, stroke_width=7),
                lab("marker-gene\nborders: shifted", 3.55, -1.85, 26, TEXT, line_spacing=0.9).align_to([2.35, 0, 0], LEFT))
    s2 = VGroup(Dot([2.05, -2.7, 0], radius=0.12, color=TEXT),
                lab("thalamic axons:\nsame as normal", 3.55, -2.7, 26, TEXT, line_spacing=0.9).align_to([2.35, 0, 0], LEFT))
    return s1, s2


def s25_head():
    return tag("2008", PX, -0.12, GOLD, 34), lab("Pax6 knocked out\nin cortex only", PX, -0.95, 28, TEXT, line_spacing=0.9)


class S25(SpokenScene):
    """A cortex-only Pax6 knockout shifted the markers, yet thalamic connections stayed normal."""

    def construct(self):
        m, fb, items, plot = s23_state(self)
        c22 = tbl_cell(2, 2)
        self.add(c22)
        yr2, what = s25_head()
        fr, bars = marker_band(WT)
        newfb = fb_labels(STG3)
        # the panel is cleared and the map is reset to the area boxes alone; the knockout is named before the narrator says it
        self.play(FadeOut(VGroup(*plot)), Transform(m, mk_map(WT, STG3)), Transform(fb, newfb),
                  FadeIn(yr2, shift=UP * 0.08), FadeIn(what, shift=UP * 0.08), FadeIn(fr), FadeIn(bars), run_time=0.9)
        gh = band_ghost(WT)
        s1, s2 = legend_rows()
        c = tbl_cell(2, 1)
        self.at("shifted the markers", lead=0.3)
        self.add(gh)
        self.play(bars.animate.become(marker_band(MK_SHIFT)[1]), FadeIn(s1, shift=UP * 0.08), FadeIn(c, shift=UP * 0.08), run_time=1.1)
        th, ax_, dots = thalamus_axons()
        self.at("area specific connections", lead=0.3)
        self.play(FadeIn(th), LaggedStart(*[Create(a) for a in ax_], lag_ratio=0.3), FadeIn(s2, shift=UP * 0.08), run_time=1.6)
        self.play(FadeIn(dots), run_time=0.4)
        self.at("stayed normal")
        self.play(Indicate(dots, color=TEXT, scale_factor=1.6), run_time=1.0)
        self.finish()


def s25_state(scene):
    cells = {(0, 1): None, (0, 2): None, (0, 3): None, (1, 1): None, (2, 2): None, (2, 1): None}
    items = tbl_carry((0, 1, 2), cells)
    m = mk_map(WT, STG3)
    fb = fb_labels(STG3)
    scene.add(m, fb, *items)
    yr2, what = s25_head()
    fr, bars = marker_band(MK_SHIFT)
    gh = band_ghost(WT)
    s1, s2 = legend_rows()
    th, ax_, dots = thalamus_axons()
    grp = VGroup(yr2, what, fr, bars, gh, s1, s2, th, ax_, dots)
    scene.add(grp)
    return m, fb, grp


class S26(SpokenScene):
    """Pax6: loss and gain disagree; 2013 cortex-only knockout shrank the touch area; role unsettled."""

    def construct(self):
        m, fb, grp = s25_state(self)
        newfb = fb_labels(STG2)
        bias = bchip("may bias markers", BLUE, 28).move_to([PX, -0.2, 0])
        more_ = lab("more than it", PX, -0.95, 26, PALE)
        sits_t = T("decides where\nan area sits", 28, PALE, line_spacing=0.9)
        sits_b = RoundedRectangle(corner_radius=0.14, width=sits_t.width + 0.5, height=sits_t.height + 0.4, stroke_color=GREY,
                                  stroke_width=2.5, fill_color=BG, fill_opacity=0.92)
        sits = VGroup(sits_b, sits_t).move_to([PX, -1.9, 0])
        bias = VGroup(bias, more_)
        v1 = tbl_cell(2, 3, "loss and gain\ndisagree", TEXT)
        self.play(FadeOut(grp), Transform(m, mk_map(WT, STG2)), Transform(fb, newfb), run_time=0.5)
        self.at("may bias")
        self.play(FadeIn(bias, shift=UP * 0.08), FadeIn(v1, shift=UP * 0.08), run_time=0.8)
        self.at("more than", lead=0.2)
        self.play(FadeIn(sits, shift=UP * 0.08), run_time=0.7)
        # clear the 2008 case before the 2013 case appears
        yr3 = tag("2013", PX, -0.12, GOLD, 34)
        what3 = lab("Pax6 knocked out\nin cortex only", PX, -0.95, 28, TEXT, line_spacing=0.9)
        self.at("But in", lead=0.1)
        self.play(FadeOut(VGroup(bias, sits)), run_time=0.4)
        self.play(FadeIn(yr3, shift=UP * 0.08), run_time=0.5)
        self.at("cortex only", lead=0.5)
        self.play(FadeIn(what3, shift=UP * 0.08), run_time=0.5)
        tb = m[0][1]
        norm = DashedVMobject(Rectangle(width=tb.width, height=tb.height, stroke_color=TEXT, stroke_width=3).move_to(tb.get_center()), num_dashes=40)
        small = tb.copy().stretch_to_fit_width(tb.width * 0.55).move_to(tb.get_center())
        cx = tb.get_center()[0]
        small_lbl = tag("smaller touch area", cx, STG2["cy"] + STG2["h"] / 2 + 0.36, GREEN, 28)
        self.at("shrank the touch area", lead=0.4)
        self.add(norm)
        self.play(Transform(tb, small), FadeOut(m[1][1]), FadeIn(small_lbl, shift=UP * 0.08), run_time=1.3)
        v2 = tbl_cell(2, 3, "role in placing\nborders unsettled", GOLD, 26)
        self.at("Its role is still unsettled")
        self.play(Transform(v1, v2), Create(row_hl(2)), run_time=0.8)
        self.finish()


class S27(SpokenScene):
    """The finished table: opposite shifts are the strongest evidence; a missing converse result does not rule out."""

    def construct(self):
        cells = {(0, 1): None, (0, 2): None, (0, 3): None, (1, 1): None, (2, 2): None, (2, 1): None}
        items = tbl_carry((0, 1, 2), cells)
        m = mk_map(WT, STG2)
        fb = fb_labels(STG2)
        tb = m[0][1]
        small = tb.copy().stretch_to_fit_width(tb.width * 0.55).move_to(tb.get_center())
        tb.become(small)
        m[1][1].set_opacity(0)
        cx = tb.get_center()[0]
        norm = DashedVMobject(Rectangle(width=STG2["w"] * (WT[1] - WT[0]), height=STG2["h"], stroke_color=TEXT, stroke_width=3)
                              .move_to([cx, STG2["cy"], 0]), num_dashes=40)
        small_lbl = tag("smaller touch area", cx, STG2["cy"] + STG2["h"] / 2 + 0.36, GREEN, 28)
        yr3 = tag("2013", PX, -0.12, GOLD, 34)
        what3 = lab("Pax6 knocked out\nin cortex only", PX, -0.95, 28, TEXT, line_spacing=0.9)
        v2 = tbl_cell(2, 3, "role in placing\nborders unsettled", GOLD, 26)
        rh2 = row_hl(2)
        self.add(m, fb, *items, norm, small_lbl, yr3, what3, v2, rh2)
        self.play(FadeOut(VGroup(yr3, what3, norm, small_lbl, rh2)), Transform(tb, mk_map(WT, STG2)[0][1]), run_time=0.7)
        m[1][1].set_opacity(1)
        rh = row_hl(0)
        lose = bchip("losing a factor", RED, 28).move_to([PX, -0.55, 0])
        add = bchip("adding it", ORANGE, 28).move_to([PX, -1.55, 0])
        self.at("losing a factor", lead=0.1)
        self.play(FadeIn(lose, shift=UP * 0.08), Create(rh), run_time=0.8)
        self.at("adding it")
        self.play(FadeIn(add, shift=UP * 0.08), run_time=0.7)
        a1 = lab("loss and gain: opposite directions", 0, -1.5, 36, TEXT)
        cardA = box(11.6, 0.95, 0, -1.5, GOLD, 0.06)
        self.at("opposite directions")
        self.play(FadeOut(VGroup(m, fb, lose, add)), FadeIn(cardA), FadeIn(a1, shift=UP * 0.1), run_time=0.8)
        cardA2 = box(11.6, 1.75, 0, -1.5, GOLD, 0.06)
        a2 = lab("the strongest evidence", 0, -1.95, 46, GOLD, font=TITLE_FONT)
        self.at("strongest evidence")
        self.play(Transform(cardA, cardA2), a1.animate.move_to([0, -1.05, 0]), FadeIn(a2, shift=UP * 0.1), run_time=0.8)
        ch = cell_hl(1, 2, TEXT)
        cardB = box(11.6, 1.0, 0, -2.85, TEXT, 0.04)
        b1 = lab("a missing converse result does not rule a factor out", 0, -2.85, 32, TEXT)
        newcell = tbl_cell(1, 2, TXT[(1, 2)], PALE)
        self.at("A missing converse result")
        self.play(FadeOut(rh), Create(ch), FadeIn(newcell), FadeIn(cardB), FadeIn(b1, shift=UP * 0.1),
                  VGroup(cardA, a1, a2).animate.shift(UP * 0.55), run_time=1.0)
        self.at("rule a factor out")
        self.play(Indicate(b1, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.finish()


class S28End(EndCard):
    LINE = "Opposite shifts after loss and gain\nshow a factor helps allocate territory."

    def construct(self):
        line = T(self.LINE, size=48, font=TITLE_FONT, line_spacing=1.0)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=26, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
