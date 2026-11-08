"""Gene cloning: one gene out of thousands  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  PURPLE = the plasmid vector (rings)
  YELLOW = the wanted gene / insert / its clone
  GREY   = every other gene, insert, cell, plate, structure, de-emphasised text
  ORANGE = enzymes and the cut (EcoRI, ligase, cut marks, cloning site)
  TEAL   = messenger RNA
  GREEN  = resistant and surviving cells, the labeled probe, a positive spot
  BLUE   = a blue colony (intact lacZ-alpha); a white colony is drawn white
  RED    = the pitfall, a killed cell, the wrong or short insert
  GOLD   = dates and the closing rule
DNA is drawn only as plain bars (two lanes where strands matter) and rings; never as a helix.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
COLB = "#5A7DFF"       # blue colony
WHITE = "#F4F6FA"      # white colony


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    return Arrow(np.array([a[0], a[1], 0.0]), np.array([b[0], b[1], 0.0]), buff=0.0, color=color, stroke_width=w,
                 tip_length=tip, max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bar(x0, x1, y, color=GREY, h=0.3, op=0.9):
    return Rectangle(width=x1 - x0, height=h, stroke_width=0, fill_color=color, fill_opacity=op).move_to(
        [(x0 + x1) / 2, y, 0])


def lanes(top, bot, y, color, lh=0.3):
    """Two lanes (strands) as plain bars: top=(x0,x1), bot=(x0,x1)."""
    return VGroup(bar(top[0], top[1], y + lh / 2, color, lh), bar(bot[0], bot[1], y - lh / 2, color, lh))


def ring(cx, cy, R, color=PURPLE, w=10, gap=0.0):
    if gap <= 0:
        return Circle(radius=R, stroke_color=color, stroke_width=w).move_to([cx, cy, 0])
    return Arc(radius=R, start_angle=PI / 2 + gap, angle=TAU - 2 * gap, arc_center=np.array([cx, cy, 0.0]),
               stroke_color=color, stroke_width=w)


def insert_arc(cx, cy, R, color=YELLOW, w=10, span=0.3, at=PI / 2):
    return Arc(radius=R, start_angle=at - span, angle=2 * span, arc_center=np.array([cx, cy, 0.0]),
               stroke_color=color, stroke_width=w)


def mini_plasmid(cx, cy, R=0.36, ins=GREY, w=6, span=0.55):
    return VGroup(ring(cx, cy, R, PURPLE, w), insert_arc(cx, cy, R, ins, w + 3, max(span, 0.8)))


def plate(cx, cy, R, n, seed, minsep=0.62, rmax=0.8):
    """Colony centres inside a dish of radius R (idealised positions)."""
    rng = np.random.RandomState(seed)
    pts = []
    tries = 0
    while len(pts) < n and tries < 5000:
        tries += 1
        a = rng.rand() * TAU
        r = (rng.rand() ** 0.5) * (R - 0.4)
        p = np.array([cx + r * np.cos(a), cy + r * np.sin(a)])
        if all(np.hypot(*(p - q)) > minsep for q in pts):
            pts.append(p)
    dish = Circle(radius=R, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.07).move_to([cx, cy, 0])
    return dish, pts


def colony(p, color=GREY, r=0.2, op=0.9):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=op).move_to([p[0], p[1], 0])


def clear(sc, t=0.5):
    if sc.mobjects:
        sc.play(*[FadeOut(m) for m in sc.mobjects], run_time=t)


def cell(cx, cy, w=1.6, h=1.1, color=GREY):
    return RoundedRectangle(corner_radius=0.35, width=w, height=h, stroke_color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.12).move_to([cx, cy, 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "One Gene Out of Thousands"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """a genome with one tiny gene; a mixture of thousands with a question mark; pull out, grow pure, read."""

    def construct(self):
        # genome bar, big
        genome = bar(-6.2, 6.2, 0.4, GREY, h=2.0, op=0.45)
        gene = bar(1.9, 2.2, 0.4, YELLOW, h=2.0, op=1.0)
        g_lbl = lab("a genome", 34, GREY).move_to([-3.4, 2.0, 0])
        gene_lbl = lab("one gene", 34, YELLOW).move_to([3.6, 2.5, 0])
        gl = Line([2.95, 2.3, 0], [2.1, 1.55, 0], color=YELLOW, stroke_width=3)
        self.at("A single gene")
        self.play(FadeIn(genome), FadeIn(g_lbl), run_time=0.5)
        self.play(FadeIn(gene), FadeIn(gene_lbl), Create(gl), run_time=0.6)

        self.at("Before cloning")
        too = lab("too little to cut, sequence or study", 36, RED).move_to([0, -1.5, 0])
        self.play(FadeIn(too, shift=UP * 0.15), run_time=0.6)

        # mixture of thousands
        self.at("So how do you pull")
        rng = np.random.RandomState(4)
        bars = VGroup()
        wanted = None
        cols, rows = 11, 7
        for r in range(rows):
            for c in range(cols):
                x = -5.8 + c * 1.16 + 0.55
                y = 3.0 - r * 0.72
                w = 0.45 + rng.rand() * 0.45
                b = bar(x - w / 2, x + w / 2, y, GREY, h=0.2, op=0.75)
                if (r, c) == (3, 7):
                    b = bar(x - 0.35, x + 0.35, y, YELLOW, h=0.24, op=1.0)
                    wanted = b
                bars.add(b)
        self.play(FadeOut(VGroup(genome, gene, g_lbl, gene_lbl, gl, too)), FadeIn(bars, lag_ratio=0.01), run_time=0.6)
        q = T("?", 56, YELLOW, weight=BOLD).next_to(wanted, UP, buff=0.12)
        mix = lab("a mixture of thousands", 30, GREY).move_to([0, -2.0, 0])
        self.play(FadeIn(q), FadeIn(mix), Indicate(wanted, color=YELLOW, scale_factor=1.6), run_time=0.6)

        self.at("pull one chosen gene")
        c1 = chip("pull it out", YELLOW, 30).move_to([-4.4, -3.05, 0])
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.4)
        self.at("grow it as a pure clone")
        c2 = chip("grow a pure clone", YELLOW, 30).move_to([0.0, -3.0, 0])
        a1 = arr(c1.get_right() + [0.1, 0, 0], c2.get_left() + [-0.1, 0, 0], GREY, 4, 0.18)
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.15), run_time=0.5)
        self.at("and read it")
        c3 = chip("read it", YELLOW, 30).move_to([4.2, -3.0, 0])
        a2 = arr(c2.get_right() + [0.1, 0, 0], c3.get_left() + [-0.1, 0, 0], GREY, 4, 0.18)
        self.play(GrowArrow(a2), FadeIn(c3, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02CutJoin(SpokenScene):
    """EcoRI cuts GAATTC leaving staggered ends; the ends of plasmid and insert fit; ligase seals; a cell must copy."""

    def construct(self):
        y = -0.1
        lh = 0.75
        c1, c2 = -0.3, 0.3              # top-strand and bottom-strand cut positions (staggered)
        whole = lanes((-6.0, 6.0), (-6.0, 6.0), y, GREY, lh)
        site = DashedVMobject(Rectangle(width=1.9, height=2 * lh + 0.4, stroke_color=ORANGE, stroke_width=3).move_to([0, y, 0]))
        site_t = M("GAATTC", 44, TEXT).move_to([0, y + 1.3, 0])
        dna_t = lab("DNA", 28, GREY).move_to([-5.6, y + 1.3, 0])

        self.at("Restriction enzymes")
        self.play(FadeIn(whole), FadeIn(dna_t), run_time=0.6)
        self.at("defined sequences")
        self.play(Create(site), FadeIn(site_t), run_time=0.7)

        self.at("cuts")
        enz = chip("EcoRI", ORANGE, 40).move_to([0, 3.1, 0])
        self.play(FadeIn(enz, shift=DOWN * 0.2), run_time=0.3)
        self.at("leaving")
        cut_top = Line([c1, y + 0.03, 0], [c1, y + lh + 0.25, 0], color=ORANGE, stroke_width=7)
        cut_bot = Line([c2, y - 0.03, 0], [c2, y - lh - 0.25, 0], color=ORANGE, stroke_width=7)
        self.play(enz.animate.move_to([0, y + 2.3, 0]), FadeOut(site_t), run_time=0.3)
        self.play(Create(cut_top), Create(cut_bot), run_time=0.3)
        left = lanes((-6.0, c1), (-6.0, c2), y, GREY, lh)
        right = lanes((c1, 6.0), (c2, 6.0), y, GREY, lh)
        self.remove(whole)
        self.add(left, right)
        self.play(left.animate.shift(LEFT * 0.7), right.animate.shift(RIGHT * 0.7), FadeOut(cut_top), FadeOut(cut_bot),
                  FadeOut(site), run_time=0.6)

        self.at("overhangs")
        ov_l = arr([-1.35, y - 1.5, 0], [-0.95, y - 0.55, 0], ORANGE, 4, 0.16)
        ov_r = arr([1.35, y + 1.45, 0], [0.95, y + 0.5, 0], ORANGE, 4, 0.16)
        # arrows point at the overhangs: bottom lane of left piece, top lane of right piece
        ov_l = arr([-1.7, y - 1.7, 0], [-0.7, y - lh - 0.05, 0], ORANGE, 5, 0.18)
        ov_r = arr([1.7, y + 1.7, 0], [0.7, y + lh + 0.05, 0], ORANGE, 5, 0.18)
        ov_t = lab("single-stranded overhangs", 34, ORANGE).move_to([-3.6, y - 2.05, 0])
        self.play(GrowArrow(ov_l), GrowArrow(ov_r), FadeIn(ov_t), run_time=0.7)

        self.at("any other")
        yel = lanes((c1 + 0.7, 6.0), (c2 + 0.7, 6.0), y, YELLOW, lh).shift(RIGHT * 3.0)
        pair_t = lab("pairs with any other EcoRI end", 34, YELLOW).move_to([0, y - 1.9, 0])
        self.play(FadeOut(ov_r), FadeOut(ov_t), FadeOut(enz), right.animate.shift(RIGHT * 3.0).set_opacity(0),
                  FadeIn(yel, shift=LEFT * 0.0), run_time=0.5)
        self.play(yel.animate.shift(LEFT * 3.0), run_time=0.7)
        self.play(left.animate.shift(RIGHT * 0.7), yel.animate.shift(LEFT * 0.7), FadeIn(pair_t), FadeOut(ov_l),
                  run_time=0.6)

        # plasmid and insert
        self.at("So cut plasmid")
        clear(self, 0.4)
        cx, cy, R, g = -3.3, -0.2, 2.35, 0.2
        pl = ring(cx, cy, R, PURPLE, 14, gap=g)
        pl_t = lab("cut plasmid", 30, PURPLE).move_to([cx, cy, 0])
        gx = R * np.sin(g)
        cuts = VGroup(*[Line([cx + s * gx, cy + R * np.cos(g) + 0.4, 0], [cx + s * gx, cy + R * np.cos(g) - 0.4, 0],
                             color=ORANGE, stroke_width=6) for s in (-1, 1)])
        ins = bar(2.0, 5.2, 0.9, YELLOW, h=0.42, op=1.0)
        ins_cuts = VGroup(*[Line([x, 0.9 + 0.55, 0], [x, 0.9 - 0.55, 0], color=ORANGE, stroke_width=6) for x in (2.0, 5.2)])
        ins_t = lab("cut insert", 30, YELLOW).move_to([3.6, -0.1, 0])
        self.play(Create(pl), FadeIn(pl_t), Create(cuts), run_time=0.5)
        self.play(FadeIn(ins), Create(ins_cuts), FadeIn(ins_t), run_time=0.5)
        self.at("fit together")
        self.play(FadeOut(ins_cuts), FadeOut(ins_t), FadeOut(cuts), FadeOut(pl_t), run_time=0.3)
        tgt = ins.copy().stretch_to_fit_width(2 * gx).move_to([cx, cy + R * np.cos(g) - 0.01, 0])
        self.play(Transform(ins, tgt), run_time=0.8)

        self.at("ligase")
        lig = chip("DNA ligase", ORANGE, 32).move_to([cx, cy + R + 0.85, 0])
        self.play(FadeIn(lig, shift=DOWN * 0.15), run_time=0.4)
        seal = VGroup(*[Dot([cx + s * gx, cy + R * np.cos(g), 0], radius=0.11, color=ORANGE) for s in (-1, 1)])
        self.play(FadeIn(seal), Flash(seal[0], color=ORANGE, flash_radius=0.4), Flash(seal[1], color=ORANGE, flash_radius=0.4),
                  run_time=0.7)
        joined = VGroup(lab("joined:", 28, TEXT), lab("one recombinant", 28, TEXT), lab("plasmid", 28, TEXT)).arrange(DOWN, buff=0.1).move_to([cx, cy, 0])
        self.play(FadeIn(joined), FadeOut(lig), FadeOut(seal), run_time=0.5)

        self.at("living cell")
        cl = cell(3.6, 0.1, w=4.4, h=3.2, color=GREY)
        cl_t = lab("a living cell", 30, GREY).move_to([3.6, 1.2, 0])
        a = arr([-0.6, 0.0, 0], [1.3, 0.1, 0], GREY, 5, 0.22)
        qq = T("copies?", 40, YELLOW, weight=BOLD).move_to([3.6, -0.3, 0])
        self.play(Create(cl), FadeIn(cl_t), GrowArrow(a), FadeIn(qq), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Transform(SpokenScene):
    """vector parts; competent bacteria take it up (a fraction); antibiotic keeps those cells; blue-white colonies."""

    def construct(self):
        cx, cy, R = 0.0, -0.1, 1.9
        pl = ring(cx, cy, R, PURPLE, 14)
        # parts: origin (grey dot), marker (green arc), cloning site (orange tick)
        a_org = np.deg2rad(200)
        org = Dot([cx + R * np.cos(a_org), cy + R * np.sin(a_org), 0], radius=0.2, color=GREY)
        mk = Arc(radius=R, start_angle=np.deg2rad(-70), angle=np.deg2rad(70), arc_center=np.array([cx, cy, 0.0]),
                 stroke_color=GREEN, stroke_width=18)
        site = Line([cx, cy + R + 0.3, 0], [cx, cy + R - 0.3, 0], color=ORANGE, stroke_width=8)
        t_org = lab("origin of replication", 28, GREY).move_to([-5.0, 0.9, 0])
        l_org = Line(org.get_center() + [-0.25, 0.05, 0], [-3.3, 0.7, 0], color=GREY, stroke_width=2)
        t_mk = lab("selectable marker: ampicillin resistance", 28, GREEN).move_to([3.05, -2.45, 0])
        l_mk = Line([cx + R * np.cos(np.deg2rad(-35)) + 0.2, cy + R * np.sin(np.deg2rad(-35)) - 0.1, 0], [3.0, -2.1, 0],
                    color=GREEN, stroke_width=2)
        t_site = lab("cloning site", 28, ORANGE).move_to([0, 3.1, 0])
        self.at("A plasmid vector")
        self.play(Create(pl), run_time=0.6)
        self.at("origin of replication")
        self.play(FadeIn(org), FadeIn(t_org), Create(l_org), run_time=0.5)
        self.at("selectable marker")
        self.play(Create(mk), FadeIn(t_mk), Create(l_mk), run_time=0.6)
        self.at("cloning site")
        self.play(Create(site), FadeIn(t_site), run_time=0.5)

        # bacteria take it up
        self.at("Cold calcium chloride")
        clear(self, 0.5)
        xs = [-5.2 + 2.08 * i for i in range(6)]
        cells = VGroup(*[cell(x, -0.6, 1.7, 1.5) for x in xs])
        cc = chip("cold calcium chloride", ORANGE, 28).move_to([-3.2, 3.1, 0])
        comp = lab("competent bacteria", 30, GREY).move_to([3.0, 3.1, 0])
        pls = VGroup(*[mini_plasmid(x, 1.55, 0.36, YELLOW, 6, 0.55) for x in xs])
        self.play(FadeIn(cells, lag_ratio=0.1), FadeIn(cc, shift=DOWN * 0.15), FadeIn(comp), run_time=1.0)
        self.play(FadeIn(pls, lag_ratio=0.1), run_time=0.7)
        self.at("take up the plasmid")
        take = [1, 4]
        self.play(*[pls[i].animate.move_to([xs[i], -0.6, 0]) for i in take], run_time=0.9)
        self.at("only a fraction")
        frac = lab("only a fraction take it up", 30, TEXT).move_to([0, -2.0, 0])
        self.play(FadeOut(VGroup(*[pls[i] for i in range(6) if i not in take])), FadeIn(frac), run_time=0.6)

        # antibiotic
        self.at("Antibiotic leaves")
        ab = chip("antibiotic", RED, 30).move_to([0, 3.1, 0])
        self.play(FadeOut(cc), FadeOut(comp), FadeOut(frac), FadeIn(ab, shift=DOWN * 0.15), run_time=0.4)
        dead = [i for i in range(6) if i not in take]
        crosses = VGroup(*[T("✕", 44, RED, weight=BOLD).move_to([xs[i], -0.6, 0]) for i in dead])
        self.play(*[cells[i].animate.set_opacity(0.18) for i in dead], FadeIn(crosses), run_time=0.7)
        self.play(*[cells[i].animate.set_stroke(GREEN, 5) for i in take], run_time=0.4)
        keep_t = lab("cells that carry the plasmid survive", 30, GREEN).move_to([0, -2.0, 0])
        self.play(FadeIn(keep_t), run_time=0.4)

        # plate
        self.at("In a blue white screen")
        clear(self, 0.5)
        px, py, PR = -3.4, -0.1, 3.0
        dish, pts = plate(px, py, PR, 16, 7, 0.78)
        cols = [COLB, WHITE, COLB, COLB, WHITE, COLB, COLB, COLB, WHITE, COLB, WHITE, COLB, COLB, WHITE, COLB, COLB]
        cols[4], cols[8], cols[10], cols[13] = WHITE, WHITE, WHITE, WHITE
        cols = [COLB if i not in (1, 4, 8, 10, 13) else WHITE for i in range(16)]
        dots = VGroup(*[colony(p, GREY, 0.3, 0.8) for p in pts])
        ex = lab("example, idealised", 22, GREY).move_to([px, py - PR - 0.3, 0])
        self.play(FadeIn(dish), FadeIn(dots, lag_ratio=0.05), FadeIn(ex), run_time=0.8)
        # lacZ-alpha diagrams: the plasmid's piece pairs with the host's partner fragment to make the enzyme
        dx0, dx1 = 0.7, 6.2
        zl = lab("lac Z alpha", 28, TEXT).move_to([2.1, 3.0, 0])
        a_piece = bar(dx0, 3.5, 2.0, PURPLE, h=0.8, op=0.9)
        a_site = Line([2.1, 2.55, 0], [2.1, 1.45, 0], color=ORANGE, stroke_width=6)
        site_t = lab("cloning site", 26, ORANGE).move_to([2.1, 1.0, 0])
        host = bar(4.3, 6.2, 2.0, GREY, h=0.8, op=0.7)
        host_t = lab("host's partner fragment", 24, GREY).move_to([5.0, 3.0, 0])
        self.play(FadeIn(zl), FadeIn(a_piece), Create(a_site), FadeIn(site_t), FadeIn(host), FadeIn(host_t), run_time=0.7)
        self.at("helps make")
        t_blue = VGroup(lab("together: an enzyme", 28, COLB), lab("X-gal turns blue", 28, COLB)).arrange(DOWN, buff=0.08).move_to([3.45, 0.55, 0])
        self.play(FadeOut(site_t), FadeOut(host_t), host.animate.move_to([4.55, 2.0, 0]),
                  a_piece.animate.set_fill(COLB, 1.0), run_time=0.7)
        self.play(host.animate.set_fill(COLB, 1.0), FadeIn(t_blue), run_time=0.4)
        self.play(*[dots[i].animate.set_fill(COLB, 1.0) for i in range(16) if cols[i] == COLB], run_time=0.8)
        self.at("An insert breaks it")
        b1 = bar(dx0, 1.6, -1.0, PURPLE, h=0.8, op=0.9)
        bi = bar(1.6, 2.6, -1.0, YELLOW, h=0.8, op=1.0)
        b2 = bar(2.6, 3.5, -1.0, PURPLE, h=0.8, op=0.9)
        bh = bar(4.3, 6.2, -1.0, GREY, h=0.8, op=0.7)
        nox = T("✕", 40, RED, weight=BOLD).move_to([3.9, -1.0, 0])
        t_white = VGroup(lab("insert breaks it: no enzyme", 28, WHITE), lab("the colony is white", 28, WHITE)).arrange(DOWN, buff=0.08).move_to([3.45, -2.2, 0])
        self.play(FadeIn(b1), FadeIn(bi), FadeIn(b2), FadeIn(bh), FadeIn(nox), FadeIn(t_white), run_time=0.6)
        self.play(*[dots[i].animate.set_fill(WHITE, 1.0) for i in range(16) if cols[i] == WHITE], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Library(SpokenScene):
    """mRNA -> cDNA -> library of clones -> filter, lysed, probed -> three kinds of probe."""

    def construct(self):
        rng = np.random.RandomState(9)
        # --- messenger RNA bars (left), their DNA copies (right)
        n = 8
        ys = [2.5 - i * 0.68 for i in range(n)]
        wi = 4
        mr = VGroup()
        cp = VGroup()
        for i, y in enumerate(ys):
            w = 2.6 + rng.rand() * 1.8
            b = bar(-6.0, -6.0 + w, y, TEAL, h=0.3, op=0.95)
            if i == wi:
                b.set_stroke(YELLOW, 4)
            mr.add(b)
            c = lanes((1.7, 1.7 + w), (1.7, 1.7 + w), y, YELLOW if i == wi else GREY, 0.16)
            cp.add(c)
        t_mr = lab("messenger RNA", 30, TEAL).move_to([-3.6, 3.35, 0])
        self.at("One route to a gene")
        self.play(FadeIn(mr, lag_ratio=0.1), FadeIn(t_mr), run_time=1.0)

        self.at("Reverse transcriptase")
        rt = chip("reverse transcriptase", ORANGE, 28).move_to([-0.3, -3.1, 0])
        self.play(FadeIn(rt, shift=UP * 0.15), run_time=0.4)
        arrs = VGroup(*[arr([-1.2, y, 0], [1.4, y, 0], ORANGE, 3, 0.14) for y in ys])
        self.play(FadeIn(arrs, lag_ratio=0.05), run_time=0.5)
        t_cp = lab("double-stranded copy: cDNA", 30, GREY).move_to([3.9, 3.35, 0])
        self.play(FadeIn(cp, lag_ratio=0.06), FadeIn(t_cp), run_time=0.7)

        # --- library of clones: plasmid rings
        self.at("is cloned")
        cols_n, rows_n = 8, 3
        gx = [-5.6 + 1.6 * i for i in range(cols_n)]
        gy = [2.0, 0.45, -1.1]
        rings = VGroup()
        wanted = {(1, 5)}
        for r in range(rows_n):
            for c in range(cols_n):
                rings.add(mini_plasmid(gx[c], gy[r], 0.5, YELLOW if (r, c) in wanted else GREY, 7, 0.6))
        t_lib = lab("every clone carries a different insert", 32, PURPLE).move_to([0, -2.75, 0])
        self.play(*[FadeOut(m) for m in (mr, t_mr, rt, arrs, cp, t_cp)], run_time=0.3)
        self.play(FadeIn(rings, lag_ratio=0.02), FadeIn(t_lib), run_time=0.8)

        self.at("A tissue rich")
        org = chip("ray's electric organ", GREY, 26).move_to([-3.4, -3.25, 0])
        t_more = lab("wanted clone more common", 28, YELLOW).move_to([2.6, -3.25, 0])
        self.play(FadeOut(t_lib), FadeIn(org), run_time=0.4)
        one = rings[1 * cols_n + 5]
        self.play(Indicate(one, color=YELLOW, scale_factor=1.25), run_time=0.6)

        def enrich(r, c):
            old = rings[r * cols_n + c]
            new = mini_plasmid(gx[c], gy[r], 0.5, YELLOW, 7, 0.6)
            return Transform(old, new)
        self.at("electric organ")
        self.play(enrich(0, 2), run_time=0.6)
        self.play(Indicate(rings[0 * cols_n + 2], color=YELLOW, scale_factor=1.25), run_time=0.5)
        self.at("more common")
        self.play(enrich(2, 6), FadeIn(t_more), run_time=0.5)
        self.play(Indicate(rings[2 * cols_n + 6], color=YELLOW, scale_factor=1.25), run_time=0.5)

        # --- colonies on a filter
        self.at("Colonies on a filter")
        filt = RoundedRectangle(corner_radius=0.2, width=12.4, height=5.1, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([0, 0.45, 0])
        filt_t = lab("filter", 26, GREY).move_to([-5.6, 2.55, 0])
        ydots = {(1, 5), (0, 2), (2, 6)}
        dots = VGroup()
        for r in range(rows_n):
            for c in range(cols_n):
                dots.add(colony([gx[c], gy[r]], GREY, 0.3, 0.9))
        self.play(FadeOut(org), FadeOut(t_more), FadeIn(filt), FadeIn(filt_t),
                  *[ReplacementTransform(rings[i], dots[i]) for i in range(len(rings))], run_time=0.6)
        self.at("broken open")
        def dna_pair(p, color):
            return VGroup(bar(p[0] - 0.26, p[0] + 0.26, p[1] + 0.045, color, h=0.09, op=1.0),
                          bar(p[0] - 0.26, p[0] + 0.26, p[1] - 0.045, color, h=0.09, op=1.0))
        cols_ = [d.get_fill_color() for d in dots]
        sq = VGroup(*[dna_pair(d.get_center(), GREY)
                      for i, d in enumerate(dots)])
        t_lys = lab("colonies broken open", 32, TEXT).move_to([0, -3.1, 0])
        self.play(*[ReplacementTransform(dots[i], sq[i]) for i in range(len(dots))], FadeIn(t_lys), run_time=0.7)

        self.at("fixed to the filter")
        t_fix = lab("DNA fixed to the filter as single strands", 32, TEXT).move_to([0, -3.1, 0])
        self.play(*[sq[i][0].animate.shift(UP * 0.2) for i in range(len(sq))],
                  *[sq[i][1].animate.shift(DOWN * 0.2) for i in range(len(sq))],
                  ReplacementTransform(t_lys, t_fix), run_time=0.8)

        self.at("a labeled probe")
        probe = chip("labeled probe", GREEN, 30).move_to([-4.2, 3.4, 0])
        self.play(FadeIn(probe, shift=DOWN * 0.15), FadeOut(t_fix), run_time=0.5)
        self.at("pairs with")
        hits = [sq[r * cols_n + c] for (r, c) in ydots]
        pr_bars = VGroup(*[bar(h.get_center()[0] - 0.26, h.get_center()[0] + 0.26, h.get_center()[1], GREEN, h=0.09, op=1.0)
                           for h in hits])
        glow = VGroup(*[Circle(radius=0.4, stroke_color=GREEN, stroke_width=6).move_to(h.get_center()) for h in hits])
        t_hit = lab("probe pairs with the wanted clone", 32, GREEN).move_to([0, -3.1, 0])
        self.play(FadeIn(pr_bars), *[Create(g) for g in glow], FadeIn(t_hit),
                  *[h[k].animate.set_fill(YELLOW, 1.0) for h in hits for k in (0, 1)], run_time=0.8)

        # --- kinds of probe: two pair with DNA, the antibody binds protein
        self.at("The probe can be")
        clear(self, 0.5)

        def two(a, b, size=28):
            g = VGroup(T(a, size, GREEN), T(b, size, GREEN)).arrange(DOWN, buff=0.06)
            box = RoundedRectangle(corner_radius=0.14, width=g.width + 0.44, height=g.height + 0.4, stroke_color=GREEN,
                                   stroke_width=2.5, fill_color=GREEN, fill_opacity=0.16)
            return VGroup(box, g.move_to(box))

        X0 = -6.1
        c1 = chip("a related gene", GREEN, 32)
        c2 = two("an oligonucleotide from", "partial protein sequence")
        c3 = two("an antibody, if the library", "expresses the protein")
        rows = [(c1, 2.1), (c2, 0.0), (c3, -2.1)]
        for c, y in rows:
            c.move_to([X0 + c.width / 2, y, 0])
        dna_t = [VGroup(bar(2.4, 6.0, y + 0.07, YELLOW, h=0.14, op=1.0), bar(2.4, 6.0, y - 0.07, YELLOW, h=0.14, op=1.0))
                 for y in (2.1, 0.0)]
        dna_l = [lab("the clone's DNA", 26, YELLOW).move_to([4.2, y - 0.55, 0]) for y in (2.1, 0.0)]
        prot = chip("the clone's protein", YELLOW, 30).move_to([4.2, -2.1, 0])
        targets = [dna_t[0], dna_t[1], prot]
        labels = [dna_l[0], dna_l[1], None]
        for (c, y), ph, tg, lb in zip(rows, ("a related gene", "an oligonucleotide", "or, if the library"), targets, labels):
            self.at(ph)
            a = arr([c.get_right()[0] + 0.1, y, 0], [tg.get_left()[0] - 0.15, y, 0], GREEN, 3, 0.16)
            self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.4)
            self.play(GrowArrow(a), FadeIn(tg), *([FadeIn(lb)] if lb is not None else []), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """example plate and film; dark spot traced back to a white colony; then the estrogen receptor chain."""

    def construct(self):
        px, py, PR = -3.6, 0.35, 2.7
        dish, pts = plate(px, py, PR, 18, 21, 0.8)
        white_i = {2, 7, 11, 14}
        dots = VGroup(*[colony(p, WHITE if i in white_i else COLB, 0.3, 1.0) for i, p in enumerate(pts)])
        p_t = lab("reference plate", 28, GREY).move_to([px, py - PR - 0.3, 0])
        ex = lab("example, idealised", 22, GREY).move_to([px, py + PR + 0.3, 0])
        fx, fy, FW, FH = 3.6, 0.2, 4.8, 4.8
        film = RoundedRectangle(corner_radius=0.12, width=FW, height=FH, stroke_color=GREY, stroke_width=3,
                                fill_color="#C9CDD6", fill_opacity=1.0).move_to([fx, fy, 0])
        f_t = lab("X-ray film", 28, GREY).move_to([fx, fy - FH / 2 - 0.35, 0])
        rp = chip("radioactive probe", GREEN, 28).move_to([fx, 3.1, 0])
        # film spots sit where the plate colonies sit (scaled to the film)
        sc = (FW * 0.9) / (2 * PR)
        def on_film(p):
            return np.array([fx + (p[0] - px) * sc, fy + (p[1] - py) * sc])
        spots = VGroup(*[Circle(radius=0.26, stroke_color="#10131a", stroke_width=2, fill_color="#10131a", fill_opacity=0.95)
                         .move_to([*on_film(pts[i]), 0]) for i in (7, 14)])

        self.at("A radioactive probe")
        self.play(FadeIn(rp, shift=DOWN * 0.15), run_time=0.5)
        self.at("exposes")
        self.play(FadeIn(film), FadeIn(f_t), run_time=0.6)
        self.at("Dark spots mark")
        self.play(FadeIn(spots, lag_ratio=0.4), run_time=0.7)
        self.at("matched to a reference plate")
        self.play(FadeIn(dish), FadeIn(dots, lag_ratio=0.04), FadeIn(p_t), FadeIn(ex), run_time=0.9)
        links = VGroup()
        rings_ = VGroup()
        for i in (7, 14):
            s = spots[[7, 14].index(i)].get_center()
            links.add(DashedLine(s + np.array([-0.3, 0, 0]), np.array([pts[i][0] + 0.4, pts[i][1], 0]), color=YELLOW,
                                 stroke_width=3))
            rings_.add(Circle(radius=0.42, stroke_color=YELLOW, stroke_width=5).move_to([pts[i][0], pts[i][1], 0]))
        self.play(Create(links), Create(rings_), run_time=0.9)

        self.at("White colonies are")
        wc = VGroup(*[Circle(radius=0.42, stroke_color=GREEN, stroke_width=4).move_to([pts[i][0], pts[i][1], 0])
                      for i in white_i if i not in (7, 14)])
        wt = lab("white: a strong hint of an insert, not proof", 30, GREEN).move_to([0.0, -3.35, 0])
        self.play(Create(wc), FadeIn(wt), run_time=0.8)

        # --- the estrogen receptor chain
        self.at("Estrogen receptor clones")
        clear(self, 0.5)
        c_m = chip("mRNA from MCF-7 cells", TEAL, 30).move_to([-3.4, 2.9, 0])
        c_l = chip("cDNA libraries", PURPLE, 30).move_to([2.9, 2.9, 0])
        a0 = arr(c_m.get_right() + [0.1, 0, 0], c_l.get_left() + [-0.1, 0, 0], GREY, 4, 0.18)
        self.play(FadeIn(c_m), GrowArrow(a0), FadeIn(c_l), run_time=0.8)
        c_a = chip("found with an antibody", GREEN, 30).move_to([-3.3, 1.1, 0])
        c_o = chip("and with oligonucleotide probes", GREEN, 30).move_to([2.8, 1.1, 0])
        self.at("found with an antibody")
        self.play(FadeIn(c_a, shift=UP * 0.15), run_time=0.5)
        self.at("and with oligonucleotide")
        self.play(FadeIn(c_o, shift=UP * 0.15), run_time=0.5)
        self.at("The full")
        c_f = chip("full cDNA", YELLOW, 30).move_to([-3.4, -0.7, 0])
        c_s = chip("protein sequence", YELLOW, 30).move_to([2.2, -0.7, 0])
        a1 = arr(c_f.get_right() + [0.1, 0, 0], c_s.get_left() + [-0.1, 0, 0], GREY, 4, 0.18)
        self.play(FadeIn(c_f), GrowArrow(a1), FadeIn(c_s), run_time=0.8)
        self.at("Expressed in")
        c_h = chip("expressed in HeLa cells", GREY, 26).move_to([-3.65, -2.5, 0])
        c_e = chip("binds estradiol like the natural receptor", GREEN, 26).move_to([2.95, -2.5, 0])
        a2 = arr(c_h.get_right() + [0.1, 0, 0], c_e.get_left() + [-0.1, 0, 0], GREY, 4, 0.18)
        self.play(FadeIn(c_h), GrowArrow(a2), FadeIn(c_e), run_time=0.8)
        tag = lab("Green et al., 1986", 22, GREY).move_to([5.0, -3.4, 0])
        self.play(FadeIn(tag), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """traits are not sequence; vector-only control plate; white colony with no insert; short recovered insert."""

    def construct(self):
        # traits vs sequence
        self.at("Antibiotic resistance")
        t1 = chip("antibiotic resistance", GREEN, 38)
        t2 = chip("color", COLB, 38)
        ne = T("≠", 80, RED, weight=BOLD)
        sq = chip("sequence", YELLOW, 42)
        row = VGroup(t1, t2, ne, sq).arrange(RIGHT, buff=0.4).move_to([0, 0.2, 0])
        tr = lab("traits", 44, TEXT).move_to([VGroup(t1, t2).get_center()[0], 1.7, 0])
        br = Line([t1.get_left()[0], 1.2, 0], [t2.get_right()[0], 1.2, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(tr), Create(br), run_time=0.6)
        self.at("not sequence")
        self.play(FadeIn(ne, scale=1.3), FadeIn(sq), run_time=0.6)

        # control plate
        self.at("A vector that closed")
        clear(self, 0.5)
        R = 2.45
        d1, p1 = plate(-3.4, -0.1, R, 14, 5, 0.7)
        d2, p2 = plate(3.4, -0.1, R, 5, 8, 1.0)
        dots1 = VGroup(*[colony(p, GREY, 0.27, 0.85) for p in p1])
        dots2 = VGroup(*[colony(p, GREY, 0.27, 0.85) for p in p2])
        l1 = lab("vector + insert + ligase", 28, TEXT).move_to([-3.4, -0.1 + R + 0.4, 0])
        l2 = lab("vector only: insert left out", 28, TEXT).move_to([3.4, -0.1 + R + 0.4, 0])
        self.play(FadeIn(d1), FadeIn(dots1, lag_ratio=0.05), FadeIn(l1), run_time=0.7)
        self.play(FadeIn(d2), FadeIn(l2), run_time=0.4)
        self.play(FadeIn(dots2, lag_ratio=0.2), run_time=0.8)
        rs = VGroup(*[Circle(radius=0.4, stroke_color=RED, stroke_width=4).move_to([p[0], p[1], 0]) for p in p2])
        bgt = lab("still resistant: background", 28, RED).move_to([3.4, -0.1 - R - 0.4, 0])
        self.at("so plate a")
        self.play(Create(rs), FadeIn(bgt), run_time=0.8)

        # white colonies with no insert
        self.at("Some white colonies")
        clear(self, 0.5)
        xs = [-4.5, -1.5, 1.5, 4.5]
        whites = VGroup(*[colony([x, 2.4], WHITE, 0.5, 1.0) for x in xs])
        rg = VGroup()
        for i, x in enumerate(xs):
            rg.add(ring(x, -0.2, 0.95, PURPLE, 10))
            if i != 2:
                rg.add(insert_arc(x, -0.2, 0.95, YELLOW, 11, 0.55))
        ar = VGroup(*[arr([x, 1.8, 0], [x, 0.95, 0], GREY, 3, 0.14) for x in xs])
        wlab = lab("white colonies", 28, WHITE).move_to([0, 3.4, 0])
        self.play(FadeIn(whites, lag_ratio=0.15), FadeIn(wlab), run_time=0.7)
        self.play(FadeIn(ar), FadeIn(rg), run_time=0.7)
        ni = lab("no insert", 30, RED, weight=BOLD).move_to([xs[2], -1.7, 0])
        ok = lab("insert", 28, YELLOW).move_to([xs[0], -1.7, 0])
        self.play(FadeIn(ni, shift=UP * 0.1), FadeIn(ok), run_time=0.6)

        self.at("So confirm")
        conf = chip("digest or colony PCR", ORANGE, 30).move_to([-3.4, -3.0, 0])
        self.play(FadeIn(conf, shift=UP * 0.15), run_time=0.5)
        self.at("and sequence")
        clear(self, 0.4)
        bx, by, BR, sp = 0.0, -0.3, 1.8, 0.55
        big = VGroup(ring(bx, by, BR, PURPLE, 14), insert_arc(bx, by, BR, YELLOW, 15, sp))
        jl = np.array([bx - BR * np.sin(sp), by + BR * np.cos(sp), 0])
        jr = np.array([bx + BR * np.sin(sp), by + BR * np.cos(sp), 0])
        jd = VGroup(Dot(jl, radius=0.12, color=ORANGE), Dot(jr, radius=0.12, color=ORANGE))
        v_t = lab("vector", 30, PURPLE).move_to([bx, by - 0.2, 0])
        i_t = lab("insert", 30, YELLOW).move_to([bx, by + BR + 1.3, 0])
        self.play(FadeIn(big), FadeIn(v_t), FadeIn(i_t), FadeIn(jd), run_time=0.7)
        RR = BR + 0.55
        def read(a0, da):
            r = Arc(radius=RR, start_angle=a0, angle=da, arc_center=np.array([bx, by, 0.0]), stroke_color=ORANGE,
                    stroke_width=7)
            r.add_tip(tip_length=0.22)
            return r
        r1 = read(PI / 2 + sp + 0.75, -1.15)     # starts in the vector (left), runs across the left junction into the insert
        r2 = read(PI / 2 - sp - 0.75, 1.15)      # starts in the vector (right), runs across the right junction into the insert
        t_r = VGroup(lab("each read starts in the vector,", 30, ORANGE), lab("runs across a junction into the insert", 30, ORANGE)) \
            .arrange(DOWN, buff=0.08).move_to([0, -3.1, 0])
        self.play(Create(r1), Create(r2), FadeIn(t_r), run_time=1.0)

        # short insert
        self.at("Clones can lose")
        clear(self, 0.5)
        ex_b = bar(-5.6, 5.6, 1.6, YELLOW, h=0.6, op=1.0)
        ex_t = lab("expected insert size", 32, YELLOW).move_to([0, 2.5, 0])
        got_b = bar(-5.6, -1.6, -0.6, RED, h=0.6, op=1.0)
        lost = DashedVMobject(Rectangle(width=7.2, height=0.6, stroke_color=RED, stroke_width=3).move_to([2.0, -0.6, 0]))
        got_t = lab("recovered insert: shorter", 32, RED).move_to([-3.6, -1.5, 0])
        self.play(FadeIn(ex_b), FadeIn(ex_t), run_time=0.6)
        self.play(FadeIn(got_b), Create(lost), FadeIn(got_t), run_time=0.8)
        self.at("so compare")
        cmp_t = lab("compare the insert with its expected size", 32, TEXT).move_to([0, -2.9, 0])
        lines_ = VGroup(*[DashedLine([x, 1.25, 0], [x, -0.95, 0], color=GREY, stroke_width=2) for x in (-5.6, 5.6)])
        self.play(FadeIn(cmp_t), Create(lines_), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
def card(cx, cy, w, h):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=GREY, stroke_width=2.5,
                            fill_color=GREY, fill_opacity=0.08).move_to([cx, cy, 0])


class S07Found1(SpokenScene):
    """1973: recombinant plasmids replicate in E. coli. 1982: the Torpedo acetylcholine receptor subunit read from cDNA."""

    def construct(self):
        CW, CH = 6.1, 6.9
        x1, x2 = -3.25, 3.25
        # ---- 1973
        c1 = card(x1, 0, CW, CH)
        y1 = T("1973", 60, GOLD, font=TITLE_FONT).move_to([x1, 2.5, 0])
        n1 = lab("Cohen, Chang, Boyer & Helling", 28, TEXT).move_to([x1, 1.65, 0])
        pl = VGroup(ring(x1 - 1.85, 0.2, 0.75, PURPLE, 10), insert_arc(x1 - 1.85, 0.2, 0.75, YELLOW, 11, 0.5))
        cl = cell(x1 + 1.3, 0.2, 2.9, 2.5, GREY)
        inside = VGroup(*[mini_plasmid(x1 + 1.3 + dx, 0.2 + dy, 0.3, YELLOW, 5, 0.5)
                          for dx, dy in ((-0.8, 0.5), (0.0, 0.55), (0.8, 0.5), (-0.8, -0.4), (0.0, -0.45), (0.8, -0.4))])
        a = arr([x1 - 0.95, 0.2, 0], [x1 - 0.25, 0.2, 0], GREY, 4, 0.18)
        t1 = VGroup(lab("recombinant", 24, PURPLE), lab("plasmid", 24, PURPLE)).arrange(DOWN, buff=0.05).move_to([x1 - 1.85, -1.0, 0])
        t2 = VGroup(lab("many copies", 24, GREY), lab("in E. coli", 24, GREY)).arrange(DOWN, buff=0.05).move_to([x1 + 1.3, -1.45, 0])
        s1 = lab("replicates in E. coli", 30, TEXT).move_to([x1, -2.35, 0])
        g1 = lab("Cohen, Chang, Boyer, Helling, 1973", 22, GREY).move_to([x1, -3.05, 0])
        self.at("In 1973")
        self.play(FadeIn(c1), FadeIn(y1), FadeIn(n1), run_time=0.6)
        self.play(FadeIn(pl), FadeIn(t1), run_time=0.5)
        self.at("made recombinant plasmids")
        self.play(GrowArrow(a), FadeIn(cl), run_time=0.5)
        self.at("that replicate")
        self.play(FadeIn(inside, lag_ratio=0.15), FadeIn(t2), FadeIn(s1), FadeIn(g1), run_time=1.0)

        # ---- 1982
        c2 = card(x2, 0, CW, CH)
        y2 = T("1982", 60, GOLD, font=TITLE_FONT).move_to([x2, 2.5, 0])
        n2 = lab("Noda, Numa & colleagues", 28, TEXT).move_to([x2, 1.65, 0])
        mr = bar(x2 - 2.6, x2 - 0.9, 0.7, TEAL, h=0.3, op=0.95)
        mrt = lab("electric organ mRNA", 22, TEAL).move_to([x2 - 1.5, 0.28, 0])
        cl_ = mini_plasmid(x2 + 1.5, 0.7, 0.45, YELLOW, 8, 0.6)
        a3 = arr([x2 - 0.7, 0.7, 0], [x2 + 0.9, 0.7, 0], GREY, 3, 0.14)
        seq = bar(x2 - 2.6, x2 + 2.6, -0.55, YELLOW, h=0.4, op=1.0)
        a4 = arr([x2 + 1.5, 0.15, 0], [x2 + 1.5, -0.3, 0], GREY, 3, 0.14)
        st = lab("461 amino acids", 28, YELLOW).move_to([x2, -1.15, 0])
        s2 = lab("Torpedo acetylcholine receptor", 24, TEXT).move_to([x2, -1.75, 0])
        s2b = lab("alpha-subunit precursor,", 24, TEXT).move_to([x2, -2.1, 0])
        s2c = lab("from cloned cDNA", 24, TEXT).move_to([x2, -2.45, 0])
        g2 = lab("Noda et al., 1982", 22, GREY).move_to([x2, -3.05, 0])
        self.at("In 1982")
        self.play(FadeIn(c2), FadeIn(y2), FadeIn(n2), run_time=0.6)
        self.at("read the 461")
        self.play(FadeIn(mr), FadeIn(mrt), FadeIn(a3), FadeIn(cl_), run_time=0.6)
        self.play(GrowArrow(a4), FadeIn(seq), FadeIn(st), run_time=0.7)
        self.play(FadeIn(s2), FadeIn(s2b), FadeIn(s2c), FadeIn(g2), run_time=0.6)
        self.at("from cloned")
        self.play(Indicate(cl_, color=YELLOW, scale_factor=1.3), run_time=0.7)
        self.at("Cloning gave the sequence")
        box = SurroundingRectangle(VGroup(seq, st), color=YELLOW, buff=0.15, stroke_width=3)
        note = VGroup(lab("the sequence from the gene,", 26, YELLOW), lab("not the protein", 26, YELLOW)) \
            .arrange(DOWN, buff=0.06).move_to([x2, -2.3, 0])
        self.play(FadeOut(s2b), FadeOut(s2c), FadeOut(s2), Create(box), FadeIn(note), run_time=0.7)
        self.finish()


class S08Found2Rule(SpokenScene):
    """1986 cone pigment genes: a strict screen lights human rhodopsin only; a relaxed screen lights extra spots; then the rule."""

    def construct(self):
        yr = T("1986", 60, GOLD, font=TITLE_FONT).move_to([-4.6, 3.1, 0])
        nm = lab("Nathans, Thomas & Hogness", 32, TEXT).move_to([0.9, 3.1, 0])
        pr = chip("bovine rhodopsin probe", GREEN, 32).move_to([-3.4, 2.1, 0])
        strg = lab("strict hybridization", 32, TEXT).move_to([3.4, 2.1, 0])
        filt = RoundedRectangle(corner_radius=0.2, width=12.2, height=3.0, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([0, -0.05, 0])
        xs = [-4.8, -2.9, -1.0, 0.9, 2.8, 4.7]
        spots = VGroup(*[Circle(radius=0.5, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
                         .move_to([x, 0.55, 0]) for x in xs])
        rl = VGroup(lab("human", 28, TEXT), lab("rhodopsin", 28, TEXT)).arrange(DOWN, buff=0.06).move_to([xs[0], -0.5, 0])
        self.at("In 1986")
        self.play(FadeIn(yr), FadeIn(nm), run_time=0.6)
        self.play(FadeIn(filt), FadeIn(spots, lag_ratio=0.1), run_time=0.6)
        # light motion while the header holds: a faint scan line sweeps the row of spots
        scan = Line([-5.8, 1.15, 0], [-5.8, -1.35, 0], color=TEXT, stroke_width=3).set_opacity(0.35)
        self.add(scan)
        left_to_right = True
        while True:
            rest = self.t_of("A first screen") - 0.3 - self.elapsed()
            if rest < 1.0:
                break
            d = min(3.2, rest)
            self.play(scan.animate.move_to([5.8 if left_to_right else -5.8, scan.get_center()[1], 0]), run_time=d,
                      rate_func=smooth)
            left_to_right = not left_to_right
        self.play(FadeOut(scan), run_time=0.2)
        self.at("A first screen")
        self.play(FadeIn(pr, shift=DOWN * 0.15), FadeIn(strg), FadeIn(rl), run_time=0.5)
        self.at("found only human rhodopsin")
        self.play(spots[0].animate.set_fill(GREEN, 0.95).set_stroke(GREEN), run_time=0.6)
        lonely = lab("only the gene you already know", 32, GREEN).move_to([0, -2.3, 0])
        self.play(FadeIn(lonely, shift=UP * 0.1), run_time=0.5)
        self.at("The cone genes appeared")
        strg2 = lab("relaxed: mismatches allowed", 30, ORANGE).move_to([3.0, 2.1, 0])
        self.play(FadeOut(lonely), ReplacementTransform(strg, strg2), run_time=0.4)
        self.play(spots[3].animate.set_fill(GREEN, 0.95).set_stroke(GREEN),
                  spots[4].animate.set_fill(GREEN, 0.6).set_stroke(GREEN, opacity=0.6),
                  spots[5].animate.set_fill(GREEN, 0.3).set_stroke(GREEN, opacity=0.3), run_time=0.8)
        brk = VGroup(Line([xs[3] - 0.5, -0.2, 0], [xs[5] + 0.5, -0.2, 0], color=GREEN, stroke_width=4),
                     lab("cone pigment genes", 28, GREEN).move_to([(xs[3] + xs[5]) / 2, -0.7, 0]),
                     lab("…", 44, GREEN).move_to([5.7, 0.55, 0]))
        self.play(FadeIn(brk), run_time=0.5)
        self.at("A probe may find only")
        pm = lab("a probe may find only the gene you already know", 32, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(pm), run_time=0.5)

        self.at("Color and resistance")
        keep = VGroup(yr, nm, pr, strg2, filt, spots, rl, brk, pm)
        self.play(FadeOut(keep), run_time=0.5)
        r1 = T("Color and resistance are hints.", 54, TEXT, font=TITLE_FONT)
        r2 = T("Sequence confirms a clone.", 58, GOLD, font=TITLE_FONT)
        fit(r1, max_w=12.2)
        fit(r2, max_w=12.2)
        r1.move_to([0, 0.9, 0])
        r2.move_to([0, -0.6, 0])
        self.play(FadeIn(r1, shift=UP * 0.15), run_time=0.6)
        self.at("Sequence confirms")
        self.play(FadeIn(r2, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "Color and resistance are hints. Sequence confirms a clone."
