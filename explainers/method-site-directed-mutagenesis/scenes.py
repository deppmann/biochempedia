"""Swap One Residue, Read the Result  (Biochemistrypedia methods film: engineered mutants)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  GREY   = proteins as labelled blocks, structure, de-emphasised text
  BLUE   = DNA: the gene, the template, the primer, the new strand
  YELLOW = the one chosen position / residue in the wild-type protein, question marks
  ORANGE = the change: the swapped residue, the mutant, the mutant protein
  PURPLE = phosphate (and ATP) and its imitation
  TEAL   = ligand, the partner that binds, the signal coming in
  GREEN  = it works, the response is on, a control that checks
  RED    = blocked, lost, the pitfall
  GOLD   = dates, source tags and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=22, color=GREY, **kw):
    return T(text, size, color, **kw)


def lines(*texts, size=22, color=TEXT, buff=0.1, align=ORIGIN, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow([a[0], a[1], 0], [b[0], b[1], 0], buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    return m


def rchip(text, color=YELLOW, size=22, pad=0.12, fo=0.22):
    return chip(text, color, size, pad=pad, fill_opacity=fo)


def chipl(texts, color=GREEN, size=22, pad=0.2):
    """A chip with several short lines of text."""
    g = lines(*texts, size=size, color=color, buff=0.06)
    box = RoundedRectangle(corner_radius=0.14, width=g.width + 2 * pad, height=g.height + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.14).move_to(g)
    return VGroup(box, g)


def tick(x, y, s=0.2, color=GREEN, w=5):
    return poly([[x - s, y], [x - s * 0.35, y - s * 0.8], [x + s, y + s * 0.9]], color, w)


def cross(x, y, s=0.2, color=RED, w=5):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def pbadge(x, y, r=0.26, text="P", color=PURPLE):
    c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35).move_to([x, y, 0])
    t = T(text, 22, color, weight=BOLD).move_to(c)
    return VGroup(c, t)


def blk(w, h, label="", color=GREY, size=22, fo=0.18, cx=0.0, cy=0.0, sw=2.5):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=sw,
                         fill_color=color, fill_opacity=fo).move_to([cx, cy, 0])
    g = VGroup(r)
    if label:
        g.add(T(label, size, color).move_to(r))
    return g


class Prot(VGroup):
    """A protein as a row of labelled blocks. segs = [(label, width), ...]."""

    def __init__(self, cx, cy, segs, h=0.7, color=GREY, gap=0.06, size=22):
        total = sum(w for _, w in segs) + gap * (len(segs) - 1)
        x = cx - total / 2
        self.lefts, self.widths, blocks = [], [], []
        for label, w in segs:
            blocks.append(blk(w, h, label, color, size, cx=x + w / 2, cy=cy))
            self.lefts.append(x)
            self.widths.append(w)
            x += w + gap
        self.cx_, self.cy_, self.h_ = cx, cy, h
        self.blocks = blocks
        super().__init__(*blocks)

    def xat(self, i, f=0.5):
        return self.lefts[i] + f * self.widths[i]

    def top(self):
        return self.cy_ + self.h_ / 2


def marker(x, y_top, text, color=YELLOW):
    """A residue chip above a block with a small arrow pointing down at the marked position."""
    c = rchip(text, color).move_to([x, y_top + 0.62, 0])
    t = Triangle(color=color, fill_color=color, fill_opacity=1).scale(0.11).rotate(PI).move_to([x, y_top + 0.17, 0])
    return VGroup(c, t)


def bases(letters, cx, y, colors=None, w=0.66, h=0.6, size=28):
    cells = VGroup()
    x0 = cx - w * len(letters) / 2
    for i, ch in enumerate(letters):
        col = colors[i] if colors else BLUE
        r = Rectangle(width=w, height=h, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.2)
        r.move_to([x0 + w * (i + 0.5), y, 0])
        cells.add(VGroup(r, M(ch, size, col).move_to(r)))
    return cells


def arc_at(c, r, a0, a1, color=BLUE, w=6):
    return Arc(radius=r, start_angle=a0, angle=a1 - a0, arc_center=[c[0], c[1], 0], stroke_color=color, stroke_width=w)


def pol(c, r, a):
    return [c[0] + r * np.cos(a), c[1] + r * np.sin(a), 0]


def gold_tag(text, pos, size=22):
    return lab(text, size, GOLD).move_to([pos[0], pos[1], 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Swap One Residue, Read the Result"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """A cloned gene and protein, but which part does which job? Tube tests miss a partner; no general change before 1978."""

    def construct(self):
        gene = RoundedRectangle(corner_radius=0.12, width=8.0, height=0.5, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.25).move_to([0, 3.1, 0])
        gl = T("cloned gene", 22, BLUE).move_to(gene)
        prot = Prot(0, 1.55, [("tail", 1.6), ("domain", 2.4), ("domain", 2.4), ("tail", 1.6)])
        down = arr([0, 2.8, 0], [0, 2.1, 0], GREY, w=4, tip=0.16)
        prot_l = lab("its protein", 22, GREY).move_to([4.9, 1.55, 0])
        self.at("A gene is cloned")
        self.play(FadeIn(gene), FadeIn(gl), run_time=0.6)
        self.at("its protein is known")
        self.play(GrowArrow(down), FadeIn(prot), FadeIn(prot_l), run_time=0.8)
        self.at("But which residue")
        qs = VGroup(*[T("?", 36, YELLOW, weight=BOLD).move_to([x, 2.35, 0]) for x in (-3.2, -1.5, 1.6, 3.3)])
        # keep the arrow clear: question marks sit either side of it
        self.play(LaggedStart(*[FadeIn(q, shift=DOWN * 0.1) for q in qs], lag_ratio=0.25), run_time=1.0)

        # --- a test in a tube
        self.at("A test in a tube")
        tube = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.06).move_to([-3.3, -1.55, 0])
        tube_l = lab("test in a tube", 22, GREY).move_to([-3.3, -0.4, 0])
        mini = Prot(-3.9, -1.3, [("domain", 2.0), ("domain", 2.0)], h=0.6)
        self.play(FadeIn(tube), FadeIn(tube_l), FadeIn(mini), run_time=0.6)
        self.at("can miss a part")
        read = chipl(["one activity:", "measured"], GREEN).move_to([3.4, -1.0, 0])
        self.play(FadeIn(read, shift=LEFT * 0.2), run_time=0.5)
        self.at("whose job is to hold")
        partner = rchip("partner", TEAL).move_to([mini.xat(1, 0.5), -2.45, 0])
        miss_box = DashedVMobject(Rectangle(width=2.5, height=1.7, stroke_color=RED, stroke_width=3)
                                  .move_to([mini.xat(1, 0.5), -1.95, 0]))
        miss = lines("holding a partner:", "missed", size=22, color=RED, buff=0.06).move_to([3.4, -2.4, 0])
        self.play(FadeIn(partner, shift=UP * 0.3), run_time=0.5)
        self.play(Create(miss_box), FadeIn(miss), run_time=0.6)

        # --- before 1978
        self.at("there was no widely")
        self.play(FadeOut(VGroup(tube, tube_l, mini, read, partner, miss_box, miss)), run_time=0.4)
        dna = RoundedRectangle(corner_radius=0.1, width=8.0, height=0.5, stroke_color=BLUE, stroke_width=3,
                               fill_color=BLUE, fill_opacity=0.2).move_to([0, -0.8, 0])
        spot = Rectangle(width=0.5, height=0.5, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                         fill_opacity=0.5).move_to([1.4, -0.8, 0])
        dna_l = lab("a known DNA sequence", 22, BLUE).move_to([-2.2, -0.8, 0])
        spot_l = lab("a chosen position", 22, YELLOW).move_to([1.4, -0.1, 0])
        none = lab("before 1978: no widely used way to change it", 26, GREY).move_to([0, -1.75, 0])
        self.play(FadeIn(dna), FadeIn(dna_l), FadeIn(spot), FadeIn(spot_l), run_time=0.5)
        self.play(FadeIn(none), run_time=0.4)
        self.at("Hutchison")
        new = Rectangle(width=0.5, height=0.5, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                        fill_opacity=0.55).move_to([1.4, -0.8, 0])
        yr = lab("1978: Hutchison, Smith and colleagues", 26, GOLD).move_to([0, -1.75, 0])
        self.play(FadeOut(none), ReplacementTransform(spot, new), run_time=0.4)
        self.play(FadeIn(yr), run_time=0.4)
        self.at("Now a site")
        ch1 = rchip("necessary?", YELLOW, 30).move_to([-2.3, -3.0, 0])
        ch2 = rchip("sufficient?", YELLOW, 30).move_to([2.3, -3.0, 0])
        self.play(FadeIn(ch1, shift=UP * 0.2), FadeIn(ch2, shift=UP * 0.2), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Primer(SpokenScene):
    """Choose a residue, choose its replacement (Ala, Asp), and a primer that carries the change."""

    def construct(self):
        prot = Prot(0, 1.9, [("domain", 2.4), ("domain", 2.8), ("tail", 2.2)], h=0.8)
        mx = prot.xat(1, 0.5)
        mk = marker(mx, prot.top(), "Tyr", YELLOW)
        hyp = lab("chosen from a hypothesis", 24, YELLOW).move_to([4.3, 2.9, 0])
        self.at("Pick the residue")
        self.play(FadeIn(prot), run_time=0.5)
        self.play(FadeIn(mk, shift=DOWN * 0.15), FadeIn(hyp), run_time=0.5)
        self.at("then choose what it becomes")
        self.play(Indicate(mk[0], color=YELLOW, scale_factor=1.2), run_time=0.7)

        segs = [("", 1.6), ("", 1.9), ("", 1.5)]
        xa, xd = -3.4, 3.4
        vy = -0.2
        va = Prot(xa, vy, segs, h=0.7)
        vd = Prot(xd, vy, segs, h=0.7)
        ma = marker(va.xat(1, 0.5), va.top(), "Ala", ORANGE)
        md = marker(vd.xat(1, 0.5), vd.top(), "Asp", ORANGE)
        by = vy + 0.35 + 0.62
        self.at("Alanine cannot accept")
        self.play(FadeIn(va), FadeIn(ma), run_time=0.5)
        bx = va.xat(1, 0.5) + 1.6
        pa = pbadge(bx, by)
        self.play(FadeIn(pa), run_time=0.2)
        self.play(pa.animate.shift(LEFT * 0.75), run_time=0.4)
        xr = cross(bx - 0.75, by, 0.22)
        self.play(FadeIn(xr), run_time=0.2)
        self.play(pa.animate.shift(RIGHT * 0.75), run_time=0.3)
        ta = lab("cannot accept a phosphate", 24, RED).move_to([xa, vy - 0.85, 0])
        self.play(FadeIn(ta), run_time=0.3)
        self.at("Aspartate has")
        self.play(FadeIn(vd), FadeIn(md), run_time=0.5)
        neg = Circle(radius=0.26, stroke_color=PURPLE, stroke_width=3, fill_opacity=0).move_to([vd.xat(1, 0.5) + 0.95, by, 0])
        negt = T("−", 30, PURPLE, weight=BOLD).move_to(neg)
        negg = VGroup(DashedVMobject(neg, num_dashes=10), negt)
        self.play(FadeIn(negg), run_time=0.4)
        self.at("that imitates one")
        td = lab("negative charge imitates one", 24, PURPLE).move_to([xd, vy - 0.85, 0])
        self.play(FadeIn(td), run_time=0.4)

        self.at("A short synthetic")
        py, ty = -0.9, -1.9
        pl = list("ATGAGTTCGTAG")
        tl = list("TACTCAGGCATC")
        cols_p = [BLUE] * 12
        cols_p[6] = ORANGE
        prim = bases(pl, 0, py, cols_p)
        prim_l = lab("primer", 24, BLUE).move_to([-5.3, py, 0])
        var = VGroup(va, vd, ma, md, pa, xr, ta, td, negg)
        self.play(FadeOut(VGroup(prot, mk, hyp)), run_time=0.3)
        self.play(var.animate.shift(UP * 2.3), run_time=0.6)
        self.play(FadeIn(prim, shift=UP * 0.2), FadeIn(prim_l), run_time=0.5)
        self.at("carries the change")
        cx6 = prim[6][0].get_center()[0]
        codon = Rectangle(width=0.66 * 3 + 0.08, height=0.74, stroke_color=YELLOW, stroke_width=3).move_to([cx6, py, 0])
        chg = lab("the change", 24, ORANGE).move_to([cx6, py + 0.62, 0])
        self.play(Create(codon), FadeIn(chg), run_time=0.5)
        self.at("bases long")
        n12 = lab("12 bases", 24, BLUE).move_to([5.3, py, 0])
        self.play(FadeIn(n12), run_time=0.4)
        self.at("matching the")
        temp = bases(tl, 0, ty, [BLUE] * 12)
        temp_l = lab("template", 24, BLUE).move_to([-5.3, ty, 0])
        illus = lab("illustrative sequence", 22, GREY).move_to([0, ty - 0.62, 0])
        bar = lab("phiX174 DNA", 24, BLUE).move_to([5.4, ty, 0])
        mism = cross(cx6, (py + ty) / 2, 0.16, RED, 5)
        self.play(FadeIn(temp, shift=DOWN * 0.2), FadeIn(temp_l), FadeIn(bar), FadeIn(illus), run_time=0.6)
        self.at("except for the change")
        self.play(Create(mism), Indicate(prim[6], color=ORANGE, scale_factor=1.3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Copy(SpokenScene):
    """Anneal, extend, seal; yields; plasmid whole copy then DpnI removes the parent."""

    def construct(self):
        C = [-2.7, 0.2]
        Rt, Rn = 2.4, 2.1
        ring = Circle(radius=Rt, stroke_color=GREY, stroke_width=6).move_to([C[0], C[1], 0])
        ring_l = lab("single-stranded circle", 24, GREY).move_to([C[0], C[1] - Rt - 0.5, 0])
        a_p0, a_p1 = np.radians(110), np.radians(70)
        primer = arc_at(C, Rn, a_p0, a_p1, BLUE, 8)
        tk = Line(pol(C, Rn - 0.3, np.radians(90)), pol(C, Rn + 0.3, np.radians(90)), color=ORANGE, stroke_width=8)
        p_lab = lab("primer", 26, BLUE).move_to([1.3, 2.8, 0])
        p_lead = Line([0.5, 2.8, 0], pol(C, Rt + 0.05, np.radians(75)), color=BLUE, stroke_width=2)

        self.at("The primer anneals")
        self.play(Create(ring), FadeIn(ring_l), run_time=0.6)
        self.play(Create(primer), FadeIn(tk), FadeIn(p_lab), Create(p_lead), run_time=0.7)
        self.at("A DNA polymerase")
        self.play(FadeOut(p_lab), FadeOut(p_lead), run_time=0.2)
        a_end = np.radians(110 - 360 + 8)
        ext = arc_at(C, Rn, a_p1, a_end, BLUE, 8)
        path = arc_at(C, 1.05, a_p1, a_end)
        pc = rchip("polymerase", ORANGE, pad=0.07).move_to(pol(C, 1.05, a_p1))
        self.play(FadeIn(pc), run_time=0.3)
        self.play(Create(ext, rate_func=linear), MoveAlongPath(pc, path, rate_func=linear), run_time=2.2)
        self.at("and DNA ligase seals")
        gap_a = np.radians(114)
        lig = rchip("ligase", GOLD).move_to([C[0], C[1], 0])
        glead = arr([C[0] - 0.4, C[1] + 0.4, 0], pol(C, Rn - 0.12, gap_a), GOLD, w=3, tip=0.14)
        self.play(FadeOut(pc), FadeIn(lig), GrowArrow(glead), run_time=0.5)
        seal = arc_at(C, Rn, np.radians(118), np.radians(110), GOLD, 9)
        self.play(Create(seal), run_time=0.5)
        self.play(FadeOut(lig), FadeOut(glead), seal.animate.set_color(BLUE), run_time=0.4)

        self.at("Fifteen percent")
        ax0, sc = 1.4, 0.05
        ay = -0.7
        ax = Line([ax0, ay, 0], [ax0 + 100 * sc, ay, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[VGroup(Line([ax0 + v * sc, ay, 0], [ax0 + v * sc, ay + 0.15, 0], color=GREY, stroke_width=3),
                                lab(t, 24, GREY).move_to([ax0 + v * sc, ay - 0.35, 0])) for v, t in ((0, "0"), (50, "50"), (100, "100"))])
        axl = lines("percent of progeny", "that are mutants", size=24, color=GREY, buff=0.05).move_to([ax0 + 2.5, ay - 1.15, 0])
        b1 = Rectangle(width=15 * sc, height=0.6, stroke_color=ORANGE, stroke_width=2, fill_color=ORANGE,
                       fill_opacity=0.5).move_to([ax0 + 7.5 * sc, 2.0, 0])
        b1l = lines("phiX174 phage, 1978:", "15%", size=24, color=ORANGE, buff=0.04, align=LEFT).move_to([ax0 + 1.4, 2.85, 0])
        b1l.align_to([ax0, 0, 0], LEFT)
        self.play(FadeIn(ax), FadeIn(ticks), FadeIn(axl), run_time=0.5)
        self.play(GrowFromEdge(b1, LEFT), FadeIn(b1l), run_time=0.7)
        self.at("Kunkel reached")
        b2 = Rectangle(width=20 * sc, height=0.6, stroke_color=GREEN, stroke_width=2, fill_color=GREEN,
                       fill_opacity=0.5).move_to([ax0 + 50 * sc, 0.4, 0])
        b2l = lines("Kunkel, 1985:", "40 to 60%", size=24, color=GREEN, buff=0.04, align=LEFT).move_to([ax0 + 1.4, 1.25, 0])
        b2l.align_to([ax0, 0, 0], LEFT)
        self.play(GrowFromCenter(b2), FadeIn(b2l), run_time=0.7)

        self.at("For plasmids")
        self.play(FadeOut(VGroup(ring, ring_l, primer, tk, ext, seal, ax, ticks, axl, b1, b1l, b2, b2l)), run_time=0.5)
        PC = [0.0, 0.2]
        par = Circle(radius=Rt, stroke_color=GREY, stroke_width=6).move_to([PC[0], PC[1], 0])
        par_l = lab("parental plasmid, methylated", 24, GREY).move_to([0, PC[1] - Rt - 0.5, 0])
        self.at("Quick Change")
        self.play(Create(par), FadeIn(par_l), run_time=0.7)
        pa1, pa2 = np.radians(150), np.radians(330)
        pr1 = arc_at(PC, Rn, pa1 - 0.35, pa1 + 0.35, BLUE, 9)
        pr2 = arc_at(PC, Rn, pa2 - 0.35, pa2 + 0.35, BLUE, 9)
        t1 = Line(pol(PC, Rn - 0.3, pa1), pol(PC, Rn + 0.3, pa1), color=ORANGE, stroke_width=8)
        t2 = Line(pol(PC, Rn - 0.3, pa2), pol(PC, Rn + 0.3, pa2), color=ORANGE, stroke_width=8)
        self.play(FadeIn(pr1), FadeIn(pr2), FadeIn(t1), FadeIn(t2), run_time=0.5)
        self.at("copies the whole plasmid")
        n1 = arc_at(PC, Rn, pa1 + 0.35, pa1 + 0.35 - 2 * np.pi + 0.7, BLUE, 7)
        n2 = arc_at(PC, Rn - 0.35, pa2 + 0.35, pa2 + 0.35 - 2 * np.pi + 0.7, BLUE, 5)
        self.play(Create(n1, rate_func=linear), Create(n2, rate_func=linear), run_time=1.5)
        self.at("two complementary")
        l1 = lab("mutant primer", 24, ORANGE).move_to([-5.0, 1.9, 0])
        l2 = lab("mutant primer", 24, ORANGE).move_to([5.0, -1.5, 0])
        ld1 = Line([-3.8, 1.8, 0], pol(PC, Rn + 0.35, pa1), color=ORANGE, stroke_width=2)
        ld2 = Line([3.8, -1.4, 0], pol(PC, Rn + 0.35, pa2), color=ORANGE, stroke_width=2)
        self.play(FadeIn(l1), FadeIn(l2), Create(ld1), Create(ld2), run_time=0.6)
        self.at("then destroys")
        dpn = rchip("Dpn I", RED, 28).move_to([0, 3.2, 0])
        self.play(FadeOut(VGroup(l1, l2, ld1, ld2)), FadeIn(dpn, shift=DOWN * 0.2), run_time=0.5)
        self.at("methylated")
        self.play(par.animate.set_stroke(RED, 6, 0.3), FadeIn(cross(0, PC[1] + Rt, 0.3, RED, 7)), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Kinds(SpokenScene):
    """Tyr to Phe; kinase-dead; dominant-negative; then wild-type gene against mutant gene in cells."""

    def construct(self):
        CX = [-4.35, 0.0, 4.35]
        HY = 3.3

        def head(cx, text):
            return fit(lab(text, 26, TEXT, weight=BOLD), max_w=4.0).move_to([cx, HY, 0])

        def two(a, b, color, pos):
            return lines(a, b, size=24, color=color, buff=0.06).move_to(pos)

        # ----- column 1
        c1 = CX[0]
        h1 = head(c1, "Tyrosine to phenylalanine")
        p1 = Prot(c1, 1.3, [("protein", 3.6)], h=0.9)
        m1 = marker(c1 - 0.5, p1.top(), "Tyr", YELLOW)
        ph1 = pbadge(c1 + 0.55, p1.top() + 0.62)
        t1a = two("loses only the", "hydroxyl", ORANGE, [c1, -0.2, 0])
        t1b = two("cannot be", "phosphorylated", RED, [c1, -1.5, 0])
        self.at("Tyrosine to phenylalanine")
        self.play(FadeIn(h1), FadeIn(p1), FadeIn(m1), FadeIn(ph1), run_time=0.6)
        f1 = marker(c1 - 0.5, p1.top(), "Phe", ORANGE)
        self.play(ReplacementTransform(m1, f1), run_time=0.6)
        self.at("loses only the hydroxyl")
        self.play(FadeIn(t1a), run_time=0.4)
        self.at("cannot be phosphorylated")
        self.play(FadeIn(t1b), FadeIn(cross(c1 + 0.55, p1.top() + 0.62, 0.3, RED, 6)), run_time=0.5)

        # ----- column 2
        c2 = CX[1]
        h2 = head(c2, "Kinase-dead")

        def receptor(cx, color=GREY):
            return VGroup(blk(1.5, 0.6, "", color, cx=cx, cy=2.3), blk(1.5, 1.0, "kinase", color, cx=cx, cy=1.5))

        rl = receptor(c2 - 0.85)
        rr = receptor(c2 + 0.85)
        lig = [Circle(radius=0.17, stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.6).move_to([x, 2.85, 0])
               for x in (c2 - 0.85, c2 + 0.85)]
        lys = rchip("Lys", YELLOW, pad=0.08).move_to([c2 - 0.85, 0.6, 0])
        lyl = Line([c2 - 0.85, 0.9, 0], [c2 - 0.85, 1.0, 0], color=YELLOW, stroke_width=3)
        atp = rchip("ATP", PURPLE, pad=0.1).move_to([c2 - 0.85, -0.05, 0])
        t2a = two("still folds, pairs", "and binds ligand", GREEN, [c2, -0.95, 0])
        t2b = two("cannot transfer", "phosphate", RED, [c2, -2.05, 0])
        self.at("kinase dead mutant")
        self.play(FadeIn(h2), FadeIn(rl), FadeIn(rr), run_time=0.5)
        self.at("changes the lysine")
        self.play(FadeIn(lys), FadeIn(lyl), run_time=0.3)
        self.at("that holds")
        self.play(FadeIn(atp, shift=UP * 0.2), run_time=0.4)
        lys2 = rchip("changed", ORANGE, pad=0.08).move_to(lys)
        self.play(ReplacementTransform(lys, lys2), run_time=0.4)
        self.at("can still fold")
        self.play(*[FadeIn(g, shift=DOWN * 0.2) for g in lig], FadeIn(t2a), run_time=0.6)
        self.at("but cannot transfer phosphate")
        tr = arr([c2 - 0.3, -0.05, 0], [c2 + 0.8, 0.95, 0], PURPLE, w=4, tip=0.16)
        self.play(FadeIn(t2b), GrowArrow(tr), run_time=0.4)
        self.play(FadeIn(cross(c2 + 0.25, 0.45, 0.22, RED, 6)), run_time=0.3)

        # ----- column 3
        c3 = CX[2]
        h3 = head(c3, "Dominant-negative")
        rn = VGroup(blk(1.5, 0.6, "normal", GREEN, cx=c3 - 0.85, cy=2.3), blk(1.5, 1.0, "kinase", GREEN, cx=c3 - 0.85, cy=1.5))
        rm = VGroup(blk(1.5, 0.6, "mutant", ORANGE, cx=c3 + 0.85, cy=2.3),
                    DashedVMobject(Rectangle(width=1.5, height=1.0, stroke_color=ORANGE, stroke_width=2.5).move_to([c3 + 0.85, 1.5, 0]), num_dashes=24),
                    lab("no kinase", 22, ORANGE).move_to([c3 + 0.85, 1.5, 0]))
        t3a = two("pairs with normal", "partners", GREEN, [c3, -0.95, 0])
        t3b = two("cannot pass the", "signal on", RED, [c3, -2.05, 0])
        self.at("A dominant negative receptor")
        self.play(FadeIn(h3), FadeIn(rn), run_time=0.5)
        self.at("can lack its kinase domain")
        self.play(FadeIn(rm), run_time=0.6)
        self.at("It pairs with normal")
        self.play(rn.animate.shift(RIGHT * 0.1), rm.animate.shift(LEFT * 0.1), FadeIn(t3a), run_time=0.6)
        self.at("cannot pass the signal on")
        sg = arr([c3, 0.9, 0], [c3, 0.0, 0], TEAL, w=5, tip=0.16)
        self.play(FadeIn(t3b), GrowArrow(sg), run_time=0.4)
        self.play(FadeIn(cross(c3, 0.45, 0.25, RED, 6)), run_time=0.3)

        # ----- compare in cells
        self.at("Compare the mutant")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        cw, cm = -3.4, 3.4
        cell_w = Ellipse(width=4.8, height=3.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([cw, 0.2, 0])
        cell_m = Ellipse(width=4.8, height=3.6, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([cm, 0.2, 0])
        en_w = rchip("own wild-type protein", GREY, 22).move_to([cw, 0.85, 0])
        en_m = rchip("own wild-type protein", GREY, 22).move_to([cm, 0.85, 0])
        gw = rchip("added: wild-type gene", BLUE, 24).move_to([cw, -0.35, 0])
        gm = rchip("added: mutant gene", ORANGE, 24).move_to([cm, -0.35, 0])
        self.play(FadeIn(cell_w), FadeIn(cell_m), FadeIn(en_w), FadeIn(en_m), FadeIn(gm, shift=DOWN * 0.4), run_time=0.4)
        self.at("with wild type")
        self.play(FadeIn(gw, shift=DOWN * 0.4), run_time=0.5)
        same = chipl(["identical conditions"], TEAL, 26).move_to([0, 3.0, 0])
        a1 = arr([-0.9, 2.7, 0], [cw + 0.8, 1.95, 0], TEAL, w=4, tip=0.16)
        a2 = arr([0.9, 2.7, 0], [cm - 0.8, 1.95, 0], TEAL, w=4, tip=0.16)
        self.at("under identical conditions")
        self.play(FadeIn(same), GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        q1 = chipl(["result: ?"], YELLOW, 26).move_to([cw, -2.7, 0])
        q2 = chipl(["result: ?"], YELLOW, 26).move_to([cm, -2.7, 0])
        self.play(FadeIn(q1), FadeIn(q2), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """Sufficiency vs need; then the real Feig and Cooper 1988 case."""

    def construct(self):
        def row(y, sig, sigc, blk_t, blk_c, resp, respc, tag, tagc, arrow_x=False):
            s = rchip(sig, sigc, 26, pad=0.18).move_to([-4.7, y, 0])
            a1 = arr([-3.6, y, 0], [-2.9, y, 0], GREY, w=4, tip=0.16)
            b = blk(3.0, 1.0, blk_t, blk_c, size=24, cx=-1.3, cy=y)
            a2 = arr([0.3, y, 0], [1.2, y, 0], GREY, w=4, tip=0.16)
            r = rchip(resp, respc, 26, pad=0.18).move_to([2.8, y, 0])
            t = lab(tag, 32, tagc, weight=BOLD).move_to([5.3, y, 0])
            xs = VGroup()
            if arrow_x:
                xs.add(cross(0.75, y, 0.26, RED, 6))
            return VGroup(s, a1, b, a2, r), xs, t

        r1, x1, t1 = row(1.5, "no signal", TEAL, "active mutant", ORANGE, "response ON", GREEN, "sufficient", GREEN)
        r2, x2, t2 = row(-0.8, "signal", TEAL, "blocking mutant", ORANGE, "no response", RED, "needed", RED, arrow_x=True)
        self.at("A mutant that acts")
        self.play(FadeIn(r1[0]), FadeIn(r1[1]), FadeIn(r1[2]), run_time=0.6)
        self.play(FadeIn(r1[3]), FadeIn(r1[4]), run_time=0.6)
        self.at("suggests sufficiency")
        self.play(FadeIn(t1, shift=LEFT * 0.2), run_time=0.4)
        self.at("One that blocks")
        self.play(FadeIn(r2[0]), FadeIn(r2[1]), FadeIn(r2[2]), run_time=0.6)
        self.play(FadeIn(r2[3]), Create(x2), FadeIn(r2[4]), run_time=0.6)
        self.at("suggests need")
        self.play(FadeIn(t2, shift=LEFT * 0.2), run_time=0.4)

        self.at("Feig and Cooper")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)
        head = lab("A real case: Feig and Cooper, 1988", 28, GOLD, weight=BOLD).move_to([0, 3.3, 0])
        ras = Prot(-3.0, 1.5, [("H-Ras", 4.6)], h=0.9, size=26)
        sm = marker(-2.0, ras.top(), "Ser 17", YELLOW)
        self.play(FadeIn(head), FadeIn(ras), FadeIn(sm), run_time=0.6)
        self.at("to asparagine")
        sm2 = marker(-2.0, ras.top(), "Asn 17", ORANGE)
        self.play(ReplacementTransform(sm, sm2), run_time=0.6)
        self.at("Its affinity for")
        gt = lines("affinity for GTP:", "20 to 40 fold lower", size=24, color=TEXT, buff=0.06).move_to([3.3, 1.5, 0])
        ga = arr([5.5, 1.95, 0], [5.5, 1.05, 0], RED, w=5, tip=0.18)
        self.play(FadeIn(gt), GrowArrow(ga), run_time=0.6)

        rng = np.random.RandomState(4)

        def dish(cx, n, color, label_t, lc):
            c = Circle(radius=0.95, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([cx, -0.75, 0])
            pts = []
            while len(pts) < n:
                p = rng.uniform(-0.65, 0.65, 2)
                if np.hypot(*p) < 0.65 and all(np.hypot(*(p - q)) > 0.32 for q in pts):
                    pts.append(p)
            d = VGroup(*[Dot([cx + p[0], -0.75 + p[1], 0], radius=0.09, color=color) for p in pts])
            lb = lab(label_t, 24, lc).move_to([cx, -2.05, 0])
            return VGroup(c, d), lb

        d1, l1 = dish(-4.2, 11, GREEN, "expected", GREY)
        d2, l2 = dish(0.0, 2, ORANGE, "Asn-17 Ras", ORANGE)
        d3, l3 = dish(4.2, 10, GREEN, "plus activated ras", GREEN)
        sch = lab("schematic dishes: drug-resistant colonies", 24, GREY).move_to([0, 0.6, 0])
        self.at("Cells with it")
        self.play(FadeIn(d1), FadeIn(l1), FadeIn(sch), run_time=0.5)
        self.play(FadeIn(d2), FadeIn(l2), run_time=0.5)
        self.at("so it inhibited")
        self.play(Indicate(d2, color=RED, scale_factor=1.15), run_time=0.6)
        self.at("reversed that")
        self.play(FadeIn(d3), FadeIn(l3), run_time=0.6)

        cy = 1.4
        src = rchip("Src", GREY, 34, pad=0.2).move_to([-4.0, cy, 0])
        ras_c = rchip("Ras", GREY, 34, pad=0.2).move_to([-1.2, cy, 0])
        raf = rchip("Raf", GREY, 34, pad=0.2).move_to([1.6, cy, 0])
        a1 = arr([-3.2, cy, 0], [-2.0, cy, 0], GREY, w=5, tip=0.2)
        a2 = arr([-0.4, cy, 0], [0.8, cy, 0], GREY, w=5, tip=0.2)
        vmos = rchip("v-mos: resistant", GREEN, 26, pad=0.14).move_to([4.8, cy, 0])
        vraf = rchip("v-raf: resistant", GREEN, 26, pad=0.14).move_to([1.6, cy - 1.2, 0])
        vsrc = rchip("v-src: not resistant", RED, 26, pad=0.14).move_to([-4.0, cy - 1.2, 0])
        self.at("resisted it")
        self.play(FadeOut(VGroup(ras, sm2, gt, ga, sch, d1, l1, d2, l2, d3, l3)), run_time=0.3)
        self.play(FadeIn(src), FadeIn(ras_c), FadeIn(raf), FadeIn(a1), FadeIn(a2), run_time=0.5)
        self.play(FadeIn(vmos), FadeIn(vraf), run_time=0.5)
        self.at("did not")
        self.play(FadeIn(vsrc), run_time=0.4)
        self.at("That places")
        bt = lab("Ras sits between Src and Raf, in this system", 30, GOLD).move_to([0, -1.6, 0])
        self.play(FadeIn(bt), Indicate(ras_c, color=GOLD, scale_factor=1.25), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """Three traps: a wrecked protein, an imperfect mimic, overexpression; and the controls."""

    def construct(self):
        CX = [-4.35, 0.0, 4.35]
        HY = 3.3

        def head(cx, text):
            return fit(lab(text, 26, TEXT, weight=BOLD), max_w=4.0).move_to([cx, HY, 0])

        def two(a, b, color, pos):
            return lines(a, b, size=24, color=color, buff=0.06).move_to(pos)

        c1 = CX[0]
        h1 = head(c1, "A wrecked protein")
        p1 = Prot(c1, 1.7, [("", 1.15), ("", 1.2), ("", 1.15)], h=0.9)
        m1 = marker(c1, p1.top(), "swap", ORANGE)
        t1 = two("folding or expression", "damaged instead", RED, [c1, 0.3, 0])
        k1 = chipl(["control: expression", "and a retained", "activity"], GREEN, 24).move_to([c1, -1.7, 0])
        self.at("A mutation can damage")
        self.play(FadeIn(h1), FadeIn(p1), FadeIn(m1), run_time=0.6)
        self.at("instead of the chosen function")
        self.play(p1.blocks[0].animate.rotate(0.35).shift(LEFT * 0.12 + DOWN * 0.25),
                  p1.blocks[2].animate.rotate(-0.4).shift(RIGHT * 0.12 + DOWN * 0.3),
                  p1.blocks[1].animate.shift(UP * 0.12), VGroup(*[b[0] for b in p1.blocks]).animate.set_color(RED),
                  FadeIn(t1), run_time=0.9)
        self.at("so confirm expression")
        self.play(FadeIn(k1, shift=UP * 0.2), run_time=0.5)

        c2 = CX[1]
        h2 = head(c2, "An imperfect mimic")
        asp_c = Circle(radius=0.34, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.35).move_to([c2 + 1.15, 1.95, 0])
        asp_m = T("−", 40, ORANGE, weight=BOLD).move_to([c2 + 1.15, 1.2, 0])
        asp_t = two("aspartate:", "one charge", ORANGE, [c2 + 1.15, 0.4, 0])
        pho = pbadge(c2 - 1.15, 1.95, r=0.5)
        pho_m = VGroup(T("−", 40, PURPLE, weight=BOLD).move_to([c2 - 1.4, 1.2, 0]), T("−", 40, PURPLE, weight=BOLD).move_to([c2 - 0.9, 1.2, 0]))
        pho_t = two("phosphate:", "two charges", PURPLE, [c2 - 1.15, 0.4, 0])
        sm = lab("and smaller", 24, ORANGE).move_to([c2 + 1.15, -0.4, 0])
        k2 = chipl(["control: a second", "line of evidence,", "such as a kinase", "inhibitor"], GREEN, 24).move_to([c2, -1.9, 0])
        self.at("An aspartate mimic")
        self.play(FadeIn(h2), FadeIn(asp_c), run_time=0.5)
        self.at("one charge where")
        self.play(FadeIn(asp_m), FadeIn(asp_t), run_time=0.5)
        self.at("phosphate has two")
        self.play(FadeIn(pho), FadeIn(pho_m), FadeIn(pho_t), run_time=0.6)
        self.at("and is smaller")
        self.play(FadeIn(sm), asp_c.animate.scale(0.7), run_time=0.5)
        self.at("so add a second line")
        self.play(FadeIn(k2, shift=UP * 0.2), run_time=0.5)

        c3 = CX[2]
        h3 = head(c3, "Overexpression")
        cell = Circle(radius=1.1, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to([c3, 1.9, 0])
        rng = np.random.RandomState(9)
        pts = []
        while len(pts) < 22:
            p = rng.uniform(-0.9, 0.9, 2)
            if np.hypot(*p) < 0.88 and all(np.hypot(*(p - q)) > 0.3 for q in pts):
                pts.append(p)
        dots = VGroup(*[Dot([c3 + p[0], 1.9 + p[1], 0], radius=0.09, color=ORANGE) for p in pts])
        mut_l = lab("mutant protein", 24, ORANGE).move_to([c3, 0.55, 0])
        side = two("effects beyond", "the intended block", RED, [c3, -0.3, 0])
        k3a = chipl(["control: wild-type protein", "at matching levels"], GREEN, 22).move_to([c3, -1.4, 0])
        k3b = chipl(["and a rescue:", "restores the", "blocked response"], GREEN, 22).move_to([c3, -2.85, 0])
        self.at("Dominant negatives work")
        self.play(FadeIn(h3), FadeIn(cell), run_time=0.5)
        self.at("through overexpression")
        self.play(LaggedStart(*[FadeIn(d, scale=2.0) for d in dots], lag_ratio=0.05), FadeIn(mut_l), run_time=1.0)
        self.at("beyond the intended block")
        self.play(FadeIn(side), run_time=0.5)
        self.at("wild type protein")
        self.play(FadeIn(k3a, shift=UP * 0.2), run_time=0.5)
        self.at("and a rescue")
        self.play(FadeIn(k3b, shift=UP * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Found1(SpokenScene):
    """Src Y527F (constitutively active) and the Notch / Lin-12 intracellular domain."""

    def construct(self):
        src = Prot(-3.0, 1.5, [("head", 2.0), ("kinase", 2.8), ("tail", 1.8)], h=0.9)
        m416 = marker(src.xat(1, 0.5), src.top(), "Tyr 416", YELLOW)
        m527 = marker(src.xat(2, 0.5), src.top(), "Tyr 527", YELLOW)
        src_l = lab("Src", 24, GREY).move_to([-3.0, 0.7, 0])
        tag1 = gold_tag("Kmiecik and Shalloway, 1987", [-3.0, 0.2], 24)
        self.at("tyrosine")
        self.play(FadeIn(src), FadeIn(src_l), FadeIn(m416), FadeIn(m527), run_time=0.7)
        self.at("to phenylalanine")
        f527 = marker(src.xat(2, 0.5), src.top(), "Phe 527", ORANGE)
        self.play(ReplacementTransform(m527, f527), run_time=0.6)
        on = chipl(["transforming and", "kinase activities:", "strongly activated"], GREEN, 24).move_to([4.2, 1.5, 0])
        self.at("strongly activated")
        self.play(VGroup(*[b[0] for b in src.blocks]).animate.set_color(GREEN), FadeIn(on, shift=LEFT * 0.2), FadeIn(tag1), run_time=0.6)
        self.at("an added change")
        f416 = marker(src.xat(1, 0.5), src.top(), "Phe 416", ORANGE)
        off = chipl(["transforming and", "kinase activities:", "suppressed (reduced)"], YELLOW, 24).move_to([4.2, 1.5, 0])
        self.play(ReplacementTransform(m416, f416), run_time=0.5)
        self.play(VGroup(*[b[0] for b in src.blocks]).animate.set_color(GREY), ReplacementTransform(on, off), run_time=0.6)

        self.at("made truncated")
        full = Prot(-3.6, -1.7, [("outside", 1.7), ("membrane", 1.9), ("inside", 1.5)], h=0.9)
        fl = lines("worm Lin-12 /", "fly Notch receptor", size=24, color=GREY, buff=0.04).move_to([-3.6, -0.8, 0])
        self.play(FadeIn(full), FadeIn(fl), run_time=0.6)
        self.at("only their intracellular")
        tr = Prot(0.9, -1.7, [("inside", 1.7)], h=0.9, color=ORANGE)
        tl = lines("truncated worm Lin-12", "and fly Notch", size=24, color=ORANGE, buff=0.04).move_to([1.0, -0.8, 0])
        ar = arr([-0.95, -1.7, 0], [-0.15, -1.7, 0], GREY, w=4, tip=0.16)
        self.play(GrowArrow(ar), FadeIn(tr), FadeIn(tl), run_time=0.7)
        self.at("These caused")
        res = chipl(["associated with", "constitutive activity:", "cell-fate changes"], GREEN, 24).move_to([4.6, -1.3, 0])
        self.play(FadeIn(res, shift=LEFT * 0.2), run_time=0.5)
        self.at("independent of")
        ind = lines("does not depend on", "endogenous gene function", size=24, color=GREEN, buff=0.05).move_to([4.5, -2.55, 0])
        tag2 = gold_tag("Struhl, Fitzgerald and Greenwald, 1993", [-2.2, -2.9], 24)
        self.play(FadeIn(ind), FadeIn(tag2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Found2(SpokenScene):
    """Truncated activin receptor neuralizes Xenopus explants; a caution; the rule."""

    def construct(self):
        full = Prot(-3.6, 2.4, [("outside", 1.7), ("membrane", 1.9), ("inside", 1.5)], h=0.9)
        fl = lab("activin receptor", 24, GREY).move_to([-3.6, 1.65, 0])
        tag = gold_tag("Hemmati-Brivanlou and Melton, 1994", [0, 0.95], 24)
        self.at("In")
        self.play(FadeIn(full), FadeIn(fl), FadeIn(tag), run_time=0.6)
        self.at("a truncated")
        tr = Prot(2.4, 2.4, [("outside", 1.7), ("membrane", 1.9)], h=0.9, color=ORANGE)
        gone = DashedVMobject(Rectangle(width=1.5, height=0.9, stroke_color=ORANGE, stroke_width=2.5).move_to(
            [2.4 + (3.6 + 0.06) / 2 + 0.06 + 0.75, 2.4, 0]), num_dashes=24)
        tl = lab("truncated: part deleted", 24, ORANGE).move_to([3.2, 1.65, 0])
        ar = arr([-0.8, 2.4, 0], [0.1, 2.4, 0], GREY, w=4, tip=0.16)
        self.play(GrowArrow(ar), FadeIn(tr), FadeIn(gone), FadeIn(tl), run_time=0.7)
        self.at("that would become")
        ey = -0.5
        e1 = Ellipse(width=3.8, height=1.8, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12).move_to([-3.3, ey, 0])
        e1t = lab("Xenopus explant", 24, GREY).move_to(e1)
        e1l = lab("would become epidermal cells", 24, GREY).move_to([-3.3, ey - 1.3, 0])
        e2 = Ellipse(width=3.8, height=1.8, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.18).move_to([3.3, ey, 0])
        e2t = lab("neural tissue", 28, GREEN, weight=BOLD).move_to(e2)
        e2l = lab("with the truncated receptor", 24, GREEN).move_to([3.3, ey - 1.3, 0])
        mid = arr([-1.2, ey, 0], [1.2, ey, 0], ORANGE, w=5, tip=0.2)
        self.play(FadeIn(e1), FadeIn(e1t), FadeIn(e1l), run_time=0.6)
        self.play(GrowArrow(mid), FadeIn(e2), FadeIn(e2t), FadeIn(e2l), run_time=0.8)
        self.at("That receptor also blocks")
        cau = chipl(["it also blocks related ligands:", "it blocked more than activin"], RED, 26).move_to([0, -3.0, 0])
        self.play(FadeIn(cau, shift=UP * 0.2), run_time=0.6)

        self.at("Confirm expression and")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        rule = lines("Confirm expression and activity,", "then add a second line", "of evidence.", size=40, color=TEXT, buff=0.2)
        rule_box = SurroundingRectangle(rule, color=GOLD, stroke_width=3, buff=0.45, corner_radius=0.2)
        head_t = lab("KEEP THIS RULE", 26, GOLD, weight=BOLD).next_to(rule_box, UP, buff=0.25)
        VGroup(rule, rule_box, head_t).move_to([0, 0, 0])
        self.play(FadeIn(head_t), Create(rule_box), run_time=0.5)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "Confirm expression and activity, then add a second line of evidence."
