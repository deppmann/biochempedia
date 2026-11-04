"""The First Brake: The Mitochondrial Gate  (Biochemistrypedia explainer, chapter 4 of 6,
"The Death Machinery in Neurons").  Timed to the SPOKEN words: every self.at("...") waits for that phrase
in audio/words.json.   (Second draft: redrawn after the frame-by-frame review in FIXES.md.)

COLOR MAP (one colour per concept, shared with the other chapters; taken from scenes.old.py)
  BLUE   = the neuron / a living cell
  YELLOW = NGF, the survival signal, Akt, and the brakes it applies
  TEAL   = new gene expression: c-Jun, the pro-death genes, the 1988 drugs that block it
  ORANGE = pro-death BCL-2 family proteins (Bim, Bax, EGL-1, the BH3 helix)
  PINK   = cytochrome c
  PURPLE = CED-4 / Apaf-1 and the apoptosome wheel
  RED    = the killers (CED-3 / caspases), death, "removed / crossed out"
  GREEN  = protective: CED-9 / Bcl-2, "survives"
  GREY   = mitochondrion outline, timelines, plain labels (light grey LGREY for text), dead or inactive things
  WHITE  = (new in chapter 4) the stress kinase JNK, phosphate tags, the gate label, the step markers

THE GATE (one picture in every gate scene): Bcl-2 blocks sit on the outer membrane and hold Bax shut beside them.
It opens when Bax rods insert into the membrane and leave a gap between them; cytochrome c leaves through that gap.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F28CB1"
WHITE = TEXT
LGREY = "#B8BEC9"


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def dimchip(c, o=0.35):
    return [c[1].animate.set_stroke(opacity=o).set_fill(opacity=0.16 * o), c[2].animate.set_opacity(o)]


def litchip(c, color, fill=0.38):
    return [c[1].animate.set_stroke(color, opacity=1).set_fill(color, fill), c[2].animate.set_color(color).set_opacity(1)]


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def inhib(a, b, color=RED, w=5):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    b = b - d * 0.08
    perp = np.array([-d[1], d[0], 0])
    return VGroup(Line(a, b, color=color, stroke_width=w),
                  Line(b + perp * 0.26, b - perp * 0.26, color=color, stroke_width=w + 1))


def xmark(center, s=0.22, color=RED, w=6):
    c = np.array(center, float)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], color=color, stroke_width=w),
                  Line(c + [-s, s, 0], c + [s, -s, 0], color=color, stroke_width=w))


def neuron(r=0.75, color=BLUE):
    body = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.28)
    stubs = VGroup()
    for ang in (150, 210, 90):
        v = np.array([np.cos(np.radians(ang)), np.sin(np.radians(ang)), 0])
        stubs.add(Line(v * r, v * (r + 0.28), color=color, stroke_width=4))
    nuc = Circle(radius=r * 0.3, stroke_width=0, fill_color=color, fill_opacity=0.55)
    g = VGroup(body, stubs, nuc)
    g.body, g.stubs, g.nuc = body, stubs, nuc
    return g


def vbar(x, base_y, w, color, h0):
    tr = ValueTracker(h0)
    bar = always_redraw(lambda: Rectangle(width=w, height=max(tr.get_value(), 0.02), stroke_color=color, stroke_width=2,
                                          fill_color=color, fill_opacity=0.85).move_to([x, base_y, 0], aligned_edge=DOWN))
    return tr, bar


def wiggle(x0, y0, length=0.9, amp=0.12, color=TEAL, w=5):
    return ParametricFunction(lambda t: np.array([x0 + t, y0 + amp * np.sin(t * 12), 0]), t_range=[0, length, 0.02],
                              color=color, stroke_width=w).move_to([x0, y0, 0])


def notched(w, h, color, nw_ratio=0.55, nd=0.45, fill=0.28, sw=4):
    """a rounded block with a groove (notch) in its top edge; centred on the origin"""
    nw = w * nw_ratio
    pts = [(-w / 2, -h / 2), (-w / 2, h / 2), (-nw / 2, h / 2), (-nw / 2, h / 2 - nd), (nw / 2, h / 2 - nd), (nw / 2, h / 2),
           (w / 2, h / 2), (w / 2, -h / 2)]
    poly = Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=fill)
    poly.round_corners(0.1)
    return poly


def rod_at(x, y, w=1.3, h=0.28, color=ORANGE):
    return RoundedRectangle(corner_radius=min(h / 2, 0.14), width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.8).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
# the cell, the step markers (shared by many scenes)
# ---------------------------------------------------------------------------------------------
CELL_C = np.array([0.0, -0.35, 0.0])
CELL_W, CELL_H = 13.0, 6.9


def cell(color=BLUE, op=1.0):
    fill = Ellipse(width=CELL_W, height=CELL_H, stroke_width=0, fill_color=color, fill_opacity=0.07 * op).move_to(CELL_C)
    segs = VGroup(*[ParametricFunction(
        lambda t: CELL_C + np.array([CELL_W / 2 * np.cos(t), CELL_H / 2 * np.sin(t), 0]),
        t_range=[k * TAU / 16 - 0.03, (k + 1) * TAU / 16 + 0.03, 0.05], color=color, stroke_width=4, stroke_opacity=op)
        for k in range(16)])
    g = VGroup(fill, segs)
    g.fill, g.segs = fill, segs
    return g


STEP_LABELS = ["signal falls", "genes on", "gate opens", "killers assemble"]


def _spec(s):
    return {"hidden": (GREY, 0, TEXT, 0, GREY, 0, TEXT, 0),
            "dark": (GREY, 1, TEXT, 0, GREY, 1, TEXT, 0),
            "neutral": (GREY, 1, TEXT, 0, GREY, 1, LGREY, 1),
            "lit": (TEXT, 1, TEXT, 1, BG, 1, TEXT, 1)}[s]


def tracker(states=("hidden",) * 4, y=3.45, size=25):
    """Four step markers across the top. states: hidden / dark (circle only) / neutral (circle + grey label) / lit."""
    items, groups = [], []
    for i, lab in enumerate(STEP_LABELS):
        c = Circle(radius=0.28, stroke_width=3, stroke_color=GREY, fill_color=TEXT, fill_opacity=0)
        n = T(str(i + 1), 24, GREY, weight=BOLD)
        l = T(lab, size, TEXT)
        n.move_to(c)
        l.next_to(c, RIGHT, buff=0.15)
        groups.append(VGroup(c, n, l))
        items.append([c, n, l])
    row = VGroup(*groups).arrange(RIGHT, buff=0.42).move_to([0, y, 0])
    if row.width > 12.6:
        row.scale(12.6 / row.width).move_to([0, y, 0])
    row.items = items
    row.groups = groups
    for i, s in enumerate(states):
        tset(row, i, s)
    return row


def tset(row, i, s, animate=False):
    c, n, l = row.items[i]
    a, b, cc, d, e, f, g, h = _spec(s)
    if animate:
        return [c.animate.set_stroke(a, opacity=b).set_fill(cc, opacity=d), n.animate.set_color(e).set_opacity(f),
                l.animate.set_color(g).set_opacity(h)]
    c.set_stroke(a, opacity=b).set_fill(cc, opacity=d)
    n.set_color(e).set_opacity(f)
    l.set_color(g).set_opacity(h)
    return None


def light(row, i):
    """animations that light marker i (plus a ring so the eye goes to it)"""
    c = row.items[i][0]
    return tset(row, i, "lit", True) + [Flash(c.get_center(), color=TEXT, flash_radius=0.55, line_length=0.18, run_time=0.8)]


# ---------------------------------------------------------------------------------------------
# nucleus (steps 2): at the right of the cell, with a visible pore in its outline on the left
# ---------------------------------------------------------------------------------------------
NUC_C = np.array([3.0, -0.35, 0.0])
NUC_A, NUC_B = 2.5, 2.2
GENE_Y = -1.0
GENE_XS = [1.7, 3.0, 4.3]
PORE = np.array([NUC_C[0] - NUC_A, NUC_C[1], 0.0])


def nucleus(inner=True):
    g = 0.17
    fill = Ellipse(width=2 * NUC_A, height=2 * NUC_B, stroke_width=0, fill_color=GREY, fill_opacity=0.10).move_to(NUC_C)
    out = ParametricFunction(lambda t: NUC_C + np.array([NUC_A * np.cos(t), NUC_B * np.sin(t), 0]),
                             t_range=[PI + g, 3 * PI - g, 0.04], color=LGREY, stroke_width=4)
    ticks = VGroup()
    for s in (-1, 1):
        t = PI + s * g
        p = NUC_C + np.array([NUC_A * np.cos(t), NUC_B * np.sin(t), 0])
        ticks.add(Line(p + [-0.22, 0, 0], p + [0.12, 0, 0], color=LGREY, stroke_width=5))
    lab = T("nucleus", 28, LGREY).move_to([NUC_C[0], NUC_C[1] - NUC_B - 0.32, 0])
    dna = Line([0.8, GENE_Y, 0], [5.2, GENE_Y, 0], color=GREY, stroke_width=3)
    genes = VGroup(*[Rectangle(width=1.1, height=0.75, stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.0)
                     .move_to([x, GENE_Y, 0]) for x in GENE_XS])
    glab = T("pro-death genes", 30, TEAL).move_to([NUC_C[0], -1.8, 0])
    G = VGroup(fill, out, ticks, lab, dna, genes, glab)
    G.fill, G.out, G.ticks, G.lab, G.dna, G.genes, G.glab = fill, out, ticks, lab, dna, genes, glab
    G.shell = VGroup(fill, out, ticks)
    G.inner = VGroup(dna, genes, glab)
    return G


def genes_lit(nuc, op=0.7):
    return [gx.animate.set_fill(TEAL, op) for gx in nuc.genes]


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "The Death Machinery in Neurons"
    TITLE = "The First Brake: The Mitochondrial Gate"


# ---------------------------------------------------------------------------------------------
class S01(SpokenScene):
    """a sympathetic neuron loses its NGF; four unknown steps stand before the killers"""

    def construct(self):
        by = -0.6
        tissue = RoundedRectangle(corner_radius=0.3, width=2.3, height=6.0, stroke_color=GREY, stroke_width=3,
                                  fill_color=GREY, fill_opacity=0.12).move_to([-5.6, by, 0])
        tlab = T("target\ntissue", 26, LGREY, line_spacing=0.8).move_to([-5.6, -3.0, 0])
        ngf_pos = [[-6.2, 1.2], [-5.6, 1.5], [-5.0, 1.1], [-6.2, 0.4], [-5.5, 0.6], [-4.95, 0.2], [-6.2, -0.5], [-5.5, -0.3],
                   [-5.0, -0.8], [-6.1, -1.4], [-5.5, -1.2], [-5.0, -1.8]]
        dots = VGroup(*[Dot([x, y, 0], radius=0.17, color=YELLOW) for x, y in ngf_pos])
        ngf_lab = T("NGF", 34, YELLOW, weight=BOLD).move_to([-5.6, 2.0, 0])
        body = neuron(1.8).move_to([4.2, by, 0])
        axon = VGroup(Line([2.4, by, 0], [-3.3, by, 0], color=BLUE, stroke_width=7),
                      Line([-3.3, by, 0], [-4.2, by + 1.9, 0], color=BLUE, stroke_width=6),
                      Line([-3.3, by, 0], [-4.2, by, 0], color=BLUE, stroke_width=6),
                      Line([-3.3, by, 0], [-4.2, by - 1.9, 0], color=BLUE, stroke_width=6))
        tips = VGroup(*[Dot([-4.2, by + dy, 0], radius=0.2, color=BLUE) for dy in (1.9, 0, -1.9)])
        nlab = T("sympathetic neuron", 28, BLUE).move_to([4.2, by - 2.6, 0])
        xs = (-4.3, -2.7, -1.1, 0.5)
        boxes = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.12, width=1.0, height=1.0, stroke_color=TEAL, stroke_width=3),
                                T("?", 40, TEAL)).move_to([x, 3.1, 0]) for x in xs])
        for b in boxes:
            b[1].move_to(b[0])
        row_arr = VGroup(*[arr([x + 0.58, 3.1, 0], [x + 1.02, 3.1, 0], GREY, 4, 0.18) for x in xs[:3]])
        killers = bchip("killers", RED, 32).move_to([3.3, 3.1, 0])
        k_arr = arr([1.15, 3.1, 0], [2.05, 3.1, 0], GREY, 4, 0.18)
        cross = xmark([-5.6, -0.15, 0], 1.0, RED, 10)

        self.play(FadeIn(tissue), FadeIn(tlab), FadeIn(dots), FadeIn(ngf_lab), run_time=0.4)
        self.at("neuron")
        self.play(Create(axon), FadeIn(tips), FadeIn(body), FadeIn(nlab), run_time=0.7)
        self.at("loses its")
        self.play(Create(cross), *[d.animate.set_opacity(0.3) for d in dots], run_time=0.8)
        self.at("step by step")
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in boxes], lag_ratio=0.25), FadeIn(row_arr), run_time=1.0)
        self.at("before the killers")
        self.play(FadeIn(k_arr), FadeIn(killers, shift=LEFT * 0.2), run_time=0.5)
        self.at("switch on")
        self.play(*litchip(killers, RED), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02(SpokenScene):
    """the worm pathway: EGL-1 takes the brake off the killers"""

    def construct(self):
        worm = ParametricFunction(lambda t: np.array([3.5 + t, 3.1 + 0.18 * np.sin(t * 3.2), 0]), t_range=[0, 2.6, 0.03],
                                  color=LGREY, stroke_width=12)
        head = Dot([3.5 + 2.6, 3.1 + 0.18 * np.sin(2.6 * 3.2), 0], radius=0.19, color=LGREY)
        wlab = T("worm", 32, LGREY).move_to([2.2, 3.1, 0])
        c4 = bchip("CED-4", PURPLE, 46).move_to([-3.4, -1.5, 0])
        c3 = bchip("CED-3", RED, 46).move_to([3.4, -1.5, 0])
        c9 = bchip("CED-9", GREEN, 46).move_to([0.0, 1.0, 0])
        b4 = inhib([-0.7, 0.45, 0], c4.get_top() + [0.1, 0.05, 0], GREEN, 8)
        b3 = inhib([0.7, 0.45, 0], c3.get_top() + [-0.1, 0.05, 0], GREEN, 8)
        brake = T("brake", 34, GREEN).move_to([0.0, -0.45, 0])
        egl = bchip("EGL-1", ORANGE, 46).move_to([-4.7, 1.0, 0])
        e_arrow = inhib([-3.2, 1.0, 0], [-1.65, 1.0, 0], ORANGE, 9)
        kbr = Brace(VGroup(c4, c3), DOWN, color=RED, buff=0.25)
        klab = T("the killers", 34, RED).next_to(kbr, DOWN, buff=0.12)

        self.at("worm")
        self.play(Create(worm), FadeIn(head), FadeIn(wlab), run_time=0.7)
        self.play(FadeIn(c4, shift=UP * 0.2), FadeIn(c3, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(c9, shift=DOWN * 0.2), Create(b4), Create(b3), FadeIn(brake), run_time=0.7)
        self.at("there")
        self.play(FadeIn(egl, shift=RIGHT * 0.3), run_time=0.35)
        self.at("EGL")
        self.play(Create(e_arrow), run_time=0.6)
        self.at("takes the")
        self.play(FadeOut(b4), FadeOut(b3), FadeOut(brake), *dimchip(c9, 0.4), run_time=0.9)
        self.at("killers")
        self.play(FadeIn(kbr), FadeIn(klab), *litchip(c4, PURPLE, 0.55), *litchip(c3, RED, 0.55), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
# THE GATE VIEW: a zoomed mitochondrion with its outer membrane across the middle of the frame
# ---------------------------------------------------------------------------------------------
MY = -0.20            # centre of the outer membrane band
BAND = 0.34           # thickness of the membrane band
BAND_TOP = MY + BAND / 2
MBOT = -3.15
MX0, MX1 = -5.9, 5.9  # straight part of the membrane
MR = 0.7
BAX_INS_X = [1.2, 3.7, 5.8]
GL, GR = BAX_INS_X[0] + 0.17, BAX_INS_X[1] - 0.17  # the pore (gap between the first two Bax rods of scene 20)
PORE_X = (GL + GR) / 2
BCL_X, BCL_W, BCL_H = -2.2, 4.16, 2.47
BAX_HELD_X = 1.65


def band_piece(x0, x1, op=0.55):
    return Rectangle(width=x1 - x0, height=BAND, stroke_width=0, fill_color=GREY, fill_opacity=op + 0.1).move_to([(x0 + x1) / 2, MY, 0])


def mito_parts(cyt=True):
    cy = (MY + MBOT) / 2
    fill = RoundedRectangle(corner_radius=MR, width=MX1 - MX0 + 2 * MR, height=MY - MBOT, stroke_width=0,
                            fill_color=GREY, fill_opacity=0.15).move_to([0, cy, 0])
    out = VGroup(
        Arc(radius=MR, start_angle=PI / 2, angle=-PI / 2, arc_center=[MX1, MY - MR, 0]),
        Line([MX1 + MR, MY - MR, 0], [MX1 + MR, MBOT + MR, 0]),
        Arc(radius=MR, start_angle=0, angle=-PI / 2, arc_center=[MX1, MBOT + MR, 0]),
        Line([MX1, MBOT, 0], [MX0, MBOT, 0]),
        Arc(radius=MR, start_angle=-PI / 2, angle=-PI / 2, arc_center=[MX0, MBOT + MR, 0]),
        Line([MX0 - MR, MBOT + MR, 0], [MX0 - MR, MY - MR, 0]),
        Arc(radius=MR, start_angle=PI, angle=-PI / 2, arc_center=[MX0, MY - MR, 0]),
    ).set_stroke(GREY, width=5)
    memL, memP, memR = band_piece(MX0, GL), band_piece(GL, GR), band_piece(GR, MX1)
    mem = VGroup(memL, memP, memR)
    pos1 = [(x, -1.25) for x in (-4.5, -1.5, 1.5, 4.5)]
    pos2 = [(x, -2.05) for x in (-3.0, 0.0, 3.0)]
    dots = VGroup(*[Dot([x, y, 0], radius=0.22, color=PINK) for x, y in pos1 + pos2])
    mlab = T("mitochondrion", 28, LGREY).move_to([-4.0, -3.55, 0])
    clab = T("cytochrome c", 28, PINK).move_to([2.0, -3.55, 0])
    P = dict(fill=fill, out=out, mem=mem, memL=memL, memP=memP, memR=memR, dots=dots, mlab=mlab, clab=clab)
    return P


def cyto_field():
    return Ellipse(width=16.0, height=9.6, stroke_width=0, fill_color=BLUE, fill_opacity=0.07).move_to([0, 0.3, 0])


def bcl_block(label="Bcl-2", label_size=36, x=BCL_X, w=BCL_W, h=BCL_H):
    body = notched(w, h, GREEN)
    lab = T(label, label_size, GREEN, weight=BOLD).move_to([0, -0.15, 0])
    g = VGroup(body, lab)
    g.body, g.lab = body, lab
    g.move_to([x, BAND_TOP + h / 2, 0])
    g.top = BAND_TOP + h
    return g


def bax_cartoon(s=1.0, label="Bax", color=ORANGE, fill=0.25):
    """inactive Bax: a notched block with its last helix tucked in the groove (3.0 x 1.9 at s=1), centred at the origin"""
    w, h, nd = 3.4, 2.1, 0.55
    body = notched(w, h, color, nd=nd, fill=fill)
    rod = rod_at(0, h / 2 - nd + 0.18, w=1.5, h=0.32)
    lab = T(label, 52, color, weight=BOLD).move_to([0, -0.25, 0])
    g = VGroup(body, lab, rod)
    g.body, g.lab, g.rod = body, lab, rod
    g.scale(s)
    return g


def hold_bar(x=-0.12, y=0.55):
    return VGroup(Line([x - 0.2, y, 0], [x, y, 0], color=GREEN, stroke_width=9),
                  Line([x, y - 0.45, 0], [x, y + 0.45, 0], color=GREEN, stroke_width=9))


def held_bax():
    b = bax_cartoon(0.90)
    b.move_to([BAX_HELD_X, BAND_TOP + b.body.height / 2, 0])
    return b


def inserted_bax(x, label=True):
    block = RoundedRectangle(corner_radius=0.14, width=1.95, height=1.24, stroke_color=ORANGE, stroke_width=3,
                             fill_color=ORANGE, fill_opacity=0.5).move_to([x, 0.95, 0])
    rod = RoundedRectangle(corner_radius=0.08, width=0.44, height=0.88, stroke_color=ORANGE, stroke_width=3,
                           fill_color=ORANGE, fill_opacity=0.95).move_to([x, MY + 0.20, 0])
    lab = T("Bax", 39, ORANGE, weight=BOLD).move_to([x, 0.95, 0])
    g = VGroup(rod, block, lab)
    g.block, g.rod, g.lab = block, rod, lab
    return g


FINALS = [(0.5, 1.9), (1.9, 1.9), (3.3, 1.9), (4.7, 1.9), (1.2, 2.55), (2.6, 2.55), (4.0, 2.55)]
CYT_LAB_GATE = np.array([-3.4, 2.85, 0.0])


def gate_closed_group():
    """Bcl-2 on the membrane holding Bax shut beside it"""
    return bcl_block(), held_bax(), hold_bar()


def gate_label():
    br = Line([4.7, 2.65, 0], [0.2, 2.3, 0], color=WHITE, stroke_width=3)
    lab = T("gate", 38, WHITE, weight=BOLD).move_to([5.55, 2.65, 0])
    return br, lab


# ---------------------------------------------------------------------------------------------
class S03(SpokenScene):
    """the neuron's brake works one step earlier, as a gate at the mitochondria, which store cytochrome c"""

    def construct(self):
        cyto = cyto_field()
        cl = cell()
        cy_lab = T("inside the neuron", 34, BLUE).move_to([0.0, 2.45, 0])
        brake = bchip("brake", GREEN, 64).move_to([0.0, 0.3, 0])
        M = mito_parts()
        bcl, bax, hb = gate_closed_group()
        br, glab = gate_label()
        mito = VGroup(M["fill"], M["out"], M["mem"], M["dots"])

        self.play(FadeIn(cl), FadeIn(cy_lab), run_time=0.4)
        self.at("break")
        self.play(FadeIn(brake, shift=DOWN * 0.2), run_time=0.5)
        self.at("one step earlier")
        self.play(brake.animate.move_to([-0.45, 0.9, 0]).scale(0.6), run_time=0.8)
        self.at("gate")
        self.play(FadeOut(cl), FadeOut(cy_lab), FadeIn(cyto), FadeIn(mito), FadeIn(bcl), FadeIn(bax), FadeIn(hb), FadeIn(br), ReplacementTransform(brake, glab), run_time=0.5)
        self.at("mitochondria")
        self.play(FadeIn(M["mlab"]), run_time=0.4)
        self.at("cytochrome")
        self.play(FadeIn(M["clab"]), Indicate(M["dots"], color=PINK, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04(SpokenScene):
    """Step 1: the survival signal falls"""

    def construct(self):
        tr = tracker()
        frame = Rectangle(width=1.8, height=5.3, stroke_color=GREY, stroke_width=3).move_to([-3.4, -0.25, 0])
        level, bar = vbar(-3.4, -2.9, 1.8, YELLOW, 5.2)
        lab = T("survival signal", 32, YELLOW).move_to([-3.4, -3.45, 0])
        n = neuron(1.5).move_to([3.3, -0.5, 0])
        dots = VGroup(*[Dot([3.3 + 2.4 * np.cos(a), -0.5 + 2.15 * np.sin(a), 0], radius=0.17, color=YELLOW)
                        for a in np.linspace(0, TAU, 12, endpoint=False) + 0.2])
        nlab = T("NGF", 32, YELLOW, weight=BOLD).move_to([3.3, 2.55, 0])
        self.add(tr)
        self.at("step")
        self.play(*tset(tr, 0, "lit", True), Flash(tr.items[0][0].get_center(), color=TEXT, flash_radius=0.55, line_length=0.18),
                  FadeIn(frame), FadeIn(bar), FadeIn(n), FadeIn(dots), FadeIn(nlab), run_time=0.8)
        self.at("survival signal")
        self.play(FadeIn(lab), run_time=0.5)
        self.at("falls")
        self.play(level.animate.set_value(0.35), *[d.animate.set_opacity(0.12) for d in dots], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def terminal_scene():
    """tissue + axon + cell body of the neuron, as used in s05; returns a dict of parts"""
    P = {}
    by = -0.3
    P["by"] = by
    P["tissue"] = RoundedRectangle(corner_radius=0.3, width=2.3, height=6.0, stroke_color=GREY, stroke_width=3,
                                   fill_color=GREY, fill_opacity=0.12).move_to([-5.6, by, 0])
    P["body"] = neuron(1.8).move_to([4.2, by, 0])
    P["axon"] = VGroup(Line([2.4, by, 0], [-3.2, by, 0], color=BLUE, stroke_width=7),
                       Line([-3.2, by, 0], [-4.2, by + 1.9, 0], color=BLUE, stroke_width=6),
                       Line([-3.2, by, 0], [-4.2, by, 0], color=BLUE, stroke_width=6),
                       Line([-3.2, by, 0], [-4.2, by - 1.9, 0], color=BLUE, stroke_width=6))
    P["tips"] = VGroup(*[Dot([-4.2, by + dy, 0], radius=0.2, color=BLUE) for dy in (1.9, 0, -1.9)])
    P["cups"] = VGroup(*[Arc(radius=0.4, start_angle=-PI / 2, angle=PI, color=WHITE, stroke_width=7).move_to([-4.4, by + dy, 0])
                         for dy in (1.9, 0, -1.9)])
    P["tlab"] = T("target", 28, LGREY).move_to([-5.6, -2.85, 0])
    return P


TAG_POS = [0.3, 2.55, 0]


class S05(SpokenScene):
    """NGF from the target acts through TrkA on the axon terminals"""

    def construct(self):
        P = terminal_scene()
        by = P["by"]
        tr = tracker(("lit", "hidden", "hidden", "hidden"))
        pos = [[-6.2, 1.9], [-5.6, 1.3], [-5.0, 1.9], [-6.2, 0.7], [-5.5, 0.4], [-5.0, 0.9],
               [-6.2, -0.3], [-5.5, -0.8], [-5.0, -0.4], [-6.2, -1.4], [-5.5, -1.8], [-5.0, -1.3]]
        dots = VGroup(*[Dot([x, y, 0], radius=0.17, color=YELLOW) for x, y in pos])
        ngf_lab = T("NGF", 34, YELLOW, weight=BOLD).move_to([-5.6, 2.45, 0])
        tag = T("normally, with NGF", 28, YELLOW).move_to(TAG_POS)
        trk = T("TrkA", 34, WHITE, weight=BOLD).move_to([-2.0, by + 2.3, 0])
        trk_ln = Line([-2.65, by + 2.2, 0], [-4.3, by + 2.3, 0], color=WHITE, stroke_width=3)
        trk_ln = Line([-2.7, by + 2.18, 0], [-4.3, by + 2.38, 0], color=WHITE, stroke_width=3)
        term = T("axon terminals", 28, BLUE).move_to([-1.6, by - 2.55, 0])
        term_ln = Line([-2.85, by - 2.4, 0], [-4.15, by - 2.15, 0], color=BLUE, stroke_width=3)
        self.add(tr, P["tissue"], P["body"], P["axon"], P["tips"])
        self.play(FadeIn(dots), FadeIn(ngf_lab), FadeIn(tag), run_time=0.6)
        self.at("from the target")
        self.play(FadeIn(P["tlab"]), run_time=0.5)
        self.at("acts through")
        self.play(dots[2].animate.move_to([-4.8, by + 1.9, 0]), dots[8].animate.move_to([-4.8, by, 0]),
                  dots[11].animate.move_to([-4.8, by - 1.9, 0]), run_time=0.9)
        self.at("receptor")
        self.play(FadeIn(P["cups"]), run_time=0.5)
        self.play(dots[2].animate.move_to([-4.7, by + 1.9, 0]), dots[8].animate.move_to([-4.7, by, 0]),
                  dots[11].animate.move_to([-4.7, by - 1.9, 0]), run_time=0.5)
        self.at("Track A")
        self.play(FadeIn(trk), Create(trk_ln), run_time=0.5)
        self.at("terminals")
        self.play(FadeIn(term), Create(term_ln), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
AKT_P = np.array([-3.6, 0.0, 0.0])
BLOB_X = -0.4
BLOB_Y = (1.5, 0.0, -1.5)


def interior_s06():
    """the cell body with Akt holding three pro-death proteins; returns dict"""
    D = {}
    D["cell"] = cell()
    D["sig"] = bchip("NGF signal", YELLOW, 30).move_to([-3.6, 1.85, 0])
    D["akt"] = bchip("Akt", YELLOW, 56).move_to(AKT_P)
    D["glow"] = Circle(radius=1.15, stroke_width=0, fill_color=YELLOW, fill_opacity=0.22).move_to(D["akt"])
    D["s_a"] = arr(D["sig"].get_bottom(), D["akt"].get_top() + UP * 0.08, YELLOW, 6)
    D["blobs"] = VGroup(*[Circle(radius=0.55, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.35).move_to([BLOB_X, y, 0])
                          for y in BLOB_Y])
    D["bars"] = VGroup(*[inhib([-2.55, y * 0.3, 0], [BLOB_X - 0.62, y, 0], YELLOW, 7) for y in BLOB_Y])
    D["plab"] = T("pro-death proteins", 30, ORANGE).move_to([BLOB_X, -2.75, 0])
    D["tag"] = T("normally, with NGF", 28, YELLOW).move_to(TAG_POS)
    return D


class S06(SpokenScene):
    """the signal keeps Akt active; Akt holds back several pro-death proteins (zoom into the cell body)"""

    def construct(self):
        P = terminal_scene()
        tr = tracker(("lit", "hidden", "hidden", "hidden"))
        D = interior_s06()
        tag = T("normally, with NGF", 28, YELLOW).move_to(TAG_POS)
        dots = VGroup(*[Dot([-5.6 + dx, y, 0], radius=0.17, color=YELLOW) for dx, y in [(-0.5, 1.9), (0.0, 1.3), (-0.4, 0.7), (0.1, 0.4), (-0.5, -0.3), (0.2, -0.8)]])
        dots.add(*[Dot([-4.7, P["by"] + dy, 0], radius=0.17, color=YELLOW) for dy in (1.9, 0, -1.9)])
        old = VGroup(P["tissue"], P["axon"], P["tips"], P["cups"], P["tlab"], dots)
        self.add(tr, old, P["body"], tag)

        self.at("signal keeps")
        self.play(FadeOut(old), FadeTransform(P["body"], D["cell"]), run_time=1.2)
        self.play(FadeIn(D["sig"], shift=DOWN * 0.15), run_time=0.4)
        self.at("such as")
        self.play(FadeIn(D["akt"]), GrowArrow(D["s_a"]), run_time=0.6)
        self.play(FadeIn(D["glow"]), run_time=0.5)
        self.at("holds back")
        self.play(FadeIn(D["blobs"], lag_ratio=0.2), run_time=0.6)
        self.play(*[Create(b) for b in D["bars"]], run_time=0.6)
        self.at("proteins")
        self.play(FadeIn(D["plab"]), run_time=0.5)
        self.finish()


FREED = [(0.45, 1.5), (1.25, 0.0), (0.45, -1.5)]


class S07(SpokenScene):
    """without NGF the restraint weakens; Akt dims and the proteins are freed"""

    def construct(self):
        D = interior_s06()
        tr = tracker(("lit", "hidden", "hidden", "hidden"))
        tag2 = T("without NGF", 28, RED).move_to(TAG_POS)
        self.add(tr, D["cell"], D["sig"], D["akt"], D["glow"], D["s_a"], D["blobs"], D["bars"], D["plab"], D["tag"])
        self.play(FadeOut(D["sig"]), FadeOut(D["s_a"]), ReplacementTransform(D["tag"], tag2),
                  D["glow"].animate.set_opacity(0), *dimchip(D["akt"], 0.35), FadeOut(D["bars"]), run_time=1.3)
        self.at("restraint")
        self.play(*[b.animate.move_to([x, y, 0]).set_fill(ORANGE, 0.7) for b, (x, y) in zip(D["blobs"], FREED)], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def s07_end_parts():
    D = interior_s06()
    for b, (x, y) in zip(D["blobs"], FREED):
        b.move_to([x, y, 0]).set_fill(ORANGE, 0.7)
    D["akt"][1].set_stroke(opacity=0.35).set_fill(opacity=0.056)
    D["akt"][2].set_opacity(0.35)
    D["tag"] = T("without NGF", 28, RED).move_to(TAG_POS)
    return D


class S08(SpokenScene):
    """Step 2: pro-death genes are switched on (the freed proteins arrive at the nucleus; the genes are still off)"""

    def construct(self):
        D = s07_end_parts()
        tr = tracker(("lit", "hidden", "hidden", "hidden"))
        nuc = nucleus()
        self.add(tr, D["cell"], D["akt"], D["blobs"], D["plab"], D["tag"])
        self.at("step")
        self.play(*light(tr, 1), FadeIn(nuc.shell), FadeIn(nuc.lab), FadeOut(D["plab"]), FadeOut(D["tag"]),
                  *[b.animate.move_to(p) for b, p in zip(D["blobs"], [[1.7, 0.6, 0], [3.0, 0.2, 0], [4.3, 0.6, 0]])], run_time=1.4)
        self.at("genes")
        self.play(FadeIn(nuc.dna), FadeIn(nuc.genes), FadeIn(nuc.glab), run_time=0.6)
        self.at("switched on")
        self.play(*[Indicate(g, color=TEAL, scale_factor=1.15) for g in nuc.genes], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
JNK_P = np.array([-3.6, -0.5, 0.0])


def jnk_chip(active=False, size=54):
    j = bchip("JNK", WHITE if active else GREY, size)
    if active:
        j[1].set_stroke(WHITE).set_fill(WHITE, 0.92)
        j[2].set_color(BG)
    return j


def jnk_on(j):
    return [j[1].animate.set_stroke(WHITE, opacity=1).set_fill(WHITE, 0.92), j[2].animate.set_color(BG).set_opacity(1)]


class S09(SpokenScene):
    """a stress pathway turns on; the kinase JNK becomes active"""

    def construct(self):
        tr = tracker(("lit", "lit", "hidden", "hidden"))
        cl = cell()
        nuc = nucleus()
        stress = bchip("stress pathway", GREY, 32).move_to([-3.6, 1.8, 0])
        jnk = jnk_chip(False).move_to(JNK_P)
        glow = Circle(radius=1.15, stroke_width=0, fill_color=WHITE, fill_opacity=0.0).move_to(JNK_P)
        a = arr(stress.get_bottom(), jnk.get_top(), WHITE, 6)
        self.add(tr, cl, nuc)
        self.at("stress pathway")
        self.play(FadeIn(stress, shift=DOWN * 0.15), run_time=0.6)
        self.at("turns on")
        self.play(*litchip(stress, WHITE, 0.3), Flash(stress.get_center(), color=WHITE, flash_radius=1.0, run_time=0.8))
        self.at("kinase")
        self.add(glow)
        self.play(GrowArrow(a), FadeIn(jnk, shift=DOWN * 0.15), run_time=0.6)
        self.at("becomes active")
        self.play(*jnk_on(jnk), glow.animate.set_fill(WHITE, 0.3), Flash(jnk.get_center(), color=WHITE, flash_radius=1.4, run_time=0.8))
        self.finish()


TF_P = np.array([3.0, 0.45, 0.0])
JNK10 = np.array([-1.8, 0.45, 0.0])


class S10(SpokenScene):
    """JNK adds phosphates to a transcription factor called c-Jun"""

    def construct(self):
        tr = tracker(("lit", "lit", "hidden", "hidden"))
        cl = cell()
        nuc = nucleus()
        nuc.glab.set_opacity(1)
        jnk = jnk_chip(True, 54).move_to(JNK_P)
        glow = Circle(radius=1.2, stroke_width=0, fill_color=WHITE, fill_opacity=0.3).move_to(JNK_P)
        stress = bchip("stress pathway", WHITE, 32).move_to([-3.6, 1.8, 0])
        stress[1].set_stroke(WHITE).set_fill(WHITE, 0.3)
        stress[2].set_color(WHITE)
        tf = bchip("transcription factor", TEAL, 26).move_to(TF_P)
        cj = bchip("c-Jun", TEAL, 44).move_to(TF_P)
        self.add(tr, cl, nuc, glow, jnk, stress)
        self.at("JNK adds")
        self.play(jnk.animate.scale(0.8).move_to(JNK10), glow.animate.scale(0.8).move_to(JNK10), FadeOut(stress), run_time=0.7)
        self.at("phosphates")
        ps = VGroup(*[VGroup(Circle(radius=0.3, stroke_color=WHITE, stroke_width=3, fill_color=BG, fill_opacity=1),
                             T("P", 26, WHITE, weight=BOLD)) for _ in range(3)])
        for p_ in ps:
            p_[1].move_to(p_[0])
            p_.move_to(JNK10 + [1.0, 0, 0])
        self.add(ps)
        mids = [[2.2, 1.3], [3.0, 1.3], [3.8, 1.3]]
        self.play(LaggedStart(*[p_.animate.move_to([x, y, 0]) for p_, (x, y) in zip(ps, mids)], lag_ratio=0.3), run_time=0.8)
        self.at("transcription factor")
        spots = [[2.2, 1.3], [3.0, 1.3], [3.8, 1.3]]
        connection = arr(JNK10 + [0.9, 0, 0], tf.get_left(), WHITE, 5)
        self.play(FadeIn(tf), GrowArrow(connection), *[p_.animate.move_to([x, y, 0]) for p_, (x, y) in zip(ps, spots)], run_time=0.8)
        self.at("called")
        self.play(ReplacementTransform(tf, cj), *[p_.animate.move_to([x, 1.3, 0]) for p_, x in zip(ps, (2.2, 3.0, 3.8))], run_time=0.6)
        self.wait(0.2)
        self.play(*genes_lit(nuc), Flash(nuc.genes.get_center(), color=TEAL, flash_radius=1.4, run_time=0.8), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S11(SpokenScene):
    """c-Jun rises in deprived neurons; blocking it protects them"""

    def construct(self):
        tr = tracker(("lit", "lit", "hidden", "hidden"))
        sep = DashedLine([0.5, 2.7, 0], [0.5, -3.6, 0], color=GREY, stroke_width=2)
        bx = -3.9
        base = -2.9
        frame = Rectangle(width=1.9, height=5.0, stroke_color=GREY, stroke_width=3).move_to([bx, base + 2.5, 0])
        level, bar = vbar(bx, base, 1.9, TEAL, 0.55)
        lab = T("c-Jun", 40, TEAL, weight=BOLD).move_to([bx, 2.6, 0])
        axis = T("level (relative)", 26, LGREY).rotate(PI / 2).move_to([bx - 1.5, base + 2.5, 0])
        ref = DashedLine([bx - 1.1, base + 0.55, 0], [bx + 2.2, base + 0.55, 0], color=LGREY, stroke_width=3)
        refl = T("with NGF", 26, LGREY).move_to([bx + 3.0, base + 0.55 + 0.0, 0])
        dep = T("deprived neurons", 30, LGREY).move_to([bx + 0.3, -3.5, 0])
        cx = 3.9
        cj = bchip("c-Jun", TEAL, 40).move_to([cx, 2.45, 0])
        xm = xmark(cj.get_center(), 0.6, RED, 9)
        n = neuron(1.7).move_to([cx, -0.05, 0])
        cond = T("no NGF, c-Jun blocked", 28, LGREY).move_to([cx, -2.35, 0])
        ok = T("survives", 44, GREEN, weight=BOLD).move_to([cx, -3.2, 0])
        self.add(tr)
        self.play(FadeIn(frame), FadeIn(bar), FadeIn(lab), FadeIn(axis), FadeIn(ref), FadeIn(refl), run_time=0.5)
        self.at("rises")
        self.play(level.animate.set_value(4.4), run_time=0.8)
        self.at("deprived")
        self.play(FadeIn(dep), run_time=0.5)
        self.at("blocking")
        self.play(FadeIn(sep), FadeIn(cj), FadeIn(n), FadeIn(cond), run_time=0.5)
        self.at("its function")
        self.play(Create(xm), run_time=0.5)
        self.at("protects")
        self.play(FadeIn(ok, shift=UP * 0.15), Flash(n.get_center(), color=GREEN, flash_radius=1.9, run_time=0.8))
        self.finish()


# ---------------------------------------------------------------------------------------------
def ribosome(x, y, s=1.0):
    g = VGroup(Ellipse(width=1.5, height=0.8, stroke_width=0, fill_color=LGREY, fill_opacity=0.9).move_to([x, y - 0.28, 0]),
               Ellipse(width=1.05, height=0.58, stroke_width=0, fill_color=LGREY, fill_opacity=0.9).move_to([x, y + 0.18, 0]))
    return g.scale(s)


class S12(SpokenScene):
    """BH3-only proteins such as Bim: transcripts leave the nucleus through the pore, ribosomes make Bim protein"""

    def construct(self):
        tr = tracker(("lit", "lit", "hidden", "hidden"))
        cl = cell()
        nuc = nucleus()
        for gx in nuc.genes:
            gx.set_fill(TEAL, 0.7)
        ribos = VGroup(ribosome(-4.8, -0.7), ribosome(-3.2, -1.3), ribosome(-3.7, -0.1, 1.0))
        rlab = T("ribosomes", 28, LGREY).move_to([-3.5, -2.45, 0])
        bh3 = T("BH3-only proteins", 28, ORANGE).move_to([-2.3, 2.1, 0])
        bim = T("Bim", 44, ORANGE, weight=BOLD).move_to([-2.9, 1.35, 0])
        self.add(tr, cl, nuc)
        self.play(FadeIn(ribos), FadeIn(rlab), run_time=0.4)
        self.at("genes then")
        trs = [wiggle(1.3 + 0.2 * i, GENE_Y + 0.7, 0.9) for i in range(3)]
        targets = [[-3.3, -0.35], [-4.0, -1.0], [-2.7, -0.9]]
        anims = []
        for i, t in enumerate(trs):
            self.add(t)
            path = VMobject().set_points_as_corners([t.get_center(), [1.1, -0.35, 0],
                [PORE[0], PORE[1], 0], [-0.3, -0.35, 0], [*targets[i], 0]])
            anims.append(MoveAlongPath(t, path, rate_func=linear))
        self.play(LaggedStart(*anims, lag_ratio=0.12), run_time=1.4)
        self.at("BH3")
        self.play(FadeIn(bh3), run_time=0.5)
        self.at("such as")
        prot = VGroup(*[Circle(radius=0.42, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.5).move_to([x, 0.55, 0])
                        for x in (-3.9, -2.9, -1.9)])
        self.play(FadeOut(VGroup(*trs)), FadeIn(prot, shift=UP * 0.8, lag_ratio=0.15), FadeIn(bim), run_time=0.30)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S13(SpokenScene):
    """the new gene expression the 1988 drugs blocked (callback to the delayed death of chapter 1)"""

    def construct(self):
        tr = tracker(("lit", "lit", "hidden", "hidden"))
        cj = bchip("c-Jun", TEAL, 38).move_to([-2.6, 2.45, 0])
        bim = bchip("Bim", ORANGE, 38).move_to([0.6, 2.45, 0])
        ca = arr(cj.get_right(), bim.get_left(), TEAL, 6)
        br = Brace(VGroup(cj, bim), DOWN, color=TEAL, buff=0.15)
        brl = T("new gene expression", 34, TEAL).next_to(br, DOWN, buff=0.1)
        drug = bchip("1988 drugs", TEAL, 34).move_to([4.25, 2.4, 0])
        dbar = inhib(drug.get_bottom(), br.get_right() + [0.05, 0, 0], TEAL, 7)
        ya, yb = -0.65, -2.35
        na = neuron(0.65).move_to([-5.8, ya, 0])
        nb = neuron(0.65).move_to([-5.8, yb, 0])
        ta = Arrow([-4.8, ya, 0], [6.4, ya, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        tb = Arrow([-4.8, yb, 0], [6.4, yb, 0], buff=0, color=GREY, stroke_width=5, tip_length=0.25)
        la = T("NGF removed", 28, LGREY).move_to([-3.0, ya + 0.5, 0])
        lb = T("NGF removed + 1988 drugs", 28, TEAL).move_to([-1.5, yb + 0.5, 0])
        tl = T("time after NGF removal", 26, LGREY).move_to([-1.0, yb - 1.1, 0])
        ma = Dot([-4.5, ya, 0], radius=0.19, color=TEXT)
        mb = Dot([-4.5, yb, 0], radius=0.19, color=TEXT)
        xa, xb = -0.7, 3.9
        ticks = VGroup(Line([xa, ya - 0.25, 0], [xa, ya + 0.25, 0], color=RED, stroke_width=6),
                       Line([xb, yb - 0.25, 0], [xb, yb + 0.25, 0], color=RED, stroke_width=6))
        da = T("neuron dies", 26, RED).move_to([xa, ya - 0.55, 0])
        db_ = T("neuron dies (delayed)", 26, RED).move_to([xb - 0.4, yb - 0.55, 0])
        self.add(tr, cj, bim, ca)
        self.play(FadeIn(na), FadeIn(nb), Create(ta), Create(tb), FadeIn(la), FadeIn(lb),
                  FadeIn(ma), FadeIn(mb), FadeIn(tl), Create(ticks), FadeIn(da), FadeIn(db_), run_time=0.6)
        self.at("new gene expression")
        self.play(Create(br), FadeIn(brl), run_time=0.55)
        self.at("1988")
        self.play(FadeIn(drug), Create(dbar), run_time=0.55)
        self.at("blocked")
        self.play(ma.animate.move_to([xa, ya, 0]).set_color(RED),
                  mb.animate.move_to([xb, yb, 0]).set_color(RED), run_time=0.8, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class GateScene(SpokenScene):
    """base: builds the stage (cytoplasm field, mitochondrion, cytochrome c) so the scenes stay short"""

    def stage(self, tr_states=("lit", "lit", "lit", "hidden"), labels=True):
        self.tr = tracker(tr_states)
        self.cyto = cyto_field()
        self.M = mito_parts()
        M = self.M
        self.add(self.tr, self.cyto, M["fill"], M["out"], M["mem"], M["dots"])
        if labels:
            self.add(M["mlab"], M["clab"])
        return M


class S14(GateScene):
    """Step 3: the gate opens (marker lights; the closed gate pulses)"""

    def construct(self):
        M = self.stage(("lit", "lit", "hidden", "hidden"))
        bcl, bax, hb = gate_closed_group()
        br, glab = gate_label()
        self.add(bcl, bax, hb, br, glab)
        self.at("step")
        self.play(*light(self.tr, 2), run_time=0.8)
        self.at("gate opens")
        self.play(Indicate(glab, color=WHITE, scale_factor=1.3), Indicate(bax, color=ORANGE, scale_factor=1.06),
                  Flash(bax.get_center(), color=WHITE, flash_radius=1.6, run_time=0.9), run_time=0.9)
        self.finish()


class S15(GateScene):
    """a BH3 domain is a short helix that fits a groove on protective proteins such as Bcl-2"""

    def construct(self):
        M = self.stage()
        bcl = bcl_block("", 36)
        plabel = T("protective\nprotein", 30, GREEN, line_spacing=0.8).move_to([BCL_X, BAND_TOP + 0.62, 0])
        bax = held_bax()
        bax.set_opacity(0.45)
        hb = hold_bar()
        groove_y = bcl.top - 0.45
        rod = rod_at(BCL_X, 2.45)
        rlab = T("BH3 domain", 32, ORANGE).move_to([1.5, 2.45, 0])
        hlab = T("a short helix", 28, ORANGE).move_to([1.5, 2.0, 0])
        gl = T("groove", 30, WHITE).move_to([1.3, 2.0, 0])
        gla = arr([0.55, 1.92, 0], [BCL_X + 0.9, groove_y + 0.12, 0], WHITE, 4, 0.18)
        self.add(bcl, bax, hb)
        self.play(FadeIn(rod, shift=DOWN * 0.2), FadeIn(rlab), run_time=0.6)
        self.at("short helix")
        self.play(FadeIn(hlab), run_time=0.5)
        self.at("fits")
        self.play(rod.animate.move_to([BCL_X, groove_y + 0.17, 0]), FadeOut(rlab), FadeOut(hlab), run_time=0.5)
        self.at("groove")
        self.play(FadeIn(gl), GrowArrow(gla), run_time=0.4)
        self.at("protective")
        self.play(FadeIn(plabel), run_time=0.3)
        self.at("such as")
        newlab = T("Bcl-2", 42, GREEN, weight=BOLD).move_to(plabel)
        self.play(ReplacementTransform(plabel, newlab), run_time=0.5)
        self.finish()


class S16(SpokenScene):
    """the same in the worm: EGL-1 in the CED-9 groove (no mitochondrion, no gate)"""

    def construct(self):
        tr = tracker(("lit", "lit", "lit", "hidden"))
        cx, cy = -0.8, -0.85
        blk = notched(5.4, 3.4, GREEN, nd=0.85)
        blk.move_to([cx, cy, 0])
        groove_y = cy + 1.7 - 0.85
        rod = rod_at(cx, 2.15, w=2.6, h=0.5)
        egl = T("EGL-1", 46, ORANGE, weight=BOLD).move_to([cx + 3.6, 2.15, 0])
        ced = T("CED-9", 60, GREEN, weight=BOLD).move_to([cx, cy - 0.5, 0])
        wlab = T("in the worm", 38, LGREY, weight=BOLD).move_to([cx, -3.3, 0])
        self.add(tr, blk)
        self.play(FadeIn(rod, shift=DOWN * 0.2), run_time=0.4)
        self.at("EGL")
        self.play(FadeIn(egl), run_time=0.4)
        self.at("does to")
        self.play(rod.animate.move_to([cx, groove_y + 0.27, 0]), Indicate(blk, color=GREEN, scale_factor=1.03), run_time=0.7)
        self.at("SED")
        self.play(FadeIn(ced), run_time=0.4)
        self.at("in the worm")
        self.play(FadeIn(wlab), run_time=0.5)
        self.finish()


class S17(GateScene):
    """filled grooves can no longer hold Bax back; Bim can also activate Bax directly"""

    def construct(self):
        M = self.stage()
        bcl = bcl_block("Bcl-2", 40)
        bax = held_bax()
        hb = hold_bar()
        groove_y = bcl.top - 0.45
        rod = rod_at(BCL_X, 2.15)
        bim = T("Bim", 36, ORANGE, weight=BOLD).move_to([BCL_X, 2.7, 0])
        self.add(bcl, bax, hb)
        self.play(FadeIn(bim, shift=DOWN * 0.2), FadeIn(rod, shift=DOWN * 0.2), run_time=0.6)
        self.at("filled grooves")
        self.play(rod.animate.move_to([BCL_X, groove_y + 0.17, 0]), bim.animate.move_to([BCL_X, groove_y + 0.17 + 0.6, 0]), run_time=0.9)
        self.at("can no longer hold")
        self.play(FadeOut(hb), bax.animate.move_to([3.6, 1.6, 0]), run_time=1.0)
        self.at("Bim can also")
        a = arr([BCL_X + 0.8, groove_y + 0.95, 0], [bax.get_left()[0] - 0.05, bax.get_center()[1] + 0.3, 0], ORANGE, 6)
        self.play(GrowArrow(a), run_time=0.8)
        self.at("activate")
        self.play(bax.body.animate.set_fill(ORANGE, 0.6), Flash(bax.get_center(), color=ORANGE, flash_radius=1.8, run_time=0.8))
        self.finish()


class S18(GateScene):
    """inactive Bax sits in the cytoplasm, with its last helix tucked into its own groove"""

    def construct(self):
        M = self.stage()
        bcl = bcl_block("Bcl-2", 40)
        bcl_rod = rod_at(BCL_X, bcl.top - 0.45 + 0.17)
        bx = bax_cartoon(0.72)
        bx.move_to([3.6, 1.6, 0])
        bx.body.set_fill(ORANGE, 0.25)
        self.add(bcl, bcl_rod, bx)
        cy = 1.5
        inact = T("inactive", 30, LGREY).move_to([3.6, 0.1, 0])
        cyto = T("cytoplasm", 30, BLUE).move_to([-4.6, 2.75, 0])
        hl = T("last helix", 32, ORANGE).set_opacity(1).move_to([2.4, 2.75, 0])
        gl = T("groove", 30, WHITE).move_to([6.0, 1.95, 0])
        self.play(bx.animate.scale(1 / 0.72).move_to([3.6, cy, 0]), FadeIn(inact), run_time=0.9)
        gt = bx.body.get_top()[1]
        rod_c = bx.rod.get_center()
        l1 = Line(hl.get_bottom(), rod_c + [0, 0.12, 0], color=ORANGE, stroke_width=3)
        l2 = Line([5.55, 1.9, 0], [rod_c[0] + 0.95, gt - 0.15, 0], color=WHITE, stroke_width=3)
        self.at("sits in")
        self.play(FadeIn(cyto), run_time=0.5)
        self.at("last helix")
        self.play(FadeIn(hl), Create(l1), Indicate(bx.rod, color=ORANGE, scale_factor=1.15), run_time=0.7)
        self.at("groove")
        self.play(FadeIn(gl), Create(l2), run_time=0.6)
        self.finish()


class S19(GateScene):
    """active Bax moves to the mitochondria and inserts its helix into the outer membrane"""

    def construct(self):
        M = self.stage()
        bcl = bcl_block("Bcl-2", 40)
        bcl_rod = rod_at(BCL_X, bcl.top - 0.45 + 0.17)
        bx = bax_cartoon(1.0)
        bx.move_to([3.6, 1.5, 0])
        bx.body.set_fill(ORANGE, 0.25)
        inact = T("inactive", 30, LGREY).move_to([3.6, 0.1, 0])
        cyto = T("cytoplasm", 30, BLUE).move_to([-4.6, 2.75, 0])
        self.add(bcl, bcl_rod, bx, inact, cyto)
        act = T("active", 34, ORANGE, weight=BOLD).move_to(inact)
        self.play(FadeTransform(inact, act), bx.body.animate.set_fill(ORANGE, 0.5), bx.rod.animate.shift(UP * 0.6), run_time=0.8)
        self.at("moves to")
        tgt = inserted_bax(BAX_INS_X[0])
        self.play(ReplacementTransform(bx.body, tgt.block), FadeOut(bx.lab), FadeOut(act), FadeIn(tgt.lab),
                  bx.rod.animate.scale(0.7).move_to([BAX_INS_X[0], 1.95, 0]), run_time=1.5)
        self.at("inserts")
        self.play(bx.rod.animate.move_to([BAX_INS_X[0] + 1.2, 0.6, 0]), run_time=0.5)
        self.play(ReplacementTransform(bx.rod, tgt.rod), run_time=0.9)
        self.at("outer membrane")
        om = T("outer membrane", 28, LGREY).move_to([-5.3, 0.95, 0])
        oma = arr([-5.3, 0.6, 0], [-5.3, -0.25, 0], LGREY, 5, 0.2)
        self.play(FadeIn(om), GrowArrow(oma), run_time=0.6)
        self.finish()


class S20(GateScene):
    """several Bax molecules make the membrane leaky; cytochrome c escapes through the gap between them"""

    def construct(self):
        M = self.stage()
        bcl = bcl_block("Bcl-2", 40)
        bcl_rod = rod_at(BCL_X, bcl.top - 0.45 + 0.17)
        b1 = inserted_bax(BAX_INS_X[0])
        self.add(bcl, bcl_rod, b1)
        others = [inserted_bax(x) for x in BAX_INS_X[1:]]
        self.at("other Bax")
        self.play(*[FadeIn(o, shift=DOWN * 1.2) for o in others], run_time=1.0)
        self.at("makes the membrane")
        self.remove(M["mem"])
        self.add(M["memL"], M["memR"])
        gap = Rectangle(width=GR - GL, height=BAND + 0.06, stroke_width=0,
                        fill_color=BG, fill_opacity=1).move_to([PORE_X, MY, 0]).set_z_index(1)
        self.play(FadeIn(gap), run_time=0.5)
        self.at("Cytochrome")
        M["dots"].set_z_index(3)
        order = sorted(range(len(FINALS)), key=lambda i: -M["dots"][i].get_center()[0])
        anims = []
        for k, i in enumerate(order):
            d = M["dots"][i]
            fx, fy = FINALS[i]
            lane = PORE_X
            path = VMobject().set_points_as_corners([d.get_center(), [lane, -0.95, 0],
                [lane, MY, 0], [lane, 1.65, 0], [fx, fy, 0]])
            anims.append(MoveAlongPath(d, path, rate_func=linear))
        self.play(FadeOut(M["clab"]), LaggedStart(*anims, lag_ratio=0.2), run_time=2.7)
        cl = T("cytochrome c", 30, PINK).move_to(CYT_LAB_GATE)
        self.play(FadeIn(cl), run_time=0.4)
        self.finish()


def open_stage(scene):
    """rebuild the end of s20 (open mitochondrion, escaped cytochrome c) for s21 and s22; returns (stage group, dots, label)"""
    tr = tracker(("lit", "lit", "lit", "hidden"))
    cyto = cyto_field()
    M = mito_parts()
    bcl = bcl_block("Bcl-2", 40)
    bcl_rod = rod_at(BCL_X, bcl.top - 0.45 + 0.17)
    bs = [inserted_bax(x) for x in BAX_INS_X]
    M["mem"].remove(M["memP"])
    gap = Rectangle(width=GR - GL, height=BAND + 0.06, stroke_width=0, fill_color=BG,
                    fill_opacity=1).move_to([PORE_X, MY, 0]).set_z_index(1)
    for d, (fx, fy) in zip(M["dots"], FINALS):
        d.move_to([fx, fy, 0])
    cl = T("cytochrome c", 30, PINK).move_to(CYT_LAB_GATE)
    lower = VGroup(M["fill"], M["out"], M["mem"], M["mlab"], gap, bcl, bcl_rod, *bs)
    return tr, cyto, lower, M["dots"], cl


class S21(SpokenScene):
    """Step 4: the killers assemble"""

    def construct(self):
        tr, cyto, lower, dots, cl = open_stage(self)
        kil = bchip("killers", RED, 38).move_to([-5.2, 1.2, 0])
        kil[1].set_stroke(RED, opacity=0.5).set_fill(RED, 0.04)
        kil[2].set_opacity(0.5)
        self.add(cyto, lower, dots, cl, tr)
        self.at("step")
        self.play(*light(tr, 3), run_time=0.8)
        self.at("killers")
        self.play(FadeIn(kil, shift=DOWN * 0.15), run_time=0.5)
        self.at("assemble")
        self.play(*litchip(kil, RED, 0.35), Flash(kil.get_center(), color=RED, flash_radius=1.2, run_time=0.8))
        self.finish()


# ---------------------------------------------------------------------------------------------
WC = np.array([-0.4, -0.35, 0.0])
WR = 1.95
HUB_R = 0.95
ANG = [np.radians(25.7 + 360 / 7 * k) for k in range(7)]
RING = [WC + WR * np.array([np.cos(a), np.sin(a), 0]) for a in ANG]


def radial(p, d):
    v = (p - WC) / np.linalg.norm(p - WC)
    return p + v * d


def wheel_parts():
    W = {}
    W["subs"] = VGroup(*[Circle(radius=0.5, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to(p) for p in RING])
    W["dots"] = VGroup(*[Dot(radial(p, 0.8), radius=0.18, color=PINK) for p in RING])
    W["hub"] = Circle(radius=HUB_R, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.15).move_to(WC)
    W["spokes"] = VGroup(*[Line(WC + (p - WC) / WR * HUB_R, p - (p - WC) / WR * 0.5, color=PURPLE, stroke_width=4) for p in RING])
    W["lab"] = T("apoptosome", 30, PURPLE, weight=BOLD).move_to([-4.85, -0.35, 0])
    W["leader"] = Line([-3.55, -0.35, 0], [WC[0] - WR - 0.9, -0.35, 0], color=PURPLE, stroke_width=3)
    return W


C3_POS = np.array([4.9, -0.35, 0.0])


class S22(SpokenScene):
    """cytochrome c binds Apaf-1; Apaf-1 assembles into the apoptosome wheel (camera comes down into the cytoplasm)"""

    def construct(self):
        tr, cyto, lower, dots, cl = open_stage(self)
        tr = tracker(("lit", "lit", "lit", "lit"))
        cell_ = cell()
        scatter = [np.array(p, float) for p in ([-4.8, 0.3, 0], [-3.4, -1.9, 0], [-1.6, -0.3, 0], [0.4, -2.4, 0], [2.4, -0.4, 0],
                                                [4.4, -1.7, 0], [5.0, 0.3, 0])]
        subs = VGroup(*[Circle(radius=0.5, stroke_color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.3).move_to(p)
                        for p in scatter])
        alab = T("Apaf-1", 30, PURPLE, weight=BOLD).move_to(scatter[2] + [0, 0.95, 0])
        W = wheel_parts()
        self.add(cyto, lower, dots, cl, tr)
        self.play(lower.animate.scale(0.40).to_corner(DL, buff=0.25), FadeIn(cell_),
                  cl.animate.move_to([0.4, 2.8, 0]), FadeIn(subs, lag_ratio=0.1), run_time=0.7)
        self.at("binds")
        self.play(*[d.animate.move_to(p + np.array([0.7, 0.0, 0])) for d, p in zip(dots, scatter)], FadeOut(cl), FadeIn(alab), run_time=1.3)
        self.at("assembles")
        self.play(FadeOut(lower), FadeOut(cyto), *[s_.animate.move_to(p) for s_, p in zip(subs, RING)],
                  *[d.animate.move_to(radial(p, 0.8)) for d, p in zip(dots, RING)], FadeOut(alab), run_time=0.8)
        self.at("wheel")
        self.play(Create(W["hub"]), Create(W["spokes"]), run_time=0.3)
        self.at("called the")
        self.play(FadeIn(W["lab"]), Create(W["leader"]), run_time=0.7)
        self.finish()


class S23(SpokenScene):
    """the apoptosome activates caspase-9; caspase-9 cuts and activates caspase-3"""

    def construct(self):
        tr = tracker(("lit", "lit", "lit", "lit"))
        cl = cell()
        W = wheel_parts()
        c9 = T("caspase-9", 26, GREY, weight=BOLD).move_to(WC)
        c3 = bchip("caspase-3", GREY, 34).move_to(C3_POS)
        a = arr([WC[0] + HUB_R + 0.1, WC[1], 0], c3.get_left() + [-0.05, 0, 0], GREY, 6)
        self.add(tr, cl, W["spokes"], W["hub"], W["subs"], W["dots"], W["lab"], W["leader"])
        self.at("activates")
        self.play(FadeIn(c9), run_time=0.5)
        self.at("caspase")
        self.play(c9.animate.set_color(RED), Flash(WC, color=RED, flash_radius=1.2, run_time=0.8))
        self.at("caspase 9 cuts", lead=0.55)
        self.play(GrowArrow(a), FadeIn(c3, shift=LEFT * 0.2), run_time=0.7)
        self.at("cuts")
        mid = c3.get_center()
        cut = Line(mid + [0.25, 0.45, 0], mid + [-0.25, -0.45, 0], color=RED, stroke_width=8)
        self.play(Create(cut), run_time=0.3)
        self.at("activates", nth=1, lead=0)
        self.play(a.animate.set_color(RED), *litchip(c3, RED, 0.4),
                  Flash(c3.get_center(), color=RED, flash_radius=1.3, run_time=0.8))
        self.finish()


class S24(SpokenScene):
    """caspase-3 takes the cell apart: cuts proteins; the neuron outline breaks up and stays broken"""

    def construct(self):
        tr = tracker(("lit", "lit", "lit", "lit"))
        cl = cell()
        W = wheel_parts()
        c9 = T("caspase-9", 26, RED, weight=BOLD).move_to(WC)
        c3 = bchip("caspase-3", RED, 34).move_to(C3_POS)
        c3[1].set_stroke(RED).set_fill(RED, 0.4)
        c3[2].set_color(RED)
        a = arr([WC[0] + HUB_R + 0.1, WC[1], 0], c3.get_left() + [-0.05, 0, 0], RED, 6)
        cut = Line(C3_POS + [0.25, 0.45, 0], C3_POS + [-0.25, -0.45, 0], color=RED, stroke_width=8)
        prot_pos = [[4.1, 1.5], [4.0, -2.2], [-4.4, 1.5]]

        def prot(x, y):
            l = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.65, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([x - 0.43, y, 0])
            r = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.65, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35).move_to([x + 0.43, y, 0])
            return VGroup(l, r)

        prots = [prot(x, y) for x, y in prot_pos]
        # a thin line joins the two halves so they read as one protein before the cut
        links = [Line(p[0].get_right(), p[1].get_left(), color=BLUE, stroke_width=4) for p in prots]
        self.add(tr, cl, W["spokes"], W["hub"], W["subs"], W["dots"], W["lab"], W["leader"], c9, a, c3, cut, *prots, *links)
        self.wait(0.3)
        self.play(*[FadeOut(l) for l in links], *[p[0].animate.shift([-0.3, 0.15, 0]).rotate(0.3) for p in prots],
                  *[p[1].animate.shift([0.3, -0.15, 0]).rotate(-0.3) for p in prots],
                  Flash(c3.get_center(), color=RED, flash_radius=1.3), run_time=0.6)
        self.at("takes")
        outs = []
        for k, s in enumerate(cl.segs):
            ang = (k + 0.5) * TAU / 16
            v = np.array([np.cos(ang), np.sin(ang), 0])
            outs.append(s.animate.shift(v * 0.8).set_stroke(GREY, opacity=0.4).rotate(0.4))
        self.play(*outs, cl.fill.animate.set_fill(GREY, 0.0), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
Q_POS = [np.array(p, float) for p in ([-3.15, 1.15, 0], [2.7, 1.15, 0], [-3.15, -0.15, 0], [2.7, -0.15, 0])]


def question_state():
    """the question card shared by s25 and s26: markers in the middle (1.4x), Bax and NGF crossed out, ? marks"""
    Q = {}
    Q["tr"] = tracker(("neutral",) * 4, y=0.5)
    for g, p in zip(Q["tr"].groups, Q_POS):
        g.scale(1.4).move_to(p)
    Q["bax"] = bchip("Bax", ORANGE, 52).move_to([-2.7, 2.8, 0])
    Q["ngf"] = bchip("NGF", YELLOW, 52).move_to([2.7, 2.8, 0])
    Q["bx"] = xmark(Q["bax"].get_center(), 0.7, RED, 10)
    Q["nx"] = xmark(Q["ngf"].get_center(), 0.7, RED, 10)
    qxs = [Q["tr"].groups[i].get_right()[0] + 0.45 for i in range(4)]
    Q["qs"] = VGroup(*[T("?", 56, TEAL, weight=BOLD).move_to([qxs[i], Q_POS[i][1], 0]) for i in range(4)])
    Q["n"] = neuron(1.15).move_to([-0.9, -2.45, 0])
    Q["nq"] = T("?", 100, TEAL, weight=BOLD).move_to([1.5, -2.4, 0])
    return Q


class S25(SpokenScene):
    """now delete Bax and take NGF away: which steps still happen? does the neuron live?"""

    def construct(self):
        tr0 = tracker(("lit",) * 4)
        Q = question_state()
        self.add(tr0)
        bax, ngf = Q["bax"], Q["ngf"]
        self.at("delete")
        anims = []
        for i, (g, p) in enumerate(zip(tr0.groups, Q_POS)):
            tset(tr0, i, "neutral")
            anims += [g.animate.scale(1.4).move_to(p)]
        self.play(FadeIn(bax, shift=DOWN * 0.2), *anims, run_time=1.0)
        self.play(Create(Q["bx"]), run_time=0.4)
        self.at("take")
        self.play(FadeIn(ngf, shift=DOWN * 0.2), run_time=0.5)
        self.at("away")
        self.play(Create(Q["nx"]), *dimchip(ngf, 0.45), run_time=0.5)
        self.at("which steps")
        self.play(LaggedStart(*[FadeIn(q, shift=UP * 0.15) for q in Q["qs"]], lag_ratio=0.25), run_time=1.4)
        self.at("does the neuron")
        self.play(FadeIn(Q["n"]), FadeIn(Q["nq"]), run_time=0.7)
        self.finish()


class S26Pause(NarratedScene):
    """silent pause: the question stays on screen, still"""

    def construct(self):
        Q = question_state()
        self.add(Q["tr"], Q["bax"], Q["ngf"], Q["bx"], Q["nx"], Q["qs"], Q["n"], Q["nq"])
        Q["ngf"][1].set_stroke(opacity=0.45).set_fill(opacity=0.07)
        Q["ngf"][2].set_opacity(0.45)
        self.finish()


# ---------------------------------------------------------------------------------------------
GX = [-4.7, -2.3, 0.1]
BASE = -2.45
GH = 4.4
BW = 1.5


class S27(SpokenScene):
    """steps 1 and 2 still happen: Akt dims, c-Jun and Bim rise; they lie upstream of Bax"""

    def construct(self):
        tr = tracker(("dark",) * 4)
        frames = VGroup(*[Rectangle(width=BW, height=GH, stroke_color=GREY, stroke_width=3).move_to([x, BASE + GH / 2, 0]) for x in GX])
        t_akt, b_akt = vbar(GX[0], BASE, BW, YELLOW, 3.9)
        t_cj, b_cj = vbar(GX[1], BASE, BW, TEAL, 0.5)
        t_bim, b_bim = vbar(GX[2], BASE, BW, ORANGE, 0.5)
        refs = VGroup(DashedLine([GX[0] - 0.95, BASE + 3.9, 0], [GX[0] + 0.95, BASE + 3.9, 0], color=LGREY, stroke_width=3),
                      DashedLine([GX[1] - 0.95, BASE + 0.5, 0], [GX[1] + 0.95, BASE + 0.5, 0], color=LGREY, stroke_width=3),
                      DashedLine([GX[2] - 0.95, BASE + 0.5, 0], [GX[2] + 0.95, BASE + 0.5, 0], color=LGREY, stroke_width=3))
        labs = VGroup(T("Akt", 32, YELLOW, weight=BOLD).move_to([GX[0], -2.95, 0]),
                      T("c-Jun", 32, TEAL, weight=BOLD).move_to([GX[1], -2.95, 0]),
                      T("Bim", 32, ORANGE, weight=BOLD).move_to([GX[2], -2.95, 0]))
        axis = T("level (relative)", 26, LGREY).move_to([-2.3, 2.5, 0])
        leg = VGroup(DashedLine([2.45, -2.95, 0], [3.2, -2.95, 0], color=LGREY, stroke_width=3), T("level with NGF", 26, LGREY).move_to([5.0, -2.95, 0]))
        bax = bchip("Bax", ORANGE, 52).move_to([5.3, 0.3, 0])
        bx = xmark(bax.get_center(), 0.7, RED, 10)
        self.add(tr, frames, b_akt, b_cj, b_bim, refs, labs, axis, leg, bax, bx)
        self.at("Steps")
        self.wait(1.0)
        self.play(*light(tr, 0), t_akt.animate.set_value(0.6), run_time=0.55)
        self.play(*light(tr, 1), t_cj.animate.set_value(3.9), t_bim.animate.set_value(3.2), run_time=0.9)
        self.at("they lie")
        up = arr([1.2, 0.3, 0], [3.9, 0.3, 0], GREY, 7, 0.3)
        self.play(GrowArrow(up), run_time=0.7)
        self.finish()


class S28(GateScene):
    """step 3 cannot happen: the gate stays shut and cytochrome c stays inside"""

    def construct(self):
        M = self.stage(("lit", "lit", "neutral", "neutral"), labels=False)
        bcl = bcl_block("Bcl-2", 40)
        bax = bchip("Bax", ORANGE, 52).move_to([3.4, 1.5, 0])
        bxx = xmark(bax.get_center(), 0.7, RED, 10)
        br = Line([-2.2, 2.6, 0], [-2.2, 2.4, 0], color=WHITE, stroke_width=3)
        shut = T("gate shut", 40, WHITE, weight=BOLD).move_to([-2.2, 2.95, 0])
        xm3 = xmark(self.tr.items[2][0].get_center(), 0.2, RED, 5)
        ok_rect = None
        self.add(bcl, bax, bxx)
        self.at("cannot happen")
        self.play(Create(xm3), run_time=0.5)
        self.at("gate stays shut")
        self.play(FadeIn(br), FadeIn(shut), Indicate(bcl, color=GREEN, scale_factor=1.05), run_time=0.8)
        self.at("cytochrome")
        self.play(FadeIn(M["clab"]), FadeIn(M["mlab"]), run_time=0.5)
        self.at("stays inside")
        self.play(Indicate(M["dots"], color=PINK, scale_factor=1.2), run_time=0.9)
        self.finish()


class S29(SpokenScene):
    """the neuron survives, but as a shrunken cell, because NGF also supports its growth"""

    def construct(self):
        tr = tracker(("lit", "lit", "neutral", "neutral"))
        xm3 = xmark(tr.items[2][0].get_center(), 0.2, RED, 5)
        cc = np.array([-2.2, -0.4, 0])
        R0 = 2.5
        n = neuron(R0).move_to(cc)
        ghost = DashedVMobject(Circle(radius=R0 + 0.12, stroke_color=LGREY, stroke_width=4).move_to(cc), num_dashes=44)
        glab = T("normal size", 28, LGREY).move_to([-2.2, cc[1] + R0 + 0.55, 0])
        ok = T("survives", 40, GREEN, weight=BOLD).move_to([-2.2, -3.55, 0])
        small = T("alive, but small", 38, GREEN, weight=BOLD).move_to([-2.2, -3.55, 0])
        ngf = bchip("NGF", YELLOW, 40).move_to([4.9, 0.9, 0])
        ngf_x = xmark(ngf.get_center(), 0.5, RED, 8)
        nolab = T("no NGF", 30, RED).move_to([4.9, 1.95, 0])
        ga = DashedLine([3.9, 0.9, 0], [0.0, 0.9, 0], color=GREY, stroke_width=5)
        gx = xmark([1.95, 0.9, 0], 0.3, RED, 7)
        gl = T("growth support lost", 32, RED).move_to([3.4, -0.45, 0])
        self.add(tr, xm3)
        self.play(FadeIn(n), run_time=0.5)
        self.at("survives")
        self.play(FadeIn(ok, shift=UP * 0.15), Flash(n.get_center(), color=GREEN, flash_radius=2.8, run_time=0.8))
        self.at("it survives as")
        self.play(FadeIn(ghost), FadeIn(glab), run_time=0.4)
        self.at("shrunken")
        self.play(n.animate.scale(0.55), ReplacementTransform(ok, small), run_time=1.2)
        self.at("NGF also")
        self.play(FadeIn(ngf), Create(ngf_x), *dimchip(ngf, 0.45), FadeIn(nolab), run_time=0.7)
        self.at("supports")
        self.play(Create(ga), Create(gx), FadeIn(gl), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
GX0 = 0.9      # left end of the compact gate drawn on the end card
GMY = -0.5     # membrane height there


def gate_card(open_=False):
    """the gate structure for the end card (same picture as the gate scenes, drawn compact at the right)"""
    th = 0.22
    top = GMY + th / 2
    x0, x1 = GX0, 6.5
    parts = []
    body = RoundedRectangle(corner_radius=0.5, width=x1 - x0 + 0.4, height=1.9, stroke_color=GREY, stroke_width=5,
                            fill_color=GREY, fill_opacity=0.15).move_to([(x0 + x1) / 2, GMY - th / 2 - 0.95 + 0.02, 0])
    body.set_stroke(opacity=0)
    bx_x = [3.6, 5.6]
    gl, gr = bx_x[0] + 0.14, bx_x[1] - 0.14

    def band(a, b):
        return Rectangle(width=b - a, height=th, stroke_width=0, fill_color=GREY, fill_opacity=0.65).move_to([(a + b) / 2, GMY, 0])

    if not open_:
        bands = [band(x0, x1)]
        bcl = notched(1.9, 1.15, GREEN, nd=0.35).move_to([x0 + 1.05, top + 0.575, 0])
        bcl_t = T("Bcl-2", 28, GREEN, weight=BOLD).move_to(bcl).shift(DOWN * 0.12)
        bax = notched(1.5, 1.0, ORANGE, nd=0.3).move_to([4.1, top + 0.5, 0])
        bax_t = T("Bax", 28, ORANGE, weight=BOLD).move_to(bax).shift(DOWN * 0.1)
        hb = VGroup(Line([x0 + 2.15, 0.1, 0], [x0 + 2.4, 0.1, 0], color=GREEN, stroke_width=8),
                    Line([x0 + 2.4, -0.2, 0], [x0 + 2.4, 0.4, 0], color=GREEN, stroke_width=8))
        dots = VGroup(*[Dot([x, y, 0], radius=0.17, color=PINK) for x, y in
                        [(1.6, -1.15), (2.8, -1.15), (4.0, -1.15), (5.2, -1.15), (2.2, -1.75), (3.4, -1.75), (4.6, -1.75)]])
        parts = [body, *bands, dots, bcl, bcl_t, bax, bax_t, hb]
    else:
        bands = [band(x0, gl), band(gr, x1)]
        bcl = notched(1.9, 1.15, GREEN, nd=0.35).move_to([x0 + 1.05, top + 0.575, 0])
        bcl_t = T("Bcl-2", 28, GREEN, weight=BOLD).move_to(bcl).shift(DOWN * 0.12)
        ins = []
        for x in bx_x:
            blk = RoundedRectangle(corner_radius=0.12, width=1.1, height=0.75, stroke_color=ORANGE, stroke_width=3,
                                   fill_color=ORANGE, fill_opacity=0.5).move_to([x, top + 0.5, 0])
            rod = RoundedRectangle(corner_radius=0.07, width=0.28, height=0.55, stroke_color=ORANGE, stroke_width=3,
                                   fill_color=ORANGE, fill_opacity=0.95).move_to([x, GMY + 0.1, 0])
            lab = T("Bax", 24, ORANGE, weight=BOLD).move_to(blk)
            ins += [rod, blk, lab]
        dots = VGroup(*[Dot([x, y, 0], radius=0.17, color=PINK) for x, y in
                        [(1.6, -1.15), (2.8, -1.15), (2.2, -1.75), (3.4, -1.75), (4.6, -1.75)]])
        dots.add(*[Dot([x, y, 0], radius=0.17, color=PINK) for x, y in [(4.15, 0.95), (4.95, 0.95)]])
        parts = [body, *bands, dots, bcl, bcl_t, *ins]
    return VGroup(*parts)


class S30(SpokenScene):
    """the guiding idea card: NGF loss -> new gene expression -> gate opens"""

    def construct(self):
        line1 = T("That is the first brake.", 40, font=TITLE_FONT).move_to([0, 3.2, 0])
        closed = gate_card(False).scale(0.90).move_to([0, -1.4, 0])
        opened = gate_card(True).scale(0.90).move_to(closed)
        lab = T("Brake 1: the gate", 40, YELLOW, weight=BOLD).move_to([0, -3.25, 0])
        ngf = bchip("NGF loss", YELLOW, 50).move_to([-4.9, 1.3, 0])
        gene = bchip("new gene\nexpression", TEAL, 50).move_to([-0.5, 1.3, 0])
        gate = bchip("gate opens", WHITE, 50).move_to([4.3, 1.3, 0])
        a1 = arr(ngf.get_right(), gene.get_left(), GREY, 7)
        a2 = arr(gene.get_right(), gate.get_left(), GREY, 7)
        self.play(FadeIn(line1), run_time=0.5)
        self.at("1 is the")
        self.play(FadeIn(closed), FadeIn(lab), run_time=0.6)
        self.at("NGF loss")
        self.play(FadeIn(ngf), run_time=0.4)
        self.at("opens it")
        self.play(FadeIn(gate), run_time=0.4)
        self.at("new gene")
        self.play(FadeIn(gene), GrowArrow(a1), GrowArrow(a2), run_time=0.45)
        self.play(FadeOut(closed), FadeIn(opened), run_time=0.35)
        self.finish()


class S31End(EndCard):
    LINE = "Brake one is the gate,\nopened through new gene expression."
