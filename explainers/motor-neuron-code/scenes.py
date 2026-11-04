"""One Protein, Two Cell Types  (chapter 1 of "Transcription Factor Codes: Building a Motor Neuron")

COLOR MAP (one colour per concept, shared by every chapter; taken from scenes.old.py)
  BLUE   = Lhx3
  YELLOW = Isl1
  PURPLE = NLI (the cofactor clip)
  ORANGE = V2 interneuron and its genes (Chx10)
  GREEN  = motor neuron and its genes
  PINK   = Mnx1 in older drafts; in this chapter Mnx1 is drawn GREEN with the motor-neuron genes
  TEAL   = Sonic hedgehog (not used in this chapter)
  RED    = absent / crossed out
  GREY   = cells, tissue, DNA, structure, labels
  GOLD   = the model banner and the "one idea" card (Olig2 / Hox in other chapters)

SHAPE LANGUAGE (same in every scene)
  a protein is a rounded block; its LIM domains are two knobs on stems (handles) on top
  NLI is a purple clip: a block with two rings that close around a pair of knobs, plus a peg
  (right unit) or socket (left unit) so two NLI clips snap together
  Isl1 reaches Lhx3 with a short tail that ends in a bracket around the Lhx3 knobs
"""
import numpy as np
from types import SimpleNamespace as NS
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58AB5"
LIGHT = "#B8BFCC"   # captions and tick labels: lighter than GREY so they read on the dark ground


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def tag(text, pos, size=24, color=GREY):
    return T(text, size, color).move_to(pos)


def left_text(text, size, color, x, y, weight=NORMAL):
    t = T(text, size, color, weight=weight)
    return t.move_to([x + t.width / 2, y, 0])


def dna_bar(cx, y, w=11.0, color=GREY, h=0.3):
    return RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35).move_to([cx, y, 0])


# ---- protein blocks with LIM-domain knobs -------------------------------------------------------
KNOB_DX = 0.42


def prot(label, color, cx, bottom, k, w=1.5, h=0.9, knobs=True):
    blk = RoundedRectangle(corner_radius=0.14 * k, width=w * k, height=h * k, stroke_color=color, stroke_width=4,
                           fill_color=color, fill_opacity=0.28).move_to([cx, bottom + h * k / 2, 0])
    txt = T(label, max(22, int(round(24 * k))), color, weight=BOLD).move_to(blk)
    parts = [blk]
    pts = []
    if knobs:
        top = bottom + h * k
        for s in (-1, 1):
            x = cx + s * KNOB_DX * k
            parts.append(Line([x, top, 0], [x, top + 0.35 * k, 0], color=color, stroke_width=5))
            parts.append(Dot([x, top + 0.35 * k, 0], radius=0.17 * k, color=color))
            pts.append(np.array([x, top + 0.35 * k, 0]))
    g = VGroup(*parts, txt)
    g.blk, g.txt, g.knob_pts = blk, txt, pts
    return g


