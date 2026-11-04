"""Chapter 3: The Kinase from a Tumour (Neurotrophins, Trk Receptors and p75)

COLOR MAP (one color per concept, shared by every chapter of this lesson; taken from scenes.old.py)
  BLUE   = the neurotrophin (NGF): the dimer and its name label
  PINK   = Trk receptors (Trk, TrkB, TrkC), their kinase domains, and the genes for them
  VIOLET = p75 (the receptor, its gene, its binding sites in the cartoons)
  CLAY   = cancer / tumour origin: the tumour cell, the tropomyosin part of the fusion, "found in cancer" tags
  GREEN  = survival
  GREY   = membranes, cells, dishes, outlines, unknowns (LG, a lighter grey, is used for every text label and credit line)
  TEXT   = generic DNA, phosphate badges, question marks, DCC (a different receptor), the final statement
  (ORANGE pro-domain, YELLOW sortilin, GOLD cutting enzymes and RED death are not used in this chapter.)

Genes carry the colour of the protein they encode; unnamed DNA is white. Every shape is a labelled cartoon:
no molecular structures, no equations are needed because no curve is plotted in this chapter.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PINK = "#E879B9"
VIOLET = "#A98BE0"
CLAY = "#D08A5E"
LG = "#BCC3CF"      # light grey for every text label and credit line (readable on the dark ground)

CELL_Y = -1.85      # centre height of the fibroblast scenes
CELL_B = 1.25       # half height of the fibroblast
MEMB_Y = -0.6       # membrane height in the receptor-in-membrane scenes
OK = 1.35           # receptor scale in the orphan / DCC scenes


# ---------------------------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------------------------
def lab(text, color, x, y, size=26):
    return T(text, max(size, 26), color).move_to([x, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=12)


def membrane(y, h=0.5, w=13.4):
    return Rectangle(width=w, height=h, stroke_width=0, fill_color=GREY, fill_opacity=0.5).move_to([0, y, 0])


def tint(my, w=13.4):
    top = my - 0.25
    return Rectangle(width=w, height=top + 3.8, stroke_width=0, fill_color=GREY,
                     fill_opacity=0.10).move_to([0, top - (top + 3.8) / 2, 0])


def dimer(cx, cy, k=1.0, color=BLUE):
    h1, h2 = [Ellipse(width=1.0 * k, height=0.85 * k, stroke_color=color, stroke_width=3,
                      fill_color=color, fill_opacity=0.5).move_to([cx + s * 0.5 * k, cy, 0]) for s in (-1, 1)]
    return VGroup(h1, h2)


def badge(pos, r=0.25):
    c = Circle(radius=r, stroke_color=TEXT, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    return VGroup(c, T("P", 26, TEXT)).move_to(pos)


def ghost(g, color, n=18):
    """a dashed, unfilled copy of a group: 'the thing that is not there'."""
    return VGroup(*[DashedVMobject(m.copy().set_fill(opacity=0).set_stroke(color, 3), num_dashes=n, dashed_ratio=0.55)
                    for m in g])


def trk(cx, my, k=1.45, fill=0.45):
    """a Trk receptor cartoon: two binding blobs outside, a bar through the membrane at height my, a kinase blob inside."""
    def blob(w, h, y):
        return Ellipse(width=w * k, height=h * k, stroke_color=PINK, stroke_width=3,
                       fill_color=PINK, fill_opacity=fill).move_to([cx, my + y * k, 0])
    lo, up = blob(1.0, 0.85, 0.85), blob(1.0, 0.85, 1.65)
    tm = RoundedRectangle(corner_radius=0.12 * k, width=0.26 * k, height=0.8 * k, stroke_color=PINK, stroke_width=3,
                          fill_color=PINK, fill_opacity=0.8).move_to([cx, my, 0])
    kb = Ellipse(width=1.3 * k, height=1.0 * k, stroke_color=PINK, stroke_width=3,
                 fill_color=PINK, fill_opacity=fill).move_to([cx, my - 1.05 * k, 0])
    st = Line([cx, my - 0.4 * k, 0], [cx, my - 0.55 * k, 0], color=PINK, stroke_width=6)
    g = VGroup(st, lo, up, tm, kb)
    g.lo, g.up, g.tm, g.kb = lo, up, tm, kb
    g.top = my + 2.075 * k
    g.cx, g.my, g.k = cx, my, k
    return g


def p75r(cx, my, k=1.45):
    """p75: a tall bar outside, a bar through the membrane, a short empty tail inside (no kinase)."""
    ecd = RoundedRectangle(corner_radius=0.2 * k, width=0.75 * k, height=1.9 * k, stroke_color=VIOLET, stroke_width=3,
                           fill_color=VIOLET, fill_opacity=0.45).move_to([cx, my + 1.35 * k, 0])
    tm = RoundedRectangle(corner_radius=0.12 * k, width=0.26 * k, height=0.8 * k, stroke_color=VIOLET, stroke_width=3,
                          fill_color=VIOLET, fill_opacity=0.8).move_to([cx, my, 0])
    tail = Line([cx, my - 0.4 * k, 0], [cx, my - 0.95 * k, 0], color=VIOLET, stroke_width=6)
    g = VGroup(tail, ecd, tm)
    g.ecd, g.tm = ecd, tm
    g.top = my + 2.3 * k
    g.cx, g.my, g.k = cx, my, k
    return g


def dcc(cx, my, k=1.25):
    """DCC: a stack of small domains outside, a bar through the membrane, a blob inside (a different receptor: white)."""
    pills = VGroup(*[RoundedRectangle(corner_radius=0.14 * k, width=0.9 * k, height=0.36 * k, stroke_color=TEXT,
                                      stroke_width=3, fill_color=TEXT, fill_opacity=0.25).move_to([cx, my + (0.62 + 0.42 * i) * k, 0])
                     for i in range(4)])
    tm = RoundedRectangle(corner_radius=0.12 * k, width=0.26 * k, height=0.8 * k, stroke_color=TEXT, stroke_width=3,
                          fill_color=TEXT, fill_opacity=0.6).move_to([cx, my, 0])
    kb = Ellipse(width=0.95 * k, height=0.75 * k, stroke_color=TEXT, stroke_width=3,
                 fill_color=TEXT, fill_opacity=0.25).move_to([cx, my - 0.95 * k, 0])
    g = VGroup(pills, tm, kb)
    g.top = my + 2.1 * k
    return g


def circ(x, y, r, color=GREY, op=0.14, sw=3):
    body = Circle(radius=r, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=op)
    nuc = Circle(radius=r * 0.3, stroke_width=0, fill_color=color, fill_opacity=0.45)
    g = VGroup(body, nuc).move_to([x, y, 0])
    g.body = body
    return g


def neuron(x, y, r=1.7):
    body = Circle(radius=r, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14)
    nuc = Circle(radius=r * 0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.4)
    arms = VGroup(*[Line(np.array([np.cos(a), np.sin(a), 0]) * r, np.array([np.cos(a), np.sin(a), 0]) * (r + 0.55),
                         color=GREY, stroke_width=5) for a in np.radians([205, 250, 290, 335])])
    g = VGroup(arms, body, nuc).move_to([x, y, 0])
    g.body = body
    return g


def tumour(x, y, r=1.5, op=0.32):
    """a lumpy cell: a smooth closed curve with a computed wobble in its radius."""
    def f(t):
        rr = r * (1 + 0.11 * np.sin(5 * t) + 0.07 * np.sin(3 * t + 1.0) + 0.04 * np.sin(8 * t + 2.0))
        return np.array([rr * np.cos(t), rr * np.sin(t), 0])
    body = ParametricFunction(f, t_range=[0, TAU, 0.05], stroke_color=CLAY, stroke_width=4,
                              fill_color=CLAY, fill_opacity=op)
    nuc = Circle(radius=r * 0.38, stroke_width=0, fill_color=CLAY, fill_opacity=0.5).shift(LEFT * 0.12 * r)
    g = VGroup(body, nuc).move_to([x, y, 0])
    g.body = body
    return g


def gene(x, y, w=2.6, h=0.55, color=PINK, op=0.4):
    return RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def block(x, y, w, h, color, op=0.5):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def gbar(text, color, x, y, w, h, op=0.4, size=36):
    """a gene bar with its name written inside it (a label that sits on the thing it names)."""
    rect = gene(x, y, w, h, color, op)
    t = T(text, size, TEXT).move_to([x, y, 0]) if text else VGroup()
    g = VGroup(rect, t)
    g.rect, g.txt = rect, t
    return g


def dish_line(y):
    return Rectangle(width=12.6, height=0.14, stroke_width=0, fill_color=GREY, fill_opacity=0.7).move_to([0, y, 0])


def probe_icon():
    return VGroup(Circle(radius=0.55, stroke_color=PINK, stroke_width=6),
                  Line([0.39, -0.39, 0], [0.95, -0.95, 0], color=PINK, stroke_width=8))


# ---- a dish of mouse cells (scenes 3 and 4): three rows of cells in a big tray
DISH_Y = -0.4
ROW_Y = [DISH_Y + 1.55, DISH_Y, DISH_Y - 1.55]
ROW_X = [list(np.linspace(-4.5, 4.5, 7)), list(np.linspace(-3.75, 3.75, 6)), list(np.linspace(-4.5, 4.5, 7))]
DNA_CELLS = [1, 2, 3, 4, 5, 6]     # indices (top row) of the cells that take up a DNA fragment


def mouse_dish():
    tray = RoundedRectangle(corner_radius=0.3, width=12.2, height=5.1, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.08).move_to([0, DISH_Y, 0])
    cells = VGroup(*[circ(x, y, 0.68) for y, xs in zip(ROW_Y, ROW_X) for x in xs])
    return tray, cells


def dna_dot(cell):
    c = cell.get_center()
    return RoundedRectangle(corner_radius=0.05, width=0.42, height=0.13, stroke_width=0, fill_color=TEXT,
                            fill_opacity=0.95).rotate(0.4).move_to([c[0] + 0.05, c[1] - 0.28, 0])


# ---- the fibroblast (scenes 17 to 21): a flat, blunt cell in a dish
def sq(v, e):
    return np.sign(v) * abs(v) ** e


def cell_body(cx=0.0, a=5.9, p=4):
    return ParametricFunction(lambda t: np.array([cx + a * sq(np.cos(t), 2 / p), CELL_Y + CELL_B * sq(np.sin(t), 2 / p), 0]),
                              t_range=[0, TAU, 0.05], stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.14)


def ytop(x, cx=0.0, a=5.9, p=4):
    return CELL_Y + CELL_B * max(0.0, 1 - abs((x - cx) / a) ** p) ** (1 / p)


def nucleus(cx=0.0, w=2.0):
    return Ellipse(width=w, height=0.7, stroke_width=0, fill_color=GREY, fill_opacity=0.4).move_to([cx, CELL_Y - 0.3, 0])


RX = [-3.75, -2.45, 2.45, 3.75]    # receptor positions on the fibroblast (two pairs)
DX = [-3.1, 3.1]                    # a dimer sits on each pair
KR = 0.85                           # receptor scale on the fibroblast
DK = 1.3                            # dimer scale on the fibroblast
PAIR_TOP = ytop(2.45) + 2.075 * KR
DOCK_Y = PAIR_TOP + 0.425 * DK - 0.04      # the dimer rests on the receptor tips
HOVER_Y = DOCK_Y + 0.5                     # ... or hovers just above them


def surface_receptors():
    return [trk(x, ytop(x), KR) for x in RX]


def fib_scene(scene, label=True):
    line = dish_line(CELL_Y - CELL_B - 0.12)
    cell, nuc = cell_body(), nucleus()
    fl = lab("fibroblast", LG, 0, CELL_Y - CELL_B - 0.45, 26)
    scene.add(line, cell, nuc, *([fl] if label else []))
    return line, cell, nuc, fl


def test_head(x=-5.85, y=3.55):
    return T("A test", 30, TEXT).move_to([x, y, 0]).align_to([-6.7, 0, 0], LEFT)


def question():
    q1 = lab("What should happen?", TEXT, 0, 3.52, 40)
    q2 = lab("And what would that show Trk is sufficient for?", LG, 0, 3.02, 28)
    return q1, q2


def side_labels():
    """the 'Trk' label with a short leader to the left pair, and the 'NGF' label beside the left dimer."""
    tk = lab("Trk", PINK, -5.5, 0.15, 30)
    tl = Line([-5.0, 0.15, 0], [-4.3, 0.15, 0], color=PINK, stroke_width=3)
    return tk, tl


# ---------------------------------------------------------------------------------------------
# scenes
# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Neurotrophins, Trk Receptors and p75"
    TITLE = "The Kinase from a Tumour"


class S01(SpokenScene):
    def construct(self):
        n = neuron(-3.9, -0.9, 1.9)
        nl = lab("nerve cell", LG, -3.9, -3.55, 30)
        tc = tumour(3.9, -0.9, 1.9)
        tl = lab("colon tumour cell", CLAY, 3.9, -3.55, 30)
        ngf = dimer(-3.9, 3.3, 1.0)
        ngl = lab("growth factor", BLUE, -1.0, 3.3, 28)
        rec = trk(-3.9, 1.0, 0.85)
        rl = lab("Trk", PINK, -2.9, 1.9, 34)
        a = arr([-2.1, 1.45, 0], [2.3, 0.75, 0], CLAY, w=4)
        an = lab("named after", CLAY, 0.1, 1.75, 28)
        self.play(FadeIn(n), FadeIn(nl), FadeIn(tc), FadeIn(tl), run_time=0.6)
        self.at("growth factor")
        self.play(FadeIn(ngf, shift=DOWN * 0.2), FadeIn(ngl), run_time=0.5)
        self.at("receptor named")
        self.play(FadeIn(rec, scale=0.6), FadeIn(rl), run_time=0.5)
        self.at("named after")
        self.play(GrowArrow(a), FadeIn(an), run_time=0.6)
        self.at("tumor")
        self.play(Indicate(tc, color=CLAY, scale_factor=1.05), run_time=0.6)
        self.finish()


class S02(SpokenScene):
    def construct(self):
        my, k = -0.8, 1.45
        mem, inner = membrane(my), tint(my)
        p = p75r(-1.2, my, k)
        pl = lab("p75", VIOLET, -2.8, my + 1.4, 38)
        date = lab("1986", TEXT, -5.6, 3.4, 40)
        chip_s = chip("survival", GREEN, 30).move_to([2.2, -2.35, 0])
        da = DashedLine([-1.05, -2.35, 0], [chip_s.get_left()[0] - 0.05, -2.35, 0], color=GREY, stroke_width=4, dash_length=0.2)
        q = lab("?", TEXT, 2.2, -1.5, 70)
        self.play(FadeIn(mem), FadeIn(inner), FadeIn(date), run_time=0.5)
        self.at("first neurotrophin")
        self.play(FadeIn(p, shift=UP * 0.2), FadeIn(pl), run_time=0.6)
        self.at("could not")
        self.play(FadeIn(chip_s), Create(da), run_time=0.6)
        self.at("explain")
        self.play(GrowFromCenter(q), run_time=0.5)
        self.finish()


class S03(SpokenScene):
    def construct(self):
        tray, cells = mouse_dish()
        date = lab("1986", TEXT, -5.7, 3.45, 40)
        credit = lab("Chao and colleagues", LG, 4.3, 3.45, 28)
        ml = lab("mouse cells", LG, 0, DISH_Y - 3.0, 30)
        xs = [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
        frags = VGroup(*[RoundedRectangle(corner_radius=0.06, width=w, height=0.15, stroke_width=0, fill_color=TEXT,
                                          fill_opacity=0.95).rotate(a).move_to([x, 2.75, 0])
                         for x, w, a in zip(xs, [0.8, 0.55, 0.9, 0.6, 0.85, 0.5], [0.3, -0.5, 0.1, 0.7, -0.2, 0.4])])
        dl = lab("human DNA", TEXT, -4.7, 2.75, 30)
        self.play(FadeIn(tray), FadeIn(cells), FadeIn(date), FadeIn(ml), run_time=0.6)
        self.at("and colleagues")
        self.play(FadeIn(credit), run_time=0.4)
        self.at("human dna")
        self.play(FadeIn(frags, shift=DOWN * 0.2), FadeIn(dl), run_time=0.5)
        self.at("into mouse")
        dots = [dna_dot(cells[i]) for i in DNA_CELLS]
        self.play(*[f.animate.move_to(d.get_center()).scale(0.5) for f, d in zip(frags, dots)], FadeOut(dl), run_time=1.0)
        self.remove(frags)
        self.add(*dots)
        self.finish()


class S04(SpokenScene):
    def construct(self):
        tray, cells = mouse_dish()
        date = lab("1986", TEXT, -5.7, 3.45, 40)
        ml = lab("mouse cells", LG, 0, DISH_Y - 3.0, 30)
        dots = [dna_dot(cells[i]) for i in DNA_CELLS]
        self.add(tray, cells, date, ml, *dots)
        c = cells[3]
        cx, cy = c.get_center()[0], c.get_center()[1]
        self.at("cells that made")
        halo = Circle(radius=0.82, stroke_color=VIOLET, stroke_width=6).move_to(c.get_center())
        self.play(c.animate.set_color(VIOLET), FadeIn(halo), run_time=0.4)
        self.at("human receptor")
        base = cy + 0.68 - 0.1
        recs = VGroup(*[p75r(cx + dx, base - (0.1 if dx else 0), 0.5) for dx in (-0.5, 0, 0.5)])
        rl = lab("human receptor", VIOLET, 3.1, 2.6, 28)
        self.play(FadeIn(recs, shift=UP * 0.15), FadeIn(rl), run_time=0.5)
        self.at("and cloned")
        g = gene(cx, cy, 2.2, 0.45, VIOLET, 0.5).scale(0.2)
        self.add(g)
        self.play(g.animate.scale(5).move_to([-3.1, 3.0, 0]), run_time=0.9)
        self.at("its gene")
        gl = lab("p75 gene", VIOLET, -3.1, 2.45, 28)
        self.play(FadeIn(gl), run_time=0.4)
        self.finish()


class S05(SpokenScene):
    def construct(self):
        my, k = -1.0, 1.7
        mem, inner = membrane(my), tint(my)
        left = p75r(-3.4, my, k)
        ll = lab("human receptor, 1986", VIOLET, -3.4, -3.15, 28)
        self.add(mem, inner, left, ll)
        sh = lab("Shooter laboratory", LG, 3.4, 3.45, 30)
        right = p75r(3.4, my, k)
        rl = lab("rat receptor", VIOLET, 3.4, -3.15, 28)
        rl2 = lab("rat receptor, 1987", VIOLET, 3.4, -3.15, 28)
        a = arr([-2.3, 1.0, 0], [2.3, 1.0, 0], TEXT, w=4)
        ny = lab("next year", LG, 0, 1.5, 28)
        self.play(FadeIn(sh), FadeIn(right, shift=UP * 0.2), FadeIn(rl2), run_time=0.6)
        self.at("next year")
        self.play(GrowArrow(a), FadeIn(ny), run_time=0.6)
        self.finish()


class S06(SpokenScene):
    def construct(self):
        my, k = -0.8, 1.45
        mem, inner = membrane(my), tint(my)
        p = p75r(-1.8, my, k)
        pl = lab("p75", VIOLET, -3.5, my + 1.4, 38)
        self.add(mem, inner, p, pl)
        d = dimer(1.4, 2.4, 1.2)
        nl = lab("NGF", BLUE, -0.1, p.top + 0.53, 30)
        self.at("bound ngf")
        self.play(FadeIn(d), run_time=0.3)
        self.play(d.animate.move_to([-1.8, p.top + 0.51 + 0.02, 0]), FadeIn(nl), run_time=0.7)
        self.at("low affinity")
        low = chip("low affinity", TEXT, 28).move_to([3.0, 1.2, 0])
        self.play(d.animate.shift(RIGHT * 0.7 + UP * 0.1), FadeIn(low), run_time=0.45)
        self.play(d.animate.shift(LEFT * 0.7 + DOWN * 0.1), run_time=0.4)
        self.play(d.animate.shift(RIGHT * 0.6 + UP * 0.05), run_time=0.4)
        self.play(d.animate.shift(LEFT * 0.6 + DOWN * 0.05), run_time=0.4)
        self.at("no kinase")
        empty = DashedVMobject(Ellipse(width=1.3 * k, height=1.0 * k, stroke_color=PINK, stroke_width=4).move_to([-1.8, my - 1.55 * k, 0]),
                               num_dashes=20, dashed_ratio=0.55)
        nk = lab("no kinase", PINK, 0.7, my - 1.55 * k, 30)
        self.play(Create(empty), FadeIn(nk), run_time=0.6)
        self.finish()


# ---- scenes 7 and 8: two classes of binding site on a neuron, each holding an NGF dimer
NX, NY, NR = 0.0, -1.2, 2.2
CUPY = 2.15


def site(x, tight):
    sy = NY + np.sqrt(NR * NR - (x - NX) ** 2)
    if tight:      # a deep cup: the dimer sits snug inside it
        cup = Arc(radius=1.0, start_angle=np.radians(160), angle=np.radians(240), stroke_color=TEXT, stroke_width=7)
    else:          # a shallow dish: the dimer sits above it with a gap
        cup = Arc(radius=1.0, start_angle=np.radians(215), angle=np.radians(110), stroke_color=TEXT, stroke_width=7)
    cup.move_arc_center_to([x, CUPY, 0])
    stalk = Line([x, sy, 0], [x, CUPY - 1.0, 0], color=GREY, stroke_width=6)
    return VGroup(stalk, cup)


def site_dimer(x, tight):
    return dimer(x, CUPY - 0.4 if tight else CUPY + 0.35, 0.9)


class S07(SpokenScene):
    def construct(self):
        n = neuron(NX, NY, NR)
        nl = lab("neuron", LG, 0, -2.3, 34)
        loose, tight = site(-1.3, False), site(1.3, True)
        dl, dt = site_dimer(-1.3, False), site_dimer(1.3, True)
        loose_l = lab("loose", TEXT, -1.3, 3.45, 32)
        tight_l = lab("tight", TEXT, 1.3, 3.45, 32)
        ngl = lab("NGF", BLUE, -3.2, 2.5, 30)
        note = lab("schematic:\nhow many of\neach is not shown", LG, -4.9, -1.2, 26)
        self.play(FadeIn(n), FadeIn(nl), run_time=0.6)
        self.at("known to have")
        self.play(FadeIn(loose, shift=UP * 0.15), FadeIn(dl, shift=DOWN * 0.3), FadeIn(loose_l), FadeIn(ngl), run_time=0.6)
        self.play(dl.animate.shift(UP * 0.08), run_time=0.2)
        self.play(dl.animate.shift(DOWN * 0.08), run_time=0.2)
        self.at("higher affinity")
        self.play(FadeIn(tight, shift=UP * 0.15), FadeIn(dt, shift=DOWN * 0.3), FadeIn(tight_l), run_time=0.6)
        self.at("as well")
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


class S08(SpokenScene):
    def construct(self):
        n = neuron(NX, NY, NR)
        nl = lab("neuron", LG, 0, -2.3, 34)
        loose, tight = site(-1.3, False), site(1.3, True)
        dl, dt = site_dimer(-1.3, False), site_dimer(1.3, True)
        loose_l = lab("loose", TEXT, -1.3, 3.45, 32)
        tight_l = lab("tight", TEXT, 1.3, 3.45, 32)
        ngl = lab("NGF", BLUE, -3.2, 2.5, 30)
        note = lab("schematic:\nhow many of\neach is not shown", LG, -4.9, -1.2, 26)
        self.add(n, nl, loose, tight, dl, dt, loose_l, tight_l, ngl, note)
        pc = chip("p75", VIOLET, 34).move_to([-5.3, 1.1, 0])
        da = DashedLine([pc.get_right()[0] + 0.05, 1.15, 0], [-2.3, 1.75, 0], color=VIOLET, stroke_width=4, dash_length=0.2)
        q = lab("?", TEXT, 3.3, 2.0, 90)
        self.at("on its own")
        self.play(FadeIn(pc), run_time=0.4)
        self.at("p75 could")
        self.play(Create(da), run_time=0.5)
        self.at("could not account")
        self.play(GrowFromCenter(q), Indicate(tight, color=TEXT), Indicate(dt, color=BLUE), run_time=0.6)
        self.finish()


class S09(SpokenScene):
    def construct(self):
        kin = block(0, 0, 3.4, 1.9, PINK, 0.5)
        kl = lab("kinase", PINK, 0, 0, 36)
        kg = VGroup(kin, kl)
        tc = tumour(3.5, -0.3, 2.0)
        tl = lab("human colon tumour cell", CLAY, 3.5, -3.1, 30)
        a = arr([1.0, -0.3, 0], [-1.8, -0.3, 0], CLAY, w=5)
        self.at("kinase came")
        self.play(FadeIn(kg, scale=0.8), run_time=0.5)
        self.at("somewhere else")
        self.play(kg.animate.move_to([-3.8, -0.3, 0]), run_time=0.9)
        self.at("human colon")
        self.play(FadeIn(tc), run_time=0.5)
        self.play(GrowArrow(a), run_time=0.4)
        self.at("tumor")
        self.play(FadeIn(tl), run_time=0.4)
        self.finish()


class S10(SpokenScene):
    def construct(self):
        tc = tumour(3.5, -0.3, 2.0)
        tl = lab("human colon tumour cell", CLAY, 3.5, -3.1, 30)
        date = lab("1986", TEXT, -3.0, 2.7, 56)
        credit = lab("Martin-Zanca, Hughes\nand Barbacid", LG, -3.0, 1.0, 34)
        self.add(tc, tl)
        self.play(FadeIn(date), run_time=0.4)
        self.at("mariano")
        self.play(FadeIn(credit), run_time=0.5)
        self.at("an oncogene")
        onc = gbar("oncogene", TEXT, 3.5, -0.3, 4.4, 0.9, 0.15, 36).scale(0.25)
        self.add(onc)
        self.play(onc.animate.scale(4).move_to([-3.0, -1.5, 0]), run_time=0.9)
        self.at("that tumor")
        self.play(Indicate(tc, color=CLAY, scale_factor=1.06), run_time=0.6)
        self.finish()


GAPW = 5.6   # width of each block of the fusion
BH = 3.2     # height of each block


class S11(SpokenScene):
    def construct(self):
        bar = gbar("oncogene", TEXT, -3.0, -1.5, 5.2, 1.2, 0.15, 36)
        self.add(bar)
        left = block(-GAPW / 2 - 0.5, 0.0, GAPW, BH, CLAY, 0.5)
        right = block(GAPW / 2 + 0.5, 0.0, GAPW, BH, PINK, 0.5)
        ll = lab("tropomyosin\ngene (part)", TEXT, -GAPW / 2 - 0.5, 0.0, 38)
        rl = lab("tyrosine\nkinase gene", TEXT, GAPW / 2 + 0.5, 0.0, 38)
        self.at("tropomyosin gene")
        self.play(FadeOut(bar.txt), run_time=0.2)
        self.play(ReplacementTransform(bar.rect, left), FadeIn(ll), run_time=0.8)
        self.at("fused to")
        self.play(FadeIn(right, shift=LEFT * 0.4), run_time=0.4)
        self.play(left.animate.shift(RIGHT * 0.5), right.animate.shift(LEFT * 0.5), ll.animate.shift(RIGHT * 0.5),
                  run_time=0.6)
        seam = Line([0, -BH / 2, 0], [0, BH / 2, 0], color=TEXT, stroke_width=4)
        self.play(Create(seam), run_time=0.3)
        self.at("tyrosine kinase")
        self.play(FadeIn(rl.shift(LEFT * 0.5)), run_time=0.4)
        self.finish()


class S12(SpokenScene):
    def construct(self):
        top = block(0, 1.2, 5.0, 2.0, CLAY, 0.5)
        bot = block(0, -1.1, 5.0, 2.6, PINK, 0.5)
        tl = lab("tropomyosin part", TEXT, 0, 1.2, 36)
        bl = lab("kinase", TEXT, 0, -1.1, 44)
        fp = lab("one fused\nprotein", LG, -4.9, 0.0, 32)
        ring = DashedVMobject(Ellipse(width=3.0, height=1.1, stroke_color=TEXT, stroke_width=4).move_to([0, 3.0, 0]),
                              num_dashes=22, dashed_ratio=0.55)
        nlg = lab("no ligand", TEXT, 3.9, 3.0, 34)
        on = lab("kinase on", TEXT, 4.6, -1.1, 36)
        self.play(FadeIn(top), FadeIn(bot), FadeIn(tl), FadeIn(bl), FadeIn(fp), run_time=0.5)
        self.at("kept the kinase")
        glows = [bot.copy().set_fill(opacity=0).set_stroke(PINK, 6, 1) for _ in range(3)]
        self.add(*glows)
        self.play(bot.animate.set_fill(PINK, 0.95), FadeIn(on),
                  LaggedStart(*[g.animate.scale(1.25).set_stroke(opacity=0) for g in glows], lag_ratio=0.4),
                  run_time=1.0)
        self.at("without any")
        self.play(Create(ring), FadeIn(nlg), run_time=0.5)
        while self.narration_s - self.elapsed() > 0.9:
            g = bot.copy().set_fill(opacity=0).set_stroke(PINK, 6, 1)
            self.add(g)
            self.play(g.animate.scale(1.25).set_stroke(opacity=0), run_time=0.8)
            self.remove(g)
        self.finish()


class S13(SpokenScene):
    def construct(self):
        cb = block(-1.2, 0.0, 2.4, 3.4, CLAY, 0.5)
        pb = block(1.2, 0.0, 2.4, 3.4, PINK, 0.5)
        blocks = VGroup(cb, pb)
        words = VGroup(T("tropomyosin", 84, LG), T("receptor", 84, LG), T("kinase", 84, LG)).arrange(
            DOWN, buff=0.45).move_to([0, 0.0, 0])
        final = VGroup(T("t", 300, CLAY, weight=BOLD), T("r", 300, TEXT, weight=BOLD), T("k", 300, PINK, weight=BOLD)).arrange(
            RIGHT, buff=0.15, aligned_edge=DOWN).move_to([0, 0.0, 0])
        self.play(FadeIn(blocks), run_time=0.5)
        for n, (w, cue, col) in enumerate(zip(words, ["tropomyosin", "receptor", "kinase"], [CLAY, TEXT, PINK])):
            self.at(cue)
            w[0].set_color(col)
            if n == 0:
                self.play(FadeOut(blocks), FadeIn(w, shift=UP * 0.1), run_time=0.4)
            else:
                self.play(FadeIn(w, shift=UP * 0.1), run_time=0.25 if n == 2 else 0.4)
        self.play(*[FadeOut(w[1:]) for w in words], *[TransformFromCopy(words[i][0], final[i]) for i in range(3)],
                  *[w[0].animate.set_opacity(0) for w in words], run_time=0.45)
        self.finish()


def orphan_receptor(cx):
    r = trk(cx, MEMB_Y, OK)
    ring = DashedVMobject(Ellipse(width=2.4, height=1.02, stroke_color=TEXT, stroke_width=4).move_to([cx, r.top + 0.53, 0]),
                          num_dashes=18, dashed_ratio=0.55)
    return r, ring


class S14(SpokenScene):
    def construct(self):
        g = gene(-4.2, 1.6, 3.4, 0.8, PINK, 0.4)
        gl = lab("normal gene", PINK, -4.2, 0.85, 32)
        mem, inner = membrane(MEMB_Y), tint(MEMB_Y)
        r, ring = orphan_receptor(1.2)
        a = arr([-2.3, 1.6, 0], [0.45, 1.1, 0], GREY, w=4)
        ol = lab("orphan", LG, 3.65, r.top + 0.53, 40)
        self.play(FadeIn(g), FadeIn(gl), run_time=0.5)
        self.at("a membrane")
        self.play(FadeIn(mem), FadeIn(inner), run_time=0.4)
        self.play(GrowArrow(a), FadeIn(r, shift=UP * 0.2), run_time=0.7)
        self.at("no known ligand")
        self.play(Create(ring), FadeIn(ol), run_time=0.6)
        self.finish()


class S15(SpokenScene):
    def construct(self):
        mem, inner = membrane(MEMB_Y), tint(MEMB_Y)
        r, ring = orphan_receptor(1.2)
        ol = lab("orphan", LG, 3.65, r.top + 0.53, 40)
        trkl = VGroup(r, ring, ol)
        self.add(mem, inner, trkl)
        d = dcc(3.5, MEMB_Y, 1.3)
        dl = lab("DCC", TEXT, 5.4, 0.6, 34)
        self.at("dcc from")
        self.play(trkl.animate.shift(LEFT * 4.5), run_time=0.9)
        self.play(FadeIn(d, shift=UP * 0.2), FadeIn(dl), run_time=0.5)
        self.at("comes to mind")
        self.play(Indicate(d, color=TEXT, scale_factor=1.06), run_time=0.7)
        self.at("it should")
        self.play(Indicate(r, color=PINK, scale_factor=1.06), run_time=0.7)
        self.finish()


class S16(SpokenScene):
    def construct(self):
        mem, inner = membrane(MEMB_Y), tint(MEMB_Y)
        r = trk(-3.3, MEMB_Y, OK)
        d = dcc(3.5, MEMB_Y, 1.3)
        dl = lab("DCC", TEXT, 5.4, 0.6, 34)
        tl = lab("Trk", PINK, -5.2, 0.6, 34)
        self.add(mem, inner, r, d, dl, tl)
        self.at("in cancer")
        c1 = chip("found in cancer", CLAY, 28).move_to([-3.3, 2.85, 0])
        c2 = chip("found in cancer", CLAY, 28).move_to([3.5, 2.85, 0])
        self.play(FadeIn(c1, shift=DOWN * 0.15), FadeIn(c2, shift=DOWN * 0.15), run_time=0.5)
        self.at("wiring")
        n1 = chip("works in neurons", LG, 28).move_to([-3.3, -3.2, 0])
        n2 = chip("works in neurons", LG, 28).move_to([3.5, -3.2, 0])
        self.play(FadeIn(n1, shift=UP * 0.15), FadeIn(n2, shift=UP * 0.15), run_time=0.5)
        self.finish()


class S17(SpokenScene):
    def construct(self):
        head = test_head()
        line = dish_line(CELL_Y - CELL_B - 0.12)
        cell, nuc = cell_body(), nucleus()
        self.play(FadeIn(head), FadeIn(line), FadeIn(cell), FadeIn(nuc), run_time=0.5)
        self.at("fibroblast that")
        fl = lab("fibroblast", LG, 0, CELL_Y - CELL_B - 0.45, 26)
        self.play(FadeIn(fl), run_time=0.3)
        self.at("makes no")
        gh = ghost(trk(-3.1, ytop(-3.1), KR * 1.15), PINK)
        nt = lab("no Trk receptor", PINK, -3.1, ytop(-3.1) + 2.075 * KR * 1.15 + 0.4, 28)
        self.play(FadeIn(gh), FadeIn(nt), run_time=0.5)
        self.at("and ignores")
        xs = (0.6, 3.8)
        dims = VGroup(*[dimer(x, 2.3, DK) for x in xs])
        self.play(FadeIn(dims, shift=DOWN * 0.2), run_time=0.3)
        self.play(*[d.animate.move_to([x, ytop(x) + 0.425 * DK + 0.02, 0]) for d, x in zip(dims, xs)], run_time=0.6)
        ngf = lab("NGF", BLUE, 2.2, 1.0, 30)
        nr = lab("no response", LG, 2.2, 1.8, 34)
        self.play(FadeIn(ngf), FadeIn(nr), run_time=0.3)
        self.finish()


class S18(SpokenScene):
    def construct(self):
        head = test_head()
        self.add(head)
        fib_scene(self)
        self.at("the gene for")
        g = gene(-3.1, 1.3, 3.6, 0.7, PINK, 0.4)
        gl = lab("Trk gene", PINK, -3.1, 0.55, 30)
        self.play(FadeIn(g), FadeIn(gl), run_time=0.4)
        self.play(g.animate.scale(0.3).move_to([-3.0, CELL_Y, 0]), FadeOut(gl), run_time=0.6)
        self.play(FadeOut(g), run_time=0.2)
        self.at("protein")
        recs = surface_receptors()
        tk, tl = side_labels()
        self.play(*[FadeIn(r, shift=UP * 0.2) for r in recs], FadeIn(tk), FadeIn(tl), run_time=0.7)
        self.at("then add")
        dims = VGroup(*[dimer(x, HOVER_Y, DK) for x in DX])
        ngl = lab("NGF", BLUE, -5.35, HOVER_Y, 30)
        self.play(FadeIn(dims, shift=DOWN * 0.2), FadeIn(ngl), run_time=0.6)
        self.at("what should happen")
        q1, q2 = question()
        self.play(FadeIn(q1), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(q2), run_time=0.5)
        self.finish()


class S19Pause(NarratedScene):
    def construct(self):
        head = test_head()
        self.add(head)
        fib_scene(self)
        for r in surface_receptors():
            self.add(r)
        tk, tl = side_labels()
        self.add(tk, tl)
        self.add(VGroup(*[dimer(x, HOVER_Y, DK) for x in DX]), lab("NGF", BLUE, -5.35, HOVER_Y, 30))
        self.add(*question())
        self.finish()


class S20(SpokenScene):
    def construct(self):
        head = test_head()
        self.add(head)
        fib_scene(self)
        recs = surface_receptors()
        self.add(*recs)
        tk, tl = side_labels()
        self.add(tk, tl)
        dims = VGroup(*[dimer(x, HOVER_Y, DK) for x in DX])
        ngl = lab("NGF", BLUE, -5.35, HOVER_Y, 30)
        self.add(dims, ngl)
        q1, q2 = question()
        self.add(q1, q2)
        res = T("Result, spring 1991", 30, TEXT).move_to([-5.85, 3.55, 0]).align_to([-6.7, 0, 0], LEFT)
        self.at("in spring")
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(head), FadeIn(res), run_time=0.4)
        self.at("two groups")
        c1 = lab("Kaplan and colleagues", LG, 0, 3.55, 26)
        c2 = lab("Klein, Barbacid and colleagues", LG, 0, 3.1, 26)
        c1.align_to([6.7, 0, 0], RIGHT)
        c2.align_to([6.7, 0, 0], RIGHT)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        self.at("ngf binds")
        self.play(*[d.animate.move_to([x, DOCK_Y, 0]) for d, x in zip(dims, DX)], ngl.animate.move_to([-5.35, DOCK_Y, 0]),
                  run_time=0.8)
        self.at("causes")
        kb = badge([3.2, -3.55, 0], 0.25)
        kt = lab("= phosphate", TEXT, 4.75, -3.55, 28)
        self.play(FadeIn(kb), FadeIn(kt), run_time=0.4)
        self.at("tyrosine")
        bs = [badge([x, ytop(x) - 1.05 * KR, 0], 0.25) for x in RX]
        self.play(*[FadeIn(b, scale=0.5) for b in bs], run_time=0.5)
        self.at("phosphorylation")
        pl = lab("tyrosine\nphosphorylation", TEXT, 0, 0.3, 30)
        self.play(FadeIn(pl), run_time=0.4)
        self.finish()


class S21(SpokenScene):
    def construct(self):
        res = T("Result, spring 1991", 30, TEXT).move_to([-5.85, 3.55, 0]).align_to([-6.7, 0, 0], LEFT)
        c1 = lab("Kaplan and colleagues", LG, 0, 3.55, 26)
        c2 = lab("Klein, Barbacid and colleagues", LG, 0, 3.1, 26)
        c1.align_to([6.7, 0, 0], RIGHT)
        c2.align_to([6.7, 0, 0], RIGHT)
        line = dish_line(CELL_Y - CELL_B - 0.12)
        cell, nuc = cell_body(), nucleus()
        fl = lab("fibroblast", LG, 0, CELL_Y - CELL_B - 0.45, 26)
        recs = surface_receptors()
        dims = VGroup(*[dimer(x, DOCK_Y, DK) for x in DX])
        bs = VGroup(*[badge([x, ytop(x) - 1.05 * KR, 0], 0.25) for x in RX])
        ngl = lab("NGF", BLUE, -5.35, DOCK_Y, 30)
        tk, tl = side_labels()
        pl = lab("tyrosine\nphosphorylation", TEXT, 0, 0.3, 30)
        kb = badge([3.2, -3.55, 0], 0.25)
        kt = lab("= phosphate", TEXT, 4.75, -3.55, 28)
        self.add(res, c1, c2, line, cell, nuc, fl, *recs, dims, bs, ngl, tk, tl, pl, kb, kt)
        head = lab("Barbacid's group", TEXT, -4.9, 3.55, 30).align_to([-6.7, 0, 0], LEFT)
        self.play(FadeOut(res), FadeOut(c1), FadeOut(c2), FadeOut(pl), FadeOut(kb), FadeOut(kt), FadeIn(head), run_time=0.5)
        self.play(cell.animate.stretch(1.05, 0), nuc.animate.stretch(1.4, 0), run_time=1.2)
        self.at("fibroblasts carrying")
        self.play(*[Indicate(r, color=PINK, scale_factor=1.12) for r in recs], run_time=0.8)
        self.play(cell.animate.stretch(1.05, 0), nuc.animate.stretch(1.35, 0), run_time=0.7)
        self.at("divided", lead=0.4)
        d1 = cell_body(-3.1, 2.9)
        d2 = cell_body(3.1, 2.9)
        n1, n2 = nucleus(-3.1, 1.6), nucleus(3.1, 1.6)
        fl1, fl2 = lab("fibroblast", LG, -3.1, CELL_Y - CELL_B - 0.45, 26), lab("fibroblast", LG, 3.1, CELL_Y - CELL_B - 0.45, 26)
        self.play(ReplacementTransform(cell, VGroup(d1, d2)), ReplacementTransform(nuc, VGroup(n1, n2)),
                  FadeOut(fl), FadeIn(fl1), FadeIn(fl2), FadeOut(ngl), FadeOut(tk), FadeOut(tl), run_time=1.2)
        self.at("response to")
        self.play(Indicate(dims, color=BLUE, scale_factor=1.06), run_time=0.7)
        self.at("without needing")
        gps = []
        gls = []
        for sgn in (-1, 1):
            gx = sgn * 5.2
            gps.append(ghost(p75r(gx, ytop(gx, sgn * 3.1, 2.9), 0.7), VIOLET))
            gls.append(lab("no p75", VIOLET, gx, ytop(gx, sgn * 3.1, 2.9) + 2.3 * 0.7 + 0.4, 26))
        self.play(*[FadeIn(g) for g in gps], *[FadeIn(g) for g in gls], run_time=0.5)
        self.finish()


class S22(SpokenScene):
    def construct(self):
        mem, inner = membrane(MEMB_Y), tint(MEMB_Y)
        r, ring = orphan_receptor(0.4)
        ol = lab("orphan", LG, 3.9, r.top + 0.53, 40)
        self.add(mem, inner)
        self.at("orphan kinase")
        self.play(FadeIn(r, shift=UP * 0.2), Create(ring), FadeIn(ol), run_time=0.5)
        self.at("from a tumor")
        tc = chip("from a tumour", CLAY, 28).move_to([-3.3, 0.9, 0])
        ta = arr([tc.get_right()[0] + 0.05, 0.9, 0], [-0.5, 0.9, 0], CLAY, w=4)
        self.play(FadeIn(tc), GrowArrow(ta), run_time=0.5)
        self.at("receptor for")
        d = dimer(3.0, r.top + 0.53, 1.2)
        self.add(d)
        self.play(d.animate.move_to([0.4, r.top + 0.53, 0]), FadeOut(ring), run_time=0.5)
        self.at("for ngf")
        nl = lab("NGF receptor", TEXT, 3.9, r.top + 0.53, 36)
        self.play(FadeOut(ol), run_time=0.3)
        self.play(FadeIn(nl), run_time=0.4)
        self.finish()


LIB_X = [-5.1 + 1.7 * i for i in range(7)]
LIB_Y = [2.2, 1.1, 0.0, -1.1, -2.2]
BAR_X, BAR_W, BAR_H = -1.0, 7.0, 1.7
ROW_YS = [2.0, 0.0, -2.0]     # the three gene bars: trk, trkB, trkC
YR_X = 4.9
ROW2 = [1.55, -1.55]      # the two bars of scene 24 (before the third arrives)
BH2 = 2.6


def library(op=0.15):
    return VGroup(*[Rectangle(width=1.5, height=0.95, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                              fill_opacity=op).move_to([x, y, 0]) for y in LIB_Y for x in LIB_X])


def tile(col, row):
    return col + 7 * row


class S23(SpokenScene):
    def construct(self):
        tiles = library()
        self.play(FadeIn(tiles), run_time=0.6)
        self.at("laboratory")
        credit = lab("Klein, Barbacid laboratory", LG, 3.9, 3.4, 28)
        self.play(FadeIn(credit), run_time=0.4)
        self.at("went looking")
        probe = probe_icon().move_to([LIB_X[0], LIB_Y[0], 0])
        self.play(FadeIn(probe), run_time=0.2)

        def row(j, t):
            xs = LIB_X if j % 2 == 0 else LIB_X[::-1]
            pts = [probe.get_center()] + [np.array([x, LIB_Y[j], 0]) for x in xs]
            return MoveAlongPath(probe, VMobject().set_points_as_corners(pts), rate_func=linear, run_time=t)
        bar = gbar("trk gene", PINK, -4.2, 3.35, 2.8, 0.55, 0.4, 26)
        ml = lab("mouse brain", LG, 0, -3.3, 30)
        self.play(row(0, 0.5), run_time=0.5)
        self.at("gene in")
        self.play(FadeIn(bar), row(1, 0.4), run_time=0.4)
        self.at("mouse brain")
        self.play(FadeIn(ml), row(2, 0.5), run_time=0.5)
        self.play(row(3, 0.5), run_time=0.5)
        self.play(row(4, 0.5), run_time=0.5)
        self.finish()


class S24(SpokenScene):
    def construct(self):
        tiles = library()
        bar = gbar("trk gene", PINK, -4.2, 3.35, 2.8, 0.55, 0.4, 26)
        ml = lab("mouse brain", LG, 0, -3.3, 30)
        self.add(tiles, bar, ml)
        self.at("later account")
        note = lab("Klein's later account", LG, 3.9, 3.4, 28)
        self.play(FadeIn(note), run_time=0.4)
        self.at("recovered a related")
        t = tiles[tile(4, 3)]
        self.play(t.animate.set_stroke(PINK, 4).set_fill(PINK, 0.5), run_time=0.4)
        trkbar = gbar("trk", PINK, BAR_X, ROW2[0], BAR_W, BH2, 0.4, 60)
        found = gene(t.get_center()[0], t.get_center()[1], 1.2, 0.5, PINK, 0.4)
        self.add(found)
        self.play(FadeOut(tiles), FadeOut(ml), FadeOut(note), ReplacementTransform(bar, trkbar),
                  found.animate.become(gene(BAR_X, ROW2[1], BAR_W, BH2, PINK, 0.4)), run_time=1.1)
        self.at("instead")
        self.play(Indicate(found, color=PINK, scale_factor=1.04), run_time=0.6)
        self.at("in 1989")
        yr = lab("1989", TEXT, YR_X, ROW2[1], 36)
        self.play(FadeIn(yr), run_time=0.4)
        self.at("track b")
        bt = T("trkB", 60, TEXT).move_to([BAR_X, ROW2[1], 0])
        self.play(FadeIn(bt), run_time=0.4)
        self.finish()


class S25(SpokenScene):
    def construct(self):
        a1 = gbar("trk", PINK, BAR_X, ROW2[0], BAR_W, BH2, 0.4, 60)
        a2 = gbar("trkB", PINK, BAR_X, ROW2[1], BAR_W, BH2, 0.4, 60)
        ya = lab("1989", TEXT, YR_X, ROW2[1], 36)
        b1 = gbar("trk", PINK, BAR_X, ROW_YS[0], BAR_W, BAR_H, 0.4, 54)
        b2 = gbar("trkB", PINK, BAR_X, ROW_YS[1], BAR_W, BAR_H, 0.4, 54)
        y2 = lab("1989", TEXT, YR_X, ROW_YS[1], 36)
        self.add(a1, a2, ya)
        self.play(ReplacementTransform(a1, b1), ReplacementTransform(a2, b2), ReplacementTransform(ya, y2), run_time=0.5)
        self.at("search with")
        credit = lab("Lamballe, Klein and Barbacid", LG, 0, 3.4, 28)
        self.play(FadeIn(credit), run_time=0.4)
        probe = probe_icon().move_to([-4.0, ROW_YS[2], 0])
        self.play(FadeIn(probe), run_time=0.25)
        self.play(probe.animate.move_to([1.6, ROW_YS[2], 0]), run_time=1.0, rate_func=linear)
        self.at("found a third")
        third = gbar("", PINK, BAR_X, ROW_YS[2], BAR_W, BAR_H, 0.4, 54)
        self.play(FadeIn(third, scale=0.9), probe.animate.move_to([3.6, ROW_YS[2] - 0.2, 0]), run_time=0.6)
        self.at("third relative")
        tt = T("trkC", 54, TEXT).move_to([BAR_X, ROW_YS[2], 0])
        self.play(FadeIn(tt), FadeOut(probe), run_time=0.4)
        self.at("reported in")
        yr = lab("1991", TEXT, YR_X, ROW_YS[2], 36)
        self.play(FadeIn(yr), run_time=0.4)
        self.finish()


class S26(SpokenScene):
    def construct(self):
        names = ["trk", "trkB", "trkC"]
        bars = VGroup(*[gbar(n, PINK, BAR_X, y, BAR_W, BAR_H, 0.4, 54) for n, y in zip(names, ROW_YS)])
        yrs = VGroup(lab("1989", TEXT, YR_X, ROW_YS[1], 36), lab("1991", TEXT, YR_X, ROW_YS[2], 36))
        self.add(bars, yrs)
        self.at("turned up")
        my = -0.5
        mem, inner = membrane(my), tint(my)
        recs = [trk(x, my, 1.35) for x in (-4.4, 0.0, 4.4)]
        rl = VGroup(*[lab(n, PINK, x, -3.25, 34) for n, x in zip(["Trk", "TrkB", "TrkC"], (-4.4, 0.0, 4.4))])
        self.play(FadeOut(bars), FadeOut(yrs), FadeIn(mem), FadeIn(inner), *[FadeIn(r, scale=0.7) for r in recs], FadeIn(rl),
                  run_time=0.6)
        self.at("family of three")
        br = VMobject(stroke_color=TEXT, stroke_width=4)
        br.set_points_as_corners([[-5.6, 2.7, 0], [-5.6, 3.0, 0], [5.6, 3.0, 0], [5.6, 2.7, 0]])
        fam = lab("a family of three", TEXT, 0, 3.45, 38)
        self.play(Create(br), FadeIn(fam), run_time=0.6)
        self.finish()


class S27(SpokenScene):
    def construct(self):
        my = -0.5
        mem, inner = membrane(my), tint(my)
        recs = [trk(x, my, 1.35) for x in (-4.4, 0.0, 4.4)]
        rl = [lab(n, PINK, x, -3.25, 34) for n, x in zip(["Trk", "TrkB", "TrkC"], (-4.4, 0.0, 4.4))]
        self.add(mem, inner, *recs, *rl)
        self.at("original")
        og = lab("original", TEXT, -4.4, 2.8, 32)
        self.play(FadeIn(og), Indicate(recs[0], color=PINK, scale_factor=1.06), run_time=0.7)
        self.at("now called")
        newl = lab("TrkA", PINK, -4.4, -3.25, 34)
        self.play(FadeOut(rl[0]), FadeIn(newl), run_time=0.5)
        self.finish()


class S28(SpokenScene):
    def construct(self):
        my = -0.5
        mem, inner = membrane(my), tint(my)
        a = trk(-2.8, my, 1.4)
        p = p75r(2.8, my, 1.4)
        al = lab("TrkA", PINK, -4.9, 0.6, 34)
        self.add(mem, inner, a, al)
        q = lab("?", TEXT, 0.1, 1.2, 100)
        self.at("one question")
        self.play(GrowFromCenter(q), run_time=0.5)
        self.at("p75 and")
        pl = lab("p75", VIOLET, 4.9, 0.6, 34)
        self.play(FadeIn(p, shift=UP * 0.2), FadeIn(pl), run_time=0.6)
        self.at("together")
        d1 = DashedLine([-1.9, 1.2, 0], [-0.6, 1.2, 0], color=TEXT, stroke_width=5, dash_length=0.18)
        d2 = DashedLine([0.8, 1.2, 0], [2.0, 1.2, 0], color=TEXT, stroke_width=5, dash_length=0.18)
        self.play(Create(d1), Create(d2), run_time=0.6)
        self.at("high affinity")
        hc = chip("high-affinity binding", TEXT, 30).move_to([0.0, 3.3, 0])
        self.play(FadeIn(hc, shift=DOWN * 0.15), run_time=0.5)
        self.at("still argued")
        sa = lab("still argued", TEXT, 0, 0.4, 40)
        self.play(FadeIn(sa), run_time=0.5)
        self.finish()


class S29(SpokenScene):
    def construct(self):
        my = -0.5
        mem, inner = membrane(my, w=7.4).shift(RIGHT * 2.3), tint(my, w=7.4).shift(RIGHT * 2.3)
        r = trk(2.3, my, 1.45)
        head = lab("Takeaway", TEXT, -5.2, 3.45, 36)
        sr = lab("survival\nreceptor", PINK, 5.7, 0.9, 30)
        self.play(FadeIn(head), run_time=0.4)
        self.at("survival receptor")
        self.play(FadeIn(mem), FadeIn(inner), FadeIn(r, shift=UP * 0.2), FadeIn(sr), run_time=0.6)
        self.at("found in cancer")
        tc = tumour(-4.6, 0.9, 1.5)
        tcl = lab("cancer cell", CLAY, -4.6, -1.35, 30)
        a = arr([1.45, 0.9, 0], [-2.7, 0.9, 0], CLAY, w=4)
        fi = lab("first found in", CLAY, -0.6, 1.4, 28)
        self.play(FadeIn(tc), FadeIn(tcl), run_time=0.5)
        self.play(GrowArrow(a), FadeIn(fi), run_time=0.5)
        self.at("ngf")
        d = dimer(4.4, r.top + 0.53, 1.2)
        nl = lab("NGF", BLUE, 5.6, r.top + 0.53, 30)
        self.play(FadeIn(d), FadeIn(nl), run_time=0.3)
        self.play(d.animate.move_to([2.3, r.top + 0.53, 0]), nl.animate.move_to([4.7, r.top + 0.53, 0]), run_time=0.5)
        self.at("turned it on")
        b = badge([2.3, my - 1.05 * 1.45, 0], 0.27)
        ok = chip("kinase on, phosphorylated", TEXT, 28).move_to([2.3, -3.3, 0])
        self.play(r.kb.animate.set_fill(PINK, 0.95), FadeIn(b, scale=0.5), FadeIn(ok), run_time=0.5)
        self.finish()


class S30End(EndCard):
    LINE = "The survival receptor was found in cancer,\nand NGF turned it on."
