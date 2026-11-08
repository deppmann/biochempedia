"""Chapter 3: Which Motor Neuron, and a Recipe  (Developmental Neuroscience, motor-neuron-code)

COLOR MAP (one colour per concept; shared with chapters 1 and 2 where the concept recurs)
  NEUTRAL (light grey-white) = a motor neuron / cell whose column is not yet assigned, and dish cells
  GREEN   = the lateral motor column (LMC), and only that
  GOLD    = generic Hox / positional information (retinoic acid)
  level colours (cord position, and the Hox protein that marks it):
            cervical pale gold, brachial PURPLE (Hoxc6), thoracic ORANGE (Hoxc9), lumbar PINK
  AZURE   = medial motor column (MMC)
  MAGENTA = preganglionic column (PGC)
  AQUA    = hypaxial column (HMC)
  TEXT    = FoxP1 and Lim1 (white, as Lhx1 in chapter 1)
  YELLOW  = Isl1 (and the axons of Isl1 cells)
  LIME    = hedgehog agonist, Mnx1, Eph receptors and ephrins (signals and markers, never a column)
  RED     = absent / deleted / suppressed / crossed out
  GREY    = tissue, structure, labels, "not yet assigned" outlines
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58AB5"
CERV = "#E8D27A"
BRACH = PURPLE
THOR = ORANGE
LUMB = PINK
AZURE = "#4EA3F2"      # MMC
MAGENTA = "#D96CE0"    # PGC
AQUA = "#2EC4B6"       # HMC
LIME = "#C5E04A"       # hedgehog, Mnx1, Eph, ephrins
NEUT = "#CBD0DA"       # unassigned motor neurons and dish cells
LEVELS = [("cervical", CERV), ("brachial", BRACH), ("thoracic", THOR), ("lumbar", LUMB)]


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def blunt(a, b, color=RED, w=5):
    """A repression symbol: a line that ends in a bar."""
    a = np.array(a, float)
    b = np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w), Line(b + n * 0.24, b - n * 0.24, color=color, stroke_width=w + 2))


def cross(center, w=1.0, h=0.7, color=RED, sw=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-w / 2, h / 2, 0], c + [w / 2, -h / 2, 0], color=color, stroke_width=sw),
                  Line(c + [-w / 2, -h / 2, 0], c + [w / 2, h / 2, 0], color=color, stroke_width=sw))


def neuron(pos, radius=0.7, color=NEUT):
    """A cell body with three short processes. A dark underlay hides anything drawn behind it."""
    pos = [pos[0], pos[1], 0]
    under = Circle(radius=radius, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(pos)
    body = Circle(radius=radius, color=color, stroke_width=4, fill_color=color, fill_opacity=0.18).move_to(pos)
    branches = VGroup(*[Line(body.get_center() + radius * np.array([np.cos(a), np.sin(a), 0]),
                              body.get_center() + radius * 1.5 * np.array([np.cos(a), np.sin(a), 0]),
                              color=color, stroke_width=3) for a in (2.3, 3.1, 3.9)])
    return VGroup(under, body, branches)


def cell_dot(p, color=NEUT, r=0.17, ring=None, op=0.6):
    d = Circle(radius=r, stroke_color=ring or color, stroke_width=4 if ring else 2.5, fill_color=color, fill_opacity=op)
    return d.move_to([p[0], p[1], 0])


def blob(c, r=0.8, color=NEUT):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, stroke_opacity=0.6,
                  fill_color=color, fill_opacity=0.07).move_to([c[0], c[1], 0])


OFFS = [(0.0, 0.0), (0.42, 0.18), (-0.4, 0.22), (0.18, -0.42), (-0.3, -0.36), (0.05, 0.52), (0.5, -0.28)]


def cluster_pts(c, n=6):
    return [(c[0] + dx, c[1] + dy) for dx, dy in OFFS[:n]]


def cluster(c, color=NEUT, n=6, ring=None):
    return VGroup(blob(c, 0.82, color), *[cell_dot(p, color, ring=ring) for p in cluster_pts(c, n)])


def muscle(pos, label="muscle", width=2.1, color=GREY, size=24):
    box = RoundedRectangle(width=width, height=0.72, corner_radius=0.3, color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.16).move_to([pos[0], pos[1], 0])
    return VGroup(box, T(label, size, color).move_to(box))


def route(start, end, via=None, color=GREEN, w=4, n=26):
    """An axon path computed from smooth-step interpolation (flat tangents at the joins)."""
    s = np.array(start, float)
    e = np.array(end, float)

    def seg(p, q):
        out = []
        for t in np.linspace(0, 1, n):
            u = t * t * (3 - 2 * t)
            out.append([p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * u, 0])
        return out

    pts = seg(s, np.array(via, float)) + seg(np.array(via, float), e)[1:] if via is not None else seg(s, e)
    m = VMobject(color=color, stroke_width=w)
    m.set_points_smoothly(pts)
    return m


# ---- the side view of the cord -----------------------------------------------------------------
XB = [-6.2, -3.7, -0.7, 3.0, 6.2]            # level boundaries (unequal, as in a real cord)
CORD_Y = 0.35
CORD_H = 4.4


def cord_x(i):
    return (XB[i] + XB[i + 1]) / 2


def cord(y=CORD_Y, h=CORD_H, op=0.30, axis=False):
    outline = RoundedRectangle(width=12.4, height=h, corner_radius=0.5, stroke_color=GREY, stroke_width=3,
                               fill_opacity=0).move_to([0, y, 0])
    segs = VGroup()
    for i, (_, col) in enumerate(LEVELS):
        r = Rectangle(width=XB[i + 1] - XB[i], height=h, stroke_width=0, fill_color=col, fill_opacity=op).move_to([cord_x(i), y, 0])
        if i in (0, 3):
            r = Intersection(r, outline.copy(), stroke_width=0, fill_color=col, fill_opacity=op)
        segs.add(r)
    seams = VGroup(*[Line([x, y + h / 2, 0], [x, y - h / 2, 0], color=GREY, stroke_width=2, stroke_opacity=0.5) for x in XB[1:4]])
    labels = VGroup(*[T(n, 28, c).move_to([cord_x(i), y + h / 2 + 0.4, 0]) for i, (n, c) in enumerate(LEVELS)])
    g = VGroup(segs, seams, outline, labels)
    if axis:
        g.add(cord_axis())
    return g


def cord_axis(y=-3.25):
    line = Arrow([-3.0, y, 0], [3.0, y, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.22)
    r = T("rostral (head)", 26, GREY).move_to([-4.9, y, 0])
    c = T("caudal (tail)", 26, GREY).move_to([4.9, y, 0])
    return VGroup(line, r, c)


# ---- the half cross-section --------------------------------------------------------------------
def half_section():
    sec = Sector(radius=2.8, angle=PI, start_angle=-PI / 2, stroke_color=GREY, stroke_width=3,
                 fill_color=GREY, fill_opacity=0.10)
    sec.stretch(1.9, 0, about_point=ORIGIN)
    sec.shift(LEFT * 6.2)
    mid = DashedLine([-6.2, 2.8, 0], [-6.2, -2.8, 0], color=GREY, stroke_width=3, dash_length=0.18)
    mlab = T("midline", 24, GREY).move_to([-6.0, -3.4, 0])
    dors = T("dorsal", 26, GREY).move_to([-4.3, 3.25, 0])
    vent = T("ventral", 26, GREY).move_to([-3.6, -3.4, 0])
    return VGroup(sec, mid, mlab, dors, vent)


MMC_C = (-5.0, -0.5)
LMC_C = (-3.3, -1.25)
PGC_C = (-3.5, 0.8)
MMC_LABEL_POS = (-5.0, -1.95)
LMC_LABEL_POS = (-2.95, 0.1)
SEC_TAG = (-1.2, 3.35)


def column_label(acr, name, color, pos, size=22):
    return VGroup(T(acr, 28, color, weight=BOLD), T(name, size, color, line_spacing=0.6)).arrange(DOWN, buff=0.06).move_to([pos[0], pos[1], 0])


# ---- the full cross-section (prediction scenes) ------------------------------------------------
def full_section(cy=-0.1):
    ell = Ellipse(width=8.6, height=5.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.10).move_to([0, cy, 0])
    mid = DashedLine([0, cy + 2.7, 0], [0, cy - 2.7, 0], color=GREY, stroke_width=2, dash_length=0.16)
    return VGroup(ell, mid)


PROG_X = 0.5
PROG_YS = [1.45, 1.0, 0.55, 0.1, -0.35, -0.8, -1.25]
RIGHT_MN = (2.7, -0.85)
LEFT_MN = (-2.7, -0.85)
RLAB = (2.7, 0.45)
LLAB = (-2.7, 0.45)


def progenitors(side, color=NEUT, ring=None):
    return VGroup(*[cell_dot([side * PROG_X, y], color, r=0.15, ring=ring, op=0.5) for y in PROG_YS])


# ---- the limb ----------------------------------------------------------------------------------
LIMB_C = (3.9, 0.0)


def limb(labels=True):
    outline = RoundedRectangle(width=5.4, height=5.6, corner_radius=0.8, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.07).move_to([LIMB_C[0], LIMB_C[1], 0])
    split = DashedLine([1.2, 0, 0], [6.6, 0, 0], color=GREY, stroke_width=2, dash_length=0.16).set_stroke(opacity=0.55)
    dl = T("dorsal", 26, GREY).move_to([2.4, 2.4, 0])
    vl = T("ventral", 26, GREY).move_to([2.4, -2.4, 0])
    return VGroup(outline, split, dl, vl) if labels else VGroup(outline, split)


# ---- zoomed limb column ------------------------------------------------------------------------
LZ_C = (-4.1, 0.0)
LZ_R = 2.5
LAT_DOTS = [(-2.9, 1.5), (-2.4, 0.75), (-2.9, 0.07)]
MED_DOTS = [(-5.55, 1.2), (-4.85, 0.35), (-5.6, -0.55), (-4.85, -1.15), (-5.45, -1.65)]


def lmc_zoom():
    big = Circle(radius=LZ_R, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.07).move_to([LZ_C[0], LZ_C[1], 0])
    div = DashedLine([LZ_C[0], LZ_R, 0], [LZ_C[0], -LZ_R, 0], color=GREY, stroke_width=2, dash_length=0.14)
    lat = VGroup(*[cell_dot(p, GREEN) for p in LAT_DOTS])
    med = VGroup(*[cell_dot(p, GREEN) for p in MED_DOTS])
    ll = T("lateral", 26, GREY).move_to([-2.9, -3.05, 0])
    ml = T("medial", 26, GREY).move_to([-5.3, -3.05, 0])
    lmc = T("LMC", 30, GREEN, weight=BOLD).move_to([-4.1, 3.05, 0])
    return dict(big=big, div=div, lat=lat, med=med, ll=ll, ml=ml, lmc=lmc)


VIA_D = [(0.7, 1.15), (0.7, 0.85), (0.7, 0.55)]
VIA_V = [(0.7, -0.55), (0.7, -0.85), (0.7, -1.15)]
LAT_AX_END = [(4.9, 1.4), (5.3, 2.0), (4.5, 0.8)]
MED_AX_END = [(4.9, -1.4), (5.3, -2.0), (4.5, -0.8)]
MED_START = [MED_DOTS[3], MED_DOTS[4], MED_DOTS[2]]
LIM_POS = (-3.4, 0.75)
ISL_POS = (-5.7, 3.05)


def lat_axons(color=TEXT, ends=None):
    ends = ends or LAT_AX_END
    return VGroup(*[route([LAT_DOTS[i][0] + 0.2, LAT_DOTS[i][1]], ends[i], VIA_D[i], color, 4) for i in range(3)])


def med_axons(color=YELLOW):
    return VGroup(*[route([MED_START[i][0] + 0.2, MED_START[i][1]], MED_AX_END[i], VIA_V[i], color, 4) for i in range(3)])


def tips(axons, color, r=0.11):
    return VGroup(*[Dot(a.get_end(), radius=r, color=color) for a in axons])


# ---- dishes ------------------------------------------------------------------------------------
DISH_X = [-4.6, 0.0, 4.6]
DISH_Y = 0.35
DISH_W = 3.8
DISH_H = 4.0
DISH_PTS = [(-0.9, 1.0), (0.1, 1.25), (1.0, 0.8), (-0.5, 0.0), (0.6, -0.2), (-1.0, -0.9), (0.0, -1.1), (1.0, -1.1)]


def dish(x, y=DISH_Y, cells=True, color=GREY, faint=False):
    op = 0.3 if faint else 1.0
    box = RoundedRectangle(width=DISH_W, height=DISH_H, corner_radius=0.6, stroke_color=color, stroke_width=4,
                           fill_color=GREY, fill_opacity=0.10).move_to([x, y, 0])
    box.set_stroke(opacity=op)
    if faint:
        box.set_fill(opacity=0.04)
    cs = VGroup(*[cell_dot([x + dx, y + dy], NEUT, r=0.3, op=0.4) for dx, dy in DISH_PTS])
    return VGroup(box, cs) if cells else VGroup(box)


# ---------------------------------------------------------------------------------------------
# title
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Transcription Factor Codes: Building a Motor Neuron"
    TITLE = "Which Motor Neuron, and a Recipe"


# ---------------------------------------------------------------------------------------------
# s01 the question
# ---------------------------------------------------------------------------------------------
class S01Q(SpokenScene):
    def construct(self):
        c = cord(axis=True)
        self.play(FadeIn(c), run_time=0.9)
        self.at("your neck")
        n1 = neuron([cord_x(0), CORD_Y], 0.95)
        l1 = T("neck", 30, NEUT).move_to([cord_x(0), -2.3, 0])
        self.play(FadeIn(n1, scale=0.6), FadeIn(l1), run_time=0.6)
        self.at("lower back")
        n2 = neuron([cord_x(3), CORD_Y], 0.95)
        l2 = T("lower back", 30, NEUT).move_to([cord_x(3), -2.3, 0])
        self.play(FadeIn(n2, scale=0.6), FadeIn(l2), run_time=0.6)
        self.at("tells them apart")
        line = DashedLine([cord_x(0) + 1.3, CORD_Y, 0], [cord_x(3) - 1.3, CORD_Y, 0], color=TEXT, stroke_width=4)
        q = VGroup(Circle(radius=0.65, stroke_color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1),
                   T("?", 64, TEXT)).move_to([0.0, CORD_Y, 0])
        q[1].move_to(q[0])
        self.play(Create(line), FadeIn(q, scale=0.6), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s02 Hox position
# ---------------------------------------------------------------------------------------------
def hox_stripes(y=CORD_Y, h=CORD_H):
    g = VGroup()
    for i, (_, col) in enumerate(LEVELS):
        w = XB[i + 1] - XB[i]
        n = int(w / 0.62)
        for k in range(n):
            x = cord_x(i) + (k - (n - 1) / 2) * 0.62
            g.add(Rectangle(width=0.22, height=h * 0.8, stroke_width=0, fill_color=col, fill_opacity=0.6).move_to([x, y, 0]).set_z_index(1))
    return g


class S02Hox(SpokenScene):
    def construct(self):
        c = cord(h=4.8, axis=True)
        n1 = neuron([cord_x(0), CORD_Y], 0.95).set_z_index(3)
        n2 = neuron([cord_x(3), CORD_Y], 0.95).set_z_index(3)
        l1 = T("neck", 30, NEUT).move_to([cord_x(0), -2.6, 0])
        l2 = T("lower back", 30, NEUT).move_to([cord_x(3), -2.6, 0])
        self.add(c, n1, n2, l1, l2)
        self.wait(0.2)
        self.at("along the cord")
        self.play(Indicate(c[0], color=TEXT, scale_factor=1.02), run_time=0.45)
        self.at("written in")
        st = hox_stripes(h=4.8)
        self.play(LaggedStart(*[FadeIn(s) for s in st], lag_ratio=0.03), run_time=0.6)
        self.at("hox proteins")
        lab = T("Hox proteins", 34, GOLD, weight=BOLD).move_to([-0.7, -2.6, 0])
        up = Arrow([-0.7, -2.3, 0], [-0.7, -1.7, 0], buff=0, color=GOLD, stroke_width=4, tip_length=0.2)
        self.play(FadeIn(lab), GrowArrow(up), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s03 columns
# ---------------------------------------------------------------------------------------------
SCATTER = [(-5.4, 1.9), (-4.4, 2.0), (-3.2, 1.5), (-2.1, 0.9), (-5.3, 0.2), (-3.9, 0.6),
           (-2.6, -0.2), (-4.6, -0.9), (-3.3, -1.5), (-2.0, -0.9), (-5.1, -1.8), (-4.0, -0.2)]


def sorted_targets():
    return cluster_pts(MMC_C, 6) + cluster_pts(LMC_C, 6)


def sec_tag(text, color=GREY):
    return T(text, 26, color).move_to([SEC_TAG[0], SEC_TAG[1], 0])


MMC_AX = dict(start=[MMC_C[0] + 0.1, MMC_C[1] + 0.8], end=[3.3, 2.0], via=[-4.0, 1.75])
BACK_POS = [4.6, 2.0, 0]
LIMBM_POS = [4.6, -1.75, 0]


def mmc_axon():
    return route(MMC_AX["start"], MMC_AX["end"], MMC_AX["via"], AZURE, 5)


def lmc_axon():
    return route([LMC_C[0] + 0.7, LMC_C[1]], [3.3, LIMBM_POS[1]], None, GREEN, 5)


class S03Cols(SpokenScene):
    def construct(self):
        strip = cord(axis=True)
        hl = SurroundingRectangle(strip[0][1], color=TEXT, buff=0.0, stroke_width=4)
        self.add(strip, hl)
        sec = half_section()
        dots = VGroup(*[cell_dot(p) for p in SCATTER])
        self.play(FadeOut(strip), FadeOut(hl), FadeIn(sec), FadeIn(dots), FadeIn(sec_tag("limb level")), run_time=1.0)
        self.at("sort into")
        tg = sorted_targets()
        mm = cluster(MMC_C, AZURE)
        lm = cluster(LMC_C, GREEN)
        anims = []
        for i, d in enumerate(dots):
            col = AZURE if i < 6 else GREEN
            anims.append(d.animate.move_to([tg[i][0], tg[i][1], 0]).set_color(col))
        self.play(*anims, FadeIn(mm[0]), FadeIn(lm[0]), run_time=1.3)
        self.at("medial column")
        ml = column_label("MMC", "medial column", AZURE, MMC_LABEL_POS)
        self.play(FadeIn(ml), run_time=0.5)
        self.at("drives back")
        bm = muscle(BACK_POS, "back muscles", 2.7)
        self.play(FadeIn(bm), run_time=0.4)
        self.play(Create(mmc_axon()), run_time=0.9)
        self.at("lateral column")
        ll = column_label("LMC", "lateral column", GREEN, LMC_LABEL_POS)
        self.play(FadeIn(ll), run_time=0.5)
        self.at("limb levels")
        self.play(Indicate(sec[0], color=GREEN, scale_factor=1.01), run_time=0.7)
        self.at("drives limb")
        lmu = muscle(LIMBM_POS, "limb muscles", 2.7)
        self.play(FadeIn(lmu), run_time=0.4)
        self.play(Create(lmc_axon()), run_time=0.9)
        self.finish()


def s03_final():
    sec = half_section()
    mm = cluster(MMC_C, AZURE)
    lm = cluster(LMC_C, GREEN)
    ml = column_label("MMC", "medial column", AZURE, MMC_LABEL_POS)
    ll = column_label("LMC", "lateral column", GREEN, LMC_LABEL_POS)
    bm = muscle(BACK_POS, "back muscles", 2.7)
    lmu = muscle(LIMBM_POS, "limb muscles", 2.7)
    return dict(sec=sec, tag=sec_tag("limb level"), mm=mm, lm=lm, ml=ml, ll=ll, bm=bm, ax=mmc_axon(), lmu=lmu, ax2=lmc_axon())


# ---------------------------------------------------------------------------------------------
# s04 preganglionic
# ---------------------------------------------------------------------------------------------
class S04Cols2(SpokenScene):
    def construct(self):
        p = s03_final()
        self.add(*p.values())
        newtag = sec_tag("thoracic level", THOR)
        pg = cluster(PGC_C, MAGENTA)
        pl = column_label("PGC", "preganglionic column", MAGENTA, (1.2, 1.55), 24)
        hm = cluster(LMC_C, AQUA)
        hl = column_label("HMC", "hypaxial column", AQUA, (1.0, -0.8), 24)
        hmu = muscle(LIMBM_POS, "body-wall muscles", 3.0, AQUA)
        hax = route([LMC_C[0] + 0.7, LMC_C[1]], [3.1, LIMBM_POS[1]], None, AQUA, 5)
        gang = VGroup(Ellipse(width=3.4, height=1.1, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18),
                      T("autonomic ganglion", 24, GREY)).move_to([4.6, 0.8, 0])
        ax = route([PGC_C[0] + 0.7, PGC_C[1]], [2.9, 0.8], None, MAGENTA, 5)
        self.play(FadeOut(p["lm"]), FadeOut(p["ll"]), FadeOut(p["lmu"]), FadeOut(p["ax2"]), FadeOut(p["tag"]),
                  FadeOut(p["bm"]), FadeOut(p["ax"]), p["mm"].animate.set_opacity(0.35), FadeOut(p["ml"]),
                  FadeIn(hm), FadeIn(hl), FadeIn(hmu), FadeIn(hax), FadeIn(newtag), run_time=0.4)
        self.play(FadeIn(pg), FadeIn(pl), run_time=0.3)
        self.at("column projects")
        self.play(FadeIn(gang, scale=0.8), run_time=0.4)
        self.play(Create(ax), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s05 Hox cross-repression
# ---------------------------------------------------------------------------------------------
class S05Cross(SpokenScene):
    def construct(self):
        cell = Ellipse(width=11.8, height=6.6, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.10).move_to([0, 0, 0])
        cl = T("inside one cell", 30, GREY).move_to([0, 2.65, 0])
        hox = chip("Hox", GOLD, 52).move_to([-4.0, 0, 0])
        g1 = chip("target gene", NEUT, 30).move_to([3.4, 1.35, 0])
        g2 = chip("target gene", NEUT, 30).move_to([3.4, -1.35, 0])
        self.play(FadeIn(cell), FadeIn(cl), FadeIn(hox, scale=0.7), FadeIn(g1), FadeIn(g2), run_time=0.9)
        self.at("repressors")
        b = blunt([hox.get_right()[0] + 0.15, 0.2, 0], [g1.get_left()[0] - 0.1, g1.get_center()[1] - 0.1, 0], RED)
        bl = T("represses", 30, RED).move_to([-0.1, 1.5, 0])
        self.play(Create(b), FadeIn(bl), run_time=0.7)
        self.at("activators")
        a = arr([hox.get_right()[0] + 0.15, -0.2, 0], [g2.get_left()[0] - 0.1, g2.get_center()[1] + 0.1, 0], GREEN)
        al = T("activates", 30, GREEN).move_to([-0.1, -1.5, 0])
        self.play(GrowArrow(a), FadeIn(al), run_time=0.7)
        self.at("hox c6", lead=1.1)
        c = cord(0.3, 4.8, 0.30)
        self.play(*[FadeOut(m) for m in (cell, cl, hox, g1, g2, b, bl, a, al)], run_time=0.5)
        self.play(FadeIn(c), run_time=0.5)
        self.at("hox c6", lead=0.1)
        h6 = chip("Hoxc6", BRACH, 36).move_to([cord_x(1), 0.7, 0])
        fl = T("forelimb levels", 26, BRACH).move_to([cord_x(1), -0.4, 0])
        self.play(FadeIn(h6, scale=0.7), FadeIn(fl), Indicate(c[0][1], color=BRACH, scale_factor=1.02), run_time=0.7)
        self.at("hox c9", lead=0.1)
        h9 = chip("Hoxc9", THOR, 36).move_to([cord_x(2), 0.7, 0])
        tl = T("thoracic levels", 26, THOR).move_to([cord_x(2), -0.4, 0])
        self.play(FadeIn(h9, scale=0.7), FadeIn(tl), Indicate(c[0][2], color=THOR, scale_factor=1.02), run_time=0.7)
        x1 = h6.get_right()[0] + 0.08
        x2 = h9.get_left()[0] - 0.08
        r1 = blunt([x1, 0.95, 0], [x2, 0.95, 0], RED)
        r2 = blunt([x2, 0.45, 0], [x1, 0.45, 0], RED)
        rl = T("repress each other", 32, RED).move_to([(x1 + x2) / 2 + 0.2, -1.4, 0])
        cr = T("Dasen, Liu and Jessell, 2003", 26, GREY).move_to([0, -3.2, 0])
        self.play(Create(r1), Create(r2), FadeIn(rl), FadeIn(cr), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s06 / s07 prediction 1
# ---------------------------------------------------------------------------------------------
def pred1_parts():
    sec = full_section()
    pl = progenitors(-1)
    pr = progenitors(1)
    pls = VGroup(T("progenitors", 26, GREY).move_to([-1.35, 1.9, 0]), T("progenitors", 26, GREY).move_to([1.35, 1.9, 0]))
    lm = cluster(LEFT_MN, GREEN)
    lml = T("LMC", 28, GREEN, weight=BOLD).move_to([LLAB[0], LLAB[1], 0])
    cl = T("control side", 26, GREY).move_to([-2.7, -3.15, 0])
    el = T("electroporated side", 26, GREY).move_to([2.7, -3.15, 0])
    title = T("Predict.", 40, GOLD, weight=BOLD).move_to([-5.5, 3.4, 0])
    ctag = T("chick, forelimb level", 28, GREY).move_to([0.8, 3.4, 0])
    quest = T("What column do they become?", 34, TEXT).move_to([0.9, 3.4, 0])
    hx = chip("Hoxc9", THOR, 30).move_to([5.6, 1.3, 0])
    ar = arr([4.55, 1.25, 0], [0.95, 1.0, 0], THOR, 4)
    pr_col = progenitors(1, ORANGE)
    rm = cluster(RIGHT_MN, NEUT, ring=ORANGE)
    q = T("?", 60, TEXT).move_to([RLAB[0], RLAB[1] + 0.05, 0])
    return dict(sec=sec, pl=pl, pr=pr, pls=pls, lm=lm, lml=lml, cl=cl, el=el, title=title, ctag=ctag, quest=quest,
                hx=hx, ar=ar, pr_col=pr_col, rm=rm, q=q)


PRED_FINAL = ("title", "sec", "pl", "pr_col", "pls", "lm", "lml", "cl", "el", "quest", "hx", "ar", "rm", "q")


class S06Predict(SpokenScene):
    def construct(self):
        p = pred1_parts()
        self.play(FadeIn(p["title"]), FadeIn(p["sec"]), FadeIn(p["pl"]), FadeIn(p["pr"]), FadeIn(p["pls"]),
                  FadeIn(p["lm"]), FadeIn(p["lml"]), FadeIn(p["cl"]), FadeIn(p["el"]), run_time=0.9)
        self.at("in chick")
        self.play(FadeIn(p["ctag"]), run_time=0.5)
        self.at("hoxc9")
        self.play(FadeIn(p["hx"], scale=0.7), GrowArrow(p["ar"]), run_time=0.6)
        self.at("progenitors")
        self.play(ReplacementTransform(p["pr"], p["pr_col"]), run_time=0.8)
        self.at("motor neurons")
        self.play(FadeIn(p["rm"], scale=0.7), run_time=0.7)
        self.at("what column")
        self.play(ReplacementTransform(p["ctag"], p["quest"]), FadeIn(p["q"], scale=0.6), run_time=0.6)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        p = pred1_parts()
        for k in PRED_FINAL:
            self.add(p[k])
        self.wait(self.narration_s)


# ---------------------------------------------------------------------------------------------
# s08 reveal
# ---------------------------------------------------------------------------------------------
class S08Reveal(SpokenScene):
    def construct(self):
        p = pred1_parts()
        for k in PRED_FINAL:
            self.add(p[k])
        lmc2 = T("LMC", 30, GREEN, weight=BOLD).move_to([RLAB[0], RLAB[1], 0])
        green_dots = [cell_dot(p_, GREEN, ring=ORANGE) for p_ in cluster_pts(RIGHT_MN, 6)]
        self.play(ReplacementTransform(p["q"], lmc2),
                  *[ReplacementTransform(old, nd) for old, nd in zip(p["rm"][1:], green_dots)], run_time=0.4)
        self.at("lateral column")
        st = Line(lmc2.get_left() + LEFT * 0.1, lmc2.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        self.play(Create(st), run_time=0.4)
        self.at("suppressed")
        grey_dots = [cell_dot(p_, NEUT, ring=ORANGE) for p_ in cluster_pts(RIGHT_MN, 6)]
        self.play(FadeOut(lmc2), FadeOut(st), *[ReplacementTransform(a, b) for a, b in zip(green_dots, grey_dots)], run_time=0.9)
        self.at("take on")
        pgl = T("PGC", 30, MAGENTA, weight=BOLD).move_to([RLAB[0], RLAB[1], 0])
        newdots = [cell_dot(p_, MAGENTA, ring=ORANGE) for p_ in cluster_pts(RIGHT_MN, 6)]
        self.play(FadeIn(pgl), *[ReplacementTransform(old, nd) for old, nd in zip(grey_dots, newdots)], run_time=0.6)
        self.at("preganglionic")
        ann = VGroup(T("column", 26, MAGENTA), T("of Terni", 26, MAGENTA), T("(in chick)", 26, MAGENTA)).arrange(DOWN, buff=0.1).move_to([5.6, -0.9, 0])
        self.play(FadeIn(ann), run_time=0.5)
        self.at("thoracic column")
        thx = VGroup(T("a thoracic", 26, THOR), T("column", 26, THOR)).arrange(DOWN, buff=0.1).move_to([5.6, -2.5, 0])
        self.play(FadeIn(thx), Indicate(p["hx"], color=THOR), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s08b timing
# ---------------------------------------------------------------------------------------------
def panel(x0, kind):
    """kind 'a': Hoxc9 from the progenitor on. kind 'b': Hoxc9 only after the last division."""
    d = {}
    px, nx, cy = x0 - 1.55, x0 + 1.55, -0.15
    d["pr"] = neuron([px, cy], 1.12, NEUT)
    d["prl"] = T("progenitor", 30, GREY).move_to([px, -1.9, 0])
    d["ar"] = arr([x0 - 0.36, cy, 0], [x0 + 0.36, cy, 0], GREY, 4)
    d["mn"] = neuron([nx, cy], 1.12, NEUT)
    d["mnh"] = chip("Hoxc9", THOR, 32).move_to([nx, 1.95, 0])
    if kind == "a":
        d["title"] = T("Hoxc9 in\nprogenitors", 34, TEXT, line_spacing=0.7).move_to([x0, 3.15, 0])
        d["hx"] = chip("Hoxc9", THOR, 32).move_to([px, 1.95, 0])
        d["res"] = T("PGC", 38, MAGENTA, weight=BOLD).move_to([nx, -1.9, 0])
    else:
        d["title"] = T("Hoxc9 only after\nthe last division", 34, TEXT, line_spacing=0.7).move_to([x0, 3.15, 0])
        d["ld"] = T("last division", 26, GREY).move_to([x0, 1.32, 0])
        d["tick"] = DashedLine([x0, 0.6, 0], [x0, -0.8, 0], color=TEXT, stroke_width=4, dash_length=0.12)
        d["lmc"] = T("LMC", 38, GREEN, weight=BOLD).move_to([nx - 0.2, -1.9, 0])
        d["sup"] = T("LMC suppressed", 30, RED, weight=BOLD).move_to([nx - 0.2, -1.9, 0])
        d["nopg"] = T("no PGC", 34, RED, weight=BOLD).move_to([nx - 0.2, -2.5, 0])
    return d


NOTE_T = "PGC identity needs Hoxc9 in progenitors too"


def tint(n, color):
    """Return a copy of a neuron with the outline and processes in a new colour."""
    c = n.copy()
    c[1].set_stroke(color).set_fill(color, 0.18)
    c[2].set_stroke(color)
    return c


class S08bTiming(SpokenScene):
    def construct(self):
        a = panel(-3.45, "a")
        b = panel(3.45, "b")
        div = Line([0, 3.7, 0], [0, -2.75, 0], color=GREY, stroke_width=2, stroke_opacity=0.5)
        self.play(FadeIn(a["title"]), FadeIn(a["pr"]), FadeIn(a["prl"]), FadeIn(a["hx"], shift=DOWN * 0.3), FadeIn(div), run_time=0.7)
        mn_a = tint(a["mn"], MAGENTA)
        self.play(GrowArrow(a["ar"]), FadeIn(a["mn"]), FadeIn(a["mnh"], shift=DOWN * 0.3), run_time=0.5)
        self.play(ReplacementTransform(a["mn"], mn_a), FadeIn(a["res"]), run_time=0.5)
        self.at("given only")
        self.play(FadeIn(b["title"]), FadeIn(b["pr"]), FadeIn(b["prl"]), run_time=0.6)
        self.at("last division")
        mn_b = tint(b["mn"], GREEN)
        self.play(Create(b["tick"]), FadeIn(b["ld"]), GrowArrow(b["ar"]), FadeIn(mn_b), FadeIn(b["lmc"]), run_time=0.7)
        self.at("suppresses")
        mn_b2 = tint(b["mn"], GREY)
        self.play(FadeIn(b["mnh"], shift=DOWN * 0.3), run_time=0.5)
        self.play(ReplacementTransform(mn_b, mn_b2), ReplacementTransform(b["lmc"], b["sup"]), run_time=0.8)
        self.at("preganglionic cells")
        self.play(FadeIn(b["nopg"]), run_time=0.5)
        note = T(NOTE_T, 38, TEXT).move_to([0, -3.08, 0])
        cr = T("Dasen, Liu and Jessell, 2003", 26, GREY).move_to([0, -3.55, 0])
        self.play(FadeIn(note), FadeIn(cr), run_time=0.6)
        self.finish()


def timing_final():
    a = panel(-3.45, "a")
    b = panel(3.45, "b")
    div = Line([0, 3.7, 0], [0, -2.75, 0], color=GREY, stroke_width=2, stroke_opacity=0.5)
    note = T(NOTE_T, 38, TEXT).move_to([0, -3.08, 0])
    cr = T("Dasen, Liu and Jessell, 2003", 26, GREY).move_to([0, -3.55, 0])
    items = [a["title"], a["pr"], a["prl"], a["hx"], a["ar"], tint(a["mn"], MAGENTA), a["mnh"], a["res"], div,
             b["title"], b["pr"], b["prl"], b["tick"], b["ld"], b["ar"], tint(b["mn"], GREY), b["mnh"], b["sup"], b["nopg"], note, cr]
    return items


class S09Beat(NarratedScene):
    def construct(self):
        self.add(*timing_final())
        self.wait(self.narration_s)


# ---------------------------------------------------------------------------------------------
# s10 FoxP1 gates
# ---------------------------------------------------------------------------------------------
LANE_Y = [2.45, 0.8, -0.85, -2.5]
GATE_X = -0.9
BUS_X = -3.6
COL_X = 2.7


def bar(y0, y1, color=TEXT):
    return Rectangle(width=0.45, height=y1 - y0, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([GATE_X, (y0 + y1) / 2, 0])


# Each pair of coloured bars straddles its arrow at the centre of the gap.
WALL_LMC = VGroup(bar(2.45 + 0.48, 2.45 + 0.80, GREEN),
                  bar(2.45 - 0.80, 2.45 - 0.48, GREEN))
WALL_PGC = VGroup(bar(0.8 + 0.18, 0.8 + 0.80, MAGENTA),
                  bar(0.8 - 0.80, 0.8 - 0.18, MAGENTA))


class S10Fox(SpokenScene):
    def construct(self):
        names = [("LMC", GREEN), ("PGC", MAGENTA), ("MMC", AZURE), ("HMC", AQUA)]
        cols = VGroup()
        for (nm, col), y in zip(names, LANE_Y):
            cl = cluster([COL_X, y], col, n=5).scale(0.75, about_point=np.array([COL_X, y, 0]))
            lab = T(nm, 34, col, weight=BOLD).move_to([5.6, y, 0])
            cols.add(VGroup(cl, lab))
        hox = chip("Hox", GOLD, 40).move_to([-5.5, 0.8, 0])
        self.play(FadeIn(cols), FadeIn(hox, scale=0.7), run_time=0.9)
        lanes = VGroup(*[arr([BUS_X, y, 0], [COL_X - 0.9, y, 0], GREY, 3, 0.18) for y in LANE_Y])
        bus = Line([BUS_X, LANE_Y[0], 0], [BUS_X, LANE_Y[3], 0], color=GREY, stroke_width=3)
        feed = Line([hox.get_right()[0] + 0.1, 0.8, 0], [BUS_X, 0.8, 0], color=GOLD, stroke_width=3)
        self.play(Create(feed), Create(bus), FadeIn(lanes), run_time=0.7)
        self.at("accessory factor")
        cap = T("accessory factor", 26, GREY).move_to([-5.2, -1.6, 0])
        self.play(FadeIn(cap), run_time=0.4)
        self.at("fox p1")
        fox = chip("FoxP1", TEXT, 40).move_to([-5.5, -0.55, 0])
        feed2 = Line([fox.get_right()[0] + 0.1, -0.55, 0], [BUS_X, -0.55, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(fox, shift=LEFT * 0.4), Create(feed2), run_time=0.6)
        self.at("limb", lead=0.3)
        w1 = WALL_LMC
        gl1 = T("FoxP1 high", 28, TEXT).move_to([0.95, LANE_Y[0] + 0.5, 0])
        cr = T("Dasen et al., 2008; Rousso et al., 2008", 26, GREY).move_to([0, -3.55, 0])
        self.play(FadeIn(w1, scale=0.6), FadeIn(gl1), FadeIn(cr), run_time=0.5)
        self.at("autonomic", lead=0.3)
        w2 = WALL_PGC
        gl2 = T("FoxP1 low", 28, TEXT).move_to([0.95, LANE_Y[1] + 0.5, 0])
        self.play(FadeIn(w2, scale=0.6), FadeIn(gl2), run_time=0.5)
        self.at("columns")
        n3 = T("no gate", 26, GREY).move_to([0.95, LANE_Y[2] + 0.5, 0])
        n4 = T("no gate", 26, GREY).move_to([0.95, LANE_Y[3] + 0.5, 0])
        self.play(FadeIn(n3), FadeIn(n4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s11 / s12 predict FoxP1
# ---------------------------------------------------------------------------------------------
def foxq_parts():
    sec = half_section()
    tg = sec_tag("mouse, limb level")
    title = T("Predict.", 40, GOLD, weight=BOLD).move_to([5.3, 3.4, 0])
    fox = chip("Foxp1", TEXT, 50).move_to([2.7, 2.0, 0])
    x = cross([5.5, 2.0, 0], 1.0, 1.0, RED, 8)
    de = T("deleted", 30, RED, weight=BOLD).move_to([4.1, 1.15, 0])
    d1 = DashedVMobject(Circle(radius=0.95).move_to([MMC_C[0], MMC_C[1], 0]), num_dashes=22).set_stroke(GREY, 4, opacity=0.9)
    d2 = DashedVMobject(Circle(radius=0.95).move_to([LMC_C[0], LMC_C[1], 0]), num_dashes=22).set_stroke(GREY, 4, opacity=0.9)
    q1 = T("?", 54, TEXT).move_to([MMC_C[0], MMC_C[1], 0])
    q2 = T("?", 54, TEXT).move_to([LMC_C[0], LMC_C[1], 0])
    made = T("Are limb-level\nmotor neurons\nstill made?", 38, TEXT, weight=BOLD, line_spacing=0.8).move_to([3.5, -0.9, 0])
    return dict(sec=sec, tg=tg, title=title, fox=fox, x=x, de=de, d1=d1, d2=d2, q1=q1, q2=q2, made=made)


class S11Predict(SpokenScene):
    def construct(self):
        p = foxq_parts()
        self.play(FadeIn(p["sec"]), FadeIn(p["tg"]), FadeIn(p["title"]), run_time=0.8)
        self.at("delete")
        self.play(FadeIn(p["fox"], scale=0.7), run_time=0.4)
        self.play(Create(p["x"]), FadeIn(p["de"]), run_time=0.5)
        self.at("limb level")
        self.play(FadeIn(p["d1"]), FadeIn(p["d2"]), FadeIn(p["q1"]), FadeIn(p["q2"]), run_time=0.7)
        self.at("still made")
        self.play(FadeIn(p["made"], scale=0.9), run_time=0.5)
        self.finish()


class S12Pause(NarratedScene):
    def construct(self):
        p = foxq_parts()
        self.add(*p.values())
        self.wait(self.narration_s)


# ---------------------------------------------------------------------------------------------
# s13 / s14
# ---------------------------------------------------------------------------------------------
FILL = [(-5.3, 1.6), (-4.6, 1.15), (-3.9, 1.85), (-5.3, 0.55), (-3.9, 0.85), (-4.6, 0.05), (-3.1, 0.5),
        (-2.3, -0.3), (-3.4, -0.5), (-4.5, -0.75), (-2.5, -1.3), (-3.5, -1.5), (-5.3, -0.5), (-2.9, 1.35)]
FOX_SMALL_POS = (5.0, 3.4)


def fox_small():
    return chip("Foxp1 deleted", RED, 26).move_to([FOX_SMALL_POS[0], FOX_SMALL_POS[1], 0])


class S13Reveal(SpokenScene):
    def construct(self):
        p = foxq_parts()
        for k in ("sec", "tg", "title", "fox", "x", "de", "d1", "d2", "q1", "q2", "made"):
            self.add(p[k])
        small = fox_small()
        self.play(FadeOut(p["x"]), FadeOut(p["de"]), FadeOut(p["made"]), ReplacementTransform(p["fox"], small), FadeOut(p["title"]),
                  run_time=0.5)
        self.at("motor neurons")
        dots = VGroup(*[cell_dot(q, NEUT, r=0.22) for q in FILL])
        self.play(FadeOut(p["d1"]), FadeOut(p["d2"]), FadeOut(p["q1"]), FadeOut(p["q2"]), FadeIn(dots, lag_ratio=0.1),
                  run_time=0.55)
        self.at("still made")
        made = T("made", 84, NEUT, weight=BOLD).move_to([3.6, 1.5, 0])
        self.play(FadeIn(made, scale=0.8), run_time=0.5)
        self.at("what fails")
        na = T("but not\nassigned", 60, RED, weight=BOLD, line_spacing=0.8).move_to([3.6, -0.6, 0])
        self.play(FadeIn(na, shift=UP * 0.2), run_time=0.6)
        self.at("which one each")
        self.play(*[Indicate(d, color=TEXT, scale_factor=1.5) for d in dots[::2]], run_time=0.9)
        self.finish()


def s13_final():
    p = foxq_parts()
    dots = VGroup(*[cell_dot(q, NEUT, r=0.22) for q in FILL])
    made = T("made", 84, NEUT, weight=BOLD).move_to([3.6, 1.5, 0])
    na = T("but not\nassigned", 60, RED, weight=BOLD, line_spacing=0.8).move_to([3.6, -0.6, 0])
    return dict(sec=p["sec"], tg=p["tg"], fox=fox_small(), dots=dots, made=made, na=na)


MUS_POS = [(5.2, 1.9), (5.2, 0.65), (5.2, -0.6), (5.2, -1.85)]


def scrambled(color=AQUA):
    """Four complete, crossing axons, each ending inside a different muscle box."""
    order = [2, 0, 3, 1]
    starts = [FILL[i] for i in (2, 6, 8, 10)]
    ax = VGroup()
    for i, (start, target) in enumerate(zip(starts, order)):
        end = MUS_POS[target]
        ax.add(route([start[0] + 0.2, start[1]],
                     [end[0] - 0.73, end[1]], [1.3, 0.45 - 0.3 * i], color, 4))
    return ax


def limb_with_muscles():
    lb = limb(labels=False)
    ms = VGroup(*[muscle(p, "muscle", 1.55, GREY, 24) for p in MUS_POS])
    return lb, ms


HMC_LABEL = "thoracic hypaxial column (HMC)"


class S14Reveal2(SpokenScene):
    def construct(self):
        p = s13_final()
        self.add(*p.values())
        self.wait(0.15)
        self.at("resemble")
        self.play(FadeOut(p["made"]), FadeOut(p["na"]),
                  *[d.animate.set_color(AQUA) for d in p["dots"]], run_time=0.8)
        self.at("thoracic hypaxial")
        hl = T(HMC_LABEL, 26, AQUA, weight=BOLD).move_to([-0.3, 3.35, 0])
        self.play(FadeOut(p["tg"]), FadeIn(hl), run_time=0.5)
        self.at("in the limb")
        lb, ms = limb_with_muscles()
        self.play(FadeIn(lb), FadeIn(ms), run_time=0.7)
        self.at("their axons")
        ax = scrambled(AQUA)
        self.play(LaggedStart(*[Create(a) for a in ax], lag_ratio=0.15), run_time=2.2)
        self.at("at random")
        self.play(Indicate(ax, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.finish()


class S15Beat(NarratedScene):
    def construct(self):
        p = s13_final()
        for k in ("sec", "fox"):
            self.add(p[k])
        for d in p["dots"]:
            self.add(d.set_color(AQUA))
        hl = T(HMC_LABEL, 26, AQUA, weight=BOLD).move_to([-0.3, 3.35, 0])
        lb, ms = limb_with_muscles()
        self.add(hl, lb, ms, scrambled(AQUA))
        self.wait(self.narration_s)


# ---------------------------------------------------------------------------------------------
# s16 / s17 / s18 the limb choice
# ---------------------------------------------------------------------------------------------
class S16Lim(SpokenScene):
    def construct(self):
        z = lmc_zoom()
        lb = limb()
        self.play(FadeIn(z["big"]), FadeIn(z["lat"]), FadeIn(z["med"]), FadeIn(z["lmc"]), FadeIn(z["ll"]), FadeIn(z["ml"]),
                  FadeIn(lb), run_time=0.9)
        self.at("one more choice")
        self.play(Create(z["div"]), run_time=0.9)
        self.at("lateral cells")
        self.play(Indicate(z["lat"], color=TEXT, scale_factor=1.3), run_time=0.6)
        self.at("make limb one")
        lim = chip("Lim1", TEXT, 28).move_to([LIM_POS[0], LIM_POS[1], 0])
        self.play(FadeIn(lim, shift=DOWN * 0.2), run_time=0.5)
        self.at("their axons go dorsal", lead=0.0)
        ax = lat_axons(TEXT)
        self.play(Create(ax, lag_ratio=0.2), run_time=0.9)
        self.play(FadeIn(tips(ax, TEXT)), run_time=0.3)
        self.finish()


RND_ENDS = [(5.8, 1.7), (5.9, 0.35), (3.5, -1.8)]


class S17Isl(SpokenScene):
    def construct(self):
        z = lmc_zoom()
        lb = limb()
        lim = chip("Lim1", TEXT, 28).move_to([LIM_POS[0], LIM_POS[1], 0])
        la = lat_axons(TEXT)
        lt = tips(la, TEXT)
        self.add(z["big"], z["div"], z["lat"], z["med"], z["ll"], z["ml"], z["lmc"], lb, lim, la, lt)
        self.wait(0.1)
        self.at("medial cells")
        self.play(Indicate(z["med"], color=YELLOW, scale_factor=1.3), run_time=0.6)
        self.at("keep islet")
        isl = chip("Isl1", YELLOW, 32).move_to([ISL_POS[0], ISL_POS[1], 0])
        self.play(FadeIn(isl, shift=DOWN * 0.2), run_time=0.5)
        self.at("their axons go")
        ma = med_axons(YELLOW)
        self.play(Create(ma, lag_ratio=0.2), run_time=1.3)
        self.play(FadeIn(tips(ma, YELLOW)), run_time=0.3)
        self.at("without limb")
        x = cross(lim.get_center(), 1.3, 0.9, RED, 7)
        cr = T("Kania, Johnson and Jessell, 2000", 26, GREY).move_to([-3.6, -3.55, 0])
        self.play(Create(x), FadeIn(cr), run_time=0.6)
        self.at("lateral axons", lead=0.0)
        rnd = lat_axons(TEXT, RND_ENDS)
        self.play(ReplacementTransform(la, rnd), ReplacementTransform(lt, tips(rnd, TEXT)), run_time=1.5)
        self.at("dorsal preference")
        lost = T("no dorsal preference", 32, RED, weight=BOLD).move_to([3.5, -3.45, 0])
        self.play(FadeIn(lost), run_time=0.5)
        self.finish()


S18_LAT_END = [(4.9, 1.0), (4.85, 1.85), (4.4, 0.55)]


class S18Next(SpokenScene):
    def construct(self):
        z = lmc_zoom()
        lb = limb()
        self.add(z["big"], z["div"], z["lat"], z["med"], z["lmc"], lb)
        # ephrins: a mild dorsal-to-ventral gradient (denser and brighter toward ventral)
        eps = VGroup()
        for row, y in enumerate(np.linspace(2.0, -2.0, 7)):
            for xk in (2.3, 3.2, 4.1, 5.0, 5.9):
                eps.add(Dot([xk, float(y), 0], radius=0.06 + 0.012 * row, color=LIME).set_opacity(0.2 + 0.12 * row))
        # both bundles run to the entry of the limb and stop at the split point
        lstem = VGroup(*[route([LAT_DOTS[i][0] + 0.2, LAT_DOTS[i][1]], [0.7, VIA_D[i][1]], None, TEXT) for i in range(3)])
        mstem = VGroup(*[route([MED_START[i][0] + 0.2, MED_START[i][1]], [0.7, VIA_V[i][1]], None, YELLOW) for i in range(3)])
        gcs = VGroup(*[Dot([0.7, VIA_D[i][1], 0], radius=0.1, color=TEXT) for i in range(3)],
                     *[Dot([0.7, VIA_V[i][1], 0], radius=0.1, color=YELLOW) for i in range(3)])
        self.add(lstem, mstem, gcs)
        self.wait(0.1)
        self.at("receptors")
        eph = chip("Eph receptors", LIME, 26).move_to([-0.6, 2.05, 0])
        eph_l = Line([-0.2, 1.72, 0], [0.7, 1.3, 0], color=LIME, stroke_width=3)
        eph2 = chip("Eph receptors", LIME, 26).move_to([-0.6, -2.05, 0])
        eph2_l = Line([-0.2, -1.72, 0], [0.7, -1.3, 0], color=LIME, stroke_width=3)
        self.play(FadeIn(eph), Create(eph_l), FadeIn(eph2), Create(eph2_l), run_time=0.7)
        self.at("and")
        epl = chip("ephrins in the limb", LIME, 26).move_to([3.5, -3.4, 0])
        self.play(FadeIn(eps, lag_ratio=0.02), FadeIn(epl), run_time=0.9)
        self.at("carry out")
        la = lat_axons(TEXT, S18_LAT_END)
        ma = med_axons(YELLOW)
        mu = muscle([5.55, 1.85, 0], "muscle", 1.5, GREY, 24)
        self.play(FadeOut(lstem), FadeOut(mstem), FadeOut(gcs), Create(la, lag_ratio=0.2), Create(ma, lag_ratio=0.2), FadeIn(mu), run_time=1.0)
        self.at("alongside other")
        og = chip("other guidance systems", GREY, 26).move_to([-4.1, -3.25, 0])
        self.play(FadeIn(og), run_time=0.6)
        ptr = T("See the neurotrophic\nhypothesis lesson", 26, LIME, line_spacing=0.7).move_to([1.2, 3.25, 0])
        self.play(FadeIn(ptr), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s19-s21 the dish
# ---------------------------------------------------------------------------------------------
def dish_label(text, x, color=GREY, size=28, y=-2.65):
    return T(text, size, color, line_spacing=0.7).move_to([x, y, 0])


TL_Y = -3.45


def timeline():
    l1 = Arrow([-6.4, TL_Y, 0], [-1.0, TL_Y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.0)
    l2 = Arrow([1.0, TL_Y, 0], [6.4, TL_Y, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
    tlab = T("recipe", 30, GREY).move_to([0, TL_Y, 0])
    return VGroup(l1, l2), tlab


def arrow12(faint=False):
    a = arr([DISH_X[0] + 2.0, DISH_Y, 0], [DISH_X[1] - 2.0, DISH_Y, 0], GREY)
    return a.set_opacity(0.3) if faint else a


def arrow23(faint=False):
    a = arr([DISH_X[1] + 2.0, DISH_Y, 0], [DISH_X[2] - 2.0, DISH_Y, 0], GREY)
    return a.set_opacity(0.3) if faint else a


RA_POS = [(DISH_X[0] + DISH_X[1]) / 2, 2.8, 0]
HH_POS = [(DISH_X[1] + DISH_X[2]) / 2, 2.8, 0]


class S19Dish(SpokenScene):
    def construct(self):
        tl, tlab = timeline()
        d1 = dish(DISH_X[0])
        l1 = dish_label("mouse embryonic\nstem cells", DISH_X[0])
        d2p = dish(DISH_X[1], cells=False, faint=True)
        d3p = dish(DISH_X[2], cells=False, faint=True)
        a12 = arrow12(True)
        a23 = arrow23(True)
        self.play(Create(tl), FadeIn(tlab), FadeIn(d1), FadeIn(l1), FadeIn(d2p), FadeIn(d3p), FadeIn(a12), FadeIn(a23), run_time=1.3)
        self.at("a recipe")
        self.play(Indicate(tl, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.at("retinoic acid")
        ra = chip("retinoic acid", GOLD, 30).move_to(RA_POS)
        self.play(FadeIn(ra, shift=DOWN * 0.3), a12.animate.set_opacity(1.0), run_time=0.6)
        self.at("mouse stem cells")
        self.play(Indicate(d1[1], color=TEXT, scale_factor=1.05), run_time=0.6)
        self.at("spinal character")
        d2 = dish(DISH_X[1])
        l2 = dish_label("spinal character", DISH_X[1], GOLD)
        self.play(ReplacementTransform(d2p, d2), run_time=0.4)
        self.play(*[c.animate.set_stroke(GOLD, 3).set_fill(GOLD, 0.4) for c in d2[1]], FadeIn(l2), run_time=0.6)
        self.finish()


def dishes_12(with_d3=True):
    tl, tlab = timeline()
    d1 = dish(DISH_X[0])
    l1 = dish_label("mouse embryonic\nstem cells", DISH_X[0])
    ra = chip("retinoic acid", GOLD, 30).move_to(RA_POS)
    d2 = dish(DISH_X[1])
    for c in d2[1]:
        c.set_stroke(GOLD, 3).set_fill(GOLD, 0.4)
    a12 = arrow12()
    l2 = dish_label("spinal character", DISH_X[1], GOLD)
    out = [tl, tlab, d1, l1, ra, d2, a12, l2]
    if with_d3:
        out += [dish(DISH_X[2], cells=False, faint=True), arrow23(True)]
    return out


class S20Dish2(SpokenScene):
    def construct(self):
        self.add(*dishes_12(with_d3=False))
        d3p = dish(DISH_X[2], cells=False, faint=True)
        a23 = arrow23(True)
        self.add(d3p, a23)
        self.wait(0.1)
        self.at("hedgehog agonist")
        hh = chip("Hedgehog agonist", LIME, 30).move_to(HH_POS)
        d3 = dish(DISH_X[2])
        self.play(FadeIn(hh, shift=DOWN * 0.3), ReplacementTransform(d3p, d3), a23.animate.set_opacity(1.0), run_time=0.8)
        self.at("motor neuron domain")
        l3 = dish_label("motor neuron\ndomain", DISH_X[2], LIME)
        self.play(*[c.animate.set_stroke(LIME, 3).set_fill(LIME, 0.4) for c in d3[1]], FadeIn(l3), run_time=0.8)
        self.at("motor neurons appear")
        ns = VGroup(*[neuron([DISH_X[2] + dx, DISH_Y + dy], 0.3, NEUT) for dx, dy in DISH_PTS])
        l3b = dish_label("Mnx1-positive\nmotor neurons", DISH_X[2], LIME)
        self.play(ReplacementTransform(d3[1], ns), ReplacementTransform(l3, l3b), run_time=0.9)
        cr = T("Wichterle et al., 2002", 30, TEXT).move_to([3.9, 3.5, 0])
        self.play(FadeIn(cr), run_time=0.4)
        self.finish()


EMB_C = (3.9, 0.1)
EMB_MUS = [(5.1, 1.55), (5.1, 0.2), (5.1, -1.15)]
D21_C = (-3.7, 0.35)


class S21Dish3(SpokenScene):
    def construct(self):
        d = dish(D21_C[0], y=D21_C[1], cells=False)
        d[0].stretch_to_fit_width(5.0).move_to([D21_C[0], D21_C[1], 0])
        pts = [(-1.5, 1.0), (-0.6, 1.3), (0.4, 0.9), (1.4, 1.2), (-1.1, -0.1), (0.0, 0.1), (1.0, -0.2), (-0.7, -1.1), (0.4, -1.2), (1.5, -1.0)]
        cells = VGroup(*[neuron([D21_C[0] + dx, D21_C[1] + dy], 0.28, NEUT) for dx, dy in pts])
        lab = T("motor neurons from the dish", 28, NEUT).move_to([D21_C[0], -2.65, 0])
        emb = RoundedRectangle(width=5.2, height=6.0, corner_radius=0.9, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.07).move_to([EMB_C[0], EMB_C[1], 0])
        el = T("embryo", 28, GREY).move_to([EMB_C[0], 2.5, 0])
        ms = [muscle(q, "muscle", 1.6, GREY, 24) for q in EMB_MUS]
        self.add(d, cells, lab, emb, el, *ms)
        self.at("into an embryo")
        mover = neuron([-0.9, 0.35], 0.34, NEUT)
        self.play(TransformFromCopy(cells[3], mover), run_time=0.3)
        self.play(mover.animate.move_to([2.0, 0.2, 0]), run_time=0.6)
        self.at("reach muscle")
        ax = route([2.3, 0.2], [EMB_MUS[0][0] - 0.8, EMB_MUS[0][1]], None, NEUT, 5)
        self.play(Create(ax), run_time=0.9)
        self.at("mostly medial")
        newcells = VGroup(*[neuron([c[1].get_center()[0], c[1].get_center()[1]], 0.28, AZURE if i < 8 else GREY) for i, c in enumerate(cells)])
        for nc in newcells[8:]:
            nc[1].set_fill(opacity=0)
        ml = T("mostly MMC", 38, AZURE, weight=BOLD).move_to([D21_C[0], -2.65, 0])
        self.play(ReplacementTransform(cells, newcells), ReplacementTransform(lab, ml), run_time=0.9)
        self.at("one named pool")
        q = chip("one named pool?", TEXT, 30).move_to([3.4, -2.3, 0])
        hl = SurroundingRectangle(ms[2], color=TEXT, buff=0.1, stroke_width=5)
        leader = Line([4.9, -1.95, 0], [5.1, -1.55, 0], color=TEXT, stroke_width=4)
        self.play(*[m.animate.set_opacity(0.3) for m in ms[:2]], Create(hl), FadeIn(q), Create(leader), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# s22 takeaway
# ---------------------------------------------------------------------------------------------
BAND_Y = [3.0, 1.5, 0.0, -1.5]
BAND_H = 1.25
BANDS = [("progenitor", -6.5, -1.5, GOLD, "Hox", GOLD),
         ("class", -4.6, 0.6, NEUT, "Isl1 + Lhx3", YELLOW),
         ("column", -2.7, 2.7, AZURE, "Hox + FoxP1", TEXT),
         ("limb choice", -0.8, 6.0, YELLOW, "Lim1 / Isl1", TEXT)]


def band(i, op=0.22):
    name, x0, x1, col, tf, tfc = BANDS[i]
    r = RoundedRectangle(width=x1 - x0, height=BAND_H, corner_radius=0.3, stroke_color=col, stroke_width=3,
                         fill_color=col, fill_opacity=op).move_to([(x0 + x1) / 2, BAND_Y[i], 0])
    lab = T(name, 28, col, weight=BOLD)
    lab.move_to([x0 + 0.25 + lab.width / 2, BAND_Y[i], 0])
    ch = chip(tf, tfc, 26).move_to([x1 - 0.3 - chip(tf, tfc, 26).width / 2, BAND_Y[i], 0])
    return VGroup(r, lab, ch)


DISH_ICON = (4.8, -3.05)


class S22Take(SpokenScene):
    def construct(self):
        bs = [band(i) for i in range(4)]
        self.at("overlapping layers")
        self.play(FadeIn(bs[0], shift=RIGHT * 0.3), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in bs[1:]], lag_ratio=0.35), run_time=1.2)
        self.at("class")
        self.play(Indicate(bs[1], color=TEXT, scale_factor=1.03), run_time=0.6)
        self.at("its column")
        self.play(Indicate(bs[2], color=TEXT, scale_factor=1.03), run_time=0.6)
        self.at("limb choice")
        self.play(Indicate(bs[3], color=TEXT, scale_factor=1.03), run_time=0.6)
        self.at("run them in order")
        ph = Line([-6.5, 3.5, 0], [-6.5, -2.15, 0], color=TEXT, stroke_width=5)
        self.play(ph.animate.shift(RIGHT * 12.0), run_time=0.7, rate_func=linear)
        self.play(FadeOut(ph), run_time=0.2)
        self.at("and you have")
        dd = VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.4, stroke_color=TEXT, stroke_width=4,
                                     fill_color=NEUT, fill_opacity=0.22),
                    *[cell_dot([-0.9 + 0.6 * k, 0.0], NEUT, r=0.19) for k in range(4)]).move_to([DISH_ICON[0], DISH_ICON[1], 0])
        a = arr([1.8, BAND_Y[3] - BAND_H / 2 - 0.05, 0],
                [DISH_ICON[0] - 1.35, DISH_ICON[1], 0], TEXT, 6, 0.28)
        rl = T("recipe", 40, TEXT, weight=BOLD).move_to([1.65, -3.35, 0])
        self.play(GrowArrow(a), FadeIn(dd), FadeIn(rl), run_time=0.6)
        self.finish()


class S23End(EndCard):
    LINE = "Overlapping layers set a motor neuron's class, column, and limb choice."
