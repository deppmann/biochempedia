"""The Lift: A Nucleus on a Timetable  (Biochemistrypedia chaptered explainer, chapter 2)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one colour per concept, whole film; shared with chapter 1 where the concept recurs)
  BLUE   = the radial glial cell (cell body, shaft, fibre); dashed BLUE outline = intermediate progenitor
  YELLOW = the nucleus (the lift car is a yellow cab around it)
  TEAL   = cell-cycle phase (ring, G1 / S / G2 / M, "copy DNA", "divide")
  ORANGE = the radioactive pulse label (thymidine); a LABELED nucleus is always a solid orange disc with an orange ring
  PURPLE = centrosome, spindle and primary cilium
  PINK   = the Notch signal
  GOLD   = evidence status tags ("partly known", "proposal"), citations
  RED    = the open question
  GREY   = ventricle, pia, labels, the old reading of the wall, de-emphasised things
  (GREEN, the neuron colour, is not used in this chapter.)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB4"

# ----------------------------------------------------------------------------- geometry
BOT = -2.7                       # nucleus at the apical surface (wall view)
COLS = [-5.5 + 1.0 * k for k in range(10)]
WCW = 0.9                        # width of a wall cell
HX = -3.5                        # x of the hero cell (column 2)
HW = 3.0                         # width of the hero shaft
LX = -1.2                        # left edge of labels beside the shaft
CAR_R = 0.5
CELL_H = 6.1                     # long cells run from the ventricle (y -3.15) to the pia (y 2.95)
CELL_Y = -0.1
B_L = -2.3                       # lift: ground floor
S_L = -0.86                      # lift: floor where the car stops for S phase (third floor)
FLOORS = [-2.3 + 0.72 * k for k in range(8)]
VZ_TOP = -0.45                   # top of the ventricular zone: three of the eight floors
K_WIDE = 1.45                    # nuclei spread over the whole wall (old anatomists' section)
K_MODEL = 0.62                   # nuclei confined to the ventricular zone (the lift model)

# every cell of the section: (u, S) = position in its cycle (see ny_of) and the height of its S-phase stop
CYC = [(0.20, 0.45), (0.45, 0.35), (0.95, 0.50), (0.80, 0.40), (0.50, 0.55),
       (0.12, 0.50), (0.42, 0.30), (0.72, 0.45), (0.25, 0.50), (0.48, 0.40)]
S_CELLS = [1, 4, 6, 9]           # cells caught in S phase in the still section


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ny_of(u, S, B=BOT, k=1.0):
    """Height of a nucleus u of the way round its cycle: G1 rises, S holds near the top, G2 falls, M at the surface."""
    S = B + (S - B) * k
    u = u % 1.0
    if u < 0.40:
        return B + (S - B) * smooth(u / 0.40)
    if u < 0.55:
        return S
    if u < 0.90:
        return S + (B - S) * smooth((u - 0.55) / 0.35)
    return B


def heights(k):
    return [ny_of(u, S, k=k) for u, S in CYC]


NY1 = heights(1.0)
NYW = heights(K_WIDE)
NYM = heights(K_MODEL)

RING_C = np.array([3.8, 0.5, 0])
RING_R = 1.55
PHASES = [("G1", 60, -120), ("S", -60, -110), ("G2", -170, -100), ("M", 90, -30)]


# ----------------------------------------------------------------------------- helpers
def left(m, x, y):
    return m.move_to([x + m.width / 2, y, 0])


def right_at(m, x, y):
    return m.move_to([x - m.width / 2, y, 0])


def tb(text, size=26, color=TEXT, pad=0.1, **kw):
    """A text label on an opaque background, so it stays readable over cell outlines."""
    t = T(text, size, color, **kw)
    back = Rectangle(width=t.width + 2 * pad, height=t.height + 2 * pad, stroke_width=0,
                     fill_color=BG, fill_opacity=0.93).move_to(t)
    g = VGroup(back, t)
    g.set_z_index(10)
    return g


def bchip(text, color=BLUE, size=26):
    c = chip(text, color, size=size)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    g = VGroup(back, *c)
    g.set_z_index(10)
    return g


def cap(big, small):
    parts = [T(big, 40, TEAL, weight=BOLD)] + ([T(small, 28, TEAL)] if small else [])
    g = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    return g.move_to([LX + g.width / 2, -0.5, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def vent(label=True):
    strip = Rectangle(width=13.2, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to([0, -3.4, 0])
    g = VGroup(strip)
    if label:
        g.add(T("ventricle", 26, GREY).move_to([5.6, -3.4, 0]))
    return g


def long_cell(x, w=WCW, op=0.6, sw=3):
    c = RoundedRectangle(corner_radius=0.35, width=w, height=CELL_H, stroke_color=BLUE, stroke_width=sw,
                         stroke_opacity=op, fill_color=BLUE, fill_opacity=0.07).move_to([x, CELL_Y, 0])
    c.set_z_index(0)
    return c


def hero_shaft(op=1.0):
    return RoundedRectangle(corner_radius=0.5, width=HW, height=CELL_H, stroke_color=BLUE, stroke_width=3.5,
                            stroke_opacity=op, fill_color=BLUE, fill_opacity=0.12).move_to([HX, CELL_Y, 0]).set_z_index(0)


def nuc_c(x, y, r=0.28, cab=False):
    n = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85)
    parts = [n]
    if cab:
        parts.insert(0, RoundedRectangle(corner_radius=0.08, width=2 * r + 0.16, height=2 * r + 0.16,
                                         stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.22))
    g = VGroup(*parts).move_to([x, y, 0])
    g.set_z_index(3)
    return g


def dumb(x, y, r=0.18, dx=0.22):
    g = VGroup(*[Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85)
                 .move_to([x + d, y, 0]) for d in (-dx, dx)])
    g.set_z_index(3)
    return g


def lab_nuc(x, y, r=0.28, ring=0.09):
    """THE labeled look: a solid orange nucleus inside an orange ring."""
    core = Circle(radius=r, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE, fill_opacity=0.95)
    rg = Circle(radius=r + ring, stroke_color=ORANGE, stroke_width=3, fill_opacity=0)
    g = VGroup(rg, core).move_to([x, y, 0])
    g.set_z_index(4)
    return g


def lab_pair(x, y, r=0.14, dx=0.21):
    g = VGroup(lab_nuc(x - dx, y, r, 0.06), lab_nuc(x + dx, y, r, 0.06))
    g.set_z_index(4)
    return g


def legend(x, y):
    sym = lab_nuc(0, 0, 0.14, 0.07)
    lab = T("labeled", 26, ORANGE)
    g = VGroup(sym, lab).arrange(RIGHT, buff=0.2).move_to([x, y, 0])
    g.set_z_index(6)
    return g


def lift_car(x, y):
    return nuc_c(x, y, CAR_R, cab=True)


def cable_for(car, x=HX):
    c = Line([x, 2.95, 0], [x, car.get_top()[1], 0], color="#B8C0CC", stroke_width=7)
    c.add_updater(lambda m: m.put_start_and_end_on([x, 2.95, 0], [x, car.get_top()[1], 0]))
    c.set_z_index(2)
    return c


def ring_arcs():
    arcs = {}
    for name, a0, span in PHASES:
        arcs[name] = Arc(radius=RING_R, start_angle=np.deg2rad(a0), angle=np.deg2rad(span), arc_center=RING_C,
                         stroke_color=TEAL, stroke_width=9).set_stroke(opacity=0.35)
    return arcs


def ring_labels():
    out = {}
    for name, a0, span in PHASES:
        mid = np.deg2rad(a0 + span / 2)
        p = RING_C + (RING_R + 0.6) * np.array([np.cos(mid), np.sin(mid), 0])
        out[name] = T(name, 30, TEAL, weight=BOLD).move_to(p)
    return out


def pt_on_ring(deg):
    return RING_C + RING_R * np.array([np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg)), 0])


def make_floors(lit=3):
    fl = []
    for k, y in enumerate(FLOORS):
        a = Line([HX + HW / 2, y, 0], [HX + HW / 2 + 0.4, y, 0])
        b = Line([HX - HW / 2 - 0.4, y, 0], [HX - HW / 2, y, 0])
        g = VGroup(a, b)
        if k < lit:
            g.set_stroke(YELLOW, width=4, opacity=1)
        else:
            g.set_stroke(GREY, width=3, opacity=0.35)
        g.set_z_index(1)
        fl.append(g)
    return fl


def pia_group():
    strip = Rectangle(width=13.2, height=0.4, stroke_width=0, fill_color=GREY, fill_opacity=0.55).move_to([0, 3.15, 0])
    lab = T("pia", 26, TEXT).move_to([-5.9, 3.15, 0])
    return VGroup(strip, lab)


HERO_BAND_H = VZ_TOP + 3.15


def hero_band(label=True):
    band = Rectangle(width=13.2, height=HERO_BAND_H, stroke_width=0, fill_color=GREY, fill_opacity=0.13) \
        .move_to([0, (VZ_TOP - 3.15) / 2, 0])
    band.set_z_index(-1)
    g = VGroup(band)
    if label:
        g.add(T("ventricular zone", 26, GREY).move_to([5.0, -2.3, 0]))
    return g


def wall_band():
    """Ventricular zone of the wall view: a shaded band behind the cells, a bracket and a label at the right."""
    band = Rectangle(width=10.7, height=HERO_BAND_H, stroke_width=0, fill_color=GREY, fill_opacity=0.14) \
        .move_to([-1.05, (VZ_TOP - 3.15) / 2, 0])
    band.set_z_index(-1)
    xb = 4.45
    br = VGroup(Line([xb, -3.15, 0], [xb, VZ_TOP, 0], color=GREY, stroke_width=3),
                Line([xb - 0.12, -3.15, 0], [xb, -3.15, 0], color=GREY, stroke_width=3),
                Line([xb - 0.12, VZ_TOP, 0], [xb, VZ_TOP, 0], color=GREY, stroke_width=3))
    lab = T("ventricular\nzone", 26, GREY, line_spacing=0.8)
    left(lab, xb + 0.2, (VZ_TOP - 3.15) / 2)
    return VGroup(band, br, lab)


def lift_base(floors=True, band=True, pia=True, y=B_L):
    d = {"vent": vent(), "shaft": hero_shaft(), "car": lift_car(HX, y)}
    d["floors"] = make_floors() if floors else []
    d["pia"] = pia_group() if pia else None
    d["band"] = hero_band() if band else None
    d["cable"] = cable_for(d["car"])
    return d


def add_base(scene, d):
    scene.add(d["vent"], d["shaft"], d["cable"], d["car"], *d["floors"])
    if d["pia"] is not None:
        scene.add(d["pia"])
    if d["band"] is not None:
        scene.add(d["band"])


def wall_cells(op=0.6):
    return [long_cell(x, op=op) for x in COLS]


def wall_nuclei(ny, cab=False, r=0.26):
    return [nuc_c(x, y, r, cab=cab) for x, y in zip(COLS, ny)]


def old_bands():
    """The 19th-century reading of the wall: three 'types' of cells, sorted by the height of the nucleus."""
    ys = [3.0, 1.1, -1.0, -3.15]
    shades = [0.05, 0.12, 0.05]
    rects = [Rectangle(width=10.3, height=ys[i] - ys[i + 1], stroke_width=0, fill_color=GREY, fill_opacity=shades[i])
             .move_to([-1.0, (ys[i] + ys[i + 1]) / 2, 0]) for i in range(3)]
    lines = VGroup(*[DashedLine([-6.15, y, 0], [4.15, y, 0], color=GREY, stroke_width=3, dash_length=0.18) for y in ys[1:3]])
    labs = VGroup(*[T(s, 46, "#A9B3BF", font=TITLE_FONT, slant=ITALIC).move_to([5.4, (ys[i] + ys[i + 1]) / 2, 0])
                    for i, s in enumerate(("type A", "type B", "type C"))])
    return VGroup(*rects), lines, labs


# two-panel experiment
PX = (-3.0, 3.6)
PW = 6.0
OFFS = [-2.2, -1.1, 0, 1.1, 2.2]
PR = 0.24
P_MIT = -2.7                    # height of a cell dividing at the ventricle (panel view)
P_TOP = 1.9


def panel(cx):
    frame = RoundedRectangle(corner_radius=0.12, width=PW, height=5.5, stroke_color=GREY, stroke_width=2,
                             stroke_opacity=0.6).move_to([cx, -0.85, 0])
    strip = Rectangle(width=PW - 0.04, height=0.4, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to([cx, -3.4, 0])
    vl = T("ventricle", 26, GREY).move_to([cx, -3.4, 0])
    cells = [RoundedRectangle(corner_radius=0.3, width=0.9, height=4.9, stroke_color=BLUE, stroke_width=2.5,
                              stroke_opacity=0.6, fill_color=BLUE, fill_opacity=0.06).move_to([cx + o, -0.73, 0]) for o in OFFS]
    return VGroup(frame, strip, vl, *cells)


def pband(cx):
    b = Rectangle(width=PW - 0.04, height=2.9, stroke_width=0, fill_color=GREY, fill_opacity=0.15).move_to([cx, -1.75, 0])
    b.set_z_index(-1)
    return b


def pbracket():
    x = PX[0] - PW / 2 - 0.2
    ln = VGroup(Line([x, -3.2, 0], [x, -0.3, 0], color=GREY, stroke_width=3),
                Line([x, -3.2, 0], [x + 0.12, -3.2, 0], color=GREY, stroke_width=3),
                Line([x, -0.3, 0], [x + 0.12, -0.3, 0], color=GREY, stroke_width=3))
    lab = T("ventricular zone", 26, GREY).rotate(PI / 2).move_to([x - 0.3, -1.75, 0])
    return VGroup(ln, lab)


def timeline():
    line = Line([-6.2, 3.5, 0], [4.8, 3.5, 0], color=GREY, stroke_width=3)
    pdot = Dot([-5.9, 3.5, 0], radius=0.16, color=ORANGE)
    plab = T("pulse", 26, ORANGE).move_to([-5.9, 3.0, 0])
    ticks = VGroup(*[Line([x, 3.35, 0], [x, 3.65, 0], color=GREY, stroke_width=3) for x in PX])
    conn = VGroup(*[DashedLine([x, 3.3, 0], [x, 3.12, 0], color=GREY, stroke_width=2, dash_length=0.06) for x in PX])
    return line, pdot, plab, ticks, conn


def header(text, cx, color=TEXT):
    return T(text, 28, color).move_to([cx, 2.95, 0])


def qmark(cx, y):
    return T("?", 80, RED, weight=BOLD).move_to([cx, y, 0])


def qtexts():
    return (T("where are the labeled nuclei?", 26, RED).move_to([PX[0], 2.4, 0]),
            T("when do labeled mitoses appear?", 26, RED).move_to([PX[1], 2.4, 0]))


def dim(cx, op=0.62):
    r = Rectangle(width=PW + 0.2, height=5.7, stroke_width=0, fill_color=BG, fill_opacity=op).move_to([cx, -0.85, 0])
    r.set_z_index(8)
    return r


def rcell(x, y, r=0.44):
    c = Circle(radius=r, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2).move_to([x, y, 0])
    c.set_z_index(2)
    return c


def mit_plain(x, y=P_MIT):
    g = VGroup(rcell(x, y), dumb(x, y, r=0.15, dx=0.2))
    return g


def mit_lab(x, y=P_MIT):
    g = VGroup(rcell(x, y), lab_pair(x, y, r=0.15, dx=0.22))
    return g


# panel 1 (soon after the pulse): unlabeled nuclei, two labeled nuclei high in the zone, one cell at the surface
P1_UNL = [(-2.2, -1.9), (2.2, -1.6)]
P1_LAB = [(-1.1, -0.85), (1.1, -0.75)]
# panel 2 (later): unlabeled nuclei, two labeled cells dividing at the ventricle
P2_UNL = [(-2.2, -1.7), (0, -1.2), (2.2, -0.65)]
P2_LAB = [(-1.1, P_MIT), (1.1, P_MIT)]


def p1_items(cx=PX[0]):
    unl = [nuc_c(cx + o, y, PR) for o, y in P1_UNL]
    lab = [lab_nuc(cx + o, y, PR) for o, y in P1_LAB]
    mit = mit_plain(cx)
    return unl, lab, mit


def p2_items(cx=PX[1]):
    unl = [nuc_c(cx + o, y, PR) for o, y in P2_UNL]
    mit = [mit_lab(cx + o) for o, _ in P2_LAB]
    return unl, mit


# ----------------------------------------------------------------------------- scenes
class S00Title(TitleCard):
    LESSON = "The Ventricular Zone: Radial Glia as Stem Cells"
    TITLE = "The Lift: A Nucleus on a Timetable"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 22, TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), 24, GREY)
        title = T(self.TITLE, 48, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.34).move_to(ORIGIN)
        self.add(brand, lesson, title)
        self.play(GrowFromCenter(rule), run_time=0.7)
        self.wait(1.6)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()


class S01Q(SpokenScene):
    def construct(self):
        v = vent()
        nucs = VGroup(*wall_nuclei(NY1))
        self.add(v)
        q = Text("Why would a cell copy its DNA\nin one place, and divide in another?", font=TITLE_FONT,
                 font_size=38, color=TEXT, t2c={"copy its DNA": TEAL, "divide": TEAL}, line_spacing=0.9).move_to([0, 2.4, 0])
        fit(q, max_w=12.4)
        self.play(FadeIn(nucs), FadeIn(q, shift=UP * 0.15), run_time=0.6)
        x = COLS[4]
        ring = Circle(radius=0.45, color=TEAL, stroke_width=4).move_to([x, NY1[4], 0])
        lab1 = tb("copy DNA", 28, TEAL).move_to([x, 1.2, 0])
        self.at("copy its DNA")
        self.play(Create(ring), FadeIn(lab1), run_time=0.6)
        ghost = DashedVMobject(Circle(radius=0.3, color=TEAL, stroke_width=4)).move_to([x, BOT, 0])
        lab2 = tb("divide", 28, TEAL).move_to([x, -2.05, 0])
        qm = qmark(x, -0.8)
        self.at("divide in another")
        self.play(FadeIn(ghost), FadeIn(lab2), run_time=0.5)
        self.play(FadeIn(qm, scale=0.6), run_time=0.5)
        self.finish()


def old_tag(text="19th century: a fixed section"):
    return left(T(text, 28, GREY), -6.3, 3.5)


class S02His(SpokenScene):
    def construct(self):
        v = vent()
        nucs = VGroup(*wall_nuclei(NYW))
        tag = old_tag()
        rects, lines, labs = old_bands()
        self.add(v, tag)
        self.play(FadeIn(nucs), run_time=0.6)
        self.at("anatomists saw")
        self.play(Indicate(nucs, color=YELLOW, scale_factor=1.12), run_time=0.9)
        self.at("They read the wall")
        self.play(FadeIn(rects), Create(lines), run_time=0.9)
        self.at("several kinds of cells")
        for lb in labs:
            self.play(FadeIn(lb), run_time=0.4)
        self.finish()


class S03Sauer(SpokenScene):
    def construct(self):
        v = vent()
        nucs = wall_nuclei(NYW)
        rects, lines, labs = old_bands()
        tag0 = old_tag()
        self.add(v, *nucs, rects, lines, labs, tag0)
        tag = left(T("F. C. Sauer, 1935", 30, GOLD), -6.3, 3.5)
        self.at("F C Sauer")
        self.play(FadeOut(tag0), FadeIn(tag, shift=DOWN * 0.1), run_time=0.6)
        self.at("simpler picture")
        self.play(FadeOut(rects), FadeOut(lines), FadeOut(labs), run_time=0.8)
        cells = wall_cells()
        self.at("one kind of long cell")
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.1), run_time=1.1)
        self.at("whose nucleus moves")
        n = nucs[2]
        y0 = n.get_center()[1]
        self.play(n.animate.move_to([COLS[2], 1.8, 0]), run_time=1.0)
        self.play(n.animate.move_to([COLS[2], y0, 0]), run_time=1.0)
        self.finish()


class S04Pseudo(SpokenScene):
    def construct(self):
        v = vent()
        cells = wall_cells()
        nucs = wall_nuclei(NYW)
        self.add(v, *cells, *nucs)
        y = 3.12
        br = VGroup(Line([COLS[0] - 0.45, y, 0], [COLS[-1] + 0.45, y, 0], color=BLUE, stroke_width=4),
                    Line([COLS[0] - 0.45, y - 0.12, 0], [COLS[0] - 0.45, y, 0], color=BLUE, stroke_width=4),
                    Line([COLS[-1] + 0.45, y - 0.12, 0], [COLS[-1] + 0.45, y, 0], color=BLUE, stroke_width=4))
        lab = T("one layer of cells", 28, BLUE).move_to([-0.8, 3.5, 0])
        self.at("A single layer of cells")
        self.play(Create(br), FadeIn(lab), run_time=0.9)
        self.at("nuclei at many heights")
        xb = 4.5
        top = VGroup(Line([xb, 2.05, 0], [xb, -2.95, 0], color=YELLOW, stroke_width=4),
                     Line([xb - 0.12, 2.05, 0], [xb, 2.05, 0], color=YELLOW, stroke_width=4),
                     Line([xb - 0.12, -2.95, 0], [xb, -2.95, 0], color=YELLOW, stroke_width=4))
        hl = left(T("many\nheights", 30, YELLOW), xb + 0.25, -0.45)
        self.play(Create(top), FadeIn(hl), run_time=0.8)
        self.at("pseudostratified epithelium")
        term = T("pseudostratified epithelium", 32, TEXT, font=TITLE_FONT).move_to([-0.8, 3.5, 0])
        self.play(ReplacementTransform(lab, term), run_time=0.9)
        self.finish()


def key_icon(text):
    if text.startswith("shaft"):
        ic = RoundedRectangle(corner_radius=0.18, width=0.4, height=0.8, stroke_color=BLUE, stroke_width=4,
                              fill_color=BLUE, fill_opacity=0.25)
    else:
        ic = VGroup(Square(side_length=0.7, stroke_color=YELLOW, stroke_width=5, fill_color=YELLOW, fill_opacity=0.2),
                    Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85))
    return ic


def key_row(text, color, y, target, size=42):
    ic = key_icon(text).move_to([1.5, y, 0])
    t = left(T(text, size, color), 2.0, y)
    ld = Line([1.15, y, 0], target, color=color, stroke_width=2.5)
    dot = Dot(target, radius=0.07, color=color)
    return VGroup(ic, t), VGroup(ld, dot)


class S05Lift(SpokenScene):
    def construct(self):
        v = vent(label=False)
        cells = wall_cells()
        nucs = wall_nuclei(NYW)
        self.add(v, *cells, *nucs)
        shaft = hero_shaft()
        car = nuc_c(HX, B_L, CAR_R)
        head = left(T("the lift picture", 46, TEXT, font=TITLE_FONT), 1.2, 2.5)
        self.at("Picture a lift")
        others = [m for i, m in enumerate(cells) if i != 2] + [m for i, m in enumerate(nucs) if i != 2]
        self.play(*[FadeOut(m) for m in others], ReplacementTransform(cells[2], shaft),
                  ReplacementTransform(nucs[2], car), FadeIn(head), run_time=1.2)
        gf = T("ground floor = the ventricle", 30, GREY).move_to([2.6, -3.4, 0])
        self.at("the ventricle")
        self.play(Indicate(v[0], color=GREY, scale_factor=1.0), FadeIn(gf), run_time=0.8)
        t1, l1 = key_row("shaft = the cell", BLUE, 0.7, [HX + HW / 2, 0.7, 0])
        self.at("The shaft is the cell")
        self.play(FadeIn(t1), Create(l1), Indicate(shaft, color=BLUE, scale_factor=1.0), run_time=0.8)
        cab = lift_car(HX, B_L)[0]
        cable = Line([HX, 2.95, 0], [HX, B_L + CAR_R + 0.08, 0], color="#B8C0CC", stroke_width=7).set_z_index(2)
        t2, l2 = key_row("car = the nucleus", YELLOW, -2.3, [HX + CAR_R + 0.08, -2.3, 0])
        self.at("The car is the nucleus")
        self.play(Create(cab), Create(cable), FadeIn(t2), Create(l2), run_time=1.0)
        self.finish()


class S06Floors(SpokenScene):
    def construct(self):
        d = lift_base(floors=False, band=False, pia=False)
        d["vent"] = vent(label=False)
        add_base(self, d)
        gf = T("ground floor = the ventricle", 30, GREY).move_to([2.6, -3.4, 0])
        t1, l1 = key_row("shaft = the cell", BLUE, 0.7, [HX + HW / 2, 0.7, 0])
        t2, l2 = key_row("car = the nucleus", YELLOW, -2.3, [HX + CAR_R + 0.08, -2.3, 0])
        keys = VGroup(t1, l1, t2, l2).set_opacity(0.55)
        self.add(gf, keys)
        self.at("The shaft runs all the way up")
        self.play(ShowPassingFlash(Line([HX, -3.1, 0], [HX, 2.95, 0], color=BLUE, stroke_width=12), time_width=0.6),
                  run_time=1.4)
        pia = pia_group()
        self.at("to the pia")
        self.play(FadeIn(pia[0], shift=DOWN * 0.1), FadeIn(pia[1]), run_time=0.6)
        fl = make_floors(lit=0)
        for g in fl:
            g.set_stroke(YELLOW, width=4, opacity=0.95)
        self.at("the car only serves")
        self.play(FadeOut(keys), LaggedStart(*[FadeIn(g) for g in fl], lag_ratio=0.1), run_time=1.2)
        self.at("lowest floors")
        bx = HX + HW / 2 + 0.55
        brace = Brace(Line([bx, FLOORS[0] - 0.15, 0], [bx, FLOORS[2] + 0.15, 0]), direction=RIGHT, color=YELLOW, buff=0.02)
        lowl = left(T("lowest floors", 36, YELLOW), bx + 0.7, FLOORS[1])
        abv = left(T("floors above:\nno car", 32, GREY, line_spacing=0.9), bx + 0.3, 1.0)
        self.play(*[g.animate.set_stroke(GREY, width=3, opacity=0.35) for g in fl[3:]],
                  GrowFromCenter(brace), FadeIn(lowl), FadeIn(abv), run_time=0.9)
        band = hero_band()
        self.at("the ventricular zone")
        self.play(FadeIn(band), run_time=0.8)
        self.finish()


def lit_anims(arcs, name):
    return [arcs[k].animate.set_stroke(opacity=1 if k == name else 0.35) for k in arcs]


class S07G1(SpokenScene):
    def construct(self):
        d = lift_base()
        add_base(self, d)
        car = d["car"]
        arcs, labs = ring_arcs(), ring_labels()
        ring = VGroup(*arcs.values(), *labs.values(), T("cell cycle", 26, GREY).move_to(RING_C))
        marker = Dot(pt_on_ring(60), radius=0.14, color=YELLOW).set_z_index(5)
        c1 = cap("G1", "the car rides up")
        self.play(FadeIn(ring), FadeIn(marker), FadeIn(c1), run_time=0.7)
        self.at("the car rides up")
        self.play(car.animate.move_to([HX, S_L, 0]), MoveAlongPath(marker, arcs["G1"]), *lit_anims(arcs, "G1"),
                  run_time=1.4, rate_func=linear)
        self.at("It stops near the top")
        self.play(FadeOut(c1), run_time=0.3)
        glow = Circle(radius=0.95, color=TEAL, stroke_width=5).move_to([HX, S_L, 0]).set_z_index(4)
        c2 = cap("S phase", "")
        self.at("S phase")
        self.play(Create(glow), MoveAlongPath(marker, arcs["S"]), *lit_anims(arcs, "S"), FadeIn(c2),
                  run_time=0.9, rate_func=linear)
        self.at("when DNA is copied")
        c3 = cap("S phase", "DNA is copied")
        self.play(Transform(c2, c3), run_time=0.5)
        self.finish()


class S08G2(SpokenScene):
    def construct(self):
        d = lift_base()
        add_base(self, d)
        car = d["car"]
        car.move_to([HX, S_L, 0])
        arcs, labs = ring_arcs(), ring_labels()
        ring = VGroup(*arcs.values(), *labs.values(), T("cell cycle", 26, GREY).move_to(RING_C))
        arcs["S"].set_stroke(opacity=1)
        marker = Dot(pt_on_ring(-170), radius=0.14, color=YELLOW).set_z_index(5)
        glow = Circle(radius=0.95, color=TEAL, stroke_width=5).move_to([HX, S_L, 0]).set_z_index(4)
        c3 = cap("S phase", "DNA is copied")
        self.add(ring, marker, glow, c3)
        self.at("In G2")
        c4 = cap("G2", "the car comes down")
        self.play(FadeOut(glow), FadeOut(c3), run_time=0.25)
        self.play(FadeIn(c4), *lit_anims(arcs, "G2"), run_time=0.4)
        self.at("it comes back down")
        self.play(car.animate.move_to([HX, B_L, 0]), MoveAlongPath(marker, arcs["G2"]), run_time=1.2, rate_func=linear)
        self.at("ground floor")
        self.play(d["floors"][0].animate.set_stroke(TEXT, width=8), run_time=0.3)
        self.play(d["floors"][0].animate.set_stroke(YELLOW, width=4), run_time=0.3)
        ap = left(T("apical surface", 30, GREY), LX, -2.3)
        self.at("the apical surface")
        self.play(FadeIn(ap), run_time=0.5)
        rnd = Circle(radius=0.85, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.18).move_to([HX, B_L, 0])
        rnd.set_z_index(2)
        self.at("The cell divides there")
        nc = car[1]
        pair = dumb(HX, B_L, r=0.3, dx=0.42)
        c5 = cap("M", "the cell divides")
        self.play(FadeOut(c4), FadeOut(ap), run_time=0.25)
        self.play(FadeIn(rnd, scale=0.6), FadeOut(car[0]), FadeOut(d["cable"]), ReplacementTransform(nc, pair),
                  FadeIn(c5), MoveAlongPath(marker, arcs["M"]), *lit_anims(arcs, "M"), run_time=0.7,
                  rate_func=linear)
        cut = Line([HX, B_L + 0.85, 0], [HX, B_L - 0.85, 0], color=BLUE, stroke_width=4).set_z_index(5)
        self.play(Create(cut), run_time=0.5)
        self.finish()


def run_cars(tracker, cars, k):
    def upd(i):
        u0, S = CYC[i]

        def f(m):
            m.move_to([COLS[i], ny_of(u0 - 1 + tracker.get_value(), S, k=k), 0])
        return f
    for i, c in enumerate(cars):
        c.add_updater(upd(i))


class S09Own(SpokenScene):
    def construct(self):
        v = vent()
        d = lift_base(floors=False, band=False, pia=False)
        shaft = d["shaft"]
        car = d["car"]
        self.add(v, shaft, d["cable"], car)
        cells = wall_cells()
        cars = wall_nuclei(NYM, cab=True)
        band = wall_band()
        self.at("Each cell's car")
        others = [m for i, m in enumerate(cells) if i != 2] + [m for i, m in enumerate(cars) if i != 2]
        self.play(ReplacementTransform(shaft, cells[2]), ReplacementTransform(car, cars[2]), FadeOut(d["cable"]),
                  *[FadeIn(m) for m in others], FadeIn(band), run_time=0.9)
        tr = ValueTracker(0)
        run_cars(tr, cars, K_MODEL)
        self.at("runs on its own timetable")
        self.play(tr.animate.set_value(1), run_time=1.9, rate_func=linear)
        for c in cars:
            c.clear_updaters()
        self.at("That is why nuclei sit")
        self.play(Indicate(VGroup(*cars), color=YELLOW, scale_factor=1.1), run_time=1.0)
        self.finish()


class S10Name(SpokenScene):
    def construct(self):
        strip = Rectangle(width=13.2, height=0.75, stroke_width=0, fill_color=GREY, fill_opacity=0.3).move_to([0, -3.43, 0])
        cells = wall_cells()
        cars = wall_nuclei(NYM, cab=True)
        band = wall_band()
        self.add(strip, band, *cells, *cars)
        tr = ValueTracker(0)
        run_cars(tr, cars, K_MODEL)
        tr.add_updater(lambda m, dt: m.increment_value(dt / 2.8))
        self.add(tr)
        term = T("interkinetic nuclear migration", 34, TEXT, font=TITLE_FONT)
        gloss = T("= movement between divisions", 28, GREY)
        row = VGroup(term, gloss).arrange(RIGHT, buff=0.35)
        fit(row, max_w=12.6)
        row.move_to([0, -3.43, 0]).set_z_index(10)
        self.at("interkinetic nuclear migration")
        self.play(FadeIn(term, shift=UP * 0.1), run_time=1.0)
        self.at("Movement between divisions")
        self.play(FadeIn(gloss), run_time=0.5)
        self.finish()


class S11Thy(SpokenScene):
    def construct(self):
        v = vent()
        cells = wall_cells()
        nucs = wall_nuclei(NYM)
        band = wall_band()
        self.add(v, band, *cells, *nucs)
        RX = 5.55
        face = Circle(radius=0.5, stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=1).move_to([RX, 2.75, 0]).set_z_index(10)
        hand = Line(face.get_center(), face.get_center() + UP * 0.34, color=TEXT, stroke_width=4).set_z_index(11)
        hand2 = Line(face.get_center(), face.get_center() + RIGHT * 0.24, color=TEXT, stroke_width=3).set_z_index(11)
        self.at("A pulse label")
        self.play(Create(face), Create(hand), Create(hand2), run_time=0.9)
        self.at("timetable")
        self.play(Rotate(hand, angle=-TAU, about_point=face.get_center()), run_time=1.5, rate_func=linear)
        chip_t = bchip("tritiated\nthymidine", ORANGE, size=28).move_to([RX, 1.6, 0])
        self.at("Tritiated thymidine")
        self.play(FadeIn(chip_t, shift=DOWN * 0.1), run_time=0.5)
        flights = []
        for i in S_CELLS:
            for dxy in ((-0.1, 0.1), (0.1, -0.1)):
                f = Dot([RX, 1.6, 0], radius=0.09, color=ORANGE).set_z_index(12)
                flights.append((f, [COLS[i] + dxy[0], NYM[i] + dxy[1], 0]))
        self.add(*[f for f, _ in flights])
        self.play(*[f.animate.move_to(p) for f, p in flights], run_time=1.0)
        labn = [lab_nuc(COLS[i], NYM[i], 0.26) for i in S_CELLS]
        lg = legend(5.4, -2.7)
        self.play(*[Transform(nucs[i], l) for i, l in zip(S_CELLS, labn)], *[FadeOut(f) for f, _ in flights],
                  FadeIn(lg), run_time=0.5)
        sub = T("radioactive DNA\nbuilding block", 26, ORANGE, line_spacing=0.85).move_to([RX, 0.25, 0])
        self.at("radioactive DNA building block")
        self.play(FadeIn(sub), run_time=0.6)
        tag = left(T("S phase only", 28, TEAL), 4.6, -0.4)
        ld = arr([4.55, -0.5, 0], [COLS[9] + 0.5, NYM[9] + 0.0, 0], TEAL, w=4, tip=0.18)
        self.at("only in S phase")
        self.play(FadeIn(tag), GrowArrow(ld), run_time=0.5)
        self.finish()


class S12Predict(SpokenScene):
    def construct(self):
        line, pdot, plab, ticks, conn = timeline()
        p1, p2 = panel(PX[0]), panel(PX[1])
        h1, h2 = header("soon after the pulse", PX[0]), header("later", PX[1])
        q1, q2 = qtexts()
        m1, m2 = qmark(PX[0], -0.4), qmark(PX[1], -2.3)
        o1, o2 = dim(PX[0], 0.65), dim(PX[1], 0.65)
        self.add(line, p1, p2, o1, o2)
        self.play(FadeIn(pdot, scale=0.5), FadeIn(plab), run_time=0.6)
        self.at("then fix the tissue at intervals")
        self.play(FadeIn(ticks), FadeOut(o1), FadeOut(o2), run_time=1.0)
        self.at("Soon after the pulse")
        self.play(FadeIn(h1), FadeIn(conn[0]), run_time=0.5)
        self.at("the labeled nuclei")
        self.play(FadeIn(q1), FadeIn(m1, scale=0.6), run_time=0.6)
        self.at("And when do labeled mitoses appear")
        self.play(FadeIn(h2), FadeIn(conn[1]), FadeIn(q2), FadeIn(m2, scale=0.6), run_time=0.7)
        self.finish()


class S13Pause(NarratedScene):
    def construct(self):
        line, pdot, plab, ticks, conn = timeline()
        p1, p2 = panel(PX[0]), panel(PX[1])
        h1, h2 = header("soon after the pulse", PX[0]), header("later", PX[1])
        q1, q2 = qtexts()
        m1, m2 = qmark(PX[0], -0.4), qmark(PX[1], -2.3)
        self.add(line, pdot, plab, ticks, conn, p1, p2, h1, h2, q1, q2, m1, m2)
        turn = bchip("your turn: predict", RED, size=28).move_to([0.2, 3.5, 0])
        self.play(FadeIn(turn), run_time=0.4)
        def numb(n):
            return VGroup(Circle(radius=0.36, stroke_color=RED, stroke_width=3, fill_color=BG, fill_opacity=1),
                          T(str(n), 36, RED, weight=BOLD)).move_to([2.9, 3.5, 0]).set_z_index(10)
        num = numb(5)
        self.add(num)
        for n in (5, 4, 3, 2, 1):
            new = numb(n)
            self.remove(num)
            num = new
            self.add(num)
            self.wait(1.0 if n != 5 else 0.6)
        self.finish()


class S14Rev1(SpokenScene):
    def construct(self):
        line, pdot, plab, ticks, conn = timeline()
        p1, p2 = panel(PX[0]), panel(PX[1])
        h1, h2 = header("soon after the pulse", PX[0]), header("later", PX[1], GREY)
        q1, q2 = qtexts()
        m1, m2 = qmark(PX[0], -0.4), qmark(PX[1], -2.3)
        self.add(line, pdot, plab, ticks, conn, p1, p2, h1, h2, q1, q2, m1, m2)
        unl, lab, mit = p1_items()
        band1 = pband(PX[0])
        ov = dim(PX[1])
        cell0 = nuc_c(PX[0], P_MIT, PR)
        self.play(FadeOut(q1), FadeOut(m1), FadeIn(ov), FadeIn(band1), *[FadeIn(n) for n in unl], FadeIn(cell0), run_time=0.9)
        self.at("labeled nuclei sit out")
        lg = legend(5.4, 3.5)
        self.play(*[FadeIn(n, scale=1.7) for n in lab], FadeIn(lg), run_time=0.8)
        br = pbracket()
        self.at("in the ventricular zone")
        self.play(Create(br[0]), FadeIn(br[1]), run_time=0.7)
        self.at("No cell in mitosis")
        self.play(ReplacementTransform(cell0, mit), run_time=0.6)
        ml = tb("in mitosis", 26, GREY).move_to([PX[0], -4.05, 0])
        self.play(FadeIn(ml), run_time=0.4)
        self.at("is labeled")
        ml2 = tb("mitosis: no label", 26, TEXT).move_to([PX[0], -4.05, 0])
        self.play(Transform(ml, ml2), run_time=0.5)
        self.finish()


class S15Rev2(SpokenScene):
    def construct(self):
        line, pdot, plab, ticks, conn = timeline()
        p1, p2 = panel(PX[0]), panel(PX[1])
        h1, h2 = header("soon after the pulse", PX[0], GREY), header("later", PX[1])
        unl1, lab1, mit1 = p1_items()
        band1, band2 = pband(PX[0]), pband(PX[1])
        br = pbracket()
        lg = legend(5.4, 3.5)
        ml = tb("mitosis: no label", 26, TEXT).move_to([PX[0], -4.05, 0])
        self.add(line, pdot, plab, ticks, conn, p1, p2, h1, h2, band1, band2, *unl1, *lab1, mit1, br, lg, ml)
        ov = dim(PX[0])
        self.add(ov)
        unl2, mit2 = p2_items()
        self.play(*[FadeIn(n) for n in unl2], run_time=0.6)
        self.at("the labeled nuclei")
        a = lab_nuc(PX[1] + P1_LAB[0][0], P1_LAB[0][1], PR)
        b = lab_nuc(PX[1] + P1_LAB[1][0], P1_LAB[1][1], PR)
        self.play(TransformFromCopy(lab1[0], a), TransformFromCopy(lab1[1], b), run_time=0.7)
        self.at("come down")
        self.play(a.animate.move_to([PX[1] + P2_LAB[0][0], P_MIT, 0]), b.animate.move_to([PX[1] + P2_LAB[1][0], P_MIT, 0]),
                  run_time=0.9)
        self.at("divide at the ventricle")
        self.play(ReplacementTransform(a, mit2[0]), ReplacementTransform(b, mit2[1]), run_time=0.6)
        tl = tb("labeled mitosis", 26, ORANGE).move_to([PX[1], -4.05, 0])
        self.play(FadeIn(tl), run_time=0.4)
        self.finish()


class S16Y1959(SpokenScene):
    def construct(self):
        p1, p2 = panel(PX[0]), panel(PX[1])
        h1, h2 = header("soon after the pulse", PX[0]), header("later", PX[1])
        band1, band2 = pband(PX[0]), pband(PX[1])
        unl1, lab1, mit1 = p1_items()
        unl2, mit2 = p2_items()
        br = pbracket()
        lg = legend(5.4, 2.4)
        self.add(p1, p2, h1, h2, band1, band2, *unl1, *lab1, mit1, *unl2, *mit2, br)
        self.add(dim(PX[0], 0.42), dim(PX[1], 0.42))
        yr = T("1959", 44, TEXT, font=TITLE_FONT).move_to([0.1, 3.5, 0])
        self.at("In 1959")
        self.play(FadeIn(yr), run_time=0.5)
        c1 = chip("M. E. Sauer and Walker", GOLD, size=26, pad=0.12).move_to([-3.9, 3.5, 0]).set_z_index(12)
        c2 = chip("Sidman, Miale and Feder", GOLD, size=26, pad=0.12).move_to([4.1, 3.5, 0]).set_z_index(12)
        self.at("two groups")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.5)
        self.at("reported this")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
        step = T("labeled nuclei move in step with the cell cycle", 30, TEAL).move_to([0.3, 2.4, 0]).set_z_index(12)
        self.at("Labeled nuclei moved in step")
        self.play(FadeIn(step), run_time=0.7)
        ar = arr([-1.7, -0.9, 0], [2.3, -2.5, 0], TEAL, w=7, tip=0.3).set_z_index(12)
        self.at("with the cell cycle")
        self.play(GrowArrow(ar), run_time=0.9)
        self.finish()


class S17Atlas(SpokenScene):
    def construct(self):
        AY = -0.1
        head = T("11-day mouse embryos", 36, TEXT, font=TITLE_FONT).move_to([-2.0, 3.3, 0])
        axis = Arrow([-6.2, AY, 0], [2.6, AY, 0], buff=0, color=GREY, stroke_width=9, tip_length=0.3)
        inj = Dot([-5.6, AY, 0], radius=0.26, color=ORANGE).set_z_index(5)
        injl = T("injection", 30, ORANGE).move_to([-5.4, AY + 0.65, 0])
        zero = T("0", 30, TEXT).move_to([-5.6, AY - 0.6, 0])
        axt = right_at(T("time after injection", 26, GREY), 2.7, AY - 0.6)
        # the small lift: same geometry as the hero shaft, narrower; present from the pulse, nucleus in S phase
        SX = 4.75
        band = Rectangle(width=3.5, height=3.15 + VZ_TOP, stroke_width=0, fill_color=GREY, fill_opacity=0.14).move_to([SX, (VZ_TOP - 3.15) / 2, 0])
        shaft = RoundedRectangle(corner_radius=0.4, width=1.9, height=5.1, stroke_color=BLUE, stroke_width=3.5,
                                 fill_color=BLUE, fill_opacity=0.12).move_to([SX, -0.6, 0])
        stripv = Rectangle(width=3.5, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to([SX, -3.4, 0])
        vl = T("ventricle", 26, GREY).move_to([SX, -3.4, 0])
        nuc = lab_nuc(SX, S_L, 0.38)
        slab = T("labeled, in S phase", 26, ORANGE).move_to([SX, 2.55, 0])
        self.play(FadeIn(head), FadeIn(axis), FadeIn(inj, scale=0.5), FadeIn(injl), FadeIn(zero), FadeIn(axt),
                  FadeIn(band), FadeIn(shaft), FadeIn(stripv), FadeIn(vl), FadeIn(nuc), FadeIn(slab), run_time=0.8)
        bar = Line([-5.6, AY, 0], [-1.6, AY, 0], color=GREY, stroke_width=26).set_stroke(opacity=0.55)
        barl = T("no labeled mitosis", 30, GREY).move_to([-3.4, AY + 1.45, 0])
        self.at("no labeled mitosis appeared")
        self.play(Create(bar), FadeIn(barl), run_time=1.0)
        tick = Line([-1.6, AY - 0.38, 0], [-1.6, AY + 0.38, 0], color=TEXT, stroke_width=7)
        tl = T("1 h", 32, TEXT).move_to([-1.6, AY - 0.65, 0])
        self.at("until an hour")
        self.play(Create(tick), FadeIn(tl), run_time=0.7)
        mits = VGroup(*[mit_lab(x, AY + 1.1) for x in (-0.5, 0.75, 2.0)])
        ml = T("first labeled mitoses", 30, ORANGE).move_to([0.8, AY + 2.0, 0])
        self.at("after the injection")
        self.play(FadeIn(mits, scale=0.5), FadeIn(ml), run_time=0.7)
        by = AY - 1.25
        brace = Brace(Line([-5.6, by, 0], [-1.6, by, 0]), direction=DOWN, color=TEAL, buff=0.05)
        lag = T("lag to first labeled mitosis", 30, TEXT).move_to([-3.6, by - 0.8, 0])
        self.at("That lag")
        self.play(GrowFromCenter(brace), FadeIn(lag), run_time=0.8)
        g2 = T("roughly G2", 56, TEAL, weight=BOLD).move_to([-3.6, by - 1.8, 0])
        self.at("spans G2")
        self.play(FadeIn(g2, scale=0.8), run_time=0.6)
        trip = T("the trip back down", 28, TEXT).move_to([SX, 2.55, 0])
        marker = Dot([-5.6, AY, 0], radius=0.2, color=ORANGE).set_z_index(6)
        self.at("which includes")
        self.add(marker)
        self.play(FadeOut(slab), run_time=0.3)
        self.at("the trip back down")
        self.play(FadeIn(trip), nuc.animate.move_to([SX, -2.7, 0]),
                  marker.animate.move_to([-1.6, AY, 0]), run_time=1.1, rate_func=linear)
        pair = mit_lab(SX, -2.7)
        self.play(ReplacementTransform(nuc, pair), FadeOut(marker), run_time=0.3)
        self.finish()


def why_rows():
    specs = [("centrosome", PURPLE, "partly known", GOLD, 1.0), ("packing", TEXT, "proposal", GREY, -0.5),
             ("signals", PINK, "proposal", GREY, -2.0)]
    rows = []
    for topic, tcol, status, scol, y in specs:
        box = RoundedRectangle(corner_radius=0.2, width=11.0, height=1.2, stroke_color=scol, stroke_width=3,
                               fill_color=scol, fill_opacity=0.08).move_to([0, y, 0])
        t = left(T(topic, 42, tcol), -5.2, y)
        s = right_at(T(status, 36, scol), 5.2, y)
        rows.append(VGroup(box, t, s))
    return rows


class S18Why(SpokenScene):
    def construct(self):
        q = T("Why divide at the ventricle?", 52, TEXT, font=TITLE_FONT).move_to([0, 2.7, 0])
        rows = why_rows()
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.at("The answer")
        self.play(FadeIn(rows[0], shift=UP * 0.1), run_time=0.5)
        self.at("partly")
        self.play(FadeIn(rows[1], shift=UP * 0.1), run_time=0.4)
        self.at("settled")
        self.play(FadeIn(rows[2], shift=UP * 0.1), run_time=0.4)
        self.finish()


# ----- the zoomed apical end (s19, s20)
CX2 = -2.6
CW2 = 4.4
SURF = -0.9
NUC_R = 1.3
LBL = 0.35   # left edge of labels in the close-up scenes


def closeup(nuc_y=3.4):
    vz = Rectangle(width=13.2, height=SURF + 3.8, stroke_width=0, fill_color=GREY, fill_opacity=0.2).move_to([0, (SURF - 3.8) / 2, 0])
    vl = T("ventricle", 26, GREY).move_to([5.6, -3.4, 0])
    cell = RoundedRectangle(corner_radius=0.25, width=CW2, height=7.4, stroke_color=BLUE, stroke_width=3.5,
                            fill_color=BLUE, fill_opacity=0.12).move_to([CX2, SURF + 3.7, 0])
    foot = Line([CX2 - CW2 / 2, SURF, 0], [CX2 + CW2 / 2, SURF, 0], color=BLUE, stroke_width=9).set_z_index(2)
    nuc = Circle(radius=NUC_R, stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.85) \
        .move_to([CX2, nuc_y, 0]).set_z_index(3)
    return {"vz": VGroup(vz, vl), "cell": cell, "foot": foot, "nuc": nuc}


def centrosome(dy=0.0):
    mother = RoundedRectangle(corner_radius=0.08, width=0.45, height=1.5, stroke_width=0, fill_color=PURPLE, fill_opacity=1) \
        .move_to([CX2 - 0.45, SURF + 0.75, 0])
    daughter = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.45, stroke_width=0, fill_color=PURPLE, fill_opacity=1) \
        .move_to([CX2 + 0.75, SURF + 0.45, 0])
    g = VGroup(mother, daughter).shift(UP * dy)
    g.set_z_index(4)
    return g


def cilium():
    return ArcBetweenPoints([CX2 - 0.45, SURF, 0], [CX2 - 0.1, -3.3, 0], angle=-0.3, color=PURPLE, stroke_width=12).set_z_index(3)


def lbl_line(text, size, color, y, target, x=LBL):
    t = left(T(text, size, color), x, y)
    ld = Line([x - 0.08, y, 0], target, color=color, stroke_width=2.5)
    return t, ld


class S19Centro(SpokenScene):
    def construct(self):
        d = closeup()
        self.add(d["vz"], d["cell"], d["foot"], d["nuc"])
        tag = chip("partly known", GOLD, size=30).move_to([4.8, 3.3, 0])
        self.at("The best supported part")
        self.play(FadeIn(tag, shift=DOWN * 0.1), run_time=0.5)
        il, ild = lbl_line("interphase", 34, TEAL, 2.55, [CX2 + NUC_R - 0.05, 2.7, 0])
        self.at("For much of interphase")
        self.play(FadeIn(il), Create(ild), run_time=0.5)
        cen = centrosome()
        cl, cld = lbl_line("centrosome", 34, PURPLE, 0.45, [CX2 + 1.55, SURF + 0.5, 0])
        self.at("the centrosome sits")
        self.play(FadeIn(cen, scale=1.6), FadeIn(cl), Create(cld), run_time=0.8)
        sl, sld = lbl_line("apical surface", 34, GREY, -1.0, [CX2 + CW2 / 2 + 0.03, SURF, 0])
        self.at("at the apical surface")
        self.play(FadeIn(sl), Create(sld), run_time=0.5)
        cil = cilium()
        self.at("the base of")
        self.play(Create(cil), run_time=1.0)
        pl, pld = lbl_line("primary cilium", 34, PURPLE, -2.6, [CX2 - 0.22, -2.6, 0])
        self.at("primary cilium")
        self.play(FadeIn(pl), Create(pld), run_time=0.5)
        self.finish()


def fan_group(center, L):
    n = 7
    lines = []
    for a in np.deg2rad(np.linspace(-55, 55, n)):
        lines.append(Line(center, center + max(L, 0.01) * np.array([np.sin(a), np.cos(a), 0]), color=PURPLE, stroke_width=4))
    g = VGroup(*lines)
    g.set_z_index(4)
    return g


class S20Spindle(SpokenScene):
    def construct(self):
        d = closeup()
        cen = centrosome()
        nuc = d["nuc"]
        cl, cld = lbl_line("centrosome", 34, PURPLE, 0.45, [CX2 + 1.55, SURF + 0.5, 0])
        sl, sld = lbl_line("apical surface", 34, GREY, -1.0, [CX2 + CW2 / 2 + 0.03, SURF, 0])
        tag = chip("partly known", GOLD, size=30).move_to([4.8, 3.3, 0])
        self.add(d["vz"], d["cell"], d["foot"], nuc, cen, cl, cld, sl, sld, tag)
        L = ValueTracker(0.0)
        fan = fan_group(cen[0].get_top() + RIGHT * 0.2, 0.0)
        fan.add_updater(lambda m: m.become(fan_group(cen[0].get_top() + RIGHT * 0.2, L.get_value())))
        self.add(fan)
        sp, spd = lbl_line("spindle", 34, PURPLE, 1.55, [CX2 + 0.45, SURF + 1.95, 0])
        self.at("builds its spindle")
        self.play(L.animate.set_value(0.8), FadeIn(sp), Create(spd), run_time=1.0)
        tg2 = chip("usual account, not settled", GOLD, size=28)
        tg2.move_to([6.6 - tg2.width / 2, 3.3, 0])
        self.at("On the usual account")
        self.play(ReplacementTransform(tag, tg2), run_time=0.6)
        self.at("the nucleus travels")
        self.play(nuc.animate.move_to([CX2, SURF + 1.5 + NUC_R + 0.2, 0]), FadeOut(sp), FadeOut(spd), run_time=0.95)
        self.at("meet them")
        d1 = Circle(radius=0.62, stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.85).move_to([CX2 - 0.85, 2.1, 0]).set_z_index(3)
        d2 = d1.copy().move_to([CX2 + 0.85, 2.1, 0])
        cut = Line([CX2, SURF, 0], [CX2, 3.0, 0], color=BLUE, stroke_width=4).set_z_index(5)
        dl = left(T("the cell splits", 34, YELLOW), LBL, 2.1)
        self.play(L.animate.set_value(1.35), ReplacementTransform(nuc, VGroup(d1, d2)), Create(cut), FadeIn(dl), run_time=0.5)
        late = left(T("late G2", 34, TEAL), LBL, 2.55)
        nuc2 = Circle(radius=NUC_R, stroke_color=YELLOW, stroke_width=3.5, fill_color=YELLOW, fill_opacity=0.85).move_to([CX2, 3.0, 0]).set_z_index(3)
        self.at("in G2")
        self.play(FadeOut(d1), FadeOut(d2), FadeOut(cut), FadeOut(dl), FadeOut(fan), FadeIn(nuc2), FadeIn(late), run_time=0.5)
        fan.clear_updaters()
        self.at("the centrosome can also move")
        up = 0.9
        self.play(nuc2.animate.move_to([CX2, 2.85, 0]), cen.animate.shift(UP * up), cl.animate.shift(UP * up),
                  cld.animate.shift(UP * up), run_time=1.4)
        self.at("meet the nucleus")
        self.play(Indicate(cen, color=PURPLE, scale_factor=1.15), run_time=0.7)
        self.finish()


# ----- packing (s21-s23): the ventricular surface seen from above
CX0, CY0, PC, PF = -5.2, -2.8, 1.4, 0.7


def coarse(k, j):
    return (CX0 + PC * k, CY0 + PC * j)


COARSE = [coarse(k, j) for k in range(7) for j in range(5)]
FINE = [(CX0 + PF * a, CY0 + PF * b) for a in range(1, 12, 2) for b in range(1, 8, 2)]   # centres of the squares: a staggered lattice
ROUNDS_A = [coarse(1, 3), coarse(4, 1), coarse(5, 3)]
ROUNDS_B = [coarse(2, 0), coarse(3, 3), coarse(6, 2)]
RR = 0.6


def foot(p, s=0.36):
    return Square(side_length=s, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.75).move_to([p[0], p[1], 0])


def rnd(p, r=RR):
    return Circle(radius=r, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.2).move_to([p[0], p[1], 0])


def near(p, q, rad):
    return np.hypot(p[0] - q[0], p[1] - q[1]) < rad


def want(rounds, fine=True):
    s = set()
    for p in COARSE:
        if not any(near(p, r, 0.1) for r in rounds):
            s.add(p)
    if fine:
        for p in FINE:
            if all(not near(p, r, 0.9) for r in rounds):
                s.add(p)
    return s


def count_label(n, y=-2.2):
    big = M(f"{n} cells", 40, TEAL)
    small = T("in this patch", 26, GREY)
    g = VGroup(big, small).arrange(DOWN, buff=0.08)
    return left(g, 3.95, y)


class S21Pack(SpokenScene):
    def construct(self):
        feet = {p: foot(p) for p in COARSE}
        title = T("ventricular surface, seen from above", 28, GREY).move_to([-1.0, 3.5, 0])
        tag = chip("proposal", GREY, size=28).move_to([5.3, 3.3, 0])
        self.play(*[FadeIn(f) for f in feet.values()], FadeIn(title), FadeIn(tag), run_time=1.0)
        rs = [rnd(p) for p in ROUNDS_A]
        self.at("a cell in mitosis")
        self.play(*[FadeOut(feet[p]) for p in ROUNDS_A if p in feet], *[GrowFromCenter(r) for r in rs], run_time=0.9)
        l1 = left(T("in mitosis:\nround and wide", 28, TEAL), 3.95, 1.9)
        ld = Line([3.9, 1.9, 0], [ROUNDS_A[2][0] + RR + 0.03, ROUNDS_A[2][1] + 0.1, 0], color=TEAL, stroke_width=2.5)
        self.at("round and wide")
        self.play(FadeIn(l1), Create(ld), run_time=0.6)
        l2 = left(T("the rest:\nthin feet", 28, BLUE), 3.95, -0.4)
        samp = [feet[coarse(6, 1)], feet[coarse(6, 3)], feet[coarse(2, 2)]]
        ld2 = Line([3.9, -0.4, 0], [coarse(6, 1)[0] + 0.2, coarse(6, 1)[1] + 0.1, 0], color=BLUE, stroke_width=2.5)
        self.at("The rest can stay thin")
        self.play(FadeIn(l2), Create(ld2), *[Indicate(m, color=BLUE, scale_factor=1.8) for m in samp], run_time=1.0)
        n = len(want(ROUNDS_A, fine=False)) + len(ROUNDS_A)
        self.play(FadeIn(count_label(n)), run_time=0.6)
        self.finish()


class S22Pack2(SpokenScene):
    def construct(self):
        U = 0.3   # one micrometre drawn as 0.3 units, for both shapes
        tag = T("illustrative numbers", 28, GOLD).move_to([3.7, 3.45, 0])
        asm = T("12 h cycle, 0.5 h in mitosis,\nspread evenly through the cycle:\n1 cell in 24 is dividing", 28, TEXT,
                line_spacing=0.9).move_to([3.7, 1.95, 0])
        self.add(tag, asm)
        circ = Circle(radius=5 * U, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.2).move_to([-4.5, 0.55, 0])
        cl = T("round cell\n10 µm across", 28, TEXT, line_spacing=0.9).move_to([-4.5, 2.9, 0])
        ca = M("π × 5² ≈ 80 µm²", 28, TEXT).move_to([-4.5, -1.35, 0])
        self.at("A round cell")
        self.play(FadeIn(circ, scale=0.6), FadeIn(cl), run_time=0.7)
        self.play(FadeIn(ca), run_time=0.5)
        sq = Square(side_length=2 * U, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.75).move_to([-1.4, 0.55, 0])
        fl = T("thin foot\n2 × 2 µm", 28, TEXT, line_spacing=0.9).move_to([-1.4, 2.9, 0])
        fa = M("= 4 µm²", 28, TEXT).move_to([-1.4, -1.35, 0])
        self.at("the room of a thin foot")
        self.play(FadeIn(sq, scale=0.6), FadeIn(fl), run_time=0.6)
        self.play(FadeIn(fa), run_time=0.4)
        ratio = M("80 ÷ 4 = 20 times", 36, TEAL).move_to([-3.0, -2.55, 0])
        self.at("thin foot")
        self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.5)
        f1 = M("(80 + 23 × 4) / 24", 32, TEXT).move_to([3.7, 0.35, 0])
        self.at("So on average")
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.5)
        f2 = M("≈ 7 µm² per cell", 36, TEXT).move_to([3.7, -0.55, 0])
        self.at("each cell needs")
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.5)
        tenth = chip("about a tenth of a dividing cell", TEAL, size=30).move_to([3.7, -2.0, 0])
        self.at("about a tenth")
        self.play(FadeIn(tenth, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S23Pack3(SpokenScene):
    def construct(self):
        objs = {p: foot(p) for p in COARSE + FINE}
        vis = want(ROUNDS_A, fine=False)
        rs = [rnd(p) for p in ROUNDS_A]
        title = T("ventricular surface, seen from above", 28, GREY).move_to([-1.0, 3.5, 0])
        tag = chip("proposal", GREY, size=28).move_to([5.3, 3.3, 0])
        cnt = count_label(len(vis) + len(rs))
        same = left(T("same surface,\nmore cells", 28, TEXT), 3.95, 0.9)
        self.add(title, tag, *[objs[p] for p in vis], *rs, cnt)

        def switch(new_rounds, cur_rs, cur_vis, fine, run):
            nv = want(new_rounds, fine=fine)
            outs = [objs[p] for p in cur_vis - nv]
            ins = [objs[p] for p in nv - cur_vis]
            nrs = [rnd(p) for p in new_rounds]
            anims = [FadeOut(m) for m in outs] + [FadeIn(m) for m in ins] + [FadeOut(r) for r in cur_rs] + [GrowFromCenter(r) for r in nrs]
            self.play(*anims, run_time=run)
            return nrs, nv
        self.at("Staggered timetables")
        rs, vis = switch(ROUNDS_B, rs, vis, False, 0.6)
        self.at("more progenitors")
        rs, vis = switch(ROUNDS_B, rs, vis, True, 0.5)
        newc = count_label(len(vis) + len(rs))
        self.play(Transform(cnt, newc), FadeIn(same), run_time=0.4)
        self.at("share the ventricle")
        rs, vis = switch(ROUNDS_A, rs, vis, True, 0.6)
        newc2 = count_label(len(vis) + len(rs))
        self.play(Transform(cnt, newc2), run_time=0.3)
        self.finish()


def sig(y):
    return float(np.exp(-(y + 3.15) / 2.2))


class S24Signal(SpokenScene):
    def construct(self):
        XA, XB = -4.3, -0.3
        PXC, PWD = 0.0, 13.2
        v = vent(label=False)
        frame = Rectangle(width=PWD, height=6.1, stroke_color=GREY, stroke_width=2, stroke_opacity=0.7).move_to([PXC, CELL_Y, 0]).set_z_index(1)
        shafts = [RoundedRectangle(corner_radius=0.45, width=3.0, height=CELL_H, stroke_color=BLUE, stroke_width=3,
                                   fill_color=BLUE, fill_opacity=0.08).move_to([x, CELL_Y, 0]).set_z_index(1) for x in (XA, XB)]
        n = 36
        h = 6.1 / n
        slices = VGroup(*[Rectangle(width=PWD, height=h + 0.01, stroke_width=0, fill_color=PINK,
                                    fill_opacity=0.6 * sig(-3.15 + (i + 0.5) * h))
                          .move_to([PXC, -3.15 + (i + 0.5) * h, 0]) for i in range(n)])
        slices.set_z_index(0)
        nl = left(tb("Notch signal", 38, PINK, weight=BOLD), 3.3, 0.1)
        strong = left(tb("strong, apical", 32, PINK), 3.3, -2.5)
        weak = left(tb("weak, basal", 32, PINK), 3.3, 2.5)
        self.add(v)
        tag = chip("proposal", GREY, size=28).move_to([5.4, 3.4, 0])
        self.play(FadeIn(frame), FadeIn(slices), FadeIn(*shafts), FadeIn(nl), FadeIn(strong), FadeIn(weak),
                  FadeIn(tag, shift=DOWN * 0.1), run_time=0.9)
        zt = left(tb("zebrafish retina,\n2008", 28, GOLD, line_spacing=0.9), 3.3, -1.0)
        self.at("In zebrafish retina")
        self.play(FadeIn(zt), run_time=0.5)
        fall = arr([3.0, -2.5, 0], [3.0, 2.4, 0], PINK, w=6, tip=0.3)
        self.at("reported to fall")
        self.play(GrowArrow(fall), run_time=1.3)
        nA = nuc_c(XA, B_L, 0.5)[0]
        nB = nuc_c(XB, B_L, 0.5)[0]
        nA.set_z_index(3)
        nB.set_z_index(3)
        halos = []
        for nn in (nA, nB):
            hh = Circle(radius=0.95, stroke_width=0, fill_color=PINK, fill_opacity=0.9 * sig(B_L)).move_to(nn.get_center()).set_z_index(2)
            hh.add_updater(lambda m, nn=nn: m.move_to(nn.get_center()).set_fill("#FFC2DD", opacity=min(1.0, 1.1 * sig(nn.get_center()[1]))).set_stroke("#FFE3F0", width=16 * sig(nn.get_center()[1]), opacity=1))
            halos.append(hh)
        self.at("So how far")
        self.play(FadeIn(nA), FadeIn(nB), FadeIn(halos[0]), FadeIn(halos[1]), run_time=0.6)
        self.at("nucleus travels")
        self.play(nA.animate.move_to([XA, -0.5, 0]), nB.animate.move_to([XB, 2.2, 0]), run_time=1.4)
        tA = tb("short trip", 28, TEXT).move_to([XA, -1.5, 0])
        tB = tb("long trip", 28, TEXT).move_to([XB, 1.2, 0])
        self.at("the signal it meets")
        self.play(FadeIn(tA), FadeIn(tB), Indicate(halos[0], color=PINK, scale_factor=1.15), Indicate(halos[1], color=PINK, scale_factor=1.15),
                  run_time=1.0)
        self.finish()


class S25Payoff(SpokenScene):
    def construct(self):
        v = vent()
        head = T("The payoff", 46, TEXT, font=TITLE_FONT).move_to([0, 3.2, 0])
        sx = -5.0
        shaft = RoundedRectangle(corner_radius=0.4, width=1.2, height=5.4, stroke_color=BLUE, stroke_width=3.5,
                                 fill_color=BLUE, fill_opacity=0.12).move_to([sx, -0.45, 0])
        nuc = nuc_c(sx, -2.7, 0.35)
        self.add(v, shaft, nuc)
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.7)
        al = left(T("apical radial glia", 36, BLUE), -4.1, 1.2)
        self.at("apical radial glia")
        self.play(FadeIn(al), Indicate(shaft, color=BLUE, scale_factor=1.0), run_time=0.8)
        pair = dumb(sx, -2.65, r=0.22, dx=0.3)
        dl = left(T("divides at the surface", 32, TEAL), -4.1, -2.5)
        self.at("divide at the surface")
        self.play(ReplacementTransform(nuc, pair), FadeIn(dl), run_time=0.8)
        c1 = chip("where a cell divides", TEXT, size=36).move_to([2.7, 0.9, 0])
        self.at("So where a cell divides")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        c2 = chip("a first clue to its kind", GOLD, size=36).move_to([2.7, -0.7, 0])
        ar = arr([2.7, 0.3, 0], [2.7, -0.1, 0], GOLD, w=6)
        self.at("a first clue")
        self.play(GrowArrow(ar), FadeIn(c2), run_time=0.8)
        self.finish()


def mitotic(x, y, dashed=False, r=0.5):
    if dashed:
        c = DashedVMobject(Circle(radius=r, stroke_color=BLUE, stroke_width=3.5), num_dashes=18).move_to([x, y, 0])
        back = Circle(radius=r, stroke_width=0, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
        tint = Circle(radius=r, stroke_width=0, fill_color=BLUE, fill_opacity=0.12).move_to([x, y, 0])
        body = VGroup(back, tint, c)
    else:
        body = Circle(radius=r, stroke_color=BLUE, stroke_width=3.5, fill_color=BLUE, fill_opacity=0.2).move_to([x, y, 0])
    g = VGroup(body, dumb(x, y, r=0.18, dx=0.22))
    g.set_z_index(5)
    return g


def fibre(x, y0, y1=2.95):
    return Line([x, y0, 0], [x, y1, 0], color=BLUE, stroke_width=3.5, stroke_opacity=0.7).set_z_index(1)


class S26Away(SpokenScene):
    def construct(self):
        v = vent(label=False)
        YS = -2.5
        band_v = Rectangle(width=13.2, height=2.25, stroke_width=0, fill_color=GREY, fill_opacity=0.09).move_to([0, -2.025, 0])
        band_v.set_z_index(-1)
        edge = DashedLine([-6.6, -0.9, 0], [6.6, -0.9, 0], color=GREY, stroke_width=2.5, dash_length=0.16)
        lab_v = right_at(T("at the ventricle", 28, GREY), 6.5, -1.3)
        self.add(v, band_v)
        xs = [-5.2, -4.1, -3.0, -1.9]
        ar = [mitotic(x, YS) for x in xs]
        fibs = [fibre(x, YS + 0.55) for x in xs]
        self.at("Most mitoses at the ventricle")
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in ar], lag_ratio=0.2), *[Create(f) for f in fibs], FadeIn(lab_v), run_time=1.4)
        bl = left(T("mostly apical radial glia", 30, BLUE), -1.2, -1.45)
        bld = Line([-1.25, -1.5, 0], [-1.75, -2.0, 0], color=BLUE, stroke_width=2.5)
        self.at("apical radial glia")
        self.play(FadeIn(bl, shift=UP * 0.1), Create(bld), run_time=0.7)
        ip1 = mitotic(-0.6, YS, dashed=True)
        il = left(T("intermediate\nprogenitor", 28, TEXT, line_spacing=0.85), 0.3, YS)
        self.at("some intermediate progenitors")
        self.play(FadeIn(ip1, scale=0.6), FadeIn(il), run_time=0.8)
        self.at("divide there")
        self.play(Indicate(ip1, color=BLUE, scale_factor=1.15), run_time=0.7)
        away = right_at(T("away from the ventricle", 28, GREY), 6.5, -0.65)
        self.at("Mitoses away from it")
        self.play(Create(edge), FadeIn(away), run_time=0.7)
        ips = [mitotic(x, y, dashed=True) for x, y in ((0.5, 0.9), (2.0, 1.7), (3.3, 0.6))]
        il2 = T("mostly intermediate progenitors", 28, TEXT).move_to([1.8, 2.65, 0])
        self.at("mostly intermediate progenitors")
        self.play(*[FadeIn(m, scale=0.6) for m in ips], FadeIn(il2), run_time=0.9)
        fib = fibre(5.5, 2.05)
        org = mitotic(5.5, 1.5)
        ol = T("outer radial\nglia", 28, BLUE, line_spacing=0.85).move_to([5.5, 0.55, 0])
        self.at("outer radial glia")
        self.play(FadeIn(org, scale=0.6), Create(fib), FadeIn(ol), run_time=0.9)
        self.finish()


class S27Take(SpokenScene):
    def construct(self):
        def row(y, a, ca, b, cb, size=36):
            left_chip = chip(a, ca, size=size)
            left_chip.move_to([-6.4 + left_chip.width / 2, y, 0])
            x1 = -6.4 + left_chip.width
            ar = arr([x1 + 0.1, y, 0], [x1 + 0.7, y, 0], GREY, w=5, tip=0.2)
            rt = left(T(b, size, cb), x1 + 0.85, y)
            return VGroup(left_chip, ar, rt)
        r1 = row(2.9, "where it divides", TEXT, "a first clue", GOLD, 46)
        r2 = row(0.4, "shape and markers", BLUE, "name the cell", BLUE, 46)
        r3 = row(-2.3, "lineage", TEAL, "what its daughters become", TEAL, 46)
        left(r3[2], r3[1].get_right()[0] + 0.15, -2.3)
        self.add(r1)
        self.at("To name the cell")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.8)
        self.at("To learn what")
        self.play(FadeIn(r3[2], shift=UP * 0.1), run_time=0.7)
        self.at("you need")
        self.play(FadeIn(r3[0]), FadeIn(r3[1]), run_time=0.6)
        root = Dot([5.3, 1.2, 0], radius=0.17, color=BLUE)
        kids = [Dot([4.4, -0.6, 0], radius=0.15, color=BLUE), Dot([6.2, -0.6, 0], radius=0.15, color=BLUE)]
        grand = [Dot([x, -2.4, 0], radius=0.13, color=BLUE) for x in (3.9, 4.8, 5.7, 6.6)]
        lines = [Line(root.get_center(), k.get_center(), color=BLUE, stroke_width=4) for k in kids]
        lines += [Line(kids[i // 2].get_center(), g.get_center(), color=BLUE, stroke_width=4) for i, g in enumerate(grand)]
        tl = T("descendants of\none cell", 26, TEAL, line_spacing=0.85).move_to([5.25, -3.3, 0])
        self.at("the descendants of one cell")
        self.play(FadeIn(root), Create(VGroup(*lines)), FadeIn(VGroup(*kids)), FadeIn(VGroup(*grand)), FadeIn(tl), run_time=1.2)
        self.finish()


class S28End(EndCard):
    LINE = "To name the cell, add its shape and markers; daughters need lineage."
