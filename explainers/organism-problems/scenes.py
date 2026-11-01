"""Organism problems: every exchange surface has a cost  (Biochemistrypedia explainer)

COLOR MAP (one colour per concept, whole film)
  GREEN  = carbon / gas taken in (CO2 in the leaf, oxygen in the lung)
  BLUE   = water / water vapour lost
  PURPLE = stomata and guard cells (and stomatal density)
  YELLOW = the efficiency ratio and the answers drawn from it
  RED    = caution (not proof) and the claim that is wrong
  GREY   = outlines, waxy layer, chest, leaf cells, labels
  GOLD   = title rule only
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
CO2 = "C O₂"


def arr(a, b, color=GREY, w=6, tip=0.25):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def box(w, h, color=GREY, fill=0.0, r=0.12, sw=3):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill)


def mchip(text, color, size=26, pad=0.22):
    """chip with a multi-line label"""
    lab = T(text, size=size, color=color, line_spacing=0.9)
    b = box(lab.width + 2 * pad, lab.height + 2 * pad, color, 0.14, r=0.16, sw=2.5)
    return VGroup(b, lab.move_to(b))


class Stoma(VGroup):
    """Block cross-section of a leaf surface: waxy layer with one pore between two guard cells,
    leaf cells below. Not to scale. s = overall scale, cx, cy = centre of the waxy layer."""

    def __init__(self, cx=0, cy=0, s=1.0, half=5.5, depth=3.6, opened=True):
        super().__init__()
        self.s, self.cx, self.cy = s, cx, cy
        self.open_half = 0.5 * s
        self.wax_h = 0.34 * s
        gx = 1.3 * s
        L = (half - 1.3) * s
        self.wax_l = box(L, self.wax_h, GREY, 0.45, r=0.05).move_to([cx - gx - L / 2, cy, 0])
        self.wax_r = box(L, self.wax_h, GREY, 0.45, r=0.05).move_to([cx + gx + L / 2, cy, 0])
        self.inner = box(2 * half * s, depth * s, GREY, 0.07, r=0.05, sw=2.5).move_to(
            [cx, cy - self.wax_h / 2 - depth * s / 2, 0])
        gw, gh = 0.8 * s, 0.95 * s
        gap = self.open_half if opened else 0.02
        self.gl = box(gw, gh, PURPLE, 0.45, r=0.3 * s).move_to([cx - gap - gw / 2, cy - 0.25 * s, 0])
        self.gr = box(gw, gh, PURPLE, 0.45, r=0.3 * s).move_to([cx + gap + gw / 2, cy - 0.25 * s, 0])
        self.add(self.inner, self.wax_l, self.wax_r, self.gl, self.gr)

    def close_anims(self):
        gw = 0.8 * self.s
        return [self.gl.animate.move_to([self.cx - 0.02 - gw / 2, self.gl.get_center()[1], 0]),
                self.gr.animate.move_to([self.cx + 0.02 + gw / 2, self.gr.get_center()[1], 0])]


class S00Title(TitleCard):
    LESSON = "What an organism has to do"
    TITLE = "Every exchange surface has a cost"


# ---------------------------------------------------------------------------------------------
class S01Pore(SpokenScene):
    def construct(self):
        head = T("Barley leaf, block cross-section (not to scale)", 26, GREY).to_edge(UP, buff=0.35)
        st = Stoma(0, 0.7, 1.0, opened=True)
        self.play(FadeIn(head), FadeIn(st.inner), FadeIn(st.wax_l), FadeIn(st.wax_r), run_time=0.9)
        wax = T("waxy layer", 26, GREY).move_to([-4.2, 1.5, 0])
        cells = T("leaf cells", 26, GREY).move_to([0, -1.9, 0])
        self.play(FadeIn(wax), FadeIn(cells), FadeIn(st.gl), FadeIn(st.gr), run_time=0.7)
        self.at("The gas enters")
        a_in = arr([-0.25, 2.95, 0], [-0.25, -0.8, 0], GREEN)
        l_in = T(f"{CO2} in", 30, GREEN).move_to([-2.2, 2.6, 0])
        self.play(GrowArrow(a_in), FadeIn(l_in), run_time=0.9)
        self.at("tiny pores")
        gl = T("guard cells around the pore", 26, PURPLE).move_to([3.7, 1.75, 0])
        gline = Line([2.4, 1.5, 0], [1.4, 0.75, 0], color=PURPLE, stroke_width=2)
        self.play(FadeIn(gl), Create(gline), Indicate(VGroup(st.gl, st.gr), color=PURPLE, scale_factor=1.06), run_time=0.9)
        self.at("leaves through")
        a_out = arr([0.25, -0.8, 0], [0.25, 2.95, 0], BLUE)
        l_out = T("water vapour out", 30, BLUE).move_to([3.1, 2.7, 0])
        self.play(GrowArrow(a_out), FadeIn(l_out), run_time=0.9)
        self.at("very same pores")
        self.play(Indicate(VGroup(st.gl, st.gr), color=PURPLE, scale_factor=1.06), run_time=0.8)
        self.at("both things happen")
        self.play(Indicate(a_in, color=GREEN, scale_factor=1.1), Indicate(a_out, color=BLUE, scale_factor=1.1), run_time=0.9)
        self.finish()


class S02Lung(SpokenScene):
    def construct(self):
        # carried over from scene 1, rebuilt smaller on the left
        st = Stoma(-3.6, 0.6, 0.55, half=5.5 * 0.9, depth=5.6, opened=True)
        a_in = arr([-3.85, 3.0, 0], [-3.85, 0.1, 0], GREEN, w=5)
        a_out = arr([-3.35, 0.1, 0], [-3.35, 3.0, 0], BLUE, w=5)
        lab_l = T("barley leaf", 28, GREY).move_to([-3.6, 3.35, 0])
        self.add(st, a_in, a_out, lab_l)
        self.at("An adult human lung")
        chest = box(5.4, 6.2, GREY, 0.0, r=0.3).move_to([3.6, -0.1, 0])
        chest_l = T("chest, not to scale", 24, GREY).move_to([3.6, -2.7, 0])
        lung = box(4.6, 4.4, GREY, 0.07, r=0.25).move_to([3.6, 0.2, 0])
        lung_l = T("lung", 26, GREY).move_to([3.6, 2.0, 0])
        who = T("adult human", 28, GREY).move_to([3.6, 3.35, 0])
        self.play(FadeIn(who), Create(chest), FadeIn(chest_l), run_time=0.8)
        self.play(Create(lung), FadeIn(lung_l), run_time=0.7)
        self.at("dissolve in a thin")
        film = box(3.8, 0.38, BLUE, 0.35, r=0.1).move_to([3.6, -1.15, 0])
        film_l = T("thin, wet film", 24, BLUE).move_to([3.6, -1.75, 0])
        self.play(FadeIn(film), FadeIn(film_l), run_time=0.7)
        self.at("diffuse into cells")
        g_in = arr([2.4, 0.4, 0], [2.4, -0.95, 0], GREEN)
        g_l = T("oxygen in", 24, GREEN).move_to([2.4, 0.8, 0])
        self.play(GrowArrow(g_in), FadeIn(g_l), run_time=0.8)
        self.at("loses water by evaporation")
        w_out = arr([4.9, -0.95, 0], [4.9, 0.4, 0], BLUE)
        w_l = T("water\nvapour out", 24, BLUE, line_spacing=0.9).move_to([4.9, 0.85, 0])
        self.play(GrowArrow(w_out), FadeIn(w_l), run_time=0.8)
        self.at("each breath")
        self.play(Indicate(w_out, color=BLUE, scale_factor=1.12), run_time=0.8)
        self.at("A stoma can close")
        self.play(FadeOut(a_in), FadeOut(a_out), *st.close_anims(), run_time=0.9)
        can = T("can close", 28, PURPLE).move_to([-3.6, -2.9, 0])
        self.play(FadeIn(can), run_time=0.4)
        self.at("cannot close")
        no = T("cannot close", 24, RED).move_to([3.6, 1.55, 0])
        self.play(FadeIn(no), run_time=0.5)
        self.finish()


def ratio_text(top="carbon gained", bot="water lost", size=30):
    t = T(top, size, GREEN)
    b = T(bot, size, BLUE)
    ln = Line(LEFT * max(t.width, b.width) / 2, RIGHT * max(t.width, b.width) / 2, color=YELLOW, stroke_width=4)
    g = VGroup(t, ln, b).arrange(DOWN, buff=0.12)
    return g


def leaf_card(name, carbon, water, x, eff_text, res, color=YELLOW, y0=2.7):
    title = T(name, 30, GREY, weight=BOLD).move_to([x, y0, 0])
    c = mchip(carbon, GREEN, 26).move_to([x, y0 - 1.1, 0])
    w = mchip(water, BLUE, 26).move_to([x, y0 - 2.2, 0])
    res_t = VGroup(T(eff_text, 30, YELLOW), T(res, 24, YELLOW)).arrange(DOWN, buff=0.1).move_to([x, y0 - 3.4, 0])
    return title, c, w, res_t


class S03Ratio(SpokenScene):
    def construct(self):
        q = T("What does the exchange cost?", 36, font=TITLE_FONT).move_to([0, 2.9, 0])
        self.play(Write(q), run_time=1.2)
        self.at("Divide the carbon gained")
        eq = T("water-use efficiency  =", 34, YELLOW)
        fr = ratio_text(size=34)
        grp = VGroup(eq, fr).arrange(RIGHT, buff=0.4).move_to([0, 1.3, 0])
        self.play(FadeOut(q), run_time=0.4)
        self.play(FadeIn(fr, shift=UP * 0.1), run_time=0.9)
        self.at("This is called")
        self.play(FadeIn(eq, shift=RIGHT * 0.1), run_time=0.7)
        self.at("Here are two")
        tA = T("Leaf A: made-up numbers, not barley data", 28, GREY, weight=BOLD).move_to([0, -0.2, 0])
        self.play(FadeIn(tA), run_time=0.6)
        self.at("Leaf A gains")
        c = mchip(f"gains 20 µmol {CO2}  per m² per s", GREEN, 28).move_to([-3.4, -1.3, 0])
        self.play(FadeIn(c, shift=UP * 0.1), run_time=0.7)
        self.at("and loses")
        w = mchip("loses 5 mmol H₂O  per m² per s", BLUE, 28).move_to([3.4, -1.3, 0])
        self.play(FadeIn(w, shift=UP * 0.1), run_time=0.7)
        self.at("Its efficiency is")
        res = T("20 / 5  =  4.0", 44, YELLOW, weight=BOLD).move_to([0, -2.45, 0])
        unit = T(f"µmol {CO2} per mmol H₂O", 26, YELLOW).move_to([0, -3.1, 0])
        self.play(FadeIn(res, scale=1.1), run_time=0.7)
        self.play(FadeIn(unit), run_time=0.4)
        self.finish()


class S04Leafb(SpokenScene):
    def construct(self):
        xa, xb = -3.5, 3.5
        tA, cA, wA, rA = leaf_card("Leaf A", "gains 20", "loses 5", xa, "20 / 5 = 4.0", "µmol per mmol", y0=3.0)
        # keep the units visible by label under the pair
        cA = mchip(f"gains 20 µmol {CO2}", GREEN, 28).move_to([xa, 1.9, 0])
        wA = mchip("loses 5 mmol H₂O", BLUE, 28).move_to([xa, 0.95, 0])
        rA = T("20 / 5  =  4.0", 40, YELLOW, weight=BOLD).move_to([xa, -0.05, 0])
        self.add(tA, cA, wA, rA)
        self.at("Leaf B has fewer")
        tB = T("Leaf B: fewer stomata", 30, PURPLE, weight=BOLD).move_to([xb, 3.0, 0])
        note = T("made-up numbers, not barley data; rates are per m² per s", 22, GREY).move_to([0, -3.4, 0])
        self.play(FadeIn(tB), FadeIn(note), run_time=0.6)
        self.at("It gains")
        cB = mchip(f"gains 16 µmol {CO2}", GREEN, 28).move_to([xb, 1.9, 0])
        wB = mchip("loses 3 mmol H₂O", BLUE, 28).move_to([xb, 0.95, 0])
        self.play(FadeIn(cB, shift=UP * 0.1), FadeIn(wB, shift=UP * 0.1), run_time=0.8)
        self.at("so its efficiency")
        rB = T("16 / 3  =  5.3", 40, YELLOW, weight=BOLD).move_to([xb, -0.05, 0])
        self.play(FadeIn(rB, scale=1.1), run_time=0.7)
        self.at("less carbon")
        lc = T("carbon: 0.8 of A, 20% less", 26, GREEN).move_to([xb, -1.05, 0])
        self.play(FadeIn(lc, shift=UP * 0.1), run_time=0.6)
        self.at("less water")
        lw = T("water: 0.6 of A, 40% less", 26, BLUE).move_to([xb, -1.65, 0])
        self.play(FadeIn(lw, shift=UP * 0.1), run_time=0.6)
        self.at("Neither leaf is better everywhere")
        mid = T("neither leaf is better everywhere", 28, YELLOW).move_to([0, -2.7, 0])
        self.play(FadeOut(lc), FadeOut(lw), run_time=0.5)
        self.play(FadeIn(mid), run_time=0.6)
        self.at("When water is scarce")
        bcase = T("water is scarce:\nB keeps more water\nper unit of carbon", 26, YELLOW, line_spacing=0.9).move_to([xb, -1.4, 0])
        self.play(FadeIn(bcase, shift=UP * 0.1), run_time=0.7)
        self.at("When water is plentiful")
        acase = T("water is plentiful and\ncarbon limits growth:\nA gains more", 26, YELLOW, line_spacing=0.9).move_to([xa, -1.4, 0])
        self.play(FadeIn(acase, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S05Barley(SpokenScene):
    def construct(self):
        q = mchip("fewer stomata  →  less grain?", YELLOW, 32).move_to([0, 3.0, 0])
        self.at("You might expect")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)
        self.at("tested this in barley")
        gene = mchip("barley lines making more of one gene's product:\nfewer stomata develop", PURPLE, 26).move_to([0, 3.0, 0])
        self.play(ReplacementTransform(q, gene), run_time=0.9)
        # bars
        base_y, H = -3.0, 3.7
        title = T("stomatal density, mature sixth leaf (% of control)", 24, GREY).move_to([-3.0, 1.45, 0])
        def bar(x, pct, lab, col):
            h = H * pct / 100
            b = Rectangle(width=1.3, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.4)
            b.move_to([x, base_y + h / 2, 0])
            l = T(lab, 24, GREY).move_to([x, base_y - 0.3, 0])
            return b, l
        self.at("In the mature sixth leaf")
        b0, l0 = bar(-5.2, 100, "control", GREY)
        v0 = T("100%", 26, GREY).next_to(b0, UP, buff=0.1)
        # density axis only needs 100% -> shorten so title fits above
        self.play(FadeIn(title), GrowFromEdge(b0, DOWN), FadeIn(l0), FadeIn(v0), run_time=0.9)
        self.at("two lines kept")
        b1, l1 = bar(-3.3, 24, "line 1", PURPLE)
        b2, l2 = bar(-1.4, 12, "line 2", PURPLE)
        v1 = T("about 24%", 24, PURPLE).next_to(b1, UP, buff=0.1)
        v2 = T("about 12%", 24, PURPLE).next_to(b2, UP, buff=0.1)
        self.play(GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(l1), FadeIn(l2), run_time=0.9)
        self.play(FadeIn(v1), FadeIn(v2), run_time=0.4)
        self.at("Gas exchange fell")
        c1 = mchip("gas exchange fell\nin well-watered plants", BLUE, 26).move_to([3.6, 1.45, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.at("plants per group")
        c2 = mchip("greenhouse grain yield: no\nstatistically significant drop\nunder either watering treatment\n(5 plants per group)", GREEN, 24).move_to([3.6, -0.55, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.8)
        self.at("does not prove")
        c3 = mchip("not proof the yields are equal:\nno loss was detected", RED, 26).move_to([3.6, -2.35, 0])
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        t = T("Why does a structure usually fit what it does?", 34, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("Why does a structure")
        self.play(Write(t), run_time=1.6)
        self.at("A sound claim")
        good = mchip("Lineages with fewer stomata lost less water\nand left more descendants in dry places", GREEN, 32).move_to([0, 1.5, 0])
        self.play(FadeIn(good, shift=UP * 0.1), run_time=0.9)
        self.at("shorthand")
        bad = mchip("\"Barley has fewer stomata to save water\":\nshorthand that hides the history", YELLOW, 28).move_to([0, 0.15, 0])
        self.play(FadeIn(bad, shift=UP * 0.1), run_time=0.7)
        self.at("links two traits")
        a = mchip(f"more stomata: more {CO2} in", GREEN, 28).move_to([-3.4, -1.45, 0])
        b = mchip("more water out", BLUE, 28).move_to([4.0, -1.45, 0])
        lk = DoubleArrow(a.get_right() + RIGHT * 0.1, b.get_left() + LEFT * 0.1, buff=0, color=YELLOW, stroke_width=6,
                         tip_length=0.25)
        self.play(FadeIn(a), FadeIn(b), run_time=0.6)
        self.play(GrowFromCenter(lk), run_time=0.6)
        self.at("Improving one worsens")
        trl = T("a trade-off: improving one worsens the other", 26, YELLOW).move_to([0, -2.35, 0])
        self.play(FadeIn(trl), run_time=0.6)
        self.at("Every exchange surface")
        rule = T("Every exchange surface carries a cost.", 36, font=TITLE_FONT, color=GOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Every exchange surface carries a cost."
