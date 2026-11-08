"""Body water and its compartments: water goes where the solute stays  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = water (water blocks, water dots, "water only" door)
  GREEN  = inside cells (ICF)
  ORANGE = outside cells (ECF)
  YELLOW = effective solute (osmoles, sodium salts, the concentration in mOsm/kg)
  RED    = "none" (nothing enters cells)
  GREY   = membrane, notes, assumptions, things not predicted
  GOLD   = the question marks (puzzle) and the title rule
  Everything is a labelled schematic block: not to scale beyond the 2:1 room widths in the reference man.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
WATER, ICF_C, ECF_C, SOL = BLUE, GREEN, ORANGE, YELLOW


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
class Rooms:
    """Two rooms (inside cells, outside cells) with a membrane that has a door in it."""

    def __init__(self, cy=-0.8, h=4.4, wi=7.2, we=3.6, labels=True):
        self.cy, self.h = cy, h
        x0 = -(wi + we + 0.5) / 2
        self.xi = x0 + wi / 2
        self.mx = x0 + wi + 0.25
        self.xe = x0 + wi + 0.5 + we / 2
        self.icf = RoundedRectangle(corner_radius=0.2, width=wi, height=h, stroke_color=ICF_C, stroke_width=4,
                                    fill_color=ICF_C, fill_opacity=0.10).move_to([self.xi, cy, 0])
        self.ecf = RoundedRectangle(corner_radius=0.2, width=we, height=h, stroke_color=ECF_C, stroke_width=4,
                                    fill_color=ECF_C, fill_opacity=0.10).move_to([self.xe, cy, 0])
        gap = 1.2
        th = h / 2 - gap / 2
        self.mem_top = RoundedRectangle(corner_radius=0.08, width=0.5, height=th, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.45).move_to([self.mx, cy + h / 2 - th / 2, 0])
        self.mem_bot = RoundedRectangle(corner_radius=0.08, width=0.5, height=th, stroke_color=GREY, stroke_width=3,
                                        fill_color=GREY, fill_opacity=0.45).move_to([self.mx, cy - h / 2 + th / 2, 0])
        self.top = cy + h / 2
        self.lab_i = T("Inside cells (ICF)", 24, ICF_C).move_to([self.xi, self.top - 0.4, 0])
        self.lab_e = T("Outside cells (ECF)", 24, ECF_C).move_to([self.xe, self.top - 0.4, 0])

    def frame(self):
        return VGroup(self.icf, self.ecf, self.mem_top, self.mem_bot)

    def all(self):
        return VGroup(self.icf, self.ecf, self.mem_top, self.mem_bot, self.lab_i, self.lab_e)


def dot(color, x, y, r=0.1, o=1.0):
    return Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=o).move_to([x, y, 0])


def block(color, label="1 L", size=0.95):
    sq = Square(size, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.35)
    return VGroup(sq, M(label, 26, TEXT).move_to(sq))


def arrow(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


XI, XE = None, None


class S00Title(TitleCard):
    LESSON = "Body water and its compartments"
    TITLE = "Water goes where the solute stays"


# ---------------------------------------------------------------------------------------------
class S01Puzzle(SpokenScene):
    """The puzzle: one litre of pure water vs one litre of isotonic saline, two rooms, where does each go?"""

    def construct(self):
        R = Rooms()
        self.play(FadeIn(R.frame()), FadeIn(R.lab_i), FadeIn(R.lab_e), run_time=0.9)
        self.at("textbook model")
        note = T("Textbook model of an adult man", 26, GREY).move_to([0, 3.3, 0])
        self.play(FadeIn(note), run_time=0.5)
        # pure water
        wchip = chip("1 L pure water, no solute", WATER, 26).move_to([R.mx - 0.9, 2.5, 0])
        self.at("of pure water")
        self.play(FadeIn(wchip, shift=DOWN * 0.2), run_time=0.6)
        a1 = arrow([R.mx - 1.6, 2.15, 0], [R.xi + 0.2, R.top + 0.05, 0], ICF_C)
        t1 = T("about two thirds", 26, ICF_C).move_to([-4.6, 2.5, 0])
        self.at("About")
        self.play(GrowArrow(a1), FadeIn(t1), run_time=0.7)
        self.at("ends up inside cells")
        self.play(Indicate(R.icf, color=ICF_C, scale_factor=1.02), run_time=0.8)
        # isotonic saline
        schip = chip("1 L isotonic saline", SOL, 26).move_to([R.mx + 1.4, 2.5, 0])
        a2 = arrow([R.mx + 1.6, 2.15, 0], [R.xe, R.top + 0.05, 0], ECF_C)
        self.at("isotonic saline instead")
        self.play(FadeOut(wchip), FadeOut(a1), FadeOut(t1), FadeIn(schip, shift=DOWN * 0.2), run_time=0.6)
        self.at("Once it has spread")
        self.play(GrowArrow(a2), run_time=0.6)
        none = T("none", 52, RED, weight=BOLD).move_to([R.xi, R.cy - 0.1, 0])
        self.at("none of it")
        self.play(FadeIn(none, scale=1.2), run_time=0.5)
        self.at("Same body")
        self.play(Indicate(R.icf, color=RED, scale_factor=1.02), run_time=0.8)
        # the puzzle
        q1 = T("?", 110, GOLD, weight=BOLD).move_to([R.xi, R.cy - 0.1, 0])
        q2 = T("?", 110, GOLD, weight=BOLD).move_to([R.xe, R.cy - 0.1, 0])
        self.at("Why does the water go")
        self.play(FadeOut(none), FadeOut(schip), FadeOut(a2), FadeOut(note), run_time=0.4)
        self.play(FadeIn(q1, scale=0.8), FadeIn(q2, scale=0.8), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Tanks(SpokenScene):
    """70-kg bar with 60 percent water -> total body water block -> splits into 28 L and 14 L."""

    def construct(self):
        R = Rooms()
        bw, bx0 = 11.3, -5.65
        bar = RoundedRectangle(corner_radius=0.15, width=bw, height=1.7, stroke_color=GREY, stroke_width=3
                               ).move_to([0, 0.6, 0])
        body_lab = T("70-kg reference man", 28, GREY).move_to([bx0 + bw * 0.805, 0.6, 0])
        self.at("reference man")
        self.play(Create(bar), FadeIn(body_lab), run_time=0.8)
        wfill = Rectangle(width=bw * 0.6, height=1.7, stroke_width=0, fill_color=WATER, fill_opacity=0.4
                          ).move_to([bx0 + bw * 0.3, 0.6, 0])
        wlab = T("60 percent water", 36, WATER).move_to(wfill)
        self.at("whose body")
        self.play(GrowFromEdge(wfill, LEFT), FadeIn(wlab), run_time=0.9)
        conv = T("a convention for arithmetic, not a measurement of anyone", 30, GREY).move_to([0, -0.8, 0])
        self.at("convention")
        self.play(FadeIn(conv, shift=UP * 0.15), run_time=0.6)
        # total body water
        tbw = RoundedRectangle(corner_radius=0.2, width=R.icf.width + R.ecf.width + 0.5, height=R.h,
                               stroke_color=WATER, stroke_width=4, fill_color=WATER, fill_opacity=0.12).move_to([0, R.cy, 0])
        tlab = T("Total body water: about 42 L", 36, WATER).move_to([0, R.cy + 0.2, 0])
        self.at("Total body water")
        self.play(ReplacementTransform(VGroup(wfill, wlab), tbw), FadeOut(bar), FadeOut(body_lab), FadeOut(conv),
                  run_time=1.0)
        self.play(FadeIn(tlab), run_time=0.4)
        # split into the rooms
        vi = M("28 L", 56, ICF_C).move_to([R.xi, R.cy - 0.3, 0])
        ve = M("14 L", 56, ECF_C).move_to([R.xe, R.cy - 0.3, 0])
        self.at("of it")
        self.play(ReplacementTransform(tbw, R.frame()), FadeOut(tlab), run_time=0.9)
        self.play(FadeIn(vi, scale=0.8), run_time=0.5)
        self.at("inside cells")
        self.play(FadeIn(R.lab_i), run_time=0.5)
        self.at("About", nth=2)
        self.play(Indicate(R.ecf, color=ECF_C, scale_factor=1.02), run_time=0.6)
        self.play(FadeIn(ve, scale=0.8), run_time=0.5)
        self.at("outside them")
        self.play(FadeIn(R.lab_e), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Door(SpokenScene):
    """Two rooms, a door only water passes; the stuck solute in each room decides the water it holds."""

    def construct(self):
        R = Rooms()
        vi = M("28 L", 56, ICF_C).move_to([R.xi, R.cy - 0.3, 0])
        ve = M("14 L", 56, ECF_C).move_to([R.xe, R.cy - 0.3, 0])
        self.add(R.all(), vi, ve)
        # the door: water only
        door = DoubleArrow([R.mx - 0.38, R.cy, 0], [R.mx + 0.38, R.cy, 0], color=WATER, stroke_width=6, buff=0,
                           tip_length=0.2)
        wdots = VGroup(*[dot(WATER, x, y, 0.1, 0.8) for x, y in
                         [(-5.0, R.cy - 1.75), (-3.4, R.cy - 1.5), (-1.5, R.cy - 1.75), (0.2, R.cy - 1.45),
                          (2.9, R.cy - 1.85), (4.7, R.cy - 1.85)]])
        self.at("Water crosses")
        self.play(FadeOut(vi), FadeOut(ve), FadeIn(door), FadeIn(wdots), run_time=0.6)
        dl = T("the door: only water passes", 24, WATER).move_to([R.mx, R.cy - 2.65, 0])
        self.at("two rooms joined")
        self.play(FadeIn(dl), run_time=0.5)
        self.at("only water can pass")
        mv = [dot(WATER, R.xe - 0.6, R.cy - 0.1, 0.13), dot(WATER, R.xi + 1.2, R.cy - 0.9, 0.13)]
        self.play(FadeIn(mv[0]), FadeIn(mv[1]), run_time=0.3)
        self.play(mv[0].animate.move_to([R.xi + 1.2, R.cy - 0.1, 0]), mv[1].animate.move_to([R.xe - 0.6, R.cy - 0.9, 0]),
                  run_time=0.9, rate_func=linear)
        self.play(FadeOut(mv[0]), FadeOut(mv[1]), run_time=0.3)
        # stuck guests
        an = chip("anions that cannot leave", SOL, 24).move_to([R.xi - 1.4, R.cy + 0.35, 0])
        kc = chip("K⁺", SOL, 24).move_to([R.xi + 2.3, R.cy + 0.35, 0])
        self.at("stuck in each room")
        self.play(Indicate(R.icf, color=SOL, scale_factor=1.015), Indicate(R.ecf, color=SOL, scale_factor=1.015),
                  run_time=0.8)
        self.at("Inside cells")
        self.play(FadeIn(an, shift=UP * 0.15), run_time=0.5)
        self.at("and the potassium")
        self.play(FadeIn(kc, shift=UP * 0.15), run_time=0.5)
        na = chip("Na⁺", SOL, 24).move_to([R.xe - 0.7, R.cy + 0.35, 0])
        cl = chip("Cl⁻", SOL, 24).move_to([R.xe + 0.75, R.cy + 0.35, 0])
        bi = chip("bicarbonate", SOL, 24).move_to([R.xe, R.cy - 0.4, 0])
        self.at("Outside")
        self.play(FadeIn(na, shift=UP * 0.15), run_time=0.5)
        self.at("chloride")
        self.play(FadeIn(cl, shift=UP * 0.15), FadeIn(bi, shift=UP * 0.15), run_time=0.6)
        # sodium leaks in, the pump moves it back out
        y1, y2 = 2.95, 2.2
        a_in = arrow([R.mx + 1.6, y1, 0], [R.mx - 1.2, y1, 0], SOL)
        t_in = T("Na⁺ leaks into cells", 24, SOL).next_to(a_in, LEFT, buff=0.2)
        a_out = arrow([R.mx - 1.2, y2, 0], [R.mx + 1.6, y2, 0], SOL)
        t_out = T("pump moves Na⁺ back out", 24, SOL).next_to(a_out, LEFT, buff=0.2)
        self.at("leaks into")
        self.play(GrowArrow(a_in), FadeIn(t_in), run_time=0.8)
        self.at("moves it back out")
        self.play(GrowArrow(a_out), FadeIn(t_out), run_time=0.8)
        eff = T("effective solute", 26, SOL, weight=BOLD).move_to([R.xe, R.cy - 1.15, 0])
        self.at("effective solute")
        self.play(Indicate(VGroup(na, cl, bi), color=SOL, scale_factor=1.12), FadeIn(eff), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Count(SpokenScene):
    """Count the effective solute: 300 mOsm/kg in both rooms; osmoles = volume x concentration."""

    def construct(self):
        R = Rooms(cy=-0.3, h=4.0)
        self.add(R.all())
        # solute guests: equal density, so twice as many in the room twice the size
        grid = VGroup()
        for x in np.arange(R.xi - 3.0, R.xi + 3.1, 0.8):
            for y in (R.cy - 1.3, R.cy - 1.75):
                grid.add(dot(SOL, x, y, 0.1, 0.9))
        for x in np.arange(R.xe - 1.2, R.xe + 1.3, 0.8):
            for y in (R.cy - 1.3, R.cy - 1.75):
                grid.add(dot(SOL, x, y, 0.1, 0.9))
        legend = T("Yellow dots: effective solute (schematic, not to scale)", 22, SOL).move_to([0, R.cy + 2.45, 0])
        self.at("count the guests")
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in grid], lag_ratio=0.03), FadeIn(legend), run_time=1.2)
        ci = M("300 mOsm/kg", 28, SOL).move_to([R.xi, R.cy - 0.2, 0])
        ce = M("300 mOsm/kg", 28, SOL).move_to([R.xe, R.cy - 0.2, 0])
        self.at("both rooms sit")
        self.play(FadeIn(ci, scale=0.9), FadeIn(ce, scale=0.9), run_time=0.7)
        note = T("Made-up, rounded numbers. Measured adult values are about 275 to 295 mOsm/kg.", 22, GREY
                 ).move_to([0, 2.65, 0])
        self.at("made up")
        self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.6)
        vi = M("28 L", 40, TEXT).move_to([R.xi, R.cy + 0.55, 0])
        ve = M("14 L", 40, TEXT).move_to([R.xe, R.cy + 0.55, 0])
        oi = M("= 8,400 mOsm", 28, SOL).move_to([R.xi, R.cy - 0.8, 0])
        oe = M("= 4,200 mOsm", 28, SOL).move_to([R.xe, R.cy - 0.8, 0])
        self.at("of cells hold")
        self.play(FadeIn(vi, scale=0.9), run_time=0.4)
        self.play(FadeIn(oi, shift=UP * 0.1), run_time=0.5)
        self.at("fluid hold")
        self.play(FadeIn(ve, scale=0.9), run_time=0.4)
        self.play(FadeIn(oe, shift=UP * 0.1), run_time=0.5)
        c1 = T("closed body: no urine, sweat or breath losses", 22, GREY).move_to([0, R.cy - 2.45, 0])
        c2 = T("added sodium chloride stays outside cells", 22, GREY).move_to([0, R.cy - 2.9, 0])
        self.at("closed body")
        self.play(FadeIn(c1), run_time=0.5)
        self.at("added sodium chloride")
        self.play(FadeIn(c2), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Litre(SpokenScene):
    """Trial A: 1 L isotonic saline. Trial B: 1 L solute-free water. Where does each litre go?"""

    def construct(self):
        R = Rooms()

        def vol(txt, x, color):
            return M(txt, 40, color).move_to([x, R.cy + 0.45, 0])

        def conc(txt, x):
            return M(txt, 26, SOL).move_to([x, R.cy - 0.45, 0])

        def delta(txt, x, color):
            return M(txt, 34, color).move_to([x, R.cy - 1.4, 0])

        vi, ve = vol("28.0 L", R.xi, TEXT), vol("14.0 L", R.xe, TEXT)
        ci, ce = conc("300 mOsm/kg", R.xi), conc("300 mOsm/kg", R.xe)
        self.add(R.all(), vi, ve, ci, ce)

        # ---- Trial A: isotonic saline ----------------------------------------------------------
        ta = T("Trial A: 1 L isotonic saline", 30, SOL).move_to([0, 3.25, 0])
        bA = block(SOL, "1 L").move_to([R.xe, 2.3, 0])
        sdots = VGroup(*[dot(SOL, R.xe + dx, R.cy + 1.15, 0.1) for dx in (-1.2, -0.6, 0.0, 0.6, 1.2)])
        self.at("Retain")
        self.play(FadeIn(ta, shift=DOWN * 0.1), FadeIn(bA), run_time=0.6)
        self.at("Its particles stay outside")
        self.play(bA.animate.move_to([R.xe, R.top - 0.05, 0]).scale(0.4).set_opacity(0.0),
                  LaggedStart(*[FadeIn(d, scale=0.4) for d in sdots], lag_ratio=0.15), run_time=1.0)
        self.at("so the concentration does not change")
        self.play(Indicate(VGroup(ci, ce), color=SOL, scale_factor=1.1), run_time=0.9)
        di = delta("unchanged", R.xi, GREY)
        self.at("Cells stay")
        self.play(FadeIn(di), run_time=0.5)
        ve2 = vol("15.0 L", R.xe, ECF_C)
        de = delta("+1.0 L", R.xe, ECF_C)
        self.at("grows to")
        self.play(ReplacementTransform(ve, ve2), FadeIn(de, shift=UP * 0.1), run_time=0.8)

        # ---- Trial B: solute-free water (reset every answer in the same beat as the new label) -----
        tb = T("Trial B: 1 L solute-free water", 30, WATER).move_to([0, 3.25, 0])
        ve0 = vol("14.0 L", R.xe, TEXT)
        bB = block(WATER, "1 L").move_to([R.xe, 2.3, 0])
        self.at("Now retain")
        self.play(ReplacementTransform(ta, tb), ReplacementTransform(ve2, ve0), FadeOut(de), FadeOut(di), FadeOut(sdots),
                  FadeIn(bB, shift=DOWN * 0.2), run_time=0.8)
        # the litre sits outside cells first: ECF 15.0 L, its concentration no longer the same as the cells'
        ve15 = vol("15.0 L", R.xe, ECF_C)
        de15 = delta("+1.0 L", R.xe, ECF_C)
        cdil = T("diluted", 28, SOL).move_to([R.xe, R.cy - 0.45, 0])
        self.at("first sits")
        self.play(bB.animate.move_to([R.xe, R.top - 0.05, 0]).scale(0.4).set_opacity(0.0),
                  ReplacementTransform(ve0, ve15), FadeIn(de15, shift=UP * 0.1), ReplacementTransform(ce, cdil),
                  run_time=1.0)
        # water crosses the door into the cells; volumes end at 28.67 / 14.33 (sum stays 43 L)
        vi3 = vol("28.67 L", R.xi, ICF_C)
        ve3 = vol("14.33 L", R.xe, ECF_C)
        mv = VGroup(*[dot(WATER, R.xe - 1.1 + 0.4 * k, R.cy, 0.12) for k in range(3)])
        self.at("crosses until")
        self.play(FadeIn(mv, scale=0.5), FadeOut(ci), FadeOut(cdil), FadeOut(de15), run_time=0.3)
        self.play(mv.animate.shift(LEFT * 3.6), ReplacementTransform(vi, vi3), ReplacementTransform(ve15, ve3),
                  run_time=1.2, rate_func=linear)
        self.play(FadeOut(mv), run_time=0.3)
        ci2, ce2 = conc("293.0 mOsm/kg", R.xi), conc("293.0 mOsm/kg", R.xe)
        self.at("They end")
        self.play(FadeIn(ci2, scale=0.9), FadeIn(ce2, scale=0.9), run_time=0.7)
        di3 = delta("+0.67 L", R.xi, ICF_C)
        self.at("Cells gain")
        self.play(FadeIn(di3, shift=UP * 0.1), run_time=0.6)
        de3 = delta("+0.33 L", R.xe, ECF_C)
        self.at("gains")
        self.play(FadeIn(de3, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    """The rule: water follows effective solute. Where the litre goes, in the model; not how long it stays."""

    def construct(self):
        rule = T("Water follows effective solute", 46, TEXT, font=TITLE_FONT, t2c={"effective solute": SOL}
                 ).move_to([0, 3.0, 0])
        self.at("rule to keep")
        self.play(FadeIn(rule, shift=DOWN * 0.15), run_time=0.8)
        sub = T("each compartment holds water in proportion to its effective osmoles", 26, GREY).move_to([0, 2.15, 0])
        self.at("Each compartment holds water")
        self.play(FadeIn(sub), run_time=0.6)
        W = 10.0
        x0 = -W / 2

        def bar(frac_i, y):
            parts = VGroup()
            if frac_i > 0:
                parts.add(Rectangle(width=W * frac_i, height=0.75, stroke_color=ICF_C, stroke_width=3, fill_color=ICF_C,
                                    fill_opacity=0.35).move_to([x0 + W * frac_i / 2, y, 0]))
            parts.add(Rectangle(width=W * (1 - frac_i), height=0.75, stroke_color=ECF_C, stroke_width=3, fill_color=ECF_C,
                                fill_opacity=0.35).move_to([x0 + W * frac_i + W * (1 - frac_i) / 2, y, 0]))
            return parts

        la = T("In the model, one litre of retained isotonic saline", 24, SOL).move_to([0, 1.35, 0])
        ba = bar(0.0, 0.7)
        ta = T("+1.0 L outside cells", 26, ECF_C).move_to(ba)
        self.at("retained saline")
        self.play(FadeIn(la), run_time=0.4)
        self.play(GrowFromEdge(ba, LEFT), FadeIn(ta), run_time=0.8)
        lb = T("one litre of retained solute-free water", 24, WATER).move_to([0, -0.2, 0])
        bb = bar(2 / 3, -0.85)
        tb1 = T("+0.67 L inside cells", 26, ICF_C).move_to(bb[0])
        tb2 = T("+0.33 L outside", 24, ECF_C).move_to(bb[1])
        self.at("pure water is shared")
        self.play(FadeIn(lb), run_time=0.4)
        self.play(GrowFromEdge(bb, LEFT), FadeIn(tb1), FadeIn(tb2), run_time=0.9)
        eq = T("equilibrium arithmetic", 28, TEAL, weight=BOLD).move_to([0, -1.85, 0])
        self.at("This is equilibrium arithmetic")
        self.play(FadeIn(eq, shift=UP * 0.1), run_time=0.5)
        c1 = chip("where it goes: predicted", GREEN, 24).move_to([-3.1, -2.85, 0])
        c2 = chip("how long it stays: not predicted", GREY, 24).move_to([3.3, -2.85, 0])
        self.at("where a retained load goes")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        self.at("how long it stays")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Water follows effective solute."
