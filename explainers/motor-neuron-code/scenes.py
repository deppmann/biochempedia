"""A motor neuron is a combination  (Developmental Neuroscience explainer, motor-neuron-code)

COLOR MAP (one colour per concept, whole film)
  BLUE   = Lhx3
  YELLOW = Isl1
  PURPLE = NLI (the cofactor)
  ORANGE = V2 interneuron and its genes
  GREEN  = motor neuron and its genes
  PINK   = Mnx1
  TEAL   = Sonic hedgehog
  RED    = absent / deleted / crossed out
  GREY   = cells, tissue, structure, labels
  WHITE  = rings that point at the shared binding site
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58AB5"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def cross(center, w=1.0, h=0.7, color=RED, sw=7):
    c = np.array(center, float)
    return VGroup(Line(c + [-w / 2, h / 2, 0], c + [w / 2, -h / 2, 0], color=color, stroke_width=sw),
                  Line(c + [-w / 2, -h / 2, 0], c + [w / 2, h / 2, 0], color=color, stroke_width=sw))


R0 = 1.5


def lhx(c, k=1.0):
    """Lhx3 drawn as a cup: a round body with a round socket bitten out of its right side."""
    R = R0 * k
    cx, cy = c[0], c[1]
    circ = Circle(radius=R).move_to([cx, cy, 0])
    cut = Circle(radius=0.44 * k).move_to([cx + 0.95 * R, cy, 0])
    body = Difference(circ, cut, stroke_color=BLUE, stroke_width=4, fill_color=BLUE, fill_opacity=0.3)
    lab = T("Lhx3", int(round(34 * k)), BLUE, weight=BOLD).move_to([cx - 0.2 * R, cy, 0])
    return VGroup(body, lab)


def notch(c, k=1.0):
    return np.array([c[0] + 0.95 * R0 * k, c[1], 0])


def nli(peg, k=1.0, color=PURPLE):
    """NLI: a block with a round peg that fits the socket."""
    p = Circle(radius=0.40 * k, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5).move_to([peg[0], peg[1], 0])
    b = RoundedRectangle(corner_radius=0.16, width=1.5 * k, height=1.1 * k, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.3).move_to([peg[0] + 1.15 * k, peg[1], 0])
    lab = T("NLI", int(round(32 * k)), color, weight=BOLD).move_to(b)
    return VGroup(p, b, lab)


def isl(peg, k=1.0, color=YELLOW):
    """Isl1: a block with a long tail that ends in the same kind of peg."""
    p = Circle(radius=0.40 * k, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5).move_to([peg[0], peg[1], 0])
    tail = Line([peg[0] + 0.4 * k, peg[1], 0], [peg[0] + 2.0 * k, peg[1], 0], color=color, stroke_width=7)
    b = RoundedRectangle(corner_radius=0.2, width=2.0 * k, height=1.2 * k, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.3).move_to([peg[0] + 3.0 * k, peg[1], 0])
    lab = T("Isl1", int(round(34 * k)), color, weight=BOLD).move_to(b)
    return VGroup(p, tail, b, lab)


def nli_down(peg, k=1.0, color=PURPLE):
    """NLI bound beneath Isl1: the same peg and block, the block hanging below the peg."""
    p = Circle(radius=0.40 * k, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.5).move_to([peg[0], peg[1], 0])
    b = RoundedRectangle(corner_radius=0.16, width=1.5 * k, height=1.1 * k, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.3).move_to([peg[0], peg[1] - 0.95 * k, 0])
    lab = T("NLI", int(round(32 * k)), color, weight=BOLD).move_to(b)
    return VGroup(p, b, lab)


def isl_dock(s, k=1.0):
    """Where NLI binds on Isl1: under the middle of the Isl1 block."""
    blk = s[2]
    return np.array([blk.get_center()[0], blk.get_bottom()[1] - 0.25 * k, 0])


def ghost_isl(center, k=1.0):
    box = RoundedRectangle(corner_radius=0.2, width=2.0 * k, height=1.2 * k).move_to(center)
    d = DashedVMobject(box, num_dashes=26).set_stroke(RED, 4, opacity=0.9)
    lab = T("no Isl1", int(round(30 * k)), RED, weight=BOLD).move_to(box)
    return VGroup(d, lab)


def tag(text, pos):
    return T(text, 24, GREY).move_to(pos)


class S00Title(TitleCard):
    LESSON = "Transcription Factor Codes: Building a Motor Neuron"
    TITLE = "A Motor Neuron Is a Combination"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        # tube in cross section: seven stacked stripes, dorsal at the top
        W, H, N = 3.0, 6.2, 7
        tc = np.array([0.4, 0.0, 0])
        bands = VGroup(*[Rectangle(width=W, height=H / N, stroke_color=GREY, stroke_width=2,
                                   fill_color=GREY, fill_opacity=0.10 + 0.08 * (i % 2)) for i in range(N)])
        bands.arrange(DOWN, buff=0).move_to(tc)
        pmn = bands[5]  # a stripe in the lower half (ventral)
        # gradient bar left of the tube, strongest at the bottom
        steps = 16
        bar = VGroup(*[Rectangle(width=0.45, height=H / steps, stroke_width=0, fill_color=TEAL,
                                 fill_opacity=0.06 + 0.85 * (i / (steps - 1)) ** 1.5) for i in range(steps)])
        bar.arrange(DOWN, buff=0).move_to([tc[0] - 2.5, 0, 0])
        shh = T("Sonic hedgehog", 26, TEAL).rotate(PI / 2).move_to([tc[0] - 3.2, 0, 0])

        self.at("Sonic hedgehog")
        self.play(FadeIn(bar), FadeIn(shh), run_time=0.8)
        self.at("read their position")
        self.play(LaggedStart(*[FadeIn(b) for b in bands], lag_ratio=0.12), run_time=1.3)
        self.at("one stripe")
        lab = T("pMN", 34, GREEN, weight=BOLD).move_to([tc[0] + W / 2 + 0.9, pmn.get_center()[1], 0])
        self.play(pmn.animate.set_fill(GREEN, 0.5).set_stroke(GREEN, 4), FadeIn(lab, shift=LEFT * 0.2), run_time=0.7)
        self.at("makes motor neurons")
        self.play(Indicate(pmn, color=GREEN, scale_factor=1.06), run_time=0.8)

        # the stripe becomes one cell
        cell_c = np.array([-3.2, 0.0, 0])
        cell = Circle(radius=2.5, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(cell_c)
        self.at("does not contain")
        others = [m for m in bands if m is not pmn]
        self.play(FadeOut(VGroup(*others)), FadeOut(bar), FadeOut(shh), FadeOut(lab), ReplacementTransform(pmn, cell), run_time=1.0)
        q = RoundedRectangle(corner_radius=0.16, width=5.4, height=0.95, stroke_color=GREEN, stroke_width=3,
                             fill_color=GREEN, fill_opacity=0.1).move_to([3.6, 2.5, 0])
        ql = T("a gene for motor neuron?", 28, GREEN).move_to(q)
        self.play(FadeIn(q), FadeIn(ql), run_time=0.5)
        x = cross([q.get_left()[0] - 0.55, q.get_center()[1], 0], 0.6, 0.6)
        self.play(Create(x), ql.animate.set_opacity(0.5), q.animate.set_stroke(opacity=0.5), run_time=0.5)

        self.at("transcription factors")
        pos = [(-0.95, 0.65), (0.95, 0.65), (-0.95, -0.65), (0.95, -0.65)]
        chips = VGroup(*[chip("factor", GREY, size=28).move_to([cell_c[0] + dx, cell_c[1] + dy, 0]) for dx, dy in pos])
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in chips], lag_ratio=0.25), run_time=1.4)
        self.at("that particular set")
        a = arr([cell_c[0] + 2.55, 0, 0], [1.6, -0.9, 0], GREEN)
        mn = T("motor neuron", 38, GREEN, weight=BOLD).move_to([4.0, -0.9, 0])
        self.play(GrowArrow(a), Indicate(chips, color=GREEN, scale_factor=1.05), run_time=0.8)
        self.play(FadeIn(mn, shift=RIGHT * 0.2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Markers(SpokenScene):
    def construct(self):
        lc = np.array([-3.5, 0.3, 0])
        rc = np.array([3.5, 0.3, 0])
        cell_l = Circle(radius=2.3, stroke_color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.12).move_to(lc)
        lab_l = T("progenitor", 30, GREY).move_to([lc[0], -2.55, 0])
        self.play(FadeIn(cell_l), FadeIn(lab_l), run_time=0.7)
        self.at("final division")
        self.play(Indicate(cell_l, color=GREY, scale_factor=1.06), run_time=0.8)
        self.at("new set")
        lab_l2 = T("motor neuron", 30, GREEN, weight=BOLD).move_to(lab_l)
        self.play(cell_l.animate.set_stroke(GREEN).set_fill(GREEN, 0.12), ReplacementTransform(lab_l, lab_l2), run_time=0.6)
        c_isl = chip("Isl1", YELLOW, 30).move_to(lc + [-0.55, 0.95, 0])
        c_lhx = chip("Lhx3", BLUE, 30).move_to(lc)
        c_mnx = chip("Mnx1", PINK, 30).move_to(lc + [0, -0.95, 0])
        self.at("These are")
        self.play(FadeIn(c_isl, scale=0.8), run_time=0.6)
        self.at("or its relative")
        orl = T("or Isl2", 26, YELLOW).next_to(c_isl, RIGHT, buff=0.22)
        self.play(FadeIn(orl, shift=LEFT * 0.15), run_time=0.5)
        self.wait(2.4)   # Lhx3 is named about three seconds after "or its relative"
        self.play(FadeIn(c_lhx, scale=0.8), run_time=0.5)
        self.wait(1.0)   # then Mnx1
        self.play(FadeIn(c_mnx, scale=0.8), run_time=0.5)
        self.at("stain for")
        # stained nuclei: each marker lights up in its own colour, as in a section
        glows = VGroup(*[SurroundingRectangle(c, color=col, buff=0.1, corner_radius=0.12, stroke_width=5)
                         for c, col in ((c_isl, YELLOW), (c_lhx, BLUE), (c_mnx, PINK))])
        stain = T("markers you stain for", 26, GREY).move_to([lc[0], 2.95, 0])
        self.play(LaggedStart(*[Create(g) for g in glows], lag_ratio=0.3), FadeIn(stain), run_time=1.2)
        self.at("also made")
        self.play(FadeOut(glows[0]), FadeOut(glows[2]), Indicate(c_lhx, color=BLUE, scale_factor=1.2), run_time=0.9)
        self.at("of the motor neuron")
        cell_r = Circle(radius=2.3, stroke_color=ORANGE, stroke_width=4, fill_color=ORANGE, fill_opacity=0.12).move_to(rc)
        lab_r = T("V2 interneuron", 30, ORANGE, weight=BOLD).move_to([rc[0], -2.55, 0])
        c_lhx2 = chip("Lhx3", BLUE, 30).move_to(rc)
        g2 = SurroundingRectangle(c_lhx2, color=BLUE, buff=0.1, corner_radius=0.12, stroke_width=5)
        self.play(FadeIn(cell_r), FadeIn(lab_r), TransformFromCopy(c_lhx, c_lhx2), TransformFromCopy(glows[1], g2), run_time=1.3)
        self.at("One protein sits")
        self.play(Indicate(VGroup(c_lhx, glows[1]), color=BLUE, scale_factor=1.2),
                  Indicate(VGroup(c_lhx2, g2), color=BLUE, scale_factor=1.2), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
LC = np.array([-4.2, 0.6, 0])
KK = 1.2
OUT_X = -2.8
OUT_Y = -2.8
ARR_X = -4.0


class S03Nli(SpokenScene):
    def construct(self):
        sp = tag("chick neural tube", [-4.8, 3.2, 0])
        cup = lhx(LC, KK)
        self.at("experiment")
        self.play(FadeIn(sp), GrowFromCenter(cup), run_time=0.9)
        ghost = ghost_isl([5.0, LC[1], 0], KK)
        self.at("have no")
        self.play(FadeIn(ghost), run_time=0.6)
        v2 = chip("V2 interneuron genes", ORANGE, 30).move_to([OUT_X, OUT_Y, 0])
        a = arr([ARR_X, LC[1] - 1.9, 0], [ARR_X, OUT_Y + 0.55, 0], ORANGE)
        self.at("You get")
        self.play(GrowArrow(a), FadeIn(v2, shift=DOWN * 0.2), run_time=0.8)
        n = nli([1.4, LC[1], 0], KK)
        self.at("binds")
        self.play(FadeIn(n, shift=LEFT * 0.3), run_time=0.4)
        self.play(n.animate.shift(notch(LC, KK) - n[0].get_center()), run_time=1.0)
        self.at("That complex")
        self.play(Indicate(VGroup(cup, n), color=ORANGE, scale_factor=1.04), a.animate.set_stroke(width=8), run_time=1.0)
        self.finish()


class S04Isl1(SpokenScene):
    def construct(self):
        sp = tag("chick neural tube", [-4.8, 3.2, 0])
        cup = lhx(LC, KK)
        n = nli(notch(LC, KK), KK)
        ghost = ghost_isl([5.0, LC[1], 0], KK)
        v2 = chip("V2 interneuron genes", ORANGE, 30).move_to([OUT_X, OUT_Y, 0])
        a = arr([ARR_X, LC[1] - 1.9, 0], [ARR_X, OUT_Y + 0.55, 0], ORANGE)
        self.add(sp, cup, n, ghost, v2, a)
        s = isl([1.4, LC[1], 0], KK)
        self.at("Add")
        # old answer cleared in the same beat the new partner arrives
        self.play(FadeOut(v2), FadeOut(a), FadeOut(ghost), FadeIn(s), run_time=0.7)
        self.at("competes")
        self.play(s.animate.shift(LEFT * 1.1), run_time=0.9)
        # Isl1 takes NLI: NLI leaves the Lhx3 socket and binds beneath Isl1, where it stays
        n_on = nli_down(isl_dock(s, KK), KK)
        self.play(Transform(n, n_on), run_time=1.2)
        self.at("displaces")
        # Isl1, holding NLI, plugs its tail into the Lhx3 socket
        d = notch(LC, KK) - s[0].get_center()
        self.play(VGroup(s, n).animate.shift(d), run_time=1.2)
        self.at("C terminal")
        ct = T("C-terminal region", 24, YELLOW).move_to([-1.2, LC[1] - 1.15, 0])
        self.play(FadeIn(ct, shift=UP * 0.1), Indicate(s[1], color=YELLOW, scale_factor=1.0), run_time=0.8)
        self.at("complex that forms")
        self.play(Indicate(VGroup(cup, s, n), color=GREEN, scale_factor=1.04), run_time=0.9)
        mn = chip("motor neuron genes", GREEN, 30).move_to([OUT_X, OUT_Y, 0])
        a2 = arr([ARR_X, LC[1] - 1.9, 0], [ARR_X, OUT_Y + 0.55, 0], GREEN)
        self.at("promotes")
        self.play(GrowArrow(a2), FadeIn(mn, shift=DOWN * 0.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Surface(SpokenScene):
    def construct(self):
        k = 0.78
        c1 = np.array([-5.0, 0.7, 0])   # V2 panel
        c2 = np.array([1.3, 0.7, 0])    # motor-neuron panel
        cup1, n1 = lhx(c1, k), nli(notch(c1, k), k)
        cup2, s2 = lhx(c2, k), isl(notch(c2, k), k)
        n2 = nli_down(isl_dock(s2, k), k)   # NLI stays bound, now to Isl1
        ox1, ox2, oy = -3.9, 2.9, -2.4
        v2 = chip("V2 interneuron genes", ORANGE, 26).move_to([ox1, oy, 0])
        mn = chip("motor neuron genes", GREEN, 26).move_to([ox2, oy, 0])
        a1 = arr([c1[0], c1[1] - 1.3, 0], [c1[0], oy + 0.5, 0], ORANGE)
        a2 = arr([c2[0], c2[1] - 1.3, 0], [c2[0], oy + 0.5, 0], GREEN)
        right = VGroup(cup2, s2, n2, a2, mn)
        left = VGroup(cup1, n1, a1, v2)
        self.add(right)
        self.at("not reading")
        self.play(Indicate(right, color=GREEN, scale_factor=1.02), run_time=0.8)
        self.at("wins a competition")
        self.play(FadeIn(left, shift=RIGHT * 0.3), run_time=0.9)
        self.at("shared partner")
        self.play(Indicate(n1, color=PURPLE, scale_factor=1.15), Indicate(n2, color=PURPLE, scale_factor=1.15), run_time=1.0)
        self.at("one binding site")
        r1 = Circle(radius=0.44 * k + 0.1, stroke_color=TEXT, stroke_width=4).move_to(notch(c1, k))
        r2 = Circle(radius=0.44 * k + 0.1, stroke_color=TEXT, stroke_width=4).move_to(notch(c2, k))
        lab = T("one binding site", 28, TEXT).move_to([-1.5, 3.2, 0])
        self.play(Create(r1), Create(r2), FadeIn(lab), run_time=0.8)
        self.at("same surface")
        lab2 = T("the same surface of Lhx3", 28, BLUE).move_to([-1.5, 3.2, 0])
        self.play(ReplacementTransform(lab, lab2), Indicate(r1, color=TEXT, scale_factor=1.25),
                  Indicate(r2, color=TEXT, scale_factor=1.25), run_time=1.0)
        h1 = T("holds NLI", 26, PURPLE).move_to([-4.6, 2.3, 0])
        h2 = T("holds a segment of Isl1", 26, YELLOW).move_to([2.6, 2.3, 0])
        self.at("It holds")
        self.play(Indicate(n1, color=PURPLE, scale_factor=1.15), FadeIn(h1, shift=DOWN * 0.1), run_time=0.9)
        self.at("In the other")
        self.play(Indicate(s2[0:2], color=YELLOW, scale_factor=1.1), Indicate(r2, color=TEXT, scale_factor=1.25), run_time=0.9)
        self.at("a segment of")
        self.play(FadeIn(h2, shift=DOWN * 0.1), s2[1].animate.set_stroke(width=11), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Tests(SpokenScene):
    def construct(self):
        y1, y2 = 1.5, -1.5
        t1 = T("chick", 30, GREY, weight=BOLD).move_to([-5.6, y1, 0])
        t2 = T("mouse", 30, GREY, weight=BOLD).move_to([-5.6, y2, 0])
        slots = []
        for y in (y1, y2):
            box = RoundedRectangle(corner_radius=0.16, width=4.4, height=0.9)
            d = DashedVMobject(box, num_dashes=24).set_stroke(GREY, 3).move_to([3.9, y, 0])
            q = T("?", 34, GREY).move_to([3.9, y, 0])
            slots.append(VGroup(d, q))
        self.at("Two tests")
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(slots[0]), FadeIn(slots[1]), run_time=0.8)

        i1 = chip("Isl1", YELLOW, 30).move_to([-3.6, y1, 0])
        plus = T("+", 36, TEXT).move_to([-2.45, y1, 0])
        l1 = chip("Lhx3", BLUE, 30).move_to([-1.3, y1, 0])
        ar1 = arr([-0.3, y1, 0], [1.5, y1, 0], GREEN)
        r1 = chip("motor neuron genes", GREEN, 30).move_to([3.9, y1, 0])
        self.at("chick cell")
        self.play(FadeIn(i1, shift=RIGHT * 0.2), FadeIn(plus), FadeIn(l1, shift=LEFT * 0.2), run_time=0.8)
        self.at("come up")
        self.play(GrowArrow(ar1), FadeOut(slots[0]), FadeIn(r1), run_time=0.8)

        i2 = chip("no Isl1", RED, 30).move_to([-3.4, y2, 0])
        x2 = VGroup()
        ar2 = arr([-0.3, y2, 0], [1.5, y2, 0], RED)
        r2 = chip("no motor neurons", RED, 30).move_to([3.9, y2, 0])
        self.at("in the mouse")
        self.play(FadeIn(i2), run_time=0.4)
        self.at("not generated")
        self.play(GrowArrow(ar2), FadeOut(slots[1]), FadeIn(r2), run_time=0.8)

        c1 = T("adding: what it can impose", 26, GREY).move_to([0.2, y1 - 1.0, 0])
        c2 = T("deleting: what cannot be built without it", 26, GREY).move_to([0.2, y2 - 1.0, 0])
        self.at("Adding a factor")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.at("Deleting it")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)

        self.at("Keep this rule")
        rows = VGroup(t1, t2, i1, plus, l1, ar1, r1, i2, ar2, r2, c1, c2)
        self.play(FadeOut(rows), run_time=0.8)
        rl0 = T("a motor neuron is spelled by", 34, GREEN).move_to([0, 1.7, 0])
        rl1 = T("a combination of factors", 46, TEXT, font=TITLE_FONT).move_to([0, 0.5, 0])
        self.at("combination of factors")
        self.play(FadeIn(rl0, shift=UP * 0.15), FadeIn(rl1, shift=UP * 0.15), run_time=0.7)
        rl2 = T("not one master gene", 46, GREY, font=TITLE_FONT).move_to([0, -0.8, 0])
        self.at("one master gene")
        self.play(FadeIn(rl2, shift=UP * 0.15), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "A motor neuron is spelled by a combination, not one master gene."
