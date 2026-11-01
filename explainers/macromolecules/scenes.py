"""Macromolecules: small blocks build living things  (Biochemistrypedia high school Biology explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
Nothing here is a molecular structure: blocks, chips, bars and arrows only.

COLOR MAP (one color per concept, whole video)
  TEAL   = a monomer / a generic building block, and the chains made of it
  BLUE   = water
  GREEN  = joining (dehydration synthesis, the new link)
  RED    = splitting (hydrolysis)
  ORANGE = carbohydrates (simple sugars, cellulose)
  PURPLE = proteins (amino acids, enzyme)
  PINK   = nucleic acids (nucleotides, DNA strands)
  YELLOW = lipids (fatty acids, glycerol, phospholipid)
  GOLD   = "shape decides the job"
  GREY   = outlines, links, food and body blocks, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FC0"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG, fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def blk(color=TEAL, s=0.6, op=0.25):
    """one building block: an opaque backing plus a coloured outline (a schematic bead, never a structure)."""
    back = RoundedRectangle(corner_radius=0.08, width=s, height=s, stroke_width=0, fill_color=BG, fill_opacity=1)
    front = RoundedRectangle(corner_radius=0.08, width=s, height=s, stroke_color=color, stroke_width=2.5,
                             fill_color=color, fill_opacity=op)
    g = VGroup(back, front)
    g.set_z_index(2)
    return g


def link(a, b, color=GREY, w=4):
    l = Line(a.get_center(), b.get_center(), color=color, stroke_width=w)
    l.add_updater(lambda m, a=a, b=b: m.put_start_and_end_on(a.get_center(), b.get_center()))
    l.set_z_index(1)
    return l


class Chain:
    def __init__(self, pts, color=TEAL, s=0.6, ops=None):
        self.blocks = [blk(color, s, ops[i] if ops else 0.25).move_to([p[0], p[1], 0]) for i, p in enumerate(pts)]
        self.links = [link(a, b) for a, b in zip(self.blocks, self.blocks[1:])]
        self.group = VGroup(*self.links, *self.blocks)

    def build(self, lag=0.2):
        anims = []
        for i, b in enumerate(self.blocks):
            parts = [FadeIn(b, scale=0.6)]
            if i > 0:
                parts.insert(0, FadeIn(self.links[i - 1]))
            anims.append(AnimationGroup(*parts))
        return LaggedStart(*anims, lag_ratio=lag)


def row_pts(n, x0, y, gap):
    return [(x0 + i * gap, y) for i in range(n)]


class S00Title(TitleCard):
    LESSON = "What am I made of?"
    TITLE = "Small blocks build living things"


# ---------------------------------------------------------------------------------------------
class S01Sandwich(SpokenScene):
    """a sandwich beside a body made of cells: what are cells made of?"""

    def construct(self):
        ys = [1.15, 0.0, -1.15]
        bars = [RoundedRectangle(corner_radius=0.15, width=4.4, height=1.0, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.22).move_to([-4.0, y, 0]) for y in ys]
        lab_b1 = T("bread: wheat plants", 26, TEXT).move_to(bars[0])
        lab_t = T("turkey: a bird", 26, TEXT).move_to(bars[1])
        lab_b2 = T("bread: wheat plants", 26, TEXT).move_to(bars[2])
        title = T("a turkey sandwich", 28, GREY).move_to([-4.0, 2.25, 0])
        self.at("turkey sandwich")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in bars], lag_ratio=0.25), FadeIn(title), run_time=1.0)

        body = RoundedRectangle(corner_radius=0.2, width=4.4, height=4.2, stroke_color=TEXT, stroke_width=3).move_to([4.0, 0, 0])
        body_t = T("your body", 30, TEXT).move_to([4.0, 2.5, 0])
        ar = arr([-1.6, 0, 0], [1.5, 0, 0], GREY)
        self.at("part of you")
        self.play(GrowArrow(ar), Create(body), FadeIn(body_t), run_time=1.0)

        self.at("wheat plants")
        self.play(FadeIn(lab_b1), FadeIn(lab_b2), run_time=0.6)
        self.at("a bird")
        self.play(FadeIn(lab_t), run_time=0.6)

        cells = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.0, height=0.9, stroke_color=GREY, stroke_width=2.5,
                                          fill_color=GREY, fill_opacity=0.2).move_to([4.0 + dx, dy + 0.1, 0])
                         for dy in (1.1, 0.0, -1.1) for dx in (-1.25, 0.0, 1.25)])
        cap = T("cells", 24, GREY).move_to([4.0, -1.78, 0])
        self.at("body is made")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in cells], lag_ratio=0.08), FadeIn(cap), run_time=1.1)

        q = T("What are cells made of?", 38, GOLD, font=TITLE_FONT).move_to([0, 3.15, 0])
        qs = VGroup(*[T("?", 34, GOLD, weight=BOLD).move_to(c) for c in cells])
        self.at("what are cells")
        self.play(Write(q), LaggedStart(*[FadeIn(m, scale=0.5) for m in qs], lag_ratio=0.06), run_time=1.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
def necklace_pts(n=9):
    xs = np.linspace(-5.2, 5.2, n)
    return [(x, 2.0 * (x / 5.2) ** 2 - 1.2) for x in xs]


def fold_pts():
    out = []
    for r, y in enumerate((1.6, 0.0, -1.6)):
        xs = [-2.4, 0, 2.4] if r % 2 == 0 else [2.4, 0, -2.4]
        out += [(x, y) for x in xs]
    return out


def coil_pts(n=9, rad=2.0, cy=0.2):
    return [(rad * np.cos(np.radians(90 - 40 * i)), cy + rad * np.sin(np.radians(90 - 40 * i))) for i in range(n)]


class S02Chain(SpokenScene):
    """beads on a string -> monomer, polymer -> the chain folds, coils, branches."""

    def construct(self):
        ch = Chain(necklace_pts(), TEAL, 0.8)
        self.at("necklace of beads")
        self.play(ch.build(0.22), run_time=2.2)

        mono_lab = T("monomer", 34, TEXT, weight=BOLD).move_to([0, -2.85, 0])
        mono_ar = arr([0, -2.45, 0], [0, -1.7, 0], TEXT)
        self.at("A monomer")
        self.play(FadeIn(mono_lab), GrowArrow(mono_ar),
                  *[b[1].animate.set_stroke(opacity=0.3).set_fill(opacity=0.06) for i, b in enumerate(ch.blocks) if i != 4],
                  Indicate(ch.blocks[4][1], color=TEAL, scale_factor=1.3), run_time=0.9)

        brace = Brace(ch.group, direction=UP, color=TEAL, buff=0.3)
        poly_lab = T("polymer", 34, TEAL, weight=BOLD).next_to(brace, UP, buff=0.15)
        self.at("A polymer")
        self.play(FadeOut(mono_lab), FadeOut(mono_ar), *[b[1].animate.set_stroke(opacity=1).set_fill(opacity=0.25) for i, b in enumerate(ch.blocks) if i != 4],
                  GrowFromCenter(brace), FadeIn(poly_lab), run_time=1.0)

        self.at("Real chains fold")
        fold_t = T("fold", 34, TEXT, weight=BOLD).move_to([-5.2, 0, 0])
        coil_t = T("coil", 34, TEXT, weight=BOLD).move_to([-5.2, 0.2, 0])
        self.play(FadeOut(brace), FadeOut(poly_lab), FadeIn(fold_t),
                  *[b.animate.move_to([p[0], p[1], 0]) for b, p in zip(ch.blocks, fold_pts())], run_time=0.9)
        self.at("coil")
        self.play(FadeOut(fold_t), FadeIn(coil_t),
                  *[b.animate.move_to([p[0], p[1], 0]) for b, p in zip(ch.blocks, coil_pts())], run_time=0.8)
        self.at("branch")
        cp = coil_pts()
        x2, y2 = cp[2]
        e1 = blk(TEAL, 0.8).move_to([x2 + 1.3, y2, 0])
        e2 = blk(TEAL, 0.8).move_to([x2 + 2.6, y2, 0])
        l1, l2 = link(ch.blocks[2], e1), link(e1, e2)
        branch_t = T("branch", 34, TEXT, weight=BOLD).move_to([-5.2, 0.2, 0])
        self.play(FadeOut(coil_t), FadeIn(branch_t), FadeIn(l1), FadeIn(e1, shift=RIGHT * 0.3), FadeIn(l2), FadeIn(e2, shift=RIGHT * 0.3), run_time=0.7)

        shape = T("shape matters for the job", 38, GOLD, font=TITLE_FONT).move_to([0, -3.05, 0])
        self.at("shape matters")
        self.play(FadeOut(branch_t), FadeIn(shape, shift=UP * 0.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Water(SpokenScene):
    """two monomers join: H and OH leave as water (dehydration synthesis); water returns and splits them (hydrolysis)."""

    def construct(self):
        def mono(side):
            r = RoundedRectangle(corner_radius=0.2, width=3.0, height=1.8, stroke_color=TEAL, stroke_width=3.5,
                                 fill_color=TEAL, fill_opacity=0.22)
            return VGroup(r, T("monomer", 30, TEAL).move_to(r.get_center() + [-0.3 * side, 0, 0]))
        Y = 0.3
        A = mono(1).move_to([-3.7, Y, 0])
        B = mono(-1).move_to([3.7, Y, 0])
        self.at("link two monomers")
        self.play(FadeIn(A, shift=RIGHT * 0.3), FadeIn(B, shift=LEFT * 0.3), run_time=0.9)

        H = bchip("H", BLUE, 32).move_to([A[0].get_right()[0], Y, 0])
        OH = bchip("OH", BLUE, 32).move_to([B[0].get_left()[0], Y, 0])
        self.at("a hydrogen from one")
        self.play(FadeIn(H, scale=0.6), run_time=0.5)
        self.play(Indicate(H, color=BLUE, scale_factor=1.25), run_time=0.5)
        self.at("oxygen and a hydrogen")
        self.play(FadeIn(OH, scale=0.6), run_time=0.5)
        self.play(Indicate(OH, color=BLUE, scale_factor=1.25), run_time=0.5)

        self.at("leave together")
        self.play(H.animate.move_to([-0.6, 2.3, 0]), OH.animate.move_to([0.6, 2.3, 0]),
                  A.animate.move_to([-1.5, Y, 0]), B.animate.move_to([1.5, Y, 0]), run_time=1.2)
        water = bchip("water", BLUE, 32).move_to([0, 2.3, 0])
        newlink = Rectangle(width=0.18, height=1.4, stroke_width=0, fill_color=GREEN, fill_opacity=1).move_to([0, Y, 0])
        newlink.set_z_index(3)
        link_t = T("new link", 26, GREEN).move_to([0, Y - 1.25, 0])
        self.at("one water molecule")
        self.play(ReplacementTransform(VGroup(H, OH), water), FadeIn(newlink), FadeIn(link_t), run_time=0.8)
        self.play(water.animate.move_to([4.6, 2.4, 0]), run_time=0.8)

        d_ar = arr([-5.9, -2.4, 0], [-4.6, -2.4, 0], GREEN)
        d_t = T("dehydration synthesis", 36, GREEN, weight=BOLD).move_to([-1.55, -2.4, 0])
        d_grp = VGroup(d_ar, d_t)
        d_sub = T("making something by removing water", 28, GREY).move_to([0, -3.15, 0])
        self.at("dehydration synthesis")
        self.play(GrowArrow(d_ar), FadeIn(d_t), run_time=0.7)
        self.at("making something")
        self.play(FadeIn(d_sub), run_time=0.6)

        h_ar = arr([5.6, -2.4, 0], [4.4, -2.4, 0], RED)
        h_t = T("hydrolysis", 36, RED, weight=BOLD).move_to([2.9, -2.4, 0])
        self.at("The reverse")
        self.play(FadeOut(d_sub), d_grp.animate.scale(0.6).move_to([-3.9, -2.4, 0]).set_opacity(0.45),
                  GrowArrow(h_ar), FadeIn(h_t), run_time=0.8)
        poly_t = T("polymer", 30, TEAL).move_to([0, 1.55, 0])
        self.at("splits a polymer")
        self.play(FadeIn(poly_t), run_time=0.4)
        self.at("adding water")
        self.play(water.animate.move_to([0, 2.4, 0]), run_time=0.7)
        self.play(FadeOut(water), FadeOut(newlink), FadeOut(link_t), FadeOut(poly_t),
                  A.animate.move_to([-3.7, Y, 0]), B.animate.move_to([3.7, Y, 0]), run_time=1.0)
        pcs = T("smaller pieces", 30, GREY).move_to([0, Y, 0])
        self.play(FadeIn(pcs), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Classes(SpokenScene):
    """four classes: name, building blocks as a short chain, main job."""

    def construct(self):
        ys = [2.6, 1.0, -0.6, -2.5]
        JX = 4.0

        def head(name, color, y):
            return bchip(name, color, 28).move_to([-4.7, y, 0])

        def mini_chain(color, y):
            ch = Chain(row_pts(4, -2.5, y, 0.8), color, 0.5)
            dots = VGroup(*[Dot(radius=0.04, color=GREY).move_to([0.2 + 0.18 * k, y, 0]) for k in range(3)])
            return ch, dots

        def lbl(text, color, y):
            return T(text, 24, color).move_to([-1.1, y - 0.62, 0])

        def job(text, y):
            return T(text, 26, TEXT, line_spacing=0.8).move_to([JX, y, 0])

        self.at("four classes")
        # --- carbohydrates
        h1 = head("Carbohydrates", ORANGE, ys[0])
        self.at("Carbohydrates are made")
        self.play(FadeIn(h1, shift=RIGHT * 0.2), run_time=0.5)
        c1, d1 = mini_chain(ORANGE, ys[0])
        l1 = lbl("simple sugars", ORANGE, ys[0])
        self.at("simple sugars")
        self.play(c1.build(0.2), FadeIn(d1), FadeIn(l1), run_time=1.0)
        j1 = job("quick energy", ys[0])
        self.at("quick energy")
        self.play(FadeIn(j1, shift=LEFT * 0.2), run_time=0.5)
        # --- proteins
        h2 = head("Proteins", PURPLE, ys[1])
        self.at("Proteins are chains")
        self.play(FadeIn(h2, shift=RIGHT * 0.2), run_time=0.5)
        c2, d2 = mini_chain(PURPLE, ys[1])
        l2 = lbl("amino acids", PURPLE, ys[1])
        self.at("amino acids")
        self.play(c2.build(0.2), FadeIn(d2), FadeIn(l2), run_time=1.0)
        j2 = job("build tissues and\nrun cell processes", ys[1])
        self.at("build tissues")
        self.play(FadeIn(j2, shift=LEFT * 0.2), run_time=0.5)
        # --- nucleic acids
        h3 = head("Nucleic acids", PINK, ys[2])
        self.at("Nucleic acids")
        self.play(FadeIn(h3, shift=RIGHT * 0.2), run_time=0.5)
        c3, d3 = mini_chain(PINK, ys[2])
        l3 = lbl("nucleotides", PINK, ys[2])
        self.at("of nucleotides")
        self.play(c3.build(0.2), FadeIn(d3), FadeIn(l3), run_time=1.0)
        j3 = job("store and pass on\ngenetic information", ys[2])
        self.at("pass on")
        self.play(FadeIn(j3, shift=LEFT * 0.2), run_time=0.5)
        # --- lipids
        h4 = head("Lipids", YELLOW, ys[3])
        self.at("Lipids mostly")
        self.play(FadeIn(h4, shift=RIGHT * 0.2), run_time=0.5)
        y = ys[3]
        gly = RoundedRectangle(corner_radius=0.08, width=0.5, height=1.25, stroke_color=YELLOW, stroke_width=2.5,
                               fill_color=YELLOW, fill_opacity=0.25).move_to([-2.7, y, 0])
        bars = VGroup(*[RoundedRectangle(corner_radius=0.06, width=1.5, height=0.28, stroke_color=YELLOW, stroke_width=2.5,
                                         fill_color=YELLOW, fill_opacity=0.25).move_to([-1.5, y + dy, 0])
                        for dy in (0.45, 0.0, -0.45)])
        ties = VGroup(*[Line([-2.45, y + dy, 0], [-2.25, y + dy, 0], color=GREY, stroke_width=4) for dy in (0.45, 0.0, -0.45)])
        fa_t = T("fats: glycerol +\nfatty acids", 24, YELLOW, line_spacing=0.8).move_to([0.9, y, 0])
        self.at("fatty acids and glycerol")
        self.play(FadeIn(gly), FadeIn(ties), LaggedStart(*[FadeIn(b, shift=LEFT * 0.2) for b in bars], lag_ratio=0.2),
                  FadeIn(fa_t), run_time=1.1)
        j4 = job("store energy for\na long time", y)
        self.at("long time")
        self.play(FadeIn(j4, shift=LEFT * 0.2), run_time=0.5)
        three = T("one glycerol +\nthree fatty acids", 24, YELLOW, line_spacing=0.8).move_to([1.1, y, 0])
        self.at("one glycerol joined")
        self.play(Indicate(gly, color=YELLOW, scale_factor=1.15), ReplacementTransform(fa_t, three), run_time=0.9)
        self.play(Indicate(bars, color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Shape(SpokenScene):
    """shape decides the job: a key and lock, then one example per class."""

    def construct(self):
        # --- key and lock
        socket = Difference(Rectangle(width=4.2, height=3.0), Rectangle(width=1.5, height=1.3).move_to([0, 1.0, 0]),
                            stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.18).move_to([2.0, -0.5, 0])
        piece = Rectangle(width=1.4, height=1.2, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.5).move_to([-3.4, 1.4, 0])
        head = T("Shape decides the job", 44, GOLD, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("Shape decides")
        self.play(Write(head), FadeIn(socket), FadeIn(piece), run_time=1.2)
        self.at("key in a lock")
        self.play(piece.animate.move_to([2.0, 0.7, 0]), run_time=1.3)

        # --- four panels
        PW, PH = 5.9, 3.15
        centers = [(-3.2, 1.75), (3.2, 1.75), (-3.2, -1.75), (3.2, -1.75)]
        cols = [ORANGE, PURPLE, PINK, YELLOW]
        names = ["cellulose: a carbohydrate", "an enzyme: a protein", "DNA: a nucleic acid", "phospholipid: a lipid"]

        def panel(i):
            cx, cy = centers[i]
            fr = RoundedRectangle(corner_radius=0.18, width=PW, height=PH, stroke_color=cols[i], stroke_width=2.5).move_to([cx, cy, 0])
            tt = T(names[i], 24, cols[i], weight=BOLD).move_to([cx, cy + 1.28, 0])
            return fr, tt

        # panel 1: cellulose
        fr, tt = panel(0)
        cx, cy = centers[0]
        self.at("Cellulose chains")
        self.play(FadeOut(VGroup(head, socket, piece)), FadeIn(fr), FadeIn(tt), run_time=0.7)
        chains = [Chain(row_pts(6, cx - 1.4, cy + 0.65 - 0.5 * r, 0.56), ORANGE, 0.36) for r in range(3)]
        self.play(*[c.build(0.1) for c in chains], run_time=1.0)
        self.at("strong fibers")
        self.play(*[Indicate(c.group, color=ORANGE, scale_factor=1.05) for c in chains], run_time=0.8)
        fiber_t = T("strong fibers", 24, ORANGE).move_to([cx, cy - 1.15, 0])
        self.play(FadeIn(fiber_t), run_time=0.4)
        wall = SurroundingRectangle(VGroup(*[c.group for c in chains]), color=GREY, buff=0.2, stroke_width=5, corner_radius=0.1)
        wall_t = T("plant cell wall", 24, GREY).move_to([cx, cy - 1.15, 0])
        self.at("plant cell walls")
        self.play(Create(wall), ReplacementTransform(fiber_t, wall_t), run_time=0.9)

        # panel 2: enzyme
        fr2, tt2 = panel(1)
        cx, cy = centers[1]
        ex = cx - 0.6
        enz = Difference(RoundedRectangle(corner_radius=0.3, width=2.6, height=1.35),
                         Circle(radius=0.5).move_to([0, 0.675, 0]),
                         stroke_color=PURPLE, stroke_width=3.5, fill_color=PURPLE, fill_opacity=0.3).move_to([ex, cy - 0.4, 0])
        enz_t = T("enzyme", 26, PURPLE).move_to([ex, cy - 0.5, 0])
        self.at("An enzyme")
        self.play(FadeIn(fr2), FadeIn(tt2), FadeIn(enz), FadeIn(enz_t), run_time=0.8)
        pk_t = T("folded pocket", 24, PURPLE).move_to([cx + 1.8, cy + 0.75, 0])
        pk_ar = arr([cx + 1.2, cy + 0.6, 0], [ex + 0.45, cy + 0.3, 0], PURPLE, w=3, tip=0.18)
        self.at("folded pocket")
        self.play(GrowArrow(pk_ar), FadeIn(pk_t), run_time=0.7)
        mol = Sector(radius=0.44, angle=PI, start_angle=PI, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.3).move_to([cx - 2.2, cy + 1.2, 0])
        mol_t = T("one kind of molecule", 24, TEXT).move_to([ex, cy - 1.3, 0])
        self.at("one kind of molecule")
        self.play(FadeIn(mol), run_time=0.4)
        self.play(mol.animate.move_to([ex, cy + 0.275 - 0.22, 0]), FadeOut(pk_ar), FadeIn(mol_t), run_time=1.0)

        # panel 3: DNA, two parallel bars with matching blocks
        fr3, tt3 = panel(2)
        cx, cy = centers[2]
        sx = cx - 0.4
        top = RoundedRectangle(corner_radius=0.08, width=3.8, height=0.2, stroke_color=PINK, stroke_width=2.5, fill_color=PINK, fill_opacity=0.5).move_to([sx, cy + 0.55, 0])
        bot = RoundedRectangle(corner_radius=0.08, width=3.8, height=0.2, stroke_color=PINK, stroke_width=2.5, fill_color=PINK, fill_opacity=0.5).move_to([sx, cy - 0.45, 0])
        hs = [0.5, 0.2, 0.5, 0.2, 0.2, 0.5]
        xs = [sx - 1.5 + 0.6 * k for k in range(6)]
        tops = VGroup(*[Rectangle(width=0.3, height=h, stroke_width=0, fill_color=PINK, fill_opacity=0.9).move_to([x, cy + 0.45 - h / 2, 0]) for x, h in zip(xs, hs)])
        bots = VGroup(*[Rectangle(width=0.3, height=0.7 - h, stroke_width=0, fill_color=PINK, fill_opacity=0.45).move_to([x, cy - 0.35 + (0.7 - h) / 2, 0]) for x, h in zip(xs, hs)])
        s_t1 = T("strand", 24, PINK).move_to([cx + 2.15, cy + 0.55, 0])
        s_t2 = T("strand", 24, PINK).move_to([cx + 2.15, cy - 0.45, 0])
        self.at("two strands")
        self.play(FadeIn(fr3), FadeIn(tt3), FadeIn(top), FadeIn(bot), FadeIn(s_t1), FadeIn(s_t2), run_time=0.8)
        self.play(FadeIn(tops, lag_ratio=0.1), run_time=0.6)
        fixed_t = T("bases pair in a fixed way", 26, TEXT).move_to([cx, cy - 1.1, 0])
        self.at("pair in a fixed way")
        self.play(FadeIn(bots, lag_ratio=0.12), FadeIn(fixed_t), run_time=1.0)

        # panel 4: phospholipid
        fr4, tt4 = panel(3)
        cx, cy = centers[3]

        def phos(x, y, up=True, s=1.0):
            hd = Circle(radius=0.2 * s, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.6).move_to([x, y, 0])
            d = -1 if up else 1
            t1 = Line([x - 0.09 * s, y + d * 0.2 * s, 0], [x - 0.09 * s, y + d * 0.2 * s + d * 0.38 * s, 0], color=YELLOW, stroke_width=4)
            t2 = Line([x + 0.09 * s, y + d * 0.2 * s, 0], [x + 0.09 * s, y + d * 0.2 * s + d * 0.38 * s, 0], color=YELLOW, stroke_width=4)
            return VGroup(t1, t2, hd)
        one = phos(cx - 1.6, cy - 0.1, True, 1.8)
        head_t = T("head: attracted to water", 24, YELLOW).move_to([cx + 0.75, cy + 0.0, 0])
        tail_t = T("two tails", 24, YELLOW).move_to([cx - 0.45, cy - 0.8, 0])
        self.at("A phospholipid")
        self.play(FadeIn(fr4), FadeIn(tt4), FadeIn(one), run_time=0.8)
        self.at("head attracted to water")
        self.play(FadeIn(head_t), run_time=0.5)
        self.at("two tails")
        self.play(FadeIn(tail_t), run_time=0.5)
        xs4 = [cx - 2.2 + 0.55 * k for k in range(5)]
        toprow = VGroup(*[phos(x, cy + 0.3, True) for x in xs4])
        botrow = VGroup(*[phos(x, cy - 0.95, False) for x in xs4])
        w1 = T("water", 22, BLUE).move_to([cx - 1.1, cy + 0.88, 0])
        w2 = T("water", 22, BLUE).move_to([cx - 1.1, cy - 1.35, 0])
        self.at("In water")
        self.play(FadeOut(VGroup(one, head_t, tail_t)), FadeIn(w1), FadeIn(w2), run_time=0.6)
        self.at("double layer")
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in toprow], lag_ratio=0.08),
                  LaggedStart(*[FadeIn(p, scale=0.6) for p in botrow], lag_ratio=0.08), run_time=1.2)
        mem_t = T("cell\nmembrane", 24, TEXT, line_spacing=0.8).move_to([cx + 1.9, cy - 0.3, 0])
        self.at("basic structure")
        self.play(FadeIn(mem_t), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """sandwich -> pieces -> new chains; a turkey protein is rebuilt as yours; four classes build every part of a living thing."""

    def construct(self):
        sand = bchip("sandwich", GREY, 30).move_to([-5.2, 0.4, 0])
        self.at("sandwich become")
        self.play(FadeIn(sand, scale=0.8), run_time=0.7)

        ys = [2.0, 0.55, -0.9, -2.5]
        names = ["simple sugars", "amino acids", "parts of nucleotides", "fatty acids"]
        cols = [ORANGE, PURPLE, PINK, YELLOW]
        pieces = [bchip(n, c, 24).move_to([-0.6, y, 0]) for n, c, y in zip(names, cols, ys)]
        head_p = T("small pieces", 26, GREY).move_to([-0.6, 3.1, 0])
        sp_ar = [arr([-4.1, 0.4, 0], [-2.8, y, 0], GREY, w=3, tip=0.16) for y in ys]
        self.at("Digestion splits")
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(p, shift=RIGHT * 0.2)) for a, p in zip(sp_ar, pieces)],
                              lag_ratio=0.25), FadeIn(head_p), run_time=1.6)

        chains = []
        for c, y in zip(cols[:3], ys[:3]):
            chains.append(Chain(row_pts(4, 3.0, y, 0.75), c, 0.5))
        gy = ys[3]
        gly = RoundedRectangle(corner_radius=0.08, width=0.45, height=1.2, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.25).move_to([3.0, gy, 0])
        fas = VGroup(*[RoundedRectangle(corner_radius=0.06, width=1.5, height=0.26, stroke_color=YELLOW, stroke_width=2.5, fill_color=YELLOW, fill_opacity=0.25).move_to([4.1, gy + dy, 0]) for dy in (0.42, 0, -0.42)])
        fat = VGroup(gly, fas, *[Line([3.22, gy + dy, 0], [3.35, gy + dy, 0], color=GREY, stroke_width=4) for dy in (0.42, 0, -0.42)])
        head_n = T("new large molecules", 26, GREY).move_to([4.3, 3.1, 0])
        jar = [arr([1.6, y, 0], [2.4, y, 0], GREEN, w=4, tip=0.16) for y in ys]
        self.at("Your cells use")
        self.play(FadeIn(head_n), LaggedStart(*[AnimationGroup(GrowArrow(a)) for a in jar], lag_ratio=0.2), run_time=0.8)
        self.play(*[c.build(0.2) for c in chains], FadeIn(fat), run_time=1.2)

        # --- turkey protein rebuilt as yours
        self.at("A turkey protein")
        self.play(FadeOut(VGroup(sand, head_p, head_n, *pieces, *sp_ar, *jar, *[c.group for c in chains], fat)), run_time=0.7)
        ops = [0.2, 0.45, 0.7, 0.95, 0.35, 0.6]
        top = Chain(row_pts(6, -2.75, 1.4, 1.1), PURPLE, 0.7, ops)
        top_t = T("turkey protein", 28, PURPLE).move_to([0, 2.45, 0])
        self.play(FadeIn(top_t), top.build(0.15), run_time=1.0)
        self.at("amino acids are reused")
        new_order = [3, 0, 5, 1, 4, 2]
        slots = row_pts(6, -2.75, -1.4, 1.1)
        bot = Chain(slots, PURPLE, 0.7, [ops[i] for i in new_order])
        bot_t = T("your protein", 28, PURPLE).move_to([0, -2.45, 0])
        mid = T("same amino acids, new chain", 26, GREY).move_to([0, 0, 0])
        self.play(*[FadeOut(l) for l in top.links], run_time=0.5)
        self.play(*[top.blocks[old].animate.move_to([slots[k][0], slots[k][1], 0]) for k, old in enumerate(new_order)],
                  FadeOut(top_t), FadeIn(mid), run_time=1.4)
        self.play(*[FadeIn(l) for l in bot.links], FadeIn(bot_t), run_time=0.6)

        # --- four classes
        self.at("Four kinds")
        self.play(FadeOut(VGroup(*top.blocks, *bot.links, bot_t, mid)), run_time=0.7)
        chips = VGroup(*[bchip(n, c, 32) for n, c in zip(["Carbohydrates", "Proteins", "Nucleic acids", "Lipids"], cols)])
        chips.arrange(RIGHT, buff=0.3).move_to([0, 2.4, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in chips], lag_ratio=0.2), run_time=1.0)
        icons, subs = VGroup(), VGroup()
        for k, (n, c, ch) in enumerate(zip(names, cols, chips)):
            x = ch.get_center()[0]
            if k < 3:
                ic = Chain(row_pts(3, x - 0.55, 1.2, 0.55), c, 0.4)
                icons.add(ic.group)
            else:
                g0 = RoundedRectangle(corner_radius=0.06, width=0.3, height=0.9, stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.25).move_to([x - 0.6, 1.2, 0])
                bs = [RoundedRectangle(corner_radius=0.05, width=0.9, height=0.2, stroke_color=c, stroke_width=2.5, fill_color=c, fill_opacity=0.25).move_to([x + 0.15, 1.2 + dy, 0]) for dy in (0.3, 0, -0.3)]
                icons.add(VGroup(g0, *bs))
            subs.add(T(n.replace(" + ", "\n+ "), 24, c, line_spacing=0.8).move_to([x, 0.3, 0]))
        self.at("small set")
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.1) for g in icons], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in subs], lag_ratio=0.2), run_time=1.2)
        brace = Brace(VGroup(chips, icons, subs), direction=DOWN, color=GREY, buff=0.25)
        every = T("every part of a living thing", 44, TEXT, font=TITLE_FONT).next_to(brace, DOWN, buff=0.35)
        self.at("every part")
        self.play(GrowFromCenter(brace), FadeIn(every, shift=UP * 0.15), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "Four kinds of large molecule make every part of a living thing."
