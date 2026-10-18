"""Same four species, different diversity (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE / YELLOW / GREEN / ORANGE = the four species (circle, square, triangle, diamond)
  RED    = Simpson concentration lambda
  TEAL   = effective numbers of species (blocks of equally common species)
  GOLD   = the open question and the take-home rule
  GREY   = frames, outlines, labels
  TEXT   = counts, richness S, evenness
"""
import random
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
SP = [BLUE, YELLOW, GREEN, ORANGE]
CA = [25, 25, 25, 25]
CB = [40, 40, 10, 10]
SHARE_A = ["0.25"] * 4
SHARE_B = ["0.4", "0.4", "0.1", "0.1"]
LX, RX = -3.75, 3.75  # panel centres


def mark(k, r=0.13, color=None):
    c = color or SP[k]
    kw = dict(stroke_width=0, fill_color=c, fill_opacity=0.92)
    if k == 0:
        return Circle(radius=r, **kw)
    if k == 1:
        return Square(side_length=r * 1.75, **kw)
    if k == 2:
        return Triangle(**kw).scale(r * 1.3)
    return Square(side_length=r * 1.55, **kw).rotate(PI / 4)


def alien(k, r=0.15):
    kw = dict(stroke_width=0, fill_color=GREY, fill_opacity=0.9)
    if k == 0:
        return RegularPolygon(5, **kw).scale(r * 1.2)
    if k == 1:
        return RegularPolygon(6, **kw).scale(r * 1.2)
    if k == 2:
        return Star(5, outer_radius=r * 1.4, inner_radius=r * 0.6, **kw)
    return Square(side_length=r * 1.5, **kw).rotate(PI / 4)


def make_plot(counts, seed, d=0.4):
    sp = [k for k, c in enumerate(counts) for _ in range(c)]
    random.Random(seed).shuffle(sp)
    dots = VGroup()
    groups = [VGroup() for _ in counts]
    for i, k in enumerate(sp):
        r_, c_ = divmod(i, 10)
        m = mark(k, 0.13).move_to([(c_ - 4.5) * d, (4.5 - r_) * d, 0])
        dots.add(m)
        groups[k].add(m)
    frame = RoundedRectangle(corner_radius=0.15, width=10 * d + 0.4, height=10 * d + 0.4,
                             stroke_color=GREY, stroke_width=3, fill_opacity=0)
    g = VGroup(frame, dots)
    g.frame, g.dots, g.groups = frame, dots, groups
    return g


def count_row(counts, cx, y, size=26):
    items = []
    for k, c in enumerate(counts):
        items.append(VGroup(mark(k, 0.13), M(str(c), size, TEXT)).arrange(RIGHT, buff=0.14))
    row = VGroup(*items).arrange(RIGHT, buff=0.38).move_to([cx, y, 0])
    return row


def bar_set(counts, labels, cx, base_y, unit=0.05, sp=1.1, w=0.62, mk=mark):
    bars, marks, labs = VGroup(), VGroup(), VGroup()
    for k, c in enumerate(counts):
        x = cx + (k - 1.5) * sp
        h = unit * c
        rect = Rectangle(width=w, height=h, stroke_width=0, fill_color=SP[k] if mk is mark else GREY,
                         fill_opacity=0.85).move_to([x, base_y + h / 2, 0])
        lab = M(labels[k], 24, TEXT).next_to(rect, UP, buff=0.1)
        m = mk(k, 0.15).move_to([x, base_y - 0.38, 0])
        bars.add(rect); labs.add(lab); marks.add(m)
    line = Line([cx - 2.15, base_y, 0], [cx + 2.15, base_y, 0], color=GREY, stroke_width=3)
    return bars, labs, marks, line


def mini_plot(counts, seed, cx):
    p = make_plot(counts, seed).scale(0.38).move_to([cx - 1.05, 2.5, 0])
    return p


def plot_label(txt, cx, y=2.5, size=34):
    return T(txt, size, TEXT, weight=BOLD).move_to([cx + 0.95, y, 0])


def blocks(value, x0, y, w=0.66, h=0.85, gap=0.08):
    g = VGroup()
    n = int(value + 1e-9)
    frac = value - n
    for i in range(n):
        g.add(Rectangle(width=w, height=h, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL,
                        fill_opacity=0.5).move_to([x0 + w / 2 + i * (w + gap), y, 0]))
    if frac > 0.02:
        pw = w * frac
        g.add(Rectangle(width=pw, height=h, stroke_color=TEAL, stroke_width=2.5, fill_color=TEAL,
                        fill_opacity=0.5).move_to([x0 + n * (w + gap) + pw / 2, y, 0]))
    return g


