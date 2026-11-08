"""Linkage and recombination mapping: distance is how often crossovers separate two loci.

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the chromosome that carries the dominant alleles A and B (and, in the last scene, A with b)
  YELLOW = the chromosome that carries the recessive alleles a and b (and, in the last scene, a with B)
  GREEN  = parental classes / offspring that look like a grandparent
  RED    = recombinant classes, and crossovers that fall between two loci
  TEAL   = map distance: centimorgans, the Haldane curve, the linked chip
  GOLD   = the 50% ceiling
  GREY   = outlines, axes, de-emphasised things
  TEXT   = loci, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
DOM, REC = BLUE, YELLOW


def allele_text(letters, colors, size=30, buff=0.14):
    """e.g. allele_text("Ab", [BLUE, YELLOW]) -> the letters 'A b', each coloured by the chromosome it came from."""
    g = VGroup(*[T(ch, size, c, weight=BOLD) for ch, c in zip(letters, colors)])
    return g.arrange(RIGHT, buff=buff)


def seg(x0, x1, y, h, color, label=None, fz=26):
    r = Rectangle(width=x1 - x0, height=h, stroke_color=BG, stroke_width=2, fill_color=color, fill_opacity=0.92)
    r.move_to([(x0 + x1) / 2, y, 0])
    g = VGroup(r)
    if label:
        g.add(T(label, fz, BG, weight=BOLD).move_to(r))
    return g


def chromatid(xl, y, w, cols, alleles, h=0.5, fz=26):
    """A chromatid as three pieces (L, M, R). Allele A/a sits in L, B/b in R.
    cols = colours of (L, M, R). A crossover swaps pieces between two chromatids."""
    a, b = alleles
    L = seg(xl, xl + 0.3 * w, y, h, cols[0], a, fz)
    M = seg(xl + 0.3 * w, xl + 0.7 * w, y, h, cols[1])
    R = seg(xl + 0.7 * w, xl + w, y, h, cols[2], b, fz)
    g = VGroup(L, M, R)
    g.L, g.M, g.R = L, M, R
    return g


def mini_gamete(x, y, letters, colors, w=1.8, h=0.46):
    a, b = letters
    return chromatid(x - w / 2, y, w, (colors[0], colors[0], colors[1]), (a, b), h=h, fz=24)


def bracket(x0, x1, y, color, up=True, tick=0.14):
    d = tick if up else -tick
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                  Line([x0, y, 0], [x0, y + d, 0], color=color, stroke_width=4),
                  Line([x1, y, 0], [x1, y + d, 0], color=color, stroke_width=4))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def haldane(cm):
    return 50 * (1 - np.exp(-2 * cm / 100))   # percent recombinant for a distance in cM


class S00Title(TitleCard):
    LESSON = "Linkage and recombination mapping"
    TITLE = "Distance is how often crossovers separate"


# ---------------------------------------------------------------------------------------------
class S01Flies(SpokenScene):
    """1,000 test-cross offspring: Mendel predicts 500, you count 830; the alleles are held together on one chromosome."""

    def construct(self):
        # --- the cross --------------------------------------------------------------
        fa = chip("fly with two mutations", GREY, 28).move_to([-3.6, 0.3, 0])
        fb = chip("fly with only recessive alleles", GREY, 28).move_to([3.4, 0.3, 0])
        x = T("×", 48, TEXT).move_to([0, 0.3, 0])
        self.play(FadeIn(fa, shift=RIGHT * 0.2), run_time=0.8)
        self.at("to a fly")
        self.play(FadeIn(fb, shift=LEFT * 0.2), FadeIn(x), run_time=0.8)

        # --- 1,000 offspring --------------------------------------------------------
        cols, rows, sp = 40, 25, 0.185
        dots = VGroup(*[Dot(radius=0.055, color=GREY).set_opacity(0.75) for _ in range(cols * rows)])
        for i, d in enumerate(dots):
            r, c = divmod(i, cols)
            d.move_to([-6.0 + c * sp + sp / 2 - 0.0, 1.9 - r * sp, 0])
        grid_c = np.array([-6.0 + cols * sp / 2, 1.9 - rows * sp / 2 + sp / 2, 0])
        lab_n = T("1,000 offspring", 30, TEXT).move_to([3.7, 2.4, 0])
        self.at("Mendel's law")
        self.play(FadeOut(VGroup(fa, fb, x)), FadeIn(dots, lag_ratio=0.001), FadeIn(lab_n), run_time=1.6)

        leg = VGroup(Dot(radius=0.1, color=GREEN), T("look like a grandparent", 26, GREEN)).arrange(RIGHT, buff=0.2)
        leg.move_to([3.7, 1.55, 0])
        pred_t = T("Mendel predicts", 28, GREY).move_to([3.7, 0.5, 0])
        pred_n = M("500", 64, GREEN, weight=BOLD).move_to([3.7, -0.2, 0])
        self.at("predicts")
        self.play(FadeIn(leg), FadeIn(pred_t), run_time=0.5)
        self.play(LaggedStart(*[d.animate.set_color(GREEN).set_opacity(0.4) for d in dots[:500]], lag_ratio=0.003),
                  FadeIn(pred_n), run_time=1.8)

        cnt_t = T("You count", 28, GREY).move_to([3.7, -1.3, 0])
        cnt_n = M("830", 64, GREEN, weight=BOLD).move_to([3.7, -2.0, 0])
        self.at("You count")
        self.play(FadeIn(cnt_t), run_time=0.4)
        self.play(LaggedStart(*[d.animate.set_color(GREEN).set_opacity(1.0) for d in dots[:830]], lag_ratio=0.002),
                  FadeIn(cnt_n), run_time=1.5)

        # --- something holds them together ----------------------------------------------
        self.at("Something is holding")
        self.play(Indicate(cnt_n, color=GREEN, scale_factor=1.12), run_time=0.9)

        bar = RoundedRectangle(corner_radius=0.18, width=9.0, height=0.55, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.3).move_to([0, 0.0, 0])
        la = T("A", 36, TEXT, weight=BOLD)
        lb = T("B", 36, TEXT, weight=BOLD)
        ba = Rectangle(width=0.18, height=0.55, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to([-0.7, 0, 0])
        bb = Rectangle(width=0.18, height=0.55, stroke_width=0, fill_color=TEXT, fill_opacity=0.95).move_to([0.7, 0, 0])
        la.next_to(ba, UP, buff=0.2)
        lb.next_to(bb, UP, buff=0.2)
        chrom = VGroup(bar, ba, bb, la, lb)
        chr_lbl = T("one chromosome", 28, GREY).next_to(bar, DOWN, buff=0.35)
        self.at("Genes that lie near")
        self.play(FadeOut(VGroup(dots, leg, pred_t, pred_n, cnt_t, cnt_n, lab_n)), run_time=0.6)
        self.play(FadeIn(bar), FadeIn(ba), FadeIn(bb), FadeIn(la), FadeIn(lb), FadeIn(chr_lbl), run_time=0.8)
        link = chip("linked", TEAL, 40).move_to([0, 1.9, 0])
        link_line = bracket(-0.7, 0.7, -0.75, TEAL, up=True, tick=0.16)
        link_line.shift(UP * 0.0)
        self.at("called linked")
        self.play(FadeIn(link, shift=DOWN * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Testcross(SpokenScene):
    """female with A B / a b, tester a b / a b; each offspring reads out her gamete."""

    def construct(self):
        fem_lbl = T("heterozygous female", 28, GREY).move_to([-3.4, 3.05, 0])
        f1 = chromatid(-6.1, 2.25, 5.4, (DOM, DOM, DOM), ("A", "B"))
        f2 = chromatid(-6.1, 1.4, 5.4, (REC, REC, REC), ("a", "b"))
        tst_lbl = T("tester", 28, GREY).move_to([-3.4, 0.2, 0])
        t1 = chromatid(-6.1, -0.55, 5.4, (REC, REC, REC), ("a", "b"))
        t2 = chromatid(-6.1, -1.4, 5.4, (REC, REC, REC), ("a", "b"))

        F = VGroup(fem_lbl, f1, f2)
        F.save_state()
        F.scale(1.45).move_to([0, 0.5, 0])
        fem_lbl.set_opacity(0)
        self.add(fem_lbl)
        self.at("Take two loci")
        self.play(FadeIn(VGroup(f1, f2)), run_time=0.9)
        self.at("each a gene's")
        self.play(Indicate(f1.L, color=TEXT, scale_factor=1.15), Indicate(f1.R, color=TEXT, scale_factor=1.15), run_time=0.9)
        self.at("female")
        self.play(fem_lbl.animate.set_opacity(1), run_time=0.6)
        self.at("dominant")
        self.play(Indicate(f1, color=DOM, scale_factor=1.05), run_time=0.8)
        self.at("recessive")
        self.play(Indicate(f2, color=REC, scale_factor=1.05), run_time=0.8)

        self.at("The tester")
        self.play(Restore(F), FadeIn(tst_lbl), FadeIn(t1), FadeIn(t2), run_time=0.7)

        # --- the gametes meet -----------------------------------------------------------
        g_her = mini_gamete(2.4, 0.95, ("A", "b"), (DOM, REC))
        g_tst = mini_gamete(2.4, -1.05, ("a", "b"), (REC, REC))
        l_her = T("her gamete", 26, GREY).next_to(g_her, UP, buff=0.2)
        l_tst = T("tester gamete", 26, GREY).next_to(g_tst, DOWN, buff=0.2)
        a1 = arr([-0.5, 1.8, 0], [1.3, 1.0, 0], GREY)
        a2 = arr([-0.5, -0.95, 0], [1.3, -1.05, 0], GREY)
        self.at("gives only")
        self.play(GrowArrow(a2), FadeIn(g_tst), FadeIn(l_tst), run_time=0.8)
        off = mini_gamete(5.4, -0.05, ("A", "b"), (DOM, REC))
        off_lbl = T("offspring", 26, TEXT).next_to(off, DOWN, buff=0.2)
        a3 = arr([3.4, 0.9, 0], [4.35, 0.15, 0], GREY)
        a4 = arr([3.4, -1.0, 0], [4.35, -0.25, 0], GREY)
        self.at("So each offspring")
        self.play(GrowArrow(a1), FadeIn(g_her), FadeIn(l_her), run_time=0.7)
        self.play(GrowArrow(a3), GrowArrow(a4), FadeIn(off), FadeIn(off_lbl), run_time=0.8)
        self.at("which alleles came")
        self.play(Indicate(off, color=TEXT, scale_factor=1.12), Indicate(g_her, color=TEXT, scale_factor=1.12), run_time=0.9)
        fin = T("count offspring = count her gametes", 32, TEXT).move_to([0.6, -3.05, 0])
        self.at("counting offspring")
        self.play(FadeIn(fin, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Crossover(SpokenScene):
    """four chromatids; a crossover swaps two; two parental, two recombinant; near loci are rarely split, far loci often."""

    def construct(self):
        W, XL = 7.4, -5.6
        ys = [2.5, 1.55, 0.6, -0.35]
        b1 = chromatid(XL, 2.2, W, (DOM, DOM, DOM), ("A", "B"))
        c1 = chromatid(XL, -0.9, W, (REC, REC, REC), ("a", "b"))
        self.play(FadeIn(b1), FadeIn(c1), run_time=0.8)

        # --- copy -> sister chromatids, then pair ------------------------------------------
        b2 = b1.copy()
        c2 = c1.copy()
        self.at("copied itself")
        self.add(b2, c2)
        self.play(b1.animate.move_to([b1.get_center()[0], ys[0], 0]),
                  b2.animate.move_to([b1.get_center()[0], ys[1], 0]),
                  c1.animate.move_to([c1.get_center()[0], ys[2] - 0.9, 0]),
                  c2.animate.move_to([c1.get_center()[0], ys[3] - 0.9, 0]), run_time=1.1)
        # re-bind rows by name: b1 top, b2 sister, c1, c2
        sis_lbl = T("sister chromatids", 26, GREY).move_to([4.5, 2.0, 0])
        sis_br = VGroup(Line([2.0, ys[0] + 0.25, 0], [2.3, ys[0] + 0.25, 0], color=GREY, stroke_width=4),
                        Line([2.3, ys[0] + 0.25, 0], [2.3, ys[1] - 0.25, 0], color=GREY, stroke_width=4),
                        Line([2.0, ys[1] - 0.25, 0], [2.3, ys[1] - 0.25, 0], color=GREY, stroke_width=4))
        self.at("sister chromatids")
        self.play(FadeIn(sis_br), FadeIn(sis_lbl), run_time=0.6)
        self.at("partners pair")
        self.play(FadeOut(sis_br), FadeOut(sis_lbl),
                  c1.animate.move_to([c1.get_center()[0], ys[2], 0]),
                  c2.animate.move_to([c1.get_center()[0], ys[3], 0]), run_time=0.9)

        # --- the crossover -----------------------------------------------------------------
        xc = XL + 0.3 * W
        mark = DashedLine([xc, ys[1] + 0.3, 0], [xc, ys[2] - 0.3, 0], color=TEXT, stroke_width=4)
        xmark = Cross(Square(0.3), stroke_color=TEXT, stroke_width=5).move_to([xc, (ys[1] + ys[2]) / 2, 0])
        self.at("one crossover")
        self.play(Indicate(VGroup(b2, c1), color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("falls between")
        self.play(Create(mark), FadeIn(xmark, scale=0.5), run_time=0.6)
        # b2 is row 2 (blue sister), c1 is row 3 (yellow). swap their M and R pieces.
        dy = ys[2] - ys[1]
        self.at("swaps matching")
        self.play(b2.M.animate.shift(DOWN * abs(dy)), b2.R.animate.shift(DOWN * abs(dy)),
                  c1.M.animate.shift(UP * abs(dy)), c1.R.animate.shift(UP * abs(dy)), run_time=1.3)
        self.play(FadeOut(mark), FadeOut(xmark), run_time=0.3)
        self.at("non sister")
        self.play(Indicate(VGroup(b2.L, c1.L), color=TEXT, scale_factor=1.04), run_time=0.8)

        # --- tags --------------------------------------------------------------------------
        t_par1 = chip("parental", GREEN, 24).move_to([4.9, ys[0], 0])
        t_rec1 = chip("recombinant", RED, 24).move_to([4.9, ys[1], 0])
        t_rec2 = chip("recombinant", RED, 24).move_to([4.9, ys[2], 0])
        t_par2 = chip("parental", GREEN, 24).move_to([4.9, ys[3], 0])
        self.at("Those two")
        self.play(Indicate(VGroup(b2, c1), color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("new combinations")
        self.play(Indicate(VGroup(b2.M, b2.R, c1.M, c1.R), color=TEXT, scale_factor=1.05), run_time=0.9)
        self.at("two recombinant")
        self.play(FadeIn(t_rec1), FadeIn(t_rec2), run_time=0.5)
        self.at("parental ones")
        self.play(FadeIn(t_par1), FadeIn(t_par2), Indicate(VGroup(b1, c2), color=TEXT, scale_factor=1.03), run_time=0.8)

        # --- near and far ------------------------------------------------------------------
        tags = VGroup(t_par1, t_par2, t_rec1, t_rec2)
        self.at("farther apart")
        self.play(FadeOut(VGroup(b1, b2, c1, c2, tags)), run_time=0.7)

        def row(y, xa, xb, label):
            bar = Rectangle(width=11.0, height=0.3, stroke_width=0, fill_color=GREY, fill_opacity=0.4).move_to([0, y, 0])
            ma = Rectangle(width=0.14, height=0.3, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([xa, y, 0])
            mb = Rectangle(width=0.14, height=0.3, stroke_width=0, fill_color=TEXT, fill_opacity=1).move_to([xb, y, 0])
            la = T("A", 30, TEXT, weight=BOLD).move_to([xa, y + 0.5, 0])
            lb = T("B", 30, TEXT, weight=BOLD).move_to([xb, y + 0.5, 0])
            gap = bracket(xa, xb, y - 0.35, TEAL, up=True, tick=0.14)
            lab = T(label, 26, TEAL).move_to([(xa + xb) / 2, y - 0.85, 0])
            return VGroup(bar, ma, mb, la, lb, gap, lab)

        near = row(1.5, -0.5, 0.5, "close together")
        far = row(-1.6, -3.6, 3.6, "far apart")
        self.play(FadeIn(near), FadeIn(far), run_time=0.8)
        pos = [-5.0, -3.0, 0.0, 2.0, 4.6]
        ticks = VGroup()
        for yy, xa, xb in ((1.5, -0.5, 0.5), (-1.6, -3.6, 3.6)):
            for p in pos:
                inside = xa < p < xb
                ticks.add(Line([p, yy - 0.35, 0], [p, yy + 0.35, 0], color=RED if inside else GREY, stroke_width=5 if inside else 3))
        self.at("more often")
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.1), run_time=1.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Count(SpokenScene):
    """420 / 410 parental, 85 / 85 recombinant -> 170 of 1,000 = 17% = 17 cM."""

    def construct(self):
        base = -1.5
        xs = [-5.1, -3.7, -2.3, -0.9]
        names = [("AB", (DOM, DOM)), ("ab", (REC, REC)), ("Ab", (DOM, REC)), ("aB", (REC, DOM))]
        counts = [420, 410, 85, 85]
        cols = [GREEN, GREEN, RED, RED]
        k = 3.3 / 420
        axis = Line([-6.0, base, 0], [0.0, base, 0], color=GREY, stroke_width=3)
        head = T("test-cross offspring", 28, GREY).move_to([-3.0, 3.2, 0])
        labels = VGroup(*[allele_text(n[0], n[1], 30).move_to([x, base - 0.45, 0]) for n, x in zip(names, xs)])
        self.at("In our cross")
        self.play(Create(axis), FadeIn(head), FadeIn(labels), run_time=0.9)

        bars, nums = [], []
        for x, n, c in zip(xs, counts, cols):
            b = Rectangle(width=1.0, height=n * k, stroke_width=0, fill_color=c, fill_opacity=0.9)
            b.move_to([x, base + n * k / 2, 0])
            bars.append(b)
            nums.append(M(str(n), 28, c).next_to(b, UP, buff=0.12))
        self.at("hold")
        self.play(GrowFromEdge(bars[0], DOWN), FadeIn(nums[0]), run_time=0.8)
        self.at("and")
        self.play(GrowFromEdge(bars[1], DOWN), FadeIn(nums[1]), run_time=0.8)

        br_p = bracket(xs[0] - 0.5, xs[1] + 0.5, base - 0.95, GREEN, up=True, tick=0.14)
        lb_p = T("parental", 26, GREEN).move_to([(xs[0] + xs[1]) / 2, base - 1.35, 0])
        n830 = M("830", 36, GREEN, weight=BOLD).move_to([-4.4, 2.65, 0])
        self.at("parental flies")
        self.play(FadeIn(br_p), FadeIn(lb_p), FadeIn(n830, shift=DOWN * 0.1), run_time=0.7)

        self.at("recombinant classes")
        for b, nn in zip(bars[2:], nums[2:]):
            self.play(GrowFromEdge(b, DOWN), FadeIn(nn), run_time=0.6)
        br_r = bracket(xs[2] - 0.5, xs[3] + 0.5, base - 0.95, RED, up=True, tick=0.14)
        lb_r = T("recombinant", 26, RED).move_to([(xs[2] + xs[3]) / 2, base - 1.35, 0])
        self.play(FadeIn(br_r), FadeIn(lb_r), run_time=0.5)
        self.at("each")
        self.play(Indicate(VGroup(*bars[2:], *nums[2:]), color=RED, scale_factor=1.1), run_time=0.9)

        f1 = M("170 / 1,000", 38, RED, weight=BOLD).move_to([3.6, 1.9, 0])
        self.at("flies are recombinant")
        self.play(FadeOut(n830), FadeIn(f1, shift=DOWN * 0.1), run_time=0.7)
        f2 = M("= 17%", 46, RED, weight=BOLD).move_to([3.6, 0.9, 0])
        self.at("which is")
        self.play(FadeIn(f2, shift=DOWN * 0.1), run_time=0.6)
        f3 = M("1% = 1 cM", 32, TEAL).move_to([3.6, -0.3, 0])
        self.at("offspring is")
        self.play(FadeIn(f3, shift=UP * 0.1), run_time=0.6)
        f4 = T("17 cM", 70, TEAL, weight=BOLD).move_to([3.6, -1.7, 0])
        self.at("so these loci")
        self.play(FadeIn(f4, scale=0.8), run_time=0.7)
        self.play(Indicate(f4, color=TEAL, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Ceiling(SpokenScene):
    """frequency cannot pass 50%; a second crossover puts the loci back; Haldane's curve corrects 17% to about 20.8 cM."""

    def construct(self):
        ox, oy = 0.5, -2.65
        sx, sy = 0.058, 0.088   # per cM, per percent

        def P(cm, pct):
            return np.array([ox + cm * sx, oy + pct * sy, 0])

        xaxis = Line(P(0, 0), P(100, 0), color=GREY, stroke_width=3)
        yaxis = Line(P(0, 0), P(0, 55), color=GREY, stroke_width=3)
        xt = VGroup(*[T(s, 22, GREY).move_to(P(v, 0) + DOWN * 0.3) for s, v in (("0", 0), ("50", 50), ("100", 100))])
        yt = VGroup(*[T(s, 22, GREY).move_to(P(0, v) + LEFT * 0.35) for s, v in (("0", 0), ("25", 25), ("50", 50))])
        xl = T("map distance (cM)", 24, GREY).move_to(P(50, 0) + DOWN * 0.75)
        yl = T("recombination frequency (%)", 24, GREY).rotate(PI / 2).move_to(P(0, 25) + LEFT * 0.95)
        axes = VGroup(xaxis, yaxis, xt, yt, xl, yl)
        self.at("Recombination frequency")
        self.play(Create(xaxis), Create(yaxis), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), run_time=1.2)

        ceil_l = DashedLine(P(0, 50), P(100, 50), color=GOLD, stroke_width=4)
        ceil_t = T("50% ceiling", 26, GOLD).move_to(P(70, 50) + UP * 0.4)
        self.at("never passes")
        self.play(Create(ceil_l), FadeIn(ceil_t), run_time=0.9)

        # --- four chromatids, one crossover -------------------------------------------------
        iw, ixl = 3.8, -6.3
        ys = [2.2, 1.5, 0.8, 0.1]
        r1 = chromatid(ixl, ys[0], iw, (DOM, DOM, DOM), ("A", "B"), h=0.46, fz=22)
        r2 = chromatid(ixl, ys[1], iw, (DOM, DOM, DOM), ("A", "B"), h=0.46, fz=22)
        r3 = chromatid(ixl, ys[2], iw, (REC, REC, REC), ("a", "b"), h=0.46, fz=22)
        r4 = chromatid(ixl, ys[3], iw, (REC, REC, REC), ("a", "b"), h=0.46, fz=22)
        self.at("One crossover")
        self.play(FadeIn(VGroup(r1, r2, r3, r4)), run_time=0.7)
        d = ys[1] - ys[2]
        self.at("two of the four")
        self.play(r2.M.animate.shift(DOWN * d), r2.R.animate.shift(DOWN * d),
                  r3.M.animate.shift(UP * d), r3.R.animate.shift(UP * d), run_time=1.0)
        frame = VGroup(SurroundingRectangle(VGroup(r2, r3), color=RED, buff=0.1, stroke_width=3))
        note = T("half are\nrecombinant", 26, RED, line_spacing=0.8).move_to([-4.4, -1.1, 0])
        self.at("half recombinant")
        self.play(Create(frame), FadeIn(note), run_time=0.7)

        # --- a second crossover puts the loci back --------------------------------------------
        self.at("second crossover")
        self.play(r2.R.animate.shift(UP * d), r3.R.animate.shift(DOWN * d), run_time=1.0)
        frame2 = SurroundingRectangle(VGroup(r2, r3), color=GREEN, buff=0.1, stroke_width=3)
        note2 = T("loci back in\ntheir old pairs", 26, GREEN, line_spacing=0.8).move_to([-4.4, -1.1, 0])
        self.at("put the loci back")
        self.play(ReplacementTransform(frame, frame2), ReplacementTransform(note, note2), run_time=0.7)

        # --- the curves ---------------------------------------------------------------------------
        diag = DashedLine(P(0, 0), P(50, 50), color=GREY, stroke_width=3)
        diag_t = T("dashed: frequency = distance\n(short intervals only)", 22, GREY, line_spacing=0.8).move_to([2.3, oy + 62 * sy, 0])
        curve = ParametricFunction(lambda t: P(t, haldane(t)), t_range=[0, 100, 1], color=TEAL, stroke_width=6)
        self.at("intervals are underestimated")
        self.play(Create(diag), FadeIn(diag_t), run_time=0.8)
        self.play(Create(curve), run_time=1.4)
        h_t = T("Haldane's function", 26, TEAL).move_to(P(66, 20))
        self.at("Haldane's function")
        self.play(FadeIn(h_t), run_time=0.6)

        self.at("independently")
        self.play(ShowPassingFlash(curve.copy().set_color(TEXT).set_stroke(width=9), time_width=0.6), run_time=1.6)

        # --- 17% -> about 20.8 cM ----------------------------------------------------------------
        hz = DashedLine(P(0, 17), P(20.8, 17), color=TEXT, stroke_width=3)
        vt = DashedLine(P(20.8, 17), P(20.8, 0), color=TEXT, stroke_width=3)
        dot = Dot(P(20.8, 17), radius=0.12, color=TEAL)
        call = T("17% = about 20.8 cM", 28, TEAL, weight=BOLD).move_to(P(66, 6.5))
        self.at("It turns")
        self.play(Create(hz), FadeIn(dot), run_time=0.6)
        self.play(Create(vt), FadeIn(call, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Phase(SpokenScene):
    """repulsion female: the recombinant and parental classes swap places; read the parents first."""

    def construct(self):
        fem = T("female", 28, GREY).move_to([-3.4, 1.7, 0])
        f1 = chromatid(-6.0, 0.95, 5.0, (DOM, DOM, DOM), ("A", "b"))
        f2 = chromatid(-6.0, 0.1, 5.0, (REC, REC, REC), ("a", "B"))
        self.play(FadeIn(fem), FadeIn(f1), FadeIn(f2), run_time=0.9)
        self.at("big A with little b")
        self.play(Indicate(f1, color=DOM, scale_factor=1.05), run_time=0.9)
        self.at("little a with")
        self.play(Indicate(f2, color=REC, scale_factor=1.05), run_time=0.9)

        base = -2.3
        xs = [1.2, 2.7, 4.2, 5.7]
        names = [("AB", (DOM, DOM)), ("ab", (REC, REC)), ("Ab", (DOM, REC)), ("aB", (REC, DOM))]
        pct = [8.5, 8.5, 41.5, 41.5]
        k = 3.3 / 41.5
        axis = Line([0.2, base, 0], [6.5, base, 0], color=GREY, stroke_width=3)
        labels = VGroup(*[allele_text(n[0], n[1], 30).move_to([x, base - 0.45, 0]) for n, x in zip(names, xs)])
        bars = [Rectangle(width=1.0, height=p * k, stroke_width=0, fill_color=GREY, fill_opacity=0.7)
                .move_to([x, base + p * k / 2, 0]) for x, p in zip(xs, pct)]
        self.at("still gives")
        self.play(Create(axis), FadeIn(labels), *[GrowFromEdge(b, DOWN) for b in bars], run_time=1.0)

        nums = [M(f"{p}%", 26, TEXT).next_to(b, UP, buff=0.12) for b, p in zip(bars, pct)]
        self.at("but now")
        self.play(*[b.animate.set_color(RED).set_opacity(0.9) for b in bars[:2]],
                  *[FadeIn(n) for n in nums[:2]], run_time=0.8)
        lab_r = T("recombinant", 26, RED).move_to([(xs[0] + xs[1]) / 2, base - 1.05, 0])
        self.play(FadeIn(lab_r), run_time=0.4)
        self.at("big A big B")
        self.play(Indicate(bars[0], color=TEXT, scale_factor=1.12), run_time=0.7)
        self.at("little a little b")
        self.play(Indicate(bars[1], color=TEXT, scale_factor=1.12), run_time=0.7)
        self.at("big A little b")
        self.play(Indicate(VGroup(bars[2], bars[3]), color=TEXT, scale_factor=1.05), run_time=0.8)
        self.at("are parental")
        self.play(*[b.animate.set_color(GREEN).set_opacity(0.9) for b in bars[2:]],
                  *[FadeIn(n) for n in nums[2:]], run_time=0.8)
        lab_p = T("parental", 26, GREEN).move_to([(xs[2] + xs[3]) / 2, base - 1.05, 0])
        self.play(FadeIn(lab_p), run_time=0.4)

        self.at("define the classes")
        self.play(Indicate(f1, color=TEXT, scale_factor=1.06), Indicate(f2, color=TEXT, scale_factor=1.06), run_time=0.9)

        # --- map with short intervals ---------------------------------------------------------
        self.at("not the counts")
        self.play(FadeOut(VGroup(axis, labels, *bars, *nums, lab_r, lab_p, fem, f1, f2)), run_time=0.7)
        line = Line([-5.4, 0, 0], [5.4, 0, 0], color=GREY, stroke_width=5)
        pts = [-5.4, -1.8, 1.8, 5.4]
        dots = VGroup(*[Dot([p, 0, 0], radius=0.16, color=TEXT) for p in pts])
        brs = VGroup(*[bracket(pts[i] + 0.1, pts[i + 1] - 0.1, 0.55, TEAL, up=False, tick=0.16) for i in range(3)])
        lbs = VGroup(*[T("short interval", 26, TEAL).move_to([(pts[i] + pts[i + 1]) / 2, 1.1, 0]) for i in range(3)])
        self.play(Create(line), FadeIn(dots), run_time=0.6)
        self.at("map with")
        self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(l)) for b, l in zip(brs, lbs)], lag_ratio=0.3), run_time=1.1)
        self.finish()


class S07End(EndCard):
    LINE = "Read the parents first, then map with short intervals."
