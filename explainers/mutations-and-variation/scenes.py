"""Why no two living things match  (grade 7 Life Science explainer, mutations-and-variation)

COLOR MAP (one color per concept, whole film)
  LEAF   = white oak leaves (s01, s02 only)
  YELLOW = vocabulary words (trait, population, variation, mutation, body cells, sex cells, random)
  BLUE   = genes and DNA bases
  PINK   = the environment (food and health, where it lives)
  ORANGE = a mutation (a changed base, a mutated cell, the mutation chip)
  PURPLE = sex cells (eggs and sperm)
  GREEN  = helps (also the closing answer)
  RED    = harms, questions, "not passed on" marks
  GREY   = body cells, parent and child outlines, no difference, neutral labels
  TEXT   = plain labels
"""
from bp_style import *  # noqa: F401,F403

LEAF = "#B8D86B"
ORANGE = "#FF9F43"
PURPLE = "#B07CFF"
PINK = "#F28CB1"


def word(text, size=32):
    return T(text, size, YELLOW, weight=BOLD)


def arrow(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22)


def leaf(x, base, length, w=0.62):
    """Schematic oak leaf: blade, rounded lobes and a midvein. (x, base) is the stalk end. Not to scale."""
    cy = base + length / 2
    parts = [Ellipse(width=w, height=length, stroke_width=0, fill_color=LEAF, fill_opacity=0.9).move_to([x, cy, 0])]
    for f in (0.28, 0.5, 0.72):
        for sgn in (-1, 1):
            parts.append(Circle(radius=0.15, stroke_width=0, fill_color=LEAF, fill_opacity=0.9)
                         .move_to([x + sgn * w * 0.5, base + length * f, 0]))
    parts.append(Line([x, base + 0.05, 0], [x, base + length - 0.08, 0], color=BG, stroke_width=2))
    return VGroup(*parts)


class S00Title(TitleCard):
    LESSON = "Mutations and variation"
    TITLE = "Why no two living things match"


