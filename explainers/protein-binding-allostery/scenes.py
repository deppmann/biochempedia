"""The Delivery Problem  (Biochemistrypedia: Protein binding & allostery, chapter 1)

COLOR MAP (one color per concept, whole series; taken from scenes.old.py)
  BLUE   = hemoglobin / protein, and the T (tense, weak-grip) shape
  GREEN  = the R (relaxed, tight-grip) shape; a check mark
  YELLOW = O2, the ligand, and how full a site is
  RED    = a cross (not delivered); carbon monoxide in the last chapter
  TEAL   = 2,3-BPG (later chapters)
  GOLD   = call-outs, cooperativity, loading/unloading labels
  TEXT   = neutral labels;  GREY = axes, secondary labels
  Added here: PURPLE (MB) = myoglobin and the generic "tight binder"; HEME = the heme chip;
  CELL/LUNGC/MUSC = the red blood cell, lung and muscle pictures.
Curves are computed: hemoglobin Y = x^n/(P50^n + x^n) with P50 = 26.4 torr, n = 2.8;
myoglobin Y = x/(2 + x); the T/R mix from the two-state (MWC) model, L = 1000, c = 0.01, KR = 5 torr.
NO molecular structures are drawn: blocks, chips, bars and curves only.
"""
import numpy as np

from bp_style import *

# ------------------------------------------------------------------ colours and numbers
MB = "#B48EDE"
HEME = "#E8935A"
CELL = "#E5566A"
LUNGC = "#E58FB0"
MUSC = "#C9754F"

P50, NH = 26.4, 2.8
MB_P50 = 2.0
KR, LL, CC = 5.0, 1000.0, 0.01


def hill(x, p50=P50, n=NH):
    return x ** n / (p50 ** n + x ** n)


def mwc(p):
    """Two-state model: (fraction of molecules in R, fullness of an R site, of a T site, overall)."""
    a = p / KR
    r = (1 + a) ** 4
    t = LL * (1 + CC * a) ** 4
    rb = r / (r + t)
    yr, yt = a / (1 + a), CC * a / (1 + CC * a)
    return rb, yr, yt, rb * yr + (1 - rb) * yt


P_MIX = 15.0          # torr: the mix shown in scenes 15 to 18 (about 81 % T, 19 % R)
P_END = 40.0          # torr: after oxygen shifts the mix (about 17 % T, 83 % R)

F_MB = hill(100, MB_P50, 1) - hill(20, MB_P50, 1)       # about 0.07
F_HB = hill(100) - hill(20)                              # about 0.66
F_RS = hill(100) - hill(40)                              # about 0.21


# ------------------------------------------------------------------ small pieces
def o2(r=0.27, size=22):
    c = Circle(radius=r, color=YELLOW, fill_opacity=1, stroke_width=0)
    return VGroup(c, T("O₂", size, BG, weight=BOLD).move_to(c))


def check(c=GREEN, s=0.45):
    return VMobject(stroke_color=c, stroke_width=12).set_points_as_corners(
        [LEFT * s + UP * 0.02, LEFT * s * 0.3 + DOWN * s * 0.6, RIGHT * s + UP * s * 0.8])


def cross(c=RED, s=0.4):
    return VGroup(Line(UL * s, DR * s, color=c, stroke_width=12), Line(UR * s, DL * s, color=c, stroke_width=12))


def cell_pic(r=0.62):
    c = Circle(radius=r, stroke_color=CELL, stroke_width=3, fill_color=CELL, fill_opacity=0.6)
    d = Circle(radius=r * 0.42, stroke_width=0, fill_color=BG, fill_opacity=0.35)
    return VGroup(c, d).set_z_index(3)


def surface_dots(center, r, dot_r=0.22):
    """Four O2 dots sitting on the rim of a red cell."""
    out = VGroup()
    for k in range(4):
        ang = PI / 4 + k * PI / 2
        out.add(o2(dot_r, 20).move_to(center + np.array([np.cos(ang), np.sin(ang), 0]) * r).set_z_index(5))
    return out


# ------------------------------------------------------------------ the big lung-to-muscle stage (s01, s05, s08)
LX, MX, SY, SS = -3.95, 4.15, -0.7, 1.3


def lung_pic(center=(LX, SY), s=SS, label=True):
    sh = VGroup()
    for dx in (-1.0, 1.0):
        sh.add(Ellipse(width=1.95, height=3.0, stroke_color=LUNGC, stroke_width=3,
                       fill_color=LUNGC, fill_opacity=0.25).shift(RIGHT * dx))
    sh.add(Line(UP * 1.85, UP * 0.8, color=LUNGC, stroke_width=5))
    sh.add(Line(UP * 0.8, LEFT * 0.9 + UP * 0.3, color=LUNGC, stroke_width=4))
    sh.add(Line(UP * 0.8, RIGHT * 0.9 + UP * 0.3, color=LUNGC, stroke_width=4))
    sh.scale(s).move_to([center[0], center[1] + 0.2 * s, 0])
    g = VGroup(sh)
    if label:
        g.add(T("lungs", 32, LUNGC).move_to([center[0], center[1] - 1.95 * s - 0.15, 0]))
    return g.set_z_index(0)


def muscle_pic(center=(MX, SY), w=3.7, h=3.0, s=SS, label=True):
    r = RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=MUSC, stroke_width=3,
                         fill_color=MUSC, fill_opacity=0.25)
    fib = VGroup(*[Line(LEFT * (w / 2 - 0.2), RIGHT * (w / 2 - 0.2), color=MUSC, stroke_width=2).set_opacity(0.45)
                   .shift(UP * y) for y in np.linspace(-h / 2 + 0.5, h / 2 - 0.5, 4)])
    pic = VGroup(r, fib).scale(s).move_to([center[0], center[1], 0])
    g = VGroup(pic)
    if label:
        g.add(T("muscle", 32, MUSC).move_to([center[0], center[1] - h / 2 * s - 0.6, 0]))
    return g.set_z_index(0)


# ---- a population of 16 tight-binding carriers (s05, s08), with a legend on first use
def tray(color=MB, u=0.5, gap=0.08, cols=4, n=16):
    boxes, dots = VGroup(), VGroup()
    rows = n // cols
    for i in range(n):
        r, c = divmod(i, cols)
        x, y = (c - (cols - 1) / 2) * (u + gap), ((rows - 1) / 2 - r) * (u + gap)
        boxes.add(RoundedRectangle(corner_radius=0.08, width=u, height=u, stroke_color=color, stroke_width=2.5,
                                   fill_color=interpolate_color(ManimColor(BG), ManimColor(color), 0.25),
                                   fill_opacity=1).move_to([x, y, 0]))
        dots.add(Circle(radius=u * 0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=1).move_to([x, y, 0]))
    pad = u * 0.35
    back = RoundedRectangle(corner_radius=0.15, width=cols * (u + gap) + pad, height=rows * (u + gap) + pad,
                            stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=0.92).set_z_index(2)
    boxes.add(back)
    return boxes.set_z_index(3), dots.set_z_index(4)