def clip(cx, ky, k, peg=None, color=PURPLE, label="NLI"):
    """NLI clip whose two rings are centred on the knob height ky. peg: 'R' = peg on right edge,
    'L' = socket on left edge, None = plain."""
    rr, bw, bh = 0.30 * k, 1.7 * k, 0.9 * k
    cy = ky + rr + bh / 2
    kw = dict(stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.3)
    base = RoundedRectangle(corner_radius=0.14 * k, width=bw, height=bh).move_to([cx, cy, 0])
    if peg == "L":
        body = Difference(base, Circle(radius=0.26 * k).move_to([cx - bw / 2, cy, 0]), **kw)
    else:
        body = base.set_style(**kw)
    rings = [Circle(radius=rr, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([cx + s * KNOB_DX * k, ky, 0])
             for s in (-1, 1)]
    parts = [body, *rings]
    if peg == "R":
        parts.append(Circle(radius=0.2 * k, stroke_color=color, stroke_width=4, fill_color=color,
                            fill_opacity=0.6).move_to([cx + bw / 2, cy, 0]))
    txt = T(label, max(22, int(round(24 * k))), color, weight=BOLD).move_to([cx, cy, 0])
    g = VGroup(*parts, txt)
    g.body, g.rings, g.txt = body, rings, txt
    return g


GAP = 0.5


def v2_unit(cx, gene_top, k, peg):
    ky = gene_top + 1.25 * k
    L = prot("Lhx3", BLUE, cx, gene_top, k)
    N = clip(cx, ky, k, peg)
    return NS(L=L, N=N, ky=ky)


def mn_unit(sgn, cxI, gene_top, k, peg):
    """Motor-neuron unit. sgn=-1: Lhx3 sits to the left of Isl1; sgn=+1: to the right."""
    cxL = cxI + sgn * (1.5 * k + GAP)
    kyL = gene_top + 1.25 * k
    L = prot("Lhx3", BLUE, cxL, gene_top, k)
    ib = kyL - 0.45 * k
    I = prot("Isl1", YELLOW, cxI, ib, k)
    kyI = ib + 0.9 * k + 0.35 * k
    N = clip(cxI, kyI, k, peg)
    xs, xe = cxI + sgn * 0.75 * k, cxL - sgn * 0.7 * k
    tail = Line([xs, kyL, 0], [xe, kyL, 0], color=YELLOW, stroke_width=8)
    brk = RoundedRectangle(corner_radius=0.2 * k, width=(2 * KNOB_DX + 0.56) * k, height=0.7 * k,
                           stroke_color=YELLOW, stroke_width=5, fill_opacity=0).move_to([cxL, kyL, 0])
    return NS(L=L, I=I, N=N, tail=VGroup(tail, brk), kyL=kyL, kyI=kyI, cxL=cxL, cxI=cxI, tail_mid=(xs + xe) / 2)


# ---- spinal cord stage (chapter opening) ---------------------------------------------------------
CELL_R = 1.5
CELL_DY = 1.65
CX = -3.2


def cord_group(cx):
    cord = Ellipse(width=5.6, height=7.2, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                   fill_opacity=0.06).move_to([cx, 0, 0]).set_z_index(-1)
    up = Circle(radius=CELL_R, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                fill_opacity=0.14).move_to([cx, CELL_DY, 0])
    lo = Circle(radius=CELL_R, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                fill_opacity=0.14).move_to([cx, -CELL_DY, 0])
    return cord, up, lo


def lab_row(text, color, y):
    t = left_text(text, 32, color, 0.5, y)
    ln = Line([-1.6, y, 0], [0.35, y, 0], color=GREY, stroke_width=2.5)
    return VGroup(ln, t)


def cord_lab():
    """'chick spinal cord, cross-section' label with a leader to the cord outline (right side, low)."""
    t = left_text("chick spinal cord, cross-section", 28, LIGHT, 0.5, -3.0)
    ln = Line([0.35, -3.0, 0], [-1.7, -3.0, 0], color=GREY, stroke_width=2.5)
    return VGroup(ln, t)


def lhx_chip(cy, size=32):
    return chip("Lhx3", BLUE, size).move_to([CX, cy + 0.5, 0])


def isl_chip(cy, size=32):
    return chip("Isl1", YELLOW, size).move_to([CX, cy - 0.5, 0])


def labeled_stage(chips=True):
    cord, up, lo = cord_group(CX)
    for c in (up, lo):
        c.set_fill(BLUE, 0.3)
    up.set_stroke(ORANGE)
    lo.set_stroke(GREEN)
    labs = VGroup(lab_row("V2 interneuron", ORANGE, CELL_DY), lab_row("newly born motor neuron", GREEN, -CELL_DY))
    chip_up = lhx_chip(CELL_DY)
    chip_lo = lhx_chip(-CELL_DY)
    base = VGroup(cord, up, lo, labs, cord_lab())
    if chips:
        base.add(chip_up, chip_lo)
    return NS(all=base, cord=cord, up=up, lo=lo, labs=labs, chip_up=chip_up, chip_lo=chip_lo)


def ghost_isl(center, w=1.9, h=0.9):
    box = RoundedRectangle(corner_radius=0.14, width=w, height=h).move_to(center)
    d = DashedVMobject(box, num_dashes=22).set_stroke(RED, 3.5, opacity=0.9)
    return VGroup(d, T("no Isl1", 28, RED).move_to(box))


def neighbour_labels(text="two neighbouring cells", color=LIGHT):
    t = left_text(text, 30, color, 0.5, 0.0)
    l1 = Line([0.35, 0.12, 0], [-1.9, 1.0, 0], color=GREY, stroke_width=2.5)
    l2 = Line([0.35, -0.12, 0], [-1.9, -1.0, 0], color=GREY, stroke_width=2.5)
    return t, VGroup(l1, l2)


# ---- the prediction panels (chapter scenes 6-10) ------------------------------------------------
YA, YB = 2.15, 0.0
PX = 2.4
GENE_X = 5.55


def gchip(name, color):
    return chip(name, color, 28, pad=0.16)


def pred_stage():
    c = [-4.7, 0.9, 0]
    tube = Ellipse(width=2.8, height=4.4, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                   fill_opacity=0.06).move_to(c)
    half = Intersection(Ellipse(width=2.8, height=4.4).move_to(c), Rectangle(width=1.4, height=4.4).move_to([-4.0, 0.9, 0]),
                        stroke_width=0, fill_color=GREEN, fill_opacity=0.4)
    ep_lab = VGroup(T("electroporated side", 26, GREEN).move_to([-4.7, 3.55, 0]),
                    Line([-3.9, 3.28, 0], [-3.9, 2.8, 0], color=GREEN, stroke_width=3))
    tube_lab = T("chick embryo\nneural tube", 26, LIGHT).move_to([-4.7, -1.9, 0])
    ptr_a = arr([-1.95, YA, 0], [-3.65, 2.0, 0], GREY, w=4, tip=0.2)
    ptr_b = arr([-1.95, YB, 0], [-3.7, 0.4, 0], GREY, w=4, tip=0.2)

    def box(y):
        return RoundedRectangle(corner_radius=0.2, width=8.6, height=1.95, stroke_color=GREY, stroke_width=3,
                                fill_opacity=0).move_to([PX, y, 0])
    pa_box, pb_box = box(YA), box(YB)
    pa_let = T("A", 48, TEXT, weight=BOLD).move_to([-1.35, YA, 0])
    pb_let = T("B", 48, TEXT, weight=BOLD).move_to([-1.35, YB, 0])
    pa_lhx = chip("Lhx3", BLUE, 28).move_to([0.1, YA, 0])
    pb_lhx = chip("Lhx3", BLUE, 28).move_to([0.1, YB, 0])
    pa_ghost = ghost_isl([2.35, YA, 0])
    pb_plus = T("+", 36, TEXT).move_to([1.2, YB, 0])
    pb_isl = chip("Isl1", YELLOW, 28).move_to([2.35, YB, 0])
    q = T("Which genes come up?", 36, TEXT).move_to([2.4, -1.7, 0])
    a1 = chip("motor-neuron genes\n(Mnx1)", GREEN, 26)
    a2 = chip("V2 genes\n(Chx10)", ORANGE, 26)
    a3 = chip("neither", GREY, 26)
    ans = VGroup(a1, a2, a3).arrange(RIGHT, buff=0.35).move_to([2.3, -3.0, 0])
    # Both gene chips share the panel's centre line, in matching columns.
    mnxA = gchip("Mnx1", GREEN).move_to([4.5, YA, 0])
    # A separate small cross preserves the gene name's legibility.
    crossA = VGroup(Line([3.55, YA - 0.16, 0], [3.87, YA + 0.16, 0], color=RED, stroke_width=4),
                    Line([3.55, YA + 0.16, 0], [3.87, YA - 0.16, 0], color=RED, stroke_width=4))
    chxA = gchip("Chx10", ORANGE).move_to([5.9, YA, 0])
    mnxB = gchip("Mnx1", GREEN).move_to([4.5, YB, 0])
    chxB = gchip("Chx10", ORANGE).move_to([5.9, YB, 0])
    arrB = arr([3.35, YB, 0], [3.85, YB, 0], GREEN, w=4, tip=0.16)
    dnB = arr([5.9, YB - 0.42, 0], [5.9, YB - 0.83, 0], ORANGE, w=4, tip=0.16)
    held = T("V2 genes largely held down", 28, ORANGE).move_to([2.4, -1.5, 0])
    return NS(tube=tube, half=half, ep_lab=ep_lab, tube_lab=tube_lab, ptr_a=ptr_a, ptr_b=ptr_b,
              pa=VGroup(pa_box, pa_let, pa_lhx), pa_box=pa_box, pa_ghost=pa_ghost,
              pb_box=pb_box, pb_base=VGroup(pb_box, pb_let, pb_lhx), pb_plus=pb_plus, pb_isl=pb_isl,
              q=q, ans=ans, a1=a1, a2=a2, a3=a3, mnxA=mnxA, crossA=crossA, chxA=chxA,
              mnxB=mnxB, chxB=chxB, arrB=arrB, dnB=dnB, held=held)


def dim_fn(f):
    return lambda m: m.set_fill(opacity=m.get_fill_opacity() * f).set_stroke(opacity=m.get_stroke_opacity() * f)


def dim(m, f=0.35):
    """Fade a group's fills and strokes by a factor (keeps empty boxes empty)."""
    m.apply_to_family(dim_fn(f))
    return m


def dimmed(m, f=0.35):
    return m.animate.apply_to_family(dim_fn(f))


def hi(c, color):
    """Highlight a chip: thicker outline, stronger fill (box only, text untouched)."""
    return c[0].animate.set_fill(color, 0.35).set_stroke(color, 6)


def static_predict(p, question=True, answers=True):
    parts = [p.tube, p.half, p.ep_lab, p.tube_lab, p.ptr_a, p.ptr_b, p.pa, p.pa_ghost, p.pb_base, p.pb_plus, p.pb_isl]
    if question:
        parts.append(p.q)
    if answers:
        parts.append(p.ans)
    return parts


class S00Title(TitleCard):
    LESSON = "Transcription Factor Codes: Building a Motor Neuron"
    TITLE = "One Protein, Two Cell Types"


class S01Q(SpokenScene):
    def construct(self):
        cord, up, lo = cord_group(CX)
        self.play(FadeIn(up, scale=0.9), FadeIn(lo, scale=0.9), run_time=0.6)
        self.at("neighboring cells")
        nb, nb_l = neighbour_labels()
        self.play(FadeIn(nb, shift=LEFT * 0.15), Create(nb_l), run_time=0.6)
        self.at("spinal cord")
        cl = cord_lab()
        self.play(Create(cord), FadeIn(cl), run_time=0.8)
        self.at("make the same protein")
        same = left_text("same protein in both", 30, BLUE, 0.5, 0.0)
        self.play(up.animate.set_stroke(BLUE).set_fill(BLUE, 0.3), lo.animate.set_stroke(BLUE).set_fill(BLUE, 0.3),
                  ReplacementTransform(nb, same), run_time=0.7)
        q1 = T("?", 80, TEXT, weight=BOLD).move_to(lo)
        q2 = T("?", 80, TEXT, weight=BOLD).move_to(up)
        self.at("one becomes")
        self.play(FadeIn(q1, scale=1.4), run_time=0.5)
        self.at("the other")
        self.play(FadeIn(q2, scale=1.4), run_time=0.5)
        self.at("interneuron")
        self.play(Indicate(q1, color=TEXT), Indicate(q2, color=TEXT), run_time=0.9)
        self.finish()


def s01_end():
    cord, up, lo = cord_group(CX)
    for c in (up, lo):
        c.set_stroke(BLUE).set_fill(BLUE, 0.3)
    q1 = T("?", 80, TEXT, weight=BOLD).move_to(lo)
    q2 = T("?", 80, TEXT, weight=BOLD).move_to(up)
    same = left_text("same protein in both", 30, BLUE, 0.5, 0.0)
    _, nb_l = neighbour_labels()
    return NS(cord=cord, up=up, lo=lo, q1=q1, q2=q2, same=same, leaders=nb_l, cl=cord_lab())


class S02Lhx3(SpokenScene):
    def construct(self):
        s = s01_end()
        self.add(s.cord, s.up, s.lo, s.q1, s.q2, s.same, s.leaders, s.cl)
        self.at("LHX3")
        big = chip("Lhx3", BLUE, 56).move_to([3.3, 0, 0])
        self.play(FadeOut(s.q1), FadeOut(s.q2), FadeOut(s.leaders), ReplacementTransform(s.same, big), run_time=0.8)
        self.at("newly born motor neurons")
        lab_lo = lab_row("newly born motor neuron", GREEN, -CELL_DY)
        c_lo = lhx_chip(-CELL_DY)
        self.play(s.lo.animate.set_stroke(GREEN), FadeIn(lab_lo), TransformFromCopy(big, c_lo), run_time=0.9)
        self.at("V2 interneurons")
        lab_up = lab_row("V2 interneuron", ORANGE, CELL_DY)
        c_up = lhx_chip(CELL_DY)
        self.play(s.up.animate.set_stroke(ORANGE), FadeIn(lab_up), TransformFromCopy(big, c_up), FadeOut(big), run_time=0.9)
        self.at("make it")
        self.remove(big)
        self.play(Indicate(c_up, color=BLUE), Indicate(c_lo, color=BLUE), run_time=0.9)
        self.finish()


class S03Isl1(SpokenScene):
    def construct(self):
        st = labeled_stage()
        g = ghost_isl([CX, CELL_DY - 0.5, 0])
        self.add(st.all, g)
        self.at("islet 1")
        big = chip("Isl1", YELLOW, 56).move_to([3.3, 0, 0])
        self.play(GrowFromCenter(big), run_time=0.7)
        self.at("made in the motor neurons")
        c = isl_chip(-CELL_DY)
        self.play(ReplacementTransform(big, c), run_time=1.0)
        self.at("not the V2 interneurons")
        self.play(Indicate(g, color=RED, scale_factor=1.12), run_time=0.9)
        self.finish()


class S04Lim(SpokenScene):
    def construct(self):
        # two proteins, then a close-up of one
        def blk(name, color, x):
            b = VGroup(RoundedRectangle(corner_radius=0.25, width=4.6, height=3.0, stroke_color=color, stroke_width=4,
                                        fill_color=color, fill_opacity=0.28), T(name, 60, color, weight=BOLD))
            b[1].move_to(b[0])
            return b.move_to([x, -0.3, 0])
        sm_l, sm_r = blk("Lhx3", BLUE, -3.3), blk("Isl1", YELLOW, 3.3)
        self.play(FadeIn(sm_l, scale=0.9), FadeIn(sm_r, scale=0.9), run_time=0.5)
        bt = T("LIM homeodomain proteins", 44, TEXT).move_to([0, 2.7, 0])
        br = VGroup(Line([-5.6, 2.2, 0], [5.6, 2.2, 0], color=GREY, stroke_width=3),
                    Line([-5.6, 2.2, 0], [-5.6, 1.5, 0], color=GREY, stroke_width=3),
                    Line([5.6, 2.2, 0], [5.6, 1.5, 0], color=GREY, stroke_width=3))
        self.play(FadeIn(bt, shift=DOWN * 0.15), Create(br), run_time=0.8)
        # close-up geometry (a larger version of the protein block)
        dna_y = -2.55
        top0 = dna_y + 0.15
        foot_h, body_h = 0.7, 2.5
        foot = VGroup(RoundedRectangle(corner_radius=0.12, width=3.8, height=foot_h, stroke_color=BLUE, stroke_width=4,
                                       fill_color=BLUE, fill_opacity=0.55),
                      T("homeodomain", 28, TEXT)).move_to([0, top0 + foot_h / 2, 0])
        foot[1].move_to(foot[0])
        body = VGroup(RoundedRectangle(corner_radius=0.2, width=5.0, height=body_h, stroke_color=BLUE, stroke_width=4,
                                       fill_color=BLUE, fill_opacity=0.28), T("Lhx3", 52, BLUE, weight=BOLD))
        body[0].move_to([0, top0 + foot_h + body_h / 2, 0])
        body[1].move_to(body[0])
        float_up = 0.8
        foot.shift(UP * float_up)
        body.shift(UP * float_up)
        self.at("the homeodomain")
        self.play(FadeOut(sm_r), FadeOut(bt), FadeOut(br), ReplacementTransform(sm_l, body),
                  FadeIn(foot, shift=DOWN * 0.2), run_time=0.8)
        bar = dna_bar(0, dna_y, w=11.0)
        dna_lab = T("DNA", 28, LIGHT).move_to([-5.0, dna_y - 0.55, 0])
        self.at("binds")
        self.play(FadeIn(bar), FadeIn(dna_lab), foot.animate.shift(DOWN * float_up), body.animate.shift(DOWN * float_up),
                  run_time=0.7)
        fy = top0 + foot_h / 2
        bd = left_text("binds DNA", 34, TEXT, 2.3, fy)
        bd_ar = arr([2.25, fy, 0], [1.95, fy, 0], TEXT, w=4, tip=0.18)
        self.play(FadeIn(bd, shift=LEFT * 0.15), FadeIn(bd_ar), run_time=0.5)
        # handles
        kx, ky0 = 1.3, top0 + foot_h + body_h
        ky1 = ky0 + 1.1
        stems = VGroup(*[Line([s * kx, ky0, 0], [s * kx, ky1, 0], color=BLUE, stroke_width=8) for s in (-1, 1)])
        knobs = VGroup(*[Dot([s * kx, ky1, 0], radius=0.36, color=BLUE) for s in (-1, 1)])
        self.at("two")
        self.play(Create(stems), run_time=0.4)
        self.play(GrowFromCenter(knobs), run_time=0.3)
        self.at("domains are")
        lim_lab = T("LIM domains", 36, BLUE)
        lim_lab.move_to([-1.9 - lim_lab.width / 2, ky1, 0])
        self.play(FadeIn(lim_lab, shift=RIGHT * 0.15), run_time=0.5)
        self.at("handles that")
        hl = T("handles that other proteins grip", 32, TEXT).move_to([0, 3.45, 0])
        ld = VGroup(*[Line([s * 0.9, 3.15, 0], [s * kx, ky1 + 0.45, 0], color=TEXT, stroke_width=3) for s in (-1, 1)])
        self.play(FadeIn(hl, shift=DOWN * 0.15), Create(ld), Indicate(knobs, color=TEXT), run_time=0.8)
        self.finish()


class S05Nli(SpokenScene):
    def construct(self):
        k = 2.5
        ky = -1.95
        c1 = clip(0, ky, k, "R")
        self.play(GrowFromCenter(c1), run_time=0.8)
        # labels, at the start: rings grip LIM domains, peg pairs with NLI
        ring_x = -KNOB_DX * k - 0.3 * k
        ring_lab = VGroup(Line([ring_x - 0.05, ky, 0], [-2.9, ky, 0], color=PURPLE, stroke_width=3),
                          T("grip LIM\ndomains", 30, PURPLE).move_to([-4.4, ky, 0]))
        peg_y = ky + 0.3 * k + 0.45 * k
        peg_lab = VGroup(Line([2.2 * 1.0 + 0.1, peg_y, 0], [3.0, peg_y, 0], color=PURPLE, stroke_width=3),
                         T("pairs with\nNLI", 30, PURPLE).move_to([4.4, peg_y, 0]))
        self.play(FadeIn(ring_lab), run_time=0.5)
        self.at("cofactor")
        name = T("NLI (also called Ldb1)", 36, PURPLE, weight=BOLD).move_to([0, 1.75, 0])
        self.play(FadeIn(name, shift=DOWN * 0.15), FadeIn(peg_lab), run_time=0.6)
        bar = dna_bar(0, -3.35, w=11.0)
        cross = VGroup(Line([-0.55, -3.05, 0], [0.55, -3.65, 0], color=RED, stroke_width=10),
                       Line([-0.55, -3.65, 0], [0.55, -3.05, 0], color=RED, stroke_width=10))
        nolab = T("no DNA-binding\ndomain", 30, RED).move_to([4.6, -2.55, 0])
        self.at("binds no")
        self.play(FadeIn(bar), run_time=0.5)
        self.at("DNA")
        self.play(Create(cross), FadeIn(nolab), run_time=0.7)
        c2 = clip(0.85 * k, ky, k, "L").shift(RIGHT * 9.0)
        self.at("pairs with itself")
        self.play(FadeOut(bar), FadeOut(cross), FadeOut(nolab), FadeOut(peg_lab), FadeOut(ring_lab), FadeOut(name),
                  c1.animate.shift(LEFT * 0.85 * k + UP * 1.2), c2.animate.shift(LEFT * 9.0 + UP * 1.2), run_time=1.2)
        self.at("grips")
        grips = T("NLI pairs with NLI; both grip LIM domains", 32, PURPLE).move_to([0, -2.55, 0])
        self.play(FadeIn(grips, shift=UP * 0.15), *[Indicate(r, color=TEXT, scale_factor=1.2) for r in c1.rings + c2.rings],
                  run_time=0.9)
        self.finish()


class S06Predict(SpokenScene):
    def construct(self):
        p = pred_stage()
        self.play(FadeIn(p.tube), FadeIn(p.tube_lab), FadeIn(p.half), FadeIn(p.ep_lab), run_time=0.9)
        self.at("put LHX3")
        self.play(FadeIn(p.pa, shift=LEFT * 0.3), GrowArrow(p.ptr_a), run_time=0.7)
        self.at("chick cells")
        self.play(Indicate(p.half, color=GREEN, scale_factor=1.04), run_time=0.8)
        self.at("without islet")
        self.play(FadeIn(p.pa_ghost), run_time=0.6)
        self.at("then")
        self.play(FadeIn(p.pb_base, shift=LEFT * 0.3), GrowArrow(p.ptr_b), run_time=0.7)
        self.at("in both")
        self.play(FadeIn(p.pb_plus), FadeIn(p.pb_isl, shift=LEFT * 0.2), run_time=0.6)
        self.at("which genes")
        self.play(FadeIn(p.q, shift=UP * 0.15),
                  LaggedStart(*[FadeIn(a, shift=UP * 0.2) for a in (p.a1, p.a2, p.a3)], lag_ratio=0.3), run_time=1.2)
        self.finish()


class S07Pause(NarratedScene):
    def construct(self):
        p = pred_stage()
        self.add(*static_predict(p))
        cue = T("Pause. Decide.", 36, GOLD, weight=BOLD).move_to([-4.7, -2.85, 0])
        ring = Circle(radius=0.42, stroke_color=GOLD, stroke_width=4, fill_opacity=0).move_to([-2.25, -2.85, 0])
        self.add(cue, ring)
        num = T("5", 40, GOLD, weight=BOLD).move_to(ring)
        self.add(num)
        for n in (4, 3, 2, 1):
            self.wait(1.0)
            new = T(str(n), 40, GOLD, weight=BOLD).move_to(ring)
            self.remove(num)
            self.add(new)
            num = new
        self.finish()


def a_parts(p):
    return [p.mnxA, p.crossA, p.chxA]


class S08RevealA(SpokenScene):
    def construct(self):
        p = pred_stage()
        self.add(*static_predict(p, question=False))
        p.chxA[0].set_stroke(ORANGE, 6).set_fill(ORANGE, 0.5)
        self.play(p.pa_box.animate.set_stroke(TEXT, 6), dimmed(p.pb_base, 0.4), dimmed(p.pb_plus, 0.4), dimmed(p.pb_isl, 0.4),
                  dimmed(p.ptr_b, 0.4), run_time=0.6)
        self.at("V2 interneuron genes")
        self.play(FadeIn(p.chxA, scale=0.7), FadeIn(p.mnxA), FadeIn(p.crossA), hi(p.a2, ORANGE),
                  dimmed(p.a1, 0.3), dimmed(p.a3, 0.3), run_time=0.9)
        self.at("such as")
        self.play(Indicate(p.chxA, color=ORANGE, scale_factor=1.05), run_time=1.0)
        self.finish()


def b_start(p):
    """Everything at the start of the B reveal: A quiet, answers neutral, no question."""
    p.chxA[0].set_stroke(ORANGE, 4).set_fill(ORANGE, 0.3)
    parts = static_predict(p, question=False, answers=True) + a_parts(p)
    for m in (p.pa, p.pa_ghost, p.chxA, p.ptr_a):
        dim(m, 0.4)
    return parts


class S09RevealB(SpokenScene):
    def construct(self):
        p = pred_stage()
        self.add(*b_start(p))
        p.mnxB[0].set_stroke(GREEN, 6).set_fill(GREEN, 0.5)
        dim(p.chxB, 0.4)
        self.play(p.pb_box.animate.set_stroke(TEXT, 6), Indicate(p.pb_isl, color=YELLOW), run_time=0.7)
        self.at("turns on", lead=0.5)
        self.play(GrowArrow(p.arrB), FadeIn(p.mnxB, scale=0.7), FadeIn(p.chxB), hi(p.a1, GREEN), dimmed(p.a2, 0.3), dimmed(p.a3, 0.3),
                  run_time=0.8)
        self.at("such as")
        self.play(Indicate(p.mnxB, color=GREEN, scale_factor=1.05), run_time=1.0)
        self.at("V2 genes")
        self.play(Indicate(p.chxB, color=ORANGE, scale_factor=1.05), GrowArrow(p.dnB), FadeIn(p.held, shift=UP * 0.1), run_time=0.9)
        self.at("largely held down")
        self.play(Indicate(p.held, color=ORANGE, scale_factor=1.1), run_time=0.8)
        self.finish()


class S10Beat(NarratedScene):
    def construct(self):
        p = pred_stage()
        self.add(*b_start(p))
        p.pb_box.set_stroke(TEXT, 6)
        p.mnxB[0].set_stroke(GREEN, 6).set_fill(GREEN, 0.5)
        dim(p.chxB, 0.4)
        p.a1[0].set_fill(GREEN, 0.35).set_stroke(GREEN, 6)
        dim(p.a2, 0.3)
        dim(p.a3, 0.3)
        self.add(p.arrB, p.mnxB, p.chxB, p.dnB, p.held)
        self.finish()


# ---- V2 complex (scenes 11-12) -------------------------------------------------------------------
KV = 2.1
V2_YG = -2.5


def cell_icon(label, color):
    c = Circle(radius=0.42, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25).move_to([-6.2, 3.4, 0])
    t = left_text(label, 28, color, -5.55, 3.4)
    return VGroup(c, t)


def v2_scene_parts():
    icon = cell_icon("V2 interneuron", ORANGE)
    bar = dna_bar(0, V2_YG, w=12.0)
    gt = V2_YG + 0.15
    return icon, bar, gt


def v2_extras():
    credit = T("Thaler et al., 2002", 26, LIGHT).move_to([4.9, -3.4, 0])
    ghost = ghost_isl([-5.7, V2_YG + 1.5, 0], w=1.9, h=0.9)
    return credit, ghost


class S11V2(SpokenScene):
    def construct(self):
        icon, bar, gt = v2_scene_parts()
        credit, ghost = v2_extras()
        u1 = v2_unit(0, gt, KV, "R")
        self.play(FadeIn(icon), FadeIn(bar), FadeIn(credit), run_time=0.5)
        self.play(FadeIn(u1.L, shift=DOWN * 0.3), run_time=0.6)
        self.at("without islet")
        self.play(FadeIn(ghost), run_time=0.4)
        self.at("grips", lead=0.7)
        u1.N.shift(UP * 0.8)
        self.play(FadeIn(u1.N, shift=DOWN * 0.1), run_time=0.4)
        self.at("grips")
        self.play(u1.N.animate.shift(DOWN * 0.8), run_time=0.9)
        self.at("directly")
        self.play(*[Indicate(r, color=TEXT, scale_factor=1.25) for r in u1.N.rings], run_time=0.8)
        u2 = v2_unit(0.85 * KV, gt, KV, "L")
        sh = 10.0
        u2.L.shift(RIGHT * sh)
        u2.N.shift(RIGHT * sh)
        self.at("pairs of these")
        self.play(u1.L.animate.shift(LEFT * 0.85 * KV), u1.N.animate.shift(LEFT * 0.85 * KV),
                  u2.L.animate.shift(LEFT * sh), u2.N.animate.shift(LEFT * sh), run_time=1.0)
        self.at("bind V2 genes")
        lab = T("V2 genes", 34, ORANGE).move_to([0, V2_YG - 0.65, 0])
        self.play(bar.animate.set_stroke(ORANGE).set_fill(ORANGE, 0.5), FadeIn(lab, shift=UP * 0.1), run_time=0.8)
        self.finish()


def v2_final():
    icon, bar, gt = v2_scene_parts()
    bar.set_stroke(ORANGE).set_fill(ORANGE, 0.5)
    u1 = v2_unit(-0.85 * KV, gt, KV, "R")
    u2 = v2_unit(0.85 * KV, gt, KV, "L")
    lab = T("V2 genes", 34, ORANGE).move_to([0, V2_YG - 0.65, 0])
    credit, ghost = v2_extras()
    return [icon, bar, u1.L, u1.N, u2.L, u2.N, lab, ghost, credit]


class S12Beat(NarratedScene):
    def construct(self):
        self.add(*v2_final())
        self.finish()


# ---- motor-neuron complex (scenes 13-15) --------------------------------------------------------
K = 1.7
MN_YG = -2.35


def mn_scene_parts():
    icon = cell_icon("motor neuron", GREEN)
    bar = dna_bar(0, MN_YG, w=12.0)
    return icon, bar, MN_YG + 0.15


def seg_label(u):
    """'short segment' label and leader, placed left of the tail."""
    xm = u.tail_mid
    lab = T("short segment", 30, YELLOW).move_to([xm - 1.5, u.kyL + 1.2, 0])
    ld = Line([xm - 0.55, u.kyL + 0.95, 0], [xm, u.kyL + 0.12, 0], color=YELLOW, stroke_width=3)
    return VGroup(lab, ld)


class S13Mn(SpokenScene):
    def construct(self):
        icon, bar, gt = mn_scene_parts()
        cxI = (1.5 * K + GAP) / 2
        u = mn_unit(-1, cxI, gt, K, "R")
        self.play(FadeIn(icon), FadeIn(bar), FadeIn(u.L, shift=DOWN * 0.3), run_time=0.7)
        self.at("present")
        self.play(FadeIn(u.I, shift=RIGHT * 1.0), run_time=0.7)
        self.at("grips", lead=0.6)
        # Park beside the knobs with clear space, then close in one motion.
        u.N.shift(RIGHT * 2.7)
        self.play(FadeIn(u.N), run_time=0.4)
        self.at("grips")
        self.play(u.N.animate.shift(LEFT * 2.7), run_time=0.6)
        self.at("then it holds")
        self.play(Create(u.tail), run_time=1.0)
        self.at("short segment")
        self.play(FadeIn(seg_label(u)), run_time=0.6)
        self.finish()


def mn_single():
    icon, bar, gt = mn_scene_parts()
    cxI = (1.5 * K + GAP) / 2
    u = mn_unit(-1, cxI, gt, K, "R")
    return icon, bar, gt, u, seg_label(u)


def unit_caption():
    """Bracket under the left unit and its caption."""
    x0, x1 = -0.85 * K - 2.25 * K - 0.5, -0.85 * K + 1.05 * K
    y = MN_YG - 0.5
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=TEXT, stroke_width=4),
                Line([x0, y, 0], [x0, y + 0.22, 0], color=TEXT, stroke_width=4),
                Line([x1, y, 0], [x1, y + 0.22, 0], color=TEXT, stroke_width=4))
    cap = T("three-part unit: NLI + Isl1 + Lhx3", 30, TEXT).move_to([(x0 + x1) / 2, MN_YG - 0.95, 0])
    return VGroup(br, cap)


