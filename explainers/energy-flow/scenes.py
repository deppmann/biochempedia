"""Energy flow and productivity: where all the energy goes (Biochemistrypedia explainer)

Every number is the lesson's own made-up closed budget for one square metre over one year,
in kJ per m^2 per year. Nothing here is a data set; the ten-percent bars are arithmetic only.

COLOR MAP (one color per concept, whole video)
  YELLOW = sunlight / gross primary production (the energy fixed)
  GREEN  = production: net primary production and new consumer tissue
  BLUE   = consumers and what they ingest
  RED    = respiration, energy leaving as heat
  ORANGE = detritus and everything that flows into it (feces, dead matter)
  TEAL   = decomposers
  PURPLE = efficiencies (ratios)
  GREY   = outlines, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
UNIT = "kJ per m² per year · made-up budget"


def box(label, color, pos, w=2.7, h=1.3, size=28):
    r = RoundedRectangle(corner_radius=0.16, width=w, height=h, stroke_color=color, stroke_width=3.5,
                         fill_color=color, fill_opacity=0.18)
    t = T(label, size, color)
    g = VGroup(r, t).move_to(pos)
    return g


def arr(a, b, color=GREY, w=6):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def num(text, color, size=28):
    return M(text, size, color, weight=BOLD)


def lab(name, number, color, size=24, direction=DOWN, buff=0.04, align=ORIGIN):
    """two-line label: number over name."""
    g = VGroup(num(number, color, size + 2), T(name, size - 2, color)).arrange(direction, buff=buff)
    return g


def seg(x0, width, y, h, color, op=0.45):
    return Rectangle(width=width, height=h, stroke_color=color, stroke_width=3, fill_color=color,
                     fill_opacity=op).move_to([x0 + width / 2, y, 0])


def unit_note():
    return T(UNIT, 22, GREY).move_to([-3.9, -3.3, 0])


class S00Title(TitleCard):
    LESSON = "Energy flow and productivity"
    TITLE = "Where all the energy goes"


# ---------------------------------------------------------------------------------------------
def stage1():
    """end state of scene 1, rebuilt at the start of scene 2."""
    P = box("Producers", GREEN, [0, 0.2, 0], w=3.6, h=1.6, size=34)
    sun = Circle(radius=0.32, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([0, 3.0, 0])
    sun_l = T("sunlight", 24, YELLOW).next_to(sun, LEFT, buff=0.25)
    sun_a = arr([0, 2.6, 0], [0, 1.02, 0], YELLOW, 7)
    gpp = VGroup(num("12,000", YELLOW, 32), T("gross primary production", 24, YELLOW)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
    gpp.next_to(sun_a, RIGHT, buff=0.3).shift(UP * 0.05)
    heat_a = arr([1.85, 0.2, 0], [4.6, 0.2, 0], RED, 7)
    heat_l = VGroup(num("6,000", RED, 30), T("respired, lost as heat", 24, RED)).arrange(DOWN, buff=0.05).next_to(heat_a, UP, buff=0.12).shift(RIGHT * 0.55)
    npp_a = arr([0, -0.62, 0], [0, -2.2, 0], GREEN, 7)
    npp_l = VGroup(num("6,000", GREEN, 30), T("net primary production", 24, GREEN)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
    npp_l.next_to(npp_a, RIGHT, buff=0.3)
    sun_all = VGroup(sun, sun_l, sun_a, gpp)
    return P, sun, sun_l, sun_a, gpp, heat_a, heat_l, npp_a, npp_l


class S01Fix(SpokenScene):
    def construct(self):
        P, sun, sun_l, sun_a, gpp, heat_a, heat_l, npp_a, npp_l = stage1()
        self.at("Plants often respire")
        self.play(FadeIn(P, scale=0.9), run_time=0.8)
        self.at("one year")
        unit = unit_note()
        self.play(FadeIn(unit), run_time=0.5)
        self.at("producers fix")
        self.play(FadeIn(sun), FadeIn(sun_l), run_time=0.4)
        self.play(GrowArrow(sun_a), run_time=0.6)
        self.play(FadeIn(gpp, shift=RIGHT * 0.2), run_time=0.5)
        self.at("gross primary production")
        self.play(Indicate(gpp, color=YELLOW, scale_factor=1.08), run_time=0.8)
        self.at("producers respire")
        self.play(GrowArrow(heat_a), run_time=0.7)
        self.play(FadeIn(heat_l, shift=UP * 0.1), run_time=0.4)
        self.at("what is left")
        self.play(GrowArrow(npp_a), run_time=0.6)
        self.play(FadeIn(npp_l, shift=RIGHT * 0.2), run_time=0.4)
        self.at("net primary production")
        self.play(Indicate(npp_l, color=GREEN, scale_factor=1.08), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
PX, HX, RX = -3.7, 3.7, 4.7
ROW = 1.0
DPOS = [0.0, -1.9, 0]


def layout_p():
    return box("Producers", GREEN, [PX, ROW, 0], w=3.3, h=1.5)


def layout_heat(b, text, up=0.9):
    a = arr(b.get_top(), b.get_top() + UP * up, RED, 6)
    l = VGroup(num(text, RED, 26), T("heat", 24, RED)).arrange(RIGHT, buff=0.15).next_to(a, UP, buff=0.1)
    return a, l


class S02Graze(SpokenScene):
    def construct(self):
        P, sun, sun_l, sun_a, gpp, heat_a, heat_l, npp_a, npp_l = stage1()
        unit = unit_note()
        self.add(P, sun, sun_l, sun_a, gpp, heat_a, heat_l, npp_a, npp_l, unit)
        Pn = layout_p()
        ha, hl = layout_heat(Pn, "6,000")
        self.at("Now herbivores eat")
        H = box("Herbivores", BLUE, [HX, ROW, 0], w=3.3, h=1.5)
        self.play(FadeOut(VGroup(sun, sun_l, sun_a, gpp, npp_a, npp_l)),
                  ReplacementTransform(P, Pn),
                  ReplacementTransform(VGroup(heat_a, heat_l), VGroup(ha, hl)), run_time=1.0)
        self.play(FadeIn(H, shift=LEFT * 0.3), run_time=0.6)
        self.at("ingest")
        a1 = arr([PX + 1.7, ROW, 0], [HX - 1.7, ROW, 0], BLUE, 7)
        l1 = VGroup(num("1,800", BLUE, 28), T("ingested", 22, BLUE)).arrange(DOWN, buff=0.04).next_to(a1, UP, buff=0.1)
        # keep label inside gap between the boxes
        self.play(GrowArrow(a1), FadeIn(l1), run_time=0.7)
        self.at("net primary production")
        pct = T("30% of the NPP", 24, PURPLE).next_to(a1, DOWN, buff=0.25)
        self.play(FadeIn(pct, shift=UP * 0.1), run_time=0.5)
        self.at("never grazed")
        D = box("Detritus", ORANGE, DPOS, w=3.2, h=1.4)
        a2 = arr([PX, ROW - 0.8, 0], [-1.65, DPOS[1] + 0.15, 0], ORANGE, 7)
        l2 = VGroup(num("4,200", ORANGE, 28), T("never grazed", 22, ORANGE)).arrange(DOWN, buff=0.04).move_to([-4.5, -0.9, 0])
        self.play(GrowArrow(a2), FadeIn(l2), run_time=0.7)
        self.at("enters detritus")
        self.play(FadeIn(D, scale=0.9), run_time=0.5)
        self.at("dead matter")
        self.play(Indicate(D, color=ORANGE, scale_factor=1.06), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
def effic(big, small, color=PURPLE, size=40):
    return VGroup(num(big, color, size), T(small, 22, color)).arrange(DOWN, buff=0.06)


class S03Herb(SpokenScene):
    def construct(self):
        unit = unit_note()
        K = 0.0018
        x0 = -5.4
        top = seg(x0, 6000 * K, 2.55, 0.8, GREEN, 0.35)
        top_l = VGroup(T("net primary production", 24, GREEN), num("6,000", GREEN, 28)).arrange(RIGHT, buff=0.2).next_to(top, UP, buff=0.18)
        self.at("Follow the herbivores")
        self.play(FadeIn(top), FadeIn(top_l), FadeIn(unit), run_time=0.7)
        slice_ = seg(x0, 1800 * K, 2.55, 0.8, BLUE, 0.6)
        self.at("They ingest")
        self.play(FadeIn(slice_), run_time=0.4)
        k2 = 0.006
        yb = 0.35
        bar = seg(x0, 1800 * k2, yb, 1.1, BLUE, 0.5)
        ing_l = VGroup(T("ingested", 24, BLUE), num("1,800", BLUE, 28)).arrange(RIGHT, buff=0.2).next_to(bar, UP, buff=0.3)
        self.play(ReplacementTransform(slice_.copy(), bar), run_time=0.9)
        self.play(FadeIn(ing_l), run_time=0.4)
        self.wait(0.2)
        # egest
        self.at("egest")
        egw, rsw, pdw = 1080 * k2, 360 * k2, 360 * k2
        eg = seg(x0, egw, yb, 1.1, ORANGE, 0.5)
        rest = seg(x0 + egw, rsw + pdw, yb, 1.1, BLUE, 0.5)
        self.play(ReplacementTransform(bar, VGroup(eg, rest)), run_time=0.8)
        eg_l = lab("egested as feces", "1,080", ORANGE).next_to(eg, DOWN, buff=0.2)
        self.play(FadeIn(eg_l), run_time=0.4)
        self.at("assimilated")
        br = Brace(rest, UP, color=BLUE, buff=0.1)
        as_l = VGroup(T("assimilated", 24, BLUE), num("720", BLUE, 28)).arrange(RIGHT, buff=0.2).next_to(br, UP, buff=0.1)
        self.play(FadeOut(ing_l), GrowFromCenter(br), run_time=0.5)
        self.play(FadeIn(as_l), run_time=0.4)
        self.at("respire")
        rs = seg(x0 + egw, rsw, yb, 1.1, RED, 0.5)
        pd = seg(x0 + egw + rsw, pdw, yb, 1.1, BLUE, 0.5)
        self.play(ReplacementTransform(rest, VGroup(rs, pd)), run_time=0.7)
        rs_l = lab("respired", "360", RED).next_to(rs, DOWN, buff=0.2)
        self.play(FadeIn(rs_l), run_time=0.4)
        self.at("new tissue")
        self.play(pd.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), run_time=0.5)
        pd_l = lab("production", "360", GREEN).next_to(pd, DOWN, buff=0.2)
        self.play(FadeIn(pd_l), run_time=0.4)
        self.at("three efficiencies")
        e1 = effic("30%", "consumption")
        e2 = effic("40%", "assimilation")
        e3 = effic("50%", "net production")
        eq = effic("6%", "transfer efficiency", color=PURPLE, size=48)
        t1, t2, t3 = M("×", 36, GREY), M("×", 36, GREY), M("=", 36, GREY)
        row = VGroup(e1, t1, e2, t2, e3, t3, eq).arrange(RIGHT, buff=0.4)
        fit(row, max_w=12.2)
        row.move_to([0.2, -2.4, 0])
        for part in (e1, e2, e3):
            self.play(FadeIn(part, shift=UP * 0.1), run_time=0.35)
            if part is e1:
                self.play(FadeIn(t1), run_time=0.1)
            elif part is e2:
                self.play(FadeIn(t2), run_time=0.1)
        self.at("Multiplied")
        self.play(FadeIn(t3), FadeIn(eq, scale=0.8), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Pred(SpokenScene):
    def construct(self):
        unit = unit_note()
        K = 0.03
        x0 = -5.4
        yt = 2.4
        top = seg(x0, 360 * K, yt, 0.8, GREEN, 0.4)
        top_l = VGroup(T("herbivore production", 24, GREEN), num("360", GREEN, 28)).arrange(RIGHT, buff=0.2).next_to(top, UP, buff=0.18)
        self.at("Predators keep the same books")
        self.play(FadeIn(top), FadeIn(top_l), FadeIn(unit), run_time=0.7)
        sl = seg(x0, 200 * K, yt, 0.8, BLUE, 0.6)
        rm = seg(x0 + 200 * K, 160 * K, yt, 0.8, ORANGE, 0.5)
        self.at("they ingest")
        self.play(FadeIn(sl), run_time=0.4)
        sl_l = VGroup(T("ingested", 22, BLUE), num("200", BLUE, 26)).arrange(RIGHT, buff=0.15).next_to(sl, DOWN, buff=0.15)
        self.play(FadeIn(sl_l), run_time=0.3)
        self.at("goes to detritus")
        self.play(FadeIn(rm), run_time=0.4)
        rm_l = VGroup(T("to detritus", 22, ORANGE), num("160", ORANGE, 26)).arrange(RIGHT, buff=0.15).next_to(rm, DOWN, buff=0.15)
        self.play(FadeIn(rm_l), run_time=0.3)
        yb = 0.2
        bar = seg(x0, 200 * K, yb, 1.1, BLUE, 0.5)
        self.play(ReplacementTransform(sl.copy(), bar), run_time=0.8)
        self.at("egest")
        egw, rsw, pdw = 100 * K, 60 * K, 40 * K
        eg = seg(x0, egw, yb, 1.1, ORANGE, 0.5)
        rest = seg(x0 + egw, rsw + pdw, yb, 1.1, BLUE, 0.5)
        self.play(ReplacementTransform(bar, VGroup(eg, rest)), run_time=0.7)
        eg_l = lab("egested", "100", ORANGE).next_to(eg, DOWN, buff=0.2)
        self.play(FadeIn(eg_l), run_time=0.3)
        self.at("respire")
        rs = seg(x0 + egw, rsw, yb, 1.1, RED, 0.5)
        pd = seg(x0 + egw + rsw, pdw, yb, 1.1, BLUE, 0.5)
        self.play(ReplacementTransform(rest, VGroup(rs, pd)), run_time=0.6)
        rs_l = lab("respired", "60", RED).next_to(rs, DOWN, buff=0.2)
        self.play(FadeIn(rs_l), run_time=0.3)
        self.at("Their production is")
        self.play(pd.animate.set_stroke(GREEN).set_fill(GREEN, 0.5), run_time=0.4)
        pd_l = lab("production", "40", GREEN).next_to(pd, DOWN, buff=0.2).shift(RIGHT * 0.25)
        self.play(FadeIn(pd_l), run_time=0.3)
        self.at("transfer efficiency")
        second = VGroup(num("11%", PURPLE, 52), T("second link: 40 / 360", 24, PURPLE)).arrange(DOWN, buff=0.08)
        first = VGroup(num("6%", PURPLE, 52), T("first link: 360 / 6,000", 24, PURPLE)).arrange(DOWN, buff=0.08)
        second.move_to([3.3, -2.2, 0]); first.move_to([-2.3, -2.2, 0])
        self.play(FadeIn(second, shift=UP * 0.1), run_time=0.6)
        self.at("first link")
        self.play(FadeIn(first, shift=UP * 0.1), run_time=0.6)
        self.at("no single number")
        self.play(Indicate(VGroup(first, second), color=PURPLE, scale_factor=1.05), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Detritus(SpokenScene):
    def construct(self):
        unit = unit_note()
        H = 4.4
        k = H / 5540.0
        tx0, tw = -0.3, 1.8
        tcx = tx0 + tw / 2
        ybot = -3.0
        LX = -1.5   # right edge of the left-hand labels
        tank = Rectangle(width=tw, height=H, stroke_color=ORANGE, stroke_width=3, fill_opacity=0).move_to([tcx, ybot + H / 2, 0])
        title = T("Detritus", 28, ORANGE).move_to([tcx, 1.95, 0])
        self.at("Now the detritus")
        self.play(Create(tank), FadeIn(title), FadeIn(unit), run_time=0.9)
        items = [("ungrazed plants", 4200, 0.55), ("herbivore feces", 1080, 0.35),
                 ("predator feces", 100, 0.55), ("uneaten animal production", 160, 0.28)]
        y = ybot
        stack = []
        labels = []
        label_y = [-1.4, 0.2, 1.0, 1.8]
        for (name, val, op), ly in zip(items, label_y):
            h = val * k
            s_ = Rectangle(width=tw, height=h, stroke_color=BG, stroke_width=2, fill_color=ORANGE, fill_opacity=op)
            s_.move_to([tcx, y + h / 2, 0])
            lbl = VGroup(T(name, 22, ORANGE), num(f"{val:,}", ORANGE, 24)).arrange(RIGHT, buff=0.15)
            lbl.move_to([0, ly, 0]).align_to([LX, 0, 0], RIGHT)
            ln = Line(lbl.get_right() + RIGHT * 0.1, [tx0, y + h / 2, 0], color=GREY, stroke_width=1.5)
            stack.append(s_); labels.append(VGroup(lbl, ln))
            y += h
        self.at("Ungrazed plants")
        self.play(FadeIn(stack[0], shift=DOWN * 0.1), FadeIn(labels[0]), run_time=0.8)
        self.at("feces")
        self.play(FadeIn(stack[1]), FadeIn(labels[1]), run_time=0.4)
        self.play(FadeIn(stack[2]), FadeIn(labels[2]), run_time=0.4)
        self.at("uneaten animal")
        self.play(FadeIn(stack[3]), FadeIn(labels[3]), run_time=0.5)
        self.at("Together they come to")
        tot = num("5,540", ORANGE, 30).move_to([tcx, 2.6, 0])
        self.play(FadeIn(tot, shift=DOWN * 0.1), run_time=0.5)
        self.at("The decomposers respire")
        hr, ho = 3240 * k, 2300 * k
        red = Rectangle(width=tw, height=hr, stroke_color=BG, stroke_width=2, fill_color=RED, fill_opacity=0.5).move_to([tcx, ybot + hr / 2, 0])
        org = Rectangle(width=tw, height=ho, stroke_color=BG, stroke_width=2, fill_color=ORANGE, fill_opacity=0.5).move_to([tcx, ybot + hr + ho / 2, 0])
        red_l = VGroup(T("decomposers respire", 22, TEAL), num("3,240", RED, 26), T("as heat", 22, RED)).arrange(DOWN, buff=0.06)
        red_l.move_to([0, ybot + hr / 2, 0]).align_to([LX, 0, 0], RIGHT)
        self.play(FadeOut(VGroup(*labels)), ReplacementTransform(VGroup(*stack), VGroup(red, org)), run_time=0.9)
        self.play(FadeIn(red_l), run_time=0.4)
        self.at("That leaves")
        org_l = lab("left as detritus", "2,300", ORANGE)
        org_l.move_to([0, ybot + hr + ho / 2, 0]).align_to([LX, 0, 0], RIGHT)
        self.play(FadeIn(org_l), run_time=0.5)
        self.at("more than every animal")
        kk = 0.0011
        xr = 2.0
        d_bar = Rectangle(width=3240 * kk, height=0.7, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.5).move_to([xr + 3240 * kk / 2, 0.8, 0])
        a_bar = Rectangle(width=420 * kk, height=0.7, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.5).move_to([xr + 420 * kk / 2, -0.8, 0])
        d_l = VGroup(T("decomposers", 24, TEAL), num("3,240", RED, 26)).arrange(RIGHT, buff=0.2).next_to(d_bar, UP, buff=0.12, aligned_edge=LEFT)
        a_l = VGroup(T("herbivores + predators", 24, BLUE), num("360 + 60 = 420", RED, 26)).arrange(DOWN, buff=0.04, aligned_edge=LEFT).next_to(a_bar, UP, buff=0.12, aligned_edge=LEFT)
        self.play(GrowFromEdge(d_bar, LEFT), FadeIn(d_l), run_time=0.8)
        self.play(GrowFromEdge(a_bar, LEFT), FadeIn(a_l), run_time=0.8)
        self.at("most net primary production")
        most = VGroup(T("most NPP never passed", 26, ORANGE), T("through an animal", 26, ORANGE)).arrange(DOWN, buff=0.08)
        most.move_to([4.2, -2.3, 0])
        self.play(FadeIn(most, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Ledger(SpokenScene):
    def construct(self):
        unit = unit_note()
        W = 11.0
        k = W / 12000.0
        x0 = -5.5
        yb = 0.5
        bh = 1.2
        self.at("Now add it up")
        full = Rectangle(width=W, height=bh, stroke_color=YELLOW, stroke_width=3, fill_opacity=0).move_to([0, yb, 0])
        full_l = VGroup(T("fixed", 26, YELLOW), num("12,000", YELLOW, 30)).arrange(RIGHT, buff=0.2).next_to(full, UP, buff=0.65).shift(LEFT * 2.0)
        br_full = Brace(full, UP, color=YELLOW, buff=0.1)
        self.play(Create(full), FadeIn(unit), run_time=0.7)
        self.play(GrowFromCenter(br_full), FadeIn(full_l), run_time=0.6)
        self.at("Respiration totals")
        parts = [6000, 360, 60, 3240]
        x = x0
        red = []
        for p in parts:
            s = seg(x, p * k, yb, bh, RED, 0.5)
            s.set_stroke(BG, 2)
            red.append(s); x += p * k
        self.play(LaggedStart(*[FadeIn(s) for s in red], lag_ratio=0.3), run_time=1.4)
        brr = Brace(VGroup(*red), DOWN, color=RED, buff=0.1)
        rr = VGroup(T("respired", 26, RED), num("9,660", RED, 30)).arrange(RIGHT, buff=0.2).next_to(brr, DOWN, buff=0.1)
        sm = num("6,000 + 360 + 60 + 3,240", RED, 24).next_to(rr, DOWN, buff=0.12)
        self.play(GrowFromCenter(brr), FadeIn(rr), FadeIn(sm), run_time=0.7)
        self.at("net ecosystem production")
        o = seg(x, 2300 * k, yb, bh, ORANGE, 0.5); o.set_stroke(BG, 2)
        x2 = x + 2300 * k
        g = seg(x2, 40 * k, yb, bh, GREEN, 0.9); g.set_stroke(GREEN, 3)
        self.play(FadeIn(o), FadeIn(g), run_time=0.7)
        brn = Brace(VGroup(o, g), DOWN, color=GREEN, buff=0.1)
        nep = VGroup(T("net ecosystem", 24, GREEN), T("production", 24, GREEN), num("2,340", GREEN, 30)).arrange(DOWN, buff=0.04)
        nep.next_to(brn, DOWN, buff=0.1).shift(LEFT * 0.0)
        nep.set_x(4.55)
        self.play(GrowFromCenter(brn), FadeIn(nep), run_time=0.7)
        self.at("That is the detritus")
        o_l = lab("detritus", "2,300", ORANGE, 22).move_to([3.3, yb + 1.45, 0])
        g_l = lab("predators", "+ 40", GREEN, 22).move_to([5.0, yb + 1.45, 0])
        self.play(FadeIn(o_l), FadeIn(g_l), run_time=0.6)
        self.at("The ledger closes")
        closes = T("the ledger closes", 30, TEXT).move_to([0, -2.6, 0])
        self.play(FadeIn(closes), Indicate(full, color=YELLOW, scale_factor=1.03), run_time=0.9)
        # ten percent sketch
        self.at("Suppose each step")
        everything = VGroup(full, full_l, br_full, *red, brr, rr, sm, o, g, brn, nep, o_l, g_l, closes)
        self.play(FadeOut(everything), run_time=0.6)
        head = T("if each step passed on 10%", 30, PURPLE).move_to([0, 2.7, 0])
        note = T("arithmetic, not data", 22, GREY).next_to(head, DOWN, buff=0.12)
        self.play(FadeIn(head), FadeIn(note), run_time=0.5)
        rows = []
        vals = [("level 1: NPP", 100.0, "100%"), ("level 2", 10.0, "10%"), ("level 3", 1.0, "1%"), ("level 4", 0.1, "0.1%")]
        x0b = -2.4
        sc = 6.5 / 100.0
        grp = VGroup()
        for i, (nm, v, txt) in enumerate(vals):
            y = 1.1 - i * 0.95
            lb = T(nm, 24, TEXT).move_to([-4.6, y, 0]); lb.align_to([-6.3, 0, 0], LEFT)
            bar = Rectangle(width=max(v * sc, 0.03), height=0.6, stroke_color=PURPLE, stroke_width=2, fill_color=PURPLE, fill_opacity=0.55)
            bar.move_to([x0b + max(v * sc, 0.03) / 2, y, 0])
            vl = num(txt, PURPLE, 26).next_to(bar, RIGHT, buff=0.2)
            grp.add(VGroup(lb, bar, vl))
        self.at("gets a tenth")
        for r in grp:
            self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.5)
        self.at("rough average")
        rule = T("a rough average, not a law", 32, GOLD).move_to([0, -2.7, 0])
        self.play(FadeIn(rule, shift=UP * 0.1), run_time=0.7)
        self.at("Keep rates")
        self.play(Indicate(rule, color=GOLD, scale_factor=1.06), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Keep rates in matching units, and keep the detritus."
