"""Chapter 3 of 6: A Code in Two Classes  (Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole film series; taken from scenes.old.py, class I moved off the teal)
  YELLOW = Sonic hedgehog (Shh) and the slope of signal it makes (gradient, chips, arrows)
  TEAL   = notochord and floor plate (the source tissue)
  CI     = class I factors (Pax7, Dbx1, Dbx2, Irx3, Pax6): Shh switches them off. Indigo, clearly away from teal
  ORANGE = class II factors (Nkx6.1, Nkx2.2) and the p3 domain beside the floor plate
  GREEN  = Olig2 (a bHLH protein, not a homeodomain factor) and the pMN domain it marks
  RED    = repression (the T-bars) and nothing else
  PURPLE = Patched1 (not used in this chapter)
  GREY   = tube wall, neutral cells, axes, roof plate, epidermis
  TEXT   = neutral things: transcription-factor cartoon, table frame, p0 to p2 stripes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

_BaseSpoken = SpokenScene


class SpokenScene(_BaseSpoken):  # noqa: F811
    """Cues fire on the first sound of the phrase, not 0.2 s ahead of it."""

    def at(self, phrase, lead=0.0, nth=0):
        return _BaseSpoken.at(self, phrase, lead=lead, nth=nth)

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
CI = "#8F9BFF"

LESSON = "Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube"


# ----------------------------------------------------------------------------- small helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * 0.22, b - perp * 0.22, color=color, stroke_width=w + 1))


def put(mob, x, y, edge=None):
    if edge is None:
        return mob.move_to([x, y, 0])
    return mob.move_to([x, y, 0], aligned_edge=edge)


# ----------------------------------------------------------------------------- the tube map (always at the left)
TX = -5.3                 # tube centre x
WX = -4.75                # wall cells centre x
Y0, Y1 = -2.4, 2.9        # wall runs from the floor plate up to the roof plate
SLOTS = {"p3": (-2.4, -1.8), "pMN": (-1.8, -1.2), "p2": (-1.2, -0.6), "p1": (-0.6, 0.0), "p0": (0.0, 0.6)}
SLOT_COL = {"p0": TEXT, "p1": TEXT, "p2": TEXT, "pMN": GREEN, "p3": ORANGE}


def shh(y):
    return np.exp(-(y - Y0) / 2.0)


def cell_style(y):
    lv = shh(y)
    return 0.04 + 0.86 * lv ** 1.2, 0.25 + 0.75 * lv        # fill opacity, stroke opacity


def tube_base():
    tube = RoundedRectangle(corner_radius=0.9, width=2.0, height=5.8, stroke_color=GREY, stroke_width=5,
                            fill_color=GREY, fill_opacity=0.07).move_to([TX, 0.3, 0])
    canal = RoundedRectangle(corner_radius=0.07, width=0.14, height=4.4, stroke_width=0,
                             fill_color=GREY, fill_opacity=0.45).move_to([TX, 0.3, 0])
    roof = RoundedRectangle(corner_radius=0.05, width=0.9, height=0.2, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.5).move_to([TX, 3.05, 0])
    epi = Line([TX - 1.1, 3.55, 0], [TX + 1.1, 3.55, 0], color=GREY, stroke_width=5)
    fp = RoundedRectangle(corner_radius=0.05, width=1.2, height=0.2, stroke_color=TEAL, stroke_width=3,
                          fill_color=TEAL, fill_opacity=0.6).move_to([TX, -2.5, 0])
    noto = Circle(radius=0.3, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.35).move_to([TX, -3.2, 0])
    return VGroup(tube, canal, roof, epi, fp, noto)


WALL_YS = np.linspace(Y0 + 0.19, Y1 - 0.19, 14)


def wall_cells(shaded=True):
    cs = VGroup()
    for y in WALL_YS:
        c = RoundedRectangle(corner_radius=0.06, width=0.8, height=0.34, stroke_width=2).move_to([WX, y, 0])
        if shaded:
            fo, so = cell_style(y)
            c.set_stroke(YELLOW, opacity=so).set_fill(YELLOW, fo)
        else:
            c.set_stroke(GREY).set_fill(GREY, 0.2)
        cs.add(c)
    return cs


def shade_anims(cells):
    out = []
    for c, y in zip(cells, WALL_YS):
        fo, so = cell_style(y)
        out.append(c.animate.set_stroke(YELLOW, opacity=so).set_fill(YELLOW, fo))
    return out


def wall_stripes(filled=()):
    """The wall as five domain slots plus the dorsal half. Returns (dorsal, {name: rect})."""
    def mk(y0, y1, name):
        r = Rectangle(width=0.8, height=y1 - y0 - 0.04, stroke_width=2.5).move_to([WX, (y0 + y1) / 2, 0])
        r.set_stroke(GREY, opacity=0.5).set_fill(GREY, 0.0)
        if name in filled:
            fill_slot(r, name)
        return r
    return mk(0.6, Y1, "dorsal"), {n: mk(a, b, n) for n, (a, b) in SLOTS.items()}


def fill_slot(r, name, strong=0.45):
    col = SLOT_COL.get(name, CI)
    r.set_stroke(col, opacity=0.95).set_fill(col, strong if col != TEXT else 0.2)
    return r


def slot_anim(r, name, strong=0.45):
    col = SLOT_COL.get(name, CI)
    return r.animate.set_stroke(col, opacity=0.95).set_fill(col, strong if col != TEXT else 0.2)


# ----------------------------------------------------------------------------- the slope beside the tube
SLX0, SLW = -3.9, 2.4


def curve_x(y, x0=SLX0, w=SLW):
    return x0 + w * shh(y)


def slope_parts(x0=SLX0, w=SLW):
    ys = np.linspace(Y0, Y1, 50)
    pts = [np.array([curve_x(y, x0, w), y, 0]) for y in ys]
    axis = Line([x0, Y0, 0], [x0, Y1, 0], color=GREY, stroke_width=3)
    crv = VMobject(stroke_color=YELLOW, stroke_width=6).set_points_smoothly(pts)
    area = Polygon(*([np.array([x0, Y0, 0])] + pts + [np.array([x0, Y1, 0])]), stroke_width=0,
                   fill_color=YELLOW, fill_opacity=0.2)
    return axis, area, crv


def slope_label():
    return put(T("Shh level", 26, YELLOW), SLX0 + 1.2, Y0 - 0.42)


# ----------------------------------------------------------------------------- factor bars (columns right of the slope)
BAR_W = 0.4
CLS1_TOP = Y1
# name: (x, class, border)
BARS = {"Pax7": (-0.45, 1, 0.6), "Dbx1": (0.4, 1, 0.0), "Dbx2": (1.25, 1, -0.6), "Irx3": (2.1, 1, -1.2),
        "Pax6": (2.95, 1, -1.8), "Nkx6.1": (4.0, 2, -0.6), "Nkx2.2": (4.95, 2, -1.8), "Olig2": (6.0, 3, -1.2)}
BARS_R = 6.5          # right end of the baseline and the border lines
CLS_COL = {1: CI, 2: ORANGE, 3: GREEN}
CLS1 = ("Pax7", "Dbx1", "Dbx2", "Irx3", "Pax6")
BORDER_YS = [0.6, 0.0, -0.6, -1.2, -1.8]


def _rect(x, ytop, ybot, color, fo, so):
    return Rectangle(width=BAR_W, height=ytop - ybot, stroke_color=color, stroke_width=2.5, stroke_opacity=so,
                     fill_color=color, fill_opacity=fo).move_to([x, (ytop + ybot) / 2, 0])


def make_bar(name, k=1.0):
    x, cls, b = BARS[name]
    col = CLS_COL[cls]
    if cls == 1:
        if name == "Pax6":      # full down to the p2/pMN border, then a thin dim stretch: pMN keeps only a little Pax6
            return VGroup(_rect(x, CLS1_TOP, -1.2, col, 0.55 * k, k), _rect(x, -1.2, b, col, 0.14 * k, 0.5 * k))
        return _rect(x, CLS1_TOP, b, col, 0.55 * k, k)
    if cls == 2:
        return _rect(x, b, Y0, col, 0.55 * k, k)
    return _rect(x, -1.2, -1.8, col, 0.55 * k, k)      # Olig2 sits in the pMN stretch only


def label_pos(name):
    x, cls, b = BARS[name]
    return (x, b - 0.3) if cls == 1 else (x, b + 0.3)


def bar_label(name, size=26, k=1.0, weight=NORMAL):
    x, cls, b = BARS[name]
    t = T(name, size, CLS_COL[cls], weight=weight)
    put(t, *label_pos(name))
    if name == "Pax6":      # tag the dim stretch so the chart agrees with the table
        t = VGroup(t, put(T("low", 22, CI), x + 0.52, -1.5))
    if k < 1:
        t.set_opacity(k)
    return t


def thr_line(name, op=0.6, full=False):
    """Dashed threshold line from the slope (where Shh crosses this factor's level) to the bar."""
    x, cls, b = BARS[name]
    x1 = BARS_R if full else x + 0.25
    ln = DashedLine([curve_x(b) + 0.06, b, 0], [x1, b, 0], color=TEXT, stroke_width=2.5, dash_length=0.14)
    ln.set_opacity(op)
    ln.set_z_index(-1)
    return ln


def thr_dot(name, k=1.0):
    x, cls, b = BARS[name]
    return Dot([curve_x(b), b, 0], radius=0.1, color=CLS_COL[cls], fill_opacity=k)


def tip_cap(name):
    x, cls, b = BARS[name]
    return Line([x - 0.27, b, 0], [x + 0.27, b, 0], color=TEXT, stroke_width=4)


def baseline():
    return Line([SLX0, Y0, 0], [BARS_R, Y0, 0], color=GREY, stroke_width=2, stroke_opacity=0.7)


def items(names, k=1.0, labels=True):
    """name -> dict(bar, line, dot, label) in the finished state; k < 1 ghosts them."""
    d = {}
    for n in names:
        d[n] = dict(bar=make_bar(n, k), line=thr_line(n, 0.6 * k), dot=thr_dot(n, k),
                    label=bar_label(n, 26, k) if labels else None)
    return d


def flat(d, keys=("bar", "line", "dot", "label")):
    return [m for v in d.values() for kk in keys for m in [v[kk]] if m is not None]


def class_legend(cls):
    """Shh --| Class I   or   Shh --> Class II, at the top."""
    s = chip("Shh", YELLOW, 26)
    if cls == 1:
        link = inhib([0, 0, 0], [1.3, 0, 0], RED)
        c = chip("Class I", CI, 26)
    else:
        link = arr([0, 0, 0], [1.3, 0, 0], YELLOW, 5)
        c = chip("Class II", ORANGE, 26)
    VGroup(s, link, c).arrange(RIGHT, buff=0.12).move_to([2.0, 3.4, 0])
    return s, link, c


def base_stage(scene, wall_shaded=True):
    base = tube_base()
    wall = wall_cells(shaded=wall_shaded)
    axis, area, crv = slope_parts()
    bl, xl = baseline(), slope_label()
    scene.add(base, wall, area, axis, crv, bl, xl)
    return base, wall, axis, area, crv, bl, xl


def tube_labels():
    return VGroup(put(T("epidermis", 26, GREY), -4.05, 3.55, LEFT), put(T("roof plate", 26, GREY), -4.05, 3.0, LEFT),
                  put(T("floor plate", 26, TEAL), -4.05, -2.62, LEFT), put(T("notochord", 26, TEAL), -4.75, -3.3, LEFT))


# ----------------------------------------------------------------------------- the table (scenes 14 to 19)
TB_COLS = [("Dbx1", CI), ("Dbx2", CI), ("Irx3", CI), ("Pax6", CI), ("Nkx6.1", ORANGE), ("Olig2", GREEN), ("Nkx2.2", ORANGE)]
TB_X = [-3.95 + 1.3 * i for i in range(7)]
TB_ROWS = ["p0", "p1", "p2", "pMN", "p3"]
TB_Y = [2.1 - 0.92 * i for i in range(5)]
TB_DATA = {"p0": [1, 1, 1, 1, 0, 0, 0], "p1": [0, 1, 1, 1, 0, 0, 0], "p2": [0, 0, 1, 1, 1, 0, 0],
           "pMN": [0, 0, 0, 2, 1, 1, 0], "p3": [0, 0, 0, 0, 1, 0, 1]}      # 1 present, 0 absent, 2 low
ROW_COL = {"p0": TEXT, "p1": TEXT, "p2": TEXT, "pMN": GREEN, "p3": ORANGE}
TB_L, TB_R = -6.1, 4.4


def build_table():
    head = VGroup(*[put(T(n, 24, c, weight=BOLD), x, 3.28, UP) for (n, c), x in zip(TB_COLS, TB_X)])
    rowl = VGroup(*[put(T(r, 28, ROW_COL[r], weight=BOLD), -5.3, y) for r, y in zip(TB_ROWS, TB_Y)])
    cells = {}
    cg = VGroup()
    for r, y in zip(TB_ROWS, TB_Y):
        for j, ((n, c), x) in enumerate(zip(TB_COLS, TB_X)):
            v = TB_DATA[r][j]
            if v == 1:
                m = Dot([x, y, 0], radius=0.22, color=c)
            elif v == 2:
                m = VGroup(Dot([x - 0.3, y, 0], radius=0.12, color=c), put(T("low", 24, c), x + 0.25, y))
            else:
                m = Line([x - 0.15, y, 0], [x + 0.15, y, 0], color=GREY, stroke_width=3, stroke_opacity=0.55)
            cells[(r, j)] = m
            cg.add(m)
    ys = [2.6] + [y - 0.46 for y in TB_Y]
    sep = VGroup(*[Line([TB_L, y, 0], [TB_R, y, 0], color=GREY, stroke_width=1.5, stroke_opacity=0.4) for y in ys])
    return head, rowl, cg, cells, sep


def row_box(name, color, fill=0.0):
    y = TB_Y[TB_ROWS.index(name)]
    b = RoundedRectangle(corner_radius=0.12, width=TB_R - TB_L + 0.2, height=0.86, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=fill).move_to([(TB_L + TB_R) / 2, y, 0])
    b.set_z_index(-1)
    return b


def cell_ring(row, j, color, op=1.0):
    r = Circle(radius=0.33, stroke_color=color, stroke_width=4, stroke_opacity=op).move_to([TB_X[j], TB_Y[TB_ROWS.index(row)], 0])
    r.set_z_index(2)
    return r


def low_ring(row, color):
    r = RoundedRectangle(corner_radius=0.2, width=1.2, height=0.62, stroke_color=color, stroke_width=4).move_to(
        [TB_X[3], TB_Y[TB_ROWS.index(row)], 0])
    r.set_z_index(2)
    return r


def simp_tag():
    return chip("simplified", GREY, 26).move_to([5.6, 2.6, 0])


QUESTION = "Which markers differ?"


def question_text():
    return put(T(QUESTION, 38, TEXT), -0.9, -3.1)


# ----------------------------------------------------------------------------- the zoomed ventral panel (scenes 20 to 22)
PX0, PX1 = -2.7, 1.9
PY = {"p0": (1.92, 2.9), "p1": (0.94, 1.92), "p2": (-0.04, 0.94), "pMN": (-1.02, -0.04), "p3": (-2.0, -1.02)}
OUTS = {"p0": ("V0 interneurons", TEXT), "p1": ("V1 interneurons", TEXT), "p2": ("V2 interneurons", TEXT),
        "pMN": ("motor neurons", GREEN), "p3": ("V3 interneurons", ORANGE)}


def panel_slots():
    d = {}
    for n, (a, b) in PY.items():
        r = Rectangle(width=PX1 - PX0, height=b - a - 0.06, stroke_width=3).move_to([(PX0 + PX1) / 2, (a + b) / 2, 0])
        r.set_stroke(GREY, opacity=0.5).set_fill(GREY, 0.0)
        d[n] = r
    return d


def panel_label(n):
    return put(T(n, 34, TEXT, weight=BOLD), PX0 + 0.75, (PY[n][0] + PY[n][1]) / 2)


def panel_out(n):
    a = (PY[n][0] + PY[n][1]) / 2
    txt, col = OUTS[n]
    ar = arr([PX1 + 0.1, a, 0], [PX1 + 0.7, a, 0], col if col != TEXT else GREY, 4, 0.18)
    lab = put(T(txt, 30, col), PX1 + 0.85, a, LEFT)
    return VGroup(ar, lab)


def zoom_lines():
    return VGroup(DashedLine([-4.35, 0.6, 0], [PX0, 2.9, 0], color=GREY, stroke_width=2),
                  DashedLine([-4.35, Y0, 0], [PX0, -2.0, 0], color=GREY, stroke_width=2))


def fp_band():
    b = RoundedRectangle(corner_radius=0.08, width=PX1 - PX0, height=0.5, stroke_color=TEAL, stroke_width=3,
                         fill_color=TEAL, fill_opacity=0.5).move_to([(PX0 + PX1) / 2, -2.35, 0])
    return b, put(T("floor plate", 30, TEXT, weight=BOLD), (PX0 + PX1) / 2, -2.35)


def fill_stage(scene, filled=()):
    base = tube_base()
    dors, st = wall_stripes(filled)
    slots = panel_slots()
    for n in filled:
        fill_slot(slots[n], n)
    labs = {n: panel_label(n) for n in PY}
    zl = zoom_lines()
    return base, dors, st, slots, labs, zl


# =============================================================================================
class S00Title(TitleCard):
    LESSON = LESSON
    TITLE = "A Code in Two Classes"


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        base = tube_base()
        wall = wall_cells(shaded=False)
        lab_epi = put(T("epidermis", 26, GREY), -4.05, 3.55, LEFT)
        lab_roof = put(T("roof plate", 26, GREY), -4.05, 3.0, LEFT)
        lab_vz = put(T("ventricular\nzone", 26, GREY, line_spacing=0.8), -4.05, 1.5, LEFT)
        lab_fp = put(T("floor plate", 26, TEAL), -4.05, -2.62, LEFT)
        lab_n = put(T("notochord", 26, TEAL), -4.75, -3.3, LEFT)
        head = put(T("A Code in Two Classes", 40, TEXT, font=TITLE_FONT), 3.4, 3.4)
        labels = VGroup(lab_epi, lab_roof, lab_vz, lab_fp, lab_n)
        self.play(FadeIn(base), FadeIn(wall), FadeIn(labels), FadeIn(head), run_time=0.25)

        x0, w = -1.4, 4.6
        axis, area, crv = slope_parts(x0, w)
        axis = Arrow([x0, Y0, 0], [x0, Y1 + 0.1, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
        xlab = put(T("Sonic hedgehog level", 28, YELLOW), x0 + 2.4, Y0 - 0.45)
        ylab = put(T("distance from\nfloor plate", 26, GREY, line_spacing=0.8), x0 + 1.9, 2.15)
        self.at("sonic hedgehog")
        self.play(*shade_anims(wall), Create(axis), FadeIn(xlab), run_time=0.5)
        self.at("falls off")
        self.play(Create(crv), FadeIn(area), run_time=1.0)
        self.play(FadeIn(ylab), run_time=0.3)
        self.at("floor plate")
        self.play(Indicate(base[4], color=TEAL, scale_factor=1.3), Indicate(lab_fp, color=TEAL, scale_factor=1.1), run_time=0.8)

        how = put(T("how much?", 34, YELLOW), 1.5, 0.9)
        self.at("how does")
        self.play(FadeIn(how, shift=UP * 0.1), Indicate(crv, color=YELLOW, scale_factor=1.0), run_time=0.7)
        qs = VGroup(*[chip("?", TEXT, 34, pad=0.2).move_to([5.5, y, 0]) for y in (1.7, 0.85, 0.0, -0.85, -1.7)])
        which = put(T("which neuron?", 30, TEXT), 5.2, 2.6)
        divs = VGroup(*[Line([WX - 0.4, y, 0], [WX + 0.4, y, 0], color=TEXT, stroke_width=2, stroke_opacity=0.7) for y in (0.6, 0.0, -0.6, -1.2, -1.8)])
        go = arr([3.3, 0.0, 0], [4.55, 0.0, 0], YELLOW, 5)
        self.at("which neuron")
        self.play(FadeIn(divs), FadeOut(lab_vz), FadeIn(which, shift=UP * 0.1), GrowArrow(go),
                  LaggedStart(*[FadeIn(q, scale=0.6) for q in qs], lag_ratio=0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Morph(SpokenScene):
    def construct(self):
        cy = 1.9
        src = Circle(radius=0.45, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.55).move_to([-5.4, cy, 0])
        src_l = put(T("source", 26, TEAL), -5.4, cy - 0.95)
        slices = VGroup(*[Rectangle(width=0.9, height=1.9, stroke_width=0, fill_color=YELLOW,
                                    fill_opacity=0.5 * np.exp(-i * 0.3)).move_to([-4.75 + 0.45 + 0.9 * i, cy, 0]) for i in range(12)])
        xs = (-3.2, -0.2, 2.8)
        lv = (0.95, 0.5, 0.12)
        cells = VGroup()
        for x, ch, l in zip(xs, "ABC", lv):
            c = RoundedRectangle(corner_radius=0.12, width=1.0, height=1.0, stroke_color=YELLOW, stroke_width=3,
                                 fill_color=YELLOW, fill_opacity=0.05 + 0.85 * l).move_to([x, cy, 0])
            cells.add(VGroup(c, put(T(ch, 38, BG if l > 0.6 else TEXT, weight=BOLD), x, cy)))
        levels = VGroup(*[put(T(t, 26, YELLOW), x, 0.7) for x, t in zip(xs, ("high", "middle", "low"))])
        outs = VGroup(*[chip(f"instruction {i + 1}", TEXT, 26, pad=0.18).move_to([x, 0.0, 0]) for i, x in enumerate(xs)])
        card = RoundedRectangle(corner_radius=0.25, width=12.2, height=2.2, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([0, -2.4, 0])
        title = put(T("morphogen", 44, YELLOW, weight=BOLD), 0, -1.75)
        l1 = put(T("a signal that spreads from a source", 28, TEXT), 0, -2.45)
        l2 = put(T("and gives different instructions at different concentrations", 28, TEXT), 0, -3.0)

        self.play(FadeIn(src, scale=0.6), FadeIn(src_l), run_time=0.5)
        self.at("spreads from a source")
        self.play(LaggedStart(*[FadeIn(s) for s in slices], lag_ratio=0.08), FadeIn(card), FadeIn(l1), run_time=1.3)
        self.at("different instructions")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.3), FadeIn(l2), run_time=1.0)
        self.at("different concentrations")
        self.play(FadeIn(levels), LaggedStart(*[FadeIn(o, shift=DOWN * 0.1) for o in outs], lag_ratio=0.25), run_time=1.0)
        self.at("called a morphogen")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
        self.play(Indicate(title, color=YELLOW, scale_factor=1.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Hd(SpokenScene):
    def construct(self):
        dna = Rectangle(width=12.6, height=0.55, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to([0, -2.2, 0])
        dna_l = put(T("DNA", 28, TEXT), -5.7, -2.2)
        body = RoundedRectangle(corner_radius=0.6, width=5.4, height=2.6, stroke_color=TEXT, stroke_width=4,
                                fill_color=TEXT, fill_opacity=0.12).move_to([-3.0, 0.9, 0])
        body_l = put(T("transcription\nfactor", 34, TEXT, line_spacing=0.85), -3.0, 0.9)
        foot = Polygon([-3.85, -0.4, 0], [-2.15, -0.4, 0], [-2.4, -1.925, 0], [-3.6, -1.925, 0],
                       stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.35)
        prot = VGroup(body, body_l, foot)
        body2 = RoundedRectangle(corner_radius=0.3, width=2.4, height=1.0, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.12).move_to([3.6, -0.35, 0])
        body2_l = put(T("other", 28, GREY), 3.6, -0.35)
        foot2 = Polygon([3.15, -0.85, 0], [4.05, -0.85, 0], [3.95, -1.925, 0], [3.25, -1.925, 0],
                        stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.3)
        other = VGroup(body2, body2_l, foot2)
        head = put(T("mostly homeodomain transcription factors", 36, TEXT, weight=BOLD), 0, 3.2)
        hd = put(T("homeodomain", 30, TEXT, weight=BOLD), -1.9, -1.15, LEFT)
        ar = arr([-0.2, 1.3, 0], [0.9, 1.3, 0], GREY, 5)
        idt = chip("cell identity", TEXT, 38).move_to([2.9, 1.3, 0])
        self.play(GrowFromEdge(dna, LEFT), FadeIn(dna_l), run_time=1.0)
        self.at("transcription factors")
        self.play(FadeIn(prot, shift=DOWN * 1.1), run_time=0.9)
        self.at("mostly")
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(other, shift=DOWN * 0.5), run_time=0.35)
        self.at("homeodomain proteins")
        self.play(FadeIn(hd, shift=LEFT * 0.15), Indicate(foot, color=TEXT, scale_factor=1.15), run_time=0.9)
        self.at("cell identity")
        self.play(GrowArrow(ar), FadeIn(idt, shift=LEFT * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Sort(SpokenScene):
    def construct(self):
        card = RoundedRectangle(corner_radius=0.25, width=11.6, height=6.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.07).move_to([0, 0, 0])
        year = put(T("2000", 110, GOLD, font=TITLE_FONT), 0, 2.0)
        rule = Line([-2.6, 1.15, 0], [2.6, 1.15, 0], color=GOLD, stroke_width=3)
        order = ("Briscoe", "Jessell", "Pierani", "Ericson")
        ys = (0.35, -0.5, -1.35, -2.2)
        slots = VGroup(*[Line([-5.0, y - 0.38, 0], [-1.7, y - 0.38, 0], color=GREY, stroke_width=2, stroke_opacity=0.55) for y in ys])
        names = {n: put(T(n, 48, TEXT, font=TITLE_FONT), -5.0, y, LEFT) for n, y in zip(order, ys)}
        brk = VGroup(Line([-1.35, ys[0] + 0.3, 0], [-1.35, ys[3] - 0.3, 0], color=GREY, stroke_width=5),
                     Line([-1.35, ys[0] + 0.3, 0], [-1.55, ys[0] + 0.3, 0], color=GREY, stroke_width=5),
                     Line([-1.35, ys[3] - 0.3, 0], [-1.55, ys[3] - 0.3, 0], color=GREY, stroke_width=5),
                     Line([-1.35, (ys[0] + ys[3]) / 2, 0], [-1.0, (ys[0] + ys[3]) / 2, 0], color=GREY, stroke_width=5))
        sorted_t = put(T("sorted them in", 38, GREY), 3.2, -0.2)
        chick = chip("chick", TEXT, 72).move_to([3.2, -1.35, 0])
        self.add(card, year, rule, slots)
        self.at("james briscoe")
        self.play(FadeIn(names["Briscoe"], shift=RIGHT * 0.15), run_time=0.4)
        self.at("thomas jessel")
        self.play(FadeIn(names["Jessell"], shift=RIGHT * 0.15), run_time=0.4)
        self.at("colleagues")
        self.play(FadeIn(names["Pierani"], shift=RIGHT * 0.15), FadeIn(names["Ericson"], shift=RIGHT * 0.15), run_time=0.5)
        self.at("sorted them")
        self.play(Create(brk), FadeIn(sorted_t, shift=UP * 0.1), run_time=0.5)
        self.at("in chick")
        self.play(FadeIn(chick, scale=0.8), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def case_card(kind):
    """kind 'off' or 'on': a button card with the little diagram and its words."""
    cx = -3.3 if kind == "off" else 3.3
    frame = RoundedRectangle(corner_radius=0.25, width=5.9, height=3.4, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.08).move_to([cx, -0.9, 0])
    s = chip("Shh", YELLOW, 32).move_to([cx - 1.9, -0.35, 0])
    f = chip("factor", TEXT, 32).move_to([cx + 1.7, -0.35, 0])
    if kind == "off":
        link = inhib([cx - 1.25, -0.35, 0], [cx + 0.75, -0.35, 0], RED)
        words = T("Shh switches it off", 32, TEXT)
    else:
        link = arr([cx - 1.25, -0.35, 0], [cx + 0.75, -0.35, 0], YELLOW, 6)
        words = T("Shh switches it on", 32, TEXT)
    put(words, cx, -1.85)
    return VGroup(frame, s, link, f, words)


class S05Sort2(SpokenScene):
    def construct(self):
        s = chip("Shh", YELLOW, 44).move_to([-2.6, 0.3, 0])
        q = put(T("?", 72, TEXT, weight=BOLD), 0.0, 0.3)
        f = chip("factor", TEXT, 44).move_to([2.6, 0.3, 0])
        offc, onc = case_card("off"), case_card("on")
        self.play(FadeIn(s), FadeIn(f), run_time=0.6)
        self.at("one question")
        self.play(FadeIn(q, scale=0.6), run_time=0.5)
        self.at("does sonic")
        self.play(Indicate(s, color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.at("switch the factor off")
        row = VGroup(s, q, f)
        self.play(row.animate.shift(UP * 2.0), FadeIn(offc, shift=UP * 0.2), run_time=0.8)
        self.at("or switch it on")
        self.play(FadeIn(onc, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06C1(SpokenScene):
    def construct(self):
        base, wall, axis, area, crv, bl, xl = base_stage(self)
        s, link, c = class_legend(1)
        self.add(c)
        its = items(CLS1, labels=False)
        # carry: the tube and slope are already up; the legend's class chip too
        self.play(Indicate(crv, color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("switched off")
        self.play(FadeIn(s, shift=RIGHT * 0.2), Create(link), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(its[n]["dot"], scale=0.5), Create(its[n]["line"])) for n in reversed(CLS1)],
                              lag_ratio=0.12), run_time=0.7)
        self.play(LaggedStart(*[GrowFromEdge(its[n]["bar"], UP) for n in CLS1], lag_ratio=0.2), run_time=1.5)
        ghosts = VGroup(*[Rectangle(width=BAR_W, height=BARS[n][2] - Y0, stroke_color=CI, stroke_width=2, stroke_opacity=0.4,
                                    fill_color=CI, fill_opacity=0.05).move_to([BARS[n][0], (BARS[n][2] + Y0) / 2, 0]) for n in CLS1])
        exp_t = put(T("expressed above", 28, CI), 5.0, 1.6)
        lost_t = put(T("lost below", 28, RED), 5.0, -0.6)
        self.at("expressed above")
        self.play(FadeIn(exp_t, shift=DOWN * 0.1), run_time=0.5)
        self.at("lost below it")
        self.play(FadeIn(ghosts), FadeIn(lost_t, shift=DOWN * 0.1), run_time=0.8)
        self.finish()


def class1_state(scene, labels=True, k=1.0):
    base, wall, axis, area, crv, bl, xl = base_stage(scene)
    s, link, c = class_legend(1)
    its = items(CLS1, k=k, labels=labels)
    scene.add(s, link, c, *flat(its))
    return base, wall, crv, its, (s, link, c)


class S07C1b(SpokenScene):
    def construct(self):
        base, wall, crv, its, leg = class1_state(self, labels=False)
        cues = {"Pax7": "pac 7", "Dbx1": "dbx1", "Dbx2": "and 2", "Irx3": "irx3", "Pax6": "pac 6"}
        for n in CLS1:
            self.at(cues[n])
            lab = bar_label(n)
            self.play(FadeIn(lab, shift=DOWN * 0.1), Indicate(its[n]["bar"], color=CI, scale_factor=1.0), run_time=0.6)
        self.finish()


class S08C1c(SpokenScene):
    def construct(self):
        base, wall, crv, its, leg = class1_state(self, labels=True)
        ax = 4.95
        up = arr([ax, -1.8, 0], [ax, 0.6, 0], YELLOW, 6)
        up_l = T("more sensitive", 28, YELLOW).move_to([ax, 1.55, 0])
        up_l2 = T("lost at lower Shh", 26, YELLOW).move_to([ax, 1.1, 0])
        self.at("the more sensitive")
        self.play(GrowArrow(up), FadeIn(up_l), FadeIn(up_l2), run_time=0.8)
        self.at("higher its border")
        self.play(LaggedStart(*[Indicate(its[n]["line"], color=YELLOW, scale_factor=1.0) for n in reversed(CLS1)], lag_ratio=0.25), run_time=1.6)
        others = [m for n in CLS1[1:] for m in (its[n]["bar"], its[n]["line"], its[n]["dot"], its[n]["label"])]
        lc = wall[int(np.argmin(np.abs(WALL_YS - 0.6)))]
        up_cells = [cl for cl, y in zip(wall, WALL_YS) if y > 0.6]
        brk = VGroup(Line([-4.2, 0.62, 0], [-4.2, 2.88, 0], color=CI, stroke_width=6),
                     Line([-4.2, 0.62, 0], [-4.05, 0.62, 0], color=CI, stroke_width=6),
                     Line([-4.2, 2.88, 0], [-4.05, 2.88, 0], color=CI, stroke_width=6),
                     Line([-4.2, 1.75, 0], [-4.05, 1.75, 0], color=CI, stroke_width=6))
        dh = put(T("dorsal half", 32, CI, weight=BOLD), -3.2, 1.75, LEFT)
        self.at("pac 7 is lost")
        self.play(*[m.animate.set_opacity(0.18) for m in others],
                  its["Pax7"]["line"].animate.set_opacity(1.0), Indicate(its["Pax7"]["bar"], color=CI, scale_factor=1.1),
                  Indicate(its["Pax7"]["dot"], color=YELLOW, scale_factor=2.0), Indicate(lc, color=YELLOW, scale_factor=1.2),
                  Create(brk), *[cl.animate.set_stroke(CI).set_fill(CI, 0.45) for cl in up_cells],
                  run_time=1.6)
        self.at("so it stays")
        self.play(FadeIn(dh, shift=RIGHT * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
CLS2 = ("Nkx6.1", "Nkx2.2")


def class2_state(scene, labels=True):
    base, wall, axis, area, crv, bl, xl = base_stage(scene)
    s, link, c = class_legend(2)
    old = items(CLS1, k=0.22, labels=True)
    new = items(CLS2, labels=labels)
    scene.add(*flat(old), s, link, c, *flat(new))
    return base, wall, crv, old, new, (s, link, c), bl


class S09C2(SpokenScene):
    def construct(self):
        base, wall, axis, area, crv, bl, xl = base_stage(self)
        s, link1, c1 = class_legend(1)
        s2, link2, c2 = class_legend(2)
        old = items(CLS1, labels=True)
        self.add(*flat(old), s, link1, c1)
        self.at("class two")
        # the red T-bar leaves first, so Class II is never drawn behind a repression bar
        self.play(FadeOut(link1), run_time=0.2)
        self.play(Transform(c1, c2), *[m.animate.set_opacity(0.22) for m in flat(old)], run_time=0.6)
        self.at("switched on by")
        hi = put(T("high Shh", 26, YELLOW), SLX0 + 0.9, Y0 + 0.3)
        self.play(GrowArrow(link2), FadeIn(hi), Indicate(crv, color=YELLOW, scale_factor=1.0), run_time=0.8)
        new = items(CLS2, labels=False)
        self.at("expressed only")
        self.play(LaggedStart(*[AnimationGroup(FadeIn(new[n]["dot"], scale=0.5), Create(new[n]["line"]), GrowFromEdge(new[n]["bar"], DOWN))
                                for n in CLS2], lag_ratio=0.35), run_time=0.7)
        txt = put(T("expressed only\nbelow the border", 28, ORANGE, line_spacing=0.8), 5.35, 0.6)
        self.at("below a certain")
        self.play(FadeIn(txt, shift=DOWN * 0.1), *[FadeIn(tip_cap(n)) for n in CLS2], run_time=0.8)
        self.finish()


class S10C2b(SpokenScene):
    def construct(self):
        base, wall, crv, old, new, leg, bl = class2_state(self, labels=False)
        self.at("nkx 6 1")
        self.play(FadeIn(bar_label("Nkx6.1"), shift=DOWN * 0.1), Indicate(new["Nkx6.1"]["bar"], color=ORANGE, scale_factor=1.0), run_time=0.6)
        self.at("nkx 2 2")
        self.play(FadeIn(bar_label("Nkx2.2"), shift=DOWN * 0.1), Indicate(new["Nkx2.2"]["bar"], color=ORANGE, scale_factor=1.0), run_time=0.6)
        most = put(T("most signal", 28, YELLOW), -0.1, -2.1)
        pt = arr([-1.2, -2.1, 0], [-1.55, -2.32, 0], YELLOW, 4, 0.14)
        self.at("most signal")
        self.play(FadeIn(most), GrowArrow(pt), Indicate(crv, color=YELLOW, scale_factor=1.0), Indicate(VGroup(*wall[:3]), color=YELLOW, scale_factor=1.1), run_time=0.9)
        fl = put(T("floor plate level", 30, TEAL, weight=BOLD), 3.1, -2.85)
        self.at("so it sits")
        self.play(bl.animate.set_stroke(TEAL, width=6, opacity=1.0), FadeIn(fl), Indicate(base[4], color=TEAL, scale_factor=1.3),
                  Indicate(new["Nkx2.2"]["bar"], color=ORANGE, scale_factor=1.1), run_time=0.9)
        self.finish()


class S11Warn(SpokenScene):
    def construct(self):
        def card(cx, cls):
            col = CI if cls == 1 else ORANGE
            frame = RoundedRectangle(corner_radius=0.3, width=5.9, height=5.0, stroke_color=col, stroke_width=3,
                                     fill_color=col, fill_opacity=0.07).move_to([cx, -0.55, 0])
            c = chip("Class I" if cls == 1 else "Class II", col, 44).move_to([cx, 1.3, 0])
            sh = chip("Shh", YELLOW, 40).move_to([cx, -1.15, 0])
            if cls == 1:
                lk = inhib([cx, -0.6, 0], [cx, 0.8, 0], RED, 7)
                words = T("Shh represses", 38, TEXT)
            else:
                lk = arr([cx, -0.6, 0], [cx, 0.8, 0], YELLOW, 8, 0.3)
                words = T("Shh induces", 38, TEXT)
            put(words, cx, -2.2)
            return frame, c, sh, lk, words
        f1, c1, sh1, lk1, w1 = card(-3.3, 1)
        f2, c2, sh2, lk2, w2 = card(3.3, 2)
        ring = Triangle(color=GOLD, stroke_width=7).scale(0.75).move_to([0, 3.0, 0])
        warn = put(T("!", 56, GOLD, weight=BOLD), 0.0, 2.95)
        self.play(FadeIn(f1), FadeIn(f2), Create(ring), FadeIn(warn), FadeIn(c1, scale=0.8), FadeIn(c2, scale=0.8), run_time=0.8)
        self.at("class 1 proteins")
        self.play(Indicate(c1, color=CI, scale_factor=1.15), FadeIn(sh1, shift=UP * 0.1), Create(lk1), run_time=0.9)
        self.play(FadeIn(sh2, shift=UP * 0.1), GrowArrow(lk2), run_time=0.7)
        self.at("represses")
        self.play(FadeIn(w1, shift=UP * 0.1), run_time=0.5)
        self.wait(0.2)
        self.play(FadeIn(w2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def full_stage(scene, olig=False, labels=True):
    base, wall, axis, area, crv, bl, xl = base_stage(scene)
    its = items(CLS1 + CLS2, labels=labels)
    scene.add(*flat(its))
    return base, wall, crv, its, bl


class S12Stagger(SpokenScene):
    def construct(self):
        base, wall, crv, its, bl = full_stage(self)
        lines = VGroup(*[thr_line(n, 0.5, full=True) for n in ("Pax7", "Dbx1", "Dbx2", "Irx3", "Pax6")])
        self.at("each border")
        self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.3), run_time=1.6)
        self.at("dbx1's among")
        self.play(Indicate(VGroup(its["Dbx1"]["bar"], its["Dbx1"]["label"]), color=CI, scale_factor=1.12),
                  Indicate(lines[1], color=YELLOW, scale_factor=1.0), run_time=1.0)
        band = Rectangle(width=BARS_R + 6.2, height=0.6, stroke_width=0, fill_color=TEXT, fill_opacity=0.14).move_to([(-6.2 + BARS_R) / 2, -0.9, 0])
        band.set_z_index(-2)
        wall_box = Rectangle(width=1.0, height=0.6, stroke_color=TEXT, stroke_width=4).move_to([WX, -0.9, 0])
        tag = put(T("one stretch", 28, TEXT, weight=BOLD), -0.95, -0.9)
        self.at("stretch between two borders")
        self.play(FadeIn(band), Create(wall_box), FadeIn(tag), run_time=0.7)
        rings = VGroup(*[Circle(radius=0.3, stroke_color=CLS_COL[BARS[n][1]], stroke_width=4).move_to([BARS[n][0], -0.9, 0])
                         for n in ("Irx3", "Pax6", "Nkx6.1")])
        comb = chip("combination", TEXT, 24, pad=0.16).move_to([5.6, -0.93, 0])
        self.at("combination of factors")
        self.play(LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.3), FadeIn(comb, shift=LEFT * 0.2), run_time=1.0)
        addr = chip("address", GOLD, 36, pad=0.2).move_to([5.65, -0.93, 0])
        self.at("the cell's")
        self.play(Transform(comb, addr), Indicate(tag, color=GOLD, scale_factor=1.1), run_time=0.7)
        self.finish()


class S13Olig(SpokenScene):
    def construct(self):
        base, wall, crv, its, bl = full_stage(self)
        lines = VGroup(*[thr_line(n, 0.5, full=True) for n in ("Pax7", "Dbx1", "Dbx2", "Irx3", "Pax6")])
        self.add(lines)
        OX = BARS["Olig2"][0]
        ph = Rectangle(width=BAR_W, height=0.6, stroke_color=GREEN, stroke_width=3, stroke_opacity=0.8, fill_opacity=0).move_to([OX, -1.5, 0])
        q = put(T("?", 26, GREEN, weight=BOLD), OX, -1.5)
        self.at("one more")
        self.play(Create(ph), FadeIn(q), run_time=0.6)
        ob = make_bar("Olig2")
        ol = bar_label("Olig2", 26, weight=BOLD)
        self.at("olig 2")
        self.play(ReplacementTransform(ph, ob), FadeOut(q), FadeIn(ol, shift=DOWN * 0.1), run_time=0.8)
        tag = put(T("bHLH protein", 26, GREEN), OX - 0.6, -2.95)
        leader = Line([OX, -1.85, 0], [OX, -2.75, 0], color=GREEN, stroke_width=3)
        self.at("different kind of protein")
        self.play(FadeIn(tag, shift=UP * 0.1), Create(leader), run_time=0.6)
        sh = chip("Shh", YELLOW, 26).move_to([OX, 1.3, 0])
        ar = arr([OX, 0.95, 0], [OX, -0.58, 0], YELLOW, 5, 0.2)
        self.at("sonic hedgehog also induces")
        self.play(FadeIn(sh, shift=DOWN * 0.2), GrowArrow(ar), run_time=0.7)
        band = Rectangle(width=BARS_R + 4.4, height=0.6, stroke_width=0, fill_color=GREEN, fill_opacity=0.2).move_to([(-4.4 + BARS_R) / 2, -1.5, 0])
        band.set_z_index(-2)
        mn = put(T("motor neuron progenitors", 26, GREEN), OX - 1.6, -3.45)
        self.at("motor neuron progenitors")
        self.play(FadeIn(band), FadeIn(mn), Indicate(ob, color=GREEN, scale_factor=1.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S14Predict(SpokenScene):
    def construct(self):
        head, rowl, cg, cells, sep = build_table()
        simp = simp_tag()
        self.add(sep, head, rowl, cg, simp)     # the table is already up at the cut
        b3 = row_box("p3", ORANGE)
        bm = row_box("pMN", GREEN)
        self.at("p3 row")
        self.play(Create(b3), run_time=0.7)
        self.at("pmn row")
        self.play(Create(bm), run_time=0.7)
        q = question_text()
        self.at("which markers differ")
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S15Pause(NarratedScene):
    def construct(self):
        head, rowl, cg, cells, sep = build_table()
        b3, bm = row_box("p3", ORANGE), row_box("pMN", GREEN)
        self.add(sep, head, rowl, cg, b3, bm, question_text(), simp_tag())
        for _ in range(2):
            self.play(b3.animate.set_fill(ORANGE, 0.16), bm.animate.set_fill(GREEN, 0.16), run_time=1.0, rate_func=smooth)
            self.play(b3.animate.set_fill(ORANGE, 0.0), bm.animate.set_fill(GREEN, 0.0), run_time=1.0, rate_func=smooth)
        self.finish()


class S16Reveal(SpokenScene):
    def construct(self):
        head, rowl, cg, cells, sep = build_table()
        self.add(sep, head, rowl, cg, row_box("p3", ORANGE), row_box("pMN", GREEN), simp_tag())
        self.play(Indicate(rowl[3], color=GREEN, scale_factor=1.3), run_time=0.7)
        r_p3 = cell_ring("p3", 6, ORANGE)
        r_mn = cell_ring("pMN", 6, ORANGE)
        self.at("lacks")
        self.play(GrowFromCenter(r_p3), GrowFromCenter(r_mn), run_time=0.7)
        note = put(T("needs the most signal", 28, YELLOW), 2.7, -2.75)
        ln = Line([TB_X[6], -2.13, 0], [TB_X[6], -2.45, 0], color=YELLOW, stroke_width=3)
        self.at("needs the most signal")
        self.play(FadeIn(note, shift=UP * 0.1), Create(ln), run_time=0.7)
        r1 = cell_ring("pMN", 5, GREEN)
        self.at("it has")
        self.play(FadeOut(r_p3), FadeOut(r_mn), FadeOut(note), FadeOut(ln), run_time=0.4)
        self.at("olig 2")
        self.play(GrowFromCenter(r1), run_time=0.6)
        r2 = low_ring("pMN", CI)
        self.at("a little")
        self.play(GrowFromCenter(r2), run_time=0.6)
        self.finish()


class S17Reveal2(SpokenScene):
    def construct(self):
        head, rowl, cg, cells, sep = build_table()
        bm = row_box("pMN", GREEN)
        rings = [cell_ring("pMN", 5, GREEN), low_ring("pMN", CI)]
        self.add(sep, head, rowl, cg, bm, simp_tag(), *rings)
        self.at("combination")
        self.play(bm.animate.set_fill(GREEN, 0.22), run_time=0.8)
        lab = put(T("motor neuron\nprogenitors", 24, GREEN, line_spacing=0.8), 4.85, TB_Y[3], LEFT)
        self.at("motor neuron progenitors")
        self.play(FadeIn(lab, shift=LEFT * 0.2), run_time=0.7)
        self.at("called pmn")
        self.play(Indicate(rowl[3], color=GREEN, scale_factor=1.4), run_time=0.9)
        self.finish()


class S18Reveal3(SpokenScene):
    def construct(self):
        head, rowl, cg, cells, sep = build_table()
        bm = row_box("pMN", GREEN, 0.22)
        self.add(sep, head, rowl, cg, bm, simp_tag())
        self.at("pmn with")
        self.play(Indicate(rowl[3], color=GREEN, scale_factor=1.3), run_time=0.6)
        b2 = row_box("p2", TEXT)
        self.at("p2 above it")
        self.play(Create(b2), run_time=0.7)
        o1, o2 = cell_ring("p2", 5, GREEN), cell_ring("pMN", 5, GREEN)
        self.at("lacks olig2")
        self.play(GrowFromCenter(o1), GrowFromCenter(o2), run_time=0.8)
        i1, i2 = cell_ring("p2", 2, CI), cell_ring("pMN", 2, CI)
        self.at("has irx3")
        self.play(GrowFromCenter(i1), GrowFromCenter(i2), run_time=0.8)
        self.finish()


class S18bRows(SpokenScene):
    def construct(self):
        head, rowl, cg, cells, sep = build_table()
        b2, bm = row_box("p2", TEXT), row_box("pMN", GREEN, 0.15)
        self.add(sep, head, rowl, cg, b2, bm, simp_tag(), cell_ring("p2", 2, CI), cell_ring("pMN", 2, CI),
                 cell_ring("p2", 5, GREEN), cell_ring("pMN", 5, GREEN))
        ya, yb = TB_Y[2], TB_Y[3]
        brk = VGroup(Line([4.75, ya + 0.35, 0], [4.75, yb - 0.35, 0], color=TEXT, stroke_width=6),
                     Line([4.75, ya + 0.35, 0], [4.55, ya + 0.35, 0], color=TEXT, stroke_width=6),
                     Line([4.75, yb - 0.35, 0], [4.55, yb - 0.35, 0], color=TEXT, stroke_width=6))
        cap = put(T("neighbouring domains compared", 34, TEXT), -0.9, -2.75)
        self.at("neighboring domains")
        self.play(Create(brk), FadeIn(cap, shift=UP * 0.1), run_time=0.9)
        # a single cell climbing the table: drawn, then crossed out
        cell = RoundedRectangle(corner_radius=0.12, width=1.3, height=0.9, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.3).move_to([5.9, -1.9, 0])
        up = arr([5.9, -1.3, 0], [5.9, 1.4, 0], TEXT, 6, 0.3)
        cross = VGroup(Line([5.1, -1.35, 0], [6.7, -2.45, 0], color=TEXT, stroke_width=9),
                       Line([5.1, -2.45, 0], [6.7, -1.35, 0], color=TEXT, stroke_width=9))
        cap2 = put(T("not one cell moving", 34, TEXT), -0.9, -3.4)
        self.at("show a cell")
        self.play(FadeIn(cell), GrowArrow(up), FadeIn(cap2, shift=UP * 0.1), run_time=0.8)
        self.at("changing")
        self.play(Create(cross), run_time=0.5)
        self.finish()
        self.wait(0.7)


class S19Pair(SpokenScene):
    def construct(self):
        head, rowl, cg, cells, sep = build_table()
        # carried from the end of the previous scene: the two compared rows and their marked cells
        carry = VGroup(row_box("p2", TEXT), row_box("pMN", GREEN, 0.15), cell_ring("p2", 2, CI), cell_ring("pMN", 2, CI),
                       cell_ring("p2", 5, GREEN), cell_ring("pMN", 5, GREEN))
        self.add(sep, head, rowl, cg, simp_tag(), carry)
        y_lo = (TB_Y[3] + TB_Y[4]) / 2
        y_up = (TB_Y[2] + TB_Y[3]) / 2
        l_lo = DashedLine([TB_L, y_lo, 0], [4.9, y_lo, 0], color=TEXT, stroke_width=3.5, dash_length=0.15)
        l_up = DashedLine([TB_L, y_up, 0], [4.9, y_up, 0], color=TEXT, stroke_width=3.5, dash_length=0.15)
        self.play(FadeOut(carry), Create(l_up), Create(l_lo), run_time=0.7)
        self.play(Indicate(l_up, color=YELLOW, scale_factor=1.0), Indicate(l_lo, color=YELLOW, scale_factor=1.0), run_time=1.0)
        lo = VGroup(RoundedRectangle(corner_radius=0.12, width=1.2, height=1.75, stroke_color=CI, stroke_width=4).move_to([TB_X[3], (TB_Y[3] + TB_Y[4]) / 2, 0]),
                    RoundedRectangle(corner_radius=0.12, width=0.9, height=1.75, stroke_color=ORANGE, stroke_width=4).move_to([TB_X[6], (TB_Y[3] + TB_Y[4]) / 2, 0]))
        up = VGroup(RoundedRectangle(corner_radius=0.12, width=0.9, height=1.75, stroke_color=CI, stroke_width=4).move_to([TB_X[2], (TB_Y[2] + TB_Y[3]) / 2, 0]),
                    RoundedRectangle(corner_radius=0.12, width=0.9, height=1.75, stroke_color=GREEN, stroke_width=4).move_to([TB_X[5], (TB_Y[2] + TB_Y[3]) / 2, 0]))
        lab_lo = VGroup(T("Nkx2.2", 28, ORANGE), T("Pax6", 28, CI)).arrange(DOWN, buff=0.12).move_to([5.75, y_lo - 0.3, 0])
        lab_up = VGroup(T("Olig2", 28, GREEN), T("Irx3", 28, CI)).arrange(DOWN, buff=0.12).move_to([5.75, y_up + 0.3, 0])
        self.at("pair of factors")
        self.play(Create(lo), FadeIn(lab_lo), run_time=0.6)
        self.at("trades places")
        self.play(Create(up), FadeIn(lab_up), run_time=0.6)
        tag = chip("chapter 5", GOLD, 32).move_to([-0.9, -2.9, 0])
        self.at("chapter 5")
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S20Fill(SpokenScene):
    def construct(self):
        base, dors, st, slots, labs, zl = fill_stage(self)
        self.play(FadeIn(base), FadeIn(dors), FadeIn(VGroup(*st.values())), FadeIn(zl),
                  FadeIn(VGroup(*slots.values())), run_time=0.9)
        self.at("five slots")
        self.play(LaggedStart(*[Indicate(slots[n], color=GOLD, scale_factor=1.03) for n in PY], lag_ratio=0.2), run_time=1.3)
        for n, cue in (("p0", "p0"), ("p1", "p1"), ("p2", "and p2")):
            self.at(cue)
            self.play(FadeIn(labs[n], shift=RIGHT * 0.15), run_time=0.3)
        for n, cue in (("p0", "make v0"), ("p1", "v1"), ("p2", "v2")):
            self.at(cue)
            self.play(slot_anim(slots[n], n), slot_anim(st[n], n), FadeIn(panel_out(n), shift=RIGHT * 0.15), run_time=0.6)
        self.finish()


class S21Fill2(SpokenScene):
    def construct(self):
        filled = ("p0", "p1", "p2")
        base, dors, st, slots, labs, zl = fill_stage(self, filled)
        for n in filled:
            fill_slot(st[n], n)
        self.add(base, dors, VGroup(*st.values()), zl, VGroup(*slots.values()), *[labs[n] for n in filled], *[panel_out(n) for n in filled])
        self.at("pmn makes")
        self.play(FadeIn(labs["pMN"], shift=RIGHT * 0.15), run_time=0.3)
        self.at("motor neurons")
        self.play(slot_anim(slots["pMN"], "pMN"), slot_anim(st["pMN"], "pMN"), FadeIn(panel_out("pMN"), shift=RIGHT * 0.15), run_time=0.7)
        self.at("p3")
        self.play(FadeIn(labs["p3"], shift=RIGHT * 0.15), run_time=0.3)
        fpb, fpl = fp_band()
        self.at("beside the floor plate")
        self.play(FadeIn(fpb, shift=UP * 0.15), FadeIn(fpl), Indicate(base[4], color=TEAL, scale_factor=1.3), run_time=0.7)
        self.at("v3")
        self.play(slot_anim(slots["p3"], "p3"), slot_anim(st["p3"], "p3"), FadeIn(panel_out("p3"), shift=RIGHT * 0.15), run_time=0.7)
        self.finish()


class S22Markers(SpokenScene):
    def construct(self):
        base = tube_base()
        dors, st = wall_stripes(filled=tuple(SLOTS))
        axis, area, crv = slope_parts()
        bl, xl = baseline(), slope_label()
        its = items(CLS1 + CLS2 + ("Olig2",))
        self.add(base, dors, VGroup(*st.values()), area, axis, crv, bl, xl, *flat(its))
        marks = ("Pax7", "Olig2", "Nkx2.2")
        rest = [m for n in its if n not in marks for m in (its[n]["bar"], its[n]["line"], its[n]["dot"], its[n]["label"])]
        self.at("three markers")
        self.play(*[m.animate.set_opacity(0.2) for m in rest], run_time=0.8)
        specs = [("Pax7", "pac7", dors, "dorsal"), ("Olig2", "olig 2", st["pMN"], "pMN"), ("Nkx2.2", "nkx 2 2", st["p3"], "p3")]
        for n, cue, wr, sn in specs:
            self.at(cue)
            x, cls, b = BARS[n]
            bigl = put(T(n, 30, CLS_COL[cls], weight=BOLD), *label_pos(n))
            if sn == "dorsal":
                wanim = wr.animate.set_stroke(CI, opacity=0.95).set_fill(CI, 0.5)
            else:
                wanim = slot_anim(wr, sn, 0.7)
            self.play(wanim, Transform(its[n]["label"], bigl), Indicate(its[n]["bar"], color=CLS_COL[cls], scale_factor=1.15),
                      Flash(its[n]["bar"], color=CLS_COL[cls], flash_radius=0.5, line_length=0.2, num_lines=8, run_time=0.7), run_time=0.7)
        self.finish()


class S23Takeaway(SpokenScene):
    def construct(self):
        base = tube_base()
        wall = wall_cells(shaded=True)
        box = RoundedRectangle(corner_radius=0.08, width=0.95, height=0.56, stroke_color=GREEN, stroke_width=4).move_to([WX, -1.5, 0])
        plab = put(T("pMN", 36, GREEN, weight=BOLD), -3.55, -1.5)
        tk = put(T("The takeaway", 36, GOLD, weight=BOLD), 2.4, 3.4)
        self.play(FadeIn(base), FadeIn(wall), FadeIn(tk), run_time=0.5)
        cx = 2.4
        lvl = chip("level of signal", YELLOW, 52).move_to([cx, 2.35, 0])
        ar1 = arr([cx, 1.7, 0], [cx, 0.95, 0], GREY, 7, 0.28)
        adr = chip("address", GOLD, 56).move_to([cx, 0.2, 0])
        self.at("a level of signal")
        self.play(FadeIn(lvl, shift=DOWN * 0.2), run_time=0.7)
        self.at("becomes an address")
        self.play(GrowArrow(ar1), FadeIn(adr, shift=DOWN * 0.2), Create(box), FadeIn(plab), run_time=0.9)
        chips = VGroup(chip("Nkx6.1", ORANGE, 38), chip("Olig2", GREEN, 38), chip("Pax6 low", CI, 38)).arrange(RIGHT, buff=0.25).move_to([cx + 0.2, -1.5, 0])
        conn = DashedLine([-2.95, -1.5, 0], [chips.get_left()[0] - 0.1, -1.5, 0], color=GREEN, stroke_width=3, dash_length=0.15)
        down = arr([cx, -0.5, 0], [cx, -0.95, 0], GOLD, 6, 0.2)
        words = put(T("a combination of factors", 42, TEXT), cx, -2.75)
        self.at("combination of")
        self.play(GrowArrow(down), Create(conn), LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.25), run_time=1.1)
        self.play(FadeIn(words, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S24End(EndCard):
    LINE = "A level of signal becomes an address, a combination of factors."
