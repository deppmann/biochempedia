"""Domains, kingdoms and DNA: why mushrooms are not plants  (grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole film)
  ORANGE = fungi / the mushroom
  GREEN  = plants (and the green chloroplast part)
  PURPLE = animals (and "you")
  BLUE   = the nucleus and DNA
  GOLD   = the cell wall, and the common ancestor
  TEAL   = the three domain boxes
  PINK   = new tools / new evidence
  YELLOW = the question, highlights, "matching" lines
  RED    = "no", crossed out, "not"
  GREY   = outlines, neutral structure, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E58FAF"


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color, x=0, y=0, op=0.1, sw=3):
    return RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def cell(r=0.9, nucleus=False, wall=False, chl=0, color=GREY, x=0, y=0):
    """A simple outlined cell: membrane circle, optional wall ring, nucleus circle, chloroplast ovals."""
    g = VGroup()
    g.mem = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.10)
    g.add(g.mem)
    g.wall = Circle(radius=r + 0.15, stroke_color=GOLD, stroke_width=6)
    g.nuc = Circle(radius=r * 0.36, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.35)
    g.chls = VGroup()
    if wall:
        g.add(g.wall)
    if nucleus:
        g.nuc.move_to(g.mem.get_center() + r * 0.1 * UP)
        g.add(g.nuc)
    spots = [(-0.55, -0.45), (0.55, -0.45), (0.0, -0.62), (-0.62, 0.35), (0.62, 0.35)]
    for i in range(chl):
        sx, sy = spots[i]
        e = Ellipse(width=r * 0.5, height=r * 0.28, stroke_color=GREEN, stroke_width=3,
                    fill_color=GREEN, fill_opacity=0.6).move_to(g.mem.get_center() + np.array([sx * r, sy * r, 0]))
        g.chls.add(e)
    g.add(g.chls)
    g.move_to([x, y, 0])
    return g


def cross_over(mob, color=RED, w=7):
    c = Cross(mob, stroke_color=color, stroke_width=w)
    return c


def mushroom(x, y):
    stalk = Rectangle(width=0.55, height=1.3, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.25)
    cap = Sector(radius=1.25, angle=PI, start_angle=0, stroke_color=ORANGE, stroke_width=4,
                 fill_color=ORANGE, fill_opacity=0.4)
    cap.stretch(0.75, 1, about_edge=DOWN)
    stalk.move_to([0, 0, 0])
    cap.next_to(stalk, UP, buff=0)
    g = VGroup(stalk, cap)
    g.move_to([x, y, 0])
    return g


class S00Title(TitleCard):
    LESSON = "Domains, kingdoms and DNA"
    TITLE = "Why mushrooms are not plants"


# ---------------------------------------------------------------------------------------------
class S01Mushroom(SpokenScene):
    def construct(self):
        log = box(5.4, 0.9, GREY, -3.6, -2.4, op=0.35)
        log_l = T("dead log", 26, GREY).move_to([-3.6, -3.1, 0])
        mush = mushroom(-3.6, -1.35)
        mush.align_to(log, UP).shift(UP * 0.0)
        mush.next_to(log, UP, buff=0)
        mush_l = T("mushroom", 30, ORANGE).next_to(mush, UP, buff=0.3)
        self.at("pops up")
        self.play(FadeIn(log), FadeIn(log_l), run_time=0.4)
        self.play(GrowFromEdge(mush, DOWN), FadeIn(mush_l), run_time=0.9)

        chips = VGroup(*[chip(w, GREY, size=32) for w in ("walk", "swim", "fly")]).arrange(DOWN, buff=0.45).move_to([3.0, 0.2, 0])
        self.at("does not walk")
        self.play(FadeIn(chips[0]), run_time=0.3)
        x0 = cross_over(chips[0])
        self.play(Create(x0), run_time=0.3)
        self.at("swim or fly")
        self.play(FadeIn(chips[1]), FadeIn(chips[2]), run_time=0.3)
        x1, x2 = cross_over(chips[1]), cross_over(chips[2])
        self.play(Create(x1), Create(x2), run_time=0.4)

        plants = chip("plants", GREEN, size=36).move_to([3.0, 0.9, 0])
        a1 = arr([-1.6, 0.0, 0], [1.5, 0.9, 0], YELLOW)
        self.at("grouped mushrooms with plants")
        self.play(FadeOut(chips), FadeOut(x0), FadeOut(x1), FadeOut(x2), run_time=0.3)
        self.play(FadeIn(plants), GrowArrow(a1), run_time=0.7)

        own = chip("their own kingdom", ORANGE, size=32).move_to([3.0, -1.1, 0])
        a2 = arr([-1.6, -0.6, 0], [1.1, -1.1, 0], ORANGE)
        self.at("their own kingdom")
        xp = cross_over(plants)
        self.play(Create(xp), a1.animate.set_color(RED), run_time=0.4)
        self.play(FadeIn(own), GrowArrow(a2), run_time=0.7)

        you = chip("you", PURPLE, size=28).move_to([0.7, 0.5, 0])
        mu = chip("mushroom", ORANGE, size=28).move_to([2.85, 0.5, 0])
        oak = chip("oak tree", GREEN, size=28).move_to([5.4, 0.5, 0])
        self.at("closer to you")
        self.play(FadeOut(VGroup(plants, a1, xp, own, a2)), run_time=0.3)
        self.play(FadeIn(you), FadeIn(mu), FadeIn(oak), run_time=0.6)
        near = T("closer", 30, YELLOW).move_to([1.53, -0.3, 0])
        far = T("farther", 30, GREY).move_to([4.15, -0.3, 0])
        self.play(FadeIn(near), run_time=0.4)
        self.play(FadeIn(far), run_time=0.3)

        q = VGroup(T("Why are mushrooms no longer called plants,", 38, YELLOW),
                   T("and how can DNA change", 38, YELLOW),
                   T("where a living thing belongs?", 38, YELLOW)).arrange(DOWN, buff=0.3).move_to([0, 0, 0])
        self.at("How did that happen")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Clues(SpokenScene):
    def construct(self):
        pos = [(-3.2, 1.75), (3.2, 1.75), (-3.2, -1.75), (3.2, -1.75)]
        frames = [box(5.9, 3.1, GREY, x, y, op=0.05) for x, y in pos]
        nums = [T(str(i + 1), 30, GREY, weight=BOLD).move_to([x - 2.6, y + 1.2, 0]) for i, (x, y) in enumerate(pos)]
        self.at("Scientists sort")
        self.play(*[FadeIn(f) for f in frames], *[FadeIn(n) for n in nums], run_time=0.8)

        # clue 1
        (cx, cy) = pos[0]
        c1 = cell(0.85, nucleus=True, x=cx - 1.6, y=cy - 0.1)
        l1 = T("nucleus", 32, BLUE).move_to([cx + 1.3, cy + 0.45, 0])
        l1b = T("holds the DNA", 26, GREY).move_to([cx + 1.3, cy - 0.15, 0])
        self.at("have a nucleus")
        self.play(FadeIn(c1.mem), run_time=0.4)
        self.play(GrowFromCenter(c1.nuc), FadeIn(l1), run_time=0.5)
        self.at("holds its DNA")
        self.play(FadeIn(l1b), Indicate(c1.nuc, color=BLUE, scale_factor=1.25), run_time=0.7)

        # clue 2
        (cx, cy) = pos[1]
        c2 = cell(0.85, nucleus=True, wall=True, chl=3, x=cx - 1.6, y=cy - 0.1)
        l2 = T("cell wall", 30, GOLD).move_to([cx + 1.2, cy + 0.6, 0])
        l2b = T("chloroplast", 30, GREEN).move_to([cx + 1.2, cy - 0.5, 0])
        self.at("which cell parts")
        self.play(FadeIn(c2.mem), FadeIn(c2.nuc), run_time=0.5)
        self.at("a stiff layer")
        self.play(Create(c2.wall), FadeIn(l2), run_time=0.7)
        self.at("a green part")
        self.play(FadeIn(c2.chls), FadeIn(l2b), run_time=0.7)

        # clue 3
        (cx, cy) = pos[2]
        one = Circle(radius=0.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1).move_to([cx - 1.6, cy + 0.25, 0])
        many = VGroup(*[Circle(radius=0.32, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.1)
                        .move_to([cx + 1.3 + dx * 0.64, cy + 0.25 + dy * 0.64, 0])
                        for dx, dy in ((-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5))])
        lo = T("one cell", 28, TEXT).move_to([cx - 1.6, cy - 0.85, 0])
        lm = T("many cells", 28, TEXT).move_to([cx + 1.3, cy - 0.85, 0])
        self.at("one cell or many")
        self.play(FadeIn(one), FadeIn(lo), run_time=0.5)
        self.play(FadeIn(many, lag_ratio=0.2), FadeIn(lm), run_time=0.6)

        # clue 4
        (cx, cy) = pos[3]
        f1 = chip("makes its own food", TEXT, size=28).move_to([cx, cy + 0.55, 0])
        f2 = chip("takes food in", TEXT, size=28).move_to([cx, cy - 0.55, 0])
        self.at("make its own food")
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.5)
        self.at("take food in")
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Domains(SpokenScene):
    def construct(self):
        Y, H = -0.2, 5.0
        left = box(6.05, H, GREY, -3.075, Y, op=0.06)
        right = box(5.9, H, TEAL, 3.15, Y, op=0.08)
        cl = cell(0.8, x=-3.075, y=0.5)
        cr = cell(0.8, nucleus=True, x=3.15, y=0.5)
        ll = T("no nucleus", 32, TEXT).move_to([-3.075, -0.9, 0])
        lr = T("nucleus", 32, BLUE).move_to([3.15, -0.9, 0])
        self.at("splits life")
        self.play(FadeIn(left), FadeIn(right), run_time=0.6)
        self.play(FadeIn(cl), FadeIn(cr), FadeIn(ll), FadeIn(lr), run_time=0.7)

        b1 = box(2.9, H, TEAL, -4.6, Y, op=0.08)
        b2 = box(2.9, H, TEAL, -1.5, Y, op=0.08)
        cl1 = cell(0.7, x=-4.6, y=0.5)
        cl2 = cell(0.7, x=-1.5, y=0.5)
        ll1 = T("no nucleus", 28, TEXT).move_to([-4.6, -0.9, 0])
        ll2 = T("no nucleus", 28, TEXT).move_to([-1.5, -0.9, 0])
        self.at("Genes and chemistry")
        self.play(ReplacementTransform(left, VGroup(b1, b2)), ReplacementTransform(cl, VGroup(cl1, cl2)),
                  ReplacementTransform(ll, VGroup(ll1, ll2)), run_time=1.0)

        tb = T("Bacteria", 34, TEAL, weight=BOLD).move_to([-4.6, 1.85, 0])
        ta = T("Archaea", 34, TEAL, weight=BOLD).move_to([-1.5, 1.85, 0])
        te = T("Eukarya", 34, TEAL, weight=BOLD).move_to([3.15, 1.85, 0])
        dl = T("3 domains", 32, TEAL).move_to([0, 3.15, 0])
        self.at("three domains")
        self.play(FadeIn(dl, shift=DOWN * 0.1), run_time=0.4)
        self.at("Bacteria")
        self.play(FadeIn(tb), run_time=0.3)
        self.at("Archaea")
        self.play(FadeIn(ta), run_time=0.3)
        self.at("and Eukarya")
        self.play(FadeIn(te), run_time=0.3)

        self.at("whose cells have a nucleus")
        self.play(Indicate(cr.nuc, color=BLUE, scale_factor=1.3), run_time=0.7)

        names = [("protists", TEXT), ("fungi", ORANGE), ("plants", GREEN), ("animals", PURPLE)]
        ks = VGroup(*[chip(n, c, size=30) for n, c in names])
        for k, (px, py) in zip(ks, [(1.7, 0.7), (4.6, 0.7), (1.7, -0.8), (4.6, -0.8)]):
            k.move_to([px, py, 0])
        note = T("Many textbooks use six kingdoms", 26, GREY).move_to([0, -3.15, 0])
        self.at("six kingdoms")
        self.play(FadeOut(cr), FadeOut(lr), FadeIn(note), run_time=0.4)
        self.at("four are inside")
        self.play(FadeIn(ks, lag_ratio=0.25), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Mushroom(SpokenScene):
    def construct(self):
        mc = cell(1.5, nucleus=True, wall=True, color=ORANGE, x=-3.6, y=0.6)
        title = T("mushroom cell", 30, ORANGE).move_to([-3.6, 3.0, 0])
        rows = [("nucleus", "yes", BLUE, YELLOW), ("cell wall", "yes", GOLD, YELLOW),
                ("chloroplasts", "no", GREEN, RED), ("food", "takes it in", TEXT, YELLOW)]
        R = []
        for i, (a, b, ca, cb) in enumerate(rows):
            y = 2.3 - i * 1.15
            ta = T(a, 32, ca).move_to([1.6, y, 0]); ta.align_to([0.5, 0, 0], LEFT)
            tb = T(b, 32, cb, weight=BOLD).move_to([5.6, y, 0]); tb.align_to([4.0, 0, 0], LEFT)
            R.append((ta, tb))
        self.add(title, mc.mem)
        self.at("cells have a nucleus")
        self.play(GrowFromCenter(mc.nuc), FadeIn(R[0][0]), FadeIn(R[0][1]), run_time=0.6)
        self.at("a cell wall")
        self.play(Create(mc.wall), FadeIn(R[1][0]), FadeIn(R[1][1]), run_time=0.7)
        self.at("no chloroplasts")
        self.play(FadeIn(R[2][0]), FadeIn(R[2][1]), run_time=0.6)
        self.at("cannot make sugar")
        self.play(Indicate(R[2][1], color=RED, scale_factor=1.2), run_time=0.8)
        self.at("takes in food")
        self.play(FadeIn(R[3][0]), FadeIn(R[3][1]), run_time=0.6)

        fchip = chip("fungi: their own kingdom", ORANGE, size=32).move_to([-3.0, -2.9, 0])
        pchip = chip("plants", GREEN, size=32).move_to([3.2, -2.9, 0])
        self.at("in their own kingdom")
        self.play(FadeIn(fchip, shift=UP * 0.15), run_time=0.6)
        self.at("not with plants")
        self.play(FadeIn(pchip), run_time=0.3)
        self.play(Create(cross_over(pchip)), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
SEQ = [0, 1, 2, 3, 0, 1, 3, 2, 1, 0, 2, 3, 1, 2]
BW, BG_ = 0.55, 0.06
X0 = -5.85 + BW / 2


def seq_row(seq, y):
    g = VGroup()
    for i, v in enumerate(seq):
        b = Rectangle(width=BW, height=0.5, stroke_color=BLUE, stroke_width=2.5,
                      fill_color=BLUE, fill_opacity=[0.12, 0.35, 0.6, 0.9][v])
        b.move_to([X0 + i * (BW + BG_), y, 0])
        g.add(b)
    return g


def other(seq, diffs):
    return [((v + 1) % 4 if i in diffs else v) for i, v in enumerate(seq)]


def links(r1, r2, diffs):
    g = VGroup()
    for i in range(len(r1)):
        if i not in diffs:
            g.add(Line(r1[i].get_bottom(), r2[i].get_top(), color=YELLOW, stroke_width=4))
    return g


class S05Dna(SpokenScene):
    def construct(self):
        d1 = {4, 9}
        d2 = {1, 3, 4, 6, 8, 10, 12}
        rowA = seq_row(SEQ, 2.0)
        lab = T("DNA sequence", 32, BLUE).move_to([4.5, 2.0, 0])
        self.at("Then came DNA")
        self.play(FadeIn(lab), run_time=0.4)
        self.at("sequence is the")
        self.play(FadeIn(rowA, lag_ratio=0.12), run_time=1.8)

        rowB = seq_row(other(SEQ, d1), 1.0)
        L1 = links(rowA, rowB, d1)
        rowC = seq_row(SEQ, -0.6)
        rowD = seq_row(other(SEQ, d2), -1.6)
        L2 = links(rowC, rowD, d2)
        more = T("more alike", 32, YELLOW).move_to([4.5, 1.5, 0])
        less = T("less alike", 32, GREY).move_to([4.5, -1.1, 0])
        note = T("a sketch, not real data", 24, GREY).move_to([0, -3.1, 0])
        self.at("the more alike")
        self.play(FadeIn(rowB), run_time=0.4)
        self.play(Create(L1), ReplacementTransform(lab, more), run_time=0.8)
        self.play(FadeIn(rowC), FadeIn(rowD), run_time=0.4)
        self.play(Create(L2), FadeIn(less), FadeIn(note), run_time=0.8)

        more2 = T("more closely\nrelated", 28, YELLOW).move_to([4.5, 1.5, 0])
        less2 = T("less closely\nrelated", 28, GREY).move_to([4.5, -1.1, 0])
        self.at("more closely related")
        self.play(ReplacementTransform(more, more2), ReplacementTransform(less, less2), run_time=0.7)

        node = Dot([0, -1.2, 0], radius=0.14, color=GOLD)
        g1 = chip("group", TEXT, size=30).move_to([-3.0, 1.6, 0])
        g2 = chip("group", TEXT, size=30).move_to([3.0, 1.6, 0])
        e1 = arr([0, -1.1, 0], g1.get_bottom() + DOWN * 0.1, GOLD)
        e2 = arr([0, -1.1, 0], g2.get_bottom() + DOWN * 0.1, GOLD)
        nl = T("common ancestor", 32, GOLD).move_to([0, -1.9, 0])
        self.at("A common ancestor")
        allrows = VGroup(rowA, rowB, rowC, rowD, L1, L2, more2, less2, note)
        self.play(FadeOut(allrows), run_time=0.4)
        self.play(FadeIn(node), FadeIn(nl), run_time=0.4)
        self.at("both descend from")
        self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(g1), FadeIn(g2), run_time=0.8)

        an = chip("animals", PURPLE, size=42).move_to([-4.6, 0.2, 0])
        fu = chip("fungi", ORANGE, size=42).move_to([-0.6, 0.2, 0])
        pl = chip("plants", GREEN, size=42).move_to([4.5, 0.2, 0])
        near = DoubleArrow(an.get_right() + RIGHT * 0.08, fu.get_left() + LEFT * 0.08, color=YELLOW, buff=0, stroke_width=5, tip_length=0.18)
        far = DoubleArrow(fu.get_right() + RIGHT * 0.08, pl.get_left() + LEFT * 0.08, color=GREY, buff=0, stroke_width=5, tip_length=0.18)
        t1 = T("closer", 30, YELLOW).next_to(near, UP, buff=0.2)
        t2 = T("farther", 30, GREY).next_to(far, UP, buff=0.2)
        self.at("put fungi closer")
        self.play(FadeOut(VGroup(node, nl, e1, e2, g1, g2)), run_time=0.4)
        self.play(FadeIn(an), FadeIn(fu), FadeIn(pl), run_time=0.6)
        self.play(GrowFromCenter(near), FadeIn(t1), run_time=0.5)
        self.play(GrowFromCenter(far), FadeIn(t2), run_time=0.5)
        self.play(FadeIn(T("a sketch: only the order is shown", 24, GREY).move_to([0, -2.4, 0])), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        an = chip("animals", PURPLE, size=42).move_to([-4.6, 0.2, 0])
        fu = chip("fungi", ORANGE, size=42).move_to([-0.6, 0.2, 0])
        pl = chip("plants", GREEN, size=42).move_to([4.5, 0.2, 0])
        self.add(an, fu, pl)
        eq = VGroup(T("=", 64, RED, weight=BOLD), Line([-0.35, -0.45, 0], [0.35, 0.45, 0], color=RED, stroke_width=7))
        eq.move_to([-2.45, 0.2, 0])
        self.at("does not make")
        self.play(FadeIn(eq, scale=0.8), run_time=0.5)

        tips_y = 2.2
        n1 = np.array([-2.9, 0.6, 0]); n2 = np.array([0.8, -1.2, 0])
        self.at("share a more recent")
        self.play(FadeOut(eq), an.animate.move_to([-4.4, tips_y, 0]), fu.animate.move_to([-1.4, tips_y, 0]),
                  pl.animate.move_to([4.4, tips_y, 0]), run_time=0.8)
        la = Line([-4.4, tips_y - 0.5, 0], n1, color=PURPLE, stroke_width=5)
        lf = Line([-1.4, tips_y - 0.5, 0], n1, color=ORANGE, stroke_width=5)
        d1 = Dot(n1, radius=0.14, color=GOLD)
        t1 = T("more recent\ncommon ancestor", 26, GOLD).move_to([-4.8, 0.2, 0])
        self.at("recent common ancestor")
        self.play(Create(la), Create(lf), run_time=0.7)
        self.play(FadeIn(d1), FadeIn(t1), run_time=0.4)
        lp = VGroup(Line([4.4, tips_y - 0.5, 0], [4.4, n2[1], 0], color=GREEN, stroke_width=5),
                    Line([4.4, n2[1], 0], n2, color=GREEN, stroke_width=5))
        l12 = Line(n1, n2, color=GOLD, stroke_width=5)
        d2 = Dot(n2, radius=0.14, color=GOLD)
        t2 = T("ancestor shared\nwith plants", 26, GOLD).move_to([0.8, -2.3, 0])
        self.at("either shares with plants")
        self.play(Create(l12), Create(lp), run_time=0.8)
        self.play(FadeIn(d2), FadeIn(t2), run_time=0.4)

        # new tools
        mic = chip("microscopes", PINK, size=30).move_to([-3.2, 2.7, 0])
        dna = chip("DNA comparisons", PINK, size=30).move_to([3.2, 2.7, 0])
        ar = arr([-1.3, 2.7, 0], [1.1, 2.7, 0], PINK)
        newt = T("new evidence", 26, PINK).move_to([0, 3.25, 0])
        self.at("New tools give")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)
        self.play(FadeIn(newt), run_time=0.3)
        self.at("from microscopes")
        self.play(FadeIn(mic), run_time=0.4)
        self.at("DNA comparisons")
        self.play(GrowArrow(ar), FadeIn(dna), run_time=0.6)

        pbox = box(5.4, 3.2, GREEN, -3.2, -0.6, op=0.08)
        pbl = T("plants", 30, GREEN).move_to([-3.2, 0.7, 0])
        fbox = box(5.4, 3.2, ORANGE, 3.2, -0.6, op=0.08)
        fbl = T("fungi", 30, ORANGE).move_to([3.2, 0.7, 0])
        mu = chip("mushroom", ORANGE, size=32).move_to([-3.2, -0.9, 0])
        self.at("can change how")
        self.play(FadeIn(pbox), FadeIn(pbl), FadeIn(fbox), FadeIn(fbl), run_time=0.6)
        self.play(FadeIn(mu), run_time=0.4)
        self.at("So DNA can move")
        cap = T("cell clues, then DNA comparisons", 26, PINK).move_to([0, -2.9, 0])
        self.play(mu.animate.move_to([3.2, -0.9, 0]), FadeIn(cap), run_time=1.4)
        self.finish()


class S07End(EndCard):
    LINE = "DNA evidence can move a living thing to a new group."
