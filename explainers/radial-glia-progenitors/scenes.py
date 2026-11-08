"""One Cell Across the Wall  (chapter 1 of the radial glia film series), fix-round version

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, shared by every chapter of this lesson; taken from scenes.old.py)
  BLUE   = the radial glial / neuroepithelial cell (body and fibre); also a progenitor
  YELLOW = the nucleus (the thing that moves); it glows yellow while it copies its DNA
  TEAL   = mitosis (a cell caught dividing); also the "later lessons" chips
  GREEN  = a neuron
  RED    = the open question (puzzle cards, "?")
  GREY   = ventricle edge, pia, de-emphasised text, a spent daughter (LBL is a brighter grey for labels)
  TEXT   = neutral white (definitions, headers, glial marker chips)
  FLUID  = the ventricle's fluid (a slate blue, kept apart from the cell blue)
  GOLD   = the one highlight (the idea card, the takeaway)
  (PURPLE kinesin, ORANGE dynein, PINK actomyosin are used in chapter 2, not here)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB4"
FLUID = "#5B86B5"
LBL = "#C6CCD8"        # bright grey for labels on the dark ground
NUC = "#AEB8C6"        # a resting nucleus (grey-blue), before it copies its DNA

# the wall: strip x range and band edges (y), ventricle at the bottom, pia at the top
X0, X1 = -4.1, 2.5
Y_V0, Y_V1 = -3.7, -3.1      # ventricle band
Y_VZ, Y_SVZ, Y_IZ, Y_CP = -1.7, -0.9, 0.8, 2.7
Y_PIA, Y_BM = 3.0, 2.78
CELL_X = -2.9
LABEL_X = 2.8                 # left edge of the zone labels
PANEL_X = 4.8                 # centre of the right-hand panel in the wall scenes


# ---------------------------------------------------------------- helpers
def rect(x0, x1, y0, y1, color, op, stroke=0, stroke_op=1.0):
    r = Rectangle(width=x1 - x0, height=y1 - y0, stroke_width=stroke, stroke_color=color,
                  fill_color=color, fill_opacity=op)
    if stroke:
        r.set_stroke(color, stroke, opacity=stroke_op)
    return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def tag(text, color=TEXT, size=26, **kw):
    """Text on a dark backing so faint tissue lines never run through it."""
    t = T(text, size, color, **kw)
    back = RoundedRectangle(corner_radius=0.08, width=t.width + 0.22, height=t.height + 0.18, stroke_width=0,
                            fill_color=BG, fill_opacity=0.94).move_to(t)
    return VGroup(back, t)


def left_at(mob, x, y):
    """Put mob so its left edge is at x, centred on y."""
    return mob.move_to([x + mob.width / 2, y, 0])


def circ(x, y, r, color=BLUE, op=0.3, sw=3):
    return Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op).move_to([x, y, 0])


def sq(x, y, s=0.9, color=TEXT, op=0.15):
    return RoundedRectangle(corner_radius=0.12, width=s, height=s, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def arr(a, b, color=GREY, w=4, tip=0.2):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def check(x, y, s=0.32, color=GREEN):
    c = VMobject(stroke_color=color, stroke_width=9)
    c.set_points_as_corners([[x - s, y, 0], [x - s * 0.35, y - s * 0.7, 0], [x + s, y + s * 0.8, 0]])
    return c


def not_equal(x, y, s=0.38, color=TEXT):
    return VGroup(Line([x - s, y + 0.13, 0], [x + s, y + 0.13, 0], stroke_color=color, stroke_width=7),
                  Line([x - s, y - 0.13, 0], [x + s, y - 0.13, 0], stroke_color=color, stroke_width=7),
                  Line([x - 0.2, y - 0.4, 0], [x + 0.2, y + 0.4, 0], stroke_color=color, stroke_width=7))


def dashed(mob, n=40):
    return DashedVMobject(mob, num_dashes=n)


def leader(a, b, color=LBL, w=3):
    return Line(a, b, stroke_color=color, stroke_width=w)


def callout(text, anchor, x, y, color=BLUE, size=28, lead=None, sub=None):
    """A label whose left edge is at (x, y) with a leader line back to `anchor`."""
    t = T(text, size, color)
    if sub:
        t = VGroup(t, T(sub, 24, LBL)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    back = RoundedRectangle(corner_radius=0.08, width=t.width + 0.22, height=t.height + 0.18, stroke_width=0,
                            fill_color=BG, fill_opacity=0.94).move_to(t)
    g = VGroup(back, t)
    left_at(g, x, y)
    ln = leader(anchor, [x, y, 0], color if lead is None else lead)
    return VGroup(ln, g)


def card_frame(cx, cy, w, h, color=GREY, op=0.55, fill=False):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            stroke_opacity=op, fill_color=BG, fill_opacity=0.9 if fill else 0).move_to([cx, cy, 0])


class RGCell(VGroup):
    """The radial glial cell: apical foot, soma, long fibre, basal foot (a cartoon, no structure)."""

    def __init__(self, x=CELL_X, y0=Y_V1, y1=2.74, ys=-2.4, k=1.0, color=BLUE, soma_h=1.15):
        sh = soma_h * k
        afoot = Polygon([x - 0.32 * k, y0, 0], [x + 0.32 * k, y0, 0], [x + 0.12 * k, y0 + 0.3 * k, 0],
                        [x - 0.12 * k, y0 + 0.3 * k, 0], stroke_width=0, fill_color=color, fill_opacity=0.85)
        soma = RoundedRectangle(corner_radius=0.45 * k, width=1.15 * k, height=sh, stroke_color=color,
                                stroke_width=3, fill_color=color, fill_opacity=0.35).move_to([x, ys, 0])
        top = ys + sh / 2
        fibre = Line([x, top, 0], [x, y1 - 0.3 * k, 0], stroke_color=color, stroke_width=8)
        glow = Line([x, top, 0], [x, y1 - 0.3 * k, 0], stroke_color=color, stroke_width=24, stroke_opacity=0.28)
        bfoot = Polygon([x - 0.12 * k, y1 - 0.3 * k, 0], [x + 0.12 * k, y1 - 0.3 * k, 0],
                        [x + 0.32 * k, y1, 0], [x - 0.32 * k, y1, 0], stroke_width=0,
                        fill_color=color, fill_opacity=0.85)
        super().__init__(glow, fibre, soma, afoot, bfoot)
        self.glow, self.fibre, self.soma, self.afoot, self.bfoot = glow, fibre, soma, afoot, bfoot


# ---- wall pieces
def tissue_bg():
    return rect(X0, X1, Y_V1, Y_CP, GREY, 0.14, stroke=3, stroke_op=0.8)


def fibres():
    """The neighbouring cells, drawn very faintly so the one lit cell stands out."""
    g = VGroup()
    for i in range(14):
        x = -3.8 + 0.45 * i
        if abs(x - CELL_X) < 0.2:
            continue
        g.add(Line([x, Y_V1, 0], [x, Y_CP, 0], stroke_color=GREY, stroke_width=2.5, stroke_opacity=0.26))
    return g


def fluid_band():
    band = rect(X0, X1, Y_V0, Y_V1, FLUID, 0.5)
    lab = T("ventricle", 26, TEXT).move_to(band)
    return VGroup(band, lab)


def pia_bars():
    pia = rect(X0 - 0.2, X1 + 0.2, Y_PIA - 0.07, Y_PIA + 0.07, LBL, 0.85)
    bm = Line([X0 - 0.2, Y_BM, 0], [X1 + 0.2, Y_BM, 0], stroke_color=LBL, stroke_width=3)
    return VGroup(pia, bm)


def pia_labels():
    """'pia' and 'basement membrane' each with a leader to its own bar."""
    p = left_at(T("pia", 28, LBL), LABEL_X + 0.15, 3.42)
    pl = leader([X1 + 0.22, Y_PIA + 0.02, 0], [LABEL_X + 0.1, 3.36, 0])
    b = left_at(T("basement membrane", 26, LBL), LABEL_X + 0.3, Y_BM)
    bl = leader([X1 + 0.22, Y_BM, 0], [LABEL_X + 0.25, Y_BM, 0])
    return VGroup(p, pl, b, bl)


ZNAMES = ["ventricular zone (VZ)", "subventricular zone (SVZ)", "intermediate zone", "cortical plate"]
ZSPEC = [(Y_V1, Y_VZ, BLUE, 0.30, BLUE), (Y_VZ, Y_SVZ, GREY, 0.14, LBL),
         (Y_SVZ, Y_IZ, GREY, 0.30, LBL), (Y_IZ, Y_CP, GREY, 0.18, LBL)]


def zone_band(i):
    y0, y1, col, op, _ = ZSPEC[i]
    return rect(X0, X1, y0, y1, col, op)


def zone_label(i):
    y0, y1, _, _, lc = ZSPEC[i]
    t = fit(T(ZNAMES[i], 26, lc), max_w=3.95)
    return left_at(t, LABEL_X, (y0 + y1) / 2)


def zone_lines():
    return VGroup(*[Line([X0, y, 0], [X1, y, 0], stroke_color=GREY, stroke_width=1.5, stroke_opacity=0.6)
                    for y in (Y_VZ, Y_SVZ, Y_IZ)])


def side_labels():
    a = T("apical", 30, TEXT, weight=BOLD).move_to([-5.5, -3.0, 0])
    b = T("basal", 30, TEXT, weight=BOLD).move_to([-5.5, 2.75, 0])
    aa = arr([-4.85, -3.0, 0], [X0 - 0.1, -3.0, 0], TEXT, 3)
    ba = arr([-4.85, 2.75, 0], [X0 - 0.1, 2.75, 0], TEXT, 3)
    return VGroup(a, aa), VGroup(b, ba)


def species_tag(text="embryonic\nmouse cortex"):
    return T(text, 26, LBL, line_spacing=0.8).move_to([-5.45, 0.0, 0])


def zones_dim():
    """Zone shading and divider lines, no labels."""
    return [zone_band(i) for i in range(4)] + [zone_lines()]


def full_wall(zones=True, labels=True, side=True, cell=True, fib=True):
    """Everything the wall scenes share, returned as one list ready to self.add."""
    parts = [tissue_bg()]
    if fib:
        parts.append(fibres())
    parts.append(fluid_band())
    parts.append(pia_bars())
    if zones:
        parts += zones_dim()
    if labels:
        parts.append(pia_labels())
        parts += [zone_label(i) for i in range(4)]
    if side:
        a, b = side_labels()
        parts += [a, b]
    if cell:
        parts.append(RGCell())
    return parts


def dish_pieces(cx, cy):
    bowl = Arc(radius=2.2, start_angle=PI, angle=PI, stroke_color=LBL, stroke_width=5).stretch(0.4, 1)
    bowl.move_to([cx, cy, 0])
    return bowl


# ================================================================ scenes
class S00Title(TitleCard):
    LESSON = "The Ventricular Zone: Radial Glia as Stem Cells"
    TITLE = "One Cell Across the Wall"


class S01Q(SpokenScene):
    def construct(self):
        head = T("Where do cortical neurons come from?", 40, TEXT, font=TITLE_FONT)
        fit(head, max_w=12.0)
        head.move_to([0, 3.2, 0])
        dots = VGroup(*[circ(-6.0 + 0.62 * c + (0.2 if r % 2 else 0), 2.0 - 0.62 * r, 0.2, GREEN, 0.8, 2)
                        for r in range(8) for c in range(9)])
        nl = T("cortical neurons", 28, GREEN).move_to([-3.5, -3.2, 0])
        box = dashed(RoundedRectangle(width=3.6, height=5.0, corner_radius=0.3, stroke_color=RED, stroke_width=4), 56)
        box.move_to([3.7, -0.3, 0])
        q = T("?", 170, RED, weight=BOLD).move_to([3.7, -0.35, 0])
        a = arr([1.8, -0.3, 0], [-0.7, -0.3, 0], LBL, 6, 0.3)
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.5)
        self.at("neurons of the")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.02), FadeIn(nl), run_time=1.0)
        self.at("cortex come from")
        self.play(Create(box), FadeIn(q, scale=0.6), run_time=0.6)
        self.play(GrowArrow(a), run_time=0.5)
        self.at("one kind of cell")
        cell = RGCell(x=3.7, y0=-2.55, y1=1.95, ys=-1.5, k=1.3)
        lab = T("one kind of cell", 30, BLUE).move_to([3.7, -3.3, 0])
        self.play(FadeOut(q, scale=0.6), box.animate.set_color(BLUE), FadeIn(cell, scale=0.8), FadeIn(lab),
                  run_time=0.9)
        self.finish()


class S02Slice(SpokenScene):
    def construct(self):
        bg, fl, tg = tissue_bg(), fluid_band(), species_tag()
        self.play(FadeIn(bg, scale=0.97), run_time=0.6)                     # "Here is a slice"
        self.at("slice through")
        self.play(Indicate(bg, color=TEXT, scale_factor=1.02), run_time=0.9)
        self.at("embryonic mouse cortex")
        self.play(FadeIn(tg, shift=RIGHT * 0.2), run_time=0.6)
        self.at("the ventricle")
        self.play(FadeIn(fl[0], shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(fl[1]), run_time=0.3)
        ff = callout("fluid-filled space", [X1 + 0.05, -3.4, 0], LABEL_X, -3.4, LBL, 26)
        self.at("fluid filled")
        self.play(FadeIn(ff), run_time=0.5)
        self.at("is at the bottom")
        self.play(Indicate(fl[0], scale_factor=1.07, color=TEXT), run_time=0.9)
        self.finish()


class S03Apical(SpokenScene):
    def construct(self):
        bg, fl, tg = tissue_bg(), fluid_band(), species_tag()
        bars, plab = pia_bars(), pia_labels()
        a, b = side_labels()
        self.add(bg, fl, tg)
        edge_a = Line([X0, Y_V1, 0], [X1, Y_V1, 0], stroke_color=TEXT, stroke_width=7)
        edge_b = Line([X0, Y_CP, 0], [X1, Y_CP, 0], stroke_color=TEXT, stroke_width=7)
        self.at("facing the ventricle")
        self.play(Create(edge_a), run_time=0.8)
        self.at("is apical")
        self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=0.5)
        self.at("outer surface")
        self.play(Create(edge_b), run_time=0.7)
        self.at("under the pia")
        self.play(Create(bars), FadeIn(plab), run_time=0.7)
        self.at("is basal")
        self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.5)
        self.finish()


def s04_base():
    a, b = side_labels()
    return [tissue_bg(), fluid_band(), species_tag(), pia_bars(), pia_labels(), a, b]


class S04Vz(SpokenScene):
    def construct(self):
        self.add(*s04_base())
        vz, vl = zone_band(0), zone_label(0)
        self.at("beside the ventricle")
        self.play(Indicate(self.mobjects[1][0], scale_factor=1.05, color=TEXT), run_time=0.7)
        self.at("ventricular zone")
        self.play(FadeIn(vz), FadeIn(vl, shift=LEFT * 0.2), run_time=0.8)
        self.at("progenitors live")
        self.play(Indicate(vz, scale_factor=1.04, color=BLUE), run_time=0.9)
        card = card_frame(PANEL_X, 0.55, 3.9, 3.3, BLUE, 0.9, fill=True)
        w = T("progenitor", 42, BLUE, weight=BOLD).move_to([PANEL_X, 1.55, 0])
        d = T("a cell that\nstill divides", 30, TEXT, line_spacing=0.85).move_to([PANEL_X, 0.4, 0])
        icon = circ(PANEL_X, -0.6, 0.38, BLUE, 0.3)
        self.at("a progenitor is")
        self.play(FadeIn(card), FadeIn(w), FadeIn(icon), run_time=0.6)
        self.play(FadeIn(d), run_time=0.5)
        self.at("still divides")
        two = VGroup(circ(PANEL_X - 0.45, -0.6, 0.3, BLUE, 0.3), circ(PANEL_X + 0.45, -0.6, 0.3, BLUE, 0.3))
        self.play(ReplacementTransform(icon, two), run_time=0.8)
        self.finish()


class S05Zones(SpokenScene):
    def construct(self):
        self.add(*s04_base(), zone_band(0), zone_label(0))
        lines = zone_lines()
        self.add(lines[0])
        self.at("subventricular zone")
        self.play(FadeIn(zone_band(1)), FadeIn(zone_label(1), shift=LEFT * 0.2), run_time=0.8)
        self.add(lines[1])
        dots = VGroup(*[circ(x, -1.3, 0.17, GREEN, 0.9, 2) for x in (-1.9, -1.35, -0.8)])
        nl = tag("young neurons", GREEN, 26).move_to([0.9, -1.3, 0])
        ns = VGroup(dots, nl)
        self.at("young neurons cross")
        self.play(FadeIn(ns, scale=0.6), run_time=0.5)
        self.at("intermediate zone")
        self.add(lines[2])
        self.play(FadeIn(zone_band(2)), FadeIn(zone_label(2), shift=LEFT * 0.2), ns.animate.shift(UP * 1.3),
                  run_time=1.5)
        self.at("cortical plate")
        self.play(FadeIn(zone_band(3)), FadeIn(zone_label(3), shift=LEFT * 0.2), ns.animate.shift(UP * 1.9),
                  run_time=1.0)
        self.wait(0.2)
        self.play(FadeOut(ns), run_time=0.4)
        self.finish()


class S06Onecell(SpokenScene):
    def construct(self):
        self.add(*full_wall(cell=False, fib=False))
        fib = fibres()
        # the label sits left of the strip, on two lines, so it stays inside the frame
        nb = VGroup(leader([-3.82, -0.5, 0], [-4.4, -0.5, 0]),
                    T("neighbouring\ncells", 26, LBL, line_spacing=0.8).move_to([-5.55, -0.5, 0]))
        self.play(FadeIn(fib), FadeIn(nb), run_time=0.6)
        c = RGCell()
        self.at("light up")
        self.play(FadeOut(nb), FadeIn(c.afoot), FadeIn(c.soma), run_time=0.3)
        self.play(Create(c.glow), Create(c.fibre), run_time=1.2, rate_func=linear)
        self.play(FadeIn(c.bfoot), run_time=0.2)
        self.at("spans the whole")
        span = DoubleArrow([-2.2, Y_V1, 0], [-2.2, 2.74, 0], buff=0, color=TEXT, stroke_width=5, tip_length=0.25)
        self.play(GrowFromCenter(span), run_time=0.9)
        self.finish()


class S07Feet(SpokenScene):
    def construct(self):
        parts = full_wall()
        self.add(*parts)
        cell = parts[-1]
        ap = callout("apical foot", [CELL_X + 0.22, -3.0, 0], -1.95, -2.5, BLUE, 28)
        fb = callout("long radial fibre", [CELL_X + 0.05, 0.1, 0], -2.2, 0.1, BLUE, 28)
        bf = callout("basal foot", [CELL_X + 0.2, 2.62, 0], -2.2, 2.0, BLUE, 28, sub="on the basement membrane")
        self.at("apical foot")
        self.play(Indicate(cell.afoot, color=BLUE, scale_factor=1.4), FadeIn(ap), run_time=0.9)
        self.at("long fiber")
        self.play(Indicate(cell.fibre, color=BLUE, scale_factor=1.0), FadeIn(fb), run_time=0.9)
        self.at("basal foot")
        self.play(Indicate(cell.bfoot, color=BLUE, scale_factor=1.4), FadeIn(bf), run_time=0.9)
        self.finish()


def s08_base(zones=True):
    a, b = side_labels()
    parts = [tissue_bg(), fibres(), fluid_band(), pia_bars()]
    if zones:
        parts += zones_dim()
        parts.append(left_at(T("VZ", 30, BLUE, weight=BOLD), LABEL_X, -2.4))
    parts += [a, b, RGCell()]
    return parts


class S08Ne(SpokenScene):
    def construct(self):
        self.add(*s08_base())
        anc = [CELL_X + 0.06, 0.3, 0]
        lab = callout("neuroepithelial\ncell", anc, -2.2, 0.3, BLUE, 30)
        self.at("neuroepithelial cells")
        self.play(FadeIn(lab, shift=RIGHT * 0.2), run_time=0.7)
        neuro = T("neurogenesis begins", 28, GREEN).move_to([PANEL_X, 2.5, 0])
        self.at("neurogenesis begins")
        self.play(FadeIn(neuro, shift=UP * 0.2), run_time=0.7)
        mouse = T("embryonic day, mouse", 28, LBL).move_to([PANEL_X, 1.5, 0])
        axis = Arrow([3.1, 0.6, 0], [6.6, 0.6, 0], buff=0, color=LBL, stroke_width=4, tip_length=0.25)
        self.at("in mouse")
        self.play(FadeIn(mouse), Create(axis), run_time=0.7)
        t10 = VGroup(Line([3.9, 0.45, 0], [3.9, 0.75, 0], stroke_color=TEXT, stroke_width=5),
                     T("E10", 28, TEXT).move_to([3.9, 0.1, 0]))
        t12 = VGroup(Line([5.7, 0.45, 0], [5.7, 0.75, 0], stroke_color=TEXT, stroke_width=5),
                     T("E12", 28, TEXT).move_to([5.7, 0.1, 0]))
        self.at("days 10")
        self.play(FadeIn(t10), run_time=0.4)
        self.at("to 12")
        span = Line([3.9, 0.6, 0], [5.7, 0.6, 0], stroke_color=TEXT, stroke_width=9)
        self.play(FadeIn(t12), Create(span), run_time=0.6)
        new = callout("radial glial\ncell", anc, -2.2, 0.3, BLUE, 30)
        self.at("they become", lead=0.4)
        self.play(ReplacementTransform(lab, new), run_time=0.8)
        self.play(Indicate(new, color=BLUE, scale_factor=1.06), run_time=0.8)
        self.finish()


class S09Glial(SpokenScene):
    def construct(self):
        base = s08_base()
        self.add(*base)
        cell = base[-1]
        lab = callout("radial glial\ncell", [CELL_X + 0.06, 0.3, 0], -2.2, 0.3, BLUE, 30)
        self.add(lab)
        self.at("keep the long shape")
        self.play(Indicate(cell.glow, color=BLUE, scale_factor=1.0), Indicate(cell.soma, color=BLUE), run_time=1.2)

        def prot(name, y):
            dot = Dot([CELL_X, y, 0], radius=0.13, color=TEXT)
            ch = chip(name, TEXT, size=32)
            ch.add_to_back(RoundedRectangle(corner_radius=0.14, width=ch[0].width, height=ch[0].height, stroke_width=0,
                                            fill_color=BG, fill_opacity=0.96).move_to(ch[0]))
            left_at(ch, -1.7, y)
            ln = leader([CELL_X + 0.15, y, 0], [-1.72, y, 0], TEXT, 3)
            return dot, ln, ch
        d1, l1, c1 = prot("GLAST", 1.5)
        d2, l2, c2 = prot("BLBP", -0.9)
        self.at("they switch on")
        self.play(FadeIn(d1, scale=0.2), Create(l1), FadeIn(c1, shift=RIGHT * 0.2), run_time=0.5)
        self.at("proteins")
        self.play(FadeIn(d2, scale=0.2), Create(l2), FadeIn(c2, shift=RIGHT * 0.2), run_time=0.5)
        gf = chip("GFAP in primates", LBL, size=28)
        gf.move_to([PANEL_X, 0.0, 0])
        self.at("associated with")
        self.play(FadeIn(gf, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


class S10Mitoses(SpokenScene):
    def construct(self):
        # start from the slice with the VZ band, then enlarge that band into a box
        bg, fl = tissue_bg(), fluid_band()
        bands = [zone_band(i) for i in range(4)]
        lines = zone_lines()
        vzl = zone_label(0)
        self.add(bg, *bands, lines, fl, vzl)
        big = rect(X0, X1, Y_V1, 3.3, BLUE, 0.12, stroke=3, stroke_op=0.8)
        vzl2 = left_at(T("ventricular zone\n(enlarged)", 28, BLUE, line_spacing=0.8), LABEL_X, 2.5)
        self.at("where cells divide")
        self.play(FadeOut(bg), FadeOut(VGroup(*bands[1:])), FadeOut(lines), run_time=0.45)
        self.play(ReplacementTransform(bands[0], big), FadeOut(vzl), FadeIn(vzl2), run_time=0.8)

        bodies = VGroup(*[circ(-3.55 + 0.78 * i, -2.6, 0.34, BLUE, 0.25, 3) for i in range(8)])
        bars = VGroup(*[Line([-3.55 + 0.78 * i, -2.6 - 0.24, 0], [-3.55 + 0.78 * i, -2.6 + 0.24, 0],
                             stroke_color=TEAL, stroke_width=9) for i in range(8)])
        pos = [(-3.2, -0.3), (-1.5, 1.0), (0.1, -0.9), (1.5, 0.5)]
        halos = VGroup(*[circ(x, y, 0.42, YELLOW, 0.14, 0) for x, y in pos])
        nuc = VGroup(*[circ(x, y, 0.27, NUC, 0.9, 3).set_stroke(TEXT) for x, y in pos])
        # the cells first, unlabelled and neutral
        self.play(LaggedStart(*[FadeIn(b_, scale=0.6) for b_ in bodies], lag_ratio=0.05),
                  LaggedStart(*[FadeIn(n_, scale=0.6) for n_ in nuc], lag_ratio=0.1), run_time=0.8)
        ml = callout("mitosis", [2.28, -2.6, 0], LABEL_X, -2.6, TEAL, 32)
        self.at("caught in mitosis")
        self.play(LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.08), FadeIn(ml), run_time=1.0)
        self.at("against the ventricle")
        self.play(Indicate(VGroup(bodies, bars), color=TEAL, scale_factor=1.04), run_time=0.9)
        cl = callout("copying DNA", [1.9, 0.5, 0], LABEL_X, 0.5, YELLOW, 32)
        self.at("copying their DNA")
        self.play(*[n_.animate.set_fill(YELLOW, 0.95).set_stroke(YELLOW) for n_ in nuc], FadeIn(halos), FadeIn(cl),
                  run_time=0.8)
        self.at("farther out")
        self.play(Indicate(VGroup(nuc, halos), color=YELLOW, scale_factor=1.06), run_time=0.9)
        self.finish()


# ---- stem cell card (s11, s12)
LP, RP = -3.5, 3.5


def stem_card(labels=("a kind", "another kind")):
    title = T("stem cell", 48, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
    fl = card_frame(LP, -0.4, 6.4, 5.6, GREY, 0.55)
    fr = card_frame(RP, -0.4, 6.4, 5.6, GREY, 0.55)
    hl = T("renews itself", 34, TEXT).move_to([LP, 1.7, 0])
    hr = T("makes more than\none kind of cell", 32, TEXT, line_spacing=0.8).move_to([RP, 1.5, 0])
    pl = circ(-5.2, -0.6, 0.65, BLUE, 0.3)
    tl = circ(-1.9, -0.6, 0.65, BLUE, 0.3)
    al = arr(pl.get_right(), tl.get_left(), TEXT, 5)
    pr = circ(1.5, -0.6, 0.65, BLUE, 0.3)
    o1 = circ(5.2, 0.35, 0.5, GREEN, 0.7)
    o2 = sq(5.2, -1.55, 0.9, TEXT, 0.15)
    ar1 = arr(pr.get_right(), o1.get_left(), TEXT, 4)
    ar2 = arr(pr.get_right(), o2.get_left(), TEXT, 4)
    n1 = T(labels[0], 26, GREEN).move_to([5.2, -0.4, 0])
    n2 = T(labels[1], 26, TEXT).move_to([5.2, -2.25, 0])
    return dict(title=title, fl=fl, fr=fr, hl=hl, hr=hr, pl=pl, tl=tl, al=al, pr=pr, o1=o1, o2=o2, ar1=ar1,
                ar2=ar2, n1=n1, n2=n2)


class S11Stem(SpokenScene):
    def construct(self):
        c = stem_card()
        self.play(FadeIn(c["title"], shift=DOWN * 0.15), run_time=0.5)          # "Two words will matter"
        self.play(FadeIn(c["fl"]), FadeIn(c["fr"]), run_time=0.6)
        self.at("renews itself")
        self.play(FadeIn(c["hl"]), FadeIn(c["pl"]), run_time=0.5)
        self.play(GrowArrow(c["al"]), FadeIn(c["tl"], scale=0.6), run_time=0.6)
        self.at("makes more than")
        self.play(FadeIn(c["hr"]), FadeIn(c["pr"]), run_time=0.5)
        self.at("one kind of cell")
        self.play(GrowArrow(c["ar1"]), FadeIn(c["o1"], scale=0.6), FadeIn(c["n1"]), run_time=0.5)
        self.play(GrowArrow(c["ar2"]), FadeIn(c["o2"], scale=0.6), FadeIn(c["n2"]), run_time=0.5)
        self.finish()


class S12Rgstem(SpokenScene):
    def construct(self):
        c = stem_card()
        self.add(*c.values())
        r1 = T("radial glia", 26, BLUE).move_to([-5.2, 0.45, 0])
        r2 = T("radial glia", 26, BLUE).move_to([1.5, 0.45, 0])
        self.at("radial glia")
        self.play(FadeIn(r1), FadeIn(r2), Indicate(c["pl"], color=BLUE), Indicate(c["pr"], color=BLUE), run_time=0.9)
        bx1 = RoundedRectangle(corner_radius=0.08, width=0.55, height=0.55, stroke_color=TEXT, stroke_width=3).move_to([-5.7, 1.7, 0])
        bx2 = RoundedRectangle(corner_radius=0.08, width=0.55, height=0.55, stroke_color=TEXT, stroke_width=3).move_to([0.95, 1.5, 0])
        self.at("meet both conditions")
        self.play(FadeIn(bx1), FadeIn(bx2), Indicate(c["fl"], color=TEXT, scale_factor=1.02),
                  Indicate(c["fr"], color=TEXT, scale_factor=1.02), run_time=1.0)
        other = dashed(Circle(radius=0.5, stroke_color=LBL, stroke_width=3), 20).move_to([-3.55, -2.15, 0])
        oa = arr(c["pl"].get_bottom() + RIGHT * 0.3, other.get_left(), LBL, 3)
        self.at("an asymmetric division")
        self.play(GrowArrow(oa), FadeIn(other), run_time=0.8)
        kept = T("radial glial\ncell, kept", 26, BLUE, line_spacing=0.8).move_to([-1.9, 0.62, 0])
        leaves = T("leaves", 26, LBL).move_to([-3.55, -2.95, 0])
        k = check(-5.7, 1.7)
        self.at("keeps one radial glial cell")
        self.play(Indicate(c["tl"], color=BLUE, scale_factor=1.15), FadeIn(kept), FadeIn(leaves), Create(k), run_time=1.0)
        note = T("some lineages, in mouse", 26, LBL).move_to([RP, -2.85, 0])
        self.at("some single lineages")
        self.play(FadeIn(note), run_time=0.6)
        g1 = T("neurons", 26, GREEN).move_to([5.2, -0.4, 0])
        g2 = T("glia, later", 26, TEXT).move_to([5.2, -2.25, 0])
        self.at("later")
        self.play(Transform(c["n1"], g1), run_time=0.5)
        self.at("glia as well as neurons")
        k2 = check(0.95, 1.5)
        self.play(Transform(c["n2"], g2), Indicate(c["o2"], color=TEXT, scale_factor=1.15), Create(k2), run_time=0.9)
        self.finish()


class S13Potential(SpokenScene):
    def construct(self):
        fl = card_frame(LP, -0.4, 6.4, 5.6, GREY, 0.55)
        fr = card_frame(RP, -0.4, 6.4, 5.6, GREY, 0.55)
        tis = rect(1.2, 5.8, -2.3, -0.5, GREY, 0.14, stroke=2, stroke_op=0.6)
        bowl = dish_pieces(LP, -1.55)
        cell_l = circ(LP, -1.4, 0.5, BLUE, 0.3)
        cell_r = circ(RP, -1.4, 0.5, BLUE, 0.3)
        # first frame: the two settings, each holding one cell
        self.play(FadeIn(fl), FadeIn(fr), Create(bowl), FadeIn(tis), FadeIn(cell_l, scale=0.6),
                  FadeIn(cell_r, scale=0.6), run_time=0.35)
        eq = not_equal(0, 3.05)
        hp = T("potential", 44, TEXT, font=TITLE_FONT).move_to([LP, 3.05, 0])
        hf = T("fate", 44, TEXT, font=TITLE_FONT).move_to([RP, 3.05, 0])
        self.at("potential is not")
        self.play(Write(hp), run_time=0.5)
        self.at("not fate")
        self.play(FadeIn(eq), Write(hf), run_time=0.6)
        o1 = circ(-5.0, 0.7, 0.5, GREEN, 0.7)
        o2 = sq(-2.0, 0.7, 0.9, TEXT, 0.15)
        a1 = arr(cell_l.get_top() + UP * 0.05, o1.get_bottom(), TEXT, 4)
        a2 = arr(cell_l.get_top() + UP * 0.05, o2.get_bottom(), TEXT, 4)
        n1 = T("neuron", 26, GREEN).move_to([-5.0, 1.45, 0])
        n2 = T("glia", 26, LBL).move_to([-2.0, 1.45, 0])
        cm = T("can make", 28, LBL).move_to([LP, 2.0, 0])
        self.at("can make")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(o1, scale=0.6), FadeIn(o2, scale=0.6), FadeIn(cm),
                  FadeIn(n1), FadeIn(n2), run_time=0.5)
        dl = T("alone in a dish", 28, LBL).move_to([LP, -2.75, 0])
        self.at("alone in a dish")
        self.play(FadeIn(dl), run_time=0.5)
        p1 = circ(RP, 0.7, 0.5, GREEN, 0.7)
        b1 = arr(cell_r.get_top() + UP * 0.05, p1.get_bottom(), TEXT, 4)
        m1 = T("neuron", 26, GREEN).move_to([RP, 1.45, 0])
        dm = T("does make", 28, LBL).move_to([RP, 2.0, 0])
        self.at("does make")
        self.play(GrowArrow(b1), FadeIn(p1, scale=0.6), FadeIn(dm), FadeIn(m1), run_time=0.45)
        er = T("in the embryo", 28, LBL).move_to([RP, -2.75, 0])
        self.at("in the embryo")
        self.play(FadeIn(er), run_time=0.5)
        self.finish()


def puzzle_card(n, cx=PANEL_X, cy=0.9, w=3.9, h=5.2):
    fr = card_frame(cx, cy, w, h, RED, 0.9, fill=True)
    head = T(f"Puzzle {n}", 40, RED, weight=BOLD).move_to([cx, cy + h / 2 - 0.55, 0])
    return fr, head


class S14Puzzle1(SpokenScene):
    def construct(self):
        parts = full_wall(zones=True, labels=False, side=False)
        pia_l = pia_labels()
        self.add(*parts)
        cell = parts[-1]
        tg = T("fetal monkey\ncortex", 26, LBL, line_spacing=0.8).move_to([-5.45, -1.3, 0])
        fr, ph = puzzle_card(1, cy=0.0, h=5.2)
        sub = T("scaffold or\nsource?", 34, RED, line_spacing=0.85).move_to([PANEL_X, 0.9, 0])
        # the young neuron rises from the ventricle along the fibre, continuously, timed by the clock
        dot = circ(CELL_X, -2.95, 0.2, GREEN, 0.9, 2)
        T0, T1, YA, YB = 0.5, 6.4, -2.95, 2.4
        dot.add_updater(lambda m: m.move_to([CELL_X, YA + (YB - YA) * min(1.0, max(0.0, (self.elapsed() - T0) / (T1 - T0))), 0]))
        nlab = tag("young neuron", GREEN, 26)
        nlab.add_updater(lambda m: m.next_to(dot, RIGHT, buff=0.15))
        self.play(FadeIn(fr), FadeIn(ph), FadeIn(sub), FadeIn(dot, scale=0.3), run_time=0.5)  # "Now the first puzzle"
        self.at("fetal monkey cortex")
        self.play(FadeIn(tg), run_time=0.6)
        climb_t = T("young neurons climb\nradial glial fibres", 26, GREEN, line_spacing=0.85).move_to([PANEL_X, 1.0, 0])
        self.at("young neurons")
        self.add(nlab)
        self.play(FadeIn(nlab), Transform(sub, climb_t), run_time=0.5)
        fl = VGroup(leader([-4.35, 1.2, 0], [CELL_X - 0.1, 1.2, 0], BLUE),
                    T("radial glial\nfibre", 26, BLUE, line_spacing=0.8).move_to([-5.45, 1.2, 0]))
        self.at("radial glial fibers")
        self.play(Indicate(cell.glow, color=BLUE, scale_factor=1.0), FadeIn(fl), run_time=1.0)
        c1 = chip("scaffold", RED, size=34).move_to([PANEL_X, -0.4, 0])
        self.at("is the scaffold")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.5)
        orr = T("or", 30, LBL).move_to([PANEL_X, -1.1, 0])
        c2 = chip("source?", RED, size=34).move_to([PANEL_X, -1.85, 0])
        self.at("also the source")
        self.play(FadeIn(orr), FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        dot.clear_updaters()
        nlab.clear_updaters()
        self.finish()


class S15Puzzle2(SpokenScene):
    def construct(self):
        parts = [tissue_bg(), fibres(), fluid_band(), pia_bars()] + zones_dim()
        cell = RGCell()
        nuc = Circle(radius=0.27, stroke_color=TEXT, stroke_width=3, fill_color=NUC, fill_opacity=0.9).move_to([CELL_X, -2.7, 0])
        halo = Circle(radius=0.46, stroke_width=0, fill_color=YELLOW, fill_opacity=0.0).move_to([CELL_X, -2.7, 0])
        self.add(*parts, cell, halo, nuc)
        fr, ph = puzzle_card(2, cy=1.0, h=5.0)
        brace = BraceBetweenPoints([X1 + 0.1, Y_V1, 0], [X1 + 0.1, Y_VZ, 0], direction=RIGHT, color=BLUE)
        zl = T("ventricular\nzone", 28, BLUE, line_spacing=0.8)
        left_at(zl, X1 + 0.75, -2.4)
        self.at("second puzzle")
        self.play(FadeIn(fr), FadeIn(ph), run_time=0.6)
        q = T("Why divide at\nthe ventricle?", 36, RED, line_spacing=0.85).move_to([PANEL_X, 0.6, 0])
        self.at("why does")
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.6)
        cl = callout("copying DNA", [CELL_X + 0.3, -2.1, 0], -2.05, -2.1, YELLOW, 28)
        self.at("copy its DNA")
        self.play(nuc.animate.move_to([CELL_X, -2.1, 0]).set_fill(YELLOW, 0.95).set_stroke(YELLOW),
                  halo.animate.move_to([CELL_X, -2.1, 0]).set_fill(YELLOW, 0.3), run_time=1.0)
        self.play(FadeIn(cl), run_time=0.4)
        self.at("ventricular zone")
        self.play(FadeIn(brace), FadeIn(zl), run_time=0.7)
        self.at("then come back")
        self.play(FadeOut(cl), nuc.animate.move_to([CELL_X, -2.7, 0]).set_fill(NUC, 0.9).set_stroke(TEXT),
                  halo.animate.move_to([CELL_X, -2.7, 0]).set_fill(YELLOW, 0.0), run_time=1.1)
        dd = VGroup(*[circ(CELL_X + d, -2.7, 0.2, NUC, 0.9, 3).set_stroke(TEXT) for d in (-0.3, 0.3)])
        dv = callout("divides", [CELL_X + 0.5, -2.7, 0], -2.05, -2.7, TEXT, 28)
        self.at("to divide")
        self.play(ReplacementTransform(nuc, dd), FadeIn(dv), run_time=0.8)
        self.finish()


def wall_idea(glow_op=0.5):
    parts = [tissue_bg(), fibres(), fluid_band(), pia_bars()] + zones_dim()
    cell = RGCell()
    cell.glow.set_stroke(opacity=glow_op)
    return parts, cell


class S16Idea1(SpokenScene):
    def construct(self):
        parts, cell = wall_idea(0.8)
        halo = cell.glow.copy().set_stroke(GOLD, width=40, opacity=0.35)
        self.add(*parts, halo, cell)
        title = T("the idea", 40, GOLD, font=TITLE_FONT).move_to([PANEL_X, 3.05, 0])
        c1 = chip("radial glial cell", BLUE, size=32).move_to([PANEL_X, 1.9, 0])
        isa = T("is a", 30, LBL).move_to([PANEL_X, 1.0, 0])
        c2 = chip("stem cell", TEXT, size=32).move_to([PANEL_X, 0.15, 0])
        self.at("the idea to carry")
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.at("radial glial cell")
        self.play(FadeIn(c1), Indicate(cell.glow, color=BLUE, scale_factor=1.0), run_time=0.8)
        self.at("is a stem cell")
        self.play(FadeIn(isa), FadeIn(c2), run_time=0.7)
        anc = T("anchored at\nthe ventricle", 38, GOLD, line_spacing=0.85).move_to([PANEL_X, -2.0, 0])
        ring = Circle(radius=0.5, stroke_color=GOLD, stroke_width=5).move_to([CELL_X, -3.0, 0])
        lead = leader([CELL_X + 0.55, -3.1, 0], [PANEL_X - 1.75, -2.4, 0], GOLD, 4)
        self.at("anchored at the ventricle", lead=0.5)
        self.play(FadeIn(anc), Create(ring), Create(lead), Indicate(cell.afoot, color=GOLD, scale_factor=1.6),
                  halo.animate.set_stroke(GOLD, width=44, opacity=0.5), run_time=0.9)
        self.play(Indicate(parts[2][0], scale_factor=1.06, color=TEXT), run_time=0.8)
        self.finish()


class S17Idea2(SpokenScene):
    def construct(self):
        parent = circ(0, 1.2, 1.25, BLUE, 0.3)
        pl = T("radial glial\ncell", 28, BLUE, line_spacing=0.8).move_to([0, 1.2, 0])
        self.play(FadeIn(parent, scale=0.8), FadeIn(pl), run_time=0.6)
        d1 = dashed(Circle(radius=1.0, stroke_color=TEXT, stroke_width=4), 28).move_to([-3.0, -1.5, 0])
        d2 = dashed(Circle(radius=1.0, stroke_color=TEXT, stroke_width=4), 28).move_to([3.0, -1.5, 0])
        q1 = T("?", 80, RED, weight=BOLD).move_to(d1)
        q2 = T("?", 80, RED, weight=BOLD).move_to(d2)
        a1 = arr([-0.7, 0.2, 0], [-2.5, -0.65, 0], TEXT, 6)
        a2 = arr([0.7, 0.2, 0], [2.5, -0.65, 0], TEXT, 6)
        self.at("divides")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(d1), FadeIn(d2), FadeIn(q1), FadeIn(q2), run_time=1.0)
        stay = T("how many stay radial glia?", 40, TEXT).move_to([0, -3.2, 0])
        self.at("how many daughters stay")
        self.play(FadeIn(stay, shift=UP * 0.2), run_time=0.7)
        self.finish()


class S18Keep(SpokenScene):
    def construct(self):
        xs = [-4.55, 0, 4.55]
        frames = [card_frame(x, 0.0, 4.3, 6.9, GREY, 0.5) for x in xs]
        heads = [T(h, 46, TEXT, font=TITLE_FONT).move_to([x, 2.85, 0]) for x, h in zip(xs, ["keep 2", "keep 1", "keep 0"])]
        parents = [circ(x, 1.5, 0.75, BLUE, 0.3) for x in xs]
        slots = []
        arrows = []
        waits = []
        for x in xs:
            slots.append((x - 1.1, x + 1.1))
            arrows.append(VGroup(arr([x - 0.3, 0.8, 0], [x - 0.9, -0.0, 0], TEXT, 5, 0.2),
                                 arr([x + 0.3, 0.8, 0], [x + 0.9, -0.0, 0], TEXT, 5, 0.2)))
            waits.append(VGroup(*[dashed(Circle(radius=0.6, stroke_color=LBL, stroke_width=3), 18).move_to([sx, -0.65, 0])
                                  for sx in (x - 1.1, x + 1.1)]))
        # all three panels at once, daughters still waiting to be sorted
        self.play(*[FadeIn(f) for f in frames], *[FadeIn(h) for h in heads], *[FadeIn(p, scale=0.8) for p in parents],
                  *[FadeIn(a) for a in arrows], *[FadeIn(w) for w in waits], run_time=0.7)

        def kid(sx, color, op=0.3):
            return circ(sx, -0.65, 0.6, color, op, 3)

        def cap(text, x, color=BLUE):
            return T(text, 28, color, line_spacing=0.8).move_to([x, -2.4, 0])
        # keep 2
        k11, k12 = kid(xs[0] - 1.1, BLUE), kid(xs[0] + 1.1, BLUE)
        self.at("and its radial glial")
        self.play(FadeOut(waits[0]), FadeIn(k11), FadeIn(k12), run_time=0.5)
        self.at("line doubles")
        self.play(FadeIn(cap("radial glial line\ndoubles", xs[0])), run_time=0.5)
        # keep 1
        k21, k22 = kid(xs[1] - 1.1, BLUE), kid(xs[1] + 1.1, GREY)
        self.at("keep one")
        self.play(Indicate(heads[1], color=TEXT, scale_factor=1.1), run_time=0.4)
        self.at("and the line")
        self.play(FadeOut(waits[1]), FadeIn(k21), FadeIn(k22), run_time=0.5)
        self.at("line holds")
        self.play(FadeIn(cap("radial glial line\nholds steady", xs[1])), run_time=0.5)
        nl = T("neuron", 26, GREEN).move_to([xs[1] + 1.1, -1.45, 0])
        self.at("makes neurons")
        self.play(k22.animate.set_fill(GREEN, 0.8).set_stroke(GREEN), FadeIn(nl), run_time=0.6)
        # keep 0
        k31, k32 = kid(xs[2] - 1.1, GREY, 0.18), kid(xs[2] + 1.1, GREY, 0.18)
        self.at("keep none")
        self.play(Indicate(heads[2], color=TEXT, scale_factor=1.1), run_time=0.4)
        self.at("and its radial", nth=1)
        n3 = T("a daughter may still divide", 24, LBL).move_to([xs[2], -3.15, 0])
        fit(n3, max_w=4.0)
        self.play(FadeOut(waits[2]), FadeIn(k31), FadeIn(k32),
                  FadeIn(cap("radial glial line\nends", xs[2])), FadeIn(n3), run_time=0.6)
        self.finish()


class S19Spent(SpokenScene):
    def construct(self):
        dau = circ(-5.0, 0.2, 0.7, GREY, 0.3)
        lab = T("spent as a\nstem cell", 28, LBL, line_spacing=0.8).move_to([-5.0, -1.2, 0])
        dl = T("daughter that leaves", 26, LBL)
        left_at(dl, -4.55, 1.75)
        par = circ(-5.0, 3.0, 0.55, BLUE, 0.3)
        pa = arr([-5.0, 2.4, 0], [-5.0, 0.95, 0], TEXT, 5)
        n1 = circ(1.9, 2.3, 0.55, GREEN, 0.8)
        nl = T("a neuron", 32, GREEN).move_to([3.7, 2.3, 0])
        a1 = arr([-4.2, 0.65, 0], [1.3, 2.3, 0], TEXT, 5)
        orr = T("or", 32, LBL).move_to([-3.2, 0.2, 0])
        ip = circ(-1.2, -1.7, 0.75, BLUE, 0.3)
        ipl = T("intermediate\nprogenitor", 28, BLUE, line_spacing=0.8).move_to([-1.2, -3.1, 0])
        a2 = arr([-4.25, -0.2, 0], [-1.95, -1.55, 0], TEXT, 5)
        m1 = circ(2.2, -0.9, 0.5, GREEN, 0.8)
        m2 = circ(2.2, -2.5, 0.5, GREEN, 0.8)
        b1 = arr([-0.45, -1.5, 0], [1.65, -0.95, 0], TEXT, 4)
        b2 = arr([-0.45, -1.9, 0], [1.65, -2.45, 0], TEXT, 4)
        dv = T("divides", 26, LBL).move_to([0.5, -0.55, 0])
        nt = T("usually two\nneurons", 32, GREEN, line_spacing=0.8)
        left_at(nt, 3.1, -1.7)
        # the full branch skeleton, dim, so the frame is balanced from the first second
        names = dict(n1=n1, nl=nl, a1=a1, orr=orr, ip=ip, ipl=ipl, a2=a2, m1=m1, m2=m2, b1=b1, b2=b2, dv=dv, nt=nt)
        dim = {k: v.copy().set_opacity(0.18) for k, v in names.items()}
        self.play(FadeIn(par), FadeIn(pa), FadeIn(dau, scale=0.7), FadeIn(lab), FadeIn(dl),
                  *[FadeIn(d) for d in dim.values()], run_time=0.6)
        self.at("spent as a stem cell")
        self.play(Indicate(lab, color=TEXT, scale_factor=1.08), run_time=0.8)

        def lit(*ks):
            return [FadeOut(dim[k]) for k in ks]
        self.at("becomes a neuron")
        self.play(*lit("a1", "n1", "nl"), GrowArrow(a1), FadeIn(n1, scale=0.6), FadeIn(nl), run_time=0.9)
        self.at("or")
        self.play(*lit("orr"), FadeIn(orr), run_time=0.4)
        self.at("an intermediate progenitor")
        self.play(*lit("a2", "ip", "ipl"), GrowArrow(a2), FadeIn(ip, scale=0.6), FadeIn(ipl), run_time=0.9)
        self.at("that usually")
        self.play(*lit("b1", "b2", "m1", "m2", "dv", "nt"), GrowArrow(b1), GrowArrow(b2), FadeIn(m1, scale=0.6),
                  FadeIn(m2, scale=0.6), FadeIn(dv), FadeIn(nt), run_time=0.8)
        self.finish()


class S20Count(SpokenScene):
    def construct(self):
        xA, xB = -3.5, 3.5
        fa, fb = card_frame(xA, -0.15, 6.4, 6.3, GREY, 0.5), card_frame(xB, -0.15, 6.4, 6.3, GREY, 0.5)
        rA = T("rule: keep 1,\nmake 1 neuron", 30, TEXT, line_spacing=0.85).move_to([xA, 2.35, 0])
        rB = T("rule: keep 1, make an\nintermediate progenitor", 30, TEXT, line_spacing=0.85).move_to([xB, 2.35, 0])
        cA, cB = circ(xA, 0.65, 1.0, BLUE, 0.3), circ(xB, 0.65, 1.0, BLUE, 0.3)
        rl = M("round 0", 34, TEXT).move_to([0, 3.45, 0])
        tg = T("simple counting model, no cell death", 26, LBL).move_to([0, -3.6, 0])

        def counter(x):
            lab = T("neurons", 30, GREEN).move_to([x - 1.4, -2.7, 0])
            num = M("0", 60, GREEN).move_to([x + 1.2, -2.7, 0])
            return lab, num
        la, na = counter(xA)
        lb, nb = counter(xB)
        slotsA = [(xA + 1.3 - 1.3 * i, -1.5) for i in range(3)]
        slotsB = [(xB + 1.3 - 1.3 * (i // 2), -1.15 - 0.68 * (i % 2)) for i in range(6)]
        self.play(*[FadeIn(m) for m in (fa, fb, rA, rB, cA, cB, rl, tg, la, na, lb, nb)], run_time=0.7)
        self.at("round by round")
        for i in range(3):
            nrl = M(f"round {i + 1}", 34, TEXT).move_to(rl)
            nna = M(str(i + 1), 60, GREEN).move_to(na)
            nnb = M(str(2 * (i + 1)), 60, GREEN).move_to(nb)
            ga = circ(xA + 1.7, 0.65, 0.3, GREEN, 0.85, 3)
            ip = circ(xB + 1.7, 0.65, 0.3, BLUE, 0.5, 3)
            self.play(Indicate(cA, color=BLUE, scale_factor=1.06), Indicate(cB, color=BLUE, scale_factor=1.06),
                      FadeIn(ga, scale=0.3), FadeIn(ip, scale=0.3), run_time=0.4)
            sa = slotsA[i]
            gb1 = circ(xB + 1.7, 0.65, 0.3, GREEN, 0.85, 3)
            gb2 = circ(xB + 1.7, 0.65, 0.3, GREEN, 0.85, 3)
            self.add(gb1, gb2)
            self.remove(ip)
            def path(m, tgt):
                p = VMobject()
                p.set_points_as_corners([m.get_center(), [m.get_center()[0], -0.8, 0], [tgt[0], -0.8, 0], [tgt[0], tgt[1], 0]])
                return MoveAlongPath(m, p)
            self.play(path(ga, sa), path(gb1, slotsB[2 * i]), path(gb2, slotsB[2 * i + 1]),
                      Transform(rl, nrl), Transform(na, nna), Transform(nb, nnb), run_time=0.5)
            self.wait(0.15)
        self.play(Indicate(na, color=GREEN, scale_factor=1.25), Indicate(nb, color=GREEN, scale_factor=1.25),
                  run_time=0.9)
        self.wait(2.0)
        self.finish()


SC_X = -3.4


class S21Scope(SpokenScene):
    def construct(self):
        fr = card_frame(SC_X, 1.1, 6.0, 4.6, GREY, 0.6)
        hd = T("scope of the model", 28, LBL).move_to([SC_X, 2.9, 0])
        r1 = T("counting model", 38, TEXT).move_to([SC_X, 1.95, 0])
        r2 = T("excitatory projection\nneurons", 32, GREEN, line_spacing=0.8).move_to([SC_X, 0.7, 0])
        r3 = T("rodent dorsal cortex", 32, TEXT).move_to([SC_X, -0.6, 0])
        self.at("a counting model")
        self.play(FadeIn(fr), FadeIn(hd), FadeIn(r1), run_time=0.7)
        self.at("projection neurons")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.6)
        self.at("rodent dorsal cortex")
        self.play(FadeIn(r3, shift=UP * 0.15), run_time=0.6)
        # outer radial glia: drawn at the same scale as the cell and ventricle of the slice
        band = rect(0.8, 6.3, Y_V0, Y_V1, FLUID, 0.5)
        vl = T("ventricle", 26, TEXT).move_to(band)
        cx = 3.55
        soma = circ(cx, 0.5, 0.58, BLUE, 0.35)
        fibre = Line([cx, 1.08, 0], [cx, 3.0, 0], stroke_color=BLUE, stroke_width=8)
        bfoot = Polygon([cx - 0.12, 3.0, 0], [cx + 0.12, 3.0, 0], [cx + 0.32, 3.3, 0], [cx - 0.32, 3.3, 0],
                        stroke_width=0, fill_color=BLUE, fill_opacity=0.85)
        lab = T("outer radial\nglia", 30, BLUE, line_spacing=0.8)
        left_at(lab, cx + 0.8, 0.9)
        self.at("outer radial glia")
        self.play(FadeIn(band), FadeIn(vl), FadeIn(soma, scale=0.6), Create(fibre), FadeIn(bfoot), FadeIn(lab),
                  run_time=0.9)
        pr = T("common in\nprimates", 26, LBL, line_spacing=0.8)
        left_at(pr, cx + 0.8, -0.1)
        self.at("common in primates")
        self.play(FadeIn(pr), run_time=0.5)
        loop = Arc(radius=0.95, start_angle=PI * 0.62, angle=PI * 0.78, arc_center=[cx, 0.5, 0],
                   stroke_color=BLUE, stroke_width=5).add_tip(tip_length=0.22)
        rn = T("renews itself,\nno anchor", 26, BLUE, line_spacing=0.8)
        left_at(rn, 0.45, 1.0)
        self.at("renew themselves")
        self.play(Create(loop), FadeIn(rn), run_time=0.9)
        gap = DashedLine([cx, -0.12, 0], [cx, Y_V1, 0], color=RED, stroke_width=4)
        nt = T("no apical\ncontact", 28, RED, line_spacing=0.8)
        left_at(nt, cx + 0.3, -1.7)
        self.at("without the anchor")
        self.play(Create(gap), FadeIn(nt), run_time=0.8)
        self.finish()


class S22Explain(SpokenScene):
    def construct(self):
        fr = card_frame(0, 0.0, 12.4, 6.9, GREY, 0.6)
        hd = T("the rule", 44, TEXT, font=TITLE_FONT).move_to([0, 2.85, 0])
        k1 = check(-5.3, 1.6, 0.4)
        r1 = T("counts the choices", 40, TEXT)
        left_at(r1, -4.4, 1.6)
        self.play(FadeIn(fr), FadeIn(hd), run_time=0.5)
        self.at("rule counts")
        self.play(FadeIn(r1, shift=RIGHT * 0.2), Create(k1), run_time=0.7)
        q = T("?", 70, RED, weight=BOLD).move_to([-5.3, 0.1, 0])
        r2 = T("does not explain what makes\na daughter stay or leave", 40, TEXT, line_spacing=0.85)
        left_at(r2, -4.4, 0.1)
        self.at("does not explain")
        ar = arr([0.0, -0.8, 0], [0.0, -1.35, 0], TEXT, 5, 0.2)
        ll = T("answered in later lessons:", 30, LBL).move_to([0, -1.8, 0])
        c1 = chip("Notch", TEAL, size=34).move_to([-2.2, -2.75, 0])
        c2 = chip("asymmetric division", TEAL, size=34).move_to([2.3, -2.75, 0])
        d1, d2 = c1.copy().set_opacity(0.22), c2.copy().set_opacity(0.22)
        self.play(FadeIn(r2, shift=RIGHT * 0.2), FadeIn(q), GrowArrow(ar), FadeIn(ll), FadeIn(d1), FadeIn(d2),
                  run_time=0.7)
        self.at("stay or leave")
        self.play(FadeOut(d1), FadeOut(d2), FadeIn(c1), FadeIn(c2), run_time=0.5)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        parts, cell = wall_idea(0.55)
        halo = cell.glow.copy().set_stroke(GOLD, width=44, opacity=0.0)
        self.add(*parts, halo, cell)
        l0 = T("hold on to\none picture", 40, GOLD, font=TITLE_FONT, line_spacing=0.85).move_to([PANEL_X, 2.7, 0])
        self.play(FadeIn(l0, shift=UP * 0.2), run_time=0.4)
        self.at("hold on to")
        self.play(halo.animate.set_stroke(GOLD, width=44, opacity=0.6), Indicate(cell.soma, color=GOLD),
                  run_time=0.7)
        self.play(halo.animate.set_stroke(GOLD, width=40, opacity=0.25), run_time=0.7)
        l1 = T("one long cell\nacross the wall,", 36, BLUE, line_spacing=0.85).move_to([PANEL_X, 0.65, 0])
        self.at("one long cell across")
        self.play(FadeIn(l1, shift=UP * 0.2), run_time=0.8)
        l2 = T("spending its\ndivisions one\nchoice at a time", 36, TEXT, line_spacing=0.85).move_to([PANEL_X, -1.9, 0])
        self.at("spending its")
        self.play(FadeIn(l2, shift=UP * 0.2), run_time=0.7)
        cl = callout("one choice per division", [CELL_X + 0.6, -0.9, 0], -1.9, -0.9, GREEN, 26)
        for i, (cue, y) in enumerate((("divisions one", -0.3), ("choice at", -0.9), ("a time", -1.5))):
            self.at(cue)
            n = circ(CELL_X, -2.4, 0.2, GREEN, 0.9, 2)
            self.play(Indicate(cell.soma, color=GREEN, scale_factor=1.08), FadeIn(n, scale=0.3), run_time=0.15)
            self.play(n.animate.move_to([CELL_X + 0.38, y, 0]), run_time=0.4)
            if i == 1:
                self.play(FadeIn(cl), run_time=0.2)
        self.finish()


class S24End(EndCard):
    LINE = "One long cell spends its divisions one choice at a time."

    def construct(self):
        line = T(self.LINE, size=42, font=TITLE_FONT)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=30, color="#8EE6EC", weight=BOLD)
        g = VGroup(line, sub).arrange(DOWN, buff=0.45)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