def legend():
    box = RoundedRectangle(corner_radius=0.06, width=0.42, height=0.42, stroke_color=MB, stroke_width=2.5,
                           fill_color=interpolate_color(ManimColor(BG), ManimColor(MB), 0.25), fill_opacity=1)
    dot = Circle(radius=0.14, stroke_width=0, fill_color=YELLOW, fill_opacity=1)
    a = VGroup(box, T("= one carrier (16 carriers shown)", 28)).arrange(RIGHT, buff=0.18)
    b = VGroup(dot, T("= carrying O₂", 28)).arrange(RIGHT, buff=0.18)
    return VGroup(a, b).arrange(RIGHT, buff=0.7).move_to([0, 3.35, 0])


def chips_jobs(y=2.5):
    return chip("LOAD", GOLD, 34).move_to([LX, y, 0]), chip("UNLOAD", GOLD, 34).move_to([MX, y, 0])


# ------------------------------------------------------------------ the three pressure panels (s02 to s04)
COLX = [-4.55, 0.0, 4.55]
PANEL_OFF = 0.24
PIC_X, PIC_Y = -0.55, 0.3
LUNG_DOTS = [(sx * 0.64, y) for y in (1.15, 0.58, 0.0, -0.58, -1.15) for sx in (-1, 1)]
TIS_DOTS = [(0.75, 0.85), (-0.75, -0.85), (-0.75, 0.85), (0.75, -0.85)]