# ----------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        lens = [2.0, 2.6, 2.3, 1.8, 2.9, 2.2, 2.5, 1.9, 2.7, 2.4]
        xs = [-4.4 + 1.05 * i for i in range(10)]
        base = -1.2
        leaves = VGroup(*[leaf(x, base, L) for x, L in zip(xs, lens)])
        cap = T("ten leaves from one white oak (not to scale)", 26, GREY).move_to([0, 3.15, 0])
        self.at("ten leaves")
        self.play(FadeIn(cap), FadeIn(leaves, lag_ratio=0.15, shift=UP * 0.15), run_time=2.0)
        self.at("rounded lobes")
        self.play(Indicate(leaves, color=YELLOW, scale_factor=1.04), run_time=1.1)
        rx = -5.9
        ruler = VGroup(Rectangle(width=0.32, height=3.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([rx, base + 1.7, 0]))
        for k in range(1, 9):
            ruler.add(Line([rx - 0.16, base + 0.4 * k, 0], [rx - 0.16 + (0.18 if k % 2 else 0.3), base + 0.4 * k, 0], color=GREY, stroke_width=2))
        rl = T("ruler", 24, GREY).move_to([rx, base - 0.4, 0])
        self.at("with a ruler")
        self.play(FadeIn(ruler), FadeIn(rl), run_time=0.8)
        top_hi, top_lo = base + max(lens), base + min(lens)
        d1 = DashedLine([-5.2, top_hi, 0], [5.3, top_hi, 0], color=YELLOW, stroke_width=3)
        d2 = DashedLine([-5.2, top_lo, 0], [5.3, top_lo, 0], color=YELLOW, stroke_width=3)
        gap = DoubleArrow([5.65, top_lo, 0], [5.65, top_hi, 0], color=YELLOW, buff=0, stroke_width=4, tip_length=0.18)
        dl = T("different lengths and shapes", 28, YELLOW, weight=BOLD).move_to([0, 2.45, 0])
        self.at("different lengths")
        self.play(Create(d1), Create(d2), run_time=0.8)
        self.play(GrowFromCenter(gap), FadeIn(dl, shift=DOWN * 0.1), run_time=0.8)
        q1 = T("Why is no living thing exactly like another", 34, TEXT, weight=BOLD)
        q1m = T("?", 40, RED, weight=BOLD)
        g1 = VGroup(q1, q1m).arrange(RIGHT, buff=0.2).move_to([0, -2.3, 0])
        self.at("exactly like another")
        self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.9)
        q2 = T("Are all mutations bad", 34, ORANGE, weight=BOLD)
        q2m = T("?", 40, RED, weight=BOLD)
        g2 = VGroup(q2, q2m).arrange(RIGHT, buff=0.2).move_to([0, -3.1, 0])
        self.at("all mutations")
        self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S02Variation(SpokenScene):
    def construct(self):
        tw = word("trait", 34)
        td = T("a feature of a living thing: color, shape, height", 26)
        l1 = VGroup(tw, td).arrange(RIGHT, buff=0.3).move_to([0, 3.1, 0])
        self.at("A trait is")
        self.play(FadeIn(l1, shift=DOWN * 0.1), run_time=1.2)
        rect = RoundedRectangle(corner_radius=0.3, width=11.6, height=4.3, stroke_color=GREY, stroke_width=4).move_to([0, -0.6, 0])
        pw = word("population", 34)
        pd = T("a group of the same kind of living thing in one area", 26)
        l2 = VGroup(pw, pd).arrange(RIGHT, buff=0.3).move_to([0, 2.15, 0])
        lens = [1.9, 2.3, 2.0, 1.7, 2.2, 2.4, 1.8]
        xs = [-4.5 + 1.5 * i for i in range(7)]
        base = -2.45
        leaves = VGroup(*[leaf(x, base, L, 0.72) for x, L in zip(xs, lens)])
        self.at("A population is")
        self.play(FadeIn(l2, shift=DOWN * 0.1), Create(rect), run_time=1.0)
        self.play(FadeIn(leaves, lag_ratio=0.12), run_time=1.2)
        same = T("same basic features: rounded lobes", 28, GREEN, weight=BOLD).move_to([0, 1.05, 0])
        self.at("share the same basic")
        self.play(FadeIn(same, shift=DOWN * 0.1), Indicate(leaves, color=GREEN, scale_factor=1.03), run_time=1.2)
        top_hi, top_lo = base + max(lens), base + min(lens)
        d1 = DashedLine([-5.5, top_hi, 0], [5.3, top_hi, 0], color=YELLOW, stroke_width=3)
        d2 = DashedLine([-5.5, top_lo, 0], [5.3, top_lo, 0], color=YELLOW, stroke_width=3)
        gap = DoubleArrow([5.5, top_lo, 0], [5.5, top_hi, 0], color=YELLOW, buff=0, stroke_width=4, tip_length=0.16)
        self.at("varies a little")
        self.play(Create(d1), Create(d2), GrowFromCenter(gap), run_time=1.0)
        vw = word("variation", 34)
        vd = T("small differences among members of a population", 26)
        l3 = VGroup(vw, vd).arrange(RIGHT, buff=0.3).move_to([0, -3.15, 0])
        self.at("Variation means")
        self.play(FadeIn(l3, shift=UP * 0.1), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S03Genes(SpokenScene):
    def construct(self):
        base = -2.6
        bw, bh = 1.7, 0.52
        xa, xb = -3.6, 0.5
        title = T("height (in this sketch)", 28, GREY).move_to([-1.6, 3.15, 0])
        self.add(title)
        lab_a = T("child A", 26, GREY).move_to([xa, base - 0.4, 0])
        lab_b = T("child B", 26, GREY).move_to([xb, base - 0.4, 0])
        ground = Line([-5.6, base, 0], [2.3, base, 0], color=GREY, stroke_width=3)
        self.play(Create(ground), FadeIn(lab_a), FadeIn(lab_b), run_time=0.6)
        gchip = chip("genes", BLUE, 30).move_to([4.2, 1.9, 0])
        gdef = T("a gene carries the\ncode for a protein", 24, TEXT, line_spacing=0.85).next_to(gchip, DOWN, buff=0.2)
        self.at("comes from genes")
        self.play(FadeIn(gchip, scale=0.8), run_time=0.7)
        self.at("gene carries")
        self.play(FadeIn(gdef, shift=UP * 0.1), run_time=0.8)
        echip = chip("environment", PINK, 30).move_to([4.2, -0.5, 0])
        edef = T("food and health", 26, TEXT).next_to(echip, DOWN, buff=0.2)
        self.at("from the environment")
        self.play(FadeIn(echip, scale=0.8), FadeIn(edef, shift=UP * 0.1), run_time=0.9)
        self.at("shows both")
        self.play(Indicate(title, color=YELLOW, scale_factor=1.1), run_time=0.8)

        def block(x, y, color):
            return Rectangle(width=bw, height=bh, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.45).move_to([x, y, 0])

        n = 5
        ga = [block(xa, base + bh * (i + 0.5), BLUE) for i in range(n)]
        gb = [block(xb, base + bh * (i + 0.5), BLUE) for i in range(n)]
        gb[1].set_fill(BLUE, opacity=0.3); gb[3].set_fill(BLUE, opacity=0.6)
        self.at("genes add a little")
        self.play(FadeIn(VGroup(*ga), lag_ratio=0.25), FadeIn(VGroup(*gb), lag_ratio=0.25), run_time=1.8)
        ha, hb = 1.6, 0.6
        ta = Rectangle(width=bw, height=ha, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.45).move_to([xa, base + n * bh + ha / 2, 0])
        tb = Rectangle(width=bw, height=hb, stroke_color=PINK, stroke_width=3, fill_color=PINK, fill_opacity=0.45).move_to([xb, base + n * bh + hb / 2, 0])
        self.at("Food and health")
        self.play(GrowFromEdge(ta, DOWN), GrowFromEdge(tb, DOWN), run_time=1.4)
        self.at("very similar genes")
        self.play(Indicate(VGroup(*ga, *gb), color=BLUE, scale_factor=1.06), run_time=1.0)
        topa, topb = base + n * bh + ha, base + n * bh + hb
        d1 = DashedLine([xa - 1.0, topa, 0], [xb + 1.2, topa, 0], color=YELLOW, stroke_width=3)
        d2 = DashedLine([xa - 1.0, topb, 0], [xb + 1.2, topb, 0], color=YELLOW, stroke_width=3)
        gap = DoubleArrow([xb + 1.5, topb, 0], [xb + 1.5, topa, 0], color=YELLOW, buff=0, stroke_width=4, tip_length=0.16)
        dh = T("different heights", 28, YELLOW, weight=BOLD).move_to([xa + 2.0, topa + 0.4, 0])
        self.at("different heights")
        self.play(Create(d1), Create(d2), GrowFromCenter(gap), FadeIn(dh, shift=DOWN * 0.1), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S04Mutation(SpokenScene):
    def construct(self):
        n = 8
        cx, cy = -2.2, 2.2
        blocks = VGroup(*[Square(side_length=0.62, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.35) for _ in range(n)])
        blocks.arrange(RIGHT, buff=0.08).move_to([cx, cy, 0])
        lab = word("DNA sequence", 30).move_to([cx, cy + 0.95, 0])
        mw = word("mutation", 40).move_to([4.2, cy + 0.9, 0])
        self.at("New variation starts")
        self.play(FadeIn(mw, scale=0.8), run_time=0.8)
        self.at("change in the")
        self.play(FadeIn(lab, shift=DOWN * 0.1), FadeIn(blocks, lag_ratio=0.1), run_time=1.4)
        order = T("order of the bases", 26, BLUE).move_to([cx, cy - 0.85, 0])
        self.at("the order of")
        self.play(FadeIn(order, shift=UP * 0.1), Indicate(blocks, color=BLUE, scale_factor=1.04), run_time=1.0)
        gene = SurroundingRectangle(VGroup(*blocks[2:6]), color=BLUE, buff=0.1, stroke_width=4)
        gl = T("a gene", 26, BLUE).move_to([cx, cy - 0.85, 0])
        prot = RoundedRectangle(corner_radius=0.2, width=2.4, height=0.9, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.25).move_to([cx, 0.0, 0])
        pl = T("protein", 28, TEXT).move_to(prot)
        pa = arrow([cx, cy - 1.2, 0], [cx, 0.55, 0], BLUE)
        newb = Square(side_length=0.62, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.8).move_to(blocks[4])
        newp = RoundedRectangle(corner_radius=0.45, width=1.9, height=1.3, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.25).move_to(prot)
        note = T("can change", 24, ORANGE).move_to([cx, -0.95, 0])
        self.at("It can change")
        self.play(FadeOut(order), Create(gene), FadeIn(gl), run_time=0.6)
        self.play(Transform(blocks[4], newb), run_time=0.6)
        self.at("the protein")
        self.play(GrowArrow(pa), FadeIn(prot), FadeIn(pl), run_time=0.7)
        self.play(Transform(prot, newp), FadeIn(note, shift=UP * 0.1), run_time=0.8)
        causes = [("copying mistakes", 1.6), ("radiation", 0.7), ("some chemicals", -0.2)]
        chips = [chip(txt, ORANGE, 26).move_to([4.2, y, 0]) for txt, y in causes]
        self.at("Copying mistakes")
        self.play(FadeIn(chips[0], shift=LEFT * 0.2), run_time=0.6)
        self.at("radiation")
        self.play(FadeIn(chips[1], shift=LEFT * 0.2), run_time=0.6)
        self.at("some chemicals")
        self.play(FadeIn(chips[2], shift=LEFT * 0.2), run_time=0.6)
        self.at("can cause")
        self.play(Indicate(VGroup(*chips), color=YELLOW, scale_factor=1.05), run_time=0.8)
        rw = word("random", 36)
        eq = T("= happens by chance", 30, TEXT)
        rline = VGroup(rw, eq).arrange(RIGHT, buff=0.25).move_to([-1.6, -1.95, 0])
        self.at("Mutations are random")
        self.play(FadeIn(rw, scale=0.8), run_time=0.7)
        self.at("by chance")
        self.play(FadeIn(eq, shift=LEFT * 0.15), run_time=0.8)
        nb = T("not because", 28, TEXT)
        need = chip("a living thing needs it", GREY, 26)
        nline = VGroup(nb, need).arrange(RIGHT, buff=0.3).move_to([-1.6, -3.0, 0])
        slash = Line(need.get_corner(DL) + [-0.1, -0.05, 0], need.get_corner(UR) + [0.1, 0.05, 0], color=RED, stroke_width=7)
        self.at("not because a living")
        self.play(FadeIn(nline, shift=UP * 0.1), run_time=0.8)
        self.play(Create(slash), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S05Where(SpokenScene):
    def construct(self):
        parent = RoundedRectangle(corner_radius=0.3, width=7.6, height=5.6, stroke_color=GREY, stroke_width=4).move_to([-2.5, -0.1, 0])
        pl = T("parent", 28, GREY).move_to([-2.5, 2.35, 0])
        child = RoundedRectangle(corner_radius=0.3, width=3.0, height=3.4, stroke_color=GREY, stroke_width=4).move_to([4.6, -0.5, 0])
        cl = T("child", 28, GREY).move_to([4.6, 0.8, 0])
        self.at("Where a mutation")
        self.play(Create(parent), FadeIn(pl), Create(child), FadeIn(cl), run_time=1.0)
        bxs = [-5.3, -4.2, -3.1]
        by = 1.0
        body = VGroup(*[Circle(radius=0.45, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([x, by, 0]) for x in bxs])
        bw_ = word("body cells", 30).move_to([-4.2, 1.85, 0])
        bd = T("all cells except\neggs and sperm", 24, TEXT, line_spacing=0.85).move_to([-0.8, by, 0])
        self.at("Body cells are")
        self.play(FadeIn(bw_, shift=DOWN * 0.1), FadeIn(body, lag_ratio=0.25), run_time=1.0)
        self.play(FadeIn(bd, shift=UP * 0.1), run_time=0.7)
        skl = T("skin cell", 24, GREY).move_to([-5.3, 0.3, 0])
        self.at("such as skin")
        self.play(FadeIn(skl, shift=UP * 0.1), Indicate(body[0], color=YELLOW, scale_factor=1.25), run_time=0.9)
        sxs = [-5.3, -4.2]
        sy = -1.5
        sex = VGroup(*[Circle(radius=0.45, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.3).move_to([x, sy, 0]) for x in sxs])
        sw_ = word("sex cells", 30).move_to([-4.75, -0.7, 0])
        sd = T("eggs and sperm", 24, TEXT).move_to([-4.75, -2.3, 0])
        self.at("Sex cells are")
        self.play(FadeIn(sw_, shift=DOWN * 0.1), FadeIn(sex, lag_ratio=0.25), run_time=1.0)
        self.play(FadeIn(sd, shift=UP * 0.1), run_time=0.6)
        dot_b = Dot(radius=0.17, color=ORANGE).move_to(body[0])
        stay = T("stays in that person", 26, ORANGE, weight=BOLD).move_to([-1.3, -2.35, 0])
        self.at("mutation in a skin")
        self.play(FadeOut(bd), FadeIn(dot_b, scale=2.0), run_time=0.7)
        xmark = VGroup(Line([-0.3, -0.3, 0], [0.3, 0.3, 0]), Line([-0.3, 0.3, 0], [0.3, -0.3, 0])).set_color(RED).set_stroke(width=8).move_to([1.3, by, 0])
        a_stay = Line([-2.45, by, 0], [0.9, by, 0], color=ORANGE, stroke_width=5)
        self.at("stays in that")
        self.play(Create(a_stay), run_time=0.6)
        self.play(FadeIn(xmark, scale=1.5), FadeIn(stay, shift=UP * 0.1), run_time=0.6)
        dot_s = Dot(radius=0.17, color=ORANGE).move_to(sex[1])
        cpos = [[4.0, -1.7], [5.2, -1.7], [4.0, -0.95], [5.2, -0.95]]
        ccells = VGroup(*[Circle(radius=0.38, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.18).move_to([x, y, 0]) for x, y in cpos])
        cc = ccells[0]
        a_pass = arrow([-3.55, sy, 0], [3.1, sy, 0], ORANGE)
        self.at("mutation in a sex")
        self.play(FadeOut(stay), FadeIn(dot_s, scale=2.0), run_time=0.7)
        self.at("pass to offspring")
        self.play(GrowArrow(a_pass), FadeIn(ccells), run_time=0.8)
        moving = dot_s.copy()
        self.play(moving.animate.move_to(cc), run_time=0.8)
        marks = VGroup(*[Dot(radius=0.14, color=ORANGE).move_to(c) for c in ccells[1:]])
        self.play(FadeIn(marks, lag_ratio=0.2), run_time=0.6)
        passed = T("can pass to offspring", 26, ORANGE, weight=BOLD).move_to([-1.3, -2.35, 0])
        kid = T("offspring: the young\nmutation in every cell", 22, TEXT, line_spacing=0.85).move_to([4.6, 0.1, 0])
        self.play(FadeIn(passed, shift=UP * 0.1), FadeIn(kid), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------------------------
class S06Effect(SpokenScene):
    def construct(self):
        title = T("Does a mutation help?", 40, YELLOW, weight=BOLD).move_to([0, 3.15, 0])
        mut = chip("a mutation", ORANGE, 30).move_to([-4.3, 1.55, 0])
        self.at("Does a mutation")
        self.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(mut, scale=0.8), run_time=0.9)
        outs = [("helps", GREEN, 1.7), ("makes no difference", GREY, 0.3), ("harms", RED, -1.1)]
        oc = [chip(txt, col, 30).move_to([2.4, y, 0]) for txt, col, y in outs]
        q = [T("?", 34, RED, weight=BOLD).next_to(c, RIGHT, buff=0.2) for c in oc]
        arrs = [Line(mut.get_right() + [0.1, 0, 0], c.get_left() + [-0.1, 0, 0], color=GREY, stroke_width=3) for c in oc]
        self.play(*[Create(a) for a in arrs], FadeIn(VGroup(*oc), lag_ratio=0.2), FadeIn(VGroup(*q), lag_ratio=0.2), run_time=1.2)
        e1 = chip("the living thing", PINK, 26)
        e2 = chip("where it lives", PINK, 26)
        eg = VGroup(T("depends on", 26, TEXT), e1, T("and", 26, TEXT), e2).arrange(RIGHT, buff=0.3).move_to([0, -3.2, 0])
        self.at("depends on")
        self.play(FadeIn(eg, shift=UP * 0.1), run_time=1.2)
        card = RoundedRectangle(corner_radius=0.15, width=3.4, height=2.0, stroke_color=GREY, stroke_width=3).move_to([-4.3, -0.55, 0])
        ys = [-0.05 - 0.38 * i for i in range(4)]
        bars = VGroup(*[Line([-5.7, y, 0], [-5.7 + w, y, 0], color=GREY, stroke_width=6) for y, w in zip(ys, [2.6, 2.0, 2.4, 1.8])])
        card_l = T("recipe", 24, GREY).next_to(card, UP, buff=0.12)
        self.at("misprint in a recipe")
        self.play(Create(card), FadeIn(card_l), Create(bars), run_time=1.2)
        mis = Line([-5.7, ys[2], 0], [-5.7 + 2.4, ys[2], 0], color=ORANGE, stroke_width=8)
        self.play(Transform(bars[2], mis), run_time=0.6)
        self.at("change little")
        self.play(FadeOut(q[1]), Indicate(oc[1], color=GREY, scale_factor=1.1), run_time=0.8)
        self.at("ruin the dish")
        self.play(FadeOut(q[2]), Indicate(oc[2], color=RED, scale_factor=1.1), run_time=0.8)
        self.at("rare one")
        self.play(FadeOut(q[0]), Indicate(oc[0], color=GREEN, scale_factor=1.1), run_time=0.8)
        wr = T("a recipe has a writer", 24, GREY).move_to([-4.3, -2.0, 0])
        no = T("no one chooses a mutation", 26, ORANGE, weight=BOLD).move_to([2.4, -2.2, 0])
        self.at("has a writer")
        self.play(FadeIn(wr, shift=UP * 0.1), run_time=0.7)
        self.at("no one chooses")
        self.play(FadeIn(no, shift=UP * 0.1), run_time=0.8)
        self.at("can help")
        self.play(Indicate(oc[0], color=GREEN, scale_factor=1.12), Indicate(oc[2], color=RED, scale_factor=1.12),
                  Indicate(oc[1], color=GREY, scale_factor=1.12), run_time=0.8)
        fin = T("Not all mutations are bad.", 40, GREEN, weight=BOLD).move_to([0, 3.15, 0])
        self.at("not all mutations")
        self.play(FadeOut(title), FadeIn(fin, shift=DOWN * 0.1), run_time=0.9)
        self.finish()


class S07End(EndCard):
    LINE = "A mutation can help, harm or make no difference."
