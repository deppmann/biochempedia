"""Tools for development: marking a cell and its descendants  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = Cre recombinase (the enzyme, the actor)
  GOLD   = loxP sites
  RED    = the stop signal, and anything deleted or lost
  GREEN  = the fluorescent reporter: gene, its glow, a marked cell and its mark
  PURPLE = the floxed gene and its protein
  ORANGE = tamoxifen
  TEAL   = the modified estrogen receptor fused to Cre
  GREY   = cells, DNA lines, unmarked or dark things
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def cell(pos, r, on=False, dark_fill=True):
    c = Circle(radius=r, stroke_width=3 if r > 0.6 else 2.5,
               stroke_color=GREEN if on else GREY,
               fill_color=GREEN if on else GREY, fill_opacity=0.35 if on else 0.12)
    return c.move_to(pos)


def cell_on(c):
    return c.animate.set_stroke(GREEN).set_fill(GREEN, 0.38)


def edge(p, r1, q, r2, color=GREY):
    p, q = np.array(p, float), np.array(q, float)
    d = (q - p) / np.linalg.norm(q - p)
    return Line(p + d * r1, q - d * r2, color=color, stroke_width=3)


def mark_at(pos, w, on=True):
    """tiny DNA line with a green square: 'the mark written into the DNA'."""
    line = Line(LEFT * w / 2, RIGHT * w / 2, color=GREY, stroke_width=3)
    sq = Square(side_length=w * 0.26, stroke_width=0, fill_color=GREEN, fill_opacity=1)
    return VGroup(line, sq).move_to(pos)


def loxbar(x, k, y=0.0):
    return Rectangle(width=0.16 * k, height=1.05 * k, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([x * k, y, 0])


def reporter(k=1.0, labels=True, stop=True, on=False):
    """reporter strip: lox | STOP | lox | gene. Parts are exposed as attributes."""
    line = Line([-4.2 * k, 0, 0], [4.7 * k, 0, 0], color=GREY, stroke_width=4 if k > 0.5 else 3)
    l1, l2 = loxbar(-3.4, k), loxbar(-1.3, k)
    sbox = RoundedRectangle(corner_radius=0.08 * k, width=1.5 * k, height=0.8 * k, stroke_color=RED, stroke_width=3 if k > 0.5 else 2,
                            fill_color=RED, fill_opacity=0.25).move_to([-2.35 * k, 0, 0])
    st = VGroup(RoundedRectangle(corner_radius=0.08 * k, width=1.5 * k, height=0.8 * k, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(sbox), sbox)
    if labels:
        st.add(T("STOP", 24, RED, weight=BOLD).move_to(sbox))
    gbox = RoundedRectangle(corner_radius=0.08 * k, width=4.4 * k, height=0.9 * k, stroke_color=GREEN, stroke_width=3 if k > 0.5 else 2,
                            fill_color=GREEN, fill_opacity=0.9 if on else 0.06).move_to([2.2 * k, 0, 0])
    gbox.set_stroke(opacity=1 if on else 0.55)
    gn = VGroup(RoundedRectangle(corner_radius=0.08 * k, width=4.4 * k, height=0.9 * k, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(gbox), gbox)
    glabel = None
    if labels:
        glabel = T("fluorescent protein gene", 22, GREEN if not on else BG, weight=BOLD if on else NORMAL).move_to(gbox)
        if not on:
            glabel.set_opacity(0.7)
        gn.add(glabel)
    parts = [line, l1, l2, gn]
    if stop:
        parts.insert(1, st)
    g = VGroup(*parts)
    g.line, g.lox1, g.lox2, g.stop, g.gene, g.gbox, g.glabel = line, l1, l2, st, gn, gbox, glabel
    g.shift(LEFT * 0.25 * k)
    g.k = k
    return g


def gene_strip(k=1.0, with_lox=False, labels=False):
    """floxed-gene strip: left part | important part | right part, lox bars optional."""
    w = 3.6 * k
    left = Rectangle(width=2.4 * k, height=0.8 * k, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.25).move_to([-2.4 * k, 0, 0])
    mid = Rectangle(width=2.4 * k, height=0.8 * k, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.65).move_to([0, 0, 0])
    right = Rectangle(width=2.4 * k, height=0.8 * k, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.25).move_to([2.4 * k, 0, 0])
    g = VGroup(left, mid, right)
    g.left, g.mid, g.right = left, mid, right
    g.l1 = loxbar(-1.2, k * 1.0)
    g.l2 = loxbar(1.2, k * 1.0)
    g.add(g.l1, g.l2)
    if not with_lox:
        g.l1.set_opacity(0)
        g.l2.set_opacity(0)
    return g


def small_note(text, color=GREY, size=24):
    return T(text, size, color)


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Tools for following cells and genes"
    TITLE = "Marking a cell and its descendants"


# ---------------------------------------------------------------------------------------------
class S01Label(SpokenScene):
    """a cell with no label -> a mark written in the DNA is inherited -> Cre recombinase is the tool."""

    def construct(self):
        big = cell([0, 0.2, 0], 1.9)
        q = T("?", 110, GREY).move_to(big)
        self.play(FadeIn(big, scale=0.9), FadeIn(q), run_time=0.8)

        tag = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=2.3, height=1.0, stroke_color=RED, stroke_width=3), num_dashes=28)
        tag_t = T("label", 30, RED)
        tagg = VGroup(tag, tag_t).move_to([3.7, 1.9, 0])
        cross = Cross(tagg, stroke_color=RED, stroke_width=6).scale(0.8)
        self.at("no label")
        self.play(FadeIn(tagg, shift=LEFT * 0.2), run_time=0.4)
        self.play(Create(cross), run_time=0.4)

        anc = VGroup(Circle(radius=0.5, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.1),
                     T("?", 44, GREY)).move_to([-5.3, 0.2, 0])
        anc[1].move_to(anc[0])
        arrow = DashedLine([-4.7, 0.2, 0], [-2.1, 0.2, 0], color=GREY, dash_length=0.18, stroke_width=4).add_tip(tip_length=0.24)
        self.at("where it came")
        self.play(FadeIn(anc), Create(arrow), run_time=0.8)

        # the single cell becomes the root of a family
        root_pos, r0 = np.array([-5.0, 0.0, 0]), 0.95
        g1 = [np.array([-2.3, 1.3, 0]), np.array([-2.3, -1.3, 0])]
        g2 = [np.array([0.4, y, 0]) for y in (1.95, 0.65, -0.65, -1.95)]
        self.at("lineage is one family")
        self.play(FadeOut(VGroup(tagg, cross, anc, arrow, q)),
                  big.animate.scale(r0 / 1.9).move_to(root_pos), run_time=0.9)
        e1 = [edge(root_pos, r0, p, 0.62) for p in g1]
        c1 = [cell(p, 0.62) for p in g1]
        e2 = [edge(g1[i // 2], 0.62, p, 0.48) for i, p in enumerate(g2)]
        c2 = [cell(p, 0.48) for p in g2]
        self.play(*[Create(e) for e in e1], *[FadeIn(c, scale=0.7) for c in c1], run_time=0.8)
        fam = T("a lineage: one family", 30, TEXT).move_to([-1.0, -3.15, 0])
        self.play(FadeIn(fam), run_time=0.4)

        m0 = mark_at(root_pos, 1.2)
        ml = T("a mark in its DNA", 26, GREEN).move_to([-5.0, -1.55, 0])
        self.at("write a mark")
        self.play(FadeIn(m0, scale=0.6), FadeIn(ml), run_time=0.7)

        self.at("every descendant")
        m1 = [mark_at(p, 0.9) for p in g1]
        m2 = [mark_at(p, 0.7) for p in g2]
        self.play(*[FadeIn(m, scale=0.6) for m in m1], run_time=0.5)
        self.play(*[Create(e) for e in e2], *[FadeIn(c, scale=0.7) for c in c2],
                  *[FadeIn(m, scale=0.6) for m in m2], run_time=0.8)

        cre = chip("Cre recombinase", BLUE, size=34).move_to([4.15, 0.2, 0])
        self.at("enzyme called")
        self.play(FadeIn(cre, shift=LEFT * 0.3), run_time=0.7)
        self.play(Indicate(cre, color=BLUE, scale_factor=1.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Reporter(SpokenScene):
    """build the Cre-dependent reporter: gene, stop in front, loxP either side. Dark while the stop is in place."""

    def construct(self):
        cell_o = Ellipse(width=12.2, height=5.7, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.08).move_to([0, -0.15, 0])
        inside = T("inside one cell", 24, GREY).move_to([0, 2.25, 0])
        self.play(FadeIn(cell_o), FadeIn(inside), run_time=0.6)

        K = 1.2
        rep = reporter(K, labels=True).move_to([0, 0.15, 0])
        rep.shift(RIGHT * 0.0)
        # reporter(...) moved as a whole; individual parts keep their relative places
        self.at("fluorescent protein")
        self.play(Create(rep.line), FadeIn(rep.gene, shift=LEFT * 0.3), run_time=0.9)

        self.at("front of it")
        self.play(FadeIn(rep.stop, shift=DOWN * 0.5), run_time=0.6)

        lox_labels = VGroup(*[T("loxP", 22, GOLD).next_to(l, DOWN, buff=0.35) for l in (rep.lox1, rep.lox2)])
        self.at("each side")
        self.play(FadeIn(rep.lox1, scale=0.5), FadeIn(rep.lox2, scale=0.5), run_time=0.5)
        self.play(FadeIn(lox_labels), run_time=0.4)

        mid = (rep.lox1.get_center() + rep.lox2.get_center()) / 2
        bp = T("34 base pairs each", 24, GOLD).move_to([mid[0], rep.get_bottom()[1] - 1.0, 0])
        self.at("short DNA sequence")
        self.play(Indicate(VGroup(rep.lox1, rep.lox2), color=GOLD, scale_factor=1.25), FadeIn(bp), run_time=0.9)

        head = T("Cre-dependent reporter", 38, TEXT, font=TITLE_FONT).move_to([0, 1.65, 0])
        under = Line(rep.line.get_left() + UP * 1.0, rep.line.get_right() + UP * 1.0, color=GREY, stroke_width=2)
        under.move_to([0, 1.2, 0])
        self.at("reporter", nth=1)
        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.6)

        blk_x = (rep.lox2.get_center()[0] + rep.gbox.get_left()[0]) / 2
        blk = VGroup(Line([blk_x, 0.62, 0], [blk_x, -0.62, 0], color=RED, stroke_width=7))
        nr = T("not read", 24, GREY).move_to([rep.gbox.get_center()[0], rep.get_bottom()[1] - 0.6, 0])
        nr.shift(DOWN * 0.0)
        self.at("gene is not")
        self.play(Create(blk), FadeIn(nr), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cut(SpokenScene):
    """Cre appears in a cell, deletes the stop, the cell glows; only Cre-making cells do this."""

    def construct(self):
        pos = [np.array(p + (0,)) for p in [(-3.6, 1.45), (0, 1.45), (3.6, 1.45), (-3.6, -1.45), (0, -1.45), (3.6, -1.45)]]
        R = 1.2
        cells = [cell(p, R) for p in pos]
        strips = []
        for p in pos:
            s = reporter(0.26, labels=False).move_to(p + np.array([0, -0.35, 0]))
            strips.append(s)
        self.play(*[FadeIn(c, scale=0.9) for c in cells], *[FadeIn(s) for s in strips], run_time=0.9)

        def cre_chip(p):
            return chip("Cre", BLUE, size=24, pad=0.14).move_to(p + np.array([0, 0.5, 0]))

        def delete_stop(s):
            return [s.stop.animate.shift(UP * 0.5).set_opacity(0), s.lox2.animate.set_opacity(0)]

        def glow(i, s):
            return [cell_on(cells[i]), s.gbox.animate.set_fill(GREEN, 0.9).set_stroke(GREEN, opacity=1)]

        chips = {0: cre_chip(pos[0]), 4: cre_chip(pos[4])}
        self.at("appears in a")
        self.play(FadeIn(chips[0], scale=0.6), run_time=0.5)
        self.at("deletes the stop")
        self.play(s_flash := Indicate(strips[0].stop, color=RED, scale_factor=1.3), run_time=0.4)
        self.play(*delete_stop(strips[0]), run_time=0.5)
        self.at("the cell glows")
        self.play(*glow(0, strips[0]), run_time=0.7)

        note = T("Cre made in one cell type only", 28, BLUE).move_to([0, -3.2, 0])
        self.at("promoter active")
        self.play(FadeIn(chips[4], scale=0.6), FadeIn(note), run_time=0.6)
        self.at("make")
        self.play(Indicate(strips[4].stop, color=RED, scale_factor=1.3), run_time=0.4)
        self.play(*delete_stop(strips[4]), run_time=0.5)
        self.play(*glow(4, strips[4]), run_time=0.7)

        dark = T("no Cre: stop stays, cell stays dark", 28, GREY).move_to([0, -3.2, 0])
        self.at("neighbors stay dark")
        self.play(ReplacementTransform(note, dark),
                  *[Indicate(cells[i], color=GREY, scale_factor=1.06) for i in (1, 2, 3, 5)], run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Family(SpokenScene):
    """the marked cell divides; the edit is in its DNA, so every descendant glows."""

    def construct(self):
        xs = [-5.3, -2.7, -0.3, 2.0]
        rs = [0.8, 0.62, 0.48, 0.34]
        ys = [[0.0]]
        for g in range(1, 4):
            n = 2 ** g
            step = 0.85 * (8 / n)
            ys.append([(i - (n - 1) / 2) * step for i in range(n)])
        pts = [[np.array([xs[g], y, 0]) for y in ys[g]] for g in range(4)]
        root = cell(pts[0][0], rs[0], on=True)
        self.play(FadeIn(root, scale=0.8), run_time=0.7)

        cells = {(0, 0): root}
        edges = []

        def build(g):
            cs, es = [], []
            for i, p in enumerate(pts[g]):
                par = i // 2
                es.append(edge(pts[g - 1][par], rs[g - 1], p, rs[g], color=GREEN))
                c = cell(p, rs[g], on=True)
                cs.append(c)
                cells[(g, i)] = c
            return cs, es

        c1, e1 = build(1)
        self.at("cell divides")
        self.play(*[Create(e) for e in e1], *[FadeIn(c, scale=0.6) for c in c1], run_time=0.9)

        k = 0.36
        edited = reporter(k, labels=False, stop=False, on=True)
        edited.remove(edited.lox2)
        edited.move_to([4.7, 2.7, 0])
        elab = T("edited DNA", 26, TEXT).next_to(edited, UP, buff=0.3)
        self.at("in its DNA")
        self.play(FadeIn(elab), FadeIn(edited), run_time=0.6)

        self.at("both daughters inherit")
        self.play(*[Indicate(c, color=GREEN, scale_factor=1.15) for c in c1], run_time=0.8)

        c2, e2 = build(2)
        c3, e3 = build(3)
        self.at("every one of its")
        self.play(*[Create(e) for e in e2], *[FadeIn(c, scale=0.6) for c in c2], run_time=0.4)
        self.play(*[Create(e) for e in e3], *[FadeIn(c, scale=0.6) for c in c3], run_time=0.5)

        brace = Brace(VGroup(*c3), direction=RIGHT, color=GREEN, buff=0.15)
        lab = T("every descendant\nglows", 28, GREEN, line_spacing=0.8).next_to(brace, RIGHT, buff=0.2)
        self.at("descendants from then on")
        self.play(GrowFromCenter(brace), FadeIn(lab), run_time=0.8)

        perm = T("permanent", 36, TEXT, weight=BOLD).move_to([4.7, -2.1, 0])
        self.at("marking is permanent")
        self.play(FadeIn(perm, shift=UP * 0.15), run_time=0.5)
        lt = T("lineage tracing", 34, GREEN, font=TITLE_FONT).move_to([4.7, -3.0, 0])
        self.at("lineage tracing")
        self.play(FadeIn(lt, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Gene(SpokenScene):
    """a floxed gene: Cre cuts the important part out in one cell type only; CreER waits for tamoxifen."""

    def construct(self):
        CL, CR = np.array([-3.35, 0.1, 0]), np.array([3.35, 0.1, 0])
        R = 2.8
        cl, cr = cell(CL, R), cell(CR, R)
        K = 0.62
        gl = gene_strip(K).move_to(CL + np.array([0, -0.6, 0]))
        gr = gene_strip(K).move_to(CR + np.array([0, -0.6, 0]))
        gtl = T("gene", 26, PURPLE).next_to(gl, UP, buff=0.25)
        gtr = T("gene", 26, PURPLE).next_to(gr, UP, buff=0.25)
        self.play(FadeIn(cl, scale=0.9), FadeIn(cr, scale=0.9), run_time=0.7)
        self.at("remove a gene")
        self.play(FadeIn(gl), FadeIn(gr), FadeIn(gtl), FadeIn(gtr), run_time=0.7)

        impl = T("important part", 24, PURPLE).next_to(gl, DOWN, buff=0.35)
        impr = T("important part", 24, PURPLE).next_to(gr, DOWN, buff=0.35)
        self.at("important part")
        self.play(Indicate(gl.mid, color=PURPLE, scale_factor=1.15), Indicate(gr.mid, color=PURPLE, scale_factor=1.15),
                  FadeIn(impl), FadeIn(impr), run_time=0.9)

        self.at("sites")
        self.play(*[m.animate.set_opacity(1) for m in (gl.l1, gl.l2, gr.l1, gr.l2)], run_time=0.5)
        fl = T("floxed: works normally", 28, TEXT).move_to([0, -3.4, 0])
        self.at("allele is called")
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.5)

        cre = chip("Cre", BLUE, size=28).move_to(CL + np.array([0, 1.9, 0]))
        pro = T("promoter active in one cell type", 24, BLUE).move_to([0, -3.4, 0])
        self.at("Supply")
        self.play(FadeIn(cre, scale=0.6), ReplacementTransform(fl, pro), run_time=0.7)

        nocre = T("no Cre: gene intact", 24, GREY).move_to(CR + np.array([0, 1.9, 0]))
        self.at("deleted there alone")
        self.play(gl.mid.animate.set_stroke(RED).set_fill(RED, 0.5), FadeOut(impl), run_time=0.3)
        self.play(FadeOut(gl.mid, shift=UP * 1.0), gl.l2.animate.set_opacity(0), FadeIn(nocre), run_time=0.8)

        who = T("which tissue mattered?", 30, TEXT).move_to([0, -3.4, 0])
        self.at("which tissue mattered")
        self.play(ReplacementTransform(pro, who), run_time=0.5)

        # timing: Cre fused to a modified estrogen receptor waits for tamoxifen
        cre_er = VGroup(chip("Cre", BLUE, size=28, pad=0.16), chip("ER", TEAL, size=28, pad=0.16)).arrange(RIGHT, buff=0.04)
        cre_er.move_to(CL + np.array([0, 1.9, 0]))
        wait_t = T("fused to a modified estrogen receptor", 24, TEAL).move_to([0, -3.4, 0])
        self.at("for timing")
        old = VGroup(cl, gl, gtl, cre)
        cl2 = cell(CL, R)
        gl2 = gene_strip(K, with_lox=True).move_to(CL + np.array([0, -0.6, 0]))
        gtl2 = T("gene", 26, PURPLE).next_to(gl2, UP, buff=0.25)
        impl2 = T("important part", 24, PURPLE).next_to(gl2, DOWN, buff=0.35)
        new_lbl = T("a second cell", 26, TEXT).move_to(CL + np.array([0, -2.2, 0]))
        new = VGroup(cl2, gl2, gtl2, impl2, cre_er, new_lbl)
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(new, shift=UP * 0.2), ReplacementTransform(who, wait_t), run_time=0.6)

        tam_final = chip("tamoxifen", ORANGE, size=26).move_to(CL + np.array([0.95, 0.95, 0]))
        wait2 = T("the cut waits for the drug", 24, ORANGE).move_to([0, -3.4, 0])
        self.at("waits for the drug")
        self.play(FadeIn(tam_final, shift=LEFT * 0.4), ReplacementTransform(wait_t, wait2), run_time=0.6)
        self.at("tamoxifen")
        self.play(gl2.mid.animate.set_stroke(RED).set_fill(RED, 0.5), FadeOut(impl2), run_time=0.25)
        done = T("deleted after tamoxifen", 24, ORANGE).move_to([0, -3.4, 0])
        self.play(FadeOut(gl2.mid, shift=UP * 1.0), gl2.l2.animate.set_opacity(0), ReplacementTransform(wait2, done), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Trap(SpokenScene):
    """a reporter shows where Cre acted; it does not show where the floxed gene was lost."""

    def construct(self):
        C = np.array([-2.0, 0.0, 0])
        body = Ellipse(width=8.6, height=6.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.1).move_to(C)
        rep = reporter(0.5, labels=False, stop=False, on=True).move_to(C + np.array([0, 1.7, 0]))
        rlab = T("reporter: read", 26, GREEN).next_to(rep, UP, buff=0.3)
        self.play(FadeIn(body, scale=0.95), run_time=0.6)

        self.at("reporter cross")
        self.play(body.animate.set_stroke(GREEN).set_fill(GREEN, 0.28), FadeIn(rep), FadeIn(rlab), run_time=0.9)
        cre = chip("Cre acted here", BLUE, size=26).move_to(C + np.array([0, -3.35, 0]))
        cre.move_to([4.2, 1.7, 0])
        self.at("acted")
        self.play(FadeIn(cre, shift=LEFT * 0.3), run_time=0.6)

        gs = gene_strip(0.55, with_lox=True).move_to(C + np.array([0, -0.6, 0]))
        glab = T("floxed gene", 26, PURPLE).next_to(gs, UP, buff=0.3)
        qm = T("?", 44, RED, weight=BOLD).move_to(gs.mid.get_center())
        qm_bg = DashedVMobject(Rectangle(width=gs.mid.width, height=gs.mid.height, stroke_color=RED, stroke_width=3), num_dashes=20).move_to(gs.mid)
        self.at("does not tell")
        self.play(FadeIn(gs), FadeIn(glab), run_time=0.7)
        self.at("was lost")
        self.play(FadeIn(qm_bg), FadeIn(qm, scale=1.3), run_time=0.5)

        self.at("independently")
        two = T("two separate\ntargets", 26, GOLD, line_spacing=0.8).move_to([4.2, -0.1, 0])
        self.play(Indicate(VGroup(rep.lox1, rep.lox2), color=GOLD, scale_factor=1.4), FadeIn(two), run_time=0.7)
        self.play(Indicate(VGroup(gs.l1, gs.l2), color=GOLD, scale_factor=1.4), run_time=0.7)

        rng = np.random.default_rng(3)
        dots = VGroup(*[Dot(C + np.array([x, y, 0]), radius=0.1, color=PURPLE) for x, y in
                        [(-2.3, -1.5), (-1.3, -1.9), (-0.3, -1.5), (0.8, -1.9), (1.8, -1.5), (-2.9, -0.9)]])
        plab = T("protein made earlier stays", 26, PURPLE).move_to(C + np.array([0, -2.55, 0]))
        self.at("persists")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.1), FadeIn(plab), run_time=1.0)

        meas = chip("measure the loss", TEXT, size=28).move_to([4.2, -1.9, 0])
        marr = Arrow(meas.get_left(), gs.get_right() + RIGHT * 0.15, color=TEXT, stroke_width=4, buff=0.08)
        self.at("measure the loss")
        self.play(FadeIn(meas, shift=LEFT * 0.3), GrowArrow(marr), run_time=0.7)

        self.at("shows where")
        self.play(Indicate(rep, color=GREEN, scale_factor=1.12), run_time=0.7)
        self.at("gone")
        self.play(Indicate(qm, color=RED, scale_factor=1.6), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "A reporter shows where Cre acted, not where the gene is gone."
