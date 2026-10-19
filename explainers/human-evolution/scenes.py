"""Human evolutionary history: a positive D is not proof  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the sampled African genome / P1 (and the African populations)
  YELLOW = the sampled Eurasian genome / P2 (and the ancestors of Eurasians)
  ORANGE = Neanderthal, Neanderthal-like segments, gene flow
  PURPLE = old population structure (the alternative history)
  GREEN  = D (the statistic) and the "clue" it gives
  TEAL   = time, recombination, segment length (the test)
  RED    = "no" (a crossed-out reading)
  GREY   = ancestral alleles, chromosomes, chimpanzee, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
SAFE_L, SAFE_R = -6.3, 6.3


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def site(derived, col, letter=None, size=0.5):
    """one site of a genome: filled = derived allele (B), hollow = ancestral allele (A)."""
    s = Square(size, stroke_color=col if derived else GREY, stroke_width=3,
               fill_color=col, fill_opacity=0.85 if derived else 0)
    g = VGroup(s)
    if letter:
        g.add(T(letter, 22, BG if derived else GREY, weight=BOLD).move_to(s))
    return g


def genome_row(y, derived, col, name, name_col, n=12, x0=-3.0, dx=0.78):
    sqs = VGroup(*[site(i in derived, col).move_to([x0 + i * dx, y, 0]) for i in range(n)])
    lab = T(name, 26, name_col)
    lab.move_to([x0 - 0.55 - lab.width / 2, y, 0])
    return VGroup(sqs, lab)


def card(pattern, title):
    """a four-row ABBA / BABA pattern card: African, Eurasian, Neanderthal, chimpanzee."""
    taxa = [("African", BLUE), ("Eurasian", YELLOW), ("Neanderthal", ORANGE), ("Chimpanzee", GREY)]
    rows = VGroup()
    for (name, col), a in zip(taxa, pattern):
        lab = T(name, 22, col)
        sq = site(a == "B", col, a)
        lab.next_to(sq, LEFT, buff=0.2)
        rows.add(VGroup(lab, sq))
    for i, r in enumerate(rows):                       # align the squares in one column
        r.shift(RIGHT * (rows[0][1].get_center()[0] - r[1].get_center()[0]))
    rows.arrange(DOWN, buff=0.14, aligned_edge=RIGHT)
    t = T(title, 28, TEXT, weight=BOLD).next_to(rows, UP, buff=0.22)
    return VGroup(t, rows)


def bars(h1, h2, base, x1, x2, n1=None, n2=None, w=1.3):
    b1 = Rectangle(width=w, height=h1, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.7)
    b2 = Rectangle(width=w, height=h2, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.7)
    b1.move_to([x1, base + h1 / 2, 0]); b2.move_to([x2, base + h2 / 2, 0])
    g = VGroup(b1, b2)
    if n1:
        g.add(M(n1, 30, YELLOW).next_to(b1, UP, buff=0.12), M(n2, 30, BLUE).next_to(b2, UP, buff=0.12))
    return g


def dscale(x0, x1, y, val=None):
    """the D scale from -1 to +1; returns group and a function giving the x for a value."""
    xs = lambda v: x0 + (v + 1) / 2 * (x1 - x0)
    line = Line([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=4)
    ticks = VGroup(*[Line([xs(v), y - 0.12, 0], [xs(v), y + 0.12, 0], color=GREY, stroke_width=3) for v in (-1, 0, 1)])
    labs = VGroup(M("-1", 22, GREY).move_to([xs(-1), y - 0.42, 0]), M("0", 22, GREY).move_to([xs(0), y - 0.42, 0]),
                  M("+1", 22, GREY).move_to([xs(1), y - 0.42, 0]))
    return VGroup(line, ticks, labs), xs


def marker(x, y):
    tri = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1, stroke_width=0).scale(0.2).rotate(PI)
    tri.move_to([x, y + 0.3, 0])
    return tri


def chrom(y, x0=-5.3, x1=5.3, h=0.7):
    return RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=h, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.25).move_to([(x0 + x1) / 2, y, 0])


def blocks(y, spans, h=0.7):
    return VGroup(*[Rectangle(width=b - a, height=h - 0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=0.95)
                    .move_to([(a + b) / 2, y, 0]) for a, b in spans])


def blob(label, col, pos, r=0.5, below=True, size=24):
    c = Circle(radius=r, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.3).move_to(pos)
    t = T(label, size, col)
    t.next_to(c, DOWN if below else UP, buff=0.15)
    return VGroup(c, t)


class S00Title(TitleCard):
    LESSON = "Human evolutionary history"
    TITLE = "A positive D is not proof"


# ---------------------------------------------------------------------------------------------
class S01Surplus(SpokenScene):
    """African / Neanderthal / Eurasian genomes; Eurasian shares more derived sites; chimp = ancestral; two histories."""

    def construct(self):
        N = {0, 2, 3, 5, 7, 9, 11}
        AF = {0, 7, 10}
        EU = {2, 3, 5, 8, 9, 11}
        r_af = genome_row(2.8, AF, BLUE, "African", BLUE)
        r_ne = genome_row(1.9, N, ORANGE, "Neanderthal", ORANGE)
        r_eu = genome_row(0.9, EU, YELLOW, "Eurasian", YELLOW)
        r_ch = genome_row(-0.2, set(), GREY, "Chimpanzee", GREY)
        
        tag = T("schematic: a few sites drawn for illustration", 22, GREY).move_to([0.5, 3.55, 0])
        self.at("sampled African genome")
        self.add(tag)
        self.play(FadeIn(r_af, shift=RIGHT * 0.2), run_time=0.7)
        self.at("sampled Eurasian genome")
        self.play(FadeIn(r_eu, shift=RIGHT * 0.2), run_time=0.7)
        self.at("with a Neanderthal genome")
        self.play(FadeIn(r_ne, shift=RIGHT * 0.2), run_time=0.7)

        # matches: only drawn where both genomes carry the derived allele
        xs = lambda i: -3.0 + i * 0.78
        m_eu = VGroup(*[Line([xs(i), 1.9 - 0.28, 0], [xs(i), 0.9 + 0.28, 0], color=YELLOW, stroke_width=5) for i in sorted(N & EU)])
        m_af = VGroup(*[Line([xs(i), 2.9 - 0.28, 0], [xs(i), 1.9 + 0.28, 0], color=BLUE, stroke_width=5) for i in sorted(N & AF)])
        self.at("shares more derived variants")
        self.play(LaggedStart(*[Create(l) for l in m_eu], lag_ratio=0.15), run_time=1.3)
        self.play(LaggedStart(*[Create(l) for l in m_af], lag_ratio=0.2), run_time=0.6)

        self.at("chimpanzee shows which allele")
        self.play(FadeIn(r_ch, shift=RIGHT * 0.2), run_time=0.7)
        leg1 = VGroup(site(False, GREY), T("ancestral allele", 24, GREY)).arrange(RIGHT, buff=0.2)
        leg2 = VGroup(site(True, TEXT), T("derived allele: a newer variant", 24, TEXT)).arrange(RIGHT, buff=0.2)
        leg = VGroup(leg1, leg2).arrange(RIGHT, buff=0.7).move_to([0.5, -1.2, 0])
        self.play(FadeIn(leg1, shift=UP * 0.1), run_time=0.5)
        self.at("derived variant is a newer one")
        self.play(FadeIn(leg2, shift=UP * 0.1), run_time=0.5)

        self.at("Where does the surplus")
        q = T("Where does the surplus come from?", 32, TEXT).move_to([0.5, -1.2, 0])
        self.play(FadeOut(leg), FadeIn(q, shift=UP * 0.1), run_time=0.6)
        self.at("Two different histories")
        h1 = chip("one history ?", ORANGE, size=28)
        h2 = chip("another history ?", PURPLE, size=28)
        VGroup(h1, h2).arrange(RIGHT, buff=1.0).move_to([0.5, -2.6, 0])
        self.play(FadeIn(h1, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(h2, shift=UP * 0.2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Count(SpokenScene):
    """ABBA and BABA site cards -> hypothetical counts 600 and 400 -> D = 0.20."""

    def construct(self):
        c1 = card("ABBA", "ABBA site").scale(1.15).move_to([-4.5, 1.65, 0])
        c2 = card("BABA", "BABA site").scale(1.15).move_to([-1.3, 1.65, 0])
        self.at("Count the sites")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.7)
        self.at("Eurasian and the Neanderthal share")
        ring1 = SurroundingRectangle(VGroup(c1[1][1], c1[1][2]), color=YELLOW, buff=0.06, stroke_width=3)
        self.play(Create(ring1), run_time=0.5)
        self.at("African and the Neanderthal share it")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.7)
        ring2 = SurroundingRectangle(VGroup(c2[1][0], c2[1][2]), color=BLUE, buff=0.06, stroke_width=3)
        self.play(Create(ring2), run_time=0.5)

        base = -2.9
        self.at("Suppose you count")
        bs = bars(0.01, 0.01, base, -4.5, -1.3)
        target = bars(2.1, 1.4, base, -4.5, -1.3, "600", "400")
        self.add(bs)
        self.play(Transform(bs, target[:2]), run_time=1.2)
        self.play(FadeIn(target[2]), FadeIn(target[3]), run_time=0.4)
        tag = T("hypothetical counts", 22, GREY).move_to([-2.9, -3.3, 0])
        self.play(FadeIn(tag), run_time=0.3)

        self.at("difference divided by the total")
        frac = VGroup(M("600 - 400", 30, TEXT), Line(LEFT * 1.2, RIGHT * 1.2, color=TEXT, stroke_width=3), M("600 + 400", 30, TEXT)).arrange(DOWN, buff=0.12)
        f1 = VGroup(M("D =", 34, GREEN), frac).arrange(RIGHT, buff=0.3).move_to([3.5, 1.9, 0])
        self.play(FadeIn(f1, shift=LEFT * 0.2), run_time=0.8)
        f2 = M("= 200 / 1,000", 32, TEXT).move_to([3.6, 0.3, 0])
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.6)

        self.at("which comes to")
        f3 = M("D = 0.20", 44, GREEN).move_to([3.5, -0.9, 0])
        self.play(Write(f3), run_time=0.8)
        sc, xs = dscale(0.9, 6.1, -2.4)
        mk = marker(xs(0.2), -2.4)
        self.play(FadeIn(sc), run_time=0.5)
        self.play(FadeIn(mk, shift=DOWN * 0.3), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Null(SpokenScene):
    """null: equal counts, D = 0 (in this sketch) -> 600/400, D = 0.20 -> not a percentage -> two histories."""

    def construct(self):
        base = -2.8
        cond = T("no gene flow, one randomly mating ancestor", 28, GREY).move_to([0, 3.15, 0])
        self.at("With no gene flow")
        self.play(FadeIn(cond, shift=DOWN * 0.1), run_time=0.7)

        self.at("the model predicts")
        eq = bars(2.6, 2.6, base, -4.2, -1.4)
        l1 = T("ABBA", 26, YELLOW).next_to(eq[0], DOWN, buff=0.15)
        l2 = T("BABA", 26, BLUE).next_to(eq[1], DOWN, buff=0.15)
        sk = T("in this sketch: equal counts", 24, GREY).move_to([-2.8, 1.6, 0])
        self.play(GrowFromEdge(eq[0], DOWN), GrowFromEdge(eq[1], DOWN), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.play(FadeIn(sk), run_time=0.4)
        sc, xs = dscale(1.0, 6.0, -0.2)
        mk = marker(xs(0), -0.2)
        dz = M("D = 0", 44, GREEN).move_to([3.5, 1.7, 0])
        self.at("equals zero")
        self.play(FadeIn(sc), FadeIn(mk, shift=DOWN * 0.3), Write(dz), run_time=0.9)

        self.at("here the Eurasian genome")
        unequal = bars(3.1, 2.07, base, -4.2, -1.4, "600", "400")
        sk2 = T("hypothetical counts", 24, GREY).move_to([-2.8, 1.6, 0])
        dz2 = M("D = 0.20", 44, GREEN).move_to([3.5, 1.7, 0])
        self.play(FadeOut(cond), Transform(eq, unequal[:2]), FadeIn(unequal[2]), FadeIn(unequal[3]),
                  Transform(sk, sk2), Transform(dz, dz2),
                  mk.animate.move_to([xs(0.2), 0.1, 0]), run_time=1.3)

        # --- not a percentage ------------------------------------------------------------
        self.at("do not read")
        self.play(FadeOut(VGroup(eq, unequal[2], unequal[3], l1, l2, sk, sc, mk, dz)), run_time=0.5)
        d = M("D = 0.20", 44, GREEN).move_to([-4.3, 0.5, 0])
        ne = T("not equal to", 28, GREY).move_to([-0.7, 0.5, 0])
        pc = chip("20% Neanderthal ancestry", ORANGE, size=28).move_to([3.7, 0.5, 0])
        self.play(FadeIn(d), run_time=0.4)
        self.play(FadeIn(ne), FadeIn(pc), run_time=0.5)
        x = VGroup(Line(pc.get_corner(UL), pc.get_corner(DR), color=RED, stroke_width=7),
                   Line(pc.get_corner(DL), pc.get_corner(UR), color=RED, stroke_width=7))
        self.play(Create(x), run_time=0.5)

        # --- two histories ---------------------------------------------------------------
        self.at("Old structure in")
        self.play(FadeOut(VGroup(d, ne, pc, x)), run_time=0.5)
        # left: gene flow
        lt = T("gene flow", 30, ORANGE, weight=BOLD).move_to([-3.2, 3.1, 0])
        ne_b = blob("Neanderthal", ORANGE, [-5.0, 1.4, 0])
        eu_b = blob("Eurasian", YELLOW, [-1.6, 1.4, 0])
        af_b = blob("African", BLUE, [-3.3, -0.7, 0])
        fl = Arrow([-4.45, 1.4, 0], [-2.15, 1.4, 0], color=ORANGE, stroke_width=6, buff=0)
        fl_t = T("interbreeding", 24, ORANGE).next_to(fl, UP, buff=0.12)
        # right: structure
        rt = T("old structure", 30, PURPLE, weight=BOLD).move_to([2.6, 3.1, 0])
        box = RoundedRectangle(corner_radius=0.2, width=3.9, height=2.1, stroke_color=PURPLE, stroke_width=4,
                               fill_color=PURPLE, fill_opacity=0.08).move_to([1.4, 0.95, 0])
        btitle = T("old subdivided African population", 22, PURPLE).next_to(box, UP, buff=0.12)
        cells = VGroup(*[Circle(radius=0.38, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3)
                         .move_to([0.5 + 1.2 * k, 0.95, 0]) for k in range(3)])
        cells[2].set_stroke(YELLOW).set_fill(YELLOW, 0.4)
        anc = T("ancestors of Eurasians,\nif closer to the Neanderthal lineage", 22, YELLOW, line_spacing=0.8).move_to([2.9, -0.55, 0])
        ne2 = blob("Neanderthal lineage", ORANGE, [5.0, 0.95, 0], r=0.4, size=22)
        nointer = T("no interbreeding", 24, PURPLE).move_to([3.3, -1.45, 0])
        self.play(FadeIn(lt), FadeIn(ne_b), FadeIn(eu_b), FadeIn(af_b), run_time=0.7)
        self.play(GrowArrow(fl), FadeIn(fl_t), run_time=0.6)
        self.play(FadeIn(rt), FadeIn(box), FadeIn(btitle), FadeIn(cells), run_time=0.7)
        self.play(FadeIn(ne2), FadeIn(anc), FadeIn(nointer), run_time=0.7)
        dl = chip("D above 0", GREEN, size=28).move_to([-3.2, -2.2, 0])
        dr = chip("D above 0", GREEN, size=28).move_to([3.3, -2.2, 0])

        self.at("also make D positive")
        self.play(FadeIn(dl, shift=UP * 0.1), FadeIn(dr, shift=UP * 0.1), run_time=0.6)
        self.at("consistent with gene flow")
        self.play(Indicate(VGroup(lt, dl), color=ORANGE, scale_factor=1.12), run_time=0.8)
        self.at("It is not proof")
        pr = T("consistent with gene flow, not proof", 28, RED, weight=BOLD).move_to([0, -3.15, 0])
        self.play(FadeIn(pr, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cut(SpokenScene):
    """recombination cuts an entering segment each generation; recent flow = long blocks, old structure = short pieces."""

    def construct(self):
        ys = [2.3, 0.6, -1.1]
        rows = [chrom(y) for y in ys]
        spans = [[(-3.3, 1.7)],
                 [(-3.3, -0.9), (-0.5, 1.7)],
                 [(-3.3, -2.4), (-2.0, -0.9), (-0.5, 0.4), (0.8, 1.7)]]
        blk = [blocks(y, s) for y, s in zip(ys, spans)]
        cap = T("a chromosome", 24, GREY).move_to([-4.4, ys[0] + 0.75, 0])

        self.at("Time can separate")
        self.wait(0.1)
        self.at("Recombination cuts")
        self.play(FadeIn(rows[0]), FadeIn(cap), run_time=0.6)
        self.at("DNA that entered")
        self.play(FadeIn(blk[0], scale=0.9), run_time=0.6)
        lab = T("DNA that entered from another population", 24, ORANGE).move_to([0.3, ys[0] + 0.75, 0])
        self.play(FadeIn(lab), FadeOut(cap), run_time=0.5)

        def step(i, label_x):
            a = Arrow([0, ys[i - 1] - 0.42, 0], [0, ys[i] + 0.42, 0], color=TEAL, stroke_width=5, buff=0)
            t = T("recombination", 24, TEAL).move_to([label_x, (ys[i - 1] + ys[i]) / 2, 0])
            self.play(GrowArrow(a), FadeIn(t), FadeIn(rows[i]), run_time=0.5)
            self.play(TransformFromCopy(blk[i - 1], blk[i]), run_time=0.8)
            return VGroup(a, t)

        self.at("shorter pieces")
        s1 = step(1, 2.0)
        self.at("every generation")
        s2 = step(2, 2.0)

        self.at("tens of thousands")
        self.play(FadeOut(VGroup(*rows, *blk, lab, s1, s2)), run_time=0.6)
        y1, y2 = 1.9, -0.9
        a_ch, b_ch = chrom(y1), chrom(y2)
        a_bl = blocks(y1, [(-4.9, -1.1), (0.9, 4.7)])
        b_sp = [(-5.0 + 0.55 * k, -5.0 + 0.55 * k + 0.28) for k in range(19)]
        b_bl = blocks(y2, b_sp)
        a_lab = T("gene flow tens of thousands of years ago: long blocks", 26, ORANGE).next_to(a_ch, UP, buff=0.2).align_to(a_ch, LEFT)
        self.play(FadeIn(a_ch), FadeIn(a_lab), run_time=0.5)
        self.play(FadeIn(a_bl, scale=0.95), run_time=0.7)

        self.at("Old structure leaves only short")
        b_lab = T("old structure: only short pieces", 26, PURPLE).next_to(b_ch, UP, buff=0.2).align_to(b_ch, LEFT)
        self.play(FadeIn(b_ch), FadeIn(b_lab), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in b_bl], lag_ratio=0.05), run_time=1.0)

        self.at("segment length carries")
        key = chip("segment length: a clue to timing", TEAL, size=30).move_to([0, -2.8, 0])
        self.play(FadeIn(key, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Dated(SpokenScene):
    """Ust'-Ishim ~45,000 years ago; longer segments than present-day; structure predicts no change; 7,000-13,000 years before."""

    def construct(self):
        # timeline: 0 (present) at x=5.8, 60,000 years ago at x=-5.8
        tx = lambda yrs: 5.8 - yrs * 11.6 / 60000.0
        ty = -2.4
        axis = Line([tx(60000), ty, 0], [tx(0), ty, 0], color=GREY, stroke_width=4)
        pres = VGroup(Line([tx(0), ty - 0.12, 0], [tx(0), ty + 0.12, 0], color=GREY, stroke_width=3),
                      T("present", 22, GREY).move_to([tx(0) - 0.2, ty - 0.45, 0]))
        mk = Dot([tx(45000), ty, 0], radius=0.14, color=TEAL)
        mk_t = T("Ust'-Ishim, about 45,000 years ago", 24, TEAL).move_to([tx(45000), ty - 0.55, 0])

        self.at("was a Homo sapiens")
        self.play(Create(axis), FadeIn(pres), run_time=0.8)
        self.play(FadeIn(mk, scale=2), FadeIn(mk_t, shift=UP * 0.1), run_time=0.7)

        # segment bars
        def seg_row(y, name, col, spans):
            ch = chrom(y, -3.6, 5.8, 0.6)
            lab = T(name, 26, col).move_to([-3.9 - 1.0, y, 0])
            lab.move_to([-3.85 - lab.width / 2, y, 0])
            return VGroup(ch, lab), blocks(y, spans, 0.6)
        ust, ust_b = seg_row(2.8, "Ust'-Ishim", TEAL, [(-3.4, -1.6), (0.0, 1.8), (3.4, 5.2)])
        prs, prs_b = seg_row(1.7, "present day", GREY, [(-3.4 + 1.0 * k, -3.4 + 1.0 * k + 0.6) for k in range(9)])
        self.at("His genome carried")
        self.play(FadeIn(ust), FadeIn(prs), run_time=0.6)
        self.play(FadeIn(ust_b, scale=0.95), FadeIn(prs_b, scale=0.95), run_time=0.8)
        sk = T("schematic: segment lengths only", 22, GREY).move_to([1.1, 1.05, 0])
        self.play(FadeIn(sk), run_time=0.4)

        self.at("Dated genomes should")
        self.play(Indicate(ust_b, color=ORANGE, scale_factor=1.06), run_time=0.9)

        self.at("a slight change")
        note = chip("old structure: only a slight change with age", PURPLE, size=28).move_to([0, 0.1, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.7)

        self.at("From the lengths")
        a = DashedLine([tx(45000) - 0.12, ty + 0.5, 0], [tx(52000), ty + 0.5, 0], color=ORANGE, stroke_width=4)
        br = Line([tx(52000), ty + 0.5, 0], [tx(58000), ty + 0.5, 0], color=ORANGE, stroke_width=9)
        e1 = Line([tx(52000), ty + 0.35, 0], [tx(52000), ty + 0.65, 0], color=ORANGE, stroke_width=5)
        e2 = Line([tx(58000), ty + 0.35, 0], [tx(58000), ty + 0.65, 0], color=ORANGE, stroke_width=5)
        bt = T("gene flow: 7,000 to 13,000 years before he lived", 24, ORANGE).move_to([-2.6, ty + 1.0, 0])
        self.play(Create(a), run_time=0.5)
        self.play(Create(br), FadeIn(e1), FadeIn(e2), FadeIn(bt, shift=UP * 0.1), run_time=0.8)

        self.at("carries the uncertainty")
        rough = T("an estimate; it depends on\nthe recombination model", 22, GREY, line_spacing=0.8).move_to([4.3, ty + 1.0, 0])
        self.play(FadeIn(rough, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """compare both models on the same data; conclusion for the sampled non-Africans only; clue -> test."""

    def construct(self):
        self.at("fit both histories")
        m1 = chip("gene flow model", ORANGE, size=28)
        m2 = chip("structure model", PURPLE, size=28)
        VGroup(m1, m2).arrange(RIGHT, buff=1.4).move_to([0, 2.5, 0])
        data = chip("the same data", GREY, size=28).move_to([0, 1.15, 0])
        a1 = Arrow(m1.get_bottom(), data.get_top() + LEFT * 0.4, color=GREY, stroke_width=4, buff=0.08)
        a2 = Arrow(m2.get_bottom(), data.get_top() + RIGHT * 0.4, color=GREY, stroke_width=4, buff=0.08)
        self.play(FadeIn(m1, shift=DOWN * 0.1), FadeIn(m2, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(data), GrowArrow(a1), GrowArrow(a2), run_time=0.7)

        concl = chip("Neanderthal gene flow into the ancestors\nof the sampled non-Africans", ORANGE, size=28)
        concl.move_to([-1.9, -0.6, 0])
        self.at("supports Neanderthal gene flow")
        self.play(FadeIn(concl, shift=UP * 0.2), run_time=0.9)

        self.at("Keep the conclusion")
        frame = SurroundingRectangle(concl, color=TEXT, buff=0.15, stroke_width=3)
        ftag = T("these samples only", 22, TEXT).next_to(frame, UP, buff=0.1)
        self.play(Create(frame), FadeIn(ftag), run_time=0.7)

        self.at("other contacts")
        oc = chip("other contacts", GREY, size=26).move_to([4.7, -0.6, 0])
        oc[0].set_stroke(opacity=0.6)
        oc_t = T("nothing shown", 22, GREY).next_to(oc, DOWN, buff=0.12)
        self.play(FadeIn(oc), FadeIn(oc_t), run_time=0.6)

        self.at("is a clue")
        clue = chip("a positive D: a clue", GREEN, size=30).move_to([-3.1, -2.7, 0])
        self.play(FadeIn(clue, shift=UP * 0.15), run_time=0.6)
        self.at("Test it with")
        test = chip("segment length: the test", TEAL, size=30).move_to([3.1, -2.7, 0])
        ar = Arrow(clue.get_right(), test.get_left(), color=TEXT, stroke_width=5, buff=0.12)
        self.play(GrowArrow(ar), FadeIn(test, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A positive D is a clue, not proof of gene flow."
