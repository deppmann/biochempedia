"""Mendel's peas: two cards, handed on at random  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = the R allele (round)
  ORANGE = the r allele (wrinkled)
  GREEN  = a pea seed (shape tells round from wrinkled)
  YELLOW = counts and the thing being highlighted right now
  GREY   = outlines, plants, squares, labels
  TEXT   = ratios and plain words
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
RC, WC = BLUE, ORANGE


def seed(kind="round", r=0.3, op=0.7):
    if kind == "round":
        s = Circle(radius=r, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=op)
    else:
        s = ParametricFunction(lambda t: np.array([r * (1 + 0.16 * np.sin(7 * t)) * np.cos(t),
                                                   r * (1 + 0.16 * np.sin(7 * t)) * np.sin(t), 0]),
                               t_range=[0, TAU], color=GREEN, stroke_width=3)
        s.set_fill(GREEN, op)
    return s


def ghost_seed(r=0.3):
    s = seed("wrinkled", r, 0)
    s.set_stroke(GREY, 3).set_fill(GREY, 0)
    return DashedVMobject(s, num_dashes=24)


def col(ch):
    return RC if ch == "R" else (WC if ch == "r" else GREY)


def geno(s, size=40):
    g = VGroup(*[M(ch, size, col(ch), weight=BOLD) for ch in s]).arrange(RIGHT, buff=0.04)
    return g


def card(ch, w=0.9, h=1.2, size=44):
    c = col(ch)
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=c, stroke_width=4,
                           fill_color=c, fill_opacity=0.2)
    return VGroup(box, M(ch, size, c, weight=BOLD).move_to(box))


def gamete(ch, r=0.42):
    c = col(ch)
    ci = Circle(radius=r, stroke_color=c, stroke_width=4, fill_color=c, fill_opacity=0.2)
    return VGroup(ci, M(ch, 34, c, weight=BOLD).move_to(ci))


def arr(a, b, color=GREY, w=5):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=0.22,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def pos_label(text, size=24, color=GREY):
    return T(text, size, color)


class S00Title(TitleCard):
    LESSON = "Mendel's peas"
    TITLE = "Two cards, handed on at random"


# ---------------------------------------------------------------------------------------------
class S01Count(SpokenScene):
    def construct(self):
        BX0, BW = -5.0, 10.0
        wr = BW * 1850 / 7324
        rw = BW - wr
        rseg = Rectangle(width=rw, height=0.95, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.22)
        wseg = Rectangle(width=wr, height=0.95, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.22)
        rseg.move_to([BX0 + rw / 2, -0.7, 0])
        wseg.move_to([BX0 + rw + wr / 2, -0.7, 0])
        title = T("7,324 seeds from the hybrids", 36, YELLOW, font=TITLE_FONT).move_to([0, 1.3, 0])
        self.at("Mendel counted")
        self.play(Write(title), run_time=0.9)
        self.play(GrowFromEdge(rseg, LEFT), GrowFromEdge(wseg, LEFT), run_time=0.8)
        ri = seed("round", 0.32).move_to(rseg)
        wi = seed("wrinkled", 0.32).move_to(wseg)
        rl = T("5,474 round", 30, YELLOW).next_to(rseg, UP, buff=0.2)
        wl = T("1,850 wrinkled", 30, YELLOW).next_to(wseg, UP, buff=0.2).align_to(wseg, RIGHT)
        self.at("That is")
        self.play(FadeIn(ri), FadeIn(wi), FadeIn(rl, shift=UP * 0.1), FadeIn(wl, shift=UP * 0.1), run_time=0.7)
        ratio = M("2.96 : 1", 44, TEXT, weight=BOLD).move_to([0, -2.1, 0])
        self.at("for every wrinkled")
        self.play(FadeIn(ratio, shift=UP * 0.15), run_time=0.5)
        # hybrids, all round
        f1 = VGroup(*[seed("round", 0.3) for _ in range(4)]).arrange(RIGHT, buff=0.25)
        f1lbl = T("hybrid seeds: all round", 30, TEXT)
        f1g = VGroup(f1, f1lbl).arrange(RIGHT, buff=0.5).move_to([-0.8, 2.85, 0])
        self.at("all been round")
        self.play(FadeOut(title), FadeIn(f1g, shift=DOWN * 0.15), run_time=0.7)
        gh = ghost_seed(0.3)
        gh.next_to(f1, RIGHT, buff=0.25).shift(UP * 0)
        self.at("vanished")
        # put the missing slot after the round seeds; label slides to make room
        self.play(f1lbl.animate.shift(RIGHT * 0.9), FadeIn(gh), run_time=0.5)
        q = T("?", 30, GREY, weight=BOLD).move_to(gh)
        self.play(FadeIn(q), run_time=0.3)
        curve = CurvedArrow(gh.get_bottom() + DOWN * 0.1, wseg.get_top() + UP * 0.9 + LEFT * 0.0, angle=-0.9,
                            color=ORANGE, stroke_width=5)
        curve = arr([gh.get_center()[0], 2.3, 0], [wseg.get_center()[0], 0.45, 0], ORANGE)
        self.at("came back")
        self.play(GrowArrow(curve), Indicate(VGroup(wseg, wi), color=ORANGE, scale_factor=1.08), run_time=0.8)
        self.at("What must a plant carry")
        qt = T("What must a plant carry?", 44, TEXT, font=TITLE_FONT).move_to([0, 2.3, 0])
        self.play(FadeOut(f1g), FadeOut(gh), FadeOut(q), FadeOut(curve), FadeOut(rl), FadeOut(wl), FadeOut(ratio), run_time=0.5)
        cards = VGroup(card("?"), card("?")).arrange(RIGHT, buff=0.4).move_to([0, 0.95, 0])
        self.play(FadeIn(qt, shift=UP * 0.1), FadeIn(cards), run_time=0.7)
        self.finish()


def plant_box(x, y, w=3.8, h=2.7):
    return RoundedRectangle(corner_radius=0.3, width=w, height=h, stroke_color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0])


# ---------------------------------------------------------------------------------------------
class S02Cards(SpokenScene):
    def construct(self):
        PX, PY = -3.7, -0.3
        box = plant_box(PX, PY)
        plbl = T("hybrid plant", 26, GREY).next_to(box, DOWN, buff=0.15)
        blank = VGroup(card("?"), card("?")).arrange(RIGHT, buff=0.5).move_to(box)
        self.play(FadeIn(box), FadeIn(plbl), run_time=0.6)
        self.at("two cards")
        self.play(FadeIn(blank), run_time=0.6)
        fR, fr = card("R"), card("r")
        fR.move_to(blank[0]); fr.move_to(blank[1])
        self.at("Each card is an allele")
        al = T("each card is an allele", 28, TEXT).move_to([PX, 2.3, 0])
        self.play(ReplacementTransform(blank[0], fR), ReplacementTransform(blank[1], fr), FadeIn(al, shift=DOWN * 0.1), run_time=0.7)
        self.play(Indicate(VGroup(fR, fr), color=YELLOW, scale_factor=1.1), run_time=0.5)
        lg1 = T("R = round allele", 26, RC)
        lg2 = T("r = wrinkled allele", 26, WC)
        lg = VGroup(lg1, lg2).arrange(RIGHT, buff=0.5).move_to([PX, -2.55, 0]).shift(RIGHT * 0.0)
        # keep it inside the left half
        lg.arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([PX, -2.95, 0])
        plbl.move_to([PX, -1.95, 0])
        self.at("Capital R")
        self.play(FadeIn(lg1, shift=UP * 0.1), Indicate(fR, color=RC), run_time=0.5)
        self.at("Small r")
        self.play(FadeIn(lg2, shift=UP * 0.1), Indicate(fr, color=WC), run_time=0.5)
        gl = VGroup(T("genotype: ", 28, TEXT), geno("Rr", 36)).arrange(RIGHT, buff=0.1).move_to([PX, 2.3, 0])
        self.at("its genotype is")
        self.play(ReplacementTransform(al, gl), run_time=0.6)
        # gametes
        order = ["R", "r", "r", "R", "r", "R"]
        gs = VGroup(*[gamete(ch) for ch in order]).arrange(RIGHT, buff=0.2).move_to([2.4, -0.3, 0])
        glab = T("eggs and pollen (gametes)", 28, TEXT).next_to(gs, UP, buff=0.5)
        self.at("When it makes eggs and pollen")
        self.play(FadeIn(glab, shift=DOWN * 0.1), run_time=0.5)
        self.at("hands one card")
        src = VGroup(fR, fr)
        self.play(LaggedStart(*[FadeIn(g, shift=LEFT * 1.2) for g in gs], lag_ratio=0.35), run_time=2.0)
        eq = T("equal numbers", 30, YELLOW).next_to(gs, DOWN, buff=0.5)
        self.at("equal numbers")
        Rs = VGroup(*[g for g, ch in zip(gs, order) if ch == "R"])
        rs = VGroup(*[g for g, ch in zip(gs, order) if ch == "r"])
        self.play(FadeIn(eq), Indicate(Rs, color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.play(Indicate(rs, color=YELLOW, scale_factor=1.15), run_time=0.6)
        self.finish()


# square helpers (same place in s03 and s04)
GX, GY, CW, CH = -2.6, -0.45, 1.8, 1.7


def cell_pos(i, j):
    return np.array([GX + (j - 0.5) * CW, GY + (0.5 - i) * CH, 0])


def build_grid():
    cells = [[Rectangle(width=CW, height=CH, stroke_color=GREY, stroke_width=3).move_to(cell_pos(i, j))
              for j in range(2)] for i in range(2)]
    return cells


def axis_labels():
    pol = [geno(c, 38).move_to(cell_pos(0, j) + UP * (CH / 2 + 0.45)) for j, c in enumerate("Rr")]
    egg = [geno(c, 38).move_to(cell_pos(i, 0) + LEFT * (CW / 2 + 0.45)) for i, c in enumerate("Rr")]
    pl = T("pollen", 24, GREY).move_to([GX, GY + CH + 0.95, 0])
    el = T("eggs", 24, GREY).move_to([GX - CW - 1.05, GY, 0])
    return pol, egg, pl, el


GENO = [["RR", "Rr"], ["Rr", "rr"]]
TALLY_X = 1.7
TALLY_Y = [1.0, -0.45, -1.9]


def tally_rows():
    out = []
    for (f, g), y in zip([("1/4", "RR"), ("1/2", "Rr"), ("1/4", "rr")], TALLY_Y):
        row = VGroup(M(f, 32, YELLOW), geno(g, 38)).arrange(RIGHT, buff=0.25).move_to([TALLY_X, y, 0])
        out.append(row)
    return out


class S03Square(SpokenScene):
    def construct(self):
        head = VGroup(geno("Rr", 44), M("x", 36, GREY), geno("Rr", 44)).arrange(RIGHT, buff=0.35).move_to([GX, 3.0, 0])
        cells = build_grid()
        pol, egg, pl, el = axis_labels()
        self.at("pollinate itself")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)
        self.at("meet at random")
        self.play(FadeIn(pl), FadeIn(el), *[FadeIn(x, shift=DOWN * 0.1) for x in pol],
                  *[FadeIn(x, shift=RIGHT * 0.1) for x in egg], run_time=0.8)
        self.play(*[Create(c) for r in cells for c in r], run_time=0.8)
        fills = {}
        order = [(0, 0, "meets", 0), (0, 1, "meets", 1), (1, 0, "So does", 0), (1, 1, "And small r meeting", 0)]
        for i, j, ph, n in order:
            g = geno(GENO[i][j], 46).move_to(cell_pos(i, j))
            fills[(i, j)] = g
            self.at(ph, nth=n)
            self.play(cells[i][j].animate.set_fill(YELLOW, 0.14), FadeIn(g, scale=1.2), run_time=0.45)
            self.play(cells[i][j].animate.set_fill(YELLOW, 0), run_time=0.2)
        rows = tally_rows()
        self.at("The offspring are")
        self.wait(0.01)
        self.at("one quarter")
        self.play(FadeIn(rows[0], shift=LEFT * 0.2), run_time=0.4)
        self.at("one half")
        self.play(FadeIn(rows[1], shift=LEFT * 0.2), run_time=0.4)
        self.at("and one quarter")
        self.play(FadeIn(rows[2], shift=LEFT * 0.2), run_time=0.4)
        self.finish()


class S04Dominant(SpokenScene):
    def construct(self):
        head = VGroup(geno("Rr", 44), M("x", 36, GREY), geno("Rr", 44)).arrange(RIGHT, buff=0.35).move_to([GX, 3.0, 0])
        cells = build_grid()
        pol, egg, pl, el = axis_labels()
        fills = {(i, j): geno(GENO[i][j], 46).move_to(cell_pos(i, j)) for i in range(2) for j in range(2)}
        rows = tally_rows()
        self.add(head, pl, el, *pol, *egg, *[c for r in cells for c in r], *fills.values(), *rows)
        self.at("Now ask")
        self.wait(0.3)
        seeds = {}
        for (i, j), g in fills.items():
            kind = "wrinkled" if GENO[i][j] == "rr" else "round"
            seeds[(i, j)] = seed(kind, 0.32).move_to(cell_pos(i, j) + RIGHT * 0.52)
        self.at("One R is enough")
        shifts = [g.animate.shift(LEFT * 0.42) for g in fills.values()]
        self.play(*shifts, run_time=0.5)
        Rletters = VGroup(fills[(0, 0)][0], fills[(0, 1)][0], fills[(1, 0)][0])
        self.play(*[FadeIn(seeds[k], scale=0.6) for k in [(0, 0), (0, 1), (1, 0)]], run_time=0.5)
        self.play(Indicate(Rletters, color=YELLOW, scale_factor=1.3), run_time=0.6)
        self.at("look the same")
        self.play(*[Indicate(seeds[k], color=YELLOW, scale_factor=1.25) for k in [(0, 0), (0, 1), (1, 0)]], run_time=0.8)
        self.at("Only")
        self.play(FadeIn(seeds[(1, 1)], scale=0.6), run_time=0.4)
        self.play(Indicate(seeds[(1, 1)], color=ORANGE, scale_factor=1.3), run_time=0.5)
        dom = T("round: dominant", 26, TEXT).move_to([-4.1, -2.95, 0])
        rec = T("wrinkled: recessive (latent)", 26, TEXT).move_to([0.1, -2.95, 0])
        self.at("dominant character")
        self.play(FadeIn(dom, shift=UP * 0.1), run_time=0.5)
        self.at("recessive character")
        self.play(FadeIn(rec, shift=UP * 0.1), run_time=0.5)
        b1 = Brace(VGroup(rows[0], rows[1]), RIGHT, color=GREY, buff=0.2)
        b2 = Brace(rows[2], RIGHT, color=GREY, buff=0.2)
        l1 = VGroup(seed("round", 0.26), T("3/4 round", 30, YELLOW)).arrange(RIGHT, buff=0.15)
        l2 = VGroup(seed("wrinkled", 0.26), T("1/4 wrinkled", 30, YELLOW)).arrange(RIGHT, buff=0.15)
        l1.next_to(b1, RIGHT, buff=0.2)
        l2.next_to(b2, RIGHT, buff=0.2)
        self.at("three quarters")
        self.play(GrowFromCenter(b1), FadeIn(l1, shift=LEFT * 0.2), run_time=0.7)
        self.at("one quarter are wrinkled")
        self.play(GrowFromCenter(b2), FadeIn(l2, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


class S05Test(SpokenScene):
    def construct(self):
        BX0, BW = -5.0, 10.0
        w1 = BW * 193 / 565
        w2 = BW - w1
        # two look-alike seeds
        sA = seed("round", 0.6).move_to([-1.8, 1.4, 0])
        sB = seed("round", 0.6).move_to([1.8, 1.4, 0])
        qa = T("?", 36, TEXT, weight=BOLD).move_to(sA)
        qb = T("?", 36, TEXT, weight=BOLD).move_to(sB)
        look = T("look alike", 30, GREY).move_to([0, 2.7, 0])
        self.at("Round seeds should")
        self.play(FadeIn(sA, scale=0.7), FadeIn(sB, scale=0.7), FadeIn(qa), FadeIn(qb), run_time=0.7)
        self.at("two kinds of plant")
        self.play(FadeIn(look, shift=DOWN * 0.1), Indicate(VGroup(sA, sB), color=YELLOW, scale_factor=1.12), run_time=0.8)
        title = T("565 plants, each pollinating itself", 34, YELLOW, font=TITLE_FONT).move_to([0, 2.8, 0])
        s1 = Rectangle(width=w1, height=1.2, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.22)
        s2 = Rectangle(width=w2, height=1.2, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.22)
        s1.move_to([BX0 + w1 / 2, 1.4, 0])
        s2.move_to([BX0 + w1 + w2 / 2, 1.4, 0])
        self.at("Mendel grew")
        self.play(FadeOut(sA), FadeOut(sB), FadeOut(qa), FadeOut(qb), FadeOut(look),
                  FadeIn(title, shift=DOWN * 0.1), run_time=0.5)
        self.play(GrowFromEdge(s1, LEFT), GrowFromEdge(s2, LEFT), run_time=0.7)
        n1 = M("193", 48, YELLOW, weight=BOLD).move_to(s1)
        d1 = T("only round seeds", 28, TEXT).next_to(s1, DOWN, buff=0.4)
        row1 = VGroup(*[seed("round", 0.36) for _ in range(4)]).arrange(RIGHT, buff=0.25).next_to(d1, DOWN, buff=0.4)
        n2 = M("372", 48, YELLOW, weight=BOLD).move_to(s2)
        d2 = T("round and wrinkled seeds", 28, TEXT).next_to(s2, DOWN, buff=0.4)
        row2 = VGroup(*[seed("round", 0.36) for _ in range(3)], seed("wrinkled", 0.36)).arrange(RIGHT, buff=0.25).next_to(d2, DOWN, buff=0.4)
        d1.move_to([s1.get_center()[0], d1.get_center()[1], 0]); row1.move_to([s1.get_center()[0], row1.get_center()[1], 0])
        d2.move_to([s2.get_center()[0], d2.get_center()[1], 0]); row2.move_to([s2.get_center()[0], row2.get_center()[1], 0])
        self.at("gave only round")
        self.play(FadeIn(n1), FadeIn(d1, shift=UP * 0.1), FadeIn(row1), Indicate(s1, color=YELLOW, scale_factor=1.04), run_time=0.8)
        self.at("gave round and wrinkled")
        self.play(FadeIn(n2), FadeIn(d2, shift=UP * 0.1), FadeIn(row2), Indicate(s2, color=YELLOW, scale_factor=1.04), run_time=0.8)
        g1 = VGroup(T("about 1/3", 32, YELLOW), geno("RR", 48)).arrange(RIGHT, buff=0.25).move_to([s1.get_center()[0], -2.5, 0])
        g2 = VGroup(T("about 2/3", 32, YELLOW), geno("Rr", 48)).arrange(RIGHT, buff=0.25).move_to([s2.get_center()[0], -2.5, 0])
        self.at("one third")
        self.play(FadeIn(g1, shift=UP * 0.15), run_time=0.6)
        self.at("two thirds")
        self.play(FadeIn(g2, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        title = T("The law of segregation", 36, TEXT, font=TITLE_FONT).move_to([0, 3.05, 0])
        PX, PY = -3.9, 0.95
        box = plant_box(PX, PY, 3.4, 2.4)
        cR, cr = card("R", 0.8, 1.05, 40), card("r", 0.8, 1.05, 40)
        pair = VGroup(cR, cr).arrange(RIGHT, buff=0.4).move_to(box)
        self.at("law of segregation")
        self.play(Write(title), FadeIn(box), FadeIn(pair), run_time=0.9)
        g1, g2 = gamete("R", 0.6), gamete("r", 0.6)
        g1.move_to([0.9, PY + 0.9, 0]); g2.move_to([0.9, PY - 0.9, 0])
        a1 = arr([PX + 1.8, PY + 0.3, 0], [0.2, PY + 0.9, 0], GREY)
        a2 = arr([PX + 1.8, PY - 0.3, 0], [0.2, PY - 0.9, 0], GREY)
        self.at("separate into different gametes")
        cR2, cr2 = cR.copy(), cr.copy()
        self.play(GrowArrow(a1), ReplacementTransform(cR2, g1), run_time=0.7)
        self.play(GrowArrow(a2), ReplacementTransform(cr2, g2), run_time=0.7)
        one = T("one allele in each gamete", 28, TEXT).move_to([3.9, PY, 0])
        self.at("Each gamete carries one")
        self.play(FadeIn(one, shift=LEFT * 0.1), run_time=0.5)
        div = Line([0, -1.0, 0], [0, -3.4, 0], color=GREY, stroke_width=3)
        lp = VGroup(M("3 : 1", 50, TEXT, weight=BOLD),
                    VGroup(seed("round", 0.32), seed("wrinkled", 0.32)).arrange(RIGHT, buff=0.3)).arrange(RIGHT, buff=0.5).move_to([-3.2, -1.8, 0])
        lpl = T("phenotype: what you see", 28, TEXT).move_to([-3.2, -2.9, 0])
        rp = VGroup(M("1 : 2 : 1", 50, TEXT, weight=BOLD),
                    VGroup(geno("RR", 40), geno("Rr", 40), geno("rr", 40)).arrange(RIGHT, buff=0.35)).arrange(DOWN, buff=0.2)
        rp.move_to([3.2, -1.95, 0])
        rpl = T("genotype: what the plant carries", 28, TEXT).move_to([3.2, -3.1, 0])
        self.at("Keep two things apart")
        self.play(Create(div), run_time=0.4)
        self.at("phenotype ratio")
        self.play(FadeIn(lp, shift=UP * 0.15), run_time=0.6)
        self.at("what you see")
        self.play(FadeIn(lpl), run_time=0.4)
        self.at("genotype ratio")
        self.play(FadeIn(rp, shift=UP * 0.15), run_time=0.6)
        self.at("what the plant carries")
        self.play(FadeIn(rpl), run_time=0.4)
        self.finish()


class S07End(EndCard):
    LINE = "Alleles separate into gametes, and each carries one."
