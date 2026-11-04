"""Chapter 6 of 6: The Top of the Tube  (Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, the whole film series; taken from scenes.old.py and chapter 1)
  YELLOW = Sonic hedgehog and the signalling it causes (gold, from below)
  DORSAL = BMP and the dorsal tissues that send it: roof plate, epidermis (blue-violet, from above);
           also the dorsal interneuron rows dI1 to dI6 and "dorsalized" tissue
  WNT    = Wnt1 and Wnt3a (new in this chapter: pink, so they are not mistaken for BMP)
  TEAL   = notochord and floor plate (the ventral source tissue)
  BLUE   = class I factors (Pax6, Irx3: one side of each repressing pair)
  ORANGE = class II factors (Nkx2.2) and the p3 domain
  GREEN  = Olig2 / the pMN domain; also "on / active" (receptor kinase, phosphate badge)
  RED    = repression (the T-bars and the block) and nothing else
  GREY   = tube wall, neutral cells, axes, membranes; TEXT (white) = progenitor outlines, cells of interest
Map geometry (every map scene rebuilds it in the same place): tube centred at x=0, dorsal up (chapter 1),
ELEVEN wall rows, one per class: p3 at the bottom, then pMN, p2, p1, p0, dI6 ... dI1 at the top. Source labels
(epidermis, roof plate, floor plate, notochord) sit to the right of the tube, row names to the left.
Smallest text is 26 pt; most is 28 pt or more.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
DORSAL = "#7D8BFF"
WNT = "#E58BC4"
SOFT = "#C3C9D6"        # high-contrast secondary text (never dim grey for words)
LESSON = "Ventral to Dorsal: Sonic Hedgehog and BMP in the Neural Tube"
SZ = 28


# ----------------------------------------------------------------------------- small helpers
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def inhib(a, b, color=RED, w=5, half=0.22):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.04
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + perp * half, b - perp * half, color=color, stroke_width=w + 1))


def mix(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), float(np.clip(t, 0, 1)))


def lab(s, x, y, color=TEXT, size=SZ, anchor="c", **kw):
    t = T(s, size, color, **kw).move_to([x, y, 0])
    if anchor == "l":
        t.shift(RIGHT * (x - t.get_left()[0]))
    elif anchor == "r":
        t.shift(RIGHT * (x - t.get_right()[0]))
    return t


def mlab(s, x, y, color=TEXT, size=SZ, anchor="c", **kw):
    t = M(s, size, color, **kw).move_to([x, y, 0])
    if anchor == "l":
        t.shift(RIGHT * (x - t.get_left()[0]))
    elif anchor == "r":
        t.shift(RIGHT * (x - t.get_right()[0]))
    return t


def bar(x, y, w, h, color, o=0.55, sw=3):
    return RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=o).move_to([x, y, 0])


def cellr(x, y, color=GREY, o=0.18, w=1.0, h=0.4, sw=2):
    return RoundedRectangle(corner_radius=0.07, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=o).move_to([x, y, 0])


def dot(x, y, color, r=0.09, o=0.95):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=o).move_to([x, y, 0])


def neuron(x, y, flip=1):
    soma = Circle(radius=0.16, stroke_width=0, fill_color=TEXT, fill_opacity=0.9).move_to([x, y, 0])
    ax = Line([x, y, 0], [x + 0.5 * flip, y, 0], color=TEXT, stroke_width=3)
    d1 = Line([x, y, 0], [x - 0.27 * flip, y + 0.22, 0], color=TEXT, stroke_width=3)
    d2 = Line([x, y, 0], [x - 0.27 * flip, y - 0.22, 0], color=TEXT, stroke_width=3)
    return VGroup(ax, d1, d2, soma)


def fchip(text, color, size=SZ, pad=0.16, fill_opacity=0.16, font=MONO):
    """Chip with a monospace label (so a capital I in Irx3 cannot be read as a lowercase l)."""
    label = Text(text, font=font, font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.14, width=label.width + 2 * pad, height=label.height + 2 * pad + 0.04,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill_opacity)
    return VGroup(box, label.move_to(box))


# ----------------------------------------------------------------------------- the transverse neural tube map
ROWN = ["p3", "pMN", "p2", "p1", "p0", "dI6", "dI5", "dI4", "dI3", "dI2", "dI1"]    # index 0 = bottom
NR = len(ROWN)
PITCH = 0.42


def ry(i):
    return -1.95 + PITCH * i


FLOOR_Y, ROOF_Y, EPI_Y, NOTO_Y = -2.4, 2.66, 3.32, -3.2
NEUT_STROKE, NEUT_FILL, NEUT_O = TEXT, GREY, 0.45
VCOL = {"p3": (ORANGE, 0.6), "pMN": (GREEN, 0.6), "p2": (TEXT, 0.34), "p1": (TEXT, 0.2), "p0": (TEXT, 0.34)}
ROWCOL = {"p3": ORANGE, "pMN": GREEN, "p2": TEXT, "p1": TEXT, "p0": TEXT}


def row_style(i):
    n = ROWN[i]
    if n.startswith("dI"):
        k = int(n[2]) - 1
        return DORSAL, (0.6 if k % 2 == 0 else 0.38)
    return VCOL[n]


def blend(i, ya=1.0, yb=1.0, lam=3.2):
    a = ya * float(np.exp(-i / lam))
    b = yb * float(np.exp(-(NR - 1 - i) / lam))
    t = b / (a + b) if (a + b) > 0 else 0
    return mix(YELLOW, DORSAL, t), 0.08 + 0.68 * min(1.0, a + b)


class TM:
    """The tube map. Everything is built at the origin, then scaled and shifted as one group; P() maps a map point."""

    def __init__(self, ox=0.0, oy=0.0, s=1.0, roof=True, floor=True, epi=True, noto=True):
        self.ox, self.oy, self.s = ox, oy, s
        self.shell = RoundedRectangle(corner_radius=0.8, width=3.3, height=5.5, stroke_color=GREY, stroke_width=5,
                                      fill_color=GREY, fill_opacity=0.06).move_to([0, 0.17, 0])
        self.can = RoundedRectangle(corner_radius=0.12, width=0.3, height=4.75, stroke_color=GREY, stroke_width=1.5,
                                    fill_color=BG, fill_opacity=0.9).move_to([0, 0.17, 0])
        self.rows = [VGroup(*[cellr(sx * 0.78, ry(i), NEUT_STROKE, NEUT_O, 1.2, 0.36, 3).set_fill(NEUT_FILL, NEUT_O) for sx in (-1, 1)])
                     for i in range(NR)]
        parts = [self.shell, self.can] + self.rows
        self.fl = bar(0, FLOOR_Y, 1.5, 0.24, TEAL, 0.6) if floor else None
        self.rf = bar(0, ROOF_Y, 1.5, 0.24, DORSAL, 0.6) if roof else None
        self.no = Circle(radius=0.33, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.4).move_to([0, NOTO_Y, 0]) if noto else None
        self.ep = bar(0, EPI_Y, 3.6, 0.2, DORSAL, 0.55) if epi else None
        for p in (self.fl, self.rf, self.no, self.ep):
            if p is not None:
                parts.append(p)
        self.g = VGroup(*parts)
        self.g.scale(s, about_point=ORIGIN).shift(np.array([ox, oy, 0.0]))

    def P(self, x, y):
        return np.array([x * self.s + self.ox, y * self.s + self.oy, 0.0])

    def L(self, text, x, y, color=TEXT, size=SZ, anchor="c", **kw):
        p = self.P(x, y)
        return lab(text, p[0], p[1], color, size, anchor, **kw)

    def l_floor(self):
        return self.L("floor plate", 1.95, FLOOR_Y, TEAL, SZ, "l")

    def l_noto(self):
        return self.L("notochord", 0.6, NOTO_Y, TEAL, SZ, "l")

    def l_roof(self):
        return self.L("roof plate", 1.95, ROOF_Y, DORSAL, SZ, "l")

    def l_epi(self):
        return self.L("epidermis", 2.1, EPI_Y, DORSAL, SZ, "l")

    def rowlab(self, i, color=None, font=MONO):
        n = ROWN[i]
        c = color or ROWCOL.get(n, TEXT)
        return self.L(n, -1.95, ry(i), c, SZ, "r", font=font, weight=BOLD if not n.startswith("dI") else NORMAL)

    def tint_anims(self, ya=1.0, yb=1.0):
        out = []
        for i, r in enumerate(self.rows):
            col, op = blend(i, ya, yb)
            out += [c.animate.set_stroke(col, 3).set_fill(col, op) for c in r]
        return out

    def tint_now(self, ya=1.0, yb=1.0):
        for i, r in enumerate(self.rows):
            col, op = blend(i, ya, yb)
            for c in r:
                c.set_stroke(col, 3).set_fill(col, op)

    def untint_anims(self):
        return [c.animate.set_stroke(NEUT_STROKE, 3).set_fill(NEUT_FILL, NEUT_O) for r in self.rows for c in r]

    def style_anims(self, idxs):
        out = []
        for i in idxs:
            col, op = row_style(i)
            out += [c.animate.set_stroke(col, 3).set_fill(col, op) for c in self.rows[i]]
        return out

    def style_now(self, idxs):
        for i in idxs:
            col, op = row_style(i)
            for c in self.rows[i]:
                c.set_stroke(col, 3).set_fill(col, op)

    def row_box(self, i, color=TEXT, sw=6):
        return RoundedRectangle(corner_radius=0.09, width=2.98 * self.s, height=0.5 * self.s, stroke_color=color,
                                stroke_width=sw).move_to(self.P(0, ry(i)))


DORSAL_ROWS = list(range(5, 11))      # dI6 (5) ... dI1 (10)
VENTRAL_ROWS = list(range(0, 5))
LOST_ROWS = [8, 9, 10]                # dI3, dI2, dI1
KEPT_ROWS = [5, 6, 7]                 # dI6, dI5, dI4


def base_labels(tm, roof=True, epi=True):
    out = [tm.l_floor(), tm.l_noto()]
    if roof:
        out.append(tm.l_roof())
    if epi:
        out.append(tm.l_epi())
    return out


# ============================================================================================ scenes
class S00Title(TitleCard):
    LESSON = LESSON
    TITLE = "The Top of the Tube"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=SOFT)
        title = T(self.TITLE, size=60, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.34)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(lesson, shift=UP * 0.1), run_time=self.beat(0.2))
        # a clean fade instead of the stroke-by-stroke Write, so no half-drawn outlines show
        self.play(FadeIn(title, shift=UP * 0.15), GrowFromCenter(rule), run_time=self.beat(0.3))
        self.wait(self.beat(0.3))
        self.play(FadeOut(g), run_time=self.beat(0.15))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        tm = TM()
        labs = VGroup(*base_labels(tm))
        chip_s = chip("Sonic hedgehog", YELLOW, SZ).move_to([4.75, -1.65, 0])
        pointer = arr([3.15, -1.65, 0], [1.75, -1.65, 0], YELLOW, 6, 0.22)
        self.play(FadeIn(tm.g), FadeIn(labs), run_time=0.7)
        self.at("patterns")
        self.play(*tm.tint_anims(1.0, 0.0), FadeIn(chip_s, shift=LEFT * 0.2), GrowArrow(pointer), run_time=1.0)
        self.at("bottom")
        self.play(Indicate(tm.fl, color=TEAL, scale_factor=1.3), run_time=0.6)
        self.at("what tells")
        q = T("What tells\nthe top it is\nthe top?", 46, TEXT, font=TITLE_FONT, line_spacing=1.0)
        q.move_to([-4.55, 0.7, 0])
        gr, ge = RoundedRectangle(corner_radius=0.2, width=1.9, height=0.55, stroke_width=0, fill_color=DORSAL, fill_opacity=0.35).move_to(tm.rf), \
            RoundedRectangle(corner_radius=0.2, width=3.9, height=0.5, stroke_width=0, fill_color=DORSAL, fill_opacity=0.3).move_to(tm.ep)
        self.play(FadeOut(chip_s), FadeOut(pointer), *tm.untint_anims(), FadeIn(q, shift=RIGHT * 0.2), FadeIn(gr), FadeIn(ge), run_time=0.7)
        self.at("top of")
        self.play(Indicate(tm.rf, color=DORSAL, scale_factor=1.3), Indicate(tm.ep, color=DORSAL, scale_factor=1.12), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
CAP_CY = -1.5
CAP_A, CAP_B = 4.6, 3.5


def dome_outline():
    ts = np.linspace(0, np.pi, 80)
    pts = [np.array([CAP_A * np.cos(t), CAP_CY + CAP_B * np.sin(t), 0]) for t in ts]
    return Polygon(*pts, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08)


def block_arc(color=RED):
    ts = np.linspace(np.radians(22), np.radians(158), 60)
    pts = [np.array([5.1 * np.cos(t), CAP_CY + 3.9 * np.sin(t), 0]) for t in ts]
    return VMobject(stroke_color=color, stroke_width=10).set_points_smoothly(pts)


def arc_y(x):
    return CAP_CY + 3.9 * np.sqrt(max(0.0, 1 - (x / 5.1) ** 2))


def cap_cells(style):
    spec = [(-0.92, np.arange(-3.6, 3.7, 1.2)), (0.15, np.arange(-3.0, 3.1, 1.2)), (1.12, np.array([-1.8, -0.6, 0.6, 1.8]))]
    cs = VGroup()
    for y, xs in spec:
        for x in xs:
            c = Circle(radius=0.5).move_to([x, y, 0])
            if style == "bmp":
                c.set_stroke(DORSAL, 3).set_fill(DORSAL, 0.5)
            else:
                c.set_stroke(TEXT, 3).set_fill(GREY, 0.4)
            cs.add(c)
    return cs


BMP_DOTS = [(x, arc_y(x) + 0.4 + 0.3 * ((k * 5) % 3)) for k, x in enumerate(np.linspace(-4.3, 4.3, 15))]


def cap_header():
    return lab("Neural induction", -6.5, 3.4, TEXT, 38, "l", font=TITLE_FONT)


class S02Recall(SpokenScene):
    def construct(self):
        head = cap_header()
        dome = dome_outline()
        cells = cap_cells("bmp")
        dots = VGroup(*[dot(x, y, DORSAL, 0.13) for x, y in BMP_DOTS if not (x < -2.6 and y > 2.0)])
        chip_b = chip("BMP", DORSAL, SZ).move_to([5.6, 1.5, 0])
        lead_b = Line([5.05, 1.5, 0], [3.9, arc_y(3.9) + 0.45, 0], color=DORSAL, stroke_width=3)
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(dome), FadeIn(cells, lag_ratio=0.05), FadeIn(dots),
                  FadeIn(chip_b), Create(lead_b), run_time=1.0)
        self.at("frog")
        l_cap = lab("frog animal cap", 0, -2.05, TEXT, 30)
        self.play(FadeIn(l_cap, shift=UP * 0.1), run_time=0.5)
        self.at("blocking")
        arc = block_arc()
        l_blk = lab("BMP\nblocked", 5.0, -0.55, RED, SZ, "l", line_spacing=0.9, weight=BOLD)
        self.play(Create(arc), FadeIn(l_blk, shift=LEFT * 0.15), dots.animate.shift(UP * 0.2).set_opacity(0.4),
                  FadeOut(lead_b), chip_b.animate.set_opacity(0.5), run_time=0.9)
        self.at("let the cells")
        self.play(*[c.animate.set_stroke(TEXT, 3).set_fill(GREY, 0.4) for c in cells], run_time=1.0)
        self.at("become")
        l_n = lab("neural", 0, -2.65, TEXT, 34, weight=BOLD)
        note_t = lab("In chick, BMP inhibition alone is not enough.", 0, -3.3, TEXT, 26)
        note_b = RoundedRectangle(corner_radius=0.14, width=note_t.width + 0.5, height=0.62, stroke_color=GOLD, stroke_width=2.5,
                                  fill_color=GOLD, fill_opacity=0.1).move_to(note_t)
        self.play(FadeIn(l_n, shift=UP * 0.1), FadeIn(note_b), FadeIn(note_t), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Back(SpokenScene):
    def construct(self):
        # carry the neural cap from the last scene, then let it fully fade before the tube appears
        cap_group = VGroup(cap_header(), dome_outline(), cap_cells("neural"), lab("neural", 0, -2.65, TEXT, 34, weight=BOLD))
        self.add(cap_group)
        tm = TM()
        tm.rf.set_fill(DORSAL, 0.1).set_stroke(DORSAL, 2, opacity=0.35)
        tm.ep.set_fill(DORSAL, 0.3)
        l_vz = tm.L("ventricular zone", -1.95, 0.17, TEXT, SZ, "r")
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_roof().set_opacity(0.5), tm.l_epi(), l_vz)
        self.at("now", lead=0.0)
        self.play(FadeOut(cap_group), run_time=0.5)
        self.play(FadeIn(tm.g), FadeIn(labs), run_time=0.8)
        self.at("bmp")
        b1 = chip("BMP", DORSAL, SZ).move_to([-3.45, EPI_Y, 0])
        k1 = Line([-2.85, EPI_Y, 0], [-1.85, EPI_Y, 0], color=DORSAL, stroke_width=3)
        self.play(FadeIn(b1, shift=RIGHT * 0.2), Create(k1), tm.ep.animate.set_fill(DORSAL, 0.85), run_time=0.6)
        self.at("comes back")
        ea = VGroup(*[arr([x, EPI_Y - 0.14, 0], [x, ROOF_Y + 0.2, 0], DORSAL, 8, 0.2) for x in (-0.8, 0, 0.8)])
        self.play(LaggedStart(*[GrowArrow(a) for a in ea], lag_ratio=0.2),
                  *tm.tint_anims(0.0, 0.35), run_time=1.3)
        self.at("roof plate", lead=1.9)
        b2 = chip("BMP", DORSAL, SZ).move_to([-3.45, ROOF_Y, 0])
        k2 = Line([-2.85, ROOF_Y, 0], [-0.8, ROOF_Y, 0], color=DORSAL, stroke_width=3)
        ra = VGroup(*[arr([x, ROOF_Y - 0.16, 0], [x, 1.3, 0], DORSAL, 8, 0.22) for x in (-0.55, 0.55)])
        self.play(tm.rf.animate.set_fill(DORSAL, 0.85).set_stroke(DORSAL, 3, opacity=1), labs[2].animate.set_opacity(1),
                  FadeIn(b2, shift=RIGHT * 0.2), Create(k2), Flash(tm.rf, color=DORSAL, flash_radius=0.7),
                  LaggedStart(*[GrowArrow(a) for a in ra], lag_ratio=0.2), *tm.tint_anims(0.0, 1.0), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Bmp(SpokenScene):
    def construct(self):
        YM = 1.2
        xs = [-4.4, -1.6, 1.6, 4.4]
        names = ["type II", "type I", "type I", "type II"]
        mem = Rectangle(width=12.4, height=0.28, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, YM, 0])
        l_mem = lab("cell\nmembrane", 5.25, 0.5, SOFT, 26, "l", line_spacing=0.9)
        caps = VGroup(*[RoundedRectangle(corner_radius=0.22, width=1.3, height=1.55, stroke_color=TEXT, stroke_width=3,
                                         fill_color=GREY, fill_opacity=0.3).move_to([x, YM + 0.2, 0]) for x in xs])
        tl = VGroup(*[lab(n, x, YM + 0.62, TEXT, 26) for n, x in zip(names, xs)])
        kin = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.3, height=0.55, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.2).move_to([x, 0.1, 0]) for x in xs])
        kl = VGroup(*[lab("kinase", x, 0.1, SOFT, 26) for x in xs])
        nuc = Ellipse(width=11.4, height=1.4, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to([0, -3.05, 0])
        l_nuc = lab("nucleus", -4.3, -3.05, SOFT, SZ, "c")
        # BMP dimer: two joined halves above the receptors
        lobe_l = RoundedRectangle(corner_radius=0.3, width=5.0, height=0.7, stroke_color=DORSAL, stroke_width=3, fill_color=DORSAL, fill_opacity=0.55)
        lobe_r = lobe_l.copy()
        lobe_l.move_to([-2.7, 3.0, 0])
        lobe_r.move_to([2.7, 3.0, 0])
        join = Circle(radius=0.22, stroke_color=DORSAL, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([0, 3.0, 0])
        bl, br = lab("BMP", -2.7, 3.0, TEXT, SZ, weight=BOLD), lab("BMP", 2.7, 3.0, TEXT, SZ, weight=BOLD)
        dimer = VGroup(lobe_l, lobe_r, join, bl, br)
        s1 = chip("Smad", TEXT, SZ, pad=0.14).move_to([-1.6, -1.0, 0])
        s2 = chip("Smad", TEXT, SZ, pad=0.14).move_to([1.6, -1.0, 0])
        s4 = chip("Smad4", TEXT, SZ, pad=0.14, fill_opacity=0.08).move_to([0, -1.85, 0])
        bright = [m.copy() for m in (s1, s2, s4)]
        for m in (s1, s2, s4):
            m.set_opacity(0.35)
        self.play(FadeIn(mem), FadeIn(l_mem), FadeIn(caps), FadeIn(tl), FadeIn(kin), FadeIn(kl), FadeIn(nuc, run_time=0.8),
                  FadeIn(l_nuc), FadeIn(dimer, shift=DOWN * 0.2), FadeIn(s1), FadeIn(s2), FadeIn(s4), run_time=0.9)
        self.at("bone")
        l_full = lab("bone morphogenetic proteins", 0, 3.57, DORSAL, SZ)
        self.play(FadeIn(l_full, shift=DOWN * 0.1), run_time=0.5)
        self.at("act through")
        self.play(dimer.animate.shift(DOWN * 0.5), l_full.animate.set_opacity(0.0),
                  *[c.animate.set_stroke(DORSAL, 4) for c in caps], run_time=0.7)
        self.at("receptor")
        self.play(*[k.animate.set_stroke(GREEN, 3).set_fill(GREEN, 0.5) for k in kin], *[l.animate.set_color(TEXT) for l in kl], run_time=0.6)
        self.at("and", lead=0.3)
        self.play(*[Transform(m, b) for m, b in zip((s1, s2, s4), bright)], run_time=0.3)
        a1 = arr([-1.6, -0.2, 0], [-1.6, -0.62, 0], GREEN, 6, 0.2)
        a2 = arr([1.6, -0.2, 0], [1.6, -0.62, 0], GREEN, 6, 0.2)
        pb1 = VGroup(Circle(radius=0.22, stroke_width=0, fill_color=GREEN, fill_opacity=1), T("P", 26, BG, weight=BOLD)).move_to(s1.get_corner(UR) + np.array([0.12, 0.2, 0]))
        pb2 = VGroup(Circle(radius=0.22, stroke_width=0, fill_color=GREEN, fill_opacity=1), T("P", 26, BG, weight=BOLD)).move_to(s2.get_corner(UL) + np.array([-0.12, 0.2, 0]))
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(pb1, scale=0.5), FadeIn(pb2, scale=0.5), run_time=0.4)
        self.play(FadeOut(a1), FadeOut(a2), s1.animate.move_to([-1.6, -3.05, 0]), s2.animate.move_to([1.6, -3.05, 0]),
                  s4.animate.move_to([0, -3.05, 0]), pb1.animate.move_to([-1.6, -3.05, 0] + (pb1.get_center() - s1.get_center())),
                  pb2.animate.move_to([1.6, -3.05, 0] + (pb2.get_center() - s2.get_center())), run_time=1.85)
        self.finish()


# ---------------------------------------------------------------------------------------------
DR = 2.5
DX, DY = 3.4, -0.5
EXY = -1.25


def dish(x, y, r=DR):
    return VGroup(Circle(radius=r, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0]),
                  Circle(radius=r - 0.18, stroke_width=2, stroke_color=GREY, stroke_opacity=0.5).move_to([x, y, 0]))


CELLS_OFF = [(-0.7, 0.12), (-0.25, 0.22), (0.25, 0.12), (0.7, 0.2), (-0.5, -0.2), (0.0, -0.12), (0.5, -0.2)]


def explant(cx, cy, color=None):
    g = VGroup()
    for dx, dy in CELLS_OFF:
        c = Circle(radius=0.32).move_to([cx + dx * 1.4, cy + dy * 1.6, 0])
        if color:
            c.set_stroke(color, 3).set_fill(color, 0.55)
        else:
            c.set_stroke(TEXT, 3).set_fill(GREY, 0.4)
        g.add(c)
    return g


def credit(year, names, x=-6.5, y=3.4):
    return lab(f"{year}   {names}", x, y, SOFT, 26, "l")


class S05Liem(SpokenScene):
    def construct(self):
        dl, dr = dish(-DX, DY), dish(DX, DY)
        el, er = explant(-DX, EXY), explant(DX, EXY)
        cit = credit("1995", "Liem, Tremml, Roelink and Jessell")
        self.play(FadeIn(dl, scale=0.9), FadeIn(dr, scale=0.9), FadeIn(el, scale=0.5), FadeIn(er, scale=0.5), FadeIn(cit, shift=RIGHT * 0.2),
                  run_time=1.0)
        self.at("tested", lead=0.4)
        cb = chip("BMP", DORSAL, SZ).move_to([DX, DY + 2.9, 0])
        self.add(cb)
        self.play(FadeIn(cb, shift=DOWN * 0.1), run_time=0.3)
        self.play(cb.animate.move_to([DX, DY + 1.35, 0]), run_time=0.7)
        self.at("chick")
        l_e = lab("chick neural plate explants", 0, -3.45, TEXT, SZ)
        self.play(FadeIn(l_e, shift=UP * 0.1), Indicate(el, color=TEXT, scale_factor=1.04), Indicate(er, color=TEXT, scale_factor=1.04), run_time=0.8)
        self.finish()


class S06Liem2(SpokenScene):
    def construct(self):
        dl, dr = dish(-DX, DY), dish(DX, DY)
        el, er = explant(-DX, EXY), explant(DX, EXY)
        cit = credit("1995", "Liem, Tremml, Roelink and Jessell")
        l_e = lab("chick neural plate explants", 0, -3.45, TEXT, SZ)
        cb = chip("BMP", DORSAL, SZ).move_to([DX, DY + 1.35, 0])
        self.add(dl, dr, el, er, cit, l_e, cb)
        self.at("bmp4", lead=0.0)
        c4 = chip("BMP4", DORSAL, SZ).move_to([DX, DY + 1.35, 0])
        self.play(ReplacementTransform(cb, c4), run_time=0.4)
        self.at("bmp7")
        c7 = chip("BMP7", DORSAL, SZ).move_to([DX, DY + 0.55, 0])
        self.play(FadeIn(c7, shift=DOWN * 0.3), run_time=0.5)
        self.at("could mimic")
        strip = bar(-DX, DY + 0.55, 2.6, 0.28, DORSAL, 0.55)
        l_ep = lab("epidermis", -DX, DY + 1.35, DORSAL, SZ)
        self.play(FadeIn(strip, shift=DOWN * 0.3), FadeIn(l_ep), run_time=0.6)
        self.at("dorsalizing")
        tl = lab("dorsal", -DX, -3.45, DORSAL, 30, weight=BOLD)
        tr = lab("dorsal", DX, -3.45, DORSAL, 30, weight=BOLD)
        self.play(FadeOut(l_e), *[c.animate.set_stroke(DORSAL, 3).set_fill(DORSAL, 0.55) for c in list(el) + list(er)],
                  FadeIn(tl), FadeIn(tr), run_time=1.1)
        self.at("epidermis")
        self.play(Indicate(strip, color=DORSAL, scale_factor=1.1), Indicate(l_ep, color=DORSAL), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Roof(SpokenScene):
    def construct(self):
        tm = TM()
        tm.rf.set_fill(DORSAL, 0.1).set_stroke(DORSAL, 2, opacity=0.35)
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_epi())
        l_roof = tm.l_roof()
        year = T("1997", 80, TEXT, font=TITLE_FONT).move_to([-4.6, 1.3, 0])
        cit = lab("Liem, Tremml and\nJessell, 1997", -4.6, 0.1, SOFT, SZ, line_spacing=0.95)
        self.add(tm.g, labs)
        self.at("1997", lead=0.0)
        self.play(FadeIn(year, scale=0.9), FadeIn(cit, shift=UP * 0.1), run_time=0.7)
        self.at("bmps")
        cb = chip("BMPs", DORSAL, SZ).move_to([-3.5, EPI_Y, 0])
        kb = Line([-2.85, EPI_Y, 0], [-1.85, EPI_Y, 0], color=DORSAL, stroke_width=3)
        ar = VGroup(*[arr([x, EPI_Y - 0.08, 0], [x, ROOF_Y + 0.1, 0], DORSAL, 16, 0.3) for x in (-0.9, 0, 0.9)])
        self.play(FadeIn(cb, shift=RIGHT * 0.2), Create(kb), Indicate(tm.ep, color=DORSAL, scale_factor=1.1),
                  LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.25, run_time=1.5), run_time=1.5)
        self.at("induce")
        self.play(tm.rf.animate.set_fill(DORSAL, 0.85).set_stroke(DORSAL, 3, opacity=1), FadeIn(l_roof),
                  Flash(tm.rf, color=DORSAL, flash_radius=0.8), run_time=0.8)
        self.finish()


class S08Roof2(SpokenScene):
    def construct(self):
        tm = TM()
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_roof(), tm.l_epi())
        self.add(tm.g, labs)
        self.at("roof plate", lead=0.0)
        self.play(Indicate(tm.rf, color=DORSAL, scale_factor=1.25), run_time=0.6)
        self.at("then becomes")
        g = RoundedRectangle(corner_radius=0.2, width=1.9, height=0.6, stroke_width=0, fill_color=DORSAL, fill_opacity=0.0).move_to(tm.rf)
        self.add(g)
        self.play(g.animate.set_fill(DORSAL, 0.45), tm.rf.animate.set_fill(DORSAL, 0.95), run_time=0.8)
        self.at("second")
        dots = VGroup(*[dot(s * (0.3 + 0.28 * k), ROOF_Y - 0.28, DORSAL, 0.15) for k in range(3) for s in (-1, 1)])
        dots.set_opacity(0)
        self.add(dots)
        l_s = lab("second source of\nrelated signals", 2.7, 1.55, DORSAL, SZ, "l", line_spacing=0.95)
        lk = Line([2.6, 1.95, 0], [0.8, ROOF_Y - 0.1, 0], color=DORSAL, stroke_width=3)
        self.play(FadeIn(l_s, shift=LEFT * 0.15), Create(lk),
                  LaggedStart(*[d.animate.set_opacity(0.95).shift(DOWN * (0.45 + 0.08 * i)) for i, d in enumerate(dots)], lag_ratio=0.08),
                  run_time=1.3)
        self.finish()


class S09Wnt(SpokenScene):
    def construct(self):
        tm = TM()
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_roof(), tm.l_epi())
        g = RoundedRectangle(corner_radius=0.2, width=1.9, height=0.6, stroke_width=0, fill_color=DORSAL, fill_opacity=0.45).move_to(tm.rf)
        tm.rf.set_fill(DORSAL, 0.95)
        self.add(tm.g, labs, g)
        self.bring_to_front(tm.rf)
        self.at("makes", lead=0.2)
        dots = VGroup(*[dot(s * (0.3 + 0.28 * k), ROOF_Y - 0.28, WNT, 0.15) for k in range(3) for s in (-1, 1)])
        dots.set_opacity(0)
        self.add(dots)
        c0 = chip("Wnts", WNT, SZ).move_to([-3.6, 2.9, 0])
        k0 = Line([-2.95, 2.85, 0], [-0.8, ROOF_Y + 0.05, 0], color=WNT, stroke_width=3)
        self.play(FadeIn(c0, shift=RIGHT * 0.2), Create(k0),
                  LaggedStart(*[d.animate.set_opacity(0.95).shift(DOWN * (0.45 + 0.08 * i)) for i, d in enumerate(dots)], lag_ratio=0.08),
                  run_time=1.0)
        self.at("wnt1", lead=0.1)
        c1 = chip("Wnt1", WNT, SZ).move_to([-3.6, 2.9, 0])
        self.play(ReplacementTransform(c0, c1), run_time=0.3)
        self.at("and")
        c2 = chip("Wnt3a", WNT, SZ).move_to([-3.6, 2.05, 0])
        k2 = Line([-2.85, 2.05, 0], [-0.8, ROOF_Y - 0.12, 0], color=WNT, stroke_width=3)
        self.play(FadeIn(c2, shift=RIGHT * 0.2), Create(k2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def dI_icons():
    return VGroup(*[neuron(x, 0.15) for x in (2.6, 3.5, 4.4)])


def wnt_carry():
    c1 = chip("Wnt1", WNT, SZ).move_to([-3.6, 2.9, 0])
    c2 = chip("Wnt3a", WNT, SZ).move_to([-3.6, 2.05, 0])
    k1 = Line([-2.95, 2.85, 0], [-0.8, ROOF_Y + 0.05, 0], color=WNT, stroke_width=3)
    k2 = Line([-2.85, 2.05, 0], [-0.8, ROOF_Y - 0.12, 0], color=WNT, stroke_width=3)
    ds = VGroup(*[dot(s * (0.3 + 0.28 * k), ROOF_Y - 0.28 - 0.45 - 0.08 * (2 * k + (s > 0)), WNT, 0.15, 0.95) for k in range(3) for s in (-1, 1)])
    return VGroup(c1, c2, k1, k2, ds)


class S10DI(SpokenScene):
    def construct(self):
        tm = TM()
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_roof(), tm.l_epi())
        wc = wnt_carry()
        self.add(tm.g, labs, wc)
        self.at("dorsal", lead=0.2)
        self.play(*[Indicate(c, color=DORSAL, scale_factor=1.08) for i in DORSAL_ROWS for c in tm.rows[i]],
                  Succession(Wait(0.7), FadeOut(wc, run_time=0.4)), run_time=0.9)
        self.at("six", lead=0.3)
        self.play(LaggedStart(*[AnimationGroup(*tm.style_anims([i])) for i in reversed(DORSAL_ROWS)], lag_ratio=0.3), run_time=1.5)
        self.at("interneurons")
        br = Line([1.85, 2.42, 0], [1.85, -0.02, 0], color=DORSAL, stroke_width=4)
        l_i = lab("six early classes\nof interneurons", 2.25, 1.2, TEXT, SZ, "l", line_spacing=0.95)
        ic = dI_icons()
        self.play(Create(br), FadeIn(l_i, shift=LEFT * 0.15), LaggedStart(*[FadeIn(n, scale=0.6) for n in ic], lag_ratio=0.25), run_time=1.0)
        self.at("named", lead=0.3)
        rl = VGroup(*[tm.rowlab(i) for i in reversed(DORSAL_ROWS)])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in rl], lag_ratio=0.22), run_time=1.5)
        self.at("top down", lead=0.4)
        da = arr([-3.3, 2.4, 0], [-3.3, 0.05, 0], TEXT, 5, 0.22)
        self.play(GrowArrow(da), run_time=0.9)
        self.finish()


def stripes_frame(tm, with_roof=False):
    tm.style_now(DORSAL_ROWS)


def predict_items(question=True):
    tm = TM(roof=False, epi=False)
    tm.style_now(DORSAL_ROWS)
    rl = VGroup(*[tm.rowlab(i) for i in DORSAL_ROWS])
    slot = DashedVMobject(RoundedRectangle(corner_radius=0.07, width=1.5, height=0.28, stroke_color=TEXT, stroke_width=3),
                          num_dashes=26).move_to([0, ROOF_Y, 0])
    l_rm = tm.L("roof plate removed", 1.95, ROOF_Y, TEXT, 26, "l")
    labs = VGroup(tm.l_floor(), tm.l_noto())
    head = lab("mouse\n(schematic)", -6.5, 2.2, TEXT, 30, "l", line_spacing=0.95)
    items = [tm.g, rl, slot, l_rm, labs, head]
    q = None
    if question:
        q = lab("Which classes\nare lost?", 4.5, 0.9, TEXT, 40, line_spacing=0.95)
    return tm, items, q


class S11Predict(SpokenScene):
    def construct(self):
        tm = TM()
        tm.style_now(DORSAL_ROWS)
        rl = VGroup(*[tm.rowlab(i) for i in DORSAL_ROWS])
        l_epi, l_roof = tm.l_epi(), tm.l_roof()
        labs = VGroup(tm.l_floor(), tm.l_noto())
        self.add(tm.g, rl, labs, l_epi, l_roof)
        head = T("Predict", 46, GOLD, font=TITLE_FONT).move_to([-5.3, 3.2, 0])
        self.play(FadeIn(head, shift=RIGHT * 0.2), FadeOut(tm.ep), FadeOut(l_epi), run_time=0.6)
        self.at("remove")
        slot = DashedVMobject(RoundedRectangle(corner_radius=0.07, width=1.5, height=0.28, stroke_color=TEXT, stroke_width=3),
                              num_dashes=26).move_to([0, ROOF_Y, 0])
        l_rm = tm.L("roof plate removed", 1.95, ROOF_Y, TEXT, 26, "l")
        self.play(Flash(tm.rf, color=TEXT, flash_radius=0.8), FadeOut(tm.rf), FadeIn(slot), ReplacementTransform(l_roof, l_rm), run_time=0.9)
        self.at("mouse")
        l_m = lab("mouse\n(schematic)", -6.5, 2.2, TEXT, 30, "l", line_spacing=0.95)
        self.play(FadeIn(l_m, shift=RIGHT * 0.15), run_time=0.5)
        self.at("leaving")
        g_f = RoundedRectangle(corner_radius=0.2, width=1.9, height=0.6, stroke_width=0, fill_color=TEAL, fill_opacity=0.35).move_to(tm.fl)
        g_n = Circle(radius=0.5, stroke_width=0, fill_color=TEAL, fill_opacity=0.35).move_to(tm.no)
        self.play(FadeIn(g_f), FadeIn(g_n), Indicate(tm.fl, color=TEAL, scale_factor=1.25), Indicate(tm.no, color=TEAL, scale_factor=1.25),
                  run_time=1.0)
        self.at("which")
        q = lab("Which classes\nare lost?", 4.5, 0.9, TEXT, 40, line_spacing=0.95)
        self.play(FadeIn(q, shift=LEFT * 0.2), FadeOut(g_f), FadeOut(g_n), run_time=0.6)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        tm, items, q = predict_items(True)
        self.add(*items, q)
        pd = lab("Pause and decide", 4.5, -0.35, GOLD, 34, weight=BOLD)
        track = RoundedRectangle(corner_radius=0.06, width=4.2, height=0.16, stroke_color=GOLD, stroke_width=2, fill_color=GOLD, fill_opacity=0.12).move_to([4.5, -1.05, 0])
        fill = Rectangle(width=4.2, height=0.16, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([4.5, -1.05, 0])
        self.add(pd, track, fill)
        self.play(fill.animate(rate_func=linear).stretch(0.001, 0, about_edge=LEFT), run_time=4.8)
        self.finish()


class S13Reveal(SpokenScene):
    def construct(self):
        tm, items, q = predict_items(True)
        l_rm = items[3]
        self.add(*items, q)
        year = T("2000", 80, TEXT, font=TITLE_FONT).move_to([-4.9, 0.7, 0])
        cit = lab("Lee, Dietrich and\nJessell, 2000", -6.5, -0.45, SOFT, SZ, "l", line_spacing=0.95)
        l_no = tm.L("no roof plate", 1.95, ROOF_Y, TEXT, SZ, "l")
        self.at("in", lead=0.0)
        self.play(FadeIn(year, scale=0.9), FadeIn(cit, shift=UP * 0.1), FadeOut(q), ReplacementTransform(l_rm, l_no), run_time=0.8)
        self.at("removed")
        self.play(Indicate(items[2], color=TEXT, scale_factor=1.25), l_no.animate.set_color(GOLD), run_time=0.9)
        self.at("genetically")
        l_g = tm.L("removed genetically", 1.95, ROOF_Y - 0.58, TEXT, 26, "l")
        self.play(FadeIn(l_g, shift=LEFT * 0.15), run_time=0.6)
        self.finish()


class S14Reveal2(SpokenScene):
    def construct(self):
        tm, items, q = predict_items(False)
        l_no = tm.L("no roof plate", 1.95, ROOF_Y, TEXT, SZ, "l")
        cit = lab("Lee, Dietrich and\nJessell, 2000", -6.5, 0.3, SOFT, SZ, "l", line_spacing=0.95)
        items[3] = l_no
        self.add(*items, cit)
        rl = items[1]                                   # dorsal row labels: dI6 first ... dI1 last
        lab_of = {i: rl[k] for k, i in enumerate(DORSAL_ROWS)}
        self.at("three", lead=0.0)
        self.play(*[Indicate(c, color=TEXT, scale_factor=1.06) for i in LOST_ROWS for c in tm.rows[i]], run_time=1.0)
        self.at("later")
        b1 = Line([1.95, ry(10) + 0.2, 0], [1.95, ry(8) - 0.2, 0], color=TEXT, stroke_width=4)
        t1 = lab("lost", 2.25, ry(9), TEXT, 32, "l", weight=BOLD)
        fade = []
        for i in LOST_ROWS:
            fade += [c.animate.set_fill(BG, 0.0).set_stroke(GREY, 2, opacity=0.5) for c in tm.rows[i]]
            fade.append(lab_of[i].animate.set_opacity(0.35))
        self.play(*fade, FadeIn(b1), FadeIn(t1), run_time=1.2)
        self.at("classes further")
        self.play(*[Indicate(c, color=TEXT, scale_factor=1.06) for i in KEPT_ROWS for c in tm.rows[i]], run_time=1.0)
        self.at("did not")
        b2 = Line([1.95, ry(7) + 0.2, 0], [1.95, ry(5) - 0.2, 0], color=TEXT, stroke_width=4)
        t2 = lab("still form", 2.25, ry(6) + 0.2, TEXT, 32, "l", weight=BOLD)
        self.play(FadeIn(b2), FadeIn(t2), run_time=0.6)
        self.at("in that")
        t3 = lab("in that experiment", 2.25, ry(6) - 0.26, TEXT, SZ, "l")
        self.play(FadeIn(t3, shift=LEFT * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def altered_anims(tm):
    out = []
    for i, r in enumerate(tm.rows):
        col, op = blend(i, 1.0, 2.6)
        if 3 <= i <= 8:
            op *= 0.8
        out += [c.animate.set_stroke(col, 3).set_fill(col, op) for c in r]
    return out


class S15Oppose(SpokenScene):
    def construct(self):
        tm = TM(epi=False)
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_roof())
        self.add(tm.g, labs)
        ys = VGroup(*[arr([x, FLOOR_Y + 0.2, 0], [x, -0.3, 0], YELLOW, 9, 0.25) for x in (-0.78, 0.78)])
        bs = VGroup(*[arr([x, ROOF_Y - 0.2, 0], [x, 0.55, 0], DORSAL, 9, 0.25) for x in (-0.78, 0.78)])
        c_s = chip("Shh", YELLOW, SZ).move_to([3.4, -1.45, 0])
        k_s = Line([2.8, -1.5, 0], [0.8, FLOOR_Y + 0.05, 0], color=YELLOW, stroke_width=3)
        c_b = chip("BMP", DORSAL, SZ).move_to([3.4, 1.75, 0])
        k_b = Line([2.8, 1.8, 0], [0.8, ROOF_Y - 0.05, 0], color=DORSAL, stroke_width=3)
        self.at("the two", lead=0.2)
        self.play(FadeIn(c_s, shift=LEFT * 0.2), Create(k_s), FadeIn(c_b, shift=LEFT * 0.2), Create(k_b),
                  *tm.tint_anims(1.0, 1.0),
                  LaggedStart(*[GrowArrow(a) for a in ys], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in bs], lag_ratio=0.2), run_time=1.3)
        self.at("oppose")
        self.play(Flash(tm.P(-0.78, 0.17), color=TEXT, flash_radius=0.55), Flash(tm.P(0.78, 0.17), color=TEXT, flash_radius=0.55), run_time=0.8)
        self.at("alters")
        cap = lab("BMP changes\nhow cells\nanswer Shh", 2.45, 0.35, TEXT, 30, "l", line_spacing=0.95)
        self.play(*altered_anims(tm), FadeIn(cap, shift=LEFT * 0.15),
                  *[a.animate.put_start_and_end_on(a.get_start(), [a.get_start()[0], -1.0, 0]) for a in ys],
                  *[a.animate.put_start_and_end_on(a.get_start(), [a.get_start()[0], -0.1, 0]) for a in bs], run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
G_LAM = 2.2
GX0, GSC = 1.7, 4.4


def GA(y):
    return float(np.exp(-(y - FLOOR_Y) / G_LAM))


def BA(y):
    return float(np.exp(-(ROOF_Y - y) / G_LAM))


def curve_pts(f, y0, y1, n=60):
    return [np.array([GX0 + GSC * f(y), y, 0]) for y in np.linspace(y0, y1, n)]


class S16Oppose2(SpokenScene):
    def construct(self):
        tm = TM(epi=False)
        tm.tint_now(1.0, 1.0)
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_roof())
        whole = VGroup(tm.g, labs)
        self.add(whole)
        OX = -3.8
        # axes: vertical = position in the tube (aligned with the rows), horizontal = signal level
        y_lo, y_hi = FLOOR_Y, ROOF_Y
        vax = Line([GX0, -2.75, 0], [GX0, 3.0, 0], color=SOFT, stroke_width=3)
        hax = Line([GX0, -2.75, 0], [GX0 + 4.7, -2.75, 0], color=SOFT, stroke_width=3)
        v_title = T("position in\nthe tube", SZ, SOFT, line_spacing=0.9).rotate(PI / 2).move_to([0.75, 1.55, 0])
        l_dor = lab("dorsal", GX0 - 0.15, 2.95, SOFT, SZ, "r")
        l_ven = lab("ventral", GX0 - 0.15, -2.1, SOFT, SZ, "r")
        l_low = lab("low", GX0 + 0.1, -3.2, SOFT, 26, "l")
        l_sig = lab("signal level", GX0 + 2.4, -3.2, SOFT, SZ)
        l_high = lab("high", GX0 + 4.6, -3.2, SOFT, 26, "r")
        gp = curve_pts(GA, y_lo, y_hi)
        bp = curve_pts(BA, y_lo, y_hi)
        gc = VMobject(stroke_color=YELLOW, stroke_width=7).set_points_smoothly(gp)
        bc = VMobject(stroke_color=DORSAL, stroke_width=7).set_points_smoothly(bp)
        self.play(whole.animate.shift(RIGHT * OX), run_time=0.7)
        quick = AnimationGroup(Create(vax), Create(hax), FadeIn(v_title), FadeIn(l_dor), FadeIn(l_ven),
                               FadeIn(l_low), FadeIn(l_sig), FadeIn(l_high), run_time=0.7)
        self.play(quick, Create(gc, run_time=1.2))
        self.at("below", lead=0.4)
        l_g = lab("from below", GX0 + 1.0, -1.9, YELLOW, SZ, "l", weight=BOLD)
        self.play(FadeIn(l_g, shift=LEFT * 0.1), run_time=0.4)
        self.at("above", lead=0.2)
        l_b = lab("from above", GX0 + 1.0, 2.35, DORSAL, SZ, "l", weight=BOLD)
        self.play(AnimationGroup(FadeIn(l_b, shift=LEFT * 0.1), run_time=0.5), Create(bc, run_time=1.3))
        self.at("cells in")
        rb = tm.row_box(5)
        rb.shift(RIGHT * OX)
        self.play(Create(rb), run_time=0.5)
        self.at("shaped")
        yc = ry(5)
        xc = GX0 + GSC * GA(yc)
        dl = DashedLine([-2.05, yc, 0], [xc - 0.3, yc, 0], color=TEXT, stroke_width=3)
        d1 = dot(xc, yc, YELLOW, 0.15)
        ring = Circle(radius=0.27, stroke_color=DORSAL, stroke_width=6).move_to([xc, yc, 0])
        self.play(Create(dl), run_time=0.5)
        self.play(FadeIn(ring, scale=0.3), FadeIn(d1, scale=0.3), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
FACT = {"p3": "Nkx2.2", "pMN": "Olig2", "p2": "Irx3 · Nkx6.1", "p1": "Dbx2", "p0": "Dbx1"}


class S17Code(SpokenScene):
    def construct(self):
        tm = TM(epi=False, roof=False, floor=False, noto=False)
        tm.tint_now(1.0, 1.0)
        self.add(tm.g)
        self.at("ventral", lead=0.3)
        rl = VGroup(*[tm.rowlab(i) for i in VENTRAL_ROWS])
        fc = VGroup(*[mlab(FACT[ROWN[i]], 1.95, ry(i), ROWCOL[ROWN[i]], SZ, "l") for i in VENTRAL_ROWS])
        bk = Line([-3.15, ry(4) + 0.2, 0], [-3.15, ry(0) - 0.2, 0], color=TEXT, stroke_width=4)
        cv = lab("ventral:\nin full", -3.4, ry(2), TEXT, 30, "r", weight=BOLD, line_spacing=0.95)
        self.play(*[c.animate.set_stroke(NEUT_STROKE, 3).set_fill(NEUT_FILL, NEUT_O) for i in DORSAL_ROWS for c in tm.rows[i]],
                  LaggedStart(*[AnimationGroup(*tm.style_anims([i])) for i in reversed(VENTRAL_ROWS)], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(l) for l in rl], lag_ratio=0.1), FadeIn(bk), FadeIn(cv), run_time=0.8)
        self.at("full")
        hd = lab("marker factors, for example", 1.95, ry(4) + 0.62, SOFT, 26, "l")
        self.play(FadeIn(hd), LaggedStart(*[FadeIn(f, shift=LEFT * 0.15) for f in fc], lag_ratio=0.2), run_time=1.0)
        self.at("dorsal")
        outs = VGroup()
        for i in DORSAL_ROWS:
            for c in tm.rows[i]:
                outs.add(DashedVMobject(RoundedRectangle(corner_radius=0.07, width=1.2 * tm.s, height=0.36 * tm.s, stroke_color=DORSAL, stroke_width=3.5).move_to(c), num_dashes=22))
        dl = VGroup(*[tm.rowlab(i) for i in DORSAL_ROWS])
        bk2 = Line([-3.15, ry(10) + 0.2, 0], [-3.15, ry(5) - 0.2, 0], color=TEXT, stroke_width=4)
        cd = lab("dorsal:\nin outline", -3.4, ry(7.5), TEXT, 30, "r", weight=BOLD, line_spacing=0.95)
        self.play(*[c.animate.set_stroke(DORSAL, 2, opacity=0.25).set_fill(BG, 0.0) for i in DORSAL_ROWS for c in tm.rows[i]],
                  LaggedStart(*[Create(o) for o in outs], lag_ratio=0.04), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(l) for l in dl], lag_ratio=0.1), FadeIn(bk2), FadeIn(cd), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
CA, CB = -3.2, 3.2
CP = 0.5


def col_y(i):
    return -2.5 + CP * i


def col_cell(x, i, color, o, w=1.8):
    return RoundedRectangle(corner_radius=0.06, width=w, height=CP - 0.05, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=o).move_to([x, col_y(i), 0])


class S18Rule(SpokenScene):
    def construct(self):
        head = T("The whole rule", 46, TEXT, font=TITLE_FONT).move_to([0, 3.35, 0])
        colA = VGroup(*[col_cell(CA, i, NEUT_STROKE, NEUT_O).set_fill(NEUT_FILL, NEUT_O) for i in range(NR)])
        colA.shift(RIGHT * -CA)
        self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(colA, lag_ratio=0.05), run_time=0.9)
        self.at("neighbors")
        self.play(LaggedStart(*[c.animate.set_stroke(blend(i)[0], 3).set_fill(blend(i)[0], blend(i)[1]) for i, c in enumerate(colA)], lag_ratio=0.1),
                  run_time=0.95)
        tA = lab("The neighbors supply a slope.", 0, -3.3, TEXT, SZ)
        self.at("slope")
        self.play(FadeIn(tA, shift=UP * 0.1), run_time=0.5)
        self.at("progenitors", lead=0.3)
        colB = VGroup(*[col_cell(CB, i, blend(i)[0], blend(i)[1]) for i in range(NR)])
        ar = arr([CA + 1.15, 0.0, 0], [CB - 1.15, 0.0, 0], GREY, 7, 0.3)
        self.play(VGroup(colA, tA).animate.shift(RIGHT * CA), FadeIn(colB, shift=RIGHT * 0.2), GrowArrow(ar), run_time=0.8)
        self.at("draw")
        tB = lab("The progenitors draw the lines.", CB, -3.3, TEXT, SZ)
        self.play(*[colB[i].animate.set_stroke(row_style(i)[0], 3).set_fill(row_style(i)[0], row_style(i)[1]) for i in range(NR)],
                  FadeIn(tB, shift=UP * 0.1), run_time=1.0)
        seps = VGroup(*[Line([CB - 1.05, col_y(i) - CP / 2, 0], [CB + 1.05, col_y(i) - CP / 2, 0], color=TEXT, stroke_width=3.5)
                        for i in (1, 2, 5)])
        self.play(Create(seps), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S19Rule2(SpokenScene):
    def construct(self):
        S, OX = 0.9, -4.85
        tm = TM(ox=OX, oy=-0.05, s=S, epi=False)
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_roof())
        self.add(tm.g, labs)
        ups = VGroup(*[arr(tm.P(x, FLOOR_Y + 0.2), tm.P(x, -0.4), YELLOW, 8, 0.2) for x in (-0.78, 0.78)])
        dns = VGroup(*[arr(tm.P(x, ROOF_Y - 0.2), tm.P(x, 1.0), DORSAL, 8, 0.2) for x in (-0.78, 0.78)])
        self.at("signals", lead=0.0)
        self.play(*tm.tint_anims(1.0, 1.0), run_time=0.8)
        self.at("below")
        self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.2), run_time=0.5)
        self.at("above")
        self.play(LaggedStart(*[GrowArrow(a) for a in dns], lag_ratio=0.2), run_time=0.4)
        # level dial
        P = np.array([0.3, 1.0, 0])
        arc = Arc(radius=1.05, start_angle=0, angle=PI, arc_center=P, stroke_color=GREY, stroke_width=6)
        ticks = VGroup(*[Line(P + 1.05 * np.array([np.cos(a), np.sin(a), 0]), P + 0.87 * np.array([np.cos(a), np.sin(a), 0]),
                              color=GREY, stroke_width=3) for a in np.linspace(0, PI, 7)])
        needle = Line(P, P + 0.9 * np.array([np.cos(2.7), np.sin(2.7), 0]), color=TEXT, stroke_width=6)
        l_lv = lab("level", P[0], P[1] - 0.8, TEXT, SZ)
        l_lo = lab("low", P[0] - 1.1, P[1] - 0.25, SOFT, 26, "c")
        l_hi = lab("high", P[0] + 1.1, P[1] - 0.25, SOFT, 26, "c")
        self.at("set the")
        approx = lab("to a first approximation", 0.3, 3.3, GOLD, 30, weight=BOLD)
        self.play(FadeIn(arc), FadeIn(ticks), FadeIn(needle), FadeIn(l_lv), FadeIn(l_lo), FadeIn(l_hi), FadeIn(approx, shift=DOWN * 0.1), run_time=0.6)
        self.play(Rotate(needle, angle=-1.3, about_point=P), run_time=0.8)
        # clock
        cc = np.array([0.3, -1.35, 0])
        face = Circle(radius=0.85, stroke_color=GREY, stroke_width=6, fill_color=BG, fill_opacity=0.9).move_to(cc)
        hand = Line(cc, cc + np.array([0, 0.68, 0]), color=TEXT, stroke_width=6)
        cticks = VGroup(*[Line(cc + 0.85 * np.array([np.sin(a), np.cos(a), 0]), cc + 0.7 * np.array([np.sin(a), np.cos(a), 0]),
                               color=GREY, stroke_width=3) for a in np.linspace(0, 2 * PI, 12, endpoint=False)])
        l_t = lab("how long", cc[0], cc[1] - 1.45, TEXT, SZ)
        l_sh = lab("short", cc[0] - 0.8, cc[1] - 1.0, SOFT, 26, "c")
        l_lg = lab("long", cc[0] + 0.8, cc[1] - 1.0, SOFT, 26, "c")
        self.at("how long")
        self.play(FadeIn(face), FadeIn(cticks), FadeIn(hand), FadeIn(l_t), FadeIn(l_sh), FadeIn(l_lg), run_time=0.5)
        self.play(Rotate(hand, angle=-2 * PI * 0.55, about_point=cc), run_time=1.0)
        # address box
        box = RoundedRectangle(corner_radius=0.2, width=3.5, height=5.0, stroke_color=TEXT, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([4.95, 0.0, 0])
        a1 = arr([1.65, 1.3, 0], [3.1, 0.8, 0], GREY, 5, 0.22)
        a2 = arr([1.3, -1.35, 0], [3.1, -0.5, 0], GREY, 5, 0.22)
        t_ex = lab("for example: pMN", 4.95, 2.05, GOLD, 26, weight=BOLD)
        self.at("answer")
        self.play(Create(box), GrowArrow(a1), GrowArrow(a2), FadeIn(t_ex), run_time=0.8)
        chips = VGroup(fchip("Nkx6.1", ORANGE, SZ), fchip("Olig2", GREEN, SZ), fchip("Pax6 low", BLUE, SZ)).arrange(DOWN, buff=0.28).move_to([4.95, 0.1, 0])
        l_f = lab("combination\nof factors", 4.95, -1.85, TEXT, SZ, line_spacing=0.95)
        self.at("combination")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in chips], lag_ratio=0.2), FadeIn(l_f), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
BX0, BX1 = -5.0, -1.8
BCX = (BX0 + BX1) / 2
BANDS = {"p3": (-2.5, -1.5), "pMN": (-1.5, -0.5), "p2": (-0.5, 0.5), "p1": (0.5, 1.5), "p0": (1.5, 2.5)}
BCOL = {"p3": ORANGE, "pMN": GREEN, "p2": TEXT, "p1": TEXT, "p0": TEXT}


def slot_rect(a, b, col, fill, sw=3):
    return Rectangle(width=BX1 - BX0, height=b - a - 0.05, stroke_color=col, stroke_width=sw, fill_color=col, fill_opacity=fill).move_to([BCX, (a + b) / 2, 0])


def pair_panel(y, name_l, col_l, name_r, col_r, xl=0.0, xr=3.9):
    cl, cr = fchip(name_l, col_l, SZ), fchip(name_r, col_r, SZ)
    cl.move_to([xl, y, 0])
    cr.move_to([xr, y, 0])
    x1, x2 = cl.get_right()[0] + 0.1, cr.get_left()[0] - 0.1
    b1 = inhib([x1, y + 0.17, 0], [x2, y + 0.17, 0], RED, 5, 0.14)
    b2 = inhib([x2, y - 0.17, 0], [x1, y - 0.17, 0], RED, 5, 0.14)
    return cl, cr, VGroup(b1, b2)


class S21Rule4(SpokenScene):
    def construct(self):
        names = list(BANDS)
        soft = {}
        for n in names:
            a, b = BANDS[n]
            soft[n] = slot_rect(a - 0.3, b + 0.3, BCOL[n], 0.2, 2)
            soft[n].set_stroke(BCOL[n], 2, opacity=0.35)
        labs = VGroup(*[lab(n, BX0 - 0.15, sum(BANDS[n]) / 2, BCOL[n], SZ, "r", font=MONO, weight=BOLD) for n in names])
        self.play(*[FadeIn(s) for s in soft.values()], FadeIn(labs), run_time=0.7)
        self.at("pairs")
        # pair 1 sits on the p3 / pMN border, pair 2 on the pMN / p2 border
        l1, r1, bars1 = pair_panel(-2.4, "Pax6", BLUE, "Nkx2.2", ORANGE)
        l2, r2, bars2 = pair_panel(-0.1, "Irx3", BLUE, "Olig2", GREEN)
        ex1 = lab("for example", 1.95, -1.78, SOFT, 26)
        ex2 = lab("for example", 1.95, 0.6, SOFT, 26)
        ld1 = DashedLine([BX1 + 0.02, -1.5, 0], [l1.get_left()[0] - 0.05, -2.4, 0], color=SOFT, stroke_width=2.5)
        ld2 = DashedLine([BX1 + 0.02, -0.5, 0], [l2.get_left()[0] - 0.05, -0.1, 0], color=SOFT, stroke_width=2.5)
        self.play(FadeIn(l1, shift=RIGHT * 0.2), FadeIn(r1, shift=LEFT * 0.2), Create(ld1), FadeIn(ex1), run_time=0.7)
        self.at("neighboring")
        self.play(FadeIn(l2, shift=RIGHT * 0.2), FadeIn(r2, shift=LEFT * 0.2), Create(ld2), FadeIn(ex2), run_time=0.7)
        self.at("repress", lead=0.3)
        crisp = {n: slot_rect(*BANDS[n], BCOL[n], 0.4) for n in names}
        self.play(Create(bars1), Create(bars2), *[Transform(soft[n], crisp[n]) for n in names], run_time=1.1)
        self.at("each cell")
        cell_y, cell_x = -1.3, BCX
        cell = Rectangle(width=0.9, height=0.34, stroke_color=TEXT, stroke_width=5, fill_color=GREEN, fill_opacity=0.75).move_to([cell_x, cell_y, 0])
        lead = DashedLine([cell_x + 0.47, cell_y, 0], [-1.45, cell_y, 0], color=TEXT, stroke_width=3)
        cap1 = lab("one cell", -1.35, cell_y, TEXT, 30, "l", weight=BOLD)
        self.play(FadeIn(cell, scale=1.5), Create(lead), FadeIn(cap1, shift=LEFT * 0.1), run_time=0.7)
        self.at("one identity")
        cap2 = lab("one identity", -1.35, cell_y, TEXT, 30, "l", weight=BOLD)
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)
        self.at("hold")
        self.play(Indicate(cell, color=TEXT, scale_factor=1.15), run_time=0.7)
        self.at("though")
        sg = arr([6.3, 1.9, 0], [6.3, -2.2, 0], YELLOW, 11, 0.38)
        l_s = lab("more Shh,\nlonger", 6.0, -3.35, YELLOW, SZ, "c", line_spacing=0.95)
        self.play(GrowArrow(sg), FadeIn(l_s), run_time=1.0)
        self.at("move it", lead=0.4)
        cap3 = lab("new identity", -1.35, cell_y, ORANGE, 30, "l", weight=BOLD)
        self.play(cell.animate.set_fill(ORANGE, 0.8),
                  ReplacementTransform(cap2, cap3), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tag(text, x, y, color=GOLD, w=4.1):
    t = T(text, 26, TEXT, line_spacing=0.95).move_to([x, y, 0])
    b = RoundedRectangle(corner_radius=0.14, width=w, height=t.height + 0.34, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.1).move_to(t)
    return VGroup(b, t)


class S22Limits(SpokenScene):
    def construct(self):
        hdr_t = lab("The neighbors supply a slope. The progenitors draw the lines.", 0, 3.3, TEXT, 26)
        hdr = VGroup(RoundedRectangle(corner_radius=0.16, width=hdr_t.width + 0.7, height=0.72, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.07).move_to(hdr_t), hdr_t)
        self.add(hdr)
        xs = (-4.4, 0.0, 4.4)
        BY, TY = -1.45, -2.75
        self.at("keep", lead=0.0)
        self.play(Indicate(hdr[0], color=GOLD, scale_factor=1.02), run_time=0.8)
        # 1: sharp is not accurate
        self.at("sharp")
        x = xs[0]
        base = Line([x - 1.9, BY, 0], [x + 1.9, BY, 0], color=GREY, stroke_width=3)
        drawn = Line([x - 1.2, BY, 0], [x - 1.2, BY + 3.3, 0], color=TEXT, stroke_width=8)
        true = DashedLine([x + 1.2, BY, 0], [x + 1.2, BY + 3.3, 0], color=GOLD, stroke_width=6, dash_length=0.16)
        l_d = lab("drawn line", x - 1.2, BY + 3.65, TEXT, SZ)
        l_t = lab("true position", x + 1.2, BY + 3.65, GOLD, SZ)
        off = DoubleArrow([x - 1.2, BY + 1.6, 0], [x + 1.2, BY + 1.6, 0], color=SOFT, stroke_width=5, tip_length=0.2, buff=0)
        self.play(Create(base), Create(drawn), FadeIn(l_d), run_time=0.6)
        t1 = tag("Sharp is not the same\nas accurate", x, TY)
        self.play(Create(true), FadeIn(l_t), GrowFromCenter(off), FadeIn(t1, shift=UP * 0.1), run_time=0.9)
        # 2: signal shapes its own slope
        self.at("signal")
        x = xs[1]
        pf = lambda t: np.array([x - 1.6 + t * 3.2, BY + 3.3 * np.exp(-t * 3.0), 0])
        crv = VMobject(stroke_color=YELLOW, stroke_width=8).set_points_smoothly([pf(t) for t in np.linspace(0, 1, 40)])
        bs2 = Line([x - 1.7, BY, 0], [x + 1.7, BY, 0], color=GREY, stroke_width=3)
        loop = CurvedArrow(pf(0.62) + np.array([0, -0.15, 0]), pf(0.07) + np.array([0.15, -0.55, 0]), color=GOLD, angle=-1.6, stroke_width=6, tip_length=0.25)
        self.play(Create(bs2), Create(crv), run_time=0.7)
        t2 = tag("The signal shapes\nits own slope", x, TY)
        self.play(Create(loop), FadeIn(t2, shift=UP * 0.1), run_time=0.9)
        # 3: floor plate
        self.at("and the floor", lead=0.2)
        x = xs[2]
        fp = bar(x, BY + 1.6, 3.4, 0.8, TEAL, 0.6)
        fpl = lab("floor plate", x, BY + 1.6, TEXT, SZ)
        ring = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=4.1, height=1.5, stroke_color=GOLD, stroke_width=4), num_dashes=44).move_to(fp)
        t3 = tag("The floor plate follows\npartly different rules", x, TY)
        self.play(GrowFromCenter(fp), FadeIn(fpl), run_time=0.6)
        self.play(Create(ring), FadeIn(t3, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def axon_pts(side):
    return [np.array([side * 0.78, ry(7), 0]), np.array([side * 1.2, ry(6) - 0.2, 0]), np.array([side * 1.28, ry(3), 0]),
            np.array([side * 1.0, ry(0) - 0.15, 0]), np.array([side * 0.6, FLOOR_Y + 0.3, 0]), np.array([side * 0.25, FLOOR_Y + 0.02, 0]), np.array([-side * 0.2, FLOOR_Y, 0])]


class S23Bridge(SpokenScene):
    def construct(self):
        tm = TM(epi=False, roof=False)
        tm.style_now(DORSAL_ROWS + VENTRAL_ROWS)
        labs = VGroup(tm.l_floor(), tm.l_noto())
        self.add(tm.g, labs)
        self.at("later", lead=0.2)
        somas = VGroup(*[dot(s * 0.78, ry(7), TEXT, 0.17, 0.95) for s in (-1, 1)])
        self.play(FadeIn(somas, scale=0.5), run_time=0.4)
        self.at("same floor")
        g = RoundedRectangle(corner_radius=0.2, width=2.0, height=0.65, stroke_width=0, fill_color=TEAL, fill_opacity=0.0).move_to(tm.fl)
        self.add(g)
        self.play(g.animate.set_fill(TEAL, 0.55), Indicate(tm.fl, color=TEAL, scale_factor=1.3), run_time=0.3)
        self.at("floor plate", lead=0.2)
        paths = [VMobject(stroke_color=TEXT, stroke_width=5).set_points_smoothly(axon_pts(s)) for s in (-1, 1)]
        cones = [Dot(p.get_start(), radius=0.13, color=TEXT) for p in paths]
        ring = Circle(radius=0.55, stroke_color=TEXT, stroke_width=4).move_to([0, FLOOR_Y, 0])
        ring2 = Circle(radius=0.3, stroke_color=TEXT, stroke_width=4).move_to([0, FLOOR_Y, 0])
        l_ax = VGroup(lab("growing axon", 1.95, 0.3, TEXT, SZ, "l"), lab("growing axon", -1.95, 0.3, TEXT, SZ, "r"))
        lk = VGroup(Line([1.9, 0.3, 0], [1.3, 0.3, 0], color=TEXT, stroke_width=3), Line([-1.9, 0.3, 0], [-1.3, 0.3, 0], color=TEXT, stroke_width=3))
        self.add(*cones)
        self.play(*[Create(p, run_time=3.4, rate_func=linear) for p in paths],
                  *[MoveAlongPath(c, p, run_time=3.4, rate_func=linear) for c, p in zip(cones, paths)],
                  Succession(Wait(1.1), AnimationGroup(Create(ring), Create(ring2), run_time=0.7)),
                  Succession(Wait(1.55), AnimationGroup(FadeIn(l_ax), FadeIn(lk), run_time=0.5)))
        self.finish()


class S24Takeaway(SpokenScene):
    def construct(self):
        tm = TM()
        labs = VGroup(tm.l_floor(), tm.l_noto(), tm.l_roof(), tm.l_epi())
        self.add(tm.g, labs)
        n = 14
        h = 4.8 / n
        gs = VGroup(*[Rectangle(width=0.42, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.08 + 0.8 * np.exp(-j / 4.5)).move_to([-4.9, -2.3 + h * (j + 0.5), 0]) for j in range(n)])
        gb = VGroup(*[Rectangle(width=0.42, height=h, stroke_width=0, fill_color=DORSAL, fill_opacity=0.08 + 0.8 * np.exp(-(n - 1 - j) / 4.5)).move_to([-4.35, -2.3 + h * (j + 0.5), 0]) for j in range(n)])
        l_gs = lab("Shh\nfrom below", -5.15, -2.95, YELLOW, SZ, "c", line_spacing=0.9)
        l_gb = lab("BMP and Wnt\nfrom above", -4.6, 3.0, DORSAL, SZ, "c", line_spacing=0.9)
        self.at("two slopes", lead=0.2)
        self.play(FadeIn(gs), FadeIn(gb), FadeIn(l_gs), FadeIn(l_gb), run_time=0.8)
        self.at("read by", lead=0.3)
        rl = VGroup(*[tm.rowlab(i) for i in reversed(range(NR))])
        self.play(LaggedStart(*[AnimationGroup(*tm.style_anims([i])) for i in range(NR)], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(l) for l in reversed(list(rl))], lag_ratio=0.1), run_time=1.1)
        l_t = lab("Two slopes,\nread by the cells,\nbecome the map\nof the spinal cord.", 2.55, 0.35, TEXT, 34, "l", line_spacing=1.0)
        self.at("cord", lead=0.2)
        self.play(FadeIn(l_t, shift=LEFT * 0.2), run_time=0.6)
        self.finish()


class S25End(EndCard):
    LINE = "Two slopes, read by the cells, become the spinal cord's map."
