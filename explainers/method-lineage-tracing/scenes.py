"""Lineage tracing: mark one cell, read its family  (Biochemistrypedia methods film)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  ORANGE = the mark and everything that carries it (tracer, insert, lit reporter, barcode, a clone)
  BLUE   = the tool the experimenter adds (pipette, virus, Cre)
  GREY   = ordinary cells, structure, labels
  TEAL   = the inducer drug (tamoxifen, dexamethasone, low dose)
  RED    = the trap: a stop, a leak, a blocked path, a doubt
  GREEN  = a control that catches a trap
  YELLOW = a change or a question being asked (cohort ring, a mutation, "?")
  GOLD   = dates' source tags and the closing rule
  Shapes (circle, square, triangle, diamond) = four cell types.
  Multicolour parts only (s04, s05): four or many arbitrary hues, labelled as random colours.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
CF = ["#E66AA8", "#4FD1C5", "#F5D547", "#8E7CFF"]   # four arbitrary reporter colours


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def lab(text, size=24, color=GREY, **kw):
    return T(text, size, color, **kw)


def P(x, y):
    return np.array([x, y, 0.0])


def arr(a, b, color=GREY, w=4, tip=0.18):
    return Arrow(P(*a), P(*b), buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def shp(kind, pos, r=0.34, color=GREY, fill=0.12, fc=None, w=3):
    fc = fc or color
    if kind == "c":
        m = Circle(radius=r)
    elif kind == "s":
        m = Square(side_length=1.7 * r)
    elif kind == "t":
        m = Triangle().scale(r * 1.2)
    else:
        m = Square(side_length=1.6 * r).rotate(PI / 4)
    m.set_stroke(color, w).set_fill(fc, fill).move_to(P(*pos))
    return m


def cell(pos, r=0.34, color=GREY, fc=None, fill=0.12, w=3):
    return Circle(radius=r, stroke_color=color, stroke_width=w, fill_color=fc or color, fill_opacity=fill).move_to(P(*pos))


def lit(m):
    """Turn a cell into a marked (orange) cell."""
    return m.animate.set_fill(ORANGE, 0.85).set_stroke(ORANGE, 3)


def xmark(pos, s=0.2, color=RED, w=5):
    return VGroup(Line(P(pos[0] - s, pos[1] - s), P(pos[0] + s, pos[1] + s), color=color, stroke_width=w),
                  Line(P(pos[0] - s, pos[1] + s), P(pos[0] + s, pos[1] - s), color=color, stroke_width=w))


def pipette(tip, h=1.3, tip_w=0.16, top_w=0.55, fill=None):
    tx, ty = tip
    L, R = P(tx - tip_w / 2, ty), P(tx + tip_w / 2, ty)
    UL, UR = P(tx - top_w / 2, ty + h), P(tx + top_w / 2, ty + h)
    f = Polygon(L, R, UR, UL, stroke_width=0, fill_color=fill or BLUE, fill_opacity=0.5 if fill else 0.1)
    return VGroup(f, Line(UL, L, color=BLUE, stroke_width=5), Line(UR, R, color=BLUE, stroke_width=5))


def barcode(pos, cols=None, n=5):
    cols = cols or [ORANGE] * n
    g = VGroup(*[Rectangle(width=0.11, height=0.32, stroke_width=0, fill_color=cols[i], fill_opacity=1) for i in range(n)])
    g.arrange(RIGHT, buff=0.1).move_to(P(*pos))
    return g


def band(text, color, size=26, w=None):
    t = lab(text, size, color)
    return t


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Methods library"
    TITLE = "Mark One Cell, Read Its Family"


# ---------------------------------------------------------------------------------------------
class S01Problem(SpokenScene):
    """A stain shows now, not descendants; cohort vs family; one cell many types, or many committed cells."""

    def construct(self):
        kinds = ["c", "s", "t", "d"] * 2
        xs = np.linspace(-4.9, 4.9, 8)
        row = VGroup(*[shp(kinds[i], (xs[i], 2.5), 0.34) for i in range(8)])
        l1 = lab("stain: what each cell is now", 26).move_to(P(0, 1.65))

        self.at("A stain")
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in row], lag_ratio=0.12), FadeIn(l1), run_time=1.4)

        self.at("It cannot follow")
        c0 = cell((-4.4, -0.5), 0.42)
        l0 = lab("one cell", 24).next_to(c0, DOWN, buff=0.15)
        da = DashedLine(P(-3.7, -0.5), P(-0.9, -0.5), color=RED, stroke_width=4)
        qb = chip("?", RED, 40).move_to(P(0.0, -0.5))
        ld = lab("its descendants?", 26, RED).move_to(P(0.0, -1.5))
        self.play(FadeIn(c0), FadeIn(l0), run_time=0.4)
        self.play(Create(da), FadeIn(qb), FadeIn(ld), run_time=0.9)

        self.at("A birth date")
        ring = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=2.9, height=0.95, stroke_color=YELLOW, stroke_width=4)
                              .move_to(P(xs[3], 2.5)))
        l2 = lab("birth date: one cohort", 26, YELLOW).move_to(P(xs[3], 1.65))
        self.play(FadeOut(VGroup(c0, l0, da, qb, ld, l1)), run_time=0.4)
        self.play(Create(ring), FadeIn(l2), run_time=0.8)

        self.at("A lineage is one family")
        self.play(FadeOut(ring), FadeOut(l2), run_time=0.3)
        one = cell((0, -0.6), 0.42, ORANGE, fill=0.85)
        fan = VGroup(*[Line(P(0, -0.2), P(xs[i], 2.1), color=ORANGE, stroke_width=3) for i in range(8)])
        l3 = lab("a lineage: one family, all descendants of one cell", 26, ORANGE).move_to(P(0, -1.55))
        self.play(FadeIn(one, scale=0.6), run_time=0.4)
        self.play(LaggedStart(*[Create(f) for f in fan], lag_ratio=0.08), FadeIn(l3), run_time=1.4)

        self.at("Could one embryonic")
        self.play(FadeOut(VGroup(one, fan, l3)), run_time=0.4)
        l4 = lab("the same mixed population", 26).move_to(P(0, 1.65))
        top = [(-4.65, 0.3), (-3.75, 0.3), (-2.85, 0.3), (-1.95, 0.3)]
        tk = ["c", "s", "t", "d"]
        aS = VGroup(*[shp(tk[i], top[i], 0.3) for i in range(4)])
        aC = cell((-3.3, -1.5), 0.38)
        aA = VGroup(*[arr((-3.3, -1.1), (top[i][0], -0.1), GREY, 3, 0.15) for i in range(4)])
        aL = lab("one cell, many types?", 26).move_to(P(-3.3, -2.6))
        self.play(FadeIn(l4), FadeIn(aC), run_time=0.4)
        self.play(LaggedStart(*[GrowArrow(a) for a in aA], lag_ratio=0.1), FadeIn(aS), FadeIn(aL), run_time=1.0)

        self.at("or did the population")
        bx = [3.3 + d for d in (-1.35, -0.45, 0.45, 1.35)]
        bS = VGroup(*[shp(tk[i], (bx[i], 0.3), 0.3) for i in range(4)])
        bC = VGroup(*[cell((bx[i], -1.5), 0.3) for i in range(4)])
        bA = VGroup(*[arr((bx[i], -1.15), (bx[i], -0.1), GREY, 3, 0.15) for i in range(4)])
        bL = lab("many committed cells?", 26).move_to(P(3.3, -2.6))
        self.play(FadeIn(bC), run_time=0.4)
        self.play(LaggedStart(*[GrowArrow(a) for a in bA], lag_ratio=0.1), FadeIn(bS), FadeIn(bL), run_time=1.0)

        self.at("could not tell")
        q = T("?", 80, YELLOW, weight=BOLD).move_to(P(0, -0.2))
        ql = lab("population graft:\ncannot tell", 26, YELLOW, line_spacing=0.9).move_to(P(0, -1.6))
        self.play(FadeIn(q, scale=0.5), FadeIn(ql), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02WatchDye(SpokenScene):
    """Route one: watch the worm divide and record the tree. Route two: inject a tracer into one cell."""

    def construct(self):
        xL, xR = -3.4, 3.4
        # ---- left: watch
        h1 = lab("watch", 30, TEXT, weight=BOLD).move_to(P(xL, 3.2))
        ring = Circle(radius=1.0, stroke_color=GREY, stroke_width=4).move_to(P(xL, 2.0))
        z = cell((xL, 2.0), 0.4)
        self.at("One route")
        self.play(FadeIn(h1), Create(ring), FadeIn(z), run_time=0.8)

        self.at("Brenner chose")
        wl = lab("small transparent worm: cells watched alive", 24).move_to(P(xL, 0.7))
        self.play(FadeIn(wl, shift=UP * 0.1), run_time=0.6)

        self.at("Sulston watched")
        # divisions inside the ring: 1 -> 2 -> 4
        d2 = [cell((xL - 0.35, 2.0), 0.3), cell((xL + 0.35, 2.0), 0.3)]
        d4 = [cell((xL - 0.5, 2.25), 0.22), cell((xL - 0.5, 1.75), 0.22), cell((xL + 0.5, 2.25), 0.22), cell((xL + 0.5, 1.75), 0.22)]
        self.play(ReplacementTransform(z, VGroup(*d2)), run_time=0.8)
        self.play(ReplacementTransform(VGroup(*d2), VGroup(*d4)), run_time=0.8)

        self.at("recorded which cell")
        # lineage tree
        yr, y1, y2, y3 = 0.05, -0.8, -1.65, -2.5
        l1x = [xL - 1.4, xL + 1.4]
        l2x = [l1x[0] - 0.7, l1x[0] + 0.7, l1x[1] - 0.7, l1x[1] + 0.7]
        l3x = []
        for x in l2x:
            l3x += [x - 0.35, x + 0.35]
        tree = VGroup()
        for x in l1x:
            tree.add(Line(P(xL, yr), P(x, y1), color=GREY, stroke_width=3))
        for i, x in enumerate(l2x):
            tree.add(Line(P(l1x[i // 2], y1), P(x, y2), color=GREY, stroke_width=3))
        for i, x in enumerate(l3x):
            tree.add(Line(P(l2x[i // 2], y2), P(x, y3), color=GREY, stroke_width=3))
        leaves = VGroup(*[cell((x, y3), 0.14, fill=0.5) for x in l3x])
        tl = lab("the lineage tree", 24).move_to(P(xL, -3.15))
        self.play(LaggedStart(*[Create(t) for t in tree], lag_ratio=0.1), FadeIn(leaves), FadeIn(tl), run_time=2.2)

        # ---- right: inject
        self.at("Another is to inject")
        h2 = lab("inject a tracer", 30, TEXT, weight=BOLD).move_to(P(xR, 3.2))
        xs = [xR + d for d in (-2.3, -1.15, 0, 1.15, 2.3)]
        row1 = VGroup(*[cell((x, 1.1), 0.42) for x in xs])
        pip = pipette((xR, 1.55), fill=ORANGE)
        self.play(FadeIn(h2), FadeIn(row1), FadeIn(pip, shift=DOWN * 0.3), run_time=0.9)
        self.play(lit(row1[2]), run_time=0.6)

        self.at("Its descendants receive")
        self.play(FadeOut(pip), run_time=0.3)
        row2 = [cell((xR - 2.5, -0.6), 0.38), cell((xR - 1.5, -0.6), 0.38),
                cell((xR - 0.33, -0.6), 0.28, ORANGE, fill=0.85), cell((xR + 0.33, -0.6), 0.28, ORANGE, fill=0.85),
                cell((xR + 1.5, -0.6), 0.38), cell((xR + 2.5, -0.6), 0.38)]
        aa = [arr((xR - 0.15, 0.62), (xR - 0.33, -0.2), ORANGE, 3, 0.15), arr((xR + 0.15, 0.62), (xR + 0.33, -0.2), ORANGE, 3, 0.15)]
        self.play(FadeIn(VGroup(*[row2[i] for i in (0, 1, 4, 5)])), *[GrowArrow(a) for a in aa],
                  FadeIn(row2[2]), FadeIn(row2[3]), run_time=1.0)

        self.at("A large dextran")
        xm = VGroup(xmark((xR - 0.9, -0.6), 0.16), xmark((xR + 0.9, -0.6), 0.16))
        dl = lab("dextran: too large\nto pass to neighbours", 24, RED, line_spacing=0.9).move_to(P(xR, -1.9))
        self.play(FadeIn(xm), FadeIn(dl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Marks(SpokenScene):
    """Three ways a mark is written into the DNA: retrovirus insert, Cre reporter, inducible Cre with a low dose."""

    def construct(self):
        xA, xB, xC = -4.3, 0.0, 4.3
        # ---- column A: retrovirus
        hA = lab("retrovirus", 28, TEXT, weight=BOLD).move_to(P(xA, 3.2))
        cA = cell((xA, 1.0), 1.0)
        nA = cell((xA, 1.0), 0.5, GREY, fill=0.05, w=2)
        dna = Rectangle(width=0.7, height=0.1, stroke_width=0, fill_color=GREY, fill_opacity=0.8).move_to(P(xA, 1.0))
        vir = cell((xA - 1.4, 2.5), 0.2, BLUE, fill=0.7)
        vl = lab("virus", 22, BLUE).next_to(vir, UP, buff=0.08)
        self.at("A retrovirus")
        self.play(FadeIn(hA), FadeIn(cA), FadeIn(nA), FadeIn(dna), FadeIn(vir), FadeIn(vl), run_time=0.9)
        self.at("joins its genome")
        self.play(FadeOut(vl), vir.animate.move_to(P(xA, 1.0)).scale(0.6), run_time=0.7)
        ins = Rectangle(width=0.22, height=0.2, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(P(xA + 0.15, 1.0))
        self.play(FadeOut(vir), FadeIn(ins, scale=1.6), run_time=0.4)
        self.at("so every descendant")
        d1 = cell((xA - 0.85, -1.6), 0.6)
        d2 = cell((xA + 0.85, -1.6), 0.6)
        dn = [cell((xA - 0.85, -1.6), 0.3, GREY, fill=0.05, w=2), cell((xA + 0.85, -1.6), 0.3, GREY, fill=0.05, w=2)]
        di = [Rectangle(width=0.14, height=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(P(xA - 0.85 + 0.0, -1.6)),
              Rectangle(width=0.14, height=0.12, stroke_width=0, fill_color=ORANGE, fill_opacity=1).move_to(P(xA + 0.85 + 0.0, -1.6))]
        a1 = arr((xA - 0.3, -0.1), (xA - 0.7, -0.95), GREY, 3, 0.15)
        a2 = arr((xA + 0.3, -0.1), (xA + 0.7, -0.95), GREY, 3, 0.15)
        al = lab("every descendant\ninherits the insert", 24, ORANGE, line_spacing=0.9).move_to(P(xA, -2.75))
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(d1), FadeIn(d2), FadeIn(VGroup(*dn)), FadeIn(VGroup(*di)), FadeIn(al), run_time=1.2)

        # ---- column B: Cre reporter
        self.at("puts a fluorescent")
        hB = lab("Cre reporter", 28, TEXT, weight=BOLD).move_to(P(xB, 3.2))
        lamp = cell((xB, 1.0), 0.55, GREY, fill=0.1, w=4)
        gl = lab("fluorescent protein gene", 22).move_to(P(xB, 0.05))
        self.play(FadeIn(hB), FadeIn(lamp), FadeIn(gl), run_time=0.7)
        self.at("behind a stop")
        stop = chip("stop", RED, 22, pad=0.1).move_to(P(xB, 1.0))
        lx1 = lab("loxP", 22, GREY).move_to(P(xB - 1.35, 1.0))
        lx2 = lab("loxP", 22, GREY).move_to(P(xB + 1.35, 1.0))
        self.play(FadeIn(stop, shift=DOWN * 0.4), run_time=0.6)
        self.play(FadeIn(lx1), FadeIn(lx2), run_time=0.5)
        self.at("deletes the stop")
        cre = chip("Cre", BLUE, 24, pad=0.12).move_to(P(xB, 2.5))
        self.play(FadeIn(cre, shift=DOWN * 0.3), run_time=0.4)
        self.play(FadeOut(VGroup(stop, lx1, lx2), shift=DOWN * 0.6), run_time=0.5)
        glow = Circle(radius=0.7, stroke_width=0, fill_color=ORANGE, fill_opacity=0.25).move_to(P(xB, 1.0))
        self.play(lamp.animate.set_fill(ORANGE, 0.95).set_stroke(ORANGE, 4), FadeIn(glow), FadeOut(cre), run_time=0.6)
        self.at("all its descendants")
        e1 = VGroup(cell((xB - 0.8, -1.6), 0.3, ORANGE, fill=0.95, w=4), Circle(radius=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.2).move_to(P(xB - 0.8, -1.6)))
        e2 = VGroup(cell((xB + 0.8, -1.6), 0.3, ORANGE, fill=0.95, w=4), Circle(radius=0.5, stroke_width=0, fill_color=ORANGE, fill_opacity=0.2).move_to(P(xB + 0.8, -1.6)))
        b1 = arr((xB - 0.3, 0.1), (xB - 0.7, -0.95), GREY, 3, 0.15)
        b2 = arr((xB + 0.3, 0.1), (xB + 0.7, -0.95), GREY, 3, 0.15)
        bl = lab("lit in that cell\nand its descendants", 24, ORANGE, line_spacing=0.9).move_to(P(xB, -2.75))
        self.play(FadeOut(gl), GrowArrow(b1), GrowArrow(b2), FadeIn(e1), FadeIn(e2), FadeIn(bl), run_time=1.0)

        # ---- column C: inducible
        self.at("mutated estrogen")
        hC = lab("Cre + tamoxifen", 28, TEXT, weight=BOLD).move_to(P(xC, 3.2))
        fz = VGroup(chip("Cre", BLUE, 24, pad=0.12), chip("ER", GREY, 24, pad=0.12)).arrange(RIGHT, buff=0.05).move_to(P(xC, 2.1))
        fz.set_opacity(0.35)
        fl = lab("mutated estrogen-\nreceptor domain", 22, GREY, line_spacing=0.9).move_to(P(xC, 1.35))
        self.play(FadeIn(hC), FadeIn(fz), FadeIn(fl), run_time=0.7)
        self.at("tamoxifen switches it on")
        tam = chip("tamoxifen", TEAL, 22, pad=0.1).move_to(P(xC + 1.5, 2.65))
        self.play(FadeIn(tam, shift=DOWN * 0.2), run_time=0.4)
        self.play(tam.animate.move_to(P(xC, 2.65)), run_time=0.4)
        self.play(fz.animate.set_opacity(1.0), run_time=0.5)
        self.at("marks few")
        sheet = VGroup()
        for r in range(3):
            for c in range(5):
                sheet.add(cell((xC - 1.5 + 0.75 * c, 0.4 - 0.7 * r), 0.25, fill=0.1, w=2.5))
        self.play(FadeOut(tam), FadeIn(sheet), run_time=0.5)
        dl = chip("low dose", TEAL, 22, pad=0.1).move_to(P(xC, -1.65))
        self.play(FadeIn(dl), *[lit(sheet[i]) for i in (3, 6, 13)], run_time=0.7)
        cl = lab("few, scattered cells marked", 22, ORANGE).move_to(P(xC, -2.4))
        self.play(FadeIn(cl), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04ColourCodes(SpokenScene):
    """Colour separates neighbours (random colours, four colours); barcodes carry the family without colour."""

    def construct(self):
        xL, xR = -3.4, 3.4
        hL = lab("colour", 30, TEXT, weight=BOLD).move_to(P(xL, 3.2))
        grid = VGroup()
        for r in range(5):
            for c in range(5):
                grid.add(cell((xL - 2.2 + 1.1 * c, 2.3 - 0.95 * r), 0.4, fill=0.1))
        self.at("can separate")
        self.play(FadeIn(hL), FadeIn(grid), run_time=0.8)

        self.at("chooses at random")
        rng = np.random.RandomState(3)
        hues = [ManimColor.from_hsv((0.17 + 0.82 * i / 13.0, 0.62, 1.0)) for i in range(14)]
        rc = [hues[i] for i in rng.permutation(14)[:1]]
        anims = []
        for i, m in enumerate(grid):
            hue = hues[rng.randint(14)]
            anims.append(m.animate.set_fill(hue, 0.9).set_stroke(hue, 3))
        self.play(*anims, run_time=1.0)
        l1 = lab("Brainbow: random colours,\nabout 90 with tandem copies", 24, TEXT, line_spacing=0.9).move_to(P(xL, -2.6))
        self.at("tandem copies")
        self.play(FadeIn(l1), run_time=0.5)

        self.at("Confetti switches")
        clone = [[0, 0, 1, 1, 1], [0, 0, 0, 1, 2], [3, 3, 0, 2, 2], [3, 3, 3, 2, 2], [3, 3, 2, 2, 2]]
        anims = []
        for r in range(5):
            for c in range(5):
                col = CF[clone[r][c]]
                anims.append(grid[r * 5 + c].animate.set_fill(col, 0.9).set_stroke(col, 3))
        l2 = lab("Confetti: one of four,\nneighbouring clones can differ", 24, TEXT, line_spacing=0.9).move_to(P(xL, -2.6))
        self.play(FadeOut(l1), *anims, run_time=1.0)
        self.play(FadeIn(l2), run_time=0.4)

        # ---- right: barcodes
        self.at("gave blood progenitors")
        hR = lab("barcodes", 30, TEXT, weight=BOLD).move_to(P(xR, 3.2))
        root = cell((xR, 2.3), 0.3, ORANGE, fill=0.3)
        rb = barcode((xR, 1.78))
        self.play(FadeIn(hR), FadeIn(root), FadeIn(rb), run_time=0.7)
        n1 = [(xR - 1.5, 0.65), (xR + 1.5, 0.65)]
        n2 = [(xR - 2.2, -1.1), (xR - 0.8, -1.1), (xR + 0.8, -1.1), (xR + 2.2, -1.1)]
        c1 = [cell(p, 0.3, ORANGE, fill=0.3) for p in n1]
        b1 = [barcode((p[0], p[1] - 0.52)) for p in n1]
        c2 = [cell(p, 0.3, ORANGE, fill=0.3) for p in n2]
        b2 = [barcode((p[0], p[1] - 0.52)) for p in n2]
        e1 = [arr((xR, 2.0 - 0.0 - 0.25), (p[0], p[1] + 0.35), GREY, 3, 0.14) for p in n1]
        e1 = [Line(P(xR, 1.98 - 0.0), P(p[0], p[1] + 0.32), color=GREY, stroke_width=3) for p in n1]
        e2 = [Line(P(n1[i // 2][0], n1[i // 2][1] - 0.7), P(p[0], p[1] + 0.32), color=GREY, stroke_width=3) for i, p in enumerate(n2)]
        self.at("passed to every descendant")
        self.play(*[Create(e) for e in e1], *[FadeIn(c) for c in c1], *[FadeIn(b) for b in b1], run_time=0.9)
        self.play(*[Create(e) for e in e2], *[FadeIn(c) for c in c2], *[FadeIn(b) for b in b2], run_time=0.9)
        rl = lab("the same barcode in every descendant", 24, ORANGE).move_to(P(xR, -2.5))
        self.play(FadeIn(rl), run_time=0.4)

        self.at("that gather mutations")
        # mutations accumulate: bar index 1 on left branch, bar 4 on right branch, bar 3 on one grandchild
        Y = YELLOW

        def mut(bc, i):
            return bc[i].animate.set_fill(Y, 1)
        self.play(FadeOut(rl), mut(b1[0], 1), mut(b2[0], 1), mut(b2[1], 1), mut(b1[1], 4), mut(b2[2], 4), mut(b2[3], 4), run_time=0.9)
        self.play(mut(b2[3], 2), run_time=0.6)
        self.at("shared patterns")
        sl = lab("shared mutations show relatedness", 24, YELLOW).move_to(P(xR, -2.5))
        hl = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=2.2, height=1.3, stroke_color=YELLOW, stroke_width=3)
                            .move_to(P(xR - 1.5, -1.35)))
        self.play(FadeIn(sl), Create(hl), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Reading(SpokenScene):
    """A sparse cluster is a family (a sampling argument); gut crypts drift to one colour; one over N."""

    def construct(self):
        # top sheet
        sheet = VGroup()
        for r in range(3):
            for c in range(14):
                sheet.add(cell((-5.2 + 0.8 * c, 3.0 - 0.62 * r), 0.22, fill=0.1, w=2.5))
        self.at("Mark cells sparsely")
        self.play(FadeIn(sheet), run_time=0.7)
        mk = [sheet[i] for i in (17, 18, 19, 31, 32)]
        # cluster: row1 cols 3,4,5 ; row2 cols 3,4  (indices r*14+c)
        self.play(*[lit(m) for m in (sheet[17], sheet[18], sheet[19], sheet[31], sheet[32])], run_time=0.8)
        lone = [sheet[i] for i in (4, 9, 40)]
        self.play(*[lit(m) for m in (sheet[4], sheet[10], sheet[38])], run_time=0.5)
        self.at("one progenitor's family")
        ring = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=2.9, height=1.6, stroke_color=YELLOW, stroke_width=4)
                              .move_to(P(-5.2 + 0.8 * 4 - 0.0, 2.38)))
        self.play(Create(ring), run_time=0.6)
        self.at("That is a sampling argument")
        t1 = lab("read as one progenitor's family: a sampling argument, not an observation", 24, YELLOW).move_to(P(0, 0.95))
        self.play(FadeIn(t1), run_time=0.6)

        # bottom rings
        self.at("In the gut")
        cx = [-4.3, 0.0, 4.3]
        cy = -1.2
        order = [[0, 1, 2, 3, 0, 1], [0, 0, 2, 0, 0, 1], [0, 0, 0, 0, 0, 0]]

        def ringcells(k, cols):
            g = VGroup()
            for j in range(6):
                a = PI / 2 + j * TAU / 6
                m = cell((cx[k] + 1.0 * np.cos(a), cy + 1.0 * np.sin(a)), 0.33, CF[cols[j]], fill=0.9)
                g.add(m)
            return g

        r1 = ringcells(0, order[0])
        s1 = lab("start", 24).move_to(P(cx[0], -2.95))
        idl = lab("idealised example", 24, GREY).move_to(P(-4.55, -3.5))
        self.play(FadeOut(t1), FadeOut(ring), FadeIn(r1), FadeIn(s1), FadeIn(idl), run_time=0.8)
        self.at("and colleagues used")
        self.play(Indicate(r1, scale_factor=1.08), run_time=0.5)
        self.at("Some clones grew")
        r2 = ringcells(1, order[1])
        a1 = arr((-2.7, cy), (-1.6, cy), GREY, 3, 0.15)
        s2 = lab("later", 24).move_to(P(cx[1], -2.95))
        self.play(GrowArrow(a1), FadeIn(r2), FadeIn(s2), run_time=0.9)
        self.at("crypts drifted")
        r3 = ringcells(2, order[2])
        a2 = arr((1.6, cy), (2.7, cy), GREY, 3, 0.15)
        s3 = lab("1 to 6 months", 24).move_to(P(cx[2], -2.95))
        self.play(GrowArrow(a2), FadeIn(r3), FadeIn(s3), run_time=0.9)
        self.at("neutral drift")
        nl = lab("neutral drift among equivalent stem cells", 24, TEXT).move_to(P(0, 0.9))
        self.play(FadeIn(nl), run_time=0.6)
        self.at("With N of them")
        nn = lab("N equivalent stem cells", 24, TEXT).move_to(P(2.0, -3.5))
        self.play(FadeIn(nn), run_time=0.4)
        self.at("takes over a crypt")
        pr = M("one clone takes over: probability 1/N", 26, ORANGE).move_to(P(0, -0.0 - 3.4 + 0.0))
        pr.move_to(P(2.6, -3.5))
        self.play(FadeOut(nn), FadeIn(pr), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Pitfalls(SpokenScene):
    """Two founders look like one clone; leaky labelling marks cells with no inducer. Controls for each."""

    def construct(self):
        xL, xR = -3.4, 3.4
        hL = lab("two founders marked", 28, RED, weight=BOLD).move_to(P(xL, 3.2))
        xs = [xL - 2.4 + 0.8 * i for i in range(7)]
        row = VGroup(*[cell((x, 2.2), 0.3) for x in xs])
        self.at("marked at once")
        self.play(FadeIn(hL), FadeIn(row), run_time=0.7)
        self.play(lit(row[3]), lit(row[4]), run_time=0.6)
        self.at("look like one clone")
        clus = VGroup(*[cell((xL - 1.5 + 0.55 * i + (0.0), 0.7 - 0.0), 0.24, ORANGE, fill=0.85) for i in range(6)])
        clus.arrange(RIGHT, buff=0.06).move_to(P(xL, 0.8))
        ar = arr((xL, 1.6), (xL, 1.25), GREY, 3, 0.14)
        q = T("one clone or two?", 26, RED).move_to(P(xL, -0.1))
        self.play(GrowArrow(ar), FadeIn(clus), FadeIn(q), run_time=0.9)
        self.at("sparse and count")
        g1 = chip("keep induction sparse", GREEN, 24).move_to(P(xL, -1.3))
        self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.5)
        self.at("close pairs")
        g2 = chip("count close pairs of marks", GREEN, 24).move_to(P(xL, -2.2))
        self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.5)

        self.at("Leaky")
        hR = lab("leaky labelling", 28, RED, weight=BOLD).move_to(P(xR, 3.2))
        sheet = VGroup()
        for r in range(3):
            for c in range(5):
                sheet.add(cell((xR - 1.8 + 0.9 * c, 2.3 - 0.8 * r), 0.3, fill=0.1))
        vl = chip("no tamoxifen", TEAL, 22, pad=0.1).move_to(P(xR, -0.05))
        self.play(FadeIn(hR), FadeIn(sheet), FadeIn(vl), run_time=0.7)
        self.at("no excision appeared")
        t1 = lab("1996 test: no excision in untreated animals", 22, GREEN).move_to(P(xR, -0.75))
        self.play(FadeIn(t1), run_time=0.5)
        self.at("without tamoxifen")
        self.play(lit(sheet[1]), lit(sheet[8]), t1.animate.set_opacity(0.3), run_time=0.6)
        t2 = lab("2020 mouse study: labelling without\ntamoxifen in every CreERT2 line examined;\ndepends on reporter", 22, RED, line_spacing=0.9).move_to(P(xR, -1.8))
        self.play(FadeIn(t2), run_time=0.4)
        self.at("genotype animals")
        g3 = chip("full-genotype animals + vehicle", GREEN, 24).move_to(P(xR, -2.85))
        self.play(FadeIn(g3, shift=UP * 0.1), run_time=0.5)
        self.at("reporter stays off")
        g4 = lab("reporter stays off?", 24, GREEN).move_to(P(xR, -3.4))
        self.play(FadeIn(g4), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07Discoveries1(SpokenScene):
    """Bronner-Fraser and Fraser 1988; Ginhoux and colleagues 2010."""

    def construct(self):
        xL, xR = -3.4, 3.4
        # ---- left: neural tube
        tube = RoundedRectangle(corner_radius=0.5, width=4.0, height=3.2, stroke_color=GREY, stroke_width=4).move_to(P(xL, 1.0))
        tl = lab("chick neural tube", 24).move_to(P(xL, -0.95))
        tc = VGroup(*[cell((xL - 1.2 + 0.6 * i, 0.5), 0.22, fill=0.1, w=2.5) for i in range(5)],
                    *[cell((xL - 0.9 + 0.6 * i, -0.1), 0.22, fill=0.1, w=2.5) for i in range(4)])
        top = cell((xL, 1.85), 0.26, fill=0.1)
        self.at("injected dye")
        pip = pipette((xL, 2.15), fill=ORANGE)
        self.play(FadeIn(tube), FadeIn(tl), FadeIn(tc), FadeIn(top), FadeIn(pip, shift=DOWN * 0.2), run_time=0.9)
        self.play(lit(top), run_time=0.5)
        self.play(FadeOut(pip), run_time=0.3)
        self.at("Many clones held")
        kinds = ["c", "s", "t", "d"]
        pos = [(xL - 1.2 + 0.8 * i, 1.55) for i in range(4)]
        outs = VGroup(*[shp(kinds[i], pos[i], 0.28, ORANGE, fill=0.85) for i in range(4)])
        self.play(ReplacementTransform(top, outs), run_time=1.0)
        cl = lab("one clone, several cell types", 24, ORANGE).move_to(P(xL, -1.65))
        self.play(FadeIn(cl), run_time=0.4)
        self.at("multipotent")
        m = lab("some crest cells are multipotent", 24, TEXT).move_to(P(xL, -2.3))
        self.play(FadeIn(m), run_time=0.5)
        self.at("That needed", nth=0)
        tg = lab("Bronner-Fraser and Fraser, 1988", 22, GOLD).move_to(P(xL, -3.3))
        nd = chip("single-cell marking", ORANGE, 22, pad=0.1).move_to(P(xL + 0.0, 3.3))
        self.play(FadeIn(nd), FadeIn(tg), run_time=0.5)

        # ---- right: Ginhoux
        self.at("pulsed tamoxifen")
        axy = -0.4
        ax = arr((0.7, axy), (6.1, axy), GREY, 4, 0.18)
        e8x = 2.8
        e8 = Line(P(e8x, axy - 0.18), P(e8x, axy + 0.18), color=YELLOW, stroke_width=5)
        e8l = lab("embryonic day 8", 22, YELLOW).move_to(P(e8x + 1.0, axy + 0.4))
        pt = Line(P(2.15, axy - 0.18), P(2.15, axy + 0.18), color=TEAL, stroke_width=6)
        tam = chip("tamoxifen pulse\nabout day 7.5", TEAL, 22, pad=0.1).move_to(P(1.7, -1.95))
        ta = arr((2.0, -1.45), (2.15, axy - 0.25), TEAL, 3, 0.14)
        self.play(Create(ax), Create(e8), FadeIn(e8l), run_time=0.7)
        self.play(FadeIn(tam), GrowArrow(ta), Create(pt), run_time=0.7)
        self.at("Adult mouse microglia")
        pm = chip("primitive myeloid\nprogenitors\narise before day 8", ORANGE, 22, pad=0.12).move_to(P(1.6, 1.3))
        mg = chip("adult mouse\nmicroglia", ORANGE, 22, pad=0.12).move_to(P(5.35, 1.3))
        a2 = arr((3.25, 1.3), (4.3, 1.3), ORANGE, 4, 0.18)
        self.play(FadeIn(pm), run_time=0.6)
        self.play(GrowArrow(a2), FadeIn(mg), run_time=0.7)
        self.at("before embryonic day")
        self.play(Indicate(e8l, color=YELLOW), run_time=0.6)
        self.at("not significantly")
        pb = chip("postnatal blood\nprogenitors", GREY, 22, pad=0.12).move_to(P(5.0, -1.6))
        a3 = arr((5.0, -1.05), (5.3, 0.7), GREY, 3, 0.14)
        xm = xmark((5.08, -0.75), 0.2)
        nl = lab("no significant\ncontribution,\nadult mouse", 22, RED, line_spacing=0.9).move_to(P(5.0, -2.85))
        self.play(FadeIn(pb), GrowArrow(a3), FadeIn(xm), FadeIn(nl), run_time=0.8)
        self.at("That needed a pulse")
        tg2 = lab("Ginhoux and colleagues, 2010", 22, GOLD).move_to(P(xR, -3.75))
        nd2 = chip("a pulse in time", TEAL, 22, pad=0.1).move_to(P(5.0, 2.7))
        self.play(FadeIn(nd2), FadeIn(tg2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S08Discoveries2(SpokenScene):
    """Shi and colleagues 2019: scattered clones in the plant cambium; then the rule to keep."""

    def construct(self):
        xL, xR = -3.6, 3.2
        # ---- left: the three layers
        names = [("phloem", 2.2), ("cambium", 1.25), ("xylem", 0.3)]
        bands = {}
        allc = VGroup()
        for nm, y in names:
            cs = [cell((xL - 1.5 + 0.6 * i, y), 0.27, fill=0.1, w=2.5) for i in range(6)]
            bands[nm] = cs
            allc.add(*cs)
        nl = VGroup(*[lab(nm, 24).move_to(P(xL + 2.75, y)) for nm, y in names])
        self.at("marked scattered cambium")
        self.play(FadeIn(allc), FadeIn(nl), run_time=0.8)
        dex = chip("dexamethasone", TEAL, 22, pad=0.1).move_to(P(xL - 0.9, 3.2))
        self.play(FadeIn(dex, shift=DOWN * 0.2), run_time=0.4)
        self.play(lit(bands["cambium"][1]), lit(bands["cambium"][4]), run_time=0.6)
        inf = lab("marked cells: inferred founders", 22, ORANGE).move_to(P(xL, -0.35))
        self.play(FadeIn(inf), run_time=0.4)
        self.at("dexamethasone as the inducer")
        nt = lab("not tamoxifen", 22, GREY).move_to(P(xL + 1.9, 3.2))
        self.play(FadeIn(nt), run_time=0.4)
        self.at("clones at 10")
        # right: 99 clones
        gh = lab("99 clones at 10 days", 24, TEXT).move_to(P(xR, 3.2))
        rng = np.random.RandomState(5)
        grid = VGroup(*[Square(side_length=0.3, stroke_width=1.5, stroke_color=GREY, fill_color=GREY, fill_opacity=0.25)
                        .move_to(P(xR - 1.9 + 0.38 * (i % 11), 2.5 - 0.38 * (i // 11), )) for i in range(99)])
        self.play(FadeIn(grid), FadeIn(gh), run_time=0.8)
        self.at("spanned xylem")
        pick = rng.permutation(99)[:35]
        self.play(*[grid[int(i)].animate.set_fill(ORANGE, 0.9).set_stroke(ORANGE, 1.5) for i in pick], run_time=0.9)
        # the spanning clone on the left
        self.play(*[lit(bands[nm][4]) for nm in ("phloem", "xylem")], run_time=0.6)
        gl = lab("35 spanned xylem, cambium and phloem", 22, ORANGE).move_to(P(xR + 0.1, -1.2))
        self.play(FadeIn(gl), run_time=0.4)
        self.at("support for one")
        bf = chip("support for one bifacial stem cell", ORANGE, 22, pad=0.1).move_to(P(xL + 0.3, -0.95))
        tg = lab("Shi and colleagues, 2019", 22, GOLD).move_to(P(xL + 0.3, -1.55))
        self.play(FadeIn(bf), FadeIn(tg), run_time=0.6)
        self.at("A cluster read")
        rule = lab("A cluster read as one family is a sampling argument,\nnot an observation.", 32, TEXT, font=TITLE_FONT, line_spacing=0.9)
        box = RoundedRectangle(corner_radius=0.2, width=rule.width + 0.8, height=rule.height + 0.5, stroke_color=GOLD, stroke_width=4,
                               fill_color=GOLD, fill_opacity=0.08)
        g = VGroup(box, rule.move_to(box)).move_to(P(0, -2.65))
        self.play(FadeIn(g, shift=UP * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S09End(EndCard):
    LINE = "A cluster read as one family is a sampling argument."