def panel(kind, name, torr, ndots):
    """One panel built around the origin: picture, cell, free O2, a 0-100 torr gauge and the reading."""
    pc = np.array([PIC_X, PIC_Y, 0])
    if kind == "lung":
        pic = VGroup()
        for dx in (-0.64, 0.64):
            pic.add(Ellipse(width=1.25, height=3.0, stroke_color=LUNGC, stroke_width=3, fill_color=LUNGC,
                            fill_opacity=0.25).move_to(pc + RIGHT * dx))
        pic.add(Line(pc + UP * 1.95, pc + UP * 1.2, color=LUNGC, stroke_width=5))
        pic.add(Line(pc + UP * 1.2, pc + UP * 0.85 + LEFT * 0.6, color=LUNGC, stroke_width=4))
        pic.add(Line(pc + UP * 1.2, pc + UP * 0.85 + RIGHT * 0.6, color=LUNGC, stroke_width=4))
        col, pos = LUNGC, LUNG_DOTS
    else:
        r = RoundedRectangle(corner_radius=0.25, width=2.5, height=3.0, stroke_color=MUSC, stroke_width=3,
                             fill_color=MUSC, fill_opacity=0.25 if kind == "muscle" else 0.14).move_to(pc)
        pic = VGroup(r)
        if kind == "muscle":
            pic.add(*[Line(pc + LEFT * 1.05 + UP * y, pc + RIGHT * 1.05 + UP * y, color=MUSC, stroke_width=2)
                    .set_opacity(0.45) for y in (-0.9, -0.3, 0.3, 0.9)])
        col, pos = MUSC, TIS_DOTS
    cell = cell_pic(0.38).move_to(pc)
    dots = VGroup(*[o2(0.2, 18).move_to(pc + np.array([dx, dy, 0])).set_z_index(5) for dx, dy in pos[:ndots]])
    head = T(name, 30, col).move_to([0.15, 3.25, 0])
    gx, gy, gh = 1.35, 0.3, 3.4
    fr = Rectangle(width=0.45, height=gh, stroke_color=GREY, stroke_width=3).move_to([gx, gy, 0])
    ticks = VGroup()
    for v in (0, 50, 100):
        y = gy - gh / 2 + gh * v / 100
        ticks.add(Line([gx + 0.225, y, 0], [gx + 0.38, y, 0], color=GREY, stroke_width=3))
        if v != 50:
            ticks.add(M(str(v), 26, GREY).next_to([gx + 0.38, y, 0], RIGHT, buff=0.08))
    gl = M("pO₂", 26, GREY).move_to([gx - 0.05, 2.5, 0])
    fill = Rectangle(width=0.45, height=max(gh * torr / 100, 0.01), stroke_width=0, fill_color=YELLOW,
                     fill_opacity=0.95).align_to(fr, DOWN).set_x(gx)
    read = VGroup(M(str(torr), 46, YELLOW), M("torr", 28, GREY)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
    read.move_to([0.15, -2.2, 0])
    return dict(pic=pic, cell=cell, dots=dots, head=head, gauge=VGroup(fr, ticks, gl), fill=fill, read=read)


def place(p, cx, s=1.0, cy=0.0):
    for v in p.values():
        v.scale(s, about_point=ORIGIN).shift(RIGHT * (cx - PANEL_OFF * s) + UP * cy)
    return p


def pgroup(p):
    return VGroup(p["pic"], p["cell"], p["dots"], p["head"], p["gauge"], p["fill"], p["read"])


PANELS = [("lung", "lungs", 100, 10), ("tissue", "resting tissue", 40, 4), ("muscle", "hard-working muscle", 20, 2)]


# ------------------------------------------------------------------ bar chart (s09 to s12)
AX0, AX1 = -5.0, 6.3
BASE, CH = -2.15, 5.0
BX = [-2.9, 0.7, 4.3]
BW = 1.8
BAR_INFO = [("myoglobin", MB), ("hemoglobin", BLUE), ("hemoglobin", BLUE)]
BAR_P = [(100, 20, "lungs → hard work"), (100, 20, "lungs → hard work"), (100, 40, "lungs → rest")]


def chart_frame():
    g = VGroup()
    g.add(Line([AX0, BASE, 0], [AX1, BASE, 0], color=GREY, stroke_width=3))
    g.add(Line([AX0, BASE, 0], [AX0, BASE + CH, 0], color=GREY, stroke_width=3))
    for v in (0, 50, 100):
        y = BASE + CH * v / 100
        g.add(M(f"{v}%", 26, GREY).next_to([AX0 - 0.05, y, 0], LEFT, buff=0.1))
        if v:
            g.add(Line([AX0, y, 0], [AX1, y, 0], color=GREY, stroke_width=1.2).set_opacity(0.4))
    g.add(T("oxygen delivered (share of the load given up)", 32, TEXT).move_to([0.65, 3.42, 0]))
    return g


def bar_labels(i, p_lo=None, ctx=None):
    nm, col = BAR_INFO[i]
    hi, lo, c = BAR_P[i]
    lo = lo if p_lo is None else p_lo
    c = c if ctx is None else ctx
    g = VGroup(T(nm, 28, col), M(f"{hi} → {lo:.0f} torr", 26, TEXT), T(c, 26, GREY)).arrange(DOWN, buff=0.06)
    return g.move_to([BX[i], BASE - 0.14 - g.height / 2, 0])


def bar_rect(i, frac):
    col = BAR_INFO[i][1]
    h = max(frac * CH, 0.015)
    return Rectangle(width=BW, height=h, stroke_width=0, fill_color=col, fill_opacity=0.88).move_to([BX[i], BASE + h / 2, 0])


def bar_value(i, frac):
    h = max(frac * CH, 0.015)
    lab = M(f"{round(frac * 100)}%", 38, TEXT)
    if i == 2:
        return lab.move_to([BX[i] + BW / 2 + 0.2 + lab.width / 2, BASE + h - 0.25, 0])
    return lab.move_to([BX[i], BASE + h + 0.35, 0])


def aboard_box():
    """The part of the resting bar's load that stays aboard (s11, s12)."""
    top, bot = BASE + CH, BASE + F_RS * CH
    r = DashedVMobject(Rectangle(width=BW, height=top - bot, stroke_color=GOLD, stroke_width=3), num_dashes=40)
    r.move_to([BX[2], (top + bot) / 2, 0])
    txt = VGroup(T("still", 28, GOLD), T("aboard", 28, GOLD), M(f"{round((1 - F_RS) * 100)}%", 34, GOLD)).arrange(DOWN, buff=0.1)
    txt.move_to(r)
    return r, txt


# ------------------------------------------------------------------ hemoglobin cartoons
def hb4(color, size=1.4, gap=0.08, op=0.2):
    """Four blocks in a square: a cartoon, not a structure."""
    dd = (size + gap) / 2
    g = VGroup()
    for x, y in [(-dd, dd), (dd, dd), (-dd, -dd), (dd, -dd)]:
        g.add(RoundedRectangle(corner_radius=0.14, width=size, height=size, stroke_color=color, stroke_width=3,
                               fill_color=color, fill_opacity=op).move_to([x, y, 0]))
    return g


def shapeT(cx, cy, s=1.35):
    """T: four blocks packed tight together."""
    return hb4(BLUE, s, 0.08, 0.22).move_to([cx, cy, 0])


def shapeR(cx, cy, s=1.35):
    """R: the same four blocks, loosened and turned (more open)."""
    g = hb4(GREEN, s, 0.5 * s / 1.35, 0.32)
    for k, b in enumerate(g):
        b.rotate((1 if k in (0, 3) else -1) * 0.22)
    return g.move_to([cx, cy, 0])


def heme_chip():
    return chip("heme", HEME, 26, pad=0.12)


def fe_badge():
    c = Circle(radius=0.27, stroke_width=0, fill_color=TEXT, fill_opacity=1)
    return VGroup(c, T("Fe", 22, BG, weight=BOLD).move_to(c))


def mb_pic(cx=-3.9, cy=0.25, s=3.0):
    blk = RoundedRectangle(corner_radius=0.2, width=s, height=s, stroke_color=MB, stroke_width=3,
                           fill_color=MB, fill_opacity=0.22).move_to([cx, cy, 0])
    return blk, heme_chip().move_to(blk.get_center())


def hb_pic(cx=3.6, cy=0.25, s=1.85):
    blks = hb4(BLUE, s, 0.12).move_to([cx, cy, 0])
    return blks, VGroup(*[heme_chip().move_to(b.get_center()) for b in blks])


def popbar(fr, cx, cy, w, h, size=30):
    """T (blue) on the left, R (green) on the right, R share = fr, with percent labels."""
    g = VGroup()
    wt, wr = w * (1 - fr), w * fr
    left = cx - w / 2
    pt = round((1 - fr) * 100)
    for wd, x0, col, nm, pc in [(wt, left, BLUE, "T", pt), (wr, left + wt, GREEN, "R", 100 - pt)]:
        if wd > 0.01:
            g.add(Rectangle(width=wd, height=h, stroke_width=0, fill_color=col, fill_opacity=0.95)
                  .move_to([x0 + wd / 2, cy, 0]))
            lab = T(f"{nm} {pc}%", size, BG, weight=BOLD)
            if lab.width < wd - 0.15:
                g.add(lab.move_to([x0 + wd / 2, cy, 0]))
            else:
                g.add(T(f"{nm} {pc}%", 28, col, weight=BOLD).next_to([x0 + wd / 2, cy - h / 2, 0], DOWN, buff=0.15))
    return g


def mk_axes(w, h, center, xt, yt=((0, "0"), (0.5, "0.5"), (1, "1")), xmax=110):
    ax = Axes(x_range=[0, xmax, xmax], y_range=[0, 1, 1], x_length=w, y_length=h, tips=False,
              axis_config={"include_numbers": False, "include_ticks": False, "color": GREY, "stroke_width": 3})
    ax.move_to(center)
    deco = VGroup()
    for v, lab, sub, col in xt:
        deco.add(Line(ax.c2p(v, 0), ax.c2p(v, 0) + DOWN * 0.12, color=GREY, stroke_width=3))
        t = M(lab, 26, GREY).next_to(ax.c2p(v, 0), DOWN, buff=0.18)
        deco.add(t)
        if sub:
            deco.add(T(sub, 26, col).next_to(t, DOWN, buff=0.06))
    for v, lab in yt:
        deco.add(Line(ax.c2p(0, v), ax.c2p(0, v) + LEFT * 0.12, color=GREY, stroke_width=3))
        deco.add(M(lab, 26, GREY).next_to(ax.c2p(0, v), LEFT, buff=0.2))
    return ax, deco


class Sc(SpokenScene):
    pass


# ---------------------------------------------------------------- cards
class S00Title(TitleCard):
    LESSON = "Protein Binding and Allostery: How Hemoglobin Loads and Delivers Oxygen"
    TITLE = "The Delivery Problem"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=22, color=TEAL, weight=BOLD).set_opacity(0.9)
        les = VGroup(T("PROTEIN BINDING AND ALLOSTERY:", 26, GREY),
                     T("HOW HEMOGLOBIN LOADS AND DELIVERS OXYGEN", 26, GREY)).arrange(DOWN, buff=0.14)
        title = T(self.TITLE, size=72, font=TITLE_FONT)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        g = VGroup(brand, les, title, rule).arrange(DOWN, buff=0.4)
        g[2].shift(DOWN * 0.25)
        g[3].shift(DOWN * 0.25)
        g.move_to(ORIGIN)
        self.play(FadeIn(brand, shift=UP * 0.1), FadeIn(les, shift=UP * 0.1), run_time=self.beat(0.2))
        self.play(FadeIn(title, shift=UP * 0.15), GrowFromCenter(rule), run_time=self.beat(0.25))
        self.wait(self.beat(0.35))
        self.play(FadeOut(g), run_time=self.beat(0.15))
        self.finish()


class S20End(EndCard):
    LINE = "Two shapes, weak and tight, and oxygen shifts the mix between them."

    def construct(self):
        line = VGroup(T("Two shapes, weak and tight,", 66, font=TITLE_FONT),
                      T("and oxygen shifts the mix between them.", 66, font=TITLE_FONT)).arrange(DOWN, buff=0.35)
        fit(line, max_w=12.4)
        sub = T("biochemistrypedia.com", size=28, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.7).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.25))
        self.play(FadeIn(sub), run_time=self.beat(0.12))
        self.finish()


