"""Nutrient cycling: nitrogen leaves when trees go  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = pools and plants (soil organic N, plants, trees)
  GREEN  = inputs (deposition, fixation); also a net gain
  RED    = outputs (stream, gas loss, nitrate washing out); also a net loss
  YELLOW = the internal loop (mineralisation, 90)
  ORANGE = the cut and herbicide
  GOLD   = the budget rule
  GREY   = boundary, labels, the uncut reference
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
MINUS = "−"
BX, BY, BW, BH = 0.0, -0.1, 8.0, 4.6      # the boundary
SOIL_P = np.array([-2.3, -0.3, 0.0])
PLANT_P = np.array([2.7, -0.3, 0.0])
IN_Y = [1.3, -0.6]
OUT_Y = [1.3, -0.6]
UNITS = "invented numbers · kg N per hectare per year"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=14)


def boundary(dashed=True):
    r = RoundedRectangle(corner_radius=0.3, width=BW, height=BH, stroke_color=GREY, stroke_width=4).move_to([BX, BY, 0])
    return DashedVMobject(r, num_dashes=60, dashed_ratio=0.55) if dashed else r


def tag(text, pos, color=GREY, size=24):
    return T(text, size, color).move_to(pos)


def pool_chips():
    soil = chip("Soil organic N", BLUE, 26).move_to(SOIL_P)
    plant = chip("Plants", BLUE, 26).move_to(PLANT_P)
    return soil, plant


def flux_arrows():
    """deposition, fixation in; stream, gas loss out. Returns dict of (arrow, label)."""
    d = {}
    d["dep"] = (arr([-6.3, IN_Y[0], 0], [-4.0, IN_Y[0], 0], GREEN), tag("deposition 8", [-5.15, IN_Y[0] + 0.42, 0], GREEN))
    d["fix"] = (arr([-6.3, IN_Y[1], 0], [-4.0, IN_Y[1], 0], GREEN), tag("fixation 6", [-5.15, IN_Y[1] + 0.42, 0], GREEN))
    d["str"] = (arr([4.0, OUT_Y[0], 0], [6.3, OUT_Y[0], 0], RED), tag("stream 3", [5.15, OUT_Y[0] + 0.42, 0], RED))
    d["gas"] = (arr([4.0, OUT_Y[1], 0], [6.3, OUT_Y[1], 0], RED), tag("gas loss 2", [5.15, OUT_Y[1] + 0.42, 0], RED))
    return d


def loop_arrows():
    up = arr(SOIL_P + np.array([1.6, 0.18, 0]), PLANT_P + np.array([-1.15, 0.18, 0]), YELLOW, 8)
    dn = arr(PLANT_P + np.array([-1.15, -0.18, 0]), SOIL_P + np.array([1.6, -0.18, 0]), YELLOW, 8)
    lab = M("90", 28, YELLOW).move_to([0.5, 0.55, 0])
    return up, dn, lab


def tri(h=0.9, w=0.72, color=BLUE):
    return Polygon([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [0, h / 2, 0], stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.4)


def stump(color=GREY):
    return Rectangle(width=0.4, height=0.22, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.5)


class S00Title(TitleCard):
    LESSON = "Nutrient cycling"
    TITLE = "Nitrogen leaves when trees go"


# ---------------------------------------------------------------------------------------------
class S01Cut(SpokenScene):
    def construct(self):
        top = T("Hubbard Brook, New Hampshire", 26, GREY).move_to([0, 3.35, 0])
        cx = [-3.4, 3.4]
        boxes = [RoundedRectangle(corner_radius=0.3, width=4.8, height=3.3, stroke_color=GREY, stroke_width=4).move_to([x, 0.45, 0]) for x in cx]
        offs = [(dx, dy) for dy in (0.6, -0.55) for dx in (-1.2, 0, 1.2)]
        trees = [VGroup(*[tri().move_to([x + dx, 0.45 + dy, 0]) for dx, dy in offs]) for x in cx]
        h_l = T("uncut watershed", 26, GREY).move_to([cx[0], 2.65, 0])
        h_r = T("cut, regrowth suppressed", 26, ORANGE).move_to([cx[1], 2.65, 0])
        s_l = arr([cx[0], -1.2, 0], [cx[0], -2.45, 0], RED, 4)
        s_r0 = arr([cx[1], -1.2, 0], [cx[1], -2.45, 0], RED, 4)
        n_l = T("nitrate in stream", 24, RED).move_to([cx[0], -2.95, 0])
        n_r = T("nitrate in stream", 24, RED).move_to([cx[1], -2.95, 0])
        self.play(FadeIn(top), *[Create(b) for b in boxes], FadeIn(trees[0]), FadeIn(trees[1]), FadeIn(h_l), run_time=0.8)
        self.play(GrowArrow(s_l), GrowArrow(s_r0), FadeIn(n_l), FadeIn(n_r), run_time=0.5)
        self.at("cut the forest")
        stumps = VGroup(*[stump().move_to([cx[1] + dx, 0.45 + dy - 0.3, 0]) for dx, dy in offs])
        self.play(ReplacementTransform(trees[1], stumps), run_time=1.0)
        self.at("used herbicide")
        self.play(FadeIn(h_r, shift=UP * 0.1), run_time=0.6)
        self.at("far more nitrate")
        s_r = arr([cx[1], -1.2, 0], [cx[1], -2.45, 0], RED, 20, tip=0.5)
        self.play(ReplacementTransform(s_r0, s_r), run_time=0.8)
        self.at("had been there all along")
        dots = VGroup(*[Dot(radius=0.09, color=BLUE).move_to([cx[1] + dx, 0.45 + dy - 0.3, 0]) for dx, dy in offs])
        dots2 = VGroup(*[Dot(radius=0.09, color=BLUE).move_to([cx[0] + dx, 0.45 + dy - 0.3, 0]) for dx, dy in offs])
        ntag = T("nitrogen", 24, BLUE).move_to([0, -0.7, 0])
        self.play(FadeIn(dots), FadeIn(dots2), FadeIn(ntag), run_time=0.6)
        self.at("where it went")
        self.play(*[d.animate.move_to([cx[1] + (i - 2.5) * 0.12, -1.9 - 0.0 * i, 0]).set_color(RED) for i, d in enumerate(dots)],
                  run_time=1.4)
        q = T("?", 100, YELLOW, weight=BOLD).move_to([0, 0.45, 0])
        self.at("How would you know")
        self.play(FadeIn(q, scale=0.6), FadeOut(ntag), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Accounts(SpokenScene):
    def construct(self):
        soil, plant = pool_chips()
        bnd = boundary()
        self.at("Keep accounts")
        self.play(FadeIn(soil, shift=UP * 0.1), FadeIn(plant, shift=UP * 0.1), run_time=0.8)
        self.at("A pool is")
        pl = tag("pools: amounts held", [0.0, -1.55, 0], BLUE)
        self.play(Indicate(soil, color=BLUE), Indicate(plant, color=BLUE), FadeIn(pl), run_time=1.2)
        self.at("A flux is")
        a_in = arr([-6.3, 0.9, 0], [-4.0 + 0.3, 0.9, 0], GREEN)
        a_out = arr([3.7, -0.6, 0], [6.3, -0.6, 0], RED)
        self.play(FadeOut(pl), run_time=0.3)
        fl = tag("fluxes: transfers", [0.0, -1.55, 0], GREEN)
        self.play(GrowArrow(a_in), FadeIn(fl), run_time=0.7)
        self.at("deposit")
        l_in = tag("deposit", [-5.15, 1.32, 0], GREEN)
        self.play(FadeIn(l_in), run_time=0.4)
        self.at("withdrawal")
        l_out = tag("withdrawal", [5.0, -0.18, 0], RED)
        self.play(GrowArrow(a_out), FadeIn(l_out), run_time=0.7)
        self.at("Draw a boundary")
        self.play(FadeOut(fl), Create(bnd), run_time=1.4)
        bt = tag("boundary", [-2.8, 1.65, 0])
        self.play(FadeIn(bt), run_time=0.4)
        self.at("such as a year")
        yr = tag("interval: one year", [2.5, 1.65, 0], GREY)
        self.play(FadeIn(yr), run_time=0.6)
        self.at("one rule holds")
        rule = T(f"change in stock = inputs {MINUS} outputs", 36, GOLD).move_to([0, -3.1, 0])
        self.play(Write(rule), run_time=1.6)
        self.at("Change in stock")
        self.play(Indicate(rule, color=GOLD, scale_factor=1.06), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Numbers(SpokenScene):
    def construct(self):
        soil, plant = pool_chips()
        bnd = boundary(dashed=False)
        fa = flux_arrows()
        units = T(UNITS, 24, GREY).move_to([0, 3.4, 0])
        self.play(Create(bnd), FadeIn(soil), FadeIn(plant), run_time=0.5)
        self.at("invented forest")
        self.play(FadeIn(units), run_time=0.4)
        self.at("illustrative")
        self.play(Indicate(units, color=TEXT, scale_factor=1.08), run_time=1.0)
        self.at("per hectare per year")
        self.play(Indicate(units, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.at("Deposition from the air")
        self.play(GrowArrow(fa["dep"][0]), FadeIn(fa["dep"][1]), run_time=0.7)
        self.at("Fixation brings")
        self.play(GrowArrow(fa["fix"][0]), FadeIn(fa["fix"][1]), run_time=0.7)
        self.at("The stream carries")
        self.play(GrowArrow(fa["str"][0]), FadeIn(fa["str"][1]), run_time=0.7)
        self.at("returns 2")
        self.play(GrowArrow(fa["gas"][0]), FadeIn(fa["gas"][1]), run_time=0.7)
        t_in = T("in: 8 + 6 = 14", 30, GREEN).move_to([-4.0, -3.2, 0])
        t_out = T("out: 3 + 2 = 5", 30, RED).move_to([4.0, -3.2, 0])
        self.at("Inputs are")
        self.play(Write(t_in), run_time=0.9)
        self.at("Outputs are")
        self.play(Write(t_out), run_time=0.9)
        self.at("The forest gains")
        net = T(f"14 {MINUS} 5 = +9", 38, GREEN, weight=BOLD).move_to([0, -3.2, 0])
        self.play(Write(net), soil.animate.scale(1.12), plant.animate.scale(1.12), run_time=1.0)
        self.at("stored in wood")
        note = tag("stored in wood and soil", [0, -1.55, 0], BLUE)
        self.play(FadeIn(note), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Inside(SpokenScene):
    def construct(self):
        soil, plant = pool_chips()
        bnd = boundary(dashed=False)
        fa = flux_arrows()
        allfa = VGroup(*[m for v in fa.values() for m in v])
        self.add(bnd, soil, plant, allfa)
        self.play(allfa.animate.set_opacity(0.4), run_time=0.6)
        self.at("soil organic nitrogen")
        amt = M("4,500", 28, BLUE).next_to(soil, DOWN, buff=0.25)
        self.play(Indicate(soil, color=BLUE), FadeIn(amt), run_time=1.0)
        self.at("Decomposers release")
        up, dn, lab = loop_arrows()
        self.play(GrowArrow(up), FadeIn(lab), run_time=0.8)
        self.at("as ammonium")
        self.play(Indicate(lab, color=YELLOW, scale_factor=1.4), run_time=0.8)
        self.at("Plants take it up")
        self.play(Indicate(plant, color=BLUE), run_time=0.8)
        self.at("about six times")
        b1 = Rectangle(width=14 * 0.07, height=0.32, stroke_width=0, fill_color=GREEN, fill_opacity=0.9)
        b2 = Rectangle(width=90 * 0.07, height=0.32, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        b1.move_to([-2.8 + b1.width / 2, -3.0, 0]); b2.move_to([-2.8 + b2.width / 2, -3.5, 0])
        l1 = T("inputs 14", 24, GREEN).move_to([-4.15, -3.0, 0])
        l2 = T("flux 90", 24, YELLOW).move_to([-4.25, -3.5, 0])
        self.play(FadeIn(l1), GrowFromEdge(b1, LEFT), run_time=0.5)
        self.play(FadeIn(l2), GrowFromEdge(b2, LEFT), run_time=1.0)
        self.at("never appeared")
        self.play(FadeOut(VGroup(b1, b2, l1, l2)), allfa.animate.set_opacity(0.2), run_time=0.6)
        self.at("so they cancel")
        out_l = T(f"{MINUS}90 from soil", 26, YELLOW).move_to([-2.2, 1.55, 0])
        in_l = T("+90 into plants", 26, YELLOW).move_to([2.2, 1.55, 0])
        self.play(FadeIn(out_l), FadeIn(in_l), run_time=0.7)
        zero = M(f"{MINUS}90 + 90 = 0", 36, YELLOW).move_to([0, -1.75, 0])
        self.play(Write(zero), run_time=1.0)
        self.at("does not mean")
        self.wait(0.2)
        self.at("largest flux")
        self.play(Indicate(up, color=YELLOW, scale_factor=1.15), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Cut(SpokenScene):
    def construct(self):
        soil, plant = pool_chips()
        bnd = boundary(dashed=False)
        fa = flux_arrows()
        up, dn, lab = loop_arrows()
        amt = M("4,500", 28, BLUE).next_to(soil, DOWN, buff=0.25)
        self.add(bnd, soil, plant, up, lab, *[m for v in fa.values() for m in v])
        self.at("cut the forest")
        cutl = T("forest cut, regrowth suppressed", 28, ORANGE).move_to([0, 3.35, 0])
        self.play(FadeIn(cutl), plant.animate.set_color(GREY), up.animate.set_color(GREY), lab.animate.set_color(GREY), run_time=0.9)
        self.at("Plant uptake stops")
        blk = Line([PLANT_P[0] - 1.15, 0.0, 0], [PLANT_P[0] - 1.15, 0.4, 0], color=RED, stroke_width=8)
        self.play(FadeOut(lab), FadeIn(blk), run_time=0.8)
        self.at("keep releasing ammonium")
        rel = T("ammonium released", 24, YELLOW).move_to(SOIL_P + np.array([0.0, 1.0, 0]))
        self.play(FadeIn(rel), run_time=0.5)
        self.at("turn it into nitrate")
        nit = T("nitrate", 24, RED).move_to(SOIL_P + np.array([0.0, 1.0, 0]))
        self.play(ReplacementTransform(rel, nit), run_time=0.6)
        self.at("washes out")
        route = Line(SOIL_P + np.array([0, 0.4, 0]), [-2.2, 1.3, 0])
        dots = [Dot(radius=0.12, color=RED).move_to(SOIL_P + np.array([0, 0.4, 0])) for _ in range(5)]
        self.add(*dots)
        anims = []
        for i, d in enumerate(dots):
            path = VMobject().set_points_as_corners([SOIL_P + np.array([0, 0.4, 0]), np.array([SOIL_P[0], 1.3, 0]), np.array([4.0, 1.3, 0]), np.array([5.6, 1.3, 0])])
            anims.append(Succession(Wait(0.2 * i), MoveAlongPath(d, path, run_time=1.5, rate_func=linear)))
        self.play(AnimationGroup(*anims), run_time=2.3)
        self.at("rises to")
        thick = arr([4.0, OUT_Y[0], 0], [6.3, OUT_Y[0], 0], RED, 22, tip=0.55)
        lab40 = tag("stream 40", [5.15, OUT_Y[0] + 0.55, 0], RED)
        self.play(ReplacementTransform(fa["str"][0], thick), ReplacementTransform(fa["str"][1], lab40), FadeOut(nit), run_time=0.9)
        self.at("Outputs are now")
        t_out = T("out: 40 + 2 = 42", 30, RED).move_to([4.0, -3.2, 0])
        t_in = T("in: 8 + 6 = 14", 30, GREEN).move_to([-4.0, -3.2, 0])
        self.play(Write(t_out), FadeIn(t_in), run_time=1.0)
        self.at("a loss of")
        net = T(f"14 {MINUS} 42 = {MINUS}28", 38, RED, weight=BOLD).move_to([0, -3.2, 0])
        self.play(Write(net), soil.animate.scale(0.9), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Rule(SpokenScene):
    def construct(self):
        ax_y = 0.8
        sc = 0.08
        axis = Line([-5.0, ax_y, 0], [5.0, ax_y, 0], color=GREY, stroke_width=3)
        tl = T(f"net change, kg N per hectare per year · {chr(0x201c)}in this sketch{chr(0x201d)}: invented", 22, GREY)
        tl = VGroup(T("invented numbers", 34, ORANGE, weight=BOLD), T("net change, kg N per hectare per year", 24, GREY)).arrange(DOWN, buff=0.1).move_to([0, 3.2, 0])
        b1 = Rectangle(width=1.6, height=9 * sc, stroke_width=0, fill_color=GREEN, fill_opacity=0.9)
        b1.move_to([-2.4, ax_y + 9 * sc / 2, 0])
        b2 = Rectangle(width=1.6, height=28 * sc, stroke_width=0, fill_color=RED, fill_opacity=0.9)
        b2.move_to([2.4, ax_y - 28 * sc / 2, 0])
        v1 = T("+9 invented", 34, GREEN, weight=BOLD).next_to(b1, UP, buff=0.15)
        v2 = T(f"{MINUS}28 invented", 34, RED, weight=BOLD).next_to(b2, DOWN, buff=0.15)
        n1 = T("forest intact", 26, TEXT).move_to([-2.4, ax_y - 0.45, 0])
        n2 = T("after the cut", 26, ORANGE).move_to([2.4, ax_y + 0.45, 0])
        self.play(FadeIn(tl), Create(axis), run_time=0.6)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(n1), FadeIn(v1), GrowFromEdge(b2, UP), FadeIn(n2), FadeIn(v2), run_time=1.2)
        self.at("That size is invented")
        self.play(Indicate(tl, color=GREY), run_time=0.8)
        self.at("stream losses of nitrate")
        real = VGroup(T("Real Hubbard Brook result, 1970:", 26, TEAL, weight=BOLD),
                      T("stream losses of nitrate and calcium rose above the uncut reference", 26, TEXT),
                      T("the direction, not this size", 26, YELLOW)).arrange(DOWN, buff=0.18)
        fit(real, 11.5)
        real.move_to([0, -3.0, 0])
        sep = DashedLine([-6.2, -2.3, 0], [6.2, -2.3, 0], color=TEAL, stroke_width=3)
        self.play(Create(sep), FadeIn(real[0]), FadeIn(real[1]), run_time=1.0)
        self.at("shows the direction")
        self.play(FadeIn(real[2]), run_time=0.6)
        self.at("What changed was")
        self.play(b1.animate.set_opacity(0.35), v1.animate.set_opacity(0.35), run_time=0.8)
        self.at("Keep the rule")
        self.play(FadeOut(VGroup(real, sep, tl, axis, b1, b2, v1, v2, n1, n2)), run_time=0.6)
        rule = T(f"change in stock = inputs {MINUS} outputs", 44, GOLD).move_to([0, 0.5, 0])
        sub = T("for a stated boundary and interval", 32, GREY).move_to([0, -0.5, 0])
        self.play(Write(rule), run_time=1.2)
        self.play(FadeIn(sub), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Change in stock equals inputs minus outputs, for a stated boundary."
