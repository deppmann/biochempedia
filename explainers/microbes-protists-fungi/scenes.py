"""Microbes, protists and fungi: look alike, yet far apart  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = typical bacteria (E. coli)
  ORANGE = methanogens / archaea
  GREEN  = eukaryotes (yeast)
  TEAL   = ribosomal RNA and its short pieces
  PURPLE = the enzyme, ribonuclease T1
  YELLOW = the shared pieces, the score, the open question
  RED    = the expectation that failed
  GREY   = outlines, labels, absences, cautions
  GOLD   = title rule only
Everything here is a schematic: cells are plain outlines, pieces and scores are drawn for
illustration (not data), the map is a sketch. No molecule is drawn.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
TEAL_ = TEAL


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def rod(color, w=4.4, h=2.4):
    return RoundedRectangle(corner_radius=h / 2.2, width=w, height=h, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.2)


def dashed_ellipse(w, h, color, n=28):
    return DashedVMobject(Ellipse(width=w, height=h, stroke_color=color, stroke_width=3), num_dashes=n)


def blob(color, label, w=3.2, h=1.7, size=26):
    e = Ellipse(width=w, height=h, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.22)
    t = T(label, size, color)
    g = VGroup(e, t.move_to(e))
    g.e, g.t = e, t
    return g


class S00Title(TitleCard):
    LESSON = "Microbes, protists and fungi"
    TITLE = "Look alike, yet far apart"


# ---------------------------------------------------------------------------------------------
class S01Lookalike(SpokenScene):
    def construct(self):
        meth = rod(ORANGE, 5.2, 3.0).move_to([-3.5, 1.3, 0])
        eco = rod(BLUE, 5.2, 3.0).move_to([3.5, 1.3, 0])
        m_name = T("methanogen", 34, ORANGE).move_to([-3.5, -0.5, 0])
        m_sub = T("a methane-producing microbe", 26, GREY).move_to([-3.5, -1.05, 0])
        e_name = T("Escherichia coli", 34, BLUE).move_to([3.5, -0.5, 0])
        e_sub = T("a bacterium", 26, GREY).move_to([3.5, -1.05, 0])
        self.at("microbe")
        self.play(GrowFromCenter(meth), FadeIn(m_name), FadeIn(m_sub), run_time=0.9)
        self.at("bacterium")
        self.play(GrowFromCenter(eco), FadeIn(e_name), FadeIn(e_sub), run_time=0.9)
        self.at("alike")
        same = T("≈", 80, TEXT).move_to([0, 1.3, 0])
        self.play(FadeIn(same, scale=0.8), run_time=0.5)
        self.at("neither")
        n1 = chip("no nucleus", GREY, 26).move_to([-3.5, -2.0, 0])
        n2 = chip("no nucleus", GREY, 26).move_to([3.5, -2.0, 0])
        self.play(FadeIn(n1, shift=UP * 0.15), FadeIn(n2, shift=UP * 0.15), run_time=0.6)
        self.at("cattle")
        g = T("live in the guts of cattle and humans", 24, GREY).move_to([-3.5, -3.05, 0])
        self.play(FadeIn(g), run_time=0.5)
        self.at("relatives")
        q = T("?", 100, YELLOW, weight=BOLD).move_to([0, 1.3, 0])
        ql = T("close relatives?", 28, YELLOW).move_to([0, -0.5, 0])
        self.play(ReplacementTransform(same, q), FadeIn(ql), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Absence(SpokenScene):
    def construct(self):
        # --- A: the lump -------------------------------------------------------------------
        meth = rod(ORANGE, 4.4, 2.6).move_to([-3.5, 0.7, 0])
        eco = rod(BLUE, 4.4, 2.6).move_to([3.5, 0.7, 0])
        mn = T("methanogen", 28, ORANGE).move_to([-3.5, -0.95, 0])
        en = T("E. coli", 28, BLUE).move_to([3.5, -0.95, 0])
        self.add(meth, eco, mn, en)
        self.at("lump")
        brace = Brace(VGroup(meth, eco), UP, color=GREY, buff=0.2)
        lump = chip("prokaryotes", GREY, 30).next_to(brace, UP, buff=0.15)
        self.play(GrowFromCenter(brace), run_time=0.6)
        self.play(FadeIn(lump), run_time=0.4)
        self.at("absence")
        d1 = dashed_ellipse(1.5, 1.2, GREY).move_to(meth)
        d2 = dashed_ellipse(1.5, 1.2, GREY).move_to(eco)
        ab = T("nucleus: absent", 30, GREY).move_to([0, -2.2, 0])
        self.play(Create(d1), Create(d2), FadeIn(ab), run_time=0.8)
        self.at("need not")
        q = T("?", 96, YELLOW, weight=BOLD).move_to([0, 0.7, 0])
        self.play(brace.animate.set_opacity(0.3), lump.animate.set_opacity(0.35), FadeIn(q, scale=0.8), run_time=0.6)

        # --- B: something every cell has ------------------------------------------------
        self.at("ribosomes")
        yeast = rod(GREEN, 3.8, 2.4)
        meth2 = rod(ORANGE, 3.8, 2.4)
        eco2 = rod(BLUE, 3.8, 2.4)
        cells = VGroup(eco2, meth2, yeast).arrange(RIGHT, buff=0.4).move_to([0, 1.0, 0])
        nuc = Circle(radius=0.5, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to(yeast.get_center() + RIGHT * 0.9)
        names = VGroup(T("typical bacteria", 26, BLUE).next_to(eco2, DOWN, buff=0.2),
                       T("methanogen", 26, ORANGE).next_to(meth2, DOWN, buff=0.2),
                       T("yeast", 26, GREEN).next_to(yeast, DOWN, buff=0.2))
        nuclab = T("nucleus", 24, GREEN).move_to(yeast.get_top() + UP * 0.3 + RIGHT * 0.9)
        rib = VGroup(*[Circle(radius=0.45, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).move_to(c.get_center() + LEFT * 0.8)
                       for c in (eco2, meth2, yeast)])
        old = VGroup(meth, eco, mn, en, brace, lump, d1, d2, ab, q)
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(cells), FadeIn(names), FadeIn(nuc), FadeIn(nuclab), run_time=0.6)
        self.play(FadeIn(rib, scale=0.6), run_time=0.5)
        rl = T("ribosomes", 28, GREY).move_to([0, -1.75, 0])
        self.add(rl)
        self.at("particles")
        self.play(Indicate(rib, color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.at("looked")
        want = chip("a part every cell carries", YELLOW, 32).move_to([0, -1.75, 0])
        self.play(ReplacementTransform(rl, want), run_time=0.6)
        self.at("subunit")
        bars = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.56, height=0.16, stroke_width=0, fill_color=TEAL, fill_opacity=1).move_to(r)
                        for r in rib])
        rna = chip("small-subunit RNA", TEAL, 32).move_to([0, -1.75, 0])
        self.play(ReplacementTransform(want, rna), FadeIn(bars, scale=0.4), run_time=0.7)
        self.at("present in all cells")
        self.play(Indicate(bars, color=TEAL, scale_factor=1.4), run_time=0.8)
        self.at("same job")
        job = T("the same job in each", 36, TEXT).move_to([0, -2.85, 0])
        self.play(FadeIn(job, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Catalogue(SpokenScene):
    def construct(self):
        self.at("laboratory")
        lab = chip("Woese's laboratory and its collaborators", GREY, 30).move_to([0, 2.3, 0])
        self.play(FadeIn(lab, shift=DOWN * 0.15), run_time=0.6)
        self.at("grew")
        arrow_l = arr([-1.2, 1.7, 0], [-3.0, 0.9, 0], GREY)
        arrow_r = arr([1.2, 1.7, 0], [3.0, 0.9, 0], GREY)
        tb = chip("typical bacteria", BLUE, 30).move_to([-3.4, 0.5, 0])
        mg = chip("methanogens", ORANGE, 30).move_to([3.4, 0.5, 0])
        plus = T("grew", 26, GREY).move_to([0, 0.5, 0])
        self.play(FadeIn(plus), run_time=0.4)
        self.at("typical")
        self.play(GrowArrow(arrow_l), FadeIn(tb, shift=DOWN * 0.15), run_time=0.6)
        self.at("called")
        self.play(GrowArrow(arrow_r), FadeIn(mg, shift=DOWN * 0.15), run_time=0.6)
        self.at("extracted")
        widths = [1.9, 1.1, 2.0, 1.4, 1.2, 1.7, 1.2]
        scale = 11.0 / sum(widths)
        widths = [w * scale for w in widths]
        segs, x = [], -5.5
        for w in widths:
            segs.append(Rectangle(width=w, height=0.7, stroke_color=BG, stroke_width=2, fill_color=TEAL, fill_opacity=0.85)
                        .move_to([x + w / 2, 1.9, 0]))
            x += w
        bar = VGroup(*segs)
        bl = T("ribosomal RNA of one microbe", 28, TEAL).move_to([0, 2.8, 0])
        self.play(FadeOut(VGroup(tb, plus, mg, lab, arrow_l, arrow_r)), run_time=0.3)
        self.play(GrowFromCenter(bar), FadeIn(bl), run_time=0.8)
        self.at("cut")
        cuts = VGroup(*[Line([s.get_right()[0], 1.35, 0], [s.get_right()[0], 2.45, 0], color=PURPLE, stroke_width=5)
                        for s in segs[:-1]])
        self.play(bl.animate.set_opacity(0.0), Create(cuts), run_time=0.6)
        self.at("short pieces")
        self.play(*[s.animate.shift(UP * (0.3 if i % 2 else -0.1)) for i, s in enumerate(segs)],
                  FadeOut(cuts), run_time=0.6)
        self.at("enzyme")
        enz = chip("ribonuclease T1", PURPLE, 32).move_to([0, 3.0, 0])
        self.play(FadeIn(enz, shift=DOWN * 0.15), run_time=0.5)
        box = RoundedRectangle(corner_radius=0.2, width=12.0, height=2.4, stroke_color=GREY, stroke_width=3).move_to([0, -1.3, 0])
        cl = T("catalogue of pieces", 28, GREY).move_to([0, 0.15, 0])
        self.at("cataloged")
        self.play(Create(box), FadeIn(cl), FadeOut(enz), run_time=0.5)
        k = 0.85
        tw = sum(w * k for w in widths) + 0.3 * (len(segs) - 1)
        x = -tw / 2
        moves = []
        for s, w in zip(segs, widths):
            moves.append(s.animate.scale(k).move_to([x + w * k / 2, -1.5, 0]))
            x += w * k + 0.3
        self.play(LaggedStart(*moves, lag_ratio=0.1), run_time=1.2)
        self.at("each piece")
        self.play(LaggedStart(*[Indicate(s, color=YELLOW, scale_factor=1.2) for s in segs], lag_ratio=0.25), run_time=1.8)
        note = T("pieces drawn for illustration, not to scale", 24, GREY).move_to([0, -3.3, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Score(SpokenScene):
    def construct(self):
        rows = [2.2 - 0.55 * i for i in range(6)]
        lens = [1.5, 0.8, 1.9, 1.1, 1.6, 0.9]
        # left column piece i  -> right column piece j (monotone, no crossing)
        shared = [(0, 1), (2, 2), (3, 4), (5, 5)]
        lx, rx = -3.9, 3.9

        def column(x, color, names_order):
            box = RoundedRectangle(corner_radius=0.2, width=3.4, height=3.7, stroke_color=color, stroke_width=3).move_to([x, 0.7, 0])
            ps = VGroup(*[Rectangle(width=lens[k], height=0.34, stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to([x, rows[i], 0])
                          for i, k in enumerate(names_order)])
            return box, ps

        lorder = [0, 1, 2, 3, 4, 5]
        # right column: shared pieces carry the same lengths as their left partners
        rorder = [None] * 6
        left_k = {i: lorder[i] for i in range(6)}
        rem = [k for k in range(6) if k not in [left_k[a] for a, b in shared]]
        for a, b in shared:
            rorder[b] = left_k[a]
        rem_iter = iter(rem)
        for j in range(6):
            if rorder[j] is None:
                rorder[j] = next(rem_iter)
        lbox, lps = column(lx, GREY, lorder)
        rbox, rps = column(rx, GREY, rorder)
        ll = T("organism 1", 28, GREY).move_to([lx, 3.1, 0])
        rl = T("organism 2", 28, GREY).move_to([rx, 3.1, 0])
        # meter
        mx0, mw, my = -4.0, 8.0, -2.55
        mframe = RoundedRectangle(corner_radius=0.1, width=mw, height=0.5, stroke_color=GREY, stroke_width=3).move_to([0, my, 0])
        mlab = T("similarity score (relative, in this sketch)", 26, TEXT).move_to([0, my + 0.6, 0])

        def fill(frac, color):
            f = max(frac, 0.001)
            return Rectangle(width=mw * f, height=0.5, stroke_width=0, fill_color=color, fill_opacity=0.9) \
                .move_to([mx0 + mw * f / 2, my, 0])

        mfill = fill(0.0, YELLOW)
        self.at("similarity score")
        self.play(FadeIn(VGroup(lbox, lps, ll)), FadeIn(VGroup(rbox, rps, rl)), run_time=0.7)
        self.play(FadeIn(mframe), FadeIn(mlab), FadeIn(mfill), run_time=0.4)
        self.at("shared more pieces")
        links = VGroup(*[Line(lps[a].get_right(), rps[b].get_left(), color=YELLOW, stroke_width=3) for a, b in shared])
        sh_l = [lps[a] for a, b in shared]
        sh_r = [rps[b] for a, b in shared]
        self.play(Create(links), *[p.animate.set_fill(YELLOW) for p in sh_l + sh_r], run_time=0.8)
        self.play(Transform(mfill, fill(0.7, YELLOW)), run_time=0.8)
        # --- reset to the methanogen / bacterium case ----------------------------------
        self.at("old split")
        ll2 = T("methanogen", 28, ORANGE).move_to(ll)
        rl2 = T("typical bacterium", 28, BLUE).move_to(rl)
        self.play(FadeOut(links), *[p.animate.set_fill(TEAL) for p in sh_l + sh_r],
                  Transform(mfill, fill(0.0, YELLOW)),
                  ReplacementTransform(ll, ll2), ReplacementTransform(rl, rl2),
                  lbox.animate.set_stroke(ORANGE), rbox.animate.set_stroke(BLUE), run_time=0.7)
        self.at("closest")
        exp = DashedLine([mx0 + mw * 0.8, my - 0.45, 0], [mx0 + mw * 0.8, my + 0.45, 0], color=GREEN, stroke_width=5)
        expl = T("expected", 24, GREEN).move_to([mx0 + mw * 0.8, my - 0.78, 0])
        self.play(Create(exp), FadeIn(expl), run_time=0.6)
        self.at("did not")
        one = Line(lps[0].get_right(), rps[1].get_left(), color=YELLOW, stroke_width=3)
        self.play(Create(one), lps[0].animate.set_fill(YELLOW), rps[1].animate.set_fill(YELLOW),
                  Transform(mfill, fill(0.15, RED)), run_time=0.8)
        note = T("pieces drawn for illustration, not data", 22, GREY).move_to([-3.6, -3.35, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
BAC_P = np.array([-4.5, -1.6, 0])
EUK_P = np.array([4.5, -1.6, 0])
GHOST_P = np.array([-0.7, -1.6, 0])
ARC_P = np.array([0.0, 1.4, 0])


class S05Three(SpokenScene):
    def construct(self):
        bac = blob(BLUE, "typical\nbacteria", 3.4, 2.0, 28).move_to(BAC_P)
        euk = blob(GREEN, "eukaryotes", 3.4, 2.0, 28).move_to(EUK_P)
        ghost = dashed_ellipse(3.4, 2.0, ORANGE).move_to(GHOST_P)
        ghost_l = T("expected: next to bacteria", 24, GREY).move_to(GHOST_P + UP * 1.4)
        legend = T("similarity map, in this sketch: farther apart = less alike RNA", 24, GREY).move_to([0, -3.3, 0])
        year = T("1977", 34, GREY).move_to([-5.4, 3.1, 0])
        self.add(bac, euk, ghost, ghost_l, legend)
        self.at("reported")
        self.play(FadeIn(year), run_time=0.4)
        meth = blob(ORANGE, "methanogens", 3.4, 2.0, 28).move_to(GHOST_P)
        self.at("methanogens")
        self.play(FadeIn(meth, scale=0.8), run_time=0.5)
        self.at("their own group")
        self.play(meth.animate.move_to(ARC_P), ghost.animate.set_opacity(0.0), FadeOut(ghost_l), run_time=1.2)
        self.at("about as distant")
        l1 = DashedLine(meth.e.get_bottom() + LEFT * 0.9, bac.e.get_top() + RIGHT * 0.3, color=TEXT, stroke_width=4)
        t1 = T("typical bacteria", 28, BLUE).move_to([-4.3, 0.8, 0])
        self.play(Create(l1), FadeIn(t1), run_time=0.7)
        self.at("eukaryotes")
        l2 = DashedLine(meth.e.get_bottom() + RIGHT * 0.9, euk.e.get_top() + LEFT * 0.3, color=TEXT, stroke_width=4)
        t2 = T("cytoplasmic ribosomal RNA\nof eukaryotes", 24, GREEN, line_spacing=0.8).move_to([3.6, 0.8, 0])
        self.play(Create(l2), FadeIn(t2), run_time=0.7)
        self.at("kingdom")
        k = chip("a third primary kingdom: archaebacteria", ORANGE, 28).move_to([0, 3.0, 0])
        self.play(FadeIn(k, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        bp, ep, ap = np.array([-4.2, 0.0, 0]), np.array([4.2, 0.0, 0]), np.array([0.0, 2.1, 0])
        bac = blob(BLUE, "typical\nbacteria", 3.8, 2.0, 28).move_to(bp)
        euk = blob(GREEN, "eukaryotes", 3.8, 2.0, 28).move_to(ep)
        arc = blob(ORANGE, "methanogens", 3.8, 2.0, 28).move_to(ap)
        year = T("1990", 34, GREY).move_to([-5.4, 3.1, 0])
        self.add(bac, euk, arc, year)
        self.at("three domains")
        dl = T("three domains", 32, TEXT).move_to([0, -0.3, 0])
        self.play(bac.e.animate.set_stroke(width=7), arc.e.animate.set_stroke(width=7), euk.e.animate.set_stroke(width=7),
                  FadeIn(dl), run_time=0.8)
        self.at("they are")
        b2 = T("Bacteria", 34, BLUE, weight=BOLD).move_to(bac.e)
        a2 = T("Archaea", 34, ORANGE, weight=BOLD).move_to(arc.e)
        e2 = T("Eukarya", 34, GREEN, weight=BOLD).move_to(euk.e)
        self.play(ReplacementTransform(bac.t, b2), run_time=0.5)
        self.at("archaea")
        self.play(ReplacementTransform(arc.t, a2), run_time=0.5)
        self.at("eukarya")
        self.play(ReplacementTransform(euk.t, e2), run_time=0.5)
        self.at("more than")
        c1 = chip("ether-linked lipids", ORANGE, 28).move_to([4.3, 2.9, 0])
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.5)
        self.at("walls")
        c2 = chip("no peptidoglycan", ORANGE, 28).move_to([4.3, 1.9, 0])
        self.play(FadeIn(c2, shift=LEFT * 0.2), run_time=0.5)
        self.at("extreme")
        c3 = chip("not simply\nextreme bacteria", ORANGE, 28).move_to([-4.2, 2.0, 0])
        self.play(FadeIn(c3, shift=RIGHT * 0.2), run_time=0.5)
        self.at("ancestor")
        n1 = chip("no ancestor observed", GREY, 28)
        n2 = chip("how eukaryotic cells arose: not shown", GREY, 28)
        ns = VGroup(n1, n2).arrange(RIGHT, buff=0.4).move_to([0, -2.4, 0])
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3), FadeOut(dl), FadeIn(n1, shift=UP * 0.15), run_time=0.5)
        self.at("arose")
        self.play(FadeIn(n2, shift=UP * 0.15), run_time=0.5)
        self.at("appearance")
        r1 = T("appearance does not reveal deep relationships", 34, GREY).move_to([0, -2.1, 0])
        r2 = T("a shared molecule can", 44, TEAL, weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeOut(ns), FadeIn(r1, shift=UP * 0.15), run_time=0.5)
        self.at("shared molecule")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Appearance does not reveal deep relationships. A shared molecule can."
