"""Sex linkage: sons take their mother's X  (Biochemistrypedia explainer, Genetics course)

COLOR MAP (one color per concept, whole film)
  RED    = the red-eye allele X+ and red eyes
  TEXT   = the white-eye allele Xw and white eyes (near-white)
  BLUE   = X chromosome
  GREEN  = Y chromosome
  YELLOW = what is highlighted or passed on (arrows from parent to child, the not-equal sign)
  GOLD   = counts and fractions (1/4, 100)
  GREY   = frames, labels, fly heads
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

RED_HEX = str(RED)


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def head(red, s=1.0):
    """A fly head seen from the front: two eyes, red or white."""
    h = Ellipse(width=1.0 * s, height=0.75 * s, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
    ec = RED if red else TEXT
    eyes = VGroup(*[Circle(radius=0.22 * s, stroke_color=GREY, stroke_width=2, fill_color=ec, fill_opacity=1)
                    .move_to(h.get_center() + RIGHT * dx * s) for dx in (-0.3, 0.3)])
    return VGroup(h, eyes)


def gmark(tokens, size=30):
    """Genotype such as X+Xw or XwY, with real superscripts; the + is red, the w is white."""
    s = ""
    for t in tokens:
        if t == "Y":
            s += "Y"
        else:
            col = RED_HEX if t[1:] == "+" else str(TEXT)
            s += f'X<sup><span foreground="{col}">{t[1:]}</span></sup>'
    return MarkupText(s, font=FONT, font_size=size, color=TEXT)


def card(tokens, red, sex=None, s=1.0, gsize=30, ssize=24):
    parts = [head(red, s)]
    if tokens:
        parts.append(gmark(tokens, gsize))
    if sex:
        parts.append(T(sex, ssize, GREY))
    return VGroup(*parts).arrange(DOWN, buff=0.1)


def chrom(kind, h=3.0, band=False):
    """A chromosome as a capsule: X is blue, Y is green and shorter."""
    col = BLUE if kind == "X" else GREEN
    hh = h if kind == "X" else h * 0.72
    body = RoundedRectangle(corner_radius=0.25, width=0.5, height=hh, stroke_color=col, stroke_width=4,
                            fill_color=col, fill_opacity=0.3)
    g = VGroup(body)
    g.body = body
    return g


def band_at(ch, y_off, color=TEXT, filled=False):
    b = Rectangle(width=0.5, height=0.18, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=1 if filled else 0.0)
    return b.move_to(ch.body.get_center() + UP * y_off)


def key(tokens, label):
    return VGroup(gmark(tokens, 32), T(label, 26, GREY)).arrange(RIGHT, buff=0.25)


def aline(a, b, color=YELLOW, w=6):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=0.25,
                 max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=14)


# Punnett grid geometry shared by scenes 3 and 5
COLX = [-1.5, 1.3]
ROWY = [0.85, -1.65]
HDRY = 2.6
RHX = -4.1


def cellbox(i, j):
    return Rectangle(width=2.7, height=2.4, stroke_color=GREY, stroke_width=2).move_to([COLX[i], ROWY[j], 0])


def grid_skeleton(eggs, sperm):
    boxes = VGroup(*[cellbox(i, j) for j in range(2) for i in range(2)])
    heads = VGroup(*[gmark([a], 36).move_to([COLX[i], HDRY, 0]) for i, a in enumerate(eggs)])
    rows = VGroup(*[gmark([b], 36).move_to([RHX, ROWY[j], 0]) for j, b in enumerate(sperm)])
    lab_e = T("eggs", 24, GREY).move_to([np.mean(COLX), HDRY + 0.62, 0])
    lab_s = T("sperm", 24, GREY).move_to([RHX, HDRY, 0])
    return boxes, heads, rows, lab_e, lab_s


def cell_card(i, j, tokens, red, sex):
    return card(tokens, red, sex, s=1.1, gsize=30, ssize=24).move_to([COLX[i], ROWY[j], 0])


# ---------------------------------------------------------------------------------------------
class S00Title(TitleCard):
    LESSON = "Sex linkage and non-Mendelian inheritance"
    TITLE = "Sons Take Their Mother's X"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    """Two reciprocal crosses, two different answers."""

    def construct(self):
        ycard = [1.6, -1.5]
        wm = card(None, False, "white male", s=1.7, ssize=28).move_to([-4.15, ycard[0], 0])
        rf = card(None, True, "red female", s=1.7, ssize=28).move_to([-0.75, ycard[0], 0])
        x1 = T("x", 40, GREY).move_to([-2.45, ycard[0] + 0.1, 0])
        wf = card(None, False, "white female", s=1.7, ssize=28).move_to([-4.15, ycard[1], 0])
        rm = card(None, True, "red male", s=1.7, ssize=28).move_to([-0.75, ycard[1], 0])
        x2 = T("x", 40, GREY).move_to([-2.45, ycard[1] + 0.1, 0])
        q1 = chip("?", YELLOW, size=64, pad=0.4).move_to([3.75, ycard[0] + 0.1, 0])
        q2 = chip("?", YELLOW, size=64, pad=0.4).move_to([3.75, ycard[1] + 0.1, 0])
        ar1 = aline([0.85, ycard[0] + 0.1, 0], [2.65, ycard[0] + 0.1, 0], GREY)
        ar2 = aline([0.85, ycard[1] + 0.1, 0], [2.65, ycard[1] + 0.1, 0], GREY)
        neq = T("≠", 80, YELLOW, weight=BOLD).move_to([3.75, (ycard[0] + ycard[1]) / 2 + 0.1, 0])
        note = T("Mendel's peas: the same result whichever plant was the mother", 26, GREY).move_to([0, -3.35, 0])

        self.at("male fruit fly")
        self.play(FadeIn(wm, shift=UP * 0.2), run_time=0.6)
        self.at("laboratory full")
        self.play(FadeIn(x1), FadeIn(rf, shift=UP * 0.2), run_time=0.6)
        self.at("its crosses")
        self.play(GrowArrow(ar1), FadeIn(q1, scale=0.8), run_time=0.6)
        self.at("different answers")
        self.play(FadeIn(wf, shift=UP * 0.2), FadeIn(x2), FadeIn(rm, shift=UP * 0.2), run_time=0.6)
        self.at("depending on")
        self.play(GrowArrow(ar2), FadeIn(q2, scale=0.8), run_time=0.4)
        self.at("which parent was white")
        self.play(FadeIn(neq, scale=1.4), run_time=0.5)
        self.at("peas never")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.at("so why would")
        self.play(Indicate(neq, color=YELLOW, scale_factor=1.3), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Hemizygous(SpokenScene):
    """Female XX, male XY: the male has one copy of the white gene, and it comes from his mother."""

    def construct(self):
        H = 3.4
        by = 0.75   # band height above chromosome centre
        cy = -0.1
        fx = [-4.7, -3.3]
        mx = [2.6, 4.2]
        f1, f2 = chrom("X", H).move_to([fx[0], cy, 0]), chrom("X", H).move_to([fx[1], cy, 0])
        m1 = chrom("X", H).move_to([mx[0], cy, 0])
        my = chrom("Y", H)
        my.move_to([mx[1], cy + H / 2 - my.body.height / 2, 0])  # top-aligned, shorter than the X
        fb1, fb2, mb1 = band_at(f1, by), band_at(f2, by), band_at(m1, by)
        slot = DashedVMobject(Rectangle(width=0.5, height=0.18, stroke_color=TEXT, stroke_width=3), num_dashes=16)
        slot.move_to([mx[1], cy + by, 0])
        flab = T("female", 30, GREY).move_to([np.mean(fx), -2.4, 0])
        mlab = T("male", 30, GREY).move_to([np.mean(mx), -2.4, 0])
        fg = gmark(["X", "X"], 36)
        fg = MarkupText("XX", font=FONT, font_size=40, color=BLUE).move_to([np.mean(fx), -3.0, 0])
        mg = MarkupText('<span foreground="%s">X</span><span foreground="%s">Y</span>' % (BLUE, GREEN),
                        font=FONT, font_size=40).move_to([np.mean(mx), -3.0, 0])

        self.at("the X chromosome")
        self.play(FadeIn(VGroup(f1, f2, m1)), FadeIn(flab), run_time=0.7)
        self.at("a female fly")
        self.play(FadeIn(fg, shift=UP * 0.1), run_time=0.4)
        self.at("a male fly")
        self.play(FadeIn(my), FadeIn(mlab), FadeIn(mg, shift=UP * 0.1), run_time=0.6)
        self.at("the white gene")
        glab = T("white gene", 28, TEXT).move_to([-0.35, cy + by, 0])
        a1 = aline([-1.5, cy + by, 0], [-2.95, cy + by, 0], GREY, 4)
        a2 = aline([0.8, cy + by, 0], [2.25, cy + by, 0], GREY, 4)
        self.play(FadeIn(glab), Create(fb1), Create(fb2), Create(mb1), GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        self.at("carries no copy")
        nolab = T("no copy", 26, TEXT).move_to([5.55, cy + by - 0.5, 0])
        self.play(Create(slot), FadeIn(nolab), run_time=0.6)
        self.at("so a male is")
        hemi = chip("hemizygous", YELLOW, size=32).move_to([np.mean(mx), 2.45, 0])
        self.play(FadeIn(hemi, shift=DOWN * 0.15), run_time=0.5)
        self.at("one copy")
        self.play(Indicate(mb1, color=YELLOW, scale_factor=1.5), run_time=0.8)
        self.at("not two")
        self.play(Indicate(mb1, color=YELLOW, scale_factor=1.5), run_time=0.8)
        self.at("his only X")
        arc = CurvedArrow([fx[1] + 0.35, 1.8, 0], [mx[0] - 0.35, 1.8, 0], angle=-TAU / 6, color=YELLOW, stroke_width=6)
        mom = T("from his mother", 30, YELLOW).move_to([-0.4, 3.0, 0])
        self.play(FadeOut(hemi), Create(arc), FadeIn(mom), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Crossa(SpokenScene):
    """Cross A: red female by white male; F1 all red; F2 three red to one white, every white one male."""

    def construct(self):
        k1 = key(["X+"], "red allele")
        k2 = key(["Xw"], "white allele")
        keys = VGroup(k1, k2).arrange(RIGHT, buff=1.3).move_to([0, 3.2, 0])
        mom = card(["X+", "X+"], True, "red female", s=1.5, gsize=38, ssize=28).move_to([-3.5, 1.45, 0])
        dad = card(["Xw", "Y"], False, "white male", s=1.5, gsize=38, ssize=28).move_to([3.5, 1.45, 0])
        times = T("x", 48, GREY).move_to([0, 1.45, 0])
        dau = card(["X+", "Xw"], True, "daughters", s=1.5, gsize=38, ssize=28).move_to([-2.6, -2.0, 0])
        son = card(["X+", "Y"], True, "sons", s=1.5, gsize=38, ssize=28).move_to([2.6, -2.0, 0])
        ar_d = aline([-0.4, 0.2, 0], [-2.0, -0.75, 0])
        ar_s = aline([0.4, 0.2, 0], [2.0, -0.75, 0])

        self.at("the red allele")
        self.play(FadeIn(k1, shift=DOWN * 0.1), run_time=0.5)
        self.at("for white")
        self.play(FadeIn(k2, shift=DOWN * 0.1), run_time=0.5)
        self.at("red female")
        self.play(FadeIn(mom, shift=UP * 0.2), run_time=0.6)
        self.at("white male")
        self.play(FadeIn(times), FadeIn(dad, shift=UP * 0.2), run_time=0.6)
        self.at("every daughter")
        self.play(GrowArrow(ar_d), FadeIn(dau, shift=UP * 0.2), run_time=0.6)
        self.at("every son")
        self.play(GrowArrow(ar_s), FadeIn(son, shift=UP * 0.2), run_time=0.6)
        self.at("red eyes")
        self.play(Indicate(dau[0], color=RED, scale_factor=1.2), Indicate(son[0], color=RED, scale_factor=1.2),
                  run_time=0.8)

        # --- the intercross -------------------------------------------------------------------
        self.at("cross those flies")
        boxes, heads, rows, lab_e, lab_s = grid_skeleton(["X+", "Xw"], ["X+", "Y"])
        self.play(FadeOut(VGroup(mom, dad, times, dau, son, ar_d, ar_s)),
                  k1.animate.move_to([4.75, 2.3, 0]), k2.animate.move_to([4.75, 1.5, 0]),
                  FadeIn(boxes), FadeIn(heads), FadeIn(rows), FadeIn(lab_e), FadeIn(lab_s), run_time=0.8)
        c00 = cell_card(0, 0, ["X+", "X+"], True, "female")
        c10 = cell_card(1, 0, ["X+", "Xw"], True, "female")
        c01 = cell_card(0, 1, ["X+", "Y"], True, "male")
        c11 = cell_card(1, 1, ["Xw", "Y"], False, "male")
        self.at("daughters all")
        rowbox0 = SurroundingRectangle(VGroup(boxes[0], boxes[1]), color=YELLOW, buff=0.06, stroke_width=4)
        self.play(FadeIn(c00, scale=0.9), FadeIn(c10, scale=0.9), Create(rowbox0), run_time=0.7)
        self.at("so they are red")
        self.play(Indicate(VGroup(c00[0], c10[0]), color=RED, scale_factor=1.15), run_time=0.7)
        self.at("sons get")
        rowbox1 = SurroundingRectangle(VGroup(boxes[2], boxes[3]), color=YELLOW, buff=0.06, stroke_width=4)
        self.play(FadeOut(rowbox0), FadeIn(c01, scale=0.9), FadeIn(c11, scale=0.9), Create(rowbox1), run_time=0.7)
        self.at("half are white")
        self.play(Indicate(c11[0], color=TEXT, scale_factor=1.25), run_time=0.7)
        self.at("three red")
        self.play(FadeOut(rowbox1), run_time=0.3)
        t3 = chip("3 red", RED, size=40).move_to([4.8, -0.2, 0])
        t1 = chip("1 white", TEXT, size=40).move_to([4.8, -1.5, 0])
        self.play(FadeIn(t3, shift=LEFT * 0.2), FadeIn(t1, shift=LEFT * 0.2), run_time=0.6)
        self.at("every white fly")
        hl = SurroundingRectangle(boxes[3], color=YELLOW, buff=0.06, stroke_width=5)
        self.play(Create(hl), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Crossb(SpokenScene):
    """Cross B, the reciprocal: criss-cross inheritance."""

    def construct(self):
        mom = card(["Xw", "Xw"], False, "white female", s=1.6, gsize=40, ssize=28).move_to([-3.4, 1.9, 0])
        dad = card(["X+", "Y"], True, "red male", s=1.6, gsize=40, ssize=28).move_to([3.4, 1.9, 0])
        times = T("x", 48, GREY).move_to([0, 1.9, 0])
        eggs = T("eggs: all", 26, GREY)
        eggs = VGroup(T("eggs: all ", 26, GREY), gmark(["Xw"], 30)).arrange(RIGHT, buff=0.12).move_to([-3.4, 0.45, 0])
        sperm = VGroup(T("sperm: ", 26, GREY), gmark(["X+"], 30), T(" or Y", 26, GREY)).arrange(RIGHT, buff=0.12).move_to([3.4, 0.45, 0])
        dau = card(["X+", "Xw"], True, "daughters", s=1.6, gsize=40, ssize=28).move_to([-3.4, -2.0, 0])
        son = card(["Xw", "Y"], False, "sons", s=1.6, gsize=40, ssize=28).move_to([3.4, -2.0, 0])
        ar_f = aline([3.0, 0.0, 0], [-3.0, -0.85, 0], RED)      # father's red eyes to his daughters
        ar_m = aline([-3.0, 0.0, 0], [3.0, -0.85, 0], TEXT)     # mother's white eyes to her sons
        crit = T("criss-cross inheritance", 30, YELLOW, weight=BOLD).move_to([0, -2.2, 0])
        crit_bg = Rectangle(width=crit.width + 0.3, height=crit.height + 0.2, stroke_width=0, fill_color=BG,
                            fill_opacity=0.9).move_to(crit)

        self.at("reverse the cross")
        self.play(FadeIn(mom, shift=UP * 0.2), FadeIn(times), FadeIn(dad, shift=UP * 0.2), run_time=0.8)
        self.at("the daughters are")
        self.play(FadeIn(dau, shift=UP * 0.2), run_time=0.6)
        self.at("the sons are")
        self.play(FadeIn(son, shift=UP * 0.2), run_time=0.6)
        self.at("the father's eyes")
        self.play(GrowArrow(ar_f), Indicate(dad[0], color=RED, scale_factor=1.15), run_time=0.8)
        self.at("the mother's pass")
        self.play(GrowArrow(ar_m), Indicate(mom[0], color=TEXT, scale_factor=1.15), run_time=0.8)
        self.at("criss-cross")
        self.play(FadeIn(crit_bg), FadeIn(crit, scale=1.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Ratio(SpokenScene):
    """The Cross B intercross: 1:1:1:1, 100 of each in 400 flies."""

    def construct(self):
        boxes = VGroup(*[cellbox(i, j) for j in range(2) for i in range(2)])
        lab_e = T("eggs", 24, GREY).move_to([np.mean(COLX), HDRY + 0.62, 0])
        lab_s = T("sperm", 24, GREY).move_to([RHX, HDRY, 0])
        eh = VGroup(*[gmark([a], 36).move_to([COLX[i], HDRY, 0]) for i, a in enumerate(["X+", "Xw"])])
        rh = VGroup(*[gmark([b], 36).move_to([RHX, ROWY[j], 0]) for j, b in enumerate(["Xw", "Y"])])
        cells = {
            (0, 0): cell_card(0, 0, ["X+", "Xw"], True, "red female"),
            (1, 0): cell_card(1, 0, ["Xw", "Xw"], False, "white female"),
            (0, 1): cell_card(0, 1, ["X+", "Y"], True, "red male"),
            (1, 1): cell_card(1, 1, ["Xw", "Y"], False, "white male"),
        }
        order = [(0, 0), (1, 0), (0, 1), (1, 1)]
        fr = {}
        for (i, j) in order:
            fr[(i, j)] = M("1/4", 30, GOLD).move_to([COLX[i] + 0.88, ROWY[j] + 0.9, 0])
        ratio = M("1:1:1:1", 40, YELLOW).move_to([4.8, -0.3, 0])
        total = M("400 flies", 36, GREY).move_to([4.75, 1.0, 0])

        self.at("cross those")
        self.play(FadeIn(boxes), run_time=0.5)
        self.at("makes eggs")
        self.play(FadeIn(lab_e), FadeIn(eh, shift=DOWN * 0.1), run_time=0.5)
        self.at("makes sperm")
        self.play(FadeIn(lab_s), FadeIn(rh, shift=RIGHT * 0.1), run_time=0.5)
        self.at("four combinations")
        self.play(*[FadeIn(cells[k], scale=0.9) for k in order], run_time=0.8)
        self.at("probability one quarter")
        self.play(*[FadeIn(fr[k]) for k in order], run_time=0.5)
        names = ["one red female", "one white female", "one red male", "one white male"]
        for k, nm in zip(order, names):
            self.at(nm)
            self.play(Indicate(cells[k][0], color=YELLOW, scale_factor=1.2), run_time=0.5)
        self.play(FadeIn(ratio, shift=LEFT * 0.2), run_time=0.5)
        self.at("flies expect")
        self.play(FadeIn(total), run_time=0.4)
        self.at("of each")
        hundred = {k: M("100", 32, GOLD).move_to(fr[k].get_center() + LEFT * 0.05) for k in order}
        self.play(*[ReplacementTransform(fr[k], hundred[k]) for k in order], run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """An autosomal gene would give the same F1 in both crosses; these differ, following the X."""

    def construct(self):
        def pair(reds):
            return VGroup(*[head(r, 1.1) for r in reds]).arrange(RIGHT, buff=0.35)

        def hollow(n):
            hs = [head(True, 1.1) for _ in range(n)]
            for h in hs:
                h[1].set_fill(opacity=0).set_stroke(GREY, 2)
            return VGroup(*hs).arrange(RIGHT, buff=0.35)

        # left panel: autosomal expectation
        ltitle = T("autosomal gene", 30, GREY).move_to([-3.4, 3.3, 0])
        la = VGroup(T("Cross A", 26, GREY), hollow(2)).arrange(RIGHT, buff=0.4)
        lb = VGroup(T("Cross B", 26, GREY), hollow(2)).arrange(RIGHT, buff=0.4)
        lcol = VGroup(la, lb).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([-3.4, 1.45, 0])
        leq = T("same", 30, GREY, weight=BOLD)
        leq.next_to(lcol, DOWN, buff=0.25)
        # right panel: what the crosses gave
        rtitle = T("the white gene", 30, TEXT).move_to([3.4, 3.3, 0])
        ra = VGroup(T("Cross A", 26, GREY), pair([True, True])).arrange(RIGHT, buff=0.4)
        rb = VGroup(T("Cross B", 26, GREY), pair([True, False])).arrange(RIGHT, buff=0.4)
        rcol = VGroup(ra, rb).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.4, 1.45, 0])
        req = T("different", 30, YELLOW, weight=BOLD)
        req.next_to(rcol, DOWN, buff=0.25)
        def tags(col):
            heads = col[0][1]
            out = []
            for h, w in zip(heads, ("daughter", "son")):
                out.append(T(w, 22, GREY).next_to(h, UP, buff=0.08))
            return VGroup(*out)
        ltags, rtags = tags(lcol), tags(rcol)
        # bottom: the X
        mx = chrom("X", 1.8).move_to([-3.2, -1.9, 0])
        mband = band_at(mx, 0.35, TEXT)
        mlab = T("mother's X", 26, GREY).next_to(mx, LEFT, buff=0.25)
        sonhead = head(False, 1.2)
        sx = chrom("X", 1.8)
        sx.next_to(sonhead, RIGHT, buff=0.3)
        sband = band_at(sx, 0.35, TEXT)
        son = VGroup(sonhead, sx, sband).move_to([3.2, -1.9, 0])
        slab = T("son", 26, GREY).next_to(son, UP, buff=0.15)
        arrow = aline([-2.7, -1.9, 0], [1.9, -1.9, 0], YELLOW)
        onx = T("the gene is on the X", 30, YELLOW, weight=BOLD).move_to([-0.4, -1.3, 0])
        note1 = T("Mendel's segregation still holds", 26, GREY).move_to([0, -3.3, 0])
        note2 = T("Real broods are noisier than these expectations", 26, GREY).move_to([0, -3.3, 0])

        self.at("autosomal gene")
        self.play(FadeIn(ltitle), FadeIn(lcol), FadeIn(ltags), run_time=0.6)
        self.at("same first generation")
        self.play(FadeIn(leq, shift=UP * 0.1), run_time=0.5)
        self.at("these crosses differ")
        self.play(FadeIn(rtitle), FadeIn(rcol), FadeIn(rtags), run_time=0.6)
        self.play(FadeIn(req, shift=UP * 0.1), run_time=0.5)
        self.at("follows the X")
        self.play(FadeIn(mx), Create(mband), FadeIn(mlab), run_time=0.6)
        self.at("sons always take")
        self.play(FadeIn(son), FadeIn(slab), GrowArrow(arrow), run_time=0.9)
        self.at("so the gene")
        self.play(FadeIn(onx, scale=1.1), Indicate(mband, color=YELLOW, scale_factor=1.5), run_time=0.8)
        self.at("segregation still")
        self.play(FadeIn(note1, shift=UP * 0.1), run_time=0.5)
        self.at("real broods")
        self.play(ReplacementTransform(note1, note2), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S07End(EndCard):
    LINE = "Sons take the mother's allele, so the gene is on the X."