ROWS_Y = [0.85, -0.45, -1.75]
BX = {"A": -5.9, "B": 1.5}


def row_value(v, side, y, txt):
    x = BX[side] + 4 * 0.66 + 3 * 0.08 + 0.25
    return M(txt, 32, TEAL).move_to([x, y, 0], aligned_edge=LEFT)


def order_labels():
    out = VGroup()
    for (a, b), y in zip([("order 0", "S"), ("order 1", "exp H"), ("order 2", "1/λ")], ROWS_Y):
        out.add(VGroup(T(a, 22, GREY), T(b, 28, TEXT)).arrange(DOWN, buff=0.06).move_to([0, y, 0]))
    return out


class S00Title(TitleCard):
    LESSON = "Diversity, Disturbance and Succession"
    TITLE = "Same four species, different diversity"


# ---------------------------------------------------------------------------------------------
class S01Plots(SpokenScene):
    def construct(self):
        pA = make_plot(CA, 1).move_to([-3.3, 0.15, 0])
        pB = make_plot(CB, 2).move_to([3.3, 0.15, 0])
        lA = T("Plot A", 36, TEXT, weight=BOLD).move_to([-3.3, 2.85, 0])
        lB = T("Plot B", 36, TEXT, weight=BOLD).move_to([3.3, 2.85, 0])
        self.at("Two plots")
        self.play(FadeIn(pA.frame), FadeIn(pB.frame), FadeIn(lA), FadeIn(lB), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in pA.dots], lag_ratio=0.01),
                  LaggedStart(*[FadeIn(m, scale=0.5) for m in pB.dots], lag_ratio=0.01), run_time=2.0)
        self.at("Each plot has")
        n100 = [T("100 individuals", 24, GREY).move_to([x, -2.3, 0]) for x in (-3.3, 3.3)]
        self.play(*[FadeIn(n) for n in n100], run_time=0.5)
        self.at("every species")
        rA = count_row(CA, -3.3, -2.85)
        self.play(FadeIn(rA, shift=UP * 0.1), run_time=0.6)
        self.at("the counts are")
        rB = count_row(CB, 3.3, -2.85)
        self.play(FadeIn(rB, shift=UP * 0.1), run_time=0.6)
        self.at("more diverse")
        q = T("?", 110, GOLD, font=TITLE_FONT, weight=BOLD).move_to([0, 0.15, 0])
        self.play(GrowFromCenter(q), run_time=0.5)
        self.at("decide to count")
        self.play(Indicate(rA, color=TEXT, scale_factor=1.08), Indicate(rB, color=TEXT, scale_factor=1.08), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Richness(SpokenScene):
    def construct(self):
        pA = make_plot(CA, 1).move_to([-3.3, 0.15, 0])
        pB = make_plot(CB, 2).move_to([3.3, 0.15, 0])
        lA = T("Plot A", 36, TEXT, weight=BOLD).move_to([-3.3, 2.85, 0])
        lB = T("Plot B", 36, TEXT, weight=BOLD).move_to([3.3, 2.85, 0])
        self.add(pA, pB, lA, lB)
        self.at("Start with richness")
        self.play(pA.animate.scale(0.38).move_to([LX - 1.05, 2.5, 0]), pB.animate.scale(0.38).move_to([RX - 1.05, 2.5, 0]),
                  lA.animate.scale(0.9).move_to([LX + 0.95, 2.5, 0]), lB.animate.scale(0.9).move_to([RX + 0.95, 2.5, 0]),
                  run_time=1.0)
        base = -1.2
        aB, aL, aM, aLine = bar_set(CA, [str(c) for c in CA], LX, base)
        bB, bL, bM, bLine = bar_set(CB, [str(c) for c in CB], RX, base)
        self.at("number of species present")
        self.play(FadeIn(aLine), FadeIn(bLine), LaggedStart(*[FadeIn(m, scale=0.5) for m in list(aM) + list(bM)], lag_ratio=0.12), run_time=1.4)
        self.at("Both plots have four")
        sA = M("S = 4", 36, TEXT).move_to([LX, -2.75, 0])
        sB = M("S = 4", 36, TEXT).move_to([RX, -2.75, 0])
        self.play(FadeIn(sA, shift=UP * 0.1), FadeIn(sB, shift=UP * 0.1), run_time=0.6)
        self.at("is tied")
        eq = M("=", 50, GOLD).move_to([0, -2.75, 0])
        self.play(GrowFromCenter(eq), run_time=0.4)
        self.at("ignores abundance")
        self.play(*[GrowFromEdge(b, DOWN) for b in list(aB) + list(bB)], *[FadeIn(l) for l in list(aL) + list(bL)],
                  sA.animate.set_opacity(0.45), sB.animate.set_opacity(0.45), eq.animate.set_opacity(0.45), run_time=1.0)
        self.at("two common species")
        com = T("common", 24, GREY).move_to([RX - 1.1, -2.05, 0])
        rare = T("rare", 24, GREY).move_to([RX + 1.1, -2.05, 0])
        self.play(FadeIn(com), FadeIn(rare), run_time=0.5)
        self.at("relative abundance")
        head = VGroup(T("share of", 26, TEXT), T("individuals", 26, TEXT)).arrange(DOWN, buff=0.05).move_to([0, 0.0, 0])
        newA = [M(s, 22, TEXT).next_to(aB[i], UP, buff=0.1) for i, s in enumerate(SHARE_A)]
        newB = [M(s, 22, TEXT).next_to(bB[i], UP, buff=0.1) for i, s in enumerate(SHARE_B)]
        self.play(*[ReplacementTransform(aL[i], newA[i]) for i in range(4)],
                  *[ReplacementTransform(bL[i], newB[i]) for i in range(4)], FadeIn(head), run_time=0.8)
        self.at("every share")
        self.play(*[Indicate(l, color=GOLD, scale_factor=1.25) for l in newA], run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def tiny_panels(scene):
    pA = mini_plot(CA, 1, LX)
    pB = mini_plot(CB, 2, RX)
    lA = plot_label("Plot A", LX).scale(0.9).move_to([LX + 0.95, 2.5, 0])
    lB = plot_label("Plot B", RX).scale(0.9).move_to([RX + 0.95, 2.5, 0])
    scene.add(pA, pB, lA, lB)
    return pA, pB, lA, lB


class S03Simpson(SpokenScene):
    def construct(self):
        pA, pB, lA, lB = tiny_panels(self)
        base = -1.2
        aB, aL, aM, aLine = bar_set(CA, SHARE_A, LX, base)
        bB, bL, bM, bLine = bar_set(CB, SHARE_B, RX, base)
        for g in (aB, aL, aM, bB, bL, bM):
            pass
        self.add(aB, aL, aM, aLine, bB, bL, bM, bLine)
        # bar heights above are count-scaled, as they were in the last scene
        L = 3.0
        top = 1.0
        framesA = Square(side_length=L, stroke_color=GREY, stroke_width=3).move_to([LX, top - L / 2, 0])
        framesB = Square(side_length=L, stroke_color=GREY, stroke_width=3).move_to([RX, top - L / 2, 0])

        def strips(shares, fr):
            out = VGroup()
            tl = fr.get_corner(UL)
            off = 0.0
            for k, p in enumerate(shares):
                s_ = p * L
                out.add(Rectangle(width=s_, height=0.12, stroke_width=0, fill_color=SP[k], fill_opacity=0.9).move_to(tl + np.array([off + s_ / 2, 0.14, 0])))
                out.add(Rectangle(width=0.12, height=s_, stroke_width=0, fill_color=SP[k], fill_opacity=0.9).move_to(tl + np.array([-0.14, -off - s_ / 2, 0])))
                off += s_
            return out
        stA = strips([0.25] * 4, framesA)
        stB = strips([0.4, 0.4, 0.1, 0.1], framesB)
        self.at("Pull two individuals")
        self.play(FadeOut(VGroup(aB, aL, aM, aLine, bB, bL, bM, bLine)), FadeIn(framesA), FadeIn(framesB), FadeIn(stA), FadeIn(stB), run_time=0.9)
        draw_t = VGroup(T("first draw", 22, GREY), T("second draw", 22, GREY)).arrange(DOWN, buff=0.1).move_to([0, 0.0, 0])
        self.play(FadeIn(draw_t), run_time=0.4)
        def squares(shares, fr):
            out = VGroup()
            tl = fr.get_corner(UL)
            off = 0.0
            for k, p in enumerate(shares):
                s = p * L
                sq = Square(side_length=s, stroke_color=SP[k], stroke_width=2, fill_color=SP[k], fill_opacity=0.7)
                sq.move_to(tl + np.array([off + s / 2, -off - s / 2, 0]))
                off += s
                out.add(sq)
            return out
        sqA = squares([0.25] * 4, framesA)
        sqB = squares([0.4, 0.4, 0.1, 0.1], framesB)
        self.play(FadeOut(draw_t), LaggedStart(*[GrowFromPoint(s, s.get_corner(UL)) for s in list(sqA) + list(sqB)], lag_ratio=0.1), run_time=1.6)
        self.at("in plot")
        lamA = M("λ = 0.25", 38, RED).move_to([LX, -2.6, 0])
        self.play(FadeIn(lamA, shift=UP * 0.1), run_time=0.5)
        self.at("in plot", nth=1)
        lamB = M("λ = 0.34", 38, RED).move_to([RX, -2.6, 0])
        self.play(FadeIn(lamB, shift=UP * 0.1), run_time=0.5)
        self.at("opposite way")
        note = T("λ rises as common species dominate", 26, RED).move_to([0, -3.3, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Effective(SpokenScene):
    def construct(self):
        pA, pB, lA, lB = tiny_panels(self)
        self.at("hard to compare")
        def hcard(h, l, cx):
            return VGroup(T("Shannon entropy H, in nats", 22, GREY), M(h, 30, TEXT), T("Simpson concentration λ", 22, GREY), M(l, 30, RED)).arrange(DOWN, buff=0.2).move_to([cx, 0.0, 0])
        hA = hcard("H = 1.386", "λ = 0.25", LX)
        hB = hcard("H = 1.194", "λ = 0.34", RX)
        self.play(FadeIn(hA, shift=UP * 0.1), FadeIn(hB, shift=UP * 0.1), run_time=0.7)
        self.at("effective number")
        labs = order_labels()
        self.play(FadeOut(hA), FadeOut(hB), FadeIn(labs), run_time=0.8)
        self.at("equally common")
        s_row = [blocks(4, BX["A"], ROWS_Y[0]), blocks(4, BX["B"], ROWS_Y[0])]
        vA0, vB0 = row_value(4, "A", ROWS_Y[0], "4"), row_value(4, "B", ROWS_Y[0], "4")
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in s_row[0]], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in s_row[1]], lag_ratio=0.15), FadeIn(vA0), FadeIn(vB0), run_time=1.2)
        self.at("by every measure")
        grp = []
        for y in ROWS_Y[1:]:
            grp += [blocks(4, BX["A"], y), row_value(4, "A", y, "4.00")]
        self.play(*[FadeIn(g, shift=RIGHT * 0.15) for g in grp], run_time=0.9)
        self.at("Shannon entropy")
        self.play(FadeIn(blocks(3.3, BX["B"], ROWS_Y[1]), shift=RIGHT * 0.15), FadeIn(row_value(3.3, "B", ROWS_Y[1], "3.30")), run_time=0.8)
        self.at("Inverse Simpson")
        self.play(FadeIn(blocks(2.94, BX["B"], ROWS_Y[2]), shift=RIGHT * 0.15), FadeIn(row_value(2.94, "B", ROWS_Y[2], "2.94")), run_time=0.8)
        self.finish()