def mn_genes_label():
    return T("motor-neuron genes", 34, GREEN).move_to([3.4, MN_YG - 0.95, 0])


class S14Mn2(SpokenScene):
    def construct(self):
        icon, bar, gt, u, lab = mn_single()
        self.add(icon, bar, u.L, u.I, u.N, u.tail, lab)
        shift = -0.85 * K - u.cxI
        u2 = mn_unit(+1, 0.85 * K, gt, K, "L")
        parts2 = [u2.L, u2.I, u2.N, u2.tail]
        for m in parts2:
            m.shift(RIGHT * 11.0)
        self.at("pairs of", lead=0.0)
        self.play(*[m.animate.shift(RIGHT * shift) for m in (u.L, u.I, u.N, u.tail)], FadeOut(lab),
                  *[m.animate.shift(LEFT * 11.0) for m in parts2], run_time=0.8)
        self.at("three part")
        self.play(FadeIn(unit_caption(), shift=UP * 0.1), run_time=0.6)
        self.at("promote")
        gl = mn_genes_label()
        self.play(bar.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), FadeIn(gl, shift=UP * 0.1), run_time=0.8)
        self.at("genes")
        self.play(Indicate(bar, color=GREEN, scale_factor=1.02), run_time=0.7)
        self.finish()


def mn_final():
    icon, bar, gt = mn_scene_parts()
    bar.set_stroke(GREEN).set_fill(GREEN, 0.5)
    ul = mn_unit(-1, -0.85 * K, gt, K, "R")
    ur = mn_unit(+1, 0.85 * K, gt, K, "L")
    return [icon, bar, ul.L, ul.I, ul.N, ul.tail, ur.L, ur.I, ur.N, ur.tail, mn_genes_label(), unit_caption()]


