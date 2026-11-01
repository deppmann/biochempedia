"""Gas exchange: how two streams flow matters  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.
The lesson's own numbers only: dry air at sea level about 21% oxygen at about 760 mmHg, so about
160 mmHg; alveolar PO2 about 100 mmHg in an adult human at rest; warmed, humidified inhaled air
about 150 mmHg. Every level, bar and shade is "in this sketch, not to scale".

COLOR MAP (one color per concept, whole video)
  BLOOD   = blood, purple (the stream inside the lamella or capillary)
  TEAL   = the outside medium: water or air
  YELLOW = oxygen partial pressure (brighter fill = higher, in this sketch)
  RED    = a stretch that adds little
  GREY   = structure, outlines, notes
  TEXT   = generic labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


BLOOD = "#B48CF0"


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def bchip(text, color=BLOOD, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def sketch_note(y=-3.45, x=0):
    return T("in this sketch, not to scale", 22, GREY).move_to([x, y, 0])


def bar(x, base, h, w=0.9, color=YELLOW, op=0.5, stroke=None):
    return Rectangle(width=w, height=max(h, 0.02), stroke_color=stroke or color, stroke_width=3,
                     fill_color=color, fill_opacity=op).move_to([x, base + max(h, 0.02) / 2, 0])


def cell(x, y, v, edge, w=1.2, h=0.8):
    return Rectangle(width=w, height=h, stroke_color=edge, stroke_width=3, fill_color=YELLOW,
                     fill_opacity=0.12 + 0.78 * v).move_to([x, y, 0])


class S00Title(TitleCard):
    LESSON = "Gas exchange and breathing"
    TITLE = "How two streams flow matters"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        base, k = -1.7, 3.6
        XL1, XL2, XR1, XR2 = -5.0, -2.9, 2.4, 4.5
        left = RoundedRectangle(corner_radius=0.2, width=6.0, height=5.6, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.05).move_to([-3.95, -0.2, 0])
        right = RoundedRectangle(corner_radius=0.2, width=6.0, height=5.6, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.05).move_to([3.45, -0.2, 0])
        tl = T("a trout's gill", 30, TEXT).move_to([-3.95, 2.1, 0])
        tr = T("your lung", 30, TEXT).move_to([3.45, 2.1, 0])
        water = chip("water holds far less oxygen than air", TEAL, 24).move_to([0, 3.2, 0])
        note = sketch_note(-3.3)

        self.at("Water holds")
        self.play(FadeIn(water, shift=DOWN * 0.1), run_time=0.8)
        self.at("trout")
        self.play(FadeIn(left), FadeIn(tl), run_time=0.6)
        w_in = bar(XL1, base, 0.75 * k, color=YELLOW, op=0.55, stroke=TEAL)
        w_in_l = T("water\nflowing in", 22, TEAL, line_spacing=0.6).next_to(w_in, DOWN, buff=0.12)
        self.play(FadeIn(w_in, shift=UP * 0.2), FadeIn(w_in_l), run_time=0.6)
        self.at("close to")
        b_out = bar(XL2, base, 0.7 * k, color=YELLOW, op=0.55, stroke=BLOOD)
        b_out_l = T("blood\nleaving", 22, BLOOD, line_spacing=0.6).next_to(b_out, DOWN, buff=0.12)
        gap = DashedLine([XL1 - 0.45, base + 0.75 * k, 0], [XL2 + 0.45, base + 0.75 * k, 0], color=TEXT, stroke_width=3)
        self.play(FadeIn(b_out, shift=UP * 0.2), FadeIn(b_out_l), Create(gap), run_time=0.8)
        self.at("Your lung")
        self.play(FadeIn(right), FadeIn(tr), run_time=0.6)
        a_in = bar(XR1, base, 0.75 * k, color=YELLOW, op=0.55, stroke=TEAL)
        a_in_l = T("air\nflowing in", 22, TEAL, line_spacing=0.6).next_to(a_in, DOWN, buff=0.12)
        q_box = DashedVMobject(Rectangle(width=0.9, height=0.75 * k, stroke_color=BLOOD, stroke_width=3
                                         ).move_to([XR2, base + 0.75 * k / 2, 0]), num_dashes=30)
        q_l = T("blood\nleaving", 22, BLOOD, line_spacing=0.6).next_to(q_box, DOWN, buff=0.12)
        self.play(FadeIn(a_in, shift=UP * 0.2), FadeIn(a_in_l), run_time=0.6)
        self.play(Create(q_box), FadeIn(q_l), run_time=0.6)
        self.at("Why not")
        q = T("?", 90, YELLOW, weight=BOLD).move_to(q_box.get_center())
        self.play(FadeIn(q, scale=1.4), FadeIn(note), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Fick(SpokenScene):
    def construct(self):
        base, k = -2.2, 3.4
        XH, XB, XLO = -5.2, -3.4, -1.6
        slab = Rectangle(width=0.7, height=3.8, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.35).move_to([XB, base + 1.9, 0])
        slab_l = T("barrier", 24, GREY).next_to(slab, UP, buff=0.12)
        hi = bar(XH, base, 0.95 * k, w=1.0)
        lo = bar(XLO, base, 0.35 * k, w=1.0)
        hi_l = T("higher", 22, YELLOW).next_to(hi, DOWN, buff=0.12)
        lo_l = T("lower", 22, YELLOW).next_to(lo, DOWN, buff=0.12)
        flow = arr([XH + 0.6, base + 2.6, 0], [XLO - 0.6, base + 2.6, 0], TEXT)
        pp_l = T("partial pressure", 24, YELLOW).move_to([-3.4, base + 4.95, 0])

        self.at("by diffusion")
        self.play(FadeIn(slab), FadeIn(slab_l), run_time=0.6)
        self.at("higher partial pressure")
        self.play(FadeIn(hi, shift=UP * 0.2), FadeIn(hi_l), FadeIn(pp_l), run_time=0.6)
        self.at("to lower")
        self.play(FadeIn(lo, shift=UP * 0.2), FadeIn(lo_l), GrowArrow(flow), run_time=0.8)

        c1 = bchip("dry air, sea level:\nabout 21% oxygen", TEAL, 24).move_to([3.1, 2.7, 0])
        c1b = bchip("total pressure\nabout 760 mmHg", TEAL, 24).move_to([3.1, 1.3, 0])
        c2 = bchip("oxygen: 0.21 x 760\nroughly 160 mmHg", YELLOW, 24).move_to([3.1, -0.1, 0])
        self.at("Dry air")
        self.play(FadeIn(c1, shift=LEFT * 0.2), run_time=0.7)
        self.at("total pressure")
        self.play(FadeIn(c1b, shift=LEFT * 0.2), run_time=0.7)
        self.at("So oxygen's")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.7)

        eq = M("rate = k x A x (P1 - P2) / T", 26, TEXT).move_to([3.1, -1.25, 0])
        self.at("The rate")
        self.play(FadeIn(eq), run_time=0.6)
        tags = VGroup(T("A: area", 22, TEXT), T("P1 - P2: pressure difference", 22, YELLOW),
                      T("T: barrier thickness", 22, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.12
                                                                   ).move_to([3.1, -2.55, 0])
        self.play(FadeIn(tags), run_time=0.5)
        self.at("pressure difference")
        self.play(Circumscribe(tags[1], color=YELLOW, buff=0.1), run_time=0.7)
        self.at("barrier thickness")
        self.play(Circumscribe(tags[2], color=GREY, buff=0.1), run_time=0.7)
        self.at("kept up")
        dbl = DoubleArrow([XLO + 0.9, base + 0.35 * k, 0], [XLO + 0.9, base + 0.95 * k, 0], buff=0, color=YELLOW,
                          stroke_width=5, tip_length=0.2)
        self.play(GrowFromCenter(dbl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Gill(SpokenScene):
    N = 8
    XS = np.linspace(-4.55, 4.55, 8)
    YW, YB = 1.05, -1.05

    def row(self, y, vals, edge):
        return VGroup(*[cell(x, y, v, edge) for x, v in zip(self.XS, vals)])

    def construct(self):
        N, XS, YW, YB = self.N, self.XS, self.YW, self.YB
        # sketch values (relative), water falls along its path, blood rises along its path
        w = np.linspace(1.0, 0.45, N)
        b_ctr = w - 0.1                     # blood exits at the left, enters at the right
        outline = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=11.4, height=4.7, stroke_color=GREY,
                                                  stroke_width=3).move_to([0, 0, 0]), num_dashes=80)
        lam_l = T("one lamella", 26, GREY).move_to([4.5, 1.8, 0])
        water = self.row(YW, w, TEAL)
        wl = T("water", 26, TEAL).move_to([-6.0, YW, 0]) if False else None
        w_arr = arr([-5.0, 1.85, 0], [-3.2, 1.85, 0], TEAL)
        w_lbl = T("water in", 24, TEAL).next_to(w_arr, RIGHT, buff=0.15)

        self.at("In teleost fish")
        t = bchip("teleost fish: gill filaments carry thin plates, the lamellae", GREY, 24).move_to([0, 3.2, 0])
        self.play(FadeIn(t), run_time=0.7)
        self.at("carries filaments")
        self.play(Create(outline), FadeIn(lam_l), run_time=0.8)
        self.at("called lamellae")
        self.play(FadeIn(water), GrowArrow(w_arr), FadeIn(w_lbl), run_time=0.8)

        # blood, opposite direction
        blood = self.row(YB, b_ctr, BLOOD)
        b_arr = arr([5.0, -1.85, 0], [3.2, -1.85, 0], BLOOD)
        b_lbl = T("blood in", 24, BLOOD).next_to(b_arr, LEFT, buff=0.15)
        self.at("opposite to the water")
        self.play(FadeIn(blood), GrowArrow(b_arr), FadeIn(b_lbl), run_time=0.9)
        cc = T("countercurrent exchange", 32, TEXT, font=TITLE_FONT).move_to([0, -3.05, 0])
        self.at("countercurrent exchange")
        self.play(FadeIn(cc, shift=UP * 0.1), run_time=0.6)

        # leaving blood meets new water (both at left)
        out_arr = arr([-3.2, -1.85, 0], [-5.0, -1.85, 0], BLOOD)
        out_lbl = T("blood out", 24, BLOOD).next_to(out_arr, RIGHT, buff=0.15)
        self.at("about to leave")
        self.play(FadeOut(b_arr), FadeOut(b_lbl), run_time=0.01)
        self.play(GrowArrow(out_arr), FadeIn(out_lbl), Circumscribe(blood[0], color=BLOOD, buff=0.08), run_time=0.8)
        self.at("just arrived")
        self.play(Circumscribe(water[0], color=TEAL, buff=0.08), run_time=0.8)

        # difference marks all along
        marks = VGroup(*[DoubleArrow([x, YW - 0.45, 0], [x, YB + 0.45, 0], buff=0, color=YELLOW, stroke_width=4,
                                     tip_length=0.12) for x in XS])
        self.at("along the whole")
        self.play(FadeIn(marks, lag_ratio=0.1), run_time=1.0)
        diff_l = T("a difference everywhere", 24, YELLOW).move_to([0, 0, 0]).set_z_index(5)
        back = Rectangle(width=diff_l.width + 0.3, height=diff_l.height + 0.12, stroke_width=0, fill_color=BG,
                         fill_opacity=0.92).move_to(diff_l).set_z_index(4)
        self.play(FadeIn(back), FadeIn(diff_l), run_time=0.4)

        # reset to the same-direction case in one move
        wv = np.array([1.0, 0.84, 0.72, 0.64, 0.6, 0.6, 0.6, 0.6])
        bv = np.array([0.2, 0.35, 0.46, 0.55, 0.6, 0.6, 0.6, 0.6])
        blood2 = self.row(YB, bv, BLOOD)
        water2 = self.row(YW, wv, TEAL)
        same_arr = arr([-5.0, -1.85, 0], [-3.2, -1.85, 0], BLOOD)
        same_l = T("blood in", 24, BLOOD).next_to(same_arr, RIGHT, buff=0.15)
        cc2 = T("same direction", 32, TEXT, font=TITLE_FONT).move_to([0, -3.05, 0])
        self.at("ran the same way")
        self.play(FadeOut(marks), FadeOut(diff_l), FadeOut(back), FadeOut(out_arr), FadeOut(out_lbl),
                  FadeOut(cc), Transform(blood, blood2), Transform(water, water2), run_time=0.9)
        self.play(GrowArrow(same_arr), FadeIn(same_l), FadeIn(cc2), run_time=0.6)
        self.at("equal partial pressure")
        eq_box = SurroundingRectangle(VGroup(water[4:], blood[4:]), color=RED, buff=0.08, stroke_width=4,
                                      corner_radius=0.08)
        eq_l = T("nearly equal from here", 24, RED).move_to([2.3, 0.28, 0]).set_z_index(5)
        eq_back = Rectangle(width=eq_l.width + 0.3, height=eq_l.height + 0.12, stroke_width=0, fill_color=BG,
                            fill_opacity=0.92).move_to(eq_l).set_z_index(4)
        self.play(Create(eq_box), FadeIn(eq_back), FadeIn(eq_l), run_time=0.8)
        self.at("add little")
        nothing = T("adds little", 24, RED, weight=BOLD).move_to([2.3, -0.28, 0])
        self.play(FadeIn(nothing), FadeIn(sketch_note(-3.5, 4.4)), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Mammal(SpokenScene):
    def construct(self):
        YT = 0.5
        tube = Rectangle(width=3.9, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.12).move_to([-4.3, YT, 0])
        tube_l = T("airways", 24, GREY).next_to(tube, UP, buff=0.12)
        sac = RoundedRectangle(corner_radius=0.5, width=2.6, height=2.6, stroke_color=TEAL, stroke_width=3,
                               fill_color=TEAL, fill_opacity=0.08).move_to([-0.7, YT, 0])
        sac_l = T("alveoli, dead-ended", 24, TEAL).next_to(sac, UP, buff=0.12)
        two = DoubleArrow([-6.0, YT, 0], [-2.6, YT, 0], buff=0, color=TEAL, stroke_width=6, tip_length=0.25)
        in_out = T("in and out, same airways", 24, TEAL).next_to(tube, DOWN, buff=0.12)

        self.at("Now")
        mm = T("in mammals", 28, TEXT).move_to([-5.2, 3.2, 0])
        self.play(FadeIn(mm), run_time=0.5)
        self.at("same airways")
        self.play(FadeIn(tube), FadeIn(tube_l), GrowFromCenter(two), FadeIn(in_out), run_time=0.9)
        self.at("tidal ventilation")
        tv = T("tidal ventilation", 32, TEXT, font=TITLE_FONT).move_to([-3.4, -2.0, 0])
        self.play(FadeIn(tv, shift=UP * 0.1), run_time=0.5)
        self.at("airways end")
        self.play(FadeIn(sac), FadeIn(sac_l), run_time=0.8)

        # stale air left behind, fresh air mixing in
        stale = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color=GREY, fill_opacity=0.9
                                ).move_to([-0.7 + dx, YT + dy, 0]) for dx, dy in
                         [(0.5, 0.6), (0.75, -0.1), (0.3, -0.7), (0.85, 0.7)]])
        fresh = VGroup(*[Circle(radius=0.12, stroke_width=0, fill_color=TEAL, fill_opacity=1
                                ).move_to([-3.0 + 0.35 * i, YT + dy, 0]) for i, dy in enumerate([0.25, -0.25, 0.3, -0.2])])
        stale_l = T("stale air left behind", 22, GREY).next_to(sac, DOWN, buff=0.12)
        self.at("stale air")
        self.play(FadeIn(stale), FadeIn(stale_l), run_time=0.5)
        self.play(FadeIn(fresh), run_time=0.3)
        self.play(*[fresh[i].animate.move_to([-1.3 + 0.3 * i, YT + [0.35, -0.35, 0.05, -0.15][i], 0]) for i in range(4)],
                  run_time=1.0)

        # the bars (right half)
        base, K = -2.3, 3.2 / 150.0
        X1, X2, X3 = 2.4, 4.2, 6.0
        b1 = bar(X1, base, 150 * K, w=1.1, color=YELLOW, op=0.5, stroke=TEAL)
        b2 = bar(X2, base, 100 * K, w=1.1, color=YELLOW, op=0.5, stroke=TEAL)
        b3 = bar(X3, base, 100 * K, w=1.1, color=YELLOW, op=0.5, stroke=BLOOD)
        v1 = T("roughly 150", 22, YELLOW).next_to(b1, UP, buff=0.1)
        v2 = T("about 100", 22, YELLOW).next_to(b2, UP, buff=0.1)
        v3 = T("at best 100", 22, YELLOW).next_to(b3, UP, buff=0.1)
        l1 = T("inhaled air,\nwarmed and\nhumidified", 22, TEAL, line_spacing=0.6).next_to(b1, DOWN, buff=0.1)
        l2 = T("alveolar\ngas", 22, TEAL, line_spacing=0.6).next_to(b2, DOWN, buff=0.1)
        l3 = T("blood", 22, BLOOD).next_to(b3, DOWN, buff=0.1)
        unit = T("oxygen partial pressure, mmHg", 22, YELLOW).move_to([4.2, 3.3, 0])
        who = T("adult human at rest", 22, GREY).move_to([4.2, 2.85, 0])
        self.at("adult human at rest")
        self.play(FadeIn(unit), FadeIn(who), FadeIn(b2), FadeIn(v2), FadeIn(l2), run_time=0.9)
        self.at("millimeters")
        self.play(Indicate(b2, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.at("humidified inhaled")
        self.play(FadeIn(b1), FadeIn(v1), FadeIn(l1), run_time=0.9)
        self.at("Blood can at best")
        self.play(FadeIn(b3), FadeIn(v3), FadeIn(l3), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Bird(SpokenScene):
    def construct(self):
        YT = 1.0
        tube = Rectangle(width=11.2, height=1.3, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.12).move_to([0, YT, 0])
        tube_l = T("one parabronchus", 24, GREY).move_to([-4.6, YT + 1.0, 0])
        in_a = arr([-5.4, YT + 0.27, 0], [-3.0, YT + 0.27, 0], TEAL, w=6)
        out_a = arr([-5.4, YT - 0.27, 0], [-3.0, YT - 0.27, 0], TEAL, w=6)
        in_l = T("breathing in", 22, TEAL).next_to(in_a, RIGHT, buff=0.15)
        out_l = T("breathing out", 22, TEAL).next_to(out_a, RIGHT, buff=0.15)

        self.at("Birds do it")
        b = T("in birds", 28, TEXT).move_to([-5.2, 3.2, 0])
        self.play(FadeIn(b), run_time=0.5)
        self.at("parabronchi")
        self.play(FadeIn(tube), FadeIn(tube_l), run_time=0.7)
        self.at("same way")
        self.play(GrowArrow(in_a), FadeIn(in_l), run_time=0.7)
        self.at("breathing out")
        self.play(GrowArrow(out_a), FadeIn(out_l), run_time=0.7)

        xs = [0.2, 2.4, 4.6]
        caps = VGroup(*[Rectangle(width=0.55, height=3.0, stroke_color=BLOOD, stroke_width=3, fill_color=BLOOD,
                                  fill_opacity=0.18).move_to([x, YT, 0]) for x in xs])
        cap_l = T("capillaries cross the airstream", 24, BLOOD).move_to([2.8, YT + 1.95, 0])
        self.at("Capillaries cross")
        self.play(FadeIn(caps, lag_ratio=0.3), FadeIn(cap_l), run_time=1.0)
        cx = T("crosscurrent exchange", 32, TEXT, font=TITLE_FONT).move_to([0, -1.0, 0])
        self.at("crosscurrent")
        self.play(FadeIn(cx, shift=UP * 0.1), run_time=0.6)
        self.at("different stage")
        self.play(*[Indicate(c, color=YELLOW, scale_factor=1.12) for c in caps], run_time=1.5, lag_ratio=0.4)

        # comparison: mixed blood leaving versus air breathed out (relative, in this sketch)
        base, K = -3.1, 1.9
        X1, X2 = -1.4, 1.4
        a = bar(X1, base, 0.55 * K, w=1.0, color=YELLOW, op=0.5, stroke=TEAL)
        m = bar(X2, base, 0.85 * K, w=1.0, color=YELLOW, op=0.5, stroke=BLOOD)
        a_l = T("air breathed out", 22, TEAL).next_to(a, LEFT, buff=0.15)
        m_l = T("mixed blood leaving", 22, BLOOD).next_to(m, RIGHT, buff=0.15)
        ql = T("oxygen partial pressure, in this sketch, not to scale", 22, YELLOW).move_to([0, -3.45, 0])
        self.at("mixed blood")
        self.play(FadeIn(a), FadeIn(a_l), FadeIn(m), FadeIn(m_l), FadeIn(ql), run_time=0.9)
        self.at("a higher partial pressure")
        self.play(Indicate(m, color=YELLOW, scale_factor=1.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rank(SpokenScene):
    def construct(self):
        XS = [-4.1, 0.0, 4.1]
        head = T("idealized models, matched conditions", 28, GREY).move_to([0, 3.3, 0])
        who = T("Piiper and Scheid, 1972", 24, GREY).move_to([0, 2.8, 0])

        def icon_counter(x):
            a = arr([x - 1.0, 1.75, 0], [x + 1.0, 1.75, 0], TEAL, w=5)
            b = arr([x + 1.0, 1.15, 0], [x - 1.0, 1.15, 0], BLOOD, w=5)
            return VGroup(a, b)

        def icon_cross(x):
            a = arr([x - 1.2, 1.45, 0], [x + 1.2, 1.45, 0], TEAL, w=5)
            bars = VGroup(*[Rectangle(width=0.3, height=1.5, stroke_color=BLOOD, stroke_width=3, fill_color=BLOOD,
                                      fill_opacity=0.2).move_to([x + dx, 1.45, 0]) for dx in (-0.6, 0.0, 0.6)])
            return VGroup(a, bars)

        def icon_pool(x):
            box = RoundedRectangle(corner_radius=0.25, width=1.8, height=1.5, stroke_color=TEAL, stroke_width=3,
                                   fill_color=TEAL, fill_opacity=0.1).move_to([x, 1.45, 0])
            d = DoubleArrow([x - 1.7, 1.45, 0], [x - 0.9, 1.45, 0], buff=0, color=TEAL, stroke_width=5, tip_length=0.2)
            return VGroup(box, d)

        icons = [icon_counter(XS[0]), icon_cross(XS[1]), icon_pool(XS[2])]
        names = [T("countercurrent", 26, TEXT), T("crosscurrent", 26, TEXT), T("mixed pool", 26, TEXT)]
        subs = [T("teleost gill", 22, GREY), T("bird lung", 22, GREY), T("mammal lung", 22, GREY)]
        for n, s, x in zip(names, subs, XS):
            n.move_to([x, 0.35, 0])
            s.next_to(n, DOWN, buff=0.1)

        self.at("Johan's")
        self.play(FadeIn(head), FadeIn(who), run_time=0.6)
        self.at("these three arrangements")
        self.play(*[FadeIn(i) for i in icons], *[FadeIn(n) for n in names], *[FadeIn(s) for s in subs], run_time=1.0)

        base = -2.9
        hs = [2.0, 1.3, 0.6]
        bars = [bar(x, base, h, w=1.2, color=YELLOW, op=0.5) for x, h in zip(XS, hs)]
        tags = [T("most", 24, YELLOW), T("next", 24, YELLOW), T("least", 24, YELLOW)]
        for t, b in zip(tags, bars):
            t.next_to(b, UP, buff=0.1)
        axl = T("gas transferred, by their measure", 24, YELLOW).move_to([0, -3.3, 0])
        self.at("By their measure")
        self.play(FadeIn(axl), run_time=0.5)
        self.at("the most gas")
        self.play(FadeIn(bars[0], shift=UP * 0.2), FadeIn(tags[0]), run_time=0.7)
        self.at("Crosscurrent came next")
        self.play(FadeIn(bars[1], shift=UP * 0.2), FadeIn(tags[1]), run_time=0.7)
        self.at("the least")
        self.play(FadeIn(bars[2], shift=UP * 0.2), FadeIn(tags[2]), run_time=0.7)
        note = T("a ranking of arrangements, not of animals", 26, TEXT).move_to([0, -0.9, 0])
        self.at("ranks arrangements")
        self.play(FadeIn(note), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "How two streams flow past each other changes gas exchange."
