"""A Punnett square predicts the chances  (grade 7 Life Science explainer, predicting-traits)

COLOR MAP (one color per concept, whole film)
  PURPLE = the P allele, purple flowers, purple offspring
  WHITE  = the p allele, white flowers, white offspring
  YELLOW = vocabulary words (allele, genotype, phenotype, ratio, probability, Punnett square)
  BLUE   = the Punnett grid, sex cells, gene copies
  GREEN  = chances and predictions (1 in 4, 50 percent, 3 : 1 line)
  GOLD   = Mendel's counted seeds
  RED    = question marks
  GREY   = structure and neutral labels
  TEXT   = plain labels
"""
from bp_style import *  # noqa: F401,F403

PURPLE = "#B07CFF"
WHITE = "#FFFFFF"


def geno(s, size=44):
    """Allele letters coloured: P purple, p white."""
    return T(s, size, WHITE, weight=BOLD, t2c={"P": PURPLE})


def flower(kind, x, y, r=0.38):
    col = PURPLE if kind == "purple" else WHITE
    return Circle(radius=r, stroke_color=col, stroke_width=4, fill_color=col, fill_opacity=0.9).move_to([x, y, 0])


def plant(kind, x, y, label=None, size=24):
    """A schematic plant: a stem and a flower disc (not to scale)."""
    stem = Line([x, y - 0.65, 0], [x, y + 0.1, 0], color=GREEN if False else GREY, stroke_width=6)
    fl = flower(kind, x, y + 0.45)
    parts = [stem, fl]
    if label:
        parts.append(T(label, size, GREY).move_to([x, y - 0.95, 0]))
    return VGroup(*parts)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22)


def word(text, size=32):
    return T(text, size, YELLOW, weight=BOLD)


def grid_at(cx, cy, s=1.7):
    """2x2 Punnett grid: returns (outline group, cell centres in order TL, TR, BL, BR, col x's, row y's)."""
    cols = [cx - s / 2, cx + s / 2]
    rows = [cy + s / 2, cy - s / 2]
    lines = VGroup(
        Rectangle(width=2 * s, height=2 * s, stroke_color=BLUE, stroke_width=5).move_to([cx, cy, 0]),
        Line([cx, cy + s, 0], [cx, cy - s, 0], color=BLUE, stroke_width=5),
        Line([cx - s, cy, 0], [cx + s, cy, 0], color=BLUE, stroke_width=5),
    )
    cells = [[cols[0], rows[0]], [cols[1], rows[0]], [cols[0], rows[1]], [cols[1], rows[1]]]
    return lines, cells, cols, rows


class S00Title(TitleCard):
    LESSON = "Predicting traits with Punnett squares"
    TITLE = "A Punnett square predicts the chances"