def full_rows():
    g = VGroup()
    for side, vals in (("A", [4, 4, 4]), ("B", [4, 3.3, 2.94])):
        for y, v, t in zip(ROWS_Y, vals, (["4", "4.00", "4.00"] if side == "A" else ["4", "3.30", "2.94"])):
            g.add(blocks(v, BX[side], y), row_value(v, side, y, t))
    return g


class S05Orders(SpokenScene):
    def construct(self):
        pA, pB, lA, lB = tiny_panels(self)
        labs = order_labels()
        rows = full_rows()
        self.add(labs, rows)
        self.at("Notice the pattern")
        box = SurroundingRectangle(VGroup(*[m for m in rows if True][1::2]) if False else VGroup(*rows[1::2]), color=GOLD, buff=0.15, stroke_width=3)
        # a box around plot B's three rows
        rowsB = VGroup(*[rows[i] for i in (6, 7, 8, 9, 10, 11)])
        boxB = SurroundingRectangle(rowsB, color=GOLD, buff=0.18, stroke_width=3, corner_radius=0.12)
        self.play(Create(boxB), run_time=0.7)
        self.at("gives four species")
        self.play(Indicate(rowsB[0:2], color=GOLD, scale_factor=1.06), Indicate(labs[0], color=GOLD), run_time=0.8)
        self.at("next order")
        self.play(Indicate(rowsB[2:4], color=GOLD, scale_factor=1.06), Indicate(labs[1], color=GOLD), run_time=0.8)
        self.at("the one after")
        self.play(Indicate(rowsB[4:6], color=GOLD, scale_factor=1.06), Indicate(labs[2], color=GOLD), run_time=0.8)
        self.at("give more weight")
        note = T("higher order: more weight on common species", 26, TEXT).move_to([0, -2.75, 0])
        self.play(FadeOut(boxB), FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.at("rare species count")
        rare = VGroup(*pB.groups[2], *pB.groups[3])
        self.play(*[m.animate.scale(0.65).set_opacity(0.6) for m in rare], run_time=1.0)
        self.at("Evenness is")
        ev = T("evenness", 24, GREY).move_to([0, -3.3, 0])
        self.play(FadeIn(ev), run_time=0.4)
        self.at("for plot")
        eA = M("E = 1.00", 30, TEXT).move_to([-3.6, -3.3, 0])
        self.play(FadeIn(eA, shift=UP * 0.1), run_time=0.4)
        self.at("for plot", nth=1)
        eB = M("E = 0.735", 30, TEXT).move_to([3.9, -3.3, 0])
        self.play(FadeIn(eB, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Identity(SpokenScene):
    def construct(self):
        LXc, RXc = -4.2, 4.2
        base = -1.2
        unit = 0.075
        bB, bL, bM, bLine = bar_set(CB, [str(c) for c in CB], LXc, base, unit=unit, sp=0.85, w=0.55)
        for l in bLine:
            pass
        bLine = Line([LXc - 1.6, base, 0], [LXc + 1.6, base, 0], color=GREY, stroke_width=3)
        lab = T("Plot B", 34, TEXT, weight=BOLD).move_to([LXc, 2.9, 0])
        card_lines = VGroup(M("S = 4", 32, TEAL), M("exp H = 3.30", 32, TEAL), M("1/λ = 2.94", 32, TEAL)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        card_box = RoundedRectangle(corner_radius=0.2, width=card_lines.width + 0.7, height=card_lines.height + 0.7,
                                    stroke_color=TEAL, stroke_width=3, fill_color=TEAL, fill_opacity=0.08)
        card = VGroup(card_box, card_lines.move_to(card_box)).move_to([0, 0.4, 0])
        self.add(bB, bL, bM, bLine, lab, card)
        self.at("swap the labels")
        newcols = [SP[2], SP[3], SP[0], SP[1]]
        newm = [mark(k, 0.15).move_to(bM[i]) for i, k in enumerate([2, 3, 0, 1])]
        self.play(*[bB[i].animate.set_fill(newcols[i], 0.85) for i in range(4)],
                  *[ReplacementTransform(bM[i], newm[i]) for i in range(4)], run_time=1.2)
        self.at("stays the same")
        same = T("unchanged", 28, GREEN).next_to(card, DOWN, buff=0.3)
        self.play(Indicate(card, color=TEAL, scale_factor=1.06), FadeIn(same), run_time=1.0)
        self.at("which species are present")
        self.wait(0.1)
        self.at("share no species")
        rB, rL, rM, rLine = bar_set(CB, [str(c) for c in CB], RXc, base, unit=unit, sp=0.85, w=0.55, mk=alien)
        rLine = Line([RXc - 1.6, base, 0], [RXc + 1.6, base, 0], color=GREY, stroke_width=3)
        rlab = T("another plot", 34, TEXT, weight=BOLD).move_to([RXc, 2.9, 0])
        rnote = T("no species in common", 24, GREY).move_to([RXc, -2.4, 0])
        self.play(FadeIn(rLine), FadeIn(rlab), *[GrowFromEdge(b, DOWN) for b in rB], *[FadeIn(x) for x in rL], *[FadeIn(m) for m in rM], run_time=1.0)
        self.play(FadeIn(rnote), run_time=0.4)
        self.at("misses something")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        r1 = VGroup(T("Richness", 34, TEXT, weight=BOLD), T("ignores abundance", 34, GREY)).arrange(RIGHT, buff=0.4).move_to([0, 1.0, 0])
        r2 = VGroup(T("Higher orders", 34, TEXT, weight=BOLD), T("discount rare species", 34, GREY)).arrange(RIGHT, buff=0.4).move_to([0, -0.3, 0])
        self.at("ignores abundance")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.5)
        self.at("discount rare species")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
        self.at("always name")
        rule = T("Name the measure. Say what it misses.", 44, GOLD, font=TITLE_FONT).move_to([0, -1.9, 0])
        self.play(Write(rule), run_time=1.2)
        self.finish()


class S07End(EndCard):
    LINE = "Name the measure, and say what it misses."
