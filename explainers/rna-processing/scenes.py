"""RNA processing: a gene is longer than its message  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = exons, and the mRNA made of them (what is kept)
  GREY   = introns, DNA, labels, de-emphasized
  GOLD   = the 5' cap and its phosphates
  GREEN  = the poly(A) tail
  YELLOW = signal sequences (GU, AG, AAUAAA)
  ORANGE = the branch-point adenosine
  TEAL   = the small nuclear particles U1 and U2
  PURPLE = enzymes (exonuclease, poly(A) polymerase)
  RED    = lost, skipped, blocked, frame shifted
  TEXT   = neutral marks (question marks, the cut, sums)
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"

K = 9.6 / 5137.0          # scale: units per nucleotide in the gene bar
X0 = -4.7                 # left end of the transcript
LENS = [("e", 150), ("i", 900), ("e", 87), ("i", 1500), ("e", 100), ("i", 2000), ("e", 400)]


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


def gene(y, eh=1.0, ih=0.2):
    """the 5,137-nucleotide transcript to scale: 4 exons, 3 introns"""
    ex, it, x = [], [], X0
    for kind, n in LENS:
        w = n * K
        if kind == "e":
            r = Rectangle(width=w, height=eh, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.45)
            ex.append(r.move_to([x + w / 2, y, 0]))
        else:
            r = Rectangle(width=w, height=ih, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.55)
            it.append(r.move_to([x + w / 2, y, 0]))
        x += w
    return ex, it


def cap_parts(y):
    blob = VGroup(Circle(radius=0.42, stroke_color=GOLD, stroke_width=3.5, fill_color=GOLD, fill_opacity=0.3),
                  T("m7G", 22, GOLD)).move_to([-5.75, y, 0])
    dots = VGroup(*[Circle(radius=0.08, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([-5.2 + 0.17 * i, y, 0])
                    for i in range(3)])
    return blob, dots


def tail_text(y, x_left=4.98):
    t = M("AAAA", 28, GREEN, weight=BOLD)
    return t.move_to([x_left + t.width / 2, y, 0])


def strip(active):
    names = ["1  Cap", "2  Cut and tail", "3  Splice"]
    cs = []
    for i, n in enumerate(names):
        col = TEXT if i + 1 == active else GREY
        c = chip(n, col, size=24, pad=0.2, fill_opacity=0.22 if i + 1 == active else 0.06)
        cs.append(c)
    return VGroup(*cs).arrange(RIGHT, buff=0.5).move_to([0, 3.05, 0])


class S00Title(TitleCard):
    LESSON = "RNA processing"
    TITLE = "A gene is longer than its message"


# ---------------------------------------------------------------------------------------------
class S01Gap(SpokenScene):
    """the 5,137-nucleotide gene vs the 737-nucleotide mRNA: the puzzle"""

    def construct(self):
        ex, it = gene(0.5, eh=1.3)
        head = T("an imagined human gene", 30, GREY).move_to([0, 3.15, 0])
        self.at("imagined human gene")
        self.play(FadeIn(head), run_time=0.5)
        nums = [T(str(i + 1), 26, BLUE).next_to(e, UP, buff=0.18) for i, e in enumerate(ex)]
        self.at("four exons")
        self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.2) for e in ex], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.2), run_time=1.2)
        ilab = [T(f"intron {i + 1}", 24, GREY).next_to(r, DOWN, buff=0.35) for i, r in enumerate(it)]
        self.at("three introns")
        self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in it], lag_ratio=0.3),
                  LaggedStart(*[FadeIn(l) for l in ilab], lag_ratio=0.3), run_time=1.4)
        brace = BraceBetweenPoints([X0, 1.95, 0], [X0 + 9.6, 1.95, 0], UP, color=GREY)
        blab = T("5,137 nucleotides", 32, TEXT).move_to([0, 2.65, 0])
        self.at("it runs")
        self.play(GrowFromCenter(brace), Write(blab), run_time=1.0)

        # the short mRNA, built from copies of the exons
        short, x = [], X0
        for e in ex:
            w = e.width
            s = Rectangle(width=w, height=1.3, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.45)
            short.append(s.move_to([x + w / 2, -1.9, 0]))
            x += w
        mlab = T("mRNA: 737 nucleotides", 32, BLUE).next_to(short[-1], RIGHT, buff=0.35)
        self.at("carries only")
        self.play(*[ReplacementTransform(e.copy(), s) for e, s in zip(ex, short)], run_time=1.3)
        self.play(FadeIn(mlab), run_time=0.5)

        q = [T("?", 56, TEXT, weight=BOLD).move_to([r.get_center()[0], 1.5, 0]) for r in it]
        self.at("Where did the rest")
        self.play(LaggedStart(*[FadeIn(a, scale=1.4) for a in q], lag_ratio=0.25), run_time=1.0)

        p1 = T("primary transcript", 36, TEXT, weight=BOLD)
        p2 = T("is not yet a message", 36, GREY)
        VGroup(p1, p2).arrange(RIGHT, buff=0.3).move_to([0, -3.2, 0])
        self.at("primary transcript")
        self.play(Write(p1), run_time=0.9)
        self.at("not yet a message")
        self.play(Write(p2), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Ends(SpokenScene):
    """cap on the 5' end; AAUAAA guides a cut; poly(A) tail added with no template"""

    def construct(self):
        Y = 0.45
        ex, it = gene(Y, eh=1.3)
        self.add(*ex, *it)
        stp = strip(0)
        self.at("Three changes")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in stp], lag_ratio=0.25), run_time=1.0)

        # --- cap ---------------------------------------------------------------------------
        blob, dots = cap_parts(Y)
        caplab = T("cap", 26, GOLD).move_to([-5.75, Y + 1.0, 0])
        self.at("a cap goes")
        self.play(stp[0][0].animate.set_stroke(TEXT).set_fill(TEXT, 0.22), stp[0][1].animate.set_color(TEXT),
                  FadeIn(blob, shift=RIGHT * 0.5), FadeIn(caplab), run_time=0.9)
        self.at("methylated guanosine")
        self.play(Indicate(blob, color=GOLD, scale_factor=1.15), run_time=0.7)
        pl = T("three phosphates", 24, GOLD).move_to([-3.9, Y + 1.25, 0])
        lead = Line(pl.get_bottom() + [-0.3, -0.05, 0], [-5.03, Y + 0.2, 0], color=GOLD, stroke_width=2)
        self.at("three phosphates")
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.25), FadeIn(pl), Create(lead), run_time=0.9)

        exo = chip("exonuclease", PURPLE, size=24).move_to([-3.6, -1.9, 0])
        stop = inhib([-4.7, -1.45, 0], [-5.65, -0.3, 0], RED)
        self.at("blocks exonucleases")
        self.play(FadeIn(exo, shift=UP * 0.2), run_time=0.5)
        self.play(Create(stop[0]), run_time=0.5)
        self.play(Create(stop[1]), run_time=0.2)

        # --- cut and tail ---------------------------------------------------------------
        self.at("Near the other end")
        self.play(FadeOut(exo), FadeOut(stop), FadeOut(pl), FadeOut(lead), run_time=0.5)
        self.play(stp[0][0].animate.set_stroke(GREY).set_fill(GREY, 0.06), stp[0][1].animate.set_color(GREY),
                  stp[1][0].animate.set_stroke(TEXT).set_fill(TEXT, 0.22), stp[1][1].animate.set_color(TEXT), run_time=0.5)
        sig = chip("AAUAAA", YELLOW, size=24).move_to([2.9, Y + 1.7, 0])
        tick = Rectangle(width=0.14, height=1.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.95).move_to([4.5, Y, 0])
        lead2 = Line(sig.get_right() + [0.05, 0, 0], [4.5, Y + 0.65, 0], color=YELLOW, stroke_width=2.5)
        self.at("the signal")
        self.play(FadeIn(sig, shift=DOWN * 0.2), FadeIn(tick), Create(lead2), run_time=0.8)
        cut = DashedLine([4.98, Y - 0.7, 0], [4.98, Y + 0.7, 0], color=TEXT, stroke_width=4, dash_length=0.12)
        cutlab = T("cut about 10 to 30 nt past AAUAAA (not to scale)", 22, TEXT).move_to([1.6, Y - 1.0, 0])
        self.at("guides a cut")
        self.play(Create(cut), FadeIn(cutlab), run_time=0.7)

        pol = chip("poly(A) polymerase", PURPLE, size=24).move_to([3.9, -2.2, 0])
        tail = tail_text(Y)
        tlab = T("poly(A) tail", 22, GREEN).move_to([5.45, Y + 1.0, 0])
        self.at("polymerase adds")
        self.play(FadeIn(pol, shift=UP * 0.2), run_time=0.5)
        self.play(AddTextLetterByLetter(tail, time_per_char=0.12), FadeIn(tlab), run_time=0.9)

        dna = Line([X0, -1.05, 0], [X0 + 9.6, -1.05, 0], color=GREY, stroke_width=5)
        dlab = T("the gene (DNA)", 24, GREY).move_to([-0.2, -1.55, 0])
        self.at("without copying")
        self.play(Create(dna), FadeIn(dlab), run_time=0.8)
        self.at("not in the gene")
        self.play(Indicate(VGroup(tail, tlab), color=GREEN, scale_factor=1.15), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Signals(SpokenScene):
    """zoom to one intron: GU ... A ... AG, then U1 and U2 find the sites"""

    def construct(self):
        Y = 0.45
        ex, it = gene(Y)
        blob, dots = cap_parts(Y)
        tail = tail_text(Y)
        self.add(*ex, *it, blob, dots, tail)
        stp = strip(3)
        self.add(stp)

        E1 = Rectangle(width=1.5, height=1.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45).move_to([-5.25, Y, 0])
        E2 = Rectangle(width=1.5, height=1.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45).move_to([5.25, Y, 0])
        INT = Rectangle(width=9.0, height=0.24, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.55).move_to([0, Y, 0])
        t1, t2 = T("exon", 28, BLUE).move_to(E1), T("exon", 28, BLUE).move_to(E2)
        il = T("intron", 26, GREY).move_to([-0.8, Y - 0.5, 0])
        self.play(ReplacementTransform(ex[0], E1), ReplacementTransform(it[0], INT), ReplacementTransform(ex[1], E2),
                  FadeOut(VGroup(ex[2], ex[3], it[1], it[2], blob, dots, tail)), FadeIn(t1), FadeIn(t2), FadeIn(il), run_time=1.3)

        gu = VGroup(Rectangle(width=0.9, height=0.64, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.3),
                    T("GU", 26, YELLOW)).move_to([-4.05, Y, 0])
        ag = VGroup(Rectangle(width=0.9, height=0.64, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.3),
                    T("AG", 26, YELLOW)).move_to([4.05, Y, 0])
        self.at("rule")
        self.play(FadeIn(gu, scale=1.3), FadeIn(ag, scale=1.3), run_time=0.7)
        self.at("sits at")
        self.play(Indicate(gu, color=YELLOW, scale_factor=1.25), run_time=0.8)
        self.at("intron and")
        self.play(Indicate(ag, color=YELLOW, scale_factor=1.25), run_time=0.8)

        A = VGroup(Circle(radius=0.33, stroke_color=ORANGE, stroke_width=3.5, fill_color=ORANGE, fill_opacity=0.45),
                   T("A", 28, ORANGE, weight=BOLD)).move_to([2.0, Y, 0])
        bl = T("branch point", 26, ORANGE).move_to([2.0, Y + 1.25, 0])
        self.at("third site")
        self.play(FadeIn(A, scale=0.3), run_time=0.6)
        self.at("branch point")
        self.play(FadeIn(bl, shift=DOWN * 0.15), run_time=0.5)
        self.at("adenosine")
        self.play(Indicate(A, color=ORANGE, scale_factor=1.3), run_time=0.7)

        u1 = chip("U1", TEAL, size=26).move_to([-4.05, Y - 1.9, 0])
        self.at("small nuclear particle")
        self.play(FadeIn(u1, shift=UP * 0.2), run_time=0.7)
        t1s = VGroup(*[Line([-4.35 + 0.3 * i, Y - 0.38, 0], [-4.35 + 0.3 * i, Y - 0.72, 0], color=TEAL, stroke_width=4) for i in range(3)])
        self.at("base pairing")
        self.play(u1.animate.move_to([-4.05, Y - 1.1, 0]), run_time=0.6)
        self.play(Create(t1s), run_time=0.5)

        u2 = chip("U2", TEAL, size=26).move_to([2.0, Y - 1.9, 0])
        self.at("pairs with")
        self.play(FadeIn(u2, shift=UP * 0.2), run_time=0.6)
        self.play(u2.animate.move_to([1.1, Y - 1.1, 0]), run_time=0.6)
        t2s = VGroup(*[Line([0.8 + 0.3 * i, Y - 0.38, 0], [0.8 + 0.3 * i, Y - 0.72, 0], color=TEAL, stroke_width=4) for i in range(3)])
        self.play(Create(t2s), run_time=0.4)
        bulge_to = [2.0, Y + 0.6, 0]
        stalk = Line([2.0, Y, 0], bulge_to, color=GREY, stroke_width=4)
        self.at("bulged out")
        self.play(A.animate.move_to(bulge_to), bl.animate.move_to([2.0, Y + 1.7, 0]), Create(stalk), run_time=0.8)

        rest = self.narration_s + 0.4 - self.elapsed()
        if rest > 1.6:
            self.wait(rest - 1.4)
        self.play(FadeOut(VGroup(u1, u2, t1s, t2s, stalk)), A.animate.move_to([2.0, Y, 0]), bl.animate.move_to([2.0, Y + 1.25, 0]), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Lariat(SpokenScene):
    """two steps: branch A attacks the 5' site (lariat); freed exon attacks the 3' site (join, release)"""

    def construct(self):
        Y = 0.45
        E1 = Rectangle(width=1.5, height=1.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45).move_to([-5.25, Y, 0])
        E2 = Rectangle(width=1.5, height=1.4, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.45).move_to([5.25, Y, 0])
        INT = Rectangle(width=9.0, height=0.24, stroke_color=GREY, stroke_width=1.5, fill_color=GREY, fill_opacity=0.55).move_to([0, Y, 0])
        t1, t2 = T("exon", 28, BLUE).move_to(E1), T("exon", 28, BLUE).move_to(E2)
        E1g, E2g = VGroup(E1, t1), VGroup(E2, t2)
        gu = VGroup(Rectangle(width=0.9, height=0.64, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.3),
                    T("GU", 26, YELLOW)).move_to([-4.05, Y, 0])
        ag = VGroup(Rectangle(width=0.9, height=0.64, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.3),
                    T("AG", 26, YELLOW)).move_to([4.05, Y, 0])
        A = VGroup(Circle(radius=0.33, stroke_color=ORANGE, stroke_width=3.5, fill_color=ORANGE, fill_opacity=0.45),
                   T("A", 28, ORANGE, weight=BOLD)).move_to([2.0, Y, 0])
        self.add(INT, E1g, E2g, gu, ag, A)

        s1 = T("step 1", 34, TEXT, weight=BOLD).move_to([5.3, 3.0, 0])
        self.at("two steps")
        self.play(Indicate(VGroup(E1g, E2g), color=BLUE, scale_factor=1.04), run_time=0.7)
        self.at("In the first")
        self.play(FadeIn(s1), run_time=0.4)

        att1 = CurvedArrow([1.8, Y + 0.45, 0], [-4.55, Y + 0.5, 0], angle=TAU / 5, color=ORANGE, stroke_width=6)
        self.at("branch adenosine")
        self.play(Create(att1), run_time=1.0)
        # exon 1 is freed
        self.at("upstream exon is freed")
        self.play(E1g.animate.shift(UP * 1.8), FadeOut(att1), run_time=0.8)

        # the lariat: intron line becomes a loop with a tail
        C = np.array([0.9, Y, 0])
        loop = Circle(radius=1.1, stroke_color=GREY, stroke_width=9).move_to(C)
        tailln = Line([2.0 + 0.33, Y, 0], [3.6, Y, 0], color=GREY, stroke_width=9)
        gu_to = C + 1.1 * np.array([np.cos(np.radians(60)), np.sin(np.radians(60)), 0])
        lab = T("lariat", 30, TEXT, weight=BOLD).move_to([-1.0, Y, 0])
        self.at("forms a loop")
        self.play(ReplacementTransform(INT, VGroup(loop, tailln)), gu.animate.move_to(gu_to), run_time=1.3)
        self.at("the lariat")
        self.play(FadeIn(lab, scale=1.3), run_time=0.6)
        A.set_z_index(3); gu.set_z_index(3); ag.set_z_index(3)

        # step 2
        s2 = T("step 2", 34, TEXT, weight=BOLD).move_to([5.3, 3.0, 0])
        self.at("In the second step")
        self.play(ReplacementTransform(s1, s2), run_time=0.5)
        att2 = CurvedArrow([-4.4, Y + 1.8 + 0.4, 0], [4.45, Y + 0.7, 0], angle=-TAU / 8, color=BLUE, stroke_width=6)
        self.at("attacks the", nth=1)
        self.play(Create(att2), run_time=1.0)
        lar = VGroup(loop, tailln, A, gu, ag, lab)
        self.at("joined")
        self.play(FadeOut(att2), E1g.animate.move_to([-0.75, Y, 0]), E2g.animate.move_to([0.75, Y, 0]),
                  lar.animate.shift(DOWN * 2.2), run_time=1.4)
        self.at("released")
        self.play(lar.animate.shift(DOWN * 0.4), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Gone(SpokenScene):
    """all three introns out: 5,137 -> 737, with a cap and a tail"""

    def construct(self):
        Y = 2.0
        ex, it = gene(Y)
        blob, dots = cap_parts(Y)
        tail = tail_text(Y)
        self.add(*ex, *it, blob, dots, tail)

        names = [("900", "intron 1"), ("1,500", "intron 2"), ("2,000", "intron 3")]
        drops, labs = [], []
        self.at("Run it on")
        self.wait(0.3)
        for r, (n, nm), cue in zip(it, names, ["intron 1", "intron 2", "and intron 3"]):
            lab = M(n, 28, GREY).move_to([r.get_center()[0], -1.55, 0])
            self.at(cue)
            self.play(r.animate.move_to([r.get_center()[0], -0.75, 0]), FadeIn(lab, shift=UP * 0.2), run_time=0.8)
            drops.append(r); labs.append(lab)

        # exons slide together; cap and tail go with them
        x = X0
        moves = []
        for e in ex:
            moves.append(e.animate.move_to([x + e.width / 2, Y, 0]))
            x += e.width
        moves.append(tail.animate.move_to([x + 0.08 + tail.width / 2, Y, 0]))
        self.at("joins the four exons")
        self.play(*moves, run_time=1.3)
        mrna = VGroup(blob, dots, *ex, tail)
        self.play(mrna.animate.scale(1.7).move_to([0, 1.55, 0]), run_time=1.0)

        isum = M("900 + 1,500 + 2,000 = 4,400", 34, GREY).move_to([0, -2.45, 0])
        self.at("add up")
        self.play(Write(isum), run_time=1.1)
        esum = M("150 + 87 + 100 + 400 = 737", 36, BLUE).move_to([0, 0.25, 0])
        self.at("exons add up")
        self.play(Write(esum), run_time=1.1)

        self.at("shorter")
        self.play(FadeOut(VGroup(*drops, *labs)), isum.animate.set_opacity(0.0), run_time=0.8)
        res = M("5,137  →  737", 48, TEXT).move_to([0, -1.5, 0])
        self.play(FadeIn(res, shift=UP * 0.2), run_time=0.7)

        cl = T("cap", 26, GOLD).next_to(blob, UP, buff=0.2)
        tl = T("poly(A) tail", 26, GREEN).next_to(tail, UP, buff=0.2)
        self.at("cap and a tail")
        self.play(FadeIn(cl), FadeIn(tl), Indicate(blob, color=GOLD, scale_factor=1.1), Indicate(tail, color=GREEN, scale_factor=1.1), run_time=1.0)
        self.at("never encoded")
        self.play(Indicate(VGroup(cl, tl), color=TEXT, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def cell_positions(n, grouped, w=0.085, gin=0.012, ggap=0.06, extra_gap=True):
    xs, x = [], 0.0
    for i in range(n):
        xs.append(x + w / 2)
        x += w + gin
        if grouped and (i + 1) % 3 == 0 and i + 1 < n:
            x += ggap - gin
    width = x - gin
    return xs, width


def cell_row(n, color, y, grouped, w=0.085):
    xs, wd = cell_positions(n, grouped, w)
    cells = VGroup(*[Square(side_length=w, stroke_width=0.6, stroke_color=color, fill_color=color, fill_opacity=0.9)
                     .move_to([x - wd / 2, y, 0]) for x in xs])
    return cells


class S06Frame(SpokenScene):
    """skip exon 2 (87 = 3x29, frame kept) vs exon 3 (100 = 3x33+1, frame shifts); the rule"""

    def construct(self):
        # exon row to scale (737 nt over 11 units) with small gaps for the introns
        U = 11.0 / 737
        lens = [150, 87, 100, 400]
        gap = 0.3
        total = 11.0 + 3 * gap
        x = -total / 2
        RY = 3.0
        blocks, vals, idx, links = [], [], [], []
        for i, n in enumerate(lens):
            w = n * U
            b = Rectangle(width=w, height=0.85, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.45).move_to([x + w / 2, RY, 0])
            v = M(str(n), 24, TEXT).move_to(b)
            ix = T(f"exon {i + 1}", 22, GREY).move_to([x + w / 2, RY - 0.75, 0])
            blocks.append(b); vals.append(v); idx.append(ix)
            if i < 3:
                links.append(Line([x + w, RY, 0], [x + w + gap, RY, 0], color=GREY, stroke_width=5))
            x += w + gap
        self.add(*blocks, *vals, *idx, *links)

        def reset_exons():
            return [blocks[i].animate.set_stroke(BLUE).set_fill(BLUE, 0.45) for i in (1, 2)] + [FadeOut(m) for m in []]

        # --- a splice-site change, exon 2 skipped ---------------------------------------
        mark = Square(side_length=0.26, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(links[1].get_center() + [0, 0.0, 0])
        self.at("splice site")
        self.play(FadeIn(mark, scale=2.5), run_time=0.6)
        bypass = ArcBetweenPoints(blocks[0].get_corner(UR) + [0.0, 0.0, 0], blocks[2].get_corner(UL) + [0, 0, 0], angle=-1.4, color=GREY, stroke_width=4)
        self.at("often skipped")
        self.play(blocks[1].animate.set_stroke(RED).set_fill(RED, 0.4), Create(bypass), run_time=0.9)

        # --- exon 2: 87 = 3 x 29 -------------------------------------------------------
        CY = 0.85
        row87 = cell_row(87, RED, CY, False)
        lab87 = M("87 nucleotides", 32, RED).move_to([0, 1.5, 0])
        self.at("Lose exon 2")
        self.play(Indicate(blocks[1], color=RED, scale_factor=1.12), run_time=0.7)
        self.at("87 nucleotides")
        self.play(FadeIn(lab87), LaggedStart(*[FadeIn(c) for c in row87], lag_ratio=0.01), run_time=1.1)
        xs_g, wd_g = cell_positions(87, True)
        lab87b = M("87 = 3 × 29", 36, RED).move_to([0, 1.5, 0])
        self.at("3 times 29")
        self.play(*[c.animate.move_to([xg - wd_g / 2, CY, 0]) for c, xg in zip(row87, xs_g)], ReplacementTransform(lab87, lab87b), run_time=1.3)

        # downstream reading frame row
        FY = -1.55
        pitch = 0.5
        fx0 = -(12 * pitch) / 2 + pitch / 2
        fcells = VGroup(*[Square(side_length=0.42, stroke_color=BLUE, stroke_width=2, fill_color=BLUE, fill_opacity=0.3).move_to([fx0 + i * pitch, FY, 0]) for i in range(12)])
        flab = T("reading frame in exon 4", 24, GREY).move_to([0, FY + 0.65, 0])

        def brackets(shift, color):
            out = VGroup()
            for g in range(4):
                a = fx0 + (3 * g + shift) * pitch - 0.21
                b = fx0 + (3 * g + shift + 2) * pitch + 0.21
                if a < fx0 - 0.3 or b > fx0 + 11 * pitch + 0.3:
                    continue
                out.add(Line([a, FY - 0.42, 0], [b, FY - 0.42, 0], color=color, stroke_width=6))
            return out
        br0 = brackets(0, BLUE)
        self.at("The frame is kept")
        self.play(FadeIn(fcells), FadeIn(flab), Create(br0), run_time=0.9)
        kept = T("frame kept", 34, BLUE, weight=BOLD).move_to([0, FY - 1.05, 0])
        self.play(FadeIn(kept, shift=UP * 0.15), run_time=0.5)
        loss = T("the protein loses 29 amino acids", 30, RED).move_to([0, 0.05, 0])
        self.at("loses")
        self.play(FadeIn(loss, shift=UP * 0.15), run_time=0.7)

        # --- exon 3 instead: clear the old answer first ---------------------------------------
        row100 = cell_row(100, RED, CY, True)
        lab100 = M("100 = 3 × 33 + 1", 36, RED).move_to([0, 1.5, 0])
        self.at("exon 3 instead")
        self.play(FadeOut(row87), FadeOut(lab87b), FadeOut(loss), FadeOut(kept), FadeOut(bypass), FadeOut(mark),
                  blocks[1].animate.set_stroke(BLUE).set_fill(BLUE, 0.45),
                  blocks[2].animate.set_stroke(RED).set_fill(RED, 0.4), run_time=0.7)
        mark2 = Square(side_length=0.26, stroke_width=0, fill_color=RED, fill_opacity=1).move_to(links[2].get_center())
        bypass2 = ArcBetweenPoints(blocks[1].get_corner(UR), blocks[3].get_corner(UL), angle=-1.4, color=GREY, stroke_width=4)
        self.play(FadeIn(mark2, scale=2.0), Create(bypass2), run_time=0.5)
        self.at("100 go")
        self.play(FadeIn(lab100), FadeIn(row100), run_time=0.8)
        # the one leftover base, in red outline, set apart
        left = row100[-1]
        self.at("plus 1")
        self.play(Indicate(left, color=TEXT, scale_factor=3.0), run_time=0.8)
        br1 = brackets(1, RED)
        shifts = T("frame shifts by one base", 34, RED, weight=BOLD).move_to([0, FY - 1.05, 0])
        self.at("frame shifts")
        self.play(Transform(br0, br1), FadeIn(shifts, shift=UP * 0.15), run_time=1.0)

        # --- the rule -----------------------------------------------------------------------
        everything = VGroup(*blocks, *vals, *idx, *links, mark2, bypass2, row100, lab100, fcells, flab, br0, shifts)
        r1 = T("frame kept if", 44, BLUE, weight=BOLD)
        r2 = T("(change in coding length) ÷ 3", 44, TEXT)
        r3 = T("leaves remainder 0", 44, BLUE, weight=BOLD)
        card = VGroup(r1, r2, r3).arrange(DOWN, buff=0.35).move_to([0, 0.7, 0])
        box = SurroundingRectangle(card, color=GREY, buff=0.4, corner_radius=0.2, stroke_width=3)
        self.at("this rule")
        self.play(FadeOut(everything), run_time=0.6)
        self.play(FadeIn(card, shift=UP * 0.15), Create(box), run_time=0.9)
        e1 = M("87  → remainder 0 → kept", 30, BLUE).move_to([0, -2.1, 0])
        e2 = M("100 → remainder 1 → shifts", 30, RED).move_to([0, -2.85, 0])
        self.at("survives")
        self.play(FadeIn(e1, shift=UP * 0.1), run_time=0.5)
        self.at("length lost")
        self.play(FadeIn(e2, shift=UP * 0.1), run_time=0.5)
        self.at("multiple of 3")
        self.play(Indicate(r3, color=BLUE, scale_factor=1.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "The frame survives only if the loss is a multiple of three."
