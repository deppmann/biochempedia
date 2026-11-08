"""Evolution of development: same protein, different switch  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the Pitx1 gene and its protein
  PURPLE = the pelvis, and the pelvic enhancer Pel
  GOLD   = the jaw / head tissue (and its enhancer)
  GREEN  = marine allele / marine fish
  ORANGE = Paxton allele / Paxton fish
  PINK   = transcription factors
  YELLOW = the question, the mapped region
  WHITE  = the methods ladder
  RED    = broken, deleted, a bad outcome
  GREY   = outlines, chromosomes, de-emphasized, promoter / marker, Bear Paw Lake fry
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E88FB4"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def fish_body(color, pos, scale=1.0):
    """Level, right-facing silhouette: body, tail, eye. Centered on pos."""
    st = dict(stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.22)
    body = Ellipse(width=3.6, height=1.4, **st)
    tail = Polygon([-1.7, 0, 0], [-2.6, 0.65, 0], [-2.6, -0.65, 0], **st)
    eye = Dot([1.2, 0.2, 0], radius=0.07, color=TEXT)
    g = VGroup(body, tail, eye)
    g.scale(scale, about_point=ORIGIN).shift(np.array([pos[0], pos[1], 0]))
    return g


def spines(color, pos, scale=1.0, lens=(1.0, 1.0)):
    """Two pelvic spines hanging from the belly. lens are lengths in unscaled units."""
    starts = [np.array([0.05, -0.69, 0]), np.array([0.40, -0.68, 0])]
    dirs = [np.array([-0.35, -1.0, 0]), np.array([-0.10, -1.0, 0])]
    out = VGroup()
    for s, d, L in zip(starts, dirs, lens):
        d = d / np.linalg.norm(d)
        out.add(Line(s * scale + np.array([pos[0], pos[1], 0]), (s + d * L) * scale + np.array([pos[0], pos[1], 0]),
                     color=color, stroke_width=7))
    return out


def belly(pos, scale=1.0, dx=0.2, dy=-0.35):
    return np.array([pos[0] + dx * scale, pos[1] + dy * scale, 0])


def lamp(pos, r=0.2):
    return Circle(radius=r, stroke_width=0, fill_color=PURPLE, fill_opacity=0.95).move_to(pos)


class S00Title(TitleCard):
    LESSON = "Evolution of development"
    TITLE = "Same protein, different switch"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """Two fish, one unchanged protein, one question."""

    def construct(self):
        mpos, ppos = (-3.4, 0.6), (3.4, 0.6)
        m_fish = fish_body(GREEN, mpos)
        p_fish = fish_body(ORANGE, ppos)
        m_lbl = T("marine", 30, GREEN).move_to([-3.4, 2.2, 0])
        p_lbl = T("Paxton Lake benthic", 30, ORANGE).move_to([3.4, 2.2, 0])
        self.play(FadeIn(m_fish, shift=RIGHT * 0.3), FadeIn(m_lbl), run_time=0.8)
        m_sp = spines(GREEN, mpos, 1.0, (1.0, 1.0))
        self.at("two spines")
        self.play(Create(m_sp), run_time=0.8)
        self.at("lake")
        self.play(FadeIn(p_fish, shift=LEFT * 0.3), FadeIn(p_lbl), run_time=0.8)
        none = T("most have no pelvic bones", 24, ORANGE).move_to([3.4, -0.9, 0])
        self.at("pelvic bones")
        self.play(FadeIn(none, shift=UP * 0.1), run_time=0.7)

        g1 = chip("Pitx1 gene", BLUE, 26).move_to([-3.4, -1.95, 0])
        g2 = chip("Pitx1 gene", BLUE, 26).move_to([3.4, -1.95, 0])
        self.at("gene most")
        self.play(FadeIn(g1, shift=UP * 0.2), FadeIn(g2, shift=UP * 0.2), run_time=0.7)
        pr1 = chip("Pitx1 protein", BLUE, 26).move_to([-3.4, -2.95, 0])
        pr2 = chip("Pitx1 protein", BLUE, 26).move_to([3.4, -2.95, 0])
        same = T("= same", 28, TEXT).move_to([0, -2.95, 0])
        self.at("its protein")
        self.play(FadeIn(pr1, shift=UP * 0.2), FadeIn(pr2, shift=UP * 0.2), run_time=0.7)
        self.at("unchanged")
        self.play(FadeIn(same), run_time=0.5)
        q = T("How can the part shrink, with the protein unchanged?", 30, YELLOW).move_to([0, 3.15, 0])
        self.at("How can")
        self.play(FadeIn(q, shift=DOWN * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Switch(SpokenScene):
    """The gene has separate enhancers; break the pelvic one."""

    def construct(self):
        gene = RoundedRectangle(corner_radius=0.14, width=4.2, height=0.8, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.22).move_to([0, 1.2, 0])
        gname = T("Pitx1 gene", 28, BLUE).move_to(gene)
        self.play(FadeIn(gene), FadeIn(gname), run_time=0.6)
        prot = chip("protein binds DNA", BLUE, 24).move_to([0, -0.7, 0])
        a_p = arr([0, 0.78, 0], [0, -0.2, 0], BLUE)
        self.at("makes a protein")
        self.play(GrowArrow(a_p), FadeIn(prot, shift=DOWN * 0.15), run_time=0.7)
        mice = T("mice without it: malformed hind limbs", 22, RED).move_to([0, -1.75, 0])
        self.at("mice without")
        self.play(FadeIn(mice, shift=UP * 0.1), run_time=0.7)

        # enhancers
        ej = chip("jaw enhancer", GOLD, 26).move_to([-4.3, 2.85, 0])
        ep = chip("pelvic enhancer", PURPLE, 26).move_to([4.3, 2.85, 0])
        aj = arr([-3.0, 2.55, 0], [-1.5, 1.68, 0], GOLD)
        ap = arr([3.0, 2.55, 0], [1.5, 1.68, 0], PURPLE)
        self.at("several switches")
        self.play(FadeOut(mice), FadeIn(ej, shift=DOWN * 0.2), FadeIn(ep, shift=DOWN * 0.2), run_time=0.6)
        self.play(GrowArrow(aj), GrowArrow(ap), run_time=0.6)
        self.at("short stretch")
        self.play(Indicate(ej, color=GOLD, scale_factor=1.12), Indicate(ep, color=PURPLE, scale_factor=1.12), run_time=1.0)

        # tissues
        frames, bars, names = {}, {}, {}
        for key, x, col, nm in (("jaw", -4.6, GOLD, "jaw: Pitx1 use"), ("pel", 4.6, PURPLE, "pelvis: Pitx1 use")):
            fr = Rectangle(width=2.2, height=2.6, stroke_color=GREY, stroke_width=2.5).move_to([x, -1.55, 0])
            bar = Rectangle(width=1.0, height=2.2, stroke_width=0, fill_color=col, fill_opacity=0.85)
            bar.move_to(fr.get_bottom() + UP * 1.1 + UP * 0.1)
            frames[key], bars[key] = fr, bar
            names[key] = T(nm, 24, col).move_to([x, -3.3, 0])
        ag = arr([-1.3, 0.78, 0], [-3.9, -0.28, 0], GOLD)
        ar = arr([1.3, 0.78, 0], [3.9, -0.28, 0], PURPLE)
        self.at("raises a gene's use")
        self.play(FadeIn(frames["jaw"]), FadeIn(frames["pel"]), GrowArrow(ag), GrowArrow(ar), run_time=0.6)
        self.play(GrowFromEdge(bars["jaw"], DOWN), GrowFromEdge(bars["pel"], DOWN),
                  FadeIn(names["jaw"]), FadeIn(names["pel"]), run_time=0.9)
        self.at("serve the jaw")
        self.play(Indicate(ej, color=GOLD, scale_factor=1.12), Indicate(bars["jaw"], color=GOLD, scale_factor=1.05), run_time=0.9)
        self.at("pelvis")
        self.play(Indicate(ep, color=PURPLE, scale_factor=1.12), Indicate(bars["pel"], color=PURPLE, scale_factor=1.05), run_time=0.9)

        # break the pelvic switch
        self.at("Break the pelvic switch")
        x1 = Line(ep.get_corner(UL) + [0.1, -0.1, 0], ep.get_corner(DR) + [-0.1, 0.1, 0], color=RED, stroke_width=7)
        x2 = Line(ep.get_corner(DL) + [0.1, 0.1, 0], ep.get_corner(UR) + [-0.1, -0.1, 0], color=RED, stroke_width=7)
        new_bar = Rectangle(width=1.0, height=0.45, stroke_width=0, fill_color=PURPLE, fill_opacity=0.85)
        new_bar.move_to(frames["pel"].get_bottom() + UP * 0.1 + UP * 0.225)
        self.play(ep[0].animate.set_stroke(RED), Create(x1), Create(x2), FadeOut(ap), FadeOut(ar), run_time=0.7)
        self.play(Transform(bars["pel"], new_bar), run_time=0.9)
        self.at("light stays on")
        self.play(Indicate(bars["jaw"], color=GOLD, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Hybrid(SpokenScene):
    """Mapped region -> cis or trans? -> one nucleus holding both alleles."""

    def construct(self):
        chrom = RoundedRectangle(corner_radius=0.12, width=11.0, height=0.4, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.3).move_to([0, 1.9, 0])
        chrom_lbl = T("chromosome", 24, GREY).move_to([-4.6, 2.55, 0])
        self.play(FadeIn(chrom), FadeIn(chrom_lbl), run_time=0.7)
        region = Rectangle(width=3.4, height=0.7, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                           fill_opacity=0.18).move_to([0.6, 1.9, 0])
        reg_lbl = T("mapped region", 26, YELLOW).move_to([0.6, 1.1, 0])
        gtick = Rectangle(width=0.22, height=0.9, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to([0.6, 1.9, 0])
        glbl = T("Pitx1", 26, BLUE).move_to([0.6, 2.75, 0])
        self.at("found a region")
        self.play(FadeIn(region), FadeIn(reg_lbl), FadeIn(gtick), FadeIn(glbl), run_time=0.8)
        others = VGroup(*[Rectangle(width=0.16, height=0.6, stroke_width=0, fill_color=GREY, fill_opacity=0.9).move_to([x, 1.9, 0])
                          for x in (-0.6, -0.1, 1.1, 1.6, 2.0)])
        self.at("many genes")
        self.play(LaggedStart(*[FadeIn(o, scale=0.6) for o in others], lag_ratio=0.15), run_time=1.0)

        cis = chip("cis:\nbeside the gene", PURPLE, 28).move_to([-3.4, -0.9, 0])
        trans = chip("trans:\nanother gene's product", PINK, 28).move_to([3.4, -0.9, 0])
        self.at("beside the gene")
        self.play(FadeIn(cis, shift=UP * 0.2), run_time=0.7)
        self.at("another gene")
        self.play(FadeIn(trans, shift=UP * 0.2), run_time=0.7)

        # one nucleus
        nuc = Circle(radius=3.0, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([0, -0.2, 0])
        self.at("can test for")
        self.play(FadeOut(VGroup(chrom, chrom_lbl, region, reg_lbl, gtick, glbl, others, cis, trans)),
                  FadeIn(nuc, scale=0.8), run_time=0.9)

        def allele(y, col):
            bar = RoundedRectangle(corner_radius=0.1, width=3.6, height=0.4, stroke_color=col, stroke_width=3,
                                   fill_color=col, fill_opacity=0.3).move_to([0, y, 0])
            tick = Rectangle(width=0.22, height=0.8, stroke_width=0, fill_color=BLUE, fill_opacity=1).move_to([0, y, 0])
            return VGroup(bar, tick)
        am = allele(0.9, GREEN)
        ap = allele(-1.1, ORANGE)
        lm = T("marine allele", 26, GREEN).move_to([-4.65, 0.9, 0])
        lp = T("Paxton allele", 26, ORANGE).move_to([-4.65, -1.1, 0])
        self.at("marine allele")
        self.play(FadeIn(am, shift=RIGHT * 0.2), FadeIn(lm), run_time=0.7)
        self.at("Paxton allele")
        self.play(FadeIn(ap, shift=RIGHT * 0.2), FadeIn(lp), run_time=0.7)
        nl = T("one nucleus", 26, GREY).move_to([4.6, 1.9, 0])
        nline = Line([3.3, 1.7, 0], [2.6, 1.3, 0], color=GREY, stroke_width=2.5)
        self.at("one nucleus")
        self.play(FadeIn(nl), Create(nline), run_time=0.6)

        pts = [(-2.2, 0.0), (-1.2, -0.2), (-0.2, 0.15), (0.9, -0.05), (1.9, 0.1), (2.2, -0.35), (-1.8, -0.4), (0.4, -0.4)]
        dots = VGroup(*[Dot([x, y, 0], radius=0.13, color=PINK) for x, y in pts])
        flab = T("same\ntranscription\nfactors", 24, PINK).move_to([4.75, -1.0, 0])
        self.at("same transcription")
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.1), FadeIn(flab), run_time=1.2)
        self.play(*[d.animate.shift(RIGHT * 0.3 * (1 if i % 2 else -1)) for i, d in enumerate(dots)], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Ratio(SpokenScene):
    """Invented 90:10 vs 50:50 split; cis verdict; then the real 2010 result."""

    def construct(self):
        tag = T("invented example: Pitx1 transcripts in F1 hybrids", 24, GREY).move_to([0, 3.15, 0])
        self.play(FadeIn(tag), run_time=0.6)
        bot, H, W = -1.7, 4.0, 1.5

        def seg(x, y0, h, col):
            return Rectangle(width=W, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x, bot + y0 + h / 2, 0])
        px, jx = -3.6, 1.6
        pm = seg(px, 0, 3.6, GREEN)
        pp = seg(px, 3.6, 0.4, ORANGE)
        jm = seg(jx, 0, 2.0, GREEN)
        jp = seg(jx, 2.0, 2.0, ORANGE)
        pname = T("pelvis", 28, PURPLE).move_to([px, -2.3, 0])
        jname = T("jaw", 28, GOLD).move_to([jx, -2.3, 0])
        self.play(FadeIn(pname), FadeIn(jname), run_time=0.4)
        pml = T("marine 90%", 26, GREEN).move_to([px + W / 2 + 1.35, bot + 1.8, 0])
        self.at("pelvic transcripts")
        self.play(GrowFromEdge(pm, DOWN), FadeIn(pml), run_time=0.9)
        ppl = T("Paxton 10%", 26, ORANGE).move_to([px + W / 2 + 1.35, bot + 3.8, 0])
        self.at("Paxton allele")
        self.play(GrowFromEdge(pp, DOWN), FadeIn(ppl), run_time=0.7)
        jml = T("marine 50%", 26, GREEN).move_to([jx + W / 2 + 1.3, bot + 1.0, 0])
        jpl = T("Paxton 50%", 26, ORANGE).move_to([jx + W / 2 + 1.3, bot + 3.0, 0])
        self.at("jaw")
        self.play(GrowFromEdge(jm, DOWN), GrowFromEdge(jp, DOWN), FadeIn(jml), FadeIn(jpl), run_time=0.9)
        verdict = T("Shared factors: the Paxton allele itself is less active (cis)", 24, TEXT).move_to([0, -3.1, 0])
        self.at("factors are shared")
        self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.7)
        self.at("pelvis but")
        self.play(Circumscribe(VGroup(pm, pp), color=PURPLE, buff=0.15), run_time=1.0)

        # real result
        inv = VGroup(tag, pm, pp, jm, jp, pname, jname, pml, ppl, jml, jpl, verdict)
        head = T("real hybrids: Chan and colleagues, 2010", 28, TEXT).move_to([0, 3.0, 0])
        self.at("In 2010")
        self.play(FadeOut(inv), run_time=0.6)
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)

        def tile(x, nm, col):
            fr = Rectangle(width=5.4, height=4.4, stroke_color=GREY, stroke_width=2.5).move_to([x, -0.2, 0])
            t = T(nm, 30, col).move_to([x, 1.5, 0])
            c = chip("Paxton allele", ORANGE, 28).move_to([x, 0.3, 0])
            return fr, t, c
        fr1, t1, c1 = tile(-3.2, "pelvic tissue", PURPLE)
        fr2, t2, c2 = tile(3.2, "head tissue", GOLD)
        self.at("real version")
        self.play(FadeIn(fr1), FadeIn(fr2), FadeIn(t1), FadeIn(t2), FadeIn(c1), FadeIn(c2), run_time=0.8)
        dn = Arrow([-3.2, -0.45, 0], [-3.2, -1.45, 0], buff=0, color=TEXT, stroke_width=7, tip_length=0.3)
        lo = T("lower", 30, TEXT).move_to([-3.2, -1.95, 0])
        self.at("lower in pelvic")
        self.play(GrowArrow(dn), FadeIn(lo), run_time=0.7)
        nl = T("not lower", 30, GREY).move_to([3.2, -1.2, 0])
        self.at("not in head")
        self.play(FadeIn(nl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reporter(SpokenScene):
    """Pel, a reporter assay (marine drives, Paxton does not), then rescue in Bear Paw Lake fry."""

    def construct(self):
        # --- Pel upstream of the gene -----------------------------------------------------------
        pel = chip("Pel", PURPLE, 32).move_to([-3.2, 0.6, 0])
        gene = RoundedRectangle(corner_radius=0.14, width=4.0, height=0.8, stroke_color=BLUE, stroke_width=3,
                                fill_color=BLUE, fill_opacity=0.22).move_to([2.0, 0.6, 0])
        gname = T("Pitx1 gene", 28, BLUE).move_to(gene)
        up = T("upstream", 26, GREY).move_to([-0.6, -0.3, 0])
        a = arr(pel.get_right(), gene.get_left(), PURPLE)
        self.play(FadeIn(gene), FadeIn(gname), FadeIn(pel), run_time=0.7)
        self.at("upstream")
        self.play(GrowArrow(a), FadeIn(up), run_time=0.6)

        # --- reporter constructs ---------------------------------------------------------------
        hm = T("marine Pel", 30, GREEN).move_to([-3.3, 3.1, 0])
        hp = T("Paxton Pel", 30, ORANGE).move_to([3.3, 3.1, 0])

        def construct_row(x, y=2.15):
            c1 = chip("Pel", PURPLE, 24)
            c2 = chip("promoter", GREY, 24)
            c3 = chip("marker", GREY, 24)
            row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3).move_to([x, y, 0])
            return row
        rm, rp = construct_row(-3.3), construct_row(3.3)
        self.at("reporter assay")
        self.play(FadeOut(VGroup(gene, gname, a, up)), Transform(pel, rm[0]), run_time=0.8)
        self.play(FadeIn(rm[1:], shift=LEFT * 0.2), FadeIn(hm), run_time=0.7)
        self.at("visible marker")
        self.play(Indicate(rm[2], color=TEXT, scale_factor=1.2), run_time=0.8)
        self.at("embryos")
        arm = arr([-3.3, 1.65, 0], [-3.3, 1.0, 0], GREY)
        self.play(GrowArrow(arm), run_time=0.5)

        mpos = (-3.3, 0.1)
        mfish = fish_body(GREEN, mpos, 0.85)
        glow = lamp(belly(mpos, 0.85), 0.26)
        mlbl = T("pelvic expression", 26, PURPLE).move_to([-3.3, -1.5, 0])
        self.at("Marine")
        self.play(FadeIn(mfish), run_time=0.5)
        self.play(FadeIn(glow, scale=0.4), FadeIn(mlbl), run_time=0.6)

        self.at("Paxton version")
        self.play(FadeIn(rp, shift=DOWN * 0.1), FadeIn(hp), run_time=0.7)
        slash = Line(rp[0].get_corner(UL) + [0.05, -0.05, 0], rp[0].get_corner(DR) + [-0.05, 0.05, 0], color=RED, stroke_width=7)
        slash2 = Line(rp[0].get_corner(DL) + [0.05, 0.05, 0], rp[0].get_corner(UR) + [-0.05, -0.05, 0], color=RED, stroke_width=7)
        self.at("carried a deletion")
        self.play(Create(slash), Create(slash2), rp[0][0].animate.set_stroke(RED), run_time=0.6)
        arp = arr([3.3, 1.65, 0], [3.3, 1.05, 0], GREY)
        minis = VGroup(*[fish_body(ORANGE, (1.35 + 1.3 * (i % 4), 0.6 - 0.95 * (i // 4)), 0.22) for i in range(8)])
        plbl = T("pelvic expression in 0 of 8 fish", 26, RED).move_to([3.3, -1.5, 0])
        self.at("gave none")
        self.play(GrowArrow(arp), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in minis], lag_ratio=0.12), run_time=1.0)
        self.play(FadeIn(plbl), run_time=0.5)
        qlbl = T("a reporter asks: can this sequence drive expression?", 26, GREY).move_to([0, -2.7, 0])
        self.at("A reporter shows")
        self.play(FadeIn(qlbl, shift=UP * 0.1), run_time=0.7)

        # --- rescue ------------------------------------------------------------------------------
        self.at("Rescue comes closer")
        left_over = VGroup(pel, rm[1:], hm, arm, mfish, glow, mlbl, rp, slash, slash2, hp, arp, minis, plbl, qlbl)
        self.play(FadeOut(left_over), run_time=0.8)
        head = T("Bear Paw Lake fry", 30, GREY).move_to([0, 3.15, 0])
        ch = chip("marine Pel + Pitx1 minigene", PURPLE, 28).move_to([0, 2.2, 0])
        upos, ipos = (-3.4, 0.2), (3.4, 0.2)
        uf = fish_body(GREY, upos, 0.8)
        usp = spines(GREY, upos, 0.8, (0.18, 0.18))
        ifs = fish_body(GREY, ipos, 0.8)
        isp = spines(GREY, ipos, 0.8, (0.6, 0.35))
        ul = T("uninjected sibling", 26, GREY).move_to([-3.4, -1.7, 0])
        il = T("injected:\nspines variably enhanced", 26, PURPLE).move_to([3.4, -1.85, 0])
        self.at("Pit")
        self.play(FadeIn(head), FadeIn(ch, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(uf), FadeIn(ifs), FadeIn(ul), run_time=0.6)
        self.add(usp)
        ai = arr([1.4, 1.85, 0], [3.0, 1.15, 0], PURPLE)
        self.at("minigene")
        self.play(GrowArrow(ai), run_time=0.5)
        sp_small = spines(GREY, ipos, 0.8, (0.18, 0.18))
        self.add(sp_small)
        self.at("variably enhanced")
        self.play(Transform(sp_small, isp), FadeIn(il), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Ladder(SpokenScene):
    """PelB deletion in mice (about 0.85 of control) and the five-rung ladder of methods."""

    def construct(self):
        title = T("mouse hind-limb Pitx1 RNA\nrelative units", 24, GREY).move_to([-2.8, 3.0, 0])
        base = -2.0
        bw = 1.6
        cx, mx = -4.2, -1.4
        axis = Line([-5.4, base, 0], [-0.2, base, 0], color=GREY, stroke_width=3)
        ctrl = Rectangle(width=bw, height=3.6, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to([cx, base + 1.8, 0])
        ref = DashedLine([-5.2, base + 3.6, 0], [-0.4, base + 3.6, 0], color=GREY, stroke_width=2.5)
        cl = VGroup(T("control", 24, TEXT), M("1.00", 24, TEXT)).arrange(DOWN, buff=0.08).move_to([cx, -2.75, 0])
        self.play(FadeIn(title), Create(axis), run_time=0.6)
        self.play(GrowFromEdge(ctrl, DOWN), Create(ref), FadeIn(cl), run_time=0.9)
        mut = Rectangle(width=bw, height=3.06, stroke_width=0, fill_color=BLUE, fill_opacity=0.85).move_to([mx, base + 1.53, 0])
        ml = VGroup(T("PelB deleted", 24, RED), M("0.85", 24, TEXT)).arrange(DOWN, buff=0.08).move_to([mx, -2.75, 0])
        self.at("left about")
        self.play(GrowFromEdge(mut, DOWN), FadeIn(ml), run_time=0.9)
        bones = T("several hind-limb\nbones shorter", 28, TEXT).move_to([3.5, 1.2, 0])
        self.at("Several bones")
        self.play(FadeIn(bones, shift=LEFT * 0.2), run_time=0.7)
        tune = T("supplies part of the\nlimb's Pitx1; other\nenhancers the rest;\nnot an on-off switch", 28, BLUE).move_to([3.5, -1.0, 0])
        self.at("supplies part")
        self.play(FadeIn(tune, shift=LEFT * 0.2), run_time=0.8)

        # ladder
        chart = VGroup(title, axis, ctrl, ref, cl, mut, ml, bones, tune)
        rows = [("Mapping", "which chromosome region"),
                ("In situ hybridization", "where the transcript is"),
                ("F1 hybrid test", "whether there is a cis difference"),
                ("Reporter", "what a sequence can drive"),
                ("Native deletion", "whether form depends on it")]
        ys = [2.5, 1.25, 0.0, -1.25, -2.5]
        chips, arrs, txts = [], [], []
        for (nm, ans), y in zip(rows, ys):
            c = chip(nm, TEXT, 28).move_to([-3.6, y, 0])
            c.shift(RIGHT * 0)  # width differs per name; right-align below
            chips.append(c)
        right = max(c.get_right()[0] for c in chips)
        for c, (nm, ans), y in zip(chips, rows, ys):
            c.shift(RIGHT * (right - c.get_right()[0]))
            ar = arr([right + 0.1, y, 0], [right + 0.8, y, 0], TEXT, w=4, tip=0.18)
            tx = T(ans, 28, TEXT)
            tx.move_to([right + 1.0 + tx.width / 2, y, 0])
            arrs.append(ar); txts.append(tx)
        for c in chips:
            pass
        # shift all rows so the whole ladder is centered in the frame
        total = VGroup(*chips, *arrs, *txts)
        dx = -total.get_center()[0]
        for m in (*chips, *arrs, *txts):
            m.shift(RIGHT * dx)

        def rung(i):
            return [FadeIn(chips[i], shift=RIGHT * 0.2), GrowArrow(arrs[i]), FadeIn(txts[i], shift=RIGHT * 0.2)]
        self.at("Mapping")
        self.play(FadeOut(chart), run_time=0.6)
        self.play(*rung(0), run_time=0.6)
        self.at("hybridization")
        self.play(*rung(1), run_time=0.6)
        self.at("hybrid test")
        self.play(*rung(2), run_time=0.6)
        self.at("A reporter")
        self.play(*rung(3), run_time=0.6)
        self.at("native deletion")
        self.play(*rung(4), run_time=0.6)
        self.at("Each method")
        self.play(*[Indicate(c, color=TEXT, scale_factor=1.08) for c in chips], run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "Each method answers its own question."
