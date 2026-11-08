"""Forward genetic screens: start from what goes wrong  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = chromosomes and genomes (DNA bars)
  RED    = a mutation (a random break), also a pitfall, leak or a miss
  YELLOW = the phenotype: mutant animals, the thing we score and pick
  GREEN  = normal / wild type, a confirmation or control
  ORANGE = mapping: SNPs, the interval, the gene being found
  PURPLE = the transposon (P element)
  GREY   = outlines, labels, structure
  GOLD   = dates and the closing rule
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def arr(a, b, color=GREY, w=5, tip=0.2):
    a = [a[0], a[1], 0]
    b = [b[0], b[1], 0]
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def badge_x(box, color=RED):
    """A small red cross badge on the top-right corner of a box (meaning: not available)."""
    c = box.get_corner(UR) + LEFT * 0.35 + DOWN * 0.3
    return cross_x(c, 0.2, color)


def dbox(w, h, color=GREY, sw=2.5):
    return DashedVMobject(RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=sw),
                          num_dashes=36)


def larva(w=2.4, h=0.7, belts=(1, 1, 1, 1, 1), bc=TEXT, color=GREY, spines=3, fill=0.12):
    """A fly larva as a capsule of segments; belts of small spine ticks mark the pattern."""
    n = len(belts)
    body = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=fill)
    g = VGroup(body)
    x_start = -w / 2 + h * 0.45
    seg_w = (w - h * 0.9) / n
    for i in range(n):
        x0 = x_start + i * seg_w
        if i > 0:
            g.add(Line([x0, -h * 0.34, 0], [x0, h * 0.34, 0], color=GREY, stroke_width=1.5).set_opacity(0.6))
        if belts[i]:
            for k in range(spines):
                xx = x0 + seg_w * (0.18 + 0.64 * (k + 0.5) / spines)
                g.add(Line([xx, -h * 0.2, 0], [xx, h * 0.2, 0], color=bc, stroke_width=3))
    return g


def pair(w=1.5, causal=(), color=BLUE, h=0.16, gap=0.3):
    """A chromosome pair: two bars. `causal` lists which bars (0 top, 1 bottom) carry a red mutation mark."""
    bars = VGroup()
    for j in range(2):
        b = RoundedRectangle(corner_radius=h / 2, width=w, height=h, stroke_color=color, stroke_width=2,
                             fill_color=color, fill_opacity=0.35).move_to([0, (0.5 - j) * gap, 0])
        bars.add(b)
        if j in causal:
            bars.add(Line([w * 0.12, (0.5 - j) * gap - h, 0], [w * 0.12, (0.5 - j) * gap + h, 0], color=RED, stroke_width=5))
    return bars


def yeast(r=0.4, bud=0.0, color=GREY):
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15)
    g = VGroup(c)
    if bud > 0:
        b = Circle(radius=r * bud, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.15)
        b.move_to(c.get_right() + RIGHT * r * bud * 0.7 + UP * r * 0.15)
        g.add(b)
    return g


def worm_cell(r=0.42, color=GREY, fill=0.15):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill)


def cross_x(center, s=0.35, color=RED):
    cx, cy = center[0], center[1]
    return VGroup(Line([cx - s, cy - s, 0], [cx + s, cy + s, 0], color=color, stroke_width=6),
                  Line([cx - s, cy + s, 0], [cx + s, cy - s, 0], color=color, stroke_width=6))


def lines(*texts, size=24, color=TEXT, buff=0.14, align=LEFT, colors=None):
    g = VGroup(*[T(t, size, (colors[i] if colors else color)) for i, t in enumerate(texts)])
    return g.arrange(DOWN, aligned_edge=align, buff=buff)


def poly(pts, color=YELLOW, w=5):
    m = VMobject()
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in pts])
    m.set_stroke(color, w)
    m.set_fill(opacity=0)
    return m



# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Start From What Goes Wrong"


def qbox(name, x, y, w=3.3, h=1.9):
    b = dbox(w, h, GREY)
    t = T(name, 36, TEXT).move_to([0, 0.38, 0])
    q = T("?", 64, YELLOW, weight=BOLD).move_to([0, -0.3, 0])
    g = VGroup(b, t, q).move_to([x, y, 0])
    g.box = b
    return g


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """gene and protein unknown (question boxes); forward genetics starts from the phenotype in a mutagenized population."""

    def construct(self):
        rng = np.random.RandomState(4)
        ry = 1.85
        mut = larva(3.7, 1.25, belts=(1, 0, 1, 0, 1), bc=YELLOW, color=YELLOW, spines=3, fill=0.2).move_to([4.2, ry, 0])
        mut_lbl = lab("segmentation phenotype", 28, YELLOW).move_to([4.2, ry - 1.2, 0])
        gb = qbox("gene", -4.6, ry)
        pb = qbox("protein", -0.8, ry)
        a1 = DashedLine([-2.85, ry, 0], [-2.55, ry, 0], color=GREY, stroke_width=3)
        a2 = DashedLine([0.95, ry, 0], [2.3, ry, 0], color=GREY, stroke_width=3)

        self.at("How do you find")
        self.play(FadeIn(mut, shift=LEFT * 0.2), FadeIn(mut_lbl), run_time=0.6)
        self.at("the genes behind")
        self.play(FadeIn(gb), FadeIn(pb), Create(a1), Create(a2), run_time=0.8)

        self.at("Before cloning was routine")
        before = lab("before cloning was routine", 30, GOLD).move_to([-2.4, 0.0, 0])
        self.play(FadeIn(before, shift=UP * 0.1), run_time=0.5)
        self.at("could not start from")
        x1 = badge_x(gb.box)
        x2 = badge_x(pb.box)
        self.play(Create(x1), Create(x2), gb.box.animate.set_color(RED), pb.box.animate.set_color(RED), run_time=0.5)
        self.at("products were unknown")
        unk = lab("products unknown", 28, RED).move_to([-2.4, -0.6, 0])
        self.play(FadeIn(unk), run_time=0.4)

        self.at("Forward genetics starts")
        self.play(FadeOut(before), FadeOut(unk), FadeOut(x1), FadeOut(x2), FadeOut(a1), FadeOut(a2),
                  gb.box.animate.set_color(GREY), pb.box.animate.set_color(GREY),
                  gb.animate.set_opacity(0.6), pb.animate.set_opacity(0.6), run_time=0.5)
        fg = lab("forward genetics: phenotype first", 32, YELLOW, weight=BOLD).move_to([1.6, -0.15, 0])
        self.play(FadeIn(fg, shift=DOWN * 0.1), run_time=0.5)

        self.at("a population")
        py = -2.0
        xs = [-4.9 + 2.0 * i for i in range(6)]
        pop = VGroup()
        for i, x in enumerate(xs):
            lv = larva(1.8, 0.62, belts=(1, 1, 1, 1, 1), bc=TEXT, color=GREY, spines=2)
            lv.move_to([x, py, 0])
            for _ in range(rng.randint(1, 4)):
                tx = x + rng.uniform(-0.75, 0.75)
                lv.add(Line([tx, py - 0.25, 0], [tx, py + 0.25, 0], color=RED, stroke_width=4))
            pop.add(lv)
        pop_lbl = lab("a population carrying random mutations", 28, GREY).move_to([0, -3.1, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in pop], lag_ratio=0.15), FadeIn(pop_lbl),
                  run_time=1.2)

        self.at("works toward the gene")
        picked = larva(1.8, 0.62, belts=(1, 0, 1, 0, 1), bc=YELLOW, color=YELLOW, spines=2, fill=0.25).move_to(pop[0].get_center())
        self.play(Transform(pop[0], picked), run_time=0.4)
        up = arr([xs[0], py + 0.5], [xs[0], ry - 1.15], YELLOW, w=7, tip=0.28)
        self.play(GrowArrow(up), gb.animate.set_opacity(1.0), run_time=0.8)

        self.at("makes no guess")
        ng = lab("no candidate chosen first", 32, GREEN, weight=BOLD).move_to([1.6, -0.15, 0])
        self.play(FadeOut(fg), FadeIn(ng, shift=DOWN * 0.1), run_time=0.5)
        self.at("no one had thought")
        self.play(pb.animate.set_opacity(1.0), Indicate(pb[2], color=YELLOW, scale_factor=1.3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Mutagenize(SpokenScene):
    """choose a scorable phenotype; random breaks in many genomes (EMS, a hopping P element)."""

    def construct(self):
        lv = larva(7.0, 2.0, belts=(1, 1, 1, 1, 1), bc=YELLOW, color=GREY, spines=3).move_to([0, 0.6, 0])
        lv_lbl = lines("belts of spines on a fly larva's cuticle", size=34, color=YELLOW).move_to([0, -1.2, 0])
        head = lab("a phenotype you can score", 38, TEXT, weight=BOLD).move_to([0, 2.9, 0])

        self.at("Choose a phenotype")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        self.at("belts of spines")
        self.play(FadeIn(lv), FadeIn(lv_lbl), run_time=0.7)

        self.at("Then break genes")
        self.play(FadeOut(VGroup(lv, lv_lbl, head)), run_time=0.3)
        n = 7
        gx0, gx1 = -6.2, 1.5
        gys = [2.9 - i * 0.82 for i in range(n)]
        bars = VGroup(*[RoundedRectangle(corner_radius=0.11, width=gx1 - gx0, height=0.28, stroke_color=BLUE, stroke_width=2,
                                         fill_color=BLUE, fill_opacity=0.35).move_to([(gx0 + gx1) / 2, y, 0]) for y in gys])
        gl = lab("many genomes", 28, BLUE).move_to([-2.35, -2.75, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.08), FadeIn(gl), run_time=0.7)

        def ticks(seed, k):
            r = np.random.RandomState(seed)
            out = VGroup()
            for y in gys:
                for _ in range(r.randint(0, k + 1)):
                    x = r.uniform(gx0 + 0.3, gx1 - 0.3)
                    out.add(Line([x, y - 0.33, 0], [x, y + 0.33, 0], color=RED, stroke_width=6))
            return out

        RX = 4.2
        self.at("alkylates")
        ems = chip("EMS: a chemical", ORANGE, 30).move_to([RX, 2.5, 0])
        t1 = ticks(1, 2)
        self.play(FadeIn(ems, shift=LEFT * 0.2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t, scale=2.0) for t in t1], lag_ratio=0.06), run_time=0.9)
        self.at("A jump")
        pe = chip("P element", PURPLE, 30).move_to([RX, 0.9, 0])
        blk = Rectangle(width=0.55, height=0.55, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.8).move_to([-4.9, gys[1], 0])
        self.play(FadeIn(pe, shift=LEFT * 0.2), FadeIn(blk, scale=1.5), run_time=0.5)
        self.at("supplies transposase")
        js = lines("jumpstarter supplies", "transposase", size=26, color=PURPLE, align=ORIGIN, buff=0.06).move_to([RX, -0.2, 0])
        self.play(FadeIn(js), run_time=0.3)
        self.at("to new places")
        path = [(-2.0, gys[1]), (-3.6, gys[1]), (-0.6, gys[1])]
        for px, py in path:
            self.play(blk.animate.move_to([px, py, 0]), run_time=0.35)
        self.at("in the fly genome")
        gen = lines("mutator moves to new", "places in the fly genome", size=26, color=PURPLE, align=ORIGIN, buff=0.06).move_to([RX, -1.4, 0])
        self.play(FadeIn(gen), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Breed(SpokenScene):
    """breed so the recessive shows, then score a dish and pick the rare mutants."""

    def construct(self):
        rng = np.random.RandomState(21)
        cy = 2.35
        xs = [-4.1, 0.3, 4.5]
        icons = [pair(2.2, causal=(1,), h=0.2, gap=0.38).move_to([x, cy, 0]) for x in xs]
        gl = [lines("one mutagenized", "chromosome", size=26, color=RED, buff=0.05, align=ORIGIN), lab("bred again", 26, GREY), lab("bred again", 26, GREY)]
        for g, x in zip(gl, xs):
            g.move_to([x, cy - 0.85, 0])
        ar = [arr([xs[0] + 1.3, cy], [xs[1] - 1.3, cy], GREY, w=4, tip=0.18),
              arr([xs[1] + 1.3, cy], [xs[2] - 1.3, cy], GREY, w=4, tip=0.18)]

        home0 = icons[0].get_center().copy()
        glhome0 = gl[0].get_center().copy()
        icons[0].scale(2.0).move_to([0, 0.5, 0])
        gl[0].move_to([0, -0.7, 0])
        self.at("breed so that")
        self.play(FadeIn(icons[0]), FadeIn(gl[0]), run_time=0.6)
        self.at("bred two more generations")
        self.play(icons[0].animate.scale(0.5).move_to(home0), gl[0].animate.move_to(glhome0), run_time=0.5)
        self.play(GrowArrow(ar[0]), FadeIn(icons[1]), FadeIn(gl[1]), run_time=0.5)
        self.play(GrowArrow(ar[1]), FadeIn(icons[2]), FadeIn(gl[2]), run_time=0.5)

        self.at("two broken copies")
        gx, gy = -2.0, -1.45
        cell = 2.2
        pos = [(-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5)]
        cau = [(), (1,), (0,), (0, 1)]
        grid = VGroup()
        for (px, py), c in zip(pos, cau):
            sq = Rectangle(width=cell, height=cell, stroke_color=GREY, stroke_width=2)
            ic = pair(1.5, causal=c, h=0.2, gap=0.46).move_to(sq)
            grid.add(VGroup(sq, ic).move_to([gx + px * cell, gy + py * cell, 0]))
        self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.15), run_time=0.8)
        hl = SurroundingRectangle(grid[3], color=YELLOW, buff=0.0, stroke_width=7)
        ql = lines("two broken copies", "of the same gene:", "the mutation shows", size=30, color=YELLOW, buff=0.1, align=LEFT).move_to([3.9, -1.8, 0])
        self.play(Create(hl), FadeIn(ql), run_time=0.5)

        self.at("score every line")
        self.play(FadeOut(VGroup(*icons, *gl, *ar, grid, hl, ql)), run_time=0.4)
        field = Ellipse(width=8.2, height=3.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.06).move_to([-2.2, 0.3, 0])
        fl = lab("microscope field: larval cuticles", 28, GREY).move_to([-2.2, 2.35, 0])
        xs_l = [-5.1, -3.4, -1.7, 0.0]
        cut = VGroup(*[larva(1.5, 0.7, belts=(1, 1, 1, 1, 1), bc=TEXT, color=GREY, spines=2).move_to([x, 0.3, 0]) for x in xs_l])
        dl = lab("every line scored", 30, GREY).move_to([-2.2, -1.7, 0])
        self.play(FadeIn(field), FadeIn(fl), LaggedStart(*[FadeIn(c) for c in cut], lag_ratio=0.1), FadeIn(dl), run_time=0.7)
        self.at("keep the mutants")
        mut = larva(1.5, 0.7, belts=(1, 0, 1, 0, 1), bc=YELLOW, color=YELLOW, spines=2, fill=0.3).move_to(cut[2].get_center())
        self.play(Transform(cut[2], mut), run_time=0.4)
        ring = SurroundingRectangle(cut[2], color=YELLOW, buff=0.2, corner_radius=0.2, stroke_width=4)
        rare = lab("abnormal spine belts: a mutant", 28, YELLOW).move_to([-2.2, -2.6, 0])
        vials = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.12, width=0.9, height=1.7, stroke_color=YELLOW, stroke_width=3,
                                                 fill_color=YELLOW, fill_opacity=0.08),
                                Rectangle(width=0.98, height=0.22, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.5).shift(UP * 0.9)).move_to([3.1 + i * 1.25, 0.2, 0]) for i in range(3)])
        tl = lab("fly stock vials", 28, GREY).move_to([4.4, -1.4, 0])
        kept = lab("mutant line kept", 28, YELLOW).move_to([3.1, -2.1, 0])
        self.play(Create(ring), FadeIn(rare), run_time=0.4)
        self.play(FadeIn(vials), FadeIn(tl), run_time=0.5)
        self.play(vials[0][0].animate.set_fill(YELLOW, 0.5), FadeIn(kept), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def boxlab(*ls, color=GREY, w=3.8, h=1.5, size=27):
    t = VGroup(*[T(l, size, TEXT) for l in ls]).arrange(DOWN, buff=0.08)
    box = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.14)
    return VGroup(box, t.move_to(box))


class S04Find(SpokenScene):
    """complementation sorts mutants into genes; mapping cross, pooled sequencing and rescue find and confirm the gene."""

    def construct(self):
        def case(x, b="mutant 2"):
            m1 = chip("mutant 1", YELLOW, 30).move_to([x - 1.45, 1.9, 0])
            m2 = chip(b, YELLOW, 30).move_to([x + 1.45, 1.9, 0])
            xs = T("x", 36, TEXT).move_to([x, 1.9, 0])
            d = arr([x, 1.25], [x, 0.3], GREY, w=6, tip=0.25)
            return VGroup(m1, m2, xs), d

        self.at("Then sort the mutants")
        head = lab("complementation: do two mutants hit the same gene?", 32, TEXT, weight=BOLD).move_to([0, 3.05, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
        self.at("Cross two mutants")
        pa, da = case(-3.2)
        pb, db = case(3.2, "mutant 3")
        self.play(FadeIn(pa), FadeIn(pb), run_time=0.6)
        self.at("Normal offspring")
        la = larva(3.5, 1.05, belts=(1, 1, 1, 1, 1), bc=TEXT, color=GREEN, fill=0.2).move_to([-3.2, -0.45, 0])
        ta = lines("normal offspring:", "different genes", size=30, color=GREEN, align=ORIGIN, buff=0.08).move_to([-3.2, -1.9, 0])
        self.play(GrowArrow(da), FadeIn(la, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(ta), run_time=0.4)
        self.at("A returning defect")
        lb = larva(3.5, 1.05, belts=(1, 0, 1, 0, 1), bc=YELLOW, color=YELLOW, fill=0.25).move_to([3.2, -0.45, 0])
        tb = lines("defect returns:", "the same gene", size=30, color=YELLOW, align=ORIGIN, buff=0.08).move_to([3.2, -1.9, 0])
        self.play(GrowArrow(db), FadeIn(lb, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(tb), run_time=0.4)


        self.at("To find the gene")
        self.play(FadeOut(VGroup(head, pa, pb, da, db, la, lb, ta, tb)), run_time=0.4)
        xs = [-4.35, 0.0, 4.35]
        y1, y2 = 1.45, -1.65
        bw = 3.8
        h2 = lab("mapping and confirming the gene", 32, TEXT, weight=BOLD).move_to([0, 3.15, 0])
        b1 = boxlab("mutant x", "polymorphic strain", color=BLUE).move_to([xs[0], y1, 0])
        b2 = boxlab("select mutant", "F2 recombinants", color=YELLOW).move_to([xs[1], y1, 0])
        b3 = boxlab("pool their", "descendants", color=GREY).move_to([xs[2], y1, 0])
        b4 = boxlab("sequence", "the pool", color=GREY).move_to([xs[2], y2, 0])
        b5 = boxlab("SNP markers: pattern", "points to linked interval", color=ORANGE, size=25).move_to([xs[1], y2, 0])
        b6 = boxlab("confirm with", "complementation", "or rescue", color=GREEN, h=1.5, size=25).move_to([xs[0], y2, 0])
        gap = xs[1] - xs[0] - bw
        a1 = arr([xs[0] + bw / 2 + 0.03, y1], [xs[1] - bw / 2 - 0.03, y1], GREY, w=5, tip=0.16)
        a2 = arr([xs[1] + bw / 2 + 0.03, y1], [xs[2] - bw / 2 - 0.03, y1], GREY, w=5, tip=0.16)
        a3 = arr([xs[2], y1 - 0.75 - 0.03], [xs[2], y2 + 0.75 + 0.03], GREY, w=5, tip=0.2)
        a4 = arr([xs[2] - bw / 2 - 0.03, y2], [xs[1] + bw / 2 + 0.03, y2], GREY, w=5, tip=0.16)
        a5 = arr([xs[1] - bw / 2 - 0.03, y2], [xs[0] + bw / 2 + 0.03, y2], GREY, w=5, tip=0.16)
        self.play(FadeIn(h2), FadeIn(b1, shift=UP * 0.1), run_time=0.5)
        self.at("select mutant")
        self.play(GrowArrow(a1), FadeIn(b2), run_time=0.5)
        self.at("their descendants")
        self.play(GrowArrow(a2), FadeIn(b3), run_time=0.5)
        self.at("and sequencing")
        self.play(GrowArrow(a3), FadeIn(b4), run_time=0.5)
        self.at("pattern points")
        self.play(GrowArrow(a4), FadeIn(b5), run_time=0.5)
        self.at("Confirm with")
        self.play(GrowArrow(a5), FadeIn(b6), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """schematic SNP-frequency plot: mapping-strain alleles dip around the mutation; 2.13 Mb interval; vab-3."""

    def construct(self):
        ox, oy = -4.6, -2.1
        W, H = 7.0, 4.5

        def yv(v):
            return oy + 0.2 + v * (H - 0.5)
        ax_x = Line([ox, oy, 0], [ox + W, oy, 0], color=GREY, stroke_width=3)
        ax_y = Line([ox, oy, 0], [ox, oy + H, 0], color=GREY, stroke_width=3)
        ticks = VGroup()
        for v, t in ((0, "0"), (0.5, "0.5"), (1, "1")):
            ticks.add(M(t, 22, GREY).move_to([ox - 0.5, yv(v), 0]))
            ticks.add(Line([ox - 0.08, yv(v), 0], [ox, yv(v), 0], color=GREY, stroke_width=2))
        xl = lab("position along chromosome", 26, GREY).move_to([ox + W / 2, oy - 1.0, 0])
        yl = VGroup(T("fraction of mapping-strain", 22, GREY), T("(Hawaiian) SNP alleles", 22, GREY)).arrange(DOWN, buff=0.06).rotate(PI / 2).move_to([ox - 1.3, oy + H / 2, 0])
        xc = ox + W * 0.58
        ex = lab("example: idealised, schematic, not to scale", 26, GOLD).move_to([ox + W / 2 + 0.4, oy + H + 0.35, 0])

        def curve(s_, A, seed, color):
            r = np.random.RandomState(seed)
            xs = np.linspace(ox + 0.1, ox + W - 0.1, 150)
            ys = [yv(0.5) - A * np.exp(-((x - xc) / s_) ** 2) + r.randn() * 0.03 for x in xs]
            return poly(list(zip(xs, ys)), color, 4)

        self.at("Here is one real")
        self.play(Create(ax_x), Create(ax_y), FadeIn(ticks), FadeIn(xl), FadeIn(yl), FadeIn(ex), run_time=0.8)
        self.at("roughly equal frequency")
        flat = DashedLine([ox, yv(0.5), 0], [ox + W, yv(0.5), 0], color=GREEN, stroke_width=3)
        fl = lab("unlinked: about 0.5", 24, GREEN).move_to([ox + 1.6, yv(0.5) + 0.35, 0])
        self.play(Create(flat), FadeIn(fl), run_time=0.6)
        self.at("departure from that")
        c = curve(0.9, 1.75, 5, ORANGE)
        self.play(Create(c, run_time=1.4, rate_func=linear))
        dep = lab("departure: linkage", 24, ORANGE).move_to([ox + 1.8, yv(0.2), 0])
        self.play(FadeIn(dep), run_time=0.3)

        RX = 4.4
        self.at("Pooling 50")
        w50 = 2.0
        yy = oy - 0.4
        br = VGroup(Line([xc - w50 / 2, yy, 0], [xc + w50 / 2, yy, 0], color=YELLOW, stroke_width=5),
                    Line([xc - w50 / 2, yy + 0.14, 0], [xc - w50 / 2, yy - 0.14, 0], color=YELLOW, stroke_width=5),
                    Line([xc + w50 / 2, yy + 0.14, 0], [xc + w50 / 2, yy - 0.14, 0], color=YELLOW, stroke_width=5))
        t50 = lines("50 mutant recombinants", "41-fold coverage", "interval: 2.13 Mb", size=28, color=YELLOW, buff=0.1).move_to([RX, 1.7, 0])
        self.play(FadeOut(dep), Create(br), FadeIn(t50), run_time=0.7)
        self.at("The mutation was in")
        gene = VGroup(T("vab-3", 36, GREEN, weight=BOLD), T("worm ortholog of", 26, GREEN), T("Pax6 and Eyeless", 26, GREEN)).arrange(DOWN, buff=0.08)
        gene.move_to([RX, -0.7, 0])
        gb = SurroundingRectangle(gene, color=GREEN, buff=0.25, corner_radius=0.14, stroke_width=3)
        pk = Line([xc, yv(0.05) - 0.1, 0], [xc, yv(1.0), 0], color=GREEN, stroke_width=3).set_opacity(0.8)
        src = lab("Doitsidou and colleagues", 24, GOLD).move_to([RX, -2.6, 0])
        self.play(FadeIn(gene, shift=LEFT * 0.2), Create(gb), Create(pk), FadeIn(src), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """left: a screen's threshold misses a small defect; right: other lesions, backcross, rescue; complementation exceptions."""

    def construct(self):
        LX = -3.3
        RX = 3.4
        d = Line([0, 3.4, 0], [0, -3.4, 0], color=GREY, stroke_width=2).set_opacity(0.4)
        self.at("Two ways")
        self.play(Create(d), run_time=0.3)
        h1 = lab("1  What the assay can see", 30, TEXT, weight=BOLD).move_to([LX, 3.2, 0])
        h2 = lab("2  Background mutations", 30, TEXT, weight=BOLD).move_to([RX, 3.2, 0])
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.3)

        self.at("First an assay")
        base_y = -0.6
        L = [2.3, 1.55, 2.3, 2.3, 2.3, 2.15, 2.3]
        cols = [GREY, YELLOW, GREY, GREY, GREY, RED, GREY]
        bars = VGroup()
        for i, (l, c) in enumerate(zip(L, cols)):
            r = Rectangle(width=0.5, height=l, stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.3)
            r.move_to([LX - 2.1 + i * 0.8, base_y + l / 2, 0])
            bars.add(r)
        thr_y = base_y + 2.0
        exl = lab("example: fruit length", 26, GOLD).move_to([LX, 2.7, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.08), FadeIn(exl), run_time=0.7)
        self.at("detection threshold")
        thr = DashedLine([LX - 2.6, thr_y, 0], [LX + 2.6, thr_y, 0], color=ORANGE, stroke_width=3)
        thr_l = lab("detection threshold", 26, ORANGE).move_to([LX + 0.1, thr_y + 0.7, 0])
        self.play(Create(thr), FadeIn(thr_l), run_time=0.5)
        flag = lab("flagged", 24, YELLOW).move_to([bars[1].get_center()[0], base_y - 0.4, 0])
        miss = lines("small defect:", "missed", size=24, color=RED, align=ORIGIN, buff=0.04).move_to([bars[5].get_center()[0] + 0.1, base_y - 0.65, 0])
        self.play(FadeIn(flag), FadeIn(miss), run_time=0.5)
        self.at("choose a sensitive readout")
        ctl = lines("control: a sensitive readout,", "and state the criterion", size=28, color=GREEN, buff=0.08, align=ORIGIN).move_to([LX, -2.85, 0])
        self.play(FadeIn(ctl, shift=UP * 0.1), run_time=0.5)

        self.at("Second")
        w = 5.0
        by = 1.65
        bar = RoundedRectangle(corner_radius=0.14, width=w, height=0.36, stroke_color=BLUE, stroke_width=2,
                               fill_color=BLUE, fill_opacity=0.35).move_to([RX, by, 0])
        causal = Line([RX + 0.5, by - 0.35, 0], [RX + 0.5, by + 0.35, 0], color=YELLOW, stroke_width=8)
        others = VGroup(*[Line([RX + dx, by - 0.35, 0], [RX + dx, by + 0.35, 0], color=RED, stroke_width=6) for dx in (-2.1, -1.3, -0.1, 1.2, 2.1)])
        cl = lab("causal mutation", 26, YELLOW).move_to([RX + 0.5, by + 0.75, 0])
        ol = lab("other background mutations", 26, RED).move_to([RX, by - 0.75, 0])
        self.play(FadeIn(bar), FadeIn(causal), FadeIn(cl), run_time=0.4)
        self.play(FadeIn(others, scale=1.8), FadeIn(ol), run_time=0.5)
        self.at("Backcross")
        bc = lab("backcross: fewer remain, not none", 26, GREEN).move_to([RX, by - 0.75, 0])
        self.play(FadeOut(VGroup(others[0], others[1], others[4])), FadeOut(ol), run_time=0.5)
        self.play(FadeIn(bc), run_time=0.3)
        self.at("by complementation or rescue")
        rs = boxlab("test the candidate:", "complementation or rescue", color=GREEN, w=5.4, h=1.2, size=26).move_to([RX, -0.6, 0])
        self.play(FadeIn(rs, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tag(text, x, y, size=26):
    return lab(text, size, GOLD).move_to([x, y, 0])


class S07UnlockedA(SpokenScene):
    """segmentation loci and the spiny hedgehog larva; ced-3 and ced-4 and cells that survive."""

    def construct(self):
        LX, RX = -3.2, 3.5
        head1 = lab("segmentation", 34, TEXT, weight=BOLD).move_to([LX, 3.1, 0])
        normal = larva(4.8, 1.0, belts=(1, 1, 1, 1, 1), bc=TEXT, color=GREY).move_to([LX, 2.15, 0])
        nl = lab("normal", 26, GREY).move_to([LX, 1.35, 0])
        mutant = larva(4.8, 1.0, belts=(1, 0, 1, 0, 1), bc=YELLOW, color=YELLOW, fill=0.2).move_to([LX, 0.5, 0])
        ml = lab("altered segment pattern", 26, YELLOW).move_to([LX, -0.2, 0])
        spiny = larva(4.8, 1.0, belts=(1, 1, 1, 1, 1), bc=YELLOW, color=YELLOW, spines=7, fill=0.2).move_to([LX, -1.2, 0])
        sl = lab("spiny: named hedgehog", 26, YELLOW).move_to([LX, -1.95, 0])
        t1 = tag("Nüsslein-Volhard and Wieschaus, 1980", LX, -3.15, 24)
        rb = lab("genes unknown: random breaking", 26, RED).move_to([LX, 1.35, 0])

        self.at("In 1980")
        self.play(FadeIn(head1), FadeIn(normal), FadeIn(nl), FadeIn(t1), run_time=0.6)
        self.at("alter the larval")
        self.play(FadeIn(mutant, shift=UP * 0.1), FadeIn(ml), run_time=0.6)
        self.at("Random breaking was needed")
        self.play(FadeOut(nl), FadeIn(rb, shift=UP * 0.1), run_time=0.4)
        self.at("Hedgehog was named")
        self.play(FadeIn(spiny, shift=UP * 0.1), FadeIn(sl), run_time=0.6)

        head2 = lab("programmed cell death", 34, TEXT, weight=BOLD).move_to([RX, 3.1, 0])
        self.at("In 1986")
        self.play(FadeIn(head2), run_time=0.4)
        t2 = tag("Ellis and Horvitz, 1986", RX, -3.15, 26)
        wl = lab("wild-type worm: the cell dies", 26, GREY).move_to([RX, 1.4, 0])
        c1 = worm_cell(0.6, GREY).move_to([RX, 0.5, 0])
        ml2 = lab("ced-3 or ced-4 mutant", 26, YELLOW).move_to([RX, -0.55, 0])
        c2 = worm_cell(0.6, GREY).move_to([RX - 1.3, -1.5, 0])
        self.play(FadeIn(t2), FadeIn(wl), FadeIn(c1), run_time=0.5)
        self.at("required to start")
        req = lines("ced-3 and ced-4:", "needed to start the deaths", size=28, color=YELLOW, buff=0.06).move_to([RX, 2.35, 0])
        self.play(c1.animate.set_opacity(0.15), FadeIn(cross_x(c1.get_center(), 0.5, RED)), FadeIn(req), run_time=0.7)
        self.at("Cells that would die")
        sv = lines("survives and", "differentiates", size=28, color=GREEN, buff=0.06).move_to([RX + 1.3, -1.5, 0])
        self.play(FadeIn(ml2), FadeIn(c2), run_time=0.4)
        self.play(c2.animate.set_color(GREEN).set_fill(GREEN, 0.3), FadeIn(sv), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08UnlockedB(SpokenScene):
    """cdc mutants at low and high temperature; sec mutants pile up organelles; the closing rule."""

    def construct(self):
        LX, RX = -3.2, 3.5
        head1 = lab("cell cycle (yeast)", 34, TEXT, weight=BOLD).move_to([LX, 3.1, 0])
        t1 = tag("Hartwell and colleagues, 1973", LX, 2.5, 26)
        cold = lab("low temperature: cells grow", 28, GREEN).move_to([LX, 1.65, 0])
        cells_c = VGroup(yeast(0.5, 0.0), yeast(0.5, 0.55), yeast(0.5, 0.0)).arrange(RIGHT, buff=0.6).move_to([LX, 0.8, 0])
        hot = lab("high temperature: cells fail", 28, RED).move_to([LX, -0.15, 0])
        cells_h = VGroup(*[yeast(0.5, 0.8, RED) for _ in range(3)]).arrange(RIGHT, buff=0.5).move_to([LX, -1.0, 0])
        h28 = chip("CDC28: the handle on Start", ORANGE, 28).move_to([LX, -2.05, 0])
        stt = lines("Start: the point in G1 where", "a yeast cell commits to dividing", size=24, color=GREY, buff=0.06, align=ORIGIN).move_to([LX, -3.0, 0])

        self.at("In 1973")
        self.play(FadeIn(head1), FadeIn(t1), run_time=0.5)
        self.at("temperature sensitive")
        self.play(FadeIn(cells_c), run_time=0.5)
        self.at("grow at low")
        self.play(FadeIn(cold), run_time=0.4)
        self.at("fail at high")
        self.play(FadeIn(hot), FadeIn(cells_h), run_time=0.5)
        self.at("became the handle")
        self.play(FadeIn(h28, shift=UP * 0.1), FadeIn(stt), run_time=0.5)

        head2 = lab("secretion (yeast)", 34, TEXT, weight=BOLD).move_to([RX, 3.1, 0])
        t2 = tag("Novick, Field and Schekman, 1980", RX, 2.5, 26)
        cell = RoundedRectangle(corner_radius=0.7, width=3.8, height=2.2, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.08).move_to([RX - 0.6, 0.9, 0])
        org_pos = [(-1.0, 0.4), (-0.4, -0.5), (0.3, 0.5), (0.95, -0.2), (-0.65, 0.0), (0.5, -0.05)]
        orgs = VGroup(*[Circle(radius=0.24, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3).move_to([cell.get_center()[0] + x, cell.get_center()[1] + y, 0]) for x, y in org_pos])
        hot2 = M("37 °C", 32, RED).move_to([RX + 2.4, 0.9, 0])
        pile = lines("membrane-enclosed organelles", "pile up in most mutants", size=26, color=PURPLE, buff=0.06).move_to([RX, -0.7, 0])
        cons = lines("conditional mutants:", "secretion is essential", size=28, color=GREY, buff=0.08).move_to([RX, -1.8, 0])

        self.at("In 1980")
        self.play(FadeIn(head2), FadeIn(t2), FadeIn(cell), run_time=0.5)
        self.at("of which accumulate")
        self.play(FadeIn(orgs, scale=0.4), FadeIn(hot2), run_time=0.6)
        self.play(FadeIn(pile), run_time=0.4)
        self.at("Conditional mutants")
        self.play(FadeIn(cons), run_time=0.5)

        self.at("Keep this rule")
        everything = VGroup(head1, t1, cold, cells_c, hot, cells_h, h28, stt, head2, t2, cell, orgs, hot2, pile, cons)
        r1 = T("A screen finds only what its assay can see.", 42, TEXT, font=TITLE_FONT)
        box = SurroundingRectangle(r1, color=GOLD, buff=0.5, stroke_width=4, corner_radius=0.2)
        self.play(FadeOut(everything), FadeIn(r1, shift=UP * 0.15), Create(box), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A screen finds only what its assay can see."
