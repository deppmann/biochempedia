"""Radial glia: the cell stays, the nucleus travels  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = the radial glial / neuroepithelial cell (body and fiber)
  YELLOW = the nucleus (the thing that moves)
  TEAL   = cell-cycle phase (ring, G1 / S / G2 / M, "copying DNA")
  GREEN  = a neuron
  PURPLE = kinesin Kif1a (basal motor)
  ORANGE = dynein (apical motor)
  PINK   = actomyosin (zebrafish retina)
  RED    = the open question
  GREY   = ventricle, pia, labels, historical reading, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
PINK = "#E58FB4"

CX = -1.8          # x of the single cell in scenes 3 to 6
BIGW = 2.4         # width of the single (zoomed) cell
NR = 0.70          # radius of the single cell's nucleus
Y_AP = -2.1        # nucleus at the apical end
Y_BA = 1.85        # nucleus in the basal ventricular zone (S phase)
RIGHT_OF_CELL = CX + BIGW / 2 + 0.5   # left edge for labels beside the cell
COLS = [-3.0, -1.8, -0.6, 0.6, 1.8, 3.0]


# ---------------------------------------------------------------- helpers
def wall():
    strip = Rectangle(width=9.6, height=0.44, stroke_width=0, fill_color=GREY, fill_opacity=0.28).move_to([0, -3.22, 0])
    vlab = T("ventricle", 22, GREY).move_to(strip)
    pia = Rectangle(width=9.6, height=0.16, stroke_width=0, fill_color=GREY, fill_opacity=0.6).move_to([0, 3.16, 0])
    plab = T("pia", 24, GREY).move_to([5.5, 3.16, 0])
    return VGroup(strip, vlab, pia, plab)


def side_labels():
    a = T("apical", 26, GREY).move_to([-5.3, -2.5, 0])
    b = T("basal", 26, GREY).move_to([-5.3, 2.5, 0])
    return VGroup(a, b)


def cell(x, color=BLUE, width=1.0):
    c = RoundedRectangle(corner_radius=0.4, width=width, height=5.8, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.13).move_to([x, 0, 0])
    c.set_z_index(0)
    return c


def nuc(x, y, r=0.34):
    n = Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85).move_to([x, y, 0])
    n.set_z_index(3)
    return n


def dumb(x, y, r=0.18, dx=0.22):
    g = VGroup(*[Circle(radius=r, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.85)
                 .move_to([x + d, y, 0]) for d in (-dx, dx)])
    g.set_z_index(3)
    return g


def ring_of(x, y, r=0.34):
    c = Circle(radius=r + 0.09, stroke_color=TEAL, stroke_width=4).move_to([x, y, 0])
    c.set_z_index(4)
    return c


def bigcell():
    return cell(CX, width=BIGW)


def bignuc(y):
    return nuc(CX, y, NR)


def bigdumb(y):
    return dumb(CX, y, r=0.38, dx=0.44)


def beside(mob, y):
    """Place mob with its left edge just right of the big cell."""
    return mob.move_to([RIGHT_OF_CELL + mob.width / 2, y, 0])


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


RING_C = np.array([4.1, 0.2, 0])
RING_R = 1.3
# (name, start deg, span deg clockwise)
PHASES = [("G1", 60, -120), ("S", -60, -110), ("G2", -170, -100), ("M", 90, -30)]


def ring_arcs():
    arcs = {}
    for name, a0, span in PHASES:
        arcs[name] = Arc(radius=RING_R, start_angle=np.deg2rad(a0), angle=np.deg2rad(span), arc_center=RING_C,
                         stroke_color=TEAL, stroke_width=9).set_stroke(opacity=0.35)
    return arcs


def ring_labels():
    out = {}
    for name, a0, span in PHASES:
        mid = np.deg2rad(a0 + span / 2)
        p = RING_C + (RING_R + 0.6) * np.array([np.cos(mid), np.sin(mid), 0])
        out[name] = T(name, 28, TEAL, weight=BOLD).move_to(p)
    return out


def pt_on_ring(deg):
    return RING_C + RING_R * np.array([np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg)), 0])


class S00Title(TitleCard):
    LESSON = "The ventricular zone: radial glia as stem cells"
    TITLE = "The cell stays, the nucleus travels"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    def construct(self):
        w = wall()
        self.at("Slice an embryonic mouse cortex")
        tag = T("embryonic mouse cortex", 24, GREY).move_to([-3.9, 0.3, 0])
        self.play(FadeIn(w), FadeIn(tag), run_time=0.8)

        div = [dumb(COLS[i], Y_AP) for i in (0, 3, 5)]
        cop = [nuc(COLS[1], 1.2), nuc(COLS[2], 2.0), nuc(COLS[4], 1.6)]
        rings = [ring_of(n.get_center()[0], n.get_center()[1]) for n in cop]

        self.at("caught in mitosis")
        self.play(*[FadeIn(d, scale=0.6) for d in div], run_time=0.6)
        lab_m = T("in mitosis", 26, TEAL).move_to([5.2, -2.5, 0])
        am = arr([4.2, -2.5, 0], [3.55, -2.5, 0], TEAL)
        self.play(FadeIn(lab_m), GrowArrow(am), run_time=0.6)
        self.at("against the ventricle")
        self.play(Indicate(w[0], color=TEAL, scale_factor=1.0), run_time=1.0)
        self.at("copying their DNA")
        self.play(*[FadeIn(n, scale=0.6) for n in cop], *[Create(r) for r in rings], run_time=0.8)
        lab_c = T("copying DNA", 26, TEAL).move_to([5.2, 1.6, 0])
        ac = arr([4.05, 1.6, 0], [2.5, 1.6, 0], TEAL)
        self.play(FadeIn(lab_c), GrowArrow(ac), run_time=0.6)
        self.at("farther out")
        self.play(*[Indicate(VGroup(n, r), color=YELLOW, scale_factor=1.1) for n, r in zip(cop, rings)], run_time=0.9)
        self.at("Why would a cell")
        q = T("?", 120, RED, weight=BOLD).move_to([-4.6, -0.6, 0])
        self.play(FadeOut(tag), FadeIn(q, scale=0.5), run_time=0.7)
        self.play(Indicate(q, color=RED, scale_factor=1.15), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Cells(SpokenScene):
    def construct(self):
        w = wall()
        div = [dumb(COLS[i], Y_AP) for i in (0, 3, 5)]
        cop = [nuc(COLS[1], 1.2), nuc(COLS[2], 2.0), nuc(COLS[4], 1.6)]
        rings = [ring_of(m.get_center()[0], m.get_center()[1]) for m in cop]
        lab_m = T("in mitosis", 26, TEAL).move_to([5.2, -2.5, 0])
        am = arr([4.2, -2.5, 0], [3.55, -2.5, 0], TEAL)
        lab_c = T("copying DNA", 26, TEAL).move_to([5.2, 1.6, 0])
        ac = arr([4.05, 1.6, 0], [2.5, 1.6, 0], TEAL)
        q = T("?", 120, RED, weight=BOLD).move_to([-4.6, -0.6, 0])
        old = VGroup(lab_m, am, lab_c, ac, q, *rings)
        self.add(w, *div, *cop, old)
        # nuclei at many heights
        n = [nuc(x, y) for x, y in zip(COLS, [-1.0, 1.2, 2.0, -0.2, 1.6, -2.5])]
        self.at("looks layered")
        self.play(FadeOut(old),
                  ReplacementTransform(div[0], n[0]), ReplacementTransform(div[1], n[3]),
                  ReplacementTransform(div[2], n[5]),
                  ReplacementTransform(cop[0], n[1]), ReplacementTransform(cop[1], n[2]),
                  ReplacementTransform(cop[2], n[4]), run_time=1.4)
        lay = T("looks layered", 28, GREY).move_to([5.0, 0.6, 0])
        self.play(FadeIn(lay), run_time=0.5)
        self.at("several kinds of cells")
        kinds = VGroup(T("several kinds", 28, RED), T("of cells?", 28, RED)).arrange(DOWN, buff=0.12).move_to([5.0, -0.6, 0])
        self.play(FadeIn(kinds), run_time=0.6)
        self.at("something simpler")
        cells = [cell(x) for x in COLS]
        sauer = T("Sauer, 1935", 26, GREY).move_to([5.0, 2.2, 0])
        self.play(FadeOut(lay), FadeOut(kinds), FadeIn(sauer),
                  LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=0.15), run_time=1.8)
        self.at("long and thin")
        self.play(Indicate(cells[3], color=BLUE, scale_factor=1.04), run_time=1.0)
        self.at("apical surface")
        sl = side_labels()
        self.play(FadeIn(sl[0]), Indicate(w[0], color=GREY, scale_factor=1.0), run_time=0.8)
        self.at("basal surface")
        self.play(FadeIn(sl[1]), Indicate(w[2], color=GREY, scale_factor=1.0), run_time=0.8)
        self.at("Only the nucleus moves")
        self.play(*[nn.animate.set_y(y) for nn, y in zip(n, [1.8, -1.8, -0.6, 1.2, -1.2, 0.6])], run_time=1.6)
        self.play(*[nn.animate.set_y(y) for nn, y in zip(n, [-0.2, 0.4, 1.6, -1.4, 0.4, -2.0])], run_time=1.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Lift(SpokenScene):
    def construct(self):
        w = wall()
        sl = side_labels()
        cells = [cell(x) for x in COLS]
        ys = [-0.2, 0.4, 1.6, -1.4, 0.4, -2.0]
        n = [nuc(x, y) for x, y in zip(COLS, ys)]
        self.add(w, sl, *cells, *n)
        # keep the middle cell; slide it to the left stage
        c = cells[2]
        main = n[2]
        others = VGroup(*[cells[i] for i in (0, 1, 3, 4, 5)], *[n[i] for i in (0, 1, 3, 4, 5)])
        self.at("Picture a lift")
        big_c, big_n = bigcell(), bignuc(Y_AP)
        self.play(FadeOut(others), ReplacementTransform(c, big_c), ReplacementTransform(main, big_n), run_time=0.8)
        c, main = big_c, big_n
        shaft = beside(T("the cell: a fixed shaft", 28, BLUE), 1.6)
        car = beside(T("the nucleus: the car", 28, YELLOW), 0.7)
        self.at("The shaft is the cell")
        self.play(FadeIn(shaft, shift=RIGHT * 0.2), run_time=0.6)
        self.at("The car is the nucleus")
        self.play(FadeIn(car, shift=RIGHT * 0.2), run_time=0.6)
        self.play(main.animate.set_y(0.0), run_time=0.8)
        self.play(main.animate.set_y(Y_AP), run_time=0.8)

        arcs = ring_arcs()
        labs = ring_labels()
        mid = T("cell cycle", 24, GREY).move_to(RING_C)
        marker = Dot(pt_on_ring(60), radius=0.14, color=YELLOW).set_z_index(5)
        self.at("timetable")
        self.play(FadeOut(shaft), FadeOut(car), run_time=0.4)
        self.play(*[Create(a) for a in arcs.values()],
                  *[FadeIn(l) for l in labs.values()], FadeIn(mid), FadeIn(marker), run_time=1.0)

        def go(name, **kw):
            return MoveAlongPath(marker, arcs[name], **kw)

        def lit(name):
            return [arcs[k].animate.set_stroke(opacity=1.0 if k == name else 0.35) for k in arcs]

        self.at("moves basally")
        self.play(go("G1"), main.animate.move_to([CX, Y_BA - 1.0, 0]), *lit("G1"), run_time=1.1, rate_func=linear)
        self.at("S phase")
        copy_ring = ring_of(CX, Y_BA, NR)
        self.play(go("S"), main.animate.move_to([CX, Y_BA, 0]), *lit("S"), Create(copy_ring), run_time=0.9, rate_func=linear)
        dna = beside(T("copying DNA", 26, TEAL), Y_BA)
        self.at("DNA is copied")
        self.play(FadeIn(dna, shift=LEFT * 0.2), run_time=0.5)
        self.at("basal part")
        self.play(Indicate(dna, color=TEAL, scale_factor=1.1), run_time=0.8)
        self.at("back to the apical")
        self.play(go("G2"), main.animate.move_to([CX, Y_AP, 0]), *lit("G2"), FadeOut(copy_ring), FadeOut(dna),
                  run_time=1.7, rate_func=linear)
        self.at("Mitosis happens")
        d = bigdumb(Y_AP)
        self.play(go("M"), *lit("M"), ReplacementTransform(main, d), run_time=0.9, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Motors(SpokenScene):
    def construct(self):
        w = wall()
        sl = side_labels()
        c = bigcell()
        main = bignuc(Y_AP)
        self.add(w, sl, c, main)
        self.at("has motors")
        # motor tag ride-along
        kin = beside(bchip("kinesin Kif1a", PURPLE, 26), Y_AP)
        g1 = T("G1", 28, TEAL, weight=BOLD).next_to(kin, UP, buff=0.12)
        rat = T("embryonic rat cortex", 24, GREY).move_to([4.1, 2.6, 0])
        self.at("In embryonic rat cortex")
        self.play(FadeIn(rat), run_time=0.5)
        self.at("carries the nucleus basally")
        self.play(FadeIn(kin, shift=LEFT * 0.2), run_time=0.5)
        self.play(FadeIn(g1), run_time=0.3)
        kg = VGroup(kin, g1)
        self.play(kg.animate.shift(UP * (Y_BA - Y_AP)), main.animate.move_to([CX, Y_BA, 0]), run_time=2.0)
        self.at("Cytoplasmic dynein")
        dyn = beside(bchip("dynein", ORANGE, 26), Y_BA)
        g2 = T("G2", 28, TEAL, weight=BOLD).next_to(dyn, UP, buff=0.12)
        self.play(FadeOut(kg), FadeIn(dyn, shift=RIGHT * 0.2), FadeIn(g2), run_time=0.6)
        self.at("pulls it apically")
        dg = VGroup(dyn, g2)
        self.play(dg.animate.shift(DOWN * (Y_BA - Y_AP)), main.animate.move_to([CX, Y_AP, 0]), run_time=2.0)
        self.at("measured in rat")
        mr = bchip("measured in rat", GREY, 24).move_to([3.4, 1.7, 0])
        self.play(FadeOut(dg), FadeOut(rat), FadeIn(mr), run_time=0.6)
        self.at("zebrafish retina")
        zf = bchip("zebrafish retina", GREY, 24).move_to([3.4, 0.2, 0])
        self.play(FadeIn(zf), run_time=0.6)
        self.at("depend on")
        am = bchip("apical move: actomyosin", PINK, 24).move_to([3.4, -1.2, 0])
        down = arr([zf.get_bottom()[0], zf.get_bottom()[1] - 0.05, 0], [am.get_top()[0], am.get_top()[1] + 0.05, 0], PINK)
        self.play(GrowArrow(down), FadeIn(am), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Fate(SpokenScene):
    def construct(self):
        w = wall()
        sl = side_labels()
        c = bigcell()
        d = bigdumb(Y_AP)
        self.add(w, sl, c, d)
        q1 = T("?", 72, RED, weight=BOLD).move_to([CX - 1.8, Y_AP + 1.0, 0])
        q2 = T("?", 72, RED, weight=BOLD).move_to([CX + 1.8, Y_AP + 1.0, 0])
        self.at("Where a cell divides")
        self.play(FadeIn(q1, scale=0.5), FadeIn(q2, scale=0.5), run_time=0.7)
        self.at("what its daughters become")
        self.play(Indicate(VGroup(q1, q2), color=RED, scale_factor=1.2), run_time=1.0)

        main = bignuc(Y_AP)
        ne = beside(T("neuroepithelial cell", 28, GREY), 2.3)
        self.at("neuroepithelial cells")
        self.play(FadeOut(q1), FadeOut(q2), ReplacementTransform(d, main), FadeIn(ne), run_time=0.9)
        rg = T("radial glial cell", 28, BLUE).move_to(ne.get_center())
        rg.align_to(ne, LEFT)
        self.at("become radial glia")
        self.play(ReplacementTransform(ne, rg), run_time=0.8)
        self.at("a foot on the ventricle")
        self.play(Indicate(w[0], color=BLUE, scale_factor=1.0), run_time=0.9)
        self.at("long fiber")
        self.play(Indicate(c, color=BLUE, scale_factor=1.03), run_time=0.9)
        self.at("keep the lift")
        self.play(main.animate.set_y(Y_BA - 0.6), run_time=0.6)
        self.play(main.animate.set_y(Y_AP), run_time=0.6)

        # direct neurogenesis equation
        chipA = bchip("radial glial cell", BLUE, 24)
        chipB = bchip("radial glial cell", BLUE, 24)
        chipN = bchip("neuron", GREEN, 24)
        plus = T("+", 30, TEXT)
        row2 = VGroup(chipB, plus, chipN).arrange(RIGHT, buff=0.25).move_to([3.4, -0.5, 0])
        chipA.move_to([3.4, 1.0, 0])
        down = arr([3.4, chipA.get_bottom()[1] - 0.02, 0], [3.4, row2.get_top()[1] + 0.02, 0], GREY)
        self.at("direct neurogenesis")
        self.play(FadeOut(rg), FadeIn(chipA), run_time=0.6)
        self.at("divides into another")
        dd = bigdumb(Y_AP)
        fx = CX + BIGW / 2   # the parent's fiber: the cell's right edge
        neuron = Circle(radius=0.3, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.9).move_to([fx, Y_AP, 0])
        neuron.set_z_index(5)
        keep = bignuc(Y_AP)
        self.play(ReplacementTransform(main, dd), run_time=0.6)
        self.play(ReplacementTransform(dd, keep), FadeIn(neuron, scale=0.4), GrowArrow(down), FadeIn(row2), run_time=1.0)
        self.at("that neuron moved out")
        trail = Line([fx, Y_AP, 0], [fx, Y_AP + 0.01, 0], stroke_color=GREEN, stroke_width=7).set_z_index(4)
        self.add(trail)
        trail.add_updater(lambda m: m.put_start_and_end_on([fx, Y_AP, 0], neuron.get_center() + DOWN * 0.001))
        self.play(neuron.animate.move_to([fx, 1.8, 0]), Indicate(chipN, color=GREEN, scale_factor=1.15), run_time=2.6)
        trail.clear_updaters()
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        w = wall()
        sl = side_labels()
        c = bigcell()
        main = bignuc(Y_AP)
        fx = CX + BIGW / 2
        neuron = Circle(radius=0.3, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.9).move_to([fx, 1.8, 0])
        neuron.set_z_index(5)
        trail = Line([fx, Y_AP, 0], [fx, 1.8, 0], stroke_color=GREEN, stroke_width=7).set_z_index(4)
        self.add(w, sl, c, main, trail, neuron)
        self.at("stays put")
        stay = beside(T("the cell stays put", 28, BLUE), 0.0)
        self.play(Indicate(c, color=BLUE, scale_factor=1.04), FadeIn(stay, shift=RIGHT * 0.2), run_time=1.0)
        self.at("copies DNA")
        ringc = ring_of(CX, Y_BA, NR)
        dna = beside(T("copying DNA", 26, TEAL), Y_BA - 0.5)
        self.play(main.animate.move_to([CX, Y_BA, 0]), neuron.animate.move_to([fx, 2.6, 0]),
                  trail.animate.put_start_and_end_on([fx, Y_AP, 0], [fx, 2.6, 0]), run_time=1.4)
        self.play(Create(ringc), FadeIn(dna), run_time=0.6)
        self.at("rides back")
        self.play(FadeOut(ringc), FadeOut(dna), main.animate.move_to([CX, Y_AP, 0]), run_time=0.9)
        self.at("divides at the ventricle")
        dd = bigdumb(Y_AP)
        self.play(ReplacementTransform(main, dd), run_time=0.6)
        self.play(FadeOut(stay), run_time=0.3)
        self.at("guides migrating neurons")
        g = bchip("guides migrating neurons", GREEN, 26).move_to([3.2, 1.5, 0])
        self.play(FadeIn(g, shift=LEFT * 0.2), Indicate(neuron, color=GREEN, scale_factor=1.3), run_time=0.9)
        self.at("makes most of them")
        m = bchip("makes most of them", GREEN, 26).move_to([3.2, -0.3, 0])
        self.play(FadeIn(m, shift=LEFT * 0.2), Indicate(dd, color=YELLOW, scale_factor=1.3), run_time=0.9)
        self.at("Keep the rule")
        rule = VGroup(T("The cell stays put.", 34, BLUE), T("The nucleus rides the cell cycle.", 34, YELLOW)).arrange(DOWN, buff=0.25).move_to([2.2, -1.9, 0])
        rule.set_x(3.0)
        self.play(FadeIn(rule, shift=UP * 0.2), run_time=1.0)
        self.finish()


class S07End(EndCard):
    LINE = "The cell stays put; its nucleus rides the cell cycle."
