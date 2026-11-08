"""Molecular evolution: genes date a split without fossils  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the lineages (tree branches, tips, species names)
  YELLOW = sequence differences and substitutions (ticks, differing sites, the observed share)
  TEAL   = the clock: distance D, rate r, and the arithmetic that uses them
  GOLD   = the fossil calibration (diamond, "3.0 million years", minimum age)
  GREEN  = the dated answer (6.0 million years)
  RED    = the wrong answer (forgetting the factor of two)
  GREY   = axes, outlines, de-emphasised labels
"""
import math
import numpy as np
from bp_style import *  # noqa: F401,F403


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def tree(nx, tx, cy, dy, n=0, color=BLUE, w=6, tick_len=0.2):
    """Rectangular tree: root node at nx, two level tips at tx. n substitution ticks per branch."""
    v = Line([nx, cy - dy, 0], [nx, cy + dy, 0], color=color, stroke_width=w)
    top = Line([nx, cy + dy, 0], [tx, cy + dy, 0], color=color, stroke_width=w)
    bot = Line([nx, cy - dy, 0], [tx, cy - dy, 0], color=color, stroke_width=w)
    ta = Dot([tx, cy + dy, 0], radius=0.13, color=color)
    tb = Dot([tx, cy - dy, 0], radius=0.13, color=color)
    node = Dot([nx, cy, 0], radius=0.14, color=TEXT)
    tt, tb_ = [], []
    for i in range(n):
        x = nx + (tx - nx) * (i + 0.5) / n
        tt.append(Line([x, cy + dy - tick_len, 0], [x, cy + dy + tick_len, 0], color=YELLOW, stroke_width=5))
        x2 = nx + (tx - nx) * (i + 0.28) / n
        tb_.append(Line([x2, cy - dy - tick_len, 0], [x2, cy - dy + tick_len, 0], color=YELLOW, stroke_width=5))
    g = VGroup(v, top, bot, ta, tb, node, *tt, *tb_)
    g.v, g.top, g.bot, g.ta, g.tb, g.node = v, top, bot, ta, tb, node
    g.tt, g.tb_ = tt, tb_
    g.nx, g.tx, g.cy, g.dy = nx, tx, cy, dy
    return g


def bare(g):
    """the tree without its ticks, as a VGroup of the six body parts."""
    return VGroup(g.v, g.top, g.bot, g.ta, g.tb, g.node)


def strip(x0, y, diff, n=12, side=0.34, gap=0.06):
    sq = VGroup()
    for i in range(n):
        s = Square(side, stroke_color=GREY, stroke_width=2.5, fill_color=GREY, fill_opacity=0.12)
        s.move_to([x0 + side / 2 + i * (side + gap), y, 0])
        sq.add(s)
    sq.diff = [sq[i] for i in diff]
    return sq


def diamond(pos, r=0.2):
    d = RegularPolygon(4, radius=r, color=GOLD, fill_color=GOLD, fill_opacity=1, stroke_width=3)
    d.move_to(pos)
    return d


def mrow(parts, size=24):
    """a mono text line."""
    return M(parts, size=size)


def panel_line(txt, color=TEAL, size=24, font=None):
    return (M(txt, size=size, color=color) if font is None else T(txt, size=size, color=color))


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Molecular evolution"
    TITLE = "Genes date a split without fossils"