# ----------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        p1 = plant("purple", -3, 1.9, "purple flowers", 24)
        p2 = plant("purple", 3, 1.9, "purple flowers", 24)
        self.at("pea plants")
        self.play(FadeIn(p1, shift=UP * 0.2), FadeIn(p2, shift=UP * 0.2), run_time=1.0)
        g1 = geno("Pp", 34).move_to([-3, 0.4, 0])
        g2 = geno("Pp", 34).move_to([3, 0.4, 0])
        x = T("x", 34, GREY).move_to([0, 1.9, 0])
        self.at("one purple allele")
        self.play(FadeIn(g1, shift=UP * 0.1), FadeIn(g2, shift=UP * 0.1), FadeIn(x), run_time=0.9)
        a1 = arrow([-1.6, 1.0, 0], [-0.6, 0.15, 0])
        a2 = arrow([1.6, 1.0, 0], [0.6, 0.15, 0])
        kids = VGroup(*[plant("purple" if i < 3 else "white", xx, -1.0, None) for i, xx in enumerate([-3.6, -1.2, 1.2, 3.6])])
        klab = T("offspring: predicted chances, not a drawn sample", 24, GREY).move_to([0, -2.2, 0])
        self.at("offspring")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(kids, lag_ratio=0.25), FadeIn(klab), run_time=1.6)
        pred = T("chances: about 3 purple : 1 white", 30, GREEN, weight=BOLD).move_to([0, -2.75, 0])
        self.at("bloom purple")
        self.play(FadeIn(pred, shift=UP * 0.1), run_time=0.8)
        ring = Circle(radius=0.62, stroke_color=YELLOW, stroke_width=5).move_to([3.6, -0.55, 0])
        self.at("bloom white")
        self.play(FadeIn(ring), run_time=0.5)
        q = T("?", 34, RED, weight=BOLD).move_to([3.6, -0.55, 0])
        w = T("Where was the white hiding?", 38, YELLOW).move_to([0, -3.3, 0])
        self.at("hiding")
        self.play(FadeIn(q, scale=1.3), FadeIn(w, shift=UP * 0.1), run_time=0.8)
        w2 = T("Could we predict it first?", 38, YELLOW).move_to([0, -3.3, 0])
        self.at("single seed")
        self.play(FadeOut(w, shift=UP * 0.1), FadeIn(w2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Alleles(SpokenScene):
    def construct(self):
        cx, cy = -3.6, 0.5
        cell = Ellipse(width=4.8, height=3.2, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])
        cl = T("body cell of a pea plant", 26, GREY).move_to([cx, cy + 2.05, 0])
        self.at("body cell")
        self.play(FadeIn(cell, scale=0.9), FadeIn(cl), run_time=0.9)
        g1 = RoundedRectangle(corner_radius=0.15, width=0.7, height=1.5, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3).move_to([cx - 0.9, cy, 0])
        g2 = g1.copy().move_to([cx + 0.9, cy, 0])
        gl = T("two copies of the flower-color gene", 24, BLUE).move_to([cx, cy - 2.05, 0])
        self.at("two copies")
        self.play(FadeIn(g1, scale=0.8), FadeIn(g2, scale=0.8), FadeIn(gl), run_time=1.0)
        al = word("allele = one version of a gene", 26).move_to([cx, cy - 2.7, 0])
        self.at("one version")
        self.play(FadeIn(al, shift=UP * 0.1), run_time=0.7)
        bp = RoundedRectangle(corner_radius=0.15, width=0.7, height=1.5, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.85).move_to(g1)
        bw = RoundedRectangle(corner_radius=0.15, width=0.7, height=1.5, stroke_color=WHITE, stroke_width=3, fill_color=WHITE, fill_opacity=0.9).move_to(g2)
        lp = T("P", 40, BG, weight=BOLD).move_to(bp)
        lw = T("p", 40, BG, weight=BOLD).move_to(bw)
        self.at("purple allele")
        self.play(Transform(g1, bp), run_time=0.7)
        self.at("white allele")
        self.play(Transform(g2, bw), run_time=0.7)
        self.at("capital")
        self.play(FadeIn(lp, scale=0.7), run_time=0.6)
        self.at("small")
        self.play(FadeIn(lw, scale=0.7), run_time=0.6)
        dom = VGroup(T("dominant", 30, YELLOW, weight=BOLD), T("shows with only one copy", 26)).arrange(DOWN, buff=0.1).move_to([3.5, 1.7, 0])
        self.at("dominant allele")
        self.play(FadeIn(dom, shift=LEFT * 0.2), run_time=0.8)
        rec = VGroup(T("recessive", 30, YELLOW, weight=BOLD), T("shows only with both copies", 26)).arrange(DOWN, buff=0.1).move_to([3.5, 0.1, 0])
        self.at("recessive allele")
        self.play(FadeIn(rec, shift=LEFT * 0.2), run_time=0.8)
        hid = T("p is hidden, not destroyed", 30, YELLOW).move_to([3.5, -1.7, 0])
        self.at("hidden")
        self.play(FadeIn(hid, shift=UP * 0.1), Indicate(VGroup(g2, lw), color=YELLOW, scale_factor=1.2), run_time=1.1)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Genotype(SpokenScene):
    def construct(self):
        ys = [2.0, 1.0, 0.0]
        gh = word("genotype", 32).move_to([-3.6, 3.0, 0])
        rows = []
        self.at("pair of alleles")
        self.play(FadeIn(gh, shift=DOWN * 0.1), run_time=0.6)
        gl = []
        for s, y in zip(["PP", "Pp", "pp"], ys):
            g = geno(s, 44).move_to([-3.6, y, 0])
            gl.append(g)
        self.play(FadeIn(VGroup(*gl), lag_ratio=0.3), run_time=0.9)
        ph = word("phenotype", 32).move_to([1.4, 3.0, 0])
        self.at("trait that shows")
        self.play(FadeIn(ph, shift=DOWN * 0.1), run_time=0.6)
        fl, wl = [], []
        for k, y in zip(["purple", "purple", "white"], ys):
            f = flower(k, 0.3, y)
            t = T(k, 30, PURPLE if k == "purple" else WHITE).next_to(f, RIGHT, buff=0.3)
            fl.append(f)
            wl.append(t)
        self.play(FadeIn(VGroup(*fl, *wl), lag_ratio=0.2), run_time=1.0)
        self.at("two purple alleles")
        self.play(Indicate(VGroup(gl[0], fl[0]), color=PURPLE, scale_factor=1.1), run_time=0.8)
        self.at("one of each")
        self.play(Indicate(VGroup(gl[1], fl[1]), color=PURPLE, scale_factor=1.1), run_time=0.8)
        self.at("white alleles")
        self.play(Indicate(VGroup(gl[2], fl[2]), color=WHITE, scale_factor=1.12), run_time=0.9)
        sc = word("sex cells", 30).move_to([1.8, -0.95, 0])
        self.at("sex cell")
        self.play(FadeIn(sc, shift=UP * 0.1), run_time=0.6)
        src = VGroup(geno("Pp", 44), T("plant", 26, GREY)).arrange(RIGHT, buff=0.25).move_to([-3.6, -2.3, 0])
        c1 = chip("P", PURPLE, 36).move_to([1.8, -1.85, 0])
        c2 = chip("p", WHITE, 36).move_to([1.8, -2.8, 0])
        self.play(FadeIn(src), run_time=0.5)
        self.at("passes on")
        self.play(GrowArrow(arrow([-2.2, -2.2, 0], [1.1, -1.85, 0], BLUE)), GrowArrow(arrow([-2.2, -2.4, 0], [1.1, -2.8, 0], BLUE)),
                  FadeIn(c1), FadeIn(c2), run_time=1.0)
        p1 = T("50 percent", 30, GREEN, weight=BOLD).move_to([4.4, -1.85, 0])
        p2 = T("50 percent", 30, GREEN, weight=BOLD).move_to([4.4, -2.8, 0])
        self.at("chance each")
        self.play(FadeIn(p1, shift=LEFT * 0.1), FadeIn(p2, shift=LEFT * 0.1), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S04Square(SpokenScene):
    def construct(self):
        cx, cy, s = 0.0, -0.6, 1.9
        lines, cells, cols, rows = grid_at(cx, cy, s)
        title = word("Punnett square", 40).move_to([0, 3.05, 0])
        self.at("Punnett square")
        self.play(FadeIn(title, shift=DOWN * 0.1), Create(lines), run_time=1.4)
        self.at("can join")
        self.play(Indicate(lines, color=BLUE, scale_factor=1.03), run_time=1.0)
        top = [geno("P", 44).move_to([cols[0], cy + s + 0.55, 0]), geno("p", 44).move_to([cols[1], cy + s + 0.55, 0])]
        tl = T("one parent's sex cells", 26, BLUE).move_to([0, cy + s + 1.25, 0])
        self.at("across the top")
        self.play(FadeIn(top[0]), FadeIn(top[1]), FadeIn(tl), run_time=0.9)
        side = [geno("P", 44).move_to([cx - s - 0.55, rows[0], 0]), geno("p", 44).move_to([cx - s - 0.55, rows[1], 0])]
        sl = T("the other parent's\nsex cells", 26, BLUE, line_spacing=0.85).move_to([-5.0, cy, 0])
        self.at("down the side")
        self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(sl), run_time=0.9)
        texts = []
        for (a, b), c in zip([("P", "P"), ("P", "p"), ("P", "p"), ("p", "p")], cells):
            texts.append(geno(a + b, 44).move_to([c[0], c[1], 0]))
        self.at("fill each box")
        self.play(FadeIn(VGroup(*texts), lag_ratio=0.4), run_time=2.0)
        bx = VGroup(T("each box:", 30, TEXT), T("1 in 4 chance", 36, GREEN, weight=BOLD)).arrange(DOWN, buff=0.15).move_to([4.7, cy, 0])
        self.at("chance")
        self.play(FadeIn(bx, shift=LEFT * 0.2), run_time=0.8)
        for i, c in enumerate(cells):
            self.play(Indicate(texts[i], color=GREEN, scale_factor=1.2), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S05Read(SpokenScene):
    def construct(self):
        cx, cy, s = -3.3, -0.5, 1.9
        lines, cells, cols, rows = grid_at(cx, cy, s)
        top = VGroup(geno("P", 44).move_to([cols[0], cy + s + 0.55, 0]), geno("p", 44).move_to([cols[1], cy + s + 0.55, 0]))
        side = VGroup(geno("P", 44).move_to([cx - s - 0.55, rows[0], 0]), geno("p", 44).move_to([cx - s - 0.55, rows[1], 0]))
        texts = [geno(a + b, 44).move_to([c[0], c[1], 0]) for (a, b), c in zip([("P", "P"), ("P", "p"), ("P", "p"), ("p", "p")], cells)]
        title = word("Punnett square", 34).move_to([cx, 3.05, 0])
        self.add(lines, top, side, *texts, title)
        shades = []
        for i, c in enumerate(cells):
            col = WHITE if i == 3 else PURPLE
            shades.append(Square(side_length=s - 0.1, stroke_width=0, fill_color=col, fill_opacity=0.28 if i < 3 else 0.35).move_to([c[0], c[1], 0]))
        self.at("boxes")
        self.at("two purple alleles")
        self.play(FadeIn(shades[0]), run_time=0.6)
        self.at("one of each")
        self.play(FadeIn(shades[1]), FadeIn(shades[2]), run_time=0.7)
        self.at("two white alleles")
        self.play(FadeIn(shades[3]), run_time=0.6)
        # counts as labels
        ratio_w = word("ratio", 32).move_to([3.6, 2.7, 0])
        ratio_d = T("compares two numbers", 26).next_to(ratio_w, RIGHT, buff=0.2)
        rg = VGroup(ratio_w, ratio_d).move_to([3.6, 2.7, 0])
        self.at("ratio compares")
        self.play(FadeIn(rg, shift=LEFT * 0.2), run_time=0.8)
        r31 = VGroup(T("3 purple", 40, PURPLE, weight=BOLD), T(":", 40), T("1 white", 40, WHITE, weight=BOLD)).arrange(RIGHT, buff=0.25).move_to([3.6, 1.5, 0])
        self.at("purple to")
        self.play(FadeIn(r31, shift=UP * 0.1), run_time=0.9)
        pw = word("probability", 32)
        pd = T("the chance something\nwill happen", 26, line_spacing=0.85)
        pg = VGroup(pw, pd).arrange(DOWN, buff=0.12).move_to([3.6, 0.0, 0])
        self.at("probability is")
        self.play(FadeIn(pg, shift=LEFT * 0.2), run_time=0.8)
        ring_t = Rectangle(width=0.7, height=0.8, stroke_color=YELLOW, stroke_width=4).move_to(top[1])
        ring_s = Rectangle(width=0.7, height=0.8, stroke_color=YELLOW, stroke_width=4).move_to(side[1])
        ring_c = Square(side_length=s - 0.05, stroke_color=YELLOW, stroke_width=6).move_to([cells[3][0], cells[3][1], 0])
        self.at("white needs")
        self.play(Create(ring_t), Create(ring_s), run_time=0.8)
        self.at("pass on")
        self.play(Create(ring_c), run_time=0.7)
        ans = T("1 in 4 = 25 percent", 40, GREEN, weight=BOLD).move_to([3.6, -1.7, 0])
        self.at("that chance")
        self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S06Counts(SpokenScene):
    def construct(self):
        self.at("the square")
        note = T("A Punnett square gives chances,\nnot exact counts", 38, GREEN, weight=BOLD, line_spacing=0.9).move_to([0, 1.6, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=1.0)
        kids = VGroup(*[plant("purple", x, -0.9) for x in [-4.5, -1.5, 1.5, 4.5]])
        lab = T("4 offspring from two Pp parents", 28, GREY).move_to([0, -2.4, 0])
        self.at("four seeds")
        self.play(FadeOut(note), FadeIn(kids, lag_ratio=0.25), FadeIn(lab), run_time=1.3)
        ch = T("all purple: about 32 percent chance", 38, GREEN, weight=BOLD).move_to([0, 1.5, 0])
        self.at("chance of that")
        self.play(FadeIn(ch, shift=DOWN * 0.1), run_time=0.8)
        self.at("counted thousands")
        self.play(FadeOut(VGroup(kids, lab, ch)), run_time=0.4)
        # Mendel's seed-shape counts (lesson table): round 5,474, wrinkled 1,850
        base = -2.0
        H = 4.0
        h1, h2 = H, H * 1850 / 5474
        b1 = Rectangle(width=1.6, height=h1, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.5).move_to([-4.6, base + h1 / 2, 0])
        b2 = Rectangle(width=1.6, height=h2, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.5).move_to([-2.2, base + h2 / 2, 0])
        axis = Line([-6.0, base, 0], [-0.8, base, 0], color=GREY, stroke_width=3)
        n1 = M("5,474", 28, GOLD).next_to(b1, UP, buff=0.12)
        n2 = M("1,850", 28, GOLD).next_to(b2, UP, buff=0.12)
        l1 = T("round seeds", 24).next_to(axis, DOWN, buff=0.15).set_x(-4.6)
        l2 = T("wrinkled seeds", 24).next_to(axis, DOWN, buff=0.15).set_x(-2.2)
        ttl = T("Mendel's pea seeds, seed shape", 28, GOLD, weight=BOLD).move_to([-3.4, 3.3, 0])
        sub = T("from self-fertilized hybrid plants", 22, GOLD).move_to([-3.4, 2.85, 0])
        self.play(FadeIn(ttl), FadeIn(sub), Create(axis), run_time=0.4)
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.3)
        got = VGroup(T("counted:", 28, GOLD), M("about 2.96 : 1", 34, GOLD, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([3.4, 1.7, 0])
        self.at("seed shape counts")
        self.play(FadeIn(got, shift=LEFT * 0.2), run_time=0.8)
        pl = DashedLine([-3.2, base + H / 3, 0], [-1.2, base + H / 3, 0], color=GREEN, stroke_width=5, dash_length=0.15)
        pred = VGroup(T("predicted:", 28, GREEN), M("3 : 1", 34, GREEN, weight=BOLD)).arrange(DOWN, buff=0.1).move_to([3.4, 0.2, 0])
        self.at("close to")
        self.play(Create(pl), FadeIn(pred, shift=LEFT * 0.2), run_time=1.0)
        fin = T("Predict the chances.\nCounts land near them.", 34, YELLOW, line_spacing=0.9).move_to([3.4, -1.9, 0])
        self.at("so we can predict")
        self.play(FadeIn(fin, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "Punnett squares predict chances; real counts land near them."
