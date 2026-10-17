"""Extending Mendel: the boxes stay, the labels change  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

One idea: a cross always fills the same boxes (2 x 2 for one gene, 4 x 4 for two). What the
boxes are CALLED depends on how the genes act.

COLOR MAP (one color per concept, whole video)
  YELLOW   = the yellow coat (mouse, Labrador); also the yellow allele dot
  BLACKC   = the black coat / black allele (dark fill with a light rim)
  CHOC     = chocolate (brown) coat
  FLOWER_RED / PINK / WHITE = snapdragon flower colours (and the red / white allele dots)
  TEXT     = genotype letters and dots (the fixed layer: what the boxes hold)
  BLUE / ORANGE / PURPLE / TEAL = anonymous phenotype classes of the regrouping scenes,
             always labelled next to the ratio; BLUE = colour made, GREY = no colour (9:7, 15:1)
  GOLD     = ratios and the word "map" (what the boxes are labelled with)
  GREEN    = rules that hold / survivors
  RED      = death, a failed idea
  GREY     = box outlines and secondary labels

No molecules: alleles are round dots, genotypes are letter strings, plants and mice are simple shapes.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#F08CB0"
FLOWER_RED = "#E04656"
WHITE = "#F2F2F2"
BLACKC = "#262A34"
CHOC = "#8B5A3C"
LABEL_ON_YELLOW = "#1b1d24"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def dot(kind, r=0.17):
    """An allele: a round dot. Colour/fill says which allele."""
    if kind == "red":
        d = Circle(radius=r, stroke_color=FLOWER_RED, fill_color=FLOWER_RED, fill_opacity=1)
    elif kind == "white":
        d = Circle(radius=r, stroke_color=WHITE, fill_color=WHITE, fill_opacity=1)
    elif kind == "yel":
        d = Circle(radius=r, stroke_color=YELLOW, fill_color=YELLOW, fill_opacity=1)
    elif kind == "blk":
        d = Circle(radius=r, stroke_color=TEXT, fill_color=BLACKC, fill_opacity=1)
    elif kind == "D":
        d = Circle(radius=r, stroke_color=TEXT, fill_color=TEXT, fill_opacity=1)
    else:  # "r": hollow ring
        d = Circle(radius=r, stroke_color=TEXT, fill_color=BG, fill_opacity=1)
    d.set_stroke(width=3)
    return d


def flower(color, s=1.0):
    petals = VGroup()
    for k in range(5):
        a = np.pi / 2 + k * 2 * np.pi / 5
        p = Circle(radius=0.28 * s, stroke_width=2, stroke_color=color, fill_color=color, fill_opacity=0.95)
        p.move_to(0.31 * s * np.array([np.cos(a), np.sin(a), 0]))
        petals.add(p)
    ctr = Circle(radius=0.14 * s, stroke_width=0, fill_color=BG, fill_opacity=1)
    g = VGroup(petals, ctr)
    g.petals = petals
    return g


def mouse(kind, s=1.0):
    if kind == "yel":
        col, edge = YELLOW, YELLOW
        eye = BG
    else:
        col, edge = BLACKC, GREY
        eye = TEXT
    kw = dict(stroke_color=edge, stroke_width=2, fill_color=col, fill_opacity=1)
    body = Ellipse(width=1.3 * s, height=0.8 * s, **kw)
    head = Circle(radius=0.32 * s, **kw).move_to([0.62 * s, 0.12 * s, 0])
    ear = Circle(radius=0.15 * s, **kw).move_to([0.5 * s, 0.44 * s, 0])
    tail = ArcBetweenPoints([-0.62 * s, 0.0, 0], [-1.15 * s, 0.5 * s, 0], angle=-PI / 2,
                            stroke_color=edge if kind != "yel" else YELLOW, stroke_width=4)
    e = Circle(radius=0.045 * s, stroke_width=0, fill_color=eye, fill_opacity=1).move_to([0.74 * s, 0.2 * s, 0])
    g = VGroup(tail, body, head, ear, e)
    return g


def xmark(center, size=0.5, color=RED, w=9):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, -size, 0], c + [size, size, 0], stroke_width=w, color=color),
                  Line(c + [-size, size, 0], c + [size, -size, 0], stroke_width=w, color=color))


def check(center, size=0.5, color=GREEN, w=9):
    c = np.array(center, float)
    return VGroup(Line(c + [-size, 0.0, 0], c + [-size * 0.3, -size * 0.75, 0], stroke_width=w, color=color),
                  Line(c + [-size * 0.3, -size * 0.75, 0], c + [size, size * 0.8, 0], stroke_width=w, color=color))


def left_at(mob, x, y):
    mob.move_to([x, y, 0])
    mob.shift(RIGHT * (x - mob.get_left()[0]))
    return mob


class Sq2:
    """A two-by-two cross square. Gametes of the two parents run across the top and down the left."""

    def __init__(self, center, t, top, left, r=0.2):
        self.t = t
        self.c = np.array([center[0], center[1], 0.0])
        self.tiles, self.ctrs, self.gdots = [], [], []
        self.top_dots = [dot(top[c], r).move_to(self.c + [(c - 0.5) * t, t + 0.45, 0]) for c in range(2)]
        self.left_dots = [dot(left[rr], r).move_to(self.c + [-t - 0.45, (0.5 - rr) * t, 0]) for rr in range(2)]
        for rr in range(2):
            for c in range(2):
                ctr = self.c + [(c - 0.5) * t, (0.5 - rr) * t, 0]
                tile = RoundedRectangle(corner_radius=0.08, width=t, height=t, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.08).move_to(ctr)
                gd = VGroup(dot(left[rr], r).move_to(ctr + [-0.3, t / 2 - 0.4, 0]),
                            dot(top[c], r).move_to(ctr + [0.3, t / 2 - 0.4, 0]))
                self.tiles.append(tile)
                self.ctrs.append(ctr)
                self.gdots.append(gd)

    def icon_pos(self, k):
        return self.ctrs[k] + [0, -0.22, 0]


G4 = [("B", "E"), ("b", "E"), ("B", "e"), ("b", "e")]


class Grid4:
    """A four-by-four dihybrid square. cells[(r, c)] = VGroup(rect, label); .dom[(r, c)] = (has B, has E)."""

    def __init__(self, center, cell=1.25):
        self.cell = cell
        self.c = np.array([center[0], center[1], 0.0])
        self.cells, self.dom = {}, {}
        self.top_lbl, self.left_lbl = [], []
        for k, g in enumerate(G4):
            lab = "".join(g)
            self.top_lbl.append(M(lab, 24, GREY).move_to(self.c + [(k - 1.5) * cell, 2 * cell + 0.38, 0]))
            self.left_lbl.append(M(lab, 24, GREY).move_to(self.c + [-2 * cell - 0.52, (1.5 - k) * cell, 0]))
        for r in range(4):
            for c in range(4):
                a = "".join(sorted([G4[r][0], G4[c][0]], key=lambda x: x.islower()))
                b = "".join(sorted([G4[r][1], G4[c][1]], key=lambda x: x.islower()))
                rect = Rectangle(width=cell, height=cell, stroke_color=GREY, stroke_width=2.5,
                                 fill_color=GREY, fill_opacity=0.08).move_to(self.c + [(c - 1.5) * cell, (1.5 - r) * cell, 0])
                txt = M(a + b, 22, TEXT).move_to(rect)
                self.cells[(r, c)] = VGroup(rect, txt)
                self.dom[(r, c)] = ("B" in a, "E" in b)
        self.all = VGroup(*self.cells.values())
        self.heads = VGroup(*self.top_lbl, *self.left_lbl)

    def paint(self, fn):
        """fn(hasB, hasE) -> (fill, fill_opacity, stroke, text_color); returns animations."""
        anims = []
        for k, grp in self.cells.items():
            fill, op, stroke, tc = fn(*self.dom[k])
            anims.append(grp[0].animate.set_fill(fill, op).set_stroke(stroke))
            anims.append(grp[1].animate.set_color(tc))
        return anims

    def block(self, rows, cols, color=GOLD, w=7):
        pts = [self.cells[(r, c)][0].get_center() for r in rows for c in cols]
        ctr = np.mean(pts, axis=0)
        wd = (len(cols)) * self.cell
        ht = (len(rows)) * self.cell
        return Rectangle(width=wd, height=ht, stroke_color=color, stroke_width=w, fill_opacity=0).move_to(ctr)


NEUTRAL = (GREY, 0.08, GREY, TEXT)


def neutral(a, b):
    return NEUTRAL


def classes4(a, b):
    """the four usual classes of a dihybrid cross, as anonymous hues"""
    if a and b:
        return (BLUE, 0.4, BLUE, TEXT)
    if (not a) and b:
        return (ORANGE, 0.4, ORANGE, TEXT)
    if a and (not b):
        return (PURPLE, 0.4, PURPLE, TEXT)
    return (PINK, 0.4, PINK, TEXT)


def lab_final(a, b):
    if a and b:
        return (BLACKC, 1.0, TEXT, TEXT)
    if (not a) and b:
        return (CHOC, 1.0, CHOC, TEXT)
    return (YELLOW, 0.95, YELLOW, LABEL_ON_YELLOW)


def swatch_row(color, text, size=26, x=1.0, y=0.0, fill=None, rim=None):
    sw = Circle(radius=0.2, stroke_color=rim or color, stroke_width=3, fill_color=fill or color, fill_opacity=1)
    t = T(text, size, TEXT)
    g = VGroup(sw, t).arrange(RIGHT, buff=0.22)
    return left_at(g, x, y)


class S00Title(TitleCard):
    LESSON = "Extending Mendel"
    TITLE = "The boxes stay, the labels change"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """yellow x yellow never breeds true -> Mendel's rules fail? no -> the map from genotype to phenotype changes."""

    def construct(self):
        self.at("Mate two yellow mice")
        m1 = mouse("yel", 1.2).move_to([-4.9, 2.0, 0])
        m2 = mouse("yel", 1.2).move_to([-1.5, 2.0, 0])
        x = T("x", 44, GREY).move_to([-3.2, 2.0, 0])
        self.play(FadeIn(m1, shift=RIGHT * 0.2), FadeIn(m2, shift=LEFT * 0.2), FadeIn(x), run_time=0.6)
        self.at("as often as you like")
        ar = arr_down([-3.2, 1.1, 0], [-3.2, 0.2, 0])
        pups = VGroup(mouse("yel", 0.95).move_to([-5.3, -1.0, 0]), mouse("yel", 0.95).move_to([-3.2, -1.0, 0]),
                      mouse("blk", 0.95).move_to([-1.1, -1.0, 0]))
        cap = T("some young are not yellow", 28, GREY).move_to([-3.2, -2.4, 0])
        self.play(GrowArrow(ar), run_time=0.3)
        self.play(LaggedStart(*[GrowFromCenter(p) for p in pups], lag_ratio=0.25), FadeIn(cap), run_time=0.8)
        self.at("never get")
        box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=4.7, height=5.3, stroke_color=GREY, stroke_width=3)
                             .move_to([3.6, -0.1, 0]), num_dashes=60)
        ym = mouse("yel", 1.3).move_to([3.6, 1.3, 0])
        lab = T("breeds true?", 36).move_to([3.6, -0.5, 0])
        q = T("all young yellow", 30, GREY).move_to([3.6, -1.5, 0])
        self.play(FadeIn(box), FadeIn(ym), FadeIn(lab), FadeIn(q), run_time=0.6)
        self.at("that breeds true")
        xm = xmark([3.6, -0.1, 0], 2.0, RED, 10)
        self.play(Create(xm), run_time=0.5)
        # --- Mendel failed? ---
        self.at("That looked like a failure")
        old = VGroup(m1, m2, x, ar, pups, cap, box, ym, lab, q, xm)
        mchip = chip("Mendel's rules", RED, size=64, pad=0.45).move_to([-1.3, 0.2, 0])
        mx = xmark([4.5, 0.2, 0], 0.9, RED, 12)
        self.play(FadeOut(old), run_time=0.4)
        self.play(FadeIn(mchip, scale=0.9), Create(mx), run_time=0.5)
        self.at("It was not")
        mchip_g = chip("Mendel's rules", GREEN, size=64, pad=0.45).move_to(mchip)
        ck = check([4.5, 0.2, 0], 0.9, GREEN, 12)
        self.play(ReplacementTransform(mchip, mchip_g), ReplacementTransform(mx, ck), run_time=0.5)
        self.at("Segregation and independent")
        c1 = chip("segregation", GREEN, size=40, pad=0.3).move_to([-3.7, -1.4, 0])
        c2 = chip("independent assortment", GREEN, size=40, pad=0.3).move_to([2.2, -1.4, 0])
        self.play(mchip_g.animate.scale(0.8).move_to([0, 2.5, 0]), FadeOut(ck), run_time=0.4)
        self.play(FadeIn(c1, shift=UP * 0.2), FadeIn(c2, shift=UP * 0.2), run_time=0.5)
        self.at("never stop working")
        k1 = check(c1.get_top() + [0, 0.5, 0], 0.3, GREEN, 8)
        k2 = check(c2.get_top() + [0, 0.5, 0], 0.3, GREEN, 8)
        w = T("never stop working", 44, GREEN).move_to([0, 1.1, 0])
        self.play(Create(k1), Create(k2), FadeIn(w), run_time=0.5)
        # --- the map ---
        self.at("What changes")
        self.play(FadeOut(VGroup(mchip_g, c1, c2, k1, k2, w)), run_time=0.4)
        gt = chip("genotype", GREY, size=48, pad=0.36).move_to([-4.2, 1.7, 0])
        gdots = VGroup(dot("yel", 0.36), dot("blk", 0.36)).arrange(RIGHT, buff=0.4).move_to([-4.2, -0.4, 0])
        pt = chip("phenotype", GREY, size=48, pad=0.36).move_to([4.2, 1.7, 0])
        pm = mouse("yel", 1.6).move_to([4.2, -0.4, 0])
        mp = Arrow([-1.9, 0.6, 0], [1.5, 0.6, 0], buff=0, color=GOLD, stroke_width=9, tip_length=0.4)
        mlab = T("map", 60, GOLD, weight=BOLD).move_to([0, 1.7, 0])
        self.play(FadeIn(gt), FadeIn(gdots), FadeIn(pt), FadeIn(pm), run_time=0.5)
        self.play(GrowArrow(mp), FadeIn(mlab), run_time=0.5)
        self.play(Indicate(VGroup(mp, mlab), color=GOLD, scale_factor=1.12), run_time=0.8)
        self.finish()