# ---------------------------------------------------------------------------------------------
class S01Record(SpokenScene):
    """two tips, a split with a question, no fossil; two gene strips with differing sites."""

    def construct(self):
        dy = 2.0
        t = tree(-4.0, -0.6, 0, dy)
        lab_a = T("species A", 28, BLUE).move_to([3.2, dy + 0.5, 0])
        lab_b = T("species B", 28, BLUE).move_to([3.2, -dy + 0.5, 0])
        join_a = Line([-0.45, dy, 0], [0.15, dy, 0], color=GREY, stroke_width=3)
        join_b = Line([-0.45, -dy, 0], [0.15, -dy, 0], color=GREY, stroke_width=3)
        sa = strip(0.2, dy, [1, 4, 5, 9], side=0.42, gap=0.06)
        sb = strip(0.2, -dy, [1, 4, 5, 9], side=0.42, gap=0.06)
        self.play(FadeIn(t.node), Create(t.v), run_time=0.3)
        self.play(Create(t.top), Create(t.bot), FadeIn(t.ta), FadeIn(t.tb), run_time=0.5)
        self.play(FadeIn(lab_a), FadeIn(lab_b), run_time=0.3)

        fossil = chip("fossil?", GOLD, 28)
        fossil.move_to([-5.2, -1.3, 0])
        self.at("left no fossil")
        self.play(FadeIn(fossil, shift=UP * 0.1), run_time=0.5)

        when = chip("when?", WHITE, 30).move_to([-5.2, 1.0, 0])
        warrow = Arrow(when.get_right(), t.node.get_center() + LEFT * 0.12, buff=0.06, color=GREY, stroke_width=4,
                       tip_length=0.2)
        self.at("moment they split")
        self.play(FadeIn(when, shift=RIGHT * 0.1), GrowArrow(warrow), run_time=0.6)

        self.at("Line up the same gene")
        self.play(FadeIn(join_a), FadeIn(join_b), FadeIn(sa, lag_ratio=0.05), FadeIn(sb, lag_ratio=0.05), run_time=1.2)

        self.at("They differ")
        self.play(*[s.animate.set_fill(YELLOW, 0.85).set_stroke(YELLOW) for s in sa.diff + sb.diff], run_time=0.6)
        self.play(*[Indicate(s, color=YELLOW, scale_factor=1.25) for s in sa.diff + sb.diff], run_time=0.8)

        self.at("a record")
        self.play(Indicate(VGroup(*sa.diff, *sb.diff), color=YELLOW, scale_factor=1.12), run_time=0.8)
        self.at("read as time")
        self.play(when[0].animate.set_stroke(TEAL).set_fill(TEAL, 0.16), when[1].animate.set_color(TEAL),
                  warrow.animate.set_color(TEAL), run_time=0.6)
        self.play(Indicate(when, color=TEAL, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Both(SpokenScene):
    """ticks pile up along both branches; D = rt + rt = 2rt."""

    def construct(self):
        nx, tx, cy, dy = -3.2, 3.8, 0.5, 1.75
        t = tree(nx, tx, cy, dy, n=5)
        lab_a = T("species A", 26, BLUE).move_to([tx + 1.3, cy + dy, 0])
        lab_b = T("species B", 26, BLUE).move_to([tx + 1.3, cy - dy, 0])
        anc = T("common\nancestor", 24, GREY, line_spacing=0.9).next_to(t.node, LEFT, buff=0.3)
        self.play(FadeIn(t.node), Create(t.v), run_time=0.5)
        self.play(Create(t.top), Create(t.bot), FadeIn(t.ta), FadeIn(t.tb), FadeIn(lab_a), FadeIn(lab_b), run_time=1.0)

        self.at("each keeps gaining")
        for i in range(5):
            self.play(GrowFromCenter(t.tt[i]), GrowFromCenter(t.tb_[i]), run_time=0.28)
        self.at("Some spread")
        self.play(Indicate(t.tt[2], color=YELLOW, scale_factor=1.6), run_time=0.7)

        sub = chip("substitution", YELLOW, 26)
        sub.move_to([t.tt[2].get_center()[0], cy + dy - 1.0, 0])
        sub_ln = Line(sub.get_top(), t.tt[2].get_bottom(), color=YELLOW, stroke_width=3)
        self.at("is a substitution")
        self.play(FadeIn(sub, shift=UP * 0.1), Create(sub_ln), run_time=0.5)

        self.at("along both branches")
        self.play(FadeOut(sub), FadeOut(sub_ln), run_time=0.3)
        bt = Brace(Line(t.top.get_start(), t.top.get_end()), UP, color=TEAL).shift(UP * 0.28)
        bb = Brace(Line(t.bot.get_start(), t.bot.get_end()), DOWN, color=TEAL).shift(DOWN * 0.28)
        lt = M("r t", 30, TEAL).next_to(bt, UP, buff=0.12)
        lb = M("r t", 30, TEAL).next_to(bb, DOWN, buff=0.12)
        self.play(GrowFromCenter(bt), GrowFromCenter(bb), run_time=0.6)
        self.play(FadeIn(lt), FadeIn(lb), run_time=0.4)
        self.at("common ancestor")
        self.play(FadeIn(anc), Indicate(t.node, color=WHITE, scale_factor=2.0), run_time=0.6)

        self.at("the distance between the two tips")
        dline = DoubleArrow([tx + 0.55, cy - dy, 0], [tx + 0.55, cy + dy, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.2)
        dl = M("D", 30, TEAL).next_to(dline, RIGHT, buff=0.15)
        self.play(FadeOut(lab_a), FadeOut(lab_b), GrowFromCenter(dline), FadeIn(dl), run_time=0.7)

        self.at("Write it as")
        f = M("D = r t + r t = 2 r t", 38, TEAL).move_to([0.3, -3.05, 0])
        self.play(Write(f), run_time=1.4)
        self.play(Indicate(f, color=TEAL, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Unseen(SpokenScene):
    """a site changes and changes back; observed 0.30 against corrected 0.383."""

    def construct(self):
        P = 0.30
        D = -0.75 * math.log(1 - (4 / 3) * P)
        assert abs(D - 0.383) < 0.0005, D

        sq = Square(2.0, stroke_color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.12).move_to([0, 0.6, 0])
        site = T("one site", 32, GREY).next_to(sq, UP, buff=0.35)
        self.at("There is a catch")
        self.play(FadeIn(sq), FadeIn(site), run_time=0.6)

        self.at("change twice")
        c1 = T("changes", 34, YELLOW).next_to(sq, DOWN, buff=0.5)
        self.play(sq.animate.set_stroke(YELLOW).set_fill(YELLOW, 0.8), FadeIn(c1), run_time=0.5)
        self.at("change and change back")
        c2 = T("changes back", 34, YELLOW).move_to(c1)
        self.play(sq.animate.set_stroke(GREY).set_fill(GREY, 0.12), ReplacementTransform(c1, c2), run_time=0.6)
        self.at("fewer differences")
        c3 = T("two changes happened, none seen", 34, YELLOW).move_to(c2)
        self.play(ReplacementTransform(c2, c3), run_time=0.5)

        # chart
        x0, sc = -2.8, 16.0
        yo, yd = 0.6, -1.0
        bh = 1.1
        bar_o = Rectangle(width=P * sc, height=bh, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.8)
        bar_o.move_to([x0 + P * sc / 2, yo, 0])
        base = Rectangle(width=P * sc, height=bh, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.8)
        base.move_to([x0 + P * sc / 2, yd, 0])
        ext = Rectangle(width=(D - P) * sc, height=bh, stroke_color=YELLOW, stroke_width=3, fill_opacity=0)
        ext.move_to([x0 + P * sc + (D - P) * sc / 2, yd, 0])
        lab_o = T("p: proportion of\nsites that differ", 26, YELLOW, line_spacing=0.9).move_to([x0 - 1.55, yo, 0])
        lab_d = T("d: substitutions\nper site", 26, YELLOW, line_spacing=0.9).move_to([x0 - 1.55, yd, 0])
        val_o = M("0.30", 32, YELLOW).next_to(bar_o, RIGHT, buff=0.25)
        val_d = M("0.383", 32, YELLOW).next_to(ext, RIGHT, buff=0.25)
        axis = Line([x0, yd - 0.75, 0], [x0, yo + 0.75, 0], color=GREY, stroke_width=3)

        self.at("undercounts the change")
        self.play(FadeOut(sq), FadeOut(site), FadeOut(c3), run_time=0.4)
        self.play(FadeIn(axis), FadeIn(lab_o), run_time=0.4)
        self.at("of sites differ")
        self.play(GrowFromEdge(bar_o, LEFT), FadeIn(val_o), run_time=0.8)

        form = M("d = -(3/4) × ln(1 - (4/3) × p)", 30, TEAL).move_to([0, 2.5, 0])
        self.at("The corrected distance")
        self.play(FadeIn(form, shift=DOWN * 0.1), FadeIn(lab_d), run_time=0.5)
        self.play(GrowFromEdge(base, LEFT), run_time=0.4)
        self.play(Create(ext), FadeIn(val_d), run_time=0.8)

        self.at("more than a quarter")
        br = Brace(ext, DOWN, color=YELLOW)
        bl = T("change you cannot see", 28, YELLOW).next_to(br, DOWN, buff=0.12)
        self.play(GrowFromCenter(br), FadeIn(bl), ext.animate.set_fill(YELLOW, 0.3), run_time=0.7)
        self.play(Indicate(ext, color=YELLOW, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Rate(SpokenScene):
    """same distance, fast-short or slow-long; then a fossil gives the rate."""

    def construct(self):
        head = M("same distance: 0.02", 36, TEAL).move_to([0, 2.95, 0])
        L = tree(-6.0, -3.5, 0.5, 1.5, n=5)
        R = tree(-1.2, 5.9, 0.5, 1.5, n=5)
        ll = T("fast rate\nshort time", 30, GREY, line_spacing=0.9).move_to([-4.75, -1.95, 0])
        lr = T("slow rate\nlong time", 30, GREY, line_spacing=0.9).move_to([2.35, -1.95, 0])
        self.at("cannot separate rate from time")
        self.play(FadeIn(head), run_time=0.5)
        self.play(FadeIn(L, lag_ratio=0.03), run_time=1.0)
        self.at("fast rate")
        self.play(FadeIn(ll), Indicate(L, color=YELLOW, scale_factor=1.04), run_time=0.6)
        self.at("slow rate")
        self.play(FadeIn(R, lag_ratio=0.03), run_time=1.2)
        self.play(FadeIn(lr), run_time=0.4)

        # pair 1, dated by a fossil
        nx, tx, cy, dy = -5.5, -1.0, 0.5, 1.75
        P1 = tree(nx, tx, cy, dy, n=5)
        self.at("from outside the sequences")
        self.play(FadeOut(VGroup(head, L, R, ll, lr)), run_time=0.5)
        self.play(FadeIn(P1.node), Create(P1.v), run_time=0.3)
        self.play(Create(P1.top), Create(P1.bot), FadeIn(P1.ta), FadeIn(P1.tb), run_time=0.7)
        self.play(*[GrowFromCenter(x) for x in P1.tt + P1.tb_], run_time=0.5)

        dm = diamond(P1.node.get_center(), 0.28)
        self.at("The commonest is a fossil")
        self.play(FadeIn(dm, scale=1.6), run_time=0.5)
        self.play(Indicate(dm, color=GOLD, scale_factor=1.5), run_time=0.6)

        age = T("split 3.0 million years ago", 30, GOLD).move_to([(nx + tx) / 2 + 0.3, cy - dy - 0.95, 0])
        self.at("known from fossils")
        self.play(FadeIn(age, shift=UP * 0.1), run_time=0.6)

        dline = DoubleArrow([tx + 0.5, cy - dy, 0], [tx + 0.5, cy + dy, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.2)
        dval = M("0.012", 30, TEAL).next_to(dline, RIGHT, buff=0.15)
        self.at("Their corrected distance")
        self.play(GrowFromCenter(dline), FadeIn(dval), run_time=0.6)

        l0 = T("rate per lineage", 26, GREY)
        l1 = T("r = 0.012 / (2 × 3,000,000)", 26, TEAL)
        l2 = T("= 2.0 × 10⁻⁹", 52, TEAL)
        l3 = T("substitutions per site per year", 24, TEAL)
        pan = VGroup(l0, l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        pan.move_to([4.0, 0.4, 0])
        pan.shift(RIGHT * (1.75 - pan.get_left()[0]))
        print("S04 panel width", pan.width, "left", pan.get_left()[0], "right", pan.get_right()[0])
        self.at("Divide by twice")
        self.play(FadeIn(l0), FadeIn(l1, shift=LEFT * 0.1), run_time=0.7)
        self.at("and the rate is")
        self.play(FadeIn(l2, shift=LEFT * 0.1), run_time=0.6)
        self.play(FadeIn(l3), run_time=0.4)
        self.play(Indicate(l2, color=TEAL, scale_factor=1.08), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
TIPX, K = 0.3, 0.75      # tip x, units per million years
Y1, Y2, YAX = -0.65, 1.55, -2.45
DYP = 0.8


def two_pairs(second_node_x, n2, y1=Y1, y2=Y2, dy=DYP):
    n1x = TIPX - 3.0 * K
    P1 = tree(n1x, TIPX, y1, dy, n=4)
    P2 = tree(second_node_x, TIPX, y2, dy, n=n2)
    return P1, P2


def axis_marks():
    ax = Line([TIPX, YAX, 0], [TIPX - 6.6 * K, YAX, 0], color=GREY, stroke_width=3)
    marks = VGroup()
    for v, lab in [(0, "0"), (3, "3.0"), (6, "6.0")]:
        x = TIPX - v * K
        marks.add(Line([x, YAX - 0.1, 0], [x, YAX + 0.1, 0], color=GREY, stroke_width=3))
        marks.add(M(lab, 24, GREY).move_to([x, YAX - 0.4, 0]))
    cap = T("million years ago", 24, GREY).move_to([TIPX - 3.0 * K, YAX - 0.9, 0])
    return VGroup(ax, marks, cap)


def tip_labels():
    """a column to the right of the tips: pair name over distance."""
    out = VGroup()
    for y, name, dist in [(Y1, "pair 1", "0.012"), (Y2, "pair 2", "0.024")]:
        a = T(name, 24, GREY).move_to([TIPX + 1.0, y + 0.3, 0])
        d = M(dist, 26, TEAL).move_to([TIPX + 1.0, y - 0.25, 0])
        out.add(a, d)
    return out


class S05Second(SpokenScene):
    """second pair on the same time axis: dense branches stretch until the node lands at six."""

    def construct(self):
        P1, P2s = two_pairs(TIPX - 3.0 * K, 8)
        _, P2 = two_pairs(TIPX - 6.0 * K, 8)
        ax = axis_marks()
        dm1 = diamond(P1.node.get_center(), 0.22)
        tl = tip_labels()
        PX = 4.3
        q = T("?", 44, WHITE, weight=BOLD)

        self.add(P1, dm1, ax, tl[0], tl[1])
        self.at("take a second pair")
        self.play(FadeIn(P2s.node), Create(P2s.v), run_time=0.3)
        self.play(Create(P2s.top), Create(P2s.bot), FadeIn(P2s.ta), FadeIn(P2s.tb), run_time=0.5)
        self.play(*[GrowFromCenter(x) for x in P2s.tt + P2s.tb_], run_time=0.4)
        q.next_to(P2s.node, LEFT, buff=0.2)
        self.play(FadeIn(q), FadeIn(tl[2]), run_time=0.3)

        self.at("Their corrected distance")
        self.play(FadeIn(tl[3], shift=LEFT * 0.1), run_time=0.5)

        PL = 2.3
        r_line = T("r = 2.0 × 10⁻⁹", 30, TEAL).move_to([PX, 2.65, 0]).align_to([PL, 0, 0], LEFT)
        l2 = T("t = 0.024 / (4.0 × 10⁻⁹)", 28, TEAL).move_to([PX, 1.8, 0]).align_to([PL, 0, 0], LEFT)
        l3 = T("= 6.0 million years", 32, GREEN, weight=BOLD).move_to([PX, 0.95, 0]).align_to([PL, 0, 0], LEFT)
        for m in (r_line, l2, l3):
            print("S05 width", m.width, m.get_left()[0], m.get_right()[0])
        self.at("Divide by twice the rate")
        self.play(FadeIn(r_line), run_time=0.4)
        self.play(FadeIn(l2, shift=LEFT * 0.1), run_time=0.6)

        self.at("The answer is")
        drop = DashedLine([TIPX - 6.0 * K, Y2 - 0.1, 0], [TIPX - 6.0 * K, YAX, 0], color=GREEN, stroke_width=3)
        self.play(ReplacementTransform(P2s, P2), q.animate.next_to(P2.node, LEFT, buff=0.2), run_time=1.5)
        self.play(FadeOut(q), Create(drop), FadeIn(l3, shift=LEFT * 0.1),
                  P2.node.animate.set_color(GREEN).scale(1.5), run_time=0.8)

        self.at("Check it")
        chk1 = T("check:", 26, GREY)
        chk2 = T("2 × 2.0 × 10⁻⁹ × 6,000,000", 24, TEAL)
        chk3 = T("= 0.024", 32, TEAL)
        chk = VGroup(chk1, chk2, chk3).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        chk.move_to([PX, -0.35, 0]).align_to([PL, 0, 0], LEFT)
        print("S05 chk width", chk.width, chk.get_left()[0], chk.get_right()[0])
        self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(chk3, color=TEAL, scale_factor=1.12), Indicate(tl[3], color=TEAL, scale_factor=1.2), run_time=0.8)

        self.at("common error")
        wr1 = T("forget the 2", 30, RED)
        wr2 = T("12 million years", 32, RED, weight=BOLD)
        wr = VGroup(wr1, wr2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([PX, -1.95, 0]).align_to([PL, 0, 0], LEFT)
        self.play(FadeIn(wr, shift=UP * 0.1), run_time=0.6)
        self.at("which is wrong")
        strike = Line(wr2.get_left() + LEFT * 0.1, wr2.get_right() + RIGHT * 0.1, color=RED, stroke_width=6)
        self.play(Create(strike), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Minimum(SpokenScene):
    """the fossil is a minimum: both dates may be older; the assumptions; the rule."""

    def construct(self):
        P1, P2 = two_pairs(TIPX - 6.0 * K, 8)
        ax = axis_marks()
        dm1 = diamond(P1.node.get_center(), 0.22)
        P2.node.set_color(GREEN)
        P2.node.scale(1.5)
        tl = tip_labels()
        self.add(P1, P2, ax, dm1, tl)

        self.at("One caution remains")
        self.play(Indicate(dm1, color=GOLD, scale_factor=1.6), run_time=0.7)
        self.at("The oldest fossil")
        self.play(Indicate(dm1, color=GOLD, scale_factor=1.8), run_time=0.7)

        n1 = P1.node.get_center()
        n2 = P2.node.get_center()
        ar1 = Arrow(n1 + LEFT * 0.3, n1 + LEFT * 1.8, buff=0, color=GOLD, stroke_width=6, tip_length=0.25)
        or1 = T("or earlier", 26, GOLD).next_to(ar1, UP, buff=0.12).shift(LEFT * 0.2)
        self.at("So it gives")
        mn = T("minimum age", 30, GOLD).move_to([n1[0] - 1.95, Y1 - 0.55, 0])
        self.play(FadeIn(mn, shift=UP * 0.1), run_time=0.5)
        self.at("by an unknown margin")
        self.play(GrowArrow(ar1), FadeIn(or1), run_time=0.8)

        ar2 = Arrow(n2 + LEFT * 0.3, n2 + LEFT * 1.4, buff=0, color=GOLD, stroke_width=6, tip_length=0.25)
        or2 = T("or earlier", 26, GOLD).next_to(ar2, UP, buff=0.12).shift(LEFT * 0.35)
        self.at("Both dates may be older")
        self.play(GrowArrow(ar2), FadeIn(or2), run_time=0.8)

        a1 = chip("equal, constant rates", TEAL, 26)
        a2 = chip("exact calibration", GOLD, 26)
        ag = VGroup(a1, a2).arrange(DOWN, buff=0.4).move_to([4.3, 0.9, 0])
        print("S06 chips", a1.width, a1.get_left()[0], a1.get_right()[0])
        self.at("equal, constant rates")
        self.play(FadeIn(a1, shift=LEFT * 0.1), run_time=0.5)
        self.at("exact calibration")
        self.play(FadeIn(a2, shift=LEFT * 0.1), run_time=0.5)
        sens = T("a date stays sensitive\nto its assumptions", 28, GREY, line_spacing=0.9).move_to([4.3, -1.0, 0])
        self.at("sensitive to its assumptions")
        self.play(FadeIn(sens, shift=UP * 0.1), Indicate(ag, color=TEAL, scale_factor=1.05), run_time=0.8)

        r1 = T("A clock needs a calibration", 44, font=TITLE_FONT)
        r2 = T("A fossil gives only a minimum age", 44, font=TITLE_FONT, color=GOLD)
        rg = VGroup(r1, r2).arrange(DOWN, buff=0.5)
        fit(rg, max_w=11.8)
        self.at("keep this rule")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.6)
        self.at("a fossil gives only")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "A clock needs a calibration; a fossil gives only a minimum age."