class S15Beat(NarratedScene):
    def construct(self):
        self.add(*mn_final())
        self.finish()


# ---- side by side (scene 16) ---------------------------------------------------------------------
class S16Both(SpokenScene):
    def construct(self):
        k = 1.55
        yg = -2.4
        gt = yg + 0.15
        cxv = -3.7
        bar_v = dna_bar(cxv, yg, w=4.6, color=ORANGE).set_fill(ORANGE, 0.5)
        bar_m = dna_bar(2.5, yg, w=7.0, color=GREEN).set_fill(GREEN, 0.5)
        hv = T("interneuron complex", 34, ORANGE, weight=BOLD).move_to([cxv, 3.4, 0])
        hm = T("motor-neuron complex", 34, GREEN, weight=BOLD).move_to([2.5, 3.4, 0])
        lv = T("V2 genes", 30, ORANGE).move_to([cxv, yg - 0.6, 0])
        lm = T("motor-neuron genes", 30, GREEN).move_to([2.5, yg - 0.6, 0])
        uv = v2_unit(cxv, gt, k, None)
        cxI = 3.7
        um = mn_unit(-1, cxI, gt, k, None)
        self.play(FadeIn(VGroup(bar_v, bar_m, hv, hm, lv, lm, uv.L, uv.N, um.L, um.I, um.N, um.tail)), run_time=0.8)
        self.at("in both")
        rv = SurroundingRectangle(uv.N, color=PURPLE, buff=0.16, corner_radius=0.2, stroke_width=8)
        rm = SurroundingRectangle(um.N, color=PURPLE, buff=0.16, corner_radius=0.2, stroke_width=8)
        self.play(Create(rv), Create(rm), Indicate(uv.N, color=PURPLE, scale_factor=1.06),
                  Indicate(um.N, color=PURPLE, scale_factor=1.06), run_time=1.0)
        self.at("what differs")
        self.play(FadeOut(rv), FadeOut(rm), run_time=0.4)
        self.at("the bridge")
        ri = SurroundingRectangle(um.I, color=YELLOW, buff=0.12, corner_radius=0.2, stroke_width=6)
        br = T("the bridge", 32, YELLOW).move_to([um.cxI, gt + 0.4, 0])
        self.play(Create(ri), FadeIn(br, shift=UP * 0.1), Indicate(um.I, color=YELLOW, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---- binding model (scenes 17-20) ---------------------------------------------------------------
TXK = {"none": -5.0, "half": 0.0, "equal": 5.0}
TRACK_Y = 1.95
BAR_Y = -0.25
BAR_H = 1.3
COLS = (-4.2, 0.0, 4.2)
BARCOLS = (ORANGE, GREEN, GREY)


def ratio_static(knob="equal"):
    banner = VGroup(RoundedRectangle(corner_radius=0.14, width=9.0, height=0.7, stroke_color=GOLD, stroke_width=2.5,
                                     fill_opacity=0),
                    T("Ideal binding model, not a measurement", 28, GOLD)).move_to([0, 3.3, 0])
    title = T("Isl1 relative to Lhx3", 32, YELLOW).move_to([0, 2.62, 0])
    track = Line([-5, TRACK_Y, 0], [5, TRACK_Y, 0], color=GREY, stroke_width=6)
    ticks = VGroup(*[Line([x, TRACK_Y - 0.15, 0], [x, TRACK_Y + 0.15, 0], color=GREY, stroke_width=4) for x in TXK.values()])
    tl = VGroup(T("none", 28, LIGHT).move_to([TXK["none"], 1.35, 0]),
                T("half as much", 28, LIGHT).move_to([TXK["half"], 1.35, 0]),
                T("equal", 28, LIGHT).move_to([TXK["equal"], 1.35, 0]))
    knob = Circle(radius=0.26, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                  fill_opacity=0.9).move_to([TXK[knob], TRACK_Y, 0])
    slider = VGroup(title, track, ticks, tl)
    bar_bg = Rectangle(width=10, height=BAR_H, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([0, BAR_Y, 0])
    bar_t = T("Where the Lhx3 sits", 28, LIGHT).move_to([0, 0.72, 0])
    names = VGroup(T("V2 interneuron\ncomplex", 26, ORANGE).move_to([COLS[0], -2.15, 0]),
                   T("motor-neuron\ncomplex", 26, GREEN).move_to([COLS[1], -2.15, 0]),
                   T("free, or held by\nIsl1 alone", 26, LIGHT).move_to([COLS[2], -2.15, 0]))
    cap = T("equal binding strengths; Lhx3 and NLI at ten times\nthe dissociation constant; single units, no DNA",
            26, LIGHT).move_to([0, -3.2, 0])
    return NS(banner=banner, slider=slider, knob=knob, bar_bg=bar_bg, bar_t=bar_t, names=names, cap=cap)


def segs_build(vals):
    x0 = -5.0
    g = VGroup()
    for i in range(3):
        w = 10 * vals[i] / 100
        g.add(Rectangle(width=max(w, 1e-3), height=BAR_H, stroke_width=0, fill_color=BARCOLS[i],
                        fill_opacity=0.65 if i < 2 else 0.35).move_to([x0 + w / 2, BAR_Y, 0]))
        x0 += w
    return g


def nums_build(vals):
    return VGroup(*[T(f"{int(round(vals[i]))}%", 44, BARCOLS[i] if i < 2 else LIGHT, weight=BOLD).move_to([COLS[i], -1.2, 0])
                    for i in range(3)])


def live_bar(v):
    """Segments and numbers that follow three trackers while an animation runs (clear the updaters afterwards)."""
    return (always_redraw(lambda: segs_build([t.get_value() for t in v])),
            always_redraw(lambda: nums_build([t.get_value() for t in v])))


class S17RatioQ(SpokenScene):
    def construct(self):
        r = ratio_static("none")
        self.add(r.banner)
        self.play(FadeIn(r.slider), FadeIn(r.knob), run_time=0.8)
        self.at("at all")
        self.play(r.knob.animate.move_to([TXK["equal"], TRACK_Y, 0]), run_time=1.6, rate_func=smooth)
        self.at("try a simple")
        self.play(Create(r.bar_bg), FadeIn(r.bar_t), run_time=0.9)
        self.at("binding model")
        self.play(FadeIn(r.names, shift=UP * 0.1), run_time=0.6)
        self.finish()


def ratio_base(knob):
    r = ratio_static(knob)
    return r, [r.slider, r.knob, r.banner, r.bar_bg, r.bar_t, r.names]


class S18Ratio(SpokenScene):
    def construct(self):
        r, base = ratio_base("equal")
        self.add(*base)
        self.at("equal amounts", lead=0.1)
        ring = Circle(radius=0.45, stroke_color=TEXT, stroke_width=4, fill_opacity=0).move_to(r.knob)
        self.play(FadeIn(r.cap), Create(ring), run_time=0.7)
        self.play(FadeOut(ring), run_time=0.3)
        self.at("about a quarter")
        v = [ValueTracker(0), ValueTracker(0), ValueTracker(0)]
        segs, nums = live_bar(v)
        self.add(segs, nums)
        self.play(v[0].animate.set_value(24), v[1].animate.set_value(37), v[2].animate.set_value(39),
                  run_time=1.4, rate_func=smooth)
        segs.clear_updaters()
        nums.clear_updaters()
        self.remove(segs, nums)
        self.add(segs_build([24, 37, 39]), nums_build([24, 37, 39]))
        self.at("interneuron complex")
        self.play(Indicate(r.names[0], color=ORANGE, scale_factor=1.12), run_time=1.0)
        self.finish()


class S19Ratio2(SpokenScene):
    def construct(self):
        r, base = ratio_base("equal")
        v = [ValueTracker(24), ValueTracker(37), ValueTracker(39)]
        segs, nums = live_bar(v)
        self.add(*base, r.cap, segs, nums)
        self.at("islet one", lead=0.1)     # the bar holds 24 / 37 / 39 until the narrator says "less islet one"
        self.play(FadeOut(r.cap), r.knob.animate.move_to([TXK["half"], TRACK_Y, 0]), v[0].animate.set_value(45),
                  v[1].animate.set_value(23), v[2].animate.set_value(32), run_time=0.6, rate_func=smooth)
        # hold on "half as much" (45 / 23 / 32) until the narrator says the conclusion
        self.at("binding alone", lead=0.1)
        concl = T("binding alone gives a mixture, not a switch", 34, TEXT, weight=BOLD).move_to([0, -3.2, 0])
        self.play(FadeIn(concl, shift=UP * 0.1), r.knob.animate.move_to([TXK["none"], TRACK_Y, 0]), v[0].animate.set_value(73),
                  v[1].animate.set_value(0), v[2].animate.set_value(27), run_time=1.0, rate_func=smooth)
        segs.clear_updaters()
        nums.clear_updaters()
        self.at("mixture")
        self.play(Indicate(r.bar_bg, color=TEXT, scale_factor=1.03), run_time=0.9)
        self.finish()


def padlock(cx, cy, s=2.0, open_=False):
    body = RoundedRectangle(corner_radius=0.18 * s, width=1.9 * s, height=1.5 * s, stroke_color=GREY, stroke_width=5,
                            fill_color=GREY, fill_opacity=0.3).move_to([cx, cy, 0])
    r = 0.55 * s
    yc = cy + 0.75 * s + 0.3 * s
    sh = VGroup(Arc(radius=r, start_angle=0, angle=PI, stroke_color=GREY, stroke_width=14, arc_center=[cx, yc, 0]),
                Line([cx - r, cy + 0.75 * s, 0], [cx - r, yc, 0], color=GREY, stroke_width=14),
                Line([cx + r, cy + 0.75 * s, 0], [cx + r, yc, 0], color=GREY, stroke_width=14))
    q = T("?", 96, TEXT, weight=BOLD).move_to(body)
    if open_:
        sh.shift(UP * 0.4 * s)
    return NS(body=body, sh=sh, q=q)


class S20Lock(SpokenScene):
    def construct(self):
        cell = Circle(radius=2.4, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.18).move_to([-3.7, 0.1, 0])
        clab = T("motor neuron", 36, GREEN, weight=BOLD).move_to(cell)
        pl = padlock(3.6, -0.5, 2.0, open_=True)
        conn = DashedLine([-1.3, -0.2, 0], [pl.body.get_left()[0] - 0.05, -0.2, 0], color=GREY, stroke_width=5)
        sep = T("shown by separate experiments (chapter 2)", 30, LIGHT).move_to([0, -3.4, 0])
        self.add(sep)
        self.play(GrowFromCenter(cell), FadeIn(clab), FadeIn(pl.body), FadeIn(pl.sh), FadeIn(pl.q), Create(conn),
                  run_time=0.6)
        self.at("a downstream regulator")
        reg = chip("downstream\nregulator", GREY, 28).move_to([0.15, 1.75, 0])
        a = arr([0.15, 1.2, 0], [0.15, -0.1, 0], GREY, w=4, tip=0.2)
        self.play(FadeIn(reg, shift=DOWN * 0.2), GrowArrow(a), run_time=0.7)
        self.at("lock the choice")
        self.play(pl.sh.animate.shift(DOWN * 0.8), Indicate(pl.body, color=TEXT, scale_factor=1.04), run_time=0.8)
        self.finish()


# ---- the idea (scenes 21-23) ---------------------------------------------------------------------
def idea_parts():
    card = RoundedRectangle(corner_radius=0.3, width=12.2, height=6.0, stroke_color=GOLD, stroke_width=4,
                            fill_color=GOLD, fill_opacity=0.06).move_to([0, 0, 0])
    head = T("The one idea", 48, GOLD, weight=BOLD).move_to([0, 2.15, 0])
    st = T("No single factor says motor neuron.", 42, TEXT, font=TITLE_FONT,
           t2c={"motor neuron": GREEN}).move_to([0, 1.05, 0])
    a = T("Here, identity depends on which complexes form.", 36, GREEN, font=TITLE_FONT)
    fit(a, max_w=11.2)
    a.move_to([0, -0.05, 0])
    b1 = T("That depends on which partners are present,", 36, TEXT, font=TITLE_FONT)
    fit(b1, max_w=11.2)
    b1.move_to([0, -1.1, 0])
    b2 = T("and in what ratio.", 36, YELLOW, font=TITLE_FONT).move_to([0, -1.95, 0])
    return NS(card=card, head=head, st=st, a=a, b1=b1, b2=b2)


class S21Idea(SpokenScene):
    def construct(self):
        o = idea_parts()
        for line in (o.a, o.b1, o.b2):
            dim(line, 0.22)
        self.add(o.a, o.b1, o.b2)
        self.play(FadeIn(o.card, scale=0.97), FadeIn(o.head, shift=DOWN * 0.1), run_time=0.5)
        self.at("single factor", lead=0.9)
        self.play(FadeIn(o.st, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S22Idea2(SpokenScene):
    def construct(self):
        o = idea_parts()
        for line in (o.a, o.b1, o.b2):
            dim(line, 0.22)
        self.add(o.card, o.head, o.st, o.a, o.b1, o.b2)
        self.at("here", lead=0.0)
        self.play(o.a.animate.set_opacity(1), run_time=0.8)
        self.at("that depends")
        self.play(o.b1.animate.set_opacity(1), run_time=0.7)
        self.at("and in what ratio")
        self.play(o.b2.animate.set_opacity(1), run_time=0.7)
        self.finish()


class S23Take(SpokenScene):
    def construct(self):
        lhx = chip("Lhx3", BLUE, 52).move_to([0, 2.85, 0])
        self.play(GrowFromCenter(lhx), run_time=0.6)
        self.at("one protein")
        self.play(Indicate(lhx, color=BLUE, scale_factor=1.1), run_time=0.7)
        self.at("different partners")
        p1 = chip("NLI", PURPLE, 38).move_to([-3.6, 0.65, 0])
        p2 = VGroup(chip("NLI", PURPLE, 38), T("+", 34, TEXT), chip("Isl1", YELLOW, 38)).arrange(RIGHT, buff=0.2).move_to([3.6, 0.65, 0])
        a1 = arr([-0.5, 2.3, 0], [-3.4, 1.2, 0], GREY, w=4, tip=0.22)
        a2 = arr([0.5, 2.3, 0], [3.4, 1.2, 0], GREY, w=4, tip=0.22)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(p1, shift=DOWN * 0.2), FadeIn(p2, shift=DOWN * 0.2), run_time=1.0)
        self.at("two different cells")
        c1 = Circle(radius=1.4, stroke_color=ORANGE, stroke_width=5, fill_color=ORANGE, fill_opacity=0.2).move_to([-3.6, -2.3, 0])
        c2 = Circle(radius=1.4, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.2).move_to([3.6, -2.3, 0])
        l_1 = T("V2\ninterneuron", 30, ORANGE, weight=BOLD).move_to(c1)
        l_2 = T("motor\nneuron", 30, GREEN, weight=BOLD).move_to(c2)
        b1 = arr([-3.6, 0.1, 0], [-3.6, -0.85, 0], ORANGE, w=5, tip=0.22)
        b2 = arr([3.6, 0.1, 0], [3.6, -0.85, 0], GREEN, w=5, tip=0.22)
        self.play(GrowArrow(b1), GrowArrow(b2), FadeIn(c1, scale=0.8), FadeIn(c2, scale=0.8), FadeIn(l_1), FadeIn(l_2),
                  run_time=1.0)
        self.finish()


class S24End(EndCard):
    LINE = "One protein, held by different partners, builds two different cells."
