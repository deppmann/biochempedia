"""Family linkage and positional cloning: following a trait to its gene  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  RED    = the trait: affected people, the broken gene, its mutations
  BLUE   = the chromosome (or stretch of it) that carries the disease allele, and the marker allele "2" that travels with it
  GREY   = unaffected people, ordinary chromosomes, the other marker allele "1", structure
  YELLOW = the LOD score (evidence), the linked interval
  GREEN  = genes inside the interval (candidates)
  ORANGE = recombinants and cautions (the pitfalls)
  TEAL   = the control that catches a pitfall
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), buff=0.0, color=color, stroke_width=w,
                 tip_length=tip, max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def seg(a, b, color=GREY, w=3):
    return Line(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), color=color, stroke_width=w)


def hbar(x0, x1, y, color=GREY, h=0.34, fo=0.28):
    return RoundedRectangle(corner_radius=min(0.12, h / 2), width=x1 - x0, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=fo).move_to([(x0 + x1) / 2, y, 0])


def vbar(x, y0, y1, color=GREY, w=0.4, fo=0.28):
    return RoundedRectangle(corner_radius=min(0.12, w / 2), width=w, height=y1 - y0, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=fo).move_to([x, (y0 + y1) / 2, 0])


# ---- pedigree ------------------------------------------------------------------------------
DX = -2.7          # whole pedigree sits left of centre
S = 0.66           # symbol size
Y1, Y2, Y3 = 2.3, 0.2, -1.9

# name: (kind, x, y, affected, genotype) ; genotype is the pair of marker alleles, "2" travels with the trait
PEOPLE = {
    "I1": ("m", -1.5, Y1, True, "21"), "I2": ("f", 0.0, Y1, False, "11"),
    "II1": ("m", -3.0, Y2, True, "21"), "II2": ("f", -1.5, Y2, False, "11"),
    "II4": ("m", 0.0, Y2, False, "11"), "II3": ("f", 1.5, Y2, True, "21"), "SP": ("m", 3.0, Y2, False, "11"),
    "III1": ("m", 0.9, Y3, True, "21"), "III2": ("f", 2.25, Y3, False, "11"), "III3": ("f", 3.6, Y3, True, "21"),
}
KIDS = {"I": ["II1", "II2", "II4", "II3"], "II": ["III1", "III2", "III3"]}
COUPLES = {"I": ("I1", "I2"), "II": ("II3", "SP")}


def pxy(name):
    k, x, y, a, g = PEOPLE[name]
    return np.array([x + DX, y, 0.0])


def symbol(name):
    k, x, y, a, g = PEOPLE[name]
    col = RED if a else TEXT
    if k == "m":
        s = Square(side_length=S)
    else:
        s = Circle(radius=S / 2)
    s.set_stroke(col if a else GREY, 3).set_fill(RED if a else BG, 0.85 if a else 1.0)
    return s.move_to(pxy(name))


def geno(name, size=26):
    k, x, y, a, g = PEOPLE[name]
    parts = VGroup(*[M(c, size, BLUE if c == "2" else GREY, weight=BOLD) for c in g]).arrange(RIGHT, buff=0.22)
    return parts.move_to(pxy(name) + DOWN * 0.64)


def ped_lines():
    out = VGroup()
    for key, (a, b) in COUPLES.items():
        pa, pb = pxy(a), pxy(b)
        out.add(seg(pa + RIGHT * S / 2, pb + LEFT * S / 2, GREY, 3))
        mid = (pa + pb) / 2
        ys = pa[1] - 1.0
        kids = KIDS[key]
        xs = [pxy(k)[0] for k in kids]
        out.add(seg(mid, [mid[0], ys], GREY, 3))
        out.add(seg([min(xs + [mid[0]]), ys], [max(xs + [mid[0]]), ys], GREY, 3))
        for k in kids:
            out.add(seg([pxy(k)[0], ys], pxy(k) + UP * S / 2, GREY, 3))
    return out


def ped_syms():
    return VGroup(*[symbol(n) for n in PEOPLE])


def ped_genos():
    return VGroup(*[geno(n) for n in PEOPLE])


AFFECTED = [n for n, v in PEOPLE.items() if v[3]]


def legend(y=-3.25, x=-3.3):
    a = Square(side_length=0.3).set_stroke(RED, 3).set_fill(RED, 0.85).move_to([x - 1.8, y, 0])
    la = lab("affected", 24, TEXT).next_to(a, RIGHT, buff=0.15)
    u = Circle(radius=0.15).set_stroke(GREY, 3).set_fill(BG, 1).move_to([x + 0.7, y, 0])
    lu = lab("unaffected", 24, TEXT).next_to(u, RIGHT, buff=0.15)
    return VGroup(a, la, u, lu)


def gene_box(x, y, w=0.9, h=0.5, color=GREEN, fo=0.35):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fo).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Following a Trait to Its Gene"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a trait in a family; which stretch of which chromosome; no handle without a guessed protein."""

    def construct(self):
        lines, syms = ped_lines(), ped_syms()
        bx = 5.5
        bar = vbar(bx, -3.0, 3.0, GREY, 0.5, 0.3)
        barl = lab("chromosome", 22, GREY).move_to([bx, 3.35, 0])

        self.at("Which stretch")
        self.play(FadeIn(lines), FadeIn(syms), run_time=1.0)
        self.play(FadeIn(bar), FadeIn(barl), run_time=0.5)
        leg = legend()
        self.play(FadeIn(leg), run_time=0.4)
        br = Brace(Line([bx, -0.4, 0], [bx, 1.4, 0]), direction=LEFT, color=YELLOW, buff=0.5)
        q1 = T("?", 56, YELLOW, weight=BOLD).next_to(br, LEFT, buff=0.15)
        stretch = lab("which stretch?", 24, YELLOW).next_to(q1, LEFT, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(q1), FadeIn(stretch), run_time=0.6)

        self.at("which gene inside")
        g = gene_box(bx, 0.5, 0.5, 0.36, GREEN, 0.2)
        gq = T("?", 36, GREEN, weight=BOLD).move_to(g)
        self.play(FadeIn(g), FadeIn(gq), run_time=0.5)

        self.at("Before DNA markers")
        self.play(FadeOut(VGroup(br, q1, stretch)), FadeOut(leg), run_time=0.4)
        c1 = chip("its protein, guessed", GREY, 24).move_to([3.3, 1.7, 0])
        c2 = chip("a nearby known gene", GREY, 24).move_to([3.3, 0.5, 0])
        need = lab("needed first", 26, TEXT).move_to([3.3, 2.6, 0])
        self.play(FadeIn(need), FadeIn(c1, shift=RIGHT * 0.2), FadeIn(c2, shift=RIGHT * 0.2), run_time=0.7)
        a1 = arr(c1.get_right() + RIGHT * 0.08, [bx - 0.3, 1.2, 0], GREY, 3, 0.15)
        a2 = arr(c2.get_right() + RIGHT * 0.08, [bx - 0.3, 0.45, 0], GREY, 3, 0.15)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.4)

        self.at("A gene known only")
        eff = chip("known only from its effect", RED, 20).move_to([3.2, -1.1, 0])
        cut = T("✕", 40, RED, weight=BOLD).move_to([5.0, -1.1, 0])
        self.play(FadeIn(eff, shift=UP * 0.2), run_time=0.5)
        self.at("no handle")
        nh = lab("no handle", 32, RED, weight=BOLD).move_to([2.9, -2.2, 0])
        self.play(Create(cut), FadeIn(nh), FadeOut(VGroup(a1, a2)), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
def chrom_panel(xs=(2.2, 3.7, 5.2), y0=-2.6, y1=2.6):
    bars = VGroup(*[vbar(x, y0, y1, GREY, 0.42, 0.3) for x in xs])
    rng = np.random.RandomState(4)
    ticks = VGroup()
    pos = {}
    for i, x in enumerate(xs):
        ys = np.sort(rng.uniform(y0 + 0.4, y1 - 0.4, 6))
        for j, y in enumerate(ys):
            t = seg([x - 0.3, y, 0], [x + 0.3, y, 0], TEXT, 3)
            ticks.add(t)
            pos[(i, j)] = (x, y)
    return bars, ticks, pos


class S02Markers(SpokenScene):
    """collect families; markers spread across the genome; each marker typed in every member."""

    def construct(self):
        lines, syms = ped_lines(), ped_syms()
        title = lab("idealised example family", 24, GREY).move_to([-2.9, 3.45, 0])
        self.at("Collect families")
        self.play(FadeIn(title), FadeIn(lines), FadeIn(syms), run_time=1.0)
        self.at("affected and unaffected")
        leg = legend()
        self.play(FadeIn(leg), *[Indicate(syms[list(PEOPLE).index(n)], color=RED, scale_factor=1.25) for n in AFFECTED], run_time=1.2)

        self.at("variable markers")
        bars, ticks, pos = chrom_panel()
        self.play(FadeIn(bars), run_time=0.5)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.05), run_time=0.9)
        gl = lab("markers across the genome", 24, TEXT).move_to([3.7, -3.2, 0])
        self.play(FadeIn(gl), run_time=0.3)

        self.at("Each marker is typed")
        i, j = 1, 3
        x, y = pos[(i, j)]
        hl = seg([x - 0.34, y, 0], [x + 0.34, y, 0], BLUE, 8)
        self.play(FadeIn(hl), FadeOut(gl), run_time=0.4)
        tl = lab("one marker, typed in everyone", 24, BLUE).move_to([3.7, -3.2, 0])
        self.play(FadeIn(tl), run_time=0.3)
        genos = ped_genos()
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in genos], lag_ratio=0.18), run_time=2.0)

        self.at("tested for")
        q = lab("does allele 2 follow the trait in this family?", 24, BLUE).move_to([-2.9, -3.25, 0])
        self.play(FadeOut(leg), FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Cosegregation(SpokenScene):
    """recombination: near marker stays with the gene, far one separates; allele 2 follows the trait."""

    def construct(self):
        lines, syms, genos = ped_lines(), ped_syms(), ped_genos()
        title = lab("idealised pedigree, one marker", 24, GREY).move_to([-2.9, 3.45, 0])
        self.add(title, lines, syms, genos)

        X0, X1 = 1.8, 6.3
        xg, xn, xf, xc = 3.0, 3.6, 5.5, 4.55
        yA, yB, yC = 2.8, 2.0, 0.2
        H = 0.46
        mk = lambda x, y, c: seg([x, y - 0.3, 0], [x, y + 0.3, 0], c, 6)
        self.at("The physical fact")
        A = hbar(X0, X1, yA, BLUE, H)
        B = hbar(X0, X1, yB, GREY, H)
        gene = seg([xg, yA - 0.32, 0], [xg, yA + 0.32, 0], RED, 8)
        nearA, farA = mk(xn, yA, BLUE), mk(xf, yA, BLUE)
        nearB, farB = mk(xn, yB, GREY), mk(xf, yB, GREY)
        gl = lab("gene", 22, RED).move_to([xg - 0.1, yA + 0.55, 0])
        self.play(FadeIn(A), FadeIn(B), run_time=0.5)
        self.play(FadeIn(gene), FadeIn(gl), FadeIn(nearA), FadeIn(farA), FadeIn(nearB), FadeIn(farB), run_time=0.5)
        tl = lab("idealised meiosis: one crossover", 22, TEXT).move_to([4.05, 1.2, 0])
        self.play(FadeIn(tl), run_time=0.3)

        self.at("Markers close")
        cross = T("✕", 46, ORANGE, weight=BOLD).move_to([xc, (yA + yB) / 2, 0])
        self.play(FadeIn(cross, scale=1.4), run_time=0.4)
        left = hbar(X0, xc, yC, BLUE, H)
        right = hbar(xc, X1, yC, GREY, H)
        gene2 = seg([xg, yC - 0.32, 0], [xg, yC + 0.32, 0], RED, 8)
        n2, f2 = mk(xn, yC, BLUE), mk(xf, yC, GREY)
        nl = lab("near", 22, TEXT).move_to([xn, yC - 0.55, 0])
        fl = lab("far", 22, TEXT).move_to([xf, yC - 0.55, 0])
        self.play(FadeIn(left), FadeIn(right), FadeIn(gene2), FadeIn(n2), FadeIn(f2), FadeIn(nl), FadeIn(fl), run_time=0.7)
        s1 = lab("near marker stays with the gene", 22, BLUE).move_to([4.05, yC - 1.1, 0])
        s2 = lab("far marker is separated", 22, ORANGE).move_to([4.05, yC - 1.6, 0])
        self.play(FadeIn(s1), run_time=0.4)
        self.play(FadeIn(s2), run_time=0.4)

        self.at("travel with the trait")
        rects = VGroup(*[SurroundingRectangle(genos[list(PEOPLE).index(n)][0], color=BLUE, buff=0.08, stroke_width=3)
                         for n in AFFECTED])
        self.play(LaggedStart(*[Create(r) for r in rects], lag_ratio=0.15), run_time=1.0)

        self.at("One percent")
        self.play(FadeOut(VGroup(s1, s2)), run_time=0.3)
        pct = VGroup(lab("1% recombination", 28, YELLOW), lab("= 1 centimorgan", 28, YELLOW)).arrange(DOWN, buff=0.1).move_to([4.05, -2.2, 0])
        self.play(FadeIn(pct, shift=UP * 0.1), run_time=0.5)

        self.at("few or no recombinants")
        rc = lab("example: no recombinants", 24, TEXT).move_to([-2.9, -3.25, 0])
        self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Narrowing(SpokenScene):
    """more recombinants shrink the interval; genes in the interval; mutations in affected people."""

    def construct(self):
        X0, X1 = -5.8, 5.8
        gt = lambda y: seg([0.1, y - 0.33, 0], [0.1, y + 0.33, 0], RED, 7)
        chrom = VGroup(hbar(X0, X1, 3.1, GREY, 0.5), gt(3.1))
        cl = lab("chromosome, with the gene (red tick)", 22, GREY).move_to([-3.6, 3.65, 0])
        idl = lab("idealised", 22, ORANGE).move_to([5.4, 3.65, 0])
        blab = lab("affected people's recombinant chromosomes; blue = shared with the disease chromosome", 22, TEXT).move_to([0, -2.6, 0])
        self.add(idl)
        rows = [(-5.8, 3.4), (-2.2, 5.8), (-5.8, 1.0), (-0.8, 5.8)]
        ys = [2.25, 1.45, 0.65, -0.15]
        bands = [(-5.8, 3.4), (-2.2, 3.4), (-2.2, 1.0), (-0.8, 1.0)]
        bars = [VGroup(hbar(X0, X1, y, GREY, 0.5, 0.2), hbar(a, b, y, BLUE, 0.5, 0.5), gt(y)) for (a, b), y in zip(rows, ys)]
        self.add(chrom, cl)

        def band(i):
            bl, br_ = bands[i]
            top, bot = 2.25 + 0.35, ys[i] - 0.35
            return Rectangle(width=br_ - bl, height=top - bot, stroke_color=YELLOW, stroke_width=2.5,
                             fill_color=YELLOW, fill_opacity=0.14).move_to([(bl + br_) / 2, (top + bot) / 2, 0])

        self.at("Examine more recombinant")
        self.play(FadeIn(bars[0]), FadeIn(blab), run_time=0.5)
        band_rect = band(0)
        lbl = lab("few meioses: a long stretch", 28, YELLOW).move_to([0, -1.3, 0])
        self.play(FadeIn(band_rect), FadeIn(lbl), run_time=0.4)
        for i in (1, 2, 3):
            self.play(FadeIn(bars[i], shift=UP * 0.1), run_time=0.25)
            self.play(Transform(band_rect, band(i)), run_time=0.4)
            if i == 1:
                self.at("interval shrinks")
        newl = lab("more meioses: interval shrunk", 28, YELLOW).move_to([0, -1.3, 0])
        self.play(FadeOut(lbl), FadeIn(newl), run_time=0.3)

        self.at("Then find the genes")
        fade = VGroup(*bars, chrom, cl)
        interval = Rectangle(width=1.8, height=0.3, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5).move_to([0.1, -0.15, 0])
        gx = np.linspace(-4.4, 4.4, 6)
        gbox = VGroup(*[gene_box(x, -2.4, 1.3, 1.0, GREEN, 0.25) for x in gx])
        spread = VGroup(seg([-1.0, -0.3, 0], [-5.05, -1.9, 0], YELLOW, 2), seg([0.8, -0.3, 0], [5.05, -1.9, 0], YELLOW, 2))
        self.play(FadeOut(newl), FadeOut(blab), FadeOut(band_rect), fade.animate.set_opacity(0.2), FadeIn(interval), run_time=0.5)
        self.play(Create(spread), LaggedStart(*[FadeIn(b) for b in gbox], lag_ratio=0.12), run_time=1.1)
        gl = lab("genes in the interval", 28, GREEN).move_to([0, -1.0, 0])
        self.play(FadeIn(gl), run_time=0.3)
        self.at("expressed genes")
        gl2 = lab("the expressed genes among them", 28, GREEN).move_to([0, -1.0, 0])
        self.play(FadeOut(gl), FadeIn(gl2), *[b.animate.set_fill(GREEN, 0.5) for b in gbox], run_time=0.5)

        self.at("search them for mutations")
        pick = gbox[3]
        self.play(Indicate(pick, color=RED, scale_factor=1.12), pick.animate.set_stroke(RED, 4), run_time=0.8)

        self.at("Proof is")
        self.play(gbox.animate.set_opacity(0.25), pick.animate.set_fill(GREEN, 0.5).set_stroke(RED, 4, 1.0), FadeOut(gl2), FadeOut(spread),
                  FadeOut(fade), FadeOut(interval), run_time=0.5)
        self.play(pick.animate.move_to([-3.4, 0.2, 0]).scale(1.8), FadeOut(VGroup(*[b for b in gbox if b is not pick])), run_time=0.7)
        gname = lab("the same gene", 30, RED).move_to([-3.4, 1.6, 0])
        self.play(FadeIn(gname), run_time=0.3)
        cx = 1.6
        ra = VGroup(hbar(cx - 1.5, cx + 1.5, 1.0, GREY, 0.5, 0.3), seg([cx - 0.7, 0.7, 0], [cx - 0.7, 1.3, 0], RED, 8))
        rb = VGroup(hbar(cx - 1.5, cx + 1.5, -0.4, GREY, 0.5, 0.3), seg([cx + 0.6, -0.7, 0], [cx + 0.6, -0.1, 0], RED, 8))
        la = lab("affected, family A", 24, TEXT).next_to(ra, RIGHT, buff=0.3)
        lb = lab("affected, family B", 24, TEXT).next_to(rb, RIGHT, buff=0.3)
        self.play(FadeIn(ra), FadeIn(la), run_time=0.4)
        self.at("different ones")
        self.play(FadeIn(rb), FadeIn(lb), run_time=0.4)
        mt = lab("a different mutation in each family", 28, RED).move_to([1.4, -1.6, 0])
        self.play(FadeIn(mt), run_time=0.3)
        self.at("mutant protein")
        mp = lab("and the mutant protein tested", 28, TEAL).move_to([1.4, -2.4, 0])
        self.play(FadeIn(mp), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Lod(SpokenScene):
    """idealised arithmetic: ten informative meioses, LOD 3.01; one recombinant, LOD 1.60."""

    def construct(self):
        ay0, k = -3.0, 1.55
        axx = 2.3
        bx = 3.5
        axis = VGroup(seg([axx, ay0, 0], [axx, ay0 + 3.7 * k, 0], GREY, 3), seg([axx, ay0, 0], [6.3, ay0, 0], GREY, 3))
        ylab = lab("LOD", 28, YELLOW, weight=BOLD).move_to([axx + 0.45, ay0 + 3.7 * k + 0.3, 0])
        ideal = lab("idealised arithmetic, not real data", 24, ORANGE).move_to([-3.5, 3.55, 0])
        eq = VGroup(lab("LOD = base-10 log of", 30, TEXT),
                    lab("probability of data if linked / if unlinked", 28, TEXT)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        eq.move_to([-3.5, 2.5, 0]).align_to([-6.3, 0, 0], LEFT)
        self.play(FadeIn(axis), FadeIn(ylab), FadeIn(ideal), run_time=0.6)
        self.at("likelihood ratio")
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.6)

        self.at("example ten")
        ten = lab("ten fully informative meioses, phase known", 28, TEXT).move_to([-3.5, 1.3, 0]).align_to([-6.3, 0, 0], LEFT)
        boxes = VGroup(*[Square(side_length=0.85).set_stroke(GREY, 3).set_fill(BG, 1)
                         .move_to([-5.7 + 1.05 * (i % 5), 0.3 - 1.05 * (i // 5), 0]) for i in range(10)])
        self.play(FadeIn(ten), FadeIn(boxes), run_time=0.7)

        def bar_to(v):
            h = max(v * k, 0.01)
            return Rectangle(width=1.0, height=h, stroke_width=0, fill_color=YELLOW, fill_opacity=0.85).move_to([bx, ay0 + h / 2, 0])
        bar = bar_to(0.0)
        self.add(bar)

        self.at("fully informative")
        pending = lab("each meiosis: no recombination", 26, BLUE).move_to([-3.5, -2.25, 0]).align_to([-6.3, 0, 0], LEFT)
        self.play(FadeIn(pending), run_time=0.3)
        for i in range(10):
            self.play(boxes[i].animate.set_fill(BLUE, 0.6).set_stroke(BLUE, 3), Transform(bar, bar_to(0.30103 * (i + 1))), run_time=0.17)
        self.at("give a")
        val = M("3.01", 34, YELLOW, weight=BOLD).move_to([bx, ay0 + 3.01 * k + 0.65, 0])
        self.play(FadeIn(val, shift=UP * 0.1), run_time=0.4)

        self.at("Traditionally")
        th = DashedLine([axx, ay0 + 3 * k, 0], [6.3, ay0 + 3 * k, 0], color=GOLD, stroke_width=3)
        thl = VGroup(lab("usual", 22, GOLD), lab("threshold: 3", 22, GOLD)).arrange(DOWN, buff=0.05).move_to([5.3, ay0 + 3 * k - 0.55, 0])
        self.play(Create(th), FadeIn(thl), run_time=0.6)

        self.at("One recombinant")
        self.play(FadeOut(pending), run_time=0.2)
        r_lbl = lab("one recombinant, at recombination fraction 0.1", 24, ORANGE).move_to([-3.5, -2.25, 0]).align_to([-6.3, 0, 0], LEFT)
        self.play(boxes[9].animate.set_fill(ORANGE, 0.7).set_stroke(ORANGE, 3), FadeIn(r_lbl), run_time=0.5)
        val2 = M("1.60", 34, YELLOW, weight=BOLD).move_to([bx, ay0 + 1.60 * k + 0.65, 0])
        self.play(Transform(bar, bar_to(1.60)), ReplacementTransform(val, val2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """LOD 3 is ~20:1, 1 in 20 spurious: replicate. An interval holds many genes: find the mutation in the gene itself."""

    def construct(self):
        div = seg([0, -3.5, 0], [0, 3.5, 0], GREY, 2)
        self.add(div)
        lt = lab("A LOD of 3 is not proof", 30, ORANGE, weight=BOLD).move_to([-3.2, 3.2, 0])
        self.at("not proof")
        self.play(FadeIn(lt), run_time=0.5)
        cells = VGroup(*[Square(side_length=0.78).set_stroke(GREY, 2.5).set_fill(BG, 1)
                         .move_to([-5.4 + 0.98 * (i % 5), 1.35 - 0.98 * (i // 5), 0]) for i in range(20)])
        odds = VGroup(lab("odds about 20 to 1,", 24, TEXT), lab("given most loci are unlinked", 24, TEXT)).arrange(DOWN, buff=0.05).move_to([-3.2, 2.5, 0])
        self.at("means odds")
        self.play(FadeIn(odds), FadeIn(cells), run_time=0.8)
        self.at("spurious")
        self.play(cells[7].animate.set_fill(ORANGE, 0.8).set_stroke(ORANGE, 3), run_time=0.5)
        bl = lab("about 1 in 20 is spurious", 26, ORANGE).move_to([-3.2, -2.45, 0])
        self.play(FadeIn(bl), run_time=0.4)
        self.at("replicate")
        ctl = chip("control: replicate in independent families", TEAL, 22).move_to([-3.2, -3.2, 0])
        self.play(FadeIn(ctl, shift=UP * 0.1), run_time=0.5)

        self.at("linked interval holds")
        rt = lab("An interval holds many genes", 30, ORANGE, weight=BOLD).move_to([3.2, 3.2, 0])
        iv = hbar(0.8, 5.8, 2.5, YELLOW, 0.4, 0.3)
        ivl = lab("loop-tail interval of the mouse", 24, YELLOW).move_to([3.3, 1.95, 0])
        self.play(FadeIn(rt), FadeIn(iv), FadeIn(ivl), run_time=0.7)
        self.at("transcription units")
        g = VGroup(*[gene_box(1.2 + 0.92 * (i % 6), 1.2 - 0.95 * (i // 6), 0.7, 0.62, GREEN, 0.3) for i in range(17)])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in g], lag_ratio=0.1), run_time=1.4)
        n17 = lab("at least 17 transcription units", 26, GREEN).move_to([3.3, -2.2, 0])
        self.play(FadeIn(n17), run_time=0.4)
        self.at("find a mutation")
        ctl2 = chip("control: a mutation in the gene itself", TEAL, 22).move_to([3.3, -3.1, 0])
        pick = g[8]
        self.play(FadeIn(ctl2, shift=UP * 0.1), g.animate.set_opacity(0.3), run_time=0.5)
        self.play(pick.animate.set_opacity(1.0).set_stroke(RED, 4).set_fill(RED, 0.4), run_time=0.5)
        c = pick.get_center()
        mut = seg([c[0] + 0.1, c[1] - 0.25, 0], [c[0] + 0.1, c[1] + 0.25, 0], RED, 7)
        self.play(Create(mut), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Discoveries(SpokenScene):
    """Huntington disease (1983 linkage, 1993 repeat); Tlr4 in the mouse (1998)."""

    def construct(self):
        X0, X1 = -5.9, 5.9
        # ---- Huntington, full frame
        hd = lab("Huntington disease", 34, TEXT, weight=BOLD).move_to([0, 3.3, 0])
        c4 = hbar(X0, X1, 2.3, GREY, 0.5)
        c4l = lab("chromosome 4", 24, GREY).move_to([-4.9, 1.75, 0])
        self.at("Huntington disease gene")
        self.play(FadeIn(hd), FadeIn(c4), FadeIn(c4l), run_time=0.6)
        self.at("a marker on")
        mx = -2.2
        mk = seg([mx, 2.0, 0], [mx, 2.6, 0], BLUE, 7)
        mkl = lab("linked marker", 24, BLUE).move_to([mx, 1.65, 0])
        # timeline
        TL = -1.9
        tline = Arrow(np.array([-5.5, TL, 0]), np.array([5.5, TL, 0]), buff=0, color=GREY, stroke_width=3, tip_length=0.18)
        d83 = Dot(np.array([-4.0, TL, 0]), color=GOLD, radius=0.12)
        t83 = VGroup(lab("1983", 28, GOLD, weight=BOLD), lab("Gusella and colleagues", 22, GOLD), lab("linked to a marker", 22, TEXT)).arrange(DOWN, buff=0.1).move_to([-3.6, TL - 0.9, 0])
        self.play(FadeIn(mk), FadeIn(mkl), Create(tline), FadeIn(d83), FadeIn(t83), run_time=0.8)
        self.at("the collaborative group")
        gx = 2.4
        gb = gene_box(gx, 2.3, 1.6, 0.5, GREEN, 0.4)
        gbl = lab("new gene", 24, GREEN).move_to([gx, 1.75, 0])
        d93 = Dot(np.array([4.0, TL, 0]), color=GOLD, radius=0.12)
        t93 = VGroup(lab("1993", 28, GOLD, weight=BOLD), lab("Collaborative Research Group", 22, GOLD), lab("expanded repeat, new gene", 22, TEXT)).arrange(DOWN, buff=0.1).move_to([3.7, TL - 0.9, 0])
        self.play(FadeIn(gb), FadeIn(gbl), FadeIn(d93), FadeIn(t93), run_time=0.6)
        self.at("expanded")
        rep = VGroup(*[chip("CAG", RED, 26, pad=0.12) for _ in range(9)]).arrange(RIGHT, buff=0.1).move_to([0, 0.7, 0])
        repl = lab("unstable, expanded CAG repeat", 24, RED).move_to([0, 0.1, 0])
        self.play(LaggedStart(*[FadeIn(r) for r in rep], lag_ratio=0.1), FadeIn(repl), run_time=1.0)
        self.at("new gene there")
        n75 = lab("found in all 75 disease families tested", 26, TEXT).move_to([0, -0.5, 0])
        self.play(FadeIn(n75), run_time=0.4)
        self.at("decade separated")
        dec = DoubleArrow([-3.9, TL + 0.35, 0], [3.9, TL + 0.35, 0], buff=0, color=GOLD, stroke_width=3, tip_length=0.15)
        dtx = lab("a decade from map to gene", 24, GOLD).move_to([0, TL + 0.7, 0])
        self.play(Create(dec), FadeIn(dtx), run_time=0.6)

        # ---- mouse, full frame
        self.at("confine the mouse mutation")
        top = VGroup(hd, c4, c4l, mk, mkl, gb, gbl, rep, repl, n75, tline, d83, t83, d93, t93, dec, dtx)
        self.play(FadeOut(top), run_time=0.5)
        mt = lab("Mouse: resistance to LPS", 34, TEXT, weight=BOLD).move_to([-1.6, 3.3, 0])
        mb = hbar(X0, X1, 2.3, GREY, 0.5)
        mbl = lab("mouse chromosome", 24, GREY).move_to([-4.6, 1.75, 0])
        ivx = 1.2
        iv = Rectangle(width=0.55, height=0.8, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.35).move_to([ivx, 2.3, 0])
        ivl = lab("0.9 cM interval, from 2093 meioses", 26, YELLOW).move_to([2.4, 1.6, 0])
        t98 = lab("Beutler's group, 1998", 24, GOLD).move_to([4.3, 3.3, 0])
        self.play(FadeIn(mt), FadeIn(mb), FadeIn(mbl), FadeIn(iv), FadeIn(ivl), FadeIn(t98), run_time=0.8)
        self.at("missense change")
        gt = gene_box(0.0, 0.3, 3.6, 0.9, GREEN, 0.35)
        tl4 = lab("Tlr4", 34, GREEN, weight=BOLD).move_to(gt)
        sp = VGroup(seg([ivx - 0.3, 1.9, 0], [-1.8, 0.75, 0], YELLOW, 2), seg([ivx + 0.3, 1.9, 0], [1.8, 0.75, 0], YELLOW, 2))
        self.play(FadeOut(ivl), Create(sp), FadeIn(gt), FadeIn(tl4), run_time=0.6)
        b1 = hbar(-1.8, 1.8, -0.9, GREY, 0.4, 0.3)
        k1 = seg([-0.6, -1.15, 0], [-0.6, -0.65, 0], RED, 7)
        s1 = lab("C3H/HeJ: missense change", 26, RED).next_to(b1, LEFT, buff=0.4)
        self.play(FadeIn(b1), FadeIn(k1), FadeIn(s1), run_time=0.5)
        self.at("a null")
        b2 = hbar(-1.8, 1.8, -2.0, GREY, 0.4, 0.3)
        k2 = VGroup(seg([-0.2, -2.25, 0], [0.2, -1.75, 0], RED, 7), seg([-0.2, -1.75, 0], [0.2, -2.25, 0], RED, 7))
        s2 = lab("C57BL/10ScCr: null", 26, RED).next_to(b2, LEFT, buff=0.4)
        self.play(FadeIn(b2), FadeIn(k2), FadeIn(s2), run_time=0.5)
        self.at("The method was needed")
        nd = lab("gene known only from its effect", 28, TEXT).move_to([0, -3.1, 0])
        self.play(FadeIn(nd), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
def small_ped(cx, y):
    """A cousin-marriage pedigree reduced to parents (double marriage line) and one affected child."""
    f = Square(side_length=0.7).set_stroke(GREY, 3).set_fill(BG, 1).move_to([cx - 0.8, y, 0])
    m = Circle(radius=0.35).set_stroke(GREY, 3).set_fill(BG, 1).move_to([cx + 0.8, y, 0])
    m1 = seg([cx - 0.45, y + 0.06, 0], [cx + 0.45, y + 0.06, 0], GREY, 3)
    m2 = seg([cx - 0.45, y - 0.06, 0], [cx + 0.45, y - 0.06, 0], GREY, 3)
    d = seg([cx, y, 0], [cx, y - 0.7, 0], GREY, 3)
    c = Square(side_length=0.7).set_stroke(RED, 3).set_fill(RED, 0.85).move_to([cx, y - 1.05, 0])
    return VGroup(f, m, m1, m2, d, c)


class S08Painless(SpokenScene):
    """Cox, Woods 2006: three consanguineous families, chromosome 2, three different nonsense mutations; the rule."""

    def construct(self):
        title = lab("Inability to feel pain", 34, TEXT, weight=BOLD).move_to([0, 3.4, 0])
        xs = [-4.0, 0.0, 4.0]
        peds = VGroup(*[small_ped(x, 2.1) for x in xs])
        fam = VGroup(*[lab(f"family {i + 1}", 24, GREY).move_to([x, 2.75, 0]) for i, x in enumerate(xs)])
        self.at("mapped inability")
        sch = lab("schematic", 22, ORANGE).move_to([5.5, 3.4, 0])
        self.play(FadeIn(title), FadeIn(sch), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(p) for p in peds], lag_ratio=0.2), FadeIn(fam), run_time=1.0)
        self.at("three consanguineous")
        cons = lab("related parents: double line", 24, TEXT).move_to([0, 0.3, 0])
        self.play(FadeIn(cons), run_time=0.4)
        self.at("to chromosome")
        ch = hbar(-5.9, 5.9, -0.7, GREY, 0.5)
        chl = lab("chromosome 2", 24, GREY).move_to([-4.9, -0.15, 0])
        reg = Rectangle(width=1.3, height=0.8, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.3).move_to([0, -0.7, 0])
        regl = lab("2q24.3", 26, YELLOW).move_to([1.6, -0.15, 0])
        ls = VGroup(*[seg([x, 0.8, 0], [0.0, -0.3, 0], GREY, 2) for x in xs])
        self.play(FadeOut(cons), FadeIn(ch), FadeIn(chl), run_time=0.4)
        self.play(FadeIn(reg), FadeIn(regl), run_time=0.5)

        self.at("three different homozygous")
        gene = gene_box(0, -2.0, 4.0, 0.8, GREEN, 0.3)
        gl = lab("SCN9A", 30, GREEN, weight=BOLD).move_to([0, -2.0, 0])
        sp = VGroup(seg([-0.6, -1.1, 0], [-2.0, -1.6, 0], YELLOW, 2), seg([0.6, -1.1, 0], [2.0, -1.6, 0], YELLOW, 2))
        self.play(FadeOut(regl), Create(sp), FadeIn(gene), FadeIn(gl), run_time=0.5)
        ticks = VGroup(*[seg([x, -2.4, 0], [x, -1.6, 0], RED, 7) for x in (-1.5, 1.0, 1.6)])
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.35), run_time=0.9)
        self.at("truncating mutations")
        nl = lab("3 different homozygous truncating mutations", 26, RED).move_to([0, -2.85, 0])
        self.play(FadeIn(nl), run_time=0.4)

        self.at("Mutant channels")
        self.play(FadeOut(VGroup(peds, fam, ch, chl, reg, sp, nl)), VGroup(gene, gl, ticks).animate.shift(UP * 4.0), run_time=0.7)
        hl = lab("HEK293 cells, channel expressed", 28, TEXT).move_to([0, 1.15, 0])
        by = 0.2
        bg = DashedLine([-6.0, by, 0], [6.0, by, 0], color=GREY, stroke_width=3)
        bgl = lab("background", 24, GREY).move_to([5.0, by + 0.3, 0])
        rng = np.random.RandomState(3)
        def flat(x0, x1):
            xx = np.linspace(x0, x1, 40)
            m = VMobject(); m.set_points_as_corners([np.array([x, by + rng.randn() * 0.03, 0]) for x in xx]); m.set_stroke(RED, 4); return m
        xw = np.linspace(-5.8, -3.4, 60)
        yw = by - 2.3 * np.exp(-((xw + 4.7) / 0.3) ** 2) + rng.randn(60) * 0.03
        wt = VMobject(); wt.set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xw, yw)]); wt.set_stroke(YELLOW, 4)
        mts = [flat(-2.4, 5.2)]
        wl = lab("wild type, for comparison (schematic)", 22, YELLOW).move_to([-3.6, -2.9, 0])
        ml = lab("mutant channels: no more than background", 22, RED).move_to([2.9, -2.1, 0])
        self.play(FadeIn(hl), Create(bg), FadeIn(bgl), run_time=0.5)
        self.play(Create(wt), *[Create(m) for m in mts], run_time=0.9)
        self.play(FadeIn(wl), FadeIn(ml), run_time=0.4)

        self.at("Keep this rule")
        self.play(FadeOut(VGroup(sch, title, gene, gl, ticks, hl, bg, bgl, wt, *mts, wl, ml)), run_time=0.5)
        r1 = lab("Linkage finds a region;", 46, TEXT, font=TITLE_FONT)
        r2 = lab("different mutations in unrelated families", 42, GOLD, font=TITLE_FONT)
        r3 = lab("show which gene.", 42, GOLD, font=TITLE_FONT)
        VGroup(r2, r3).arrange(DOWN, buff=0.2).move_to([0, -0.5, 0])
        r1.move_to([0, 0.9, 0])
        fit(r2, max_w=11.8)
        self.at("linkage finds")
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.5)
        self.at("unrelated families")
        self.play(FadeIn(r2, shift=UP * 0.15), FadeIn(r3, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S09End(EndCard):
    LINE = "Linkage finds a region; different mutations in unrelated families show which gene."