# ---------------------------------------------------------------- 1: the question
class S01Q(Sc):
    def construct(self):
        L1, M1, Y1, S1 = -3.7, 3.9, -0.45, 1.5
        lung, mus = lung_pic((L1, Y1), S1), muscle_pic((M1, Y1), 3.4, 3.0, S1)
        q = VGroup(T("How can one protein", 46), T("grab oxygen and let it go?", 46, YELLOW)).arrange(DOWN, buff=0.15)
        q.move_to([0, 3.25, 0])
        lc = np.array([L1, Y1 + 0.1, 0])
        cell = cell_pic(0.9).move_to(lc)
        free = VGroup(*[o2(0.32).move_to(lc + np.array([dx, dy, 0])).set_z_index(5)
                        for dx, dy in [(-1.5, 1.1), (1.5, 1.1), (-1.5, -1.3), (1.5, -1.3)]])
        self.at("your blood")
        self.play(FadeIn(q, shift=DOWN * 0.15), FadeIn(lung), FadeIn(mus), FadeIn(cell, scale=0.6), run_time=0.8)
        self.at("grab oxygen")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in free], lag_ratio=0.1), run_time=0.5)
        on = surface_dots(lc, 0.9, 0.32)
        self.play(*[Transform(a, b) for a, b in zip(free, on)], run_time=0.6)
        self.at("let it go")
        grp = VGroup(cell, free)
        mc = np.array([M1, Y1 + 0.1, 0])
        self.play(grp.animate.move_to(mc), run_time=0.8)
        self.at("working muscle")
        tgt = [mc + np.array([dx, dy, 0]) for dx, dy in [(-1.8, 1.3), (1.8, 1.3), (-1.8, -1.3), (1.8, -1.3)]]
        self.play(*[d.animate.move_to(t) for d, t in zip(free, tgt)], run_time=0.8)
        self.at("how can one protein")
        self.play(Indicate(q, color=YELLOW, scale_factor=1.06), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------- 2: the lungs
class S02Lungs(Sc):
    def construct(self):
        p = place(panel(*PANELS[0]), 0.0, 1.1, -0.2)
        self.play(FadeIn(p["pic"]), FadeIn(p["head"]), FadeIn(p["cell"], scale=0.6), run_time=0.5)
        self.at("the oxygen pressure")
        fill = p["fill"]
        self.play(Create(p["gauge"]), FadeIn(p["read"]), GrowFromEdge(fill, DOWN), run_time=0.9)
        self.at("oxygen is plentiful")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in p["dots"]], lag_ratio=0.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------- 3: three pressures