def arr_down(a, b, color=GREY):
    return Arrow(a, b, buff=0, color=color, stroke_width=6, tip_length=0.25)


# ---------------------------------------------------------------------------------------------
class S02Pink(SpokenScene):
    """red x white -> pink F1; selfed -> 1 red : 2 pink : 1 white; the hidden 1:2:1 is in plain sight."""

    def construct(self):
        self.at("Cross red snapdragons")
        fr = flower(FLOWER_RED, 2.0).move_to([-5.0, 0.9, 0])
        dr = VGroup(dot("red", 0.25), dot("red", 0.25)).arrange(RIGHT, buff=0.35).move_to([-5.0, -1.1, 0])
        x = T("x", 48, GREY).move_to([-3.4, 0.9, 0])
        fw = flower(WHITE, 2.0).move_to([-1.8, 0.9, 0])
        dw = VGroup(dot("white", 0.25), dot("white", 0.25)).arrange(RIGHT, buff=0.35).move_to([-1.8, -1.1, 0])
        self.play(FadeIn(VGroup(fr, dr), shift=RIGHT * 0.2), FadeIn(x), FadeIn(VGroup(fw, dw), shift=LEFT * 0.2), run_time=0.7)
        self.at("flower is pink")
        ar = Arrow([-0.3, 0.9, 0], [1.3, 0.9, 0], buff=0, color=GREY, stroke_width=7, tip_length=0.3)
        fp = flower(PINK, 2.0).move_to([3.6, 0.9, 0])
        dp = VGroup(dot("red", 0.25), dot("white", 0.25)).arrange(RIGHT, buff=0.35).move_to([3.6, -1.1, 0])
        f1 = T("F1", 44, GOLD, weight=BOLD).move_to([3.6, 2.9, 0])
        self.play(GrowArrow(ar), run_time=0.3)
        self.play(GrowFromCenter(fp), FadeIn(dp), FadeIn(f1), run_time=0.5)
        self.at("incomplete dominance")
        inc = T("incomplete dominance", 46, GOLD).move_to([0.0, -2.8, 0])
        self.play(FadeIn(inc, shift=UP * 0.15), run_time=0.5)
        # --- self the pink plants: the square ---
        self.at("Self the pink plants")
        sq = Sq2((-2.7, -0.35), 2.5, ("red", "white"), ("red", "white"))
        small_f1 = VGroup(flower(PINK, 0.8), VGroup(dot("red", 0.14), dot("white", 0.14)).arrange(RIGHT, buff=0.22))
        small_f1[1].next_to(small_f1[0], DOWN, buff=0.2)
        small_f1.move_to([1.7, 2.4, 0])
        sl = T("pink plants, selfed", 26, GREY).next_to(small_f1, RIGHT, buff=0.3)
        self.play(FadeOut(VGroup(fr, dr, x, fw, dw, ar, inc, f1)), ReplacementTransform(VGroup(fp, dp), small_f1), run_time=0.6)
        self.play(FadeIn(VGroup(*sq.tiles)), FadeIn(VGroup(*sq.top_dots, *sq.left_dots)), FadeIn(sl), run_time=0.5)
        self.play(*[FadeIn(g) for g in sq.gdots], run_time=0.5)
        self.at("red and white come back")
        cols = [FLOWER_RED, PINK, PINK, WHITE]
        fls = [flower(cols[k], 1.0).move_to(sq.icon_pos(k)) for k in range(4)]
        self.play(LaggedStart(*[GrowFromCenter(f) for f in fls], lag_ratio=0.3), run_time=1.2)
        self.at("one red")
        rows = []
        specs = [(FLOWER_RED, "1  red", 1.0), (PINK, "2  pink", 0.2), (WHITE, "1  white", -1.2)]
        for col, txt, y in specs:
            ic = flower(col, 0.55)
            tx = T(txt, 34, TEXT)
            g = VGroup(ic, tx).arrange(RIGHT, buff=0.35)
            left_at(g, 1.9, y)
            rows.append(g)
        self.play(FadeIn(rows[0], shift=LEFT * 0.2), run_time=0.3)
        self.at("two pink")
        self.play(FadeIn(rows[1], shift=LEFT * 0.2), run_time=0.3)
        self.at("one white")
        self.play(FadeIn(rows[2], shift=LEFT * 0.2), run_time=0.3)
        ratio = M("1 : 2 : 1", 62, GOLD).move_to([3.9, -2.3, 0])
        self.play(Write(ratio), run_time=0.6)
        self.at("Nothing blended")
        self.play(Indicate(fls[0].petals, scale_factor=1.25, color=FLOWER_RED), Indicate(fls[3].petals, scale_factor=1.25, color=WHITE), run_time=0.8)
        self.at("a pink plant is a heterozygote")
        het = T("heterozygote", 28, GOLD)
        left_at(het, 2.5, -0.45)
        self.play(Circumscribe(sq.gdots[1], color=GOLD), Circumscribe(sq.gdots[2], color=GOLD),
                  FadeIn(het), run_time=0.9)
        self.at("In Mendel's peas")
        hid = M("3 : 1", 62, GOLD).move_to(ratio)
        cd = T("if red hid white, as in peas", 28, GREY).next_to(ratio, DOWN, buff=0.25)
        self.play(fls[1].petals.animate.set_color(FLOWER_RED), fls[2].petals.animate.set_color(FLOWER_RED),
                  FadeOut(*rows), FadeOut(het), ReplacementTransform(ratio, hid), FadeIn(cd), run_time=0.6)
        self.at("but here the colors")
        ratio2 = M("1 : 2 : 1", 62, GOLD).move_to(hid)
        self.play(fls[1].petals.animate.set_color(PINK), fls[2].petals.animate.set_color(PINK),
                  FadeIn(*rows), ReplacementTransform(hid, ratio2), FadeOut(cd), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Lethal(SpokenScene):
    """A^y/a x A^y/a: one quarter die, survivors 2 yellow : 1 black; every live yellow mouse is a heterozygote."""

    def construct(self):
        sq = Sq2((-2.7, -0.35), 2.5, ("yel", "blk"), ("yel", "blk"))
        self.at("Now back to the yellow mouse")
        p1 = VGroup(mouse("yel", 0.6), VGroup(dot("yel", 0.14), dot("blk", 0.14)).arrange(RIGHT, buff=0.2))
        p1[1].next_to(p1[0], DOWN, buff=0.15)
        p1.move_to([2.0, 2.45, 0])
        p2 = p1.copy().move_to([5.2, 2.45, 0])
        px = T("x", 36, GREY).move_to([3.6, 2.45, 0])
        self.play(FadeIn(VGroup(*sq.tiles)), FadeIn(VGroup(*sq.top_dots, *sq.left_dots)), FadeIn(p1), FadeIn(p2), FadeIn(px),
                  run_time=0.6)
        self.play(*[FadeIn(g) for g in sq.gdots], run_time=0.5)
        self.at("dominant for coat color")
        kinds = ["yel", "yel", "yel", "blk"]
        ms = [mouse(kinds[k], 1.0).move_to(sq.icon_pos(k) + [0.1, 0, 0]) for k in range(4)]
        self.play(LaggedStart(*[GrowFromCenter(m) for m in ms], lag_ratio=0.25), run_time=1.0)
        self.at("recessive for survival")
        self.play(Circumscribe(sq.tiles[0], color=RED), run_time=0.8)
        self.at("dies before implantation")
        X = xmark(sq.ctrs[0] + [0, -0.2, 0], 0.8, RED, 12)
        note = T("dies before implantation", 28, RED).move_to([3.6, 1.35, 0])
        self.play(ms[0].animate.set_opacity(0.2), Create(X), FadeIn(note), run_time=0.6)
        self.at("one quarter")
        q = T("one quarter of conceptions die", 28, RED).move_to(note)
        self.play(FadeOut(note), run_time=0.2)
        self.play(FadeIn(q), run_time=0.3)
        self.at("The survivors")
        rings = VGroup(*[RoundedRectangle(corner_radius=0.08, width=2.5, height=2.5, stroke_color=GREEN, stroke_width=7)
                         .move_to(sq.ctrs[k]) for k in (1, 2, 3)])
        self.play(Create(rings), run_time=0.5)
        self.at("two yellow")
        ty = T("2 yellow", 36, YELLOW).move_to([2.4, 0.35, 0])
        self.play(FadeIn(ty, shift=UP * 0.1), run_time=0.3)
        self.at("one black")
        tc = T(":", 36).move_to([3.7, 0.35, 0])
        tb = T("1 black", 36, TEXT).move_to([5.0, 0.35, 0])
        self.play(FadeIn(tc), FadeIn(tb, shift=UP * 0.1), run_time=0.3)
        self.at("twelve live pups")
        pl = T("12 live pups", 26, GREY).move_to([3.6, -0.5, 0])
        pups = VGroup(*[Circle(radius=0.2, stroke_color=GREY, stroke_width=3, fill_opacity=0).move_to([1.0 + i * 0.46, -1.25, 0])
                        for i in range(12)])
        self.play(FadeIn(pl), FadeIn(pups), run_time=0.5)
        self.at("eight yellow")
        self.play(LaggedStart(*[p.animate.set_fill(YELLOW, 1).set_stroke(YELLOW) for p in pups[:8]], lag_ratio=0.1), run_time=0.8)
        self.at("four black")
        self.play(LaggedStart(*[p.animate.set_fill(BLACKC, 1).set_stroke(TEXT) for p in pups[8:]], lag_ratio=0.1), run_time=0.5)
        self.at("Every live yellow mouse")
        het = T("heterozygote", 34, GOLD).move_to([3.6, -2.25, 0])
        self.play(Circumscribe(sq.gdots[1], color=GOLD), Circumscribe(sq.gdots[2], color=GOLD),
                  FadeIn(het), run_time=0.9)
        self.at("That is why none")
        why = T("so none breeds true", 32, TEXT).move_to([3.6, -3.0, 0])
        self.play(FadeIn(why, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Epistasis(SpokenScene):
    """BbEe x BbEe: 16 boxes in four classes; ee hides B; the last two classes merge: 9 black : 3 chocolate : 4 yellow."""

    def construct(self):
        g = Grid4((-2.7, -0.2), 1.25)
        self.at("When two genes act")
        self.play(FadeIn(g.heads), LaggedStart(*[FadeIn(c) for c in g.cells.values()], lag_ratio=0.02), run_time=0.8)
        self.at("which is called")
        ep = T("epistasis", 44, GOLD).move_to([3.6, 3.0, 0])
        self.play(FadeIn(ep, shift=UP * 0.1), run_time=0.4)
        self.at("In Labrador retrievers")
        lr = T("Labrador retrievers", 28, GREY).move_to([3.6, 2.2, 0])
        self.play(FadeIn(lr), run_time=0.3)
        self.at("a dominant B makes black")
        r1 = swatch_row(BLACKC, "dominant B: black pigment", 26, 1.0, 1.4, fill=BLACKC, rim=TEXT)
        self.play(FadeIn(r1, shift=LEFT * 0.2), run_time=0.4)
        self.at("makes brown")
        r2 = swatch_row(CHOC, "recessive b: brown, chocolate", 26, 1.0, 0.65)
        self.play(FadeIn(r2, shift=LEFT * 0.2), run_time=0.4)
        self.at("Cross two black dogs")
        cr = M("BbEe  x  BbEe", 30, TEXT).move_to([3.6, -0.25, 0])
        self.play(FadeIn(cr, shift=UP * 0.1), run_time=0.4)
        self.at("the 16 boxes sort")
        self.play(*g.paint(classes4), run_time=1.0)
        self.at("But a dog with two copies")
        blk = g.block((2, 3), (2, 3), GOLD, 8)
        self.play(Create(blk), run_time=0.5)
        self.at("is yellow")
        r3 = swatch_row(YELLOW, "ee: yellow", 28, 1.0, -1.15)
        r3b = T("whatever its B genotype", 24, GREY)
        left_at(r3b, 1.0, -1.8)
        self.play(FadeIn(r3, shift=LEFT * 0.2), run_time=0.4)
        self.at("whatever its B")
        self.play(FadeIn(r3b), run_time=0.3)
        self.at("the last two classes merge")
        self.play(*g.paint(lab_final), FadeOut(blk), run_time=1.0)
        self.at("9 black")
        t1 = chip("9 black", TEXT, size=24, pad=0.16)
        t2 = chip("3 chocolate", CHOC, size=24, pad=0.16)
        t3 = chip("4 yellow", YELLOW, size=24, pad=0.16)
        tl = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.18)
        fit(tl, max_w=5.7)
        tl.move_to([3.5, -2.85, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.3)
        self.at("3 chocolate")
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.3)
        self.at("4 yellow")
        self.play(FadeIn(t3, shift=UP * 0.1), run_time=0.3)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Regroup(SpokenScene):
    """the same sixteen boxes regrouped: 9:7, 12:3:1, 15:1."""

    def construct(self):
        g = Grid4((-2.7, -0.2), 1.25)
        for k, grp in g.cells.items():  # the scene opens on s04's last picture
            fill, op, stroke, tc = lab_final(*g.dom[k])
            grp[0].set_fill(fill, op).set_stroke(stroke)
            grp[1].set_color(tc)
        self.add(g.heads, g.all)
        self.at("Other interactions regroup")
        title = T("same sixteen boxes", 32, GREY).move_to([3.6, 2.9, 0])
        self.play(*g.paint(neutral), FadeIn(title), run_time=0.8)

        def panel(head, lines):
            h = T(head, 28, TEXT).move_to([3.6, 1.9, 0])
            return h

        # ---- 9 : 7 ----
        self.at("If both genes need")
        h1 = T("both genes need a\ndominant allele to make colour", 28, TEXT, line_spacing=0.8).move_to([3.6, 1.6, 0])
        self.play(FadeIn(h1, shift=UP * 0.1), run_time=0.4)

        def f97(a, b):
            return (BLUE, 0.55, BLUE, TEXT) if (a and b) else (GREY, 0.25, GREY, TEXT)
        r97 = M("9 : 7", 64, GOLD).move_to([3.6, 0.2, 0])
        l97 = VGroup(swatch_row(BLUE, "colour: 9 boxes", 26, 1.4, -1.0), swatch_row(GREY, "no colour: 7 boxes", 26, 1.4, -1.7))
        self.at("make color")
        self.play(*g.paint(f97), run_time=0.7)
        self.at("9 to 7")
        self.play(FadeIn(r97), FadeIn(l97), run_time=0.5)
        # ---- 12 : 3 : 1 ----
        self.at("If a dominant allele at one gene")
        h2 = T("a dominant allele at one\ngene hides the other", 28, TEXT, line_spacing=0.8).move_to([3.6, 1.6, 0])
        self.play(*g.paint(neutral), FadeOut(VGroup(h1, r97, l97)), run_time=0.4)
        self.play(FadeIn(h2), run_time=0.3)

        def f1231(a, b):
            if a:
                return (PURPLE, 0.55, PURPLE, TEXT)
            if b:
                return (ORANGE, 0.55, ORANGE, TEXT)
            return (TEAL, 0.55, TEAL, TEXT)
        r1231 = M("12 : 3 : 1", 64, GOLD).move_to([3.6, 0.2, 0])
        l1231 = VGroup(swatch_row(PURPLE, "12 boxes", 26, 2.4, -0.95), swatch_row(ORANGE, "3 boxes", 26, 2.4, -1.5),
                       swatch_row(TEAL, "1 box", 26, 2.4, -2.05))
        self.at("hides the other")
        self.play(*g.paint(f1231), run_time=0.7)
        self.at("12 to 3 to 1")
        self.play(FadeIn(r1231), FadeIn(l1231), run_time=0.5)
        # ---- 15 : 1 ----
        self.at("If a dominant allele at either")
        h3 = T("a dominant allele at either\ngene is enough", 28, TEXT, line_spacing=0.8).move_to([3.6, 1.6, 0])
        self.play(*g.paint(neutral), FadeOut(VGroup(h2, r1231, l1231)), run_time=0.4)
        self.play(FadeIn(h3), run_time=0.3)

        def f151(a, b):
            return (BLUE, 0.55, BLUE, TEXT) if (a or b) else (GREY, 0.25, GREY, TEXT)
        r151 = M("15 : 1", 64, GOLD).move_to([3.6, 0.2, 0])
        l151 = VGroup(swatch_row(BLUE, "colour: 15 boxes", 26, 1.4, -1.0), swatch_row(GREY, "no colour: 1 box", 26, 1.4, -1.7))
        self.at("is enough")
        self.play(*g.paint(f151), run_time=0.7)
        self.at("15 to 1")
        self.play(FadeIn(r151), FadeIn(l151), run_time=0.5)
        # ---- only the labels ----
        self.at("In every case")
        fin = T("only the labels change", 36, GOLD).move_to([3.6, -2.95, 0])
        self.play(Circumscribe(g.all, color=GOLD, buff=0.15), FadeIn(fin), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """one fixed square, three labellings (3:1, 1:2:1, 2:1), then the genotype -> phenotype map."""

    def construct(self):
        sq = Sq2((-2.7, -0.35), 2.5, ("D", "r"), ("D", "r"))
        self.at("The boxes never changed")
        self.play(FadeIn(VGroup(*sq.tiles)), FadeIn(VGroup(*sq.top_dots, *sq.left_dots)), run_time=0.6)
        self.play(*[FadeIn(g) for g in sq.gdots], run_time=0.5)
        lab = T("genotype boxes", 32, GREY).move_to([3.6, 2.7, 0])
        self.play(FadeIn(lab), run_time=0.3)
        self.at("only their labels")
        self.play(Indicate(lab, color=GOLD), run_time=0.7)

        def tint(k, col, op=0.5):
            return sq.tiles[k].animate.set_fill(col, op).set_stroke(col)

        # 3 : 1
        self.at("One allele hides the other")
        r31 = M("3 : 1", 72, GOLD).move_to([3.6, 0.7, 0])
        l31 = T("one allele hides the other", 28, TEXT).move_to([3.6, -0.5, 0])
        self.play(tint(0, BLUE), tint(1, BLUE), tint(2, BLUE), tint(3, ORANGE), FadeIn(r31), FadeIn(l31), run_time=0.7)
        # 1 : 2 : 1
        self.at("Neither hides")
        r121 = M("1 : 2 : 1", 72, GOLD).move_to([3.6, 0.7, 0])
        l121 = T("neither hides", 28, TEXT).move_to([3.6, -0.5, 0])
        self.play(tint(1, PURPLE), tint(2, PURPLE), ReplacementTransform(r31, r121), ReplacementTransform(l31, l121), run_time=0.7)
        # 2 : 1
        self.at("one class dies")
        r21 = M("2 : 1", 72, GOLD).move_to([3.6, 0.7, 0])
        l21 = T("one class dies", 28, RED).move_to([3.6, -0.5, 0])
        X = xmark(sq.ctrs[0] + [0, -0.2, 0], 0.8, RED, 12)
        self.play(tint(1, BLUE), tint(2, BLUE), tiny_dim(sq.tiles[0]), Create(X),
                  ReplacementTransform(r121, r21), ReplacementTransform(l121, l21), run_time=0.7)
        self.at("Keep this rule")
        self.play(FadeOut(VGroup(r21, l21, lab)), run_time=0.4)
        self.at("Segregation never stops working")
        sg = T("same boxes, every time", 32, GREEN).move_to([3.6, 2.1, 0])
        self.play(FadeIn(sg, shift=UP * 0.1), Circumscribe(VGroup(*sq.tiles), color=GREEN, buff=0.15), run_time=1.0)
        self.at("the map from genotype")
        gt = chip("genotype", GREY, size=36, pad=0.28).move_to([3.6, 0.6, 0])
        pt = chip("phenotype", GREY, size=36, pad=0.28).move_to([3.6, -2.2, 0])
        mp = Arrow([3.6, 0.0, 0], [3.6, -1.55, 0], buff=0, color=GOLD, stroke_width=9, tip_length=0.35)
        ml = T("map", 44, GOLD, weight=BOLD).next_to(mp, RIGHT, buff=0.35)
        self.play(FadeIn(gt), run_time=0.3)
        self.play(GrowArrow(mp), FadeIn(ml), FadeIn(pt), run_time=0.6)
        self.at("changes")
        self.play(Indicate(VGroup(mp, ml), color=GOLD, scale_factor=1.15), run_time=0.8)
        self.finish()


def tiny_dim(tile):
    return tile.animate.set_fill(GREY, 0.15).set_stroke(RED)


class S07End(EndCard):
    LINE = "Segregation never stops working, only the map from genotype to phenotype changes."