class S03Tissue(Sc):
    def construct(self):
        big = place(panel(*PANELS[0]), 0.0, 1.1, -0.2)
        g = pgroup(big)
        self.add(g)
        tgt = pgroup(place(panel(*PANELS[0]), COLX[0]))
        self.play(Transform(g, tgt), run_time=0.55)
        for i, (c1, c2) in ((1, ("resting tissue", "near 40")), (2, ("hard", "near 20"))):
            p = place(panel(*PANELS[i]), COLX[i])
            self.at(c1)
            self.play(FadeIn(p["head"]), FadeIn(p["pic"]), FadeIn(p["cell"], scale=0.6), Create(p["gauge"]), run_time=0.6)
            self.at(c2)
            self.play(GrowFromEdge(p["fill"], DOWN), FadeIn(p["read"]),
                      LaggedStart(*[FadeIn(d, scale=0.4) for d in p["dots"]], lag_ratio=0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- 4: two jobs
class S04Jobs(Sc):
    def construct(self):
        ps = [place(panel(*PANELS[i]), COLX[i]) for i in range(3)]
        for p in ps:
            self.add(pgroup(p))
        ld = chip("LOAD", GOLD, 34).move_to([COLX[0] - 0.1, -3.25, 0])
        ul = chip("UNLOAD", GOLD, 34).move_to([COLX[2] - 0.1, -3.25, 0])
        route = Arrow([ld.get_right()[0] + 0.15, -3.25, 0], [ul.get_left()[0] - 0.15, -3.25, 0], color=GREY,
                      stroke_width=5, buff=0, max_tip_length_to_length_ratio=0.05)
        self.at("two opposite jobs")
        self.play(pgroup(ps[1]).animate.set_opacity(0.22), GrowArrow(route), run_time=0.9)
        self.at("load oxygen")
        lc = ps[0]["cell"].get_center()
        on = surface_dots(lc, 0.38, 0.17)
        self.play(FadeIn(ld, shift=UP * 0.2), *[ReplacementTransform(d, o) for d, o in zip(ps[0]["dots"][2:6], on)],
                  run_time=0.9)
        car = VGroup(cell_pic(0.38).move_to(lc), on)
        self.add(car)
        self.at("unload it")
        mc = ps[2]["cell"].get_center()
        self.play(FadeIn(ul, shift=UP * 0.2), car.animate.move_to(mc), run_time=0.9)
        out = [mc + np.array([dx, dy, 0]) for dx, dy in [(-0.75, 0.85), (0.75, -0.85), (0.0, 1.2), (0.0, -1.2)]]
        self.play(*[d.animate.move_to(t) for d, t in zip(on, out)], run_time=0.7)
        self.finish()


TRAY_C, TRAY_LAB = [LX, SY - 0.45, 0], [LX, 1.2, 0]


# ---------------------------------------------------------------- 5: tight binder
class S05Tight(Sc):
    def construct(self):
        lung, mus = lung_pic(), muscle_pic()
        ld, ul = chips_jobs()
        self.add(lung, mus, ld, ul)
        lg = legend()
        b, d = tray()
        VGroup(b, d).scale(1.4).move_to(TRAY_C)
        self.at("a protein")
        self.play(FadeIn(b, scale=0.7), FadeIn(lg, shift=DOWN * 0.15), run_time=0.7)
        self.at("binds tightly")
        self.play(LaggedStart(*[FadeIn(x, scale=2.5) for x in d], lag_ratio=0.04), run_time=0.8)
        self.at("good at the first job")
        ck = check().next_to(ld, RIGHT, buff=0.3)
        self.play(Create(ck), Indicate(ld, color=GREEN, scale_factor=1.1), run_time=0.6)
        self.at("bad at the second")
        qm = T("?", 120, GOLD, weight=BOLD).move_to([MX, SY + 0.1, 0]).set_z_index(5)
        self.play(FadeIn(qm, scale=0.5), Indicate(ul, color=GOLD, scale_factor=1.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- 6 and 7: the question
def predict_frame():
    tag = chip("PREDICT", GOLD, 34).move_to([0, 2.5, 0])
    q = VGroup(T("Would a tighter binder", 62), T("be a better carrier?", 62)).arrange(DOWN, buff=0.25).move_to([0, 0.45, 0])
    return tag, q


class S06Predict(Sc):
    def construct(self):
        tag, q = predict_frame()
        self.at("predict")
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.5)
        self.at("would a protein")
        self.play(FadeIn(q[0], shift=UP * 0.1), run_time=0.5)
        self.at("make a better")
        self.play(FadeIn(q[1], shift=UP * 0.1), run_time=0.5)
        self.finish()


class S07Pause(Sc):
    def construct(self):
        tag, q = predict_frame()
        self.add(tag, q)
        k = ValueTracker(1.0)
        cen = np.array([-2.3, -2.3, 0])
        base = Circle(radius=0.55, stroke_color=GREY, stroke_width=6, stroke_opacity=0.35, fill_opacity=0).move_to(cen)
        ring = always_redraw(lambda: Arc(radius=0.55, start_angle=PI / 2, angle=max(k.get_value(), 0.001) * TAU,
                                         arc_center=cen, color=GOLD, stroke_width=10))
        txt = T("pause and decide", 38, GOLD).next_to(base, RIGHT, buff=0.45)
        self.add(base, ring, txt)
        self.play(k.animate.set_value(0.0), run_time=4.7, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------- 8: the answer
BIGM = (2.9, -0.6)


class S08Reveal(Sc):
    def construct(self):
        lung, mus = lung_pic(), muscle_pic()
        lg = legend()
        self.add(lg)
        self.play(FadeIn(lung), FadeIn(mus), run_time=0.5)
        b, d = tray()
        VGroup(b, d).scale(1.4).move_to(TRAY_C)
        self.at("a tight binder")
        self.play(FadeIn(b, scale=0.7), run_time=0.5)
        self.at("fills in the lungs")
        self.play(LaggedStart(*[FadeIn(x, scale=2.5) for x in d], lag_ratio=0.04), run_time=0.7)
        self.at("but it stays")
        big = muscle_pic(BIGM, 6.4, 4.9, 1.0, label=False)
        mlab = T("muscle", 34, MUSC).move_to([BIGM[0], 2.35, 0])
        grid = VGroup(b, d)
        self.play(FadeOut(lung), ReplacementTransform(mus[0], big[0]), ReplacementTransform(mus[1], mlab),
                  grid.animate.scale(1.6 / 1.4).move_to([BIGM[0], BIGM[1], 0]), run_time=1.2)
        self.at("in the muscle")
        lost = d[6]
        self.play(lost.animate.shift(DOWN * 2.0 + RIGHT * 2.2).set_opacity(0), run_time=0.8)
        self.at("oxygen that stays")
        l1 = VGroup(T("still aboard:", 38, GOLD), T("15 of 16 carriers", 38, GOLD)).arrange(DOWN, buff=0.12).move_to([-3.9, 0.55, 0])
        br = SurroundingRectangle(grid, color=GOLD, buff=0.15, corner_radius=0.15, stroke_width=4)
        arr = Arrow(l1.get_right() + RIGHT * 0.1, br.get_left() + LEFT * 0.05 + UP * 0.0, color=GOLD, stroke_width=5, buff=0.05)
        arr.put_start_and_end_on(l1.get_right() + RIGHT * 0.15, [br.get_left()[0] - 0.05, l1.get_y(), 0])
        self.play(FadeIn(l1, shift=RIGHT * 0.15), Create(br), GrowArrow(arr), run_time=0.8)
        self.at("not delivered")
        l2 = T("= not delivered", 42, RED).move_to([-3.9, -0.9, 0])
        xx = cross().next_to(l2, DOWN, buff=0.35)
        self.play(FadeIn(l2, shift=RIGHT * 0.15), Create(xx), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------- 9 to 12: the bar chart
class S09Mb(Sc):
    def construct(self):
        frame = chart_frame()
        self.add(frame)
        bl = bar_labels(0)
        self.at("myoglobin")
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=0.6)
        self.at("storage protein")
        sub = T("muscle's storage protein", 28, MB).move_to([-2.6, 0.9, 0])
        self.play(FadeIn(sub), run_time=0.5)
        self.at("tight binder")
        tb = chip("tight binder", MB, 30).move_to([BX[0], 0.0, 0])
        self.play(FadeIn(tb, scale=0.8), run_time=0.5)
        self.at("across the same gap")
        self.play(Indicate(bl[1], color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.at("about 7 percent")
        bar = bar_rect(0, 0.0)
        self.add(bar)
        self.play(Transform(bar, bar_rect(0, F_MB)), FadeIn(bar_value(0, F_MB), scale=1.3), run_time=0.6)
        self.finish()


def chart_upto(scene, n):
    scene.add(chart_frame())
    for i in range(n):
        f = [F_MB, F_HB, F_RS][i]
        scene.add(bar_labels(i), bar_rect(i, f), bar_value(i, f))


class S10Hb(Sc):
    def construct(self):
        chart_upto(self, 1)
        sub = T("muscle's storage protein", 28, MB).move_to([-2.6, 0.9, 0])
        tb = chip("tight binder", MB, 30).move_to([BX[0], 0.0, 0])
        self.add(sub, tb)
        bl = bar_labels(1)
        self.at("hemoglobin")
        self.play(FadeOut(sub), FadeOut(tb), FadeIn(bl, shift=UP * 0.1), run_time=0.6)
        self.at("gives up")
        bar = bar_rect(1, 0.0)
        self.add(bar)
        self.play(Transform(bar, bar_rect(1, F_HB)), run_time=1.0)
        self.at("thirds")
        self.play(FadeIn(bar_value(1, F_HB), scale=1.3), run_time=0.5)
        self.at("between the lungs")
        self.play(Indicate(bl[1], color=YELLOW, scale_factor=1.15), Indicate(bl[2], color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.finish()


class S11Rest(Sc):
    def construct(self):
        chart_upto(self, 2)
        bl = bar_labels(2)
        self.at("resting tissue")
        self.play(FadeIn(bl, shift=UP * 0.1), run_time=0.6)
        self.at("about a fifth")
        bar = bar_rect(2, 0.0)
        self.add(bar)
        self.play(Transform(bar, bar_rect(2, F_RS)), FadeIn(bar_value(2, F_RS), scale=1.3), run_time=0.8)
        self.at("still mostly full")
        r, txt = aboard_box()
        self.play(Create(r), FadeIn(txt), run_time=0.8)
        self.finish()


class S12Work(Sc):
    def construct(self):
        self.add(chart_frame())
        for i in (0, 2):
            f = [F_MB, F_HB, F_RS][i]
            self.add(bar_labels(i), bar_rect(i, f), bar_value(i, f))
        r, txt = aboard_box()
        self.add(r, txt)
        p = ValueTracker(20.0)
        fh = lambda: hill(100) - hill(p.get_value())

        def ctx():
            v = p.get_value()
            return "lungs → rest" if v > 37 else ("lungs → hard work" if v < 22 else "lungs → working")
        mid = always_redraw(lambda: bar_rect(1, fh()))
        midv = always_redraw(lambda: bar_value(1, fh()))
        midl = always_redraw(lambda: bar_labels(1, p.get_value(), ctx()))
        self.add(mid, midv, midl)
        self.at("drains far more")
        self.play(Indicate(mid, color=GOLD, scale_factor=1.05), run_time=0.9)
        # slider: how hard the muscle works
        y0 = 1.55
        hd = T("how hard the muscle works", 26, MUSC).move_to([-2.55, 2.35, 0])
        trk = Line([-4.3, y0, 0], [-1.4, y0, 0], color=GREY, stroke_width=7)
        l1 = T("rest", 28, GREY).next_to(trk.get_start(), DOWN, buff=0.38)
        l2 = T("hard work", 28, GREY).next_to(trk.get_end(), DOWN, buff=0.38)
        kx = lambda: -4.3 + (40 - p.get_value()) / 20 * 2.9
        knob = always_redraw(lambda: Circle(radius=0.27, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([kx(), y0, 0]))
        rd = always_redraw(lambda: VGroup(M("pO₂", 30, GREY), M(f"{p.get_value():.0f}", 50, YELLOW), M("torr", 30, GREY))
                           .arrange(RIGHT, buff=0.18, aligned_edge=DOWN).move_to([-2.75, 0.2, 0]))
        ghost = DashedVMobject(Rectangle(width=BW, height=F_HB * CH, stroke_color=BLUE, stroke_width=3), num_dashes=40)
        ghost.move_to([BX[1], BASE + F_HB * CH / 2, 0])
        self.at("the harder")
        self.add(ghost, knob, rd)
        self.play(FadeIn(hd), Create(trk), FadeIn(l1), FadeIn(l2), p.animate.set_value(40.0), run_time=0.8)
        self.at("works the more")
        self.play(p.animate.set_value(20.0), run_time=1.6, rate_func=smooth)
        self.finish()


# ---------------------------------------------------------------- 13: same heme, same iron
def s13_parts():
    blk, h1 = mb_pic()
    blks, hs = hb_pic()
    n1 = T("myoglobin", 38, MB).move_to([-3.9, 2.95, 0])
    n2 = T("hemoglobin", 38, BLUE).move_to([3.6, 2.95, 0])
    s1 = T("one chain", 30, GREY).move_to([-3.9, -2.3, 0])
    s2 = T("four chains", 30, GREY).move_to([3.6, -2.3, 0])
    return blk, h1, blks, hs, n1, n2, s1, s2


class S13Same(Sc):
    def construct(self):
        blk, h1, blks, hs, n1, n2, s1, s2 = s13_parts()
        self.at("both proteins")
        self.play(FadeIn(blk), FadeIn(blks), FadeIn(n1), FadeIn(n2), FadeIn(s1), FadeIn(s2), run_time=0.8)
        self.at("same heme")
        self.play(FadeIn(h1, scale=0.6), LaggedStart(*[FadeIn(x, scale=0.6) for x in hs], lag_ratio=0.1), run_time=0.7)
        self.at("same iron")
        bad = [fe_badge().move_to(c[0].get_corner(UR) + np.array([0.22, 0.3, 0])) for c in [h1] + list(hs)]
        self.play(*[FadeIn(b, scale=0.4) for b in bad], run_time=0.6)
        self.at("so what is hemoglobin")
        q = T("?", 160, GOLD, weight=BOLD).move_to([-0.15, 0.25, 0])
        self.play(FadeIn(q, scale=0.5), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------- 14: one site, four sites, and the steep part
class S14Four(Sc):
    def construct(self):
        blk, h1, blks, hs, n1, n2, s1, s2 = s13_parts()
        bad = [fe_badge().move_to(c[0].get_corner(UR) + np.array([0.22, 0.3, 0])) for c in [h1] + list(hs)]
        self.add(blk, h1, blks, hs, n1, n2, s1, s2, *bad)
        self.at("myoglobin has")
        ring = SurroundingRectangle(h1, color=YELLOW, buff=0.1, corner_radius=0.12, stroke_width=6)
        self.play(Create(ring), run_time=0.5)
        self.at("one binding site")
        t1 = T("one site", 34, YELLOW).move_to([-3.9, -2.95, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.at("hemoglobin has")
        rings = VGroup(*[SurroundingRectangle(x, color=YELLOW, buff=0.1, corner_radius=0.12, stroke_width=6) for x in hs])
        t2 = T("four sites", 34, YELLOW).move_to([3.6, -2.95, 0])
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), FadeIn(t2, shift=UP * 0.1), run_time=0.7)
        self.at("cooperate")
        c = blks.get_center()
        rad = np.linalg.norm(hs[0].get_center() - c)
        arcs = VGroup()
        for k in range(4):
            a0 = PI / 4 + k * PI / 2 + 0.5
            arc = Arc(radius=rad, start_angle=a0, angle=PI / 2 - 1.0, arc_center=c, color=GOLD, stroke_width=11)
            arc.add_tip(tip_length=0.32, tip_width=0.32)
            arcs.add(arc)
        arcs.set_z_index(6)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1),
                  *[h[0].animate.set_fill(YELLOW, opacity=0.6) for h in hs], run_time=0.8)
        self.at("its grip is set")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)
        ax, deco = mk_axes(10.0, 4.8, [0.75, 0.15, 0],
                           [(20, "20", "muscle", MUSC), (40, "40", "rest", GREY), (100, "100", "lungs", LUNGC)])
        xl = T("oxygen pressure, pO₂ (torr)", 28, GREY).move_to([0.75, -3.45, 0])
        yl = T("fraction of sites full", 28, GREY).rotate(PI / 2).move_to([-5.95, 0.15, 0])
        curve = ax.plot(lambda x: hill(x), x_range=[0.01, 110, 0.5], color=BLUE, stroke_width=6)
        nm = T("hemoglobin", 34, BLUE).move_to(ax.c2p(18, 0.86))
        self.play(Create(ax), FadeIn(deco), FadeIn(xl), FadeIn(yl), FadeIn(nm), Create(curve), run_time=0.8)
        self.at("pressures between")
        part = ax.plot(lambda x: hill(x), x_range=[20, 100, 0.5], color=GOLD, stroke_width=12)
        pm, pl = ax.c2p(20, hill(20)), ax.c2p(100, hill(100))
        dm, dl = Dot(pm, color=GOLD, radius=0.14), Dot(pl, color=GOLD, radius=0.14)
        vm = DashedLine(ax.c2p(20, 0), pm, color=MUSC, stroke_width=3)
        vl = DashedLine(ax.c2p(100, 0), pl, color=LUNGC, stroke_width=3)
        self.play(Create(part), FadeIn(dm), FadeIn(dl), Create(vm), Create(vl), run_time=0.6)
        self.at("lung")
        tl = T(f"lungs: {round(hill(100) * 100)}% full", 30, LUNGC).move_to(ax.c2p(74, 0.8))
        self.play(FadeIn(tl), run_time=0.4)
        self.at("muscle")
        tm = T(f"muscle: {round(hill(20) * 100)}% full", 30, MUSC).move_to(ax.c2p(46, 0.2))
        self.play(FadeIn(tm), run_time=0.4)
        self.wait(0.6)
        self.finish()


# ---------------------------------------------------------------- 15 to 19: two shapes
TX, RX, SY2 = -3.4, 3.4, 0.7
RB_MIX = mwc(P_MIX)[0]
RB_END = mwc(P_END)[0]


def letters():
    return (T("T", 56, BLUE, weight=BOLD).move_to([TX - 1.9, 3.2, 0]),
            T("R", 56, GREEN, weight=BOLD).move_to([RX - 1.9, 3.2, 0]))


def mixbar(fr=RB_MIX):
    return popbar(fr, 0, -2.55, 10.4, 1.0)


def mixtitle():
    return T("mix of T and R in the blood", 30, TEXT).move_to([0, -1.6, 0])


class S15Idea(Sc):
    def construct(self):
        hb = shapeT(0, SY2)
        nm = T("hemoglobin", 40, BLUE).move_to([0, 3.0, 0])
        self.play(FadeIn(hb, scale=0.8), FadeIn(nm), run_time=0.6)
        self.at("hemoglobin is")
        hb2 = hb.copy()
        self.add(hb2)
        Tl, Rl = letters()
        self.play(ReplacementTransform(hb, shapeT(TX, SY2)), ReplacementTransform(hb2, shapeR(RX, SY2)),
                  FadeOut(nm), FadeIn(Tl), FadeIn(Rl), run_time=0.9)
        self.at("a mix")
        self.play(FadeIn(mixbar(), shift=UP * 0.2), FadeIn(mixtitle()), run_time=0.7)
        self.finish()


def grip(shape, closed):
    """The cup on the right edge of a shape's upper-right block, and where the O2 sits."""
    blk = shape[1]
    edge = np.array([blk.get_right()[0], blk.get_center()[1], 0])
    if closed:
        c = edge + RIGHT * 0.3
        cup = VGroup(Circle(radius=0.62, arc_center=c, stroke_width=0, fill_color=GREEN, fill_opacity=0.3),
                     Arc(radius=0.62, start_angle=PI * 0.12, angle=1.76 * PI, arc_center=c, color=GREEN, stroke_width=12))
    else:
        c = edge + RIGHT * 0.85
        cup = Arc(radius=0.7, start_angle=PI * 0.68, angle=0.64 * PI, arc_center=c, color=BLUE, stroke_width=10)
    return cup, c


def rattle(m, base, amp):
    tt = [0.0]

    def f(mob, dt):
        tt[0] += dt
        mob.move_to(base + np.array([amp * np.sin(6 * tt[0]), amp * 0.8 * np.sin(8.1 * tt[0] + 1.0), 0]))
    m.add_updater(f)


class S16Shapes(Sc):
    def construct(self):
        sT, sR = shapeT(TX, SY2), shapeR(RX, SY2)
        Tl, Rl = letters()
        self.add(sT, sR, Tl, Rl, mixbar(), mixtitle())
        cupT, cT = grip(sT, False)
        cupR, cR = grip(sR, True)
        self.at("one shape")
        self.play(Indicate(VGroup(sT, Tl), color=BLUE, scale_factor=1.05), Create(cupT), run_time=0.8)
        self.at("holds oxygen")
        dT = o2(0.3).move_to(cT + UP * 1.4 + RIGHT * 0.3).set_z_index(5)
        self.add(dT)
        self.play(dT.animate.move_to(cT + RIGHT * 0.15), run_time=0.45)
        rattle(dT, cT + RIGHT * 0.15, 0.22)
        self.at("weakly")
        wk = T("= holds O₂ weakly", 34, BLUE).next_to(Tl, RIGHT, buff=0.25)
        self.play(FadeIn(wk, shift=LEFT * 0.1), run_time=0.5)
        self.at("the other")
        self.play(Indicate(VGroup(sR, Rl), color=GREEN, scale_factor=1.05), Create(cupR), run_time=0.8)
        self.at("holds it")
        dR = o2(0.4, 26).move_to(cR + UP * 1.4 + LEFT * 0.3).set_z_index(5)
        self.add(dR)
        self.play(dR.animate.move_to(cR), run_time=0.4)
        self.at("tightly")
        tg = T("= holds O₂ tightly", 34, GREEN).next_to(Rl, RIGHT, buff=0.25)
        self.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.5)
        self.wait(0.6)
        self.finish()


class S17Mix(Sc):
    def construct(self):
        rb, yr, yt, yall = mwc(P_MIX)
        GW, GH, GY = 4.8, 0.7, 2.15
        OW, OY = 11.4, -1.9

        def hgauge(cx, y, w):
            return Rectangle(width=w, height=GH, stroke_color=GREY, stroke_width=3).move_to([cx, y, 0])

        def hfill(fr, frac, col):
            return Rectangle(width=max(fr.width * frac, 0.02), height=fr.height, stroke_width=0, fill_color=col,
                             fill_opacity=0.95).align_to(fr, LEFT).set_y(fr.get_y())
        # overall gauge first, empty
        og = hgauge(0, OY, OW)
        ol = T("how full hemoglobin is", 32, YELLOW).move_to([0, OY + 0.8, 0])
        self.at("how full hemoglobin")
        self.play(Create(og), FadeIn(ol), run_time=0.6)
        # each shape's own fullness
        gt, gr = hgauge(-3.3, GY, GW), hgauge(3.3, GY, GW)
        it = shapeT(0, 0, 0.25)
        ir = shapeR(0, 0, 0.25)
        lt = VGroup(it, T("T alone: how full", 30, BLUE)).arrange(RIGHT, buff=0.2).move_to([-3.3, GY + 0.8, 0])
        lr = VGroup(ir, T("R alone: how full", 30, GREEN)).arrange(RIGHT, buff=0.2).move_to([3.3, GY + 0.8, 0])
        ft, fr_ = hfill(gt, yt, YELLOW), hfill(gr, yr, YELLOW)
        vt = M(f"{round(yt * 100)}%", 30, TEXT).next_to(ft, RIGHT, buff=0.12)
        vr = M(f"{round(yr * 100)}%", 30, TEXT).next_to(fr_, RIGHT, buff=0.12)
        self.at("how full each")
        self.play(Create(gt), Create(gr), FadeIn(lt), FadeIn(lr), run_time=0.5)
        self.play(GrowFromEdge(ft, LEFT), GrowFromEdge(fr_, LEFT), FadeIn(vt), FadeIn(vr), run_time=0.6)
        # how much of each is present
        pb = popbar(rb, 0, 0.3, OW, 0.9)
        pt = T("how much of each is present", 30, TEXT).move_to([0, 1.12, 0])
        self.at("how much of each")
        ex = T("example: very low oxygen", 28, GOLD).move_to([0, 3.48, 0])
        self.play(FadeIn(pb, shift=UP * 0.15), FadeIn(pt), FadeIn(ex), run_time=0.6)
        # weighted contributions add up
        self.at("present")
        ct = Rectangle(width=OW * yt * (1 - rb), height=0.8, stroke_width=0, fill_color=BLUE, fill_opacity=0.95)
        ct.align_to(og, LEFT).set_y(OY)
        cr = Rectangle(width=OW * yr * rb, height=0.8, stroke_width=0, fill_color=GREEN, fill_opacity=0.95)
        cr.next_to(ct, RIGHT, buff=0).set_y(OY)
        eq = M(f"{round((1 - rb) * 100)}% × {round(yt * 100)}%  +  {round(rb * 100)}% × {round(yr * 100)}%"
               f"  =  {round(yall * 100)}%", 28, TEXT).move_to([0, -3.15, 0])
        self.play(ReplacementTransform(ft.copy(), ct), ReplacementTransform(fr_.copy(), cr), FadeIn(eq), run_time=1.3)
        tot = Rectangle(width=OW * yall, height=0.8, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).align_to(og, LEFT).set_y(OY)
        tv = M(f"{round(yall * 100)}%", 34, YELLOW).next_to(tot, RIGHT, buff=0.15)
        self.play(ReplacementTransform(VGroup(ct, cr), tot), FadeIn(tv), run_time=0.6)
        self.wait(1.6)
        self.finish()


# s18 / s19 layout
BW18, BY18, BH18 = 8.6, -0.6, 1.6


def side_shapes():
    sT = shapeT(-5.65, BY18, 0.55)
    sR = shapeR(5.6, BY18, 0.55)
    Tl = T("T", 46, BLUE, weight=BOLD).next_to(sT, UP, buff=0.3)
    Rl = T("R", 46, GREEN, weight=BOLD).next_to(sR, UP, buff=0.3)
    return sT, sR, Tl, Rl


def mix_caption(fr):
    return T("mostly R: more O₂" if fr > 0.5 else "mostly T: low O₂", 40, GREEN if fr > 0.5 else BLUE).move_to([0, -2.4, 0])


DROP_X = np.linspace(-3.6, 3.6, 10)


class S18Shift(Sc):
    def construct(self):
        sT, sR, Tl, Rl = side_shapes()
        lp = ValueTracker(P_MIX)
        pb = always_redraw(lambda: popbar(mwc(lp.get_value())[0], 0, BY18, BW18, BH18, 34))
        cap = always_redraw(lambda: mix_caption(mwc(lp.get_value())[0]))
        title = T("mix of T and R in the blood", 30, TEXT).move_to([0, 2.2, 0])
        self.play(FadeIn(sT), FadeIn(sR), FadeIn(Tl), FadeIn(Rl), FadeIn(pb), FadeIn(cap), FadeIn(title), run_time=0.6)
        self.at("shifts the mix")
        bx = -BW18 / 2 + BW18 * (1 - RB_MIX)
        dv = DoubleArrow([bx - 1.4, 0.75, 0], [bx + 1.4, 0.75, 0], color=GOLD, stroke_width=8, buff=0, tip_length=0.3)
        self.play(GrowFromCenter(dv), run_time=0.5)
        self.at("oxygen itself")
        self.play(FadeOut(dv), FadeOut(title), run_time=0.25)
        drops = VGroup(*[o2().move_to([x, 3.6, 0]) for x in DROP_X]).set_z_index(5)
        self.add(drops)
        self.play(LaggedStart(*[d.animate.move_to([d.get_x(), 0.75, 0]) for d in drops], lag_ratio=0.06),
                  run_time=0.9, rate_func=rush_into)
        self.play(Indicate(VGroup(sR, Rl), color=GREEN, scale_factor=1.12), run_time=0.6)
        self.play(lp.animate.set_value(P_END), run_time=4.0, rate_func=smooth)
        self.wait(0.8)
        self.finish()


class S19Take(Sc):
    def construct(self):
        sT, sR, Tl, Rl = side_shapes()
        pb = popbar(RB_END, 0, BY18, BW18, BH18, 34)
        cap = mix_caption(RB_END)
        drops = VGroup(*[o2().move_to([x, 0.75, 0]) for x in DROP_X]).set_z_index(5)
        self.add(sT, sR, Tl, Rl, pb, cap, drops)
        self.at("oxygen pushes")
        ar = Arrow([-2.5, 1.65, 0], [3.5, 1.65, 0], color=GOLD, stroke_width=8, buff=0)
        at = T("toward R", 32, GREEN).next_to(ar, UP, buff=0.15)
        self.play(GrowArrow(ar), FadeIn(at), run_time=0.8)
        self.at("grabs oxygen best")
        self.play(Indicate(VGroup(sR, Rl), color=GREEN, scale_factor=1.15), run_time=0.9)
        self.at("that is cooperativity")
        co = T("cooperativity", 60, GOLD, font=TITLE_FONT).move_to([0, 3.25, 0])
        ax, deco = mk_axes(9.6, 4.6, [0.6, -0.3, 0], [(20, "20", "muscle", MUSC), (100, "100", "lungs", LUNGC)])
        yl = T("fraction of sites full", 26, GREY).rotate(PI / 2).move_to([-5.75, -0.3, 0])
        curve = ax.plot(lambda x: hill(x), x_range=[0.01, 110, 0.5], color=BLUE, stroke_width=6)
        why = VGroup(T("S-shaped because", 28, GOLD), T("the mix shifts", 28, GOLD)).arrange(DOWN, buff=0.08)
        why.move_to(ax.c2p(22, 0.9))
        inset = popbar(RB_END, 4.6, 3.3, 3.6, 0.4, 22).set_opacity(0.6)
        self.play(*[FadeOut(m) for m in (sT, sR, Tl, Rl, pb, cap, drops, ar, at)],
                  FadeIn(co, shift=DOWN * 0.1), FadeIn(ax), FadeIn(deco), FadeIn(yl), FadeIn(inset), run_time=0.5)
        self.play(Create(curve), FadeIn(why), run_time=0.9)
        self.at("why blood delivers")
        pm, pl = ax.c2p(20, hill(20)), ax.c2p(100, hill(100))
        xb = pl[0] + 0.4
        br = Line([xb, pl[1], 0], [xb, pm[1], 0], color=GOLD, stroke_width=8)
        caps = VGroup(Line([xb - 0.12, pl[1], 0], [xb + 0.12, pl[1], 0], color=GOLD, stroke_width=8),
                      Line([xb - 0.12, pm[1], 0], [xb + 0.12, pm[1], 0], color=GOLD, stroke_width=8))
        hz = DashedLine(pm, [xb, pm[1], 0], color=GOLD, stroke_width=3)
        dl = T("delivered", 32, GOLD).next_to(br, LEFT, buff=0.25)
        self.play(FadeIn(Dot(pm, color=GOLD, radius=0.12)), FadeIn(Dot(pl, color=GOLD, radius=0.12)),
                  Create(br), Create(caps), Create(hz), FadeIn(dl), run_time=0.7)
        self.wait(1.2)
        self.finish()
